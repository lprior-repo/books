# Concurrency in Go
**Author:** Katherine Cox-Buday
**Topic tags:** `#concurrency` `#go` `#testing`
**Language focus:** Go-first
**Sources:** `markdown_output/Concurrency_in_Go_-_Katherine_Cox-Buday/Concurrency_in_Go_-_Katherine_Cox-Buday.md` · `summaries/Concurrency_in_Go_-_Katherine_Cox-Buday.md`

## TL;DR
The definitive guide to Go's concurrency story. CSP is the philosophical backbone (goroutines + channels + `select`); the `sync` package supplies lower-level primitives; patterns compose them into pipelines, fan-out/fan-in, or/tee/bridge/or-done, heartbeats, replicated requests, rate limiting, and healing stewards; the `context` package standardizes cancellation and request-scoped data. Every goroutine must have a termination path, channels have owners, errors flow as values, and logical correctness — never `time.Sleep` — is the goal.

---

## Best Practices by Topic

### 1. Distinguish Concurrency from Parallelism

**Principle:** Concurrency is a property of code (how you structure the problem); parallelism is a property of the running program (whether multiple tasks execute simultaneously).

**Do:**
- Model each naturally independent unit of work as a separate goroutine.
- Use CSP abstractions (goroutines, channels, `select`) as the default; reach for memory access primitives only when they are simpler.
- Treat goroutines as a free resource — don't pool them up front.
- Keep parallelism concerns in the runtime; don't reinvent them with thread pools.

**Don't:**
- Don't conflate concurrency with parallelism.
- Don't port OS-thread patterns (fine-grained lock lattices, hand-rolled thread pools) into Go.
- Don't assume "share memory by communicating" forbids `sync.Mutex` — it does not, when the mutex stays inside a type.

*Ref: Concurrency_in_Go.md — "The Difference Between Concurrency and Parallelism"*

---

### 2. Use Go's Decision Tree to Pick Channels or Mutexes

**Principle:** Pick the simplest primitive that matches the scope of concurrency.

**Do:**
- Transferring ownership of data → use a channel.
- Guarding internal state of a small struct → use a `sync.Mutex` or `sync.RWMutex` kept private to that type.
- Coordinating multiple pieces of logic → use channels + `select` for composability.
- Performance-critical section proven by profiling → use mutex (channels *use* mutexes internally).

**Don't:**
- Don't expose `*Mutex` fields past a type boundary.
- Don't introduce channels for single-field internal state.
- Don't pick channels just to avoid writing `Lock`/`Unlock`; the `select` overhead can be larger.

*Ref: Concurrency_in_Go.md — "Go's Philosophy on Concurrency"*

---

### 3. Recognize and Treat the Common Concurrency Bugs

**Principle:** There are four canonical failure modes; treat them as distinct problems.

**Do:**
- Track race conditions by enumerating all interleavings ("imagine an hour between operations").
- Bound critical sections to what truly must be atomic.
- Keep the Coffman conditions in mind for deadlock prevention.
- Use metrics + heartbeats to detect starvation and goroutine ill-health.
- Use timeouts on operations in large systems to guarantee the system can't deadlock forever.

**Don't:**
- Don't use `panic` to signal business-rule errors.
- Don't sprinkle `time.Sleep` to "fix" races; it only raises the probability of correctness, never reaches it.
- Don't expose locks beyond the type that owns the data.
- Don't hold a lock far longer than the critical section.
- Don't attempt to retry indefinitely to "fix" a deadlock — you may turn it into a livelock.

**Code:**
```go
// BAD: data race. Three outcomes are possible (nothing, "0", or "1").
var data int
go func() { data++ }()
if data == 0 {
    fmt.Printf("the value is %v.\n", data)
}

// BAD: sleep does NOT fix the race — all three outcomes still possible.
var data int
go func() { data++ }()
time.Sleep(1 * time.Second) // This is bad!
if data == 0 {
    fmt.Printf("the value is %v.\n", data)
}
```

*Ref: Concurrency_in_Go.md — "Race Conditions"*

---

### 4. Make Race Conditions Impossible by Construction

**Principle:** Hide synchronization behind a type so callers cannot forget to lock.

**Do:**
- Hide `sync.Mutex` in a struct's API; expose only the methods that lock internally.
- Use `defer c.mu.Unlock()` so unlocks always happen, even on panic.
- Keep critical sections as small as the atomicity contract requires.
- Run `go test -race` and `go build -race` in CI.

**Don't:**
- Don't make callers reason about the lock.
- Don't unlock outside `defer` from a method that might panic.
- Don't conflate unrelated state under one lock.

**Code:**
```go
// Hiding locking behind a type's API so callers never see the lock.
type Counter struct {
    mu    sync.Mutex
    value int
}
func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}
```

*Ref: Concurrency_in_Go.md — "Memory Access Synchronization"*

---

### 5. Prevent Deadlock with the Coffman Conditions

**Principle:** All four Coffman conditions must hold for a deadlock: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one.

**Do:**
- Order lock acquisition globally (resource hierarchy) to break circular wait.
- Use timeouts on operations in large systems.
- Detect starvation with metrics — log when work is accomplished and compare against expected rate.

**Don't:**
- Don't acquire locks in different orders from different goroutines.
- Don't hold a lock far longer than the critical section.
- Don't try to prevent deadlocks with uncoordinated retries.

**Code:**
```go
// Classic deadlock: printSum locks a then b; the other locks b then a.
type value struct {
    mu    sync.Mutex
    value int
}
printSum := func(v1, v2 *value) {
    defer wg.Done()
    v1.mu.Lock()
    defer v1.mu.Unlock()
    time.Sleep(2 * time.Second)
    v2.mu.Lock()
    defer v2.mu.Unlock()
    fmt.Printf("sum=%v\n", v1.value+v2.value)
}
var a, b value
wg.Add(2)
go printSum(&a, &b)
go printSum(&b, &a)
wg.Wait()
// fatal error: all goroutines are asleep - deadlock!
```

*Ref: Concurrency_in_Go.md — "Deadlock"*

---

### 6. Model Starvation and Tune Fairness Deliberately

**Principle:** A greedy worker can do 2x the work of a polite one with the same critical section — measure to find it.

**Do:**
- Record and sample metrics: log when work is accomplished and compare against expected rate.
- Prefer fine-grained locking first; broaden the lock only after profiling proves a need.
- Use starv­ation-detection metrics when concurrency is high.

**Don't:**
- Don't accept greedy locks that "feel fast" without measuring.
- Don't broaden the lock scope to "save" lock calls without proof.

**Code:**
```go
// Starvation: the greedy worker (one big lock) does ~2x the work of the polite
// worker (three smaller locks for the same total sleep).
greedyWorker := func() {
    defer wg.Done()
    var count int
    for begin := time.Now(); time.Since(begin) <= runtime; {
        sharedLock.Lock()
        time.Sleep(3 * time.Nanosecond)
        sharedLock.Unlock()
        count++
    }
    fmt.Printf("Greedy worker was able to execute %v work loops\n", count)
}
```

*Ref: Concurrency_in_Go.md — "Starvation"*

---

### 7. Make Concurrency Safety Obvious from the Signature

**Principle:** Document who is responsible for the goroutine, the channels, and the synchronization.

**Do:**
- Comment concurrent APIs with: (1) who owns the goroutine, (2) how the problem maps to primitives, (3) who synchronizes.
- Prefer side-effect-free signatures so callers don't worry about shared state.
- Return `<-chan T` to signal the function spins up its own goroutine.

**Don't:**
- Don't expose a `*Pi` pointer and leave callers guessing about synchronization.
- Don't write a function that performs work in a goroutine and returns without signaling the goroutine.

