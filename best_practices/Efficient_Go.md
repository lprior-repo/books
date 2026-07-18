# Efficient Go — Data-Driven Performance Optimization

**Author:** Bartłomiej Płotka
**Topic tags:** `#performance` `#testing` `#general` `#profiling` `#benchmarking`
**Language focus:** Go-first, 8/11 chapters language-agnostic
**Sources:** `markdown_output/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md` · `summaries/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md`

## TL;DR
A pragmatic, data-driven handbook for performance: profiler-led optimization (pprof, flame, trace), disciplined benchmarking (goleak, `b.Run`, `benchstat`), memory and GC management (allocation budgets, arenas, `GOMEMLIMIT`), coordination-free sharding, channel drainage, the RAER requirements framework, TFBO testing, and resource-leak detection (goleak.VerifyNone). Apply any time you optimise code in any language — 80 % of the methods are universal.

---

## Best Practices by Topic

### What Efficiency Actually Means

**Principle:** Performance = `accuracy × efficiency × speed`. The book renames "performance" to "efficiency" because most teams conflate the three and mis-prioritise.

**Do:**
- Be explicit when you say "performance" — speed, memory, accuracy, energy?
- Optimise one axis at a time and measure.
- Treat *efficiency* as a first-class software quality, alongside correctness and readability.

**Don't:**
- Don't optimise for one axis at the cost of another without telling stakeholders.

*Ref: Efficient_Go.md — "Behind Performance", "Why I Wrote This Book"*

---

### The Five Efficiency Misconceptions

1. **"Optimised code is unreadable."** Wrong — pre-allocation and avoiding redundant calls are often *more* readable.
2. **"Optimisation can wait."** Premature pessimisation accumulates.
3. **"Hardware is cheap, just buy more."** Cloud bills disagree.
4. **"We can optimise later."** Architectural choices are hard to reverse.
5. **"Premature optimisation is the root of all evil."** Knuth's actual quote is about hot paths, not all code.

**Do:**
- Distinguish *premature pessimisation* (avoid free wins) from *premature optimisation* (micro-optimisation on cold paths).
- Apply obvious efficiency improvements (like pre-allocation) by default.

*Ref: Efficient_Go.md — "Common Efficiency Misconceptions"*

---

### Readability and Efficiency Coexist

**Principle:** Calling a getter three times is both less readable AND less efficient. The fix makes the code clearer too.

**Do:**
```go
// Idiomatic, readable, faster
func FailureRatio(reports ReportGetter) float64 {
    got := reports.Get()
    if len(got) == 0 {
        return 0
    }
    var sum float64
    for _, report := range got {
        if report.Error() != nil {
            sum++
        }
    }
    return sum / float64(len(got))
}
```

**Don't:**
- Don't write `reports.Get()` three times — it's slower, race-prone, AND less readable.

*Ref: Efficient_Go.md — "Optimized Code Is Not Readable", "Code after optimization can be more readable"*

---

### Pre-Allocate If You Can

**Principle:** `make([]T, 0, n)` is one of the cheapest wins in Go. It removes growth re-allocations AND hints at intent.

**Do:**
```go
// Good
func createSlice(n int) []string {
    slice := make([]string, 0, n*7)
    for i := 0; i < n; i++ {
        slice = append(slice, "I", "am", "going", "to", "take", "some", "space")
    }
    return slice
}
```

**Don't:**
- Don't `var s []T` and append in a hot loop — every growth copies.

*Ref: Efficient_Go.md — "Pre-Allocate If You Can"*

---

### The Pragmatic Performance Mindset

**Principle:** Measure first, then optimise. Use simple observability, repeat experiments, share results.

**Do:**
- Set explicit efficiency goals before optimising (e.g., "p99 < 50 ms").
- Measure on production-like data and load.
- Re-measure after each change.

**Don't:**
- Don't optimise without a goal — you'll work on the wrong thing.

*Ref: Efficient_Go.md — "The Key to Pragmatic Code Performance"*

---

### Optimization Design Levels (5 Levels)

| Level | Examples |
|-------|----------|
| 1. Algorithm & data structures | Better sort, hash map instead of linear search |
| 2. API & contracts | Pagination, batch endpoints |
| 3. Runtime config | GC tuning, GOGC |
| 4. Architecture | Caching, async, queues |
| 5. System | Hardware, network, OS tuning |

**Do:**
- Always look at Level 1–4 before Level 5 (hardware).
- Pick the cheapest level that meets your goal.

**Don't:**
- Don't buy faster hardware to fix an O(n²) algorithm.

*Ref: Efficient_Go.md — "Optimization Design Levels"*

---

### RAER — Requirements And Expected Results

**Principle:** RAER entries document the efficiency goal before you code: latency, throughput, accuracy, memory, error rate, blast radius.

**Do:**
- Write a RAER entry for every non-trivial feature:
  ```
  Goal: <business outcome>
  Latency: p99 < 100 ms
  Throughput: 10k req/s
  Memory: < 4 GiB per pod
  Error budget: 0.1 %
  Workload: 80 % reads, 20 % writes, keys uniformly distributed
  ```
- Update RAER after each optimisation step.

**Don't:**
- Don't accept "make it fast" as a requirement — quantify it.

*Ref: Efficient_Go.md — "RAER — Requirements and Expected Results"*

---

### The Efficiency-Aware Development Flow

1. Test functionality first.
2. Do we pass functional tests?
3. If not, fix or design.
4. Efficiency assessment against RAER.
5. Are we within RAERs?
6. Find the main bottleneck (profile).
7. Choose optimisation level.
8. Optimise.
9. Re-measure.
10. Release and enjoy.

**Do:**
- Follow the flow on every feature.
- Don't skip the profiling step — gut feel is usually wrong.

*Ref: Efficient_Go.md — "Efficiency-Aware Development Flow"*

---

### Performance = (accuracy × efficiency × speed)

**Principle:** Any axis can be improved without sacrificing the others — up to a point.

**Do:**
- Pick the axis you care about for each metric.
- Document the trade-off you made.

**Don't:**
- Don't call something "fast" without saying fast at what.

*Ref: Efficient_Go.md — "Behind Performance"*

---

### CPU vs Memory: Pick Your Bottleneck

**Principle:** Optimising for memory often helps CPU (less GC). Optimising for CPU often trades memory (caching). Decide based on data.

**Do:**
- Profile CPU and memory separately.
- If memory-bound: reduce allocations.
- If CPU-bound: reduce work or parallelise.

*Ref: Efficient_Go.md — "How Go Uses the CPU Resource", "How Go Uses Memory Resource"*

