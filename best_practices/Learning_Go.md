# Learning Go — Maximum-Depth Deep-Dive

> Source: *Learning Go: An Idiomatic Approach to Real-World Go Programming*, 2nd Edition — Jon Bodner (O'Reilly)
>
> Coverage tags: `#general` `#concurrency` `#testing` `#api`
>
> This is a deep, code-first extraction organized by topic. Every claim is grounded in the book's source text. Code blocks are reproduced verbatim (or condensed only for length) from the book.

---

## Table of Contents

1. Go Environment & Toolchain (`#general`)
2. Composite Types: Arrays, Slices, Maps, Strings, Structs (`#general`)
3. Blocks, Shadowing, Control Flow (`#general`)
4. Functions: Multiple Returns, Closures, defer (`#general`)
5. Pointers & Memory (`#general`)
6. Types, Methods, Interfaces (`#general`)
7. Generics (`#general`)
8. Errors (`#general`)
9. Modules, Packages, Imports (`#general`)
10. Go Tooling (`#general`)
11. Concurrency: Goroutines, Channels, select (`#concurrency`)
12. Standard Library: io, time, encoding/json, net/http (`#api`)
13. Context (`#concurrency` `#api`)
14. Testing (`#testing`)
15. Reflection, Unsafe, Cgo (`#general`)

---

## 1. Go Environment & Toolchain `#general`

### 1.1 Installation & Single Native Binary

Go programs compile to a **single native binary** with no external runtime. Distribution is dramatically simpler than JVM, Python, or JavaScript workloads:

```sh
$ tar -C /usr/local -xzf go1.20.5.linux-amd64.tar.gz
$ echo 'export PATH=$PATH:/usr/local/go/bin' >> $HOME/.bash_profile
$ source $HOME/.bash_profile
$ go version
go version go1.20.5 linux/amd64
```

This property lets Go apps ship inside `scratch` or `distroless` Docker images.

### 1.2 The Three Foundational Commands

| Command     | Purpose                                                                                  |
|-------------|------------------------------------------------------------------------------------------|
| `go build`  | Compiles to a binary named after the module (`hello_world` by default; override with `-o`) |
| `go fmt`    | Enforces the single standard format (tabs, opening brace on same line as declaration) |
| `go vet`    | Catches likely bugs (e.g. `fmt.Printf("Hello, %s!\n")` with no arg) — valid syntax, almost certainly wrong |

### 1.3 Semicolon Insertion Rule

Go automatically inserts semicolons after the last token on a line if that token is any of:

- An **identifier** (e.g. `int`, `float64`)
- A **literal** (number, string)
- One of `break`, `continue`, `fallthrough`, `return`, `++`, `--`, `)`, `}`

This is why braces must open on the **same line** as the preceding statement. If you write:

```go
func main()
{
    fmt.Println("Hello, world!")
}
```

The lexer turns it into:

```go
func main();
{
    fmt.Println("Hello, world!");
};
```

— which is not valid Go.

### 1.4 Your First Program — `hello.go`

```go
package main
import "fmt"
func main() {
    fmt.Println("Hello, world!")
}
```

```sh
$ go mod init hello_world
$ go build
$ ./hello_world
Hello, world!
```

**Module path**: globally unique identifier, usually the repo URL (`github.com/jonbodner/proteus`). For local-only modules the name does not need to be unique.

### 1.5 Makefiles

```
.DEFAULT_GOAL := build
.PHONY: fmt vet build
fmt:
    go fmt ./...
vet: fmt
    go vet ./...
build: vet
    go build
```

- `.PHONY` prevents make from being confused if a directory or file shares a target name.
- Indentation **must** be tabs (not spaces). Make is not installed by default on Windows.

### 1.6 The Go Compatibility Promise

Since Go 1.0 (and reaffirmed by Russ Cox in the 2017 keynote "Compatibility: How Go Programs Keep Working"):

> Go 1 programs will continue to compile and run unchanged, in all major environments, for years to come.

This guarantee applies to the **language and standard library** — *not* to `go` command flags, which have been broken in the past.

### 1.7 Staying Up-to-Date

Linux/BSD: tar + replace. macOS/Windows: installers remove old versions automatically.

---

## 2. Composite Types `#general`

### 2.1 The Zero Value

Every type in Go has a default zero value, eliminating the C/C++ bug class of uninitialized variables:

| Type                    | Zero value                                |
|-------------------------|-------------------------------------------|
| Numeric (int, float, …) | `0`                                        |
| `bool`                  | `false`                                    |
| `string`                | `""`                                       |
| Pointer / slice / map / channel / function / interface | `nil` |

```go
var flag bool    // false
var isAwesome = true
```

### 2.2 Literals

**Integer**: base 10 default; prefixes `0b` (binary), `0o` (octal), `0x` (hex). Avoid the legacy `0` for octal — confusing.

**Underscore digit separators**: `1_234` is legal; underscores cannot lead/trail or sit adjacent.

**Floating-point**: decimal `6.03e23`; hex `0x12.34p5` (=582.5).

**Rune** (single quotes only): `'a'`, `'\141'`, `'\x61'`, `'\u0061'`, `'\U00000061'`.

**Strings**:
- **Interpreted**: `"Greetings and\n\"Salutations\""`
- **Raw** (backticks): `` `Greetings and "Salutations"` `` — no escapes, may span lines.

Single and double quotes are **not** interchangeable.

### 2.3 Numeric Types

12 types + special names. Default type for an integer literal is `int`.

| Type      | Use                                                                |
|-----------|--------------------------------------------------------------------|
| `int8`–`int64` | Signed integer (specified width)                            |
| `uint8`–`uint64` | Unsigned                                                |
| `float32`, `float64` | IEEE-754 floats; default to **float64**              |
| `complex64`, `complex128` | Built-in complex; rarely used                  |
| `byte`    | Alias for `uint8`                                                  |
| `rune`    | Alias for `int32`                                                  |
| `int`     | Platform word (32 or 64 bits); **the default**                    |
| `uint`    | Platform word, unsigned                                           |
| `uintptr` | Large enough to hold a pointer bit pattern (used in `unsafe`)      |

**Choosing an integer**:
1. Binary file format / network protocol with a specified width → use that width.
2. Generic library function → use a type parameter (Go 1.18+).
3. Everything else → **`int`**.

Operators: `+ - * / %`, with combined-assignment `+= -= *= /= %=`. `int / int` truncates toward zero. Comparison: `== != > >= < <=`.

**Floating-point pitfalls**:
- `0/0.0` → `NaN`; `x/0.0` → `+Inf` or `-Inf`.
- Never use `==` or `!=` to compare floats — use an epsilon.
- **Never represent money with floats** — use `shopspring/decimal` or similar.

### 2.4 Arrays — "Too Rigid to Use Directly"

The size is part of the type: `[3]int` and `[4]int` are *not* assignable.

```go
var x [3]int                          // all zero
var y = [3]int{10, 20, 30}            // full literal
var z = [12]int{1, 5: 4, 6, 10: 100, 15}  // sparse: index 0=1, 5=4, 6=6, 10=100, 11=15
var w = [...]int{10, 20, 30}          // size inferred
```

Read/write with `[i]`. Out-of-bounds with a constant → compile error; with a variable → runtime panic. `len(x)` returns length.

```go
var x [2][3]int   // multidim: array of 2 arrays of 3 ints
```

Arrays exist primarily as backing storage for slices.

### 2.5 Slices — The Workhorse

A slice is a 3-field struct `(pointer, length, capacity)` over an underlying array.

```go
var x = []int{10, 20, 30}
var y []int               // nil slice, len 0
x = append(x, 10)        // MUST assign return value
x = append(x, 5, 6, 7)   // multiple
y := []int{20, 30, 40}
x = append(x, y...)      // spread
```

**Growth**: when `len == cap`, `append` allocates a new array. Go 1.18+ growth rule:
- capacity < 256: **double**
- larger: `(cap + 768) / 4` (≈ 25% growth)

**`make`**: `make([]T, len)` or `make([]T, len, cap)`.

**`clear`** (Go 1.21+): zeroes elements; length unchanged.

**Nil vs empty slice**:
```go
var data []int      // nil — len 0, == nil true, JSON encodes as null
var x = []int{}     // empty — len 0, == nil false, JSON encodes as []
```

Prefer **nil** slices; reserve empty for JSON interop where `[]` is required.

**Slicing slices** (no copy — memory is shared):
```go
x := []string{"a","b","c","d"}
y := x[:2]    // ["a","b"], cap 4 — appending y can corrupt x!
z := x[1:3:3] // full slice expression — cap equals len, safe append
```

**Three-part expression** (`x[low:high:max]`): `cap(z) = max - low`. Limits subslice capacity to prevent silent append-overwrites.

**`copy`**:
```go
src := []int{1,2,3,4}
dst := make([]int, 4)
n := copy(dst, src)        // copies min(len(dst), len(src)) elements
copy(dst, src[2:])         // copies from middle
copy(x[:3], x[1:])         // overlapping — supported
```

**Array → slice**: `xArray[:]` (entire) or `xArray[:2]`. Memory is shared.

**Slice → array** (Go 1.20+): `xArray := [4]int(xSlice)`. **Data is copied**. If the array size exceeds the slice length, runtime panic. Also `[4]int{...}` versus `(*[4]int)(xSlice)` — the latter shares memory.

### 2.6 Strings, Runes, and Bytes

Strings are **immutable UTF-8 byte sequences**, *not* rune sequences.

```go
var s string = "Hello there"
var b byte = s[6]             // byte 116 == 't'
var sub = s[4:7]              // "o t"  (byte-indexed)
len("Hello ☀")               // 10 (sun emoji = 4 bytes), NOT 7
```

`for-range` over a string yields runes (correctly iterating multi-byte code points):

```go
samples := []string{"hello", "apple_π!"}
for _, sample := range samples {
    for i, r := range sample {
        fmt.Println(i, r, string(r))
    }
}
// for "apple_π!" — index 6 = 960 ('π'), then index jumps to 8 (skipping 7)
```

`rune` is `int32`. A single rune can be cast to string:

```go
var a rune = 'x'
var s string = string(a)        // "x"
```

`go vet` blocks `string(intVal)` conversions (Go 1.15+) — a common new-developer bug.

```go
var bs []byte = []byte(s)        // [72 101 108 ...]
var rs []rune = []rune(s)        // [72 101 108 ...]
```

`clear(s)` zeroes string characters (Go 1.21+).

### 2.7 Maps

```go
var m1 map[string]int                          // nil; READ returns zero, WRITE panics
m2 := map[string]int{}                        // empty literal — readable & writable
m3 := map[string][]string{                    // composite value
    "Orcas": {"Fred", "Ralph"},
}
m4 := make(map[int][]string, 10)               // initial size hint
```

**Read/Write**:
```go
totalWins["Orcas"] = 1
v := totalWins["Orcas"]    // returns 0 if missing — same as zero value!
```

**Comma-ok**:
```go
v, ok := m["hello"]    // ok = true if key present
```

**Delete**: `delete(m, "key")` — safe on missing key or nil map.

**Clear** (Go 1.21+): `clear(m)` empties the map (length → 0).

**Equality**: `==` only works vs `nil`. Use `maps.Equal` / `maps.EqualFunc` (Go 1.21+).

**Key constraints**: any comparable type. No slices, no maps.

**Set idiom**:
```go
intSet := map[int]bool{}
for _, v := range vals {
    intSet[v] = true
}
```

Use `map[T]struct{}` to save 1 byte per entry if you have huge sets; otherwise `bool` is clearer.

### 2.8 Structs

```go
type person struct {
    name string
    age  int
    pet  string
}

var fred person                      // zero-valued struct
bob := person{}                      // same as var bob person
julia := person{"Julia", 40, "cat"}  // positional — all fields required
beth := person{                      // named — partial allowed (missing → zero)
    age:  30,
    name: "Beth",
}
```

**Anonymous structs** — useful for JSON and table tests:
```go
var person struct {
    name string
    age  int
    pet  string
}
person.name = "bob"
```

**Comparison**: structs are comparable iff all fields are comparable. Slices/maps/functions in fields → not comparable.

**Conversion**: allowed only when both structs have identical field names, order, and types. A named struct and an anonymous struct with the same fields are assignable directly (no conversion needed).

---

## 3. Blocks, Shadowing, Control Flow `#general`

### 3.1 Block Hierarchy

```
universe block   ←  true, false, nil, int, len, make, …
└── package block ←  declared at package scope
    └── file block ←  imports
        └── function block ←  parameters + locals
            └── inner block ←  if/for/switch bodies
```

Inner blocks can read outer; **declarations in inner blocks shadow outer identifiers**.

### 3.2 Shadowing — The Most Common Beginner Bug

```go
func main() {
    x := 10
    if x > 5 {
        fmt.Println(x)   // 10 — outer x visible
        x := 5            // SHADOWS outer x — new variable
        fmt.Println(x)   // 5  — inner x
    }
    fmt.Println(x)       // 10 — outer x unchanged
}
```

Output: `10 5 10`.

`:=` makes accidental shadowing dangerously easy:

```go
x := 10
if x > 5 {
    x, y := 5, 20    // x is shadowed (NOT reused) — surprise!
    fmt.Println(x, y)
}
```

**Package shadowing** is even worse:
```go
fmt.Println(x)
fmt := "oops"
fmt.Println(fmt)   // compile error: type string has no field or method Println
```

**Universe shadowing** (the truly insidious one):
```go
fmt.Println(true)
true := 10          // compiler doesn't catch this for built-ins!
fmt.Println(true)   // prints "true 10"
```

Use a linter like `shadow` (in golangci-lint) to detect accidental shadowing.

### 3.3 `if` — With Init Statement

```go
if n := rand.Intn(10); n == 0 {
    fmt.Println("That's too low")
} else if n > 5 {
    fmt.Println("That's too big:", n)
} else {
    fmt.Println("That's a good number:", n)
}
fmt.Println(n)   // COMPILE ERROR — n out of scope
```

`n` lives only within the if/else chain.

### 3.4 `for` — The Only Loop Keyword

Four forms:

```go
// 1. C-style
for i := 0; i < 10; i++ { }

// 2. While-style (condition only)
for i < 100 {
    i = i * 2
}

// 3. Infinite
for {
    if done { break }
}

// 4. for-range
for i, v := range slice {
    fmt.Println(i, v)
}
```

**Map iteration order varies per run** — a deliberate security feature against Hash DoS attacks. `fmt.Println` of a map sorts keys.

**String iteration yields runes**, not bytes, with offset in bytes:
```go
for i, r := range "apple_π!" {
    fmt.Println(i, r)
}
// 6 960  (π = U+03C0, 2 bytes in UTF-8)
// 8 33   (next offset is 8, not 7)
```

**Pre-Go 1.22 bug**: `for _, v := range data` reused the same `v` across iterations. With goroutines this caused all closures to see the final value. **Go 1.22+ creates a fresh `v` per iteration** (controlled by `go 1.22` directive in go.mod).

```go
// Mitigation for older Go:
for _, v := range data {
    v := v                            // explicit shadow
    go func() { ch <- v * 2 }()
}
// OR pass explicitly:
for _, v := range data {
    go func(val int) { ch <- val * 2 }(v)
}
```

**Labels**: nested-loop escape:
```go
outer:
    for _, sample := range samples {
        for i, r := range sample {
            if r == 'l' { continue outer }
        }
    }
```

### 3.5 `switch`

**No implicit fallthrough**. Multiple values with comma:

```go
switch size := len(word); size {
case 1, 2, 3, 4:
    fmt.Println(word, "is a short word!")
case 5:
    wordLen := len(word)
    fmt.Println(word, "is exactly the right length:", wordLen)
case 6, 7, 8, 9:
    // empty case = nothing happens
default:
    fmt.Println(word, "is a long word!")
}
```

**Blank switch** (`switch {}`) — like `if/else if` with N boolean comparisons:
```go
switch {
case i%3 == 0 && i%5 == 0: fmt.Println("FizzBuzz")
case i%3 == 0:            fmt.Println("Fizz")
case i%5 == 0:            fmt.Println("Buzz")
default:                  fmt.Println(i)
}
```

**`fallthrough`** exists but should be avoided.

### 3.6 `goto`

Heavily restricted — cannot skip variable declarations, cannot jump into inner blocks. One valid use: cleanup at end of function regardless of how exited:

```go
done:
    fmt.Println("cleanup")
```

`continue` and `break` cover most labeled-loop needs; prefer them.

---

## 4. Functions `#general`

### 4.1 Declaration

```go
func div(num, denom int) int {  // consecutive same-type parameters
    if denom == 0 {
        return 0
    }
    return num / denom
}
```

Returns:
- `(int, int, error)` — multiple values are common, error always last by convention
- Named returns: `(result int, remainder int, err error)` — pre-declared, modifiable, useful with `defer`

**Never use blank (naked) returns** — they obscure data flow.

### 4.2 Variadic Parameters

```go
func addTo(base int, vals ...int) []int {
    out := make([]int, 0, len(vals))
    for _, v := range vals {
        out = append(out, base+v)
    }
    return out
}
addTo(3)                 // []
addTo(3, 2)              // [5]
addTo(3, 2, 4, 6, 8)     // [5 7 9 11]
addTo(3, []int{4, 3}...) // [7 6] — spread
```

### 4.3 Multiple Return Values Are Values (Not Tuples)

```go
result, remainder, err := divAndRemainder(5, 2)
result, _, err := divAndRemainder(5, 2)        // discard remainder
divAndRemainder(5, 2)                          // discards ALL returns — usually bad
```

You must assign each return to a separate variable. `_, _ = f()` is allowed.

### 4.4 Functions as Values

```go
var opMap = map[string]func(int, int) int{
    "+": add, "-": sub, "*": mul, "/": div,
}
opFunc, ok := opMap[op]
result := opFunc(p1, p2)
```

**Function type declaration** for documentation:
```go
type opFuncType func(int, int) int
```

### 4.5 Anonymous Functions and Closures

```go
f := func(j int) {
    fmt.Println("printing", j, "from inside of an anonymous function")
}
f(10)
```

**Closures capture variables** from their enclosing scope:
```go
func main() {
    a := 20
    f := func() {
        fmt.Println(a)
        a = 30
    }
    f()              // 20
    fmt.Println(a)   // 30
}
```

Using `:=` inside a closure creates a *new* variable that disappears when the closure exits:
```go
a := 20
f := func() {
    fmt.Println(a)
    a := 30           // shadow — different a!
    fmt.Println(a)
}
f()                    // 20 30
fmt.Println(a)         // 20
```

### 4.6 Passing / Returning Functions

**Higher-order functions** are common — `sort.Slice(slice, func(i, j int) bool { ... })`.

```go
func makeMult(base int) func(int) int {
    return func(factor int) int {
        return base * factor
    }
}
twoBase := makeMult(2)
fmt.Println(twoBase(5))   // 10
```

### 4.7 `defer`

```go
f, err := os.Open(name)
if err != nil { return err }
defer f.Close()        // runs when function exits — even on panic
```

**Rules**:
- Multiple `defer` runs in **LIFO** order.
- Arguments to deferred calls are evaluated **immediately** (the function's reference, but the args are captured now).
- Input parameters are NOT evaluated immediately — the function call is.
- Deferred function **return values are discarded** (Go does let you pass them into a wrapper).

**Modify return values via named returns** — the canonical pattern for adding context to errors:
```go
func DoSomeInserts(ctx context.Context, db *sql.DB, val1, val2 string) (err error) {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil { return err }
    defer func() {
        if err == nil {
            err = tx.Commit()
        }
        if err != nil {
            tx.Rollback()
        }
    }()
    _, err = tx.ExecContext(ctx, "INSERT ...", val1)
    return err
}
```

### 4.8 Closures as Cleanup Handlers

Returning a cleanup closure enforces its use:
```go
func getFile(name string) (*os.File, func(), error) {
    file, err := os.Open(name)
    if err != nil { return nil, nil, err }
    return file, func() { file.Close() }, nil
}

f, closer, err := getFile(os.Args[1])
if err != nil { log.Fatal(err) }
defer closer()
```

### 4.9 Go Is Call by Value

```go
type person struct { age int; name string }
func modifyFails(i int, s string, p person) {
    i = i*2; s = "Goodbye"; p.name = "Bob"
}

p := person{}
i, s := 2, "Hello"
modifyFails(i, s, p)
fmt.Println(i, s, p)   // 2 Hello {0 }  — nothing changed
```

**Maps**: passes the pointer — modifications are visible to caller.

**Slices**: header (ptr, len, cap) is copied but the underlying array is shared — element changes are visible, `append` (which may reallocate) is NOT visible.

### 4.10 The `simple_cat` Pattern (I/O Starter)

```go
func main() {
    if len(os.Args) < 2 { log.Fatal("no file specified") }
    f, err := os.Open(os.Args[1])
    if err != nil { log.Fatal(err) }
    defer f.Close()
    data := make([]byte, 2048)
    for {
        count, err := f.Read(data)
        os.Stdout.Write(data[:count])
        if err != nil {
            if err != io.EOF { log.Fatal(err) }
            break
        }
    }
}
```

---

## 5. Pointers & Memory `#general`

### 5.1 Anatomy

```go
var x int32 = 10
var y bool = true
pointerX := &x       // type *int32
pointerY := &y       // type *bool
var pointerZ *string // nil
```

- `&x` — address-of operator (yields `*T`).
- `*p` — dereference / indirection.
- Dereferencing nil → **panic**.

```go
var x = new(int)       // *int pointing to a zero int
fmt.Println(x == nil)  // false
fmt.Println(*x)         // 0
```

`new(T)` returns `*T` to a zero-valued T. For structs prefer `&Foo{}`. Cannot `&(literal)` — literals have no address.

**Generic helper to take the address of a literal**:
```go
func makePointer[T any](t T) *T {
    return &t
}
p := person{ FirstName: "Pat", MiddleName: makePointer("Perry"), LastName: "Peterson" }
```

### 5.2 Pointers Are Just Familiar OOP Behavior

Java/JavaScript/Python/Ruby always pass class instances by pointer (under the hood). Go gives you the **choice**:

| Situation                              | Use Pointer or Value?          |
|----------------------------------------|--------------------------------|
| Want to mutate the parameter           | Pointer                        |
| Want to signal "optional / no value"   | Pointer (nil)                  |
| Data > 10 MB                           | Pointer (perf)                 |
| Pure functional transform              | Value                          |
| All other cases                        | **Value (default)**            |

The book offers this analogy: **"pointer parameters behave exactly like class instances in Java."** The surprising thing for newcomers is not pointers but Go's *value* semantics.

### 5.3 Pointers = Mutable Parameters

```go
func failedUpdate(g *int) {
    x := 10
    g = &x        // reassigning local g; caller still sees nil
}
func update(px *int) {
    *px = 20       // dereference and write through — caller sees change
}
```

You **cannot** make a nil parameter non-nil — `g = &x` only updates the copy.

### 5.4 "Pointers Are a Last Resort"

```go
// DON'T
func MakeFoo(f *Foo) error {
    f.Field1 = "val"
    f.Field2 = 20
    return nil
}
// DO
func MakeFoo() (Foo, error) {
    return Foo{Field1: "val", Field2: 20}, nil
}
```

**Exception**: when the function expects an interface (e.g. `json.Unmarshal([]byte, &f)` must take pointer because of generics absence pre-1.18 and allocation control).

### 5.5 Pointer Passing Performance

| Data size       | Pass by value | Pass by pointer |
|-----------------|---------------|-----------------|
| 100 B           | ~10 ns        | ~30 ns          |
| 100 KB          | similar       | faster          |
| 10 MB           | ~0.7 ms       | ~0.5 ms         |
| 10 MB return    | ~1.5 ms       | ~0.5 ms         |

For data under 10 MB, **value returns are faster** (no heap allocation).

### 5.6 Zero Value vs No Value (Pointer in JSON Fields)

```go
type person struct {
    FirstName  string
    MiddleName *string  // nil = "not set"; "" = "explicitly empty"
    LastName   string
}
```

Use `*string` for **nullable JSON fields**, otherwise use plain `string`.

### 5.7 Memory Model: Stack vs Heap

- **Stack**: local variables, parameters. Very fast. Known-size data.
- **Heap**: data whose lifetime can't be predicted at compile time. Subject to GC.

**Escape analysis** (compiler):
- Pointer returned from function → escapes to heap.
- Pointer passed to a function the compiler can't fully trace → escapes.

```sh
go build -gcflags="-m"
# main.go:5:6: moved to heap: x
```

**Goroutine stacks** grow dynamically (unlike OS threads). Initial stack is small (2 KB); can grow to 1 GB. Growing requires copying — expensive.

### 5.8 GOGC and GOMEMLIMIT

```sh
GOGC=100           # default — trigger GC when heap doubles
GOGC=200           # halve GC CPU time (bigger heap)
GOGC=off           # disable GC (memory leak risk)

GOMEMLIMIT=3GiB    # soft limit; soft means it can be exceeded under pressure
```

`GOMEMLIMIT` is **soft** to prevent thrashing — Go allows temporary overruns rather than spinning in GC.

### 5.9 Map and Slice Memory Layout

**Map**: implemented as `*runtime.hmap` — passing a map passes the pointer.

**Slice**: struct `(data *T, len int, cap int)` — header copied, underlying array shared. Length-changing `append` is invisible to caller; element changes are visible.

```go
func modSlice(s []int) {
    for k, v := range s { s[k] = v * 2 }   // visible to caller
    s = append(s, 10)                     // NOT visible
}
```

---

## 6. Types, Methods, Interfaces `#general`

### 6.1 Type Declarations — Executable Documentation

```go
type Score int
type Converter func(string) Score
type TeamScores map[string]Score
```

`type X Y` creates a **distinct type** sharing Y's underlying representation. Not inheritance — no implicit conversion, no method sharing.

```go
var i int = 300
var s Score = 100
s = i              // compile error
s = Score(i)       // OK
```

**User-defined types whose underlying type is a built-in can use literals and operators**:
```go
var s Score = 50
scoreWithBonus := s + 100   // also Score
```

### 6.2 Methods

```go
type Counter struct {
    total       int
    lastUpdated time.Time
}

func (c *Counter) Increment() {       // pointer receiver
    c.total++
    c.lastUpdated = time.Now()
}

func (c Counter) String() string {    // value receiver
    return fmt.Sprintf("total: %d, last updated: %v", c.total, c.lastUpdated)
}
```

**Receiver choice**:
- Mutates receiver → **pointer** (required).
- Must handle `nil` → **pointer** (required).
- Otherwise, **value** unless the type has other pointer receivers — then be consistent.
- `nil`-pointer **value receiver method** → panic. `nil`-pointer **pointer receiver method** → works if the method handles nil.

**Method set rules**:
- Pointer instance has both value-receiver and pointer-receiver methods in its method set.
- Value instance has only value-receiver methods.
- `(&c).String()` and `c.Increment()` syntax is interchangeable — Go inserts the address/dereference.

```go
// Common pattern:
type IntTree struct {
    val         int
    left, right *IntTree
}

func (it *IntTree) Insert(val int) *IntTree {
    if it == nil {
        return &IntTree{val: val}
    }
    if val < it.val { it.left  = it.left.Insert(val) }
    if val > it.val { it.right = it.right.Insert(val) }
    return it
}

func (it *IntTree) Contains(val int) bool {
    switch {
    case it == nil:            return false
    case val < it.val:         return it.left.Contains(val)
    case val > it.val:         return it.right.Contains(val)
    default:                   return true
    }
}

var it *IntTree
it = it.Insert(5).Insert(3).Insert(10).Insert(2)
fmt.Println(it.Contains(2))   // true
```

### 6.3 Methods as Functions

```go
type Adder struct{ start int }
func (a Adder) AddTo(val int) int { return a.start + val }

myAdder := Adder{start: 10}

// Method value — closure-like
f1 := myAdder.AddTo
f1(5)                // 15

// Method expression
f2 := Adder.AddTo
f2(myAdder, 15)      // 25
```

### 6.4 `iota` for Enumerations

```go
type MailCategory int
const (
    Uncategorized MailCategory = iota  // 0
    Personal                            // 1
    Spam                                // 2
    Social                              // 3
    Advertisements                      // 4
)
```

**iota is fragile** when reordered or inserted in the middle. **Best practice**: use iota only when the **names** matter, not the values. If the spec dictates values, hard-code them.

If zero value is meaningless, assign `_` or `Invalid` to iota=0 to make uninitialized detection easy:
```go
const (
    InvalidStatus Status = iota   // 0 = invalid sentinel
    Active
    Paused
)
```

### 6.5 Embedding for Composition — Not Inheritance

```go
type Employee struct {
    Name string
    ID   string
}
func (e Employee) Description() string { return fmt.Sprintf("%s (%s)", e.Name, e.ID) }

type Manager struct {
    Employee          // embedded — methods promoted
    Reports []Employee
}

m := Manager{
    Employee: Employee{Name: "Bob Bobson", ID: "12345"},
    Reports:  []Employee{},
}
fmt.Println(m.ID)              // 12345 — promoted
fmt.Println(m.Description())    // promoted method
```

**Embedding is NOT inheritance**:
- `var e Employee = m` — compile error. `var e Employee = m.Employee` works.
- No dynamic dispatch. If `Manager.Double()` exists, embedded field's `Double()` still wins inside embedded methods.

You can embed **any type** (not just structs). Embedded field methods are promoted.

### 6.6 Interfaces — Type-Safe Duck Typing

```go
type Stringer interface {
    String() string
}
type Incrementer interface {
    Increment()
}

var counter Counter
var inc Incrementer = &counter   // pointer has pointer-receiver methods
inc.Increment()

var val Counter
var inc2 Incrementer = val         // COMPILE ERROR — value lacks pointer-receiver methods
```

Implicit — no `implements` keyword. Implementation is structural.

**Interface rule of thumb**:
```go
// Wrong:
type Customer interface { ... }    // defined in same package as implementation

// Right:
type Customer interface { ... }    // defined in package that USES it
// Implementation lives elsewhere with no awareness of Customer
```

### 6.7 `Accept Interfaces, Return Structs`

- Input parameters: interfaces (flexible, testable, documented contract).
- Return values: concrete structs (avoids breaking backward compat when methods are added).

**Rare exceptions**: factory functions returning interfaces (database drivers, parsers with multiple token types), `error` (must be interface), `io.Reader`.

### 6.8 Interfaces and `nil`

An interface value is a `(type, value)` pair. **Both** must be nil for the interface to be nil:

```go
var pc *Counter            // nil pointer
var inc Incrementer = pc   // type=*Counter, value=nil → NOT nil interface
fmt.Println(inc == nil)   // false
```

Detecting a nil underlying value requires reflection (`reflect.Value.IsNil()`).

### 6.9 Interfaces Are Comparable — Carefully

Two interface values are equal iff types match and values are equal:

```go
type Doubler interface{ Double() }
type DoubleInt int
func (d *DoubleInt) Double()      { *d *= 2 }
type DoubleIntSlice []int
func (d DoubleIntSlice) Double()  { for i := range d { d[i] *= 2 } }

DoublerCompare(&di, dis2)         // PANIC: DoubleIntSlice not comparable
```

Panic at runtime. **Avoid `==` on interface values** unless you control all implementations.

### 6.10 The Empty Interface — `any`

```go
var i any
i = 20
i = "hello"
i = struct{ FirstName, LastName string }{"Fred", "Fredson"}
```

`any` is an alias for `interface{}` since Go 1.18. **Use sparingly** — it loses type safety.

### 6.11 Type Assertions and Type Switches

```go
i2 := i.(MyInt)                      // type assertion — panics if wrong type
i2, ok := i.(int)                    // comma-ok — safe
```

```go
switch j := i.(type) {
case nil:                  // j is any
case int:                  // j is int
case MyInt:                // j is MyInt
case io.Reader:            // j is io.Reader
case string:               // j is string
case bool, rune:           // j is any (multiple types)
default:                   // j is any
}
```

**Use sparingly**. Prefer accepting concrete types or interfaces in function signatures.

### 6.12 Function Types as a Bridge to Interfaces

```go
type HandlerFunc func(http.ResponseWriter, *http.Request)
func (f HandlerFunc) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    f(w, r)
}
```

Now any plain function with that signature satisfies `http.Handler`.

### 6.13 Implicit Interfaces Enable Dependency Injection

```go
type Logger interface{ Log(message string) }
type DataStore interface{ UserNameForID(string) (string, bool) }

type LoggerAdapter func(string)
func (lg LoggerAdapter) Log(msg string) { lg(msg) }

// LoggerAdapter and *SimpleDataStore* implicitly satisfy Logger and DataStore — neither
// "knows" it implements the interface.
type SimpleLogic struct {
    l  Logger
    ds DataStore
}

func main() {
    l  := LoggerAdapter(LogOutput)
    ds := NewSimpleDataStore()
    logic := NewSimpleLogic(l, ds)
    c   := NewController(l, logic)
    http.HandleFunc("/hello", c.SayHello)
    http.ListenAndServe(":8080", nil)
}
```

This is what enables idiomatic Go testing — interfaces let you substitute fakes/stubs in tests without changing production code.

For heavyweight projects, [Wire](https://github.com/google/wire) generates the wiring.

---

## 7. Generics `#general`

### 7.1 Why Generics

Before Go 1.18, generic algorithms required interface-based wrappers which lose compile-time type safety:

```go
type Orderable interface { Order(any) int }
type OrderableInt int
func (oi OrderableInt) Order(val any) int {
    return int(oi - val.(OrderableInt))   // panics if wrong type
}
```

Generics bring back static type safety for reusable algorithms.

### 7.2 Generic Stack — First Example

```go
type Stack[T any] struct { vals []T }

func (s *Stack[T]) Push(val T) { s.vals = append(s.vals, val) }

func (s *Stack[T]) Pop() (T, bool) {
    if len(s.vals) == 0 { var zero T; return zero, false }
    top := s.vals[len(s.vals)-1]
    s.vals = s.vals[:len(s.vals)-1]
    return top, true
}

var intStack Stack[int]
intStack.Push(10)
intStack.Push("nope")    // COMPILE ERROR
```

### 7.3 Type Constraints

```go
type Stack[T comparable] struct { vals []T }   // comparable = supports ==, !=

type Integer interface {
    int | int8 | int16 | int32 | int64 |
    uint | uint8 | uint16 | uint32 | uint64 | uintptr
}

func divAndRemainder[T Integer](num, denom T) (T, T, error) {
    if denom == 0 { return 0, 0, errors.New("division by zero") }
    return num / denom, num % denom, nil
}
```

Use `~T` to match **types with T as underlying type**. The `cmp.Ordered` interface (Go 1.21+) covers all comparable + ordered types.

### 7.4 Generic Functions — Map/Reduce/Filter

```go
func Map[T1, T2 any](s []T1, f func(T1) T2) []T2 {
    r := make([]T2, len(s))
    for i, v := range s { r[i] = f(v) }
    return r
}

func Reduce[T1, T2 any](s []T1, init T2, f func(T2, T1) T2) T2 {
    r := init
    for _, v := range s { r = f(r, v) }
    return r
}

func Filter[T any](s []T, f func(T) bool) []T {
    var r []T
    for _, v := range s { if f(v) { r = append(r, v) } }
    return r
}
```

### 7.5 Limitations & Performance

- ❌ No method-level type parameters (can't chain `.Map().Reduce()`).
- ❌ No variadic type parameters. ❌ No specialization, currying, metaprogramming.

**Performance**: Go 1.20 shares generated functions across pointer types with runtime lookups. **Replacing interface parameters with type parameters can make code ~30% slower** for trivial functions. Benchmark before optimizing.

**New standard library helpers** (Go 1.21+): `slices.Equal/Insert/Delete/Clone/Sort*/BinarySearch*`, `maps.Equal/Clone/Copy/DeleteFunc`, `cmp.Compare/Less/Ordered`.

---

## 8. Errors `#general`

### 8.1 The `error` Interface

```go
type error interface { Error() string }
```

Convention: error is **last return value**. `nil` means success.

```go
func calcRemainderAndMod(num, denom int) (int, int, error) {
    if denom == 0 { return 0, 0, errors.New("denominator is 0") }
    return num / denom, num % denom, nil
}

remainder, mod, err := calcRemainderAndMod(numerator, denominator)
if err != nil { fmt.Println(err); os.Exit(1) }
fmt.Println(remainder, mod)
```

**Error message style**: not capitalized, no trailing punctuation/newline.

### 8.2 Sentinel Errors

```go
package zip
var ErrFormat = errors.New("not a valid zip file")

notAZipFile := bytes.NewReader(data)
_, err := zip.NewReader(notAZipFile, int64(len(data)))
if err == zip.ErrFormat { fmt.Println("Told you so") }
```

**Rules**: rare, names start with `Err` (except `io.EOF`), use `==` to test. Once public, you cannot remove.

### 8.3 Custom Error Types

```go
type Status int
const (
    InvalidLogin Status = iota + 1
    NotFound
)

type StatusErr struct {
    Status  Status
    Message string
}
func (se StatusErr) Error() string { return se.Message }
```

**Critical**: always return `error`, never `*StatusErr` or `StatusErr`. An uninitialized custom error variable has non-nil type and is **non-nil**:

```go
// BAD — interface has type=StatusErr, value=zero → NOT nil!
func GenerateErrorBroken(flag bool) error {
    var genErr StatusErr
    if flag { genErr = StatusErr{Status: NotFound} }
    return genErr
}

// GOOD — explicit nil
func GenerateErrorOK(flag bool) error {
    if flag { return StatusErr{Status: NotFound} }
    return nil
}

// GOOD — error-typed variable
func GenerateErrorVar(flag bool) error {
    var genErr error
    if flag { genErr = StatusErr{Status: NotFound} }
    return genErr
}
```

### 8.4 Wrapping Errors — `%w`

```go
func fileChecker(name string) error {
    f, err := os.Open(name)
    if err != nil { return fmt.Errorf("in fileChecker: %w", err) }
    f.Close()
    return nil
}
// Output: in fileChecker: open not_here.txt: no such file or directory
```

`%v` creates a new message without the chain. `%w` preserves it. Custom type with chain:

```go
type StatusErr struct {
    Status Status; Message string; Err error
}
func (se StatusErr) Error() string { return se.Message }
func (se StatusErr) Unwrap() error { return se.Err }
```

### 8.5 Multiple Errors — `errors.Join`

```go
func ValidatePerson(p Person) error {
    var errs []error
    if len(p.FirstName) == 0 { errs = append(errs, errors.New("field FirstName cannot be empty")) }
    if len(p.LastName) == 0  { errs = append(errs, errors.New("field LastName cannot be empty")) }
    if p.Age < 0             { errs = append(errs, errors.New("field Age cannot be negative")) }
    if len(errs) > 0 { return errors.Join(errs...) }
    return nil
}
```

Or with multiple `%w`: `fmt.Errorf("first: %w, second: %w", err1, err2)`. Implement custom `Unwrap() []error` for multi-wrapping.

### 8.6 `errors.Is` and `errors.As`

```go
err := fileChecker("not_here.txt")
if errors.Is(err, os.ErrNotExist) { fmt.Println("That file doesn't exist") }

var myErr MyErr
if errors.As(err, &myErr) { fmt.Println(myErr.Codes) }
// Or by interface:
var coder interface { CodeVals() []int }
if errors.As(err, &coder) { fmt.Println(coder.CodeVals()) }
```

**Custom `Is` for pattern matching**:
```go
type ResourceErr struct { Resource string; Code int }
func (re ResourceErr) Is(target error) bool {
    if other, ok := target.(ResourceErr); ok {
        return other.Resource == re.Resource || other.Code == re.Code
    }
    return false
}
if errors.Is(err, ResourceErr{Resource: "Database"}) { /* ... */ }
```

> `errors.Is` looks for **specific instances / values**. `errors.As` looks for **specific types**.

### 8.7 Wrapping Errors with `defer`

```go
func DoSomeThings(val1 int, val2 string) (_ string, err error) {
    defer func() {
        if err != nil { err = fmt.Errorf("in DoSomeThings: %w", err) }
    }()
    val3, err := doThing1(val1)
    if err != nil { return "", err }
    val4, err := doThing2(val2)
    if err != nil { return "", err }
    return doThing3(val3, val4)
}
```

Named return + deferred wrap = clean repetitive context.

### 8.8 `panic` and `recover`

```go
func div60(i int) {
    defer func() {
        if v := recover(); v != nil { fmt.Println(v) }
    }()
    fmt.Println(60 / i)
}
```

**When to use**:
- ✅ Wrap third-party libraries that may panic, to prevent escape from your public API.
- ✅ Genuine unrecoverable situations (out of memory).
- ❌ Not for normal error flow — return errors instead.
- ❌ The Go team now considers `net/http` server's automatic `panic` recovery in handlers a mistake.

`panic(nil)` is identical to `panic(new(runtime.PanicNilError))` since Go 1.21.

`panic(nil)` → since Go 1.21, treated as `panic(new(runtime.PanicNilError))`.

---

## 9. Modules, Packages, Imports `#general`

### 9.1 Repository → Module → Package Hierarchy

```
Repository (git)
└── Module (go.mod)  ← one per repo (recommended)
    ├── Package (directory) ← "do-format" imports as "format"
    │   └── .go files (all share package clause)
    └── Package ...
```

Go's "module" ≈ Node's "package", Go's "package" ≈ Node's "module".

### 9.2 `go.mod`, Commands, and MVS

```go
module github.com/learning-go-book-2e/money
go 1.21
require (
    github.com/learning-go-book-2e/formatter v0.0.0-20220918024742-...
    github.com/shopspring/decimal v1.3.1
)
```

**`go` directive** (Go 1.21+) interacts with `toolchain` and `GOTOOLCHAIN`: `auto` (default), `local`, or `go1.X.Y`. **Go 1.22+** enables per-iteration loop variables when `go 1.22` is set.

```sh
go mod init github.com/me/project     # create go.mod
go get ./...                          # scan imports and add requires
go get pkg@version                    # add or update specific version
go get -u=patch                       # upgrade within current minor
go get -u                             # upgrade to latest (within major)
go mod tidy                           # sync go.mod with imports
go mod vendor                         # copy deps into vendor/
go list -m -versions pkg              # show available versions
go mod graph                          # full dependency graph
```

**Minimal Version Selection**: when two deps want different versions, Go picks the **lowest version that satisfies all** `require` directives.

### 9.3 Incompatible Versions (Major ≥ 2)

Major version bumps require **module path suffix**: `github.com/me/project/v2`. The v1 and v2 are *separate modules* that can be imported side by side.

### 9.4 Package Basics

```go
// package_clause.go
package math
func Double(a int) int { return a * 2 }
```

```go
package main
import (
    "fmt"
    "github.com/learning-go-book-2e/package_example/do-format"
    "github.com/learning-go-book-2e/package_example/math"
)

func main() {
    num := math.Double(2)
    output := format.Number(num)
    fmt.Println(output)
}
```

Package name (in clause) need not match directory name — but should. `package main` is the program entry; not importable. **Don't use underscores in package names.**

**Naming**: short, lowercase, descriptive purpose. `names.Extract` not `names.ExtractNames`. Exception: `sort.Sort`, `context.Context`.

**Collision resolution**:
```go
import (
    crand "crypto/rand"      // renamed
    "math/rand"              // default name
)
```

`.` (dot) import — discouraged. `_` blank import triggers `init()` for side effects (database drivers, image format registration).

### 9.5 Documentation

```go
// Package convert provides utilities to convert money
// from one currency to another.
package convert

// Money represents an amount of money and the currency.
// The value is stored using a [github.com/shopspring/decimal.Decimal]
type Money struct {
    Value    decimal.Decimal
    Currency string
}

// Convert converts the value of one currency to another.
//
// [Investopedia]: https://www.investopedia.com/terms/e/exchangerate.asp
func Convert(from Money, to string) (Money, error) { /* ... */ }
```

Rules:
- Comment directly above declaration, no blank line.
- Start with the identifier name (or "A"/"An" + identifier).
- `// Package x ...` for package-level docs (or `doc.go`).
- Bracket syntax: `[pkg]`, `[Symbol]`, `[text]: url`.

### 9.6 Internal Packages, Cycles, Workspaces, Proxy

```
myapp/
└── internal/         ← only myapp and its subpackages can import
    └── pkg/
```

A imports B (directly or indirectly) → B cannot import A. Fix by extracting shared code, merging packages, or introducing interfaces.

Workspaces (`go.work`):
```sh
go work init ./app
go work use ./lib
```
Edit multiple modules simultaneously. **Do not commit** `go.work`.

Module proxy: by default `go get` hits Google's proxy. Disable with `GOPROXY=direct` or set `GOPRIVATE`:
```sh
GOPRIVATE=*.example.com,company.com/repo
```

---

## 10. Go Tooling `#general`

### 10.1 `go run`

Compiles to temp dir, runs, deletes. Use for quick experiments.

### 10.2 `go install`

```sh
go install github.com/rakyll/hey@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
go install golang.org/x/vuln/cmd/govulncheck@latest
```

**Always include `@version` or `@latest`**. Without it, you get confusing behavior based on `go.mod` state.

Binaries go to `$GOBIN` (default `$HOME/go/bin`); add to `$PATH`.

### 10.3 `goimports`

```sh
go install golang.org/x/tools/cmd/goimports@latest
goimports -l -w .   # list and write-in-place
```

Like `go fmt` but also alphabetizes imports and removes unused ones.

### 10.4 Code-Quality Scanners

- **`go vet`** — built-in, mandatory.
- **`staticcheck`** (honnef.co) — 150+ checks, few false positives. Recommended first third-party tool.
- **`revive`** — golint successor, configurable.
- **`golangci-lint`** — meta-linter running 50+ tools.

Run all in CI: `staticcheck ./...` plus `golangci-lint run`.

### 10.5 `govulncheck`

```sh
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...
```

Scans deps + your call graph against a vulnerability database. Reports only reachable vulns.

### 10.6 Embedding

```go
import _ "embed"

//go:embed passwords.txt
var passwords string

//go:embed help
var helpInfo embed.FS

func main() {
    data, err := helpInfo.ReadFile("help/" + os.Args[1])
}
```

- Variable type: `string`, `[]byte`, or `embed.FS`.
- Variable must be **package-level**.
- `all:dir` includes hidden files; `dir/*` includes root hidden files only.

### 10.7 `go generate`

```go
//go:generate stringer -type=Direction
//go:generate protoc -I=. --go_out=. --go_opt=module=github.com/... person.proto
```

```sh
go generate ./...
```

Commit generated code to version control — readers see everything invoked.

### 10.8 Build Info

```go
import "runtime/debug"

info, ok := debug.ReadBuildInfo()
// info.Settings has GOOS, GOARCH, vcs.revision, etc.
```

```sh
$ go version -m mybinary
mybinary: go1.20
    path github.com/learning-go-book-2e/vulnerable
    build vcs=git
    build vcs.revision=623a65b...
```

### 10.9 Cross-Compilation

```sh
GOOS=linux GOARCH=arm64 go build
GOOS=windows GOARCH=amd64 go build
```

Valid values in `go help buildconstraint`.

### 10.10 Build Tags

```go
//go:build linux
//go:build !darwin && !linux
//go:build linux && amd64
//go:build go1.22
//go:build integration      ← custom tag, enable with -tags integration
```

Or use filename suffix: `something_linux_arm64.go`.

**Custom tag** for skipping experimental files:
```go
//go:build ignore
```

### 10.11 Secondary Go Versions

```sh
go install golang.org/dl/go1.19.2@latest
go1.19.2 download
go1.19.2 build
```

Uninstall: `rm -rf ~/sdk/go1.19.2 ~/go/bin/go1.19.2`.

---

## 11. Concurrency `#concurrency`

> Go's concurrency model is based on **Communicating Sequential Processes (CSP)** (Hoare, 1978).

### 11.1 When to Use Concurrency

Use concurrency when:
- Independent operations can run in parallel (I/O-bound).
- Multiple data streams need combining.
- Latency budget requires parallel fan-out.

Do NOT use when:
- Algorithm is in-memory and fast (overhead exceeds gain).
- Operations are inherently sequential.

**Concurrency ≠ Parallelism.** More goroutines don't automatically mean more speed (Amdahl's law).

### 11.2 Goroutines

A goroutine is a **lightweight thread managed by the Go runtime**. Each has its own stack that grows dynamically (2 KB → up to 1 GB).

```go
func process(val int) int { /* do something with val */ }

func processConcurrently(inVals []int) []int {
    in  := make(chan int, 5)
    out := make(chan int, 5)
    for i := 0; i < 5; i++ {
        go func() {
            for val := range in {
                out <- process(val)
            }
        }()
    }
    // ... load in, drain out
}
```

Business logic stays oblivious to concurrency — wrappers handle it.

### 11.3 Channels

```go
ch := make(chan int)        // unbuffered
ch := make(chan int, 10)   // buffered (capacity 10)

a := <-ch       // read
ch <- b         // write
```

**Directional types** enforce usage at compile time:
```go
func reader(ch <-chan int)       { <-ch }   // can only read
func writer(ch chan<- int)       { ch <- 1 } // can only write
```

**Unbuffered channels**: every write blocks until a read; every read blocks until a write. Synchronization.

**Buffered channels**: writes don't block until buffer is full; reads don't block until empty. Behavior:

| Operation | Unbuffered open | Unbuffered closed | Buffered open | Buffered closed | Nil |
|-----------|-----------------|-------------------|---------------|-----------------|-----|
| Read      | Pause until written | Return zero value (use `,ok`) | Pause if empty | Return buffered value; if empty, zero value | **Hang forever** |
| Write     | Pause until read  | **PANIC**         | Pause if full | **PANIC**       | **Hang forever** |
| Close     | Works            | **PANIC**         | Works        | **PANIC**       | **PANIC** |

### 11.4 `for-range` and Closing

```go
for v := range ch {
    fmt.Println(v)
}
// exits when ch is closed
```

```go
v, ok := <-ch   // ok = false after close
```

**Rules**:
- Closing is required only if someone is waiting via `for-range`.
- Writing goroutine closes; multiple writers → use `sync.WaitGroup` to close exactly once.

### 11.5 `select` — The Concurrency Control Structure

```go
select {
case v := <-ch1:
    fmt.Println(v)
case v := <-ch2:
    fmt.Println(v)
case ch3 <- x:
    fmt.Println("wrote", x)
case <-ch4:
    fmt.Println("got value on ch4, ignored")
}
```

**Critical**: if multiple cases are ready, `select` picks **randomly** (not by source order). This prevents starvation and the deadlock-from-lock-order bug.

```go
// DISABLE a case via nil channel:
for count := 0; count < 2; {
    select {
    case v, ok := <-in:
        if !ok { in = nil; count++; continue }
        // process v
    case v, ok := <-in2:
        if !ok { in2 = nil; count++; continue }
        // process v
    }
}
```

### 11.6 Goroutine Leaks — Always Clean Up

```go
// BAD — if consumer breaks early, goroutine blocks forever:
func countTo(max int) <-chan int {
    ch := make(chan int)
    go func() {
        for i := 0; i < max; i++ {
            ch <- i
        }
        close(ch)
    }()
    return ch
}
```

### 11.7 Context Cancellation

```go
func countTo(ctx context.Context, max int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; i < max; i++ {
            select {
            case <-ctx.Done():
                return
            case ch <- i:
            }
        }
    }()
    return ch
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    ch := countTo(ctx, 10)
    for i := range ch {
        if i > 5 { break }
        fmt.Println(i)
    }
}
```

### 11.8 `context.WithCancelCause`

```go
ctx, cancel := context.WithCancelCause(context.Background())
defer cancel(nil)
if errSomething {
    cancel(errors.New("bad status"))
}
fmt.Println(context.Cause(ctx))
```

### 11.9 Timeouts

```go
func timeLimit[T any](worker func() T, limit time.Duration) (T, error) {
    out := make(chan T, 1)
    ctx, cancel := context.WithTimeout(context.Background(), limit)
    defer cancel()
    go func() { out <- worker() }()
    select {
    case result := <-out:
        return result, nil
    case <-ctx.Done():
        var zero T
        return zero, errors.New("work timed out")
    }
}
```

Note: the worker **keeps running** after timeout — only context cancellation stops it.

### 11.10 `sync.WaitGroup`

```go
var wg sync.WaitGroup
wg.Add(3)
go func() { defer wg.Done(); doThing1() }()
go func() { defer wg.Done(); doThing2() }()
go func() { defer wg.Done(); doThing3() }()
wg.Wait()
```

**Pattern**: pass `WaitGroup` via **closure** (not parameter) to avoid copies.

**Closing exactly once with WaitGroup**:
```go
func processAndGather[T, R any](in <-chan T, processor func(T) R, num int) []R {
    out := make(chan R, num)
    var wg sync.WaitGroup
    wg.Add(num)
    for i := 0; i < num; i++ {
        go func() {
            defer wg.Done()
            for v := range in {
                out <- processor(v)
            }
        }()
    }
    go func() {
        wg.Wait()
        close(out)
    }()
    var result []R
    for v := range out {
        result = append(result, v)
    }
    return result
}
```

For "first-error wins": use `errgroup.Group` from `golang.org/x/sync/errgroup`.

### 11.11 `sync.Once` / `sync.OnceValue` (Go 1.21+)

```go
var parser SlowComplicatedParser
var once sync.Once

func Parse(data string) string {
    once.Do(func() { parser = initParser() })
    return parser.Parse(data)
}

// Go 1.21+ cleaner:
var initParserCached func() SlowComplicatedParser = sync.OnceValue(initParser)
```

`OnceFunc`, `OnceValue`, `OnceValues` differ by number of return values (0, 1, 2).

### 11.12 Backpressure with Buffered Channels

```go
type PressureGauge struct{ ch chan struct{} }

func New(limit int) *PressureGauge {
    return &PressureGauge{ch: make(chan struct{}, limit)}
}

func (pg *PressureGauge) Process(f func()) error {
    select {
    case pg.ch <- struct{}{}:
        f()
        <-pg.ch
        return nil
    default:
        return errors.New("no more capacity")
    }
}
```

### 11.13 Channels vs Mutexes — Decision Tree

Katherine Cox-Buday's rule (from *Concurrency in Go*):

1. **Coordinate goroutines or pass data between stages** → channels.
2. **Protect access to a struct field** → mutex.
3. **Critical perf issue with channels** → switch to mutex.

```go
type MutexScoreboardManager struct {
    l         sync.RWMutex
    scoreboard map[string]int
}
func (msm *MutexScoreboardManager) Update(name string, val int) {
    msm.l.Lock()
    defer msm.l.Unlock()
    msm.scoreboard[name] = val
}
func (msm *MutexScoreboardManager) Read(name string) (int, bool) {
    msm.l.RLock()
    defer msm.l.RUnlock()
    val, ok := msm.scoreboard[name]
    return val, ok
}
```

**`sync.Map`** is rarely the right choice — keys/values are `any`, only fits "write once, read many times" workloads.

### 11.14 Atomics & Race Detector

`sync/atomic` provides lock-free ops for CPU-level CAS. **Almost never needed** — use channels or mutexes.

```sh
go test -race ./...
go build -race           # instruments the binary (~10× slowdown)
```

The race detector doesn't catch every race, but when it does, fix it. **Never** fix races with sleeps.

---

## 12. Standard Library: io, time, encoding/json, net/http `#api`

### 12.1 `io.Reader` / `io.Writer`

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
```

**Why slice parameter (not `[]byte` return)?** Caller controls allocation. Reuse a single buffer.

```go
func countLetters(r io.Reader) (map[string]int, error) {
    buf := make([]byte, 2048)
    out := map[string]int{}
    for {
        n, err := r.Read(buf)
        for _, b := range buf[:n] {
            if (b >= 'A' && b <= 'Z') || (b >= 'a' && b <= 'a') {
                out[string(b)]++
            }
        }
        if err == io.EOF { return out, nil }
        if err != nil { return nil, err }
    }
}
```

- `io.EOF` is sentinel "end of data" — not a real error.
- `io.ErrUnexpectedEOF` for premature termination.
- `io.Copy(dst, src)`, `io.ReadAll(r)`, `io.MultiReader(rs...)`, `io.MultiWriter(ws...)`, `io.LimitReader(r, n)`, `io.NopCloser(r)`.

### 12.2 `time`

```go
d := 2*time.Hour + 30*time.Minute  // time.Duration = int64 nanoseconds
t := time.Now()
formatted := t.Format(time.RFC3339)
```

**Reference date**: `Mon Jan 2 15:04:05 MST 2006` (1, 2, 3, 4, 5, 6, 7 in sequence) — memorize once.

`time.Time` contains both wall and monotonic clocks. `Sub` uses monotonic when both instances have it.

**Timers**: `time.After(d)` returns a channel. `time.NewTicker(d)` is preferred over `time.Tick(d)` (Tickers can be stopped; Tick cannot).

### 12.3 `encoding/json`

**Struct tags**:
```go
type Order struct {
    ID          string    `json:"id"`
    DateOrdered time.Time `json:"date_ordered"`
    CustomerID  string    `json:"customer_id,omitempty"`   // omit if empty
    Items       []Item    `json:"items"`
}
type Item struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}
```

- `-` ignores a field.
- `omitempty` omits zero values (zero-length slices/maps count as empty; zero struct does not).

**Unmarshal/Marshal**:
```go
var o Order
err := json.Unmarshal([]byte(data), &o)
out, err := json.Marshal(o)
```

**Streaming**:
```go
dec := json.NewDecoder(strings.NewReader(streamData))
for {
    err := dec.Decode(&t)
    if errors.Is(err, io.EOF) { break }
    if err != nil { panic(err) }
    // process t
}
```

**Custom JSON parsing**:
```go
type RFC822ZTime struct{ time.Time }
func (rt RFC822ZTime) MarshalJSON() ([]byte, error) {
    out := rt.Time.Format(time.RFC822Z)
    return []byte(`"` + out + `"`), nil
}
func (rt *RFC822ZTime) UnmarshalJSON(b []byte) error {
    if string(b) == "null" { return nil }
    t, err := time.Parse(`"`+time.RFC822Z+`"`, string(b))
    if err != nil { return err }
    *rt = RFC822ZTime{t}
    return nil
}
```

**Trick to break infinite recursion in MarshalJSON**:
```go
func (o Order) MarshalJSON() ([]byte, error) {
    type Dup Order
    tmp := struct {
        DateOrdered string `json:"date_ordered"`
        Dup
    }{ Dup: (Dup)(o) }
    tmp.DateOrdered = o.DateOrdered.Format(time.RFC822Z)
    return json.Marshal(tmp)
}
```

### 12.4 `net/http` Client

**Always** create your own client with a timeout:
```go
client := &http.Client{ Timeout: 30 * time.Second }

req, err := http.NewRequestWithContext(ctx, http.MethodGet,
    "https://jsonplaceholder.typicode.com/todos/1", nil)
req.Header.Add("X-My-Client", "Learning Go")

res, err := client.Do(req)
defer res.Body.Close()

if res.StatusCode != http.StatusOK {
    panic(fmt.Sprintf("unexpected status: got %v", res.Status))
}

var data struct {
    UserID    int    `json:"userId"`
    ID        int    `json:"id"`
    Title     string `json:"title"`
    Completed bool   `json:"completed"`
}
err = json.NewDecoder(res.Body).Decode(&data)
```

Avoid `http.Get` / `http.Post` — they use the timeout-less `DefaultClient`.

### 12.5 `net/http` Server

```go
type Handler interface {
    ServeHTTP(http.ResponseWriter, *http.Request)
}

s := http.Server{
    Addr:         ":8080",
    ReadTimeout:  30 * time.Second,
    WriteTimeout: 90 * time.Second,
    IdleTimeout:  120 * time.Second,
    Handler:      HelloHandler{},
}
err := s.ListenAndServe()
if err != nil && err != http.ErrServerClosed {
    panic(err)
}
```

**Always set timeouts**. Default = no timeout.

### 12.6 `http.ServeMux` (Go 1.22+ Enhanced Patterns)

```go
mux := http.NewServeMux()
mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello!\n"))
})

