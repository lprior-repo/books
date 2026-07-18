# Concurrency in Go
**Author:** Katherine Cox-Buday
**Topic tags:** `#concurrency` `#go` `#testing` `#architecture` `#performance` `#error-handling`
**Language focus:** Go-first
**Sources:** `markdown_output/Concurrency_in_Go_-_Katherine_Cox-Buday/Concurrency_in_Go_-_Katherine_Cox-Buday.md` · `summaries/Concurrency_in_Go_-_Katherine_Cox-Buday.md`

## TL;DR
The definitive guide to Go's concurrency story. It establishes CSP as Go's philosophical backbone (goroutines + channels + `select`), enumerates the building blocks in the `sync` package, then composes them into reusable patterns (pipelines, fan-out/fan-in, or/tee/bridge/or-done channels, heartbeats, replicated requests, rate limiting, healing goroutines) and finally scales them with the `context` package. The book's central conventions: every goroutine must have a termination path, channels have owners, errors are first-class values flowing through the same channels as results, and you should prefer logical correctness over probabilistic timing (never sprinkle `time.Sleep`).

---

## Best Practices by Topic

### Concurrency vs. Parallelism & the CSP Philosophy

**Principle:** Concurrency is a property of code (how you *structure* the problem); parallelism is a property of the running program (whether it *executes* simultaneously). Go models concurrency with CSP primitives — goroutines, channels, and `select` — supplanting the OS-thread + lock model.

**Do:**
- Model problems at their natural level of concurrency with goroutines (one goroutine per connection, per user, per unit of work).
- Prefer channels when coordinating multiple pieces of logic or transferring ownership of data.
- Use whichever is most expressive/simple: channels for coordination/ownership, mutexes for guarding internal struct state.
- Treat goroutines as a free resource — don't pool them up front; that's premature optimization.

**Don't:**
- Conflate concurrency with parallelism — concurrent code may or may not run in parallel depending on the host.
- Carry over OS-thread patterns (thread pools, fine-grained lock lattices) unless profiling proves they're needed.
- Assume "share memory by communicating" forbids mutexes entirely — the Go FAQ explicitly allows `sync.Mutex` when simpler.

**Decision tree (from Ch. 2):**
1. Transferring ownership of data? → channel
2. Guarding internal state of a struct? → mutex (keep it internal; never leak locks past the type boundary)
3. Coordinating multiple pieces of logic? → channels (composable via `select`)
4. Performance-critical section proven by profiling? → mutex (channels *use* mutexes internally, so they can only be slower)

*Ref: Concurrency_in_Go.md — "Go's Philosophy on Concurrency", "The Difference Between Concurrency and Parallelism"*

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
*Ref: Concurrency_in_Go.md — "Go's Philosophy on Concurrency"*

---

### Race Conditions, Atomicity & the Memory Model

**Principle:** A race condition occurs when the program relies on an ordering it never guaranteed. Target logical correctness — never paper over races with `time.Sleep`.

**Do:**
- Define the *context* (scope) in which an operation must be atomic before reasoning about safety.
- Force atomicity with channels, mutexes, or `sync/atomic` where needed.
- Iterate through all possible interleavings when reviewing concurrent code — "imagine an hour passes between operations."
- Run `go test -race` and `go build -race` in CI.

**Don't:**
- Sprinkle `time.Sleep` to "fix" races — it only raises the probability of correctness, asymptotically approaching but never reaching it.
- Assume `i++` is atomic — it expands to load / inc / store, each atomic alone but not in combination.
- Assume ordering guarantees beyond what the memory model states; compilers and CPUs reorder freely.

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

```go
// Synchronizing access to memory with a mutex (illustrative, not idiomatic).
var memoryAccess sync.Mutex
var value int
go func() {
    memoryAccess.Lock()
    value++
    memoryAccess.Unlock()
}()
memoryAccess.Lock()
if value == 0 {
    fmt.Printf("the value is %v.\n", value)
} else {
    fmt.Printf("the value is %v.\n", value)
}
memoryAccess.Unlock()
```
*Ref: Concurrency_in_Go.md — "Memory Access Synchronization"*

---

### Deadlocks, Livelocks & Starvation

**Principle:** Correctness is necessary but not sufficient — you must also guarantee *liveness* (the program makes progress). The Coffman conditions enumerate what must all be present for a deadlock; break any one to prevent it.

**Coffman conditions (all four must hold for deadlock):** Mutual exclusion · Hold-and-wait · No preemption · Circular wait.

**Do:**
- Order lock acquisition globally (resource hierarchy) to break circular wait.
- Keep critical sections small; broaden scope only after profiling proves a need (favor fairness first).
- Detect starvation with metrics — log when work is accomplished and compare against expected rate.
- Use timeouts on concurrent operations in large systems to guarantee the system can't deadlock forever.

**Don't:**
- Acquire locks in different orders from different goroutines.
- Hold a lock for far longer than the critical section ("greedy worker" starves others).
- Try to prevent deadlocks with uncoordinated retries — that turns a deadlock into a livelock.

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
*Ref: Concurrency_in_Go.md — "Deadlock", "Coffman Conditions"*

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

### Determining Concurrency Safety (API & Comment Hygiene)

**Principle:** The hardest part of concurrency is people. Make ownership and synchronization responsibilities obvious from the signature.

**Do:**
- Document, on concurrent APIs, three things: (1) who is responsible for the concurrency, (2) how the problem maps onto primitives, (3) who is responsible for synchronization.
- Prefer side-effect-free signatures (`func CalculatePi(begin, end int64) []uint`) so callers don't have to worry about shared state.
- Return channels (`<-chan uint`) to signal that the function spins up its own goroutine.

**Don't:**
- Expose a `*Pi` pointer and leave callers guessing whether they must synchronize writes.

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

### Goroutines & the Fork-Join Model

**Principle:** Goroutines are functions running concurrently — not OS threads, not green threads, but coroutines deeply integrated with the runtime. They are cheap (~few KB, grow/shrink automatically) and not garbage collected, so each must have a termination path.

**Do:**
- Create goroutines freely; only worry about the count after profiling shows it's the bottleneck.
- Always establish a join point (`sync.WaitGroup`, channel receive) — without one you have a race, not correctness.
- Pass loop variables explicitly into goroutines to avoid the classic closure-capture bug.

**Don't:**
- Rely on `time.Sleep` to "wait" for a goroutine — it's a race, not a join.
- Assume a goroutine will ever run before `main` returns.
- Abandon goroutines — they are not GC'd and will leak.

```go
// The most basic goroutine: function + go keyword.
go sayHello()

// Anonymous closure works too — must invoke immediately.
go func() {
    fmt.Println("hello")
}()

// Join point via WaitGroup (correct version of the example above).
var wg sync.WaitGroup
sayHello := func() {
    defer wg.Done()
    fmt.Println("hello")
}
wg.Add(1)
go sayHello()
wg.Wait()
```
*Ref: Concurrency_in_Go.md — "Goroutines"*

