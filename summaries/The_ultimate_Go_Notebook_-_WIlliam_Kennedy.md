# Summary: Ultimate Go Notebook

**Author:** William Kennedy with Hoanh An
**Edition:** First Edition, Version 1.0 (Patch 38)

This summary covers the entire book in detail, organized by chapter. The book is written as class notes from the Ultimate Go training course. It covers language mechanics, data structures, design philosophy, concurrency, testing, benchmarking, generics, profiling, and tracing -- all from a perspective of data-oriented design and mechanical sympathy with the hardware.

---

## Chapter 1: Introduction -- Design Philosophy

The book opens by establishing a mindset for engineering software. Kennedy argues that the industry has become impressed with large codebases and abstractions while forgetting that hardware is the platform and every decision carries a cost. He advocates for a shift from "throwing more hardware or developers" at problems toward writing mechanically sympathetic, data-oriented code.

**Core Design Philosophy (prioritized in order):**

1. **Integrity** -- Both micro (memory accuracy, type system) and macro (data transformations, error handling). Studies show 92% of critical failures come from bad error handling (35% incorrect handling, 25% simply ignoring errors). Writing less code directly reduces bugs (industry average: 15-50 bugs per 1,000 lines).

2. **Readability** -- Code must never lie. It should be written for the average developer to comprehend. Go's underlying machine is a real machine (not a VM), giving direct hardware access with abstraction.

3. **Simplicity** -- Hard to design, complicated to build. Encapsulation at the package level is Go's approach. "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."

4. **Performance** -- Never guess about performance. Measure, profile, then test. Productivity and performance are not mutually exclusive in Go.

**Data-Oriented Design** is presented as a core philosophy: "If you don't understand the data, you don't understand the problem." Data structures, not algorithms, are central to programming. Changing data layouts can yield more significant performance improvements than changing algorithms alone.

**Interface and Composition Design Philosophy:** Interfaces give programs structure, encourage composition, and enforce clean divisions. Don't group types by common DNA (inheritance) but by common behavior. Interfaces with more than one method have more than one reason to change.

**Concurrency Philosophy:** Applications must start up and shut down with integrity. All goroutines should terminate before main returns. Rate limiting, back-pressure monitoring, and timeout/cancellation via the Context package are essential. "No request or task is allowed to take forever."

**Channel Signaling:** Focus on signaling semantics, not data sharing. Unbuffered channels provide guarantees (receive before send) at the cost of unknown latency. Buffered channels reduce latency but sacrifice guarantees. Less is more with buffers.

---

## Chapter 2: Language Mechanics

### Built-in Types

Types provide integrity and readability by answering: (1) How much memory to allocate? (2) What does that memory represent? Non-precision types (e.g., `int`) have sizes based on the target architecture (4 bytes on 32-bit, 8 bytes on 64-bit). The **word size** matches pointer/integer size for a given architecture.

### Zero Value Concept

Every value in Go is initialized to its zero value state (all bits set to zero) unless explicitly initialized. This ensures data integrity:

| Type     | Zero Value |
|----------|-----------|
| Boolean  | `false`   |
| Integer  | `0`       |
| Float    | `0`       |
| String   | `""`      |
| Pointer  | `nil`     |

Use `var` for zero-value construction and the short declaration operator `:=` with `{}` for non-zero-value construction.

### Strings

Strings are two-word data structures: a pointer to a backing byte array and a length. Copying a string is always a two-word copy regardless of string size.

### Conversion vs Casting

Go has conversion, not casting. Bytes are copied to a new memory location for the new representation. The `unsafe` package enables actual casting but should be avoided.

### Struct and Construction Mechanics

Structs are composites of different fields and types. Padding and alignment are handled by the compiler. Fields should be laid out from highest allocation to lowest to minimize padding bytes. For example, reordering fields from `bool, int16, bool, float32` (12 bytes with padding) to `float32, int16, bool, bool` (8 bytes) eliminates unnecessary padding.

