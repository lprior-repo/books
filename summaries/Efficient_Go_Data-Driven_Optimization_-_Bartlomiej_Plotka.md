# Efficient Go: Data-Driven Performance Optimization

**By Bartlomiej Plotka (O'Reilly, 2022) -- Comprehensive Summary**

---

## Chapter 1. Software Efficiency Matters

### Behind Performance

The book opens by distinguishing between performance and efficiency. Performance is about how fast a system executes under a given workload; efficiency is about how well resources are used to achieve that performance. Kernighan and Pike define the true definition of efficiency as achieving a goal with minimum waste. The chapter argues that software efficiency is not a luxury -- it is a critical engineering discipline.

### Optimized Code Is Not Readable (A Misconception)

A common misconception is that optimized code must be unreadable. Plotka argues the opposite: well-optimized code is often more readable because it is more explicit. He contrasts two Go functions -- one calling `Get()` three times and another storing the result in a variable and reusing it. The latter is both faster and more readable because it clearly communicates intent. Similarly, slice pre-allocation with `make([]string, 0, n*7)` is both more efficient and more self-documenting than naive `append` in a loop.

Plotka also discusses how readability standards evolve. Hungarian notation, useful in the 1970s-80s, is now obsolete because modern IDEs show types instantly. The same principle applies to efficiency patterns: what feels unfamiliar today becomes second nature with practice.

### You Aren't Going to Need It

The YAGNI principle says avoid implementing features not required right now. However, Plotka draws an important distinction: YAGNI does not mean ignoring performance entirely. Small efficiency habits like pre-allocating slices, basic monitoring, and avoiding obvious waste should be part of everyday coding hygiene. The chapter uses a story about a developer named Katie to illustrate when optimizations violate YAGNI and when they represent good practice.

### Hardware Is Getting Faster and Cheaper (But Not Fast Enough)

Three forces undermine the "just buy more hardware" argument:

1. **Parkinson's Law**: Software expands to fill available memory. No matter how much hardware improves, software will consume it.
2. **Software gets slower faster than hardware gets faster**: "Fat software" (Wirth's term) means that for the same problems, we now have bulkier solutions with prettier UIs, more features, and more abstraction layers.
3. **Technological limits**: Moore's Law has slowed. Dennard scaling ended around 2006, meaning transistors are smaller but not more power-efficient. Clock speeds have plateaued around 3-5 GHz.

### Faster Execution Is More Energy Efficient

Faster code uses less energy. With data centers consuming significant portions of global electricity, efficiency has environmental implications. Inclusive, accessible software also depends on efficiency because not all users have high-end devices.

### We Can Scale Horizontally Instead (But At What Cost?)

Horizontal scaling is not always the answer. Adding more machines adds operational complexity, more potential failures, higher costs, and often does not solve latency problems for individual requests. The chapter cites real examples from the Thanos project where a single function allocated 17.61 TB of memory in five days -- small inefficiencies compound dramatically at scale.

### Time to Market Is More Important (But Quality Matters)

Shipping fast is important, but shipping inefficient software creates technical debt. The Cyberpunk 2077 launch disaster is cited as an example where performance problems severely damaged a product's reputation and required massive patching effort.

### The Key to Pragmatic Code Performance

The chapter concludes with the book's philosophy: be pragmatic, not obsessed. Set clear efficiency goals. Invest in observability tools. Treat optimization like any other feature -- do it when needed, measure it, and do not over-engineer. The difference between "efficient" and "ultra-performance" is significant; this book is about the former.

---

## Chapter 2. Efficient Introduction to Go

### Basics You Should Know About Go

This chapter provides a rapid overview of Go's design philosophy and features relevant to efficiency.

**Imperative, Compiled, and Statically Typed**: Go compiles directly to machine code. It is statically typed, catching errors at compile time. It is imperative, focusing on how to compute results step by step.

**Designed to Improve Serious Codebases**: Go was created at Google to solve problems in large-scale software engineering: slow compilation, difficult dependency management, and hard-to-read code. It was designed for readability, maintainability, and efficiency from the start.

**Simplicity, Safety, and Readability Are Paramount**: Go deliberately omits features like inheritance, exceptions, and operator overloading to keep code predictable. The gofmt tool enforces a single code style across the entire ecosystem.

**Governed by Google, Yet Open Source**: Go is open source with strong community governance. The Go 1 compatibility guarantee means code written for Go 1.0 still compiles today.

**Packaging and Modules**: Go organizes code into packages (directories of .go files) and modules (versioned collections of packages, tracked in go.mod). Dependencies are explicit and transparent, avoiding dependency hell.

**Dependencies Transparency by Default**: Go's dependency model emphasizes minimalism. The standard library avoids unnecessary dependencies, and the module system makes the dependency graph visible.

**Consistent Tooling**: The `go` CLI provides formatting (`go fmt`), testing (`go test`), building (`go build`), documentation (`godoc`), dependency management (`go mod`), and profiling (`go tool pprof`).

**Single Way of Handling Errors**: Go treats errors as first-class citizens. Functions that can fail return an `error` as the last return value. There are no exceptions for control flow. This explicit error handling makes programs more predictable and easier to debug, though more verbose. Plotka recommends `github.com/efficientgo/core/errors` for wrapping errors with stack traces.

**Strong Ecosystem**: The Go standard library is rich, high-quality, and well-optimized. Running an HTTP server requires only a few lines of code. The Go Playground allows testing code in-browser.

**Unused Import or Variable Causes Build Error**: Go refuses to compile with unused variables or imports, keeping code clean.

**Unit Testing and Table Tests**: Tests are first-class citizens in Go. Files ending in `_test.go` contain tests. Table tests (iterating over test cases in a struct slice) are the idiomatic pattern for thorough coverage.

### Advanced Language Elements

**Code Documentation as a First Citizen**: The `godoc` tool generates documentation from code comments. Five rules govern godoc: package comments start with `Package <name>`, public constructs have full-sentence comments starting with their name, bug annotations use `BUG(who)`, example functions use `Example<ConstructName>`, and output assertions use `// Output:`.

**Backward Compatibility and Portability**: Go guarantees backward compatibility since Go 1.0. Cross-compilation is built in. However, there are no efficiency guarantees between versions.

**Go Runtime**: Unlike Java's JVM, Go compiles to native machine code. The Go runtime manages memory (garbage collection) and concurrency (goroutine scheduling) in the background.

**Object-Oriented Programming**: Go supports OOP through structs with methods, embedding (a form of inheritance), and interfaces (implicit implementation -- no `implements` keyword needed). Interfaces enable polymorphism. Value receivers copy the struct; pointer receivers allow mutation.

**Generics**: Since Go 1.18, generics (type parameters) allow type-safe reusable code. The book shows a generic sort implementation using `constraints.Ordered`. Generics complement interfaces but should be used sparingly to maintain code simplicity.

---

## Chapter 3. Conquering Efficiency

### Beyond Waste, Optimization Is a Zero-Sum Game

Plotka defines two types of optimization:

**Reasonable Optimizations** eliminate waste -- unnecessary work that provides no value. These should be part of everyday coding hygiene. Examples: removing debug print statements, stopping leaked goroutines, using pre-allocated slices. These do not sacrifice readability or other qualities.

**Deliberate Optimizations** involve trade-offs: improving one aspect (e.g., latency) by sacrificing another (e.g., memory usage, code complexity). Adding caching, introducing compression, or switching algorithms are deliberate. These require measurement to confirm the trade-off is worthwhile.

### Optimization Challenges

Five core challenges face any optimization effort:

1. **Programmers are bad at estimating bottlenecks**: The Pareto Principle applies -- 80% of resource consumption comes from 20% of code. Finding that 20% requires tools, not guessing.
2. **Programmers are bad at estimating resource consumption**: Never trust judgment; always measure.
3. **Maintaining efficiency over time is hard**: Code, dependencies, hardware, and workloads change.
4. **Reliable verification is difficult**: Reproducing production conditions, avoiding noisy neighbors, proper warm-up, and preventing compiler optimizations from skewing benchmarks are all non-trivial.
5. **Optimization impacts other software qualities**: Functionality, readability, maintainability, and security may suffer.

### Understand Your Goals

Efficiency goals must be explicit, written, and data-driven. Plotka introduces **Resource-Aware Efficiency Requirements (RAER)** -- a template that specifies:

- The module/function being optimized
- The input characteristics (size, rate)
- Latency requirements (per-operation, percentiles)
- Resource constraints (memory, CPU, network)
- Any assumptions and exclusions

Example: A JPEG enhancement service processing images up to 16 MB should complete in under 60 seconds using no more than 100 MB of RAM.

### Efficiency-Aware Development Flow (TFBO)

Plotka introduces **Test-Driven Flow for Better Optimization (TFBO)**, a 9-step process:

1. **Functionality Phase**: Write requirements, design, implement, and test functionality first.
2. **Define efficiency requirements** (RAER).
3. **Write tests** for the functional correctness.
4. **Efficiency Phase**: Assess current efficiency using benchmarks and profiling.
5. **Optimize**: Apply reasonable then deliberate optimizations.
6. **Re-benchmark**: Verify the optimization worked.
7. **Repeat** if goals are not met.
8. **Document** the optimization and its rationale.
9. **Release and enjoy**.

### Optimization Design Levels

Optimizations operate at different levels, from highest to lowest impact:

1. **System level** (architecture, distributed systems design)
2. **Algorithm and data structure level** (choosing the right algorithm)
3. **Data-driven level** (caching, precomputation, indexing)
4. **Code level** (loop optimization, memory allocation patterns)
5. **Hardware level** (CPU cache alignment, SIMD)

Higher levels offer bigger wins. A better algorithm always beats micro-optimizing a poor one.

### Got an Efficiency Problem? Keep Calm!

When efficiency problems are reported, follow a calm, blameless process:

1. Check if the problem matches the requirements (maybe the expectations are wrong).
2. Check if it is a known issue.
3. Check if the environment is at fault (hardware, configuration).
4. Profile and benchmark to confirm the bottleneck.
5. Only then, optimize.

---

## Chapter 4. How Go Uses the CPU Resource

### CPU in a Modern Computer Architecture

The CPU executes instructions fetched from memory. Modern CPUs are extraordinarily complex, with billions of transistors executing billions of operations per second.

### Assembly

Go has its own Assembly syntax (Plan 9 style). Understanding Assembly helps verify compiler output and understand what the CPU actually executes. Plotka shows a simple `Sum` function in Go and its Assembly output, demonstrating how Go function calls and stack management work at the machine level.

### Understanding Go Compiler

The Go compiler focuses on one package at a time, compiling source to native code for the target architecture. Key compiler optimizations include:

- **Function inlining**: Replacing function calls with the function body for small functions.
- **Escape analysis**: Determining whether variables can live on the stack (fast) or must escape to the heap (requires GC).
- **Dead code elimination**: Removing unreachable code.

The `-gcflags="-m"` flag shows optimization decisions. Understanding the compiler helps write code that cooperates with it rather than fighting it ("mechanical sympathy").

### CPU and Memory Wall Problem

The primary bottleneck in modern computing is not CPU speed but memory access latency. CPU cores are fast (0.3 ns cycle time) but main memory access is slow (50-100 ns). This gap is the "memory wall."

### Hierarchical Cache System

To bridge the memory wall, CPUs use layered caches:

- **L1 cache**: ~0.9 ns, per-core, small (32-64 KB)
- **L2 cache**: ~3 ns, per-core, larger (256 KB-1 MB)
- **L3 cache**: ~20 ns, shared across cores, larger still (several MB)

Cache hits are fast; cache misses require going to main memory. Contiguous memory structures (arrays) are cache-friendly; pointer-chasing structures (linked lists) cause cache misses. This is why arrays often outperform linked lists in practice.

### Pipelining and Out-of-Order Execution

Modern CPUs use instruction pipelining (overlapping instruction execution stages) and out-of-order execution (reordering independent instructions to keep execution units busy). Branch prediction guesses which way conditional branches will go. Mispredictions cost 10-20 cycles. Writing branch-predictable code (e.g., sorting data before processing) can improve performance.

### Hyper-Threading

Hyper-Threading (or SMT) allows a single physical core to appear as two logical cores, sharing execution units. It improves throughput by 15-30% but does not double performance.

### Schedulers

**OS Scheduler (CFS)**: The Linux Completely Fair Scheduler allocates CPU time to threads. Context switches (~10 microseconds) are expensive. When a Go program uses more OS threads than physical cores, threads compete and context-switch.

**Go Runtime Scheduler**: Go's M:N scheduler maps many goroutines onto fewer OS threads. It uses work-stealing to balance load. Goroutines are cheap (~2 KB stack, fast creation). Channels synchronize goroutines using CSP (Communicating Sequential Processes).

**GOMAXPROCS**: Controls how many OS threads the Go runtime uses for goroutines. Defaults to the number of CPU cores.

### When to Use Concurrency

Concurrency is beneficial when:
- The program does I/O (network, disk) -- goroutines can wait while others work
- Work can be parallelized across multiple CPU cores
- Background tasks need to run independently

Concurrency is NOT beneficial when:
- The workload is purely CPU-bound on a single core
- Coordination overhead exceeds the work itself
- The number of goroutines is unbounded (can cause scheduler thrashing)

---

## Chapter 5. How Go Uses Memory Resource

### Do We Have a Memory Problem?

Memory is both the most used resource and the most common bottleneck. Symptoms include OOM kills, growing RSS, slow GC pauses, and increased latency during high allocation periods.

### Physical Memory

Memory is organized as cells (bytes), accessed via addresses. DRAM provides the main memory, with typical access latencies of 50-100 ns.

### Virtual Memory

The OS provides each process a virtual address space, mapped to physical memory through page tables (4 KB pages on Linux). The Memory Management Unit (MMU) translates virtual to physical addresses using TLB (Translation Lookaside Buffer) caches.

### OS Memory Management

The OS manages memory through:
- **Stack**: Automatic, per-goroutine, grows and shrinks
- **Heap**: Dynamic, managed by the allocator and garbage collector
- **Memory-mapped files**: Using `mmap` syscall for file-backed or anonymous memory

### OS Memory Mapping

`mmap` maps files or anonymous memory into the process address space. Go uses this for large allocations. Understanding virtual memory helps understand Go's memory behavior.

### Go Memory Management

Go manages memory transparently. Variables are allocated on the stack (fast, auto-freed) or heap (GC-managed). The compiler's escape analysis decides where variables go. In general:

- Stack allocation is essentially free
- Heap allocation requires the Go allocator and eventual garbage collection

### Values, Pointers, and Memory Blocks

Go uses value semantics by default. Passing a struct by value copies it. Pointers (`*T`) reference the original. Slices contain a pointer to an underlying array, a length, and a capacity. Strings are immutable slices of bytes.

Key insight: a slice with small length but large capacity keeps the entire underlying array alive. This is a common source of "memory leaks."

### Go Allocator

Go uses a specialized memory allocator (tcmalloc-inspired) that allocates memory from the OS in large chunks and subdivides it efficiently. Small objects (<32 KB) are allocated from per-CPU caches (mcache), avoiding locks.

### Garbage Collection

Go uses a concurrent, tri-color mark-and-sweep garbage collector. Key characteristics:

- **Concurrent**: GC runs alongside application code (with some stop-the-world phases)
- **Non-generational**: Unlike Java, Go GC does not distinguish young/old objects
- **Tuned by GOGC**: Default GOGC=100 means GC triggers when heap doubles. Higher values mean less frequent GC but more memory usage
- **GOMEMLIMIT**: Sets a soft memory limit; GC runs more aggressively near the limit

The GC overhead is proportional to the number of live pointers. Fewer pointers means less GC work.

---

## Chapter 6. Observability

### Observability

Observability is the ability to understand the internal state of a system from its external outputs. Three pillars: metrics, logging, and tracing. Profiling is a fourth pillar essential for efficiency work.

### Example: Instrumenting for Latency

The simplest instrumentation uses `time.Now()` and `time.Since()` to measure wall-clock time for operations. This raw event information is a starting point but insufficient for production systems.

### Logging

Logging records discrete events. Structured logging (key-value pairs) is preferred. Logger patterns (keeping a logger instance in structs) avoid global state. For efficiency, log sparingly on hot paths.

### Tracing

Distributed tracing tracks requests across service boundaries using trace IDs and spans. It is essential for debugging latency in microservices but has overhead. Plotka recommends OpenTelemetry for instrumentation.

### Metrics

Metrics aggregate measurements into numeric time series. Key concepts:
- **Counter**: Monotonically increasing (e.g., request count)
- **Gauge**: Point-in-time value (e.g., current memory usage)
- **Histogram/Summary**: Distribution of values (e.g., request latency percentiles)

Plotka recommends Prometheus for metrics. Cardinality (number of unique label combinations) must be controlled to prevent metric storage explosion.

### Efficiency Metrics Semantics

**Latency**: Measure percentiles (p50, p90, p99), not averages. Averages hide outliers. Understand what you measure -- wall-clock time vs. CPU time, end-to-end vs. server-side latency.

**CPU Usage**: Can be measured as CPU time (actual CPU cycles used) or CPU utilization (percentage of available cycles). These differ significantly for I/O-bound workloads.

**Memory Usage**: Multiple metrics exist -- RSS (Resident Set Size from OS), heap size (from Go runtime), allocated objects, GC pressure. Understanding the difference is critical.

---

## Chapter 7. Data-Driven Efficiency Assessment

### Complexity Analysis

**"Estimated" Efficiency Complexity**: Running benchmarks and computing per-element cost (e.g., "6.9 * N nanoseconds per line") gives practical complexity estimates.

**Asymptotic Complexity with Big O Notation**: Theoretical analysis classifies algorithms as O(1), O(log N), O(N), O(N log N), O(N^2), etc. Big O describes the upper bound of growth rate. Big Theta gives tight bounds.

**Practical Applications**: Complexity analysis helps predict how code scales. Combined with napkin math (rough estimates using known hardware latencies), it provides early feedback on whether an approach is viable.

### Reliability of Experiments

Experiments (benchmarks) can be unreliable due to:

- **Performance nondeterminism**: OS scheduling, CPU frequency scaling, cache state, and background processes add noise. Mitigate with pinning, disabling turbo boost, and repeated runs.
- **Human errors**: Wrong test setup, incorrect measurements, misinterpretation. Document everything.
- **Reproducing production**: Local environments differ from production in hardware, data, network, and load. Use production-like conditions.
- **Benchmarks can lie**: Microbenchmarks may be optimized away by the compiler, may not reflect real allocation patterns, and may not show GC effects.

### Efficiency Metrics Semantics (Deep Dive)

Understanding metric semantics is critical. Latency measured at different points tells different stories. CPU usage as time vs. utilization differs. Memory has RSS, heap, stack, and GC overhead. The chapter provides detailed guidance on choosing and interpreting metrics for different optimization goals.

---

## Chapter 8. Benchmarking

### The Art of Benchmarking

Benchmarking is the empirical assessment of software efficiency. The formula:

**Benchmark = N * (Experiment + Measurements) + Comparison**

### Benchmarking Levels

Three levels of benchmarking:

1. **Microbenchmarks**: Test individual functions using Go's `testing.B`. Fast feedback, precise, but may not reflect reality.
2. **Macrobenchmarks**: Test entire systems end-to-end (e.g., using k6 for load testing). Slower feedback but more realistic.
3. **Benchmarking in Production**: Testing on real traffic (A/B testing, canary deploys). Most realistic but risky.

### Go Benchmarks (Microbenchmarks)

Go benchmarks use `BenchmarkXxx(b *testing.B)` functions in `_test.go` files:

```go
func BenchmarkSum(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Sum("test.txt")
    }
}
```

Key conventions:
- Use `b.ReportAllocs()` to track allocations
- Use `b.ResetTimer()` to exclude setup time
- Use `benchstat` to compare results statistically
- The `-benchmem` flag shows allocation stats

### Understanding Results

`benchstat` computes statistics (mean, confidence intervals) from multiple runs. Always run benchmarks multiple times and compare with benchstat, never rely on a single run.

### Compiler Optimizations Versus Benchmarks

The Go compiler can optimize away benchmark code if results are unused. Use the `Sink` pattern or global variables to prevent dead code elimination. Always verify the benchmark actually exercises the code you intend to measure.

### Microbenchmarks Versus Memory Management

Microbenchmarks do not accurately reflect GC behavior. The GC runs are less frequent in short benchmarks, so memory usage appears lower than in production. Maximum memory usage, peak RSS, and GC pauses may not be visible.

### Macrobenchmarks

Macrobenchmarks test the entire system:

**Basics**: Use tools like k6, Vegeta, or custom load generators to simulate real traffic patterns.

**Go e2e Framework**: Plotka's own framework (`github.com/efficientgo/e2e`) uses Docker containers to create isolated, reproducible test environments for Go services.

**Server-Side Latency**: Measure end-to-end request latency under load. Different latency granularities (client-side, server-side, function-level) serve different debugging purposes.

**CPU Time**: Macrobenchmarking reveals real CPU usage patterns, including GC overhead, scheduler contention, and I/O waits.

**Memory**: Observe RSS, heap profiles, and GC metrics over sustained load. Memory leaks that do not appear in microbenchmarks become visible.

### Common Macrobenchmarking Workflows

Plotka recommends a disciplined workflow:
1. Define what to test
2. Set up the environment
3. Document all experiment details
4. Run the benchmark, check for errors
5. Capture metrics, profiles, and observations
6. Compare with previous versions

---

## Chapter 9. Data-Driven Bottleneck Analysis

### Root Cause Analysis, but for Efficiency

Profiling is the primary tool for finding efficiency bottlenecks. It answers: "Where does my program spend its time or memory?"

### Profiling in Go

Go has built-in profiling support via the `runtime/pprof` and `net/http/pprof` packages.

**pprof Format**: Go uses the pprof profile format, which records resource usage (CPU time, memory allocations, goroutines, etc.) with stack traces.

**Capturing Profiles**:

```go
// CPU profile
f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()

// Heap profile
f, _ := os.Create("mem.prof")
pprof.WriteHeapProfile(f)
```

For long-running services, `net/http/pprof` exposes profiles via HTTP endpoints.

### Common Profile Instrumentation

**CPU Profile**: Shows where CPU time is spent. Records stack traces at 100 Hz sampling rate.

**Heap Profile**: Shows memory allocations. Four key metrics:
- `alloc_space`: Total bytes allocated (cumulative)
- `alloc_objects`: Total objects allocated
- `inuse_space`: Bytes currently in use
- `inuse_objects`: Objects currently in use

**Goroutine Profile**: Shows all live goroutines with their stack traces. Useful for detecting goroutine leaks.

**Block Profile**: Shows where goroutines block on synchronization primitives (channels, mutexes). Requires `runtime.SetBlockProfileRate()`.

**Mutex Profile**: Shows contention on mutex locks. Requires `runtime.SetMutexProfileFraction()`.

**Off-CPU Time**: Time spent waiting (not on CPU). Tools like `fgprof` can capture this, showing wall-clock time including I/O waits.

### go tool pprof Reports

The `go tool pprof` CLI and web UI provides several views:

**Top Report**: Text-based list of functions ranked by resource usage.

**Graph View**: Node-and-edge graph showing call hierarchy with node sizes proportional to resource usage.

**Flame Graph (Icicle Graph)**: Stack traces visualized as stacked rectangles. Width represents time/resource. Essential for quickly identifying hot paths.

**Source View**: Shows resource usage annotated on source code lines.

**Disassemble View**: Shows resource usage at the Assembly instruction level.

### Capturing the Profiling Signal

Use `go tool pprof -http=:8080 <profile_file>` to launch the web UI. For running services, use `go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30`.

### Tips and Tricks

- Profile during representative load
- Use `go tool pprof -http` for interactive exploration
- Focus on the biggest contributors first
- Use `-focus` and `-ignore` flags to filter noise
- Profile multiple resources (CPU + memory + goroutines) to build a complete picture

### Sharing Profiles

Profiles can be saved as files and shared. The pprof format is self-contained.

### Continuous Profiling

Tools like Parca, Polar Signals, and Pyroscope provide continuous profiling in production, sampling profiles at regular intervals and storing them for analysis. This is invaluable for finding regressions and understanding production behavior.

### Comparing and Aggregating Profiles

`go tool pprof` can diff profiles: `go tool pprof -base profile1.prof profile2.prof` shows the difference. Continuous profiling tools offer timeline views to see changes over time.

---

## Chapter 10. Optimization Examples

This chapter provides a detailed walkthrough of optimizing a simple `Sum` function that reads integers from a file and sums them, using the TFBO flow.

### The Starting Point

The naive implementation reads the entire file, splits by newlines using `bytes.Split`, converts each line to an integer using `strconv.ParseInt`, and sums them.

Initial benchmark results (10 million lines): ~505 ms latency, ~60 MB memory per operation.

### Optimizing Latency

**Step 1: Profile to find the bottleneck**

CPU profiling shows `bytes.Split` and `strconv.ParseInt` dominate. `bytes.Split` allocates a massive slice of byte slices.

**Step 2: Optimize bytes.Split**

Replace `bytes.Split` with a manual loop iterating over bytes, finding newlines, and parsing integers in-place. This eliminates the massive allocation of intermediate slices and combines two passes (split + parse) into one.

Result: ~107 ms, ~30 MB (both roughly halved).

**Step 3: Optimize string conversion**

The loop still converts `[]byte` to `string` for `strconv.ParseInt`. This `runtime.slicebytetostring` conversion allocates. Solution: write a custom `ParseInt` that works directly on `[]byte`, avoiding the string conversion.

Result: ~93 ms, ~30 MB.

**Step 4: Optimize strconv.ParseInt further**

The custom `ParseInt` strips leading whitespace and handles negative signs not needed for the input format. Removing these unnecessary checks reduces work further.

Result: ~67 ms, ~30 MB.

### Optimizing Memory Usage

Goal: Reduce memory from ~30 MB to under 10 KB.

**Step 5: Move to a streaming algorithm**

Instead of reading the entire file into memory, read it in chunks using a fixed-size buffer:

```go
func Sum6Reader(r io.Reader, buf []byte) (int64, error) {
    var ret int64
    var offset int
    for {
        n, err := r.Read(buf[offset:])
        // Process lines in buf[0 : offset+n]
        // Shift remaining bytes to front of buf
    }
    return ret, nil
}
```

Using an 8 KB buffer, each chunk is processed line by line, and partial lines are shifted to the front of the buffer for the next read. Result: ~69 ms, ~8 KB -- constant space complexity regardless of file size.

### Optimizing Latency Using Concurrency

Goal: Reduce latency to ~2.5 ns per line using 4 CPU cores.

**Naive Concurrency (ConcurrentSum1)**: Spin a goroutine for each line, using `atomic.AddInt64`. Result: 540 ms -- 40x slower due to goroutine creation overhead and scheduler thrashing.

**Worker Approach with Distribution (ConcurrentSum2)**: Fixed number of worker goroutines receiving work through a channel. Result: 207 ms -- still 15x slower because channel communication overhead exceeds the work itself.

**Worker Approach Without Coordination (ConcurrentSum3)**: Sharding -- split file bytes evenly among workers with no communication. Each worker knows its byte range. Result: 7 ms -- ~2x faster than sequential.

**Streamed, Sharded Worker Approach (ConcurrentSum4)**: Each worker reads its portion of the file directly using `io.SectionReader`, combining streaming with sharding. Result: 4.5 ms for 2M lines, ~2.3 * N ns throughput.

### Bonus: Thinking Out of the Box

A simple cache using `map[string]int64` reduces amortized complexity to ~228 ns per operation with 0 bytes allocated. Caching is the ultimate optimization when the same inputs repeat.

### Summary of Optimization Journey

| Version | Latency (10M lines) | Memory |
|---------|---------------------|--------|
| Naive Sum | ~505 ms | ~60 MB |
| Without bytes.Split | ~107 ms | ~30 MB |
| Custom ParseInt | ~67 ms | ~30 MB |
| Streaming (Sum6) | ~69 ms | ~8 KB |
| Concurrent (ConcurrentSum4) | ~23 ms | ~30 KB |

Key lesson: Benchmarking and profiling at every step is essential. Optimizations that seem obvious (naive concurrency) can make things worse. Data-driven decisions are paramount.

---

## Chapter 11. Optimization Patterns

### Be a Mindful Go Developer

Patterns in this chapter are deliberate optimizations -- use them only when benchmarks confirm they improve your specific workload.

### Common Patterns

Four high-level optimization patterns:

**1. Do Less Work**
- Skip unnecessary logic (strip unused checks from generic functions)
- Do things once (avoid redundant loops, reuse memory)
- Leverage math (estimate instead of counting)
- Use precomputed information

Example: Using `struct{}` instead of `any` for map values when the value is unused saves 5x memory and is 22% faster.

**2. Trading Functionality for Efficiency**
Remove features from critical paths that are rarely used or can be moved elsewhere.

**3. Trading Space for Time**
Precompute results, add caches, augment data structures with extra fields, decompress data to save CPU time.

**4. Trading Time for Space**
Compress data, remove extra struct fields, recompute instead of cache.

### The Three Rs Optimization Method

Borrowed from ecology (reduce, reuse, recycle):

**Reduce Allocations**: Fewer allocations means less GC work. Techniques: pre-allocate slices/maps, string interning, avoid unnecessary `[]byte`-to-`string` conversions, ensure variables do not escape to heap.

**Reuse Memory**: Reuse buffers, slices, and objects across operations. Pass buffers as parameters. Use streaming algorithms.

**Recycle**: Let the GC do its job efficiently. Reduce pointers in structs (pointer-free objects are cheaper for GC). Tune `GOGC` and `GOMEMLIMIT`. For Kubernetes workloads, set `GOMEMLIMIT` to 90-95% of the pod memory limit.

### Don't Leak Resources

**Control the Lifecycle of Your Goroutines**: Every goroutine must have a clear exit strategy. Use `goleak` (from Uber) in tests to detect goroutine leaks. A common pattern:

```go
// WRONG: leaks goroutine on cancellation
go func() { respCh <- ComplexComputation() }()
select {
case <-ctx.Done():
    return  // Goroutine left behind!
case resp := <-respCh:
    // ...
}
```

Fix: Always read from the channel to unblock the goroutine:

```go
resp := <-respCh  // Always read, even after cancellation
if ctx.Err() != nil {
    return
}
```

**Reliably Close Things**: Always close resources (files, HTTP bodies, context cancellers). Use `errcapture.Do` to capture close errors in defers:

```go
defer errcapture.Do(&err, f.Close, "close file")
```

**Exhaust Things**: HTTP response bodies must be fully read and closed to enable TCP connection reuse. Failing to exhaust can cause 29% latency overhead due to TCP connection re-establishment.

### Pre-Allocate If You Can

Always pre-allocate when you know the size:
- `make([]string, 0, size)` for slices -- 8x faster, 5x less memory
- `make(map[int]string, size)` for maps -- 2x faster, 2x less memory
- `buf.Grow(size)` for `bytes.Buffer` and `strings.Builder`
- `io.ReadFull` instead of `io.ReadAll` when size is known -- 8x faster

Pre-allocate linked list nodes in a single `[]Node` slice instead of individual allocations -- 4x faster with one allocation instead of millions.

### Overusing Memory with Arrays

A critical gotcha: when using a pre-allocated pool (like `[]Node`) or subslicing, deleting elements does not release the underlying array. The GC sees the large array as still referenced (even if only one element is used).

Example: A linked list with 1 million nodes pre-allocated in a pool still uses ~15 MB after deleting all but one node. Solution: implement a `ClipMemory()` method that copies live objects to a smaller array.

This also applies to zero-copy `[]byte`-to-`string` conversions: a small substring keeps the entire original byte array alive.

### Memory Reuse and Pooling

**Simple Buffer Reuse**: Pass a buffer as a parameter and reuse it:

```go
func processUsingBuffer(buf []byte) {
    buf = buf[:0]  // Reset length, keep capacity
    // Use buf...
}
```

**sync.Pool**: The standard library's pooling mechanism. Important characteristics:
- Objects are pooled only until the next GC cycle (then cleared)
- Thread-safe with minimal locking
- `Get()` returns `any` -- requires type assertion

Common bugs with sync.Pool:
- `defer p.Put(buf)` evaluates `buf` at defer time, not at execution time. If `append` grows the slice, the original (not current) slice is returned to the pool
- After GC, all pooled objects are lost, causing allocation spikes

**When to use sync.Pool**:
- Reusing large or extreme numbers of objects
- Objects are interchangeable (content does not matter)
- Multiple goroutines need objects
- Objects are reused quickly (within one GC cycle)

**When NOT to use sync.Pool**:
- Long-lived objects
- Objects that need to survive GC
- Single-goroutine scenarios (use simple buffers instead)
- When maximum memory usage matters more than allocation speed

The chapter concludes with a detailed experiment comparing no-buffering, sync.Pool, bucketed pool, and static buffers on both micro and macro levels. The surprising result: the simple no-buffering approach had the lowest maximum heap usage in macrobenchmarks, despite higher total allocations. Microbenchmark results were misleading.

---

## Key Takeaways

1. **Software efficiency is a critical engineering discipline**, not a luxury. Small inefficiencies compound dramatically at scale (a single function allocating 1 MB can waste 10 TB over 100 runs by 100 users).

2. **Be pragmatic, not obsessed**. Set clear, written efficiency goals using RAER (Resource-Aware Efficiency Requirements). No optimization is premature when done within the premise of requirements.

3. **Use the TFBO flow** (Test-Driven Flow for Better Optimization): implement functionality first with tests, then measure efficiency, then optimize iteratively with benchmarks confirming each step.

4. **Never optimize without data**. Always profile first to find the bottleneck. Use CPU profiling, heap profiling, and goroutine profiling. Tools: `go tool pprof`, Parca for continuous profiling.

5. **Benchmarking levels matter**. Microbenchmarks are fast but can mislead (compiler optimizations, no GC pressure, no real memory patterns). Always validate with macrobenchmarks under realistic load.

6. **The four optimization patterns**: do less work, trade functionality for efficiency, trade space for time, trade time for space. Apply them in this order.

7. **The Three Rs**: Reduce allocations first, then reuse memory, then recycle (optimize GC). In that order.

8. **Pre-allocation is the easiest win**. Always pre-allocate slices, maps, and buffers when the size is known. It is both more efficient and more readable.

9. **Control goroutine lifecycles**. Every goroutine must have a clear termination strategy. Use `goleak` in tests. Leaked goroutines cause memory leaks that are hard to debug.

10. **Be careful with sync.Pool**. It has narrow use cases. After GC, all pooled objects are cleared. Simple static buffers often outperform sync.Pool in macrobenchmarks.

11. **Watch for array memory overuse**. Subslicing and pooled arrays keep the entire underlying array alive. Implement explicit clipping when objects are deleted.

12. **Concurrency is not a silver bullet**. Naive concurrency (goroutine per item) can be 40x slower. Coordination-free sharding with streaming is the pattern that delivers real speedups.

13. **Think out of the box**. Before deep optimization work, consider if caching, precomputation, or restructuring the problem can achieve goals with less effort.

14. **Invest in observability**. Prometheus for metrics, Jaeger/Tempo for tracing, Parca for continuous profiling. Without observability, efficiency work is blind guessing.

15. **Hardware is not getting faster fast enough**. Software bloat, growing data volumes, and plateauing clock speeds mean efficient code is increasingly important. The developer's role is to be the pragmatic mechanic: fix the leaks, ensure reliability, and optimize what matters.
