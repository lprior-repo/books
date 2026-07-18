# Summary: The Software Developers' Guidebook

**Author:** Dave Farley (Edited by Bernard McCarty)
**Published:** 2025 (Leanpub)

This summary covers Dave Farley's practical collection of modern engineering practices for software developers. The book distills decades of real-world experience into actionable guidance spanning project inception, testing strategy, continuous delivery, architecture, and developer habits.

---

## Part 1: Foundations of Modern Software Development

### Starting a New Project

Farley opens with a fundamental tension: the start of a project is when we know the least about requirements, the environment, the team, and what customers will want, yet it is precisely when we must make foundational decisions about design, technology, and approach. His philosophy is to work in a way that optimises for learning, builds in flexibility, and provides fast feedback. If we assume that initial decisions may be wrong, then we need mechanisms to learn quickly what is working and what is not, so we can change course before wasting significant effort.

His top tips for starting a new project are:

**Fast Feedback.** Feedback must come from multiple sources: build systems, automated tests, deployment pipelines, and production metrics. Share test results and metrics data transparently across the team so everyone can see where the project stands and where improvements are needed.

**Optimise for Learning.** Software development is fundamentally about learning. Ask questions, be open about problems, and be honest about what you do not know. Conduct regular retrospectives so the team reviews progress and shares expertise. Draw on previous experience but keep an open mind -- this new project is different, and previous experience may not apply. Make decisions based on evidence, not dogma.

**Set Up the Dev Environment.** Invest in quality tooling for fast feedback. Ensure good network connectivity so developers can collaborate even when geographically dispersed. Automate the development environment setup so new team members can be productive quickly. Agree on team working practices such as pairing, TDD, and coding standards from the outset, then iterate as you learn more.

**Build a Deployment Pipeline.** Get a minimal deployment pipeline in place with the very first feature. Start with a "walking skeleton" -- the simplest feature that exercises the full architecture -- and add tests and infrastructure as you develop. Adopt TDD for commit tests and ATDD for acceptance tests even for this first feature. Automate everything you can, then identify and speed up the slowest components.

**Setting Goals.** Create a team vision: a direction of travel that is aspirational but not detailed. Focus on how the software will make things better for users, without precise targets. Fix either time or scope but never both. Check whether each step moves you closer to or further from the goal.

**Working in Small Steps.** Start small. Identify the simplest feature that is representative of the proposed system and build code, tests, and infrastructure to complete it. Working incrementally means fast feedback, quick reverts, and limited impact from missteps. Abstract unknowns so you can delay working out details until later.

**Get Measures in Place.** Establish the DORA metrics as a minimum: throughput (how efficiently you build and deploy new features) and stability (the quality of output at that throughput). These metrics inform decisions and keep progress on track.

**Be Prepared to Change.** Adopt a defensive approach to design: modular architecture, good separation of concerns. Retain a strong focus on the problem and a loose grip on the current solution. Be willing to discard bad ideas quickly.

### Writing Better User Stories

A user story is a simple description of something a user wants to do. It is a target, not a task. User stories should describe small increments of system behaviour from the user's perspective. They are not "programming by remote control" instructions from outside the development team.

**What Makes a Good User Story:**
- Describes what the user wants, not how the software will work
- Uses natural language a non-technical person would understand
- Eliminates implementation details and anything specific to the system
- Describes a user-visible outcome

Farley provides concrete examples: "Pay by Credit Card" is a good story; "Integrate Component X with Payment Provider Y" is not. "Buy a Book" is good; "Add Buy button to Home Page" is not. The difference is that good stories express user needs while bad stories prescribe technical solutions.

**Who Writes User Stories:** This is best done collaboratively between people with the product vision, domain experts, and developers. Techniques like event-storming and story-mapping help bridge communication gaps. Stories should be accessible to domain experts, operations, business leaders, developers, and QA testers alike.

**Common Mistakes to Avoid:**
1. Defining solutions before exploring the problem
2. Confusing what the system should do with how it does it
3. Writing stories as "remote control" programming instructions
4. Treating stories as contracts that prescribe work
5. Relying too heavily on written communication rather than conversation
6. Creating monster stories that cannot be completed in a sprint
7. Breaking stories into technical task lists that make prioritisation impossible

**Transforming Technical Requirements into User Stories:** Every technical requirement contains user value. "Scale the system to handle more users" becomes "I want results back quickly." "Implement disaster recovery" becomes "I want to carry on placing orders even during an outage." This reframing allows sensible prioritisation by comparing user needs rather than mixing features with technical tasks.

