# Monolith to Microservices — Evolutionary Patterns to Transform Your Monolith
**Author:** Sam Newman (independent consultant; previously @ ThoughtWorks; author of *Building Microservices*, O'Reilly 2015/2021)
**Topic tags:** `#architecture` `#api` `#migration` `#microservices` `#decomposition` `#ddd` `#data` `#sagas` `#team-topology` `#observability` `#resilience`
**Language focus:** Language-agnostic. Music Corp (a fictional multi-national music retailer selling CDs) is the running case study. Stacks seen in examples: Java / JVM, Ruby, Go, Node.js, Python, PHP, Oracle, MySQL, PostgreSQL, MongoDB, Neo4j, Cassandra, DynamoDB, Riak, Kafka, RabbitMQ/JMS, NGINX, Envoy, Istio, Linkerd, Kubernetes, OpenShift, Debezium, SchemaSpy, FlywayDB, Pact, Jaeger, ELK, Humio, Atomist, Vault.
**Sources:** `markdown_output/Monolith To Microservices/Monolith To Microservices.md` (1.26 MB / 4,347 lines / 2019 O'Reilly first edition) · `summaries/Monolith_To_Microservices.md`

## TL;DR
*Monolith to Microservices* is the second book of Newman's microservices canon, focused exclusively on **migration** rather than greenfield adoption. Newman's north star is **independent deployability**: deploy one service without deploying anything else. Everything else — domain-driven design boundaries, modular monolith, the strangler fig, change data capture, the *Aggregate-Exposing Monolith*, the *Tracer Write*, and sagas — is a tool in service of that principle. Migration is *incremental*: chip away like a block of marble; **big-bang rewrites are dangerous**, *"the only thing you're guaranteed of is a big bang"* (Martin Fowler). **The database is the hardest part** — most patterns exist to handle data ownership, referential integrity, transactions, and reporting once a schema is shared. **Distributed monoliths** and **incomplete migrations** are the two most common destination anti-patterns. The SnapCI war story (decompose → merge back into monolith → re-decompose a year later once domain stabilized) is the canonical counter-example to "microservices first." People, process and Kotter-style change management are as central as code. Treat reversible decisions as reversible; reserve deliberation for irreversible ones (Bezos's Type 1 vs. Type 2).

---

## Best Practices by Topic

### 1. Microservices Are a Means, Not the Goal

**Principle:** Start every migration with the *why*. *"Microservices are not the goal. You don't 'win' by having microservices."*

**Do:**
- Ask the three questions before any architectural work:
  1. What are you hoping to achieve?
  2. Have you considered alternatives to using microservices?
  3. How will you know if the transition is working?
  *Ref: Monolith To Microservices.md — "Three Key Questions" (`page-50-0`).*
- Use the **slider model** to rank competing priorities (team autonomy vs. scale vs. technology flexibility vs. robustness) and identify the *core driver*, separating it from secondary benefits.
  *Ref: Monolith To Microservices.md — "Trade-Offs" (`page-60-0`).*
- Identify the *real* bottleneck via **path-to-production mapping** before assuming deployment is the bottleneck — Newman recounts a project where ideas spent 40 weeks waiting for developers and only 6 weeks in actual delivery.
  *Ref: Monolith To Microservices.md — "Reduce Time to Market" (`page-52-0`).*
- Treat decisions on a **reversible ↔ irreversible** spectrum; make reversible decisions quickly, invest deliberation in irreversible ones (Bezos Type 1 vs. Type 2).
  *Ref: Monolith To Microservices.md — "Cost of Change" (`page-69-0`).*
- Re-evaluate goals at every checkpoint: *"If the business has changed direction such that the direction you're going in no longer makes sense, then stop!"*
  *Ref: Monolith To Microservices.md — "Having Regular Checkpoints" (`page-86-0`).*

**Don't:**
- Don't adopt microservices because "everyone else is doing it" — Newman calls this *"the worst reason"*.
  *Ref: Monolith To Microservices.md — "Not Having a Good Reason!" (`page-67-0`).*
- Don't optimise for **reuse** as a primary goal — reuse is a tactic, time-to-market / cost are the goals.
  *Ref: Monolith To Microservices.md — "Reuse?" (`page-56-0`).*
- Don't make a CTO-driven *"in 12 months we will…"* announcement that no one believes — vision must be believable.
  *Ref: Monolith To Microservices.md — "Communicating the Change Vision" (`page-65-0`).*

---

### 2. Independent Deployability Is the Defining Characteristic

**Principle:** *"If there is only one thing you take out of this book, it should be this: ensure you embrace the concept of independent deployability of your microservices."* — *Ref: Monolith To Microservices.md — "Independent Deployability" (`page-17-0`).*

**Do:**
- Require that **every release** practices the discipline — "it's not just that we *can* do this; it's that this is *actually* how you manage deployments in your system."
  *Ref: Monolith To Microservices.md — "Independent Deployability" (`page-17-0`).*
- Back independent deployability with **explicit, well-defined, stable contracts** between services.
- Avoid the *release train* as an end state — at best a transitional tool. *"If you are trying to transform the way software is developed in your company, … deploy-on-demand is the destination."*
  *Ref: Monolith To Microservices.md — "Deployment coupling" (`page-38-0`).*
- Combine with **strong code ownership** once the dev count grows past ~20 (see §10).

**Don't:**
- Don't share databases across service owners — *"one of the worst things you can do if you're trying to achieve independent deployability."*
  *Ref: Monolith To Microservices.md — "Own Their Own Data" (`page-20-0`).*
- Don't let **delivery contention** silently grow (multiple teams trying to push different changes through the same monolith). Microservices raise the *number* of teams but reduce the *contention rate*.
  *Ref: Monolith To Microservices.md — "Challenges of Monoliths" (`page-30-0`).*

---

### 3. When NOT to Migrate — Anti-Trigger Checklist

**Principle:** *"Microservices are definitely not for everyone."* — Newman names five situations where you should *not* adopt microservices.

**Do (refuse the migration if):**
1. **Unclear domain.** SnapCI (ThoughtWorks) decomposed into microservices, discovered the service boundaries were wrong, merged back into one application, then re-decomposed a year later once they understood the domain. *"Prematurely decomposing a system into microservices can be costly, especially if you are new to the domain."*
   *Ref: Monolith To Microservices.md — "Unclear Domain" (`page-58-0`).*
2. **You're a real startup (not scale-up).** Find product/market fit first. Famous microservice shops (Netflix, Airbnb) decomposed *later* in their evolution.
   *Ref: Monolith To Microservices.md — "Startups" (`page-58-0`).*
3. **Customer-installed software.** *"You cannot expect your customers to have the skills or platforms available to manage microservice architectures. Even if they do, they may not have the same skills or platform that you require."*
   *Ref: Monolith To Microservices.md — "Customer-Installed and Managed Software" (`page-59-0`).*
4. **No good reason.** See §1.
5. **Reuse as primary motivator.** See §1.

**Operational rules:**
- Aim to do strategic separation rather than tactical: keep new code in a modular monolith (see §4) until the domain is stable.
- *"A real startup is likely a small organization with limited funding, which needs to focus all its attention on finding the right fit for its product."*
  *Ref: Monolith To Microservices.md — "Startups" (`page-58-0`).*

---

### 4. The Modular Monolith — Often the Destination

**Principle:** Before reaching for distributed systems, *"an obvious next step that is worth considering is to take your newly identified seams and start to extract them as separate modules, making your monolith a modular monolith."* Multiple teams have stopped decomposing at this stage because the modular monolith solved their problems (Shopify is the named example).

**Do:**
- Define *seams* using Michael Feathers' concept from *Working Effectively with Legacy Code* (Prentice Hall, 2004) — *"a place where you can change the behavior of a program without having to edit the existing behavior."*
  *Ref: Monolith To Microservices.md — "Refactoring the Monolith" (`page-91-0`).*
- Package modules as JARs (Java) / gems (Ruby) — independent code ownership, shared deployment unit.
  *Ref: Monolith To Microservices.md — "A modular monolith?" (`page-92-0`).*
- Push *database-per-bounded-context* even within the monolith to keep future microservice decomposition cheap (see §21).
  *Ref: Monolith To Microservices.md — "Pattern: Database per bounded context" (`page-178-0`).*
- *"I've spoken to more than one team that has started breaking its monolith apart into a modular monolith, with a view to eventually move to a microservice architecture, only to find that the modular monolith solved most of its problems!"*
  *Ref: Monolith To Microservices.md — "A modular monolith?" (`page-92-0`).*

**Don't:**
- Don't accept *"the database [of the modular monolith] tends to lack the decomposition we find in the code level"* — split schemas too, not just code.
  *Ref: Monolith To Microservices.md — "And the modular monolith" (`page-27-0`).*
- Don't pretend the modular monolith is *free* — publishing a Schema per bounded context is more ops work than a single schema.

---

### 5. Coupling & Cohesion — The Diagnostic Lens

**Principle:** *"A structure is stable if cohesion is high, and coupling is low."* — Larry Constantine, *Structured Design* (1979). Microservice architecture = Constantine's modules *that communicate via networks and can be independently deployed*.

**Do:**
- Aim for **cohesion of business functionality**, not technical layer. The thin vertical slice (UI + logic + data per service) is the goal.
  *Ref: Monolith To Microservices.md — "Modeled Around a Business Domain" (`page-18-0`).*
- Use David Parnas's **information hiding** (1971) — *"a module boundary [should] hide those parts of the module implementation that we expect to change more often."*
  *Ref: Monolith To Microservices.md — "Information Hiding" (`page-32-0`).*
- Apply **outside-in** thinking: *"ask the people that will call your service"* — service interfaces are user interfaces.
  *Ref: Monolith To Microservices.md — "Information Hiding" (`page-37-0`).*

**Newman's coupling taxonomy (4 types):**
1. **Domain coupling** — A needs B's data because the real domains interact. *"Can't avoid that level of domain coupling. But by thinking carefully about what and how we share these concepts, we can still aim to reduce the level of coupling."* — `page-39-0`.
2. **Temporal coupling** — A and B must both be online. Mitigate with **caching**, **async messaging**, **timeouts**, **circuit breakers**. — `page-37-0`.
3. **Implementation coupling** — A breaks when B's internals change. Solution: stable public contracts, **shared DB is the canonical bad smell**. — `page-33-0`.
4. **Deployment coupling** — Change to one module forces redeploy of all. Solution: small release scope. *"Smaller releases make for less risk. There is less to go wrong."* — `page-38-0`.

**Don't:**
- Don't share a database to "save" coupling — that's the worst form of implementation coupling.
- Don't assume *size* is the key dimension of microservices — *"the concept of size is highly contextual."* Aim for *"as small an interface as possible"* (Chris Richardson). — `page-24-0`.

---

### 6. Domain-Driven Design as the Source of Service Boundaries

**Principle:** Bounded contexts make natural service boundaries; aggregates make natural splits within services. *"Even if you decide to split a service that models an entire bounded context into smaller services later on, you can still hide this decision from the outside world."*

**Do:**
- Use the **aggregate** as *"a representation of a real domain concept — think of something like an Order, Invoice, Stock Item, etc."* — a state machine with a life cycle, **self-contained, code + state colocated**.
  *Ref: Monolith To Microservices.md — "Aggregate" (`page-44-0`).*
- Aim to expose aggregates through service interfaces — *"outside party requests a state transition in an aggregate, the aggregate can say no."*
  *Ref: Monolith To Microservices.md — "Aggregate" (`page-44-0`).*
- Treat aggregates *inside* a bounded context as the granularity of secondary decomposition — *"When starting out, … I think you should probably target services that encompass entire bounded contexts. As you find your feet, … look to split them around aggregate boundaries."*
  *Ref: Monolith To Microservices.md — "Mapping Aggregates and Bounded Contexts to Microservices" (`page-46-0`).*
- Use **Event Storming** (Alberto Brandolini) — bottom-up: domain events → aggregates → bounded contexts. *"The output of this exercise isn't just the model itself; it is the shared understanding of the model."*
  *Ref: Monolith To Microservices.md — "Event Storming" (`page-72-0`).*

**Don't:**
- Don't try to derive service boundaries from technical layers (MVC packages, ORM tables) — the code is technically cohesive but **business-cohesion poor**.
- Don't get obsessed with getting the domain model right first time — *"You don't have to get it right first time; you just need enough information to make some informed next steps."*
  *Ref: Monolith To Microservices.md — "How Far Do You Have to Go?" (`page-72-0`).*

**Code (Music Corp three-tier → Customer-service example):**
```
# Three-tier (Figure 1-1/1-2) — change crosses UI + Java + DBA teams
UI genre dropdown  ──►  backend OrderService.setGenre()  ──►  DB customer.favorite_genre

# Domain-oriented service (Figure 1-3) — change isolated
Customer Service
  ├─ GET /genres (proxy to Catalog Service)
  ├─ PUT /customers/{id}/favorite-genre  ──►  customer.favorite_genre (own table)
  └─ Recommendation Service reads the favorite-genre column via API
```
*Ref: Monolith To Microservices.md — "Modeled Around a Business Domain" (`page-18-0`).*

---

### 7. Migration Mindset — Incremental, Production-Bound, Reversible

**Principle:** *"If you do a big-bang rewrite, the only thing you're guaranteed of is a big bang."* — Martin Fowler. *"Chip away at these monoliths, extracting a bit at a time."*

**Do:**
- Run an extracted service in **production but not yet in use** (deploy ≠ release). Validate deployment, configs, monitoring in situ before traffic flows.
  *Ref: Monolith To Microservices.md — "How It Works" (strangler fig) (`page-95-0`).*
- Make each step **easily reversible** (toggleable switches, parallel run capability). *"We all make mistakes — so we want techniques that allow us to not only make mistakes as cheaply as possible (hence lots of small steps), but also fix our mistakes quickly."* — `page-96-0`.
- Remember: *"the extraction of a microservice can't be considered complete until it is in production and being actively used."* Most lessons are learned in production. — `page-68-0`.
- Fold migration work *into* feature delivery — *"Rather than breaking your backlog into 'feature' and 'technical' stories, fold all this work together."*
  *Ref: Monolith To Microservices.md — "Incremental rollout" (`page-104-0`).*

**Don't:**
- Don't allow *behavioural changes* in migrated functionality before the migration is complete — it kills roll-back. *"If you allow for changes in functionality you are moving before the migration is complete, then you have to accept that you are making any rollback harder."*
  *Ref: Monolith To Microservices.md — "Changing Behavior While Migrating Functionality" (`page-112-0`).*
- Don't fund a year-long *"Perfect Microservice Platform"* before extracting any service. *"Don't fall into the trap of spending a year defining The Perfect Microservice Platform only to find that it doesn't actually solve the problems you have."* — `page-65-0`.

---

### 8. Prioritisation — Value vs. Difficulty Quadrant

**Principle:** *"It is important, therefore, to separate the core driver behind the shift from any secondary benefits."* Choose your first extractions to maximise learning and momentum, not just to hit the easiest targets.

**Do:**
- Plot candidate services on two axes — **value of decomposition** (x) vs **difficulty of extraction** (y). Start with top-right (Invoicing in Music Corp).
  *Ref: Monolith To Microservices.md — "A Combined Model" (`page-75-0`).*
- Read the domain model for *inbound dependencies* — Notifications had many inbound calls (hard), Invoicing had none (easy).
  *Ref: Monolith To Microservices.md — "Using a Domain Model for Prioritization" (`page-73-0`).*
- Treat the logical model as a guide, not a guarantee — re-examine the actual code to see entanglement.
  *Ref: Monolith To Microservices.md — "Using a Domain Model for Prioritization" (`page-74-0`).*
- Revisit the quadrant after every extraction — *"Some of the things you thought were easy will turn out to be hard. Some of the things you thought would be hard turn out to be easy. This is natural!"* — `page-76-0`.

**Quadrant (mental model):**
```
       Difficulty
          ▲
          │
  Avoid   │  Investigate further
          │  (good candidates AFTER learning)
          │
 ─────────┼────────────────────►
          │                      Value
          │
  Low-pri │  ★ Quick wins
          │  (start here)
```

---

### 9. Change Management — Kotter's 8-Step Process for Microservice Adoption

**Principle:** Use Kotter's organisational-change model (John Kotter, *Leading Change*, 1996) to shepherd the migration through the people side. Tech adoption = organisational adoption.

**Do (apply all eight steps to the migration):**
1. **Establish urgency** — *"Sometimes the right time to bolt the stable door is after the horse has bolted."* Find teachable moments, especially after crises.
   *Ref: Monolith To Microservices.md — "Establishing a Sense of Urgency" (`page-63-0`).*
2. **Guiding coalition** — Pull people outside IT into the coalition. *"Many of the changes you make can potentially have significant impacts on how the software works and behaves."* Trade-offs about caching/staleness must be agreed with non-engineers.
   *Ref: Monolith To Microservices.md — "Creating the Guiding Coalition" (`page-63-0`).*
3. **Vision + strategy** — *"Vision is mostly about the goal — what it is you're aiming for. The strategy is about the how."* Be ready to change strategy, never vision.
   *Ref: Monolith To Microservices.md — "Developing a Vision and Strategy" (`page-64-0`).*
4. **Communicate face-to-face** — *"When it comes to sharing important messages of this sort, face-to-face communication … will be significantly more effective."*
   *Ref: Monolith To Microservices.md — "Communicating the Change Vision" (`page-65-0`).*
5. **Empower employees** — Remove infrastructure blockers (six-month hardware-lead-time orgs need cloud or self-service VM provisioning before microservice adoption will fly).
   *Ref: Monolith To Microservices.md — "Empowering Employees for Broad-Based Action" (`page-65-0`).*
6. **Short-term wins** — Pick easy extractions first (build momentum). Easy ≠ low-value; use the §8 quadrant.
   *Ref: Monolith To Microservices.md — "Generating Short-Term Wins" (`page-66-0`).*
7. **Consolidate, don't rest** — *"Quick wins might be the only wins if you don't continue to push on."* Move into database decomposition when ready.
   *Ref: Monolith To Microservices.md — "Consolidating Gains and Producing More Change" (`page-66-0`).*
8. **Anchor in culture** — Share stories, not just artefacts. New way becomes *"the way."*
   *Ref: Monolith To Microservices.md — "Anchoring New Approaches in the Culture" (`page-67-0`).*

**Don't:**
- Don't skip Kotter steps even for a "small team" adoption — *"even in these smaller-scoped settings, though, I've found this model to be useful, especially the earlier steps."*
  *Ref: Monolith To Microservices.md — "Changing Organizations" (`page-62-0`).*
- Don't treat *"DevOps"* as *"NoOps"* — DevOps is a cultural break-down of silos, not developer-doing-ops.
  *Ref: Monolith To Microservices.md — "DevOps Doesn't Mean NoOps!" (`page-79-0`).*

---

### 10. Team Topology — From Siloed to Cross-Functional

**Principle:** Service ownership must align with team boundaries. Conway's law says the *system* will mirror the *organisation*; choose an organisation whose shape you want the system to take.

**Do:**
- Move from **siloed by technical specialty** (Java team, DBA team, test team) to **cross-functional by business domain** (Customer team owns UI + backend + DB for Customer).
  *Ref: Monolith To Microservices.md — "Shifting Structures" (`page-77-0`).*
- Build the *as-is* state explicitly — list every delivery activity, attribute it to a team. Surface hidden silos.
  *Ref: Monolith To Microservices.md — "Making a Change" (`page-80-0`).*
- Use **private self-assessment skills matrices** aggregated into a team chart to spot training needs (e.g. The Guardian story — Oracle / Kotlin upskilling).
  *Ref: Monolith To Microservices.md — "Changing Skills" (`page-83-0`).*
- Aim for **gradual empowerment** — *"Having them owning their own test deployments is a good first step."* Ownership grows incrementally; don't mandate 24/7 dev on-call for a team new to ops.
  *Ref: Monolith To Microservices.md — "Making a Change" (`page-82-0`).*

**Don't:**
- Don't copy the **Spotify model** uncritically — *"Turns out not even Spotify uses the Spotify model."* Copy the questions, not the answers (Jessica Kerr).
  *Ref: Monolith To Microservices.md — "It's Not One Size Fits All" (`page-78-0`).*
- Don't conflate *autonomy* with *isolation* — robust autonomy requires shared principles for cross-cutting concerns (see §28).
- Don't force developers into 24/7 on-call before they've been coached through it. *"You're more likely to alienate your staff and lose a lot of people."*
  *Ref: Monolith To Microservices.md — "It's Not One Size Fits All" (`page-78-0`).*

---

### 11. The Strangler Fig Application — the Workhorse Pattern

**Principle:** Named by Martin Fowler after the fig that envelops a tree. *"The idea is that the old and the new can coexist, giving the new system time to grow and potentially entirely replace the old system."*

**Do:**
- Three-step skeleton — *"identify parts of the existing system that you wish to migrate … implement this functionality in your new microservice … reroute calls from the monolith over to your shiny new microservice."*
  *Ref: Monolith To Microservices.md — "Pattern: Strangler Fig Application" (`page-94-0`).*
- **Insert the proxy first** (HTTP reverse proxy such as NGINX) and measure latency impact before any redirect.
  *Ref: Monolith To Microservices.md — "Step 1: Insert proxy" (`page-99-0`).*
- Implement the new service returning `501 Not Implemented` initially — exercise deploy/monitoring pipeline without customers seeing it.
  *Ref: Monolith To Microservices.md — "Step 2: Migrate functionality" (`page-100-0`).*
- Use **feature toggles** on the proxy / service for instant switch-back. Most proxies make this a config change. *"If this fails for whatever reason, then you can switch the redirection back … a very quick and easy process."* — `page-101-0`.
- Keep the pipe dumb — *"Keep the pipes dumb, the endpoints smart."* Avoid layering transformation logic into the shared proxy.
  *Ref: Monolith To Microservices.md — "Changing Protocols" (`page-106-0`).*

**Use when:** *"functionality with clear, interceptable inbound calls (especially HTTP)"* — call is at the **perimeter** of the monolith.

**Don't:**
- Don't strangler-extract deeply nested functionality with many internal callers — use **Branch by Abstraction** instead (see §13).
- Don't build your own proxy from scratch — *"I've written a couple of network proxies by hand before … in both situations the proxies were incredibly inefficient, adding significant lag."*
  *Ref: Monolith To Microservices.md — "Proxy Options" (`page-102-0`).*

**Code/Diagram (HTTP reverse proxy — the canonical sequence):**
```
Step 1            Step 2                 Step 3
 ┌──────┐         ┌──────┐                ┌──────┐
 │Proxy │ ──pass──► Proxy │ ──proxy-some──► Proxy │
 └──┬───┘         └──┬─┬──┘                └──┬──┬─┘
    │               │ │                      │  │
    ▼               │ ▼                      │  ▼
 ┌─────────┐        │ ┌─────────┐            │ ┌─────────┐
 │Monolith │        │ │Monolith │ (call..)  │ │Monolith │ (rest)
 └─────────┘        │ └─────────┘            │ └─────────┘
                    │                        │
                    ▼                        ▼
                  ┌────────┐              ┌────────┐
                  │New svc │ (deployed,  │New svc │
                  │ 501    │  not used)  │ LIVE   │
                  └────────┘              └────────┘
```
*Ref: Monolith To Microservices.md — "Pattern: Strangler Fig Application" (`page-94-0`).*

**Other strangler examples:**
- **FTP interception (Homegate)** — monitor FTP server log, route new uploads via an adapter to the new REST listing service. Both upload paths run in parallel (see §14).
  *Ref: Monolith To Microservices.md — "Example: FTP" (`page-108-0`).*
- **Message interception** — content-based router (split queue), or selective-consumption (same queue, each consumer filters).
  *Ref: Monolith To Microservices.md — "Example: Message Interception" (`page-109-0`).*
- **Service mesh (Square)** — Envoy per-instance proxy; per-service config; avoid central smart pipe.
  *Ref: Monolith To Microservices.md — "And service meshes" (`page-108-0`).*
- **Protocol translation inside the service** — when migrating SOAP→gRPC, support both on the same service endpoint rather than putting logic in shared middleware.
  *Ref: Monolith To Microservices.md — "Changing Protocols" (`page-106-0`).*

---

### 12. UI Composition — Migrating the Front-End Alongside

**Principle:** Leaving the UI as a single monolithic layer sabotages backend decomposition — *"If we want an architecture that makes it easier for us to more rapidly deploy new features, then leaving the UI as a monolithic blob can be a big mistake."* Decompose page-by-page (vertical) or widget-by-widget (horizontal).

**Do:**
- **Page Composition** (The Guardian, REA Group) — migrate a *vertical* (Travel, News, Culture) at a time. *"Visitors to the website during this transition time would have been presented with a different look and feel."*
  *Ref: Monolith To Microservices.md — "Example: Page Composition" (`page-113-0`).*
- **Widget Composition** with Edge-Side Includes (ESI / Apache originally; CDN-served Fastly later at The Guardian). Inject a top-10 widget into old travel pages from the new CMS.
  *Ref: Monolith To Microservices.md — "Example: Widget Composition" (`page-114-0`).*
- Use **browser-composition** for SPA UIs — independent widget fails gracefully without breaking the whole page.
  *Ref: Monolith To Microservices.md — "Example: Widget Composition" (`page-115-0`).*
- For mobile, **declare layout server-side** (Spotify) so changes don't need App-Store releases.
  *Ref: Monolith To Microservices.md — "And mobile applications" (`page-117-0`).*
- Use **service-aligned UI modules** (Orbitz) — Content Orchestration delegates one module at a time to a downstream service.
  *Ref: Monolith To Microservices.md — "Example: Widget Composition" (`page-116-0`).*
- Treat **Micro Frontends** as a viable SPA decomposition strategy (Vue / React / Angular coexisting in one page).
  *Ref: Monolith To Microservices.md — "Example: Micro Frontends" (`page-118-0`).*

**Don't:**
- Don't bind a UI migration to a vendor app store release cycle — use server-side configuration instead.
- Don't insist on widget decomposition when the UI doesn't decompose cleanly — vertical page-based migration may be the right level of cut.

---

### 13. Branch by Abstraction — for Deeply Nested Functionality

**Principle:** When the functionality is *not* at the perimeter (it sits deep inside the monolith, called from many places), use *branch by abstraction* instead of long-lived source branches. Five steps in one trunk-based repo.

**Do (the five steps):**
1. **Create an abstraction** — interface / `Extract Interface` refactoring / new function for the seam.
2. **Route existing callers through the abstraction** — small mechanical commits.
3. **Create a new implementation** — the new one delegates to the microservice (or is the client). Initially returns `Not Implemented`; deploy but don't switch.
4. **Switch** via feature flag / config — keep both impls live long enough to verify equivalence.
5. **Clean up** — remove the old implementation, then optionally remove the abstraction.
   *Ref: Monolith To Microservices.md — "Pattern: Branch by Abstraction" (`page-119-0`).*

**Validate by example:** *"Jez Humble details the use of the branch by abstraction pattern to migrate the database persistence layer used in the continuous delivery application GoCD (at the time called Cruise). The switch from using iBatis to Hibernate lasted several months — during which the application was still being shipped to clients on a twice weekly basis."*
  *Ref: Monolith To Microservices.md — "Step 3: Create new implementation" (`page-122-0`).*

**Variation — Verify Branch by Abstraction (Steve Smith):** Auto-switch back to the old implementation if the new one fails on a given request. Adds complexity + data-consistency considerations; only worth it when stateful side-effects matter.
  *Ref: Monolith To Microservices.md — "As a Fallback Mechanism" (`page-126-0`).*

**Don't:**
- Don't keep long-lived source branches instead — *"I am not a fan of long-lived branches, and I'm not alone."*
  *Ref: Monolith To Microservices.md — "Pattern: Branch by Abstraction" (`page-119-0`).*
- Don't leave feature-toggle infrastructure lying around after switch is complete — *"One of the real problems associated with the use of feature flags is leaving old ones lying around — don't do that!"* — `page-125-0`.

---

### 14. Parallel Run, Dark Launching & Canary Release — Progressive Delivery

**Principle:** *"A parallel run … can be just as useful within a single system, when comparing two implementations of the same functionality."* Part of **progressive delivery** (umbrella term coined by James Governor).

**Do:**
- **Parallel Run** — call *both* old and new implementations; compare outputs without switching live traffic. Used for credit-derivative pricing (Sam's own war story — *"we had a few issues that we had to fix, but we also found a larger number of discrepancies caused by bugs in the existing system"*).
  *Ref: Monolith To Microservices.md — "Example: Comparing Credit Derivative Pricing" (`page-128-0`).*
- **Homegate listing migration** — single FTP upload triggers both old monolith import and new REST service. Disable old import only once new one proves equivalent.
  *Ref: Monolith To Microservices.md — "Example: Homegate Listings" (`page-130-0`).*
- **Dark Launching** — deploy new functionality, exercise, never let users see it (parallel run is a way of dark launching).
  *Ref: Monolith To Microservices.md — "Dark Launching and Canary Releasing" (`page-133-0`).*
- **Canary Release** — direct a *subset* of users to the new path; bulk traffic stays on old. Different from parallel run (which calls *both*).
- **N-Version Programming** as analogy — fly-by-wire redundant implementations with quorum voting. Newman's *"end goal here is not to replace any of the implementations."*
  *Ref: Monolith To Microservices.md — "N-Version Programming" (`page-130-0`).*
- Use **Spy pattern** inside the new service to verify side effects (e.g. emails would have been sent) without the user receiving duplicates.
  *Ref: Monolith To Microservices.md — "Using Spies" (`page-131-0`).*
- Try **GitHub Scientist** as a ready-made library — *"ports now exist for multiple languages including Java, .NET, Python, Node.JS."*
  *Ref: Monolith To Microservices.md — "GitHub Scientist" (`page-132-0`).*

**Don't:**
- Don't parallel-run *everything* — *"Implementing a parallel run is rarely a trivial affair, and is typically reserved for those cases where the functionality being changed is considered to be high risk."*
  *Ref: Monolith To Microservices.md — "Where to Use It" (parallel run) (`page-133-0`).*
- Don't confuse **canary release** (subset of users) with **parallel run** (subset of *implementations* called for every user).
  *Ref: Monolith To Microservices.md — "Dark Launching and Canary Releasing" (`page-133-0`).*

**Verification matrix you should run during a parallel run:**
- Functional equivalence (same outputs for same inputs).
- Latency distribution — *"is our new service responding quickly enough?"*
- Failure rate — *"are we seeing too many time-outs?"*
- Side-effect parity (via Spy).

---

### 15. Decorating Collaborator — Attaching New Behaviour Without Changing the Monolith

**Principle:** *"What happens if you want to trigger some behavior based on something happening inside the monolith, but you are unable to change the monolith itself?"* The classic decorator, applied at the *inbound call* boundary, lets a proxy call out to a new microservice based on the response.

**Do:**
- Use when the monolith **cannot be changed** (vendor / SaaS) but you need to attach new behaviour (e.g. Loyalty points on order placement).
  *Ref: Monolith To Microservices.md — "Example: Loyalty Program" (`page-133-0`).*
- Extract the necessary info from the **request or response** — if you have to call back into the monolith for more data, you're introducing circular dependency (see §16 for CDC instead).
  *Ref: Monolith To Microservices.md — "Example: Loyalty Program" (`page-134-0`).*

**Don't:**
- Don't pile business logic into the decorator's proxy — *"The more code you start adding here, the more it ends up becoming a microservice in its own right, albeit a technical one, with all the challenges we've discussed previously."*
  *Ref: Monolith To Microservices.md — "Example: Loyalty Program" (`page-134-0`).*
- Don't decorate when required information isn't in the inbound/response payload — use CDC instead.
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-135-0`).*

---

### 16. Change Data Capture (CDC) — React to Database Events

**Principle:** *"With change data capture, rather than trying to intercept and act on calls made into the monolith, we react to changes made in a datastore."* Use when the monolith cannot emit events / be modified / be intercepted.

**Do — pick an implementation to match trade-offs:**
1. **Database triggers** — call a service / stored proc on INSERT/UPDATE. Cheap, but *"having one or two database triggers isn't terrible. Building a whole system off them is a terrible idea."* (Randy Shoup).
   *Ref: Monolith To Microservices.md — "Database triggers" (`page-137-0`).*
2. **Transaction-log pollers** — Debezium, Oracle GoldenGate, etc. Run as a separate process against the DB's transaction log (committed transactions only). *"In many ways this is the neatest solution."*
   *Ref: Monolith To Microservices.md — "Transaction log pollers" (`page-138-0`).*
3. **Batch delta copier** — cron job scans for changed rows (requires last-modified timestamps). *"I've been bitten too many times by batch processes not running or taking too long to run."*
   *Ref: Monolith To Microservices.md — "Implementing Change Data Capture" (`page-138-0`).*

**Use when:** you need to *react* to a state change in the monolith (loyalty card printing when enrollment completes) without being able to emit events or modify the monolith.
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-139-0`).*

**Don't:**
- Don't lean on CDC when you could decorate or strangle instead — *"My gut feeling is that if the request and response to and from the monolith don't contain the information you need, then think carefully before using the [decorator] pattern. Consider CDC instead."*
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-135-0`).*

---

### 17. Decomposing the Database — Step 1: Recognise the Shared-Database Anti-Pattern

**Principle:** *"Of the three [coupling types], it's implementation coupling that often occupies us most when considering databases."* A shared DB denies information hiding and unclear ownership of state transitions.

**Do:**
- Reject the shared database *as the default*. Cope with it temporarily (see §18) if you must, but plan the decomposition.
  *Ref: Monolith To Microservices.md — "Pattern: The Shared Database" (`page-140-0`).*
- Allow shared read-only access for **truly static reference data** only (country codes, postal codes).
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-142-0`).*
- Allow direct DB access when the service itself *offers* the database as a *designed endpoint* — see §20 (Database-as-a-Service Interface).
  *Ref: Monolith To Microservices.md — "Coping Patterns" (`page-142-0`).*

**Distinguish terms once:** *"a schema [is] a logically separated set of tables that hold data. Multiple schemas can then be hosted on a single database engine."* In the chapter, "database" = "logically isolated schema".
  *Ref: Monolith To Microservices.md — "Schemas and Databases" (`page-142-0`).*

---

### 18. Database Coping Patterns — Use as Stepping Stones, Not Destinations

**Principle:** When full decomposition is premature, use coping patterns that *stop the problem getting worse* and *are reversible*.

### 18a. Database View
- Replaces raw-table access with a view that hides un-used columns. *"Changes to the underlying source schema may require the view to be updated … treat any published database views … like any other service interface."*
  *Ref: Monolith To Microservices.md — "Pattern: Database View" (`page-143-0`).*
- **Constraints:** typically read-only; usually same DB engine; consider a *materialised view* for performance — *"the trade-off then is around how this pre-computed view is updated; it may well mean you could be reading a 'stale' set of data."*
  *Ref: Monolith To Microservices.md — "Views to Present" (`page-145-0`).*
- **Bank war story:** *"over 20 [external] applications … the same username and password … we created a dedicated schema hosting views that looked like the old schema."*
  *Ref: Monolith To Microservices.md — "The Database as a Public Contract" (`page-144-0`).*

### 18b. Database Wrapping Service
- Place an explicit service in front of the schema to *halt further schema growth*. Australian bank entitlements story: DBA begged *"stop them putting things into the database!"* until a wrapping service could be introduced.
  *Ref: Monolith To Microservices.md — "Pattern: Database Wrapping Service" (`page-147-0`).*
- Better than a view: *"you can write code in your wrapping service to present much more sophisticated projections";* can take writes. Align ownership of the service *and* the schema to the same team.
  *Ref: Monolith To Microservices.md — "Pattern: Database Wrapping Service" (`page-149-0`).*

### 18c. Database-as-a-Service Interface
- Expose a *dedicated read-only database* (perhaps different engine — Oracle inside, Cassandra outside) populated via a mapping engine (CDC). Suitable for reporting tools (Tableau).
  *Ref: Monolith To Microservices.md — "Pattern: Database-as-a-Service Interface" (`page-150-0`).*
- *"Outside clients need to understand that they are therefore seeing potentially stale data, and you may find it appropriate to programmatically expose information regarding when the external database was last updated."* — `page-151-0`.

### 18d. Aggregate-Exposing Monolith (key transition pattern)
- When the new service needs data still *owned* by the monolith, expose that aggregate *through a real service endpoint on the monolith itself* — *"We're exposing operations that allow external parties to query the current state of an aggregate, and to make requests for new state transitions."*
  *Ref: Monolith To Microservices.md — "Pattern: Aggregate Exposing Monolith" (`page-153-0`).*
- Often the natural *next* step is to extract a new service (e.g. Employee service after exposing Employee data from monolith for an Invoice service).
  *Ref: Monolith To Microservices.md — "As a pathway to more services" (`page-154-0`).*

### 18e. Change Data Ownership
- Once the new service becomes the source of truth for an aggregate, change the monolith to *consume* the data via the service endpoint. Optionally project a database view back from the new service's schema for legacy readers.
  *Ref: Monolith To Microservices.md — "Pattern: Change Data Ownership" (`page-156-0`).*

**Don't:**
- Don't forget the bank's mistake of issuing identical credentials to 20+ applications — *"when you're relying on network analysis to determine who is using your database, you're in trouble."*
  *Ref: Monolith To Microservices.md — "The Database as a Public Contract" (`page-144-0`).*
- Don't leave a coping pattern in place long-term — *"it could be argued we're just putting a bandage over the problem."*
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-149-0`).*

---

### 19. Data Synchronisation — Dual Reads / Dual Writes / Tracer Write

**Principle:** When source-of-truth handover cannot be instantaneous, run *two* sources of truth temporarily and converge them via a strategy chosen for the data shape.

**Do (three primary strategies for synchronisation):**
1. **Write to one source** — single sink writes to the *real* DB; a CDC pipeline pushes to the other side.
2. **Send writes to both sources** — client fans out (or intermediary broadcasts); consumer is responsible for either-side failure handling.
3. **Seed writes to either source** — bidirectional sync. **Avoid this** — *"requires two-way synchronization (something that can be very difficult to achieve)."*
   *Ref: Monolith To Microservices.md — "Data Synchronization" (tracer write) (`page-167-0`).*

**Tracer Write (the workhorse) — step plan:**
- Step 1: **Bulk Synchronize** — batch import + CDC catch-up; tolerate downtime OR snapshot copy.
- Step 2: **Synchronize on Write, Read from Old** — application writes to *both* (via the new service's API on the new side); reads still come from the old DB so failures in the new side don't lose data.
- Step 3: **Synchronize on Write, Read from New** — the application now reads from the new DB but continues dual-writing; old DB can be retired when confidence is high.
   *Ref: Monolith To Microservices.md — "Pattern: Synchronize Data in Application" (`page-160-0`).*

**Square Orders war story:** Created new Fulfillments service, bulk-replicated existing data via a *flag-controlled* background worker (could be turned off instantly). Subsequent updates were dual-written by upstream clients. *"Eventually, getting to the point where all consumers had switched over ended up being pretty much a non-event. It was just another small change done during a routine release."*
  *Ref: Monolith To Microservices.md — "Example: Orders at Square" (`page-168-0`).*

**Alternative — pub/sub event replication:** Both sources subscribe to the same event stream (when an event-driven architecture already exists). Still eventually consistent.
  *Ref: Monolith To Microservices.md — "Example: Orders at Square" (Figure 4-23) (`page-171-0`).*

**Trifork / Danish medical records story:** MySQL → Riak migration via the same three-step pattern. *"An existing system stored data in one database, but there were limits to how long the system could be offline, and it was vital that data wasn't lost."*
  *Ref: Monolith To Microservices.md — "Pattern: Synchronize Data in Application" (`page-160-0`).*

**Don't:**
- Don't trigger monotonically increasing counters on each side — apply state-machine compensating logic.
- Don't forget to **reconcile** — *"without checking that the synchronization is working as expected, you may end up with inconsistencies between the two systems and not realize it until it is too late."*
  *Ref: Monolith To Microservices.md — "Data Synchronization" (tracer write) (`page-168-0`).*
- Don't use **bidirectional two-way sync** unless you have no alternative — *"very difficult to achieve."*
  *Ref: Monolith To Microservices.md — "Data Synchronization" (`page-167-0`).*

---

### 20. Database-as-a-Service Interface vs. Reporting Database

**Principle:** Already covered in §18c; restated as a standalone principle because it's the most common ask from reporting/BI teams.

**Do:**
- Run a **mapping engine** (Debezium today; batch historically) to keep an external DB in step with the service's internal DB. Expose schema shapes tuned for consumers, not your service's internal model.
  *Ref: Monolith To Microservices.md — "Implementing a Mapping Engine" (`page-151-0`).*
- Surface *last updated* timestamps so clients know staleness is real.
  *Ref: Monolith To Microservices.md — "Compared to Views" (`page-152-0`).*
- Allow the exposed DB to live on a *different* engine (Cassandra inside, PostgreSQL outside) when reporting tools demand SQL.
  *Ref: Monolith To Microservices.md — "Compared to Views" (`page-152-0`).*

**Don't:**
- Don't underestimate the work to keep the external DB in sync — "*Don't underestimate the work required to ensure that this external database projection is kept properly up-to-date."*
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-152-0`).*

---

### 21. Logical vs Physical Separation & Sequencing the Split

**Principle:** *"Logical decomposition allows for simpler independent change and information hiding, whereas physical decomposition potentially improves system robustness, and could help remove resource contention allowing for improved throughput or latency."*

**Do:**
- Sequence explicitly — three options, two preferred:
  - **Split the database first** — exposes performance / atomicity issues early, but no short-term benefit. Use when transactional integrity worries dominate.
  - **Split the code first** — gets independent-deployability win early; carry risk that *"teams may get this far and then stop, leaving a shared database in play on an ongoing basis."*
    *Ref: Monolith To Microservices.md — "Split the Code First" (`page-181-0`).*
  - **Both at once** — usually too big a step. Avoid.
    *Ref: Monolith To Microservices.md — "Split Database and Code Together" (`page-185-0`).*
- Newman's hot take: *"If I'm able to change the monolith, and if I am concerned about the potential impact to performance or data consistency, I'll look to split the schema apart first. Otherwise, I'll split the code out."*
  *Ref: Monolith To Microservices.md — "So, Which Should I Split First?" (`page-185-0`).*

**Pre-decomposition code patterns:**
- **Repository per Bounded Context** — split persistence layer along domain lines; use SchemaSpy to visualise table relationships.
  *Ref: Monolith To Microservices.md — "Pattern: Repository per bounded context" (`page-177-0`).*
- **Database per Bounded Context** — *"At ThoughtWorks … each bounded context in the Revenue service had its own, totally separate databases … if there was a need to separate them into microservices later, this would be much easier."* Hedge your bets.
  *Ref: Monolith To Microservices.md — "Pattern: Database per bounded context" (`page-178-0`).*
- **Monolith as Data Access Layer** (JustSocial) — expose an API on the monolith; new service calls it for data. *"Has so many things going for it that I'm surprised it doesn't seem as well-known as it should be."*
  *Ref: Monolith To Microservices.md — "Pattern: Monolith as data access layer" (`page-181-0`).*
- **Multischema Storage** — keep brand-new functionality's tables in the new service's schema, even while the monolith owns legacy tables.
  *Ref: Monolith To Microservices.md — "Pattern: Multischema storage" (`page-184-0`).*

**Tools:**
- FlywayDB (or DBDeploy-like) for incremental SQL migrations.
  *Ref: Monolith To Microservices.md — "A Note on Tooling" (`page-176-0`).*
- SchemaSpy for visualising cross-table FK coupling.

**Don't:**
- Don't ignore the **risk of never finishing** the DB split when you go code-first.
- Don't assume licence cost = constraint — many orgs have already invested in high-resilience Oracle clusters; running multiple smaller DBs may be the wrong trade-off.
  *Ref: Monolith To Microservices.md — "Physical Versus Logical Database Separation" (`page-174-0`).*

---

### 22. Table-Level Decomposition — Split Table, Move FK to Code

**Principle:** When *tables* (not just schemas) span bounded contexts, you must split them along ownership lines and accept that the database no longer enforces referential integrity across them.

**Do:**
- **Split Table** — when columns are clearly owned by one context or another. When the same column is touched by two contexts, *"a customer's Status still feels like it should be part of the customer domain model. … the new Finance service will need to make a service call to update this status."* (Customer / Status split example.)
  *Ref: Monolith To Microservices.md — "Pattern: Split Table" (`page-186-0`).*
- **Move Foreign-Key Relationship to Code** — for cross-service joins (Catalog Albums ↔ Finance Ledger via SKU). Three deletion strategies after the split:
  - **Check before deletion** — strongly discouraged; *"I strongly urge you not to consider this option."* Race conditions + cascading coupling.
    *Ref: Monolith To Microservices.md — "Check before deletion" (`page-191-0`).*
  - **Handle deletion gracefully** — return `410 GONE` (not `404`) so consumers know the SKU existed once. *"The distinction can be important."*
    *Ref: Monolith To Microservices.md — "Handle deletion gracefully" (`page-191-0`).*
  - **Don't allow deletion** — soft-delete, status flag, or "graveyard" table. Newman's recommendation for the Albums/Ledger case.
    *Ref: Monolith To Microservices.md — "Don't allow deletion" (`page-192-0`).*
- Account for the latency cost of moving joins to code: *"I've gone from a world where we have a single SELECT statement, to a new world where we have a SELECT query against the Ledger table, followed by a service call to the Catalog service."*
  *Ref: Monolith To Microservices.md — "Moving the Join" (`page-190-0`).*
- Use **bulk SKU lookup** + aggressive caching for batch reads like monthly best-sellers reports.
- **Watch for "bigger bite = better"**: when splitting `Order` and `Order Line` apart would break referential integrity, take both together as part of the *same* service — *"Really, the lines of an order are part of the order itself. We should therefore see them as a unit."*
  *Ref: Monolith To Microservices.md — "Where to Use It" (`page-192-0`).*

---

### 23. Static Reference Data — Polyglot Persistence at the Micro Level

**Principle:** Static reference data (country codes, sizing enums) tempts "shared DB" anti-patterns because it's "permanent." Each pattern has a clear cost/benefit profile.

**Do — rank-order these options by Newman's preference:**
1. **Static Reference Data Library** — bundle a JVM/native package with the data. *"The sweet spot … was for types of data that were small in volume and that changed infrequently or not at all."* (Randy Shoup, Stitch Fix).
   *Ref: Monolith To Microservices.md — "Pattern: Static reference data library" (`page-196-0`).*
2. **Dedicated Reference Data Schema** — one logical schema shared by services. Version it as an API.
   *Ref: Monolith To Microservices.md — "Pattern: Dedicated reference data schema" (`page-195-0`).*
3. **Static Reference Data Service** — when teams can ship a microservice in <1 day, or use a FaaS. *"An in-memory dictionary is fine — 249 country codes fits in RAM."*
   *Ref: Monolith To Microservices.md — "Pattern: Static reference data service" (`page-199-0`).*
4. **Duplicate static reference data** — *"Sometimes duplication is the lesser of two evils."* When each consumer uses it locally, inconsistency is not a problem.
   *Ref: Monolith To Microservices.md — "Pattern: duplicate static reference data" (`page-194-0`).*

**Don't:**
- Don't share a mutable DB across services for reference data unless the cost of a dedicated service is *unjustifiable*. Plain sharing is a coupling smell.
- Don't assume lock-step library releases are acceptable. *"If your microservices use shared libraries, remember that you have to accept that you might have different versions of the library deployed in production!"*
  *Ref: Monolith To Microservices.md — "Pattern: Static reference data library" (`page-197-0`).*
- Don't underprice the **service-creation tax** — *"In organizations where deploying new software requires lots of manual work, approvals, and perhaps even the need to procure and configure new hardware, the inherent cost of creating services is significant."* (Kief Morris's bank had a one-year lead time for the first release.)
  *Ref: Monolith To Microservices.md — "Pattern: Static reference data service" (`page-200-0`).*

