# Per-Book Best Practices — Enabling Microservice Success

> **Author:** Sarah Wells (Foreword by Sam Newman)
> **Publisher:** O'Reilly Media, 2024 (First Edition)
> **Topic tags:** `#architecture` `#organization` `#leadership`
> **Language focus:** Language-agnostic (case studies drawn from Java, Go, Node.js, Python, Ruby)
> **Sources:** `markdown_output/Enabling Microservice Success/Enabling Microservice Success.md` · `summaries/Enabling_Microservice_Success.md`

---

## TL;DR

This book distills a decade of microservices experience at the *Financial Times* (FT) and other adopter organizations into the technical, organizational, and cultural changes required to make microservices succeed long term. Wells argues that microservices are an organizational pattern as much as a technical one: Conway's Law, Team Topologies, paved-road platform engineering, federated governance, and blameless incident management matter more than any framework or runtime. The payoff is fast flow of business value and continuous evolution of the system without catastrophic rewrites; the cost is sustained investment in autonomy, observability, resilience, and change management. Apply this material when you are scaling the number of teams working on the same product, when developer experience is degrading, when independent deployability is becoming impossible, or when you need to evolve architecture piece by piece without big-bang rewrites.

---

## Best Practices by Topic

### 1. Conway's Law and the Inverse Conway Maneuver

**Principle:** Software architecture mirrors the communication structure of the organization that builds it — so design the org and the architecture together, iteratively.

**Do:**
- Start decomposition with team-size constraints (5–9 people per Team Topologies team, 50–150 per group), then derive service boundaries from those team sizes.
- Use the Inverse Conway Maneuver to reshape teams so that the system you want becomes buildable. Plan org changes and architecture changes as one program, not two.
- Pinch off small parts of the system *and* the organization iteratively rather than reorging everything at once — Mathias Verraes' rule "a reorganisation won't fix a broken design" still applies.
- Treat the system graph (subsystems and interfaces) and the organization graph (subgroups and communication paths) as twin artefacts that must remain isomorphic.
- Use Conway's Law as the diagnostic when boundaries are wrong: if a flow needs handoffs across many teams, you probably have the boundaries in the wrong place.

**Don't:**
- Don't reorganise before you know the end-state architecture — reorgs are stressful, sap productivity for months, and often accelerate attrition.
- Don't let a hierarchical organization (frontend / backend / DBA silos) produce a tightly coupled layered system — every feature will need three teams.
- Don't fight Conway's Law by trying to enforce architecture against the org chart.

**Code / Notes:**
```
Conway's original 1968 paper (45 paragraphs): "Any system of consequence
is structured from smaller subsystems which are interconnected... different
teams then design these different subsystems."

Elementary probability theory tells us that the number of possible
communication paths in an organization is approximately half the square
of the number of people in the organization. Even in a moderately small
organization it becomes necessary to restrict communication in order that
people can get some WORK done.
```

*Ref: Enabling Microservice Success.md — "Conway's Law" (Ch. 4), "The Inverse Conway Maneuver"*

---

### 2. Team Topologies: Stream-Aligned, Platform, Enabling, Complicated-Subsystem

**Principle:** A loosely coupled microservice architecture requires a loosely coupled organization made of just four team types, each interacting in well-defined ways.

**Do:**
- Make the majority of teams **stream-aligned**: cross-functional, owned by a single stream of work, capable of taking a feature from idea to production.
- Create a **platform team** (or platform group) to provide self-service APIs, tools, and services that reduce extrinsic cognitive load for stream-aligned teams.
- Use **enabling teams** as internal consultants who grow capabilities in stream-aligned teams (observability, security, deployment, design systems).
- Apply **complicated-subsystem teams** only when specialist knowledge is required and consumed by many other teams (e.g., ML, search, payments crypto).
- Build groups of 50–150 people so team-lead meetings, 24/7 rotas, and shared learning remain feasible.
- Pair stream-aligned and platform teams through *X-as-a-Service* interaction after an initial *Collaboration* phase to pathfind a new capability.

**Don't:**
- Don't use a complicated-subsystem team for things that any stream-aligned team could build — keep this team type rare.
- Don't allow a platform team to become a dumping ground for unrelated systems.
- Don't build a "platform team" that has only one hammer — Team Topologies practitioners now speak of a *platform grouping* containing multiple teams of different types.
- Don't separate platform from product — both must "build and run" their services (platform runs the platform, products run the products).

*Ref: Enabling Microservice Success.md — "Optimizing for Flow" (Ch. 5), "Engineering Enablement and Paving the Road" (Ch. 7)*

---

### 3. Team Topologies Interaction Modes: Collaboration, X-as-a-Service, Facilitating

**Principle:** Reduce coordination overhead by being explicit about how teams interact, and reserve high-bandwidth modes for high-value work.

**Do:**
- Use **Collaboration** (two teams working closely, often via a temporary feature team) only during discovery, prototyping, or boundary innovation.
- Transition to **X-as-a-Service** once the capability stabilises — one team provides the service, others consume it.
- Use **Facilitating** (mentoring, knowledge transfer) for ongoing capability uplift; this is the primary mode of enabling teams.
- When forming feature teams, decide up front who owns the resulting assets once the feature team disbands.
- Make consumer relationships explicit: provider teams need product management skills to understand and serve their consumers.

**Don't:**
- Don't sustain Collaboration for long periods — it blurs team boundaries and creates a high cognitive-load, high-intensity mode of working.
- Don't skip the Collaboration phase entirely for high-risk integrations — pathfinding saves time later.
- Don't let consumers dictate implementation; that couples them in.

*Ref: Enabling Microservice Success.md — "Interaction Styles" (Ch. 6)*

---

### 4. Domain-Driven Design, Bounded Contexts, and the ISH Heuristics

**Principle:** Service boundaries should track bounded contexts where teams use the same language and own data that changes together.

**Do:**
- Use **bounded contexts** to find candidate service boundaries: when the same word (e.g., "lead") means different things to two stakeholders, you have found a context split.
- Co-locate data that changes together in the same service. Avoid distributed transactions by design.
- Use **event storming** workshops to identify domain events and bounded contexts collaboratively.
- Apply **Independent Service Heuristics (ISH)** to validate a candidate split: Is it Independent? Is it Stateless? Is it Helpful?
- Ask the ISH data questions:
  - Is it fairly independent from any data sources?
  - Are the sources internal (under our control)?
  - Is the input data clean (not messy)?
  - Is the input data provided in a self-service way?
- Use Nick Tune's **Bounded Context Canvas** to design naming, responsibilities, public interfaces, and dependencies for each candidate context.
- Accept that bounded contexts may need to change as you learn the domain.

**Don't:**
- Don't decompose too early when you don't yet understand the domain — start with a modular monolith.
- Don't split a domain so that transactions cross services unnecessarily — moving money between accounts belongs in one service, not across an Account and a Transfer service.
- Don't keep changing two services in lockstep — they probably shouldn't be two services.

*Ref: Enabling Microservice Success.md — "Business Domains" (Ch. 4)*

---

### 5. Strategic Service Boundaries: Compliance, Failure Tolerance, Change Frequency

**Principle:** Beyond business domains, additional fracture planes help when they reflect real organisational or risk realities — but use them as a primary boundary only when business domains won't work.

**Do:**
- Use **compliance** as a primary boundary when parts of the system must meet PCI, GDPR, or zero-trust requirements — segregating PII storage behind a verified-access service is a classic win.
- Use **failure tolerance / service tier** as a primary boundary to avoid forcing every service into platinum-grade multiregion running.
- Use **change frequency** to separate app-store-deployed mobile apps from back-end services.
- Align teams to **locations** so a single domain is owned within a single time zone (per Martin Fowler: "Putting teams in separate cities … further gets in the way of regular conversation").
- When Fowler's architect had six teams in six cities, his first architectural decision was simply "there are going to be six major subsystems."

**Don't:**
- Don't make **technology** the primary fracture plane — it leads to layered teams (frontend/backend/DBA) and a tightly coupled layered system.
- Don't introduce a second programming language casually — every additional language multiplies the cost of libraries, hiring, and runbooks.
- Don't split boundaries because a different team has a different view of the same domain without first trying to align them.

*Ref: Enabling Microservice Success.md — "Possible Boundaries" (Ch. 4)*

---

### 6. Paved Road / Golden Path / Production-Ready Service Template

**Principle:** A paved road is a self-service, internally supported set of tools and templates that makes the right way the easiest way — and remains optional so teams are still customers, not captives.

**Do:**
- Make the paved road **optional**, but so good that most teams choose it. Optionality is a feedback signal: if people opt out, find out why.
- Build a paved road for *every team* capability: source control, CI/CD, deployment, observability, runtime, storage, networking, API gateways.
- Run on **public cloud or PaaS first**; build bespoke platforms only when there's a clear differentiator. The *FT* moved off its own container orchestration as soon as Kubernetes was production-ready.
- Include healthchecks, structured logging, correlation IDs, security scanning, change logging, and runbook scaffolding in the service template — most guardrails should be *embedded in the template*, not documented.
- Provide **APIs** rather than copied templates — APIs decouple the implementation from the consumer and let you version and update centrally.
- Lean on **Werner Vogels' "undifferentiated heavy lifting"**: don't run your own message queues or database clusters when the cloud does it for you.

**Don't:**
- Don't make the paved road mandatory — it kills the market signal and removes the pressure to actually build something people want.
- Don't let the platform team block off-road experiments with "we're about to build that" — if you're not literally next, let teams go.
- Don't expose so much abstraction that teams can't get at underlying functionality when they need it (Alan Kay: "Simple things should be simple, complex things should be possible").
- Don't rely on copied templates — they're hard to update centrally and have caused global outages (e.g., Skyscanner).

**Code / Notes:**
```
*Ref: Enabling Microservice Success.md — "Paving the Road" (Ch. 7), "Beyond the Platform" (Ch. 7)*
Principle checklist for paved-road capabilities:
  - Optional
  - Provides value
  - Self-service
  - Owned and supported
  - Easy to use (good docs, sane defaults, good errors)
  - Guides people to do the right thing (safe defaults, hard to overspend)
  - Composable and extendable (APIs, SDKs, CLIs)
```

---

### 7. Platform-as-Product: Treat Internal Platforms as Compelling Internal Products

**Principle:** A platform team is a *product team* whose customers are engineers — without product thinking, the platform becomes shelf-ware.

**Do:**
- Apply **Evan Bottcher's** definition: "A digital platform is a foundation of self-service APIs, tools, services, knowledge and support which are arranged as a compelling internal product."
- Recruit engineers *from* stream-aligned teams — they bring real pain points and existing relationships.
- Run **developer huddles**, showcases, and surveys to gather real demand rather than guessing what engineers need.
- Don't add complexity to fix a problem a vendor already solves — buy where possible.
- Aim for the **thinnest viable platform (TVP)**: build only what customers need, no more. The platform may be a wiki of available SaaS options.
- Re-evaluate regularly: as the cloud or vendor offerings evolve, your "TVP" should *float* (Greg Hohpe's term).
- Provide **internal developer portals** (Backstage, OpsLevel, Cortex) that surface service catalog, templates, docs, and scorecards.

**Don't:**
- Don't call the team "the platform team" if your culture still thinks of them as the gatekeeping ops team of old. The name signals the model.
- Don't build for the *innovator* (Simon Wardley's explorer) — build for the *majority* (village-dweller / settler) and let explorer-driven teams hack their own path off-road.
- Don't ship a six-month platform feature with no feedback loop — ship MVPs, iterate, and continuously improve.
- Don't score teams without making the scoring transparent and clearly tied to action.

*Ref: Enabling Microservice Success.md — "Platform as a Product", "Paving the Road" (Ch. 7)*

---

### 8. Service Tiers, Criticality, and Cost-Aware Engineering

**Principle:** Don't run every service like it's platinum — segregate by criticality so resilience investment matches business impact.

**Do:**
- Define explicit service tiers (FT used **platinum / gold / silver / bronze**).
- Require that out-of-hours support is paired with enhanced resilience — you should not expect engineers to support 24/7 unless the system is multiregion.
- Tie tier to alerts and on-call rotas: only platinum gets 24/7; bronze gets business-hours-only.
- Use tier to drive observability investment, runbook depth, and runbook review cadence.
- Capture tier in the service catalog and link it to dashboards.