```go
// GOTCHA: closures capture loop variables by reference.
// Prints "good day" three times on many machines.
var wg sync.WaitGroup
for _, salutation := range []string{"hello", "greetings", "good day"} {
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println(salutation) // captures the same salutation
    }()
}
wg.Wait()

// FIX: pass a copy of the loop variable as a parameter.
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
*Ref: Concurrency_in_Go.md — "Goroutines" (closure example)*

```go
// Goroutines are NOT garbage collected. This leaks forever:
go func() {
    // <operation that will block forever>
}()
// Do work
```
*Ref: Concurrency_in_Go.md — "Goroutines"*

```go
// Measuring goroutine weight (~2.7 KB each on a 64-bit machine).
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
*Ref: Concurrency_in_Go.md — "Goroutines" (Table 3-1: ~3.7e5 goroutines/GB)*

```go
// Goroutine context switch ≈ 225 ns vs. OS thread ≈ 1.47 µs (92% faster).
func BenchmarkContextSwitch(b *testing.B) {
    var wg sync.WaitGroup
    begin := make(chan struct{})
    c := make(chan struct{})
    var token struct{}
    sender := func() {
        defer wg.Done()
        <-begin
        for i := 0; i < b.N; i++ {
            c <- token
        }
    }
    receiver := func() {
        defer wg.Done()
        <-begin
        for i := 0; i < b.N; i++ {
            <-c
        }
    }
    wg.Add(2)
    go sender()
    go receiver()
    b.StartTimer()
    close(begin)
    wg.Wait()
}
```
*Ref: Concurrency_in_Go.md — "Goroutines" (context-switch benchmark)*

---

### The sync Package — WaitGroup

**Principle:** `WaitGroup` is a concurrent-safe counter for waiting on a batch of goroutines when you don't care about results.

**Do:**
- Call `Add` *outside* the goroutine it tracks (inside introduces a race: `Wait` could return before the goroutine starts).
- Always `defer wg.Done()` as the first statement in the tracked goroutine.
- Use `Add(n)` before a loop instead of `Add(1)` per iteration when you know the count up front.

```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    fmt.Println("1st goroutine sleeping...")
    time.Sleep(1)
}()
wg.Add(1)
go func() {
    defer wg.Done()
    fmt.Println("2nd goroutine sleeping...")
    time.Sleep(2)
}()
wg.Wait()
fmt.Println("All goroutines complete.")
```
*Ref: Concurrency_in_Go.md — "WaitGroup"*

```go
// Add N once before the loop — cleaner than Add(1) per iteration.
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
*Ref: Concurrency_in_Go.md — "WaitGroup"*

---

### The sync Package — Mutex & RWMutex

**Principle:** A mutex guards a critical section. `RWMutex` allows many concurrent readers *or* one writer. Use `RWMutex` when readers outnumber writers and the cross-section is non-trivial.

**Do:**
- Always pair `Lock` with `defer Unlock()` (survives panics).
- Minimize critical-section size — entering/exiting is expensive.
- Profile before assuming `RWMutex` helps; its win only kicks in around 2+ readers.

```go
var count int
var lock sync.Mutex
increment := func() {
    lock.Lock()
    defer lock.Unlock()
    count++
    fmt.Printf("Incrementing: %d\n", count)
}
decrement := func() {
    lock.Lock()
    defer lock.Unlock()
    count--
    fmt.Printf("Decrementing: %d\n", count)
}
```
*Ref: Concurrency_in_Go.md — "Mutex and RWMutex"*

```go
// RWMutex benchmark — read-only Locker vs full Mutex under many readers.
producer := func(wg *sync.WaitGroup, l sync.Locker) {
    defer wg.Done()
    for i := 5; i > 0; i-- {
        l.Lock()
        l.Unlock()
        time.Sleep(1)
    }
}
observer := func(wg *sync.WaitGroup, l sync.Locker) {
    defer wg.Done()
    l.Lock()
    defer l.Unlock()
}
test := func(count int, mutex, rwMutex sync.Locker) time.Duration {
    var wg sync.WaitGroup
    wg.Add(count + 1)
    beginTestTime := time.Now()
    go producer(&wg, mutex)
    for i := count; i > 0; i-- {
        go observer(&wg, rwMutex)
    }
    wg.Wait()
    return time.Since(beginTestTime)
}
// RWMutex wins around 2+ readers; gap widens with reader count.
```
*Ref: Concurrency_in_Go.md — "Mutex and RWMutex"*

---

### The sync Package — Cond

**Principle:** `Cond` is a rendezvous point for goroutines waiting for or announcing an event. Far more efficient than polling loops with `time.Sleep`, and `Broadcast` reaches multiple waiters in one call (hard to reproduce with channels).

**Do:**
- Check the condition in a `for` loop around `Wait()` — a signal only means *something* happened, not your specific condition.
- Remember `Wait()` atomically unlocks `c.L` on entry and re-locks on exit (a hidden side effect).

**Don't:**
- Poll a condition with `for !cond { time.Sleep(...) }` — burns CPU or adds latency.

```go
c := sync.NewCond(&sync.Mutex{})
c.L.Lock()
for conditionTrue() == false {
    c.Wait()
}
c.L.Unlock()
```
*Ref: Concurrency_in_Go.md — "Cond"*

```go
// Bounded queue: producers Wait when full; Signal after dequeue.
c := sync.NewCond(&sync.Mutex{})
queue := make([]interface{}, 0, 10)
removeFromQueue := func(delay time.Duration) {
    time.Sleep(delay)
    c.L.Lock()
    queue = queue[1:]
    fmt.Println("Removed from queue")
    c.L.Unlock()
    c.Signal()
}
for i := 0; i < 10; i++ {
    c.L.Lock()
    for len(queue) == 2 {
        c.Wait()
    }
    fmt.Println("Adding to queue")
    queue = append(queue, struct{}{})
    go removeFromQueue(1 * time.Second)
    c.L.Unlock()
}
```
*Ref: Concurrency_in_Go.md — "Cond"*

```go
// Broadcast fans out to many subscribers at once (channels can't easily do this).
type Button struct { Clicked *sync.Cond }
button := Button{Clicked: sync.NewCond(&sync.Mutex{})}
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
subscribe(button.Clicked, func() { fmt.Println("Maximizing window.");    clickRegistered.Done() })
subscribe(button.Clicked, func() { fmt.Println("Displaying annoying dialog box!"); clickRegistered.Done() })
subscribe(button.Clicked, func() { fmt.Println("Mouse clicked.");        clickRegistered.Done() })
button.Clicked.Broadcast()
clickRegistered.Wait()
```
*Ref: Concurrency_in_Go.md — "Cond" (Button/Broadcast example)*

---

### The sync Package — Once

**Principle:** `sync.Once` guarantees `Do`'s function runs exactly once across all goroutines. Wrap it in a small lexical scope — `Once` is coupled to *the first function passed in*, not to uniqueness of functions.

**Do:**
- Formalize the coupling between a `Once` and its function inside a small type or function.

**Don't:**
- Pass two different functions to the same `Once` expecting both to run — only the first executes.
- Create circular `Once` dependencies (deadlock).

```go
var count int
increment := func() { count++ }
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
fmt.Printf("Count is %d\n", count) // Count is 1

