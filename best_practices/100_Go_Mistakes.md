# 100 Go Mistakes and How to Avoid Them
**Author:** Teiva Harsanyi
**Topic tags:** `#general` `#concurrency` `#testing` `#api` `#cli`
**Language focus:** Go-first
**Sources:** `markdown_output/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi.md` · `summaries/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi.md`

## TL;DR
A catalog of 100 recurring Go mistakes spanning code organization, data types, control flow, strings, functions, errors, concurrency (foundations + practice), the standard library, testing, and low-level optimizations. The through-line is that **simplicity ≠ easy**: Go's small surface area hides real traps around goroutines, channels, slices, escape analysis, and the runtime. Use the do/don't cluster per topic to harden code reviews, then lean on the cheat-sheets at the bottom for quick recall.

---

## Best Practices by Topic

### 1. Code & Project Organization (Mistakes #1–#16)

**Principle:** Discover abstractions (interfaces, generics, packages) — don't pre-create them. Keep the happy path on the left edge of the file.

**Do:**
- Use early returns / guard clauses; flatten nesting.
- Default to concrete types on outputs; accept interfaces on inputs.
- Name packages by what they *provide*, never `util` / `common` / `shared`.
- Document every exported symbol starting with its name; one sentence, ends with punctuation.
- Wire `golangci-lint` (`go vet`, `errcheck`, `staticcheck`, `gocyclo`, `goconst`) into CI.

**Don't:**
- Shadow a variable inside an `if` with `:=` when you meant to assign.
- Embed `sync.Mutex`, `io.WriteCloser`, or other "convenient" types inside exported structs.
- Pre-create interfaces with a single implementation "just in case."
- Build multi-arg config with config-structs of `*T` pointers to distinguish zero from absent.
- Skip `gofmt` / `goimports` because "the team knows the style."