**Code:**
```go
// Bad: forces the caller to reason about concurrency & synchronization.
func CalculatePi(begin, end int64, pi *Pi)

// Good: no side effects, no shared state.
func CalculatePi(begin, end int64) []uint

// Better: channel signals goroutine ownership to the caller.
func CalculatePi(begin, end int64) <-chan uint
```

*Ref: Concurrency_in_Go.md — "Determining Concurrency Safety"*

---

### 8. Treat Goroutines as Functions with a Termination Path

**Principle:** Goroutines are not garbage collected; every goroutine must end.

**Do:**
- Always establish a join point (`WaitGroup` or channel receive).
- Pass loop variables explicitly into goroutines to avoid the closure-capture bug.
- Treat goroutines as a free resource, but always set up termination before they leak.

**Don't:**
- Don't `go func() { ... }()` without a join.
- Don't capture loop variables by reference in a goroutine that outlives the loop.
- Don't write main-without-`Wait()`; the process can exit before goroutines run.

**Code:**
```go
var wg sync.WaitGroup
sayHello := func() {
    defer wg.Done()
    fmt.Println("hello")
}
wg.Add(1)
go sayHello()
wg.Wait()
```

```go
// Correct: pass the loop variable into the goroutine explicitly.
var wg sync.WaitGroup
for _, salutation := range []string{"hello", "greetings", "good day"} {
    wg.Add(1)
    go func(salutation string) {
        defer wg.Done()
        fmt.Println(salutation)
    }(salutation)
}
wg.Wait()
```

```text
good day
hello
greetings
```

*Ref: Concurrency_in_Go.md — "Goroutines"*

---

### 9. Verify Goroutine Cost with the MemStats Trick

**Principle:** A few kilobytes per goroutine, but unobserved goroutines still cost resources.

**Do:**
- Use `runtime.MemStats` before and after to measure approximate goroutine cost.
- Always keep the `noop` running so the goroutine never exits and the measurement is accurate.
- Treat goroutine size as a known quantity during capacity planning.

**Don't:**
- Don't assert that goroutines are "free" without measuring.
- Don't pool goroutines preemptively.

**Code:**
```go
memConsumed := func() uint64 {
    runtime.GC()
    var s runtime.MemStats
    runtime.ReadMemStats(&s)
    return s.Sys
}
var c <-chan interface{}
var wg sync.WaitGroup
noop := func() { wg.Done(); <-c }
const numGoroutines = 1e4
wg.Add(numGoroutines)
before := memConsumed()
for i := numGoroutines; i > 0; i-- {
    go noop()
}
wg.Wait()
after := memConsumed()
fmt.Printf("%.3fkb", float64(after-before)/numGoroutines/1000)
```

*Ref: Concurrency_in_Go.md — "Goroutines"*

---

### 10. Use the `sync` Primitives at the Right Scope

**Principle:** `WaitGroup`, `Mutex`, `RWMutex`, `Cond`, `Once`, and `Pool` each solve one problem.

**Do:**
- `WaitGroup` for "don't care about the result, just join."
- `Mutex` for internal state with no other access patterns.
- `RWMutex` only after profiling shows a benefit.
- `Cond` for rendezvous points, but prefer channels when the scope is broad.
- `Once` for initialization that must run exactly once.
- `Pool` for expensive objects with similar shape.

**Don't:**
- Don't reach for `RWMutex` "just in case" — the extra complexity has overhead.
- Don't lock beyond the type that owns the data.
- Don't `Add` to a `WaitGroup` from inside the goroutine being tracked (race!).
- Don't `Unlock` outside `defer` from a method that might panic.
- Don't use `Cond` when a `chan struct{}` would be simpler.

**Code:**
```go
hello := func(wg *sync.WaitGroup, id int) {
    defer wg.Done()
    fmt.Printf("Hello from %v!\n", id)
}
const numGreeters = 5
var wg sync.WaitGroup
wg.Add(numGreeters)
for i := 0; i < numGreeters; i++ {
    go hello(&wg, i+1)
}
wg.Wait()
```

```text
Hello from 5!
Hello from 4!
Hello from 3!
Hello from 2!
Hello from 1!
```

```go
// Always call Unlock within a defer statement.
decrement := func() {
    lock.Lock()
    defer lock.Unlock()
    count--
    fmt.Printf("Decrementing: %d\n", count)
}
```

*Ref: Concurrency_in_Go.md — "The sync Package"*

---

### 11. Use `Cond` for Wait/Signal Rendezvous

**Principle:** `Cond` is the right primitive when goroutines rendezvous on a single event with the same Locker.

**Do:**
- Use `c.Wait()` to suspend until another goroutine signals.
- Recheck the predicate after `Wait()` returns — the signal only means "something changed."
- `Broadcast` for any-state changes; `Signal` for FIFO wake of one waiter.
- `Broadcast` for "click" events with arbitrary handler count.

**Don't:**
- Don't use `Cond` where a channel-based `chan struct{}` would be clearer.
- Don't expose `Cond` past a small scope; wrap it in a type.

**Code:**
```go
type Button struct {
    Clicked *sync.Cond
}
button := Button{ Clicked: sync.NewCond(&sync.Mutex{}) }
subscribe := func(c *sync.Cond, fn func()) {
    var goroutineRunning sync.WaitGroup
    goroutineRunning.Add(1)
    go func() {
        goroutineRunning.Done()
        c.L.Lock()
        defer c.L.Unlock()
        c.Wait()
        fn()
    }()
    goroutineRunning.Wait()
}
var clickRegistered sync.WaitGroup
clickRegistered.Add(3)
subscribe(button.Clicked, func() {
    fmt.Println("Maximizing window.")
    clickRegistered.Done()
})
subscribe(button.Clicked, func() {
    fmt.Println("Displaying annoying dialog box!")
    clickRegistered.Done()
})
subscribe(button.Clicked, func() {
    fmt.Println("Mouse clicked.")
    clickRegistered.Done()
})
button.Clicked.Broadcast()
clickRegistered.Wait()
```

```text
Mouse clicked. Maximizing window. Displaying annoying dialog box!
```

*Ref: Concurrency_in_Go.md — "Cond"*

---

### 12. Use `sync.Once` for One-Shot Initialization

**Principle:** `Once` counts calls, not unique functions passed in.

**Do:**
- Wrap the call and the `Once` in a small lexical block to keep their coupling obvious.
- Detect `Once.Do` circular deadlocks by audit.

**Don't:**
- Don't pass different functions to the same `Once` and expect each to run once.
- Don't construct cycles where `onceA.Do` calls into `onceB.Do` and vice versa.

**Code:**
```go
var count int
increment := func() {
    count++
}
var once sync.Once
var increments sync.WaitGroup
increments.Add(100)
for i := 0; i < 100; i++ {
    go func() {
        defer increments.Done()
        once.Do(increment)
    }()
}
increments.Wait()
fmt.Printf("Count is %d\n", count)
```

```text
Count is 1
```

```go
// This call can't proceed until the call at returns.
var onceA, onceB sync.Once
var initB func()
initA := func() { onceB.Do(initB) }
initB = func() { onceA.Do(initA) }
onceA.Do(initA)
```

*Ref: Concurrency_in_Go.md — "Once"*

---

### 13. Use `sync.Pool` for Expensive, Homogeneous Objects

**Principle:** `Pool` shines for things that are expensive to create and have a uniform shape.

**Do:**
- Make `New` thread-safe.
- Don't assume anything about the state of an object returned from `Get`.
- `Put` the object back (usually in `defer`).
- Use `Pool` for chunking to reduce allocations.

