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

**Don't:**
- Use the words interchangeably; the distinction drives design decisions.

*Ref: Grokking_Concurrency.md — "Concurrency vs. parallelism" (Ch. 2)*

---

### Performance: Latency vs. Throughput

**Principle:** Concurrency improves systems in exactly three ways: (1) **reduce** latency (faster per-task), (2) **hide** latency (do other work while waiting — key for responsive systems), (3) **increase** throughput (more tasks per unit time). Optimizing one may worsen another.

**Do:**
- Pick the metric your system actually cares about (a GUI cares about latency; a batch pipeline cares about throughput).
- Use concurrency to hide I/O latency — the CPU should never idle while a task waits on disk/network.

**Don't:**
- Assume higher throughput implies lower latency — a bus has 25× the throughput of a motorcycle but a longer per-trip latency.

*Ref: Grokking_Concurrency.md — "Latency vs. throughput" (Ch. 1)*

---

### Amdahl's Law & Gustafson's Law

**Principle:** Speedup is bounded by the **sequential fraction** of a program: `Speedup = 1 / (S + (1−S)/N)`. If 33% of a program is sequential, even a million processors yield at most 3× speedup. Gustafson's counter: if you scale the *problem size* with the processor count, sequential parts matter less and speedup can grow linearly.

**Do:**
- Use Amdahl to estimate whether parallelizing is worth the engineering cost.
- Use Gustafson's framing (grow the workload) when designing distributed/batch systems.

**Don't:**
- Throw cores at a mostly-sequential program and expect linear gains.
- Forget coordination overhead — Amdahl assumes none.

*Ref: Grokking_Concurrency.md — "Amdahl's law", "Gustafson's law" (Ch. 2)*

---

### Hardware Awareness — Cache, SMP, Flynn's Taxonomy

**Principle:** Effective concurrency requires understanding the hardware. Scaled latency grows alarmingly: L1 ≈ 1 s, RAM ≈ 4 min, SSD ≈ 1.5 days, network round-trip SF→NYC ≈ 5 years (when 1 CPU cycle = 1 s).

**Do:**
- Favor cache-friendly access patterns (sequential, local) — cache misses dwarf most algorithmic gains.
- Match the architecture to the problem: SIMD/GPU for data-parallel uniform ops; MIMD/CPU for diverse logic.

**Taxonomy (Flynn):** SISD · SIMD (GPUs, vector ops) · MISD (rare) · MIMD (multicore CPUs, clusters — most common).

*Ref: Grokking_Concurrency.md — "Cache", "Multiple levels of concurrent hardware", "CPU vs. GPU" (Ch. 3)*

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

**Don't:**
- Use raw low-level threads when a library/runtime abstraction will do.

*Ref: Grokking_Concurrency.md — "Processes", "Threads" (Ch. 4)*

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
*Ref: Grokking_Concurrency.md — "Threads"*

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
*Ref: Grokking_Concurrency.md — "Message queues" (Ch. 5)*

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
*Ref: Grokking_Concurrency.md — "Pipes" (Ch. 5)*

---

### Thread Pool Pattern

**Principle:** Pre-create a fixed set of long-lived worker threads and feed them from a shared queue. Eliminates per-task thread creation cost, bounds resource usage, and isolates task failures from workers.

**Do:**
- Default to thread pools for most concurrent applications.
- Set the pool size from empirical measurement, not guesswork.

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

**Don't:**
- Rely on observed scheduling order — it's nondeterministic; synchronize explicitly when order matters.

*Ref: Grokking_Concurrency.md — "Multitasking", "Context switching" (Ch. 6)*

---

### Decomposition — Task vs. Data

**Principle:** Before writing concurrent code, build a **task dependency graph** and find independent work. Two complementary techniques: **task decomposition** (split by function) and **data decomposition** (split by data chunk). Combine them for maximum concurrency.

**Do:**
- Draw the dependency graph; concurrency is possible wherever there's no edge.
- Use task decomposition for MIMD systems; data decomposition for SIMD.
- Combine pipeline (task) + chunking (data) for compound speedups.

*Ref: Grokking_Concurrency.md — "Dependency analysis", "Task decomposition", "Data decomposition" (Ch. 7)*

---

### Pipeline Pattern (Task Decomposition)

**Principle:** Split an algorithm into ordered stages, each running concurrently and handing results to the next. Best when shared resources (a single washer/dryer) limit pure parallelism. Steady-state throughput = 1 / (slowest stage time).

