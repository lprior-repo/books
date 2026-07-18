# TDD Top Tips -- Comprehensive Summary

**Author:** Dave Farley (Continuous Delivery Ltd.)
**Original Date:** 11-05-22
**Summary Date:** April 2026

---

## Overview

This short but concentrated guide distills the most important practical advice for practitioners of Test Driven Development (TDD). Written by Dave Farley -- a leading voice in continuous delivery and software engineering best practices -- the document addresses not just the mechanics of TDD but the deeper design philosophy that makes it transformative when practiced well. Farley positions TDD as one of the very rare software engineering practices that can make a genuine, measurable difference to code quality. The guide is structured as a series of top tips organized thematically, covering when and how to use TDD, the mindset required, the shape of good tests, strategies for dealing with legacy code, refactoring, and practical advice for teams adopting the discipline.

The central thesis is that TDD is not merely a testing technique but a design technique. Writing tests first forces developers to think about their code from the outside in -- from the perspective of a consumer -- and this subtle pressure consistently produces better-designed, more modular, more maintainable software. However, Farley is clear that TDD is a skill that must be learned and practiced. There is no simple checklist or paint-by-numbers approach. The tips in this guide are intended to help practitioners navigate the common pitfalls and hurdles that arise during the learning process.

---

## When to Use TDD

### Start Any New Project with TDD

Farley's first and most straightforward piece of advice is that the easiest time to begin practicing TDD is at the start of a new project. When there is no existing code, no legacy constraints, and no entrenched design decisions to work around, the discipline of writing tests first can be established from day one. This creates a foundation of well-tested, well-designed code that will pay dividends throughout the life of the project.

Critically, Farley also insists on establishing a Continuous Integration (CI) system from the outset. CI provides the fast, automated feedback loop that makes TDD practical at scale. Running tests automatically on every change gives the team confidence that the codebase remains in a healthy state and that regressions are caught immediately. The combination of TDD and CI creates a virtuous cycle: TDD produces a comprehensive test suite, and CI ensures that suite is always running and providing value.

### Write All New Code with TDD

Even when working in an existing or legacy system, Farley advocates that all new code should be written with TDD. This is a pragmatic middle ground. You may not be able to retroactively test every line of a legacy codebase, but you can establish a beachhead of quality by insisting that any new code added to the system -- whether it is a new feature, a bug fix, or a refactoring -- is developed test-first.

This approach gradually improves the quality of the codebase over time. Each piece of TDD-developed code is better tested, better designed, and more modular than the code it replaces or extends. Over time, the proportion of well-tested code in the system grows, and the legacy problems shrink. The key discipline is to never write new code without a failing test that demands it.

### Start When You Are Clear on the Outcome

Farley draws an important distinction between understanding the problem and knowing the solution. You do not need to know how you will implement something before you start TDD. In fact, TDD is a technique for discovering the implementation. What you do need is clarity about the desired outcome -- what the code should do, not how it should do it.

This is the essence of designing from the outside in. By focusing on the outcome first, expressed as a test, you allow the implementation to emerge organically. The test defines the contract that the code must fulfill, and the code is then written to satisfy that contract in the simplest possible way.

### Always Start with a Failing Test

This is perhaps the most fundamental rule of TDD, and Farley emphasizes it strongly. Every piece of production code must be preceded by a failing test. The test must fail for the right reason -- it should fail because the functionality it describes does not yet exist, not because of a syntax error or a setup problem.

Farley also recommends predicting the outcome of the test before running it. This is not just a mechanical step; it is a mindfulness exercise. By thinking carefully about how and why the test will fail, you deepen your understanding of both the problem and the code you are about to write. This prediction step helps catch mistakes in the test itself and ensures that you are truly driving development from the test rather than writing tests that merely confirm what the code already does.

---

## Test to Evaluate Behaviour, NOT Implementation

This is one of the most important and frequently misunderstood principles in TDD, and Farley gives it significant attention. The core idea is that tests should be focused on the behaviour of the system -- the desirable outcomes that the system produces -- rather than on the details of how that behaviour is achieved internally.

### Why Behaviour Over Implementation?

When tests are coupled to implementation details, they become brittle. Any change to the internal structure of the code, even a change that preserves correct behaviour, risks breaking tests. This creates a disincentive to refactor and improve the code, which undermines one of the primary benefits of TDD.

