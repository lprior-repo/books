# 100 Go Mistakes and How to Avoid Them
**Author:** Teiva Harsanyi
**Topic tags:** `#general` `#concurrency` `#testing` `#api` `#cli`
**Language focus:** Go-first
**Sources:** `markdown_output/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi.md` · `summaries/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi.md`

## TL;DR
A catalog of 100 Go anti-patterns organized by Go's own domain model — code/project organization, data types, control structures, strings, functions, error management, concurrency foundations and practice, standard library, testing, and optimization. This deep-dive condenses every mistake into a crisp do/don't with the book's bad/good code snippets preserved verbatim, plus the cluster-level trade-offs you need to internalize to write idiomatic, race-free, production-grade Go.

---

## Best Practices by Topic

### Variable Shadowing and Scope Hygiene

**Principle:** `:=` redeclares; `=` assigns. One silently shadows the other — and Go's shadow analyzer (via `go vet -vettool=$(which shadow)`) is your only safety net.

**Do:**
- Use `:=` only when introducing a new variable in the current scope.
- Use `=` when assigning to an existing outer-scope variable.
- Run `go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow` and add it to vet in CI.

**Don't:**
- Use `:=` inside an `if` / `for` / `switch` body when you meant to assign to an outer variable.
- Trust that "looks like assignment" means assignment.

**Code:**
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
*Ref: 100_Go_Mistakes.md — "#1: Unintended variable shadowing"*

---

### Happy-Left Alignment and Early Returns

**Principle:** Keep the happy path on the left edge of the screen; use guard clauses (early returns) instead of nested `if/else`.

**Do:**
- Invert conditions and return early on errors.
- Read top-to-bottom; reserve nesting for the happy path.

**Don't:**
- Nest `if cond { if cond2 { ... } else { return err1 } } else { return err2 }`.

**Code:**
```go
// BAD
if condition {
    if anotherCondition {
        // do work
    } else {
        return errors.New("another condition failed")
    }
} else {
    return errors.New("condition failed")
}

// GOOD
if !condition {
    return errors.New("condition failed")
}
if !anotherCondition {
    return errors.New("another condition failed")
}
// happy path - do work
```
*Ref: 100_Go_Mistakes.md — "#2: Unnecessary nested code"*

---

### init() Discipline

**Principle:** `init()` runs before `main()`, can't return errors, complicates testing, and forces package-global state. Use it only when failure means the process must abort.

**Do:**
- Wrap dependency creation in plain `func NewX() (*X, error)` and return errors.
- Reserve `init()` for static, can't-fail setup (e.g., HTTP route registration, `MustCompile` regexes for known-valid patterns).

**Don't:**
- Open DB connections in `init()` — you force callers into panics and make integration testing painful.
- Stash results in package-level globals from `init()`.

**Code:**
```go
// BAD
var db *sql.DB
func init() {
    dataSourceName := os.Getenv("MYSQL_DATA_SOURCE_NAME")
    d, err := sql.Open("mysql", dataSourceName)
    if err != nil {
        log.Panic(err)
    }
    err = d.Ping()
    if err != nil {
        log.Panic(err)
    }
    db = d
}

// GOOD
func createClient(dsn string) (*sql.DB, error) {
    db, err := sql.Open("mysql", dsn)
    if err != nil {
        return nil, err
    }
    if err = db.Ping(); err != nil {
        return nil, err
    }
    return db, nil
}
```
*Ref: 100_Go_Mistakes.md — "#3: Misusing init functions"*

---

### Getters and Setters — Idiomatic Naming

**Principle:** Go has no auto-properties. Don't add Java-style `Get*`/`Set*` everywhere; expose fields and reach for a method only when you need encapsulation, validation, or computed semantics.

**Do:**
- `func (c Customer) Balance() float64` — no `Get` prefix for non-boolean getters.
- `func (c Customer) IsActive() bool` — `Get` prefix only on bool getters per Go convention.
- `SetBalance(...)` is fine when there is real behavior behind the set.

**Don't:**
- Write `GetBalance()` / `SetBalance()` for plain field access.

**Code:**
```go
// Naming convention
currentBalance := customer.Balance()
if currentBalance < 0 {
    customer.SetBalance(0)
}
```
*Ref: 100_Go_Mistakes.md — "#4: Overusing getters and setters"*

---

### Interface Pollution and the Discovery Rule

**Principle:** "Don't design with interfaces, discover them." Interfaces exist to abstract; the consumer defines the interface, not the producer.

**Do:**
- Create interfaces when you have ≥2 implementations (real polymorphism) or for mocking.
- Define the interface in the consumer package with only the methods it uses (Interface Segregation Principle).

**Don't:**
- Create an interface in the producer package "just in case".
- Make single-implementation interfaces.
- Pre-emptively declare interface hierarchies.

**Code:**
```go
// Producer-side interface — BAD
package store
type CustomerStorage interface {
    StoreCustomer(customer Customer) error
    GetCustomer(id string) (Customer, error)
    UpdateCustomer(customer Customer) error
    GetAllCustomers() ([]Customer, error)
    GetCustomersWithoutContract() ([]Customer, error)
    GetCustomersWithNegativeBalance() ([]Customer, error)
}

// Consumer-side minimal interface — GOOD
package client
type customersGetter interface {
    GetAllCustomers() ([]store.Customer, error)
}
```
*Ref: 100_Go_Mistakes.md — "#5: Interface pollution", "#6: Interface on the producer side"*

**Rule of thumb from Rob Pike:** *"The bigger the interface, the weaker the abstraction."*

---

### Returning Interfaces vs Concrete Types

