# Modern Software Engineering: Doing What Works to Build Better Software Faster

**Author:** David Farley
**Summary of core arguments, concepts, and patterns**

---

## Overview and Core Thesis

David Farley's *Modern Software Engineering* argues that software development has fundamentally misapplied the term "engineering" for decades. Instead of the bureaucratic, plan-driven processes most organizations call "software engineering," Farley proposes a definition rooted in the actual practice of engineering across other disciplines: the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems.

The book's central claim is that software development is an exercise in **discovery and learning**, not production. Because digital assets have essentially zero cost of production (unlike physical goods), our discipline is solely one of **design engineering**, not production engineering. This single insight reframes how we should think about every aspect of building software.

Farley organizes his thinking around two fundamental capabilities that software engineers must master:

1. **Optimizing for Learning** -- becoming experts at learning through iteration, feedback, incrementalism, empiricism, and experimentation.
2. **Optimizing for Managing Complexity** -- becoming experts at managing complexity through modularity, cohesion, separation of concerns, abstraction, and loose coupling.

These ten ideas, supported by practical tools like testability, deployability, speed, controlling the variables, and continuous delivery, form what Farley argues are the genuine foundations of an engineering discipline for software.

---

## Part I: What Is Software Engineering?

### Chapter 1 -- Introduction

Farley opens by grounding software engineering in the scientific method. The scientific method, as most people learn it, consists of four steps:

- **Characterize**: Make an observation of the current state.
- **Hypothesize**: Create a description, a theory that may explain your observation.
- **Predict**: Make a prediction based on your hypothesis.
- **Experiment**: Test your prediction.

When software developers organize their thinking around many small, informal experiments, they limit the risk of jumping to inappropriate conclusions and end up producing better work. Thinking in terms of controlling variables leads to more deterministic systems. Thinking in terms of falsification helps eliminate bad ideas quickly.

Farley offers his working definition of software engineering:

> **Software engineering** is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software.

The adoption of this approach matters for two reasons. First, software development is always an exercise in discovery and learning. Second, if the aim is to be efficient and economic, then the ability to learn must be **sustainable** -- meaning we must manage the complexity of the systems we create so that we can continue to learn and adapt indefinitely.

The book traces the birth of the term "software engineering" to Margaret Hamilton, who led the development of the Apollo flight-control software at MIT in the 1960s. Around the same time, NATO convened a conference in Garmisch-Partenkirchen, Germany -- the first software engineering conference -- in response to what was called the "software crisis," a perceived gap between hardware progress and software progress. Fred Brooks later observed in his famous 1986 paper "No Silver Bullet" that there was no single development that promised even a 10x improvement in productivity, reliability, or simplicity. Farley notes that Brooks' observation remains true decades later, but argues that the anomaly is not that software progress is slow, but that hardware progress has been staggeringly, unprecedentedly fast.

Farley invokes Thomas Kuhn's concept of **paradigm shift** to argue that treating software development as a genuine engineering discipline -- rooted in scientific rationalism -- represents such a shift. It requires discarding old ideas (like waterfall planning) that this approach supersedes.

### Chapter 2 -- What Is Engineering?

This chapter dismantles the common confusion between production engineering and design engineering.

**Production Is Not Our Problem.** For most human endeavors, production of physical things is the hard part. Designing a car is difficult, but taking that design into mass production is immensely more expensive and complicated. In software, production consists of triggering the build. It is automatic, push-button, and essentially free. "Production is not our problem." This makes software unusual and subject to easy misunderstanding, because people reflexively apply production-style thinking (like waterfall processes) to what is fundamentally a design and learning activity.

**Design Engineering, Not Production Engineering.** Even in physical engineering, building the *first* of a new kind of bridge involves two problems: the production problem (irrelevant to software) and the design problem. Physical engineers adopt modeling and simulation techniques because they cannot iterate quickly on real physical artifacts. Software developers have an enormous advantage: the models we create (our code) ARE the product. We do not need to worry about whether our simulation matches reality; our simulation IS the reality of our system.

Farley traces the history of formal methods in the 1980s and 1990s -- the attempt to mathematically prove code correct. While appealing, formal methods never gained widespread adoption because they make code harder to produce, not easier, and because the "provability" quickly becomes impractical for any system involving concurrency, real-world interaction, or complex domains. He compares this to aerospace engineering: if math alone were enough to design an airplane, companies would skip building prototypes. They do not. They use math extensively, then test real devices. SpaceX, even with detailed mathematical models of tensile strength, still builds experimental prototypes and pressurizes them to destruction.

Glenn Vanderburg's insight is quoted: in other disciplines, "engineering means stuff that works," but in software, almost the opposite has become true. If our practices do not allow us to build better software faster, they are not engineering.

**A Working Definition of Engineering.** Farley proposes:

> Engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems.

All the words matter. Engineering is applied science. It is practical, using empirical means to learn and advance. Solutions are practical and applicable. They are efficient and constrained by economics.

**Engineering != Code.** Engineering is not just the output (the code) or even its design. It is the entire process, tools, techniques, philosophy, and approach. When Farley talks about engineering, he means everything that it takes to make software -- process, tools, and culture.

**The Limits of Craft.** Craft-based production is fundamentally low-quality compared to machine-based production. A human being, however talented, is extraordinarily accurate at 1/10 of a millimeter; machines can manipulate individual atoms. In software, a modern computer processes roughly 3 billion operations per second. In the minimum time a human can perceive any change (about 13 milliseconds), a computer executes 39 million instructions. If we limit quality to human-scale perception, we are sampling at a rate of 1 to 39 million. This gap highlights two aspects of engineering: **precision** and **scalability**.

Engineering approaches are not limited by individual human capability the way craft is. Engineering allows us to build on the work of others, accumulate knowledge, and create increasingly complex systems. The transition from craft to engineering in software requires adopting repeatable, measurable practices that scale beyond individual capability.

**Trade-Offs.** Engineering is about making informed trade-offs. There is no perfect solution; there are only better and worse solutions given the constraints. This is a deeply pragmatic view. The journey from craft to engineering is about replacing intuition with evidence where possible, while still recognizing the role of creativity and judgment.

### Chapter 3 -- Fundamentals of an Engineering Approach

This chapter lays the groundwork for the rest of the book by introducing the importance of measurement and the two pillars of the engineering approach.

**The Importance of Measurement.** If engineering is the application of scientific thinking, then measurement is essential. Farley cites the DORA (DevOps Research and Assessment) metrics as the best available measures of software development performance:

- **Stability** -- the quality of the software produced (measured by things like change failure rate and time to restore service).
- **Throughput** -- the efficiency of the development process (measured by deployment frequency and lead time for changes).

Critically, research shows these measures are not in tension. Teams that optimize for throughput also achieve better stability. This contradicts the common assumption that moving faster means sacrificing quality.

**The Foundations of a Software Engineering Discipline.** Farley distills the foundations into two groups:

