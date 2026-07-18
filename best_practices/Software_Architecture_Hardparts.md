# Software Architecture: The Hard Parts
**Authors:** Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani
**Topic tags:** `#architecture`
**Language focus:** language-agnostic (Java/.NET examples)
**Sources:** `markdown_output/Software Architecture - The Hardparts/Software Architecture - The Hardparts.md` · `summaries/Software_Architecture_Hardparts.md`

## TL;DR
There are no best practices in distributed architecture — only trade-offs. Strive for the "least worst" combination. Every hard decision (granularity, data ownership, distributed transactions, contracts, coordination) is resolved by named trade-off drivers, ADRs, and architecture fitness functions that verify the decision objectively.

---

## Best Practices by Topic

### Core Philosophy: Trade-Offs Over Best Practices

**Principle:** Don't maximize — minimize pain.

**Do:**
- Treat every architectural decision as a trade-off between entangled dimensions.
- Document every significant decision as an ADR (Context / Decision / Consequences).
- Encode architectural characteristics as objective fitness functions and run them continuously.
- Use MECE lists so the things you compare are mutually exclusive and collectively exhaustive.

**Don't:**
- Search for a single "best" pattern — every organization is a snowflake.
- Default to a saga pattern (e.g. Epic Saga) because it feels familiar to monolithic ACID.
- Combine conflicting techniques in isolation (e.g. async + atomic + choreographed → Horror Story).
- Adopt a snake-oil "share nothing" rule without measuring its cost.

**Code:**
```
Don't try to find the best design in software architecture;
instead, strive for the least worst combination of trade-offs.
```
*Ref: Hardparts.md — "What Happens When There Are No 'Best Practices'?"*

```
*ADR: A short noun phrase containing the architecture decision*

*Context*
...one- or two-sentence description of the problem, list of alternatives.

*Decision*
...the architecture decision and detailed justification.

*Consequences*
...consequences after the decision is applied; trade-offs considered.
```
*Ref: Hardparts.md — "Architectural Decision Records"*

---

### Architecture Quanta & Coupling

**Principle:** A quantum is an independently deployable unit with high functional cohesion and high static coupling. Find your quanta before picking a style.

**Do:**
- Model static coupling (OS/container, transitive deps, persistence, integration points, brokers) and dynamic coupling (communication × consistency × coordination).
- Treat the database as part of a quantum — a shared DB forces a single quantum.
- Map your style to its quantum count: monolith=1, service-based=1 (shared DB), microservices=N, event-driven=variable.

**Don't:**
- Assume functional decomposition equals deployment decomposition.
- Allow a shared database to silently collapse multiple services into one quantum.

**Code:**
```
Two artifacts (including services) are coupled if a change in one
might require a change in the other to maintain proper functionality.
```
*Ref: Hardparts.md — "Architecture Versus Design: Keeping Definitions Simple"*

Dynamic quantum coupling dimensions: Communication (sync/async) × Consistency (atomic/eventual) × Coordination (orchestrated/choreographed).
*Ref: Hardparts.md — "Dynamic Quantum Coupling"*

---

### Architectural Fitness Functions

**Principle:** Fitness functions are objective, executable checks that verify architectural characteristics — not domain behavior.

**Do:**
- Classify by scope: atomic (single characteristic) vs holistic (combination).
- Trigger continuously in CI/CD; treat manual ones as exceptions.
- Use them to govern layers, prevent cycles, detect contract drift, govern service mesh sidecar inclusion.
- Use JDepend / ArchUnit / NetArchTest for code-level fitness functions.
- Use consumer-driven contract tests as architectural fitness functions.

**Don't:**
- Over-engineer a "cabal" of interlocking fitness functions that frustrate teams.
- Conflate fitness functions with unit tests — fitness functions validate architecture characteristics, not domain criteria. Ask: "Is any domain knowledge required to execute this test?"

**Code:**
```java
public class CycleTest {
    private JDepend jdepend;
    @BeforeEach void init() {
        jdepend = new JDepend();
        jdepend.addDirectory("/path/to/project/persistence/classes");
        jdepend.addDirectory("/path/to/project/web/classes");
    }
    @Test void testAllPackages() {
        Collection packages = jdepend.analyze();
        assertEquals("Cycles exist", false, jdepend.containsCycles());
    }
}
```
*Ref: Hardparts.md — "Using Fitness Functions" — Example 1-1*

```java
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```
*Ref: Hardparts.md — "Using Fitness Functions" — Example 1-2*