**Don't:**
- Don't store heterogeneous objects in a single `Pool` (type-conversion cost will exceed the savings).
- Don't hold onto a single `Pool`'s instances forever.
- Don't depend on the identity of an object after `Get` — it may have been mutated by other consumers.

**Code:**
```go
myPool := &sync.Pool{
    New: func() interface{} {
        fmt.Println("Creating new instance.")
        return struct{}{}
    },
}
myPool.Get()
instance := myPool.Get()
myPool.Put(instance)
myPool.Get()
```

```text
Creating new instance.
Creating new instance.
```

*Ref: Concurrency_in_Go.md — "Pool"*

---

### 14. Treat Channels as First-Class Coordination Primitives

**Principle:** Channels are conduits for streams of values; ownership rules prevent nil, closed, and full/empty panics.

**Do:**
- Declare channels with the right direction (`chan T`, `chan<- T`, `<-chan T`).
- Use a buffered channel only when you know the upper bound.
- Close a channel from the goroutine that wrote to it — never the reader.
- Use `<-T` to signal "value not present" for absent values.
- Range over channels; the loop terminates on close.

**Don't:**
- Don't close a never-closed channel; the signal can only be sent once.
- Don't write to a closed channel; it panics.
- Don't read or write to a nil channel; it blocks forever.
- Don't close a channel to indicate "end of stream" if the receiver may still need to send.

**Code:**
```go
// Read from a closed stream returns the zero value.
intStream := make(chan int)
close(intStream)
integer, ok := <- intStream
fmt.Printf("(%v): %v", ok, integer)
```

```text
(false): 0
```

*Ref: Concurrency_in_Go.md — "Channels"*

---

### 15. Know the Channel-Operation Reference Chart

**Principle:** Memorize what each operation does on each channel state.

**Do:**
- Treat nil as "blocked" for reads and writes, "panic" for close.
- Treat closed as "panic" for writes, "zero value + false" for reads.
- Treat open-empty vs. open-not-empty as the gate for read/write blocking.

**Don't:**
- Don't write to a closed channel.
- Don't close a nil channel.
- Don't close a channel twice.

**Code:**
```text
| Operation | Channel state         | Result                                                                                         |
|-----------|-----------------------|------------------------------------------------------------------------------------------------|
| Read      | nil                   | Block                                                                                          |
|           | Open and Not Empty    | Value                                                                                          |
|           | Open and Empty        | Block                                                                                          |
|           | Closed                | default value, false                                                                           |
|           | Write Only            | Compilation Error                                                                             |
| Write     | nil                   | Block                                                                                          |
|           | Open and Full         | Block                                                                                          |
|           | Open and Not Full     | Write Value                                                                                    |
|           | Closed                | panic                                                                                          |
|           | Receive Only          | Compilation Error                                                                             |
| close     | nil                   | panic                                                                                          |
|           | Open and Not Empty    | Closes Channel; reads succeed until channel is drained, then reads produce default value        |
|           | Open and Empty        | Closes Channel; reads produces default value                                                   |
|           | Closed                | panic                                                                                          |
|           | Receive Only          | Compilation Error                                                                             |
```

*Ref: Concurrency_in_Go.md — "Channels"*

---

### 16. Assign Channel Ownership Explicitly

**Principle:** Ownership = a single goroutine that instantiates, writes, and closes. Use unidirectional channel types to make the contract compile-time checked.

**Do:**
- Have the owner goroutine instantiate, write, and close the channel.
- Expose only `<-chan T` to consumers.
- Encapsulate the lifecycle in a constructor-like function.

**Don't:**
- Don't write to a channel from a consumer.
- Don't close a channel from outside the owner.
- Don't reuse a channel after closing it.

**Code:**
```go
chanOwner := func() <-chan int {
    resultStream := make(chan int, 5)
    go func() {
        defer close(resultStream)
        for i := 0; i <= 5; i++ {
            resultStream <- i
        }
    }()
    return resultStream
}
resultStream := chanOwner()
for result := range resultStream {
    fmt.Printf("Received: %d\n", result)
}
fmt.Println("Done receiving!")
```

```text
Received: 0
Received: 1
Received: 2
Received: 3
Received: 4
Received: 5
Done receiving!
```

*Ref: Concurrency_in_Go.md — "Channels"*

---

### 17. Compose Channels with the `select` Statement

**Principle:** `select` is the glue between channels — multiplex reads, multiplex writes, handle timeouts, and drive cancellation.

**Do:**
- Use `select` to wait on multiple channel operations at once.
- Add a `default` case when you need non-blocking polls.
- Use `time.After(d)` for a one-shot timeout.
- Use `time.Tick(d)` for periodic timeouts (mind the leak: `defer ticker.Stop()`).
- Use `close(done)` to fan-out a cancellation signal to many goroutines.

**Don't:**
- Don't use a single `select` to do both pulse sending and result sending when you don't want a lost result.
- Don't write `time.After` inside a loop without keeping a reference — every call creates a new timer.
- Don't rely on `time.After` for huge timeouts that block GC of the underlying channel.

**Code:**
```go
start := time.Now()
c := make(chan interface{})
go func() {
    time.Sleep(5*time.Second)
    close(c)
}()
fmt.Println("Blocking on read...")
select {
case <-c:
    fmt.Printf("Unblocked %v later.\n", time.Since(start))
}
```

```text
Blocking on read...
Unblocked 5.000170047s later.
```

*Ref: Concurrency_in_Go.md — "The select Statement"*

---

### 18. Use `select` for Fair Multiplexed Reads

**Principle:** Go selects among ready cases pseudo-randomly — use this to avoid starvation between equal-priority channels.

**Do:**
- Trust the random selection when cases are equally valid.
- Re-measure if you suspect one case is unfairly favored.

**Don't:**
- Don't try to bias `select` for fairness — it's pseudo-random by design.

**Code:**
```go
c1 := make(chan interface{}); close(c1)
c2 := make(chan interface{}); close(c2)
var c1Count, c2Count int
for i := 1000; i >= 0; i-- {
    select {
    case <-c1:
        c1Count++
    case <-c2:
        c2Count++
    }
}
fmt.Printf("c1Count: %d\nc2Count: %d\n", c1Count, c2Count)
```

```text
c1Count: 505 c2Count: 496
```

*Ref: Concurrency_in_Go.md — "The select Statement"*

---

### 19. Use Confinement (Ad-Hoc and Lexical) When Possible

**Principle:** Confinement eliminates races by guaranteeing only one goroutine touches the data — no synchronization needed.

**Do:**
- Document ad-hoc confinement with code review (it cannot be enforced by the compiler).
- Use lexical confinement whenever the data structure is mutable.
- Expose only the part of the data each consumer needs.

**Don't:**
- Don't rely on ad-hoc confinement across a large codebase without tooling.
- Don't use ad-hoc confinement when the compiler can enforce it.

**Code:**
```go
data := make([]int, 4)
loopData := func(handleData chan<- int) {
    defer close(handleData)
    for i := range data {
        handleData <- data[i]
    }
}
handleData := make(chan int)
go loopData(handleData)
for num := range handleData {
    fmt.Println(num)
}
```

```go
// Lexical confinement: each goroutine gets a sub-slice of the original.
printData := func(wg *sync.WaitGroup, data []byte) {
    defer wg.Done()
    var buff bytes.Buffer
    for _, b := range data {
        fmt.Fprintf(&buff, "%c", b)
    }
    fmt.Println(buff.String())
}
var wg sync.WaitGroup
wg.Add(2)
data := []byte("golang")
go printData(&wg, data[:3])
go printData(&wg, data[3:])
wg.Wait()
```

