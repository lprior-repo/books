# The Art of Unit Testing, Third Edition — MAXIMUM-DEPTH Deep Dive
**Authors:** Roy Osherove (with Vladimir Khorikov)
**Topic tags:** `#testing` `#unit-testing` `#test-design` `#test-doubles` `#mocking` `#tdd` `#test-strategy` `#legacy-code` `#ci` `#refactoring` `#ddd` `#design-for-testability`
**Language focus:** Language-agnostic (examples in JavaScript / TypeScript with Jest & substitute.js; patterns transfer to Java, C#, Python, Go, Ruby, Rust)
**Sources:** `markdown_output/The_Art_of_Unit_Testing_3E_-_Roy_Osherove/The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md` · `summaries/The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md` (9541 lines; chapters 1–12 + monkey-patching appendix)

## TL;DR
A unit test is an automated piece of code that invokes a *unit of work* through an *entry point* and checks one specific *exit point* (return value, state change, or third-party call). Good tests are **trustworthy, readable, maintainable**, run fast, in memory, with full control over all dependencies. **Stubs break incoming dependencies (never assert against them); mocks break outgoing dependencies (at most one per test); fakes are reusable role-specific doubles; spies wrap real code with tracking; dummies are placeholders.** Avoid `if`/`for`/`try` in tests, avoid `beforeEach` bloat in favor of **factory methods**, avoid testing private methods, avoid overspecification (partial regex matching, ignore order/schema), and prefer **design seams** (parameters, factories, constructors, typed interfaces) over monkey-patching. For async code, use **Extract Entry Point** or **Extract Adapter** so logic becomes testable synchronously. For legacy code, build a **test-feasibility table** and go easy-first (inexperienced team) or hard-first (experienced team). Strategy: split **delivery** (blocking, fast, deploy-on-green) from **discovery** (non-blocking, slow, KPI) pipelines. For org change, identify champions and blockers, run time-boxed experiments, and track lagging (DORA) + leading (coverage/test-count) indicators together.

---

## Best Practices by Topic

### Unit of Work, Entry Points & Exit Points — The Three Primitives

**Principle:** Test a *unit of work* (a use case), not a function. A unit of work spans from an *entry point* (public API you trigger) to one or more *exit points* (observable end results). It may cross functions, modules, or classes — and that's fine.

**Do:**
- Identify entry points (public functions / methods / constructors) and exit points *before* writing a test.
- Treat each exit point as a separate requirement → write a separate test per exit point.
- Choose the testing technique based on exit-point type:
  - **Return value** → value-based test (easiest, preferred).
  - **State change** → state-based test (query a sibling).
  - **Third-party call** → interaction test with a mock (hardest; minimize).
- Quote Martin Fowler (*EAA*): "CUT = Component, class, or code under test."

**Don't:**
- Don't equate "unit" with "method" — a unit of work can span many functions/classes.
- Don't test purely internal behavior that has no public exit point.
- Don't pretend "exit point" is jargon — it is the language of xUnit Test Patterns and helps you notice hidden requirements.

**Code:**
```javascript
// Three exit points in one function: return value, state change, third-party call
let total = 0;
const totalSoFar = () => total;
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
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 1.3 Adding a logger call to the function" / "1.4 Exit point types" / *xUnit Test Patterns* definition*

---

### Characteristics of a Good Unit Test — Trustworthiness Checklist

**Principle:** Every good unit test is automated, fast, isolated, in-memory, controllable, consistent, readable, maintainable, and trustworthy. These are not aspirational — they are a checklist you apply to every test.

**Do (checklist — answer "yes" to all):**
- Can I run and get results from a test I wrote months ago?
- Can any teammate run it and get the same results?
- Can I run all tests in a few minutes at the push of a button?
- Can I write a basic test in a few minutes?
- Do tests pass when there are bugs in another team's code?
- Do tests show the same results on different machines?
- Do tests keep working with no DB / network / deployment?
- If I delete/move/change one test, do the others stay unaffected?

**Don't:**
- Don't use in-memory databases as a halfway house — they aren't as easy as stubs and don't match the real DB; prefer stubs for unit tests or real DBs for integration tests.
- Don't add parallel threads to unit tests when sync/linear is possible.
- Don't treat "the test runs" as "the test is trustworthy" — a missing assert still passes.

**Verification — confirm tests catch real bugs:**
```javascript
// Verify the test catches real bugs: deliberately introduce a regression,
// confirm the test now fails, then revert.
test('sum of two numbers, given valid input, returns the sum', () => {
  const result = sum('1,2');
  expect(result).toBe(3);
});
// mutate production: return parseInt(a) - parseInt(b);
// observe test fail. Revert.
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.7 Characteristics of a good unit test" / "1.7.2 A unit test checklist" / "7.1 How to know you trust a test"*

---

### Unit vs. Integration Tests — Final Definition

**Principle:** *Integration testing* is testing a unit of work **without full control** over its real dependencies (network, FS, DB, time, threads, RNG). *Unit testing* is the same thing with all dependencies in memory and under your control.

> A unit test is an automated piece of code that invokes the unit of work through an entry point and then checks one of its exit points. A unit test is almost always written using a unit testing framework. It can be written easily and runs quickly. It's trustworthy, readable, and maintainable. It is consistent as long as the production code we control has not changed.

**Implications:**
- A unit test that uses *some* real dependency (e.g., the filesystem but not the network) is *partially* an integration test.
- A "fast integration test" can still be valuable if it covers seams we cannot stub (third-party compiled modules without DI).
- Replace the database dependency with a stub for unit tests; keep one or two slow integration tests against the *real* DB for confidence.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.8 Integration tests" / "1.9 Finalizing our definition" / "Replacing the database with a stub" / "Emulating asynchronous processing with linear, synchronous tests"*

---

### TDD — Test-Driven Development (Three Distinct Skills)

**Principle:** TDD = write a failing test → write minimal production code to pass → refactor. Its biggest benefit is *verifying the test itself*: you see it fail when it should and pass when it should.

**Do:**
- Learn the **three core skills separately**: (1) writing good tests, (2) writing them test-first, (3) design for testability. Each is a learned practice.
- Use TDD to gain trust — seeing the test fail first is the only way to know it would catch a regression.
- Refactor in tiny steps; run all tests after each.
- After a test passes, **intentionally break production** to confirm the test fails — testing the test.
- Predict how the test will fail *before* you run it.

**Don't:**
- Don't assume TDD guarantees good tests — you can TDD terrible tests.
- Don't conflate TDD with "having lots of tests."
- Don't mix refactor with feature work during Green.

**Three-step loop:**
1. **Red** — Write a failing test that proves the functionality is missing. Fail for the *right* reason (feature absent, not typo).
2. **Green** — Make it pass with the simplest possible production code (don't touch the test).
3. **Refactor** — Improve production code and tests (no behavior change); run tests after each step.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "1.10 Test-driven development" / "1.10.1 TDD: Not a substitute for good unit tests" / "1.10.2 Three core skills needed for successful TDD"*

---

### Test Design — Arrange-Act-Assert (AAA) — Visible Phases

**Principle:** Every test follows three visible phases: **Arrange** (set up inputs/state), **Act** (invoke the entry point), **Assert** (check the exit point). Keep them separated and visually distinct. AAA exists so you can *find the assertion* at a glance during debugging.

**Do:**
- Use blank lines between the three sections.
- Make inputs so simple that the expected output is trivially hardcoded.
- Use AAA to debug — name each phase so a reader can mentally locate the assert.
- Use AAA to *test the test*: when the assert fails, immediately know whether Arrange was right, Act was right, or Assert itself is wrong.

**Don't:**
- Don't merge act and assert on one line — destroys readability and debuggability.
- Don't bury Arrange inside Act with argument lists the reader must parse.

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
**Anti-example — separate asserts from actions:**
```javascript
// BAD - act and assert in one line (longer, denser, hard to debug)
expect(verifier.verify("any value")[0]).toContain("fake reason");
// GOOD - separated
const result = verifier.verify("any value");
expect(result[0]).toContain("fake reason");
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 2.3 The first test" / "2.5.1 The Arrange-Act-Assert pattern" / "Listing 9.5 Separating asserts from actions"*

---

### Test Naming — USE Convention (Unit / Scenario / Expected)

**Principle:** A test name must contain three pieces of information: **U**nit under test + **S**cenario (inputs) + **E**xpected behavior. Test names are executable documentation and the only thing visible in CI failure logs.

**Do:**
- Put the unit-of-work name first (aids IDE auto-complete and alphabetical grouping).
- Use `describe()`/`context()` blocks to nest Unit → Scenario, with `it()` for the expectation.
- Make the name readable as a sentence: "verifyPassword, with a failing rule, returns errors."
- Include enough info that the team can diagnose the failure from the CI log alone — *no one reopens the test code in a red build*.
- The name serves as executable documentation: a new dev should be able to learn the system from test names.

**Don't:**
- Don't use generic names like `test1`, `itWorks`, `badly named test`.
- Don't drop one of the three pieces — the reader will have to open the test body.

**Code — same USE info, three valid layouts:**
```javascript
test('verifyPassword, with a failing rule, returns error based on rule.reason', () => { /* ... */ });

describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns error based on the rule.reason', () => { /* ... */ });
  });
});

