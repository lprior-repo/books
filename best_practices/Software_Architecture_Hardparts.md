# Software Architecture: The Hard Parts — Deep Dive
**Authors:** Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani
**Topic tags:** `#architecture` `#api` `#general`
**Language focus:** language-agnostic (Java/.NET/Python/Bash examples)
**Sources:** `markdown_output/Software Architecture - The Hardparts/Software Architecture - The Hardparts.md` · `summaries/Software_Architecture_Hardparts.md`

## TL;DR
There are no best practices in distributed architecture — only trade-offs. Strive for the "least worst" combination. Every hard decision (granularity, data ownership, distributed transactions, contracts, coordination) is resolved by named trade-off drivers, ADRs, and architectural fitness functions that verify the decision objectively. The book formalizes an eight-cell saga matrix from three orthogonal dimensions (Communication, Consistency, Coordination), six granularity disintegrators vs. four integrators, four code-reuse patterns, three eventual consistency patterns, and four data-mesh principles — all wrapped around a Sysops Squad case study.

---

## Best Practices by Topic

### Core Philosophy: There Are No Best Practices
**Principle:** Don't maximize — minimize pain by analyzing trade-offs explicitly.

**Do:**
- Treat every architectural decision as a trade-off between entangled dimensions.
- Document every significant decision as an ADR (Context / Decision / Consequences).
- Encode architectural characteristics as objective fitness functions and run them continuously in CI/CD.
- Use MECE lists so the things you compare are mutually exclusive and collectively exhaustive.
- Strive for the "least worst" combination of trade-offs.

**Don't:**
- Search for a single "best" pattern — every organization is a snowflake.
- Default to Epic Saga (synchronous + atomic + orchestrated) because it feels familiar to monolithic ACID.
- Combine conflicting techniques in isolation (e.g., async + atomic + choreographed → Horror Story Saga).
- Adopt "share nothing" as a religion — measure its cost first.

**Code:**
```
Don't try to find the *best* design in software architecture;
instead, strive for the *least worst* combination of trade-offs.

— All things are poison, and nothing is without poison;
the dosage alone makes it so a thing is not a poison. (Paracelsus)
```
*Ref: Hardparts.md — "Why 'The Hard Parts'?" / "Giving Timeless Advice About Software Architecture"*

---

### Architecture Decision Records (ADRs)
**Principle:** Capture every consequential architectural decision as a short, version-controlled artifact.

**Do:**
- Use the Michael Nygard template: Context / Decision / Consequences.
- Write the ADR before or during the decision, not after the fact.
- Treat each ADR as approved at the time it's referenced by future decisions (the book assumes "all ADRs are approved").
- Co-locate ADRs with the codebase under `docs/adr/` (or equivalent).

**Don't:**
- Write ADRs as multi-page essays — the book deliberately keeps them one to two pages.
- Use ADRs as a substitute for empirical evaluation (fitness functions are the verification).
- Forget to revisit ADRs when context changes.

**Code:**
```
*ADR: A short noun phrase containing the architecture decision*

*Context*
…one- or two-sentence description of the problem, list of alternatives.

*Decision*
…the architecture decision and detailed justification.

*Consequences*
…consequences after the decision is applied; trade-offs considered.
```
*Ref: Hardparts.md — "Architectural Decision Records"*

---

### Architectural Fitness Functions
**Principle:** Fitness functions are objective, executable checks that verify architectural characteristics — not domain behavior.

**Do:**
- Classify by scope: **atomic** (single characteristic, e.g., a cycle test) vs **holistic** (combination, e.g., security + performance).
- Trigger continuously in CI/CD; treat manual ones as exceptional (legal review, sign-off).
- Use them to govern layers, prevent cycles, detect contract drift, govern service-mesh sidecar inclusion.
- Use **JDepend / ArchUnit / NetArchTest** for code-level fitness functions.
- Use **consumer-driven contract tests** as architectural fitness functions for distributed contracts.
- Apply the test: *"Is any domain knowledge required to execute this test?"* — if no → fitness function; if yes → unit/functional/UAT.

**Don't:**
- Over-engineer an interlocking "cabal" of fitness functions that frustrate teams.
- Conflate fitness functions with unit tests — fitness functions validate architecture characteristics, not domain criteria.
- Use only manual review for governance (Equifax data breach is the canonical cautionary tale).

**Code:**
```java
// JDepend — atomic fitness function to detect component cycles
public class CycleTest {
  private JDepend jdepend;
  @BeforeEach void init() {
    jdepend = new JDepend();
    jdepend.addDirectory("/path/to/project/persistence/classes");
    jdepend.addDirectory("/path/to/project/web/classes");
    jdepend.addDirectory("/path/to/project/thirdpartyjars");
  }
  @Test
  void testAllPackages() {
    Collection packages = jdepend.analyze();
    assertEquals("Cycles exist", false, jdepend.containsCycles());
  }
}
```
```java
// ArchUnit — holistic layer fitness function
layeredArchitecture()
  .layer("Controller").definedBy("..controller..")
  .layer("Service").definedBy("..service..")
  .layer("Persistence").definedBy("..persistence..")
  .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
  .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
  .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```
```csharp
// NetArchTest (C#) — same idea in .NET
var result = Types.InCurrentDomain()
  .That().ResideInNamespace("NetArchTest.SampleLibrary.Presentation")
  .ShouldNot().HaveDependencyOn("NetArchTest.SampleLibrary.Data")
  .GetResult().IsSuccessful;
```
*Ref: Hardparts.md — "Architecture Fitness Functions" / "Using Fitness Functions" / "The Equifax Data Breach"*

---

### Architecture Quanta & Coupling
**Principle:** A quantum is an independently deployable unit with high functional cohesion and high static coupling. Find your quanta before picking a style.

**Do:**
- Model **static coupling** (OS/container, transitive deps, persistence, integration points, brokers).
- Model **dynamic coupling** (communication × consistency × coordination).
- Treat the database as part of a quantum — a shared DB forces a single quantum.
- Map your style to its quantum count: monolith=1, service-based=1 (shared DB), microservices=N, event-driven=variable.

**Don't:**
- Assume functional decomposition equals deployment decomposition.
- Allow a shared database to silently collapse multiple services into one quantum.
- Treat a tightly-coupled UI as independent — it forms its own quantum around backend coupling points.

**Code:**
```
Two artifacts (including services) are coupled if a change in one
might require a change in the other to maintain proper functionality.
```
Dynamic quantum coupling dimensions:
```
{ Communication: sync/async } × { Consistency: atomic/eventual } ×
{ Coordination: orchestrated/choreographed }
```
*Ref: Hardparts.md — "Architecture (Quantum | Quanta)" / "Dynamic Quantum Coupling"*

---

### Modularity Drivers: Maintainability, Testability, Deployability, Scalability, Availability
**Principle:** Architectural modularity is driven by five forces; each style optimizes for different drivers.

**Do:**
- Match styles to business drivers (speed-to-market vs. competitive advantage).
- Use a modular monolith or microkernel when modularity is required but full distribution isn't.
- Quantify trade-offs: e.g., monolith = 1 quantum + low scalability; microservices = N quanta + excellent MTTS (mean time to startup).

**Don't:**
- Break apart applications on technical partitioning alone (wish "domain partitioning").
- Treat MTTS as a runtime-only concern — it is an architectural characteristic improved by smaller, fine-grained services.

**Code (star ratings from Fundamentals of Software Architecture):**
```
                | Layered | Service-Based | Microservices
Scalability     |   ★     |     ★★★       |    ★★★★★
Elasticity      |   ★     |     ★★        |    ★★★★★
```
*Ref: Hardparts.md — "Architectural Modularity" / "Maintainability" / "Testability" / "Deployability" / "Scalability" / "Availability/Fault Tolerance"*

**Pitfall — the Big Ball of Distributed Mud:**
```
If your microservices must be deployed as a complete set in a specific order,
please put them back in a monolith and save yourself some pain.
— Matt Stine
```
*Ref: Hardparts.md — "Deployability"*

---

### Code Decomposability: Afferent/Efferent Coupling, Abstractness/Instability, Distance from Main Sequence
**Principle:** Measure before you migrate. A codebase falling into the "zone of uselessness" or "zone of pain" is not a good salvage target.

**Do:**
- Use **Ca** (afferent = incoming dependencies) and **Ce** (efferent = outgoing) from Yourdon/Constantine (1979).
- Calculate **Abstractness** = Σ abstract / (Σ concrete + Σ abstract) — Robert Martin.
- Calculate **Instability** = Ce / (Ce + Ca).
- Calculate **Distance from the Main Sequence** = |A + I − 1|.
- Use JDepend or similar to visualize coupling matrices.

**Don't:**
- Migrate a Big Ball of Mud (Foote, 1999) without re-establishing internal structure first.
- Confuse high abstractness with bad design — extreme abstractness is the "zone of uselessness"; extreme concreteness is the "zone of pain".

**Code:**
```
Abstractness (A)  = Σm^a / (Σm^c + Σm^a)
Instability  (I)  = C^e / (C^e + C^a)
Distance from main sequence (D) = |A + I - 1|

Zone of Uselessness = high A, high I     (too abstract, breaks)
Zone of Pain        = low  A, low  I     (too concrete, brittle)
```
*Ref: Hardparts.md — "Afferent and Efferent Coupling" / "Abstractness and Instability" / "Distance from the Main Sequence"*

