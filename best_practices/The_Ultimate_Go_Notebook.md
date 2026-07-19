# The Ultimate Go Notebook
**Author:** William Kennedy with Hoanh An
**Topic tags:** `#general` `#go` `#concurrency` `#testing` `#performance`
**Language focus:** Go-first
**Sources:** `markdown_output/The_ultimate_Go_Notebook_-_WIlliam_Kennedy/The_ultimate_Go_Notebook_-_WIlliam_Kennedy.md` · `summaries/The_ultimate_Go_Notebook_-_WIlliam_Kennedy.md`

## TL;DR
Kennedy's notebook is a mechanically-sympathetic, data-oriented tour of Go: language mechanics, data structures, decoupling, concurrency, testing, benchmarking, generics, profiling, and tracing. Two threads run throughout: (1) every value decision is a value-vs-pointer semantics decision (and once you switch to pointer semantics you can never go back); (2) never guess about performance — measure, profile, then test. Correctness → readability → simplicity → performance, in that order.

---

## Best Practices by Topic

---

### Design Philosophy — Integrity First
`#general`

**Principle:** Integrity (micro: memory/type correctness; macro: data transformations/error handling) is the highest-priority design value. 92% of critical failures stem from bad error handling.

**Do:**
- Write less code (industry average: 15–50 bugs per 1,000 LOC).
- Check every error the moment it is returned.
- Handle errors at the macro level: log with context, decide recover/continue/shutdown.

**Don't:**
- Add abstractions "just in case" — design concrete first, discover interfaces.
- Guess about performance — measure.

*Ref: The_Ultimate_Go_Notebook.md — "Introduction / Design Philosophy"*

---

### Design Philosophy — The Four Priorities In Order
`#general`

**Principle:** Prioritize in this exact order: Integrity → Readability → Simplicity → Performance.

**Do:**
- Make code correct first, then clear, then concise, then fast.
- Refactor in cycles: readability, efficiency, abstraction, testability.
- Be a "programmer" (concrete, prototype) then switch to "engineer" (refactor).

**Don't:**
- Optimize prematurely — you can only optimize what you can measure.
- Trade readability for cleverness.

*Ref: The_Ultimate_Go_Notebook.md — "Productivity vs Performance" / "Correctness vs Performance"*

---

### Language Mechanics — Zero Value Concept
`#go`

**Principle:** Every value is initialized to its zero value (all bits zero) unless explicitly initialized. This guarantees data integrity.

| Type    | Zero Value |
|---------|-----------|
| Boolean | `false`   |
| Integer | `0`       |
| Float   | `0`       |
| Complex | `0i`      |
| String  | `""`      |
| Pointer | `nil`     |

**Do:**
- Use `var` for zero-value construction.
- Use `:=` with `{}` for non-zero-value construction.

**Code:**
```go
var a int
var b string
var c float64
var d bool
fmt.Printf("var a int \t %T [%v]\n", a, a)
fmt.Printf("var b string \t %T [%v]\n", b, b)
fmt.Printf("var c float64 \t %T [%v]\n", c, c)
fmt.Printf("var d bool \t %T [%v]\n\n", d, d)
// Output:
// var a int int [0]
// var b string string []
// var c float64 float64 [0]
// var d bool bool [false]
```
*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Declare and Initialize"*

**Code (short declaration for non-zero):**
```go
aa := 10       // int [10]
bb := "hello"  // string [hello]
cc := 3.14159  // float64 [3.14159]
dd := true     // bool [true]
```
*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Declare and Initialize"*

---

### Language Mechanics — Strings Are Two-Word Headers
`#go` `#performance`

**Principle:** A `string` is a two-word data structure (pointer to backing byte array + length). Copying a string is always a two-word copy regardless of its size.

**Do:**
- Pass strings by value freely; the cost is constant.
- Remember assignment shares the backing byte array (immutable).

**Don't:**
- Worry about string size when passing — worry about allocation when constructing.

*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Strings"*

---

### Language Mechanics — Conversion, Not Casting
`#go`

**Principle:** Go has conversion (`T(v)`), not casting. Bytes are copied to a new memory location for the new representation.

**Code:**
```go
aaa := int32(10)
fmt.Printf("aaa := int32(10) %T [%v]\n", aaa, aaa)
// Output: aaa := int32(10) int32 [10]
```
*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Conversion vs Casting"*

**Don't:** Reach for `unsafe` to cast. Be honest about why you would.

---

### Language Mechanics — Struct Construction
`#go`

**Principle:** Use literal construction for non-zero values; `var` for zero.