### Organising Software Development Teams

This chapter tackles one of the most consequential questions in software development: how to organise teams for maximum effectiveness.

**Team Size and Structure.** Research consistently shows that small teams (5-9 people) are more efficient and produce better code than large teams. As team size grows, cognitive load, communication complexity, and coordination costs increase exponentially. The challenge is how to scale beyond one or two teams without creating interdependencies that grind progress to a halt.

Farley cites Conway's Law: "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." This means that how you organise teams directly shapes how your code and systems are structured.

**Team Skills and Responsibilities.** The team is the primary unit of work, not the individual. High-performing teams minimise hand-offs between teams. This means each team needs the full range of skills -- development, testing, design, architecture, infrastructure, operability, security, monitoring, and more -- to complete a piece of work independently.

**Team Organisation -- Four Team Types (from Team Topologies):**
- **Stream-Aligned Teams:** The majority of teams, focused on business goals and producing valuable software for users. Aligned with a bounded context in the problem domain.
- **Enabling Teams:** Lend expertise when stream-aligned teams encounter the "difficult 20%" of work. Their dual goal is to implement the feature and teach the stream-aligned team.
- **Complex Subsystem Teams:** Deep experts in narrow fields who handle technically specialised components like hardware interfaces, freeing stream-aligned teams to focus on business value.
- **Platform Teams:** Build tools and infrastructure that make stream-aligned teams more productive. Their goal is to enable independent progress, never to force change on other teams.

**Platform Team Best Practices:** A platform team's goal is to enable stream-aligned teams to deliver with substantial autonomy. Common mistakes include grouping unrelated "leftovers" into a platform and building grand designs that must be complete before anyone can use them. Effective platform teams work incrementally, focus on ease of use from the consumer's perspective, and use loosely coupled API design so changes do not force consumer code changes.

**Transforming Existing Team Structures:** Start by creating an Enabling Team to promote CD practices. Look for ways to reduce coupling between teams. Bring more functions together without making teams bigger. Use temporary expertise lending. Incrementally increase team autonomy and responsibility. Accept extra design costs if they allow teams to work more independently.

### Pair Programming Patterns

Pair programming involves two programmers working together: one as the "Driver" writing code, the other as the "Navigator" reviewing each line and thinking strategically. They switch roles periodically.

**Pair Patterns:**
- **Driver and Navigator:** The standard model. The Driver focuses on code-level concerns; the Navigator focuses on strategic direction.
- **Ping Pong:** Well-suited to TDD. One writes the failing test (Red), the other writes code to pass it (Green), then they refactor together and switch.
- **Strong Style:** Ideal for knowledge transfer. The experienced partner navigates while the novice drives, learning by doing.
- **Parent Child (Anti-Pattern):** The experienced partner gives overly detailed instructions while the novice becomes passive. Limited learning occurs.

**Pair Rotation:** Pairs rotate over time, with one partner staying as the "Anchor" while the other moves on. This ensures continuity while spreading knowledge across the team.

**Benefits of Pair Programming:**
- **Continuous Review:** Code is reviewed as it is written, at the moment when feedback is most valuable. This catches mistakes immediately.
- **Amplified Learning:** Partners explore problems together and learn from each other's knowledge and techniques in both directions.
- **Quality:** Research shows measurable increases in code quality: simpler, more readable, more correct, and more maintainable code.
- **Productivity:** Pairs complete work in about 60% of the time of solo programmers. Better focus, fewer defects, limited WIP, and reduced integration complexity.
- **Innovation:** Pairing is more creative because partners can bounce ideas off each other and take supported risks.
- **Knowledge Distribution:** No part of the code is the sole property of any individual. The team builds shared knowledge, and business resilience increases.
- **Teamwork and Job Satisfaction:** Regular rotation builds trust and respect. Most programmers who try pairing never go back.

**Tips for Successful Pairing:** Adopt pairing as the default. Understand the problem before coding. Let pairs form naturally. Coordinate calendars and workspace setup. For remote pairing, use screen-sharing and video. Rotate every 2-3 days. Take frequent breaks. Overcome reluctance by trying pairing for a few sprints before committing. Different patterns suit different people and projects.

---

## Part 2: Software Testing

### Beginners Guide to TDD (Test Driven Development)

