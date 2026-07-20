# Test-Driven Development in Go
**Author:** Adelina Simion (Packt, 2023)
**Topic tags:** `#testing` `#go` `#general` `#architecture`
**Language focus:** Go-first (standard `testing` package + ecosystem)
**Sources:** `markdown_output/_pdf_extracts/Test-Driven_Development_in_Go.md` (no summary exists)

## TL;DR
A practitioner's tour of TDD in Go that starts from the Red-Green-Refactor loop and the testing pyramid, builds the `BookSwap` REST API as a running example, and progresses through table-driven tests, mocking with `testify/mock`, BDD with `ginkgo` and `godog`, `httptest` integration tests, Docker-driven E2E tests, refactoring, contract testing with Pact, the race detector, fuzz and property-based testing, and generics. Treat it as the canonical map of Go testing techniques and the libraries that complement the standard `testing` package.

---

## Best Practices by Topic

### The Red-Green-Refactor Cycle

**Principle:** Every piece of production code is preceded by a failing test, made green with the minimum code necessary, then refactored while the test stays green.

**Do:**
- Start every feature with a failing test that captures one requirement slice.
- In Green, write the *minimum* code to pass — defer optimization to Refactor.
- Re-run the full suite after each Refactor step.
- Predict how the test will fail before you run it.

**Don't:**
- Mix mindsets — adding features during Refactor or refactoring during Green.
- Write the implementation first and call the after-the-fact test "TDD".

*Ref: Test-Driven_Development_in_Go.md — "The iterative approach of TDD" / "TDD best practices"*

---

### The Arrange-Act-Assert (AAA) Pattern

**Principle:** Tests follow a uniform Arrange → Act → Assert structure so they read like specifications.

**Do:**
- Use comments (`// Arrange`, `// Act`, `// Assert`) to make phases explicit.
- Extract variables for inputs and `want` values during Refactor.
- Let Act/Assert repeat for additional assertions on the same UUT.

**Don't:**
- Pile multiple outcomes into a single convoluted test.

**Code:**
```go
func TestAdd(t *testing.T) {
    // Arrange
    e := calculator.Engine{}
    x, y := 2.5, 3.5
    want := 6.0

    // Act
    got := e.Add(x, y)

    //Assert
    if got != want {
        t.Errorf("Add(%.2f,%.2f) incorrect, got: %.2f, want: %.2f",
            x, y, got, want)
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Writing tests" / "Use case – implementing the calculator engine"*

---

### The Testing Pyramid

**Principle:** Lots of cheap unit tests at the base, fewer integration tests in the middle, very few expensive E2E tests on top.

**Do:**
- Keep unit tests isolated, fast, and the most numerous.
- Treat integration and E2E tests as complements that verify seams and user journeys.
- Push as much logic as possible down into unit-testable code.

**Don't:**
- Substitute a mountain of E2E tests for missing unit tests.

*Ref: Test-Driven_Development_in_Go.md — "The testing pyramid"*

---

### Go Modules and Packages as the Unit Under Test

**Principle:** Modules bundle packages for distribution; packages are the UUT and Go's primary encapsulation boundary.

**Do:**
- Initialize the module with `go mod init <path>`.
- Name packages short, descriptive, and meaningful alongside their exported types.
- Treat packages as small APIs — export only what callers need.

**Don't:**
- Manually edit `go.mod` for non-version changes.

**Code:**
```go
module github.com/PacktPublishing/Test-Driven-Development-in-Go
go 1.19
```
```go
package format

func Result(expression string, result float64) string {
    // implementation code
    return ""
}
```
```go
package calculator

type Engine struct {}

func(e *Engine) Add(x, y float64) float64{
    // implementation code
    return 0
}

// ... method declarations
```
```go
package input

import "github.com/PacktPublishing/Test-Driven-Development-in-Go/chapter02/calculator"

type Parser struct {
    engine *calculator.Engine
    validator *Validator
}

func (p *Parser) ProcessExpression(expr string) (*string, error) {
    // implementation code
}

// ... method declarations
```
*Ref: Test-Driven_Development_in_Go.md — "Modules and packages" / "The power of Go packages"*

---

### Test File Placement and the External `_test` Package

**Principle:** Test files live next to source files (`*_test.go`) and should declare a `<pkg>_test` package so they only exercise exported behavior.

**Do:**
- Name test files after their source file (`engine.go` → `engine_test.go`).
- Use the external `_test` package whenever possible.
- Reap the benefits: no brittle internal-state assertions, isolated test deps, consumer-perspective API checks.

**Don't:**
- Reach into unexported state from tests unless absolutely necessary.

**Code:**
```go
package calculator_test

import "testing"

func TestAdd(t *testing.T) {
}
```
*Ref: Test-Driven_Development_in_Go.md — "Test file naming and placement" / "Additional test packages"*

---

### The `testing` Package — Core Types and Methods

**Principle:** The standard `testing` package is the only way to interact with the test runner. Use the convenience methods (`Errorf`, `Fatalf`, `Skipf`) rather than `Fail`/`FailNow` directly.

**Key methods on `*testing.T`:**
- `t.Log` / `t.Logf` — log on completion
- `t.Fail` — mark failed, keep going; `t.FailNow` — mark failed, stop now
- `t.Error` / `t.Errorf` ≡ `Log` + `Fail`
- `t.Fatal` / `t.Fatalf` ≡ `Log` + `FailNow`
- `t.Skip` / `t.Skipf` / `t.SkipNow` — mark skipped
- Types: `testing.T` (tests), `testing.B` (benchmarks), `testing.F` (fuzz, Go 1.18+)

**Don't:**
- Expect built-in assertions — Go provides none; use `if` + `t.Errorf` or `testify`.

*Ref: Test-Driven_Development_in_Go.md — "The testing package"*

---

### Test Signatures and Naming

**Principle:** Tests are functions matching `func TestName(t *testing.T)`; name them after the UUT (`TestAdd`), not the implementation detail.

**Do:**
- Suffix must start with a capital letter (`TestAdd`, not `Testadd`).
- Optionally use BDD-style `TestUUT_Precondition_Expected` when precision matters.
- Keep names short and consistent.

**Code:**
```go
func TestName(t *testing.T) {
    // implementation
}
```
*Ref: Test-Driven_Development_in_Go.md — "Test signatures"*

---

### Running Tests with `go test`

**Principle:** Master the runner's modes and flags for fast, targeted feedback.

**Do:**
- `go test ./...` — package-list mode across the project (cache enabled).
- `go test -run "^TestAdd" ./chapter02/calculator -v` — regex + path + verbose.
- `go test -cover -coverprofile=cover.out` — capture coverage.
- `go test -bench.` — run benchmarks.
- `go test -race` — enable the race detector.

**Don't:**
- Forget local-directory mode does not cache results.

*Ref: Test-Driven_Development_in_Go.md — "Running tests"*

---

### The Expanded TDD-in-Go Workflow (11 Steps)

**Principle:** Concretize Red-Green-Refactor into a repeatable Go workflow.

1. Create the test file and `<pkg>_test` package.
2. Create the source file and `<pkg>` package.
3. Write the test signature.
4. Write stub UUT definitions returning zero/dummy values.
5. Set up the test scenario with AAA.
6. Run the test — watch it fail (Red).
7. Implement just enough to pass (Green).
8. Run again — watch it pass.
9. Refactor test and source.
10. Re-run — confirm still green.
11. Repeat for new functionality.

**Code:** (stubs that compile before any real implementation)
```go
package calculator

type Engine struct {}

func(e *Engine) Add(x, y float64) float64{
    return 0
}
```
```go
// Real implementation after Green
func(e *Engine) Add(x, y float64) float64{
    return x + y
}
```
*Ref: Test-Driven_Development_in_Go.md — "Writing tests"*

---

### Test Setup and Teardown — `TestMain`

**Principle:** `TestMain(m *testing.M)` runs once per package and gives you the only reliable place for package-wide setup/teardown.

**Do:**
- Always invoke `m.Run()`, capture its exit code, run teardown, then call `os.Exit(code)`.
- Factor setup/teardown into named helpers for readability.
- Only one `TestMain` per package is allowed.

**Don't:**
- Forget `os.Exit(e)` — silent false positives result.

**Code:**
```go
func TestMain(m *testing.M) {
    // setup statements
    setup()

    // run the tests
    e := m.Run()

    // cleanup statements
    teardown()

    // report the exit code
    os.Exit(e)
}

func setup() {
    log.Println("Setting up.")
}