### Pointers

Pointers share values across program boundaries (function calls, goroutines). Each goroutine gets its own 2KB stack that can grow. Stack frames are sized at compile time. Values whose size is unknown at compile time must be allocated on the heap.

### Pass By Value

All data moves by value. Every function gets its own copy. Even pointer addresses are copied. The `&` operator gets an address; `*` dereferences it. This is pass-by-value, not pass-by-reference.

### Escape Analysis

The compiler's escape analysis algorithm determines if a value is constructed on the stack or heap. The rule is about **ownership**: if a value constructed in a function must exist after that function returns, it escapes to the heap. Returning a pointer causes escape; returning a value keeps it on the stack.

```go
func stayOnStack() user {         // No allocation - value copy returned
    u := user{name: "Bill"}
    return u
}
func escapeToHeap() *user {       // Allocation - pointer returned
    u := user{name: "Bill"}
    return &u
}
```

### Stack Growth

Go uses contiguous stacks. Before each function call, a preamble checks if enough stack space exists. If not, a new larger stack is allocated and memory is copied. No goroutine can have a pointer to another goroutine's stack due to the overhead of tracking pointer adjustments during growth.

### Garbage Collection

Once values escape to the heap, the GC's pacing algorithm determines the frequency of collections to maintain the smallest heap with best throughput.

### Constants

Go's constant system is unique. Constants can be **typed** or **untyped** (kind). Untyped numeric constants have 256-bit precision. Kind promotion handles arithmetic between different kinds. All constant evaluation happens at compile time.

### IOTA

`iota` provides successive integer constants within a const block, starting at 0 and incrementing by 1. Useful for bit-shift flag patterns (like the `log` package uses).

---

## Chapter 3: Data Structures

### CPU Caches

Performance today is about data flow through hardware. Accessing L1 cache takes ~0.5ns (6 instructions), L2 ~7ns (84 instructions), and main memory ~100ns (1,200 instructions). The cache line is 64 bytes. **Predictable access patterns** (contiguous memory, linear traversal) allow the hardware prefetcher to efficiently move data into caches.

Benchmarks demonstrate:
- **Row traversal** of a matrix: ~11ms (fastest -- cache-line prefetching works)
- **Linked list traversal**: ~28ms (moderate -- some cache misses but fewer TLB misses)
- **Column traversal**: ~126ms (slowest -- crosses page boundaries, no predictability)

### Translation Lookaside Buffer (TLB)

The TLB caches virtual-to-physical address translations. TLB misses cause large latencies because the OS must scan page tables. For memory-intensive applications, larger page sizes (1-2MB) can improve performance.

### Arrays and Slices

**Arrays** have fixed size known at compile time. Size is part of the type -- `[4]int` and `[5]int` are different types. Arrays provide contiguous memory with predictable strides.

**Slices** are Go's most important data structure -- a three-word header (pointer, length, capacity). Use value semantics to move slices around, but pointer semantics for reading/writing. The `append` function uses value-semantic mutation: it gets its own copy, mutates, and returns a copy.

Key behaviors:
- Slicing creates a new slice header sharing the same backing array
- Mutations through sliced views affect all shared views
- Three-index slicing `[a:b:c]` limits capacity to prevent append side effects
- The `copy` function performs shallow copies
- Growth: doubles capacity up to 1024 elements, then grows by 25%

**Warning:** Appending to a slice replaces the backing array. Any existing pointers to elements of the old backing array become stale.

### UTF-8

Go source code is UTF-8. Strings are bytes; code points (runes, alias for `int32`) are 1-4 bytes. Iterating over a string moves code point by code point.

### Maps

Maps use a hash map and bucket system. A nil map panics on use. Construct with `make` or literal syntax. Key lookup returns the value and an existence boolean. Map iteration order is undefined and random for larger maps. Keys must be comparable (no slices, maps, or functions).

---

## Chapter 4: Decoupling

