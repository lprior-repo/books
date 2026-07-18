# Building Evolutionary Architectures (2nd Edition)

**Authors:** Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage
**Topic tags:** `#architecture` `#testing` `#general` `#evolutionary` `#fitness-functions`
**Language focus:** Language-agnostic; the source's example code is in Java, .NET, JSON Schema, GraphQL, SQL/PLSQL, Ruby, and Jupyter/Cypher. Go-applicable.
**Sources:** `markdown_output/Building Evolutionary Architectures 2nd edition/Building Evolutionary Architectures 2nd edition.md` · `summaries/Building_Evolutionary_Architectures_2nd_edition.md`

## TL;DR

An evolutionary architecture supports guided, incremental change across multiple dimensions.
Treat fitness functions — the architectural equivalent of unit tests — as the central mechanism for protected, automated governance.
Run them in deployment pipelines, decide their cadence and scope deliberately, and let them enforce appropriate coupling, controlled reuse, and evolutionary data practices.
Pair them with structural decisions (connascence, architectural quantum, contracts, data mesh) and a team topology built around business capability and the Inverse Conway Maneuver.
Avoid the well-known antipatterns (Last 10% trap, Vendor King, leaky abstractions, Inappropriate Governance, Reporting Atop the System of Record, snowflake servers) and treat evolvability as one architectural characteristic among others, not a universal good.

### Source-Coverage Boundary

- Use the book's fitness-function categories, connascence scale, architectural quantum definition, Expand/Contract, LMAX, LCOM, Chidamber & Kemerer, and Scientist case studies by name.
- Do not attribute a named **"change velocity"** model to this book; cycle time is the book's velocity proxy.
- Use the book's distinction between **parallel run** and **dark launching** under the Strangler Fig and canary-release cases, both cited from the source.
- The book labels change data capture implicitly through event-driven architecture and double-writing in the Strangler Fig concurrency case study; the **change data capture** phrase itself is not used as a named pattern in the source.

---

## Best Practices by Topic

### 1. Define Evolutionary Architecture as Guided, Incremental, and Multidimensional

**Principle:** A software architecture is evolutionary when it supports *guided*, *incremental* change across *multiple dimensions*.

**Do:**

- Separate the three parts of the definition: *guidance* (what "good" means), *incremental* (small verifiable steps), and *dimensions* (technical, data, security, operational/system).
- Treat evolvability as a meta-characteristic that protects the other "-ilities."
- Identify all dimensions that the project must protect before designing fitness functions.
- Build the deployment pipeline at project inception so incremental change is the default.
- Use the term "architecture characteristics" (synonymous with nonfunctional requirements, system quality attributes, cross-cutting requirements) without forcing a vocabulary change.
- Plan for the "no useless architecture" principle: design for the problem's actual size and leave the bigger box empty until the project demands it.

**Don't:**

- Don't reduce evolution to incremental change; without guidance, evolution becomes reaction.
- Don't assume one team owns the whole picture; architecture choices virtually always require collaboration.
- Don't pre-commit to a particular architecture style before understanding the dimensions; every style is a starting point that grows to look like no other.
- Don't treat "evolvability" as a synonym for "adaptable"; adaptation piles on; evolution makes fundamental change.

**Core quote:**

> "An evolutionary software architecture supports *guided*, *incremental* change across *multiple dimensions*."

**Dimensional checklist:**

- Technical: frameworks, libraries, languages.
- Data: schemas, table layouts, optimization plans.
- Security: policies, guidelines, scanning tools.
- Operational/System: physical/virtual infrastructure, server clusters, cloud resources.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Evolving Software Architecture"; "Guided Change"; "Incremental Change"; "Multiple Architectural Dimensions"*

---

### 2. Treat Fitness Functions as the Core Mechanism

**Principle:** An architectural fitness function is *any mechanism that provides an objective integrity assessment of some architectural characteristic(s)*.

**Do:**

- Use a fitness function whenever a characteristic can be evaluated objectively (pass/fail, threshold, range, set inclusion, correlation ID reconciliation).
- Make the test for fitness function trivial: would an architect willingly stake a decision on it? If yes, the measure is objective.
- Write the function from the *outcome*, not the *implementation*: pick the answer first, choose the tool later.
- Allow the "function" to be a manual stage in the pipeline when automation is impossible (legal review, exploratory testing, accounting audit).
- Be willing to glue 10–20 lines in a scripting language when no off-the-shelf tool exists.

**Don't:**

- Don't write "all tests are fitness functions." Only tests that verify an *architectural characteristic* count.
- Don't require the function to be code; the function part of the name is mathematical, not syntactic.
- Don't use a monitor as a fitness function unless the architect has defined an objective threshold that triggers an alarm.
- Don't demand that one number summarize the entire architecture; precise, unambiguous conversation about each function is the goal.

**Tooling buckets for fitness functions:**

- Monitors (DevOps / operational).
- Code metrics (unit tests that encode architecture criteria).
- Chaos engineering.
- Architecture-testing frameworks (ArchUnit, NetArchTest).
- Security scanning (SCA, SAST, dependency CVE checks).
- Synthetic transactions.
- ADRs and BDD scenarios as documentation of the rule.

**Definition text:**

```
An architectural fitness function is any mechanism that provides
an objective integrity assessment of some architectural
characteristic(s).
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "What Is a Fitness Function?"; "Outcomes Versus Implementations"*

---

### 3. Classify Every Fitness Function on Six Axes

**Principle:** Every fitness function lives in the same six-dimensional category space; classify yours explicitly so reviewers know what they are buying.

**Do:**

- Tag every function with scope, cadence, result type, invocation mode, proactivity, and coverage.
- Choose **atomic** for single-context, single-characteristic checks (most CI tests).
- Choose **holistic** for cross-context, multi-characteristic checks (caching + freshness, fault tolerance + latency, message volume + endpoint reliability).
- Choose **triggered** when one well-defined event can launch the check (CI run, deployment, commit).
- Choose **continual** when only continuous observation in production can answer (response-time SLO, synthetic transaction).
- Choose **temporal** when calendar-driven prompts make sense (encryption-library CVE refresh, "break upon upgrade" for back-ported features, framework major-version nudges).
- Choose **static** for fixed thresholds, **dynamic** when the threshold depends on real-world context (acceptable response time *given* concurrent users).
- Choose **automated** whenever possible; explicitly mark manual stages when the organization cannot automate yet.
- Mark **intentional** functions at project inception; budget time to add **emergent** ones at every architectural stress point.
- Treat domain tests as separate artifacts even when the framework is the same; fitness functions answer a different question.

**Don't:**

- Don't deploy a fitness function without naming it on each axis.
- Don't claim a monitor is a fitness function; the *threshold* is what makes it one.
- Don't make a synthetic transaction without flipping the synthetic flag in the last step; build a fitness function to verify the flag.
- Don't pack architectural fitness functions into the domain test pipeline; noisy failures will defeat both.
- Don't use a 100% pass rate against zero as the only definition of "good."

**Atomic vs holistic example:**

- Atomic: "no cycles between packages" (ArchUnit slices test).
- Holistic: caching passes the scalability fitness function, but enabling caching makes data 40s stale, which fails the 30s-freshness security test. The combined function is what catches it.

**Synthetic transaction flag fitness function:**

- Synthetic transactions follow the normal path with a flag; the last step inspects the flag and does not commit.
- The fitness function: any annotated synthetic-transaction entry must have the flag set; otherwise alert.

**Continual fitness function rule:**

> "A monitoring tool in which the architect has created an alarm for deviations outside the objective measure of the metric converts the mere use of monitors into a fitness function."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Categories"; "Scope: Atomic Versus Holistic"; "Cadence"; "Synthetic Transactions"; "Result: Static Versus Dynamic"; "Invocation: Automated Versus Manual"; "Proactivity: Intentional Versus Emergent"; "Coverage"*

---

### 4. Choose Triggered or Continual With a Reason

**Principle:** Triggered and continual functions both implement the same outcome, but the cost and value differ; pick the one whose trade-off matches the consequence of a violation.

**Do:**

- Use triggered functions for cheap, isolated checks that a CI server can run.
- Use continual functions for security or compliance issues where a day's lag is unacceptable.
- Add runtime overhead (monitors, message queues) only when the cost of violation justifies it.
- Use log-based, reactive functions for structural governance that does not require immediate reaction.
- Implement continual versions through monitors that broadcast who a service is calling, or through async message queues where each service publishes collaboration messages.

**Don't:**

- Don't use triggered functions for security violations; the lag is too long.
- Don't use continual functions for low-severity structural rules; the runtime cost is wasted.
- Don't pick a cadence in isolation from the consequence of the failure.

**Microservices orchestration example:**

- Architecture: orchestrator holds workflow state; domain services must not bypass it.
- Triggered (reactive) version: deployment pipeline runs a Ruby/Python script that harvests 24 hours of logs and raises on any service-to-service call.
- Continual version: each service exposes a port broadcasting calls; a utility service monitors and reacts immediately.
- Trade-off: reactive has no runtime overhead but lags; continual catches violations at the cost of operational drag.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Triggered or Continuous?"; "Communication Governance in Microservices"*

---

### 5. Use the Deployment Pipeline as the Definitive Test of Releasability

**Principle:** If the deployment pipeline passes, the system is releasable; no further work is required.

**Do:**

- Define pipeline stages that map to architecture characteristics: commit, acceptance, security/compliance, performance, deployment.
- Treat fan-out + fan-in as the default for parallel verification: run old-and-new state, multiple contracts, and varied scenarios concurrently.
- Use feature toggles to decouple deployment from release, and clean up toggles aggressively.
- Use synthetic transactions (with a flag) to verify behavior in production.
- Include manual stages inside the pipeline so they appear as bottlenecks and become decision points at the last responsible moment.
- Track cycle time as a fitness function: evolution speed is proportional to cycle time (v ∝ c).

**Don't:**

- Don't pretend continuous delivery and continuous deployment are the same; continuous delivery has a manual gate, continuous deployment does not.
- Don't keep a "trunk"-only pipeline; deployment-pipeline rigor still applies.
- Don't use old feature flags; the Knight Capital / PowerPeg lesson is that stale toggles cost $400M in 45 minutes.
- Don't track only lead time; lead time includes estimation and prioritization, which are subjective. Track cycle time from work start to production.

**PenultimateWidgets invoicing pipeline stages:**

- Stage 1: Replicate CI.
- Stage 2: Containerize and deploy.
- Stage 3: Execute atomic fitness functions (scalability, security penetration, auditability metrics).
- Stage 4: Execute holistic fitness functions (consumer-driven contracts, integration scalability).
- Stage 5a: Security review (manual).
- Stage 5b: Audit (manual).
- Stage 6: Deploy to production.

**Cycle-time fitness function example:**

- Goal: keep cycle time under four hours.
- Implement as an atomic, process-based fitness function in the deployment pipeline.
- When the threshold fires, treat it as the last responsible moment: keep the verifications, or accept slower cycle time deliberately.

**Quote:**

> "Cycle time is therefore a critical metric in evolutionary architecture projects—faster cycle time implies a faster ability to evolve."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Engineering Incremental Change"; "Deployment Pipelines"; "Case Study: Adding Fitness Functions to PenultimateWidgets' Invoicing Service"; "Pitfall: Lack of Speed to Release"*

---

### 6. Detect Component Cycles with ArchUnit

**Principle:** Cyclic dependencies defeat reuse and create the Big Ball of Mud; detect and prevent them with an atomic fitness function.

**Do:**

- Define a fitness function that checks for cycles at the package or slice level.
- Wire it into the build so auto-imports cannot quietly create a cycle.
- Make the rule language-like by using Hamcrest matchers inside ArchUnit.

**Don't:**

- Don't rely on developer discipline; modern IDE auto-imports create cycles without warning.
- Don't accept the cycle as a refactoring opportunity; the fitness function is cheaper than the cleanup.
- Don't forget to scope the rule (e.g., per bounded context, per feature).

**ArchUnit cycle test (verbatim from the source):**

```
public class CycleTest {
 @Test
 public void test_for_cycles() {
  slices().
  matching("com.myapp.(*)..").
  should().beFreeOfCycles()
 }
}
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "What Is a Fitness Function?"; "ArchUnit"*

