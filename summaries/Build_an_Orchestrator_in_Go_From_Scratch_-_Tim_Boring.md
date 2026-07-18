# Build an Orchestrator in Go (From Scratch) - Tim Boring

## Comprehensive Summary

---

## Part 1: Introduction

### Chapter 1: What Is an Orchestrator?

**The orchestration landscape:** Modern applications run as containers, and orchestrators manage container lifecycles at scale. The core components of any orchestration system:

- **Manager** (BorgMaster / Control Plane / Server): Coordinates the cluster, receives requests, assigns tasks
- **Worker** (Borglet / Kubelet / Client/Agent): Executes tasks on individual machines
- **Scheduler**: Decides which worker runs which task based on constraints and resources
- **Task**: The unit of work (typically a container)
- **Storage**: Persists task state, job definitions, cluster configuration

**Container vs VM:** Containers share the host OS kernel (lightweight), VMs include full guest OS (heavy). Containers start in milliseconds; VMs take minutes. This fundamental difference enables orchestration at scale.

**The book's project: Cube**, a simple orchestrator built in Go that demonstrates the principles behind Kubernetes, Nomad, and Mesos.

### Chapter 2: From Mental Model to Skeleton Code

**Task skeleton:** Defines the work to be done:
- Container image, command, arguments
- Required resources (CPU, memory)
- State (pending, scheduled, running, completed, failed)
- Unique ID for tracking

**Worker skeleton:** Runs on each machine:
- Accepts tasks from manager
- Starts/stops containers via Docker API
- Reports status back to manager

**Manager skeleton:** Central coordinator:
- Maintains cluster state
- Receives task submissions
- Delegates scheduling decisions
- Communicates with workers

**Scheduler skeleton:** Assignment algorithm:
- Takes pending tasks and available workers
- Matches tasks to workers based on resource requirements
- Supports different scheduling strategies (round-robin, bin-packing, resource-based)

### Chapter 3: Task Implementation with Docker

**Docker fundamentals for orchestration:**
- Starting containers programmatically via Docker Engine API
- Managing container lifecycle (create, start, stop, remove)
- Inspecting container state and logs
- Handling container failures and restarts

**Task configuration:**
```go
type Task struct {
    ID            string
    ContainerID   string
    Name          string
    State         State
    Image         string
    CPU           float64
    Memory        int64
    Disk          int64
    Port          int
    RestartCount  int
}
```

**State machine for tasks:** Pending → Scheduled → Running → Completed/Failed

---

## Part 2: Worker

### Chapter 4: The Cube Worker

The worker is the workhorse of the orchestrator. It:

1. **Receives tasks** from the manager (or from a queue)
2. **Starts containers** using Docker API
3. **Monitors running tasks** for health and resource usage
4. **Reports status** back to the manager
5. **Stops tasks** when instructed

**Task lifecycle management:**
```go
func (w *Worker) StartTask(t task.Task) error
func (w *Worker) StopTask(t task.Task) error
func (w *Worker) RunTask(t task.Task) error  // Start if not running, stop if completed
```

**Task counting and state tracking:** Workers maintain a count of running tasks and their states. The manager queries workers to make scheduling decisions.

**Failure handling:** Should the manager or worker handle failures? The book argues the manager should own failure policy, while the worker executes it. This separation of concerns keeps the worker simple and the manager in control.

### Chapter 5: Worker API

**REST API for the worker:**
- `POST /tasks` - Start a new task
- `DELETE /tasks/{id}` - Stop a task
- `GET /tasks` - List all tasks
- `GET /tasks/{id}` - Get task details

**API design principles:**
- Use standard HTTP methods and status codes
- JSON request/response format
- Clean separation between API handler and worker logic

### Chapter 6: Metrics

**Collecting system metrics from /proc filesystem:**
- CPU usage (per core and aggregate)
- Memory usage (total, used, available)
- Disk usage
- Network I/O
- Per-container resource usage via Docker stats