### Methods

Methods provide data with behavior. **Value receivers** implement value semantics (operate on a copy); **pointer receivers** implement pointer semantics (operate on shared access). The Go compiler adjusts calls so both value and pointer variables can call methods regardless of receiver type. However, data semantic consistency is critical: do not mix value and pointer receivers on the same type.

### Data Semantic Guidelines

- **Built-in types** (numbers, strings, bools): Use value semantics
- **Internal types** (slices, maps, channels, functions, interfaces): Use value semantics for moving; pointer semantics for reading/writing
- **Struct types**: Evaluate if data is safe to copy. If safe, use value semantics. If uncertain, use pointer semantics. Look at factory function return types to determine the chosen semantics

Key principle: "Once I switch to pointer semantics, all future calls need to stick to pointer semantics. I can never go from pointer to value."

### Interfaces

Interfaces are **valueless types**. They declare a method set of behavior that concrete types must implement. Go uses convention over configuration -- no explicit `implements` declaration is needed.

**Polymorphism** means code changes behavior depending on the concrete data it operates on. Interface values are two-word internal types: the first word points to an iTable (type description + function pointers), the second points to the concrete value stored.

**Method Set Rules:**
- Values of type T can only use methods with value receivers
- Pointers to type T can use all methods
- When storing in an interface, methods must exist explicitly (no compiler adjustments)

### Embedding

Embedding promotes inner type fields and methods to outer types. It looks like inheritance but is about behavior promotion, not state reuse. Outer type methods override promoted inner type methods of the same name.

### Exporting

Identifiers starting with a capital letter are exported (accessible across packages). Be consistent with exporting -- mixing exported fields with unexported embedded types creates partial construction problems.

---

## Chapter 5: Software Design

### Grouping Different Types of Data

The book presents a detailed anti-pattern using Animal/Dog/Cat with embedding to simulate inheritance. The correct Go approach is to use **interfaces to group by behavior**, not by common DNA.

Guidelines: Declare types that represent something new. Don't create aliases just for readability. Embed for behavior, not state.

### Don't Design With Interfaces

Work in two modes: **programmer mode** (concrete, break walls, get things working) and **engineer mode** (refactor for readability, efficiency, abstraction, testability). Start with concrete solutions, then **discover** interfaces. "Don't design with interfaces, discover them." -- Rob Pike.

### Composition Pattern

The book walks through a complete refactoring example:
1. Start with concrete types (`Xenia` for pulling data, `Pillar` for storing data)
2. Build concrete functions (`Pull`, `Store`) operating on concrete types
3. Compose a `System` type via embedding
4. Identify change: systems may change (add `Alice`, `Bob`)
5. Create interfaces (`Puller`, `Storer`) to decouple
6. Compose larger interfaces from smaller ones (`PullStorer`)
7. Compose the System from interface types for maximum flexibility
8. Refactor for precision: remove unnecessary types and make function signatures ask only for what they need

```go
type Puller interface { Pull(d *Data) error }
type Storer interface { Store(d *Data) error }
// Compose from smaller interfaces:
type PullStorer interface { Puller; Storer }
```

### Implicit Interface Conversions

A value stored in a larger interface can be assigned to a smaller interface (the compiler knows the concrete value implements the smaller interface). The reverse requires a type assertion at runtime.

### Type Assertions

`m.(bike)` panics if the assertion fails. `b, ok := m.(bike)` is the safe form. Type assertions can test for specific concrete types or for interfaces (behavior-based checks).

### Interface Pollution

Signs of pollution: interfaces matching the entire API of a single concrete type; exported interfaces with unexported implementations; factory functions returning interface values. Use interfaces when users need to provide implementations, when multiple implementations exist, or when decoupling from identified change.

### Interface Ownership

In Go, the consumer declares the interface, not the producer. Application developers can define their own interfaces for third-party concrete types, enabling test mocks without modifying the original package.

### Error Handling