---

### 24. Transactions After Decomposition — Avoid Distributed Transactions

**Principle:** ACID = Atomicity, Consistency, Isolation, Durability. When data is split, *"we have to accept that we've lost guaranteed atomicity of the operation as a whole."*

**Do:**
- Use ACID transactions **inside each service** for its own aggregate; accept that *across services* you no longer have atomicity.
  *Ref: Monolith To Microservices.md — "ACID Transactions" (`page-187-0`).*
- Skip two-phase commit (2PC). Common failure modes include coordinator crashes, partial commits, deadlocks across distributed locks. *"I strongly suggest you avoid the use of distributed transactions like the two-phase commit to coordinate changes in state across your microservices."*
  *Ref: Monolith To Microservices.md — "Distributed Transactions—Just Say No" (`page-207-0`).*
- Use **sagas** for any cross-service workflow that involves long-lived transactions or compensating semantics.
  *Ref: Monolith To Microservices.md — "Sagas" (`page-208-0`).*

**Why 2PC is bad (in Newman's words):**
- *"When two-phase commits work, at their heart they are very often just coordinating distributed locks. The workers need to lock local resources to ensure that the commit can take place during the second phase."* — `page-207-0`.
- *"The more participants you have, and the more latency you have in the system, the more issues a two-phase commit will have."* — `page-207-0`.
- Pat Helland's warning: *"the failure of a single node causes transaction commit to stall … the larger it gets, the more likely the system is going to be down."*
  *Ref: Monolith To Microservices.md — "Sagas Versus Distributed Transactions" (`page-220-0`).*

**Don't:**
- Don't use single-DB ACID as an excuse not to split data. Sometimes *"if you have pieces of state that you want to manage in a truly atomic and consistent way, and you cannot work out how to sensibly get these characteristics without an ACID-style transaction, then leave that state in a single database."*
  *Ref: Monolith To Microservices.md — "Distributed Transactions—Just Say No" (`page-208-0`).*

---

### 25. Sagas — The Cross-Service Transaction Pattern

**Principle:** A saga decomposes a long-lived transaction into a sequence of independent sub-transactions, each with ACID inside its own service. *"A saga does not give us atomicity in ACID terms … What a saga gives us is enough information to reason about which state it's in."* — Garcia-Molina & Salem, 1987.

**Do (recovery modes):**
- **Backward recovery (rollback)** — trigger *compensating transactions* to undo committed sub-transactions. These are **semantic rollbacks**, not real ones: *"you can't unsend an email!"* — you send a *second* email explaining the cancellation.
  *Ref: Monolith To Microservices.md — "Saga rollbacks" (`page-211-0`).*
- **Forward recovery (retry)** — persist enough state to resume. Implementation wise requires the saga to be re-entrant.
  *Ref: Monolith To Microservices.md — "Saga Failure Modes" (`page-210-0`).*
- **Reorder steps to reduce rollback scope** — e.g. award loyalty points *after* dispatch. *"Sometimes you can simplify your rollback operations just by tweaking how the process is carried out."*
  *Ref: Monolith To Microservices.md — "Reordering steps to reduce rollbacks" (`page-213-0`).*
- **Mix recovery modes** — package failure could rollback; courier-van-full failure could retry.
  *Ref: Monolith To Microservices.md — "Mixing fail-backward and fail-forward situations" (`page-214-0`).*

**Do (implementation styles):**

**Orchestrated sagas** — a central orchestrator decides the sequence, can fire compensations. Command-and-control.
- Pros: process is **explicitly modelled**; easier to understand; **central place to track saga state**.
- Cons: high **domain coupling** in the orchestrator; risk of "god service" absorbing logic that should live in participants.
- *Anti-anti-pattern tip:* *"one of the ways to avoid too much centralization with orchestrated flows can be to ensure you have different services playing the role of the orchestrator for different flows."* (Order Processor for ordering; Returns service for returns; Goods Receiving for stock intake.)
  *Ref: Monolith To Microservices.md — "Orchestrated sagas" (`page-214-0`).*
- BPM tools (Camunda, Zeebe) map to orchestrated sagas but Newman dislikes them — *"the central conceit — that nondevelopers will define the business process — has in my experience almost never been true."* If your developers are coding the flows, let them use code.
  *Ref: Monolith To Microservices.md — "BPM Tools?" (`page-216-0`).*

**Choreographed sagas** — services react to events; no central coordinator. Loose coupling / trust-but-verify.
- Pros: extremely **loose coupling**; "if you don't have a place where logic can be centralized, then it won't be centralized!" — `page-218-0`.
- Cons: harder to track saga state; attach a **correlation ID** to every event and have a state projector reconstruct progress.
  *Ref: Monolith To Microservices.md — "Choreographed sagas" (`page-217-0`).*

**Newman's recommendation:**
- *"I'm very relaxed in the use of orchestrated sagas when one team owns implementation of the entire saga. … If you have multiple teams involved, I greatly prefer the more decomposed choreographed saga."*
  *Ref: Monolith To Microservices.md — "Should I use choreography or orchestration?" (`page-219-0`).*

**Reference order-flow saga (Figure 4-50, `page-210-0`):**
```
Create order  →  Authorize payment  →  Reserve stock  →  Package item
                                                         │
                                              on failure: ▼
                                  Compensating transactions:
                                  Undo payment auth + release stock
                                                         │
                                            on success:   ▼
                                   Award loyalty points  →  Dispatch
```
*Ref: Monolith To Microservices.md — "Saga Failure Modes" (`page-210-0`).*

**Don't:**
- Don't claim semantic rollback == database rollback — semantically they undo state but not *effect-time* (e.g. sent email, charged card).
- Don't pretend a single orchestrator can own all sagas without becoming a god service.

---

### 26. Growth Pains (Predictable Pains at Service-Count Thresholds)

**Principle:** Pain points are roughly correlated with service count. Plan capacity, tooling and process for them *before* they bite.

| Service count | Likely pains | Forward-fix |
|---|---|---|
| **2–10** | Breaking changes; reporting across the new world | Lock down contracts (Pact/CDCs); establish reporting DB (§20) early |
| **10–50** | Ownership at scale; degraded developer experience; running too many things | Strong code ownership; logging aggregation; Kubernetes / FaaS; stubbing |
| **50+** | Global vs. local optimisation; orphaned services | Architecture guild / community of practice; service registry (§26-h) |
| **Any** | Robustness & resilience; monitoring & troubleshooting; end-to-end testing | Circuit breakers / timeouts; correlation IDs + tracing; consumer-driven contract tests |

*Ref: Monolith To Microservices.md — "More Services, More Pain" (`page-222-0`).*

---

### 27. Ownership at Scale — Strong > Weak > Collective for >=100 devs

**Principle:** Martin Fowler's three ownership models apply to microservices:
- **Strong** — owners must accept external changes via PR.
- **Weak** — sources anyone can edit; conventions/"ask first" hold.
- **Collective** — anyone can change anything.

Newman's prescription: *"Strong code ownership is almost universally the model adopted by organizations implementing large-scale microservice architectures consisting of multiple teams and over 100 developers."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Ownership at Scale) (`page-224-0`).*

**Do:**
- Allow each team to adopt *collective* ownership *within* its boundary; that's how the model scales.
- Pair ownership with **product-oriented teams** — *"if your team owns some services, and those services are oriented around the business domain, then your team becomes more focused on one area of the business domain."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-225-0`).*

**Don't:**
- Don't try to keep collective ownership at >100 developers — *"At scale I've seen collective code ownership be disastrous."* One fintech ended up with *"colander architecture"* — *"people would just 'punch a new hole' whenever they felt like it."*
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-224-0`).*
- Don't treat distributed monoliths as microservices — *"the cost of detangling a distributed monolith is much higher"* than a real monolith.
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-225-0`).*

---

### 28. Breaking-Change Discipline (3 rules)

**Principle:** *"I have a set of rules for managing breaking contracts. They're pretty simple:"* `page-227-0`
1. **Eliminate accidental breaking changes** — use explicit schemas (avoid magic JSON serialization). Try `protolock` for Protobuf.
2. **Think twice** — prefer additive (expand) changes; keep old endpoints working.
3. **Give consumers time** — run two versions of the contract in one service (single deploy, two ports), OR deploy two versions of the service.

**Do:**
- Distinguish `410 GONE` (used to exist) from `404` (never existed) — it makes post-incident forensics much easier.
  *Ref: Monolith To Microservices.md — "Handle deletion gracefully" (`page-191-0`).*
- Treat **lock-step releases** as a smell when they happen across teams. *Within* a team, they're tolerable.
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-227-0`).*
- "*You need good communication with the people who manage the services that consume your service. … Treat consumers of your service like customers."*
  *Ref: Monolith To Microservices.md — "Give consumers time to migrate" (`page-230-0`).*