Farley presents TDD as one of the few techniques that helps us design better software faster. The key insight is that creating "testable" code results in code that is more modular, more loosely coupled, has better separation of concerns, better abstraction, and higher cohesion -- these five properties are the general hallmarks of well-designed software. TDD steers us toward better design primarily by forcing us to apply Dependency Inversion so we can inject test-time components.

**The Red-Green-Refactor Cycle:**

1. **Red:** Write a test and see it fail. Focus on designing the external interface of the code. Express what the code should do, not how. Start each test with "should" to maintain behavioural focus. Predict the expected outcome before running. Write from the user's perspective.

2. **Green:** Write the simplest code to make the test pass. Get back to a safe, passing state as quickly as possible. Make the smallest possible changes. Do not try to perfect the design at this stage -- you are in an unstable state.

3. **Refactor:** Rework code and tests to make them clearer, more expressive, and better designed while keeping tests passing. Focus on internal design: improve abstraction, create boundaries, keep different concerns separate. Only refactor when tests are green. Work in small steps, running tests after each change.

Josh Graham's framing is memorable: "Create a tiny universe where the software exists to do one thing, and do it well."

**Top Tips for TDD:** Simulate inputs and use fake dependencies. A high level of test coverage should be a side-benefit, not a goal. Do not chase coverage -- drive code changes from tests and better coverage will follow. Write one test at a time, the simplest test that moves behaviour forward. Automate nearly everything.

**Getting Going with TDD:** Farley recommends Cyber Dojo for practising TDD katas. Dedicate 30 minutes daily for at least two weeks. The goal of a kata is practising the discipline, not solving the problem.

### TDD Top Tips (Advanced Guidance)

**When to Use TDD:** Start any new project with TDD. Write all new code with TDD, even in legacy systems. Start when you understand the problem, not when you know the solution. Always begin with a failing test. Predict the failure mode before running.

**Test Behaviour, Not Implementation:** When writing a test, imagine replacing your entire implementation with something different. If the test is still valid, you have the right focus.

**Design from the Outside In:** Writing the test first means you experience your code's public interface before it exists. This subtle pressure to make code easy to use has a significant positive impact on design quality.

**The Three Mindsets of TDD:**
- **Red mindset:** External design focus. Make the public interface easy to express and use.
- **Green mindset:** Tactical. Get to safety quickly. Write naive code. This is not a design step.
- **Refactor mindset:** Internal design focus. Improve implementation quality under the protection of passing tests. Quality of code is measured by ease of change.

**Listen to Your Tests:** If a test is hard to write, the design is too complex. Complex tests equal poor design. Do not fix this in the test -- change the design to make it simpler to test.

**Testing at the Edges:** Code that touches I/O boundaries (UIs, storage, network) is inherently harder to test. Minimise this code. Use abstraction to hide I/O details. A call like `storeAccount(Account account)` is better than embedding SQL statements in business logic. Pick simple, generic cases for edge tests. Unit test individual pieces; use integration tests to validate interactions.

### Acceptance Test Driven Development (ATDD)

In Continuous Delivery, acceptance tests are business-facing and support programming. They evaluate the system from an external user's perspective, in life-like scenarios, in production-like environments, through public interfaces. They determine the releasability of the system.

Creating an acceptance test before writing any code makes it an executable specification. Combined with TDD, this approach can reduce defects by two orders of magnitude.

**Properties of Effective Acceptance Tests:**
- Written from the perspective of an external user
- Evaluated in production-like environments
- Interact through public interfaces only
- Focus on what the system does, not how

**The Four Layer Separation of Concerns:**

1. **Test Cases:** Written in the language of the problem domain. Should be readable by the least technical person who understands the domain.
2. **Domain Specific Language (DSL):** Shared between test cases. Designed to make writing test cases easy. Uses optional parameters with default values for flexibility.
3. **Protocol Drivers:** Translators from DSL to the language of the system. Isolate all test infrastructure knowledge of the system here.
4. **System Under Test (SUT):** Deployed using the same tools and configuration as production. Must be production-like from the SUT's perspective.

**Growing the DSL:** Start with two or three test cases exercising the most common behaviour. Build the infrastructure to make them pass. Adopt the discipline of creating a new acceptance test for every acceptance criterion of every user story. Anyone can write test cases, but developers own the tests and the plumbing.

### What to Test, and When?

Farley provides a testing strategy framework with four stages:

**Commit Stage (Fail Fast):** Unit tests, coding standards checks, common error detection, static analysis, and data migration unit tests. Aim for sub-5-minute feedback.

