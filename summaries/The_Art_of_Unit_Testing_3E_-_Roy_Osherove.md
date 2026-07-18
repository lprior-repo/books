# The Art of Unit Testing, Third Edition - Comprehensive Summary

**Author:** Roy Osherove, with Vladimir Khorikov
**Examples in:** JavaScript/TypeScript

---

## Overview

This book provides a comprehensive guide to unit testing, covering everything from fundamental definitions and first tests through advanced techniques for breaking dependencies, testing asynchronous code, and integrating testing into organizations. The third edition updates all examples to JavaScript/TypeScript using Jest, and introduces concepts like test recipes and delivery pipelines. The book is organized into four parts: Getting Started, Core Techniques, The Test Code (quality attributes), and Design and Process.

---

# Part 1: Getting Started

## Chapter 1: The Basics of Unit Testing

This chapter lays the conceptual foundation for the entire book.

### Unit of Work

A **unit of work** is the scope of the thing being tested. It can be a single function, a class, or a group of related classes that together represent a logical unit of behavior. The unit of work is bounded by its **entry points** (where you begin invoking the unit) and its **exit points** (where you observe the results).

### Entry Points and Exit Points

An **entry point** is the public API through which you invoke the unit of work -- typically a function call, constructor, or public method.

An **exit point** is where you observe what the unit of work has done. There are three types of exit points:

1. **Return value** -- The function returns a value you can assert against. This is the simplest and most preferred type.
2. **State change** -- The unit of work changes the state of the system (e.g., modifying an object property, updating a database) that you can verify through another function or property.
3. **Third-party call** -- The unit of work calls an external dependency (e.g., logging, sending email, calling an API). This is the hardest to test and requires mock objects.

### Defining a Unit Test

The book provides a refined definition: A unit test is an automated piece of code that invokes the unit of work being tested, and checks some specific end result against an expected behavior. Good unit tests are consistent, readable, maintainable, trustworthy, and run fast (in memory, with no external dependencies).

### Integration Tests

Integration tests differ from unit tests in that they use real external dependencies (databases, filesystems, networks). They provide more confidence but are slower, more complex, and more flaky.

### Test-Driven Development (TDD)

TDD is a development methodology where you write a failing test first, then write the minimum code to make it pass, then refactor. The book stresses that TDD is not a substitute for good unit tests -- you can write bad tests with TDD. Three core skills are needed: writing good tests, knowing how to design for testability, and being skilled enough to write tests first.

---

## Chapter 2: A First Unit Test

This chapter introduces Jest and walks through writing the first tests for a Password Verifier project.

### Jest Setup and Structure

Jest is the chosen framework for the book. Tests are discovered through `__tests__` folders or files ending in `.spec.js` or `.test.js`. Jest acts as test library, assertion library, test runner, and test reporter all in one.

### The Arrange-Act-Assert (AAA) Pattern

Tests follow the AAA pattern:
- **Arrange**: Set up inputs and dependencies
- **Act**: Invoke the entry point
- **Assert**: Check the exit point

### USE Naming Convention

Test names should contain three pieces of information (USE):
- **U**nit of work under test
- **S**cenario (inputs/conditions)
- **E**xpected behavior (exit point result)

Example: `test('verifyPassword, given a failing rule, returns errors', ...)`

### Test Organization Approaches

The chapter explores several approaches to organizing tests and reducing duplication:

1. **describe() blocks** -- Nested describe blocks can separate the unit, scenario, and expectation into hierarchical levels, providing clear context.

2. **it() vs test()** -- `it()` is an alias for `test()` that reads more naturally with describe blocks: "describe verifyPassword, with a failing rule, it returns errors."

3. **beforeEach()** -- Used to remove duplication but has downsides: causes scroll fatigue, tends to become a "garbage bin" of test initialization, and hides important setup from the test body.

4. **Factory methods (helper functions)** -- The preferred approach. Small helper functions that create objects or states, called directly from each test. They provide reuse without hiding setup details.

5. **Parameterized tests** -- Using `test.each()` to run the same test logic with different inputs and expected outputs, reducing duplication.

### Refactoring Production Code

The chapter demonstrates how production code changes affect tests by refactoring the Password Verifier from a pure function to a stateful class. This increases the surface of the unit of work (spanning `addRule` and `verify` together) and introduces coupling that affects test design.

### Checking for Thrown Errors

