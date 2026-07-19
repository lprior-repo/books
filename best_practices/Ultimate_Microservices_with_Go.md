# Ultimate Microservices with Go
**Author:** Nir Shtein
**Topic tags:** `#architecture` `#go` `#api` `#systems` `#concurrency` `#testing`
**Language focus:** Go-first (microservices in Go on Kubernetes)
**Sources:** `markdown_output/Ultimate_Microservices_with_Go_-_Nir_Shtein/Ultimate_Microservices_with_Go_-_Nir_Shtein.md` · `summaries/Ultimate_Microservices_with_Go_-_Nir_Shtein.md`

## TL;DR
A 10-chapter tour that pairs Go's design philosophy (simplicity, efficiency, maintainability, concurrency) with the core elements of microservices architecture (REST APIs, message brokers, gRPC, service discovery, API gateway, event-driven systems), shows how to build RESTful APIs in Gin, deploy them onto Kubernetes, harden them with timeouts/retries/circuit breakers, and operate them in production with logs, metrics, tracing, profiling, and alerting. Apply this book when you are designing or running Go services that need to scale horizontally on Kubernetes with REST as the primary IPC.

---

## Best Practices by Topic

### Microservices Fundamentals — When to Choose Microservices

**Principle:** Microservices trade operational complexity for independent workloads, plug-and-play replaceability, fault tolerance, and agility.

**Do:**
- Adopt microservices when Agile delivery cadence, cloud computing, Docker, and DevOps practices are already in place — they dissolve microservices' main drawback (operations overhead).
- Split workloads so each service owns its own codebase, tests, and deployment pipeline.
- Scale horizontally by increasing replicated containers per service.
- Design services as honeycomb cells — easily replaceable, rollback-able, and rollable-forward independently.

**Don't:**
- Don't choose microservices for short-term ROI if you lack cloud/DevOps maturity — the operations tax will dominate.
- Don't let one service's failure cascade into others; loose coupling is mandatory, not optional.
- Don't assume microservices simplify troubleshooting — distributed systems are *harder* to observe than monoliths.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 1 / Benefits of Microservices" & "Drawbacks of Microservices"*

---

### Architecture Alternatives — Monolith vs. SOA vs. Serverless

**Principle:** Know the alternatives before committing — each sits on a decomposition spectrum.

**Do:**
- Use **monolith** for simple, fast-to-deliver systems with minimal network hops and easy DRY adherence.
- Use **SOA** for reusable, loosely-coupled provider/consumer services that *may* share deployable components.
- Use **serverless** (FaaS/BaaS) when you want zero infrastructure management and accept vendor lock-in.
- Use **microservices** for fine-grained, independently deployable, self-contained units.

**Don't:**
- Don't confuse SOA with microservices — SOA providers/consumers can share deployables; microservices cannot.
- Don't underestimate serverless vendor lock-in, edge-case limits, and tooling constraints.
- Don't reject monolith outright — it remains a valid choice for greenfield projects with small teams.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 1 / Monolithic, SOA, and Serverless"*

---

### Why Go and Microservices Correlate

**Principle:** Go's simplicity, fast compilation, lightweight concurrency (goroutines), strong standard library, and 1.x backward-compatibility guarantee align with microservices' demand for many small, independent, maintainable services.

**Do:**
- Lean on Go's ~25 keywords and single-source-of-truth conventions (the Go team owns the rules).
- Exploit goroutines (2 KB stacks vs. 8 KB OS threads) for cheap, abundant concurrency.
- Trust the Go 1.x compatibility promise to keep services stable across version upgrades.
- Use the holistic toolchain (`go mod`, `gofmt`, `go test`, `go vet`, `govulncheck`, `pprof`, `gopls`).

**Don't:**
- Don't expect try-catch style error handling — Go deliberately returns errors as values to enable "telling a story."
- Don't reach for inheritance — Go uses composition via embedding.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Invention of Go" & "Popularity of Golang"*

---

### Go Core Principles & Paradigms

**Principle:** Go is built on three unofficial core principles — simplicity, efficiency, maintainability — and supports imperative, concurrent, and (modified) object-oriented paradigms.

**Do:**
- Treat Go as **statically + strongly typed** — variables can't change type at runtime; mixing types in operations fails to compile.
- Use composition + interfaces as the substitute for classical inheritance/polymorphism.
- Accept that Go is intentionally "boring" — most releases focus on compiler/perf improvements, not feature sprawl.

**Code:**
```go
// Go is statically typed — type inference works only with :=
x := 5
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Statically typed"*

```go
// Strong typing: this WILL NOT compile — cannot concatenate string and int
myString := "name" + 2
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Strong typing"*

---

### Go Fast Compilation — Why It Matters for CI

**Principle:** Go compiles fast because packages form a DAG (no cyclic dependencies), unused imports/variables are forbidden, and the language is intentionally small.

**Do:**
- Trust that large Go binaries build in seconds, enabling high release rates.
- Run `go mod tidy` to keep the dependency graph clean.
- Avoid unused imports — they break the build by design.

**Don't:**
- Don't introduce cyclic package dependencies — the compiler will reject them.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Fast Compiling"*

---

### Go Scheduler and GOMAXPROCS

**Principle:** Goroutines are managed by the Go runtime scheduler (not the OS), which allocates them onto threads with per-thread queues and work-stealing for load balancing.

**Do:**
- Keep `GOMAXPROCS` at its default (number of cores) unless benchmarks prove otherwise.
- Understand that practical goroutine limits are 1,000–10,000 per machine, bounded by memory (2 KB each) and GC pressure.
- Let the scheduler steal work between threads automatically.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Concurrency Approach"*

---

### Error Handling — Telling a Story

**Principle:** Go returns errors as values so you can wrap them with context — creating a "story" of where the error originated and propagated through.

**Do:**
- Wrap errors with `%w` to preserve the chain while adding context.
- Pick the right error constructor by matching + message type (see conventions table).
- Pass enriched errors across service boundaries so distributed tracing can correlate them.

**Don't:**
- Don't swallow errors silently or return bare `err` without context in cross-service paths.
- Don't reach for `panic` for ordinary failures — reserve it for unrecoverable server-level conditions.

