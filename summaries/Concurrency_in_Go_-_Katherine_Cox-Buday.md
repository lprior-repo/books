# Concurrency in Go - Katherine Cox-Buday

## Comprehensive Summary

---

## Chapter 1: An Introduction to Concurrency

**Why concurrency matters:**
- Moore's Law has shifted from faster single cores to more cores
- Clock speeds plateaued around 2005; the industry went multicore
- To utilize modern hardware, software must be concurrent

**Concurrency vs parallelism:**
- **Concurrency**: Dealing with many things at once (structure, design)
- **Parallelism**: Doing many things at once (execution)
- Concurrency enables parallelism but doesn't guarantee it

**The difficulty of concurrency:**
- **Race conditions**: Multiple threads access shared data, at least one writes, with no synchronization
- **Atomicity**: An operation appears indivisible from outside. Context determines atomicity.
- **Memory access synchronization**: Controlling access to shared memory via locks, mutexes
- **Deadlock**: All processes are blocked waiting on each other; none can proceed
- **Livelock**: Processes are active but making no progress (like people dodging in a hallway)
- **Starvation**: A process never gets CPU time or resources due to unfair scheduling

**Deadlock conditions (Coffman conditions):** All four must be present:
1. Mutual exclusion: Only one thread can hold a resource
2. Hold and wait: Thread holds one resource while waiting for another
3. No preemption: Resources cannot be forcibly taken
4. Circular wait: Circular chain of threads waiting on each other

**Why Go is good at concurrency:**
- Goroutines are lightweight (2KB stack, grows/shrinks)
- Channels provide safe communication between goroutines
- CSP (Communicating Sequential Processes) model avoids shared memory
- Runtime handles scheduling, garbage collection cooperatively
- Race detector built into the toolchain

---

## Chapter 2: Communicating Sequential Processes (CSP)

**CSP origins:** Tony Hoare's 1978 paper. Core idea: programs are compositions of processes that communicate through channels. No shared memory—communication IS synchronization.

**Go's philosophy on concurrency:**
- "Don't communicate by sharing memory; share memory by communicating"
- Channels are first-class citizens
- Goroutines are cheap (create thousands freely)
- The select statement multiplexes channel operations
- Go's concurrency decision tree:
  1. Is this problem naturally concurrent? → Use goroutines
  2. Do goroutines need to communicate? → Use channels
  3. Do you need shared state? → Use sync primitives (mutexes) as last resort

**Go's approach vs other languages:**
- Java: Shared memory with locks/synchronized blocks
- Erlang: Actor model with message passing (each actor has a mailbox)
- Go: CSP with channels (communication is synchronous by default)

---

## Chapter 3: Go's Concurrency Building Blocks

### Goroutines

**What goroutines are:**
- Functions or methods that run concurrently with other functions
- Not OS threads—they're managed by the Go runtime (M:N scheduling)
- Start with ~2KB stack that grows and shrinks as needed
- Created with the `go` keyword

**Goroutine lifecycle:**
- Created → Running → Blocked (waiting on channel/I/O) → Finished
- Goroutines are not garbage collected—they must terminate on their own
- If the main goroutine exits, all goroutines are terminated

### Channels

**Channel types:**
- **Unbuffered**: `make(chan int)` — synchronous; sender blocks until receiver is ready
- **Buffered**: `make(chan int, 5)` — asynchronous up to buffer size; sender only blocks when buffer is full

**Channel directions:**
- `chan int` — bidirectional
- `chan<- int` — send-only
- `<-chan int` — receive-only
- Go implicitly converts bidirectional to unidirectional

**Channel operations:**
- Send: `ch <- value`
- Receive: `value := <-ch`
- Close: `close(ch)` — indicates no more values will be sent
- Reading from closed channel returns zero value immediately

**Channel semantics:**
- Reading from a nil channel blocks forever
- Writing to a nil channel blocks forever
- Closing a nil channel panics
- Reading from a closed channel returns zero value
- Writing to a closed channel panics

