# Monolith to Microservices: Comprehensive Summary

**Author:** Sam Newman
**Subtitle:** Evolutionary Patterns to Transform Your Monolith

---

## Overview

This book is a companion to Sam Newman's *Building Microservices*, focused specifically on the practical challenge of migrating existing monolithic systems to a microservice architecture. Rather than advocating for microservices as a silver bullet, Newman provides a grounded, incremental approach to decomposition, complete with battle-tested migration patterns, database decomposition strategies, and guidance on organizational change. The book emphasizes that microservices are a means to an end, not the goal itself, and that any migration must be driven by clear business objectives.

---

## Chapter 1: Just Enough Microservices

### What Are Microservices?

Microservices are independently deployable services modeled around a business domain. They communicate via networks and encapsulate their own data storage and retrieval, exposing data through well-defined interfaces. They are a type of service-oriented architecture (SOA), opinionated about service boundaries and independent deployability.

### Independent Deployability

The single most important concept in the book: you should be able to make a change to a microservice, deploy it into production, and not have to deploy anything else. This requires loose coupling, explicit and stable contracts between services, and avoiding shared databases. Independent deployability is a discipline, not just a capability.

### Modeled Around a Business Domain

Newman introduces Music Corp, a fictional company used throughout the book. The traditional three-tier architecture (UI, backend, database) groups code by technical layer, creating low cohesion of business functionality. Changes to a single feature often require coordination across all three tiers and the teams that own them.

By modeling services around business domains instead, each service encapsulates a thin slice of UI, application logic, and data storage. This aligns with Conway's Law -- that system designs mirror organizational communication structures. When teams are organized around business domains rather than technical specialties, the architecture naturally follows.

### Own Their Own Data

Microservices should not share databases. If one service wants data held by another, it should ask via a well-defined interface. This gives the owning service control over what is shared and hidden, enables stable public contracts, and is essential for independent deployability.

### Advantages and Challenges

Microservices offer flexibility, improved team autonomy, reduced time to market, cost-effective scaling, and the ability to embrace new technology. However, they introduce distributed systems challenges: network latency and reliability, increased operational complexity, the need for explicit contracts, and the difficulty of testing distributed systems.

### The Monolith

Monoliths come in several forms: single-process monoliths (most common), distributed monoliths (multiple services but tightly coupled), and third-party/black-box systems. Monoliths have advantages: simpler deployment, easier monitoring, simpler developer workflows, and well-understood patterns. Their challenges include increasing difficulty of change as they grow and difficulty in scaling specific parts independently.

### Coupling and Cohesion

Newman draws heavily on Constantine's concepts: cohesion (how related the parts of a module are) and coupling (how interdependent modules are). We want high cohesion (related functionality grouped together) and low coupling (modules independent). In a monolith, technical cohesion is high but business cohesion is low. Microservices aim for high business cohesion within each service, and low coupling between services.

Three types of coupling:
- **Domain coupling:** Service A needs something from Service B (least problematic, but minimize)
- **Temporal coupling:** Service A and B must both be available at the same time
- **Implementation (pass-through) coupling:** Service A passes data to B that it only needs for C

### Domain-Driven Design Essentials

- **Aggregates:** Units of consistency boundary (e.g., a Customer and its associated data)
- **Bounded contexts:** Represent a cohesive grouping of aggregates; ideal candidates for microservice boundaries
- **Event Storming:** A collaborative exercise (created by Alberto Brandolini) where stakeholders identify domain events, group them into aggregates, then into bounded contexts

---

## Chapter 2: Planning a Migration

### Understanding the Goal

"Microservices are not the goal." You need a clear understanding of what you are trying to achieve that you cannot achieve with your current architecture. Without this, you risk analysis paralysis, cargo cult adoption, and the sunk cost fallacy.

**Three key questions to ask:**
1. What are you hoping to achieve?
2. Have you considered alternatives to using microservices?
3. How will you know if the transition is working?

### Why Might You Choose Microservices?

**Improve Team Autonomy:** Small, autonomous teams owning services can work more effectively. Alternatives include modular monoliths, code ownership models, and self-service provisioning.

**Reduce Time to Market:** Independent deployments allow faster feature delivery. Newman recommends path-to-production mapping to find the real bottleneck -- often not in deployment but in upstream processes.