**Code:**
```go
if err != nil {
    return err
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Error Handling"*

```go
If err != nil {
 return fmt.Errorf("connecting to DB: %w", err)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 2 / Error Handling"*

| Error matching? | Message  | Guidance                          |
|-----------------|----------|-----------------------------------|
| No              | Static   | `errors.New`                      |
| No              | Dynamic  | `fmt.Errorf`                      |
| Yes             | Static   | Top-level `var` with `errors.New` |
| Yes             | Dynamic  | Custom error type                 |

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Conventions (Uber-Go table)"*

---

### Three Ways to Create an Error in Go

**Principle:** Choose between `fmt.Errorf`, `errors.New`, and a custom error type based on whether you need dynamic formatting and/or sentinel matching.

**Code:**
```go
err := fmt.Errorf("a height of %0.2f is invalid", -2.3333)
fmt.Println(err.Error()) // a height of -2.33 is invalid
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Errors — Talking About Error Propagation"*

```go
err = errors.New("this is an invalid height")
fmt.Println(err.Error()) // this is an invalid height
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Errors — Talking About Error Propagation"*

```go
type ApiError struct {
 Path string
 StatusCode int
}
func (e *ApiError) Error() string {
 return fmt.Sprintf("API error: %s returned a %d", e.Path,
 e.StatusCode)
}
func main() {
 err = &ApiError{Path: "/api/users", StatusCode: 500}
 fmt.Println(err.Error()) // API error: /api/users returned a
 // 500
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Errors — Talking About Error Propagation"*

---

### Hello World — Go Entry Points

**Principle:** Every Go program needs `package main` and a `func main()` entry point; `func init()` runs before `main()`.

**Code:**
```go
package main
import "fmt"
func main() {
  fmt.Println("Hello World!")
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Hello World"*

```go
import (
 "fmt"
 "os"
)
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Hello World"*

```go
fmt.Println("Hello World!")
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Hello World"*

---

### Variable Declaration — Three Forms

**Principle:** Go offers explicit-typed, inferred, and short-declaration (`:=`) variable forms.

**Code:**
```go
var emptyMessage string
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Variables"*

```go
var message string = "This is a message"
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Variables"*

```go
var inferredMessage = "This is an inferred message"
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Variables"*

```go
alsoInferredMessage := "This is also an inferred message"
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Variables"*

---

### Primitive Data Types & Defaults

**Principle:** Go has four primitive categories — `string`, `int` (and variants), `float32/64`, `bool` — each with a deterministic zero value.

**Code:**
```go
package main
import "fmt"
func main() {
 message := "This is a message"
 fmt.Println(message)
 var zero int
 fmt.Println(zero)
 number := 42
 fmt.Println(number)
 var pi float64 = 3.14
 fmt.Println(pi)
 var booleanVar bool
 fmt.Println(booleanVar)
```

```go
trueBooleanVar := true
 fmt.Println(trueBooleanVar)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Primitive Data Types"*

- `string` default `""`, `int` default `0`, `float32/64` default `0`, `bool` default `false`.

---

### Comments

**Code:**
```go
func main() {
 // This is simple comment
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Comments"*

```go
/*
 This is a multi-line comment
*/
fmt.Println("Hello World!")
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Comments"*

---

### Operators

**Code:**
```go
package main
func main() {
 // Arithmetic Operators
 x := 5 + 5 // 10
 x = 5 - 5 // 0
 x = 5 * 5 // 25
 x = 5 / 5 // 1
 x = 5 % 5 // 0
 x++ // 6
 x-- // 5
 // Comparison Operators
 y := 5 == 5 // true
 y = 5 != 5 // false
 y = 5 > 5 // false
 y = 5 < 5 // false
 y = 5 >= 5 // true
 y = 5 <= 5 // true
 // Logical Operators
 a := true && true // true
 a = true && false // false
 a = true || true // true
 a = true || false // true
 a = !true // false
 a = !false // true
 // Bitwise Operators
 b := 5 & 5 // 5
 b = 5 | 5 // 5
 b = 5 ^ 5 // 0
 b = 5 << 5 // 160
 b = 5 >> 5 // 0
 // Assignment Operators
 c := 5
 c += 5 // 10
```

```go
c -= 5 // 5
 c *= 5 // 25
 c /= 5 // 5
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Operators"*

---

### Loops — Only `for`

**Principle:** Go has a single loop keyword (`for`); there is no `while`. Use `break`, `continue`, and `range` for variations.

**Code:**
```go
func main() {
 // for loop with initialization, condition, and post
 for i := 0; i < 5; i++ {
  println(i)
 }
 // for loop with single condition, act as a "while"
 i := 0
 for i < 5 {
  println(i)
  i++
 }
 // for loop with no condition, act as a "while"
 i = 0
 for {
  println(i)
  i++
  if i >= 5 {
    break
  }
 }
 // for loop with continue
```

```go
for i := 0; i < 5; i++ {
  if i%2 == 0 {
    continue
  }
  println(i)
 }
 // for loop with range
 s := []int{1, 2, 3}
 for k, v := range s {
  println(k, v)
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Loops"*

---

### Arrays — Fixed Length

**Code:**
```go
func main() {
 // declare an array of 5 integers
 var a = [5]int{1, 2, 3, 4, 5}
 // declare an array with inferred length
 var b = […]int{1, 2, 3}
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Arrays"*

---

### Slices — Flexible Length

**Principle:** Slices are Go's flexible arrays — declare with literal syntax or `make([]type, length, capacity)`.

**Code:**
```go
mySlice := []string{"nir", "david"}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Slices"*

```go
mySlice := make([]type, length, capacity)
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Slices"*

```go
slice := make([]int, 2, 5)
fmt.Println(slice) // [0 0]
fmt.Println(len(slice)) // 2
fmt.Println(cap(slice)) // 5
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Slices"*

```go
myArray := [5]int{1, 2, 3, 4, 5}
slice = myArray[1:4] // from the 1st index to the 4th index
(not included)
fmt.Println(mySlice) // [2 3 4]
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Slices"*

---

### Functions — Multiple Returns, Named Returns, defer

**Principle:** Go functions support multiple return values, named return values, first-class citizenship, and the `defer` keyword for scheduled execution.

**Code:**
```go
func myFunction(amount int, prefix string) string {
 return fmt.Sprintf("%s: %d", prefix, amount)
} // Input: 5, "nir" | Output: "nir: 5"
func multipleReturns(prefix string, amount int) (string, int) {
 amount++
 return fmt.Sprintf("%s: %d", prefix, amount), amount
} // Input: "nir", 5 | Output: "nir: 6", 6
func namedReturnValues(prefix string, amount int) (result
string, newAmount int) {
```

```go
amount++
 result = fmt.Sprintf("%s: %d", prefix, amount)
 newAmount = amount
 return
} // Input: "nir", 5 | Output: "nir: 6", 6
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Functions"*

```go
func functionWithDefer() {
 defer fmt.Println("This will be printed last")
 fmt.Println("This will be printed first")
} // Output: This will be printed first
// This will be printed last
func functionWithMultipleDefers() {
 defer func() {
  fmt.Println("This will be printed last")
 }()
 defer fmt.Println("This will be printed second")
 fmt.Println("This will be printed first")
}
// Output: This will be printed first
// This will be printed second
// This will be printed last
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Functions"*

---

### Maps — Key-Value Storage

**Principle:** Maps hold key-value pairs; default is `nil`. Use the `value, ok` idiom to check existence.

**Code:**
```go
fruitsPrices := map[string]int{
 "orange": 10,
 "apple": 20,
 "banana": 15,
}
fmt.Println(fruitsPrices) // Output: map[apple:20 banana:15
orange:10]
// Add a new key-value pair
fruitsPrices["mango"] = 25
fmt.Println(fruitsPrices) // Output: map[apple:20 banana:15
mango:25 orange:10]
// Delete a key-value pair
delete(fruitsPrices, "orange")
fmt.Println(fruitsPrices) // Output: map[apple:20 banana:15
mango:25]
// Get a value from a map
fmt.Println(fruitsPrices["apple"]) // Output: 20
// Get a value from a map that doesn't exist
fmt.Println(fruitsPrices["grapes"]) // Output: 0 (the default
value for int)
// Check if a key exists in a map
price, ok := fruitsPrices["grapes"]
fmt.Println(price, ok) // Output: 0 false
// Iterate over a map
for fruit, price := range fruitsPrices {
 fmt.Printf("%s: %d\n", fruit, price)
} // Output: apple: 20 banana: 15 mango: 25 (order may vary)
fmt.Println(len(fruitsPrices)) // Output: 3
// Create an empty map
emptyMap := make(map[string]int)
fmt.Println(emptyMap) // Output: map[]
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Maps"*

---

### Switch — Breaks by Default

**Principle:** Go `switch` breaks by default; use `fallthrough` to continue to the next case.

**Code:**
```go
func main() {
 printString("b") // b
 printString("a") // a b
}
func printString(str string) {
 switch str {
 case "a":
  println("a")
  fallthrough
 case "b":
  println("b")
 default:
  println("default")
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Switch"*

---

### Constants & iota

**Code:**
```go
const str string = "const string"
const (
 _ = iota
 one
 two
 three
)
```

```go
func main() {
 println(str) // string
 str = "new string" // cannot assign to str, will fail in
 // compilation
 println(one) // 1
 println(two) // 2
 println(three) // 3
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Consts"*

---

### Packages & Access Modifiers

**Principle:** Capitalization controls visibility — uppercase = public, lowercase = private. Rename packages with an alias in imports.

**Code:**
```go
import (
 f "fmt"
 "math"
)
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

```go
const myName = "jack" // not public
const MyName = "jack" // public
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

```go
go mod init githubple.com/nir/mymodule
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

```go
module github.com/OrangeAVA/Microservices-with-Go
go 1.21.0
require (
 github.com/gin-gonic/gin v1.9.0
)
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

```go
go mod download
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

```go
go mod tidy
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Packages"*

---

### Go Project Structure — `cmd`, `pkg`, `internal`

**Principle:** Standard Go project layout uses `cmd/` for entry points, `pkg/` for code safe to share across services, and `internal/` for private packages.

**Do:**
- Put binary entry points under `cmd/`, with directory names matching binary names.
- Use a single top-level `pkg/` for monorepo shared code.
- Reserve `internal/` for service-private packages — the compiler enforces the boundary.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Project Structure"*

---

### Structs & Methods — Value vs. Pointer Receivers

**Principle:** Structs are typed field collections. Value receivers are read-only; pointer receivers can mutate.

**Code:**
```go
type user struct {
 name string
 email string
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
type admin struct {
 user
 level string
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
u1 := user{
 name: "john",
 email: "john@gmail.com",
}
fmt.Printf("%+v\n", u1) // {name:john email:john@gmail.com}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
func newUser(name string) user {
 return user{
```

```go
name: name,
  email: fmt.Sprintf("%s@gmail.com", name),
 }
}
u2 := newUser("jack")
fmt.Printf("%+v\n", u2) // {name:jack email:jack@gmail.com}
a := admin{
  user: user{
   name: "john",
   email: "john@gmail.com",
  },
  level: "super",
}
fmt.Printf("%+v\n", a) // {user:{name:john
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
u3 := newUser("amanda")
fmt.Printf("%+v\n", u3) // {name:amanda email:amanda@gmail.com}
fmt.Println(u3.name) // amanda - we access the field name of
// the struct user
u3.name = "ruth" // we change the value of the field name of
// the struct user
fmt.Printf("%+v\n", u3) // {name:ruth email:amanda@gmail.com}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
func (u user) Print() {
 fmt.Printf("Name: %s, Email: %s\n", u.name, u.email)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

```go
func (u *user) ChangeEmail(email string) {
 u.email = email
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Structs"*

---

### Composition Over Inheritance

**Principle:** Go uses embedding, not inheritance — embedded structs expose their methods to the outer struct.

**Code:**
```go
type Animal struct {
 Sound string
}
func (a *Animal) Speak() {
 println(a.Sound)
}
type Cat struct {
 Animal // Embedding
}
type Dog struct {
 Animal // Embedding
}
func main() {
 cat := Cat{Animal{"Meow"}}
 cat.Speak() // Meow
 dog := Dog{Animal{"Woof"}}
 dog.Speak() // Woof
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Composition"*

---

### Interfaces — Implicit Implementation

**Principle:** Go interfaces contain only method signatures. Types satisfy interfaces implicitly — no explicit declaration needed.

**Code:**
```go
type Person struct {
 Name string
}
func (m Person) Print() {
 fmt.Println(m.Name)
}
type DogPerson struct {
 Name string
}
type PrintInterface interface {
 Print()
}
var PrintableObject PrintInterface = Person{}
var PrintableObject2 PrintInterface = DogPerson{} // This will
// throw an error in compile time
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Interfaces"*

```go
var i interface{}
// Or
var myName interface{}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 3 / Interfaces"*

---

### Functional Options Pattern

**Principle:** Use the Functional Options pattern to build structs cleanly since Go lacks function overloading and optional parameters.

**Do:**
- Define an option type as `func(*StructName)`.
- Constructor accepts required params + `options ...StructNameOption`.
- Prefix each option helper with `With`.

**Code:**
```go
type ShoppingClient struct {
 endpoint string
 apiKey string
```

```go
userId string
  shouldRetry bool
  timeout time.Duration
}
The second step is to create the option type:
type ShoppingClientOption func(*ShoppingClient)
Now, we can make our constructor that should look like this:
func NewShoppingClient(endpoint string, options …
ShoppingClientOption) *ShoppingClient {
  client := &ShoppingClient{
   endpoint: endpoint,
  }
  for _, option := range options {
   option(client)
  }
  return client
}
Note that if we don't give any option, the fields will get their default value,
except endpoint, which is required field. All that is left is to create the
option functions.
func WithApiKey(key string) ShoppingClientOption {
  return func(c *ShoppingClient) {
   c.apiKey = key
  }
}
func WithUserId(id string) ShoppingClientOption {
  return func(c *ShoppingClient) {
   c.userId = id
  }
}
func WithTimeout(timeout time.Duration) ShoppingClientOption {
  return func(c *ShoppingClient) {
   c.timeout = timeout
  }
```

```go
}
func WithRetry(shouldRetry bool) ShoppingClientOption {
 return func(c *ShoppingClient) {
   c.shouldRetry = shouldRetry
 }
}
Let's demonstrate two usages of the pattern:
client := NewShoppingClient("https://api.shopping.com/v1",
 WithApiKey("my-api-key"),
 WithTimeout(10*time.Second),
)
fmt.Printf("%+v\n", client) // &
{endpoint:https://api.shopping.com/v1 apiKey:my-api-key userId:
shouldRetry:false timeout:10000000000}
clientV2 := NewShoppingClient("https://api.shopping.com/v2",
 WithRetry(true),
 WithUserId("my-user-id"),
)
fmt.Printf("%+v\n", clientV2) // &
{endpoint:https://api.shopping.com/v2 apiKey: userId:my-user-id
shouldRetry:true timeout:0}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Functional Options Pattern"*

---

### Generics — Constraints and Type Parameters

**Principle:** Generics (Go 1.18+) let you write reusable code with type parameters in square brackets. Built-in constraints: `any`, `comparable`. Custom constraints via interfaces with type unions.

**Code:**
```go
func printIt[T any](item T) {
 fmt.Println(item)
}
printIt(1) // 1
printIt("Hello") // Hello
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Generics"*

```go
type Number interface {
 int | float64
}
func bigger[T Number, K any](a T, b T, prefix K) {
 if a > b {
  fmt.Println(prefix, a)
  return
 }
 fmt.Println(prefix, b)
}
```

```go
bigger(1, 2, "The bigger integer is:") // The bigger
integer is: 2
bigger(3.0, 2.0, "The bigger float is:") // The bigger
float is: 3
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Generics"*

```go
type StorageInter[T any] interface {
 GetItem() T
 StoreItem(T)
}
type Storage[T any] struct {
 Item T
}
func (s *Storage[T]) GetItem() T {
 return s.Item
}
func (s *Storage[T]) StoreItem(item T) {
 s.Item = item
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Generics"*

```go
var _ StorageInter[int] = &Storage[int]{}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Generics"*

```go
var intStorage StorageInter[int] = &Storage[int]{}
intStorage.StoreItem(789)
fmt.Println(intStorage.GetItem())
var stringStorage StorageInter[string] = &Storage[string]{}
stringStorage.StoreItem("This is a string")
fmt.Println(stringStorage.GetItem())
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Generics"*

---

### Context — The Microservices Communication Backbone

**Principle:** `context.Context` manages key-value stores, concurrency coordination, and task lifecycle (cancellation/deadlines/timeouts). Propagate it explicitly through function arguments.

**Do:**
- Pass context explicitly as the first function argument.
- Prefer `context.WithCancel` over `context.WithTimeout` for manual control.
- Derive child contexts from parents to preserve propagation (auth, tracing, request metadata).
- Use context propagation to pass auth/observability data between services.

**Don't:**
- Don't call `context.Background()` mid-request — it breaks the lifecycle.
- Don't store context in a global variable or struct field.

**Code:**
```go
type Context interface {
 Deadline() (deadline time.Time, ok bool)
 Done() <-chan struct{}
 Err() error
 Value(key any) any
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

```go
ctx := context.Background()
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

```go
func main() {
 ctx := context.Background()
 childContext := context.WithValue(ctx, "apiKey", 123456)
 printAPIKey(childContext)
}
func printAPIKey(ctx context.Context) {
 apiKey := ctx.Value("apiKey")
 fmt.Println("API Key:", apiKey) // API Key: 123456
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

```go
contextWithCancel, cancel := context.WithCancel(ctx)
cancel()
```

```go
fmt.Println("What happened ?", contextWithCancel.Err()) // What
// happened ? context canceled
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

```go
contextWithTimeout, _ := context.WithTimeout(ctx,
 30*time.Second)
fmt.Println("What happened ?", contextWithTimeout.Err()) //
// What happened ? <nil>
time.Sleep(35 * time.Second)
fmt.Println("What happened ?", contextWithTimeout.Err()) //
// What happened ? context deadline exceeded
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

```go
func WithTimeout(parent Context, timeout time.Duration)
(Context, CancelFunc) {
 return WithDeadline(parent, time.Now().Add(timeout))
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Understanding Context in Go"*

---

### Testing — Built-in `testing` Package

**Principle:** Go ships a first-party `testing` package; prefer it over external frameworks. Tests live in `_test.go` files with `Test*` functions.

**Do:**
- Use table-driven tests with subtests via `t.Run`.
- Keep tests independent, reproducible, and non-flaky.

**Don't:**
- Don't reach for third-party frameworks unless absolutely necessary — the standard library is sufficient.

**Code:**
```go
3. Use the Go CLI to run the test by running - go test ./
We have a function called get bigger ("example.go")
func GetBigger(a, b float64) float64 {
  return math.Max(a, b)
}
And this is how the testing file should look like (example_test.go):
package main
import "testing"
func TestGetBigger(t *testing.T) {
  type args struct {
   a float64
   b float64
  }
  tests := []struct {
   name string
   args args
   want float64
  }{
   {
    name: "a is the bigger one",
    args: args{
      a: 9,
      b: 6,
    },
    want: 9,
   },
   {
    name: "b is the bigger one",
    args: args{
      a: 3,
      b: 7,
    },
    want: 7,
   },
  }
```

```go
for _, tt := range tests {
  t.Run(tt.name, func(t *testing.T) {
   if got := GetBigger(tt.args.a, tt.args.b); got != tt.want {
     t.Errorf("GetBigger() = %v, want %v", got, tt.want)
   }
  })
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Testing - Best Practices, Mocking, and Fuzzy Tests"*

---

### Mocking — Interfaces + mockery/gomock

**Principle:** You cannot mock functions directly in Go — wrap them in structs that implement interfaces, then mock the interface with `mockery` or `gomock`.

**Code:**
```go
// Valid name is between 8 and 16 chars and doesn't contain
// number
func IsValidName(name string) bool {
 numbersValid := IsNumbersValid(name)
 lengthValid := IsLengthValid(name)
 return numbersValid && lengthValid
}
func IsNumbersValid(name string) bool {
```

```go
return !strings.ContainsAny(name, "0123456789")
}
func IsLengthValid(name string) bool {
  length := len(name)
  return length >= 8 && length <= 16
}
Let's say that we want to create a test for IsValidName function, but we
want to mock IsNumbersValid and IsLengthValid functions. The first step
is to create an interface and empty struct as follows:
type ValidationClient struct{}
type ValidationClientInter interface {
  IsNumbersValid(name string) bool
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Mocking"*

```go
func (c *ValidationClient) IsNumbersValid(name string) bool {
 return !strings.ContainsAny(name, "0123456789")
}
func (c *ValidationClient) IsLengthValid(name string) bool {
 length := len(name)
 return length >= 8 && length <= 16
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Mocking"*

```go
var Client ValidationClientInter = &ValidationClient{}
func IsValidName(name string) bool {
 numbersValid := Client.IsNumbersValid(name)
 lengthValid := Client.IsLengthValid(name)
 return numbersValid && lengthValid
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Mocking"*

```go
mockery --all --inpackage
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Mocking"*

```go
mockedClient := &MockValidationClientInter{}
mockedClient.On("IsNumbersValid", mock.Anything).Return(true)
mockedClient.On("IsLengthValid", mock.Anything).Return(true)
Client = mockedClient
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Mocking"*

---

### Fuzz Testing (Go 1.18+)

**Principle:** Fuzz tests use seed inputs to generate random data, uncovering panics and edge cases invisible to unit tests. Functions must be prefixed `Fuzz` and take `*testing.F`.

**Code:**
```go
// ParseName parses a name into first and last.
func ParseName(s string) (string, string, error) {
  parts := strings.Split(s, " ")
  return parts[0], parts[1], nil
}
We created a fuzz test for this function like this:
func FuzzParseName(f *testing.F) {
  f.Add("John Adams")
  f.Add("George Washington")
  f.Fuzz(func(t *testing.T, s string) {
```

```go
_, _, err := ParseName(s)
  if err != nil {
    t.Errorf("%v", err)
  }
 })
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Fuzzy Testing"*

```go
go test -fuzz FuzzParseName -fuzztime=12s
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Fuzzy Testing"*

```go
panic: runtime error: index out of range [1] with length 1
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Fuzzy Testing"*

```go
var ErrInvalidName = errors.New("invalid name")
// ParseName parses a name into first and last.
func ParseName(s string) (string, string, error) {
 parts := strings.Split(s, " ")
 if len(parts) != 2 {
  return "", "", ErrInvalidName
 }
 return parts[0], parts[1], nil
}
func FuzzParseName(f *testing.F) {
 f.Add("John Adams")
 f.Add("George Washington")
 f.Fuzz(func(t *testing.T, s string) {
  _, _, err := ParseName(s)
  if err != nil {
   if errors.Is(err, ErrInvalidName) {
     return
   }
   t.Errorf("%v", err)
  }
```

```go
})
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Fuzzy Testing"*

---

### Microservices Testing — Wrap HTTP Clients

**Principle:** Wrap inter-service HTTP clients in structs that implement interfaces — so you can mock them in unit tests.

**Do:**
- Each service client gets its own interface (more flexible, more work), OR all share a common interface (less flexible, less work).
- Use the Functional Options Pattern to configure Setup/Teardown for inter-service tests.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Microservices Testing"*

---

### Benchmarks

**Principle:** Benchmark tests (`Benchmark*` functions taking `*testing.B`) measure function performance by running `b.N` iterations.

**Code:**
```go
func Fib(n int) int {
 if n < 2 {
  return n
 }
 return Fib(n-1) + Fib(n-2)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Performing Benchmark"*

```go
func BenchmarkFib(b *testing.B) {
 for n := 0; n < b.N; n++ {
  Fib(20)
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Performing Benchmark"*

```go
go test -bench=.
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Performing Benchmark"*

---

### Race Detector

**Principle:** Use `go test -race` or `go run -race` to detect data races at runtime.

**Code:**
```go
func main() {
 i := 0
```

```go
go func() {
   i++
 }()
 fmt.Println(i)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Race Detector"*

```go
go run -race race-detector.go
We will accept a warning
==================
WARNING: DATA RACE
Write at 0x00c00011a028 by goroutine 6:
   main.main.func1()
       /Users/nirshtein/Documents/GitHub/Microservices-with-
     Go/chapter-5/race-detector/race-detector.go:8 +0x3c
Previous read at 0x00c00011a028 by main goroutine:
   main.main()
       /Users/nirshtein/Documents/GitHub/Microservices-with-
     Go/chapter-5/race-detector/race-detector.go:10 +0xa8
Goroutine 6 (running) created at:
   main.main()
       /Users/nirshtein/Documents/GitHub/Microservices-with-
     Go/chapter-5/race-detector/race-detector.go:7 +0x9c
==================
Found 1 data race(s)
exit status 66
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 4 / Race Detector"*

---

### Concurrency vs. Parallelism vs. Asynchrony

**Principle:** Don't conflate the three. Concurrency = interleaved execution. Parallelism = actual simultaneous execution. Asynchrony = events at different times.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Introduction"*

---

### Goroutines — Launching Concurrent Work

**Principle:** Launch a goroutine with the `go` keyword followed by a function call. The Go scheduler manages allocation onto threads.

**Code:**
```go
func main() {
 go printHello() // Hello
 go func() {
  fmt.Println("Hello from anonymous function")
 }() // Hello from anonymous function
 time.Sleep(1 * time.Second)
}
func printHello() {
 fmt.Println("Hello")
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Goroutines"*

---

### Channels — Unbuffered

**Principle:** Unbuffered channels (`make(chan T)`) have zero length — sends block until a receiver is ready.

**Code:**
```go
func main() {
 messages := make(chan string)
 go func() {
  messages <- "ping"
 }()
 msg := <-messages
```

```go
println(msg)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channels - Buffered vs. Unbuffered"*

---

### Channels — Buffered

**Principle:** Buffered channels (`make(chan T, n)`) allow sending up to `n` items without a receiver. Sending to a full channel blocks; sending with no receiver ever causes deadlock.

**Code:**
```go
func main() {
 messages := make(chan string, 2)
 messages <- "ping"
 messages <- "pong"
 println(<-messages) // ping
 println(<-messages) // pong
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channels - Buffered vs. Unbuffered"*

```go
func main() {
 messages := make(chan string, 1)
 messages <- "ping"
 messages <- "pong"
 println(<-messages)
 println(<-messages)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channels - Buffered vs. Unbuffered"*

```go
fatal error: all goroutines are asleep - deadlock!
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channels - Buffered vs. Unbuffered"*

---

### Closing Channels

**Principle:** `close(ch)` prevents further sends but allows remaining receives. Always close from the sender side, never the receiver.

**Code:**
```go
func main() {
 ch := make(chan int)
 close(ch)
 ch <- 1 // panic: send on closed channel
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Closing a Channel"*

---

### Ranging Over a Channel

**Principle:** `for item := range ch` iterates until the channel is closed — forgetting to close deadlocks the loop.

**Code:**
```go
func main() {
 ch := make(chan int, 3)
 for i := 0; i < 3; i++ {
  ch <- i
 }
 close(ch) // if you don't close the channel, deadlock will
 // occur
 for i := range ch {
  fmt.Printf("%d ", i) // 0 1 2
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Range Over a Channel"*

---

### Select — Multiplexing Channels

**Code:**
```go
func main() {
 c1 := make(chan int)
 c2 := make(chan int)
 go func() {
  c1 <- 1
 }()
 go func() {
```

```go
c2 <- 2
 }()
 go func() {
  for {
    select {
    case <-c1:
     println("c1")
    case <-c2:
     println("c2")
    }
  }
 }()
 time.Sleep(1 * time.Second)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Selecting a Channel"*

---

### Channel Directions

**Principle:** Restrict channels to send-only (`chan<-`) or receive-only (`<-chan`) in function signatures for compile-time safety.

**Code:**
```go
func main() {
 ch := make(chan int, 1)
 send(ch)
 recv(ch)
}
func send(ch chan<- int) {
 ch <- 1
}
func recv(ch <-chan int) {
 fmt.Println(<-ch) // 1
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channels Directions"*

---

### Synchronization — "Done" Pattern

**Principle:** Use a buffered bool channel of size 1 to signal "done" between goroutines.

**Code:**
```go
func main() {
 done := make(chan bool, 1)
 go func() {
  println("Start goroutine")
  time.Sleep(1 * time.Second) // simulate work
  println("End goroutine")
  done <- true
 }()
 println("Waiting goroutine")
 <-done
 println("All done")
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Synchronization Between Goroutines"*

---

### sync.WaitGroup — Waiting for Goroutines

**Principle:** WaitGroup is a counter; `Add(delta)` increments, `Done()` decrements, `Wait()` blocks until zero. Pass by pointer when crossing function boundaries.

**Code:**
```go
func main() {
 wg := sync.WaitGroup{}
 wg.Add(5)
 for i := 0; i < 5; i++ {
  go func(i int) {
    defer wg.Done()
    time.Sleep(1 * time.Second)
    println(i)
  }(i)
 }
 fmt.Println("Waiting…")
 wg.Wait()
```

```go
fmt.Println("Done")
}
The output will look like this (the order of the numbers can change):
Waiting…
2
0
1
3
4
Done
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / WaitGroups"*

---

### sync.Mutex — Protecting Shared State

**Principle:** Unprotected concurrent access to shared variables leads to data races (or fatal `concurrent map writes`). Use `mu.Lock()` / `mu.Unlock()` to serialize access.

**Code:**
```go
func main() {
 counter := 0
 wg := sync.WaitGroup{}
 wg.Add(10000)
 for i := 0; i < 10000; i++ {
  go func() {
   defer wg.Done()
```

```go
counter++
  }()
 }
 wg.Wait()
 fmt.Println("counter:", counter)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Locks"*

```go
func main() {
 counter := 0
 wg := sync.WaitGroup{}
 mu := sync.Mutex{}
 wg.Add(10000)
 for i := 0; i < 10000; i++ {
  go func() {
    defer wg.Done()
    mu.Lock()
    counter++
    mu.Unlock()
  }()
 }
 wg.Wait()
 fmt.Println("counter:", counter)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Locks"*

---

### sync.Once — Singleton Pattern

**Principle:** `Once.Do(fn)` runs `fn` exactly once across all goroutines — the cleanest way to implement singletons in Go.

**Code:**
```go
type cache struct{}
var cacheSingleton *cache
var once sync.Once
func main() {
 GetCache()
 GetCache()
 GetCache()
}
func GetCache() *cache {
 once.Do(func() {
  println("Creating singleton object")
  cacheSingleton = &cache{}
 })
 return cacheSingleton
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Singleton in Golang - Once.Do"*

---

### Other sync Primitives

**Principle:** Use higher-level channel patterns when possible; fall back to low-level sync primitives only when justified.

- `sync.Map` — concurrent-safe map.
- `sync/atomic` — shared counters across goroutines.
- `sync.Pool` — temporary object pool to reduce GC pressure.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Low-Level Routines"*

---

### Pub/Sub Pattern in Go

**Principle:** Build Pub/Sub to broadcast messages from publishers to all subscribers of a topic — central to microservices for decoupling, scaling, and real-time notifications.

**Do:**
- Prefer existing libraries (Redis, cloud Pub/Sub) over hand-rolled implementations.
- Remember Pub/Sub vs. Message Broker: Pub/Sub broadcasts (one-to-many, no FIFO, more message loss); Message Broker unicasts (one-to-one, FIFO, more reliable).

**Code:**
```go
type PubSub struct {
 subscribers map[string][]chan interface{}
}
func NewPubSub() *PubSub {
 return &PubSub{
  subscribers: make(map[string][]chan interface{}),
```

```go
}
}
func (ps *PubSub) Publish(topic string, item interface{}) {
 for _, ch := range ps.subscribers[topic] {
  ch <- item
 }
}
func (ps *PubSub) Subscribe(topic string) <-chan interface{} {
 ch := make(chan interface{})
 ps.subscribers[topic] = append(ps.subscribers[topic], ch)
 return ch
}
func main() {
 ps := NewPubSub()
 ch := ps.Subscribe("t1")
 go ps.Publish("t1", "hello")
 item := <-ch
 println(item.(string))
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Pub/Sub"*

---

### Channel Closing Principle — Graceful Close with Multiple Senders

**Principle:** Close channels only from the sender side. With multiple senders, use a `sync.WaitGroup` and close after `wg.Wait()` returns.

**Code:**
```go
func main() {
 ch := make(chan int)
```

```go
wg := &sync.WaitGroup{}
 wg.Add(10)
 for i := 0; i < 10; i++ {
  go Sender(ch, wg, i)
 }
 go func() {
  wg.Wait()
  close(ch) // graceful close
 }()
 // receiver
 for i := range ch {
  println(i)
 }
}
func Sender(ch chan<- int, wg *sync.WaitGroup, i int) {
 defer wg.Done()
 ch <- i
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Channel Closing Principle"*

---

### Goroutine Leak — Forgotten Sender

**Principle:** A sender goroutine that blocks forever on a channel with no receiver is a goroutine leak — manifesting as a memory leak.

**Code:**
```go
func leak(ch chan int) {
 data := <-ch
 fmt.Println(data)
}
func main() {
 ch := make(chan int)
 go leak(ch)

}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Avoiding Goroutine Leak"*

```go
func forgottenSender(ch chan int) {
 data := 3
 // This is blocked as no one is receiving the data
 ch <- data
}
func main() {
 ch := make(chan int)
 go forgottenSender(ch)
 println(runtime.NumGoroutine()) // 2 instead of 1
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Forgotten Sender"*

```go
func forgottenSender(ch chan int) {
 data := 3
 // This is blocked as no one is receiving the data
 ch <- data
}
func main() {
 ch := make(chan int, 1) // avoid goroutine leak by using
 // buffered channel
 go forgottenSender(ch)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Forgotten Sender"*

```go
func networkCall() int {
 return 1
}
func anotherAction() error {
 return errors.New("data is invalid! Returning")
}
func forgottenSender(ch chan int) {
 data := networkCall()
 ch <- data
}
func handler() error {
 ch := make(chan int)
 go forgottenSender(ch)
 err := anotherAction()
 if err != nil {
  return err
 }
 data := <-ch
 fmt.Println(data)
 return nil
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Forgotten Sender"*

```go
func networkCall() int {
 time.Sleep(3 * time.Second)
```

```go
return 1
}
func forgottenSender(ch chan int) {
 data := networkCall()
 ch <- data
}
func handler() error {
 ctx, cancel := context.WithTimeout(context.Background(),
 10*time.Millisecond)
 defer cancel()
 ch := make(chan int)
 go forgottenSender(ch)
 for {
  select {
  case data := <-ch:
    fmt.Printf("received data! %d\n", data)
    return nil
  case <-ctx.Done():
    return errors.New("timeout! Process canceled. Returning")
  }
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Forgotten Sender"*

---

### Goroutine Leak — Abandoned Receiver

**Principle:** If the sender never closes the channel, a `range`-looping receiver blocks forever. Always close the channel after the sender finishes.

**Code:**
```go
func abandonedReceiver(ch chan string) {
```

```go
for data := range ch {
  println(data)
 }
 println("Worker is done")
}
func sender(ch chan string) {
 for _, data := range []string{"one", "two", "three"} {
  ch <- data
 }
}
func handler() {
 ch := make(chan string, 3)
 sender(ch)
 go abandonedReceiver(ch)
}
func main() {
 handler()
 time.Sleep(1 * time.Second)
 println(runtime.NumGoroutine()) // 2 instead of 1
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Abandoned Receiver"*

```go
func sender(ch chan string) {
 for _, data := range []string{"one", "two", "three"} {
  ch <- data
 }
 close(ch) // solve the goroutine leak
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Abandoned Receiver"*

---

### Detecting Goroutine Leaks

**Principle:** Detect leaks via profiling (`pprof`, `gops`) or unit tests asserting on `runtime.NumGoroutine()` or using `uber-go/goleak`.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Detecting Goroutine Leak"*

---

### Fan-Out Pattern

**Principle:** Fan-out distributes work across multiple workers reading from separate channels to parallelize CPU- or I/O-bound processing.

**Code:**
```go
func generator(numbers []int) <-chan int {
 out := make(chan int)
 go func() {
  for _, num := range numbers {
```

```go
out <- num
  }
  close(out)
 }()
 return out
}
func businessLogic(num int) int {
 return num * 2
}
func main() {
 data := []int{1, 2, 3, 4, 5, 6}
 var wg sync.WaitGroup
 ch1 := generator(data[0:3])
 ch2 := generator(data[3:])
 wg.Add(2)
 go func() {
  for num := range ch1 {
    println(businessLogic(num))
  }
  wg.Done()
 }()
 go func() {
  for num := range ch2 {
    println(businessLogic(num))
  }
  wg.Done()
 }()
 wg.Wait()
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Fan Out"*

---

### Fan-In (Multiplexing) Pattern

**Principle:** Fan-in merges multiple source channels into one output channel via a `merge` function. The output is closed only after all input channels close.

**Code:**
```go
func merge(sourcesCh …<-chan int) <-chan int {
 var wg sync.WaitGroup
 wg.Add(len(sourcesCh))
 out := make(chan int)
 outputFunc := func(sourceCh <-chan int) {
  for num := range sourceCh {
   out <- num
  }
  wg.Done()
 }
 for _, sourceCh := range sourcesCh {
  go outputFunc(sourceCh)
 }
 go func() {
  wg.Wait()
  close(out)
 }()
 return out
}
func generator(numbers []int) <-chan int {
 out := make(chan int)
 go func() {
```

```go
for _, num := range numbers {
    out <- num
   }
   close(out)
  }()
  return out
}
func main() {
 data := []int{1, 2, 3, 4, 5, 6}
 ch1 := generator(data[0:3])
 ch2 := generator(data[3:])
 ch := merge(ch1, ch2)
 for num := range ch {
  println(num)
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 5 / Fan In"*

---

### Service Communication — API Calls, Message Brokers, gRPC

**Principle:** Three primary IPC styles in microservices: API calls (REST over HTTP L7), message brokers (Kafka/RabbitMQ/Amazon MQ with retries + DLQ), and gRPC (Protocol Buffers + HTTP/2 with bidirectional streaming).

**Do:**
- Use API calls for the majority of synchronous request/response communication.
- Use message brokers when you need retries, DLQs, monitoring, and message mediation.
- Use gRPC for language-agnostic, high-performance RPC with streaming needs.

**Don't:**
- Don't build a message broker from scratch — it's strenuous and risky; use proven tech.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Communication Between Services"*

---

### API Gateway — Centralizing Cross-Cutting Concerns

**Principle:** A single entry point that consolidates security, observability (metrics/logs/traces), and routing (rate-limiting, caching, load balancing, rolling updates).

**Do:**
- Use the gateway to centralize concerns that would otherwise be duplicated per service.
- Remember the gateway is also a load balancer and a service discovery mechanism.
- In Kubernetes, Ingress provides several gateway capabilities natively.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / API Gateway"*

---

### Service Discovery — Client-Side vs. Server-Side

**Principle:** Service discovery locates the dynamic network addresses of service instances. Two patterns: client-side (client queries service registry directly) and server-side (load balancer mediates).

**Do:**
- Use server-side discovery when you want to avoid duplicating load-balancing logic across languages.
- Use etcd (or the equivalent) as the service registry.

**Don't:**
- Don't choose client-side discovery in polyglot systems — the LB logic gets duplicated per language.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Service Discovery"*

---

### Load Balancer Algorithms

**Principle:** Pick the LB algorithm to match system requirements: Round Robin (simplest), Least Connections, Least Time, Hash (URL/IP/port), Random with Two Choices.

**Do:**
- Treat L7 LBs as the default for microservices (operate on application layer).
- Use mature tech — NGINX, HAProxy, AWS ELB/ALB — rather than building your own.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Load Balancer"*

---

### Database per Service

**Principle:** Highest level of data separation — each service owns its own database. Maximizes loose coupling, technology freedom, and independent scaling.

**Do:**
- Adopt this pattern early — separating databases after a long shared-DB period is very expensive.
- Use Saga or a similar pattern for distributed transactions across services.

**Don't:**
- Don't expect SQL joins across services — they require external aggregation tools.
- Don't underestimate the operational complexity of running many databases.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Database per Service"*

---

### Backends for Frontends (BFF)

**Principle:** Run a separate API gateway per client type (web/mobile/desktop) to optimize data shape and payload per client.

**Do:**
- Use BFF when client needs diverge significantly (mobile needs less data than web).
- Accept the trade-off: better client optimization vs. another network hop and moving part.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Backends for Frontends (BFF)"*

---

### External Configuration

**Principle:** Pull environment-specific config (DB connections, credentials, endpoints) from external sources at startup, typically via environment variables.

**Do:**
- Use Kubernetes ConfigMaps and Secrets to inject configuration.
- Use Helm for templated, even more seamless configuration.

**Don't:**
- Don't bake environment-specific values into the binary.
- Don't confuse dev and production configurations — it's painful.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / External Configuration"*

---

### Service Mesh

**Principle:** A dedicated infrastructure layer handling service-to-service communication (LB, discovery, security, monitoring).

**Do:**
- Consider Istio (Kubernetes), Linkerd, or Consul when you need consistent cross-cutting service communication.

**Don't:**
- Don't underestimate configuration complexity — service mesh can be challenging to tune.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Service Mesh"*

---

### Event-Driven Architecture — Event vs. Message

**Principle:** A **message** is specific (sender/receiver share a schema, destination is predetermined). An **event** is general — contains data (not instructions), is immutable, has no specific destination, and is broadcast to interested consumers.

**Do:**
- Use events for auditing, big-data processing, backend processing, and tracking another system's events.
- Accept trade-offs: decoupled services + scalability vs. data consistency + duplicate events + complexity.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Event Versus Message"*

---

### Event Sourcing

**Principle:** Store all events instead of performing CRUD. Immutability gives a full audit trail; replayability lets you replay from any point.

**Do:**
- Apply event sourcing when you need audit-grade history and replayability.
- Plan for high storage costs, retention policies, indexing, and integrity management.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / Event Sourcing"*

---

### CQRS — Command and Query Responsibility Segregation

**Principle:** Segregate write and read handlers. Writes trigger event aggregation into materialized views; reads query the view, not the raw event store.

**Do:**
- Accept that reads are not immediately consistent with writes.
- Accept that aggregation can be expensive in time and compute.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 6 / CQRS"*

---

### REST Constraints — The Six Rules

**Principle:** REST is an architectural style defined by six constraints. RESTful APIs fulfill all (or most) of them.

1. **Client-Server** — loose coupling; client only knows URIs.
2. **Uniform Interface** — URI identification, manipulation via representations, self-descriptive messages, HATEOAS.
3. **Stateless** — each request carries all needed data; no server-side session dependence.
4. **Layered System** — request passes through layers (auth, caching, LB); client is layer-agnostic.
5. **Cacheable** — responses indicate cacheability.
6. **Code on Demand** (optional) — server may ship executable code.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Constraints"*

---

### Designing an API — Capabilities Checklist

**Principle:** Define capabilities up front from product requirements — don't retrofit.

Standard capabilities: documentation, auth, RBAC, pagination, rate limit, caching, filtering, sorting, monitoring, feature toggling, alerting, error handling, auto-generated client code.

**Do:**
- Build shared infrastructure (`pkg/` for monorepo, SDK for polyrepo) to avoid boilerplate duplication.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Capabilities"*

---

### Swagger / OpenAPI

**Principle:** OpenAPI standardizes API specification (YAML/JSON); Swagger provides tooling — Editor, UI, Codegen (multi-language client/server generation).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Documentation: Swagger and OpenAPI"*

---

### REST API Folder Structure in Go

**Principle:** Two viable layouts, both sharing `cmd/`, `deploy/`, `middleware/`, `server.go`, and `routes_registrator.go`.

- **Option A** — directory per category → directory per resource, each with `controller.go`, `db.go`/`repository.go`, `routes.go`, `service.go`.
- **Option B** — top-level directories per layer (`controllers/`, `routes/`, `repositories/`, `services/`), each with subdirectories per category.

Per-resource files:
- `controller.go` — primary handler; parses request, returns 4XX on bad input, returns data per OpenAPI spec.
- `db.go` / `repository.go` — all DB operations; switch databases by editing only this file.
- `routes.go` — declares all endpoints for the resource.
- `service.go` — business logic.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / API Folder Structure"*

```go
func RegisterRoutes(group *gin.RouterGroup) {
 group.GET("/fruits/apple/search",gin.HandlersChain{Process
 RequestSearch}…)
group.GET("/fruits/apple/:id",
gin.HandlersChain{ProcessRequestID}…)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / API Folder Structure"*

---

### HTTP Resource Methods & Status Codes

**Principle:** Map operations to the correct HTTP verb and status code.

- `GET` — Read (cacheable, idempotent).
- `POST` — Create (not cacheable, not idempotent).
- `PUT` — Update/replace (idempotent).
- `DELETE` — Remove.
- `PATCH`, `OPTIONS`, `HEAD`, `CONNECT`, `TRACE` — less common.

Status codes: 2XX success (200 OK, 201 Created), 3XX redirection, 4XX client errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found), 5XX server errors (500 Internal Server Error).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Resources Methods"*

---

### Crafting a Gin Server

**Principle:** Build the engine with middleware (logger, recovery, CORS), register route groups, then run via `http.Server.ListenAndServe()`.

**Code:**
```go
func main() {
 port := 8080
 engine := internal.BuildEngine()
 srv := &http.Server{
  Addr: fmt.Sprintf(":%d", port),
  Handler: engine,
 }
 log.Printf("Starting server on port %d", port)
 if err := srv.ListenAndServe(); err != nil && err !=
 http.ErrServerClosed {
  log.Print("error while running API gin server", "error",
  err.Error())
  os.Exit(1)
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Gin Gonic Setup"*

```go
func BuildEngine() *gin.Engine {
 engine := gin.New()
 engine.Use(gin.Logger())
 engine.Use(gin.Recovery())
 engine.Use(CORS())
 group := engine.Group("/api")
 RegisterRoutes(group)
 // engine.use(<any middleware you want>)
 return engine
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Gin Gonic Setup"*

```go
func RegisterRoutes(routerGroup *gin.RouterGroup) {
 apple.RegisterRoutes(routerGroup)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Gin Gonic Setup"*

```go
package apple
import "github.com/gin-gonic/gin"
var Path = "/fruits/apple"
func RegisterRoutes(group *gin.RouterGroup) {
  group.GET(Path, gin.HandlersChain{ProcessRequest}…)
}
And in the controller.go file:
package apple
import "github.com/gin-gonic/gin"
func ProcessRequest(c *gin.Context) {
  c.JSON(200, gin.H{
   "color": "red",
   "date": "2023-12-11",
   "taste": "sweet",
  })
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Gin Gonic Setup"*

---

### CORS Middleware

**Code:**
```go
func CORS() gin.HandlerFunc {
 return func(c *gin.Context) {
  c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
  c.Writer.Header().Set("Access-Control-Allow-Credentials",
  "true")
  c.Writer.Header().Set("Access-Control-Allow-Methods", "POST,
  GET")
  c.Next()
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / CORS"*

---

### Pagination Strategies

**Principle:** Three primary algorithms: page number, offset+limit (most common), and cursor-based (auto-increment PK).

```
GET /api/users?page=2
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Pagination"*

```
GET /api/users?limit=10
GET /api/users?limit=10&offset=10
GET /api/users?limit=10&offset=20
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Pagination"*

```
GET /api/users?limit=10
GET /api/users?limit=10&cursor=
<last_id_from_previous_request>
GET /api/users?limit=10&cursor=
<last_id_from_previous_request>
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Pagination"*

---

### Rate Limiting

**Principle:** Block excessive requests per time interval; return HTTP 429 (Too Many Requests). Implement as reusable middleware in a shared package.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Rate Limit"*

---

### Panic Recovery Middleware

**Principle:** A single endpoint's panic should never crash the whole server — recover from panics and return 500.

**Code:**
```go
engine.Use(gin.Recovery())
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Panic Recovery"*

```go
func WithCustomRecovery() gin.HandlerFunc {
 return func(c *gin.Context) {
  defer func() {
   if err := recover(); err != nil {
     _ = c.Error(fmt.Errorf("[recovered] panic: %v", err))
```

```go
c.AbortWithStatusJSON(http.StatusInternalServerError,
     gin.H{"Error": "Internal Server Error"})
    }
  }()
  c.Next()
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Panic Recovery"*

---

### Graceful Shutdown

**Principle:** On SIGINT/SIGTERM, give on-flight requests a grace period (e.g., 10 s) to complete using `context.WithTimeout` and `srv.Shutdown()`.

**Code:**
```go
func main() {
 port := 8080
 engine := internal.BuildEngine()
 srv := &http.Server{
  Addr: fmt.Sprintf(":%d", port),
  Handler: engine,
 }
 log.Printf("Starting server on port %d", port)
 startHTTPServer(srv)
}
func startHTTPServer(srv *http.Server) {
 // Create context that listens for the interrupt signal from
 // the OS.
```

```go
sigCtx, stopSig := signal.NotifyContext(context.Background(),
  syscall.SIGINT, syscall.SIGTERM)
 defer stopSig()
 go func() {
  if err := srv.ListenAndServe(); err != nil && err !=
  http.ErrServerClosed {
   log.Print("error while running API gin server", "error",
   err.Error())
   os.Exit(1)
  }
 }()
 // Listen for the interrupt signal.
 <-sigCtx.Done()
 // Restore default behavior on the interrupt signal and notify
 // a user of a shutdown.
 stopSig()
 // Requests are currently on-flight; wait 10 seconds for them
 // to finish.
 ctx, cancel := context.WithTimeout(context.Background(),
 10*time.Second)
 defer cancel()
 if err := srv.Shutdown(ctx); err != nil {
  log.Print("server forced to shutdown: ", "error",
  err.Error())
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Graceful Shutdown"*

---

### Filtering

**Principle:** Three styles: path params (specific cases), query params (most popular, keep simple), request body (complex filtering).

```
GET /api/accounts/{category} -> GET
/api/accounts/Enterprise
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Filter"*

```
GET /api/accounts?category=Enterprise&size_gt=500
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Filter"*

```
POST /api/accounts
Content-Type: application/json
{
 "or": {
  "category": "Enterprise",
  "size_gt": 500,
 }
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Filter"*

---

### Sorting

**Principle:** Use `sort` and `order` query params. Support ascending, descending, and multi-field.

```
GET /api/accounts?sort=size&order=asc
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Sort"*

```
GET /api/accounts?sort=size&order=desc
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Sort"*

```
GET /api/account?sort=effective_score,-size
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Sort"*

---

### Caching

**Principle:** Use `Expires`, `Cache-Control`, and `Last-Modified` headers. GET is cacheable by default, POST only on explicit request, PUT/DELETE never.

```
Expires: Sun, 21 June 2023 16:27:59 GMT
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Caching"*

---

### REST URI Conventions

**Do:**
- Use nouns, not verbs (`DELETE /api/accounts/{id}`, not `GET /api/deleteAccounts/{id}`).
- Use plural for collections (`/accounts`).
- Use hyphens for readability (`/user-management`).
- No trailing slashes, no backward slashes, no file extensions.

**Don't:**
- Don't include the operation name in the URI.
- Don't make endpoints overcomplicated — split into multiple endpoints when needed.

```
GET /api/accounts: Collection resource
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Conventions"*

```
GET /api/deleteAccounts/{id} - bad
DELETE /api/accounts/{id} - good
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Conventions"*

```
GET /api/user-management
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Conventions"*

```
GET /api/account/ - bad
GET /api/account - good
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Conventions"*

```
GET /api/accounts/billing.json - bad
GET /api/accounts/billing - good
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Conventions"*

---

### API Versioning Strategies

**Principle:** Three strategies: URI versioning (popular, easy), query parameter (no URL change), header versioning (most REST-aligned, but version is hidden).

```
GET /api/v1/accounts
GET /api/v2/accounts
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Versioning Strategies"*

```
GET /api/account?version=1
GET /api/account?version=2
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Versioning Strategies"*

```
GET /api/accountsHeaders: { "X-API-version": "1" }
GET /api/accountsHeaders: { "X-API-version": "2" }
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Versioning Strategies"*

**Best Practices:**
- Use semantic versioning: `major.minor.patch`.
- Major = breaking changes; Minor = backward-compatible features; Patch = bug fixes.
- Always preserve backward compatibility.
- Communicate changes clearly.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Versioning Best Practices"*

---

### API Deprecation

**Principle:** Deprecate gracefully with long grace periods, frequent customer communication, and explicit `deprecated` markers in docs.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Deprecation"*

---

### REST Common Pitfalls

- **Overusing POST** — use the full verb vocabulary (DELETE, PATCH, PUT, GET).
- **Bad resource naming** — confusing "resource" leads to bad URIs.
- **Lack of versioning** — keep API versioning and deprecation discipline.
- **Inappropriate HTTP status codes** — don't just default to 200/400/500.
- **Messy Swagger docs** — misinformation hurts consumers.
- **Overcomplicating** — keeping it simple is hard but mandatory.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 7 / Common Pitfalls"*

---

### Kubernetes Essentials — Tools

**Principle:** Three tools every K8s dev needs: `kind` (cluster in Docker for local/testing), `kubectl` (CLI for K8s API), `kubectx` (cluster context switcher).

```
kubectl get pods
kubectl get nodes --output json
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Kubectl"*

```
kubectl create -f pod.yaml
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Kubectl"*

```
kubectl apply -f pod.yaml
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Kubectl"*

```
kubectl delete pods/frontend
To see all the commands kubectl has, we can run:
kubectl help
kubectl help <command-name>
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Kubectl"*

---

### Kubernetes Basic Resources — Node, Namespace, Pod

**Principle:** Node = worker machine; Namespace = isolation mechanism (names must be unique within); Pod = smallest deployable unit (containers sharing volumes + network).

```
kubectl api-resources
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Namespace"*

---

### Kubernetes Workloads

**Principle:** Match the workload type to the service's needs.

- **Deployment** — stateless services (most common); managed via ReplicaSets.
- **DaemonSet** — one Pod per Node (storage/network/log daemons).
- **StatefulSet** — persistent state or unique identity; pods recreated with same name + PV/PVC.
- **Job** — runs to completion (data processing).
- **CronJob** — Job + cron scheduler (backups, maintenance).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 name: random-deployment
spec:
 replicas: 3
 selector:
  matchLabels:
    app: random-app
 template:
  metadata:
    labels:
     app: random-app
  spec:
    containers:
    - name: random-container
     image: nginx:latest
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Deployment"*

```yaml
spec:
 schedule: "*/5 * * * *" # Runs every 5 minutes
 jobTemplate:
  spec:
    template:
     metadata:
      labels:
        app: random-cronjob
     spec:
      containers:
      - name: random-container
        image: busybox
        command: ["echo", "Hello from the cronjob!"]
      restartPolicy: OnFailure
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / CronJob"*

---

### ConfigMap & Secret

**Principle:** ConfigMap stores non-confidential key-value data; Secret stores sensitive data (passwords, API keys, certs). Both inject into Pods via env vars, args, or volumes.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
 name: random-configmap
data:
 app_name: my-app
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / ConfigMap"*

---

### HPA & Ingress

**Principle:** HPA (Horizontal Pod Autoscaler) scales replica count by CPU/memory metrics within configurable min/max bounds. Ingress exposes HTTP/HTTPS routes from outside the cluster and consolidates API gateway concerns (LB, security, routing).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / HPA" & "Ingress"*

---

### Readiness and Liveness Probes

**Principle:** Readiness probe = can the container accept traffic? Liveness probe = is it healthy, or does it need a restart? Probes can use HTTP GET, TCP socket, or shell command.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 name: web-app-deployment
spec:
 replicas: 3
 selector:
  matchLabels:
    app: web-app
 template:
  metadata:
    labels:
```

```yaml
app: web-app
spec:
 containers:
 - name: web-app-container
  image: nginx:latest
  ports:
  - containerPort: 80
  readinessProbe:
    httpGet:
     path: /healthz
     port: 80
    initialDelaySeconds: 5
    periodSeconds: 10
  livenessProbe:
    httpGet:
     path: /status
     port: 80
    initialDelaySeconds: 10
    periodSeconds: 15
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Readiness and Liveness Probes"*

---

### Resource Requests & Limits

**Principle:** `requests` guide the scheduler; `limits` are enforced by the kubelet. CPU over-limit → throttling; memory over-limit → Pod kill + restart.

```yaml
apiVersion: v1
kind: Pod
metadata:
 name: example
spec:
 containers:
 - name: hello
  image: hello-world:latest
  resources:
    requests:
     memory: "128Mi"
     cpu: "250m"
    limits:
     memory: "256Mi"
     cpu: "1"
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Resources Allocations"*

---

### Kubernetes Best Practices

**Do:**
- **YAML hygiene** — clean configs, no redeclared defaults, proper labels/annotations.
- **Logging** — include service name (not pod name), version, and cluster/node info.
- **Environment management** — choose between separate clusters (full isolation, high overhead) or separate namespaces (low isolation, low overhead).
- **Proper monitoring** — track resources (CPU/mem/storage), container status (restarts, probes), and Kubernetes events.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 8 / Kubernetes Best Practices"*

---

### CI/CD

**Principle:** CI/CD is a cultural shift — frequent integration, automated testing, automated packaging, and (optionally) automated production release.

- **CI** — plan, code, build, test.
- **Continuous Delivery** — automated packaging + deployment with manual production approval.
- **Continuous Deployment** — fully automated production release.

**Do:**
- Use CI/CD in microservices to maintain consistency across services and scale deployment as service count grows.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / CI/CD"*

---

### Timeouts — Channel + select, or context

**Principle:** Timeouts prevent unnecessary on-flight requests that overload services. Implement via `select` + `time.After()` or `context.WithTimeout()`.

**Code:**
```go
// Example with timeout
resultCh := make(chan string, 1)
go func() {
 time.Sleep(3 * time.Second)
 resultCh <- "Received before timeout"
```

```go
}()
select {
case res := <-resultCh:
 println(res)
case <-time.After(2 * time.Second):
 println("Timeout")
}
// Output: Timeout
// Example without timeout
resultCh = make(chan string, 1)
go func() {
 time.Sleep(1 * time.Second)
 resultCh <- "Received before timeout"
}()
select {
case res := <-resultCh:
 println(res)
case <-time.After(2 * time.Second):
 println("Timeout")
}
// Output: Received before timeout
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Timeouts"*

```go
ctx, _ := context.WithTimeout(context.Background(),
 2*time.Second)
go func() {
 select {
  case <-ctx.Done():
   println("Timeout")
   os.Exit(1)
  }
}()
time.Sleep(3 * time.Second)
```

```go
fmt.Println("Done")
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Timeouts"*

---

### Retries with Exponential Backoff

**Principle:** A simple retry can dramatically reduce error rates. Aim for ~2 retries on top of the initial try, with exponential backoff (1, 2, 4, 8, 16, … seconds).

**Code:**
```go
func main() {
 err := Retry(3, time.Second, func() error {
  fmt.Println("trying…")
  return fmt.Errorf("some error")
 })
 if err != nil {
  fmt.Printf("error: %s\n", err)
 }
}
func Retry(attempts int, sleep time.Duration, f func() error)
(err error) {
 currentAttempt := 1
 for {
  err = f()
```

```go
if err == nil {
    return nil
   }
   if currentAttempt >= attempts {
     return fmt.Errorf("after %d attempts, last error: %w",
     attempts, err)
   }
   time.Sleep(sleep)
   sleep *= 2
   currentAttempt++
  }
}
The output:
trying…
trying…
trying…
error: after 3 attempts, last error: some error
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Retries"*

---

### Fallback

**Principle:** When retries can't solve the problem, execute a trusted fallback function — error-free or, at minimum, user-informing.

**Code:**
```go
func main() {
 result, err := performOperation()
 if err != nil {
  // Fallback operation in case of an error
  result = fallbackOperation()
 }
```

```go
fmt.Println("Result:", result)
}
func performOperation() (string, error) {
 return "", fmt.Errorf("Operation failed")
}
func fallbackOperation() string {
 return "Fallback result"
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Fallback"*

---

### Circuit Breaker — Closed / Open / Half-Open

**Principle:** Monitor a service's availability; if failures exceed a threshold, "open" the circuit and block calls to give the failing service time to recover. After a timeout, allow limited "half-open" probe requests; success → return to "closed".

**Do:**
- Use an existing library like `github.com/sony/gobreaker` — don't roll your own.
- Tune the failure threshold (e.g., 10 failures per minute), open-state timeout, and half-open probe count.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Circuit Breaker"*

---

### Bulkhead Pattern

**Principle:** Isolate components so failure in one can't cascade. At system level: separate replicas with isolated resources (e.g., separate cache per replica). At service level: cap concurrent goroutines.

**Code (using `sizedwaitgroup`):**
```go
package main
import (
 "fmt"
 "time"
 "github.com/remeh/sizedwaitgroup"
)
func main() {
 swg := sizedwaitgroup.New(5)
 for i := 0; i < 100; i++ {
  swg.Add()
  go func(i int) {
    defer swg.Done()
    logic(i)
  }(i)
 }
 swg.Wait()
}
func logic(i int) {
 fmt.Println(i)
 time.Sleep(1 * time.Second)
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Bulkhead"*

---

### Authentication — Verify Identity

**Principle:** Authentication verifies *who you are*. Options: third-party services (Auth0, Firebase), self-implemented (JWT, session-based), or frameworks (Passport.js, Spring Security).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Authentication"*

---

### Authorization — Enforce Permissions

**Principle:** Authorization decides *what you can do*. It requires business logic — only the product team can define per-user permissions. Inject permissions via middleware; reuse via a central authorization service or shared code.

**Do:**
- Implement RBAC/ABAC at the middleware or DB level (e.g., `POST /users` for admins only; `GET /views` for all users; `DELETE /views` for admins only).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Authorization"*

---

### Feature Toggling in Go

**Principle:** Feature flags are dynamic (usually boolean) values that control runtime visibility of features — useful for A/B testing, gradual rollouts, and load testing.

**Do:**
- Implement via environment variables for simplicity, or use a SaaS like LaunchDarkly for advanced control.

**Code:**
```go
func main() {
 if getEnvBool("feature-a", false) {
  fmt.Println("Feature A is enabled. Performing Feature A
  logic.")
  // Include Feature A logic here
 } else {
  fmt.Println("Feature A is not enabled.")
 }
 if getEnvBool("feature-b", false) {
```

```go
fmt.Println("Feature B is enabled. Performing Feature B
  logic.")
  // Include Feature B logic here
 } else {
  fmt.Println("Feature B is not enabled.")
 }
 // Rest of the application logic
}
func getEnvBool(flagName string, defaultValue bool) bool {
 value, exists := os.LookupEnv(flagName)
 if !exists {
  return defaultValue
 }
 result, err := strconv.ParseBool(value)
 if err != nil {
  fmt.Printf("Error parsing environment variable %s: %v\n",
  flagName, err)
  return defaultValue
 }
 return result
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Feature Toggling"*

---

### Rollout Strategies

**Principle:** Five rollout techniques, each with a speed/safety/cost trade-off.

- **Basic Deployment** (`.spec.strategy.type==Recreate`) — kill all old Pods, start new. Fastest, riskiest.
- **Rolling Update** (`.spec.strategy.type==RollingUpdate`) — gradual transition with `maxUnavailable` + `maxSurge`.
- **Blue-Green Deployment** — full new version alongside old; manual switch. Safest, most expensive. Requires ArgoCD or similar.
- **Multi-Service Rollout** — roll out several services as a unit via Helm.
- **Canary Deployment** — gradual traffic split between versions with manual decision. Requires ArgoCD.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Rollouts"*

---

### Rollbacks

**Principle:** Revert to a previous revision when a new version causes issues.

```
kubectl rollout undo <kind>/<resource-name> --to-revision=
<revision-number>
kubectl rollout undo deployment/nginx-deployment --to-
revision=2
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Rollbacks"*

```
helm rollback <RELEASE> [REVISION] [flags]
helm rollback frontend-services 13
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 9 / Rollbacks"*

---

### Monitoring vs. Observability

**Principle:** Monitoring answers **what** is happening (continuous observation, dashboards, alerts). Observability answers **why and how** the system behaves — using logs, metrics, and tracing together.

**Do:**
- Build observability stack: centralized monitor (Prometheus/Grafana or DataDog/NewRelic), agents (DaemonSet per node), and per-language SDKs.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Monitoring" & "Observability"*

---

### Logs — Levels & Structured Format

**Principle:** Logs are records of events with metadata, level, and message. Use structured JSON, not plain text.

Levels (in order of severity):
- **Info** — useful info, default level.
- **Debug** — detailed debugging info; removed later.
- **Warning** — potentially problematic; no immediate remediation.
- **Error** — bad, requires user intervention.
- **Fatal** — forces service shutdown; instant reaction required.

**Do:**
- Use Go's `log` package, or `github.com/sirupsen/logrus` for advanced options.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Logs"*

---

### Metrics — Counter, Gauge, Histogram

**Principle:** Three primary metric types:
- **Counter** — cumulative, only increases (or resets to 0). E.g., total requests, failed requests.
- **Gauge** — arbitrary value that goes up or down. E.g., CPU usage, active users.
- **Histogram** — samples observations counted in buckets. E.g., latency distribution.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Metrics"*

---

### Tracing & Distributed Tracing

**Principle:** Tracing follows request flow through functions/services. Each step is a *span*; an entire trace tells a user's story. Distributed tracing extends this across many services — essential for microservices debugging.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Tracing"*

---

### Production Troubleshooting — Remediate, RCA, Resolve

**Principle:** Three-step process:
1. **Remediation** — immediate action to restore health (rollback, revert PR, scale up, fix config).
2. **RCA (Root Cause Analysis)** — identify underlying cause via dashboards, logs, metrics, K8s events, profiling, anomaly detection.
3. **Resolve** — prevent recurrence (bug fix, config tuning, scaling).

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Production Troubleshooting"*

---

### The Power of Theory

**Principle:** There is no observability without theory, and no theory without observability. Each investigation should form a hypothesis (theory) and validate it against the data — data without theory is meaningless; theory without data is guessing.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / The Power of Theory"*

---

### Profiling with pprof

**Principle:** Go's built-in `net/http/pprof` exposes runtime profiling endpoints. Import it with a blank identifier, serve it on a port, then analyze with `go tool pprof`.

**Do:**
- Import `_ "net/http/pprof"` to register handlers.
- Serve on a separate port (commonly `:6060`).
- Analyze heap, CPU, and goroutines: `go tool pprof -web http://localhost:6060/debug/pprof/heap`.

**Code:**
```go
package main
import (
 "net/http"
 _ "net/http/pprof"
 "sync"
 "time"
)
var leakSlice1 = []string{}
var leakSlice2 = []string{}
var leakSlice3 = []string{}
func main() {
 // start pprof server
```

```go
go func() {
   http.ListenAndServe(":6060", nil)
  }()
 wg := sync.WaitGroup{}
 wg.Add(1)
 go leak(&wg)
 wg.Wait()
}
func leak(wg *sync.WaitGroup) {
 defer wg.Done()
 for i := 0; i < 10_000_000; i++ {
  appendToLeakSlice1()
  if (i % 10_000) == 0 {
    time.Sleep(100 * time.Millisecond)
  }
 }
}
func appendToLeakSlice1() {
 leakSlice1 = append(leakSlice1, "a")
 appendToLeakSlice2()
}
func appendToLeakSlice2() {
 leakSlice2 = append(leakSlice2, "ab")
 appendToLeakSlice3()
}
func appendToLeakSlice3() {
 leakSlice3 = append(leakSlice3, "abc")
}
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Profiling"*

```go
go func() {
 http.ListenAndServe(":6060", nil)
}()
```
*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Profiling"*

---

### PGO — Profile-Guided Optimization (Go 1.21+)

**Principle:** The Go compiler uses profiling data (`default.pgo` or `go build -pgo=/path/to/file.pprof`) to generate higher-performance binaries.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / PGO"*

---

### Common Performance Issues

- **CPU Throttling** — Pod hits its CPU `limit` in K8s; performance degrades without restart.
- **Memory Leak** — application consumes memory without releasing it; Pod restarts at memory limit.
- **Goroutine Leak** — blocked goroutines never GC'd; detectable via `pprof`.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Performance Issues"*

---

### Alerting

**Principle:** Automated notifications when metrics cross thresholds. Use PagerDuty or Atlassian Opsgenie with escalation via Slack, email, SMS, phone calls, and configurable on-call schedules.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Alerting"*

---

### Recommended Performance Metrics for RESTful APIs

**Principle:** Three metrics to monitor and alert on:
- **Requests Success Rate** — % of successful requests. Count only 5XX as failures. Measure in "nines" (e.g., 99.999% = five nines).
- **P95 Latency** — 95% of request durations fall under this value.
- **P99 Latency** — 99% of request durations fall under this value.

**Do:**
- Measure only successful requests for latency (avoid average flooding).
- Use percentiles, not averages, to reflect real user experience.

*Ref: Ultimate_Microservices_with_Go.md — "Chapter 10 / Performance Metrics"*

---

## Anti-Patterns & Common Mistakes

- **Goroutine leak via forgotten sender** — sender blocks forever on unbuffered channel with no receiver → *fix:* use a buffered channel of size ≥ 1.
- **Goroutine leak via abandoned receiver** — receiver `range`s over a never-closed channel → *fix:* always close from the sender side after the sender finishes.
- **Closing channels from the receiver** — causes `send on closed channel` panics → *fix:* close only from the sender side; with multiple senders, use a WaitGroup to perform a graceful close.
- **Unprotected shared state across goroutines** — `concurrent map writes` fatal or lost updates → *fix:* wrap with `sync.Mutex` or use `sync.Map`.
- **Overusing POST** — using POST for delete/update operations → *fix:* use the right HTTP verb.
- **Inappropriate HTTP status codes** — always 200/400/500 → *fix:* use 201 Created, 401/403/404, etc.
- **Wrapping context.Background() mid-request** — breaks propagation of cancellation/auth/tracing → *fix:* derive child contexts from the parent.
- **No timeouts on inter-service calls** — overload and slow failures → *fix:* always set timeouts via `context.WithTimeout` or `select` + `time.After`.
- **No retries / retries without backoff** — burst retry storms hammer failing services → *fix:* ~2 retries with exponential backoff.
- **No circuit breaker** — cascading failures → *fix:* `sony/gobreaker` with closed/open/half-open states.
- **No bulkhead** — one slow consumer starves others → *fix:* cap concurrent goroutines with `sizedwaitgroup`.
- **Logging Pod name instead of service name** — can't correlate logs across replicas → *fix:* log service name, version, and cluster/node info.
- **Skipping graceful shutdown** — on-flight requests dropped on SIGTERM → *fix:* `srv.Shutdown(ctx)` with a grace period.
- **Messy Swagger docs** — misinformation hurts consumers → *fix:* keep OpenAPI specs accurate and reviewed.
- **No API versioning** — breaking changes hurt clients → *fix:* semantic versioning with deprecation grace periods.
- **Database sharing across services** — tight coupling + ad-hoc SQL joins → *fix:* database per service.

## Decision Heuristics / Checklists

- **When to use microservices** — adopt when Agile + cloud + Docker + DevOps maturity is present; the operations tax is otherwise too high.
- **Monolith vs. SOA vs. Serverless vs. Microservices** — pick by decomposition granularity and operations appetite.
- **Buffered vs. unbuffered channels** — default to unbuffered; switch to buffered when the receiver lags or synchronization is required before retrieval.
- **Mutex vs. channel** — use channels for higher-level coordination; use `sync.Mutex` for low-level shared-state protection.
- **Functional Options vs. config struct** — use Functional Options when many optional fields exist and you want fluent construction.
- **REST vs. gRPC vs. message broker** — REST for synchronous request/response; gRPC for high-perf RPC + streaming; broker for retries/DLQ/decoupling.
- **Client-side vs. server-side discovery** — server-side wins in polyglot systems (no duplicated LB logic).
- **Database per service checklist** — accept the operational cost; plan for distributed transactions (Saga); abandon cross-service SQL joins.
- **Rollout strategy** — Basic (fast, risky) < Rolling Update (default) < Canary (observe + decide) < Blue-Green (safest, expensive).
- **Percentile vs. average latency** — always prefer P95/P99 to avoid average flooding.
- **K8s environment separation** — separate clusters (full isolation, high overhead) vs. separate namespaces (less isolation, low overhead).

## Key Takeaways

1. **Microservices and Go are a natural pair.** Go's simplicity, fast compilation, lightweight concurrency (goroutines), and strong standard library suit the many small, independent services microservices demand.
2. **Go's design philosophy prioritizes simplicity and maintainability.** ~25 keywords, no inheritance (composition instead), explicit error handling (no try-catch), and 1.x backward compatibility.
3. **Concurrency is Go's superpower — but goroutine leaks are real.** Always close channels from the sender side; use buffered channels to prevent forgotten senders.
4. **REST is the dominant API style for microservices.** The six REST constraints map naturally to microservices principles; Gin is an effective Go foundation.
5. **Kubernetes solves microservices' operations complexity.** ConfigMaps/Secrets (external config), Ingress (gateway), HPA (autoscaling), probes (health), Deployments/StatefulSets (workloads).
6. **Design for failure from the start.** Timeouts, retries with exponential backoff, fallback, circuit breakers, bulkheads — these prevent cascading failures.
7. **CI/CD is essential at scale.** Automated pipelines maintain consistency across services and prevent deployment from becoming the bottleneck.
8. **Observability is non-negotiable.** Logs (what happened), metrics (counters/gauges/histograms), and tracing (request flow) together answer "why and how."
9. **Rollout strategies must balance speed and safety.** Choose per service — basic (fastest, riskiest) to blue-green (safest, most expensive) — and use feature toggles for gradual releases.
10. **Production is a continuous responsibility.** Monitor, alert, profile (CPU throttling, memory leaks, goroutine leaks), and follow the remediate → RCA → resolve troubleshooting loop.

## Cross-References
- Related: [[../summaries/Ultimate_Microservices_with_Go_-_Nir_Shtein.md]]
- Source: `markdown_output/Ultimate_Microservices_with_Go_-_Nir_Shtein/Ultimate_Microservices_with_Go_-_Nir_Shtein.md`
- Topic index: [[../INDEX.md]]
