# The Art of Unit Testing, Third Edition
**Author:** Roy Osherove (with Vladimir Khorikov)
**Topic tags:** `#testing` `#unit-testing` `#test-design` `#test-doubles` `#mocking` `#tdd` `#test-strategy` `#legacy-code` `#ci`
**Language focus:** Language-agnostic (examples in JavaScript / TypeScript with Jest & substitute.js; patterns transfer to Java, C#, Python, Go, Ruby)
**Sources:** `markdown_output/The_Art_of_Unit_Testing_3E_-_Roy_Osherove/The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md` · `summaries/The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md`

## TL;DR
A unit test is an automated piece of code that invokes a *unit of work* through an *entry point* and checks one specific *exit point* (return value, state change, or third-party call). Good tests are **trustworthy, readable, and maintainable**; they run fast, in memory, with full control over all dependencies. Stubs break *incoming* dependencies (never assert against them); mocks break *outgoing* dependencies (at most one per test). Prefer return-value/state-based tests over interaction tests. Avoid logic, overspecification, and `beforeEach` setup bloat in favor of factory methods and parameterized tests.

---

## Best Practices by Topic

### Unit of Work, Entry Points & Exit Points

**Principle:** Test a *unit of work* (use case), not a function. A unit of work spans from an *entry point* (public API you trigger) to one or more *exit points* (observable end results). It may cross functions, modules, or classes.

**Do:**
- Identify entry points (public functions/methods/constructors) and exit points before writing a test.
- Treat each exit point as a separate requirement → write a separate test per exit point.
- Choose the testing technique based on exit-point type:
  - Return value → value-based test (easiest, preferred).
  - State change → state-based test (query a sibling).
  - Third-party call → interaction test with a mock (hardest; minimize).

**Don't:**
- Don't equate "unit" with "method" — a unit of work can span many functions/classes.
- Don't test purely internal behavior that has no public exit point.

**Code:**
```javascript
// Three exit points in one function: return value, state change, third-party (logger) call
let total = 0;
const totalSoFar = () => { return total; };
const logger = makeLogger();
const sum = (numbers) => {
  const [a, b] = numbers.split(',');
  logger.info('this is a very important log output',
              { firstNumWas: a, secondNumWas: b });   // exit point #3: third-party call
  const result = parseInt(a) + parseInt(b);
  total += result;                                    // exit point #2: state change
  return result;                                      // exit point #1: return value
};
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 1.3 Adding a logger call to the function" / "1.4 Exit point types"*

---

### Characteristics of a Good Unit Test

**Principle:** Every good unit test is automated, fast, isolated, in-memory, controllable, consistent, readable, maintainable, and trustworthy.

**Do (checklist — answer "yes" to all):**
- Can I run and get results from a test I wrote months ago?
- Can any teammate run it and get the same results?
- Can I run all tests in a few minutes at the push of a button?
- Can I write a basic test in a few minutes?
- Do tests pass when there are bugs in another team's code?
- Do tests show the same results on different machines?
- Do tests keep working with no database, network, or deployment?
- If I delete/move/change one test, do the others stay unaffected?

**Don't:**
- Don't use in-memory databases as a halfway house — they aren't as easy as stubs and don't match the real DB; prefer stubs for unit tests or real DBs for integration tests.
- Don't add parallel threads to unit tests when sync/linear is possible.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.7 Characteristics of a good unit test" / "1.7.2 A unit test checklist"*

---

### Unit vs. Integration Tests — Final Definition

**Principle:** *Integration testing* is testing a unit of work **without full control** over its real dependencies (network, FS, DB, time, threads, RNG). *Unit testing* is the same thing with all dependencies in memory and under your control.

> A unit test is an automated piece of code that invokes the unit of work through an entry point and then checks one of its exit points. A unit test is almost always written using a unit testing framework. It can be written easily and runs quickly. It's trustworthy, readable, and maintainable. It is consistent as long as the production code we control has not changed.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.8 Integration tests" / "1.9 Finalizing our definition"*

---

### TDD — Test-Driven Development

**Principle:** TDD = write a failing test → write minimal production code to pass → refactor. Its biggest benefit is *verifying the test itself*: you see it fail when it should and pass when it should.

**Do:**
- Learn the **three core skills separately**: (1) writing good tests, (2) writing them test-first, (3) design for testability.
- Use TDD to gain trust — seeing the test fail first is the only way to know it would catch a regression.
- Refactor in tiny steps; run all tests after each.

**Don't:**
- Don't assume TDD guarantees good tests — you can TDD terrible tests.
- Don't conflate TDD with "having lots of tests."

**Three-step loop:**
1. Write a failing test that proves the functionality is missing.
2. Make the test pass with the simplest possible production code (don't touch the test).
3. Refactor production code and tests (no behavior change); run tests after each step.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.10 Test-driven development" / "1.10.2 Three core skills needed for successful TDD"*

---

### Test Design — Arrange-Act-Assert (AAA)

**Principle:** Every test follows three visible phases: **Arrange** (set up inputs/state), **Act** (invoke the entry point), **Assert** (check the exit point). Keep them separated and visually distinct.

**Do:**
- Use blank lines between the three sections.
- Make inputs so simple that the expected output is trivially hardcoded.
- After a test passes, deliberately introduce a bug in production code to confirm the test catches it (testing the test).

**Don't:**
- Don't merge act and assert on one line — destroys readability and debuggability.

**Code:**
```javascript
test('verifyPassword, given a failing rule, returns errors', () => {
  // Arrange
  const fakeRule = input => ({ passed: false, reason: 'fake reason' });
  // Act
  const errors = verifyPassword('any value', [fakeRule]);
  // Assert
  expect(errors[0]).toContain('fake reason');
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 2.3 The first test against verifyPassword()" / "2.5.1 The Arrange-Act-Assert pattern"*

**Anti-example — separate asserts from actions:**
```javascript
// BAD - act and assert in one line
expect(verifier.verify("any value")[0]).toContain("fake reason");
// GOOD - separated
const result = verifier.verify("any value");
expect(result[0]).toContain("fake reason");
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 9.5 Separating asserts from actions"*

---

### Test Naming — USE Convention

**Principle:** A test name must contain three pieces of information: **U**nit under test + **S**cenario (inputs) + **E**xpected behavior. Test names are executable documentation and the only thing visible in CI failure logs.

**Do:**
- Put the unit-of-work name first (aids IDE auto-complete and alphabetical grouping).
- Use `describe()`/`context()` blocks to nest Unit → Scenario, with `it()` for the expectation.
- Make the name readable as a sentence: "verifyPassword, with a failing rule, returns errors."

**Don't:**
- Don't use generic names like `test1`, `itWorks`, `badly named test`.
- Don't drop one of the three pieces — the reader will have to open the test body.

**Code — same USE info, three valid layouts:**
```javascript
test('verifyPassword, with a failing rule, returns error based on rule.reason', () => { /*...*/ })

describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns error based on the rule.reason', () => { /*...*/ })
  })
})

