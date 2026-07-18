# Functional Programming in Go
**Author:** Dylan Meeus
**Topic tags:** `#general` `#testing` `#go` `#fp`
**Language focus:** Go-first (Go is multi-paradigm; FP is a tool, not a religion)
**Sources:** `markdown_output/Functional_Programming_in_Go_-_Dylan_Meeus/Functional_Programming_in_Go_-_Dylan_Meeus.md` · `summaries/Functional_Programming_in_Go_-_Dylan_Meeus.md`

## TL;DR
Use Go's first-class functions, generics, and value semantics to push impure effects to the edges: pure core / impure shell, immutability by default, type aliases for self-documenting signatures, monads/Options for absent values, function types as struct fields for testable behavior, fluent pipelines with channels, and benchmarking for performance claims. Reach for FP when it improves readability and testability; back off when it adds friction without payoff.

---

## Best Practices by Topic

### Pure Functions: Push Side Effects to the Edges

**Principle:** Aim for ~90% pure code with ~10% impure code at the boundaries (I/O, randomness, panic). Pure functions are deterministic, referentially transparent, and trivially testable without mocks.

**Do:**
- Make functions depend only on their arguments; return a new value instead of mutating an input.
- Bubble errors up via Go's `(T, error)` return idiom rather than panicking on the happy path.
- Isolate impurity: separate validation from persistence, do not mix them in one function.
- Each function should do one thing; if you can split a function into "validate" + "save" + "log", do it.

**Don't:**
- Don't use `panic` for control flow. Reserve it for "the normal flow can't proceed" (e.g., OOM, programmer error).
- Don't rely on package-level `var` blocks for state a function depends on — that destroys idempotence and testability.
- Don't make a function "do something useful" *and* persist the result — split the work.

**Code:**
```go
// Pure: validate, then construct. Returns a new User; no side effects.
func createUser(username, password string) (User, error) {
    u := User{username, password}
    if !u.validPassword() {
        return User{}, errors.New("invalid password")
    }
    return u, nil
}

// Impure: orchestration layer handles the side effect.
func signup(username, password string) {
    user, err := createUser(username, password)
    if err != nil {
        panic("Could not create account")
    }
    saveUser(user)
}
func saveUser(u User) { userDb.save(u) }
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Demonstrating pure versus impure function calls", "How do we create pure functions?"*

---

### Immutability & Pass-by-Value (Go Uses Value Semantics by Default)

**Principle:** Go is value-oriented. Prefer pass-by-value with returned copies. Pointers cause heap allocation, GC pressure, and concurrency hazards. Immutable structs make concurrent code safer and reasoning easier.

**Do:**
- Accept a struct by value, return a new struct with the change applied: `func setName(p Person, name string) Person { p.name = name; return p }`.
- Use the same pattern as `append` — never mutate; return a new value.
- Treat maps as a known exception: maps always act as pass-by-reference; document this clearly.
- Reuse the result by `buf = buf[:0]` between operations, not by re-allocating.

**Don't:**
- Don't use pointers for the sake of "performance" — benchmarks in the book show pass-by-value immutable code can match or beat pointer-based code because it stays on the stack.
- Don't use `*Person` to mutate a struct from a function; return the new value.
- Don't assume `s = append(s, x)` mutates the caller's slice — it never does.

**Code:**
```go
// Immutable update via pass-by-value return.
func setName(p Person, name string) Person {
    p.name = name
    return p
}

// Slice growth: reassign the returned slice; the original is untouched.
names := []string{"Miranda", "Paula"}
names = append(names, "Yvonne") // [Miranda Paula Yvonne], original untouched
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "What is immutability?", "How to write immutable code in Go"*

---

### Type Aliases: Self-Documenting Signatures and Better Error Messages

**Principle:** Use type aliases on primitives and function signatures to make intent explicit at the type level. They make signatures readable and turn cryptic error messages into domain-named ones.