// Go 1.22: methods + path wildcards:
mux.HandleFunc("GET /hello/{name}", func(w http.ResponseWriter, r *http.Request) {
    name := r.PathValue("name")
    fmt.Fprintf(w, "Hello, %s!\n", name)
})

// Nested muxes with prefix stripping:
person := http.NewServeMux()
person.HandleFunc("/greet", func(w http.ResponseWriter, r *http.Request) { w.Write([]byte("greetings!\n")) })
dog := http.NewServeMux()
dog.HandleFunc("/greet", func(w http.ResponseWriter, r *http.Request) { w.Write([]byte("good puppy!\n")) })
mux := http.NewServeMux()
mux.Handle("/person/", http.StripPrefix("/person", person))
mux.Handle("/dog/",    http.StripPrefix("/dog",    dog))
```

Avoid `http.DefaultServeMux`, `http.Handle*`, `http.ListenAndServe*` outside trivial demos.

### 12.7 Middleware & ResponseController

```go
func RequestTimer(h http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        h.ServeHTTP(w, r)
        slog.Info("request time", "path", r.URL.Path, "duration", time.Since(start))
    })
}

func TerribleSecurityProvider(password string) func(http.Handler) http.Handler {
    return func(h http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            if r.Header.Get("X-Secret-Password") != password {
                w.WriteHeader(http.StatusUnauthorized)
                return
            }
            h.ServeHTTP(w, r)
        })
    }
}