Behaviour-focused tests, by contrast, are more stable and more useful. They define what the system should do, and as long as the system continues to do those things correctly, the tests pass. This gives developers the freedom to change the implementation freely -- to refactor, optimize, or restructure -- without fear of breaking the test suite.

### The "Different Implementations" Thought Experiment

Farley offers a practical technique for evaluating whether a test is behaviour-focused or implementation-coupled: imagine different implementations of the same functionality. If the test would still be valid and meaningful with a completely different implementation, then it is testing behaviour. If the test would break or become meaningless with a different implementation, then it is testing implementation details.

This is a powerful heuristic because it forces you to think about what really matters. For example, if you are testing a sorting function, a behaviour-focused test would verify that the output is correctly sorted, regardless of whether the implementation uses quicksort, mergesort, or bubble sort. An implementation-focused test might check the number of comparisons made or the order in which elements are accessed -- details that are specific to one particular algorithm.

### Design Your Code from the Outside In

This principle follows naturally from the behaviour-first approach. Since TDD requires writing the test before the code, the test defines the public interface to the code. The test is, in effect, the first consumer of the code, and this gives the developer the opportunity to design that interface from the consumer's perspective.

This outside-in design approach has a profound effect on code quality. Code that is designed to be easy to use from the outside tends to be more modular, more cohesive, and less coupled than code that is designed from the inside out. The subtle pressure to make the test easy to write naturally leads to better design decisions. Nobody wants to make their own life more difficult by creating a hard-to-use interface just so they can test it.

---

## Test First to Improve Design

Farley devotes significant attention to the idea that TDD is fundamentally a design practice, not just a testing practice. The act of writing a test first is an act of design.

### The Design Pressure of TDD

When you write a test before writing the code, you are forced to think about what the code should do and how it should be used. At the point of writing the test, there is no code yet -- there is only the question of what the code's interface should look like and what outcomes it should produce.

This creates what Farley describes as a "small, subtle pressure" to write code that is easy to use. Since the developer is both the author of the test and the author of the code, they have a direct incentive to make the interface clean and simple. This pressure, applied consistently across the entire codebase, has a significant cumulative effect on code quality.

The properties that emerge from this design pressure are the classic markers of high-quality software: modularity, cohesion, loose coupling, separation of concerns, and clear interfaces. These are not accidental byproducts of TDD -- they are the natural consequence of designing code from the consumer's perspective.

---

## The Three Mindsets of TDD: Red, Green, Refactor

The core TDD cycle is described by the simple mantra "Red, Green, Refactor." Farley breaks this down into three distinct mindsets, each with its own goals and constraints. Understanding and respecting these separate mindsets is crucial to practicing TDD effectively.

### Red: Write a Failing Test

The Red phase is about expressing a need. The goal is to write a test that clearly describes an outcome that the code needs to achieve. During this phase, the developer should focus entirely on the external view of the code -- how it will be seen and used by consumers -- without worrying about implementation details.

The test should fail, and it should fail for the right reason: the functionality it describes does not yet exist. The test should be expressive and clear about what it expects. This is not the time to think about how the code will work; it is the time to think about what the code should do.

### Green: Make the Test Pass

The Green phase begins when the test is failing. At this point, the code is in an unstable state -- there is a failing test that describes a gap in the functionality. The goal now is to get back to a safe, passing state as quickly and simply as possible.

Farley emphasizes simplicity in this phase. Write the minimum amount of code necessary to make the test pass. Do not try to fix everything at once. Do not try to implement features that are not demanded by the current test. Do not try to make the code elegant or general -- just make it work.

This is a crucial discipline. The temptation in the Green phase is to over-engineer, to anticipate future needs, or to clean up existing code. But the TDD cycle demands that you focus on one thing at a time: make this test pass, as simply as possible. Small steps, one at a time.

### Refactor: Improve the Design

The Refactor phase is where design quality happens. Now that the tests are passing and the code is in a safe state, you have the freedom to improve the code without fear of breaking anything. The tests act as a safety net, giving you confidence that any change you make that keeps the tests passing is a safe change.