verifyPassword_withFailingRule_returnsErrorBasedOnRuleReason()
```

**Code — bad name (missing info) — what's wrong:**
```javascript
test('failing rule, returns error based on rule.reason', () => { /* ... */ });  // ❶ missing Unit
test('verifyPassword, returns error based on rule.reason', () => { /* ... */ });  // ❷ missing Scenario
test('verifyPassword, with a failing rule,', () => { /* ... */ });               // ❸ missing Expected
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.5.3 USE naming" / "Listing 9.1 / 9.2 — same info, variations, and missing-information examples" / "9.1 Naming unit tests"*

---

### Test Doubles — Stubs vs. Mocks vs. Fakes vs. Spies vs. Dummies (Formal Taxonomy)

**Principle:** A **stub** breaks *incoming* dependencies (provides fake data/behavior INTO the SUT; never assert against it; many allowed). A **mock** breaks *outgoing* dependencies (asserts a call was made correctly; at most one per test). A **fake** / **test double** is the generic term for anything not real. A **spy** wraps a real implementation with tracking; a **dummy** is a placeholder argument.

**Do:**
- Name fakes by role: `mockXXX` *only* for things you assert against; `stubXXX` for things that feed data in; `fakeXXX` / `FakeLogger` for reusable doubles that may serve either role.
- Have many stubs, at most one mock per test.
- Prefer value-based or state-based tests; aim for mocks in only ~2–5% of tests.

**Don't:**
- Don't assert against a stub — that's overspecification.
- Don't use the word "mock" as a catch-all (it muddles the rule of "one mock per test").
- Don't confuse *spying* (tracking real calls) with *asserting against them* (mocking).

**Terminology table (per *xUnit Test Patterns* by Meszaros):**

| Category | Pattern | Purpose | Asserts? | Replaces? |
|----------|---------|---------|----------|-----------|
| Test double | Dummy | Placeholder argument | No | No |
| Test double | Stub | Provides fake indirect inputs | No | Yes |
| Test double | Fake | Full-working lightweight impl (in-mem DB) | Maybe | Yes |
| Test double | Spy | Captures inputs/outputs for later verification | Yes (post-hoc) | Sometimes (partial) |
| Test double | Mock | Verifies indirect outputs were sent correctly | Yes (definitionally) | Yes |

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "3.1 Types of dependencies" / Table 3.1 / "4.4 The importance of differentiating between mocks and stubs"*

---

### Handwritten Fakes / Mocks — Minimal Pattern

**Principle:** A handwritten mock is a tiny object with a function that captures the args so you can assert later. Only name it `mockXxx` if you actually verify against it.

**Code (functional capture mock):**
```javascript
describe('password verifier with logger', () => {
  describe('when all rules pass', () => {
    it('calls the logger with PASSED', () => {
      let written = '';
      const mockLog = {
        info: (text) => { written = text; }   // capture for later assertion
      };
      verifyPassword2('anything', [], mockLog);
      expect(written).toMatch(/PASSED/);
    });
  });
});
```

**Code (OO class fake — reusable across tests):**
```typescript
class FakeLogger implements ILogger {
  written = '';
  info(text: string) { this.written = text; }   // implement contract, don't log
}
test('verify, with logger, calls logger', () => {
  const mockLog = new FakeLogger();
  const verifier = new PasswordVerifier([], mockLog);
  verifier.verify('anything');
  expect(mockLog.written).toMatch(/PASS/);
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 4.3 Handwritten mock object" / "Listing 4.14 Injecting a handwritten mock ILogger" / "4.7 Mocks in an object-oriented style"*

---

### Isolation & Seams — Dependency Injection Techniques (Lightest → Heaviest)

**Principle:** A **seam** (Michael Feathers, *Working Effectively with Legacy Code*) is a place where you can alter behavior without editing in that place. Use seams to inject fakes: parameters, functions, factory/curried functions, modules, class constructors, object parameters (duck typing), or typed interfaces. **Aim to make production code testable by design — tests should change with intent, not with infrastructure.**

**Do — pick the lightest seam that works:**
- **Parameter injection** (functional, simplest): add the dependency as a parameter → makes the function pure.
- **Function as parameter**: pass `getDayFn()` instead of a value (allows simulating exceptions).
- **Partial application / currying / factory function**: returns a preconfigured function.
- **Constructor function / class constructor injection**: explicit, required dependencies (OO).
- **Object as parameter (duck typing)**: replace one object with another that has the same method(s).
- **Common interface (TypeScript/Java/C#)**: contract-checked fakes (strongest design clarity).
- **Module injection**: least preferred — couples tests to the third-party module's API signature.

**Don't:**
- Don't `require()`/`import` third-party dependencies directly in code you control — wrap them behind an internal adapter (Ports & Adapters / Hexagonal / Onion).
- Don't over-engineer with IoC containers in tests; manual factory functions are clearer.

**Code — parameter injection (time dependency) — the simplest seam:**
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

**Code — function-as-parameter injection — allows behavior simulation:**
```javascript
const verifyPassword3 = (input, rules, getDayFn) => {
  const dayOfWeek = getDayFn();
  if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
    throw Error("It's the weekend!");
  }
  return [];
};
describe('verifier3 - dummy function', () => {
  test('on weekends, throws exceptions', () => {
    const alwaysSunday = () => SUNDAY;
    expect(() => verifyPassword3('anything', [], alwaysSunday))
      .toThrow("It's the weekend!");
  });
});
```

**Code — factory function (higher-order) — the test's Arrange becomes one line:**
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

**Code — curried function — configuration + invocation split:**
```javascript
const makeVerifierCurried = (rules) => (dayOfWeekFn) => (input) => {
  if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
    throw new Error("It's the weekend!");
  }
  return [];
};
test('curried: with passing rules, returns empty errors', () => {
  const verifyPassword = makeVerifierCurried([])(() => MONDAY);
  expect(() => verifyPassword('anything')).not.toThrow();
});
```

**Code — modular inject seam (uses-and-resets pattern) — log a reset() for cleanup:**
```javascript
const originalDependencies = { moment: require('moment') };
let dependencies = { ...originalDependencies };
const inject = (fakes) => {
  Object.assign(dependencies, fakes);
  return function reset() { dependencies = { ...originalDependencies }; };
};
const verifyPassword4 = (input, rules) => {
  const dayOfWeek = dependencies.moment().day();
  if ([SATURDAY, SUNDAY].includes(dayOfWeek)) throw Error("It's the weekend!");
  return [];
};
// in test:
const reset = inject({ moment: () => ({ day: () => SATURDAY }) });
verifyPassword4('anything', []);
reset();
```

**Code — OO class + common interface (TypeScript) — strongest design clarity:**
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

**Why the lightest seam matters:** each step up the seam ladder adds ceremony. Parameter injection makes a function pure; factories enable pre-configuration; class injection encodes required-ness; interfaces make contracts explicit. **Don't skip to interfaces if a parameter works** — but don't shrink from interfaces when the dependency has many methods.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 3.3 / 3.4 / 3.5 / 3.6 / 3.7 / 3.9 / 3.10 / 3.11 / 3.14" / "3.4 Functional injection techniques" / "3.4.2 Dependency injection via partial application" / "3.5 Modular injection techniques" / "4.5 Modular-style mocks" / "4.7 Mocks in OO style"*

---

### Control, Inversion of Control, Dependency, Dependency Injection, Seam — Terminology Lock-In

**Principle:** Five terms, one concept.

| Term | Definition (verbatim-ish) |
|------|---------------------------|
| **Dependencies** | The things that make our testing lives (and code maintainability) difficult, since we cannot control them from our tests. Examples include time, the filesystem, the network, random values, and more. |
| **Control** | The ability to instruct a dependency how to behave. Whoever is *creating* the dependency is in control. |
| **Inversion of control** | Designing the code to remove the responsibility of creating the dependency internally, and externalizing it instead. |
| **Dependency injection** | The act of sending a dependency through the design interface to be used internally. The place where you inject is the *injection point*. |
| **Seam** | Pronounced "s-ee-m"; coined by Michael Feathers. *"A place where you can alter behavior in your program without editing in that place."* Examples: parameters, functions, module loaders, function rewriting, class interfaces, public virtual methods. |

**Why the taxonomy matters:** the conversation "should I use DI?" becomes answerable. The answer is *yes, if it removes a non-deterministic dependency*. The fix is *introduce a seam*. The verification is *you can now inject a stub*.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Table 3.2 Terminology used in this chapter" / "3.1 Types of dependencies"*

---

### Isolation Frameworks (Mocking Libraries) — Jest & substitute.js

**Principle:** An isolation framework dynamically creates and configures fakes. Two flavors: **loose** (Jest, Sinon — function/module friendly) and **typed** (substitute.js — class/interface friendly). Use them to remove boilerplate, but the same stub/mock rules still apply. Frameworks make overspecification dangerously easy.

**Do:**
- Use `jest.mock("./module")` at the top of the spec to fake a whole module.
- Use `jest.fn()` for single-function fakes; configure returns via `mockReturnValue` / `mockReturnValueOnce` / `mockImplementation`.
- Use `Substitute.for<T>()` for full OO interfaces (auto-handles methods you don't care about).
- Wrap fake creation in helper/factory functions to keep tests readable.
- Reset between tests: `afterEach(jest.resetAllMocks)`.
- Use Sinon sandbox when crossing framework boundaries (Jasmine, vanilla Node).

**Don't:**
- Don't use isolation frameworks as a license to add mocks everywhere — they make overspecification easy.
- Don't use `jest.mock()` to fake modules you control — abstract them behind your own adapter first.
- Don't use Jest manual mocks (`__mocks__/` folder) — high maintenance cost, low readability.
- Don't use `jest.spyOn()` without `mockImplementation` to *fake* — it's a *spy* (tracks calls), not a stub.

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
    stubConfigModule.getLogLevel.mockReturnValue("info");     // stub — feeds IN
    verifyPassword("anything", []);
    expect(mockLoggerModule.info)                              // mock — verify OUT
      .toHaveBeenCalledWith(stringMatching(/PASS/));
  });
});
```