---

### Goroutine Scheduling and `GOMAXPROCS`

**Principle:** `GOMAXPROCS` is the number of OS threads that can execute user-level Go code simultaneously. Default = `NumCPU()` since Go 1.5.

**Do:**
- Leave default unless you have evidence it's wrong.
- For pure-CPU workloads, set to `NumCPU()`.
- For latency-sensitive mixed workloads, lower to limit GC/mark assist contention.

**Don't:**
- Don't crank `GOMAXPROCS` past `NumCPU()` — won't help CPU-bound code.

*Ref: Efficient_Go.md — "How Go Uses the CPU Resource"*

---

### Memory Model: Stack vs Heap

**Principle:** Each goroutine starts with a small stack (2 KiB) that grows as needed. Heap is shared, GC-managed.

**Do:**
- Use `go build -gcflags="-m=2"` to see escape analysis output.
- Keep hot-loop values stack-allocated.

**Don't:**
- Don't allocate in loops when a stack value would do.

*Ref: Efficient_Go.md — "Stack and heap allocation", "Escape analysis"*

---

### Memory Arenas (`arena` package, Go 1.20+)

**Principle:** Arenas let you allocate a batch of objects and free them all at once. The compiler can pack them tighter than the GC heap.

**Do:**
- Use arenas for request-scoped processing where lifetimes are bounded.
- Document that pointers cannot outlive `arena.Free()`.

**Don't:**
- Don't store arena pointers in long-lived structures — use-after-free risk.

*Ref: Efficient_Go.md — "Memory arenas"*

---

### Allocation Reduction Tactics

**Do:**
- Pre-size slices/maps with `make(..., 0, n)`.
- Reuse buffers with `sync.Pool`.
- Stream large data; don't read whole files into memory.
- Pass small structs by value, large ones by pointer.
- Use `[]byte` instead of `string` for I/O buffers when you'll mutate.

**Don't:**
- Don't `fmt.Sprintf` in hot paths — it allocates.
- Don't concatenate strings with `+` in loops — use `strings.Builder`.

*Ref: Efficient_Go.md — "Memory allocations", "Common pitfalls"*

---

### GC Pressure: Reducing `NumGC` Cycles

**Principle:** Each GC cycle costs CPU proportional to live heap. Reducing allocation rate keeps the heap small and the GC quiet.

**Do:**
- Use `GOMEMLIMIT` to soft-cap memory and let GC work harder under pressure.
- Use `GOGC=200` for higher throughput on memory-rich machines.
- Profile `mem.NumGC` over time.

**Don't:**
- Don't set `GOMEMLIMIT` above the container's limit — OOMKilled.

*Ref: Efficient_Go.md — "GC pacer", "GOMEMLIMIT", "Memory ballast"*

---

### Memory Ballast for Steady-State GC

**Principle:** Allocating a large never-touched byte slice at startup gives the GC a "fudge factor" — it triggers fewer cycles at the same heap size.

**Do:**
- Use ~1 GiB on memory-rich hosts.
- Document why it's there and how to tune.

**Don't:**
- Don't use ballast on memory-constrained hosts (< 2 GiB).

**Code:**
```go
var ballast = make([]byte, 1<<30) // 1 GiB
```

*Ref: Efficient_Go.md — "Memory ballast"*

---

### Observability: Logs, Metrics, Traces

**Principle:** You can't optimise what you can't observe. Logs (events), metrics (aggregates), traces (request paths) are the three pillars.

**Do:**
- Use **structured logs** (`slog` JSON) with `trace_id` and `request_id`.
- Instrument **RED metrics**: Rate, Errors, Duration.
- Use **distributed tracing** with OpenTelemetry for cross-service visibility.

**Don't:**
- Don't mix three observability backends — pick one vendor-neutral standard.

*Ref: Efficient_Go.md — "Efficiency Observability", "Logs, Metrics, Traces"*

---

### CPU Profiling with `pprof`

**Principle:** `pprof` samples the call stack at 100 Hz. The output shows which functions consume CPU.

**Do:**
- Profile with realistic load.
- View in `go tool pprof -http=:8080 cpu.prof`.
- Read `flat` (time in this fn) and `cum` (time in this fn + callees).

**Don't:**
- Don't profile an idle process — zero samples, useless output.

**Code:**
```go
import (
    "os"
    "runtime/pprof"
)

f, _ := os.Create("cpu.prof")
defer f.Close()
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... do work ...
```

*Ref: Efficient_Go.md — "CPU profiling", "pprof"*

---

### Memory Profiling

**Principle:** The heap profile (`heap` profile) shows where allocations happen. Sample size matters.

**Do:**
- `runtime.MemProfileRate = 1` for accurate small allocations (1 → every alloc sampled, slow).
- Default `512 * 1024` for production-safe profiling.

**Don't:**
- Don't try to attribute allocations to a specific line without `-lineprecision`.

*Ref: Efficient_Go.md — "Memory profiling", "pprof"*

---

### Flame Graphs

**Principle:** A flame graph is a stack profile rendered as a tree of bars. Wide bars = hot paths. Each row is a function, each column is a sample.

**Do:**
- Generate with `pprof -http` or Brendan Gregg's `flamegraph.pl`.
- Compare before/after with `pprof -base old.pprof new.pprof`.

**Don't:**
- Don't micro-optimise narrow bars (< 1 % of total).

*Ref: Efficient_Go.md — "Profiling"*

---

### Execution Tracing with `go tool trace`

**Principle:** `trace` shows goroutine state transitions, GC events, syscalls — useful when pprof says "where" and you want to know "why it's waiting".

**Do:**
- `trace.Start(os.Stdout); defer trace.Stop()`.
- Open in `go tool trace` for a timeline view.
- Look for long "Syscall" bars or "Stop-the-World" GC pauses.

**Don't:**
- Don't trace for long — file size grows fast.

*Ref: Efficient_Go.md — "trace"*

---

### `pprof` Endpoints in Production

**Do:**
- Mount `net/http/pprof` on `localhost:6060`, behind a sidecar or auth.
- Restrict via firewall.

**Don't:**
- Don't expose `/debug/pprof` to the public internet — leaks goroutine stacks and memory.

**Code:**
```go
import (
    "net/http"
    _ "net/http/pprof"
)

go http.ListenAndServe("localhost:6060", nil)
```

*Ref: Efficient_Go.md — "pprof", "fgprof"*

---

### Microbenchmarks with `testing.B`

**Principle:** A microbenchmark measures one operation. Use them to compare implementations of the same function.

