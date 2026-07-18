# Mastering Go
**Author:** Mihalis Tsoukalos
**Topic tags:** `#general` `#concurrency` `#testing` `#cli` `#systems` `#api`
**Language focus:** Go-first
**Sources:** `markdown_output/Mastering_Go_-_Mihalis_Tsoukalos/Mastering_Go_-_Mihalis_Tsoukalos.md` · `summaries/Mastering_Go_-_Mihalis_Tsoukalos.md`

## TL;DR
*Mastering Go* connects Go's small language core to the runtime, Unix, concurrency, testing, profiling, HTTP, and lower-level networking.
Use it to build explicit, observable programs from standard-library primitives: return errors, compose `io.Reader` and `io.Writer`, synchronize goroutines, bound network waits, test handlers, and profile before optimizing.
Its deepest recurring lesson is to understand the machinery without bypassing Go's safety unless a measured systems requirement forces you to do so.

---

## Best Practices by Topic

### 1. Treat Compiler Strictness as a Quality Gate

**Principle:** Let the compiler reject unused imports, malformed blocks, and type mismatches instead of weakening its checks.

**Do:**
- Remove packages you do not use.
- Put an opening brace on the declaration line.
- Read compiler diagnostics as specific repair instructions.
- Use blank imports only for packages whose initialization side effects are required.

**Don't:**
- Don't accumulate speculative imports.
- Don't fight automatic semicolon insertion with a brace on the next line.
- Don't hide ordinary unused imports behind `_`.