**Acceptance Stage (Define Releasable):** Acceptance tests (BDD-style executable specifications), deployment tests, configuration tests, security tests, performance tests, scalability tests, resilience tests, and compliance tests.

**Release Stage (Support Release):** Smoke tests/health checks, canary release testing, monitoring, and exception tracking.

**Production Stage (Inform Product Design):** Capacity monitoring, technical monitoring, performance verification, security verification, A/B testing, business experiments, and commercial performance metrics.

### Testing in Production

Testing in production closes the feedback loop on things that can only be learned when real users interact with the system. It is not an excuse to avoid testing during development or permission to release inadequately tested software. It works best alongside a comprehensive deployment pipeline with effective TDD and ATDD.

**Types of Production Testing:**
- **Smoke Tests/Health Checks:** Validate the environment is correctly configured immediately after release.
- **Canary Releases:** Deploy to low-risk environments first, progressively deploying to higher-risk ones with pass/fail criteria.
- **A/B Tests:** Deploy two versions, monitor both, and compare impact on customers and business.
- **Configuration Testing:** Verify all software works together, ideally detectable by automated systems.
- **Monitoring and Observability as Tests:** Set thresholds for success on technical and business metrics.

**Business (Pirate) Metrics -- AARRR:** Acquisition, Activation, Retention, Revenue, Referral. Track these and measure the impact of changes experimentally.

**Why Not End-to-End Testing:** E2E testing is a common but problematic approach where teams deploy to a staging environment and evaluate all changes together. It is slow, complex, and less thorough. As the amount of change increases, interactions and risk grow exponentially. Farley argues strongly against this pattern.

### Eliminating Intermittent Tests

Intermittent tests undermine trust in automated testing. The solution is to address root causes:

- **Control the Test Environment:** Version control everything -- code, tests, environment configurations, and infrastructure.
- **Isolate Test Data:** Use atomic test data. Share no writable data between tests. Generate unique identifiers. This is called Functional Isolation.
- **Implement Continuous Integration:** Run tests after every commit. Get immediate feedback. Address failures immediately.
- **Handle Concurrency and Race Conditions:** Use synchronisation techniques. Wait for conditions that show completion before proceeding. Hide concurrency from test cases. Never rely on timing.
- **Test in Isolation:** Test individual components or services in isolation. The narrower the scope, the easier to control variables.
- **Treat Tests as Falsification Mechanisms:** Passing tests do not guarantee correctness, but failing tests indicate definite issues. Never rerun intermittent tests and trust the pass. Treat intermittency as failure and investigate root causes.

### Behaviour Driven Development (BDD)

BDD is a refinement of TDD that shifts focus from testing code to verifying system behaviour. It addresses common TDD misunderstandings where adopters focused on code coverage rather than design. BDD emphasises specifications over tests, scenarios over implementation details.

**Core Principles:**
- Focus on behaviour, not testing. Start specification descriptions with "should."
- Establish a ubiquitous language shared across all stakeholders.
- Use Given-When-Then format: Given the system state, When an action occurs, Then the expected outcome.
- Separate WHAT from HOW. Specifications should say nothing about implementation.

Farley provides a powerful example comparing two tests for buying a book on Amazon. The first test is tightly coupled to UI elements (finding elements by ID, XPath queries for specific DOM structures). It is unreadable to non-developers, fragile to any UI change, and won't work against a mobile app. The second, equivalent test uses domain language: `shopping.searchForBook()`, `shopping.selectBook()`, `shopping.addSelectedItemToShoppingBasket()`, `shopping.assertItemListedInShoppingBasket()`. This version is instantly readable, hides implementation detail, has separation of concerns, encourages code reuse, significantly reduces maintenance, and always represents an accurate specification even when failing.

**The Process of Translation:** BDD guides development from vague ideas to working software through: broad user needs, refinement into smaller steps, user stories, concrete examples, acceptance criteria, executable specifications, and outcome focus.

**Common Pitfalls:** Overfocusing on tooling (Cucumber is an aid, not the essence). Including technical jargon in scenarios. Neglecting the refinement process. Ignoring feedback. Treating BDD as just a testing methodology. Over-specifying. Including implementation details. Working in isolation.

### Testing Software Performance

Performance testing determines whether systems perform as expected under workload. It identifies bottlenecks and ensures responsiveness and efficiency under high load.

