# 100 Go Mistakes and How to Avoid Them - Teiva Harsanyi

## Comprehensive Summary

---

## Chapter 1: Go - Simple to Learn but Hard to Master

Go was designed to be simple, with only 25 keywords and a straightforward syntax. A developer can become productive in Go within days. However, simplicity does not equal ease. Go's deliberate simplicity hides deep subtleties around concurrency, memory management, and idiomatic patterns that take significant experience to master.

The book categorizes the 100 mistakes into seven types:
- **Bugs** - Code that produces incorrect results
- **Needless complexity** - Over-engineering solutions
- **Weaker readability** - Code that's hard to understand
- **Suboptimal or unidiomatic organization** - Fighting the language's conventions
- **Lack of API convenience** - Poorly designed interfaces for callers
- **Under-optimized code** - Missing performance opportunities
- **Lack of productivity** - Failing to leverage Go's tooling

---

## Chapter 2: Code and Project Organization (Mistakes #1-#16)

### #1: Unintended Variable Shadowing

Variable shadowing occurs when a variable declared in an inner scope has the same name as one in an outer scope. This is legal Go but frequently introduces bugs.

```go
var client *http.Client // outer scope client
if tracing {
    client, err := createClientWithTracing() // shadows outer client!
    if err != nil {
        return err
    }
    log.Println(client) // uses inner client
}
// client here is still nil - the outer variable was never assigned
```

The fix is to either use a different variable name or use direct assignment (`=`) instead of short variable declaration (`:=`) when you want to assign to the outer variable.

### #2: Unnecessary Nested Code

Deep nesting makes code hard to read and maintain. The "happy path" should be aligned to the left, with error cases returning early.

Bad pattern:
```go
if condition {
    if anotherCondition {
        // do work
    } else {
        return errors.New("another condition failed")
    }
} else {
    return errors.New("condition failed")
}
```

Good pattern (early returns / guard clauses):
```go
if !condition {
    return errors.New("condition failed")
}
if !anotherCondition {
    return errors.New("another condition failed")
}
// happy path - do work
```

### #3: Misusing init Functions

`init()` functions run automatically when a package is imported, before `main()`. Problems with init:
- They have no return values, so errors can't be propagated
- They make testing harder (side effects on import)
- They create hidden dependencies between packages
- Order of execution across files in a package is not guaranteed

When init IS appropriate: registering drivers, database connections that never fail, or truly one-time setup where failure means the program shouldn't start.

### #4: Overusing Getters and Setters

Go doesn't have native getter/setter support. The convention is:
- Use a `Get` prefix only for boolean getters (e.g., `GetIsActive`)
- For other getters, just use the field name (e.g., `Name()` not `GetName()`)
- Don't blindly add getters/setters for every field - only create them when you need encapsulation, validation, or lazy computation

### #5: Interface Pollution

Interfaces should be created when you need polymorphism, not "just in case." Common mistakes:
- Creating interfaces before concrete implementations
- Making every struct implement an interface unnecessarily
- Creating single-implementation interfaces

When to use interfaces:
- When multiple types share common behavior
- When you need to decouple from a concrete implementation (for testing, mocking)
- When you need to enforce a contract across packages

### #6: Interface on the Producer Side

Interfaces should be defined by the consumer, not the producer. The package that uses an interface should define it, not the package that implements it. This follows Go's implicit interface satisfaction and keeps dependencies clean.

Example: If package A needs to call methods on types from package B, package A should define the interface it needs, not package B.

### #7: Returning Interfaces