**Scale Cost-Effectively for Load:** Services can be scaled independently. Alternatives include vertical scaling (bigger machines), horizontal scaling of the monolith (running multiple copies), and technology replacement.

**Improve Robustness:** Failure in one service doesn't bring down the whole system. Alternatives include decoupling modules within the monolith and better fault tolerance.

**Embrace New Technology:** Each service can use different technology stacks. Alternatives include multi-language runtimes (e.g., JVM languages) and modular architectures.

### When Microservices Are a Bad Idea

- **Unclear domain:** Getting boundaries wrong is expensive. The SnapCI team initially decomposed into microservices, found boundaries were wrong, merged back into a monolith, and re-decomposed a year later with better understanding.
- **Startups:** Startups should focus on product-market fit, not architecture. Decomposition is easier on brownfield systems.
- **Customer-installed software:** You cannot expect customers to manage distributed systems.
- **No good reason:** Doing microservices because everyone else is doing it is the worst reason.

### Trade-Offs

Use a slider model to rank competing priorities (e.g., team autonomy vs. scale vs. technology flexibility). Separate the core driver from secondary benefits to avoid scope creep.

### Taking People on the Journey

Newman maps Kotter's eight-step change model to microservice adoption:
1. **Establish urgency:** Find teachable moments, especially after crises
2. **Create a guiding coalition:** Get enough people on board, including non-IT stakeholders
3. **Develop a vision and strategy:** Vision is the "what"; strategy is the "how"
4. **Communicate the change vision:** Make it believable; use face-to-face communication
5. **Empower employees:** Remove roadblocks, bring in tools to solve real problems
6. **Generate short-term wins:** Start with easy extractions that deliver value
7. **Consolidate gains and produce more change:** Don't stop after first successes
8. **Anchor new approaches in culture:** Share stories, make the new way "the way"

### Importance of Incremental Migration

"Chip away at the monolith like a block of marble." Big-bang rewrites are extremely risky. Incremental extraction allows learning, limits the impact of mistakes, and unlocks value progressively.

**It's production that counts:** A microservice extraction is not complete until it is running in production and being actively used. Most lessons are learned only in production.

### Cost of Change

Jeff Bezos distinguishes Type 1 (irreversible) and Type 2 (reversible) decisions. Most microservice decisions are reversible. Newman places decisions on a spectrum from irreversible (changing a public API used by external customers) to reversible (moving code within a codebase). Make reversible decisions quickly; invest more thought in irreversible ones.

### Where to Start

**Domain modeling** identifies bounded contexts as candidate services. Use the domain model to assess extraction difficulty: bounded contexts with many inbound dependencies (like Notifications) are harder to extract than those with few (like Invoicing).

**Prioritization quadrant:** Plot candidate services on two axes -- value of decomposition vs. difficulty of extraction. Start with high-value, low-difficulty items (top right quadrant).

### Reorganizing Teams

Move from siloed teams (by technical specialty) to cross-functional teams (by business domain). Map all delivery activities to current team structure, then plan a future state. Use self-assessment skills matrices (private per individual, aggregated for team) to identify training needs.

---

## Chapter 3: Splitting the Monolith

### To Change the Monolith, or Not?

Having the ability to change the existing monolith gives the most flexibility. When you cannot (vendor software, lost source code), several patterns still work. If you can change it, you have three options for code migration: cut (move code as-is), copy (duplicate code to the new service, leave original in place for rollback), or reimplement (clean-room implementation).

### Refactoring the Monolith

Before extracting services, reorganize the monolith's code along domain boundaries using Michael Feathers' concept of **seams** -- places where behavior can be changed without editing existing code. This can lead to a **modular monolith**: a single deployment unit composed of multiple independent modules. Many teams find this solves their problems without needing full microservice decomposition.

### Migration Patterns

#### Pattern: Strangler Fig Application

Named after a fig that envelops a tree, this pattern involves incrementally migrating functionality from the monolith to new microservices by intercepting and redirecting calls.

**How it works (three steps):**
1. Identify functionality to migrate
2. Implement it in a new microservice
3. Reroute calls from the monolith to the new service

Best suited for functionality with clear, interceptable inbound calls (especially HTTP). Not ideal for deep internal functionality that is called from many places within the monolith.