During refactoring, the focus shifts to the implementation detail. The goal is to make the code simpler, more readable, more concise, more general, and easier to maintain. This is the time to eliminate duplication, improve naming, extract methods or classes, and generally leave the codebase in a better state than you found it.

Farley stresses several important principles for the Refactor phase:

- **Refactoring means behaviour-preserving change.** If you refactor and the behaviour of the code changes, it is not refactoring -- it is a bug. The tests are your guarantee that behaviour is preserved.
- **Use good tools.** Modern IDEs and editors (JetBrains, Eclipse, VS Code, Xcode) have excellent refactoring support that can automate many common refactoring operations safely.
- **Adopt the Boy Scout Rule.** Always leave the codebase in a better state after every commit. Even small improvements accumulate over time.

---

## Refactoring for Legacy Systems

Farley devotes a section to the specific challenge of refactoring legacy code -- code that was not developed with TDD and may have little or no test coverage. This is one of the most difficult scenarios in software development, and Farley offers a pragmatic strategy.

### A Strategy for Refactoring Legacy Code

1. **Add tests only for code that you are changing.** Do not attempt to test the entire legacy codebase. Focus your testing effort on the specific areas where you need to make changes. This is a targeted, pragmatic approach that provides safety where it is most needed.

2. **Use Approval Tests or Acceptance Tests to defend the code you want to change.** These are testing techniques that capture the current behaviour of the code (even if that behaviour contains bugs) and then guard against unintended changes. This creates a safety net that allows you to refactor with confidence.

3. **Prefer design choices that enhance modularity and cohesion.** When making changes to legacy code, use the opportunity to improve the design. Break large, monolithic functions into smaller, more focused ones. Separate concerns that have been tangled together. This makes the code easier to understand, test, and maintain.

4. **Reduce coupling through separation of concerns and abstraction.** Tight coupling is one of the biggest problems in legacy code. Use abstraction to decouple components, making them easier to test independently and easier to change without causing cascading failures.

5. **Do not retrofit TDD-style unit tests to legacy code.** This is a counterintuitive but important point. Retrofitting unit tests to existing code often results in tests that are tightly coupled to the implementation, because the tests are written with knowledge of how the code works. These tests provide little design benefit and become a maintenance burden. Instead, use higher-level tests (approval tests, acceptance tests) to capture behaviour, and then use TDD for any new code you write.

6. **Treat boundaries between modules and services with caution.** The boundaries between components, modules, services, and subsystems are critical points in the architecture. They should change more slowly than the internal details of the components they connect. Defend these boundaries with loosely-coupled design strategies and contract testing.

7. **Use the "Ports and Adapters" design strategy.** Also known as Hexagonal Architecture, this pattern insulates the core business logic of the system from external concerns like databases, user interfaces, and network communication. By defining clear interfaces (ports) and providing concrete implementations (adapters) for each external system, you create a system where the core logic can be tested independently and where external dependencies can be swapped out easily.

---

## The Shape of Your Tests

Farley provides guidance on what good tests look like and how to evaluate their quality. Good tests share certain properties that make them effective and maintainable.

### Simple, Expressive, and Focused

Tests should be simple to read and understand. Anyone looking at a test should be able to quickly understand what behaviour is being tested and what the expected outcome is. Tests should be expressive -- they should clearly communicate their intent. And they should be focused on a single outcome -- each test should verify one specific piece of behaviour.

This focus on simplicity and single-outcome testing is not just an aesthetic preference. It has practical benefits. Simple, focused tests are less tightly coupled to the system under test, which means they are less likely to break when the implementation changes. This is a crucial property of good tests: they should give you the freedom to change your code without constantly breaking the test suite.

### Listen to Your Tests

One of the most valuable aspects of TDD is the feedback it provides about your design. Farley encourages developers to listen to what their tests are telling them. If a test is hard to write, that is a signal that something is wrong with the design. The code may be too complex, the interface may be poorly designed, or the concerns may be improperly separated.

This is a diagnostic tool of enormous power. Test difficulty is not just an inconvenience -- it is information. It tells you where your design needs improvement. Rather than struggling to write a complex test, Farley advises decomposing the code into smaller, simpler pieces that are easier to test.

Similarly, if your tests are big or complex, that usually means one of two things: either you did not practice TDD (you wrote the test after the code, so the test is trying to cover too much ground), or there is a design problem. The solution is not to fix the test -- it is to fix the design problem that made the test complex in the first place.