Functions should return concrete types, not interfaces. This gives callers the full API of the concrete type while still allowing the result to be used wherever an interface is expected (Go's implicit satisfaction).

```go
// Bad: returns interface
func NewClient() Client { ... }

// Good: returns concrete type
func NewClient() *client { ... }
```

### #8: Using `any` Says Nothing

Using `interface{}` or its alias `any` as a parameter type provides zero type information. Prefer specific types or use generics when you need type flexibility.

```go
// Bad
func Process(data any) { ... }

// Better with generics
func Process[T any](data T) { ... }
```

### #9: Being Confused About When to Use Generics

Generics (added in Go 1.18) are powerful but should be used judiciously. Good use cases:
- Functions that operate on slices of any type (e.g., `slices.Contains`)
- Generic data structures (maps, sets, trees)
- Utility functions like `Filter`, `Map`, `Reduce`

Bad use cases:
- When a concrete type would be clearer
- When the type constraint is so narrow it only applies to one type
- Just because you can

### #10: Type Embedding Pitfalls

Embedding a type in a struct makes its methods available on the outer type. Problems arise when:
- The embedded type has methods you don't want to expose
- Embedding a mutex leaks the Lock/Unlock to external callers
- You embed for code reuse rather than composition

```go
// Bad: leaks mutex methods
type MyStruct struct {
    sync.Mutex
}

// Good: use a named field
type MyStruct struct {
    mu sync.Mutex
}
```

### #11: Not Using the Functional Options Pattern

For struct configuration with optional parameters, Go developers should use the functional options pattern instead of:
- Config structs (verbose, can't validate at construction)
- Builder pattern (not idiomatic Go)

```go
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080} // defaults
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### #12: Project Misorganization

Follow the standard Go project layout:
- `cmd/` - application entry points
- `internal/` - private application code
- `pkg/` - public library code (optional, debated)
- Package names should be short, meaningful, lowercase, single-word

Avoid deep nesting. Packages should be organized around domain concepts, not technical layers.

### #13: Creating Utility Packages

Packages named `util`, `common`, `shared`, or `base` are code smells. They become junk drawers. Instead, create meaningful package names:

```go
// Bad: util.NewStringSet(), util.SortStringSet()
// Good: stringset.New(), stringset.Sort()
```

### #14: Ignoring Package Name Collisions

Package names should not conflict with common standard library packages (e.g., don't name your package `strings` or `http`). This creates confusion when reading code.

### #15: Missing Code Documentation

Every exported type, function, variable, and constant should have a doc comment. The comment should start with the name of the thing being documented and be a complete sentence.

### #16: Not Using Linters

Essential Go linting tools:
- `golangci-lint` - aggregator for many linters
- `go vet` - finds common mistakes
- `staticcheck` - advanced static analysis
- Configure them in CI/CD to catch issues before review

---

## Chapter 3: Data Types (Mistakes #17-#29)

### #17: Octal Literal Confusion

Go supports decimal, hexadecimal, octal, and binary literals. Octal starts with `0` (e.g., `010` = 8 in decimal). This can cause confusion, especially with file permissions: `0644` is octal notation.

### #18: Neglecting Integer Overflows

Go integers have fixed sizes (int8, int16, int32, int64). Operations can overflow silently:
- `int8(127) + 1` wraps to -128
- Always check for overflow when dealing with external input or critical calculations
- Use the `math` package constants (`math.MaxInt32`, etc.) for bounds checking

### #19: Not Understanding Floating Points

Floats are IEEE 754 binary floating-point numbers. Key issues:
- They can't precisely represent many decimal numbers (0.1 cannot be exactly represented)
- Comparisons should use a tolerance threshold
- For financial calculations, use integer arithmetic (cents) or a decimal library

### #20: Slice Length and Capacity

A slice has both a length (number of elements) and a capacity (size of the backing array). Understanding the difference is crucial:
- `len(s)` - number of elements currently in the slice
- `cap(s)` - total capacity of the backing array
- `make([]int, 3, 10)` creates a slice with length 3 and capacity 10
- `append` increases length; when length reaches capacity, a new backing array is allocated

### #21: Inefficient Slice Initialization

When you know the final size, preallocate:
```go
// Bad: grows backing array multiple times
var s []int
for i := 0; i < n; i++ {
    s = append(s, i)
}

// Good: single allocation
s := make([]int, 0, n)
for i := 0; i < n; i++ {
    s = append(s, i)
}
```

### #22: nil vs Empty Slices

- `nil` slice: `var s []int` - has no backing array, len=0, cap=0
- Empty slice: `s := []int{}` or `s := make([]int, 0)` - has a backing array, len=0, cap=0

Both behave identically with `append` and `len`, but `nil` slices are the idiomatic default for "no elements." JSON encoding differs: nil slice → `null`, empty slice → `[]`.

### #23: Checking if a Slice is Empty

Use `len(s) == 0`, not `s == nil`. A nil slice and an empty slice both have length 0, and `len` works correctly for both.

### #24: Not Making Slice Copies Correctly

```go
src := []int{1, 2, 3}
dst := make([]int, len(src))
copy(dst, src)
```

Simply assigning `dst := src` copies the slice header, not the underlying data. Both slices share the same backing array.

### #25: Unexpected Side Effects with Slice Append

`append` may or may not allocate a new backing array. If there's spare capacity, it modifies the original backing array:
```go
s1 := make([]int, 3, 10)
s2 := append(s1[:3], 4) // overwrites s1's backing array!
```

Use full slice expressions `s1[:3:3]` to prevent `append` from accessing spare capacity.

### #26: Slices and Memory Leaks

Two leak scenarios:
1. **Leaking capacity**: A large slice, when sliced to a small portion, keeps the entire backing array alive. Use copy or full slice expression to release memory.
2. **Slice of pointers**: A slice of pointers keeps all pointed-to objects alive even after they're no longer needed. Set unused elements to nil.

### #27: Inefficient Map Initialization

Like slices, maps should be preallocated when the size is known:
```go
m := make(map[string]int, 1000) // avoids runtime resizing
```

### #28: Maps and Memory Leaks

Maps never shrink. Once entries are added and later deleted, the memory isn't returned. Solutions:
- Periodically recreate the map
- Use a map of pointers and nil out deleted values
- Use a specialized data structure if this is a problem

### #29: Comparing Values Incorrectly

Slices, maps, and functions can't be compared with `==`. Use `reflect.DeepEqual` for deep comparison, or implement custom comparison logic. For byte slices, use `bytes.Equal`.

---

## Chapter 4: Control Structures (Mistakes #30-#35)

### #30: Elements Are Copied in Range Loops

The range loop copies each element into the loop variable:
```go
type Foo struct {
    bar int
}
foos := []Foo{{bar: 1}, {bar: 2}}
for _, foo := range foos {
    foo.bar = 99 // modifies the copy, not the original!
}
```

To modify the original, use the index or a pointer slice.

### #31: Range Loop Expression Evaluation

The range expression is evaluated once, before the loop starts. For channels, this means the variable is captured at the start. For arrays, it means a copy of the entire array is made.

### #32: Pointer Elements in Range Loops

Taking the address of the loop variable creates a single pointer that gets overwritten each iteration:
```go
for _, v := range values {
    go func() {
        fmt.Println(&v) // all goroutines print address of last element!
    }()
}
```

Fix by creating a local copy inside the loop or passing as a parameter.

### #33: Map Iteration Assumptions

Map iteration order is random by design in Go. Never assume ordering. Also, modifying a map during iteration (adding/deleting keys) produces undefined results.

### #34: Break Statement Scope

A `break` inside a `select` or `switch` only breaks out of that statement, not a surrounding `for` loop. Use labeled breaks:
```go
loop:
    for {
        select {
        case <-ch:
            break loop // breaks the for loop
        }
    }
```

### #35: Using defer Inside a Loop

`defer` runs when the function returns, not when the loop iteration ends. Using defer in a loop accumulates resources until the function exits:
```go
// Bad: all files closed only when function returns
for _, path := range paths {
    f, _ := os.Open(path)
    defer f.Close()
}

// Good: use a closure or anonymous function
for _, path := range paths {
    func() {
        f, _ := os.Open(path)
        defer f.Close()
        // process f
    }()
}
```

---

## Chapter 5: Strings (Mistakes #36-#41)

### #36: Not Understanding Runes

Go strings are UTF-8 encoded byte sequences. A rune is a single Unicode code point. A single character like "é" might be 2 bytes, and emoji might be 4 bytes. Don't assume `len(s)` gives character count; use `utf8.RuneCountInString(s)` or `range` over the string.

### #37: Inaccurate String Iteration

Using index-based iteration gives bytes; using `range` gives runes:
```go
s := "hello世界"
for i := 0; i < len(s); i++ {
    // iterates over bytes, not characters
}
for i, r := range s {
    // iterates over runes, i is byte position
}
```

### #38: Misusing Trim Functions

- `strings.Trim` trims characters from a set
- `strings.TrimSuffix`/`strings.TrimPrefix` trims a specific string
- `strings.Trim(s, "123")` removes all 1s, 2s, and 3s from both ends, not the string "123"

### #39: Under-Optimized String Concatenation

Using `+` in a loop creates many intermediate strings. Use `strings.Builder`:
```go
var sb strings.Builder
for _, s := range parts {
    sb.WriteString(s)
}
result := sb.String()
```

### #40: Useless String Conversions

Avoid unnecessary conversions between `[]byte` and `string`. Each conversion allocates. If you're working with I/O, stay in `[]byte`. If you need string operations, stay in `string`.

### #41: Substrings and Memory Leaks

A substring operation shares the same backing array as the parent string. If you keep a small substring of a large string, the entire large string remains in memory. Use `strings.Clone()` or manual copying to release the parent.

---

## Chapter 6: Functions and Methods (Mistakes #42-#47)

### #42: Choosing the Right Receiver Type

Value receivers: use when the method doesn't modify the receiver, for small types, or when you want value semantics.

Pointer receivers: use when the method modifies the receiver, for large types (avoid copying), or when you need consistency (if one method uses a pointer, all should).

Be consistent: don't mix value and pointer receivers on the same type.

### #43: Named Return Parameters

Named returns improve readability and are used in the naked return pattern. They're also essential for `defer` to modify return values:
```go
func (c *Client) Get(url string) (resp *http.Response, err error) {
    defer func() {
        err = fmt.Errorf("Get %s: %w", url, err)
    }()
    // ...
    return
}
```

### #44: Named Return Parameter Side Effects

Named returns are initialized to their zero value. If you accidentally assign to them inside a naked return, you might return zero values unexpectedly.

### #45: Returning a nil Receiver

Returning a nil pointer to a struct but typing it as an interface doesn't make a nil interface:
```go
func Get() error {
    var p *MyError // nil pointer
    return p       // non-nil interface with nil underlying value!
}
```

The interface holds both a type and a value. If the type is set but the value is nil, the interface is not nil. This is a classic Go gotcha.

### #46: Using a Filename as Function Input

Functions should accept `io.Reader` or `io.Writer`, not filenames. This makes them testable (pass a `bytes.Buffer`) and reusable (works with files, network, memory).

### #47: How defer Evaluates Arguments and Receivers

Arguments to a defer call are evaluated at the time of the defer statement, not when the deferred function executes:
```go
i := 1
defer fmt.Println(i) // prints 1, not 2
i = 2
```

For methods, the receiver is also evaluated at defer time.

---

## Chapter 7: Error Management (Mistakes #48-#54)

### #48: Panicking

`panic` should only be used for truly unrecoverable situations (like index out of bounds or nil pointer). For expected failures (file not found, network timeout), return an `error`. Panic bypasses normal control flow and should not be part of your API contract.

### #49: When to Wrap an Error

Error wrapping (using `fmt.Errorf("context: %w", err)`) preserves the error chain for inspection with `errors.Is()` and `errors.As()`. Wrap when you want to add context. Use `%v` instead of `%w` when you want to transform the error without keeping the chain.

### #50: Checking Error Type Inaccurately

Use `errors.As()` to check for a specific error type in the chain:
```go
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    // handle path error
}
```

Don't use type assertions directly, as they won't work with wrapped errors.

### #51: Checking Error Value Inaccurately

Use `errors.Is()` to check for a specific error value:
```go
if errors.Is(err, os.ErrNotExist) {
    // handle file not found
}
```

Don't use `==` directly, as it won't work with wrapped errors.

### #52: Handling an Error Twice

Don't both log and return the same error. This leads to duplicate log entries. Handle it once - either log it or return it, not both:
```go
// Bad
if err != nil {
    log.Println(err)
    return err // logged AND returned
}
```

### #53: Not Handling an Error

Never ignore errors with `_`. Even if you can't think of what to do, at least log it. Ignored errors hide bugs.

### #54: Not Handling defer Errors

`defer f.Close()` ignores the error return. For write operations, this can silently lose data. Always check:
```go
defer func() {
    if err := f.Close(); err != nil {
        log.Printf("close error: %v", err)
    }
}()
```

---

## Chapter 8: Concurrency Foundations (Mistakes #55-#60)

### #55: Concurrency vs. Parallelism

Concurrency is about dealing with many things at once (structure). Parallelism is about doing many things at once (execution). Go's concurrency primitives (goroutines, channels) enable parallelism but don't guarantee it. A concurrent program may or may not run in parallel depending on available cores.

### #56: Thinking Concurrency Is Always Faster

Concurrency adds overhead (goroutine scheduling, context switches, synchronization). For small workloads or CPU-bound tasks with more goroutines than cores, concurrency can be slower than sequential code. Always benchmark.

### #57: Channels vs. Mutexes

Use channels when goroutines communicate by passing ownership of data. Use mutexes when goroutines share access to the same data. The Go aphorism: "Don't communicate by sharing memory; share memory by communicating."

### #58: Race Problems

**Data races** occur when multiple goroutines access the same memory simultaneously with at least one write. **Race conditions** are about timing affecting correctness, even without data races.

The Go memory model defines when writes are visible to other goroutines. Use the `-race` flag to detect data races.

### #59: Workload Types and Concurrency

Two workload categories:
- **CPU-bound**: Computation-heavy. Benefit from goroutines up to the number of CPU cores.
- **I/O-bound**: Waiting on external resources. Can benefit from many more goroutines than cores.

Choose your concurrency pattern based on workload type.

### #60: Misunderstanding Go Contexts

Contexts serve three purposes:
1. **Deadline**: `WithTimeout` / `WithDeadline` - cancel after a time
2. **Cancellation**: `WithCancel` - manual cancellation signals
3. **Values**: `WithValue` - request-scoped data (use sparingly, with custom types for keys)

Always propagate context through your call chain. Don't store contexts in structs.

---

## Chapter 9: Concurrency in Practice (Mistakes #61-#74)

### #61: Propagating an Inappropriate Context

Don't pass a context with a timeout meant for one operation to a long-running goroutine. Each operation should have its own context derived from the parent.

### #62: Starting a Goroutine Without Knowing When to Stop

Every goroutine should have a clear lifecycle. Use context cancellation, done channels, or WaitGroups to ensure goroutines stop when they're supposed to. Leaked goroutines cause memory leaks.

### #63: Goroutines and Loop Variables

The loop variable is shared across all iterations. In Go < 1.22, capturing it in a goroutine closure captures a reference that changes:
```go
for _, v := range values {
    go func() {
        process(v) // all goroutines see the last value!
    }()
}
```

Fix by passing as parameter: `go func(val int) { process(val) }(v)` or create a local copy.

### #64: Non-Deterministic select with Channels

When multiple `select` cases are ready, Go picks one randomly. Don't assume ordering. Use nested selects with defaults to implement priority.

### #65: Not Using Notification Channels

Notification channels carry no data, only a signal. Use `chan struct{}` instead of `chan bool`:
```go
done := make(chan struct{})
close(done) // signal
```

### #66: Not Using nil Channels

A nil channel blocks forever on send and receive. This is useful in select statements to dynamically disable cases:
```go
select {
case <-ch1: // active
case <-ch2: // if ch2 is nil, this case is disabled
}
```

This pattern allows graceful shutdown by setting channels to nil after closing.

### #67: Channel Size

Unbuffered channels (`make(chan int)`) synchronize sender and receiver. Buffered channels (`make(chan int, n)`) decouple them. Don't use buffered channels "for performance" without measuring. Buffer size should be informed by actual throughput measurements, not guesses.

### #68: String Formatting Side Effects

Calling methods that access shared state from inside string formatting (e.g., inside a `String()` method that acquires a lock) can cause deadlocks if the formatting routine also tries to acquire the same lock.

### #69: Data Races with append

`append` is not thread-safe. If multiple goroutines append to the same slice, you have a data race. Use a mutex or have each goroutine append to its own slice and merge afterward.

### #70: Mutexes with Slices and Maps

Maps are not safe for concurrent use. Use `sync.Mutex`, `sync.RWMutex`, or `sync.Map` for concurrent map access. The same applies to slices that are shared and modified.

### #71: Misusing sync.WaitGroup

Common mistakes:
- Forgetting to call `wg.Add(1)` before starting the goroutine
- Calling `wg.Add` inside the goroutine (race condition)
- Not using `wg.Done` in a defer

Pattern:
```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(item T) {
        defer wg.Done()
        process(item)
    }(item)
}
wg.Wait()
```

### #72: Forgetting About sync.Cond

`sync.Cond` is useful when goroutines need to wait for a condition and be woken up by another goroutine. Use `Broadcast()` to wake all waiters or `Signal()` to wake one.

### #73: Not Using errgroup

`errgroup` manages a group of goroutines and collects the first error. It combines WaitGroup semantics with error propagation:
```go
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return task1(ctx) })
g.Go(func() error { return task2(ctx) })
if err := g.Wait(); err != nil {
    return err
}
```

### #74: Copying sync Types

`sync.Mutex`, `sync.WaitGroup`, etc. must not be copied after first use. Always pass by pointer. Use `go vet` to detect copies.

---

## Chapter 10: The Standard Library (Mistakes #75-#81)

### #75: Wrong Time Duration

`time.Sleep` takes a `time.Duration`. `time.Sleep(1000)` is 1 microsecond, not 1 second. Always use explicit duration units: `time.Sleep(1000 * time.Millisecond)` or `time.Sleep(time.Second)`.

### #76: time.After and Memory Leaks

`time.After` creates a new ticker each time it's called. In a select loop, using `time.After` on every iteration creates timers that can't be GC'd until they fire:
```go
// Bad: creates new timer every iteration
for {
    select {
    case <-ch:
        // process
    case <-time.After(3 * time.Second):
        // timeout
    }
}