// Composition:
mux.Handle("/hello", terribleSecurity(RequestTimer(http.HandlerFunc(handler))))
wrappedMux := terribleSecurity(RequestTimer(mux))
```

**`http.ResponseController`** — handles optional ResponseWriter methods without breaking the interface:
```go
rc := http.NewResponseController(rw)
err := rc.Flush()
if err != nil && !errors.Is(err, http.ErrNotSupported) {
    slog.Error("error flushing", "msg", err)
    return
}
```

### 12.8 `log/slog` (Structured Logging, Go 1.21+)

```go
slog.Info("user login", "id", userID, "login_count", loginCount)
// 2023/04/20 23:36:38 INFO user login id=fred login_count=20

options := &slog.HandlerOptions{Level: slog.LevelDebug}
handler := slog.NewJSONHandler(os.Stderr, options)
mySlog := slog.New(handler)

mySlog.LogAttrs(ctx, slog.LevelInfo, "faster logging",
    slog.String("id", userID),
    slog.Time("last_login", lastLogin))
// {"time":"...","level":"INFO","msg":"...","id":"fred","last_login":"..."}

myLog := slog.NewLogLogger(mySlog.Handler(), slog.LevelDebug)  // bridge from log
```

---

## 13. Context `#concurrency` `#api`

### 13.1 The Interface