**Code — `jest.fn()` for single functions:**
```javascript
test('given logger and passing scenario', () => {
  const mockLog = { info: jest.fn() };
  const verify = makeVerifier([], mockLog);
  verify('any input');
  expect(mockLog.info).toHaveBeenCalledWith(stringMatching(/PASS/));
});
```

**Code — stubbing return values / sequences / errors:**
```javascript
const stubFunc = jest.fn().mockReturnValue("abc");            // permanent
const stubSeq  = jest.fn()
  .mockReturnValueOnce("a")
  .mockReturnValueOnce("b")
  .mockReturnValueOnce("c");                                  // sequential
yourStub.mockImplementation(() => { throw new Error(); });    // simulate errors
```

**Code — typed fakes with substitute.js (auto-stub methods you don't configure):**
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

**Code — Stub + Mock together (OO substitute.js):**
```typescript
const stubMaintWindow = Substitute.for<MaintenanceWindow>();
stubMaintWindow.isUnderMaintenance().returns(true);   // stub: feeds data IN
const mockLog = Substitute.for<IComplicatedLogger>();  // mock: assert call OUT
const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
verifier.verify("anything");
mockLog.received().info("Under Maintenance", "verify");
```

**Code — Sinon.js sandbox for cross-framework JS:**
```javascript
const sinon = require('sinon');
const sandbox = sinon.createSandbox();
afterEach(() => sandbox.restore());
test('calls external API', () => {
  const mockHttp = sandbox.stub(http, 'get').returns({ status: 200 });
  doRequest('http://example.com');
  expect(mockHttp.calledOnce).toBe(true);
});
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 5.2 / 5.4 / 5.8 / 5.9 / 5.11" / "5.6 Advantages and traps of isolation frameworks" / "5.5 Stubbing behavior dynamically" / Appendix A.4.4 Sinon.js*

---

### Complicated Interfaces — Interface Segregation Principle (ISP)

**Principle:** Don't fake a 4-method `IComplicatedLogger` in 100 tests. Define a tiny role-specific interface (e.g. `ILogger { info(text) }`) that only exposes what the consumer needs, and fake that. Now tests survive third-party API churn.

**Do:**
- Define interfaces that *you own* and that are *adapted to your unit of work's needs* (ISP, Robert Martin).
- Pass the simple interface around; tests fakes get tiny; production can use any class that satisfies the contract.

**Don't:**
- Don't fake interfaces you don't control — wrap them in an internal adapter first.
- Don't fake long interfaces directly — they have more reasons to change, more boilerplate, and unused methods can shift in unrelated ways.

**Code — handwritten fake for long interface is boilerplate-heavy (BAD):**
```typescript
// BAD — long, third-party-shaped
export interface IComplicatedLogger {
  info(text: string, method: string);
  debug(text: string, method: string);
  warn(text: string, method: string);
  error(text: string, location: string, stacktrace: string);
}
// Each test in 100 tests has to write a fake that implements ALL four methods,
// even if it only cares about `info`. And any unrelated change to `error` breaks
// every test.
//
// ISP fix (GOOD) — only expose what PasswordVerifier uses:
export interface ILogger { info(text: string) }
//
// The handwritten fake becomes a one-liner:
class FakeLogger implements ILogger {
  written = '';
  info(text: string) { this.written = text; }
}
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "4.8 Dealing with complicated interfaces" / "4.8.4 The interface segregation principle" / "Listing 4.15 / 4.16 Boilerplate"*

---

### Partial Mocks (Extract and Override) — Legacy Only

**Principle:** A *partial mock* overrides one function on a real object while leaving the rest real. Useful for legacy code (existing classes you can't fully refactor yet); risky — keep it rare. The trade-off: you can override less but you inherit more.

**Code — OO via inheritance:**
```typescript
class TestableLogger extends RealLogger {
  logged = "";
  info(text) { this.logged = text; }    // override only info; error/debug stay real
}
test('verify with logger, calls logger', () => {
  const mockLog = new TestableLogger();
  const verifier = new PasswordVerifier([], mockLog);
  verifier.verify('any input');
  expect(mockLog.logged).toMatch(/PASSED/);
});
```

**Code — functional: override one method on a real instance:**
```typescript
const testableLog = new RealLogger();   // real first
testableLog.info = (text) => (logged = text);  // override ONE method
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "4.9 Partial mocks" / "Listing 4.17 / 4.18"*

---

### Spies — Wrapping Real Code with Tracking (Jest)

**Principle:** A **spy** wraps the real implementation of a function with a tracking layer so inputs/outputs can be verified. **`jest.spyOn(obj, 'fn')` alone only *tracks*; combine with `.mockImplementation(...)` to also *fake* (so it becomes a *stub* or *mock*).**

**Do:**
- Use `jest.spyOn(Date, 'now').mockImplementation(() => stubTime)` to fake `Date.now`.
- Restore with `jest.restoreAllMocks()` in `afterEach`.
- Use spies for verification of *real* behavior — did it call the real `console.warn` with the expected format?

**Don't:**
- Don't rely on spies alone to alter behavior — `spyOn` only tracks by default. Combine with `mockImplementation` to fake.
- Don't forget restoration — global state leaks across tests and across parallel workers.

**Code:**
```javascript
describe('v4 findRecentlyRebooted with jest spyOn', () => {
  afterEach(() => jest.restoreAllMocks());
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    Date.now = jest.spyOn(Date, 'now')
      .mockImplementation(() => fromDate.getTime());
    const rebootTwoDaysEarly = new Date(2000,0,1);
    const machines = [
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }
    ];
    const result = findRecentlyRebooted(machines, 1, fromDate);
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
    // afterEach → jest.restoreAllMocks() restores Date.now
  });
});
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Appendix A.2.2 Jest spies" / "Listing A.3 spyOn + mockImplementation" / "xUnit Test Patterns* spy definition"*

---

### Testing Asynchronous Code — Two Refactoring Patterns (Extract Entry Point / Extract Adapter)

**Principle:** Async forces explicit waiting. Two refactoring patterns make async unit-testable: **Extract Entry Point** (split pure logic out of the async orchestration) and **Extract Adapter** (wrap the async dependency behind a synchronous-looking seam). Decide by *which side has the heavy lift*.

**Do:**
- Keep one or two integration tests against the original async entry point for confidence.
- Test every scenario as a synchronous unit test against the *extracted* pure logic.
- Use `async/await` in tests (cleaner than `done()`/`.then()`).
- Fake timers with `jest.useFakeTimers()` + `jest.advanceTimersToNextTimer()`; reset with `jest.clearAllTimers`.
- For UI events, verify the *state change in the DOM* rather than asserting on the event subscription itself.

**Don't:**
- Don't pepper all scenarios as integration tests — they're slow and flaky.
- Don't assert on event subscriptions alone — verify an observable state change.
- Don't forget that even fake timers reset state — `afterEach(jest.clearAllTimers)` before the next test uses real timers again.

**Pattern A — Extract Entry Point (callback version):**
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

**Pattern A — async/await version (cleaner; return values beat callbacks):**
```javascript
const processFetchContent = (text) => {
  const included = text.includes("illustrative");
  if (included) return { success: true, status: "ok" };
  return { success: false, status: "missing text" };
};
// test: no async, no await, no done()
test('on fetch success with good content, returns true', () => {
  const result = samples.processFetchContent("illustrative");
  expect(result.success).toBe(true);
  expect(result.status).toBe("ok");
});
```

**Pattern B — Extract Adapter (modular) — wrapped behind a file you own:**
```javascript
// network-adapter.js — the only file that imports node-fetch
const fetch = require("node-fetch");
const fetchUrlText = async (url) => {
  const resp = await fetch(url);
  if (resp.ok) return { ok: true, text: await resp.text() };
  return { ok: false, text: resp.statusText };
};
// module.exports.fetchUrlText = fetchUrlText;
//
// test fakes the adapter module
jest.mock("./network-adapter");
const stubSyncNetwork = require("./network-adapter");
beforeEach(jest.resetAllMocks);
test('with good content, returns true', async () => {
  stubSyncNetwork.fetchUrlText.mockReturnValue({ ok: true, text: "illustrative" });
  const result = await webverifier.isWebsiteAlive();
  expect(result.success).toBe(true);
});
```

**Code — fake timers (Jest) — `jest.advanceTimersToNextTimer` runs the next scheduled callback:**
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