// GOTCHA: only the FIRST Do's function is ever called.
var once sync.Once
once.Do(increment) // runs increment
once.Do(decrement) // never runs — prints "Count: 1"
```
*Ref: Concurrency_in_Go.md — "Once"*

---

### The sync Package — Pool

**Principle:** `sync.Pool` is a concurrent-safe object pool for reusing short-lived, expensive-to-create objects (buffers, connections) to reduce GC pressure and front-load allocation cost.

**Do:**
- Provide a `New` func that is thread-safe.
- `defer pool.Put(obj)` after `Get`.
- Make no assumptions about the state of objects you receive.
- Keep pooled objects roughly homogeneous.

**Don't:**
- Use a Pool when object size/shape varies wildly — you'll waste time resizing.
- Forget `Put` — the pool becomes useless.

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
// "Creating new instance." printed only twice.
```
*Ref: Concurrency_in_Go.md — "Pool"*

```go
// Pool of 1KB byte buffers reused by 1M goroutines — only 8 allocations.
var numCalcsCreated int
calcPool := &sync.Pool{
    New: func() interface{} {
        numCalcsCreated += 1
        mem := make([]byte, 1024)
        return &mem
    },
}
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())
const numWorkers = 1024 * 1024
var wg sync.WaitGroup
wg.Add(numWorkers)
for i := numWorkers; i > 0; i-- {
    go func() {
        defer wg.Done()
        mem := calcPool.Get().(*[]byte)
        defer calcPool.Put(mem)
    }()
}
wg.Wait()
fmt.Printf("%d calculators were created.", numCalcsCreated) // 8
```
*Ref: Concurrency_in_Go.md — "Pool"*

```go
// Pool warming a connection cache → 3 orders of magnitude faster responses.
func warmServiceConnCache() *sync.Pool {
    p := &sync.Pool{New: connectToService}
    for i := 0; i < 10; i++ {
        p.Put(p.New())
    }
    return p
}
// Handler: svcConn := connPool.Get(); ...; connPool.Put(svcConn)
// Benchmark: 1,000,038,543 ns/op  →  2,904,307 ns/op
```
*Ref: Concurrency_in_Go.md — "Pool" (network daemon benchmark)*

---

### Channels — Types, Ownership & State Semantics

**Principle:** Channels are the composable conduit for goroutine-to-goroutine communication. The goroutine that *instantiates* a channel owns it: it writes, closes, and exposes a read-only view to consumers.

**Do:**
- Make the **owner** instantiate, write, close, and encapsulate — expose only `<-chan` to consumers.
- Make the **consumer** handle blocking reads and detect closure via the `, ok` form.
- Keep the scope of channel ownership small so lifecycle is obvious.

**Don't:**
- Write to or close a channel from outside its owner.
- Close a channel twice, close a nil channel, or write to a closed channel (all panic).
- Instantiate unidirectional channels; convert bidirectional to unidirectional at API boundaries instead.

**Channel state table (memorize this):**

| Operation | nil | Open & Empty | Open & Full | Closed | Wrong Direction |
|-----------|-----|--------------|-------------|--------|------------------|
| Read      | Block | Block | Value | zero, false | Compile error |
| Write     | Block | Write | Block | **panic** | Compile error |
| close     | **panic** | Closes; reads drain then return zero | Closes; reads drain then zero | **panic** | Compile error |

```go
// Owner instantiates, writes, closes; consumer receives a read-only view.
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
*Ref: Concurrency_in_Go.md — "Channels" (ownership example)*

```go
// Unidirectional channels as API contracts.
var receiveChan <-chan interface{}
var sendChan    chan<- interface{}
dataStream := make(chan interface{})
receiveChan = dataStream // implicit conversion
sendChan    = dataStream
```
*Ref: Concurrency_in_Go.md — "Channels"*

```go
// Buffered channels: sender blocks only when buffer is full; receiver blocks only when empty.
c := make(chan rune, 4)
c <- 'A' // fills slot 1; blocks only after the 4th write with no reader

// Unbuffered == buffered with capacity 0.
a := make(chan int)
b := make(chan int, 0)
```
*Ref: Concurrency_in_Go.md — "Channels" (buffered)*

```go
// Closing a channel unblocks N receivers at once (cheaper than N writes).
begin := make(chan interface{})
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(i int) {
        defer wg.Done()
        <-begin                       // wait
        fmt.Printf("%v has begun\n", i)
    }(i)
}
fmt.Println("Unblocking goroutines...")
close(begin)                           // releases all 5 simultaneously
wg.Wait()
```
*Ref: Concurrency_in_Go.md — "Channels" (close-as-broadcast)*

```go
// range over a channel exits automatically when the channel is closed.
intStream := make(chan int)
go func() {
    defer close(intStream)
    for i := 1; i <= 5; i++ {
        intStream <- i
    }
}()
for integer := range intStream {
    fmt.Printf("%v ", integer)
}
```
*Ref: Concurrency_in_Go.md — "Channels" (ranging)*

---

### The select Statement

**Principle:** `select` is the multiplexer that makes channels composable. It considers all cases simultaneously; when multiple are ready it picks pseudo-randomly (uniform); `default` makes it non-blocking; `time.After` adds timeouts.

**Do:**
- Use `select` with `time.After` to bound waits.
- Use `default` for non-blocking attempts and to do work between checks (for-select loop).
- Rely on the random selection to keep programs fair in the average case.

**Don't:**
- Assume cases are evaluated top-to-bottom — they aren't.

```go
// Timeout with time.After.
var c <-chan int
select {
case <-c:
case <-time.After(1 * time.Second):
    fmt.Println("Timed out.")
}
```
*Ref: Concurrency_in_Go.md — "The select Statement"*

```go
// Random uniform selection — over 1000 iterations, ~500/500 split.
c1 := make(chan interface{}); close(c1)
c2 := make(chan interface{}); close(c2)
var c1Count, c2Count int
for i := 1000; i >= 0; i-- {
    select {
    case <-c1: c1Count++
    case <-c2: c2Count++
    }
}
fmt.Printf("c1Count: %d\nc2Count: %d\n", c1Count, c2Count)
```
*Ref: Concurrency_in_Go.md — "The select Statement"*

```go
// for-select with default — make progress while polling for cancellation.
done := make(chan interface{})
go func() {
    time.Sleep(5 * time.Second)
    close(done)
}()
workCounter := 0
loop:
for {
    select {
    case <-done:
        break loop
    default:
    }
    workCounter++
    time.Sleep(1 * time.Second)
}
fmt.Printf("Achieved %v cycles of work before signalled to stop.\n", workCounter)
```
*Ref: Concurrency_in_Go.md — "The select Statement"*

---

### Confinement — Eliminating Synchronization Entirely

**Principle:** If data is only ever available to *one* concurrent process, no synchronization is needed. Prefer **lexical** confinement (enforced by the compiler via types/scope) over **ad hoc** confinement (enforced by convention).

**Do:**
- Expose only read-only or write-only channel views to confine channel use.
- Pass non-overlapping slices of a buffer to different goroutines to confine data ranges.

```go
// Lexical confinement via read-only channel views.
chanOwner := func() <-chan int {
    results := make(chan int, 5)
    go func() {
        defer close(results)
        for i := 0; i <= 5; i++ {
            results <- i
        }
    }()
    return results
}
consumer := func(results <-chan int) {
    for result := range results {
        fmt.Printf("Received: %d\n", result)
    }
    fmt.Println("Done receiving!")
}
results := chanOwner()
consumer(results)
```
*Ref: Concurrency_in_Go.md — "Confinement"*

```go
// Lexical confinement of a non-concurrent-safe bytes.Buffer by slicing.
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
go printData(&wg, data[:3]) // "gol"
go printData(&wg, data[3:]) // "ang"
wg.Wait()
```
*Ref: Concurrency_in_Go.md — "Confinement"*

---

### The for-select Loop Pattern

**Principle:** The workhorse shape for goroutines that loop until cancelled.

```go
// Variation 1: send iteration variables out on a channel.
for _, s := range []string{"a", "b", "c"} {
    select {
    case <-done:        return
    case stringStream <- s:
    }
}