```go
type Context interface {
    Deadline() (deadline time.Time, ok bool)
    Done() <-chan struct{}
    Err() error
    Value(key any) any
}
```

**Convention**: first parameter named `ctx`. Acquire from `context.Background()` or `context.TODO()` at entry points; wrap as it flows down.

### 13.2 Cancellation

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()                       // ALWAYS — resource leak otherwise
ch := make(chan string)
var wg sync.WaitGroup
wg.Add(2)

go func() {
    defer wg.Done()
    for {
        resp, err := makeRequest(ctx, "http://httpbin.org/status/200,200,200,500")
        if err != nil { cancel(); return }
        if resp.StatusCode == http.StatusInternalServerError { cancel(); return }
        select {
        case ch <- "success":
        case <-ctx.Done(): return
        }
    }
}()

loop:
for {
    select {
    case s := <-ch:
        fmt.Println("in main:", s)
    case <-ctx.Done():
        fmt.Println("cancelled:", context.Cause(ctx))
        break loop
    }
}
wg.Wait()
```

`context.WithCancelCause(ctx)` lets you pass an error to `cancel(err)`, retrievable via `context.Cause(ctx)`.

### 13.3 Timeouts, Deadlines, Values

```go
ctx, cancel := context.WithTimeout(ctx, 50*time.Millisecond)
defer cancel()
// WithDeadline(ctx, time.Time) — similar but absolute.
```

**Nesting**: child timeout is bounded by parent. Parent 2s, child 3s → child cancels after 2s.

`ctx.Err()` returns `nil` while active, else `context.Canceled` or `context.DeadlineExceeded`.

**Context values** — use sparingly:
```go
type userKey int
const key userKey = iota