**HTTP Reverse Proxy example:**
- Step 1: Insert a proxy between clients and monolith (verify latency impact)
- Step 2: Implement new service
- Step 3: Redirect specific routes to the new service
- Step 4: Optionally remove old functionality from monolith

Key insight: separate *deployment* from *release*. Software can be deployed to production without being actively used.

#### Changing Protocols

When the monolith uses non-HTTP protocols, a proxy can still intercept and translate. For message-based systems, duplicate messages to both old and new systems. The concept of an **anti-corruption layer** (from DDD) can translate between the monolith's data model and the new service's cleaner model.

#### Pattern: UI Composition

Rather than a monolithic UI, compose pages from fragments served by different services. The Guardian newspaper used this approach, with the monolith initially serving the page structure while new services provided page fragments. This enables incremental migration of the frontend alongside the backend.

#### Pattern: Branch by Abstraction

For migrating functionality that is used internally by the monolith (not just at the edges):
1. Create an abstraction layer for the functionality to be replaced
2. Route all existing consumers through this abstraction
3. Implement the new microservice as a new implementation behind the abstraction
4. Switch over traffic
5. Remove the old implementation and the abstraction

This avoids feature branches and allows coexistence of old and new implementations.

#### Pattern: Parallel Run

Run both old and new implementations simultaneously, comparing results without switching live traffic. Useful for high-risk migrations (e.g., financial calculations). Combined with the **Scientist** pattern (from GitHub) for automated comparison of results.

**Dark launching and canary releasing** are related techniques for gradually rolling out new functionality to a subset of users.

#### Pattern: Decorating Collaborator

Attach new functionality to an existing system by intercepting calls. When the monolith handles a request, a new collaborator service is also called (e.g., for loyalty program integration). The monolith doesn't need to know about the new functionality.

#### Pattern: Change Data Capture

When you cannot change the monolith to emit events, use CDC to watch for changes in the monolith's database and trigger actions in new services. Tools like Debezium can monitor database transaction logs. Useful for triggering loyalty card issuance when customer records change.

---

## Chapter 4: Decomposing the Database

This is the most technically detailed chapter, addressing the hardest part of microservice migration.

### Pattern: The Shared Database

Multiple services directly accessing the same database is the most common anti-pattern. Problems: no information hiding, unclear ownership of business logic, inconsistent behavior across services, and inability to independently change schemas.

**When it's acceptable:** For read-only static reference data (country codes, postal codes) and for databases explicitly designed as service interfaces.

### Coping Patterns

#### Pattern: Database View

Create views that project a limited subset of the underlying schema to each service. This provides a form of information hiding while keeping data in one place. Views are typically read-only, must be on the same database engine, and changes to the underlying schema may break views.

Newman shares a war story where a bank's database schema became a de facto public API because over 20 external applications had direct database access. They resolved this by creating a dedicated schema with views matching the old structure, giving them room to refactor the underlying schema.

#### Pattern: Database Wrapping Service

Place a thin service wrapper around the database, converting database dependencies into service dependencies. This stops the problem from getting worse while giving time to plan proper decomposition. Example: an Australian bank's entitlements system, where the database was buckling under load from stored procedures, was wrapped in a service to at least stop new functionality from being added to the overloaded database.

#### Pattern: Database-as-a-Service Interface

Expose a dedicated read-only database as a service endpoint. A mapping engine (often using CDC) keeps the exposed database in sync with the internal database. This allows the internal schema to evolve independently and can use different database technologies. It's more sophisticated than views but requires more infrastructure.

### Transferring Ownership

#### Pattern: Aggregate Exposing Monolith

When the new service needs data still owned by the monolith, expose that data through a service endpoint on the monolith. The monolith still owns the aggregate and its state transitions.

#### Pattern: Data Synchronization via Tracer Write

Gradually migrate data ownership by having the new service become a source of truth:
1. New service starts writing data
2. Data is synchronized to the old source
3. Consumers gradually switch to reading from the new service
4. Once all consumers have migrated, stop synchronizing

Three approaches to data synchronization:
- **Write to one source:** All writes go to one source, then sync to the other
- **Write to both sources:** Clients send writes to both (or an intermediary broadcasts)
- **Write to either source:** Two-way sync between systems

The Square orders example shows how a new Orders service was incrementally migrated using application-level dual writes, with the monolith reading from the new service as data was migrated table by table.

