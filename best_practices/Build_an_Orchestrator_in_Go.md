# Per-Book Best Practices — Deep Dive: Build an Orchestrator in Go (From Scratch)

# Build an Orchestrator in Go (From Scratch)
**Author:** Tim Boring (Manning, 2024)
**Topic tags:** `#architecture` `#go` `#systems` `#concurrency` `#cloud`
**Language focus:** Go-first
**Sources:** `markdown_output/Build_an_Orchestrator_in_Go_From_Scratch_-_Tim_Boring/Build_an_Orchestrator_in_Go_From_Scratch_-_Tim_Boring.md` · `summaries/Build_an_Orchestrator_in_Go_From_Scratch_-_Tim_Boring.md`

## TL;DR
Tim Boring builds "Cube" — a tiny but real container orchestrator in <3,000 lines of Go — by translating the Borg/Kubernetes/Nomad mental model into skeleton structs (`Task`, `Worker`, `Manager`, `Scheduler`, `Node`), then fleshing them out with the Docker SDK, a chi-based HTTP API, goprocinfo metrics, a state-machine for task lifecycle, a pluggable `Scheduler` interface (round-robin + E-PVM), a `Store` interface (in-memory map + BoltDB), health-check-driven restarts, and a Cobra CLI. Apply it whenever you need to design a manager/worker (control-plane/data-plane) system in Go, a stateful reconciliation loop, or a swappable-by-interface architecture.

---

## Best Practices by Topic

### 1. Mental Model First: Five Core Components #architecture

**Principle:** Every orchestrator decomposes into the same five building blocks: *manager*, *worker*, *scheduler*, *task*, *storage*. Different products use different names (BorgMaster/Borglet, control-plane/kubelet, server/client, master/agent) but the architecture is invariant.

**Do:**
- Map your domain onto these five concepts before writing code.
- Use the manager/worker split to separate *administrative* concerns (scheduling, state, recovery) from *execution* concerns (running tasks).
- Treat the scheduler as a pluggable brain and storage as a pluggable memory — both behind interfaces.

**Don't:**
- Don't conflate "worker the component" with "worker the machine"; the worker component is software that *runs on* a node.
- Don't try to build distributed consensus, service discovery, load balancing, and security into v1 — strip the orchestrator to its core.

*Ref: Build_an_Orchestrator_in_Go.md — "1.5 The components of an orchestration system"*

---

### 2. Container vs. VM — Know What You're Orchestrating #cloud

**Principle:** A container is not a concrete technical object like a VM; it's shorthand for *Linux namespaces + cgroups*. Containers share the host kernel; VMs ship a full guest kernel. This is why containers start in milliseconds and pack densely.

**Do:**
- Use containers as the unit of work so your orchestrator doesn't have to reason about per-OS idiosyncrasies.
- Standardize on a single container runtime (Docker SDK here) to scope v1.

**Don't:**
- Don't pretend containers give the same isolation guarantees as VMs.
- Don't reinvent container creation — reuse the Docker Go SDK that powers the `docker` CLI.

*Ref: Build_an_Orchestrator_in_Go.md — "1.3 What is a container, and how is it different from a virtual machine?"*

---

### 3. Project Layout Mirrors the Mental Model #architecture #go

**Principle:** Each major concept gets its own package directory; the layout is the documentation of the architecture.

**Code:**
```
.
├── main.go
├── manager
│   └── manager.go
├── node
│   └── node.go
├── scheduler
│   └── scheduler.go
├── task
│   └── task.go
└── worker
    └── worker.go
```
*Ref: Build_an_Orchestrator_in_Go.md — "2. From mental model to skeleton code"*

---

### 4. Modeling Task State as an `iota` Enum #go

**Principle:** Encode the legal task states as a typed `iota` so the compiler enforces them.