**Principle:** Return concrete types; accept interfaces when possible. (Postel's law: be conservative in what you do, be liberal in what you accept.)

**Do:**
- Return `*client` so callers retain the full concrete API.
- Accept `io.Reader` for inputs.

**Don't:**
- Return interfaces from constructors — this creates import cycles and hides the API.

**Code:**
```go
// BAD: forces caller to depend on interface package, hides methods
func NewClient() Client { ... }

// GOOD: caller still satisfies Client implicitly if needed
func NewClient() *client { ... }
```
*Ref: 100_Go_Mistakes.md — "#7: Returning interfaces"*

---

### `any` Says Nothing

**Principle:** `any` (alias for `interface{}`) carries zero type info and moves errors to runtime. Use generics or per-type methods when you need polymorphism.

**Do:**
- Use generics (Go 1.18+) for type-parameterized code.
- Declare per-type methods (`GetContract`, `SetContract`) when you have a closed set of types.

**Don't:**
- Use `any` as a default storage type — it disables compile-time safety.

**Code:**
```go
// BAD
func (s *Store) Get(id string) (any, error) { ... }
func (s *Store) Set(id string, v any) error { ... }

// GOOD
func (s *Store) GetContract(id string) (Contract, error) { ... }
func (s *Store) SetContract(id string, contract Contract) error { ... }
```
*Ref: 100_Go_Mistakes.md — "#8: any says nothing"*

**Exception:** `json.Marshal(v any)` and `db.QueryContext(... args ...any)` legitimately accept arbitrary types — that's their contract.

---

### When to Use Generics

**Principle:** Generics factor boilerplate, not architecture. Use them when you see duplication, not preemptively.

**Do:**
- Use generics for slice/map utilities, data structures (binary trees, linked lists, heaps), and merging channels.
- Use constraints (`comparable`, `~int | ~string`) to express requirements.

**Don't:**
- Use generics where a concrete type is clearer.
- Use generics to call a single method on the type parameter (just take the interface).

**Code:**
```go
// GOOD: data structure
type Node[T any] struct {
    Val  T
    next *Node[T]
}

func (n *Node[T]) Add(next *Node[T]) {
    n.next = next
}

// BAD: just take the interface
func foo[T io.Writer](w T) {
    b := getBytes()
    _, _ = w.Write(b)
}
// prefer: func foo(w io.Writer) { ... }

// GOOD: factoring out sorting behavior
type SliceFn[T any] struct {
    S       []T
    Compare func(T, T) bool
}

func (s SliceFn[T]) Len() int           { return len(s.S) }
func (s SliceFn[T]) Less(i, j int) bool { return s.Compare(s.S[i], s.S[j]) }
func (s SliceFn[T]) Swap(i, j int)      { s.S[i], s.S[j] = s.S[j], s.S[i] }
```
*Ref: 100_Go_Mistakes.md — "#9: Being confused about when to use generics"*

**`~int` vs `int`:** `~int` accepts any type whose underlying type is `int` (e.g., `type customInt int`); `int` accepts only the literal `int`.

---

### Type Embedding Pitfalls

**Principle:** Embedding promotes fields and methods. Don't embed types whose methods shouldn't be public — especially `sync.Mutex`.

**Do:**
- Use named fields for sync primitives: `mu sync.Mutex`.
- Use embedding for true composition (e.g., embedding `io.WriteCloser` to satisfy an interface) when the promotion is desired.

**Don't:**
- Embed `sync.Mutex` — `Lock`/`Unlock` leak to consumers.
- Embed for cosmetic syntactic sugar alone.

**Code:**
```go
// BAD: leaks mutex methods
type InMem struct {
    sync.Mutex
    m map[string]int
}

// GOOD: encapsulation preserved
type InMem struct {
    mu sync.Mutex
    m  map[string]int
}

// GOOD: embedding for interface satisfaction
type Logger struct {
    io.WriteCloser
}
```
*Ref: 100_Go_Mistakes.md — "#10: Not being aware of the possible problems with type embedding"*

---

### Functional Options Pattern

**Principle:** For optional constructor parameters, prefer variadic `Option` functions over config structs and the builder pattern.

**Do:**
- Define `type Option func(*options) error`.
- Validate inside each `WithX` closure.
- Iterate opts in the constructor.

**Don't:**
- Use pointer fields in a Config struct to distinguish "not set" from zero (ugly).
- Use the builder pattern — non-idiomatic for Go.

**Code:**
```go
type options struct {
    port *int
}
type Option func(options *options) error

func WithPort(port int) Option {
    return func(options *options) error {
        if port < 0 {
            return errors.New("port should be positive")
        }
        options.port = &port
        return nil
    }
}

func NewServer(addr string, opts ...Option) (*http.Server, error) {
    var options options
    for _, opt := range opts {
        err := opt(&options)
        if err != nil {
            return nil, err
        }
    }
    // ...port handling logic
}

// Call site
server, err := httplib.NewServer("localhost",
    httplib.WithPort(8080),
    httplib.WithTimeout(time.Second))

// Default config — clean
server, err := httplib.NewServer("localhost")
```
*Ref: 100_Go_Mistakes.md — "#11: Not using the functional options pattern"*

---

### Project Layout and Package Naming

**Principle:** Use the project-layout convention (`cmd/`, `internal/`, `pkg/`); name packages by what they **provide**, not what they **contain**.

**Do:**
- `cmd/<app>/main.go` for entry points.
- `internal/` for code that must not be importable externally.
- Short, lowercase, single-word package names.
- Domain-driven grouping (per context) or hexagonal layout — pick one and stay consistent.

**Don't:**
- Create `util`, `common`, `shared`, `base` packages — they become junk drawers.
- Name packages the same as stdlib (`strings`, `http`).
- Use a package name that conflicts with one of its variables.

**Code:**
```go
// BAD
package util
func NewStringSet(...string) map[string]struct{} { ... }
func SortStringSet(map[string]struct{}) []string { ... }

// GOOD
package stringset
type Set map[string]struct{}
func New(...string) Set { ... }
func (s Set) Sort() []string { ... }
```
*Ref: 100_Go_Mistakes.md — "#12: Project misorganization", "#13: Creating utility packages", "#14: Ignoring package name collisions"*

---

### Documentation Discipline

**Principle:** Document every exported element. Comments start with the name being documented.

**Do:**
- `// Customer is a customer representation.` precedes `type Customer struct{}`.
- `// Deprecated: ...` for deprecated symbols (IDE will warn).
- Document packages with `// Package math provides ...`.
- Use `go doc` and `pkg.go.dev`.

**Don't:**
- Omit doc comments on exported items.
- Write implementation details in public docs.

**Code:**
```go
// Customer is a customer representation.
type Customer struct{}

// ID returns the customer identifier.
func (c Customer) ID() string { return "" }

// ComputePath returns the fastest path between two points.
// Deprecated: This function uses a deprecated way to compute
// the fastest path. Use ComputeFastestPath instead.
func ComputePath() {}
```
*Ref: 100_Go_Mistakes.md — "#15: Missing code documentation"*

---

### Lint and Format Toolchain

**Principle:** Automate `go vet`, `gofmt`, `goimports`, `staticcheck`, `golangci-lint` in CI.

**Do:**
- `go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow` and run via `go vet`.
- Use `golangci-lint` as a one-stop aggregator.
- Run them on pre-commit and in CI.

**Don't:**
- Rely on review alone to catch shadowing, errcheck, gocyclo, goconst.

**Code:**
```bash
$ go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow
$ go vet -vettool=$(which shadow)
./main.go:8:3: declaration of "i" shadows declaration at line 6
```
*Ref: 100_Go_Mistakes.md — "#16: Not using linters"*

---

### Octal, Hex, Binary Literals

**Principle:** `010` is octal (8 in decimal). Use the `0o` prefix for clarity.

**Do:**
- Use `0o644`, `0xFF`, `0b1010`, underscores `1_000_000_000`.

**Don't:**
- Write `0644` and expect the next reader to spot octal.

**Code:**
```go
sum := 100 + 010 // prints 108, not 110
fmt.Println(sum)

file, err := os.OpenFile("foo", os.O_RDONLY, 0o644) // clearer
```
*Ref: 100_Go_Mistakes.md — "#17: Creating confusion with octal literals"*

---

### Integer Overflow is Silent

**Principle:** Runtime integer overflow wraps silently — no panic. Check explicitly when working with narrow types or untrusted input.

**Do:**
- Bound check before increment/add/mul against `math.MaxInt32`, `math.MaxInt64`, `math.MinInt`.
- Use `math/big` for arbitrary precision.

**Don't:**
- Trust `int32` arithmetic with external values.

**Code:**
```go
func Inc32(counter int32) int32 {
    if counter == math.MaxInt32 {
        panic("int32 overflow")
    }
    return counter + 1
}

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
    if a == 1 || b == 1 {
        return result
    }
    if a == math.MinInt || b == math.MinInt {
        panic("integer overflow")
    }
    if result/b != a {
        panic("integer overflow")
    }
    return result
}
```
*Ref: 100_Go_Mistakes.md — "#18: Neglecting integer overflows"*

---

### Floating Point is Approximation

**Principle:** IEEE-754 floats can't represent most decimals exactly. Compare with a delta; order operations to favor accuracy.

**Do:**
- Compare with `testify.InDelta` or a small epsilon.
- Group operations of similar magnitude for additions/subtractions.
- Do multiplication/division before addition/subtraction when accuracy matters.

**Don't:**
- Compare floats with `==`.
- Use float64 for money — use `int64` cents or `math/big`/`shopspring/decimal`.

**Code:**
```go
// Order matters: f2 is more accurate
func f1(n int) float64 {
    result := 10_000.
    for i := 0; i < n; i++ {
        result += 1.0001
    }
    return result
}

func f2(n int) float64 {
    result := 0.
    for i := 0; i < n; i++ {
        result += 1.0001
    }
    return result + 10_000.
}

// Special values
var a float64
positiveInf := 1 / a  // +Inf
negativeInf := -1 / a // -Inf
nan := a / a          // NaN (NaN is the only float satisfying f != f)
math.IsInf(x, 0)
math.IsNaN(x)
```
*Ref: 100_Go_Mistakes.md — "#19: Not understanding floating points"*

---

### Slice Length vs Capacity

**Principle:** `len(s)` is what you can read; `cap(s)` is the backing array size. `append` may or may not allocate.

**Do:**
- Allocate with `make([]T, len, cap)` when length is known.
- Slice with the full expression `s[low:high:max]` when you need to bound capacity.

**Don't:**
- Confuse length and capacity — `s[cap(s)-1]` will panic if `len(s) < cap(s)`.

**Code:**
```go
s := make([]int, 3, 6) // length 3, capacity 6
s[1] = 1
s = append(s, 2)            // uses spare capacity
s = append(s, 3, 4, 5)      // backing array full -> grows
fmt.Println(s)              // [0 1 0 2 3 4 5]

s1 := make([]int, 3, 6)
s2 := s1[1:3]                // length 2, capacity 5 (same backing array)
s2 = append(s2, 2)          // mutates backing array; s1[2] = 2!
```
*Ref: 100_Go_Mistakes.md — "#20: Not understanding slice length and capacity"*

---

### Preallocate Slices When Length is Known

**Principle:** Letting a slice grow via repeated `append` doubles and copies; preallocate to amortize.

**Do:**
- `make([]T, 0, n)` + `append`, OR `make([]T, n)` + direct index assignment.

**Don't:**
- Start with `make([]T, 0)` when you know the target size.

**Code:**
```go
func convert(foos []Foo) []Bar {
    n := len(foos)
    bars := make([]Bar, n)
    for i, foo := range foos {
        bars[i] = fooToBar(foo)
    }
    return bars
}

// Or use capacity + append if readability matters more
bars := make([]Bar, 0, n)
for _, foo := range foos {
    bars = append(bars, fooToBar(foo))
}
```
*Ref: 100_Go_Mistakes.md — "#21: Inefficient slice initialization"*

**Benchmark result for 1M elements:** empty slice ~50ms; preallocate ~13ms; preallocate-with-length ~13ms. The first approach is **~400% slower**.

---

### nil vs Empty Slices

**Principle:** `nil` slice has no backing array (no allocation); empty slice `[]int{}` has one. JSON marshals them differently.

**Do:**
- Default to `var s []int` for "no elements yet".
- Use `make([]T, n)` when length is known.

**Don't:**
- Return `[]int{}` from a function that might have no elements — it allocates.

**Code:**
```go
// All four have len == 0, but only #1 and #2 are nil
var s []string         // nil, no allocation
s = []string(nil)      // nil, no allocation
s = []string{}         // non-nil, allocated
s = make([]string, 0)  // non-nil, allocated

// JSON marshal
// nil slice -> null
// empty slice -> []
```
*Ref: 100_Go_Mistakes.md — "#22: Being confused about nil vs. empty slices"*

---

### Check Slice Emptiness by Length, Not nil

**Principle:** `len(s) == 0` works for both nil and empty slices; `s == nil` only catches nil. Different libraries distinguish — don't rely on that distinction.

**Do:**
- Always check `len(s) == 0`.

**Don't:**
- Branch on `s == nil`.

**Code:**
```go
if len(operations) != 0 {
    handle(operations)
}
```
*Ref: 100_Go_Mistakes.md — "#23: Not properly checking if a slice is empty"*

---

### Slice Copy with the Right Length

**Principle:** `copy(dst, src)` copies `min(len(dst), len(src))` elements. Initialize `dst` length or you'll copy zero.

**Do:**
- `dst := make([]int, len(src)); copy(dst, src)`.

**Don't:**
- `var dst []int; copy(dst, src)` — copies nothing.

**Code:**
```go
src := []int{0, 1, 2}
dst := make([]int, len(src))
copy(dst, src) // dst == [0 1 2]

// alt one-liner
dst := append([]int(nil), src...)
```
*Ref: 100_Go_Mistakes.md — "#24: Not making slice copies correctly"*

**Argument order:** destination is **first** (`copy(dst, src)`).

---

### Hidden append Side Effects on Shared Backing Arrays

**Principle:** If you slice from a slice, the result shares the backing array. `append` may overwrite sibling data.

**Do:**
- Use full slice expression `s[low:high:max]` to constrain capacity.
- Copy when the callee must not see or mutate sibling data.

**Don't:**
- Pass a `s[:n]` slice and assume `append` inside the callee can't reach beyond `n`.

**Code:**
```go
s := []int{1, 2, 3}
f(s[:2:2]) // length 2, capacity 2 — f's append won't touch s[2]
```
*Ref: 100_Go_Mistakes.md — "#25: Unexpected side effects using slice append"*

---

### Slice Memory Leaks

**Principle:** Two leak modes — leaking capacity (reslicing a huge array keeps the whole backing array alive) and slice-of-pointers (GC can't reclaim unreferenced pointed-to objects).

**Do:**
- Copy the small portion out (`make([]T, n); copy(...)`).
- Nil out excluded pointer/struct-pointer elements before slicing.

**Don't:**
- `return hugeMsg[:5]` and store it.

**Code:**
```go
func getMessageType(msg []byte) []byte {
    msgType := make([]byte, 5)
    copy(msgType, msg)
    return msgType
}

// slice of pointers / pointer fields
func keepFirstTwoElementsOnly(foos []Foo) []Foo {
    for i := 2; i < len(foos); i++ {
        foos[i].v = nil // release slice backing arrays
    }
    return foos[:2]
}
```
*Ref: 100_Go_Mistakes.md — "#26: Slices and memory leaks"*

**Note:** Full slice expression `msg[:5:5]` does NOT release the underlying space — only a copy does.

---

### Preallocate Maps

**Principle:** Maps grow by doubling buckets; preallocate to avoid rehash.

**Do:**
- `m := make(map[K]V, expectedSize)`.

**Don't:**
- Add to a `nil` or `make(map[K]V)` map in a hot loop.

**Code:**
```go
m := make(map[string]int, 1_000_000)

// Benchmark with 1M inserts:
// make(map[string]int)            227413490 ns/op
// make(map[string]int, 1_000_000)  91174193 ns/op  (~60% faster)
```
*Ref: 100_Go_Mistakes.md — "#27: Inefficient map initialization"*

---

### Maps Never Shrink

**Principle:** Map buckets aren't released when you delete entries. For long-lived maps with bursty traffic, recreate periodically.

**Do:**
- For cache-style maps with key/value >128 bytes, use `map[K]*V` to shrink the per-entry footprint.
- Recreate maps periodically if peak >> steady-state.

**Don't:**
- Assume `delete` returns memory.

**Code:**
```go
// For 1M entries of [128]byte:
// map[int][128]byte: 461 MB peak, 293 MB after delete + GC
// map[int]*[128]byte: 182 MB peak, 38 MB after delete + GC
```
*Ref: 100_Go_Mistakes.md — "#28: Maps and memory leaks"*

---

### Comparing Values Correctly

**Principle:** `==` works on comparable types (booleans, numerics, strings, pointers, channels, interfaces, structs/arrays composed of these). Slices, maps, and funcs are NOT comparable with `==`.

**Do:**
- Use `bytes.Equal` for `[]byte`.
- Use `reflect.DeepEqual` in tests (slower) or write a custom comparator.
- Be aware `reflect.DeepEqual` distinguishes nil from empty slices.

**Don't:**
- Compare slices/maps with `==` (compile error).
- Store slices/maps in fields of a struct that you compare with `==` (compile error).
- Use `any` to bypass — comparing two `any` values containing uncomparable types panics at runtime.

**Code:**
```go
// Custom comparator is ~96x faster than reflect.DeepEqual
func (a customer) equal(b customer) bool {
    if a.id != b.id {
        return false
    }
    if len(a.operations) != len(b.operations) {
        return false
    }
    for i := 0; i < len(a.operations); i++ {
        if a.operations[i] != b.operations[i] {
            return false
        }
    }
    return true
}
```
*Ref: 100_Go_Mistakes.md — "#29: Comparing values incorrectly"*

---

### Range Loops Copy Elements

**Principle:** In `for _, v := range s`, `v` is a copy. Mutating `v` doesn't mutate the slice.

**Do:**
- Use `for i := range s { s[i].field = ... }` to mutate.
- Or use `[]*T` (slices of pointers) if you want `v.field = ...` to work.

**Don't:**
- Iterate by value with the intent to mutate.

**Code:**
```go
accounts := []account{
    {balance: 100.}, {balance: 200.}, {balance: 300.},
}
for _, a := range accounts {
    a.balance += 1000 // modifies the COPY
}
// accounts is still [{100} {200} {300}]
```
*Ref: 100_Go_Mistakes.md — "#30: Ignoring the fact that elements are copied in range loops"*

---

### Range Expression is Evaluated Once

**Principle:** The `range` expression is evaluated once before the loop. For channels, you can't "switch" mid-loop; for arrays, you get a copy.

**Do:**
- For arrays, use `range &a` to iterate by pointer.

**Don't:**
- Try to swap the channel being ranged.

**Code:**
```go
ch := ch1
for v := range ch { // ch is evaluated once (== ch1)
    fmt.Println(v)
    ch = ch2 // doesn't affect range
}
```
*Ref: 100_Go_Mistakes.md — "#31: Ignoring how arguments are evaluated in range loops"*

---

### Pointer Elements in Range Loops

**Principle:** `for _, customer := range customers` creates one `customer` variable per loop, with one stable address. Storing `&customer` stores the same pointer N times.

**Do:**
- `current := customer; s.m[current.ID] = &current`.
- Or `customer := &customers[i]`.

**Don't:**
- `s.m[customer.ID] = &customer` for non-trivial loops.

**Code:**
```go
func (s *Store) storeCustomers(customers []Customer) {
    for i := range customers {
        customer := &customers[i]
        s.m[customer.ID] = customer
    }
}
```
*Ref: 100_Go_Mistakes.md — "#32: Ignoring the impact of using pointer elements in range loops"*

---

### Map Iteration is Unspecified

**Principle:** Map iteration order is randomized — never assume ordering or insertion order. Adding keys during iteration may or may not be visited.

**Do:**
- Use a binary heap or sort separately if order matters.
- Iterate a copy if you need to mutate the source.

**Don't:**
- Assume any ordering from `range m`.
- Rely on keys added mid-iteration being visited.

**Code:**
```go
m2 := copyMap(m)
for k, v := range m {
    m2[k] = v
    if v {
        m2[10+k] = true
    }
}
```
*Ref: 100_Go_Mistakes.md — "#33: Making wrong assumptions during map iterations"*

---

### break, continue, switch, select, label

**Principle:** `break` in a `switch`/`select` only exits the innermost statement — it does NOT exit the surrounding `for`. Use labels.

**Do:**
- `break loop` to exit a labeled `for`.

**Don't:**
- Assume `break` inside `switch` exits the loop.

**Code:**
```go
loop:
    for i := 0; i < 5; i++ {
        switch i {
        case 2:
            break loop
        }
    }
```
*Ref: 100_Go_Mistakes.md — "#34: Ignoring how the break statement works"*

**Bonus:** `continue loop` works too — restart the labeled loop iteration.

---

### defer in Loops Accumulates

**Principle:** `defer` runs at function return, not loop iteration end. Deferred calls stack up.

**Do:**
- Extract loop body into its own function so `defer` runs per iteration.

**Don't:**
- `defer f.Close()` inside a `for` over a million paths.

**Code:**
```go
func readFiles(ch <-chan string) error {
    for path := range ch {
        if err := readFile(path); err != nil {
            return err
        }
    }
    return nil
}

func readFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()
    // Do something with file
    return nil
}
```
*Ref: 100_Go_Mistakes.md — "#35: Using defer inside a loop"*

---

### Runes Are Unicode Code Points

**Principle:** `len(s)` returns bytes; one rune may be 1–4 bytes in UTF-8. A rune is `int32`. String literals are UTF-8 but `[]byte` from outside may not be.

**Do:**
- `utf8.RuneCountInString(s)` for rune count.
- `for i, r := range s` iterates runes; `i` is the byte index.

**Don't:**
- Use `s[i]` to access the i-th rune.
- Assume `len("é") == 1`.

**Code:**
```go
s := "hêllo"
fmt.Println(len(s))                     // 6 (bytes)
fmt.Println(utf8.RuneCountInString(s))  // 5 (runes)

for i, r := range s {
    fmt.Printf("position %d: %c\n", i, r)
}
// position 0: h
// position 1: ê
// position 3: l
// position 4: l
// position 5: o
```
*Ref: 100_Go_Mistakes.md — "#36: Not understanding the concept of a rune"*

---

### String Iteration: Bytes vs Runes

**Principle:** `for i := 0; i < len(s); i++` iterates bytes; `range s` iterates runes.

**Do:**
- Use `range` for rune iteration; use `[]rune(s)` when you need rune-by-rune indexing.

**Don't:**
- Mix `s[i]` indexing with rune semantics.

**Code:**
```go
// Bytes (wrong for multi-byte chars)
for i := 0; i < len(s); i++ {
    fmt.Printf("%c ", s[i])
}

// Runes (correct)
for i, r := range s {
    fmt.Printf("position %d: %c\n", i, r)
}
```
*Ref: 100_Go_Mistakes.md — "#37: Inaccurate string iteration"*

---

### Trim Functions: Set vs Substring

**Principle:** `TrimRight(s, "xo")` removes any trailing chars in the SET `{x, o}` — not the substring `"xo"`. Use `TrimSuffix` for substring removal.

**Do:**
- `TrimRight`/`TrimLeft` for character sets.
- `TrimSuffix`/`TrimPrefix` for substrings.

**Don't:**
- Use `TrimRight` to strip a file extension.

**Code:**
```go
strings.TrimRight("123oxo", "xo")    // "123" (each trailing x or o removed)
strings.TrimSuffix("123oxo", "xo")   // "123o" (substring removed)
strings.TrimLeft("oxo123", "ox")     // "123"
strings.TrimPrefix("oxo123", "ox")   // "o123"
strings.Trim("oxo123oxo", "ox")      // "123"
```
*Ref: 100_Go_Mistakes.md — "#38: Misusing trim functions"*

---

### String Concatenation Performance

**Principle:** `s += v` reallocates each iteration because strings are immutable. Use `strings.Builder` and preallocate with `Grow`.

**Do:**
- `strings.Builder` + `WriteString`; call `Grow(total)` if you know the final length.

**Don't:**
- Concatenate with `+` in a tight loop.

**Code:**
```go
func concat(values []string) string {
    total := 0
    for i := 0; i < len(values); i++ {
        total += len(values[i])
    }
    sb := strings.Builder{}
    sb.Grow(total)
    for _, value := range values {
        _, _ = sb.WriteString(value)
    }
    return sb.String()
}

// Benchmark (1000 strings × 1000 bytes):
// v1 (+ operator):      72,291,485 ns/op
// v2 (Builder no grow):    878,962 ns/op
// v3 (Builder + Grow):     190,340 ns/op (~99% faster than v1)
```
*Ref: 100_Go_Mistakes.md — "#39: Under-optimized string concatenation"*

---

### Avoid Useless []byte ↔ string Conversions

**Principle:** Each `[]byte`↔`string` conversion allocates. The `bytes` package mirrors the `strings` API for byte work.

**Do:**
- Keep I/O code in `[]byte`; use `bytes.TrimSpace`, `bytes.Split`, etc.

**Don't:**
- Round-trip through `string` just to call `strings.TrimSpace`.

**Code:**
```go
func sanitize(b []byte) []byte {
    return bytes.TrimSpace(b) // no []byte→string→[]byte round-trip
}
```
*Ref: 100_Go_Mistakes.md — "#40: Useless string conversions"*

**Bonus:** `[]byte` is immutable once converted to `string`:
```go
b := []byte{'a', 'b', 'c'}
s := string(b)
b[1] = 'x'
fmt.Println(s) // "abc" (the string holds its own copy)
```

---

### Substring Memory Leaks

**Principle:** A substring shares the backing array of the original string. Storing a 5-byte UUID from a 1 MB log keeps the whole log alive.

**Do:**
- `strings.Clone(s)` (Go 1.18+) or `string([]byte(s[:n]))` to force a copy.

**Don't:**
- Store `log[:36]` long-term.

**Code:**
```go
uuid := strings.Clone(log[:36])
s.store(uuid)

// or manually
uuid := string([]byte(log[:36]))
```
*Ref: 100_Go_Mistakes.md — "#41: Substrings and memory leaks"*

---

### Receiver Types: Value vs Pointer

**Principle:** Receiver must be a pointer when (a) method mutates receiver or (b) receiver contains a sync primitive. Receiver must be a value when (a) immutability is required or (b) receiver is a map/func/channel.

**Do:**
- Default to pointer receivers when in doubt.
- Stay consistent within a type.
- Use value receivers for small immutable types (`time.Time`).

**Don't:**
- Mix value and pointer receivers casually.

**Code:**
```go
// Pointer receiver — needed when mutex is embedded as a value
func (c *Counter) Increment(name string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.counters[name]++
}
```
*Ref: 100_Go_Mistakes.md — "#42: Not knowing which type of receiver to use"*

**Consistency note:** `time.Time` mixes both because it must satisfy `encoding.TextUnmarshaler.UnmarshalBinary([]byte) error` (needs pointer) while enforcing immutability for most methods.

---

### Named Return Parameters

**Principle:** Named returns add context and are required for `defer` to mutate the result, but their zero values can hide bugs.

**Do:**
- Name returns when there are multiple values of the same type, or when `defer` modifies them.

**Don't:**
- Rely on naked returns in long functions.
- Return the named variable without thinking — its zero value may not be what you want.

**Code:**
```go
// GOOD: lat/lng names clarify semantics
func (l loc) getCoordinates(ctx context.Context, address string) (
    lat, lng float32, err error) {
    // ...
}

// Named returns for defer-modification pattern
func getBalance(db *sql.DB, clientID string) (
    balance float32, err error) {
    rows, err := db.Query(query, clientID)
    if err != nil {
        return 0, err
    }
    defer func() {
        closeErr := rows.Close()
        if err != nil {
            if closeErr != nil {
                log.Printf("failed to close rows: %v", err)
            }
            return
        }
        err = closeErr
    }()
    // ...
}
```
*Ref: 100_Go_Mistakes.md — "#43: Never using named result parameters", "#44: Unintended side effects with named result parameters"*

**Bug example:** `return 0, 0, err` (where err is a named return) returns `nil` because `err` was never assigned.

---

### Returning a Nil Receiver Wrapped in Interface

**Principle:** A nil pointer wrapped in an interface is NOT a nil interface. The interface holds `(type=*MultiError, value=nil)`.

**Do:**
- `return nil` explicitly when the interface should be nil.

**Don't:**
- Return a nil pointer typed as an interface.

**Code:**
```go
func (c Customer) Validate() error {
    var m *MultiError
    if c.Age < 0 {
        m = &MultiError{}
        m.Add(errors.New("age is negative"))
    }
    if c.Name == "" {
        if m == nil {
            m = &MultiError{}
        }
        m.Add(errors.New("name is nil"))
    }
    if m != nil {
        return m
    }
    return nil // explicit nil interface
}
```
*Ref: 100_Go_Mistakes.md — "#45: Returning a nil receiver"*

**Why:** `var foo *Foo; fmt.Println(foo.Bar())` is valid Go — nil is a valid receiver.

---

### Filenames vs io.Reader

**Principle:** Functions that read files should accept `io.Reader`, not a filename. It's testable, reusable, and decouples from the data source.

**Do:**
- `func countEmptyLines(reader io.Reader) (int, error)`.

**Don't:**
- `func countEmptyLinesInFile(filename string) (int, error)` — forces you to create test files.

**Code:**
```go
func countEmptyLines(reader io.Reader) (int, error) {
    scanner := bufio.NewScanner(reader)
    for scanner.Scan() {
        // ...
    }
}

// In tests
emptyLines, err := countEmptyLines(strings.NewReader(`foo
bar
baz`))
```
*Ref: 100_Go_Mistakes.md — "#46: Using a filename as a function input"*

---

### defer Argument and Receiver Evaluation

**Principle:** Arguments to `defer` are evaluated at the `defer` statement, not when the deferred function runs. The receiver is also evaluated at defer time.

**Do:**
- Pass a pointer if the value can change.
- Use a closure to capture variables at execution time.

**Don't:**
- `defer notify(status)` if `status` is set later — it captures the empty string.

**Code:**
```go
// BAD
defer notify(status)        // status frozen at defer time

// GOOD (pointer)
defer notify(&status)

// GOOD (closure)
defer func() {
    notify(status)
    incrementCounter(status)
}()
```
*Ref: 100_Go_Mistakes.md — "#47: Ignoring how defer arguments and receivers are evaluated"*

**Receiver behavior:** pointer receiver defers capture the pointer, so later mutations are visible; value receiver defers capture the value copy.

---

### When to Panic

**Principle:** Panic is for genuinely unrecoverable conditions: programmer errors and mandatory dependency failures.

**Do:**
- Panic for nil mandatory arguments (`nil` driver in `sql.Register`).
- Panic for invalid constants (`http.checkWriteHeaderCode` on code <100 or >999).
- Use `regexp.MustCompile` for patterns that must succeed at startup.

**Don't:**
- Panic for expected runtime failures (file not found, network down). Return `error`.

**Code:**
```go
func checkWriteHeaderCode(code int) {
    if code < 100 || code > 999 {
        panic(fmt.Sprintf("invalid WriteHeader code %v", code))
    }
}
```
*Ref: 100_Go_Mistakes.md — "#48: Panicking"*

---

### Error Wrapping and Context

**Principle:** Wrap with `%w` to preserve the chain for `errors.Is/As`. Use `%v` when you want to **transform** (not preserve) the source.

**Do:**
- `fmt.Errorf("failed to validate source coordinates: %w", err)` to add context AND preserve chain.

**Don't:**
- Wrap when the source is implementation detail (use `%v` instead).

**Code:**
```go
// preserve chain (caller can errors.Is/As)
return fmt.Errorf("bar failed: %w", err)

// transform (chain is broken)
return fmt.Errorf("bar failed: %v", err)

// sentinel — pass through directly
if err != nil {
    return err
}
```
*Ref: 100_Go_Mistakes.md — "#49: Ignoring when to wrap an error"*

---

### errors.Is and errors.As

**Principle:** `==` and type switches don't unwrap. Use `errors.Is(err, target)` for sentinels and `errors.As(err, &target)` for typed errors.

**Do:**
- `errors.Is(err, sql.ErrNoRows)` for sentinels.
- `errors.As(err, &transientError{})` for typed errors.

**Don't:**
- `err == sql.ErrNoRows` (fails if wrapped).
- `switch err.(type) { case MyError: ... }` (doesn't traverse chain).

**Code:**
```go
// Compare error value
if errors.Is(err, sql.ErrNoRows) {
    // ...
}

// Compare error type
if errors.As(err, &transientError{}) {
    http.Error(w, err.Error(), http.StatusServiceUnavailable)
}
```
*Ref: 100_Go_Mistakes.md — "#50: Checking an error type inaccurately", "#51: Checking an error value inaccurately"*

**Sentinel vs typed:** Expected errors → sentinels (`var ErrFoo = errors.New("foo")`); Unexpected errors → typed structs (`type BarError struct{...}`).

---

### Handle Errors Once

**Principle:** Logging + returning = duplicate handling. Pick one.

**Do:**
- Return the wrapped error and let the caller (or a top-level middleware) log it.

**Don't:**
- `log.Println(err); return err`.

**Code:**
```go
// BAD — duplicate logging
if err != nil {
    log.Println("failed to validate source coordinates")
    return Route{}, err
}

// GOOD — caller decides
return Route{}, fmt.Errorf("failed to validate source coordinates: %w", err)
```
*Ref: 100_Go_Mistakes.md — "#52: Handling an error twice"*

---

### Ignoring Errors Explicitly

**Principle:** `_ = someFunc()` is the only acceptable way to drop an error.

**Do:**
- Add a comment explaining WHY ignoring is safe.

**Don't:**
- Bare-call a function that returns an error without `_ =`.

**Code:**
```go
// At-most once delivery.
// Hence, it's accepted to miss some of them in case of errors.
_ = notify()
```
*Ref: 100_Go_Mistakes.md — "#53: Not handling an error"*

---

### defer Errors

**Principle:** `defer f.Close()` discards the error. For writable resources, that can silently lose data.

**Do:**
- Use named returns + a closure to capture and propagate the close error.
- Or at minimum, log it.

**Don't:**
- Use naked `defer f.Close()` for writable resources.

**Code:**
```go
func writeToFile(filename string, content []byte) (err error) {
    // Open file
    defer func() {
        closeErr := f.Close()
        if err == nil {
            err = closeErr
        }
    }()
    _, err = f.Write(content)
    return
}
```
*Ref: 100_Go_Mistakes.md — "#54: Not handling defer errors"*

---

### Concurrency vs Parallelism

**Principle:** Concurrency is structure; parallelism is execution. Coffee shop analogy: waiters + coffee machines = parallel; introducing a separate role = concurrent.

**Do:**
- Restructure the problem into stages first.
- Parallelize each stage separately.

**Don't:**
- Assume concurrent = faster.

**Code:** Rob Pike: *"Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once."*

*Ref: 100_Go_Mistakes.md — "#55: Mixing up concurrency and parallelism"*

---

### Concurrency Isn't Always Faster

**Principle:** Goroutine creation, scheduling, and synchronization all have overhead. Below a workload threshold, sequential is faster.

**Do:**
- Benchmark parallel vs sequential.
- Use a threshold to switch from sequential to parallel.

**Don't:**
- Recurse on tiny workloads into infinite goroutines.

**Code:**
```go
const max = 2048

func parallelMergesortV2(s []int) {
    if len(s) <= 1 {
        return
    }
    if len(s) <= max {
        sequentialMergesort(s) // below threshold: sequential
        return
    }
    middle := len(s) / 2
    var wg sync.WaitGroup
    wg.Add(2)
    go func() {
        defer wg.Done()
        parallelMergesortV2(s[:middle])
    }()
    go func() {
        defer wg.Done()
        parallelMergesortV2(s[middle:])
    }()
    wg.Wait()
    merge(s, middle)
}

// Benchmark on 10K elements:
// sequential: 2278993555 ns/op
// parallel v1 (no threshold): 17525998709 ns/op (~8x SLOWER)
// parallel v2 (threshold=2048): 1313010260 ns/op (~40% FASTER)
```
*Ref: 100_Go_Mistakes.md — "#56: Thinking concurrency is always faster"*

**Scheduler:** Go uses G-M-P model. `GOMAXPROCS` defaults to logical CPU count. Work-stealing from local queues. Preemptive since Go 1.14.

---

### Channels vs Mutexes

**Principle:** Parallel goroutines → mutexes (synchronization). Concurrent goroutines → channels (coordination, ownership transfer).

**Do:**
- Mutex for shared state among parallel workers.
- Channels for signaling and ownership transfer between stages.

**Don't:**
- Force channels for everything; mutex for everything.

*Ref: 100_Go_Mistakes.md — "#57: Being puzzled about when to use channels or mutexes"*

---

### Data Races vs Race Conditions

**Principle:** Data race = simultaneous access with at least one write. Race condition = behavior depends on timing (no data race required). Use `-race`.

**Do:**
- Run `go test -race ./...` in CI.
- Use atomic, mutex, or channels to prevent data races.

**Don't:**
- Confuse "race-condition-free" with "deterministic".

**Code:**
```go
// Data race
i := 0
go func() { i++ }()
go func() { i++ }()
```
*Ref: 100_Go_Mistakes.md — "#58: Not understanding race problems"*

**Fix options:** `atomic.AddInt64`, `sync.Mutex`, or pass value via channel.

---

### Workload Type: CPU-bound vs I/O-bound

**Principle:** Pool size = `GOMAXPROCS` for CPU-bound; depends on external system for I/O-bound.

**Do:**
- `runtime.GOMAXPROCS(0)` for the actual thread count.
- Use `runtime.NumCPU()` only if `GOMAXPROCS` ≤ NumCPU.

**Don't:**
- Spawn thousands of goroutines for CPU-bound work.

*Ref: 100_Go_Mistakes.md — "#59: Not understanding the concurrency impacts of a workload type"*

---

### Go Contexts: Deadline, Cancellation, Values

**Principle:** A `context.Context` carries a deadline, a cancellation signal, and request-scoped values. Use `context.TODO()` when unsure.

**Do:**
- Always `defer cancel()` after `WithTimeout`/`WithCancel`.
- Use unexported custom types for keys (`type key string; const myCustomKey key = "key"`).
- Select on `<-ctx.Done()` to react to cancellation.

**Don't:**
- Store contexts in structs.
- Use string keys for context values (collisions).

**Code:**
```go
ctx, cancel := context.WithTimeout(context.Background(), 4*time.Second)
defer cancel() // CRITICAL: prevents goroutine leak
return h.pub.Publish(ctx, position)

func handler(ctx context.Context, ch chan Message) error {
    for {
        select {
        case msg := <-ch:
            // process
        case <-ctx.Done():
            return ctx.Err()
        }
    }
}
```
*Ref: 100_Go_Mistakes.md — "#60: Misunderstanding Go contexts"*

---

### Propagating Inappropriate Contexts

**Principle:** Don't propagate the HTTP request context to a long-running async task — the context cancels when the response is written.

**Do:**
- Detach cancellation while preserving values with a custom context wrapper.

**Don't:**
- Pass `r.Context()` to a `go func()` doing async work.

**Code:**
```go
type detach struct{ ctx context.Context }

func (d detach) Deadline() (time.Time, bool) { return time.Time{}, false }
func (d detach) Done() <-chan struct{}      { return nil }
func (d detach) Err() error                 { return nil }
func (d detach) Value(key any) any          { return d.ctx.Value(key) }

// detached but values preserved
err := publish(detach{ctx: r.Context()}, response)
```
*Ref: 100_Go_Mistakes.md — "#61: Propagating an inappropriate context"*

---

### Goroutine Lifecycle Discipline

**Principle:** Every goroutine must have a clear exit. Leaks leak memory + connections + file descriptors.

**Do:**
- Tie goroutine lifetime to a context that cancels.
- Block the parent until resources close (use `defer w.close()`).

**Don't:**
- `go w.watch()` without a termination signal.

**Code:**
```go
func main() {
    w := newWatcher()
    defer w.close() // blocks until resources released
    // run app
}

func newWatcher() watcher {
    w := watcher{}
    go w.watch()
    return w
}
```
*Ref: 100_Go_Mistakes.md — "#62: Starting a goroutine without knowing when to stop it"*

---

### Goroutines and Loop Variables (Go <1.22)

**Principle:** The loop variable is one variable shared by all goroutines; they capture by reference.

**Do:**
- `val := i` (shadow inside the loop).
- Pass as argument: `go func(val int) { ... }(i)`.

**Don't:**
- `for _, i := range s { go func() { fmt.Print(i) }() }`.

**Code:**
```go
// FIX 1: local variable
for _, i := range s {
    val := i
    go func() {
        fmt.Print(val)
    }()
}

// FIX 2: parameter
for _, i := range s {
    go func(val int) {
        fmt.Print(val)
    }(i)
}
```
*Ref: 100_Go_Mistakes.md — "#63: Not being careful with goroutines and loop variables"*

**Go 1.22+:** Per-iteration scoping fixes this at the language level — upgrade if you can.

---

### select is Non-Deterministic

**Principle:** When multiple cases are ready, Go picks one at random. Source order does not win.

**Do:**
- Use unbuffered channels for strict ordering with single producers.
- Use a single channel carrying a tagged struct.
- For multiple producers, drain in an inner `select` with `default`.

**Don't:**
- Rely on case order to imply priority.

**Code:**
```go
for {
    select {
    case v := <-messageCh:
        fmt.Println(v)
    case <-disconnectCh:
        for {
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
*Ref: 100_Go_Mistakes.md — "#64: Expecting deterministic behavior using select and channels"*

---

### Notification Channels: chan struct{}

**Principle:** Use `chan struct{}` (zero-byte) for signals, not `chan bool`.

**Do:**
- `disconnectCh := make(chan struct{})`.
- Close to broadcast (all receivers wake).

**Don't:**
- Use `chan bool` and invent meaning for `true`/`false`.

**Code:**
```go
var s struct{}
fmt.Println(unsafe.Sizeof(s)) // 0
// empty interface would be 8 (32-bit) or 16 bytes (64-bit)
```
*Ref: 100_Go_Mistakes.md — "#65: Not using notification channels"*

---

### nil Channels Disable select Cases

**Principle:** A nil channel blocks forever on send and receive. Set a channel to nil to remove its case from a select.

**Do:**
- Use nil-channel state machine in `select` for graceful multi-channel merge.

**Code:**
```go
func merge(ch1, ch2 <-chan int) <-chan int {
    ch := make(chan int, 1)
    go func() {
        for ch1 != nil || ch2 != nil {
            select {
            case v, open := <-ch1:
                if !open {
                    ch1 = nil
                    break
                }
                ch <- v
            case v, open := <-ch2:
                if !open {
                    ch2 = nil
                    break
                }
                ch <- v
            }
        }
        close(ch)
    }()
    return ch
}
```
*Ref: 100_Go_Mistakes.md — "#66: Not using nil channels"*

---

### Channel Size and Buffering

**Principle:** Default to unbuffered for synchronization; default buffered size = 1 unless you have measured.

**Do:**
- Unbuffered when sender-receiver handshake matters.
- Buffered = worker pool count or rate-limit size.

**Don't:**
- Use magic buffer sizes (`make(chan int, 40)`) without rationale.

**Code:**
```go
// Synchronization guarantee:
ch1 := make(chan int)        // unbuffered — strong sync
ch2 := make(chan int, 0)      // same as above
ch3 := make(chan int, 1)      // buffered, weak sync
```
*Ref: 100_Go_Mistakes.md — "#67: Being puzzled about channel size"*

**LMAX quote:** *"Queues are typically always close to full or close to empty due to the differences in pace between consumers and producers."*

---

### String Formatting Side Effects

**Principle:** `fmt.Sprintf` traversing a context can read mutable values; a `String()` method that takes a lock can deadlock if called from a holder of that lock.

**Do:**
- Restrict mutex scope: validate input first, then lock.
- Don't format a struct via its `String()` while holding its lock.

**Don't:**
- `c.mutex.Lock(); fmt.Errorf("error: %v", c);` if `String()` takes the lock.

**Code:**
```go
// BAD: deadlock potential
func (c *Customer) UpdateAge(age int) error {
    c.mutex.Lock()
    defer c.mutex.Unlock()
    if age < 0 {
        return fmt.Errorf("age should be positive for customer %v", c) // String() tries to RLock
    }
    c.age = age
    return nil
}

// GOOD: validate first, then lock
func (c *Customer) UpdateAge(age int) error {
    if age < 0 {
        return fmt.Errorf("age should be positive for customer id %s", c.id)
    }
    c.mutex.Lock()
    defer c.mutex.Unlock()
    c.age = age
    return nil
}
```
*Ref: 100_Go_Mistakes.md — "#68: Forgetting about possible side effects with string formatting"*

**Real-world example:** etcd's `Watcher.Watch` used `fmt.Sprintf("%v", ctx)` to key a map; the context had mutable pointer values → data race.

---

### append is Not Thread-Safe

**Principle:** Multiple goroutines `append`ing to the same slice may race when there's spare capacity.

**Do:**
- Each goroutine appends to its own slice; merge afterward.
- Or use a mutex.

**Don't:**
- `append(sharedSlice, v)` from many goroutines.

**Code:**
```go
// FULL slice (len==cap) -> append allocates, race-free
s := make([]int, 1)
go func() { s1 := append(s, 1); _ = s1 }()
go func() { s2 := append(s, 1); _ = s2 }() // safe

// WITH spare cap (len<cap) -> data race
s := make([]int, 0, 1)
go func() {
    sCopy := make([]int, len(s), cap(s))
    copy(sCopy, s)
    s1 := append(sCopy, 1)
    _ = s1
}()
```
*Ref: 100_Go_Mistakes.md — "#69: Creating data races with append"*

**Map rule:** Any concurrent map access with at least one write is a data race (race detector flags all map access, even different keys).

---

### Mutex Boundaries with Slices and Maps

**Principle:** `balances := c.balances` copies the slice/map **header**, not the data — both point to the same backing array/buckets.

**Do:**
- Either expand the critical section to cover iteration.
- Or deep-copy (iterate and copy each entry) inside the lock.

**Don't:**
- Assume assignment creates isolation.

**Code:**
```go
// BAD — header copy
func (c *Cache) AverageBalance() float64 {
    c.mu.RLock()
    balances := c.balances
    c.mu.RUnlock()                  // releases lock too early
    sum := 0.
    for _, balance := range balances { // iterating over shared data!
        sum += balance
    }
    return sum / float64(len(balances))
}

// GOOD — full lock
func (c *Cache) AverageBalance() float64 {
    c.mu.RLock()
    defer c.mu.RUnlock()
    sum := 0.
    for _, balance := range c.balances {
        sum += balance
    }
    return sum / float64(len(c.balances))
}

// GOOD — deep copy + short lock
func (c *Cache) AverageBalance() float64 {
    c.mu.RLock()
    m := make(map[string]float64, len(c.balances))
    for k, v := range c.balances {
        m[k] = v
    }
    c.mu.RUnlock()
    sum := 0.
    for _, balance := range m {
        sum += balance
    }
    return sum / float64(len(m))
}
```
*Ref: 100_Go_Mistakes.md — "#70: Using mutexes inaccurately with slices and maps"*

---

### sync.WaitGroup Discipline

**Principle:** `Add` must happen in the parent goroutine BEFORE starting the worker, not inside the worker.

**Do:**
- `wg.Add(1)` in the loop body, BEFORE `go func()`.

**Don't:**
- `wg.Add(1)` inside the goroutine.

**Code:**
```go
// BAD — race between wg.Wait() and wg.Add(1)
wg := sync.WaitGroup{}
for i := 0; i < 3; i++ {
    go func() {
        wg.Add(1)
        atomic.AddUint64(&v, 1)
        wg.Done()
    }()
}
wg.Wait() // may see counter=0 and return early!

// GOOD
wg := sync.WaitGroup{}
wg.Add(3)
for i := 0; i < 3; i++ {
    go func() {
        atomic.AddUint64(&v, 1)
        wg.Done()
    }()
}
wg.Wait()
```
*Ref: 100_Go_Mistakes.md — "#71: Misusing sync.WaitGroup"*

**Counter cannot go negative** — panics.

---

### sync.Cond for Broadcast

**Principle:** `sync.Cond` is the only way to repeatedly broadcast a signal to multiple goroutines. `chan struct{}` can be closed only once.

**Do:**
- Use `Broadcast()` to wake all waiters when the state changes.

**Don't:**
- Try to broadcast through a regular channel.

**Code:**
```go
type Donation struct {
    cond    *sync.Cond
    balance int
}

donation := &Donation{cond: sync.NewCond(&sync.Mutex{})}

f := func(goal int) {
    donation.cond.L.Lock()
    for donation.balance < goal {
        donation.cond.Wait() // unlocks, waits, re-locks
    }
    fmt.Printf("%d$ goal reached\n", donation.balance)
    donation.cond.L.Unlock()
}
go f(10)
go f(15)

for {
    time.Sleep(time.Second)
    donation.cond.L.Lock()
    donation.balance++
    donation.cond.L.Unlock()
    donation.cond.Broadcast()
}
```
*Ref: 100_Go_Mistakes.md — "#72: Forgetting about sync.Cond"*

**`Signal()`** wakes one waiter; `Broadcast()` wakes all. `Broadcast()` with no waiters is a no-op.

---

### errgroup for Goroutine Groups

**Principle:** For groups of goroutines that all need error collection AND context cancellation, use `golang.org/x/sync/errgroup` instead of hand-rolling `sync.WaitGroup` + error plumbing.

**Do:**
- `errgroup.WithContext(parent)` → `g.Go(func() error { ... })` → `g.Wait()`.

**Don't:**
- Hand-roll a shared error slice with a mutex.

**Code:**
```go
import "golang.org/x/sync/errgroup"

func handler(ctx context.Context, circles []Circle) ([]Result, error) {
    results := make([]Result, len(circles))
    g, ctx := errgroup.WithContext(ctx)
    for i, circle := range circles {
        i := i
        circle := circle
        g.Go(func() error {
            result, err := foo(ctx, circle)
            if err != nil {
                return err
            }
            results[i] = result
            return nil
        })
    }
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}
```
*Ref: 100_Go_Mistakes.md — "#73: Not using errgroup"*

**Benefit:** When one goroutine errors, the shared context cancels → the others can react via `<-ctx.Done()`.

---

### Never Copy a sync Type

**Principle:** `sync.Mutex`, `sync.RWMutex`, `sync.WaitGroup`, `sync.Cond`, `sync.Map`, `sync.Once`, `sync.Pool` must never be copied after first use.

**Do:**
- Use pointer receivers when a struct contains a sync type.
- Use pointer fields for the mutex itself.

**Don't:**
- Value receivers that copy the struct containing the mutex.

**Code:**
```go
// BAD — Increments copy the struct, copying the mutex
func (c Counter) Increment(name string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.counters[name]++
}

// GOOD — pointer receiver
func (c *Counter) Increment(name string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.counters[name]++
}
```
*Ref: 100_Go_Mistakes.md — "#74: Copying a sync type"*

**Detect:** `go vet` flags this: `Increment passes lock by value: Counter contains sync.Mutex`

---

### time.Duration Units

**Principle:** `time.Duration` is nanoseconds. `time.NewTicker(1000)` ticks every microsecond.

**Do:**
- `time.NewTicker(1000 * time.Millisecond)` or `time.NewTicker(time.Second)`.

**Don't:**
- Pass raw integers to time functions.

**Code:**
```go
ticker := time.NewTicker(1000) // 1000 ns = 1 µs, NOT 1 second
```
*Ref: 100_Go_Mistakes.md — "#75: Providing a wrong time duration"*

---

### time.After in Loops Leaks

**Principle:** `time.After` allocates a timer that's freed only when it fires. In a hot loop, this leaks ~200B/timer (Go 1.15).

**Do:**
- `time.NewTimer(d)` + `timer.Reset(d)`.

**Don't:**
- `time.After` inside `for` loops or HTTP handlers.

**Code:**
```go
func consumer(ch <-chan Event) {
    timerDuration := 1 * time.Hour
    timer := time.NewTimer(timerDuration)
    for {
        timer.Reset(timerDuration)
        select {
        case event := <-ch:
            handle(event)
        case <-timer.C:
            log.Println("warning: no messages received")
        }
    }
}
```
*Ref: 100_Go_Mistakes.md — "#76: time.After and memory leaks"*

---

### JSON Pitfalls: Embedding, Monotonic Clock, map[string]any

**Principle:**
- Embedded `time.Time` implements `json.Marshaler` → marshals only the time, dropping other fields.
- `time.Time` carries wall + monotonic clocks; JSON drops monotonic → `==` after marshal/unmarshal is `false`.
- `map[string]any` decodes ALL numbers as `float64`.

**Do:**
- Don't embed `time.Time`; name the field.
- Use `time.Time.Equal()` for semantic comparison; `t.Truncate(0)` to strip monotonic.
- Type-assert `float64` from `map[string]any`.

**Don't:**
- `Event{ID int; time.Time}`.
- Compare `event1 == event2` after JSON round-trip.

**Code:**
```go
type Event struct {
    ID   int
    Time time.Time
}

// BAD: time.Time implements json.Marshaler, promoted by embedding
event := Event{ID: 1234, Time: time.Now()}
b, _ := json.Marshal(event) // produces only the time string!

// FIX 1: name the field
type Event struct {
    ID   int
    Time time.Time
}

// FIX 2: implement MarshalJSON explicitly
func (e Event) MarshalJSON() ([]byte, error) {
    return json.Marshal(struct {
        ID   int
        Time time.Time
    }{ID: e.ID, Time: e.Time})
}
```
*Ref: 100_Go_Mistakes.md — "#77: Common JSON-handling mistakes"*

---

### SQL Pitfalls

**Principle:**
- `sql.Open` is lazy — doesn't connect. Use `db.Ping()`.
- Configure pool: `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`.
- Use prepared statements for repeated/untrusted queries.
- Use `*string` or `sql.Null*` for nullable columns.
- Always check `rows.Err()` after `for rows.Next()`.

**Do:**
- `db.PingContext(ctx)` after `sql.Open`.
- `defer rows.Close()` + check `rows.Err()`.

**Don't:**
- Trust `sql.Open` to fail on bad config.
- Compare nullable columns into non-pointer strings.

**Code:**
```go
db, err := sql.Open("mysql", dsn)
if err != nil {
    return err
}
if err := db.Ping(); err != nil {
    return err
}

// Nullable column handling
var department sql.NullString
var age int
for rows.Next() {
    err := rows.Scan(&department, &age)
    if err != nil {
        return err
    }
}
if err := rows.Err(); err != nil { // CRITICAL
    return err
}
```
*Ref: 100_Go_Mistakes.md — "#78: Common SQL mistakes"*

---

### Closing Transient Resources

**Principle:** Anything implementing `io.Closer` (HTTP body, sql.Rows, os.File) must be closed. For writable files, the close error may report write failures.

**Do:**
- `defer` close with error logging.
- Read response body before closing (to enable keep-alive).

**Don't:**
- Forget `resp.Body.Close()`.
- Use `if resp != nil { defer resp.Body.Close() }` — per docs, "On error, any Response can be ignored."

**Code:**
```go
resp, err := http.Get(url)
if err != nil {
    return err
}
defer func() {
    err := resp.Body.Close()
    if err != nil {
        log.Printf("failed to close response: %v", err)
    }
}()
// Read body fully for keep-alive
_, _ = io.Copy(io.Discard, resp.Body)

// For writable files, capture close error
func writeToFile(filename string, content []byte) (err error) {
    defer func() {
        closeErr := f.Close()
        if err == nil {
            err = closeErr
        }
    }()
    _, err = f.Write(content)
    return
}
```
*Ref: 100_Go_Mistakes.md — "#79: Not closing transient resources"*

---

### HTTP Handler Return Statements

**Principle:** `http.Error` does NOT return — execution continues. Forgetting `return` leads to double responses and warnings.

**Do:**
- `return` after every error response.

**Don't:**
- Forget the trailing `return`.

**Code:**
```go
func handler(w http.ResponseWriter, req *http.Request) {
    err := foo(req)
    if err != nil {
        http.Error(w, "foo", http.StatusInternalServerError)
        return // CRITICAL
    }
    // ...
}
```
*Ref: 100_Go_Mistakes.md — "#80: Forgetting the return statement after replying to an HTTP request"*

**Symptom of the bug:** `http: superfluous response.WriteHeader call from main.handler`

---

### HTTP Client/Server Timeouts

**Principle:** The default `http.Client` and `http.Server` have NO timeouts. Production needs them.

**Do:**
- Configure `Timeout`, `DialContext`, `TLSHandshakeTimeout`, `ResponseHeaderTimeout` on the client.
- Configure `ReadHeaderTimeout`, `ReadTimeout`, `IdleTimeout` on the server.
- Use `http.TimeoutHandler` for handler-level timeouts.

**Don't:**
- Use `http.Get` / `http.DefaultClient` in production.

**Code:**
```go
// CLIENT
client := &http.Client{
    Timeout: 5 * time.Second,
    Transport: &http.Transport{
        DialContext: (&net.Dialer{
            Timeout: time.Second,
        }).DialContext,
        TLSHandshakeTimeout:   time.Second,
        ResponseHeaderTimeout: time.Second,
        MaxIdleConns:          100,
        MaxIdleConnsPerHost:   100, // default is 2 — bump for high-fanout
    },
}

// SERVER
s := &http.Server{
    Addr:              ":8080",
    ReadHeaderTimeout: 500 * time.Millisecond,
    ReadTimeout:       500 * time.Millisecond,
    IdleTimeout:       time.Second,
    Handler:           http.TimeoutHandler(handler, time.Second, "timeout!"),
}
```
*Ref: 100_Go_Mistakes.md — "#81: Using the default HTTP client and server"*

**Server steps:** ① wait for request, ② TLS, ③ read headers, ④ read body, ⑤ write response.

---

### Categorize Tests

**Principle:** Don't run integration tests in CI unit phase. Use build tags, env vars, or `testing.Short()`.

**Do:**
- `//go:build integration` for integration tests; use `!integration` for unit-only files.
- Use `t.Skip()` with env-var gate for test skipping visibility.
- Use `testing.Short()` to skip long tests.

**Don't:**
- Mix slow integration tests into the default `go test ./...`.

**Code:**
```go
//go:build integration
package db

func TestInsert(t *testing.T) {
    // ...
}

// env var gate
func TestInsert(t *testing.T) {
    if os.Getenv("INTEGRATION") != "true" {
        t.Skip("skipping integration test")
    }
    // ...
}

// short mode
func TestLongRunning(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping long-running test")
    }
    // ...
}
```
*Ref: 100_Go_Mistakes.md — "#82: Not categorizing tests"*

---

### Always Run `-race`

**Principle:** Race conditions are the hardest bugs. The race detector has 5–10× memory and 2–20× time overhead — use it in tests, not prod.

**Do:**
- `go test -race ./...` in CI.
- Wrap race-prone tests in a 100-iteration loop.

**Don't:**
- Trust test results without `-race`.

**Code:**
```go
func TestDataRace(t *testing.T) {
    for i := 0; i < 100; i++ { // amplify chance of catching races
        // Actual logic
    }
}
```
*Ref: 100_Go_Mistakes.md — "#83: Not enabling the -race flag"*

**False positives:** Never. False negatives: possible (race detector is sample-based).

---

### Test Execution Modes

**Principle:** Use `t.Parallel()` for parallel tests (limited by `-parallel N`); use `-shuffle=on` to detect order dependencies.

**Do:**
- Mark safe tests with `t.Parallel()`.
- Run `go test -shuffle=on` in CI.
- Use the seed printed by `-v` to reproduce failures.

**Don't:**
- Have tests that depend on shared global state without synchronization.

**Code:**
```bash
$ go test -shuffle=on -v .
-test.shuffle 1636399552801504000
=== RUN TestBar
--- PASS: TestBar (0.00s)
=== RUN TestFoo
--- PASS: TestFoo (0.00s)
```
*Ref: 100_Go_Mistakes.md — "#84: Not using test execution modes"*

**Default `-parallel`** = `GOMAXPROCS`.

---

### Table-Driven Tests

**Principle:** Replace N near-identical test functions with one loop over a slice/map of cases.

**Do:**
- Use a `map[string]struct{ input, expected string }{...}` or slice.
- Run with `t.Run(name, func(t *testing.T) { ... })`.
- Shadow loop variable for `t.Parallel()`.

**Don't:**
- Write `TestX_CaseA`, `TestX_CaseB`, ... when structure is identical.

**Code:**
```go
func TestRemoveNewLineSuffix(t *testing.T) {
    tests := map[string]struct {
        input    string
        expected string
    }{
        `empty`:               {input: "", expected: ""},
        `ending with \r\n`:    {input: "a\r\n", expected: "a"},
        `ending with \n`:      {input: "a\n", expected: "a"},
        `ending with multiple \n`: {input: "a\n\n\n", expected: "a"},
        `ending without newline`: {input: "a", expected: "a"},
    }
    for name, tt := range tests {
        tt := tt // shadow for t.Parallel()
        t.Run(name, func(t *testing.T) {
            t.Parallel()
            got := removeNewLineSuffixes(tt.input)
            if got != tt.expected {
                t.Errorf("got: %s, expected: %s", got, tt.expected)
            }
        })
    }
}
```
*Ref: 100_Go_Mistakes.md — "#85: Not using table-driven tests"*

**Subtest selection:** `go test -run=TestRemoveNewLineSuffix/ending_with_\\\n`

---

### Flaky Tests: Sleep vs Sync vs Retry

**Principle:** `time.Sleep` in tests is a smell. Use channels/sync or retry-with-backoff.

**Do:**
- Use channels to synchronize producer and consumer goroutines.
- Use `testify.Eventually` or a retry helper for unavoidable timing.

**Don't:**
- Sleep for an arbitrary duration.

**Code:**
```go
// BAD
time.Sleep(10 * time.Millisecond)
published := mock.Get()

// GOOD: retry-with-backoff
func assert(t *testing.T, assertion func() bool,
    maxRetry int, waitTime time.Duration) {
    for i := 0; i < maxRetry; i++ {
        if assertion() {
            return
        }
        time.Sleep(waitTime)
    }
    t.Fail()
}

// BEST: synchronization via channel
type publisherMock struct {
    ch chan []Foo
}
func (p *publisherMock) Publish(got []Foo) { p.ch <- got }

if v := len(<-mock.ch); v != 2 {
    t.Fatalf("expected 2, got %d", v)
}
```
*Ref: 100_Go_Mistakes.md — "#86: Sleeping in unit tests"*

---

### Testing Time-Dependent Code

**Principle:** Don't call `time.Now()` deep in logic. Inject a `now func() time.Time` field or take the time as a parameter.

**Do:**
- `now now` field on the struct; inject in tests.
- Or `func TrimOlderThan(t time.Time)` taking the cutoff.

**Don't:**
- `time.Now()` deep in untestable logic.

**Code:**
```go
type now func() time.Time
type Cache struct {
    mu     sync.RWMutex
    events []Event
    now    now
}

func NewCache() *Cache {
    return &Cache{
        events: make([]Event, 0),
        now:    time.Now,
    }
}

// Test
cache := &Cache{now: func() time.Time {
    return parseTime(t, "2020-01-01T12:00:00.06Z")
}}
```
*Ref: 100_Go_Mistakes.md — "#87: Not dealing with the time API efficiently"*

**Avoid** global `var now = time.Now` — kills test parallelism.

---

### httptest and iotest

**Principle:** Use `httptest.NewRecorder` for handler tests, `httptest.NewServer` for client tests, and `iotest.*` to inject read errors.

**Do:**
- Use `httptest.NewRecorder()` + `httptest.NewRequest()` for handlers.
- Use `iotest.ErrReader`, `iotest.TimeoutReader` to test error paths.

**Don't:**
- Spin up real Docker containers for unit tests.

**Code:**
```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "http://localhost",
        strings.NewReader("foo"))
    w := httptest.NewRecorder()
    Handler(w, req)
    if got := w.Result().Header.Get("X-API-VERSION"); got != "1.0" {
        t.Errorf("api version: expected 1.0, got %s", got)
    }
}

// iotest for resilience
err := foo(iotest.TimeoutReader(strings.NewReader(randomString(1024))))
```
*Ref: 100_Go_Mistakes.md — "#88: Not using testing utility packages"*

---

### Benchmark Accuracy

**Principle:** Benchmarking is hard. Four common traps:
1. Not resetting/pausing the timer around setup.
2. Micro-benchmark volatility (use `benchstat`).
3. Compiler inlining killing the function under test.
4. Observer effect (reused data in cache).

**Do:**
- `b.ResetTimer()` after one-time setup.
- `b.StopTimer()` / `b.StartTimer()` around per-iteration setup.
- Assign result to local then global: `v = popcnt(); global = v`.
- Use `-count=10` + `benchstat` for stability.
- Re-create large data structures per iteration.

**Don't:**
- Skip `ResetTimer` when setup is heavy.
- Trust a single benchmark run.

**Code:**
```go
func BenchmarkPopcnt2(b *testing.B) {
    var v uint64
    for i := 0; i < b.N; i++ {
        v = popcnt(uint64(i)) // assign to local, prevents inlining trick
    }
    global = v
}

// benchmark with observer-effect fix
func BenchmarkCalculateSum512(b *testing.B) {
    var sum int64
    for i := 0; i < b.N; i++ {
        b.StopTimer()
        s := createMatrix512(rows)
        b.StartTimer()
        sum = calculateSum512(s)
    }
    res = sum
}
```
*Ref: 100_Go_Mistakes.md — "#89: Writing inaccurate benchmarks"*

---

### Advanced Testing Features

**Principle:**
- `go test -coverprofile=coverage.out` + `go tool cover -html=...`.
- Black-box tests in `package_test` to focus on behavior.
- Pass `*testing.T` to helpers so they call `t.Fatal`.
- `t.Cleanup(func() { ... })` registers teardown.
- `TestMain(m *testing.M)` for package-level setup/teardown.

**Do:**
- Use black-box test packages for behavioral tests.
- Use `t.Cleanup` over manual `defer` ordering.

**Don't:**
- Chase 100% coverage; think about what tests COVER.

**Code:**
```go
// Black-box test in package counter_test
package counter_test

import (
    "testing"
    "myapp/counter"
)

func TestCount(t *testing.T) {
    if counter.Inc() != 1 {
        t.Errorf("expected 1")
    }
}

// Test helper takes *testing.T
func createCustomer(t *testing.T, someArg string) Customer {
    // Create customer
    if err != nil {
        t.Fatal(err)
    }
    return customer
}

// Package-level setup
func TestMain(m *testing.M) {
    setupMySQL()
    code := m.Run()
    teardownMySQL()
    os.Exit(code)
}

// Per-test cleanup
t.Cleanup(func() {
    _ = db.Close()
})
```
*Ref: 100_Go_Mistakes.md — "#90: Not exploring all the Go testing features"*

---

### CPU Caches, Cache Lines, and Mechanical Sympathy

**Principle:** L1 ≈ 1 ns; main memory ≈ 50–100 ns slower. Data layout matters.

**Do:**
- Use struct-of-arrays for hot iteration on one field.
- Pad to cache-line boundaries for hot concurrent data (false sharing).

**Don't:**
- Use linked lists when arrays/slices will do (non-unit stride).
- Pack fields randomly (cache line waste).

**Code:**
```go
// AOS (array of structs) — cache-line waste when iterating on .a
type Foo struct {
    a int64
    b int64
}
func sumFoo(foos []Foo) int64 {
    var total int64
    for i := 0; i < len(foos); i++ {
        total += foos[i].a
    }
    return total
}

// SOA (struct of arrays) — better spatial locality
type Bar struct {
    a []int64
    b []int64
}
func sumBar(bar Bar) int64 {
    var total int64
    for i := 0; i < len(bar.a); i++ {
        total += bar.a[i]
    }
    return total
}
// sumBar is ~20% faster on author's machine — fewer cache lines fetched.
```
*Ref: 100_Go_Mistakes.md — "#91: Not understanding CPU caches"*

**Strides:**
- Unit stride (slice) — predictable, fastest.
- Constant stride (slice every N) — predictable, slower.
- Non-unit stride (linked list) — CPU can't predict.

**Critical stride:** with 64-byte lines and 64-set 8-way cache, the critical stride for `[]T` is `64 × 64 = 4096` bytes — about 512 int64s. A `[][512]int64` matrix has poor cache distribution; `[][513]int64` does not.

---

### False Sharing

**Principle:** Two goroutines writing to the SAME cache line (but different variables) cause the line to bounce between cores (MESI protocol).

**Do:**
- Pad concurrent shared structs to cache-line boundaries.

**Don't:**
- Use adjacent fields for two goroutine-local accumulators.

**Code:**
```go
type Result struct {
    sumA int64
    _    [56]byte // padding
    sumB int64
}
// Without padding: ~40% slower.
```
*Ref: 100_Go_Mistakes.md — "#92: Writing concurrent code that leads to false sharing"*

---

### Instruction-Level Parallelism

**Principle:** Modern CPUs (superscalar) execute multiple instructions per cycle when there are no data/control hazards.

**Do:**
- Reduce data dependencies by introducing temporaries.

**Don't:**
- Force a read-modify-write chain on a single variable when you can split it.

**Code:**
```go
// Original — data hazard: check depends on increment
func add(s [2]int64) [2]int64 {
    for i := 0; i < n; i++ {
        s[0]++
        if s[0]%2 == 0 {
            s[1]++
        }
    }
    return s
}

// Optimized — both increments can execute in parallel
func add2(s [2]int64) [2]int64 {
    for i := 0; i < n; i++ {
        v := s[0]
        s[0] = v + 1
        if v%2 != 0 {
            s[1]++
        }
    }
    return s
}
// ~20% faster on author's machine.
```
*Ref: 100_Go_Mistakes.md — "#93: Not taking into account instruction-level parallelism"*

---

### Data Alignment in Structs

**Principle:** Field order affects padding. Sort by size in descending order to minimize padding.

**Do:**
- Order struct fields from largest to smallest.

**Don't:**
- Mix sizes randomly.

**Code:**
```go
// 24 bytes (with padding)
type Bad struct {
    a bool  // 1 byte + 7 padding
    b int64 // 8 bytes
    c int32 // 4 bytes + 4 padding
}

// 16 bytes (optimal)
type Good struct {
    b int64 // 8 bytes
    c int32 // 4 bytes
    a bool  // 1 byte + 3 padding
}

// ~15% faster iteration due to better spatial locality.
```
*Ref: 100_Go_Mistakes.md — "#94: Not being aware of data alignment"*

**Verify:** `unsafe.Sizeof(v)`.

---

### Stack vs Heap, Escape Analysis

**Principle:**
- Stack: LIFO, self-cleaning, goroutine-local — fast.
- Heap: shared, GC-managed — slow.
- *Sharing up* (returning a pointer to a local) escapes to the heap.
- *Sharing down* (passing a parent pointer in) stays on the stack.

**Do:**
- Return values, not pointers, when you can.
- Verify with `go build -gcflags "-m"`.

**Don't:**
- Return pointers "to avoid a copy" without measuring.

**Code:**
```go
func sumValue(x, y int) int {
    z := x + y
    return z // stays on stack
}

func sumPtr(x, y int) *int {
    z := x + y
    return &z // ESCAPES to heap
}

// BenchmarkSumValue-4  992800992  1.261 ns/op  0 B/op  0 allocs/op
// BenchmarkSumPtr-4     82829653   14.84 ns/op  8 B/op  1 allocs/op
```
*Ref: 100_Go_Mistakes.md — "#95: Not understanding stack vs. heap"*

**Escape triggers:** global vars, channel sends, sizes unknown at compile time, `append` overflow.

---

### Reducing Allocations

**Principle:** Three strategies: API design, compiler optimizations, `sync.Pool`.

**Do:**
- Design APIs so the caller provides buffers (sharing-down).
- Use `m[string(bytes)]` lookups — the compiler elides the conversion.
- `sync.Pool` for high-frequency allocations of the same object.

**Don't:**
- Allocate defensively in hot paths.

**Code:**
```go
// compiler optimization — elides []byte→string copy
func (c *cache) get(bytes []byte) (v int, contains bool) {
    v, contains = c.m[string(bytes)]
    return
}

// sync.Pool for reusable buffers
var pool = sync.Pool{
    New: func() any {
        return make([]byte, 1024)
    },
}

func write(w io.Writer) {
    buffer := pool.Get().([]byte)
    buffer = buffer[:0]
    defer pool.Put(buffer)
    getResponse(buffer)
    _, _ = w.Write(buffer)
}
```
*Ref: 100_Go_Mistakes.md — "#96: Not knowing how to reduce allocations"*

---

### Inlining and Fast-Path Optimization

**Principle:** Inlining replaces a call site with the function body. The Go compiler inlines small functions; `defer` and complex control flow can prevent it.

**Do:**
- Extract slow paths into separate functions so the fast path stays inlineable.

**Don't:**
- Write a single function with both fast and slow paths that exceeds the inlining budget.

**Code:**
```go
// Standard library sync.Mutex Lock() refactor
func (m *Mutex) Lock() {
    if atomic.CompareAndSwapInt32(&m.state, 0, mutexLocked) {
        // Fast path — must stay inlineable
        if race.Enabled {
            race.Acquire(unsafe.Pointer(m))
        }
        return
    }
    m.lockSlow() // Slow path extracted
}

func (m *Mutex) lockSlow() {
    // Complex slow-path logic
}
```
*Ref: 100_Go_Mistakes.md — "#97: Not relying on inlining"*

**Check:** `go build -gcflags "-m=2"`

---

### Profiling and Execution Tracing

**Principle:** Use `pprof` and `go tool trace` to find hotspots. Profile types: CPU, heap, goroutine, block, mutex.

**Do:**
- Expose `net/http/pprof` endpoint in production.
- Use CPU profiles for time, heap for memory.
- Use the execution tracer for goroutine scheduling visualization.

**Don't:**
- Enable multiple profiles simultaneously (corrupts data).
- Run profiler with default 10 ms interruption in latency-sensitive paths without benchmarking the impact.

**Code:**
```go
import (
    "net/http"
    _ "net/http/pprof" // blank import exposes /debug/pprof
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {})
    log.Fatal(http.ListenAndServe(":80", nil))
}

// CPU profile
$ go test -bench=. -cpuprofile cpu.out
$ go tool pprof -http=:8080 cpu.out

// Heap diff for leak detection
$ curl http://host/debug/pprof/heap?gc=1 -o h1.pprof
$ # wait
$ curl http://host/debug/pprof/heap?gc=1 -o h2.pprof
$ go tool pprof -http=:8080 -diff_base h2.pprof h1.pprof

// Execution trace
$ go test -bench=. -trace=trace.out
$ go tool trace trace.out
```
*Ref: 100_Go_Mistakes.md — "#98: Not using Go diagnostics tooling"*

---

### Garbage Collector Tuning

**Principle:** Concurrent tri-color mark-and-sweep. `GOGC=100` (default) triggers GC when heap doubles. `GOMEMLIMIT` (Go 1.19+) sets a soft memory limit.

**Do:**
- Profile under production load before tuning `GOGC`.
- For bursty workloads, pre-allocate a "minimum" with `mmap` to reduce GC pressure.

**Don't:**
- Set `GOGC=off` for production without thought.
- Assume smaller `GOGC` is always better (more frequent pauses).

**Code:**
```bash
# GC trace
$ GODEBUG=gctrace=1 go test -bench=. -v

# Force memory return to OS
debug.FreeOSMemory()

# Pre-allocate virtual heap floor for burst handling
var min = make([]byte, 1_000_000_000) // 1 GB virtual, lazy physical
```
*Ref: 100_Go_Mistakes.md — "#99: Not understanding how the GC works"*

**GC pacing:** heap doubles at `GOGC=100`; at peak load with frequent allocation, increase `GOGC` to grow heap faster, fewer cycles.

---

### Go in Docker / Kubernetes

**Principle:** Go is NOT CFS-aware — `GOMAXPROCS` defaults to **host** logical CPUs, not container CPU quota. This can cause CPU throttling.

**Do:**
- Use `go.uber.org/automaxprocs` to auto-set `GOMAXPROCS` from cgroup quota.

**Don't:**
- Assume `GOMAXPROCS` matches `resources.limits.cpu`.

**Code:**
```go
import _ "go.uber.org/automaxprocs" // blank import in main.go
// GOMAXPROCS now matches container CPU quota
```
*Ref: 100_Go_Mistakes.md — "#100: Not understanding the impacts of running Go in Docker and Kubernetes"*

**Symptom:** average latency 50ms can spike to 150ms under throttling (3×).

---

## Anti-Patterns & Common Mistakes

- **Variable shadowing (`:=` inside a block):** Outer variable unchanged → *fix:* use `=` or rename.
- **Nested `if`/`else`:** Inverted guard clauses keep happy path left → *fix:* early returns.
- **`init()` for connections:** No error returns, hard to test → *fix:* factory function returning errors.
- **Java-style getters everywhere:** `GetBalance()` → *fix:* `Balance()` (no `Get` for non-bool).
- **Producer-side interfaces:** Forces all callers to one abstraction → *fix:* consumer defines interface.
- **Returning interfaces:** Hides concrete methods, creates import cycles → *fix:* return concrete type.
- **`any` everywhere:** No type info at compile time → *fix:* generics or per-type methods.
- **Generic for single-method interfaces:** Just use the interface → *fix:* `func foo(w io.Writer)`.
- **Embedded `sync.Mutex`:** Leaks `Lock`/`Unlock` → *fix:* named `mu sync.Mutex`.
- **Utility packages (`util`, `common`):** Junk drawers → *fix:* purpose-named packages.
- **Octal literals (`0644`):** Confusing → *fix:* `0o644`.
- **Silent int overflow:** `int32` + 1 wraps → *fix:* explicit bounds checks.
- **Float `==`:** IEEE-754 inexact → *fix:* compare with delta.
- **Slice without capacity:** Repeated `append` doubling → *fix:* `make([]T, n)` or `make([]T, 0, n)`.
- **Returning `[]int{}` from empty case:** Allocates unnecessarily → *fix:* return nil slice.
- **Slice copy with `var dst []int; copy(...)`:** Copies 0 elements → *fix:* `make([]int, len(src))`.
- **Slicing huge slice:** Keeps backing array alive → *fix:* `copy` or `strings.Clone`.
- **Map without size hint:** Constant rehash → *fix:* `make(map[K]V, expectedSize)`.
- **Comparing slices with `==`:** Compile error → *fix:* `reflect.DeepEqual` or custom.
- **Range loop value mutation:** `v` is a copy → *fix:* index or pointer slice.
- **Pointer elements in range:** Single address shared → *fix:* local copy or `&s[i]`.
- **Map iteration order assumption:** Unspecified → *fix:* don't assume; sort separately.
- **`break` in switch inside for:** Only breaks switch → *fix:* label.
- **`defer` in loop:** Accumulates → *fix:* extract to function.
- **`len("é")` == 1:** Wrong — UTF-8 bytes → *fix:* `utf8.RuneCountInString`.
- **`strings.TrimRight(s, "xo")` for suffix:** Wrong → *fix:* `TrimSuffix`.
- **`+=` for string concat in loop:** O(n²) → *fix:* `strings.Builder` + `Grow`.
- **`[]byte`↔`string` round-trip:** Allocates → *fix:* use `bytes` package.
- **`s[:5]` from huge string:** Backing array kept → *fix:* `strings.Clone`.
- **Value receiver on struct with mutex:** Mutex copied → *fix:* pointer receiver.
- **Naked `return` of named param without assignment:** Returns zero → *fix:* explicit assignment.
- **Returning nil pointer as interface:** Non-nil interface → *fix:* explicit `return nil`.
- **Filename parameter:** Untestable, unreusable → *fix:* `io.Reader`.
- **`defer notify(status)`:** Captures zero value → *fix:* pointer or closure.
- **`panic` for expected errors:** Halts program → *fix:* return error.
- **Logging and returning:** Duplicate handling → *fix:* return wrapped error.
- **Ignoring errors silently:** Confusing for readers → *fix:* `_ = fn()` with comment.
- **`defer f.Close()` for writable files:** Loses write errors → *fix:* capture in named return.
- **Goroutines without exit:** Leaks → *fix:* context cancellation + close hook.
- **Goroutine + loop var in Go <1.22:** All see last value → *fix:* `val := i` or pass as param.
- **`select` case order ≠ priority:** Random selection → *fix:* inner `select` with `default`.
- **`chan bool` for signal:** Misleading semantics → *fix:* `chan struct{}`.
- **`time.After` in loop:** Timer leak → *fix:* `time.NewTimer` + `Reset`.
- **Embedded `time.Time` + JSON:** Promotes `MarshalJSON` → *fix:* named field.
- **`map[string]any` for ints:** All become `float64` → *fix:* struct or `json.Number`.
- **`sql.Open` only:** No connection until first use → *fix:* `db.Ping()`.
- **Missing `defer rows.Close()`:** Connection leak → *fix:* always close.
- **`http.Get` default client:** No timeouts → *fix:* custom client with all 4 timeouts.
- **`http.Server{}` default:** No timeouts → *fix:* `ReadHeaderTimeout` + `TimeoutHandler`.
- **`forget return after http.Error`:** Double response → *fix:* add `return`.
- **Tests without `-race`:** Miss races → *fix:* `go test -race ./...` in CI.
- **`time.Sleep` in tests:** Flaky → *fix:* channels or `Eventually`.
- **`time.Now()` in untestable logic:** → *fix:* inject `now func() time.Time`.
- **Benchmark without `ResetTimer`:** Setup inflates time → *fix:* `b.ResetTimer()`.
- **Benchmark where compiler inlines to nothing:** Wrong numbers → *fix:* `v = fn(); global = v`.
- **Linked list for hot iteration:** Non-unit stride → *fix:* slice.
- **Adjacent fields for parallel writers:** False sharing → *fix:* padding.
- **Returning `&local`:** Escape to heap → *fix:* return value when possible.
- **Pointer-receiver function with embedded mutex:** Mutex copied → *fix:* `mu *sync.Mutex`.
- **`GOMAXPROCS` in K8s without `automaxprocs`:** CPU throttling → *fix:* add blank import.

---

## Decision Heuristics / Checklists

- **Channel vs mutex?** Parallel goroutines + shared state → mutex. Concurrent goroutines + coordination/ownership → channel.
- **Channel buffer size?** Default = 1 unless synchronization required (then unbuffered). Size = worker-pool size only when justified.
- **Pointer or value receiver?** Default to pointer. Must be pointer if mutating or contains sync type. Must be value for maps/funcs/channels.
- **Return interface or struct?** Return struct; accept interface.
- **Stack or heap?** Verify with `go build -gcflags "-m"`. `&` returned from function = escapes.
- **Compare with `==` or not?** Slices/maps/funcs → no. `any` types containing these → runtime panic.
- **Test time-dependent code?** Inject `now`; or take time as parameter.
- **Wrap error?** With `%w` to preserve chain for `errors.Is/As`. Use `%v` to break the chain intentionally.
- **Generic or interface?** Generics for type-parameterized data structures. Interfaces for behavior abstractions.
- **Channel `for range` vs explicit check?** Use comma-ok: `v, open := <-ch; if !open { ... }`.
- **`sync.Pool` or `sync.Map`?** Pool for object reuse; Map for concurrent read-mostly maps.
- **Goroutine leak test?** Check `runtime.NumGoroutine()` before/after.
- **Cache-line alignment for shared counters?** Yes, pad to 64 bytes.
- **Struct field order?** Largest first.

---

## Key Takeaways

1. **Readability first.** Optimize for clarity, then correctness, then performance.
2. **Read the runtime.** Understand slices, maps, channels, GC, escape analysis, scheduler.
3. **Test thoroughly.** `-race`, table-driven, `-shuffle`, parallel tests, benchmark with benchstat.
4. **Profile before optimizing.** Measure with pprof/trace; never guess.
5. **Stay idiomatic.** Follow Go conventions: named returns for clarity, functional options for APIs, errors as values.
6. **Context propagates correctly.** Don't leak parent cancellation to long-running async work.
7. **Concurrency is not free.** Benchmark; use thresholds; pool size = GOMAXPROCS for CPU-bound.
8. **Every mistake is a learning opportunity.** Understand WHY something is wrong, not just the rule.

---

## Cross-References

- Related: `Concurrency_in_Go.md`, `Shipping_Go.md`, `Efficient_Go.md`, `Mastering_Go.md`, `Learning_Go.md`, `Functional_Programming_in_Go.md`, `Grokking_Concurrency.md`, `Go_Systems_Programming.md`, `Domain_Driven_Design_with_Golang.md`, `Building_Modern_CLI_Applications_in_Go.md`
- Topic index: `../INDEX.md`