**Don't:**
- Don't use "schema-less" interchange formats reflexively — *"Developers tend to curse the constraints of formal schemas initially — after they've had to deal with breaking changes across services, they'll change their minds."*
  *Ref: Monolith To Microservices.md — "Eliminate accidental breaking changes" (`page-227-0`).*
- Don't fret endlessly about backward compatibility within one team — the cost is cheap there. Reserve strictness for boundaries you don't control.
  *Ref: Monolith To Microservices.md — "Give consumers time to migrate" (`page-230-0`).*

---

### 29. Reporting Across Services

**Principle:** Splitting the schema breaks the assumption that one SQL endpoint can JOIN everything. Restore it deliberately.

**Do:**
- Push service-owned data into a **dedicated reporting database** via CDC, events, or programmatic copies.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Reporting) (`page-232-0`).*
- Allow the reporting schema to drift from internal schemas (decouple reporting concerns from operational).
- Consider a **data warehouse / data lake** as the natural place for cross-service historical joins.
  *Ref: Monolith To Microservices.md — "Reporting" (`page-216-0`).*
- Surface stale-data latency to consumers (`last_updated_at` per row) so BI tools can flag freshness.

**Don't:**
- Don't assume BI stakeholders will rewrite their queries for the new world. *"Unless you want to change how they work, you're going to still need to present a single database for reporting, and quite possibly one that matches the old schema design."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Reporting) (`page-232-0`).*
- Don't discover the reporting constraint halfway through migration — *"out of sight, out of mind."*
  *Ref: Monolith To Microservices.md — "When Might This Problem Occur?" (`page-232-0`).*

