# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Grokking Concurrency
**Author:** Kirill Bobrov
**Topic tags:** `#concurrency` `#parallelism` `#architecture` `#performance` `#distributed-systems` `#async`
**Language focus:** Language-agnostic (Python 3.9 examples) — concepts transfer to Go and any runtime
**Sources:** `markdown_output/Grokking_Concurrency_-_Kirill_Bobrov/Grokking_Concurrency_-_Kirill_Bobrov.md`

## TL;DR
A concept-first tour of concurrency from hardware up to distributed systems. Establishes the vocabulary (processes/threads, IPC, multitasking, decomposition), the governing laws (Amdahl, Gustafson, Little-style throughput), the failure modes (race conditions, deadlocks, livelocks, starvation), and the canonical patterns (pipeline, map, fork/join, map/reduce, producer-consumer, readers-writer, thread pool, reactor/event-loop). Closes with the C10k problem and why nonblocking/event-driven I/O displaced thread-per-connection servers. Use it as the theoretical foundation that complements Go-specific idioms in [[../Concurrency_in_Go.md]].

---

## Best Practices by Topic

### Concurrency vs. Parallelism

**Principle:** *"Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once."* — Rob Pike. Concurrency is a property of how a program is structured; parallelism is a property of the runtime environment.

**Do:**
- Design for concurrency first; parallelism follows if hardware allows.
- Recognize that an app can be concurrent-but-not-parallel (juggling tasks on one core), parallel-but-not-concurrent (SIMD on a single task), both, or neither.
- Use concurrency to express structure (multiple independent tasks); use parallelism to express execution (multiple CPUs doing work).

**Don't:**
- Use the words interchangeably; the distinction drives design decisions.
- Assume a concurrent program is faster — concurrency is about structure, not speed.

*Ref: Grokking_Concurrency.md — "Concurrency vs. parallelism" (Ch. 2)*

---

### Performance: Latency vs. Throughput

**Principle:** Concurrency improves systems in exactly three ways: (1) **reduce** latency (faster per-task), (2) **hide** latency (do other work while waiting — key for responsive systems), (3) **increase** throughput (more tasks per unit time). Optimizing one may worsen another.

**Do:**
- Pick the metric your system actually cares about (a GUI cares about latency; a batch pipeline cares about throughput).
- Use concurrency to hide I/O latency — the CPU should never idle while a task waits on disk/network.
- Measure **percentiles** (P95, P99) for latency — averages hide long tails.

**Don't:**
- Assume higher throughput implies lower latency — a bus has 25× the throughput of a motorcycle but a longer per-trip latency.
- Optimize both blindly; explicit trade-offs.
- Treat latency and throughput as independent — they interact.

*Ref: Grokking_Concurrency.md — "Latency vs. throughput" (Ch. 1)*

---

### Amdahl's Law & Gustafson's Law

**Principle:** Speedup is bounded by the **sequential fraction** of a program: `Speedup = 1 / (S + (1−S)/N)`. If 33% of a program is sequential, even a million processors yield at most 3× speedup. Gustafson's counter: if you scale the *problem size* with the processor count, sequential parts matter less and speedup can grow linearly.

**Do:**
- Use Amdahl to estimate whether parallelizing is worth the engineering cost.
- Use Gustafson's framing (grow the workload) when designing distributed/batch systems.
- Identify and minimize the sequential fraction of your program.

**Don't:**
- Throw cores at a mostly-sequential program and expect linear gains.
- Forget coordination overhead — Amdahl assumes none.
- Ignore Amdahl when "just adding cores" doesn't help.

*Ref: Grokking_Concurrency.md — "Amdahl's law", "Gustafson's law" (Ch. 2)*

---

### Hardware Awareness — Cache, SMP, Flynn's Taxonomy

**Principle:** Effective concurrency requires understanding the hardware. Scaled latency grows alarmingly: L1 ≈ 1 s, RAM ≈ 4 min, SSD ≈ 1.5 days, network round-trip SF→NYC ≈ 5 years (when 1 CPU cycle = 1 s).

**Do:**
- Favor cache-friendly access patterns (sequential, local) — cache misses dwarf most algorithmic gains.
- Match the architecture to the problem: SIMD/GPU for data-parallel uniform ops; MIMD/CPU for diverse logic.
- Use prefetching, batching, and locality to reduce cache misses.
- Choose cache-line-aligned data structures.

**Don't:**
- Assume memory access is uniform — locality matters enormously.
- Choose CPU for uniform parallel ops (use GPU/SIMD).
- Ignore NUMA effects in multi-socket servers.

**Taxonomy (Flynn):** SISD · SIMD (GPUs, vector ops) · MISD (rare) · MIMD (multicore CPUs, clusters — most common).

*Ref: Grokking_Concurrency.md — "Cache", "Multiple levels of concurrent hardware", "CPU vs. GPU" (Ch. 3)*

---

### Moore's Law & Multicore Reality

**Principle:** Single-core clock speeds plateaued ~2005; performance gains now come from parallelism (more cores, more hardware threads). Software must be designed for parallelism to exploit modern hardware.

**Do:**
- Design software assuming multiple cores by default.
- Use parallel algorithms where applicable.
- Profile to identify parallelism opportunities.

**Don't:**
- Expect single-thread performance to keep growing — it won't.
- Assume "faster CPU" will save you — better algorithms + parallelism does.
- Ignore Amdahl's law — sequential code is a dead end for performance.

*Ref: Grokking_Concurrency.md — "Moore's law" (Ch. 1)*

---

### Layers of Concurrency

**Principle:** Concurrency exists at multiple layers — hardware (cores, threads), runtime (processes, threads), application (coroutines, futures, async), distributed (multiple machines). Each layer has different primitives and trade-offs.

**Do:**
- Match the layer to the workload:
  - Hardware parallelism: data-parallel computation.
  - OS threads: blocking I/O.
  - User-space (goroutines, async): high-concurrency I/O.
  - Distributed: independent services.
- Use the right abstraction for each layer — don't fight the runtime.

**Don't:**
- Use OS threads for thousands of connections — switch to user-space (goroutines, async).
- Use user-space for CPU-bound blocking work — need a real thread.
- Assume layers compose linearly — each has overhead.

*Ref: Grokking_Concurrency.md — "Layers of concurrency" (Ch. 1)*

---

### Processes vs. Threads

**Principle:** A *process* is a resource container (address space, files, connections); a *thread* is a unit of execution *within* a process. Threads share memory (fast communication, but require synchronization); processes are isolated (safe, but IPC is costly).

| Property        | Process             | Thread                  |
|-----------------|---------------------|-------------------------|
| Memory          | Isolated            | Shared address space    |
| Creation cost   | Heavyweight         | Lightweight             |
| Communication   | IPC (slow)          | Shared memory (fast)    |
| Crash impact    | Other processes safe| Whole process dies      |
| Synchronization | Kernel-mediated     | Required (locks etc.)   |

**Do:**
- Use processes for fault isolation (prefork servers like NGINX, Apache, Gunicorn).
- Use threads (or finer user-space units) when you need shared state and low communication overhead.
- Prefer high-level abstractions (Go goroutines, Scala parallel collections, Erlang processes) over raw POSIX threads.
- Understand the cost of each — process creation forks the address space.

**Don't:**
- Use raw low-level threads when a library/runtime abstraction will do.
- Assume threads are always faster than processes — context-dependent.
- Spawn a thread per connection at scale — context-switching dominates.

```python
# Chapter 4/multithreading.py — five child threads sharing one process.
import os, time, threading
from threading import Thread

def cpu_waster(i: int) -> None:
    name = threading.current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)

def main(num_threads: int) -> None:
    for i in range(num_threads):
        Thread(target=cpu_waster, args=(i,)).start()

if __name__ == "__main__":
    main(5)
```

*Ref: Grokking_Concurrency.md — "Processes", "Threads" (Ch. 4)*

---

### Interprocess Communication (IPC)