---

### 7. Express Coupling, Abstractness, and Distance in Fitness Functions

**Principle:** Quantify structure with Ca, Ce, abstractness, instability, and distance from the main sequence; encode the rules that matter.

**Do:**

- Calculate Ca and Ce for every significant package and component.
- Plot abstractness and instability; flag the zone of uselessness and the zone of pain.
- Use JDepend, IntelliJ dependency matrix, SonarQube, NDepend, JArchitect, or Structure101.
- Use the formulas from the book, not approximations:

**Equations (verbatim):**

- Abstractness: A = Σm_a / (Σm_c + Σm_a)
- Instability: I = C_e / (C_e + C_a)
- Normalized distance from the main sequence: D = |A + I − 1|

**Don't:**

- Don't optimize for zero coupling; components must interact.
- Don't trust a single number; look at A and I together (low I may be stable or rigid — concrete elements tell you which).
- Don't let the cycle metric stagnate; raise the bar over time as the codebase improves.

**Cycle formula for refactoring target:**

- The component with the largest D from the main sequence is the refactoring target.
- Identify drivers (long methods, duplication), use refactoring tools to extract.
- Watch the zone of uselessness (high A, high I — over-abstract, hard to use).
- Watch the zone of pain (low A, low I — concrete implementation, brittle, hard to maintain).

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Afferent and Efferent Coupling"; "Abstractness, Instability, and Distance from the Main Sequence"*

---

### 8. Lock the Direction of Package Imports

**Principle:** Use a unit test (and JDepend's API) to enforce the direction packages may depend on.

**Do:**

- Define allowed package-to-package dependencies as a constraint.
- Run the check on every commit.
- Treat a violation as a build failure, not a code-review note.

**Don't:**

- Don't rely on a wiki page describing layered architecture; nothing enforces it.
- Don't punish developers for breaking the rule; let the build teach the rule.
- Don't skip the rule for "tests" or "examples" unless you mean it.

**JDepend direction test (verbatim from the source):**

```
public void testMatch() {
 DependencyConstraint constraint = new DependencyConstraint();
 JavaPackage persistence = constraint.addPackage("com.xyz.persistence");
 JavaPackage web = constraint.addPackage("com.xyz.web");
 JavaPackage util = constraint.addPackage("com.xyz.util");
 persistence.dependsUpon(util);
 web.dependsUpon(util);
 jdepend.analyze();
 assertEquals("Dependency mismatch",
 true, jdepend.dependencyMatch(constraint));
}
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Directionality of Imports"*

---

### 9. Herd Cyclomatic Complexity Instead of Declaring War

**Principle:** Use cascading thresholds to gradually tighten complexity limits rather than blocking merges on day one.

**Do:**

- Treat <10 as the absolute upper bound; aim for <5.
- Use Crap4j to combine complexity with code coverage.
- Recognize that TDD naturally produces smaller, less complex methods.
- Distinguish essential complexity (algorithm) from accidental complexity (sloppy code).
- Apply a cascading threshold: warning today, error after a grace period.

**Don't:**

- Don't set an absolute threshold the codebase will fail on day one; nobody will keep the rule.
- Don't assume a single CC number distinguishes "fine" from "bad"; use multiple thresholds.
- Don't forget the higher-CC tolerance for genuinely hard algorithms.

**Cyclomatic complexity formula (verbatim):**

- Single function: CC = E − N + 2
- Multiple connected components: CC = E − N + 2P

**CC example (verbatim):**

```
public void decision(int c1, int c2) {
 if (c1 < 100)
 return 0;
 else if (c1 + C2 > 500)
 return 1;
 else
 return -1;
}
```

- CC for this function is 3 (3 − 2 + 2).

**Thresholds from the source:**

- Industry: under 10 acceptable, under 5 ideal.
- Crap4j thresholds: CC above 50 cannot be rescued by coverage.
- Real-world ceiling: 800 (single C function Neal encountered) — the cautionary warning sign.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Cyclomatic Complexity and 'Herding' Governance"; "What's a Good Value for Cyclomatic Complexity?"*

---

### 10. Detect Open-Source License Changes with a Small Fitness Function

**Principle:** Track each open-source license file by location, contents, and version; raise on change so legal can approve before the build proceeds.

**Do:**

- Store each dependency's license path and contents (or hash) alongside its version.
- On a new version, pull the new license file and compare.
- Raise a build failure and notify legal on mismatch.
- Treat detection as automated; treat approval as manual.

**Don't:**

- Don't assume license terms are stable; UI libraries have changed them historically.
- Don't let a tool detection lapse; one stale update is enough to re-expose the company.
- Don't use detection as a substitute for legal review; the architect's job is to notify, not to interpret.

**License-tracker fitness function (steps from the source):**

1. Note the location of each license file in a database.
2. Save contents (or hash) with the library version.
3. When a new version is detected, pull the license file, compare to the saved version, fail the build on mismatch, and notify legal.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Legality of Open Source Libraries"*

---

### 11. Apply ArchUnit Beyond Cycle Detection

**Principle:** Express layered architecture, package wiring, class dependencies, inheritance, and annotations as ArchUnit fitness functions; they are the executable analog of governance wikis.

**Do:**

- Use the `noClasses()…should().dependOnClassesThat()` form to forbid package wiring.
- Use `classes()…should().onlyHaveDependentClassesThat()` to allow specific package access.
- Use `classes().that().haveNameMatching(...)` for class-level coupling.
- Use inheritance rules to bind implementation names to contracts (e.g., `Connection` suffix).
- Use annotation rules to constrain usage (e.g., only `@Transactional` classes can touch `EntityManager`).
- Use the layered-architecture DSL with `.layer(...).definedBy(...)` and `.whereLayer(...).mayNotBeAccessedByAnyLayer()`.
- Combine ArchUnit with Hamcrest matchers for human-readable assertions.

**Don't:**

- Don't keep layered architecture in a wiki while developers violate it daily.
- Don't confuse "no cycles" with "no coupling"; allow permitted coupling and forbid only what is forbidden.
- Don't write the rule once and forget it; the ArchUnit rule must move with the architecture.

**Layered-architecture fitness function (verbatim from the source):**

```
layeredArchitecture()
 .consideringAllDependencies()
 .layer("Controller").definedBy("..controller..")
 .layer("Service").definedBy("..service..")
 .layer("Persistence").definedBy("..persistence..")
 .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
 .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
 .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

**Package wiring rules (verbatim from the source):**

```
noClasses().that().resideInAPackage("..source..")
 .should().dependOnClassesThat().resideInAPackage("..foo..")
```

```
classes().that().resideInAPackage("..foo..")
 .should().onlyHaveDependentClassesThat()
 .resideInAnyPackage("..source.one..", "..foo..")
```

**Class dependency rule (verbatim from the source):**

```
classes().that().haveNameMatching(".*Bar")
 .should().onlyHaveDependentClassesThat().haveSimpleName("Bar")
```

**Inheritance rule (verbatim from the source):**

```
classes().that().implement(Connection.class)
 .should().haveSimpleNameEndingWith("Connection")
```

**Annotation rule (verbatim from the source):**

```
classes().that().areAssignableTo(EntityManager.class)
 .should().onlyHaveDependentClassesThat().areAnnotatedWith(Transactional.class)
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "ArchUnit"*

---

### 12. Lint Every Ecosystem for Code Governance

**Principle:** Linters carry most of the governance load for ecosystems where ArchUnit and NetArchTest are unavailable; the rule is the rule regardless of tool.

**Do:**

- Use ESLint for JavaScript/ECMAScript; Cpplint for C++; staticcheck for Go; sql-lint for SQL.
- Write custom plug-ins for the specific governance rules the team needs.
- Wire lint rules into the same pipeline as tests.

**Don't:**

- Don't assume a turnkey ArchUnit equivalent exists for every language.
- Don't skip lint configuration in monorepos because the cost compounds.
- Don't argue linter rules with linters; let the build decide.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Linters for Code Governance"*

---

### 13. Govern Microservice Communication With a Log-Based Fitness Function

**Principle:** When no off-the-shelf governance tool exists for a distributed architecture, build a small fitness function that harvests logs in a common format.

**Do:**

- Mandate a common log format with service name, username, IP, correlation ID, timestamp, duration, and method name.
- Write a Ruby/Python script that parses 24 hours of logs and validates the allowed communication pattern.
- Use this in places where the cost of monitors or message queues is unjustified.

**Don't:**

- Don't try to build a "proactive" monitor for governance that has no immediate consequence; use a reactive daily-cycle function instead.
- Don't depend on log records you don't actually write; mandate the format first.
- Don't assume the source code emitting the log is correct; pair this with a fitness function that validates log format.

**Sample log format (verbatim from the source):**

```
["OrderOrchestrator", "jdoe", "192.16.100.10", "ABC123",
 "2021-11-05T08:15:30-05:00", "3100ms", "updateOrderState()"]
```

**Log-based check (Ruby, verbatim from the source):**

```
list_of_services.each { |service|
 service.import_logsFor(24.hours)
 calls_from(service).each { |call|
 unless call.destination.equals("orchestrator")
 raise FitnessFunctionFailure.new()
 }
 }
}
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Communication Governance in Microservices"*