**Don't:**
- Don't put every service in platinum — it dilutes effort and is unnecessarily expensive.
- Don't promise platinum support without multiregion running.
- Don't move tier up silently when scope changes — make it explicit.

*Ref: Enabling Microservice Success.md — "Service tier & support" (Ch. 11)*

---

### 9. Federal Tech Governance Group (TGG): Lightweight, Documented, Distributed

**Principle:** Replace centralised architecture mandates with a lightweight, transparent forum that *endorses* decisions after the work is done — and keeps a public record.

**Do:**
- Adopt a **two-page proposal template** with the following sections: Authors, Need, Proposed Approach, Known Limitations & Risks, Impact, Costs, Benefits, and Alternatives (including "Do Nothing").
- Circulate proposals in advance via Slack and a GitHub repo. Aim for ≥1 week of public review.
- Hold meetings where reps from each dev group endorse (or query) proposals. People who don't show up are presumed to endorse — their responsibility to attend.
- Frame the meeting as endorsement of work already done — raise concerns in advance on the document.
- Apply Andrew Harmel-Law's **Architecture Advice Process**: anyone can decide, but the decision-taker must consult those affected and those with expertise.
- Keep decisions in a searchable archive. Three years later, you'll want to ask "what on earth were they thinking?"
- Require TGG proposals for changes that have **broad impact**, **cost a lot of money**, or **go from local to global**.

**Don't:**
- Don't make TGG signoff a precondition for starting a POC — but do require it before large investments.
- Don't use TGG as a design-by-committee meeting. The work happens before the meeting.
- Don't allow attendance issues to block endorsement — make absence equivalent to endorsement and require groups to send reps.
- Don't let one architecture team become a bottleneck; TGG is a federated model.

**Code / Notes:**
```
TGG Proposal Template (FT):
  1. Authors:    Sponsors, accountable for the work.
  2. Need:       What is not working about the current status quo?
  3. Proposed Approach: Preferred solution.
  4. Known Limitations & Risks: With mitigations.
  5. Impact:     What or who is impacted?
  6. Costs:      CAPEX, OPEX, supplier contracts, licensing, people-effort.
  7. Benefits:   Quantitative (savings) or qualitative (morale, risk mitigation).
  8. Alternatives: Always include "Do Nothing" — it sharpens the need.
```

*Ref: Enabling Microservice Success.md — "Tech Governance Group" (Ch. 11)*

---

### 10. The 16-Step FT Guardrails (Production-Ready Service Checklist)

**Principle:** Encode "what it means to be production-ready" as a short, scoped checklist covering the full lifecycle of a service — embedded in tools where possible.

**Do:**
- Step through these when bringing a service live or auditing one:
  1. **Buy vs. Build** — Can you buy this rather than build it?
  2. **Procurement** — Run new vendor relationships through procurement (even free trials).
  3. **Significant Technology Changes** — Discuss openly; use TGG.
  4. **Service Record** — Create a record in the service catalog (Biz Ops).
  5. **Security & Privacy** — Build secure products; segregate PII storage.
  6. **Accessibility & Browser Support** — Meet accessibility standards.
  7. **Analytics, Logs, Metrics** — Decide log format, correlation IDs, system codes.
  8. **Change & Release Logging** — Log every production change (Change API).
  9. **Healthchecks & Monitoring** — Standardised JSON endpoint with severity and panicGuide.
  10. **Runbooks** — Could someone else fix a problem with your service?
  11. **Service Tier & Support** — Platinum / Gold / Silver / Bronze.
  12. **Performance** — Define and measure "too slow."
  13. **Cost Management** — TCO estimate; alert on overspend.
  14. **Going Live** — Mini-checklist (full Biz Ops record, runbook handover).
  15. **While Live** — Security patches, dependency upgrades, EOL tracking.
  16. **Decommissioning** — Shut down, remove from monitoring, set to "Decommissioned" in catalog.
- Embed each guardrail into the template, pipeline, or platform tooling rather than relying on people to read them.
- Tag AWS resources with the system code so the catalog entry is the source of truth.

**Don't:**
- Don't expect engineers to read a Drive of policy documents. Embed the rules.
- Don't make all 16 equally critical — some (compliance, accessibility) need active verification; others are nudges.

*Ref: Enabling Microservice Success.md — "The FT's Guardrails" (Ch. 11)*

---

### 11. Federated vs Centralised Governance: Light Touch with Insight

**Principle:** With autonomous teams, governance is "guide and verify," not "sign off." Make the right thing the default and surface insight into where teams are falling short.