// Variation 2a: check done, then do work.
for {
    select {
    case <-done: return
    default:
    }
    // Do non-preemptable work
}

// Variation 2b: embed work in default.
for {
    select {
    case <-done: return
    default:
        // Do non-preemptable work
    }
}
```
*Ref: Concurrency_in_Go.md — "The for-select Loop"*

---

### Goroutine Lifecycle — Preventing Leaks

**Principle:** **If a goroutine is responsible for creating a goroutine, it is also responsible for ensuring it can stop the goroutine.** Pass a `done <-chan interface{}` (conventionally the first arg) and `close(done)` to cancel.

**Do:**
- Give every goroutine a clear termination path: completion, unrecoverable error, or external cancellation.
- Wrap both reads *and* writes with a `select` that includes `<-done` so a goroutine blocked either way can still be cancelled.

**Don't:**
- Pass a nil channel to a goroutine that ranges over it — it blocks forever and leaks.

```go
// LEAK: nil channel means the goroutine ranges forever.
doWork := func(strings <-chan string) <-chan interface{} {
    completed := make(chan interface{})
    go func() {
        defer fmt.Println("doWork exited.")
        defer close(completed)
        for s := range strings { // blocks on nil forever
            fmt.Println(s)
        }
    }()
    return completed
}
doWork(nil)
fmt.Println("Done.")
```
*Ref: Concurrency_in_Go.md — "Preventing Goroutine Leaks"*

```go
// FIXED: done channel lets the parent cancel a blocked child.
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
    time.Sleep(1 * time.Second)
    fmt.Println("Canceling doWork goroutine...")
    close(done)
}()
<-terminated
fmt.Println("Done.")
```
*Ref: Concurrency_in_Go.md — "Preventing Goroutine Leaks"*

```go
// Canceling a producer blocked on send.
newRandStream := func(done <-chan interface{}) <-chan int {
    randStream := make(chan int)
    go func() {
        defer fmt.Println("newRandStream closure exited.")
        defer close(randStream)
        for {
            select {
            case randStream <- rand.Int():
            case <-done:
                return
            }
        }
    }()
    return randStream
}
done := make(chan interface{})
randStream := newRandStream(done)
for i := 1; i <= 3; i++ {
    fmt.Printf("%d: %d\n", i, <-randStream)
}
close(done)
time.Sleep(1 * time.Second)
```
*Ref: Concurrency_in_Go.md — "Preventing Goroutine Leaks"*

---

### The or-Channel — Combining Done Channels

**Principle:** Recursively combine N done channels into one that closes when *any* input closes. Useful at module intersections where multiple cancellation conditions apply.

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

// Usage — closes after the soonest input (1s).
sig := func(after time.Duration) <-chan interface{} {
    c := make(chan interface{})
    go func() {
        defer close(c)
        time.Sleep(after)
    }()
    return c
}
start := time.Now()
<-or(
    sig(2*time.Hour),
    sig(5*time.Minute),
    sig(1*time.Second),
    sig(1*time.Hour),
    sig(1*time.Minute),
)
fmt.Printf("done after %v", time.Since(start)) // ~1s
```
*Ref: Concurrency_in_Go.md — "The or-channel"*

---

### Error Handling in Concurrent Code

**Principle:** Errors are first-class citizens. Couple the error with its result and send both through the same channel — never swallow errors inside the goroutine that produced them. The parent (with full system context) decides what to do.

**Do:**
- Define a `Result` type carrying both `Error` and the response/value.
- Have the goroutine send `Result` instances; let the consumer apply policy (retry, break, count).

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

// Consumer-side policy: bail after 3 errors.
done := make(chan interface{})
defer close(done)
errCount := 0
urls := []string{"a", "https://www.google.com", "b", "c", "d"}
for result := range checkStatus(done, urls...) {
    if result.Error != nil {
        fmt.Printf("error: %v\n", result.Error)
        errCount++
        if errCount >= 3 {
            fmt.Println("Too many errors, breaking!")
            break
        }
        continue
    }
    fmt.Printf("Response: %v\n", result.Response.Status)
}
```
*Ref: Concurrency_in_Go.md — "Error Handling"*

---

### Pipelines — Stages, Generators & Composition

**Principle:** A pipeline is a series of stages that consume and return the same type. Channels let stages run concurrently, be ranged over, and be combined without modification. Stages should be preemptable via a `done` channel so closing `done` cascades a clean teardown.

**Stage properties:**
- Consumes and returns the same type.
- Reified by the language (Go functions are first-class).

**Do:**
- Make every stage take `done <-chan interface{}` as its first arg and select on it for every send.
- `defer close(outStream)` at the top of each stage's goroutine.
- Make the first stage a *generator* that converts discrete values into a stream.

```go
// Canonical channel-based pipeline: generator → multiply → add → multiply.
generator := func(done <-chan interface{}, integers ...int) <-chan int {
    intStream := make(chan int)
    go func() {
        defer close(intStream)
        for _, i := range integers {
            select {
            case <-done:        return
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
            case <-done:                      return
            case multipliedStream <- i * multiplier:
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
            case <-done:                  return
            case addedStream <- i + additive:
            }
        }
    }()
    return addedStream
}

done := make(chan interface{})
defer close(done)
intStream := generator(done, 1, 2, 3, 4)
pipeline := multiply(done, add(done, multiply(done, intStream, 2), 1), 2)
for v := range pipeline {
    fmt.Println(v) // 6 10 14 18
}
```
*Ref: Concurrency_in_Go.md — "Best Practices for Constructing Pipelines"*

```go
// Generic reusable generators — repeat, repeatFn, take, toString.
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
                case <-done:               return
                case valueStream <- v:
                }
            }
        }
    }()
    return valueStream
}
repeatFn := func(
    done <-chan interface{},
    fn func() interface{},
) <-chan interface{} {
    valueStream := make(chan interface{})
    go func() {
        defer close(valueStream)
        for {
            select {
            case <-done:             return
            case valueStream <- fn():
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
            case <-done:                  return
            case takeStream <- <-valueStream:
            }
        }
    }()
    return takeStream
}
toString := func(
    done <-chan interface{},
    valueStream <-chan interface{},
) <-chan string {
    stringStream := make(chan string)
    go func() {
        defer close(stringStream)
        for v := range valueStream {
            select {
            case <-done:               return
            case stringStream <- v.(string):
            }
        }
    }()
    return stringStream
}