---

### 14. Count Messages or Use Correlation IDs to Verify Reliability

**Principle:** For orchestrated workflows where dropped messages matter, pick a holistic fitness function that fits the operation, not just the easiest one.

**Do:**

- Use the container-instrumentation approach when service-level reliability is enough: count incoming vs. outgoing messages.
- Use correlation IDs when end-to-end reliability matters and you can carry state through the workflow.
- Visualize the service-level-indicator data in a real dashboard so missing messages are obvious.

**Don't:**

- Don't pick the container-count approach if the requirement is workflow-level; you will miss workflow losses.
- Don't pick correlation IDs if you cannot maintain the state across the entire workflow.
- Don't accept "it depends" as the end of the analysis; document the trade-off.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Choosing How to Implement a Fitness Function"*

---

### 15. Embrace the Simian Army as a Holistic Fitness Function

**Principle:** Treat resilience as a continuous fitness function that runs against the live system, not a scheduled test.

**Do:**

- Use Chaos Monkey to inject random faults.
- Use Chaos Gorilla to take out an entire data center.
- Use Chaos Kong to take out an entire availability zone.
- Use Doctor Monkey to check service health (CPU, disk).
- Use Latency Monkey to stress latency specifically.
- Use Janitor Monkey (now Swabbie) to garbage-collect orphaned services.
- Use Conformity Monkey to verify REST endpoint conformance.
- Use Security Monkey to scan for open debug ports, missing auth, etc.
- Replace deprecated monkeys with modern equivalents (Swabbie for Janitor Monkey).

**Don't:**

- Don't run chaos engineering only on a schedule; the value is the continual stress.
- Don't confuse chaos engineering with load testing; chaos injects faults, load adds volume.
- Don't skip monitoring the results; inject only what you can detect.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Chaos Engineering"*

---

### 16. Treat Enterprise Architects as Builders of Enterprise Fitness Functions

**Principle:** Enterprise architects provide guidance and enterprise-wide fitness functions, not technology choices for individual services.

**Do:**

- Codify platform choices through shared service templates and platform teams.
- Define cross-cutting fitness functions (security, scalability, auditability) at the enterprise level.
- Use the role to carve out bounded contexts inside existing integration architectures.
- Carve the role as "evolutionary architect" inside the team when the formal enterprise architect role is missing.

**Don't:**

- Don't dictate implementation details; that is the domain architect's job.
- Don't try to be the Frozen Caveman: avoid irrationally refusing change because of an old incident.
- Don't ignore "you build it, you run it" — give domain teams operational ownership.

**Frozen Caveman definition:**

- Architect who always reverts to a pet irrational concern for every architecture (e.g., "what if we lose Italy?").
- Caused by a single bad past experience that has become an inflexible decision rule.
- Antidote: keep risk assessment realistic; distinguish genuine from perceived technical risk.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Enterprise Architecture"; "Frozen Caveman Antipattern"; "Carving Out Bounded Contexts Within Existing Integration Architecture"*

---

### 17. Build Fitness Functions as Experimental Media

**Principle:** Use fitness functions to answer architectural questions empirically rather than to enforce rules from above.

**Do:**

- Build fitness functions to test hypotheses (UDP loss, dependency security, concurrency, fidelity).
- Use a Mock Service to simulate traffic and measure processing correctness.
- Use New Relic queries to derive real production call rates before sizing the auto-scaling factor.
- Treat each fitness function as both a measurement and a continuing guardrail.

**Don't:**

- Don't trust estimates over measurements; build the fitness function to verify the estimate.
- Don't hide the methodology of a fitness function; transparency builds trust.
- Don't treat "always trust 300 req/sec" as more authoritative than the actual measured peak.

**UDP communications case study (from the source):**

- Custom monitoring tool: 40% of messages lost at high scale.
- Mock Service simulated expected traffic; analytics tool processed the JSON.
- Outcome: replaced the custom tool with a standard implementation.

**Security-dependencies case study (from the source):**

- Library dependency list scanned in CI against a real-time block list.
- Alert raised on any project using an affected library.

**Concurrency case study (from the source):**

- Strangler Fig replacement microservice, double-writing strategy with legacy source of truth.
- Initial estimate: 120 req/sec. Measured peak: 1,200 req/sec.
- Auto-scaling factor updated accordingly.

**Fidelity fitness function:**

- Side-by-side comparison of old and new system.
- Side effect: discovered undocumented data sources in the legacy system.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Fitness Functions as Experimental Media"*

---

### 18. Verify API Consistency in the Build

**Principle:** Treat API design and API operation as fitness functions that run on every change.

**Do:**

- Stage 1: Validate the new OpenAPI specification with Spectral and OpenAPI.Tools.
- Stage 2: Publish the spec to a sandbox for functional testing.
- Stage 3: Use Pact (or other consumer-driven-contract tooling) to verify integration with each consumer.
- Stage 4: Deploy under a feature toggle that controls exposure to users.
- Stage 5: Operate continuous fitness functions and monitors in production.

**Don't:**

- Don't design APIs in a wiki and assume they will be honored.
- Don't allow changes to bypass consumer verification.
- Don't let A/B testing or canary releases replace contractual verification; use both.

**Consumer-driven contract principle:**

- Consumers write tests that capture what they need from the provider.
- Provider runs those tests and commits to keep them passing.
- Provider can evolve in any way that does not break the consumer tests.
- Provider can run the union of all consumer tests as an engineering safety net.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Validating API Consistency in an Automated Build"*

---

### 19. Use the Scientist Framework for Refactor-With-Confidence

**Principle:** GitHub's Scientist runs old and new code side by side, returns the old result, and logs the difference.

**Do:**

- Use Scientist for high-impact refactors where the new implementation must replicate the old behavior.
- Configure the percentage of traffic that runs the new path (1% in the GitHub case).
- Return the result of the *use* block (the control) always; log mismatches from the *try* block (the candidate).
- Compare results, swallow exceptions, randomize order, and measure durations.
- Run the experiment long enough to cover all relevant code paths.

**Don't:**

- Don't expose exceptions from the new path to end users.
- Don't show users the new behavior until the experiment is complete.
- Don't remove the old code path before the experiment has run long enough to be confident.

**Scientist setup (Ruby, verbatim from the source):**

```
require "scientist"
class MyWidget
 include Scientist
 def allows?(user)
  science "widget-permissions" do |e|
  e.use { model.check_user(user).valid? } # old way
  e.try { user.can?(:read, model) } # new way
  end # returns the control value
  end
end
```

**Merge-commit experiment (Clojure-flavored, verbatim from the source):**