---

### Component-Based Decomposition (CBD) vs Tactical Forking
**Principle:** Build services from *components*, not individual classes.

**Do:**
- Use **Component-Based Decomposition** when the codebase has observable component boundaries.
- Use **Tactical Forking** when the codebase is a Big Ball of Mud — clone, then *delete* what you don't need (extraction is harder because of high coupling).
- Walk the directory structure first; convert separators to dots and create a logical namespace per component (e.g., `ss/ticket/assign` → `ss.ticket.assign`).
- Use CBD as a stepping-stone to a service-based architecture before microservices.

**Don't:**
- Extract components one class at a time from chaotic code (unravels dependencies).
- Try to break apart the database in the same step as breaking apart components.
- Assume tactical forking is a strategic move — it's tactical (and leaves duplicate code).

**Code (Sysops Squad ADR for the choice):**
```
ADR: Migration Using the Component-Based Decomposition Approach

Decision: Use component-based decomposition. The application has well-defined
component boundaries, lending itself to the component-based decomposition
approach. This approach reduces the chance of having to maintain duplicate
code within each service.

Consequences: The migration effort will likely take longer than with tactical
forking. However, the justifications outweigh this trade-off.
```
*Ref: Hardparts.md — "Component-Based Decomposition" / "Tactical Forking" / "Sysops Squad Saga: Choosing a Decomposition Approach"*

---

### Six Component-Based Decomposition Patterns
**Principle:** Apply these patterns in sequence during monolith migration; treat as a roadmap.

**The six patterns:**
1. **Identify and Size Components Pattern** — catalog components, percent of code, statements, files.
2. **Gather Common Domain Components Pattern** — consolidate common *domain* logic (not infrastructure).
3. **Flatten Components Pattern** — remove unnecessary abstraction layers; enforce "no code in root namespaces".
4. **Determine Component Dependencies Pattern** — map and refactor inter-component dependencies.
5. **Create Component Domains Pattern** — group related components into domains.
6. **Create Domain Services Pattern** — physically separate domains into deployable units.

**Do:**
- Size components within 1-2 standard deviations of the mean size.
- Use **percent** of code (statements / total statements) as the primary sizing metric.
- Apply a fitness function that "no component shall exceed X% of the overall codebase".
- Issue an **architecture story** (not a user story) when refactoring impacts the structural architecture.

**Don't:**
- Treat technical partitioning as the same as domain partitioning.
- Leave source code in a root namespace — write a fitness function that fails on it.

**Code (Identify-and-Size component inventory):**
```
# Pseudocode for maintaining component inventory
LIST prior_list = read_from_datastore()
LIST current_list = identify_components(root_directory)
LIST added_list = find_added(current_list, prior_list)
LIST removed_list = find_removed(current_list, prior_list)
IF added_list NOT EMPTY { add_to_datastore(added_list); send_alert(added_list) }
IF removed_list NOT EMPTY { remove_from_datastore(removed_list); send_alert(removed_list) }
```
**Code (size by percent threshold):**
```
LIST component_list = identify_components(root_directory)
total_statements = accumulate_statements(root_directory)
FOREACH component IN component_list {
  component_statements = accumulate_statements(component)
  percent = component_statements / total_statements
  IF percent > .10 { send_alert(component, percent) }
}
```
**Code (size by standard deviation):**
```
std_dev = square_root(square_diff_sum / (num_components - 1))
FOREACH component.size IN component_size_map {
  diff_from_mean = absolute_value(size - mean)
  num_std_devs = diff_from_mean / std_dev
  IF num_std_devs > 3 { send_alert(component, num_std_devs) }
}
```
*Ref: Hardparts.md — "Identify and Size Components Pattern" / "Gather Common Domain Components Pattern" / "Flatten Components Pattern" / "Determine Component Dependencies Pattern" / "Create Component Domains Pattern" / "Create Domain Services Pattern"*

---

### Data Decomposition: 5-Step Process
**Principle:** Decompose the database only after the code is well-componentized.

**The five steps:**
1. Analyze database and create data domains.
2. Assign tables to data domains.
3. Separate database connections to data domains (use distinct connection pools per domain).
4. Move schemas to separate database servers (the moment of truth — typically read-only then switchover).
5. Switch over to independent database servers (cut traffic).

**Do:**
- Distinguish *data disintegrators* (domain separation, data ownership, characteristics, volatility, relationships) from *data integrators* (transactions, referential integrity, queries, shared tables).
- Use **database type optimization** to pick the right tool per data domain (relational / key-value / document / column-family / graph / NewSQL / cloud-native / time-series).
- Move schema-as-unit before moving database-as-unit.
- Create the new schema on the new DB before migrating any traffic.

**Don't:**
- Migrate all tables to all databases ("spread = combine back into monolithic").
- Connect a service to multiple schemas without a data-domain sharing decision.
- Assume one DB technology fits all data — relational fails on aggregations for analytics.

**Code (Step 3 — separate connections):**
```
A service MUST NOT connect to multiple data domains (schemas).
If a service needs access to another domain's tables:
  - Either form a data domain (shared schema, shared ownership)
  - Or use a delegate technique (pass data through event message)
```
*Ref: Hardparts.md — "Decomposing Monolithic Data" / "Step 1-5" / "Data Decomposition Drivers"*

---

### Database Type Selection per Data Domain
**Principle:** Polyglot persistence — pick the database optimized for each domain's access pattern.

**Do:**
- Use **Relational** (RDBMS) for transactional integrity, complex joins, ACID.
- Use **Key-Value** (Redis, DynamoDB) for fast lookup by key, high-write throughput.
- Use **Document** (MongoDB, CouchDB) for aggregate-oriented data with flexible schema.
- Use **Column-Family** (Cassandra, HBase) for time-series-ish wide rows with column-level sparsity.
- Use **Graph** (Neo4j, JanusGraph) for relationship-heavy traversal; choose keys in *graph terms*.
- Use **NewSQL** (CockroachDB, Spanner) for global-scale ACID on distributed nodes.
- Use **Cloud-Native** (Aurora, Cosmos DB) for managed service replacement of legacy RDBMS.
- Use **Time-Series** (InfluxDB, TimescaleDB) for high-cardinality timestamped data.

**Don't:**
- Use a single database for all domains just for simplicity.
- Use relational as the default for everything (a frequent, costly mistake).
- Mix OLTP and OLAP workloads in a single database.

*Ref: Hardparts.md — "Selecting a Database Type" / "Relational Databases" / "Key-Value Databases" / "Document Databases" / "Column Family Databases" / "Graph Databases" / "NewSQL Databases" / "Cloud Native Databases" / "Time-Series Databases"*

---

### Service Granularity — Disintegrators
**Principle:** Six forces push services apart into smaller pieces.

**The six disintegrators:**
1. **Service Scope and Function** — weak cohesion = one service doing too many unrelated things (Single-Responsibility Principle applied to services).
2. **Code Volatility** — parts changing at very different rates (volatility-based decomposition).
3. **Scalability and Throughput** — different scaling needs (e.g., SMS: 220,000/min vs. postal: 1/min).
4. **Fault Tolerance** — crashing sub-features should not take down the whole service.
5. **Security** — separate function-level access (PCI/PII handling).
6. **Extensibility** — planned additions (e.g., new payment types).

**Do:**
- Measure change frequency objectively via version-control change logs.
- Measure throughput objectively before breaking apart.
- Always check that the "leftover" functionality still has strong cohesion (`Email Service + SMS-Letter Service` is a poor name; `Email Service + SMS Service + Letter Service` is good).
- Use security access path as a disintegrator only when sensitive function isolation matters, not just data isolation.

**Don't:**
- Break apart because "microservices should be small" — single-responsibility is subjective.
- Create an "Other" service — it's a sign of over-disintegration.
- Use extensibility as a primary disintegrator until a pattern is established.

*Ref: Hardparts.md — "Service Scope and Function" / "Code Volatility" / "Scalability and Throughput" / "Fault Tolerance" / "Security" / "Extensibility"*

---

### Service Granularity — Integrators
**Principle:** Four forces push services back together.

**The four integrators:**
1. **Database Transactions** — single ACID unit required → keep in one service.
2. **Workflow and Choreography** — too much synchronous interservice communication (every request Service A → B → C → ... adds ~300ms).
3. **Shared Code** — frequent changes to shared *domain* code.
4. **Data Relationships** — inter-table dependencies make back-and-forth communication inevitable.

**Do:**
- Apply the **30/70 rule of thumb**: if ≥30% of requests require workflow between services to complete, consider consolidating.
- Use the rule to find the "right balance" (the secret of getting granularity right).
- Distinguish *shared domain code* (drive to consolidate) from *shared infrastructure code* (orthogonal — use sidecars).

**Don't:**
- Reorganize database table relationships purely to support service granularity (rarely feasible).
- Treat "shared code" generically — domain vs. infrastructure make opposite recommendations.