**Code — `setInterval` fake timers (advance twice, expect two results):**
```javascript
describe("calculate with intervals", () => {
  beforeEach(jest.clearAllTimers);
  beforeEach(jest.useFakeTimers);
  test("calculate, incr input/output, calculates correctly", () => {
    let xInput = 1;
    let yInput = 2;
    const inputFn = () => ({ x: xInput++, y: yInput++ });
    const results = [];
    Samples.calculate4(inputFn, (result) => results.push(result));
    jest.advanceTimersToNextTimer();        // first tick
    jest.advanceTimersToNextTimer();        // second tick
    expect(results[0]).toBe(3);
    expect(results[1]).toBe(5);
  });
});
```

**Code — DOM events (jsdom + DOM Testing Library — query by user-visible text):**
```javascript
const { fireEvent, findByText, getByText } = require("@testing-library/dom");
test("dom test lib button click triggers change in page", () => {
  const { window, docElem, button } = loadHtmlAndGetUIElements();
  fireEvent.load(window);
  fireEvent.click(button);
  // wait until true or timeout in 1s
  expect(findByText(docElem, "clicked", { exact: false })).toBeTruthy();
});
```

**Code — vanilla event-emitter test (use `done()` so missing emit fails the test):**
```javascript
describe("events based module", () => {
  describe("add", () => {
    it("generates addition event when called", (done) => {
      const adder = new Adder();
      adder.on("added", (result) => {
        expect(result).toBe(3);
        done();
      });
      adder.add(1, 2);
    });
  });
});
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 6.5 / 6.7 / 6.8 / 6.10 / 6.11 / 6.19 / 6.21 / 6.27" / "6.2.1 Extract Entry Point" / "6.2.2 Extract Adapter" / "6.3 Timers" / "6.4 Events" / "6.5 DOM Testing Library"*

---

### Trustworthy Tests — Avoid Logic in Tests (Including Test Reproducibility)

**Principle:** Any logic (`if`/`else`/`switch`/`for`/`while`/`try`/`catch`/string concatenation) inside a test is a likely bug in the test. The most dangerous form is *dynamically recomputing the expected value by repeating the production algorithm* — if the algorithm is wrong, the test enshrines the same bug.

**Do:**
- Hardcode expected values whenever inputs are simple enough.
- When trust clashes with maintainability, **trust wins** — a maintainable test you can't trust is worthless.
- Separate multi-input scenarios into separate tests with hardcoded expected outputs.
- After fixing a buggy test, introduce an obvious bug in production code to verify the test fails.

**Don't:**
- Don't write `expect(result).toBe("hello" + name)` — repeats production logic.
- Don't loop over inputs with `if`/`else` to pick the expected result.
- Don't write `try { ... } catch { fail() }` — use `expect(...).toThrowError(/regex/)`.

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
// Split into two tests with hardcoded outputs:
it("multi-word name is detected as name", () => expect(trust.isName("first second")).toBe(true));
it("single-word name is detected as name", () => expect(trust.isName("firstOnly")).toBe(true));
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 7.1 / 7.2 / 7.3 / 7.5" / "7.3 Avoiding logic in unit tests" / "Listing 7.3 Logic in asserts"*

---

### Trustworthy Tests — Red Flags in Passing Tests

**Principle:** A passing test isn't automatically trustworthy. Five red flags:

1. **No asserts** — the test runs code but verifies nothing. Add an assert or remove the test; if it's a "does not throw" check, name it so and use `expect(() => fn()).not.toThrow()`.
2. **You can't understand the test** — bad names, hidden logic, magic values.
3. **Unit and flaky integration tests mixed** — devs learn to dismiss all failures. Separate them; keep a "safe green zone" of fast, non-flaky tests.
4. **Testing multiple exit points in one test** — name becomes generic; first failing assert hides the rest. Split.
5. **Tests that keep changing** — current time, RNG, machine name → each run is a different test. Stub them out.

**Splitting rule:** *If the first assert fails, do you still care about the next one?* If yes → split into two tests. Multiple asserts on the *same concern* (e.g. `name` and `age` of one returned object) are fine.

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

### Trustworthy Tests — Why Tests Fail & Recovery Loop

**Principle:** Match the failure to the cause, fix the cause, then re-verify by intentionally breaking production.

**Why-tests-fail matrix:**

| Reason | What to do |
|--------|-----------|
| Real bug in production code | Celebrate — that's the job. |
| Buggy test gives false failure | Fix test, then *intentionally break production* to confirm test catches it. |
| Test out of date (functionality changed) | Adapt or delete; consult product owner if unsure. |
| Test conflicts with another test | Remove the irrelevant one (ask the product owner which behavior is correct). |
| Test is flaky | Quarantine; then **fix, convert, or kill** (see Flakiness). |

**Buggy-test recovery loop (verbatim from book):**
1. Reproduce the failure.
2. Debug the *test* (not the production code) first.
3. Fix the test.
4. Intentionally break the production code path it covers.
5. Confirm the test now fails.
6. Restore production code; confirm test passes.
7. Repeat if it still misbehaves.

**Sub-rule — "the test is no longer relevant or conflicts with another test":** In a changing world, sometimes a test's requirements changed. Talk to the product owner; do *not* delete unilaterally. If two tests demand the same input/output, one is wrong — find which one reflects current intent.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "7.2 Why tests fail" / "7.2.1 A real bug has been uncovered" / "7.2.3 The test is out of date" / "7.3 / 7.4"*

---

### Flaky Tests — Fix / Convert / Kill

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

**Don't:**
- Don't tolerate a "kind of flaky" test in the delivery pipeline — even one rollback the team ignores costs trust across the whole suite.
- Don't pay the cognitive cost of differentiating flaky runs from real failures.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "7.5 Dealing with flaky tests" / "7.5.1 What can you do once you've found a flaky test?" / "7.5.2 Preventing flakiness in higher-level tests"*

---

### Maintainability — Factory Methods Decouple Object Creation

**Principle:** When production code's constructor or signature changes, every test that directly calls `new PasswordVerifier(...)` breaks. Centralize creation in **factory functions** so a signature change touches one place. Factory methods make each test read top-to-bottom with no scroll fatigue.

**Do:**
- One factory per object under test; one per fake (e.g. `makeFakeLogger()`).
- Default parameters let most tests call `makePasswordVerifier([])` with no logger arg.
- Combine with helper functions for repeated actions (`addDefaultUser()`).
- Replace `beforeEach()` with factory methods called *from inside each test* to eliminate scroll fatigue.

**Don't:**
- Don't push `Arrange` + `Act` into `beforeEach` — readers can't see what the test depends on.
- Don't re-create the SUT inline in each test — go through a factory.

**Code — refactor tests to factory functions:**
```javascript
describe("password verifier 1", () => {
  const makeFakeLogger = () => ({ info: jest.fn() });
  const makePasswordVerifier = (
    rules,
    fakeLogger = makeFakeLogger()
  ) => new PasswordVerifier(rules, fakeLogger);

  it("passes with zero rules", () => {
    const verifier = makePasswordVerifier([]);
    const result = verifier.verify("any input");
    expect(result).toBe(true);
  });
});
```

**Code — full factory-method refactor (no `beforeEach`):**
```javascript
const makeVerifier = () => new PasswordVerifier1();
const passingRule = (input) => ({passed: true, reason: ''});
const makeVerifierWithFailedRule = (reason) => {
  const verifier = makeVerifier();
  verifier.addRule((input) => ({passed: false, reason}));
  return verifier;
};
const makeVerifierWithPassingRule = () => {
  const verifier = makeVerifier();
  verifier.addRule(passingRule);
  return verifier;
};
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      const errors = verifier.verify('any input');
      expect(errors[0]).toContain('fake reason');
    });
  });
});
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 8.4 Refactoring to factory functions" / "2.7 / 2.7.1 Replacing beforeEach() completely with factory methods" / "Listing 2.16 / 2.17 / 2.18"*

---

### Maintainability — Test Isolation (No Constrained Test Order)

**Principle:** Tests must not depend on each other. Test runners don't guarantee order. Shared mutable state (singletons, caches, DB rows) is the root cause of "passes locally, fails in CI" mysteries.

**Do:**
- Reset shared resources in `beforeEach`/`afterEach` (e.g. `getUserCache().reset()`).
- Extract setup actions into reusable helper functions called from inside each test.
- Run a single test in isolation (`test.only`) to verify it doesn't rely on siblings.

**Don't:**
- Don't let one test populate a cache that a later test relies on.
- Don't share mutable variables across `it()` blocks.
- Don't forget that Jest runs tests in parallel by default — moving shared state to the top of the file can cause race conditions across workers.

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
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Listing 8.9 Refactoring tests to remove order dependence" / "2.6.1 beforeEach() and scroll fatigue" / "8.1.1 The test is not relevant or conflicts with another test"*

---

### Maintainability — Avoid Testing Private/Protected Methods

**Principle:** Private methods are implementation details; testing them couples tests to internal changes (refactor → tests fail even though behavior is unchanged). Treat `private` as a signal that the design is right but the contract is hidden.

**Do — when a private method seems worth testing, choose one:**
- Test it through the public method that exercises it.
- Make it public (its contract is meaningful).
- Make a stateless private method public + static (utility contract).
- Extract it into a new class/module with its own public API.