*Experts at Learning:*
1. Iteration
2. Feedback
3. Incrementalism
4. Experimentation
5. Empiricism

*Experts at Managing Complexity:*
1. Modularity
2. Cohesion
3. Separation of Concerns
4. Abstraction
5. Loose Coupling

These are not new ideas. The power comes from organizing them into a coherent, intellectually consistent framework and applying them deliberately as the guiding principles of software development.

---

## Part II: Optimize for Learning

### Chapter 4 -- Working Iteratively

Iteration is the most fundamental of the learning techniques. Farley defines iteration as repeating a process to approach a desired result, where each cycle builds on the learning from the previous one. The Merriam-Webster dictionary defines iteration as "a procedure in which repetition of a sequence of operations yields results successively closer to a desired result."

**Practical Advantages of Working Iteratively.** Iteration reduces risk. Instead of planning everything upfront and executing a grand plan, iterative work allows teams to discover requirements, validate assumptions, and correct course frequently. This is a **defensive design strategy** -- it protects against the inevitable inaccuracies in our plans and predictions. Farley draws on Fred Brooks' advice from *The Mythical Man-Month*, where Brooks recommended building a system to throw away, because you will anyway. Iteration makes this practical rather than wasteful by making each attempt cheap and informative.

**Iteration as a Defensive Design Strategy.** Working iteratively is a defense against uncertainty. If we knew exactly what we needed to build and how to build it, a plan-driven approach might work. But we never do -- not because we are incompetent, but because the problems we solve are genuinely complex and the requirements genuinely emergent. Iteration allows us to discover what we need to build as we build it. Each cycle teaches us something, and each lesson is incorporated into the next cycle.

**The Lure of the Plan.** Farley is sharply critical of the waterfall mindset that assumes "if we only think/work hard enough, we can get things right at the beginning." This is a production-engineering mindset applied to a design-engineering problem. Software development is exploration; plans are guesses that need to be validated. Waterfall processes are production lines for software -- they are the tools of mass production, not the tools of discovery, learning, and experimentation.

Agile thinking took a step in the right direction by recognizing software development as a learning exercise rather than a production problem. However, Farley argues that many organizations practice "faux agile" -- adopting agile ceremonies while maintaining waterfall thinking at the organizational level. Most organizations are still, at heart, dominated by waterfall thinking at the organizational level, if not also at the technical level. The phrase that best captures genuine agile thinking is "inspect and adapt."

This shift in perception is significant because it represents a step toward perceiving software development as a learning exercise. Waterfall, when applied to software development, is so inefficient that improving it by an order of magnitude is perfectly possible. Waterfall-style thinking starts from the assumption that "if we only think/work hard enough, we can get things right at the beginning." Iterative thinking starts from the assumption that we will learn our way to the right solution.

**Practicalities of Working Iteratively.** To work iteratively effectively, teams need:
- Short cycles with clear goals
- The ability to measure progress against those goals
- The willingness to change direction based on what is learned
- Technical practices that support rapid change (continuous integration, automated testing, etc.)

Farley emphasizes that the cycle time of iteration matters. Shorter cycles provide more frequent learning opportunities. The cost of each cycle should be low enough that we can afford many of them, and the feedback from each cycle should be clear enough to inform the next one.

### Chapter 5 -- Feedback

Feedback is the mechanism through which we learn from our iterations. Without feedback, iteration is just repetition.

**A Practical Example.** Farley describes how feedback works at multiple levels in software development:

- **Feedback in Coding**: The fastest feedback loop is the development environment itself -- syntax highlighting, type checking, compilation errors. Test-driven development (TDD) creates a tight feedback loop where each small change is validated by automated tests. This is feedback at the scale of seconds.
- **Feedback in Integration**: Continuous integration provides feedback on whether changes work correctly when combined with the rest of the system. This operates at the scale of minutes.
- **Feedback in Design**: Code reviews, pair programming, and design discussions provide feedback on the quality of design decisions.
- **Feedback in Architecture**: Monitoring, alerting, and production metrics provide feedback on whether architectural decisions are working in practice.
- **Feedback in Product Design**: User testing, A/B testing, and usage analytics tell us whether we are building the right thing.
- **Feedback in Organization and Culture**: Team retrospectives, organizational metrics, and employee satisfaction surveys provide feedback on the health of the development process itself.

**Prefer Early Feedback.** In all cases, earlier feedback is more valuable than later feedback. A bug caught by the compiler is cheaper to fix than one caught by a unit test, which is cheaper than one caught in code review, which is cheaper than one caught in production. Farley describes a hierarchy of feedback loops, from the fastest (IDE feedback, milliseconds) to the slowest (production incidents, days or weeks), and argues that we should optimize for the fastest, most definitive feedback at each level.

When Farley is coding, he can use development tools to highlight errors as he types -- the fastest, cheapest feedback loop. He can run tests in the area of code he is working on and get feedback in seconds. His automated unit tests, created through TDD, give a second level of feedback when run locally. Continuous integration provides the next layer, running the full test suite in a clean environment. Acceptance tests verify that the system meets its requirements. Performance tests check non-functional characteristics. Finally, production monitoring tells us whether the system is behaving correctly in the real world. Each layer provides progressively broader but slower and more expensive feedback.

The adoption of continuous delivery promotes more modular, better-abstracted, more loosely coupled designs because only then can you deploy and test efficiently enough to practice continuous delivery. This is a profound idea: focusing on the efficient delivery of high-quality feedback naturally leads to better software architecture. By focusing process, technology, practice, and culture on the efficient delivery of high-quality feedback, we can create better-quality software and do that with greater efficiency.

**Feedback in Product Design and Organization.** Farley extends the concept beyond code. In product design, user research, A/B testing, and usage analytics provide feedback on whether we are building the right thing. In organizations, retrospectives, team surveys, and performance metrics tell us whether our processes and structures are working. The same principle applies everywhere: seek the fastest, most definitive feedback possible, and use it to guide decisions.

### Chapter 6 -- Incrementalism

Incrementalism is the practice of making progress through many small, safe steps rather than large, risky leaps. It is closely related to iteration but focuses specifically on the size and safety of each step forward.

**Importance of Modularity.** Incrementalism depends on modularity. If a system is a monolithic, tightly coupled mass, then any change potentially affects everything, making small safe steps difficult or impossible. Modularity allows us to isolate changes and their effects. This creates a virtuous cycle: incrementalism demands modularity, and modularity enables incrementalism.

Farley distinguishes between incremental development (building the system piece by piece, where each piece adds working functionality) and iterative development (repeating a process to refine a result). Both are important, but incrementalism specifically focuses on ensuring that each step adds real, working value to the system.

**Organizational Incrementalism.** Farley extends the concept beyond code. Organizations should also work incrementally -- making small changes to team structures, processes, and strategies rather than attempting large reorganizations. This is consistent with the idea that organizations are information systems too, and the principles of managing complexity apply to them. Organizational changes are most effective when they are small, measurable, and reversible.

