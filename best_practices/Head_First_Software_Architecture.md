# Head First Software Architecture

**Authors:** Raju Gandhi, Mark Richards, Neal Ford
**Topic tags:** `#architecture` `#general`
**Language focus:** Language-agnostic; style and trade-off oriented
**Sources:** `markdown_output/Head First Software Architecture/Head First Software Architecture.md` · `summaries/Head_First_Software_Architecture.md`

## TL;DR
A learner's guide to architectural thinking through four dimensions (characteristics, decisions, logical components, styles). The book's two laws: (1) **everything in software architecture is a trade-off** and (2) **understanding why is more important than knowing how**. Practice via trade-off analysis, ADRs, and architecture-style selection. Cover monolithic styles (layered, modular monolith, microkernel) and distributed styles (microservices, event-driven), plus the most common modern hybrid: event-driven microservices.

---

## Best Practices by Topic

### The Four Dimensions of Software Architecture

**Principle:** Architecture is described by four aligned dimensions:

| Dimension | Definition |
|-----------|-----------|
| **Architectural Characteristics** | Non-domain "ilities" the architecture must support |
| **Architectural Decisions** | Rules/constraints that guide how the system is built |
| **Logical Components** | Functional building blocks; how pieces fit together |
| **Architectural Style** | Overarching structural pattern (layered, microservices, EDA, etc.) |

**Do:**
- Design the logical architecture *before* the physical architecture.
- Drive architectural decisions from characteristics.
- Keep all four dimensions aligned — they reinforce each other.

**Don't:**
- Don't confuse architecture with design. Architecture decisions: structural, broad impact, hard to reverse, affect whole system. Design decisions: localized, easier to change.
- Don't pick an architectural style first — let characteristics drive the choice.

*Ref: Head First Software Architecture.md — "Software Architecture Demystified"*

---

### The Two Laws of Software Architecture

**Law #1: Everything in software architecture is a trade-off.**
**Law #2: Understanding *why* you made a decision is more important than knowing *how* to implement it.**

**Trade-off analysis framework:**
1. Identify the options.
2. Evaluate each option's benefits and costs.
3. Consider the context (requirements, constraints).
4. Make a decision.
5. Document the decision (with rationale).

**When is a decision *architectural* (vs. design)?**
- Hard to reverse or change
- Affects multiple components/teams/stakeholders
- Involves significant trade-offs
- Impacts architectural characteristics
- Influences system structure

**Do:**
- Apply context-aware analysis to every decision.
- Document the *why*, not just the *what*.
- Train yourself to spot when "best practice" claims are actually context-dependent.

**Don't:**
- Don't reach for "best practices" — there are none in architecture, only contextually appropriate decisions.
- Don't skip the why — context changes, but understanding survives.

*Ref: Head First Software Architecture.md — "The Two Laws of Software Architecture"*

---

### Architectural Characteristics (The "-ilities")

**Definition:** Architectural characteristics are *non-domain design considerations* that influence structure and require trade-offs.

**Categories:**

| Category | Examples |
|----------|----------|
| **Operational** | Performance, availability, scalability, reliability, elasticity |
| **Structural** | Extensibility, maintainability, testability, configurability |
| **Cross-cutting** | Security, data integrity, privacy, auditability |

**Sources of characteristics:**
1. Problem domain (trading system → ultra-low latency; healthcare → strict privacy)
2. Environmental awareness (deployment, team structure, operational context)
3. Holistic domain knowledge (architect's experience surfaces what stakeholders don't mention)

**Composite characteristics:**
- "Performance" is composite; "first contentful paint" is a measurable sub-characteristic.
- If you can't measure a characteristic, decompose it until you can.

**The critical limit:**
- Pick **3–5 top-priority characteristics**. More → over-engineering.

**Do:**
- Make characteristics measurable. If you can't, decompose or remove.
- Use ISO 25010 categories for completeness.
- Document which characteristics are out-of-scope — and why.