**Basic Concepts:**
- **Throughput:** Rate of processing -- transactions per timeframe. Maximum throughput is bandwidth.
- **Latency:** Time delay between initiating an action and observing its result.
- **Responsiveness:** Users prefer consistent quick responses. Best achieved with high throughput and low latency.

**Key Principle -- Control the Variables:** Use dedicated test environments mirroring production. Adopt infrastructure-as-code. Isolate the testing network. Use pass/fail criteria with clear thresholds.

**Component vs. Whole System Testing:** Component tests isolate performance-critical parts, reduce complexity, and enhance repeatability. They are good at finding expected problems. Whole system tests identify unexpected issues but require more complex setup. Controlling variables in whole system tests is much more challenging.

**Usability Benchmarks:** Excellent responsiveness is 0-150ms, good is up to 300ms, poor is 300-450ms, and unacceptable is above 450ms.

**Test-First Performance Testing:** Write tests against stubs before testing actual code. This ensures tests are capable of measuring at the desired rate before the real code exists.

---

## Part 3: Continuous Delivery Practices

### How to Build a Deployment Pipeline

The deployment pipeline is a machine that organises software development from commit to releasable outcome. It includes all steps required for software to be releasable: unit tests, acceptance tests, validation, integration, version control, sign-offs, and any other requirements. When code completes transit through the pipeline, the software can be safely released.

**What the Deployment Pipeline Is NOT:** It is not only an automated build/test/deploy workflow. It is not separate pipelines for build, test, and deployment. It is not just tools and processes. It is not for proving software is good. It is a falsification mechanism, a platform for testing ideas safely, and a measurement system that produces data for evidence-based decisions.

**Key Components:**
- **Commit Stage:** Fast (under 5 minutes), lightweight technical tests giving developers high confidence.
- **Artifact Repository:** Successful commit output is a Release Candidate, version-controlled and stored.
- **Acceptance Test Stage:** User-centred testing in life-like scenarios and production-like environments.
- **Ability to Deploy into Production:** A Release Candidate that passes all stages is ready to deploy.

**Building the Pipeline Step by Step:**
1. Start with a "Walking Skeleton" -- the simplest end-to-end feature exercising the full architecture.
2. Set up version control, keeping everything in one repository initially.
3. Create a Commit Stage: pick a build management system, configure testing tools, establish naming conventions.
4. Create an Artifact Repository: decide on packaging, generate unique IDs for Release Candidates.
5. Create an Acceptance Stage: write acceptance tests, automate deployment, automate environment configuration, set up polling for new Release Candidates.
6. Create a simple version of production: decide on release approach (manual or automated).

**Team Behaviours:** Developers wait and watch for commit test results (about 5 minutes). If tests fail, the committer fixes them immediately. If a team-mate does not stick around to fix failures, the team reverts the change. The team prioritises finding and fixing failures quickly to keep software releasable.

**Key Principles:**
- **Automation:** Automate everything for repeatability, reliability, and efficiency. Manual testing is costly and low-quality for regression, though useful for exploratory testing.
- **Efficiency:** Goal is commit-to-releasable several times per day. Include only essential steps. Do each step only once.
- **Continuous Integration:** First stage of the pipeline. Only one interesting version -- the current one. Commit at least once per day.
- **TDD:** Makes development more efficient overall. Builds quality in by testing throughout the process.
- **Version Control:** Apply to everything -- code, dependencies, configuration, infrastructure.

### Continuous Integration Top Tips

CI is the antidote to "Integration Hell." It is an Extreme Programming discipline that minimises code ownership conflicts by ensuring correct changes are available to everyone almost instantly. There is only one interesting version of the system -- the current one.

CI means little or no branching. Changes go to trunk/master as small, continuously evaluated changes. Any branches must be tiny and short-lived (no more than a day). DORA research found that merging frequently is a reliable predictor of higher throughput and stability.

Farley's 10 CI Tips:
1. Work in small steps: commit and test small changes, not whole features.
2. Run commit tests locally first.
3. Aim to commit every 10-15 minutes with feedback in under 5 minutes. Wait for results.
4. Monitor your changes through all evaluations -- unit tests, acceptance tests, and beyond.
5. Fix any failure in under 10 minutes, or revert and work offline.
6. Revert team-mates' changes if they do not stick around to fix failures.
7. As a team, prioritise fixing failures quickly.
8. Gamify "Build Sins" with silly hats, swear jars, and instant alert systems.
9. Adopt TDD.
10. Build and use a Continuous Delivery deployment pipeline.