**Do:**
```go
func BenchmarkSum(b *testing.B) {
    data := make([]int, 1024)
    for i := range data { data[i] = i }

    b.ResetTimer()
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        _ = Sum(data)
    }
}
```

**Don't:**
- Don't benchmark code that calls `time.Sleep`, `os.Exit`, or external services.
- Don't compare microbenchmarks across machines.

*Ref: Efficient_Go.md — "Microbenchmarks", "Benchmarking"*

---

### Sub-Benchmarks for Configuration Matrices

**Do:**
```go
func BenchmarkSum(b *testing.B) {
    for _, n := range []int{100, 1000, 10000} {
        b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
            data := make([]int, n)
            for i := 0; i < b.N; i++ {
                _ = Sum(data)
            }
        })
    }
}
```

*Ref: Efficient_Go.md — "Sub-benchmarks"*

---

### `benchstat` — Statistically Robust Comparison

**Principle:** `benchstat` reads multiple runs of `go test -bench` and produces a confidence interval comparison.

**Do:**
- Run `-bench` ≥ 10 times: `go test -bench=. -count=10 > old.txt`.
- Change code, repeat: `go test -bench=. -count=10 > new.txt`.
- `benchstat old.txt new.txt` shows p value + delta.

**Don't:**
- Don't claim "X% faster" from a single run — benchstat will tell you it's noise.

*Ref: Efficient_Go.md — "benchstat", "Benchmarking"*

---

### Stable Benchmark Environment

**Do:**
- Pin CPU frequency (Linux `performance` governor).
- Close other applications.
- Use `-cpu` to pick a specific GOMAXPROCS.
- Run `go test -bench=. -count=N -benchtime=3s` for stable results.

**Don't:**
- Don't compare across machines, kernel versions, or after `go mod upgrade`.

*Ref: Efficient_Go.md — "Benchmarking discipline", "Stability best practices"*

---

### Parallel Benchmarks with `b.RunParallel`

**Do:**
```go
func BenchmarkParallelSum(b *testing.B) {
    data := make([]int, 1024)
    b.ResetTimer()
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            _ = Sum(data)
        }
    })
}
```

*Ref: Efficient_Go.md — "Parallel benchmarks"*

---

### Profiling Contention: `block` and `mutex` Profiles

**Principle:** The `block` profile shows goroutine blocking on chan sends, mutexes, `time.Sleep`. The `mutex` profile shows specifically mutex contention.

**Do:**
- Enable with `runtime.SetBlockProfileRate(1)` and `runtime.SetMutexProfileFraction(1)`.
- Use `go tool pprof /debug/pprof/block` and `/mutex`.

**Don't:**
- Don't run with rate=1 in production for long — overhead is real.

*Ref: Efficient_Go.md — "Block profile", "Mutex profile"*

---

### Asymptotic Complexity: Big-O Reality Check

**Principle:** Most real systems are not bottlenecked by Big-O — they're bottlenecked by constant factors, GC, locks, or I/O. Use Big-O to rule out algorithmic mistakes.

**Do:**
- Verify the algorithmic class first (O(n) vs O(n²)).
- Then measure constant factors.

**Don't:**
- Don't trade Big-O for constant factor unless the constant is huge.

*Ref: Efficient_Go.md — "Asymptotic Complexity with Big O Notation"*

---

### Measurement Beats Theory

**Principle:** Benchmarks, profilers, and tracing beat theoretical reasoning every time.

**Do:**
- Profile before optimising.
- Re-profile after each change.
- Share flame graphs in PRs.

**Don't:**
- Don't ship an "optimisation" without a before/after benchmark.

*Ref: Efficient_Go.md — "Measurement", "Benchmarks Lie"*

---

### Reproducing Production Workloads

**Principle:** A benchmark that doesn't match production traffic is fiction.

**Do:**
- Record production traffic patterns (key distribution, request size distribution).
- Replay with `vegeta`, `wrk`, `hey`, or a custom load generator.
- Profile under replay, not synthetic.

**Don't:**
- Don't benchmark against a single user — concurrency issues won't show.

*Ref: Efficient_Go.md — "Reproducing Production"*

---

### Performance Non-Determinism

**Principle:** Modern systems have nondeterministic scheduling, GC, kernel interrupts. Variance is the rule.

**Do:**
- Run benchmarks multiple times; report min/median/95th percentile.
- Use `benchstat` for statistical comparison.
- Disable ASLR, turbo boost, and other features only when you want minimal noise.

**Don't:**
- Don't cherry-pick the best run — it will lie.

*Ref: Efficient_Go.md — "Performance Nondeterminism"*

---

### Caching Strategies

**Principle:** Cache hit = free; cache miss = full cost. Aim for high hit rate, low staleness.

**Do:**
- Cache read-mostly data at the edge (CDN, reverse proxy).
- Cache expensive computations (memoization) inside processes.
- Use TTL for time-sensitive data.
- Use bounded LRU/LFU caches to prevent OOM.

**Don't:**
- Don't cache write-heavy data — contention kills throughput.
- Don't cache without invalidation — stale data is worse than no cache.

*Ref: Efficient_Go.md — "Optimization Examples", "Caching strategies"*

---

### Resource Leak Detection

**Principle:** Long-running goroutines, file descriptors, sockets, and timers all leak. Detect them in tests with `goleak.VerifyNone`.

**Do:**
- Add `goleak.VerifyNone(t)` to every package's `TestMain`.
- Use `defer` for all resource cleanup.
- Always close HTTP response bodies.

**Don't:**
- Don't `go func() { ... }()` without a termination path.