Errors are values implementing the `error` interface (`Error() string`). The `Error()` method is for logging, not parsing. Context is everything:

- **Error variables** (`ErrBadRequest`) identify specific errors via switch comparison
- **Custom concrete error types** (e.g., `UnmarshalTypeError`) carry structured state
- **Interface-based type checks** (e.g., testing for a `temporary` interface) maintain decoupling
- **Always use the `error` interface** as return type -- using concrete error types causes subtle nil-interface bugs

**Wrapping errors** adds context as errors propagate up the call stack. Use either Dave Cheney's `errors` package (`errors.Wrap`, `errors.Cause`) or the standard library (`fmt.Errorf` with `%w`, `errors.As`, `errors.Unwrap`).

---

## Chapter 6: Concurrency

### Scheduler Semantics

The Go runtime creates OS threads (M) attached to logical processors (P). Goroutines (G) are managed by the Go scheduler on top of the OS scheduler. Key definitions:

- **Concurrency**: Undefined out-of-order execution
- **Parallelism**: Executing instructions simultaneously on multiple cores
- **CPU-Bound Work**: Doesn't cause threads to wait (e.g., Fibonacci)
- **I/O-Bound Work**: Causes threads to wait (e.g., HTTP requests)
- **Synchronization**: Managing shared memory access between goroutines
- **Orchestration**: Signaling between goroutines

### Goroutine Basics

`runtime.GOMAXPROCS(1)` forces single-threaded execution. `sync.WaitGroup` provides orchestration: `Add(n)` sets the counter, `Done()` decrements it, `Wait()` blocks until zero. Keep `Add` and `Done` calls in the same line of sight. The scheduler is preemptive -- context switches are unpredictable and change on every run.

### Data Races

Data races occur when two or more goroutines access the same memory with at least one writing, without synchronization. They are **impossible to predict** and bugs can be hidden for years. A single added log statement can expose a latent data race.

Use the race detector: `go build -race`, `go test -race`.

### Atomics

Atomic operations provide hardware-level synchronization for individual words. Use precision-based integers (`int32`, `int64`). The `atomic` package provides `Add`, `CompareAndSwap`, `Load`, `Store`, `Swap`, and the `Value` type.

### Mutexes

Mutexes synchronize groups of operations. `Lock()` and `Unlock()` should be in the same function. Lock creates back-pressure -- minimize the time between lock and unlock. Never call `Lock` twice from the same mutex in the same function. **Read/Write Mutexes** (`sync.RWMutex`) allow multiple concurrent readers but exclusive writers.

### Channel Semantics

Channels are signaling mechanisms, not queues. Three key decisions:

1. **Guarantee level**: Unbuffered = guarantee at signaling level (receive before send). Buffered = guarantee outside signaling (send before receive).
2. **Data with signal**: Data signals are 1-to-1. Close signals (no data) can be 1-to-many.
3. **Channel state**: Open (constructed with `make`), nil (zero value, blocks send/receive), closed (receive returns immediately, send panics).

### Channel Patterns (7 patterns)

1. **Wait For Result**: Unbuffered channel; child goroutine signals result back to parent. Unknown latency cost.

2. **Fan Out/In**: Buffered channel sized to number of goroutines. One goroutine per work item. Counter tracks completion. Dangerous in services because goroutine count is a multiplier.

3. **Wait For Task**: Unbuffered channel; child goroutine waits for parent to send work. Foundation for pooling.

4. **Pooling**: Unbuffered channel with GOMAXPROCS-number of goroutines in a for-range loop. Efficient resource usage. Close the channel to signal shutdown.

5. **Drop**: Buffered channel with capacity limit. Uses `select` with `default` to drop work when at capacity. Critical for services under heavy load.

6. **Cancellation**: Context with timeout. Buffered channel of size 1 (so child goroutine can send even if parent walks away). Select between result and context cancellation.