**Code:**
```go
package main 
import ( 
 "fmt" 
) 
func main() { 
 fmt.Println("This is a sample Go program!") 
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Two Go rules"*

---

### 2. Choose `go build` for Artifacts and `go run` for Experiments

**Principle:** Build a self-contained binary for distribution; use `go run` when a disposable compile-and-execute cycle is more useful.

**Do:**
- Build when you need an executable to inspect, transfer, trace, or run repeatedly.
- Use `go run` for quick examples and development checks.
- Remember that `go run` still compiles an executable before deleting it.
- Inspect build steps with `go build -x` when the toolchain itself is relevant.

**Don't:**
- Don't mistake `go run` for interpretation.
- Don't trace `go run` when temporary compiler activity would obscure the target process.

**Code:**
```go
package main
import (
 "fmt"
)
func main() {
 fmt.Println("Hello there!")
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Compiling Go code / Executing Go code / Learning more about go build"*

---

### 3. Keep Standard Output and Standard Error Semantically Separate

**Principle:** Write result data to `os.Stdout` and diagnostics to `os.Stderr` so Unix callers can redirect each stream independently.

**Do:**
- Use `os.Stdin`, `os.Stdout`, and `os.Stderr` instead of platform paths.
- Use `fmt.Print` when the data already contains a newline.
- Use `fmt.Printf` when formatting control matters.
- Use the `F` family when writing through an `io.Writer`.

**Don't:**
- Don't mix machine-readable output and errors on one stream.
- Don't assume `fmt.Print`, `fmt.Println`, and `fmt.Printf` space and terminate output identically.

**Code:**
```go
 io.WriteString(os.Stdout, "This is Standard
output\n") 
 io.WriteString(os.Stderr, myString) 
 io.WriteString(os.Stderr, "\n")
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Unix stdin, stdout, and stderr / About error output"*

---

### 4. Validate Command-Line Input Before Using It

**Principle:** Treat every command-line argument as untrusted text and check both cardinality and conversion errors.

**Do:**
- Check `len(os.Args)` before indexing.
- Remember that `os.Args[0]` is the executable name.
- Check every `strconv` conversion result.
- Keep searching when a utility is designed to tolerate individual invalid arguments.

**Don't:**
- Don't let a failed conversion silently become a zero value.
- Don't use `_` to discard production conversion errors.
- Don't assume that users provide the type your usage text requests.

**Code:**
```go
 for err != nil { 
 if k >= len(arguments) { 
 fmt.Println("None of the arguments is a
float!") 
 return 
 } 
 n, err = strconv.ParseFloat(arguments[k], 64) 
 k++ 
 } 
 min, max := n, n
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Error handling"*

---

### 5. Return or Log an Error Deliberately

**Principle:** Decide at the error boundary whether to recover, return, log, or terminate; do not react accidentally.

**Do:**
- Return `nil` when an error-returning function succeeds.
- Return errors when the caller can add context or choose policy.
- Log server and critical-process failures where they can be retained and searched.
- Reserve `log.Fatal` and `log.Panic` for conditions that justify termination.

**Don't:**
- Don't compare an `error` directly with a string.
- Don't both log and return the same error without a reason.
- Don't use `panic` as routine error handling.

**Code:**
```go
func returnError(a, b int) error { 
 if a == b { 
 err := errors.New("Error in returnError()
function!") 
 return err
 } else { 
 return nil 
 } 
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The error data type / General Go coding advices"*

---

### 6. Configure System Logging Before Emitting Events

**Principle:** Select a meaningful facility, severity, and process name, then verify that the host logger routes that facility.

**Do:**
- Use the executable basename as the logger identity.
- Check `syslog.New` before calling `log.SetOutput`.
- Match facilities to the host's syslog configuration.
- Use logging for persistent, searchable server diagnostics.

**Don't:**
- Don't assume an unconfigured facility will be retained.
- Don't use `log.Fatal` when deferred cleanup must run.
- Don't make unconditional noisy logging part of a reusable package API.

**Code:**
```go
 programName := filepath.Base(os.Args[0]) 
 sysLog, err :=
syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, 
 programName)
 if err != nil { 
 log.Fatal(err) 
 } else { 
 log.SetOutput(sysLog) 
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A Go program that sends information to log files"*

---

### 7. Understand the Tricolor Collector Before Tuning Memory

**Principle:** Reason about reachability through white, grey, and black sets before attributing latency or memory growth to the collector.

**Do:**
- Treat roots as the starting reachable set.
- Remember that grey objects are discovered but not fully scanned.
- Remember that black objects must not point to white objects.
- Understand that the write barrier preserves that invariant while the mutator runs.

**Don't:**
- Don't assume all unreachable objects disappear in the current cycle.
- Don't call concurrent collection equivalent to a simple stop-the-world sweep.
- Don't treat collector internals as detached from allocation behavior.

**Code:**
```go
func printStats(mem runtime.MemStats) {
 runtime.ReadMemStats(&mem)
 fmt.Println("mem.Alloc:", mem.Alloc)
 fmt.Println("mem.TotalAlloc:", mem.TotalAlloc)
 fmt.Println("mem.HeapAlloc:", mem.HeapAlloc)
 fmt.Println("mem.NumGC:", mem.NumGC)
 fmt.Println("-----")
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Garbage Collection / The Tricolor algorithm"*

---

### 8. Observe Garbage Collection with Runtime Evidence

**Principle:** Measure allocation and collection behavior with `runtime.MemStats`, `GODEBUG`, profiles, and traces instead of guessing.

**Do:**
- Refresh statistics with `runtime.ReadMemStats` before reading them.
- Use `GODEBUG=gctrace=1` to inspect heap transitions.
- Interpret the live heap separately from total allocation.
- Use execution tracing when pause placement and scheduler interaction matter.

**Don't:**
- Don't invoke `runtime.GC()` casually; it blocks its caller and may stall a busy program.
- Don't optimize collection behavior before establishing an allocation problem.

**Code:**
```go
 var mem runtime.MemStats
 printStats(mem)
 for i := 0; i < 10; i++ {
 s := make([]byte, 50000000)
 if s == nil {
 fmt.Println("Operation failed!")
 }
 }
 printStats(mem)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Garbage Collection"*

---

### 9. Keep `unsafe` Exceptional and Contained

**Principle:** Use `unsafe` only when type safety must be traded for a demonstrated low-level requirement.

**Do:**
- Isolate unsafe conversions behind a small boundary.
- Check representation size and alignment assumptions.
- Use `unsafe.Sizeof`, `unsafe.Offsetof`, and `unsafe.Alignof` to inspect layout.
- Recognize that `runtime`, `syscall`, and `os` use unsafe code internally so callers usually do not have to.

**Don't:**
- Don't use pointer arithmetic when normal indexing works.
- Don't expect the compiler to catch out-of-bounds access performed through raw addresses.
- Don't convert a wider value through a narrower pointer and expect preservation.

**Code:**
```go
func main() {
 var value int64 = 5
 var p1 = &value
 var p2 = (*int32)(unsafe.Pointer(p1))
 fmt.Println("*p1: ", *p1)
 fmt.Println("*p2: ", *p2)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Unsafe code"*

---

### 10. Cross the C Boundary with Explicit Ownership

**Principle:** Use cgo only for capabilities that cannot reasonably stay in Go, and make C allocation ownership visible.

**Do:**
- Put `import "C"` immediately after the cgo preamble.
- Use `C.CString` for Go-to-C strings.
- Free C-allocated strings with `C.free`.
- Prefer one mixed file for small calls and a static C library for larger integrations.

**Don't:**
- Don't forget that a C string is not garbage-collected by Go.
- Don't scatter repeated cgo calls throughout the application.
- Don't assume cgo preserves Go's portability and safety.

**Code:**
```go
 fmt.Println("Going to call another C function!")
 myMessage := C.CString("This is Mihalis!")
 defer C.free(unsafe.Pointer(myMessage))
 C.printMessage(myMessage)
 fmt.Println("All perfectly done!")
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Calling C code from Go using separate files"*

---

### 11. Use `defer` Near Acquisition and Understand Capture

**Principle:** Defer cleanup beside acquisition, but pass loop values explicitly when deferred closures must preserve each iteration's value.

**Do:**
- Place `defer f.Close()` immediately after a successful open.
- Remember that deferred calls run in LIFO order.
- Pass loop state as an anonymous-function parameter.
- Use deferred recovery only around a boundary that can handle the failure coherently.

**Don't:**
- Don't defer closures that ambiguously capture a changing loop variable.
- Don't expect statements after the panicking call to execute.
- Don't use bare `panic` when an ordinary error can be returned.

**Code:**
```go
func d3() {
 for i := 3; i > 0; i-- {
 defer func(n int) {
 fmt.Print(n, " ")
 }(i)
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The defer keyword / Panic and Recover"*

---

### 12. Inspect the Runtime and Toolchain When Assumptions Matter

**Principle:** Query architecture, compiler, Go version, CPU count, and goroutine count instead of hard-coding the environment.

**Do:**
- Use `runtime.Version()` for the active Go version.
- Use `runtime.NumCPU()` when CPU availability informs design.
- Use `runtime.NumGoroutine()` while diagnosing lifecycle behavior.
- Inspect assembly with `go tool compile -S` only when low-level evidence is useful.

**Don't:**
- Don't parse a version string without checking conversion errors.
- Don't assume all `GOOS` and `GOARCH` pairs are valid.
- Don't treat generated assembly as the first debugging tool.

**Code:**
```go
func main() {
 fmt.Print("You are using ", runtime.Compiler, " ")
 fmt.Println("on a", runtime.GOARCH, "machine")
 fmt.Println("Using Go version", runtime.Version())
 fmt.Println("Number of CPUs:", runtime.NumCPU())
 fmt.Println("Number of Goroutines:", runtime.NumGoroutine())
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Your Go environment / The Go Assembler"*

---

### 13. Prefer Slices for Dynamic Sequences

**Principle:** Use slices for variable-size data and arrays only when fixed cardinality is part of the requirement.

**Do:**
- Create slices with literals or `make`.
- Track length and capacity separately.
- Use `append` rather than indexing beyond the current length.
- Preallocate when the expected size is known.

**Don't:**
- Don't pass large arrays when an array copy is unnecessary.
- Don't assume append preserves the backing array.
- Don't use multidimensional slices when a simpler model is available.

**Code:**
```go
 aSlice := []int{-1, 0, 4}
 fmt.Printf("aSlice: ")
 printSlice(aSlice)
 fmt.Printf("Cap: %d, Length: %d\n", cap(aSlice),
len(aSlice))
 aSlice = append(aSlice, -100)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Go slices / Slices are being expanded automatically"*

---

### 14. Treat Re-Slicing as Shared Storage

**Principle:** A re-slice references the same backing array, so changes and retention propagate beyond the apparent view.

**Do:**
- Copy when the new slice must own independent data.
- Size the destination before calling `copy`.
- Remember that `copy(dst, src)` copies the smaller length.
- Release references to large backing arrays when a tiny retained view would pin them.

**Don't:**
- Don't mistake `s[a:b]` for a deep copy.
- Don't assume copying into a shorter destination copies every source element.
- Don't retain a tiny subsection of a huge file buffer without considering memory retention.

**Code:**
```go
 s1 := make([]int, 5)
 reSlice := s1[1:3]
 fmt.Println(s1)
 fmt.Println(reSlice)
 reSlice[0] = -100
 reSlice[1] = 123456
 fmt.Println(s1)
 fmt.Println(reSlice)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Performing basic operations on slices / The copy() function"*

---

### 15. Use Maps for Keyed Lookup, Not Ordered Output

**Principle:** Use maps when key-based access is the requirement, and test key presence separately from the zero value.

**Do:**
- Initialize a writable map with `make` or a literal.
- Use `value, ok := m[key]` to distinguish absence.
- Use `delete` without prechecking when deletion semantics permit it.
- Synchronize every concurrent write and conflicting read.

**Don't:**
- Don't write to a nil map.
- Don't infer presence from a returned zero value.
- Don't depend on map iteration order.
- Don't perform concurrent map writes without coordination.

**Code:**
```go
 _, ok := iMap["doesItExist"]
 if ok {
 fmt.Println("Exists!")
 } else {
 fmt.Println("Does NOT exist")
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Go maps / Storing to a nil map"*

---

### 16. Distinguish Bytes, Runes, and String Length

**Principle:** Treat strings as read-only byte sequences and use rune iteration when the unit is a Unicode code point.

**Do:**
- Use `range` to iterate decoded runes.
- Use byte indexing for protocol or binary operations.
- Expect `len(string)` to report bytes.
- Use `%#U`, `%c`, `%x`, and `%q` according to the representation needed.

**Don't:**
- Don't equate byte count with character count.
- Don't assume every byte is a printable character.
- Don't mutate strings; convert to a byte or rune slice when mutation is required.

**Code:**
```go
 s2 := "€£³"
 for x, y := range s2 {
 fmt.Printf("%#U starts at byte position %d\n",
y, x)
 }
 fmt.Printf("s2 length: %d\n", len(s2))
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Strings / What is a rune?"*

---

### 17. Parse Time with Go's Reference Layout

**Principle:** Parse and format dates with the reference values `15`, `04`, `05`, `02`, `Jan`, and `2006`, then check parsing errors.

**Do:**
- Match the layout to the exact input form.
- Use `time.Duration` constants for readable intervals.
- Use `Sub` to compare instants.
- Load locations when output belongs in another time zone.

**Don't:**
- Don't import `strftime`-style assumptions into Go layouts.
- Don't ignore `time.Parse` errors.
- Don't confuse a duration with a wall-clock timestamp.

**Code:**
```go
 d, err := time.Parse("15:04", myTime)
 if err == nil {
 fmt.Println("Full:", d)
 fmt.Println("Time:", d.Hour(), d.Minute())
 } else {
 fmt.Println(err)
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Working with times / Parsing times"*

---

### 18. Make the Pattern the Center of Regex Work

**Principle:** Define and test the grammar before trusting any data extracted by a regular expression.

**Do:**
- Model the valid domain, not merely the visual shape.
- Test false positives and false negatives.
- Use capturing groups only for data you need later.
- Validate extracted IP text again with `net.ParseIP` when correctness matters.

**Don't:**
- Don't solve every parsing task with regex.
- Don't compile an invariant regex on every call.
- Don't trust external text to contain the requested field count.

**Code:**
```go
func findIP(input string) string {
 partIP := "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?
[0-9])"
 grammar := partIP + "\\." + partIP + "\\." + partIP
+ "\\." + partIP
 matchMe := regexp.MustCompile(grammar)
 return matchMe.FindString(input)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Matching IPv4 addresses"*

---

### 19. Centralize Structure Construction and Validation

**Principle:** Construct important structures through one function when initialization needs validation or normalization.

**Do:**
- Use named fields when positional order would be obscure.
- Return a pointer when callers should share and mutate one instance.
- Return a value when copy semantics are desired.
- Keep field order stable because it contributes to type identity.

**Don't:**
- Don't spread validation across every structure literal.
- Don't use `new` when `make` is required to initialize maps, slices, or channels.
- Don't pass pointers when values are sufficient.

**Code:**
```go
func createStruct(n, s string, h int32) *myStructure {
 if h > 300 {
 h = 0
 }
 return &myStructure{n, s, h}
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Pointers to structures / Using the new keyword"*

---

### 20. Keep Functions Focused and Closures Local

**Principle:** Make each function do one job, and use anonymous functions only for small behavior with a local focus.

**Do:**
- Use multiple returns instead of temporary result structures when values naturally travel together.
- Pass functions when behavior is the variable part of an operation.
- Return closures when each returned function should retain independent state.
- Pass pointers only when mutation or identity requires them.

**Don't:**
- Don't let anonymous functions grow into hidden subsystems.
- Don't reassign function-valued variables in ways that silently change their meaning.
- Don't combine unrelated jobs in one function.

**Code:**
```go
func funReturnFun() func() int {
 i := 0
 return func() int {
 i++
 return i * i
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Anonymous functions / Functions that return other functions"*

---

### 21. Name Return Values Only When They Clarify the Contract

**Principle:** Named results can document meaning and support bare returns, but the returned state must remain obvious.

**Do:**
- Name same-typed results when their order would otherwise be ambiguous.
- Assign every named result on every branch.
- Keep functions short enough that a bare return remains readable.
- Return explicit names when it improves local clarity.

**Don't:**
- Don't rely on distant mutation of named result variables.
- Don't use bare returns in long, branching functions.
- Don't ignore conversion errors merely to populate arguments.

**Code:**
```go
func namedMinMax(x, y int) (min, max int) {
 if x > y {
 min = y
 max = x
 } else {
 min = x
 max = y
 }
 return
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The return values of a function can be named!"*

---

### 22. Build Cohesive Packages with Small Public Surfaces

**Principle:** Group related behavior, export only what callers need, and make the package fit naturally into surrounding Go code.

**Do:**
- Start exported identifiers with uppercase and private identifiers with lowercase.
- Split a package into files by related task or concept.
- Keep package names concise and expressive.
- Exercise a package internally before publishing it.
- Include tests, examples, and documentation.

**Don't:**
- Don't combine unrelated domains in one package.
- Don't export an endless list of functions.
- Don't recreate an existing package without first extending or adapting it.
- Don't break callers unnecessarily during updates.

**Code:**
```go
package aPackage
import (
 "fmt"
)
func A() {
 fmt.Println("This is function A!")
}
func B() {
 fmt.Println("privateConstant:", privateConstant)
}
const MyConstant = 123
const privateConstant = 21
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating good Go packages"*

---

### 23. Use `init` Sparingly and Know Its Order

**Principle:** Reserve `init` for unavoidable package initialization because callers cannot invoke, order, or suppress it directly.

**Do:**
- Initialize dependencies before dependent packages.
- Remember that an imported package's `init` runs once.
- Keep `init` deterministic and small.
- Prefer explicit constructors when callers should control failure and timing.

**Don't:**
- Don't put surprising external effects in a public package's `init`.
- Don't assume repeated imports repeat initialization.
- Don't require callers to understand hidden startup work.

**Code:**
```go
package a
import (
 "fmt"
)
func init() {
 fmt.Println("init() a")
}
func FromA() {
 fmt.Println("fromA()")
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The init() function"*

---

### 24. Define Interfaces Around Behavior

**Principle:** Keep interfaces small, behavioral, and close to the code that needs the abstraction.

**Do:**
- Model behavior with method signatures.
- Let types satisfy interfaces implicitly.
- Prefer single-method interfaces such as `io.Reader` and `io.Writer` when sufficient.
- Accept an interface when multiple implementations must be interchangeable.

**Don't:**
- Don't define data fields in an interface.
- Don't create an interface and its sole implementation together without questioning the abstraction.
- Don't make callers implement methods they do not need.

**Code:**
```go
package myInterface
 type Shape interface {
 Area() float64
 Perimeter() float64
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Go interfaces / Developing your own interfaces"*

---

### 25. Use the Two-Value Form of Type Assertion

**Principle:** Check a type assertion with its Boolean result unless a mismatch is a deliberate panic condition.

**Do:**
- Use `v, ok := x.(T)` for ordinary branching.
- Use a type switch when more than one concrete type is supported.
- Keep interface-to-concrete conversion close to the behavior requiring it.
- Include a default case for unsupported types.

**Don't:**
- Don't use `x.(T)` alone on untrusted dynamic values.
- Don't mistake `interface{}` for compile-time type safety.
- Don't replace a useful common interface with repetitive type tests.

**Code:**
```go
func tellInterface(x interface{}) {
 switch v := x.(type) {
 case square:
 fmt.Println("This is a square!")
 case circle:
 fmt.Printf("%v is a circle!\n", v)
 case rectangle:
 fmt.Println("This is a rectangle!")
 default:
 fmt.Printf("Unknown type %T!\n", v)
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "About type assertion / Using switch with interface and data types"*

---

### 26. Reach for Reflection Only for Unknown Types

**Principle:** Use reflection when code must inspect types or values unavailable at compile time, not as a substitute for ordinary typed code.

**Do:**
- Use `reflect.TypeOf` for dynamic type information.
- Use `reflect.ValueOf` when field values or methods must be inspected.
- Pass a pointer and call `Elem` when fields must be changed.
- Test every reflective path thoroughly.

**Don't:**
- Don't use reflection when an interface or concrete type solves the problem.
- Don't accept runtime panics that static typing could prevent.
- Don't ignore reflection's runtime and maintenance cost.

**Code:**
```go
func printMethods(i interface{}) {
 r := reflect.ValueOf(i)
 t := r.Type()
 fmt.Printf("Type to examine: %s\n", t)
 for j := 0; j < r.NumMethod(); j++ {
 m := r.Method(j).Type()
 fmt.Println(t.Method(j).Name, "-->", m)
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reflection / The three disadvantages of reflection"*

---

### 27. Use Templates to Separate Data from Presentation

**Principle:** Keep formatting in templates and typed data preparation in Go.

**Do:**
- Use `text/template` for composable plain-text output.
- Use `html/template` for HTML and its injection protections.
- Use external template files for substantial layouts.
- Parse once when repeated execution does not require reparsing.
- Execute into an `io.Writer`.

**Don't:**
- Don't generate HTML with `text/template` when `html/template` fits.
- Don't intermix both packages without import aliases.
- Don't bury a large presentation in `fmt.Fprintf` calls.

**Code:**
```go
 t := template.Must(template.ParseGlob(tFile))
 t.Execute(os.Stdout, Entries)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Text and HTML templates / Generating text output"*

---

### 28. Prefer Built-In Structures Until Requirements Demand Custom Ones

**Principle:** Use maps, slices, arrays, and `container` implementations before paying for custom data-structure complexity.

**Do:**
- Choose by operation complexity and data shape.
- Use balanced trees for hierarchical ordered search.
- Use hash tables for average constant-time key lookup.
- Use queues for FIFO and stacks for LIFO.
- Use `container/list`, `container/heap`, or `container/ring` when their contract fits.

**Don't:**
- Don't implement a custom structure merely for novelty.
- Don't ignore balancing when tree performance matters.
- Don't lose the head pointer of a singly linked list.
- Don't iterate a ring without an explicit stopping rule.

**Code:**
```go
type Tree struct {
 Left *Tree
 Value int
 Right *Tree
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Enhancing Go Code with Data Structures"*

---

### 29. Seed Pseudorandom Generators According to the Use Case

**Principle:** Use reproducible seeds for tests, changing seeds for simulations, and `crypto/rand` for security-sensitive values.

**Do:**
- Call `rand.Seed` before using the package-level pseudorandom generator.
- Preserve a seed when a failing sequence must be reproduced.
- Constrain `rand.Intn` to a valid positive range.
- Use cryptographically secure randomness for secrets.

**Don't:**
- Don't mistake `math/rand` output for secure password material.
- Don't always seed identically when variation is required.
- Don't discard numeric parsing errors in a production random-data CLI.

**Code:**
```go
func random(min, max int) int {
 return rand.Intn(max-min) + min
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Generating random numbers"*

---

### 30. Parse Nontrivial CLIs with `flag`

**Principle:** Let the standard `flag` package parse, validate, order, and document command-line options.

**Do:**
- Define all flags before parsing.
- Always call `flag.Parse()`.
- Dereference the pointers returned by flag constructors.
- Read remaining operands with `flag.Args()`.
- Supply useful usage strings.

**Don't:**
- Don't hand-roll option parsing for a utility with multiple flags.
- Don't assume Boolean flags consume a following token in every form.
- Don't ignore the package's generated error and usage output.

**Code:**
```go
func main() {
 minusK := flag.Bool("k", true, "k")
 minusO := flag.Int("O", 1, "O")
 flag.Parse()
 valueK := *minusK
 valueO := *minusO
 valueO++
 fmt.Println("-k:", valueK)
 fmt.Println("-O:", valueO)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The flag package"*

---

### 31. Implement `flag.Value` for Domain-Specific Options

**Principle:** Encapsulate custom option parsing behind `String` and `Set` instead of leaking parsing into `main`.

**Do:**
- Implement both methods of `flag.Value`.
- Return an error for invalid or repeated values.
- Parse a multi-value option once into a typed field.
- Expose the parsed value through a focused method.

**Don't:**
- Don't silently accept duplicate flags when only one occurrence is valid.
- Don't postpone validation until business logic executes.
- Don't parse custom options from `os.Args` after `flag.Parse` already modeled them.

**Code:**
```go
func (s *NamesFlag) Set(v string) error {
 if len(s.Names) > 0 {
 return fmt.Errorf("Cannot use names flag more
than once!")
 }
 names := strings.Split(v, ",")
 for _, item := range names {
 s.Names = append(s.Names, item)
 }
 return nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The flag package"*

---

### 32. Program Against `io.Reader` and `io.Writer`

**Principle:** Express streaming code through `Read` and `Write` contracts so files, memory, standard streams, and network connections compose.

**Do:**
- Accept an `io.Reader` when the source does not matter.
- Accept an `io.Writer` when the destination does not matter.
- Use `io.Copy` for straightforward stream transfer.
- Wrap with `bufio.Reader` or `bufio.Writer` when buffering is useful.

**Don't:**
- Don't require `*os.File` when any reader or writer would work.
- Don't duplicate copy loops provided by `io.Copy`.
- Don't forget that buffering changes visibility and durability timing.

**Code:**
```go
type Reader interface {
 Read(p []byte) (n int, err error)
}
type Writer interface {
 Write(p []byte) (n int, err error)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The io.Reader and io.Writer interfaces"*

---

### 33. Read Text Line by Line with Explicit EOF Handling

**Principle:** Open once, defer close after success, and distinguish `io.EOF` from other read errors.

**Do:**
- Create one buffered reader per opened file.
- Use `ReadString('\n')` for newline-delimited text.
- Return open errors to the caller.
- Preserve or deliberately handle the final unterminated line.

**Don't:**
- Don't defer `Close` before confirming `Open` succeeded.
- Don't print a second newline when the read line already includes one.
- Don't treat every error as EOF.

**Code:**
```go
func lineByLine(file string) error {
 var err error
 f, err := os.Open(file)
 if err != nil {
 return err
 }
 defer f.Close()
 r := bufio.NewReader(f)
 for {
 line, err := r.ReadString('\n')
 if err == io.EOF {
 break
 } else if err != nil {
 fmt.Printf("error reading file %s", err)
 break
 }
 fmt.Print(line)
 }
 return nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading a text file line by line"*

---

### 34. Slice Reads to the Number of Bytes Actually Returned

**Principle:** Use the `n` returned by `Read`; the allocated buffer length is not the amount of valid data.

**Do:**
- Allocate a buffer for the maximum chunk.
- Return or process `buffer[:n]`.
- Treat EOF as normal termination.
- Use binary encoding when representation size matters.

**Don't:**
- Don't process stale bytes beyond `n`.
- Don't assume every read fills the buffer.
- Don't print the whole buffer on the final partial read.

**Code:**
```go
func readSize(f *os.File, size int) []byte {
 buffer := make([]byte, size)
 n, err := f.Read(buffer)
 if err == io.EOF {
 return nil
 }
 if err != nil {
 fmt.Println(err)
 return nil
 }
 return buffer[0:n]
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading the amount of data you want from a file"*

---

### 35. Decode Binary and CSV Data with Format-Aware Packages

**Principle:** Use `encoding/binary` and `encoding/csv` rather than parsing structured bytes or delimited records by hand.

**Do:**
- Select the correct byte order before decoding binary values.
- Pass a pointer to the destination of `binary.Read`.
- Configure `FieldsPerRecord` intentionally.
- Check `ReadAll`, record width, and numeric conversion errors.

**Don't:**
- Don't assume host endianness matches the data source.
- Don't index CSV records before validating their fields.
- Don't discard malformed numeric fields silently.

**Code:**
```go
 var seed int64
 binary.Read(f, binary.LittleEndian, &seed)
 fmt.Println("Seed:", seed)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading from /dev/random / Reading CSV files"*

---

### 36. Flush Buffered Writers and Check Write Results

**Principle:** Buffer repeated writes for throughput, but flush and propagate every error before reporting success.

**Do:**
- Create files with deliberate permissions.
- Defer the file close after successful creation.
- Call `Flush` on a `bufio.Writer`.
- Check returned byte counts and errors.
- Benchmark buffer sizes for the actual workload.

**Don't:**
- Don't assume `WriteString` wrote everything successfully.
- Don't exit with unwritten buffered data.
- Don't choose one-byte buffers for high-volume output.

**Code:**
```go
 f3, err := os.Create("f3.txt")
 if err != nil {
 fmt.Println(err)
 return
 }
 w := bufio.NewWriter(f3)
 n, err = w.WriteString(string(s))
 fmt.Printf("wrote %d bytesn", \n)
 w.Flush()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Writing to a file"*

---

### 37. Serialize Go-Owned State with `encoding/gob`

**Principle:** Use gob for Go-to-Go persistence when language portability is not required; use JSON or XML when it is.

**Do:**
- Encode through a file-backed `gob.Encoder`.
- Decode into a pointer with `gob.Decoder`.
- Check open, encode, decode, close, and replacement errors.
- Decide explicitly when state should load and save.

**Don't:**
- Don't defer `Close` on a nil file after a failed open.
- Don't overwrite the only valid state before a replacement is safely encoded.
- Don't choose gob for consumers written in other languages.

**Code:**
```go
func load() error {
 fmt.Println("Loading", DATAFILE)
 loadFrom, err := os.Open(DATAFILE)
 defer loadFrom.Close()
 if err != nil {
 fmt.Println("Empty key/value store!")
 return err
 }
 decoder := gob.NewDecoder(loadFrom)
 decoder.Decode(&DATA)
 return nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Loading and saving data on disk"*

---

### 38. Use `strings.Reader` and `bytes.Buffer` as Stream Adapters

**Principle:** Convert in-memory strings and bytes into standard stream interfaces instead of creating special-case APIs.

**Do:**
- Use `strings.NewReader` for read-only string data.
- Use `bytes.Buffer` as both writer and reader-backed storage.
- Use `Reset` before reusing a buffer.
- Remember that `WriteTo` drains a buffer.

**Don't:**
- Don't expect a second `WriteTo` to repeat drained content.
- Don't allocate files merely to satisfy a reader API.
- Don't ignore partial reads from a `bytes.Reader`.

**Code:**
```go
 var buffer bytes.Buffer
 buffer.Write([]byte("This is"))
 fmt.Fprintf(&buffer, " a string!\n")
 buffer.WriteTo(os.Stdout)
 buffer.WriteTo(os.Stdout)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The strings package revisited / About the bytes package"*

---

### 39. Inspect File Types and Permissions Through `os.FileMode`

**Principle:** Use `os.Stat` and `FileMode` to classify files and inspect permissions rather than parsing shell output.

**Do:**
- Check the `os.Stat` error.
- Use `Mode().IsRegular()` and `Mode().IsDir()` for classification.
- Apply explicit creation modes such as `0600` or `0644` according to policy.
- Distinguish permission bits from type bits.

**Don't:**
- Don't index `mode.String()` after an unchecked `Stat` failure.
- Don't treat devices, sockets, links, and regular files as identical.
- Don't assume Unix permission semantics are fully portable.

**Code:**
```go
 filename := arguments[1]
 info, _ := os.Stat(filename)
 mode := info.Mode()
 fmt.Println(filename, "mode is", mode.String()
[1:10])
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "File permissions"*

---

### 40. Handle Unix Signals Through a Channel

**Principle:** Register signal delivery to a buffered channel and centralize asynchronous policy in one dispatch loop.

**Do:**
- Use `signal.Notify` with the signals the process supports.
- Use one signal such as `SIGTERM` for orderly termination.
- Put signal-specific behavior in a `switch`.
- Remember that `SIGKILL` and `SIGSTOP` cannot be handled.

**Don't:**
- Don't assume every named signal exists on every Unix variant.
- Don't perform unsafe, scattered shutdown work from unrelated goroutines.
- Don't expect ignored signals to appear in a narrowly registered channel.

**Code:**
```go
 sigs := make(chan os.Signal, 1)
 signal.Notify(sigs)
 go func() {
 for {
 sig := <-sigs
 switch sig {
 case os.Interrupt:
 handle(sig)
 case syscall.SIGTERM:
 handle(sig)
 os.Exit(0)
 case syscall.SIGUSR2:
 fmt.Println("Handling
syscall.SIGUSR2!")
 default:
 fmt.Println("Ignoring:", sig)
 }
 }
 }()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Handling all signals"*

---

### 41. Make CLI Tools Compose Through Unix Pipes

**Principle:** Read standard input when no file operand is given and write primary data to standard output.

**Do:**
- Use `io.Copy(os.Stdout, os.Stdin)` for transparent pass-through.
- Process multiple file operands in order.
- Report per-file errors without necessarily abandoning later files.
- Keep each utility focused on one transformation.

**Don't:**
- Don't require temporary files between composable tools.
- Don't send diagnostics into pipeline data.
- Don't make a simple stream copy more complicated than `io.Copy`.

**Code:**
```go
func main() {
 filename := ""
 arguments := os.Args
 if len(arguments) == 1 {
 io.Copy(os.Stdout, os.Stdin)
 return
 }
 for i := 1; i < len(arguments); i++ {
 filename = arguments[i]
 err := printFile(filename)
 if err != nil {
 fmt.Println(err)
 }
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Programming Unix pipes in Go / Implementing the cat(1) utility in Go"*

---

### 42. Traverse Directory Trees with a Focused Walk Function

**Principle:** Put classification policy in the `filepath.Walk` callback and propagate traversal failures.

**Do:**
- Inspect each path's mode.
- Return errors that should stop traversal.
- Keep flag-derived display policy explicit.
- Start at a caller-selected root.

**Don't:**
- Don't assume every visited path is a regular file or directory.
- Don't ignore sockets and symbolic links accidentally.
- Don't perform an unchecked second `os.Stat` if supplied walk information is sufficient.

**Code:**
```go
func walk(path string, info os.FileInfo, err error)
error {
 fileInfo, err := os.Stat(path)
 if err != nil {
 return err
 }
 mode := fileInfo.Mode()
 if mode.IsRegular() && minusF {
 fmt.Println("+", path)
 return nil
 }
 if mode.IsDir() && minusD {
 fmt.Println("*", path)
 return nil
 }
 fmt.Println(path)
 return nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Traversing directory trees"*

---

### 43. Use System-Call Tools Before Adding Debug Code

**Principle:** Diagnose process/kernel interaction with `strace`, `dtrace`, `dtruss`, or ptrace-based tools when ordinary logs do not explain behavior.

**Do:**
- Build the target first to avoid tracing `go run` compilation noise.
- Count calls and time to identify expensive syscall patterns.
- Use Linux-specific ptrace functionality only on supported systems.
- Compare custom tracing results with established tools.

**Don't:**
- Don't assume syscall numbers are portable across Unix variants.
- Don't ship a low-level tracer without explicit platform constraints.
- Don't reach for ptrace when profiling or application logs answer the question.

**Code:**
```go
 cmd := exec.Command(os.Args[1], os.Args[2:]...)
 cmd.Stdout = os.Stdout
 cmd.Stderr = os.Stderr
 cmd.SysProcAttr = &syscall.SysProcAttr{Ptrace:
true}
 err := cmd.Start()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Two handy Unix utilities / About syscall.PtraceRegs / Tracing system calls"*

---

### 44. Design for Concurrency, Not Merely Parallel Execution

**Principle:** Decompose work into independent components first; parallel execution is a possible consequence of a sound concurrent design.

**Do:**
- Identify tasks that can progress independently.
- Define explicit fork and join points.
- Use concurrency to improve structure even on one processor.
- Let measured workload determine whether additional parallelism helps.

**Don't:**
- Don't equate concurrency with simultaneous execution.
- Don't add goroutines to code that has no independent work.
- Don't assume more goroutines always improve throughput.

**Code:**
```go
go function()
go func() {
 for i := 10; i < 20; i++ {
 fmt.Print(i, " ")
 }
}()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Concurrency and parallelism / Goroutines"*

---

### 45. Make Goroutine Lifetimes Explicit

**Principle:** Every goroutine needs a known completion, cancellation, or process-lifetime policy.

**Do:**
- Prefer a named function when goroutine work is substantial.
- Pass loop values as parameters to the closure.
- Define how the caller observes completion.
- Define how blocked I/O or channel operations terminate.

**Don't:**
- Don't assume goroutines finish before `main` returns.
- Don't rely on output order.
- Don't use `time.Sleep` as a lifecycle protocol.
- Don't capture a changing loop variable unintentionally.

**Code:**
```go
 for i := 0; i < count; i++ {
 go func(x int) {
 fmt.Printf("%d ", x)
 }(i)
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating multiple goroutines"*

---

### 46. Pair Every `WaitGroup.Add` with One `Done`

**Principle:** Increment the group before spawning, defer one decrement in the worker, and wait only after all planned increments.

**Do:**
- Call `Add(1)` before the `go` statement.
- Put `defer waitGroup.Done()` at the start of the goroutine.
- Audit dynamic branches so every accepted job decrements once.
- Treat `Wait` as the join point.

**Don't:**
- Don't copy a `WaitGroup` after first use.
- Don't add fewer tasks than call `Done`.
- Don't add more tasks than can finish.
- Don't call `Add` after a concurrent `Wait` has made lifecycle ambiguous.

**Code:**
```go
 for i := 0; i < count; i++ {
 waitGroup.Add(1)
 go func(x int) {
 defer waitGroup.Done()
 fmt.Printf("%d ", x)
 }(i)
 }
 waitGroup.Wait()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Waiting for your goroutines to finish"*

---

### 47. Use Unbuffered Channels for Synchronous Handoffs

**Principle:** An unbuffered send and receive rendezvous, so each side must have a matching participant.

**Do:**
- Create channels with `make`.
- Match the channel element type to transferred data.
- Recognize that a send blocks until a receiver participates.
- Use the two-value receive form when open/closed state matters.

**Don't:**
- Don't send when no receiver can run.
- Don't assume a send queues automatically.
- Don't use a nil channel unless permanent blocking or select disabling is intentional.

**Code:**
```go
func writeToChannel(c chan int, x int) {
 fmt.Println(x)
 c <- x
 close(c)
 fmt.Println(x)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Writing to a channel / Reading from a channel"*

---

### 48. Give Channel Ownership to the Sender

**Principle:** The producer that knows no more values will arrive should close the channel; receivers should observe closure.

**Do:**
- Close output after the final send.
- Receive with `value, ok := <-ch` when zero values are ambiguous.
- Range over a channel until it closes.
- Close each pipeline stage's outbound channel.

**Don't:**
- Don't send to a closed channel.
- Don't close a nil channel.
- Don't close the same channel from multiple goroutines.
- Don't treat a zero value from a closed channel as ordinary data without checking `ok`.

**Code:**
```go
 _, ok := <-c
 if ok {
 fmt.Println("Channel is open!")
 } else {
 fmt.Println("Channel is closed!")
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading from a channel / Go channels revisited"*

---

### 49. Encode Channel Direction in Function Signatures

**Principle:** Restrict parameters to send-only or receive-only channels whenever their role is known.

**Do:**
- Use `chan<- T` for producers.
- Use `<-chan T` for consumers.
- Let the compiler reject reversed operations.
- Make bidirectional channels only where both operations are part of the contract.

**Don't:**
- Don't expose more channel capability than a function needs.
- Don't close a receive-only channel.
- Don't read from a send-only channel.

**Code:**
```go
func f1(out chan<- int64, in <-chan int64) {
 fmt.Println(x)
 c <- x
}
func f2(out chan int64, in chan int64) {
 fmt.Println(x)
 c <- x
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Channels as function parameters"*

---

### 50. Build Pipelines with Stage-Local Responsibilities

**Principle:** Let each stage read one input, perform one transformation, and close its own output when complete.

**Do:**
- Type stage inputs as receive-only and outputs as send-only.
- Range over incoming values.
- Filter by choosing whether to send downstream.
- Keep a final synchronous stage when it should hold `main` open.

**Don't:**
- Don't leave downstream stages waiting on an output never closed.
- Don't use shared flags when a channel can carry termination cleanly.
- Don't accumulate every intermediate value if streaming suffices.

**Code:**
```go
func third(in <-chan int) {
 var sum int
 sum = 0
 for x2 := range in {
 sum = sum + x2
 }
 fmt.Printf("The sum of the random numbers is %d\n",
sum)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Pipelines"*

---

### 51. Understand the Scheduler's M:G:P Model

**Principle:** Diagnose scheduling in terms of goroutines, OS threads, logical processors, local queues, the global queue, and work stealing.

**Do:**
- Treat goroutines as scheduled tasks, not OS threads.
- Remember that processors own local run queues.
- Recognize that idle processors steal continuations.
- Account for synchronization and scheduling overhead.

**Don't:**
- Don't assume goroutine count equals OS-thread count.
- Don't set `GOMAXPROCS` above CPU count and assume a speedup.
- Don't add scheduling work without benchmarking.

**Code:**
```go
func getGOMAXPROCS() int {
 return runtime.GOMAXPROCS(0)
}
func main() {
 fmt.Printf("GOMAXPROCS: %d\n", getGOMAXPROCS())
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The Go scheduler revisited / The GOMAXPROCS environment variable"*

---

### 52. Orchestrate Multiple Channel Operations with `select`

**Principle:** Use `select` to wait on competing communications without imposing source-order priority.

**Do:**
- Include only operations that may legitimately proceed.
- Expect blocking when no case is ready and no default exists.
- Expect a pseudo-random choice when several cases are ready.
- Add a timeout case when indefinite waiting is unacceptable.

**Don't:**
- Don't read `select` as a sequential switch.
- Don't add `default` when backpressure is required.
- Don't overlook deadlock paths across the connected channels.

**Code:**
```go
 select {
 case createNumber <- rand.Intn(max-min) + min:
 case <-end:
 close(end)
 return
 case <-time.After(4 * time.Second):
 fmt.Println("n\time.After()!")
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The select keyword"*

---

### 53. Bound Waiting with a Timeout Case

**Principle:** Pair the result channel with `time.After` when a goroutine may take longer than the caller can wait.

**Do:**
- Choose a duration from service requirements.
- Return a distinct timeout outcome.
- Ensure timed-out workers can eventually terminate or be canceled.
- Prefer context when cancellation must propagate across API boundaries.

**Don't:**
- Don't choose a timeout so short that valid work fails routinely.
- Don't mistake caller timeout for worker cancellation.
- Don't leak a goroutine blocked forever trying to send a late result.

**Code:**
```go
select {
 case res := <-c1:
 fmt.Println(res)
 case <-time.After(time.Second * 1):
 fmt.Println("timeout c1")
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Timing out a goroutine – take 1"*

---

### 54. Use Buffered Channels to Bound In-Flight Work

**Principle:** Treat capacity as an explicit limit on queued or admitted work, not as a way to conceal missing receivers.

**Do:**
- Pick capacity from resource constraints.
- Use nonblocking `select` only when dropping or rejecting is valid.
- Inspect `cap` when explaining configured limits.
- Close the jobs channel after production ends.

**Don't:**
- Don't assume a bigger buffer always makes a system faster.
- Don't discard work through `default` without policy.
- Don't confuse buffering with additional workers.

**Code:**
```go
 numbers := make(chan int, 5)
 counter := 10
for i := 0; i < counter; i++ {
 select {
 case numbers <- i:
 default:
 fmt.Println("Not enough space for", i)
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Buffered channels"*

---

### 55. Disable `select` Cases with Nil Channels

**Principle:** Assign `nil` to a channel variable when its `select` branch must become permanently ineligible.

**Do:**
- Use nil assignment to retire an input after a state transition.
- Keep the other cases capable of making progress.
- Distinguish a nil channel from a closed channel.
- Make the state transition visible near the select.

**Don't:**
- Don't send to or receive from a nil channel outside a select expecting progress.
- Don't close a nil channel.
- Don't leave a loop with every select case disabled.

**Code:**
```go
func add(c chan int) {
 sum := 0
 t := time.NewTimer(time.Second)
 for {
 select {
 case input := <-c:
 sum = sum + input
 case <-t.c:
 c = nil
 fmt.Println(sum)
 }
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Nil channels"*

---

### 56. Use Channels of Channels Only for Dynamic Reply Paths

**Principle:** Pass a channel through a channel only when participants must exchange a communication endpoint dynamically.

**Do:**
- Declare the nested element type explicitly.
- Use a separate signal channel for cancellation when needed.
- Close the inner channel at the goroutine that owns its sends.
- Prefer a simpler result channel when dynamic routing is unnecessary.

**Don't:**
- Don't introduce channel-of-channel complexity for ordinary request/result work.
- Don't lose ownership of inner-channel closure.
- Don't use a data-carrying Boolean channel when `struct{}` communicates only a signal.

**Code:**
```go
func f1(cc chan chan int, f chan bool) {
 c := make(chan int)
 cc <- c
 defer close(c)
 sum := 0
 select {
 case x := <-c:
 for i := 0; i <= x; i++ {
 sum = sum + i
 }
 c <- sum
 case <-f:
 return
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Channel of channels"*

---

### 57. Sequence Goroutines with Closed Signal Channels

**Principle:** Close zero-data channels to establish explicit happens-before ordering between stages.

**Do:**
- Use `chan struct{}` for pure notification.
- Block each stage on its predecessor's channel.
- Let one owner close each signal channel exactly once.
- Close the first signal to start the chain.

**Don't:**
- Don't close the same channel from duplicate goroutines.
- Don't assume launch order is execution order.
- Don't put payloads in a signal-only protocol.

**Code:**
```go
func A(a, b chan struct{}) {
 <-a
 fmt.Println("A()!")
 time.Sleep(time.Second)
 close(b)
}
func B(a, b chan struct{}) {
 <-a
 fmt.Println("B()!")
 close(b)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Specifying the order of execution for your goroutines"*

---

### 58. Protect the Smallest Critical Section with `sync.Mutex`

**Principle:** Lock only the shared state transition that must be exclusive and make unlock unavoidable.

**Do:**
- Identify critical sections before adding locks.
- Lock before the first conflicting access.
- Use `defer Unlock()` when early returns could bypass release.
- Keep the mutex and protected state close together.

**Don't:**
- Don't spread one mutex across opaque call chains.
- Don't nest critical sections guarded by the same non-reentrant mutex.
- Don't forget to unlock.
- Don't copy a mutex after use.

**Code:**
```go
func change(i int) {
 m.Lock()
 time.Sleep(time.Second)
 v1 = v1 + 1
 if v1%10 == 0 {
 v1 = v1 - 10*i
 }
 m.Unlock()
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The sync.Mutex type"*

---

### 59. Use `sync.RWMutex` for Read-Dominated Shared State

**Principle:** Permit concurrent readers with `RLock` while preserving exclusive writers with `Lock`.

**Do:**
- Pair `RLock` with `RUnlock`.
- Pair `Lock` with `Unlock`.
- Keep read sections free of mutation.
- Benchmark against a plain mutex for the actual read/write ratio.

**Don't:**
- Don't expect a writer to proceed while readers hold the lock.
- Don't use `RWMutex` automatically for every shared value.
- Don't mutate under `RLock`.

**Code:**
```go
func show(c *secret) string {
 c.RWM.RLock()
 fmt.Print("show")
 time.Sleep(3 * time.Second)
 defer c.RWM.RUnlock()
 return c.password
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The sync.RWMutex type"*

---

### 60. Prefer a Monitor Goroutine for Complex Shared State

**Principle:** Give one goroutine ownership of mutable state and expose reads and writes through channels.

**Do:**
- Keep the owned value local to the monitor.
- Separate read requests from write requests.
- Use one `select` to serialize state transitions.
- Wrap channel operations in focused API functions.

**Don't:**
- Don't allow other goroutines to mutate the owned value directly.
- Don't combine monitor ownership with unsynchronized side access.
- Don't use a mutex merely because shared memory is familiar.

**Code:**
```go
func monitor() {
 var value int
 for {
 select {
 case newValue := <-writeValue:
 value = newValue
 fmt.Printf("%d ", value)
 case readValue <- value:
 }
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Sharing memory using goroutines"*

---

### 61. Run the Race Detector on Concurrent Code

**Principle:** Treat every unsynchronized conflicting memory access as a defect and use `-race` to reveal executed races.

**Do:**
- Run `go run -race`, `go build -race`, or race-enabled tests.
- Read both current and previous access stacks.
- Pass loop indices into goroutine parameters.
- Synchronize maps around every conflicting access.

**Don't:**
- Don't trust apparently correct output from one run.
- Don't write maps from multiple goroutines without coordination.
- Don't interpret a clean race run as proof of unexecuted paths.

**Code:**
```go
 for i = 0; i < numGR; i++ {
 waitGroup.Add(1)
 go func(j int) {
 defer waitGroup.Done()
 aMutex.Lock()
 k[j] = j
 aMutex.Unlock()
 }(i)
 }
 waitGroup.Wait()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Catching race conditions"*

---

### 62. Propagate Cancellation with `context.Context`

**Principle:** Carry cancellation and deadlines through a context tree and always release derived-context resources.

**Do:**
- Begin with `context.Background()` at the top level.
- Derive with `WithCancel`, `WithTimeout`, or `WithDeadline`.
- Call the returned cancel function, usually with `defer`.
- Select on `ctx.Done()` and inspect `ctx.Err()`.

**Don't:**
- Don't implement the `Context` interface yourself for ordinary use.
- Don't use context values as a general mutable parameter bag.
- Don't create a timeout without arranging for blocked work to observe it.

**Code:**
```go
 c2 := context.Background()
 c2, cancel := context.WithTimeout(c2,
time.Duration(t)*time.Second)
 defer cancel()
 go func() {
 time.Sleep(4 * time.Second)
 cancel()
 }()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The context package"*

---

### 63. Couple HTTP Cancellation to the Actual Request

**Principle:** A request timeout must cancel the transport operation, not merely stop waiting for its answer.

**Do:**
- Keep response and error together on one result channel.
- Cancel the in-flight request when the context ends.
- Drain the goroutine's result path when required for cleanup.
- Close response bodies after successful requests.

**Don't:**
- Don't leave a transport request running after caller cancellation.
- Don't read a nil response body after an error.
- Don't forget the worker's `WaitGroup.Done`.

**Code:**
```go
 select {
 case <-c.Done():
 tr.CancelRequest(req)
 <-data
 fmt.Println("The request was cancelled!")
 return c.Err()
 case ok := <-data:
 err := ok.err
 resp := ok.r
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "An advanced example of the context package"*

---

### 64. Bound Concurrency with a Worker Pool

**Principle:** Feed a fixed set of workers from a jobs channel and close result flow only after every worker exits.

**Do:**
- Model jobs and results as explicit types.
- Close the jobs channel after production.
- Range over jobs in each worker.
- Wait for all workers before closing results.
- Consume results concurrently when workers may block on result sends.

**Don't:**
- Don't launch one unbounded goroutine for every request by default.
- Don't close results while a worker can still send.
- Don't leave workers waiting on a jobs channel that never closes.

**Code:**
```go
func makeWP(n int) {
 var w sync.WaitGroup
 for i := 0; i < n; i++ {
 w.Add(1)
 go worker(&w)
 }
 w.Wait()
 close(data)
}
func create(n int) {
 for i := 0; i < n; i++ {
 c := Client{i, i}
 clients <- c
 }
 close(clients)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Worker pools"*

---

### 65. Optimize Correct Code Only

**Principle:** Establish correctness, profile the real workload, and optimize the measured bottleneck rather than the first visible loop.

**Do:**
- Test before optimizing.
- Start with frequently executed or profile-dominant functions.
- Compare algorithms before micro-optimizing syntax.
- Re-measure after every change.

**Don't:**
- Don't optimize a bug.
- Don't optimize the first version prematurely.
- Don't infer bottlenecks from intuition alone.
- Don't benchmark on a busy machine without a reason.

**Code:**
```go
func N1(n int) bool {
 k := math.Floor(float64(n/2 + 1))
 for i := 2; i < int(k); i++ {
 if (n % i) == 0 {
 return false
 }
 }
 return true
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "About optimization / Optimizing Go code"*

---

### 66. Capture CPU and Heap Profiles Deliberately

**Principle:** Profile one resource dimension at a time and collect enough representative work for useful samples.

**Do:**
- Start CPU profiling after opening the profile file.
- Defer `pprof.StopCPUProfile()`.
- Write a heap profile after the workload of interest.
- Use `top`, cumulative views, and `list` to localize cost.
- Use the web UI when graph and source views help.

**Don't:**
- Don't expect useful samples from a program that ends too quickly.
- Don't combine CPU and memory profiling in normal analysis without considering interference.
- Don't optimize functions absent from the profile.

**Code:**
```go
 cpuFile, err := os.Create("/tmp/cpuProfile.out")
 if err != nil {
 fmt.Println(err)
 return
 }
 pprof.StartCPUProfile(cpuFile)
 defer pprof.StopCPUProfile()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Profiling Go code / A simple profiling example"*

---

### 67. Use Execution Tracing for Scheduler and GC Questions

**Principle:** Use `runtime/trace` when the question concerns goroutine blocking, syscalls, processor activity, heap changes, or GC timing.

**Do:**
- Create a trace output file.
- Start tracing before the workload.
- Defer `trace.Stop()` and file closure.
- View the trace with `go tool trace`.
- Use pprof instead when the question is per-function resource cost.

**Don't:**
- Don't treat tracing and CPU profiling as interchangeable.
- Don't omit trace shutdown.
- Don't expect the trace viewer to solve every performance issue.

**Code:**
```go
 f, err := os.Create("/tmp/traceFile.out")
 if err != nil {
 panic(err)
 }
 defer f.Close()
 err = trace.Start(f)
 if err != nil {
 fmt.Println(err)
 return
 }
 defer trace.Stop()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The go tool trace utility"*

---

### 68. Follow Go's Test Discovery Conventions

**Principle:** Put automated checks in `_test.go` files and name test functions `TestXxx(*testing.T)` so `go test` can discover them.

**Do:**
- Keep test code separate from production code.
- Cover normal, boundary, empty, and erroneous inputs.
- Use `t.Error` to continue collecting failures.
- Use `-run` to select tests and `-v` for detailed output.

**Don't:**
- Don't modify production code merely to make the test runner find tests.
- Don't infer bug absence from passing tests.
- Don't rely on cached results when the environment itself is under test.

**Code:**
```go
func TestS2(t *testing.T) {
 if s2("123456789") != 9 {
 t.Error(`s2("123456789") != 9`)
 }
 if s2("") != 0 {
 t.Error(`s2("") != 0`)
 }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Testing Go code / Writing tests for existing Go code"*

---

### 69. Benchmark Stable Workloads with `testing.B`

**Principle:** Keep the problem size fixed while the framework varies `b.N`, and make benchmark results observable to the compiler.

**Do:**
- Name entry points `BenchmarkXxx`.
- Put only the measured operation inside the `b.N` loop.
- Store results in a package-level variable when needed to prevent elimination.
- Run with `go test -bench=.`.
- Add `-benchmem` to measure allocations.

**Don't:**
- Don't make input complexity grow with `b.N`.
- Don't omit `-bench` and expect benchmarks to run.
- Don't compare results collected under materially different machine loads.

**Code:**
```go
var result int
func benchmarkfibo1(b *testing.B, n int) {
 var r int
 for i := 0; i < b.N; i++ {
 r = fibo1(n)
 }
 result = r
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A simple benchmarking example / A wrong benchmark function"*

---

### 70. Benchmark I/O Buffer Sizes Instead of Guessing

**Principle:** Measure throughput and allocations across realistic buffer sizes to find the useful range rather than maximizing blindly.

**Do:**
- Expose buffer and file size as function parameters.
- Benchmark the same file size at several buffer sizes.
- Include allocation results.
- Remove generated artifacts between benchmark cases.

**Don't:**
- Don't measure setup unrelated to the operation if it can be excluded.
- Don't conclude that a 100-times larger buffer yields a 100-times speedup.
- Don't design a function around globals that prevent controlled benchmarks.

**Code:**
```go
func Benchmark1Create(b *testing.B) {
 benchmarkCreate(b, 1, 1000000)
}
func Benchmark2Create(b *testing.B) {
 benchmarkCreate(b, 2, 1000000)
}
func Benchmark1000Create(b *testing.B) {
 benchmarkCreate(b, 1000, 1000000)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Benchmarking buffered writing"*

### 71. Make Examples Executable Documentation

**Principle:** Use `ExampleXxx` functions and `// Output:` assertions to keep usage documentation synchronized with behavior.

**Do:**
- Put examples in `_test.go` files.
- Give examples no parameters or return values.
- Print the documented result.
- Include exact expected output when the example should be tested.

**Don't:**
- Don't publish examples that are never exercised.
- Don't make output nondeterministic when an output assertion is present.
- Don't let documentation drift from production behavior.

**Code:**
```go
func ExampleF1() {
 fmt.Println(F1(10))
 fmt.Println(F1(2))
 // Output:
 // 55
 // 1
}
```

*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating example functions"*

---

### 72. Generate Documentation from Declaration Comments
**Principle:** Put meaningful comments immediately before top-level declarations and let Go tooling assemble package documentation.

**Do:**
- Describe purpose and decisions rather than restating syntax.
- Make the first package documentation line complete and descriptive.
- Attach examples to the documented identifiers.
- Use `BUG(name)` comments for known defects that belong in generated docs.

**Don't:**
- Don't document obvious variable creation.
- Don't place important declaration documentation where godoc will omit it.
- Don't treat examples as a substitute for explaining constraints.

**Code:**
```go
// The S1() function finds the length of a string
// It iterates over the string using range
func S1(s string) int {
 if s == "" {
 return 0
 }
 n := 0
 for range s {
 n++
 }
 return n
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Generating documentation"*

---

### 73. Find Unreachable Code with Static Tools

**Principle:** Run vet-style analysis because valid syntax and successful execution do not prove every statement is reachable.

**Do:**
- Run the compiler and tests first.
- Run `go tool vet` to catch supported unreachable cases.
- Review constant conditions and statements after returns manually.
- Remove unused functions and dead branches.

**Don't:**
- Don't assume the compiler reports every logical dead path.
- Don't assume vet catches every constant-condition case.
- Don't retain dead code as undocumented future intent.

**Code:**
```go
func f1() int {
 fmt.Println("Entering f1()")
 return -10
 fmt.Println("Exiting f1()")
 return -1
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Finding unreachable Go code"*

---

### 74. Cross-Compile with Explicit Target Variables

**Principle:** Set `GOOS` and `GOARCH` for the target and inspect the produced binary before distribution.

**Do:**
- Choose a supported operating-system and architecture pair.
- Build, then inspect with the platform's file-identification tool.
- Test the artifact on the real target.
- Remember that the binary reflects the compiler version that built it.

**Don't:**
- Don't execute a foreign-architecture binary on the build host and call the build invalid.
- Don't assume all target pairs are supported.
- Don't overlook cgo and platform-specific source constraints.

**Code:**
```go
func main() {
 fmt.Print("You are using ", runtime.Compiler, " ")
 fmt.Println("on a", runtime.GOARCH, "machine")
 fmt.Println("with Go version", runtime.Version())
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Cross-compilation"*

---

### 75. Discover Network Interfaces Through `net`

**Principle:** Use `net.Interfaces` and interface methods for portable address and capability discovery.

**Do:**
- Check interface enumeration errors.
- Iterate every interface because hosts commonly have virtual and physical devices.
- Read addresses with `Addrs()`.
- Inspect flags, MTU, and hardware address when capabilities matter.

**Don't:**
- Don't assume every listed interface is configured or physical.
- Don't assume every address is IPv4.
- Don't expect portable APIs for every routing and DNS configuration detail.

**Code:**
```go
 interfaces, err := net.Interfaces()
 if err != nil {
 fmt.Println(err)
 return
 }
for _, i := range interfaces {
 fmt.Printf("Interface: %v\n", i.Name)
 byName, err := net.InterfaceByName(i.Name)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading the configuration of network interfaces"*

---

### 76. Use Dedicated DNS Lookup Functions

**Principle:** Parse an argument first, then select forward, reverse, NS, or MX lookup according to the requested record type.

**Do:**
- Use `net.ParseIP` to distinguish addresses from hostnames.
- Use `LookupAddr` for reverse lookup.
- Use `LookupHost`, `LookupNS`, and `LookupMX` for their specific records.
- Iterate all returned records.

**Don't:**
- Don't assume one hostname maps to one address.
- Don't assume a subdomain has the parent domain's NS or MX records.
- Don't hide resolver errors.

**Code:**
```go
func lookHostname(hostname string) ([]string, error) {
 IPs, err := net.LookupHost(hostname)
 if err != nil {
 return nil, err
 }
 return IPs, nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Performing DNS lookups"*

---

### 77. Build HTTP Servers from Handlers and Explicit Routes

**Principle:** Keep each handler focused, register specific paths before the catch-all root, and start the server with a checked error.

**Do:**
- Use the `func(http.ResponseWriter, *http.Request)` handler shape.
- Write response data through the writer.
- Read path and host data from the request.
- Use `http.NewServeMux` for nontrivial routing.
- Let `/` handle paths not matched more specifically.

**Don't:**
- Don't confuse process logs with HTTP response output.
- Don't bury unrelated operations in one handler.
- Don't ignore `ListenAndServe` failures.

**Code:**
```go
func myHandler(w http.ResponseWriter, r *http.Request)
{
 fmt.Fprintf(w, "Serving: %s\n", r.URL.Path)
 fmt.Printf("Served: %s\n", r.Host)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating a web server in Go"*

---

### 78. Register pprof Endpoints on a Custom Mux

**Principle:** Expose `net/http/pprof` handlers explicitly when the server does not use the default mux.

**Do:**
- Use `net/http/pprof` for live HTTP applications.
- Register the index, command line, profile, symbol, and trace endpoints needed.
- Generate representative traffic while capturing a profile.
- Analyze captures with `go tool pprof`.

**Don't:**
- Don't assume importing pprof populates a custom mux automatically.
- Don't expose profiling endpoints without considering operational access.
- Don't collect an idle profile and infer loaded behavior.

**Code:**
```go
 r.HandleFunc("/debug/pprof/", pprof.Index)
 r.HandleFunc("/debug/pprof/cmdline", pprof.Cmdline)
 r.HandleFunc("/debug/pprof/profile", pprof.Profile)
 r.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
 r.HandleFunc("/debug/pprof/trace", pprof.Trace)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Profiling an HTTP server"*

---

### 79. Trace HTTP Request Phases with `httptrace`

**Principle:** Attach a `ClientTrace` when DNS, dial, connection reuse, headers, or first-byte latency must be separated.

**Do:**
- Define hooks only for events relevant to the diagnosis.
- Attach the trace through the request context.
- Correlate callbacks with the current transport round trip.
- Use trace output to locate the slow phase before tuning.

**Don't:**
- Don't infer DNS latency from total request duration.
- Don't use default clients without timeouts in production-shaped code.
- Don't confuse one logical request with multiple redirected round trips.

**Code:**
```go
trace := &httptrace.ClientTrace{
 GotFirstResponseByte: func() {
 fmt.Println("First response byte!")
 },
 GotConn: func(connInfo httptrace.GotConnInfo) {
 fmt.Printf("Got Conn: %+v\n", connInfo)
 },
 DNSDone: func(dnsInfo httptrace.DNSDoneInfo) {
 fmt.Printf("DNS Info: %+v\n", dnsInfo)
 },
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "HTTP tracing"*

---

### 80. Test HTTP Handlers without Opening a Socket

**Principle:** Invoke the handler directly with a synthetic request and a response recorder.

**Do:**
- Build a request with `http.NewRequest`.
- Record output with `httptest.NewRecorder`.
- Adapt the function with `http.HandlerFunc`.
- Assert both status and body.
- Test failure statuses as first-class behavior.

**Don't:**
- Don't start a real listener for a handler unit test.
- Don't assert only the body and ignore status.
- Don't print request-construction errors and return a passing test.

**Code:**
```go
func TestCheckStatusOK(t *testing.T) {
 req, err := http.NewRequest("GET",
"/CheckStatusOK", nil)
 if err != nil {
 fmt.Println(err)
 return
 }
 rr := httptest.NewRecorder()
 handler := http.HandlerFunc(CheckStatusOK)
 handler.ServeHTTP(rr, req)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Testing HTTP handlers"*

---

### 81. Use `http.Client` When Requests Need Control

**Principle:** Move from `http.Get` to an explicit client and request when timeout, transport, method, or response inspection matters.

**Do:**
- Parse and validate the URL.
- Create the request with `http.NewRequest`.
- Set a client timeout.
- call `Do` and close the response body.
- Inspect status, headers, content length, and body errors independently.

**Don't:**
- Don't use the default client when unbounded waiting is unacceptable.
- Don't read the body before checking the request error.
- Don't forget that unknown content length is represented separately from zero.

**Code:**
```go
c := &http.Client{
 Timeout: 15 * time.Second,
}
request, err := http.NewRequest("GET", URL.String(),
nil)
if err != nil {
 fmt.Println("Get:", err)
 return
}
httpData, err := c.Do(request)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Making your Go web client more advanced"*

---

### 82. Set HTTP Timeouts on Both Client and Server

**Principle:** Bound the whole client request and server read/write phases so slow or broken peers cannot hold resources indefinitely.

**Do:**
- Set `http.Client.Timeout` for the simplest whole-request limit.
- Use transport dialing and deadlines for lower-level control.
- Set `ReadTimeout` and `WriteTimeout` on `http.Server`.
- Test timeout behavior with a deliberately slow peer.

**Don't:**
- Don't rely on zero-value HTTP timeouts in production software.
- Don't set a connection deadline after the read or write it should bound.
- Don't treat timeout errors as ordinary successful responses.

**Code:**
```go
 srv := &http.Server{
 Addr: PORT,
 Handler: m,
 ReadTimeout: 3 * time.Second,
 WriteTimeout: 3 * time.Second,
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Setting the timeout period on the server side / Yet another way to time out!"*

---

### 83. Treat `net.Conn` as a Stream with Ownership

**Principle:** A TCP handler owns its accepted connection, reads framed messages, writes complete replies, and closes on termination.

**Do:**
- Listen with `net.Listen`.
- Accept in a loop when multiple clients are supported.
- Delimit a text protocol explicitly, such as with newlines.
- Close the listener and every connection.
- Check every read and write error.

**Don't:**
- Don't put `Accept` outside the loop if the server must serve later clients.
- Don't call `os.Exit` from one connection handler and kill every client.
- Don't assume TCP preserves application message boundaries.

**Code:**
```go
 for {
 c, err := l.Accept()
 if err != nil {
 fmt.Println(err)
 return
 }
 go handleConnection(c)
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A TCP server / A concurrent TCP server"*

---

### 84. Design TCP Protocols Before Coding Them

**Principle:** Document commands, arguments, framing, responses, errors, and termination before implementing a custom TCP protocol.

**Do:**
- Use an explicit delimiter.
- Normalize and tokenize input predictably.
- Return success and failure messages consistently.
- Separate domain operations from connection I/O where possible.
- Synchronize state shared by concurrent clients.

**Don't:**
- Don't let missing tokens produce out-of-range indexing.
- Don't save shared state concurrently without protection.
- Don't couple every domain function directly to `net.Conn`.

**Code:**
```go
 command := strings.TrimSpace(string(netData))
 tokens := strings.Fields(command)
 switch len(tokens) {
 case 0:
 continue
 case 1:
 tokens = append(tokens, "")
 tokens = append(tokens, "")
 tokens = append(tokens, "")
 tokens = append(tokens, "")
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A handy concurrent TCP server"*

---

### 85. Treat UDP as Independent Datagrams

**Principle:** Preserve each datagram's byte count and remote address because UDP has no reliable stream connection.

**Do:**
- Resolve and listen with UDP-specific functions when their options are needed.
- Use the `n` returned by `ReadFromUDP`.
- Reply to the returned remote address.
- Design application behavior for loss, duplication, and reordering.

**Don't:**
- Don't assume delivery or ordering.
- Don't process the unused portion of the receive buffer.
- Don't carry TCP stream-framing assumptions into UDP.
- Don't expect a STOP datagram to terminate generic tools automatically.

**Code:**
```go
 for {
 n, addr, err := connection.ReadFromUDP(buffer)
 fmt.Print("-> ", string(buffer[0:n-1]))
 if strings.TrimSpace(string(buffer[0:n])) ==
"STOP" {
 fmt.Println("Exiting UDP server!")
 return
 }
 data := []byte(strconv.Itoa(random(1, 1001)))
 _, err = connection.WriteToUDP(data, addr)
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Developing a UDP server"*

---

### 86. Spawn One TCP Handler per Accepted Client Deliberately

**Principle:** A goroutine per connection enables simultaneous clients, but shared state and shutdown still need explicit coordination.

**Do:**
- Accept continuously in the listener goroutine.
- Pass the accepted connection into its handler.
- Keep per-client parsing state local.
- Close the connection when that client stops.
- Protect global maps and persistence across clients.

**Don't:**
- Don't assume independent connections imply independent global state.
- Don't leave a handler blocked forever without deadlines or cancellation.
- Don't terminate the process for one client's malformed input.

**Code:**
```go
func handleConnection(c net.Conn) {
 for {
 netData, err :=
bufio.NewReader(c).ReadString('\n')
 if err != nil {
 fmt.Println(err)
 os.Exit(100)
 }
 temp := strings.TrimSpace(string(netData))
 if temp == "STOP" {
 break
 }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A concurrent TCP server"*

---

### 87. Keep RPC Contracts Shared and Methods Conformant

**Principle:** Put wire argument types and behavior contracts in a shared package, then register a server implementation and invoke exported methods by name.

**Do:**
- Export RPC methods and transmitted fields.
- Use the required argument and reply-pointer signature.
- Return an error from each RPC method.
- Register the implementation before serving connections.
- Check client `Call` errors.

**Don't:**
- Don't make the client depend on the server's implementation details.
- Don't pass an unaddressable reply value.
- Don't ignore registration, dial, or call failures.

**Code:**
```go
package sharedRPC
 type MyFloats struct {
 A1, A2 float64
}
type MyInterface interface {
 Multiply(arguments *MyFloats, reply *float64) error
 Power(arguments *MyFloats, reply *float64) error
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Remote Procedure Call (RPC)"*

---

### 88. Restrict Raw Networking to Protocol-Specific Tools

**Principle:** Capture raw packets only with an explicit protocol, bounded buffer, privilege model, and binary decoding plan.

**Do:**
- Specify IPv4 or IPv6 and the intended protocol.
- Use `buffer[:n]` after reading.
- Expect elevated privileges for raw sockets.
- Set socket options deliberately.
- Decode headers according to the protocol specification.

**Don't:**
- Don't treat raw packet bytes as text.
- Don't capture every protocol when only ICMP is needed.
- Don't assume packet layouts are portable without parsing.
- Don't send raw packets without constructing valid headers and checksums.

**Code:**
```go
 fd, err := syscall.Socket(syscall.AF_INET,
syscall.SOCK_RAW, syscall.IPPROTO_ICMP)
 if err != nil {
 fmt.Println("Error in syscall.Socket:", err)
 return
 }
 f := os.NewFile(uintptr(fd), "captureICMP")
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Doing low-level network programming / Grabbing raw ICMP network data"*

---

## Anti-Patterns & Common Mistakes

- **Discarded conversion error:** Bad input becomes a misleading zero value. → *Fix:* check every `strconv` error before updating state.
- **Unused import hidden with `_`:** A blank import obscures intent. → *Fix:* reserve blank imports for required initialization side effects.
- **Mixed stdout and stderr:** Pipelines consume diagnostics as data. → *Fix:* keep results on stdout and failures on stderr.
- **Double-handled error:** The same layer logs and returns without purpose. → *Fix:* choose one owner for logging policy.
- **Routine panic:** Expected failure tears down control flow. → *Fix:* return `error`; reserve panic for exceptional invariants.
- **Deferred close before error check:** A nil file may be closed. → *Fix:* check `Open`, then defer.
- **Loop-variable closure capture:** Deferred or concurrent code observes the changing variable. → *Fix:* pass the value as a parameter.
- **Unsafe pointer arithmetic:** The compiler cannot enforce bounds. → *Fix:* use slices and indexing unless a measured low-level need exists.
- **C string leak:** `C.CString` allocation outlives the call. → *Fix:* `defer C.free(unsafe.Pointer(p))`.
- **Manual GC as tuning:** Collection blocks without proving benefit. → *Fix:* inspect allocation and GC traces first.
- **Array used as a dynamic collection:** Growth requires allocation and copying. → *Fix:* use a slice.
- **Re-slice mistaken for copy:** Mutations affect the original backing array. → *Fix:* allocate and `copy` for ownership.
- **Tiny slice pins huge array:** A small view retains a large file buffer. → *Fix:* copy the needed segment.
- **Write to nil map:** Runtime panics. → *Fix:* initialize with `make` or a literal.
- **Map zero value treated as presence:** Missing and stored zero are conflated. → *Fix:* use the `ok` result.
- **Map order dependency:** Output changes across runs. → *Fix:* extract and sort keys when order matters.
- **Byte length treated as rune count:** Unicode text is truncated or miscounted. → *Fix:* range over runes.
- **Regex as universal parser:** The grammar becomes brittle and unreadable. → *Fix:* use structured parsers when available.
- **Regex compiled per record:** Repeated compilation adds unnecessary work. → *Fix:* compile invariant expressions once.
- **Overgrown anonymous function:** Important behavior is hidden inline. → *Fix:* extract a named function.
- **Mutable function variable:** A familiar identifier changes behavior at runtime. → *Fix:* keep function bindings stable.
- **Large public package surface:** Callers cannot identify the intended API. → *Fix:* export a short coherent set.
- **Surprising `init`:** Importing a package performs hidden work. → *Fix:* expose an explicit constructor or setup function.
- **Provider-owned interface:** The abstraction mirrors one implementation. → *Fix:* define the behavior where it is consumed.
- **One-value type assertion:** A mismatch panics. → *Fix:* use `v, ok` or a type switch.
- **Reflection for known types:** Static guarantees and speed are lost. → *Fix:* use concrete types or interfaces.
- **HTML generated with text templates:** Escaping guarantees are absent. → *Fix:* use `html/template`.
- **Home-grown standard data structure:** Maintenance exceeds the requirement. → *Fix:* prefer built-ins and `container` first.
- **`math/rand` password:** Output is reproducible and unsuitable for secrets. → *Fix:* use `crypto/rand`.
- **Hand-parsed complex flags:** Ordering and usage behavior break. → *Fix:* use `flag` and `flag.Value`.
- **Whole buffer processed after `Read`:** Stale bytes contaminate output. → *Fix:* process `buf[:n]`.
- **Buffered writer not flushed:** Final data remains in memory. → *Fix:* check `Flush` before successful completion.
- **Gob chosen for non-Go consumers:** Other languages cannot easily decode it. → *Fix:* use JSON or XML.
- **Signal portability assumption:** A Unix-specific constant prevents compilation. → *Fix:* isolate platform-specific signal sets.
- **SIGKILL cleanup plan:** The signal cannot be caught. → *Fix:* use catchable termination for graceful cleanup.
- **CLI refuses stdin:** The tool cannot compose in a pipeline. → *Fix:* default to stdin when no file is supplied.
- **Syscall number hard-coded across OSes:** The wrong kernel operation runs or fails. → *Fix:* use portable wrappers or platform-specific files.
- **Goroutine used as decoration:** Scheduling overhead is added without independent work. → *Fix:* keep synchronous code synchronous.
- **`time.Sleep` as join:** Fast and slow machines behave differently. → *Fix:* use `WaitGroup`, channels, or context.
- **`WaitGroup.Add` inside worker:** The worker may finish or `Wait` may race first. → *Fix:* add before spawning.
- **Extra `Done`:** Counter becomes negative and panics. → *Fix:* one deferred `Done` per successful `Add`.
- **Missing `Done`:** `Wait` blocks forever. → *Fix:* audit all exit paths and defer.
- **Unbuffered send without receiver:** The goroutine deadlocks. → *Fix:* arrange a receiver or revise the protocol.
- **Receiver closes shared channel:** A sender later panics. → *Fix:* give closure to the producer that knows completion.
- **Double close:** Multiple owners panic. → *Fix:* establish one closer.
- **Closed channel repeatedly selected:** Zero values spin the loop. → *Fix:* check `ok` and nil the channel when retired.
- **Default case defeats backpressure:** Work is silently dropped. → *Fix:* omit default unless rejection is explicit behavior.
- **All select channels nil:** The goroutine blocks forever. → *Fix:* retain a cancellation or progress case.
- **Oversized buffer as performance cure:** Memory rises without added workers. → *Fix:* benchmark capacity and service rate.
- **Mutex spread across functions:** Nested locking becomes invisible. → *Fix:* localize the critical section.
- **Forgotten unlock:** Every later locker blocks. → *Fix:* defer unlock where control flow can branch.
- **Mutation under `RLock`:** Multiple readers race on writes. → *Fix:* use exclusive `Lock`.
- **Concurrent map writes:** Runtime may terminate with `fatal error: concurrent map writes`. → *Fix:* mutex or monitor ownership.
- **Race detector omitted:** Schedule-dependent defects escape ordinary tests. → *Fix:* run race-enabled tests on concurrent paths.
- **Timeout without cancellation:** The caller leaves, worker continues or blocks sending. → *Fix:* propagate context or an explicit stop signal.
- **Derived context never canceled:** Timer and child resources linger. → *Fix:* call the returned cancel function.
- **Results closed too early:** Workers panic on send. → *Fix:* wait for workers, then close results.
- **Worker jobs never closed:** Workers wait forever. → *Fix:* producer closes after final job.
- **Premature optimization:** Effort targets the wrong code and introduces bugs. → *Fix:* test, profile, change, remeasure.
- **Profile too short:** Sampling yields no useful data. → *Fix:* run representative work long enough.
- **CPU and heap profiles conflated:** One experiment perturbs another. → *Fix:* capture dimensions separately.
- **Trace used for function hotspots:** The evidence is indirect. → *Fix:* use pprof for per-function cost.
- **Test only the happy path:** Boundary defects survive. → *Fix:* include zero, empty, invalid, and failure cases.
- **Benchmark input grows with `b.N`:** Calibration never converges. → *Fix:* keep workload size fixed.
- **Benchmark result unused:** Compiler may eliminate work. → *Fix:* retain the result outside the loop.
- **Real socket in handler unit test:** Tests become slow and flaky. → *Fix:* use `httptest.ResponseRecorder`.
- **HTTP body not closed:** Connections and resources cannot be reused promptly. → *Fix:* defer `Body.Close` after a successful response.
- **Default HTTP timeout:** A peer can hold resources indefinitely. → *Fix:* configure client and server timeouts.
- **TCP treated as messages:** Reads split or combine application records. → *Fix:* define framing.
- **One client error exits server:** Other clients are terminated. → *Fix:* return from the handler, not the process.
- **UDP treated as reliable:** Loss and reordering break state. → *Fix:* add application semantics or choose TCP.
- **Concurrent persistence without synchronization:** Shared files and maps corrupt. → *Fix:* serialize state ownership.
- **Undocumented custom protocol:** Clients disagree on framing and errors. → *Fix:* specify the protocol before implementation.
- **Raw socket without protocol filter:** Parsing becomes unsafe and ambiguous. → *Fix:* select one protocol and decode its headers.

## Decision Heuristics / Checklists

### General Go Checklist
- Is every import used for an explicit reason?
- Is every returned error checked, returned, or deliberately logged?
- Does each function perform one coherent job?
- Are pointers used only for mutation, identity, size, or API requirements?
- Is a slice preferable to an array for this collection?
- Does every map lookup that distinguishes absence use the `ok` result?
- Does Unicode logic operate on runes rather than bytes?
- Are package exports minimal and cohesive?
- Are comments about purpose and constraints rather than obvious syntax?

### Concurrency Checklist
- What starts each goroutine?
- What ends each goroutine?
- Who owns each channel close?
- Is `WaitGroup.Add` called before spawn with one deferred `Done`?
- Is shared mutable state protected or monitor-owned?
- Is timeout accompanied by cancellation?
- Has race detection exercised the concurrent path?
- Would synchronous code be simpler and fast enough?

### Channels vs. Mutexes
- Channels for ownership, sequencing, cancellation, and work transfer.
- Monitor goroutine for one owner serializing complex state.
- Mutex for a small in-memory critical section.
- `RWMutex` only when reads dominate and measurements justify it.
- Buffered channel when a bounded queue or admission limit is explicit.
- `chan struct{}` for notification without payload.
- Directional channel parameters at function boundaries.

### File and CLI Checklist
- Does the utility read stdin when no file is supplied?
- Is primary output isolated from diagnostics?
- Are flags defined before `flag.Parse()` and read from `flag.Args()`?
- Is every opened file checked before its deferred close?
- Is every read sliced to `n` with `io.EOF` handled separately?
- Is every buffered writer flushed?
- Are permissions and endianness explicit?
- Is the serialization format compatible with all consumers?

### Testing and Performance Checklist
- Are tests in `_test.go` files with correct names?
- Do tests cover success, boundary, empty, malformed, and error behavior?
- Are HTTP status and body both asserted without real sockets?
- Do benchmarks keep input size independent of `b.N` and retain the result?
- Are allocations measured with `-benchmem`?
- Is correctness established before profiling and re-profiling after changes?
- Do examples still match their documented output?

### HTTP and Networking Checklist
- Is the URL parsed and validated?
- Do client and server have explicit timeouts?
- Is every response body closed and transport error separated from status?
- Does the mux register specific routes and a deliberate catch-all?
- Is TCP framing documented and each connection owned by one handler?
- Does UDP logic tolerate loss, duplication, and reordering?
- Are RPC methods exported and signature-conformant?
- Is shared server state synchronized across client goroutines?

## Key Takeaways

1. **Make failure explicit.** Return and check errors; do not let blank identifiers convert bad input into plausible data.
2. **Use the standard library as the default architecture.** Its interfaces connect files, memory, HTTP, TCP, UDP, templates, tests, and tooling.
3. **Prefer slices over arrays for dynamic data, but remember that slices can share and retain backing storage.**
4. **Keep interfaces small and behavioral.** Implicit satisfaction is most useful when the abstraction is defined by its consumer.
5. **Avoid reflection and unsafe code unless static typing cannot satisfy a real requirement.** Both move failures from compile time to runtime.
6. **Compose Unix tools through stdin, stdout, stderr, flags, and `io.Reader`/`io.Writer`.**
7. **Design goroutine termination before spawning.** Every goroutine needs a completion or cancellation path.
8. **Treat channel closure as ownership.** One producer closes; receivers observe and stop.
9. **Use `select` for orchestration, context for propagated cancellation, and worker pools for bounded concurrency.**
10. **Prefer monitor ownership over scattered shared-memory mutation when state is complex.**
11. **Run the race detector.** Ordinary successful runs do not expose every schedule-dependent defect.
12. **Profile correct code before optimizing.** Use pprof for hotspots, trace for scheduler and blocking behavior, and benchmarks for controlled comparisons.
13. **Test public behavior with Go's built-in tools.** Use direct handler tests, executable examples, race checks, vet, and allocation-aware benchmarks.
14. **Set network timeouts on both sides.** Zero-value client and server timeouts permit indefinite resource retention.
15. **Treat TCP as a stream and UDP as datagrams.** Define framing for TCP and reliability policy for UDP.
16. **Synchronize state shared by concurrent server clients.** Separate connections do not make global maps or files safe.
17. **Document custom protocols before writing them.** Commands, framing, errors, and shutdown are part of the contract.
18. **Learn the runtime deeply, but preserve Go's safety and simplicity until evidence requires lower-level control.**

## Cross-References
- Related: [[../Shipping_Go.md]]
- Topic index: [[../INDEX.md]]