```csharp
var result = Types.InCurrentDomain()
    .That().ResideInNamespace("NetArchTest.SampleLibrary.Presentation")
    .ShouldNot().HaveDependencyOn("NetArchTest.SampleLibrary.Data")
    .GetResult().IsSuccessful;
```
*Ref: Hardparts.md — "Using Fitness Functions" — Example 1-3*

---

### Service Granularity — Disintegrators vs Integrators

**Principle:** Granularity is the size of a service (function), not modularity (the breaking apart). Find equilibrium between disintegrators (forces favoring finer) and integrators (forces favoring coarser).

**Granularity Disintegrators (break apart):**
| Driver | Reason for applying driver |
|---|---|
| Service scope | Single-purpose services with tight cohesion |
| Code volatility | Agility (reduced testing scope and deployment risk) |
| Scalability | Lower costs and faster responsiveness |
| Fault tolerance | Better overall uptime |
| Security access | Better security access control to certain functions |
| Extensibility | Agility (ease of adding new functionality) |

**Granularity Integrators (put back together):**
| Driver | Reason for applying driver |
|---|---|
| Database transactions | Data integrity and consistency |
| Workflow | Fault tolerance, performance, and reliability |
| Shared code | Maintainability |
| Data relationships | Data integrity and correctness |

*Ref: Hardparts.md — "Finding the Right Balance" — Tables 7-2 and 7-3*

**Do:**
- Break a service apart when its cohesion is weak (Customer Profile + Preferences + Comments) — not when cohesion is strong (Notification via SMS/email/letter).
- Use volatility-based decomposition when change rates diverge wildly (Postal Letter changes weekly, SMS/email every six months).
- Keep services coarse-grained if they require an ACID transaction (e.g. customer registration = profile + credit card + password).
- Verify leftover pieces can form a strong, named cohesion: "Email Service + Other Notification Service" is a sign of over-splitting.
- Apply rule-of-thumb: if >30–40% of collective code is shared domain library → consider consolidation.
- Measure churn rate per source code area objectively via VCS metrics.

**Don't:**
- Default to "microservice = as small as possible" — "single responsibility" is subjective at the service level.
- Split tightly-bound synchronous functions that must scale and fault-tolerate identically (e.g. ticket assignment + routing).
- Create a service you can't name without "Other", "Non-Email", or "Leftover".

**Code (named-namespace separation inside one service):**
```
// Rather than split assignment + routing into two services,
// keep them together and separate via namespaces:
app.ticket.assign.*
app.ticket.route.*
app.ticket.shared.*
```
*Ref: Hardparts.md — "Sysops Squad Saga: Ticket Assignment Granularity"*

---

### Pulling Apart Operational Data

**Principle:** Data is harder than code and outlives any architecture. Decide disintegration vs integration by explicit forces.

**Data Disintegrators (break apart):**
- Change control (breaking schema changes impact many services)
- Connection management (50 services × 2 instances × 10 connections = 1,000 connections)
- Scalability (database throughput & capacity)
- Fault tolerance (single DB = single point of failure)
- Architectural quanta (shared DB forces one quantum)
- Database type optimization (polyglot persistence: relational, key-value, document, column family, graph, NewSQL, cloud-native, time-series)

**Data Integrators (keep together):**
- Data relationships (foreign keys, views, triggers, stored procedures)
- Database transactions (ACID)

*Ref: Hardparts.md — "Data Disintegrators" / "Data Integrators"*

**Do (5-step process for breaking apart a monolith DB):**
1. Analyze DB and create data domains.
2. Assign tables to data domains (move into schemas; drop cross-schema synonyms).
3. Separate DB connections to data domains — no service connects to multiple domains.
4. Move schemas to separate DB servers (backup-restore with downtime, or replication without downtime).
5. Switch over to independent DB servers.

**Do (database connection governance):**
- Start with even-distribution connection quotas; tune via fitness functions.
- Move to variable-distribution quotas once you know each service's peak need.
- Store quotas in external config so they can be tuned programmatically.