### The select Statement

`select` waits on multiple channel operations simultaneously:
```go
select {
case v := <-ch1:
    fmt.Println("received from ch1:", v)
case v := <-ch2:
    fmt.Println("received from ch2:", v)
case ch3 <- 42:
    fmt.Println("sent to ch3")
default:
    fmt.Println("no channel ready")
}
```

- When multiple cases are ready, one is chosen randomly
- `default` makes select non-blocking
- Empty select `select{}` blocks forever

### The sync Package

**WaitGroup**: Wait for a collection of goroutines to finish:
```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    // do work
}()
wg.Wait()
```

**Mutex and RWMutex**: Protect shared memory:
- `sync.Mutex`: Exclusive lock
- `sync.RWMutex`: Multiple readers OR single writer
- Always unlock with `defer m.Unlock()`

**Cond**: Condition variable for signaling between goroutines
- `Signal()`: Wake one waiter
- `Broadcast()`: Wake all waiters

**Once**: Ensure a function runs exactly once:
```go
var once sync.Once
once.Do(func() { /* initialization */ })
```

**Pool**: Object pool for reuse (reduces GC pressure):
```go
pool := sync.Pool{
    New: func() interface{} { return new(MyObject) },
}
obj := pool.Get().(*MyObject)
pool.Put(obj)
```

### GOMAXPROCS

Controls the number of OS threads available to goroutines. Default is number of CPU cores. Can be tuned for specific workloads.

---

## Chapter 4: Concurrency Patterns in Go

### Confinement
Restricting data access to a single goroutine eliminates the need for synchronization:
- **Ad hoc confinement**: By convention (fragile, not enforced)
- **Lexical confinement**: By code structure (enforced by compiler)

### The for-select Loop Pattern
```go
for {
    select {
    case <-done:
        return
    case v := <-ch:
        process(v)
    }
}
```

### Preventing Goroutine Leaks
Goroutines that never terminate cause memory leaks. Always provide an exit path:
```go
go func() {
    defer close(resultCh)
    for {
        select {
        case <-done:
            return  // exit when done signal received
        case resultCh <- doWork():
        }
    }
}()
```

### The or-channel
Combine multiple done channels into one that closes when any input closes:
```go
func or(channels ...<-chan interface{}) <-chan interface{} {
    // Returns a channel that closes when ANY input channel closes
}
```

### Pipelines
A pipeline is a series of stages where each stage is a goroutine:
- Stages receive work from upstream via a channel
- Stages send results downstream via a channel
- Each stage can be independently scaled

```go
// Stage 1: generate numbers
generator := func(done <-chan interface{}, integers ...int) <-chan int {
    stream := make(chan int)
    go func() {
        defer close(stream)
        for _, i := range integers {
            select {
            case <-done: return
            case stream <- i:
            }
        }
    }()
    return stream
}

// Stage 2: square numbers
square := func(done <-chan interface{}, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for v := range in {
            select {
            case <-done: return
            case out <- v * v:
            }
        }
    }()
    return out
}
```

### Fan-Out, Fan-In
- **Fan-out**: Start multiple goroutines reading from the same channel (parallelism)
- **Fan-in**: Merge multiple channels into one

### The tee-channel
Duplicate values from one channel to two channels:
```go
tee := func(done <-chan interface{}, in <-chan interface{}) (_, _ <-chan interface{}) {
    out1, out2 := make(chan interface{}), make(chan interface{})
    // forwards each value to both outputs
    return out1, out2
}
```

### The or-done-channel
Wrap a channel to handle cancellation transparently:
```go
orDone := func(done, c <-chan interface{}) <-chan interface{} {
    valStream := make(chan interface{})
    go func() {
        defer close(valStream)
        for {
            select {
            case <-done: return
            case v, ok := <-c:
                if !ok { return }
                select {
                case <-done: return
                case valStream <- v:
                }
            }
        }
    }()
    return valStream
}
```

---