verifyPassword_withFailingRule_returnsErrorBasedOnRuleReason()
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.5.3 USE naming" / "Listing 9.1 Same information, different variations"*

---

### Test Doubles — Stubs vs. Mocks vs. Fakes

**Principle:** A **stub** breaks *incoming* dependencies (provides fake data/behavior INTO the SUT; never assert against it; many allowed). A **mock** breaks *outgoing* dependencies (asserts a call was made correctly; at most one per test). A **fake** / **test double** is the generic term for anything not real.

**Do:**
- Name fakes by role: `mockXXX` only for things you assert against; `stubXXX` for things that feed data in; `fakeXXX` / `FakeLogger` for reusable doubles that may serve either role.
- Have many stubs, at most one mock per test.
- Prefer value-based or state-based tests; aim for mocks in only ~2–5% of tests.

**Don't:**
- Don't assert against a stub — that's overspecification.
- Don't use the word "mock" as a catch-all (it muddles the rule of "one mock per test").

**Terminology table (per *xUnit Test Patterns*):**

| Category | Pattern | Purpose |
|----------|---------|---------|
| Test double | Dummy / Stub / Spy / Mock / Fake | Generic stand-in for a real dependency |
| Stub | Dummy object | Irrelevant parameter argument |
| Stub | Test stub | Provides fake indirect inputs |
| Mock | Test spy | Captures indirect outputs for later verification |
| Mock | Mock object | Verifies indirect outputs were sent correctly |

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "3.1 Types of dependencies" / Table 3.1 / "4.4 The importance of differentiating between mocks and stubs"*

---

### Handwritten Mock — Minimal Pattern

**Principle:** A handwritten mock is a tiny object with a function that captures the args so you can assert later. Only name it `mockXxx` if you actually verify against it.