**Tools of Incrementalism.** Three primary technical tools support incrementalism:

1. **Version control** -- allows us to track, revert, and manage changes precisely.
2. **Automated testing** -- provides a safety net that allows us to make changes with confidence.
3. **Continuous integration** -- ensures that changes are validated frequently in the context of the whole system.

Automated testing has a particularly important side effect: it drives better design. Test-driven development demands that we create mini executable specifications for each change. To keep tests simple, we must design code to be testable, which means designing it to be modular with good separation of concerns. This creates a positive feedback loop that enhances design quality.

**Limiting the Impact of Change.** The aim is to manage complexity so that we can develop systems incrementally. We prefer to make progress in many small steps rather than a few larger, riskier ones. Each step should be small enough that if something goes wrong, we can understand and fix the problem quickly.

**Incremental Design.** Farley argues against "big design up front." Instead, design should evolve incrementally alongside the code. This does not mean no design; it means designing at the last responsible moment, when we have the most information. The design should emerge from the iterative, incremental process of building the system, guided by feedback.

### Chapter 7 -- Empiricism

Empiricism means grounding our decisions and understanding in observed reality rather than theory, speculation, or authority.

**Grounded in Reality.** An empirical approach values real-world evidence over theoretical reasoning. In software, this means measuring, observing, and testing rather than assuming. The scientific method is inherently empirical -- it starts with observation and builds understanding from there.

**Separating Empirical from Experimental.** Farley makes an important distinction. Empiricism is about being guided by observed reality. Experimentation (covered in the next chapter) is about deliberately creating scenarios to test hypotheses. Empiricism is the broader philosophical stance; experimentation is one technique within it.

**"I Know That Bug!"** Farley warns against the common trap of pattern-matching -- assuming that because a bug looks like one we have seen before, it must have the same cause. This is a form of cognitive bias that can lead us astray. An empirical approach demands that we verify our assumptions with evidence rather than relying on recognition or intuition.

**Avoiding Self-Deception.** Humans are remarkably good at deceiving themselves. We see patterns where none exist, we confirm our biases, and we rationalize failures. An empirical, engineering approach demands that we build in safeguards against self-deception: measurements, automated tests, controlled experiments, and a willingness to be proven wrong.

**Inventing a Reality to Suit Our Argument.** Farley cautions against the tendency to construct narratives that support our preferred conclusions. In software, this manifests as cherry-picking metrics, ignoring inconvenient test results, or constructing post-hoc justifications for decisions. Engineering demands intellectual honesty.

**Guided by Reality.** The ultimate goal is to let reality guide our decisions. This means measuring what matters, testing our assumptions, and being willing to change course when the evidence demands it.

### Chapter 8 -- Experimental

Being experimental means treating our work as a series of carefully controlled experiments. This is the practical application of the scientific method to software development.

**What Does "Being Experimental" Mean?** Farley quotes Richard Feynman: "Science is the belief in the ignorance of experts." We must move away from decisions based on authority, charisma, or fame, and instead make decisions based on evidence. This is a significant cultural change for most software organizations.

**Feedback.** Experiments are structured to produce feedback. The key insight is that we should design our work so that every step produces useful, measurable feedback. This is not about making work more bureaucratic; it is about making it more informative.

**Hypothesis.** Before making a change, we should form a clear hypothesis about what we expect to happen. This makes the outcome more informative: if the result matches our hypothesis, we have confirmation; if it does not, we have learned something potentially more valuable.

**Measurement.** Experiments require measurement. In software, this often means automated tests, performance benchmarks, monitoring data, or user behavior metrics. The key is to measure things that actually tell us something useful about whether our hypothesis was correct.

**Controlling the Variables.** This is perhaps the most important practical aspect of experimental work. If we want to understand the impact of a change, we need to control everything else so that the change is the only variable. In software, this means:

- Deterministic tests that produce the same result every time
- Controlled environments that are isolated from external variability
- Small changes that limit the scope of potential side effects
- Version control for everything (code, configuration, data, infrastructure)

**Automated Testing as Experiments.** Farley describes how TDD is essentially a series of tiny experiments. Each test is an experiment: characterize the desired behavior, form a hypothesis (the test should fail in a specific way), make a prediction (the exact error message), and run the experiment. This is a tiny application of the scientific method, but applied consistently, it has a profound impact on code quality and developer confidence.

**Putting Experimental Test Results into Context.** Testing alone is not enough. We need to understand what our tests tell us and what they do not. Tests are samples of behavior, not proofs of correctness. The value of testing lies in the quality of the samples and our understanding of their limitations.

**Scope of an Experiment.** Experiments range from tiny (a single TDD cycle) to large (a major architectural change). Farley emphasizes that being experimental does not mean only doing large, formal experiments. The power comes from consistently applying experimental thinking at every scale, from individual lines of code to system architecture.

---

## Part III: Optimize for Managing Complexity

### Chapter 9 -- Modularity

Modularity is the practice of dividing a system into distinct, manageable parts (modules) that can be understood, developed, tested, and modified independently.

**Hallmarks of Modularity.** A well-modularized system has clear boundaries between modules, well-defined interfaces, and minimal dependencies between modules. Each module should be small enough to be understood as a unit but large enough to be meaningful.

**Undervaluing the Importance of Good Design.** Farley argues that the software industry systematically undervalues good design, particularly at the code level. Many developers and organizations treat design as a luxury or an afterthought, prioritizing speed of feature delivery. This is a false economy: poor design slows down feature delivery over time as the system becomes harder to understand and change.

**The Importance of Testability.** Testability is both a benefit of good modularity and a driver of it. Code that is easy to test is, almost by definition, well-modularized. Conversely, designing for testability forces us to think about modularity, because testable code requires clear boundaries, well-defined interfaces, and controlled dependencies.

**Designing for Testability Improves Modularity.** This is one of Farley's key themes. When we design code to be testable, we naturally create better-modularized designs. Testability demands that we:
- Separate concerns clearly
- Define explicit interfaces
- Manage dependencies through injection
- Keep modules small and focused

Dependency injection is highlighted as the most effective tool to provide pressure on code that encourages systems composed of many small pieces. The dependencies become the points of measurement that we can inject into our system to achieve a more thoroughly testable outcome. At smaller scales, dependency injection is the most effective tool to provide pressure on our code that encourages us to create systems composed of many small pieces. Ensuring that our code is testable encourages designs that are genuinely modular and, as a result, code that is easier to read.

Some people criticize this style of design, arguing that it is harder to understand code with a bigger surface area. Farley counters that this criticism misses the point. If it is necessary to expose that surface area in order to test the code, then that is the real surface area of the code. The question is not whether the code has many small pieces, but whether those pieces are well-named, well-organized, and clearly responsible for a single concern. A big ball of mud does not become clearer by hiding its complexity behind fewer, larger interfaces.

**Services and Modularity.** At a larger scale, modularity manifests as services (or microservices). A service is a deployable unit of software with a well-defined interface. The same principles of modularity apply at this scale: clear boundaries, well-defined interfaces, and minimal dependencies.