**Don't:**
- Allow a service to connect to multiple schemas/databases (it's a "no-go" in the Sysops Squad model).
- Tolerate cross-schema synonyms indefinitely — they hide coupling points and must be removed by step 3.
- Assume a single shared DB can scale to the N × M instances × pool size a microservices ecosystem demands.

**Code:**
```sql
-- Step 2: move table to its data-domain schema
ALTER SCHEMA payment TRANSFER sysops.billing;

-- synonym approach (to be removed in Step 3):
CREATE SYNONYM ticketing.sysops_user FOR profile.sysops_user;
```
*Ref: Hardparts.md — "Step 2: Assign Tables to Data Domains"*

```sql
-- Breaking-change isolation: contract shields caller from schema drift
ALTER TABLE Wishlist DROP COLUMN EXPIRATION_DT;
-- Service D still emits a contract field; downstream callers untouched.
```
*Ref: Hardparts.md — "Change control"*

Connection-quota tuning table (variable distribution):
| Service | Quota | Max used | Waits |
|---|---|---|---|
| A | 8 | 5 | No |
| B | 29 | 27 | No |
| C | 20 | 15 | No |
| D | 25 | 25 | No |
| E | 18 | 14 | No |

*Ref: Hardparts.md — "Connection management" — Table 6-3*

---

### Data Ownership Scenarios

**Principle:** The service that performs write operations to a table is the owner. Decide ownership before deciding on distributed transactions.

**Three scenarios:**
- **Single ownership** — only one service writes; simplest.
- **Common ownership** — most/all services write; create a dedicated owner (e.g. Audit Service) and have others send fire-and-forget to a persisted queue.
- **Joint ownership** — two services in the same domain write; resolve via Table Split, Data Domain, Delegate, or Service Consolidation.

*Ref: Hardparts.md — "Assigning Data Ownership"*

**Four techniques for joint ownership:**

| Technique | Use when | Trade-off |
|---|---|---|
| Table Split | Tables can be cleanly partitioned; volatility differs | Sync overhead, possible consistency issues |
| Data Domain | Tables are tightly coupled, must be accessed together | Schema changes touch many services |
| Delegate | One service logically owns; others go through it | High coupling, low performance for non-owner writes |
| Service Consolidation | ACID needed across the tables, no other way | Coarse-grained, less fault tolerance, harder scaling |

*Ref: Hardparts.md — "Table Split / Data Domain / Delegate / Service Consolidation Techniques" — Tables 9-1, 9-2, 9-3, 9-4*

**Do:**
- Resolve single-ownership scenarios first; they clear the playing field.
- For joint ownership, generally prefer Delegate with **primary domain priority** (owner = service doing most CRUD), then use a replicated cache to handle performance.
- For common ownership, use a dedicated owner + persistent async queue (guaranteed delivery, fire-and-forget).
- Validate assignments by walking through real business workflows and transactions.

**Don't:**
- Allow joint ownership of the same table without one of the four resolution techniques.
- Use the operational-characteristics delegate (Inventory owns Product) — domain management becomes a mess.
- Treat audit tables as common-owned via a shared DB — reintroduces all the issues broken apart by Chapter 6.

**Code:**
```sql
-- Table Split: pull inventory out of Product
CREATE TABLE Inventory (
    product_id VARCHAR(10),
    inv_cnt INT
);
INSERT INTO Inventory (product_id, inv_cnt)
AS SELECT product_id, inv_cnt FROM Product;
COMMIT;
ALTER TABLE Product DROP COLUMN inv_cnt;
```
*Ref: Hardparts.md — "Table Split Technique" — Example 9-1*

---

### Distributed Transactions (ACID vs BASE)

**Principle:** Distributed transactions are NOT ACID. They are BASE (Basic Availability, Soft state, Eventual consistency). Atomicity binds to the service, not the business request.

**Do:**
- Plan for BASE semantics — services commit independently; data converges over time.
- Use eventual consistency patterns explicitly: Background Synchronization, Orchestrated Request-Based, or Event-Based.
- Bound transactional scope to a single service whenever possible.

**Don't:**
- Try to span ACID across services. Distributed transactions "have legendary failure modes."
- Treat Saga compensation as a perfect undo — it's messy and full of edge cases.

*Ref: Hardparts.md — "Distributed Transactions"*

---

### Eventual Consistency Patterns

**Principle:** Pick the pattern that matches the consistency window and coupling tolerance.

| Pattern | Best for | Advantage | Disadvantage |
|---|---|---|---|
| Background Synchronization | Closed heterogeneous systems, batch windows | Decoupled services, good responsiveness | Couples all data sources; breaks bounded contexts; duplicates business logic; slow |
| Orchestrated Request-Based | In-request consistency with complex workflows | All sources updated in request | Tight coupling, synchronous, bottlenecks |
| Event-Based | Loosely coupled, scalable | Most decoupled, eventual | Eventual-only, requires broker & event design |

*Ref: Hardparts.md — "Eventual Consistency Patterns" — Table 9-5*

**Do:**
- Prefer dedicated orchestrator service over loading one onto a domain service.
- Use persisted queues for fire-and-forget audit/event emission.
- Send parallel compensating calls from the mediator on error.
- Treat background sync as a last resort — it breaks bounded contexts.

**Don't:**
- Use Background Synchronization inside a microservices architecture (it breaks bounded contexts).
- Assume API endpoint versioning solves shared-service versioning (REST, gRPC, and messaging all need separate strategy).

---

### Saga Patterns (Dynamic Coupling Matrix)

**Principle:** Eight named saga patterns span (Communication × Consistency × Coordination). Pick the one with the best overall balance — don't default to "familiar" Epic Saga.

| Pattern | Comm | Consistency | Coord | Coupling | Complexity | Resp/Avail | Scale |
|---|---|---|---|---|---|---|---|
| Epic Saga (sao) | Sync | Atomic | Orchestrated | Very high | Low | Low | Very low |
| Phone Tag Saga (sac) | Sync | Atomic | Choreographed | High | High | Low | Low |
| Fairy Tale Saga (seo) | Sync | Eventual | Orchestrated | High | Very low | Medium | High |
| Time Travel Saga (sec) | Sync | Eventual | Choreographed | Medium | Low | Medium | High |
| Fantasy Fiction Saga (aao) | Async | Atomic | Orchestrated | High | High | Low | Low |
| Horror Story (aac) | Async | Atomic | Choreographed | Medium | Very high | Low | Medium |
| Parallel Saga (aeo) | Async | Eventual | Orchestrated | Low | Low | High | High |
| Anthology Saga (aec) | Async | Eventual | Choreographed | Very low | High | High | Very high |

*Ref: Hardparts.md — "Transactional Saga Patterns" — Tables 12-2 through 12-9, "Build Your Own Trade-Off Analysis" — Table 15-2*

**Inverse correlation:** coupling level vs scale/elasticity. As coupling rises, scalability falls.

**Do:**
- Choose Fairy Tale Saga(seo) or Parallel Saga(aeo) when you can take eventual consistency — they give the best trade-offs for most workflows.
- Use Saga State Machines to track saga lifecycle (CREATED → ASSIGNED → ACCEPTED → COMPLETED, etc.) and decide compensating actions on failure.
- Move saga state to NO_SURVEY (eventual) rather than blocking the user on a downstream service outage.

**Don't:**
- Default to Epic Saga (sao) because it mimics monolithic ACID — orchestration plus transactionality creates bottlenecks and legendary failure modes.
- Use the Horror Story (aac) pattern — async + atomic + choreographed is the worst combination (very high complexity, low responsiveness).
- Combine Saga atomicity with asynchronicity and choreography simultaneously; that's how Horror Stories are born.
- Assume choreography simplifies error paths — every error condition adds new communication links.

**Code (state machine — saga states for ticket processing):**
```
START → CREATED → ASSIGNED → ACCEPTED → COMPLETED → CLOSED
                          ↘ REASSIGN → ASSIGNED
```
*Ref: Hardparts.md — "Saga State Machines" — Figure 12-21*

---

### Orchestration vs Choreography

**Principle:** As workflow complexity rises, the need for an orchestrator rises proportionally. Implementation coupling cannot reduce semantic coupling — only make it worse.

| Orchestration | Choreography |
|---|---|
| Workflow control | — |
| State query | State query |
| Error handling | — |
| (Responsiveness) | Responsiveness |
| (Fault tolerance) | Fault tolerance |
| (Service decoupling) | Service decoupling |
| (Recoverability) | — |
| (State management) | — |
| (Scalability) | Scalability |
| (Distributed workflow) | — |
| (Error handling) | — |
| (Recoverability) | — |

*Ref: Hardparts.md — "Trade-Offs Between Orchestration and Choreography" — Tables 11-1, 11-5, 11-8*

**Do:**
- Use orchestration for complex workflows with many error/boundary conditions.
- Use choreography for high-throughput, simple, infrequent-error workflows.
- Use Front Controller pattern when you need a pseudo-orchestrator inside choreography (state in first-called service).
- Use stateless choreography only when high performance outweighs state-query cost.
- Use stamp coupling in the contract to pass workflow state when choreography is required but workflow is non-trivial.
- Place exactly one orchestrator per workflow — not a global ESB-style orchestrator.

**Don't:**
- Always-choreograph "for decoupling" — error paths always add complexity you didn't anticipate.
- Always-orchestrate — leaves scale on the table for fire-and-forget workloads.
- Mix the two ad hoc — pick a primary style per workflow, document in ADR.

**Code (workflow state management for choreography):**
```
Front Controller:   first service owns workflow state — adds
                    communication overhead (good for state queries,
                    bad for performance).

Stateless:           query each service on demand — high performance,
                    high network chatter, complex ad-hoc reconstruction.

Stamp Coupling:     embed workflow state in the contract — no
                    single status query point, but no front controller
                    needed.
```
*Ref: Hardparts.md — "Workflow State Management" — Tables 11-2, 11-3, 11-4*

---

### Contracts — Strict vs Loose

**Principle:** Contracts are orthogonal to communication/consistency/coordination. Strict contracts give fidelity; loose contracts give evolvability. Use the spectrum deliberately, not by default.

**Strict contract spectrum examples:** RMI/PRC → gRPC → JSON-Schema → GraphQL → REST → JSON/YAML name-value pairs.

| Strict contract | Loose contract |
|---|---|
| Guaranteed contract fidelity | Highly decoupled |
| Versioned | Easier to evolve |
| Easier to verify at build time | Contract management (typos, missing keys) |
| Better documentation | Requires fitness functions |
| Tight coupling | — |
| Versioned (integration nightmare without deprecation) | — |

*Ref: Hardparts.md — "Strict Versus Loose Contracts" — Tables 13-1, 13-2*

**Do:**
- Use strict contracts for internal services with controlled consumers and tightly semantically-coupled data.
- Use loose (name-value JSON/YAML) contracts for external/mobile/external-storefront services where rate of change is constrained (e.g. app-store approval latency).
- Use consumer-driven contracts as architectural fitness functions to keep loose contracts verifiable.
- Use loose contracts where the team has high engineering maturity; otherwise prefer strict.

**Don't:**
- Auto-include every Profile field in Wishlist's contract "just in case" — that's stamp coupling, an anti-pattern.
- Assume JSON is automatically "loose" — JSON-Schema with required fields is strict.
- Forget to budget for contract deprecation strategy (custom per shared library, never `LATEST`).

**Code:**
```json
// Strict JSON contract (with schema validation)
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "properties": {
    "acct":   {"type": "number"},
    "cusip":  {"type": "string"},
    "shares": {"type": "number", "minimum": 100}
  },
  "required": ["acct", "cusip", "shares"]
}
```
*Ref: Hardparts.md — "Strict Versus Loose Contracts" — Example 13-1*

```json
// Loose contract (name-value pairs)
{ "name": "Mark", "status": "active", "joined": "2003" }
```
*Ref: Hardparts.md — "Strict Versus Loose Contracts" — Example 13-4*

```graphql
# Two views of Profile — keep only the slice you need
type Profile { name: String }                 # Wishlist's view
type Profile { name: String; addr1: String; addr2: String; country: String; ... }  # Customer's view
```
*Ref: Hardparts.md — "Strict Versus Loose Contracts" — Examples 13-2, 13-3*

---

### Stamp Coupling

**Principle:** Stamp coupling is passing a large structure when each consumer needs only a slice. Sometimes anti-pattern, sometimes legitimate workflow-state vehicle.

**Do:**
- Use stamp coupling to carry workflow status through a choreographed chain when you need both throughput and shared workflow state.
- Calculate bandwidth cost: 2,000 req/s × 500 KB = 1,000,000 KB/s vs 2,000 × 200 B = 400 KB/s.

**Don't:**
- Over-specify contracts with fields "just in case" — causes breaking changes in fields consumers don't care about.
- Conflate "industry standard document format" (legitimate, e.g. travel XML) with "I might want this field" (anti-pattern).

*Ref: Hardparts.md — "Stamp Coupling" — Table 13-4*

---

### Code Reuse Patterns

**Principle:** Reuse is derived via abstraction but operationalized by **slow rate of change**. Pick the pattern that matches the shared code's rate of change.

| Pattern | Use when | Avoid when |
|---|---|---|
| Code Replication | Static one-offs (annotations, attributes, util base classes); low change frequency | Code that changes often — propagation cost is brutal |
| Shared Library | Homogeneous stacks; low-to-moderate change; need compile-time versioning | Many heterogeneous languages; many libraries (dependency matrix explosion) |
| Shared Service | High volatility; polyglot; shared state required | Latency-sensitive paths; when shared service becomes single point of failure |
| Sidecar + Service Mesh | Cross-cutting *operational* concerns (logging, monitoring, auth, circuit breakers) | Domain code — sidecars are for orthogonal coupling, not domain coupling |

*Ref: Hardparts.md — "Code Replication / Shared Library / Shared Service / Sidecars and Service Mesh" — Tables 8-1, 8-2, 8-3, 8-4*

**Do:**
- Use shared libraries for stable technical utilities (formatters, validators, security primitives).
- Version every shared library. Use a custom deprecation strategy per library based on its rate of change.
- Use a sidecar/service mesh for cross-cutting operational concerns (logging, monitoring, auth, service discovery, circuit breakers).
- Place shared operational libraries in the sidecar when more than ~50% of teams need them.
- Use shared services only for high-volatility code or shared state needs.
- Centralize sidecar ownership in a platform/infra team that releases via fitness-function-gated CI.

**Don't:**
- Use `LATEST` as the library version pin.
- Use a single coarse-grained "SharedStuff.jar" — every change ripples across all consumers.
- Put domain classes (Address, Customer) into the sidecar — that's inappropriate coupling.
- Create a shared service when every consumer call is latency-critical (the shared service becomes a network bottleneck and fault-tolerance SPOF).
- Replicate code that has bugs or is expected to change often.

**Code (versioned shared library):**
```
app/1.0/discountcalc?orderid=123
app/1.1/discountcalc?orderid=123
app/1.2/discountcalc?orderid=123
app/1.3/discountcalc?orderid=123
latest change -> app/1.4/discountcalc?orderid=123
```
*Ref: Hardparts.md — "Change Risk" — Example 8-3*

**Reuse principle:**
> Reuse is derived via abstraction but operationalized by slow rate of change.

*Ref: Hardparts.md — "Code Reuse: When Does It Add Value?"*

**Orthogonal coupling:**
> Two parts of an architecture may be orthogonally coupled: two distinct purposes that must still intersect to form a complete solution (e.g. monitoring vs. catalog checkout).

*Ref: Hardparts.md — "Orthogonal Coupling"*

---

### Distributed Data Access

**Principle:** A service that doesn't own data must access it through the owning service — never reach across the boundary.

| Pattern | Use when | Trade-off |
|---|---|---|
| Interservice Communication | Real-time, small payload, low-latency | Synchronous coupling |
| Column Schema Replication | One column subset is read very frequently | Replication lag, governance |
| Replicated Caching | Repeated reads, can tolerate staleness | Cache coherence |
| Data Domain | Aggregating across many services is required | Coupling, governance |

*Ref: Hardparts.md — "Distributed Data Access" — Patterns overview*

**Do:**
- Treat the contract as a schema firewall — schema changes inside the owning DB must not leak to consumers.
- Prefer column replication / cached subset over direct interservice reads for high-volume reference data.
- Use the data domain pattern for analytics-style aggregations.

**Don't:**
- Let Service C read Database D directly when D is in another bounded context.
- Couple the API contract to the underlying database schema (one is an integration contract, the other is implementation detail).

---

### Analytical Data — Data Mesh

**Principle:** Analytical data is not operational data; it has its own architecture. Apply the same quantum/sidecar discipline used for operational data.

**Evolution:** Data Warehouse (centralized, schema-on-write, brittle ETL) → Data Lake (centralized, schema-on-read, "data swamp") → **Data Mesh** (domain-oriented, data-as-product, self-serve platform, federated governance).

| Approach | Advantage | Disadvantage |
|---|---|---|
| Data Warehouse | Centralized consolidation; dedicated analytics silo | Extreme partitioning of domain knowledge; integration brittleness; complexity; limited functionality for intended purpose |
| Data Lake | Less structured; less up-front transformation; better suited to distributed architectures | Difficulty understanding relationships; ad hoc transformations required |
| Data Mesh | Highly suitable for microservices; follows modern principles; decouples analytical from operational data | Requires contract coordination with DPQ; requires async + eventual consistency |

*Ref: Hardparts.md — "Previous Approaches" — Tables 14-1, 14-2, 14-3*

**Data Mesh four principles:**
1. **Domain ownership of data** — domains that originate or consume the data own it.
2. **Data as a product** — domains serve data products with their own fitness functions.
3. **Self-serve data platform** — discoverability, declarative creation, lineage.
4. **Computational federated governance** — automated policies as code in every DPQ sidecar.

*Ref: Hardparts.md — "Definition of Data Mesh"*

**Data Product Quantum (DPQ):**
- **Source-aligned DPQ** — provides analytical data for its service (cooperative quantum).
- **Aggregate DPQ** — combines data from multiple DPQs (sync or async).
- **Fit-for-purpose DPQ** — purpose-built for a specific need (ML, BI, reporting).

**Do:**
- Always implement the DPQ ↔ service coupling as one of the eventual-consistency + asynchronicity patterns (Parallel Saga aeo or Anthology Saga aec).
- Use a cooperative quantum pattern: DPQ is operationally independent but tightly contract-coupled to its service.
- Build consumer-driven contract fitness functions between DPQs (Ticket DPQ ↔ Expert Supply DPQ).
- Use a complete-snapshot or none rule for trend analysis: missing day > incomplete day.

**Don't:**
- Try to keep analytical and operational data transactionally consistent — it's a "daunting challenge in distributed architectures".
- Put analytical data behind a synchronous transactional boundary with the service — defeats orthogonal decoupling.

**Code (ADR pattern for data mesh):**
```
*ADR: Ensure that Expert Supply DPQ Sources Supply an Entire Day's Data or None*

*Context*
The Expert Supply DPQ performs trend analysis over specified time
periods. Incomplete data for a particular day will skew trend
results and should be avoided.

*Decision*
We will ensure that each data source receives complete snapshots
for daily trends or no data for that day, allowing data scientists
to exempt that day.

*Consequences*
If too many days become exempt because of availability or other
problems, accuracy of trends will be negatively impacted.

*Fitness functions*:
- Complete daily snapshot. Check timestamps on messages as they
  arrive. Any gap of more than one minute indicates a gap in
  processing, marking that day as exempt.
- Consumer-driven contract fitness function for Ticket DPQ and
  Expert Supply DPQ.
```
*Ref: Hardparts.md — "Sysops Squad Saga: Data Mesh"*

---

### Trade-Off Analysis Process

**Principle:** Three-step process for modern trade-off analysis.

1. **Find entangled dimensions** — what's braided together (communication, consistency, coordination + your domain's unique forces).
2. **Analyze coupling points** — model combinations; rate by coupling, complexity, responsiveness/availability, scale/elasticity.
3. **Assess trade-offs** — iteratively fix dimensions and propagate downstream.

