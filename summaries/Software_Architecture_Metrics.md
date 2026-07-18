# Software Architecture Metrics: Comprehensive Summary

**Authors:** Christian Ciceri, Dave Farley, Neal Ford, Andrew Harmel-Law, Michael Keeling, Carola Lilienthal, Joao Rosa, Alexander von Zitzewitz, Rene Weiss, and Eoin Woods

**Subtitle:** Case Studies to Improve the Quality of Your Architecture

**Publisher:** O'Reilly Media

This is a practical, case-study-driven book that introduces key software architecture metrics for measuring and improving architecture quality. Ten experienced practitioners share their approaches, tools, and real-world experiences for using metrics to guide architectural decisions, combat technical debt, and ensure maintainability. The book is not about theory -- it is about practice and implementation, based on real-world experience and written for software architects and developers.

---

## Chapter 1: Four Key Metrics Unleashed -- Andrew Harmel-Law

This chapter provides a detailed practical guide to implementing the four key metrics from the book *Accelerate* (by Forsgren, Humble, and Kim): deployment frequency, lead time for changes, change failure rate, and time to restore service. These metrics measure two complementary aspects of software delivery: development throughput (first pair) and service stability (second pair). The power lies in their combination -- improving throughput while degrading stability produces no long-term benefit. Transformations that realize predictable, long-term value are ones that deliver positive impact across the board.

### The Mental Model and Instrumentation Points

The metrics are built on a pipeline model: changes flow from developer commit through CI/CD to production deployment, as visualized in the fundamental mental model diagram. There are four instrumentation points: commit timestamp, deployment timestamp, service failure detection time, and service restoration time. The commit timestamp starts the clock (ideally when any developer change-set is considered complete and committed); the deployment timestamp stops it for throughput metrics (when the final deployment to production completes). Service failure and restoration timestamps feed the stability metrics.

### Refactoring the Mental Model for Your Context

Real-world pipeline shapes vary widely, and the author walks through four major varieties with diagrams:

1. **Single end-to-end pipeline:** The simplest -- a monolith in a monorepo with one pipeline from commit to production. Rarely seen in practice.
2. **Multiple end-to-end pipelines:** One pipeline per artifact or repository (e.g., one per microservice). Ideal for microservices; simple to instrument.
3. **Subpipeline chains:** Multiple subpipelines that fit end-to-end. For example: first subpipeline does compilation, packaging, and testing; second deploys to test environments; third handles CAB process to production. Requires tracking change-sets across subpipelines.
4. **Multistage fan-in pipelines:** Individual subpipelines per repository that "fan in" to shared subpipelines. Most complex to instrument because you must trace each deployment back to its originating repository and commit timestamp.

Key subtleties: only count successful builds (failed builds artificially lower lead times); define "failure in production" consistently (anything preventing users from completing tasks, not cosmetic defects); include "zero" deployment days in frequency calculations; and treat the highest non-production environment as a proxy when production metrics are unavailable.

### Capture, Calculation, and Display

Manual capture is acceptable and even recommended as a starting point -- every time the author has rolled out the four key metrics, he started with manual collection. While automation is desirable, beginning manually is fine and frequently serves not only for the initial baseline but for ongoing tracking as well. The reported metrics should use rolling windows to smooth fluctuations:

