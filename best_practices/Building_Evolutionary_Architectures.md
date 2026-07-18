# Building Evolutionary Architectures (2nd Edition)

**Authors:** Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage
**Topic tags:** `#architecture` `#testing`
**Language focus:** Language-agnostic (with ArchUnit/NetArchTest code examples in Java/.NET)
**Sources:** `markdown_output/Building Evolutionary Architectures 2nd edition/Building Evolutionary Architectures 2nd edition.md` · `summaries/Building_Evolutionary_Architectures_2nd_edition.md`

## TL;DR
Evolutionary architecture = **guided, incremental change across multiple dimensions**, protected by **fitness functions** as automated architectural governance. The discipline replaces up-front prediction and architecture review boards with continuous verification wired into CI/CD. Connascence, architecture quanta, deployability, and migration patterns are the structural mechanics. Test outcomes, not implementations.

---

## Best Practices by Topic

### Core Definition: What Makes an Architecture Evolutionary

**Principle:** Three characteristics define evolutionary architecture: *guided change*, *incremental change*, *multiple architectural dimensions*.

**Do:**
- Architect for evolution across **all** dimensions: technical, data, security, operational/system — not just structure.
- Pair every decision with an explicit fitness function that protects it.
- Plan for change instead of predicting it.

**Don't:**
- Don't try to predict the future; the "Why We Didn't Have Microservices in 2000" rule applies — building for hypothetical requirements wastes effort.
- Don't restrict fitness functions to one dimension (e.g., code only); apply them across data, security, operations.

*Ref: Building Evolutionary Architectures.md — "Evolving Software Architecture"*

---

### Fitness Functions — The Core Mechanism

**Principle:** A fitness function is any mechanism that provides objective evaluation criteria for architecture characteristics. It is *automated, applied continuously, and outcome-oriented*.

**Five categories of fitness functions:**

| Dimension | Types |
|-----------|-------|
| **Scope** | Atomic (single component) vs Holistic (system-wide) |
| **Cadence** | Triggered (on event) vs Continual (always running) vs Temporal (scheduled) |
| **Result** | Static (pass/fail) vs Dynamic (trend analysis) |
| **Invocation** | Automated vs Manual |
| **Proactivity** | Intentional (designed) vs Emergent (discovered) |

**Do:**
- Test **outcomes, not implementations** — fitness functions verify the goal, not how it's achieved.
- Convert dashboards into fitness functions by adding objective thresholds + fast feedback.
- Pair reactive log-based fitness functions (no runtime overhead, 24-hour cycle) with proactive monitor-based fitness functions (immediate catch, small runtime cost) — pick based on criticality.
- Treat fitness functions like Gawande's *Checklist Manifesto* — codify important-but-easily-skipped principles.

**Don't:**
- Don't use these tools "every once in a while" — without continuous verification wiring, they are not fitness functions.
- Don't pile up complex, interlocking fitness functions in an ivory tower — they must add real developer value.
- Don't mandate fitness functions you can't objectively measure.

*Ref: Building Evolutionary Architectures.md — "Fitness Functions"*

---

### Code-Based Fitness Functions (ArchUnit / NetArchTest)

**Principle:** Architects used to write governance docs in wikis nobody read. Code-based fitness functions turn principles into CI-enforced rules.

**Do:**
- Use ArchUnit (Java) or NetArchTest (.NET) for component/layer checks.
- Define layered architectures with explicit access rules between layers.
- Express annotation intent as rules ("only `@Transactional` classes may depend on `EntityManager`").
- Validate cycles at the slice level.
- For microservices where no off-the-shelf tool works, write small (10–15 line) glue scripts that parse consistent log formats.

**Don't:**
- Don't write architectural principles only in wikis — without enforcement they are aspirational, not governance.
- Don't assume the same tool exists for every language — fall back to linters (ESLint, staticcheck, sql-lint, Cpplint) for less rich structural checks.

**Code (ArchUnit — layer enforcement):**
```java
layeredArchitecture()
  .consideringAllDependencies()
  .layer("Controller").definedBy("..controller..")
  .layer("Service").definedBy("..service..")
  .layer("Persistence").definedBy("..persistence..")
  .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
  .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
  .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

**Code (ArchUnit — annotation check):**
```java
classes().that().areAssignableTo(EntityManager.class)
  .should().onlyHaveDependentClassesThat().areAnnotatedWith(Transactional.class)