**Don't:**
- Don't try to maximize all characteristics — they trade off.
- Don't pick characteristics without business justification.
- Don't add characteristics because they sound good — every added characteristic costs.

*Ref: Head First Software Architecture.md — "Architectural Characteristics"*

---

### Architecture Decision Records (ADRs)

**ADR template (5 sections):**

| Section | Purpose |
|---------|---------|
| **Title** | Noun phrase describing the decision |
| **Status** | Proposed / Accepted / Deprecated / Superseded |
| **Context** | Forces at play — constraints, requirements, concerns |
| **Decision** | What was decided and why |
| **Consequences** | Honest list of benefits AND drawbacks |

**Do:**
- Use noun-phrase titles ("Use PostgreSQL for transactional data" — not "Database choice").
- Update status as decisions evolve (Accepted → Deprecated → Superseded).
- Store ADRs in version control alongside code.
- Treat ADRs as **governed** — reviewed, referenced, maintained.
- Be honest about consequences — both positive and negative.
- Reference related ADRs (especially Superseded relationships).

**Don't:**
- Don't write a Decision section without rationale — context + decision + consequences must stand alone.
- Don't skip consequences (especially downsides) — that's where future architects learn.
- Don't let in-document comments accumulate after release — move discussion elsewhere.

**Benefits of ADRs:**
- Prevent re-litigating settled decisions.
- Onboard new team members.
- Support governance (auditable).
- Enable evolution (Superseded links form architectural history).

*Ref: Head First Software Architecture.md — "Architecture Decision Records"*

---

### Logical Components

**Definition:** Functional building blocks — how the system's pieces fit together at a logical level, independent of physical deployment.

**Logical vs. Physical architecture:**
- **Logical**: what the components are and how they interact (responsibilities, boundaries).
- **Physical**: how components are deployed and communicate at runtime (servers, containers, network calls).

**Four-step process for creating logical architecture:**
1. **Identify initial core components** (workflow approach OR actor/action approach)
2. **Assign requirements** — every requirement must map to a component
3. **Analyze roles and responsibilities** — cohesion, single responsibility
4. **Analyze characteristics** — split or restructure for performance, scalability, etc.

**Two identification approaches:**

| Approach | How | Best for |
|----------|-----|----------|
| Workflow | Group functionality by use cases (user registration, item listing, bid placement) | Systems with clear workflows |
| Actor/Action | Group actions by actor (sellers list items, bidders place bids) | Systems with clear actors |

**The Entity Trap:**
- ❌ Don't model components after domain entities ("Order Manager," "Customer Service")
- Why bad: vague names, too many responsibilities, poor cohesion, hard to scale.
- Watch for words like "manager," "supervisor," "handler" in names — these signal the trap.
- ✅ Group by cohesive *responsibility*, not by entity.

**Component coupling (4 types):**

| Type | Definition | Implication |
|------|-----------|-------------|
| **Afferent coupling (Ca)** | How many components depend on this one | High = widely used; changes affect many |
| **Efferent coupling (Ce)** | How many components this depends on | High = vulnerable to external change |
| **Abstractness** | Ratio of abstract types to total types | High = extension point; low = concrete |
| **Instability** | Ce / (Ca + Ce) | High = volatile; low = stable |

**Distance from the Main Sequence:**
- Ideal: balanced (abstract + stable OR concrete + unstable).
- Plot distance to identify modules that are misaligned.

**Law of Demeter (Principle of Least Knowledge):**
- Components should talk to immediate friends, not strangers.
- Avoid chains: `a.getB().getC().doSomething()`.

**Do:**
- Aim for **high cohesion within, loose coupling between**.
- Make component names describe *what they do*, not what entity they manage.
- Use the Law of Demeter — favor `a.doSomething()` over chains.

**Don't:**
- Don't decompose by entity alone.
- Don't accept poor cohesion as a trade-off — refactor or split.
- Don't expose internals through chains of method calls.