func teardown() {
    log.Println("Tearing down.")
}
```
*Ref: Test-Driven_Development_in_Go.md — "The TestMain approach"*

---

### Setup with `init` Functions

**Principle:** For setup-only (no teardown), `init()` is lighter than `TestMain`.

**Do:**
- Use `init` when you only need pre-test initialization.
- Remember multiple `init` functions per package are allowed (file-order matters).

**Don't:**
- Use `init` if you also need cleanup — combine with `defer` or `TestMain`.

**Code:**
```go
func init() {
    log.Println("Init setup.")
}
```
*Ref: Test-Driven_Development_in_Go.md — "init functions"*

---

### Teardown with `defer`

**Principle:** For per-test teardown, `defer` an anonymous function at the top of the test.

**Do:**
- Place `defer` calls at the very top of the test body so they always register.
- Prefer `defer` over package-level teardown when scope is local.

**Don't:**
- Rely on `defer` for setup — it only runs on exit.

**Code:**
```go
func TestAdd(t *testing.T) {
    defer func ()  {
    log.Println("Deferred tearing down.")
}()

    // Arrange
    e := calculator.Engine{}
    x, y := 2.5, 3.5
    want := 6.0

    // Act
    got := e.Add(x, y)

    //Assert
    if got != want {
        t.Errorf("Add(%.2f,%.2f) incorrect, got: %.2f, want: %.2f", x, y, got, want)
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Deferred functions"*

---

### Subtests with `t.Run`

**Principle:** Group related scenarios under a single test using `t.Run(name, fn)` for hierarchical, shareable setup.

**Do:**
- Extract shared Act/Assert into a closure to keep subtests tiny.
- Use subtests to share Arrange state across multiple scenarios.

**Don't:**
- Force unrelated scenarios into one parent test.

**Code:**
```go
func TestAdd(t *testing.T) {
    // Arrange
    e := calculator.Engine{}

    actAssert := func(x, y, want float64) {
        // Act
        got := e.Add(x, y)

        //Assert
        if got != want {
            t.Errorf("Add(%.2f,%.2f) incorrect, got: %.2f, want: %.2f", x, y, got, want)
        }
    }

    t.Run("positive input", func(t *testing.T) {
        x, y := 2.5, 3.5
        want := 6.0
        actAssert(x, y, want)
    })

    t.Run("negative input", func(t *testing.T) {
        x, y := -2.5, -3.5
        want := -6.0
        actAssert(x, y, want)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Implementing subtests"*

---

### Code Coverage

**Principle:** Track coverage as a TDD health indicator, but don't optimize for 100%.

**Do:**
- `go test -cover` prints coverage; `-coverprofile=FILE` saves it.
- `go tool cover -html=FILE` opens a visual report.
- Aim ~80%; beyond that yields diminish.

**Don't:**
- Equate high coverage with bug-free code.

*Ref: Test-Driven_Development_in_Go.md — "Code coverage"*

---

### Benchmarks

**Principle:** Use `testing.B` to measure performance with the same `go test` toolchain.

**Do:**
- Loop `b.N` times in the body — the runner scales N until measurements stabilize.
- Profile with `-cpuprofile`, `-benchmem`.
- Treat benchmarks as part of the test suite.

**Don't:**
- Trust a single local run — variance is real.

**Code:**
```go
func BenchmarkAdd(b *testing.B) {
    e := calculator.Engine{}

    // run the Add function b.N times
    for i := 0; i < b.N; i++ {
        e.Add(2, 3)
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "The difference between a test and a benchmark"*

---

### Interfaces as Dependencies

**Principle:** Wrap every external dependency in an interface defined on the consumer side to decouple packages and enable mocking.

**Do:**
- Keep dependency interfaces exported; concrete structs can stay unexported.
- Prefer small interfaces (ISP) — small mocks and simple setups follow.
- Define the interface where it's *consumed*, not where it's implemented.

**Don't:**
- Hard-code struct dependencies in the UUT — it kills testability.

**Code:**
```go
// OperationProcessor is the interface for processing
// mathematical expressions
type OperationProcessor interface {
    ProcessOperation(operation *calculator.Operation) (*string, error)
}

// ValidationHelper is the interface for input validation
type ValidationHelper interface {
    CheckInput(operator string, operands []float64) error
}
```
```go
// Parser is responsible for converting input to
// mathematical operations
type Parser struct {
    engine    OperationProcessor
    validator ValidationHelper
}
```
*Ref: Test-Driven_Development_in_Go.md — "Interfaces as dependencies" / "Exploring mocks"*

---

### Dependency Injection — Manual and with `wire`

**Principle:** Inject dependencies via constructors (preferred) or fields; use code-gen tools like `wire` or `dig` when graphs get complex.

**Do:**
- Keep constructors small — Go eschews the verbose constructors of other languages.
- Pass dependencies as interfaces, not concrete structs.

**Code:** (manual DI)
```go
type Adder interface {
    Add(x, y float64) float64
}

func (e Engine) Add(x, y float64) float64 {
    return x + y
}

func NewEngine() *Engine {
    return &Engine{}
}

type Calculator struct {
    Adder Adder
}
func NewCalculator(a Adder) *Calculator {
    return &Calculator{Adder: a}
}
func (c Calculator) PrintAdd(x, y float64) {
    fmt.Println("Result:", c.Adder.Add(x, y))
}
```
```go
func main() {
    engine := NewEngine()
    calc := NewCalculator(engine)
    calc.PrintAdd(2.5, 6.3)
}
```
**Code:** (wire code-gen)
```go
//go:build wireinject
package main
import "github.com/google/wire"
var Set = wire.NewSet(NewEngine, wire.Bind(new(Adder), new(*Engine)), NewCalculator)
func InitCalc() *Calculator {
    wire.Build(Set)
    return nil
}
```
```go
// generated wire_gen.go
func InitCalc() *Calculator {
    adder := NewEngine()
    calculator := NewCalculator(adder)
    return calculator
}
```
*Ref: Test-Driven_Development_in_Go.md — "Dependency injection" / "Implementing dependency injection"*

---

### Mocking Frameworks — `testify/mock` + `mockery`

**Principle:** Generate mocks for free with `mockery`, then drive them in tests with `On(...).Return(...)` and `AssertExpectations`.

**Do:**
- `go get github.com/stretchr/testify` and `go install github.com/vektra/mockery/v2@latest`.
- Regenerate mocks as part of CI to keep them in sync with interfaces.
- Use `mock.AnythingOfType("T")` instead of `mock.Anything` whenever possible — preserve intent.

**Don't:**
- Forget `AssertExpectations(t)` — otherwise `On` expectations aren't verified.

**Code:**
```sh
$ mockery --dir "chapter03" --output "chapter03/mocks" --all
```
```go
// OperationProcessor is an autogenerated mock type for the
// OperationProcessor type
type OperationProcessor struct {
    mock.Mock
}

// ProcessOperation provides a mock function with given
// fields: operation
func (_m *OperationProcessor) ProcessOperation(operation calculator.Operation) (*string, error) {
    ret := _m.Called(operation)
    // implementation code
}
```
*Ref: Test-Driven_Development_in_Go.md — "Mocking frameworks" / "Generating mocks"*

---

### Writing Tests with Mocks (AAA + Mock Lifecycle)

**Principle:** Follow a 5-step recipe: create mocks → inject → set expectations → act → assert expectations.

**Code:**
```go
func TestProcessExpression(t *testing.T) {
    t.Run("valid input", func(t *testing.T) {
        // Arrange
        expr := "2 + 3"
        operator := "+"
        operands := []float64{2.0, 3.0}
        expectedResult := "2 + 3 = 5.5"
        engine := mocks.NewOperationProcessor(t)
        validator := mocks.NewValidationHelper(t)
        parser := input.NewParser(engine, validator)

        validator.On("CheckInput", operator, operands).Return(nil).Once()
        engine.On("ProcessOperation", &calculator.Operation{
            Expression: expr,
            Operator:   operator,
            Operands:   operands,
        }).Return(expectedResult).Once()

        // Act
        result, err := parser.ProcessExpression(expr)

        // Assert
        // other assertions
        validator.AssertExpectations(t)
        engine.AssertExpectations(t)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Verifying mocks"*

---

### Assertion Frameworks — `testify/assert` and `require`

**Principle:** Use `assert` for non-fatal checks; use `require` when subsequent lines can't run if the check fails.

**Do:**
- `assert.Equal(t, expected, actual)` — equality.
- `assert.Nil(t, x)` / `assert.NotNil(t, x)` — nil checks (don't use `Equal(nil, ...)`).
- `assert.Contains(t, collection, element)` — string/list/map membership.
- `assert.Subset(t, list, subset)` — subset relationships.
- `require.Nil(t, err)` for setup errors that invalidate everything after.

**Code:**
```go
assert.Equal(t, expected, actual)
assert.NotEqual(t, expected, actual)
assert.Nil(t, actual)
assert.NotNil(t, actual)
assert.Contains(t, collection, element)
assert.NotContains(t, collection, element)
assert.Subset(t, list, subset)
assert.NotSubset(t, list, subset)
require.Nil(t, err)
```
*Ref: Test-Driven_Development_in_Go.md — "Using testify"*

---

### Asserting Errors

**Principle:** Don't just check `err != nil` — verify the error message or, better, a custom error type.

**Do:**
- `assert.EqualError(t, err, expectedMsg)` — message equality.
- `assert.Contains(t, err.Error(), substring)` — robust to formatting changes.
- Prefer custom error types and `errors.As` for type-safe verification.

**Code:**
```go
t.Run("invalid operation", func(t *testing.T) {
    // Arrange
    expr := "2 % 3"
    operator := "%"
    operands := []float64{2.0, 3.0}
    expectedErrMsg := "bad operator"
    engine := mocks.NewOperationProcessor(t)
    validator := mocks.NewValidationHelper(t)
    parser := input.NewParser(engine, validator)
    validator.On("CheckInput", operator, operands).
        Return(fmt.Errorf(expectedErrMsg)).Once()

    // Act
    result, err := parser.ProcessExpression(expr)

    // Assert
    require.NotNil(t, err)
    require.Nil(t, result)
    assert.Contains(t, err.Error(), expr)
    assert.Contains(t, err.Error(), expectedErrMsg)
    validator.AssertExpectations(t)
})
```
*Ref: Test-Driven_Development_in_Go.md — "Asserting errors"*

---

### SOLID Principles for Testable Code

**Principle:** The five SOLID principles all converge on testable, refactorable Go packages.

1. **S**RP — one reason to change per package; small surface, easy edge-case coverage.
2. **O**CP — extend behavior without modifying existing code (fewer test changes).
3. **L**SP — substitutable interfaces keep tests stable across implementations.
4. **I**SP — small interfaces → small mocks → simple setups.
5. **D**IP — depend on abstractions (interfaces) → loose coupling and easy DI.

**Don't:**
- Forget that in Go the SOLID "entity" is the package, not the struct.

*Ref: Test-Driven_Development_in_Go.md — "Writing testable code"*

---

### Identifying Edge Cases by Variable Type

**Principle:** Enumerate base/edge/boundary/corner cases per input variable type.

- **String:** `""`, long, Unicode/special chars, multiline, raw-string literals.
- **Numeric:** `0`, min/max of type, negatives.
- **Struct:** zero value, nil pointer, partially initialized fields.
- **Collection:** empty, single, nil, duplicates, very large.

**Don't:**
- Conflate edge cases (one variable) with corner cases (multiple variables at extremes).

*Ref: Test-Driven_Development_in_Go.md — "Identifying edge cases"*

---

### Positive and Negative Tests

**Principle:** Functional requirements need positive tests; robustness needs equally important negative tests.

- **Positive:** valid input → expected result.
- **Negative:** invalid input → meaningful error, no crash.

**Don't:**
- Skip negative tests — error handling is part of the user journey.

*Ref: Test-Driven_Development_in_Go.md — "Testing multiple conditions"*

---

### External Service Edge Cases

**Principle:** Always mock external dependencies; design operations to be idempotent so retries are safe.

**Do:**
- Test for: 5xx errors, slow requests, dropped responses.
- Verify retry and timeout behavior at the UUT boundary.

**Don't:**
- Mock databases (use the real engine in a container).

*Ref: Test-Driven_Development_in_Go.md — "External services"*

---

### Go's Explicit Error Handling

**Principle:** Handle errors first; return them as the last return value; check `err != nil`, not the absence of error.

**Code:**
```go
type error interface {
    Error() string
}
```
```go
func (p *Parser) ProcessExpression(expr string) error
```
```go
if err := parser.ProcessExpression(*expr); err != nil {
    log.Fatal(err)
}
```
*Ref: Test-Driven_Development_in_Go.md — "Error-handling refresher"*

---

### Table-Driven Tests — The 5-Step Recipe

**Principle:** Tables of named cases keep test suites concise and trivially extensible.

1. Declare function signature (return zeros so all cases initially fail).
2. Declare an inline `testCase` struct type.
3. Build a `map[string]testCase` (or `map[string]struct{...}`) keyed by scenario name.
4. Loop the map and run each as a subtest.
5. Implement assertions — handle the error case first and `return`.

**Code:**
```go
package table

func Divide (x, y int8) (*string, error) {
    return nil, nil
}
```
```go
func TestDivide(t *testing.T) {
    type testCase struct {
        x, y    int8
        wantErr error
        want    *string
    }
}
```
```go
tests := map[string]testCase{
    "pos x, pos y": {x: 8, y: 4, want: "2.00"},
    "neg x, neg y": {x: -4, y: -8, want: "0.50"},
}
```
```go
tests := map[string]struct {
    x, y int
    wantErr error
    want string
}{
    "pos x, pos y": {x: 8, y: 4, want: "2.00"},
    "neg x, neg y": {x: -4, y: -8, want: "0.50"},
}
```
```go
for name, tc := range tests {
    t.Run(name, func(t *testing.T) {
        // Test execution
    })
}
```
```go
for name, tc := range tests {
    t.Run(name, func(t *testing.T) {
        x, y := int8(tc.x), int8(tc.y)
        r, err := table.Divide(x, y)
        if tc.wantErr != nil {
            assert.Equal(t, tc.wantErr, err)
            return
        }
        assert.Nil(t, err)
        assert.Equal(t, tc.want, *r)
    })
}
```
```go
func Divide(x, y int8) (*string, error) {
    r := float64(x) / float64(y)
    result := fmt.Sprintf("%.2f", r)
    return &result, nil
}
```
```go
tests := map[string]struct {
    x, y int
    wantErr error
    want string
}{
    "pos x, pos y":  {x: 8, y: 4, want: "2.00"},
    "neg x, neg y":  {x: -4, y: -8, want: "0.50"},
    "equal x, y":    {x: 4, y: 4, want: "1.00"},
    "max x, pos y":  {x: 127, y: 2, want: "63.50"},
    "min x, pos y":  {x: -128, y: 2, want: "-64.00"},
    "zero x, pos y": {x: 0, y: 2, want: "0.00"},
    "pos x, zero y": {x: 10, y: 0, wantErr: errors.New("cannot divide by 0")},
    "zero x, zero y": {x: 0, y: 0, wantErr: errors.New("cannot divide by 0")},
    "max x, max y":  {x: 127, y: 127, want: "1.00"},
    "min x, min y":  {x: -128, y: -128, want: "1.00"},
}
```
```go
func Divide(x, y int8) (*string, error) {
    if y == 0 {
        return nil, errors.New("cannot divide by 0")
    }
    r := float64(x) / float64(y)
    result := fmt.Sprintf("%.2f", r)
    return &result, nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Table-driven testing in action"*

---

### Parallelizing Table-Driven Tests

**Principle:** Mark subtests `t.Parallel()` and capture the range variable into a local copy.

**Do:**
- `tc := rtc` inside the loop body before `t.Run` so each goroutine sees its own case.
- Limit concurrency via `-parallel N` (default `GOMAXPROCS`).

**Don't:**
- Forget the capture — parallel subtests will otherwise share the last loop value.

**Code:**
```go
for name, rtc := range tests {
    tc := rtc
    t.Run(name, func(t *testing.T) {
        t.Parallel()
        x, y := int8(tc.x), int8(tc.y)
        r, err := table.Divide(x, y)
        if tc.wantErr != nil {
            assert.Equal(t, tc.wantErr, err)
            return
        }
        assert.Nil(t, err)
        assert.Equal(t, tc.want, *r)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Parallelization"*

---

### Table-Driven Tests — Pros and Cons

**Pros:** concise, easy to extend, refactor-friendly.
**Cons:** uniform setup makes per-case variations hard, doesn't suit cases needing different teardowns, less readable than BDD.

**Don't:**
- Force disparate setups into a single table — split into separate subtests.

*Ref: Test-Driven_Development_in_Go.md — "Advantages and disadvantages of table-driven testing"*

---

### The BookSwap Application — Service Layout

**Principle:** A small REST API is the book's running example for table-driven, integration, E2E, contract, and concurrency testing.

- **UserService** — endpoints `GET /`, `POST /users`, `GET /users/{id}`.
- **BookService** — endpoints `POST /books`, `POST /books/{id}?user={userId}`.
- **PostingService** — external stub for shipping.

**Code:**
```go
type Book struct {
    ID      string `json:"id"`
    Name    string `json:"name"`
    Author  string `json:"author"`
    OwnerID string `json:"owner_id"`
    Status  string `json:"status"`
}
```
```go
// NewBookService initializes a BookService given its dependencies.
func NewBookService(initial []Book, ps PostingService) *BookService

// Get returns a given book or error if none exists.
func (bs *BookService) Get(id string) (*Book, error)

// Upsert creates or updates a book.
func (bs *BookService) Upsert(b Book) Book

// List returns the list of available books.
func (bs *BookService) List() []Book

// ListByUser returns the list of books for a given user.
func (bs *BookService) ListByUser(userID string) []Book

// SwapBook checks whether a book is available and, if possible, marks it as swapped.
func (bs *BookService) SwapBook(bookID, userID string) (*Book, error)
```
```go
type BookService struct {
    books map[string]Book
    ps    PostingService
}
```
*Ref: Test-Driven_Development_in_Go.md — "Use case – the BookSwap application"*

---

### Testing BookService with Subtests + Tables

**Principle:** When different cases need different UUT setup, nest subtests and only use tables inside the ones that share setup.

**Code:**
```go
func TestGetBook(t *testing.T) {
    t.Run("initial books", func(t *testing.T) {
        // Books are available in the BookService
    })
    t.Run("empty books", func(t *testing.T) {
        // No books in the BookService
    })
}
```
```go
eb := db.Book{
    ID: uuid.New().String(),
    Name: "Existing book",
    Status: db.Available.String(),
}
bs := db.NewBookService([]db.Book{eb}, nil)
```
```go
tests := map[string]struct {
    id string
    want db.Book
    wantErr error
}{
    "existing book": {id: eb.ID, want: eb},
    "no book found": {id: "not-found", wantErr: errors.New("no book found")},
    "empty id":      {id: "", wantErr: errors.New("no book found")},
}
```
```go
for name, tc := range tests {
    t.Run(name, func(t *testing.T) {
        b, err := bs.Get(tc.id)
        if tc.wantErr != nil {
            assert.Equal(t, tc.wantErr, err)
            assert.Nil(t, b)
            return
        }
        assert.Nil(t, err)
        assert.Equal(t, tc.want, *b)
    })
}
```
```go
t.Run("empty books", func(t *testing.T) {
    bs := db.NewBookService([]db.Book{})
    b, err := bs.Get("id")
    assert.Equal(t, errors.New("no book found"), err)
    assert.Nil(t, b)
})
```
*Ref: Test-Driven_Development_in_Go.md — "Testing BookService"*

---

### Integration Testing with `httptest`

**Principle:** Use `httptest.NewServer(handler)`, `httptest.NewRequest`, and `httptest.ResponseRecorder` to exercise HTTP handlers end-to-end without real network.

**Code:**
```go
// Handler contains the handler and all its dependencies.
type Handler struct {
    bs *db.BookService
    us *db.UserService
}
// Index is invoked by HTTP GET /.
func (h *Handler) Index(w http.ResponseWriter, r *http.Request) {
    // Send an HTTP status & a hardcoded message
    resp := &Response{
        Message: "Welcome to the BookSwap service!",
        Books:   h.bs.List(),
    }
    writeResponse(w, http.StatusOK, resp)
}
```
```go
func TestIndexIntegration(t *testing.T) {
    // Arrange
    book := db.Book{
        ID: uuid.New().String(),
        Name: "My first integration test",
        Status: db.Available.String(),
    }
    bs := db.NewBookService([]db.Book{book}, nil)
    h := handlers.NewHandler(bs, nil)
    svr := httptest.NewServer(http.HandlerFunc(h.Index))
    defer svr.Close()
    // Act
    r, err := http.Get(svr.URL)
    // Assert
    require.Nil(t, err)
    assert.Equal(t, http.StatusOK, r.StatusCode)
    body, err := io.ReadAll(r.Body)
    r.Body.Close()
    require.Nil(t, err)
    var resp handlers.Response
    err = json.Unmarshal(body, &resp)
    require.Nil(t, err)
    assert.Equal(t, 1, len(resp.Books))
    assert.Contains(t, resp.Books, book)
}
```
*Ref: Test-Driven_Development_in_Go.md — "Implementing integration tests"*

---

### Separating Slow Integration Tests

**Principle:** Pick a strategy (short mode, naming convention, or env var) and make *fast* the default.

**Do:**
- `LONG=true go test ...` (env var, the book's preferred option).
- Combine with `t.Skip` for opt-in slow tests.

**Don't:**
- Make `go test` slow by default — devs will avoid running it.

**Code:**
```go
func TestIndexIntegration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping TestIndexIntegration in short mode.")
    }
    // testing code continues
}
```
```go
func TestIndexIntegration(t *testing.T) {
    if os.Getenv("LONG") == "" {
        t.Skip("Skipping TestIndexIntegration in short mode.")
    }
    // testing code continues
}
```
*Ref: Test-Driven_Development_in_Go.md — "Running integration tests"*

---

### Behavior-Driven Development (BDD) Fundamentals

**Principle:** Write tests in business language using Given-When-Then to bridge technical/non-technical stakeholders.

**Pros:** single source of truth, tests-as-docs, narrow behaviors, wider involvement.
**Cons:** time-consuming upfront and to maintain, requires cross-functional commitment, depends on good BDD practice.

*Ref: Test-Driven_Development_in_Go.md — "Fundamentals of BDD"*

---

### BDD with Ginkgo + Gomega

**Principle:** `ginkgo bootstrap` generates a suite; use `Describe`, `Context`, `BeforeEach`, `AfterEach`, `It`, and `Expect(...).To(...)` matchers.

**Code:**
```go
package handlers_test

import (
    "testing"
    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"
)

func TestHandlers(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Handlers Suite")
}
```
```go
var _ = Describe("Handlers integration", func() {
    var svr *httptest.Server
    var book db.Book
    BeforeEach(func() {
        book = db.Book{
            ID: uuid.New().String(),
            Name: "My first integration test",
            Status: db.Available.String(),
        }
        bs := db.NewBookService([]db.Book{book}, nil)
        ha := handlers.NewHandler(bs, nil)
        svr = httptest.NewServer(http.HandlerFunc(ha.Index))
    })
    AfterEach(func() {
        svr.Close()
    })

    Describe("Index endpoint", func() {
        Context("with one existing book", func() {
            It("should return book", func() {
                r, err := http.Get(svr.URL)
                Expect(err).To(BeNil())
                Expect(r.StatusCode).To(Equal(http.StatusOK))
                // … assertions continue
            })
        })
    })
})
```
*Ref: Test-Driven_Development_in_Go.md — "Implementing BDD tests with Ginkgo"*

---

### Database Testing — Libraries and Principles

**Principle:** Test against the *real* DB engine in a container; mocking databases is an anti-pattern.

**Useful Go libraries:**
- `go-testfixtures` — Ruby-on-Rails-style fixtures.
- `golang-migrate` — versioned migrations.
- `go-txdb` — wrap test queries in transactions, rolled back after.
- `gorm` — popular ORM.
- `bun` — newer ORM for SQL.

**Don't:**
- Mock databases — differences in behavior/perf hide bugs.

*Ref: Test-Driven_Development_in_Go.md — "Understanding database testing"*

---

### Docker Fundamentals for Test Environments

**Principle:** Containerize components for identical local/CI/prod setups.

**Key commands:** `docker pull|run|ps|stop|kill|exec`; `docker compose up|ps|stop|kill`.

**Containerization vs. virtualization:**
- Virtualization runs multiple OSes on one machine.
- Containerization runs multiple apps from one OS on one machine.

*Ref: Test-Driven_Development_in_Go.md — "Fundamentals of Docker"*

---

### E2E Testing with Docker — Dockerfile

**Principle:** A Dockerfile specifies a reproducible application image; pair it with `docker-compose` for multi-container setups.

**Code:**
```dockerfile
FROM golang:1.19-alpine
WORKDIR /app
COPY go.mod ./
COPY go.sum ./
COPY . .
RUN go mod download
RUN go build ./chapter06/cmd
EXPOSE ${BOOKSWAP_PORT}
CMD [ "./cmd" ]
```
*Ref: Test-Driven_Development_in_Go.md — "Using Docker"*

---

### Adding Persistent Storage with `golang-migrate` + GORM

**Principle:** Version DB schema with migration files; bind Go types to tables with an ORM.

**Code:** (up migration)
```sql
BEGIN;
CREATE TABLE IF NOT EXISTS users
(
    id VARCHAR (50) PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    -- other column definitions
);
COMMIT;
```
```sql
DROP TABLE IF EXISTS users;
```
```go
func main() {
    // other initialisation code
    postgresURL, ok := os.LookupEnv("BOOKSWAP_DB_URL")
    if !ok {
        log.Fatal("env variable BOOKSWAP_DB_URL not found")
    }
    m, err := migrate.New("file://chapter06/db/migrations", postgresURL)
    if err != nil {
        log.Fatal(err)
    }
    if err := m.Up(); err != nil {
        log.Fatal(err)
    }
    defer func() {
        m.Down()
    }()
    // other initialisation code
}
```
```go
func main() {
    // other initialisation code
    postgresURL, ok := os.LookupEnv("BOOKSWAP_DB_URL")
    if !ok {
        log.Fatal("$BOOKSWAP_DB_URL not found")
    }
    dbConn, err := gorm.Open(postgres.Open(postgresURL), &gorm.Config{})
    if err != nil {
        log.Fatal(err)
    }
    ps := db.NewPostingService()
    b := db.NewBookService(dbConn, ps)
    u := db.NewUserService(dbConn, b)
    // initialisation code continues
}
```
```go
// ListByUser returns the list of books for a given user.
func (bs *BookService) ListByUser(userID string) ([]Book, error) {
    var items []Book
    if result := bs.DB.Where("owner_id = ?", userID).Find(&items); result.Error != nil {
        return nil, result.Error
    }
    return items, nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Persistent storage"*

---

### Docker Compose for Multi-Service Apps

**Code:**
```yaml
version: '3'
services:
  books:
    build:
      context: .
      dockerfile: Dockerfile.book-swap.chapter06
    ports:
      - "${BOOKSWAP_PORT}:${BOOKSWAP_PORT}"
    depends_on:
      db:
        condition: service_healthy
    restart: on-failure
    env_file:
      - docker.env
  db:
    image: postgres:15.0-alpine
    ports:
      - "5432:5432"
    expose:
      - "5432"
    env_file:
      - docker.env
    restart: on-failure
```
```ini
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_DB=books
BOOKSWAP_DB_URL=postgres://root:root@db:5432/books?sslmode=disable
BOOKSWAP_PORT=3000
```
*Ref: Test-Driven_Development_in_Go.md — "Running the BookSwap application"*

---

### BDD E2E with Godog

**Principle:** Godog generates step scaffolding from Gherkin `.feature` files; chain state between steps with `context.Context`.

**Feature file:**
```gherkin
Feature: New user signs up
 In order to use the BookSwap application
 As a new user
 I need to be able to sign up.

Background: Verify configuration
 Given the BookSwap app is up

Scenario: Sign up
  Given user details
  When sent to the users endpoint
  Then a new user profile is created
```

**Generated step scaffolding:**
```go
func aNewUserProfileIsCreated() error {
    return godog.ErrPending
}
func sentToTheUsersEndpoint() error {
    return godog.ErrPending
}
func theBookSwapAppIsUp() error {
    return godog.ErrPending
}
func userDetails() error {
    return godog.ErrPending
}

func InitializeScenario(ctx *godog.ScenarioContext) {
    ctx.Step(`^a new user profile is created$`, aNewUserProfileIsCreated)
    ctx.Step(`^sent to the users endpoint$`, sentToTheUsersEndpoint)
    ctx.Step(`^the BookSwap app is up$`, theBookSwapAppIsUp)
    ctx.Step(`^user details$`, userDetails)
}
```

**Passing context between steps:**
```go
func theBookSwapAppIsUp(ctx context.Context) (context.Context, error) {
    // test step implementation
}
```
```go
// contextKey is used to pass information between test steps.
type contextKey struct {
    UsersURL string
    User     db.User
}
```
```go
func theBookSwapAppIsUp(ctx context.Context) (context.Context, error) {
    url, err := getTestURL()
    if err != nil {
        return ctx, fmt.Errorf("incorrect config:%v", err)
    }
    resp, err := http.Get(url)
    if err != nil || resp.StatusCode != http.StatusOK {
        return ctx, fmt.Errorf("bookswap not up:%v", err)
    }
    return context.WithValue(ctx, contextKey{}, contextKey{
        UsersURL: url + "/users",
    }), nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Exploring Godog" / "Implementing tests with Godog"*

---

### Database Assertions and Seed Data

**Principle:** Insert seed data and assert on DB state directly through GORM (not via the application API) to isolate failure sources.

**Code:**
```go
func addUser() error {
    dbConn, err := gorm.Open(postgres.Open(postgresURL), &gorm.Config{})
    if err != nil {
        return err
    }
    dbConn.Save(&db.User{
        ID:   uuid.New().String(),
        Name: "Generated User",
    })
    return nil
}
```
```go
func verifyUser(want db.User) error {
    dbConn, err := gorm.Open(postgres.Open(postgresURL), &gorm.Config{})
    if err != nil {
        log.Fatal(err)
    }
    var got db.User
    if err := dbConn.Where("id = ?", want.ID).First(&got); err != nil {
        return err.Error
    }
    if want != got {
        return fmt.Errorf("user does not match: got %v, want %v", got, want)
    }
    return nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Using database assertions"*

---

### Code Refactoring — Process and Techniques

**Principle:** Refactoring is behavior-preserving change done in small steps with the test suite as the safety net.

**Five techniques:**
- **Red-Green-Refactor** — natural test evolution.
- **Extract** — pull fragments into named helpers.
- **Simplify** — improve conditional/parameter complexity.
- **Inline** — collapse needless indirection.
- **Abstraction** — introduce interfaces for reuse.

**Don't:**
- Mix redesign (changes behavior) with refactoring.

*Ref: Test-Driven_Development_in_Go.md — "Code refactoring steps and techniques"*

---

### Managing Technical Debt

**Principle:** Refactor "little and often" inside sprint planning — never save it for a dedicated big-bang sprint.

**Consequences of ignoring it:** bugs, slowed feature delivery, engineer frustration, attrition.

*Ref: Test-Driven_Development_in_Go.md — "Technical debt"*

---

### Changing Dependencies via Interfaces

**Principle:** Interfaces defined on the consumer side make swapping implementations painless; the compiler guides you.

**Do:**
- Use IDE rename/lookup to update all call sites.
- Regenerate mocks after interface changes.
- Let the compiler pinpoint broken call sites.

**Code:**
```go
// PostingService interface wraps around external posting functionality.
type PostingService interface {
    NewOrder(b Book) error
}
```
```go
// NewBookService initialises a BookService given its dependencies.
func NewBookService(db *gorm.DB, ps PostingService) *BookService {
    return &BookService{
        DB: db,
        ps: ps,
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Changing dependencies"*

---

### Automated Refactoring — Renaming

**Code:**
```go
// BookRepository contains all the functionality and dependencies for managing books.
type BookRepository struct {
    DB *gorm.DB
    ps PostingService
}
```
```go
// NewBookRepository initialises a BookService given its dependencies.
func NewBookRepository(db *gorm.DB, ps PostingService) *BookRepository {
    return &BookRepository{
        DB: db,
        ps: ps,
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Automated refactoring"*

---

### Validating Refactored Code — Method Signature Change

**Principle:** Change the signature first; let tests go red; update them minimally; implement last.

**Code:**
```go
// Get returns a given book or error if none exists.
func (bs *BookRepository) Get(id string) (*Book, error)
```
```go
// Get populates a given book or returns error if none exists.
func (bs *BookRepository) Get(b *Book) error
```
```go
for name, tc := range tests {
    t.Run(name, func(t *testing.T) {
        var b db.Book
        b.ID = tc.id
        err := bs.Get(&b)
        if tc.wantErr != nil {
            assert.Equal(t, tc.wantErr, err)
            assert.Nil(t, b)
            return
        }
        assert.Nil(t, err)
        assert.Equal(t, tc.want, b)
    })
}
```
```go
func (bs *BookRepository) Get(b *Book) error {
    if r := bs.DB.Where("id = ?", b.ID).First(&b); r.Error != nil {
        return r.Error
    }
    return nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Validating refactored code"*

---

### Error Verification — Three Strategies

**Principle:** Prefer custom error types over `errors.New` strings or substring matching for type-safe assertions.

**Strategy 1 — Recreate the message (brittle):**
```go
func TestErrorsVerification(t *testing.T) {
    t.Run("formatted custom error", func(t *testing.T) {
        input := 4
        wantMsg := fmt.Sprintf("Input %d cannot be even.", input)
        err := checkOdd(input)
        gotMsg := err.Error()
        assert.Equal(t, wantMsg, gotMsg)
    })
}
```

**Strategy 2 — Substring match (loose):**
```go
func TestErrorsVerification(t *testing.T) {
    t.Run("formatted custom error", func(t *testing.T) {
        input := 4
        err := checkOdd(input)
        gotMsg := err.Error()
        assert.Contains(t, gotMsg, fmt.Sprint(input))
        assert.Contains(t, gotMsg, "even")
    })
}
```

**Strategy 3 — Custom error type (preferred):**
```go
type evenNumberError struct {
    input int
}

func (e *evenNumberError) Error() string {
    return fmt.Sprintf("Input %d cannot be even.", e.input)
}

func checkOdd(input int) error {
    if input%2 == 0 {
        return &evenNumberError{
            input: input,
        }
    }
    return nil
}
```
```go
func TestErrorsVerification(t *testing.T) {
    t.Run("custom error type", func(t *testing.T) {
        input := 4
        wantErr := &evenNumberError{
            input: input,
        }
        err := checkOdd(input)
        var gotErr *evenNumberError
        require.True(t, errors.As(err, &gotErr))
        assert.Equal(t, wantErr, gotErr)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Error verification" / "Custom error types"*

---

### Errors New / Format helpers

**Code:**
```go
err := errors.New("Something is wrong!")
```
```go
msg := err.Error()
```
```go
func TestErrorsVerification(t *testing.T){
    t.Run("simple custom error", func(t *testing.T) {
        wantMsg := "Something went wrong!"
        err := errors.New(wantMsg)
        gotMsg := err.Error()
        assert.Equal(t, wantMsg, gotMsg)
    })
}
```
```go
func checkOdd(input int) error {
    if input%2 == 0 {
        return fmt.Errorf("Input %d cannot be even.", input)
    }
    return nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Error verification"*

---

### Splitting the Monolith — Rules of Thumb

**Principle:** Design microservices that remain loosely coupled.

**Do:**
- Separate data stores per service (no shared DB).
- Use asynchronous communication (queues, event buses).
- Implement fault tolerance (circuit breaker).
- Make backward-compatible changes.
- Add request tracing and monitoring.

**Don't:**
- Forget graceful degradation — design and test for dependency outages.

*Ref: Test-Driven_Development_in_Go.md — "Splitting up the monolith" / "Key refactoring considerations"*

---

### Non-Functional Testing Types

**Principle:** Functional tests verify correctness; non-functional tests verify performance, scalability, security, and usability.

**Performance types:** load, stress, volume, scalability/spike.
**Usability types:** failover, configuration, usability, security.

*Ref: Test-Driven_Development_in_Go.md — "Functional and non-functional testing"*

---

### Performance Metrics and Thresholds

**Track:** response time, error rate, CPU/memory, concurrent users, data throughput.

**Rules of thumb:**
- Average response < 500ms; peak < 1s.
- Error rate < 5%.
- CPU/memory < 70%.

*Ref: Test-Driven_Development_in_Go.md — "Performance testing in Go"*

---

### Performance Testing with Benchmarks + pprof

**Principle:** Use `testing.B` for microbenchmarks; integrate `net/http/pprof` for live profiling.

**Code:**
```go
func BenchmarkGetIndex(b *testing.B) {
    endpoint := getTestEndpoint(b)
    for x := 0; x < b.N; x++ {
        bks, err := http.Get(*endpoint)
        assert.Nil(b, err)
        assert.NotNil(b, bks)
    }
}
```
```go
func ConfigureServer(handler *Handler) *mux.Router {
    router := mux.NewRouter().StrictSlash(true)
    // other handler functions
    if os.Getenv("DEBUG") != "" {
        router.PathPrefix("/debug/pprof/").
            Handler(http.DefaultServeMux)
    }
    return router
}
```
*Ref: Test-Driven_Development_in_Go.md — "Implementing performance tests"*

---

### Microservices — Complexities and Trade-offs

**Three complexity axes:** development, deployment, organizational.
**Pros vs. monolith:** flexible scaling, smaller code bases, isolated failures.
**Cons:** higher infra cost, organizational overhead, harder debugging.

*Ref: Test-Driven_Development_in_Go.md — "Contract testing"*

---

### Contract Testing with Pact — Consumer Test

**Principle:** The consumer records its expectations into a contract file; the provider verifies against it later.

**Code:**
```go
func TestConsumerIndex_Local(t *testing.T) {
    // Initialize
    pact := dsl.Pact{
        Consumer: "Consumer",
        Provider: "BookSwap",
    }
    pact.Setup(true)
    // Test case - makes the call to the provider
    var test = func() (err error) {
        baseURL, ok := os.LookupEnv("BOOKSWAP_BASE_URL")
        require.True(t, ok)
        url := fmt.Sprintf("%s:%d/", baseURL, pact.Server.Port)
        req, err := http.NewRequest("GET", url, nil)
        assert.Nil(t, err)
        req.Header.Set("Content-Type", "application/json")
        resp, err := http.DefaultClient.Do(req)
        assert.Nil(t, err)
        assert.NotNil(t, resp)
        return
    }
    t.Run("get index", func(t *testing.T) {
        pact.AddInteraction().
            Given("BookSwap is up").
            UponReceiving("GET / request").
            WithRequest(dsl.Request{
                Method: "GET", Path: dsl.String("/"),
                Headers: dsl.MapMatcher{
                    "Content-Type": dsl.String("application/json"),
                }
            }).
            WillRespondWith(dsl.Response{
                Status: http.StatusOK,
                Body: dsl.Like(handlers.Response{
                    Message: "Welcome to the BookSwap Service!",
                })
            })
        require.Nil(t, pact.Verify(test))
    })
    // Clean up
    require.Nil(t, pact.WritePact())
    pact.Teardown()
}
```
*Ref: Test-Driven_Development_in_Go.md — "Using Pact"*

---

### Contract Testing with Pact — Provider Verification

**Code:**
```go
func TestProviderIndex_Local(t *testing.T) {
    // Initialise
    pact := dsl.Pact{
        Provider: "BookSwap",
    }
    url := getTestEndpoint(t)

    // Verify
    _, err := pact.VerifyProvider(t, types.VerifyRequest{
        ProviderBaseURL: url,
        PactURLs:        []string{PACTS_PATH},
    })
    require.Nil(t, err)
}
```
*Ref: Test-Driven_Development_in_Go.md — "Using Pact"*

---

### Distributed BookSwap — Service Decomposition

**Principle:** When splitting a monolith, each service gets its own DB and well-defined access patterns; contract-test every consumer-provider pair.

- `SwapService` — entry point, consumer of `BookService` and `UserService`.
- `UserService` — owns `UsersDB`, consumer of `BookService`.
- `BookService` — owns `BooksDB`, consumer of external `PostingService`.

*Ref: Test-Driven_Development_in_Go.md — "Breaking up the BookSwap monolith"*

---

### Production Best Practices for Microservices

**Do:**
- **Monitoring & observability** — structured logging (`zap`, `logrus`, `apex/log`).
- **Deployment patterns** — canary, blue-green.
- **Circuit breaker** (`hystrix-go`) to prevent cascading failures.

**Don't:**
- Forget graceful degradation when a dependency fails.

*Ref: Test-Driven_Development_in_Go.md — "Production best practices"*

---

### Goroutines — Lightweight Threads

**Principle:** `go f()` runs `f` concurrently; creation is non-blocking, so the parent may exit before the child prints.

**Code:**
```go
func greet(gr string) {
    fmt.Println("Hello, friend!")
}

func main() {
    go greet()
    fmt.Println("Goodbye, friend!")
}
```

**Communicating by sharing memory (fragile):**
```go
var finished bool
func greet() {
    fmt.Println("Hello, friend!")
    finished = true
}

func main() {
    go greet()
    for !finished {
        fmt.Println("Child goroutine not finished.")
        time.Sleep(10 * time.Millisecond)
    }
    fmt.Println("Child goroutine finished.")
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Goroutines"*

---

### Channels — Sharing Memory by Communicating

**Principle:** Channels are pipes between goroutines; `chan struct{}` is the idiomatic signal type.

**Operations:** `ch <- v` (send), `v := <-ch` (receive), `close(ch)`.

**Code:**
```go
func greet(ch chan bool) {
    fmt.Println("Hello, friend!")
    ch <- true
}
func main() {
    ch := make(chan bool)
    go greet(ch)
    <-ch
    fmt.Println("Child goroutine finished.")
    fmt.Println("Goodbye, friend!")
}
```
```go
func greet(ch chan struct{}) {
    fmt.Println("Hello, friend!")
    close(ch)
}

func main() {
    ch := make(chan struct{})
    go greet(ch)
    <-ch
    fmt.Println("Child goroutine finished.")
    fmt.Println("Goodbye, friend!")
}
```

**Channel state summary:**
- **Nil channel:** send/recv block forever; `close` panics.
- **Initialized channel:** send/recv block until both parties ready; `close` succeeds.
- **Closed channel:** send panics; recv returns zero value immediately; `close` panics.

*Ref: Test-Driven_Development_in_Go.md — "Channels"*

---

### `sync.Once` — Safe Close

**Code:**
```go
func safelyClose(once *sync.Once, ch chan struct{}) {
    fmt.Println("Hello, friend!")
    once.Do(func() {
        fmt.Println("Channel closed.")
        close(ch)
    })
}
func main() {
    var once sync.Once
    ch := make(chan struct{})
    for i := 0; i<3; i++ {
        go safelyClose(&once, ch)
    }
    <-ch
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Closing once"*

---

### Thread-Safe Data Structures — `sync.Map`

**Code:**
```go
const workerCount = 3
func greet(id int, smap *sync.Map, done chan struct{}) {
    g := fmt.Sprintf("Hello, friend! I'm Goroutine %d.", id)
    smap.Store(id, g)
    done <- struct{}{}
}

func main() {
    var smap sync.Map
    done := make(chan struct{})
    for i := 0; i < workerCount; i++ {
        go greet(i, &smap, done)
    }
    for i := 0; i < workerCount; i++ {
        <-done
    }
    smap.Range(func(key, value any) bool {
        fmt.Println(value)
        return true
    })
    fmt.Println("Goodbye, friend!")
}
```

**Custom thread-safe stack using `sync.Mutex`:**
```go
// Thread safe LIFO Stack implementation
type Stack struct {
    lock sync.Mutex
    data []string
}
// Push adds the given element to the end of the list
func (s *Stack) Push(el string) {
    defer s.lock.Unlock()
    s.lock.Lock()
    s.data = append(s.data, el)
}
// Pop removes and returns the last element from the list,
// or an error if the list is empty.
func (s *Stack) Pop() (*string, error) {
    defer s.lock.Unlock()
    s.lock.Lock()
    if len(s.data) == 0 {
        return nil, fmt.Errorf("stack is empty")
    }
    last := s.data[len(s.data)-1]
    s.data = s.data[0 : len(s.data)-1]
    return &last, nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Thread-safe data structures"*

---

### `sync.WaitGroup` — Wait for Many Goroutines

**Code:**
```go
const workerCount = 3
func greet(id int, smap *sync.Map, wg *sync.WaitGroup) {
    defer wg.Done()
    g := fmt.Sprintf("Hello, friend! I'm Goroutine %d.", id)
    smap.Store(id, g)
}
func main() {
    var smap sync.Map
    var wg sync.WaitGroup
    wg.Add(workerCount)
    for i := 0; i < workerCount; i++ {
        go greet(i, &smap, &wg)
    }
    wg.Wait()
    smap.Range(func(key, value any) bool {
        fmt.Println(value)
        return true
    })
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Waiting for completion"*

---

### Data Races — The Default Trap

**Principle:** Concurrent `append` to an unprotected slice loses data silently.

**Code:**
```go
const workerCount = 3
var greetings []string
func greet(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    g := fmt.Sprintf("Hello, friend! I'm Goroutine %d.", id)
    greetings = append(greetings, g)
}
func main() {
    var wg sync.WaitGroup
    wg.Add(workerCount)
    for i := 0; i < workerCount; i++ {
        go greet(i, &wg)
    }
    wg.Wait()
    for _, g := range greetings {
        fmt.Println(g)
    }
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Data races"*

---

### Deadlocks from Synchronous Channels

**Principle:** The last sender with no receiver blocks forever; Go runtime detects all-asleep and panics.

**Code:**
```go
var greetings []string
const workerCount = 3
func greet(id int, ch chan struct{}, wg *sync.WaitGroup) {
    defer wg.Done()
    g := fmt.Sprintf("Hello, friend! I'm Goroutine %d.", id)
    <-ch
    greetings = append(greetings, g)
    ch <- struct{}{}
}
func main() {
    ch := make(chan struct{})
    var wg sync.WaitGroup
    wg.Add(workerCount)
    for i := 0; i < workerCount; i++ {
        go greet(i, ch, &wg)
    }
    ch <- struct{}{}
    wg.Wait()
    for _, g := range greetings {
        fmt.Println(g)
    }
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Deadlocks"*

---

### Buffered Channels

**Principle:** `make(chan T, capacity)` decouples sender and receiver up to N; capacity reached → behaves as unbuffered.

**Code:**
```go
ch := make(chan Type, capacity)
```
```go
const workerCount = 3
func greet(id int, ch chan string) {
    g := fmt.Sprintf("Hello, friend! I'm Goroutine %d.", id)
    ch <- g
    fmt.Printf("Goroutine %d completed.\n", id)
}
func main() {
    ch := make(chan string, workerCount)
    for i := 0; i < workerCount; i++ {
        go greet(i, ch)
    }
    fmt.Println(<-ch)
    fmt.Println(<-ch)
    fmt.Println("Goodbye, friend!")
}
```
*Ref: Test-Driven_Development_in_Go.md — "Buffered channels"*

---

### The Go Race Detector

**Principle:** `go test -race` instruments memory access and reports data races without false positives.

**Do:**
- Run race-enabled load/integration tests under realistic workloads.
- Expect ~10× CPU/memory overhead — never enable in production.

**Don't:**
- Treat it as proof of correctness — it only catches *executed* races.

*Ref: Test-Driven_Development_in_Go.md — "The Go race detector"*

---

### Untestable Concurrency Conditions

**Four conditions tests cannot fully prove absent:**
1. **Race conditions** — unsynchronized shared mutations.
2. **Deadlocks** — circular waits.
3. **Livelocks** — polling without progress.
4. **Starvation** — greedy goroutines blocking others.

**Three rules of thumb:**
1. Share values with channels, not variables.
2. `defer` lock releases as soon as acquired.
3. Wait for all child goroutines before parent exit.

*Ref: Test-Driven_Development_in_Go.md — "Untestable conditions"*

---

### Concurrent Load Test for the BookSwap API

**Principle:** Combine `t.Parallel()` with a `for` loop to issue concurrent requests; instrument the *server* with `-race`.

**Code:**
```go
func TestUpsertUser_Load(t *testing.T) {
    if os.Getenv("LONG") == "" {
        t.Skip("Skipping TestUpsertUser_Load in short mode.")
    }
    userEndpoint := getTestEndpoint(t)
    requestBody, err := json.Marshal(map[string]string{
        "name":      "Concurrent Test User",
        "address":   "1 London Road",
        "post_code": "N1",
        "country":   "United Kingdom",
    })
    require.Nil(t, err)
    require.NotNil(t, requestBody)
    for i := 0; i < LOAD_AMOUNT; i++ {
        t.Run("concurrent upsert", func(t *testing.T) {
            t.Parallel()
            req := bytes.NewBuffer(requestBody)
            r, err := http.Post(userEndpoint, "application/json", req)
            assert.Nil(t, err)
            body, err := io.ReadAll(r.Body)
            r.Body.Close()
            require.Nil(t, err)
            var resp handlers.Response
            err = json.Unmarshal(body, &resp)
            require.Nil(t, err)
            assert.Equal(t, http.StatusOK, r.StatusCode)
            assert.Nil(t, err)
            assert.NotNil(t, resp)
            assert.NotEmpty(t, resp.User.ID)
        })
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Use case – testing concurrency in the BookSwap application"*

---

### Code Robustness — Characteristics and Best Practices

**Principle:** Robust code is easy to change, makes minimal assumptions, handles errors well, exposes a clear API, is easy to test, consistently styled, readable, and well-named/commented.

**Unix-philosophy roots:** transparency + simplicity.

**Don't:**
- Rely on globals, hardcoded strings, or implicit behavior.

*Ref: Test-Driven_Development_in_Go.md — "Code robustness"*

---

### Refactoring Fragile Code into Robust Code

**Principle:** Move from globals + magic strings to typed parameters, nil checks, switch over enum, pre-allocated slices, error returns.

**Before (fragile):**
```go
var input map[int]string
func GetValues(dir string) []string {
    var keys []int
    for k := range input {
        keys = append(keys, k)
    }
    if dir == "asc" {
        sort.Ints(keys)
    }
    if dir == "desc" {
        sort.Slice(keys, func(i, j int) bool {
            return keys[i] > keys[j]
        })
    }
    var vals []string
    for _, k := range keys {
        vals = append(vals, input[k])
    }
    return vals
}
```

**After (robust):**
```go
type SortDirection int
const (
    ASC SortDirection = iota
    DESC
)
// GetSortedValues returns the key-sorted values of a given map.
func GetSortedValues(input map[int]string, dir SortDirection) ([]string, error) {
    if input == nil {
        return nil, fmt.Errorf("cannot sort nil input map")
    }
    keys := make([]int, 0, len(input))
    for k := range input {
        keys = append(keys, k)
    }
    switch dir {
    case ASC:
        sort.Slice(keys, func(i, j int) bool {
            return keys[i] < keys[j]
        })
    case DESC:
        sort.Slice(keys, func(i, j int) bool {
            return keys[i] > keys[j]
        })
    default:
        return nil, fmt.Errorf("sort direction not recognized")
    }
    vals := make([]string, 0, len(input))
    for _, k := range keys {
        vals = append(vals, input[k])
    }
    return vals, nil
}
```
*Ref: Test-Driven_Development_in_Go.md — "Best practices"*

---

### Fuzz Testing in Go (Go 1.18+)

**Principle:** Native `*testing.F` lets the toolchain generate random inputs to surface panics, leaks, and incorrect outputs.

**Rules:**
- Function name starts with `Fuzz`.
- Single `*testing.F` parameter, no return value.
- Exactly one `f.Fuzz(...)` target per test.
- Acceptable arg types: `string`, `[]byte`, all `int`/`uint`/`float`, `bool`, `rune`, `byte`.
- Run with `go test -fuzz=FuzzName -fuzztime=5s`.
- Tests must be deterministic.

**Code:**
```go
func FuzzGetSortedValues_ASC(f *testing.F) {
    input := map[int]string{
        99: "B",
        0:  "A",
    }
    f.Add(3, "W")
    f.Fuzz(func(t *testing.T, k int, v string) {
        input[k] = v
        keys := make([]int, 0, len(input))
        for k := range input {
            keys = append(keys, k)
        }
        sort.Ints(keys)
        sortedValues, err := GetSortedValues(input, ASC)
        require.Nil(t, err)
        require.NotNil(t, sortedValues)
        for index, v := range sortedValues {
            key := keys[index]
            assert.Equal(t, input[key], v)
        }
    })
}
```

**Pros:** easy to use, early in dev lifecycle, finds many bugs.
**Cons:** doesn't replace other tests, no guarantees, CPU/memory intensive.

*Ref: Test-Driven_Development_in_Go.md — "Usages of fuzzing" / "Fuzz testing in Go"*

---

### Property-Based Testing with `testing/quick`

**Principle:** Define a property as a function returning `bool`; `quick.Check` searches for inputs that falsify it.

**Helpers:** `quick.Check`, `quick.CheckEqual`, `quick.Value`, `quick.Generator`.

**Code:**
```go
func TestGetSortedValues_ASC(t *testing.T) {
    input := map[int]string{
        99: "B",
        0:  "A",
    }
    isSorted := func(k int, val string) bool {
        input[k] = val
        keys := make([]int, 0, len(input))
        for k := range input {
            keys = append(keys, k)
        }
        sort.Ints(keys)
        sortedValues, err := fr.GetSortedValues(input, fr.ASC)
        if err != nil || sortedValues == nil {
            return false
        }
        for index, v := range sortedValues {
            key := keys[index]
            if input[key] != v {
                return false
            }
        }
        return true
    }
    if err := quick.Check(isSorted, nil); err != nil {
        t.Error(err)
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Property-based testing"*

---

### Fuzzing HTTP Endpoints — BookSwap User Creation

**Principle:** Fuzz every untrusted input source — user payloads and other-service responses.

**Code:**
```go
func FuzzTestUserCreation(f *testing.F) {
    // other initialization
    f.Add("test user", "1 London Road", "N1", "UK")
    f.Fuzz(func(t *testing.T, name string, address string,
        postCode string, country string) {
        requestBody, err := json.Marshal(map[string]string{
            "name":      name,
            "address":   address,
            "post_code": postCode,
            "country":   country,
        })
        require.Nil(t, err)
        req := bytes.NewBuffer(requestBody)
        resp, err := http.Post(userEndpoint, "application/json", req)
        assert.Nil(t, err)
        defer resp.Body.Close()
        assert.Equal(t, http.StatusOK, resp.StatusCode)
        assert.Nil(t, err)
        assert.NotNil(t, resp)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Use case – edge cases of the BookSwap application"*

---

### Generics — Core Components

**Principle:** Go 1.18 generics add type parameters (`[T Constraint]`) for reusable, type-safe code.

- **Type parameters** — placeholders like `T`.
- **Type constraints** — `any`, `comparable`, type sets (`int64 | float64`), `~T` for underlying type, custom interfaces, `constraints` package.
- **Type arguments** — supplied at call site.
- **Type inference** — compiler derives types when possible.

**Code:**
```go
func sum[T any](x, y T) T {
    // implementation
}
```
```go
func sum[T comparable](x, y T) T {
    // implementation
}
```
```go
func sum[T int64 | float64](x, y T) T {
    // implementation
}
```
```go
type Number interface {
    int64 | float64
}
func sum[T Number](x, y T) T {
    // implementation
}
```
```go
type Number interface {
    ~int64 | ~float64
}
```
```go
func sum[T constraints.Signed](x, y T) T {
    // implementation
}
```
*Ref: Test-Driven_Development_in_Go.md — "Generics in Go" / "Exploring type constraints"*

---

### Generic `GetSortedValues` for Any `~int` Key

**Code:**
```go
// GetSortedValues returns the key-sorted values of a given map.
func GetSortedValues[K ~int, V comparable](input map[K]V, dir SortDirection) ([]V, error) {
    // implementation
}
```
*Ref: Test-Driven_Development_in_Go.md — "Writing generic code in Go"*

---

### Generic Table-Driven Tests

**Step 1 — generic test case type:**
```go
type testCase[K ~int, V comparable] struct {
    input map[K]V
}
```

**Step 2 — multiple typed case maps:**
```go
type CustomI int
testStrings := map[string]testCase[int, string]{
    "unordered":      {input: map[int]string{99: "A", 50: "X"}},
    "empty map":      {input: map[int]string{}},
    "negative values": {input: map[int]string{-99: "A", -1: "X"}},
}
testFloats := map[string]testCase[CustomI, float64]{
    "unordered":    {input: map[CustomI]float64{99: 1.2, 0: 4.6}},
    "empty map":    {input: map[CustomI]float64{}},
    "negative keys": {input: map[CustomI]float64{-99: 1.2, 0: 4.6}},
}
```

**Step 3 — generic run helper:**
```go
func runTests[K ~int, V comparable](t *testing.T, tests map[string]testCase[K, V]) {
    t.Helper()
    for name, rtc := range tests {
        tc := rtc
        t.Run(name, func(t *testing.T) {
            keys := make([]K, 0, len(tc.input))
            for k := range tc.input {
                keys = append(keys, k)
            }
            sort.Slice(keys, func(i, j int) bool {
                return keys[i] < keys[j]
            })
            sortedValues, err := gs.GetSortedValues(tc.input, gs.ASC)
            require.Nil(t, err)
            require.NotNil(t, sortedValues)
            for index, v := range sortedValues {
                key := keys[index]
                assert.Equal(t, tc.input[key], v)
            }
        })
    }
}
```

**Step 4 — top-level test:**
```go
func TestGetSortedValues(t *testing.T) {
    t.Run("[int]string", func(t *testing.T) {
        testStrings := map[string]testCase[int, string]{
            // values declaration
        }
        runTests(t, testStrings)
    })

    t.Run("[CustomI]float64", func(t *testing.T) {
        testFloats := map[string]testCase[CustomI, float64]{
            // values declaration
        }
        runTests(t, testFloats)
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Table-driven testing revisited"*

---

### Generic Test Utilities

**Principle:** Generics replace reflection-based helpers with type-safe, reusable test utilities.

**Code:**
```go
func AssertMapOrderedByKeys[K ~int, V comparable](t *testing.T, input map[K]V, want []V) {
    t.Helper()
    keys := make([]K, 0, len(input))
    for k := range input {
        keys = append(keys, k)
    }
    sort.Slice(keys, func(i, j int) bool {
        return keys[i] < keys[j]
    })
    for index, v := range want {
        key := keys[index]
        assert.Equal(t, input[key], v)
    }
}
```
*Ref: Test-Driven_Development_in_Go.md — "Test utilities"*

---

### Generics in the BookSwap Application — Typed Response

**Code:**
```go
type Response struct {
    Message string    `json:"message,omitempty"`
    Error   string    `json:"error,omitempty"`
    Books   []db.Book `json:"books,omitempty"`
    User    *db.User  `json:"user,omitempty"`
}
```
```go
type ResponseItemType interface {
    db.Book | db.Magazine
}
```
```go
type Response[T ResponseItemType] struct {
    Message string   `json:"message,omitempty"`
    Error   string   `json:"error,omitempty"`
    Items   []T      `json:"items,omitempty"`
    User    *db.User `json:"user,omitempty"`
}
```
```go
func writeResponse[T ResponseItemType](w http.ResponseWriter, status int, resp *Response[T]) {
    // implementation
}
```
```go
// ListBooks is invoked by HTTP GET /books.
func (h *Handler) ListBooks(w http.ResponseWriter, r *http.Request) {
    books, err := h.bs.List()
    if err != nil {
        writeResponse(w, http.StatusInternalServerError, &Response[db.Book]{
            Error: err.Error(),
        })
        return
    }
    // Send an HTTP status & the list of books
    writeResponse(w, http.StatusOK, &Response[db.Book]{
        Items: books,
    })
}
```
*Ref: Test-Driven_Development_in_Go.md — "Extending the BookSwap application with generics"*

---

## Anti-Patterns & Common Mistakes

- **Writing tests after the code and calling it TDD** → *fix:* always red first.
- **Mixing Red/Green/Refactor mindsets** → *fix:* one mindset per phase.
- **Testing implementation, not behavior** → *fix:* "different implementations" thought experiment.
- **Sharing state across tests** → *fix:* each test builds its own UUT.
- **Reaching into unexported state from tests** → *fix:* use the `<pkg>_test` external package.
- **Mocking databases** → *fix:* run the real DB in a container.
- **Forgetting `os.Exit(m.Run())` in `TestMain`** → *fix:* always propagate the exit code.
- **Forgetting `tc := rtc` in parallel table tests** → *fix:* capture the loop variable.
- **Forgetting `AssertExpectations` on mocks** → *fix:* call it on every mock.
- **Comparing errors by full message string** → *fix:* use custom error types + `errors.As`.
- **Overusing `mock.Anything`** → *fix:* prefer `mock.AnythingOfType`.
- **Asserting on full error messages from `fmt.Errorf`** → *fix:* assert on substrings or custom types.
- **Sharing one DB across microservices** → *fix:* dedicated storage per service.
- **Treating race-detector runs as proof** → *fix:* design-first concurrency discipline.
- **Big-bang refactors over hours** → *fix:* small behavior-preserving steps.
- **Optimizing for 100% coverage** → *fix:* ~80% as a healthy target.

*Ref: Test-Driven_Development_in_Go.md — across all chapters*

---

## Decision Heuristics / Checklists

- **Start with a test?** Yes for any new code or behavior change.
- **Which package type?** External `<pkg>_test` package by default.
- **Setup scope?** Use `init` (setup only), `TestMain` (setup + teardown), or `defer` (per-test).
- **Many similar test cases?** Use a table-driven test with `map[string]struct{...}`.
- **Need parallelism?** `t.Parallel()` + `tc := rtc` capture.
- **Mocking strategy?** `testify/mock` + `mockery` generated mocks for interfaces.
- **Assertion failure stops the test?** `require.*` (fatal) vs `assert.*` (continue).
- **Slow integration tests?** Gate them with `LONG=true` env var; default to fast.
- **HTTP handler tests?** `httptest.NewServer` + `http.Get/Post` + JSON unmarshal into typed response.
- **Database tests?** Real PostgreSQL in Docker + GORM; never mock.
- **BDD-style tests?** Ginkgo for unit/integration; Godog for E2E feature files.
- **Monolith → microservices?** Define boundaries, separate DBs, async comms, contract testing with Pact.
- **Error verification?** Custom error type + `errors.As` is preferred.
- **Concurrency correctness?** Channels over shared memory, `defer` unlock, `sync.WaitGroup` for child completion; race-detector in CI.
- **Edge-case coverage?** Fuzz tests for untrusted inputs; property-based tests for invariants.
- **Generic code?** Generic table-driven tests with multiple typed case maps.
- **Refactoring?** Small steps, run tests after each, IDE rename + compiler as guides.

---

## Key Takeaways

1. **Red-Green-Refactor is the loop** — never write code without a failing test demanding it.
2. **Test behavior, not implementation** — keep tests stable through refactors.
3. **Use the external `<pkg>_test` package** — forces black-box-style testing of exported APIs.
4. **Table-driven tests** are the canonical Go pattern for covering many scenarios concisely.
5. **Wrap dependencies in interfaces** defined on the consumer side — enables mocking and loose coupling.
6. **Generate mocks with `mockery`** and verify with `AssertExpectations`.
7. **`testify` `assert` vs `require`** — continue vs fatal; choose deliberately.
8. **Integration tests with `httptest`** bring realistic HTTP coverage at low cost.
9. **Use `LONG=true` or `testing.Short()`** to keep the default `go test` fast.
10. **BDD via Ginkgo (unit/integration) and Godog (E2E)** makes tests readable to non-engineers.
11. **Never mock databases** — run real PostgreSQL in Docker with `golang-migrate` + GORM.
12. **Docker Compose** is the simplest reproducible environment for Go + DB.
13. **Refactoring is behavior-preserving** — done in small steps with green tests throughout.
14. **Custom error types + `errors.As`** beats string-matching for robust error verification.
15. **Microservices need contract testing** — Pact records consumer expectations and verifies them on the provider.
16. **Performance benchmarks + `pprof`** reveal real bottlenecks; integrate `pprof` into the server in debug mode.
17. **Concurrent code demands three disciplines:** share by communicating, `defer` unlocks, wait for all children.
18. **`go test -race`** is essential in CI but cannot prove the absence of races.
19. **Robust code** = transparent, simple, well-typed, nil-safe, error-returning.
20. **Fuzz tests** (Go 1.18+) generate inputs you wouldn't think to write; property-based testing with `testing/quick` covers invariants.
21. **Generics** enable type-safe table-driven tests and reusable test utilities without reflection.
22. **No testing strategy is perfect** — prioritize user journeys, document NFRs, and refactor "little and often".

---

## Cross-References
- Related: [[../100_Go_Mistakes.md]]
- Related: [[../Concurrency_in_Go.md]]
- Related: [[../Learning_Go.md]]
- Related: [[../The_Art_of_Unit_Testing.md]]
- Related: [[../TDD_Top_Tips.md]]
- Related: [[../What_to_Test_and_When.md]]
- Related: [[../Fundamentals_of_Software_Testing.md]]
- Related: [[../ATDD_Guide.md]]
- Topic index: [[../INDEX.md]]