---

### 30. Monitoring, Tracing & Test-in-Production

**Principle:** *"With a standard monolithic application, we can have a fairly simplistic approach to monitoring … With a microservice architecture, we can have the failure of just one service instance, or just one type of instance to consider."*

**Do (build in this order):**
1. **Log aggregation first** — *"Strongly consider implementing log aggregation as the first thing you do before implementing a microservice architecture."* (ELK stack / Humio / Fluentd).
   *Ref: Monolith To Microservices.md — "Log aggregation" (`page-233-0`).*
2. **Correlation IDs** — generate at the perimeter (API gateway / service mesh), propagate via HTTP headers / message envelope. *"When the Notification service handles the call, it can log information about what it is doing in conjunction with that same correlation ID."*
   *Ref: Monolith To Microservices.md — "Tracing" (`page-234-0`).*
3. **Distributed tracing** (Jaeger, Zipkin, OpenTelemetry) — adopt when latency budget tightens. A service mesh handles inbound/outbound tracing for free.
   *Ref: Monolith To Microservices.md — "Tracing" (`page-235-0`).*
4. **Synthetic transactions / test in production** — Atomist wired a fake-customer enrollment through GitHub + Slack to catch API-rate-limit and auth bugs before real users hit them.
   *Ref: Monolith To Microservices.md — "Test in production" (`page-236-0`).*
5. **Observability mindset** — *"Don't assume you know the answers up front. … make sure you use toolchains that allow for ad hoc querying of information."* Cindy Sridharan, *Distributed Systems Observability*.
   *Ref: Monolith To Microservices.md — "Toward observability" (`page-237-0`).*

**Don't:**
- Don't accidentally order 200 washing machines. Atomist synthetic tests used fake accounts they could clean up; yours must too.
  *Ref: Monolith To Microservices.md — "Test in production" (`page-237-0`).*
- Don't make tests-in-prod ignore privacy, idempotency, and load implications. They are real transactions.

---

### 31. Local Developer Experience at Scale

**Principle:** *"I could probably run four or five JVM-based microservices as separate processes on my laptop, but could I run ten or twenty? Probably not."*

**Do:**
- Stub out services outside the developer's concern. Strong ownership teams tend to do this naturally.
- Adopt **hybrid local/remote dev** tooling — Telepresence proxies local calls to a remote cluster; Azure Functions let you run locally while talking to cloud resources.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Local Developer Experience) (`page-239-0`).*
- Track developer-experience metrics — local build time, time-to-first-render, dev-container start-up time.

**Don't:**
- Don't just hand out bigger laptops — *"While that might be OK for a short-term fix, that will only buy you some time if your service estate continues to grow."*
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-238-0`).*
- Don't pretend remote-only dev is free — connectivity, slower feedback loops, infra cost all change.

---

### 32. Running Too Many Things — Platform Choices

**Principle:** *"Desired state management in particular becomes increasingly important … the ability for you to specify the number and location of service instances that you require, and ensure that this is maintained over time."*

**Do:**
- Adopt **Kubernetes / OpenShift** when your manual deployment stories start to strain — *"you should wait until you have enough processes that your current approach and technology are starting to strain."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Running Too Many Things) (`page-240-0`).*
- Go **serverless-first** on public cloud — *"try to make use of serverless technology like FaaS as a default choice, because of the reduction in operational work."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-240-0`).*
- Adopt infrastructure-as-code (Kief Morris, *Infrastructure as Code*) before platform sprawl.

**Don't:**
- Don't adopt Kubernetes prematurely — *"people reaching for Kubernetes … a bit too early in the process of adopting microservices, often assuming it is a prerequisite."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-240-0`).*

---

### 33. End-to-End Testing — Limit Scope, Use CDCs

**Principle:** *"The more functionality a test executes — the broader the scope of the test — the more confidence you have in your application. On the other hand, the larger the scope of the test, the longer it can take to run, and the harder it can be to work out what is broken when it fails."*

**Do:**
- **Limit cross-service test scope** — keep tests inside the team that owns them.
- **Consumer-Driven Contracts (Pact)** — *"with CDCs, you have the consumer of your microservice define their expectations of how your service should behave in terms of an executable specification."*
  *Ref: Monolith To Microservices.md — "Use consumer-driven contracts" (`page-242-0`).*