// Infinite stream — only N+1 values ever generated.
for num := range take(done, repeat(done, 1), 10) {
    fmt.Printf("%v ", num) // 1 1 1 1 1 1 1 1 1 1
}
for num := range take(done, repeatFn(done, func() interface{} { return rand.Int() }), 10) {
    fmt.Println(num)
}
```
*Ref: Concurrency_in_Go.md — "Some Handy Generators"*

> **Empty-interface tradeoff:** `interface{}` channels make a reusable stage library possible; type-specific stages are ~2× faster but only marginally faster in magnitude. Usually you're I/O-bound, so the difference is negligible.

---

### Fan-Out, Fan-In

**Principle:** Run multiple copies of an *order-independent*, *long-running* stage to parallelize pulls from upstream; then multiplex the outputs back into one channel.

**Criteria for fanning out a stage:**
- It doesn't rely on values the stage had calculated before (order-independent).
- It takes a long time to run.

```go
// Fan-out: start NumCPU copies of primeFinder.
numFinders := runtime.NumCPU()
finders := make([]<-chan int, numFinders)
for i := 0; i < numFinders; i++ {
    finders[i] = primeFinder(done, randIntStream)
}

// Fan-in: multiplex many channels into one.
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
            case <-done:                  return
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

for prime := range take(done, fanIn(done, finders...), 10) {
    fmt.Printf("\t%d\n", prime)
}
// Search time: ~23s single → ~5s fanned out (78% faster)
```
*Ref: Concurrency_in_Go.md — "Fan-Out, Fan-In"*

---

### The or-Done Channel

**Principle:** Wrap an arbitrary channel read so cancellation is handled transparently and you can use a clean `for v := range orDone(done, ch)`.

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
                if ok == false {
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

// Before: ugly nested select. After: clean range.
for val := range orDone(done, myChan) {
    // Do something with val
}
```
*Ref: Concurrency_in_Go.md — "The or-done-channel"*

---

### The tee Channel

**Principle:** Split one input channel into two outputs that each see every value (like Unix `tee`).

```go
tee := func(
    done <-chan interface{},
    in <-chan interface{},
) (_, _ <-chan interface{}) {
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
                case out1 <- val:
                    out1 = nil
                case out2 <- val:
                    out2 = nil
                }
            }
        }
    }()
    return out1, out2
}

done := make(chan interface{})
defer close(done)
out1, out2 := tee(done, take(done, repeat(done, 1, 2), 4))
for val1 := range out1 {
    fmt.Printf("out1: %v, out2: %v\n", val1, <-out2)
}
```
*Ref: Concurrency_in_Go.md — "The tee-channel"*

---

### The bridge Channel