**Code (shadowing, mistake #1):**
```go
var client *http.Client
if tracing {
    client, err := createClientWithTracing() // SHADOWS outer client; outer is still nil
    if err != nil {
        return err
    }
    log.Println(client) // uses inner client only
}
```
*Fix:* use a different name, or pass the inner client out explicitly: `client, err = createClientWithTracing()`.

**Code (functional options, mistake #11):**
```go
type options struct {
    port *int
}
type Option func(options *options) error

func WithPort(port int) Option {
    return func(o *options) error {
        if port < 0 {
            return errors.New("port should be positive")
        }
        o.port = &port
        return nil
    }
}

func NewServer(addr string, opts ...Option) (*http.Server, error) {
    var o options
    for _, opt := range opts {
        if err := opt(&o); err != nil {
            return nil, err
        }
    }
    // apply defaults + port-zero-means-random logic using o.port ...
}
```
*Ref: 100_Go_Mistakes.md — "#11 Not using the functional options pattern."*

---

### 2. Data Types — Integers, Floats, Slices, Maps (Mistakes #17–#29)

**Principle:** Slices are pointers (header + backing array). Maps never shrink. Floats are approximations. Integer overflow is silent.

**Do:**
- Use `0o644` not `0644` for octal literals; honor `math.MaxInt32`/`MaxInt64` when bounds matter.
- Preallocate slices with `make([]T, len, cap)` when the size is known.
- Use `len(s) == 0` to test emptiness — never `s == nil` or `s == nil` checks for receiver calls.
- Use `copy(dst, src)` with a destination that has `len(dst) >= len(src)`; alternative: `append([]int(nil), src...)`.
- Compare byte slices with `bytes.Equal`; deep-compare other types with `reflect.DeepEqual` (or a typed helper).
- Use `s[low:high:max]` (full slice expression) when handing a sub-slice to a function that may `append`.

**Don't:**
- Write `010` and expect ten.
- Compare floats with `==`; build tolerance into assertions.
- Use an empty-slice literal `[]string{}` as a default; favor `var s []string` (nil, zero alloc).
- Forget that `s1 := make([]int, 3, 6)` and `s2 := s1[1:3]` share the same backing array — `append(s2, x)` can clobber `s1`.
- Expect a deleted map entry to free memory; maps never shrink.
- Compare slices or maps with `==`.

**Code (slice append side effect, mistake #25):**
```go
s1 := []int{1, 2, 3}
s2 := s1[1:2]            // one-length, two-capacity slice
s3 := append(s2, 10)     // s2 isn't full ⇒ overwrites s1's backing array
fmt.Println(s1)          // [1 2 10]   ← unintended mutation
```
*Ref: 100_Go_Mistakes.md — "#25 Unexpected side effects using slice append."*

**Code (slice copy, mistake #24):**
```go
src := []int{0, 1, 2}
dst := make([]int, len(src)) // dst is zero-length if you omit len
copy(dst, src)               // copies min(len(src), len(dst))
```
*Ref: 100_Go_Mistakes.md — "#24 Not making slice copies correctly."*

**Code (slice leak, mistake #26):**
```go
// Leaks the whole backing array via the small sub-slice
small := big[:1]
```
*Fix:* `small := append([]int(nil), big[:1]...)`, or `full := big[:1:1]` with full-slice expression, or copy into a sized target: `small := make([]int, 1); copy(small, big[:1])`.

**Code (overflow detection, mistake #18):**
```go
func AddInt(a, b int) int {
    if a > math.MaxInt-b {
        panic("int overflow")
    }
    return a + b
}

func MultiplyInt(a, b int) int {
    if a == 0 || b == 0 {
        return 0
    }
    result := a * b
    if a == math.MinInt || b == math.MinInt {
        panic("integer overflow")
    }
    if result/b != a {
        panic("integer overflow")
    }
    return result
}
```
*Ref: 100_Go_Mistakes.md — "#18 Neglecting integer overflows."*

---

### 3. Control Structures (Mistakes #30–#35)

**Principle:** `range` evaluates its expression *once*; range copies each element; the loop variable is shared; defer schedules at function return, not iteration end.

**Do:**
- Mutate struct elements via the index (`for i := range xs { xs[i].foo++ }`) or by ranging over a pointer slice.
- Use a labeled `break loop` to escape a `for` from inside a `select`/`switch`.
- Move the loop body into its own function so `defer` fires per iteration:
  ```go
  for _, path := range paths {
      if err := handle(path); err != nil { return err }
  }
  func handle(path string) error {
      f, err := os.Open(path)
      if err != nil { return err }
      defer f.Close()
      // ...
      return nil
  }
  ```
- Loop over a channel without assuming the channel is fixed; range copies the channel value once.

**Don't:**
- "Modify" a value element from a range loop and expect the slice to change.
- Use `defer` directly inside a loop expecting per-iteration cleanup.
- `break` from inside a `select`/`switch` thinking it exits the outer `for`.
- Modify a map during `for range m` and assume deterministic inclusion of new keys.
- Print the loop variable from a goroutine without copying: all goroutines see the last value.

**Code (pointer element in range, mistake #32):**
```go
func (s *Store) storeCustomers(customers []Customer) {
    for _, customer := range customers {
        s.m[customer.ID] = &customer // SAME pointer each iteration ⇒ all keys point to last customer
    }
}
```
*Fixes:*
```go
// Option A: local variable
for _, customer := range customers {
    current := customer
    s.m[current.ID] = &current
}
// Option B: take pointer to slice element
for i := range customers {
    customer := &customers[i]
    s.m[customer.ID] = customer
}
```
*Ref: 100_Go_Mistakes.md — "#32 Ignoring the impact of using pointer elements in range loops."*

---

### 4. Strings (Mistakes #36–#41)

**Principle:** A Go string is `(pointer, length)` over arbitrary bytes (typically UTF-8 from literals). A `rune` is a Unicode code point (`int32`), 1–4 bytes when encoded.

**Do:**
- Iterate runes with `for i, r := range s { ... }`; `i` is the *byte* index.
- Use `utf8.RuneCountInString(s)` to count runes; `len(s)` is bytes.
- Use `strings.TrimSuffix` / `TrimPrefix` for an exact suffix/prefix; `strings.TrimRight`/`TrimLeft` for a *set* of runes.
- Concatenate ≥ ~5 strings with `strings.Builder` and pre-call `Grow(n)`.
- Use `bytes.TrimSpace`, `bytes.Split`, … instead of `string` ⇄ `[]byte` round-trips in I/O paths.
- `strings.Clone(s[i:j])` to detach a substring from a large backing array (Go 1.18+).

**Don't:**
- Index a string with `s[i]` and assume "the i-th rune."
- Build a result via `s += part` in a loop — every iteration reallocates because strings are immutable.
- Take a substring of a large string and keep it; the parent stays alive in memory.
- Use `string(bytes)` ⇄ `[]byte(s)` unnecessarily; conversions copy.

**Code (substring leak, mistake #41):**
```go
func (s store) handleLog(log string) error {
    if len(log) < 36 {
        return errors.New("log is not correctly formatted")
    }
    uuid := log[:36]                  // shares backing array with `log`
    s.store(uuid)                     // retains whole `log` in memory
    return nil
}
```
*Fix:* `uuid := strings.Clone(log[:36])` or `uuid := string([]byte(log[:36]))`.
*Ref: 100_Go_Mistakes.md — "#41 Substrings and memory leaks."*

**Code (string builder, mistake #39):**
```go
func concat(values []string) string {
    total := 0
    for _, v := range values {
        total += len(v)
    }
    sb := strings.Builder{}
    sb.Grow(total)
    for _, v := range values {
        _, _ = sb.WriteString(v)
    }
    return sb.String()
}
```
*Ref: 100_Go_Mistakes.md — "#39 Under-optimized string concatenation."*

**Code (byte-vs-string, mistake #40):**
```go
// Bad: extra copies
return []byte(sanitize(string(b))), nil

// Good: keep working in []byte
func sanitize(b []byte) []byte { return bytes.TrimSpace(b) }
```
*Ref: 100_Go_Mistakes.md — "#40 Useless string conversions."*

---

### 5. Functions & Methods (Mistakes #42–#47)

**Principle:** Pick the receiver type for *semantics* (mutability + consistency), not for premature optimization. Treat defer args as captured at defer time.

**Do:**
- Use a pointer receiver when the method mutates the receiver, when the struct contains a `sync` type, or when consistency with other pointer-receiver methods is needed.
- Use a value receiver for maps / funcs / channels, small immutable structs (`time.Time`), basic types.
- Accept interfaces (`io.Reader`/`io.Writer`) instead of filenames so callers can pass `strings.NewReader` / `bytes.Buffer` for tests.
- Use a closure (or pointer) inside `defer` when you need the *current* value of a variable.

**Don't:**
- Mix value and pointer receivers on the same type casually.
- Embed `sync.Mutex` so its `Lock`/`Unlock` methods leak to external callers.
- Name every return for "documentation"; only name when it adds clarity (e.g., two same-typed returns).
- Return a typed nil pointer wrapped in an interface — that's a non-nil interface holding a nil pointer.
- Treat `defer f.Close()` as infallible; check writable closes for errors.

**Code (nil receiver in interface, mistake #45):**
```go
func (c Customer) Validate() error {
    var m *MultiError
    if c.Age < 0 { /* … */ m = &MultiError{} }
    if c.Name == "" { /* … */ }
    return m // non-nil interface wrapping a nil *MultiError when nothing failed
}
```
*Fix:* `if m != nil { return m }; return nil`.
*Ref: 100_Go_Mistakes.md — "#45 Returning a nil receiver."*

**Code (filenames as input, mistake #46):**
```go
func countEmptyLines(reader io.Reader) (int, error) {
    scanner := bufio.NewScanner(reader)
    for scanner.Scan() { /* … */ }
    return /* n */, nil
}

// Test:
countEmptyLines(strings.NewReader("foo\n\nbar\n")) // no temp file
```
*Ref: 100_Go_Mistakes.md — "#46 Using a filename as a function input."*

**Code (defer argument capture, mistake #47):**
```go
func f() error {
    var status string
    defer func() {                          // closure: reads current `status` at return
        notify(status); incrementCounter(status)
    }()
    // ...
    status = StatusErrorFoo
    return err
}
```
*Ref: 100_Go_Mistakes.md — "#47 Ignoring how defer arguments and receivers are evaluated."*

---

### 6. Error Management (Mistakes #48–#54)

**Principle:** Errors are values. Handle each error *exactly once* (log OR wrap+return, not both). Use sentinels for expected errors and types for unexpected ones.

**Do:**
- Return `error`; use `panic` only for programmer-error / impossible states.
- Wrap with `fmt.Errorf("op %s: %w", name, err)` to preserve the chain; use `%v` if you intentionally want to break the chain.
- Match values with `errors.Is(err, os.ErrNotExist)`; match types with `errors.As(err, &target)`.
- Always check the close error of writable resources via deferred `func(){ if err := f.Close(); err != nil { … } }`.
- Ignore explicitly with `_` if you mean to; never silently drop.

**Don't:**
- Use type assertions or `==` on raw errors when wrapping is in play — both will silently miss wrapped errors.
- Log *and* return the same error; that's two handlers.
- Drop errors with `_` "just this once" without a comment and named return.
- Rely on `defer f.Close()` alone for `os.File` writes or `sql.Rows`.

**Code (defer error, mistake #54):**
```go
defer func() {
    err := rows.Close()
    if err != nil {
        log.Printf("failed to close rows: %v", err)
    }
}()
```
*Ref: 100_Go_Mistakes.md — "#54 Not handling defer errors."*

**Code (multi-error reconcile, mistake #54 deeper):**
```go
defer func() {
    closeErr := rows.Close()
    if err != nil {              // preserve the original error
        if closeErr != nil {
            log.Printf("failed to close rows: %v", closeErr)
        }
        return
    }
    err = closeErr
}()
```
*Ref: 100_Go_Mistakes.md — "#54 Not handling defer errors."*

---

### 7. Concurrency Foundations (Mistakes #55–#60)

**Principle:** Concurrency = structure. Parallelism = execution. A race condition is about timing; a data race is about unsynchronized memory access. Mutexes synchronize parallel goroutines; channels coordinate concurrent ones.

**Do:**
- Distinguish CPU-bound (size ~`GOMAXPROCS`) from I/O-bound (size bounded by external system).
- Always run tests with `-race`; instrument only in dev/CI (5–10× memory, 2–20× CPU).
- Rely on the Go memory model: channel send ⇄ receive, channel close ⇄ receive, `goroutine go` ⇄ start are sync points.
- Pass `context.Context` through the call chain (deadline, cancellation, request-scoped values).
- Use `context.WithValue` keys as unexported types to avoid collision.
- Use `context.TODO()` when you have *no* good context yet, instead of `context.Background()`.

**Don't:**
- Assume `concurrency ⇒ faster`; benchmark before parallelizing small workloads.
- Use buffered channels "for performance" without measuring.
- Confuse *data races* (concurrent unsynchronized access with at least one write) with *race conditions* (nondeterministic behavior due to timing).
- Rely on goroutine exit happening-before any later event; only `go` itself is sync'd to start.
- Block on raw channel send/receive inside a function whose context could be canceled — use a `select` with `<-ctx.Done()`.

**Code (worker pool sizing, mistake #59):**
```go
ch := make(chan []byte, n)              // buffered to pool size to reduce contention
wg.Add(n)
for i := 0; i < n; i++ {
    go func() {
        defer wg.Done()
        for b := range ch {
            v := task(b)
            atomic.AddInt64(&count, int64(v))
        }
    }()
}
```
Use `n = runtime.GOMAXPROCS(0)` for CPU-bound pools; let I/O-bound pools follow the external service.
*Ref: 100_Go_Mistakes.md — "#59 Not understanding the concurrency impacts of a workload type."*

**Code (cancel-safe channel ops, mistake #60):**
```go
func f(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case ch1 <- struct{}{}:
    }
    select {
    case <-ctx.Done():
        return ctx.Err()
    case v := <-ch2:
        _ = v
    }
    return nil
}
```
*Ref: 100_Go_Mistakes.md — "#60 Misunderstanding Go contexts."*

---

### 8. Concurrency Practice (Mistakes #61–#74)

**Principle:** Every goroutine needs an exit plan; every channel-shared state needs ownership clarity; every `sync` type must not be copied.

**Do:**
- Detach a parent context's cancellation when spawning a long goroutine (custom `Context` wrapper or `context.Background()` + the values you want).
- Always pair `goroutine` with: `done` channel, `context.Done()`, or a `defer wg.Done()`.
- Use `chan struct{}` for notifications; close once to broadcast, never send values to a notification channel.
- Use a `nil` channel inside a `select` to dynamically disable a case (graceful shutdown).
- Use `sync.WaitGroup.Add(n)` *before* spawning goroutines; `defer wg.Done()` inside.
- Use `errgroup.WithContext(ctx)` when launching parallel tasks that can fail (cancels shared ctx on first error).
- Copy only by pointer: any struct embedding `sync.Mutex`/`WaitGroup`/etc. must be referenced by pointer.

**Don't:**
- Propagate a request context (which cancels when the HTTP response is written) into a goroutine that must outlive the response.
- Start `go func()` without a plan for when it stops.
- Take `&v` from a `for _, v := range …` and ship it to a goroutine before Go 1.22 — every goroutine sees the final `v`.
- Treat `select` as deterministic: when multiple cases are ready, Go picks pseudo-randomly.
- Loop `time.After(time.Hour)`; it allocates a fresh timer every iteration.
- Append to a shared slice from multiple goroutines (race); use per-goroutine buffers then merge.
- Read/write a map from multiple goroutines; use `sync.Map`, a mutex, or a channel of operations.
- Copy a struct containing `sync.Mutex`/`RWMutex`/`Cond`/`WaitGroup`/`Pool`/`Map`/`Once`.

**Code (loop variable capture, mistake #63):**
```go
for _, v := range values {
    go func() {            // closure: every goroutine sees the last `v`
        process(v)
    }()
}
```
*Fix (Go < 1.22):*
```go
for _, v := range values {
    go func(v int) { process(v) }(v)   // pass as parameter
}
```
*Ref: 100_Go_Mistakes.md — "#63 Not being careful with goroutines and loop variables."*

**Code (inappropriate context propagation, mistake #61):**
```go
func handler(w http.ResponseWriter, r *http.Request) {
    response, err := doSomeTask(r.Context(), r)
    if err != nil { /* … */ }
    go func() {                                         // r.Context() cancels when response is written
        _ = publish(r.Context(), response)             // BAD: publishes may never happen
    }()
    writeResponse(response)
}
```
*Fix:* wrap with `detach{ctx: r.Context()}` that returns `nil` from `Done()`/`Err()` while still propagating values.
*Ref: 100_Go_Mistakes.md — "#61 Propagating an inappropriate context."*

**Code (goroutine without exit plan, mistake #62):**
```go
func main() {
    w := newWatcher()
    defer w.close()      // blocks main until watcher releases its resources
    // …
}
func newWatcher() watcher { w := watcher{}; go w.watch(); return w }
func (w watcher) close() { /* close resources */ }
```
*Ref: 100_Go_Mistakes.md — "#62 Starting a goroutine without knowing when to stop it."*

**Code (select is non-deterministic, mistake #64):**
```go
for {
    select {
    case v := <-messageCh:
        fmt.Println(v)
    case <-disconnectCh:
        for {                                // drain remaining messages
            select {
            case v := <-messageCh:
                fmt.Println(v)
            default:
                fmt.Println("disconnection, return")
                return
            }
        }
    }
}
```
*Ref: 100_Go_Mistakes.md — "#64 Expecting deterministic behavior using select and channels."*

**Code (nil channels for shutdown, mistake #66):**
```go
func merge(ch1, ch2 <-chan int) <-chan int {
    ch := make(chan int, 1)
    go func() {
        defer close(ch)
        for ch1 != nil || ch2 != nil {       // close+nil a finished channel
            select {
            case v, ok := <-ch1:
                if !ok { ch1 = nil; continue }
                ch <- v
            case v, ok := <-ch2:
                if !ok { ch2 = nil; continue }
                ch <- v
            }
        }
    }()
    return ch
}
```
*Ref: 100_Go_Mistakes.md — "#66 Not using nil channels."*

**Code (sync.WaitGroup discipline, mistake #71):**
```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)               // BEFORE the go statement
    go func(item T) {
        defer wg.Done()      // inside the goroutine
        process(item)
    }(item)
}
wg.Wait()
```
*Ref: 100_Go_Mistakes.md — "#71 Misusing sync.WaitGroup."*

**Code (errgroup, mistake #73):**
```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)
for i, circle := range circles {
    i, circle := i, circle        // capture for Go < 1.22
    g.Go(func() error {
        res, err := foo(ctx, circle)
        if err != nil { return err }
        results[i] = res
        return nil
    })
}
if err := g.Wait(); err != nil { return nil, err }
```
*Ref: 100_Go_Mistakes.md — "#73 Not using errgroup."*

**Code (don't copy sync types, mistake #74):**
```go
type Counter struct {
    mu sync.Mutex           // VALUE field ⇒ Increment with value receiver copies the mutex!
    counters map[string]int
}
func (c *Counter) Increment(name string) { c.mu.Lock(); defer c.mu.Unlock(); c.counters[name]++ }
```
If you must keep a value receiver, store the mutex by pointer: `mu *sync.Mutex`.
*Ref: 100_Go_Mistakes.md — "#74 Copying a sync type."*

---

### 9. Standard Library — time / JSON / SQL / HTTP (Mistakes #75–#81)

**Principle:** The stdlib hides assumptions that bite in production: `time.Duration` is nanoseconds, `sql.Open` is lazy, `http.DefaultClient` has no timeouts, `json.Unmarshal` into `map[string]any` makes numbers `float64`.

**Do:**
- Always pass `time.Duration` via the API: `time.Millisecond`, `5 * time.Second`. Never raw integers.
- In long-lived loops/handlers use `time.NewTimer` + `Reset(d)` + `defer timer.Stop()` instead of `time.After`.
- Treat `time.Time` comparisons with `Equal()`, not `==`, when JSON marshaling is involved (monotonic vs wall clock).
- Call `db.Ping()` (or `PingContext`) after `sql.Open` if you must verify reachability eagerly.
- Configure `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxIdleTime`, `SetConnMaxLifetime` for prod pools.
- Always `defer rows.Close()` and check `rows.Err()` after iteration.
- Close HTTP response bodies; `io.Copy(io.Discard, resp.Body)` to enable keep-alive when you don't read it.
- Build an `http.Client` with explicit `Timeout`, `DialContext`, `TLSHandshakeTimeout`, `ResponseHeaderTimeout`; build an `http.Server` with `ReadHeaderTimeout`, `ReadTimeout`, `IdleTimeout`, and wrap handlers in `http.TimeoutHandler(...)`.
- Use prepared statements for repeated queries.
- Handle nullable SQL via `*T` or `sql.NullString`/`NullInt64`/etc.
- `return` after `http.Error(...)` and any other response write.

**Don't:**
- Pass `time.Sleep(1000)` thinking that's one second; it's one microsecond.
- Use `time.After` inside a hot loop — each call allocates a timer that lives until it fires.
- Embed `time.Time` into a struct that you `json.Marshal`; the embedded `MarshalJSON` shadows sibling fields.
- Loop `for rows.Next() { /* scan */ }` without checking `rows.Err()` afterwards.
- Use `http.Get` / `http.Post` (which use `http.DefaultClient`) in production code.
- Forget to handle the error from `defer rows.Close()` / `defer f.Close()` for writable resources.

**Code (time.After leak, mistake #76):**
```go
// Bad — each iteration leaks ~200 B of timer state
for {
    select {
    case event := <-ch:
        handle(event)
    case <-time.After(time.Hour):
        log.Println("warning: no messages")
    }
}
```
*Fix:*
```go
timer := time.NewTimer(time.Hour)
defer timer.Stop()
for {
    timer.Reset(time.Hour)
    select {
    case event := <-ch:
        handle(event)
    case <-timer.C:
        log.Println("warning: no messages")
    }
}
```
*Ref: 100_Go_Mistakes.md — "#76 time.After and memory leaks."*

**Code (HTTP client timeouts, mistake #81):**
```go
client := &http.Client{
    Timeout: 5 * time.Second,
    Transport: &http.Transport{
        DialContext: (&net.Dialer{Timeout: time.Second}).DialContext,
        TLSHandshakeTimeout:   time.Second,
        ResponseHeaderTimeout: time.Second,
    },
}
```
*Ref: 100_Go_Mistakes.md — "#81 Using the default HTTP client and server."*

**Code (HTTP server timeouts, mistake #81):**
```go
s := &http.Server{
    Addr:              ":8080",
    ReadHeaderTimeout: 500 * time.Millisecond,
    ReadTimeout:       500 * time.Millisecond,
    IdleTimeout:       time.Second,
    Handler:           http.TimeoutHandler(handler, time.Second, "timeout"),
}
```
*Ref: 100_Go_Mistakes.md — "#81 Using the default HTTP client and server."*

**Code (embedded time.Time → JSON shadowing, mistake #77):**
```go
// BAD — MarshalJSON promoted from time.Time eclipses the whole struct
type Event struct {
    ID int
    time.Time
}
```
*Fix:* name the field, don't embed:
```go
type Event struct {
    ID   int
    Time time.Time
}
```
*Ref: 100_Go_Mistakes.md — "#77 Common JSON-handling mistakes."*

**Code (return after http.Error, mistake #80):**
```go
if err := foo(req); err != nil {
    http.Error(w, "foo", http.StatusInternalServerError)
    return                       // mandatory
}
```
*Ref: 100_Go_Mistakes.md — "#80 Forgetting the return statement after replying to an HTTP request."*

---

### 10. Testing (Mistakes #82–#90)

**Principle:** Tests must be deterministic, fast, isolated, and target behaviors (not internals). Benchmarks must avoid compiler/observer effects and report allocations.

**Do:**
- Categorize tests: build tags (`//go:build integration`), `t.Skip` on env var (`INTEGRATION!=true`), `testing.Short()` for slow tests.
- `go test -race ./...` in CI.
- Run with `-shuffle=on` to flush out hidden ordering dependencies; reproduce failures with the printed seed.
- Use the table-driven pattern + `t.Run(name, ...)`; for parallel subtests, shadow `tt := tt`:
  ```go
  for name, tt := range tests {
      tt := tt
      t.Run(name, func(t *testing.T) {
          t.Parallel()
          // use tt ...
      })
  }
  ```
- Test through interfaces and `httptest.NewRecorder` / `httptest.NewServer` (fake server) to avoid opening real sockets.
- Use `iotest` to inject `io.Reader` errors.
- Inject time dependency: pass a `now func() time.Time` instead of `time.Now`. Eventually `replace Time` via an overridable package var.
- Synchronize instead of `time.Sleep`; if you must retry, bound it (`assert.Eventually`).
- For benchmarks: call `b.ResetTimer()` after setup; assign the result of the function under test to a *local* var, then assign that to a *package-level* var (defeats dead-code elimination); recreate inputs each iteration to avoid CPU-cache pollution:
  ```go
  func BenchmarkX(b *testing.B) {
      var r int
      for i := 0; i < b.N; i++ {
          b.StopTimer(); data := makeInput(); b.StartTimer()
          r = work(data)
      }
      globalSink = r
  }
  ```
- Use `-benchtime=Nx` or `-count=10` + `benchstat` for statistical comparison.
- Place tests in `package foo_test` (black-box) to enforce behavior-only testing.
- Use `b.ReportAllocs()` in benchmarks to surface heap escape cost.
- `t.Cleanup(...)` for per-test teardown; `TestMain(m *testing.M)` for per-package fixtures.

**Don't:**
- Write tests that silently depend on each other or on a specific execution order.
- Use `time.Sleep` to "wait for things to settle" — flaky.
- Use `package foo` tests if you want to guarantee you're only calling the public API.
- Compare with `reflect.DeepEqual` for byte slices — use `bytes.Equal`.
- Let the compiler delete the work in your benchmark (`popcnt(uint64(i))` with unused result).
- Reuse the same large input across benchmark iterations and conclude about CPU-bound speed — caches will lie to you.

**Code (avoiding sleep in tests, mistake #86):**
```go
func TestLongRunning(t *testing.T) { if testing.Short() { t.Skip("skipping long-running test") } /* … */ }
```
*Ref: 100_Go_Mistakes.md — "#86 Sleeping in unit tests."*

**Code (httptest client/server, mistake #87):**
```go
// Fake server
ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "hello")
}))
defer ts.Close()
resp, err := http.Get(ts.URL)
// Handler test
rec := httptest.NewRecorder()
handler(rec, httptest.NewRequest("GET", "/x", nil))
```
*Ref: 100_Go_Mistakes.md — "#87 Not using testing utility packages."*

**Code (defeat dead-code elimination, mistake #88):**
```go
var globalSink uint64
func BenchmarkPopcnt(b *testing.B) {
    var v uint64
    for i := 0; i < b.N; i++ {
        v = popcnt(uint64(i))
    }
    globalSink = v
}
```
*Ref: 100_Go_Mistakes.md — "#88 Writing inaccurate benchmarks."*

---

### 11. Optimizations & Runtime (Mistakes #91–#100)

**Principle:** "Mechanical sympathy" — your code shares the machine with cache lines, ILP, the GC, and CFS. Profile before optimizing; measure the right thing.

**Do:**
- Lay out struct fields in *descending size order* to minimize padding.
  ```go
  // BAD: 24 B
  type Foo struct { a bool; b int64; c int32 }
  // GOOD: 16 B
  type Foo struct { b int64; c int32; a bool }
  ```
- For CPU-bound iteration over one field, prefer "struct of slices" over "slice of structs" (better spatial locality).
- For tight loops, favor *unit stride* and constant strides; avoid non-unit strides (linked lists, pointer chases).
- Pad per-goroutine hot counters to a cache line to avoid false sharing:
  ```go
  type Result struct {
      SumA int64
      _    [56]byte   // pad to 64 B
      SumB int64
  }
  ```
- Restructure hot loops to expose ILP (introduce a temporary variable to break data hazards on `s[0]`):
  ```go
  for i := 0; i < n; i++ {
      v := s[0]
      s[0] = v + 1
      if v%2 != 0 { s[1]++ }     // OLD read-modify on s[0] hidden
  }
  ```
- Know the rules of escape analysis: "sharing up escapes, sharing down stays on stack." Verify with `go build -gcflags="-m=2"`.
- For hot short-lived objects, consider `sync.Pool` with a `New: func() any { … }`.
- Enable `net/http/pprof` in production (safe); profile with `go test -bench=. -cpuprofile out` and inspect via `go tool pprof -http=:8080 out`.
- Generate execution traces: `go test -trace=trace.out` then `go tool trace trace.out`.
- Tune `GOGC` (default 100%) against prod load; consider pre-faulting a virtual arena for known spikes.
- Use `go.uber.org/automaxprocs` so `GOMAXPROCS` matches the CFS quota in containers.
- Use `pgrep`-style memory leak hunting via `GOMEMLIMIT` (Go 1.19+) ≈ 90% of the container memory limit; Alpine images need `musl` DNS workarounds.

**Don't:**
- Parallelize micro-workloads without benchmarking (goroutine spin-up overhead can eat the win — use a threshold).
- Store "sharing up" data through interfaces / channels / pointers-to-loop-variables unless necessary.
- `defer` in the hottest path of a function — it can inhibit inlining.
- Conclude from one micro-benchmark that `atomic.StoreInt32` is faster than `atomic.StoreInt64` — re-run in reversed order and use `benchstat`.
- Trust CPU cache timing on one machine to predict performance on production hardware.
- Forget to `defer timer.Stop()` for `time.Timer` so resources don't leak while idle.

**Code (escape verification, mistake #95):**
```sh
$ go build -gcflags="-m=2" ./...
./main.go:12:2: z escapes to heap:
```
*Ref: 100_Go_Mistakes.md — "#95 Not understanding stack vs. heap."*

**Code (sync.Pool, mistake #96):**
```go
var pool = sync.Pool{New: func() any { return make([]byte, 0, 1024) }}

func write(w io.Writer, req func([]byte)) error {
    buf := pool.Get().([]byte)
    buf = buf[:0]
    defer pool.Put(buf)
    req(buf)
    _, err := w.Write(buf)
    return err
}
```
*Ref: 100_Go_Mistakes.md — "#96 Not knowing how to reduce allocations."*

**Code (fast-path inlining, mistake #97):**
```go
func (m *Mutex) Lock() {
    if atomic.CompareAndSwapInt32(&m.state, 0, mutexLocked) {
        if race.Enabled { race.Acquire(unsafe.Pointer(m)) }
        return                              // fast path: inlinable
    }
    m.lockSlow()                           // slow path extracted
}
```
*Ref: 100_Go_Mistakes.md — "#97 Not relying on inlining."*

**Code (GOMEMLIMIT + automaxprocs, mistake #100):**
```go
import _ "go.uber.org/automaxprocs"
// Set GOMEMLIMIT via env or debug.SetMemoryLimit in main:
//   GOMEMLIMIT=450MiB  GOGC=100 ./myapp
// If running on Alpine: replace netgo default resolver with pure-Go DNS lookup.
```
*Ref: 100_Go_Mistakes.md — "#100 Not understanding the impacts of running Go in Docker and Kubernetes."*

---

## Anti-Patterns & Common Mistakes

| # | Anti-pattern | Why it's bad | Fix |
|---|---|---|---|
| 1 | `x, err := f()` inside an `if` shadowing an outer `x` | Outer variable never updated | rename, or use `=` (no `:=`) |
| 2 | "Else on the inside" pyramid | Hard to read, worse refactor | early-return guard clauses |
| 3 | Hidden work in `init()` | No error reporting, side effects on import | `MustX` factory or `main()` init |
| 4 | `GetName()`/`SetName()` ceremony | Un-Go-like, no encapsulation gain | exported field, name method after value |
| 5 | `interface{}` for one consumer | Unneeded abstraction | concrete type until you need polymorphism |
| 6 | Producer defines the interface | API lock-in, opposite direction | consumer-side interfaces |
| 7 | `NewX() X` (interface) return | Hides implementation, complicates mocking | return concrete `*x` |
| 8 | `func Process(data any)` | Strips type safety, no compile-time checking | specific type or generic `[T any]` |
| 9 | Generics for one-type constraints | Boilerplate without benefit | concrete type |
| 10 | Embedded `sync.Mutex` | Leaks `Lock`/`Unlock` to callers | name the field: `mu sync.Mutex` |
| 11 | Config struct of `*T` for "missing" values | Awkward API | functional options |
| 12 | `src/util` / `pkg/shared` packages | Junk drawer | `stringset`, `httpx`, domain name |
| 13 | Package name `redis` + variable `redis` | Ambiguous qualifier | rename or import alias |
| 14 | Undoc'd exported symbol | Future-hostile | `// Foo does …` |
| 17 | `010` thinking it's ten | Octal literal | `0o10` to be explicit |
| 18 | Bare `i++` near `MaxInt` | Silent wrap | check against `math.MaxInt`; use `math/big` |
| 19 | `f == g` for floats | Approximation error | compare `Abs(f-g) < epsilon` |
| 20 | `len(slice)` vs capacity confusion | Hard-to-trace mutations | memorize: `len ≤ cap`, append may reallocate |
| 21 | `make([]T, 0)` then append in a loop | O(n) allocations | preallocate `make([]T, 0, n)` |
| 22 | `[]T{}` returned as "empty" default | Allocates when nil wouldn't | return `var s []T` (nil) when applicable |
| 23 | `if s != nil` to test emptiness | Misses non-nil empty slices | use `len(s) == 0` |
| 24 | `dst := append([]int(nil), src...)` without intent | Pointer-API confusion | stick with `copy` for clarity |
| 25 | `append(s[:n], x)` mutating caller | Hidden write through shared backing array | `s[:n:n]` (full slice) or copy |
| 26 | Long-lived small slice over big parent | Backing array leak | `strings.Clone` / manual copy |
| 27 | `m := make(map[K]V)` without size hint | Resize churn | `make(map[K]V, hint)` |
| 28 | Map that grows then mostly empties | Never shrinks | periodic recreation or pointer values + nil |
| 29 | `[]int == []int` | Compile error / `reflect.DeepEqual` accepts variadic | use `bytes.Equal` or typed compare |
| 30 | `for _, x := range xs { x.foo = … }` | Mutates copy | `for i := range xs { xs[i].foo = … }` |
| 31 | `for range s { s = append(s, …) }` | Looks infinite; isn't (range evaluates expr once) | know the rule; express with classic `for` if needed |
| 32 | `&loopVar` captured into a goroutine | All goroutines see last element | local copy or pointer-to-slice-element |
| 33 | Assuming map order | Go randomizes deliberately | design data structures independent of order |
| 34 | `break` inside `select`/`switch` in `for` | Breaks inner only | labeled `break loop` |
| 35 | `defer f.Close()` in a `for` | Accumulates until function returns | extract per-iteration work into a function |
| 36 | `len(s)` for character count | Bytes, not runes | `utf8.RuneCountInString(s)` or `[]rune(s)` |
| 37 | Index iteration for multibyte strings | Splits runes in half | `for i, r := range s` |
| 38 | `TrimRight(s, "ox")` to strip "ox" | Trims *set* characters | `TrimSuffix(s, "ox")` |
| 39 | String concatenation with `+=` | O(n²) allocs | `strings.Builder` + `Grow` |
| 40 | `[]byte ⇄ string` round trips in I/O | Copies | stay in `[]byte` with `bytes.*` |
| 41 | Long-lived substring of huge string | Backing array stays alive | `strings.Clone` / copy |
| 42 | Mixed value/pointer receivers | API confusion | be consistent; `time.Time` is a documented exception |
| 43 | Never using named returns | Misses clarity for same-typed multiple returns | name only what aids readability |
| 44 | Returning named `err` zero-value by mistake | Always-`nil` error path compiles | shadow with `if err := ...; err != nil { return …, err }` |
| 45 | Returning `var p *Foo; return p` as `error` | Non-nil interface wrapping nil pointer | `if p != nil { return p }; return nil` |
| 46 | `func Read(path string)` | Untestable, narrow | `func Read(r io.Reader)` |
| 47 | `defer notify(status)` with mutated `status` | Captures old value | pass pointer or use a closure |
| 48 | `panic` for expected failures | Unrecoverable for callers | return `error` |
| 49 | `fmt.Errorf("… : %s", err)` | Breaks the error chain | `%w` to wrap; `%v` to transform |
| 50 | `err.(*MyErr)` against wrapped error | Misses the chain | `errors.As(err, &target)` |
| 51 | `err == os.ErrNotExist` after wrap | Misses the chain | `errors.Is(err, os.ErrNotExist)` |
| 52 | Log *and* return the same error | Two handlers | one — usually wrap + return |
| 53 | `_ = f()` for "I'll handle later" | Forgotten bugs | explicit `_ = f()` with a reason or handle inline |
| 54 | `defer f.Close()` for writable `os.File` | Silent data loss | check error in deferred closure |
| 55 | Treating concurrency as parallelism | Wrong mental model | learn Rob Pike's "concurrency is structure" |
| 56 | Goroutines for tiny workloads | Spin-up overhead eats gains | parallelize only above a benchmarked threshold |
| 57 | Channels for parallel sync | Channels ≠ synchronization for shared state | mutex for parallel goroutines; channels for coordination |
| 58 | "Go is fast because of goroutines" | Race conditions, nondeterminism | study memory model; use `-race` |
| 59 | One pool size for any workload | CPU-bound oversubscribes, I/O-bound undersubscribes | `n = GOMAXPROCS(0)` for CPU; external quota for I/O |
| 60 | `ctx` as background when unsure | Loses cancellation/deadline | use `context.TODO()` instead |
| 61 | `go publish(r.Context(), …)` | Request ctx dies when response is written | detach ctx or pass `context.Background()` |
| 62 | `go w.watch()` with no exit plan | Goroutine + resource leak | `close()` + `defer`; pass a cancellable ctx |
| 63 | Closure capturing loop var in goroutines | All see last value | pass as parameter (`go func(v T){…}(v)`) |
| 64 | `select` written for "priority" | Random when both ready | nested select with `default` (drain pattern) |
| 65 | `chan bool` for notifications | Misleading; should be signal-only | `chan struct{}` |
| 66 | Closing channels to send values | Can't close a `chan` and "unclose" it | nil-out channels inside `select` after close |
| 67 | Buffered channel for "throughput" | Hides backpressure | size 0/1 unless measured, then document the rationale |
| 68 | `String()` calling methods that lock | Deadlock with formatting lock | pre-compute or document the hazard |
| 69 | Shared-slice `append` from goroutines | Race | per-goroutine buffers + merge, or mutex |
| 70 | Plain maps/slices across goroutines | Race | `sync.Map`, mutex, channel of operations |
| 71 | `wg.Add(1)` inside goroutine | Race against `wg.Wait` | `Add` *before* `go`, `Done` `defer`'d inside |
| 72 | `for { time.Sleep }` polling | Wasteful | `sync.Cond` `Broadcast`/`Signal` |
| 73 | Manual `WaitGroup + error slice + mutex` | Reinventing `errgroup` | `errgroup.WithContext` + `g.Go` |
| 74 | Value receiver / value arg / `range` copy of `sync` type | Breaks mutex invariant | pointer everywhere; `go vet` |
| 75 | `time.Sleep(1000)` | µs, not s | `time.Second`, `100 * time.Millisecond` |
| 76 | `time.After` in a loop | ~200 B leak per call per loop iteration | `time.NewTimer` + `Reset` + `defer Stop` |
| 77 | Embedded `time.Time` (or any `Marshaler`) | Embedded interface eclipses the whole struct | name the field; or implement explicit `MarshalJSON` |
| 78 | `sql.Open` as proof-of-config | Lazy connect | follow with `Ping`/`PingContext` |
| 79 | `defer rows.Close()` ignoring error | Connection pool leak | check error in deferred closure |
| 80 | `http.Error` without `return` | Continues past error | always `return` after the write |
| 81 | `http.Get`, `http.DefaultClient`, `&http.Server{}` in prod | No timeouts ⇒ hangs, Slowloris | explicit `Timeout`, `ReadHeaderTimeout`, etc. |
| 82 | No test categorization (unit/integration/slow) | CI is slow or hides bugs | build tags / env vars / `testing.Short()` |
| 83 | `go test` without `-race` | Race slips to prod | `-race` in CI |
| 84 | Always-same execution order | Hidden dependencies survive | `-shuffle=on`; log+reproduce the seed |
| 85 | One-test-per-function `TestX_Empty` etc. | Boilerplate | table-driven with `t.Run` |
| 86 | `time.Sleep` to wait async ops | Flaky | synchronize via channels; or `assert.Eventually` |
| 87 | Skipping `httptest` | Opens real sockets | `httptest.NewServer` / `NewRecorder` |
| 88 | Benchmarks dropping work to dead-code elimination | Lies about cost | assign result to local then package-level sink |
| 89 | Benchmark reusing huge input | CPU cache hides real cost | rebuild input each iteration with `b.StopTimer/StartTimer` |
| 90 | Chasing 100% coverage | Neglects assertions / mutation resistance | focus on contract coverage; use `-coverpkg=./...` |
| 91 | Ignoring CPU caches | Slow hot loops | unit/constant stride; struct-of-slices for one field |
| 92 | Adjacent fields touched by different goroutines | Cache-line bouncing | pad to 64 B |
| 93 | Data hazards in tight loops | Pipeliner stalls | introduce a temp to allow ILP |
| 94 | Random struct field order | Padding, larger cache footprint | size-descending order |
| 95 | Returned pointer "to avoid a copy" | Heap escape, GC pressure | return values by default; share only when semantics demand |
| 96 | Allocating fresh buffers on hot path | GC pressure | `sync.Pool` + `Grow` |
| 97 | One huge function with slow + fast paths | No inlining | extract slow path into separate function (fast-path inlining) |
| 98 | No profiling/tracing | Optimizing blind | `pprof` + `go tool trace` on benchmarks and prod |
| 99 | Default `GOGC` for everything | GC pauses / heap bloat | tune `GOGC` per workload; consider `GOMEMLIMIT` |
| 100 | Ignoring CFS in containers | CPU throttling, latency blow-up | `go.uber.org/automaxprocs`, align `GOMEMLIMIT` to cgroup limit |

---

## Decision Heuristics / Checklists

**Channels vs mutexes (mistake #57):**
- Parallel goroutines modifying shared state → **`sync.Mutex` / `sync.RWMutex`** (or `sync.Map`).
- Concurrent (piped) goroutines transferring ownership or signalling → **channel**.

**Channel type (mistakes #65–#67):**
- No payload, only signal → `chan struct{}`.
- Sender/receiver coupling required → unbuffered (size 0).
- Need decoupling AND you've measured throughput benefits → buffered, size 1 by default, larger only with profiling.

**Receiver type (mistake #42):**
- Mutates receiver? → pointer.
- Has `sync`/`os`/pointer-bearing fields? → pointer.
- Map/func/channel? → value (compile enforces).
- Tiny immutable value (e.g., `time.Time`, `Point{x,y}`)? → value.
- Otherwise → prefer value, default to pointer if in doubt.

**When to use generics (mistake #9):**
- YES: factor element type across heterogeneous containers (slice/map/channel); reuse constraints across impls.
- NO: when you'd constrain to *one* type; when an interface covers your needs; before you have two callers.

**Slice operation checklist:**
- Know `len` vs `cap`. `append` may grow.
- Use `make([]T, n, cap)` when size is known.
- Use full-slice expression `s[:n:n]` before handing a sub-slice to a function that may `append`.
- Use `strings.Clone` (or manual copy) to detach long-lived substrings.
- Test emptiness with `len(s) == 0`.

**Error-handling checklist (mistakes #48–#54):**
- `panic` only for programmer errors.
- Wrap with `%w` if you want `errors.Is/As` later; `%v` to break the chain.
- Sentinels for *expected* errors (`os.ErrNotExist`); custom types for *unexpected* ones.
- Never log AND return (handle once).
- Always check close errors for writable resources (`defer f.Close()` with log/propagation).

**Test checklist (mistakes #82–#90):**
- Tests in `package foo_test` (public API) or `package foo` (interactions with internals).
- Categorize via build tag / env / short mode.
- `go test -race ./...` always.
- `-shuffle=on` routinely; re-run with the seed to reproduce.
- For async ops: synchronization, never `Sleep`.
- For time: inject `now func() time.Time`.
- Mock HTTP with `httptest.NewServer`; capture with `httptest.NewRecorder`.
- Benchmarks: local+package-level sinks; `b.ResetTimer`; new inputs per iter; `benchstat` over `-count=10`.

**Performance checklist (mistakes #91–#100):**
- Profile first (`pprof`+trace), don't guess.
- Field-order structs (descending size).
- Avoid false sharing (pad hot per-goroutine counters).
- Use struct-of-slices for one-field iteration.
- Reduce heap pressure: preallocate, `sync.Pool`, `Grow`, API choices (sharing down).
- Watch Go memory model for sync guarantees.
- Set `GOMEMLIMIT` ≈ 90% of container memory; install `automaxprocs`.

---

## Key Takeaways

1. **Right-abstraction discipline.** Define interfaces on the consumer side, return concrete types, name packages by *what they provide*, prefer functional options over config-structs of pointers.
2. **Slices and maps are pointers.** Allocate once with `len`/`cap` hints, never leak capacity via cross-cutting subslices, never compare them with `==`, beware maps never shrink.
3. **Strings are bytes plus rune semantics.** Iterate runes not bytes, use `strings.Builder` for loops, `strings.Clone` for long-lived substrings, stay in `[]byte` for I/O.
4. **Errors are values handled once.** Wrap with `%w` for context; use `errors.Is`/`errors.As`; name returns carefully; check `defer` close errors for writable resources.
5. **Concurrency = structure.** Don't sprinkle goroutines; pick the concurrency model first (CPU-bound vs I/O-bound), prefer a worker pool sized to `GOMAXPROCS` for CPU work, and *always* run `-race` in CI.
6. **Goroutines need an exit plan.** Pair `go …` with `defer wg.Done()`, `<-ctx.Done()`, or a `done` channel; pass loop variables explicitly.
7. **Channels vs mutexes.** Channels coordinate concurrent goroutines; mutexes synchronize parallel goroutines sharing state.
8. **Notify with `chan struct{}`.** Use `select` with nil-channels to disable cases; remember `select` chooses randomly when multiple cases are ready; use one unbuffered channel (or a struct sum-type) for deterministic ordering from a single producer.
9. **Standard library has hidden prod hazards.** `time.Duration` is nanoseconds; `time.After` leaks in loops; `sql.Open` is lazy; `http.DefaultClient`/default `Server` have no timeouts — configure them explicitly.
10. **Tests are documentation.** Table-driven + subtests + `-race` + `-shuffle` + `httptest` + benchmark hygiene (sink + reset timer + `benchstat`). Cover the public API via `package foo_test`.
11. **Profile before optimizing.** Cache-line layout, false sharing, ILP, escape analysis, GC tuning, `GOMEMLIMIT`, `automaxprocs` — measure, don't guess. Use `go tool pprof` and `go tool trace` as core tools.
12. **Mechanical sympathy wins.** Unit strides, struct-of-slices, descending-size struct fields, fast-path inlining via extracted slow path, padding to cache lines — these are *measured* improvements in tight loops.

---

## Cross-References
- Topic index: [[../INDEX.md]]