*Ref: Concurrency_in_Go.md — "Confinement"*

---

### 20. Use `for-select` for Goroutine Loops

**Principle:** `for-select` is the canonical loop structure for long-lived goroutines.

**Do:**
- Use `for { select { case <-done: return ... } }` for infinite loops.
- Prefer the shorter form (do work after the `select`) when the work is preemptable.
- Embed work in `default` only when the work is small and non-preemptable.

**Don't:**
- Don't write `for {}` without a `select` — it's hard to tell where cancellation lives.
- Don't make goroutines loop forever without a termination path.

**Code:**
```go
// Short form: keep select small, do work after.
for {
    select {
    case <-done:
        return
    default:
    }
    // Do non-preemptable work
}

// Embedded form: small work lives in default.
for {
    select {
    case <-done:
        return
    default:
        // Do non-preemptable work
    }
}
```

*Ref: Concurrency_in_Go.md — "The for-select Loop"*

---

### 21. Prevent Goroutine Leaks with a `done` Channel

**Principle:** If a goroutine has a long lifetime and can be preempted, every blocking operation must select on `done`.

**Do:**
- Make `done` the first parameter of any long-running function.
- Close `done` from the parent to signal cancellation.
- Make sure producers select on `done` too, not just consumers.

**Don't:**
- Don't forget `done` on the write side of a channel — a goroutine blocked on `<-ch` may never see a cancellation.
- Don't leak goroutines in tests — they will outlive the test process.
- Don't use unbuffered channels with no receiver — writes block forever.

**Code:**
```go
doWork := func(
    done <-chan interface{},
    strings <-chan string,
) <-chan interface{} {
    terminated := make(chan interface{})
    go func() {
        defer fmt.Println("doWork exited.")
        defer close(terminated)
        for {
            select {
            case s := <-strings:
                // Do something interesting
                fmt.Println(s)
            case <-done:
                return
            }
        }
    }()
    return terminated
}
done := make(chan interface{})
terminated := doWork(done, nil)
go func() {
    // Cancel the operation after 1 second.
    time.Sleep(1 * time.Second)
    fmt.Println("Canceling doWork goroutine...")
    close(done)
}()
<-terminated
fmt.Println("Done.")
```

```text
Canceling doWork goroutine...
doWork exited.
Done.
```

*Ref: Concurrency_in_Go.md — "Preventing Goroutine Leaks"*

---

### 22. Use the `or-channel` to Combine Many Done Channels

**Principle:** `or` returns a single done channel that closes when *any* of its inputs closes.

**Do:**
- Use the recursive `or` pattern when the count of done channels is dynamic.
- Pass the `orDone` channel back through the recursion so each child can exit.
- Document that `or(nil)` returns `nil` (blocks forever).

**Don't:**
- Don't allocate one goroutine per done channel when a recursive binary merge will do.
- Don't use `or` when you know the count up-front and a single `select` works.

**Code:**
```go
var or func(channels ...<-chan interface{}) <-chan interface{}
or = func(channels ...<-chan interface{}) <-chan interface{} {
    switch len(channels) {
    case 0:
        return nil
    case 1:
        return channels[0]
    }
    orDone := make(chan interface{})
    go func() {
        defer close(orDone)
        switch len(channels) {
        case 2:
            select {
            case <-channels[0]:
            case <-channels[1]:
            }
        default:
            select {
            case <-channels[0]:
            case <-channels[1]:
            case <-channels[2]:
            case <-or(append(channels[3:], orDone)...):
            }
        }
    }()
    return orDone
}
```

*Ref: Concurrency_in_Go.md — "The or-channel"*

---

### 23. Return Errors as Values from Goroutines

**Principle:** Don't make a goroutine decide what to do with an error — let the parent with full context decide.

**Do:**
- Define a `Result` struct that pairs a value with an error.
- Send results on a `chan Result` and let the consumer inspect.
- Use a goroutine's *outputs* for success, its *errors* for failure.
- Terminate the goroutine cleanly after the error is delivered.

**Don't:**
- Don't `panic` from a goroutine for recoverable business errors.
- Don't have a goroutine `fmt.Println` an error and hope someone notices.
- Don't swallow errors in goroutines.

**Code:**
```go
type Result struct {
    Error    error
    Response *http.Response
}
checkStatus := func(done <-chan interface{}, urls ...string) <-chan Result {
    results := make(chan Result)
    go func() {
        defer close(results)
        for _, url := range urls {
            var result Result
            resp, err := http.Get(url)
            result = Result{Error: err, Response: resp}
            select {
            case <-done:
                return
            case results <- result:
            }
        }
    }()
    return results
}
done := make(chan interface{})
defer close(done)
urls := []string{"https://www.google.com", "https://badhost"}
for result := range checkStatus(done, urls...) {
    if result.Error != nil {
        fmt.Printf("error: %v", result.Error)
        continue
    }
    fmt.Printf("Response: %v\n", result.Response.Status)
}
```

```text
Response: 200 OK
error: Get https://badhost: dial tcp: lookup badhost on 127.0.1.1:53: no such host
```

*Ref: Concurrency_in_Go.md — "Error Handling"*

---

### 24. Build Pipelines from Channel-Based Stages

**Principle:** A pipeline is a series of stages that consume and emit the same type, composed by passing channels.

**Do:**
- Define `type Node[A any] func(<-chan A) <-chan A` and `GeneratorNode[A any] func() <-chan A`.
- `close(out)` in the goroutine when the stage is done.
- Use the `done` channel in every stage's `select`.
- Use `for-select` to combine `done` with the channel operation.
- Pre-empt work on `done` before long computations.

**Don't:**
- Don't return a value from a stage; return the output channel.
- Don't share a channel across stages; let each stage own its output channel.
- Don't forget `defer close(out)`.

**Code:**
```go
generator := func(done <-chan interface{}, integers ...int) <-chan int {
    intStream := make(chan int)
    go func() {
        defer close(intStream)
        for _, i := range integers {
            select {
            case <-done:
                return
            case intStream <- i:
            }
        }
    }()
    return intStream
}
multiply := func(
    done <-chan interface{},
    intStream <-chan int,
    multiplier int,
) <-chan int {
    multipliedStream := make(chan int)
    go func() {
        defer close(multipliedStream)
        for i := range intStream {
            select {
            case <-done:
                return
            case multipliedStream <- i*multiplier:
            }
        }
    }()
    return multipliedStream
}
add := func(
    done <-chan interface{},
    intStream <-chan int,
    additive int,
) <-chan int {
    addedStream := make(chan int)
    go func() {
        defer close(addedStream)
        for i := range intStream {
            select {
            case <-done:
                return
            case addedStream <- i+additive:
            }
        }
    }()
    return addedStream
}
```

*Ref: Concurrency_in_Go.md — "Pipelines"*

---

### 25. Chain Pipeline Stages with `ChainPipes`

**Principle:** `ChainPipes(generator, nodes...)` composes a generator with any number of `Node[A]` stages.

**Do:**
- Provide a `GeneratorNode` that returns a `<-chan A` from variadic or known input.
- Give a type hint when the generator is ambiguous.
- Reorder stages by reordering arguments.

**Don't:**
- Don't pass a raw `<-chan A` to `ChainPipes`; always go through a generator.
- Don't share state across stages through closures when a generator could supply it.

**Code:**
```go
type (
    Node[A any]         func(<-chan A) <-chan A
    GeneratorNode[A any] func() <-chan A
)
func ChainPipes[A any](gn GeneratorNode[A], nodes ...Node[A]) []A {
    in := gn()
    for _, node := range nodes {
        in = node(in)
    }
    return Collector(in)
}
```