*Ref: Hardparts.md — "Build Your Own Trade-Off Analysis"*

**Do:**
- Use MECE lists (mutually exclusive, collectively exhaustive) so comparisons are valid.
- Use qualitative (not quantitative) analysis — no two architectures are identical enough for numbers.
- Build a matrix of named patterns × rated dimensions (see Tables 12-2 through 12-9) and look for inverse correlations.
- Iterate the analysis; don't expect the first draft to be correct.

**Don't:**
- Trust evangelists (including the authors of this book).
- Treat a pattern's existence as evidence of its solvability — "patterns recognize commonality, not solvability."
- Use snake-oil absolutes ("reuse is abuse", "always choreograph", "share nothing").

---

## Anti-Patterns & Common Mistakes

- **Distributed monolith:** Many separately deployed services that must deploy as a set in a specific order → fix: consolidate or reduce coupling. *Ref: Hardparts.md — "Deployability"* (Matt Stine: "If your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain.")

- **SharedStu.jar / coarse-grained shared library:** All shared code in one blob; every change ripples → fix: split into functionally-partitioned, versioned libraries. *Ref: Hardparts.md — "Dependency Management and Change Control"*

- **Horror Story Saga:** Asynchronous + atomic + choreographed = worst combination → fix: switch to Anthology Saga (aec) and drop atomic requirement. *Ref: Hardparts.md — "Horror Story(aac) Pattern"*