**Do:**
- Use pipelines when resources are limited (filesystems, DB connections) — bound the threads per stage.
- Combine with data decomposition to parallelize within a stage.

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

### Granularity & Agglomeration

**Principle:** *Granularity* = task size/count. Fine-grained → more parallelism but more communication/scheduling overhead; coarse-grained → less overhead but risk of load imbalance. Find the sweet spot; merge tasks (*agglomeration*) to cut communication when beneficial.

**Do:**
- Aim for at least as many tasks as processors, preferably more, to give the scheduler flexibility.
- Agglomerate tiny tasks when communication cost dominates.

*Ref: Grokking_Concurrency.md — "Granularity" (Ch. 7)*

---

### Race Conditions & Critical Sections

**Principle:** A **race condition** occurs when correctness depends on the relative timing of concurrent operations. A **critical section** is code that accesses shared resources and must execute atomically. Race-condition bugs are *heisenbugs* — they disappear when you try to observe them.

**Do:**
- Treat every shared mutable resource as a critical section needing protection.
- Verify libraries are thread-safe before sharing them across tasks.
- Reproduce races by inserting strategic `sleep`s to perturb timing (debugging only, never a fix).

**Don't:**
- Assume read-modify-write sequences like `balance += amount` are atomic — they aren't.

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

**Do:**
- Keep critical sections as short as possible.
- Acquire/release locks in a consistent global order to avoid deadlocks.
- Use atomics when the operation is a primitive-type op — they don't block.

**Don't:**
- Mix synchronization styles on the same resource; pick one and apply it everywhere.

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
*Ref: Grokking_Concurrency.md — "Mutual exclusion" (Ch. 8)*

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
*Ref: Grokking_Concurrency.md — "Semaphores" (Ch. 8)*

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

**Don't:**
- Acquire the same set of locks in different orders from different tasks.

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

**Don't:**
- Add random backoff alone — can produce livelock if both tasks back off in sync.

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

### C10k Problem & Nonblocking I/O

**Principle:** Thread-per-connection servers can't scale past ~10,000 concurrent connections — context-switching overhead dominates when thread count ≫ core count. **Nonblocking I/O** + a single thread (or small pool) overlaps many I/O operations without thread overhead.

**Do:**
- For high-concurrency I/O servers, prefer nonblocking sockets + an event loop (or async/await) over thread-per-connection.
- Remember: nonblocking I/O is not *faster* per operation — it just lets the CPU do useful work while waiting.

**Don't:**
- Busy-wait in a tight loop polling nonblocking sockets — that burns a whole core. Use multiplexing (`select`/`poll`/`epoll`/`kqueue`) or async runtimes.

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

*Ref: Grokking_Concurrency.md — "Event-based concurrency", "Reactor pattern", "Event loop", "I/O multiplexing" (Ch. 11)*

---

### Asynchronous Communication & Cooperative Multitasking

**Principle:** Cooperative multitasking (async/await, coroutines, futures) lets a single thread suspend at await points and resume later — the runtime, not a preemptive timer, decides when to yield.

**Do:**
- Use async/await for I/O-bound, high-concurrency work (web servers, scrapers, gateways).
- Keep CPU-bound work in a separate thread/process — it has no natural await points.

**Don't:**
- Mix blocking calls into an async event loop — they stall every other task.

*Ref: Grokking_Concurrency.md — "Asynchronous communication", "Cooperative multitasking", "Future objects" (Ch. 12)*

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

**Decomposition strategy?**
- Distinct functional stages with limited shared resources? → task decomposition / pipeline
- Same op on many data elements? → data decomposition / map
- Need aggregation after parallel split? → fork/join or map/reduce

**Server architecture for N concurrent connections?**
- N small (< few thousand), blocking I/O OK? → thread pool
- N large (10k+), I/O-bound? → nonblocking sockets + event loop / async runtime
- Mixed CPU + I/O? → event loop + worker pool for CPU work

**Granularity checklist:**
- [ ] At least as many tasks as processors?
- [ ] Communication cost per task << task compute cost?
- [ ] Load roughly balanced across tasks?
- If not → agglomerate or decompose further.

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

---

## Cross-References
- Related: [[../Concurrency_in_Go.md]] — Go-specific realization of these concepts (goroutines = cheap user-space units; channels = message-passing IPC; `select` = the multiplexer; `context` = cancellation/deadlines across the call-graph).
- Topic index: [[../INDEX.md]]