**Don't:**
- Don't reach into private state via reflection/bracket access (`pv4["findFailedRules"]`) — that's overspecification.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "8.2.1 Avoid testing private or protected methods" / "Making stateless private methods public and static"*

---

### Maintainability — Keep Tests DRY, Avoid `beforeEach` Bloat

**Principle:** DRY applies to tests — but readability trumps DRY when trade-offs collide. `beforeEach` becomes a "garbage bin" of unrelated setup; it can't take parameters or return values, and hides mocks/stubs from readers.

**Do:**
- Prefer **factory/helper methods** called from inside each test.
- For shared resource *reset only*, a minimal `beforeEach(() => resource.reset())` is acceptable.
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
    verifier.verify("anything");
    mockLog.received().info(Arg.is((x) => x.includes("PASSED")), "verify");
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
- Use the format string (`%s`, `%i`, `%d`) so each row has a readable name in the report.
- Use vanilla `for ... of` if `test.each` feels awkward (it works with any runner).

**Don't:**
- Don't lump different scenarios into one table to "save lines" — readability plummets.
- Don't parameterize across different output *behaviors* — only across input variations.

**Code — single parameter table:**
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
**Code — multi-arg table (failing + passing scenarios as separate tables):**
```javascript
test.each([ ['Abc', true], ['aBc', true] ])
  ('given %s, %s ', (input, expected) => {
    const result = oneUpperCaseRule(input);
    expect(result.passed).toEqual(expected);
  });
test.each([ ['abc', false] ])
  ('given %s, %s ', (input, expected) => {
    const result = oneUpperCaseRule(input);
    expect(result.passed).toEqual(expected);
  });
```
**Code — vanilla JS parameterization (works in any runner):**
```javascript
describe('one uppercase rule, with vanilla JS for', () => {
  const tests = { 'Abc': true, 'aBc': true, 'abc': false };
  for (const [input, expected] of Object.entries(tests)) {
    test(`given ${input}, ${expected}`, () => {
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(expected);
    });
  }
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.9 Refactoring to parameterized tests" / "Listing 2.20 / 2.21 / 2.22 / 2.23 / 8.10"*

---

### Test Organization — Checking Thrown Errors (Declarative Form)

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

**Use `expect.assertions(N)` to catch "test passes when no assertion ran" cases** (e.g. when an async callback never fires). Jest has dropped the `fail()` function in favor of this.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.10 Checking for expected thrown errors" / "Listing 2.25 / 2.26" / "Using fail()" sidebar*

---

### Test Organization — Jest Snapshots (Use Sparingly)

**Principle:** `toMatchSnapshot()` saves a JSON rendering and diffs against it next time. Useful for *rendered HTML* or *serialized blobs* that you don't want to assert by hand. **Easy to abuse** — every irrelevant re-render breaks the test, the diff is opaque, the snapshot itself becomes a hidden source of expected values.

**Do:**
- Use `toMatchInlineSnapshot()` so the snapshot lives inline with the test (readable, PR-reviewable).
- Use snapshots for render output where every property is meaningful, not for "I don't know what to test" excuses.

**Don't:**
- Don't use snapshots in place of USE-named tests with explicit expects.
- Don't allow snapshot tests to grow a long history of `--update-snapshot` re-baselines that nobody reads.

```javascript
// ABUSE — many things asserted, none readable
it('renders', () => {
  expect(<MyComponent/>).toMatchSnapshot();
});
// BETTER — explicit assertions for things you care about
it('renders the title in an h1', () => {
  render(<MyComponent title="hello" />);
  expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('hello');
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.10 sidebar Jest snapshots"*

---

### Test Organization — Setting Test Categories

**Principle:** Group tests by purpose (unit/integration/contract) to enable fast selective runs. Jest doesn't have built-in categories but supports them via config files or path patterns.

**Do:**
- Use `--testPathPattern` on the CLI to filter without code changes.
- Or split `jest.config.unit.js` and `jest.config.integration.js` each with a separate `testRegex`.
- Wire each to its own npm script.

```javascript
// jest.config.integration.js
var config = require('./jest.config')
config.testRegex = "integration\\.js$"
module.exports = config
// jest.config.unit.js
var config = require('./jest.config')
config.testRegex = "unit\\.js$"
module.exports = config
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.11 Setting test categories" / "Listing 2.27"*

---

### Test Readability — Magic Values & Sentinel Strings

**Principle:** Unexplained literals (`0`, `[]`, `'jhGGu78!'`) force readers to guess. Wrap them in named constants, or use sentinel strings (`"anything"`, `"any input"`) that signal "this value does not matter." Variable names communicate *what does not matter* in equal weight to what matters.

**Code — magic values (BAD):**
```javascript
test('on weekends, throws exceptions', () => {
  expect(() => verifyPassword2("jhGGu78!", [], 0)).toThrowError("It's the weekend!");
});
```
**Code — fixed (GOOD):**
```javascript
const SUNDAY = 0, NO_RULES = [];
test("on weekends, throws exceptions", () => {
  expect(() => verifyPassword2("anything", NO_RULES, SUNDAY))
    .toThrowError("It's the weekend!");
});
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "9.2 Magic values and naming variables" / "Listing 9.3 / 9.4"*

---

### Test Smells — Overspecification (Four Forms)

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
**Code — substring vs exact string (BAD vs GOOD):**
```javascript
// BAD: any punctuation change breaks it
expect(msg).toBe("you have 2 failed rules.");
// GOOD: only the meaningful part is asserted
expect(msg).toMatch(/2 failed/);
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "8.3 Avoid overspecification" / "Listing 8.11–8.18"*

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

**When E2E-only happens:**
- **Separation of duties** (separate QA & dev pipelines) — QA writes only the kinds of tests they're used to (often E2E), independent of dev priorities.
- **"If it works, don't change it"** — early wins are sticky; refactoring later is harder as the suite grows.
- **Sunk-costs fallacy** — "we can't delete them, we spent years on them."

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.1 Common test types and levels" / "10.2 Test-level antipatterns" (Tables 10.2–10.6) / "10.2.1 The end-to-end-only antipattern" / "10.2.2 The low-level-only test antipattern" / "10.2.3 Disconnected low-level and high-level tests"*

---

### Test Strategy — Test Recipes & Frequencies

**Principle:** A **test recipe** is an informal 5–20-line plan, stored in the feature story, listing each scenario and the level at which it'll be tested. It is the team's "definition of done." Living document, not a binding contract.

**Rules:**
- **Pair:** at least two people (dev + tester perspective) — never write alone.
- **Just in time:** create it right before coding the feature.
- **Faster wins:** prefer lower levels unless a high-level test is the only way to gain confidence.
- **Confidence check:** "If all these tests pass, will I feel good about this feature?" If not, add scenarios.
- **Revise freely:** recipes are living documents.
- **Don't repeat:** across features or across layers (variations go to lower levels).
- **Ratio target:** ~1 high-level test : 5+ lower-level tests.
- **Pragmatic:** not every story needs every level — unit-only is fine for a pure utility.

**Example — User profile feature:**
```
User profile feature testing recipe
E2E  - Login, go to profile screen, update email, log out, log in with new email,
       verify profile screen updated
API  - Call UpdateProfile API with more complicated data
Unit - Check profile update logic with bad email
Unit - Profile update logic with same email
Unit - Profile serialization/deserialization
```
*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.3 Test recipes as a strategy" / "10.3.1 / 10.3.2 / 10.3.3"*

---

### CI / Delivery Pipeline Strategy — Delivery vs. Discovery

**Principle:** Split pipelines into **delivery** (blocking, fast, deploy-on-green) and **discovery** (non-blocking, slow, KPI-finding). Parallelize aggressively. Run on every commit — never nightly.

**Do:**
- **Delivery pipeline** = delivery-blocking tests (unit, integration, E2E, security). Fast feedback; auto-deploys when green.
- **Discovery pipeline** = good-to-know tests (load, complexity scans, long-running nonfunctional). Runs in parallel; failures become backlog items, not blockers.
- Parallelize pipelines *and* stages *and* individual test suites (especially E2E).
- Use dynamic, ephemeral environments; throw money at parallelism, not at manual testers.

**Don't:**
- Don't do nightly builds — feedback must follow each commit.
- Don't gate delivery on good-to-know tests.
- Don't assume on-demand = sufficient. Continuously running beats scheduled; scheduling with crons is a fallback.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "10.4 Managing delivery pipelines" / "10.4.1 Delivery vs. discovery pipelines" / "10.4.2 Test layer parallelization" / "Don't do nightly builds"*

---

### Legacy Code — Test-Feasibility Table, Easy- vs. Hard-First

**Principle:** Build a **test-feasibility table**: rate each component on Logical Complexity (1–10), Dependency Level (1–10), and Priority (1–10). Ignore components below complexity ~3. Choose **easy-first** or **hard-first** based on team experience.

**Test-feasibility table example:**

| Component     | Logical complexity | Dependency level | Priority | Action |
|---------------|--------------------|-----------------|----------|--------|
| Utils         | 6                  | 1               | 5        | **Test** — easy + high value |
| Person        | 2                  | 1               | 1        | **Ignore** — too trivial |
| TextParser    | 8                  | 4               | 6        | **Test next** — hard + high value |
| ConfigManager | 1                  | 6               | 1        | **Ignore** — low ROI |

**Selection strategies:**
- **Easy-first** (fewer dependencies): quick wins, builds team confidence. *Downside:* hardest components remain when schedule pressure peaks. Good for inexperienced teams. As an experienced rule of thumb: "avoid all components over 4 dependencies at first."
- **Hard-first** (most dependencies): each refactoring unblocks testability for neighbors; time-per-test declines quickly. *Requires an experienced team.*

**Process for adding tests to legacy code:**
1. Write integration tests against the existing system to capture current behavior (characterization tests).
2. Add a failing test for the new feature/fix.
3. Refactor in small chunks; run integration tests after each.
4. Over time, replace integration tests with focused unit tests as the code becomes testable.

**Anchors / references:**
- **Michael Feathers**, *Working Effectively with Legacy Code* — "Seams" + the classic refactoring recipes.
- **CodeScene** — commercial tool for technical-debt visualization in legacy code.
- **Vladimir Khorikov**, *Unit Testing Principles, Practices, and Patterns* (2020), chapter 7 — full refactoring example.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "12.1 Where do you start?" / "12.2 Choosing a selection strategy" / "12.3 Writing integration tests before refactoring" / "12.3.1 Read Feathers" / "12.3.2 CodeScene" / "Table 12.1 Simple test-feasibility table" / "Figure 12.2–12.4 Strategy plots"*

---

### Monkey-Patching Functions & Modules (CFRA Pattern) — Last Resort

**Principle:** Monkey-patching globals (`Date.now`, `setTimeout`, entire modules) is fragile and hurts parallelism. **Use it only when you cannot refactor to add seams.** Frameworks give you tooling (Jest fake timers, `jest.spyOn().mockImplementation`, Sinon sandbox) that reduce boilerplate — but the underlying problems remain.

**Do (if forced):**
- Save the original, replace, **and** restore in `afterEach` — never inline, because a thrown assert will skip restoration.
- Prefer framework support: `jest.spyOn(obj, 'fn').mockImplementation(...)` + `jest.restoreAllMocks()` in `afterEach`.
- For per-test module faking use the **CFRA pattern**: **C**lear (`jest.resetAllMocks` / `jest.resetModules`) → **F**ake (`jest.mock` + `mockImplementation`) → **R**equire (re-`require` the SUT after faking) → **A**ct.
- Use `jest.runInBand` (single-threaded) only when all parallelism routes are exhausted.

**Don't:**
- Don't use Jest manual mocks (`__mocks__/` folder) — high maintenance, low readability.
- Don't fake modules you control — wrap them in an adapter first.
- Don't forget that parallel tests can collide on global state — restore, restore, restore.

**Code — vanilla Date.now monkey-patch (BAD; fails to restore on assert failure):**
```javascript
test('v1 findRecentlyRebooted', () => {
  const originalNow = Date.now;
  const fromDate = new Date(2000,0,3);
  Date.now = () => fromDate.getTime();
  const rebootTwoDaysEarly = new Date(2000,0,1);
  const machines = [
    { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
    { lastBootTime: fromDate, name: 'found' }
  ];
  const result = findRecentlyRebooted(machines, 1, fromDate);
  expect(result.length).toBe(1);     // ← if this throws, restoration is skipped
  expect(result[0].name).toContain('found');
  Date.now = originalNow;
});
```
**Code — proper beforeEach/afterEach (BETTER):**
```javascript
describe('v2 findRecentlyRebooted', () => {
  let originalNow;
  beforeEach(() => originalNow = Date.now);
  afterEach(() => Date.now = originalNow);
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    Date.now = () => fromDate.getTime();
    const rebootTwoDaysEarly = new Date(2000,0,1);
    const machines = [
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }
    ];
    const result = findRecentlyRebooted(machines, 1, fromDate);
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
  });
});
```
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

**Code — Sinon.js (vanilla require) CFRA:**
```javascript
const sinon = require('sinon');
let dataModule;
const fakeDataFromModule = fakeData =>
  sinon.stub(dataModule, 'getAllMachines').returns(fakeData);