## Chapter 5: Concurrency at Scale

### Error propagation
- Errors should be propagated through channels like any other value
- Create a `Result` type that can hold either a value or an error
- Errors from goroutines should be collected and aggregated

### Heartbeats
Goroutines periodically signal they're alive:
- **Interval-based**: Send a heartbeat every N seconds
- **Work-based**: Send a heartbeat before each unit of work
- Use heartbeats for health monitoring and deterministic testing

### Replicated requests
Send the same request to multiple goroutines and use the first response:
```go
func replicatedRequest(done <-chan interface{}, fn func() interface{}) interface{} {
    ch := make(chan interface{})
    for i := 0; i < numReplicas; i++ {
        go func() {
            select {
            case <-done: return
            case ch <- fn():
            }
        }()
    }
    return <-ch
}
```

### Rate limiting
Control the rate of operations:
- Use a ticker to pace operations
- Token bucket algorithm: refill tokens at a fixed rate
- Use `time.Tick` or `time.NewTicker`

### Timeout and cancellation
- **Timeouts**: Use `context.WithTimeout` or `select` with `time.After`
- **Cancellation**: Use `context.WithCancel` to signal goroutines to stop
- Cancellation propagation: parent cancels → all children should detect and terminate
- Handle shared state carefully during cancellation (don't leave partially modified state)

---

## Chapter 6: Goroutines and the Go Runtime

### Go's work-stealing scheduler
- M:N scheduling: M goroutines on N OS threads
- Each OS thread has a local run queue of goroutines
- When a thread's queue is empty, it steals from other threads
- Work stealing improves load balancing and cache locality

### Goroutine scheduling:
- Cooperative scheduling with preemption points
- Goroutines yield at channel operations, function calls, and allocation points
- Since Go 1.14: asynchronous preemption (goroutines can be preempted at any safe point)

### Work stealing strategy:
- Thread runs goroutines from its local queue
- If queue is empty, steal half from another thread's queue
- If all queues empty, check global run queue
- If still nothing, poll network (for I/O-bound work)

### Stealing tasks vs continuations:
- **Task stealing**: Steal entire goroutines
- **Continuation stealing**: Steal the continuation (what happens after a yield point)
- Go uses continuation stealing for better locality

---

## Appendix: Tools

**Race detector**: `go test -race` or `go build -race`
- Detects data races at runtime
- Adds instrumentation that tracks memory access patterns
- Not a guarantee (only catches races that actually occur during the test run)

**pprof**: CPU and memory profiling
```bash
go tool pprof cpu.prof
go tool pprof mem.prof
```

**Goroutine dumps**: `runtime.NumGoroutine()` and `pprof.Lookup("goroutine")`

---

## Key Takeaways

1. **Think in CSP, not threads**: Model concurrent programs as processes communicating through channels, not as threads sharing memory.

2. **Goroutines are cheap; use them freely**: The Go runtime efficiently schedules thousands of goroutines. Don't pool goroutines—create them as needed.

3. **Channels are the primary communication mechanism**: Prefer channels over shared memory with locks. They combine communication and synchronization.

4. **Always prevent goroutine leaks**: Every goroutine must have a clear termination path. Use done channels or contexts.

5. **The select statement is the multiplexer**: It enables waiting on multiple channel operations and is essential for cancellation patterns.

6. **Pipelines compose concurrent stages**: Build processing pipelines where each stage is a goroutine reading from one channel and writing to another.

7. **Fan-out for parallelism, fan-in for aggregation**: Scale individual pipeline stages by running multiple instances (fan-out) and merging results (fan-in).

8. **Use the race detector in all tests**: `go test -race` catches data races that are nearly impossible to find through code review.

9. **Confinement eliminates synchronization**: When data is only accessed by one goroutine, no locks are needed. Prefer lexical confinement.

10. **The Go runtime handles the hard parts**: Work-stealing scheduling, cooperative preemption, and efficient goroutine management mean you focus on the problem, not the scheduling.