**Code:**
```go
package task
type State int
const (
 Pending State = iota
 Scheduled
 Running
 Completed
 Failed
)
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.1 The State type"*

**Do:** Keep states small and terminal states (`Completed`, `Failed`) explicit.
**Don't:** Don't add a state without also updating the state-transition map.

---

### 5. The `Task` Struct — Resource + Identity + Lifecycle #go

**Principle:** A task aggregates identity (UUID + name), desired resources (CPU/Memory/Disk), Docker specifics (image, exposed ports, restart policy), and lifecycle timestamps.

**Code:**
```go
import(
 "..."
 "time"
)
type Task struct {
 ID uuid.UUID
 ContainerID string
 Name string
 State State
 Image string
 CPU float64
 Memory int64
 Disk int64
 ExposedPorts nat.PortSet
 PortBindings map[string]string
 RestartPolicy string
 StartTime time.Time
 FinishTime time.Time
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.4 Adding StartTime and FinishTime fields to the Task struct"*

---

### 6. `TaskEvent` — Desired-State Envelope #go

**Principle:** Separate *the task* (current state) from *the user's request to change it* with a `TaskEvent` wrapper. This is the poor-man's Kubernetes "spec vs status" split.

**Code:**
```go
type TaskEvent struct {
 ID uuid.UUID
 State State
 Timestamp time.Time
 Task Task
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.5 The TaskEvent struct"*

---

### 7. Worker Skeleton: Compose, Don't Reimplement #go

**Principle:** Compose a `Worker` from a `Queue` (from `golang-collections`) and an in-memory `Db` map rather than rolling your own.

**Code:**
```go
package worker
import (
 "fmt"
 "github.com/google/uuid"
 "github.com/golang-collections/collections/queue"
 "cube/task"
)
type Worker struct {
 Name string
 Queue queue.Queue
 Db map[uuid.UUID]*task.Task
 TaskCount int
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.6 The beginnings of the Worker struct"*

---

### 8. Stub Methods Early — `fmt.Println` Skeletons #go

**Principle:** Sketch every method first with a one-line print so the design compiles before you commit to behavior.

**Code:**
```go
func (w *Worker) CollectStats() {
 fmt.Println("I will collect stats")
}
func (w *Worker) RunTask() {
 fmt.Println("I will start or stop a task")
}
func (w *Worker) StartTask() {
 fmt.Println("I will start a task")
}
func (w *Worker) StopTask() {
 fmt.Println("I will stop a task")
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.7 The skeleton of the Worker component"*

---

### 9. Manager Skeleton with Reverse-Lookup Maps #go #architecture

**Principle:** A manager needs forward and reverse indices — `WorkerTaskMap` (worker → task IDs) and `TaskWorkerMap` (task ID → worker) — so any direction is O(1).

**Code:**
```go
package manager
import(
 "cube/task"
 "fmt"
 "github.com/golang-collections/collections/queue"
 "github.com/google/uuid"
)
type Manager struct {
 Pending queue.Queue
 TaskDb map[string][]*task.Task
 EventDb map[string][]*task.TaskEvent
 Workers []string
 WorkerTaskMap map[string][]uuid.UUID
 TaskWorkerMap map[uuid.UUID]string
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.8 The beginnings of our Manager skeleton"*

---

### 10. Scheduler as an Interface (Three Phases) #go #architecture

**Principle:** Scheduling has three universal phases — *select candidate nodes*, *score*, *pick*. Encode them in an interface so multiple algorithms can coexist.

**Code:**
```go
package scheduler
type Scheduler interface {
 SelectCandidateNodes()
 Score()
 Pick()
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.10 The skeleton of the Scheduler component"*

**Do:** Refine signatures later (Listing 10.1) — the initial bare interface is enough to drive the design.

---

### 11. `Node` — Physical/Machine Facet of a Worker #go

**Principle:** Decouple *what the worker does* (logical) from *what the machine has* (physical) via a `Node` struct carrying capacity (`Memory`, `Disk`, `Cores`) and allocation counters.

**Code:**
```go
package node
type Node struct {
 Name string
 Ip string
 Cores int
 Memory int
 MemoryAllocated int
 Disk int
 DiskAllocated int
 Role string
 TaskCount int
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.11 The Node struct, representing a physical machine"*

---

### 12. Skeleton Wiring — Smoke-Test Main #go

**Principle:** After writing skeletons, write a throw-away `main.go` that instantiates everything and calls every method. If it compiles and prints, the architecture is coherent.

**Code:**
```go
package main
import (
 "cube/node"
 "cube/task"
 "fmt"
 "time"
 "github.com/golang-collections/collections/queue"
 "github.com/google/uuid"
 "cube/manager"
 "cube/worker"
)
func main() {
 t := task.Task{
 ID: uuid.New(),
 Name: "Task-1",
 State: task.Pending,
 Image: "Image-1",
 Memory: 1024,
 Disk: 1,
 }
 te := task.TaskEvent{
 ID: uuid.New(),
 State: task.Pending,
 Timestamp: time.Now(),
 Task: t,
 }
 fmt.Printf("task: %v\n", t)
 fmt.Printf("task event: %v\n", te)
 w := worker.Worker{
 Name: "worker-1",
 Queue: *queue.New(),
 Db: make(map[uuid.UUID]*task.Task),
 }
 fmt.Printf("worker: %v\n", w)
 w.CollectStats()
 w.RunTask()
 w.StartTask()
 w.StopTask()
 m := manager.Manager{
 Pending: *queue.New(),
 TaskDb: make(map[string][]task.Task),
 EventDb: make(map[string][]task.TaskEvent),
 Workers: []string{w.Name},
 }
 fmt.Printf("manager: %v\n", m)
 m.SelectWorker()
 m.UpdateTasks()
 m.SendWork()
 n := node.Node{
 Name: "Node-1",
 Ip: "192.168.1.1",
 Cores: 4,
 Memory: 1024,
 Disk: 25,
 Role: "worker",
 }
 fmt.Printf("node: %v\n", n)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 2.13 / 2.14 Testing the skeletons with a minimal program"*

---

### 13. Drive Docker via the Go SDK, Not Raw HTTP #go #cloud

**Principle:** Use the official Docker Go SDK (`github.com/docker/docker/client`) — it's the same code path the `docker` CLI uses, and it abstracts HTTP, serialization, and unix-socket details.

**Do:**
- Use `NewClientWithOpts`, `ImagePull`, `ContainerCreate`, `ContainerStart`, `ContainerStop`, `ContainerRemove`.

**Don't:**
- Don't shell out to `docker ...` from Go; the SDK is idiomatically cheaper and gives typed responses.

*Ref: Build_an_Orchestrator_in_Go.md — "3.2 Docker: Starting, stopping, and inspecting containers from the API"*

---

### 14. `Config` Struct — Task → Docker Translation Layer #go

**Principle:** Keep your orchestrator's `Config` separate from Docker's `container.Config` so the rest of the system never imports Docker types.

**Code:**
```go
type Config struct {
 Name string
 AttachStdin bool
 AttachStdout bool
 AttachStderr bool
 ExposedPorts nat.PortSet
 Cmd []string
 Image string
 Cpu float64
 Memory int64
 Disk int64
 Env []string
 RestartPolicy string
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.6 The Config struct that will hold the configuration for orchestration tasks"*

---

### 15. `Docker` Wrapper + `DockerResult` — Encapsulate Side Effects #go

**Principle:** Wrap the Docker client in a struct that returns a uniform `DockerResult` from every action; this lets callers handle errors and metadata uniformly.

**Code:**
```go
type Docker struct {
 Client *client.Client
 Config Config
}
```
```go
type DockerResult struct {
 Error error
 Action string
 ContainerId string
 Result string
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.7 The Docker struct / Listing 3.8 The DockerResult struct"*

---

### 16. `Run()` — Pull → Create → Start → Logs #go #cloud

**Principle:** A "run" decomposes into the four SDK calls. Check `err` after each and short-circuit by returning a populated `DockerResult`.

**Code (image-pull phase):**
```go
func (d *Docker) Run() DockerResult {
 ctx := context.Background()
 reader, err := d.Client.ImagePull(
 ctx, d.Config.Image, types.ImagePullOptions{})
 if err != nil {
 log.Printf("Error pulling image %s: %v\n", d.Config.Image, err)
 return DockerResult{Error: err}
 }
 io.Copy(os.Stdout, reader)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.9 The start of our Run() method"*

---

### 17. Translate Cube `Config` → Docker `container.Config`/`HostConfig` #go

**Principle:** Cross the boundary once, in one place: copy fields into Docker's `container.Config`, `container.HostConfig` (with `RestartPolicy`, `Resources`, `PublishAllPorts`).

**Code:**
```go
rp := container.RestartPolicy{
 Name: d.Config.RestartPolicy,
}
r := container.Resources{
 Memory: d.Config.Memory,
 NanoCPUs: int64(d.Config.Cpu * math.Pow(10, 9)),
}
cc := container.Config{
 Image: d.Config.Image,
 Tty: false,
 Env: d.Config.Env,
 ExposedPorts: d.Config.ExposedPorts,
}
hc := container.HostConfig{
 RestartPolicy: rp,
 Resources: r,
 PublishAllPorts: true,
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.11 The next phase of running a container"*

**Do:** Set `PublishAllPorts: true` so Docker auto-allocates host ports instead of forcing the user to pick.

---

### 18. Create + Start + Capture Logs #go

**Code:**
```go
func (d *Docker) Run() DockerResult {
 // previous code not listed
 resp, err := d.Client.ContainerCreate(ctx, &cc, &hc, nil, nil,
 ➥ d.Config.Name)
 if err != nil {
 log.Printf("Error creating container using image %s: %v\n",
 ➥ d.Config.Image, err)
 return DockerResult{Error: err}
 }
 err = d.Client.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{})
 if err != nil {
 log.Printf("Error starting container %s: %v\n", resp.ID, err)
 return DockerResult{Error: err}
 }
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.12 The penultimate phase"*

```go
func (d *Docker) Run() DockerResult {
 // previous code not listed
 d.Config.Runtime.ContainerID = resp.ID
 out, err := cli.ContainerLogs(
 ctx,
 resp.ID,
 types.ContainerLogsOptions{ShowStdout: true, ShowStderr: true}
 )
 if err != nil {
 log.Printf("Error getting logs for container %s: %v\n", resp.ID, err)
 return DockerResult{Error: err}
 }
 stdcopy.StdCopy(os.Stdout, os.Stderr, out)
 return DockerResult{ContainerId: resp.ID, Action: "start",
 ➥ Result: "success"}
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.13 The final phase of creating and running a container"*

---

### 19. `Stop()` — Stop + Remove #go

**Code:**
```go
func (d *Docker) Stop(id string) DockerResult {
 log.Printf("Attempting to stop container %v", id)
 ctx := context.Background()
 err := d.Client.ContainerStop(ctx, id, nil)
 if err != nil {
 log.Printf("Error stopping container %s: %v\n", id, err)
 return DockerResult{Error: err}
 }
 err = d.Client.ContainerRemove(ctx, id, types.ContainerRemoveOptions{
 RemoveVolumes: true,
 RemoveLinks: false,
 Force: false,
 })
 if err != nil {
 log.Printf("Error removing container %s: %v\n", id, err)
 return DockerResult{Error: err}
 }
 return DockerResult{Action: "stop", Result: "success", Error: nil}
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.14 Stopping a container"*

---

### 20. Helper Functions for `main.go` Demos #go

**Code:**
```go
func createContainer() (*task.Docker, *task.DockerResult) {
 c := task.Config{
 Name: "test-container-1",
 Image: "postgres:13",
 Env: []string{
 "POSTGRES_USER=cube",
 "POSTGRES_PASSWORD=secret",
 },
 }
 dc, _ := client.NewClientWithOpts(client.FromEnv)
 d := task.Docker{
 Client: dc,
 Config: c,
 }
 result := d.Run()
 if result.Error != nil {
 fmt.Printf("%v\n", result.Error)
 return nil, nil
 }
 fmt.Printf(
 "Container %s is running with config %v\n", result.ContainerId, c)
 return &d, &result
}
```
```go
func stopContainer(d *task.Docker, id string) *task.DockerResult {
 result := d.Docker.Stop(id)
 if result.Error != nil {
 fmt.Printf("%v\n", result.Error)
 return nil
 }
 fmt.Printf(
 "Container %s has been stopped and removed\n", result.ContainerId)
 return &result
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 3.15 / 3.16 The createContainer / stopContainer functions"*

---

### 21. Worker `StopTask` — Bookkeeping After SDK Call #go

**Principle:** After calling `d.Stop`, update `FinishTime`, transition state to `Completed`, and persist to the worker's `Db` before returning.

**Code:**
```go
func (w *Worker) StopTask(t task.Task) task.DockerResult {
 config := task.NewConfig(&t)
 d := task.NewDocker(config)
 result := d.Stop(t.ContainerID)
 if result.Error != nil {
 log.Printf("Error stopping container %v: %v\n", t.ContainerID,
 ➥ result.Error)
 }
 t.FinishTime = time.Now().UTC()
 t.State = task.Completed
 w.Db[t.ID] = &t
 log.Printf("Stopped and removed container %v for task %v\n",
 ➥ t.ContainerID, t.ID)
 return result
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.5 Our implementation of the StopTask method"*

---

### 22. Worker `StartTask` — Set `StartTime`, Branch on Error #go

**Code:**
```go
func (w *Worker) StartTask(t task.Task) task.DockerResult {
 t.StartTime = time.Now().UTC()
 config := task.NewConfig(&t)
 d := task.NewDocker(config)
 result := d.Run()
 if result.Error != nil {
 log.Printf("Err running task %v: %v\n", t.ID, result.Error)
 t.State = task.Failed
 w.Db[t.ID] = &t
 return result
 }
 t.ContainerID = result.ContainerId
 t.State = task.Running
 w.Db[t.ID] = &t
 return result
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.7 Our implementation of the StartTask method"*

**Do:** Record `StartTime` on success-path only after a confirmed start; record `Failed` immediately on error.

---

### 23. Worker `AddTask` — Queue as Desired-State Inbox #go #concurrency

**Code:**
```go
func (w *Worker) AddTask(t task.Task) {
 w.Queue.Enqueue(t)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.8 The worker's AddTask method"*

**Principle:** The queue represents *desired* state; the Db represents *current* state. The worker's job is to reconcile the two.

---

### 24. Encode Valid Transitions in a `map[State][]State` #go #architecture

**Principle:** Don't scatter `if state == X` checks. Centralize the legal transitions in a single map and consult it through one helper.

**Code:**
```go
var stateTransitionMap = map[State][]State{
 Pending: []State{Scheduled},
 Scheduled: []State{Scheduled, Running, Failed},
 Running: []State{Running, Completed, Failed},
 Completed: []State{},
 Failed: []State{},
}
```
```go
func Contains(states []State, state State) bool {
 for _, s := range states {
 if s == state {
 return true
 }
 }
 return false
}
func ValidStateTransition(src State, dst State) bool {
 return Contains(stateTransitionMap[src], dst)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.10 / 4.11 The stateTransitionMap and helpers"*

**Do:** Make terminal states (`Completed`, `Failed`) map to empty slices — they're sinks.

---

### 25. `RunTask` — The Reconciliation Algorithm #go #concurrency

**Principle:** Dequeue → look up persisted task → validate transition → dispatch to `StartTask` or `StopTask` → surface an error on illegal transitions.

**Code:**
```go
func (w *Worker) RunTask() task.DockerResult {
 t := w.Queue.Dequeue()
 if t == nil {
 log.Println("No tasks in the queue")
 return task.DockerResult{Error: nil}
 }
 taskQueued := t.(task.Task)
 taskPersisted := w.Db[taskQueued.ID]
 if taskPersisted == nil {
 taskPersisted = &taskQueued
 w.Db[taskQueued.ID] = &taskQueued
 }
 var result task.DockerResult
 if task.ValidStateTransition(
 ➥ taskPersisted.State, taskQueued.State) {
 switch taskQueued.State {
 case task.Scheduled:
 result = w.StartTask(taskQueued)
 case task.Completed:
 result = w.StopTask(taskQueued)
 default:
 result.Error = errors.New("We should not get here")
 }
 } else {
 err := fmt.Errorf("Invalid transition from %v to %v",
 ➥ taskPersisted.State, taskQueued.State)
 result.Error = err
 }
 return result
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.12 Our implementation of the RunTask method"*

---

### 26. Worker `main` — Demonstrate Start/Stop Cycle #go

**Code:**
```go
func main() {
 db := make(map[uuid.UUID]*task.Task)
 w := worker.Worker{
 Queue: *queue.New(),
 Db: db,
 }
 t := task.Task{
 ID: uuid.New(),
 Name: "test-container-1",
 State: task.Scheduled,
 Image: "strm/helloworld-http",
 }
 fmt.Println("starting task")
 w.AddTask(t)
 result := w.RunTask()
 if result.Error != nil {
 panic(result.Error)
 }
 t.ContainerID = result.ContainerId
 fmt.Printf("task %s is running in container %s\n", t.ID, t.ContainerID)
 fmt.Println("Sleepy time")
 time.Sleep(time.Second * 30)
 fmt.Printf("stopping task %s\n", t.ID)
 t.State = task.Completed
 w.AddTask(t)
 result = w.RunTask()
 if result.Error != nil {
 panic(result.Error)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 4.13 Pulling everything together into a functioning worker"*

---

### 27. Worker API — REST Over chi Router #go #api

**Principle:** Wrap worker functionality in three routes: `GET /tasks`, `POST /tasks`, `DELETE /tasks/{taskID}`. Use chi because the standard `net/http` lacks parameterized routes.

| Method | Route | Status | Body |
|--------|-------|--------|------|
| GET | /tasks | 200 | List of tasks |
| POST | /tasks | 201 | — |
| DELETE | /tasks/{taskID} | 204 | — |

*Ref: Build_an_Orchestrator_in_Go.md — "5.1 Overview of the worker API / Table 5.2"*

---

### 28. `Api` Struct — Worker Pointer + Router #go #api

**Code:**
```go
 Worker *Worker
 Router *chi.Mux
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.3 The API struct that will power our worker"*

---

### 29. `StartTaskHandler` — Strict JSON Decoding #go #api

**Principle:** Use `json.NewDecoder(r.Body)` with `DisallowUnknownFields()` to catch typos and forward-incompatible payloads.

**Code:**
```go
func (a *Api) StartTaskHandler(w http.ResponseWriter, r *http.Request) {
 d := json.NewDecoder(r.Body)
 d.DisallowUnknownFields()
 te := task.TaskEvent{}
 err := d.Decode(&te)
 if err != nil {
 msg := fmt.Sprintf("Error unmarshalling body: %v\n", err)
 log.Printf(msg)
 w.WriteHeader(400)
 e := ErrResponse{
 HTTPStatusCode: 400,
 Message: msg,
 }
 json.NewEncoder(w).Encode(e)
 return
 }
 a.Worker.AddTask(te.Task)
 log.Printf("Added task %v\n", te.Task.ID)
 w.WriteHeader(201)
 json.NewEncoder(w).Encode(te.Task)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.4 The worker's StartTaskHandler method"*

**Do:** Return `201 Created` (not `200`) for POST that creates a resource, per RFC 7231.

---

### 30. `GetTasksHandler` — Trivial Pass-Through #go #api

**Code:**
```go
func (a *Api) GetTasksHandler(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.WriteHeader(200)
 json.NewEncoder(w).Encode(a.Worker.GetTasks())
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.5 The worker's GetTasksHandler"*

---

### 31. `StopTaskHandler` — Copy Before Mutating #go #api

**Principle:** The handler must not mutate the in-Db task pointer directly; copy first, set state to `Completed`, enqueue the copy. Otherwise the desired-state queue would already show `Completed`, making the worker reject the transition.

**Code:**
```go
func (a *Api) StopTaskHandler(w http.ResponseWriter, r *http.Request) {
 taskID := chi.URLParam(r, "taskID")
 if taskID == "" {
 log.Printf("No taskID passed in request.\n")
 w.WriteHeader(400)
 }
 tID, _ := uuid.Parse(taskID)
 _, ok := a.Worker.Db[tID]
 if !ok {
 log.Printf("No task with ID %v found", tID)
 w.WriteHeader(404)
 }
 taskToStop := a.Worker.Db[tID]
 taskCopy := *taskToStop
 taskCopy.State = task.Completed
 a.Worker.AddTask(taskCopy)
 log.Printf("Added task %v to stop container %v\n", taskToStop.ID,
 ➥ taskToStop.ContainerID)
 w.WriteHeader(204)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.6 The worker's StopTaskHandler"*

---

### 32. Route Registration with chi `Route`/`Post`/`Get` #go #api

**Code:**
```go
func (a *Api) initRouter() {
 a.Router = chi.NewRouter()
 a.Router.Route("/tasks", func(r chi.Router) {
 r.Post("/", a.StartTaskHandler)
 r.Get("/", a.GetTasksHandler)
 r.Route("/{taskID}", func(r chi.Router) {
 r.Delete("/", a.StopTaskHandler)
 })
 })
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.7 The initRouter() method"*

---

### 33. Serving the API — `http.ListenAndServe` #go #api

**Code:**
```go
func (a *Api) Start() {
 a.initRouter()
 http.ListenAndServe(fmt.Sprintf("%s:%d", a.Address, a.Port), a.Router)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.8 The Start() method"*

---

### 34. Background Loop Pattern with `go` + `time.Sleep` #go #concurrency

**Principle:** Run each long-lived concern (task processing, stats collection, health checks, manager updates) in its own goroutine that loops forever with a sleep. Simple, observable, debuggable.

**Code:**
```go
func main() {
 host := os.Getenv("CUBE_HOST")
 port, _ := strconv.Atoi(os.Getenv("CUBE_PORT"))
 fmt.Println("Starting Cube worker")
 w := worker.Worker{
 Queue: *queue.New(),
 Db: make(map[uuid.UUID]*task.Task),
 }
 api := worker.Api{Address: host, Port: port, Worker: &w}
 go runTasks(&w)
 api.Start()
}
```
```go
func runTasks(w *worker.Worker) {
 for {
 if w.Queue.Len() != 0 {
 result := w.RunTask()
 if result.Error != nil {
 log.Printf("Error running task: %v\n", result.Error)
 }
 } else {
 log.Printf("No tasks to process currently.\n")
 }
 log.Println("Sleeping for 10 seconds.")
 time.Sleep(10 * time.Second)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 5.9 / 5.10 Running our worker from main.go / runTasks function"*

**Don't:** Don't put the API loop and the task-processing loop in the same goroutine — they must run concurrently.

---

### 35. Read System Metrics From `/proc` #go #systems

**Principle:** Linux exposes CPU (`/proc/stat`), memory (`/proc/meminfo`), load (`/proc/loadavg`) through a pseudo-filesystem. Wrap with `goprocinfo` rather than parsing by hand.

**Do:** Use `linux.ReadStat`, `linux.ReadMemInfo`, `linux.ReadLoadAvg`, `linux.ReadDisk`.
**Don't:** Don't shell out to `top`/`free`/`df`; the library calls are cheaper and deterministic.

*Ref: Build_an_Orchestrator_in_Go.md — "6.2 Metrics available from the /proc filesystem"*

---

### 36. `Stats` Wrapper Type #go #systems

**Code:**
```go
type Stats struct {
 MemStats *linux.MemInfo
 DiskStats *linux.Disk
 CpuStats *linux.CPUStat
 LoadStats *linux.LoadAvg
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.4 The Stats type we'll use to hold all the worker's metrics"*

---

### 37. Memory Helper Methods #go

**Code:**
```go
func (s *Stats) MemTotalKb() uint64 {
 return s.MemStats.MemTotal
}
```
```go
func (s *Stats) MemAvailableKb() uint64 {
 return s.MemStats.MemAvailable
}
```
```go
func (s *Stats) MemUsedKb() uint64 {
 return s.MemStats.MemTotal - s.MemStats.MemAvailable
}
func (s *Stats) MemUsedPercent() uint64 {
 return s.MemStats.MemAvailable / s.MemStats.MemTotal
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.5 / 6.6 / 6.7 Memory helpers"*

---

### 38. Disk Helpers #go

**Code:**
```go
func (s *Stats) DiskTotal() uint64 {
 return s.DiskStats.All
}
func (s *Stats) DiskFree() uint64 {
 return s.DiskStats.Free
}
func (s *Stats) DiskUsed() uint64 {
 return s.DiskStats.Used
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.8 Helper methods for disk-related metrics"*

---

### 39. CPU Usage Percentage Algorithm #go #systems

**Principle:** Compute `(total - idle) / total` where `total = idle + nonIdle`. Guard against divide-by-zero.

**Code:**
```go
func (s *Stats) CpuUsage() float64 {
 idle := s.CpuStats.Idle + s.CpuStats.IOWait
 nonIdle := s.CpuStats.User + s.CpuStats.Nice + s.CpuStats.System +
 s.CpuStats.IRQ + s.CpuStats.SoftIRQ + s.CpuStats.Steal
 total := idle + nonIdle
 if total == 0 {
 return 0.00
 }
 return (float64(total) - float64(idle)) / float64(total)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.9 Using the CpuUsage() method to get CPU usage as a percentage"*

---

### 40. `GetStats()` + Per-Resource Helper Functions #go

**Code:**
```go
func GetStats() *Stats {
 return &Stats{
 MemStats: GetMemoryInfo(),
 DiskStats: GetDiskInfo(),
 CpuStats: GetCpuStats(),
 LoadStats: GetLoadAvg(),
 }
}
```
```go
func GetMemoryInfo() *linux.MemInfo {
 memstats, err := linux.ReadMemInfo("/proc/meminfo")
 if err != nil {
 log.Printf("Error reading from /proc/meminfo")
 return &linux.MemInfo{}
 }
 return memstats
}
// GetDiskInfo See https://godoc.org/github.com/c9s/goprocinfo/linux#Disk
func GetDiskInfo() *linux.Disk {
 diskstats, err := linux.ReadDisk("/")
 if err != nil {
 log.Printf("Error reading from /")
 return &linux.Disk{}
 }
 return diskstats
}
// GetCpuInfo See https://godoc.org/github.com/c9s/goprocinfo/linux#CPUStat
func GetCpuStats() *linux.CPUStat {
 stats, err := linux.ReadStat("/proc/stat")
 if err != nil {
 log.Printf("Error reading from /proc/stat")
 return &linux.CPUStat{}
 }
 return &stats.CPUStatAll
}
// GetLoadAvg See https://godoc.org/github.com/c9s/goprocinfo/linux#LoadAvg
func GetLoadAvg() *linux.LoadAvg {
 loadavg, err := linux.ReadLoadAvg("/proc/loadavg")
 if err != nil {
 log.Printf("Error reading from /proc/loadavg")
 return &linux.LoadAvg{}
 }
 return loadavg
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.10 / 6.11 GetStats and helpers"*

**Do:** On error, return a zero-valued struct so callers don't panic on nil.

---

### 41. `CollectStats` — Periodic Background Refresh #go #concurrency

**Code:**
```go
func (w *Worker) CollectStats() {
 for {
 log.Println("Collecting stats")
 w.Stats = GetStats()
 w.Stats.TaskCount = w.TaskCount
 time.Sleep(15 * time.Second)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.12 The worker's new CollectStats() method"*

---

### 42. `/stats` Handler and Route #go #api

**Code:**
```go
func (a *Api) GetStatsHandler(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.WriteHeader(200)
 json.NewEncoder(w).Encode(a.Worker.Stats)
}
```
```go
a.Router.Route("/stats", func(r chi.Router) {
 r.Get("/", a.GetStatsHandler)
})
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.13 / 6.14 GetStatsHandler and /stats route"*

---

### 43. Spawning Multiple Goroutines From `main` #go #concurrency

**Code:**
```go
func main() {
 host := os.Getenv("CUBE_HOST")
 port, _ := strconv.Atoi(os.Getenv("CUBE_PORT"))
 fmt.Println("Starting Cube worker")
 w := worker.Worker{
 Queue: *queue.New(),
 Db: make(map[uuid.UUID]*task.Task),
 }
 api := worker.Api{Address: host, Port: port, Worker: &w}
 go runTasks(&w)
 go w.CollectStats()
 api.Start()
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 6.15 Updating the main() function from our main.go file"*

---

### 44. Manager: Separation of Administrative vs. Execution Concerns #architecture

**Principle:** The manager is the *control plane* — it accepts user requests, schedules, tracks state, restarts failed tasks. The worker is the *data plane* — it actually runs containers. The two communicate only via the worker's HTTP API.

**Do:** Keep the manager stateless w.r.t. containers — it never calls Docker directly.
**Don't:** Don't let the manager's failure take down running tasks; they must keep running independently.

*Ref: Build_an_Orchestrator_in_Go.md — "7.1 The Cube manager / Control plane vs. data plane"*

---

### 45. Manager Struct — Final Shape #go

**Code:**
```go
package manager
import (
 "bytes"
 "cube/task"
 "cube/worker"
 "encoding/json"
 "fmt"
 "log"
 "net/http"
 "github.com/golang-collections/collections/queue"
 "github.com/google/uuid"
)
type Manager struct {
 Pending queue.Queue
 TaskDb map[uuid.UUID]*task.Task
 EventDb map[uuid.UUID]*task.TaskEvent
 Workers []string
 WorkerTaskMap map[string][]uuid.UUID
 TaskWorkerMap map[uuid.UUID]string
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.1 The Manager struct"*

---

### 46. Naive Round-Robin `SelectWorker` #go #architecture

**Principle:** The simplest possible scheduler tracks `LastWorker` index, increments, wraps to 0 at end of list.

**Code:**
```go
func (m *Manager) SelectWorker() string {
 var newWorker int
 if m.LastWorker+1 < len(m.Workers) {
 newWorker = m.LastWorker + 1
 m.LastWorker++
 } else {
 newWorker = 0
 m.LastWorker = 0
 }
 return m.Workers[newWorker]
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.4 Implementing a naive scheduling algorithm"*

**Don't:** This works only for a single worker; once you scale out, round-robin ignores task requirements.

---

### 47. `SendWork` — Pop, Schedule, Record, POST #go

**Principle:** The manager pops a `TaskEvent` from `Pending`, records it in `EventDb`, updates `WorkerTaskMap`/`TaskWorkerMap`, JSON-encodes, POSTs to worker, decodes response.

**Code:**
```go
func (m *Manager) SendWork() {
 if m.Pending.Len() > 0 {
 w := m.SelectWorker()
 e := m.Pending.Dequeue()
 te := e.(task.TaskEvent)
 t := te.Task
 log.Printf("Pulled %v off pending queue\n", t)
 m.EventDb[te.ID] = &te
 m.WorkerTaskMap[w] = append(m.WorkerTaskMap[w], te.Task.ID)
 m.TaskWorkerMap[t.ID] = w
 t.State = task.Scheduled
 m.TaskDb[t.ID] = &t
 data, err := json.Marshal(te)
 if err != nil {
 log.Printf("Unable to marshal task object: %v.\n", t)
 }
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.5 The manager's SendWork method"*

```go
 url := fmt.Sprintf("http://%s/tasks", w)
 resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
 if err != nil {
 log.Printf("Error connecting to %v: %v\n", w, err)
 m.Pending.Enqueue(te)
 return
 }
 d := json.NewDecoder(resp.Body)
 if resp.StatusCode != http.StatusCreated {
 e := worker.ErrResponse{}
 err := d.Decode(&e)
 if err != nil {
 fmt.Printf("Error decoding response: %s\n", err.Error())
 return
 }
 log.Printf("Response error (%d): %s", e.HTTPStatusCode, e.Message)
 return
 }
 t = task.Task{}
 err = d.Decode(&t)
 if err != nil {
 fmt.Printf("Error decoding response: %s\n", err.Error())
 return
 }
 log.Printf("%#v\n", t)
 } else {
 log.Println("No work in the queue")
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.6 The final two steps of the SendWork method"*

**Do:** On connection error, re-enqueue the event (`m.Pending.Enqueue(te)`) so it isn't lost.

---

### 48. `UpdateTasks` — Workers Are Source of Truth #go #architecture

**Principle:** Periodically poll each worker's `GET /tasks` and overwrite the manager's view. The worker's actual container state wins over the manager's bookkeeping.

**Code:**
```go
func (m *Manager) UpdateTasks() {
 for _, worker := range m.Workers {
 log.Printf("Checking worker %v for task updates", worker)
 url := fmt.Sprintf("http://%s/tasks", worker)
 resp, err := http.Get(url)
 if err != nil {
 log.Printf("Error connecting to %v: %v\n", worker, err)
 }
 if resp.StatusCode != http.StatusOK {
 log.Printf("Error sending request: %v\n", err)
 }
 d := json.NewDecoder(resp.Body)
 var tasks []*task.Task
 err = d.Decode(&tasks)
 if err != nil {
 log.Printf("Error unmarshalling tasks: %s\n", err.Error())
 }
}
```
```go
 for _, t := range tasks {
 log.Printf("Attempting to update task %v\n", t.ID)
 _, ok := m.TaskDb[t.ID]
 if !ok {
 log.Printf("Task with ID %s not found\n", t.ID)
 return
 }
 if m.TaskDb[t.ID].State != t.State {
 m.TaskDb[t.ID].State = t.State
 }
 m.TaskDb[t.ID].StartTime = t.StartTime
 m.TaskDb[t.ID].FinishTime = t.FinishTime
 m.TaskDb[t.ID].ContainerID = t.ContainerID
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.7 / 7.8 The two halves of UpdateTasks"*

---

### 49. Manager `AddTask` and `New` Helper #go

**Code:**
```go
func (m *Manager) AddTask(te task.TaskEvent) {
 m.Pending.Enqueue(te)
}
```
```go
func New(workers []string) *Manager {
 taskDb := make(map[uuid.UUID]*task.Task)
 eventDb := make(map[uuid.UUID]*task.TaskEvent)
 workerTaskMap := make(map[string][]uuid.UUID)
 taskWorkerMap := make(map[uuid.UUID]string)
 for worker := range workers {
 workerTaskMap[workers[worker]] = []uuid.UUID{}
 }
 return &Manager{
 Pending: *queue.New(),
 Workers: workers,
 TaskDb: taskDb,
 EventDb: eventDb,
 WorkerTaskMap: workerTaskMap,
 TaskWorkerMap: taskWorkerMap,
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.9 / 7.10 AddTask and New()"*

---

### 50. Anonymous Function for Periodic Manager Loop #go #concurrency

**Code:**
```go
go func() {
 for {
 fmt.Printf("[Manager] Updating tasks from %d workers\n", len(m.Workers))
 m.UpdateTasks()
 time.Sleep(15 * time.Second)
 }
}()
for {
 for _, t := range m.TaskDb {
 fmt.Printf("[Manager] Task: id: %s, state: %d\n", t.ID, t.State)
 time.Sleep(15 * time.Second)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 7.14 Using an anonymous function"*

---

### 51. Manager API — Reverse-Proxy Style #go #api

**Principle:** The manager API mirrors the worker API routes (`GET/POST/DELETE /tasks`) but operates cluster-wide. Internally it enqueues events; the manager's `ProcessTasks` goroutine actually dispatches them.

| Method | Route | Description |
|--------|-------|-------------|
| GET | /tasks | List all tasks cluster-wide |
| POST | /tasks | Submit a new task |
| DELETE | /tasks/{taskID} | Stop a task |

*Ref: Build_an_Orchestrator_in_Go.md — "8.2 Routes / Table 8.1"*

---

### 52. Manager API Struct & Handlers #go #api

**Code:**
```go
type Api struct {
 Address string
 Port int
 Manager *Manager
 Router *chi.Mux
}
```
```go
func (a *Api) StartTaskHandler(w http.ResponseWriter, r *http.Request) {
 d := json.NewDecoder(r.Body)
 d.DisallowUnknownFields()
 te := task.TaskEvent{}
 err := d.Decode(&te)
 if err != nil {
 msg := fmt.Sprintf("Error unmarshalling body: %v\n", err)
 log.Printf(msg)
 w.WriteHeader(400)
 e := ErrResponse{
 HTTPStatusCode: 400,
 Message: msg,
 }
 json.NewEncoder(w).Encode(e)
 return
 }
 a.Manager.AddTask(te)
 log.Printf("Added task %v\n", te.Task.ID)
 w.WriteHeader(201)
 json.NewEncoder(w).Encode(te.Task)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 8.1 / 8.2 The manager's Api struct and StartTaskHandler"*

```go
func (m *Manager) GetTasks() []*task.Task {
 tasks := []*task.Task{}
 for _, t := range m.TaskDb {
 tasks = append(tasks, t)
 }
 return tasks
}
```
```go
func (a *Api) GetTasksHandler(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.WriteHeader(200)
 json.NewEncoder(w).Encode(a.Manager.GetTasks())
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 8.3 / 8.4 GetTasks helper and handler"*

```go
func (a *Api) StopTaskHandler(w http.ResponseWriter, r *http.Request) {
 taskID := chi.URLParam(r, "taskID")
 if taskID == "" {
 log.Printf("No taskID passed in request.\n")
 w.WriteHeader(400)
 }
 tID, _ := uuid.Parse(taskID)
 taskToStop, ok := a.Manager.TaskDb[tID]
 if !ok {
 log.Printf("No task with ID %v found", tID)
 w.WriteHeader(404)
 }
 te := task.TaskEvent{
 ID: uuid.New(),
 State: task.Completed,
 Timestamp: time.Now(),
 }
 taskCopy := *taskToStop
 taskCopy.State = task.Completed
 te.Task = taskCopy
 a.Manager.AddTask(te)
 log.Printf("Added task event %v to stop task %v\n", te.ID, taskToStop.ID)
 w.WriteHeader(204)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 8.5 The manager's StopTaskHandler"*

---

### 53. Manager API Router and Start #go #api

**Code:**
```go
func (a *Api) initRouter() {
 a.Router = chi.NewRouter()
 a.Router.Route("/tasks", func(r chi.Router) {
 r.Post("/", a.StartTaskHandler)
 r.Get("/", a.GetTasksHandler)
 r.Route("/{taskID}", func(r chi.Router) {
 r.Delete("/", a.StopTaskHandler)
 })
 })
}
```
```go
func (a *Api) Start() {
 a.initRouter()
 http.ListenAndServe(fmt.Sprintf("%s:%d", a.Address, a.Port), a.Router)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 8.6 / 8.7 Manager API initRouter and Start"*

---

### 54. Refactor: Move Loops Into the Types #go #architecture

**Principle:** After the API exists, move background-loop functions out of `main.go` into exported methods on `Worker`/`Manager`. This encapsulates behavior and shrinks `main.go`.

**Code:**
```go
func (w *Worker) runTask() task.DockerResult {
}
func (w *Worker) RunTasks() {
 for {
 if w.Queue.Len() != 0 {
 result := w.runTask()
 if result.Error != nil {
 log.Printf("Error running task: %v\n", result.Error)
 }
 } else {
 log.Printf("No tasks to process currently.\n")
 }
 log.Println("Sleeping for 10 seconds.")
 time.Sleep(10 * time.Second)
 }
}
```
```go
func (m *Manager) UpdateTasks() {
 for {
 log.Println("Checking for task updates from workers")
 m.updateTasks()
 log.Println("Task updates completed")
 log.Println("Sleeping for 15 seconds")
 time.Sleep(15 * time.Second)
 }
}
```
```go
func (m *Manager) ProcessTasks() {
 for {
 log.Println("Processing any tasks in the queue")
 m.SendWork()
 log.Println("Sleeping for 10 seconds")
 time.Sleep(10 * time.Second)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 8.8 / 8.9 / 8.10"*

---

### 55. Failure Hierarchy — Application / Task / Orchestrator #architecture #systems

**Principle:** Failures occur at multiple levels and need different recovery strategies:
- **Application:** startup failure (e.g., DB unreachable), runtime bug
- **Task:** resource exhaustion, Docker daemon crash, machine crash
- **Worker:** component bug, machine down
- **Manager:** component bug, machine down

**Do:** Implement task-level health checks first; they cover the most common cases.
**Don't:** Don't rely on Docker restart policies — they muddy ownership of failure handling. The orchestrator should own it.

*Ref: Build_an_Orchestrator_in_Go.md — "9.2 Failure scenarios / 9.3 Recovery options"*

---

### 56. Docker `Inspect` — Authoritative Container State #go #cloud

**Code:**
```go
type DockerInspectResponse struct {
 Error error
 Container *types.ContainerJSON
}
```
```go
func (d *Docker) Inspect(containerID string) DockerInspectResponse {
 dc, _ := client.NewClientWithOpts(client.FromEnv)
 ctx := context.Background()
 resp, err := dc.ContainerInspect(ctx, containerID)
 if err != nil {
 log.Printf("Error inspecting container: %s\n", err)
 return DockerInspectResponse{Error: err}
 }
 return DockerInspectResponse{Container: &resp}
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.1 / 9.2 DockerInspectResponse and Inspect method"*

---

### 57. Worker `InspectTask` + `UpdateTasks` Reconciliation #go

**Code:**
```go
func (w *Worker) InspectTask(t task.Task) task.DockerInspectResponse {
 config := task.NewConfig(&t)
 d := task.NewDocker(config)
 return d.Inspect(t.ContainerID)
}
```
```go
func (w *Worker) UpdateTasks() {
 for {
 log.Println("Checking status of tasks")
 w.updateTasks()
 log.Println("Task updates completed")
 log.Println("Sleeping for 15 seconds")
 time.Sleep(15 * time.Second)
 }
}
```
```go
func (w *Worker) updateTasks() {
 for id, t := range w.Db {
 if t.State == task.Running {
 resp := w.InspectTask(*t)
 if resp.Error != nil {
 fmt.Printf("ERROR: %v\n", resp.Error)
 }
 if resp.Container == nil {
 log.Printf("No container for running task %s\n", id)
 w.Db[id].State = task.Failed
 }
 if resp.Container.State.Status == "exited" {
 log.Printf("Container for task %s in non-running state %s",
 ➥ id, resp.Container.State.Status)
 w.Db[id].State = task.Failed
 }
 w.Db[id].HostPorts =
 ➥ resp.Container.NetworkSettings.NetworkSettingsBase.Ports
 }
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.3 / 9.4 / 9.5 Worker InspectTask + UpdateTasks"*

---

### 58. Health Checks via Task-Defined URL #go #architecture

**Principle:** Add a `HealthCheck` field (URL path) to the Task so each task defines what "healthy" means. Add `RestartCount` to cap retries.

**Code:**
```go
type Task struct {
 // existing fields omitted
 HealthCheck string
 RestartCount int
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.6 Adding the HealthCheck and RestartCount fields"*

---

### 59. Manager `checkTaskHealth` — Build URL, GET, Inspect Status #go

**Code:**
```go
func (m *Manager) checkTaskHealth(t task.Task) error {
 log.Printf("Calling health check for task %s: %s\n",
 ➥ t.ID, t.HealthCheck)
 w := m.TaskWorkerMap[t.ID]
 hostPort := getHostPort(t.HostPorts)
 worker := strings.Split(w, ":")
 url := fmt.Sprintf("http://%s:%s%s",
 ➥ worker[0], *hostPort, t.HealthCheck)
 log.Printf("Calling health check for task %s: %s\n", t.ID, url)
 resp, err := http.Get(url)
 if err != nil {
 msg := fmt.Sprintf("Error connecting to health check %s", url)
 log.Println(msg)
 return errors.New(msg)
 }
 if resp.StatusCode != http.StatusOK {
 msg := fmt.Sprintf("Error health check for task %s did not
 ➥ return 200\n", t.ID)
 log.Println(msg)
 return errors.New(msg)
 }
 log.Printf("Task %s health check response: %v\n", t.ID, resp.StatusCode)
 return nil
}
```
```go
func getHostPort(ports nat.PortMap) *string {
 for k, _ := range ports {
 return &ports[k][0].HostPort
 }
 return nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.7 / 9.8 checkTaskHealth and getHostPort"*

---

### 60. `doHealthChecks` — Cap Restarts at 3 #go #architecture

**Code:**
```go
func (m *Manager) doHealthChecks() {
 for _, t := range m.GetTasks() {
 if t.State == task.Running && t.RestartCount < 3 {
 err := m.checkTaskHealth(*t)
 if err != nil {
 if t.RestartCount < 3 {
 m.restartTask(t)
 }
 }
 } else if t.State == task.Failed && t.RestartCount < 3 {
 m.restartTask(t)
 }
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.9 The manager's doHealthChecks method"*

**Do:** Set a restart ceiling to avoid infinite crash-loops; surface the count to operators.

---

### 61. `restartTask` — Reschedule On Same Worker (v1) #go

**Code:**
```go
func (m *Manager) restartTask(t *task.Task) {
 w := m.TaskWorkerMap[t.ID]
 t.State = task.Scheduled
 t.RestartCount++
 m.TaskDb[t.ID] = t
 te := task.TaskEvent{
 ID: uuid.New(),
 State: task.Running,
 Timestamp: time.Now(),
 Task: *t,
 }
 data, err := json.Marshal(te)
 if err != nil {
 log.Printf("Unable to marshal task object: %v.", t)
 return
 }
 url := fmt.Sprintf("http://%s/tasks", w)
 resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
 if err != nil {
 log.Printf("Error connecting to %v: %v", w, err)
 m.Pending.Enqueue(t)
 return
 }
 d := json.NewDecoder(resp.Body)
 if resp.StatusCode != http.StatusCreated {
 e := worker.ErrResponse{}
 err := d.Decode(&e)
 if err != nil {
 fmt.Printf("Error decoding response: %s\n", err.Error())
 return
 }
 log.Printf("Response error (%d): %s", e.HTTPStatusCode, e.Message)
 return
 }
 newTask := task.Task{}
 err = d.Decode(&newTask)
 if err != nil {
 fmt.Printf("Error decoding response: %s\n", err.Error())
 return
 }
 log.Printf("%#v\n", t)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.10 The manager's new restartTask method"*

```go
func (m *Manager) DoHealthChecks() {
 for {
 log.Println("Performing task health check")
 m.doHealthChecks()
 log.Println("Task health checks completed")
 log.Println("Sleeping for 60 seconds")
 time.Sleep(60 * time.Second)
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 9.11 The DoHealthChecks method"*

---

### 62. The Three-Phase Scheduler Interface #go #architecture

**Principle:** After v1, generalize scheduling into three methods, each with explicit types: `SelectCandidateNodes` (filter), `Score` (rank), `Pick` (choose).

**Code:**
```go
type Scheduler interface {
 SelectCandidateNodes(t task.Task, nodes []*node.Node) []*node.Node
 Score(t task.Task, nodes []*node.Node) map[string]float64
 Pick(scores map[string]float64, candidates []*node.Node) *node.Node
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.1 The updated Scheduler interface"*

---

### 63. Round-Robin Implementation of the Interface #go

**Code:**
```go
type RoundRobin struct {
 Name string
 LastWorker int
}
```
```go
func (r *RoundRobin) SelectCandidateNodes(t task.Task, nodes []*node.Node)
[]*node.Node {
 return nodes
}
```
```go
func (r *RoundRobin) Score(t task.Task, nodes []*node.Node)
➥ map[string]float64 {
 nodeScores := make(map[string]float64)
 var newWorker int
 if r.LastWorker+1 < len(nodes) {
 newWorker = r.LastWorker + 1
 r.LastWorker++
 } else {
 newWorker = 0
 r.LastWorker = 0
 }
 for idx, node := range nodes {
 if idx == newWorker {
 nodeScores[node.Name] = 0.1
 } else {
 nodeScores[node.Name] = 1.0
 }
 }
 return nodeScores
}
```
```go
func (r *RoundRobin) Pick(scores map[string]float64,
 ➥ candidates []*node.Node) *node.Node {
 var bestNode *node.Node
 var lowestScore float64
 for idx, node := range candidates {
 if idx == 0 {
 bestNode = node
 lowestScore = scores[node.Name]
 continue
 }
 if scores[node.Name] < lowestScore {
 bestNode = node
 lowestScore = scores[node.Name]
 }
 }
 return bestNode
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.2 / 10.3 / 10.4 / 10.5 The RoundRobin scheduler"*

**Do:** Use `0.1` for the chosen, `1.0` for everyone else so "lowest score wins" generalizes to E-PVM later.

---

### 64. Plumb the Scheduler Through Manager #go #architecture

**Code:**
```go
type Manager struct {
 // previous code not shown
 WorkerNodes []*node.Node
 Scheduler scheduler.Scheduler
}
```
```go
func New(workers []string, schedulerType string) *Manager {
 // previous code not shown
 var nodes []*node.Node
 for worker := range workers {
 workerTaskMap[workers[worker]] = []uuid.UUID{}
 nAPI := fmt.Sprintf("http://%v", workers[worker])
 n := node.NewNode(workers[worker], nAPI, "worker")
 nodes = append(nodes, n)
 }
 var s scheduler.Scheduler
 switch schedulerType {
 case "roundrobin":
 s = &scheduler.RoundRobin{Name: "roundrobin"}
 default:
 s = &scheduler.RoundRobin{Name: "roundrobin"}
 }
 return &Manager{
 Pending: *queue.New(),
 Workers: workers,
 TaskDb: taskDb,
 EventDb: eventDb,
 WorkerTaskMap: workerTaskMap,
 TaskWorkerMap: taskWorkerMap,
 WorkerNodes: nodes,
 Scheduler: s,
 }
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.6 / 10.7 / 10.8 Adding scheduler fields to the Manager"*

---

### 65. `SelectWorker` Becomes a Three-Call Pipeline #go

**Code:**
```go
func (m *Manager) SelectWorker(t task.Task) (*node.Node, error) {
 candidates := m.Scheduler.SelectCandidateNodes(t, m.WorkerNodes)
 if candidates == nil {
 msg := fmt.Sprintf("No available candidates match resource request
 ➥ for task %v", t.ID)
 err := errors.New(msg)
 return nil, err
 }
 scores := m.Scheduler.Score(t, candidates)
 selectedNode := m.Scheduler.Pick(scores, candidates)
 return selectedNode, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.9 The SelectWorker method using the Scheduler interface"*

---

### 66. The "Did You Notice the Bug?" — Stop-Task Routing #go #architecture

**Principle:** When scaling beyond one worker, naive `SendWork` may pick a different worker for a stop request than where the task actually runs. Always look up `TaskWorkerMap` first and short-circuit to `stopTask` for `Completed` events.

**Code (the fix):**
```go
// existing code
if m.Pending.Len() > 0 {
 e := m.Pending.Dequeue()
 te := e.(task.TaskEvent)
 m.EventDb[te.ID] = &te
 log.Printf("Pulled %v off pending queue\n", te)
 // new code
 taskWorker, ok := m.TaskWorkerMap[te.Task.ID]
 if ok {
 persistedTask := m.TaskDb[te.Task.ID]
 if te.State == task.Completed &&
 ➥ task.ValidStateTransition(persistedTask.State, te.State) {
 m.stopTask(taskWorker, te.Task.ID.String())
 return
 }
 log.Printf("invalid request: existing task %s is in state %v and
 ➥ cannot transition to the completed state\n",
 ➥ persistedTask.ID.String(), persistedTask.State)
 return
 }
```
```go
func (m *Manager) stopTask(worker string, taskID string) {
 client := &http.Client{}
 url := fmt.Sprintf("http://%s/tasks/%s", worker, taskID)
 req, err := http.NewRequest("DELETE", url, nil)
 if err != nil {
 log.Printf("error creating request to delete task %s: %v\n", taskID, err)
 return
 }
 resp, err := client.Do(req)
 if err != nil {
 log.Printf("error connecting to worker at %s: %v\n", url, err)
 return
 }
 if resp.StatusCode != 204 {
 log.Printf("Error sending request: %v\n", err)
 return
 }
 log.Printf("task %s has been scheduled to be stopped", taskID)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.13 / 10.14 stopTask and the stop-task fix"*

---

### 67. E-PVM Scheduler — Opportunity Cost Scoring #go #architecture

**Principle:** From the Borg-era "Opportunity Cost Approach for Job Assignment" paper: convert CPU + memory usage to a single homogeneous "cost" via the LIEB square-ice constant (`1.5396...`), then compute the *marginal* cost of adding the task to each node.

**Code:**
```go
const (
 // LIEB square ice constant
 // https://en.wikipedia.org/wiki/Lieb%27s_square_ice_constant
 LIEB = 1.53960071783900203869
)
func (e *Epvm) Score(t task.Task, nodes []*node.Node) map[string]float64 {
 nodeScores := make(map[string]float64)
 maxJobs := 4.0
 for _, node := range nodes {
 cpuUsage := calculateCpuUsage(node)
 cpuLoad := calculateLoad(cpuUsage, math.Pow(2, 0.8))
 memoryAllocated := float64(node.Stats.MemUsedKb()) +
 ➥ float64(node.MemoryAllocated)
 memoryPercentAllocated := memoryAllocated / float64(node.Memory)
 newMemPercent := (calculateLoad(memoryAllocated +
 ➥ float64(t.Memory/1000), float64(node.Memory)))
 memCost := math.Pow(LIEB, newMemPercent) + math.Pow(LIEB,
 ➥ (float64(node.TaskCount+1))/maxJobs) -
 ➥ math.Pow(LIEB, memoryPercentAllocated) -
 ➥ math.Pow(LIEB, float64(node.TaskCount)/float64(maxJobs))
 cpuCost := math.Pow(LIEB, cpuLoad) +
 ➥ math.Pow(LIEB, (float64(node.TaskCount+1))/maxJobs) -
 ➥ math.Pow(LIEB, cpuLoad) -
 ➥ math.Pow(LIEB, float64(node.TaskCount)/float64(maxJobs))
 nodeScores[node.Name] = memCost + cpuCost
 nodeScores[node.Name] = marginalCost
 }
 }
 return nodeScores
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.19 Signature of the E-PVM scheduler's Score"*

---

### 68. E-PVM Candidate Filtering by Disk #go

**Code:**
```go
func (e *Epvm) SelectCandidateNodes(t task.Task, nodes []*node.Node)
 ➥ []*node.Node {
 var candidates []*node.Node
 for node := range nodes {
 if checkDisk(t, nodes[node].Disk-nodes[node].DiskAllocated) {
 candidates = append(candidates, nodes[node])
 }
 }
 return candidates
}
func checkDisk(t task.Task, diskAvailable int64) bool {
 return t.Disk <= diskAvailable
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.18 The Epvm scheduler's SelectCandidateNodes method"*

---

### 69. Sampling CPU Usage Over a 3-Second Window #go #systems

**Code:**
```go
func calculateCpuUsage(node *node.Node) *float64 {
 stat1 := getNodeStats(node)
 time.Sleep(3 * time.Second)
 stat2 := getNodeStats(node)
 stat1Idle := stat1.CpuStats.Idle + stat1.CpuStats.IOWait
 stat2Idle := stat2.CpuStats.Idle + stat2.CpuStats.IOWait
 stat1NonIdle := stat1.CpuStats.User + stat1.CpuStats.Nice +
 ➥ stat1.CpuStats.System + stat1.CpuStats.IRQ +
 ➥ stat1.CpuStats.SoftIRQ + stat1.CpuStats.Steal
 stat2NonIdle := stat2.CpuStats.User + stat2.CpuStats.Nice +
 ➥ stat2.CpuStats.System + stat2.CpuStats.IRQ +
 ➥ stat2.CpuStats.SoftIRQ + stat2.CpuStats.Steal
 stat1Total := stat1Idle + stat1NonIdle
 stat2Total := stat2Idle + stat2NonIdle
 total := stat2Total - stat1Total
 idle := stat2Idle - stat1Idle
 var cpuPercentUsage float64
 if total == 0 && idle == 0 {
 cpuPercentUsage = 0.00
 } else {
 cpuPercentUsage = (float64(total) - float64(idle)) / float64(total)
 }
 return &cpuPercentUsage
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.20 The calculateCpuUsage helper function"*

---

### 70. `getNodeStats` — Pull `/stats` From the Worker API #go

**Code:**
```go
func getNodeStats(node *node.Node) *stats.Stats {
 url := fmt.Sprintf("%s/stats", node.Api)
 resp, err := http.Get(url)
 if err != nil {
 log.Printf("Error connecting to %v: %v", node.Api, err)
 }
 if resp.StatusCode != 200 {
 log.Printf("Error retrieving stats from %v: %v", node.Api, err)
 }
 defer resp.Body.Close()
 body, _ := ioutil.ReadAll(resp.Body)
 var stats stats.Stats
 json.Unmarshal(body, &stats)
 return &stats
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.21 The getNodeStats helper function"*

---

### 71. `HTTPWithRetry` — Transient-Fault Resilience #go #concurrency

**Principle:** Wrap HTTP calls in a retry loop with sleep; useful when worker nodes reboot or have transient network issues.

**Code:**
```go
package utils
import (
 "fmt"
 "net/http"
 "time"
)
func HTTPWithRetry(f func(string) (*http.Response, error), url string)
(*http.Response, error) {
 count := 10
 var resp *http.Response
 var err error
 for i := 0; i < count; i++ {
 resp, err = f(url)
 if err != nil {
 fmt.Printf("Error calling url %v\n", url)
 time.Sleep(5 * time.Second)
 } else {
 break
 }
 }
 return resp, err
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.24 The HTTPWithRetry helper function"*

---

### 72. Move `GetStats` Onto `Node` Itself #go #architecture

**Principle:** When a free function really operates on a single type, make it a method of that type. Reduces coupling and clarifies ownership.

**Code:**
```go
func (n *Node) GetStats() (*stats.Stats, error) {
 var resp *http.Response
 var err error
 url := fmt.Sprintf("%s/stats", n.Api)
 resp, err = utils.HTTPWithRetry(http.Get, url)
 if err != nil {
 msg := fmt.Sprintf("Unable to connect to %v. Permanent failure.\n",
 ➥ n.Api)
 log.Println(msg)
 return nil, errors.New(msg)
 }
 if resp.StatusCode != 200 {
 msg := fmt.Sprintf("Error retrieving stats from %v: %v", n.Api, err)
 log.Println(msg)
 return nil, errors.New(msg)
 }
 defer resp.Body.Close()
 body, _ := ioutil.ReadAll(resp.Body)
 var stats stats.Stats
 err = json.Unmarshal(body, &stats)
 if err != nil {
 msg := fmt.Sprintf("error decoding message while getting stats for
 ➥ node %s", n.Name)
 log.Println(msg)
 return nil, errors.New(msg)
 }
 n.Memory = int64(stats.MemTotalKb())
 n.Disk = int64(stats.DiskTotal())
 n.Stats = stats
 return &n.Stats, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.25 Renaming the getNodeStats helper function"*

---

### 73. Adding the `epvm` Case #go

**Code:**
```go
switch schedulerType {
case "roundrobin":
 s = &scheduler.RoundRobin{Name: "roundrobin"}
case "epvm"
 s = &scheduler.Epvm{Name: "epvm"}
default:
 s = &scheduler.RoundRobin{Name: "roundrobin"}
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 10.26 Adding a new epvm case to the switch statement"*

---

### 74. Storage Interface — Decouple Manager/Worker From the Engine #go #architecture

**Principle:** Just like `Scheduler`, define a `Store` interface with `Put`, `Get`, `List`, `Count`. Both manager and worker code call methods, never touching the underlying map directly.

**Code:**
```go
type Store interface {
 Put(key string, value interface{}) error
 Get(key string) (interface{}, error)
 List() (interface{}, error)
 Count() (int, error)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.2 The Store interface"*

**Do:** Skip `Remove` if your store is a historical record — you can always add it later.

---

### 75. `InMemoryTaskStore` — A Thin Wrapper Around `map` #go

**Code:**
```go
type InMemoryTaskStore struct {
 Db map[string]*task.Task
}
func NewInMemoryTaskStore() *InMemoryTaskStore {
 return &InMemoryTaskStore{
 Db: make(map[string]*task.Task),
 }
}
```
```go
func (i *InMemoryTaskStore) Put(key string, value interface{}) error {
 t, ok := value.(*task.Task)
 if !ok {
 return fmt.Errorf("value %v is not a task.Task type", value)
 }
 i.Db[key] = t
 return nil
}
```
```go
func (i *InMemoryTaskStore) Get(key string) (interface{}, error) {
 t, ok := i.Db[key]
 if !ok {
 return nil, fmt.Errorf("task with key %s does not exist", key)
 }
 return t, nil
}
```
```go
func (i *InMemoryTaskStore) List() (interface{}, error) {
 var tasks []*task.Task
 for _, t := range i.Db {
 tasks = append(tasks, t)
 }
 return tasks, nil
}
```
```go
func (i *InMemoryTaskStore) Count() (int, error) {
 return len(i.Db), nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.3 / 11.4 / 11.5 / 11.6 / 11.7 InMemoryTaskStore"*

**Do:** Use type assertions to convert `interface{}` to the concrete pointer type; return an error on mismatch.

---

### 76. `InMemoryTaskEventStore` — Same Pattern, Different Type #go

**Code:**
```go
type InMemoryTaskEventStore struct {
 Db map[string]*task.TaskEvent
}
func NewInMemoryTaskEventStore() *InMemoryTaskEventStore {
 return &InMemoryTaskEventStore{
 Db: make(map[string]*task.TaskEvent),
 }
}
func (i *InMemoryTaskEventStore) Put(key string, value interface{}) error {
 e, ok := value.(*task.TaskEvent)
 if !ok {
 return fmt.Errorf("value %v is not a task.TaskEvent type", value)
 }
 i.Db[key] = e
 return nil
}
func (i *InMemoryTaskEventStore) Get(key string) (interface{}, error) {
 e, ok := i.Db[key]
 if !ok {
 return nil, fmt.Errorf("task event with key %s does not exist", key)
 }
 return e, nil
}
func (i *InMemoryTaskEventStore) List() (interface{}, error) {
 var events []*task.TaskEvent
 for _, e := range i.Db {
 events = append(events, e)
 }
 return events, nil
}
func (i *InMemoryTaskEventStore) Count() (int, error) {
 return len(i.Db), nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.8 The InMemoryTaskEventStore"*

---

### 77. Refactor Manager to Use `Store` #go #architecture

**Code:**
```go
type Manager struct {
 // fields omitted for convenience
 TaskDb store.Store
 EventDb store.Store
 // fields omitted
```
```go
m := Manager{
 Pending: *queue.New(),
 Workers: workers,
 WorkerTaskMap: workerTaskMap,
 TaskWorkerMap: taskWorkerMap,
 WorkerNodes: nodes,
 Scheduler: s,
}
```
```go
var ts store.Store
var es store.Store
switch dbType {
case "memory":
 ts = store.NewInMemoryTaskStore()
 es = store.NewInMemoryTaskEventStore()
}
m.TaskDb = ts
m.EventDb = es
return &m
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.9 / 11.10 Refactoring Manager to use Store"*

---

### 78. Type-Assertion Pattern: From `interface{}` to Concrete #go

**Code:**
```go
for _, t := range tasks {
 // previous code omitted for convenience
 // existing code to be replaced
 // _, ok := m.TaskDb[t.ID]
 // if !ok {
 // log.Printf("[manager] Task with ID %s not found\n", t.ID)
 // continue
 // }
 result, err := m.TaskDb.Get(t.ID.String())
 if err != nil {
 log.Printf("[manager] %s\n", err)
 continue
 }
 taskPersisted, ok := result.(*task.Task)
 if !ok {
 log.Printf("cannot convert result %v to task.Task type\n", result)
 continue
 }
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.10 Using the new datastore interface to get a task from TaskDb"*

---

### 79. Replace Direct Map Mutation with `Put` #go

**Before:**
```go
if m.TaskDb[t.ID].State != t.State {
 m.TaskDb[t.ID].State = t.State
}
m.TaskDb[t.ID].StartTime = t.StartTime
m.TaskDb[t.ID].FinishTime = t.FinishTime
m.TaskDb[t.ID].ContainerID = t.ContainerID
m.TaskDb[t.ID].HostPorts = t.HostPorts
```
**After:**
```go
if taskPersisted.State != t.State {
 taskPersisted.State = t.State
}
taskPersisted.StartTime = t.StartTime
taskPersisted.FinishTime = t.FinishTime
taskPersisted.ContainerID = t.ContainerID
taskPersisted.HostPorts = t.HostPorts
m.TaskDb.Put(taskPersisted.ID.String(), taskPersisted)
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.11 / 11.12 Replacing direct map access with Put"*

---

### 80. `GetTasks` via `List` + Type Assertion #go

**Code:**
```go
func (m *Manager) GetTasks() []*task.Task {
 taskList, err := m.TaskDb.List()
 if err != nil {
 log.Printf("error getting list of tasks: %v\n", err)
 return nil
 }
 return taskList.([]*task.Task)
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.13 The GetTasks method"*

---

### 81. Worker Storage Refactor #go

**Code:**
```go
type Worker struct {
 // fields omitted
 Db store.Store
 // fields omitted
}
```
```go
func New(name string, taskDbType string) *Worker {
 w := Worker{
 Name: name,
 Queue: *queue.New(),
 }
 var s store.Store
 switch taskDbType {
 case "memory":
 s = store.NewInMemoryTaskStore()
 }
 w.Db = s
 return &w
}
```
```go
func (w *Worker) GetTasks() []*task.Task {
 taskList, err := w.Db.List()
 if err != nil {
 log.Printf("error getting list of tasks: %v\n", err)
 return nil
 }
 return taskList.([]*task.Task)
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.17 / 11.18 Worker New() and GetTasks"*

---

### 82. Worker `runTask` — Reorder Operations for Interface Errors #go

**Principle:** Because the Store's `Get` returns an error in many cases, the worker can't tell "doesn't exist" from "store failed". Solve by `Put` first, then `Get`.

**Code:**
```go
func (w *Worker) runTask() task.DockerResult {
 // previous code omitted
 err := w.Db.Put(taskQueued.ID.String(), &taskQueued)
 if err != nil {
 msg := fmt.Errorf("error storing task %s: %v",
 ➥ taskQueued.ID.String(), err)
 log.Println(msg)
 return task.DockerResult{Error: msg}
 }
 queuedTask, err := w.Db.Get(taskQueued.ID.String())
 if err != nil {
 msg := fmt.Errorf("error getting task %s from database: %v",
 ➥ taskQueued.ID.String(), err)
 log.Println(msg)
 return task.DockerResult{Error: msg}
 }
 taskPersisted := *queuedTask.(*task.Task)
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.19 The modified runTask method"*

---

### 83. Worker `StartTask`/`StopTask` Using `Put` #go

**Code:**
```go
func (w *Worker) StartTask(t task.Task) task.DockerResult {
 config := task.NewConfig(&t)
 d := task.NewDocker(config)
 result := d.Run()
 if result.Error != nil {
 log.Printf("Err running task %v: %v\n", t.ID, result.Error)
 t.State = task.Failed
 w.Db.Put(t.ID.String(), &t)
 return result
 }
 t.ContainerID = result.ContainerId
 t.State = task.Running
 w.Db.Put(t.ID.String(), &t)
```
```go
func (w *Worker) StopTask(t task.Task) task.DockerResult {
 config := task.NewConfig(&t)
 d := task.NewDocker(config)
 stopResult := d.Stop(t.ContainerID)
 if stopResult.Error != nil {
 log.Printf("%v\n", stopResult.Error)
 }
 removeResult := d.Remove(t.ContainerID)
 if removeResult.Error != nil {
 log.Printf("%v\n", removeResult.Error)
 }
 t.FinishTime = time.Now().UTC()
 t.State = task.Completed
 w.Db.Put(t.ID.String(), &t)
 log.Printf("Stopped and removed container %v for task %v\n",
 ➥ t.ContainerID, t.ID)
 return removeResult
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.20 StartTask / StopTask with Put"*

---

### 84. Embedded Key-Value Store: BoltDB #go #systems

**Principle:** Skip server-based DBs (Postgres, Mongo) for an orchestrator's local state. Use an *embedded* KV library (BoltDB) — pure Go, single file, no separate process.

**Do:**
- Use `bolt.Open(file, mode, nil)` to get a `*bolt.DB`.
- Store keys/values as byte slices (JSON-marshal structs).
- Use `View` for read-only transactions, `Update` for read-write.

*Ref: Build_an_Orchestrator_in_Go.md — "11.8 Introducing BoltDB"*

---

### 85. `TaskStore` Persistent Struct #go

**Code:**
```go
import (
 // previous imports omitted
 "github.com/boltdb/bolt"
)
type TaskStore struct {
 Db *bolt.DB
 DbFile string
 FileMode os.FileMode
 Bucket string
}
```
```go
func NewTaskStore(file string, mode os.FileMode, bucket string)
 ➥ (*TaskStore, error) {
 db, err := bolt.Open(file, mode, nil)
 if err != nil {
 return nil, fmt.Errorf("unable to open %v", file)
 }
 t := TaskStore{
 DbFile: file,
 FileMode: mode,
 Db: db,
 Bucket: bucket,
 }
 err = t.CreateBucket()
 if err != nil {
 log.Printf("bucket already exists, will use it instead
 ➥ of creating new one")
 }
 return &t, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.21 / 11.22 TaskStore and NewTaskStore"*

---

### 86. BoltDB `Count` via `View` + `ForEach` #go

**Code:**
```go
func (t *TaskStore) Count() (int, error) {
 taskCount := 0
 err := t.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte("tasks"))
 b.ForEach(func(k, v []byte) error {
 taskCount++
 return nil
 })
 return nil
 })
 if err != nil {
 return -1, err
 }
 return taskCount, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Persistent Count() method"*

---

### 87. `CreateBucket` — Idempotent Setup #go

**Code:**
```go
func (t *TaskStore) CreateBucket() error {
 return t.Db.Update(func(tx *bolt.Tx) error {
 _, err := tx.CreateBucket([]byte(t.Bucket))
 if err != nil {
 return fmt.Errorf("create bucket %s: %s", t.Bucket, err)
 }
 return nil
 })
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.23 The CreateBucket method"*

---

### 88. Persistent `Put` — Marshal → Bucket → Put #go

**Code:**
```go
func (t *TaskStore) Put(key string, value interface{}) error {
 return t.Db.Update(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(t.Bucket))
 buf, err := json.Marshal(value.(*task.Task))
 if err != nil {
 return err
 }
 err = b.Put([]byte(key), buf)
 if err != nil {
 return err
 }
 return nil
 })
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.24 The Put method for the persistent task store"*

---

### 89. Persistent `Get` — Byte-Slice → `json.Unmarshal` #go

**Code:**
```go
func (t *TaskStore) Get(key string) (interface{}, error) {
 var task task.Task
 err := t.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(t.Bucket))
 t := b.Get([]byte(key))
 if t == nil {
 return fmt.Errorf("task %v not found", key)
 }
 err := json.Unmarshal(t, &task)
 if err != nil {
 return err
 }
 return nil
 })
 if err != nil {
 return nil, err
 }
 return &task, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.25 The Get method for the persistent task store"*

**Note:** BoltDB's `Get` does *not* return an error for missing keys — it returns `nil`. You must check for `nil` and synthesize your own "not found" error.

---

### 90. Persistent `List` via `ForEach` #go

**Code:**
```go
func (t *TaskStore) List() (interface{}, error) {
 var tasks []*task.Task
 err := t.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(t.Bucket))
 b.ForEach(func(k, v []byte) error {
 var task task.Task
 err := json.Unmarshal(v, &task)
 if err != nil {
 return err
 }
 tasks = append(tasks, &task)
 return nil
 })
 return nil
 })
 if err != nil {
 return nil, err
 }
 return tasks, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Persistent List method"*

---

### 91. `EventStore` Persistent — Mirror of `TaskStore` #go

**Code:**
```go
type EventStore struct {
 DbFile string
 FileMode os.FileMode
 Db *bolt.DB
 Bucket string
}
```
```go
func NewEventStore(file string, mode os.FileMode, bucket string)
 ➥ (*EventStore, error) {
 db, err := bolt.Open(file, mode, nil)
 if err != nil {
 return nil, fmt.Errorf("unable to open %v", file)
 }
 e := EventStore{
 DbFile: file,
 FileMode: mode,
 Db: db,
 Bucket: bucket,
 }
 err = e.CreateBucket()
 if err != nil {
 log.Printf("bucket already exists, will use it instead
 ➥ of creating new one")
 }
 return &e, nil
}
```
```go
func (e *EventStore) Close() {
 e.Db.Close()
}
func (e *EventStore) CreateBucket() error {
 return e.Db.Update(func(tx *bolt.Tx) error {
 _, err := tx.CreateBucket([]byte(e.Bucket))
 if err != nil {
 return fmt.Errorf("create bucket %s: %s", e.Bucket, err)
 }
 return nil
 })
}
```
```go
func (e *EventStore) Count() (int, error) {
 eventCount := 0
 err := e.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(e.Bucket))
 b.ForEach(func(k, v []byte) error {
 eventCount++
 return nil
 })
 return nil
 })
 if err != nil {
 return -1, err
 }
 return eventCount, nil
}
```
```go
func (e *EventStore) Put(key string, value interface{}) error {
 return e.Db.Update(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(e.Bucket))
 buf, err := json.Marshal(value.(*task.TaskEvent))
 if err != nil {
 return err
 }
 err = b.Put([]byte(key), buf)
 if err != nil {
 log.Printf("unable to save item %s", key)
 return err
 }
 return nil
 })
}
func (e *EventStore) Get(key string) (interface{}, error) {
 var event task.TaskEvent
 err := e.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(e.Bucket))
 t := b.Get([]byte(key))
 if t == nil {
 return fmt.Errorf("event %v not found", key)
 }
 err := json.Unmarshal(t, &event)
 if err != nil {
 return err
 }
 return nil
 })
 if err != nil {
 return nil, err
 }
 return &event, nil
}
```
```go
func (e *EventStore) List() (interface{}, error) {
 var events []*task.TaskEvent
 err := e.Db.View(func(tx *bolt.Tx) error {
 b := tx.Bucket([]byte(e.Bucket))
 b.ForEach(func(k, v []byte) error {
 var event task.TaskEvent
 err := json.Unmarshal(v, &event)
 if err != nil {
 return err
 }
 events = append(events, &event)
 return nil
 })
 return nil
 })
 if err != nil {
 return nil, err
 }
 return events, nil
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "11.10 Implementing a persistent task event store"*

---

### 92. Switch to Persistent by Changing One String #go #architecture

**Code:**
```go
var err error
switch dbType {
case "memory":
 ts = store.NewInMemoryTaskStore()
 es = store.NewInMemoryTaskEventStore()
case "persistent":
 ts, err = store.NewTaskStore("tasks.db", 0600, "tasks")
 es, err = store.NewEventStore("events.db", 0600, "events")
}
```
```go
case "persistent":
 filename := fmt.Sprintf("%s_tasks.db", name)
 s, err = store.NewTaskStore(filename, 0600, "tasks")
```
```go
//w1 := worker.New("worker-1", "memory")
w1 := worker.New("worker-1", "persistent")
// w3 := worker.New("worker-3", "memory")
w3 := worker.New("worker-3", "persistent")
//m := manager.New(workers, "epvm", "memory")
m := manager.New(workers, "epvm", "persistent")
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 11.26 / 11.27 Switching to persistent stores"*

**Do:** Use `0600` file mode so only the owner can read/write the DB file.

---

### 93. Why Cobra for the CLI #go #cli

**Principle:** Use a CLI framework (Cobra) for subcommands, flags (long + shorthand), help text, and shell completion. Hand-rolling this is thousands of lines.

**Do:**
- Install `github.com/spf13/cobra` and the `cobra-cli` tool.
- Generate the skeleton with `cobra-cli init` and add commands with `cobra-cli add <name>`.
- Each command is a `*cobra.Command` with `Use`, `Short`, `Long`, `Run`, and an `init()` that wires flags.

*Ref: Build_an_Orchestrator_in_Go.md — "12.2 / 12.3 Introducing Cobra / Setting up"*

---

### 94. Cobra Layout: `main.go` + `cmd/` Package #go #cli

**Code:**
```go
/*
Copyright © 2023 NAME HERE <EMAIL ADDRESS>
*/
package main
import "cube/cmd"
func main() {
 cmd.Execute()
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.1 The new main.go generated by cobra-cli"*

---

### 95. Cobra `rootCmd` Anatomy #go #cli

**Principle:** The root command holds the app name and global help. `Execute()` is called from `main`. Persistent flags propagate; local flags don't.

**Code:**
```go
// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
 Use: "cube",
 Short: "A brief description of your application",
 Long: `A longer description that spans multiple lines and likely
 ➥ contains
examples and usage of using your application. For example:
Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
 // Uncomment the following line if your bare application
 // has an action associated with it:
 // Run: func(cmd *cobra.Command, args []string) { },
}
```
```go
// Execute adds all child commands to the root command and sets flags
➥ appropriately.
// This is called by main.main(). It only needs to happen once to the
➥ rootCmd.
func Execute() {
 err := rootCmd.Execute()
 if err != nil {
 os.Exit(1)
 }
}
```
```go
func init() {
 // Here you will define your flags and configuration settings.
 // Cobra supports persistent flags, which, if defined here,
 // will be global for your application.
 // rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "",
 // ➥ "config file (default is $HOME/.cube.yaml)")
 // Cobra also supports local flags, which will only run
 // when this action is called directly.
 rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "12.5 Understanding root.go"*

---

### 96. Worker Command — Flags via `StringP`/`IntP` #go #cli

**Code:**
```go
package cmd
import (
 "cube/worker"
 "fmt"
 "log"
 "github.com/google/uuid"
 "github.com/spf13/cobra"
)
func init() {
 rootCmd.AddCommand(workerCmd)
 workerCmd.Flags().StringP("host", "H", "0.0.0.0",
 ➥ "Hostname or IP address")
 workerCmd.Flags().IntP("port", "p", 5556, "Port on
 ➥ which to listen")
```
```go
 workerCmd.Flags().StringP("name", "n", fmt.Sprintf("worker-%s",
 ➥ uuid.New().String()), "Name of the worker")
 workerCmd.Flags().StringP("dbtype", "d", "memory", "Type of datastore
 ➥ to use for tasks (\"memory\" or \"persistent\")")
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.4 / 12.5 Worker command flags"*

**Do:** Always provide a sensible default so the command runs with no flags.

---

### 97. Worker Command `Run` — Read Flags, Start Components #go #cli #concurrency

**Code:**
```go
Run: func(cmd *cobra.Command, args []string) {
 host, _ := cmd.Flags().GetString("host")
 port, _ := cmd.Flags().GetInt("port")
 name, _ := cmd.Flags().GetString("name")
 dbType, _ := cmd.Flags().GetString("dbtype")
```
```go
 log.Println("Starting worker.")
 w := worker.New(name, dbType)
 api := worker.Api{Address: host, Port: port, Worker: w}
 go w.RunTasks()
 go w.CollectStats()
 go w.UpdateTasks()
 log.Printf("Starting worker API on http://%s:%d", host, port)
 api.Start()
},
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.7 / 12.8 Worker Run"*

---

### 98. Manager Command — `StringSliceP` for Worker List #go #cli

**Code:**
```go
package cmd
import (
 "cube/manager"
 "log"
 "github.com/spf13/cobra"
)
func init() {
 rootCmd.AddCommand(managerCmd)
 managerCmd.Flags().StringP("host", "H", "0.0.0.0",
 ➥ "Hostname or IP address")
 managerCmd.Flags().IntP("port", "p", 5555, "Port on which to listen")
 managerCmd.Flags().StringSliceP("workers", "w",
 ➥ []string{"localhost:5556"}, "List of workers on which the manager
 ➥ will schedule tasks.")
 managerCmd.Flags().StringP("scheduler", "s", "epvm", "Name
 ➥ of scheduler to use.")
 managerCmd.Flags().StringP("dbType", "d", "memory", "Type of datastore
 ➥ to use for events and tasks (\"memory\" or \"persistent\")")
}
```
```go
Run: func(cmd *cobra.Command, args []string) {
 host, _ := cmd.Flags().GetString("host")
 port, _ := cmd.Flags().GetInt("port")
 workers, _ := cmd.Flags().GetStringSlice("workers")
 scheduler, _ := cmd.Flags().GetString("scheduler")
 dbType, _ := cmd.Flags().GetString("dbType")
```
```go
 log.Println("Starting manager.")
 m := manager.New(workers, scheduler, dbType)
 api := manager.Api{Address: host, Port: port, Manager: m}
 go m.ProcessTasks()
 go m.UpdateTasks()
 go m.DoHealthChecks()
 go m.UpdateNodeStats()
 log.Printf("Starting manager API on http://%s:%d", host, port)
 api.Start()
 },
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.9 / 12.10 / 12.11 Manager command"*

**Do:** Use `StringSliceP` to accept comma-separated values: `-w 'localhost:5556,localhost:5557'`.

---

### 99. `run` Command — Validate File, POST to Manager #go #cli

**Code:**
```go
func fileExists(filename string) bool {
 _, err := os.Stat(filename)
 return !errors.Is(err, fs.ErrNotExist)
}
```
```go
Run: func(cmd *cobra.Command, args []string) {
 manager, _ := cmd.Flags().GetString("manager")
 filename, _ := cmd.Flags().GetString("filename")
 fullFilePath, err := filepath.Abs(filename)
 if err != nil {
 log.Fatal(err)
 }
 if !fileExists(fullFilePath) {
 log.Fatalf("File %s does not exist.", filename)
 }
 log.Printf("Using manager: %v\n", manager)
 log.Printf("Using file: %v\n", fullFilePath)
 data, err := os.ReadFile(filename)
 if err != nil {
 log.Fatalf("Unable to read file: %v", filename)
 }
 log.Printf("Data: %v\n", string(data))
 url := fmt.Sprintf("http://%s/tasks", manager)
 resp, err := http.Post(url, "application/json",
 ➥ bytes.NewBuffer(data))
 if err != nil {
 log.Panic(err)
 }
 if resp.StatusCode != http.StatusCreated {
 log.Printf("Error sending request: %v", resp.StatusCode)
 }
 defer resp.Body.Close()
 log.Println("Successfully sent task request to manager")
 },
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.13 / 12.16 / 12.17 run command"*

---

### 100. `stop` Command — `cobra.MinimumNArgs(1)` + `http.NewRequest("DELETE", ...)` #go #cli

**Code:**
```go
Args: cobra.MinimumNArgs(1),
 Run: func(cmd *cobra.Command, args []string) {
 manager, _ := cmd.Flags().GetString("manager")
 url := fmt.Sprintf("http://%s/tasks/%s", manager, args[0])
 client := &http.Client{}
 req, err := http.NewRequest("DELETE", url, nil)
 if err != nil {
 log.Printf("Error creating request %v: %v", url, err)
 }
 resp, err := client.Do(req)
 if err != nil {
 log.Printf("Error connecting to %v: %v", url, err)
 }
 if resp.StatusCode != http.StatusNoContent {
 log.Printf("Error sending request: %v", err)
 return
 }
 log.Printf("Task %v has been stopped.", args[0])
 },
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.19 The Stop command using arguments"*

**Note:** `http.Client` only has `Get` and `Post` helpers — for `DELETE` you must build a `Request` and call `client.Do(req)`.

---

### 101. `status` Command — `tabwriter` for `docker ps`-Style Output #go #cli

**Code:**
```go
Run: func(cmd *cobra.Command, args []string) {
 manager, _ := cmd.Flags().GetString("manager")
 url := fmt.Sprintf("http://%s/tasks", manager)
 resp, _ := http.Get(url)
 body, err := io.ReadAll(resp.Body)
 if err != nil {
 log.Fatal(err)
 }
 defer resp.Body.Close()
 var tasks []*task.Task
 err = json.Unmarshal(body, &tasks)
 if err != nil {
 log.Fatal(err)
 }
 w := tabwriter.NewWriter(os.Stdout, 0, 0, 5, ' ', tabwriter.TabIndent)
 fmt.Fprintln(w, "ID\tNAME\tCREATED\tSTATE\tCONTAINERNAME\tIMAGE\t")
 for _, task := range tasks {
 var start string
 if task.StartTime.IsZero() {
 start = fmt.Sprintf("%s ago",
 ➥ units.HumanDuration(time.Now().UTC().Sub(time.Now().UTC())))
 } else {
 start = fmt.Sprintf("%s ago",
 ➥ units.HumanDuration(time.Now().UTC().Sub(task.StartTime)))
 }
 state := task.State.String()[task.State]
 fmt.Fprintf(w, "%s\t%s\t%s\t%s\t%s\t%s\t\n", task.ID, task.Name,
 ➥ start, state, task.Name, task.Image)
 }
 w.Flush()
 },
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.21 The Run function (status)"*

---

### 102. `node` Command — Cluster Overview #go #cli

**Code:**
```go
Run: func(cmd *cobra.Command, args []string) {
 manager, _ := cmd.Flags().GetString("manager")
 url := fmt.Sprintf("http://%s/nodes", manager)
 resp, _ := http.Get(url)
 defer resp.Body.Close()
 body, _ := io.ReadAll(resp.Body)
 var nodes []*node.Node
 json.Unmarshal(body, &nodes)
 w := tabwriter.NewWriter(os.Stdout, 0, 0, 5, ' ',
 ➥ tabwriter.TabIndent)
 fmt.Fprintln(w, "NAME\tMEMORY (MiB)\tDISK (GiB)\tROLE\tTASKS\t")
 for _, node := range nodes {
 fmt.Fprintf(w, "%s\t%d\t%d\t%s\t%d\t\n", node.Name,
 ➥ node.Memory/1000,
 ➥ node.Disk/1000/1000/1000, node.Role, node.TaskCount)
 }
 w.Flush()
 },
}
```
*Ref: Build_an_Orchestrator_in_Go.md — "Listing 12.24 The node command"*

---

## Anti-Patterns & Common Mistakes

- **Tight coupling to `map`:** Directly indexing `m.TaskDb[t.ID]` everywhere means you can never swap implementations. → *Fix:* Introduce a `Store` interface and call methods only.
- **Naive round-robin across heterogeneous workers:** Selecting workers in rotation ignores disk/CPU/memory needs. → *Fix:* Add `SelectCandidateNodes` filter (e.g., disk-space check) before scoring.
- **Mutating shared task pointer in `StopTaskHandler`:** Setting `taskToStop.State = Completed` directly modifies the Db entry; the queue and Db now agree, so the worker rejects the transition. → *Fix:* Copy first (`taskCopy := *taskToStop`), mutate the copy, enqueue the copy.
- **Trusting `io.Copy` from `ImagePull` to be silent:** It writes user-facing progress to stdout. → *Fix:* Decide whether you want this in production logs.
- **Fire-and-forget task management:** The manager must poll workers; otherwise its view drifts. → *Fix:* Run `UpdateTasks` in a goroutine on a timer.
- **Relying on Docker restart policies:** Blurs ownership of failure handling between Docker and the orchestrator. → *Fix:* Set Docker restart policy to default and let the orchestrator restart failed tasks.
- **Stop-task bug after scaling to N workers:** Without checking `TaskWorkerMap`, a stop request may land on a different worker. → *Fix:* Look up existing task, validate transition, then call `stopTask(worker, id)`.
- **Returning a single `nil` from `http.Get(url)` calls without retry:** Transient worker reboot = lost stats. → *Fix:* Wrap calls in `HTTPWithRetry`.
- **BoltDB `Get` returns `nil`, not error, for missing key:** Easy to mis-handle. → *Fix:* Explicitly check for `nil` byte slice and synthesize your own "not found" error.
- **Infinite restart loops:** Without a cap, a permanently-broken task thrashes the cluster. → *Fix:* `RestartCount < 3` guard.
- **Crossing the Store boundary without type assertion:** Forgetting `result.(*task.Task)` panics at the next field access. → *Fix:* Always assert with `ok` guard.
- **Long-lived work in the same goroutine as the HTTP server:** The server never accepts requests. → *Fix:* Spawn `go runTasks()`, `go CollectStats()`, etc., before calling `api.Start()`.
- **Hard-coded HTTP method helpers:** `http.Client` has only `Get` and `Post`. Using `http.Get` for DELETE silently uses GET. → *Fix:* Build a `*http.Request` with the right method and call `client.Do(req)`.

## Decision Heuristics / Checklists

**When to use channels vs. goroutines + sleep loops:**
- The book deliberately uses only goroutines + `time.Sleep` for periodic work — no channels. Choose the same when the work is naturally periodic (polling, health checks). Reach for channels only when you need cross-goroutine signaling.

**Scheduler choice:**
- One worker, no resource pressure → `roundrobin` (cheap, simple).
- Multiple workers, mixed load, want to spread → `epvm` (marginal-cost-based).
- Need fairness + simplicity → round-robin.
- Need bin-packing (cost optimization) → write a new `Scheduler` implementation that scores emptier nodes lower.

**Storage choice:**
- Dev / single-process → `memory` (fast, no files).
- Production / restart-safe → `persistent` (BoltDB).
- Need ad-hoc queries / SQL → write a new `Store` implementation (e.g., SQLite).

**API design:**
- Use `201 Created` for POST that creates a resource, `200 OK` for GET, `204 No Content` for DELETE.
- Use `DisallowUnknownFields()` on JSON decoders to catch client bugs.
- Use chi (or equivalent) when you need parameterized routes (`/tasks/{taskID}`).

**Health-check design:**
- Convention: task defines its own health URL via `HealthCheck` field; manager calls it.
- Cap restart attempts (e.g., 3) before declaring the task terminally failed.
- Treat both connection errors and non-200 responses as failures.

**Refactoring triggers (interface extraction):**
- You have multiple algorithms for the same problem → extract an interface (Scheduler).
- You have multiple storage backends → extract an interface (Store).
- A function really operates on one type → make it a method (getNodeStats → Node.GetStats).
- A free function in `main.go` only operates on one type → move it into the type (`runTasks` → `Worker.RunTasks`).

**CLI design:**
- Pattern: `APPNAME COMMAND ARG --FLAG`.
- Always provide `-h/--help` with concise `Short` and detailed `Long`.
- Provide sensible defaults for every flag so the command works with zero args.
- Use Cobra's `Args: cobra.MinimumNArgs(1)` for commands that need positional input.

**Failure-handling ownership:**
- Manager owns failure *policy* (when to restart, when to give up, where to reschedule).
- Worker owns failure *detection* (Docker `ContainerInspect`).
- Docker owns nothing — leave its restart policy default.

## Key Takeaways

1. **Five components cover every orchestrator:** manager, worker, scheduler, task, storage. Map your domain onto these before coding.
2. **Skeleton first:** Write stub structs and `fmt.Println` methods, then a smoke-test `main.go`. If it compiles, the architecture is coherent.
3. **Tasks are state machines:** Encode states as `iota`, encode transitions in a `map[State][]State`, validate every transition through one helper.
4. **Desired state vs. current state:** Queue = desired; Db = current; worker/manager loops reconcile them. This is the universal orchestrator pattern (cf. Kubernetes controllers).
5. **Wrap side effects in result types:** `DockerResult`, `DockerInspectResponse` — uniform return shapes simplify error handling up the stack.
6. **Separation of concerns in the API:** Handlers don't call Docker; they only enqueue. The worker's background loop calls Docker. This keeps handlers fast and testable.
7. **Use the Docker Go SDK:** Don't shell out, don't hand-craft HTTP; the SDK is the same code path as the `docker` CLI.
8. **Use Linux `/proc` for metrics:** Wrap with `goprocinfo` to get CPU, memory, disk, load — no shelling out to `top`/`free`.
9. **Manager is the control plane:** It owns scheduling, state, and recovery. Worker is the data plane: it owns execution. They communicate via HTTP API only.
10. **Interfaces enable swapping:** Both `Scheduler` and `Store` are interfaces; concrete implementations are selected by a single string (`"roundrobin"` / `"epvm"`, `"memory"` / `"persistent"`).
11. **Health checks + bounded restarts:** Define health per-task via a URL field; cap restarts at a small number (3) to avoid crash-loops.
12. **Embedded KV (BoltDB) for orchestrator state:** No DB server to operate; transactions are explicit (`View` for reads, `Update` for writes); data persists across restarts.
13. **Use a CLI framework (Cobra):** Don't roll your own flag parser. Generate skeletons with `cobra-cli` and customize `Use`, `Short`, `Long`, `Run`, and `init()`.
14. **Poll workers as source of truth:** The manager periodically calls `GET /tasks` on each worker and overwrites its own state — workers always reflect ground truth.
15. **Concurrency via goroutines + sleep:** For periodic reconciliation, this is simpler than channels and cron — and good enough for an orchestrator at this scale.
16. **Refactor ruthlessly:** The book evolves from in-memory maps to a Store interface, from a single worker to three, from a naive scheduler to a pluggable interface — each refactor is small and behavior-preserving.
17. **3,000 lines is enough:** Borg has millions; you can build a *working* orchestrator in a weekend's worth of code. The architecture is what matters.
18. **The manager-worker pattern transfers:** Workflow systems, integration services, anything with a control loop and a pool of executors — same shape.

## Cross-References
- Related: [[../INDEX.md]]
- Topic index: `#architecture`, `#go`, `#systems`, `#concurrency`, `#cloud`
- Companion disciplines: distributed systems (Kleppmann, *Designing Data-Intensive Applications*), consensus (Raft, Paxos), service discovery (Consul), load balancing, security — all explicitly out of scope for Cube but listed as next steps in chapter 13.