**Exposing metrics via the API:**
- `GET /metrics` endpoint returns current system and task metrics
- Metrics inform scheduling decisions (don't schedule on overloaded workers)
- Future integration with Prometheus for time-series monitoring

---

## Part 3: Manager

### Chapter 7: The Cube Manager

The manager is the brain of the orchestrator:

1. **Accepts task submissions** from users (via CLI or API)
2. **Stores task definitions** in persistent storage
3. **Triggers scheduling** for pending tasks
4. **Dispatches tasks** to appropriate workers
5. **Monitors task health** across the cluster
6. **Handles failures** by rescheduling or reporting

**Manager architecture:**
```
User → Manager API → Task Store → Scheduler → Worker API → Worker → Docker
                                       ↑
                                  State Store
```

### Chapter 8: Manager API

**REST API for the manager:**
- `POST /tasks` - Submit a new task
- `GET /tasks` - List all tasks (cluster-wide)
- `GET /tasks/{id}` - Get task details
- `DELETE /tasks/{id}` - Stop and remove a task
- `GET /workers` - List all workers
- `GET /workers/{name}` - Get worker details and its tasks

### Chapter 9: Scheduler

**Scheduling strategies:**

1. **Round-robin**: Assign tasks to workers in rotation. Simple but ignores resource constraints.

2. **Greedy / Best-fit**: Assign each task to the worker with the most available resources that can satisfy the task's requirements.

3. **Bin-packing**: Pack tasks tightly onto the fewest workers (cost optimization). Leaves some workers empty for scaling.

**Scheduler implementation:**
```go
type Scheduler interface {
    SelectCandidate(t task.Task, workers []worker.Worker) (worker.Worker, error)
    Schedule(t task.Task, w worker.Worker) error
}
```

**Scheduling decisions consider:**
- Available CPU, memory, disk on each worker
- Task resource requirements
- Affinity/anti-affinity rules (not covered in detail)
- Worker health status

### Chapter 10: Persistent Storage

**Why persist state:** Without persistence, the manager loses all task definitions and state on restart. Production orchestrators must recover from failures.

**Storage implementation using SQLite** (for simplicity):
- Task definitions and current state
- Worker registrations
- Event history for debugging

**Alternative storage backends:** etcd (Kubernetes), Consul (Nomad), ZooKeeper (Mesos).

---

## Part 4: Complete System

### Chapter 11: Task Dependencies

**Job concept:** A job is a group of related tasks. Jobs can define dependencies:
- Task B starts only after Task A completes successfully
- Supports DAG (Directed Acyclic Graph) workflows

### Chapter 12: CLI with Cobra

**Command-line interface** using the Cobra library:
- `cube manager start` - Start the manager
- `cube worker start` - Start a worker
- `cube task submit` - Submit a new task
- `cube task list` - List tasks
- `cube task stop` - Stop a task

Cobra provides: subcommands, flags, help generation, shell completions.

### Chapter 13: Putting It All Together

**Running Cube:**
1. Start the manager process
2. Start one or more worker processes (registering with manager)
3. Submit tasks via CLI
4. Manager schedules tasks to workers
5. Workers execute tasks via Docker
6. Monitor via manager API

**Docker restart policies vs orchestrator-managed restarts:** The book argues against using Docker's built-in restart policies in orchestrated environments. The orchestrator should own failure handling to avoid confusion about who is responsible.

---

## Key Takeaways

1. **Orchestrators have five core components**: Manager, Worker, Scheduler, Task, Storage. Understanding these gives you insight into how Kubernetes, Nomad, and Mesos work.

2. **Separation of concerns**: The manager decides *what* to run and *where*, the worker decides *how* to run it, the scheduler optimizes placement.

3. **State machines manage task lifecycle**: Clear state transitions (Pending → Scheduled → Running → Completed/Failed) prevent inconsistent states.

4. **The scheduler is the brain**: Scheduling algorithms (round-robin, greedy, bin-packing) have direct impact on cluster efficiency and cost.

5. **Persistent state is essential**: Any production orchestrator must survive manager restarts. Store task definitions and state externally.

6. **Docker API integration**: The Docker Engine API allows programmatic container management—every orchestrator needs this capability.

7. **Build from scratch to understand**: Understanding how orchestrators work from first principles makes you a better Kubernetes/Nomad operator and troubleshooter.

8. **Go is well-suited for systems programming**: Concurrency (goroutines), standard library (HTTP, JSON), and single binary deployment make Go ideal for orchestration tools.

9. **Metrics inform decisions**: Resource metrics from workers feed scheduling decisions and enable cluster monitoring.

10. **The manager owns failure policy**: Keeping failure handling centralized in the manager, rather than distributed to workers or Docker, provides clear ownership and simpler debugging.