**Deployability and Modularity.** Farley draws a direct connection between modularity and deployability. A system that is well-modularized can be deployed in parts -- each module can be independently tested, built, and deployed. This is a key enabler of continuous delivery.

**Modularity at Different Scales.** Modularity applies at every scale of the system:
- Functions and methods within a class
- Classes and modules within a package
- Packages within an application
- Services within a system
- Systems within an enterprise

**Modularity in Human Systems.** Organizations should also be modular. Teams should be structured around modules (or groups of related modules) with clear boundaries and minimal dependencies on other teams. This is consistent with Conway's Law and the inverse Conway maneuver.

### Chapter 10 -- Cohesion

Cohesion is the degree to which the elements within a module belong together. High cohesion means that all the elements of a module are focused on a single, well-defined purpose.

**Modularity and Cohesion: Fundamentals of Design.** Cohesion and modularity are two sides of the same coin. Modularity is about dividing a system into parts; cohesion is about ensuring that each part is focused and coherent. A module with high cohesion does one thing and does it well. A module with low cohesion does many unrelated things.

**A Basic Reduction in Cohesion.** Farley illustrates how adding seemingly reasonable functionality to a module can reduce its cohesion. For example, adding logging to a business logic module, or adding data access to a domain model. Each addition seems harmless, but over time, the module becomes a grab-bag of unrelated responsibilities.

**Context Matters.** Cohesion is contextual. What constitutes "high cohesion" depends on the scale and purpose of the module. A function that calculates a total is cohesive at one level; a service that manages an entire order lifecycle is cohesive at another. The key is that each module should have a clear, singular purpose at its level of abstraction.

**High-Performance Software.** Farley addresses the common misconception that high-performance code must be poorly structured. He argues the opposite: the route to high performance is simple, efficient code that compilers and hardware can understand and optimize. Performance is not an excuse for a "big ball of mud." Even in performance-critical code, the trick is to draw the seams of abstraction so that high-performance parts of the system fall on one side of a boundary, cohesive and contained.

**Link to Coupling.** Cohesion and coupling are inversely related (in a well-designed system). High cohesion tends to result in lower coupling because a module that does one thing well has fewer reasons to depend on other modules.

**Driving High Cohesion with TDD.** Test-driven development naturally drives high cohesion. When writing a test for a module, if the test requires extensive setup of unrelated concerns, that is a signal that the module has low cohesion. The test forces us to think about what the module's single responsibility is.

**How to Achieve Cohesive Software.** Farley recommends:
- Start with a clear purpose for each module
- Resist the temptation to add "just one more thing"
- Use tests to verify that each module has a single, well-defined responsibility
- Refactor when cohesion starts to degrade

**Costs of Poor Cohesion.** Low cohesion leads to:
- Code that is hard to understand (because it does too many things)
- Code that is hard to test (because tests must set up many unrelated concerns)
- Code that is hard to change (because changes to one responsibility may affect others)
- Code that is hard to reuse (because it bundles unrelated functionality)

**Cohesion in Human Systems.** Teams should also be cohesive -- focused on a clear, singular purpose. A team that is responsible for too many unrelated things will struggle with the same problems as a module with low cohesion.

### Chapter 11 -- Separation of Concerns

Separation of concerns is the principle of dividing a system into distinct sections, each addressing a separate concern. It is closely related to modularity and cohesion but focuses specifically on the nature of the divisions.

**Dependency Injection.** Dependency injection is presented as a key technique for achieving separation of concerns. By injecting dependencies rather than creating them internally, a module can focus on its own concern without being coupled to the concerns of its collaborators. This is the primary mechanism by which testability drives better design.

**Separating Essential and Accidental Complexity.** Farley draws on Fred Brooks' distinction between essential complexity (inherent in the problem domain) and accidental complexity (introduced by the solution). Good separation of concerns isolates accidental complexity (infrastructure, frameworks, technical details) from essential complexity (business logic, domain rules). This is the core idea behind patterns like hexagonal architecture (ports and adapters).

**Importance of DDD (Domain-Driven Design).** Domain-driven design is highlighted as a powerful approach to achieving separation of concerns at the system level. DDD encourages us to:
- Model the software around the business domain
- Define bounded contexts that separate different areas of the domain
- Use a ubiquitous language that is shared between developers and domain experts
- Isolate domain logic from infrastructure concerns

**Testability.** Separation of concerns is essential for testability. If business logic is mixed with infrastructure (database access, network calls, UI code), it becomes extremely difficult to test the business logic in isolation. Separating these concerns allows each to be tested independently and efficiently.

**Ports and Adapters (Hexagonal Architecture).** Farley discusses the ports and adapters pattern as a concrete implementation of separation of concerns. The core domain logic defines ports (interfaces) for its interactions with the outside world. Adapters implement these ports for specific technologies (a database adapter, a REST API adapter, a message queue adapter). This allows the domain logic to be completely isolated from technical details and tested in isolation using fakes or mocks.

**When to Adopt Ports and Adapters.** Farley is pragmatic about this. Not every system needs a full hexagonal architecture, but the principle of separating domain logic from infrastructure is universally applicable. Even simple dependency injection achieves much of the benefit.

**What Is an API?** An API is a boundary between concerns. Farley encourages thinking carefully about APIs as the primary mechanism for separating concerns, whether at the level of a function signature, a class interface, a REST endpoint, or a service contract.

**Using TDD to Drive Separation of Concerns.** TDD is again presented as a driving force. When writing a test, if the test requires setting up infrastructure (a database, a web server, a message queue) to test business logic, that is a signal that concerns are not properly separated. The test is telling us to refactor and separate.

### Chapter 12 -- Information Hiding and Abstraction

Information hiding and abstraction are the mechanisms by which we manage complexity by controlling what is visible and what is hidden.

**Abstraction or Information Hiding.** Farley distinguishes between the two while acknowledging they are closely related. Abstraction is about simplifying a complex reality by modeling only the relevant aspects. Information hiding is about concealing implementation details behind interfaces. Both serve the same ultimate purpose: managing complexity by reducing what needs to be understood at any given level.

**What Causes "Big Balls of Mud"?** The "big ball of mud" -- a system with no discernible architecture -- is the most common architecture in software. Farley identifies two categories of causes:

1. **Organizational and Cultural Problems**: Lack of attention to design, pressure to deliver features quickly, organizational structures that discourage investment in code quality, and a culture that does not value craftsmanship. Farley describes how schedule pressure, "quick fixes," and the normalization of technical debt erode design quality over time. When organizations treat design as an expendable luxury rather than a foundational investment, big balls of mud are the inevitable result.
2. **Technical Problems and Problems of Design**: Failure to apply modularity, cohesion, separation of concerns, abstraction, and loose coupling consistently. This includes mixing business logic with infrastructure, creating classes that do too many things, and failing to define clear boundaries between modules.

