# Efficient Go
**Author:** Bartłomiej Płotka
**Topic tags:** `#performance` `#testing` `#concurrency` `#api` `#profiling`
**Language focus:** Go-first
**Sources:** `markdown_output/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md` · `summaries/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md`

## TL;DR
Pragmatic, data-driven efficiency engineering for Go: define Resource-Aware Efficiency Requirements (RAER), follow the Test-Fix-Benchmark-Optimize (TFBO) flow, eliminate waste before trading, profile with pprof, benchmark with the standard `testing` package + `benchstat`, and treat memory allocation, goroutine lifecycle, and resource leaks as the highest-leverage recurring problems.

---

## Best Practices by Topic

### Pragmatic Optimization Mindset & RAER

**Principle:** Be pragmatic, not obsessed. Small efficiency habits that do not reduce readability should be part of everyday coding hygiene, but every other optimization must be justified by a written, data-driven goal.

**Do:**
- Define Resource-Aware Efficiency Requirements (RAER) up front — operation, dataset, max latency (p50/p90), CPU/memory budget.
- Use napkin math with hardware latencies to estimate feasibility before writing code.
- When the reported observation is within the RAER, communicate that fact and move on.
- Treat YAGNI as a guideline, not a license to ignore performance: small habits (pre-allocate slices you know the size of, capture allocs in benchmarks) are reasonable, not premature.

**Don't:**
- Don't reject an efficiency change just because it is "premature" when it is obvious, free, and at worst slightly more readable.
- Don't accept stakeholder efficiency requests without translating them into a RAER — they may be the wrong framing (the XY problem).
- Don't add features/parameters you don't need on a critical path; each is a permanent efficiency tax.