func ContextWithUser(ctx context.Context, user string) context.Context {
    return context.WithValue(ctx, key, user)
}
func UserFromContext(ctx context.Context) (string, bool) {
    user, ok := ctx.Value(key).(string)
    return user, ok
}
```

**Rules**:
- Uniqueness: use unexported type (`type userKey int` or `type userKey struct{}`) for the key.
- Naming: `ContextWithX` for setters, `XFromContext` for getters.
- `Value` lookup is **linear** through the chain — don't store dozens of values.
- **Don't** pass business data through context. Copy into explicit parameters.
- **Do** pass metadata (request IDs, auth info) that crosses API boundaries invisibly.

For HTTP requests, the context is retrieved from `req.Context()`.

---

## 14. Testing `#testing`

### 14.1 Basics

```go
// adder.go
func addNumbers(x, y int) int { return x + x }   // bug: should be x + y

// adder_test.go
func Test_addNumbers(t *testing.T) {
    result := addNumbers(2, 3)
    if result != 5 { t.Error("incorrect result: expected 5, got", result) }
}
```

Files named `*_test.go`, package = same as code under test (or `package_test` for public-API testing).

### 14.2 Reporting Failures & Setup

| Method        | Effect                                    |
|---------------|-------------------------------------------|
| `t.Error`     | Mark failure, continue                    |
| `t.Errorf`    | Same with format string                   |
| `t.Fatal`     | Mark failure, **stop current test**      |
| `t.Fatalf`    | Same with format                          |

