# Software Architecture Patterns, 2nd Edition
**Author:** Mark Richards
**Topic tags:** `#architecture`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Software Architecture Patterns 2nd edition/Software Architecture Patterns 2nd edition.md` · `summaries/Software_Architecture_Patterns_2nd_edition.md`

## TL;DR
Five named architecture styles (Layered, Microkernel, Event-Driven, Microservices, Space-Based) classified by monolithic-vs-distributed and technical-vs-domain partitioning. Choose by operational characteristics, team structure, data decomposability, and budget — never by trend. Hybrid styles are the norm.

---

## Best Practices by Topic

### Terminology: Styles vs Patterns vs Design Patterns

**Principle:** Styles = macro structure. Patterns = reusable structural building blocks within a style. Design patterns = class/module-level source-code patterns.

**Do:**
- Reserve "architecture style" for macro structure (Layered, Microservices, …).
- Reserve "architecture pattern" for reusable structural blocks (CQRS, Saga, …).
- Reserve "design pattern" for class-level (Builder, Observer, Strategy, …).
- Compose them in a hierarchy: design patterns → architecture patterns → architecture styles.
- Combine styles into hybrids (event-driven microservices, space-based microservices, event-driven microkernel) only after understanding each one independently.

*Ref: Patterns 2e — "Introduction"*

---

### Monolithic vs Distributed

**Principle:** Monolithic = single deployment unit. Distributed = multiple deployment units. Distributed gives operational superpowers but inherits the fallacies of distributed computing.

**Monolithic trade-offs:**
- Simpler, cheaper, faster to build
- All functionality fails together on fatal error
- MTTR/MTTS measured in minutes
- Scaling scales the entire app, even when only one part needs it

**Distributed trade-offs:**
- Operational superpowers: per-service scalability, MTTS/MTTR in seconds or milliseconds, high fault tolerance, agility
- Fallacies of distributed computing bite: network is reliable (false), bandwidth is infinite (false), latency is zero (false), topology doesn't change (false), one administrator (false), cost is zero (false), transport is homogeneous (false), network is secure (false)
- Distributed transactions, eventual consistency, workflow, error handling, data sync, contract management all add complexity and cost

**When to choose distributed:**
- Different parts need different architecture characteristics (e.g. customer-facing needs scale/availability; back-office does not)
- Complex systems performing multiple business functions
- High scalability, fault tolerance, or elasticity required

**When to choose monolithic:**
- Simple systems or websites
- Tight budget / time constraints
- One uniform set of architecture characteristics across the whole app

*Ref: Patterns 2e — "Architecture Classification"*

---

### Technical vs Domain Partitioning

**Principle:** Partitioning must align with team structure (Conway's Law) and the dominant change pattern.

**Technical Partitioning:**
- Components grouped by layer (presentation, business, persistence, database)
- Namespace pattern: `app.presentation.customer`, `app.business.customer`, `app.persistence.customer`
- Good when teams are UI / backend / DBA silos and changes are layer-scoped (UI overhauls, DB migrations)

**Domain Partitioning:**
- Components grouped by domain area
- Namespace pattern: `app.customer`, `app.shipping`, `app.payment`
- Sub-layers allowed (`app.customer.presentation`), but top-level is the domain
- Good for cross-functional domain teams and DDD-aligned work

**Decision rule:**
- Teams by technical specialty + layer-scoped changes → technical partitioning
- Teams by domain (UI + backend + DBA per domain) + domain-scoped changes → domain partitioning
- DDD-driven development → domain partitioning

**Style × Partitioning matrix:**

| Style | Partitioning |
|---|---|
| Layered | Technical |
| Microkernel | Technical or Domain (only style that can be either) |
| Event-Driven | Technical |
| Microservices | Domain |
| Space-Based | Technical |

*Ref: Patterns 2e — "Architecture Partitioning" / "Style Analysis Summary"*

---

### Layered Architecture

**Principle:** The de-facto standard. Best when budget/time is tight, changes are layer-scoped, and teams are technically organized.

**Topology:** Presentation → Business → Persistence → Database. Optionally combine business+persistence (3 layers) or split into more (5+ layers).

**Layers of Isolation:** Closed layer = request must pass through it. Open layer = request can bypass it.
- Default: keep layers closed to preserve isolation.
- Open a shared-services layer below business so business can bypass it to reach persistence.

**Architecture sinkhole anti-pattern:** Requests pass through layers with no logic at each layer.
- Apply 80/20 rule: ~20% pass-through is healthy. If 80%+ is pass-through, open some layers (and accept the loss of layer isolation).

**Code (namespace example showing technical partitioning):**
```
app.presentation.customer  // presentation layer, customer domain
app.business.customer      // business layer, customer domain
app.persistence.customer   // persistence layer, customer domain
// The "customer" node is duplicated across layers — that's the giveaway
// for technical partitioning.
```
*Ref: Patterns 2e — "Description" / "Key Concepts"*

**Architecture characteristics:**

| Characteristic | Star rating |
|---|---|
| Partitioning type | Technical |
| Overall cost | $ |
| Agility | ★☆☆☆☆ (1/5) |
| Simplicity | ★★★★★ (5/5) |
| Scalability | ★☆☆☆☆ (1/5) |
| Fault tolerance | ★☆☆☆☆ (1/5) |
| Performance | ★★★☆☆ (3/5) |
| Extensibility | ★☆☆☆☆ (1/5) |

*Ref: Patterns 2e — "Architecture Characteristics"*

**Do:**
- Use when budget/time is tight and the team is technically organized.
- Use when most changes are isolated to a single layer (UI refresh, business-rule change, DB swap).
- Document which layers are open vs closed and why.

**Don't:**
- Use when high scalability, fault tolerance, or elasticity are required.
- Use when most changes are domain-scoped (e.g. adding an expiry date to wishlist items touches every layer).
- Use when teams are cross-functional by domain.

---

### Microkernel Architecture

**Principle:** A stable core system with plug-in modules. The only style that can be technically or domain partitioned.

**Topology:** Core system + plug-in modules + (optionally) plug-in registry.

**Plug-in connection modes:**
1. **Point-to-point** (JAR/DLL/OSGi/Jigsaw/Prism) → monolithic deployment
2. **Consolidated codebase** (namespace like `app.plugin.assessment.iphone12`) → monolithic, but separate concerns
3. **Remote services** (REST/messaging) → distributed microkernel, easier runtime deployment, better scalability

**Use cases:** Product-based apps with planned extensions, multiple configurations (cloud-vendor adapters), jurisdiction-specific rules (insurance claims), IDE/browser-style extensibility.

**Architecture characteristics:**

| Characteristic | Star rating |
|---|---|
| Partitioning type | Technical or Domain |
| Overall cost | $ |
| Agility | ★★★☆☆ (3/5) |
| Simplicity | ★★★★☆ (4/5) |
| Scalability | ★☆☆☆☆ (1/5) |
| Fault tolerance | ★☆☆☆☆ (1/5) |
| Performance | ★★★☆☆ (3/5) |
| Extensibility | ★★★☆☆ (3/5) |

*Ref: Patterns 2e — "Architecture Characteristics"*

**Do:**
- Put volatile code in plug-ins, keep core stable.
- Use plug-ins as cloud-vendor adapters when targeting multiple clouds.
- Use a registry to track plug-in metadata (name, contract, protocol).

**Don't:**
- Choose for high scalability or fault tolerance — core is the bottleneck and SPOF.
- Choose if most of your changes are in the core itself.

---

### Event-Driven Architecture

**Principle:** Asynchronous, highly decoupled event processors. Topology: event processor + initiating event + processing event + event channel.

**Components:**
- **Event processor (service):** main deployment unit; triggers and responds to events
- **Initiating event:** comes from outside the system; noun-verb naming ("Place Order")
- **Processing event (derived):** state-change advertisement; verb-noun ("Order Placed")
- **Event channel:** queue (point-to-point, initiating) or topic (publish-subscribe, processing)

**Channel ownership rule:**
- Events: sender owns the channel AND the contract
- Messages: receiver owns the channel AND the contract

**Always advertise state changes** even if no current consumer — provides architectural extensibility.

**Event-Driven vs Message-Driven:**

| Property | Event | Message |
|---|---|---|
| Context | Announces state change ("I placed an order") | Command to specific service ("apply payment") |
| Sender knowledge | Doesn't know receivers | Knows receiver |
| Channel owner | Sender | Receiver |
| Channel type | Topic / pub-sub (typically) | Queue / point-to-point (typically) |

*Ref: Patterns 2e — "Event-Driven Versus Message-Driven"*

**Architecture characteristics:**

| Characteristic | Star rating |
|---|---|
| Partitioning type | Technical |
| Overall cost | $$$$ |
| Agility | ★★★★☆ (4/5) |
| Simplicity | ★☆☆☆☆ (1/5) |
| Scalability | ★★★★★ (5/5) |
| Fault tolerance | ★★★★★ (5/5) |
| Performance | ★★★★★ (5/5) |
| Extensibility | ★★★★★ (5/5) |

*Ref: Patterns 2e — "Architecture Characteristics"*

**Do:**
- Choose when the business talks in events, triggers, and reactions ("react to something the user did").
- Use for complex nondeterministic workflows (CEP-class).
- Always have services advertise state changes, even when nobody listens.
- Treat "Order Placed" (verb-noun) and "Place Order" (noun-verb) consistently.

**Don't:**
- Choose for request-based / CRUD-dominant processing.
- Choose for synchronous user-waits-for-result processing.
- Choose when high data consistency is required (everything is eventually consistent).
- Choose when you need to coordinate strict event ordering (e.g. "A and B complete before C, D before E") — orchestration handles that better.
- Choose without budgeting for error handling complexity (e.g. customer charged + notified but inventory empty → who reverses payment? who sends another notification?).

---

### Microservices Architecture

**Principle:** Ecosystem of single-purpose, separately deployed services accessed through an API gateway. The most powerful and the most expensive style.

**Topology:** API gateway (no business logic, no orchestration, no mediation) → services → each owns its own data.

**Microservice definition:** Single-purpose, separately deployed unit of software that does one thing really well. "Micro" refers to functional scope, NOT physical size.
- Example: a service with 312 class files that all handle different customer emails is still a microservice because it does one thing.

**Bounded Context (Eric Evans, DDD):** All source code for a domain/subdomain + corresponding data structures + data encapsulated as one unit. Microservices cannot exist without it.

**Three unique features that distinguish microservices from ALL other styles:**
1. **Distributed data** — only style that *requires* data to be broken up
2. **Operational automation** — containerization (Docker), orchestration (Kubernetes), CI/CD, DevOps are required, not optional
3. **Organizational change** — only style that *requires* cross-functional domain teams

**Practical exception:** Some data sharing between 2-6 services is normal — driven by table coupling, FK constraints, triggers, materialized views, performance needs, shared ownership. When shared, the bounded context extends to include all shared tables and the services accessing them.

**Three latencies that hurt performance:**
- **Network latency:** 30-300+ ms depending on protocol and distance
- **Security latency:** few ms to 300+ ms for authn/authz
- **Data latency:** time for another service to query data on your behalf (replaces a JOIN with a remote call + DB call)

**Architecture characteristics:**

| Characteristic | Star rating |
|---|---|
| Partitioning type | Domain |
| Overall cost | $$$$$ |
| Agility | ★★★★★ (5/5) |
| Simplicity | ★☆☆☆☆ (1/5) |
| Scalability | ★★★★★ (5/5) |
| Fault tolerance | ★★★★★ (5/5) |
| Performance | ★★☆☆☆ (2/5) |
| Extensibility | ★★★★★ (5/5) |

*Ref: Patterns 2e — "Architecture Characteristics"*

**Do:**
- Verify feasibility to break functionality into dozens to hundreds of independent pieces.
- Use when high agility, fault tolerance, scalability, and extensibility are needed.
- Align with cross-functional domain teams + service owners (architects) per domain.
- Use containerization + Kubernetes + automated CI/CD from day one.
- Treat new services as "drop-in functionality" — wrap in container, expose API endpoint, deploy.
- Treat BI / analytics reports as microservices accessing a data lake / warehouse (stable schema, low breaking-change risk).

**Don't:**
- Use for complex workflows that require tight orchestration between separately deployed services.
- Use if your data can't be broken into dozens to hundreds of separate schemas/databases (FK constraints, triggers, views, stored procedures all block this).
- Use on tight budget/time constraints — most complex and expensive style.
- Use for high-performance / highly responsive systems — inter-service latency is the killer.
- Repeat the SOA mistake of putting business logic / orchestration / mediation in the API gateway.
- Use if your teams aren't cross-functional and organized by domain.

---

### Space-Based Architecture

**Principle:** Removes the database from the transactional processing path by using replicated in-memory data grids. Built for extreme elasticity and concurrency.

**Topology:** Processing units (application logic + in-memory data grid + optional web components) + virtualized middleware.

**Virtualized middleware components:**
- **Messaging grid** — request/session management; forwards to available processing units (round-robin or next-available); typically a web server
- **Data grid** — replicates in-memory data across processing units; uses Hazelcast / Apache Ignite / Oracle Coherence; includes data pumps (async to DB), data writers (apply DB updates), data readers (cold-start from DB)
- **Processing grid (optional)** — orchestration or choreography between processing units
- **Deployment manager** — dynamic start/stop of processing units based on load (typically Kubernetes)

**Use cases:** Concert ticketing, online auctions, high-volume social media — anywhere concurrency spikes from dozens to tens of thousands in seconds.

**Architecture characteristics:**

| Characteristic | Star rating |
|---|---|
| Partitioning type | Technical |
| Overall cost | $$$$$ |
| Agility | ★★☆☆☆ (2/5) |
| Simplicity | ★☆☆☆☆ (1/5) |
| Scalability | ★★★★★ (5/5) |
| Fault tolerance | ★★★★☆ (4/5) |
| Performance | ★★★★★ (5/5) |
| Extensibility | ★★★☆☆ (3/5) |

*Ref: Patterns 2e — "Architecture Characteristics"*

**Do:**
- Use for extreme concurrent scalability or elasticity (tens of thousands+ concurrent).
- Use when in-memory nanosecond data access is required.
- Consider hybrid split: cloud processing units, on-prem DB with data writers/readers.
- Start at least one processing unit populated before adding more — they replicate from each other, not from the DB.

**Don't:**
- Use when transactional data is too large to fit in memory (e.g. 45 TB RDBMS).
- Use on tight budget/time constraints — high complexity and load testing is expensive.
- Use when high data consistency is required — always eventually consistent; updates may take time to reach the DB.

---

### Style Comparison Summary (Star Ratings)

| | Layered | Microkernel | Event-Driven | Microservices | Space-Based |
|---|---|---|---|---|---|
| Partitioning | T | D/T | T | D | T |
| Overall cost | $ | $ | $$$$ | $$$$$ | $$$$$ |
| Agility | ● | ●●● | ●●●● | ●●●●● | ●● |
| Simplicity | ●●●●● | ●●●● | ● | ● | ● |
| Scalability | ● | ● | ●●●●● | ●●●●● | ●●●●● |
| Fault tolerance | ● | ● | ●●●●● | ●●●●● | ●●●● |
| Performance | ●●● | ●●● | ●●●●● | ●● | ●●●●● |
| Extensibility | ● | ●●● | ●●●●● | ●●●●● | ●●● |

*Ref: Patterns 2e — "Style Analysis Summary" — Figure A-1*

**Decision heuristic from this matrix:**
- Scalability priority → event-driven, microservices, or space-based
- Simplicity/cost priority → layered or microkernel
- Layered chosen → deployment, performance, scalability are the risk areas
- Microkernel chosen → scalability, fault tolerance are the risk areas

---

### Hybrid Architecture Styles

**Principle:** Combine styles when individual styles don't solve the whole problem — but only after understanding each style's trade-offs.

**Common hybrids:**
- **Event-driven microservices** — events flowing between microservices
- **Space-based microservices** — processing units implemented as microservices
- **Event-driven microkernel** — events between core system and remote plug-ins

*Ref: Patterns 2e — "Introduction"*

---

## Anti-Patterns & Common Mistakes

- **Big Ball of Mud:** No architecture style → tightly coupled, brittle. *Fix:* Pick a style deliberately. *Ref: Patterns 2e — "Introduction"*

- **Architecture Sinkhole (Layered):** Pass-through requests dominate (>80%). *Fix:* Open some layers OR switch style. *Ref: Patterns 2e — "Considerations and Analysis"*

- **API Gateway as ESB:** Putting business logic, orchestration, or mediation in the API gateway. *Fix:* API gateway must have NO business logic to preserve bounded context. *Ref: Patterns 2e — "Basic Topology"*

- **Microservices without bounded context:** Hundreds of services sharing one monolithic DB → structural changes become infeasible. *Fix:* Enforce data ownership per service. *Ref: Patterns 2e — "Bounded Context"*

- **Microservices for high-performance systems:** Inter-service latency (network + security + data) destroys responsiveness. *Fix:* Use space-based or hybrid. *Ref: Patterns 2e — "When Not to Consider This Style"*

- **Microservices without DevOps:** Hand-offs to test/release teams don't scale to hundreds of services. *Fix:* Cross-functional teams own their services end-to-end; container orchestration + CI/CD are required. *Ref: Patterns 2e — "Unique Features"*

- **Microkernel for high-scale systems:** Core becomes the bottleneck and SPOF. *Fix:* Use a distributed style. *Ref: Patterns 2e — "When Not to Consider This Style"*

- **Event-driven for sync / CRUD-dominant processing:** Asynchronous processing fights the use case. *Fix:* Use layered or service-based. *Ref: Patterns 2e — "When Not to Consider This Style"*

- **Event-driven without error-handling strategy:** Partial workflow completions create unrecoverable states (e.g. charged + notified but out of stock). *Fix:* Design saga / compensating transactions explicitly. *Ref: Patterns 2e — "When Not to Consider This Style"*

- **Space-based with too-large transactional data:** Cannot fit 45 TB in memory. *Fix:* Use a different style for large-data systems. *Ref: Patterns 2e — "When Not to Consider This Style"*

- **Mixing partitioning and team structure:** Technical partitioning with domain teams (or vice versa). *Fix:* Conway's Law — align partitioning with team structure. *Ref: Patterns 2e — "Architecture Partitioning"*

- **Style driven by trend instead of fit:** Microservices because "everyone uses it" without data decomposability. *Fix:* Run the honest assessment; consider service-based as a middle ground. *Ref: Patterns 2e — "Considerations and Analysis"*

- **Layered architecture applied to domain-heavy change profile:** Adding wishlist expiration ripples through every layer and team. *Fix:* Switch to domain-partitioned style. *Ref: Patterns 2e — "When Not to Consider This Style"*

---

## Decision Heuristics / Checklists

**Choosing monolithic vs distributed:**
- Different parts need different architecture characteristics → distributed
- One uniform characteristic set + tight budget → monolithic
- Simple system or website → monolithic
- Complex multi-function system → distributed
- Need for speed, scale, or fault tolerance → distributed

**Choosing technical vs domain partitioning:**
- Teams by UI/backend/DBA specialty → technical partitioning
- Cross-functional domain teams → domain partitioning
- DDD-driven development → domain partitioning
- Changes mostly layer-scoped → technical partitioning
- Changes mostly domain-scoped → domain partitioning

**Choosing between the five styles:**

| If you need… | Choose |
|---|---|
| Budget-tight, layer-scoped changes, technically organized teams | Layered |
| Product-based app, planned extensions, multiple configurations | Microkernel |
| Reactive business, high performance/scale/fault tolerance, complex nondeterministic workflows | Event-Driven |
| High agility/scale/fault tolerance/extensibility, decomposable data, cross-functional domain teams, operational automation | Microservices |
| Extreme concurrent scalability/elasticity (tens of thousands+), data fits in memory | Space-Based |

**Style-by-style when-to-use summary:**
- **Layered:** Budget/time constraints; layer-scoped changes; technically organized teams; uncertainty about the right style.
- **Microkernel:** Product-based apps with planned extensions; multi-configuration cloud deployments; tight budget.
- **Event-Driven:** Reactive processing; high performance/scale/fault tolerance; complex nondeterministic workflows.
- **Microservices:** Decomposable into dozens-to-hundreds of independent functions; high agility/scale/fault tolerance/extensibility.
- **Space-Based:** Extreme concurrent scalability/elasticity; high performance; data fits in memory.

**Style-by-style when-NOT-to-use summary:**
- **Layered:** High operational concerns; domain-level change profile; cross-functional domain teams.
- **Microkernel:** High scalability/elasticity/fault tolerance needs; most changes in core.
- **Event-Driven:** Request-based/CRUD-dominant; sync processing required; high data consistency; strict event-ordering coordination.
- **Microservices:** Complex inter-service workflows; tightly coupled monolithic data; tight budget/time; high-performance/responsive systems; non-cross-functional teams.
- **Space-Based:** Large transactional data volumes; tight budget/time; high data consistency needed.

---

## Key Takeaways

1. Architecture is not optional — no style produces a "big ball of mud".
2. Monolithic vs distributed is the first decision: monolithic is simple/cheap, distributed has operational superpowers but inherits distributed-computing fallacies.
3. Partitioning must align with team structure (Conway's Law) and the change profile.
4. Layered is the sensible default — budget-tight, layer-scoped changes, technically organized teams.
5. Microkernel = stable core + plug-ins; only style that can be technical or domain partitioned.
6. Event-Driven solves reactive problems — but demands maturity in eventual consistency, error handling, workflow complexity.
7. Microservices = maximum agility/scale/fault-tolerance/extensibility but most complex/expensive; requires bounded context, data decomposition, and cross-functional teams.
8. Space-Based removes the DB from the transactional path for extreme elasticity — data must fit in memory.
9. Hybrid architectures are normal — combine styles once each is understood.
10. Cost and complexity correlate strongly: Layered/Microkernel ($), Event-Driven ($$$$), Microservices/Space-Based ($$$$$).
11. Styles → patterns → design patterns form a hierarchy. Keep the levels distinct.
12. Once chosen, an architecture is hard and expensive to change — analyze requirements thoroughly before committing.

---

## Cross-References
- Related: [[../Software_Architecture_Hardparts.md]] — trade-off analysis, granularity, data ownership, sagas, contracts
- Related: [[../Designing_Distributed_Systems.md]] — runtime component patterns (sidecar, ambassador, work queue, scatter-gather)
- Topic index: [[../INDEX.md]]