```

**Code (Ruby — log-based microservices communication governance):**
```ruby
list_of_services.each { |service|
  service.import_logsFor(24.hours)
  calls_from(service).each { |call|
    unless call.destination.equals("orchestrator")
      raise FitnessFunctionFailure.new()
    end
  }
}
```

*Ref: Building Evolutionary Architectures.md — "Automating Architectural Governance"*

---

### Coupling Metrics — Afferent, Efferent, Abstractness, Instability

**Principle:** Coupling is best understood as a spectrum (afferent + efferent + abstractness + instability) rather than a single number.

**Do:**
- Track **Afferent Coupling (Ca)** — incoming dependencies (high = stable, hard to change).
- Track **Efferent Coupling (Ce)** — outgoing dependencies (high = volatile).
- Compute **Abstractness** = abstract types / total types.
- Compute **Instability** = Ce / (Ca + Ce).
- Plot **Distance from the Main Sequence** — modules should be either abstract+stable or concrete+unstable.
- Govern with directional imports (e.g., domain → infrastructure, never reverse).
- Use "herding" governance to flag outliers rather than block builds.

**Don't:**
- Don't optimize Instability alone — push toward the main sequence, not toward zero.
- Don't let "stable" become "impossible to change" — keep Ca-bearing modules abstract so they can extend without modification.

*Ref: Building Evolutionary Architectures.md — "Automating Architectural Governance" / "Cyclomatic Complexity and Herding Governance"*

---

### Connascence

**Principle:** Connascence (Page-Jones) is an enhanced language for coupling. Stronger forms of connascence are acceptable within bounded contexts but not across them.

**Types (weakest → strongest):**

**Static (source code):**

| Type | Example | Risk |
|------|---------|------|
| Name | Same method/variable name | Acceptable |
| Type | Same data type | Acceptable with type systems |
| Meaning / Convention | `true` = active (vs. explicit enum) | Risky — magic literals |
| Position | Positional function args | Fragile |
| Algorithm | Same algorithm duplicated | Very fragile |
| Value | Magic number shared | Fragile |

**Dynamic (runtime):**

| Type | Example | Risk |
|------|---------|------|
| Execution | Order of method calls matters | Moderate |
| Timing | Race conditions / thread interleaving | Dangerous |
| Identity | Same backing object across modules | Dangerous |
| Value (shared state) | Concurrent updates to shared queue | Dangerous |

**Three rules (Page-Jones):**
1. Minimize overall connascence by breaking the system into encapsulated elements.
2. Minimize connascence that crosses encapsulation boundaries.
3. Maximize connascence within encapsulation boundaries.

**Jim Weirich's two rules:**
- **Rule of Degree:** convert strong forms of connascence into weaker forms.
- **Rule of Locality:** as distance between software elements increases, use weaker forms of connascence.

**Do:**
- Prefer **static connascence** to dynamic connascence (easier to detect and refactor).
- Strength × Locality × Degree together — strong connascence within the same module is fine; the same connascence spread across components is code smell.
- Refactor Connascence of Meaning → Connascence of Name by introducing named constants instead of magic literals.

**Don't:**
- Don't ignore dynamic connascence — it's harder to detect but more dangerous.
- Don't tolerate strong connascence across module boundaries.

*Ref: Building Evolutionary Architectures.md — "Evolutionary Architecture Topologies"*

---

### Architecture Quantum

**Principle:** An **architecture quantum** = independently deployable component with high functional cohesion, high static coupling, and synchronous dynamic coupling.

**Do:**
- Include all dependent components in the quantum boundary (database, message broker, container orchestration, etc.).
- Use the quantum as a **shared language** between architects, developers, and ops.
- Decompose monoliths into quanta only where static coupling allows independent deployment.
- Recognize that **shared databases collapse quanta** — any system sharing a single database forms a single quantum.

**Don't:**
- Don't assume distributed = multi-quantum. Mediator-style event-driven and broker-style EDA can both be single quantum if they share a coupling point (orchestrator or database).
- Don't ignore the UI as a coupling point — a tightly coupled UI can collapse a microservices architecture into a single quantum (use micro-frontends to break this).
- Don't optimize for "as many quanta as possible" — optimize for useful bounded contexts (e.g., `CatalogCheckout`, not `Customer`).

**Three quantum types in Data Mesh:**
- **Architecture quantum** — service + dependencies
- **Data product quantum (DPQ)** — discoverable, understandable, timely, secure, high-quality data with embedded sidecar for federated governance
- **Cooperative quantum** — DPQ that collaborates with another quantum to fulfill workflows

*Ref: Building Evolutionary Architectures.md — "Evolutionary Architecture Topologies"*

---

### Reuse & Coupling Trade-offs

**Principle:** Effective reuse = abstraction + low volatility. Don't share volatile code across bounded contexts.

**Three reuse approaches:**

| Approach | When to use | Trade-off |
|----------|-------------|-----------|
| Shared service | Stable cross-cutting functionality | Network overhead + dependency |
| Shared library | Stable, well-defined | Versioning across services |
| Duplication | Different evolution paths per consumer | Inconsistency risk |

**Do:**
- Use **sidecars / service mesh** for orthogonal operational coupling (logging, security, monitoring).
- Use **data mesh / event streams** for orthogonal data coupling — never shared databases.
- Recognize the **reuse paradox**: reuse is valuable when the component is both abstract AND stable; if it's volatile, duplication is safer.

**Don't:**
- Don't share code across bounded contexts that evolve at different rates.
- Don't let reuse become a bottleneck — if the component team can't keep up with innovation pace, reuse becomes an antipattern.

*Ref: Building Evolutionary Architectures.md — "Reuse patterns"*

---

### Evolutionary Data

**Principle:** Databases must evolve alongside application code. Separate structural changes from data migrations.

**Do:**
- Version database migrations with code (Flyway, Liquibase).
- Use the **expand-contract pattern**: add new column → migrate data → remove old column.
- Embrace parallel change (old + new schemas running simultaneously during migration).
- Treat each service as the owner of its data store.

**Don't:**
- Don't share databases across services — that collapses quanta and creates tight coupling.
- Don't make structural and data changes in one irreversible step.

*Ref: Building Evolutionary Architectures.md — "Evolutionary Data"*

---

### Engineering Incremental Change

**Principle:** Incremental change requires small frequent deployments, deployment pipelines, and feature toggles.

**Deployment pipeline stages:**

| Stage | Activity | Duration |
|-------|----------|----------|
| Commit | Unit tests, code quality | Minutes |
| Acceptance | Integration tests, API contract tests | Tens of minutes |
| Security/Compliance | SAST, SCA, compliance | Hours |
| Performance | Load tests, benchmarks | Hours |
| Deployment | Canary / blue-green | Variable |

**Do:**
- Decouple deployment from release via **feature toggles**.
- Stage by value: each pipeline stage verifies something the previous stage cannot.
- Test API contracts (Pact, Spring Cloud Contract) before integration tests.
- Use synthetic transactions for continuous holistic monitoring.

**Don't:**
- Don't make release decisions outside the pipeline — the pipeline *is* the release decision.
- Don't skip the QA-in-production step (synthetic transactions + canary fitness functions) even when pre-production tests pass.

*Ref: Building Evolutionary Architectures.md — "Engineering Incremental Change"*

---

### Principles for Evolvable Architectures

| Principle | Meaning |
|-----------|---------|
| **Last Responsible Moment** | Delay decisions until you must make them, not before. Gather information until cost of delaying exceeds benefit. |
| **Architect and develop for evolvability** | Design for change via interfaces, abstractions, loose coupling. |
| **Postel's Law** | Be conservative in what you send, liberal in what you accept. |
| **Architect for testability** | If you can test it, you can change it safely. |
| **Conway's Law** (and Reverse Conway Maneuver) | Design architecture to align with (or deliberately shape) organizational structure. |

**Six additional guidelines:**
1. Remove needless variability.
2. Make decisions reversible (Fowler: "eliminate irreversibility").
3. Prefer evolvable over predictable.
4. Build anticorruption layers (isolate external systems from your domain model).
5. Build sacrificial architectures (some components are meant to be replaced).
6. Version services internally (keep external APIs stable while evolving internals).

**Do:**
- Reach for sacrificial architectures + MVP for new market exploration (eBay, Twitter, Stripe Index).
- Use the "Why We Didn't Have Microservices in 2000" rule — don't build for hypothetical scale.
- Always include an anticorruption layer at integration points.

**Don't:**
- Don't try to design the "final" architecture from the start.
- Don't share coupling-heavy code across volatile boundaries.

*Ref: Building Evolutionary Architectures.md — "Building Evolvable Architectures"*

---

### Migration Strategies

**Do:**
- Use the **strangler fig pattern** — incrementally replace monolith pieces with new services.
- Use **event interception** — intercept database changes, emit events, build new consumers.
- Use **data-first decomposition** — split data first, then services.

**Don't:**
- Don't do the "Grand Migration" — pushing for a wholesale rewrite copied from a previous employer's stack kills companies (Digg V4, Uber Grand Migrations in early days).

*Ref: Building Evolutionary Architectures.md — "Migration strategies"*

---

### Fitness Function Implementation Patterns

**Do:**
- Choose between atomic vs. holistic based on failure scope (security = proactive monitor; structural = reactive 24-hour log scrape).
- Use **GitHub Scientist** for fidelity fitness functions when replacing critical code — run new implementation in parallel for 1% of requests, log mismatches, always return the control value.
- Implement **devops fitness functions** (deployment frequency, MTTR thresholds, build time limits, infra cost ceilings).
- Implement **enterprise fitness functions** (service inventory completeness, API doc coverage, compliance audit automation).

**Don't:**
- Don't try to implement every fitness function proactively with real-time monitors — sometimes the overhead outweighs the benefit.

*Ref: Building Evolutionary Architectures.md — "Automating Architectural Governance" / "Fidelity Fitness Functions"*

---

### Chaos Engineering as Holistic Fitness Function

**Principle:** Chaos engineering is a holistic, continual, operational fitness function — it verifies architectural characteristics like resilience and scalability in production.

**Simian Army roles:**

| Monkey | Job |
|--------|-----|
| Chaos Monkey | Random latency, reliability degradation per service |
| Chaos Gorilla | Knock out an entire Amazon data center |
| Chaos Kong | Knock out an entire availability zone |
| Doctor Monkey | Resource constraint alarms (CPU, disk) |
| Latency Monkey | Specifically stress high latency |
| Janitor Monkey | Find orphaned services with no callers, disintegrate them (reborn as Swabbie) |
| Conformity Monkey | Verify governance (REST verbs, error handling, metadata) |
| Security Monkey | Find open debug ports, missing auth |

**Do:**
- Run chaos continuously, not on a schedule — forces developers to build resilient code.
- Use the principle: "It's not a question of *if* your system will eventually have a fault but rather *when*."

**Don't:**
- Don't run chaos engineering only in pre-production — its real value is the production reality check.

*Ref: Building Evolutionary Architectures.md — "Chaos Engineering"*

---

### Pitfalls and Antipatterns

| Antipattern | Description | Fix |
|-------------|-------------|-----|
| **Last 10% Trap / Low-Code/No-Code** | Tool handles 90%; the last 10% requires unsustainable workarounds | Treat all software as just another integration point, not the center of architecture |
| **Vendor King** | Over-reliance on a single vendor ecosystem limits evolution | Build anticorruption layers; assume integration at the outset |
| **Leaky Abstractions** | Abstractions expose implementation details | Tighten abstractions; refactor to better connascence |
| **Resume-Driven Development** | Tech chosen for career value, not fit | Tie every choice to a measurable diagnosis |
| **Code Reuse Abuse** | Sharing across bounded contexts creates hidden coupling | Replace with duplication when volatility differs |
| **Golden Hammer** | Same pattern applied to every problem | Pick the architecture that fits the diagnostic |
| **Fan-out without fitness functions** | Changes propagate unpredictably | Couple fan-out to fitness-function verification |
| **Over-engineering** | Building evolutionary mechanisms for dimensions that don't need them | Apply Last Responsible Moment; defer until needed |
| **Frozen Caveman** | Architect reverts to irrational pet concerns (e.g., "But what if we lose Italy?") | Distinguish genuine vs. perceived technical risk |
| **Inappropriate Governance** | Fitness functions or review boards misaligned to actual architectural challenges | Tie governance to measurable outcomes |
| **Reporting Atop the System of Record** | Reporting reads from operational DB, polluting performance | Use CQRS — separate read models |
| **Big Ball of Mud (distributed)** | Accidental complexity introduced under business pressure | Use EventStorming to identify boundaries |
| **Abstraction Distraction** | Building abstractions nobody needs yet | Apply YAGNI + Last Responsible Moment |

*Ref: Building Evolutionary Architectures.md — "Pitfalls and Antipatterns"*

---

### The Quote That Anchors Everything

> "We discuss patterns but not *best practices*, which are virtually nonexistent in software architecture. *Best practice* implies that an architect can turn their brain off whenever they encounter a particular situation — after all, this is the *best* way to handle this practice. However, everything in software architecture is a trade-off, meaning that architects must evaluate trade-offs anew for virtually every decision."

*Ref: Building Evolutionary Architectures.md — "Pitfalls and Antipatterns"*

---

## Anti-Patterns & Common Mistakes

- **"We don't need fitness functions, our devs are senior":** seniority ≠ immunity to skipped steps under pressure. Use fitness functions as checklists.
- **Writing fitness functions without clear thresholds:** dashboards ≠ engineering. Define objective measures and provide fast feedback.
- **Reactive-only fitness functions for security violations:** if the violation has immediate blast radius (data exfiltration), use proactive monitors, not 24-hour log scrapes.
- **Fitness functions that mandate implementations, not outcomes:** ("use Hibernate") not ("expose a persistence layer through this contract"). Outcomes preserve evolution.
- **Strangler fig without data decomposition:** if the monolith owns the data, new services can't be independently deployed.
- **Sharing libraries across volatile services:** every version bump forces coordinated upgrade.
- **Decomposing by entity:** creating `CustomerService`, `OrderService`, etc., leads to chatty services. Decompose by bounded context / workflow instead.
- **Carrying forward coupling hidden in shared databases:** shared databases collapse architecture quanta.

---

## Decision Heuristics / Checklists

- **Picking a fitness-function category:**
  - Scope = atomic if a single component can verify; holistic if the system must verify together.
  - Cadence = triggered for fast feedback on commits; continual for stateful invariants; temporal for expensive batch evaluations.
  - Result = static for hard pass/fail thresholds; dynamic for relative trends.
  - Invocation = automated whenever possible; manual only when automation is infeasible.
  - Proactivity = intentional for design rules; emergent for discovered behaviors.
- **Connascence audit:** identify the strongest connascence that crosses module boundaries — that's your highest-priority refactoring target.
- **Quantum audit:** draw the static coupling diagram — count static coupling points (databases, brokers, orchestrators). Each shared point collapses quanta.
- **Reuse vs. duplication:** share only when both abstract and stable. Otherwise duplicate.
- **Migration rule:** greenfield can wait; retrofit fitness functions incrementally, starting with the most painful architectural issues.
- **Last Responsible Moment check:** before adding an abstraction, ask "what decision am I making now, and what's the cost of delaying it?"
- **Greenfield principles:** define fitness functions from the start, establish CI/CD day one, resist over-engineering, start simple, evolve as needed.
- **Existing-system principles:** retrofit fitness functions incrementally, start with the most painful issues, use strangler fig for migration.
- **Reuse pattern selection:** sidecar/service mesh for orthogonal operational coupling; event streams for orthogonal data coupling; shared library only when both abstract and stable.

---

## Key Takeaways

1. **Evolutionary architecture supports guided, incremental change across multiple dimensions** — it's not about predicting the future.
2. **Fitness functions are the core mechanism** — automated tests verifying architectural characteristics, run continuously in CI/CD.
3. **Automated governance replaces architecture review boards** — fitness functions enforce rules at the speed of development, not the speed of meetings.
4. **Connascence guides coupling decisions** — stronger forms within bounded contexts; weaker forms across boundaries.
5. **Architectural quanta are the building blocks** — independently deployable, high cohesion, low external coupling, with all dependencies included.
6. **Data must evolve too** — migrations, expand-contract pattern, no shared databases across services.
7. **Last Responsible Moment beats upfront design** — delay decisions until you have enough information, then act decisively.
8. **Conway's Law is a tool** — organize teams to produce the architecture you want (Reverse Conway Maneuver).
9. **Reuse requires abstraction + low volatility** — don't share volatile code across bounded contexts.
10. **Pitfalls are predictable and avoidable** — Vendor King, leaky abstractions, Last 10% trap, Frozen Caveman, Grand Migration.
11. **Fitness functions must test outcomes, not implementations** — this is what keeps architecture evolvable.
12. **Sacrificial architectures are legitimate** — eBay, Twitter, Stripe all started with throwaway code and evolved later.

---

## Cross-References

- Related: [[../Software_Architecture_Metrics.md]] — fitness functions, MMI, coupling metrics
- Related: [[../Head_First_Software_Architecture.md]] — bounded contexts, microservices, modular monolith
- Related: [[../Software_Architect_Elevator.md]] — communicating architecture up the org
- Topic index: [[../INDEX.md]]