7. **Fan Out Semaphore**: Controls concurrent execution with a semaphore channel sized to GOMAXPROCS. All goroutines created but only GOMAXPROCS execute simultaneously.

8. **Bounded Work Pooling**: Pool of goroutines processes a fixed amount of work. WaitGroup tracks completion. Close signals shutdown.

9. **Retry Timeout**: Retries an operation at intervals until context expires. Uses `time.NewTimer` inside a select.

10. **Channel Cancellation**: Bridges legacy channel-based cancellation to context-based cancellation.

---

## Chapter 7: Testing

### Unit Tests

A unit of code in Go is a package. Test files use the `_test.go` suffix. Test functions start with `Test` and take `*testing.T`. Using `_test` package suffix forces testing through the exported API.

```go
func TestDownload(t *testing.T) {
    resp, err := http.Get(url)
    if err != nil {
        t.Fatalf("unable to issue GET: %s", err)
    }
    defer resp.Body.Close()
    if resp.StatusCode != statusCode {
        t.Fatal("status codes don't match")
    }
}
```

`t.Fatal` fails and returns immediately; `t.Error` fails but continues. `t.Log` provides verbose output.

### Table Tests

Table tests use a slice of structs containing inputs and expected outputs. They are powerful for negative-path testing and make adding test cases trivial.

### Mocking with httptest

The `httptest.NewServer` function creates a mock HTTP server for testing without network access. Handler functions return controlled responses. This is preferred over external mocking frameworks.

### Internal Endpoint Testing

`httptest.NewRequest` and `httptest.NewRecorder` allow testing HTTP handlers directly through the mux without starting a server. Call `http.DefaultServeMux.ServeHTTP(w, r)` to process the request.

### Sub-Tests

`t.Run(name, func(t *testing.T))` creates named sub-tests. Create a local copy of loop variables to prevent closure bugs. `t.Parallel()` runs sub-tests concurrently. Sub-tests can be filtered individually on the command line.

---

## Chapter 8: Benchmarking

### Basic Benchmarks

Benchmark functions start with `Benchmark` and take `*testing.B`. The core loop iterates from `0` to `b.N`. The tooling determines `b.N` through trial and error, starting at 1 and multiplying by 100 until the desired `-benchtime` is met.

```bash
$ go test -bench . -benchtime 3s -benchmem
BenchmarkSprintf-16  80984947  42.46 ns/op  5 B/op  1 allocs/op
```

Key flags: `-bench .` (run all), `-benchtime 3s` (3 seconds), `-benchmem` (show allocations). Always capture return values to prevent compiler optimization from removing the code under test.

### Validate Benchmarks

Benchmarks lie. The book demonstrates with merge sort algorithms where running benchmarks together vs. in isolation produces different results due to goroutine cleanup from previous benchmarks. Rule #1: the machine must be idle. Run benchmarks in isolation for accurate results.

---

## Chapter 9: Generics (Go 1.18)

### Basic Syntax

Generic functions use square brackets for type parameters:

```go
func print[T any](slice []T) {
    for _, v := range slice {
        fmt.Print(v, " ")
    }
}
```

Type inference often eliminates the need to explicitly pass type arguments at call sites: `print(numbers)` works instead of `print[int](numbers)`.

### Underlying Types

Generic types can be based on underlying types:

```go
type vector[T any] []T
func (v vector[T]) last() (T, error) { ... }
```

Zero-value construction uses `var zero T` or `*new(T)`.

### Struct Types

Generic struct types enable container implementations (linked lists, etc.) without code duplication:

```go
type node[T any] struct {
    Data T
    next *node[T]
    prev *node[T]
}
```

### Behavior as Constraint

Interfaces serve as behavioral constraints for generics:

```go
func stringify[T fmt.Stringer](slice []T) []string { ... }
```

### Type as Constraint

New interface syntax lists allowed concrete types:

```go
type addOnly interface {
    type string, int, int8, int16, int32, int64, float64
}
func Add[T addOnly](v1 T, v2 T) T { return v1 + v2 }
```