```
def create_merge_commit(author, base, head, options = {})
 commit_message = options[:commit_message] || "Merge #{head} into #{base}"
 now = Time.current
 science "create_merge_commit" do |e|
 e.context :base => base.to_s, :head => head.to_s, :repo => repository.nwo
 e.use { create_merge_commit_git(author, now, base, head, commit_message) }
 e.try { create_merge_commit_rugged(author, now, base, head, commit_message) }
 end
end
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Architectural Restructuring While Deploying 60 Times per Day"; "Fidelity Fitness Functions"*

---

### 20. Document Fitness Functions with ADRs, BDD, and Jupyter

**Principle:** Tests are great documentation because they cannot lie; augment them with prose for non-developers.

**Do:**

- Use Architectural Decision Records (ADRs) to capture the *why* of each decision and the fitness functions that govern it.
- Use BDD tools (Cucumber, SpecFlow) to write fitness functions in natural language.
- Use Jupyter notebooks + jQAssistant + Neo4j to write graph-database-backed governance queries.
- Post fitness function results in a visible shared space so developers remember the rules.
- Number ADRs (001, 002, ..., 999) and walk them through Proposed → RFC → Accepted → Superseded.

**Don't:**

- Don't skip the human-readable explanation; non-developers need it too.
- Don't use only ADRs; pair them with executable tests.
- Don't leave a fitness function undocumented; the test alone is too cryptic for stakeholders.

**ADR structure (from the source):**

- Title.
- Status (Proposed, RFC, Accepted, Superseded).
- Context.
- Decision.
- Consequences.
- Governance.
- Notes.

**Cucumber natural-language rule (verbatim from the source):**

```
Feature: Is it Friday yet?
  Everybody wants to know when it's Friday
  Scenario: Sunday isn't Friday
    Given today is Sunday
    When I ask whether it's Friday yet
    Then I should be told "Nope"
```

**Cucumber Java mapping (verbatim from the source):**

```
@Given("today is Sunday")
public void today_is_sunday() {
 // Write code here that turns the phrase above into concrete actions
 throw new io.cucumber.java.PendingException();
}
@When("I ask whether it's Friday yet")
public void i_ask_whether_it_s_friday_yet() {
 // Write code here that turns the phrase above into concrete actions
 throw new io.cucumber.java.PendingException();
}
@Then("I should be told {string}")
public void i_should_be_told(String string) {
 // Write code here that turns the phrase above into concrete actions
 throw new io.cucumber.java.PendingException();
}
```

**Cypher query against jQAssistant (verbatim from the source):**

```
MATCH (e:Entity)<-[:CONTAINS]-(p:Package)
WHERE p.name <> "model"
RETURN e.fqn as MisplacedEntity, p.name as WrongPackage
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Documenting Fitness Functions"*

---

### 21. Defend Architecture Characteristics with Fitness Functions

**Principle:** Fitness functions are the guardrails no matter what the road is made of; they are the architectural equivalent of surgeon and pilot checklists.

**Do:**

- Use fitness functions to enforce design principles that developers used to forget under schedule pressure.
- Use them to set invariants at fragile integration points.
- Remember that they coexist with domain tests, not replace them.
- Treat them as checklists that prevent routine omissions.

**Don't:**

- Don't wield them as a stick; that produces resentment, not quality.
- Don't use them to replace architecture review; the architect still owns the design.
- Don't let fitness functions grow into bureaucracy; prune aggressively.

**Guardrail metaphor (verbatim from the source):**

> "Fitness functions are architecture characteristics guardrails, created by architects to prevent system rot and support evolving systems over time."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Fitness Functions as a Checklist, Not a Stick"*

---

### 22. Use Connascence as the Coupling Vocabulary

**Principle:** Page-Jones's connascence gives a richer language for coupling than "tight" or "loose"; use strength, locality, and degree to reason about refactors.

**Do:**

- Distinguish static (source-level) from dynamic (runtime) connascence.
- Prefer static connascence to dynamic where possible.
- Apply Page-Jones's three rules: minimize overall connascence via encapsulation; minimize the connascence that crosses encapsulation; maximize connascence within encapsulation.
- Apply Jim Weirich's Rule of Degree (convert strong connascence to weak) and Rule of Locality (weaker forms as distance increases).
- Recognize that strong connascence inside a component is acceptable; reject it across components.

**Don't:**

- Don't treat all connascence as equal; locality matters more than strength.
- Don't refuse to introduce a new abstraction just because connascence grows; sometimes the abstraction is worth it.
- Don't assume dynamic connascence is unmanageable; synthetic transactions and correlation IDs make it observable.

**Static connascence (weakest to strongest):**

- Connascence of Name (CoN): both use the same name.
- Connascence of Type (CoT): both use the same type.
- Connascence of Meaning (CoM) / Convention (CoC): both agree on the meaning of a value (e.g., `1` means true).
- Connascence of Position (CoP): both rely on positional ordering of arguments.
- Connascence of Algorithm (CoA): both must implement the same algorithm.

**Dynamic connascence:**

- Connascence of Execution (CoE): order of execution matters.
- Connascence of Timing (CoT): timing of execution matters (race conditions).
- Connascence of Values (CoV): several values must change together (transactions).
- Connascence of Identity (CoI): both reference the same entity.

**Connascence improvement example:**

- CoM (magic numbers) → CoN (named constant).
- CoP (positional arguments) → CoN (named parameters or DTOs).
- CoA (cryptographic hash duplicated) → CoN (shared hash library).

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Connascence"; "Connascence Properties"*

---

### 23. Treat Bounded Context as the Architectural Quantum

**Principle:** An architectural quantum is an independently deployable artifact with high functional cohesion, high static coupling, and synchronous dynamic coupling.

**Do:**

- Compute the quantum from static dependencies (OS, framework, database, broker).
- Treat any shared database as a single coupling point: all services using it are one quantum.
- Treat tightly coupled user interfaces as a single-quantum boundary.
- Choose micro-frontend patterns to keep UI elements loosely coupled.
- Make smaller quanta when you need faster change; bigger quanta when coordination cost dominates.
- Use DDD bounded context as the natural quantum boundary.

**Don't:**

- Don't claim a microservice is its own quantum if it shares a database with another service.
- Don't assume microservices are always smaller than the right quantum; size to the problem.
- Don't make quanta so small that orchestration cost dominates; coordination overhead grows with the number of quanta.

**Quantum rules from the source:**

- Independent deployment: monoliths are always a single quantum.
- High functional cohesion: keep related behavior together.
- High static coupling: the things inside the quantum must operate together.
- Database, OS, framework, message broker, container orchestrator = all part of the quantum's static coupling.
- A mediator pattern (orchestrator + DB) is always one quantum.
- A broker pattern can be one quantum (if all services share a DB) or many.
- Microservices with their own databases are the natural fit for multiple quanta.
- A tightly coupled UI can collapse microservices into one quantum.
- Micro-frontends restore quantum independence.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Connascence Intersection with Bounded Context"; "Architectural Quanta and Granularity"; "Independently Deployable"; "High Functional Cohesion"; "High Static Coupling"*

---

### 24. Navigate the Three Dimensions of Dynamic Quantum Coupling

**Principle:** Communication, consistency, and coordination are interlocking forces; choosing one tilts the others.

**Do:**

- Map every distributed workflow onto the three axes.
- Accept the gravitational pulls: transactionality is easier with sync + orchestrated; scalability comes from async + choreographed + eventual.
- Use the matrix-of-options technique: change one force, observe the impact on the others.
- Document the trade-off so reviewers see the same trade-off.

**Don't:**

- Don't pick communication, consistency, or coordination independently; they are coupled.
- Don't assume more sync is simpler; in distributed systems, async often wins on scalability.
- Don't promise atomicity in a fundamentally choreographed system; design for compensation.

**Combinations from the source:**

- Synchronous + atomic + orchestrated = high transactionality, low scale.
- Asynchronous + eventual + choreographed = high scale, harder consistency reasoning.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Dynamic Quantum Coupling"*

---

### 25. Design Contracts Across the Strict-to-Loose Spectrum

**Principle:** A contract is the format used by parts of an architecture to convey information or dependencies; pick the contract tightness that matches the coupling you can accept.

**Do:**