### Splitting Apart the Database

#### Physical vs. Logical Separation

Logical separation (separate schemas) enables independent change and information hiding. Physical separation (separate database engines) adds robustness and reduces resource contention. You can have logical separation without physical separation, but not vice versa.

#### Splitting Sequences

Three approaches:
1. **Split database first, then code:** Spot performance and consistency issues earlier, but no short-term benefit
2. **Split code first, then database:** Get short-term benefit from independent deployment, but risk never completing the database separation
3. **Split both at once:** Biggest step, hardest to assess impact, generally not recommended

**Pattern: Repository per Bounded Context** -- Organize database access code along domain boundaries to understand which tables are used by which contexts.

**Pattern: Database per Bounded Context** -- Even within a monolith, give each bounded context its own schema. This keeps options open for future microservice extraction and works well as a "hedge your bets" approach.

**Pattern: Monolith as Data Access Layer** -- Rather than the new service accessing the monolith's database directly, expose an API on the monolith. This avoids direct database coupling while postponing data decomposition.

**Pattern: Multischema Storage** -- New data created by the microservice goes into its own schema, while the service still accesses legacy data from the monolith's database.

### Schema Separation Examples

#### Pattern: Split Table

When a single table spans multiple bounded contexts, split it along ownership lines. Simple when columns are clearly owned by one context. When the same column is updated by multiple contexts (e.g., a Customer Status updated by both customer management and finance), determine ownership by asking which domain concept the column belongs to.

#### Pattern: Move Foreign-Key Relationship to Code

When tables with foreign-key relationships must be split across service boundaries, the database can no longer enforce referential integrity. The join must be done in application code or via service calls. Example: Catalog's Albums table and Finance's Ledger table share a SKU relationship. After splitting, the Finance service must call the Catalog service to look up album information, or maintain a local cache of album data.

**Trade-offs of moving joins to code:**
- Increased latency (network calls vs. in-database joins)
- Inconsistency (data may be stale between services)
- Need to handle the foreign key in application code

### Transactions

#### ACID Transactions

Atomicity, Consistency, Isolation, Durability. When data is split across databases, we lose atomicity at the operation level -- each database handles its own transaction, and we cannot guarantee that changes to both databases succeed or fail together.

#### Two-Phase Commits (2PC)

A voting phase asks all workers if they can make a change; a commit phase tells them to make it. Problems: locks held during the process, potential for deadlocks, cannot guarantee simultaneous commit, and many failure modes. Newman strongly recommends avoiding distributed transactions.

#### Sagas

A saga breaks a long-lived transaction into a sequence of independent transactions, each handled by a different service. Each sub-transaction has its own ACID guarantees, but the saga as a whole does not provide atomicity.

**Failure modes:**
- **Backward recovery (rollback):** Compensating transactions undo previously committed work. These are *semantic rollbacks* -- you cannot truly undo what already happened (e.g., you cannot unsend an email), but you compensate for it.
- **Forward recovery (retry):** Pick up from the point of failure and keep processing.

**Implementation styles:**
- **Orchestrated sagas:** A central coordinator controls the flow, knows what services to call and when. Good visibility and explicit process modeling, but risk centralizing too much logic. Different services should act as orchestrators for different flows to avoid god services.
- **Choreographed sagas:** Services react to events emitted by other services, without central coordination. More loosely coupled, but harder to understand the overall flow and track saga progress.

**Order fulfillment example:** Create order -> Authorize payment -> Reserve stock -> Package item -> Award loyalty points -> Dispatch. If packaging fails, compensating transactions reverse payment authorization and stock reservation. Reordering steps (e.g., awarding loyalty points only after dispatch) can simplify rollback.

---

## Chapter 5: Growing Pains

As your microservice architecture grows, new challenges emerge. Newman maps these roughly to the number of services:

| Scale | Challenges |
|-------|-----------|
| 2-10 services | Breaking changes, Reporting |
| 10-50 services | Ownership at scale, Developer experience, Running too many things |
| 50+ services | Global vs. local optimization, Orphaned services |
| Cross-cutting | Robustness and resiliency, Monitoring and troubleshooting, End-to-end testing |

### Ownership at Scale