- **Epic Saga by default:** Mimics monolithic ACID, creates bottlenecks, legendary failure modes → fix: prefer Fairy Tale (seo) or Parallel (aeo) when eventual consistency is acceptable. *Ref: Hardparts.md — "Epic Saga(sao) Pattern"*

- **Synonyms across data domains:** Synonyms hide coupling, but must be removed in Step 3 → fix: remove them, push integration to the service layer. *Ref: Hardparts.md — "Step 2: Assign Tables to Data Domains"*

- **Big Ball of Mud:** Component cycles across packages → fix: ArchUnit/JDepend fitness function. *Ref: Hardparts.md — "Using Fitness Functions"*

- **Stamp coupling "just in case":** Including fields Wishlist doesn't need → fix: name-value pairs at the slice each consumer needs. *Ref: Hardparts.md — "Over-Coupling via Stamp Coupling"*

- **Centralized customer service across domains:** Consolidation of all institutional customer info in one place → fix: domain-partition customer, duplicate per bounded context. *Ref: Hardparts.md — "Code Reuse: When Does It Add Value?"*

- **Joint ownership without a resolution technique:** Two services writing the same table → fix: Table Split, Data Domain, Delegate, or Service Consolidation. *Ref: Hardparts.md — "Data Ownership Scenarios"*