Farley shares a telling story from his consulting work: a "strategy group" at a large organization had spent years building a grand distributed architecture that existed only as documents and non-working code. All projects were mandated to use this infrastructure, but no project ever did. On paper the architecture looked fine, but in practice it was only theory. This is the gap between architectural aspiration and engineering reality -- good intentions without the discipline of iterative, empirical validation.

**Fear of Over-Engineering.** Farley addresses the common objection that applying these principles leads to over-engineering. He argues that the opposite is true: under-engineering (the "big ball of mud") is far more costly over time than thoughtful application of these principles. The key is to apply them judiciously, not dogmatically. Good engineering is about finding the right level of abstraction for the problem at hand. Farley's rule of thumb is pragmatic: if the abstraction makes the code easier to understand, easier to test, and easier to change, it is the right level. If it adds complexity without these benefits, it is over-engineering. The fear of over-engineering is often used as an excuse for under-engineering, and the costs of under-engineering accumulate invisibly until they become overwhelming.

**Improving Abstraction Through Testing.** Testing is again a driver of good practice. A well-abstracted module has a clean interface that can be tested through that interface. If tests require knowledge of internal implementation details, the abstraction is poor. Good tests exercise behavior through the public interface, validating the abstraction by treating the module as a black box.

**Power of Abstraction.** Abstraction is arguably the most powerful tool in the software engineer's arsenal. It allows us to build complex systems by stacking layers of understanding, each layer hiding the complexity of the layer below. Programming languages are abstractions over machine code. Operating systems are abstractions over hardware. Web frameworks are abstractions over network protocols. Good software design is about choosing the right abstractions for the problem.

**Leaky Abstractions.** Farley discusses Joel Spolsky's "Law of Leaky Abstractions" -- the observation that all non-trivial abstractions leak some details of the underlying implementation. This does not invalidate abstraction; it means we must be aware of the leaks and design accordingly. A good engineer knows where the abstraction boundaries are and where they might leak. For example, a database abstraction may leak through performance characteristics (some queries are slower than others), through transaction semantics, or through limitations of the query language. Knowing where these leaks are allows us to design around them rather than being surprised by them.

**Picking Appropriate Abstractions.** Not all abstractions are equal. A good abstraction:
- Hides irrelevant details
- Exposes only what is necessary
- Is stable (unlikely to need frequent changes)
- Is meaningful in the problem domain
- Simplifies the mental model for users of the abstraction

**Abstractions from the Problem Domain.** The best abstractions come from the problem domain, not from technical concerns. A "Customer" or an "Order" is a better abstraction than a "Record" or a "DTO." Domain-driven design's emphasis on a ubiquitous language is about ensuring that abstractions in the code reflect abstractions in the domain.

**Abstract Accidental Complexity.** Farley recommends that we abstract away accidental complexity (technical details, infrastructure, frameworks) so that developers can focus on essential complexity (business logic, domain rules). This is the practical application of the separation of concerns principle at the code level.

**Isolate Third-Party Systems and Code.** Third-party code (libraries, frameworks, external services) should be isolated behind abstractions. This prevents the third-party code from leaking into the rest of the system and allows it to be replaced or modified without cascading changes. Farley is emphatic on this point: always prefer to hide information about third-party systems behind your own abstractions.

**Always Prefer to Hide Information.** The chapter's concluding principle is that information hiding should be the default. Expose only what is necessary, and hide everything else. This reduces coupling, improves modularity, and makes the system easier to understand and change.

### Chapter 13 -- Managing Coupling

Coupling is the degree to which modules depend on each other. Managing coupling is about minimizing unnecessary dependencies while maintaining necessary ones.

**Cost of Coupling.** Coupling has real costs. Tightly coupled systems are harder to understand (because changes in one place ripple through the system), harder to test (because testing one module requires setting up its dependencies), harder to deploy (because modules cannot be deployed independently), and harder to change (because changes propagate unpredictably).

**Scaling Up.** As systems grow, the costs of coupling increase disproportionately. In a system with N modules, the number of potential interactions is roughly N-squared. This means that coupling management becomes more important, not less, as the system scales.

**Microservices.** Farley discusses microservices as an architectural approach that emphasizes loose coupling at the service level. Each microservice is an independently deployable unit with a well-defined interface. However, he cautions that microservices are not a silver bullet; the same principles of modularity, cohesion, and separation of concerns apply within each service. Microservices gain their power not from being small, but from being independently deployable and independently changeable. If a "microservice" cannot be deployed without coordinating with other services, it has not achieved the loose coupling that gives the pattern its value.

Farley notes that microservices are not the only way to achieve loose coupling. A well-structured monolith, where internal modules are loosely coupled through clear interfaces, can also be effective. The key question is always: can we make changes independently and deploy them safely? If yes, the architecture is serving its purpose regardless of whether it uses microservices or a modular monolith.

**Decoupling May Mean More Code.** Decoupling often requires more code -- interfaces, adapters, indirection layers. Farley argues that this is a worthwhile investment. The additional code is the "cost" of managing complexity, and it pays dividends in reduced cognitive load, improved testability, and increased flexibility.

**Loose Coupling Is Not the Only Kind That Matters.** While loose coupling is generally preferred, there are cases where tighter coupling is acceptable or even desirable. Within a module, for example, the internal components may be tightly coupled because they share a single concern. The key is to manage coupling at the boundaries between modules, where it has the greatest impact.

**Prefer Loose Coupling.** As a general principle, prefer loose coupling. Modules should interact through well-defined interfaces, minimizing the knowledge each module has about the other's internals. This allows each module to evolve independently.