**Code:**
```javascript
describe('password verifier with logger', () => {
  describe('when all rules pass', () => {
    it('calls the logger with PASSED', () => {
      let written = '';
      const mockLog = {
        info: (text) => { written = text; }    // capture for later assertion
      };
      verifyPassword2('anything', [], mockLog);
      expect(written).toMatch(/PASSED/);
    });
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 4.3 Handwritten mock object"*

---

### Isolation & Seams — Dependency Injection Techniques

**Principle:** A **seam** (Michael Feathers) is a place where you can alter behavior without editing in that place. Use seams to inject fakes: parameters, functions, factory/curried functions, modules, class constructors, object parameters (duck typing), or typed interfaces.

**Do — pick the lightest seam that works:**
- **Parameter injection** (functional, simplest): add the dependency as a parameter → makes the function pure.
- **Function as parameter**: pass `getDayFn()` instead of a value (allows simulating exceptions).
- **Partial application / currying / factory function**: returns a preconfigured function.
- **Constructor function / class constructor injection**: explicit, required dependencies (OO).
- **Object as parameter (duck typing)**: replace one object with another that has the same method(s).
- **Common interface (TypeScript/Java/C#)**: contract-checked fakes (strongest design clarity).
- **Module injection**: least preferred — couples tests to the third-party module's API signature.

**Don't:**
- Don't `require()`/`import` third-party dependencies directly in code you control — wrap them behind an internal adapter (Ports & Adapters / Hexagonal).
- Don't over-engineer with IoC containers in tests; manual factory functions are clearer.

**Code — parameter injection (time dependency):**
```javascript
const verifyPassword2 = (input, rules, currentDay) => {
  if ([SATURDAY, SUNDAY].includes(currentDay)) {
    throw Error("It's the weekend!");
  }
  return [];
};
describe('verifier2 - dummy object', () => {
  test('on weekends, throws exceptions', () => {
    expect(() => verifyPassword2('anything', [], SUNDAY))
      .toThrow("It's the weekend!");
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 3.3 verifyPassword with a currentDay parameter"*

**Code — factory function (higher-order):**
```javascript
const makeVerifier = (rules, dayOfWeekFn) => {
  return function (input) {
    if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
      throw new Error("It's the weekend!");
    }
  };
};
test('factory method: on weekends, throws exceptions', () => {
  const alwaysSunday = () => SUNDAY;
  const verifyPassword = makeVerifier([], alwaysSunday);
  expect(() => verifyPassword('anything')).toThrow("It's the weekend!");
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 3.6 Using a higher-order factory function"*

**Code — modular inject/reset seam (use sparingly; couples to third-party API):**
```javascript
const originalDependencies = { moment: require('moment') };
let dependencies = { ...originalDependencies };
const inject = (fakes) => {
  Object.assign(dependencies, fakes);
  return function reset() { dependencies = { ...originalDependencies }; };
};
// in test:
const reset = inject({ moment: () => ({ day: () => SATURDAY }) });
// ... call production code ...
reset();
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 3.7 Abstracting the required dependencies"*

**Code — OO constructor injection + common interface (TypeScript):**
```typescript
export interface TimeProviderInterface { getDay(): number; }
export class RealTimeProvider implements TimeProviderInterface {
  getDay(): number { return moment().day(); }
}
export class PasswordVerifier {
  private _timeProvider: TimeProviderInterface;
  constructor(rules: any[], timeProvider: TimeProviderInterface) {
    this._timeProvider = timeProvider;
  }
  // ...
}
// test handwritten fake:
class FakeTimeProvider implements TimeProviderInterface {
  fakeDay: number;
  getDay(): number { return this.fakeDay; }
}
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 3.14 Extracting a common interface in production code"*

---

### Isolation Frameworks (Mocking Libraries)

**Principle:** An isolation framework dynamically creates and configures fakes. Two flavors: **loose** (Jest, Sinon — function/module friendly) and **typed** (substitute.js — class/interface friendly). Use them to remove boilerplate, but remember the same stub/mock rules still apply.

**Do:**
- Use `jest.mock("./module")` at the top of the spec to fake a whole module.
- Use `jest.fn()` for single-function fakes; configure returns via `mockReturnValue` / `mockReturnValueOnce` / `mockImplementation`.
- Use `Substitute.for<T>()` for full OO interfaces (auto-handles methods you don't care about).
- Wrap fake creation in helper/factory functions to keep tests readable.
- Reset between tests: `afterEach(jest.resetAllMocks)`.

**Don't:**
- Don't use isolation frameworks as a license to add mocks everywhere — they make overspecification easy.
- Don't use `jest.mock()` to fake modules you control — abstract them behind your own adapter first.
- Don't use Jest manual mocks (`__mocks__/`) — high maintenance cost, low readability.

**Code — faking a whole module with Jest:**
```javascript
jest.mock("./complicated-logger");
jest.mock("./configuration-service");
const { stringMatching } = expect;
const { verifyPassword } = require("./password-verifier");
const mockLoggerModule = require("./complicated-logger");
const stubConfigModule = require("./configuration-service");

describe("password verifier", () => {
  afterEach(jest.resetAllMocks);
  test('with info log level and no rules, it calls the logger with PASSED', () => {
    stubConfigModule.getLogLevel.mockReturnValue("info");     // stub
    verifyPassword("anything", []);
    expect(mockLoggerModule.info)                              // mock verify
      .toHaveBeenCalledWith(stringMatching(/PASS/));
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.2 Faking the module APIs directly with jest.mock()"*

**Code — `jest.fn()` for single functions:**
```javascript
test('given logger and passing scenario', () => {
  const mockLog = { info: jest.fn() };
  const verify = makeVerifier([], mockLog);
  verify('any input');
  expect(mockLog.info).toHaveBeenCalledWith(stringMatching(/PASS/));
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.4 Using jest.fn() for simple function mocks"*

**Code — stubbing return values / sequences:**
```javascript
const stubFunc = jest.fn().mockReturnValue("abc");            // permanent
const stubSeq  = jest.fn()
  .mockReturnValueOnce("a")
  .mockReturnValueOnce("b")
  .mockReturnValueOnce("c");                                  // sequential

yourStub.mockImplementation(() => { throw new Error(); });    // simulate errors
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.9 Stubbing a value from a fake function with jest.fn()"*

**Code — typed fakes with substitute.js:**
```typescript
import { Substitute, Arg } from "@fluffy-spoon/substitute";
const mockLog = Substitute.for<IComplicatedLogger>();
const verifier = new PasswordVerifier2([], mockLog);
verifier.verify("anything");
mockLog.received().info(
  Arg.is((x) => x.includes("PASSED")),
  "verify"
);
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.8 Using substitute.js to fake a full interface"*

---

### Stub + Mock Together (OO example)

**Code:**
```typescript
const stubMaintWindow = Substitute.for<MaintenanceWindow>();
stubMaintWindow.isUnderMaintenance().returns(true);   // stub: feeds data in
const mockLog = Substitute.for<IComplicatedLogger>();  // mock: assert call
const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
verifier.verify("anything");
mockLog.received().info("Under Maintenance", "verify");
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.11 Testing Password Verifier with substitute.js"*

---

### Complicated Interfaces — Interface Segregation Principle (ISP)

**Principle:** Don't fake a 4-method `IComplicatedLogger` in 100 tests. Define a tiny role-specific interface (e.g. `ILogger { info(text) }`) that only exposes what the consumer needs, and fake that. Now tests survive third-party API churn.

**Don't:**
- Don't fake interfaces you don't control — wrap them in an internal adapter first.
- Don't fake long interfaces directly — they have more reasons to change.

**Code — handwritten fake for a long interface is boilerplate-heavy; prefer ISP:**
```typescript
export interface IComplicatedLogger {         // long, third-party-like
  info(text: string, method: string)
  debug(text: string, method: string)
  warn(text: string, method: string)
  error(text: string, method: string)
}
// ISP fix: extract just what PasswordVerifier needs
export interface ILogger { info(text: string) }
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "4.8 Dealing with complicated interfaces" / "4.8.4 The interface segregation principle"*

---

### Partial Mocks (Extract and Override)

**Principle:** A *partial mock* overrides one function on a real object while leaving the rest real. Useful for legacy code; risky — keep it rare.

**Code — OO via inheritance:**
```javascript
class TestableLogger extends RealLogger {
  logged = "";
  info(text) { this.logged = text; }    // override only info; error/debug stay real
}
test("verify with logger, calls logger", () => {
  const mockLog = new TestableLogger();
  const verifier = new PasswordVerifier([], mockLog);
  verifier.verify("any input");
  expect(mockLog.logged).toMatch(/PASSED/);
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 4.18 An object-oriented partial mock example"*

---

### Testing Asynchronous Code

**Principle:** Async forces explicit waiting. Two refactoring patterns make async unit-testable: **Extract Entry Point** (split pure logic out of the async orchestration) and **Extract Adapter** (wrap the async dependency behind a synchronous-looking seam).

**Do:**
- Keep one or two integration tests against the original async entry point for confidence.
- Test every scenario as a synchronous unit test against the *extracted* pure logic.
- Use `async/await` in tests (cleaner than `done()`/`.then()`).
- Fake timers with `jest.useFakeTimers()` + `jest.advanceTimersToNextTimer()`; reset with `jest.clearAllTimers`.

**Don't:**
- Don't pepper all scenarios as integration tests — they're slow and flaky.
- Don't assert on event subscriptions alone — verify an observable state change.

**Code — Extract Entry Point (callback version):**
```javascript
// pure extracted entry points (unit-testable synchronously)
const processFetchSuccess = (text, callback) => {
  if (text.includes("illustrative")) callback({ success: true, status: "ok" });
  else callback({ success: false, status: "missing text" });
};
const processFetchError = (err, callback) => {
  callback({ success: false, status: err });
};
// original async orchestrator keeps one or two integration tests
const isWebsiteAlive = (callback) => {
  fetch("http://example.com")
    .then(throwOnInvalidResponse)
    .then((resp) => resp.text())
    .then((text) => processFetchSuccess(text, callback))
    .catch((err) => processFetchError(err, callback));
};
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.5 Extracting entry points with callback"*

**Code — Extract Entry Point (async/await version):**
```javascript
const processFetchContent = (text) => {
  const included = text.includes("illustrative");
  if (included) return { success: true, status: "ok" };
  return { success: false, status: "missing text" };
};
// test: no async, no await, no done()
test("on fetch success with good content, returns true", () => {
  const result = samples.processFetchContent("illustrative");
  expect(result.success).toBe(true);
  expect(result.status).toBe("ok");
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.7 / Listing 6.8"*

**Code — Extract Adapter (modular):**
```javascript
// network-adapter.js — the only file that imports node-fetch
const fetchUrlText = async (url) => {
  const resp = await fetch(url);
  if (resp.ok) return { ok: true, text: await resp.text() };
  return { ok: false, text: resp.statusText };
};
// test fakes the adapter module
jest.mock("./network-adapter");
const stubSyncNetwork = require("./network-adapter");
beforeEach(jest.resetAllMocks);
test("with good content, returns true", async () => {
  stubSyncNetwork.fetchUrlText.mockReturnValue({ ok: true, text: "illustrative" });
  const result = await webverifier.isWebsiteAlive();
  expect(result.success).toBe(true);
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.10 / Listing 6.11"*

**Code — fake timers (Jest):**
```javascript
describe("calculate1 - with jest", () => {
  beforeEach(jest.clearAllTimers);
  beforeEach(jest.useFakeTimers);
  test("fake timeout with callback", () => {
    Samples.calculate1(1, 2, (result) => { expect(result).toBe(3); });
    jest.advanceTimersToNextTimer();
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.19 Faking setTimeout with Jest"*

**Code — DOM events via Testing Library (query by user-visible text):**
```javascript
const { fireEvent, findByText, getByText } = require("@testing-library/dom");
test("dom test lib button click triggers change in page", () => {
  const { window, docElem, button } = loadHtmlAndGetUIElements();
  fireEvent.load(window);
  fireEvent.click(button);
  expect(findByText(docElem, "clicked", { exact: false })).toBeTruthy();
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.27 Using the DOM Testing Library in a simple test"*

---

### Trustworthy Tests — Avoid Logic in Tests

**Principle:** Any logic (`if`/`else`/`switch`/`for`/`while`/`try`/`catch`/string concatenation) inside a test is a likely bug in the test. The most dangerous form is *dynamically recomputing the expected value by repeating the production algorithm* — if the algorithm is wrong, the test enshrines the same bug.

**Do:**
- Hardcode expected values whenever inputs are simple enough.
- When trust clashes with maintainability, **trust wins** — a maintainable test you can't trust is worthless.
- Separate multi-input scenarios into separate tests with hardcoded expected outputs.
- After fixing a buggy test, introduce an obvious bug in production code to verify the test fails.

**Don't:**
- Don't write `expect(result).toBe("hello" + name)` — repeats production logic.
- Don't loop over inputs with `if`/`else` to pick the expected result.

**Code — BAD (repeats the algorithm):**
```javascript
const result = trust.makeGreeting("abc");
expect(result).toBe("hello" + name);           // same concatenation as production
// production:
const makeGreeting = (name) => { return "hello" + name; };
```
**Code — GOOD (hardcoded):**
```javascript
const result = trust.makeGreeting("abc");
expect(result).toBe("hello abc");
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 7.1 / 7.2 / 7.3"*

**Anti-pattern — loops + if/else in a test:**
```javascript
// BAD — production logic leaks into the test
const namesToTest = ["firstOnly", "first second", ""];
it("correctly finds out if it is a name", () => {
  namesToTest.forEach((name) => {
    const result = trust.isName(name);
    if (name.includes(" ")) expect(result).toBe(true);
    else                     expect(result).toBe(false);
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 7.5 Loops and ifs in a test"*

---

### Trustworthy Tests — Why Tests Fail

| Reason | What to do |
|--------|-----------|
| Real bug in production code | Celebrate — that's the job. |
| Buggy test gives false failure | Fix test, then *intentionally break production code* to confirm test catches it. |
| Test out of date (functionality changed) | Adapt or delete; consult product owner if unsure. |
| Test conflicts with another test | Remove the irrelevant one (ask the product owner which behavior is correct). |
| Test is flaky | Quarantine; then **fix, convert, or kill** (see §Flakiness). |

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "7.2 Why tests fail"*

---

### Trustworthy Tests — Smelling False Trust in Passing Tests

**Principle:** A passing test isn't automatically trustworthy. Five red flags:

1. **No asserts** — the test runs code but verifies nothing. Add an assert or remove the test; if it's a "does not throw" check, name it so and use `expect(() => fn()).not.toThrow()`.
2. **You can't understand the test** — bad names, hidden logic, magic values.
3. **Unit and flaky integration tests mixed** — devs learn to dismiss all failures. Separate them; keep a "safe green zone" of fast, non-flaky tests.
4. **Testing multiple exit points in one test** — name becomes generic; first failing assert hides the rest. Split.
5. **Tests that keep changing** — current time, RNG, machine name → each run is a different test. Stub them out.

**Splitting rule:** *If the first assert fails, do you still care about the next one?* If yes → split into two tests. Multiple asserts on the same concern (e.g. `name` and `age` of one returned object) are fine.

**Code — split exit points into separate tests:**
```javascript
describe("trigger", () => {
  it("triggers a given callback", () => {
    const callback = jest.fn();
    trigger(1, 2, callback);
    expect(callback).toHaveBeenCalledWith("I'm triggered");
  });
  it("sums up given values", () => {
    const result = trigger(1, 2, jest.fn());
    expect(result).toBe(3);
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "7.4 Smelling a false sense of trust" / "Listing 7.7 Checking the two exit points in separate tests"*

---

### Flaky Tests

**Principle:** Flakiness scales with the number of real dependencies: unit ≈ 0, integration moderate, E2E high. Long-term goal: **zero flaky tests**.

**Do — the "fix, convert, or kill" game:**
- **Define** flaky: run suite 10× unchanged; anything not 100% pass or 100% fail is flaky.
- Quarantine flaky tests into their own pipeline (remove from delivery-blocking build).
- **Fix** by controlling the dependency (inject data, stub the network).
- **Convert** to a lower-level test (replace real dependency with a stub).
- **Kill** if the test's value no longer justifies its maintenance cost (beware sunk-cost fallacy).

**Preventing flakiness in higher-level tests:**
- Roll back changes to shared resources after each test.
- Don't depend on other tests having mutated shared state.
- Make external systems recreatable (infra-as-code) or replace with fakes.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "7.5 Dealing with flaky tests"*

---

### Maintainability — Factory Methods Decouple Object Creation

**Principle:** When the production code's constructor or signature changes, every test that directly calls `new PasswordVerifier(...)` breaks. Centralize creation in **factory functions** so a signature change touches one place.

**Do:**
- One factory per object under test; one per fake (e.g. `makeFakeLogger()`).
- Default parameters let most tests call `makePasswordVerifier([])` with no logger arg.
- Combine with helper functions for repeated actions (`addDefaultUser()`).

**Code — refactor tests to factory functions:**
```javascript
describe("password verifier 1", () => {
  const makeFakeLogger = () => ({ info: jest.fn() });
  const makePasswordVerifier = (
    rules,
    fakeLogger = makeFakeLogger()
  ) => new PasswordVerifier(rules, fakeLogger);

  it("passes with zero rules", () => {
    const verifier = makePasswordVerifier([]);        // tests don't care about logger
    const result = verifier.verify("any input");
    expect(result).toBe(true);
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 8.4 Refactoring to factory functions"*

---

### Maintainability — Test Isolation (No Constrained Test Order)

**Principle:** Tests must not depend on each other. Test runners don't guarantee order. Shared mutable state (singletons, caches, DB rows) is the root cause.

**Do:**
- Reset shared resources in `beforeEach`/`afterEach` (e.g. `getUserCache().reset()`).
- Extract setup actions into reusable helper functions called from inside each test.
- Run a single test in isolation (`test.only`) to verify it doesn't rely on siblings.

**Don't:**
- Don't let one test populate a cache that a later test relies on.
- Don't share mutable variables across `it()` blocks.

**Code — refactored to remove order dependence:**
```javascript
const addDefaultUser = () =>
  getUserCache().addUser({ key: "a", password: "abc" });
const makeSpecialApp = () => new SpecialApp();

describe("Test Dependence v2", () => {
  beforeEach(() => getUserCache().reset());      // critical: isolate state
  describe("loginUser with loggedInUser", () => {
    test("user exists, login succeeds", () => {
      addDefaultUser();
      const app = makeSpecialApp();
      expect(app.loginUser("a", "abc")).toBe(true);
    });
    test("user missing, login fails", () => {
      const app = makeSpecialApp();
      expect(app.loginUser("a", "abc")).toBe(false);
    });
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 8.9 Refactoring tests to remove order dependence"*

---

### Maintainability — Avoid Testing Private/Protected Methods

**Principle:** Private methods are implementation details; testing them couples tests to internal changes (refactor → tests fail even though behavior is unchanged).

**Do — when a private method seems worth testing, choose one:**
- Test it through the public method that exercises it.
- Make it public (its contract is meaningful).
- Make a stateless private method public + static (utility contract).
- Extract it into a new class/module with its own public API.

**Don't:**
- Don't reach into private state via reflection/bracket access (`pv4["findFailedRules"]`) — that's overspecification.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "8.2.1 Avoid testing private or protected methods"*

---

### Maintainability — Keep Tests DRY, Avoid `beforeEach` Bloat

**Principle:** DRY applies to tests too — but readability trumps DRY when trade-offs collide. `beforeEach` becomes a "garbage bin" of unrelated setup; it can't take parameters or return values, and hides mocks/stubs from readers.

**Do:**
- Prefer **factory/helper methods** called from inside each test.
- For shared resource reset only, a minimal `beforeEach(() => resource.reset())` is acceptable.
- Use **parameterized tests** to dedupe when only inputs/outputs vary.

**Don't:**
- Don't initialize mocks/stubs in `beforeEach` — readers won't see them in the test body.
- Don't put test-specific state in a setup that runs for all tests.

**Code — `beforeEach` abuse (BAD):**
```javascript
describe("password verifier", () => {
  let mockLog;
  beforeEach(() => { mockLog = Substitute.for<IComplicatedLogger>(); });  // hidden from reader
  test("verify ... calls logger with PASS", () => {
    const verifier = new PasswordVerifier2([], mockLog);                  // where did mockLog come from?
    // ...
  });
});
```
**Code — inline initialization via helper (GOOD):**
```javascript
describe("password verifier", () => {
  test("verify ... calls logger with PASS", () => {
    const mockLog = makeMockLogger();                                     // visible, parameterizable
    const verifier = new PasswordVerifier2([], mockLog);
    verifier.verify("anything");
    mockLog.received().info(Arg.is((x) => x.includes("PASSED")), "verify");
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 9.6 / 9.7 / 9.8" / "8.2.3 Avoid setup methods"*

---

### Test Organization — Parameterized / Table-Driven Tests

**Principle:** Parameterized tests dedupe arrange + assert when only inputs/outputs change. Jest: `test.each` / `it.each`. Parameterize **only** when the scenario (type of input) is the same.

**Do:**
- Keep one scenario per parameterized test — split if some rows expect different behavior classes.
- Use the format string (`%s`, `%i`) so each row has a readable name in the report.

**Don't:**
- Don't lump different scenarios into one table to "save lines" — readability plummets.
- Don't parameterize across different output *behaviors* — only across input variations.

**Code:**
```javascript
describe('sum with parameterized tests', () => {
  test.each([
    ['1', 1],
    ['2', 2]
  ])('add ,for %s, returns that number', (input, expected) => {
    const result = sum(input);
    expect(result).toBe(expected);
  });
});
```
**Code — multi-arg rows:**
```javascript
test.each([ ['Abc', true], ['aBc', true], ['abc', false] ])
  ('given %s, %s ', (input, expected) => {
    const result = oneUpperCaseRule(input);
    expect(result.passed).toEqual(expected);
  });
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.9 Refactoring to parameterized tests" / "Listing 8.10"*

---

### Test Organization — Checking Thrown Errors

**Principle:** Don't write `try/catch` + `fail()` in tests. Use the framework's declarative form; match by regex/substring, not exact equality, for future-proofing.

**Code — BAD (verbose try/catch):**
```javascript
test('verify, with no rules, throws exception', () => {
  const verifier = makeVerifier();
  try {
    verifier.verify('any input');
    fail('error was expected but not thrown');
  } catch (e) {
    expect(e.message).toContain('no rules configured');
  }
});
```
**Code — GOOD (declarative, regex match):**
```javascript
test('verify, with no rules, throws exception', () => {
  const verifier = makeVerifier();
  expect(() => verifier.verify('any input'))
    .toThrowError(/no rules configured/);
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.10 Checking for expected thrown errors"*

---

### Test Readability — Magic Values

**Principle:** Unexplained literals (`0`, `[]`, `'jhGGu78!'`) force readers to guess. Wrap them in named constants, or use sentinel strings (`"anything"`, `"any input"`) that signal "this value does not matter."

**Code — magic values:**
```javascript
test('on weekends, throws exceptions', () => {
  expect(() => verifyPassword2("jhGGu78!", [], 0)).toThrowError("It's the weekend!");
});
```
**Code — fixed:**
```javascript
const SUNDAY = 0, NO_RULES = [];
test("on weekends, throws exceptions", () => {
  expect(() => verifyPassword2("anything", NO_RULES, SUNDAY))
    .toThrowError("It's the weekend!");
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "9.2 Magic values and naming variables"*

---

### Test Smells — Overspecification

**Principle:** An *overspecified* test asserts about internal implementation rather than observable behavior. It breaks on any internal change even though functionality is unchanged.

**Four forms to avoid:**
1. **Asserting private/internal state or internal function calls** — verify the real exit point (return value, state, third-party call) instead.
2. **Using stubs as mocks** — never assert that a stub was called.
3. **Asserting exact output and ordering** when only specific values matter — use partial matching; ignore order when irrelevant.
4. **String equality** when substring/regex would do.

**Code — internal-call overspecification (BAD):**
```javascript
const failedMock = jest.fn(() => []);
pv4["findFailedRules"] = failedMock;          // poking into protected method
pv4.verify("abc");
expect(failedMock).toHaveBeenCalled();        // verifying an internal call — useless
```
**Code — exact-order overspecification (BAD):**
```javascript
expect(results).toEqual([
  { input: "a", result: false },
  { input: "ab", result: false },
  { input: "abc", result: true },
  { input: "abcd", result: true },
]);
```
**Code — ignore schema and order (GOOD):**
```javascript
expect(results.length).toBe(4);
expect(findResultFor("a")).toBe(false);
expect(findResultFor("abc")).toBe(true);
```
**Code — substring vs exact string:**
```javascript
// BAD: any punctuation change breaks it
expect(msg).toBe("you have 2 failed rules.");
// GOOD: only the meaningful part is asserted
expect(msg).toMatch(/2 failed/);
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "8.3 Avoid overspecification" (Listings 8.11–8.18)*

---

### Test Strategy — Levels, Scorecards & Antipatterns

**Principle:** Higher test levels → more confidence but slower, flakier, harder to maintain. Use a **test scorecard** to compare options on five axes: complexity, flakiness, confidence-when-passes, maintainability, execution speed.

**Test-level scorecards (1=best, 5=worst on a given axis):**

| Level | Complexity | Flakiness | Confidence | Maintainability | Speed |
|-------|-----------|-----------|------------|-----------------|-------|
| Unit / Component (in memory) | 1 | 1 | 1 | 5 | 5 |
| Integration (in memory) | 2 | 2–3 | 2–3 | 3–4 | 3–4 |
| API (out of process) | 3 | 3–4 | 3–4 | 2–3 | 2–3 |
| E2E/UI isolated | 4 | 4 | 4 | 1–2 | 1–2 |
| E2E/UI system | 5 | 5 | 5 | 1 | 1 |

**Three organizational antipatterns:**
1. **End-to-end-only** — diminishing returns (2nd E2E adds a fraction of the 1st's confidence at full cost); creates *build whisperers*; "throw it over the wall" dev↔QA split; driven by sunk-cost fallacy.
2. **Low-level-only** — fast tests, but confidence never reaches "ship it," so people still manually test everything.
3. **Disconnected low-level and high-level** — both unit and E2E exist but duplicate scenarios and are owned by silos that don't communicate; worst of both worlds.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.1 Common test types and levels" / "10.2 Test-level antipatterns"*

---

### Test Strategy — Test Recipes

**Principle:** A **test recipe** is an informal 5–20-line plan, stored in the feature story, listing each scenario and the level at which it'll be tested. It is the team's "definition of done."

**Rules:**
- **Pair:** at least two people (dev + tester perspective) — never write alone.
- **Just in time:** create it right before coding the feature.
- **Faster wins:** prefer lower levels unless a high-level test is the only way to gain confidence.
- **Confidence check:** "If all these tests pass, will I feel good about this feature?" If not, add scenarios.
- **Revise freely:** recipes are living documents.
- **Don't repeat:** across features or across layers (variations go to lower levels).
- **Ratio target:** ~1 high-level test : 5+ lower-level tests.

**Example:**
```
User profile feature testing recipe
E2E  - Login, go to profile screen, update email, log out, log in with new email,
       verify profile screen updated
API  - Call UpdateProfile API with more complicated data
Unit - Check profile update logic with bad email
Unit - Profile update logic with same email
Unit - Profile serialization/deserialization
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.3 Test recipes as a strategy"*

---

### CI / Delivery Pipeline Strategy

**Principle:** Split pipelines into **delivery** (blocking, fast, deploy-on-green) and **discovery** (non-blocking, slow, KPI-finding). Parallelize aggressively. Run on every commit — never nightly.

**Do:**
- **Delivery pipeline** = delivery-blocking tests (unit, integration, E2E, security). Fast feedback; auto-deploys when green.
- **Discovery pipeline** = good-to-know tests (load, complexity scans, long-running nonfunctional). Runs in parallel; failures become backlog items, not blockers.
- Parallelize pipelines *and* stages *and* individual test suites (especially E2E).
- Use dynamic, ephemeral environments; throw money at parallelism, not at manual testers.

**Don't:**
- Don't do nightly builds — feedback must follow each commit.
- Don't gate delivery on good-to-know tests.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.4 Managing delivery pipelines"*

---

### Legacy Code — Where to Start

**Principle:** Build a **test-feasibility table**: rate each component on Logical Complexity (1–10), Dependency Level (1–10), and Priority (1–10). Ignore components below complexity ~3.

**Selection strategies:**
- **Easy-first** (fewer dependencies): quick wins, builds team confidence. Downside: hardest components remain when schedule pressure peaks. Good for inexperienced teams.
- **Hard-first** (most dependencies): each refactoring unblocks testability for neighbors; time-per-test declines quickly. Requires an experienced team.

**Process for adding tests to legacy code:**
1. Write integration tests against the existing system to capture current behavior (characterization tests).
2. Add a failing test for the new feature/fix.
3. Refactor in small chunks; run integration tests after each.
4. Over time, replace integration tests with focused unit tests as the code becomes testable.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "12.1 Where do you start adding tests?" / "12.2 Choosing a selection strategy" / "12.3 Writing integration tests before refactoring"*

---

### Monkey-Patching (Last Resort)

**Principle:** Monkey-patching globals (`Date.now`, `setTimeout`) is fragile and hurts parallelism. Use it only when you cannot refactor to add seams.

**Do (if forced):**
- Save the original, replace, **and** restore in `afterEach` — never inline, because a thrown assert will skip restoration.
- Prefer framework support: `jest.spyOn(obj, 'fn').mockImplementation(...)` + `jest.restoreAllMocks()` in `afterEach`.
- For per-test module faking use the **CFRA pattern**: Clear (`jest.resetAllMocks` / `jest.resetModules`) → Fake (`jest.mock` + `mockImplementation`) → Require (re-`require` the SUT after faking) → Act.

**Don't:**
- Don't use Jest manual mocks (`__mocks__/` folder).
- Don't fake modules you control — wrap them in an adapter first.

**Code — CFRA with Jest:**
```javascript
const dataModule = require('../my-data-module');
const { findRecentlyRebooted } = require('../machine-scanner4');
const fakeDataFromModule = (fakeData) =>
  dataModule.getAllMachines.mockImplementation(() => fakeData);
jest.mock('../my-data-module');

describe('findRecentlyRebooted', () => {
  beforeEach(jest.resetAllMocks);                       // Clear
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    fakeDataFromModule([                                // Fake
      { lastBootTime: new Date(2000,0,1), name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }
    ]);
    const result = findRecentlyRebooted(1, fromDate);   // Act
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
  });
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "appendix. Monkey-patching functions and modules" / "Listing A.6"*

---

## Anti-Patterns & Common Mistakes

- **Assertion roulette:** Multiple asserts in one test where failure of one hides the others → comment-out debugging roulette. *Fix:* split into separate `it()` blocks, one per exit point.
- **Asserting against a stub:** Verifying a stub was called is overspecification — it tests implementation, not behavior. *Fix:* assert on the real exit point only.
- **More than one mock per test:** Each mock is a separate requirement; multiple mocks make naming generic and hide failures. *Fix:* split into multiple single-purpose tests.
- **Logic inside tests** (`if`/`for`/`+`): introduces test bugs. *Fix:* hardcode expected values; use parameterized tests for input variation.
- **`beforeEach` as garbage bin:** hides setup from readers, becomes a soup of mostly-unused state. *Fix:* factory/helper methods called from inside each test.
- **Testing private methods:** couples tests to internals. *Fix:* test through public API, or extract to a new class, or make public.
- **Exact string/order/schema asserts:** brittle; break on cosmetic changes. *Fix:* `toMatch(/regex/)`, `toContain`, partial matchers, ignore order.
- **Mixing unit + flaky integration tests in one suite:** devs dismiss all failures. *Fix:* separate "safe green zone."
- **End-to-end-only strategy:** diminishing returns, build whisperers, throw-it-over-the-wall. *Fix:* test recipes, mostly lower-level.
- **Monkey-patching globals:** race conditions in parallel runs, restoration bugs. *Fix:* design seams (params/interfaces); reserve patching for code you don't own.
- **Coverage as a goal:** drives meaningless tests. *Fix:* measure escaped bugs, time-to-fix, defect density instead.
- **Constrained test order:** tests depend on prior tests' side effects. *Fix:* reset shared state in `beforeEach`; extract helpers; each test is self-contained.

---

## Decision Heuristics / Checklists

**Choosing a test level for a scenario (test recipe checklist):**
1. Is there *any* lower level that can prove this scenario? If yes → test it there.
2. Does the lower-level test duplicate an existing higher-level scenario? If yes → remove the duplication.
3. If all listed tests pass, do I feel confident the feature works? If not → add scenarios or move some up.
4. Target ratio: ~1 E2E : ~5–10 integration : ~50+ unit tests.

**Choosing a fake type:**
- Need to feed data IN and never assert → **stub**.
- Need to verify a call going OUT → **mock** (max one per test).
- Need a reusable double that does both across tests → **fake** (class `FakeXxx`).
- Real object with one method overridden → **partial mock** (legacy only).
- Tracking wrapper around the real impl → **spy** (verify inputs/outputs without changing behavior).

**Choosing an injection seam (lightest → heaviest):**
1. Parameter (value) — purest, easiest.
2. Function parameter.
3. Factory / curried higher-order function.
4. Constructor function (JS `new`).
5. Class constructor (OO).
6. Object parameter (duck typing).
7. Typed interface (TypeScript/Java/C#).
8. Module injection (`jest.mock`) — last resort, couples to third-party API.

**"Do I trust this test?" checklist:**
- It fails → am I worried? (yes = trust)
- It passes → am I relaxed? (yes = trust)
- If either is "no," inspect for: no asserts, unreadable code, mixed with flaky tests, multiple exit points, or dynamic values.

**Buggy-test recovery loop:**
1. Reproduce the failure.
2. Debug the *test* (not the production code) first.
3. Fix the test.
4. Intentionally break the production code path it covers.
5. Confirm the test now fails.
6. Restore production code; confirm test passes.
7. Repeat if it still misbehaves.

---

## Key Takeaways

1. **A unit test invokes a unit of work through an entry point and checks one exit point.** Exit points come in three types (return value, state change, third-party call) — each needs a different technique.
2. **Stubs feed data IN; mocks verify calls OUT.** Never assert against a stub. At most one mock per test. Aim for mocks in ≤5% of tests.
3. **AAA + USE naming** are the universal test skeleton: Arrange-Act-Assert visible phases; Unit + Scenario + Expected behavior in the name.
4. **Avoid logic in tests** — no `if`/`for`/`try`, no dynamic expected values. Hardcode. Trust > maintainability when they conflict.
5. **Design seams beat monkey-patching.** Parameters, factory functions, and constructor/interface injection make code testable *and* better designed.
6. **Prefer factory methods over `beforeEach`.** Tests read top-to-bottom; no scroll fatigue, no garbage-bin setup.
7. **Parameterize only when the scenario type is constant** — vary inputs/outputs, not behaviors.
8. **Three pillars: trustworthy, maintainable, readable.** Drop any one and the others fall.
9. **Avoid overspecification** — assert only observable behavior; use partial/regex matchers; ignore irrelevant schema/order.
10. **Quarantine flaky tests** and play *fix, convert, or kill*. Long-term goal: zero flaky tests.
11. **Use test recipes** to balance levels: mostly unit, some integration, few E2E. Split delivery (blocking) from discovery (non-blocking) pipelines; parallelize; run on every commit.
12. **For legacy code:** build a test-feasibility table, choose easy- or hard-first based on team experience, write characterization integration tests before refactoring.
13. **Metrics that matter:** escaped bugs, time-to-fix, defect density, trend lines — not raw coverage.
14. **TDD is a separate skill** from good unit testing and from design — learn all three independently.

---

## Cross-References
- Related: [[../Fundamentals_of_Software_Testing.md]] — ISTQB principles, test levels/types, black-box & white-box test design techniques.
- Topic index: [[../INDEX.md]]
