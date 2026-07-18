# Enabling Microservice Success
**Author:** Sarah Wells
**Topic tags:** `#architecture` `#general`
**Language focus:** Org / people / process (technology-agnostic; references Kubernetes, Heroku, AWS, Backstage)
**Sources:** `markdown_output/Enabling Microservice Success/Enabling Microservice Success.md` · `summaries/Enabling_Microservice_Success.md`

## TL;DR
Sarah Wells's *Enabling Microservice Success* is the *people + process +
governance + observability* companion to the technical microservices canon
(her foreword by Sam Newman makes this explicit). The thesis: microservices
are an **organizational pattern as much as a technical one**. The five
prerequisites (CI/CD, automated testing, IaC, observability, team autonomy)
must exist *before* adoption. Decompose around **business capabilities** using
DDD; use the **ISH checklist** (Independent / Stateless / Helpful) to
evaluate boundaries. Build a **paved road** that makes best practices the
default, adopt **"you build it, you run it"** with shared on-call, and
govern via a **Tech Governance Group** plus automated **guardrails** rather
than policy documents. The Financial Times (FT) case study (where the
author built her first microservice architecture in 2013) anchors the
recommendations: ~2,500 releases/year after moving to CD + microservices,
12× before.

---

## Best Practices by Topic

### Microservices Are an Organizational Pattern First

**Principle:** "Microservices are an organizational pattern as much as a
technical one." Conway's Law + team topology + autonomy + motivation
matter as much as any technology choice.

**Do:**
- Use Newman's definition: *"independently releasable services that are
  modeled around a business domain."*
  *Ref: Enabling Microservice Success.md — "Understanding Microservices" (`page-30-0`).*
- Map the *Lewis & Fowler 2014* characteristics to your own context:
  suite of services / own process / lightweight communication / built
  around business capabilities / independently deployable / small /
  bare-minimum centralized management / heterogeneous.
  *Ref: Enabling Microservice Success.md — "Defining the Microservices Architectural Style" (`page-31-0`).*

**Don't:**
- Don't default to microservices. **A monolith should be your first
  choice** for small teams. Use the modular monolith as a stepping
  stone.
  *Ref: Enabling Microservice Success.md — "The Monolith" (`page-35-0`).*
- Don't pick microservices to follow a trend — adopt when you have
  multiple teams needing independence, different scale needs, or different
  technology stacks.
  *Ref: Enabling Microservice Success.md — "When Microservices Make Sense" (`page-33-0`).*

---

### Lay the Groundwork First (5 Prerequisites)

**Principle:** *Without these five, microservices become an operational
nightmare.* Order matters: CI/CD, automated testing, IaC, observability,
team autonomy.

**Do:**
- **CI/CD** — automated build + test + deploy. Manual deployment at 10×/day
  doesn't work.
  *Ref: Enabling Microservice Success.md — "Continuous Delivery" (`page-41-0`).*
- **Automated testing** — at *every* level: unit, integration, contract.
  *Ref: Enabling Microservice Success.md — "Prerequisites for Success" (`page-39-0`).*
- **Infrastructure as code** — even private clouds need IaC to avoid
  *configuration drift* over time.
  *Ref: Enabling Microservice Success.md — "Infrastructure as Code" (`page-39-0`).*
- **Observability** — logs, metrics, traces; *before* you have 100
  services to debug.
  *Ref: Enabling Microservice Success.md — "Observability" (`page-47-0`).*
- **Team autonomy** — authority *and* capability to design, build,
  deploy, and operate.
  *Ref: Enabling Microservice Success.md — "Team autonomy" (`page-39-0`).*
- Treat servers as **cattle, not pets** — name them by purpose, terminate
  and replace when sick.
  *Ref: Enabling Microservice Success.md — "The Public Cloud" (`page-42-0`).*
- Move from manual Saturday-morning deploys to *continuous delivery*.
  The FT moved from 12 releases/year to ~2,500/year (~10/working day).
  *Ref: Enabling Microservice Success.md — "Continuous Delivery" (`page-41-0`).*
- Lean on the *cloud provider* for undifferentiated heavy lifting
  (Werner Vogels): server management, load balancing, patching.
  *Ref: Enabling Microservice Success.md — "Making your choice" (`page-48-0`).*
- Use **boring technology** (Dan McKinley): spend innovation tokens
  wisely. Adopt Kubernetes via managed services, not DIY.
  *Ref: Enabling Microservice Success.md — "Containers / Orchestration" (`page-44-0`).*