*Ref: Head First Software Architecture.md — "Logical Components"*

---

### Architectural Styles — Categorization Matrix

**Two axes:**

|  | Technical Partitioning | Domain Partitioning |
|--|------------------------|---------------------|
| **Monolithic Deployment** | Layered | Modular Monolith |
| **Distributed Deployment** | (rare) | Microservices, Event-Driven |

**Monolithic pros:** simpler dev/test/deploy, no network latency, easier transactions, lower operational complexity.
**Monolithic cons:** limited scalability, single point of failure, longer deploy cycles, technology lock-in.

**Distributed pros:** independent scalability, fault isolation, technology diversity, independent deployment.
**Distributed cons:** network latency, distributed transaction complexity, operational overhead, contract management.

**Do:**
- Pick a style based on context — no style is universally better.
- Start simpler; evolve when needed.

**Don't:**
- Don't pick distributed styles for distributed-style-sake — operational overhead is real.

*Ref: Head First Software Architecture.md — "Architectural Styles — Categorization and Philosophies"*

---

### Layered Architecture

**Standard layers:** Presentation → Workflow/Business → Persistence → Database.

**Design patterns:** MVC, layers of isolation, sinkhole anti-pattern (pass-through layers that add no value).

**The mapping problem:** Logical components (domain) don't map cleanly to layers (technical). A single domain change may touch multiple layers.

**Drivers for layered:**
- Simple system
- Time-to-market critical
- Small team familiar with pattern
- Domain not expected to change much

**Superpowers:** Simplicity, familiarity, fast initial development, clear separation.

**Kryptonite:** Poor scalability (must scale all), poor fault tolerance (failure cascades), domain changes touch many layers, monolithic coupling tendency.

**Star ratings:** Low overall agility, low scalability/testability, high ease of development.

**Do:**
- Use layered for simple problems and short time-to-market.
- Watch for sinkhole anti-pattern — delete useless pass-through layers.

**Don't:**
- Don't use layered for systems with complex, changing domains — every change ripples.

*Ref: Head First Software Architecture.md — "Layered Architecture"*

---

### Modular Monolith

**What:** Single deployment unit, but components organized by *business domain* (not technical layer).

**Why:** Domain-aligned organization, team autonomy, easier evolution, path to microservices.

**Keeping modules modular:**
- Encapsulation (clean APIs, hidden internals).
- Separate packages/namespaces.
- **Database separation** — each module should have its own schema or tables.
- **Beware of joins** — cross-module joins create hidden coupling. Use data duplication + eventual consistency instead.

**Superpowers:** Domain-aligned, team autonomy, path to microservices, simpler than distributed.

**Kryptonite:** Requires discipline, database separation is hard, single deployment unit, requires real domain understanding.

**Star ratings:** Moderate agility/testability, high performance (in-process), high ease of development.

**Do:**
- Treat the modular monolith as the **default starting point** for new systems — simpler than microservices, more evolvable than layered.
- Separate databases by schema/table from day one.
- Use events or APIs for cross-module data sharing, not joins.

**Don't:**
- Don't let shared databases become the hidden coupling point.
- Don't skip the domain analysis — poor boundaries are expensive later.

*Ref: Head First Software Architecture.md — "Modular Monoliths"*

---

### Microkernel Architecture

**Two parts:** Core system (stable, with extension points) + plug-in components (independent, implement contracts).

**Spectrum of "microkern-ality":**
- **Encapsulated:** core + plug-ins deployed together (simpler, less flexible).
- **Distributed:** plug-ins deployed separately, communicate via APIs/messaging (more flexible, more complex).

**Plugin communication:**
- Point-to-point (core calls specific plug-in)
- Pub/sub (core publishes events; plug-ins respond)
- Registry pattern (central lookup)

**Plugin contracts:** Input contracts, output contracts, behavioral contracts. Version contracts carefully — breaking changes break plug-ins.