**How Does This Differ from Separation of Concerns?** Loose coupling and separation of concerns are related but distinct. It is possible to have two pieces of code that are tightly coupled but with a good separation of concerns (they do different things but depend on each other's details), or loosely coupled with a poor separation of concerns (they do overlapping things but through generic interfaces). Both principles are important, and they complement each other.

**DRY Is Too Simplistic.** Farley critiques the "Don't Repeat Yourself" (DRY) principle as too simplistic. While eliminating harmful duplication is important, blindly applying DRY can lead to inappropriate coupling. If two modules share code through a common dependency, they become coupled through that dependency. Sometimes duplication (at the boundary between modules) is preferable to coupling. The key question is: does the shared code represent a genuine shared concept, or are we forcing two unrelated things to share code for the sake of avoiding duplication?

The real question is not "is this code duplicated?" but "does this duplication represent a harmful dependency?" If two teams working on different services happen to have similar code for similar purposes, forcing them to share a library introduces a coupling point. Now changes to that shared library must be coordinated between teams. The coordination cost may far exceed the cost of maintaining the duplication. Farley's guidance is to think about coupling first and duplication second. If sharing code increases coupling in a way that limits independence, prefer the duplication.

**Async as a Tool for Loose Coupling.** Asynchronous communication (message queues, event streams) is a powerful tool for reducing coupling between services. When services communicate asynchronously, they do not need to know about each other's availability or internal state. They simply publish events and react to events, reducing the temporal and structural coupling between them.

**Designing for Loose Coupling.** Practical techniques for achieving loose coupling include:
- Define clear, stable interfaces between modules
- Use dependency injection to manage dependencies
- Prefer asynchronous communication between services
- Isolate third-party code behind abstractions
- Version APIs carefully to allow independent evolution

**Loose Coupling in Human Systems.** Teams that can make decisions independently, without coordinating with other teams, are loosely coupled. The research behind the *Accelerate* book found that this is one of the defining characteristics of high-performing teams. Organizations should be designed to minimize the coupling between teams, allowing each team to move quickly and independently.

---

## Part IV: Tools to Support Engineering in Software

### Chapter 14 -- Tools of an Engineering Discipline

This chapter brings together the practical tools that support the engineering approach described throughout the book.

**What Is Software Development?** Farley recaps: software development is an exercise in discovery and learning. It is design engineering, not production engineering. The tools we use should support learning and managing complexity.

**Testability as a Tool.** Testability is presented as perhaps the most important engineering tool available to software developers. Testable code is:
- Modular (tests can target specific modules)
- Cohesive (tests can focus on a single concern)
- Loosely coupled (tests can isolate the module under test)
- Well-abstracted (tests interact through public interfaces)

Testability is also a measure of design quality. If code is hard to test, that is a signal that the design needs improvement. This makes testing a diagnostic tool as well as a verification tool.

**Measurement Points.** Farley emphasizes the importance of having clear, automated measurement points throughout the development process. These include:
- Unit test results (do individual modules work correctly?)
- Integration test results (do modules work together correctly?)
- Performance benchmarks (does the system meet performance requirements?)
- Deployment pipeline metrics (how long does it take to get feedback?)
- Production monitoring (is the system working correctly in production?)

**Problems with Achieving Testability.** Farley identifies common obstacles to testability:
- Code that is tightly coupled to infrastructure (databases, file systems, network services)
- Code with hidden dependencies (global state, singletons, static methods)
- Code with non-deterministic behavior (randomness, concurrency, time dependencies)
- Code with side effects (logging, metrics, notifications mixed with business logic)

Each of these problems is also a design problem, reinforcing the connection between testability and good design.

**How to Improve Testability.** Practical techniques include:
- Use dependency injection to manage all dependencies
- Separate business logic from infrastructure
- Make side effects explicit and injectable
- Control concurrency and non-determinism by isolating it to controlled boundaries
- Design interfaces that are easy to mock or fake

**Deployability.** Deployability is the ability to deploy software reliably, repeatedly, and quickly. It is a direct measure of how well we have managed complexity. A system that is hard to deploy is almost certainly one that has poor modularity, excessive coupling, or inadequate testing.

The scope of evaluation should always be an independently deployable unit of software. If we cannot confidently release a change into production without further work, then the unit of evaluation -- the scope of the deployment pipeline -- is incorrect. We can choose to include everything within the scope of our deployment pipeline, or decompose the system into independently deployable units, but nothing else makes sense. However fast the evaluation of a small part of the system, it is the time it takes to evaluate the deployability of a change that really matters. Deployability is a vital concern -- thinking in these terms helps focus us on the core question: how do we get feedback in a sensible timeframe that allows us to direct our development efforts?

**Speed.** Speed of feedback is a critical engineering tool. Farley advises teams to optimize their development process so they can achieve a releasable outcome multiple times per day, with a target of less than one hour from commit to releasable state. This target acts as a "fitness function" that drives good practices: small teams, no silos, automated testing, continuous integration, good architecture, and independently deployable units.

Consider what such a target implies. You cannot have teams that are too large, because the communication overhead will slow them down too much. You cannot have siloed teams, because the cost of coordination between teams will be too slow. You have to have a great position on automated testing, you need feedback mechanisms like continuous integration and continuous delivery, you have to have good architecture to support these strategies, and you need to be evaluating independently deployable units of software.

If you take an iterative, experimental approach to only improving the speed of feedback in your development process, it acts as a kind of fitness function for all of agile theory, all of lean theory, and all of continuous delivery and DevOps. This focus on speed and feedback leads you inexorably to these ideas. That is a much more powerful, measurable guide in the direction of better outcomes than following rituals or recipes from an off-the-shelf development process.

**Controlling the Variables.** If we want to test and deploy quickly, reliably, and repeatably, we need to control the variables:
- Automate deployment and configuration
- Ensure tests are deterministic (same results every time for the same code)
- Limit variance in test environments
- Isolate tests from external dependencies
- Version control everything

Where we cannot exert control, we must treat the boundaries that touch the uncontrolled world with great care. Abstraction, separation of concerns, and loose coupling are key ideas to limit exposure to anything outside our direct control. We want tests that give precisely the same results every time for the same version of the software. If test results vary, we should work to exert greater control, improve isolation, or improve determinism in the code. Modularity, cohesion, separation of concerns, abstraction, and coupling are again the key ideas that allow us to exert this control.

Reliably testable code is not multithreaded within the scope of a test, except for some very particular kinds of tests. Concurrent code is difficult to test because it is not deterministic. So if we design code to be testable, we think carefully about concurrency and work to move it to controlled, well-understood edges of the system. This results in code that is easier to test, easier to understand, and computationally more efficient.

Farley shares a cautionary tale of a large organization that built extensive performance tests but ran them on the corporate network, making results so variable that no one could tell what they meant. All the work to create and execute those tests was waste. Computers give us a fantastic opportunity: they are deterministic, and they are incredibly fast. We can choose to give up these advantages or take control and make use of them.

**Continuous Delivery.** Continuous delivery is presented as the organizing philosophy that ties everything together. It is not about automating deployment (though that is part of it); it is about organizing work to create a semi-continuous flow of changes. Taking continuous delivery seriously demands:
- Structuring organizations to minimize dependencies and promote team autonomy
- Applying high levels of automation, particularly in testing
- Taking deployment and configuration seriously
- Controlling variables for repeatability and reliability

Continuous delivery is a highly effective strategy around which to build a strong engineering discipline for software development.

**General Tools to Support Engineering.** Farley shows how the ideas in the book can be used as qualifiers for any technology decision. When evaluating a third-party component, framework, or service, ask:
- Is it deployable? Can we automate its deployment?
- Is it testable? Can we confirm it does what we need?
- Does it allow us to control the variables?
- Is it fast enough for continuous delivery?
- Does it allow us to maintain modular, well-designed code?

The wrong answer to any of these questions should disqualify the technology.

### Chapter 15 -- The Modern Software Engineer

The final chapter ties together the book's themes and extends them to broader organizational and strategic concerns.

**Engineering as a Human Process.** Engineering is about the process of doing work, not just the output. It is empirical, based on scientific reasoning, and focused on making rationally informed decisions with incomplete information. Engineering recognizes that organizations and teams are information systems too, and the principles of managing complexity apply to them as much as to code.

**Digitally Disruptive Organizations.** The most successful modern organizations are engineering-led. Software development is not a cost center; it is the business. Farley cites Jan Bosch's BAPO vs. OBAP model:

- **OBAP** (how most businesses operate): Fix the **Organization** first, then decide on a **Business** strategy within those constraints, then pick an **Architecture**, then choose a **Process**. This is backwards -- business vision is constrained by organizational structure.
- **BAPO** (how businesses should organize): Start with **Business** vision and goals, then determine the **Architecture** needed, then define the **Process** to build it, then create an **Organization** that supports the process.

Modular, cohesive organizations with sensible separation of concerns, where teams can hide information from other parts of the organization, are more scalable and efficient. This is one reason Amazon more than doubles in productivity when it doubles in size, while traditionally structured firms increase by only 85 percent.

**Outcomes vs. Mechanisms.** Farley argues that outcomes are more important than mechanisms. Continuous delivery defines a desirable outcome ("work so your software is always releasable," "optimize for fast feedback") rather than a specific mechanism. This makes it more useful as a general organizing principle than a collection of practices (like DevOps), because outcomes remain valid even when circumstances change.

The principles of continuous delivery still hold even when physical constraints prevent achieving the recommended feedback targets. Testing thoroughly, rejecting any change that fails a test, automating everything possible -- these principles apply whether you are building web software, cars, or rockets.

**Durable and Generally Applicable.** A genuine engineering discipline should be agnostic of technology. Its principles should be long-lasting and useful for answering questions we have not foreseen and understanding technologies we have not yet invented.

Farley demonstrates this by applying the book's principles to machine learning (ML), a field he openly admits to not being expert in:
- ML development is clearly about learning (for both the machine and the developers)
- Managing complexity is essential when working with large datasets
- The development process is inherently iterative
- Feedback is delivered through fitness function accuracy
- Controlling variables (version controlling scripts and data) is crucial
- Separation of concerns in training data helps prevent problems like biased models

Even without deep ML expertise, the engineering principles allow Farley to pose meaningful questions that are not commonly asked in ML circles. This is what a genuine engineering discipline should provide: not answers, but an approach that guides toward better answers.

**Foundations of an Engineering Discipline.** Farley concludes by reiterating the ten foundational ideas:

*Optimizing for Learning:*
1. Iteration
2. Feedback
3. Incrementalism
4. Experimentation
5. Empiricism

*Managing Complexity:*
6. Modularity
7. Cohesion
8. Separation of Concerns
9. Abstraction
10. Loose Coupling

Supported by the practical tools of testability, deployability, speed, controlling the variables, and continuous delivery.

The programming language, framework, and methodology matter less than how these fundamental principles are applied. These ideas, organized around optimizing for learning and managing complexity, form the foundation of a genuine engineering discipline for software development.

---

## Key Themes and Recurring Patterns

**The Primacy of Learning.** Every practice, technique, and tool in the book is evaluated through the lens of learning. Does this help us learn faster? Does this give us better feedback? Does this allow us to adapt to new information? If the answer is no, the practice should be questioned.

**Testing as a Design Tool.** Automated testing is not merely a quality assurance mechanism. In Farley's framework, testing is a design tool that drives modularity, cohesion, separation of concerns, and loose coupling. Test-driven development is not primarily about catching bugs; it is about designing better software.

**The Feedback Loop Architecture.** The book describes a hierarchy of feedback loops, from milliseconds (IDE feedback) to hours (deployment pipeline) to days (user feedback) to weeks (retrospectives). Optimizing each loop and ensuring information flows between them is the practical application of the learning principle.

**Complexity as the Enemy.** Complexity is the primary obstacle to sustainable software development. Every technique in the book is ultimately about managing complexity: breaking systems into manageable parts (modularity), ensuring each part is focused (cohesion), separating different kinds of concerns, hiding unnecessary details (abstraction), and minimizing dependencies (loose coupling).

**Engineering as Organizing Philosophy.** Engineering is not a set of rituals or a bureaucratic process. It is a way of thinking -- a commitment to evidence over authority, measurement over intuition, and controlled experimentation over guesswork. This philosophy applies at every scale, from individual lines of code to organizational structure.

**The Interconnectedness of the Principles.** The ten foundational ideas are deeply interconnected. You cannot achieve good modularity without cohesion, good separation of concerns without abstraction, or loose coupling without information hiding. This interconnectedness is a feature, not a bug -- it means that applying any one principle tends to reinforce the others. Modularity, cohesion, and separation of concerns enhance our ability to gather feedback and so facilitate experimentation. The principles of managing complexity directly support the principles of learning, and vice versa. Farley notes that he has looped through each of these topics many times during the book, and that this is both intentional and inevitable, but also says something important about the ideas: not only are they deeply linked, but they apply nearly everywhere, and that is the whole point.

**Sustainability.** A key concern throughout the book is sustainability. The ability to learn and adapt must be maintained over time. This means managing complexity is not optional -- without it, the system becomes progressively harder to change, and the team's ability to learn degrades. Sustainable development requires sustainable design. The *Accelerate* research found that teams taking a more disciplined approach to development spend 44% more time on new work than teams that do not, because they spend less time fixing problems caused by poor design. This is the ultimate argument for taking engineering seriously: it frees up more time to do the creative, interesting work of building new things.

---

## Quotes and Key Definitions

- **Software Engineering**: "The application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software."
- **Engineering**: "The application of an empirical, scientific approach to finding efficient, economic solutions to practical problems."
- **On production**: "Production is not our problem. This makes our discipline unusual."
- **On engineering vs. code**: "Engineering is not just the output -- the code or perhaps its design. It is the processes, tools, and techniques. It is the ideas, philosophy, and approach that together make up an engineering discipline."
- **On testing and design**: "Testable code is modular with a good separation of concerns. Automated testing creates a positive feedback loop that enhances our ability to design better systems."
- **On DRY**: "DRY is too simplistic. Sometimes duplication is preferable to coupling."
- **On craft vs. engineering**: "Craft-based production is fundamentally low-quality. A human being, however talented, is not as accurate as a machine."
- **On the scientific method in practice**: "When practicing TDD, I begin an intended change to my code with a test. I predict the exact error message that I expect the test to fail with. This is an experiment; this is a tiny application of the scientific method."

---

## Conclusion

Farley's *Modern Software Engineering* is both a manifesto and a practical guide. It argues that software development has been misusing the term "engineering" for decades, conflating production-engineering thinking with what is fundamentally a design-engineering discipline. By grounding software engineering in the actual practices of engineering -- empiricism, experimentation, measurement, and managed complexity -- Farley provides a coherent framework that connects practices like TDD, continuous delivery, and microservices to foundational principles.

The book's central message is simple: if you always optimize your work to maximize your ability to learn efficiently, you will do a better job. If you always work, at every scale, to manage the complexity of the work in front of you, you will be able to sustain your ability to do a better job indefinitely. These are the hallmarks of a genuine engineering discipline for software development, and when we apply that discipline, we dramatically improve our chances of building better software faster.

Farley is the first to acknowledge that this is not a "crank the handle" approach. You are not going to get great software by simply following a recipe, any more than you will create a great car by following a dot-to-dot car builder's manual. This approach requires being thoughtful, diligent, careful, and intelligent. Software development is not an easy thing to do well. The model is simple -- ten fundamental ideas in two groups, supported by tools like testability, deployability, speed, controlling the variables, and continuous delivery -- but the implications of those ten things are often thought-provoking and complex, which makes them difficult to apply consistently.

Farley's intention is not to say "software is easy" but rather to admit that "software is difficult, so let's approach it thoughtfully." This means approaching it with care, within a framework of thinking that enables us to find better answers to questions we have not thought of yet -- an approach to finding solutions to problems that we have no idea how to solve. These ten ideas give us that framework.

The programming language you choose does not really matter. The framework you employ does not really matter. The methodology you pick matters less than the ideas outlined in this book. These choices matter to the degree that the model of hammer a carpenter chooses matters -- they have an impact on how a team works together, but in essence the choice of one technology over another has less impact on the outcome than how that technology is applied. The best software developers Farley has worked with wrote good software whatever tools they chose to apply. Their core skill, talent, and value lay not in their tool expertise but in their ability to think clearly about complex problems and manage the complexity of their solutions.

The research is clear: teams that adopt these principles create software of higher quality, produce work more quickly, and the people on those teams report that they enjoy their work more, feel less stress, and have a better work-life balance. These are extravagant claims, but they are backed by data from the State of DevOps reports and research from organizations like Microsoft and Google. Engineering, properly understood and applied, is "the stuff that works."

---

## Key Takeaways

1. **Software engineering is design engineering, not production engineering.** Production in software is essentially free -- it is the push of a button. The entire discipline is one of design, learning, and discovery. Applying production-line thinking (waterfall, heavy upfront planning, rigid processes) to software is a category error that has caused decades of waste and failure.

2. **The definition that anchors the book:** "Software engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software." Every word is deliberate -- it is empirical (grounded in observation), scientific (structured reasoning), practical (not theoretical), efficient (minimizing waste), and economic (constrained by real-world limits).

3. **Two meta-skills define the discipline: becoming experts at learning and becoming experts at managing complexity.** These are not arbitrary categories. Software development is inherently a process of discovery (you cannot fully know what to build until you start building it), so learning speed is the primary competitive advantage. And because systems grow beyond any individual's comprehension, managing complexity is what allows learning to remain sustainable over time.

4. **The five learning principles -- iteration, feedback, incrementalism, empiricism, and experimentation -- are mutually reinforcing.** Iteration without feedback is mere repetition. Feedback without controlled experiments is noisy. Incrementalism without iteration produces incomplete systems. Together they form a coherent scientific approach to software development at every scale.

5. **The five complexity management principles -- modularity, cohesion, separation of concerns, abstraction, and loose coupling -- are also deeply interconnected.** You cannot achieve good modularity without cohesion, good separation of concerns without abstraction, or loose coupling without information hiding. Applying any one principle naturally pressures you toward the others.

6. **Testing is a design tool, not just a verification tool.** This is one of Farley's most important reframes. TDD is not primarily about catching bugs; it is about designing better software. If a test is hard to write, that is immediate feedback that the design is poor. Designing for testability drives modularity, cohesion, separation of concerns, and loose coupling. Farley calls TDD a "talent amplifier" -- it does not replace skill but enhances whatever skill level a developer has.

7. **Feedback speed is a fitness function for your entire development process.** Farley advises targeting a releasable state in under one hour from commit, with commit-stage results in five minutes. If you optimize for feedback speed alone, you are inevitably driven toward small teams, no silos, automated testing, continuous integration, good architecture, and independently deployable units. This single metric acts as a compass that points toward all the right practices.

8. **DRY is too simplistic.** The "Don't Repeat Yourself" principle, when applied blindly, creates inappropriate coupling. Two teams with similar code in separate services should sometimes tolerate duplication rather than share a library, because the shared library becomes a coupling point that forces coordination. The real question is not "is this code duplicated?" but "does this duplication represent a harmful dependency?" Think about coupling first and duplication second.

9. **Continuous delivery defines an outcome, not a mechanism.** "Work so your software is always in a releasable state" and "optimize for fast feedback" are guiding principles that remain valid regardless of technology, scale, or domain. This makes continuous delivery more durable and widely applicable than any specific collection of practices. Whether you are building web software, cars, or rockets, the principles hold even when the specific feedback targets must be adjusted for physical constraints.

10. **The principles apply to organizations, not just code.** Organizations are information systems too. Modular, cohesive teams with clear boundaries and minimal cross-team dependencies are more scalable and more effective. The DORA research found that high-performing teams are defined by their ability to make decisions independently without seeking permission or coordination from other groups -- they are informationally decoupled. Amazon's "two-pizza teams" and the BAPO model (Business first, then Architecture, then Process, then Organization) are practical applications of these engineering principles at the organizational level.

11. **Determinism is a property of well-engineered systems, and it emerges from modularity.** Digital systems are inherently deterministic in the absence of concurrency. By isolating concurrency to controlled boundaries and designing modules so that entry is sequenced and outcomes are predictable, you create systems that are reliably testable. Farley's team built a financial exchange that was so deterministic they could record production inputs and replay them later to reproduce the exact same system state in a test environment. This was not the initial goal; it was a side effect of designing for testability.

12. **Big balls of mud are the default outcome without discipline.** The most common software architecture is no architecture at all. Schedule pressure, "quick fixes," and the normalization of technical debt erode design quality over time. The fear of over-engineering is often used as an excuse for under-engineering, and the costs of under-engineering accumulate invisibly until they become overwhelming. Applying these principles judiciously -- not dogmatically -- is the antidote.

13. **The ten foundational ideas are technology-agnostic and durable.** They should help you solve problems using technologies that have not been invented yet. The programming language, framework, and methodology you choose matter less than how you apply these fundamental principles. The best developers Farley has worked with wrote good software whatever tools they used; their core skill was the ability to think clearly about complex problems and manage the complexity of their solutions.

14. **Engineering is not bureaucracy -- it is the opposite.** Properly understood, engineering is pragmatic, evidence-based, and focused on efficiency. If your "engineering process" slows you down without improving quality, it is not engineering. Engineering is "the stuff that works" -- and the data from the State of DevOps reports consistently shows that teams taking an engineering approach move faster and produce higher-quality output than teams that do not.

15. **There is no recipe.** These ten ideas give you a framework for thinking, not a dot-to-dot guide. You must be thoughtful, diligent, and willing to exercise judgment. The model is simple but its implications are complex, which makes it difficult to apply consistently. Farley's intention is not to say "software is easy" but to admit that "software is difficult, so let us approach it thoughtfully," within a framework that enables finding better answers to questions we have not yet thought of.