```go
done := make(chan interface{})
defer close(done)
intStream := generator(done, 1, 2, 3, 4)
pipeline := multiply(done, add(done, multiply(done, intStream, 2), 1), 2)
for v := range pipeline {
    fmt.Println(v)
}
```

```text
6
10
14
18
```

*Ref: Concurrency_in_Go.md — "Pipelines"*

---

### 26. Use `repeat`, `repeatFn`, and `take` for Handy Generators

**Principle:** Combine a `repeat` (or `repeatFn`) generator with a `take` stage to cap work without knowing the upper bound in advance.

**Do:**
- Use `repeat` when you have a finite list of values to send forever.
- Use `repeatFn` when you have a function that produces values indefinitely.
- Always pair with a downstream `take` so work terminates.
- Use buffered channels for the generator's output if downstream backpressure would block the producer.

**Don't:**
- Don't `repeat` without eventually `take`-ing — an unterminated `repeat` is a goroutine leak.
- Don't use `repeat` for expensive generation — the stage is still throttled by the consumer.

**Code:**
```go
repeat := func(
    done <-chan interface{},
    values ...interface{},
) <-chan interface{} {
    valueStream := make(chan interface{})
    go func() {
        defer close(valueStream)
        for {
            for _, v := range values {
                select {
                case <-done:
                    return
                case valueStream <- v:
                }
            }
        }
    }()
    return valueStream
}
take := func(
    done <-chan interface{},
    valueStream <-chan interface{},
    num int,
) <-chan interface{} {
    takeStream := make(chan interface{})
    go func() {
        defer close(takeStream)
        for i := 0; i < num; i++ {
            select {
            case <-done:
                return
            case takeStream <- <- valueStream:
            }
        }
    }()
    return takeStream
}
```

*Ref: Concurrency_in_Go.md — "Some Handy Generators"*

---

### 27. Apply Fan-Out, Fan-In for Order-Independent Stages

**Principle:** Fan-out: run multiple copies of a stage in parallel. Fan-in: multiplex their outputs back into one channel.

**Do:**
- Fan out only when the stage is order-independent (no shared state with prior calls) and slow.
- Use `runtime.NumCPU()` as a starting point; profile to refine.
- Use the multiplex fan-in pattern with `sync.WaitGroup` to close the combined channel when all are drained.

**Don't:**
- Don't fan out a stage that depends on prior state — outputs will arrive out of order.
- Don't assume output order is preserved across fan-in.
- Don't fan out when the bottleneck is upstream, not the stage.

**Code:**
```go
fanIn := func(
    done <-chan interface{},
    channels ...<-chan interface{},
) <-chan interface{} {
    var wg sync.WaitGroup
    multiplexedStream := make(chan interface{})
    multiplex := func(c <-chan interface{}) {
        defer wg.Done()
        for i := range c {
            select {
            case <-done:
                return
            case multiplexedStream <- i:
            }
        }
    }
    wg.Add(len(channels))
    for _, c := range channels {
        go multiplex(c)
    }
    go func() {
        wg.Wait()
        close(multiplexedStream)
    }()
    return multiplexedStream
}
```

*Ref: Concurrency_in_Go.md — "Fan-Out, Fan-In"*

---

### 28. Use `orDone` to Wrap a Stream When `done` Is Not Yours

**Principle:** When consuming a channel whose ownership is not yours, the consumer must still respect its own `done`.

**Do:**
- Wrap reads in `orDone(done, c)` to keep the consumer cancelable.
- Use `orDone` to clean up verbose `select` blocks.
- Treat `orDone` as the standard glue between vendor libraries and your goroutine.

**Don't:**
- Don't range over a foreign channel directly inside your goroutine.
- Don't assume the foreign channel is closed when `done` is closed.

**Code:**
```go
orDone := func(done, c <-chan interface{}) <-chan interface{} {
    valStream := make(chan interface{})
    go func() {
        defer close(valStream)
        for {
            select {
            case <-done:
                return
            case v, ok := <-c:
                if !ok {
                    return
                }
                select {
                case valStream <- v:
                case <-done:
                }
            }
        }
    }()
    return valStream
}

for val := range orDone(done, myChan) {
    // Do something with val
}
```

*Ref: Concurrency_in_Go.md — "The or-done-channel"*

---

### 29. Use the `tee` Channel to Split a Stream

**Principle:** `tee` delivers each value to two outbound channels without re-reading.

**Do:**
- Shadow the outbound channel variables locally so writes don't block each other.
- Set the shadowed copy to `nil` after a successful write so the next iteration blocks on the other channel.

**Don't:**
- Don't serialize writes to `out1` and `out2` — they must go in one `select` so both happen per iteration.
- Don't reuse the tee for > 2 outputs by hardcoding — extract a slice-based version.

**Code:**
```go
tee := func(
    done <-chan interface{},
    in <-chan interface{},
) (_, _ <-chan interface{}) { <-chan interface{}) {
    out1 := make(chan interface{})
    out2 := make(chan interface{})
    go func() {
        defer close(out1)
        defer close(out2)
        for val := range orDone(done, in) {
            var out1, out2 = out1, out2
            for i := 0; i < 2; i++ {
                select {
                case <-done:
                case out1<-val:
                    out1 = nil
                case out2<-val:
                    out2 = nil
                }
            }
        }
    }()
    return out1, out2
}
```

*Ref: Concurrency_in_Go.md — "The tee-channel"*

---

### 30. Use `bridge` to Flatten a Channel of Channels

**Principle:** `bridge` presents a `chan <-chan A` as a single `<-chan A`.

**Do:**
- Use `bridge` when pipelines restart their inner channels and you have a `chan <-chan A` emerging.
- Range over the channel of channels and forward values until close.
- Honor `done` at every level.

**Don't:**
- Don't write nested `range` statements over `chan <-chan A` manually.
- Don't ignore `done` at the outer level.

**Code:**
```go
bridge := func(
    done <-chan interface{},
    chanStream <-chan <-chan interface{},
) <-chan interface{} {
    valStream := make(chan interface{})
    go func() {
        defer close(valStream)
        for {
            var stream <-chan interface{}
            select {
            case maybeStream, ok := <-chanStream:
                if !ok {
                    return
                }
                stream = maybeStream
            case <-done:
                return
            }
            for val := range orDone(done, stream) {
                select {
                case valStream <- val:
                case <-done:
                }
            }
        }
    }()
    return valStream
}
```

*Ref: Concurrency_in_Go.md — "The bridge-channel"*

---

### 31. Queue Strategically, Not Pervasively

**Principle:** Queues decouple stages and enable batching — they do not make a pipeline run faster overall.

**Do:**
- Queue at the entry of a pipeline to break feedback loops.
- Queue where batching reduces overhead (e.g., `bufio.Writer`).
- Use Little's Law: `L = λW` to size queues correctly.
- Profile before introducing queues.

**Don't:**
- Don't pepper queues in the hope of fixing slow stages.
- Don't size queues blindly — use `L = λW` with measured `λ` and `W`.
- Don't introduce queuing as a premature optimization.

*Ref: Concurrency_in_Go.md — "Queuing"*

---

### 32. Use `context` to Standardize Cancellation

**Principle:** `context.Context` is the standard for cancellation propagation, deadlines, and request-scoped data.

**Do:**
- Pass `context.Context` as the first parameter of any function that may block.
- Use `context.WithCancel` when a parent may cancel its children.
- Use `context.WithDeadline` or `context.WithTimeout` when a finite window exists.
- Use `context.WithValue` only for request-scoped data that transits process/API boundaries.
- Define a custom unexported key type for `Value`; export typed accessor functions.