Use `Error` for independent checks; `Fatal` when further checks are doomed.

**`TestMain`** (once per package), **`t.Cleanup`** (LIFO), **`t.TempDir()`**, **`t.Setenv(key, value)`** all provide auto-revert setup/teardown.

### 14.3 Testing Public API & `testdata/`

```go
package pubadder_test    // _test suffix forces black-box testing

import (
    "github.com/learning-go-book-2e/ch15/sample_code/pubadder"
    "testing"
)

func TestAddNumbers(t *testing.T) {
    result := pubadder.AddNumbers(2, 3)
    if result != 5 { t.Error(...) }
}
```

Files in `testdata/` are accessible from tests via relative paths; Go reserves this name.

### 14.4 `go-cmp`

```go
import "github.com/google/go-cmp/cmp"

func TestCreatePerson(t *testing.T) {
    expected := Person{Name: "Dennis", Age: 37}
    result := CreatePerson("Dennis", 37)
    if diff := cmp.Diff(expected, result); diff != "" {
        t.Error(diff)
    }
}
```

Output shows line-by-line diff with `-` / `+` markers. Custom comparator (skip fields):
```go
comparer := cmp.Comparer(func(x, y Person) bool {
    return x.Name == y.Name && x.Age == y.Age
})
cmp.Diff(expected, result, comparer)
```