**Code:**
```go
import "go.uber.org/goleak"

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

*Ref: Efficient_Go.md — "Resource leaks", "goleak"*

---

### Goroutine Leak Patterns

- Blocked `<-ch` with no sender.
- Blocked channel send with no receiver.
- `time.After` in a loop without `Stop()`.
- `WaitGroup.Add(n)` where `n` exceeds `Done()` calls.
- Context cancelled but goroutine didn't `select` on it.

**Do:**
- Always pair a goroutine with an exit channel or context.

*Ref: Efficient_Go.md — "Optimization Patterns"*

---

### `defer` for Cleanup Discipline

**Do:**
```go
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil { return err }
    defer f.Close()
    // ...
}
```

**Don't:**
- Don't `defer` in million-iteration loops — wrap each iteration in a helper.

*Ref: Efficient_Go.md — "defer patterns"*

---

### Closing HTTP Response Bodies Properly

**Do:**
```go
resp, err := http.Get(url)
if err != nil { return err }
defer func() {
    io.Copy(io.Discard, resp.Body) // drain for connection reuse
    resp.Body.Close()
}()
```

**Don't:**
- Don't `resp.Body.Close()` without draining — the connection can't be reused.

*Ref: Efficient_Go.md — "HTTP client efficiency", "Closing http bodies"*

---

### `sync.Pool` for Hot Path Buffers

**Do:**
```go
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func handle(w http.ResponseWriter, r *http.Request) {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    defer bufPool.Put(buf)
    // ...
}
```

**Don't:**
- Don't pool items that must survive across GC cycles — pool is cleared.
- Don't pool tiny objects — `New` overhead exceeds the gain.

*Ref: Efficient_Go.md — "sync.Pool patterns"*

---

### Coordination-Free Sharding

**Principle:** Shard a map by `hash(key) % N` so each shard has its own lock. Removes contention on a single global lock.

**Do:**
- Pick `N` ≈ 2× NumCPU or until benchmark stops improving.
- Use `xxhash` or `fnv` for cheap hashing.

**Don't:**
- Don't shard without measuring — a small map may not need it.

**Code:**
```go
type ShardedMap[K comparable, V any] struct {
    shards [N]struct {
        sync.RWMutex
        m map[K]V
    }
}

func (s *ShardedMap[K, V]) shardFor(k K) *struct{...} {
    h := hash(k)
    return &s.shards[h%N]
}
```

*Ref: Efficient_Go.md — "Optimization Examples", "Sharding"*

---

### Channel Drainage on Cancellation

**Do:**
```go
for {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case v, ok := <-ch:
        if !ok { return nil }
        process(v)
    }
}
```

**Don't:**
- Don't `for v := range ch { ... }` without a context path — leaks on shutdown.

*Ref: Efficient_Go.md — "Channel drainage"*

---

### Buffered Channels for Backpressure

**Principle:** A buffered channel provides backpressure: producers slow down when consumers can't keep up.

**Do:**
- Size buffer to absorb normal bursts.
- Combine with `select { case c <- v: default: drop }` for non-blocking producers.

**Don't:**
- Don't size buffer arbitrarily — measure.

*Ref: Efficient_Go.md — "Channel patterns"*

---

### RAER Entry Format

```
Title: <feature or task>
Latency:
  p50: <ms>
  p99: <ms>
Throughput: <req/s or items/s>
Memory:
  RSS: <MiB per process>
  Allocs/op: <count>