- **Progressive delivery + automated release remediation** — define acceptable thresholds (e.g. p95 latency, error rate); auto-rollback if exceeded. *Netflix Spinnaker* is the canonical example.
  *Ref: Monolith To Microservices.md — "Use automated release remediation" (`page-242-0`).*
- **Continually refine quality feedback cycles** — remove tests as well as add them; balance safety with speed.
  *Ref: Monolith To Microservices.md — "Continually refine your quality feedback cycles" (`page-243-0`).*

**Don't:**
- Don't grow an end-to-end suite to cover everything — *"your end-to-end test suite grows, taking longer and longer to complete."*
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-242-0`).*
- Don't treat re-running a failed test as a debugging step; track flakiness aggressively.

---

### 34. Global vs. Local Optimisation

**Principle:** *"Teams optimizing locally can hurt the system globally."* Three teams picking three different databases (Oracle / Mongo / PG) for similar workloads is the canonical example.

**Do:**
- Map local decisions to the **reversible ↔ irreversible** spectrum. Irreversible → involve others; reversible → local autonomy.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Global vs. Local) (`page-245-0`).*
- Hold a **cross-team technical group** chaired by a CTO / chief architect — *"a sensible approach"*.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-245-0`).*
- Adopt lightweight mechanisms (Monzo's *proposals*) — *"Free-form documents published into a shared space that … alerts the whole company via Slack."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-245-0`).*
- Use *communities of practice* to spot accidental divergence — *"You can spot these problems much earlier if you have some sort of cross-team technical group."*
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-244-0`).*

**Don't:**
- Don't centralise every decision — that just moves the bottleneck.
- Don't decentralise everything — REA eventually hit *"duplicate work that each team was doing"* and had to re-platform the meta (deployment, observability) layer.
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-244-0`).*

---

### 35. Robustness, Resilience & Failure-Mode Discipline

**Principle:** *"Microservices do not necessarily give you robustness for free. Rather, they open up opportunities to design a system in such a way that it can better tolerate network partitions, service outages, and the like."*

**Do (two questions per service call):**
1. *"Do I know the way in which this call might fail?"*
2. *"If the call does fail, do I know what I should do?"*
   *Ref: Monolith To Microservices.md — "Potential Solutions" (Robustness) (`page-247-0`).*

- Apply standard patterns: timeouts, retries with jitter + exponential backoff, **circuit breakers**, **bulkheads**, **asynchronous messaging** to remove temporal coupling.
- Run **multiple service instances** for redundancy; use desired-state platforms to keep that count stable.
- Distinguish **robustness** (handle known variations) from **resilience** (organisation that adapts to unknown failures); both matter.
  *Ref: Monolith To Microservices.md — "Resilience Versus Robustness" (`page-54-0`).*
