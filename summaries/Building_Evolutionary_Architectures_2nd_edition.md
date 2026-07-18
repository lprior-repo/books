# Building Evolutionary Architectures (2nd Edition) - Neal Ford, Rebecca Parsons, Patrick Kua & Pramod Sadalage

## Comprehensive Summary

---

## Part I: Mechanics

### Chapter 1: Evolving Software Architecture

**The challenge:** Software architectures must respond to constant change—new requirements, new technologies, scaling demands, organizational shifts. Traditional "upfront design" architectures degrade over time as they resist change.

**What is evolutionary architecture:**
> Software architecture that supports guided, incremental change across multiple dimensions.

Three characteristics define evolutionary architecture:
1. **Guided change**: Architecture evolves with purpose, not randomly. Fitness functions define and protect important architectural characteristics.
2. **Incremental change**: Changes happen in small, verifiable steps. Both the architecture and the development process support incremental evolution.
3. **Multiple architectural dimensions**: Architecture isn't just structure. It includes security, scalability, performance, data patterns, deployment, and more. All dimensions must be evolvable.

**Key questions evolutionary architecture answers:**
- How can we plan long-term when everything changes? → By building architectures that accommodate change rather than resist it.
- How do we prevent architectural degradation? → With automated fitness functions that continuously verify architectural invariants.

### Chapter 2: Fitness Functions

**What is a fitness function?**
An automated mechanism that evaluates how well an architecture satisfies its important characteristics. Named by analogy to evolutionary biology's fitness landscapes.

**Categories of fitness functions:**

| Dimension | Types |
|-----------|-------|
| **Scope** | Atomic (single function) vs Holistic (system-wide) |
| **Cadence** | Triggered (on commit) vs Continual (always running) vs Temporal (scheduled) |
| **Result** | Static (pass/fail) vs Dynamic (trend analysis) |
| **Invocation** | Automated vs Manual |
| **Proactivity** | Intentional (designed) vs Emergent (discovered) |

**Examples of fitness functions:**
- **Performance**: "Response time must stay under 200ms for the checkout flow" — tested via automated load tests in CI
- **Scalability**: "System must handle 10,000 concurrent users" — periodic load testing
- **Security**: "No dependency with known critical CVE" — automated SCA scanning
- **Architecture structure**: "No circular dependencies between modules" — ArchUnit test
- **Code quality**: "Cyclomatic complexity below 10 per function" — SonarQube or similar
- **Deployability**: "Service must deploy independently" — test that service A can deploy without service B

**Fitness functions test outcomes, not implementations.** They don't mandate how to achieve a goal, just verify that it's achieved.

**Who writes fitness functions?** Architects, developers, and operations collaborate. Developers implement them as tests or CI checks.

### Chapter 3: Engineering Incremental Change

**Incremental change requires:**
1. **Small, frequent deployments**: Deploy many times per day, not once per quarter
2. **Deployment pipelines**: Automated stages (build → test → security scan → deploy) that verify fitness functions at each stage
3. **Feature toggles**: Decouple deployment from release

**Deployment pipeline stages:**
- **Commit stage**: Fast unit tests, code quality checks (minutes)
- **Acceptance stage**: Integration tests, API contract tests
- **Security/compliance stage**: SAST, SCA, compliance checks
- **Performance stage**: Load tests, benchmarks
- **Deployment stage**: Canary/blue-green deployment to production

**Case studies:**
- Adding fitness functions to a billing service: Contract tests ensure API compatibility
- Validating API consistency: Automated checks that API changes don't break consumers

### Chapter 4: Automating Architectural Governance

**Fitness functions as governance:** Instead of architecture review boards (slow, subjective), use automated fitness functions that run in CI. Governance at the speed of development.

**Code-based fitness functions:**
- **ArchUnit** (Java), **NetArchTest** (.NET): Assert architectural rules as code
- Example: "No service layer class should depend on a data layer class directly"
- Example: "All controllers must be in the api package"

