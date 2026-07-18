# Functional Programming in Go
**Author:** Dylan Meeus
**Topic tags:** `#general` `#testing`
**Language focus:** Go 1.18+ (with pre-generics caveats)
**Sources:** `markdown_output/Functional_Programming_in_Go_-_Dylan_Meeus/Functional_Programming_in_Go_-_Dylan_Meeus.md` · `summaries/Functional_Programming_in_Go_-_Dylan_Meeus.md`

## TL;DR
Treat functions as values, prefer pure transformations over hidden mutation, and isolate unavoidable effects at the program edges. Use Go value semantics, generics, closures, typed function contracts, explicit option/result values, and benchmarks to make behavior predictable and composable. Apply functional techniques where they improve Go code; do not force purity, recursion, currying, or libraries where a direct imperative solution is clearer.

---

## Best Practices by Topic

### 1. Treat Functional Programming as a Go Tool, Not a Doctrine
*Principle: Combine functional and object-oriented techniques according to the problem; do not pretend Go is a purely functional language..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "The Go programming paradigm", "Why functional programming?", "Why not functional programming in Go?", "Comparing FP and OOP"*

**Do:** Use first-class functions, higher-order functions, value semantics, generics, and recursion when they improve readability and testability.; Compose small functions and limit side effects to the program boundaries.; Trade functional elegance for measured performance or simpler Go when needed.; Follow an established codebase's conventions when paradigm novelty would cost more than it returns..

**Don't:** Don't claim FP is inherently superior to OOP.; Don't force pure FP despite required I/O, randomness, or existing team style.; Don't assume Go provides tail-call optimization, lazy evaluation, or purity guarantees..
### 2. Say What to Compute, Not Every Mechanical Step
*Principle: Prefer declarative pipelines that name intent over hand-written loops, branches, and accumulators..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Say what you want, not how you want it", "The Go programming paradigm"*

**Do:** Read a chain as a sequence of domain transformations.; Keep imperative mechanics inside small reusable functions.; Choose readable style for the team, not your personal taste..

**Don't:** Don't equate concision with readability.; Don't hide expensive eager work behind a fluent chain.; Don't replace an obvious loop with a cryptic abstraction..

```
func DeclarativeFunction() int {
    return IntRange(-10,10).
        Abs().
        Filter(func(i int64) bool {
            return i % 2 == 0
        }).
        Sum()
    // result = 60
}

func iterativeFunction() int {
    sum := 0
    for i := -10; i <= 10; i++ {
        absolute := int(math.Abs(float64(i)))
        if absolute%2 == 0 {
            sum += absolute
        }
    }
    return sum
}

package main
import "fmt"
func main() {
     fmt.Println("Hello Reader!")
}
```
### 3. Name Primitive Types to Express Intent
*Principle: Replace ambiguous primitives with local named types when the name carries domain meaning or supports domain behavior..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Type aliases for primitives"*

**Do:** Distinguish phone numbers, ages, names, countries, and identifiers at compile time.; Attach validation methods to locally defined primitive-based types.; Use typed parameters to make signatures and IDE hints self-documenting..

**Don't:** Don't make a full struct when a named string or int is sufficient.; Don't accept several indistinguishable strings when order mistakes are plausible.; Don't try to attach methods to non-local primitive types..

```go
type Person struct {
   name string
phonenumber string
}
func (p *Person) setPhoneNumber(s string) {
    p.phonenumber = s
}

type phoneNumber string
type Person struct {
    name string
    phonenumber phoneNumber
}
func (p *Person) setPhoneNumber(s phoneNumber) {
    p.phonenumber = s
}

func (p *Person) update(name, phonenumber string) {
    p.name = name
    p.phonenumber = phonenumber
}
```

```text
./prog.go:26:18: cannot use phonenumber (variable of type
 string) as type phoneNumber in assignment
```

```go
func (p *Person) update(name string, phonenumber phoneNumber) {
    p.name = name
    p.phonenumber = phonenumber
}

type age uint
type Person struct {
    name string
age age
   phonenumber phoneNumber
}

func (a age) valid() bool {
    return a < 120
}
func isValidPerson(p Person) bool {
    return p.age.valid() && p.name != ""
}
```

```go
func (u uint) valid() bool {
    return u < 120
}
```

```text
./prog.go:30:7: cannot define new methods on non-local type
 uint
Go build failed.
```
### 4. Name Function Signatures
*Principle: Give recurring function contracts a type name so signatures, compiler errors, and composition reveal intent..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Type aliases for functions"*

**Do:** Define contracts such as `Predicate`, `PaymentFunc`, `CipherFunc`, and `Node`.; Keep structural function compatibility as a compile-time check.; Use the named type throughout higher-order APIs..

**Don't:** Don't repeat a long raw function signature everywhere.; Don't reach for an interface when one function contract is the entire abstraction..

```go
func filter(is []int, predicate func(int) bool) []int {
   out := []int{}
   for _, i := range is {
 if predicate(i) {
 out = append(out, i)
 }
   }
   return out
}

type predicate func(int) bool
func filter(is []int, p predicate) []int {
   out := []int{}
   for _, i := range is {
 if p(i) {
 out = append(out, i)
 }
   }
   return out
}

filter(ints, func(i int, s string) bool { return i > 2 })
```

```text
./prog.go:9:15: cannot use func(i int, s string) bool {…}
(value of type func(i int, s string) bool) as type func(int)
bool in argument to filter

./prog.go:9:15: cannot use func(i int, s string) bool {…}
(value of type func(i int, s string) bool) as type predicate in
argument to filter
```
### 5. Pass Functions as Behavior
*Principle: Parameterize the part of an algorithm that varies instead of duplicating its iteration and control structure..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Using functions as objects", "Passing functions to functions", "In-line function definitions", "Anonymous functions"*

**Do:** Pass named functions for reusable behavior.; Use inline functions when a local name helps comprehension.; Use anonymous functions for short one-off behavior..

**Don't:** Don't hard-code a single predicate into a reusable traversal.; Don't create an anonymous function so large that it conceals the calling algorithm..

```
package main
import "fmt"
type predicate func(int) bool
func main() {
    is := []int{1, 1, 2, 3, 5, 8, 13}
    larger := filter(is, largerThan5)
    fmt.Printf("%v", larger)
}
func filter(is []int, condition predicate) []int {
    out := []int{}
    for _, i := range is {
        if condition(i) {
            out = append(out, i)
        }
    }
    return out
}
func largerThan5(i int) bool {
    return i > 5
}

type predicate func(int) bool
func largerThanTwo(i int) bool {
    return i > 2
}
func filter(is []int, p predicate) []int {
    out := []int{}
    for _, i := range is {
 if p(i) {
 out = append(out, i)
 }
    }
    return out
}
func main() {
    ints := []int{1, 2, 3}
filter(ints, largerThanTwo)
}

func main() {
    // functions in variables
    inlinePersonStruct := struct {
 name string
    }{
 name: "John",
    }
    ints := []int{1, 2, 3}
    inlineFunction := func(i int) bool { return i > 2 }
    filter(ints, inlineFunction)
}

func main() {
    filter([]int{1, 2, 3}, func(i int) bool { return i > 2 })
}
```
### 6. Return Specialized Functions
*Principle: Build reusable behavior factories by returning closures that capture configuration..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Returning functions from functions", "Functions in var"*

**Do:** Return a typed function whose captured input is fixed.; Bind frequently used specializations in a package `var` block when appropriate.; Keep runtime-created functions out of `const` declarations..

**Don't:** Don't confuse creating a function with executing it.; Don't hide mutable shared package state in a returned closure..

```go
func createLargerThanPredicate(threshold int) predicate {
    return func(i int) bool {
 return i > threshold
    }
}

func main() {
    ints := []int{1, 2, 3}
    largerThanTwo := createLargerThanPredicate(2)
    filter(ints, largerThanTwo)
}

 func main() {
    largerThanTwo := createLargerThanPredicate(2)
    largerThanFive := createLargerThanPredicate(5)
    largerThanHundred := createLargerThanPredicate(100)
}

var (
    largerThanTwo = createLargerThanPredicate(2)
    largerThanFive = createLargerThanPredicate(5)
    largerThanHundred = createLargerThanPredicate(100)
)

const (
    largerThanTwo = createLargerThanPredicate(2)
    largerThanFive = createLargerThanPredicate(5)
    largerThanHundred = createLargerThanPredicate(100)
)
```

```text
./prog.go:8:23: createLargerThanPredicate(2) (value of type
predicate) is not constant

./prog.go:9:23: createLargerThanPredicate(5) (value of type
predicate) is not constant
./prog.go:10:23: createLargerThanHundred(100) (value of type
predicate) is not constant
```
### 7. Store Functions in Collections
*Principle: Use slices for ordered behavior sequences and maps for key-based behavior dispatch..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Functions inside data structures"*

**Do:** Iterate over a slice of functions like any other slice.; Resolve behavior from a map when keys naturally select operations.; Validate missing keys before invocation..

**Don't:** Don't use a function map when a short switch is clearer and closed to extension.; Don't expose a mutable dispatcher without ownership discipline..

```go
var (
    largerThanTwo = createLargerThanPredicate(2)
    largerThanFive = createLargerThanPredicate(5)
    largerThanHundred = createLargerThanPredicate(100)
)
func main() {
    ints := []int{1, 2, 3, 6, 101}
    predicates := []predicate{largerThanTwo, largerThanFive,
 largerThanHundred}
    for _, predicate := range predicates {
 fmt.Printf("%v\n", filter(ints, predicate))
    }
}
```

```text
[3 6 101]
[6 101]
[101]
```

```go
func main() {
    ints := []int{1, 2, 3, 6, 101}
    dispatcher := map[string]predicate{
 "2": largerThanTwo,
 "5": largerThanFive,
    }
    fmt.Printf("%v\n", filter(ints, dispatcher["2"]))
}
```
### 8. Store Swappable Functions in Structs
*Principle: Put behavior in function fields when callers must choose or replace the implementation at construction or runtime..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Functions inside structs", "Example 2 – mocking functions for testing"*