---

## Changing Your Design

No design is perfect, and even the best TDD-practiced code will need to be restructured over time as understanding of the problem evolves and new requirements emerge. Farley addresses this reality honestly.

### The Inevitability of Change

Over time, your understanding of the problem you are solving will change. You will encounter new problems and discover better ways to solve old ones. This is normal and expected. The goal is not to get the design perfect from the start -- that is only possible for trivial problems. The goal is to create code that can be safely changed when needed.

TDD helps here in two ways. First, the design pressure of TDD tends to produce more modular, loosely-coupled code that is inherently easier to change. Second, the comprehensive test suite created by TDD provides the safety net needed to make changes with confidence.

### The Process of Restructuring

When you need to change your design, Farley recommends breaking the restructuring into small steps using refactoring techniques. Steer the code and tests gradually toward the new model, working to keep the tests passing for as long as possible throughout the process.

This is important: do not throw away your tests and start over. The tests are your safety net. If you discard them, you lose the ability to verify that your changes are behaviour-preserving. Instead, evolve the tests alongside the code, changing them incrementally as the design changes.

Farley is honest that changing your design always comes at a cost, even with TDD. "If you aim to work to be perfect first time, either your problem is trivial or you are in for disappointment." This is a realistic assessment. TDD makes design changes easier and safer, but it does not make them free. The investment you made in TDD pays off here, because now you have the safety to change things that would otherwise be too risky to touch.

He offers a useful metric: treat the ability to safely change your code at any point in its life as a measure of its quality. If you cannot change your code safely, the design is not good enough, regardless of how well it currently works.

---

## Testing at the Edges

Code that interacts with the boundaries of the system -- user interfaces, databases, file systems, network communication, hardware -- presents special challenges for testing. Farley addresses these challenges with specific strategies.

### The Problem with Edge Code

Edge code is inherently more complex than pure business logic. It involves I/O, which introduces concerns about latency, failure modes, state management, and external dependencies. These factors make edge code harder to test in isolation and more prone to flaky, unreliable tests.

### The Strategy: Minimize Edge Code, Maximize Abstraction

Farley's primary advice is to minimize the amount of code that directly touches the edges of the system. Push as much logic as possible away from the edges and into the core of the system, where it can be tested easily and thoroughly.

For the code that must touch the edges, improve the abstraction and separation of concerns. Define simple, clean interfaces that hide the details of the I/O interactions. The example Farley gives is illustrative:

A well-abstracted interface looks like `storeAccount(Account account)` -- the calling code expresses its intent at a high level of abstraction and does not need to know how the storage is implemented.

A poorly-abstracted interface leaks implementation details: `sqlCommand("UPDATE account_table SET (id = 1, name = my-account, ...) WHERE ...")` -- the calling code is now coupled to the specific storage mechanism and the details of the SQL query.

### Practical Advice for Edge Testing

- **Pick simple, generic cases for edge tests.** Do not try to test every possible behaviour through the edge. Test that the edge works correctly for a simple case, and trust the abstraction to handle variations.
- **Do not test business logic through edge tests.** Once you can "store an account," it does not matter whether you are storing it because an address changed or a phone number was added. The storage behaviour is the same regardless of the business reason.
- **Unit test pieces and use integration tests to validate interactions.** Test individual components in isolation using unit tests, and then use integration tests to verify that the components work together correctly when connected through the edge code.

---

## Practice

Farley concludes with practical advice for teams and individuals who want to adopt TDD.

### TDD is a Learned Skill

TDD improves the skills of the developer and the quality of the code they write, but it requires investment. Like any skill, it must be learned through deliberate practice. Reading about TDD is not sufficient -- you must actually do it, repeatedly, to develop the muscle memory and intuitive understanding that make TDD effective.

### Team Practices

- **Set expectations as a team.** Agree together to practice TDD and encourage each other to do so. TDD is most effective when the entire team is committed to the discipline.
- **Be diligent and disciplined.** Apply the skills consistently, even when it feels slow or awkward. The speed and ease will come with practice.

### Kata Practice