- **Deployment frequency:** This is a frequency, not a raw count. Sum the total number of successful deployments per day (including "zero" days when no deployments occurred). If you have multiple pipelines, sum deployments from them all. Report the mean over the last 31 days. Working with just the latest daily figure suffers from too much fluctuation.
- **Lead time for changes:** Calculate the elapsed time for each individual change from commit to deployment. This can fluctuate enormously, especially with fan-in pipelines where some builds run much faster than others due to blocking. Take each individual lead time measurement, calculate the mean over the course of a day, then report the mean of those daily values over the last 31 days. Never average an average without understanding the implications.
- **Change failure rate:** The proportion of deployments that gave rise to failures. Specifically: sum the number of resolved change failures over the last 31 days, then divide by total deployments in the same period. Only count resolved failures (because unresolved failures don't have resolution timestamps). There is a "leap of faith" here -- the metric assumes failures are distinct and caused by single deployments, which mostly holds in practice.
- **Time to restore service:** The time a change failure ticket takes from creation to closure. Both mean and median are useful: mean is sensitive to outliers (sometimes exactly what you want during learning), median is more stable. Use the last 120 days of resolved failure times.

Transparency is critical: raw data, calculations, and definitions should be openly shared. The author quotes Donella Meadows: "You keep pointing at the anomalies and failures in the old paradigm. You keep speaking and acting, loudly and with assurance, from the new one." Making metrics visible generates conversations, and conversations generate improvement ideas from the team itself. Pay attention to access -- if your four key metrics aren't shared with everyone, you're missing out on their greatest strength. The definitions you've specifically applied, and how you're treating those definitions, should be available alongside the data itself. This transparency deepens understanding and heightens engagement.

### Using Metrics to Drive Architecture

When teams see their metrics and understand the forces behind them, they naturally gravitate toward better architecture: loosely coupled, independently deployable services; comprehensive automated testing; strong observability; and modular design. The metrics act as a catalyst for architectural evolution rather than a top-down mandate. The four key metrics allow architects to "loosen their grip on the tiller" -- instead of dictating, they stimulate desire for improvement across the team.

---

## Chapter 2: Fitness Functions and the Testing Pyramid -- Rene Weiss

This chapter introduces fitness functions as a systematic method for creating architecture metrics, along with a testing pyramid adapted specifically for architectural verification. The author acknowledges George Box's observation that "all models are wrong" but hopes this one is useful.

### What Are Fitness Functions?

Borrowed from evolutionary computing, an architectural fitness function is "any mechanism that provides an objective integrity assessment of some architectural characteristic(s)." Unlike functional tests that validate domain behavior, fitness functions validate architecture characteristics like performance, security, maintainability, and scalability. The concept was first introduced in *Building Evolutionary Architectures* by Ford, Parsons, and Kua. They provide an objective, measurable way to govern architecture.

### Mandatory and Optional Categories

Fitness functions are classified along several mandatory dimensions:
- **Breadth of feedback:** Atomic (limited feedback on whole system) vs. holistic (broad feedback on system health)
- **Test execution trigger:** Triggered (by a development action) vs. continuous (constantly running)
- **Execution location:** CI/CD, test environment, or production system
- **Metric type:** True/false, discrete value, or time series/historical values
- **Automation:** Automated or manual
- **Quality attribute:** Mapped to ISO 25010 characteristics (functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability)

Optional categories include: temporary vs. permanent (e.g., active only during a refactoring), static vs. dynamic (fixed threshold vs. range relative to another value such as response time relative to concurrent users), target audience (developers, operations, product managers), and applicability scope (certain technologies or system areas).

### The Fitness Function Testing Pyramid

Adapted from the functional testing pyramid, the fitness function testing pyramid has three layers based primarily on two dimensions: breadth of feedback (atomic vs. holistic) and execution trigger (triggered vs. continuous):

- **Bottom layer (triggered atomic):** Fast, cheap, easy to implement. Examples: code coverage metrics, cyclomatic complexity checks, static code analysis, simple performance tests. These form the broad base. The author recommends building a broad base here first.
- **Middle layer (triggered holistic or continuous atomic):** Integration tests measuring system-level properties in test environments, or continuous monitoring of atomic values like transaction duration. Triggered holistic tests run on schedule (e.g., nightly) and test cross-cutting concerns.
- **Top layer (continuous holistic):** Most sophisticated feedback, closest to real-world use cases. Examples: revenue per minute monitoring with expected corridors, chaos engineering, deployment-time regression tests. Complex to build and maintain, so fewer tests belong here. Top-level tests are nondeterministic more often because many components are involved.

### Detailed Examples

The chapter provides fully categorized examples at each level:
- Bottom: Unit test coverage exceeding 90% (triggered, atomic, CI/CD, specific value, automated, maintainability)
- Middle: Integration tests with network latency simulation (triggered, atomic-to-holistic depending on scope, CI/CD and test environment, 0/1 binary, automated, reliability)
- Top: Revenue per minute monitoring with time-of-day corridors (continuous, holistic, production, discrete value, automated, multiple quality attributes, dynamic thresholds)
- Top: Regression test during rolling deployment (triggered by deployment, holistic, production, mixed metric types, automated, reliability and performance)

### Developing Fitness Functions

The recommended process, integrated into iterative development (like Scrum):

1. Work with stakeholders to identify the most important quality attributes, set architectural goals, and document them
2. Formulate draft fitness functions with target metrics in a shared backlog
3. Prioritize and select feasible functions, balancing pyramid layers
4. Finalize definitions and classify them with full categorization
5. Develop automated tests that produce the target metric
6. Visualize results on dashboards shared with the team
7. Iterate regularly -- decommission functions that no longer provide value, tighten thresholds as the system improves

The author recommends starting small and easy with bottom-layer tests, then learning while implementing. Don't try to identify all fitness functions upfront -- discover them as you learn.

---

## Chapter 3: Evolutionary Architecture -- Dave Farley

Farley argues that software architecture should be evolutionary, guided by testability and deployability, rather than based on up-front prediction of future needs. Architectural descriptions function like tourist maps: they help navigate without being overly precise about details that will change.

### The Importance of Learning and Discovery

Complex systems never spring fully formed from the minds of their creators; they are the output of a process of incremental progression and learning. Software development is always an exercise in learning and discovery. Architects should stop trying to imagine that they should, or even could, foresee how their system will be used and evolve. Real-world systems are part of complex adaptive systems encompassing developers, users, customers, and organizational contexts. This calls for a dynamic, organic approach that allows learning as you go.

### Five Attributes of Sustainable Design

The chapter identifies five attributes that enable evolutionary architecture:

1. **Modularity:** Dividing systems into parts that can change without forcing change in other parts
2. **Cohesion:** Keeping parts of the code that change together close together in the code
3. **Separation of concerns:** Ensuring each part of the code and system is focused on solving one problem
4. **Abstraction/information hiding:** Creating "seams" that allow consuming behaviors without understanding how other parts work
5. **Coupling management:** Minimizing the degree to which separate parts need to change together

These attributes are universally true for information in general, not just software. Whatever a system does and whatever technology it employs, if it scores well on these five attributes, it will be easier to work on, change, understand, and test.

### Testability Drives Quality

The key insight is that the attributes of testable code are identical to the attributes that make code easy to work with and change. Modular code is easier to test than non-modular code. Cohesive, loosely coupled code is easier to set up for testing. Good separation of concerns lets you focus on the behavior you're testing. Abstracted code lets tests be somewhat decoupled from implementation details. Designing for testability amplifies developers' talent and results in systems that embody all five attributes far better than relying on skill, experience, and commitment alone. The practical mechanism is to use tests to guide code design -- writing tests first naturally produces better-structured code.

### Deployability at Scale

Deployability, realized through continuous delivery and deployment pipelines, operates at a more systemic level than testability. In continuous delivery, software is always kept in a releasable state. A deployment pipeline automates release evaluation: if it passes all evaluations, the software is by definition safe to release. The correct scope for a deployment pipeline is always an independently deployable unit of software. To increase evaluation reliability, you need deterministic behavior: the same code should produce the same test results every time.

Farley concludes that focusing on testability and deployability keeps architectural options open. If your system is modular, abstracted, and well-factored, adding enhanced security, resilience, or scalability when actually needed is far easier. Overengineering for hypothetical future requirements is wasteful; an evolutionary approach allows you to begin sooner and better adapt to real needs.

---

## Chapter 4: Improve Your Architecture with the Modularity Maturity Index -- Dr. Carola Lilienthal

This chapter introduces the Modularity Maturity Index (MMI), a structured evaluation framework for assessing technical debt and architectural quality. Based on Lilienthal's doctoral thesis connecting cognitive science to software architecture, plus more than 300 architectural assessments, the MMI provides a standardized way to compare technical debt across systems.

### Technical Debt: Types and Origins

Implementation debt (code smells like long methods and empty catch blocks) can be found through automated tools and resolved gradually by development teams. Design and architecture debt (inconsistent class, package, and module dependencies that don't match the planned architecture) requires extensive architecture review. Systems cycle between accumulating debt during maintenance and reducing it through architecture improvement. When improvement is neglected, architecture erosion sets in until every change becomes expensive and painful. Two escape paths exist: refactoring from the inside out (step-by-step improvement) or replacing the system entirely.

### Three Principles from Cognitive Science

The MMI is grounded in three principles derived from how the human brain processes complex structures:

1. **Modularity (45% weight):** Based on "chunking" -- the brain groups related information into meaningful, coherent units. Software modules should contain coherent elements that form something meaningful. Evaluated through domain and technical modularization, internal interfaces, proportions of classes/methods/packages, and clear naming.

2. **Hierarchy (30% weight):** The brain uses hierarchical structures for organizing knowledge. Software should exhibit clear layering without cycles. Class cycles, package cycles, layer violations, and upward dependencies all break hierarchy. Cycles are easy to measure at all levels. Example: one system had 242 of 479 classes in a single cycle spread across 18 directories.

3. **Pattern consistency (25% weight):** Based on "schemas" -- mental models that help us quickly understand familiar structures. Design patterns in code provide these schemas. Consistently applied patterns help developers deal with complexity. Evaluated through pattern allocation, cycle-free pattern relationships, explicit pattern mapping, and separation of domain from technical code.

### MMI Calculation and Architecture Reviews

The MMI uses 22 specific criteria organized into the three principles, each scored 0-10 using detailed lookup tables. Modularity carries 45% weight, hierarchy 30%, and pattern consistency 25%. The resulting score is interpreted as: 8-10 = low technical debt; 4-8 = significant debt requiring refactoring; below 4 = consider replacement.

Architecture reviews compare target architecture against actual code, using tools like Sotograph, Sonargraph, Lattix, Structure101, and TeamScale. The process involves parsing source code, recording actual architecture, modeling the target, comparing, and identifying deviations. Reviews are conducted collaboratively with the development team in workshops.

---

## Chapter 5: Private Builds and Metrics -- Christian Ciceri

This chapter addresses the reality that many organizations have not fully adopted DevOps best practices, providing practical guidance for navigating imperfect transitions using private builds and targeted metrics.

### CI/CD and DevOps Fundamentals

CI is a development practice where team members integrate at least daily, verified by automated builds. CD extends CI through the full delivery pipeline. DevOps removes silos between development and operations, encompassing culture, tools, automation, and shared responsibility. Ciceri emphasizes that culture is the biggest change DevOps introduces: both developers and ops must cross borders of their disciplines. Automation from development (automated tests, private builds) must be extended by automating environments, deployments, and runtime introspections.

### Private Builds as a Survival Tool

A private build is a local build run before pushing to the shared mainline. In organizations with broken or immature CI/CD pipelines, private builds serve as a safety net. The chapter presents case studies:

- **DevOps and QA disconnected:** When QA validates independently without CI integration, developers should run private builds including integration tests.
- **Unproductive feedback loops:** Long CI build times or unreliable tests create slow feedback. Private builds with targeted test suites provide faster feedback.
- **Automation without understanding:** Teams automating everything without understanding why produce impressive dashboards but poor quality.
- **Lost ownership of validations:** When a separate team owns CI/CD, developers lose the habit of validating locally. Private builds restore responsibility.

### Key Metrics for Survival Mode

Recommended metrics when full DevOps maturity is not achievable: build success rate, time to feedback, number of bugs found in QA, deployment frequency, and bug assessment patterns (density per module, resolution time, reopen rate, correlation with code volatility and complexity). Even in imperfect environments, metrics and disciplined practices like private builds can significantly improve outcomes.

---

## Chapter 6: Sociotechnical Architecture -- Joao Rosa

Told through the fictional story of architect Anna at a fintech company called YourFinFreedom, this chapter explores how metrics connect software architecture to business outcomes through sociotechnical thinking. The narrative tracks the company's journey from monolith to distributed big ball of mud and back toward intentional architecture.

### Big Ball of Mud and Distributed Big Ball of Mud

Brian Foote and Joseph Yoder defined "big ball of mud" in 1999 as a "haphazardly structured, sprawling, sloppy, duct-tape and bailing wire, spaghetti code jungle." The distributed version adds network complexity. Both arise from accidental complexity -- dependencies, poorly documented code, unstructured design -- introduced when teams struggle with business pressures. Cognitive load (from Skelton and Pais's *Team Topologies*) becomes a critical constraint: the amount of information a team must hold in their brains to understand business transactions.

### EventStorming for Intentional Architecture

Anna uses Big Picture EventStorming to visualize business processes, map current software components onto emergent domains, and identify mismatches between process and implementation. Process Modeling EventStorming dives deeper into specific operational value streams, mapping KPIs and hotspots. These workshops reveal: boundaries between domains and software are misplaced, domain boundaries are incorrect creating accidental complexity, and cognitive load is high because teams own components across domain boundaries.

### KPI Value Trees and DORA Metrics

A KPI Value Tree has three levels: organizational KPIs (broad, lagging indicators like EBITDA and monthly active users), domain KPIs (narrower lagging indicators), and metrics (both lagging and leading indicators like deployment frequency and change fail rate). The tree is a snapshot that must evolve. Rosa warns against Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure." KPIs and metrics should be guides and enablers, not targets.

The four DORA metrics (lead time, deployment frequency, change fail rate, mean time to restore) are leading indicators of velocity and stability. Rosa also recommends mean time to discover (time between incident occurrence and discovery), throughput (team delivery capability), and employee Net Promoter Score. Comparing teams using the same metrics is counterproductive because contexts differ.

### Managing Expectations

As Anna's organization evolves, changes in software component ownership affect teams with trade-offs on both technical and social levels. Being explicit about consequences prevents frustration. Rosa argues for a new generation of software architects trained in facilitation, group dynamics, and business strategy, who understand the implications of technical decisions on the social fabric.

---

## Chapter 7: The Role of Measurement in Software Architecture -- Eoin Woods

Woods provides a comprehensive framework for integrating measurement into software architecture work throughout the delivery lifecycle.

### Adding Measurement to Software Architecture

Historically, measurement was deferred until production. Modern approaches (continuous delivery, RCDA, continuous architecture) require measurement throughout the lifecycle. The relationship is cyclical: extract measurements, inform decisions, change the system, measure again.

### Four Types of Measurement

Woods classifies measurements along two axes (artifact vs. operational, external vs. internal):

- **External artifact measurements:** Compliance checks through design documentation. Weakest but earliest possible.
- **Internal artifact measurements:** Code complexity, module coupling, schema size. Tangible, accurate, inexpensive, but require completed code.
- **External operational measurements:** Response time, throughput, failures per month. Capture actual user experience.
- **Internal operational measurements:** Memory usage, database index growth. Visible to dev/ops teams.

### Measurement Approaches

Runtime measurement uses logs, traces, and metrics from infrastructure and applications. Software analysis uses static code analysis for structural characteristics. Design analysis captures minimal design representations before implementation for predictive measurements. Estimates and models (typically spreadsheets) capture relationships between operational parameters and quality attributes -- best for numerically representable qualities.

### Measuring Specific System Qualities

**Performance:** Measured as latency (time per operation) and throughput (operations per time period). Key considerations: test environment vs. production, model calibration, realistic workload, and distribution characterization (mean, median, standard deviation).

**Scalability:** Measured by running performance measurements at different load levels and observing metric changes. Scalability profiles reveal the point where performance degrades non-linearly. Scale-out strategies (adding instances) are common but add complexity.

**Availability:** Calculated from MTBF and MTTR: Availability = MTBF / (MTBF + MTTR). "Five nines" (99.999%) allows only about 5 minutes of downtime per year. Challenges include defining what "available" means and the gap between observed and actual availability.

**Security:** Measured through proxy measures: static code analysis, dynamic analysis (penetration testing), and infrastructure scanning. Weight findings by risk (likelihood x impact). Common problems include environment inconsistency and false positives.

### Getting Started and Pitfalls

Woods recommends: start small, measure something that matters, act on what you measure, start early, make measurement visible, and make it continuous. Common pitfalls: focusing on mechanisms rather than measurements, choosing easy over important metrics, not taking action, prioritizing accuracy beyond usefulness, and measuring too much.

---

## Chapter 8: Progressing from Metrics to Engineering -- Neal Ford

Ford explains how metrics become engineering practices through automation and fitness functions, with detailed code-level case studies.

### From Metrics to Fitness Functions

A fitness function provides "objective evaluation criteria for architecture characteristics." The definition contains three elements: architecture characteristics (the "-ilities"), objective evaluation criteria (must be measurable), and any mechanism (testing libraries, performance monitors, chaos engineering). A metric becomes engineering when it is applied automatically on every code change through CI.

### Case Study: Coupling with ArchUnit

Ford demonstrates fitness functions for layered architecture using ArchUnit in Java. A simple test defines layers (Controller, Service, Persistence) and specifies access rules. When wired into CI, this prevents layer violations on every commit -- transforming passive architectural documentation into proactive governance. For microservices, where no off-the-shelf tool validates inter-service communication, custom fitness functions can parse service call logs to verify rules.

### Case Study: Zero-Day Security Check

The Equifax breach illustrates automated governance. If every project has a deployment pipeline with a security team slot, a zero-day vulnerability announcement triggers a fitness function across all projects checking for the vulnerable framework version. Projects running the vulnerable version fail the build immediately.

### Case Study: Fidelity Fitness Functions with GitHub's Scientist

GitHub's Scientist tool enables safe system replacement. When replacing old merge code, GitHub wrapped both implementations: old code always executed (serving users), new code ran in parallel for 1% of requests with result comparison. Over four days, more than 10 million experiments ran, providing high confidence before the old code was removed.

Ford warns against overusing fitness functions -- they should codify important (but not urgent) principles. Citing Gawande's *Checklist Manifesto*, he frames them as automated checklists preventing important principles from being skipped under pressure.

---

## Chapter 9: Using Software Metrics to Ensure Maintainability -- Alexander von Zitzewitz

This chapter provides an in-depth catalog of specific metrics for measuring code quality, coupling, and maintainability, with detailed formulas and threshold recommendations.

### Entropy and Cyclic Dependencies

The biggest enemy of maintainability is structural entropy. Cycle groups grow continuously once they reach critical size -- "code cancer." Apache Cassandra exemplifies this: version 2 had a cycle group of about 450 files, version 3 grew to 900+, and version 4 reached 1,300+. On the package level, 102 of 113 packages were entangled in a single cycle group. Cycles prevent isolated testing, make code harder to understand, block modularization, and prevent component replacement. All cycles can be broken using Robert C. Martin's dependency inversion principle.

### Metrics for Coupling

**Average Component Dependency (ACD):** CCD divided by number of components. High ACD indicates tight coupling.

**Propagation Cost (PC):** CCD divided by n-squared. Represents the percentage of components potentially affected by an average change. Benchmarks: mid-sized systems (500-5,000 components), PC over 20% is concerning, over 50% indicates serious cycle group issues. Large systems (5,000+), even 10% is concerning.

**Cyclicity and Relative Cyclicity:** Cyclicity = square of cycle group elements. Relative Cyclicity normalizes this to a percentage. Having many small cycle groups produces much lower values than one large group.

**Structural Debt Index (SDI):** Measures effort to break all cycles: SDI = 10 * (links to cut) + sum of weights. Combined with Relative Cyclicity, provides both severity and fixing cost.

**Maintainability Level (ML):** Measures "verticalization" -- how well a system is organized into functional silos with hierarchical dependencies. Computed from levelized dependency graphs with penalties for large cycle groups. Well-designed systems score above 90; poorly structured ones score in the 20s.

### Metrics for Size and Complexity

- **Lines of Code (LoC):** Recommended threshold of 800 per file
- **Cyclomatic Complexity:** Error rates increase above 24; recommended threshold is 15. Modified version adds 1 per switch; extended adds 1 per && and ||
- **Indentation debt:** Maximum code indentation levels. Recommended threshold of 4. Surprisingly effective for spotting complex code
- **Number of Statements per method:** Recommended threshold of 100

### Change History Metrics

- **Number of Changes(d):** How often a file changes in d days -- identifies instabilities
- **Code Churn(d):** Lines added or removed in d days -- measures volatility
- **Number of Authors(d):** Different committers -- reveals knowledge monopolies and bus-factor risks

Software city visualizations (3D charts showing size, complexity, and change frequency) help spot refactoring hotspots at a glance. The Component Rank metric (adapted from Google's PageRank) identifies "popular" classes useful for new developers deciding where to start reading code.

### Golden Rules

Von Zitzewitz's six recommended rules: enforceable architectural model, zero package-level cycles, component cycles limited to 5, no code duplication, files under 800 LoC, and maximum indentation of 4 with Modified Cyclomatic Complexity under 15.

---

## Chapter 10: Measure the Unknown with GQM -- Michael Keeling

This chapter introduces the Goal-Question-Metric (GQM) approach for defining metrics when you do not know what to measure.

### The GQM Approach

Proposed by Victor Basili and David Weiss, GQM's core assumption is that to measure something well, you must understand why you are measuring it. The model is hierarchical: Goal (root) branches to Questions, which branch to Metrics, with Data as leaves. This creates traceability from any data point back to its purpose.

### Creating a GQM Tree

Goals describe purpose, object, issue, and viewpoint. Questions are operationally focused and evaluate progress. Metrics can be rubrics, Boolean values, statistical measures, or equations. After brainstorming, prune: focus on strong-signal, low-cost metrics; identify metrics answering multiple questions; include both positive and negative metrics; and prioritize data feeding high-value metrics.

### Case Study: The Team That Learned to See the Future

A team experienced an outage when a third-party "Foo Service" rate limit was exceeded. Using GQM, they defined metrics for earlier detection: API quota remaining, heartbeat checks, error rates, queue depth, and job processing time. This revealed architectural gaps (no traffic-less monitoring, unclear failure-handling responsibility) that they fixed. Nine months later, when the Foo Service had a 14-hour outage, the team detected it in 10 minutes, diagnosed it immediately, and informed users before anyone noticed. What would have been a critical incident became barely noteworthy.

### Running a GQM Workshop

GQM works as a collaborative workshop with 2-5 participants (technical and nontechnical). Steps: introduce ground rules, write the goal, brainstorm questions, brainstorm metrics, sanity-check the goal, identify data needs, prioritize, and reflect. Key hints: encourage creative thinking before worrying about practicality, look for metric reuse, and capture the GQM tree visually.

---

## Key Takeaways

### 1. Metrics Must Be Purpose-Driven
Every metric should trace back to a business goal or quality attribute. The GQM approach provides structured traceability from data collection to organizational purpose. Understanding the "why" behind metrics makes teams more likely to use and trust them.

### 2. Fitness Functions Transform Metrics into Engineering
A metric only becomes engineering when automated and continuously applied through CI/CD. Fitness functions convert passive measurements into proactive governance -- automated checklists that prevent architectural decay under schedule pressure.

### 3. Cyclic Dependencies Are the Primary Enemy of Maintainability
Multiple authors independently identify cyclic dependencies as the most damaging form of structural erosion. Cycle groups grow like "code cancer" and must be detected early. Zero tolerance for package-level cycles and strict limits on component-level cycles are the most impactful rules.

### 4. The Four DORA Metrics Are Foundational but Not Sufficient
Deployment frequency, lead time, change failure rate, and time to restore service provide a balanced view of throughput and stability. They must be complemented with domain-specific metrics, architecture quality metrics, and sociotechnical measures. Context determines which metrics are appropriate; teams should not be compared using the same metrics.

### 5. Architecture Quality Is Objectively Measurable
The Modularity Maturity Index, Maintainability Level, Propagation Cost, Relative Cyclicity, and Structural Debt Index provide quantifiable measures of architectural health. These can be tracked over time and integrated into CI builds as fitness functions.

### 6. Measurement Must Start Early and Continue Continuously
Waiting until production is too late. Measure during design (models), implementation (static analysis), and operation (runtime metrics). The continuous cycle of measure-decide-change-measure drives architectural evolution.

### 7. Context Matters More Than Benchmarks
No metric is universally applicable. Discover metrics that fit your context rather than copying others' dashboards. Trends are sometimes more important than absolute values. Metrics should be guides, not targets (Goodhart's Law).

### 8. Technical Metrics Connect to Business Outcomes
KPI Value Trees connect organizational KPIs to domain KPIs to technical metrics, creating alignment from strategy to engineering practice. Software architecture should be intentional and connected to organizational mission.

### 9. Start Small and Iterate
Start with a small set of important metrics, automate them, visualize them, and expand. The sweet spot is around 5-6 metric-based rules. For legacy systems, start with lenient thresholds and tighten progressively.

### 10. Automation and Tooling Are Essential
Tools like SonarQube, Sonargraph, ArchUnit, and custom fitness functions in CI pipelines make metrics-based governance practical. Manual collection is a starting point but not sustainable.

### 11. Sociotechnical Architecture Requires New Skills
Modern architects need facilitation, group dynamics, and business strategy skills. Visual collaboration techniques (EventStorming) bridge business and technology. Architecture decisions affect the social fabric of organizations.

### 12. Testability and Deployability Enable Evolution
Designing for testability naturally produces better architecture. Deployability through continuous delivery keeps systems releasable. Together, they provide the foundation for evolutionary architecture that adapts without accumulating crippling technical debt. The attributes of testable code are the same attributes that make code maintainable.