### Assess Your CD Capability

Farley provides a self-assessment based on the 13 predictors of Continuous Delivery from the State of DevOps report. Score each practice from 0 to 5:

1. **Test Automation:** Can you release without manual regression testing?
2. **Deployment Automation:** Single-button deployment to test or production?
3. **Trunk-Based Development:** Merge to trunk at least daily?
4. **Shift Left on Security:** Security testing in the deployment pipeline?
5. **Loosely Coupled Architecture:** Can you change one part without testing the whole system?
6. **Empowered Teams:** Can teams change technology/design without external permission?
7. **Continuous Integration:** Commit small changes safely multiple times per day?
8. **Version Control:** Deploy a working version from any point in history?
9. **Continuous Testing:** All tests run automatically on commit to achieve a releasable outcome?
10. **Test Data Management:** Automated tests isolated and self-contained?
11. **Test Consistency:** Consistent results from parallel, repeated test runs?
12. **Monitoring and Observability:** Detect problems without waiting for user complaints?
13. **Proactive Notifications:** System actively informs of problems before you notice?
14. **Database Change Management:** Data and schema changes included in CD practice?

For improvement, Farley recommends the Toyota Improvement Kata model: Where are you now? What is your objective? What is your next step? How will you know if you have succeeded?

### Refactoring Legacy Code

Legacy code is a combination of outdated, complex, poorly structured, and difficult-to-understand code. Quality in code is defined by one thing: our ability to change it. Legacy code is a problem because it is hard to change. Refactoring is always behaviour-preserving -- if it changes behaviour, it is not refactoring.

**The 5 Steps in Refactoring to Testability:**

**Step 1 -- Approval Testing.** "Legacy code is code without tests" (Michael Feathers). Approval tests (also called Characterisation Tests) capture current behaviour and assert it. They act as safeguards against unintentional changes. Run once to capture output, then compare subsequent runs to detect unintended modifications.

**Step 2 -- Remove Clutter.** Delete dead code, superfluous comments, redundant code, and remnants of unused functionality. Version control means there is no reason to keep dead code. Removing clutter immediately improves structure and readability.

**Step 3 -- Reduce Complexity.** Reduce cyclomatic complexity by extracting methods for code blocks in loops and conditionals. Name extracted methods descriptively. Eliminate break and continue clauses. Aim for each method to have a single exit or return point.

**Step 4 -- Compose Methods.** Continue extracting methods to name blocks of code. Pick meaningful names and arrange them to "tell the story of the function." Group related code, separate unrelated code, and iterate. Use modern IDEs to automate refactoring tasks.

**Step 5 -- Refactor to Testability.** Restructure code to make it easier to test. Simplify and clarify dependencies through improved modularity and separation of concerns. Move unrelated code further apart (increase modularity) and related code closer together (improve cohesion).

---

## Part 4: Architecture and Design

### Evolve Your Software Architecture

Software architecture represents the guide-rails that help make design choices consistent with system goals. Farley challenges the notion that architecture must be "got right from the start." When we begin a project, we cannot be sure of our answers, and things will change unpredictably. Architecture is a living thing that evolves as understanding deepens.

**Core Principles:**
- Work in ways that keep things easy to change.
- Work in small steps to evaluate fitness based on present understanding.
- Adopt an evolutionary approach: assume mistakes, learn, and adapt.
- View architecture as a snapshot of current understanding, not a permanent blueprint.

**Evolutionary Architecture Techniques:**
- **Separate Concerns and Emphasise Modularity:** Divide into distinct modules. Use interfaces and abstraction for interactions. Avoid tight coupling.
- **Prioritise Testability:** Design for testability encourages modularity, cohesion, separation of concerns, abstraction, and reduced coupling.
- **Understand and Adapt to Context:** No one-size-fits-all architecture. The best approach depends on specific requirements and constraints.
- **Assume Change and Uncertainty:** Create a simple "tourist map" whiteboard model that anyone can reproduce from memory. Design for flexibility.
- **Avoid Big Upfront Design:** Start with a broad design and refine incrementally based on feedback.
- **Engage in Continuous Learning:** Regularly evaluate architecture against new knowledge and best practices. Never consider it "finished."

Automated tests embody architectural constraints: "Is it fast enough? Secure enough? Resilient enough?" These verifiable constraints become part of the continuously evolving specification of the system.

### Write Code You Can Change Easily