- **Service with no name:** After splitting, you can't name the leftover → fix: don't split that way. *Ref: Hardparts.md — "Fault Tolerance"*

- **Cross-schema multi-DB connection:** Service connects to multiple databases/schemas → fix: bounded context per service, no cross-schema access; remove synonyms in Step 3. *Ref: Hardparts.md — "Step 3: Separate Database Connections to Data Domains"*

- **`LATEST` shared library version:** Hot-deploys fail when LATEST drifts → fix: pin explicit versions, custom deprecation strategy per library. *Ref: Hardparts.md — "Versioning Strategies"*

- **Background synchronization in microservices:** Couples all data sources, breaks bounded contexts, duplicates business logic → fix: use Event-Based or Orchestrated Request-Based. *Ref: Hardparts.md — "Background Synchronization Pattern"*

- **API endpoint versioning as a workaround for shared-service versioning:** Doesn't compose with gRPC/messaging; subjective version triggers → fix: prefer compile-time versioned shared libraries, or accept the runtime risk. *Ref: Hardparts.md — "Change Risk"*

---

## Decision Heuristics / Checklists

**Choosing service granularity:**
- Single-purpose & strong cohesion → keep together
- Weak cohesion (e.g. profile + preferences + comments) → disintegrate
- Volatility differs wildly → disintegrate (volatility-based decomposition)
- Scalability differs wildly → disintegrate
- One function's fault crashes the others → disintegrate
- Some parts need higher security → disintegrate
- Extensibility is planned and ongoing → disintegrate
- Need ACID across functions → keep together
- Workflow chatter is >70% of calls → keep together
- Shared domain code >40% of total → keep together
- Leftover can't be cleanly named → reconsider the split