**Don't:**
- Don't store optional parameters in a `Context`.
- Don't store mutable data in a `Context.Value`.
- Don't pass the same `Context` to two unrelated branches expecting different cancellation.
- Don't store `Context` instances in struct fields.

**Code:**
```go
var Canceled = errors.New("context canceled")
var DeadlineExceeded error = deadlineExceededError{}

type CancelFunc
type Context
func Background() Context
func TODO() Context
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
func WithValue(parent Context, key, val interface{}) Context
```

```go
type Context interface {
    // Deadline returns the time when work done on behalf of this
    // context should be canceled. Deadline returns ok==false when no
    // deadline is set. Successive calls to Deadline return the same
    // results.
    Deadline() (deadline time.Time, ok bool)
    // Done returns a channel that's closed when work done on behalf
    // of this context should be canceled. Done may return nil if this
    // context can never be canceled. Successive calls to Done return the
    // same value.
    Done() <-chan struct{}
    // Err returns a non-nil error value after Done is closed. Err
    // returns Canceled if the context was canceled or
    // DeadlineExceeded if the context's deadline passed. No other
    // values for Err are defined. After Done is closed, successive
    // calls to Err return the same value.
    Err() error
    // Value returns the value associated with this context for key,
    // or nil if no value is associated with key. Successive calls to
    // Value with the same key return the same result.
    Value(key interface{}) interface{}
}
```

*Ref: Concurrency_in_Go.md — "The context Package"*

---

### 33. Use the Done Channel Pattern OR `context.Context` — Not Both

**Principle:** Pick one cancellation propagation mechanism per project. Mixing them leads to leaks or duplicate work.

**Do:**
- Use a single `done` channel when your project predates the `context` package or you have no deadlines.
- Use `context.Context` when you need deadlines, error reasons, or request-scoped data.
- If you have both, derive one from the other with `ctx.Done()` or a `done <-chan struct{}` from `context.Background()`.

**Don't:**
- Don't pass both a `done <-chan struct{}` and a `context.Context` to the same function.
- Don't branch on `ctx.Err()` and `done` independently — they should agree.

**Code:**
```go
func main() {
    var wg sync.WaitGroup
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    wg.Add(1)
    go func() {
        defer wg.Done()
        if err := printGreeting(ctx); err != nil {
            fmt.Printf("cannot print greeting: %v\n", err)
            cancel()
        }
    }()
    wg.Add(1)
    go func() {
        defer wg.Done()
        if err := printFarewell(ctx); err != nil {
            fmt.Printf("cannot print farewell: %v\n", err)
        }
    }()
    wg.Wait()
}
```

```text
cannot print greeting: context deadline exceeded
cannot print farewell: context canceled
```

*Ref: Concurrency_in_Go.md — "The context Package"*

---

### 34. Define a Custom Key Type for `context.WithValue`

**Principle:** A typed unexported key prevents cross-package collisions; typed accessors give consumers compile-time safety.

**Do:**
- Define a key type unique to your package.
- Expose typed accessor functions that assert the value type.
- Document the keys your package stores.

**Don't:**
- Don't use strings or built-in types as keys.
- Don't export the key or store type so other packages can read it directly.
- Don't bypass the accessor function by calling `Value(key).(string)` yourself in the consumer.

**Code:**
```go
type ctxKey int
const (
    ctxUserID ctxKey = iota
    ctxAuthToken
)
func UserID(c context.Context) string {
    return c.Value(ctxUserID).(string)
}
func AuthToken(c context.Context) string {
    return c.Value(ctxAuthToken).(string)
}
func ProcessRequest(userID, authToken string) {
    ctx := context.WithValue(context.Background(), ctxUserID, userID)
    ctx = context.WithValue(ctx, ctxAuthToken, authToken)
    HandleResponse(ctx)
}
func HandleResponse(ctx context.Context) {
    fmt.Printf(
        "handling response for %v (auth: %v)",
        UserID(ctx),
        AuthToken(ctx),
    )
}
```

```text
handling response for jane (auth: abc123)
```

*Ref: Concurrency_in_Go.md — "The context Package"*

---

### 35. Build Errors as Well-Formed, Wrappable Values

**Principle:** Errors should answer what happened, when/where, the user-facing message, and how to get more information.

**Do:**
- Create a `Result` (or `MyError`) type that holds the inner error, message, stack trace, and metadata.
- Wrap at module boundaries so each module emits a typed error.
- Log full error details; show the user a brief, friendly message with a log ID.
- Map well-formed vs malformed errors to "show user's message" vs "show generic bug message."

**Don't:**
- Don't let raw library errors reach the user.
- Don't bury the original error.
- Don't compose error messages by string concatenation at every layer.

**Code:**
```go
type MyError struct {
    Inner error
    Message string
    StackTrace string
    Misc map[string]interface{}
}
func wrapError(err error, messagef string, msgArgs ...interface{}) MyError {
    return MyError{
        Inner: err,
        Message: fmt.Sprintf(messagef, msgArgs...),
        StackTrace: string(debug.Stack()),
        Misc: make(map[string]interface{}),
    }
}
func (err MyError) Error() string {
    return err.Message
}
```

*Ref: Concurrency_in_Go.md — "Error Propagation"*

---

### 36. Use Timeouts and Cancellations Deliberately

**Principle:** Timeouts are a defense against the unknown; cancellations are an explicit response to a change in need.

**Do:**
- Place timeouts on all operations in large systems to bound blast radius.
- Set timeouts with `context.WithTimeout` (or `context.WithDeadline`) so cancellation propagates.
- Keep non-preemptable atomic operations short — break long work into preemptable chunks.
- Build intermediate results in memory; modify shared state as a final step.
- Make state changes idempotent when they may be retried.

**Don't:**
- Don't rely on a timeout to fix a deadlock; chase the cause.
- Don't hold shared locks across a long non-preemptable block.

**Code:**
```go
reallyLongCalculation := func(
    done <-chan interface{},
    value interface{},
) interface{} {
    intermediateResult := longCalculation(done, value)
    select {
    case <-done:
        return nil
    default:
    }
    return longCaluclation(done, intermediateResult)
}
```

*Ref: Concurrency_in_Go.md — "Timeouts and Cancellation"*

---

### 37. Replicate Requests When Latency Dominates

**Principle:** Send the same request to multiple handlers; cancel the rest when one returns.

**Do:**
- Use replicated requests when the work is read-only and idempotent.
- Replicate across different processes, machines, or data stores for real benefit.
- Take the first response and cancel the rest.

**Don't:**
- Don't replicate writes; the side effects compound.
- Don't replicate uniform handlers — outliers must be possible.
- Don't underestimate the resource cost of running extra handlers.

**Code:**
```go
doWork := func(
    done <-chan interface{},
    id int,
    wg *sync.WaitGroup,
    result chan<- int,
) {
    started := time.Now()
    defer wg.Done()
    // Simulate random load
    simulatedLoadTime := time.Duration(1+rand.Intn(5))*time.Second
    select {
    case <-done:
    case <-time.After(simulatedLoadTime):
    }
    select {
    case <-done:
    case result <- id:
    }
    took := time.Since(started)
    // Display how long handlers would have taken
    if took < simulatedLoadTime {
        took = simulatedLoadTime
    }
    fmt.Printf("%v took %v\n", id, took)
}
done := make(chan interface{})
result := make(chan int)
var wg sync.WaitGroup
wg.Add(10)
for i:=0; i < 10; i++ {
    go doWork(done, i, &wg, result)
}
firstReturned := <-result
close(done)
wg.Wait()
fmt.Printf("Received an answer from #%v\n", firstReturned)
```