**Superpowers:** Customization, extensibility, independent testability, deployment flexibility (in distributed mode).

**Kryptonite:** Plugin management complexity, contract versioning, core can become bottleneck, plugin interdependency creates hidden coupling.

**Star ratings:** Moderate-high agility, high testability, high performance (encapsulated), moderate scalability.

**Do:**
- Define contracts explicitly — input, output, behavioral.
- Version contracts carefully with deprecation policies.
- Use registry patterns when many plug-ins coexist.

**Don't:**
- Don't let plug-ins depend on each other — that breaks the architectural quantum.
- Don't let the core become the bottleneck for plug-in scaling.

*Ref: Head First Software Architecture.md — "Microkernel Architecture"*

---

### Microservices

**Definition:** Small, independently deployable units that own their own domain and data.

**Data isolation is foundational:** each service owns its own database.

**Granularity — two opposing forces:**

**Granularity disintegrators (make smaller):**

| Force | Reason |
|-------|--------|
| Volatility | Different rates of change → separate services |
| Scalability | Different scaling needs → separate services |
| Fault tolerance | Critical functionality isolated from less-critical |
| Security | Different security needs → separate services |

**Granularity integrators (make bigger):**

| Force | Reason |
|-------|--------|
| Workflow | Tightly coupled workflows → simpler in one service |
| Shared data | Services that share data → combine |
| Transactionality | ACID-required operations → one service |

**Rule:** Balance the forces. Start slightly larger and split when the need becomes clear.

**Sharing functionality — three approaches:**

| Approach | Pros | Cons |
|----------|------|------|
| Shared service | Centralized | Network overhead + dependency |
| Shared library | No network | Versioning challenges across services |
| Duplication | No coupling | Risk of inconsistency |

**General rule:** Use shared libraries for stable, well-defined functionality; accept duplication when services have different needs.

**Workflow management:**

| Pattern | Pros | Cons |
|---------|------|------|
| Orchestration (central coordinator) | Clear control, easier error handling | Tight coupling, single point of failure |
| Choreography (event-driven) | Loose coupling, no SPOF | Harder to reason about, complex error handling |

**Superpowers:** Independent scalability, fault isolation, independent deployment, technology diversity.

**Kryptonite:** Complexity, network latency, data consistency challenges, operational overhead.

**Star ratings:** High agility/scalability, moderate performance (network overhead), high testability.

**Do:**
- Start with **larger** services, split only when forces demand it.
- Apply disintegrators/integrators explicitly to each split decision.
- Choose choreography by default; reserve orchestration for explicit control needs.

**Don't:**
- Don't decompose by entity — use bounded context.
- Don't reach for microservices for small/simple problems.

*Ref: Head First Software Architecture.md — "Microservices Architecture"*

---

### Event-Driven Architecture (EDA)

**What:** Asynchronous event-driven processing for high throughput and scalability.

**Key concepts:**

| Concept | Definition |
|---------|-----------|
| Event | Notification that something happened; immutable; producer-decoupled |
| Initiating event | Triggered by external actor (user, sensor, time) |
| Derived event | Generated by system as result of processing other events |
| Message | Directed communication requesting specific action |

**Events vs. messages:** Events enable true decoupling; messages are more coupled but provide more control.

**Asynchronous communication patterns:**
- **Fire-and-forget** — producer sends and continues without waiting.
- **Pub/sub** — producers publish to topics; consumers subscribe.

**Sync vs. async decision:**

| Async wins for | Sync wins for |
|----------------|---------------|
| High throughput | Real-time response requirements |
| Decoupled processing | Complex request-response |
| Parallel execution | Caller needs immediate answer |
| Variable load | |

**Database topologies for EDA:**