Error rate: <fraction>
Workload: <description of inputs>
Blast radius: <max users/data affected on failure>
```

**Do:**
- Write the RAER before implementing the feature.
- Update it as you measure.

*Ref: Efficient_Go.md — "RAER — Requirements and Expected Results"*

---

### Testing for Functional Correctness Before Efficiency

**Principle:** Don't optimise code that doesn't pass functional tests.

**Do:**
- Write functional tests first.
- Confirm green before measuring performance.

**Don't:**
- Don't claim "X% faster" for code that doesn't even work.

*Ref: Efficient_Go.md — "Efficiency-Aware Development Flow"*

---

### TFBO — Test Functional, Benchmark Optimisation

**Principle:** The TFBO cycle: write functional tests, run benchmark, profile, optimise, re-run benchmark to confirm.

**Do:**
- Pair every benchmark with a test.
- Run both on every change.

*Ref: Efficient_Go.md — "Optimization Examples", "TFBO"*

---

### `golangci-lint` for Catch-All Static Analysis

**Do:**
- Configure for `govet`, `staticcheck`, `errcheck`, `ineffassign`, `unused`.
- Run in CI.

**Don't:**
- Don't disable rules globally — fix the warnings.

*Ref: Efficient_Go.md — "Static analysis"*

---

### Testing the Test Code with `goleak.VerifyNone`

**Principle:** Goroutine leaks in tests become production leaks. Verify in tests.

**Do:**
```go
func TestSomething(t *testing.T) {
    defer goleak.VerifyNone(t)
    // ...
}
```

**Don't:**
- Don't ignore goroutines left running after a test — they accumulate across the test suite.

*Ref: Efficient_Go.md — "goleak.VerifyNone"*

---

### Resource Leak Detection Patterns

- HTTP client not draining response bodies → connection pool exhaustion.
- File opened without `defer Close()` → FD leak.
- Goroutine blocked on channel send → permanent goroutine.
- `time.NewTimer` not `Stop()` → heap pressure.

**Do:**
- Audit every `go` statement with: "what exits this goroutine?"

*Ref: Efficient_Go.md — "Optimization Patterns", "Resource leaks"*

---

### `net/http` Server Timeouts

**Do:**
```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       30 * time.Second,
    WriteTimeout:      30 * time.Second,
    IdleTimeout:       120 * time.Second,
}
```

**Don't:**
- Don't use `http.ListenAndServe` in production — it has no timeouts.

*Ref: Efficient_Go.md — "Optimization Patterns", "HTTP servers"*

---

### Pre-Allocation Checklist

- `make([]T, 0, expectedLen)` for slices.
- `make(map[K]V, expectedSize)` for maps.
- `bytes.Buffer.Grow(n)` for byte buffers.
- `strings.Builder.Grow(n)` for string builders.

**Do:**
- Pre-allocate when you know the final size.
- Document the size assumption.

*Ref: Efficient_Go.md — "Pre-Allocate If You Can"*

---

### Linked-List Allocation Trick

**Principle:** Pre-allocating linked list nodes from a slice avoids per-node GC pressure.

**Code:**
```go
nodes := make([]Node, n)
for i := 0; i < n-1; i++ {
    nodes[i].Next = &nodes[i+1]
}
```

*Ref: Efficient_Go.md — "Optimization Examples", "Linked list pre-allocation"*

---

### String Builder for Concatenation

**Do:**
```go
var b strings.Builder
b.Grow(1024)
for _, s := range parts {
    b.WriteString(s)
}
result := b.String()
```

**Don't:**
- Don't `result += part` in a loop — O(n²) copies.

*Ref: Efficient_Go.md — "String building"*

---

### `sync.Pool` vs `bytes.Buffer.Reset()`

**Principle:** A pool reuses memory across goroutines; `Reset` clears one buffer. Pool is for cross-call reuse.

**Do:**
- `sync.Pool` for buffers that cross function boundaries.
- `bytes.Buffer.Reset()` for the same buffer reused within a request.

*Ref: Efficient_Go.md — "sync.Pool"*

---

### Benchmarks Don't Lie — We Misinterpret Them

**Principle:** Benchmarks don't lie; we misinterpret them. Common errors:
- Forgetting `b.ResetTimer()` after setup.
- Measuring wrong input size.
- Confusing warm-up with steady state.
- Comparing across machines.

**Do:**
- Always `b.ResetTimer()` after expensive setup.
- Always `b.ReportAllocs()`.
- Use `-benchtime=3s` minimum.

**Don't:**
- Don't trust a benchmark that runs < 1000 iterations.

*Ref: Efficient_Go.md — "Benchmarks Lie", "Human Errors"*

---

### Profiling Methodology

1. Start with a hypothesis ("I think X is slow").
2. Capture a profile.
3. Check the hypothesis — was it?
4. If yes, optimise.
5. Re-capture to confirm.
6. If no, form a new hypothesis.

**Don't:**
- Don't optimise without a hypothesis — you'll chase ghosts.

*Ref: Efficient_Go.md — "Data-Driven Bottleneck Analysis"*

---

### CPU-Bound vs I/O-Bound vs Memory-Bound

**Principle:** The dominant bottleneck determines the right optimisation.

**Do:**
- CPU-bound: reduce work, parallelise.
- I/O-bound: batch, cache, async.
- Memory-bound: reduce allocations, smaller data structures.

**Don't:**
- Don't parallelise I/O-bound code without batching — context-switch overhead grows.

*Ref: Efficient_Go.md — "How Go Uses the CPU Resource"*

---

### Channel Direction Discipline

**Do:**
```go
func gen(out chan<- int) { for i := 0; i < 10; i++ { out <- i }; close(out) }
func consume(in <-chan int) { for v := range in { process(v) } }
```

**Don't:**
- Don't use bidirectional channels in signatures — you lose the safety.

*Ref: Efficient_Go.md — "Channel patterns"*

---

### `select` with `default` for Non-Blocking Tries

**Do:**
```go
select {
case ch <- v:
    // sent
default:
    // channel full, drop or handle
}
```

**Don't:**
- Don't use `default` to silently drop important work.

*Ref: Efficient_Go.md — "select patterns"*

---

### Anti-Patterns & Common Mistakes

- **Optimising before profiling:** gut feel is usually wrong.
- **Big-O chasing without measuring:** constant factors often dominate.
- **Skipping functional tests:** an "optimisation" that breaks correctness is a bug.
- **Premature pessimisation:** free wins exist — take them.
- **Production-bound benchmarks in dev:** your laptop is not production.
- **Allocating in hot paths without `-benchmem`:** invisible until prod.
- **Using `defer` in million-iteration loops:** accumulates until function returns.
- **`time.After` in tight loops:** leaks timers.
- **Spawning goroutines without an exit path:** leaks forever.
- **Comparing benchmarks across machines:** noise.
- **Single-run benchmarks:** garbage in, garbage out.
- **Optimising during profiling pauses:** `pprof` output is sampled.
- **Forgetting to `defer ticker.Stop()`:** leaks timers.
- **Holding a lock across I/O:** serialises everything.
- **Reading the whole file when streaming would do:** OOM.

---

## Decision Heuristics / Checklists

### When to optimise
- Profile shows > 5 % time in a function → optimise.
- Otherwise → leave it.

### Picking a profiling tool
- "Where is time spent?" → CPU profile
- "Where are allocations?" → heap profile
- "Why is X blocked?" → block / mutex profile / execution trace
- "What's the call tree?" → pprof `-tree`

### Picking a benchmark approach
- One function, comparing implementations → microbenchmark
- Whole service under load → macrobenchmark + load test
- Real-world traffic patterns → replay production traffic

### Picking an observability stack
- Logs → `slog` JSON to stderr, ship via Vector/Fluent Bit
- Metrics → Prometheus exposition format
- Traces → OpenTelemetry → OTLP → collector

### Resource leak checklist
- All `Open` has matching `Close` via `defer`.
- All goroutines have an exit path (ctx or close).
- All `time.Timer` has matching `Stop()`.
- HTTP response bodies drained and closed.
- Channel senders `close()` when done.
- `ticker.Stop()` deferred.

---

### Napkin Math: Latencies You Should Memorise

| Operation | Latency |
|-----------|---------|
| L1 cache hit | 1 ns |
| L2 cache hit | 4 ns |
| L3 cache hit | 10 ns |
| Main memory | 100 ns |
| SSD read | 100 µs |
| HDD seek | 10 ms |
| Network round-trip (same dc) | 0.5 ms |
| Cross-region network | 50 ms |

**Do:**
- Estimate before measuring — napkin math catches obvious mistakes fast.
- Compare against these numbers when looking at a profile.

**Don't:**
- Don't waste a profile round on a function that can't possibly matter.

*Ref: Efficient_Go.md — "Appendix A. Latencies for Napkin Math Calculations"*

---

### Continuous Profiling in Production

**Principle:** A profile you only capture during incidents tells you nothing about normal behaviour. Continuous profiling samples all the time.

**Do:**
- Use Pyroscope, Polar Signals, or Datadog Continuous Profiler.
- Sample at low rate (≤ 1 % CPU overhead).
- Compare profiles across deploys.

**Don't:**
- Don't try to run continuous profiling yourself — too much overhead.

*Ref: Efficient_Go.md — "Optimization Examples", "Continuous profiling"*

---

### `fgprof` for Full-Goroutine Profiles

**Principle:** `pprof` samples only on-CPU. `fgprof` (by Felix Geisendörfer) samples all goroutines, including time spent in I/O waits.

**Do:**
- Use `fgprof` to find blocking hotspots that standard pprof misses.
- Combine with `pprof` for complete coverage.

**Don't:**
- Don't replace `pprof` entirely — `fgprof` has higher overhead.

**Code:**
```go
import _ "github.com/fgrosse/fgprof"