*Ref: Concurrency_in_Go.md — "Replicated Requests"*

---

### 38. Use Heartbeats for Liveness and Deterministic Tests

**Principle:** Heartbeats prove a goroutine is alive; interval heartbeats prove it is making progress; unit-of-work heartbeats prove each iteration is entered.

**Do:**
- Couple a `default`-guarded pulse send with each result channel send.
- Tie the heartbeat interval to your acceptable timeout (`timeout/2` is a good start).
- For tests, block on the first heartbeat before ranging over results.
- Detect "unhealthy" workers via a missing heartbeat within the timeout.

**Don't:**
- Don't include heartbeats and results in the same `select` case — the result may be lost.
- Don't rely on heartbeats if you can simply have the test set a short timeout.

**Code:**
```go
doWork := func(
    done <-chan interface{},
    pulseInterval time.Duration,
) (<-chan interface{}, <-chan time.Time) {
    heartbeat := make(chan interface{})
    results := make(chan time.Time)
    go func() {
        defer close(heartbeat)
        defer close(results)
        pulse := time.Tick(pulseInterval)
        workGen := time.Tick(2*pulseInterval)
        sendPulse := func() {
            select {
            case heartbeat <-struct{}{}:
            default:
            }
        }
        sendResult := func(r time.Time) {
            for {
                select {
                case <-done:
                    return
                case <-pulse:
                    sendPulse()
                case results <- r:
                    return
                }
            }
        }
        for {
            select {
            case <-done:
                return
            case <-pulse:
                sendPulse()
            case r := <-workGen:
                sendResult(r)
            }
        }
    }()
    return heartbeat, results
}
```

*Ref: Concurrency_in_Go.md — "Heartbeats"*

---

### 39. Use the `golang.org/x/time/rate` Token Bucket for Rate Limiting

**Principle:** Rate limit per system or per resource, with `MultiLimiter` for composite limits.

**Do:**
- Define a helper `Per(eventCount, duration)` to express events/time.
- Use `rate.NewLimiter(Per(n, period), burst)` for fine-grained controls.
- Combine with `MultiLimiter` for coarse + fine limits.
- Pass `ctx` to `Wait` so cancellations propagate.

**Don't:**
- Don't claim rate limits reduce total pipeline runtime — they only decouple stages.
- Don't pick the rate first; base it on measurement (Little's Law).
- Don't use `time.Sleep` for backoff — use the `Wait` semantics.

**Code:**
```go
func Open() *APIConnection {
    return &APIConnection{
        rateLimiter: rate.NewLimiter(rate.Limit(1), 1),
    }
}
type APIConnection struct {
    rateLimiter *rate.Limiter
}
func (a *APIConnection) ReadFile(ctx context.Context) error {
    if err := a.rateLimiter.Wait(ctx); err != nil {
        return err
    }
    // Pretend we do work here
    return nil
}
func (a *APIConnection) ResolveAddress(ctx context.Context) error {
    if err := a.rateLimiter.Wait(ctx); err != nil {
        return err
    }
    // Pretend we do work here
    return nil
}
```

*Ref: Concurrency_in_Go.md — "Rate Limiting"*

---

### 40. Build a Multi-Limiter from Multiple `rate.Limiter`s

**Principle:** Compose per-second and per-minute limits, with the most restrictive limit winning on each request.

**Do:**
- Sort limiters by `Limit()` and return the most restrictive as the composite.
- Call `Wait` on every limiter so all buckets decrement.
- Group limiters by purpose (API, disk, network) and combine at the call site.

**Don't:**
- Don't try to encode the period semantics in a single limiter.
- Don't return early on a less-restrictive limit; every limit must concede its token.

**Code:**
```go
type RateLimiter interface {
    Wait(context.Context) error
    Limit() rate.Limit
}
func MultiLimiter(limiters ...RateLimiter) *multiLimiter {
    byLimit := func(i, j int) bool {
        return limiters[i].Limit() < limiters[j].Limit()
    }
    sort.Slice(limiters, byLimit)
    return &multiLimiter{limiters: limiters}
}
type multiLimiter struct {
    limiters []RateLimiter
}
func (l *multiLimiter) Wait(ctx context.Context) error {
    for _, l := range l.limiters {
        if err := l.Wait(ctx); err != nil {
            return err
        }
    }
    return nil
}
func (l *multiLimiter) Limit() rate.Limit {
    return l.limiters[0].Limit()
}
```

*Ref: Concurrency_in_Go.md — "Rate Limiting"*

---

### 41. Heal Unhealthy Goroutines with a Steward

**Principle:** Long-running daemons need a mechanism to restart dead or stuck goroutines.

**Do:**
- Use a heartbeat from the ward to the steward; restart if the heartbeat stalls past the timeout.
- Pass `done` to the ward so the steward can signal it on restart.
- Treat the steward itself as monitorable (return a `startGoroutineFn` from `newSteward`).
- Restarts lose work — design the ward so the new copy can resume from a known state.

**Don't:**
- Don't make the ward responsible for healing itself; separation of concerns.
- Don't use `Once.Do` in a circular way — that's a deadlock.
- Don't restart indefinitely; track failure counts and give up after a threshold.

**Code:**
```go
type startGoroutineFn func(
    done <-chan interface{},
    pulseInterval time.Duration,
) (heartbeat <-chan interface{})
newSteward := func(
    timeout time.Duration,
    startGoroutine startGoroutineFn,
) startGoroutineFn {
    return func(
        done <-chan interface{},
        pulseInterval time.Duration,
    ) (<-chan interface{}) {
        heartbeat := make(chan interface{})
        go func() {
            defer close(heartbeat)
            var wardDone chan interface{}
            var wardHeartbeat <-chan interface{}
            startWard := func() {
                wardDone = make(chan interface{})
                wardHeartbeat = startGoroutine(or(wardDone, done), timeout/2)
            }
            startWard()
            pulse := time.Tick(pulseInterval)
        monitorLoop:
            for {
                timeoutSignal := time.After(timeout)
                for {
                    select {
                    case <-pulse:
                        select {
                        case heartbeat <- struct{}{}:
                        default:
                        }
                    case <-wardHeartbeat:
                        continue monitorLoop
                    case <-timeoutSignal:
                        log.Println("steward: ward unhealthy; restarting")
                        close(wardDone)
                        startWard()
                        continue monitorLoop
                    case <-done:
                        return
                    }
                }
            }
        }()
        return heartbeat
    }
}
```

*Ref: Concurrency_in_Go.md — "Healing Unhealthy Goroutines"*

---

### 42. Use `GOMAXPROCS` Only After Profiling

**Principle:** `GOMAXPROCS` controls OS thread count, not core count. The default is right for almost everyone.

**Do:**
- Trust the default (one context per logical CPU) in production.
- Increase only if you have evidence that more work queues help stress-test for races.
- Decrease if your host has other CPU-hungry processes.

**Don't:**
- Don't set `GOMAXPROCS(runtime.NumCPU())` reflexively in modern Go — it is the default.
- Don't tune `GOMAXPROCS` per environment — that pushes your program closer to the metal and hurts long-term stability.

*Ref: Concurrency_in_Go.md — "The GOMAXPROCS Lever"*

---

### 43. Understand Go's Work-Stealing Scheduler

**Principle:** Go uses M:N scheduling with continuation stealing; the Go runtime hides it behind `go`.

**Do:**
- Treat the runtime as a black box; reach for primitives only when you have evidence.
- Use the `M`/`P`/`G` mental model when reading the runtime source.
- Trust the scheduler's M:N continuation stealing to keep goroutines cheap.

