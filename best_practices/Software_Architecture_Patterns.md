# Software Architecture Patterns, 2nd Edition
**Author:** Mark Richards
**Topic tags:** `#architecture` `#general`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Software Architecture Patterns 2nd edition/Software Architecture Patterns 2nd edition.md` · `summaries/Software_Architecture_Patterns_2nd_edition.md`

## TL;DR
Five named architecture styles (Layered, Microkernel, Event-Driven, Microservices, Space-Based) classified by monolithic-vs-distributed deployment and by technical-vs-domain partitioning. Choose by operational characteristics (scale, fault tolerance, performance), team structure (Conway's Law), data decomposability, and budget — never by trend. Hybrid styles are the norm once each individual style is understood.

---

## Best Practices by Topic

### Terminology: Styles vs Patterns vs Design Patterns

**Principle:** The hierarchy is design patterns → architecture patterns → architecture styles. Conflating the three is the root of most architecture arguments.

**Do:**
- Reserve "architecture style" for macro structure (Layered, Microservices, …).
- Reserve "architecture pattern" for reusable structural blocks (CQRS, Saga, …).
- Reserve "design pattern" for class-level (Builder, Observer, Strategy, …).
- Compose them: e.g. Builder design pattern → CQRS architecture pattern → microservices architecture style.
- Combine styles into hybrids (event-driven microservices, space-based microservices, event-driven microkernel) only after understanding each one independently.

**Don't:**
- Don't call CQRS an "architecture" — it's an architecture pattern that lives inside a style.
- Don't pick a hybrid style until you understand each constituent style's strengths and weaknesses.

*Ref: Patterns 2e — "Introduction"*

---

### The Second Edition: What's Changed Since 2015

**Principle:** Both microservices and event-driven have matured significantly since the first edition. DDD's influence on partitioning is now mainstream. New sections for when to use (and not to use) each style.

**Do:**
- Recognize that microservices and event-driven are no longer "new" — they have well-understood patterns, pitfalls, and operational requirements.
- Use the second-edition guidance when evaluating these styles — the first edition glosses over data decomposition and orchestration concerns that the second edition treats in depth.
- Pay attention to the new "considerations and analysis" sections — they codify lessons learned from real-world adoption.

**Don't:**
- Don't fall back on first-edition advice when designing modern event-driven or microservices systems — the operational tooling and patterns have evolved substantially.

**Key evolutions:**
- Microservices: now widely understood to require bounded context, data decomposition, operational automation, and cross-functional teams simultaneously.
- Event-Driven: complex nondeterministic workflows (CEP) are now routinely modeled with event-driven + stream processing.
- DDD: now mainstream as the basis for domain partitioning decisions.
- Architecture-data intersection: explicit coverage in the second edition.

*Ref: Patterns 2e — "Introduction" / Foreword*

---

### Architecture Styles vs the "Big Ball of Mud"

**Principle:** Architecture is not optional. No style produces tightly coupled, brittle systems that are hard to change. Always pick a style deliberately.

**Do:**
- Use the architecture-style vocabulary to communicate trade-offs with developers, architects, QA, ops, and stakeholders.
- Let the chosen style reveal the system's characteristics: scalability, performance, agility, responsiveness.

**Don't:**
- Don't ship an application without a defined architecture style — that's the "big ball of mud": tightly coupled, brittle, difficult to change, no clear architectural characteristics.

**Symptom check — you might be in a big-ball-of-mud if:**
- You cannot answer "what's the architecture?" with a single style name.
- Every change ripples unpredictably across the codebase.
- New developers take months to find their bearings.
- You can't identify where to add new functionality without coordinating with many teams.

*Ref: Patterns 2e — "Introduction"*

---

### Architecture Classification: Monolithic vs Distributed

**Principle:** Monolithic = single deployment unit. Distributed = multiple deployment units. Distributed gives operational superpowers but inherits the fallacies of distributed computing. This classification is the first decision.

**Monolithic trade-offs:**
- Simpler, cheaper, faster to build.
- A fatal error (e.g. OOM) fails all functionality.
- MTTR/MTTS measured in minutes.
- Scaling scales the entire app even when only one part needs it — inefficient and costly.

**Distributed trade-offs:**
- Operational superpowers: per-service scalability, MTTS/MTTR in seconds or ms, high fault tolerance, agility.
- Eight fallacies of distributed computing bite: network is reliable (false), bandwidth is infinite (false), latency is zero (false), topology doesn't change (false), one administrator (false), cost is zero (false), transport is homogeneous (false), network is secure (false).
- Added complexity: distributed transactions, eventual consistency, workflow, error handling, data sync, contract management.
- Higher upfront and ongoing maintenance cost.

**When to choose distributed:**
- Different parts need different architecture characteristics (e.g. customer-facing needs scale/availability; back-office does not).
- Complex systems performing multiple business functions.
- Need for speed, high scalability, or high fault tolerance.

**When to choose monolithic:**
- Simple systems or websites.
- Tight budget / time constraints.
- One uniform set of architecture characteristics across the whole app.

**Style classification:**

| Style | Classification |
|---|---|
| Layered | Monolithic |
| Modular Monolith | Monolithic |
| Pipeline | Monolithic |
| Microkernel | Monolithic (typically) |
| Event-Driven | Distributed |
| Microservices | Distributed |
| Service-Based | Distributed |
| Service-Oriented | Distributed |
| Space-Based | Distributed |

**Triangle-of-bottlenecks mental model:** Most web apps follow the topology web server → app server → database. Scaling each tier is progressively harder: web servers scale easily (cheapest), app servers more expensively, database most expensively. The result is a "triangle" where the database is the narrowest part. Space-based solves this by removing the DB from the transactional path. Layered/Microkernel live in this triangle; Microservices mitigate it via per-service scaling; Space-Based removes the constraint entirely.

*Ref: Patterns 2e — "Architecture Classification" / "Space-Based — Topology and Components"*

---

### Architecture Partitioning: Technical vs Domain

**Principle:** Partitioning must align with team structure (Conway's Law) and the dominant change pattern (layer-scoped vs domain-scoped).

**Technical Partitioning:**
- Components grouped by layer (presentation, business, persistence, database).
- Namespace: `app.presentation.customer`, `app.business.customer`, `app.persistence.customer`.
- Good when teams are UI / backend / DBA silos and changes are layer-scoped (UI overhauls, DB migrations).

**Domain Partitioning:**
- Components grouped by domain area.
- Namespace: `app.customer`, `app.shipping`, `app.payment`.
- Sub-layers allowed (`app.customer.presentation`), but top-level is the domain.
- Good for cross-functional domain teams and DDD-aligned work.

**Decision rule:**
- Teams by technical specialty + layer-scoped changes → technical partitioning.
- Teams by domain (UI + backend + DBA per domain) + domain-scoped changes → domain partitioning.
- DDD-driven development → domain partitioning.

**Style × Partitioning matrix:**

| Style | Partitioning |
|---|---|
| Layered | Technical |
| Microkernel | Technical OR Domain (only style that can be either) |
| Event-Driven | Technical |
| Microservices | Domain |
| Space-Based | Technical |
| Modular Monolith | Domain |
| Service-Based | Domain |
| Pipeline | Technical |
| Service-Oriented | Domain |

**Domain anti-pattern example:** Adding "expiration date to wishlist items" in a technical-partitioned app touches DB layer (new column), persistence layer (SQL change), business layer (rules and contracts), and presentation layer (UI display). 3–4 teams must coordinate.

**Microkernel pivot:** When plug-ins are used as adapters/configurations → technically partitioned. When plug-ins add new domain functionality → domain partitioned.

*Ref: Patterns 2e — "Architecture Partitioning"*

---

### Conway's Law Alignment

**Principle:** Architecture structure must match team structure. Misalignment creates friction, coordination overhead, and slow change.

**Do:**
- Make the partitioning match your actual team topology.
- Move from technical to domain partitioning when you reorganize into cross-functional domain teams.
- Move from domain to technical partitioning when you specialize teams by layer (and accept that domain changes will ripple).
- Recognize that team reorganization is a forcing function for architecture change — and vice versa.

**Don't:**
- Don't choose domain partitioning if your teams are organized as UI / backend / DBA silos.
- Don't choose technical partitioning if you have cross-functional domain teams — they will fight the structure.

**Why this matters in practice:** If you choose microservices (domain-partitioned) but your teams are organized by UI/backend/DBA, every service will require three teams to coordinate on each change. The bottleneck isn't technology — it's communication. Conversely, a layered architecture with cross-functional domain teams will produce friction because each change request spans multiple teams' specialties.

*Ref: Patterns 2e — "Architecture Partitioning" — "Which One Should I Choose?"*

---

### Layered Architecture

**Principle:** The de-facto standard. Best when budget/time is tight, changes are layer-scoped, and teams are technically organized.

**Topology:** Presentation → Business → Persistence → Database. Optionally combine business+persistence (3 layers) or split into more (5+ layers).

**Layers of Isolation:** Closed layer = request must pass through it. Open layer = request can bypass it.
- Default: keep layers closed to preserve isolation.
- Open a shared-services layer below business so business can bypass it to reach persistence.
- Document which layers are open/closed and why — failure to do so produces tightly coupled, brittle architectures.

**Separation of concerns:** Each layer has a specific role and forms an abstraction over its work. Presentation doesn't know *how* to get customer data; business doesn't know *how* to format it for display; persistence doesn't know what UI uses it. This makes it easy to build role/responsibility models and to develop, test, govern, and maintain with well-defined interfaces and contracts.

**Refactoring power of layer isolation:** Convert presentation framework from AngularJS to React? Business layer unaffected if contracts are stable. Replace a relational DB with NoSQL? Persistence layer only. The bounded scope is the value of layers-of-isolation — IF the layers are closed.

**Architecture sinkhole anti-pattern:** Requests pass through layers with no logic at each layer.
- Apply 80/20 rule: ~20% pass-through is healthy. If 80%+ is pass-through, open some layers (and accept loss of layer isolation).

**Code (namespace example showing technical partitioning):**
```
app.presentation.customer  // presentation layer, customer domain
app.business.customer      // business layer, customer domain
app.persistence.customer   // persistence layer, customer domain
// The "customer" node is duplicated across layers — that's the giveaway
// for technical partitioning.
```
*Ref: Patterns 2e — "Layered Architecture — Description / Key Concepts"*

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

*Ref: Patterns 2e — "Architecture Characteristics" — Figure 3-5*

**Do:**
- Use when budget/time is tight and the team is technically organized.
- Use when most changes are isolated to a single layer (UI refresh, business-rule change, DB swap).
- Document which layers are open vs closed and why.
- Leverage layered isolation to make framework or DB swaps a single-layer change.

**Don't:**
- Use when high scalability, fault tolerance, or elasticity are required.
- Use when most changes are domain-scoped (e.g. adding expiry date to wishlist items touches every layer).
- Use when teams are cross-functional by domain.
- Open layers without documenting the choice — undocumented openness is how sinkholes become untestable.

---

### Layered — Worked Example

**Principle:** Understand the request/response flow through a layered architecture before committing to it.

**Principle:** A stable core system with plug-in modules. The only style that can be technically or domain partitioned.

**Topology:** Core system + plug-in modules + (optionally) plug-in registry.

**Plug-in connection modes:**
1. **Point-to-point** (JAR/DLL/OSGi/Jigsaw/Prism) → monolithic deployment.
2. **Consolidated codebase** (namespace like `app.plugin.assessment.iphone12`) → monolithic, but separate concerns.
3. **Remote services** (REST/messaging) → distributed microkernel, easier runtime deployment, better scalability.

**Plug-in registry:** Holds name, contract details (input/output), and remote-access protocol. When contracts are standard, registry may only hold name and interface name.

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

*Ref: Patterns 2e — "Architecture Characteristics" — Figure 4-3*

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

**Why event-driven gained popularity:** Complex nondeterministic workflows and highly reactive/responsive systems are hard to model with other styles. Modern techniques, tools, frameworks, and cloud-based services have made event-driven more accessible than ever.

**Components:**
- **Event processor (service):** main deployment unit; triggers and responds to events. Varies from a single-purpose function to a complex process.
- **Initiating event:** comes from outside the system; noun-verb naming ("Place Order").
- **Processing event (derived):** state-change advertisement; verb-noun ("Order Placed").
- **Event channel:** queue (point-to-point, initiating) or topic (publish-subscribe, processing).

**Channel ownership rule:**
- Events: sender owns the channel AND the contract.
- Messages: receiver owns the channel AND the contract.

**Always advertise state changes** even if no current consumer — provides architectural extensibility.

**Why naming matters:** Initiating event is noun-verb ("Place Order") because it's an incoming action. Processing event is verb-noun ("Order Placed") because it's an outgoing state-change advertisement. Mixing the two confuses consumers and breaks the abstraction.

**One-to-many fan-out:** A single initiating event typically spawns many processing events. Example: Place Order → Order Placed → Payment Applied + Inventory Updated + Customer Notified. The "Payment Applied" event then triggers further derived events.

**Event-Driven vs Message-Driven:**

| Property | Event | Message |
|---|---|---|
| Context | Announces state change ("I placed an order") | Command to specific service ("apply payment") |
| Sender knowledge | Doesn't know receivers | Knows receiver |
| Channel owner | Sender | Receiver |
| Channel type | Topic / pub-sub (typically) | Queue / point-to-point (typically) |
| Contract owner | Sender | Receiver |
| Typical use | Reactive broadcast | Targeted command |

**Channel flexibility:** Event-driven systems can use point-to-point messaging when needed — for example, to retrieve specific info from another service or to control event ordering. It's not a strict either/or.

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

*Ref: Patterns 2e — "Architecture Characteristics" — Figure 5-5*

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

**Data ownership clarification:** Each service owns its own collection of tables (typically as a schema in a single highly-available DB, or in a single DB devoted to a particular domain). The key invariant: only the service owning the tables can access/update that data. Other services request the data from the owning service via its contract.

**API gateway contract:** Hides the location and implementation of corresponding services for each endpoint. May perform cross-cutting infrastructure functions (security, metrics, request-ID generation). Crucially: it contains NO business logic, NO orchestration, NO mediation. Putting these in the gateway is the SOA mistake that destroyed bounded context.

**Why "micro" doesn't mean small:** Consider a service with 312 class files, each handling a different customer email (welcome, password reset, order confirmation, etc.). It still counts as a microservice because it does one thing — sends customer emails — extremely well. "Micro" refers to functional scope, not lines of code or class count.

**Scale of microservices:** Hundreds to thousands of separately deployed services is common. The sheer number is what makes microservices unique among architecture styles.

**Deployment forms:** Containerized services (Docker) or serverless functions.

**Topology:** API gateway (no business logic, no orchestration, no mediation) → services → each owns its own data.

**Microservice definition:** Single-purpose, separately deployed unit of software that does one thing really well. "Micro" refers to functional scope, NOT physical size.
- Example: a service with 312 class files that all handle different customer emails is still a microservice because it does one thing.

**Bounded Context (Eric Evans, DDD):** All source code for a domain/subdomain + corresponding data structures + data encapsulated as one unit. Microservices cannot exist without it.

**Why microservices can't exist without bounded context:** Imagine 250 microservices all accessing the same set of tables in one monolithic database. A structural change (e.g. dropping a column accessed by 120 services) requires coordinated changes to 120 services plus the DB — infeasible. Bounded context ensures only the owning service changes for structural data changes.

**Three unique features that distinguish microservices from ALL other styles:**
1. **Distributed data** — only style that *requires* data to be broken up.
2. **Operational automation** — containerization (Docker), orchestration (Kubernetes), CI/CD, DevOps are required, not optional.
3. **Organizational change** — only style that *requires* cross-functional domain teams.

**Practical exception:** Some data sharing between 2-6 services is normal — driven by table coupling, FK constraints, triggers, materialized views, performance needs, shared ownership. When shared, the bounded context extends to include all shared tables and the services accessing them.

**Bounded context contract detail:** When service A needs data from service B's bounded context, it calls through a contract. That contract is usually a different representation than the physical DB structure, so service B can change its internal schema without breaking A.

**Three latencies that hurt performance:**
- **Network latency:** 30-300+ ms depending on protocol and distance.
- **Security latency:** few ms to 300+ ms for authn/authz.
- **Data latency:** time for another service to query data on your behalf (replaces a JOIN with a remote call + DB call). Example: Wishlist service asks Product Catalog for descriptions → Product Catalog makes an extra DB call. With shared DB, a single INNER JOIN would have done it.

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

*Ref: Patterns 2e — "Architecture Characteristics" — Figure 6-4*

**Do:**
- Verify feasibility to break functionality into dozens to hundreds of independent pieces.
- Use when high agility, fault tolerance, scalability, and extensibility are needed.
- Align with cross-functional domain teams + service owners (architects) per domain.
- Use containerization + Kubernetes + automated CI/CD from day one.
- Treat new services as "drop-in functionality" — wrap in container, expose API endpoint, deploy.
- Treat BI / analytics reports as microservices accessing a data lake / warehouse (stable schema, low breaking-change risk).
- Recognize that hot-deploying a single service in the middle of the day is feasible because deployment risk is contained to that service.

**Architectural agility benefit in detail:**
- Change scope: easy to locate because functionality is divided into separately deployed units.
- Testing scope: reduced to only the service that is impacted.
- Deployment risk: only the impacted service is typically deployed.
- Result: significantly lower coordination cost than big-bang weekend deployments.

**Don't:**
- Use for complex workflows that require tight orchestration between separately deployed services.
- Use if your data can't be broken into dozens to hundreds of separate schemas/databases (FK constraints, triggers, views, stored procedures all block this).
- Use on tight budget/time constraints — most complex and expensive style.
- Use for high-performance / highly responsive systems — inter-service latency is the killer.
- Repeat the SOA mistake of putting business logic / orchestration / mediation in the API gateway.
- Use if your teams aren't cross-functional and organized by domain.

---

### Microservices — When to Consider / When to Walk Away

**Principle:** Microservices is the most opinionated, costly, and powerful style. Apply a strict four-condition test before adopting.

**The four preconditions (all must hold):**
1. **Data decomposability:** Can your data be split into dozens-to-hundreds of separate schemas or databases, each with bounded context?
2. **Operational automation:** Do you have (or will you build) containerization + container orchestration + automated CI/CD + DevOps practices from day one?
3. **Cross-functional domain teams:** Are your teams organized as cross-functional domain teams with UI, backend, and DB expertise per domain?
4. **High-value agility, scale, fault tolerance, or extensibility:** Do you genuinely need these, and is the cost justified?

If any precondition fails, consider modular monolith, service-based, or another intermediate style first.

**When microservices is a strong fit:**
- Agility is critical (rapid changes, hot deploys, isolated testing).
- Different functions need independent scaling (e.g. search scales differently from checkout).
- Aggressive extensibility (drop-in new services without touching existing ones).
- You can decompose the data (the dealbreaker in practice).

**When microservices is the wrong choice:**
- Complex tightly-orchestrated workflows between separate services.
- Monolithic tightly-coupled data (FK constraints, triggers, views, stored procedures everywhere).
- Tight budget/time.
- High-performance / sub-100ms responsiveness requirements.
- Non-cross-functional teams organized by layer.

**Do:**
- Use microservices when you've honestly verified all four preconditions.
- Use it for systems with separate and distinct business functions.
- Leverage drop-in functionality (container + endpoint + deploy) as your extensibility lever.
- Plan for the microservice tax up front — CI/CD, observability, contract testing.

**Don't:**
- Don't migrate to microservices to escape a bad monolith — fix the monolith first, then carve.
- Don't pick it because "everyone is doing it" — pick it because your context requires it.
- Don't skip the bounded-context thinking — it's the only thing keeping microservices coherent.

*Ref: Patterns 2e — "Microservices — Considerations and Analysis"*

**Principle:** Several recurring hard problems make microservices difficult to get right. Know them upfront.

**Hard parts:**
- **Service granularity:** Single-responsibility principle is subjective; use code volatility, fault tolerance, scalability, throughput, access control as objective factors.
- **Inter-service communication:** Sync vs async, orchestration vs choreography — every choice has trade-offs.
- **Data sharing:** When service A needs data from service B, choose REST inter-service call, in-memory data grid cache, expand the schema, or share the data — each has trade-offs.
- **Distributed transaction management:** Two-phase commit, sagas, eventual consistency — all add complexity.
- **Contracts:** API contracts must be versioned, backward-compatible, and centrally managed.
- **Code reuse:** Shared libraries risk coupling; duplication risks drift. Choose carefully per case.
- **Migration patterns:** Moving from monolithic to microservices is its own discipline — strangler, parallel-run, etc.

**Do:**
- Validate that your functionality actually decomposes into dozens-to-hundreds of independent pieces *before* committing to the style.
- Budget for the "microservice tax" — CI/CD, container orchestration, observability, contract testing, distributed tracing.
- Treat hard parts as first-class design concerns — don't discover them after the 100th service is deployed.
- Lean on Neal Ford et al., *Software Architecture: The Hard Parts* (O'Reilly) for the trade-off analysis.

*Ref: Patterns 2e — "Considerations and Analysis"*

---

### Space-Based Architecture

**Principle:** Removes the database from the transactional processing path by using replicated in-memory data grids. Built for extreme elasticity and concurrency.

**Why "space-based"?** The name comes from *tuple space* — a computer science term describing multiple parallel processors sharing memory via replicated in-memory data grids.

**Processing unit structure:** Each processing unit contains business functionality + in-memory data grid + (optionally) web-based components. Granularity varies from a single-purpose function to the entire application functionality. Processing units may communicate with each other directly or through the processing grid of the virtualized middleware.

**Topology:** Processing units (application logic + in-memory data grid + optional web components) + virtualized middleware.

**Virtualized middleware components:**
- **Messaging grid** — request/session management; forwards to available processing units (round-robin or next-available); typically a web server.
- **Data grid** — replicates in-memory data across processing units; uses Hazelcast / Apache Ignite / Oracle Coherence; includes data pumps (async to DB), data writers (apply DB updates), data readers (cold-start from DB).
- **Processing grid (optional)** — orchestration or choreography between processing units.
- **Deployment manager** — dynamic start/stop of processing units based on load (typically Kubernetes).

**Cold-start rule:** Start at least one processing unit populated before adding more — they replicate from each other, not from the DB.

**Data grid consistency invariant:** Each processing unit must contain *exactly* the same data in its in-memory data grid as every other unit. The messaging grid can forward a request to any unit, so any unit must be able to serve any request correctly.

**Deployment models:**
- Cloud only.
- On-prem only.
- **Hybrid split:** cloud processing units, on-prem DB with data writers/readers — particularly effective when data must remain on-prem.

**Use cases:** Concert ticketing, online auctions, high-volume social media — anywhere concurrency spikes from dozens to tens of thousands in seconds.

**Why agility is low (2/5):** Technical complexity makes changes expensive. High complexity and load testing are also expensive. Reaching very high user loads in a test environment is both expensive and time-consuming.

**Why partition type is "Technical":** Domain functionality is spread across processing units, in-memory data grids, data pumps, data writers, and data readers. A domain-based change (especially to data) usually impacts all of these.

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

*Ref: Patterns 2e — "Architecture Characteristics" — Figure 7-5*

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

| | Layered | Microkernel | Event-driven | Microservices | Space-based |
|---|---|---|---|---|---|
| Partitioning | T | D/T | T | D | T |
| Overall cost | $ | $ | $$$$ | $$$$$ | $$$$$ |
| Agility | ● | ●●● | ●●●● | ●●●●● | ●●● |
| Simplicity | ●●●●● | ●●●● | ● | ● | ● |
| Scalability | ● | ● | ●●●●● | ●●●●● | ●●●●● |
| Fault tolerance | ● | ● | ●●●●● | ●●●●● | ●●●● |
| Performance | ●●● | ●●● | ●●●●● | ●●● | ●●●●● |
| Extensibility | ● | ●●● | ●●●●● | ●●●●● | ●●●● |

*Ref: Patterns 2e — "Style Analysis Summary" — Figure A-1*

**Reading the matrix:**
- Scalability priority → event-driven, microservices, or space-based.
- Simplicity/cost priority → layered or microkernel.
- Layered chosen → deployment, performance, scalability are the risk areas.
- Microkernel chosen → scalability, fault tolerance are the risk areas.

**Choosing flow:**
1. Start by identifying your architecture characteristics requirements (scale, fault tolerance, performance, agility, simplicity, cost).
2. Use the matrix to shortlist styles that meet those requirements.
3. Cross-check against partitioning fit (technical vs domain).
4. Cross-check against team structure (Conway's Law).
5. Cross-check against data decomposability (microservices specifically).
6. Validate with a worst-case "what if we picked wrong" analysis.

---

### Layered — Worked Example

**Principle:** Understand the request/response flow through a layered architecture before committing to it.

**Example flow (retrieve customer info + their orders):**
- **Customer screen** (presentation) accepts the request; doesn't know where data is, how it's retrieved, or how many tables are queried.
- **Customer delegate** (presentation) knows which business module can process the request and what contract is required.
- **Customer object** (business) aggregates all information needed; invokes the data access objects.
- **Customer DAO + Order DAO** (persistence) execute SQL; return results back up.
- **Customer object** aggregates; passes to delegate; delegate passes to screen for display.

**Implication:** When the customer adds a new requirement (e.g. show "loyalty tier"), the change ripples top-to-bottom:
- DB schema (new column)
- DAO (new SQL)
- Business object (new field on aggregate)
- Delegate (new field on contract)
- Screen (new UI control)

*Ref: Patterns 2e — "Layered — Examples"*

---

### Microkernel — Worked Example

**Principle:** Insurance claims processing is a textbook case for microkernel because jurisdiction rules are volatile but the core flow is stable.

**Example (insurance claims):**
- Core system = generic claims processing flow (intake → assess → payout) — changes rarely.
- Plug-ins = jurisdiction-specific rules per US state (free windshield replacement in some, not in others).
- Plug-ins can be implemented as custom source code or separate rules-engine instances.
- Plug-ins can be added, removed, or changed with little or no effect on the rest of the core system or other plug-ins.

**Why microkernel beats a rules-engine monolith here:**
- Rules engines for jurisdictional logic grow into a "big ball of mud" — changing one rule impacts others, requires an army of analysts/testers.
- Microkernel isolates each jurisdiction in its own plug-in; each can evolve independently.

**Generalization:** Microkernel works wherever the core is stable and the variation surface is well-known and plug-in-shaped.

*Ref: Patterns 2e — "Microkernel — Examples"*

---

### Event-Driven — Worked Example

**Principle:** Use a concrete end-to-end scenario to internalize the actor/event flow.

**Architectural extensibility insight:** Even though no current service consumes **Notified Customer**, Order Placement still publishes it. Future services (notification tracking, customer engagement analytics) can subscribe without any change to Order Placement. This is one of the strongest arguments for event-driven architecture — you get extensibility for free.

**Channel selection rationale:**
- **Place Order** uses a queue (point-to-point) because the system needs exactly-once-once-processing for the initiating action — only one Order Placement service should handle the placement.
- **Order Placed**, **Payment Applied**, **Inventory Updated**, **Notified Customer** use topics (pub-sub) because multiple downstream services may independently react to each state change.

**Nondeterminism accepted by design:** Order Placement does not know in advance how many services will respond to Order Placed or what business logic each will run. This is the essence of event-driven decoupling — but it places the burden of correctness on the event contract, not on the choreography.

*Ref: Patterns 2e — "Event-Driven — Example Architecture / Considerations"*

**Example (ordering a book — "Fundamentals of Software Architecture" by Mark Richards & Neal Ford):**
1. Customer triggers **Place Order** (initiating event, noun-verb, point-to-point channel).
2. **Order Placement service** receives it; processes the order.
3. Order Placement advertises **Order Placed** (processing event, verb-noun, pub-sub topic).
4. Three independent services respond in parallel:
   - **Payment service** applies payment; advertises **Payment Applied**.
   - **Inventory Management service** updates inventory; advertises **Inventory Updated**.
   - **Notification service** notifies customer; advertises **Notified Customer**.
5. Even though no other service currently cares about **Notified Customer**, Order Placement advertises it for **architectural extensibility** — future services (e.g. notification tracking) can subscribe without changes to the producer.

**Key insight:** Order Placement doesn't know which services will respond to Order Placed. That's the highly decoupled, nondeterministic nature of event-driven architecture.

**Error-handling complexity:** What if Notification + Payment succeed but Inventory errors (out of stock)? Customer was notified and charged but nothing to ship. Who reverses the payment? Who sends another notification? Error handling is one of the most complex aspects of event-driven architecture and must be designed for up front.

*Ref: Patterns 2e — "Event-Driven — Example Architecture / Considerations"*

---

### Microservices — Worked Use Cases

**Principle:** Two patterns dominate real-world microservices adoption.

**Pattern 1 — Order entry ecosystem:**
- Place order, apply payment, notify customer, manage inventory, fulfill order, ship order, track order, send surveys, analytics → each is a separate, distinct microservice.
- Each has its own data ownership.

**Pattern 2 — BI / analytics reporting:**
- Each report, query, data feed, or data analytics = a microservice.
- All consume from a data lake or data warehouse.
- Doesn't strictly meet bounded-context-for-data (the data is shared), but the underlying schema rarely changes (older schemas are deprecated, new ones created). This low breaking-change risk makes microservices viable here.

**Why Pattern 2 works despite loose data ownership:**
- Data lake/warehouse schemas are append-and-deprecate, not evolve-in-place.
- A new column gets added; old reports still work; new reports can opt in.
- This pattern has lower breaking-change frequency than transactional microservices.
- It's a useful way to get started with microservices if your transactional data isn't yet decomposable.

*Ref: Patterns 2e — "Microservices — Examples and Use Cases"*

---

### Space-Based — Worked Use Cases

**Principle:** The style is targeted at specific high-concurrency scenarios — not a general-purpose default.

**Example — Concert ticketing:**
- Favorite rock band announces a show; tickets go on sale.
- Concurrency goes from a few dozen to tens of thousands in seconds.
- Continuously reading and writing to a database is infeasible at this scale.
- In-memory data grids across processing units handle the load.

**Example — Online auctions / bidding:**
- Sellers can't predict concurrent bidders.
- Bidding gets fast and furious at end-of-auction; then drops to a minimum; repeat.
- Classic elasticity profile.

**Example — High-volume social media:**
- Hundreds of thousands to millions of posts, likes, dislikes, responses within seconds.
- DB is the bottleneck regardless of elasticity; space-based removes it from the path.

*Ref: Patterns 2e — "Space-Based — Examples"*

---

### Hybrid Architecture Styles

**Principle:** Combine styles when individual styles don't solve the whole problem — but only after understanding each style's trade-offs.

**Common hybrids:**
- **Event-driven microservices** — events flowing between microservices.
- **Space-based microservices** — processing units implemented as microservices.
- **Event-driven microkernel** — events between core system and remote plug-ins.

**Do:**
- Pick a hybrid deliberately after independently understanding each constituent style.
- Use event-driven microservices when you need both agility/extensibility (from microservices) AND eventual consistency / high decoupling (from event-driven).

**Don't:**
- Don't combine styles without first understanding each one's trade-offs.

*Ref: Patterns 2e — "Introduction"*

---

## Anti-Patterns & Common Mistakes

- **Big Ball of Mud:** No architecture style → tightly coupled, brittle. *Fix:* Pick a style deliberately. *Ref: Patterns 2e — "Introduction"*

- **Architecture Sinkhole (Layered):** Pass-through requests dominate (>80%). *Fix:* Open some layers OR switch style. *Ref: Patterns 2e — "Layered — Considerations and Analysis"*

- **API Gateway as ESB:** Putting business logic, orchestration, or mediation in the API gateway. *Fix:* API gateway must have NO business logic to preserve bounded context. *Ref: Patterns 2e — "Microservices — Basic Topology"*

- **Microservices without bounded context:** Hundreds of services sharing one monolithic DB → structural changes become infeasible. *Fix:* Enforce data ownership per service. *Ref: Patterns 2e — "Microservices — Bounded Context"*

- **Microservices for high-performance systems:** Inter-service latency (network + security + data) destroys responsiveness. *Fix:* Use space-based or hybrid. *Ref: Patterns 2e — "Microservices — When Not to Consider This Style"*

- **Microservices without DevOps:** Hand-offs to test/release teams don't scale to hundreds of services. *Fix:* Cross-functional teams own their services end-to-end; container orchestration + CI/CD are required. *Ref: Patterns 2e — "Microservices — Unique Features"*

- **Microkernel for high-scale systems:** Core becomes the bottleneck and SPOF. *Fix:* Use a distributed style. *Ref: Patterns 2e — "Microkernel — When Not to Consider This Style"*

- **Event-driven for sync / CRUD-dominant processing:** Asynchronous processing fights the use case. *Fix:* Use layered or service-based. *Ref: Patterns 2e — "Event-Driven — When Not to Consider This Style"*

- **Event-driven without error-handling strategy:** Partial workflow completions create unrecoverable states (e.g. charged + notified but out of stock). *Fix:* Design saga / compensating transactions explicitly. *Ref: Patterns 2e — "Event-Driven — When Not to Consider This Style"*

- **Space-based with too-large transactional data:** Cannot fit 45 TB in memory. *Fix:* Use a different style for large-data systems. *Ref: Patterns 2e — "Space-Based — When Not to Consider This Style"*

- **Mixing partitioning and team structure:** Technical partitioning with domain teams (or vice versa). *Fix:* Conway's Law — align partitioning with team structure. *Ref: Patterns 2e — "Architecture Partitioning"*

- **Style driven by trend instead of fit:** Microservices because "everyone uses it" without data decomposability. *Fix:* Run the honest assessment; consider service-based as a middle ground. *Ref: Patterns 2e — "Considerations and Analysis"*

- **Layered architecture applied to domain-heavy change profile:** Adding wishlist expiration ripples through every layer and team. *Fix:* Switch to domain-partitioned style. *Ref: Patterns 2e — "Layered — When Not to Consider This Style"*

- **Microservices to escape a bad monolith:** Migration by ripping the monolith into 100 services without bounded-context thinking. *Fix:* Use modular monolith or service-based as stepping stones; only commit to microservices when data, team, and operational automation are all ready. *Ref: Patterns 2e — "Microservices — Considerations and Analysis"*

- **Treating "modern" event-driven as a CRUD bus:** Publishing CRUD-shaped operations as events with all four fallacies of distributed computing still in play. *Fix:* model events as state or business-fact transitions; budget for error handling and saga patterns up front.

---

## Decision Heuristics / Checklists

**Choosing monolithic vs distributed:**
- Different parts need different architecture characteristics → distributed.
- One uniform characteristic set + tight budget → monolithic.
- Simple system or website → monolithic.
- Complex multi-function system → distributed.
- Need for speed, scale, or fault tolerance → distributed.

**Choosing technical vs domain partitioning:**
- Teams by UI/backend/DBA specialty → technical partitioning.
- Cross-functional domain teams → domain partitioning.
- DDD-driven development → domain partitioning.
- Changes mostly layer-scoped → technical partitioning.
- Changes mostly domain-scoped → domain partitioning.

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

**Architecture change cost reminder:** Once an architecture is in place, it is very hard and expensive to change. Analyze requirements thoroughly — including infrastructure support, developer skill set, project budget, project deadlines, and application size — before committing.

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
13. The "best" style is the one that matches your operational characteristics, team structure, change profile, and budget — not the one trending in conference talks.
14. Microservices is not a free lunch: it requires bounded context, distributed data, operational automation, and cross-functional teams simultaneously.
15. Space-Based is a targeted solution for specific high-concurrency scenarios, not a general-purpose default.

---

## Cross-References
- Related: [[../Software_Architecture_Hardparts.md]] — trade-off analysis, granularity, data ownership, sagas, contracts
- Related: [[../Designing_Distributed_Systems.md]] — runtime component patterns (sidecar, ambassador, work queue, scatter-gather)
- Related: [[../Fundamentals_of_Software_Architecture.md]] — deeper coverage of the same five styles from a fundamentals lens
- Related: [[../Building_An_Event-Driven_Data_Mesh.md]] — event-driven design and data products for mesh architectures
- Topic index: [[../INDEX.md]]