The central thesis: high-quality code is code that you can change easily. This is measured by the ease of change, not by cleverness or complexity.

**Prioritise Code Readability:** Express intent clearly. Use meaningful names. Write small, focused functions. Avoid complex comments -- make code self-explanatory. Use comments to explain why decisions were made, not what code does.

**Practise TDD:** Writing tests before code ensures reliability and incremental design. Start with a failing test, make it pass, then refactor.

**Manage Complexity by Design:**
- **Modularity:** Divide into smaller pieces. Change internal workings of one module without affecting another.
- **Cohesion:** Related concepts close together, unrelated concepts far apart.
- **Separation of Concerns:** Each part focused on one thing, doing it well.
- **Abstraction:** Hide information behind abstractions so code can be used without knowing how it works.
- **Coupling:** Prefer looser coupling. Prevent change in one place from leaking out.

**Effective Refactoring Techniques:** A four-step approach: approval test to stabilise, remove clutter, reduce complexity, compose methods. Each step builds on the previous, progressively improving code quality and changeability.

**Automated Testing and Continuous Integration:** Write unit tests as mini-specifications. Set up CI to run tests automatically on every commit for quick feedback.

### Microservices Architecture

Microservices combine a distributed systems architecture with a distributed development architecture. Services are small (rewritable in 1-2 weeks), focused on one task, and independently deployable. The approach is the most scalable way to grow large development teams.

**Bounded Contexts:** The easiest way to create autonomous, independently deployable services is to align each with a bounded context -- an area of the problem where ideas have consistent meaning. For example, "book" means different things in a "find books" context versus a "ship books" context. Bounded contexts are naturally decoupled, making them excellent service boundaries.

**Design Guidance:**
- Begin with a single repository. Create first-best-guess designs, then iterate.
- Use event-storming for creative exploration.
- Create separate repositories only as design abstractions stabilise.
- Initially test in a single deployment pipeline shared between teams.

**Messaging:** When services communicate, reduce coupling by keeping messages distinct from internal implementation. Treat messages as a separate bounded context. Use the Ports and Adapters pattern. Translate when transitioning between bounded contexts. Avoid technically-focused messages -- model conversations at the problem-domain level. Consider contract testing to check for breaking changes.

---

## Part 5: Get Into Good Habits

### Adopt Great Developer Habits

Great programmers are regular programmers with great habits. The best way to develop them is to enjoy the process.

**Code as Communication:** The target of our code is other people, not computers. Write code that is easy to read, understand, and learn from. Pick clear descriptive names. Keep functions small (5-10 lines). Write code anyone could understand in seconds.

**Think Like an Engineer:** In engineering, we start by assuming we are probably wrong. Question assumptions. Demand evidence. Try alternatives. Build reasoned explanations. Experiment using small tests. Ask "What would show that this idea is wrong?"

**Be Cautious of Frameworks:** Frameworks can impose their structure on your code, potentially locking you in. Isolate third-party code behind your own abstractions. "Ask not what you can do for your framework, ask what your framework can do for you."

**Coding Is Design:** Focus on the information being dealt with and how it is exchanged. Manage complexity. Low complexity equals good design. Good design is measured by ease of change.

**Quality Over Features:** There is no trade-off between speed and quality. Focusing only on features at the expense of quality is slower, not faster. Write software that is easy to change and keep it that way indefinitely. If you see an opportunity to improve code, take it.

**Social Activity:** Great developers are great communicators. Software development is a team activity. Pair programming improves communication skills. If struggling with a problem, explain it to someone else -- you will often solve it before finishing the explanation.

**Work in Small Steps:** The best programmers make progress in small steps, checking each step as they go. This optimises for faster, higher-quality feedback. These practices work across all types of software, from Google's monorepo to financial exchanges to military systems.

### Avoid Common Software Development Pitfalls

**1. It's Not Just the Happy Path:** Avoid magical thinking. High-quality systems are resilient when things go wrong. Think defensively. Consider negative scenarios: unexpected inputs, disk full, missing files, exceptions from libraries, concurrency issues, security breaches, runaway processes. Think through risks even if you decide to defer dealing with them.

**2. Don't Fall for Code Ownership:** Avoid treating code as "yours." Shared code ownership is stronger. Break one-person silos through pair programming or rotation.

**3. It's Not My Problem:** Your goal is impact on users. It is not someone else's job to tell you what code to write, keep the codebase tidy, or grant permission to test or refactor. Take responsibility. Take pride in your work.