**Do:** Give each function field a named type.; Delegate through a stable method when shared logging or metrics may be added.; Inject a trivial function in unit tests..

**Don't:** Don't bind behavior as a method when the implementation genuinely belongs to the caller.; Don't let production tests depend on command-line arguments, databases, or external state..

```
type ConstraintChecker struct {
    largerThan predicate
    smallerThan predicate
}

func (c ConstraintChecker) check(input int) bool {
    return c.largerThan(input) && c.smallerThan(input)
}

func main() {
    checker := ConstraintChecker{
 largerThan: createLargerThanPredicate(2),
 smallerThan: func(i int) bool { return i < 10 },
    }
    fmt.Printf("%v\n", checker.check(5))
}

type Todo struct {
   Text string
   Db *Db
}
func NewTodo() Todo {
   return Todo{
 Text: "",
 Db: NewDB(),
   }
}

func (t *Todo) Write(s string){
    if t.Db.IsAuthorized() {
 t.Text = s
    } else {
 panic("user not authorized to write")
    }
}
func (t *Todo) Append(s string) {
    if t.Db.IsAuthorized() {
 t.Text += s
   } else {
 panic("user not authorized to append")
   }
}

type authorizationFunc func() bool
type Db struct {
    AuthorizationFn authorizationFunc
}

func argsAuthorization() bool {
    user := os.Args[1]
    // super secure authorization layer
    // in a real application, this would be a database call
    if user == "admin" {
 return true
    }
    return false
}

func NewDB() *Db {
    return &Db{
 AuthorizationFn: argsAuthorization,
   }
}

func (d *Db) IsAuthorized() bool {
    return d.AuthorizationFn()
}

func TestTodoWrite(t *testing.T) {
    todo := pkg.Todo{
 Db: &pkg.Db{
 AuthorizationF: func() bool { return true },
 },
    }
    todo.Write("hello")
    if todo.Text != "hello" {
 t.Errorf("Expected 'hello' but got %v\n", todo.Text)
    }
    todo.Append(" world")
    if todo.Text != "hello world" {
 t.Errorf("Expected 'hello world' but got %v\n",
 todo.Text)
   }
}
```
### 9. Replace Extensible Switches with Map Dispatchers
*Principle: Map keys to typed operations when adding behavior should be a data change rather than a control-flow edit..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example 1 – map dispatcher", "Creating a simple calculator"*

**Do:** Define one function type for every operation.; Check map membership before calling.; Use anonymous functions for concise one-off operations..

**Don't:** Don't preserve a growing switch when all branches share a signature.; Don't panic on unsupported production input without deliberate policy..

```
func add(a, b int) int {
    return a + b
}
func sub(a, b int) int {
    return a - b
}
func mult(a, b int) int {
    return a + b
}
func div(a, b int) int {
    if b == 0 {
 panic("divide by zero")
    }
    return a / b
}

func calculate(a, b int, operation string) int {
    switch operation {
case "+":
 return add(a, b)
   case "-":
 return sub(a, b)
   case "*":
 return mult(a, b)
   case "/":
 return div(a, b)
   default:
 panic("operation not supported")
   }
}

type calculateFunc func(int, int) int

var (
   operations = map[string]calculateFunc{
 "+": add,
 "-": sub,
 "*": mult,
 "/": div,
   }
)

func calculateWithMap(a, b int, opString string) int {
    if operation, ok := operations[opString]; ok {
 return operation(a, b)
    }
    panic("operation not supported")
}

var (
   operations = map[string]calculateFunc{
 "+": add,
 "-": sub,
 "*": mult,
 "/": div,
 "<<": func(a, b int) int { return a << b },
 ">>": func(a, b int) int { return a >> b },
    }
)
```
### 10. Recognize Higher-Order Functions
*Principle: A function is higher-order when it takes behavior as input, returns behavior as output, or both..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "An introduction to higher-order functions"*

**Do:** Use higher-order functions to abstract predicates, transformations, continuations, and construction options.; Distinguish passing a function from passing its already computed result..

**Don't:** Don't add layers of function passing when no behavior varies..

```
func A() string {
 return "hello"
}
func B(a A) string {
 return A() + " world"
}
```
### 11. Use Lexical Scope Deliberately
*Principle: Understand capture, shadowing, and reassignment before building closures..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Closures and variable scoping", "Variable scoping in Go"*

**Do:** Use `:=` to declare in the current scope and `=` to reassign an existing variable.; Expect inner blocks to access outer values.; Declare a recursive function variable before assigning its closure..

**Don't:** Don't mistake shadowing for updating an outer variable.; Don't reference a variable outside the block where it was declared..

```go
package main
import "fmt"
// location 1
func main() {
 // location 2
 b := true
 if b {
 // location 3
 fmt.Println(b)
 }
}

 func main() {
 {
 b := true
 }
 if b {
 fmt.Println("b is true")
 }
}

func main() {
 s := "hello"
 if true {
 s := "world"
 fmt.Println(s)
 }
 fmt.Println(s)
}

func main() {
 s := "hello"
 if true {
 s = "world"
 fmt.Println(s)
 }
 fmt.Println(s)
}
```

```text
world hello

world world
```

```go
S := world

S = world
```

```go
func main() {
 s := "hello"
 s := "world"
 fmt.Println(s)
}

func main() {
 str1, err := func1()
 if err != nil {
 panic(err)
 }
 str2, err := func2()
 if err != nil {
 panic(err)
 }
 fmt.Printf("%v %v\n", str1, str2)
}
func func1() (string, error) {
 return "", errors.New("error 1")
}
func func2() (string, error) {
 return "", errors.New("error 2")
}
```
### 12. Capture Context with Closures
*Principle: Use an inner function to retain immutable configuration from its lexical environment after the outer call returns..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Capturing variable context in functions (closures)"*

**Do:** Capture configuration that belongs to the generated behavior.; Keep captured state private.; Prefer immutable capture when functions may run concurrently..

**Don't:** Don't use closure capture as disguised mutable global state.; Don't assume the captured variable disappears when the outer function returns..

```
// location 1
func outerFunction() func() {
 // location 2
 fmt.Println("outer function")
 return func() {
 // location 3
 fmt.Println("inner function")
 }
}

func main() {
 greetingFunc := createGreeting()
 response := greetingFunc("Ana")
 fmt.Println(response)
}
func createGreeting() func(string) string {
 s := "Hello "
 return func(name string) string {
 return s + name
 }
}

func createGreeting(greeting string) func(string) string {..}
```
### 13. Use Partial Application to Fix Inputs
*Principle: Bind the first N arguments of a function and return a unary function that fills in the rest..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Partial application", "Example: DogSpawner"*

**Do:** Use partial application to derive specialized spawners or factories.; Lift repeated argument lists into a stored function.; Keep the result typed so the call site stays short..

**Don't:** Don't partially apply a function whose remaining argument list is not used in a single call site.; Don't partially apply a function whose arguments are all dynamic..

```go
func createGreeting(greeting string) func(string) string {
    return func(name string) string {
 return greeting + name
    }
}

func main() {
 firstGreeting := createGreeting("Well, hello there ")
 secondGreeting := createGreeting("Hola ")
 fmt.Println(firstGreeting("Remi"))
 fmt.Println(firstGreeting("Sean"))
 fmt.Println(secondGreeting("Ana"))
}
```

```text
Well, hello there Remi
Well, hello there Sean
Hola Ana
```

```go
type (
 Name string
 Breed int
 Gender int
 NameToDogFunc func(Name) Dog
)
// define possible breeds
const (
 Bulldog Breed = iota
 Havanese
 Cavalier
 Poodle
)
// define possible genders
const (
 Male Gender = iota
 Female
)

type Dog struct {
 Name Name
 Breed Breed
 Gender Gender
}

func createDogsWithoutPartialApplication() {
 bucky := Dog{
 Name: "Bucky",
 Breed: Havanese,
 Gender: Male,
 }
 rocky := Dog{
 Name: "Rocky",
 Breed: Havanese,
 Gender: Male,
 }
 tipsy := Dog{
 Name: "Tipsy",
 Breed: Poodle,
 Gender: Female,
 }
}

func DogSpawner(breed Breed, gender Gender) NameToDogFunc {
 return func(n Name) Dog {
 return Dog {
 Breed: breed,
 Gender: gender,
 Name: n,
 }
 }
}

var (
 maleHavaneseSpawner = DogSpawner(Havanese, Male)
 femalePoodleSpawner = DogSpawner(Poodle, Female)
)

func main() {
 bucky := maleHavaneseSpawner("bucky")
 rocky := maleHavaneseSpawner("rocky")
 tipsy := femalePoodleSpawner("tipsy")
 fmt.Printf("%v\n", bucky)
 fmt.Printf("%v\n", rocky)
 fmt.Printf("%v\n", tipsy)
}
```
### 14. Curry Only to Fit a Higher-Order Signature
*Principle: Currying reduces arity one argument at a time; use it when a unary function must compose inside a typed `Node[A]`..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Function currying, or how to reduce n-ary functions to unary functions", "Example: function currying"*

**Do:** Curry only to match a required function signature.; Document the call order in the type signature.; Let the language's generics do the heavy lifting..

**Don't:** Don't curry a 2-argument function `f(a, b)` into `f(a)(b)` for no benefit.; Don't forget that Go does not auto-curry or apply partial application..

```
func threeSum(a, b, c int) int {
 return a + b + c
}

func threeSumCurried(a int) func(int) func(int) int {
 return func(b int) func(int) int {
 return func(c int) int {
 return a + b + c
 }
 }
}

func main() {
 fmt.Println(threeSum(10, 20, 30))
 fmt.Println(threeSumCurried(10)(20)(30))
}

func DogSpawner(breed Breed) func(Gender) NameToDogFunc {
 return func(gender Gender) NameToDogFunc {
 return func(name Name) Dog {
 return Dog{
 Breed: breed,
                 Gender: gender,
 Name: name,
 }
 }
 }
}
```
### 15. Build Flexible Constructors with Function Options
*Principle: Encapsulate option application behind higher-order functions that each adjust one field..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example: server constructor"*