**Choosing contract strictness:**
- Internal + controlled consumers + low change → strict
- External + app-store / partner-driven cadence → loose
- Both → consumer-driven contracts as fitness functions

**Choosing saga pattern:**
- Need atomic + know all-or-nothing semantics → Epic Saga (sao)
- Need high scale + simple workflow + can accept eventual → Anthology (aec) or Parallel (aeo)
- Complex workflow + many error conditions → orchestrated + eventual (Fairy Tale seo)
- Don't: async + atomic + choreographed (Horror Story aac)

**Choosing code reuse:**
- Static + rarely changes → replicate
- Stable, versioned, compile-time → shared library
- High volatility + shared state + polyglot → shared service
- Cross-cutting operational concern → sidecar / service mesh

**Choosing data access pattern:**
- Real-time + small payload → interservice communication
- Read-heavy reference data → column schema replication or replicated cache
- Cross-domain analytics → data domain

**Choosing analytical data architecture:**
- Single source, structured, batch OK → data warehouse (or query lake)
- Many sources, semi-structured, ML use → data lake
- Domain-partitioned microservices → data mesh (DPQs + federated governance)

**Building a fitness function:**
- Atomic → check a single architecture characteristic (e.g. cycle detection)
- Holistic → check combination (e.g. scalability × performance)
- Continuous → run on every commit/deploy
- Manual → only for things that can't be automated (legal review)