**Code (illustrative rule):**
```
If 30% of requests require workflow A↔B↔C and 70% are atomic to one service,
keeping them separate is OK. If 70% require workflow, consolidate.

300ms latency per interservice hop × N hops ⇒ performance cliff.
```
*Ref: Hardparts.md — "Database Transactions" / "Workflow and Choreography" / "Shared Code" / "Data Relationships" / "Finding the Right Balance"*

---

### Code Reuse: Four Patterns
**Principle:** Choose your code-reuse technique by rate of change, not by aesthetics.

**Pattern Decision Matrix:**
| Pattern | Best when | Worst trade-off |
|---|---|---|
| **Code Replication** | Static, one-off (annotations, markers) | Defects propagate to every service |
| **Shared Library** (JAR/DLL) | Stable abstractions, low-to-moderate change | Version matrix becomes a "distributed monolith" |
| **Shared Service** | High change rate, polyglot codebases | Latency / fault tolerance / scale coupling |
| **Sidecar / Service Mesh** | Operational coupling only (logging, monitoring, auth) | Sidecar becomes bloat; not for domain classes |

**Do:**
- Use **fine-grained** shared libraries (security, formatters, calculators) — coarse-grained `SharedStuff.jar` becomes a version-deprecation nightmare.
- Always version shared libraries; never use `LATEST`.
- Use custom deprecation strategy per shared library (security: 2-3 versions; calculators: 10+).
- Put only **operational coupling** in sidecars (logging, monitoring, auth, discovery, circuit breakers) — never domain classes.

**Don't:**
- Replicate code that has bugs or will change.
- Treat "reuse = good" without analyzing rate of change (reuse derives from *abstraction* but is operationalized by *slow rate of change*).
- Add JSONtoXML or domain utilities to sidecars just because "everyone needs it once" — measure how many teams.
- Use shared services for low-change shared code — performance/scale/fault-tolerance overhead dominates.

**Code (Java service entry point annotation — a good replication candidate):**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ServiceEntrypoint {}
/* Usage:
@ServiceEntrypoint
public class PaymentServiceAPI {
  ...
}
*/
```
**Code (C# attribute version — same idea):**
```csharp
[AttributeUsage(AttributeTargets.Class)]
class ServiceEntrypoint : Attribute {}
/* Usage:
[ServiceEntrypoint]
class PaymentServiceAPI {
  ...
}
*/
```
**Code (API endpoint versioning — bad practice for shared services):**
```
app/1.0/discountcalc?orderid=123
app/1.1/discountcalc?orderid=123
app/1.2/discountcalc?orderid=123
app/1.3/discountcalc?orderid=123
latest change -> app/1.4/discountcalc?orderid=123
```
*Ref: Hardparts.md — "Code Replication" / "Shared Library" / "Dependency Management and Change Control" / "Versioning Strategies" / "Shared Service" / "Change Risk" / "Performance" / "Scalability" / "Fault Tolerance" / "Sidecars and Service Mesh" / "Orthogonal Coupling" / "Reuse via Platforms"*

---

### Data Ownership: Single, Common, Joint
**Principle:** Table ownership = the service that performs *write* operations on the table.

**Do:**
- Apply **Single Ownership** (simplest) when only one service writes the table.
- Apply **Common Ownership** when multiple services need read access — use a cross-service read contract.
- Resolve **Joint Ownership** with one of four techniques: **Table Split**, **Data Domain**, **Delegate**, or **Service Consolidation**.

**Don't:**
- Assign ownership based on which service reads most — ownership is defined by *write* authority.
- Have multiple services write the same table directly without an explicit technique.

*Ref: Hardparts.md — "Assigning Data Ownership" / "Single Ownership Scenario" / "Common Ownership Scenario" / "Joint Ownership Scenario"*

---

### Resolving Joint Ownership: Four Techniques

**1. Table Split Technique:** Split the table along domain seams so each part has a single owner.
*Ref: Hardparts.md — "Table Split Technique"*

**2. Data Domain Technique:** Put tables shared by multiple services into a common schema both services connect to.
**Constraint:** A service may not connect to multiple data domains (schemas).
*Ref: Hardparts.md — "Data Domain Technique"*

**3. Delegate Technique:** Assign ownership to one service; the other passes required data along with an event message (e.g., Ticket Completion Service passes survey data along with the notification event so Survey Service owns the Survey table).
*Ref: Hardparts.md — "Delegate Technique"*

**4. Service Consolidation Technique:** Merge services with too much shared data into one service.
*Ref: Hardparts.md — "Service Consolidation Technique"*

**Code (Sysops Squad ADR for delegate technique — joint Survey ownership):**
```
ADR: Survey Service Owns the Survey Table

Decision: The Survey Service will be the single owner of the Survey table,
meaning it is the only service that can perform write operations to that table.

Once a ticket is marked as complete and is accepted by the system, the Ticket
Completion Service needs to send a message to the Survey Service to kick off
the customer survey processing. Since the Ticket Completion Service is already
sending a notification event, the necessary ticket information can be passed
along with that event, thus eliminating the need for the Ticket Completion
Service to have any access to the Survey table.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Data Ownership for Ticket Processing"*

---

### Distributed Transactions — The BASE Trade-Off
**Principle:** Distributed transactions replace ACID with BASE (Basically Available, Soft state, Eventual consistency).

**Do:**
- Avoid cross-service transactions when possible.
- Treat compensating transactions as a fact of life in distributed architectures.
- Use **state management** (state machines) instead of compensating updates where possible — saga moves to NO_SURVEY state, retries asynchronously.

**Don't:**
- Believe Epic Saga (distributed transactions) is "clean" — they have legendary failure modes.
- Trust naive trust in distributed ACID — coordination failures, deadlocks, race conditions are common.
*Ref: Hardparts.md — "Distributed Transactions"*

---

### Three Eventual Consistency Patterns

**Pattern Decision Matrix:**
| Pattern | Best when | Worst trade-off |
|---|---|---|
| **Background Synchronization** | Closed heterogeneous systems (no direct communication) | Data source coupling; business logic duplicated; slow consistency |
| **Orchestrated Request-Based** | Complex workflows needing atomic feel | Slower responsiveness; complex error handling |
| **Event-Based (pub/sub)** | Most modern distributed + microservices | DLQ complexity; consumer must be durably subscribed |

**Do:**
- Use **durable subscribers** for pub/sub messaging so receivers don't lose messages when offline.
- Configure **dead-letter queues (DLQ)** with a chain of retries → automated repair → human intervention.
- With Kafka, persist messages in the topic for a reasonable period.

**Don't:**
- Use background synchronization in architectures requiring tight bounded contexts (breaks them).
- Forget the asymmetry: in event-based, ONE consumer must own the durable-subscription contract.

*Ref: Hardparts.md — "Background Synchronization Pattern" / "Orchestrated Request-Based Pattern" / "Event-Based Pattern"*

---

### Distributed Data Access: Four Patterns

**Pattern Decision Matrix:**
| Pattern | Latency | Fault Tolerance | Consistency |
|---|---|---|---|
| **Interservice Communication** | network + security + data | None if owner is down | Eventual by definition |
| **Column Schema Replication** | Single SQL join | High | Eventually consistent (sync overhead) |
| **Replicated Caching** (Hazelcast/Ignite/Coherence) | In-memory nanoseconds | High (if cache exists) | Bounded by replication lag |
| **Data Domain** | Single SQL join (same schema) | High | Strong (same DB) |

**Do:**
- Use column replication sparingly — re-sync complexity explodes with criticality.
- Configure replicated cache startup behavior carefully — owning service must populate first time, but not for subsequent instances.
- Use data domain as the last resort (sacrifices bounded context for performance).
- Account for ~30-300ms network + ~20-400ms security + ~10-50ms data latency per interservice call.

**Don't:**
- Use replicated caching when cache size × instance count drains memory (e.g., 500MB × 5 instances = 2.5GB).
- Use replicated caching for highly volatile data (inventory counts); great for static data (product descriptions).
- Underestimate the TCP/IP broadcast setup overhead in cloud/container environments.

*Ref: Hardparts.md — "Interservice Communication Pattern" / "Column Schema Replication Pattern" / "Replicated Caching Pattern" / "Data Domain Pattern"*

---

### Orchestration vs. Choreography Communication Style
**Principle:** Two generic workflow styles; semantic coupling dictates which.

**Orchestration** — central orchestrator owns state and workflow.

| Advantages | Disadvantages |
|---|---|
| Centralized workflow | Bottleneck responsiveness |
| Easier error handling | Single point of failure |
| Recoverability via retry | Limited scalability |
| State management | Service coupling |
| | No global "ESB" — orchestrator per workflow |

**Choreography** — services collaborate via events; no central state owner.

| Advantages | Disadvantages |
|---|---|
| Higher scalability | Distributed workflow (no single owner) |
| Better responsiveness | Harder state management |
| Better fault tolerance (no SPOF) | Harder error handling |
| Service decoupling | Lower recoverability |

**Do:**
- Use **orchestration for complex workflows**, especially those with many error paths.
- Use **choreography for simple workflows with high throughput / infrequent errors**.
- Model both options for the workflow before deciding.

**Don't:**
- Default to orchestration because it "looks like microservices" (a global ESB is the anti-pattern).
- Confuse absence of orchestrator with absence of state — state always lives somewhere.