**Coupling metrics:**
- **Afferent coupling (Ca)**: How many other things depend on this module (incoming). High Ca = stable, hard to change.
- **Efferent coupling (Ce)**: How many things this module depends on (outgoing). High Ce = volatile, affected by external changes.
- **Abstractness**: Ratio of abstract types to total types. Abstract modules are extension points.
- **Instability**: Ce / (Ca + Ce). Measures resilience to change. Low instability = stable.
- **Distance from main sequence**: Ideal balance of abstractness and instability. Modules should be either abstract+stable or concrete+unstable.

**Cyclomatic complexity governance:**
- Set thresholds for maximum complexity
- "Herding" governance: Automatically flag code that exceeds complexity thresholds

**Turnkey governance tools:**
- Linters (ESLint, golangci-lint)
- SAST tools (SonarQube, Checkstyle)
- Dependency analysis tools
- Accessibility testing tools
- Open source license compliance

**DevOps fitness functions:**
- Deployment frequency targets
- Mean time to recovery (MTTR) thresholds
- Build time limits
- Infrastructure cost ceilings

**Enterprise architecture fitness functions:**
- Service inventory completeness
- API documentation coverage
- Compliance audit automation

---

## Part II: Structure

### Chapter 5: Evolutionary Architecture Topologies

**Connascence**: A coupling metric developed by Meilir Page-Jones. Two components are connascent if a change in one requires a change in the other to maintain correctness.

**Types of connascence (from weakest to strongest):**
1. **Connascence of Name**: Both use the same name (method, variable). Acceptable.
2. **Connascence of Type**: Both use the same type. Acceptable with good type systems.
3. **Connascence of Meaning/Convention**: Both agree on the meaning of a value (e.g., "true" = active). Risky.
4. **Connascence of Position**: Both rely on positional ordering (e.g., function arguments). Fragile.
5. **Connascence of Algorithm**: Both must implement the same algorithm. Very fragile.
6. **Connascence of Value**: Specific values must match (e.g., magic numbers). Fragile.
7. **Connascence of Timing**: Execution timing matters (race conditions). Dangerous.

**Rule of connascence locality:** Stronger forms of connascence are acceptable within a bounded context but not across bounded contexts.

**Architectural quanta and granularity:**
- **Architectural quantum**: The smallest independently deployable unit with high functional cohesion
- Microservices are naturally sized as architectural quanta
- Monoliths can have multiple quanta if they maintain module boundaries

**Independently deployable requirements:**
- High functional cohesion (all related functionality in one unit)
- High static coupling within, low coupling between
- Dynamic quantum coupling: Loose runtime coupling between services

**Contracts between services:**
- Explicit API contracts (REST, gRPC, events)
- Contract testing (Pact, Spring Cloud Contract)
- Version strategies: semantic versioning, backward-compatible evolution

**Reuse patterns:**
- **Effective reuse = abstraction + low volatility**: Only reuse stable, well-abstracted components
- **Sidecars and service mesh**: Orthogonal operational coupling (logging, security, monitoring) implemented as sidecars, not library dependencies
- **Data mesh**: Orthogonal data coupling through event streams, not shared databases

### Chapter 6: Evolutionary Data

**Evolutionary database design principles:**
- Databases must evolve alongside application code
- Use database migrations (Flyway, Liquibase) versioned with code
- Separate structural changes from data migrations

**Data migration strategies:**
1. **Expand-contract pattern**: Add new column → migrate data → remove old column. Each step is safe and reversible.
2. **Parallel change**: Run old and new schemas simultaneously during migration

**Shared database antipattern:**
- Multiple services accessing the same database creates tight coupling
- Prefer each service owning its data store
- Use events/APIs for data sharing

**Data as an architectural dimension:**
- Data gravity: Data attracts services and logic
- Data custody: Clear ownership of data domains
- Data as a product (from data mesh thinking)

### Chapter 7: Building Evolvable Architectures

**Principles of evolutionary architecture:**

1. **Last Responsible Moment**: Delay decisions until you must make them, not before. Gather information until the cost of delaying exceeds the benefit.

2. **Architect and develop for evolvability**: Design for change. Use interfaces, abstractions, and loose coupling.