- Be conservative in what you send (don't ship more fields than needed).
- Be liberal in what you accept (validate only what you consume).
- Use versioning (internal or numbered) when a contract must break.
- Use loose contracts (JSON name/value pairs) where the system benefits from extreme decoupling.
- Use strict contracts (gRPC, JSON Schema) where call semantics mimic internal method calls.
- Add the consumer's name field only when the consumer needs it; avoid Stamp Coupling.

**Don't:**

- Don't add fields "just in case" — that is Stamp Coupling.
- Don't accept strict RPC for things that change frequently; the brittleness outweighs the type safety.
- Don't validate fields you don't use; that's accidental coupling.

**Strict JSON contract (verbatim from the source):**

```
{
 "$schema": "http://json-schema.org/draft-04/schema#",
 "properties": {
  "acct": {"type": "number"},
  "cusip": {"type": "string"},
  "shares": {"type": "number", "minimum": 100}
 },
 "required": ["acct", "cusip", "shares"]
}
```

**Loose name/value pair (verbatim from the source):**

```
{
 "name": "Mark",
 "status": "active",
 "joined": "2003"
}
```

**GraphQL example from the source (Wishlist vs Customer views):**

```
type Profile {
 name: String
}
type Profile {
 name: String, addr1: String, addr2: String, country: String
}
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Contracts"*

---

### 26. Recognize the Microservices Trade-offs

**Principle:** Microservices score highly on evolutionary criteria but introduce coordination, transactional, and data-partitioning challenges.

**Do:**

- Use the seven principles: model around business domain, hide implementation details, automate culture, decentralize, deploy independently, isolate failure, observe.
- Treat each service as a quantum candidate; check that the service owns its data.
- Use the Circuit Breaker pattern, bulkheads, and the Reactive Manifesto to manage failure isolation.
- Pick a service template to enforce consistency where the cost of polyglot proliferation would be too high.

**Don't:**

- Don't assume microservices are always the right answer; apply the "Why or Why Not" decision framework.
- Don't expose implementation details (especially database schemas) across service boundaries.
- Don't expect the monolith-to-microservices migration to be cheap; budget for transactional context breaking.

**Microservices case study (PenultimateWidgets):**

- Catalog page backed by microservices.
- Half-star rating added as a new version of the rating service.
- Original version remained available; calling services migrated at their own pace.
- Operations' "no traffic in window" rule automatically garbage-collected the old version.
- Architectural monitoring and routes between services were part of DevOps practice.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Microservices as an Evolutionary Architecture"*

---

### 27. Reuse Effectively (or Duplicate, on Purpose)

**Principle:** Effective reuse = abstraction + low volatility; when either is missing, duplication is often cheaper.

**Do:**

- Apply the "duplication is preferable to coupling" rule in microservices.
- Use orthogonal coupling (Sidecar, service mesh) for cross-cutting operational concerns.
- Use orthogonality for analytical data with the Data Mesh pattern.
- Use shared libraries (JAR, DLL) for high-abstraction, low-volatility code.
- Continuously evaluate shared components; remove them when they become bottlenecks.

**Don't:**

- Don't reuse a highly volatile component; the coupling overhead will outpace the savings.
- Don't "abstract all the things"; abstraction without need increases complexity and reduces usability.
- Don't let a reusable component become a bottleneck team.

**Reuse-effectiveness heuristic:**

- "The more reusable code is, the less usable it is."
- "Software reuse is more like an organ transplant than snapping together Lego blocks."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Reuse Patterns"; "Effective Reuse = Abstraction + Low Volatility"*

---

### 28. Use the Sidecar Pattern and Service Mesh for Orthogonal Operational Coupling

**Principle:** The Sidecar pattern (hexagonal/ports-and-adapters descendant) and service mesh decouple domain code from operational concerns.

**Do:**

- Use Sidecars to attach logging, monitoring, auth, and circuit breakers to each service.
- Combine Sidecars into a service mesh for unified operational governance.
- Use service mesh as a constraint on polyglot proliferation.
- Govern Sidecar presence with a fitness function.

**Don't:**

- Don't embed operational concerns (auth, monitoring) into domain libraries.
- Don't allow opt-out from the Sidecar; that defeats the consistency the mesh provides.
- Don't mistake a service mesh for a substitute for good operational practice; it amplifies good practice.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Sidecars and Service Mesh: Orthogonal Operational Coupling"; "Orthogonal Coupling"*

---

### 29. Build Data Mesh for Orthogonal Data Coupling

**Principle:** Apply the Sidecar/mesh idea to analytical data through data product quanta owned by domains.

**Do:**

- Treat data as a product with owners, success metrics, and contract.
- Use a self-serve data platform for declarative creation, discovery, and lineage.
- Apply computational federated governance: policies automated and embedded in each data product via sidecar.
- Distinguish source-aligned, aggregate, and fit-for-purpose data product quanta.
- Treat each DPQ as a cooperative quantum with its partner service.

**Don't:**

- Don't centralize data in a warehouse or lake; that violates domain ownership.
- Don't share schemas across DPQs; that's the data equivalent of shared database coupling.
- Don't reuse a single DPQ for both source-aligned and aggregation roles; pick the right type.

**Data Mesh principles:**

- Domain ownership of data.
- Data as a product.
- Self-serve data platform.
- Computational federated governance.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Data Mesh: Orthogonal Data Coupling"*

---

### 30. Evolve Schemas Alongside Code

**Principle:** Database schemas are abstractions; evolve them with tested, versioned, incremental migrations.

**Do:**

- Use migration tools (Flyway, Liquibase) to apply small delta scripts.
- Treat applied migrations as immutable; add a new migration rather than edit.
- Skip "undo" migrations in most projects; rebuild from earlier migrations when needed.
- Add fitness functions that check ORM mapping stays in sync with the schema.

**Don't:**

- Don't hand-edit production schemas.
- Don't edit an already-applied migration; the build is no longer reproducible.
- Don't depend on a single engineer to remember schema history; version it.

**Simple migration (verbatim from the source):**

```
CREATE TABLE customer (
 id BIGINT GENERATED BY DEFAULT AS IDENTITY (START WITH 1) PRIMARY KEY,
 firstname VARCHAR(60),
 lastname VARCHAR(60)
);
```

**Additive migration (verbatim from the source):**

```
ALTER TABLE customer ADD COLUMN dateofbirth DATETIME;
```

**Date-of-birth example with undo (verbatim from the source):**

```
ALTER TABLE customer ADD COLUMN dateofbirth DATETIME; --//@UNDO

ALTER TABLE customer DROP COLUMN dateofbirth;
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Evolving Database Design"; "Evolving Schemas"*

---

### 31. Use Expand/Contract for Shared-Database Migrations

**Principle:** When multiple applications share a database, schema changes need a transition phase.

**Do:**

- Pick the option that matches the legacy data and integrator situation.
- Use the database trigger approach when legacy data and integrators both exist.
- Use `SET UNUSED` and functional columns when drop is too expensive.
- After contraction, verify all dependencies moved to the new structure before dropping.

**Don't:**

- Don't make destructive changes without a transition phase.
- Don't assume integrators will migrate in your timeframe.
- Don't forget the functional column for backward-compatible read access.

**Three options from the source:**

- Option 1: No integration points, no legacy data — add new columns, drop the old one.
- Option 2: Legacy data, no integration points — add columns, backfill via `UPDATE`, drop the old one.
- Option 3: Legacy data and integration points — add a database trigger to keep both structures in sync.

**Option 3 trigger (verbatim from the source):**

```
CREATE OR REPLACE TRIGGER SynchronizeName
BEFORE INSERT OR UPDATE
ON Customer
REFERENCING OLD AS OLD NEW AS NEW
FOR EACH ROW
BEGIN
 IF :NEW.Name IS NULL THEN
  :NEW.Name := :NEW.firstname||' '||:NEW.lastname;
 END IF;
 IF :NEW.name IS NOT NULL THEN
  :NEW.firstname := extractfirstname(:NEW.name);
  :NEW.lastname := extractlastname(:NEW.name);
 END IF;
END;
```

**Post-contraction read-compatible column (verbatim from the source):**

```
ALTER TABLE CUSTOMER ADD (name AS
 (generatename (firstname,lastname)));
```

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Shared Database Integration"*

---

### 32. Treat Transactional Context as a Strong-Nuclear-Force Coupling

**Principle:** Transactional contexts bind quanta together more tightly than class-level coupling; respect them when choosing service boundaries.

**Do:**

- Recognize that transactions define the smallest practical granularity in heavily transactional domains.
- Prefer eventual consistency in distributed systems to escape 2PC.
- Use sagas and compensating transactions for cross-aggregate consistency.
- Make transactional boundaries visible in service design.

**Don't:**

- Don't try to build microservices over heavily transactional systems at fine granularity.
- Don't ignore transactions when sizing the quantum; they often define the granularity.
- Don't confuse class-level coupling with transactional coupling.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Two-Phase Commit Transactions"*

---

### 33. Choose Migration Granularity Deliberately

**Principle:** Start with a few larger services; iterate to finer granularity as coupling and coordination costs are understood.

**Do:**

- Identify service boundaries by business functionality, transactional boundaries, or deployment goals.
- Choose coarse service granularity first to reduce coordination problems.
- Detach services from the monolith incrementally.
- Add consumer-driven contracts to lock in integration behavior.
- Use service discovery early; even a simple proxy enables gradual migration.

**Don't:**

- Don't start with many small services; coordination cost dominates.
- Don't forget the UI; an anticorruption layer around the unified UI pays for itself.
- Don't accept monolith patterns (single DB, single deploy) under a microservices name; they are still monoliths.

**Heuristic from the source (Sam Newman):**

> "When migrating from a monolith, build a small number of larger services first."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Migration Steps"; "Migrating Architectures"*

---

### 34. Use LCOM to Decide Whether to Share, Split, or Duplicate

**Principle:** LCOM tells you whether a class ever was cohesive; if low, share or duplicate; if high, split first.

**Do:**

- Measure LCOM on shared classes before migration.
- Use ckjm or another Chidamber & Kemerer implementation.
- Treat high-LCOM as a signal to split before migration.
- Treat low-LCOM as a signal to keep shared (as a library) or duplicate.
- Reuse (JAR/DLL) or duplicate (per service) consciously.

**Don't:**

- Don't treat every shared class as a migration candidate.
- Don't duplicate a high-LCOM class across services; that duplicates the mess.

**Migration ordering from the source:**

- If LCOM is high (class lacks cohesion), split before migrating.
- If LCOM is low (class is cohesive), choose between shared library and duplication based on coupling cost.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Evolving Module Interactions"*

---

### 35. Follow the Six Guidelines for Building Evolutionary Architectures

**Principle:** Use the book's six guidelines to choose architectural moves that improve evolvability.

**Do:**

- **Remove needless variability:** prefer immutable infrastructure, declarative systems, rebuild from source.
- **Make decisions reversible:** blue/green deployments, feature toggles, canary releases, service routing.
- **Prefer evolvable over predictable:** accept unknown unknowns; prediction is impossible.
- **Build anticorruption layers:** isolate external dependencies behind interfaces; JIT-extract when needed.
- **Build sacrificial architectures:** prove the market before perfecting the architecture.
- **Mitigate external change:** internal repo, pull model, library hygiene, framework-vs-library distinction.

**Don't:**

- Don't freeze infrastructure; that reintroduces snowflake servers.
- Don't use permanent feature toggles for permanent customization; the technical debt compounds.
- Don't buy "the final, perfect" technology before validating the problem; that's the planning-horizons pitfall.
- Don't allow third-party changes to silently enter your builds; gate them through a pull model.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Guidelines for Building Evolutionary Architectures"*

---

### 36. Distinguish Frameworks from Libraries for Upgrade Strategy

**Principle:** Treat framework upgrades as push (forced) and library upgrades as pull (when needed).

**Do:**

- Update frameworks aggressively because they are tightly coupled and difficult to skip.
- Update libraries passively; upgrade when new functionality is needed.
- Prefer libraries over frameworks where possible.
- Track dependency metadata (provenance, vulnerability status) for supply-chain security.

**Don't:**

- Don't let frameworks fall more than two major versions behind; the upgrade pain grows non-linearly.
- Don't treat all dependencies the same; the engineering risk differs.
- Don't allow silent third-party changes; gate them.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Updating Libraries Versus Frameworks"*

---

### 37. Use the Strangler Fig Pattern With a Fidelity Fitness Function

**Principle:** Run new and old code side by side; return the old result, log the difference, remove the old code only when confidence is established.

**Do:**

- Use a proxy endpoint that routes by version.
- Keep the old and new versions alive while callers migrate.
- Use a fidelity fitness function (e.g., Scientist) to verify new behavior matches old.
- Decommission the old version only after the experiment has run long enough.

**Don't:**

- Don't force callers to migrate immediately.
- Don't expose users to the new behavior until confidence is established.
- Don't keep the old version alive forever.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Evolving PenultimateWidgets' Ratings"; "Fidelity Fitness Functions"*

---

### 38. Decide Where to Start Based on Organizational Maturity

**Principle:** Two paths exist for retrofitting evolutionary architecture: low-hanging fruit (safe early win) or highest value first (commitment signal).

**Do:**

- Use low-hanging fruit for skeptical organizations: pick a decoupled system, demonstrate the approach.
- Use highest-value-first for committed organizations: prove the approach on the most critical part.
- Add testing before restructuring: coarse functional tests scaffold the eventual architecture refactor.
- Fix infrastructure before architecture if the operation is blocking the architecture.
- Gather before/after metrics; demonstration defeats discussion.

**Don't:**

- Don't choose a starting point that is both high-effort and low-value.
- Don't start with the most important system if you cannot deliver a proof-of-concept quickly.
- Don't skip the testing step; the architecture refactor relies on test coverage.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Where Do You Start?"; "Low-Hanging Fruit"; "Highest Value First"; "Testing"; "Infrastructure"*

---

### 39. Use the LMAX Story for Fitness-Function-Driven Architecture

**Principle:** When a critical characteristic determines success, drive design with the fitness function.

**Do:**

- Define the fitness function first (transaction speed).
- Iteratively design the architecture to make the fitness function pass.
- Recognize mechanical sympathy: understand the layer below to optimize the layer above.
- Treat the fitness function as a continuing guardrail after the initial goal is met.

**Don't:**

- Don't expect the framework to give you the architecture.
- Don't assume context switches are free; measure them.
- Don't refuse to rewrite when mechanical-sympathy insight reveals the approach is wrong.

**LMAX discoveries (from the source):**

- Threads couldn't reach the throughput goal.
- Actor models didn't reach the goal.
- Context switches were the bottleneck.
- Single-thread + ring buffers ("input and output disruptors") reached 6M+ transactions/sec.
- Mechanical sympathy coined from Formula 1 racing.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Fitness Function-Driven Architecture"*

---

### 40. Recognize and Avoid the Major Pitfalls and Antipatterns

**Principle:** The book names explicit pitfalls and antipatterns; know them by name and avoid them in your designs.

**Technical-architecture pitfalls and antipatterns:**

- **Last 10% Trap and Low Code/No Code:** 80% works in 4GL/low-code; the next 10% requires hacks; the last 10% is impossible. Evaluate the *hardest* problem first, not the easiest.
- **Vendor King:** ERP centered as the architecture's universe. Treat vendor products as just another integration point behind an anticorruption layer.
- **Leaky Abstractions:** All nontrivial abstractions are leaky. Always fully understand at least one layer below the one you normally work in. Define invariants at fragile integration points as fitness functions.
- **Resume-Driven Development:** Choose the architecture for the problem, not the résumé.

**Incremental-change pitfalls and antipatterns:**

- **Inappropriate Governance:** One-size-fits-all standards fail in the DevOps era. Use "just enough" governance with three technology stacks (small/medium/large).
- **Lack of Speed to Release:** Slow release cadence breaks the v ∝ c relationship. Track cycle time as a fitness function.

**Business concerns:**

- **Product Customization pitfall:** Salespeople want infinite customization; it costs test and fitness-function budget. Realistically assess.
- **Reporting Atop the System of Record antipattern:** Don't share the OLTP DB with reporting. Use event streams to populate a denormalized reporting DB.
- **Excessively Long Planning Horizons pitfall:** Sunk-cost fallacy + unknown unknowns = disaster. Avoid technologies requiring significant up-front investment before feedback.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Evolutionary Architecture Pitfalls and Antipatterns"; "Technical Architecture"; "Incremental Change"; "Business Concerns"*

---

### 41. Use Conway's Law and the Inverse Conway Maneuver Deliberately

**Principle:** Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations (Conway, 1968).

**Do:**

- Use the Inverse Conway Maneuver: structure teams to match the target architecture.
- Build cross-functional teams covering architecture, business analysts, data, dev, design, operations, PM, testing.
- Keep teams small (Amazon's two-pizza rule, Hackman's n(n-1)/2 formula).
- Adopt "you build it, you run it" — full ownership prevents finger-pointing.
- Organize teams around business capabilities, not job functions.
- Balance cognitive load with business capabilities; consider stream-aligned, enabling, complicated subsystem, and platform team patterns.

**Don't:**

- Don't fight Conway's Law by maintaining technical silos while building domain architectures.
- Don't build large teams; at 14 members, there are 91 connections; at 50, 1,225.
- Don't pretend team structure doesn't affect architecture.

**Conway's law (verbatim from the source):**

> "Organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations."

**Two-pizza rule (verbatim):**

> "Each team is cross-functional, and they also embrace the philosophy of 'you build it, you run it,' meaning each team has complete ownership of their service, including operationalizing it."

**Team-size connection formula (verbatim):**

$$\frac{n(n-1)}{2}$$

**Team Topologies mapping (from the source):**

- Stream-aligned teams — flow of work from a business domain.
- Enabling teams — help stream-aligned teams overcome obstacles.
- Complicated subsystem teams — own part of the domain demanding significant expertise.
- Platform teams — provide an internal product to accelerate stream-aligned teams.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Don't Fight Conway's Law"; "Amazon's 'Two Pizza' Teams"; "Balance cognitive load with business capabilities"*

---

### 42. Build a Culture of Experimentation, Not Just Delivery

**Principle:** Successful evolution depends on small, frequent experiments; encourage kaizen, spike-and-stabilize, set-based development, and A/B testing.

**Do:**

- Bring ideas from outside (conferences, consultants).
- Practice kaizen (continuous improvement at the team level).
- Use spike solutions to learn fast, then stabilize.
- Allocate 20% time or hackathons for innovation.
- Use set-based development: prototype several approaches in a few days before committing.
- Connect engineers with end users.
- Use A/B testing for silent user experiments instead of pop-up surveys.

**Don't:**

- Don't be too busy delivering to experiment.
- Don't make spikes production code.
- Don't confuse opinions with data; run measurable experiments.
- Don't annoy users with pop-up surveys when behavior is observable.

**Edison quote (verbatim):**

> "The real measure of success is the number of experiments that can be crowded into 24 hours."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Culture"; "Culture of Experimentation"*

---

### 43. Decide When Evolutionary Architecture Is the Right Answer

**Principle:** Evolutionary architecture is not a universal good; choose it for the right reasons, and avoid it for the right reasons.

**Do — reasons to build evolutionary architecture:**

- Business change cycle has accelerated (competitive pressure).
- Scale challenges force decoupling (Amazon's monolith hit DB scale wall).
- Advanced business capabilities (A/B testing, hypothesis-driven development) require isolation.
- Cycle time is a business metric; treat it as a competitive advantage.

**Don't — reasons NOT to build evolutionary architecture:**

- Cannot evolve a Big Ball of Mud: rewrite is cheaper than refactor.
- Other architectural characteristics dominate (e.g., domain-specific architectures).
- Planning a sacrificial architecture (deliberate MVP to be replaced).
- Planning to close the business soon.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Why (or Why Not)?"; "Why Should a Company Decide to Build an Evolutionary Architecture?"; "Why Would a Company Choose Not to Build an Evolutionary Architecture?"*

---

### 44. Identify the Velocity of Change You Need

**Principle:** Cycle time is the leading indicator of evolution speed (v ∝ c); treat cycle time as a business metric and a fitness function.

**Do:**

- Track cycle time from work start to production.
- Set a threshold and treat breach as the last responsible moment for a decision.
- Use the formula v ∝ c to justify investments in cycle time.
- Treat a four-hour cycle time as the example fitness function.
- Connect cycle time to architectural quanta; smaller quanta tend to have shorter cycle times.

**Don't:**

- Don't rely on lead time (includes subjective activities).
- Don't treat "I will measure it someday" as a measurement.
- Don't let cycle time drift upward silently.

**Cycle-time equation (verbatim from the source):**

$$v \propto c$$

**Cycle-time interpretation:**

- v = velocity of change (how fast the architecture can evolve).
- c = cycle time (from developer start to production).
- The faster teams can release, the faster they can evolve.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Pitfall: Lack of Speed to Release"; "Cycle time as a business metric"*

---

### 45. Recognize Data Gravity and Inappropriate Data Entanglement

**Principle:** Data is the most common extra-architecture concern affecting evolution; treat it as a first-class design dimension.

**Do:**

- Treat data as part of the architecture, not a separate concern.
- Recognize transactional coupling as a quantum-binding force.
- Plan for shared database integration by using Expand/Contract.
- Replace triggers and stored procedures with application code using Expand/Contract and Strangler Fig.
- Use event streams for referential integrity where eventual consistency is acceptable.

**Don't:**

- Don't leave schemas unrefactored; the "add another join table" pattern obfuscates the real abstraction.
- Don't treat the database vendor as a strategic asset; recognize that the data team is the consumer.
- Don't couple reporting directly to the OLTP database.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Inappropriate Data Entanglement"; "Replacing Triggers and Stored Procedures"*

---

### 46. Use Parallel Run, Dark Launching, and the Strangler Fig for Migration

**Principle:** Replace legacy code incrementally with parallel runs that return the existing behavior, then transition routing.

**Do:**

- Run old and new code in parallel and return the old result (parallel run / Scientist).
- Deploy new code behind feature toggles and route a small percentage of users (dark launching / canary).
- Move callers to the new version at their own pace.
- Use a fidelity fitness function to confirm new behavior matches old.
- Decommission the old code only when no traffic remains.

**Don't:**

- Don't show users the new behavior during the experiment.
- Don't decommission the old code before traffic has fully migrated.
- Don't migrate the UI before the backend; build an anticorruption layer first.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Case Study: Evolving PenultimateWidgets' Ratings"; "Fidelity Fitness Functions"; "Strangler Fig pattern"*

---

### 47. Use Antidotes to External Change and "Considered Harmful" Patterns

**Principle:** Treat transitive dependency management as a strategic concern; gate it with a pull model.

**Do:**

- Use an internal repository that pulls external dependencies.
- Treat third-party changes as pull requests that your CI validates.
- Update frameworks aggressively; update libraries passively.
- Recognize that left-pad's removal broke the internet as a warning sign.
- Track supply-chain metadata with snyk, Dependabot, and equivalent tools.

**Don't:**

- Allow third parties to make breaking changes to your build silently.
- Treat transitive dependencies as "free."
- Use an "it works on my machine" workflow.

**Quote (verbatim from the source):**

> "Transitive dependency management is our 'considered harmful' moment."

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Mitigate External Change"; "The 11 Lines of Code That Broke the Internet"*

---

### 48. Combine Mechanics and Structure for a Real Architecture

**Principle:** Mechanics and structure reinforce each other; structure without mechanics is documentation; mechanics without structure is surveillance.

**Do:**

- Define dimensions to protect.
- Add fitness functions to deployment pipelines.
- Control coupling through connascence and bounded context.
- Treat data as an architectural dimension.
- Use contracts (Postel, internal versioning) and quantum-aware design.
- Wire team structure to architecture (Inverse Conway).
- Run experiments and use A/B testing.

**Don't:**

- Don't use one without the other; pipelines alone won't fix inappropriate coupling.
- Don't treat documentation as substitute for tests.
- Don't ship architecture without an engineering practice for change.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Summary" (Chapters 1–7)*

---

### 49. Apply the Future State: AI and Generative Testing

**Principle:** AI-based and generative fitness functions extend verification into territory unit tests cannot easily reach.

**Do:**

- Use AI-based fitness functions to detect anomalous behavior (e.g., near-simultaneous geographically distant transactions).
- Use generative testing to find edge cases in fuzz-style input domains.
- Track the maturity of these techniques; they complement, not replace, principled fitness functions.

**Don't:**

- Don't treat AI-based fitness functions as a substitute for principled ones.
- Don't expect generative testing to replace deterministic unit tests; it complements them.
- Don't use AI where a simple rule is sufficient.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "Future State?"; "Fitness Functions Using AI"; "Generative Testing"*

---

### 50. Close the Feedback Loop with Hypothesis-Driven Development and the Business Case

**Principle:** Evolutionary architecture supports advanced business capabilities only when the engineering practice is also in place.

**Do:**

- Use hypothesis-driven development: state the hypothesis, design the experiment, validate.
- Use A/B testing to validate with users, not surveys.
- Architect for side-by-side versions through intelligent routing.
- Sell the architecture in business terms: cycle time, A/B testing, hypothesis-driven development.
- Make cycle time a first-class business metric.

**Don't:**

- Don't gather formal requirements without testing assumptions.
- Don't annoy users with surveys when behavior is observable.
- Don't sell the architecture in technical terms; translate to business impact.

*Ref: Building_Evolutionary_Architectures_2nd_edition.md — "The Business Case"; "Hypothesis- and Data-Driven Development"*

---

## Anti-Patterns & Common Mistakes

- **Cycle-by-counter: "no cycles, ever":** Cycles inside a quantum are sometimes acceptable; cycles between quanta are the real antipattern. → *Fix:* Scope cycle fitness functions per quantum.
- **Monolith masquerading as microservices:** Shared database collapses microservices to one quantum. → *Fix:* Each service must own its data; verify with the quantum definition.
- **"Once-and-done" fitness function:** Fitness functions drift; the system evolves. → *Fix:* Re-evaluate categories and add emergent functions at every architectural stress point.
- **AI-based fitness function hype:** Replacing principled rules with anomaly detection. → *Fix:* Use AI where principled rules cannot reach, not as a substitute.
- **Just-for-case abstractions:** Building "Future-Proof" interfaces without current need. → *Fix:* Use JIT anticorruption layers; extract only when needed.
- **"The Final, Perfect" architecture before launch:** Buying the fanciest tool for future problems. → *Fix:* Plan for last responsible moment; switch when forced.
- **Old feature flag reuse:** Knight Capital / PowerPeg pattern; stale flag costs $400M in 45 minutes. → *Fix:* Aggressively remove used feature flags.
- **Reporting on OLTP:** Reporting on the operational database couples reports to schema evolution. → *Fix:* Use event streams to populate a denormalized reporting DB.
- **Snowflake servers:** Manually crafted servers cannot be reproduced. → *Fix:* Treat infrastructure as immutable code; rebuild from source.
- **Frozen Caveman:** Irrationally refusing change because of a single past incident. → *Fix:* Keep risk assessment realistic; revisit incidents in context.
- **Inappropriate governance:** Forcing one stack on every project. → *Fix:* Use "just enough" governance with three stack tiers (small/medium/large).
- **Vendor King:** Center the architecture on a vendor's product. → *Fix:* Treat vendor products as integration points behind an anticorruption layer.
- **Last 10% Trap / Low Code:** Hacks for the 10% always cost more than the 80% saved. → *Fix:* Evaluate the hardest problem first.
- **Resume-Driven Development:** Choosing tech for the résumé. → *Fix:* Choose for the problem domain.
- **Product customization pitfall:** Sales-driven permanent forking. → *Fix:* Realistically assess testing and fitness-function cost.
- **Excessively long planning horizons:** Choosing tools before feedback. → *Fix:* Use early deliveries to validate choices.
- **Refactoring as a synonym for change:** Refactoring preserves external behavior; restructuring changes it. → *Fix:* Use precise terminology.
- **"Best Practice" instead of trade-off:** "Best" implies no thought; everything in architecture is a trade-off. → *Fix:* Use patterns and antipatterns to identify context.
- **Continuous delivery ≠ continuous deployment:** Continuous delivery has a manual gate; continuous deployment does not. → *Fix:* Choose deliberately; document the choice.
- **Fitness functions as a stick:** Increasing developer burden without value. → *Fix:* Treat them as checklists, not punishment.
- **Dependency hell:** Allowing external dependencies to update your build silently. → *Fix:* Use a pull-model internal repo.
- **COTS black box:** Vendor products without testable internals. → *Fix:* Hold integration points to your level of maturity; build the best fitness functions possible.
- **Cyclomatic complexity war:** Hard threshold that fails every build. → *Fix:* Use herding; cascade the threshold gradually.
- **Architect as traffic cop:** Catching every style violation by hand. → *Fix:* Encode the rule as a fitness function.
- **Undocumented fitness function:** Test alone is not enough for non-developers. → *Fix:* Pair with ADR or BDD.
- **Library upgrade procrastination:** Frameworks that fall too far behind. → *Fix:* Update frameworks aggressively; libraries passively.
- **Synchronous choreography:** Mistaking communication mode for coordination mode. → *Fix:* Use the three-force matrix.
- **Positional arguments across modules:** CoP leaking across encapsulation. → *Fix:* Use named parameters or DTOs.
- **Stamp coupling:** Contracts that include fields just in case. → *Fix:* Send only what the consumer needs.
- **Cross-boundary database:** Schema change breaks other services. → *Fix:* Use Expand/Contract; treat schema as implementation detail.
- **Two-phase commit for cross-service atomicity:** 2PC is a strong-nuclear-force coupling. → *Fix:* Use eventual consistency, sagas, compensating transactions.
- **Pseudo-quantum:** A "microservice" sharing a database with another. → *Fix:* Verify the quantum definition: independently deployable + high functional cohesion + high static coupling + synchronous dynamic coupling.
- **Channeling a dynamic force into the static coupling field:** Treating dynamic coupling as a function of static coupling. → *Fix:* Compute them separately; understand the trade-off.
- **Bridge versus contract abuse:** Forcing a contract to be a "service mesh" while hiding an API gateway. → *Fix:* Use the right pattern for the right concern.
- **Edit an applied migration:** Re-running an edited migration is not reproducible. → *Fix:* Add a new migration.
- **"Trust the vendor" license change:** Allowing silent license changes through upgrades. → *Fix:* Use the license-tracker fitness function.
- **"Architecture is finished":** Treating the architecture as a one-shot artifact. → *Fix:* Watch for emergent fitness functions at every architectural stress point.
- **Unreachable fitness function:** A function that takes too long to run or costs too much to execute. → *Fix:* Choose cadence and scope that match the consequence of a violation.
- **Trapped-by-Abstraction-Distraction:** "Abstract all the things." → *Fix:* Use JIT anticorruption layers.
- **Adapting instead of evolving:** Patching to preserve old behavior. → *Fix:* Choose the change that fundamentally improves the architecture; remove the adaptation when stable.
- **Second-system syndrome:** Inflated feature scope after success. → *Fix:* Build sacrificial architectures; plan for the second iteration.
- **Sunk-cost planning:** Attaching too much value to a handcrafted plan. → *Fix:* Use small, early deliverables; update as you learn.
- **Treating data as immortal:** "Data lives forever, code does not." → *Fix:* Refactor schemas when reality changes; keep the data that has value, archive the rest.
- **Just-add-join-table:** Avoiding schema refactors by adding new join tables. → *Fix:* Refactor the schema; restore the real abstraction.
- **No immutability for infrastructure:** A DevOps snowflake that drifts. → *Fix:* Rebuild from source each time; treat OS as a constant.
- **Per-team review of every architecture decision:** Slow, manual governance. → *Fix:* Use fitness functions to enforce; reserve human review for exceptions.
- **Treating fitness functions as the whole architecture:** No amount of metrics substitutes for good design. → *Fix:* Pair fitness functions with connascence-aware design.
- **Hard-coding the cybernetics:** "If a number can go up, it must go up." → *Fix:* Use the cycle-time fitness function as a decision point, not an automatic alarm.

---

## Decision Heuristics / Checklists

### Fitness-Function Intake

- [ ] What dimension is at risk?
- [ ] What is the objective measure?
- [ ] Atomic or holistic?
- [ ] Triggered, continual, or temporal?
- [ ] Static or dynamic?
- [ ] Automated or manual?
- [ ] Intentional or emergent?
- [ ] Which deployment-pipeline stage hosts it?
- [ ] Who fixes the build when it fails?
- [ ] What is the cost of being wrong?

### Coupling Audit

- [ ] Ca and Ce computed for every significant package.
- [ ] A and I plotted; zone-of-pain and zone-of-uselessness flagged.
- [ ] D = |A + I − 1| computed; largest-D component is the refactoring target.
- [ ] Connascence types reviewed for every coupling point.
- [ ] Page-Jones's three rules applied.
- [ ] Weirich's Rule of Degree and Rule of Locality applied.

### Quantum Audit

- [ ] Independent deployment for every component.
- [ ] High functional cohesion verified.
- [ ] Static coupling includes OS, framework, broker, container orchestrator, database.
- [ ] Dynamic coupling analyzed on the three axes (communication, consistency, coordination).
- [ ] Database, OS, broker, UI identified as quantum-boundary factors.
- [ ] Each microservice is a candidate quantum only if it owns its data.

### Pipeline Audit

- [ ] Stages map to architecture characteristics.
- [ ] Fan-out + fan-in used for parallel verification.
- [ ] Feature toggles decouple deploy from release.
- [ ] Manual stages appear as bottlenecks and decision points.
- [ ] Cycle time measured and tracked as a fitness function.
- [ ] Synthetic transactions gated by flag.

### Database Audit

- [ ] Schema migrations are tested, versioned, incremental.
- [ ] Applied migrations are immutable.
- [ ] Expand/Contract applied to shared-database changes.
- [ ] Triggers and stored procedures are extracted to code when migrating to microservices.
- [ ] Transactional contexts are visible in service design.
- [ ] Reporting is not coupled to OLTP.

### Reuse Audit

- [ ] Shared code is genuinely abstracted.
- [ ] Shared code has low volatility.
- [ ] Sidecar pattern used for cross-cutting operational concerns.
- [ ] Service mesh used for consistent governance.
- [ ] Data Mesh used for cross-domain analytical data.
- [ ] Forking or duplication is allowed when reuse is hurting evolution.

### Team and Culture Audit

- [ ] Inverse Conway applied: team structure mirrors target architecture.
- [ ] Cross-functional roles present (architecture, BA, data, dev, design, ops, PM, testing).
- [ ] "You build it, you run it" applied.
- [ ] Two-pizza rule respected.
- [ ] Cognitive load balanced with business capability.
- [ ] Culture of experimentation (kaizen, spike-and-stabilize, A/B testing) present.
- [ ] Hypothesis-driven development practiced.

### Pitfall Audit

- [ ] No Last 10% Trap adoption without an evaluation of the hardest problem.
- [ ] No Vendor King; vendor products behind anticorruption layers.
- [ ] No leaky abstractions without understanding the layer below.
- [ ] No Resume-Driven Development; choice justified by the problem.
- [ ] No Inappropriate Governance; three-tier stack policy in place.
- [ ] No Reporting Atop the System of Record; event-stream denormalization in place.
- [ ] No Excessively Long Planning Horizons; early deliveries validate choices.
- [ ] No Snowflake infrastructure; rebuilt from source.
- [ ] No Frozen Caveman; risk assessment revisited in current context.
- [ ] No infinite product customization without an assessment of testing cost.
- [ ] No feature-flag reuse across uses; flags removed after the decision.

### Cycle-Time Fitness Function

- [ ] Current cycle time measured (developer start to production).
- [ ] Threshold set (e.g., four hours).
- [ ] Function implemented in the deployment pipeline.
- [ ] Breaches trigger a last-responsible-moment decision.
- [ ] Trade-off between cycle time and test coverage made consciously.

### Migration-from-Monolith Checklist

- [ ] Few large services identified, not many small ones.
- [ ] Service discovery introduced early.
- [ ] UI separated from backend with an anticorruption layer.
- [ ] LCOM measured for shared classes.
- [ ] Consumer-driven contracts introduced at integration points.
- [ ] Cycle time maintained as the migration progresses.

### Where-to-Start Decision

- [ ] Is the organization skeptical? → Low-hanging fruit.
- [ ] Is the organization committed? → Highest-value first.
- [ ] Is testing the bottleneck? → Add testing first.
- [ ] Is infrastructure the bottleneck? → Fix infrastructure first.
- [ ] Have before/after metrics been gathered?
- [ ] Has the proof-of-concept demonstrated the value?

### When to Skip Evolutionary Architecture

- [ ] Is the codebase a Big Ball of Mud too costly to refactor?
- [ ] Do other characteristics dominate (domain-specific architecture)?
- [ ] Is the architecture sacrificial (intentional MVP)?
- [ ] Is the business closing soon?

---

## Key Takeaways

1. An evolutionary architecture supports guided, incremental change across multiple dimensions.
2. Fitness functions are the architectural analog of unit tests; they are the central mechanism for protected, automated governance.
3. Every fitness function lives in the same six-dimensional category space (scope, cadence, result, invocation, proactivity, coverage); classify before wiring.
4. Choose triggered vs continual fitness functions based on the consequence of a violation.
5. The deployment pipeline is the definitive test of releasability; if it passes, the system is safe to deploy.
6. Cycle time is the leading indicator of evolution speed (v ∝ c); make it a fitness function.
7. Feature toggles decouple deployment from release; remove them aggressively.
8. ArchUnit, JDepend, linters, and 10–20-line glue scripts are the tools of architectural governance.
9. Log-based microservices governance is the fallback when no turnkey tool exists.
10. The Simian Army is a holistic, continual, operational fitness function.
11. ADRs, BDD/Cucumber, and Jupyter + jQAssistant + Neo4j are the documentation options.
12. Connascence is the right vocabulary for coupling; locality matters more than strength.
13. An architectural quantum is independently deployable, functionally cohesive, statically coupled, and dynamically synchronous.
14. The three forces of dynamic quantum coupling are communication, consistency, and coordination; choosing one tilts the others.
15. Contracts range from strict (gRPC, JSON Schema) to loose (REST, GraphQL, JSON name/value pairs); choose by coupling tolerance.
16. Microservices are the natural fit for evolutionary architecture when each service owns its data.
17. Reuse is most effective with high abstraction and low volatility; otherwise duplicate.
18. Sidecar and service mesh decouple operational concerns from domain code.
19. Data Mesh applies the same idea to analytical data.
20. Schemas must evolve alongside code, with tested, versioned, incremental migrations.
21. Expand/Contract is the safe pattern for shared-database schema changes.
22. Transactional contexts bind quanta more tightly than class-level coupling.
23. The Last 10% Trap and Vendor King are the most common antipatterns.
24. The "Just Enough" Governance model with three stack tiers fits modern DevOps.
25. Sacrificial architectures are valid for MVPs and new-market tests.
26. COTS software reduces evolvability; hold integration points to your level of maturity.
27. Immutable infrastructure prevents snowflake servers.
28. Cyclic dependencies between components are cancer; prevent them with ArchUnit.
29. Logging must follow a common format for log-based governance to work.
30. The LMAX story is the canonical example of fitness-function-driven architecture.
31. Scientist is the standard tool for fidelity fitness functions during refactor-with-confidence.
32. Conway's Law and the Inverse Conway Maneuver are real tools.
33. Cycle time is a first-class business metric for competitive advantage.
34. AI-based and generative-testing fitness functions extend verification, not replace it.
35. Architecture characteristic is one of many; do not make evolvability a religion.

---

## Cross-References

- Related: [[../Software_Architecture_Hardparts.md]]
- Related: [[../Fundamentals_of_Software_Architecture.md]]
- Related: [[../Software_Architecture_Patterns.md]]
- Related: [[../Building_Microservices.md]]
- Related: [[../Microservices_Up_And_Running.md]]
- Related: [[../Modern_Software_Engineering.md]]
- Related: [[../Continuous_Deployment.md]]
- Related: [[../Team_Topologies.md]]
- Related: [[../Technology_Strategy_Patterns.md]]
- Topic index: [[../INDEX.md]]