**Code:**
```go
type example struct {
    flag    bool
    counter int16
    pi      float32
}
// Zero value
var e1 example
fmt.Printf("%+v\n", e1)
// {flag:false counter:0 pi:0}

// Non-zero value
e2 := example{
    flag:    true,
    counter: 10,
    pi:      3.141592,
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Struct and Construction Mechanics"*

**Code (anonymous struct):**
```go
e3 := struct {
    flag    bool
    counter int16
    pi      float32
}{
    flag:    true,
    counter: 10,
    pi:      3.141592,
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Language Mechanics / Struct and Construction Mechanics"*

---

### Language Mechanics — Padding and Alignment (Lay Out Fields Largest First)
`#go` `#performance`

**Principle:** The compiler pads fields to alignment boundaries. Lay fields out from largest allocation to smallest to minimize padding bytes.

**Code (12 bytes — bad order):**
```go
type example2 struct {
    flag    bool
    counter int16
    flag2   bool
    pi      float32
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Padding and Alignment"*

**Code (8 bytes — reordered):**
```go
type example struct {
    pi      float32 // 0xc000100020 <- Starting Address
    counter int16   // 0xc000100024 <- 2 byte alignment
    flag    bool    // 0xc000100026 <- 1 byte alignment
    flag2   bool    // 0xc000100027 <- 1 byte alignment
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Padding and Alignment"*

**Do:** Largest-field-first ordering eliminates padding.

**Don't:** Arbitrarily order fields; the largest field defines the struct's alignment boundary.

---

### Language Mechanics — Pointers Are For Sharing
`#go`

**Principle:** Pointers share values across program boundaries (function calls, goroutines). If the word "share" isn't in your mouth, you don't need a pointer. Each goroutine starts with a 2KB stack; stack frames are sized at compile time.

**Code:**
```go
func main() {
    count := 10
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
    increment1(count)
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")

    increment2(&count)
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
}

func increment1(inc int) {
    inc++
    println("inc1:\tValue Of[", inc, "]\tAddr Of[", &inc, "]")
}

func increment2(inc *int) {
    *inc++
    println("inc2:\tValue Of[", inc, "]\tAddr Of[", &inc, "]\tPoints To[", *inc, "]")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Pass By Value"*

**Do:** Read `&` as "sharing" to preserve readability.
**Don't:** Confuse pass-by-pointer with pass-by-reference — addresses are still copied by value.

---

### Language Mechanics — Escape Analysis (Stack vs Heap)
`#go` `#performance`

**Principle:** Escape analysis decides where a value is constructed. The question is **ownership**: must this value exist after the constructing function returns? If no → stack; if yes → heap. Only heap construction counts as an allocation.

**Code (stays on stack):**
```go
type user struct {
    name  string
    email string
}

func stayOnStack() user {
    u := user{
        name:  "Bill",
        email: "bill@email.com",
    }
    return u
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

**Code (escapes to heap):**
```go
type user struct {
    name  string
    email string
}

func escapeToHeap() *user {
    u := user{
        name:  "Bill",
        email: "bill@email.com",
    }
    return &u
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

**Do:** Use value returns when the caller only needs a copy.
**Don't:** Return `&` of a local unless you accept the heap cost.

---

### Language Mechanics — Stack Growth and Contiguous Stacks
`#go`

**Principle:** Go uses contiguous stacks. Before each function call, a preamble checks for enough space; if not, a new larger stack is allocated and memory is copied. No goroutine may hold a pointer into another goroutine's stack (too costly to track on growth).

**Code (size-based heap allocation):**
```go
b := make([]byte, size) // Backing array allocates on the heap.
```
*Ref: The_Ultimate_Go_Notebook.md — "Stack Growth"*

---

### Language Mechanics — Constants: Typed vs Untyped (Kind)
`#go`

**Principle:** Constants are typed or untyped (kind). Untyped numeric constants have 256-bit precision; kind promotion handles mixed-kind arithmetic at compile time.

**Code:**
```go
const ui = 1234567890     // kind: integer
const uf = 3.141592       // kind: floating-point

const ti int = 1234567890 // type: int
const tf float64 = 3.141592 // type: float64

const myUint8 uint8 = 1000 // Compiler Error: constant 1000 overflows uint8

var answer = 3 * 0.333     // KindFloat * KindFloat
const third = 1 / 3.0       // KindFloat
const zero = 1 / 3          // KindInt = 0 (integer division)
const one int8 = 1
const two = 2 * one         // int8(2) * int8(1) -> type int8
const bigger = 9223372036854775808543522345 // fits in kind int (256-bit)
```
*Ref: The_Ultimate_Go_Notebook.md — "Constants"*

---

### Language Mechanics — IOTA for Successive Constants
`#go`

**Principle:** `iota` starts at 0 in a const block and increments by 1 per line. Math applied is reapplied with the incrementing iota. Great for bit-shift flag patterns.

**Code:**
```go
const (
    A1 = iota // 0
    B1        // 1
    C1        // 2
)

const (
    A3 = iota + 1 // 1
    B3            // 2
    C3            // 3
)

const (
    Ldate         = 1 << iota // 1  : 0000 0001
    Ltime                     // 2  : 0000 0010
    Lmicroseconds             // 4  : 0000 0100
    Llongfile                 // 8  : 0000 1000
    Lshortfile                // 16 : 0001 0000
    LUTC                      // 32 : 0010 0000
)
```
*Ref: The_Ultimate_Go_Notebook.md — "IOTA"*

---

### Data Structures — CPU Cache Latencies and Cache Lines
`#performance`

**Principle:** Performance today is about getting data into the processor efficiently. Cache lines are 64 bytes. Predictable linear traversals let the hardware prefetcher fill caches before instructions need the data.

```
1 ns  ........... 1 ns .......... 12 instructions (one)
1 µs  ......... 1,000 ns ........ 12,000 instructions (thousand)
1 ms  ..... 1,000,000 ns ....... 12,000,000 instructions (million)
1 s   .. 1,000,000,000 ns ...... 12,000,000,000 instructions (billion)

Industry Defined Latencies
L1 cache reference ......... 0.5 ns  ...... 6 ins
L2 cache reference ......... 7 ns   ...... 84 ins
Main memory reference ...... 100 ns ...... 1200 ins
```
*Ref: The_Ultimate_Go_Notebook.md — "CPU Caches"*

**Do:** Prefer contiguous memory + linear traversal.
**Don't:** Use pointer-chasing data structures (linked lists, trees of pointers) when cache-friendly arrays suffice.

---

### Data Structures — Row vs Column Traversal (Matrix)
`#performance`

**Principle:** Row traversal walks cache-line by cache-line (fast). Column traversal crosses OS page boundaries (slow). Linked-list traversal sits between because nodes cluster in pages but cache lines still miss.

**Code:**
```go
func RowTraverse() int {
    var ctr int
    for row := 0; row < rows; row++ {
        for col := 0; col < cols; col++ {
            if matrix[row][col] == 0xFF {
                ctr++
            }
        }
    }
    return ctr
}

func ColumnTraverse() int {
    var ctr int
    for col := 0; col < cols; col++ {
        for row := 0; row < rows; row++ {
            if matrix[row][col] == 0xFF {
                ctr++
            }
        }
    }
    return ctr
}

func LinkedListTraverse() int {
    var ctr int
    d := list
    for d != nil {
        if d.v == 0xFF {
            ctr++
        }
        d = d.p
    }
    return ctr
}
```
*Ref: The_Ultimate_Go_Notebook.md — "CPU Caches"*

```
BenchmarkLinkListTraverse-16   128   28738407 ns/op
BenchmarkColumnTraverse-16      30  126878630 ns/op
BenchmarkRowTraverse-16        310   11060883 ns/op
```
*Ref: The_Ultimate_Go_Notebook.md — "CPU Caches"*

---

### Data Structures — Translation Lookaside Buffer (TLB)
`#performance`

**Principle:** The TLB caches virtual→physical address translations. TLB misses cause large latencies because the OS must scan page tables. For memory-intensive apps (DNA, large matrices), consider Linux distributions with 1–2 MB huge pages.

*Ref: The_Ultimate_Go_Notebook.md — "Translation Lookaside Buffer (TLB)"*

---

### Data Structures — Iterating With Value vs Pointer Semantics
`#go` `#performance`

**Principle:** `for i, v := range xs` copies the collection and gives a copy of each element. `for i := range xs` accesses elements directly via index. For arrays the value-semantic copy can be expensive; for slices only the header is copied.

**Code:**
```go
// Value Semantic Iteration
for i, fruit := range strings {
    println(i, fruit)
}

// Pointer Semantic Iteration
for i := range strings {
    println(i, strings[i])
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Iterating Over Collections"*

---

### Data Structures — Array Type Identity Includes Size
`#go`

**Principle:** The size of an array is part of its type. `[4]int` and `[5]int` are different types and cannot be assigned to each other.

**Code:**
```go
var five [5]int
four := [4]int{10, 20, 30, 40}
five = four
// Compiler Error: cannot use four (type [4]int) as type [5]int in assignment
```
*Ref: The_Ultimate_Go_Notebook.md — "Different Type Arrays"*

**Code (proving contiguous layout):**
```go
five := [5]string{"Annie", "Betty", "Charley", "Doug", "Bill"}
for i, v := range five {
    fmt.Printf("Value[%s]\tAddress[%p] IndexAddr[%p]\n",
        v, &v, &five[i])
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Contiguous Memory Construction"*

---

### Data Structures — Constructing Slices
`#go`

**Principle:** A slice is a three-word header (pointer, length, capacity). The built-in `make` lets you pre-allocate length and capacity.

**Code:**
```go
// Several ways to construct a slice:
var slice []string            // zero value (nil)
slice := []string{}            // empty
slice := make([]string, 5)     // len=5, cap=5
slice := make([]string, 5, 8)  // len=5, cap=8
slice := []string{"A", "B", "C", "D", "E"} // literal
```
*Ref: The_Ultimate_Go_Notebook.md — "Constructing Slices"*

**Code (length vs capacity, out-of-range panic):**
```go
slice := make([]string, 5)
slice[0] = "Apple"
slice[1] = "Orange"
slice[2] = "Banana"
slice[3] = "Grape"
slice[4] = "Plum"

slice[5] = "Raspberry"
// panic: runtime error: index out of range slice[5] = "Runtime error"
```
*Ref: The_Ultimate_Go_Notebook.md — "Slice Length vs Capacity"*

---

### Data Structures — Append Uses Value-Semantic Mutation
`#go` `#performance`

**Principle:** `append` takes its own copy of the slice header, mutates it, and returns a copy. Always reassign: `s = append(s, x)`. Growth: doubles up to 1024 elements, then grows by 25%.

**Code:**
```go
var data []string
for record := 1; record <= 102400; record++ {
    data = append(data, fmt.Sprintf("Rec: %d", record))
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Appending With Slices"*

**Do:** Always assign the result of `append` back to a variable.
**Don't:** Assume the backing array is unchanged after an append that exceeds capacity.

---

### Data Structures — Slicing Shares the Backing Array
`#go`

**Principle:** Slice operations create new headers that share the underlying array. Mutations through one view affect all views whose length covers that index.

**Code:**
```go
slice1 := []string{"A", "B", "C", "D", "E"}
slice2 := slice1[2:4]
slice2[0] = "CHANGED"
// slice1[2] is now "CHANGED"
```
*Ref: The_Ultimate_Go_Notebook.md — "Slicing Slices"*

**Code (three-index slice to prevent append side effects):**
```go
slice1 := []string{"A", "B", "C", "D", "E"}
slice2 := slice1[2:4:4] // length=2, capacity=2
slice2 = append(slice2, "CHANGED")
// slice1 unchanged because slice2 got a new backing array
```
*Ref: The_Ultimate_Go_Notebook.md — "Slicing Slices"*

**Do:** Use `[a:b:c]` (three-index slicing) to isolate capacity when appending into a sub-slice.

---

### Data Structures — Append Replaces Backing Arrays (Stale Pointers)
`#go`

**Principle:** When `append` grows the backing array, old pointers to elements of the previous array become stale. Cache results in a struct field if you need stable sharing.

**Code:**
```go
users := make([]user, 1)
ptrUsr0 := &users[0]
ptrUsr0.likes++
// Output: User: 0 Likes: 1

users = append(users, user{})
ptrUsr0.likes++
// Output: User: 0 Likes: 1  (NOT 2 — pointer is into the OLD backing array)
```
*Ref: The_Ultimate_Go_Notebook.md — "Slices Use Pointer Semantic Mutation"*

**Don't:** Cache pointers into individual slice elements when the slice may be appended later.

---

### Data Structures — Manual Slice Copy
`#go`

**Code:**
```go
slice1 := []string{"A", "B", "C", "D", "E"}
slice3 := make([]string, len(slice1))
copy(slice3, slice1)
// slice3 now has its own backing array
```
*Ref: The_Ultimate_Go_Notebook.md — "Copying Slices Manually"*

---

### Data Structures — UTF-8, Runes, and Code Points
`#go`

**Principle:** Go source is UTF-8. A `rune` (alias for `int32`) is a code point (1–4 bytes). Iterating a string with `range` advances code point by code point.

**Code:**
```go
var buf [utf8.UTFMax]byte

for i, r := range s {
    rl := utf8.RuneLen(r)
    si := i + rl
    copy(buf[:], s[i:si])
    fmt.Printf("%2d: %q; codepoint: %#6x; encoded bytes: %#v\n",
        i, r, r, buf[:rl])
}
```
*Ref: The_Ultimate_Go_Notebook.md — "UTF-8"*

---

### Data Structures — Maps: Construction, Lookup, Delete
`#go`

**Principle:** Maps use a hash + bucket system. A nil map panics on use. Map iteration order is undefined (and randomized for larger maps). Keys must be comparable.

**Code:**
```go
type user struct {
    name     string
    username string
}

// Zero value map — panics on use.
var users map[string]user

// Constructed maps.
users := make(map[string]user)
users := map[string]user{}

users["Roy"] = user{"Rob", "Roy"}
users["Ford"] = user{"Henry", "Ford"}

// Key lookup returns value + existence flag.
user1, exists1 := users["Bill"]
user2, exists2 := users["Ford"]

// Delete by key.
delete(users, "Roy")
```
*Ref: The_Ultimate_Go_Notebook.md — "Declaring And Constructing Maps" / "Lookups and Deleting Map Keys"*

**Don't:** Use zero value to test key existence — zero may be a valid stored value.

**Code (invalid key types):**
```go
type slice []user
Users := make(map[slice]user)
// Compiler Error: slice is not comparable
```
*Ref: The_Ultimate_Go_Notebook.md — "Key Map Restrictions"*

---

### Decoupling — Methods: Value vs Pointer Receivers
`#go`

**Principle:** Value receivers implement value semantics (operate on a copy). Pointer receivers implement pointer semantics (operate on shared access). Don't mix on the same type. The compiler adjusts calls so concrete values and pointers can both invoke any method — but consistency matters.

**Code:**
```go
type user struct {
    name  string
    email string
}

func (u user) notify() {
    fmt.Printf("Sending User Email To %s<%s>\n", u.name, u.email)
}

func (u *user) changeEmail(email string) {
    u.email = email
    fmt.Printf("Changed User Email To %s\n", email)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Methods"*

**Code (compiler adjusts calls):**
```go
bill := user{"Bill", "bill@email.com"}
bill.notify()
bill.changeEmail("bill@hotmail.com")

bill := &user{"Bill", "bill@email.com"}
bill.notify()
bill.changeEmail("bill@hotmail.com")
```
*Ref: The_Ultimate_Go_Notebook.md — "Method Calls"*

---

### Decoupling — Data Semantic Guidelines (Built-in / Internal / Struct)
`#go` `#general`

**Principle:** Let the data dictate semantics, not the function.

| Category | Move | Read/Write |
|---|---|---|
| Built-in (int, string, bool) | Value | Value |
| Internal (slice, map, channel, func, interface) | Value | Pointer |
| Struct | Value if safe to copy; else pointer | Pointer |

**Code (built-in guideline):**
```go
func Foo(x int, y string, z bool) (int, string, bool)

type Foo struct {
    X int
    Y string
    Z bool
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Semantic Guideline For Built-In Types"*

**Code (internal guideline):**
```go
func Foo(data []byte) []byte

type Foo struct {
    X []int
    Y []string
    Z []bool
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Semantic Guideline For Slices"*

---

### Decoupling — Standard Library Examples of Semantic Consistency
`#go`

**Principle:** Look at factory function return types to determine chosen semantics.

**Code (time package — value semantics):**
```go
type Time struct {
    sec  int64
    nsec int32
    loc  *Location
}

func Now() Time {
    sec, nsec := now()
    return Time{sec + unixToInternal, nsec, Local}
}

func (t Time) Add(d Duration) Time {
    t.sec += int64(d / 1e9)
    nsec := int32(t.nsec) + int32(d%1e9)
    if nsec >= 1e9 {
        t.sec++
        nsec -= 1e9
    } else if nsec < 0 {
        t.sec--
        nsec += 1e9
    }
    t.nsec = nsec
    return t
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Semantic Guideline For Struct Types"*

**Code (os.File — pointer semantics):**
```go
func Open(name string) (file *File, err error) {
    return OpenFile(name, O_RDONLY, 0)
}

func (f *File) Chdir() error {
    if f == nil {
        return ErrInvalid
    }
    if e := syscall.Fchdir(f.fd); e != nil {
        return &PathError{"chdir", f.name, e}
    }
    return nil
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Semantic Guideline For Struct Types"*

**Don't:** Once you switch to pointer semantics, never go back to value — it's not safe to copy a value a pointer points to.

---

### Decoupling — Methods Are Just Functions
`#go`

**Principle:** Methods are syntactic sugar over functions where the receiver is the first parameter.

**Code:**
```go
type data struct {
    name string
    age  int
}

func (d data) displayName() {
    fmt.Println("My Name Is", d.name)
}

func (d *data) setAge(age int) {
    d.age = age
    fmt.Println(d.name, "Is Age", d.age)
}

// Equivalent function-style invocation:
// data.displayName(d)
// (*data).setAge(&d, 21)
```
*Ref: The_Ultimate_Go_Notebook.md — "Methods Are Just Functions"*

---

### Decoupling — Function Values Capture Receivers
`#go`

**Principle:** A method value bound to a value receiver keeps its own copy. A method value bound to a pointer receiver operates on shared state.

**Code:**
```go
d := data{name: "Bill"}
f1 := d.displayName // value receiver -> copy
f1()
d.name = "Joan"
f1() // Still "Bill"

f2 := d.setAge // pointer receiver -> shared
f2(45)
d.name = "Sammy"
f2(45) // Prints "Sammy Is Age 45"
```
*Ref: The_Ultimate_Go_Notebook.md — "Know The Behavior of the Code"*

---

### Decoupling — Interfaces Are Valueless
`#go`

**Principle:** An interface is a valueless type declaring a method set. Concrete data must implement it. An interface value is internally a two-word structure: iTable pointer + concrete value pointer.

**Code:**
```go
type reader interface {
    read(b []byte) (int, error)
}

type file struct {
    name string
}

func (file) read(b []byte) (int, error) {
    s := "<rss><channel><title>Going Go</title></channel></rss>"
    copy(b, s)
    return len(s), nil
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Interfaces / Implementing Interfaces"*

---

### Decoupling — Polymorphism Means Behavior Changes Per Concrete Value
`#go`

**Code:**
```go
func retrieve(r reader) error {
    data := make([]byte, 100)
    len, err := r.read(data)
    if err != nil {
        return err
    }
    fmt.Println(string(data[:len]))
    return nil
}

f := file{"data.json"}
p := pipe{"cfg_service"}
retrieve(f)
retrieve(p)
```
*Ref: The_Ultimate_Go_Notebook.md — "Polymorphism"*

---

### Decoupling — Method Set Rules
`#go`

**Principle:** For type `T`, only value-receiver methods belong to its method set. For `*T`, all methods belong. Storing a value in an interface requires methods to exist explicitly (no compiler adjustment).

**Code (compiler error):**
```go
type notifier interface {
    notify()
}

type user struct {
    name  string
    email string
}

func (u *user) notify() {
    fmt.Printf("Sending User Email To %s<%s>\n", u.name, u.email)
}

func sendNotification(n notifier) {
    n.notify()
}

func main() {
    u := user{"Bill", "bill@email.com"}
    sendNotification(u)
    // cannot use u (type user) as type notifier:
    // user does not implement notifier (notify method has pointer receiver)
}

// Fix: share u.
func main() {
    u := user{"Bill", "bill@email.com"}
    sendNotification(&u)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Method Set Rules"*

**Code (unaddressable values can't satisfy pointer-receiver interfaces):**
```go
type duration int

func (d *duration) notify() {
    fmt.Println("Sending Notification in", *d)
}

func main() {
    duration(42).notify()
}
// Compiler Error:
// cannot call pointer method on duration(42)
// cannot take the address of duration(42)
```
*Ref: The_Ultimate_Go_Notebook.md — "Method Set Rules"*

---

### Decoupling — Slice of Interface for Common Behavior
`#go`

**Code:**
```go
type printer interface {
    print()
}

type canon struct{ name string }

func (c canon) print() {
    fmt.Printf("Printer Name: %s\n", c.name)
}

type epson struct{ name string }

func (e *epson) print() {
    fmt.Printf("Printer Name: %s\n", e.name)
}

func main() {
    c := canon{"PIXMA TR4520"}
    e := epson{"WorkForce Pro WF-3720"}

    printers := []printer{c, &e}

    c.name = "PROGRAF PRO-1000"
    e.name = "Home XP-4100"

    for _, p := range printers {
        p.print()
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Slice of Interface"*

---

### Decoupling — Embedding Promotes Behavior, Not State
`#go`

**Principle:** Embedding is not inheritance. It promotes inner-type fields and methods to the outer type. Outer-type methods of the same name override the promotion.

**Code:**
```go
type user struct {
    name  string
    email string
}

type admin struct {
    *user // Pointer Semantic Embedding
    level string
}

func (u *user) notify() {
    fmt.Printf("Sending user email To %s<%s>\n", u.name, u.email)
}

func main() {
    ad := admin{
        user: &user{
            name:  "john smith",
            email: "john@yahoo.com",
        },
        level: "super",
    }
    ad.user.notify()
    ad.notify() // Outer type promotion
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Embedding"*

**Code (outer type overrides inner):**
```go
type admin struct {
    *user
    level string
}

func (a *admin) notify() {
    fmt.Printf("Sending admin Email To %s<%s>\n", a.name, a.email)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Embedding"*

---

### Decoupling — Exporting Rules
`#go`

**Principle:** Capitalized identifiers are exported across package boundaries. Be consistent: don't mix exported and unexported fields/types arbitrarily.

**Code:**
```go
package counters

type AlertCounter int // Exported
type alertCounter int  // Unexported
```
*Ref: The_Ultimate_Go_Notebook.md — "Exporting"*

**Code (avoid returning unexported types):**
```go
package counters

type alertCounter int

func New(value int) alertCounter {
    return alertCounter(value)
}
// Legal but confusing — callers can't reference the type name.
```
*Ref: The_Ultimate_Go_Notebook.md — "Exporting"*

**Code (embedded unexported with exported fields causes partial construction):**
```go
package users

type user struct { // unexported
    Name string    // exported
    ID   int
}

type Manager struct { // exported
    Title string
    user          // unexported embed
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Exporting"*

---

### Software Design — Group By Behavior, Not Common DNA
`#go` `#general`

**Principle:** Embedding to simulate inheritance is an anti-pattern. Use interfaces to group types by what they can do.

**Code (anti-pattern — embedding as inheritance):**
```go
type Animal struct {
    Name     string
    IsMammal bool
}

func (a *Animal) Speak() {
    fmt.Println("UGH!", "My name is", a.Name, ", it is", a.IsMammal, "I am a mammal")
}

type Dog struct {
    Animal
    PackFactor int
}

func (d *Dog) Speak() {
    fmt.Println("Woof!", "My name is", d.Name, ", it is", d.IsMammal,
        "I am a mammal with a pack factor of", d.PackFactor)
}

type Cat struct {
    Animal
    ClimbFactor int
}

func (c *Cat) Speak() {
    fmt.Println("Meow!", "My name is", c.Name, ", it is", c.IsMammal,
        "I am a mammal with a climb factor of", c.ClimbFactor)
}

// Trying to group by common DNA fails:
animals := []Animal{
    Dog{Animal: Animal{Name: "Fido", IsMammal: true}, PackFactor: 5},
    Cat{Animal: Animal{Name: "Milo", IsMammal: true}, ClimbFactor: 4},
}
// Compiler error: Dog and Cat are not Animal.
```
*Ref: The_Ultimate_Go_Notebook.md — "Grouping Different Types of Data"*

**Code (correct — group by behavior):**
```go
type Speaker interface {
    Speak()
}

speakers := []Speaker{
    &Dog{
        Animal:     Animal{Name: "Fido", IsMammal: true},
        PackFactor: 5,
    },
    &Cat{
        Animal:     Animal{Name: "Milo", IsMammal: true},
        ClimbFactor: 4,
    },
}

for _, speaker := range speakers {
    speaker.Speak()
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Grouping Different Types of Data"*

---

### Software Design — Type Declaration Guidelines
`#go` `#general`

**Do:**
- Declare types that represent something new or unique.
- Validate that a value of any type is created or used on its own.
- Embed types because you need the behavior, not the state.

**Don't:**
- Create aliases just for readability.
- Declare types whose sole purpose is to share a common set of states.

*Ref: The_Ultimate_Go_Notebook.md — "Grouping Different Types of Data"*

---

### Software Design — Don't Design With Interfaces, Discover Them
`#go` `#general`

**Principle:** Start with concrete solutions; refactor through readability, efficiency, abstraction, testability. Abstract only where data could change and cascading effects would result.

> "Don't design with interfaces, discover them." — Rob Pike

> "Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident." — Rob Pike

> "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise." — Edsger W. Dijkstra

*Ref: The_Ultimate_Go_Notebook.md — "Don't Design With Interfaces"*

---

### Software Design — Composition Pattern (Xenia/Pillar Walkthrough)
`#go`

**Principle:** Compose larger types from smaller types. Identify what changes; refactor to interfaces. Then ask: can the function be more precise?

**Code (concrete first):**
```go
type Xenia struct {
    Host    string
    Timeout time.Duration
}

func (*Xenia) Pull(d *Data) error {
    switch rand.Intn(10) {
    case 1, 9:
        return io.EOF
    case 5:
        return errors.New("Error reading data from Xenia")
    default:
        d.Line = "Data"
        fmt.Println("In:", d.Line)
        return nil
    }
}

type Pillar struct {
    Host    string
    Timeout time.Duration
}

func (*Pillar) Store(d *Data) error {
    fmt.Println("Out:", d.Line)
    return nil
}

func Pull(x *Xenia, data []Data) (int, error) {
    for i := range data {
        if err := x.Pull(&data[i]); err != nil {
            return i, err
        }
    }
    return len(data), nil
}

func Store(p *Pillar, data []Data) (int, error) {
    for i := range data {
        if err := p.Store(&data[i]); err != nil {
            return i, err
        }
    }
    return len(data), nil
}

type System struct {
    Xenia
    Pillar
}

func Copy(sys *System, batch int) error {
    data := make([]Data, batch)
    for {
        i, err := Pull(&sys.Xenia, data)
        if i > 0 {
            if _, err := Store(&sys.Pillar, data[:i]); err != nil {
                return err
            }
        }
        if err != nil {
            return err
        }
    }
}

func main() {
    sys := System{
        Xenia:  Xenia{Host: "localhost:8000", Timeout: time.Second},
        Pillar: Pillar{Host: "localhost:9000", Timeout: time.Second},
    }
    if err := Copy(&sys, 3); err != io.EOF {
        fmt.Println(err)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Composition"*

**Code (decouple with interfaces):**
```go
type Puller interface {
    Pull(d *Data) error
}

type Storer interface {
    Store(d *Data) error
}

func Pull(p Puller, data []Data) (int, error) {
    for i := range data {
        if err := p.Pull(&data[i]); err != nil {
            return i, err
        }
    }
    return len(data), nil
}

func Store(s Storer, data []Data) (int, error) {
    for i := range data {
        if err := s.Store(&data[i]); err != nil {
            return i, err
        }
    }
    return len(data), nil
}

// Compose larger interfaces from smaller ones.
type PullStorer interface {
    Puller
    Storer
}

func Copy(ps PullStorer, batch int) error {
    data := make([]Data, batch)
    for {
        i, err := Pull(ps, data)
        if i > 0 {
            if _, err := Store(ps, data[:i]); err != nil {
                return err
            }
        }
        if err != nil {
            return err
        }
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Decoupling With Interfaces"*

**Code (compose concrete type from interfaces — final precision):**
```go
type System struct {
    Puller
    Storer
}

func main() {
    sys := System{
        Puller: &Xenia{Host: "localhost:8000", Timeout: time.Second},
        Storer: &Pillar{Host: "localhost:9000", Timeout: time.Second},
    }
    if err := Copy(&sys, 3); err != io.EOF {
        fmt.Println(err)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Interface Composition"*

**Code (maximally precise — ask only for what you need):**
```go
func Copy(p Puller, s Storer, batch int) error {
    // ...
}

func main() {
    x := Xenia{Host: "localhost:8000", Timeout: time.Second}
    p := Pillar{Host: "localhost:9000", Timeout: time.Second}
    if err := Copy(&x, &p, 3); err != io.EOF {
        fmt.Println(err)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Precision Review"*

---

### Software Design — Implicit Interface Conversions (Downcast Allowed, Upcast Not)
`#go`

**Principle:** A larger-interface value can be assigned to a smaller-interface variable (the compiler knows the concrete value satisfies the smaller set). The reverse requires a runtime type assertion.

**Code:**
```go
type Mover interface {
    Move()
}

type Locker interface {
    Lock()
    Unlock()
}

type MoveLocker interface {
    Mover
    Locker
}

type bike struct{}

func (bike) Move()    { fmt.Println("Moving the bike") }
func (bike) Lock()    { fmt.Println("Locking the bike") }
func (bike) Unlock()  { fmt.Println("Unlocking the bike") }

var ml MoveLocker
var m Mover

ml = bike{} // OK
m = ml      // OK — concrete bike implements Mover

ml = m      // Compiler Error:
            // cannot use m (type Mover) as type MoveLocker in assignment:
            // Mover does not implement MoveLocker (missing Lock method)
```
*Ref: The_Ultimate_Go_Notebook.md — "Implicit Interface Conversions"*

---

### Software Design — Type Assertions (Safe vs Panic)
`#go`

**Code:**
```go
b := m.(bike)      // panics if m doesn't hold a bike
ml = b

b, ok := m.(bike)  // ok==false -> no panic, b is zero-value bike
ml = b
```
*Ref: The_Ultimate_Go_Notebook.md — "Type assertions"*

**Code (random type assertion):**
```go
mvs := []fmt.Stringer{
    Car{},
    Cloud{},
}

for i := 0; i < 10; i++ {
    rn := rand.Intn(2)
    if v, is := mvs[rn].(Cloud); is {
        fmt.Println("Got Lucky:", v)
        continue
    }
    fmt.Println("Got Unlucky")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Type assertions"*

---

### Software Design — Interface Pollution Symptoms
`#go` `#general`

**Symptoms:**
- Package declares an interface matching the entire API of its own concrete type.
- Exported interfaces with unexported concrete implementations.
- Factory returns the interface with an unexported concrete inside.
- Removing the interface changes nothing for users.
- Interface doesn't decouple from any change.

**Use an interface when:**
- Users of the API need to provide an implementation detail.
- Multiple internal implementations are maintained.
- Parts of the API that can change have been identified.

**Question an interface when:**
- Its only purpose is writing testable APIs (write usable APIs first).
- It isn't decoupling anything from change.
- It's not clear how the interface makes the code better.

*Ref: The_Ultimate_Go_Notebook.md — "Interface Pollution"*

**Code (interface pollution — Server is a noun, not a behavior):**
```go
type Server interface {
    Start() error
    Stop() error
    Wait() error
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Interface Pollution"*

---

### Software Design — Interface Ownership (Consumer Declares)
`#go`

**Principle:** In Go, the consumer declares the interface, not the producer. Application developers define their own interfaces for third-party concrete types, enabling test mocks without modifying the original package.

**Code:**
```go
package pubsub

type PubSub struct {
    host string
}

func New(host string) *PubSub {
    return &PubSub{host: host}
}

func (ps *PubSub) Publish(key string, v interface{}) error { return nil }
func (ps *PubSub) Subscribe(key string) error              { return nil }
```
*Ref: The_Ultimate_Go_Notebook.md — "Interface Ownership"*

**Code (consumer declares interface + mock):**
```go
package main

type publisher interface {
    Publish(key string, v interface{}) error
    Subscribe(key string) error
}

type mock struct{}

func (m *mock) Publish(key string, v interface{}) error { return nil }
func (m *mock) Subscribe(key string) error              { return nil }

func main() {
    pubs := []publisher{
        pubsub.New("localhost"),
        &mock{},
    }
    for _, p := range pubs {
        p.Publish("key", "value")
        p.Subscribe("key")
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Interface Ownership"*

---

### Error Handling — Errors Are Values Implementing `error`
`#go`

**Principle:** `error` is a built-in interface. `Error()` is for logging, not parsing. Always return `error` from functions — never the concrete type.

**Code:**
```go
// http://golang.org/pkg/builtin/#error
type error interface {
    Error() string
}

// errors package
type errorString struct {
    s string
}

func (e *errorString) Error() string {
    return e.s
}

func New(text string) error {
    return &errorString{text}
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Error Handling"*

---

### Error Handling — Error Variables Identify Specific Errors
`#go`

**Code:**
```go
var (
    ErrBadRequest = errors.New("Bad Request")
    ErrPageMoved  = errors.New("Page Moved")
)

func webCall(b bool) error {
    if b {
        return ErrBadRequest
    }
    return ErrPageMoved
}

func main() {
    if err := webCall(true); err != nil {
        switch err {
        case ErrBadRequest:
            fmt.Println("Bad Request Occurred")
            return
        case ErrPageMoved:
            fmt.Println("The Page moved")
            return
        default:
            fmt.Println(err)
            return
        }
    }
    fmt.Println("Life is good")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Error Handling"*

---

### Error Handling — Custom Concrete Error Types
`#go`

**Principle:** When you need state on the error (not just identity), use a custom concrete type with an `Error()` method.

**Code:**
```go
type UnmarshalTypeError struct {
    Value string
    Type  reflect.Type
}

func (e *UnmarshalTypeError) Error() string {
    return "json: cannot unmarshal " + e.Value +
        " into Go value of type " + e.Type.String()
}

type InvalidUnmarshalError struct {
    Type reflect.Type
}

func (e *InvalidUnmarshalError) Error() string {
    if e.Type == nil {
        return "json: Unmarshal(nil)"
    }
    if e.Type.Kind() != reflect.Ptr {
        return "json: Unmarshal(non-pointer " + e.Type.String() + ")"
    }
    return "json: Unmarshal(nil " + e.Type.String() + ")"
}

func Unmarshal(data []byte, v interface{}) error {
    rv := reflect.ValueOf(v)
    if rv.Kind() != reflect.Ptr || rv.IsNil() {
        return &InvalidUnmarshalError{reflect.TypeOf(v)}
    }
    return &UnmarshalTypeError{"string", reflect.TypeOf(v)}
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Error Handling"*

---

### Error Handling — Behavior-Based Type Checks Stay Decoupled
`#go`

**Principle:** When checking error types, prefer an interface (behavior) over a concrete type so you stay decoupled from implementation changes.

**Code:**
```go
type temporary interface {
    Temporary() bool
}

func (c *client) BehaviorAsContext() {
    for {
        line, err := c.reader.ReadString('\n')
        if err != nil {
            switch e := err.(type) {
            case temporary:
                if !e.Temporary() {
                    log.Println("Temporary: Client leaving chat")
                    return
                }
            default:
                if err == io.EOF {
                    log.Println("EOF: Client leaving chat")
                    return
                }
                log.Println("read-routine", err)
            }
        }
        fmt.Println(line)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Error Handling"*

---

### Error Handling — Always Use the `error` Interface (Not Concrete Types)
`#go`

**Principle:** Returning a concrete error type causes subtle nil-interface bugs.

**Code (bug — `nil` concrete stored in non-nil interface):**
```go
type customError struct{}

func (c *customError) Error() string {
    return "Find the bug."
}

func fail() ([]byte, *customError) {
    return nil, nil
}

func main() {
    var err error
    if _, err = fail(); err != nil {
        log.Fatal("Why did this fail?") // <-- Runs even though "no error"
    }
    log.Println("No Error")
}
// Output: Why did this fail?
```
*Ref: The_Ultimate_Go_Notebook.md — "Always Use The Error Interface"*

**Why:** A `*customError` value of `nil` stored inside an `error` interface is not the same as a nil `error` interface — the interface still has type information.

---

### Error Handling — Wrapping Errors (pkg/errors vs stdlib)
`#go`

**Principle:** Wrap errors as they propagate up so the handler has context. Two options: `github.com/pkg/errors` (`Wrap`/`Cause`) or the stdlib (`fmt.Errorf` with `%w`, `errors.As`, `errors.Unwrap`).

**Code (Dave Cheney's package):**
```go
package main

import (
    "fmt"
    "github.com/pkg/errors"
)

type AppError struct {
    State int
}

func (c *AppError) Error() string {
    return fmt.Sprintf("App Error, State: %d", c.State)
}

func main() {
    if err := firstCall(10); err != nil {
        switch v := errors.Cause(err).(type) {
        case *AppError:
            fmt.Println("Custom App Error:", v.State)
        default:
            fmt.Println("Default Error")
        }
        fmt.Printf("%v\n", err)
    }
}

func firstCall(i int) error {
    if err := secondCall(i); err != nil {
        return errors.Wrapf(err, "secondCall(%d)", i)
    }
    return nil
}

func secondCall(i int) error {
    return &AppError{99}
}
// Output:
// Custom App Error: 99
// secondCall(10): App Error, State: 99
```
*Ref: The_Ultimate_Go_Notebook.md — "Handling Errors"*

**Code (stdlib with %w and errors.As):**
```go
package main

import (
    "errors"
    "fmt"
)

type AppError struct {
    State int
}

func (c *AppError) Error() string {
    return fmt.Sprintf("App Error, State: %d", c.State)
}

func Cause(err error) error {
    root := err
    for {
        if err = errors.Unwrap(root); err == nil {
            return root
        }
        root = err
    }
}

func main() {
    if err := firstCall(10); err != nil {
        var ap *AppError
        if errors.As(err, &ap) {
            fmt.Println("As says it is an AppError")
        }
        switch v := Cause(err).(type) {
        case *AppError:
            fmt.Println("Custom App Error:", v.State)
        default:
            fmt.Println("Default Error")
        }
        fmt.Printf("%v\n", err)
    }
}

func firstCall(i int) error {
    if err := secondCall(i); err != nil {
        return fmt.Errorf("secondCall(%d) : %w", i, err)
    }
    return nil
}

func secondCall(i int) error {
    return &AppError{99}
}
// Output:
// As says it is an AppError
// Custom App Error: 99
// secondCall(10): App Error, State: 99
```
*Ref: The_Ultimate_Go_Notebook.md — "Handling Errors"*

---

### Concurrency — Scheduler Semantics (G/M/P)
`#concurrency`

**Principle:** The Go runtime creates an OS thread (M) per virtual core attached to a logical processor (P). Goroutines (G) are scheduled onto M/P pairs by the Go scheduler on top of the OS scheduler.

**Definitions:**
- **Concurrency**: undefined out-of-order execution.
- **Parallelism**: executing instructions simultaneously on multiple cores.
- **CPU-Bound**: doesn't cause threads to wait.
- **I/O-Bound**: causes threads to wait (network, disk, syscalls, sync).
- **Synchronization**: managing shared memory access.
- **Orchestration**: signaling between goroutines.

*Ref: The_Ultimate_Go_Notebook.md — "Scheduler Semantics"*

---

### Concurrency — Goroutine Basics and WaitGroup Orchestration
`#concurrency`

**Principle:** Use `sync.WaitGroup` for orchestration. Call `Add` once with the known count when possible. Keep `Add` and `Done` in the same line of sight.

**Code:**
```go
func init() {
    runtime.GOMAXPROCS(1)
}

func main() {
    var wg sync.WaitGroup
    wg.Add(2)

    go func() {
        lowercase()
        wg.Done()
    }()
    go func() {
        uppercase()
        wg.Done()
    }()

    fmt.Println("Waiting To Finish")
    wg.Wait()
    fmt.Println("\nTerminating Program")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Concurrency Basics"*

**Don't:**
- Pass WaitGroups across functions where Add/Done get lost.
- Forget `Done()` — causes permanent deadlock.
- Mis-size `Add()` — too small: lost guarantees; too large: deadlock.

---

### Concurrency — GOMAXPROCS Queries Available Parallelism
`#concurrency`

**Code:**
```go
g := runtime.GOMAXPROCS(0) // returns the number of threads available
```
*Ref: The_Ultimate_Go_Notebook.md — "Concurrency Basics"*

**Do:** Match this number to your container's CPU quota; mismatches hurt performance.

---

### Concurrency — Preemptive Scheduler (Context Switches Are Unpredictable)
`#concurrency`

**Principle:** Even with `GOMAXPROCS=1` the scheduler is preemptive. The number and timing of context switches vary on every run.

**Code:**
```go
func printHashes(prefix string) {
    for i := 1; i <= 50000; i++ {
        num := strconv.Itoa(i)
        sum := sha1.Sum([]byte(num))
        fmt.Printf("%s: %05d: %x\n", prefix, i, sum)
    }
    fmt.Println("Completed", prefix)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Preemptive Scheduler"*

**Don't:** Build correctness on observed ordering of goroutine execution.

---

### Concurrency — Data Races Are Hidden Until They Aren't
`#concurrency`

**Principle:** A data race is two+ goroutines accessing the same memory with at least one writer, unsynchronized. A single added log statement can expose a latent bug.

**Code (looks correct, but contains a race):**
```go
var counter int

func main() {
    const grs = 2
    var wg sync.WaitGroup
    wg.Add(grs)

    for g := 0; g < grs; g++ {
        go func() {
            for i := 0; i < 2; i++ {
                value := counter
                value++
                counter = value
            }
            wg.Done()
        }()
    }

    wg.Wait()
    fmt.Println("Counter:", counter)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Races"*

**Code (adding a log exposes the race — result becomes 2 instead of 4):**
```go
go func() {
    for i := 0; i < 2; i++ {
        value := counter
        value++
        log.Println("logging") // <-- exposes the race
        counter = value
    }
    wg.Done()
}()
```
*Ref: The_Ultimate_Go_Notebook.md — "Data Races"*

---

### Concurrency — Race Detector
`#concurrency` `#testing`

**Principle:** `go build -race`, `go test -race`, `go run -race` instrument the binary to detect unsynchronized access. Roughly 20% runtime overhead.

```
$ go build -race
$ ./example1

==================
WARNING: DATA RACE
Write at 0x000001278d88 by goroutine 8:
    main.main.func1()
    /data_race/example1/example1.go:41 +0xa6

Previous read at 0x000001278d88 by goroutine 7:
    main.main.func1()
    /data_race/example1/example1.go:38 +0x4a
==================
Found 1 data race(s)
```
*Ref: The_Ultimate_Go_Notebook.md — "Race Detection"*

---

### Concurrency — Atomics for Hardware-Level Synchronization
`#concurrency`

**Principle:** Atomics work on individual words. Use precision integers (`int32`, `int64`). The first parameter is always the address of shared state.

**Code:**
```go
var counter int32

func main() {
    const grs = 2
    var wg sync.WaitGroup
    wg.Add(grs)

    for g := 0; g < grs; g++ {
        go func() {
            for i := 0; i < 2; i++ {
                atomic.AddInt32(&counter, 1)
            }
            wg.Done()
        }()
    }

    wg.Wait()
    fmt.Println("Counter:", counter)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Atomics"*

**API surface:**
```go
func AddInt32(addr *int32, delta int32) (new int32)
func CompareAndSwapInt32(addr *int32, old, new int32) (swapped bool)
func LoadInt32(addr *int32) (val int32)
func StoreInt32(addr *int32, val int32)
func SwapInt32(addr *int32, new int32) (old int32)
type Value
    func (v *Value) Load() (x interface{})
    func (v *Value) Store(x interface{})
```
*Ref: The_Ultimate_Go_Notebook.md — "Atomics"*

---

### Concurrency — Mutex Discipline
`#concurrency`

**Principle:** A mutex boxes a group of operations so only one goroutine runs them at a time. It is not a queue. Lock creates back-pressure — minimize the time between Lock and Unlock. `Lock` and `Unlock` must live in the same function.

**Code (mutex protecting read-modify-write):**
```go
var counter int

func main() {
    const grs = 2
    var wg sync.WaitGroup
    wg.Add(grs)
    var mu sync.Mutex

    for g := 0; g < grs; g++ {
        go func() {
            for i := 0; i < 2; i++ {
                mu.Lock()
                {
                    value := counter
                    value++
                    counter = value
                }
                mu.Unlock()
            }
            wg.Done()
        }()
    }

    wg.Wait()
    fmt.Println("Counter:", counter)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Mutexes"*

**Don't:** Call `Lock` twice on the same mutex in the same function — that's a code-review stop. The race may still exist and the detector can't see it.

**Code (broken — Lock/Unlock split loses the race):**
```go
for i := 0; i < 2; i++ {
    var value int
    mu.Lock()
    {
        value = counter
    }
    mu.Unlock()
    value++                  // RACE WINDOW
    mu.Lock()
    {
        counter = value
    }
    mu.Unlock()
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Mutexes"*

---

### Concurrency — Read/Write Mutex (sync.RWMutex)
`#concurrency`

**Principle:** Multiple readers may hold `RLock` simultaneously. A writer (`Lock`) excludes all readers and other writers. Never mismatch `Lock` with `RUnlock` or `RLock` with `Unlock`.

**Code:**
```go
package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

var data []string
var rwMutex sync.RWMutex

func main() {
    var wg sync.WaitGroup
    wg.Add(1)

    go func() {
        for i := 0; i < 10; i++ {
            writer(i)
        }
        wg.Done()
    }()

    for i := 0; i < 8; i++ {
        go func(id int) {
            for {
                reader(id)
            }
        }(i)
    }

    wg.Wait()
    fmt.Println("Program Complete")
}

func writer(i int) {
    rwMutex.Lock()
    {
        time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
        fmt.Println("****> : Performing Write")
        data = append(data, fmt.Sprintf("String: %d", i))
    }
    rwMutex.Unlock()
}

func reader(id int) {
    rwMutex.RLock()
    {
        time.Sleep(time.Duration(rand.Intn(10)) * time.Millisecond)
        fmt.Printf("%d : Performing Read : Length[%d]\n", id, len(data))
    }
    rwMutex.RUnlock()
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Read/Write Mutexes"*

---

### Concurrency — Channels Are Signaling Mechanisms
`#concurrency`

**Principle:** Don't think of channels as queues — think of them as signaling. Three decisions:
1. **Guarantee level**: Unbuffered = guarantee at signaling level (recv before send). Buffered = guarantee outside signaling (send before recv).
2. **Data with signal**: With data = 1-to-1. Without data (close) = 1-to-many.
3. **Channel state**: nil (blocks both ways), open (works), closed (recv returns immediately, send panics).

*Ref: The_Ultimate_Go_Notebook.md — "Channel Semantics"*

---

### Concurrency — Pattern 1: Wait For Result
`#concurrency`

**Code:**
```go
func waitForResult() {
    ch := make(chan string)
    go func() {
        time.Sleep(time.Duration(rand.Intn(500)) * time.Millisecond)
        ch <- "data"
        fmt.Println("child : sent signal")
    }()
    d := <-ch
    fmt.Println("parent : recv'd signal :", d)
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Wait For Result"*

**Cost:** Unknown latency — sender waits for receiver.

---

### Concurrency — Pattern 2: Fan Out / In
`#concurrency`

**Principle:** One goroutine per work item; buffered channel sized to count. Dangerous in services — goroutine count is a multiplier.

**Code:**
```go
func fanOut() {
    children := 2000
    ch := make(chan string, children)
    for c := 0; c < children; c++ {
        go func(child int) {
            time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
            ch <- "data"
            fmt.Println("child : sent signal :", child)
        }(c)
    }
    for children > 0 {
        d := <-ch
        children--
        fmt.Println(d)
        fmt.Println("parent : recv'd signal :", children)
    }
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Fan Out/In"*

**Don't:** Use fan-out in a request path where each request already fans out — goroutine counts multiply.

---

### Concurrency — Pattern 3: Wait For Task
`#concurrency`

**Code:**
```go
func waitForTask() {
    ch := make(chan string)
    go func() {
        d := <-ch
        fmt.Println("child : recv'd signal :", d)
    }()
    time.Sleep(time.Duration(rand.Intn(500)) * time.Millisecond)
    ch <- "data"
    fmt.Println("parent : sent signal")
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Wait For Task"*

**Foundation** for pooling — unbuffered so timeouts/cancellation can be added later.

---

### Concurrency — Pattern 4: Pooling
`#concurrency`

**Principle:** GOMAXPROCS goroutines service one channel via `for range`. Close channel to signal shutdown.

**Code:**
```go
func pooling() {
    ch := make(chan string)
    g := runtime.GOMAXPROCS(0)
    for c := 0; c < g; c++ {
        go func(child int) {
            for d := range ch {
                fmt.Printf("child %d : recv'd signal : %s\n", child, d)
            }
            fmt.Printf("child %d : recv'd shutdown signal\n", child)
        }(c)
    }

    const work = 100
    for w := 0; w < work; w++ {
        ch <- "data"
        fmt.Println("parent : sent signal :", w)
    }
    close(ch)
    fmt.Println("parent : sent shutdown signal")
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Pooling"*

---

### Concurrency — Pattern 5: Drop (Capacity-Limiting)
`#concurrency`

**Principle:** For services under heavy load: buffered channel + `select { case ch <- x: default: drop }`.

**Code:**
```go
func drop() {
    const cap = 100
    ch := make(chan string, cap)
    go func() {
        for p := range ch {
            fmt.Println("child : recv'd signal :", p)
        }
    }()

    const work = 2000
    for w := 0; w < work; w++ {
        select {
        case ch <- "data":
            fmt.Println("parent : sent signal :", w)
        default:
            fmt.Println("parent : dropped data :", w)
        }
    }
    close(ch)
    fmt.Println("parent : sent shutdown signal")
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Drop"*

---

### Concurrency — Pattern 6: Cancellation (Context With Timeout)
`#concurrency`

**Principle:** Use `context.WithTimeout`. Always `defer cancel()`. The work channel must be buffered with size 1 so the child can always send, even if the parent has walked away.

**Code:**
```go
func cancellation() {
    duration := 150 * time.Millisecond
    ctx, cancel := context.WithTimeout(context.Background(), duration)
    defer cancel()

    ch := make(chan string, 1)
    go func() {
        time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
        ch <- "data"
    }()

    select {
    case d := <-ch:
        fmt.Println("work complete", d)
    case <-ctx.Done():
        fmt.Println("work cancelled")
    }
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Cancellation"*

**Don't:** Forget to call `cancel()` — it leaks memory.

---

### Concurrency — Pattern 7: Fan Out Semaphore
`#concurrency`

**Principle:** All goroutines are created but only GOMAXPROCS may execute concurrently. Use a semaphore channel.

**Code:**
```go
func fanOutSem() {
    children := 2000
    ch := make(chan string, children)
    g := runtime.GOMAXPROCS(0)
    sem := make(chan bool, g)

    for c := 0; c < children; c++ {
        go func(child int) {
            sem <- true
            {
                t := time.Duration(rand.Intn(200)) * time.Millisecond
                time.Sleep(t)
                ch <- "data"
                fmt.Println("child : sent signal :", child)
            }
            <-sem
        }(c)
    }

    for children > 0 {
        d := <-ch
        children--
        fmt.Println(d)
        fmt.Println("parent : recv'd signal :", children)
    }
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Fan Out/In Semaphore"*

---

### Concurrency — Pattern 8: Bounded Work Pooling
`#concurrency`

**Code:**
```go
func boundedWorkPooling() {
    work := []string{"paper", "paper", "paper", "paper", 2000: "paper"}
    g := runtime.GOMAXPROCS(0)
    var wg sync.WaitGroup
    wg.Add(g)

    ch := make(chan string, g)
    for c := 0; c < g; c++ {
        go func(child int) {
            defer wg.Done()
            for wrk := range ch {
                fmt.Printf("child %d : recv'd signal : %s\n", child, wrk)
            }
            fmt.Printf("child %d : recv'd shutdown signal\n", child)
        }(c)
    }

    for _, wrk := range work {
        ch <- wrk
    }
    close(ch)
    wg.Wait()
    time.Sleep(time.Second)
    fmt.Println("-------------------------------------------------")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Bounded Work Pooling"*

---

### Concurrency — Pattern 9: Retry Timeout
`#concurrency`

**Code:**
```go
func retryTimeout(ctx context.Context, retryInterval time.Duration,
    check func(ctx context.Context) error) {

    for {
        fmt.Println("perform user check call")
        if err := check(ctx); err == nil {
            fmt.Println("work finished successfully")
            return
        }

        fmt.Println("check if timeout has expired")
        if ctx.Err() != nil {
            fmt.Println("time expired 1 :", ctx.Err())
            return
        }

        fmt.Printf("wait %s before trying again\n", retryInterval)
        t := time.NewTimer(retryInterval)
        select {
        case <-ctx.Done():
            fmt.Println("timed expired 2 :", ctx.Err())
            t.Stop()
            return
        case <-t.C:
            fmt.Println("retry again")
        }
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Retry Timeout"*

---

### Concurrency — Pattern 10: Channel Cancellation (Bridge Legacy to Context)
`#concurrency`

**Code:**
```go
func channelCancellation(stop <-chan struct{}) {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    go func() {
        select {
        case <-stop:
            cancel()
        case <-ctx.Done():
        }
    }()

    func(ctx context.Context) error {
        req, err := http.NewRequestWithContext(
            ctx,
            http.MethodGet,
            "https://www.ardanlabs.com/blog/index.xml",
            nil,
        )
        if err != nil {
            return err
        }
        _, err = http.DefaultClient.Do(req)
        if err != nil {
            return err
        }
        return nil
    }(ctx)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Channel Cancellation"*

---

### Testing — Basic Unit Test
`#testing`

**Principle:** A unit of code is a package. Test files use `_test.go`. Test functions start with `Test` + capital letter and take `*testing.T`. The `_test` package suffix forces testing through the exported API.

**Code:**
```go
package sample_test

import (
    "testing"
)

func TestDownload(t *testing.T) {}
func TestUpload(t *testing.T) {}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Unit Test"*

**Code (real test with http.Get):**
```go
package sample_test

import (
    "testing"
    "http"
)

func TestDownload(t *testing.T) {
    url := "https://www.ardanlabs.com/blog/index.xml"
    statusCode := 200

    resp, err := http.Get(url)
    if err != nil {
        t.Fatalf("unable to issue GET on URL: %s: %s", url, err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != statusCode {
        t.Log("exp:", statusCode)
        t.Log("got:", resp.StatusCode)
        t.Fatal("status codes don't match")
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Unit Test"*

**Do:**
- `t.Fatal` for "fail and stop now"; `t.Error` for "fail and continue".
- `t.Log` for verbose info (shows with `-v` or on failure).
- Write tests like production code (e.g. `defer resp.Body.Close()`).

---

### Testing — Table Tests
`#testing`

**Code:**
```go
package sample_test

import (
    "testing"
    "http"
)

func TestDownload(t *testing.T) {
    tt := []struct {
        url        string
        statusCode int
    }{
        {"https://www.ardanlabs.com/blog/index.xml", http.StatusOK},
        {"http://rss.cnn.com/rss/cnn_topstorie.rss", http.StatusNotFound},
    }
    for _, test := range tt {
        resp, err := http.Get(test.url)
        if err != nil {
            t.Fatalf("unable to issue GET on URL: %s: %s", test.url, err)
        }
        defer resp.Body.Close()
        if resp.StatusCode != test.statusCode {
            t.Log("exp:", test.statusCode)
            t.Log("got:", resp.StatusCode)
            t.Fatal("status codes don't match")
        }
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Table Unit Test"*

---

### Testing — Mocking With httptest.NewServer
`#testing`

**Code:**
```go
package sample_test

import (
    "testing"
    "http"
    "httptest"
)

var feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss>
<channel>
    <title>Going Go Programming</title>
    <description>Golang : https://github.com/goinggo</description>
    <link>http://www.goinggo.net/</link>
    <item>
        <pubDate>Sun, 15 Mar 2015 15:04:00 +0000</pubDate>
        <title>Object Oriented Programming Mechanics</title>
        <description>Go is an object oriented language.</description>
        <link>http://www.goinggo.net/2015/03/object-oriented</link>
    </item>
</channel>
</rss>`

func mockServer() *httptest.Server {
    f := func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(200)
        w.Header().Set("Content-Type", "application/xml")
        fmt.Fprintln(w, feed)
    }
    return httptest.NewServer(http.HandlerFunc(f))
}

func TestDownload(t *testing.T) {
    statusCode := 200
    server := mockServer()
    defer server.Close()

    resp, err := http.Get(server.URL)
    if err != nil {
        t.Fatalf("unable to issue GET on the URL: %s: %s", server.URL, err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != statusCode {
        t.Log("exp:", statusCode)
        t.Log("got:", resp.StatusCode)
        t.Fatal("status codes don't match")
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Web Call Mocking"*

---

### Testing — Internal Endpoint Testing (httptest.NewRequest + Recorder)
`#testing`

**Code:**
```go
package handlers

import (
    "encoding/json"
    "net/http"
)

func Routes() {
    http.HandleFunc("/sendjson", sendJSON)
}

func sendJSON(rw http.ResponseWriter, r *http.Request) {
    u := struct {
        Name  string
        Email string
    }{
        Name:  "Bill",
        Email: "bill@ardanlabs.com",
    }
    rw.Header().Set("Content-Type", "application/json")
    rw.WriteHeader(200)
    json.NewEncoder(rw).Encode(&u)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Internal Web Endpoints"*

**Code (test using ServeHTTP directly — no network):**
```go
package handlers_test

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/ardanlabs/gotraining/app/handlers"
)

func init() {
    handlers.Routes()
}

func TestSendJSON(t *testing.T) {
    url := "/sendjson"
    statusCode := 200

    r := httptest.NewRequest("GET", url, nil)
    w := httptest.NewRecorder()
    http.DefaultServeMux.ServeHTTP(w, r)

    if w.Code != 200 {
        t.Log("exp:", statusCode)
        t.Log("got:", w.Code)
        t.Fatal("status codes don't match")
    }

    var u struct {
        Name  string
        Email string
    }
    if err := json.NewDecoder(w.Body).Decode(&u); err != nil {
        t.Fatal("unable to decode the response:", err)
    }
    // ... assertions on u.Name and u.Email
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Internal Web Endpoints"*

---

### Testing — Sub-Tests and Parallel Sub-Tests
`#testing`

**Principle:** Use `t.Run(name, fn)` for named sub-tests. Create a local copy of loop variables to prevent closure bugs. Call `t.Parallel()` as the first line of the sub-test function.

**Code:**
```go
package sample_test

import (
    "net/http"
    "testing"
)

func TestDownload(t *testing.T) {
    tt := []struct {
        name       string
        url        string
        statusCode int
    }{
        {
            "ok",
            "https://www.ardanlabs.com/blog/index.xml",
            http.StatusOK,
        },
        {
            "notfound",
            "http://rss.cnn.com/rss/cnn_topstorie.rss",
            http.StatusNotFound,
        },
    }

    for _, test := range tt {
        test := test                              // capture!
        tf := func(t *testing.T) {
            t.Parallel()                          // opt into parallel
            resp, err := http.Get(test.url)
            if err != nil {
                t.Fatalf("unable to issue GET/URL: %s: %s", test.url, err)
            }
            defer resp.Body.Close()
            if resp.StatusCode != test.statusCode {
                t.Log("exp:", test.statusCode)
                t.Log("got:", resp.StatusCode)
                t.Fatal("status codes don't match")
            }
        }
        t.Run(test.name, tf)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Sub-Tests"*

```
$ go test -v
$ go test -run TestDownload/ok -v
$ go test -run TestDownload/notfound -v
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Sub-Tests"*

---

### Benchmarking — Basic Benchmark Discipline
`#performance` `#testing`

**Principle:** Benchmark functions start with `Benchmark` + capital letter and take `*testing.B`. Loop `for i := 0; i < b.N; i++`. `b.N` is determined via trial and error (starts at 1, multiplies by 100 until `-benchtime` is met). Always capture return values to prevent the compiler from optimizing the code away.

**Code:**
```go
package basic

import (
    "fmt"
    "testing"
)

var gs string

func BenchmarkSprint(b *testing.B) {
    var s string
    for i := 0; i < b.N; i++ {
        s = fmt.Sprint("hello")
    }
    gs = s
}

func BenchmarkSprintf(b *testing.B) {
    var s string
    for i := 0; i < b.N; i++ {
        s = fmt.Sprintf("hello")
    }
    gs = s
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Benchmark"*

```
$ go test -bench . -benchtime 3s -benchmem
BenchmarkSprint-16  56956252   55.48 ns/op   5 B/op   1 allocs/op
BenchmarkSprintf-16 80984947   42.46 ns/op   5 B/op   1 allocs/op
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Benchmark"*

**Reading the columns:**
- `BenchmarkSprint-16`: name + thread count
- `56956252`: iterations of b.N
- `55.48 ns/op`: time per iteration
- `5 B/op`: bytes allocated per iteration
- `1 allocs/op`: number of heap allocations per iteration

---

### Benchmarking — Validate Benchmarks (Benchmarks Lie)
`#performance` `#testing`

**Principle:** Rule #1: the machine must be idle. Run benchmarks in isolation. Goroutine cleanup from previous benchmarks pollutes results.

**Code (merge sort comparison):**
```go
func merge(l, r []int) []int {
    ret := make([]int, 0, len(l)+len(r))
    for {
        switch {
        case len(l) == 0:
            return append(ret, r...)
        case len(r) == 0:
            return append(ret, l...)
        case l[0] <= r[0]:
            ret = append(ret, l[0])
            l = l[1:]
        default:
            ret = append(ret, r[0])
            r = r[1:]
        }
    }
}

func single(n []int) []int {
    if len(n) <= 1 {
        return n
    }
    i := len(n) / 2
    l := single(n[:i])
    r := single(n[i:])
    return merge(l, r)
}

func unlimited(n []int) []int {
    if len(n) <= 1 {
        return n
    }
    i := len(n) / 2
    var l, r []int
    var wg sync.WaitGroup
    wg.Add(2)
    go func() {
        l = unlimited(n[:i])
        wg.Done()
    }()
    go func() {
        r = unlimited(n[i:])
        wg.Done()
    }()
    wg.Wait()
    return merge(l, r)
}

func numCPU(n []int, lvl int) []int {
    if len(n) <= 1 {
        return n
    }
    i := len(n) / 2
    var l, r []int
    maxLevel := int(math.Log2(float64(runtime.GOMAXPROCS(0))))
    if lvl <= maxLevel {
        lvl++
        var wg sync.WaitGroup
        wg.Add(2)
        go func() {
            l = numCPU(n[:i], lvl)
            wg.Done()
        }()
        go func() {
            r = numCPU(n[i:], lvl)
            wg.Done()
        }()
        wg.Wait()
        return merge(l, r)
    }
    l = numCPU(n[:i], lvl)
    r = numCPU(n[i:], lvl)
    return merge(l, r)
}

func BenchmarkSingle(b *testing.B) {
    for i := 0; i < b.N; i++ {
        single(n)
    }
}
func BenchmarkUnlimited(b *testing.B) {
    for i := 0; i < b.N; i++ {
        unlimited(n)
    }
}
func BenchmarkNumCPU(b *testing.B) {
    for i := 0; i < b.N; i++ {
        numCPU(n, 0)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Validate Benchmarks"*

```
$ go test -bench . -benchtime 3s
BenchmarkSingle-16      52    66837183 ns/op
BenchmarkUnlimited-16   13   251840589 ns/op
BenchmarkNumCPU-16      85    38004899 ns/op    # when isolated: faster still
```
*Ref: The_Ultimate_Go_Notebook.md — "Validate Benchmarks"*

**Do:** Run suspected-fast benchmark in isolation. Compare via `benchstat`.

---

### Benchmarking — Sub-Benchmarks
`#performance` `#testing`

**Code:**
```go
var gs string

func BenchmarkSprint(b *testing.B) {
    b.Run("none", benchSprint)
    b.Run("format", benchSprintf)
}

func benchSprint(b *testing.B) {
    var s string
    for i := 0; i < b.N; i++ {
        s = fmt.Sprint("hello")
    }
    gs = s
}

func benchSprintf(b *testing.B) {
    var s string
    for i := 0; i < b.N; i++ {
        s = fmt.Sprintf("hello")
    }
    gs = s
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Sub-Benchmarks"*

```
$ go test -bench .
$ go test -bench BenchmarkSprint/none
$ go test -bench BenchmarkSprint/format
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Sub-Benchmarks"*

---

### Generics — Basic Generic Function Syntax
`#go`

**Principle:** Type parameter lists use square brackets. Each type parameter has a constraint (interface). `any` is predeclared and permits any type. Type inference often eliminates explicit type args at the call site.

**Code:**
```go
func print[T any](slice []T) {
    fmt.Print("Generic: ")
    for _, v := range slice {
        fmt.Print(v, " ")
    }
    fmt.Print("\n")
}

// Explicit type arguments.
numbers := []int{1, 2, 3}
print[int](numbers)

strings := []string{"A", "B", "C"}
print[string](strings)

// With inference.
print(numbers)
print(strings)
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Syntax"*

---

### Generics — Generic Underlying Type
`#go`

**Code:**
```go
type vector[T any] []T

func (v vector[T]) last() (T, error) {
    var zero T
    if len(v) == 0 {
        return zero, errors.New("empty")
    }
    return v[len(v)-1], nil
}

// Equivalent zero-value construction:
// var zero T   OR   *new(T)

// Zero Value Construction:
var vGenInt vector[int]
var vGenStr vector[string]

// Non-Zero Value Construction (compiler infers T):
vGenInt := vector{10, -1}
vGenStr := vector{"A", "B", string([]byte{0xff})}
```
*Ref: The_Ultimate_Go_Notebook.md — "Underlying Types"*

---

### Generics — Generic Struct Types
`#go`

**Code:**
```go
type node[T any] struct {
    Data T
    next *node[T]
    prev *node[T]
}

type list[T any] struct {
    first *node[T]
    last  *node[T]
}

func (l *list[T]) add(data T) *node[T] {
    n := node[T]{
        Data: data,
        prev: l.last,
    }
    if l.first == nil {
        l.first = &n
        l.last = &n
        return &n
    }
    l.last.next = &n
    l.last = &n
    return &n
}

type user struct{ name string }

func main() {
    var lv list[user]
    n1 := lv.add(user{"bill"})
    n2 := lv.add(user{"ale"})
    fmt.Println(n1.Data, n2.Data)

    var lp list[*user]
    n3 := lp.add(&user{"bill"})
    n4 := lp.add(&user{"ale"})
    fmt.Println(n3.Data, n4.Data)
}
// Output:
// {bill} {ale}
// &{bill} &{ale}
```
*Ref: The_Ultimate_Go_Notebook.md — "Struct Types"*

---

### Generics — Behavior as Constraint (Interface)
`#go`

**Code:**
```go
type User struct {
    name string
}

func (u User) String() string {
    return u.name
}

type Stringer interface {
    String() string
}

func Concrete(u User) {
    u.String()
}

func Polymorphic(s Stringer) {
    s.String()
}

func stringify[T fmt.Stringer](slice []T) []string {
    ret := make([]string, 0, len(slice))
    for _, value := range slice {
        ret = append(ret, value.String())
    }
    return ret
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Behavior As Constraint"*

---

### Generics — Type as Constraint (Type List)
`#go`

**Code:**
```go
type addOnly interface {
    type string, int, int8, int16, int32, int64, float64
}

func Add[T addOnly](v1 T, v2 T) T {
    return v1 + v2
}

// Predeclared comparable.
func index[T comparable](list []T, find T) int {
    for i, v := range list {
        if v == find {
            return i
        }
    }
    return -1
}

// Interface combining type list + method set.
type matcher[T any] interface {
    type person, food
    match(v T) bool
}

func match[T matcher[T]](list []T, find T) int {
    for i, v := range list {
        if v.match(find) {
            return i
        }
    }
    return -1
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Type As Constraint"*

---

### Generics — Multi-Type Parameters
`#go`

**Code:**
```go
func Print[L any, V fmt.Stringer](labels []L, vals []V) {
    for i, v := range vals {
        fmt.Println(labels[i], v.String())
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Multi-Type Parameters"*

---

### Generics — Field Access Without Setter Pollution
`#go`

**Code:**
```go
type User struct {
    ID    int64
    Name  string
    Email string
}

type Customer struct {
    ID    int64
    Name  string
    Email string
}

type entities interface {
    type User, Customer
}

func insert[T entities](db *sql.DB, entity T, query string, args ...interface{}) (T, error) {
    var zero T
    result, err := ExecuteQuery(query, args...)
    if err != nil {
        return zero, err
    }
    id, err := result.LastInsertId()
    if err != nil {
        return zero, err
    }
    entity.ID = id // compiler permits assignment because all listed types have ID
    return entity, nil
}

func InsertUser(db *sql.DB, u User) (User, error) {
    const query = "insert into users (name, email) values ($1, $2)"
    u, err := insert(db, u, query, u.Name, u.Email)
    if err != nil {
        return User{}, err
    }
    return u, nil
}

func InsertCustomer(db *sql.DB, c Customer) (Customer, error) {
    const query = "insert into customers (name, email) values ($1, $2)"
    u, err := insert(db, u, query, u.Name, u.Email)
    if err != nil {
        return User{}, err
    }
    return u, nil
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Field Access"*

---

### Generics — Slice Constraints Preserve User-Defined Types
`#go`

**Code:**
```go
type Numbers []int

type operateFunc[T any] func(t T) T

type Slice[T any] interface {
    type []T
}

func operate[S Slice[T], T any](slice S, fn operateFunc[T]) S {
    ret := make(S, len(slice))
    for i, v := range slice {
        ret[i] = fn(v)
    }
    return ret
}

func Double(n Numbers) Numbers {
    fn := func(n int) int {
        return 2 * n
    }
    numbers := operate(n, fn)
    fmt.Printf("%T", numbers)
    return numbers
}
// Output: main.Numbers   (NOT []int — user-defined type preserved)
```
*Ref: The_Ultimate_Go_Notebook.md — "Slice Constraints"*

---

### Generics — Concurrent Work with Generic Channels
`#go` `#concurrency`

**Code:**
```go
type workFn[Result any] func(context.Context) Result

func doWork[Result any](ctx context.Context, work workFn[Result]) chan Result {
    ch := make(chan Result, 1)
    go func() {
        ch <- work(ctx)
        fmt.Println("doWork : work complete")
    }()
    return ch
}

func main() {
    duration := 100 * time.Millisecond
    ctx, cancel := context.WithTimeout(context.Background(), duration)
    defer cancel()

    dwf := func(ctx context.Context) string {
        time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
        return "work complete"
    }

    result := doWork(ctx, dwf)
    select {
    case v := <-result:
        fmt.Println("main:", v)
    case <-ctx.Done():
        fmt.Println("main: timeout")
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Channels"*

**Code (generic poolWork):**
```go
type poolWorkFn[Input any, Result any] func(input Input) Result

func poolWork[Input any, Result any](
    size int,
    work poolWorkFn[Input, Result],
) (chan Input, func()) {
    var wg sync.WaitGroup
    wg.Add(size)
    ch := make(chan Input)

    for i := 0; i < size; i++ {
        go func() {
            defer wg.Done()
            for input := range ch {
                result := work(input)
                fmt.Println("pollWork :", result)
            }
        }()
    }

    cancel := func() {
        close(ch)
        wg.Wait()
    }
    return ch, cancel
}

func main() {
    size := runtime.GOMAXPROCS(0)
    pwf := func(input int) string {
        time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
        return fmt.Sprintf("%d : received", input)
    }
    ch, cancel := poolWork(size, pwf)
    defer cancel()
    for i := 0; i < 4; i++ {
        ch <- i
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Channels"*

---

### Generics — Hash Table Example
`#go`

**Code:**
```go
type hashFunc[K comparable] func(key K, buckets int) int

type keyValuePair[K comparable, V any] struct {
    Key   K
    Value V
}

type Table[K comparable, V any] struct {
    hashFunc hashFunc[K]
    buckets  int
    data     [][]keyValuePair[K, V]
}

func New[K comparable, V any](
    buckets int,
    hf hashFunc[K],
) *Table[K, V] {
    return &Table[K, V]{
        hashFunc: hf,
        buckets:  buckets,
        data:     make([][]keyValuePair[K, V], buckets),
    }
}

func (t *Table[K, V]) Insert(key K, value V) {
    bucket := t.hashFunc(key, t.buckets)
    for idx, kvp := range t.data[bucket] {
        if key == kvp.Key {
            t.data[bucket][idx].Value = value
            return
        }
    }
    kvp := keyValuePair[K, V]{
        Key:   key,
        Value: value,
    }
    t.data[bucket] = append(t.data[bucket], kvp)
}

func (t *Table[K, V]) Get(key K) (V, bool) {
    bucket := t.hashFunc(key, t.buckets)
    for idx, kvp := range t.data[bucket] {
        if key == kvp.Key {
            return t.data[bucket][idx].Value, true
        }
    }
    var zero V
    return zero, false
}

// Usage:
func main() {
    const buckets = 8

    hashFunc1 := func(key string, buckets int) int {
        h := fnv.New32()
        h.Write([]byte(key))
        return int(h.Sum32()) % buckets
    }
    table1 := New[string, int](buckets, hashFunc1)

    hashFunc2 := func(key int, buckets int) int {
        return key % buckets
    }
    table2 := New[int, string](buckets, hashFunc2)

    words := []string{"foo", "bar", "baz"}
    for i, word := range words {
        table1.Insert(word, i)
        table2.Insert(i, word)
    }
    for i, s := range append(words, "nope!") {
        v1, ok1 := table1.Get(s)
        fmt.Printf("t1.Rtr(%v) = (%v, %v)\n", s, v1, ok1)
        v2, ok2 := table2.Get(i)
        fmt.Printf("t2.Rtr(%v) = (%v, %v)\n", i, v2, ok2)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Hash Tables"*

---

### Profiling — Three Profile Types (CPU, Memory, Blocking)
`#performance`

**Principle:** The profiler sends SIGPROF at intervals, capturing program counters.

- **CPU profile**: Stack trace every ~10ms.
- **Memory profile**: Sample per 512KB allocated by default. Stack allocations not tracked.
- **Blocking profile**: Time goroutines spend waiting on shared resources. Specialized — use only after CPU and memory bottlenecks are resolved.

**One profile at a time.** Multiple profiles observe their own interactions and skew results.

*Ref: The_Ultimate_Go_Notebook.md — "The Basics of Profiling"*

---

### Profiling — Stable Environment Do's and Don'ts
`#performance`

**Do:**
- Idle machine — no shared hardware.
- Disable power saving and thermal scaling.
- Use dedicated performance hardware if possible.
- Run with `before` and `after` samples, multiple times.

**Don't:**
- Profile on VMs or shared cloud hosting — too noisy.
- Browse the web during a long benchmark.

*Ref: The_Ultimate_Go_Notebook.md — "The Basics of Profiling"*

---

### Profiling — Reading Profile Hints
`#performance`

**If you see…** then…
- Lots of `runtime.mallocgc` → excessive small allocations. Use memory profile.
- Lots of channel/mutex/sync time → contention. Shard, partition, batch, copy-on-write.
- Lots of `syscall.Read/Write` → wrap files/connections in `bufio`.
- Lots of GC time → too many transient objects OR heap too small.
- Large objects → impact memory consumption and GC pacing.
- Many tiny allocations → hurts marking speed.
- Values without pointers → not scanned by GC; remove pointers from hot values.

**Do:**
- Combine values into larger values to reduce allocation count and GC pressure.
- Remove pointers from actively used values.

*Ref: The_Ultimate_Go_Notebook.md — "The Basics of Profiling"*

---

### Profiling — Stream Processing Example (algOne vs algTwo)
`#performance`

**Code:**
```go
var data = []struct {
    input  []byte
    output []byte
}{
    {[]byte("abc"), []byte("abc")},
    {[]byte("elvis"), []byte("Elvis")},
    {[]byte("aElvis"), []byte("aElvis")},
    {[]byte("abcelvis"), []byte("abcElvis")},
    {[]byte("eelvis"), []byte("eElvis")},
    {[]byte("aelvis"), []byte("aElvis")},
    {[]byte("aabeeeelvis"), []byte("aabeeeElvis")},
    {[]byte("e l v i s"), []byte("e l v i s")},
    {[]byte("aa bb e l v i saa"), []byte("aa bb e l v i saa")},
    {[]byte(" elvi s"), []byte(" elvi s")},
    {[]byte("elvielvis"), []byte("elviElvis")},
    {[]byte("elvielvielviselvi1"), []byte("elvielviElviselvi1")},
    {[]byte("elvielviselvis"), []byte("elviElvisElvis")},
}

func assembleInputStream() []byte {
    var in []byte
    for _, d := range data {
        in = append(in, d.input...)
    }
    return in
}

func assembleOutputStream() []byte {
    var out []byte
    for _, d := range data {
        out = append(out, d.output...)
    }
    return out
}

// algOne — Bill's algorithm
func algOne(data []byte, find []byte, repl []byte, output *bytes.Buffer) {
    input := bytes.NewBuffer(data)
    size := len(find)
    buf := make([]byte, size)
    end := size - 1

    if n, err := io.ReadFull(input, buf[:end]); err != nil {
        output.Write(buf[:n])
        return
    }
    for {
        if _, err := io.ReadFull(input, buf[end:]); err != nil {
            output.Write(buf[:end])
            return
        }
        if bytes.Equal(buf, find) {
            output.Write(repl)
            if n, err := io.ReadFull(input, buf[:end]); err != nil {
                output.Write(buf[:n])
                return
            }
            continue
        }
        output.WriteByte(buf[0])
        copy(buf, buf[1:])
    }
}

// algTwo — Tyler's algorithm
func algTwo(data []byte, find []byte, repl []byte, output *bytes.Buffer) {
    input := bytes.NewReader(data)
    size := len(find)
    idx := 0
    for {
        b, err := input.ReadByte()
        if err != nil {
            break
        }
        if b == find[idx] {
            idx++
            if idx == size {
                output.Write(repl)
                idx = 0
            }
            continue
        }
        if idx != 0 {
            output.Write(find[:idx])
            input.UnreadByte()
            idx = 0
            continue
        }
        output.WriteByte(b)
        idx = 0
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Example Code"*

**Benchmark:**
```go
var output bytes.Buffer
var in = assembleInputStream()
var find = []byte("elvis")
var repl = []byte("Elvis")

func BenchmarkAlgorithmOne(b *testing.B) {
    for i := 0; i < b.N; i++ {
        output.Reset()
        algOne(in, find, repl, &output)
    }
}

func BenchmarkAlgorithmTwo(b *testing.B) {
    for i := 0; i < b.N; i++ {
        output.Reset()
        algTwo(in, find, repl, &output)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Benchmarking"*

```
BenchmarkAlgorithmOne-16  2120113  1594 ns/op  53 B/op  2 allocs/op
BenchmarkAlgorithmTwo-16  9103246   387.7 ns/op  0 B/op  0 allocs/op
```
*Ref: The_Ultimate_Go_Notebook.md — "Benchmarking"*

---

### Profiling — Memory Profile Workflow
`#performance`

```
$ go test -bench . -benchtime 3s -benchmem -memprofile p.out
$ go tool pprof memcpu.test p.out
(pprof) list algOne
Total: 167.51MB
12.50MB 167.51MB (flat, cum) 100% of Total
.          .         78:
.          .         79:// algOne is one way to solve the problem.
.          .         80:func algOne(data []byte, find []byte, repl []byte,
.          .         81:                  output *bytes.Buffer) {
.          .         82: // Use a bytes Buffer to provide a stream
.   155.01MB         83: input := bytes.NewBuffer(data)
.          .         84:
.          .         85: // The number of bytes we are looking for.
.          .         86: size := len(find)
.          .         87:
.          .         88: // Declare the buffers we need to process
12.50MB   12.50MB    89: buf := make([]byte, size)
```
*Ref: The_Ultimate_Go_Notebook.md — "Memory Profiling"*

---

### Profiling — Inlining and the Ownership Rule
`#performance`

**Principle:** If a factory function is inlined (cost < 80), ownership of value construction moves up to the caller. The value no longer needs to escape just because the factory returned `&`.

**Code:**
```go
// Original NewBuffer factory — small enough to inline:
func NewBuffer(buf []byte) *Buffer {
    return &Buffer{buf: buf}
}

// Inside algOne after inlining:
// Before:  input := bytes.NewBuffer(data)
// After:   input := &bytes.Buffer{buf: data}
```
*Ref: The_Ultimate_Go_Notebook.md — "Inlining"*

**Inlining scoring:**
```
./stream.go:80:6: cannot inline algOne: function too complex: cost 636 exceeds budget 80
./stream.go:131:6: cannot inline algTwo: function too complex: cost 315 exceeds budget 80
```
*Ref: The_Ultimate_Go_Notebook.md — "Inlining"*

**Do:** Make factory functions leaf functions to maximize inlinability.

---

### Profiling — Escape Analysis With -gcflags=-m=2
`#performance`

**Principle:** The compiler decides escapes; ask it why with `go test -gcflags -m=2`.

```
./stream.go:83:26: inlining call to bytes.NewBuffer func([]byte) *bytes.Buffer { return &bytes.Buffer{...} }
./stream.go:83:26: &bytes.Buffer{...} escapes to heap:
./stream.go:83:26: flow: io.r = input:
./stream.go:83:26:   from input (interface-converted) at ./stream.go:113:28
./stream.go:83:26:   from io.ReadAtLeast(io.r, io.buf, len(io.buf)) (call parameter) at ./stream.go:113:28
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

**Root cause:** `io.ReadFull(input, buf[:end])` accepts `io.Reader` — an interface conversion forces escape. Fix: call methods directly on the concrete value.

**Code (fixed — call method set, not io package):**
```go
func algOne(data []byte, find []byte, repl []byte, output *bytes.Buffer) {
    input := bytes.NewBuffer(data)
    size := len(find)
    buf := make([]byte, size)
    end := size - 1

    if n, err := input.Read(buf[:end]); err != nil {  // <-- direct method
        output.Write(buf[:n])
        return
    }
    for {
        var err error
        buf[end:][0], err = input.ReadByte()          // <-- direct method
        if err != nil {
            output.Write(buf[:end])
            return
        }
        if bytes.Equal(buf, find) {
            output.Write(repl)
            if n, err := input.Read(buf[:end]); err != nil {  // <-- direct method
                output.Write(buf[:n])
                return
            }
            continue
        }
        output.WriteByte(buf[0])
        copy(buf, buf[1:])
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

```
BenchmarkAlgorithmOne-16  3658340  975.3 ns/op   5 B/op  1 allocs/op
BenchmarkAlgorithmTwo-16  9730435  377.6 ns/op   0 B/op  0 allocs/op
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

---

### Profiling — Constant Size Eliminates Final Allocation
`#performance`

**Principle:** `make([]byte, size)` escapes when `size` is not constant. Hard-coding the size when known at compile time lets the compiler keep it on the stack.

**Code:**
```go
func algOne(data []byte, find []byte, repl []byte, output *bytes.Buffer) {
    input := bytes.NewBuffer(data)
    size := len(find)
    buf := make([]byte, 5) // <-- REPLACED: literal 5 instead of size
    // ...
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

```
BenchmarkAlgorithmOne-16  4129378  868.5 ns/op  0 B/op  0 allocs/op
BenchmarkAlgorithmTwo-16  9716834  376.0 ns/op  0 B/op  0 allocs/op
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis"*

---

### Profiling — CPU Profile Workflow
`#performance`

```
$ go test -bench . -benchtime 3s -benchmem -cpuprofile p.out
$ go tool pprof p.out
(pprof) list algOne
950ms   3.97s (flat, cum) 53.36% of Total
.          .        87:// Declare the buffers we need to process the stream.
.          .        88: buf := make([]byte, 5)
.          .        89: end := size - 1
.          .        90:
.          .        91:// Read in an initial number of bytes
110ms     120ms     92: if n, err := input.Read(buf[:end]); err != nil {
.          .        93: output.Write(buf[:n])
.          .        94: return
.          .        95: }
.          .        96:
.          .        97: for {
.          .        98:
.          .        99:// Read in one byte from the input
310ms     440ms    101: buf[end:][0], err = input.ReadByte()
.          .       102: if err != nil {
.          .       103:
.          .       104:// Flush the rest of the bytes
.          .       105: output.Write(buf[:end])
.          .       106: return
.          .       107: }
.          .       108:
.          .       109:// If we have a match, replace the
.   1.70s          110: if bytes.Equal(buf, find) {
270ms     650ms    111: output.Write(repl)
```
*Ref: The_Ultimate_Go_Notebook.md — "Profiling"*

---

### Profiling Live Code — GC Trace Anatomy
`#performance`

```
$ GODEBUG=gctrace=1 ./project > /dev/null
gc 4 @95.976s 0%: 0.048+0.47+0.016 ms clock,
0.78+0.13/1.0/1.3+0.25 ms cpu, 4->4->2 MB, 5 MB goal, 16 P
```

| Section | Meaning |
|---|---|
| `gc 4` | 4th GC run since start |
| `@95.976s` | Wall-clock seconds since start |
| `0%` | % of program time in GC |
| `0.048+0.47+0.016 ms clock` | Wall: Mark Setup STW / Mark Concurrent / Mark Termination STW |
| `0.78+0.13/1.0/1.3+0.25 ms cpu` | CPU: STW setup / Assist / Background / Idle / STW term |
| `4->4->2 MB` | Heap in-use before / in-use after / marked live |
| `5 MB goal` | Collection goal |
| `16 P` | Logical processors |

*Ref: The_Ultimate_Go_Notebook.md — "Generating a GC Trace"*

---

### Profiling Live Code — Load Testing With `hey`
`#performance`

**Code:**
```bash
$ hey -m POST -c 100 -n 10000 "http://localhost:5000/search?term=biden&cnn=on&bbc=on&nyt=on"

Summary:
Total:        2.6945 secs
Slowest:      0.2664 secs
Fastest:      0.0011 secs
Average:      0.0248 secs
Requests/sec: 3711.3009
```
*Ref: The_Ultimate_Go_Notebook.md — "Generating Load And Evaluation"*

---

### Profiling Live Code — Registering pprof Endpoints
`#performance`

**Code:**
```go
package main

import (
    _ "net/http/pprof" // call init function — registers debug routes
)

func main() {
    debugHost := ":5000"
    go func() {
        log.Printf("main: Debug Listening %s", debugHost)
        err := http.ListenAndServe(debugHost, http.DefaultServeMux)
        if err != nil {
            log.Printf("main: Debug Listener closed: %v", err)
        }
    }()
    // ...
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Adding Profile Endpoints"*

```
import _ "net/http/pprof"
// calls init that registers:
//   /debug/pprof/
//   /debug/pprof/cmdline
//   /debug/pprof/profile
//   /debug/pprof/symbol
//   /debug/pprof/trace
```
*Ref: The_Ultimate_Go_Notebook.md — "Adding Profile Endpoints"*

**Do:** Bind the debug mux to a separate port behind a firewall.

---

### Profiling Live Code — Hunting Allocations via `top` and `list`
`#performance`

```
$ go tool pprof -noinlines http://localhost:5000/debug/pprof/allocs
(pprof) top 15 -cum
Showing nodes accounting for 3300.39MB, 53.67% of 6148.89MB total

flat       flat%   sum%   cum          cum%
0          0%      0%     3675.30MB   59.77%   net/http.(*conn).serve
385.68MB   6.27%   6.27%  3653.77MB   59.42%   ...service.handler
617.76MB   10.05%  16.32% 3055.01MB   49.68%   ...service.render
48.01MB    0.78%   17.10% 2445.06MB   39.76%   ...search.rssSearch
2235.93MB  36.36%  53.52% 2393.53MB   38.93%   strings.ToLower
```
*Ref: The_Ultimate_Go_Notebook.md — "Viewing Memory Profile"*

```
(pprof) list rssSearch
Total: 6GB
ROUTINE ======================== project/search/rss.go
48.01MB    2.39GB (flat, cum) 39.76% of Total
20.50MB    20.50MB   79:  var d Document
.          3.52MB    102: if err := xml.NewDecoder(resp.Bod
.          2.34GB    119: if strings.Contains(strings.ToLower(ite
27.51MB    27.51MB   120: results = append(results, Result{
```
*Ref: The_Ultimate_Go_Notebook.md — "Viewing Memory Profile"*

---

### Profiling Live Code — Removing Allocations (Search Example)
`#performance`

**Before (2.34 GB allocated per 10k requests):**
```go
for _, item := range d.Channel.Items {
    if strings.Contains(strings.ToLower(item.Description),
        strings.ToLower(term)) {
        results = append(results, Result{
            Engine:  engine,
            Title:   item.Title,
            Link:    item.Link,
            Content: item.Description,
        })
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Removing Allocations"*

**After — move `ToLower(term)` out of loop; precompute lowercased description at cache time:**
```go
// At search time:
term = strings.ToLower(term)

for _, item := range d.Channel.Items {
    if strings.Contains(item.Description, term) {
        results = append(results, Result{
            Engine:  engine,
            Title:   item.Title,
            Link:    item.Link,
            Content: item.Description,
        })
    }
}

// At cache time:
for i := range d.Channel.Items {
    lower := strings.ToLower(d.Channel.Items[i].Description)
    d.Channel.Items[i].Description = lower
}
cache.Set(uri, d, expiration)
```
*Ref: The_Ultimate_Go_Notebook.md — "Removing Allocations"*

**Result:**
```
Before:  3,711 req/s, 836 GCs, ~6.1 GB allocated
After:   6,960 req/s,  483 GCs  (88% improvement)
```
*Ref: The_Ultimate_Go_Notebook.md — "Removing Allocations"*

---

### Tracing — Generating Traces
`#performance`

**Code:**
```go
import (
    "runtime/trace"
)

func main() {
    trace.Start(os.Stdout)
    defer trace.Stop()

    docs := make([]string, 4000)
    for i := range docs {
        docs[i] = fmt.Sprintf("newsfeed-%.4d.xml", i)
    }
    topic := "president"
    n := freq(topic, docs)
    log.Printf("Search %d files, found %s %d times.", len(docs), topic, n)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Generating Traces"*

```
$ go build
$ time ./trace > t.out
$ go tool trace t.out
```
*Ref: The_Ultimate_Go_Notebook.md — "Generating Traces"*

**Do:** Keep traces small — a few seconds at most. The data set is large.

---

### Tracing — Baseline Metrics (Single-Threaded freq)
`#performance`

| Metric           | Single  |
|------------------|---------|
| Runtime          | 2670ms  |
| Top Memory       | 4 MB    |
| GC Occurrences   | 275     |
| GC Avg Duration  | 387us   |
| GC Wall Duration | 106ms   |
| GC Time Spent    | 4%      |

*Ref: The_Ultimate_Go_Notebook.md — "Viewing Traces"*

**Code (freq function):**
```go
func freq(topic string, docs []string) int {
    var found int
    for _, doc := range docs {
        file := fmt.Sprintf("%s.xml", doc[:8])
        f, err := os.OpenFile(file, os.O_RDONLY, 0)
        if err != nil {
            log.Printf("Opening Document [%s] : ERROR : %v", doc, err)
            return 0
        }
        data, err := io.ReadAll(f)
        f.Close()
        if err != nil {
            log.Printf("Reading Document [%s] : ERROR : %v", doc, err)
            return 0
        }
        var d document
        if err := xml.Unmarshal(data, &d); err != nil {
            log.Printf("Decoding Document [%s] : ERROR : %v", doc, err)
            return 0
        }
        for _, item := range d.Channel.Items {
            if strings.Contains(item.Title, topic) {
                found++
                continue
            }
            if strings.Contains(item.Description, topic) {
                found++
            }
        }
    }
    return found
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Example Code"*

---

### Tracing — Fan-Out Concurrent Version
`#performance` `#concurrency`

**Code:**
```go
func freq(topic string, docs []string) int {
    var found int32
    g := len(docs)
    var wg sync.WaitGroup
    wg.Add(g)
    for _, doc := range docs {
        go func(doc string) {
            var lFound int32
            defer func() {
                atomic.AddInt32(&found, lFound)
                wg.Done()
            }()
            // ... file open, read, unmarshal, search ...
            for _, item := range d.Channel.Items {
                if strings.Contains(item.Title, topic) {
                    lFound++
                    continue
                }
                if strings.Contains(item.Description, topic) {
                    lFound++
                }
            }
        }(doc)
    }
    wg.Wait()
    return int(found)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Fan-Out"*

**Cache friendliness:** Per-goroutine local `lFound` counter; add to the shared `found` exactly once per goroutine via `defer`. This converts 28k atomic ops into 4k.

*Ref: The_Ultimate_Go_Notebook.md — "Cache Friendly"*

| Metric           | Single  | Fan-Out |
|------------------|---------|---------|
| Runtime          | 2670ms  | 580ms   |
| Top Memory       | 4 MB    | 53 MB   |
| GC Occurrences   | 275     | 62      |
| GC Avg Duration  | 387us   | 4ms     |
| GC Wall Duration | 106ms   | 250ms   |
| GC Time Spent    | 4%      | 43%     |

*Ref: The_Ultimate_Go_Notebook.md — "Fan-Out Results"*

---

### Tracing — Pooling Pattern
`#performance` `#concurrency`

**Code:**
```go
func freq(topic string, docs []string) int {
    var found int32
    g := runtime.GOMAXPROCS(0)
    var wg sync.WaitGroup
    wg.Add(g)
    ch := make(chan string, g)

    for i := 0; i < g; i++ {
        go func() {
            var lFound int32
            defer func() {
                atomic.AddInt32(&found, lFound)
                wg.Done()
            }()
            for doc := range ch {
                // ... process doc ...
            }
        }()
    }

    for _, doc := range docs {
        ch <- doc
    }
    close(ch)
    wg.Wait()
    return int(found)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Pooling"*

| Metric           | Single  | Fan-Out | Pooling |
|------------------|---------|---------|---------|
| Runtime          | 2670ms  | 580ms   | 1000ms  |
| Top Memory       | 4 MB    | 53 MB   | 5 MB    |
| GC Occurrences   | 275     | 62      | 876     |
| GC Avg Duration  | 387us   | 4ms     | 690us   |
| GC Wall Duration | 106ms   | 250ms   | 604ms   |
| GC Time Spent    | 4%      | 43%     | 60%     |

*Ref: The_Ultimate_Go_Notebook.md — "Pooling Results"*

---

### Tracing — GC Percentage Tuning (GOGC / SetGCPercent)
`#performance`

**Principle:** `GOGC=100` (default) means: trigger next GC when heap doubles from the last live size. Setting `GOGC=1000` lets the heap grow 10x before next GC — fewer GCs, more memory.

```
$ time GOGC=1000 ./trace > t.out
2021/05/13 14:43:06 Searching 4000 files, found president 28000 times.
GOGC=1000 ./trace > t.out  5.48s user 0.29s system 1404% cpu 0.411 total
```
*Ref: The_Ultimate_Go_Notebook.md — "GC Percentage"*

| Metric           | Single | Fan-Out | Pooling | GC%=1000 |
|------------------|--------|---------|---------|----------|
| Runtime          | 2670ms | 580ms   | 1000ms  | 397ms    |
| Top Memory       | 4 MB   | 53 MB   | 5 MB    | 40 MB    |
| GC Occurrences   | 275    | 62      | 876     | 27       |
| GC Wall Duration | 106ms  | 250ms   | 604ms   | 19ms     |
| GC Time Spent    | 4%     | 43%     | 60%     | 4%       |

*Ref: The_Ultimate_Go_Notebook.md — "GC Percentage"*

**Code (programmatic setting):**
```go
import (
    "runtime/debug"
)

func main() {
    debug.SetGCPercent(1000)
    // ...
}
```
*Ref: The_Ultimate_Go_Notebook.md — "GC Percentage"*

**Don't:** Hardcode this blindly — it favors memory over GC. Different workloads behave differently.

---

### Tracing — Tasks and Regions (Per-File Timing)
`#performance`

**Code:**
```go
for doc := range ch {
    ctx, task := trace.NewTask(context.Background(), doc)

    reg := trace.StartRegion(ctx, "OpenFile")
    file := fmt.Sprintf("%s.xml", doc[:8])
    f, err := os.OpenFile(file, os.O_RDONLY, 0)
    if err != nil {
        log.Printf("Opening Document [%s] : ERROR : %v", doc, err)
        return
    }
    reg.End()

    reg = trace.StartRegion(ctx, "ReadAll")
    data, err := io.ReadAll(f)
    f.Close()
    if err != nil {
        log.Printf("Reading Document [%s] : ERROR : %v", doc, err)
        return
    }
    reg.End()

    reg = trace.StartRegion(ctx, "Unmarshal")
    var d document
    if err := xml.Unmarshal(data, &d); err != nil {
        log.Printf("Decoding Document [%s] : ERROR : %v", doc, err)
        return
    }
    reg.End()

    reg = trace.StartRegion(ctx, "Contains")
    for _, item := range d.Channel.Items {
        if strings.Contains(item.Title, topic) {
            lFound++
            continue
        }
        if strings.Contains(item.Description, topic) {
            lFound++
        }
    }
    reg.End()

    task.End()
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Tasks And Regions"*

---

### Stack Traces — Reading Function Input Values
`#go`

**Principle:** Stack traces show words of data per function call. The first words are inputs; trailing words are outputs (garbage in a panic).

**Code:**
```go
package main

func main() {
    example(make([]string, 2, 4), "hello", 10)
}

//go:noinline
func example(slice []string, str string, i int) error {
    panic("Want stack trace")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Example"*

**Stack trace (Go 1.16):**
```
goroutine 1 [running]:
main.example(0xc000054738, 0x2, 0x4, 0x1073c53, 0x5, 0xa, 0x0, 0xc000054778)
                .../example1.go:9 +0x39
main.main()
                .../example1.go:4 +0x85
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Example"*

Decoding:
```
Slice value:  0xc000054738, 0x2, 0x4   (pointer, len, cap)
String value: 0x1073c53, 0x5           (pointer, len)
Integer:      0xa                      (10)
Return value: 0x0, 0xc000054778        (nil interface — garbage in panic)
```
*Ref: The_Ultimate_Go_Notebook.md — "Basic Example"*

---

### Stack Traces — Word Packing
`#go`

**Code:**
```go
package main

func main() {
    example(true, false, true, 25)
}

//go:noinline
func example(b1, b2, b3 bool, i uint8) error {
    panic("Want stack trace")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Word Packing"*

```
main.example(0x19010001, 0x1064ee0, 0xc00008c058)
```

Decoding little-endian word:
```
Bits    Binary      Hex   Value
00-07   0000 0001   01    true
08-15   0000 0000   00    false
16-23   0000 0001   01    true
24-31   0001 1001   19    25
```
*Ref: The_Ultimate_Go_Notebook.md — "Word Packing"*

---

### Stack Traces — Go 1.17 ABI Register Changes
`#go`

**Principle:** Go 1.17+ passes some arguments via registers on amd64 (Linux, macOS, Windows). Stack trace accuracy for input values is reduced.

```
Go 1.16: main.example(0xc000054738, 0x2, 0x4, 0x1073c53, 0x5, 0xa, 0x0, 0xc000054778)
Go 1.17: main.example({0x60, 0x10bb6c0, 0xc0000002e8}, {0xc000024060, 0x0}, 0xc0000001a0)
```
*Ref: The_Ultimate_Go_Notebook.md — "Go 1.17 ABI Changes"*

---

### Stack Traces — Core Dumps via SIGQUIT
`#go`

**Code:**
```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/sendjson", sendJSON)
    log.Println("listener : Started : Listening on: http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}

func sendJSON(rw http.ResponseWriter, r *http.Request) {
    u := struct {
        Name  string
        Email string
    }{
        Name:  "bill",
        Email: "bill@ardanlabs.com",
    }
    rw.Header().Set("Content-Type", "application/json")
    rw.WriteHeader(200)
    json.NewEncoder(rw).Encode(u)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Generating Core Dumps"*

```
$ go build
$ ./example3 &
$ kill -3 <pid>           # sends SIGQUIT — Go dumps stack traces
$ GOTRACEBACK=crash ./example3   # larger dump including runtime goroutines
```
*Ref: The_Ultimate_Go_Notebook.md — "Generating Core Dumps"*

---

### Blog Post — Frame Boundaries and Pass-By-Value
`#go`

**Principle:** Functions execute in frame boundaries. Data crosses frames by value. WYSIWYG: the value you see in the call is what is copied. The stack is self-cleaning via zero-value initialization on each function call.

**Code:**
```go
package main

func main() {
    count := 10
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
    increment(count)
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
}

//go:noinline
func increment(inc int) {
    inc++
    println("inc:\tValue Of[", inc, "]\tAddr Of[", &inc, "]")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Stacks And Pointer Mechanics / Function Calls"*

---

### Blog Post — Sharing Values (Pointers)
`#go`

**Code:**
```go
package main

func main() {
    count := 10
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
    increment(&count) // share count with increment
    println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
}

//go:noinline
func increment(inc *int) {
    *inc++ // indirect read-modify-write through pointer
    println("inc:\tValue Of[", inc, "]\tAddr Of[", &inc, "]\tValue Points To[", *inc, "]")
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Stacks And Pointer Mechanics / Sharing Values"*

**Key vocabulary:** Replace `&` with the word "sharing" when reading code.

---

### Blog Post — Stack Growth Mechanics
`#go`

**Principle:** No goroutine may point into another goroutine's stack — when the stack grows, the runtime would have to track and fix too many pointers.

**Code (stack growth observable via changing addresses):**
```go
package main

const size = 4096

func main() {
    s := "HELLO"
    stackCopy(&s, 0, [size]int{})
}

func stackCopy(s *string, c int, a [size]int) {
    println(c, s, *s)
    c++
    if c == 10 {
        return
    }
    stackCopy(s, c, a)
}
// Output:
// 0 0xc00011ff68 HELLO
// 1 0xc00011ff68 HELLO
// 2 0xc00015ff68 HELLO  <-- stack grew, address changed
// 3 0xc00015ff68 HELLO
// ...
// 6 0xc0001dff68 HELLO  <-- grew again
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis Mechanics / Sharing Stacks"*

---

### Blog Post — Heap and Escape Analysis Mechanics
`#go` `#performance`

**Code (two construction styles — one stacks, one escapes):**
```go
package main

type user struct {
    name  string
    email string
}

func main() {
    u1 := createUserV1()
    u2 := createUserV2()
    println("u1", &u1, "u2", &u2)
}

//go:noinline
func createUserV1() user {
    u := user{
        name:  "Bill",
        email: "bill@ardanlabs.com",
    }
    println("V1", &u)
    return u // value semantics -> stays on stack
}

//go:noinline
func createUserV2() *user {
    u := user{
        name:  "Bill",
        email: "bill@ardanlabs.com",
    }
    println("V2", &u)
    return &u // pointer semantics -> escapes to heap
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis Mechanics / Escape Mechanics"*

**Compiler escape report:**
```
$ go build -gcflags -m=2
./example4.go:28:2: u escapes to heap:
./example4.go:28:2: flow: ~r0 = &u:
./example4.go:28:2:   from &u (address-of) at ./example4.go:34:9
./example4.go:28:2:   from return &u (return) at ./example4.go:34:2
./example4.go:28:2: moved to heap: u
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis Mechanics / Compiler Reporting"*

---

### Blog Post — Readability of `&u` vs `u := &user{}`
`#go`

**Principle:** Construction with value semantics (`u := user{...}`) and explicit `return &u` makes sharing visible. Construction with pointer semantics hides it.

**Code (more readable — value construction):**
```go
var u user
err := json.Unmarshal([]byte(r), &u)
return &u, err
// Reads as: create user, share with json, share with caller.
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis Mechanics / Readability"*

**Code (less readable — pointer construction):**
```go
var u *user
err := json.Unmarshal([]byte(r), &u)
return u, err
// Hides that json creates the user; hides that we return it.
```
*Ref: The_Ultimate_Go_Notebook.md — "Escape Analysis Mechanics / Readability"*

---

### Blog Post — Scheduling: Go Scheduler Components
`#concurrency`

**Principle:** Every Go program gets one P per virtual core; each P has an M (OS thread); every Go program starts with one G (goroutine). LRQ per P; GRQ for unassigned goroutines.

**Code (check GOMAXPROCS):**
```go
package main

import (
    "fmt"
    "runtime"
)

func main() {
    fmt.Println(runtime.GOMAXPROCS(0))
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Go Scheduler"*

---

### Blog Post — Scheduler Events That Enable Context Switches
`#concurrency`

Events where the Go scheduler may make a decision:
1. The `go` keyword creates a goroutine.
2. Garbage collection runs (its own goroutines need P time).
3. System calls (sync or async via network poller).
4. Synchronization/orchestration (atomic, mutex, channel ops).

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Go Scheduler / Context Switching"*

---

### Blog Post — Asynchronous System Calls (Network Poller)
`#concurrency`

**Principle:** Network syscalls are handled by the network poller (kqueue/epoll/iocp). The goroutine moves to the poller; the M is free to run other goroutines. No extra M needed.

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Go Scheduler / Asynchronous System Calls"*

---

### Blog Post — Synchronous System Calls (Hand-off)
`#concurrency`

**Principle:** File I/O and CGO block the M. The scheduler detaches the blocked M/P (with the goroutine still attached) and brings in a fresh M to service the LRQ. When the syscall returns, the goroutine re-queues; the old M is parked for reuse.

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Go Scheduler / Synchronous System Calls"*

---

### Blog Post — Work Stealing Scheduler
`#concurrency`

**Principle:** A P with an empty LRQ steals half the goroutines from another P's LRQ, then checks the GRQ, then polls the network. This keeps Ms spinning and busy.

**Pseudocode from runtime.schedule():**
```go
runtime.schedule() {
    // only 1/61 of the time, check the global runnable queue for a G.
    // if not found, check the local queue.
    // if not found, try to steal from other Ps.
    // if not, check the global runnable queue.
    // if not found, poll network.
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Go Scheduler / Work Stealing"*

---

### Blog Post — Concurrency vs Parallelism
`#concurrency`

**Principle:** Concurrency is undefined out-of-order execution. Parallelism is executing instructions simultaneously. You can have concurrency without parallelism (single-core time-slicing), but parallelism requires multiple cores.

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / What is Concurrency"*

---

### Blog Post — CPU-Bound Workload Decisions
`#concurrency` `#performance`

**Principle:** CPU-bound work needs parallelism to benefit from concurrency. More goroutines than hardware threads slows things down due to context-switch overhead.

**Code (sequential add):**
```go
func add(numbers []int) int {
    var v int
    for _, n := range numbers {
        v += n
    }
    return v
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Adding Numbers"*

**Code (concurrent add with stride split):**
```go
func addConcurrent(goroutines int, numbers []int) int {
    var v int64
    totalNumbers := len(numbers)
    lastGoroutine := goroutines - 1
    stride := totalNumbers / goroutines

    var wg sync.WaitGroup
    wg.Add(goroutines)

    for g := 0; g < goroutines; g++ {
        go func(g int) {
            start := g * stride
            end := start + stride
            if g == lastGoroutine {
                end = totalNumbers
            }

            var lv int
            for _, n := range numbers[start:end] {
                lv += n
            }

            atomic.AddInt64(&v, int64(lv))
            wg.Done()
        }(g)
    }

    wg.Wait()

    return int(v)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Adding Numbers"*

**Benchmark:**
```go
func BenchmarkSequential(b *testing.B) {
    for i := 0; i < b.N; i++ {
        add(numbers)
    }
}

func BenchmarkConcurrent(b *testing.B) {
    for i := 0; i < b.N; i++ {
        addConcurrent(runtime.NumCPU(), numbers)
    }
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Adding Numbers"*

| Cores | Sequential vs Concurrent |
|---|---|
| 1 core  | Sequential ~10–13% faster (concurrency overhead) |
| 8 cores | Concurrent ~41–43% faster (parallelism wins) |

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Adding Numbers"*

---

### Blog Post — When Concurrency Doesn't Help (Bubble Sort)
`#concurrency`

**Principle:** If you can't efficiently combine the partial results, concurrency won't help.

**Code (Bubble sort — concurrent version is useless):**
```go
func bubbleSort(numbers []int) {
    n := len(numbers)
    for i := 0; i < n; i++ {
        if !sweep(numbers, i) {
            return
        }
    }
}

func sweep(numbers []int, currentPass int) bool {
    var idx int
    idxNext := idx + 1
    n := len(numbers)
    var swap bool

    for idxNext < (n - currentPass) {
        a := numbers[idx]
        b := numbers[idxNext]
        if a > b {
            numbers[idx] = b
            numbers[idxNext] = a
            swap = true
        }
        idx++
        idxNext = idx + 1
    }
    return swap
}

func bubbleSortConcurrent(goroutines int, numbers []int) {
    totalNumbers := len(numbers)
    lastGoroutine := goroutines - 1
    stride := totalNumbers / goroutines

    var wg sync.WaitGroup
    wg.Add(goroutines)

    for g := 0; g < goroutines; g++ {
        go func(g int) {
            start := g * stride
            end := start + stride
            if g == lastGoroutine {
                end = totalNumbers
            }
            bubbleSort(numbers[start:end])
            wg.Done()
        }(g)
    }

    wg.Wait()

    // Ugh, we have to sort the entire list again.
    bubbleSort(numbers)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Sorting"*

**Don't:** Add concurrency without a way to merge results efficiently.

---

### Blog Post — I/O-Bound Workload Decisions
`#concurrency` `#performance`

**Principle:** I/O-bound work benefits from concurrency even without parallelism — goroutines naturally wait, so a single thread can serve many of them.

**Code (sequential find):**
```go
func find(topic string, docs []string) int {
    var found int
    for _, doc := range docs {
        items, err := read(doc)
        if err != nil {
            continue
        }
        for _, item := range items {
            if strings.Contains(item.Description, topic) {
                found++
            }
        }
    }
    return found
}

func read(doc string) ([]item, error) {
    time.Sleep(time.Millisecond) // Simulate blocking disk read.
    var d document
    if err := xml.Unmarshal([]byte(file), &d); err != nil {
        return nil, err
    }
    return d.Channel.Items, nil
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Reading Files"*

**Code (concurrent find with pooling):**
```go
func findConcurrent(goroutines int, topic string, docs []string) int {
    var found int64

    ch := make(chan string, len(docs))
    for _, doc := range docs {
        ch <- doc
    }
    close(ch)

    var wg sync.WaitGroup
    wg.Add(goroutines)

    for g := 0; g < goroutines; g++ {
        go func() {
            var lFound int64
            for doc := range ch {
                items, err := read(doc)
                if err != nil {
                    continue
                }
                for _, item := range items {
                    if strings.Contains(item.Description, topic) {
                        lFound++
                    }
                }
            }
            atomic.AddInt64(&found, lFound)
            wg.Done()
        }()
    }

    wg.Wait()

    return int(found)
}
```
*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Reading Files"*

| Cores | Sequential vs Concurrent |
|---|---|
| 1 core  | Concurrent ~87–88% faster |
| 8 cores | Concurrent ~87–88% faster (parallelism gives no extra benefit) |

*Ref: The_Ultimate_Go_Notebook.md — "Scheduling In Go: Concurrency / Reading Files"*

---

### Blog Post — GC: Mark Setup, Marking, Mark Termination
`#performance`

**Principle:** Every GC has three phases. Two are STW (Mark Setup, Mark Termination); one is concurrent (Marking). The collector targets STW under 100 microseconds.

1. **Mark Setup (STW)**: Turn on write barrier. Wait for every goroutine to reach a safe point.
2. **Marking (Concurrent)**: Collector takes 25% of CPU (one P per 4). Traverses heap from stack roots. Heavy allocators get recruited into **Mark Assist**.
3. **Mark Termination (STW)**: Turn off write barrier, clean up, calculate next goal.

*Ref: The_Ultimate_Go_Notebook.md — "Garbage Collection Semantics / Collector Behavior"*

---

### Blog Post — GC: Sweeping Is Concurrent, Tied to Allocation
`#performance`

**Principle:** Sweeping reclaims memory for unmarked values. It happens lazily when goroutines allocate via `runtime.mallocgc` → `runtime.(*mcache).nextFree`. Sweep latency is part of allocation cost, not GC latency.

*Ref: The_Ultimate_Go_Notebook.md — "Garbage Collection Semantics / Sweeping - Concurrent"*

---

### Blog Post — GC: Pacing and the GC Percentage Knob
`#performance`

**Principle:** `GOGC=100` (default) doubles the heap before next GC. Larger `GOGC` slows pacing (more memory, fewer GCs). Smaller `GOGC` speeds pacing (less memory, more GCs).

```
$ export GODEBUG=gctrace=1,gcpacertrace=1 ./app
gc 5 @0.071s 0%: 0.018+0.46+0.071 ms clock, 0.14+0/0.38/0.14+0.56 ms cpu,
29->29->29 MB, 30 MB goal, 8 P
pacer: sweep done at heap size 29MB; allocated 0MB of spans; swept 3752 pages
pacer: assist ratio=+1.232155e+000 (scan 1 MB in 70->71 MB) workers=2+0
```
*Ref: The_Ultimate_Go_Notebook.md — "Garbage Collection Semantics / GC Trace"*

**Don't:** Adjust GOGC to delay latency — that's not sympathy. Reduce allocations instead.

---

### Blog Post — GC: Being Sympathetic Means Reducing Allocations
`#performance`

**Principle:** Reducing stress on the heap reduces GC latency. The collection pace doesn't change much; what changes is the **work done between** collections.

After removing 4.48 GB of non-productive allocations:
- Average pace: 2.08ms → 1.96ms (essentially unchanged).
- Requests per collection: 3.98 → 7.13 (79.1% more work per GC).

*Ref: The_Ultimate_Go_Notebook.md — "Garbage Collection Semantics / Being Sympathetic"*

**Do:**
- Identify and remove non-productive allocations.
- Aim for smallest heap + consistent pace + stay within goal + minimize STW and mark-assist durations.

**Don't:**
- Try to write zero-allocation code — recognize productive vs non-productive allocations.
- Confuse "slowing the GC" with performance.

---

## Anti-Patterns & Common Mistakes

- **Embedding as inheritance** (Animal/Dog/Cat): Groups by common DNA, fights the type system. → *fix:* Declare interfaces for common behavior; embed for behavior promotion, not state reuse.
- **Mixing value and pointer receivers on the same type:** Breaks method-set guarantees; causes interface satisfaction surprises. → *fix:* Pick one semantic per type and stay consistent.
- **Returning concrete error types instead of `error`:** Causes nil-interface bugs (`*customError(nil)` inside non-nil `error`). → *fix:* Always declare `error` as the return type.
- **Parsing the `Error()` string:** Couples callers to message format. → *fix:* Use sentinel vars, typed errors, or behavior-based type assertions.
- **Splitting `Lock`/`Unlock` across functions or repeating `Lock` in one function:** Loses synchronization, hides races from the detector. → *fix:* Lock and Unlock in the same function; one critical section per shared operation.
- **Mismatching `Lock` with `RUnlock`** (or vice versa): Undefined behavior. → *fix:* Pair them precisely.
- **Forgetting `cancel()` from `context.WithTimeout`/`WithCancel`:** Memory leak. → *fix:* `defer cancel()` immediately.
- **Using unbuffered channel for cancellation-result pattern:** Child goroutine blocks forever when parent walks away. → *fix:* Buffer of 1.
- **Designing with interfaces from day one:** Causes interface pollution. → *fix:* Discover interfaces during refactoring.
- **Factory returning unexported type:** Callers can't name the type. → *fix:* Return exported types or interface values mindfully.
- **Mixing exported fields with unexported embedded types:** Partial construction bugs. → *fix:* Be consistent with export discipline.
- **Cached pointer into a slice element later appended:** Stale pointer after backing-array replacement. → *fix:* Wrap the slice in a struct or re-fetch the element after appends.
- **Caching `b.N`-dependent values outside the benchmark loop:** Skews measurements. → *fix:* Reset state each iteration (`output.Reset()`).
- **Capturing loop variables in sub-tests without copying:** All sub-tests share the last value. → *fix:* `test := test` before the literal function.
- **Forgetting `Add(2)` or `Done()`:** Permanent deadlock or premature exit. → *fix:* Keep Add/Done in the same line of sight.
- **Building concurrency on observed ordering:** The scheduler is preemptive and nondeterministic. → *fix:* Use synchronization/orchestration primitives.
- **Trusting `b.N`-sharing benchmarks:** Goroutine cleanup from previous benchmarks skews later ones. → *fix:* Run suspected-fast benchmarks in isolation; use `benchstat`.
- **Adjusting GOGC to mask allocations:** Doesn't fix the root cause. → *fix:* Remove non-productive allocations.

---

## Decision Heuristics / Checklists

### When to use channels vs mutexes
1. **Is this about signaling between goroutines?** → Channels.
2. **Is this about protecting shared state during read/modify/write?** → Mutex (or atomics for a single word).
3. **Do you need a guarantee at the signaling level (recv before send)?** → Unbuffered channel.
4. **Can you accept unknown latency, or do you need bounded latency?** → Unbuffered = unknown; buffered = bounded.
5. **Are you sharing a single counter?** → `atomic.AddInt32/64`.
6. **Many readers, few writers?** → `sync.RWMutex`.
7. **Multiple goroutines coordinating shutdown?** → `context.Context` + channels.

### Table-driven test checklist
- [ ] Each row has a unique `name` for sub-test filtering.
- [ ] Loop variable is copied (`test := test`) before the closure.
- [ ] `t.Parallel()` is the first line if independent.
- [ ] `defer resp.Body.Close()` (or equivalent cleanup) is present.
- [ ] `t.Log("exp:", ...); t.Log("got:", ...)` before `t.Fatal`.
- [ ] Negative paths are included.

### Benchmark discipline checklist
- [ ] Machine is idle; no browsers, no shared cloud, no VM noise.
- [ ] Power/thermal scaling disabled (when possible).
- [ ] Loop variable `for i := 0; i < b.N; i++`.
- [ ] Return values captured into a package-level var (prevent compiler elision).
- [ ] State reset each iteration.
- [ ] Run in isolation; compare with `benchstat`.
- [ ] Run multiple times; check for consistency.

### Profiling workflow
1. Write the benchmark first.
2. Run with `-benchmem` to see allocations.
3. Add `-memprofile p.out` and inspect with `go tool pprof` and `list <func>`.
4. Add `-gcflags=-m=2` to read the escape analysis report.
5. Fix the highest-impact allocation; repeat.
6. Then add `-cpuprofile p.out` for CPU work.
7. Only after CPU and memory are tuned, consider blocking profiles.

### Interface decision checklist
- [ ] Is the consumer (not the producer) declaring the interface?
- [ ] Does the interface describe a behavior (verb), not a noun?
- [ ] Is it composed of single-method interfaces where possible?
- [ ] Would removing the interface change nothing for the user? If yes, remove it.
- [ ] Does it decouple from a concrete change that has been identified (not guessed)?

### Concurrency decision checklist
- [ ] Do you have a sequential solution that works first?
- [ ] Is the workload CPU-bound or I/O-bound?
- [ ] CPU-bound: do you have parallelism (multiple cores)?
- [ ] I/O-bound: concurrency helps even with one thread.
- [ ] Can the partial results be efficiently combined?
- [ ] Do you know how every goroutine terminates?
- [ ] Have you run `go test -race` and `go build -race`?
- [ ] Have you sized pools/buffers deliberately (start with GOMAXPROCS)?
- [ ] Have you set timeouts via context for every I/O path?

### Error handling checklist
- [ ] Every error is checked at the point of return.
- [ ] Function signatures return `error`, never concrete error types.
- [ ] Errors are wrapped with context (`%w` or `errors.Wrap`).
- [ ] The handler logs the full wrapped error and decides recover/continue/shutdown.
- [ ] Type checks use behavior interfaces where possible (`temporary`, `timeout`).

---

## Key Takeaways

1. **Correctness → readability → simplicity → performance, in that order.** Never invert this hierarchy. Optimize only what you can measure.
2. **Value vs pointer semantics is a design decision, not a performance choice.** Be consistent within a type. Once you switch to pointer semantics, never go back. The data dictates the semantic.
3. **Pointers exist for sharing.** If "share" isn't in your mouth, you don't need a pointer. Read `&` as "sharing" to preserve readability.
4. **Escape analysis is about ownership.** A value escapes when it must outlive its constructing function. Use `-gcflags=-m=2` to ask the compiler why.
5. **Interfaces are discovered, not designed.** Start concrete; refactor for readability, efficiency, abstraction, testability. Group by behavior, not common DNA. Keep them small (single method when possible). The consumer declares the interface.
6. **Composition over inheritance.** Embed for behavior promotion, not state reuse. Compose larger interfaces from smaller ones. Ask functions to accept only what they need.
7. **Error handling is integrity.** 92% of critical failures are error-handling bugs. Always return `error`. Wrap errors with context. Use sentinel vars for identity, concrete types for state, behavior interfaces for decoupled checks.
8. **Know your goroutines' lifecycle.** Every goroutine must have a defined termination. Use `sync.WaitGroup` for orchestration; keep Add/Done in the same line of sight. All goroutines should terminate before main returns.
9. **Channels are signaling mechanisms, not queues.** Decide: guarantee at signaling level (unbuffered) vs outside (buffered). Data with signal = 1-to-1; close without data = 1-to-many. Buffer of 1 for cancellation result patterns.
10. **Benchmarks lie. Validate everything.** Idle machine, run in isolation, capture return values, reset state, compare with `benchstat`. The race detector (`-race`) is your friend.
11. **Profile before optimizing.** Memory profile → escape analysis → CPU profile. Inline factory functions. Avoid interface conversions in hot paths. Constant-size `make` stays on the stack.
12. **Be sympathetic with the GC.** Reducing allocations is the lever — not slowing the pace. `GOGC`/`SetGCPercent` trades memory for fewer GCs; use sparingly and measure.
13. **Mechanical sympathy matters.** Cache lines are 64 bytes. Row traversal beats column traversal by 10x+. Linked lists lose to slices for hot paths. Lay out struct fields largest-first to eliminate padding. The Go scheduler turns I/O-bound work into CPU-bound work at the OS level — you usually don't need more OS threads than virtual cores.
14. **Less is more.** 15–50 bugs per 1,000 LOC. The best code is the code you didn't write. Concurrency adds complexity — only use it when out-of-order execution adds clear value.
15. **Generics enable type-safe reusable containers and concurrency patterns.** Use behavioral constraints (interfaces) over type lists where possible. Write concrete implementations first, then generalize.

---

## Cross-References

- Topic index: [[../INDEX.md]]
- Related best-practice notes in this repo cover Rust, Java, Python, and language-agnostic concurrency/performance topics.
- Source book: `markdown_output/The_ultimate_Go_Notebook_-_WIlliam_Kennedy/The_ultimate_Go_Notebook_-_WIlliam_Kennedy.md`
- Summary: `summaries/The_ultimate_Go_Notebook_-_WIlliam_Kennedy.md`
- Official course materials: https://github.com/ardanlabs/gotraining