*Ref: Hardparts.md — "Orchestration Communication Style" / "Choreography Communication Style" / "Workflow State Management" / "Trade-Offs Between Orchestration and Choreography"*

---

### Workflow State Management in Choreography
**Principle:** Three techniques to handle state when there's no orchestrator.

**1. Front Controller pattern** — first-called domain service owns state (pseudo-orchestrator with domain responsibility too).
**2. Stateless choreography** — query all services to assemble the state on demand (high performance/scale; complexity rises fast).
**3. Stamp coupling** — embed workflow state in the message contract (each service updates its portion).

**Do:**
- Use stamp coupling to carry minimal workflow context between services.
- Match state-management approach to complexity: simple → stateless; complex → front controller or migrate to orchestration.

**Don't:**
- Put workflow state in domain services without considering the trade-offs of additional responsibility.
- Rely on stateless choreography for complex workflows.

*Ref: Hardparts.md — "Front Controller pattern" / "Stateless choreography" / "Stamp coupling for workflow management"*

---

### The Saga Matrix: 3 Dimensions × 8 Patterns
**Principle:** Three dimensions — Communication, Consistency, Coordination — combine into eight named saga patterns.

**Master matrix — Communication × Consistency × Coordination:**
| Pattern | Comm | Cons | Coord | Coupling | Best use |
|---|---|---|---|---|---|
| **Epic Saga (sao)** | Sync | Atomic | Orchestrated | Very high | Familiar "traditional" saga — bottleneck risks |
| **Phone Tag Saga (sac)** | Sync | Atomic | Choreographed | High | Simple sync workflows needing scale |
| **Fairy Tale Saga (seo)** | Sync | Eventual | Orchestrated | High | **Best balance** — popular in microservices |
| **Time Travel Saga (sec)** | Sync | Eventual | Choreographed | Medium | Fire-and-forget high-throughput |
| **Fantasy Fiction Saga (aao)** | Async | Atomic | Orchestrated | High | Misguided attempt to improve Epic — avoid |
| **Horror Story (aac)** | Async | Atomic | Choreographed | Medium | Most difficult combination — avoid |
| **Parallel Saga (aeo)** | Async | Eventual | Orchestrated | Low | **Complex workflows with high scale** |
| **Anthology Saga (aec)** | Async | Eventual | Choreographed | Very low | **Highest throughput / extreme scale** |

**Do:**
- Default to **Fairy Tale Saga (seo)** for most microservices architectures — orchestrator + sync + eventual is easiest to model and reason about.
- Choose **Parallel Saga (aeo)** when the workflow needs high scale and tolerates eventual consistency.
- Choose **Anthology Saga (aec)** for "Pipes and Filters" style high-throughput scenarios.

**Don't:**
- Default to **Epic Saga (sao)** just because it mirrors monolithic transactions.
- Combine asynchronous communication with atomic consistency (Fantasy Fiction, Horror Story) — they have race conditions, deadlocks, debugging nightmares.
- Forget that these are dimensions, not memory points — the more coupling, the worse scale.

*Ref: Hardparts.md — "Transactional Saga Patterns"*

---

### Saga Pattern Ratings Table (consolidated)
**Principle:** Compare patterns across coupling, complexity, responsiveness, scale.

```
Pattern              | Coupling   | Complexity | Resp/Avail | Scale/Elast
-------------------- | ---------- | ---------- | ---------- | -----------
Epic Saga            | Very high  | Low        | Low        | Very low
Phone Tag Saga       | High       | High       | Low        | Low
Fairy Tale Saga      | High       | Very low   | Medium     | High
Time Travel Saga     | Medium     | Low        | Medium     | High
Fantasy Fiction Saga | High       | High       | Low        | Low
Horror Story         | Medium     | Very high  | Low        | Medium
Parallel Saga        | Low        | Low        | High       | High
Anthology Saga       | Very low   | High       | High       | Very high
```
*Ref: Hardparts.md — Table 15-2 "Consolidated comparison of dynamic coupling patterns"*

---

### Epic Saga (sao) — Default to Avoid
**Principle:** Synchronous + Atomic + Orchestrated = bottleneck AND atomic consistency burden.

**Do:**
- Use only when the requirement for ACID-like coordination is non-negotiable and scale needs are modest.
- Plan for compensating transactions — error conditions are the hard part.

**Don't:**
- Default to it because "we always used ACID". Most other patterns give better trade-offs.

**Code (failure path):**
```
Mediator monitors success of calls; if last service fails,
mediator sends compensating requests to the other two services
to undo the operation from before, returning state to pre-transaction.
```
*Ref: Hardparts.md — "Epic Saga(sao) Pattern"*

---

### Fairy Tale Saga (seo) — Best Balance
**Principle:** Sync + Eventual + Orchestrated = simplest story with a happy ending.

**Do:**
- Adopt as default for many microservices architectures.
- Use an orchestrator that handles error handling and retry, but not transactionality.

**Don't:**
- Use when one operation depends on another's success atomically.
*Ref: Hardparts.md — "Fairy Tale Saga(seo) Pattern"*

---

### Parallel Saga (aeo) — Best Complex-Workflow Pattern
**Principle:** Async + Eventual + Orchestrated = scale + complexity tolerance.

**Do:**
- Use for complex workflows with multiple services that can run concurrently.
- Mediator handles retries and compensations asynchronously.