**Do:** Define a typed `ServerOptions` returning a function that mutates an options struct.; Provide sensible defaults in the constructor.; Allow the user to compose options by passing them as variadic arguments..

**Don't:** Don't mutate the struct through public setters.; Don't accept a constructor with many positional arguments that are easy to swap..

```go
type (
 ServerOptions func(options) options
 TransportType int
)
const (
 UDP TransportType = iota
 TCP
)

type Server struct {
 options
}
type options struct {
 MaxConnection int
 TransportType TransportType
 Name string
}

func MaxConnection(n int) ServerOptions {
 return func(o options) options {
 o.MaxConnection = n
 return o
 }
}
func ServerName(n string) ServerOptions {
 return func(o options) options {
 o.Name = n
 return o
 }
}
func Transport(t TransportType) ServerOptions {
 return func(o options) options {
 o.TransportType = t
 return o
 }
}

func NewServer(os .ServerOptions) Server {
 opts := options{
 TransportType: TCP,
 }
 for _, option := range os {
 opts = option(opts)
 }
 return Server{
 options: opts,
 isAlive: true,
 }
}

func main() {
 server := NewServer(MaxConnection(10),
 ServerName("MyFirstServer"))
 fmt.Printf("%+v\n", server)
}
```

```text
{options:{MaxConnection:10 TransportType:0 Name:MyFirstServer}
 isAlive:true}

{options:{MaxConnection:10 TransportType:1 Name:MyFirstServer}
 isAlive:true}
```
### 16. Strive for Purity, Accept I/O at the Edges
*Principle: Aim for ~90% pure code with ~10% impure code at the boundaries..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Demonstrating pure versus impure function calls", "Referential transparency", "Why does purity improve our code?", "When not to write pure functions", "How do we create pure functions?"*

**Do:** Make functions depend only on their arguments and return new values.; Bubble errors up via `(T, error)` rather than panicking on the happy path.; Isolate persistence and randomness in thin shells.; Each function should do one thing; if you can split a function, do it..

**Don't:** Don't use `panic` for control flow.; Don't rely on package-level `var` blocks for state a function depends on.; Don't mix validation, persistence, and logging in one function..

```go
func add(a, b int) int {
    return a + b
}

func rollDice() int {
    return rand.Intn(6)
}

func main() {
    for i := 0; i < 5; i++ {
 fmt.Printf("dice roll: %v\n", rollDice())
    }
}
```

```text
dice roll: 5
dice roll: 3
dice roll: 5
dice roll: 5
dice roll: 1
```

```go
X = 1 + (2 * 2)

X = (1 + 4)
```

```go
func main() {
    fmt.Printf("%v\n", add(10, add(10, 5)))
    fmt.Printf("%v\n", add(10, 15))
}
func add(a, b int) int {
return a + b
}

func main() {
    fmt.Printf("%v\n", time.Now())
}
```

```go
type Player string
const (
    PlayerOne Player = "Remi"
    PlayerTwo Player = "Yvonne"
)
func selectStartingPlayer() Player {
    randomized := rand.Intn(2)
    switch randomized {
    case 0:
 return PlayerOne
    case 1:
 return PlayerTwo
    }
    panic("No further player available")
}

func PlayerSelectPure(i int) (Player, error) {
    switch i {
    case 0:
 return PlayerOne, nil
    case 1:
 return PlayerTwo, nil
    }
    return Player(""), fmt.Errorf("no player matching input:
 %v", i)
}
```

```text
PlayerSelectPure(0) = PlayerOne, nil
PlayerSelectPure(1) = PlayerTwo, nil
PlayerSelectPure(n > 1) = Player{}, error
```

```go
func TestPlayerSelectionPure(t *testing.T) {
    selectPlayerOne, err := PlayerSelectPure(0)
    if selectPlayerOne != PlayerOne || err != nil {
 t.Errorf("expected %v but got %v\n", PlayerOne,
 selectPlayerOne)
    }
    selectPlayerTwo, err := PlayerSelectPure(1)
    if selectPlayerTwo != PlayerTwo || err != nil {
 t.Errorf("expected %v but got %v\n", PlayerOne,
 selectPlayerTwo)
    }
    _, err = PlayerSelectPure(2)
    if err == nil {
 t.Error("Expected error but received nil")
    }
}

func main() {
    random := rand.Intn(2)
player.PlayerSelectPure(random)
    // start the game
}

var (
    name = "Remi"
)

func sayHello() string {
    return fmt.Sprintf("hello %s", name)
}
func main() {
    sayHello()
}
```

```go
func sayHello(name string) string {
    return fmt.Sprintf("hello %s", name)
}
func main() {
    sayHello("Remi")
}

 func add(a, b int) int {
    sum := a + b
    fmt.Println(sum)
    return sum
}
```

```go
func createUser(username, password string) {
    u := User{username, password}
    if u.validPassword() {
 userDb.save(u)
    } else {
 panic("invalid password")
    }
}

func signup(username, password string) {
    user, err := createUser(username, password)
    if err != nil {
 saveUser(user)
    } else {
 Panic("Could not create account")
    }
}
func createUser(username, password string) (User, error) {
    u := User{username, password}
    if u.validPassword() {
 return u, nil
    }
    return User{}, Errors.new("invalid password")
}
func saveUser(u User) {
    userDb.save(u)
}
```
### 17. Refactor the Hotdog Shop to Be Testable
*Principle: Move pricing, charging, and side effects out of a single function so each layer is independently testable..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example 1 – hotdog shop", "Bad hotdog shop", "Better hotdog shop"*

**Do:** Replace pointer mutation with value-returning charges.; Return errors rather than panicking for insufficient credit.; Defer the actual side effect to a returned closure.; Inject a mock `PaymentFunc` for unit tests..

**Don't:** Don't mutate a credit card in place to model a charge.; Don't panic on insufficient funds in production code.; Don't hide side effects behind a higher-level API that tests cannot observe..

```
const (
     HOTDOG_PRICE = 4
)

type CreditCard struct {
    credit int
}
type Hotdog struct{}

func (c *CreditCard) charge(amount int) {
    if amount <= c.credit {
 c.credit -= amount
    } else {
 panic("no more credit")
    }
}

func orderHotdog(c *CreditCard) Hotdog {
    c.charge(HOTDOG_PRICE)
    return Hotdog{}
}

type CreditCard struct {
    credit int
}
type Hotdog struct {
    price int
}
type CreditError error
type PaymentFunc func(CreditCard, int) (CreditCard,
 CreditError)

func NewCreditCard(initialCredit int) CreditCard {
    return CreditCard{credit: initialCredit}
}
func NewHotdog() Hotdog {
    return Hotdog{price: 4}
}

var (
    NOT_ENOUGH_CREDIT CreditError = CreditError(errors.
 New("not enough credit"))
)

func Charge(c CreditCard, amount int) (CreditCard, CreditError)
{
    if amount <= c.credit {
 c.credit -= amount
 return c, nil
    }
    return c, NOT_ENOUGH_CREDIT
}

var (
  testChargeStruct = []struct {
 inputCard CreditCard
 amount int
 outputCard CreditCard
 err CreditError
  }{
 {
 CreditCard{1000},
 500,
 CreditCard{500},
 nil,
 },
 {
 CreditCard{20},
 20,
 CreditCard{0},
 nil,
 },
 {
 CreditCard{150},
 1000,
 CreditCard{150}, // no money is withdrawn
 NOT_ENOUGH_CREDIT,
 // payment fails with this error
 },
  }
)

func TestCharge(t *testing.T) {
   for _, test := range testChargeStruct {
 t.Run("", func(t *testing.T) {
 output, err := Charge(test.inputCard, test.
 amount)
 if output != test.outputCard || !errors.
 Is(err, test.err) {
 t.Errorf("expected %v but got %v\n,
 error expected %v but got %v",
 test.outputCard, output, test.err, err)
 }
 })
}
}

func OrderHotdog(c CreditCard, pay PaymentFunc) (Hotdog, func()
 (CreditCard, error)) {
    hotdog := NewHotdog()
    chargeFunc := func() (CreditCard, error) {
 return pay(c, hotdog.price)
    }
    return hotdog, chargeFunc
}

func main() {
    myCard := NewCreditCard(1000)
hotdog, creditFunc := OrderHotdog(myCard, Charge)
    fmt.Printf("%+v\n", hotdog)
    newCard, err := creditFunc()
    if err != nil {
 panic("User has no credit")
    }
    myCard = newCard
    fmt.Printf("%+v\n", myCard)
}

func TestOrderHotdog(t *testing.T) {
    testCC := CreditCard{1000}
    calledInnerFunction := false
    mockPayment := func(c CreditCard, input int) (CreditCard,
 CreditError) {
 calledInnerFunction = true
 testCC.credit -= input
 return testCC, nil
    }
    hotdog, resultF := OrderHotdog(testCC, mockPayment)
    if hotdog != NewHotdog() {
 t.Errorf("expected %v but got %v\n", NewHotdog(),
 hotdog)
   }
   _, err := resultF()
   if err != nil {
 t.Errorf("encountered %v but expected no error\n",
 err)
   }
   if calledInnerFunction == false {
 t.Errorf("Inner function did not get called\n")
   }
}
```
### 18. Use Value Semantics for Immutability
*Principle: Go is value-oriented; prefer pass-by-value and returned copies to avoid hidden mutation..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "What is immutability?", "How to write immutable code in Go", "Writing immutable code for collection data types"*

**Do:** Accept a struct by value and return a new struct with the change applied.; Treat `append` as a value operation: assign the returned slice.; Reuse buffers with `buf = buf[:0]` rather than re-allocating..