`comparable` is a predeclared constraint for types usable in comparisons.

### Field Access

Generics allow accessing common fields across different struct types when those types are listed in the constraint interface. This avoids setter-based interface pollution.

### Slice Constraints

Constraints can restrict to actual slice types (not just underlying slice types), preserving user-defined type information through generic operations.

### Channels and Concurrency with Generics

Generic functions and types enable reusable concurrency patterns:

```go
type workFn[Result any] func(context.Context) Result
func doWork[Result any](ctx context.Context, work workFn[Result]) chan Result { ... }
```

### Hash Table Implementation

A complete generic hash table example demonstrates real-world generic usage with `Table[K comparable, V any]`, showing how generics eliminate code duplication for container types.

---

## Chapter 10: Profiling

### Profiling Basics

The profiler sends SIGPROF at regular intervals, capturing program counters. Types of profiling:

- **CPU profiling**: Records stack traces every ~10ms. Shows hottest code paths.
- **Memory profiling**: Records stack traces on heap allocation. Sample-based (default: 1 per 512KB). Does not track stack allocations.
- **Blocking profiling**: Records time goroutines wait for shared resources. Specialized -- use only after CPU and memory bottlenecks are resolved.

**One profile at a time.** Do not enable multiple profile types simultaneously.

### Practical Example: Stream Processing

The chapter walks through optimizing a byte-stream processing algorithm (`algOne`) compared to a friend's version (`algTwo`). Initial benchmarks show `algOne` at 1,594 ns/op with 2 allocations vs. `algTwo` at 388 ns/op with 0 allocations.

**Finding allocations with memory profiles:**
1. Run benchmark with `-memprofile p.out`
2. Use `go tool pprof` with `list algOne` to find specific allocating lines
3. Review escape analysis with `-gcflags -m=2`

**Inlining:** Factory functions like `bytes.NewBuffer` are inlined (scored by the compiler; must be under 80 cost points). Inlining moves ownership of value construction to the calling function, which can prevent unnecessary heap allocations.

**The root cause:** Passing a value to a polymorphic function (like `io.ReadFull` which accepts `io.Reader`) causes an interface conversion that forces the value to escape to the heap. The fix: call methods directly on the concrete value instead of through the `io` package.

**Final optimization:** Replacing `make([]byte, size)` with `make([]byte, 5)` (when size is known) eliminates the last allocation because the compiler knows the size at compile time. Result: 0 allocations, though still ~500ns slower than the alternative algorithm.

---

## Chapter 11: Profiling Live Code

### GC Traces

Use `GODEBUG=gctrace=1` to output GC traces. Each trace shows wall-clock times (STW mark setup, concurrent marking, STW mark termination), CPU times, memory usage (before/after/live), and collection goal.

### Load Testing

Using the `hey` tool for load testing: `hey -m POST -c 100 -n 10000 "http://localhost:5000/search?term=biden"`. Monitor GC trace during load to identify memory leaks (live memory should stabilize).

### Adding Profile Endpoints

Import `_ "net/http/pprof` to register debug routes. Bind the default mux to a separate debug port. Access profiles at `/debug/pprof/`.

### Identifying Bottlenecks

Use `go tool pprof` with the `top` and `list` commands to find allocation hot spots. In the example, `strings.ToLower` inside a loop accounted for 2.34GB of allocations (39.76% of total). The fix: move `strings.ToLower(term)` outside the loop and lowercase descriptions during caching.

Result: 88% improvement in requests/sec (from 3,711 to 6,960).

---

## Chapter 12: Tracing

### Generating Traces

```go
import "runtime/trace"
func main() {
    trace.Start(os.Stdout)
    defer trace.Stop()
    // ...
}
```

Run with `./trace > t.out` and review with `go tool trace t.out`. The trace viewer shows goroutines, heap memory, threads, GC events, syscalls, and processor activity down to the microsecond.