Tests for exceptions use a pattern like:
```javascript
expect(() => verifier.verify('anything')).toThrow("It's the weekend!");
```

### Test Categories

Jest supports categorizing tests (e.g., marking some as slow) using `describe.skip`, `test.skip`, or custom tags for CI pipeline filtering.

---

# Part 2: Core Techniques

## Chapter 3: Breaking Dependencies with Stubs

This chapter addresses the fundamental challenge of testing code that depends on external resources.

### Types of Dependencies

1. **Outgoing dependencies** (exit points) -- Things the unit of work calls, like loggers, databases, or email services. These represent requirements and are tested using **mocks**.

2. **Incoming dependencies** -- Things that provide data or behavior into the unit of work, like database queries or configuration values. These are not exit points and are handled using **stubs**.

### Stubs vs. Mocks

- **Stub**: Breaks incoming dependencies. Provides fake data or behavior INTO the code under test. You do NOT assert against stubs. You can have many stubs in a test.
- **Mock**: Breaks outgoing dependencies. A fake object/function that you ASSERT was called correctly. Represents an exit point. You should have no more than one mock per test.
- **Test double / Fake**: Generic terms for anything not real used in testing.

### Reasons to Use Stubs

The chapter uses a Password Verifier that depends on time (can't work on weekends) as a motivating example. Without stubs, tests become time-dependent, inconsistent, and potentially flaky.

### Injection Techniques

The book covers multiple approaches organized by programming paradigm:

**Functional injection:**
- **Parameter injection** -- Add the dependency as a parameter (e.g., `currentDay`). Simplest approach; makes the function pure.
- **Function as parameter** -- Pass a function that returns the dependency value: `getDayFn()`.
- **Partial application / currying** -- Use higher-order functions to preconfigure dependencies.
- **Factory functions / constructor functions** -- Create objects with pre-injected dependencies.

**Modular injection:**
- Abstract module dependencies behind an intermediary object with `inject` and `reset` functions. The book warns this couples tests to third-party API signatures.

**Object-oriented injection:**
- **Constructor injection** -- Pass dependencies through the class constructor. Makes dependencies explicit and required. Recommended as the default OO approach.
- **Property injection** -- Set dependencies via properties. Makes dependencies optional, which is less explicit.
- **Interface injection** -- Extract a common interface (using TypeScript) and inject implementations of that interface. Provides the strongest type safety and design clarity.

### Key Design Concepts

- **Seam**: A place where two pieces of software meet and something else can be injected (coined by Michael Feathers). Parameters, functions, module loaders, and interfaces are all seams.
- **Inversion of Control (IoC)**: Designing code so the responsibility for creating dependencies is externalized.
- **Dependency Injection (DI)**: The act of sending a dependency through a design seam.

---

## Chapter 4: Interaction Testing Using Mock Objects

This chapter covers how to test the third type of exit point: calls to third-party objects.

### Interaction Testing

**Interaction testing** verifies how a unit of work calls external dependencies. It checks that the right messages were sent to the right objects with the right parameters, at the right time.

### Why Mocks Matter

When code calls an external dependency (like a logger), you cannot verify the call through return values or state changes. Mock objects capture these outgoing calls so you can assert against them.

### Mock Injection Styles

The chapter demonstrates mock injection across the same paradigms as stubs:

**Standard style** -- Introduce parameter: add a logger parameter to the function.

**Modular style** -- Abstract module dependencies with inject/reset pattern. Useful but couples tests to external API shapes.

**Functional style** -- Use currying (with lodash's `_.curry`) or higher-order factory functions (`makeVerifier(rules, logger)` returns a preconfigured verifier function).

**Object-oriented style** -- Constructor injection with classes. The logger is passed through the constructor and stored as a class member.

### Handwritten Mocks

A handwritten mock is a simple object with a function that captures parameters:

```javascript
let written = '';
const mockLog = {
  info: (text) => { written = text; }
};
```

After invoking the unit of work, you assert on the captured value:
```javascript
expect(written).toMatch(/PASSED/);
```

### Differentiating Mocks from Stubs

The book strongly emphasizes naming conventions: use `mockXXX` only for things you assert against (exit points), and `stubXXX` for things that provide data. Having multiple mocks per test means testing multiple requirements, which reduces readability, maintainability, and trust.

### Dealing with Complicated Interfaces

When an interface has many methods (like `IComplicatedLogger` with info, debug, warn, error), creating handwritten fakes becomes tedious. The solution is the **Interface Segregation Principle** -- create a simpler interface that only exposes what the consumer needs.

### Partial Mocks

A **partial mock** is a real object where only some functions have been overridden with fake behavior. Useful for legacy code where you need to isolate specific behavior from an existing real object. The chapter shows both functional and object-oriented (inheritance-based) approaches.

---

## Chapter 5: Isolation Frameworks

This chapter introduces automated tools for creating dynamic stubs and mocks.

### What Is an Isolation Framework?

An isolation framework is a reusable library that can create and configure fake objects at runtime. These dynamic fakes replace the need for handwritten mocks and stubs, producing shorter, more readable code.

### Two Flavors

- **Loose (Jest, Sinon)** -- Vanilla JavaScript-friendly, good for functional styles and modules.
- **Typed (substitute.js)** -- TypeScript/OO-friendly, better for full classes and interfaces.

### Faking Modules with Jest

`jest.mock()` at the top of a spec file replaces entire modules with fakes:

```javascript
jest.mock("./complicated-logger");
jest.mock("./configuration-service");
```

The fake modules can then be configured in tests:
```javascript
stubConfigModule.getLogLevel.mockReturnValue("info");
```

And verified:
```javascript
expect(mockLoggerModule.info).toHaveBeenCalledWith(stringMatching(/PASS/));
```

The book warns that `jest.mock()` uses the word "mock" for both stubs and mocks, which can be confusing.

### Faking Functions with jest.fn()

`jest.fn()` creates a trackable function that can be used as a mock or stub:

```javascript
const mockLog = { info: jest.fn() };
// ... later ...
expect(mockLog.info).toHaveBeenCalledWith(stringMatching(/PASS/));
```

### Object-Oriented Fakes with substitute.js

`Substitute.for<Interface>()` generates a full fake object that automatically handles all interface methods:

```javascript
const mockLog = Substitute.for<IComplicatedLogger>();
// ... later ...
mockLog.received().info(Arg.is(x => x.includes("PASSED")), "verify");
```

This approach is more resilient to interface changes since you only specify the methods you care about.

### Stubbing Return Values

- `mockReturnValue()` -- Sets a permanent return value for the test.
- `mockReturnValueOnce()` -- Sets sequential return values.
- `mockImplementation()` -- Sets custom behavior or throws errors.

### Traps of Isolation Frameworks

1. **Unreadable test code** -- Overuse of framework APIs makes tests hard to follow.
2. **Verifying the wrong things** -- Asserting against stubs instead of mocks.
3. **More than one mock per test** -- Testing multiple requirements in one test.
4. **Overspecifying tests** -- Verifying internal implementation details rather than observable behavior.
5. **You don't need mock objects most of the time** -- Value-based tests (checking return values) are preferable to interaction-based tests.

---

## Chapter 6: Unit Testing Asynchronous Code

This chapter addresses testing callbacks, promises, async/await, timers, and DOM events.

### Integration Tests for Async Code

The simplest approach is to write integration tests using `done()` callbacks or `async/await`:

```javascript
test("NETWORK REQUIRED: correct content, true", async () => {
  const result = await samples.isWebsiteAliveWithAsyncAwait();
  expect(result.success).toBe(true);
});
```

Integration tests for async code suffer from the usual problems: slow, flaky, hard to simulate edge cases.

### Extract Entry Point Pattern

This pattern separates async code into two parts:
1. The async orchestration (which stays as-is)
2. The logical processing (which is extracted into pure, synchronous functions)

The extracted functions become new entry points for unit tests. The original async function retains one or two integration tests for confidence.

Example:
```javascript
// Extracted synchronous entry point
const processFetchContent = (text) => {
  const included = text.includes("illustrative");
  if (included) return { success: true, status: "ok" };
  return { success: false, status: "missing text" };
};

// Unit test - no async needed
test("on fetch success with good content, returns true", () => {
  const result = samples.processFetchContent("illustrative");
  expect(result.success).toBe(true);
});
```

### Extract Adapter Pattern

This pattern wraps the async dependency behind a simplified adapter interface:

1. Create a `network-adapter` module that wraps `node-fetch`
2. Inject the adapter (modular, functional, or OO style)
3. Fake the adapter in tests, making async code testable synchronously

Three injection styles are shown:
- **Modular**: `jest.mock("./network-adapter")` to fake the module
- **Functional**: Pass the adapter as a parameter
- **Object-oriented**: Constructor injection with a typed interface

### Dealing with Timers

Tests using `setTimeout` can be controlled by:
- **Stubbing timers** -- Replacing `setTimeout` with a fake
- **Using Jest's timer APIs** -- `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, `jest.clearAllTimers()`

### Dealing with Events

The chapter covers testing event emitters and DOM click events. For DOM testing, the book introduces the Testing Library pattern, which interacts with the DOM through user-facing queries rather than implementation details.

---

# Part 3: The Test Code

## Chapter 7: Trustworthy Tests

This chapter is the first of three about test quality, focusing on trustworthiness. The three pillars of good tests are:
1. **Trustworthiness** -- Tests that reliably report bugs
2. **Maintainability** -- Tests that don't require excessive effort to maintain
3. **Readability** -- Tests that can be understood without reading the code

### How to Know You Trust a Test

You don't trust a test if:
- It fails and you're not worried
- You feel fine ignoring results
- It passes and you're still worried
- You still feel the need to manually test

You trust a test if:
- It fails and you're genuinely concerned
- It passes and you feel relaxed

### Why Tests Fail (Besides Real Bugs)

1. **Buggy test** -- The test itself has a bug. Fix it, then verify by introducing a deliberate bug in production code to confirm the test catches it.
2. **Out-of-date test** -- Functionality changed but the test wasn't updated. Either adapt or remove the test.
3. **Conflicting test** -- Two tests expect different behavior from the same code. Remove the irrelevant one (consult product owner).
4. **Flaky test** -- Fails inconsistently without code changes.

### Avoiding Logic in Unit Tests

Logic in tests introduces the risk of test bugs. Avoid:
- `switch`, `if`, `else` statements
- `foreach`, `for`, `while` loops
- String concatenations in asserts
- `try/catch`

The most dangerous pattern is **dynamically creating expected values** that repeat production code logic:

```javascript
// BAD - repeats the algorithm being tested
expect(result).toBe("hello" + name);

// GOOD - hardcoded expected value
expect(result).toBe("hello abc");
```

When push comes to shove, trust should trump maintainability. A highly maintainable test you cannot trust is worthless.

### False Trust in Passing Tests

Warning signs:
1. **No asserts** -- The test runs code but verifies nothing. Remove it or add a `not.toThrow()` check.
2. **Can't understand the test** -- Bad names, confusing variables, hidden logic.
3. **Mixed unit and integration tests** -- Integration tests can be flaky, and developers will start dismissing all failures.
4. **Testing multiple exit points** -- Multiple concerns in one test means you can't see all failures. Split into separate tests.
5. **Tests that keep changing** -- Tests using current time, random numbers, or other dynamic values are never the same test twice.

**Tip on multiple asserts**: It's okay to assert multiple things that are part of the same concern (e.g., checking both `name` and `age` of a returned person object). The rule of thumb: if the first assert fails, do you still care about the next one? If yes, split the test.

### Dealing with Flaky Tests

Flakiness correlates with test level:
- **Unit tests**: Nearly no flakiness (full control over dependencies)
- **Integration tests**: Moderate flakiness (real dependencies introduce variability)
- **E2E tests**: High flakiness (network, configuration, external systems)

What to do when you find a flaky test:
- Move it out of the "safe green zone" (where unit tests live)
- Investigate the root cause
- Consider running it in a separate pipeline

Preventing flakiness in higher-level tests:
- Use dedicated test environments
- Reset state between tests
- Avoid depending on external systems you don't control

---

## Chapter 8: Maintainability

This chapter focuses on keeping tests maintainable over time.

### Changes Forced by Failing Tests

Tests fail for several maintainability-related reasons:

1. **Test not relevant or conflicts** -- Remove the irrelevant test.
2. **Production code API changes** -- When constructor signatures or function parameters change, tests break. Mitigate with **factory functions** that create the object under test, so you only need to update one place.
3. **Changes in other tests** -- Tests should be independent. Avoid shared mutable state.

### Avoid Testing Private Methods

Private methods are implementation details. Testing them couples tests to internal changes, causing false failures. Options:
- Test through the public method that calls the private one
- Make the method public if it has a meaningful contract
- Extract the method into a separate class or module
- Make stateless private methods public and static

### Keep Tests DRY

Duplication in tests hurts as much as in production code. When a constructor changes, duplicated test setup must change everywhere. Use helper methods to reduce duplication, but don't sacrifice readability.

### Avoid Setup Methods (beforeEach)

The author strongly prefers helper methods over `beforeEach` because:
- Setup methods can only initialize things; they can't have parameters or return values
- They become dumping grounds for unrelated initialization
- Mocks and stubs in setup methods are hidden from test readers
- They can only apply to all tests, leading to tests that need some setup but not all

### Use Parameterized Tests

`test.each()` in Jest allows running the same test logic with different inputs, removing duplication in both arrange and assert sections:

```javascript
test.each([
  ['1', 1],
  ['2', 2]
])('for input %s, returns %i', (input, expected) => {
  const result = sum(input);
  expect(result).toBe(expected);
});
```

### Avoid Overspecification

Overspecified tests make assumptions about internal implementation rather than observable behavior. Common forms:

1. **Internal behavior overspecification** -- Verifying that a protected/private method was called, rather than checking the return value or state change. The fix: test the real exit point (return value, state change, or third-party call).

2. **Exact output and ordering overspecification** -- Asserting on complete object structure and ordering when only specific values matter. Fix: check only the properties you care about, use partial matching, and ignore ordering when irrelevant.

3. **String overspecification** -- Using `toBe()` for exact string matches when `toMatch()` or `toContain()` would be more resilient:
```javascript
// BAD
expect(msg).toBe("you have 2 failed rules.");
// GOOD
expect(msg).toMatch(/2 failed/);
```

---

## Chapter 9: Readability

The final quality pillar chapter focuses on making tests readable.

### Naming Unit Tests

Every test name should communicate three pieces of information:
1. The **unit of work** being tested
2. The **scenario** (conditions/inputs)
3. The **expected behavior** (what should happen)

These can be in the test name directly or spread across describe/it blocks:

```javascript
test('verifyPassword, with a failing rule, returns error based on rule.reason')
// or
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns error based on the rule.reason', () => { ... })
  })
})
```

Good test names serve as **executable documentation** -- a new developer should understand component behavior by reading test names. They're also what appears in build pipeline failure logs.

### Magic Values and Variable Naming

**Magic values** are hardcoded constants without explanation. Examples: `0` (what day?), `[]` (no rules?), `'jhGGu78!'` (why this password?).

Fix: Wrap values in meaningfully named variables:

```javascript
const SUNDAY = 0, NO_RULES = [];
expect(() => verifyPassword2("anything", NO_RULES, SUNDAY)).toThrowError(...)
```

Variable names should explain both what IS important and what is NOT important. Using `"anything"` as a password input tells the reader the specific value doesn't matter.

### Separating Asserts from Actions

Always separate the act and assert parts:

```javascript
// BAD - act and assert in one line
expect(verifier.verify("any value")[0]).toContain("fake reason");

// GOOD - separated
const result = verifier.verify("any value");
expect(result[0]).toContain("fake reason");
```

This improves readability and debuggability.

### Setting Up and Tearing Down

Avoid using `beforeEach` to set up mocks and stubs. Initialize them directly in each test so readers can see the full picture. If concerned about duplication, use helper functions called from within each test rather than setup methods.

---

# Part 4: Design and Process

## Chapter 10: Developing a Testing Strategy

This chapter steps back from unit testing to discuss how all test types fit together in an organizational strategy.

### Test Levels (from low to high)

| Level | Speed | Flakiness | Confidence | Maintainability |
|-------|-------|-----------|------------|-----------------|
| Unit/Component | 5/5 | 1/5 | 1/5 | 5/5 |
| Integration (in-memory) | 3-4/5 | 2-3/5 | 2-3/5 | 3-4/5 |
| API (out-of-process) | 2-3/5 | 3-4/5 | 3-4/5 | 2-3/5 |
| E2E/UI isolated | 1-2/5 | 4/5 | 4/5 | 1-2/5 |
| E2E/UI system | 1/5 | 5/5 | 5/5 | 1/5 |

Key insight: Higher-level tests provide more confidence but cost more in speed, flakiness, and maintenance.

### Test-Level Antipatterns

1. **End-to-end-only antipattern** -- The organization relies almost entirely on E2E tests. Problems:
   - Diminishing returns: the second E2E test adds a fraction of the confidence of the first, but costs the same
   - Creates "build whisperers" -- people who must analyze failing flaky tests to determine if failures are real
   - Promotes "throw it over the wall" mentality between developers and QA
   - Driven by sunk-cost fallacy and separation of duties

2. **Low-level-only antipattern** -- Only unit tests exist. Tests run fast but don't provide enough confidence, so people still manually test everything.

3. **Disconnected low-level and high-level tests** -- Both unit and E2E tests exist, but E2E tests duplicate scenarios already covered at lower levels instead of focusing on integration confidence.

### Test Recipes

A **test recipe** is an informal plan for how a feature will be tested, outlining which scenarios are tested at which level. It should include the happy path and significant edge cases.

Rules for test recipes:
- Have at least two people create it (developer + tester perspective)
- Store it with the feature story/task
- Create it just before starting work on the feature
- The recipe becomes part of the definition of "done"
- It's a living document that can change

### Managing Delivery Pipelines

**Delivery vs. Discovery pipelines**:
- **Delivery pipeline** -- Must pass before code can be deployed. Contains fast, non-flaky tests. Blocks the delivery.
- **Discovery pipeline** -- Contains flaky, slow, or exploratory tests. Runs in parallel but doesn't block delivery. Failures are investigated but don't halt deployment.

**Test layer parallelization**: Run different test levels in separate pipeline stages. Fast unit tests run first; slower tests run in parallel afterward. Never do nightly builds -- tests should run as soon as possible after code changes.

---

## Chapter 11: Integrating Unit Testing into the Organization

This chapter addresses the human and organizational challenges of adopting unit testing.

### Steps to Becoming an Agent of Change

1. **Prepare for tough questions** -- Managers worry about time; QA worries about relevance; developers worry about effort.
2. **Identify champions and blockers**:
   - **Champions**: People who support the initiative. Give them visibility and resources.
   - **Blockers**: People who resist. Understand their concerns (often personal: job security, deadlines, comfort zone).
3. **Identify starting points**: Choose smaller teams, feasible projects, and subteams for experiments.

### Ways to Succeed

1. **Guerrilla implementation (bottom-up)** -- Developers start writing tests without official mandate. Works well when management doesn't care about testing.
2. **Convincing management (top-down)** -- Show the business value. Use metrics like escaped bugs, time to fix, and defect density.
3. **Experiments as door openers** -- Run time-boxed experiments on a specific feature or team. Compare results with and without tests. "Walk the walk."
4. **Get an outside champion** -- External consultants can lend authority to the initiative.
5. **Make progress visible** -- Use dashboards showing metrics like test counts, build status, and trend lines.
6. **Aim for specific goals, metrics, and KPIs**:
   - **Lagging indicators**: Defect count, escaped bugs, production incidents
   - **Leading indicators**: Number of tests written, test coverage percentage (but not as a goal on its own)
   - **Qualitative metrics**: Developer confidence surveys, time to fix trends

### Ways to Fail

1. **Lack of a driving force** -- No one champions the initiative consistently.
2. **Lack of political support** -- Management doesn't back the effort.
3. **Bad first impressions** -- Initial attempts are poorly executed, souring perceptions.
4. **Lack of team support** -- Team members don't buy in.

### Influence Factors

The chapter discusses how factors like team size, project criticality, and company culture affect adoption strategies.

### Tough Questions and Answers

- **"How much time will unit testing add?"** -- Initially 10-30% more development time, but this is offset by fewer bugs, faster debugging, and reduced regression testing. Studies show higher code quality increases overall productivity.

- **"Will QA lose their jobs?"** -- No. QA shifts from manual testing to higher-value activities: exploratory testing, test strategy, and automation oversight.

- **"Is there proof unit testing helps?"** -- Yes. Multiple studies (including those by Capers Jones) show higher code quality correlates with higher productivity.

- **"We have lots of untested code. Where do we start?"** -- Focus on the 20% of code that has 80% of the bugs. Start with new features and bug fixes.

- **"How can we know we don't have bugs in our tests?"** -- Use TDD to see tests fail first. Keep tests simple and logic-free. Test important scenarios.

- **"Why do I need tests if my debugger shows code works?"** -- Debugging shows code works NOW. Tests prove it continues to work in the FUTURE. Tests are regression protection.

---

## Chapter 12: Working with Legacy Code

This chapter addresses the challenge of adding tests to existing, untested codebases.

### Where to Start Adding Tests

Create a **test-feasibility table** rating each component on:
1. **Logical complexity** (cyclomatic complexity) -- 1-10
2. **Dependency level** -- How many dependencies must be broken (1-10)
3. **Priority** -- Business importance (1-10)

Components with low complexity and low priority can be ignored. Focus on components above a threshold (typically complexity >= 3).

### Selection Strategies

**Easy-first strategy**:
- Start with components that have fewer dependencies
- Quick wins build team confidence
- Downside: hardest components remain until the end, when timeline pressure is highest

**Hard-first strategy**:
- Start with the most complex, most dependent components
- Every component brought under test may solve testability issues for other parts of the system
- Quick decline in effort over time
- Requires experienced team

### Writing Integration Tests Before Refactoring

The recommended process for legacy code:
1. Write integration tests against the existing system to capture current behavior
2. Add a failing test for the feature/fix being added
3. Refactor in small chunks, running integration tests frequently
4. Over time, replace integration tests with more focused unit tests as the code becomes more testable

### Recommended Resources

- *Working Effectively with Legacy Code* by Michael Feathers -- The definitive guide to legacy code refactoring
- *Unit Testing Principles, Practices, and Patterns* by Vladimir Khorikov -- In-depth refactoring examples
- **CodeScene** -- A tool for discovering technical debt in legacy code

---

# Appendix: Monkey-Patching Functions and Modules

The appendix covers less recommended techniques for faking dependencies when code cannot be refactored.

### Warning

Monkey-patching should be a last resort. The code comes out better when you build seams into the design rather than patching around it.

### Techniques Covered

1. **Manual monkey-patching** -- Save a global function, replace it, test, then restore. Error-prone because restoration might not happen on test failure.

2. **beforeEach/afterEach cleanup** -- Improves reliability but still has parallelism issues.

3. **jest.spyOn() + mockImplementation()** -- Jest's recommended approach for patching global functions. `jest.restoreAllMocks()` in afterEach handles cleanup.

4. **Ignoring whole modules with jest.mock()** -- Safest approach when you don't need custom behavior from the fake module.

5. **CFRA Pattern (Clear-Fake-Require-Act)** -- For faking custom module behavior per test:
   - Clear cached modules
   - Fake the module
   - Require the code under test
   - Act (invoke the entry point)

6. **Sinon.js and testdouble** -- Alternative frameworks for module stubbing with potentially cleaner APIs than Jest.

---

# Key Takeaways

1. **A unit test has three types of exit points**: return values, state changes, and third-party calls. Each requires different testing techniques.

2. **Stubs break incoming dependencies (provide fake data IN); mocks break outgoing dependencies (verify calls going OUT)**. Never assert against a stub. Have at most one mock per test.

3. **The Arrange-Act-Assert pattern** is the fundamental test structure. Keep it visible and clear.

4. **USE naming** (Unit, Scenario, Expected behavior) makes test names meaningful and useful as executable documentation.

5. **Prefer factory/helper methods over beforeEach()** to reduce duplication while maintaining readability. Tests should tell a self-contained story.

6. **Avoid logic in tests** -- no if/else, loops, or dynamic expected values. Logic in tests introduces test bugs.

7. **Extract Entry Point and Extract Adapter patterns** make async code unit-testable by separating logical processing from asynchronous orchestration.

8. **The three pillars of good tests** are trustworthiness, maintainability, and readability. Drop any one and the others suffer.

9. **Avoid overspecification** -- test observable behavior (public contracts), not implementation details. Use partial matching (`toMatch`, `toContain`) instead of exact equality where possible.

10. **Test recipes** provide a strategy for balancing test levels. Have mostly unit/component tests, some integration tests, and minimal E2E tests.

11. **Separate delivery and discovery pipelines** -- fast, non-flaky tests should block delivery; flaky or slow tests should run in parallel without blocking.

12. **When adopting testing in an organization**, start with champions, run experiments, make progress visible, and use meaningful metrics (escaped bugs, time to fix) rather than raw coverage numbers.

13. **For legacy code**, create a test-feasibility table, start with either easy or hard components depending on team experience, and write integration tests before refactoring.

14. **Prefer designing code with seams** (parameters, interfaces, factory functions) over monkey-patching and framework tricks. Better design leads to better tests, and better tests lead to better design.