**Don't:** Don't reach for pointers "for performance" without measuring.; Don't treat map values as pass-by-value: maps always act as pass-by-reference.; Don't assume `s = append(s, x)` mutates the caller's slice..

```go
type Person struct {
    Age  int
    Name string
}

func changeName(p *Person, newName string) {
    p.Name = newName
}

func changeNamePure(p Person, newName string) Person {
    return Person{
        Age:  p.Age,
        Name: newName,
    }
}
```

```go
type Person struct {
 name string
 age int
}
func main() {
 p := Person{
 name: "Benny",
 age: 55,
 }
 setName(p, "Bjorn")
 fmt.Println(p.name)
}
func setName(p Person, name string) {
 p.name = name
}
```

```text
Benny
```

```go
func main() {
 p := Person{
 name: "Benny",
 age: 55,
 }
 setName(&p, "Bjorn")
 fmt.Println(p.name)
}
func setName(p *Person, name string) {
 p.name = name
}
```

```text
Bjorn
```

```go
func main() {
 p := Person{
 name: "Benny",
 age: 55,
 }
 p = setName(p, "Bjorn")
 fmt.Println(p.name)
}
func setName(p Person, name string) Person {
 p.name = name
 return p
}

func main() {
 names := []string{"Miranda", "Paula"}
 names = append(names, "Yvonne")
 fmt.Printf("%v\n", names)
}
```

```text
[Miranda Paula Yvonne]
```

```go
func main() {
 m := map[string]int{}
 addValue(m, "red", 10)
 fmt.Printf("%v\n", m)
}
func addValue(m map[string]int, colour string, value int) {
 m[colour] = value
}
```

```text
[red 10]
```

```go
func main() {
 names := []string{"Miranda"}
 addValue(names, "Yvonne")
 fmt.Printf("%v\n", names)
}
func addValue(s []string, name string) {
 s = append(s, name)
}
```

```text
Miranda
```

```go
func main() {
 names := []string{"Miranda"}
 addValue(&names, "Yvonne")
 fmt.Printf("%v\n", names)
}
func addValue(s *[]string, name string) {
 *s = append(*s, name)
}
```

```text
[Miranda Yvonne]
```
### 19. Benchmark "Pointers Are Faster" Claims
*Principle: Immutable value-based code can win because the compiler keeps it on the stack..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Measuring performance in mutable and immutable code", "Benchmarking functions", "Understanding stacks, heaps, and garbage collection", "Seeing escape analysis in action"*

**Do:** Write paired benchmarks for the immutable and mutable versions.; Use `b.ReportAllocs()` to expose allocation differences.; Inspect escape analysis with `go build -gcflags '-m -l'`.; Be willing to update your mental model when data contradicts it..

**Don't:** Don't use pointers for performance without measuring.; Don't use a global variable to track state inside recursion.; Don't assume the immutable version is slower; check..

```go
func immutableCreatePerson() Person {
 p := Person{}
 p = immutableSetName(p, "Sean")
 p = immutableSetAge(p, 29)
 return p
}

func immutableSetName(p Person, name string) Person {
 p.name = name
 return p
}
func immutableSetAge(p Person, age int) Person {
 p.age = age
 return p
}

func mutableCreatePerson() *Person {
 p := &Person{}
 mutableSetName(p, "Tom")
 mutableSetAge(p, 31)
 return p
}
func mutableSetName(p *Person, name string) {
 p.name = name
}
func mutableSetAge(p *Person, age int) {
 p.age = age
}

package pkg
import "testing"
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

```go
//go:noinline
func immutableCreatePerson() Person {
 p := Person{}
 p = immutableSetName(p, "Sean")
 p = immutableSetAge(p, 29)
 return p
}
```

```text
go build -gcflags '-m -l'

# github.com/PacktPublishing/Chapter5/Benchmark/pkg
./person.go:17:23: leaking param: p to result ~r0 level=0
./person.go:17:33: leaking param: name to result ~r0
 level=0
./person.go:23:22: leaking param: p to result ~r0 level=0
./person.go:37:21: p does not escape
./person.go:37:32: leaking param: name
./person.go:42:20: p does not escape
./person.go:30:7: &Person{} escapes to heap
```
### 20. Use Functors and Maybe/Option Monads for Absence
*Principle: Encode "value may be absent" in the type system to avoid nil dereferences..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "What are functors and monads?", "What's a functor?", "From functor to monad"*

**Do:** Define a `Maybe[A]` interface with `Get()` and `GetOrElse(def A) A`.; Provide `Just(a)` and `Nothing[A]()` constructors.; Implement `fmap` for `Maybe[A]` to compose transformations.; Use `GetOrElse(default)` instead of `if x != nil { x.foo() }`..

**Don't:** Don't return `(T, error)` for the "not found" case; use `Maybe[T]`.; Don't reach for `*T` pointers when absence is part of the domain.; Don't panic on `Get()` from `Nothing`; that defeats the purpose..

```go
func fmap[A, B any](mapFunc func(A) B, sliceA []A) []B {
 sliceB := make([]B, len(sliceA))
 for i, a := range sliceA {
 sliceB[i] = mapFunc(a)
 }
 return sliceB
}

import (
 "fmt"
 "strconv"
)
func main() {
 integers := []int{1, 2, 3}
 strings := fmap(strconv.Itoa, integers)
 fmt.Printf("%T transformed to %T - %v\n", integers,
 strings, strings)
}
```

```text
[]int transformed to []string - [1 2 3]
```

```go
type Maybe[A any] interface {
 Get() (A)
 GetOrElse(def A) A
}

type JustMaybe[A any] struct {
 value A
}
func (j JustMaybe[A]) Get() (A) {
 return j.value
}
func (j JustMaybe[A]) GetOrElse(def A) A {
 return j.value
}

type NothingMaybe[A any] struct{}
func Nothing[A any]() Maybe[A] {
 return NothingMaybe[A]{}
}
func (n NothingMaybe[A]) Get() (A) {
 return *new(A)
}
func (n NothingMaybe[A]) GetOrElse(def A) A {
 return def
}

func Just[A any](a A) JustMaybe[A] {
 return JustMaybe[A]{value: a}
}
func Nothing[A any]() Maybe[A] {
 return NothingMaybe[A]{}
}
```

```go
func getFromMap(m map[string]int, key string) Maybe[int] {
 if value, ok := m[key]; ok {
 return Just[int](value)
 } else {
 return Nothing[int]()
 }
}

func fmap[A, B any](m Maybe[A], mapFunc func(A) B) Maybe[B]
{
 switch m.(type) {
 case JustMaybe[A]:
 j := m.(JustMaybe[A])
 return JustMaybe[B]{
 value: mapFunc(j.value),
 }
 case NothingMaybe[A]:
 return NothingMaybe[B]{}
 default:
 panic("unknown type")
 }
}
```
### 21. Build a Generic Map/Filter/Reduce Toolbox
*Principle: Cover most collection work with a small generic toolbox..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Three Common Categories of Functions", "Predicate-based functions", "Implementing a Filter function", "Any or all", "Implementing DropWhile and TakeWhile", "Map/transformation functions", "Data reducing functions"*

**Do:** Use `Predicate[A any] = func(A) bool` and `MapFunc[A any] = func(A) A`.; Pre-allocate output slices with `make([]A, 0, len(input))`.; Short-circuit `Any` on the first match.; Provide a custom `Number` type constraint for arithmetic.; Use `ReduceWithStart` to start from a default value..

**Don't:** Don't write collection-specific `onlyInts` / `onlyStrings`; generics cover all of them.; Don't use `All` if a short-circuit is possible.; Don't use `Sum` on non-numeric types without a type constraint..

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
        if pred(element) { return true }
    }
    return false
}

func Map[A any](input []A, m MapFunc[A]) []A {
    output := make([]A, len(input))
    for i, element := range input {
 output[i] = m(element)
    }
    return output
}
```

```go
func FlatMap[A any](input []A, m func(A) []A) []A {
    output := []A{}
    for _, element := range input {
 newElements := m(element)
 output = append(output, newElements…)
    }
    return output
}

func main() {
 ints := []int{1, 2, 3}
 result := FlatMap(ints, func(n int) []int {
 out := []int{}
 for i := 0; i < n; i++ {
 out = append(out, i)
 }
 return out
 })
 fmt.Printf("%v\n", result)
}
```

```text
[0 0 1 0 1 2]

0: [0]
1: [0 1]
2: [0 1 2]
```

```go
type (
 reduceFunc[A any] func(a1, a2 A) A
)

func Reduce[A any](input []A, reducer reduceFunc[A]) A {
    if len(input) == 0 {
 // return default zero
 return *new(A)
    }
    result := input[0]
    for _, element := range input[1:] {
 result = reducer(result, element)
    }
    return result
}

type Number interface {
 ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uint |
 ~int8 | ~int16 | ~int32 | ~int64 | ~int |
 ~float32 | ~float64
}
```

```go
func Sum[A Number](input []A) A {
    return Reduce(input, func(a1, a2 A) A { return a1 + a2 })
}

func main() {
 ints := []int{1, 2, 3, 4}
 result := Sum(ints)
 fmt.Printf("%v\n", result)
}
```

```text
10
```

```go
func Product[A Number](input []A) A {
 return Reduce(input, func(a1, a2 A) A { return a1 * a2
 })
}

func ReduceWithStart[A any](input []A, startValue A, reducer
 reduceFunc[A]) A {
 if len(input) == 0 {
 return startValue
 }
 if len(input) == 1 {
 return reducer(startValue, input[0])
 }
 result := reducer(startValue, input[0])
 for _, element := range input[1:] {
 result = reducer(result, element)
 }
 return result
}
```

```go
func main() {
 words := []string{"hello", "world", "universe"}
 result := ReduceWithStart(words, "first", func(s1, s2
 string) string {
 return s1 + ", " + s2
 })
 fmt.Printf("%v\n", result)
}
```