**When to write an ADR:**
- Every significant architecture decision
- Format: Context → Decision → Consequences
- Include trade-offs considered

**MECE comparison rules:**
- Compare same-shaped things (don't compare a queue to an ESB).
- Mutually exclusive alternatives.
- Collectively exhaustive of the option space.

---

## Key Takeaways

1. There are no best practices in architecture — only trade-offs. Strive for the "least worst" combination.
2. Quanta define the unit of deployment. Find them before you pick a style.
3. Data outlives code. Decomposing data is harder than decomposing code; govern connection quotas, schemas, and ownership explicitly.
4. Fitness functions = objective governance. Atomic (one characteristic) or holistic (combination), continuous by default, manual only when unavoidable.
5. ADRs (Context, Decision, Consequences) are the canonical decision documentation.
6. Granularity = equilibrium of disintegrators and integrators. Don't disintegrate without weighing the integrators.
7. ACID binds to a service, not a business request. Plan for BASE.
8. Eight named saga patterns; don't default to Epic Saga. Async + atomic + choreographed = Horror Story.
9. Orchestrate complex workflows; choreograph simple/fire-and-forget. Implementation coupling cannot reduce semantic coupling.
10. Reuse = abstraction × slow rate of change. Co-locate a sidecar for operational coupling only.
11. Operational data ≠ analytical data. Apply quantum/sidecar discipline to both — use Data Mesh for modern microservice analytical architectures.
12. Every organization's problems are unique. Copy the questions, not the answers.

---

## Cross-References
- Related: [[../Software_Architecture_Patterns.md]] — pattern catalog & selection criteria
- Related: [[../Designing_Distributed_Systems.md]] — runtime component patterns (sidecar, ambassador, adapter, work queue, scatter-gather)
- Topic index: [[../INDEX.md]]