**Don't:**
- Don't adopt microservices without CI/CD, automated testing, IaC, and
  observability — these are *prerequisites*, not afterthoughts.
  *Ref: Enabling Microservice Success.md — "Before You Start" (`page-38-0`).*
- Don't build your own container orchestrator unless you're a pioneer
  willing to spend the innovation token.
  *Ref: Enabling Microservice Success.md — "Containers" (`page-44-0`).*

---

### Decompose Around Business Capabilities (DDD + ISH)

**Principle:** Services should be modeled around business domains, not
technical layers.

**Do:**
- Apply **DDD**: bounded contexts, ubiquitous language, context mapping.
  *Ref: Enabling Microservice Success.md — "Understanding Your Domain" (`page-39-0`).*
- Use **Event Storming** to discover bounded contexts in the codebase —
  identify events, group into aggregates, group into contexts.
  *Ref: Enabling Microservice Success.md — "Understanding Your Domain" (`page-39-0`).*
- Choose between fracture planes by *value of decomposition vs. difficulty*:
  - **Business capability** (DDD) — most common, recommended.
  - **Subdomain** — within a business domain.
  - **Data** — co-locate services that change the same data.
  - **Location** — geographic / organizational.
  - **Technology** — different stacks can drive decomposition.
  *Ref: Enabling Microservice Success.md — "Fracture Planes" (`page-116-0`).*
- Apply the **ISH checklist** to every candidate service:
  - **I**ndependent — can be developed, deployed, operated independently?
  - **S**tateless — minimal state between requests?
  - **H**elpful — useful unit of work?
  *Ref: Enabling Microservice Success.md — "The ISH Checklist" (`page-122-0`).*
- Use **Nick Tune's Bounded Context Canvas** to design each context
  (naming, responsibilities, public interfaces, dependencies).
  *Ref: Enabling Microservice Success.md — "Bounded Context Canvas" (`page-127-0`).*
- Migrate incrementally with the **Strangler Fig pattern**.
  *Ref: Enabling Microservice Success.md — "Incremental Migration" (`page-40-0`).*
- Migrate first to a **modular monolith** if appropriate — same domain
  boundaries, single deployable.
  *Ref: Enabling Microservice Success.md — "Modular Monoliths" (`page-37-0`).*

**Don't:**
- Don't split a table across services when the *same* column is updated
  by multiple bounded contexts. Pick the *one* domain that owns it.
  *Ref: Enabling Microservice Success.md — "Data Considerations" (`page-128-0`).*

---

### Build Effective Teams (Team Topologies + Pink)

**Principle:** Cross-functional, long-lived, autonomous teams of 5–9
people, motivated by **autonomy / mastery / purpose** (Pink).

**Do:**
- Use **Team Topologies**:
  - **Stream-aligned** — owns a flow of work end-to-end.
  - **Enabling** — helps stream-aligned teams adopt new capabilities.
  - **Complicated-subsystem** — handles complex technical problems.
  - **Platform** — builds internal platforms for stream-aligned teams.
  *Ref: Enabling Microservice Success.md — "Team Size and Structure" (`page-132-0`).*
- Size teams at **5–9 people** (Dunbar / two-pizza).
  *Ref: Enabling Microservice Success.md — "Team Size and Structure" (`page-132-0`).*
- Make teams **cross-functional** — full stack (dev, test, ops) + product
  + UX.
  *Ref: Enabling Microservice Success.md — "Cross-Functional Teams" (`page-138-0`).*
- Keep teams **long-lived** — trust and psychological safety take time.
  *Ref: Enabling Microservice Success.md — "Long-Lived Teams" (`page-140-0`).*