**Principle:** Two families: **shared memory** (fastest, but unsafe and doesn't scale past one machine) and **message passing** (safer, scales to distributed systems, but pays copy cost).

**Do:**
- Use shared memory only for local, high-throughput, same-machine data exchange — and synchronize access.
- Use message passing (pipes, queues, sockets) when you need decoupling, safety, or distribution.
- Go's philosophy ("share memory by communicating") and Erlang's pure message-passing model both favor message passing by default.

**IPC menu:**
- **Pipe (unnamed)** — one-way, related tasks only, dies with tasks.
- **Named pipe (FIFO)** — filesystem entity, unrelated tasks, FIFO order.
- **Message queue** — FIFO, multi-producer/multi-consumer, decouples producers from consumers.
- **Socket (UDS / network)** — bidirectional, network-extensible, requires serialization.

```python
# Chapter 5/message_queue.py — workers draining a shared queue.
from queue import Queue
from threading import Thread, current_thread

class Worker(Thread):
    def __init__(self, queue: Queue, id: int):
        super().__init__(name=str(id))
        self.queue = queue
    def run(self) -> None:
        while not self.queue.empty():
            item = self.queue.get()           # blocks until available
            print(f"Thread {current_thread().name}: processing item {item}")
            # ...process...

q = Queue()
for i in range(10):
    q.put(i)
threads = [Worker(q, i + 1) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()
```

```python
# Chapter 5/pipe.py — unnamed pipe between two threads.
from threading import Thread
from multiprocessing import Pipe

reader_conn, writer_conn = Pipe()
class Writer(Thread):
    def run(self): writer_conn.send("Rubber duck")
class Reader(Thread):
    def run(self): print("Received:", reader_conn.recv())

Writer().start(); Reader().start()
```

*Ref: Grokking_Concurrency.md — "Message queues", "Pipes" (Ch. 5)*

---

### Thread Pool Pattern

**Principle:** Pre-create a fixed set of long-lived worker threads and feed them from a shared queue. Eliminates per-task thread creation cost, bounds resource usage, and isolates task failures from workers.

**Do:**
- Default to thread pools for most concurrent applications.
- Set the pool size from empirical measurement, not guesswork.
- Size based on workload: CPU-bound → N cores; I/O-bound → N × (1 + W/C).
- Use thread-safe queues (`queue.Queue` in Python) instead of shared state.

**Don't use a pool when:**
- You need per-thread priorities.
- Tasks block for long periods (can starve the pool).
- You need a static thread identity.
- A task deserves a dedicated thread.

```python
# Chapter 5/thread_pool.py — minimal thread pool.
import queue, typing as T
from threading import Thread

Callback = T.Callable[..., None]
Task = T.Tuple[Callback, T.Any, T.Any]

class Worker(Thread):
    def __init__(self, tasks: "queue.Queue[Task]"):
        super().__init__()
        self.tasks = tasks
    def run(self) -> None:
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception as e: print(e)
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads: int):
        self.tasks: queue.Queue = queue.Queue(num_threads)
        for _ in range(num_threads):
            worker = Worker(self.tasks)
            worker.setDaemon(True)   # exit when main thread exits
            worker.start()
    def submit(self, func: Callback, *args, **kargs) -> None:
        self.tasks.put((func, args, kargs))
    def wait_completion(self) -> None:
        self.tasks.join()
```

*Ref: Grokking_Concurrency.md — "Thread pool pattern" (Ch. 5)*

---

### Multitasking & Context Switching

**Principle:** *Preemptive multitasking* gives each task a time slice and interrupts it via a timer; the OS creates the illusion of simultaneous execution even on one core. Context switches cost ~800–1300 ns each (~9,000–15,000 instructions lost per switch).

**Do:**
- Keep the number of runnable tasks proportional to cores — too many tasks → thrashing.
- Distinguish CPU-bound tasks (context switching hurts) from I/O-bound tasks (context switching helps — the CPU stays busy while one task waits).
- Use cooperative multitasking (async/await) when you control all yield points.

**Don't:**
- Rely on observed scheduling order — it's nondeterministic; synchronize explicitly when order matters.
- Spawn thousands of threads for I/O-bound work — use async runtime.
- Assume context switches are free — they cost ~1 µs.

*Ref: Grokking_Concurrency.md — "Multitasking", "Context switching" (Ch. 6)*

---

### CPU-bound vs I/O-bound Tasks

**Principle:** Different task types need different concurrency strategies.

**CPU-bound:** Computation is the bottleneck (matrix multiplication, encryption, compression).
- Use thread pools sized to N cores.
- Excessive parallelism wastes CPU on context switching.
- Amdahl's law dominates.

**I/O-bound:** Waiting for external resources (DB queries, network calls, disk reads).
- Use many threads or async tasks (limited by memory, not CPU).
- Concurrency hides latency — one task waits while another computes.
- More parallelism = more throughput.

**Mixed:** Some compute + some I/O.
- Use event loop + worker pool hybrid.
- Offload CPU work to dedicated thread pool.
- Use async for I/O, threads for CPU.

**Do:**
- Profile to determine if tasks are CPU or I/O bound.
- Match concurrency strategy to task type.
- Monitor queue depth, CPU utilization, and wait time.

**Don't:**
- Use async for CPU-bound work — no natural yield points.
- Use thread-per-task for I/O-bound at scale — context-switching dominates.
- Assume task type — measure.

*Ref: Grokking_Concurrency.md — "CPU-bound and I/O-bound applications" (Ch. 6)*

---

### Multitasking Environments

**Principle:** Three primary multitasking models in modern systems.

**Preemptive (OS-managed):** Kernel timer interrupts tasks; scheduler decides who runs. Used by OS threads.
- Pros: fair scheduling, isolation.
- Cons: context switch overhead.

**Cooperative (runtime-managed):** Tasks yield voluntarily at known points. Used by async/await, coroutines.
- Pros: no preemption overhead, predictable.
- Cons: one misbehaving task blocks everything.

**Hybrid:** Cooperative within cooperative frameworks, preemptive at OS level.
- Common in modern runtimes.

**Do:**
- Choose preemptive for general-purpose OS threads.
- Choose cooperative for I/O-bound async servers.
- Understand which model your runtime uses.

**Don't:**
- Mix blocking calls into cooperative runtimes.
- Assume "preemptive" means "fair" — priorities still matter.

*Ref: Grokking_Concurrency.md — "Multitasking environments" (Ch. 6)*

---

### Decomposition — Task vs. Data

**Principle:** Before writing concurrent code, build a **task dependency graph** and find independent work. Two complementary techniques: **task decomposition** (split by function) and **data decomposition** (split by data chunk). Combine them for maximum concurrency.

**Do:**
- Draw the dependency graph; concurrency is possible wherever there's no edge.
- Use task decomposition for MIMD systems; data decomposition for SIMD.
- Combine pipeline (task) + chunking (data) for compound speedups.
- Start with sequential design, then identify independent operations.

**Don't:**
- Decompose by data when tasks have heavy shared state — high coordination cost.
- Decompose by task when operations are uniform on data — SIMD would win.
- Decompose too finely — coordination overhead dominates.

*Ref: Grokking_Concurrency.md — "Dependency analysis", "Task decomposition", "Data decomposition" (Ch. 7)*

---

### Pipeline Pattern (Task Decomposition)

**Principle:** Split an algorithm into ordered stages, each running concurrently and handing results to the next. Best when shared resources (a single washer/dryer) limit pure parallelism. Steady-state throughput = 1 / (slowest stage time).

**Do:**
- Use pipelines when resources are limited (filesystems, DB connections) — bound the threads per stage.
- Combine with data decomposition to parallelize within a stage.
- Balance stage times — slowest stage determines throughput.
- Use bounded queues between stages to prevent unbounded memory growth.

**Don't:**
- Use unbounded queues — memory blowup on producer > consumer.
- Make one stage much slower than others — bottleneck.
- Couple stages tightly — defeats the pipeline's decoupling benefit.

```python
# Chapter 7/pipeline.py — washer → dryer → folder, each on its own thread.
import time
from queue import Queue
from threading import Thread

Washload = str

class Washer(Thread):
    def __init__(self, in_q: Queue, out_q: Queue):
        super().__init__(); self.in_q, self.out_q = in_q, out_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(4)                # wash
            self.out_q.put(load)
            self.in_q.task_done()

class Dryer(Thread):
    def __init__(self, in_q: Queue, out_q: Queue):
        super().__init__(); self.in_q, self.out_q = in_q, out_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(2)                # dry
            self.out_q.put(load)
            self.in_q.task_done()

class Folder(Thread):
    def __init__(self, in_q: Queue):
        super().__init__(); self.in_q = in_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(1)                # fold
            print(f"{load} done!")
            self.in_q.task_done()

to_wash, to_dry, to_fold = Queue(), Queue(), Queue()
Washer(to_wash, to_dry).start()
Dryer(to_dry, to_fold).start()
Folder(to_fold).start()
for n in range(8): to_wash.put(f"Washload #{n}")
to_wash.join(); to_dry.join(); to_fold.join()
```

*Ref: Grokking_Concurrency.md — "Pipeline pattern" (Ch. 7)*

---

### Map, Fork/Join, Map/Reduce (Data Decomposition)

**Principle:** Three canonical data-decomposition patterns:

- **Map** — one operation applied to every element independently (embarrassingly parallel).
- **Fork/Join** — split work into chunks, process in parallel, then aggregate (join) the partial results.
- **Map/Reduce** — map step produces intermediate results; reduce step aggregates. Scales beyond one machine (Hadoop, Spark).

**Do:**
- Use **map** for uniform per-element operations.
- Use **fork/join** for parallel aggregation on a single machine.
- Use **map/reduce** when scaling beyond one machine.
- Combine with task decomposition (pipeline) for compound speedups.
- Use thread pools (not raw threads) for fork/join.

**Don't:**
- Use fork/join when communication between workers is needed — defeats purpose.
- Use map/reduce on a single machine — fork/join is sufficient and simpler.
- Assume map is always faster — overhead of parallel coordination matters.

```python
# Chapter 7/count_votes/count_votes_concurrent.py — fork/join on vote piles.
from multiprocessing.pool import ThreadPool

def process_pile(pile):
    summary = {}
    for vote in pile:
        summary[vote] = summary.get(vote, 0) + 1
    return summary

def process_votes(pile, worker_count: int = 4):
    vpw = len(pile) // worker_count
    vote_piles = [pile[i*vpw:(i+1)*vpw] for i in range(worker_count)]
    with ThreadPool(worker_count) as pool:           # FORK
        worker_summaries = pool.map(process_pile, vote_piles)
    total = {}                                       # JOIN
    for ws in worker_summaries:
        for c, n in ws.items():
            total[c] = total.get(c, 0) + n
    return total
```

*Ref: Grokking_Concurrency.md — "Map pattern", "Fork/Join pattern", "Map/Reduce pattern" (Ch. 7)*

---

### Loop-Level Parallelism

**Principle:** Loops where each iteration is independent = candidates for parallel execution. **OpenMP** uses this for CPUs; **CUDA** for GPUs; map patterns in most languages.

**Do:**
- Identify loops with independent iterations — analyze data dependencies.
- Apply data decomposition to loop iterations (chunked across workers).
- Use existing libraries (OpenMP, ThreadPool, parallel collections) rather than manual loops.
- Verify that iterations truly are independent — false sharing can hurt performance.

**Don't:**
- Parallelize loops with cross-iteration dependencies (each iteration reads previous).
- Use too fine granularity — overhead exceeds gain.
- Ignore cache locality — adjacent iterations may share cache lines.

```python
# Chapter 7/find_files/find_files_concurrent.py — concurrent file search.
import os, time, typing as T, glob
from multiprocessing.pool import ThreadPool

def search_file(file_location: str, search_string: str) -> bool:
    with open(file_location, "r", encoding="utf8") as file:
        return search_string in file.read()

def search_files_concurrently(file_locations: T.List[str],
                              search_string: str) -> None:
    with ThreadPool() as pool: 
        results = pool.starmap(search_file, 
            ((file_location, search_string) for 
             file_location in file_locations))
    for result, file_name in zip(results, file_locations):
        if result:
            print(f"Found string in file: `{file_name}`")
```

*Ref: Grokking_Concurrency.md — "Loop-level parallelism" (Ch. 7)*

---

### Granularity & Agglomeration

**Principle:** *Granularity* = task size/count. Fine-grained → more parallelism but more communication/scheduling overhead; coarse-grained → less overhead but risk of load imbalance. Find the sweet spot; merge tasks (*agglomeration*) to cut communication when beneficial.

**Do:**
- Aim for at least as many tasks as processors, preferably more, to give the scheduler flexibility.
- Agglomerate tiny tasks when communication cost dominates.
- Measure load balance — adjust chunk sizes accordingly.
- Tune empirically; don't guess.

**Don't:**
- Use one task per data element — overhead dominates.
- Use one task total — no parallelism.
- Ignore communication cost — fine-grained tasks can be slower than coarse.

*Ref: Grokking_Concurrency.md — "Granularity" (Ch. 7)*

---

### Race Conditions & Critical Sections

**Principle:** A **race condition** occurs when correctness depends on the relative timing of concurrent operations. A **critical section** is code that accesses shared resources and must execute atomically. Race-condition bugs are *heisenbugs* — they disappear when you try to observe them.

**Do:**
- Treat every shared mutable resource as a critical section needing protection.
- Verify libraries are thread-safe before sharing them across tasks.
- Reproduce races by inserting strategic `sleep`s to perturb timing (debugging only, never a fix).
- Minimize critical section size — every byte inside the lock is serialized time.

**Don't:**
- Assume read-modify-write sequences like `balance += amount` are atomic — they aren't.
- Rely on "it works on my machine" — races are nondeterministic.
- Fix races with timing — synchronize correctly instead.

```python
# Chapter 8/race_condition/unsynced_bank_account.py — UNSAFE.
class UnsyncedBankAccount(BankAccount):
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount              # read / add / write — race!
        else:
            raise ValueError("You can't deposit a negative amount of money")
    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Account does not have sufficient funds")
```

*Ref: Grokking_Concurrency.md — "Race conditions" (Ch. 8)*

---

### Synchronization Primitives — Mutex, Semaphore, Atomic

**Principle:** Pick the smallest primitive that works. Atomic operations > mutexes > semaphores in cost; semaphores handle multi-permit resources that mutexes can't.

| Primitive | Counter | Use case |
|-----------|---------|----------|
| Atomic op | n/a (hardware) | Simple primitive-type ops (increment, CAS) |
| Mutex (binary semaphore) | 0/1 | Exclusive access to one resource |
| Semaphore (counting) | 0..N | Pool of N equivalent resources |
| RWLock | readers count + write flag | Read-heavy shared state |

**Do:**
- Keep critical sections as short as possible.
- Acquire/release locks in a consistent global order to avoid deadlocks.
- Use atomics when the operation is a primitive-type op — they don't block.
- Use semaphores for resource pools (DB connections, thread permits).

**Don't:**
- Mix synchronization styles on the same resource; pick one and apply it everywhere.
- Hold a lock while calling external systems — slow, deadlock-prone.
- Use a heavyweight primitive when atomic would do.

```python
# Chapter 8/race_condition/synced_bank_account.py — mutex around balance.
from threading import Lock

class SyncedBankAccount(UnsyncedBankAccount):
    def __init__(self, balance: float = 0):
        super().__init__(balance)
        self.mutex = Lock()
    def deposit(self, amount: float) -> None:
        self.mutex.acquire()
        try: super().deposit(amount)
        finally: self.mutex.release()
    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        try: super().withdraw(amount)
        finally: self.mutex.release()
```

```python
# Chapter 8/semaphore.py — counting semaphore as a parking garage (3 spots).
from threading import Thread, Semaphore, Lock

TOTAL_SPOTS = 3

class Garage:
    def __init__(self):
        self.semaphore = Semaphore(TOTAL_SPOTS)   # N permits
        self.cars_lock = Lock()
        self.parked_cars = []
    def enter(self, name):
        self.semaphore.acquire()                  # take a spot
        with self.cars_lock:
            self.parked_cars.append(name)
            print(f"{name} parked")
    def exit(self, name):
        with self.cars_lock:
            self.parked_cars.remove(name)
            print(f"{name} leaving")
        self.semaphore.release()                  # free a spot
```

*Ref: Grokking_Concurrency.md — "Mutual exclusion", "Semaphores" (Ch. 8)*

---

### Deadlocks — Coffman Conditions & Solutions

**Principle:** Deadlock needs all four Coffman conditions: **mutual exclusion**, **hold-and-wait**, **no preemption**, **circular wait**. Break any one to prevent deadlock.

**Classic solutions (illustrated via dining philosophers):**

| Solution              | Condition broken            | Trade-off |
|-----------------------|-----------------------------|-----------|
| Arbitrator (waiter)   | Hold-and-wait (atomic grab) | Limits concurrency |
| Resource hierarchy    | Circular wait (global order)| Simple, effective |
| Lock timeout          | No preemption (give up)     | Can cause livelock |

**Do:**
- Impose a global lock-ordering hierarchy whenever a task takes multiple locks.
- When a task must grab multiple locks atomically, gate the grab behind a single arbitrator lock.
- Use `tryLock(timeout)` to detect and recover from deadlock-prone situations.
- Document lock ordering in code — it must be consistent across all callers.

**Don't:**
- Acquire the same set of locks in different orders from different tasks.
- Assume deadlock is rare — design defensively.
- Hold locks across blocking calls (I/O, sleep).

```python
# Chapter 9/deadlock/deadlock_hierarchy.py — fix by ordering chopstick acquisition.
from deadlock import Philosopher
from lock_with_name import LockWithName

chopstick_a = LockWithName("chopstick_a")
chopstick_b = LockWithName("chopstick_b")
# Both philosophers grab A first, then B — circular wait is impossible.
philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
philosopher_2 = Philosopher("Philosopher #2", chopstick_a, chopstick_b)
philosopher_1.start(); philosopher_2.start()
```

*Ref: Grokking_Concurrency.md — "Arbitrator solution", "Resource hierarchy solution" (Ch. 9)*

---

### Livelocks & Starvation

**Principle:** A **livelock** has tasks actively running but making no progress (each politely gives way). **Starvation** is a task never getting resources because greedy peers hog them. Detect starvation with metrics — record work accomplished per task.

**Do:**
- Use priority queuing with **aging** (gradually raise priority of long-waiting tasks) to fight starvation.
- Resolve livelocks with the same lock-ordering hierarchy used for deadlocks.
- Detect both via metrics — work accomplished per task over time.
- Add **random jitter** to retry intervals to break synchronization.

**Don't:**
- Add random backoff alone — can produce livelock if both tasks back off in sync.
- Assume fairness — most schedulers are not strictly fair.
- Ignore starvation symptoms — slow tasks are usually symptoms of a deeper problem.

```python
# Chapter 9/starvation.py — count per-philosopher dumplings to surface unfairness.
from threading import Thread
from deadlock.lock_with_name import LockWithName

dumplings = 1000

class Philosopher(Thread):
    def __init__(self, name, left, right):
        super().__init__(); self.name=name; self.left=left; self.right=right
    def run(self):
        global dumplings
        eaten = 0
        while dumplings > 0:
            self.left.acquire(); self.right.acquire()
            if dumplings > 0:
                dumplings -= 1
                eaten += 1
            self.right.release(); self.left.release()
        print(f"{self.name} took {eaten} pieces")
# Output shows extreme imbalance (#1: 417, #9: 0, ...) → starvation.
```

*Ref: Grokking_Concurrency.md — "Livelocks", "Starvation" (Ch. 9)*

---

### Producer–Consumer Problem

**Principle:** Decouple producers from consumers via a bounded buffer. Three sync primitives coordinate them: a **mutex** guards the buffer, an **empty** semaphore counts free slots, a **full** semaphore counts filled slots.

**Pattern:**
- Producer: `empty.acquire()` (wait for free slot) → `mutex.acquire()` → write → `mutex.release()` → `full.release()`.
- Consumer: `full.acquire()` (wait for item) → `mutex.acquire()` → read → `mutex.release()` → `empty.release()`.

**Do:**
- Use bounded buffers — prevent memory blowup.
- Use semaphores for counting slots; mutex for buffer access.
- Handle shutdown gracefully — drain queues on shutdown.

**Don't:**
- Use unbounded buffers — memory exhaustion.
- Mix producer/consumer responsibilities in one thread.
- Forget about graceful shutdown — drain or kill.

```python
# Chapter 9/producer_consumer.py — bounded buffer with mutex + two semaphores.
from threading import Thread, Semaphore, Lock

SIZE = 5
BUFFER = [""] * SIZE
producer_idx = 0
mutex = Lock()
empty = Semaphore(SIZE)    # free slots
full  = Semaphore(0)       # filled slots

class Producer(Thread):
    def run(self):
        global producer_idx
        for i in range(5):
            empty.acquire(); mutex.acquire()
            BUFFER[producer_idx] = f"P-{i}"
            producer_idx = (producer_idx + 1) % SIZE
            mutex.release(); full.release()

class Consumer(Thread):
    def __init__(self):
        super().__init__(); self.idx = 0
    def run(self):
        for i in range(10):
            full.acquire(); mutex.acquire()
            item = BUFFER[self.idx]
            self.idx = (self.idx + 1) % SIZE
            mutex.release(); empty.release()
            print("consumed", item)
```

*Ref: Grokking_Concurrency.md — "Producer-consumer problem" (Ch. 9)*

---

### Readers–Writer Problem

**Principle:** Multiple readers can read concurrently; writers need exclusive access. A **readers-writer lock (RWLock)** exposes `acquire_read`/`release_read` (shared) and `acquire_write`/`release_write` (exclusive). Big win when reads vastly outnumber writes.

**Do:**
- Use RWLocks for read-heavy shared state (caches, catalogs, configs).
- First reader acquires the write lock to block writers; last reader releases it.
- Detect writer starvation and apply aging if needed.

**Don't:**
- Use RWLock when writes dominate — overhead exceeds benefit.
- Hold read lock across blocking I/O — blocks writers.
- Implement custom RWLock — most languages have battle-tested ones.

```python
# Chapter 9/reader_writer/rwlock.py — hand-rolled RWLock (Python has none built in).
from threading import Lock

class RWLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()
    def acquire_read(self):
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1:           # first reader blocks writers
            self.write_lock.acquire()
        self.read_lock.release()
    def release_read(self):
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:           # last reader unblocks writers
            self.write_lock.release()
        self.read_lock.release()
    def acquire_write(self):  self.write_lock.acquire()
    def release_write(self):  self.write_lock.release()
```

*Ref: Grokking_Concurrency.md — "Readers-writer problem" (Ch. 9)*

---

### Designing Synchronization — Beyond Correctness

**Principle:** Synchronization decisions go beyond "make it work" — they affect performance, scalability, and maintainability.

**Do:**
- Profile **before** adding synchronization — locks have cost.
- Use **lock-free** data structures for hot paths (CAS-based queues, atomic counters).
- Minimize **lock granularity** — protect data, not code.
- Consider **read-copy-update (RCU)** for read-heavy data with rare writes.
- Apply **lock striping** for high-contention locks (e.g., `ConcurrentHashMap`).

**Don't:**
- Add locks preemptively to "be safe" — measure first.
- Hold a single global lock across the whole system — kills scalability.
- Use busy-wait as a synchronization mechanism — burns CPU.

*Ref: Grokking_Concurrency.md — "Designing synchronization" (Ch. 9)*

---

### C10k Problem & Nonblocking I/O

**Principle:** Thread-per-connection servers can't scale past ~10,000 concurrent connections — context-switching overhead dominates when thread count ≫ core count. **Nonblocking I/O** + a single thread (or small pool) overlaps many I/O operations without thread overhead.

**Do:**
- For high-concurrency I/O servers, prefer nonblocking sockets + an event loop (or async/await) over thread-per-connection.
- Remember: nonblocking I/O is not *faster* per operation — it just lets the CPU do useful work while waiting.
- Use I/O multiplexing (`select`/`poll`/`epoll`/`kqueue`) to wait on many sockets simultaneously.
- Use **edge-triggered** epoll for high-performance servers.

**Don't:**
- Busy-wait in a tight loop polling nonblocking sockets — that burns a whole core. Use multiplexing (`select`/`poll`/`epoll`/`kqueue`) or async runtimes.
- Use thread-per-connection for >1000 concurrent connections.
- Mix blocking and nonblocking code — pick one model.

```python
# Chapter 10/pizza_busy_wait.py — nonblocking socket server, single thread.
from socket import socket, create_server

class Server:
    def __init__(self):
        self.server_socket = create_server(("127.0.0.1", 12345))
        self.server_socket.setblocking(False)        # nonblocking
        self.clients = set()
    def accept(self):
        try:
            conn, addr = self.server_socket.accept()
            conn.setblocking(False)
            self.clients.add(conn)
        except BlockingIOError:
            pass                                    # no pending connection
    def serve(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.send(b"response\n")
        except BlockingIOError:
            pass                                    # no data yet
    def start(self):
        while True:
            self.accept()
            for conn in self.clients.copy():
                self.serve(conn)
```

*Ref: Grokking_Concurrency.md — "C10k problem", "Nonblocking I/O" (Ch. 10)*

---

### Event-Based Concurrency & the Reactor Pattern

**Principle:** An **event loop** watches many file descriptors via I/O multiplexing (`select`/`poll`/`epoll`) and dispatches ready events to handlers/callbacks. The **Reactor pattern** formalizes this: synchronous demultiplexing of events to nonblocking handlers.

**Why it beats threads for I/O-heavy servers:**
- One thread, no context-switching cost, no synchronization between handlers.
- Scales linearly with the multiplexer's fd limit (epoll handles hundreds of thousands).

**Trade-off:** handlers must be nonblocking and short — a single slow handler stalls the whole loop. Long work must be offloaded to a worker pool.

**Do:**
- Use the reactor pattern for I/O-heavy servers (NGINX, Node.js, Redis).
- Keep handlers **nonblocking** and short.
- Offload CPU-bound work to a worker pool.
- Use the OS's most efficient multiplexer (epoll on Linux, kqueue on BSD/macOS).

**Don't:**
- Use blocking calls in handlers — stalls the entire event loop.
- Hold state across handler invocations — must be re-entrant.
- Mix reactor with traditional threads — adds complexity without benefit.

*Ref: Grokking_Concurrency.md — "Event-based concurrency", "Reactor pattern", "Event loop", "I/O multiplexing" (Ch. 11)*

---

### Synchronous vs Asynchronous Communication

**Principle:** Synchronous communication requires both parties ready simultaneously — blocks until done. Asynchronous allows sender to continue — receiver accesses results later.

**Synchronous:**
- Both parties must coordinate at the same time.
- Caller blocks until operation completes.
- Easier to reason about.
- Lower CPU utilization (waiting).

**Asynchronous:**
- Sender doesn't wait.
- Receiver pulls or gets pushed.
- Higher CPU utilization.
- More complex (callbacks, futures).

**Do:**
- Use **synchronous** for sequential, dependent operations.
- Use **asynchronous** for independent operations or when waiting is long.
- Decouple producers from consumers via async messaging.
- Understand that "asynchronous" doesn't mean "faster" — it means "non-blocking."

**Don't:**
- Use async where simple sync would do — added complexity.
- Use sync for high-latency operations — blocks threads.
- Mix sync and async without clear boundaries.

*Ref: Grokking_Concurrency.md — "Synchronization in message passing" (Ch. 11)*

---

### I/O Models — Four Combinations

**Principle:** Blocking/nonblocking × synchronous/asynchronous gives four I/O models. Each has different characteristics.

| Model | Blocking | Sync | Use case |
|---|---|---|---|
| **Synchronous blocking** | Yes | Yes | Simplest; thread-per-connection |
| **Synchronous nonblocking** | No (immediate return) | Yes (caller polls) | Rare; busy-wait |
| **Asynchronous blocking** | No | Yes (select blocks, not I/O) | Reactor pattern |
| **Asynchronous nonblocking** | No | No | Proactor pattern (IOCP, io_uring) |

**Do:**
- Use **synchronous blocking** for simple thread-per-connection servers.
- Use **asynchronous blocking** (reactor + select/epoll) for high-concurrency servers.
- Use **asynchronous nonblocking** (proactor, io_uring) for highest performance.

**Don't:**
- Use busy-wait nonblocking — burns CPU.
- Mix models in the same code — pick one.

*Ref: Grokking_Concurrency.md — "I/O models" (Ch. 11)*

---

### Asynchronous Communication & Cooperative Multitasking

**Principle:** Cooperative multitasking (async/await, coroutines, futures) lets a single thread suspend at await points and resume later — the runtime, not a preemptive timer, decides when to yield.

**Do:**
- Use async/await for I/O-bound, high-concurrency work (web servers, scrapers, gateways).
- Keep CPU-bound work in a separate thread/process — it has no natural await points.
- Use **structured concurrency** to scope async tasks (Python `asyncio.TaskGroup`, Java virtual threads, Kotlin coroutines).
- Set timeouts on every async operation — prevent hanging.

**Don't:**
- Mix blocking calls into an async event loop — they stall every other task.
- Assume async is always faster — coordination overhead.
- Create unbounded numbers of tasks — memory leak.

*Ref: Grokking_Concurrency.md — "Asynchronous communication", "Cooperative multitasking", "Future objects" (Ch. 12)*

---

### Coroutines & User-Level Threads

**Principle:** Coroutines are user-level threads — paused and resumed by the program, not the OS. Lighter than OS threads; can have millions per process.

**Do:**
- Use coroutines for cooperative multitasking (async/await, generators).
- Yield at I/O points to let other coroutines run.
- Use structured concurrency (`async with`, `TaskGroup`) for clean task lifecycle management.

**Don't:**
- Mix coroutines with blocking calls.
- Assume coroutines run in parallel — single-threaded unless scheduler uses multiple.
- Forget cancellation — coroutines need explicit cancellation paths.

```python
# Chapter 12/coroutine.py — Fibonacci via coroutines and event loop.
from collections import deque
import typing as T
Coroutine = T.Generator[None, None, int]

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    def add_coroutine(self, task: Coroutine) -> None: 
        self.tasks.append(task) 
    def run_coroutine(self, task: Coroutine) -> None:
        try:
            task.send(None) 
            self.add_coroutine(task)
        except StopIteration: 
            print("Task completed")
    def run_forever(self) -> None: 
        while self.tasks: 
            print("Event loop cycle.") 
            self.run_coroutine(self.tasks.popleft()) 

def fibonacci(n: int) -> Coroutine:
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        yield 
    return a

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonacci(5)) 
    event_loop.run_forever()
```

*Ref: Grokking_Concurrency.md — "Coroutines (user-level threads)" (Ch. 12)*

---

### Future Objects & Promises

**Principle:** A **Future** (or Promise, Delay, Deferred) is a placeholder for a value not yet computed. The caller can check for completion or be notified when the value is ready.

**Do:**
- Use Future/Promise for "call this async, get result later" patterns.
- Combine with coroutines for clean async/await syntax.
- Use `Promise.all()` (JavaScript) for parallel async coordination.
- Handle errors in Futures explicitly — they're not auto-propagated.

**Don't:**
- Block waiting on a Future in a sync context — defeats the purpose.
- Forget to handle Future completion — it may never resolve.

```python
# Chapter 12/future_burger.py — Future-based async ordering.
from __future__ import annotations
import typing as T
from collections import deque
from random import randint
Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']

class Future:
    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None
    def set_coroutine(self, coroutine: Coroutine) -> None: 
        self.coroutine = coroutine
    def set_result(self, result: Result) -> None: 
        self.done = True
        self.result = result
    def __iter__(self) -> Future:
        return self
    def __next__(self) -> Result: 
        if not self.done: 
            raise StopIteration
        return self.result

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    def add_coroutine(self, task: Coroutine) -> None:
        self.tasks.append(task)
    def run_coroutine(self, task: T.Callable) -> None:
        future = task() 
        future.set_coroutine(task) 
        try: 
            next(future) 
            if not future.done: 
                future.set_coroutine(task) 
                self.add_coroutine(task) 
        except StopIteration: 
            return
    def run_forever(self) -> None:
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())

def cook(on_done: T.Callable[[Burger], None]) -> None: 
    burger: str = f"Burger #{randint(1, 10)}" 
    print(f"{burger} is cooked!") 
    on_done(burger) 

def cashier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None:
    print("Burger is ready for pick up!") 
    on_done(burger) 

def order_burger() -> Future:
    order = Future() 
    def on_cook_done(burger: Burger) -> None:
        cashier(burger, on_cashier_done)
    def on_cashier_done(burger: Burger) -> None:
        print(f"{burger}? That's me! Mmmmmm!")
        order.set_result(burger)
    cook(on_cook_done) 
    return order

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()
```

*Ref: Grokking_Concurrency.md — "Future objects" (Ch. 12)*

---

### Cooperative vs Preemptive Multitasking — Comparison

**Principle:** Two multitasking paradigms with different trade-offs.

| Aspect | Preemptive | Cooperative |
|---|---|---|
| Scheduler | OS kernel | Runtime / program |
| Context switch | Hardware interrupt | Explicit yield |
| Cost | ~1 µs | ~10 ns (function call) |
| Scalability | Thousands of threads | Millions of coroutines |
| Pitfall | Priority inversion | One bad task blocks all |
| Examples | OS threads | async/await, goroutines |

**Do:**
- Use **preemptive** for general-purpose OS threads (fairness, isolation).
- Use **cooperative** for high-concurrency I/O servers (millions of connections).
- Combine — OS threads run coroutines; coroutines yield to each other.

**Don't:**
- Use preemptive for millions of tasks — context switch cost dominates.
- Use cooperative when one misbehaving task can block others — unsafe in adversarial settings.

*Ref: Grokking_Concurrency.md — "Cooperative multitasking" (Ch. 12)*

---

### Foster's Methodology

**Principle:** Foster's design methodology is a systematic approach for designing parallel algorithms: **Partition → Communicate → Agglomerate → Map** (PCAM).

**Steps:**
1. **Partition:** Divide computation into tasks and data into chunks.
2. **Communicate:** Identify communication patterns between tasks.
3. **Agglomerate:** Combine tasks/chunks to reduce communication overhead.
4. **Map:** Assign tasks to processors.

**Do:**
- Use PCAM for parallel algorithm design (matrix multiplication, FFT, sorting).
- Iterate — refining one step may require revisiting previous steps.
- Evaluate communication-to-computation ratio at each step.

**Don't:**
- Skip the partition step — it's the foundation.
- Ignore communication patterns — they dominate parallel performance.
- Map before agglomerating — usually results in too many tiny tasks.

*Ref: Grokking_Concurrency.md — "Foster's methodology" (Ch. 13)*

---

### Matrix Multiplication — Parallel Case Study

**Principle:** Matrix multiplication is a classic parallel-computing problem. Multiple parallelization strategies with different trade-offs.

**Approaches:**
1. **Row-wise decomposition:** Each worker computes one row of the result.
2. **Column-wise decomposition:** Each worker computes one column.
3. **Block decomposition:** Divide matrix into sub-blocks; each worker computes one block.
4. **Fox's algorithm:** Broadcast + computation phases for distributed memory.
5. **Cannon's algorithm:** Skewed block distribution for distributed memory.

**Do:**
- Use **row-wise** for simplicity when N is small.
- Use **block decomposition** for better cache utilization (each block fits in L1).
- Use **Fox's or Cannon's** for distributed memory (MPI) systems.
- Pad matrices to avoid bank conflicts in GPU.

**Don't:**
- Ignore cache effects — naive multiplication has poor locality.
- Synchronize too often — defeats parallelism.
- Use single worker for large matrices.

*Ref: Grokking_Concurrency.md — "Matrix multiplication" (Ch. 13)*

---

### Distributed Word Count — MapReduce Pattern

**Principle:** MapReduce = data-parallel computation across many machines. Map step produces (key, value) pairs; reduce step aggregates by key. Used by Hadoop, Spark.

**Workflow:**
1. **Split:** Divide input into chunks (one per mapper).
2. **Map:** Apply function to each chunk; emit intermediate (key, value) pairs.
3. **Shuffle:** Group by key (across machines).
4. **Reduce:** Apply aggregate function per key group.
5. **Output:** Write results.

**Do:**
- Use MapReduce when data is too large for one machine.
- Design map and reduce functions as pure (no side effects).
- Use **combiner** (local reduce before shuffle) for efficiency.
- Choose appropriate partitioner for key distribution.

**Don't:**
- Use MapReduce for interactive queries — too much latency.
- Store large intermediate state in memory.
- Assume map and reduce scale independently.

*Ref: Grokking_Concurrency.md — "Distributed word count" (Ch. 13)*

---

### Concurrent Programming Step-by-Step

**Principle:** A structured approach to building concurrent applications.

**Steps:**
1. **Identify concurrency:** Where are the independent tasks?
2. **Choose decomposition:** Task-based, data-based, or both.
3. **Select primitives:** Threads, processes, coroutines, actors.
4. **Design communication:** Shared memory, message passing, queues.
5. **Add synchronization:** Locks, semaphores, atomic operations.
6. **Handle failures:** Cancellation, timeouts, retries.
7. **Test:** Stress tests, race detectors, code review.

**Do:**
- Follow the steps in order — don't skip decomposition.
- Use the right primitive for each layer.
- Add monitoring from day 1 — distributed debugging is hard.

**Don't:**
- Jump to implementation before designing.
- Mix primitives without understanding.
- Skip testing under load — concurrency bugs are subtle.

*Ref: Grokking_Concurrency.md — "Concurrent programming steps" (Ch. 4)*

---

### IPC Implementation Details

**Principle:** IPC mechanisms have specific characteristics that affect performance and reliability.

**Sockets:**
- Stream (TCP) vs datagram (UDP).
- Each side: local IP + port + remote IP + port.
- TCP: connection-oriented, reliable, ordered.
- UDP: connectionless, unreliable, fast.

**Pipes:**
- Unnamed: parent-child only, one-way, OS-managed.
- Named (FIFO): filesystem-based, unrelated processes.

**Message Queues (POSIX):**
- `mq_open`, `mq_send`, `mq_receive`, `mq_close`.
- Persistent across process termination.
- Bounded by `/proc/sys/fs/mqueue/msg_max`.

**Shared Memory:**
- `shm_open`, `mmap`.
- Fastest IPC; requires synchronization.
- Persists across process termination.

**Do:**
- Use **sockets** for network communication.
- Use **message queues** for cross-process task handoff.
- Use **shared memory** only when speed is critical and synchronization is manageable.

**Don't:**
- Use **unnamed pipes** across unrelated processes.
- Use **shared memory** without synchronization — undefined behavior.

*Ref: Grokking_Concurrency.md — "Types of communication" (Ch. 5)*

---

### Thread Cracking Passwords — Case Study

**Principle:** Password cracking is an embarrassingly parallel task — each hash check is independent. Threads are ideal.

**Pattern:**
1. Generate hashes for password candidates.
2. Compare to target hash.
3. Report if match found.

**Optimization:**
- Divide candidate space across workers.
- Use efficient hashing (no string operations).
- Stop early on match (cancellation).

```python
# (paraphrased from Ch 3 example)
import hashlib
from threading import Thread, Event

target_hash = hashlib.sha256(b"secret").hexdigest()
found = Event()

def crack(start: int, end: int) -> None:
    for i in range(start, end):
        candidate = str(i).encode()
        h = hashlib.sha256(candidate).hexdigest()
        if h == target_hash:
            print(f"Found password: {candidate}")
            found.set()
            return
        if found.is_set():
            return

NUM_WORKERS = 4
chunk = 1000000 // NUM_WORKERS
threads = []
for i in range(NUM_WORKERS):
    t = Thread(target=crack, args=(i*chunk, (i+1)*chunk))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
```

*Ref: Grokking_Concurrency.md — "Cracking passwords" (Ch. 3, 5)*

---

### Concurrency vs Distributed Systems

**Principle:** Concurrency and distribution are related but distinct.

**Concurrency:** Multiple tasks in one process (or coordinated processes).
- Shared memory (or message passing).
- Fast communication (ns–µs).
- Synchronized via locks, channels.

**Distribution:** Multiple independent processes/nodes.
- No shared memory.
- Slow communication (ms–seconds).
- Tolerates partial failure.

**Do:**
- Use **concurrency** within a single node.
- Use **distribution** across nodes.
- Recognize the crossover: when communication cost exceeds task duration, concurrency breaks down.

**Don't:**
- Use distribution for problems that fit on one machine.
- Treat distributed systems as just "more concurrent" — partial failures change everything.

*Ref: Grokking_Concurrency.md — Distributed vs concurrent themes*

---

### Foster's Parallel Algorithm Design

**Principle:** PCAM (Partition, Communicate, Agglomerate, Map) is a systematic methodology for designing parallel algorithms. Each step refines the previous.

**Phase 1: Partition**
- **Task decomposition:** Divide work into independent tasks.
- **Data decomposition:** Divide data into independent chunks.
- Aim for tasks >> processors (oversubscribe).

**Phase 2: Communicate**
- Identify communication patterns: local, global, structured, unstructured.
- Determine communication volume per task.
- Minimize critical communication paths.

**Phase 3: Agglomerate**
- Combine tasks to reduce overhead.
- Combine chunks for better load balance.
- Reduce communication (combine tasks that communicate heavily).

**Phase 4: Map**
- Assign tasks to processors.
- Balance load across processors.
- Minimize inter-processor communication.

**Do:**
- Iterate PCAM — each phase may require revisiting.
- Evaluate efficiency = (computation time) / (computation + communication time).
- Aim for efficiency > 0.5 (typically).

**Don't:**
- Skip the partition step — it's where independence is identified.
- Assume map is final — load imbalance may require re-mapping.

*Ref: Grokking_Concurrency.md — "Foster's methodology" (Ch. 13)*

---

### Foster's Methodology Applied: Word Count

**Apply PCAM to distributed word count:**

**Partition:**
- Task: count words in a chunk.
- Data: input text split into N chunks (one per mapper).

**Communicate:**
- Mappers emit (word, count) pairs to reducers.
- Reduce step receives all (word, count) pairs for each unique word.

**Agglomerate:**
- Combine small chunks into larger ones for better load balance.
- Use combiner (local reduce) to reduce shuffle volume.

**Map:**
- Assign chunks to mappers (one per processor).
- Shuffle (word, count) pairs to reducers by hash(word) % R.

**Result:** Scalable word count across many machines.

*Ref: Grokking_Concurrency.md — "Foster's methodology" + "Distributed word count" (Ch. 13)*

---

### Synchronization in Message Passing

**Principle:** Message passing inherently serializes sender-receiver pairs, providing implicit synchronization. But patterns still emerge.

**Patterns:**
- **Synchronous send:** Sender waits until message is received.
- **Asynchronous send:** Sender continues immediately.
- **Receive with timeout:** Wait up to N seconds for message.
- **Select/receive:** Wait for multiple message types.

**Do:**
- Use **asynchronous send** for non-blocking producers.
- Use **synchronous receive** when sender must wait.
- Apply **timeouts** to prevent indefinite blocking.
- Use **deadletter queues** for unprocessable messages.

**Don't:**
- Rely on timing assumptions — network latency varies.
- Block indefinitely — always have a timeout.

*Ref: Grokking_Concurrency.md — "Synchronization in message passing" (Ch. 11)*

---

### Conclusion: Concurrency is a Spectrum

**Principle:** Concurrency exists on a spectrum from "no concurrency" (sequential) to "full distribution" (many machines). Each level has different tools and trade-offs.

**Spectrum:**
1. **Sequential code:** Single thread, no concurrency.
2. **Coroutines/Futures:** Single-threaded async (Python asyncio).
3. **Threads:** Multiple OS threads in one process.
4. **Processes:** Multiple processes on one machine.
5. **Containers:** Isolated processes on shared host.
6. **Distributed:** Multiple machines coordinating.

**Do:**
- Match the level to the problem's needs.
- Stay as simple as possible — simplest level that meets requirements.
- Document which level each component operates at.

**Don't:**
- Default to distributed when local would do.
- Mix levels without clear boundaries.

*Ref: Grokking_Concurrency.md — "What you'll learn from this book"*

---

## Anti-Patterns & Common Mistakes

- **No synchronization on shared state:** data races / heisenbugs → *fix:* mutex, semaphore, atomic, or message-passing IPC.
- **Inconsistent lock ordering:** classic deadlock → *fix:* impose a global hierarchy.
- **Greedy locking (huge critical sections):** starves peers → *fix:* shrink the section.
- **Polite retries without coordination:** livelock → *fix:* lock hierarchy or randomized exponential backoff.
- **Thread-per-connection at scale:** C10k → *fix:* nonblocking I/O + event loop or async runtime.
- **Busy-wait polling nonblocking sockets:** CPU spin → *fix:* I/O multiplexing (`epoll`/`kqueue`).
- **Blocking call inside an async event loop:** stalls all tasks → *fix:* offload to a worker pool.
- **Assuming libraries are thread-safe:** silent corruption → *fix:* verify or wrap calls.
- **Trusting observed scheduling order:** nondeterministic → *fix:* synchronize explicitly.
- **Fine-grained everything:** communication overhead dominates → *fix:* agglomerate tasks.
- **Coarse-grained everything:** load imbalance → *fix:* decompose finer, then agglomerate as needed.
- **Locking across I/O:** blocks indefinitely on slow I/O → *fix:* acquire lock, copy data, release lock.
- **Forgetting cancel/timeout:** hangs under failure → *fix:* explicit timeouts on every async op.
- **Using `++` (or non-atomic) on shared counter:** lost updates → *fix:* atomic increment.
- **Reading-then-writing without lock:** TOCTOU race → *fix:* lock around the whole read-modify-write.
- **Unbounded message queues:** memory exhaustion → *fix:* bounded queues + backpressure.
- **Two-phase commit without handling coordinator failure:** blocked transactions → *fix:* use Raft/Paxos-based coordination.
- **Single shared lock across whole system:** kills scalability → *fix:* lock striping or finer granularity.
- **Using sleep for synchronization:** not a sync mechanism → *fix:* use events, queues, or barriers.
- **Decoupling by data (SIMD) when tasks have heavy shared state:** high coordination cost → *fix:* task decomposition instead.
- **Decoupling by task when operations are uniform on data:** leaving perf on the table → *fix:* data decomposition.
- **Producer-consumer with unbounded queue:** memory blowup on producer > consumer → *fix:* bounded queue + blocking on put.

---

## Decision Heuristics / Checklists

**Process vs. Thread?**
- Need fault isolation / multi-machine? → process
- Need shared state, low latency? → thread (or finer user-space unit)

**IPC mechanism?**
- Same machine, maximum throughput, can synchronize? → shared memory
- Producer→consumer, same machine? → pipe or message queue
- Bidirectional / network-extensible? → socket

**Synchronization primitive?**
- Single primitive-type op? → atomic
- One exclusive resource? → mutex
- Pool of N equivalent resources? → counting semaphore
- Read-heavy shared state? → readers-writer lock
- Multiple locks across tasks? → global lock ordering hierarchy
- Many concurrent locks on independent data? → lock striping

**Decomposition strategy?**
- Distinct functional stages with limited shared resources? → task decomposition / pipeline
- Same op on many data elements? → data decomposition / map
- Need aggregation after parallel split? → fork/join or map/reduce
- Embarrassingly parallel, no dependencies? → map

**Server architecture for N concurrent connections?**
- N small (< few thousand), blocking I/O OK? → thread pool
- N large (10k+), I/O-bound? → nonblocking sockets + event loop / async runtime
- Mixed CPU + I/O? → event loop + worker pool for CPU work

**Granularity checklist:**
- [ ] At least as many tasks as processors?
- [ ] Communication cost per task << task compute cost?
- [ ] Load roughly balanced across tasks?
- If not → agglomerate or decompose further.

**Concurrency model choice:**
- CPU-bound + parallelism needed? → threads or processes (with GIL workaround in Python)
- I/O-bound + 1000s of connections? → async/await or coroutines
- High-concurrency messaging? → actors (Erlang/Elixir) or goroutines (Go)
- Distributed computation? → MapReduce (Hadoop) or Spark

**Deadlock detection:**
- [ ] All four Coffman conditions met? → deadlock possible
- [ ] Global lock ordering enforced? → circular wait broken
- [ ] Lock timeouts used? → can recover from deadlock
- [ ] Tested under contention? → races surfaced

**Performance optimization order:**
1. Algorithmic improvement (O(n²) → O(n log n)).
2. Cache-friendly data structures.
3. Parallelize independent work.
4. Reduce synchronization.
5. Use specialized hardware (GPU, FPGA).

---

## Key Takeaways

1. **Concurrency ≠ parallelism.** Concurrency structures the problem; parallelism executes it. Design for concurrency; let the runtime parallelize.
2. **Latency and throughput are different axes.** Pick the one your system serves; concurrency can reduce, hide, or multiply each differently.
3. **Amdahl bounds you; Gustafson opens the door.** Sequential fractions cap speedup; growing the workload restores linear gains.
4. **Hardware matters.** Cache misses cost orders of magnitude more than most algorithmic improvements — design cache-friendly access patterns.
5. **Decompose before you code.** Draw the dependency graph; concurrency lives where edges are absent.
6. **Match pattern to problem.** Pipeline for staged transforms; map for uniform per-element ops; fork/join for split-then-aggregate; producer-consumer for decoupled buffering.
7. **Granularity is a dial, not a switch.** Fine → parallelism; coarse → low overhead. Tune empirically; agglomerate when communication dominates.
8. **Synchronization is expensive.** Prefer none (immutability, confinement, message passing); when needed, pick the smallest primitive that fits.
9. **Deadlocks need all four Coffman conditions.** Break one — usually circular wait via a global lock hierarchy.
10. **Livelocks and starvation hide behind "polite" code.** Detect with metrics; fight starvation with aging, livelock with ordering.
11. **Thread-per-connection doesn't scale.** For C10k+, switch to nonblocking I/O and event-driven or async runtimes.
12. **Good design beats clever synchronization.** Avoiding shared resources and minimizing communication is the best protection against concurrency bugs.
13. **Reactor pattern for I/O; threads for CPU.** Match the model to the workload.
14. **Async doesn't mean faster.** It means non-blocking — design correctly first.
15. **Foster's PCAM gives you a process.** Partition, Communicate, Agglomerate, Map — iterate to find the right decomposition.

---

## Cross-References
- Related: `Concurrency_in_Go.md` — Go-specific realization of these concepts (goroutines = cheap user-space units; channels = message-passing IPC; `select` = the multiplexer; `context` = cancellation/deadlines across the call-graph).
- Related: `Building_Microservices.md` — Distributed application of concurrency concepts (sagas, event-driven, eventual consistency).
- Related: `Engineering_Resilient_Systems_on_AWS.md` — Resilience patterns applied to distributed systems.
- Related: `Grokking_Concurrency.md` (this file) — Theoretical foundations.
- Topic index: `INDEX.md`

---

### Bonus: Code Patterns from the Book

The following are condensed patterns from the book that capture canonical idioms.

#### Multithreading Basic Pattern

```python
import os, time, threading
from threading import Thread

def cpu_waster(i: int) -> None:
    name = threading.current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)

def main(num_threads: int) -> None:
    for i in range(num_threads):
        Thread(target=cpu_waster, args=(i,)).start()

if __name__ == "__main__":
    main(5)
```

#### Message Queue Workers Pattern

```python
from queue import Queue
from threading import Thread, current_thread

class Worker(Thread):
    def __init__(self, queue: Queue, id: int):
        super().__init__(name=str(id))
        self.queue = queue
    def run(self) -> None:
        while not self.queue.empty():
            item = self.queue.get()           # blocks until available
            print(f"Thread {current_thread().name}: processing item {item}")

q = Queue()
for i in range(10):
    q.put(i)
threads = [Worker(q, i + 1) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()
```

#### Pipe Pattern

```python
from threading import Thread
from multiprocessing import Pipe

reader_conn, writer_conn = Pipe()
class Writer(Thread):
    def run(self): writer_conn.send("Rubber duck")
class Reader(Thread):
    def run(self): print("Received:", reader_conn.recv())

Writer().start(); Reader().start()
```

#### Pipeline Pattern (Laundry)

```python
import time
from queue import Queue
from threading import Thread

class Washer(Thread):
    def __init__(self, in_q: Queue, out_q: Queue):
        super().__init__(); self.in_q, self.out_q = in_q, out_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(4)                # wash
            self.out_q.put(load)
            self.in_q.task_done()

class Dryer(Thread):
    def __init__(self, in_q: Queue, out_q: Queue):
        super().__init__(); self.in_q, self.out_q = in_q, out_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(2)                # dry
            self.out_q.put(load)
            self.in_q.task_done()

class Folder(Thread):
    def __init__(self, in_q: Queue):
        super().__init__(); self.in_q = in_q
    def run(self):
        while True:
            load = self.in_q.get()
            time.sleep(1)                # fold
            print(f"{load} done!")
            self.in_q.task_done()

to_wash, to_dry, to_fold = Queue(), Queue(), Queue()
Washer(to_wash, to_dry).start()
Dryer(to_dry, to_fold).start()
Folder(to_fold).start()
for n in range(8): to_wash.put(f"Washload #{n}")
to_wash.join(); to_dry.join(); to_fold.join()
```

#### Fork/Join Map Pattern (Count Votes)

```python
import typing as T, random
from multiprocessing.pool import ThreadPool

Summary = T.Mapping[int, int]

def process_pile(pile):
    summary = {}
    for vote in pile:
        summary[vote] = summary.get(vote, 0) + 1
    return summary

def process_votes(pile: T.List[int], worker_count: int = 4) -> Summary:
    vpw = len(pile) // worker_count
    vote_piles = [pile[i*vpw:(i+1)*vpw] for i in range(worker_count)]
    with ThreadPool(worker_count) as pool:           # FORK
        worker_summaries = pool.map(process_pile, vote_piles)
    total = {}                                       # JOIN
    for ws in worker_summaries:
        for c, n in ws.items():
            total[c] = total.get(c, 0) + n
    return total

if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    pile = [random.randint(1, num_candidates) for _ in range(num_voters)]
    counts = process_votes(pile)
    print(f"Total number of votes: {counts}")
```

#### Race Condition (Intentionally Broken)

```python
from threading import Thread

class UnsyncedBankAccount(BankAccount):
    def __init__(self, balance: float = 0):
        super().__init__(balance)
        self.balance = balance
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("You can't deposit a negative amount of money")
    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Account does not have sufficient funds")
```

#### Synchronized Bank Account

```python
from threading import Lock

class SyncedBankAccount(UnsyncedBankAccount):
    def __init__(self, balance: float = 0):
        super().__init__(balance)
        self.mutex = Lock()
    def deposit(self, amount: float) -> None:
        self.mutex.acquire()
        try: super().deposit(amount)
        finally: self.mutex.release()
    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        try: super().withdraw(amount)
        finally: self.mutex.release()
```

#### Semaphore (Parking Garage)

```python
from threading import Thread, Semaphore, Lock

TOTAL_SPOTS = 3

class Garage:
    def __init__(self):
        self.semaphore = Semaphore(TOTAL_SPOTS)   # N permits
        self.cars_lock = Lock()
        self.parked_cars = []
    def enter(self, name):
        self.semaphore.acquire()                  # take a spot
        with self.cars_lock:
            self.parked_cars.append(name)
            print(f"{name} parked")
    def exit(self, name):
        with self.cars_lock:
            self.parked_cars.remove(name)
            print(f"{name} leaving")
        self.semaphore.release()                  # free a spot
```

#### Deadlock Hierarchy Fix

```python
from deadlock import Philosopher
from lock_with_name import LockWithName

chopstick_a = LockWithName("chopstick_a")
chopstick_b = LockWithName("chopstick_b")
# Both philosophers grab A first, then B — circular wait is impossible.
philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
philosopher_2 = Philosopher("Philosopher #2", chopstick_a, chopstick_b)
philosopher_1.start(); philosopher_2.start()
```

#### Starvation Detection

```python
from threading import Thread
from deadlock.lock_with_name import LockWithName

dumplings = 1000

class Philosopher(Thread):
    def __init__(self, name, left, right):
        super().__init__(); self.name=name; self.left=left; self.right=right
    def run(self):
        global dumplings
        eaten = 0
        while dumplings > 0:
            self.left.acquire(); self.right.acquire()
            if dumplings > 0:
                dumplings -= 1
                eaten += 1
            self.right.release(); self.left.release()
        print(f"{self.name} took {eaten} pieces")
# Output shows extreme imbalance (#1: 417, #9: 0, ...) → starvation.
```

#### Producer-Consumer (Bounded Buffer)

```python
from threading import Thread, Semaphore, Lock

SIZE = 5
BUFFER = [""] * SIZE
producer_idx = 0
mutex = Lock()
empty = Semaphore(SIZE)    # free slots
full  = Semaphore(0)       # filled slots

class Producer(Thread):
    def run(self):
        global producer_idx
        for i in range(5):
            empty.acquire(); mutex.acquire()
            BUFFER[producer_idx] = f"P-{i}"
            producer_idx = (producer_idx + 1) % SIZE
            mutex.release(); full.release()

class Consumer(Thread):
    def __init__(self):
        super().__init__(); self.idx = 0
    def run(self):
        for i in range(10):
            full.acquire(); mutex.acquire()
            item = BUFFER[self.idx]
            self.idx = (self.idx + 1) % SIZE
            mutex.release(); empty.release()
            print("consumed", item)
```

#### RWLock (Hand-rolled in Python)

```python
from threading import Lock

class RWLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()
    def acquire_read(self):
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1:           # first reader blocks writers
            self.write_lock.acquire()
        self.read_lock.release()
    def release_read(self):
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:           # last reader unblocks writers
            self.write_lock.release()
        self.read_lock.release()
    def acquire_write(self):  self.write_lock.acquire()
    def release_write(self):  self.write_lock.release()
```

#### Nonblocking Server (Pizza — busy-wait variant)

```python
from socket import socket, create_server

class Server:
    def __init__(self):
        self.server_socket = create_server(("127.0.0.1", 12345))
        self.server_socket.setblocking(False)        # nonblocking
        self.clients = set()
    def accept(self):
        try:
            conn, addr = self.server_socket.accept()
            conn.setblocking(False)
            self.clients.add(conn)
        except BlockingIOError:
            pass                                    # no pending connection
    def serve(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.send(b"response\n")
        except BlockingIOError:
            pass                                    # no data yet
    def start(self):
        while True:
            self.accept()
            for conn in self.clients.copy():
                self.serve(conn)
```

#### Event Loop with select (Pizza Reactor)

```python
import select
from socket import socket, create_server

class EventLoop:
    def __init__(self) -> None:
        self.writers = {} 
        self.readers = {} 
    def register_event(self, source: socket, event, action) -> None:
        key = source.fileno() 
        if event & select.POLLIN: 
            self.readers[key] = (source, event, action) 
        elif event & select.POLLOUT: 
            self.writers[key] = (source, event, action)
    def unregister_event(self, source: socket) -> None:
        key = source.fileno() 
        if self.readers.get(key): 
            del self.readers[key]
        if self.writers.get(key): 
            del self.writers[key]
    def run_forever(self) -> None:
        while True: 
            readers, writers, _ = select.select( 
                self.readers, self.writers, []) 
            for reader in readers: 
                source, event, action = self.readers.pop(reader) 
                action(source)
            for writer in writers: 
                source, event, action = self.writers.pop(writer)
                action, msg = action 
                action(source, msg)
```

#### Coroutine Event Loop (Fibonacci)

```python
from collections import deque
import typing as T
Coroutine = T.Generator[None, None, int]

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    def add_coroutine(self, task: Coroutine) -> None: 
        self.tasks.append(task) 
    def run_coroutine(self, task: Coroutine) -> None:
        try:
            task.send(None) 
            self.add_coroutine(task)
        except StopIteration: 
            print("Task completed")
    def run_forever(self) -> None: 
        while self.tasks: 
            print("Event loop cycle.") 
            self.run_coroutine(self.tasks.popleft()) 

def fibonacci(n: int) -> Coroutine:
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        yield 
    return a

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonacci(5)) 
    event_loop.run_forever()
```

#### Future Object

```python
from __future__ import annotations
import typing as T
from collections import deque
from random import randint
Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']

class Future:
    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None
    def set_coroutine(self, coroutine: Coroutine) -> None: 
        self.coroutine = coroutine
    def set_result(self, result: Result) -> None: 
        self.done = True
        self.result = result
    def __iter__(self) -> Future:
        return self
    def __next__(self) -> Result: 
        if not self.done: 
            raise StopIteration
        return self.result

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    def add_coroutine(self, task: Coroutine) -> None:
        self.tasks.append(task)
    def run_coroutine(self, task: T.Callable) -> None:
        future = task() 
        future.set_coroutine(task) 
        try: 
            next(future) 
            if not future.done: 
                future.set_coroutine(task) 
                self.add_coroutine(task) 
        except StopIteration: 
            return
    def run_forever(self) -> None:
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())

def cook(on_done: T.Callable[[Burger], None]) -> None: 
    burger: str = f"Burger #{randint(1, 10)}" 
    print(f"{burger} is cooked!") 
    on_done(burger) 

def cashier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None:
    print("Burger is ready for pick up!") 
    on_done(burger) 

def order_burger() -> Future:
    order = Future() 
    def on_cook_done(burger: Burger) -> None:
        cashier(burger, on_cashier_done)
    def on_cashier_done(burger: Burger) -> None:
        print(f"{burger}? That's me! Mmmmmm!")
        order.set_result(burger)
    cook(on_cook_done) 
    return order

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()
```

*All code blocks preserved from Grokking_Concurrency.md (Kirill Bobrov, Manning 2024).*