| Topology | Coupling | Best for |
|----------|----------|----------|
| Monolithic database | Tight | Simple systems; complex joins OK |
| Domain-partitioned databases | Moderate | Balance between simplicity and isolation |
| Database-per-service | Maximum isolation | Maximum independence; eventual consistency |

**EDA vs. Microservices — 4 key differences:**

| # | Difference | EDA | Microservices |
|---|------------|-----|---------------|
| 1 | Communication style | Asynchronous | Synchronous (REST) |
| 2 | Service granularity | Variable (can be coarse) | Fine-grained (single-purpose) |
| 3 | Data granularity | Flexible (any topology) | Requires DB-per-service |
| 4 | Coupling | Loose (event-based) | Tighter (request-response) |

**The common modern hybrid:** Event-driven microservices — independently deployable services communicating via events.

**Superpowers:** High performance, scalability, loose coupling, extensibility (new consumers without changing producers).

**Kryptonite:** Complexity, error handling (async failures harder to detect), eventual consistency is hard to reason about, workflow management requires sagas.

**Star ratings:** High agility/scalability/performance, moderate testability, high ease of deployment.

**Do:**
- Default to choreography; introduce orchestration only when explicit control is needed.
- Design for eventual consistency from the start.
- Use correlation IDs for traceability across async hops.
- Apply database topology by domain — you don't need DB-per-service for EDA.

**Don't:**
- Don't try to maintain strong consistency in async systems — embrace eventual consistency + compensating actions.
- Don't introduce async where sync is required (real-time responses).

*Ref: Head First Software Architecture.md — "Event-Driven Architecture"*

---

### Architecture Style Selection — Decision Process

**Five-step process:**
1. **Identify architectural characteristics** — which 3–5 are most critical?
2. **Identify logical components** — workflow or actor/action approach.
3. **Choose architectural style** — match characteristics to style strengths.
4. **Document your decision** — write an ADR.
5. **Diagram your architecture** — visualize the components and relationships.

**Style selection by characteristic priority:**

| Top priority | Best style |
|--------------|-----------|
| Simplicity, fast initial dev | Layered |
| Domain alignment + simplicity | Modular monolith |
| Customization + extensibility | Microkernel |
| Independent scalability + fault isolation | Microservices |
| High throughput + loose coupling | Event-Driven |
| Independent scale + loose coupling | Event-driven microservices |

*Ref: Head First Software Architecture.md — "Do It Yourself — TripEZ / Make the Grade"*

---

### Architecture Style Comparison Matrix

**Six styles side-by-side:**

| Characteristic | Layered | Modular Monolith | Microkernel | Microservices | EDA | EDA-Microservices |
|---------------|---------|------------------|-------------|---------------|-----|-------------------|
| Overall agility | Low | Moderate | Mod–High | High | High | High |
| Ease of deployment | Low | Moderate | High | High | High | High |
| Testability | Low | Moderate | High | High | Moderate | High |
| Performance | Low | High | High | Moderate | High | Moderate–High |
| Scalability | Low | Low–Mod | Moderate | High | High | High |
| Ease of development | High | High | Moderate | Moderate | Moderate | Moderate |

**Do:**
- Use this matrix for fast trade-off analysis.
- Re-evaluate styles when characteristics change — don't lock in for years.

**Don't:**
- Don't pick a style whose kryptonite matches your top characteristics.

*Ref: Head First Software Architecture.md — "Appendix: Architecture Styles Quick Reference"*

---

## Anti-Patterns & Common Mistakes