### 14.5 Table Tests

```go
data := []struct {
    name        string
    num1, num2  int
    op          string
    expected    int
    errMsg      string
}{
    {"addition",       2, 2, "+", 4, ""},
    {"subtraction",    2, 2, "-", 0, ""},
    {"multiplication", 2, 2, "*", 4, ""},
    {"division",       2, 2, "/", 1, ""},
    {"bad_division",   2, 0, "/", 0, `division by zero`},
    {"bad_op",         2, 2, "?", 0, `unknown operator ?`},
}
for _, d := range data {
    t.Run(d.name, func(t *testing.T) {
        result, err := DoMath(d.num1, d.num2, d.op)
        // assert result == d.expected and errMsg == d.errMsg
    })
}
```

Each entry gets a name: `--- PASS: TestDoMath/addition`.

### 14.6 Parallel Tests

```go
func TestMyCode(t *testing.T) {
    t.Parallel()
}
```

**Pre-Go 1.22 trap** — same loop variable captured by all parallel subtests. **Fix**: shadow `d := d`, or pass `d` as parameter, or upgrade to Go 1.22.

### 14.7 Code Coverage

```sh
go test -v -cover -coverprofile=c.out
go tool cover -html=c.out   # browser with green/red highlighting
```

**Coverage ≠ correctness** — 100% coverage still allows bugs (the `DoMath` example has `*` implemented as `+` and 100% coverage doesn't catch it).

### 14.8 Fuzzing (Go 1.18+)

```go
func FuzzParseData(f *testing.F) {
    testcases := [][]byte{
        []byte("3\nhello\ngoodbye\ngreetings\n"),
        []byte("0\n"),
    }
    for _, tc := range testcases { f.Add(tc) }

    f.Fuzz(func(t *testing.T, in []byte) {
        r := bytes.NewReader(in)
        out, err := ParseData(r)
        if err != nil { t.Skip("handled error") }
        out2, err := ParseData(bytes.NewReader(ToData(out)))
        if diff := cmp.Diff(out, out2); diff != "" { t.Error(diff) }
    })
}
```

Each failure is auto-saved as a **seed corpus entry** in `testdata/fuzz/` — becomes a regression test. ⚠️ Fuzzing consumes gigabytes of resources.

### 14.9 Benchmarks

```go
var blackhole int  // prevent compiler from optimizing away the call

func BenchmarkFileLen1(b *testing.B) {
    for i := 0; i < b.N; i++ {
        result, err := FileLen("testdata/data.txt", 1)
        if err != nil { b.Fatal(err) }
        blackhole = result
    }
}
```

```sh
$ go test -bench=. -benchmem
BenchmarkFileLen/FileLen-1-12     25 47201025 ns/op  65342 B/op 65208 allocs/op
BenchmarkFileLen/FileLen-1000-12 16491   71281 ns/op  68744 B/op    70 allocs/op
```

Columns: `name-GOMAXPROCS`, `N` (runs), `ns/op`, `B/op`, `allocs/op`.

**Sub-benchmarks** via `b.Run`.

### 14.12 Stubs

**Small interface — inline implementation**:
```go
type MathSolverStub struct{}
func (ms MathSolverStub) Resolve(_ context.Context, expr string) (float64, error) {
    switch expr {
    case "2 + 2 * 10":   return 22, nil
    case "( 2 + 2 ) * 10": return 40, nil
    case "( 2 + 2 * 10":  return 0, errors.New("invalid expression")
    }
    return 0, nil
}
```

**Large interface — embed the interface** (unimplemented methods panic):
```go
type Entities interface {
    GetUser(id string) (User, error)
    GetPets(userID string) ([]Pet, error)
    // ...
}
type GetPetNamesStub struct { Entities }
func (ps GetPetNamesStub) GetPets(userID string) ([]Pet, error) {
    switch userID {
    case "1": return []Pet{{Name: "Bubbles"}}, nil
    case "2": return []Pet{{Name: "Stampy"}, {Name: "Snowball II"}}, nil
    default: return nil, fmt.Errorf("invalid id: %s", userID)
    }
}
```

**Per-test variation — function fields**:
```go
type EntitiesStub struct {
    getUser func(id string) (User, error)
    getPets func(userID string) ([]Pet, error)
    // ...
}
func (es EntitiesStub) GetPets(userID string) ([]Pet, error) { return es.getPets(userID) }
// In test:
l := Logic{Entities: EntitiesStub{getPets: d.getPets}}
```

### 14.13 `httptest`

```go
server := httptest.NewServer(http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
    expression := req.URL.Query().Get("expression")
    if expression != io.expression {
        rw.WriteHeader(http.StatusBadRequest)
        return
    }
    rw.WriteHeader(io.code)
    rw.Write([]byte(io.body))
}))
defer server.Close()

rs := RemoteSolver{MathServerURL: server.URL, Client: server.Client()}
```

### 14.14 Integration Tests with Build Tags

```go
//go:build integration

package solver

func TestRemoteSolver_ResolveIntegration(t *testing.T) {
    // hits real service via docker
}
```

```sh
go test -tags integration ./...
```

Alternative: use environment variable check + `t.Skip` for discoverability.

### 14.15 Data Race Detector

```sh
go test -race ./...
go build -race           # ~10× slower; use in CI
```

**Never** fix races by inserting sleeps — fix them with proper synchronization.

---

## 15. Reflection, Unsafe, Cgo `#general`

### 15.1 Reflection (`reflect`)

Used at program boundaries — serialization, configuration, templates. **Slower, fragile, verbose**. Many operations panic on type mismatch.

**Core types**:
```go
t := reflect.TypeOf(v)         // describes the type
v := reflect.ValueOf(v)        // describes the value
k := t.Kind()                  // reflect.Kind constant (Struct, Slice, Int, ...)
```

**Inspecting structs and tags**:
```go
type Foo struct {
    A int    `myTag:"value"`
    B string `myTag:"value2"`
}
var f Foo
ft := reflect.TypeOf(f)
for i := 0; i < ft.NumField(); i++ {
    cur := ft.Field(i)
    fmt.Println(cur.Name, cur.Type.Name(), cur.Tag.Get("myTag"))
}
```

**Setting via reflection** (must use pointer indirection):
```go
i := 10
iv := reflect.ValueOf(&i).Elem()
iv.SetInt(20)
// i is now 20
```

**Creating new values**:
```go
var stringSliceType = reflect.TypeOf([]string(nil))
ssv := reflect.MakeSlice(stringSliceType, 0, 10)
sv := reflect.New(stringType).Elem()
sv.SetString("hello")
ssv = reflect.Append(ssv, sv)
```

**Detecting nil interface value**:
```go
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
```

**Performance**: reflection `Filter` is **~50× slower** than generic:
```
BenchmarkFilterReflectString-8    5870   203962 ns/op   46616 B/op   2219 allocs/op
BenchmarkFilterGenericString-8  294355     3920 ns/op   16384 B/op      1 allocs/op
```

Use reflection only when type is truly unknown at compile time.

### 15.2 `unsafe`

Key API:
- `unsafe.Sizeof(v)` — bytes occupied.
- `unsafe.Offsetof(struct{Field})` — byte offset.
- `unsafe.Pointer` — bridge between pointer types.
- `unsafe.Add(ptr, n)` — pointer arithmetic.
- `unsafe.Slice(ptr, len)` / `unsafe.SliceData(s)` — slice over raw memory (Go 1.17+).
- `unsafe.String(ptr, len)` / `unsafe.StringData(s)` — string views (Go 1.20+).

**Field order affects size**:
```go
type BoolIntBool struct { b bool; i int64; b2 bool }   // 24 bytes (padding both sides)
type BoolBoolInt struct { b bool; b2 bool; i int64 }   // 16 bytes (group bools)
```

**Binary protocol deserialization**:
```go
type Data struct {
    Value  uint32    // 4 bytes
    Label  [10]byte  // 10 bytes
    Active bool      // 1 byte
}
const dataSize = unsafe.Sizeof(Data{})   // legal in const expression

func DataFromBytesUnsafe(b [dataSize]byte) Data {
    data := *(*Data)(unsafe.Pointer(&b))
    if isLE { data.Value = bits.ReverseBytes32(data.Value) }
    return data
}
```

~2–2.5× faster than safe code. **Use sparingly.**

**Accessing unexported fields**:
```go
sf, _ := reflect.TypeOf(huf).Elem().FieldByName("b")
pos := unsafe.Add(unsafe.Pointer(huf), sf.Offset)
b := (*bool)(pos)
*b = true   // bypasses visibility
```

Runtime check: `go build -gcflags=-d=checkptr`.

### 15.3 Cgo

`import "C"` is a magic import exposing C functions/types declared in the comment block above.

```go
package main
/*
#cgo LDFLAGS: -lm
#include <stdio.h>
#include <math.h>
#include "mylib.h"

int add(int a, int b) {
    int sum = a + b;
    printf("a: %d, b: %d, sum %d\n", a, b, sum);
    return sum;
}
*/
import "C"

func main() {
    sum := C.add(3, 2)
    fmt.Println(sum)
    fmt.Println(C.sqrt(100))
}
```

**Exporting Go to C**:
```go
//export doubler
func doubler(i int) int { return i * 2 }
```
Then in `.c` file:
```c
#include "_cgo_export.h"
int add(int a, int b) {
    int doubleA = doubler(a);
    return doubleA + b;
}
```

**Passing pointer-containing types** — use `cgo.Handle`:
```go
//export processor
func processor(handle C.uintptr_t) {
    h := cgo.Handle(handle)
    p := h.Value().(Person)
    fmt.Println(p.Name, p.Age)
    h.Delete()
}
// Call site: C.in_c(C.uintptr_t(cgo.NewHandle(p)))
```

**Performance**: cgo calls are **~29–40× slower** than pure C function calls. Use cgo for **integration with C libraries you cannot replace**, not for performance.

---

## Closing Notes (Idiomatic Go Themes)

The book's recurring philosophy:

1. **Clarity over cleverness** — explicit, readable code wins.
2. **Composition over inheritance** — embed structs; use interfaces.
3. **Accept interfaces, return structs** — flexibility at boundaries, stability in outputs.
4. **Errors are values** — wrap with `%w`, inspect with `Is`/`As`, prefer errors over panics.
5. **Concurrency is implementation detail** — keep it out of your APIs.
6. **Less is more** — Go deliberately omits exceptions, inheritance, operator overloading, named params — minimalism is a feature.

> "Properly written, Go is boring. Well-written Go programs tend to be straightforward and sometimes a bit repetitive." — Jon Bodner

That repetition is the price of clarity — and the engine of long-term maintainability.