```text
first, hello, world, universe
```
### 22. Compose the Airport Data Example
*Principle: Demonstrate that Filter + FMap + Sum is enough to express most analytical queries..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example – working with airport data"*

**Do:** Decode JSON into tagged structs.; Chain Filter, FMap, and Sum in one main flow.; Document the data shape in a struct comment..

**Don't:** Don't loop-and-append when pre-allocation matters.; Don't mix pointer mutation with the chain..

```
type Entry struct {
   Airport struct {
 Code string `json:"Code"`
 Name string `json:"Name"`
   } `json:"Airport"`
   Statistics struct {
 Flights struct {
 Cancelled int `json:"Cancelled"`
 Delayed int `json:"Delayed"`
 OnTime int `json:"On Time"`
 Total int `json:"Total"`
 } `json:"Flights"`
 MinutesDelayed struct {
 Carrier int `json:"Carrier"`
 LateAircraft int `json:"Late
 Aircraft"`
 Security int `json:"Security"`
 Weather int `json:"Weather"`
 } `json:"Minutes Delayed"`
   } `json:"Statistics"`
}

func getEntries() []Entry {
 bytes, err := ioutil.ReadFile("./resources/airlines.
 json")
 if err != nil {
 panic(err)
 }
 var entries []Entry
 err = json.Unmarshal(bytes, &entries)
 if err != nil {
 panic(err)
 }
 return entries
}

func main() {
    entries := getEntries()
    SEA := Filter(entries, func(e Entry) bool {
 return e.Airport.Code == "SEA"
    })
    WeatherDelayHours := FMap(SEA, func(e Entry) int {
 return e.Statistics.MinutesDelayed.Weather / 60
    })
    totalWeatherDelay := Sum(WeatherDelayHours)
    fmt.Printf("%v\n", totalWeatherDelay)
}
```
### 23. Recurse When the Data Is Tree-Shaped
*Principle: Recursion shines on recursive data; iteration wins on large linear input..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Iterating over trees", "Recursion and functions as first-class citizens", "Limits of recursive functions"*

**Do:** Use recursion for trees and graphs where the natural shape is recursive.; Encapsulate state in a non-recursive outer function and a recursive inner function.; Always have a base case.; Use `debug.SetMaxStack` only as a last resort on 32-bit hosts..

**Don't:** Don't recurse over lists of millions of items.; Don't rely on Go tail-call optimization.; Don't use a package-level global to track state inside recursion.; Don't write `inner := func(.) { inner(.) }`; declare `var inner func(.)` first..

```go
type node struct {
 value int
 left *node
 right *node
}

var (
 ExampleTree = &node{
 value: 1,
 left: &node{
 value: 2,
         left: &node{
 value: 3,
 },
         right: &node{
 value: 4,
 },
 },
 right: &node{
 value: 5,
 },
 }
)
```

```go
func sumIterative(root *node) int {
 queue := make(chan *node, 10)
 queue <- root
 var sum int
 for {
 select {
 case node := <-queue:
 sum += node.value
             if node.left != nil {
 queue <- node.left
 }
             if node.right != nil {
 queue <- node.right
 }
 default:
 return sum
 }
 }
}

func sumRecursive(node *node) int {
 if node == nil {
 return 0
 }
 return node.value + sumRecursive(node.left) +
 sumRecursive(node.right)
}

var maximum = 0
func MaxGlobalVariable(node *node) {
 if node == nil {
 return
 }
 if node.value > maximum {
 maximum = node.value
 }
 MaxGlobalVariable(node.left)
 MaxGlobalVariable(node.right)
}
func main() {
 maximum = int(math.MinInt)
 MaxGlobalVariable(ExampleTree)
 fmt.Println(maximum)
}
```

```go
func.maxInline(node *node,
 maxValue int) int {
 if node == nil {
 return maxValue
 }
 if node.value > maxValue {
 maxValue = node.value
 }
 maxLeft := maxInline(node.left, maxValue)
 maxRight := maxInline(node.right, maxValue)
 if maxLeft > maxRight {
 return maxLeft
 }
 return maxRight
}

func main() {
 fmt.Println(maxInline(ExampleTree, 0))
}
func MaxInline(root *node) int {
 return maxInline(root, 0)
}
func maxInline(node *node, maxValue int) int {
 if node == nil {
 return maxValue
 }
 if node.value > maxValue {
 maxValue = node.value
 }
 maxLeft := maxInline(node.left, maxValue)
 maxRight := maxInline(node.right, maxValue)
 if maxLeft > maxRight {
 return maxLeft
 }
 return maxRight
}
```

```go
func Max(root *node) int {
 currentMax := math.MinInt
 var inner func(node *node)
 inner = func(node *node) {
 if node == nil {
 return
 }
 if node.value > currentMax {
 currentMax = node.value
 }
 inner(node.left)
 inner(node.right)
 }
 inner(root)
 return currentMax
}

var inner func(node *node)
inner = func(node *node) {
 if node == nil {
 return
 }
 if node.value > currentMax {
 currentMax = node.value
 }
 inner(node.left)
 inner(node.right)
}
```

```go
inner := func(node *node) {
 if node == nil {
 return
 }
 if node.value > currentMax {
 currentMax = node.value
 }
 inner(node.left)
 inner(node.right)
}

func main() {
 infiniteCount(0)
}
func infiniteCount(i int) {
 if i%1000 == 0 {
 fmt.Println(i)
 }
 infiniteCount(i + 1)
}
```

```go
func main() {
 debug.SetMaxStack(262144000 * 2)
 infiniteCount(0)
}
func infiniteCount(i int) {
 if i%1000 == 0 {
 fmt.Println(i)
 }
 infiniteCount(i + 1)
}
```

```text
1861000
1862000
1863000
1864000
runtime: goroutine stack exceeds 262144000-byte limit
runtime: sp=0xc008080380 stack=[0xc008080000, 0xc010080000]
fatal error: stack overflow
runtime stack:
runtime.throw({0x496535?, 0x50e900?})
 /usr/lib/golang/src/runtime/panic.go:992 +0x71
runtime.newstack()
 /usr/lib/golang/src/runtime/stack.go:1101 +0x5cc
runtime.morestack()
 /usr/lib/golang/src/runtime/asm_amd64.s:547 +0x8b

3724000
3725000
3726000
3727000
3728000
runtime: goroutine stack exceeds 524288000-byte limit
runtime: sp=0xc010080388 stack=[0xc010080000, 0xc020080000]
fatal error: stack overflow
runtime stack:
runtime.throw({0x496535?, 0x50e900?})
 /usr/lib/golang/src/runtime/panic.go:992 +0x71
runtime.newstack()
 /usr/lib/golang/src/runtime/stack.go:1101 +0x38c
runtime.morestack()
 /usr/lib/golang/src/runtime/asm_amd64.s:547 +0x8cc
```
### 24. Acknowledge Go's No-Tail-Call Position
*Principle: Tail-call recursion keeps the stack independent of call depth, but Go does not perform the optimization..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Tail recursion as a solution to stack limitations", "Rewriting a recursive function into a tail-call recursive function"*

**Do:** Write tail-call recursive functions when clarity benefits.; Remember that some languages (Haskell, JavaScript) execute them in constant stack.; Be aware of the limitation when porting from another language..

**Don't:** Don't expect Go to flatten the call stack for you.; Don't use tail-call recursion to evade a stack overflow on a real production input..

```
func Fact(input int) int {
 if input == 0 {
 return 1
 }
 return input * Fact(input-1)
}

func tailCallFactorial(n int) int {
 var factorial func(counter, result int) int
 factorial = func(counter, result int) int {
 if counter == 0 {
 return result
 }
 return factorial(counter-1, result*counter)
 }
 return factorial(n, 1)
}
```
### 25. Chain Functions with Type-Aliased Methods
*Principle: Attach generic functions as methods on a type alias to enable dot-notation chaining..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Dot notation to chain functions on slices"*

**Do:** Define `type ints []int` and attach `Map`, `Filter`, `Sum`.; Use fluent style for short, obvious pipelines.; Remember it is sugar; the underlying functions still work the same..

**Don't:** Don't chain when you need to branch on intermediate results.; Don't force fluent style when separate statements are clearer.; Don't chain when each step needs its own concurrency tuning..

```
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
### 26. Treat Lazy Evaluation Explicitly
*Principle: Go is eager; reach for laziness when the savings outweigh the wrapping cost..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Lazy evaluation of function calls", "Delaying and avoiding execution", "Infinite data structures and lazy evaluation"*

**Do:** Wrap deferred computation in `func() []T`.; Use short-circuiting `Any` rather than `Filter` + `len > 0`.; Be willing to port infinite-list examples to idiomatic Go for-loops..

**Don't:** Don't pretend Go has Haskell-style laziness; eager evaluation will run everything.; Don't build an infinite list with a generator that ignores termination.; Don't use laziness to hide expensive work that should be moved out of the hot path..

```go
func main() {
    input := []int{1, 2, 3, 4, 5, 6}
    isEven := func(i int) bool {
 return i%2 == 0
    }
    numberPrinter(func() []int {
 return Filter(input, isEven)
    })
}
func numberPrinter(lazyGet func() []int) {
 fmt.Println("At this line, we don't yet know what our
 input values will be")
 for _, in := range lazyGet() {
 fmt.Println(in)
 }
}

func Head[A any](input []A) Maybe[A] {
 if len(input) == 0 {
 return Nothing[A]()
 }
 return Just(input[0])
}
```

```go
func (i ints) Head() Maybe[int] {
 return Head(i)
}

func IntRange(start, end int) []int {
 out := []int{}
 for i := start; i <= end; i++ {
 out = append(out, i)
 }
 return out
}
```

```go
func main() {
 largerThan10Mil := func(i int) bool {
 return i > 10_000_000
 }
 res := ints(IntRange(0, 100)).
 Map(Factorial).
 Filter(largerThan10Mil).
 Head()
 fmt.Printf("%v\n", res)
}
```

```text
{39916800}
```

```haskell
InfiniteInts :: [Int]
InfiniteInts = [1..]

naturals :: [Int]
naturals = [2..]
sieve :: [Int] -> [Int]
sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
primes :: Int -> [Int]
primes n = take n (sieve naturals)
main :: IO ()
main = do
 let millionPrimes = primes 1000000
 putStrLn $ "Generated " ++ show (length millionPrimes)
 ++ " prime numbers"
```

```go
func main() {
 primes := []int{}
 for len(primes) != 1_000_000 {
 // sieve or other algorithm to get prime
 }
}
```
### 27. Use Continuation-Passing Style Sparingly
*Principle: CPS makes the next step explicit but is heavy in Go's strict type system..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Continuation-passing style programming", "Implementing CPS code in Go", "Simple mathematics operations with CPS", "CPS and goroutines"*

**Do:** Use CPS for compilers, interpreters, and complex async control flow.; Reach for callbacks in goroutine-launched asynchronous code.; Pass results downward through continuations..

**Don't:** Don't reach for CPS for everyday control flow; Go's channels do better.; Don't model a one-step function as CPS.; Don't fight the type system with nested continuation signatures..

```
func factorial(n int, f func(int)) {
 if n == 1 {
 f(1) // base-case
 } else {
 factorial(n-1, func(y int) {
 f(n * y)
 })
 }
}

func main() {
 factorial(5, func(i int) {
 fmt.Printf("result: %v", i)
 })
}

func main() {
 is := []int{1, 2, 3, 4, 5, 6}
 isEven(is, func(i int) {
 double(i, print)
 })
}
func isEven(input []int, cont func(int)) {
 for _, i := range input {
 if i%2 == 0 {
 cont(i)
 }
 }
}
func double(input int, cont func(int)) {
 cont(input * 2)
}
func print(i int) {
 fmt.Println(i)
}

func main() {
 is := []int{1, 2, 3, 4, 5, 6}
 isEven(is, func(i int) {
 double(i, print)
 })
}

func main() {
 is := []int{1, 2, 3, 4, 5, 6}
 isEven(is, double(i, print))
}

func isEven(input []int, cont func(int, func(int))) {

func main() {
 callback := func(input int, b bool) {
 if b {
 fmt.Printf("the number %v is
 even\n", input)
 } else {
 fmt.Printf("the number %v is
 odd\n", input)
 }
 }
 for i := 0; i < 10; i++ {
 go isEven(i, callback)
 }
 _ = <-make(chan int)
}
func isEven(i int, callback func(int, bool)) {
 if i%2 == 0 {
 callback(i, true)
 } else {
 callback(i, false)
 }
}
```
### 28. Replace OO Patterns with Function Fields
*Principle: Strategy, Decorator, IoC, and Singleton all collapse when behavior is a value..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "The strategy pattern", "The decorator pattern", "The Hollywood principle"*

**Do:** Use a named function type in place of a one-method interface.; Compose functions for decorators.; Express state in closures rather than struct fields.; Equate `AtbashDecipher = AtbashCipher` when a function is its own inverse..

**Don't:** Don't define a single-method interface for the function alone.; Don't use struct embedding when a closure captures the same state.; Don't wrap a function with a struct that adds nothing but boilerplate..

```
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

var (
 alphabet [26]rune = [26]rune{'a', 'b', 'c', 'd', 'e',
 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
)
func indexOf(r rune, rs [26]rune) (int, bool) {
 for i := 0; i < len(rs); i++ {
 if r == rs[i] {
 return i, true
 }
 }
 return -1, false
}
type CipherService struct {
 Strategy CipherStrategy
}

func (c CaesarCipher) Cipher(input string) string {
 output := ""
 for _, r := range input {
 if idx, ok := indexOf(r, alphabet); ok {
 idx += c.Rotation
                   idx = idx % 26
                   output += string(alphabet[idx])
 } else {
 output += string(r)
 }
 }
 return output
}
func (c CaesarCipher) Decipher(input string) string {
 output := ""
 for _, r := range input {
 if idx, ok := indexOf(r, alphabet); ok {
 idx += (26 - c.Rotation)
                   idx = idx % 26
                   output += string(alphabet[idx])
 } else {
 output += string(r)
 }
 }
 return output
}

type AtbashCipher struct {}
func (a AtbashCipher) Cipher(input string) string {
 output := ""
 for _, r := range input {
 if idx, ok := indexOf(r, alphabet); ok {
 idx = 25 - idx
                   output += string(alphabet[idx])
 } else {
 output += string(r)
 }
 }
 return output
}
func (a AtbashCipher) Decipher(input string) string {
 return a.Cipher(input)
}

func main() {
 svc := CipherService{}
 svc.Strategy = CaesarCipher{Rotation: 10}
 fmt.Println(svc.Cipher("helloworld"))
 svc.Strategy = AtbashCipher{}
 fmt.Println(svc.Cipher("helloworld"))
}

func CaesarCipher(input string, rotation int) string {
 output := ""
 for _, r := range input {
 idx := indexOf(r, alphabet)
 idx += rotation
 idx = idx % 26
 output += string(alphabet[idx])
 }
 return output
}
func CaesarDecipher(input string, rotation int) string {
 output := ""
 for _, r := range input {
 idx := indexOf(r, alphabet)
 idx += (26 - rotation)
 idx = idx % 26
 output += string(alphabet[idx])
 }
 return output
}

func AtbashCipher(input string) string {
 output := ""
 for _, r := range input {
 if idx, ok := indexOf(r, alphabet); ok {
 idx = 25 - idx
 output += string(alphabet[idx])
 } else {
 output += string(r)
 }
 }
 return output
}
var AtbashDecipher = AtbashCipher

func LogCipher(cipher CipherFunc) CipherFunc {
 return func(input string) string {
 log.Printf("ciphering: %s\n", input)
 return cipher(input)
 }
}
func LogDecipher(decipher DecipherFunc) DecipherFunc {
 return func(input string) string {
 log.Printf("deciphering: %s\n", input)
 return decipher(input)
 }
}

func main() {
 caesarCipher := func(input string) string {
 return CaesarCipher(input, 10)
 }
 caesarDecipher := func(input string) string {
 return CaesarDecipher(input, 10)
 }
 fpSvc := {
 CipherFn: LogCipher(caesarCipher),
 DecipherFn: LogDecipher(caesarDecipher),
 }
 fmt.Println(fpSvc.Cipher("hello"))
}
```
### 29. Compose Concurrent Functions with Channels
*Principle: Restrict concurrency to naturally independent work; expose channel in/out for composability..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Creating concurrent functions", "Concurrent filter implementation", "Concurrent Map and FMap implementation"*

**Do:** Use `Predicate[A any] = func(A) bool` and `MapFunc[A any] = func(A) A` in concurrent versions.; Split input into batches; aggregate from `out chan`.; Have each node `range` the input and `close(out)`.; Tune `batchSize` to balance goroutine overhead..

**Don't:** Don't return values from channel nodes; return the output channel.; Don't expect concurrent output to preserve order; sort afterwards.; Don't depend on element order across goroutines..

```go
type Predicate[A any] func(A) bool
func Filter[A any](input []A, p Predicate[A], out chan []A)
 {
 output := []A{}
 for _, element := range input {
 if p(element) {
 output = append(output, element)
 }
 }
 out <- output
}

func ConcurrentFilter[A any](input []A, p Predicate[A],
    batchSize int) []A {
    output := []A{}
out := make(chan []A)
   threadCount := int(math.Ceil(float64(len(input)) /
 float64(batchSize)))
   fmt.Printf("goroutines: %d\n", threadCount)
   for i := 0; i < threadCount; i++ {
 fmt.Println("spun up thread")
 if ((i + 1) * batchSize) < len(input) {
 go Filter(input[i*batchSize:(i+1)*batchSize],
 p, out)
 } else {
 go Filter(input[i*batchSize:], p, out)
 }
   }
   for i := 0; i < threadCount; i++ {
 filtered := <-out
 fmt.Printf("got data: %v\n", filtered)
 output = append(output, filtered.)
   }
   close(out)
   return output
}

func main() {
 ints := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
 output := ConcurrentFilter(ints, func(i int) bool {
 return i%2 == 0 }, 3)
 fmt.Printf("%v\n", output)
}
```

```text
goroutines: 4
spun up thread
spun up thread
spun up thread
spun up thread
got data: [10]
got data: [2]
got data: [4 6]
got data: [8]
[10 2 4 6 8]

[]int{1,2,3}
[]int{4,5,6}
[]int{7,8,9}
[]int{10}
```

```go
type MapFunc[A any] func(A) A
func Map[A any](input []A, m MapFunc[A], out chan []A) {
 output := make([]A, len(input))
 for i, element := range input {
 output[i] = m(element)
 }
 out <- output
}

func ConcurrentMap[A any](input []A, mapFn MapFunc[A],
 batchSize int) []A {
 output := make([]A, 0, len(input))
 out := make(chan []A)
 threadCount := int(math.Ceil(float64(len(input)) /
 float64(batchSize)))
 fmt.Printf("goroutines: %d\n", threadCount)
 for i := 0; i < threadCount; i++ {
 fmt.Println("spun up thread")
 if ((i + 1) * batchSize) < len(input) {
 go Map(input[i*batchSize:(i+1)
 *batchSize], mapFn, out)
 } else {
 go Map(input[i*batchSize:],
 mapFn, out)
 }
 }
 for i := 0; i < threadCount; i++ {
 mapped := <-out
 fmt.Printf("got data: %v\n", mapped)
 output = append(output, mapped.)
 }
 close(output)
 return output
}

func main() {
 ints := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
 output := ConcurrentFilter(ints, func(i int) bool {
 return i%2 == 0 }, 3)
 fmt.Printf("%v\n", output)
 output = ConcurrentMap(output, func(i int) int {
 return i * 2 }, 2)
 fmt.Printf("%v\n", output)
}
```

```text
goroutines: 4
spun up thread
spun up thread
spun up thread
spun up thread
got data: [10]
got data: [2]
got data: [4 6]
got data: [8]
[10 2 4 6 8]
{next statements are the output for the map function}
goroutines: 3
spun up thread
spun up thread
spun up thread
got data: [16]
got data: [20 4]
got data: [8 12]
[16 20 4 8 12]
```

```go
func FMap[A, B any](input []A, m func(A) B, out chan []B) {
 output := make([]B, len(input))
 for i, element := range input {
 output[i] = m(element)
 }
 out <- output
}
func ConcurrentFMap[A, B any](input []A, fMapFn ,
 batchSize int) []B {
 output := make([]B, 0, len(input)
 out := make(chan []B)
 threadCount := int(math.Ceil(float64(len(input)) /
 float64(batchSize)))
 fmt.Printf("goroutines: %d\n", threadCount)
 for i := 0; i < threadCount; i++ {
 fmt.Println("spun up thread")
 if ((i + 1) * batchSize) < len(input) {
 go FMap(input[i*batchSize:
 (i+1)*batchSize], fMapFn, out)
 } else {
 go FMap(input[i*batchSize:],
 fMapFn, out)
 }
 }
 for i := 0; i < threadCount; i++ {
 mapped := <-out
 fmt.Printf("got data: %v\n", mapped)
 output = append(output, mapped.)
 }
 return output
}
```
### 30. Build Pipelines from Channel-Based Nodes
*Principle: Model a pipeline as `Generator → Node → Node → Collector`, where each node reads and writes channels..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "The pipeline pattern", "Chaining functions with channels", "Improved function chaining"*

**Do:** Use `type Node[A any] func(<-chan A) <-chan A` and `type GeneratorNode[A any] func() <-chan A`.; Range the input channel and `close(out)` from the goroutine.; Use `ChainPipes` to compose nodes.; `return out` from the node; never return a scalar..

**Don't:** Don't return values from a node; it returns a stream channel.; Don't reuse channels across calls.; Don't share intermediate state across nodes through globals..

```go
func FilterNode[A any](in <-chan A, predicate Predicate[A])
 <-chan A {
 out := make(chan A)
 go func() {
 for n := range in {
 if predicate(n) {
 out <- n
 }
 }
 close(out)
 }()
 return out
}

func MapNode[A any](in <-chan A, mapf MapFunc[A]) <-chan A
 {
 out := make(chan A)
 go func() {
 for n := range in {
 out <- mapf(n)
 }
 close(out)
 }()
 return out
}

func Generator[A any](input .A) <-chan A {
 out := make(chan A)
 go func() {
 for _, element := range input {
 out <- element
 }
 close(out)
 }()
 return out
}

func Cat(filepath string) <-chan string {
 out := make(chan string)
 f, err := ioutil.ReadFile(filepath)
 if err != nil {
 panic(err)
 }
 go func() {
 lines := strings.Split(string(f), "\n")
 for _, line := range lines {
 out <- line
 }
 close(out)
 }()
 return out
}

func Collector[A any](in <-chan A) []A {
 output := []A{}
 for n := range in {
 output = append(output, n)
 }
 return output
}

func main(){
 generated := Generator(1, 2, 3, 4)
 filtered := FilterNode(generated, func(i int) bool
 { return i%2 == 0 })
 mapped := MapNode(filtered, func(i int) int {
 return i * 2 })
 collected := Collector(mapped)
 fmt.Printf("%v\n", collected)
}
```

```text
[4 8]
```

```go
type (
 Node[A any]         func(<-chan A) <-chan A
 GeneratorNode[A any] func() <-chan A
)
func ChainPipes[A any](in <-chan A, nodes .Node[A]) []A {
 for _, node := range nodes {
 in = node(in)
 }
 return Collector(in)
}

func CurriedFilterNode[A any](p Predicate[A]) Node[A] {
 return func(in <-chan A) <-chan A {
 out := make(chan A)
 go func() {
 for n := range in {
 if p(n) {
 out <- n
 }
 }
            close(out)
 }()
 return out
 }
}
func CurriedMapNode[A any](mapFn MapFunc[A]) Node[A] {
 return func(in <-chan A) <-chan A {
 out := make(chan A)
 go func() {
 for n := range in {
 out <- mapFn(n)
 }
            close(out)
 }()
 return out
 }
}
```

```go
func ChainPipes[A any](gn GeneratorNode[A], nodes
 .Node[A]) []A {
 in := gn()
 for _, node := range nodes {
 in = node(in)
 }
 return Collector(in)
}

func CurriedCat(filepath string) func() <-chan string {
 return func() <-chan string {
 out := make(chan string)
 f, err := ioutil.ReadFile(filepath)
 if err != nil {
 panic(err)
 }
 go func() {
 lines := strings.Split(string(f),
 "\n")
 for _, line := range lines {
 out <- line
 }
           close(out)
 }()
 return out
 }
}
```

```go
func main() {
 out := ChainPipes[string](CurriedCat("./main.go"),
 CurriedFilterNode(func(s string) bool {
 return strings.Contains(s, "func") }),
 CurriedMapNode(func(i string) string {
 return "line contains func: " + i }))
 fmt.Printf("%v\n", out2)
}
```
### 31. Test by Boundary, Not by Implementation
*Principle: Pure functions take inputs and return outputs; test that contract directly..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Example 1 – hotdog shop"*

**Do:** Drive `Charge` with a table-driven test covering success, exact balance, and over-charge.; Use a mock `PaymentFunc` to verify `OrderHotdog` returns a closure that calls the payment function.; Assert the inner-function call flag and the hotdog value separately..

**Don't:** Don't capture panics instead of testing the return value.; Don't let tests rely on global state to track whether something was called.; Don't use real `time.Now` or `rand.Intn` in unit tests..

```
var (
  testChargeStruct = []struct {
 inputCard CreditCard
 amount int
 outputCard CreditCard
 err CreditError
  }{
 {
 CreditCard{1000},
 500,
 CreditCard{500},
 nil,
 },
 {
 CreditCard{20},
 20,
 CreditCard{0},
 nil,
 },
 {
 CreditCard{150},
 1000,
 CreditCard{150}, // no money is withdrawn
 NOT_ENOUGH_CREDIT,
 // payment fails with this error
 },
  }
)

func TestCharge(t *testing.T) {
   for _, test := range testChargeStruct {
 t.Run("", func(t *testing.T) {
 output, err := Charge(test.inputCard, test.
 amount)
 if output != test.outputCard || !errors.
 Is(err, test.err) {
 t.Errorf("expected %v but got %v\n,
 error expected %v but got %v",
 test.outputCard, output, test.err, err)
 }
 })
}
}

func TestOrderHotdog(t *testing.T) {
    testCC := CreditCard{1000}
    calledInnerFunction := false
    mockPayment := func(c CreditCard, input int) (CreditCard,
 CreditError) {
 calledInnerFunction = true
 testCC.credit -= input
 return testCC, nil
    }
    hotdog, resultF := OrderHotdog(testCC, mockPayment)
    if hotdog != NewHotdog() {
 t.Errorf("expected %v but got %v\n", NewHotdog(),
 hotdog)
   }
   _, err := resultF()
   if err != nil {
 t.Errorf("encountered %v but expected no error\n",
 err)
   }
   if calledInnerFunction == false {
 t.Errorf("Inner function did not get called\n")
   }
}
```
### 32. Use Pre-Generics Pie When Stuck Below 1.18
*Principle: Reach for the v1 Pie code-generation approach only when Go is below 1.18..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Code generation libraries for pre-generics Go", "A slice of Pie", "Pie for custom data types"*

**Do:** Use `pie.Ints{.}.Filter(.).Map(.)` for built-in slice types.; Generate per-type methods with `//go:generate pie Dogs.*` for custom types.; Add `$GOPATH/bin` (or `go/bin`) to your `PATH` so `go generate` can find the executable..

**Don't:** Don't add a code-generation dependency when you can adopt generics.; Don't import the v1 package in a project that runs on Go 1.18+.; Don't accept large binary bloat from generated per-type code; consolidate..

```go
go 1.17
require github.com/elliotchance/pie v1.39.0

package main
import (
 "fmt"
 "github.com/elliotchance/pie/pie"
)
func main() {
 out := pie.Ints{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}.
 Filter(func(i int) bool {
 return i%2 == 0
 }).
 Map(func(i int) int { return i * i })
 fmt.Printf("result: %v\n", out)
}
```

```text
result: [4 16 36 64 100]
```

```go
//go:generate pie Dogs.*
type Dogs []Dog
type Dog struct {
 Name string
 Age int
}

// Reverse returns a new copy of the slice with the
 elements ordered in reverse.
// This is useful when combined with Sort to get a
 descending sort order:
//
// ss.Sort().Reverse()
//
func (ss Dogs) Reverse() Dogs {
 // Avoid the allocation. If there is one element or
 less it is already
 // reversed.
 if len(ss) < 2 {
 return ss
 }
 sorted := make([]Dog, len(ss))
 for i := 0; i < len(ss); i++ {
 sorted[i] = ss[len(ss)-i-1]
 }
 return sorted
}
```

```go
func (ss Dogs) Filter(condition func(Dog) bool) (ss2
 Dogs) {
 for _, s := range ss {
 if condition(s) {
 ss2 = append(ss2, s)
 }
 }
 return
}
func (ss Dogs) Map(fn func(Dog) Dog) (ss2 Dogs) {
 if ss == nil {
 return nil
 }
 ss2 = make([]Dog, len(ss))
 for i, s := range ss {
 ss2[i] = fn(s)
 }
 return
}

func main() {
 MyDogs := []pkg.Dog{
 pkg.Dog{
 "Bucky",
 1,
 },
 pkg.Dog{
 "Keeno",
            15,
 },
 pkg.Dog{
 "Tala",
            16,
 },
 pkg.Dog{
 "Amigo",
            7,
 },
 }
 results := pkg.Dogs(MyDogs).
 Filter(func(d pkg.Dog) bool {
 return d.Age > 10
 }).SortUsing(func(a, b pkg.Dog) bool {
 return a.Age < b.Age
 })
 fmt.Printf("results: %v\n", results)
}
```

```text
results: [{Keeno 15} {Tala 16}]
```
### 33. Reach for Post-Generics FP Libraries When They Add Real Value
*Principle: Use Pie v2 for dot-notation chains, `lo` for nested calls and parallelism, and `mo` for monad-like types..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Post-generics functional programming libraries", "Pie with generics", "Lodash, for Go", "An example implementation with lo", "Mo, for go"*

**Do:** Use `pie.Of(MyDogs).Filter(.).Map(.).SortUsing(.)`.; Use `lo.Map`, `lo.Uniq`, and `lo/parallel.Map` for Lodash-style pipelines with concurrency.; Use `mo.Some`/`mo.None`/`mo.Ok`/`mo.Err` for `Option`/`Result` semantics..

**Don't:** Don't depend on a library for a 30-line generic helper.; Don't skip license review for commercial code.; Don't pick a library whose last commit is years old.; Don't rebuild a `Result` type with a hand-rolled `(T, error)` when `mo.Err` already does it..

```go
go 1.18
require github.com/elliotchance/pie/v2 v2.3.0

type Dog struct {
 Name string
 Age int
}
```

```go
import "github.com/elliotchance/pie/v2"
func main() {
 MyDogs := []Dog{
 Dog{
 "Bucky",
            1,
 },
 Dog{
 "Keeno",
            15,
 },
 Dog{
 "Tala",
            16,
 },
 Dog{
 "Amigo",
            7,
 },
 }
 result := pie.Of(MyDogs).
 Filter(func(d Dog) bool {
 return d.Age > 10
 }).Map(func(d Dog) Dog {
 d.Name = strings.ToUpper(d.Name)
 return d
 }).
 SortUsing(func(a, b Dog) bool {
 return a.Age < b.Age
 })
 fmt.Printf("out: %v\n", result)
}

go 1.18
require (
 github.com/samber/lo v1.37.0
)
```

```go
func main() {
 result :=
 lo.Map(lo.Uniq(MyDogs), func(d Dog, i int)
 Dog {
 d.Name = strings.ToUpper(d.Name)
               return d
 })
 fmt.Printf("%v\n", result)
}

 lop "github.com/samber/lo/parallel"
```

```go
 result :=
 lop.Map(lo.Uniq(MyDogs), func(d Dog, i int)
 Dog {
 d.Name = strings.ToUpper(d.Name)
               return d
 })
 fmt.Printf("%v\n", result)
}

func main() {
 maybe := mo.Some(Dog{"Bucky", 1})
 getOrElse := maybe.OrElse(Dog{})
 fmt.Println(getOrElse)
}
```

```text
{Bucky 1}
```

```go
 maybe2 := mo.None[Dog]()
 getOrElse2 := maybe2.OrElse(Dog{"Default", -1})
 fmt.Println(getOrElse2)
```

```text
{Default -1}
```

```go
 ok := mo.Ok(MyDogs[0])
 result1 := ok.OrElse(Dog{})
err1 := ok.Error()
 fmt.Println(result1, err1)
 err := errors.New("dog not found")
 ok2 := mo.Err[Dog](err)
 result2 := ok2.OrElse(Dog{"Default", -1})
 err2 := ok2.Error()
 fmt.Println(result2, err2)
```

```text
{Bucky 1} <nil>
{Default -1} dog not found
```
### 34. Match FP Discipline to the Problem
*Principle: "Aggregates everywhere" is the wrong default; "ubiquitous language everywhere" is the right one..* — Ref: Functional_Programming_in_Go_-_Dylan_Meeus.md — "Concurrency and Functional Programming", "Functional programming and concurrency"*

**Do:** Keep a strong language even when an aggressive time-to-market demands a simple architecture.; Reclassify a supporting capability when business rules become profitable and complex.; Use language complexity as an early signal that active records no longer fit.; Start with wider safe boundaries and extract services after learning..

**Don't:** Don't pronounce every noun an aggregate.; Don't split one aggregate's logic between application code and a database team.; Don't let simple supporting logic inherit event sourcing merely because management labels the initiative core.; Don't ignore implementation pain; it signals a mismatched model or tactic.

---

## Anti-Patterns & Common Mistakes

- **"Pointers are faster":** False by default. Benchmark before believing. → *fix:* write paired benchmarks with `b.ReportAllocs()` and inspect with `go build -gcflags '-m -l'`.
- **Mutable state via global var in recursion:** Concurrency, testability, and call isolation all break. → *fix:* use the outer-closure pattern with `var inner func(...); inner = func(...)`.
- **Recursing with `inner := func(...) { inner(...) }`:** Won't compile. → *fix:* declare `var inner func(...)` first, then assign.
- **Treating `(T, error)` as the only error path:** "Not found" is not exceptional. → *fix:* use `Maybe[T]` or `Result[T]` for may-be-absent cases.
- **Interface for a single function:** Verbose stand-in for a function type. → *fix:* use `type MyFunc func(...) ...` and a struct field.
- **FP library for 30 lines of generics:** Premature dependency. → *fix:* write your own first; adopt a library for genuine repetition.
- **Setter functions that mutate struct fields:** Destroys immutability, makes the function impure. → *fix:* accept by value, return a new struct.
- **Forgetting `close(out)` in a channel node:** Leaks the receiver goroutine. → *fix:* `defer close(out)` at the top of the goroutine.
- **CPS for everyday control flow:** Reads poorly in Go. → *fix:* use CPS only for compilers/interpreter-style work.
- **Map-discriminator vs switch:** Adding a new operation to a long `switch` is friction. → *fix:* use a `map[string]OpFunc`.
- **Currying without a higher-order consumer:** `f(a, b)` is more readable than `f(a)(b)`. → *fix:* curry only to fit a `Node[A]`.
- **Pre-allocating large maps in eager chains when you only need the first match:** No laziness in Go. → *fix:* use `Any` to short-circuit instead of `Filter` + `len > 0`.
- **Skipping the base case in recursion:** Stack overflow. → *fix:* always have a base case.
- **Concurrent map preserving element order:** It cannot. → *fix:* sort after aggregation.
- **Mixing strategies and active records arbitrarily:** Be explicit about the level of pure or impure style per module.

## Decision Heuristics / Checklists

- **Pure or impure?** Pass-by-value inputs, returns new value, no globals, no I/O → keep pure; otherwise thin shell.
- **Generics?** Writing `filterStrings`, `filterInts`, `filterDogs` → use `Predicate[A]`.
- **Type alias vs interface?** One-method contract → function alias; multi-method stateful collaboration → interface.
- **Map dispatcher vs switch?** Adding branches more than once a year → use a map; otherwise a switch is fine.
- **Recursion or iteration?** Tree/graph traversal or self-similar structure → recursion; linear scan over huge input → iteration. Always have a base case; always benchmark.
- **Dot chain or nested calls?** Short, obvious pipeline → dot-notation (`Map.Filter.Sum`); anything that needs intermediate inspection → separate statements.
- **Channel pipeline or plain calls?** If any step is asynchronous, slow, or stream-shaped → channels and `Node[A]`. Otherwise just call the functions.
- **Add a library or write 30 lines?** Default to writing your own generic toolbox; adopt a library when need is recurring.
- **Mock by interface or by function?** Function field is usually enough; use a function-type alias in the struct.
- **CPS?** Use only for compilers, interpreters, or layered async control flow.
- **Pie v1 vs v2?** v1 only for pre-1.18; v2 for any new generics work.
- **lo, mo, or hand-rolled?** `lo` for nested pipelines, `mo` for `Option`/`Result`, hand-rolled for 30 lines of bespoke code.

## Key Takeaways

1. **Go is multi-paradigm.** Treat FP as a tool, not a religion.
2. **First-class functions unlock testability and composition.** Type aliases make signatures and errors self-documenting.
3. **Higher-order functions enable abstractions.** Closure, partial application, and currying each have their place, with currying reserved for fitting higher-order signatures.
4. **Strive for purity, accept I/O at the edges.** Pure functions are testable, safe to parallelize, and trustworthy to read.
5. **Value semantics + generics make immutability ergonomic.** Pass-by-value copies often live on the stack and beat pointer-based code in benchmarks.
6. **Map/Filter/Reduce with generics cover 80% of collection work.** Pre-allocate, short-circuit, and use a `Number` type constraint.
7. **Maybe and Result eliminate nil checks.** Use `GetOrElse` for absence and explicit `Result` types for fallible operations.
8. **Recursion shines on recursive data; iteration wins on large input.** Go has no tail-call optimization; respect the 1 GB stack on 64-bit hosts.
9. **Dot-notation is sugar.** Type aliases wrap your generic toolbox; the underlying functions still work the same.
10. **Pipelines = channels + curried nodes.** `ChainPipes` composes `Node[A]`s, but always `close(out)` and never return scalars.
11. **Concurrency belongs to independent work.** Batch input, aggregate from a channel, and sort afterwards if order matters.
12. **FP libraries are tools, not religion.** Pie v2, `lo`, and `mo` each shine in their niche; reach for them after you know the cost.
13. **Let the problem pick the pattern.** Forced purity, forced recursion, or forced libraries will hurt the code more than the original sin of an "if" statement.

## Cross-References
- Related: [[./Learning_Domain_Driven_Design.md]]
- Related: [[./Building_Modern_CLI_Applications_in_Go.md]]
- Related: [[./Efficient_Go_Data-Driven_Optimization.md]]
- Related: [[../INDEX.md]].