3. **Postel's Law**: Be conservative in what you send, liberal in what you accept. Robust APIs tolerate variation in inputs.

4. **Architect for testability**: If you can test it, you can change it safely. Testability enables evolution.

5. **Conway's Law**: Design architectures that align with (or deliberately shape) organizational structure. Reverse Conway: organize teams to produce the architecture you want.

**Steps to build evolvable architectures:**
1. Identify dimensions affected by evolution (performance, security, scalability, etc.)
2. Define fitness functions for each dimension
3. Use deployment pipelines to automate fitness functions
4. Start with the most important dimensions

**For greenfield projects:**
- Define fitness functions from the start
- Establish CI/CD pipeline on day one
- Resist over-engineering: start simple, evolve as needed

**For existing architectures:**
- Retrofit fitness functions incrementally
- Start with the most painful architectural issues
- Use the strangler fig pattern for gradual migration

**Migration strategies:**
- **Strangler fig**: Incrementally replace monolith pieces with new services
- **Event interception**: Intercept database changes, emit events, build new consumers
- **Data-first decomposition**: Split data first, then services

**Guidelines for evolution:**
- **Remove needless variability**: Standardize where variety adds no value
- **Make decisions reversible**: Prefer options that can be undone
- **Prefer evolvable over predictable**: Don't lock in predictions
- **Build anticorruption layers**: Isolate external systems from your domain model
- **Build sacrificial architectures**: Some components are meant to be replaced
- **Version services internally**: Keep external APIs stable while evolving internals

### Chapter 8: Pitfalls and Antipatterns

**Technical architecture pitfalls:**
- **Last 10% trap**: Low-code/no-code tools handle 90% of cases; the last 10% requires unsustainable workarounds
- **Vendor king**: Over-reliance on a single vendor's ecosystem limits evolution
- **Leaky abstractions**: Abstractions that expose implementation details
- **Resume-driven development**: Choosing technologies for career value rather than project fit

**Structural pitfalls:**
- **Code reuse abuse**: Sharing code across bounded contexts creates hidden coupling
- **Golden hammer**: Applying the same solution pattern to every problem

**Incremental change pitfalls:**
- **Fan-out** without fitness functions: Changes propagating unpredictably
- **Over-engineering**: Building evolutionary mechanisms for dimensions that don't need them

---

## Part III: Impact

### Case Studies and Real-World Application

**Microservices as evolutionary architecture:**
- Microservices score highly on independent deployability (each service is an architectural quantum)
- The bounded context alignment provides natural evolution boundaries
- Fitness functions verify inter-service contracts, performance, and security

**Architectural restructuring at scale:**
- Case study of restructuring architecture while deploying 60 times per day
- Incremental migration with fitness functions ensuring no regression

**Fitness function-driven architecture:**
- Some organizations use fitness functions as the primary governance mechanism
- Teams have autonomy within fitness function constraints
- Architects define "what" (fitness functions), teams decide "how"

---

## Key Takeaways

1. **Evolutionary architecture supports guided, incremental change across multiple dimensions**. It's not about predicting the future—it's about building systems that can adapt.

2. **Fitness functions are the core mechanism**: Automated tests that verify architectural characteristics (performance, security, coupling, structure) run continuously in CI/CD.

3. **Automated governance replaces architecture review boards**: Fitness functions enforce rules at the speed of development, not the speed of meetings.

4. **Connascence guides coupling decisions**: Keep strong connascence within bounded contexts, minimize it across boundaries.

5. **Architectural quanta are the building blocks**: Independently deployable units with high functional cohesion and low external coupling.

6. **Data must evolve too**: Use database migrations, expand-contract patterns, and avoid shared databases.

7. **Last Responsible Moment beats upfront design**: Delay decisions until you have enough information, then act decisively.

8. **Conway's Law is a tool, not just an observation**: Organize teams to produce the architecture you want (Reverse Conway Maneuver).

9. **Reuse requires abstraction + low volatility**: Don't share volatile code across bounded contexts.

10. **Pitfalls are predictable and avoidable**: Vendor lock-in, leaky abstractions, and over-engineering can be prevented with awareness and fitness functions.