go func() {
    http.ListenAndServe(":6060", nil) // /debug/pprof/profile
}()
```

*Ref: Efficient_Go.md — "Optimization Examples", "fgprof"*

---

### Goroutine Dump for Stuck Programs

**Do:**
- `kill -SIGQUIT <pid>` — Go runtime prints every goroutine's stack to stderr.
- `runtime.Stack(buf, true)` from inside the program dumps all goroutines.

**Don't:**
- Don't deploy a binary without access to logs — SIGQUIT is your last resort.

*Ref: Efficient_Go.md — "Observability"*

---

### Hot-Path Detection with `go tool pprof -tree`

**Do:**
```bash
go tool pprof -tree -nodecount=20 cpu.prof
```

**Don't:**
- Don't read pprof output top-down only — `cum` (cumulative) often reveals more than `flat`.

*Ref: Efficient_Go.md — "Data-Driven Bottleneck Analysis"*

---

### `alloc_space` vs `alloc_objects` Profiles

**Principle:** Two heap profiles are useful:
- `alloc_space`: total bytes allocated → optimise for size (e.g., huge buffers).
- `alloc_objects`: number of allocations → optimise for count (e.g., many small allocs).

**Do:**
- Switch between them with `pprof -sample_index=alloc_space` and `alloc_objects`.
- Pick based on whether size or count dominates your heap.

*Ref: Efficient_Go.md — "pprof", "alloc_space", "alloc_objects"*

---

### `go test -benchmem` Discipline

**Do:**
- Always use `-benchmem` to see allocs/op and bytes/op.
- Watch the ratio: high alloc/op count = GC pressure; high bytes/op = memory pressure.

**Don't:**
- Don't compare `ns/op` without allocs — an "improvement" that allocates more can be slower.

*Ref: Efficient_Go.md — "Microbenchmarks", "Benchmarking"*

---

### Black-Bat Optimisation: Avoid Hidden Costs

**Principle:** Some operations look cheap but allocate:
- `string(b)` where `b` is `[]byte` — allocates.
- `[]byte(s)` where `s` is a string — allocates.
- `fmt.Sprintf("%d", n)` — allocates.
- `errors.New(msg)` — allocates.

**Do:**
- Use `strconv.Itoa(n)` instead of `fmt.Sprintf("%d", n)`.
- Use `unsafe.String(&b[0], len(b))` (Go 1.20+) to avoid a copy.

**Don't:**
- Don't convert `[]byte` ↔ `string` in hot paths unless you accept the allocation.

*Ref: Efficient_Go.md — "Memory allocations"*

---

### `sync.RWMutex` for Read-Heavy State

**Do:**
- Embed `sync.RWMutex` in the struct.
- Use `RLock` for reads, `Lock` for writes.

**Don't:**
- Don't use `RWMutex` for short critical sections — overhead exceeds the gain.

*Ref: Efficient_Go.md — "Concurrency"*

---

### `context.WithCancelCause` for Rich Errors

**Do:**
```go
ctx, cancel := context.WithCancelCause(parent)
defer cancel(nil)