- Organize into **groups of 50–150** (Dunbar's number) for cross-team
  coordination, 24/7 rotas, shared learning.
  *Ref: Enabling Microservice Success.md — "Part of a Group" (`page-141-0`).*
- Invest in **skills development**: communities of practice, 10% time,
  secondments, external training, internal tech talks.
  *Ref: Enabling Microservice Success.md — "Skills Development" (`page-143-0`).*
- Use **secondments** to break down silos.
  *Ref: Enabling Microservice Success.md — "Secondments" (`page-147-0`).*
- Apply Dan Pink's three motivation pillars:
  - **Autonomy** — freedom to decide how.
  - **Mastery** — opportunities to develop skills.
  - **Purpose** — understand why the work matters.
  *Ref: Enabling Microservice Success.md — "Dan Pink's Motivation Framework" (`page-135-0`).*

---

### Communication Patterns Across Teams

**Principle:** Pick sync vs async deliberately; use OpenAPI + contract
testing for sync; use events for cross-domain reactivity.

**Do:**
- Use **synchronous (REST, gRPC)** when the caller needs an immediate
  result and the operation is short. *Accept the temporal coupling.*
  *Ref: Enabling Microservice Success.md — "Synchronous vs. Asynchronous Communication" (`page-178-0`).*
- Use **asynchronous (queues, event streams)** when the operation is
  long-running, you want decoupling, or you want to buffer against
  downstream failures.
  *Ref: Enabling Microservice Success.md — "Synchronous vs. Asynchronous Communication" (`page-178-0`).*
- For APIs: clear, consistent naming, version from day one, document via
  OpenAPI/Swagger, design for backwards compatibility.
  *Ref: Enabling Microservice Success.md — "API Design" (`page-185-0`).*
- Adopt **consumer-driven contract testing** (Pact) — the consumer
  defines its expectations; the provider verifies it can meet them.
  Catches breaking changes before production.
  *Ref: Enabling Microservice Success.md — "Contract Testing" (`page-190-0`).*
- Use **event-driven** communication: events represent "something that
  happened in the business domain"; services publish state changes,
  subscribers react.
  *Ref: Enabling Microservice Success.md — "Event-Driven Communication" (`page-195-0`).*
- Use **feature flags** to separate deployment from release — enables
  A/B testing, gradual rollouts, kill switches.
  *Ref: Enabling Microservice Success.md — "A/B Testing and Feature Flags" (`page-197-0`).*

---

### Team Autonomy (with Responsibility)

**Principle:** "Autonomy does not mean a free-for-all." Teams can choose
their stack, design their APIs, deploy when ready — *and* they own
security, operability, cost, support, and adherence to guardrails.

**Do:**
- Grant teams the freedom to choose: technology stack, API design, data
  model, deployment schedule.
  *Ref: Enabling Microservice Success.md — "What Autonomy Means" (`page-230-0`).*
- Hold teams responsible for: building secure systems, making services
  operable, controlling costs, supporting in production, following
  guardrails.
  *Ref: Enabling Microservice Success.md — "Responsibilities That Come with Autonomy" (`page-233-0`).*
- Build a **paved road / golden path** that makes the right thing the
  easy thing. *Optional but so compelling that most teams choose it.*
  *Ref: Enabling Microservice Success.md — "The Paved Road" (`page-237-0`).*
- Bake guardrails into templates and tools — security scanning, logging,
  healthchecks are included by default.
  *Ref: Enabling Microservice Success.md — "Automating Guardrails" (`page-411-0`).*
- Distribute **architecture decision-making**:
  - Every team does architecture within their domain.
  - Cross-cutting decisions go through the **Tech Governance Group** (TGG).
  - Use **ADRs** for important decisions.
  *Ref: Enabling Microservice Success.md — "Architecture as Guidance" (`page-241-0`).*

---

### Developer Experience (DevEx)

**Principle:** Poor DevEx → slow delivery, frustration, shadow IT,
inconsistency. Good DevEx is a competitive advantage.

**Do:**
- Focus on four key areas: **onboarding**, **documentation**,
  **tooling**, **internal platform**.
  *Ref: Enabling Microservice Success.md — "Key Areas of DevEx" (`page-278-0`).*
- **Consolidate documentation** in one place with a consistent
  template. The FT initially had docs scattered across GitHub, Google
  Sites, Confluence, wikis.
  *Ref: Enabling Microservice Success.md — "Documentation" (`page-285-0`).*
- Form an **Engineering Enablement group** — a single team that owns
  build/deploy pipelines, production support tooling, monitoring. Reduces
  duplication; aligns responsibilities.
  *Ref: Enabling Microservice Success.md — "Building an Engineering Enablement Group" (`page-291-0`).*
- Realize team boundaries to fix gaps — e.g., monitoring + observability
  split across two teams → realign.
  *Ref: Enabling Microservice Success.md — "Aligning Responsibilities" (`page-288-0`).*

---

### "You Build It, You Run It"

**Principle:** Teams that build a service must operate it in production.
Shared on-call, runbooks, incident response.

**Do:**
- Apply Amazon's "you build it, you run it" — teams feel the pain of
  poor operability and build operable systems.
  *Ref: Enabling Microservice Success.md — "'You Build It, You Run It'" (`page-308-0`).*
- Share on-call across **groups of teams** to make 24/7 sustainable for
  small teams. *Ref: Enabling Microservice Success.md — "On-call burden" (`page-320-0`).*
- Run a **blameless postmortem** after every incident.
  *Ref: Enabling Microservice Success.md — "Run a blameless postmortem" (`page-332-0`).*
- Maintain **runbooks** so someone else could fix a problem with the
  service. Score runbook completeness automatically (FT's SOS tool).
  *Ref: Enabling Microservice Success.md — "Maintaining Documentation" (`page-641-0`).*
- For incident management: **assign an incident manager**, **create a
  public incident channel**, **communicate regularly via status pages**,
  **take breaks** during long incidents.
  *Ref: Enabling Microservice Success.md — "Incident Management Process" (`page-330-0`).*
- Automate mitigations: **failover**, **scale up**, **roll back**.
  *Ref: Enabling Microservice Success.md — "Mitigation Strategies" (`page-338-0`).*
- Make services **start fast** (12-factor) and **handle SIGTERM
  gracefully** (finish in-flight, release resources, then exit; for queue
  consumers return jobs to the queue).
  *Ref: Enabling Microservice Success.md — "Fast Startup and Graceful Shutdown" (`page-548-0`).*
- **Alert on SLOs / business outcomes** rather than individual service
  health; alert only at the layer closest to the customer (avoid alert
  cascades).
  *Ref: Enabling Microservice Success.md — "Getting Alerting Right" (`page-604-0`).*
- Use healthchecks for **human visibility** and diagnostics, *not* to
  trigger restarts. Return HTTP 200 even on failure to avoid cascading
  restarts.
  *Ref: Enabling Microservice Success.md — "Healthchecks" (`page-613-0`).*

**Don't:**
- Don't create small teams with solo 24/7 on-call — unsustainable.
  *Ref: Enabling Microservice Success.md — "On-call burden" (`page-320-0`).*
- Don't use healthchecks as a *restart trigger* — that creates cascading
  restarts.
  *Ref: Enabling Microservice Success.md — "Healthchecks" (`page-613-0`).*

---

### Service Catalog, Ownership, Guardrails (Knowing What You Have)

**Principle:** At 100+ services, you can't know what's running without a
catalog. *Own it or it dies.*

**Do:**
- Adopt a **service catalog** (Backstage from Spotify, OpsLevel, Cortex — or
  build one like the FT's *Biz Ops*).
  *Ref: Enabling Microservice Success.md — "Service Catalog" (`page-363-0`).*
- Capture in the catalog: GitHub repos + teams, cloud accounts/regions/
  resources, DNS zones, production incidents, API gateway keys,
  dependencies. Each new piece enables more interesting queries and
  automates governance.
  *Ref: Enabling Microservice Success.md — "Types of Information to Track" (`page-378-0`).*
- Require every service to have a *clear owner team*. Use CODEOWNERS +
  source-control permissions.
  *Ref: Enabling Microservice Success.md — "Ownership" (`page-373-0`).*
- Automate **guardrails**, don't just document them. The FT's 16-step
  guardrail (Buy vs Build, Procurement, Security, Accessibility, Runbooks,
  Tier, Decommissioning, etc.) lives in templates, pipelines, and tools
  so teams follow the rules by default.
  *Ref: Enabling Microservice Success.md — "Guardrails and Policies" (`page-389-0`).*
- Establish a **Tech Governance Group (TGG)** for cross-cutting decisions:
  - Lightweight two-page proposal (Authors, Need, Proposed Approach,
    Known Limitations and Risks, Impact, Costs, Benefits,
    Alternatives including "Do Nothing").
  - Circulate via Slack + GitHub in advance.
  - Endorse rather than re-decide; keep a public log of decisions.
  *Ref: Enabling Microservice Success.md — "Tech Governance Group (TGG)" (`page-418-0`).*
- Track **technology maturity** (Innovators → Early Adopters → ... or
  Wardley's Genesis → Custom → Product → Commodity) to inform adoption.
  *Ref: Enabling Microservice Success.md — "Technology Lifecycle" (`page-428-0`).*

---

### Testing in a Microservice World

**Principle:** Minimize E2E; rely on the testing pyramid + contract tests +
testing in production.

**Do:**
- Follow the **testing pyramid**: lots of unit, fewer integration, very
  few E2E.
  *Ref: Enabling Microservice Success.md — "The Testing Pyramid" (`page-451-0`).*
- Use **consumer-driven contract tests** (Pact) to verify provider/consumer
  compatibility *without* full E2E.
  *Ref: Enabling Microservice Success.md — "Contract Testing" (`page-457-0`).*
- **Test in production** with feature flags, canary releases,
  blue-green, synthetic monitoring, and observability.
  *Ref: Enabling Microservice Success.md — "Testing in Production" (`page-465-0`).*
- Make tests **fast, independent, repeatable, self-validating, timely**.
  *Ref: Enabling Microservice Success.md — "What Makes a Good Test" (`page-474-0`).*
- Make operations **idempotent** — republish had no side effects at the FT.
  *Ref: Enabling Microservice Success.md — "Idempotency" (`page-517-0`).*

**Don't:**
- Don't set E2E coverage targets — they create slow, brittle, false-
  confidence tests. Focus on tests that find *real* problems in complex code.
  *Ref: Enabling Microservice Success.md — "The author is not a fan of test coverage targets" (`page-474-0`).*

---

### Resilience Patterns

**Principle:** One service's failure must not cascade. Build for failure.

**Do:**
- Apply the **failure cascade kit**:
  - **Circuit breakers** — stop calling a failing service, let it recover.
  - **Timeouts** — aggressive; prevent thread blocking.
  - **Bulkheads** — isolate resources per request type.
  - **Fallbacks** — degraded but functional (e.g., popular items vs.
    personalized).
  *Ref: Enabling Microservice Success.md — "Handling Cascading Failures" (`page-501-0`).*
- Use **retries with exponential backoff + jitter** + max retry count, and
  *only* on idempotent operations.
  *Ref: Enabling Microservice Success.md — "Retries" (`page-509-0`).*
- Set **SLOs** in user-facing terms ("99.9% of article publish requests
  succeed in 5s"). Track via **SLIs**. Use **error budgets** to gate
  reliability work vs. feature work.
  *Ref: Enabling Microservice Success.md — "Service Level Objectives (SLOs)" (`page-532-0`).*
- Use **redundancy**: multiple instances, multi-AZ, multi-region, load
  balancing, zero-downtime deploys.
  *Ref: Enabling Microservice Success.md — "Redundancy" (`page-539-0`).*
- Run **chaos engineering** experiments — start small (kill one instance),
  grow.
  *Ref: Enabling Microservice Success.md — "Chaos Engineering" (`page-524-0`).*

---

### Observability (Logs, Metrics, Traces)

**Principle:** In microservices, "is everything OK?" is a hard question.
You need to *infer* state from external outputs.

**Do:**
- **Structured logging** (JSON or KV), with **correlation IDs**,
  **service name**, **UTC timestamps**, consistent field names.
  *Ref: Enabling Microservice Success.md — "Logging" (`page-566-0`).*
- Use **USE** (Utilization, Saturation, Errors) for infra; **RED** (Rate,
  Errors, Duration) for services.
  *Ref: Enabling Microservice Success.md — "Monitoring and Metrics" (`page-572-0`).*
- Use **NTP-synced clocks** to avoid timestamp drift in log aggregation.
  *Ref: Enabling Microservice Success.md — "Log Aggregation" (`page-580-0`).*
- Adopt **OpenTelemetry** — vendor-neutral instrumentation; switch backends
  without re-instrumenting.
  *Ref: Enabling Microservice Success.md — "OpenTelemetry" (`page-589-0`).*
- Use **distributed tracing** (OpenTelemetry-compliant) for end-to-end
  visibility across services.
  *Ref: Enabling Microservice Success.md — "Distributed Tracing" (`page-593-0`).*
- Build **custom domain diagnostics** (the FT's *Content Doctor*,
  *List Doctor*, *Publish Monitor*). Off-the-shelf tools miss
  domain-specific failure modes.
  *Ref: Enabling Microservice Success.md — "Building Custom Tools" (`page-597-0`).*
- Monitor **business outcomes**, not just technical metrics (synthetic +
  semantic monitoring).
  *Ref: Enabling Microservice Success.md — "Monitoring Business Outcomes" (`page-623-0`).*

**Don't:**
- Don't believe that alerts on every instance-level health tell you the
  system is fine. A failing instance behind a load balancer is "OK" from
  a user perspective.
  *Ref: Enabling Microservice Success.md — "Observability" (`page-47-0`).*
- Don't use **coverage targets** for tests — they encourage low-value tests.

---

### Managing Change at Scale

**Principle:** Distribute decision-making; only centralize what's truly
cross-cutting.

**Do:**
- Distinguish change types:
  - **Emergency** — automate, minimal process.
  - **Minor planned** — low-risk, frequent, CI/CD handles.
  - **Major planned** — TGG, plan + coordinate.
  *Ref: Enabling Microservice Success.md — "Types of Change" (`page-652-0`).*
- Use the **Architecture Advice Process**: anyone can make a decision,
  but they must consult those affected and those with expertise.
  *Ref: Enabling Microservice Success.md — "Who Gets to Decide?" (`page-667-0`).*
- Maintain a public **change log** to correlate changes with incidents.
  *Ref: Enabling Microservice Success.md — "Managing Change at Scale" (`page-682-0`).*
- Schedule work that **reduces risk, improves operability, pays down tech
  debt, or enables future features**.
  *Ref: Enabling Microservice Success.md — "Scheduling Work" (`page-676-0`).*

---

### Leading Through Influence (Nudge Theory)

**Principle:** You can't *mandate* autonomous teams. Lead through
influence: data, social proof, narrative, and **nudges** (Thaler &
Sunstein).

**Do:**
- Drive change via **data**, **social proof**, **narrative**.
  *Ref: Enabling Microservice Success.md — "Leading Through Influence" (`page-694-0`).*
- Design **nudges** that make the right thing the default:
  - Make the desired behavior the default.
  - Provide clear feedback.
  - Simplify the process.
  - Use social norms.
  *Ref: Enabling Microservice Success.md — "Nudge Theory" (`page-702-0`).*
- Use **multiple communication channels** (Slack, email, talks, posters);
  **repeat** important messages; **tell stories**; enable **two-way**
  communication.
  *Ref: Enabling Microservice Success.md — "Communicating Change" (`page-720-0`).*
- Address **resistance** with curiosity, not force: understand the
  resistance, address legitimate concerns, start with enthusiasts, be
  patient but persistent.
  *Ref: Enabling Microservice Success.md — "Dealing with Resistance" (`page-728-0`).*
- **Automate compliance** so the right thing is the easy thing — *"the
  most effective governance is built into templates, pipelines, and tools."*
  *Ref: Enabling Microservice Success.md — "Automating Guardrails" (`page-411-0`).*

**Example (UK organ donation):** ~100,000 additional registrations/year
through copy changes alone (reciprocity framing + loss aversion).
  *Ref: Enabling Microservice Success.md — "UK Organ Donation Case Study" (`page-716-0`).*

---

## Anti-Patterns & Common Mistakes
- **Microservices without CI/CD, IaC, observability.** *fix:* lay the
  groundwork first. *Ref: Enabling Microservice Success.md — "Before You Start" (`page-38-0`).*
- **Sharing a database across services.** *fix:* one DB per service, even
  if you duplicate data. *Ref: Enabling Microservice Success.md — "Data Considerations" (`page-128-0`).*
- **HFT (hero-team-only-FaaS-first) without a path to production.**
  *fix:* FT moved from 12 releases/year to ~2,500 — but only after CD.
  *Ref: Enabling Microservice Success.md — "Continuous Delivery" (`page-41-0`).*
- **Manual Saturday-morning deploys** for a system with many services.
  *fix:* automate. *Ref: Enabling Microservice Success.md — "Continuous Delivery" (`page-41-0`).*
- **Central architecture team that decides for everyone.** *fix:* every
  team does architecture within their domain; cross-cutting via TGG.
  *Ref: Enabling Microservice Success.md — "Architecture as Guidance" (`page-241-0`).*
- **Document-only guardrails.** *fix:* bake them into templates, pipelines,
  tools. *Ref: Enabling Microservice Success.md — "Automating Guardrails" (`page-411-0`).*
- **Healthchecks as restart triggers.** *fix:* healthchecks for humans;
  never let them auto-restart cascading-fail.
  *Ref: Enabling Microservice Success.md — "Healthchecks" (`page-613-0`).*
- **E2E test coverage as a target.** *fix:* test pyramid + contract tests +
  test in production. *Ref: Enabling Microservice Success.md — "The author is not a fan of test coverage targets" (`page-474-0`).*
- **Solo on-call for a small team.** *fix:* share on-call across a
  *group* of teams. *Ref: Enabling Microservice Success.md — "On-call burden" (`page-320-0`).*
- **Skipping modular monolith.** *fix:* a modular monolith is a valid
  destination and a stepping stone. *Ref: Enabling Microservice Success.md — "Modular Monoliths" (`page-37-0`).*

---

## Decision Heuristics / Checklists
- **Should we adopt microservices now?** Five prerequisites
  (CI/CD, automated testing, IaC, observability, team autonomy) — all
  present? Multiple teams needing independence? Different scale / tech
  needs? If no, modular monolith.
- **Where to start a new microservice extraction?** ISH checklist
  (Independent, Stateless, Helpful) + value × difficulty quadrant
  (prefer high-value, low-difficulty).
- **Fracture plane?** Default to *business capability*; use *data*
  only when co-located data changes together; use *technology* only when
  the polyglot cost is justified.
- **Sync or async?** Sync when caller can't proceed without the result
  and operation is short. Async when you want decoupling, buffering, or
  event-driven fanout.
- **Governance decision?** Cross-team → TGG + ADR. Domain-scoped → team
  decides.
- **Paved road or off-road?** Paved road is optional, but most teams
  choose it when it's *so good*. Innovation off-road is encouraged, and
  innovations are folded back into the paved road.
- **Observability vendor?** Pick one that supports OpenTelemetry APIs so
  you can switch backends without re-instrumenting.
- **Test pyramid:** push to unit tests; replace E2E with contract tests
  and test-in-production.

---

## Key Takeaways
1. **Microservices are an organizational pattern as much as a technical
   one.** Team topology, Conway's Law, autonomy, and motivation matter
   as much as any tech choice.
2. **Lay the groundwork first.** CI/CD, automated testing, IaC,
   observability, team autonomy are *prerequisites*, not afterthoughts.
3. **Decompose around business capabilities.** DDD + Event Storming +
   the ISH checklist. Don't split a table column across services — pick
   *one* domain to own it.
4. **Cross-functional, long-lived, autonomous teams of 5–9 people**
   motivated by **autonomy, mastery, purpose** (Pink). Avoid solo on-call
   — share across a group.
5. **Paved road > policy doc.** Make the right thing the easy thing via
   templates and automated guardrails. Innovation off-road is welcome.
6. **"You build it, you run it."** Teams that feel the pain of poor
   operability build operable systems. Share on-call. Run blameless
   postmortems. Maintain runbooks.
7. **Track your software estate.** A service catalog (Backstage /
   OpsLevel / Cortex / Biz Ops) is mandatory at 100+ services.
   Automate guardrails into templates.
8. **Test pyramid + contract tests + test in production.** E2E coverage
   is a bad target. Use Pact for provider/consumer compatibility. Use
   feature flags, canary, blue-green, and synthetic monitoring.
9. **Resilience is built, not wished for.** Circuit breakers, timeouts,
   bulkheads, fallbacks, retries with jitter, SLOs with error budgets.
   Idempotency is a prerequisite for safe retries.
10. **Observability is non-negotiable.** Structured logs + correlation IDs +
    USE/RED metrics + distributed tracing (OpenTelemetry) +
    domain-specific tools. Alert on **SLOs** at the customer-facing edge.
11. **Distribute decision-making; centralize only what crosses teams.**
    TGG + ADRs for cross-cutting. Every team does architecture within
    their domain.
12. **Lead through influence.** Data, social proof, narrative, and
    **nudges**. Make the right thing the default. Automate compliance.
    Communicate repeatedly via multiple channels. Be patient with
    resistance, but persistent.

---

## Cross-References
- Related: `../Monolith_To_Microservices.md` (the migration patterns this
  book's prerequisites enable).
- Related: `../Microservices_Up_And_Running.md` (the prescriptive
  implementation that the FT-style paved road enables).
- Related: `../Building_Event-driven_Microservices.md` (the runtime
  patterns — the technical half of "microservices").
- Related: `../Building_An_Event-Driven_Data_Mesh.md` (data-product
  patterns that flow out of the data-ownership principle in this book).
- Related: `../Flow_Architectures.md` (the cross-organizational evolution
  the FT paved road enables internally).
- Topic index: `../INDEX.md`