**Do:**
- Frame governance as **supportive**, not restrictive — guardrails, not rules.
- Treat the original central architecture team as obsolete; do architecture *within* every team.
- Use a Tech Governance Group (TGG) for cross-cutting decisions.
- Trust teams to take action but verify (e.g., audit not gate; alert on root-AWS-account logins, don't pre-approve them).
- Provide **insight** via dashboards and scoring (e.g., SOS — System Operability Score for runbook completeness) so teams know where to focus.
- Use **service tier** to scope the depth of governance: platinum services get full guardrails; bronze get the basics.
- Use CODEOWNERS files in source control to formalise ownership at file or repo level.

**Don't:**
- Don't impose standards without explaining *why*. Adoption follows comprehension.
- Don't make governance a separate ticket-approval workflow — that creates a queue and slows flow.
- Don't measure the wrong things (e.g., incident counts as a bonus metric — that *hides* incidents).

*Ref: Enabling Microservice Success.md — "Aligning on Guardrails" (Ch. 11), "Trust but Verify" (Ch. 6)*

---

### 12. Service Catalog as a Graph (Biz Ops FT-Style)

**Principle:** A graph-based, API-driven, extensible service catalog is the keystone for ownership, governance, automation, and incident response.

**Do:**
- Use a graph database (FT used Neo4j) — team-lead changes propagate to all owned services automatically.
- Expose both read and write APIs. Restrict write access for fields whose source of truth is elsewhere (e.g., GitHub repos).
- Link systems to teams, groups, people, GitHub repos, AWS accounts, DNS zones, API gateway keys, and incidents.
- Use GraphQL or similar so engineers can ask sophisticated questions (e.g., "all Java services with log4j").
- Track PII and other sensitive-data flags so GDPR / SAR responses are automated.
- Use the catalog's data to drive dashboards (services in the team view), change tagging (system code on AWS resources), and security incident response (Log4Shell).
- Modern alternatives: **Backstage (open source)**, **OpsLevel**, **Cortex**, **Configure8** — don't build bespoke.

**Don't:**
- Don't store runbook information in the same DB that's not highly available — the FT had to extract runbook data to S3 because the catalog itself was single-region.
- Don't let the catalog become write-only — surface it via dashboards, scorecards, gamification.
- Don't combine disparate metrics into a single score that loses context.

**Code / Notes:**
```
FT Biz Ops graph nodes & edges (subset):
  System → owned by → Team
  Team   → part of  → Group
  Team   → has lead → Person
  Team   → has members → Person
  Group  → has lead → Person
  System → repository → GitHubRepo
  GitHubRepo → team → GitHubTeam
  System → region  → AWSAccount
  System → tier    → {platinum|gold|silver|bronze}
  System → contains PII → boolean
  System → incident → Incident
```

*Ref: Enabling Microservice Success.md — "A Service Catalog" (Ch. 7), "What You Need from a Service Catalog" (Ch. 9)*

---

### 13. Strong vs Weak vs Collective vs Active Service Ownership

**Principle:** Every service must have a *team* owner, and that ownership must be **active** — patches, runbooks, dependencies, code stewardship, production support.

**Do:**
- Make ownership a **team** responsibility, not an individual's, so holidays and turnover don't leave services orphaned.
- Use **strong ownership** by default: only the owning team can change the service.
- Allow **weak ownership** (PRs from outside teams) only when there is genuinely loose coupling — not as a workaround for contention.
- Treat **shared libraries** with caution; prefer duplication for fields a service actually uses (Postel's Law — be lenient in what you accept).
- Make the owning team responsible for:
  - Code stewardship (API changes elsewhere)
  - Upgrades and patching (dependencies, base images)
  - Migrations (when the org moves to a new vendor)
  - Production support
  - Documentation (runbook, architecture, ops handover)
- Periodically **rebuild services** even when you don't deploy them, to catch build rot before it bites.

**Don't:**
- Don't allow individual ownership — holidays, turnover, and team moves make it unreliable.
- Don't allow **collective ownership** as the norm in microservices: Linux-kernel research shows code with ≥9 contributors is 16x more likely to have a security vulnerability.
- Don't drift from active to nominal ownership silently — the FT saw teams inherit services they didn't really run, only finding out at the next incident.
- Don't accept "no ownership" as a status — when a service is feature-complete, assign an owner anyway.

*Ref: Enabling Microservice Success.md — "Active Service Ownership" (Ch. 9)*

---

### 14. Transferring Service Ownership with Knowledge and Operational Handover

**Principle:** A service transfer must include quality compliance, code stewardship handover, runbook update, and ideally a chaos-engineering exercise.

**Do:**
- Before transferring, ensure:
  - Automated test coverage is in place.
  - The service complies with guardrails.
  - The runbook is up-to-date and complete.
- Walk through architecture, monitoring, troubleshooting docs with the receiving team.
- Run a **chaos engineering scenario** to confirm the new team can detect, diagnose, and fix issues.
- Transfer any vendor relationships (account managers, status-page contacts, support contracts).
- Consider rewriting the service in the receiving team's preferred tech if the existing tech is unknown to them.
- If both teams agree, get the receiving team to make a small change and deploy it as a confidence-building exercise.

**Don't:**
- Don't throw the service "over the wall." Both teams must invest time.
- Don't forget operational handover (out-of-hours, SLO, on-call escalation paths).
- Don't transfer and walk away — schedule a 30/60/90-day check-in to surface hidden tech debt.

*Ref: Enabling Microservice Success.md — "Transferring Ownership" (Ch. 9)*

---

### 15. "You Build It, You Run It" — DevOps Discipline Without Burnout

**Principle:** Teams that build services must operate them in production — but out-of-hours support must be designed for sustainability, not heroism.

**Do:**
- Treat the *Definition of Done* as "in production and stable with appropriate security and observability."
- Run a rotating **in-hours Ops Support** person (or sub-team) so operational issues don't interrupt flow for everyone.
- Allow people to **opt out** of out-of-hours support (parental leave, health, sleep patterns) — make it opt-in with the right to step back.
- Use **best-efforts rotas** rather than formal rotas when teams are small. The FT found this still gave rapid response at lower financial cost.
- Mitigate before fixing: scale up, failover, restart, roll back. Diagnose later.
- Make calls **rare** (a few per year per person) — automate recovery from anything predictable.
- Reserve 24/7 support for **critical systems** (platinum tier). Other tiers get business-hours-only.
- Provide **practiced mitigation** (failover drills, chaos engineering) so escalations are calm.

**Don't:**
- Don't make out-of-hours mandatory — make it opt-in with explicit opt-out paths, and treat low opt-in as a system-design smell.
- Don't allow weekend deploys just because the deploy process is flaky — fix the process.
- Don't commit code out of hours; mitigate only.
- Don't firefight without an incident review: improvements must be scheduled.

*Ref: Enabling Microservice Success.md — "Ensuring 'You Build It, You Run It'" (Ch. 8)*

---

### 16. Incident Management: Blameless, Role-Based, Learning-Focused

**Principle:** Incident management is a first-class discipline — roles, communication channels, mitigation first, blameless review after.

**Do:**
- Assign an **Incident Manager** (not necessarily a tech lead) to coordinate communication and free engineers to debug.
- Open a **public incident channel** (Slack/Teams) so people can volunteer to help.
- Update an **internal status page** so stakeholders have one place to look.
- Encourage people to raise incidents **early and often**, even if it turns out to be nothing — track metrics around openness, not count.
- Mitigate first: failover, scale up, roll back. Diagnose second.
- Run **blameless postmortems** with a template including timeline, surprises, "where we got lucky," and a short action list (≤2 actions).
- Tie incident actions to OKRs and capacity: 1 agreed action per incident.
- Move long-incident hand-offs to fresh people (incident managers get tired too).

**Don't:**
- Don't track incident counts in a way that becomes a bonus metric — it suppresses reporting.
- Don't let senior leaders join the active incident channel — it changes behaviour. Communicate via a private side channel.
- Don't skip postmortems because calendars are full — book them now.
- Don't accept huge action lists from incident reviews — they won't all get done.

**Code / Notes:**
```
FT incident report template:
  - Summary (TL;DR)
  - Timeline (pinned Slack messages captured automatically)
  - Surprises (where was our model wrong?)
  - Where we got lucky
  - Agreed actions (ideally 1–2, owned, dated)
```

*Ref: Enabling Microservice Success.md — "Incident Management" (Ch. 8), "Learning from Incidents" (Ch. 13)*

---

### 17. Observability: Logs, Metrics, Traces — and OpenTelemetry

**Principle:** With distributed systems, you infer state from external outputs. Standardise on structured logs with correlation IDs, RED/USE metrics, and OpenTelemetry traces — and don't lock yourself to a vendor.

**Do:**
- Emit **structured logs** (JSON or key-value pairs) with consistent field names across services: `timestamp`, `level`, `message`, `system_code`, `correlation_id`.
- Generate a **correlation ID** at ingress and propagate it in headers and message bodies across every service hop.
- Include a system code from the service catalog in every log line.
- Use **RED metrics** (Rate, Errors, Duration) for web/API services and **USE** (Utilization, Saturation, Errors) for infrastructure.
- Tag metrics so you can aggregate by service, team, or environment.
- Adopt **OpenTelemetry** — instrument once, change providers without rewriting.
- Use **distributed tracing** for the path of a request through services.
- Archive a subset of observability data to your data warehouse so you can investigate issues from months ago.
- Treat observability as **events, not just logs/metrics/traces** — slice by high-cardinality dimensions like `user_id`.

**Don't:**
- Don't log DEBUG level in production — you'll drown in noise.
- Don't allow unsynchronised server clocks (use NTP) — out-of-order logs cause confusion.
- Don't assume every log will be shipped — defaults can silently drop logs (FT was bitten by systemd 1000-message/30-second limit).
- Don't sample away your ability to know something is wrong — be careful what you filter.

**Code / Notes:**
```json
{
  "timestamp": "2022-12-23T12:34:56Z",
  "level": "error",
  "message": "Article failed validation, no author information provided",
  "article_id": "4744cd87-8bbc-4910-9d33-be1a816f2b18",
  "correlation_id": "7d965d54-0b3f-47f7-a8a1-ae2c744248f0",
  "system_code": "article_publisher"
}
```

*Ref: Enabling Microservice Success.md — "Logging", "Monitoring and Metrics", "Distributed Tracing", "OpenTelemetry" (Ch. 13)*

---

### 18. Healthchecks: Standardised, Realistic, Cascading-Safe

**Principle:** Healthchecks are how you tell whether a service is *operationally* healthy without causing cascading restarts. Standardise the schema across all services.

**Do:**
- Define a standard HTTPS endpoint returning **JSON** with:
  - `schemaVersion`, `systemCode`, `name`, `description`
  - `checks[]` array, each with: `lastUpdated`, `ok`, `panicGuide` (runbook URL), `name`, `id`, `severity`, `businessImpact`, `technicalSummary`.
- Make healthchecks do **realistic queries** (e.g., `SELECT 1` against the DB), not just ping dependencies.
- **Return HTTP 200 even when checks fail** — only an unresponsive endpoint means "unhealthy." This prevents cascading restarts.
- Cache results for a short period to reduce traffic and false alarms.
- Show healthchecks on team dashboards — humans interact with them as well as machines.
- Document what a "failing check" means in `businessImpact` and `technicalSummary` so triagers don't have to guess.

**Don't:**
- Don't tie healthchecks too tightly to dependency health — if every dependency check causes a service restart, you get a cascading failure.
- Don't pay log-aggregation costs for healthcheck traffic — filter it out.
- Don't forget to include a `panicGuide` URL — first responders need a runbook.

**Code / Notes:**
```json
{
  "schemaVersion": 1,
  "systemCode": "article_publisher",
  "name": "ArticlePublisher",
  "description": "Publishes/updates/deletes articles",
  "checks": [
    {
      "lastUpdated": "2016-10-29T16:17:382",
      "ok": true,
      "panicGuide": "https://link_to_run_book",
      "name": "Connectivity to content data store",
      "id": "Connectivity to content data store",
      "severity": 1,
      "businessImpact": "Articles cannot be published",
      "technicalSummary": "Cannot connect to the content MongoDB cluster"
    }
  ]
}
```

*Ref: Enabling Microservice Success.md — "Healthchecks" (Ch. 13)*

---

### 19. Resilience Kit: Timeouts, Retries with Backoff+Jitter, Idempotency, Circuit Breakers, Bulkheads, Fallbacks

**Principle:** A distributed system runs in a constant state of partial failure. Build every service defensively: assume the worst, fail fast, retry safely, fall back gracefully.

**Do:**
- Set **aggressive timeouts** (seconds, not the default 10s) on every external call. Use a few multiples of the p99 latency.
- **Retry** only idempotent operations, only on 5xx, only with **exponential backoff** and **jitter**.
- Mark every operation as **idempotent** (e.g., via an idempotency key) so retries don't double-bill.
- Install **circuit breakers** that trip after a threshold of failures and recover after a cooldown.
- Use **bulkheads** (thread pools, connection limits) so a slow downstream doesn't exhaust your resources.
- **Design for fallback** — cache last-known data, return a static list, remove a UI section rather than 500.
- **Fail open or fail closed** depending on the business impact (FT fails open on subscription status check — it's better to give a free article than to deny a paying reader).
- Distinguish "down" (easy to detect) from "slow" (often worse) — test slow scenarios explicitly.

**Don't:**
- Don't retry non-idempotent operations without an idempotency key.
- Don't retry synchronously across multiple services in a chain — you'll do exponential work the user already abandoned.
- Don't use default library timeouts (often 10s+) — set them explicitly to seconds.
- Don't block startup on external systems — services should start regardless of dependency health.

*Ref: Enabling Microservice Success.md — "Building Resilience In" (Ch. 12), "Set Appropriate Timeouts", "Back Off and Retry", "Make Your Requests Idempotent", "Handling Cascading Failures" (Ch. 12)*

---

### 20. Asynchronous Messaging and Decoupling

**Principle:** Synchronous chains of services are a recipe for cascading failures and wasted work. Prefer async messaging for any non-blocking flow.

**Do:**
- Use **queues** between services wherever the consumer doesn't need to return data to the producer.
- Design messages so the consumer can be added, removed, or restarted independently.
- Use **event-driven** patterns: publish on state change; let consumers subscribe.
- Design for **eventual consistency** when data crosses service boundaries.
- Apply **Saga pattern** with compensating transactions only when truly necessary.
- Set a **request time budget** at ingress (e.g., a "best before" header) so deep chains stop doing work after the user has given up.
- Use asynchronous workflows for things like checkout ("Order received") that don't need to wait for downstream confirmation.

**Don't:**
- Don't chain synchronous calls across many services in latency-sensitive paths.
- Don't share a database to avoid using a queue — that defeats loose coupling.
- Don't ignore the operational cost of queues — they are infrastructure too.

*Ref: Enabling Microservice Success.md — "Go Asynchronous", "Avoiding Unnecessary Work" (Ch. 12)*

---

### 21. Caching, CDNs, and Reducing Cross-Region Calls

**Principle:** Cache the hot path, but plan for cache misses and invalidation.

**Do:**
- Cache frequently-read, slowly-changing data close to the consumer.
- Even "time-sensitive" content (news) can be cached briefly (minutes) when popular.
- Use **stale-on-error** — return the cached value with a note if the source is unavailable.
- Test what happens when you fully clear the cache (don't let the cache be a single point of failure).
- Use **sticky load balancing** sparingly — uneven instance loads are usually a bug elsewhere.
- Avoid cross-region synchronous calls (≈150ms US↔EU TCP round trip vs. 300 same-region round trips).

**Don't:**
- Don't cache without thinking about invalidation — old data can be worse than no data.
- Don't make caching your only resilience mechanism.

*Ref: Enabling Microservice Success.md — "Caching" (Ch. 12), "Latency" (Ch. 1)*

---

### 22. Service Level Objectives (SLOs) and Error Budgets

**Principle:** Don't promise 100% — pick a target that matches business value and use error budgets to balance reliability work with feature work.

**Do:**
- Set SLOs in terms of user-facing outcomes ("99.9% of publish requests succeed within 5s"), not internal metrics.
- Use **SLIs** (Service Level Indicators) like request duration p95, error rate, throughput, availability.
- Express availability in "nines" but explain the business impact in human terms (e.g., "4.38 minutes of downtime per month").
- Set SLOs that cover peaks: design for "lose a region + peak traffic."
- Use **error budgets**: if you have budget left, take risks; if not, focus on reliability.
- Capture SLO breach alerts at the layer closest to the customer — don't alert cascades.

**Don't:**
- Don't treat 100% reliability as the target — it's unaffordable and undifferentiated.
- Don't set SLOs in isolation — talk to business stakeholders about what matters.
- Don't alert on every individual service health metric if it cascades — focus on the entry points.

*Ref: Enabling Microservice Success.md — "Service Level Objectives", "Error Budgets" (Ch. 12)*

---

### 23. Chaos Engineering, Game Days, and Disaster Recovery Practice

**Principle:** You don't really know your resilience until you've tested it under realistic conditions.

**Do:**
- Start chaos experiments **small** (single instance, low blast radius).
- Use Russ Miles' "Dungeons & Dragons" model: sometimes let responders not know what's coming to test real readiness.
- Predict what will happen *before* the experiment, then compare.
- Run **chaos experiments as part of service handover** — the new team learns the system by trying to break it.
- Practice **failover** regularly (FT practiced moving ft.com to a single region on a schedule).
- Practice **backup-and-restore** regularly — unverified backups aren't backups.
- Test that you can run load tests to breaking point to find your real capacity ceiling.
- Test failover of *external* dependencies too (CDN, DNS, identity).

**Don't:**
- Don't break things on purpose without buy-in — coordinate with stakeholders first.
- Don't accept "we tested it once" as proof — drift happens.
- Don't skip practice for critical procedures.

*Ref: Enabling Microservice Success.md — "Chaos Engineering" (Ch. 12), "Validating Your Resilience Choices" (Ch. 12)*

---

### 24. Testing Strategy: Pyramid + Contract + Testing in Production

**Principle:** In a microservice architecture, end-to-end tests in staging become a distributed monolith. Replace them with unit/service tests + contract tests + synthetic monitoring in production.

**Do:**
- Follow the **testing pyramid**: many unit tests, fewer service tests, very few end-to-end tests.
- Write tests for both happy path and failure cases — including **slow responses**.
- Test the *service* including its data store (the database is part of your contract).
- Use **contract tests** (Pact-style) at team boundaries — consumers define expectations, providers verify.
- Run **synthetic monitoring** in production for key business flows — it's testing, not just monitoring.
- Separate **deploy** from **release** with feature flags, canary releases, and blue-green deployments.
- Run **coherence tests** that check data as it flows through services.
- Aim for **mutation-resistant** tests: tests that would fail if the code changed unexpectedly (verify your `==` is really an `==`).

**Don't:**
- Don't build large suites of acceptance tests that require data fixtures in many services — they couple everything together.
- Don't try to replicate production in staging — you can't, and the maintenance cost will dominate.
- Don't set coverage targets (e.g., 80%) — they incentivise low-value tests for simple code. Focus on complex code.
- Don't rely on staging for production-like testing — use production itself, with progressive rollout and good observability.

**Code / Notes:**
```
Testing pyramid (Mike Cohn):
       /\        ← E2E tests: few, slow, brittle, but catch integration issues
      /  \          (in production, treat the system as a black box)
     /────\      
    /      \    ← Service tests: per microservice, in-process, fast
   /        \  
  /──────────\ ← Unit tests: most numerous, sub-second, TDD
```

*Ref: Enabling Microservice Success.md — "Getting Value from Testing" (Ch. 10)*

---

### 25. Feature Flags, Canary Releases, A/B Testing

**Principle:** Decouple deployment from release so you can roll forward, roll back, or run experiments at will.

**Do:**
- Wrap new functionality in **feature flags** that can be toggled without a redeploy.
- Set **expiration dates** on feature flags (people will extend them; that's why you check).
- Use **canary releases**: 1% → 10% → 50% → 100%, watching error rates and key metrics.
- Use **A/B testing** for hypothesis validation (Linda Rising: experiments have a hypothesis, can fail, and have a control group).
- Use **blue-green deployments** with shared database (keep changes backward compatible).
- Practice **roll forward** — a small fix to a recent change is faster than a rollback.

**Don't:**
- Don't leave feature flags in code forever — they create combinatorial complexity.
- Don't batch unrelated changes to avoid coordination — it makes diagnosis harder.
- Don't deploy on Friday only because your deploy process is flaky — fix the process.

*Ref: Enabling Microservice Success.md — "Feature flags", "Canary releases", "A/B testing" (Ch. 10), "Release on Demand" (Ch. 8)*

---

### 26. Continuous Delivery, Deployment Pipelines, and "Release on Demand"

**Principle:** Multiple-times-a-day releases require automated build, test, and deploy pipelines — and the team that wrote the code must own the deploy button.

**Do:**
- Invest in **CI/CD** as a prerequisite to microservices; manual deploys won't scale.
- Use **trunk-based development** or very short-lived branches — code is never in an unreleasable state.
- Run **automated tests** (unit, contract, security scans) on every commit.
- Integrate **dependency scanning** (Dependabot, Snyk) directly into PRs.
- Allow teams to deploy when *they* decide it's ready — not on a central schedule.
- Combine release on demand with **change logs** (a Change API) that records who deployed what when, posted to a Slack channel.

**Don't:**
- Don't keep a CAB (change advisory board) — research shows it slows releases without improving quality.
- Don't deploy from a single shared staging environment with multiple teams — coordination bottlenecks.
- Don't skip code freezes by sneaking changes in — fix the change-management problem.

*Ref: Enabling Microservice Success.md — "Continuous Delivery" (Ch. 1), "Effective Software Delivery" (Ch. 2)*

---

### 27. DORA Metrics: Measuring Effective Software Delivery

**Principle:** The four DORA metrics — deployment frequency, lead time, change failure rate, time to restore service — are the most useful baseline for measuring delivery effectiveness.

**Do:**
- Track all four DORA metrics from day one if you have low baseline scores.
- Focus on **outcomes**, not output — frequency of *business value* shipped, not raw commits.
- Use DORA at team level, not individual level.
- When DORA scores are already high, switch to **SPACE** for developer productivity (Satisfaction, Performance, Activity, Communication, Efficiency).
- Pair DORA with business metrics: did the feature move the needle for customers?
- Avoid composite scores that hide context.

**Don't:**
- Don't tie bonuses to individual productivity metrics — it destroys teamwork.
- Don't use DORA as a target — Goodhart's Law: "when a measure becomes a target, it ceases to be a good measure."
- Don't rely on DORA alone — high DORA scores can mask a system that delivers no business value.

*Ref: Enabling Microservice Success.md — "Effective Software Delivery" (Ch. 2), "Measuring Impact" (Ch. 7)*

---

### 28. SPACE Framework for Developer Productivity

**Principle:** Developer productivity is multidimensional; you can't measure it with a single number.

**Do:**
- Track all five SPACE dimensions:
  - **S**atisfaction & well-being
  - **P**erformance (high-quality, high-impact code)
  - **A**ctivity (PRs, commits, releases, incidents)
  - **C**ommunication & collaboration
  - **E**fficiency & flow
- Use regular surveys for the qualitative dimensions (satisfaction, communication, flow).
- Use dashboards to surface *trends* for individuals and teams — never rank teams.
- Tie SPACE insights back to OKRs (e.g., teams that can't take on observability OKRs are overloaded).

**Don't:**
- Don't try to combine SPACE dimensions into a single score.
- Don't compare teams competitively — it kills psychological safety.

*Ref: Enabling Microservice Success.md — "Measuring Impact" (Ch. 7)*

---

### 29. Westrum Generative Culture: Open, Learning, Empowering, Change-Optimised

**Principle:** Microservices need a culture that shares information, encourages experimentation, and trusts teams to make decisions. Westrum's "generative" culture is the model.

**Do:**
- Foster **openness** — default to sharing information; broadcast rather than hide.
- Reward **learning** — give time and budget for it (10% time, communities of practice, training).
- **Empower** teams — remove barriers between teams and production.
- Build for **change** — reorg-friendly structure; reward managers for keeping the team lean and adaptable.
- Apply John Shook's lesson: "the way to change culture is to change what people do, not what they think."
- Build blameless culture: people share bad news early because they trust the response.

**Don't:**
- Don't punish messengers of bad news.
- Don't hoard information across silos (Westrum's "pathological" culture).
- Don't refuse to fund learning — it shows in retention.

*Ref: Enabling Microservice Success.md — "Organizational Culture" (Ch. 5), "The Westrum Model"*

---

### 30. Dan Pink's Motivation: Autonomy, Mastery, Purpose

**Principle:** Engineering teams respond best to intrinsic motivation: autonomy over what to do, mastery opportunities, and a purpose they care about.

**Do:**
- Give teams **autonomy**: pick your tech, decide when to release, set your own OKRs.
- Provide **mastery**: communities of practice, secondments, 10% time, internal tech conferences.
- Connect work to **purpose**: explicit outcomes ("March to 1 million subscribers") translated to team-level objectives.
- Avoid John Cutler's **Feature Factory**: where developers ship features but no one knows if they worked.
- Make sure autonomy and psychological safety both exist — they're complementary, not interchangeable.

**Don't:**
- Don't demotivate teams by treating them as interchangeable resources.
- Don't promise mastery by exposing people to nothing new.
- Don't decouple purpose from outcomes — "build this feature" is not purpose.

*Ref: Enabling Microservice Success.md — "Motivated through Autonomy, Mastery, and Purpose" (Ch. 5)*

---

### 31. Team Size: 5–9 People, Groups of 50–150 (Dunbar)

**Principle:** Communication overhead grows quadratically with team size. Effective software teams are 5–9; effective groups are 50–150 (Dunbar).

**Do:**
- Size stream-aligned teams at **5–9** (Team Topologies recommendation; aligns with Amazon's two-pizza team).
- Form groups of **50–150** so team-lead meetings, 24/7 rotas, and shared learning remain tractable.
- Acknowledge that within a group, teams share related technology and can share on-call rotas.
- Recognise that adding people to a late project makes it later (Brooks's Law).

**Don't:**
- Don't grow teams beyond ~10 — they fracture into sub-teams.
- Don't create groups larger than 150 — they fragment into silos.
- Don't tie team size to architecture diagrams — Conway's Law goes the other way.

*Ref: Enabling Microservice Success.md — "Appropriately Sized Teams" (Ch. 5), "Part of a Group"*

---

### 32. Long-Lived, Stable Teams (Tuckman's Forming-Storming-Norming-Performing)

**Principle:** Teams take months to become effective. Don't break up teams for short-term projects.

**Do:**
- Treat teams as **products**, not projects — long-lived, owned for the lifetime of the service.
- Allow turnover but maintain the team's domain ownership.
- Recognise Tuckman's stages: forming → storming → norming → performing. Invest in the middle.
- Move people *between* teams gradually and with care — sudden reorgs destroy trust.
- Build **collective ownership within the team** so no service has a single bus factor.

**Don't:**
- Don't form teams for individual projects and disband them.
- Don't rotate people constantly — psychological safety (the #1 factor in Google's Project Aristotle) takes time.

*Ref: Enabling Microservice Success.md — "Long Lived" (Ch. 5)*

---

### 33. Cross-Functional, T-Shaped, and "Capability Comb" Engineers

**Principle:** Stream-aligned teams need all the skills to take a feature to production. Build T-shaped engineers (or "Capability Comb"-shaped) with depth plus breadth.

**Do:**
- Include in each stream-aligned team: design, coding, testing, infra/deployment, ops, observability.
- Aim for **T-shaped** engineers: depth in one area, breadth across others.
- Treat QAs as part of the team from day one (not a separate phase).
- Provide opportunities to learn adjacent skills through pair programming, secondments, 10% time.
- Recruit for adaptability over narrow specialism.

**Don't:**
- Don't have a single skill type on a team (e.g., all backend engineers, no operations).
- Don't treat breadth as a substitute for depth.

*Ref: Enabling Microservice Success.md — "Cross-Functional and T-shaped" (Ch. 5), Emily Webber's "Capability Comb" exercise*

---

### 34. Cognitive Load: Germane, Intrinsic, Extrinsic

**Principle:** Total cognitive load matters. Reduce *extrinsic* load (build pipelines, processes) so teams can carry more *germane* load (the actual business problem).

**Do:**
- Apply the three cognitive-load types:
  - **Germane** — domain understanding. Encourage it.
  - **Intrinsic** — inherent difficulty (e.g., the language). Invest in training, communities of practice.
  - **Extrinsic** — incidental complexity (CI config, deploy steps). Reduce it via platform engineering.
- Aim for sustainable load — teams should not be context-switching constantly.
- Use secondments to spread domain knowledge across teams.

**Don't:**
- Don't treat "more work for the team" as a virtue — context switching has real cost.
- Don't pile on extrinsic load by adding new tools without retiring old ones.

*Ref: Enabling Microservice Success.md — "Sustainable Cognitive Load" (Ch. 5)*

---

### 35. Psychological Safety (Project Aristotle)

**Principle:** The single biggest predictor of team effectiveness is psychological safety — the belief that you can take risks and be vulnerable without punishment.

**Do:**
- Build **psychological safety** explicitly: blameless postmortems, no retaliation for raising incidents.
- Recognise the five dynamics from Google's Project Aristotle: psychological safety, dependability, structure & clarity, meaning, impact.
- Tie these to autonomy, mastery, purpose (Dan Pink).
- Allow people to admit they don't know something.
- Use written communication norms that are kind and specific (e.g., "Don't say 'just' or 'simply'").

**Don't:**
- Don't confuse low-conflict with high-safety — high-safety teams debate vigorously and disagree openly.
- Don't blame individuals for incidents — even when the human error is real.

*Ref: Enabling Microservice Success.md — "High Trust and High Psychological Safety" (Ch. 5)*

---

### 36. Conway's Law vs Gall's Law: Start Simple

**Principle:** "A complex system that works is invariably found to have evolved from a simple system that worked." — Gall's Law. Start with a monolith.

**Do:**
- Apply **Gall's Law** to all new systems: start simple, evolve.
- Start with a **monolith** (or modular monolith) for a new system — you don't yet understand the domain.
- Recognise that "microservices tax" is real: build, deploy, and operate each service has overhead.
- Move to microservices when:
  - Multiple teams need to work in parallel.
  - Different parts need different scaling.
  - Different compliance / security needs emerge.
  - Different tech choices become valuable.
- Apply the **Design Stamina Hypothesis** (Martin Fowler): don't invest in architecture before product-market fit.

**Don't:**
- Don't start greenfield with microservices — you don't know the boundaries yet.
- Don't think microservices are the only option — modular monoliths can solve many of the same problems.
- Don't ignore Gall's Law just because you have funding.

*Ref: Enabling Microservice Success.md — "Starting from Scratch" (Ch. 3), "Sticking with a Monolithic Architecture"*

---

### 37. Brownfield Migration: Strangler Fig Pattern and the Shopify Modular Monolith

**Principle:** Migrate incrementally — extract services from the monolith one by one using the Strangler Fig pattern. Avoid big-bang rewrites.

**Do:**
- Use the **Strangler Fig pattern** (Martin Fowler): new system grows around the old; old system supports until the new can stand alone.
- Start with **coarse-grained services** to minimise operational overhead.
- Pick services under **active development** first — the migration effort is justified by the value of independent deployability.
- Be prepared to **rewrite** a service in the receiving team's preferred tech if the original tech is unknown to them.
- Set explicit **decommission dates** for migrated services — leaving the old running indefinitely is expensive.
- Use the **Shopify modular monolith** pattern when you want loose coupling without distributed-system overhead: same codebase, same deploy, but logical domain boundaries enforced by tooling.

**Don't:**
- Don't do big-bang rewrites. The FT's 2015 website rebuild cost £10M and yielded nearly two years of no improvement.
- Don't pick static, low-change modules to extract first — pick modules with active churn.
- Don't keep an old service running past its expiry — pay the migration cost once.

*Ref: Enabling Microservice Success.md — "Case Study: Shopify's Modular Monolith" (Ch. 3), "Replacing an Existing Monolith"*

---

### 38. Greenfield Adoption: Start Modular Monolith, Extract as You Learn

**Principle:** For a brand-new system, start with a modular monolith. Extract services when you can articulate a clear boundary AND have multiple teams.

**Do:**
- Begin with a **single monolith** (or a small number of monoliths).
- Build it with **logical module boundaries** matching future bounded contexts.
- Extract when one of these conditions emerges:
  - Multiple teams need to work in parallel on the same domain.
  - A module has substantially different scaling, security, or compliance needs.
  - A module has substantially different technology needs.
- Use the **Strangler Fig** to extract.
- Lean on **public cloud / serverless** to defer platform investment.

**Don't:**
- Don't start with microservices — you'll pay the tax without knowing the boundaries.
- Don't extract too eagerly — every service has overhead (deploy pipeline, monitoring, on-call, runbook).
- Don't underestimate the value of having all code in one repo for early exploration.

*Ref: Enabling Microservice Success.md — "Starting from Scratch" (Ch. 3)*

---

### 39. Investment Thesis: Why Microservices? (DORA, Flow, Cost of Rewrites)

**Principle:** Justify microservices adoption with a clear business reason — usually flow, scale, or flexibility — and accept that the move takes years.

**Do:**
- Tie the move to **DORA metrics**: more frequent, smaller, safer releases.
- Recognise the four DORA metrics:
  - **Deployment frequency**
  - **Lead time for changes**
  - **Change failure rate**
  - **Time to restore service**
- Frame the goal as **continuous evolution** — microservices should let you replace parts without big-bang rewrites.
- Get explicit **leadership support**: this is a multi-year organisational change.
- Show the cost of *not* moving: how many hours are wasted on coordination; how often do features slip because of coupling.
- Communicate progress in business terms, not just technical terms.

**Don't:**
- Don't adopt microservices "because everyone is doing it" — have a real business reason.
- Don't expect short-term wins — the medium-term sweet spot (around the time releases become on-demand) is where the value shows.
- Don't move without buy-in from leadership and team leads — the cultural change is the hard part.

*Ref: Enabling Microservice Success.md — "Effective Software Delivery" (Ch. 2), "Reasons to Choose Microservices" (Ch. 3)*

---

### 40. Vendor vs Internal Platform: Buy, Lease, or Build?

**Principle:** Outsource undifferentiated heavy lifting (Werner Vogels). Build only for differentiating capabilities.

**Do:**
- Apply the **Wardley Map**: differentiate at the top of the value chain; buy or rent at the bottom.
- Use **public cloud** managed services (RDS, EKS, Lambda) over building your own clusters.
- Consider **PaaS** (Heroku, Render, fly.io) for simple applications to remove platform overhead.
- Use **SaaS** for things that aren't business differentiators (auth, monitoring, error tracking).
- Build a platform only where the cloud doesn't serve your specific needs.
- Use **serverless** (FaaS) for event-driven, intermittent workloads.

**Don't:**
- Don't build what you can rent or buy — unless the cost or compliance makes it necessary.
- Don't use Kubernetes just because it's popular — it's powerful but complex. Consider PaaS or serverless first.
- Don't pretend you're "multi-cloud" — commit to one provider and use its managed services deeply.

*Ref: Enabling Microservice Success.md — "Building a Platform" (Ch. 7), "New Deployment Options" (Ch. 1), "Serverless" (Ch. 1)*

---

### 41. Choose Boring Technology (Dan McKinley, Innovation Tokens)

**Principle:** Boring technology is well-understood; failure modes are well-documented. Spend your innovation tokens on what matters to the business.

**Do:**
- Limit "innovation tokens": every new tech choice (data store, language, orchestrator) costs one.
- Use **established** tech by default — its failure modes are Google-able.
- Prefer **commodity** over **product** over **custom-built** unless the benefit justifies the cost.
- Save innovation for things that are **business differentiators**.
- Re-evaluate technology choices as the lifecycle moves (Simon Wardley: Genesis → Custom-Built → Product → Commodity).
- Move to managed services as they become available — the FT moved from custom container orchestration to Kubernetes to managed Kubernetes.

**Don't:**
- Don't pick a bleeding-edge database because the team is excited — failure modes may be unknown.
- Don't keep custom-building once a managed product is available.
- Don't add a second programming language casually.

*Ref: Enabling Microservice Success.md — "Use Boring Technology", "Limit the Alternatives" (Ch. 11), Dan McKinley's "Choose Boring Technology"*

---

### 42. Nudge Theory (EAST Framework) for Engineering Change

**Principle:** Use behavioural economics to influence teams toward good outcomes without mandating them.

**Do:**
- Apply the **EAST** framework for nudges:
  - **Easy** — clear instructions, easy first step, defaults, removing friction.
  - **Attractive** — attention-grabbing, personal incentives.
  - **Social** — describe what peers are doing; show team progress on dashboards.
  - **Timely** — prompt when most relevant (e.g., in PR templates); avoid asking during crunches.
- Use defaults where possible (opt-out > opt-in).
- Make small changes for big impact — UK organ donation framing added ~100k registrations/year from a single text change.
- Make commitments **public** — OKRs, dashboards, showcases.

**Don't:**
- Don't mandate changes top-down without explanation — adoption follows comprehension.
- Don't ignore loss aversion — people respond more to "you'll lose X" than "you'll gain Y."
- Don't add friction (waiting for PR approval, manual steps) and expect compliance.

*Ref: Enabling Microservice Success.md — "Empathy" (Ch. 14), Nudge Unit EAST framework*

---

### 43. Communication: Multiple Channels, Repeat, Check Receipt

**Principle:** "Transmission is not communication." Plan comms to survive holidays, missed meetings, and skim-readers.

**Do:**
- Apply **Alia Rose Connor's stages of communication**: transmission, received, understood, agreed, actioned. You lose people at each transition.
- Use **multiple channels** — Slack, email, posters, all-hands, blog posts.
- **Repeat** the message — being told you're repetitive probably means you're getting it about right.
- Check for receipt — confirmations, replies.
- Be specific: what people need to do, by when, what happens if they don't.
- For big migrations, address emails to specific tech leads or product owners.
- Use **OKRs** that mirror the change in other teams' plans — public commitment drives completion.

**Don't:**
- Don't rely on one channel.
- Don't assume silence = agreement.

*Ref: Enabling Microservice Success.md — "Communication" (Ch. 14)*

---

### 44. Brownfield Adoption: Frictionless Onboarding and "Try It Out" Cultures

**Principle:** Cultural change beats technological change. Start small, prove value, scale.

**Do:**
- Use **trial projects**: extract one service, automate one pipeline, introduce CD for one team.
- Allow **pilots** of new tech by enthusiasts before mandating.
- Find **enthusiasts** in each team to seed the change.
- Make the paved road **demonstrably better** than going off road — so opt-out isn't an attractive path.
- Use **internal DevRel** (Daniel Bryant) — showcase wins, write blog posts, run hack days.
- Provide **opt-out paths** that aren't punishing — gives a market signal.

**Don't:**
- Don't mandate new tech with no trial period.
- Don't treat early adopters as lab rats — celebrate their work.
- Don't underestimate how long culture change takes.

*Ref: Enabling Microservice Success.md — "Managing Change" (Ch. 3), "Market It" (Ch. 7)*

---

### 45. Adoption Ladder: From "Aware" to "Evangelist"

**Principle:** Different stakeholders need different things from the change. Map your comms to where each stakeholder is.

**Do:**
- Recognise the typical adoption ladder:
  - **Aware** — they know the change is happening.
  - **Understanding** — they know why.
  - **Trial** — they've tried it.
  - **Adoption** — they're using it.
  - **Evangelist** — they're selling it to others.
- Tailor your comms by stage: awareness via all-hands, understanding via deep-dives, trial via office hours, adoption via paved-road migration, evangelism via showcases and blog posts.
- Apply **Diffusion of Innovations** (Everett Rogers): Innovators → Early Adopters → Early Majority → Late Majority → Laggards.
- Use social proof — quotes, case studies, internal blog posts from early adopters.

**Don't:**
- Don't assume the same message works for everyone.
- Don't ignore the Laggards — sometimes they're the canaries.

*Ref: Enabling Microservice Success.md — "Change Management" (Ch. 14), Everett Rogers diffusion of innovations model*

---

### 46. Maturity Model: Five Stages from "Surviving" to "Innovating"

**Principle:** Most organisations move through predictable stages of microservices maturity. Know where you are and what the next investment is.

**Do:**
- Recognise the typical stages (after Westrum / DORA / Gene Kim):
  1. **Reactive** — manual everything, fire-fighting.
  2. **Repeatable** — some automation, basic CI, project-by-project.
  3. **Defined** — standardised CI/CD, paved road, autonomous teams.
  4. **Managed** — automated governance, observability-driven operations, SLOs.
  5. **Optimising / Innovating** — chaos engineering, continuous improvement, generative culture.
- Use the book's **Appendix A: Microservices Assessment** to score where you are.
- Tackle prerequisites first (CI/CD, IaC, observability, team autonomy) before microservices.

**Don't:**
- Don't try to skip stages.
- Don't confuse activity with progress — *automated* observability is stage 4, not "we have dashboards."

*Ref: Enabling Microservice Success.md — Appendix A "Microservices Assessment"*

---

### 47. Federation at Scale: Monzo, Skyscanner, and Other Orgs

**Principle:** Different organisations solve the same problems differently. Steal principles, not implementations.

**Do:**
- **Monzo** (challenger bank, 1,600+ microservices): risk-based governance, automation-first, mandatory yearly training, three lines of defence with first-line embedded in engineering groups.
- **Skyscanner** (travel, 1,200 people): CloudFormation-only via CFRipper, mandatory metadata service, CloudZero cost tracking per team, "Change Tokens" to limit parallel technical change.
- **Starling Bank** (digital bank): zero-trust VPC, crypto validation only within hardened perimeters.
- **Spotify**: paved road (separate for backend and frontend), Backstage portal, scaffolder.
- Pick the model that matches your scale and risk appetite.

**Don't:**
- Don't copy a model without understanding its prerequisites.
- Don't assume your regulatory environment lets you adopt Monzo's level of automation.

*Ref: Enabling Microservice Success.md — "Governance at Monzo", "Governance at Skyscanner", Case studies across chapters*

---

### 48. Pitfalls: The Anti-Patterns of Microservices Adoption

**Principle:** Recognise the common traps before you fall into them.

**Do:**
- Watch for these pitfalls:
  - **Distributed monolith** — services coupled by shared staging, lockstep deploys, E2E test fixtures in every service.
  - **Haunted forests** — services no one has touched in years, no one can debug.
  - **Alert overload** — cascades of alerts that hide the real signal.
  - **Cattle turned back into pets** — long-lived servers requiring manual care.
  - **Tower of Babel** — too many programming languages with no strategic reason.
  - **Migration long tail** — 5 services still on Java 8 because no one got around to it.
  - **Bypass-the-paved-road sprawl** — every team has a custom CI tool.
  - **Unowned services** — "feature complete" with no team responsible for security patches.
  - **Passive monitoring** — dashboards no one looks at.
  - **Notification fatigue** — alerts that no one reads.
  - **Incident counts as KPI** — people hide incidents to protect bonuses.
  - **Local optimisation** — every team picks a new data store.

**Don't:**
- Don't accept any of these as "just the way it is."
- Don't let a pitfall become normalised before someone names it.

*Ref: Enabling Microservice Success.md — "Pitfalls" sections throughout*

---

### 49. Federated Architecture Decisions: Principal Engineer as Enabler

**Principle:** Architects enable, not dictate. Ruth Malan: "if we have managers deciding … which services will be built, by which teams, we implicitly have managers deciding on the system architecture."

**Do:**
- Embed architecture within each team.
- Have **principal engineers** (Tanya Reilly's "Staff Engineer's Path") who enable and "survey the landscape" without being gatekeepers.
- Use **Architecture Decision Records (ADRs)** for significant decisions.
- Rotate architects through teams to spread knowledge.

**Don't:**
- Don't have a central architecture team mandating tech choices without context.
- Don't confuse "architect" (a role) with "architecture" (something everyone does).

*Ref: Enabling Microservice Success.md — "The Role of the Individual Contributor" (Ch. 6)*

---

### 50. Migration Long-Tail Discipline

**Principle:** Migration is incomplete until decommissioned. Don't let the long tail grow.

**Do:**
- Set explicit **decommission dates** from the start.
- Embed migration work in teams' quarterly OKRs.
- Use dashboards to show progress and identify stragglers.
- Pair migration work with regular feature work ("upgrade-as-you-touch").
- Use "firebreak weeks" (Monzo) for focused maintenance.
- Be willing to escalate to leadership when a team won't schedule the work.
- Consider "you can keep using it, but you own it" as a last resort.

**Don't:**
- Don't leave old systems running "just in case" — they're a security risk and ongoing cost.
- Don't let migration become a long tail of partially-migrated services.

*Ref: Enabling Microservice Success.md — "Managing Change" (Ch. 14)*

---

### 51. Secondments, Communities of Practice, Internal Conferences

**Principle:** Spread knowledge across teams deliberately — don't wait for attrition to spread it.

**Do:**
- Use **secondments** (3-month rotations) to share specialist knowledge between teams.
- Run **communities of practice** for skills that cross teams (security, observability, accessibility).
- Run **internal tech conferences** (Capital One had 1,200 employees at theirs, with 13 learning tracks).
- Host **tech talks** with both internal and external speakers.
- Use **10% time** for exploration with a public show-and-tell.
- Pair-program across teams for capability transfer.

**Don't:**
- Don't let specialists hoard knowledge — it creates bus-factor risk.
- Don't undervalue internal conferences as "real work."

*Ref: Enabling Microservice Success.md — "Making Space for Learning" (Ch. 6)*

---

### 52. Operational Sustainability: Reduce Toil, Increase Joy

**Principle:** Automate toil; preserve the interesting work. People leave when they spend months upgrading dependencies.

**Do:**
- Define **toil** (Google SRE): manual, repetitive, automatable, tactical, devoid of enduring value, scales linearly.
- Invest in automation that removes toil (e.g., automated PR creation for library upgrades).
- Use the **paved road** to absorb upgrades centrally.
- Recognise that investing 20% of engineering capacity in technical work is healthy (Marty Cagan).
- Use **Kanban lanes** for technical work so product owners see the balance.

**Don't:**
- Don't let toil dominate an engineer's life — it's a retention risk.
- Don't dismiss "boring" work as unimportant — it's the floor on which everything else is built.

*Ref: Enabling Microservice Success.md — "Spending Most of Your Time on Meaningful Work" (Ch. 2), Marty Cagan's "Engineering Wants to Rewrite"*

---

### 53. Data Strategy: Eventual Consistency, Sagas, and Service Ownership

**Principle:** Co-locate data with the service that owns it. Plan for eventual consistency. Avoid distributed transactions.

**Do:**
- Keep data that changes together in the same service.
- Accept **eventual consistency** at the system level.
- Use **idempotent operations** (publish, republish) so retries are safe.
- Use **Saga pattern** with compensating transactions only when truly necessary.
- Duplicate data (e.g., customer name in the Order service) to avoid chatty calls.
- Use **cache timeouts** or **change notifications** to keep duplicated data fresh.
- Define **canonical sources** for each piece of data.
- Use **outbox pattern** for reliable event publishing from a database.
- **Test your backups** regularly.

**Don't:**
- Don't share databases across services — they become a coupling point.
- Don't try to use distributed transactions in a microservice architecture.
- Don't let data ownership drift — every piece of data must have a canonical owner.

*Ref: Enabling Microservice Success.md — "Data" (Ch. 1), "Data Consistency" (Ch. 1), "Backup and Restore" (Ch. 12)*

---

### 54. Security in Depth: Zero-Trust, PII Segregation, Dependency Scanning

**Principle:** In a distributed system, every service is a potential entry point. Build zero-trust architecture and segregate sensitive data.

**Do:**
- Apply **zero-trust** at the network layer: every service must verify callers.
- Segregate **PII data** to a specific service with specific credentials.
- Use **API gateways** to centralise auth, throttling, and rate-limiting.
- Rotate credentials frequently; use secret managers.
- Scan dependencies for vulnerabilities on every PR (Snyk, Dependabot).
- Test that your incident response works for security events (Log4Shell case study).
- Maintain an up-to-date dependency inventory (your service catalog can help).
- Have security engineers embedded as enabling-team members.

**Don't:**
- Don't assume services inside your perimeter are trustworthy.
- Don't store PII in logs that get forwarded to error-tracking tools.
- Don't rely on a single credential across services.

*Ref: Enabling Microservice Success.md — "Security" (Ch. 1), "Responding to the Log4Shell Vulnerability" (Ch. 9)*

---

### 55. Documentation as Code, in the Repo

**Principle:** Documentation that lives next to code is more likely to stay current. But don't over-engineer it.

**Do:**
- Keep **runbook information in the code repo** (markdown that ships on release).
- Use PR templates that include a "documentation updated?" checkbox.
- Annual manual reviews of runbook accuracy for critical services.
- Add a "last reviewed" date to each runbook section.
- Link from the runbook directly to live logs, metrics, and dashboards.

**Don't:**
- Don't trust unsynchronised wikis — they'll rot.
- Don't rely solely on automated checks — they can't verify accuracy.
- Don't make documentation changes too friction-filled (the FT's Markdown-in-repo approach was abandoned because it was too fiddly).

*Ref: Enabling Microservice Success.md — "Maintaining Useful Documentation" (Ch. 13)*

---

### 56. Dependency Scanning and Software Bill of Materials (SBOM)

**Principle:** With hundreds of services and transitive dependencies, you must know what's running and where.

**Do:**
- Maintain an **SBOM** (Software Bill of Materials) for each service, ideally auto-generated.
- Scan dependencies on every PR (Snyk, Dependabot, GitHub Advanced Security).
- Output language/library versions to logs or metrics on startup (so dashboards show production usage).
- Track Java/Python/Node major version distribution across the estate.
- Have a **vulnerability response process** (assign owners, set deadlines, run like an incident).

**Don't:**
- Don't let scanning drown teams in noise — focus on high-risk vulnerabilities within an actionable window.
- Don't forget transitive dependencies — the Log4Shell story was about transitive exposure.

*Ref: Enabling Microservice Success.md — "Dependencies" (Ch. 9)*

---

### 57. Cost Management and FinOps Awareness

**Principle:** Cloud spend scales linearly with adoption. Make cost visible to engineers.

**Do:**
- Tag every cloud resource with **system code** and owning team.
- Show teams their cost in dashboards.
- Use **spot instances** for fault-tolerant workloads (Skyscanner).
- Implement **auto-shutdown** for non-production environments (60% saving typical).
- Provide **cost-optimisation tooling** (right-sizing, Graviton, savings plans).
- Run **TCO analysis** for new services — compare build vs. buy vs. leave alone.
- Treat cost surprises as a governance issue (someone deployed something they shouldn't have).

**Don't:**
- Don't hide costs from engineers — visibility drives better decisions.
- Don't gold-plate resilience for non-critical services.

*Ref: Enabling Microservice Success.md — "Cost management" (Ch. 11)*

---

### 58. Wardley Maps for Investment Decisions

**Principle:** Combine a value chain with the technology evolution cycle to decide where to innovate, buy, or rent.

**Do:**
- Map your value chain: user needs → capabilities → underlying technologies.
- Plot each capability on the **evolution cycle** (Genesis → Custom-Built → Product → Commodity).
- Innovate only at the **top of the value chain** where it provides competitive advantage.
- Buy **product-grade** capabilities off the shelf.
- Use **commodity** capabilities without thinking (compute, storage).
- Re-evaluate as technology evolves.

**Don't:**
- Don't innovate at the foundation of the value chain — there are no competitive advantages there.
- Don't custom-build what a product offers.

*Ref: Enabling Microservice Success.md — "Save Innovation for Key Business Outcomes" (Ch. 11), Simon Wardley's maps*

---

### 59. Pace of Change: From Projects to Products

**Principle:** Long-term product ownership beats short-term project funding for software that has to be maintained.

**Do:**
- Fund teams by **product** rather than project.
- Keep teams stable across the lifetime of the service.
- Treat "feature complete" as the *start* of the ownership phase, not the end.
- Recognise Mik Kersten's **Project to Product** shift: teams own outcomes, not deliverables.

**Don't:**
- Don't disband teams after delivery — the code still needs owning.
- Don't measure teams by features shipped without ongoing ownership.

*Ref: Enabling Microservice Success.md — "Products Not Projects" (Ch. 3), Mik Kersten's "Project to Product"*

---

### 60. Blameless Culture in Action

**Principle:** You learn from incidents only when people feel safe to share. Blameless postmortems are a practice, not a slogan.

**Do:**
- Hold **blameless postmortems** with clear structure.
- Replace "who broke this" with "what conditions allowed this to happen?"
- Use **timeline-based** reviews — show pinned Slack messages automatically.
- Capture **surprises** (where was our understanding wrong?) and **"where we got lucky"** (e.g., "Steve happened to be online").
- Limit **agreed actions** to 1–2 per incident.
- Tie incident learnings to OKRs.

**Don't:**
- Don't name-and-shame — even "implied" blame destroys psychological safety.
- Don't skip postmortems for "obvious" incidents.
- Don't accept 10-action incident reviews — they don't get done.

*Ref: Enabling Microservice Success.md — "Blameless Culture" (Ch. 8)*

---

## Anti-Patterns & Common Mistakes

- **Distributed Monolith:** Services coupled by shared staging, lockstep deploys, end-to-end test fixtures in every service. *Fix:* Decouple with contract tests + independent deploys + per-service test data.
- **Haunted Forests:** Services no one understands, with outdated runbooks. *Fix:* Identify via the haunted-forest table (Ch. 8), then refactor or rewrite.
- **Alert Cascade:** Every dependency failure triggers alerts in all upstream services. *Fix:* Alert at the customer entry point; use healthchecks that return 200 even when checks fail.
- **Cattle Turned Back into Pets:** Long-lived servers with manual fixes. *Fix:* Immutable infrastructure; replace don't patch.
- **Migration Long Tail:** 5 services still on Java 8 three years after migration started. *Fix:* Decommission dates; pair-with-feature upgrades; firebreak weeks.
- **Notification Fatigue:** Alerts that no one reads. *Fix:* Delete noisy alerts; alert on SLO breaches not component health.
- **Passive Monitoring:** Dashboards that no one looks at. *Fix:* Tie dashboards to on-call; make them the entry point for incidents.
- **Incident Counts as KPI:** People hide incidents. *Fix:* Remove the metric; reward openness.
- **Feature Factory:** Teams ship features but no one knows if they worked. *Fix:* Connect work to outcomes (engagement, revenue).
- **Tower of Babel:** Every team has a new language with no strategic reason. *Fix:* TGG process; "innovation tokens" limit.
- **Bypass-the-Paved-Road Sprawl:** Every team has a custom CI/CD pipeline. *Fix:* Make the paved road genuinely better; provide migration assistance.
- **Unowned Services:** "Feature complete" but no team responsible for upgrades. *Fix:* Service catalog forces ownership; periodic reassignment.
- **CAB Slowdown:** Change advisory board bottlenecks releases. *Fix:* Replace with automated pipelines + light-touch governance.
- **Local Optimisation:** Every team picks a different data store. *Fix:* TGG; "Limit the Alternatives" guidance.
- **Hidden Coupling via Shared DB:** Services writing to the same database "because it's easier." *Fix:* Service-owned data; CQRS or event-driven sync.
- **Synchronous Chains:** A→B→C→D all synchronous. *Fix:* Insert queues; set time budgets at ingress.
- **Open-World Defaults:** Services default to permissive; security relies on perimeter. *Fix:* Zero-trust; mTLS; per-call auth.
- **Local Documentation Silos:** Runbooks only known by one engineer. *Fix:* Standard template; annual reviews; in-repo docs.

### 61. Case Study: FT Content Platform Evolution — 12 Releases/Year to 2,500+ Releases/Year

**Principle:** The transformation from slow, manual monolith releases to fast, automated microservice releases is achievable in months, not years — provided the prerequisites are in place.

**Do:**
- Mirror the FT's success path:
  1. Move from manual server provisioning to IaC (FT: started with private cloud IaaS, then moved to public cloud).
  2. Automate the deployment pipeline (50+ manual steps → automated).
  3. Containerise (FT: reduced AWS costs by 40% by consolidating onto fewer, larger VMs).
  4. Adopt continuous delivery (FT: 12 releases/year → 2,500 releases/year).
  5. Split into microservice teams aligned to business domains.
- Recognise that the **largest jump in productivity** comes from automating deployment, not from microservices themselves.
- Use **small early wins** to prove the case: one team, one service, one pipeline.

**Don't:**
- Don't try to do all five steps at once.
- Don't claim "we're doing microservices" without the deployment automation to back it up.

*Ref: Enabling Microservice Success.md — "Infrastructure as Code", "Continuous Delivery" (Ch. 1), "Effective Software Delivery" (Ch. 2)*

---

### 62. Case Study: FT Biz Ops Log4Shell Response (Zero-Day in 36 Hours)

**Principle:** Active ownership plus a well-modelled service catalog lets you respond to zero-day vulnerabilities in hours, not weeks.

**Do:**
- When Log4Shell hit Java services at the FT, they responded because:
  - Every service had a Biz Ops record with an owning team.
  - The graph linked GitHub repos to systems to teams.
  - A GraphQL query found all Java services in minutes.
  - The platform team ran it like an incident with status comms to the whole tech org.
- Treat critical vulnerabilities as **incidents**: incident manager, status updates, action tracking.
- Account for **transitive dependencies** — explicit version pinning may be required.

**Don't:**
- Don't rely on automated scanners to fully identify scope in a zero-day window — they update too slowly.
- Don't forget third-party vendors with Java code and access to your data.
- Don't expect scanning alone to find the answer; you need a graph of your estate.

*Ref: Enabling Microservice Success.md — "Responding to the Log4Shell Vulnerability" (Ch. 9)*

---

### 63. Case Study: FT DNS Outage — Lose Your Tools, Lose Your Sight

**Principle:** Your observability and operations tooling must survive the same failures as your production services — or you lose the ability to debug.

**Do:**
- Host **observability tooling on a different domain** from your production services (FT moved theirs after an internal DNS outage took out both).
- Use **multiple DNS providers** for critical operations, or host critical runbook info in S3 + Google Drive (FT's belt-and-braces approach).
- Have a **fallback communication channel** (WhatsApp group, phone tree) when Slack is down.
- Treat operational tooling as **platinum-tier** — it needs to survive the same outages as your customers' experience.

**Don't:**
- Don't put monitoring and production on the same top-level DNS domain.
- Don't rely on a single SaaS tool without a fallback — even Slack outages happen.

*Ref: Enabling Microservice Success.md — "When a DDoS Hits a Vendor" (Ch. 9), "Internal Tooling" (Ch. 12)*

---

### 64. Case Study: FT Content Publishing at Scale — Idempotency + Self-Healing

**Principle:** When your business flow is idempotent (publish, republish, retry), build the system to take advantage of it — and add self-healing for free.

**Do:**
- Make critical business operations **idempotent** (the FT publishing flow was — republishing had no side effects).
- Build a **Publish Monitor** that registers for publish events and verifies they reached every data store in every region within 2 minutes — alert if not.
- Build **republish tooling** that anyone can use to manually retry a single article.
- Allow the website to **self-heal** by periodically re-requesting the latest version of content from the canonical store.
- Treat this as a **service** (with its own healthcheck) — its health means "publishes are landing everywhere."

**Don't:**
- Don't build a critical flow without idempotency — retries will be unsafe.
- Don't assume your distributed publish will always succeed without verification.
- Don't rely on humans to spot inconsistencies — automate the check.

*Ref: Enabling Microservice Success.md — "Idempotency" (Ch. 2), "Backup and Restore", "Disaster Recovery" (Ch. 12)*

---

### 65. Case Study: FT URL Manager 404 — A Haunted Forest in Action

**Principle:** Long-running, untouched services are a ticking time bomb when something finally breaks.

**Do:**
- Recognise the **haunted forest pattern**: code that no one on the team has touched for years, no one understands, and that has no useful runbook.
- Use the **haunted-forest scoring exercise** (engineers rate their familiarity 1–5 with each service) to find them.
- Prioritise fixing the worst-served services: low average knowledge, low number of experts.
- Rewrite or transfer when the cost of understanding exceeds the cost of replacement.
- Practice failovers regularly, even on services that "just work."

**Don't:**
- Don't ignore the haunted forests — they will fail at the worst time.
- Don't write a runbook for an unmaintained service and assume that's enough.
- Don't pretend every service needs to be kept — some need to be replaced.

*Ref: Enabling Microservice Success.md — "Identify the Haunted Forests" (Ch. 8)*

---

### 66. Communication Plans: Information Radiators vs Information Refrigerators

**Principle:** Some information sources radiate (you don't have to look); others refrigerate (you must fetch). Choose based on who needs the information and how often.

**Do:**
- Use **information radiators** for things people should know:
  - Dashboards on TVs.
  - Posters in common areas.
  - Slack channels with pinned messages.
  - Status pages.
  - Weekly digests.
- Use **information refrigerators** for things only relevant on demand:
  - Spreadsheets of OKRs.
  - Wiki pages on specific topics.
- Recognise that **Jason Yip's "air sandwich"** (high-level vision disconnected from day-to-day work) happens when information radiators don't reach the middle layer that translates goals to actions.

**Don't:**
- Don't rely on a single channel for critical information.
- Don't expect people to remember what was said in an all-hands three weeks ago.

*Ref: Enabling Microservice Success.md — "Aligning on Outcomes" (Ch. 6), Jason Yip's "Aligned Autonomy"*

---

### 67. Secondments and Knowledge Transfer as an Architecture Tool

**Principle:** Architecture is shaped by who talks to whom. Use secondments deliberately to break silos and seed capability.

**Do:**
- Use **secondments** (3-month rotations) to transfer specialist knowledge — FT's enabling teams got dedicated secondees from stream-aligned teams.
- Run **feature teams** for cross-team work but plan ownership transfer explicitly.
- Hold **monthly showcases** for cross-team learning.
- Use **internal tech conferences** (with multiple tracks) to spread knowledge across silos.
- Provide **10% time** for exploration with show-and-tell.

**Don't:**
- Don't assume knowledge transfers automatically when a new tool launches.
- Don't expect secondments to solve capability gaps in days — they're for the medium term.

*Ref: Enabling Microservice Success.md — "Collaboration" (Ch. 6), "Making Space for Learning"*

---

### 68. Engineering Enablement Group Composition

**Principle:** Engineering Enablement (EE) groups work best when they bring together all teams whose customers are engineers — reducing the coordination cost between platform, operations, and security.

**Do:**
- At the FT, the EE group merged:
  - Cloud enablement (AWS relationship, cost control, contracts).
  - Platform management (VMs, patching, instance-type optimisation).
  - Code management (vendors, APIs, best practice).
  - Edge delivery and observability (DNS, CDN, log aggregation, metrics).
  - API gateway (throttling, security, discovery).
  - Security engineering (vulnerability scanning, SAR responses).
  - Engineering insights (Biz Ops, scoring, ownership).
  - Operations (first-line support, incident management).
- Recognise the **benefits of consolidation**: shared mission, consistent approach, less duplication, clearer boundaries.
- Apply **5–10% of engineering** to EE for midsize companies; larger companies need more.

**Don't:**
- Don't split EE across too many organisations — coordination overhead defeats the purpose.
- Don't under-invest in EE — without it, every team reinvents the wheel.

*Ref: Enabling Microservice Success.md — "Case Study: Engineering Enablement at the Financial Times" (Ch. 7)*

---

### 69. Team APIs: How Other Teams Interact with You

**Principle:** Each team needs a "Team API" that tells others how to interact with them — like a software API for collaboration.

**Do:**
- Document for each team:
  - What the team owns (links to repos, systems).
  - How to use the team's services.
  - How best to communicate (Slack channel, email, on-call).
  - Principles and ways of working.
  - Current work and what's next.
  - Team membership.
- Host this in a single place — many service catalog tools (Backstage) support team pages.
- Use a **wiki page** if a tool isn't available — consistency matters more than tooling.

**Don't:**
- Don't force other teams to know which team owns what — make it discoverable.
- Don't have multiple documentation standards — pick one, apply broadly.

*Ref: Enabling Microservice Success.md — "Maintaining a Team Page" (Ch. 6)*

---

### 70. Blameless Postmortem Structure

**Principle:** Postmortems are learning artefacts, not blame artefacts. Use a consistent structure to capture the right information.

**Do:**
- Use a template with:
  - **Summary** — TL;DR.
  - **Timeline** — what happened, in order.
  - **Surprises** — where was our understanding wrong?
  - **Where we got lucky** — e.g., "Steve was the only one with access, and he happened to be online."
  - **Agreed actions** — 1–2 owned, dated.
- Capture pinned Slack messages automatically as part of the timeline.
- Limit to **1–2 actions** — longer lists don't all get done.
- Run them soon after the incident while memory is fresh, but allow time for emotions to settle.
- Tie incident learnings to **OKRs** so they get resourced.

**Don't:**
- Don't run postmortems as "who broke this" sessions.
- Don't accept 10-action lists.
- Don't skip them because calendars are full — book now.

*Ref: Enabling Microservice Success.md — "Learning from Incidents" (Ch. 8)*

---

### 71. Observability Vendors and Vendor Lock-in

**Principle:** Observability vendors will lock you in if you let them — adopt OpenTelemetry to keep your options open.

**Do:**
- Standardise on **OpenTelemetry** for instrumentation.
- Ensure your vendor supports the **OpenTelemetry API** before adopting.
- Make sure your observability data is **accessible via API** so you can change backends without rewriting.
- Be aware of vendor-specific features that lock you in (custom query languages, proprietary SDKs).
- Run a **Honeycomb-style** thought experiment: can I switch to a new provider in a week?

**Don't:**
- Don't adopt a vendor without OpenTelemetry support.
- Don't assume you'll never change providers — the observability market is evolving fast.

*Ref: Enabling Microservice Success.md — "OpenTelemetry" (Ch. 13)*

---

### 72. Operational Concerns for Resilience: Backup, Restore, Disaster Recovery

**Principle:** Resilience includes not just running systems but recovering them after disaster — including the disaster of losing your primary region.

**Do:**
- Test **backup and restore** regularly (FT discovered that backups were sometimes not actually being written).
- Track **last restore-tested** date for each critical data store.
- Use the **canonical source pattern**: identify which data store is the source of truth and back it up; dependent stores can be regenerated.
- Plan for **disaster recovery**: how long to bring up production in a new region? Can you do it from a new account?
- Use **off-account backups** to survive ransomware.
- For multiregion, ensure each region can serve all traffic alone.

**Don't:**
- Don't trust unverified backups.
- Don't assume the canonical source is obvious — make it explicit.

*Ref: Enabling Microservice Success.md — "Backup and Restore", "Disaster Recovery" (Ch. 12)*

---

### 73. Fallacies of Distributed Computing as a Diagnostic Tool

**Principle:** The eight fallacies (network is reliable, latency is zero, bandwidth is infinite, network is secure, topology doesn't change, one administrator, transport cost is zero, network is homogeneous) are a checklist for what can bite you.

**Do:**
- Use the fallacies as a **design review checklist** for new services and flows.
- Code defensively for each one:
  - **Reliability** → retries, circuit breakers.
  - **Latency** → timeouts, caching, async.
  - **Bandwidth** → batch, minimise data transferred.
  - **Security** → zero-trust, mTLS.
  - **Topology changes** → service discovery.
  - **Multiple administrators** → clear contracts, deprecation policies.
  - **Transport cost** → minimize cross-region hops.
  - **Homogeneity** → standard formats (JSON over HTTPS).

**Don't:**
- Don't assume the network "just works."
- Don't ignore the cost of network calls — both in latency and money.

*Ref: Enabling Microservice Success.md — "Resilience for Distributed Systems" (Ch. 12)*

---

### 74. Vendor Relationship Management

**Principle:** In a microservice world you depend on many vendors — manage the relationships proactively.

**Do:**
- Assign **vendor management** responsibility to a specific team or person.
- Subscribe to vendor **status pages** and **release notes**.
- For critical vendors, have a **shared Slack channel** and a known escalation path.
- Monitor your usage against **contract terms** (overages, license audits).
- Plan for the **vendor disappearing** — acquisition, sunset, bankruptcy.
- Use **vendor engineering** to maintain a consistent abstraction across vendors.

**Don't:**
- Don't sign up for SaaS without informing procurement.
- Don't use vendor tools without verifying they have status pages and out-of-hours support.

*Ref: Enabling Microservice Success.md — "Vendor Engineering", "Third-Party Software" (Ch. 9)*

---

### 75. Adoption of Cloud-Native Patterns: Pragmatism Over Purity

**Principle:** Cloud-native doesn't mean "Kubernetes on every workload" — match the deployment option to the workload.

**Do:**
- Choose deployment by workload profile:
  - **Containers** for consistent, always-on workloads.
  - **Serverless / FaaS** for event-driven, intermittent workloads.
  - **PaaS** for simple applications.
  - **Long-running services** for latency-critical paths.
- Use **Adrian Cockcroft's "serverless first"** advice: try serverless, fall back to containers only when necessary (cost, latency, control).
- Embrace **managed services** aggressively — let AWS/GCP/Azure handle undifferentiated heavy lifting.
- Use **Adrian's other advice**: commit to one provider and use its managed services deeply rather than chasing multi-cloud portability you won't actually use.

**Don't:**
- Don't adopt Kubernetes just because it's popular — it's complex.
- Don't pretend you need multicloud — the operational overhead is enormous.
- Don't build custom orchestration when a managed option exists.

*Ref: Enabling Microservice Success.md — "New Deployment Options", "Making your choice" (Ch. 1)*

---

### 76. The 5-Step Decision Framework for Tech Changes

**Principle:** Before adopting any new technology, walk through five decision steps to avoid sprawl and regret.

**Do:**
- Use this 5-step framework (per Enabling Microservice Success):
  1. **Understand the landscape** — what we have, what's changing, what constraints exist.
  2. **Define guiding policies** — what principles should guide the decision?
  3. **Make a decision** — who decides? How? (TGG, ADR, team lead).
  4. **Schedule the work** — when? In what order? With what dependencies?
  5. **Execute with discipline** — clarity, communication, empathy.
- For each step, ask: "What could change at this stage? What could invalidate the decision?"

**Don't:**
- Don't skip the landscape-understanding step.
- Don't make decisions in isolation — consult affected teams and experts.

*Ref: Enabling Microservice Success.md — "Responding to Change" (Ch. 14)*

---

### 77. Pragmatic Investment Thesis: When NOT to Adopt Microservices

**Principle:** Recognising when microservices are wrong is as important as recognising when they're right.

**Do:**
- Consider **staying with a monolith** when:
  - You don't yet understand the domain.
  - The team is small (under ~20 engineers).
  - The cost of microservices tax exceeds the benefit.
  - You don't have CI/CD, IaC, observability, and team autonomy.
- Recognise that **modular monoliths** solve many of the same problems with less operational overhead.
- Use **Gall's Law**: a complex system that works evolved from a simple one.
- Consider **Shopify's modular monolith** as the right intermediate step.

**Don't:**
- Don't adopt microservices because "everyone is doing it."
- Don't confuse architectural choice with progress.
- Don't underestimate the cost of supporting hundreds of services.

*Ref: Enabling Microservice Success.md — "Sticking with a Monolithic Architecture" (Ch. 3)*

---

### 78. Scaling Concerns: What Microservices Actually Solve

**Principle:** Microservices help with *organisational* scaling (many teams working in parallel), not just *technical* scaling.

**Do:**
- Recognise that **team scaling** is the primary problem microservices solve — *Accelerate* says "what is important is enabling teams to make changes to their products or services without depending on other teams or systems."
- Recognise that microservices also help with:
  - **Compliance segregation** (PCI, PII).
  - **Load scaling** (only scale the hot part).
  - **Robustness** (small blast radius).
  - **Flexibility** (different tech per domain).
- Match the solution to the **primary pain point**.

**Don't:**
- Don't adopt microservices primarily for technical reasons (you can usually solve those within a monolith).
- Don't assume microservices will magically fix organisational dysfunction — they expose it.

*Ref: Enabling Microservice Success.md — "Scaling the Organization" (Ch. 3)*

---

### 79. Recap: The Book's Structure as a Maturity Roadmap

**Principle:** Wells' three-part structure maps to a maturity progression: Context (why) → Organisation (how) → Operations (what).

**Do:**
- Use the book's structure as a self-assessment:
  - **Part I: Context** — Do we understand what microservices are? Do we know if they're right for us?
  - **Part II: Organisational Structure & Culture** — Do we have the teams, autonomy, and culture to support them?
  - **Part III: Building & Operating** — Do we have the technical practices (testing, governance, resilience, observability) to run them?
- Don't skip a part — the prerequisites are real.
- Re-read parts as you mature — the same content reads differently at different stages.

**Don't:**
- Don't start with Part III and hope the culture catches up.
- Don't assume you can adopt microservices without the organisational foundation.

*Ref: Enabling Microservice Success.md — "Foreword", "Part I", "Part II", "Part III" structure*

---

### 80. The Ship of Theseus Mental Model

**Principle:** Microservices should let you replace any part of the system without rewriting everything — the system evolves continuously rather than catastrophically.

**Do:**
- Frame the goal as **continuous evolution**, not "build it once, run it forever."
- Recognise that the **Ship of Theseus** metaphor applies: at some point nothing of the original system remains except the purpose.
- Make individual services **replaceable**: small enough to rewrite, well-defined interfaces.
- Use the **habitability** concept (Richard Gabriel / Christopher Alexander): systems must be liveable, easy to understand and change.
- Avoid features that depend on internal implementation across services — those prevent independent replacement.

**Don't:**
- Don't design services that can't be replaced without coordinating with many other teams.
- Don't optimise for short-term performance at the cost of replaceability.

*Ref: Enabling Microservice Success.md — "Not Having to Start Again" (Ch. 2), "Wrapping Up" (Afterword)*

---

*Ref: Throughout Enabling Microservice Success — distributed across chapters.*

---

## Decision Heuristics / Checklists

### Should we adopt microservices?
- Do we have multiple teams needing to work in parallel on the same product? → Yes favours microservices.
- Do we have a clear business reason (flow, scale, flexibility, compliance)? → Yes required.
- Do we have CI/CD, IaC, observability, team autonomy as prerequisites? → No means fix first.
- Is the domain well-understood? → If not, start with a modular monolith.
- Can we articulate at least one bounded context with the ISH heuristics? → Yes favours extraction.
- Have we assessed the migration cost (years, not months)? → If not, reset expectations.

### Should we extract this service from the monolith?
- Is this domain under active development by multiple teams? → Yes favours extraction.
- Does it have different scaling needs? → Yes favours extraction.
- Does it have different compliance/security needs? → Yes favours extraction.
- Are there well-defined data ownership boundaries? → If not, defer.
- Do we have the team to actively own it? → If not, defer.

### Should we make this tech choice?
- Is it the default on the paved road? → Use it.
- Is there a clear business differentiator (vs. an existing option)? → Maybe justify an exception.
- Have we counted our innovation tokens? → If exhausted, defer.
- Is it boring? → Strong preference (failure modes are understood).
- Will it still be supported in 3 years? → If unsure, defer.

### Should we go off the paved road?
- Will we have the team to support the alternative long-term? → If not, stay on road.
- Have we considered the security/ops cost of going off road? → If higher than the win, stay on road.
- Is the paved road about to deliver what we need soon? → If yes, wait.
- Is the platform team blocking without an imminent plan? → Don't accept vague promises.

### Is this incident serious enough to escalate?
- Significant impact (business, customer-facing)? → Yes.
- Need help from another team? → Yes.
- I have been looking at this for a while and don't know the cause? → Yes.
- If in doubt: raise it, even if it's a false alarm.

### Is this alert worth keeping?
- Does it require action? → If not, delete it.
- Does it point to the root cause, not a symptom? → If not, replace.
- Does it correlate to an SLO breach? → If not, reconsider.

### Is this service ready to decommission?
- Is it still serving traffic? → If yes, defer.
- Have we migrated all callers? → If not, defer.
- Is the data still referenced anywhere? → If yes, archive first.
- Have we removed all DNS entries, monitoring, alerts? → Required.

---

## Key Takeaways

1. **Microservices are an organisational pattern as much as a technical one.** Conway's Law means the architecture of your system will mirror the architecture of your organisation. Start there.
2. **Lay the groundwork before adopting microservices.** CI/CD, automated testing, infrastructure as code, observability, and team autonomy are prerequisites, not afterthoughts.
3. **Decompose around business capabilities** using Domain-Driven Design. Use the ISH checklist (Independent, Stateless, Helpful) to validate service boundaries.
4. **Teams should be cross-functional, long-lived, and autonomous** — but autonomy comes with responsibilities (active ownership, runbooks, on-call).
5. **Build a paved road** that makes best practices the easy path. It should be optional but so compelling that most teams choose it.
6. **"You build it, you run it" is a fundamental principle.** Teams that operate their own services build more operable systems. Share on-call across groups to make this sustainable.
7. **Track your software estate** with a service catalog (Biz Ops or Backstage). Know what services exist, who owns them, and how they relate.
8. **Invest heavily in observability.** Structured logging, correlation IDs, distributed tracing, and business-level monitoring are essential. Use OpenTelemetry to avoid vendor lock-in.
9. **Minimise end-to-end tests** in favour of contract tests and testing in production. Feature flags, canary deployments, and synthetic monitoring are more effective.
10. **Design for resilience** with circuit breakers, timeouts, bulkheads, fallbacks, idempotency, and redundancy. Use chaos engineering to verify.
11. **Lead through influence, not authority.** Use data, social proof, narratives, and nudges (EAST framework) to drive change.
12. **Incident management requires clear roles, good tools, and blameless postmortems.** Invest in runbooks, healthchecks, and custom diagnostic tools.
13. **Guardrails should be automated, not just documented.** Embed them in templates, pipelines, and tools. The TGG (Tech Governance Group) handles cross-cutting decisions lightly.
14. **Communication is a first-class concern.** Multiple channels, repeated messages, public commitments, nudge theory.
15. **Migration should be incremental** (Strangler Fig). Avoid big-bang rewrites. Set explicit decommission dates.

---

## Cross-References

- Related: **Team Topologies** by Skelton & Pais (the four team types and three interaction modes are cited extensively).
- Related: **Accelerate** by Forsgren, Humble & Kim (the four DORA metrics and Westrum culture research).
- Related: **Building Microservices** by Sam Newman (the technical depth on service design, distributed data, and contract testing).
- Related: **Monolith to Microservices** by Sam Newman (the Strangler Fig pattern and migration strategies).
- Related: **Observability Engineering** by Majors, Miranda, Miranada (high-cardinality observability, OpenTelemetry).
- Related: **Site Reliability Engineering** by Beyer et al. (SLOs, error budgets, incident management, resilience).
- Related: **Drive** by Daniel Pink (autonomy, mastery, purpose — the motivation model).
- Related: **Team Topologies** interaction modes (collaboration, X-as-a-service, facilitating).
- Related: **Dynamic Reteaming** by Heidi Helfand (the realities of changing team composition).
- Related: **Nudge** by Thaler & Sunstein; **Inside the Nudge Unit** by David Halpern (the EAST framework).
- Related: **Inspired** by Marty Cagan (engineering capacity allocation for non-feature work).
- Related: **Choose Boring Technology** by Dan McKinley (innovation tokens).
- Topic index: `[[../INDEX.md]]`

---

*Final line count check on the file you just wrote.*