**4. Don't Be Afraid to Change the Code:** If you are scared to change code, that is a problem. Work on the assumption that code is a "best guess" that is probably wrong. Defend and maintain your freedom to change code. Use refactoring and effective tests. Great code is code you can change safely and easily.

**5. Focus on Outcomes Rather Than Tools:** What matters is getting good software to users quickly and efficiently. Understand and solve the problem first.

**6. Myth Busting:** Farley addresses six persistent myths:

- *"You can't do serious work without feature branching."* -- CI is better. Google, Amazon, and Facebook all use CI, not feature branching.
- *"My manager says I don't have time."* -- There is no trade-off between speed and quality. CD teams spend 44% more time on new features (DORA reports).
- *"Writing tests is a waste of time."* -- Tests save time. The question is only what is the most efficient way to test.
- *"You can't do code reviews with CI."* -- You can, but pair programming is more effective than stale pull requests.
- *"These ideas don't work for my system."* -- Google, Volvo, Tesla, SpaceX, the US Air Force, NYSE, and Citibank all use these techniques.
- *"We've always done it this way."* -- Even if you sit still, no one else will.

---

## Key Takeaways

1. **Work in Small Steps.** This is the foundational idea. Small steps enable faster learning, quicker feedback, easier recovery from mistakes, and more confident progress. This applies universally: writing code, testing, deploying, designing systems, managing teams, and managing projects.

2. **There Is No Trade-Off Between Speed and Quality.** The only way to deliver features more quickly is to build higher-quality software. DORA research shows CD teams spend 44% more time on new features than non-CD teams. Cutting corners on quality is always slower in the long run.

3. **Test-Driven Development Is About Design, Not Testing.** TDD steers toward better design because testable code exhibits modularity, loose coupling, separation of concerns, good abstraction, and high cohesion -- the hallmarks of well-designed software.

4. **Automate Everything You Can.** The deployment pipeline automates all steps from commit to releasable outcome. This produces repeatability, reliability, fast feedback, auditable records, and freedom from human error.

5. **Separate What from How.** Whether writing user stories, acceptance tests, or BDD specifications, focus exclusively on what the system does from the user's perspective. Never include implementation details. This makes specifications more durable, reusable, and maintainable.

6. **Architecture Evolves.** Do not attempt big upfront design. Start with a simple, broad design and refine it incrementally based on feedback and learning. Architecture is a snapshot of current understanding, not a permanent blueprint.

7. **High-Quality Code Is Easy to Change.** Quality is measured by ease of change. Achieve this through modularity, cohesion, separation of concerns, abstraction, and loose coupling. Maintain the freedom to change code at all times.

8. **Teams Are the Primary Unit of Work.** Small, multi-skilled teams (5-9 people) with all the capabilities needed to complete work independently are the most effective. Minimise dependencies between teams through loose coupling, bounded contexts, and well-designed APIs.

9. **Control the Variables.** Whether running performance tests, managing test environments, or making production changes, controlling variables is essential for meaningful results. Version control everything: code, tests, configuration, and infrastructure.

10. **Think Like an Engineer.** Start by assuming you are wrong. Question assumptions, demand evidence, try alternatives, build reasoned explanations, and experiment. Not all ideas have equal merit -- discard those that do not measure up.

11. **Pair Programming Multiplies Effectiveness.** It provides continuous code review, amplifies learning, improves quality and productivity, distributes knowledge, fosters innovation, and builds team cohesion. Most developers who try it never go back.

12. **Continuous Integration Is Non-Negotiable.** Commit to trunk at least daily (ideally much more often). Small changes, fast feedback, and immediate fixing of failures keep software always in a releasable state. Feature branching is incompatible with true CI unless branches last less than a day.

13. **Feedback Is the Engine of Improvement.** Fast, accurate feedback from automated tests, deployment pipelines, production monitoring, and team retrospectives drives continuous improvement. Close the feedback loop at every level.

14. **Refactoring Is a Daily Practice.** Great programmers refactor continuously, leaving code in a slightly better state after every small change. For legacy systems, use the five-step approach: approval testing, remove clutter, reduce complexity, compose methods, refactor to testability.

15. **Communication Is a Core Technical Skill.** Code is communication with other people. User stories are conversation placeholders. Pair programming teaches communication. Software development is a social, collaborative activity that thrives on clear, interactive communication -- never rely solely on written documents.