- Document every production incident with what was learned — *"All too often I see organizations move on too quickly once the initial problem has been solved or worked around."*
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-247-0`).*

**Don't:**
- Don't equate *chaos engineering* with *resilience*. Chaos experiments test robustness of specific failure modes; resilience is organisational.

---

### 36. Orphaned Services — Lifecycle Management

**Principle:** *"Microservices can exhibit some of the same characteristics [as servers walled up in old offices]; they're out there and they're working (we assume), but we have the same problem that we may not know what to do with them."*

**Do:**
- Maintain a **service registry** with metadata: owner, on-call, source repo, dependencies, runbook.
- The **Financial Times Biz Ops** registry calculates a *System Operability Score* per service — *"things that services and their teams should do to ensure the service can be easily operated"*.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Orphaned Services) (`page-248-0`).*
- Crawl source repos + service-discovery (Consul, etcd) to populate the registry automatically.
- Plan for **retirement, not just growth**. A service that does its job but is no longer needed is itself an orphan.

**Don't:**
- Don't let orphaned services lurk behind domain ownership changes — explicitly re-assign or retire.

---

### 37. Anti-Patterns Catalog (the Migration's Bad Endings)

**Principle:** These are the destinations Newman spends the book warning you away from.

- **The Distributed Monolith** — *"a system that consists of multiple services, but for whatever reason the entire system has to be deployed together. … In my experience, distributed monoliths have all the disadvantages of a distributed system, and the disadvantages of a single-process monolith, without having enough upsides of either."*
  *Ref: Monolith To Microservices.md — "The Distributed Monolith" (`page-29-0`).*
  - Cause: lack of focus on information hiding, cohesion, well-defined contracts.
  - Fix: back up with §2 (independent deployability) and §5 (coupling taxonomy).

- **Big-Bang Rewrite** — *"the only thing you're guaranteed of is a big bang"* (Fowler). Months/years of work delivered in one release; can't serve customers during; can't recover from early mistakes.
  *Ref: Monolith To Microservices.md — "Importance of Incremental Migration" (`page-67-0`).*
  - Fix: chip away at the monolith; assemble migration features inside feature backlogs.

- **Premature Decomposition** — SnapCI decomposed early, fought cross-service changes for months, merged back into a monolith, waited a year, decomposed again correctly.
  *Ref: Monolith To Microservices.md — "Unclear Domain" (`page-58-0`).*
  - Fix: domain modelling + event storming before extraction; modular monolith as hedge.

- **Incomplete Migration** (Code-First, DB-Later) — *"I've seen teams that have fallen into this trap … leaving a shared database in play on an ongoing basis."*
  *Ref: Monolith To Microservices.md — "Split the Code First" (`page-181-0`).*
  - Fix: be honest with yourself — *"are you confident that you will be able to make sure that any data owned by the microservice gets split out as part of the next step?"*
  - Recovery: §18-§21 patterns.

- **Cargo Cult "Microservices" / "Kafka" / "Kubernetes"** — *"I think my biggest worry about premature decomposition is people cargo-culting microservices."* (e.g. everyone adopting the Spotify model without its context.)
  *Ref: Monolith To Microservices.md — "It's Not One Size Fits All" (`page-78-0`).*

- **The Smart Pipe Anti-Pattern** — putting routing / transformation logic into shared middleware becomes a new bottleneck. *"Keep the pipes dumb, the endpoints smart."*
  *Ref: Monolith To Microservices.md — "Changing Protocols" (`page-106-0`).*

- **Sunk-Cost / Concorde Fallacy** — *"the bigger the bet, and bigger the accompanying fanfare, the harder it is to pull out when it's going wrong."*
  *Ref: Monolith To Microservices.md — "Avoiding the Sunk Cost Fallacy" (`page-88-0`).*
  - Fix: small steps + checkpoints; *"It is totally OK … what you're doing."* — `page-67-0`.

- **"Reuse" as Goal** — see §1.

- **CDCs / Strong Ownership Rejection** — see §28.

---

### 38. Migrating Data — End-to-End Rollback Strategy

**Principle:** Every data decomposition step must come with an undo plan — because the migration is rarely right the first time.

**Do (assemble the rollback ladder):**
1. **Feature flag / proxy config** — flipping a single config flag reverts the strangler redirect (§11).
2. **Feature toggle inside the abstraction** — branch by abstraction §13 lets you switch implementations.
3. **Tracer write** — keep the old schema in sync; consumers haven't migrated yet (§19).
4. **Parallel run on writes** — keep dual-writing for a sentinel period before retiring.
5. **Backup + restore script** for the *last* step (drop the old table). Test it before you need it.

**Don't:**
- Don't trust "the data was migrated successfully" without a **reconciliation query**. *"Without checking that the synchronization is working as expected, you may end up with inconsistencies between the two systems and not realize it until it is too late."* — `page-168-0`.
- Don't claim rollback is "easy" without rehearsing it. Most rollover failures happen during the rollback, not the rollout.

---

### 39. Migration Metrics — Did It Actually Work?

**Principle:** *"Based on the outcomes you are hoping to achieve, you should try defining some measures that can be tracked."*

**Do (track both quantitative and qualitative measures):**
- **Quantitative** — tailored to the goal: cycle time / deploy frequency / failure rate (time-to-market); perf test results (scale); MTTR / MTTF (resilience).
- **Qualitative** — *"'Software is made of feelings' — Astrid Atkinson."* Survey your team; are they enjoying the work, feeling empowered, supported?
  *Ref: Monolith To Microservices.md — "Qualitative Measures" (`page-87-0`).*

**Checklist for every checkpoint:**
1. Restate the expected outcome.
2. Review quantitative measures.
3. Gather qualitative feedback.
4. Decide what (if anything) to change.
   *Ref: Monolith To Microservices.md — "Having Regular Checkpoints" (`page-86-0`).*

**Watch-out:**
- *"Metrics can be gamed — inadvertently, or on purpose."* Newman's wife worked at a vendor paid by tickets closed — vendors closed tickets without fixing, opening new tickets.
  *Ref: Monolith To Microservices.md — "Quantitative Measures" (`page-86-0`).*
- Cycle time may *worsen* early in migration — *"I'd likely expect to see this get worse initially."*
  *Ref: Monolith To Microservices.md — "Quantitative Measures" (`page-87-0`).*

---

### 40. Feature-Freeze Rules During Migration

**Principle:** Each migration has a window during which behaviour in the migrated code must be frozen, otherwise rollback cannot repair production.

**Do:**
- Treat feature-freeze windows as **first-class schedule items**; assign someone to enforce them.
- When the migration window must extend, plan for *parallel-run both* (see §14) rather than allowing behavioural drift.
  *Ref: Monolith To Microservices.md — "Changing Behavior While Migrating Functionality" (`page-112-0`).*

**Don't:**
- Don't be tempted to "slip this feature in while you're at it" — *"the longer the migration takes, the more pressure you'll be under to 'just slip this feature in.'"*
  *Ref: Monolith To Microservices.md — "Changing Behavior While Migrating Functionality" (`page-112-0`).*

---

### 41. The 12-Factor Lens Applied to Migration

**Principle:** 12-Factor principles are prerequisites; the migration sometimes forces their adoption.

**Do:**
- **Config in environment** (§4) — without per-environment config the new service can't strangle.
- **Stateless processes** — rely on the new service being stateless so you can run shadow copies (§14).
- **Disposable fast startup / graceful shutdown** — required for canary/strangler proxy rerouting.
- **Dev/prod parity** — if your only "test env" is the monolith, you cannot run a parallel run safely.
- **Logs as event streams** — see §30 (log aggregation first).
- **Admin processes as one-off** — schema-migration tools (FlywayDB) belong here.
- **Port binding** — *self-contained* services, no shared middleware.

**Don't:**
- Don't ship a microservice that depends on locally-installed daemons — you've recreated the monolith's deployment hazard at smaller scale.

---

### 42. Organisational Contracts for the Borderline Cases

**Principle:** Most anti-patterns (§37) are organisational failures wearing technical clothes. Define explicit contracts *between* teams before introducing technical mechanism.

**Do:**
- Treat every API as a **shared, versioned contract**. *Reckon with the cost of change.*
- Write **downstream-as-customer** discipline into the consumer team (treat them like customers, see §28).
- Use the **three-reversibility questions** for every architectural decision:
  - *What happens if I change my mind?*
  - *How big a blast radius does reverting have?*
  - *Who else would be impacted?*
- Adopt **explicit ownership** of the trade-offs (e.g. *"the Finance team may now cache stale data"*). Face the conversation before, not after, the rollout.
  *Ref: Monolith To Microservices.md — "Creating the Guiding Coalition" (`page-63-0`).*

---

### 43. Migration Playbook Summary (executive checklist)

A condensed 12-step playbook you can hand to a delivery team:

1. **Articulate the goal** — three questions (§1), sliders, decision reversibility.
2. **Domain model** — DDD + Event Storming, draw bounded contexts and their inbound dependencies (§6).
3. **Choose first extraction** — value vs. difficulty quadrant; aim for top-right (§8).
4. **Build a foundation** — log aggregation (§30), CI/CD, deployment pipelines (§32).
5. **Build trust with the coalition** — Kotter steps (§9), get non-engineers in the room.
6. **Refactor the monolith along seams** — modular monolith (§4), repositories per context (§21).
7. **Split the database** (if same-team cohesion concerns warrant) — or split code first, schedule DB split explicitly (§21).
8. **Strangle** the chosen slice (§11); separate deployment from release.
9. **Migrate the data** with three-step tracer write (§19); reconcile continually.
10. **Verify with progressive delivery** — canary, dark launch, parallel run, Scientist (§14).
11. **Measure** quantitative + qualitative (§39); checkpoint quarterly.
12. **Communicate, share stories, consolidate** — never stop. Don't let the new plateau become the new ceiling.

---

### 45. Case Study Hall-of-Fame (Patterns in Living Colour)

**Principle:** Each named case study in *Monolith to Microservices* is itself a checkpoint pattern. Read each as *"what they did, why it worked, what could trip you up."*

### 45a. SnapCI (ThoughtWorks) — *the cautionary tale*
- Continuous-integration/continuous-delivery hosting product. Team had domain experience (Go-CD predecessors) yet decomposed prematurely into microservices.
- Result: many cross-service changes, high cost of ownership. Merged back into one app. Waited a year. Re-decomposed correctly.
- Lesson: *"Prematurely decomposing a system into microservices can be costly, especially if you are new to the domain. In many ways, having an existing codebase you want to decompose into microservices is much easier than trying to go to microservices from the beginning."*
  *Ref: Monolith To Microservices.md — "Unclear Domain" (`page-58-0`).*

### 45b. The Guardian newspaper — UI composition + skills upskilling
- Vertical-by-vertical migration (Travel first), page-composition with Edge-Side Includes.
- Single widget "*displaying the top 10 travel destinations*" spliced into the old CMS first; later the whole Travel vertical was moved.
- Re-used the Fastly CDN as a *routing layer* when migrating again years later — *"effectively using the CDN much as you might use an in-house proxy."*
- Skills upskilling tracked with a *private* per-individual self-assessment aggregated into a team chart (Oracle / Kotlin upskilling).
  *Ref: Monolith To Microservices.md — "Example: Page Composition" (`page-113-0`), "Example: Widget Composition" (`page-114-0`), "Changing Skills" (`page-83-0`).*

### 45c. Homegate (Swiss real estate) — FTP interception + parallel run
- Customers uploaded listings via FTP to the monolith. Goal: new microservice with a soon-to-be-ratified REST API.
- Solution: monitor FTP server log, redirect new uploads to an adapter calling the new REST API. Customer interface unchanged.
- *"Both listing upload mechanisms were enabled. This allowed the team to make sure the two upload mechanisms were working appropriately. This is a great example of … Pattern: Parallel Run."*
  *Ref: Monolith To Microservices.md — "Example: FTP" (`page-108-0`).*

### 45d. Investment bank credit derivatives (Newman's own) — database-as-public-contract
- Trying to increase write throughput by restructuring the schema; discovered 20+ external applications had read access (some write) to the schema, using a *shared* credential.
- Solution: dedicated schema with views that mimic the old schema; resolve the small number of external writers first; leave views stable while evolving the real schema.
- *"It was rumored that one of the systems using our database was a Python-based neural net that no one understood but 'just worked.'"*
  *Ref: Monolith To Microservices.md — "The Database as a Public Contract" (`page-144-0`).*

### 45e. Australian bank entitlements — wrapping service to stop the bleeding
- 30-year-old crown-jewel business banking product stored everything in stored procedures; entitlements logic was tangled with all data access.
- A new *Entitlements Service* — initially thin (no behaviour change!) — wrapped the database. Goal: stop new functionality going into the schema, then incrementally remove the easy pieces.
- *"It would be a nightmare to try to untangle, and the risks associated with making mistakes in this area were huge."*
  *Ref: Monolith To Microservices.md — "Pattern: Database Wrapping Service" (`page-147-0`).*

### 45f. JustSocial — *monolith as data access layer*
- Avoided direct cross-schema access by exposing the data via monolith endpoints; later extracted the Employee service directly.
  *Ref: Monolith To Microservices.md — "Pattern: Monolith as data access layer" (`page-181-0`).*

### 45g. Trifork / Danish medical records — MySQL → Riak
- Couldn't take the system offline; needed fast rollback and verification.
- Three-step tracer write: bulk migrate → CDC catch-up → dual-write while reading from old → dual-write while reading from new → drop old.
  *Ref: Monolith To Microservices.md — "Pattern: Synchronize Data in Application" (`page-160-0`).*

### 45h. Square — Fulfillments extraction
- Restaurant / driver / customer workflows all touched the same Order row; high delivery contention.
- New Fulfillments service took ownership of fulfillment-related fields; background worker (flag-controlled) copied data via the new service's API; upstream clients updated to write both sides; eventually switched reads to the new service.
- Outcome: *"getting to the point where all consumers had switched over ended up being pretty much a non-event."*
  *Ref: Monolith To Microservices.md — "Example: Orders at Square" (`page-168-0`).*

### 45i. Spotify — mobile UI server-side composition
- All Spotify clients (iOS, Android, web) render components described declaratively from the server.
- *"Spotify engineers are able to change the views that users see and roll that change quickly, without needing to submit new versions of their application to the app store."*
  *Ref: Monolith To Microservices.md — "And mobile applications" (`page-117-0`).*

### 45j. Orbitz — module-based UI decomposition
- Pre-microservices, the Orbitz website was already a "Content Orchestration" monolith serving UI modules; teams had clear ownership of those modules.
- Migration: extract modules one at a time behind the existing orchestration service. *"The fact that the UI was already decomposed visually along these lines made this work easier to do in an incremental fashion."*
  *Ref: Monolith To Microservices.md — "Example: Widget Composition" (`page-116-0`).*

### 45k. Stitch Fix — shared library for reference data
- Randy Shoup's guidance: sweet spot is small, infrequently-changing data; different library versions in production is *expected*.
  *Ref: Monolith To Microservices.md — "Pattern: Static reference data library" (`page-196-0`).*

### 45l. ThoughtWorks Revenue service — modular monolith with separate schemas
- Three contexts sharing a single deploy but each with its own schema. Years later, still a modular monolith — *"it turned out that this was never needed."*
  *Ref: Monolith To Microservices.md — "Pattern: Database per bounded context" (`page-179-0`).*

### 45m. REA Group Australia — converged deployment patterns after years of divergence
- Realised too late that N different teams had built N different deployment patterns; rebuilt the meta-layer.
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (Global vs. Local) (`page-244-0`).*

### 45n. Financial Times — Biz Ops service registry with System Operability Score
- Central registry combining source-repo crawl + service discovery; computes operability scores to nudge teams to fill gaps.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Orphaned Services) (`page-248-0`).*

### 45o. Atomist — test-in-production via fake customers
- Synthetic transactions exercised GitHub + Slack OAuth end-to-end on a regular cadence; caught rate-limit and integration bugs before real users.
- Caveat: ensure the side-effects are disposable.
  *Ref: Monolith To Microservices.md — "Test in production" (`page-236-0`).*

### 45p. Kief Morris's UK bank — service-creation tax
- Ten internal teams consulted; nearly a year to first release. *"Such experiences are far from uncommon in larger organizations."*
  *Ref: Monolith To Microservices.md — "Pattern: Static reference data service" (`page-200-0`).*

### 45q. Spotify model — the *failure* case (negative reference)
- *"An organizational structure that worked well for a Swedish music streaming company may not work for an investment bank. … It turns out not even Spotify uses the Spotify model."*
  *Ref: Monolith To Microservices.md — "It's Not One Size Fits All" (`page-78-0`).*

### 45r. GoCD / Cruise — branch-by-abstraction done for months
- Multiple-month migration of iBatis → Hibernate via branch by abstraction, while twice-weekly releases continued.
  *Ref: Monolith To Microservices.md — "Step 3: Create new implementation" (`page-122-0`).*

### 45s. Newman's own bank credit pricing — *verifying with reconciliation*
- *"We actually wrote a program to perform the reconciliation. We presented the results in an Excel spreadsheet."*
  *Ref: Monolith To Microservices.md — "Example: Comparing Credit Derivative Pricing" (`page-129-0`).*

### 45t. Netflix — consumer-driven contracts for large data migrations
- Daniel Bryant write-up of Sangeeta Handa's QCon SF talk.
  *Ref: Monolith To Microservices.md — "Data Synchronization" (`page-170-0`).*

---

### 46. Conway's Law & Inverse-Conway Maneuvers

**Principle:** *"Any organization that designs a system … will inevitably produce a design whose structure is a copy of the organization's communication structure."* — Melvin Conway, *How Do Committees Invent?*

**Do:**
- Acknowledge Conway's law when choosing architecture: define the team shape first, then derive the service shape (Inverse-Conway Maneuver).
  *Ref: Monolith To Microservices.md — "Modeled Around a Business Domain" (`page-18-0`).*
- Use the *true tech company* model (PMs in delivery teams, no central IT silo) as the target organisation.
  *Ref: Monolith To Microservices.md — "And Ownership" (`page-25-0`).*
- When silos remain, recognise *"you may need to reach across the aisle to find a supporter elsewhere"* in the guiding coalition.
  *Ref: Monolith To Microservices.md — "Creating the Guiding Coalition" (`page-64-0`).*
- Use the three-tier architecture's *organisational* roots as your mirror for what *not* to do — *"this architecture is so common … because it is based on how we organize our teams."*
  *Ref: Monolith To Microservices.md — "Modeled Around a Business Domain" (`page-19-0`).*

**Don't:**
- Don't reorganise *and* adopt microservices at the same time. Sequence org changes ahead of architecture changes; the org's communication paths will otherwise leak into coupling.
- Don't pretend Conway's law only flows one direction — teams reorganised around services will *also* influence upstream communications.

---

### 47. Conway-Mirror Risk: Distributed Monolith Anti-Pattern in Detail

**Principle:** *"Distributed monoliths typically emerge in an environment where not enough focus was placed on concepts like information hiding and cohesion of business functionality."*

**Do (avoid by):**
- **Strict ownership** (§27) — *"if you decide to break a contract, it's on you to handle the implications."* — `page-229-0`.
- **External contract discipline** (§28) — no shared databases; explicit schemas; co-existence patterns when changing.
- **Own changes end-to-end** — operate what you build.
- **Track ownership at the contract level**, not just at the code level: who owns the API definition? who owns the SLA?
- Treat the "colander architecture" symptom (*"people would just 'punch a new hole' whenever they felt like it"*) as the canary.
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (`page-224-0`).*

**Don't:**
- Don't allow direct point-to-point DB access from any service into another service's schema, *even for a "quick read"* — distributed-monolith smells start here.
- Don't overload a "shared library" with logic that becomes a de-facto coupling point (lock-step releases (§23)).

---

### 48. Growth Threshold Triggers & Tooling Investments

**Principle:** Map each growth threshold to a concrete investment — and *date* it before you hit it.

| Threshold | Investment trigger |
|---|---|
| **First release of service 2** | Log aggregation (§30) and CI/CD ready. |
| **Service 5** | Log aggregation done; choose tracing tool; create the *contract test* baseline (Pact). |
| **Service 10** | Begin ownership-model conversations; create the team's first internal RFC template (Monzo-style proposal). |
| **Service 15** | Service registry (Biz Ops-style); System Operability Score becomes a team-level KPI. |
| **Service 20–50** | Stand up a cross-team "architecture guild" / community of practice; reconsider Kubernetes / FaaS platform. |
| **Service 50+** | Established platform team; formal API lifecycle (deprecation policy, version sunset cadence). |

*Ref: Monolith To Microservices.md — "More Services, More Pain" (`page-222-0`).*

**Don't:**
- Don't perform these investments on the day you hit the threshold — they always take longer than the deal looks, and your delivery pipeline will be under stress.
- Don't adopt a tool because it's fashionable — adoption cost can exceed platform benefit.

---

### 49. Cost-of-Change Operationalisation

**Principle:** *"We can — and will — make mistakes, and we should embrace that. What we should also do, though, is understand how best to mitigate the costs of those mistakes."*

**Do:**
- Establish *where mistakes are cheapest*. Whiteboard > refactor > strangler > parallel run > API > data split > monolith-as-DB-pivot.
- Estimate reversibility at design time, not at incident time.
- For irreversible decisions, bring peers to the design review; for reversible, empower local teams.
  *Ref: Monolith To Microservices.md — "Easier Places to Experiment" (`page-71-0`).*
- Evaluate: *"the cost involved in moving code around within a codebase is pretty small. … Splitting apart a database, however, is much more work."*
  *Ref: Monolith To Microservices.md — "Easier Places to Experiment" (`page-71-0`).*
- Keep *type-2* (reversible) decisions inside the team boundary; pull type-1 (irreversible) decisions to architecture review boards.
  *Ref: Monolith To Microservices.md — "Cost of Change" (`page-69-0`).*

**Don't:**
- Don't agonise over reversible decisions as if they were irreversible — *"If you — or your organization — isn't used to that, you may find yourself falling into this trap, and progress will grind to a halt."*
  *Ref: Monolith To Microservices.md — "Cost of Change" (`page-69-0`).*
- Don't treat "small" as "easy" — a small irreversible step is more dangerous than a large reversible one.

---

### 50. Slack as the Diagnostic Mirror of Architecture

**Principle:** *"You can spot these problems much earlier if you have some sort of cross-team technical group."* — `page-244-0`. Slack channels, #proposals, public discussions are the cheap canary for organisational decay.

**Do:**
- Use a #proposals or RFC process to surface architectural decisions early. Monzo's free-form proposals with Slack alerts are the named example.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (`page-245-0`).*
- Treat #incident channels as after-action review fuel — never delete; never move past quickly.
  *Ref: Monolith To Microservices.md — "Robustness and Resiliency" (`page-247-0`).*
- Treat silence as a problem, not success — *"You'll typically find out about these things accidentally, after a passing comment you overhear at lunch, perhaps."*
  *Ref: Monolith To Microservices.md — "How Can This Problem Show Itself?" (Global vs. Local) (`page-244-0`).*
- Have face-to-face conversations for hard trade-offs (caching-staleness, decommissioning internal systems). *"When it comes to sharing important messages of this sort, face-to-face communication … will be significantly more effective."*
  *Ref: Monolith To Microservices.md — "Communicating the Change Vision" (`page-65-0`).*

**Don't:**
- Don't rely on ad-hoc information sharing once headcount grows past ~50. Formal cross-team rituals pay for themselves.

---

### 51. Choreography vs Orchestration Trade-off Decision Tree

**Principle:** Newman's bar: *"I'm very relaxed in the use of orchestrated sagas when one team owns implementation of the entire saga. … If you have multiple teams involved, I greatly prefer the more decomposed choreographed saga."*

**Do:**
- One team ownership → orchestration; multiple team ownership → choreography.
  *Ref: Monolith To Microservices.md — "Should I use choreography or orchestration?" (`page-219-0`).*
- Mix-and-match at **different scopes** — *"inside the boundary of the Warehouse service, when managing the packaging and dispatch of a package, we may use an orchestrated flow even if the original request was made as part of a larger choreographed saga."*
  *Ref: Monolith To Microservices.md — "Mixing styles" (`page-218-0`).*
- Always preserve a **way to know saga state** — orchestrator state table or choreographed projection pipeline.
- Propagate a **correlation ID** through every step — both styles need it.
  *Ref: Monolith To Microservices.md — "Choreographed sagas" (`page-217-0`).*
- For nested sagas, see Garcia-Molina et al.'s follow-on paper *"Modeling Long-Running Activities as Nested Sagas"* (Data Engineering 14 no. 1, 1991).
  *Ref: Monolith To Microservices.md — "Mixing styles" (`page-219-0`).*

**Don't:**
- Don't allow multiple teams to fight over the orchestrator — prefer choreography in that case.
- Don't over-rely on BPM tools — *"the central conceit … that nondevelopers will define the business process — has in my experience almost never been true."*
  *Ref: Monolith To Microservices.md — "BPM Tools?" (`page-216-0`).*
- Don't write orchestrators that absorb logic that should live in participants — *"If logic has a place where it can be centralized, it will become centralized!"* — `page-216-0`.

---

### 52. Resilience Engineering Mindset

**Principle:** John Allspaw distinguishes **robustness** (handle *known* variations) from **resilience** (organisational *adaptation* to unknown failures). Microservices amplify both.

**Do:**
- For robustness: deploy multiple instances, use multiple failure planes, retry with backoff, circuit-break on slow dependencies, cache where staleness is acceptable.
  *Ref: Monolith To Microservices.md — "How else could you do this?" (Robustness) (`page-55-0`).*
- For resilience: invest in chaos experiments *plus* an organisation that listens to them, gives teams space to fix root causes, and posts incident retrospectives.
  *Ref: Monolith To Microservices.md — "How else could you do this?" (`page-54-0`).*
- Hold post-incident reviews + write a record of what was learned. *"All too often I see organizations move on too quickly once the initial problem has been solved or worked around — only for those same problems to come back again some months later."* — `page-247-0`.
- Treat failures as data — *"the act of investing in more reliable hardware and software could likewise yield benefits."*
  *Ref: Monolith To Microservices.md — "How else could you do this?" (Robustness) (`page-54-0`).*

**Don't:**
- Don't equate microservices with robustness — they introduce *more* failure modes. *"Just spreading your functionality across multiple separate processes and separate machines does not guarantee improved robustness; quite the contrary — it may just increase your surface area of failure."*
  *Ref: Monolith To Microservices.md — "How else could you do this?" (Robustness) (`page-54-0`).*
- Don't underinvest in *operations* post-migration — manual ops processes were the cause of the British Airways 2017 outage.
  *Ref: Monolith To Microservices.md — "How else could you do this?" (`page-54-0`).*

---

### 53. Conway's-Law Bait: "Platform Teams" & Centralised Tooling

**Principle:** Newman's experience confirms that platform teams are the *enabling* layer for delivery teams, not a *replacement* for them. Their job is to *"help the delivery teams do the work"* via shared tooling, embed specialists, training.
  *Ref: Monolith To Microservices.md — "Shifting Structures" (`page-77-0`).*

**Do:**
- Identify platform-team candidates based on **cross-cutting pain** (CI/CD, infra provisioning, log aggregation, secret management, observability).
- Use *monorepo or polyrepo* decision to be a platform-team decision, not a per-delivery-team decision.
- Distinguish "Type 1 / irreversible" platform decisions (security model, audit logging) from "Type 2 / reversible" (default language, build tool).
- Match platform-engineering team size to a 6-to-12-month outlook — *"six months to a year is probably as far forward as you'll want to explore in detail."*
  *Ref: Monolith To Microservices.md — "Making a Change" (`page-82-0`).*

**Don't:**
- Don't let platform teams absorb delivery-team behaviour, or vice versa — both moves leave the organisation weaker.
- Don't adopt a "platform product manager" model without giving them DRI *authority* over the platform — otherwise they become roadmap-keepers with no decision power.

---

### 54. Strangler Fig Anti-Patterns (Named) You Can Spot in Code Review

These are the *typical* failure modes when teams attempt the strangler fig:

1. **The eager extraction** — extracting a service without a perimeter interceptable point. Symptoms: many callers still call the monolith; the new service is a shim. *Fix:* revert and extract bigger context first.
2. **The 501-stub forever** — service deployed at 501 Not Implemented for months. *Fix:* parallel-run the implementation; don't ship 501s to production.
3. **The "smart proxy"** — the proxy absorbs validation, transformation, orchestration. *Fix:* push it back into the service (§11).
4. **The silent feature drift** — service accepts redirects but has changed behaviour, no parallel-run validation. *Fix:* enforce feature-freeze (§40).
5. **The shared-state recovery** — proxy rewritten to share state with monolith. *Fix:* proxy *must* be stateless; stateful coordination belongs in the service.
6. **The ignored rollback** — flag set, never exercised. *Fix:* schedule quarterly rollback drills.

*Ref: Monolith To Microservices.md — "How It Works" (strangler) (`page-94-0`), "Changing Protocols" (`page-106-0`), "Other Protocols" (`page-97-0`).*

---

### 55. Working with the Monolith's Hidden Contracts

**Principle:** Every monolith has *implicit* contracts — the database column names, the protocol buffer field tags, the JSON shapes. Hidden contracts are the worst contracts because no-one owns them.

**Do:**
- Treat the existing monolith's data schema as a *de facto* API until you have actively migrated the consumers.
  *Ref: Monolith To Microservices.md — "The Database as a Public Contract" (`page-144-0`).*
- For every schema change, audit *who calls it* before you change it — network-traffic analysis is one tool of last resort.
  *Ref: Monolith To Microservices.md — "The Database as a Public Contract" (`page-144-0`).*
- Use *migrations as contracts*: FlywayDB-style versioned scripts in source control become the audit log of what changed when.
  *Ref: Monolith To Microservices.md — "A Note on Tooling" (`page-176-0`).*

**Don't:**
- Don't accept "no one else calls that table" without evidence. *"When you're relying on network analysis to determine who is using your database, you're in trouble."* — `page-144-0`.

---

### 56. Polyglot Persistence Without Polyglot Chaos

**Principle:** Microservices enable polyglot persistence, but the polyglot *must* be load-bearing — pick a DBMS *because* of the workload shape, not because of resume or hype. *"We've given all the money it's possible to give to Oracle, and it's still not enough."*

**Do:**
- Match database to data shape: relational for transactional aggregates; document for sparse / evolving shapes; graph for relationship-dense; key-value for state; wide-column for scale-out reads.
  *Ref: Monolith To Microservices.md — passim.*
- Audit licence and operations cost — the Australian bank's Oracle scale-out concern was a real procurement issue, not just a workload issue.
  *Ref: Monolith To Microservices.md — "Physical Versus Logical Database Separation" (`page-174-0`).*
- Use a *consistent* SQL dialect *within* a service's database to avoid inviting accidental coupling.
- When in doubt about MongoDB multi-doc transactions: *"MongoDB for many years supported ACID transactions around only a single document, which could cause issues if you wanted to make an atomic update to more than one document. (This has now changed with support for multidocument ACID transactions, which was released as part of Mongo 4.0.)"*
  *Ref: Monolith To Microservices.md — "ACID Transactions" (`page-202-0`).*

**Don't:**
- Don't pick a database because it's trendy; pick it for fit.
- Don't run multiple DBMSs for the same workload *in one company* unless a consolidation review has been done.

---

### 57. Observability Migration Specifics

**Principle:** Migration creates *transient* failure modes that production monitoring must surface. Existing alerting models often miss them.

**Do:**
- Add **migration-specific dashboards**: tracer-write drift, dual-write inconsistency, dual-read mismatch rate, parallel-run divergence rate.
- Adopt **correlation IDs at the inception of every migration** — the cost is too high to retrofit.
  *Ref: Monolith To Microservices.md — "Tracing" (`page-234-0`).*
- Build the **observability culture**: *"Don't assume you know the answers up front."*
  *Ref: Monolith To Microservices.md — "Toward observability" (`page-237-0`).*
- Tag every release with the **migration phase** so you can correlate regressions with migration activity (gray deploys, dual writes, etc.).

**Don't:**
- Don't fire tons of alerts during migration "just in case" — alert fatigue erodes trust in the alerts that matter.
- Don't retire old alerts until you've verified the new system has its own equivalent.

---

### 58. Twelve Takeaways from the Book *as a Unit* (compressed)

For those who only have 60 seconds:

1. **"Microservices are not the goal."** Three questions. Slider model. Reversible spectrum.
2. **Independent deployability** is the north star. Loose coupling, stable contracts.
3. **Use DDD** for boundaries. Event Storming to find them.
4. **Strangler Fig** is your default. **Branch by Abstraction** for the deep interior.
5. **Tracer Write** + reconciliation is your database migration pattern.
6. **Sagas** replace two-phase commits. Compensating transactions are *semantic* rollbacks.
7. **Progressive delivery** lets you deploy-and-learn. Canary → dark launch → parallel run.
8. **Kotter's 8-step change** model is for the people side, not just the technical.
9. **Strong code ownership** at scale; collective ownership *within* teams.
10. **"Reuse" is not a goal.** Time-to-market, scale-cost, robustness are.
11. **Schemas are contracts.** Pact + gradual rollout + co-existing contracts.
12. **Beware the destination anti-patterns** — distributed monolith is the worst of both worlds.

---

### 59. Migration as an Iterative Reductive Discipline

**Principle:** The migration is its own loop. Every extracted service is itself a *monolith* before the next extraction. Keep the same discipline at every step.

**Do:**
- Apply the prioritisation quadrant (§8) *after* every extraction — re-rank the remaining candidates using new learnings.
- Re-validate the domain model as services come out — *"You can — and should — continuously refine your domain model as you learn more, and keep it fresh to reflect new functionality as it's rolled out."*
  *Ref: Monolith To Microservices.md — "How Far Do You Have to Go?" (`page-72-0`).*
- After each extraction, **check the assumptions**: does the new service own the right aggregates? has the cost-benefit changed?
  *Ref: Monolith To Microservices.md — "A Combined Model" (`page-76-0`).*
- Treat the migration timeline as information *that must be re-checked*.

**Don't:**
- Don't freeze the migration plan against the original quadrant — the world changes; teams change; requirements change.
- Don't reverse-decision the migration at the first sign of trouble (that's also sunk-cost-in-reverse).

---

### 60. Migration Quality & Craftsmanship Lens

**Principle:** *"Software is made of feelings"* (Astrid Atkinson). Migration *quality* is about what people experience, not only what's measured.

**Do:**
- Measure both **quantitative** (cycle time, deployment frequency, MTTR) and **qualitative** (morale, ownership, autonomy).
  *Ref: Monolith To Microservices.md — "Qualitative Measures" (`page-87-0`).*
- Promote senior engineers to *teach* migration patterns internally — code review is the cheapest training vehicle.
- Use retrospectives: each migration phase should produce a written retrospective shared with the wider engineering org.

**Don't:**
- Don't treat *a passing metric* as *a finished migration* — many failed migrations still hit their cycle-time target.

---

### 61. The "Internal Monolith" Anti-Pattern

**Principle:** An extracted service that takes *too much* with it becomes a monolith with a new name.

**Do:**
- Audit each extraction 3–6 months later: is the service cohesive, or is it a polyglot-pile? Has the bounded context shifted under it?
- Apply the §6 / §21 (Database-per-Bounded-Context) test inside each new service — keep future extraction cheap.
- Use the **path-to-production mapping** from §1 to spot which extracted services are still needlessly sharing infra, code, or data.

**Don't:**
- Don't proudly call a too-large service "domain-driven" without evidence — bounded contexts can split further.

---

### 62. Migration as Organisational Training

**Principle:** *"All this means we need to develop a series of techniques that allow us to create new microservices and integrate them with our (hopefully) shrinking monolith, and get them shipped to production."* — Newman, `page-88-0`. The first migrations train the rest. Make the learning explicit.

**Do:**
- Run *internal post-mortems* on the first three migrations. Codify the lessons into runbooks ("our strangler process", "our data split playbook", "our saga conventions").
- Let *every* engineer participate in at least one migration — the skills are perishable; spread them.
- Create a *migration community of practice* before service 10 if possible.
  *Ref: Monolith To Microservices.md — "Potential Solutions" (Global vs. Local) (`page-245-0`).*

**Don't:**
- Don't centralise migration knowledge in one or two "migration engineers." That's a Conway's-law trap.
- Don't retire playbooks after the migration ends — they'll need them again as new services decompose further.

---

### 63. Migration Closure: Knowing When to Stop

**Principle:** Migration is "done" when the monolith is gone or has stabilised at a manageable size. Newman's closing message — *"Microservices are definitely not for everyone. But, hopefully, after reading this book, you'll not only a better sense of whether they are right for you, but also some ideas about how to get started on the journey."*

**Do:**
- Define a *done state* explicitly: zero functional lines remaining in the monolith (or, equivalently, monolith is a single deployment unit hosting only stable infrastructure glue).
- Plan the *monolith retirement ceremony* — removing the last instance of the old deploy is an actual milestone.
- Treat the *modular monolith* (§4) as a legitimate resting state, not a failure mode.
  *Ref: Monolith To Microservices.md — "A modular monolith?" (`page-92-0`).*

**Don't:**
- Don't declare migration done while the shared DB still exists (§37 incomplete migration).
- Don't assume the *right* number of microservices is fixed — expect continued evolution as the domain grows.

---

### 64. Migration Anti-Pattern Diagnostic — A Quick Triage

**Principle:** When a migration is in trouble, run this triage. Each column lists a likely root cause.

| Symptom | Likely root cause | Fix (cross-ref) |
|---|---|---|
| Cross-service changes dominate each release | Distribution boundaries wrong | §6 DDD re-model; §3 SnapCI lesson |
| Production outages on every release | Accidental breaking changes | §28 contract discipline + Pact |
| Latency spiked after extraction | Shared DB or smart pipe | §17, §11 smart-pipe warning |
| Dual-write inconsistency | Tracer-write reconciliation gap | §19 reconciliation + reconciliation query |
| Saga gets stuck mid-flight | Bad correlation-ID propagation | §25 correlation ID + projection pipeline |
| Team morale fell | Sunk-cost dynamic + huge mid-migration push | §39 regular checkpoints + qualitative measures |
| "We can't roll back" | Feature drift mid-migration | §40 feature freeze |
| Architecture drift across teams | No global standards | §34 architecture guild + proposal templates |
| New service acts like a mini-monolith | Service is too big | §6 re-decompose at aggregate level |

*Ref: Distributed across all sections of Monolith To Microservices.md.*

---

### 65. Quick-Reference Glossary

- **Microservice** — independently deployable service modelled around a business domain. (§2)
- **Monolith** — single unit of deployment. (§4)
- **Strangler Fig** — wrap-and-replace pattern. (§11)
- **Branch by Abstraction** — co-existence pattern for nested code. (§13)
- **Parallel Run** — run old and new side-by-side for verification. (§14)
- **Canary Release** — subset of users on new path. (§14)
- **Dark Launching** — new code deployed but invisible to users. (§14)
- **Decorating Collaborator** — proxy-based extension without changing monolith. (§15)
- **Change Data Capture (CDC)** — react to DB transactions. (§16)
- **Database View** — projected columns from underlying schema. (§18a)
- **Database Wrapping Service** — service fronting a DB to stop growth. (§18b)
- **DB-as-a-Service Interface** — exposed read-only DB. (§18c, §20)
- **Aggregate-Exposing Monolith** — monolith APIs expose aggregates to new services. (§18d)
- **Tracer Write** — dual-source-of-truth migration with eventual consistency. (§19)
- **Repository per Bounded Context** — split ORM layer by domain. (§21)
- **Database per Bounded Context** — separate schemas for each bounded context. (§21)
- **Monolith as Data Access Layer** — monolith exposes API for its own data. (§21)
- **Multischema Storage** — new tables live with new service even when monolith owns older data. (§21)
- **Split Table** — split a table across contexts. (§22)
- **Move Foreign-Key to Code** — DB-level FK becomes app-level join via API. (§22)
- **Saga** — long-lived transaction decomposed into sub-transactions. (§25)
- **Compensating Transaction** — semantic rollback for saga. (§25)
- **Orchestrated Saga** — central coordinator. (§25)
- **Choreographed Saga** — event-driven collaboration. (§25)
- **N-Version Programming** — multiple implementations for safety-critical consensus. (§14)
- **Verify Branch by Abstraction** — auto fallback when new impl fails. (§13)
- **Two-Phase Commit (2PC)** — avoid; deadlock-prone distributed transaction. (§24)
- **Biz Ops** — service registry with operability score (FT example). (§45n)
- **Synthetic Transaction** — scripted end-user behaviour for prod monitoring. (§30)
- **System Operability Score** — composite service-health metric (FT). (§45n)

---

### 66. Migration at the Edge — Tests, Tooling and Timelines

**Principle:** Newman names *few* calendar-bound commits to the migration; the emphasis is on *feedback-loop tightness*.

**Do:**
- Run end-to-end *under an hour* — *"Functional automated tests are typically used to give us feedback before deployment regarding whether or not our software is of sufficient quality to be deployed."*
  *Ref: Monolith To Microservices.md — "Test in production" (`page-236-0`).*
- Keep migration tool scripts (*schema migrations*, *proxy config* changes, *feature flags*) in the same source-control review pipeline as the rest of your code.
- Document a calendar milestone *only* when the team agrees externally — internally, the milestone is "next value unlock," not "Q4 demo."
  *Ref: Monolith To Microservices.md — "Reorganizing Teams" (`page-77-0`).*

**Don't:**
- Don't lock the migration plan into a year-long roadmap — *"being committed to a vision is important, but being overly committed to a specific strategy in the face of contrary evidence is dangerous."*
  *Ref: Monolith To Microservices.md — "Developing a Vision and Strategy" (`page-64-0`).*

---

### 67. Final Word (mine, framed in Newman's)

If you only internalise one or two things from the book, make them these:

> **Independent deployability**, achieved through **bounded-context ownership** and **stable service contracts**, with the **database ownership handover** as the hardest, slowest step — addressed via **tracer writes** and **dual-read/dual-write strategies**, **not** two-phase commits.

And the corollary on the human side:

> **Cross-functional product teams** exercising **strong code ownership**, embedded in a **Kotter-style change programme**, applying **incremental, reversible, rollback-able steps** from a domain model refined continuously — that's the migration that has the best chance of surviving contact with reality.

---

### 44. Modern Microservice-Friendly Tech Stack Hints (Newman's Picks)

**Principle:** Newman deliberately gives *tooling agnostic* advice, but names specific tools when they are foundational to a pattern:

- **Strangler proxy / load distribution** — NGINX (with Lua for custom routing); Envoy; AWS/GCP/Azure LBs.
- **Service mesh** — Istio, Linkerd, Square's Envoy mesh (`https://squ.re/2nts1Gc`).
- **Change Data Capture** — Debezium (Newman's default for the Tracer Write and the Database-as-a-Service-Interface patterns).
- **Migration feature toggles** — Pete Hodgson's patterns (`http://bit.ly/2m316zB`); LaunchDarkly / Split / Flagsmith.
- **Logging** — ELK; Humio (Newman's pick).
- **Tracing** — Jaeger (Newman's pick); Zipkin; OpenTelemetry.
- **Contract testing** — Pact (CDCs).
- **Schema-migration tool** — FlywayDB.
- **API gateway / mesh control plane** — Kong, Apigee, Istio, Linkerd.
- **Saga / orchestration** — Camunda, Zeebe (open source, developer-friendly).
- **FaaS** — AWS Lambda, Azure Cloud Functions.
- **Secret store** — HashiCorp Vault (per-actor, short-lived DB credentials for the bank scenario).
- **Schema visualisation** — SchemaSpy.
- **Synthetic-transaction framework** — Atomist (Sam's former employer).

*Ref: Monolith To Microservices.md — passim; particularly "And service meshes" (`page-108-0`), "Implementing a Mapping Engine" (`page-151-0`), "Implementing Change Data Capture" (`page-137-0`), "Tracing" (`page-234-0`), "Database Wrapping Service" (`page-144-0`).*

---

## Anti-Patterns & Common Mistakes (Summary Index)

- **Distributed Monolith** — see §2, §37.
- **Big-Bang Rewrite** — see §7, §37.
- **Incomplete Migration** (split code, keep shared DB forever) — see §21, §37.
- **Premature Decomposition** (unclear domain) — see §3, §6.
- **Smart Pipe / Dumb Endpoint violation** — see §11.
- **Cargo-cult Spotify/Kubernetes/Kafka** — see §10, §32, §37.
- **Sunk-Cost / Concorde Fallacy** — see §37, §39.
- **Collective Ownership at >100 devs** — see §27.
- **CDCs / Strong Ownership Rejection** — see §27, §33.
- **BPM tools for non-tech authors** — *"the central conceit … has in my experience almost never been true."* `page-216-0`.
- **Two-Phase Commit / Distributed Transactions** — see §24.
- **Reuse as primary goal** — see §1.
- **Behavioural changes during migration** — see §40.
- **Shared library as silent lock-step release** — see §23.
- **Auto-incrementing cross-service counters** — see §19.
- **Triggering real customer side-effects in test-in-prod** — see §30.
- **Sharing production DB credentials across 20 apps** — see §18 (bank story).
- **JDBC FROM monolith INTO the new microservice's schema** instead of via API — see §18e.
- **Long-lived source branches** instead of branch by abstraction — see §13.
- **Hand-rolled network proxy** — see §11.

---

## Decision Heuristics / Checklists

### When to consider a Modular Monolith (§4)
- Domain still shifting (startups, internal tools).
- Operational maturity for distributed systems not yet present.
- Number of developers < ~10.
- You have found seams (DDD) but can't yet justify service overhead.

### When to consider Microservices (§1, §3)
- Clear bounded contexts exist (DDD).
- Cross-functional teams can own services end-to-end.
- Greenfield deployment platform (Kubernetes / FaaS) available.
- Need any of: independent deployability, team autonomy, scale-cost effectiveness, robustness, polyglot tech.

### When to use each Migration Pattern
| Pattern | When |
|---|---|
| **Strangler Fig (§11)** | Perimeter call (HTTP, FTP, message). Functionality is naturally interceptable. |
| **Branch by Abstraction (§13)** | Deeply nested internal functionality; many in-monolith callers. |
| **Parallel Run / Scientist (§14)** | High-risk logic (credit pricing, EMR, loyalty points). |
| **Decorating Collaborator (§15)** | Can't change the monolith; new behaviour attaches to existing responses. |
| **Change Data Capture (§16)** | React to data state changes; can't intercept, can't decorate. |
| **Tracer Write (§19)** | Data ownership handover with rollback safety. |
| **Aggregate-Exposing Monolith (§18d)** | New service needs data still owned by monolith. |

### When to use each Data Pattern
| Pattern | When |
|---|---|
| **Database View (§18a)** | Read-only static / slowly-changing reference; keep schema stable for legacy readers. |
| **Database Wrapping Service (§18b)** | Stop schema growth; can't yet fully decompose; e.g. entitlements schema. |
| **DB-as-a-Service Interface (§20)** | Toolchains (Tableau) need SQL access to service-owned data. |
| **Tracer Write / Synchronize-in-Application (§19)** | Source-of-truth handover with rollback safe. |
| **Repository per Bounded Context (§21)** | First step before split. |
| **Database per Bounded Context (§21)** | Hedge for future microservice extraction (also good in modular monoliths). |
| **Multischema Storage (§21)** | Brand-new tables added by extracted service live alongside legacy in-monolith reads. |
| **Monolith as Data Access Layer (§21)** | New service can avoid direct DB access by calling monolith endpoints. |
| **Split Table (§22)** | Single table spans multiple bounded contexts. |
| **Move Foreign-Key to Code (§22)** | Cross-service relationship. Default: don't allow deletion + handle gracefully. |
| **Static Reference Data — Library / Schema / Service (§23)** | Polyglot answer; pick by service-creation cost. |

### Saga Style Heuristic (§25)
- One team owns the whole saga → **orchestrated**.
- Multiple teams → **choreographed**.
- Always propagate a **correlation ID**.
- Prefer **forward recovery** for transient errors; reserve **compensating transactions** for semantic rollback.

---

## Key Takeaways (the 12 reusable rules)

1. **"Microservices are not the goal."** Start with the three questions; use the slider model; track outcomes.
2. **Independent deployability** is the *defining* characteristic. Everything else can be debated.
3. **"Chip away at the block of marble."** *Big-bang rewrites are dangerous.*
4. **Domain-Driven Design** is the source of service boundaries. Use Event Storming to find them collectively.
5. **The database is the hardest part.** Sequence the split deliberately (code-first / schema-first) and never stop halfway.
6. **Strangler Fig** is the workhorse pattern; **Branch by Abstraction** is for nested code; **Tracer Write** is the schema companion; **Sagas** replace two-phase commit.
7. **People matter as much as technology.** Use Kotter's 8 steps; cross-functional product teams; align ownership to service ownership.
8. **Make decisions on a reversibility spectrum** (Bezos Type 1 vs Type 2). Make reversible decisions quickly.
9. **Deploy ≠ release.** Use progressive delivery (canary, dark launch, parallel run) to validate in production without risk.
10. **Reorder saga steps to simplify rollbacks.** Compensating transactions are *semantic* rollbacks, not literal ones.
11. **At scale, plan for the growing pains** (ownership at scale, breaking changes, reporting, monitoring, dev experience, global vs local optimisation, robustness, orphaned services).
12. **Beware the anti-patterns.** Distributed monoliths, big-bang rewrites, premature decomposition, incomplete migrations, smart pipes, sunk-cost spirals, reuse-by-itself, monolithic UIs, shared databases.

---

## Cross-References

- Related (same author, same ecosystem):
  - **[Building Microservices.md](./Building_Microservices.md)** — companion volume; covers greenfield microservice design (technology choices, communication, deployment, testing, observability, security, scaling, UI).
  - **[Team_Topologies.md](./Team_Topologies.md)** — Pais & Skelton; complementary organisational design primer for the team-structure changes discussed in §9, §10, §27.
- Adjacent:
  - **[Software_Architecture_Hardparts.md](./Software_Architecture_Hardparts.md)** — Richards & Ford; trade-off analysis patterns for structural decomposition.
  - **[Software_Architecture_Patterns.md](./Software_Architecture_Patterns.md)** — foundational patterns referenced from a monolith decomposition viewpoint.
  - **[Crafting_Engineering_Strategy.md](./Crafting_Engineering_Strategy.md)** — Larson; complements the §9 Kotter section on the people side.
  - **[Fundamentals_of_Software_Architecture.md](./Fundamentals_of_Software_Architecture.md)** — Richards; broader context for the *modular monolith vs. microservices* trade-off (§4, §3).
  - **[Learning_Domain_Driven_Design.md](./Learning_Domain_Driven_Design.md)** — Khononov; supporting primer for §6.
  - **[Domain_Driven_Design_with_Golang.md](./Domain_Driven_Design_with_Golang.md)** — code-level companion for bounded-context identification (§6).
  - **[Building_An_Event-Driven_Data_Mesh.md](./Building_An_Event-Driven_Data_Mesh.md)** — for the event-driven aspect of choreographed sagas (§25) and CDC (§16).
  - **[Communication_Patterns.md](./Communication_Patterns.md)** — Greenfield messaging patterns referenced from §16, §25.
  - **[Observability_Engineering.md](./Observability_Engineering.md)** — deeper coverage of §30 monitoring/tracing.
  - **[Designing_Distributed_Systems.md](./Designing_Distributed_Systems.md)** — broadens §5 coupling / §11 strangler / §25 saga discussions into the cloud-native idiom.
  - **[Software_Architecture_Metrics.md](./Software_Architecture_Metrics.md)** — for §39 measurement discipline.
  - **[Engineering_Resilient_Systems_on_AWS.md](./Engineering_Resilient_Systems_on_AWS.md)** — for §35 resilience patterns.
  - **[Mastering_Api_Architecture.md](./Mastering_Api_Architecture.md)** — API design underpinnings for §11, §28 contract management.
  - **[Continuous_API_Management.md](./Continuous_API_Management.md)** — API lifecycle parallels for §28.
- Topic index: **[../INDEX.md](../INDEX.md)**

### Bibliography (subset referenced in this file)
- Hector Garcia-Molina & Kenneth Salem, "Sagas," *ACM Sigmod Record* 16 no. 3, 1987.
- Martin Fowler, "Strangler Fig Application" (`http://bit.ly/2p5xMKo`) and "Reporting Database" (`http://bit.ly/2kWW9Ir`).
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004.
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2003.
- Vaughn Vernon, *Domain-Driven Design Distilled*, Addison-Wesley, 2016.
- Alberto Brandolini, *Introducing EventStorming* (Leanpub).
- John Kotter, *Leading Change*, HBR Press, 1996.
- Jeff Bezos, *Letter to Amazon Shareholders (2015)*.
- Frederick Brooks, *The Mythical Man-Month*, 20th Anniversary Edition, 1995.
- Larry Constantine & Edward Yourdon, *Structured Design*, 1979.
- David Parnas, "On the Criteria to be Used in Decomposing Systems into Modules," 1972.
- Pat Helland, "Life Beyond Distributed Transactions," *acmqueue* 14 no. 5.
- Cindy Sridharan, *Distributed Systems Observability*, O'Reilly, 2018.
- Jez Humble & David Farley, *Continuous Delivery*, Addison-Wesley, 2010.
- Manuel Pais & Matthew Skelton, *Team Topologies*, IT Revolution, 2019.
- Gene Kim et al., *The DevOps Handbook*, IT Revolution, 2016.
- Pete Hodgson, "Feature Toggles (aka Feature Flags)" (`http://bit.ly/2m316zB`).
- Steve Smith, "Verify Branch By Abstraction" (`http://bit.ly/2mLVevz`).
- Snow Pettersen, "The Road to an Envoy Service Mesh" (Square, `https://squ.re/2nts1Gc`).
- Kief Morris, *Infrastructure as Code*, O'Reilly, 2016.
- Michael Nygard, *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017.
- Christian Bird et al., "Don't Touch My Code! Examining the Effects of Ownership on Software Quality."
- Kresten Thorup, "Riak on Drugs (and the Other Way Around)."
- Daniel Bryant on Netflix/Square data migrations (`http://bit.ly/2m1CwLP`).
- Christiane Bird et al., ownership research (`http://bit.ly/2p5RlT1`).
- Henrik Kniberg & Anders Ivarsson, "Scaling Agile @ Spotify" (2012).
- Jessica Kerr, "Copy the questions, not the answers."
- Astratech, Randy Shoup, Graham Tackley, Erik Doornenburg, Marcin Zasepa, Pete Hodgson, Martin Fowler, Stefan Schrass, Derek Hammer — case-study contributors.

---

### 68. Migration Recipe Cards (Pull-Out Cards)

A condensed at-a-glance summary of every pattern in the book. Keep these printed on the wall during planning sessions.

#### Recipe — Strangler Fig via HTTP Reverse Proxy (§11)
```
0. Identify a slice cleanly reachable at the perimeter (HTTP / message / FTP).
1. Stand up an HTTP reverse proxy (NGINX) in front of the monolith; let it pass through; measure latency.
2. Build the new service: handle the same routes, return 501 Not Implemented; deploy to prod.
3. Implement equivalent functionality in the new service; deploy.
4. Switch the proxy to redirect the route(s); proxy config is the switchback path.
5. Once confident, remove the old functionality from the monolith.
```

#### Recipe — Branch by Abstraction (§13)
```
0. Identify deeply nested functionality with many in-monolith callers.
1. Create an interface (or extraction) wrapping the functionality — the seam.
2. Refactor existing callers to invoke the new abstraction (small, separate commits).
3. Add a new implementation that proxies to the new microservice; both impls live in the source tree.
4. Use a feature flag to switch the active implementation; verify; flag-off rollback is trivial.
5. Clean up: delete the old implementation; remove feature flag; keep or drop the abstraction.
```

#### Recipe — Tracer Write for Data (§19)
```
0. Decide which data moves with which service.
1. Snapshot-bulk-copy the data into the new service's schema (via the new service's API).
2. CDC-process changes since snapshot to catch the new service up.
3. Deploy callers to dual-write (old schema + new service API). Reads stay from old schema.
4. Once dual-writes are clean, switch reads to the new service's schema. Continue dual-writing.
5. Drop the old schema. Reconciliation queries must run throughout.
```

#### Recipe — Saga Implementation (§25)
```
0. Identify the cross-service long-lived transaction.
1. Break into a sequence of sub-transactions; each fits inside one service's ACID scope.
2. Decide orchestrator or choreography (see §51).
3. Pick a recovery mode per step: backward (compensating) vs. forward (retry).
4. Reorder steps if needed so likely-to-fail steps come first (smaller blast radius).
5. Wire correlation IDs everywhere; build the saga-state projector for visibility.
```

#### Recipe — Oracle Database-as-Public-Contract Recovery (§18a)
```
0. Recognise that the monolith's schema is a de-facto API (§55).
1. Inventory all callers of the schema (network analysis, peer queries, source-control search).
2. Issue per-actor credentials via a secret store (Vault).
3. Stop allowing new direct DB consumers.
4. For each existing consumer, project a view into a dedicated schema; redirect consumers.
5. Move writers first (smallest set), readers later.
```

#### Recipe — Modular Monolith Refactor (§4)
```
0. Identify bounded contexts (DDD, Event Storming).
1. Group code by bounded context, even within the monolith.
2. Split the persistence layer per bounded context (§21 Repository per Bounded Context).
3. Split schema per bounded context (§21 Database per Bounded Context) — hedge.
4. Stop the bleeding; let the team grow into the new boundaries.
5. Re-evaluate quarterly whether microservice extraction would now be helpful.
```

#### Recipe — Saga Recovery Decision (§25)
```
if failure_mode in {transient, retryable}:
    forward_recovery()
elif failure_mode in {semantic, expensive}:
    compensating_transaction()
else:
    human_intervention()
```

#### Recipe — Reporting Post-Migration (§29)
```
0. Identify reporting stakeholders (BI, finance, ops).
1. Define target reporting schema — may differ from internal service schemas.
2. Each service pushes its data via CDC or programmatic copy.
3. Surface `last_updated_at` for freshness hints.
4. Document drift between service-internal and reporting-exposed shapes.
5. Rebuild any monolith-shaped reports against the new reporting DB iteratively.
```

#### Recipe — Branch-by-Abstraction-as-Fallback (§13)
```
feature_flag("use_new_path") = false   # default
if new_path.attempt():
    use_new_path
else:  # automatic fallback
    use_old_path
log_outcome_to_correlation_id
```

---

### 69. Final Map — Which Chapter Covers What

| Book chapter | Best-practices section(s) |
|---|---|
| Ch 1 — Just Enough Microservices | §2, §5, §6 |
| Ch 2 — Planning a Migration | §1, §3, §8, §9, §10, §39 |
| Ch 3 — Splitting the Monolith | §11, §12, §13, §14, §15, §16, §40, §54 |
| Ch 4 — Decomposing the Database | §17, §18a–e, §19, §20, §21, §22, §23, §24, §25, §55, §56 |
| Ch 5 — Growing Pains | §26, §27, §28, §29, §30, §31, §32, §33, §34, §35, §36, §48 |
| Ch 6 — Closing Words | §37, §39, §63 |
| Case studies (in-line) | §45a–§45t |
| Bibliography (named works) | §67 + Bibliography below |

---

### 70. Closing Notes for the Migrating Architect

- The book is a *toolkit*, not a *prescription*. The right approach depends on context.
- Trust the reversibility heuristic before you trust any roadmap.
- The two most durable lessons:
  1. **"Microservices are not the goal."** (Goal = better business outcomes.)
  2. **"It's production that counts."** (Most lessons happen after deploy.)
- Every team gets to define its own *right* migration plan — but not its own *success criteria*. Those should be public.

*Ref: Monolith To Microservices.md — "Closing Words" (`page-252-0`).*