// Later
cancel(fmt.Errorf("shutdown: %w", err))
```

**Don't:**
- Don't bury the cancellation cause — pass `ctx.Err()` or `context.Cause(ctx)` to callers.

*Ref: Efficient_Go.md — "Context patterns"*

---

### Slice Capacity vs Length — Know the Difference

**Principle:** `len(s)` is the number of elements; `cap(s)` is the backing array size. `append` grows length up to capacity without copying.

**Do:**
- `s := make([]T, 0, expected)` when you know the final length.
- `len(s) == cap(s)` means the next `append` will allocate.

**Don't:**
- Don't `s = s[:cap(s)]` to access memory beyond `len(s)` — it's a bug.

*Ref: Efficient_Go.md — "Slices"*

---

### `runtime.MemStats` Sampling in Production

**Do:**
```go
var mem runtime.MemStats
runtime.ReadMemStats(&mem)
metrics.Gauge("heap_bytes", float64(mem.HeapAlloc))
metrics.Counter("gc_cycles_total", float64(mem.NumGC))
```

**Don't:**
- Don't call `runtime.ReadMemStats` more than 1 Hz — it stops the world.

*Ref: Efficient_Go.md — "Memory profiling"*

---

### `runtime.SetFinalizer` — Last-Resort Cleanup

**Principle:** `SetFinalizer(p, fn)` runs `fn(p)` when `p` becomes unreachable. Use only as a safety net.

**Do:**
- Document that finalizers may never run (no GC pressure = no finalisation).
- Use for OS resources as a backstop.

**Don't:**
- Don't rely on finalizers for primary cleanup — `Close()` is correct.

*Ref: Efficient_Go.md — "Memory management"*

---

### Continuous Benchmarking with `benchstat`

**Principle:** Compare benchmarks over time with `benchstat` to detect regressions.

**Do:**
- Run benchmarks in CI nightly.
- Store results.
- Alert on > 5 % regression.

**Don't:**
- Don't rely on memory-only CI benchmarks — they miss GC improvements.

*Ref: Efficient_Go.md — "Benchmarking discipline"*

---

### Latency Budgeting

**Principle:** A latency budget is the per-request time you can afford. Spend it deliberately:
- Network: 10 ms
- Database: 30 ms
- Business logic: 50 ms
- Response serialisation: 10 ms

**Do:**
- Budget each component of your request path.
- Alert when budget is exhausted.

**Don't:**
- Don't measure only the total — you won't know which component grew.

*Ref: Efficient_Go.md — "Optimization Examples"*

---

### Cardinality Discipline for Labels

**Do:**
- Static labels: `status` ∈ {ok, error}, `method` ∈ {GET, POST}.
- Bounded template labels: `route` ∈ {/users/{id}/orders}.

**Don't:**
- Don't label with raw URLs, user IDs, error messages — cardinality explosion.

*Ref: Efficient_Go.md — "Metrics"*

---

### Code Path Analysis with `pprof` `peek`

**Do:**
- `go tool pprof -peek` shows callers + callees of a function in one view.
- Use to understand a function's role in the call graph.

*Ref: Efficient_Go.md — "Data-Driven Bottleneck Analysis"*

---

### Profile Diffing Across Releases

**Do:**
- Save baseline `cpu.prof` per release.
- Compare with `pprof -base=old.prof new.prof`.
- Investigate any function with > 5 % change.

**Don't:**
- Don't compare profiles across major Go versions — runtime changes can dominate.

*Ref: Efficient_Go.md — "pprof diff"*

---

### Tag Memory as a Pool vs Allocation

**Do:**
- Long-lived (cache entries, config) → heap allocation.
- Short-lived (request buffers, JSON encoders) → `sync.Pool`.
- One-shot per request → `defer` cleanup.

**Don't:**
- Don't pool things that need stable identity.

*Ref: Efficient_Go.md — "Memory management"*

---

### Avoid Large Stack Frames

**Principle:** Each goroutine starts with a 2 KiB stack. A 1 MiB local array blows the stack → heap allocation + goroutine growth cost.

**Do:**
- Allocate large buffers on the heap (`make([]T, n)`).
- Use pointer to large struct instead of value.

**Don't:**
- Don't `var buf [1 << 20]byte` — stack grows.

*Ref: Efficient_Go.md — "How Go Uses the CPU Resource"*

---

### Escape Analysis Flags

**Do:**
- `go build -gcflags="-m=2" ./...` to see escape decisions.
- Look for "moved to heap: <var>" in the output.

**Don't:**
- Don't chase every escape — only when allocation rate matters.

*Ref: Efficient_Go.md — "Escape analysis"*

---

### `runtime.NumGoroutine` Monitoring

**Do:**
- Export as a gauge metric.
- Alert on monotonic growth — leak signal.

**Code:**
```go
metrics.Gauge("goroutines", float64(runtime.NumGoroutine()))
```

*Ref: Efficient_Go.md — "Goroutines"*

---

### `bytes.SplitN` vs `bytes.Split`

**Do:**
- `bytes.SplitN(s, sep, 2)` when you only care about the first token.
- Saves extra slice allocations.

*Ref: Efficient_Go.md — "bytes.Split"*

---

### Avoid `reflect` in Hot Paths

**Principle:** Reflection is ~10× slower than direct calls due to type assertions.

**Do:**
- Cache `reflect.Type`/`reflect.Value` at startup.

**Don't:**
- Don't call `reflect.TypeOf` per request — cache the result.

*Ref: Efficient_Go.md — "Optimization Patterns"*

---

### `slices.Sort` (Go 1.21+) vs `sort.Slice`

**Do:**
- `slices.Sort` is faster (no reflection).
- `slices.SortFunc` for custom comparators.

**Don't:**
- Don't use `sort.Slice` with a closure-heavy comparator in hot paths.

*Ref: Efficient_Go.md — "slices package"*

---

### `sync.OnceValue` (Go 1.21+) for One-Shot Computations

**Do:**
```go
var config = sync.OnceValue(func() *Config {
    return loadConfig()
})
```

**Don't:**
- Don't roll your own with `sync.Mutex` + bool — `OnceValue` is built-in.

*Ref: Efficient_Go.md — "sync.OnceValue"*

---

### `slices.Compact` for In-Place Dedup

**Do:**
```go
deduped := slices.Compact(sortedSlice) // O(n) no allocation
```

**Don't:**
- Don't use a map for dedup when the slice is already sorted.

*Ref: Efficient_Go.md — "slices package"*

---

### `maps.Clone` for Defensive Copies

**Do:**
- `clone := maps.Clone(original)` instead of manual loop.
- Built-in and efficient.

*Ref: Efficient_Go.md — "maps package"*

---

### `errors.Is` for Wrapped Errors

**Do:**
```go
if errors.Is(err, context.Canceled) {
    // ...
}
```

**Don't:**
- Don't `err == context.Canceled` — fails for wrapped errors.

*Ref: Efficient_Go.md — "Error handling"*

---

### `errors.As` for Typed Errors

**Do:**
```go
var netErr *net.OpError
if errors.As(err, &netErr) {
    // access netErr fields
}
```

*Ref: Efficient_Go.md — "Error handling"*

---

### Connection Pool Sizing

**Principle:** A connection pool larger than the number of upstream servers doesn't help. A pool smaller than the workload causes queueing.

**Do:**
- Size = `min(workload parallelism, upstream capacity)`.
- Measure p99 wait time on the pool queue.

**Don't:**
- Don't default to 10 — measure.

*Ref: Efficient_Go.md — "Networking patterns"*

---

### `http.Transport` Reuse

**Do:**
- Share a single `*http.Transport` across all clients.
- Configure `MaxIdleConns`, `MaxConnsPerHost`, `IdleConnTimeout`.

**Don't:**
- Don't `http.Get` per request — it creates a fresh transport each time.

**Code:**
```go
var transport = &http.Transport{
    MaxIdleConns:        100,
    MaxConnsPerHost:     20,
    IdleConnTimeout:     90 * time.Second,
    DisableCompression: true, // for benchmarks
}
```

*Ref: Efficient_Go.md — "HTTP client patterns"*

---

### `http.Server` Connection Lifecycle

**Do:**
- `SetKeepAlivesEnabled(false)` for one-shot services.
- `IdleTimeout` for long-lived connections.
- Document the expected connection lifetime.

*Ref: Efficient_Go.md — "HTTP server patterns"*

---

### Streaming HTTP Responses

**Do:**
```go
func handler(w http.ResponseWriter, r *http.Request) {
    flusher, _ := w.(http.Flusher)
    for chunk := range source {
        w.Write(chunk)
        flusher.Flush()
    }
}
```

**Don't:**
- Don't buffer entire responses in memory before writing.

*Ref: Efficient_Go.md — "HTTP server patterns"*

---

### `pprof` Labels for Per-Endpoint Profiling

**Do:**
```go
ctx = pprof.WithLabels(ctx, pprof.Labels("endpoint", r.URL.Path))
pprof.SetGoroutineLabels(ctx)
```

**Don't:**
- Don't label without bounds — cardinality grows.

*Ref: Efficient_Go.md — "pprof labels"*

---

### `pprof.Do` for Inline CPU Profiling

**Do:**
```go
pprof.Do(ctx, pprof.Labels("op", "compress"), func(ctx context.Context) {
    compress(data)
})
```

*Ref: Efficient_Go.md — "pprof.Do"*

---

### Anti-Patterns & Common Mistakes (additions)

- **Pre-allocating without testing:** sometimes the compiler already optimises.
- **Pool-allocation everything:** pool overhead exceeds gain for small objects.
- **Using `time.Now()` in benchmarks:** skews results.
- **Logging inside benchmark loops:** adds noise and allocates.
- **Comparing `% time` instead of absolute ns/op:** misleading on different cores.
- **Optimising cold paths:** profile first.
- **Forgetting `runtime.GC()` between runs:** inconsistent memory state.
- **Using `sync.Mutex` when atomic suffices:** heavier than needed.
- **Channel sends without receivers:** deadlocks.
- **`defer` for time-sensitive cleanup:** use explicit Close at the right point.

---

---

### Optimisation Decision Tree

1. Is there a RAER entry? No → write one first.
2. Are functional tests green? No → fix bugs first.
3. Is the function on a hot path? No → leave it.
4. Did you profile? No → profile first.
5. Is the bottleneck the algorithm? Yes → change algorithm.
6. Is the bottleneck allocation? Yes → reduce allocations.
7. Is the bottleneck I/O? Yes → cache / batch / async.
8. Otherwise → micro-optimise (last resort).

*Ref: Efficient_Go.md — "Efficiency-Aware Development Flow"*

---

### Cost of `fmt.Sprintf` vs `strconv`

**Principle:** `strconv.Itoa(n)` is ~5× faster than `fmt.Sprintf("%d", n)` because it skips the format parser.

**Do:**
- Use `strconv.Itoa`, `strconv.FormatInt`, `strconv.FormatFloat` for numbers.
- Use `strconv.FormatBool` for booleans.

**Don't:**
- Don't use `fmt.Sprintf` in hot paths.

*Ref: Efficient_Go.md — "Memory allocations"*

---

### Avoiding Reflection for JSON

**Principle:** `encoding/json` uses reflection. For high-throughput JSON, use `easyjson`, `jsoniter`, or `gogo protobuf`.

**Do:**
- Use stdlib `encoding/json` for default.
- Switch to `jsoniter` if JSON is on a hot path.

**Don't:**
- Don't use `map[string]any` to decode — it allocates per field.

*Ref: Efficient_Go.md — "Optimization Patterns"*

---

### Reducing GC Pressure with Smaller Pointers

**Principle:** On 32-bit platforms, pointers are 4 bytes vs 8 on 64-bit. Build with `GOARCH=386` if memory-constrained.

**Do:**
- Default to `amd64`/`arm64` unless you have a reason.
- Use `uint32` indices instead of `*T` pointers for slices when possible.

**Don't:**
- Don't sacrifice clarity for `uint32` indexing — usually not worth it.

*Ref: Efficient_Go.md — "Memory optimization"*

---

### Structured Logging with `slog`

**Do:**
```go
logger.Info("processed request",
    "method", r.Method,
    "path", r.URL.Path,
    "duration_ms", time.Since(start).Milliseconds(),
    "trace_id", traceID,
)
```

**Don't:**
- Don't `fmt.Sprintf` log messages — unparseable.

*Ref: Efficient_Go.md — "Telemetry"*

---

### `runtime/trace` for Scheduler Diagnosis

**Do:**
```go
trace.Start(os.Stdout)
defer trace.Stop()
// ... do work ...
```

- Then: `go tool trace trace.out` for a timeline view.

**Don't:**
- Don't enable trace in production for long — file size grows fast.

*Ref: Efficient_Go.md — "trace"*

---

### Goroutine State Lifecycle

**Principle:** A goroutine transitions through: `running`, `runnable`, `waiting`, `syscall`. The trace shows how long it spends in each.

**Do:**
- Look for long "waiting" periods → blocked on I/O or channel.
- Look for "Syscall" bars → C calls or syscalls.
- Look for "Stop-the-World" → GC pause.

**Don't:**
- Don't ignore goroutines in `syscall` for long — they don't release the OS thread.

*Ref: Efficient_Go.md — "trace analysis"*

---

### `pprof` Symbol Resolution

**Principle:** Stripped binaries have no symbols. Always build without `-s -w` for profiling.

**Do:**
- Build with `-gcflags="all=-N -l"` for readable profiles (disable optimisations + inlining).
- Use the same binary you deploy.

**Don't:**
- Don't profile a binary with debug info stripped — `pprof` shows addresses only.

*Ref: Efficient_Go.md — "pprof"*

---

### `pprof` Profile Comparison

**Do:**
```bash
go tool pprof -base=old.prof new.prof
```

- Shows added/removed samples per function.
- Highlights unintended regressions.

*Ref: Efficient_Go.md — "pprof diff"*

---

### Streaming Decoders

**Do:**
- `encoding/json.Decoder` for streaming JSON.
- `encoding/csv.Reader` for streaming CSV.
- `encoding/xml.Decoder` for streaming XML.

**Don't:**
- Don't `json.Unmarshal` entire HTTP bodies — stream.

*Ref: Efficient_Go.md — "Streaming I/O"*

---

### Connection Pool Tuning (`database/sql`)

**Do:**
- `db.SetMaxOpenConns(n)` — total connections.
- `db.SetMaxIdleConns(m)` — idle pool size.
- `db.SetConnMaxLifetime(d)` — recycle interval.

**Don't:**
- Don't set `MaxOpenConns` higher than the DB can handle.

*Ref: Efficient_Go.md — "Database patterns"*

---

### Database Query Optimisation

**Do:**
- Use prepared statements (cache the plan).
- Use transactions for batch inserts.
- Limit results (`LIMIT n`).

**Don't:**
- Don't `SELECT *` — projection reduces I/O.

*Ref: Efficient_Go.md — "Database patterns"*

---

### Batching for Throughput

**Do:**
- Accumulate up to N items or T duration, then flush.
- Trade latency for throughput when throughput is the bottleneck.

**Don't:**
- Don't flush per-item — 1000× more syscalls.

*Ref: Efficient_Go.md — "Optimization Examples"*

---

### Pagination Patterns

**Do:**
- Cursor-based pagination for large sets (stable, scales).
- Offset pagination only for small sets (UI).

**Don't:**
- Don't `OFFSET 1000000` — DB has to scan past 1 M rows.

*Ref: Efficient_Go.md — "API efficiency"*

---

### Streaming Uploads

**Do:**
- Stream the request body to disk (`io.Copy(file, r.Body)`).
- Don't buffer huge uploads in memory.

**Don't:**
- Don't `ioutil.ReadAll(r.Body)` on a 10 GB upload — OOM.

*Ref: Efficient_Go.md — "HTTP server patterns"*

---

### Compression Trade-offs

**Do:**
- Compress large text payloads (`gzip`, `zstd`).
- Skip compression for already-compressed data (JPEG, MP4).
- Skip for small payloads — compression overhead dominates.

**Don't:**
- Don't compress everything — measure CPU vs bandwidth.

*Ref: Efficient_Go.md — "Optimization Patterns"*

---

### Serialisation Choices

| Format | Speed | Size | Use |
|--------|-------|------|-----|
| JSON | medium | large | public APIs |
| msgpack | fast | small | internal RPC |
| protobuf | fast | small | stable schema |
| gob | fast | medium | Go-only |

**Do:**
- Match format to audience.

*Ref: Efficient_Go.md — "Serialization patterns"*

---

### Anti-Patterns & Common Mistakes (final additions)

- **Profile-driven debugging instead of test-driven:** tests catch regressions, profiles don't.
- **Sharing `http.Client` with custom `Transport`:** connection pooling breaks.
- **Using `context.Background()` deep in code:** can't cancel.
- **Forgetting `defer rows.Close()`:** leaks DB cursors.
- **Long-running goroutines without context:** leaks on shutdown.
- **`go func() { for { ... } }()` without break:** infinite leak.
- **Buffered channels with no consumers:** buffer fills, blocks.
- **Race conditions brushed off:** always run `-race`.

---