const resetAndRequireModules = () => {
  jest.resetModules();
  dataModule = require('../my-data-module');
};
const requireAndCall_findRecentlyRebooted = (maxDays, someDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, someDate);
};
```

**Code — testdouble.js with testdouble-jest bridge:**
```javascript
let td;
const resetAndRequireModules = () => {
  jest.resetModules();
  td = require('testdouble');
  require('testdouble-jest')(td, jest);
};
const fakeDataFromModule = fakeData =>
  td.replace('../my-data-module', {
    getAllMachines: () => fakeData
  });
```

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — Appendix A "Monkey-patching functions and modules" / Listings A.1–A.8 / "A.3 Ignoring a whole module with Jest" / "A.4 Faking module behavior in each test" / "A.4.4 Stubbing a module with Sinon.js" / "A.4.5 Stubbing a module with testdouble" / "CFRA pattern"*

---

### Types of Dependencies (Incoming vs. Outgoing) — Why Mocks vs. Stubs Differ

**Principle:** The *direction* of dependency determines the testing technique:
- **Incoming dependencies** are created by the SUT or passed IN to it (parameters, fields, constructor args). They're the inputs the SUT can't control → break with **stubs**.
- **Outgoing dependencies** are created by the SUT and used OUT (logger, third-party API calls, network sockets). They're the things the SUT *talks to* → verify with **mocks**.

**Why this matters:** Confusing the two is the most common cause of bad tests. If you assert against a stub, you test implementation. If you mock an incoming value, you can't tell *what* the SUT did with it. The direction of the arrow dictates the technique.

| Dependency type | Direction | Test double | Assert? | How many per test? |
|-----------------|-----------|-------------|---------|--------------------|
| Incoming (SUT receives) | IN | Stub | No | Many allowed |
| Outgoing (SUT calls OUT) | OUT | Mock | Yes | At most 1 |

**Examples:**
- A password verifier receives a list of rules (incoming) and calls a logger (outgoing). Tests use **stubs** for rules and **mocks** for the logger.
- A web handler reads from the request (incoming) and writes to a database (outgoing). Tests use a **fake/stub** request and **mock** the DB layer.
- A widget receives a date provider (incoming) and pushes events to a telemetry service (outgoing). Tests use a **fake time provider** and **mock** telemetry.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "3.1 Types of dependencies" / Table 3.1 / "4.4 The importance of differentiating between mocks and stubs"*

---

### Handwritten Fakes vs. Isolation Frameworks — Decision Tree

**Principle:** Frameworks (Jest, Sinon, substitute.js) remove boilerplate; handwritten fakes keep tests lean and dependencies explicit. Default to **handwritten** when the fake is small and reused; **frameworks** when writing fakes by hand becomes onerous (many methods, frequent change).

**Use handwritten fakes when:**
- The double has 1–2 methods.
- The fake will be reused across many tests.
- You want compile-time checks (TypeScript/Java/C#).
- You want the reader to *see* the implementation in the test file.

**Use isolation frameworks when:**
- The double has many methods (boilerplate becomes the dominant test cost).
- The double changes often (third-party library with frequent upgrades).
- You want shorthand: `jest.mock()` for whole modules, `Substitute.for<T>()` for full interfaces.

**Hybrid pattern:** handwritten `FakeLogger` for the long-lived test suite; `jest.fn()` for one-off mocks in a single test.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "4.5 Modular-style mocks" / Chapter 5 "Isolation frameworks"*

---

### Maintainability — Refactoring to New Classes / Extracting Public API

**Principle:** When a private method is hard to test through the public method (because it's used by *another* consumer, not by the SUT), don't make it public + cluttered — **extract it into its own class/module with a clean public API**. This is the *Extract Class* refactor applied to testability.

**Do:**
- When a private method has multiple call sites, suspect it's a class in disguise.
- Extract `MyClass._helper` to `HelperService` and inject both into `MyClass`.
- Test `HelperService` directly with focused tests; test `MyClass` with the now-trivially-callable public surface.

**Don't:**
- Don't promote a stateless private method to `public static` as a shortcut — extract a class with its own contract.
- Don't test a private method through reflection — extract instead.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "8.2.1 / 8.2.2 Avoid testing private or protected methods" / "Making stateless private methods public and static"*

---

### Readability — AAA Visibility, Assertion Purity, and the Debug Loop

**Principle:** Tests are read more often than they are written. Visibility into AAA + hardcoded expected values + named variables = debuggable in seconds.

**Code — every principle applied:**
```javascript
const SUNDAY = 0, NO_RULES = [];
test('verifyPassword, with a failing rule on Sunday, throws "It\'s the weekend!"', () => {
  // Arrange — AAA visible
  const failingRule = (input) => ({ passed: false, reason: 'no upper case' });
  // Act — one line
  expect(() => verifyPassword('anything', [failingRule], SUNDAY))
    // Assert — exact match the user-visible error
    .toThrowError(/It's the weekend!/);
});
```
*Why this passes the readability audit:*
- Name includes USE (Unit / Scenario / Expected).
- AAA sections visible (separated visually).
- Magic values extracted to named constants.
- Assertion is regex-based (forgive cosmetic error-string changes).
- One exit point tested per test.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "9.1 / 9.2 / 9.3 / 9.4" / "9.5 Summary"*

---

### Implementing Unit Testing in an Organization — Champions, Blockers, Experiments, Metrics

**Principle:** Changing engineering culture is more psychological than technical. Identify *champions* and *blockers* early; give both a role in the change. Use guerrilla (bottom-up) or top-down approaches, or run a *time-boxed experiment* on a small team. **Accept that the change costs you personally; bring an outside champion if you can't afford it.**

**Steps to becoming an agent of change:**
1. **Accept the role** — hiding makes things worse.
2. **Be prepared for the tough questions** (see below).
3. **Identify champions and blockers**; *make both groups part of the process*.
4. **Identify starting points**: smaller teams, subteams, feasible projects, code-and-test reviews as teaching tools.
5. **Persist for 3 months minimum**; absorb failures.

**Ways to succeed:**
- **Guerrilla** (bottom-up) — show results, then convince others. May be covert initially; don't lie about it.
- **Top-down** — a manager reads a book, gives a presentation, or uses authority to initiate.
- **Experiments as door openers** — declare a 2–3 month, one-team, one-or-two-component experiment; "which idea do we want to experiment with first?" concedes politics without sacrificing the work.
- **Get an outside champion** — freedom to speak, experience, dedicated time.
- **Make progress visible** — whiteboards, big-screen dashboards, contact details.
- **Specific goals, metrics & KPIs** — see below.

**Ways to fail:**
- Lack of a driving force.
- Lack of political (or covert) support — "Add 10% to your time for this" is a choke-out.
- Ad hoc implementation and first impressions that destroy credibility.
- Lack of team support.

**Metrics — lagging indicators (the four DORA metrics):**
- **Deployment frequency** — how often releases go to production.
- **Lead time for changes** — request → production (not commit → production; that's cycle time).
- **Escaped bugs / change failure rate** — failures per release / percentage of bad releases.
- **Time to restore service** — mean-time-to-recovery from incidents.

**Leading indicators:** code coverage, # of tests, build-run-time. Easier to fake; combine with lagging indicators for truth. Track *trends*, not snapshots. Numbers without context are neither good nor bad.

**Qualitative surveys (1–5 scale, ask in retrospectives):** "How confident are you that tests will find bugs?", "Does the code do what it's supposed to?"

**Indicator categories:** team-level vs. engineering-management-level; progress, bottlenecks & feedback, quality, skills, learning.

**Six influence factors (Patterson et al., *Influencer*):** personal ability, personal motivation, social ability, social motivation, structural (environmental) ability, structural motivation. Change must address *all* factors in play; fixing one fails. (Example: budget for a build machine *plus* deter managers from giving bonuses for "shipped early and crappy" — fixing only one still loses.)

**Tough questions and answers:**
- *How much time will this add?* — Per-feature coding doubles; integration shrinks; bug-fixing shrinks; *overall* release time stays similar or less (see Tale of Two Features table: 26 → 23 days, 71 → 11 escaped bugs). Emphasize integrated measurement.
- *Will my QA job be at risk?* — No. QA becomes more interesting (logical bugs, user acceptance) instead of button-click debugging; two layers of defense.
- *Is there proof it works?* — Anecdotal + empirical; see TDD studies (`http://mng.bz/dddo`).
- *Why is QA still finding bugs?* — Expected; unit + integration + E2E together.
- *Where do we start with code without tests?* — 80/20: 20% of the code holds 80% of bugs (Endres 1975; Gremillion 1984; Boehm 1987; Shull 2002). Start where the team already knows the pain lives.
- *What about hardware-software combos?* — Use test layers; harness simulators/emulators.
- *How can we know we don't have bugs in tests?* — Watch them fail. TDD forces this.
- *Why do I need tests if my debugger shows it works?* — Code spends most of its life in maintenance; tests prevent regression by others; multi-threaded code can't be debug-stepped; Curtis/Krasner/Iscoe showed most defects come from miscommunication, not code.
- *What about TDD?* — Style choice; pick your poison.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Chapter 11 Integrating unit testing into the organization" / "11.1–11.5" / "Lies, Damned Lies, and Metrics" / `https://pipelinedriven.org` / "Table 11.2 Team progress with/without tests"*

---

### Quick Reference — Mock Library Cheatsheet

| Library | API surface | Best for | Risk |
|---------|-------------|----------|------|
| **Jest** `jest.fn()` | `jest.fn().mockReturnValue(x)`, `.mockReturnValueOnce(x)`, `.mockImplementation(fn)`, `.toHaveBeenCalledWith(...)` | Functions, modules, simple objects | Overuse of "mock" naming — every Jest fake looks mock-shaped |
| **Jest** `jest.mock("./mod")` | Auto-fakes every export of a module; combine with `mockImplementation` | Whole-module replacement | Couples to module's export shape; manual mocks (`__mocks__/`) hurt readability |
| **Jest** `jest.spyOn(obj,'fn')` | Wraps real fn; `.mockImplementation` needed to actually *fake* | Spying AND faking | Forgetting `mockImplementation` = spy that calls the real function |
| **Sinon.js** `sinon.stub(obj, 'fn')` | Spies/fakes object methods directly, sandbox pattern | Cross-framework compatibility | Verbose vs substitute.js |
| **substitute.js** `Substitute.for<T>()` | Auto-stub type interface; `.returns()`, `.received()`, `Arg.is(...)` | Strongly-typed languages & interfaces | Auto-stubbed unused methods can mask missing-test surface |
| **testdouble.js** (`td.replace`) | Pre-configured behavior verification; `td.verify(...)` | Strict behavior assertions | Steep naming/paradigm |

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — Chapter 5 (Jest) / Appendix A (Sinon, testdouble)*

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
- **Long/complicated interfaces in tests:** tons of boilerplate per fake. *Fix:* ISP — make a tiny per-consumer role interface.
- **Direct `require()` of third-party modules in code you control:** tests become brittle when those APIs change. *Fix:* Ports & Adapters / Hexagonal — wrap behind your own module.
- **Jest manual mocks in `__mocks__/` folder:** increases cross-file scrolling, hurts readability. *Fix:* inline mocks or factory helpers.
- **Sunk-cost fallacy on legacy tests:** "we can't delete them, we spent so much on them." *Fix:* adopt easy-first or hard-first strategy; replace integration tests with unit tests during refactoring.
- **Treating "passes build = ready":** without E2E coverage you still manually test. *Fix:* test recipes + ratio target 1 high : 5+ low.
- **Forgetting to `jest.restoreAllMocks()` / `afterEach` for spies:** global state leaks across tests and parallel workers. *Fix:* always restore in `afterEach`.
- **Snapshot abuse:** `toMatchSnapshot()` in place of explicit asserts. *Fix:* prefer `toMatchInlineSnapshot()` or hand-written asserts.
- **Skipping the "test the test" pass:** never intentionally breaking production after the test goes green means you don't know it actually fails. *Fix:* after every new green test, mutate production, watch it fail, revert.

---

## Decision Heuristics / Checklists

**Choosing a test level for a scenario (test-recipe checklist):**
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
- Placeholder argument that satisfies signature → **dummy**.

**Choosing an injection seam (lightest → heaviest):**
1. Parameter (value) — purest, easiest.
2. Function parameter.
3. Factory / curried higher-order function.
4. Constructor function (JS `new`).
5. Class constructor (OO).
6. Object parameter (duck typing).
7. Typed interface (TypeScript/Java/C#).
8. Module injection (`jest.mock`) — last resort, couples to third-party API.

**Choosing an async refactoring pattern:**
- Logic is bulky; async is thin (one `fetch`, one timer) → **Extract Entry Point**.
- Async dependency is bulky (network adapter, timer library) and used elsewhere → **Extract Adapter** + own internal module.
- Always keep 1–2 integration tests for the original async orchestrator.

**"Do I trust this test?" checklist:**
- It fails → am I worried? (yes = trust)
- It passes → am I relaxed? (yes = trust)
- If either is "no," inspect for: no asserts, unreadable code, mixed with flaky tests, multiple exit points, dynamic values.

**Buggy-test recovery loop:**
1. Reproduce the failure.
2. Debug the *test* (not the production code) first.
3. Fix the test.
4. Intentionally break the production code path it covers.
5. Confirm the test now fails.
6. Restore production code; confirm test passes.
7. Repeat if it still misbehaves.

**Legacy-code-start checklist:**
1. Build a test-feasibility table (Complexity / Dependencies / Priority).
2. Drop any component with complexity < 2–3.
3. Choose easy-first (inexperienced team, avoid components with >4 dependencies at first) or hard-first (experienced team — declining time-per-test).
4. Write characterization integration tests; capture behavior before refactoring.
5. After each refactoring chunk, run integration tests; once testable, swap in focused unit tests.

**CI pipeline gate:**
- Delivery pipeline: unit + integration + E2E + security. Gates release.
- Discovery pipeline: load, complexity, long-running nonfunctional. Never gates release.

**Change-agent checklist:**
- Identify champions and blockers before the first meeting.
- Pair-blame-proof the experiment (time-boxed, low-risk).
- Measure with DORA + leading indicators from day 1.
- Have answers ready for "how much extra time?" and "is my QA job safe?"

**Six influence factors checklist:**
1. Personal ability — skills/knowledge?
2. Personal motivation — satisfaction/self-control?
3. Social ability — help at critical times?
4. Social motivation — peers encouraging?
5. Structural ability — environment makes it easy?
6. Structural motivation — incentives aligned?
Fix all six, not just one.

---

### Code Reviews as Teaching Tools (for Test Adoption)

**Principle:** Code reviews that include *tests* are the cheapest way to spread good practices. Review every line of code in the first few weeks of a unit-testing initiative.

**Do:**
- Do reviews in person (not via remote tooling) — nonverbal cues matter.
- In the first 2 weeks, review every line. Don't trust "we didn't think this code needs reviewing."
- Add a third person to reviews — they learn to review, you don't become a bottleneck.
- Treat the review as teaching TDD, not gate-keeping — point at *what* you're looking for, not just *what's wrong*.

**Don't:**
- Don't review code-only — tests are the contract; review them with equal weight.
- Don't accept "I know what I'm doing" for new joiners — they don't know your team's testing conventions yet.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "11.1.3 Identify possible starting points" / "Use code and test reviews as teaching tools"*

---

### Detecting Suspiciously-High Coverage (the Coverage Trap)

**Principle:** Coverage is a *metric*, not a goal. 100% code coverage with logic-bearing tests is worse than 80% coverage with focused ones. Track *trend lines* over *snapshots*.

**Do:**
- Pair coverage with **mutation testing** (Stryker, PIT, mutmut) to detect trivial tests.
- Look at coverage deltas in PRs alongside time-to-fix and escaped-bug metrics.
- Use coverage as a *gate for new code* in delivery pipelines (no coverage = no merge).

**Don't:**
- Don't reward teams for "raising coverage to 90%" — they game it with no-op tests.
- Don't accept the canonical errors of 80%/20% bugs (Endres 1975; Gremillion 1984; Boehm 1987; Shull 2002) as a reason to skip testing 80% of *your* code — fix the painful 20% first.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "11.5.5 We have lots of code without tests: Where do we start?" / "11.2.6 Aim for specific goals, metrics, and KPIs"*

---

### Cyclomatic Complexity vs. Dependency Level — Picking Refactor Targets

**Principle:** Cyclomatic complexity = 1 + (number of decision points: if/case/loops/&&/||). High cyclomatic complexity compounds with high dependencies to make code untestable.

**Do:**
- Use tools that report cyclomatic complexity (lizard, ESLint rules, NDepend, etc.).
- Aim to refactor components where both axes are high first (intersection of complexity + dependencies).
- Track complexity over time as a leading indicator.

**Don't:**
- Don't conflate "complex code" with "many lines" — branching logic, not LoC, is the killer.
- Don't let a `switch` statement over an external enum hide behind a "simple function" rating.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "12.1 Where do you start?" / "Logical Complexity" / "Dependency Level" / Table 12.1*

---

### Working Effectively with Legacy Code — The Five "Seam" Patterns

**Principle:** Michael Feathers' classic seams map directly to the injection techniques in this book:
1. **Preprocessing seams** — `#ifdef` (rare in app code; common in embedded).
2. **Link seams** — replace at compile time (C/C++/Rust linkage).
3. **Object seams** — replace an object with a fake (ISP, constructor injection).
4. **Class seams** — override via inheritance (partial mocks; legacy).
5. **Parameter seams** — push the dependency through a parameter (preferred).

**Where each one fits in your stack:**
- App code (Python, JS, Go, Java, C#) → parameter / object / class seams dominate.
- Library code with explicit API contracts → interface seams (ISP).
- Code you cannot refactor → class seams (partial mock) or monkey-patching.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "12.3.1 Read Michael Feathers' book" / "3.1 Seams" / Table 3.2*

---

### Test Categories + Path Patterns — Run What You Need

**Principle:** No engineer waits 30 minutes for the full suite. Provide fast filtered runs.

**Do:**
- Wire test categories (unit/integration/contract) to npm scripts or Gradle tasks.
- Run only the changed package's tests locally (vitest `changed-since`, jest `--findRelatedTests`).
- Keep two separate `jest.config.js` files and one wrapper that dispatches by env var.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "2.11 Setting test categories"*

---

### Comparing Real Outages to Escaped Bugs — Feedback from Production

**Principle:** Tests are predictive; production is ground truth. Close the loop by feeding real failures into the test suite.

**Do:**
- Triage each production bug as a *test gap*. Ask: which test could have caught it?
- Add an integration or unit test that reproduces the bug, *then* fix.
- Track escaped bugs per release (a leading DORA-adjacent metric).

**Don't:**
- Don't accept "we'd never have a test for that scenario" without first exploring whether a unit test could express it.
- Don't file post-mortems without action items in the test suite.

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "11.2.6 metrics" / "11.4 Influence factors"*

---

### Wrap-Up: The Three Pillars, Reiterated

A test that fails the *trustworthy* test is noise. A test that fails the *maintainable* test is friction. A test that fails the *readable* test is replaced by silence. **Aim for all three, drop none.**

*Ref: The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md — "Chapter 7 introductory section / Chapter 8 summary" / "Three pillars — together"*

---

## Key Takeaways

1. **A unit test invokes a unit of work through an entry point and checks one exit point.** Exit points come in three types (return value, state change, third-party call) — each needs a different technique.
2. **Stubs feed data IN; mocks verify calls OUT.** Never assert against a stub. At most one mock per test. Aim for mocks in ≤5% of tests.
3. **AAA + USE naming** are the universal test skeleton: Arrange-Act-Assert visible phases; Unit + Scenario + Expected behavior in the name.
4. **Avoid logic in tests** — no `if`/`for`/`try`, no dynamic expected values. Hardcode. Trust > maintainability when they conflict.
5. **Design seams beat monkey-patching.** Parameters, factory functions, and constructor/interface injection make code testable *and* better designed.
6. **Prefer factory methods over `beforeEach`.** Tests read top-to-bottom; no scroll fatigue, no garbage-bin setup. Combine with helper methods (`addDefaultUser()`, `makeFakeLogger()`).
7. **Parameterize only when the scenario type is constant** — vary inputs/outputs, not behaviors. Use `test.each` or vanilla `for-of`.
8. **Three pillars: trustworthy, maintainable, readable.** Drop any one and the others fall.
9. **Avoid overspecification** — assert only observable behavior; use partial/regex matchers; ignore irrelevant schema/order.
10. **Quarantine flaky tests** and play *fix, convert, or kill*. Long-term goal: zero flaky tests.
11. **Use test recipes** to balance levels: mostly unit, some integration, few E2E. Split delivery (blocking) from discovery (non-blocking) pipelines; parallelize; run on every commit.
12. **For legacy code:** build a test-feasibility table, choose easy- or hard-first based on team experience, write characterization integration tests before refactoring.
13. **Metrics that matter:** escaped bugs, time-to-fix, defect density, trend lines — not raw coverage. Lagging (DORA) + leading (coverage/#tests) together.
14. **TDD is a separate skill** from good unit testing and from design — learn all three independently.
15. **Async testing:** choose Extract Entry Point vs Extract Adapter by which side is bulkier; keep 1–2 integration tests; use fake timers (`jest.useFakeTimers` + `advanceTimersToNextTimer`).
16. **Complicated interfaces** → apply ISP to make a per-consumer role interface; the same idea as Ports & Adapters.
17. **Triangulate isolation frameworks:** Jest (loose, function/module), substitute.js (typed, interface); never skip the mock/stub rule because a framework makes mocking easy.
18. **Organizational change:** identify champions + blockers; give both a role; time-box experiments; measure with the four DORA metrics; address all six influence factors (Patterson et al.).
19. **Spies vs fakes:** `jest.spyOn()` alone is a spy (tracks real calls); combine with `mockImplementation` to *fake*. Always `restoreAllMocks()` in `afterEach`.
20. **Make every passing test a tested test:** after green, intentionally break production and watch the test fail; revert.

---

## Cross-References

- Related: [[../Fundamentals_of_Software_Testing.md]] — ISTQB principles, test levels/types, black-box & white-box test design techniques.
- Related: [[../TDD_Top_Tips.md]] — Farley's Red/Green/Refactor discipline, "listen to your tests" as design feedback.
- Related: [[../The_Feedback-Driven_Developer.md]] — feedback loops at every level of the development cycle.
- Related: [[../What_to_Test_and_When.md]] — risk-based test selection; what to cover vs. what to skip.
- Related: [[../ATDD_Guide.md]] — Acceptance Test-Driven Development; specification by example.
- Related: [[../Modern_Software_Engineering.md]] — feedback-driven engineering; production telemetry as truth.
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] — SLOs, error budgets, incident response (overlap with §Trustworthy tests, §Flakiness).
- Related: [[../Building_Microservices.md]] — service boundaries make seams easier; per-service test recipes.
- Related: [[../Building_Evolutionary_Architectures.md]] — adaptive test/pipeline design as system grows; engineering fitness functions as automated gates.
- Related: [[../Microservices_Up_And_Running.md]] — testing across service boundaries; consumer-driven contract tests as automation of recipe enforcement.
- Related: [[../Observability_Engineering.md]] — production telemetry to detect escaped bugs (the leading vs lagging indicator).
- Topic index: [[../INDEX.md]]