**Don't:**
- Don't model goroutines as OS threads.
- Don't try to outsmart the scheduler with manual affinity.
- Don't expect preemption for goroutines that loop without function calls (Go 1.13+; rare in practice).

*Ref: Concurrency_in_Go.md — "Work Stealing", "Stealing Tasks or Continuations?", "Presenting All of This to the Developer"*

---

### 44. Use `runtime/pprof` and `go test -race` to Diagnose

**Principle:** Profile for what you suspect, not for everything.

**Do:**
- Run `go test -race` and `go build -race` in CI.
- Use `pprof.Lookup("goroutine").Count()` to detect leaks.
- Use the custom profile pattern to namespace per-package data.
- Read goroutine panic stack traces as the panicking goroutine + the line that created it.

**Don't:**
- Don't enable the race detector only when chasing a specific bug — keep it on.
- Don't dump all goroutine stacks (`GOTRACEBACK=all`) unless you really need them.
- Don't ignore "failed to restore the stack" — increase `HISTORY_SIZE`.

**Code:**
```go
log.SetFlags(log.Ltime | log.LUTC)
log.SetOutput(os.Stdout)
// Every second, log how many goroutines are currently running.
go func() {
    goroutines := pprof.Lookup("goroutine")
    for range time.Tick(1*time.Second) {
        log.Printf("goroutine count: %d\n", goroutines.Count())
    }
}()
// Create some goroutines which will never exit.
var blockForever chan struct{}
for i := 0; i < 10; i++ {
    go func() { <-blockForever }()
    time.Sleep(500*time.Millisecond)
}
```

*Ref: Concurrency_in_Go.md — "Anatomy of a Goroutine Error", "Race Detection", "pprof"*

---

## Anti-Patterns & Common Mistakes

- **Racing on shared state with no synchronization:** Two goroutines reading/writing the same variable without a channel, mutex, or atomic. → *fix:* identify the context, force atomicity, run `go test -race`.
- **`time.Sleep` to "fix" a race:** Asymptotic but never correct. → *fix:* restructure for logical correctness.
- **Long-lived goroutine with no termination path:** Memory leak. → *fix:* always have a `done <-chan struct{}` and select on it.
- **Closing a channel from a consumer:** Violates the ownership rule; future writes panic. → *fix:* only the writing goroutine closes.
- **Reading or writing a nil channel:** Blocks forever (or panics on `close`). → *fix:* initialize the channel before use.
- **Hiding sync primitives in a struct's public API:** Forces callers to reason about locking. → *fix:* make the lock unexported and expose only the methods that lock.
- **Unbounded buffering to "fix" back-pressure:** Hides a real bottleneck and may create a death-spiral. → *fix:* size queues with Little's Law, queue at the entry, profile first.
- **Calling `time.After` in a hot loop without holding a reference:** Every call creates a new channel; they pile up until GC. → *fix:* use `time.NewTicker` and `defer ticker.Stop()`.
- **Mixing `done` channel and `context.Context` for the same goroutine:** Two cancellation signals = two ways to forget. → *fix:* pick one and derive the other if needed.
- **Catching panics in a goroutine silently with `recover()`:** Eats real bugs. → *fix:* only `recover` in a small recovery block that reports the panic upstream.
- **Returning `nil` from a goroutine function:** Hides whether the channel closed or had no data. → *fix:* always check `ok` or close the channel to signal completion.
- **Long non-preemptable atomic blocks:** Cancel a goroutine, it keeps running. → *fix:* break the work into chunks; select on `done` between chunks.
- **Replicating writes across many handlers:** Compounding side effects. → *fix:* replicate only read-only or idempotent operations.
- **Heal-in-place loops with no success criteria:** Livelock. → *fix:* add jitter, cap retries, and use timeouts to break out.
- **Sharing a `Context` between two unrelated branches:** Cancellation is no longer independent. → *fix:* derive child contexts with `WithCancel`/`WithTimeout` per branch.
- **Using `context.Value` for optional parameters:** Couples unrelated concerns. → *fix:* add explicit parameters.

## Decision Heuristics / Checklists

- **Channel or mutex?** Transferring ownership → channel. Guarding struct state → mutex. Coordinating multiple pieces → channel + select.
- **Buffered or unbuffered channel?** Know the upper bound and want to decouple → buffer it. Otherwise → unbuffered.
- **Goroutine count:** Start with `runtime.NumCPU()` for parallel work; otherwise one per logical unit.
- **`select` cases ready:** Pseudo-random — don't rely on order.
- **Heartbeat interval:** Roughly `timeout/2` so the heartbeat fires before the timeout triggers.
- **Cancellation propagation:** Pass `done` to all child goroutines; close once from the parent.
- **Context vs. done channel:** Use `Context` when you need deadlines, error reasons, or request-scoped data; otherwise a `done` channel is enough.
- **`once.Do` circular call:** Deadlock. Audit references.
- **Buffered channel size:** `L = λW` from Little's Law. Measure `λ` and `W`.
- **Race detector:** Always on (`-race`) for tests, builds, and CI.
- **`GOMAXPROCS`:** Trust the default. Only change with profiling evidence.
- **Restarts in a steward:** Track failure counts; give up after a threshold to avoid infinite restarts.
- **Heartbeat in test:** Block on the first heartbeat before ranging over results for deterministic tests.
- **Goroutine panic:** Look at the panicking goroutine + the line that created it. Use `GOTRACEBACK=all` only when needed.
- **Custom `context.Value` key:** Define an unexported key type and export typed accessor functions.

## Key Takeaways

1. **CSP is the philosophical backbone.** Go favors channels and `select`; reach for memory access primitives in tight scopes.
2. **Goroutines are cheap functions with termination paths.** Create freely, but always include a `done` channel.
3. **Channels have owners.** The goroutine that instantiates, writes, and closes a channel owns it; expose unidirectional types to consumers.
4. **`select` composes channels.** Timeouts, cancellations, non-blocking polls — all expressed with one construct.
5. **The `sync` package solves the small problems.** `WaitGroup` for joins, `Mutex`/`RWMutex` for internal state, `Cond` for rendezvous, `Once` for init, `Pool` for expensive objects.
6. **Pipelines compose channels.** `done`-bearing stages with `close(out)` and `for-range` over the output stream.
7. **Fan-out for order-independent, slow stages.** Multiplex with `WaitGroup` fan-in.
8. **`or` and `bridge` collapse channel-of-channels.** Use them when the count is dynamic.
9. **Queues decouple stages; they don't speed them up.** Size with Little's Law; place at the entry or at batching opportunities.
10. **`context` standardizes cancellation.** Pass as first arg, use `WithCancel`/`WithDeadline`/`WithTimeout`, store only request-scoped values via typed unexported keys.
11. **Errors are first-class values.** Pair with results in a `Result` type; let parents decide what to do.
12. **Heartbeats prove liveness and enable deterministic tests.** Couple an interval pulse with a unit-of-work pulse.
13. **Rate limit with `rate.Limiter`; compose with `MultiLimiter`.** Per second, per minute, per resource — combine at the call site.
14. **Stewards heal unhealthy long-running goroutines.** Use the heartbeat pattern; restarts lose work, so design the ward to resume from a known state.
15. **Use `go test -race` and the `pprof` package in CI.** Trust the runtime; reach for primitives only with evidence.

## Cross-References
- Related: [[./Learning_Domain_Driven_Design.md]]
- Related: [[./Building_Modern_CLI_Applications_in_Go.md]]
- Related: [[./Efficient_Go_Data-Driven_Optimization.md]]
- Related: [[../INDEX.md]]