Farley strongly recommends regular practice of coding katas -- structured exercises designed to develop specific TDD skills. His specific recommendation for beginners is to practice katas for at least 30 minutes every day for two weeks. This intensive initial practice helps establish the habits and thought patterns that make TDD a natural part of the development workflow.

The key practices to reinforce through kata practice are:
1. Start with a failing test.
2. Only write code that is demanded by a test.
3. Follow the Red, Green, Refactor cycle.
4. Take small steps.
5. Focus on behaviour, not implementation.

### Learning Resources

Farley points to several resources for continued learning:

- **Cyber Dojo** (cyber-dojo.org): An online platform for practicing coding katas and TDD exercises in a variety of languages.
- **TDD and BDD: Design Through Testing**: A comprehensive self-paced training course by Dave Farley himself.
- **Recommended books:**
  - "Test Driven Development: By Example" by Kent Beck -- the foundational text on TDD.
  - "Growing Object Oriented Software Guided by Tests" by Nat Pryce and Steve Freeman -- a practical guide to TDD in object-oriented systems.
  - "Refactoring: Improving the Design of Existing Code" by Martin Fowler -- the definitive guide to refactoring techniques.
  - "Working Effectively with Legacy Code" by Michael Feathers -- strategies for bringing legacy code under test.
- **YouTube:** The Continuous Delivery YouTube channel, which includes a curated playlist of TDD-related videos.

---

## Key Takeaways

1. **TDD is a design discipline, not just a testing technique.** The primary value of TDD is not in catching bugs but in driving better code design. Writing tests first forces you to think about your code from the consumer's perspective, which naturally leads to cleaner interfaces, better modularity, and more maintainable software.

2. **Always start with a failing test.** Every piece of production code should be preceded by a failing test that describes the behaviour you want to implement. Predict how the test will fail before you run it to deepen your understanding of the problem.

3. **Follow the Red, Green, Refactor cycle strictly.** These are three distinct mindsets with different goals. Red is about expressing a need. Green is about satisfying that need as simply as possible. Refactor is about improving the quality of the code while preserving behaviour. Do not mix these concerns.

4. **Test behaviour, not implementation.** Tests that are coupled to implementation details are brittle and resist refactoring. Use the "different implementations" thought experiment to verify that your tests are focused on outcomes rather than mechanisms.

5. **Listen to your tests as design feedback.** If a test is hard to write, your design is probably too complex. If a test is large and complicated, you probably have a design problem. Fix the design, not the test.

6. **Design from the outside in.** Since the test is the first consumer of your code, use it to design the public interface. Make the interface easy to use from the test's perspective, and you will naturally create a better design.

7. **Take small steps.** Do not try to implement multiple features at once. Do not try to refactor and add functionality simultaneously. One failing test, one simple implementation, one small refactoring at a time.

8. **For legacy code, use targeted testing strategies.** Do not try to retrofit unit tests to existing code. Use approval tests and acceptance tests to capture current behaviour, and apply TDD to all new code. Use Ports and Adapters to insulate core logic from external dependencies.

9. **Minimize edge code and maximize abstraction.** Code that touches I/O boundaries is inherently harder to test. Keep it minimal, abstract it behind clean interfaces, and test business logic independently of edge concerns.

10. **Practice deliberately and consistently.** TDD is a skill that must be learned through practice. Use coding katas, commit to daily practice when starting out, and establish team agreements to support the discipline.

11. **Refactoring means behaviour-preserving change.** If you change the behaviour, it is not refactoring. Always keep your tests passing during refactoring. Use the safety net of tests to improve code quality with confidence.

12. **Treat changeability as a quality metric.** The ability to safely change your code at any point in its life is a direct measure of its quality. If you cannot change your code safely, invest in better tests, better abstractions, and better separation of concerns.

13. **Leave the codebase better than you found it.** Adopt the Boy Scout Rule and always make at least one small improvement during each coding session. These small improvements compound over time into a significantly better codebase.

14. **Embrace the cost of changing your mind.** Design changes are always somewhat painful, even with TDD. This is normal. The investment you made in TDD pays dividends precisely at these moments, giving you the safety to make changes that would otherwise be too risky.

15. **Establish Continuous Integration early.** TDD and CI are complementary practices. TDD produces a comprehensive test suite, and CI ensures that suite is always running. Together, they create a fast feedback loop that keeps the codebase healthy.