**Code:**
```go
// RAER-style comment block, recorded next to the benchmark that validates it.
// BenchmarkSum assesses `Sum` function.
// NOTE(bwplotka): Test it with a maximum of 4 CPU cores, given we don't allocate
// more in our production containers.
//
// Recommended run options:
/*
export ver=v1 && go test \
    -run '^$' -bench '^BenchmarkSum$' \
    -benchtime 10s -count 5 -cpu 4 -benchmem \
    -memprofile=${ver}.mem.pprof -cpuprofile=${ver}.cpu.pprof \
  | tee ${ver}.txt
*/
func BenchmarkSum(b *testing.B) { /* ... */ }
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Resource-Aware Efficiency Requirements", "You Aren't Going to Need It"*

---

### TFBO: Test → Fix → Benchmark → Optimize

**Principle:** Separate the functionality phase (TDD-style test → fix loop) from the efficiency phase (benchmark → profile → optimize → re-bench). Never optimize without a baseline number, and never ship an optimization without re-running tests *and* benchmarks.

**Do:**
- In the efficiency phase, write the benchmark *first* (even before the optimization), save the result to `v1.txt`, then optimize, then save `v2.txt` and compare with `benchstat`.
- Run the full TFBO loop in *short iterations* — one level (system / algorithm / code / OS / hardware) at a time, one change at a time.
- Always assert errors in the benchmark loop (`testutil.Ok(b, err)`) — silent failures turn into "0 ns/op" lies.
- Compare relative results, not absolute; absolute numbers depend on the machine.

**Don't:**
- Don't skip the test pass after a deliberate optimization — revert if tests fail rather than debugging forward.
- Don't try to optimize all bottlenecks at once; you'll lose the ability to attribute the gain.
- Don't compare today's run against last week's numbers — environment drift will mislead you.

**Code:**
```go
// Testable benchmark: same body runs from unit test (N=1, strict assertion)
// and from go test (N=b.N, allocation tracking only).
func TestBenchSum(t *testing.T) {
    benchmarkSum(testutil.NewTB(t))
}
func BenchmarkSum(b *testing.B) {
    benchmarkSum(testutil.NewTB(b))
}
func benchmarkSum(tb testutil.TB) {
    for i := 0; i < tb.N(); i++ {
        ret, err := Sum("testdata/test.2M.txt")
        testutil.Ok(tb, err)
        if !tb.IsBenchmark() {
            testutil.Equals(tb, int64(6221600000), ret)
        }
    }
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Efficiency-Aware Development Flow", "Test Your Benchmark for Correctness!", "Avoid Comparing Efficiency with Older Experiment Results!"*

---

### Pre-Allocation & "Do Less Work" (Memory Discipline)

**Principle:** Allocation is the root cause of most Go efficiency problems. Reduce first, reuse second, recycle last (the Three Rs). Pre-allocate every container whose final size you know; pick `struct{}` for unused map values; design tight algorithms.

**Do:**
- Pre-allocate slices (`make([]T, 0, n)`), maps (`make(map[K]V, n)`), and grow buffers (`bytes.Buffer`/`strings.Builder`).
- Use `struct{}` for set-like or signaling values: `map[T]struct{}`, `chan struct{}`.
- Convert algorithms first — switch from full-file read to streaming with a fixed buffer.
- Read `*os.File` with an `io.SectionReader` and a small reused buffer; do not `os.ReadFile` for hot paths.

**Don't:**
- Don't `append` in a loop without first pre-allocating if the final size is known.
- Don't return a `(*T, error)` pair for a large `T` you only need to read — pass a value.
- Don't reach for `sync.Pool` before the easier wins (reduce allocations, pre-allocate, streaming) are exhausted — the book's macrobenchmark showed pooling can *increase* maximum heap usage.

**Code:**
```go
// Pre-allocated streaming reader — constant ~8 KB heap regardless of input size.
func Sum6Reader(r io.Reader, buf []byte) (ret int64, err error) {
    var offset, n int
    for err != io.EOF {
        n, err = r.Read(buf[offset:])
        if err != nil && err != io.EOF {
            return 0, err
        }
        n += offset
        var last int
        for i := range buf[:n] {
            if buf[i] != '\n' {
                continue
            }
            num, err := ParseInt(buf[last:i])
            if err != nil {
                return 0, err
            }
            ret += num
            last = i + 1
        }
        offset = n - last
        if offset > 0 {
            _ = copy(buf, buf[last:n])
        }
    }
    return ret, nil
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Pre-Allocate If You Can", "Moving to Streaming Algorithm", "Reduce Allocations"*

---

### Bounded Buffer Reuse, Not sync.Pool

**Principle:** For short, repeated work that exceeds a `sync.Pool`'s GC window, a static buffer is faster *and* cheaper than a pool. `sync.Pool` is wiped on every GC cycle and has narrow, well-defined use cases.

**Do:**
- Reuse a buffer by `buf = buf[:0]` between operations.
- For *many* concurrent workers with stable workloads, a small array of static buffers beats `sync.Pool`.
- Measure at the macro level: the book's `labeler` experiment proved `no-buffering` had the *lowest* maximum heap despite the highest allocation count, because slower allocation paced the GC.

**Don't:**
- Don't use `sync.Pool` for objects that must survive more than one GC cycle.
- Don't `defer p.Put(buf)` after a `append` may have grown the slice — the `defer` evaluates `buf` at defer time, so you return the *original* slice, not the grown one.
- Don't pool objects that have to be reset before reuse; reset bugs cause silent data corruption.

**Code:**
```go
// Simple buffer reuse: ~2x faster, 0 B allocated vs ~5 MB/op.
func processUsingBuffer(buf []byte) {
    buf = buf[:0]
    for i := 0; i < 1e6; i++ {
        buf = append(buf, 'a')
    }
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Memory Reuse and Pooling"*

---

### Don't Leak Resources (Goroutines, Bodies, Files)

**Principle:** A goroutine is not garbage-collected. Every goroutine must have a known exit path; every `Close`/`Cancel` returned to you must be called, even on error; HTTP response bodies must be exhausted *and* closed.

**Do:**
- Pass a `done <-chan struct{}` (or `context.Context`) into spawned goroutines; `select` on it for every send/recv.
- `defer errcapture.Do(&err, f.Close, "close file")` instead of bare `defer f.Close()` — silent close errors lose data.
- For multi-resource acquisition, accumulate a `[]io.ReadCloser` and close all on error.
- Use `goleak.VerifyNone(t)` in every test that exercises concurrent code; treat leaks as test failures.
- For HTTP responses, read to EOF before close so the keep-alive TCP connection can be reused.

**Don't:**
- Don't ignore errors on `Close` — close is where buffered writes flush.
- Don't `defer pool.Put(buf)` after a growable append.
- Don't benchmark concurrent code without waiting for the work to finish — `go func() { ... }()` in a benchmark measures scheduling, not work.
- Don't assume buffered `respCh` and the cancel path together — the goroutine still runs to completion and writes to a channel nobody reads; it can still OOM.

**Code:**
```go
// WRONG: goroutine leaks on ctx.Done because no one drains respCh.
func Handle_VeryWrong(w http.ResponseWriter, r *http.Request) {
    respCh := make(chan int)
    go func() {
        defer close(respCh)
        respCh <- ComplexComputation()
    }()
    select {
    case <-r.Context().Done():
        return
    case resp := <-respCh:
        _, _ = w.Write([]byte(strconv.Itoa(resp)))
        return
    }
}

// RIGHT: always read from the channel, then check ctx.
func Handle_Better(w http.ResponseWriter, r *http.Request) {
    respCh := make(chan int)
    go func() {
        defer close(respCh)
        respCh <- ComplexComputationWithCtx(r.Context())
    }()
    resp := <-respCh
    if r.Context().Err() != nil {
        return
    }
    _, _ = w.Write([]byte(strconv.Itoa(resp)))
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Control the Lifecycle of Your Goroutines", "Reliably Close Things", "Exhaust Things"*

---

### Concurrency Efficiency

**Principle:** Concurrency is one of the *last* deliberate optimizations, not the first. It only pays when the work is genuinely independent and worth more than the coordination overhead.

**Do:**
- Default `GOMAXPROCS` to the number of virtual CPU cores; use `uber/automaxprocs` in containers.
- Prefer *coordination-free* sharding (each worker takes a deterministic byte range) over channel-based work distribution.
- Spawn a *fixed* number of worker goroutines; never spawn a goroutine per unit of work.
- Pass data with channels, never via shared pointer mutation — "do not communicate by sharing memory; share memory by communicating".
- Read from the channel in *every* branch (including the cancel/timeout branch) to unblock the producer.

**Don't:**
- Don't spawn `N` goroutines where `N` is user input — that's unbounded concurrency.
- Don't add concurrency for single-CPU-bound work; it only serializes on the scheduler.
- Don't do atomic.AddInt64 per work item; aggregate locally and publish once.
- Don't use a single channel for fan-in if it becomes a contention point — coordination overhead can dominate the work.

**Code:**
```go
// Coordination-free sharding: ~2x faster than sequential, no channel
// distribution overhead.
func ConcurrentSum3(fileName string, workers int) (ret int64, _ error) {
    b, err := os.ReadFile(fileName)
    if err != nil {
        return 0, err
    }
    var (
        bytesPerWorker = len(b) / workers
        resultCh        = make(chan int64)
    )
    for i := 0; i < workers; i++ {
        go func(i int) {
            begin, end := shardedRange(i, bytesPerWorker, b)
            var sum int64
            for last := begin; begin < end; begin++ {
                if b[begin] != '\n' {
                    continue
                }
                num, err := ParseInt(b[last:begin])
                if err != nil {
                    continue
                }
                sum += num
                last = begin + 1
            }
            resultCh <- sum
        }(i)
    }
    for i := 0; i < workers; i++ {
        ret += <-resultCh
    }
    close(resultCh)
    return ret, nil
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "When to Use Concurrency", "Optimizing Latency Using Concurrency"*

---

### Profiling & Bottleneck Analysis (pprof)

**Principle:** Never guess. Profile first. The pprof format gives you per-stack-trace attribution of resource use; the web UI's Top / Graph / Flame Graph / Source views are the fastest path from "this is slow" to "this is the line".

**Do:**
- Capture CPU + heap + goroutine + block + mutex profiles via `net/http/pprof` on long-running services.
- Add `-cpuprofile` and `-memprofile` to your `go test -bench` runs by default.
- Use Flame Graph view to spot the widest boxes (biggest cumulative cost) and Source view to land on the exact line.
- Use `goleak` to verify profile-collecting tests don't leak; treat the heap as a *moving* estimate, not a fixed number.
- For production: continuous profiling (Parca / Polar Signals / Pyroscope / Phlare) with a 1-minute scrape is safe overhead.

**Don't:**
- Don't trust a single profile — they are statistical, missing small contributors is normal.
- Don't read VSS (virtual memory size) — most of it is unmapped; use RSS, WSS, or Go heap stats.
- Don't use a `benchstat` significance test (p > 0.05) on a known-good delta to "prove" the change didn't regress — use common sense when variance is low.
- Don't ship a profile taken against the wrong binary — `Disassemble` view is silently wrong if the binary doesn't match.

**Code:**
```go
// HTTP pprof handler registration.
m := http.NewServeMux()
m.HandleFunc("/debug/pprof/", pprof.Index)
m.HandleFunc("/debug/pprof/profile", pprof.Profile)
m.HandleFunc("/debug/fgprof/profile", fgprof.Handler().ServeHTTP)
srv := http.Server{Handler: m}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "pprof Format", "go tool pprof Reports", "Capturing the Profiling Signal", "Continuous Profiling"*

---

### Benchmarking Discipline

**Principle:** Benchmarks lie only when you let them. Run multiple iterations, watch variance, use `benchstat`, and assert correctness in the loop. Always include the profile flags (`-cpuprofile`, `-memprofile`, `-benchmem`) so the next question ("why?") is one tool away.

**Do:**
- Use the Go testing framework: `func BenchmarkXxx(b *testing.B) { b.ReportAllocs(); b.ResetTimer(); for i := 0; i < b.N; i++ { ... } }`.
- Name benchmarks as `BenchmarkFuncName` or `BenchmarkType_Method` (e.g., `BenchmarkCalculator_Sum_withDuplicates`).
- Run with `-benchtime 10s -count 5 -cpu 4` and pipe through `tee ver=v1.txt`.
- For different inputs, use sub-benchmarks with `b.Run("lines-1M", func(b *testing.B) { ... })`.
- `benchstat` for relative comparisons with delta and p-value.

**Don't:**
- Don't use `i` from the `b.N` loop as input — the compiler will fold it.
- Don't rely on a single run; variance is invisible without `-count >= 5`.
- Don't use sinks on every benchmark — only when you can prove the compiler has optimized it away.
- Don't `time.Now()` for operations that finish under 100 ns; the measurement noise dominates.

**Code:**
```go
func BenchmarkSum(b *testing.B) {
    b.ReportAllocs()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = Sum("testdata/test.2M.txt")
    }
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Go Benchmarks", "Understanding the Results", "Tips and Tricks for Microbenchmarking"*

---

### Memory, GC, and Latency Trade-offs

**Principle:** Memory allocation dominates Go efficiency. Pre-allocate when the size is known, prefer streaming when it is not. Use `GOMEMLIMIT` (90–95% of pod limit) for the GC-to-OS-pressure soft cap; `GOGC=off` only when you have spare RAM and want to trade CPU for less frequent GCs.

**Do:**
- Tune `GOGC` or set `GOMEMLIMIT` based on observed heap behavior, not defaults.
- For Kubernetes pods, `GOMEMLIMIT=90%` of the pod memory limit (leave 5–10% for non-Go memory).
- Use `runtime/metrics` (since Go 1.16) over `runtime.ReadMemStats` — no STW events.
- Use contiguous memory: prefer arrays/slices over pointer-chasing linked lists; prefer structs with `~*` no-pointer fields where possible (faster GC, L-cache friendly).
- Code on the *left of the page* — fewer nested branches, simpler loops (CPU branch predictor friendly).

**Don't:**
- Don't store pointer-rich structs when you can flatten — every pointer is GC work.
- Don't `runtime.GC()` manually in library code — it has global effects.
- Don't read `*os.File` once and walk it again from `os.ReadFile`'s `[]byte` — read with `io.NewSectionReader` per worker.
- Don't assume "fewer allocations = better latency" — the book's macrobenchmark showed the opposite for labeler.

**Code:**
```go
// Heap stats via runtime/metrics (no STW).
var memMetrics = []metrics.Sample{
    {Name: "/gc/heap/allocs:bytes"},
    {Name: "/memory/classes/heap/objects:bytes"},
}
func printMemRuntimeMetric() {
    runtime.GC()
    metrics.Read(memMetrics)
    fmt.Println("Total bytes allocated:", memMetrics[0].Value.Uint64())
    fmt.Println("In-use bytes:",        memMetrics[1].Value.Uint64())
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Garbage Collection", "Recycle", "OS memory pages statistics", "Pipelining and Out-of-Order Execution"*

---

### Caching and "Think Out of the Box"

**Principle:** Before sinking weeks into deep optimization, ask: is the same input repeated? If yes, a four-line cache may beat four days of profiling.

**Do:**
- Memoize results keyed on the input filename or a content hash when the input space is bounded.
- Choose LRU, `golang-lru`, or `ristretto` based on traffic shape; reach for Memcached/Redis/groupcache for distributed systems.
- Apply a "thinking-out-of-the-box" check after exhausting the obvious algorithmic wins.

**Don't:**
- Don't cache unbounded inputs or inputs that change constantly.
- Don't make caching the default for *every* optimization — it trades latency for memory and can hide staleness bugs.

**Code:**
```go
// Four lines of caching beats any deep optimization when inputs repeat.
var sumByFile = map[string]int64{}
func Sum7(fileName string) (int64, error) {
    if s, ok := sumByFile[fileName]; ok {
        return s, nil
    }
    ret, err := Sum(fileName)
    if err != nil {
        return 0, err
    }
    sumByFile[fileName] = ret
    return ret, nil
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Bonus: Thinking Out of the Box", "Trading Space for Time"*

---

### Algorithmic & Standard-Library Wins

**Principle:** Many efficiency problems hide inside the *generic* standard library functions you reach for first. Replacing `bytes.Split` + `strconv.ParseInt(string(b[...]))` with a single in-place loop and a tight parser often halves latency and memory.

**Do:**
- Profile, then write a tailored replacement *only* on a measured critical path.
- Stream with a fixed buffer and reuse it across iterations.
- Write the tightest possible parser (e.g., byte-wise with no allocations) for base-10 ints.

**Don't:**
- Don't use `bytes.Split` for newline-terminated records when you can scan in place.
- Don't copy `[]byte` to `string` via the standard conversion on a hot path; if safety allows, use `*(*string)(unsafe.Pointer(&b))` (e.g., Prometheus's `yoloString`).
- Don't pay for `strconv.ParseInt`'s base/bit-size flexibility when you only need base-10 int64.

**Code:**
```go
// Tailored ParseInt: ~46% faster than strconv.ParseInt on the same data,
// and parses []byte directly (no string conversion).
func ParseInt(input []byte) (n int64, _ error) {
    factor := int64(1)
    k := 0
    if input[0] == '-' {
        factor *= -1
        k++
    }
    for i := len(input) - 1; i >= k; i-- {
        if input[i] < '0' || input[i] > '9' {
            return 0, errors.Newf("not a valid integer: %v", input)
        }
        n += factor * int64(input[i]-'0')
        factor *= 10
    }
    return n, nil
}
```
*Ref: Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md — "Optimizing bytes.Split", "Optimizing runtime.slicebytetostring", "Optimizing strconv.Parse"*

---

## Anti-Patterns & Common Mistakes

- **"Optimized code is unreadable":** False in most cases. `make([]string, 0, n*7)` is *more* explicit than `append` in a loop, and the profile guides the next move. → *fix:* read the profile; if the optimization is "obvious" (free, doesn't hurt readability, easy), do it now.
- **Reading once, calling thrice via an interface:** `if len(reports.Get()) == 0 { ... return sum / float64(len(reports.Get())) }` calls `Get()` three times — once into a local; less work, more readable, safer. → *fix:* `got := reports.Get()`.
- **Goroutines as free workers:** Spinning a goroutine per work item is 40x slower than sequential when coordination dominates. → *fix:* use a fixed-size worker pool or coordination-free sharding.
- **Closing an HTTP body but not exhausting it:** loses the keep-alive TCP connection (~29% latency). → *fix:* read to EOF before close, or use `errcapture.ExhaustClose`.
- **`defer f.Close()` without error capture:** silent data loss on flush. → *fix:* `defer errcapture.Do(&err, f.Close, "close file")`.
- **`defer p.Put(buf)` after `append`:** the deferred slice is the *original*; pool sees a stale reference. → *fix:* `Put` after the loop, not in `defer`.
- **Pre-allocating `[]Node` then deleting all but one:** the underlying array keeps the whole thing alive. → *fix:* implement `ClipMemory()` or use individual allocations.
- **Trusting one-shot profiles:** always -count ≥ 5, always `benchstat` for deltas; "too good to be true" usually means the benchmark was wrong.
- **Optimizing before RAER:** every change looks premature without a written goal. → *fix:* write the RAER in the FR doc; renegotiate later if needed.
- **Manual `runtime.GC()` in libraries:** global side effects; the runtime's GC pacing already handles it. → *fix:* don't; tune GOGC/GOMEMLIMIT at the process level instead.
- **Forgetting `b.ResetTimer()`:** the benchmark includes setup time and reports it as the per-op cost. → *fix:* `b.ResetTimer()` immediately before the `b.N` loop.

## Decision Heuristics / Checklists

- **Have I written a RAER before optimizing?** No → stop and write one.
- **Did I profile the actual workload (not a synthetic one)?** No → fix the workload first.
- **Am I at the right optimization level?** Try system → algorithm → code → OS → hardware. Each level is 10–20× potential; stop when the cost stops paying back.
- **Is the bottleneck CPU or memory?** Use `fgprof` to see wall time; if I/O dominates, async/streaming helps; if allocation dominates, reduce; if CPU dominates, algorithmic.
- **Should I add concurrency?** Only if (1) the work is genuinely independent, (2) the coordination overhead is < the per-item cost, and (3) goroutine count is bounded.
- **Should I add `sync.Pool`?** Only if (1) objects are interchangeable, (2) the reuse window is < one GC cycle, (3) goroutine count varies, (4) the GC has time between reuses.
- **Should I add caching?** Only if the same input repeats with bounded cardinality, and staleness is acceptable.
- **Did I run the full TFBO loop?** Test → profile → benchmark → optimize → re-bench → re-test → ship. Never skip a step.
- **Did I run the benchmark with `-count 5` and inspect `benchstat`?** No → the result is noise.
- **Did I test on macro / production load?** No → microbenchmarks can't see GC behavior, max heap, or saturation.

## Key Takeaways

1. **Write a RAER.** Without written, data-driven goals, every optimization is potentially premature.
2. **Profile, don't guess.** Use `pprof` (CPU, heap, goroutine, block, mutex), `fgprof` for off-CPU, continuous profiling in prod.
3. **Reduce allocations first.** Pre-allocate, stream with a fixed buffer, use `struct{}`, write tight parsers. Reach for `sync.Pool` and complex machinery only after the easy wins.
4. **Every goroutine needs an exit path.** `goleak` in every concurrent test. Always read from the channel in the cancel branch.
5. **Benchmarks are relative, not absolute.** `benchstat` with `-count 5`; the *delta* and the p-value matter, not the number.
6. **Optimize one level, one change at a time.** A/B each change; profile, don't measure change.
7. **Macro matters.** Microbenchmarks lie about GC, max heap, and contention. Validate on macro / production-shaped load.
8. **Think out of the box.** A four-line cache can beat four days of profiling when the input repeats.
9. **Concurrency is the last optimization, not the first.** Coordination overhead often exceeds the work itself.
10. **Be a pragmatic mechanic.** Fix the leak, not the lap time. The book is "Efficient Go", not "Ultra-Performance Go".

## Cross-References
- Related: [[./Concurrency_in_Go.md]]
- Related: [[./Mastering_Api_Architecture.md]]
- Topic index: [[../INDEX.md]]
