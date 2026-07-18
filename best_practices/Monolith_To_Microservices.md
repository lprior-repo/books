# Monolith to Microservices
**Author:** Sam Newman
**Topic tags:** `#architecture` `#api`
**Language focus:** Language-agnostic (uses Music Corp, a fictional multi-national music retailer, as the running case study)
**Sources:** `markdown_output/Monolith To Microservices/Monolith To Microservices.md` · `summaries/Monolith_To_Microservices.md`

## TL;DR
Sam Newman's *Monolith to Microservices* is the second book in his microservices
canon — focused specifically on *migration*, not adoption. Newman's
operating principle is **independent deployability**: a change to one service
should deploy without requiring changes elsewhere. Everything else
(cohesion/coupling, DDD, event storming, modular monolith, strangler fig,
change data capture, sagas, shared-database coping patterns) is a tool in
service of that principle. Migration is *incremental* — chip away like a
block of marble; big-bang rewrites are dangerous. The database is the
hardest part: most patterns in the book exist to handle data ownership,
referential integrity, transactions, and reporting once the schema is
shared. Sagas replace two-phase commit. The SnapCI war story (decompose
→ merge back → re-decompose with better understanding) is the canonical
counter-example to "microservices first."

---

## Best Practices by Topic

### Microservices Are a Means, Not the Goal

**Principle:** Start every migration with the *why*. "Microservices are not
the goal."

**Do:**
- Ask the three questions before any architectural work:
  1. What are you hoping to achieve?
  2. Have you considered alternatives to using microservices?
  3. How will you know if the transition is working?
  *Ref: Monolith To Microservices.md — "Understanding the Goal" (`page-62-0`).*
- Use the **slider model**: rank competing priorities (team autonomy vs.
  scale vs. technology flexibility) and identify the *core driver*,
  separating it from secondary benefits.
  *Ref: Monolith To Microservices.md — "Trade-Offs" (`page-71-0`).*
- Identify the *real* bottleneck via **path-to-production mapping** before
  assuming the deployment pipeline is the bottleneck.
  *Ref: Monolith To Microservices.md — "Reduce Time to Market" (`page-64-0`).*