// Good: reuse timer
timer := time.NewTimer(3 * time.Second)
defer timer.Stop()
for {
    select {
    case <-ch:
        // process
    case <-timer.C:
        // timeout
    }
}
```

### #77: Common JSON Mistakes

- Type embedding can cause unexpected JSON serialization behavior
- `time.Time` contains both wall clock and monotonic clock; JSON marshal/unmarshal can lose monotonic portion
- Map of `any` requires type assertions to access values, making code fragile

### #78: Common SQL Mistakes

- `sql.Open` doesn't necessarily establish a connection (lazy)
- Configure connection pool settings (`SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`)
- Use prepared statements for repeated queries (performance + security)
- Handle NULL values using `sql.Null*` types or pointers
- Always check `rows.Err()` after iterating with `rows.Next()`

### #79: Not Closing Transient Resources

Always close HTTP response bodies, `sql.Rows`, and `os.File`. Use defer but remember to handle close errors for writable resources:
```go
defer func() {
    if err := f.Close(); err != nil {
        log.Printf("close error: %v", err)
    }
}()
```

### #80: Forgetting Return After HTTP Handler Write

After calling `w.Write()` or `w.WriteHeader()`, execution continues. Always return after writing an error response:
```go
http.Error(w, "bad request", http.StatusBadRequest)
return // don't forget this!
```

### #81: Using Default HTTP Client/Server

The default `http.DefaultClient` has no timeouts, which can hang indefinitely. Always create custom clients:
```go
client := &http.Client{
    Timeout: 5 * time.Second,
    Transport: &http.Transport{
        TLSHandshakeTimeout:   3 * time.Second,
        ResponseHeaderTimeout: 3 * time.Second,
    },
}
```

Similarly, configure server timeouts to prevent slowloris attacks.

---

## Chapter 11: Testing (Mistakes #82-#90)

### #82: Not Categorizing Tests

Separate tests by type:
- **Unit tests**: Fast, no external dependencies
- **Integration tests**: Use real databases, APIs
- **Functional/E2E tests**: Full system tests

Use build tags, environment variables, or short mode (`go test -short`) to control which tests run.

### #83: Not Enabling the -race Flag

Always run tests with `-race` in CI. Race conditions are some of the hardest bugs to find and reproduce:
```bash
go test -race ./...
```

### #84: Not Using Test Execution Modes

- `-parallel N`: Run test functions in parallel (default is GOMAXPROCS)
- `-shuffle=on`: Randomize test execution order to find test pollution (tests that depend on order)
- Add `t.Parallel()` inside test functions to enable parallel execution of subtests

### #85: Not Using Table-Driven Tests

The cornerstone of Go testing:
```go
tests := []struct {
    name     string
    input    int
    expected int
}{
    {"positive", 1, 2},
    {"negative", -1, 0},
    {"zero", 0, 1},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        result := fn(tt.input)
        assert.Equal(t, tt.expected, result)
    })
}
```

### #86: Sleeping in Unit Tests

Don't use `time.Sleep` to wait for async operations. Instead:
- Use channels/signals to synchronize
- Use `testify/assert.Eventually` or similar polling with timeout
- Make time injectable (accept a `now func() time.Time`)

### #87: Not Using Testing Utility Packages

- `net/http/httptest`: Create mock HTTP servers and recorders
- `testing/iotest`: Test error handling in io operations

### #88: Inaccurate Benchmarks

Common benchmark mistakes:
- Not calling `b.ResetTimer()` after setup
- Not considering compiler optimizations eliminating dead code (assign results to package-level variables)
- Not running enough iterations (`-benchtime` flag)
- Observer effect: the benchmark itself affects performance
- Use `benchstat` for statistically sound comparison

### #89: Not Using Testing Utility Packages

Use `httptest.NewServer` to create fake HTTP servers for testing HTTP clients. Use `httptest.NewRecorder` to test HTTP handlers without starting a real server.

### #90: Not Exploring All Go Testing Features

- Code coverage: `go test -coverprofile=coverage.out`
- Test from a different package (black-box testing) using `package_test` naming
- Setup/teardown with `TestMain`
- Cross-package coverage with `-coverpkg`

---

## Chapter 12: Optimizations (Mistakes #91-#100)

### #91: Not Understanding CPU Caches

CPU caches are crucial for performance. Key concepts:
- **Cache lines** (typically 64 bytes): data is fetched in chunks, not individual bytes
- **Spatial locality**: accessing nearby memory is faster
- **Temporal locality**: recently accessed data stays in cache

Optimization: Struct of slices vs. slice of structs. If you're iterating over one field, a struct of slices is faster because you get better cache utilization.

### #92: False Sharing

When multiple goroutines write to adjacent memory locations on the same cache line, they cause cache line bouncing between cores. Solution: pad data structures to align to cache line boundaries, or ensure each goroutine works on its own cache line.

### #93: Instruction-Level Parallelism

Modern CPUs execute multiple instructions simultaneously. Code with data dependencies prevents this. Restructure to reduce dependencies between operations to allow the CPU to pipeline instructions.

### #94: Data Alignment

Fields in a struct should be ordered by size (largest first) to minimize padding:
```go
// Bad: 24 bytes (with padding)
type Bad struct {
    a bool  // 1 byte + 7 padding
    b int64 // 8 bytes
    c int32 // 4 bytes + 4 padding
}