Three ownership models:
- **Strong code ownership:** Each service has an owner; external changes require pull requests
- **Weak code ownership:** Services have suggested owners; anyone can change anything
- **Collective code ownership:** No ownership; anyone changes anything

Collective ownership works at small scale (under ~20 developers) but leads to "distributed monoliths" and "colander architecture" at larger scale. Strong code ownership aligned with product-oriented teams is the most common model at scale.

### Breaking Changes

Accidental and intentional contract breakages between services. Solutions:
1. Eliminate accidental breaking changes (explicit schemas, avoid magic serialization)
2. Think twice before making a breaking change (prefer additive changes)
3. Give consumers time to migrate (coexist multiple contract versions in the same service, or run multiple service versions temporarily)

### Reporting

Splitting the database makes cross-service reporting harder. Solutions:
- Dedicated reporting database with data pushed from services (via CDC, events, or batch processes)
- Data warehouse/data lake aggregation
- Views across multiple service schemas (limited by technology)

### Monitoring and Troubleshooting

With many services, "Is everything OK?" becomes a hard question. Solutions include distributed tracing, correlation IDs, centralized logging, and moving from simple uptime monitoring to more sophisticated health indicators.

### Local Developer Experience

Running many services locally becomes impractical. Solutions:
- Mock/stub downstream services for local development
- Remote development environments
- Self-service environment provisioning

### Running Too Many Things

More services means more to deploy, configure, and manage. Solutions include containerization, orchestration platforms (Kubernetes), infrastructure as code, and CI/CD pipelines.

### End-to-End Testing

Testing across multiple services is complex. Solutions:
- Consumer-driven contract testing (e.g., Pact)
- Limit the scope of end-to-end tests
- Focus on testing in production (canary releases, feature flags)
- Make testing at smaller scopes more robust

### Global vs. Local Optimization

Teams optimizing locally can hurt the system globally. Example: Team A's service caches aggressively, causing stale data for Team B. Requires cross-team communication, shared architectural principles, and sometimes platform-level standards.

### Robustness and Resiliency

More services means more failure modes. Circuit breakers, bulkheads, timeouts, and retry logic become essential. The failure of one service should not cascade.

### Orphaned Services

Services that no one owns or maintains. Common when teams reorganize or services outlive their usefulness. Require service lifecycle management and regular cleanup.

---

## Closing Words

Newman emphasizes that this book provides a toolkit, not a prescription. The right approach depends on your specific context. Key principles to carry forward:

1. Start with clear goals
2. Make small, incremental changes
3. Learn from production
4. Be willing to change course
5. Invest in your people and culture as much as in your technology

---

## Key Takeaways

1. **Microservices are not the goal.** They are a means to achieve specific outcomes. Always start with "what are we trying to achieve?"

2. **Independent deployability is the defining characteristic.** If you cannot deploy a service without deploying others, you have not achieved a microservice architecture.

3. **Incremental migration over big-bang rewrites.** Chip away at the monolith. Each small step provides learning and limits risk. The job isn't done until the new service is in production.

4. **Domain-driven design provides the blueprint.** Bounded contexts make natural service boundaries. Use Event Storming and domain modeling to identify them.

5. **The database is the hardest part.** Splitting data requires handling referential integrity, transactions, joins, and reporting. Use coping patterns (views, wrapping services) as stepping stones.

6. **Avoid distributed transactions.** Two-phase commits introduce locking, complexity, and failure modes. Use sagas instead, accepting eventual consistency and implementing compensating transactions for rollback.

7. **Organizational change must accompany technical change.** Use Kotter's model, align teams with service boundaries, invest in skills development, and avoid copying other organizations' structures blindly.

8. **Prioritize using a value-vs-difficulty quadrant.** Start with high-value, low-difficulty extractions for quick wins, then tackle harder but valuable areas.

9. **Separate deployment from release.** Deploy new services to production before switching traffic, enabling validation in the real environment without risk.

10. **Growing pains are predictable.** Plan for challenges with ownership, breaking changes, reporting, monitoring, developer experience, and testing as your service count increases.

11. **Reversible decisions should be made quickly.** Reserve careful deliberation for truly irreversible decisions. Most architectural decisions in a microservice migration are reversible.

12. **Consider the modular monolith.** Before decomposing into microservices, reorganize your monolith along domain boundaries with separate modules and schemas. This may solve your problems without the complexity of distributed systems.