**Do:**
- Define `type phoneNumber string`, `type age uint`, `type Name string` etc. for domain primitives.
- Define function-type aliases: `type predicate func(int) bool`, `type CipherFunc func(string) string`.
- Use aliases to attach methods to "primitives" (you can't add methods to `uint`, but you can to `type age uint`).
- Prefer type aliases in struct fields and function signatures where the bare primitive would be ambiguous.

**Don't:**
- Don't over-abstract — a one-off alias for an internal helper is noise. Use them when the name adds domain meaning.
- Don't use `any` where a named alias would be clearer.

**Code:**
```go
type (
    ServerOptions func(options) options
    TransportType int
)
const (
    UDP TransportType = iota
    TCP
)

// Error messages now say:
//   "cannot use func(i int, s string) bool as type predicate"
// rather than the raw function signature.
func filter(is []int, p predicate) []int {
    out := []int{}
    for _, i := range is {
        if p(i) { out = append(out, i) }
    }
    return out
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Type aliases for primitives", "Type aliases for functions"*

---

### First-Class Functions: Pass Behavior, Not Behavior-Holders

**Principle:** Functions are values: bind them to variables, store them in struct fields, pass them as arguments, return them. This is the lever for testability, mockability, and composition — no inheritance needed.

**Do:**
- Store function references in struct fields to make implementations swappable at runtime: `type Db struct { AuthorizationFn func() bool }`.
- Use type aliases for the stored function so its contract is named and checkable at compile time.
- Use anonymous functions and closures for short, single-use logic; named functions when reused.
- Bind commonly-used partially-applied functions at package scope: `var isAdmin = isAuthorized(RoleAdmin)`.

**Don't:**
- Don't define a method on a struct when the behavior comes from outside; store a function field instead.
- Don't use closures to share mutable state across goroutines — combine the closure pattern with channels or immutability.

**Code:**
```go
type authorizationFunc func() bool
type Db struct {
    AuthorizationFn authorizationFunc
}
func (d *Db) IsAuthorized() bool {
    return d.AuthorizationFn()
}
func NewDB() *Db {
    return &Db{AuthorizationFn: argsAuthorization}
}

// Tests can inject any function:
todo := Todo{Db: &Db{AuthorizationFn: func() bool { return true }}}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Functions inside structs", "Example 2 – mocking functions for testing"*

---

### Higher-Order Functions & Map Dispatchers

**Principle:** Encapsulate the *iteration*; parameterize the *behavior*. A switch-based dispatcher can be a flat map lookup; a calculator can be `map[string]CalculatorFunc`.

**Do:**
- Replace repeated `switch op { case "add": ... }` with `addTable := map[string]func(a, b int) int`.
- Use anonymous functions inline for terse, single-use behaviors; especially powerful for "add new op" extensibility.
- Store anonymous functions directly in maps: `"<<": func(a, b int) int { return a << b }`.

**Don't:**
- Don't add a new `case` to a long `switch` when a map lookup is more extensible and equally clear.
- Don't expose the map directly if it needs to be safely constructed (use a constructor or a var initializer).

**Code:**
```go
type calcFunc func(a, b int) int
var (
    addTable = map[string]calcFunc{
        "+":  func(a, b int) int { return a + b },
        "-":  func(a, b int) int { return a - b },
        "*":  func(a, b int) int { return a * b },
        "/":  func(a, b int) int { return a / b },
        "<<": func(a, b int) int { return a << b },
    }
)
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example 1 – map dispatcher"*

---

### Closures, Partial Application & Currying

**Principle:** Closures capture surrounding variables; partial application fixes some arguments; currying decomposes an n-ary function into a chain of unary functions. Combine them to expose a clean functional API on top of Go's nominal types.

**Do:**
- Use partial application to factor out defaults: `DogSpawner(breed, gender) returns a unary NameToDogFunc`.
- Use a non-recursive outer function to own state, and an inner function to recurse — the state stays private.
- Use function currying to make a function fit a higher-order signature (e.g., `CurriedFilterNode` returns a `Node[A]`).
- Declare the inner function variable first, then assign, when the function refers to itself: `var inner func(node *node); inner = func(node *node) { ... inner(node.left) ... }`.

**Don't:**
- Don't curry a 2-argument function with no reason — the call site becomes `f(a)(b)` for no readability gain.
- Don't use closures to share *mutable* state across goroutines — Go's value semantics or channels are safer.
- Don't try to do `inner := func(...) { inner(...) }` — Go won't compile it because `inner` isn't defined at the point of the closure's reference.

**Code:**
```go
// Partial application: fix breed and gender, return a unary name-only spawner.
func DogSpawner(breed Breed, gender Gender) NameToDogFunc {
    return func(n Name) Dog {
        return Dog{Breed: breed, Gender: gender, Name: n}
    }
}
var maleHavaneseSpawner = DogSpawner(Havanese, Male)
bucky := maleHavaneseSpawner("bucky")

// Currying: turn a 2-arg function into a unary `Node[A]` for the pipeline.
func CurriedFilterNode[A any](p Predicate[A]) Node[A] {
    return func(in <-chan A) <-chan A {
        out := make(chan A)
        go func() {
            for n := range in { if p(n) { out <- n } }
            close(out)
        }()
        return out
    }
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example: DogSpawner", "Function currying", "Capturing variable context in functions (closures)"*

---

### Map/Filter/Reduce with Generics

**Principle:** Build a tiny, pure, generic toolbox (Filter, Map/MapFunc, FlatMap, All/Any, TakeWhile/DropWhile, Reduce, Sum). Each is ~10 lines, takes a function, never mutates the input. This is the workhorse layer for declarative data pipelines.

**Do:**
- Use `Predicate[A any] = func(A) bool`, `MapFunc[A any] = func(A) A`, `FMap = func(A) B` to standardize signatures.
- Pre-allocate output slices: `output := make([]A, 0, len(input))` or `make([]B, len(input))`.
- Short-circuit on the first match in `Any` (don't `Filter` then `len > 0`).
- Combine Filter + FMap + Sum: `Sum(FMap(Filter(es, byCode), minutes))`.

**Don't:**
- Don't write collection-specific functions (`onlyInts`, `onlyStrings`) — generics handle all of them.
- Don't loop-and-append without a known upper bound when memory pressure matters; pre-allocate.
- Don't use `All` if you can short-circuit — check for the first non-match.

**Code:**
```go
type Predicate[A any] func(A) bool
type MapFunc[A any] func(A) A

func Filter[A any](input []A, pred Predicate[A]) []A {
    output := []A{}
    for _, element := range input {
        if pred(element) {
            output = append(output, element)
        }
    }
    return output
}

func Any[A any](input []A, pred Predicate[A]) bool {
    for _, element := range input {
        if pred(element) { return true } // short-circuit
    }
    return false
}

// Airports: total hours of weather delays for Seattle.
SEA := Filter(entries, func(e Entry) bool { return e.Airport.Code == "SEA" })
weatherDelayHours := FMap(SEA, func(e Entry) int { return e.Statistics.MinutesDelayed.Weather / 60 })
total := Sum(weatherDelayHours)
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Three Common Categories of Functions", "Example – working with airport data"*

---

### The Maybe/Option Monad: No More Nil Checks

**Principle:** Encode "value may be absent" in the type system. A `Maybe[A]` (or `Option[A]`) makes absence explicit; you can never dereference nil because there's nothing to dereference.

**Do:**
- Define a `Maybe[A]` interface with `Get() A` and `GetOrElse(def A) A` (or equivalent).
- Provide `Just(a)` and `Nothing[A]()` constructors.
- Implement `fmap` for `Maybe[A]` to compose transformations safely.
- Use `GetOrElse(default)` instead of `if x != nil { x.foo() }`.

**Don't:**
- Don't return `(T, error)` for the "not found" case — use `Maybe[T]`.
- Don't reach for `*T` pointers when absence is part of the domain (e.g., "no user with this id").
- Don't panic on `Get()` from `Nothing` — that defeats the purpose of optional types.

**Code:**
```go
type Maybe[A any] interface {
    Get() A
    GetOrElse(def A) A
}
type JustMaybe[A any] struct{ value A }
func (j JustMaybe[A]) Get() A            { return j.value }
func (j JustMaybe[A]) GetOrElse(def A) A { return j.value }

type NothingMaybe[A any] struct{}
func Nothing[A any]() Maybe[A]              { return NothingMaybe[A]{} }
func (n NothingMaybe[A]) GetOrElse(def A) A { return def }

func getFromMap(m map[string]int, key string) Maybe[int] {
    if v, ok := m[key]; ok { return Just[int](v) }
    return Nothing[int]()
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "From functor to monad"*

---

### Immutability Actually Can Be Faster: Benchmark It

**Principle:** "Pointers are faster" is folklore. In Go, the compiler's escape analysis often keeps immutable value-based code on the stack, avoiding GC pressure. Benchmark before assuming the "efficient" code is the mutable one.

**Do:**
- Write benchmark pairs: `BenchmarkImmutablePerson` vs `BenchmarkMutablePerson` on identical work.
- Use `//go:noinline` and `go build -gcflags '-m -l'` to inspect escape analysis.
- Use `b.ReportAllocs()` to expose allocation differences.
- Be willing to update your mental model when the data contradicts it.

**Don't:**
- Don't use pointers "for performance" without measuring — you may be paying for GC, not saving copies.
- Don't use a global variable to track state in a recursive function (a benchmark-validated antipattern).

**Code:**
```go
func BenchmarkImmutablePerson(b *testing.B) {
    for n := 0; n < b.N; n++ { immutableCreatePerson() }
}
func BenchmarkMutablePerson(b *testing.B) {
    for n := 0; n < b.N; n++ { mutableCreatePerson() }
}
// Result on the author's machine:
// BenchmarkImmutablePerson  0.3758 ns/op
// BenchmarkMutablePerson      0.3775 ns/op
// Immutable wins (or ties) because of stack vs heap allocation.
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Benchmarking functions", "Understanding stacks, heaps, and garbage collection"*

---

### Recursion in Go: When to Use It, and the No-Tail-Call Caveat

**Principle:** Recursion is preferred in functional languages because it enforces immutability, but Go has no tail-call optimization and limited stack (~1 GB on 64-bit). Use recursion when the problem is naturally recursive (trees, graphs) — fall back to iteration when speed or depth matters.

**Do:**
- Use recursion for naturally tree-shaped data: a 2-line `sumRecursive` is clearer than a queue-based iterative version.
- Encapsulate recursive state in a non-recursive outer function with an inner `func` variable (avoids leaking implementation details to callers).
- Always define the base case: a `nil` check or terminal condition.
- Use `debug.SetMaxStack` only as a last resort — the 1 GB 64-bit limit is enough for most apps.

**Don't:**
- Don't recurse when the input can be huge (e.g., a list of 10 million items) — iterative is faster and avoids stack overflow.
- Don't write `inner := func(node *node) { inner(node.left) }` — declare `var inner func(...)` first, then assign.
- Don't try to rely on tail-call optimization — Go does not perform it (as of Go 1.18+).
- Don't use a global variable to track state inside the recursion — use the outer-closure pattern instead.

**Code:**
```go
// Recursive sum over a binary tree.
func sumRecursive(node *node) int {
    if node == nil { return 0 }
    return node.value + sumRecursive(node.left) + sumRecursive(node.right)
}

// Outer + inner pattern: state stays private to Max.
func Max(root *node) int {
    currentMax := math.MinInt
    var inner func(node *node)
    inner = func(node *node) {
        if node == nil { return }
        if node.value > currentMax { currentMax = node.value }
        inner(node.left)
        inner(node.right)
    }
    inner(root)
    return currentMax
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Iterating over trees", "Recursion and functions as first-class citizens", "Limits of recursive functions"*

---

### Fluent Composition: Dot Notation via Type Aliases

**Principle:** Dot-notation chaining (`input.Map(...).Filter(...).Sum()`) reads better than nested calls for the majority of Go developers. Wrap generic functions as methods on a type alias to enable it.

**Do:**
- Define `type ints []int`, then attach `Map`, `Filter`, `Sum` as methods on `ints` that call the underlying generic functions.
- Use the fluent style for "obvious" data pipelines where the order is intuitive.
- Remember it's syntactic sugar — choose dot-notation when the chain is short and obvious.

**Don't:**
- Don't fluent-chain when you need to share or branch intermediate results.
- Don't fluent-chain when each step needs a different batch size or concurrency — separate calls are clearer.
- Don't force fluent style on code that genuinely benefits from intermediate variables.

**Code:**
```go
type ints []int
func (i ints) Map(f func(i int) int) ints   { return Map(i, f) }
func (i ints) Filter(f func(i int) bool) ints { return Filter(i, f) }
func (i ints) Sum() int                      { return Sum(i) }

func chaining() int {
    input := ints([]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
    return input.Map(func(i int) int { return i * 2 }).
        Filter(func(i int) bool { return i >= 10 }).
        Sum()
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Dot notation to chain functions on slices"*

---

### Functional Design Patterns: Strategy and Decorator

**Principle:** Many OO design patterns dissolve into functions in the functional paradigm. The strategy pattern is "function field"; the decorator pattern is "function composition". Don't reach for an interface when a function type will do.

**Do:**
- Replace `interface { Cipher(string) string; Decipher(string) string }` with `type CipherFunc func(string) string`.
- For decorators, return a new function of the same type that wraps the old one: `LogCipher(c CipherFunc) CipherFunc { return func(in string) string { log.Print(...); return c(in) } }`.
- For state, capture it in a closure: `CaesarCipher := func(in string) string { ...rotation captured here... }`.
- Use `var AtbashDecipher = AtbashCipher` when a function *is* its own inverse — leverage the fact that functions are data.

**Don't:**
- Don't define an interface with one method when a function type alias will do.
- Don't use struct embedding to share state between cipher variants when a closure parameter captures it more cleanly.
- Don't decorate a function with a giant method-on-struct when a higher-order function does it in 4 lines.

**Code:**
```go
type (
    CipherFunc   func(string) string
    DecipherFunc func(string) string
)
type CipherService struct {
    CipherFn   CipherFunc
    DecipherFn DecipherFunc
}
func (c CipherService) Cipher(in string) string   { return c.CipherFn(in) }
func (c CipherService) Decipher(in string) string { return c.DecipherFn(in) }

// Decorator: add logging without touching the original cipher.
func LogCipher(cipher CipherFunc) CipherFunc {
    return func(input string) string {
        log.Printf("ciphering: %s\n", input)
        return cipher(input)
    }
}

// Atbash is its own inverse.
var AtbashDecipher = AtbashCipher
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "The strategy pattern", "The decorator pattern"*

---

### Pipeline Pattern with Channels + Curried Nodes

**Principle:** Model a data pipeline as `Generator → FilterNode → MapNode → Collector`, with each node reading from `<-chan A` and writing to `<-chan A`. Currying makes the nodes interchangeable in `ChainPipes`.

**Do:**
- Define `type Node[A any] func(<-chan A) <-chan A` and `type GeneratorNode[A any] func() <-chan A`.
- Have each node start a goroutine on entry, range over the input channel, and `close(out)` when done.
- Use `ChainPipes(generator, nodes...)` to compose them — don't manually wire channels.
- Always range the input channel and `close` the output — leaks are the most common pipeline bug.

**Don't:**
- Don't have a node *return* a value — return the output channel. The output is a stream, not a scalar.
- Don't reuse channels across calls; let the closure own them.
- Don't use CPS for everyday control flow; reserve it for compiler/interpreter work or complex async.

**Code:**
```go
type (
    Node[A any]         func(<-chan A) <-chan A
    GeneratorNode[A any] func() <-chan A
)
func ChainPipes[A any](gn GeneratorNode[A], nodes ...Node[A]) []A {
    in := gn()
    for _, node := range nodes { in = node(in) }
    return Collector(in)
}
func FilterNode[A any](in <-chan A, p Predicate[A]) <-chan A {
    out := make(chan A)
    go func() {
        for n := range in { if p(n) { out <- n } }
        close(out)
    }()
    return out
}
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "The pipeline pattern"*

---

### Error Handling Without Exceptions: Option/Result Types

**Principle:** Go's `(T, error)` is good, but in a deeply chained functional pipeline, an `Option[T]` (no value) or `Result[T]` (value-or-error) keeps the type system honest and eliminates a class of nil checks.

**Do:**
- Use `Option[T]` for "lookup may not find anything".
- Use `Result[T]` for "operation may fail with a specific error".
- Always provide an `OrElse(default)` so the call site stays short.
- Compose with `fmap`/`map` rather than manually unpacking.

**Don't:**
- Don't return `(T, error)` for cases that are *not exceptional* — those are normal "no result" cases.
- Don't reach for panics to "simplify" the API; it costs you testability and crashes callers.

**Code:**
```go
// Result type used as if it were a Maybe/Result.
ok := mo.Ok(MyDogs[0])
result1 := ok.OrElse(Dog{})         // {Bucky 1}
err1   := ok.Error()                  // <nil>
ok2   := mo.Err[Dog](errors.New("dog not found"))
result2 := ok2.OrElse(Dog{"Default", -1})  // {Default -1}
err2   := ok2.Error()                            // dog not found
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Mo, for go"*

---

### Functional Libraries: Reach for Them After 1.18, But Not First

**Principle:** Post-generics, the case for a third-party FP library is weaker in Go than in Haskell — a few dozen lines of generic `Filter`/`Map`/`Reduce` will cover 80% of needs. Reach for a library when you need a feature (e.g., dot-notation chaining, parallel map, `Option`/`Future`/`Result`) that would be tedious to write yourself.

**Do:**
- Choose by what you need:
  - **`pie` (v2)** for dot-notation chaining, `Sort`, `Uniq`, etc.
  - **`lo` (samber/lo)** for Lodash-style nested calls and `lo/parallel.Map` for easy concurrent map.
  - **`mo` (samber/mo)** for `Option`, `Result`, `Future`, `Either`.
- Check the GitHub activity (commits, issues) before adopting — the book warns that "library is alive" is a real concern.

**Don't:**
- Don't add a library for code you can write in 30 lines.
- Don't depend on a library whose last commit is years old and issues are unanswered.
- Don't skip the license review for commercial use.
- Don't build `Filter`/`Map`/`Reduce` by hand for the third time — consolidate or adopt a library.

**Code:**
```go
// Using `lo` for chained + parallel transformations.
import (
    "github.com/samber/lo"
    lop "github.com/samber/lo/parallel"
)
result := lop.Map(lo.Uniq(MyDogs), func(d Dog, _ int) Dog {
    d.Name = strings.ToUpper(d.Name)
    return d
})
```
*Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Functional Programming Libraries"*

---

## Anti-Patterns & Common Mistakes

- **"Pass-by-pointer is faster":** False by default. Benchmark before believing; immutable value-based code can win because it avoids heap allocation. → *fix:* write both versions, run `BenchmarkX` with `b.ReportAllocs()`, inspect with `go build -gcflags '-m -l'`.
- **Storing mutable state in a recursive function via global var:** Breaks concurrency, breaks testability, and leaks state between calls. → *fix:* use the outer-closure pattern (`Max` with inner `var inner func(...)`).
- **Recursing with `func(...) { inner(...) }` declaration order:** Won't compile. → *fix:* always `var inner func(...); inner = func(...) { ... }`.
- **Treating `(T, error)` as the only error path:** "Not found" is not an error — it's absence. → *fix:* use `Option[T]` or `Result[T]` for the may-be-absent case.
- **Defining an interface for a single function:** It's a verbose stand-in for a function type. → *fix:* use `type MyFunc func(...) ...` and a struct field.
- **Reaching for FP libraries before you need them:** A few dozen lines of generic `Filter`/`Map`/`Reduce` covers most needs. → *fix:* write your own first, adopt a library when the need is real and recurring.
- **Mutating a struct field from a "setter" function:** Destroys immutability, makes the function impure. → *fix:* accept by value, return a new struct.
- **Forgetting `close(out)` in a channel-based node:** Leaks the receiving goroutine. → *fix:* always defer `close(out)` at the top of the goroutine.
- **CPS for everyday control flow:** CPS is hard to read in Go's strict type system. → *fix:* use CPS only for compiler/interpreter work or complex async patterns.
- **Map-discriminator vs switch:** Adding a new operation to a long `switch` is friction. → *fix:* use a `map[string]OpFunc` and add entries (even inline anonymous functions).
- **Currying without a higher-order consumer:** A 2-arg `f(a, b)` is more readable than `f(a)(b)`. → *fix:* curry only to fit a higher-order signature (like `Node[A]`), not for its own sake.
- **Pre-allocating huge maps in eager chains when you only need the first match:** In Go you don't have Haskell's laziness, so use `Any` to short-circuit, not a `Filter` + `len > 0`.
- **Skipping the base case in recursion:** A recursive function with no base case is a stack overflow waiting to happen.

## Decision Heuristics / Checklists

- **Is the function pure enough?** Pass-by-value inputs, returns new value, no globals, no I/O. If yes, leave it pure; if not, can you split it into a pure part and a thin impure shell?
- **Do I need generics here?** If you find yourself writing `filterStrings`/`filterInts`/`filterDogs` — yes, use a `Predicate[A]`.
- **Type alias or interface?** One-method abstraction → type alias. Multi-method contract with stateful collaborators → interface.
- **Map or switch for dispatch?** If you add a new branch more than once a year, prefer a map. Otherwise, switch is fine.
- **Recursion or iteration?** Tree/graph traversal or self-similar structure → recursion. Linear scan or large input → iteration. Always have a base case; always benchmark.
- **Chain with dot-notation or with nested calls?** Short, obvious pipeline → dot-notation (`Map.Filter.Sum`). Anything that needs intermediate inspection → separate statements.
- **Channel pipeline or just call the functions?** If each step is short and synchronous, just call them. If any step is asynchronous, slow, or stream-shaped, use channels + `Node[A]`.
- **Add a library, or write 30 lines?** Default to writing your own generic toolbox. Adopt a library when the need is recurring across projects.
- **Mock by interface or by function?** Function field is usually enough; use a function-type alias in the struct.

## Key Takeaways

1. **Push impurity to the edges.** Aim for 90% pure, 10% impure. Pure functions are easier to test, reason about, and parallelize.
2. **Default to pass-by-value with returned copies.** Go is value-oriented; pointers cause heap allocation, GC pressure, and concurrency hazards.
3. **Use type aliases for clarity.** They self-document signatures, improve error messages, and enable attaching methods to "primitives".
4. **Functions are values; treat them as such.** Store them in struct fields, return them from functions, compose them. Strategy, Decorator, Factory all collapse to function manipulation.
5. **Currying and partial application exist to fit higher-order signatures.** Don't curry for fun; curry to make a function composable.
6. **Maybe/Option for absence, Result for fallible operations.** They eliminate nil checks and bubble error states through pipelines safely.
7. **Map/Filter/Reduce with generics are 30 lines that replace thousands.** Build them once.
8. **Channels + curried nodes = composable pipelines.** The pattern is the same as Unix pipes; just typed.
9. **Immutability can be faster than mutation.** Stack allocation beats heap allocation; benchmark it.
10. **Recursion in Go has no tail-call optimization.** Use it for natural tree-shaped problems; fall back to iteration for large or hot loops.
11. **FP is a tool, not a religion.** Go is multi-paradigm; pick the simplest approach that improves readability and testability.

## Cross-References
- Related: [[./Concurrency_in_Go.md]]
- Related: [[./Building_Modern_CLI_Applications_in_Go.md]]
- Topic index: [[../INDEX.md]]