// Good: 16 bytes
type Good struct {
    b int64 // 8 bytes
    c int32 // 4 bytes
    a bool  // 1 byte + 3 padding
}
```

Use `unsafe.Sizeof` to check struct sizes.

### #95: Stack vs. Heap

Stack allocation is essentially free (just moving a pointer). Heap allocation requires the garbage collector. The Go compiler uses escape analysis to decide:
- If a value's lifetime is bounded by the function, it goes on the stack
- If it escapes (returned, stored in a struct, passed to an interface), it goes on the heap

Use `go build -gcflags="-m"` to see escape analysis decisions.

### #96: Reducing Allocations

Three strategies:
1. **API changes**: Use pointers instead of values for large return types
2. **Compiler optimizations**: Pre-allocate slices/maps
3. **sync.Pool**: Reuse objects across GC cycles. Useful for short-lived, frequently allocated objects.

### #97: Inlining

The Go compiler automatically inlines small functions. Inlining eliminates function call overhead and enables further optimizations. Don't prevent inlining by:
- Making functions too large
- Using complex control flow
- Using `defer` in hot paths (prevents inlining in some cases)

Check with `go build -gcflags="-m"`.

### #98: Go Diagnostics Tooling

**Profiling tools:**
- `go tool pprof`: CPU and memory profiling
- `runtime/pprof`: Programmatic profiling
- `net/http/pprof`: Web-based profiling for running services

**Execution tracer**: Visualize goroutine scheduling and system calls over time:
```bash
go test -trace=trace.out
go tool trace trace.out
```

### #99: How the GC Works

Go uses a concurrent, tri-color mark-and-sweep garbage collector:
- The GC runs concurrently with the application
- It targets a specific heap growth ratio (GOGC, default 100%)
- Reducing allocations reduces GC pressure
- `GOMEMLIMIT` (Go 1.19+) sets a soft memory limit

### #100: Go in Docker and Kubernetes

Running Go in containers requires awareness:
- The default `GOMAXPROCS` is the number of host CPUs, not container CPUs. Use `automaxprocs` to fix this.
- Container memory limits should account for Go's GC behavior
- Set `GOMEMLIMIT` to ~90% of the container memory limit
- Alpine-based images may have DNS resolution issues with Go's net resolver

---

## Final Words

The book emphasizes that writing correct, idiomatic, and performant Go code requires understanding not just the language syntax but the runtime behavior, memory model, and hardware architecture. The most important lessons:

1. **Readability first** - Optimize for clarity, not cleverness
2. **Understand the runtime** - Know how slices, maps, channels, and the GC work internally
3. **Test thoroughly** - Use `-race`, benchmarks, and table-driven tests
4. **Profile before optimizing** - Measure first, optimize second
5. **Stay idiomatic** - Go has strong conventions; follow them
6. **Every mistake is a learning opportunity** - Understanding *why* something is wrong is more valuable than memorizing rules

The 100 mistakes span from beginner gotchas (variable shadowing, nil vs empty slices) to advanced performance tuning (false sharing, cache line alignment, escape analysis). Mastering these concepts is what separates a Go developer who can write working code from one who can write excellent Go.