### Performance Optimization Walkthrough

Starting with a single-threaded file search (2,670ms, 275 GCs, 4MB heap), the chapter progressively optimizes:

1. **Fan-Out** (one goroutine per file): 580ms, but 53MB memory, 43% GC time. Uses `atomic.AddInt32` for shared counter. Cache-friendly optimization: local counting per goroutine, then atomic add once at the end.

2. **Pooling** (GOMAXPROCS goroutines): 1,000ms, 5MB memory, 60% GC time. Slower because GC runs 876 times keeping heap at 5MB.

3. **Pooling + GC Percentage** (`GOGC=1000` or `debug.SetGCPercent(1000)`): 397ms, 40MB memory, 27 GCs, 4% GC time. Best overall balance.

### Tasks and Regions

Use `trace.NewTask` and `trace.StartRegion` to instrument individual operations within goroutines, enabling per-file timing analysis in the trace viewer.

---

## Chapter 13: Stack Traces / Core Dumps

### Reading Stack Traces

Stack traces show function names, file/line numbers, and function input/output values as hex words. For a function like `example(slice []string, str string, i int) error`, the stack trace reveals the slice's pointer/length/capacity, the string's pointer/length, and the integer value. In Go 1.17+, the ABI changed to use registers, making some input values less accurate in traces.

### Full Stack Trace Analysis

The chapter provides detailed examples of reading goroutine stack traces during panics, including how to decode slice headers, string values, and interface types from the hex words in the trace output.

---

## Chapter 14: Blog Posts (Supplementary)

This chapter collects important blog posts referenced throughout the book:
- **Stacks and Pointer Mechanics**: Detailed explanation of stack frames, goroutine stacks, and pointer behavior
- **Escape Analysis Mechanics**: How the compiler decides stack vs. heap allocation
- **Garbage Collection Semantics**: GC pacing algorithm, heap sizing, and tuning
- **Scheduling in Go** (3 parts): Gos, OS scheduler, Go scheduler, work-stealing

---

## Key Takeaways

1. **Data-oriented design is paramount.** Understand the data, then structure it for mechanical sympathy with the hardware. Contiguous memory, predictable access patterns, and minimizing padding are critical for performance.

2. **Value vs. pointer semantics is a design decision, not a performance choice.** Be consistent within a type's method set. Once you switch to pointer semantics, stay there. Never go from pointer back to value.

3. **Interfaces are discovered, not designed.** Start with concrete solutions, then identify what changes and decouple with interfaces. Group by behavior, not by DNA. Keep interfaces small (single method when possible).

4. **Error handling is not an afterthought.** 92% of critical failures come from bad error handling. Always check errors. Wrap errors with context. Use the `error` interface as the return type (never concrete error types).

5. **Concurrency requires discipline.** Know how every goroutine terminates. Use WaitGroups for orchestration. Understand channel semantics (unbuffered = guarantee, buffered = reduced latency). Rate-limit, monitor back-pressure, and always use timeouts via Context.

6. **Profile before optimizing.** Never guess about performance. Use benchmarks, memory profiles, CPU profiles, and traces. The GC percentage knob can dramatically improve performance for pooling patterns.

7. **Write less code.** The industry average is 15-50 bugs per 1,000 lines. Reducing code reduces bugs, improves readability, and decreases maintenance burden.

8. **Correctness before performance.** Make it correct, clear, concise, then fast -- in that order. Premature optimization is the root of all evil. You can only optimize after you have something working that you can measure.

9. **Mechanical sympathy matters.** Go runs on a real machine, not a VM. Understanding CPU caches (L1/L2/L3), cache lines (64 bytes), TLB, and memory layout enables writing code that the hardware can execute efficiently.

10. **Generics enable reusable, type-safe abstractions.** Use them for container types and concurrency patterns. Prefer behavioral constraints (interfaces as type constraints) over type lists when possible. Write concrete implementations first, then generalize with generics.