**Principle:** Flatten a `<-chan <-chan interface{}` (a stream of channels) into a single channel so consumers don't care that values arrive from sequenced sources.

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
                if ok == false {
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

genVals := func() <-chan <-chan interface{} {
    chanStream := make(chan (<-chan interface{}))
    go func() {
        defer close(chanStream)
        for i := 0; i < 10; i++ {
            stream := make(chan interface{}, 1)
            stream <- i
            close(stream)
            chanStream <- stream
        }
    }()
    return chanStream
}
for v := range bridge(nil, genVals()) {
    fmt.Printf("%v ", v) // 0 1 2 3 4 5 6 7 8 9
}
```
*Ref: Concurrency_in_Go.md — "The bridge-channel"*

---

### Queuing, Little's Law & Pipeline Throughput

**Principle:** Queuing **decouples stages** — it does *not* speed up total runtime. By Little's Law `L = λW`, adding queue capacity increases either arrival rate or time-in-system. Add queues only at (a) the pipeline entrance or (b) stages where batching improves efficiency.

**Do:**
- Add a buffer when a producer knows the exact write count and you want it to complete quickly.
- Use queues to break feedback loops / death-spirals at the entrance.
- Size buffers from Little's Law: `L = λ · Σ Wᵢ` — your pipeline is only as fast as its slowest stage.

**Don't:**
- Pepper buffers everywhere hoping for speed — they hide deadlocks and don't reduce total time.
- Persist in-flight state without considering what happens if the process panics (lose the queue).

```go
// Buffered write benchmark: chunking bytes via bufio.Writer.
func BenchmarkUnbufferedWrite(b *testing.B) {
    performWrite(b, tmpFileOrFatal())
}
func BenchmarkBufferedWrite(b *testing.B) {
    bufferredFile := bufio.NewWriter(tmpFileOrFatal())
    performWrite(b, bufio.NewWriter(bufferredFile))
}
// BenchmarkUnbufferedWrite-8   500000   3969 ns/op
// BenchmarkBufferedWrite-8    1000000   1356 ns/op   (~3× faster via chunking)
```
*Ref: Concurrency_in_Go.md — "Queuing"*

---

### The context Package — Cancellation, Deadlines & Values

**Principle:** `context.Context` flows through your call-graph (first arg, `ctx context.Context`) carrying cancellation, deadlines, and request-scoped data. Children can narrow the context but cannot cancel their parent.

**Do:**
- Always pass `Context` as the first argument; never store it in a struct.
- Use `context.WithCancel` for explicit cancellation, `WithTimeout`/`WithDeadline` for time bounds, `Background()`/`TODO()` to start the chain.
- `defer cancel()` immediately after creating a context to release resources.
- Check `ctx.Done()` in every blocking `select`; surface `ctx.Err()` on cancellation.
- Use `ctx.Deadline()` to fail fast when you know your operation can't possibly finish in time.

**Don't:**
- Store optional parameters in a Context — that's abuse. Request-scoped data only.
- Store mutable data, complex types with methods, or data that drives algorithm behavior.

**Context value-key hygiene:**
- Define an unexported custom key type in your package.
- Export typed accessor functions (`UserID(ctx) string`) so callers never see the key.

```go
// Timeout + cancellation propagation through a call-graph.
func main() {
    var wg sync.WaitGroup
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    wg.Add(1)
    go func() {
        defer wg.Done()
        if err := printGreeting(ctx); err != nil {
            fmt.Printf("cannot print greeting: %v\n", err)
            cancel() // cancel the sibling too
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
func genGreeting(ctx context.Context) (string, error) {
    ctx, cancel := context.WithTimeout(ctx, 1*time.Second) // narrow the context
    defer cancel()
    switch locale, err := locale(ctx); {
    case err != nil:
        return "", err
    case locale == "EN/US":
        return "hello", nil
    }
    return "", fmt.Errorf("unsupported locale")
}
func locale(ctx context.Context) (string, error) {
    if deadline, ok := ctx.Deadline(); ok {
        if deadline.Sub(time.Now().Add(1*time.Minute)) <= 0 {
            return "", context.DeadlineExceeded // fail fast
        }
    }
    select {
    case <-ctx.Done():
        return "", ctx.Err()
    case <-time.After(1 * time.Minute):
    }
    return "EN/US", nil
}
// Output:
// cannot print greeting: context deadline exceeded
// cannot print farewell: context canceled
```
*Ref: Concurrency_in_Go.md — "The context Package"*

```go
// Type-safe context value accessors.
type ctxKey int
const (
    ctxUserID   ctxKey = iota
    ctxAuthToken
)
func UserID(c context.Context) string    { return c.Value(ctxUserID).(string) }
func AuthToken(c context.Context) string { return c.Value(ctxAuthToken).(string) }
func ProcessRequest(userID, authToken string) {
    ctx := context.WithValue(context.Background(), ctxUserID, userID)
    ctx = context.WithValue(ctx, ctxAuthToken, authToken)
    HandleResponse(ctx)
}
func HandleResponse(ctx context.Context) {
    fmt.Printf("handling response for %v (auth: %v)", UserID(ctx), AuthToken(ctx))
}
```
*Ref: Concurrency_in_Go.md — "The context Package" (values)*

---

### Error Propagation at Scale

**Principle:** In a large system, treat any error that escapes a module *without* being wrapped in that module's error type as a bug. Wrap at module boundaries; include what/where/when, a friendly user-facing message, a log ID, and a stack trace.

**Do:**
- Distinguish **bugs** (raw errors) from **known edge cases** (well-formed errors).
- At module boundaries, type-assert incoming errors and wrap them in your module's type.
- Display well-formed errors directly to users; show a generic friendly message for bugs and surface the log ID.

```go
type MyError struct {
    Inner      error
    Message    string
    StackTrace string
    Misc       map[string]interface{}
}
func wrapError(err error, messagef string, msgArgs ...interface{}) MyError {
    return MyError{
        Inner:       err,
        Message:     fmt.Sprintf(messagef, msgArgs...),
        StackTrace:  string(debug.Stack()),
        Misc:        make(map[string]interface{}),
    }
}
func (err MyError) Error() string { return err.Message }

// Module boundary wrapping.
type IntermediateErr struct{ error }
func runJob(id string) error {
    const jobBinPath = "/bad/job/binary"
    isExecutable, err := isGloballyExec(jobBinPath)
    if err != nil {
        return IntermediateErr{wrapError(
            err, "cannot run job %q: requisite binaries not available", id,
        )}
    } else if !isExecutable {
        return wrapError(nil, "cannot run job %q: requisite binaries are not executable", id)
    }
    return exec.Command(jobBinPath, "--id="+id).Run()
}

// User-facing handling: well-formed → show message; otherwise generic.
func handleError(key int, err error, message string) {
    log.SetPrefix(fmt.Sprintf("[logID: %v]: ", key))
    log.Printf("%#v", err)
    fmt.Printf("[%v] %v", key, message)
}
err := runJob("1")
if err != nil {
    msg := "There was an unexpected issue; please report this as a bug."
    if _, ok := err.(IntermediateErr); ok {
        msg = err.Error()
    }
    handleError(1, err, msg)
}
```
*Ref: Concurrency_in_Go.md — "Error Propagation"*

---

### Heartbeats — Liveliness & Deterministic Testing

**Principle:** A heartbeat is a goroutine's periodic "I'm alive (and possibly making progress)" signal. It lets you bound timeouts to the heartbeat interval instead of long arbitrary durations, and makes concurrent tests deterministic.

**Two flavors:**
- **Interval-based** — emit on a `time.Ticker`; consumed to detect an unhealthy goroutine within a known window.
- **Work-based** — emit one pulse *before* each unit of work; used to know the goroutine has started (great for tests).

**Do:**
- Always `default:` the heartbeat send so a missing listener doesn't block.
- Couple the heartbeat interval to the consumer's timeout (e.g., `pulseInterval = timeout/2`).
- For long-running goroutines or goroutines under test, expose a heartbeat channel.

```go
// Interval-based heartbeat with cancellation awareness.
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
        workGen := time.Tick(2 * pulseInterval)
        sendPulse := func() {
            select {
            case heartbeat <- struct{}{}:
            default:
            }
        }
        sendResult := func(r time.Time) {
            for {
                select {
                case <-done:        return
                case <-pulse:       sendPulse()
                case results <- r:  return
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

// Consumer: timeout coupled to pulse interval.
done := make(chan interface{})
time.AfterFunc(10*time.Second, func() { close(done) })
const timeout = 2 * time.Second
heartbeat, results := doWork(done, timeout/2)
for {
    select {
    case _, ok := <-heartbeat:
        if ok == false { return }
        fmt.Println("pulse")
    case r, ok := <-results:
        if ok == false { return }
        fmt.Printf("results %v\n", r.Second())
    case <-time.After(timeout):
        fmt.Println("worker goroutine is not healthy!")
        return
    }
}
```
*Ref: Concurrency_in_Go.md — "Heartbeats"*

```go
// Work-based heartbeat (pulse before each unit of work) — ideal for tests.
DoWork := func(done <-chan interface{}, nums ...int) (<-chan interface{}, <-chan int) {
    heartbeat := make(chan interface{}, 1) // buffer of 1: pulse survives even if no listener yet
    intStream := make(chan int)
    go func() {
        defer close(heartbeat)
        defer close(intStream)
        time.Sleep(2 * time.Second)
        for _, n := range nums {
            select {
            case heartbeat <- struct{}{}:
            default:
            }
            select {
            case <-done:           return
            case intStream <- n:
            }
        }
    }()
    return heartbeat, intStream
}

// Deterministic test: wait for first heartbeat, then range — no time.Sleep.
func TestDoWork_GeneratesAllNumbers(t *testing.T) {
    done := make(chan interface{})
    defer close(done)
    intSlice := []int{0, 1, 2, 3, 5}
    heartbeat, results := DoWork(done, intSlice...)
    <-heartbeat // wait until the goroutine has actually started doing work
    i := 0
    for r := range results {
        if expected := intSlice[i]; r != expected {
            t.Errorf("index %v: expected %v, but received %v,", i, expected, r)
        }
        i++
    }
}
```
*Ref: Concurrency_in_Go.md — "Heartbeats" (work-based heartbeat + deterministic test)*

---

### Replicated Requests

**Principle:** Fire the same request at multiple handlers (goroutines, processes, data centers) and accept the first response; cancel the rest. Trades resource usage for latency. Handlers must have genuinely different runtime conditions or the technique buys little.

```go
doWork := func(
    done <-chan interface{},
    id int,
    wg *sync.WaitGroup,
    result chan<- int,
) {
    started := time.Now()
    defer wg.Done()
    simulatedLoadTime := time.Duration(1+rand.Intn(5)) * time.Second
    select {
    case <-done:
    case <-time.After(simulatedLoadTime):
    }
    select {
    case <-done:
    case result <- id:
    }
    took := time.Since(started)
    if took < simulatedLoadTime {
        took = simulatedLoadTime
    }
    fmt.Printf("%v took %v\n", id, took)
}

done := make(chan interface{})
result := make(chan int)
var wg sync.WaitGroup
wg.Add(10)
for i := 0; i < 10; i++ {
    go doWork(done, i, &wg, result)
}
firstReturned := <-result
close(done) // cancel the 9 losers
wg.Wait()
fmt.Printf("Received an answer from #%v\n", firstReturned)
```
*Ref: Concurrency_in_Go.md — "Replicated Requests"*

---

### Rate Limiting — Token Bucket & Composed Limiters

**Principle:** Rate limits make performance and stability predictable, protect users from runaway bugs, and prevent death-spirals. Use the **token bucket** algorithm (depth `d` = burst capacity, rate `r` = steady-state replenish). Compose per-second, per-minute, and per-resource limiters via a `multiLimiter`.

**Do:**
- Always set limits even if you don't think they'll be hit — you can expand them in a controlled way later.
- Keep separate limiters for separate concerns (api, disk, network) and compose them per call.

```go
type RateLimiter interface {
    Wait(context.Context) error
    Limit() rate.Limit
}

// Compose limiters; sort so the most restrictive is checked first.
func MultiLimiter(limiters ...RateLimiter) *multiLimiter {
    byLimit := func(i, j int) bool {
        return limiters[i].Limit() < limiters[j].Limit()
    }
    sort.Slice(limiters, byLimit)
    return &multiLimiter{limiters: limiters}
}
type multiLimiter struct{ limiters []RateLimiter }
func (l *multiLimiter) Wait(ctx context.Context) error {
    for _, l := range l.limiters {
        if err := l.Wait(ctx); err != nil {
            return err
        }
    }
    return nil
}
func (l *multiLimiter) Limit() rate.Limit { return l.limiters[0].Limit() }

func Per(eventCount int, duration time.Duration) rate.Limit {
    return rate.Every(duration / time.Duration(eventCount))
}

// Per-second AND per-minute limits, plus per-resource limits.
func Open() *APIConnection {
    return &APIConnection{
        apiLimit: MultiLimiter(
            rate.NewLimiter(Per(2, time.Second), 2),
            rate.NewLimiter(Per(10, time.Minute), 10),
        ),
        diskLimit:    MultiLimiter(rate.NewLimiter(rate.Limit(1), 1)),
        networkLimit: MultiLimiter(rate.NewLimiter(Per(3, time.Second), 3)),
    }
}
type APIConnection struct {
    networkLimit, diskLimit, apiLimit RateLimiter
}
func (a *APIConnection) ReadFile(ctx context.Context) error {
    return MultiLimiter(a.apiLimit, a.diskLimit).Wait(ctx)
}
func (a *APIConnection) ResolveAddress(ctx context.Context) error {
    return MultiLimiter(a.apiLimit, a.networkLimit).Wait(ctx)
}
```
*Ref: Concurrency_in_Go.md — "Rate Limiting"*

---

### Healing Unhealthy Goroutines (Steward / Ward)

**Principle:** In long-running daemons, restart goroutines that become stuck. A *steward* monitors a *ward*'s heartbeat; if no pulse arrives within the timeout, it closes the ward's done channel and starts a fresh ward. Stewards are themselves monitorable (they return a `startGoroutineFn`).

```go
type startGoroutineFn func(
    done <-chan interface{},
    pulseInterval time.Duration,
) (heartbeat <-chan interface{})

newSteward := func(timeout time.Duration, startGoroutine startGoroutineFn) startGoroutineFn {
    return func(done <-chan interface{}, pulseInterval time.Duration) <-chan interface{} {
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

// Ward pattern using closures + bridge so a restarted ward resumes a single output stream.
doWorkFn := func(
    done <-chan interface{},
    intList ...int,
) (startGoroutineFn, <-chan interface{}) {
    intChanStream := make(chan (<-chan interface{}))
    intStream := bridge(done, intChanStream)
    doWork := func(done <-chan interface{}, pulseInterval time.Duration) <-chan interface{} {
        intStream := make(chan interface{})
        heartbeat := make(chan interface{})
        go func() {
            defer close(intStream)
            select {
            case intChanStream <- intStream:
            case <-done:
                return
            }
            pulse := time.Tick(pulseInterval)
            for {
            valueLoop:
                for _, intVal := range intList {
                    if intVal < 0 {
                        log.Printf("negative value: %v\n", intVal)
                        return // simulates an unhealthy ward
                    }
                    for {
                        select {
                        case <-pulse:
                            select {
                            case heartbeat <- struct{}{}:
                            default:
                            }
                        case intStream <- intVal:
                            continue valueLoop
                        case <-done:
                            return
                        }
                    }
                }
            }
        }()
        return heartbeat
    }
    return doWork, intStream
}
```
*Ref: Concurrency_in_Go.md — "Healing Unhealthy Goroutines"*

---

### Timeouts & Cancellation — Designing for Preemption

**Principle:** Concurrency that *can be canceled* must also be *preemptable*. Define the maximum non-preemptable window and ensure every operation longer than that is broken into preemptable pieces (pass `done` deeper).

**Reasons to support timeouts:** system saturation, stale data, deadlock prevention.
**Reasons to be canceled:** timeout, user intervention, parent cancellation, replicated requests.

**Do:**
- Modify shared state in as few writes as possible (build intermediate results in memory, then commit once) so cancellation rollback is trivial.
- Design with timeouts/cancellation from the start — bolting them on later is like "adding eggs to a baked cake."

**Don't:**
- Let `reallyLongCalculation` run unpreemptably — thread `done` all the way down.

```go
// WRONG: writes to state 3 times; cancellation may leave partial state.
result := add(1, 2, 3)
writeTallyToState(result)
result = add(result, 4, 5, 6)
writeTallyToState(result)
result = add(result, 7, 8, 9)
writeTallyToState(result)

// RIGHT: build up, then commit once — tiny rollback surface.
result := add(1, 2, 3, 4, 5, 6, 7, 8, 9)
writeTallyToState(result)

// Preemptable long calculation: pass done down to every sub-call.
reallyLongCalculation := func(
    done <-chan interface{},
    value interface{},
) interface{} {
    intermediateResult := longCalculation(done, value)
    return longCalculation(done, intermediateResult)
}
```
*Ref: Concurrency_in_Go.md — "Timeouts and Cancellation"*

---

### The GOMAXPROCS Lever

**Principle:** Controls the number of OS threads hosting goroutine work queues. Default since Go 1.5 is `runtime.NumCPU()`. Tweaking is usually counterproductive; the runtime knows best.

**When to tweak:** temporarily crank it above CPU count to surface race conditions faster in a flaky test suite.

```go
// Legacy snippet (pre-Go 1.5); no longer needed.
runtime.GOMAXPROCS(runtime.NumCPU())
```
*Ref: Concurrency_in_Go.md — "The GOMAXPROCS Lever"*

---

### Work-Stealing Scheduler (Runtime Internals)

**Principle:** Go's M:N scheduler gives each OS thread a deque of goroutines. Threads push forks onto the tail, run/pop from the tail at join points, and steal from the *head* of another thread's deque when idle — preserving cache locality for the most-recently-forked tasks.

**Rules:**
1. At a fork, append the task to the tail of the current thread's deque.
2. If idle, steal from the head of a random thread's deque.
3. At an unrealized join, pop work off your own tail.
4. If your deque is empty, stall at the join or steal from another head.

**Implication:** Don't worry about how many goroutines you create — the scheduler balances them; write code that *forks* naturally and *joins* cleanly.

*Ref: Concurrency_in_Go.md — "Work Stealing"*

---

### Testing Concurrent Code

**Principle:** Concurrent code is nondeterministic by default; you must introduce determinism (heartbeats, channel-based synchronization) or you'll end up ignoring flaky tests — and then the whole suite loses meaning.

**Do:**
- Run `go test -race` in CI — it catches data races invisible to code review.
- Use the work-based heartbeat (`<-heartbeat` before assertions) to deterministically know the goroutine has started.
- Use `pprof` (`go tool pprof cpu.prof`, `go tool pprof mem.prof`) and `runtime.NumGoroutine()` / `pprof.Lookup("goroutine")` to inspect goroutine leaks.
- Prefer `time.After` inside `select` for test timeouts over `time.Sleep`.

**Don't:**
- Write tests that depend on timing — they become heisenbugs.
- Crank up `time.Sleep` to make a test "more reliable" — it just slows the suite.

```go
// BAD nondeterministic test — passes or fails based on scheduling.
func TestDoWork_GeneratesAllNumbers(t *testing.T) {
    done := make(chan interface{})
    defer close(done)
    intSlice := []int{0, 1, 2, 3, 5}
    _, results := DoWork(done, intSlice...)
    for i, expected := range intSlice {
        select {
        case r := <-results:
            if r != expected { t.Errorf("...") }
        case <-time.After(1 * time.Second):
            t.Fatal("test timed out")
        }
    }
}

// GOOD deterministic test — block on first heartbeat, then range.
func TestDoWork_GeneratesAllNumbers(t *testing.T) {
    done := make(chan interface{})
    defer close(done)
    intSlice := []int{0, 1, 2, 3, 5}
    heartbeat, results := DoWork(done, intSlice...)
    <-heartbeat
    i := 0
    for r := range results {
        if expected := intSlice[i]; r != expected {
            t.Errorf("index %v: expected %v, but received %v,", i, expected, r)
        }
        i++
    }
}
```
*Ref: Concurrency_in_Go.md — "Heartbeats" (testing section)*

```go
// Race detector & profiling tools (Appendix).
//   go test -race                 detects data races at runtime
//   go build -race                ship a race-instrumented binary
//   go tool pprof cpu.prof        CPU profile
//   go tool pprof mem.prof        memory profile
//   runtime.NumGoroutine()        count live goroutines (leak detection)
//   pprof.Lookup("goroutine")     dump all goroutine stacks
```
*Ref: Concurrency_in_Go.md — "Appendix" / Summary*

---

## Anti-Patterns & Common Mistakes

- **Sleep-as-synchronization:** `time.Sleep` after `go f()` to "wait" — it's a race, not a join. → *fix:* use `sync.WaitGroup` or a channel.
- **Closure capture of loop variables:** goroutines all see the last value. → *fix:* pass the variable as a parameter.
- **Goroutine leak via nil channel:** `for s := range nilChan` blocks forever. → *fix:* pass a `done` channel and `select` on it.
- **Abandoned goroutines:** the GC won't collect them. → *fix:* every goroutine needs a termination path; the spawner owns stopping it.
- **Writing to / closing a channel you don't own:** panics on closed channel, double-close, or nil-close. → *fix:* the owner instantiates, writes, closes; consumers get `<-chan`.
- **Mutex without `defer Unlock`:** an early return or panic deadlocks. → *fix:* `defer m.Unlock()` immediately after `Lock`.
- **Buffered channels everywhere "for performance":** hides deadlocks, doesn't speed up total runtime (Little's Law). → *fix:* buffer only at the pipeline entrance or where batching helps.
- **Greedy locking:** holding a lock across far more than the critical section starves peers. → *fix:* shrink the section first; widen only after profiling.
- **Errors swallowed in goroutines:** printing inside the goroutine loses system context. → *fix:* couple error+result in a `Result` type, let the parent decide.
- **Passing two functions to one `sync.Once`:** only the first runs. → *fix:* wrap `Once` + function in a small lexical scope.
- **Closing a `done` channel from a child:** children can't cancel parents — `Context` is immutable from below. → *fix:* use `context.WithCancel` from the parent.
- **Storing `context.Context` in a struct:** breaks the call-graph flow. → *fix:* always pass as the first argument.
- **Relying on case ordering in `select`:** cases are chosen randomly when multiple are ready. → *fix:* don't write logic that depends on priority among ready cases.
- **Premature `GOMAXPROCS` tuning:** usually net-negative; tied to specific hardware/Go version. → *fix:* leave it at default except for race-surfacing in tests.

---

## Decision Heuristics / Checklists

**Channel vs. Mutex (Ch. 2 decision tree):**
1. Transferring ownership of data? → **channel**
2. Guarding internal state of a struct? → **mutex** (keep internal)
3. Coordinating multiple pieces of logic? → **channels** (composable via `select`)
4. Profiled performance-critical hot path? → **mutex** (channels use mutexes internally)

**Should I fan out a pipeline stage?**
- [ ] Order-independent (no reliance on prior values)?
- [ ] Slow enough to matter?
- If both yes → spin up N copies and fan-in.

**Should I add a queue/buffer?**
- [ ] At the pipeline entrance (decouple producer/consumer, break death-spiral)?
- [ ] In a stage where batching improves efficiency (chunked writes, transactions)?
- Otherwise → no; it won't reduce total runtime.

**Is my goroutine leak-proof?**
- [ ] Takes a `done <-chan interface{}` as first arg?
- [ ] Every channel read/write shares a `select` with `<-done`?
- [ ] `defer close(outStream)` at the top of the goroutine?
- [ ] Caller closes `done` (or `cancel()`) on completion/error/timeout?

**Is my concurrent test deterministic?**
- [ ] Uses a heartbeat (`<-heartbeat`) before assertions instead of `time.Sleep`?
- [ ] Wrapped in `go test -race` in CI?
- [ ] Uses `time.After` in a `select` as a *timeout*, not a synchronization primitive?

**Is my error handling concurrent-safe?**
- [ ] Errors coupled with results in a single type on the channel?
- [ ] Module boundaries wrap incoming errors into the module's type?
- [ ] User-facing code distinguishes well-formed errors from bugs?

**Context usage checklist:**
- [ ] First argument, never stored in a struct?
- [ ] `defer cancel()` after every `With*` call?
- [ ] Values are request-scoped, immutable, simple, data-only (no methods)?
- [ ] Custom unexported key type + typed accessor functions?

---

## Key Takeaways

1. **Think in CSP, not threads.** Model programs as processes communicating through channels; let the runtime schedule.
2. **Goroutines are cheap — use them freely.** Don't pool, don't pre-optimize the count. The work-stealing scheduler balances them.
3. **Channels are the primary communication mechanism.** They combine communication and synchronization and compose via `select`.
4. **Every goroutine must have a termination path.** Pass a `done` channel (or `context.Context`) and have a convention that the spawner owns cancellation.
5. **Channels have owners.** The owner instantiates, writes, closes, and exposes a read-only view. Consumers handle blocking and closure.
6. **`select` is the multiplexer.** Random selection keeps things fair; `time.After` adds timeouts; `default` makes it non-blocking.
7. **Pipelines compose concurrent stages.** Each stage: `done` first arg, `defer close(out)`, range over input, select on send.
8. **Fan-out for parallelism, fan-in for aggregation.** Criteria: order-independent and slow.
9. **Use the race detector in all tests.** `go test -race` catches bugs invisible to review.
10. **Confinement eliminates synchronization.** Prefer lexical confinement (compiler-enforced) over ad hoc (convention).
11. **Errors are first-class citizens.** Couple them with results; wrap them at module boundaries; distinguish bugs from known edge cases.
12. **`context.Context` flows through the call-graph.** Cancellation, deadlines, and request-scoped values — never store it in a struct.
13. **Heartbeats make concurrency observable and tests deterministic.** Block on the first heartbeat instead of `time.Sleep`.
14. **Rate-limit by default.** Token bucket; compose multi-limiters per second/minute/resource.
15. **Queuing decouples stages but never speeds total runtime.** Little's Law (`L = λW`) governs throughput; the pipeline is only as fast as its slowest stage.
16. **Heal stuck goroutines with stewards.** Monitor heartbeats, restart wards; the steward itself is monitorable.

---

## Cross-References
- Related: [[../Grokking_Concurrency.md]] — language-agnostic theory (decomposition, Amdahl/Gustafson, deadlocks, producer-consumer, readers-writer) that underpins these Go idioms.
- Topic index: [[../INDEX.md]]