- **The Entity Trap:** creating `OrderManager`, `CustomerService` components. → *fix:* name by cohesive responsibility, not by entity.
- **Sinkhole layers:** request passes through layers without adding value. → *fix:* delete useless layers.
- **Best-practice thinking:** assuming universal solutions exist. → *fix:* analyze trade-offs in context; document the why.
- **Shared databases across modules/services:** creates hidden coupling; collapses architectural quanta. → *fix:* data duplication + eventual consistency, or DB-per-service.
- **Cross-module joins:** hide schema coupling behind query syntax. → *fix:* use events/APIs for cross-module data.
- **Microservices-by-default:** paying distributed-systems tax for small/simple problems. → *fix:* start with modular monolith; evolve when forces demand.
- **Choreography + saga errors:** hard to reason about, hard to debug. → *fix:* correlation IDs, runbooks, explicit compensation.
- **Law of Demeter violation:** `a.getB().getC().doSomething()`. → *fix:* tell, don't ask — add a method that does the work.
- **Coupling without measurement:** claiming "loosely coupled" without computing Ca, Ce, abstractness, instability. → *fix:* measure; plot distance from main sequence.
- **Premature microservices:** "we might need to scale independently someday." → *fix:* build modular monolith; extract services when forces demand.

---

## Decision Heuristics / Checklists

- **Architecture style selection:** characteristics → style, not the reverse.
- **Limit characteristics to 3–5** top-priority per system. More → over-engineering.
- **Trade-off analysis in 5 steps:** identify options → evaluate → context → decide → document.
- **ADR must-have sections:** Title (noun phrase), Status, Context, Decision, Consequences.
- **Component name test:** can you describe its task in one sentence? Avoid `*Manager`, `*Supervisor`, `*Handler`.
- **Decomposition approach choice:**
  - Clear workflows → workflow approach.
  - Clear actors with distinct actions → actor/action approach.
  - Either way, avoid entity decomposition.
- **Coupling heuristic:** high cohesion within, loose coupling between.
- **Layered vs. modular monolith:** layered = simple/time-critical; modular monolith = domain-aligned, evolvable, simpler than microservices.
- **Microservices granularity rule:** start larger; apply disintegrators/integrators explicitly; only split when forces demand.
- **Workflow coordination rule:** choreography by default; orchestration when explicit control needed.
- **Async vs. sync:** async for high throughput / decoupled / parallel; sync for real-time response / request-response.
- **EDA DB topology:** monolithic for simple, domain-partitioned for balance, DB-per-service for max isolation.
- **Cross-module data sharing:** events or APIs, never joins, never shared tables.
- **Microkernel contract versioning:** explicit input/output/behavioral contracts with deprecation policy.
- **Distance from main sequence:** plot abstractness vs. instability for each module; aim for balanced.
- **Trade-off documentation:** always document the *why* (Law #2) so context changes can adapt the decision.

---

## Key Takeaways

1. **Architecture has four dimensions** — characteristics, decisions, components, style. All four must align.
2. **Everything is a trade-off.** There are no best practices, only contextually appropriate decisions.
3. **Understanding *why* matters more than knowing *how*.** Context changes; understanding survives.
4. **Limit characteristics to 3–5** per system — more leads to over-engineering.
5. **Logical before physical.** Decide components before deployment topology.
6. **Avoid the entity trap.** Components organize around cohesive responsibilities, not entities.
7. **High cohesion within, loose coupling between.** Use coupling metrics (Ca, Ce, abstractness, instability) to verify.
8. **Style choice is contextual.** Match the style to your characteristics, not the other way around.
9. **The modular monolith is the best default starting point** — domain-aligned, simple, evolvable.
10. **Microservices need data isolation** and explicit granularity analysis (disintegrators vs. integrators).
11. **EDA enables high throughput and loose coupling** — but requires embracing eventual consistency.
12. **ADRs are essential documentation** — capture context, decision, rationale, consequences in version control.
13. **Choreography by default**; reserve orchestration for explicit control needs.
14. **No best practices — only better trade-offs.**

---

## Cross-References

- Related: [[../Software_Architecture_Metrics.md]] — coupling metrics, fitness functions, MMI
- Related: [[../Building_Evolutionary_Architectures.md]] — connascence, architecture quanta, evolvability
- Related: [[../Software_Architect_Elevator.md]] — communicating trade-offs up the org
- Topic index: [[../INDEX.md]]