- Make **reversible decisions quickly**; invest deliberation in
  *irreversible* ones (Bezos's Type 1 vs Type 2).
  *Ref: Monolith To Microservices.md — "Cost of Change" (`page-77-0`).*

**Don't:**
- Don't use microservices because "everyone else is doing it" — *the
  worst reason*.
  *Ref: Monolith To Microservices.md — "When Microservices Are a Bad Idea" (`page-72-0`).*
- Don't decompose at startup — focus on product-market fit first;
  decomposition is easier on brownfield systems.
  *Ref: Monolith To Microservices.md — "Startups" (`page-73-0`).*
- Don't decompose customer-installed software — you can't ask your
  customers to run a distributed system.
  *Ref: Monolith To Microservices.md — "Customer-installed software" (`page-73-0`).*

---

### Independent Deployability Is the Defining Characteristic

**Principle:** "If there is only one thing you take out of this book, it should
be this: ensure you embrace the concept of independent deployability."

**Do:**
- Use **strong code ownership**: each service has an owner; external
  changes require pull requests.
  *Ref: Monolith To Microservices.md — "Ownership at Scale" (`page-225-0`).*
- Keep services *loosely coupled* — explicit, well-defined, stable
  contracts.
  *Ref: Monolith To Microservices.md — "Independent Deployability" (`page-17-0`).*
- "Separate *deployment* from *release*" — deploy the new service to
  production *before* switching traffic to it.
  *Ref: Monolith To Microservices.md — "Strangler Fig Application" (`page-95-0`).*
- Use **bounded contexts** (DDD) as the natural service boundary.
  *Ref: Monolith To Microservices.md — "Domain-Driven Design Essentials" (`page-26-0`).*

**Don't:**
- Don't share databases between services — *"in my opinion, it's one of the
  worst things you can do if you're trying to achieve independent
  deployability."*
  *Ref: Monolith To Microservices.md — "Own Their Own Data" (`page-20-0`).*

---

### Understand Your Coupling

**Principle:** Three coupling types each need different solutions. Aim
for **high cohesion, low coupling** ("the code that changes together,
stays together").

**Do:**
- Treat *domain coupling* (Service A genuinely needs data from Service B)
  as expected but minimize it.
  *Ref: Monolith To Microservices.md — "Domain coupling" (`page-39-0`).*
- Reduce *temporal coupling* (both must be up at the same time) via
  caching or async transport.
  *Ref: Monolith To Microservices.md — "Temporal coupling" (`page-37-0`).*
- Eliminate *implementation (pass-through) coupling* (Service A passes
  data to B that it only needs for C) by trimming what flows across
  service boundaries.
  *Ref: Monolith To Microservices.md — "Implementation coupling" (`page-34-0`).*
- Apply *information hiding* (Parnas, 1971): separate the parts of the
  code that change frequently from the ones that are static.
  *Ref: Monolith To Microservices.md — "Information Hiding" (`page-33-0`).*

**Don't:**
- Don't use "outside-in" turned inside-out — *don't* expose your data
  model or internal implementation details as the service contract. Ask
  your consumers what they need, not what your data model happens to be.
  *Ref: Monolith To Microservices.md — "Implementation coupling" (`page-34-0`).*

---

### Consider the Modular Monolith First

**Principle:** Before decomposing, reorganize the monolith along domain
boundaries with separate modules (and ideally separate schemas). For many
organizations this solves the problem without the cost of distributed
systems.

**Do:**
- Refactor the monolith along domain boundaries using **seams** (Feathers):
  places where behavior can change without editing existing code.
  *Ref: Monolith To Microservices.md — "Refactoring the Monolith" (`page-95-0`).*
- Decompose the *database* along module boundaries even within a single
  process — it hedges your bets and makes future microservice extraction
  much easier.
  *Ref: Monolith To Microservices.md — "And the modular monolith" (`page-28-0`).*
- Study **Shopify's** approach: large, successful, deliberately
  *staying* as a modular monolith.
  *Ref: Monolith To Microservices.md — "And the modular monolith" (`page-28-0`).*
- Learn from the **SnapCI** war story: decomposed too early, merged
  back, then re-decomposed a year later with better understanding.
  *Ref: Monolith To Microservices.md — "Unclear domain" (`page-72-0`).*

**Don't:**
- Don't think of the monolith as inherently "legacy" — *monolithic
  architecture is a choice, and a valid one at that.*
  *Ref: Monolith To Microservices.md — "Advantages of Monoliths" (`page-30-0`).*

---

### Migration Patterns (Strangler Fig + Friends)

**Principle:** Migrate incrementally. The right pattern depends on whether
the functionality is at the *edge* (interceptable HTTP) or *internal*
(deep in the monolith).

**Do — pick the right pattern for the right job:**

- **Strangler Fig Application** — for edge functionality with clear
  HTTP ingress. Three steps:
  1. Identify functionality to migrate
  2. Implement in a new microservice
  3. Reroute calls from monolith to new service
  *Ref: Monolith To Microservices.md — "Strangler Fig Application" (`page-95-0`).*
- Insert a **reverse proxy** between clients and the monolith; redirect
  specific routes one at a time. Verify latency impact *before* moving
  anything.
  *Ref: Monolith To Microservices.md — "HTTP Reverse Proxy example" (`page-95-0`).*
- **UI Composition** — pages assembled from fragments served by different
  services (The Guardian pattern). Lets you migrate the frontend
  alongside the backend.
  *Ref: Monolith To Microservices.md — "UI Composition" (`page-101-0`).*
- **Branch by Abstraction** — for *internal* functionality:
  1. Create an abstraction layer
  2. Route all existing consumers through the abstraction
  3. Implement the new microservice behind the abstraction
  4. Switch over traffic
  5. Remove the old implementation and the abstraction
  *Ref: Monolith To Microservices.md — "Branch by Abstraction" (`page-101-0`).*
- **Parallel Run** — run both old and new implementations side-by-side,
  compare results without switching live traffic. *Critical for
  high-risk migrations (financial calculations).*
  *Ref: Monolith To Microservices.md — "Parallel Run" (`page-101-0`).*
- Combine with the **Scientist** pattern (from GitHub) for automated
  result comparison.
  *Ref: Monolith To Microservices.md — "Parallel Run" (`page-101-0`).*
- **Decorating Collaborator** — attach new functionality (e.g., a
  loyalty program) to an existing system by intercepting calls; the
  monolith doesn't need to know about the new collaborator.
  *Ref: Monolith To Microservices.md — "Decorating Collaborator" (`page-101-0`).*
- **Change Data Capture** — when you cannot change the monolith to emit
  events, watch its database transaction log. Tools like **Debezium**
  trigger new services from row changes.
  *Ref: Monolith To Microservices.md — "Change Data Capture" (`page-101-0`).*
- **Dark launching + canary releasing** — gradually expose new
  functionality to a subset of users.
  *Ref: Monolith To Microservices.md — "Dark launching and canary releasing" (`page-101-0`).*
- **Anti-corruption layer** (DDD) — translate between the monolith's
  data model and the new service's cleaner model.
  *Ref: Monolith To Microservices.md — "Changing Protocols" (`page-101-0`).*

**Don't:**
- Don't do the **big-bang rewrite** — *"it's production that counts"*.
  Each step should land in production and stay there.
  *Ref: Monolith To Microservices.md — "It's production that counts" (`page-77-0`).*

---

### Decomposing the Database (The Hardest Part)

**Principle:** Most patterns in the book exist to handle data ownership
once the schema is shared. The shared database is the most common
anti-pattern.

**Do — Coping patterns (when you can't yet fully separate):**

- **Database View** — create views that project a limited subset of the
  underlying schema. Read-only, information-hiding. A bank's 20+
  external apps were coupled to its schema; views gave them a stable
  contract.
  *Ref: Monolith To Microservices.md — "Database View" (`page-150-0`).*
- **Database Wrapping Service** — place a thin service wrapper around
  the database to stop the problem from getting worse while you plan
  proper decomposition.
  *Ref: Monolith To Microservices.md — "Database Wrapping Service" (`page-150-0`).*
- **Database-as-a-Service Interface** — expose a dedicated read-only
  database kept in sync via CDC. Internal schema can evolve
  independently; can use different database technologies.
  *Ref: Monolith To Microservices.md — "Database-as-a-Service Interface" (`page-150-0`).*
- **Aggregate Exposing Monolith** — the monolith still owns the
  aggregate and its state transitions; the new service reads it
  through a monolith API endpoint.
  *Ref: Monolith To Microservices.md — "Aggregate Exposing Monolith" (`page-150-0`).*
- **Data Synchronization via Tracer Write** — gradually migrate data
  ownership:
  1. New service starts writing data
  2. Data synced to the old source
  3. Consumers gradually switch to reading from the new service
  4. Once all migrated, stop synchronizing
  *Ref: Monolith To Microservices.md — "Data Synchronization via Tracer Write" (`page-150-0`).*

**Do — Splitting apart the database:**

- **Repository per Bounded Context** — organize DB access code along
  domain boundaries to understand which tables are used by which
  contexts.
  *Ref: Monolith To Microservices.md — "Repository per Bounded Context" (`page-160-0`).*
- **Database per Bounded Context** — give each context its own schema
  even within a single monolith. Keeps options open for future
  extraction.
  *Ref: Monolith To Microservices.md — "Database per Bounded Context" (`page-160-0`).*
- **Monolith as Data Access Layer** — expose an API on the monolith;
  the new service avoids direct DB coupling while DB decomposition
  is deferred.
  *Ref: Monolith To Microservices.md — "Monolith as Data Access Layer" (`page-160-0`).*
- **Multischema Storage** — new microservice writes to its own schema;
  reads legacy data from the monolith's schema.
  *Ref: Monolith To Microservices.md — "Multischema Storage" (`page-160-0`).*
- **Split Table** — split a single table spanning multiple bounded
  contexts along ownership lines. For shared columns, ask *which
  domain concept does this column belong to?* (e.g., Customer Status
  → customer management owns it).
  *Ref: Monolith To Microservices.md — "Split Table" (`page-160-0`).*
- **Move Foreign-Key Relationship to Code** — when a join must span
  services, the DB no longer enforces referential integrity. Do the
  join in application code (with caching) — accept increased latency,
  potential staleness, and FK handling in code.
  *Ref: Monolith To Microservices.md — "Move Foreign-Key Relationship to Code" (`page-160-0`).*

**Choose your split order — three approaches:**
1. **Split database first, then code** — spots consistency issues earlier,
   no short-term benefit.
2. **Split code first, then database** — short-term benefit, risk of
   never finishing the DB split.
3. **Split both at once** — biggest step, hardest to assess, generally
   not recommended.
   *Ref: Monolith To Microservices.md — "Splitting Sequences" (`page-160-0`).*

**Don't:**
- Don't share databases — *the most common anti-pattern*. Newman's
  Australian bank story: a stored-procedure-laden entitlements DB that
  *every* new feature kept adding to.
  *Ref: Monolith To Microservices.md — "The Shared Database" (`page-145-0`).*
- Don't expose the entire internal schema as the service contract.
  *Ref: Monolith To Microservices.md — "Database-as-a-Service Interface" (`page-150-0`).*

---

### Replace Distributed Transactions with Sagas

**Principle:** **Avoid two-phase commit.** Sagas accept eventual
consistency; each sub-transaction has its own ACID guarantees, but the
saga as a whole does not.

**Do:**
- Break the long-lived transaction into a sequence of *independent*
  sub-transactions, each handled by a different service.
  *Ref: Monolith To Microservices.md — "Sagas" (`page-175-0`).*
- Implement **backward recovery (rollback)** with *compensating
  transactions* — semantic, not literal, rollback. You can't un-send an
  email, but you can send a "sorry, we made a mistake" one.
  *Ref: Monolith To Microservices.md — "Failure modes" (`page-185-0`).*
- Implement **forward recovery (retry)** when the failed step is
  transient — pick up where you left off.
  *Ref: Monolith To Microservices.md — "Forward recovery (retry)" (`page-185-0`).*
- **Order fulfillment example:** create order → authorize payment →
  reserve stock → package item → award loyalty points → dispatch. If
  packaging fails, compensating transactions reverse payment auth and
  stock reservation. Reorder steps (loyalty *after* dispatch) to
  simplify rollback.
  *Ref: Monolith To Microservices.md — "Order fulfillment example" (`page-185-0`).*
- Pick **orchestrated** vs **choreographed** sagas deliberately:
  - **Orchestrated**: central coordinator knows what to call and when.
    Good visibility; risk of god service. Different services should be
    orchestrators for different flows.
    *Ref: Monolith To Microservices.md — "Orchestrated sagas" (`page-185-0`).*
  - **Choreographed**: services react to events; no central coordinator.
    Looser coupling, but harder to see the whole flow.
    *Ref: Monolith To Microservices.md — "Choreographed sagas" (`page-185-0`).*

**Don't:**
- Don't use two-phase commit — *"I strongly recommend avoiding
  distributed transactions."* Locking, deadlocks, no atomic-commit
  guarantee, too many failure modes.
  *Ref: Monolith To Microservices.md — "Two-Phase Commits" (`page-180-0`).*

---

### Plan the Organizational Journey (Kotter for Microservices)

**Principle:** New technology only succeeds if you take the people with
you. Map Kotter's change-management model onto microservice adoption.

**Do — apply the 8 steps:**
- 1. **Establish urgency** — find teachable moments, especially after
  crises.
- 2. **Create a guiding coalition** — enough people, including non-IT.
- 3. **Develop a vision and strategy** — *what* and *how*.
- 4. **Communicate the change vision** — believable, face-to-face.
- 5. **Empower employees** — remove roadblocks, bring in tools to solve
  real problems.
- 6. **Generate short-term wins** — start with easy extractions.
- 7. **Consolidate gains and produce more change** — don't stop after
  the first success.
- 8. **Anchor new approaches in culture** — share stories; make the
  new way "the way."
  *Ref: Monolith To Microservices.md — "Taking People on the Journey" (`page-75-0`).*

**Do — Reorganize teams:**
- Move from siloed (technical specialty) to **cross-functional**
  (business domain) teams.
  *Ref: Monolith To Microservices.md — "Reorganizing Teams" (`page-80-0`).*
- Use **skills matrices** (private per individual, aggregated per team)
  to identify training needs.
  *Ref: Monolith To Microservices.md — "Reorganizing Teams" (`page-80-0`).*

---

### Prioritize Extractions (Value vs Difficulty Quadrant)

**Principle:** Start with high-value, low-difficulty extractions for quick
wins. Use domain modeling to assess difficulty.

**Do:**
- Plot candidate services on a **value (Y) vs difficulty (X) quadrant**:
  *Ref: Monolith To Microservices.md — "Prioritization quadrant" (`page-80-0`).*
- Use **domain modeling** to assess difficulty: bounded contexts with
  many inbound dependencies (Notifications) are harder to extract
  than those with few (Invoicing).
  *Ref: Monolith To Microservices.md — "Where to Start" (`page-80-0`).*

---

### Code Migration: Cut, Copy, or Reimplement

**Principle:** When you can change the monolith, choose how to migrate
its code; the answer depends on how much confidence you have in your
seams.

**Do:**
- **Cut** — move code as-is, including any mess. Lowest risk; preserves
  existing behavior.
  *Ref: Monolith To Microservices.md — "To Change the Monolith, or Not?" (`page-91-0`).*
- **Copy** — duplicate code to the new service; leave original in place
  for rollback. Higher resilience, more code to maintain temporarily.
  *Ref: Monolith To Microservices.md — "To Change the Monolith, or Not?" (`page-91-0`).*
- **Reimplement** — clean-room implementation. Highest risk; only when
  you must change the language/framework *and* understand the domain
  well.
  *Ref: Monolith To Microservices.md — "To Change the Monolith, or Not?" (`page-91-0`).*

---

### Growing Pains Are Predictable (Plan Ahead)

**Principle:** New architectural challenges emerge as service count
grows. Plan for them.

**Do — by service count:**
- **2–10 services:** focus on *breaking changes* and *reporting*.
  *Ref: Monolith To Microservices.md — "Growing Pains" (`page-220-0`).*
- **10–50 services:** *ownership at scale*, *developer experience*,
  *running too many things*.
- **50+ services:** *global vs local optimization*, *orphaned services*.
- **Cross-cutting (at any scale):** *robustness*, *monitoring &
  troubleshooting*, *end-to-end testing*.

**Do — concrete tactics:**
- Avoid **breaking changes** by:
  1. Eliminating accidental ones (explicit schemas, no magic
     serialization).
  2. Thinking twice before making intentional ones (prefer additive).
  3. Giving consumers time to migrate (run multiple service
     versions temporarily).
  *Ref: Monolith To Microservices.md — "Breaking Changes" (`page-225-0`).*
- For **reporting** after splitting the DB: dedicated reporting DB
  (CDC / events / batch), data warehouse/lake, or cross-schema views
  (limited by technology).
  *Ref: Monolith To Microservices.md — "Reporting" (`page-230-0`).*
- For **monitoring**: distributed tracing, correlation IDs, centralized
  logging; move beyond uptime to *health* indicators.
  *Ref: Monolith To Microservices.md — "Monitoring and Troubleshooting" (`page-230-0`).*
- For **local dev experience at scale**: mock/stub downstream services,
  remote dev environments, self-service provisioning.
  *Ref: Monolith To Microservices.md — "Local Developer Experience" (`page-230-0`).*
- For **end-to-end testing**: *consumer-driven contract testing* (e.g.,
  Pact), *limit scope of E2E tests*, *test in production* (canary,
  feature flags), *strengthen smaller-scope tests*.
  *Ref: Monolith To Microservices.md — "End-to-End Testing" (`page-235-0`).*
- For **robustness & resiliency**: circuit breakers, bulkheads,
  timeouts, retries. The failure of one service must not cascade.
  *Ref: Monolith To Microservices.md — "Robustness and Resiliency" (`page-240-0`).*
- For **orphaned services**: lifecycle management + regular cleanup.
  *Ref: Monolith To Microservices.md — "Orphaned Services" (`page-245-0`).*

**Don't:**
- Don't fall into **collective code ownership** at scale — leads to
  "distributed monoliths" and "colander architecture". Strong
  ownership aligned with product-oriented teams is the model that
  scales.
  *Ref: Monolith To Microservices.md — "Ownership at Scale" (`page-225-0`).*

---

## Anti-Patterns & Common Mistakes
- **Big-bang rewrite.** *fix:* incremental strangler; "chip away at the
  monolith like a block of marble." *Ref: Monolith To Microservices.md — "Big-bang rewrites" (`page-77-0`).*
- **Decompose too early** (before understanding the domain). *fix:*
  ship the SnapCI lesson — merge back, learn, re-decompose later.
  *Ref: Monolith To Microservices.md — "Unclear domain" (`page-72-0`).*
- **Shared database across services.** *fix:* wrapping service first,
  then views, then schema separation, then physical separation.
  *Ref: Monolith To Microservices.md — "The Shared Database" (`page-145-0`).*
- **Two-phase commit for distributed transactions.** *fix:* sagas with
  compensating transactions. *Ref: Monolith To Microservices.md — "Two-Phase Commits" (`page-180-0`).*
- **Microservices calling microservices directly without going through the
  BFF / API gateway.** *fix:* BFF pattern. *Ref: Monolith To Microservices.md — "Avoid Microservices Calling Each Other Directly" (`page-213-0`).*
- **Adopting new tech just because microservices.** *fix:* "make use of a
  technology stack you are familiar with, and then consider whether
  changing your existing technology may help address those problems as
  you encounter them." *Ref: Monolith To Microservices.md — "Technology" (`page-22-0`).*
- **Coupling the entire service fleet to one release train.** *fix:* "I
  strongly prefer to see it as a transitional step toward proper
  release-on-demand techniques." *Ref: Monolith To Microservices.md — "Deployment coupling" (`page-38-0`).*
- **Treating microservices as a silver bullet.** *fix:* "Microservices buy
  you options. They have a cost, and you have to decide if the cost is
  worth the options you want to take up." *Ref: Monolith To Microservices.md — "What Problems Do They Create?" (`page-21-0`).*

---

## Decision Heuristics / Checklists
- **Should I decompose at all?** Three questions + a clear, testable
  business outcome. If you can't answer "how will I know if it's
  working", don't start.
- **Modular monolith or microservices?** Default to modular monolith
  unless you have a real coordination problem at scale. You can always
  decompose later; merging back is much harder.
- **Which migration pattern?**
  - Edge HTTP functionality → **Strangler Fig + Reverse Proxy**.
  - Internal deep call graph → **Branch by Abstraction**.
  - High-risk calculation → **Parallel Run** + Scientist.
  - New feature grafted on old → **Decorating Collaborator**.
  - DB change without code change → **Change Data Capture**.
  - Migrate schema first vs code first? *ref:* choose deliberately
    based on whether you can ship the code change before completing DB
    split.
- **Distributed transaction?** *Almost always* → Sagas. Avoid 2PC.
- **Where to start?** High-value + low-difficulty quadrant. Bounded
  context with few inbound dependencies (Invoicing) over one with
  many (Notifications).
- **Schema change spans two services?** *Move the join to code* —
  accept latency + staleness + in-app FK handling.
- **When to bring Kotter into play?** Before you write a single ADR —
  any migration over 6 months is a change-management problem first.

---

## Key Takeaways
1. **Microservices are not the goal.** They are a means. Always start
   with "what are we trying to achieve?" and a measurement plan.
2. **Independent deployability is the defining characteristic.** It is
   a discipline, not a capability. If you can't deploy one service
   without deploying others, you don't have microservices — you have a
   distributed monolith.
3. **Migration is incremental.** Big-bang rewrites are dangerous.
   The job isn't done until each small step is in production. Plan
   for the *production* to be where the lessons come from.
4. **The database is the hardest part.** Use the shared-database
   coping patterns (views, wrapping service, DB-as-a-Service interface)
   as stepping stones to logical then physical separation.
5. **Replace distributed transactions with sagas.** Sagas accept
   eventual consistency; use compensating transactions for backward
   recovery. Avoid 2PC.
6. **Organizational change must accompany technical change.** Use
   Kotter's 8 steps, move from siloed to cross-functional teams,
   and invest in skills development.
7. **Prioritize by the value × difficulty quadrant.** Start with
   high-value, low-difficulty extractions (Invoicing, not
   Notifications) for early wins.
8. **Separate deployment from release.** Deploy the new service to
   production *before* switching traffic to it.
9. **Plan for growing pains.** Ownership, breaking changes, reporting,
   monitoring, developer experience, and testing all become harder as
   service count grows.
10. **Reversible decisions should be made quickly.** Reserve
    deliberation for irreversible ones. Most architectural decisions in
    a microservice migration are reversible.
11. **Consider the modular monolith first.** SnapCI decomposed too
    early, merged back, and re-decomposed a year later with better
    understanding. The modular monolith is a valid destination.
12. **Independent deployability is a discipline.** It means
    *information hiding* (Parnas 1971), loose coupling, stable
    contracts, and no shared databases.

---

## Cross-References
- Related: `../Building_Microservices.md` (Newman's first book; the
  foundational principles this book builds on).
- Related: `../Microservices_Up_And_Running.md` (the hands-on, prescriptive
  implementation playbook for what this book describes architecturally).
- Related: `../Enabling_Microservice_Success.md` (the Kotter / change
  management / team-design companion for the migration journey).
- Related: `../Building_Event-driven_Microservices.md` (the runtime
  patterns for the services you extract).
- Related: `../Monolith_To_Microservices.md` (the file you're reading).
- Topic index: `../INDEX.md`
