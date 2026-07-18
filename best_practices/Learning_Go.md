# Learning Go — Best Practices
**Author:** Jon Bodner (2nd Edition, O'Reilly 2024)
**Topic tags:** `#general` `#concurrency` `#testing` `#api`
**Language focus:** Go-first
**Sources:** `markdown_output/Learning_Go_An_Idiomatic_Approach_to_Real-World_Go_Programming_2nd_Edition_-_Jon_Bodner/Learning_Go_An_Idiomatic_Approach_to_Real-World_Go_Programming_2nd_Edition_-_Jon_Bodner.md` · `summaries/Learning_Go_An_Idiomatic_Approach_to_Real-World_Go_Programming_2nd_Edition_-_Jon_Bodner.md`

## TL;DR
Idiomatic Go is "boring on purpose": clear, maintainable, predictable. The book's overriding principle is *write code that makes your intentions clear* — comprehensibility beats conciseness. Every feature exists to serve that: zero values eliminate init bugs, explicit type conversions kill a whole class of promotion bugs, returned errors force every call site to confront failure, and channels/select/cancellation make data flow between goroutines obvious. Accept interfaces, return structs; keep concurrency out of your APIs; test at boundaries (table tests + fuzz + race detector + httptest).

---

## Best Practices by Topic

### Types, Variables, and Declarations

**Principle:** Zero values, explicit conversions, and untyped constants exist so the compiler can do as much work for you as possible.

**Do:**
- Use `int` for all integer variables unless you are working with a specific binary format or network protocol that mandates a fixed-size/signed type.
- Use `float64` for floating-point work unless compatibility demands `float32`. Never use floats for money — use a decimal library (`shopspring/decimal`).
- Always capitalize rune literals `'J'` and string literals `"text"` correctly; Go treats them as different types (`int32` vs `string`).
- Use `_` (underscore) to ignore return values explicitly — `result, _, err := divAndRemainder(5, 2)`.
- Use `:=` inside functions for the common case. Use `var x int` when the zero value is intentional; use the long `var x T = v` form when the literal's default type is wrong.
- Read every declared local variable — it is a compile-time error not to. Avoid package-level mutable variables; they complicate data flow analysis.
- Use raw string literals (backticks) for multi-line strings or strings containing backslashes/quotes.
- Use `errors.New("only even numbers are processed")` for static messages, `fmt.Errorf("%d isn't even", i)` when runtime data is needed. Error strings should NOT be capitalized, end with punctuation, or end with a newline.
- Use `byte` (alias for `uint8`) instead of `uint8`, and `rune` (alias for `int32`) instead of `int32` whenever the value represents text.

**Don't:**
- Don't use `==` to compare floating-point values. Define an epsilon and check `math.Abs(a-b) < epsilon`.
- Don't use leading-zero octal literals (`0755`) — they are confusing. Use `0o755`.
- Don't use the look-alike Unicode code points as variable names; the compiler treats them as distinct and the code is unmaintainable.
- Don't try to convert an int to a bool (or vice versa). Use a comparison operator: `x == 0`, `s == ""`.
- Don't declare package-level mutable variables — the Go compiler can't enforce immutability, so you must enforce it socially.
- Don't reassign exported sentinel errors — they are treated as read-only by convention.

**Code:**
```go
// Always copy the literal value to a variable before taking its address
func makePointer[T any](t T) *T { return &t }

type Person struct {
    FirstName  string
    MiddleName *string // can't take address of literal
    LastName   string
}
p := Person{
    FirstName:  "Pat",
    MiddleName: makePointer("Perry"), // works
    LastName:   "Peterson",
}

// Float comparison — never use ==
const epsilon = 1e-9
if math.Abs(a-b) < epsilon { /* equal */ }
```
*Ref: Learning_Go.md — "Predeclared Types and Declarations", "var Versus :=", "Pointers Indicate Mutable Parameters"*

---

### Composite Types (Arrays, Slices, Maps, Strings, Structs)

**Principle:** Slices and maps are reference types implemented on top of pointers — copying the slice header does NOT copy the backing storage. Use the three-part slice expression to prevent accidental overwrites.

**Do:**
- Prefer slices over arrays; arrays exist primarily as backing storage for slices or for fixed binary layouts (e.g. cryptographic checksums).
- Use `make([]T, 0, n)` with the expected capacity when you know the size upfront — it avoids repeated reallocations and copies.
- Use `len()` and `cap()` to inspect slices, and the three-part slice expression `s[low:high:max]` to limit a subslice's capacity so `append` cannot overwrite the parent's backing array.
- Use `copy(dst, src)` to create independent slices.
- Compare slices with `slices.Equal` / `slices.EqualFunc` (Go 1.21+) — never with `==` (compile error).
- Use the comma-ok idiom to disambiguate "missing key" from "zero value" on map reads: `v, ok := m[key]`.
- Use `map[string]struct{}{}` as a memory-zero set only when set size is large; otherwise `map[T]bool` is clearer.
- Use struct literal field-name syntax (`person{Name: "Bob", Age: 30}`) for any non-trivial struct — it's forward-compatible when fields are added.
- Use anonymous structs for one-off data shapes (table tests, JSON unmarshal targets).
- Iterate strings with `for i, r := range s` to get runes (code points), not bytes.
- Use `clear(m)` (Go 1.21+) to empty a map or zero a slice's contents (length preserved on slices).
- Use `delete(m, key)` — it's a no-op on missing keys or nil maps.

**Don't:**
- Don't declare a slice with `var x = []int{}` when `var x []int` (nil slice) works — they are not equivalent (`len` and JSON output differ).
- Don't append to a subslice (`y := x[:2]; y = append(y, ...)`) without the three-part slice expression — it can clobber the parent's data.
- Don't use `reflect.DeepEqual` in new code for slice/map comparison; use `slices.Equal` / `maps.Equal`.
- Don't use a slice or map as a map key — they are not comparable.
- Don't index into a string by byte position when characters may be multibyte UTF-8 — use `[]rune(s)` or `for-range`.
- Don't try to convert an `int` directly to `string` — `string(65)` yields `"A"` (rune), not `"65"`.
- Don't write a `func` field or channel field in a struct if you need it comparable — those make the struct uncomparable.

**Code:**
```go
// Three-part slice expression prevents aliasing
x := make([]string, 0, 5)
x = append(x, "a", "b", "c", "d")
y := x[:2:2]   // y has length 2, capacity 2 — append on y cannot touch x
z := x[2:4:4]  // z has length 2, capacity 2

// Map presence vs zero value
v, ok := m["key"]
if !ok { /* key absent — don't treat zero value as "present" */ }

// Anonymous struct for one-shot JSON
var raw struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
json.Unmarshal(bytes, &raw)
```
*Ref: Learning_Go.md — "Slices", "Maps", "Using Maps as Sets", "Anonymous Structs", "Comparing and Converting Structs"*

---

### Blocks, Shadowing, and Control Flow

**Principle:** Go's block scoping is small but strict. The `:=` operator reuses outer variables only if at least one variable on the left is new — this is the #1 source of accidental shadow bugs.

**Do:**
- Use the `if n := rand.Intn(10); n == 0 { ... }` init-statement form to scope a value to the if/else blocks.
- Use a `switch` (including blank `switch {}` for boolean chains) instead of long `if/else` chains.
- Use `goto` only for cleanup jumps to a top-of-function label; it cannot skip declarations or jump into inner blocks.
- Use `for i := 0; i < n; i++ {}` (complete), `for condition {}` (while), `for {}` (infinite), or `for-range` — those are Go's only loop forms.
- Rely on Go 1.22+ semantics: the `for-range` loop variable is per-iteration (no more classic `v := v` shadow dance).

**Don't:**
- Don't put parens around `if` conditions: `if (x > 0)` is not idiomatic.
- Don't rely on switch fall-through — Go cases don't fall through by default. Use `fallthrough` explicitly and rarely.
- Don't shadow predeclared identifiers (`true`, `false`, `nil`, `len`, `int`, `make`, ...). It compiles but corrupts the universe block.
- Don't shadow loop variables in pre-Go-1.22 closures — pass values explicitly or upgrade to Go 1.22.

**Code:**
```go
// Pre-Go-1.22 closure capture workaround
for _, v := range a {
    v := v                       // shadow to give each goroutine its own copy
    go func() { ch <- v * 2 }()
}

// Switch for related comparisons
switch {
case x < 0:
    return errors.New("negative")
case x == 0:
    return nil
default:
    return process(x)
}
```
*Ref: Learning_Go.md — "Blocks, Shadows, and Control Structures", "for, Four Ways"*

---

### Functions, defer, Closures, and Methods

**Principle:** Functions are values; closures capture surrounding variables; `defer` runs LIFO after `return`.

**Do:**
- Return `(value, error)` as the last return is the strongest Go convention. On success, return `nil` for the error.
- Use named return values only when the names clarify the code or when `defer` must modify a return value (the canonical error-wrapping pattern).
- Use `defer` for ALL resource cleanup (Close, Unlock, Remove). Defer runs even on panic.
- Use the resource-allocation + cleanup-closure pattern: `func getFile(name string) (*os.File, func(), error)`.
- Defer arguments are evaluated at the `defer` statement, not at the deferred function's execution. Capture deliberately.
- Use closures to keep helpers local to one function — reduces package-level noise.
- Use methods when logic depends on state stored on a struct; use functions when logic depends only on its inputs.
- Use `defer` for `sync.Mutex.Unlock` and `*sql.Tx` rollback — name the receiver so the deferred closure can see the error.

**Don't:**
- Don't use bare `return` (blank returns) — they obscure data flow. Always `return value, err`.
- Don't put `defer` inside a tight loop for per-iteration cleanup; it accumulates until the function returns. Call the cleanup inline.
- Don't create getters/setters for Go structs unless they are needed to satisfy an interface — direct field access is the idiom.
- Don't reassign package-level function variables — package-level state should be effectively immutable.

**Code:**
```go
// Error wrapping with defer and named return value
func DoSomeThings(val1 int, val2 string) (_ string, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("in DoSomeThings: %w", err)
        }
    }()
    val3, err := doThing1(val1)
    if err != nil { return "", err }
    val4, err := doThing2(val2)
    if err != nil { return "", err }
    return doThing3(val3, val4)
}
```
*Ref: Learning_Go.md — "Functions", "defer", "Methods Are Functions Too", "Functions Versus Methods"*

---

### Types, Methods, Interfaces, Embedding

**Principle:** Go has no inheritance. Composition via embedding and implicit interfaces replace class hierarchies. The interface lives with the consumer, not the provider.

**Do:**
- Define a new named type when you want a concept to be self-documenting: `type Percentage int`, `type Score int`. The new type is NOT the underlying type — explicit conversion is required in both directions.
- Choose pointer vs value receivers consistently within a type. If ANY method needs a pointer receiver, use pointer receivers for ALL methods (so the method set is uniform).
- Use pointer receivers when the method mutates the receiver, when the type contains sync primitives, or when the struct is large (≥10 MB).
- Use value receivers for small, immutable, naturally-copyable types.
- Define your own error types with multiple fields (`Status`, `Message`) when callers need to react programmatically (not just string-compare).
- Use `errors.Is(err, target)` to check for a sentinel, `errors.As(err, &typedErr)` to extract a typed error from the chain. Never string-compare error messages.
- Declare interfaces in the package that CONSUMES the behavior — small (1–3 methods), named with `-er` suffix, package-private when only your package needs them.
- Combine small interfaces via embedding: `type ReadCloser interface { Reader; Closer }`.
- Embed interfaces in stub structs to satisfy them with only the methods you implement for a test.
- Implement `http.Handler` via `http.HandlerFunc` so any function with the right signature is automatically a handler.
- Return concrete types from factory functions. Return interfaces only for the rare case where multiple implementations are genuinely possible (e.g., `database/sql/driver`).

**Don't:**
- Don't assign a value instance to an interface variable that requires a pointer-receiver method — the method is not in the value's method set and the compiler will reject the assignment.
- Don't use embedding expecting polymorphism. `Outer` is NOT substitutable for `Inner` even if `Inner` is embedded. Use an interface field for that.
- Don't write getter/setter methods just because Java does. Go wants direct field access.
- Don't return `error` as a concrete type — always declare the return as `error` even when you return a custom type, to avoid the nil-interface trap.
- Don't compare two interface values containing uncomparable types — it panics at runtime (`reflect.Value.Comparable` first if you must).
- Don't use `any` / `interface{}` to dodge type design. It's a placeholder, not an abstraction. Save it for genuinely dynamic data (config blobs, decoded JSON).
- Don't use type assertions to peek at "optional" interfaces in wrapped/decorated chains — the wrapper hides them. Define a wider interface and use it explicitly.
- Don't make the interface unexported unless you also make at least one of its methods unexported — otherwise anyone can embed the interface in a struct and accidentally satisfy it.

**Code:**
```go
// Pointer vs value receiver consistency
type Counter struct {
    total       int
    lastUpdated time.Time
}
func (c *Counter) Increment() { c.total++; c.lastUpdated = time.Now() }
func (c Counter)  String() string { /* value receiver is fine because all in 1 type */ }

// Custom error type with status + wrap
type StatusErr struct {
    Status  Status
    Message string
    Err     error
}
func (se StatusErr) Error() string  { return se.Message }
func (se StatusErr) Unwrap() error  { return se.Err }

// Accept interface, return struct
func NewController(l Logger, logic Logic) Controller { return Controller{l: l, logic: logic} }

// Interface lives with consumer
type Logic interface {
    SayHello(userID string) (string, error)
}
```
*Ref: Learning_Go.md — "Types, Methods, and Interfaces", "Pointer Receivers and Value Receivers", "Code Your Methods for nil Instances", "Accept Interfaces, Return Structs", "Implicit Interfaces Make Dependency Injection Easier"*

---

### Generics

**Principle:** Use generics to write one implementation that the compiler type-checks at instantiation. Don't reach for them when an interface or a simple function suffices.

**Do:**
- Use type parameters to factor out algorithms (Map, Filter, Reduce, custom Tree) without losing compile-time type safety.
- Use `any` when no constraint is needed (the unconstrained case).
- Use `comparable` when you need `==` / `!=` in the body. Beware: `comparable` matches interfaces too — and comparing interface values containing uncomparable types panics.
- Define custom constraints as interfaces, including type elements (unions): `type Integer interface { ~int | ~int8 | ~int16 | ... }`. Use `~T` to allow user-defined types whose underlying type is `T`.
- Combine operators with constraints: `type Ordered interface { ~int | ~float64 | ~string }`.
- Combine type elements and methods: `type PrintableInt interface { ~int; String() string }`.
- Let the compiler infer type arguments whenever possible; supply them explicitly only when the inference fails (e.g. when a type parameter is used only as a return value).
- Prefer Go 1.21+ standard library generics (`slices`, `maps`, `cmp`) over hand-rolling.
- For zero values in generic code: `var zero T; return zero` — `nil` is NOT a valid zero for a value type like `int`.

**Don't:**
- Don't convert an interface-parameter function to a generic-parameter function hoping for speedups. As of Go 1.21, generics actually share generated functions for pointer types and add runtime lookups; measured costs can be ~30% slower for trivial functions.
- Don't expect specialization, variadic type parameters, currying, or parameterized methods — Go generics intentionally don't have them.
- Don't write a constraint like `interface { int; String() string }` (without `~`) — it has zero valid instantiations and the compiler will block any use.
- Don't over-reach: use a generic function only when you genuinely need the same algorithm for multiple concrete types.

**Code:**
```go
// Map, Filter, Reduce — generic
func Map[T1, T2 any](s []T1, f func(T1) T2) []T2 {
    out := make([]T2, len(s))
    for i, v := range s { out[i] = f(v) }
    return out
}

// Operator-bearing constraint (with ~ for user types)
type Ordered interface {
    ~int | ~int8 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint32 | ~uint64 | ~uintptr |
    ~float32 | ~float64 | ~string
}

// Custom Tree without type parameters on the algorithm — pass the comparator
type OrderableFunc[T any] func(t1, t2 T) int
type Tree[T any] struct { f OrderableFunc[T]; root *Node[T] }
```
*Ref: Learning_Go.md — "Generics", "Idiomatic Go and Generics", "Adding Generics to the Standard Library"*

---

### Error Handling

**Principle:** Errors are values, not control flow. Wrap to add context; unwrap with `errors.Is`/`errors.As` to inspect. `panic` is for programmer errors only.

**Do:**
- Always return `error` as the last return value. Always check it: `if err != nil { return err }` or handle.
- Set non-error return values to their zero values when returning a non-nil error.
- Use `errors.New` for static messages, `fmt.Errorf` for formatted messages.
- Wrap with `%w` to preserve the error chain: `return fmt.Errorf("in fileChecker: %w", err)`.
- Use `%v` (not `%w`) when you want the message but explicitly do NOT want callers to be able to inspect the wrapped error.
- Define sentinel errors as `ErrFoo` (uppercase prefix) at the package level for states where processing cannot continue. Compare with `errors.Is`, not `==`.
- Define custom error types with extra fields (status codes, retry info) for cases callers must react to programmatically.
- Use `errors.Join(err1, err2, ...)` (Go 1.20+) to merge multiple validation errors into one.
- Implement `Unwrap() error` on your custom error so `errors.Is`/`As` traverse it.
- Implement `Is(target error) bool` on your custom error for non-equality matches (e.g. pattern matching by subset of fields).
- Centralize "wrap every returned error with the same prefix" via `defer` + named return:
  ```go
  func DoWork() (_ string, err error) {
      defer func() {
          if err != nil { err = fmt.Errorf("in DoWork: %w", err) }
      }()
      ...
  }
  ```
- Define JSON-time error returns as `error`, never as your concrete type — to avoid the nil-interface trap (`var genErr StatusErr; return genErr` is a NON-nil interface even when StatusErr is zero-valued).

**Don't:**
- Don't define sentinel errors casually — once exported, they're part of your public API forever and can never be removed.
- Don't use string comparison on error messages — text changes break callers.
- Don't use a type assertion or type switch to peek at custom error fields. Use `errors.As(err, &typedErr)` instead.
- Don't panic for ordinary error conditions (bad input, network failure). Reserve panic for genuinely unrecoverable situations (programmer error, out of memory).
- Don't let a panic escape a library boundary — wrap it in `recover` and return an `error`.
- Don't call `errors.Unwrap` directly — `errors.Is` and `errors.As` already traverse the chain correctly.
- Don't return a typed nil (e.g. `*MyErr` nil) as `error` — it compares != nil because the interface's type field is set.

**Code:**
```go
// Sentinel + Is
var ErrInvalidLogin = errors.New("invalid login")
if errors.Is(err, ErrInvalidLogin) { /* ... */ }

// Typed error + As
var se *StatusErr
if errors.As(err, &se) {
    switch se.Status {
    case InvalidLogin: /* ... */
    case NotFound:     /* ... */
    }
}

// Multiple errors joined
return errors.Join(errs...)

// Pattern-matching Is
func (re ResourceErr) Is(target error) bool {
    other, ok := target.(ResourceErr)
    if !ok { return false }
    return (other.Resource == "" || other.Resource == re.Resource) &&
           (other.Code == 0 || other.Code == re.Code)
}
```
*Ref: Learning_Go.md — "Errors", "How to Handle Errors: The Basics", "Sentinel Errors", "Errors Are Values", "Wrapping Errors", "Wrapping Multiple Errors", "Is and As", "panic and recover"*

---

### Concurrency

**Principle:** Concurrency is a tool to clarify data flow between stages — not free parallelism. "Share memory by communicating; do not communicate by sharing memory." Always design for cancellation.

**When to use concurrency (and when NOT to):**
- Use it when you must wait on independent I/O or independent data streams, or when you have multiple sequential steps with natural parallelism.
- Do NOT use it for trivial in-memory computations — the goroutine overhead overwhelms the gain.
- Concurrency ≠ parallelism. Parallel speedup is bounded by Amdahl's law.

**Goroutines:**
- Launch with `go f(args)` — return values are dropped. Wrap business logic in a closure that handles the concurrency bookkeeping so the business logic itself stays concurrency-unaware.
- Keep concurrency out of your APIs. Channels and mutexes must NOT appear in exported types, function signatures, or struct fields (with rare exceptions for concurrency-helper libraries).
- Pass the loop variable explicitly to the goroutine to capture by value:
  ```go
  for _, v := range a {
      go func(val int) { ch <- val * 2 }(v)   // go 1.22 also fixes this
  }
  ```
- ALWAYS ensure goroutines can exit. A goroutine that never exits leaks its stack and pins heap memory.
- Treat goroutine leaks like memory leaks — design for termination up front.

**Channels:**
- Channels are reference types (zero value is nil). Prefer UNBUFFERED channels by default — they synchronize sender and receiver at the handoff.
- Use BUFFERED channels in exactly these three situations:
  1. You know exactly how many goroutines you launched and want each to exit without blocking (`make(chan T, N)`).
  2. You want to limit concurrency (token-bucket backpressure).
  3. You want to queue a bounded amount of work and shed load when full.
- Use directional channel types (`<-chan T` for read-only, `chan<- T` for write-only) to enforce correct usage at compile time. Assign them in struct fields or parameters; never expose a bare `chan T`.
- The writer closes the channel. Closing is required ONLY when a reader is using `for-range` (or comma-ok) to detect completion. Closing twice panics; closing from the wrong goroutine panics.
- Reading from a closed channel returns the zero value — always use `v, ok := <-ch` to distinguish "closed" from "zero".
- `len(ch)` and `cap(ch)` work on buffered channels.
- NIL channels block forever — use this deliberately to disable a `select` case (set the variable to `nil`).

**select:**
- `select` randomly picks among cases that are ready → no starvation. Use it to multiplex concurrent sources.
- For-Select loops are the idiomatic cancellable processing loop:
  ```go
  for {
      select {
      case <-ctx.Done(): return
      case v, ok := <-ch: if !ok { return }; process(v)
      }
  }
  ```
- `select` with a `default` is a NONBLOCKING read/write. Do NOT put `default` inside an infinite `for-select` unless you want a busy-spin CPU loop.

**Cancellation:**
- Pass `context.Context` as the FIRST parameter to any function that may block or call out.
- Always call the `cancel` function returned from `context.WithCancel` / `WithTimeout` / `WithDeadline` (typically via `defer cancel()`).
- Propagate `ctx` through every I/O call: `http.NewRequestWithContext`, `db.QueryContext`, etc.
- Use `context.WithCancelCause(ctx)` (Go 1.20+) when you need to attach an error to the cancellation; retrieve via `context.Cause(ctx)`.
- Wrap timeouts via `context.WithTimeout(parent, 50*time.Millisecond)`. Child deadlines are bounded by parent deadlines.
- Use `context.Background()` at process entry points, `context.TODO()` only as a temporary placeholder.

**Patterns:**
- Backpressure (limit concurrent execution):
  ```go
  type PressureGauge struct{ ch chan struct{} }
  func (pg *PressureGauge) Process(f func()) error {
      select {
      case pg.ch <- struct{}{}:
          defer func() { <-pg.ch }()
          f()
          return nil
      default:
          return errors.New("no more capacity")
      }
  }
  ```
- Disable a select case when its channel is closed by setting the variable to `nil`.
- Timeout pattern:
  ```go
  func timeLimit[T any](worker func() T, limit time.Duration) (T, error) {
      out := make(chan T, 1)              // size 1 so the worker never blocks on write
      ctx, cancel := context.WithTimeout(context.Background(), limit)
      defer cancel()
      go func() { out <- worker() }()
      select {
      case r := <-out:    return r, nil
      case <-ctx.Done():  var z T; return z, errors.New("timed out")
      }
  }
  ```
- `sync.WaitGroup` to wait for N goroutines — never pass it by value (it would be copied), capture it in a closure. Use it ONLY when you need cleanup after workers exit (e.g. closing the shared output channel exactly once):
  ```go
  var wg sync.WaitGroup
  wg.Add(num)
  for i := 0; i < num; i++ {
      go func() { defer wg.Done(); for v := range in { out <- process(v) } }()
  }
  go func() { wg.Wait(); close(out) }()    // single closer, after all writers done
  ```
- `sync.Once` (or `sync.OnceValue[T]` / `sync.OnceValues[T]` in Go 1.21+) for lazy one-shot initialization. Never copy a `sync.Once`.
- `errgroup.Group` (`golang.org/x/sync/errgroup`) cancels siblings when one fails.

**Mutexes vs channels (Cox-Buday decision tree):**
- Coordinating goroutines or tracking a value as it's transformed → use **channels**.
- Sharing access to a field in a struct → use **mutexes** (`sync.Mutex` / `sync.RWMutex`).
- Performance-critical AND no clear ownership flow → measure, then maybe a mutex.

**Mutex rules:**
- Pair every `Lock`/`RLock` with a `defer Unlock`/`RUnlock` immediately after.
- Go mutexes are NOT reentrant — recursive lock acquisition deadlocks.
- Never copy a mutex; pass via pointer.
- Never access a shared variable from multiple goroutines without locking.
- For shared maps, prefer `map[K]V` protected by `sync.RWMutex` over `sync.Map`. `sync.Map` is only for keys written once and read many times, with disjoint goroutine access.
- Prefer `sync.RWMutex` when reads dominate writes.

**Atomics:**
- Almost never needed. `sync/atomic` is for low-level experts after profiling. Channels and mutexes are correct enough for 99% of code.

**Race detector:**
- Run tests with `go test -race` in CI. It is roughly 10× slower — run it always on tests, never in production binaries.
- Do NOT try to fix races with sleeps. Add the lock.

**Code (canonical orchestration):**
```go
func GatherAndProcess(ctx context.Context, data Input) (COut, error) {
    ctx, cancel := context.WithTimeout(ctx, 50*time.Millisecond)
    defer cancel()
    ab := newABProcessor()
    ab.start(ctx, data)
    inputC, err := ab.wait(ctx)
    if err != nil { return COut{}, err }
    c := newCProcessor()
    c.start(ctx, inputC)
    return c.wait(ctx)
}
```
*Ref: Learning_Go.md — "Concurrency in Go" — full chapter (Goroutines, Channels, select, Concurrency Practices and Patterns, Goroutines for Loops, Always Clean Up, Use the Context, Buffered vs Unbuffered, Backpressure, Turn Off a case, Time Out Code, Use WaitGroups, Run Code Exactly Once, Put Your Concurrent Tools Together, When to Use Mutexes Instead of Channels, Atomics — full chapter*

---

### The Standard Library (I/O, Time, JSON, HTTP, slog)

**io and io.Reader/io.Writer:**
- `io.Reader.Read(p []byte) (n int, err error)` — pass a reusable buffer; don't `make([]byte, n)` inside Read loops.
- Always check `io.EOF` to detect end of stream; check `io.ErrUnexpectedEOF` for truncation.
- Implement small interfaces: `io.Closer` (`Close() error`), `io.Seeker`, and composites like `io.ReadCloser`, `io.ReadWriteSeeker`.
- Use `io.Copy(dst, src)` for streaming copies.
- Use `io.MultiReader`, `io.MultiWriter`, `io.LimitReader`, `io.NopCloser` for composable wrappers.
- For one-method bridging (e.g. to make a Reader into a ReadCloser), use the embedded-interface pattern:
  ```go
  type nopCloser struct{ io.Reader }
  func (nopCloser) Close() error { return nil }
  ```

**time:**
- Use `time.Duration` constants (`time.Hour`, `time.Millisecond`) for readability and type-safety. `d := 2*time.Hour + 30*time.Minute`.
- Format with the reference time `Mon Jan 2 15:04:05 MST 2006` (the magic date). Use `time.RFC3339`, `time.RFC822Z`, etc. constants when available.
- Compare `time.Time` with `.Equal()` — NOT `==` — to handle time zones correctly.
- Trust monotonic time automatically mixed into `time.Now()` results for elapsed-time calculations; that's why `Sub` is reliable across DST/NTP.
- For recurring timers: `time.NewTicker` (not `time.Tick`, which cannot be stopped and leaks).
- `time.AfterFunc(d, f)` for one-shot delayed calls.

**encoding/json:**
- Always declare struct tags: `Field int `json:"id"``. Don't rely on case-insensitive field-name fallback.
- Use `,omitempty` on optional fields. Zero structs are NOT considered empty (zero slices/maps ARE).
- Use `-` for fields to skip both directions: `json:"-"`.
- Use pointer fields (`*string`, `*int`) to distinguish "absent" from "zero" on unmarshal — `nil` means missing, non-nil with zero value means present-but-zero.
- Stream with `json.NewDecoder(r).Decode(&v)` for large or unknown-size data; call until `io.EOF`. Use `json.NewEncoder(w).Encode(v)` to stream out.
- Implement `json.Marshaler` (`MarshalJSON() ([]byte, error)`) and `json.Unmarshaler` (`UnmarshalJSON([]byte) error`) for custom encoding. To avoid infinite recursion, define a `type Dup T` alias and use it inside the methods.
- Pass `map[string]any` to `json.Marshal`/`Unmarshal` only for the exploratory phase — replace with a concrete type once the schema is known.
- `encoding/gob` and `net/rpc` are language-specific. Prefer gRPC or a language-agnostic protocol.

**net/http (Client):**
- Never use `http.DefaultClient` or the package-level `http.Get`/`Post`/`PostForm` helpers in production — they have no timeout. Construct your own:
  ```go
  client := &http.Client{ Timeout: 30 * time.Second }
  ```
- Build requests with `http.NewRequestWithContext(ctx, method, url, body)` so the context can cancel in-flight requests.
- Always `defer resp.Body.Close()` and check `resp.StatusCode`. Stream the body with `json.NewDecoder(resp.Body).Decode(&v)` rather than loading it all into memory.

**net/http (Server):**
- Build around `http.Server` with explicit timeouts:
  ```go
  s := http.Server{
      Addr:         ":8080",
      ReadTimeout:  30 * time.Second,
      WriteTimeout: 90 * time.Second,
      IdleTimeout:  120 * time.Second,
      Handler:      mux,
  }
  ```
- Avoid the package-level `http.Handle`, `http.HandleFunc`, `http.ListenAndServe`, `http.ListenAndServeTLS` outside trivial programs — they use the shared `http.DefaultServeMux` (third-party libs can register there too) and you cannot configure server timeouts.
- Use `http.NewServeMux()` (Go 1.22+ supports HTTP verbs and `{name}` wildcards: `mux.HandleFunc("GET /hello/{name}", ...)`). Read path values via `r.PathValue("name")`.
- Nest `*http.ServeMux` instances for hierarchical routing; use `http.StripPrefix` to remove already-matched path segments.
- Middleware = `func(http.Handler) http.Handler` (or `func(http.Handler) http.Handler` that returns a closure). Apply by composition:
  ```go
  wrappedMux := terribleSecurity(RequestTimer(mux))
  s.Handler = wrappedMux
  ```
- For optional response methods (Flush, Hijack, SetReadDeadline, etc.) that can't be added to the interface without breaking compatibility, wrap with `http.NewResponseController(rw)` and check the returned error against `http.ErrNotSupported` via `errors.Is`.
- Function-to-interface adapter pattern (used by stdlib for handlers):
  ```go
  type HandlerFunc func(http.ResponseWriter, *http.Request)
  func (f HandlerFunc) ServeHTTP(w http.ResponseWriter, r *http.Request) { f(w, r) }
  ```

**log/slog (Go 1.21+):**
- Use `slog.Info/Warn/Error/Debug` for structured logging. `slog.Debug` is suppressed at the default level.
- Pass key/value pairs as alternating args: `slog.Info("user login", "id", userID, "login_count", loginCount)`.
- For high-throughput paths, use `LogAttrs(ctx, level, msg, slog.String(...), slog.Int(...), slog.Time(...), slog.Any(...))` to avoid the allocation from variadic boxing.
- Create your own logger when you need JSON output, a minimum level, or a custom destination:
  ```go
  handler := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: slog.LevelDebug})
  logger := slog.New(handler)
  ```
- Include `context.Context` as the first arg of `LogAttrs` so loggers can pull request-scoped fields (request IDs, trace IDs).
- Bridge legacy `log.Logger` to slog via `slog.NewLogLogger(handler, level)`.
*Ref: Learning_Go.md — "The Standard Library", "io and Friends", "time", "encoding/json", "net/http", "Structured Logging"*

---

### Modules, Packages, Project Layout

**Principle:** The module path is a globally unique identifier — make it match the import URL.

**Do:**
- Initialize modules with `go mod init <modulepath>` (e.g. `github.com/org/project`). Never edit `go.mod` by hand; use `go get` and `go mod tidy`.
- Set the `go` directive in `go.mod` to the minimum supported Go version. With Go 1.22+, set it to 1.22 or later to opt into per-iteration loop variables.
- Use `go 1.21+` default `GOTOOLCHAIN=auto` to let `go.mod`'s `toolchain` directive download the needed Go version automatically.
- Use the `internal/` directory name to restrict a package's visibility to the parent directory tree (and its siblings).
- Name packages short, lowercase, single-word, no underscores. Don't repeat the package name in identifiers (`names.Extract`, not `names.ExtractNames`).
- Name a function with the package's noun (`context.Context`, `sort.Sort`).
- Document every exported identifier with a `//` comment that starts with the identifier name. Use a `doc.go` file for long package-level docs.
- Use `pkg.go.dev` for documentation; preview locally with `pkgsite`.
- Resolve name collisions on import with an alias: `import crand "crypto/rand"`. Avoid the dot import (`.`) — it pollutes the namespace.
- Run `go vet` and `go fmt ./...` (or `goimports`) before every commit. Add `staticcheck` / `revive` / `golangci-lint` / `govulncheck` to CI.
- Avoid `init()` — reserve it for effectively immutable package-level state (e.g. endpoint-detection from `unsafe`).
- Use `go generate ./...` for code generation; document `//go:generate` directives at the source.
- Use `//go:embed` to bake static files (templates, configs, HTML) into the binary.
- Cross-compile with `GOOS=linux GOARCH=arm64 go build`. Use `//go:build linux` constraints for OS-specific files.
- Use `go.work` for multi-module local development; remove temporary `replace` directives.
- Use semver: incompatible majors live at `/v2`, `/v3`, etc. Use `retract` in `go.mod` to yank a bad release.

**Don't:**
- Don't use relative import paths — they don't work with modules.
- Don't put business logic in `init()` — testing and ordering become nightmares.
- Don't create `util`, `helpers`, `common`, `misc` packages — name packages by what they ARE, not what they CONTAIN.
- Don't expose channels, mutexes, or other concurrency primitives in exported types.

**Code:**
```go
// Package documentation starts with the package name
// Package convert provides utilities for converting money between currencies.
package convert

// Document every exported identifier; start with its name
// Money represents an amount and the currency it's denominated in.
type Money struct {
    Value    decimal.Decimal
    Currency string
}
```
*Ref: Learning_Go.md — "Modules, Packages, and Imports", "Documenting Your Code with Go Doc Comments", "Using the internal Package", "Avoiding Circular Dependencies"*

---

### Go Tooling

**Do:**
- Use `go run` for quick experiments and small programs.
- Install third-party tools with `go install tool@version` (e.g. `go install honnef.co/go/tools/cmd/staticcheck@latest`).
- Use `goimports` (not just `gofmt`) — it groups and removes unused imports automatically on save.
- Run `staticcheck` for hundreds of additional checks beyond `go vet`.
- Run `govulncheck ./...` in CI — it scans your dependency graph against the Go vulnerability database.
- Use `//go:embed` to include static assets at compile time.
- Use `go generate ./...` for any code generation; keep `//go:generate` directives near the source they affect.
- Cross-compile via `GOOS` / `GOARCH` env vars.
- Use `//go:build linux` (or the older `// +build linux`) constraints for OS-specific files.
- Read build info from a running binary via `debug.ReadBuildInfo()` — gives you VCS revision, build settings.
- Always include a Makefile (or justfile) so `make`, `make fmt`, `make vet`, `make build` are reproducible.
- The Go Compatibility Promise guarantees no breaking language or stdlib changes within Go 1.x. New behaviors (e.g. Go 1.22 loop scoping) are gated by the `go` directive in `go.mod`.

**Don't:**
- Don't add the `// +build` syntax in new code — use `//go:build` (it allows `&&`, `||`, `!`).
- Don't write tooling that depends on undocumented `go` command flags.
*Ref: Learning_Go.md — "Setting Up Your Go Environment", "Go Tooling"*

---

### Testing

**Principle:** Tests live next to the code they test. Use table tests for breadth, fuzz tests for unknown inputs, `httptest` for handlers, and `-race` for concurrency bugs. 100% coverage does NOT mean correct.

**Test layout & conventions:**
- Test files end in `_test.go` and live in the same package as the production code. Use `package foo` (white-box) for unit tests, `package foo_test` (black-box) to test the public API only — both can coexist in the same directory.
- Test functions: `func TestXxx(t *testing.T)`. Benchmark functions: `func BenchmarkXxx(b *testing.B)`. Fuzz functions: `func FuzzXxx(f *testing.F)`. Examples: `func ExampleXxx()`.
- Test names should describe what is being tested: `TestValidateUser`, not `TestUser`.
- Run all tests in a module: `go test ./...`. Add `-v` for verbose output.

**Reporting failures:**
- `t.Error` / `t.Errorf` — mark failed but CONTINUE the test.
- `t.Fatal` / `t.Fatalf` — mark failed and STOP the test.
- Use `Fatal` when further checks would always fail or panic. Use `Error` when reporting many independent field validations (so one run surfaces every problem).
- Never call `t.Fatal` from a goroutine other than the one running the test — use `t.Errorf` and signal via channel.

**Setup / teardown:**
- `TestMain(m *testing.M)` — at most ONE per package. Use for package-level setup (DB connection, env). Don't use it for things that could be `t.Cleanup`.
- `t.Cleanup(func())` — registers a cleanup callback. Multiple callbacks run LIFO. Use this for per-test cleanup in helpers.
- `t.TempDir()` — returns a fresh temp dir that is auto-deleted after the test. Prefer over manual `os.MkdirTemp` + `defer os.RemoveAll`.
- `t.Setenv(key, value)` — sets an env var for the test and auto-restores it on completion.

**Sample data:**
- Store test data in a subdirectory named `testdata/` and access via RELATIVE paths — `go test` changes the working directory to the package.
- `testdata/` is reserved by the Go tooling; it is excluded from build and never gets packaged.

**Comparing results — use `go-cmp`:**
- Prefer `cmp.Diff(expected, actual)` (from `github.com/google/go-cmp/cmp`) over hand-rolled deep equality or `reflect.DeepEqual`.
- Use `cmp.Comparer(func(x, y T) bool { ... })` to ignore non-deterministic fields (timestamps, generated IDs).
- `slices.Equal` / `maps.Equal` (Go 1.21+) beat `reflect.DeepEqual` for slices/maps.

**Table-driven tests:**
- Define a slice of anonymous structs with fields for `name`, input args, expected output, expected error. Loop with `t.Run(name, func(t *testing.T) { ... })`.
- Name every subtest so `-v` output and `go test -run` selectors work.
- For error comparisons: prefer `errors.Is`/`errors.As` over message string comparison. Message strings have no compatibility guarantee.

**Parallel tests:**
- `t.Parallel()` marks a test as eligible to run concurrently with other parallel tests in the package.
- Don't use `t.Parallel()` on tests that share mutable state.
- On Go 1.21 or earlier, capture the loop variable before invoking `t.Run`:
  ```go
  for _, d := range data {
      d := d
      t.Run(d.name, func(t *testing.T) {
          t.Parallel()
          ...
      })
  }
  ```
  Go 1.22+ makes this unnecessary.
- `go vet` flags loop-variable capture in test closures (`go test -vet=all`).

**Code coverage:**
- `go test -cover` — summary. `go test -coverprofile=c.out` + `go tool cover -html=c.out` — annotated HTML.
- 100% coverage does NOT mean bug-free. Cover branches AND invariants.
- Use coverage to find UNTESTED code, not to prove correctness.

**Fuzzing (Go 1.18+):**
- Write fuzz tests for any function that consumes untrusted input (parsers, decoders, validators).
- Seed corpus via `f.Add(seed...)`. The seed types are limited: ints, floats, bool, string, `[]byte`.
- Inside `f.Fuzz(func(t *testing.T, in T) { ... })`, write invariants (round-trip, parse-doesn't-panic) — you cannot predict the random output.
- Failures are written to `testdata/fuzz/FuzzName/<hash>` and re-run as regression tests.
- Run with `go test -fuzz=FuzzName` — only ONE fuzz test at a time. Resource intensive (multi-GB).
- Common catches: integer overflow in allocations, negative lengths, whitespace-only inputs, zero-divisors.

**Benchmarks:**
- `func BenchmarkXxx(b *testing.B)` with a loop `for i := 0; i < b.N; i++ { ... }`.
- Write benchmark results to a `var blackhole int` package-level sink so the compiler doesn't optimize the call away.
- Add `-benchmem` to see `B/op` and `allocs/op`.
- Sub-benchmarks with `b.Run(name, func(b *testing.B) { ... })` to compare variants.
- Profiling (`pprof`) is the next step when benchmark numbers reveal a problem.
- DON'T optimize without benchmarks. If the program is fast enough, stop.

**Stubs and fakes:**
- Extract dependencies into interfaces, then provide fake implementations for tests. This is the #1 reason to "accept interfaces, return structs".
- For large interfaces, embed the interface in the stub struct — you only have to implement the methods you actually call.
- For per-test customization, use a struct of function fields:
  ```go
  type EntitiesStub struct {
      GetUser    func(id string) (User, error)
      GetPets    func(userID string) ([]Pet, error)
      ...
  }
  ```
- Stubs return canned values for known inputs. Mocks validate call sequences — write mocks by hand or use `gomock` / `testify`.
- Reserve shared-state package-level fixtures for things that are truly immutable per package; otherwise inject.

**httptest:**
- Use `httptest.NewServer(http.Handler)` to spin up a real HTTP server on a random port for end-to-end tests. `defer server.Close()`.
- Use `httptest.NewRecorder()` to inspect handler output without a network.
- `server.Client()` returns a `*http.Client` pre-configured to talk to the test server (handles TLS, redirects, etc.).

**Integration tests:**
- Gate with build tags: `//go:build integration` at the top of `*_integration_test.go`. Run with `go test -tags integration ./...`.
- Alternative: check `os.Getenv("INTEGRATION")` and call `t.Skip("set INTEGRATION=1 to run")` — more discoverable.
- Run integration tests separately from unit tests in CI.

**Race detector:**
- ALWAYS run tests with `-race`. Add it to your CI matrix.
- ~10× slowdown but acceptable for tests; never use in production binaries.
- Inserts sleep calls to "fix" races — DON'T.

**Code (canonical test file):**
```go
func DoMath(num1, num2 int, op string) (int, error) { /* ... */ }

func TestDoMath(t *testing.T) {
    data := []struct {
        name     string
        num1, num2 int
        op       string
        expected int
        errMsg   string
    }{
        {"addition", 2, 2, "+", 4, ""},
        {"bad_division", 2, 0, "/", 0, `division by zero`},
    }
    for _, d := range data {
        d := d
        t.Run(d.name, func(t *testing.T) {
            result, err := DoMath(d.num1, d.num2, d.op)
            if result != d.expected {
                t.Errorf("got %d, want %d", result, d.expected)
            }
            var msg string
            if err != nil { msg = err.Error() }
            if msg != d.errMsg {
                t.Errorf("got err %q, want %q", msg, d.errMsg)
            }
        })
    }
}

func FuzzParseData(f *testing.F) {
    f.Add([]byte("3\nhello\ngoodbye\ngreetings\n"))
    f.Add([]byte("0\n"))
    f.Fuzz(func(t *testing.T, in []byte) {
        r := bytes.NewReader(in)
        out, err := ParseData(r)
        if err != nil { t.Skip("handled error") }
        roundTrip := ToData(out)
        rtr := bytes.NewReader(roundTrip)
        out2, err := ParseData(rtr)
        if diff := cmp.Diff(out, out2); diff != "" {
            t.Error(diff)
        }
    })
}
```
*Ref: Learning_Go.md — "Writing Tests" (full chapter: Test Basics, Reporting Failures, Setup/Teardown, Environment Variables, testdata, Caching, Public API, go-cmp, Table Tests, Concurrent Tests, Code Coverage, Fuzzing, Benchmarks, Stubs, httptest, Integration Tests, Data Race Detector)*

---

### Reflection, unsafe, cgo

**Principle:** These break Go's safety guarantees. Use them only at boundaries (serialization, OS interop, C libraries). Each has a real performance or ergonomics cost; prefer safe code unless you have measured.

**Reflection (`reflect`):**
- Reserve reflection for: encoding/decoding (JSON, XML, DB), templates, generic marshaling, writing tools.
- DON'T use it as a substitute for generics or interfaces — it's slower, more fragile (many operations panic on type mismatch), and more verbose.
- Benchmarks: a reflection-based `Filter` is 50–75× slower than a custom or generic version (same allocations differ by thousands).
- Use `reflect.TypeOf(v)` for type info, `reflect.ValueOf(v)` for value access. Use `reflect.Kind` to know which methods are safe.
- `Elem()` follows pointers, interface boxes, slice/map/channel wrappers to the contained type.
- To create a `reflect.Type` from scratch:
  ```go
  var stringType = reflect.TypeOf((*string)(nil)).Elem()
  var stringSliceType = reflect.TypeOf([]string(nil))
  ```
- Check `reflect.Value.IsValid()` BEFORE calling any other method on it; check `IsNil()` ONLY when Kind is one of Pointer/Slice/Map/Func/Interface.
- `reflect.New(T)` returns a pointer; `reflect.MakeSlice/MakeMap/MakeChan` parallel `make`.
- To detect nil inside an interface (the case where `== nil` lies): combine `IsValid()` and `IsNil()` on the relevant kinds.
- `reflect.MakeFunc` can build a function dynamically (e.g. for timing wrappers); but don't use it for hot-path code.
- You CANNOT add methods via reflection — so you cannot reflectively implement an interface.

**unsafe:**
- `unsafe.Pointer` is the bridge between arbitrary pointer types. `unsafe.Sizeof` and `unsafe.Offsetof` are compile-time constants (use them in `const` declarations).
- `unsafe.String`, `unsafe.StringData`, `unsafe.Slice`, `unsafe.SliceData` (Go 1.20+) provide safer alternatives for binary data conversion.
- Primary use cases: reading/writing network protocols without per-byte copies, interop with OS syscalls (the `syscall` package itself relies on `unsafe`).
- Struct field order matters for layout: place fields of the same size together to minimize padding. Reorder large types if you hold millions of them.
- NEVER use `unsafe` to bypass type safety unless you have profiled and identified the unsafe operation as a real bottleneck. Always pass `-gcflags=-d=checkptr` in test builds to catch misuse.
- Avoid `unsafe` to access unexported fields of another package — coupling to internals will break.

**cgo:**
- Each C call costs ~30–50 ns. Calling a C function from Go is roughly 29× slower than C-to-C. Use cgo ONLY for integration with C libraries, NOT for performance.
- Keep the cgo boundary NARROW. Wrap the C call in a small Go function so business code never sees Cgo types.
- You cannot pass Go strings, slices, or other pointer-containing types directly to C — they contain pointers the C side can't safely hold. Use `cgo.NewHandle` to wrap, pass the handle as `uintptr_t`, then `handle.Value()` on the way back and `handle.Delete()` when done.
- C functions cannot store Go pointers across calls (Go's GC may relocate).
- Cannot call variadic C functions (`printf`) directly via cgo, cannot pass function pointers, cannot pass unions cleanly.
- If a third-party Go wrapper exists for your C library, use it instead of writing your own cgo.

**Code:**
```go
// Detecting nil inside an interface with reflection
func hasNoValue(i any) bool {
    iv := reflect.ValueOf(i)
    if !iv.IsValid() { return true }
    switch iv.Kind() {
    case reflect.Pointer, reflect.Slice, reflect.Map, reflect.Func, reflect.Interface:
        return iv.IsNil()
    default:
        return false
    }
}

// Safer binary-data conversion (Go 1.20+)
data := *(*Data)(unsafe.Pointer(&b))
// Or via unsafe.Slice / unsafe.SliceData when the source is a slice.
```
*Ref: Learning_Go.md — "Here Be Dragons: Reflect, Unsafe, and Cgo"*

---

## Anti-Patterns & Common Mistakes

- **Shadowing variables with `:=` in a tight block**: `if err := do(); err != nil { ... }` re-declares `err`, hiding any outer `err`. When multiple returns are involved, accidentally shadowing one of them causes silent bugs. Prefer `var` or rename explicitly.
  → *Fix:* be explicit about what you're shadowing; `go vet` won't catch this — use a third-party linter.
- **Returning a typed nil as `error`**: `var e *MyErr; return e` returns a NON-nil interface because the type field is set.
  → *Fix:* always declare the local as `var err error` and assign the typed value to it, OR explicitly `return nil` in the no-error branch.
- **Slice subslice aliasing**: `y := x[:2]; y = append(y, "z")` overwrites `x[2]` because the subslice kept x's full capacity.
  → *Fix:* `y := x[:2:2]` to cap capacity at length; or `copy` if you need independence.
- **Method set mismatch**: a value instance only has the value-receiver methods in its method set. Assigning a `Counter` value to a `Incrementer` interface that requires pointer-receiver `Increment()` won't compile.
  → *Fix:* use `&Counter{}`, or change all receivers consistently.
- **Embedding as inheritance**: `Outer` containing `Inner` does NOT make `Outer` substitutable for `Inner`. There is no dynamic dispatch through embedded fields.
  → *Fix:* declare an interface and assign an `Inner` field of that interface type.
- **Goroutine leaks**: launching a goroutine that depends on a channel that no one will ever read from.
  → *Fix:* always provide an exit path via `context.Done()` or by closing the input channel.
- **Looping with `default` in `select`**: a `for { select { default: ... } }` burns CPU at 100% when no channel is ready.
  → *Fix:* omit `default` so the goroutine blocks; add a `<-ctx.Done()` case for cancellation.
- **Race "fixes" with `time.Sleep`**: makes races intermittent, never fixes them.
  → *Fix:* add proper synchronization; verify with `go test -race`.
- **Closing channels from the wrong goroutine**: closing from a reader panics on subsequent writes; closing twice panics.
  → *Fix:* exactly one writer goroutine closes the channel, and only when readers are using `for-range` to detect end.
- **`time.Tick` in non-trivial programs**: the underlying `time.Ticker` cannot be stopped, so it leaks goroutines.
  → *Fix:* use `time.NewTicker` and call `Stop()` when done.
- **String comparison for errors**: `err.Error() == "..."` breaks when messages change.
  → *Fix:* use sentinel errors + `errors.Is`, or typed errors + `errors.As`.
- **Returning interfaces from constructors**: prevents callers from using new methods/fields you add later.
  → *Fix:* return concrete types. Use interfaces at parameter boundaries, not return boundaries.
- **Big interfaces**: hard to stub, hard to evolve. "The bigger the interface, the weaker the abstraction."
  → *Fix:* define small, role-focused interfaces (`Reader`, `Writer`, `Closer`) and let consumers compose them.
- **Reaching for reflection instead of generics/interfaces**: 50–75× slower, panics on type mismatch, fragile under refactors.
  → *Fix:* generics for type-parameterized algorithms, interfaces for behavior contracts, reflection only at boundaries.
- **`init()` for business logic**: test ordering becomes opaque, side-effects surprise readers.
  → *Fix:* use explicit initialization in `main` (or a DI container) and pass dependencies down.
- **Reaching for `sync.Map` everywhere**: only wins in narrow conditions (write-once, read-many, disjoint keys).
  → *Fix:* default to `map[K]V` protected by `sync.RWMutex`.
- **Code that relies on the for-range loop variable across goroutines** (pre-Go 1.22):
  → *Fix:* pass the variable as a parameter or shadow it (`v := v`).
- **Comparing `time.Time` with `==`**: ignores time zone.
  → *Fix:* use `.Equal()`.

---

## Decision Heuristics / Checklists

### "Should I use a pointer or a value?"
- Type contains a `sync.Mutex` or other non-copyable primitive → **pointer**.
- Method needs to mutate the receiver → **pointer**.
- Struct is large (≥10 MB or so) and the cost of copying is measurable → **pointer**.
- Type is logically a reference (e.g. an `io.Reader`) → **pointer**.
- Otherwise → **value** (makes data flow obvious, reduces GC pressure).

### "Channel or mutex?"
- Sharing a field across goroutines AND no clear transformation pipeline → **mutex** (with `RWMutex` if reads dominate).
- Coordinating multiple goroutines or tracking a value through a pipeline → **channel**.
- Performance-critical with no clean ownership story → measure first, then maybe a mutex.

### "Buffered or unbuffered channel?"
- Default: **unbuffered**.
- You know the exact number of goroutines writing → **buffered to that count**.
- Implementing backpressure (token bucket) → **buffered with `select default`**.
- Otherwise unbuffered.

### "Generics, interfaces, or reflection?"
- Same algorithm, different concrete types, no behaviour polymorphism needed → **generics**.
- Behaviour polymorphism across concrete types → **interface**.
- Type unknown until runtime (JSON parsing, DB drivers) → **reflection**, but only at the boundary.

### "What test should I write?"
- Code has many independent input/output scenarios → **table test**.
- Code reads untrusted input / network data → **fuzz test** (alongside table tests).
- Code does concurrency → **run with `-race`** and add table tests.
- Code wraps an HTTP handler → **httptest.NewServer + table test**.
- Code uses an interface with many methods → **stub via embedded interface or function-field struct**.
- Want to test only the public API → use `package foo_test`.

### "When do I use the `context`?"
- Function blocks on I/O, network, or another goroutine that may need cancellation → **first parameter is `ctx`**.
- Top-level entrypoint → use `context.Background()` or `context.TODO()`.
- HTTP server: extract via `r.Context()` in middleware, re-attach via `req.WithContext(ctx)`.
- Cross-cutting request data (request IDs, trace IDs, user identity) → store via `context.WithValue` using a private key type.
- Cancellation propagation → `WithCancel` / `WithTimeout` / `WithDeadline`; always `defer cancel()`.

### "When to use `defer`?"
- Resource cleanup (Close, Unlock, Remove, Rollback) → **always defer**.
- Per-iteration cleanup in a loop → **inline the cleanup**, do NOT defer (defers accumulate until function exit).
- Need to modify a named return value (especially the error) → use `defer func() { if err != nil { ... } }()`.

### "When to use a custom error type vs a sentinel?"
- Caller must react programmatically (e.g. status code mapping) → **custom type + `errors.As`**.
- State means "cannot continue, but caller needs no extra info" → **sentinel + `errors.Is`**.
- Routine validation with several independent problems → **sentinel + `errors.Join`**.

### "What should I do before committing?"
1. `gofmt` / `goimports ./...`
2. `go vet ./...`
3. `go test -race ./...`
4. `staticcheck ./...`
5. `govulncheck ./...`
6. Check coverage on changed files (`go test -coverprofile=... ./...`)

---

## Key Takeaways

1. **Make intentions explicit.** Idiomatic Go is verbose on purpose — clarity beats cleverness.
2. **Errors are values.** Return them, wrap them with `%w`, inspect with `errors.Is`/`errors.As`. Never panic for ordinary failure.
3. **Zero values are useful.** Design types so the zero value is a valid starting state.
4. **Accept interfaces, return structs.** Decouple input, stay flexible on output.
5. **Composition over inheritance.** Embed for promotion, interfaces for polymorphism.
6. **Concurrency is data-flow design.** Channels for pipelines, mutexes for shared state, contexts for cancellation. Never expose concurrency primitives in your public API.
7. **Always clean up goroutines.** Every `go` statement must have an exit path.
8. **Test at boundaries.** Table tests for breadth, fuzz for unknown input, httptest for HTTP, `-race` for concurrency, go-cmp for comparison.
9. **100% coverage is necessary, not sufficient.** Coverage tells you what you DIDN'T exercise — never use it as proof of correctness.
10. **Use reflection, unsafe, and cgo only at boundaries.** Each one breaks Go's safety guarantees for a real but bounded payoff.
11. **The Go Compatibility Promise is real.** Lean on `go.mod`'s `go` directive and the new `GOTOOLCHAIN` mechanism — your code will keep building.
12. **Idiomatic Go is boring.** That's the point — boring code is maintainable code.

---

## Cross-References

- Related: `[[../Concurrency_in_Go.md]]` (Katherine Cox-Buday — deep concurrency patterns)
- Related: `[[../Go_Systems_Programming.md]]` (low-level Go, OS interaction)
- Related: `[[../Building_Modern_CLI_Applications_in_Go.md]]` (CLI patterns, packaging)
- Related: `[[../The_Art_of_Unit_Testing.md]]` (testing theory, double-loop TDD)
- Related: `[[../Fundamentals_of_Software_Testing.md]]` (test taxonomy, integration vs unit)
- Related: `[[../Domain-Driven_Design_with_Golang.md]]` (DDD in Go: bounded contexts, aggregates, repositories)
- Related: `[[../Efficient_Go_Data-Driven_Optimization.md]]` (data-driven performance tuning)
- Topic index: `[[../INDEX.md]]`