**Don't:**
- Use when each service must complete before the next can start (you'd need synchronous).

*Ref: Hardparts.md — "Parallel Saga(aeo) Pattern"*

---

### Anthology Saga (aec) — Best for Pipes-and-Filters
**Principle:** Async + Eventual + Choreographed = maximum decoupling + throughput.

**Do:**
- Use for "fire and forget" pipelines (electronic data ingestion, bulk transactions).
- Pair with stamp coupling if downstream services need workflow context.

**Don't:**
- Use for critical workflows with complex error handling.

*Ref: Hardparts.md — "Anthology Saga(aec) Pattern"*

---

### Saga State Machines (over Compensating Updates)
**Principle:** Track saga state with a finite state machine; correct errors via retries rather than compensating transactions.

**Do:**
- Model every state and transition in a table.
- Move saga to a `NO_SURVEY` (or similar) state if Survey Service is unavailable; let the orchestrator retry asynchronously.
- Return success to the user immediately; resolve errors out-of-band.

**Don't:**
- Block the user while the saga resolves errors.
- Issue compensating transactions for every error path.

**Code (saga state table for Sysops Squad ticket):**
```
Initiating state | Transition state | Transaction action
------------------|------------------|------------------------
START             | CREATED          | Assign ticket to expert
CREATED           | ASSIGNED         | Route to expert device (wait if no expert)
ASSIGNED          | ACCEPTED         | Expert acknowledges
ACCEPTED          | COMPLETED        | Expert finishes repair
ACCEPTED          | REASSIGN         | Expert can't finish
REASSIGN          | ASSIGNED         | Find new expert
COMPLETED         | CLOSED           | Survey sent + completed
COMPLETED         | NO_SURVEY        | Survey not sentable; orchestrator retries
NO_SURVEY         | CLOSED           | Survey sent on retry
```
*Ref: Hardparts.md — "Saga State Machines" / "State Management and Eventual Consistency"*

---

### Strict vs. Loose Contracts
**Principle:** Strict contracts give guaranteed fidelity; loose contracts give maximum decoupling. Trade-off depends on audience.

**Strict contracts (gRPC, Avro, OpenAPI)** — explicit schema, typed, version-controlled.
**Loose contracts (REST/JSON name-value pairs)** — flexible, decoupled, schema-less.

| Strict | Loose |
|---|---|
| Guaranteed contract fidelity | Highly decoupled |
| Versioned | Easier to evolve |
| Build-time verification | Contract management issues |
| Better documentation | Requires fitness functions |

**Do:**
- Use strict contracts for *internal* services where both sides are controlled.
- Use loose contracts for *external* APIs and unstable domains.
- Hybridize: strict contracts where they fit, loose where they don't.

**Don't:**
- Assume loose contracts come for free — they need fitness-function governance (consumer-driven contracts).
- Use strict contracts for partner APIs you don't control.

*Ref: Hardparts.md — "Strict Versus Loose Contracts" / "Trade-Offs Between Strict and Loose Contracts"*

---

### Consumer-Driven Contracts (CDCs)
**Principle:** A *pull* model where consumers specify the contract; providers honor it in their build.

**Do:**
- Use **consumer-driven contracts** to bridge the loose-contract + contract-fidelity gap.
- Embed CDC tests in provider CI/CD to stay green at all times.
- Combine two simple mechanisms (name-value pairs + CDC tests) rather than one elaborate schema tool.

**Don't:**
- Rely on CDCs in teams with low engineering maturity (they get skipped).
- Forget the version implication: a CDC update on the consumer side requires a coordinated provider release.

*Ref: Hardparts.md — "Contracts in Microservices" / "Coupling levels" / "Consumer-driven contracts"*

---

### Stamp Coupling
**Principle:** Passing a large data structure between services where each reads only a small portion.

**Do:**
- Use stamp coupling intentionally when the data shape is the domain (e.g., travel-industry standard XML for itineraries).
- Use stamp coupling to carry workflow state between choreographed services (see Time Travel Saga).

**Don't:**
- Pass an entire Customer object when Wishlist only needs the customer's name — over-couples.
- Use stamp coupling casually — it inflates bandwidth and creates unintended breakage (changing an irrelevant field breaks the contract).

**Code (bandwidth anti-pattern):**
```
2,000 req/sec × 500 KB payload = 1,000,000 KB/sec  ←  over-coupling
vs.
200 req/sec × 200 byte payload  =  400 KB/sec     ←  need-to-know
```
*Ref: Hardparts.md — "Stamp Coupling" / "Over-Coupling via Stamp Coupling" / "Bandwidth" / "Stamp Coupling for Workflow Management"*

---

### Analytical Data: Data Warehouse → Data Lake → Data Mesh

**Evolution:**
| Approach | Posture | Strength | Fatal flaw |
|---|---|---|---|
| **Data Warehouse** (Star Schema) | Centralized, schema-on-write | Solves consolidation, fast queries | Integration brittleness; extreme partitioning of domain knowledge; limited functionality for ML |
| **Data Lake** (raw files) | Centralized, schema-on-read | Less up-front transformation | Difficult asset discovery; PII risk; still technically partitioned |
| **Data Mesh** (domain-owned) | Decentralized, peer-to-peer | Aligns ownership to domain, data-as-a-product | Requires federated governance and a platform team |

*Ref: Hardparts.md — "The Data Warehouse" / "The Star Schema" / "The Data Lake" / "The Data Mesh"*

---

### Data Mesh — Four Principles
**Principle:** Align analytical data ownership and architecture with business domains; share data peer-to-peer.

**The four principles:**
1. **Domain ownership of data** — domains most familiar with the data own it.
2. **Data as a product** — domains provide data in a way that delights consumers (with roles, success metrics, discoverable contract).
3. **Self-serve data platform** — platform capabilities for declarative creation, discoverability, lineage.
4. **Computational federated governance** — automated policies embedded in each data product via a sidecar.

**Do:**
- Treat data as a first-class **product** with its own contract, SLAs, ownership.
- Implement a **Data Product Quantum (DPQ)** adjacent to each operational service.
- Use **Async/Eventual (Parallel or Anthology Saga)** for the DPQ-data-plane communication — never with atomicity.
- Add a federated governance sidecar at the point of access (read/write).

**Don't:**
- Treat the data mesh as a panacea — it requires organizational and platform investment.
- Couple operational and analytical data via synchronous atomic consistency — defeats the orthogonal decoupling.
- Use DPQs as if they were services in the operational topology (different governance, different SLAs).

*Ref: Hardparts.md — "Definition of Data Mesh" / "Data Product Quantum" / "Data Mesh, Coupling, and Architecture Quantum" / "When to Use Data Mesh"*

---

### Data Product Quantum (DPQ) Types
**Principle:** Different DPQ types serve different analytical use cases.

**Three DPQ types:**
1. **Source-aligned (native) DPQ** — provides analytical data on behalf of a collaborating service.
2. **Aggregate DPQ** — aggregates from multiple inputs (sync or async per aggregator need).
3. **Fit-for-purpose DPQ** — custom-made for a specific report, ML training, or BI dashboard.

**Do:**
- Make every data product embed its governance sidecar.
- Define DPQs with their own contracts and fitness functions.

**Code (DPQ contract example):**
```
type Profile {
  name: String
  addr1: String
  addr2: String
  country: String
  ...
}
```
*Ref: Hardparts.md — "Data Product Quantum"*

---

### Build Your Own Trade-Off Analysis
**Principle:** Three-step process for modern trade-off analysis.

**The three steps:**
1. **Find entangled dimensions** — what is braided together?
2. **Analyze coupling points** — how are parts coupled?
3. **Assess trade-offs** — what's the impact of change?

**Do:**
- Use **MECE lists** (Mutually Exclusive, Collectively Exhaustive) to compare like things.
- Apply **qualitative** analysis (not quantitative) for cross-architecture comparison.
- **Model relevant domain cases** — pay an external credit card processor synchronously or asynchronously?
- **Prefer bottom line** over overwhelming evidence — boil to ~3 options.
- Build **iterative** what-if diagrams before committing.
- Build **fitness functions** for monitoring qualitative -> quantitative drift.

**Don't:**
- Fall into the **out-of-context trap**: a trade-off matrix that favors one option overall may flip when contextual drivers are added.
- Allow others to force you into evangelizing a position — bring it back to trade-offs.
- Optimize for *maximum* of one driver — go for *least worst*.
- Show non-technical stakeholders every technical detail (overwhelms them).

**Code (consumer-scenario summary — an architecture's bottom line):**
```
Synchronous                           Asynchronous
+ Credit approval guaranteed         + Customer doesn't wait for CC
  to start before customer request      to start
  ends
                                     + Application submission not
- Customer waits for CC process         dependent on orchestrator down
  to start
- Customer application rejected
  if orchestrator is down
```
*Ref: Hardparts.md — "Build Your Own Trade-Off Analysis" / "Finding Entangled Dimensions" / "Coupling" / "Analyze Coupling Points" / "Qualitative Versus Quantative Analysis" / "MECE Lists" / "The 'Out-of-Context' Trap" / "Model Relevant Domain Cases" / "Prefer Bottom Line over Overwhelming Evidence" / "Avoiding Snake Oil and Evangelism"*

---

### Operational vs. Analytical Data Separation
**Principle:** OLTP (operational) and OLAP (analytical) data have fundamentally different purposes and must be separated.

**Do:**
- Treat data as living longer than any architecture (Tim Berners-Lee).
- Make data architects and application architects collaborate from the start.
- Distinguish *operational* (sales, transactions, inventory — OLTP) from *analytical* (reports, ML, trends — OLAP).
- Remember that business depends on operational data; strategic decisions depend on analytical data.

**Don't:**
- Treat analytical data as a simple extension of operational data.
- Conflate "shared" and "operational" — they're different roles.

*Ref: Hardparts.md — "The Importance of Data in Architecture"*

---

### Definition Glossary (working vocabulary for Hardparts)

```
Service         Cohesive functionality deployed as an independent executable.
Component       Architectural building block — namespace/package/physical grouping.
Coupling        "Two artifacts are coupled if a change in one might require
                a change in the other to maintain proper functionality."
Sync comm       Caller waits for response before proceeding.
Async comm      Caller doesn't wait; optionally notified via separate channel.
Orchestrated    Workflow includes a service whose primary responsibility is
                to coordinate the workflow.
Choreographed   Workflow has no orchestrator; services share coordination.
Atomic          All parts of workflow maintain consistent state at all times.
Eventual        Soft state; converges to consistent state over time.
Contract        Interface between two software parts (broad: method/integration).
Static coupling        How services are wired (deps, DBs, brokers).
Dynamic coupling       How services call each other at runtime.
Architecture quantum   Independently deployable artifact with high
                       functional cohesion and high static coupling.
Fitness function       Objective, executable integrity assessment of an
                       architectural characteristic.
ADR                    Short text file documenting a single architecture
                       decision (Context/Decision/Consequences).
Horror Story           Async + Atomic + Choreographed — avoid.
```
*Ref: Hardparts.md — "Architecture Versus Design: Keeping Definitions Simple" / Glossary endnote*

---

## Anti-Patterns & Common Mistakes
- **Big Ball of Mud:** code without observable internal structure; can't apply decomposition patterns without restructuring first. *Fix:* assess with JDepend + abstractness/instability metrics first.
- **SharedStuff.jar / Coarse-grained shared library:** every change forces every consumer to redeploy. *Fix:* fine-grained, functionally partitioned libraries with per-library deprecation.
- **Distributed monolith:** microservices deployed as a complete set in specific order — none of the benefits, all of the operational pain. *Fix:* if shared library change requires coordinated deployment across services, the granularity is wrong.
- **Epic Saga default:** synchronous + atomic + orchestrated chosen because it "feels like monolith". *Fix:* default to Fairy Tale Saga for most microservices.
- **Horror Story combo:** async + atomic + choreographed. *Fix:* relax atomicity, use Anthology or Parallel Saga.
- **Cabal of fitness functions:** interlocking fitness functions that frustrate every team. *Fix:* start with the most important architectural characteristics only.
- **Background Synchronization in microservices:** breaks bounded contexts to keep data sources in sync. *Fix:* use event-based with durable subscribers.
- **Stamp coupling blindly:** passing entire Customer when only name is needed. *Fix:* fields at a "need to know" level.
- **Out-of-context trade-off matrix:** the deck looks fine until context-specific drivers are added. *Fix:* always run iterative design before committing.
- **Background-only "we deploy less often so it's OK":** monolithic deployment cadence caps 2-3 nines of availability at best. *Fix:* modular monolith + microkernel when full distribution is unjustified.
- **Replicated caching for highly volatile data:** replication can't keep up with rapid change; results in conflicts. *Fix:* use replicated caching for static data; use replicated state stores (Hazelcast, Ignite) for volatiles.
- **Data warehouse brittleness:** every schema change in an operational system requires coordinated data-transformation updates. *Fix:* Data Mesh with domain-owned DPQs.
- **Snake-oil evangelism:** touting a particular pattern without acknowledging its trade-offs. *Fix:* demand trade-off tables, not anecdotes.
- **Auto-evangelism:** being forced into the opposing position of an argument without an argument existing. *Fix:* force a real-world trade-off analysis instead of binary positions.
- **Treating LATEST as a pinned version:** hot-fix deployments can fail because the LATEST changed. *Fix:* pin shared-library versions explicitly.

---

## Decision Heuristics / Checklists

### Granularity Decision Heuristic
```
Step 1: Measure code volatility and throughput per functionality area.
Step 2: If small pieces change faster, scale differently, have different 
        fault tolerance or security needs → disintegrate.
Step 3: If pieces share an ACID transaction, talk synchronously >30%
        of the time, share >40% domain code, or own interlocked data 
        tables → integrate back.
Step 4: Verify the leftover has a good (cohesive) name. 
        "OtherNotification" is bad; "SMSLetter" is worse than splitting 
        into SMS + Letter.
Step 5: Validate with business sponsor using the trade-off question:
        "Which matters more — X or Y?" 
```

### Saga Pattern Decision
```
Sync + Atomic + Orchestrated → Epic Saga          (familiar; bottleneck risk)
Sync + Atomic + Choreog.     → Phone Tag Saga     (rare; complex error)
Sync + Eventual + Orchest.   → Fairy Tale Saga    (★ default for many)
Sync + Eventual + Choreog.   → Time Travel Saga   (fire-and-forget)
Async + Atomic + Orchest.    → Fantasy Fiction    (AVOID — race/deadlock)
Async + Atomic + Choreog.    → Horror Story       (AVOID — worst case)
Async + Eventual + Orchest.  → Parallel Saga      (complex wfs + scale)
Async + Eventual + Choreog.  → Anthology Saga     (highest throughput)
```

### Code Reuse Decision
```
Code changes?  Mostly static? → Code Replication or fine-grained Shared Library
Code changes?  Sometimes?    → Shared Library with versioning
Code changes?  Often/polyglot? → Shared Service
For ops only (logging, metrics, auth) → Sidecar / Service Mesh
For domain classes → NEVER Sidecar; use bounded context duplication
```

### Data Ownership Conflict
```
1. Can we split the table by domain seam?        → Table Split
2. Else, do both services need writes?           → Data Domain (shared schema)
3. Else, can the owner receive data via an event? → Delegate
4. Else, merge the services.                     → Service Consolidation
```

### Joint Ownership Resolution Question
```
"Can the other service receive all the data it needs via an event message, 
 rather than direct DB access?" — if YES, Delegate; if NO, consolidate.
```

### Saga Failure Recovery
```
Each error path in the saga = a state machine transition to a recovery state.
Let the orchestrator resolve it asynchronously while the user proceeds.
Retry → automated repair → manual intervention (DLQ-style).
```

### Contract Strictness Decision
```
Internal + both sides controlled?           → Strict (gRPC / Avro / OpenAPI)
External / unstable / partner?              → Loose (JSON name-value pairs)
Loose + need fidelity?                      → Consumer-Driven Contracts
```

### ADR Skeptic's Checklist
- Context includes 1-2 sentence problem + alternatives?
- Decision includes justification, not just choice?
- Consequences mention both upside trade-offs and costs?
- ADR is < 2 pages long?
- ADR is checked into source control?

### Service Mesh Inclusion Rule
```
Include in sidecar ONLY IF:
  - More than ~half the teams use it, AND
  - It is operational (logging, monitoring, auth, discovery, circuit breakers)
EXCLUDE from sidecar IF:
  - It is a domain class (Address, Customer, Order, etc.)
  - Fewer than half the teams use it
  - It is a utility used by a minority (use shared library instead)
```

### Architecture Quanta Identification
```
For each artifact in the architecture:
  1. List OS, framework libs, persistence, integration points, brokers → static deps.
  2. Identify which other artifacts it depends on at runtime → dynamic deps.
  3. A quantum = the smallest independently deployable boundary.
  4. Map style to quantum count: monolith=1, service-based=1, microservices=N.
```

### Trade-Off Analysis Steps (When Stuck)
1. Find entangled dimensions (Communication × Consistency × Coordination).
2. Analyze coupling points (static + dynamic).
3. Assess trade-offs by scoring coupling, complexity, responsiveness, scale.
4. Use MECE lists to keep comparisons valid.
5. Model relevant domain scenarios iteratively.
6. Prefer a 3-row bottom-line table over a 30-row evidence dump.

---

### Identification-and-Size Component Inventory Walk-Through (Sysops Squad)
**Principle:** The Sysops Squad case study measures each component by percent of code; ratios drive the disintegration decisions.

**Do:**
- Compute percent = (statements in component) / (statements in codebase).
- Identify outliers (≥ 2 standard deviations from the mean).
- Refactor outliers via functional decomposition: split a Reporting component into Reporting Shared + Ticket Reports + Expert Reports + Financial Reports.

**The Sysops Squad measurement output:**
```
Before refactor:
  Reporting           33%   27,765 statements   162 files   ← TOO BIG
  Ticket               8%    7,009               45
  Ticket Assign        9%    7,845               14

After refactor:
  Reporting Shared     7%    5,309               20          ← NEW (extracted)
  Ticket Reports       8%    6,955               58          ← NEW
  Expert Reports       9%    7,734               48          ← NEW
  Financial Reports    9%    7,767               36          ← NEW
```
*Ref: Hardparts.md — "Sysops Squad Saga: Sizing Components"*

---

### The Sysops Squad Component Inventory (full)
**Principle:** Real-world monoliths often have well-defined components already; identify them and map their lifecycles.

**Do:**
- Use namespaces (Java) or directory structures (C#) as the component identifier.
- Measure statements per component to size them; flag any component > 20% of the codebase as a candidate for decomposition.

**Component inventory (after size refactor):**
```
Component name        | Namespace                | % | Statements | Files
----------------------|--------------------------|---|------------|------
Login                 | ss.login                 |  2|    1,865   |   3
Billing Payment       | ss.billing.payment       |  5|    4,312   |  23
Billing History       | ss.billing.history       |  4|    3,209   |  17
Customer Notification | ss.customer.notification |  2|    1,433   |   7
Customer Profile      | ss.customer.profile      |  5|    4,012   |  16
Expert Profile        | ss.expert.profile        |  6|    5,099   |  32
KB Maint              | ss.kb.maintenance        |  2|    1,701   |  14
KB Search             | ss.kb.search             |  3|    2,871   |   4
Reporting Shared      | ss.reporting.shared      |  7|    5,309   |  20
Ticket Reports        | ss.reporting.tickets     |  8|    6,955   |  58
Expert Reports        | ss.reporting.experts     |  9|    7,734   |  48
Financial Reports     | ss.reporting.financial   |  9|    7,767   |  36
Ticket                | ss.ticket                |  8|    7,009   |  45
Ticket Assign         | ss.ticket.assign         |  9|    7,845   |  14
Ticket Notify         | ss.ticket.notify         |  2|    1,765   |   3
Ticket Route          | ss.ticket.route          |  2|    1,468   |   4
Support Contract      | ss.supportcontract       |  5|    4,104   |  24
Survey                | ss.survey                |  3|    2,204   |   5
Survey Notify         | ss.survey.notify         |  2|    1,299   |   3
Survey Templates      | ss.survey.templates      |  2|    1,672   |   7
User Maintenance      | ss.users                 |  4|    3,298   |  12
```
*Ref: Hardparts.md — Table 5-3 "Component size after applying the Identify and Size Components pattern"*

---

### ADR: Ticket Assignment Granularity (Consolidated Service)
**Principle:** When assignment and routing are tightly bound synchronously, keep them in a single service even when one changes more often.

**The story:** Taylen's ticket assignment algorithms change 2-3x/month; routing rarely changes. Skyler argued routing must run with assignment (one operation). Addison facilitated: applied the disintegration (volatility) vs. integrator (workflow) trade-off explicitly.

**Code (ADR result):**
```
ADR: Consolidated Service for Ticket Assignment and Routing

Decision: We will create a single consolidated ticket assignment service
for the assignment and routing functions of the ticket.

Tickets are immediately routed to the Sysops Squad expert once they are
assigned, so these two operations are tightly bound and dependent on
each other.

Both functions must scale the same, so there are no throughput
differences between these services, nor is back-pressure needed between
these functions.

Since both functions are fully dependent on each other, fault tolerance
is not a driver for breaking these functions apart.

Making these functions separate services would require workflow between
them, resulting in performance, fault tolerance, and possible reliability
issues.

Consequences: Changes to the assignment algorithm (which occur on a
regular basis) and changes to the routing mechanism (infrequent change)
would require testing and deployment of both functions, resulting in
increased testing scope and deployment risk.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Ticket Assignment Granularity"*

---

### ADR: Customer Registration Granularity (Consolidated Security)
**Principle:** When ALL-or-NOTHING registration is required and security can be controlled via design (a custom library), keep customer functionality in a single service.

**The story:** Product owner demanded atomic registration — "We cannot have a customer record without a corresponding credit card or password record. Ever." Sam (security expert) demanded tokenization + encryption + Tortoise library double-check. Decision: single service + multilevel security access via Tortoise (design controls security, not architecture).

**Code (ADR):**
```
ADR: Consolidated Service for Customer-Related Functionality

Decision: We will create a single consolidated customer service for
profile, credit card, password, and products supported.

Customer registration and unsubscribe functionality *requires* a single
atomic unit of work. A single service would support ACID transactions
to meet this requirement, whereas separate services would not.

Use of the Tortoise security libraries in the API layer and the service
mesh will mitigate security access risk to sensitive information.

Consequences: We will require the Tortoise security library to ensure
security access in both the API gateway and the service mesh. Because
it's a single service, changes to source code for profile info, credit
card, password, or products purchased will increase testing scope and
deployment risk. The combined functionality will have to scale as one unit.

Trade-off: transactionality vs. security. Breaking customer functionality
into separate services would have gained security access control but lost
ACID. We chose atomic transactionality and will control security through
design (Tortoise security libraries).
```
*Ref: Hardparts.md — "Sysops Squad Saga: Customer Registration Granularity"*

---

### ADR: Single-Table Ownership for Bounded Contexts
**Principle:** When only one service writes to a table, that table's owner is the writer — read-only access from elsewhere is allowed only via contract, not direct DB access.

**Code:**
```
ADR: Single Table Ownership for Bounded Contexts

Context: When forming bounded contexts between services and data, tables
must be assigned ownership to a particular service or group of services.

Decision: When only one service writes to a table, that table will be
assigned ownership to that service. Furthermore, services requiring
read-only access to a table in another bounded context cannot directly
access the database or schema containing that table.

Per the database team, table ownership is defined as the service that
performs write operations on a table. Therefore, for single table
ownership scenarios, regardless of how many other services need to
access the table, only one service is ever assigned an owner, and that
owner is the service that maintains the data.

Consequences: Depending on the technique used, services requiring
read-only access to a table in another bounded context may incur
performance and fault-tolerance issues when accessing data in a
different bounded context.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Data Ownership for Ticket Processing"*

---

### ADR: Survey Service Owns the Survey Table (Delegate)
**Principle:** Use the delegate technique when one service can pass all required data to the owner through an event message.

**Code:**
```
ADR: Survey Service Owns the Survey Table

Context: Both the Ticket Completion Service and the Survey Service write
to the Survey table. Because this is a joint ownership scenario, the
alternatives are to use a common shared data domain or use the delegation
technique. Table splitting is not an option because of the structure of
the Survey table.

Decision: The Survey Service will be the single owner of the Survey table,
meaning it is the only service that can perform write operations to that
table.

Once a ticket is marked as complete and is accepted by the system, the
Ticket Completion Service needs to send a message to the Survey Service
to kick off the customer survey processing. Since the Ticket Completion
Service is already sending a notification event, the necessary ticket
information can be passed along with that event, thus eliminating the
need for the Ticket Completion Service to have any access to the Survey
table.

Consequences: All of the necessary data that the Ticket Completion
Service needs to insert into the Survey table will need to be sent as
part of the payload when triggering the customer survey process.

In the monolithic system, the ticket completion inserted the survey
record as part of the completion process. With this decision, the
creation of the survey record is a separate activity from the ticket
creation process and is now handled by the Survey Service.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Data Ownership for Ticket Processing"*

---

### ADR: Orchestration for Primary Ticket Workflow
**Principle:** When a workflow needs workflow control, state queries, AND error handling, the trade-off matrix favors orchestration (the Sysops Squad case settles on orchestration).

**The story:** Addison and Austen couldn't decide. Logan facilitated a trade-off table:
- Workflow control → Orchestration
- State query → Both work
- Error handling → Orchestration

**Code (ADR):**
```
ADR: Use Orchestration for Primary Ticket Workflow

Context: For the primary ticket workflow, the architecture must support
easy tracking of lost or mistracked messages, excellent error handling,
and the ability to track ticket status. Either an orchestration solution
or a choreography solution will work.

Decision: We will use orchestration for the primary ticketing workflow.

We modeled orchestration and choreography and arrived at the trade-offs:
                      Orchestration | Choreography
  Workflow control    +             |
  State query        =             =
  Error handling      +             |

Consequences: The ticketing workflow might have scalability issues
around a single orchestrator, which should be reconsidered if current
scalability requirements change.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Managing Workflows"*

---

### ADR: Loose Contract for Sysops Squad Expert Mobile Application
**Principle:** When the consumer side has a slow update cadence (e.g., app store approval), prefer loose contracts to retain flexibility.

**Code:**
```
ADR: Loose Contract for Sysops Squad Expert Mobile Application

Context: The mobile application used by Sysops Squad experts must be
deployed through the public app store, imposing delays on the ability to
update contracts.

Decision: We will use a loose, name-value-pair contract to pass
information to and from the orchestrator and the mobile application.
We will build an extension mechanism to allow temporary extensions for
short-term flexibility.

Consequences: The decision should be revisited if the app store policy
allows for faster (or continuous) deployment. More logic to validate
contracts must reside in the orchestrator and mobile application.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Managing Ticketing Contracts"*

---

### Sidecar vs. Service-Mesh Discipline (Sysops Squad)
**Principle:** A sidecar is a reusable container owned by a shared infrastructure team — not a free-for-all.

**Do:**
- Define the sidecar's exact responsibilities (monitoring, logging, service discovery, auth, authorization).
- Have the shared infrastructure team own the sidecar build, version, and release.
- Surface a small set of "customers" (the service teams) whose needs shape the sidecar.

**Don't:**
- Let service teams add domain classes to the sidecar.
- Add shared utilities that are only used by a minority of teams.
- Let the sidecar become the biggest part of the architecture (a bloat magnet).

**The Sysops Squad ADR:**
```
ADR: Using a Sidecar for Operational Coupling

Context: Each service in our microservices architecture requires common
and consistent operational behavior; leaving that responsibility to each
team introduces inconsistencies and coordination issues.

Decision: We will use a sidecar component in conjunction with a service
mesh to consolidate shared operational coupling.

The shared infrastructure team will own and maintain the sidecar for
service teams; service teams act as their customers. The following
services will be provided by the sidecar:
  - Monitoring
  - Logging
  - Service discovery
  - Authentication
  - Authorization

Consequences: Teams should not add domain classes to the sidecar, which
encourages inappropriate coupling. Teams work with the shared infra
team to place shared, *operational* libraries in the sidecar if enough
teams require it.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Common Infrastructure Logic"*

---

### Sysops Squad: Reuse Decision ADR (Shared Library over Shared Service)
**Principle:** Empirical change-rate data drives the reuse choice — not opinion.

**The story:** Taylen proposed a shared Ticket Data service (data abstraction). Skyler proposed a shared library (DLL). Addison facilitated trade-off exploration: looked at the repo's commit history — commit history showed *less* change than Taylen believed.

**The ADR (verdict for shared library):**
```
ADR: Use of a Shared Library for Common Ticketing Database Logic

Decision: We will use a shared library for the common ticketing database
logic.

Using a shared library will improve performance, scalability, and fault
tolerance of the customer-facing Ticket Creation service, as well as for
the Ticket Assignment service.

We found that the common database logic code does not change much and is
therefore fairly stable code. Furthermore, change is less risky for the
common database logic because services would need to be tested and
redeployed.

Using a shared library reduces service coupling and eliminates additional
service dependencies, HTTP traffic, and overall bandwidth.

Consequences: Changes to the common database logic in the shared DLL
will require the ticketing services to be tested and deployed, therefore
reducing overall agility for common database logic.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Shared Domain Functionality"*

---

### Stamp Coupling for Workflow — When to Use
**Principle:** Stamp coupling is the *intentional* passing of a large data structure that contains workflow context.

**Do:**
- Use stamp coupling for **legitimate** industry-standard data shapes (e.g., travel-industry standard XML).
- Use stamp coupling as a coordination mechanism in choreographed workflows — embed status, transactional state, error messages into the contract; each service updates its portion.

**Don't:**
- Stamp-couple when the same data could be reduced to the few fields actually needed.
- Stamp-couple to dodge contract redesign.

**Code (stamp coupling for workflow management — pseudo):**
```
BEGIN
  {
    "transactionId": "TX-9921",
    "step": 3,
    "status": "IN_PROGRESS",
    "errors": []
  }
  ServiceA updates {"step": 3, "status": "PARTIAL"}
  ServiceB updates {"step": 3, "status": "COMPLETED", "errors": []}
  ServiceC can read full context from the contract without separate queries.
END
```
*Ref: Hardparts.md — "Stamp Coupling for Workflow Management"*

---

### Star Schema — Dimensional Modeling for Data Warehouses
**Principle:** Separating **facts** (quantitative measures) from **dimensions** (descriptive attributes) is the dimensional modeling pattern powering most data warehouses.

**Do:**
- Use Star Schema for OLAP workloads: simple queries, fast aggregations, multi-dimensional analysis.
- Denormalize deliberately to enable fast OLAP queries (the schema-on-write trade-off).
- Combine facts with time series, location, and product hierarchies.

**Don't:**
- Use Star Schema in operational (OLTP) databases — it's analytically specialized.
- Let Star Schema drive operational reporting — keep transactional models for that.

**Code (Sysops Squad Star Schema example):**
```
FACT_TABLE:        hourly_rate, time_to_repair, distance_to_client
DIM: squad_member  { specialties, person_names }
DIM: store         { location }
```
*Ref: Hardparts.md — "The Star Schema"*

---

### Data Domain vs Database Schema — Identity
**Principle:** A data domain is a logical grouping of tables owned by a bounded context. A database schema is a physical container. They are *not* the same thing.

**Do:**
- Map tables to data domains based on bounded-context ownership.
- Initially, multiple domains may live in a single database schema during the connection-separation step.
- Eventually, when schemas are on separate database servers, each data domain = 1 schema (or set of tables within it).

**Don't:**
- Conflate schema layout with ownership — a schema may host multiple data domains transitively.
- Move tables to different databases based on existing application conventions rather than domain ownership.

*Ref: Hardparts.md — "Data Domain Versus Database Schema"*

---

### Architecture Quanta — Style Comparison Summary
**Principle:** Each architecture style has a quantum count that exposes its true coupling shape.

**Quanta by style:**
```
Monolithic styles                              = 1 quantum
Service-based (separate services, shared DB)   = 1 quantum   (DB forces this)
Mediator event-driven                          = 1 quantum   (orchestrator + DB)
Broker event-driven (no central mediator)      = variable
   - If all services share DB    = 1 quantum
   - If services have own DBs    = N quanta (one per service)
Microservices with micro-frontends             = N quanta (one per service+UI)
Tightly-coupled microservice + monolith UI     = 1 quantum (UI forces this)
```
*Ref: Hardparts.md — "Architecture (Quantum | Quanta)" / "Service-Based Architecture" / "Dynamic Quantum Coupling"*

---

### Saga Idempotency and Retry Discipline
**Principle:** Sagas that span multiple networks must tolerate retries; idempotency is the discipline that keeps retries safe.

**Do:**
- Design saga operations to be **idempotent** — calling them twice has the same effect as calling once.
- Carry a transaction ID through all saga steps; reject duplicate processing.
- Use **durable subscribers** so receivers don't lose messages when offline.

**Don't:**
- Assume network calls are exactly-once — they're at-least-once or at-most-once.
- Mix "first-time" and "duplicate" semantics in the same operation.

*Ref: Hardparts.md — "Techniques for Managing Sagas" / "Event-Based Pattern"*

---

### ADR-Driven Decision-Making Examples Index
**Principle:** Reference library of every ADR created in the Hardparts case study.

**The complete ADR index:**
```
ADR                                              | Chapter
-------------------------------------------------|--------
Migrate to distributed architecture              | Ch 3
Migration using component-based decomposition    | Ch 4
Use of document DB for customer survey           | Ch 6
Consolidated service for ticket assign + route   | Ch 7
Consolidated service for customer-related        | Ch 7
Using a sidecar for operational coupling         | Ch 8
Shared library for common ticketing DB logic     | Ch 8
Single-table ownership for bounded contexts      | Ch 9
Survey service owns the Survey table             | Ch 9
In-memory replicated cache for Expert Profile    | Ch 10
Orchestration for primary ticket workflow        | Ch 11
Loose contract for Sysops Squad mobile app       | Ch 13
```
*Ref: Hardparts.md — Appendix B "Architecture Decision Record References"*

---

### Data Mesh — When to Use
**Principle:** Data Mesh is appropriate when analytical data outlives operational decomposition — i.e., always in distributed architectures.

**When to use Data Mesh:**
- Your architecture is decomposed into bounded contexts at the operational layer.
- Analytical data needs domain expertise to interpret (PII, business semantics).
- The team is willing to invest in a self-serve data platform.
- Domain teams can own data products (data-as-a-product mindset).

**When NOT to use Data Mesh:**
- Single monolith with no analytical complexity (use a warehouse or lake).
- No appetite for federated governance (a centralized warehouse/lake is simpler).
- Domain teams can't take ownership of analytical data products.

*Ref: Hardparts.md — "When to Use Data Mesh"*

---

### Sysops Squad Epilogue: Lessons Learned
**Principle:** Trade-off analysis, fitness functions, and ADRs all together form an architecture discipline.

**The lessons:**
- Look at business drivers before reaching for technical solutions.
- Application teams and data teams must collaborate from the start.
- Analyze trade-offs for every consequential decision.
- ADRs discipline the conversation; fitness functions discipline the implementation.
- Avoid snake oil and evangelism — every solution has trade-offs.

**Quote (Logan, epilogue):**
```
No architect, regardless of their cleverness, can instantly understand the
nuances of a truly unique situation and these nuances constantly present
themselves in complex architectures. Building a matrix of possibilities
informs the modeling exercises an architect might want to do in order to
study the implications of permutating one or more dimensions to see the
resulting effect.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Epilogue"*

---

### Footnote on Second Law of Software Architecture
**Principle:** *Why* is more important than *how*.

**Do:**
- Always articulate the trade-offs (the *why*) when recommending a pattern.
- Move from generic solutions to contextual ones before recommending.

**Don't:**
- Get into endless debates about implementation details (*how*) without first agreeing on the trade-off (*why*).
*Ref: Hardparts.md — "Architecture Versus Design: Keeping Definitions Simple"*

---

### Companion Book References
- *Fundamentals of Software Architecture* (Ford, Richards) — defines the architecture styles referenced in every ADR.
- *Building Evolutionary Architectures* (Ford, Parsons, Kua) — defines fitness functions in depth.
- *Microservices Patterns* (Chris Richardson) — defines the saga pattern classically.
- *Data Mesh* (Zhamak Dehghani) — full treatment of the data product quantum.
*Ref: Hardparts.md — index references*

---

## Key Takeaways
1. **Trade-offs over best practices.** Every architectural decision is a trade-off. Aim for the "least worst" combination.
2. **Architecture quanta** are the fundamental unit of deployment; understand static + dynamic coupling to find them.
3. **Architecture fitness functions** verify architecture characteristics objectively — ask: "Is any domain knowledge required to execute this test?"
4. **ADRs** document every significant decision (Context / Decision / Consequences), kept one to two pages.
5. **Granularity disintegrators** (scope, volatility, scalability, fault tolerance, security, extensibility) push services apart; **integrators** (DB transactions, workflow, shared domain code, data relationships) push them back together.
6. **Six component-based decomposition patterns** (Identify-Size, Gather Common, Flatten, Determine Dependencies, Create Domains, Create Domain Services) form a step-by-step monolith migration.
7. **5-step DB decomposition** (analyze → assign tables → separate connections → move schemas to separate servers → switchover) — data is the hardest part.
8. **Three eventual consistency patterns:** Background Synchronization, Orchestrated Request-Based, Event-Based — last is best for modern microservices with durable subscribers and DLQs.
9. **Four data access patterns:** Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain — choose by latency / fault tolerance / consistency trade-off.
10. **Four code reuse patterns:** Code Replication (static only), Shared Library (fine-grained + versioned), Shared Service (high change), Sidecar / Service Mesh (operational only).
11. **Three contract levels:** Strict (gRPC/Avro/OpenAPI), Loose (JSON NVP), Consumer-Driven (loose + fidelity via CI).
12. **Eight saga patterns** form a 2×2×2 matrix; defaults to **Fairy Tale Saga (seo)** or **Parallel Saga (aeo)** in most microservices; avoid **Horror Story (aac)**.
13. **Saga state machines** beat compensating transactions for user-facing responsiveness.
14. **Orchestration vs. choreography** — orchestrator per workflow (not global), choreography for simple high-throughput pipelines.
15. **Stamp coupling** is a useful technique for *legitimate* industry-standard data shapes and for carrying workflow context, but a dangerous anti-pattern when accidentally over-passing full data structures.
16. **Data Mesh** supersedes Data Warehouse and Data Lake with four principles: domain ownership, data as a product, self-serve platform, federated computational governance.
17. **Data Product Quantum (DPQ)** is a cooperative quantum with Async/Eventual communication to the analytical plane (never atomic with operational data).
18. **OUT-OF-CONTEXT TRAP:** a generic trade-off table can flip when contextual drivers are added — always run iterative what-if diagrams before committing.
19. **QUALITATIVE > QUANTITATIVE** in architecture decisions — there are no absolute numbers.
20. **EVERY ORGANIZATION IS A SNOWFLAKE** — copy the questions, not the answers.

---

## Cross-References
- Related: [[../Designing_Distributed_Systems.md]] (Brendan Burns — Kubernetes + Go pattern catalog that the Hardparts philosophy complements)
- Related: [[../Fundamentals_of_Software_Architecture.md]] (the predecessor book that introduces the architecture styles and quanta referenced here)
- Related: [[../Building_Evolutionary_Architectures.md]] (fitness functions in depth — the primary governance mechanism used throughout)
- Related: [[../Building_Microservices.md]] (microservices patterns Sam Newman — same domain, different trade-off lens)
- Related: [[../Team_Topologies.md]] (team-first architecture; complements Hardparts' service decomposition)
- Related: [[../Monolith_To_Microservices.md]] (migration pragmatics — the operational flipside of Hardparts' decomposition patterns)
- Topic index: [[../INDEX.md]]
