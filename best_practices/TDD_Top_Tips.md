# TDD Top Tips
**Author:** Dave Farley (Continuous Delivery Ltd.)
**Topic tags:** `#testing` `#process` `#tdd` `#design` `#refactoring` `#legacy-code`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/TDD Top Tips 11-05-22/TDD Top Tips 11-05-22.md` · `summaries/TDD_Top_Tips.md`

## TL;DR
TDD is a design discipline disguised as a testing technique. The Red-Green-Refactor cycle, applied strictly, drives outside-in design, prevents broken commits, and produces code that is easy to change. Apply whenever adding new behavior — including to legacy systems, where TDD governs all new code while legacy seams are guarded with approval/acceptance tests.

---

## Best Practices by Topic

### When to Use TDD

**Principle:** The right time to start TDD is *now*, including in legacy codebases. The discipline governs new code; legacy seams are handled separately.

**Do:**
- **Start any new project with TDD.** Establish Continuous Integration from day one — TDD and CI are complementary.
- **Write all new code with TDD** — even additions/improvements to legacy systems. Adopt the rule: no new code without a failing test that demands it.
- **Start when you are clear on the outcome**, not when you know the solution. The test expresses the outcome; the implementation emerges.
- **Always start with a failing test.** Every piece of production code is preceded by a failing test.
- **Predict how the test will fail before you run it** — deepens understanding and catches mistakes in the test itself.

**Don't:**
- Wait until you know the implementation before writing a test.
- Write code without a failing test demanding it.
- Skip CI setup — TDD without fast automated execution loses most of its value.
- Try to retroactively TDD an entire legacy codebase at once.

*Ref: TDD Top Tips 11-05-22.md — "When to Use TDD?"*

---

### Test Behaviour, Not Implementation

**Principle:** Tests should evaluate the desirable *outcome* of the system, not the *details* of how it is achieved. Implementation-coupled tests are brittle and discourage refactoring.

**Do:**
- Apply the **"different implementations" thought experiment**: imagine a completely different implementation that achieves the same goals. If the test would still be valid, it tests behaviour. If it would break or become meaningless, it tests implementation.
- Test outcomes, not mechanisms. Example: for a sort function, verify the output is sorted — don't count comparisons or assert on internal data-structure state.
- Design the **public interface** from the outside in: the test is the first consumer of the code, so its needs define the API.
- Ask: *would the least-technical domain-expert reader understand this test?* If not, it's too implementation-coupled.

**Don't:**
- Couple tests to internal data structures, algorithms, or call sequences.
- Assert on private state.
- Make tests that break on every refactor even when behaviour is preserved.

*Ref: TDD Top Tips 11-05-22.md — "Test to Evaluate Behaviour, NOT Implementation"*

---

### Test First to Improve Design

**Principle:** Writing the test first creates subtle, sustained pressure to write code that is easy to use — and that pressure compounds into better modularity, cohesion, and loose coupling.

**Do:**
- Treat the test as the first design exercise. At the moment of writing the test, no code exists yet — you are forced into the consumer's perspective.
- Use that pressure: if the test is hard to write, the design is wrong. Don't fight the test; fix the design.
- Embrace the markers of high-quality code that emerge from this pressure: modularity, cohesion, loose coupling, separation of concerns, clear interfaces.

**Don't:**
- Write the test after the code and then call it "TDD".
- Ignore test-difficulty signals. They are design feedback, not friction.

*Ref: TDD Top Tips 11-05-22.md — "Test First To Improve Design"*

---

### The Three Mindsets — Red, Green, Refactor

**Principle:** Each phase is a distinct mindset with its own goal. Mixing them is the most common TDD failure.

#### Red — Express a Need
- Write a test that clearly expresses the outcome your code must achieve.
- Focus on the **external view** — how the code will be seen and used.
- The test must fail for the **right reason** (functionality doesn't exist yet), not a syntax or setup error.

#### Green — Make It Pass, Minimally
- The code is in an unstable state; restore safety as fast and simply as possible.
- Write the **minimum code necessary** to make the test pass.
- **Small steps, one at a time.** Do not fix or improve everything at once.
- Do not refactor during Green. Do not add features not demanded by the current test.

#### Refactor — Improve the Design
- Now that tests pass, focus on the implementation detail.
- Refactor for: simplicity, readability, conciseness, generality, testability.
- **Refactoring is behaviour-preserving change.** If behaviour changes, it isn't refactoring — it's a bug.
- Use good refactoring tools (JetBrains, Eclipse, VS Code, Xcode).
- Adopt the **Boy Scout Rule**: always leave the codebase in a better state after every commit.

*Ref: TDD Top Tips 11-05-22.md — "Three Mindsets of TDD"*

---

### Refactoring for Legacy Systems

**Principle:** Refactoring is behaviour-preserving change. Do not retroactively TDD legacy code — the tests would couple to existing implementation and add maintenance burden without design benefit.

**Do:**
- **Add tests only for code you are changing.** Focus testing effort where you need safety.
- **Use Approval Tests or Acceptance Tests** to defend the code you want to change — capture current behaviour (bugs and all) as a safety net.
- Prefer design choices that **enhance modularity and cohesion** during changes.
- **Reduce coupling** through separation of concerns and abstraction.
- **Treat boundaries** (between modules, services, components, subsystems) with caution — they should change more slowly than internal details. Defend them with loose coupling and contract testing.
- Use **Ports & Adapters (Hexagonal Architecture)** to insulate core logic from I/O, databases, UIs, and network — making core logic independently testable.

**Don't:**
- "Retrofit" TDD-style unit tests to legacy code — they will be implementation-coupled and brittle.
- Change boundary contracts freely; defend them with tests and loose coupling.
- Refactor and change behaviour in the same step.

*Ref: TDD Top Tips 11-05-22.md — "Refactoring for Legacy Systems"*

---

### The Shape of Your Tests

**Principle:** Good tests are simple, expressive, and focused on a single outcome. This minimizes coupling to the SUT and frees you to refactor.

**Do:**
- Keep tests **simple, expressive, focused on a single outcome**.
- **Listen to your tests.** Difficulty writing a test is a signal that the design is too complex — decompose into smaller pieces.
- If a test is **big or complex**, fix the design problem, not the test. (Big tests usually mean code was written before the test, or the design is wrong.)

**Don't:**
- Write tests that cover too much ground in one method.
- Tolerate complex tests as the norm — it's a code smell, not an acceptable cost of TDD.
- Treat test-difficulty as friction to push through; treat it as information.

*Ref: TDD Top Tips 11-05-22.md — "The Shape of Your Tests" / "Listen to Your Tests"*

---

### Changing Your Design

**Principle:** No design is perfect; the goal is code that is safe to change at any point in its life. TDD pays for itself precisely when requirements evolve.

**Do:**
- Break restructuring into **small refactoring steps**, keeping tests passing throughout.
- Evolve tests alongside the code — don't throw tests away and start over.
- Treat **changeability** as a quality metric: if you cannot safely change your code, the design is not good enough.
- Expect design changes to have a cost; the TDD investment is the safety net that makes them affordable.

**Don't:**
- Aim for perfect-first-time designs. Either the problem is trivial or you will be disappointed.
- Refactor in big-bang steps that take the suite red for hours.
- Discard tests during redesigns.

*Ref: TDD Top Tips 11-05-22.md — "Changing Your Design"*

---

### Testing at the Edges

**Principle:** Code that touches I/O (UIs, databases, file systems, network, hardware) is inherently harder to test. Minimize it; maximize abstraction over what remains.

**Do:**
- **Minimize edge code.** Push as much logic as possible into the core where it is easy to test thoroughly.
- **Abstract I/O behind clean interfaces.** Compare:
  ```
  storeAccount(Account account)        // good — caller expresses intent
  ```
  vs.
  ```
  sqlCommand("UPDATE account_table SET (id = 1, name = my-account, ...) WHERE ...")   // bad — leaks storage detail into logic
  ```
- **Pick simple, generic cases for edge tests.** Don't try to test all behaviours through the edges.
- **Don't test business logic through edge tests.** Once you can "store an account", it doesn't matter *why* you're storing it (address change, phone number change, etc.).
- **Unit test pieces** and use **integration tests to validate interactions** through the edge.

**Don't:**
- Spread SQL/HTTP/UI calls through business logic.
- Try to test every variation of business behaviour through an edge — test the edge once, trust the abstraction for variations.

*Ref: TDD Top Tips 11-05-22.md — "Testing at the Edges"*

---

### Practice — Making TDD a Skill

**Principle:** TDD is a learned skill. Reading is not enough; deliberate practice is required.

**Do:**
- **Set team expectations** — agree together to practise and encourage each other.
- **Be diligent and disciplined** — apply skills consistently even when it feels slow.
- **Practise coding katas daily** when starting out (Farley recommends ≥ 30 minutes/day for 2 weeks). Use Cyber Dojo.
- Reinforce the core habits in kata work:
  1. Start with a failing test.
  2. Only write code demanded by a test.
  3. Follow Red, Green, Refactor strictly.
  4. Take small steps.
  5. Focus on behaviour, not implementation.

**Don't:**
- Treat TDD as intuitive — it requires deliberate practice to internalize the discipline.
- Expect speed and ease immediately. They come with repetition.

*Ref: TDD Top Tips 11-05-22.md — "Practise"*

---

### Refactoring Discipline

**Principle:** Refactoring and behaviour change are different activities; do not mix them.

- Refactoring = behaviour-preserving change. The test suite proves it.
- Use IDE refactoring tools for mechanical safety.
- Always leave the codebase better than you found it (Boy Scout Rule).

---

## Anti-Patterns & Common Mistakes

- **Writing tests after the code and calling it TDD:** Loses the design pressure and the outside-in perspective. *Fix:* write the failing test first, every time.
- **Mixing Red/Green/Refactor mindsets:** Adding features during refactor or refactoring during Green. *Fix:* discipline yourself to one mindset per phase.
- **Testing implementation, not behaviour:** Tests break on every refactor and discourage improvement. *Fix:* apply the "different implementations" test to every test you write.
- **Retrofitting TDD-style unit tests onto legacy code:** Tests couple to implementation and create maintenance burden. *Fix:* use Approval/Acceptance tests as a safety net; apply TDD only to new code.
- **Big-bang changes:** Refactoring in huge steps with the suite red for hours. *Fix:* small refactoring steps, tests passing throughout.
- **Complex tests as the norm:** Indicates design problems, not TDD failure. *Fix:* decompose code into smaller, simpler pieces.
- **Fighting test difficulty:** Pushing through a hard-to-write test rather than redesigning. *Fix:* trust the signal; fix the design.
- **Optimizing premature / over-engineering:** Complicates code without benefit. *Fix:* keep code simple; only optimize when measured.

*Ref: TDD Top_Tips.md — "Three Mindsets of TDD" / "Listen to Your Tests" / "Refactoring for Legacy Systems"*

---

## Decision Heuristics / Checklists

- **Should I write a test first?** Yes — for any new code or behaviour change. Even a one-line fix should have a regression test.
- **Is my test behaviour-focused?** Apply the "different implementations" test.
- **Is my Green phase minimal?** If you wrote more than the minimum to pass, you're over-implementing.
- **Is my refactor behaviour-preserving?** Are all tests still green? If not, you changed behaviour.
- **Is this a design problem or a test problem?** Big/complex test → design problem.
- **Touching legacy code?** Approval/Acceptance test first, then Ports & Adapters to expose a seam, then TDD the new code.
- **Does this code touch an edge?** Minimize, abstract, test the edge once, unit-test the rest.

---

## Key Takeaways

1. TDD is a **design discipline** — the test-first pressure produces better interfaces, modularity, and maintainability.
2. **Always start with a failing test.** Predict how it will fail.
3. **Red / Green / Refactor** are three distinct mindsets — don't mix them.
4. **Test behaviour, not implementation.** Use the "different implementations" thought experiment.
5. **Listen to your tests** — difficulty writing a test is design feedback.
6. **Design from the outside in** — the test is the first consumer of your code.
7. **Take small steps.**
8. **Refactoring = behaviour-preserving change.** Don't mix it with feature work.
9. **For legacy code:** don't retrofit TDD; use Approval/Acceptance tests as the safety net and apply TDD only to new code.
10. **Minimize edge code** and **maximize abstraction** over I/O.
11. **Treat changeability as a quality metric.**
12. **Leave the codebase better than you found it.**
13. **Practice deliberately** — katas daily for two weeks when starting out.
14. **TDD + CI are complementary** — establish CI from day one.

---

## Cross-References
- Related: [[../The_Art_of_Unit_Testing.md]]
- Related: [[../Fundamentals_of_Software_Testing.md]]
- Related: [[../What_to_Test_and_When.md]]
- Related: [[../ATDD_Guide.md]]
- Related: [[../The_Feedback-Driven_Developer.md]]