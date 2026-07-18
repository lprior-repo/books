# Team Topologies (Second Edition, 2025)

**Authors:** Matthew Skelton and Manuel Pais
**Topic tags:** `#organization` `#general` `#leadership` `#strategy` `#architecture` `#teams` `#sociotechnical` `#conways-law` `#cognitive-load`
**Language focus:** language-agnostic (organizational / sociotechnical)
**Sources:** `markdown_output/Team_Topologies_2nd_Edition/Team_Topologies_2nd_Edition.md` · `summaries/Team_Topologies_2nd_Edition.md`

## TL;DR
A practical, adaptive model for organizational design based on four fundamental team types (stream-aligned, enabling, complicated-subsystem, platform grouping) and three interaction modes (collaboration, X-as-a-Service, facilitating). The core thesis: organizations must deliberately design their team structures to achieve a fast flow of value to customers, leveraging Conway's law rather than being victimized by it. The second edition (2025) consolidates the platform concept into a "platform grouping" (fractal — the same patterns repeat at every zoom level), adds nine detailed case studies (EBSCO, GovTech Singapore, ING, KFC, Creditas, Yassir, Telenet, Trade Me, Adidas), and replaces the bucket analogy of cognitive load with a river analogy. Apply whenever you're designing team boundaries, diagnosing flow bottlenecks, or planning organizational change.

---

## Best Practices by Topic

### Conway's Law Is Real and Powerful — Design Team Structures to Shape Architecture

**Principle:** "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." Conway's "homomorphic force" pulls software architecture toward team communication structures — for better or worse.

**Verbatim — Mel Conway, "How Do Committees Invent?" (1968):** "Any organization that designs a system…is constrained to produce designs which are copies of the communication structures of these organization[s]."

**Verbatim — Eric Raymond:** "If you have four groups working on a compiler, you'll get a 4-pass compiler."

**Verbatim — Ruth Malan (modern interpretation):** "If the architecture of the system and the architecture of the organization are at odds, the architecture of the organization wins."

**Verbatim — Conway's imperative:** "Is there a better design that is not available to us because of our organization?"

**Do:**
- Treat org design as architecture work; involve technical leaders in boundary decisions.
- Apply the **reverse Conway maneuver**: design the team structure you want and let the software architecture follow.
- Aim for **team-scoped flow**: a single team owns the full lifecycle (build, test, deploy, operate) of a service; the architecture tends toward modularity and loose coupling.
- Use **focused communication**: not everyone needs to talk to everyone; team assignments should restrict the solution search space productively.

**Don't:**
- Don't treat Conway's law as a simple one-to-one mapping between teams and microservices — that's a naive use that misses the deeper point.
- Don't reorganize teams without understanding the underlying communication patterns; reorganization without a clear shape produces no architecture improvement.
- Don't use log-aggregation tools or org-chart posting to force cross-team communication; structural change must come first.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 2. Conway's Law and Why It Matters"*

---

### The Reverse Conway Maneuver — Design Teams to Match Desired Architecture

**Principle:** Don't try to mandate an architecture and hope teams follow it. Reorganize teams first; the architecture follows from Conway's law.

**Verbatim — Accelerate (Forsgren, Humble, Kim):** "Our research lends support to what is sometimes called the 'inverse Conway maneuver,' which states that organizations should evolve their team and organizational structure to achieve the desired architecture. The goal is for your architecture to support the ability of teams to get their work done—from design through to deployment—without requiring high-bandwidth communication between teams."

**Distinction:** "Reverse Conway maneuver" (proactive, strategic) vs. "inverse Conway maneuver" (reactive).

**Do:**
- Sketch the desired architecture (services, APIs, data flows).
- Derive the team boundaries required to support that architecture.
- Use collaboration and facilitating modes to test the new boundaries.
- Pair the maneuver with sufficient leadership sponsorship.

**Don't:**
- Don't insist on the new architecture before the team boundaries exist; both evolve together.

*Ref: Team_Topologies_2nd_Edition.md — "The Reverse Conway Maneuver"*

---

### Four Fundamental Team Types — The "Magnets" for All Teams

**Principle:** Restrict teams to four fundamental types — **stream-aligned, enabling, complicated-subsystem, platform grouping.** They should act as "magnets" pulling every team in the organization toward one of the four poles.

**Verbatim Figure 5.1 description:**
> "The four fundamental team topologies — stream aligned, enabling, complicated subsystem, and platform — should act as 'magnets' for all team types. All teams should move toward one of these four magnetic poles."

**Tip (verbatim):** "For organizations that are successful at delivering software rapidly and safely, most teams are stream aligned, with only around one in seven to one in ten teams not stream aligned. That is, based on what successful organizations report, the ratio of stream-aligned teams to other kinds of teams should be between about 6:1 and 9:1."

**Do:**
- Map every existing team to one of the four fundamental types; rename and reshape the ones that don't fit.
- Adopt purpose, role, responsibility, and interaction behavior of the chosen type.
- Use the four types as a clarity device; reducing ambiguity around organizational roles is a key to design success (Luo et al., 2018).

**Don't:**
- Don't keep "ops team" or "support team" as standalone topologies — operations and support live inside stream-aligned teams (with swarming rather than tiered support).
- Don't create a fifth or sixth "hybrid" type without first trying hard to fit within the four.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 5. The Four Fundamental Team Topologies"*

---

### Stream-Aligned Teams — The Primary Team Type

**Principle:** A stream-aligned team is aligned to a single, valuable stream of work — a product, service, set of features, user journey, or user persona. Empowered to build and deliver customer value as quickly, safely, and independently as possible, without requiring hand-offs to other teams.

**Do:**
- End-to-end ownership: requirements → production operation. "You build it, you run it." (Werner Vogels)
- Provide cross-functional capabilities (security, design, dev, infrastructure, metrics, PM, testing, UX) — not necessarily as individual roles.
- Keep teams close to customers; deliver a stable cadence; produce telemetry.
- Choose the stream carefully (customer, business-area, geography, product, user-persona, compliance).

**Capabilities a stream-aligned team needs (verbatim list):**
- Application security
- Commercial and operational viability analysis
- Design and architecture
- Development and coding
- Infrastructure and operability
- Metrics and monitoring
- Product management and ownership
- Testing and quality assurance
- User experience (UX)

**Expected behaviors (verbatim):**
- Steady flow of feature delivery
- Quick course correction based on feedback
- Experimental approach — expect to constantly learn and adapt
- Minimal (ideally zero) hand-offs to other teams
- Evaluated on sustainable flow of change
- Time and space to address code quality / tech debt
- Proactively engage enabling and platform teams
- "Autonomy, mastery, and purpose" (Daniel Pink)

**Use "stream-aligned," not "product" or "feature":**
A "stream" better captures continuous flow and the multi-channel, multi-device reality of modern UX. "All software situations benefit from alignment to flow."

**Don't:**
- Don't form stream-aligned teams around projects that will dissolve at the end — they must be long-lived and funded sustainably.
- Don't assume each capability must be a dedicated role; that's how teams balloon to 12+ people.

**Verbatim Bezos 2002 mandate at Amazon:**
> "Each team is fully responsible for developing and operating its own service...
> Each service is provided through an API, either for internal or external consumption; teams do not interfere or make any assumptions on other teams' services architecture or technology."

*Ref: Team_Topologies_2nd_Edition.md — "Stream-Aligned Teams"; "Why Stream-Aligned Team, Not 'Product' or 'Feature' Team?"*

---

### Enabling Teams — Capability Multipliers

**Principle:** An enabling team is composed of specialists in a given technical or product domain; they help stream-aligned teams bridge capability gaps. They multiply, not replace, capability. They should make themselves unnecessary.

**Do:**
- Detect capability gaps by actively scanning stream-aligned team needs (regular checkpoints).
- Stay ahead of industry developments, well before an actual need arises.
- Act as messenger of good news ("new UI framework reduces custom test code 50%") and bad news ("Framework X is no longer maintained").
- Plan for self-extinction from day one — quarter of time on actual implementation, rest on knowledge sharing.
- Use Robert Greenleaf's heuristic: "Do those served grow as persons? Do they, while being served, become healthier, wiser, freer, more autonomous?"

**Don't:**
- Don't become an "ivory tower" of knowledge dictating technology choices; that's the opposite of enablement.
- Don't stay indefinitely attached to a single stream-aligned team; rotating helps spread capability.

**Verbatim BCG Digital Ventures case study (BCG, 2017):**
> Goal: "enable teams to deliver features faster and with higher quality." Initial eight-week targets:
> - Time taken per successful deployment
> - Absolute number of successful deployments per day
> - Time taken to fix a failing deployment
> - Time from code commit to deployment (cycle time)
>
> After 8 weeks: 72% decrease in deployment lead time; 700% increase in deployment pipeline runs per day; deployment pipeline run duration decreased 98% (from 10 hours → 15 minutes); failing build fixed within 23 hours on average.

**Enabling Team vs. Community of Practice (CoP):**
- Enabling team: small, long-lived, full-time specialists, single team focus.
- CoP: diffuse grouping, voluntary, weekly/monthly meetings, broader reach.
- They can co-exist; several enabling teams can have their own "enabling-teams community of practice."

*Ref: Team_Topologies_2nd_Edition.md — "Enabling Teams"; "Enabling Team versus Communities of Practice (CoP)"*

---

### Complicated-Subsystem Teams — Specialist Deep Knowledge, Narrow Scope

**Principle:** A complicated-subsystem team handles a part of the system requiring deep specialist knowledge — most team members must be specialists in that area to understand and make changes. Goal: reduce cognitive load on stream-aligned teams working on systems that include or use the complicated subsystem.

**Examples (verbatim):**
- A video processing codec
- A mathematical model
- A real-time trade reconciliation algorithm
- A transaction reporting system for financial services
- A face-recognition engine

**Do:**
- Create one only when the subsystem genuinely needs specialist knowledge — driven by cognitive load, not by reuse.
- Prioritize the needs of consuming stream-aligned teams.
- Provide the subsystem with a clear API, documentation, and DevEx; reduce consumer cognitive load.
- Use collaboration during early development; transition to X-as-a-Service once the subsystem has stabilized.

**Don't:**
- Don't create a "component team" and call it a complicated-subsystem team. The latter exists only when specialist knowledge is genuinely required.
- Don't expect to have many complicated-subsystem teams — expect a few, only when strictly necessary.

*Ref: Team_Topologies_2nd_Edition.md — "Complicated-Subsystem Teams"*

---

### Platform Teams and the "Platform Grouping" — Fractal

**Principle:** In the second edition, what was a single platform team is now better understood as a **platform grouping** — a container for one or more teams providing a coherent capability. The four fundamental types appear inside a platform grouping (fractal): stream-aligned teams aligned to internal platform services, enabling teams for onboarding, complicated-subsystem teams for specialized platform components, and inner platform teams.

**Verbatim — Note on the Second Edition:**
> "In an organization larger than about forty to fifty people, an internal platform will typically need more than one eight-person team to provide the necessary services—a grouping of teams is needed. In the case of an internal platform, we're now calling this a platform grouping."

**Verbatim Figure 5.2 description:**
> "In a large organization, the platform is composed of several other fundamental team topologies: stream-aligned Dev teams, complicated-subsystem teams, and a lower-level platform."

**Verbatim — Evan Bottcher definition:**
> "A digital platform is a foundation of self-service APIs, tools, services, knowledge and support which are arranged as a compelling internal product. Autonomous delivery teams can make use of the platform to deliver product features at a higher pace, with reduced coordination."

**Verbatim — Peter Neumark (Prezi):**
> "A platform team's value can be measured by the value of the services they provide to product teams."

**Verbatim — Kenichi Shibata (Condé Nast International):**
> "The most important part of the platform is that it is built for developers."
> "Developers will sometimes have frustrations....There should be a way to give feedback to platform developers and how the platform is doing in general. Without this, the platform lives in isolation with the rest of the company."

**Do:**
- Treat the platform as a live product with internal customers — versioning, roadmaps, user feedback, on-call rota, status pages.
- Use **internal pricing** (Don Reinertsen's tip) to regulate demand — track infrastructure costs by team or service.
- Aim for the **thinnest viable platform (TVP)**: the minimum platform services that actually help stream-aligned teams.
- Use compelling, consistent, well-chosen constraints — UX/DevEx discipline.
- **Draw the platform layers** on a large diagram to explain what the platform provides and what it depends on ("turtles all the way down").

**Don't:**
- Don't leave a platform to former sysadmins without strong product management and engineering.
- Don't build a comprehensive platform before anyone needs it (Allan Kelly: "software developers love building platforms and, without strong product management input, will create a bigger platform than needed").
- Don't ship platforms to multiple internal personas with the same primitives — that's why Adidas uses **multiple platforms** (digital, enterprise, data) rather than one.

**Verbatim — Mike Cohn:** "Does the structure minimize the number of communication paths between teams?...Does the structure encourage teams to communicate who wouldn't otherwise do so?"

*Ref: Team_Topologies_2nd_Edition.md — "Platform Teams"; "Compose the Platform from Groups of Other Fundamental Teams"; "Manage as a Live Product or Service"; "A Good Platform Is 'Just Big Enough'"*

---

### Thinnest Viable Platform (TVP) — Start Small, Grow on Demand

**Principle:** A thinnest viable platform is the smallest set of platform services that actually help stream-aligned teams deliver. Grow it as actual needs emerge, not as anticipated ones.

**Do:**
- Start with the simplest possible platform: a wiki page listing underlying components/services used by consuming software.
- Add a platform team only when the underlying substrate grows complicated — even if all components are still outsourced.
- Add product management discipline and DevEx to platform teams as they grow.
- Ask stream-aligned teams "what slows you down the most?" and build only that.

**Don't:**
- Don't preemptively build a comprehensive platform — Trade Me's case study shows a TVP that started with deployment pipelines, shared logging, and a few self-service infra components.
- Don't measure platform productivity by what the team built; measure by what stream-aligned teams deliver.

**Heuristic (verbatim):**
> "Are our product teams spending enough time focused on our end customers' needs?"

**Verbatim — NAV (Norwegian Labour and Welfare Administration):** "We have a small number of coherent internal platforms [an application platform, a data platform, and a design system/platform], not a cumbersome single platform."

*Ref: Team_Topologies_2nd_Edition.md — "The Thinnest Viable Platform"; Trade Me case study (appendix)*

---

### Cognitive Load — Match Software Subsystems to Team Capacity

**Principle:** Cognitive Load Theory (John Sweller, 1988) distinguishes three types:
- **Intrinsic load:** inherent to the problem domain.
- **Extraneous load:** from the environment, tooling, processes — to be minimized.
- **Germane load:** the learning effort — to be supported.

A team should own no more than one complicated or complex domain; software boundary size must be limited to fit cognitive capacity.

**Diagnostic question (verbatim):** "Do you feel like you're effective and able to respond in a timely fashion to the work you are asked to do?"

**Do:**
- Apply the goal: minimize intrinsic (training, tools, hiring); eliminate extraneous (automation, simpler interfaces); preserve capacity for germane (value-add thinking).
- Restrict team responsibilities to match the maximum team cognitive load.
- Don't let a single team own two complicated domains — they'll behave as two subteams and degrade in coordination.
- Make software boundaries team-sized.

**Don't:**
- Don't measure cognitive load by lines of code or number of modules — the unit that matters is domain complexity.
- Don't apply the "bucket" analogy of cognitive load. The second edition uses a **river analogy**: the level fluctuates; a temporary increase is fine when the objective is clear; what must be avoided is continuously increasing load without adequate support.
- Don't blame individual team members when a team's cognitive load is overflowing; the issue is usually structural.

**The Teamperature model (with Dr. Laura Weis):**
> More than **20 drivers of cognitive load** arranged into **4 clusters**:
> 1. Team characteristics
> 2. Work practices and processes
> 3. Task characteristics
> 4. Work environments and tools

**Heuristics (verbatim):**
- Assign each domain to a single team.
- A team (5-9 people) can accommodate 2-3 "simple" domains.
- A team responsible for a complex domain should have no other domains.
- Avoid a single team responsible for two complicated domains; split into two teams of 5.

**Verbatim — Toyota, via Mike Rother:** "The roots of Toyota's success lie not in its organizational structures but in developing capability and habits in its people."

**Tip (verbatim):** "Minimize cognitive load for others" is one of the most useful heuristics for good software development.

*Ref: Team_Topologies_2nd_Edition.md — "Cognitive Load" (Chapter 3, expanded in foreword)*

---

### Team APIs — Define the Interface Between Teams

**Principle:** A **team API** is an explicit, stable interface that a team presents to other teams — the analog of a software API applied to the team level. Includes code repos, documentation, versioning, communication channels, working hours.

**The team API includes (verbatim):**
- Code: runtime endpoints, libraries, clients, UI, etc. produced by the team
- Versioning: how the team communicates changes to its code and services (e.g., using SemVer as a "team promise" not to break things)
- Wiki and documentation: how-to guides for the software owned by the team
- Practices and principles: the team's preferred ways of working
- Communication: chat tools, video conferencing
- Work information: what the team is working on now, what's coming next, and overall priorities
- Other: anything else other teams need to interact with the team

**Do:**
- Define what your team owns, how to request work, and how you communicate (CDL / Auto Trader case studies).
- Version your team API; use semantic versioning for promises of compatibility.
- Test the API by trying to onboard a new team to your code and practices.
- Apply the "promise theory" lens (Mark Burgess): teams make explicit promises rather than rely on enforced contracts.
- Adopt a developer-experience (DevEx) mindset for the consuming teams.

**Don't:**
- Don't treat the team API as a one-time definition; it's a continuously evolving interface that needs to be tested by consumers.

**Verbatim — Pivotal Cloud Foundry (Evan Wiley):**
> "We really try to maintain as much contract based, API-based separation of concerns between teams as we can. We try not to share code bases between teams. All the git repos for a particular team's feature are wholly owned by that team and if another team is going to make an addition or change to that code base, they'll either do it with a pull request or through cross-team pairing..."

**Verbatim — AWS ethos (Jeff Bezos):**
> "Every [other team] becomes a potential DOS [denial of service] attacker requiring service levels, quotas, and throttling."

*Ref: Team_Topologies_2nd_Edition.md — "Team APIs" (Chapter 3)*

---

### Three Team Interaction Modes

**Principle:** Three modes govern how teams interact:
- **Collaboration** — high-bandwidth, temporary, divergent; for discovery.
- **X-as-a-Service** — low-bandwidth, stable, convergent; for execution.
- **Facilitating** — coaching, capability growth; for learning.

**Primary interaction modes by team type (verbatim Table 7.4):**

| Team Type          | Collaboration | X-as-a-Service | Facilitating |
|--------------------|---------------|----------------|--------------|
| Stream-aligned     | Typical       | Typical        | Occasional   |
| Enabling           | Occasional    | Typical        | Typical      |
| Complicated-subsystem | Occasional| Typical        |              |
| Platform           | Occasional    | Typical        |              |

**Do:**
- Treat interaction modes as **team habits**, not ad-hoc decisions.
- Pair modes with team topology: stream-aligned × platform → X-as-a-Service; stream-aligned × enabling → facilitating; stream-aligned × complicated-subsystem → X-as-a-Service (or collaboration in early discovery).
- Use the **intermittent collaboration** finding (Bernstein, Shore & Lazer): groups whose members interacted only intermittently had nearly the same quality of solution as constantly-interacting groups, while preserving diversity for finding the best solutions.
- Apply the **principle of overlapping measurement** (Don Reinertsen) — reward both teams for collaborative outcomes.

**Don't:**
- Don't let collaboration drift into permanent inter-team meetings.
- Don't treat X-as-a-Service as "throw it over the wall"; the provider team must own service-management principles (versioning, roadmaps, DevEx).

**Verbatim:**
> "Interaction modes should become team habits. By expecting and helping to achieve these kinds of team interactions, teams experience increased clarity of purpose, improved team engagement, and reduced frustration with other teams."

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 7. Team Interaction Modes"*

---

### Collaboration Mode — Use It When Discovery Outweighs the Cost

**Principle:** Collaboration is high-bandwidth, joint work to discover new things. Suitable for rapid innovation, early phases of new systems, and problems spanning two teams' expertise. Should be intermittent, not permanent.

**Do:**
- Apply when the problem space is not well understood and discovery is valuable (cloud + sensor, networking + wearables).
- Limit collaboration to one other team at a time (constraint).
- Train for collaboration: pair programming, mob programming, boundary-spanning collaboration.
- Combine with **rewarding one team for the work of the other team** (Principle of Overlapping Measurement).

**Don't:**
- Don't use collaboration when you really want X-as-a-Service — Conway's law will tend toward tighter coupling where you don't want it.
- Don't let collaboration create ambiguity about ownership; create **joint responsibility** for the outcome.

**Constraint (verbatim):** "A team should collaborate with at most one other team at a time."

**Verbatim — Bernstein et al.:** "Groups whose members interacted only intermittently...had an average quality of solution that was nearly identical to those groups that interacted constantly, yet they preserved enough variation to find some of the best solutions too."

*Ref: Team_Topologies_2nd_Edition.md — "Collaboration: Driver of Innovation and Rapid Discovery but Boundary Blurring"*

---

### X-as-a-Service Mode — Require Real Boundaries and Real Product Management

**Principle:** One team provides something to another team with minimal day-to-day interaction. Compelling DevEx is the explicit benefit. Suited to late phases where predictable delivery matters more than discovery.

**Do:**
- Make the boundary well-chosen and well-implemented — this is the mode's biggest precondition.
- Demand excellent service-management from the providing team — versioning, semantic-versioning promises, roadmaps.
- Emphasize user experience and developer experience.
- Train teams in UX and DevEx practices for this mode.

**Don't:**
- Don't treat X-as-a-Service as "out of sight, out of mind" for the providing team — they'll be the bottleneck when the API doesn't fit consumer needs.
- Don't innovate too aggressively across the boundary; that's collaboration's job.

*Ref: Team_Topologies_2nd_Edition.md — "X-as-a-Service: Clear Responsibilities with Predictable Delivery but Needs Good Product Management"*

---

### Facilitating Mode — Sense and Reduce Gaps

**Principle:** One team helps another team remove impediments and fill capability gaps. The facilitating team's job is to grow capability, not take on the work. Closely linked to enabling teams.

**Do:**
- Use facilitating to discover gaps in existing components and platforms used across many teams.
- Pair facilitating with the **Principle of Overlapping Measurement** so the facilitator doesn't lose touch with the work.
- Use temporary facilitation to support a reverse Conway maneuver — boundaries will be tested, then refined.
- Bound by a small number of simultaneous facilitating relationships per team.

**Don't:**
- Don't use facilitating as a permanent dependency — the stream-aligned team should grow out of needing it.
- Don't have facilitating teams take on the building of the main systems; they only support other teams.

*Ref: Team_Topologies_2nd_Edition.md — "Facilitating: Sense and Reduce Gaps in Capabilities"*

---

### Fracture Planes — Where to Split Software Systems

**Principle:** Fracture planes are natural seams along which a software system can be split. The primary plane is the business domain bounded context (Domain-Driven Design); secondary planes expand the options.

**The 9 fracture planes (verbatim):**
1. **Business domain bounded context (primary)** — DDD bounded contexts.
2. **Regulatory compliance** — e.g., PCI DSS in a card-data subsystem.
3. **Change cadence** — separate parts that change at different speeds.
4. **Team location** — geographic or time-zone separations.
5. **Risk** — different test/deploy/security practices for high-risk vs. low-risk.
6. **Performance isolation** — isolate heavy I/O from real-time user-facing services.
7. **Technology** — different stacks are natural boundaries.
8. **User personas** — internal vs. external, admin vs. end user.
9. **Natural fracture planes** — domain-specific (e.g., physical factory topology in IoT).

**Do:**
- Default to the business-domain plane; use others to resolve remaining coupling.
- Make all segments **team-sized**: a single team can own and evolve them.
- Watch out for the "joined-at-the-database monolith" and other subtle monoliths.

**Don't:**
- Don't treat monoliths as only an application architecture concern. There are also:
  - **Joined-at-the-database monolith** (services share a database)
  - **Hidden monolith** (looks modular but deeply coupled)
  - **Monolithic thinking** (one-size-fits-all standardization)
  - **Monolithic workplace** (open-plan office that couples everyone's patterns)
  - **Monolithic rebuilds** (rewriting everything at once)
  - **Coupled releases** (different parts must release together)
  - **Single view of the world** (one shared data model)

**Verbatim — Amy Phillips:** "If you have microservices but you wait and do end-to-end testing of a combination of them before a release, what you have is a distributed monolith."

**Verbatim — Michael Nygard:** "A concept may appear to be atomic just because we have a single word to cover it. Look hard enough and you will find seams where you can fracture that concept."

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 6. Software Boundaries and Fracture Planes"*

---

### Team-Sized Software Architecture — Fit Architecture to Team Capacity

**Principle:** Design the system to fit the available cognitive load within delivery teams. This team-first approach leads naturally to small, decoupled services — without mandating microservices.

**Do:**
- Choose between monolith and microservices by **team cognitive load**, not by fashion.
- Aim for high cohesion and loose coupling at the team level.
- Decouple parts of the system that have different change cadences — they slow each other down.
- Apply Cohesion/Coupling rules to team-scope: a team's code bases should share internal cohesion; cross-team coupling should be explicit (APIs).

**Don't:**
- Don't "microservicify" until team-sized boundaries emerge naturally.
- Don't couple releases across bounded contexts.

**Verbatim — Don Reinertsen:** "We can also exploit architecture as an enabler of rapid changes. We do this by partitioning our architecture to gracefully absorb change."

*Ref: Team_Topologies_2nd_Edition.md — "Software Boundaries and Fracture Planes"; "Team-First Architecture"*

---

### Team Size and Trust — Dunbar, Tuckman, McChrystal

**Principle:** Effective software teams are small (5-9 members) to maintain high trust and fast communication. Longer-lived teams build trust; dissolving teams wastes the Tuckman investment (forming, storming, norming, performing).

**Verbatim — Amazon:** Team size limited to those that can be fed by two pizzas ("two-pizza team").

**Dunbar layers (verbatim):**
- Around 5 — limit of close personal relationships / working memory
- Around 15 — limit of deep trust
- Around 50 — limit of mutual trust
- Around 150 — limit of remembering capabilities
- 500, 1,500 — extended layers

**Verbatim — General Stanley McChrystal (Team of Teams):** The goal is "to create organizations with the adaptability and agility of small teams, at enterprise scale."

**Do:**
- Keep teams at 5-9 members (Dunbar's trust boundary; Onion concept of decreasing trust with distance).
- Treat the team as the **smallest unit of delivery**, not individuals.
- Give teams long lifespans; the default is stability.
- Apply Heidi Helfand's Dynamic Reteaming only when reteaming is truly needed; don't churn teams for convenience.

**Don't:**
- Don't form teams around projects that will dissolve.
- Don't grow teams past 9 expecting better results — Brooks's Law applies: adding people makes late projects later.

**Verbatim — Allan Kelly:** "Disbanding high-performing teams is worse than vandalism: it is corporate psychopathy."

*Ref: Team_Topologies_2nd_Edition.md — "Team-First Thinking"*

---

### Software Ownership — End-to-End ("You Build It, You Run It")

**Principle:** Teams should own their software systems end-to-end, including production operation. The DORA research confirms that end-to-end-owned teams deliver faster, more reliably, and with higher quality.

**Do:**
- Adopt the "you build it, you run it" principle (Werner Vogels).
- Engineer teams for operability (observability, deployment, security, compliance).
- Keep the feedback loop short: ship, observe, course correct.
- Allow teams to fail forward; restrict scope, not autonomy.

**Don't:**
- Don't have separate "ops" or "support" teams for production handoff; that's a flow-killer.
- Don't separate "new development" from "maintenance" (BAU vs. feature teams) — it creates artificial handoffs.

**Verbatim — Accelerate:** "Architectural approaches that enable this strategy [of supporting teams' full ownership from design through to deployment] include the use of bounded contexts and APIs as a way to decouple large domains into smaller, more loosely coupled units."

*Ref: Team_Topologies_2nd_Edition.md — "Stream-Aligned Teams"; "BAU teams as anti-pattern"*

---

### Avoiding Team Silos in the Flow of Change

**Principle:** Cross-functional teams aligned to the flow of change (stream-aligned) avoid silos. Teams of single-functional expertise become bottlenecks.

**Common silo types to avoid:**
- "QA-only" teams
- DBA-only teams
- UX-only teams
- Architecture-only teams
- Data-processing / ETL-only teams
- Operations-only teams (replace with stream-aligned + platform)

**Do:**
- Use cross-functional teams to drive "the simplest, most user-friendly solution" because all roles participate.
- Move toward stream-aligned teams that contain ops AND platform capabilities.
- Use platform teams as a replacement for "infrastructure," not an addition to it.

**Don't:**
- Don't carve out a "DevOps team" to centralize tooling expertise — that's an anti-pattern; it's typically a bottleneck, not an accelerator.

**Verbatim — Accenture healthcare case study:** DevOps tooling team started as anti-pattern → evolved to collaboration between Dev, Ops, and tooling → finished as the DevOps team playing an evangelizing/enabling role and making itself obsolete.

*Ref: Team_Topologies_2nd_Edition.md — "Avoid Team Silos in the Flow of Change"; Anti-pattern: DevOps team*

---

### Software-as-a-Team-Product — Treat Internal Services Like Products

**Principle:** A platform or service consumed by other teams should be treated as a product: versioning, roadmaps, customer feedback, market positioning, support model.

**Do:**
- Treat services as products with internal customers (the consuming teams).
- Apply product-management discipline: feature requests considered holistically, not built on demand.
- Track consumption metrics: number of consumers, usage patterns, time-to-onboard, satisfaction.
- Maintain SemVer promises and backwards-compatibility windows.

**Don't:**
- Don't let the producing team make unilateral breaking changes; announce, deprecate, migrate.

*Ref: Team_Topologies_2nd_Edition.md — "X-as-a-Service Mode"; "Platform Teams"*

---

### Workspace Design — Physical and Virtual Spaces

**Principle:** Physical and virtual environments affect team communication, which (via Conway's law) affects software architecture. Both must be designed deliberately.

**Do:**
- Use the **benched-bay layout** (one long bench per team, flanked by whiteboard partitions; smart-surface paint on end walls). ING Netherlands adopted this in its 2015 transformation.
- Use channels with prefixes (e.g., `#team-checkout-*`) so chat signals team boundaries.
- Reproduce the physical design virtues in virtual spaces — wiki, blogs, chat, work tracking.
- Design for "concentrated teamwork with occasional cross-team learning."

**Don't:**
- Don't use fully open-plan seating (no team boundary visibility) or fully individual cubicles (no cross-team learning).
- Don't overlook response-time, working-hours, and tone conventions for remote teams.

**Verbatim reference:** *Make Space* (Doorley & Witthoft); *Remote: Office Not Required* (Fried & Heinemeier Hansson).

*Ref: Team_Topologies_2nd_Edition.md — "Workspace Design"*

---

### Remote and Distributed Patterns

**Principle:** Virtual environment matters as much as physical for distributed teams. Tools alone aren't enough; teams need explicit ground rules on working hours, response times, video, and tone.

**Do:**
- Make team channels discoverable and stable (per-team or per-topic prefixes).
- Time-box synchronous collaboration across time zones; make async-first the default.
- Document team API expectations publicly: working hours, escalation paths, SLOs.
- Schedule "communities of practice" time across locations to preserve trust.

**Don't:**
- Don't assume Slack/Teams/Zoom equals effective remote collaboration; conventions must be designed and enforced.

**Verbatim — Heidi Helfand:** "If you must have remote workers, you will need to do extra work to foster the collaboration within the team and between the teams in order to build the community. You should try to have the same time zone versus different time zones; otherwise, people won't want to meet with each other because it cuts into their personal time at home."

*Ref: Team_Topologies_2nd_Edition.md — "Workspace Design"; case studies including ING, EBSCO*

---

### Software Architecture as Flows of Change — Not Static Structures

**Principle:** The flow of change through the organization determines software architecture. Teams that own the full lifecycle of a service produce better architectures than teams organized by silo.

**Do:**
- Treat architecture as the structure that supports change, not the snapshot at a moment in time.
- Measure DORA metrics (deploy frequency, lead time, change failure rate, mean time to restore) to sense flow quality.
- Align change cadence to architecture — slow-changing backend, fast-changing frontend.

**Don't:**
- Don't treat architecture as frozen; you'll freeze the org too.

*Ref: Team_Topologies_2nd_Edition.md — "Designing for flow of change"*

---

### Organizational Sensing — Detect When Teams Need Change

**Principle:** Organizations need mechanisms to detect when team structures are not working. Combine formal (dependency tracking, DORA metrics, cognitive load surveys) with informal (guilds, internal tech conferences, hallway conversations).

**Do:**
- Use a dependency matrix / dependency tags to track inter-team dependencies and wait times.
- Run regular dependency reviews; set thresholds and alerts for "dependency debt."
- Apply the Robert Axelrod finding: teams that rehearse interactions in learning contexts find it easier to interact in building/running.
- Adopt the GovTech Singapore forward-deployment team (FDT) model — embed experienced engineers in product teams, then gradually transfer capability out.

**Don't:**
- Don't rely solely on retrospective complaints to surface structural problems.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 8. Sensing the Organization"*

---

### Adoption of New Practices — Enabling Teams Spread Capabilities

**Principle:** New practices spread through stages: early adopters experiment → enabling teams spread successful practices → practice becomes standard. Use the facilitating interaction mode for this diffusion.

**Verbatim adoption curve (GovTech Singapore case study):**
> A forward-deployment team (FDT) acted as an enabling team, helping product teams adopt new practices around CI/CD, testing, and observability. The FDT was staffed with senior engineers who paired with product team members, gradually transferring knowledge and capability. DORA and SPACE frameworks measured impact.

**Do:**
- Identify early adopters and seed them with the new practice.
- Send enabling teams in to coach/mentor the next ring of teams.
- Measure adoption in objective terms (DORA, SPACE).
- "Plan for your own extinction" — enabling teams should not become a permanent dependency.

**Don't:**
- Don't mandate adoption top-down. Trying to fix engineering issues by mandating them from above is "doomed to failure."

*Ref: Team_Topologies_2nd_Edition.md — "Adoption of New Practices"*

---

### Triggers for Team Topology Evolution

**Principle:** Specific signals indicate a team topology needs to change:
1. **Delivery cadence slowing down** — the team structure is misaligned with the work.
2. **Software too large for one team** — split along fracture planes.
3. **Multiple business services relying on one large set of underlying services** — needs more platform/stream-aligned teams.
4. **Growing dependencies per team** — see Dominica DeGrandis's Physical Dependency Matrix.
5. **Increasing wait times** — measure with dependency tracking.
6. **Rising cognitive load** — measure with Teamperature / regular surveys.
7. **Repeated delivery failures or low morale** — listen for them.

**Do:**
- Set up dependency tracking and review dependencies regularly.
- Act on the data, not on the loudest voice in the room.
- Expect evolution to take longer than expected (TransUnion case study: three years longer than originally planned).

**Don't:**
- Don't reorganize for convenience. Reorganizations that ignore Conway's law and cognitive load are "open-heart surgery performed by a child: highly destructive."

*Ref: Team_Topologies_2nd_Edition.md — "Team Topology Evolution"; "Recognize Triggers for Organization Change"*

---

### Self-Steering Design and Development

**Principle:** Self-steering teams sense and respond to their own needs within organizational guardrails. Requires trust, clear boundaries, and access to information.

**Do:**
- Apply Jeff Sussna's "continuous design" (from *Designing Delivery*): treat service, feedback, failure, and learning as first-class concepts.
- Adopt Naomi Stanford's modern organization design framework: design for collaborative technologies and the voice of the customer.
- Set boundaries, not processes.
- Trust teams to handle ambiguity within their scope.

**Don't:**
- Don't micromanage "for safety" — it reduces ownership and pace.

*Ref: Team_Topologies_2nd_Edition.md — "Self-Steering Design and Development"*

---

### Environmental Scanning — Strategic Sense-Making

**Principle:** Monitor external trends (new technologies, market shifts, regulatory changes) for required organizational adaptation. This is a strategic responsibility, not just a technical one.

**Do:**
- Scan for shifts in regulation (GDPR, AI Act), technology (LLMs, edge compute), and market structure.
- Translate external shifts into internal team-topology changes (e.g., IoT drove the addition of connected-device stream-aligned teams and device-management platforms).

**Don't:**
- Don't adopt every trend; sense for the ones that materially change your competitive position.

*Ref: Team_Topologies_2nd_Edition.md — "Environmental Scanning"*

---

### Avoiding the BAU Anti-Pattern

**Principle:** Separating "new feature" teams from "maintenance" teams is an anti-pattern. Stream-aligned teams should handle operational concerns with support from enabling and platform teams.

**Do:**
- Use a "side-by-side" approach for new services: a new team takes on a new service while the existing team continues with the legacy system, with a planned transition period.

**Don't:**
- Don't isolate "BAU" teams — that's a recipe for slow incident response and disengaged operations.

**Verbatim — Sriram Narayan:** "Separate maintenance teams and matrix organizations...work against responsiveness."

*Ref: Team_Topologies_2nd_Edition.md — "BAU teams" anti-pattern*

---

### Composition of Teams — Avoid Single-Mode Teams

**Principle:** Cross-functional teams tend to find the simplest, most user-friendly solution; teams of single-functional expertise bias toward their domain.

**Verbatim:**
> "The use of cross-functional, stream-aligned teams has a very useful side effect. Precisely because stream-aligned teams are composed of people with various skills, there is a strong drive to find the simplest, most user-friendly solution in any given situation."

**Don't:** Don't mistake functional purity for higher quality — specialization without cross-functional pressure produces overengineered solutions.

*Ref: Team_Topologies_2nd_Edition.md — "Avoid Team Silos in the Flow of Change"*

---

### Don't Reorganize for Convenience — Conway's Law Applies

**Principle:** Reorganizations for headcount convenience, "management efficiency," or "synergies" are usually destructive of effective software delivery.

**Do:**
- Treat reorganization as a structural lever you pull rarely and deliberately.
- Use the **reverse Conway maneuver** when reorganizing: choose the team structure that produces the architecture you want.

**Don't:**
- Don't reorganize for management convenience.
- Don't reorganize without an architecture target.
- Don't reorganize before diagnosing with dependency tracking, cognitive load surveys, and DORA trends.

**Verbatim:**
> "Regular reorganizations for the sake of management convenience or reducing headcount actively destroy the ability of organizations to build and operate software systems effectively. Reorganizations that ignore Conway's law, team cognitive load, and related dynamics risk acting like open heart surgery performed by a child: highly destructive."

*Ref: Team_Topologies_2nd_Edition.md — "Org chart thinking" / Conway's Law chapter*

---

### Software-as-a-Team-Product Across the Lifecycle

**Principle:** Treat internal services like products across the entire lifecycle: design → build → deploy → operate → evolve → sunset.

**Lifecycle-stage guidance:**
- **Explore:** collaboration mode; heavy interaction with consumers.
- **Exploit:** X-as-a-Service; stable APIs; versioned promises.
- **Sustain:** retained by a stream-aligned or platform team with operational ownership.
- **Retire:** deprecation roadmap, migration path, announcement cadence.

**Don't:** Don't keep a service alive past its useful life; the cognitive cost of maintaining it is rarely recouped.

*Ref: Team_Topologies_2nd_Edition.md — chapter 8 (organization evolution)*

---

### Five Concrete Steps to Get Started

**Principle:** Team Topologies is a starting framework, not a destination. Five concrete steps to begin the transition:

1. **Identify suitable streams of change** — clear external/internal customers; can move at own cadence without blocking.
2. **Build the thinnest viable platform** — minimum platform services that actually help stream-aligned teams.
3. **Assess capability gaps** — what's missing? What patterns repeat?
4. **Share and practice interaction modes** — explain collaboration/X-as-a-Service/facilitating explicitly; train teams.
5. **Evolve continuously** — sense, respond, repeat.

**Verbatim conclusion:**
> "There is no autopilot for organizational change. Org design is like a martial art; you have to keep practicing to stay sharp."
> — Ismail Chaib

*Ref: Team_Topologies_2nd_Edition.md — "Conclusion: The Road Ahead"*

---

### Static Adoption vs. Continuous Evolution

**Principle:** "All models are wrong, but some are useful." (George Box via Deming.) The four team types and three interaction modes are building blocks, not end states. Organizations that treat them as static destinations miss the core dynamic.

**Do:**
- Treat the four types and three modes as a shared vocabulary to discuss structure.
- Use Team Topologies to start the conversation, not to end it.
- Plan for organizational change to take 3+ years for major transformations (TransUnion: 4 years from hybrid DevOps to fully integrated).

**Don't:**
- Don't impose the framework top-down as a single-shot reorganization.
- Don't confuse mapping existing teams to four types with evolution — mapping is the start, not the goal.

**Verbatim — George Box:** "All models are wrong, but some are useful."

*Ref: Team_Topologies_2nd_Edition.md — "Foreword to the Second Edition"; "Conclusion"*

---

### Foundation Patterns — Team APIs Across Stack Layers

**Principle:** The team API concept scales: every layer of the organization should have explicit APIs between adjacent layers.

**Layered team APIs:**
- Stream-aligned ↔ Stream-aligned (collaboration or X-as-a-Service)
- Stream-aligned ↔ Complicated-subsystem (X-as-a-Service)
- Stream-aligned ↔ Enabling (Facilitating)
- Stream-aligned ↔ Platform (X-as-a-Service for consumption; collaboration for new capability discovery)
- Platform ↔ Platform (X-as-a-Service; lower platform serves higher)
- Enabling ↔ Platform (Facilitating or collaboration)

**Do:** Design each interface; don't allow it to evolve by accident.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 7*

---

### Anti-Pattern: "Single Ops Team" / "Single Support Team"

**Principle:** Separate operations or support teams create handoffs, delays, and reduced accountability. Operations and support belong inside stream-aligned teams (with swarming, not tier-1/2/3).

**Do:**
- Put on-call rotation inside the stream-aligned team (you build it, you run it).
- Use an enabling team for SRE-style expertise at first; transition to stream-aligned ownership.
- Apply "swarming" — bring the right experts together to resolve incidents, rather than passing tickets between tiers.

**Don't:** Don't keep "ops" or "support" as their own topology — every team is responsible for production. The 4 fundamental types deliberately exclude ops/support teams.

**Verbatim — Jon Hall:** "The inclusion of inexperienced frontline support staff in these swarms gives exposure to knowledge that would otherwise only start to be gained after eventual promotion to more specialist teams."

*Ref: Team_Topologies_2nd_Edition.md — note "Where is the Ops team?"; "Convert Traditional Support to Swarming"*

---

### Anti-Pattern: Static Component Teams — Rename and Re-scope

**Principle:** Traditional component teams (front-end / back-end / DBA) are anti-patterns in fast-flow organizations. Convert them:
- **Component team → Platform team** providing the component as a service.
- **Infrastructure team → Platform team** (TVP, product mindset).
- **Tooling team → Enabling team** (transfer tooling use rather than centralize it).
- **Support team → Swarming in stream-aligned teams** + enabling teams for knowledge.
- **Architects → Embedded in stream-aligned teams** (architects act as enablers, not gatekeepers).

**Do:** Conduct a topology-mapping exercise; for each existing team, decide which of the four fundamental topologies they should adopt (or be split into).

*Ref: Team_Topologies_2nd_Edition.md — "Converting Common Team Types"*

---

### Building Software Architecture via Team Boundaries

**Principle:** Software architecture follows team boundaries (Conway's law). To change an architecture, change the team boundaries — not the other way around.

**Do:**
- Sketch the desired architecture (services, APIs, data flows).
- Derive the team boundaries required to support that architecture.
- Use the reverse Conway maneuver: design the team structure to beget the desired architecture.
- Pair the reverse maneuver with collaboration and facilitating modes to test new boundaries.

**Don't:**
- Don't insist on the new architecture before the team boundaries exist; both evolve together.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 2, "Chapter 8"*

---

### Adopting New Patterns via "Stealth" Diffusion

**Principle:** When an organization resists a new pattern, embed it in an enabling team and let it spread organically.

**Do:**
- Form a small enabling team with senior practitioners who embody the new pattern.
- Pair with one stream-aligned team first; get a measurable win.
- Spread to adjacent teams; broadcast outcomes (demos, recorded sessions).
- Decommission when the practice is standard.

**Don't:**
- Don't mandate a practice before anyone has demonstrated it.
- Don't let the enabling team become a permanent department.

*Ref: Team_Topologies_2nd_Edition.md — "Adoption of New Practices"; Auto Trader and ING case studies*

---

### Recognizing the DevOps Topologies Anti-Pattern

**Principle:** A "DevOps team" that executes tooling steps for delivery is a hard dependency and quickly becomes a bottleneck. Convert to enabling or to platform.

**Diagnosis:** If the DevOps team is being asked to execute steps on the delivery path of every application — anti-pattern.

**Fix:**
- Enable other teams to use the tooling themselves (enabling team).
- Or build self-service capabilities that teams use autonomously (platform team).

**Do:** Observe whether a "DevOps team" is helping or doing; the former is fine, the latter is the anti-pattern.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 4*

---

### Combining Team Topologies With Other Approaches

**Principle:** Team Topologies pairs cleanly with:
- **Sooner Safer Happier** (Jon Smart) — for cross-cutting transformation practices.
- **Dynamic Reteaming** (Heidi Helfand) — for changing team composition safely.
- **Data Mesh** (Zhamak Dehghani) — domain-oriented ownership of data.
- **Architecture for Flow** (Susanne Kaiser) — combines TT with Wardley Maps and DDD.
- **Continuous Delivery / DORA** — measurement substrate.

**Do:** Pick complementary frameworks; don't try to reinvent them within TT.

*Ref: Team_Topologies_2nd_Edition.md — Foreword to the Second Edition*

---

### SRE Pattern in Team Topologies

**Principle:** SRE (Site Reliability Engineering, Google) is a special kind of stream-aligned team responsible for the reliability of large-scale production applications. SREs interact primarily with one or more stream-aligned teams developing applications; the flow of software change is aligned to a stream.

**Do:**
- Treat SRE as a stream-aligned team serving reliability streams.
- Adapt the relationship over time: collaboration early, X-as-a-Service later as the application matures.
- Pair SRE with product teams via facilitating during early maturity (knowledge transfer).

**Don't:** Don't position SRE as a gatekeeper or external reviewer.

*Ref: Team_Topologies_2nd_Edition.md — "Site Reliability Engineering (SRE)" note*

---

### Tribe / Squad Patterns — Adaptation Notes

**Principle:** Spotify's "squads in tribes" is one adaptation. Adapting Team Topologies, the squad ~ stream-aligned team, the tribe ~ grouping. Use this structure when scale warrants.

**Do:**
- Use the **tribe** as a value stream grouping; squads inside as stream-aligned teams with shared platform within the tribe.

**Don't:**
- Don't treat tribe/squad literal names as a one-size-fits-all vocabulary.

*Ref: Team_Topologies_2nd_Edition.md — Workspace design reference to Spotify*

---

### Using Awkward Interactions to Sense Misaligned Boundaries

**Principle:** Awkward team interactions signal misaligned boundaries or missing capabilities. Use them as sensors.

**Examples:**
- Stream-aligned team spending hours trying to use a complicated-subsystem component → boundary/API/docs problem.
- Platform team expecting collaboration from a stream-aligned team and getting little interaction → maybe the consuming team doesn't understand the value, or the boundary being bridged is too ambitious.

**Do:** When interactions feel awkward, ask "Is this boundary right?" rather than "Are these people wrong?"

**Verbatim — Don Reinertsen:** "We need to be alert for the white space between the roles, gaps that nobody feels responsible for."

*Ref: Team_Topologies_2nd_Edition.md — "Use Awkwardness in Team Interactions to Sense Missing Capabilities and Misplaced Boundaries"*

---

### Hierarchy Is OK When It Supports Autonomy

**Principle:** Hierarchy in a Team-Topologies organization must serve the goal of aligning to streams of value, not legacy power structures.

**Verbatim:**
> "Real communication in organizations looks nothing like the hierarchical org chart; actual lines of communication cut across reporting structures in complex webs. ... Traditional organizational charts reflect historical power structures rather than communication pathways needed for effective software delivery."

**Do:**
- Use hierarchy to fund and protect the work of value streams, not to direct the work.
- Use Ruth Malan-style architectural governance: a small group of architects with influence over team interaction design, not centralized authority.

**Don't:**
- Don't treat hierarchy as the source of truth for how the system works.

*Ref: Team_Topologies_2nd_Edition.md — "Org chart thinking"*

---

### Fitness Functions for Team Topology Decisions

**Principle:** Use DORA metrics, cognitive load surveys, and dependency counts as "fitness functions" that signal whether the topology is working.

**Do:**
- Track DORA four: deployment frequency, lead time for changes, mean time to restore, change failure rate.
- Track team cognitive load via Teamperature-style surveys (4 clusters, 20+ drivers) regularly.
- Track inter-team dependencies and wait times; alert on thresholds.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 8*

---

### Case Studies — Nine Organizations in the Second Edition

The second edition includes nine detailed case studies (verbatim summaries from the appendix):

**1. EBSCO** — Reorganized teams around business domains using Team Topologies. **Results: 26% faster feature delivery; $9M+ cost savings; 197 additional features delivered; 76% reduction in P1/P2 incidents; 52% reduction in overall blockers.** Mike Gunning (SVP): "At first I was skeptical that reorganizing the teams would have any significant benefit. However, once the Team Topologies work had been completed, my development managers reported that they felt they had much less cognitive load and there was an increase in their job satisfaction."

**2. GovTech Singapore** — Used enabling teams (Forward Deployment Teams, FDTs) to help product teams adopt CI/CD, testing, observability. SPACE + DORA metrics measured impact. Inside-out approach: validate internally before scaling.

**3. ING Netherlands** — Applied Team Topologies as part of "ING Agile." Combined stream-aligned teams with enabling and platform teams. Benched-bay workspace. CEO-driven transformation. "Performance cockpit" with metrics that drive conversations.

**4. KFC UK&I** — Reorganized from component teams (mobile, web, kiosk) to stream-aligned teams (ordering, delivery, restaurant experience, loyalty). **Results: 3× increase in digital sales.** Three-month cognitive load assessment.

**5. Creditas** — Brazilian fintech (3,000+ employees). Used Teamperature to assess cognitive load across 4 clusters. Reorganized around value streams. Established platform teams to reduce cognitive load.

**6. Yassir** — North African super-app. Applied Team Topologies to scale engineering org. **Results: 230% increase in employee satisfaction over two years.**

**7. Telenet** — Belgian telecom. Internal and external customer-centric tribes as value stream groupings. Combined Team Topologies with Wardley Maps.

**8. Trade Me** — NZ's largest online marketplace. Built a Thinnest Viable Platform: deployment pipelines, shared logging, a few self-service infra components. Evolved based on actual team needs.

**9. Adidas** — Multi-platform reality: digital platform, enterprise platforms (SAP, Salesforce, Microsoft), data and analytics platform. Used different interaction modes at different times (collaboration for discovery, enabling for onboarding, X-as-a-Service for stable services). 80% of engineering to cross-functional product teams; 20% to central platform team.

*Ref: Team_Topologies_2nd_Edition.md — Appendix: Case Studies*

---

### Verbatim: The Four Team Types and Three Interaction Modes (Figure 0.2)

**Four fundamental team types (verbatim):**
- **Stream-aligned:** A team aligned to the main flow of business change, with cross-functional skills mix and the ability to deliver significant increments without waiting on another team.
- **Platform:** A team that works on the underlying platform supporting stream-aligned teams in delivery. The platform simplifies otherwise complex technology and reduces cognitive load for teams that use it.
- **Enabling:** A team that assists other teams in adopting and modifying software as part of a transition or learning period.
- **Complicated-subsystem:** A team with a special remit for a subsystem that is too complicated to be dealt with by a normal stream-aligned team or platform team. Optional and only used when really necessary.

**Three interaction modes (verbatim):**
- **Collaboration mode:** Two teams work together on a shared goal, particularly during discovery of new technology or approaches. The overhead is valuable due to the rapid pace of learning.
- **X-as-a-Service mode:** One team consumes something provided by another team (such as an API, a tool, or a full software product). Collaboration is minimal.
- **Facilitating mode:** One team (usually an enabling team) facilitates another team in learning or adopting a new approach.

**Verbatim:** "Team interactions outside these three core interaction modes are wasteful and indicative of poorly chosen team responsibility boundaries and poorly understood team purposes."

*Ref: Team_Topologies_2nd_Edition.md — Figure 0.2, Conclusion*

---

### Verbatim: Core Ideas Summary (Figure 9.1)

**The book summarizes its core ideas (verbatim):**

1. **Team-first thinking:** Cognitive load, team API, team-sized architecture.
2. **Conway's law:** Use it deliberately through the reverse Conway maneuver.
3. **Four team types:** Stream-aligned, platform, enabling, complicated-subsystem.
4. **Three interaction modes:** Collaboration, X-as-a-Service, facilitating.
5. **Fracture planes:** Use natural seams in business domain, technology, regulation, team structure.
6. **Evolve continuously:** Sense, respond, repeat.
7. **Organizational sensing:** Treat operations as high-fidelity sensory input.
8. **Get started:** Begin with the team, identify streams, identify the TVP, identify capability gaps, practice team interactions.

*Ref: Team_Topologies_2nd_Edition.md — Conclusion*

---

### Decision Heuristics / Checklists

- **Should I create a new team?** Check that the new team has a clear stream of value, fits within team-size limits (5-9), and isn't duplicating an existing team's purpose.
- **Stream-aligned vs. platform?** If the team's work is consumed by other teams, it's platform; if consumed by end users, it's stream-aligned.
- **Collaboration or X-as-a-Service?** During discovery, collaboration. After API stabilizes, X-as-a-Service.
- **Should I reorganize?** Only with a target architecture (reverse Conway), supported by dependency data, and after the cultural groundwork is laid.
- **Cognitive load assessment:** Use Teamperature (20+ drivers, 4 clusters) at least quarterly.
- **Awkward interaction test:** When interactions feel wrong, ask "Is this boundary right?" not "Are these people wrong?"
- **Fast flow test:** "Are our product teams spending enough time focused on our end customers' needs?"
- **Stream fit test:** Does the stream have clear customers? Can it move at its own cadence without blocking?
- **TVP test:** Is the platform the smallest set of services that helps stream-aligned teams?
- **Ratio test:** Most successful orgs have 6:1 to 9:1 stream-aligned to non-stream-aligned ratio.

## Anti-Patterns & Common Mistakes

- **Single Ops Team:** Centralized operations team becomes a bottleneck. → Move ops inside stream-aligned teams (you build it, you run it) with enabling-team support for expertise.
- **Static Component Teams:** Front-end / back-end / DBA teams separate by technical layer. → Convert: component team → platform; infrastructure → platform; tooling → enabling; support → swarming; architects → embedded.
- **BAU / Maintenance Split:** "New feature" teams separated from "maintenance" teams. → Use side-by-side approach; one team owns both.
- **"DevOps Team" as Execution:** DevOps team executing delivery steps for every team. → Convert to enabling (helping teams use tooling) or platform (self-service).
- **Reorganization for Convenience:** Reorgs for headcount or "management efficiency." → Use reverse Conway maneuver; treat reorg as rare, deliberate.
- **Naive Microservice Mapping:** One team per microservice, ignoring cognitive load. → Size boundaries to team cognitive capacity.
- **Town-Hall Adoption:** Mandating practices top-down. → Use stealth diffusion via enabling teams.
- **Permanent Tier-1/2/3 Support:** Tiered support creates handoffs. → Use swarming.
- **Open-Plan Monolithic Workplace:** One layout for everyone. → Use benched-bay or hybrid; design for varied work modes.
- **Single Platform for All Personas:** One platform serving digital, enterprise, and data personas. → Use multiple coherent platforms (NAV model).
- **Bucket Cognition of Load:** "Team at capacity, can't add more." → Use river analogy; temporary increase is OK with clear objective.
- **Holding Org Chart as Truth:** Treating the org chart as communication structure. → Map actual communication; it's a complex web.

## Key Takeaways

1. **Conway's law is real, measurable, and powerful.** Use the reverse Conway maneuver deliberately; don't fight it.
2. **Restrict teams to four fundamental types.** Stream-aligned (primary), enabling, complicated-subsystem, platform grouping. Most teams should be stream-aligned (6:1 to 9:1 ratio).
3. **Three interaction modes cover all team-to-team work.** Collaboration (discovery), X-as-a-Service (execution), facilitating (coaching).
4. **Platform is a grouping, not a single team.** Fractal: the four types appear inside platform groupings too.
5. **Use the Thinnest Viable Platform.** Build the minimum that helps stream-aligned teams; grow on actual demand, not anticipated.
6. **Treat cognitive load as a river, not a bucket.** Temporary increases are OK with clear objectives; avoid continuous increases without support.
7. **Use fracture planes to draw software boundaries.** Primary plane is DDD bounded context; secondary planes (compliance, cadence, location, risk, performance, technology, persona, natural) resolve remaining coupling.
8. **Team-sized software architecture.** Software boundaries must fit team cognitive capacity; this drives microservices-or-not decisions.
9. **You build it, you run it.** End-to-end ownership eliminates handoffs and improves quality.
10. **Fractal organization.** The same patterns repeat at every zoom level — fractal means platforms contain stream-aligned, enabling, complicated-subsystem teams, just like the consuming org does.
11. **Adopt via stealth diffusion.** Enabling teams spread practices organically; mandates fail.
12. **Evolve continuously.** Org design is a martial art — no autopilot.
13. **Detect awkward interactions as sensors.** Misaligned boundaries show up as friction, not as explicit complaints.
14. **The static-vs-continuous spectrum matters.** Mapping existing teams to four types is the start, not the goal.
15. **The river analogy beats the bucket analogy.** Cognitive load fluctuates; what matters is preventing chronic overload without support.

## Cross-References

- Related: [[../Learning_Systems_Thinking.md]] — Systems thinking is the conceptual foundation for team-level interventions (Iceberg Model, leverage points, feedback loops).
- Related: [[../Crafting_Engineering_Strategy.md]] — Strategy, leverage, and engineering decisions over time.
- Related: [[../Communication_Patterns.md]] — Communication structure design is half of Conway's law.
- Related: [[../Modern_Software_Engineering.md]] — General software engineering principles.
- Related: [[../Software_Architecture_Hardparts.md]] — Architecture trade-off analysis.
- Related: [[../Building_Microservices.md]] — Microservices patterns supporting team-sized architecture.
- Topic index: [[../INDEX.md]]
---

### CDL Office Layout — Benched Bay in Practice

**Principle:** CDL (Cambridge Decision Labs / UK retail insurance) designed a "benched bay" workspace that gave each team dedicated physical space while enabling cross-team collaboration.

**Verbatim — CDL case study:**
> "We came up with a 'benched bay' approach, with one long bench for each team, and each bench was flanked by whiteboard partitions. Where a team butted up to an end wall, we painted it with smart-surface paint so we could draw on it."

**Verbatim — CDL team-size insight:**
> "The size and growth of teams is also an important factor in design... The bench arrangement allowed for easy growth, especially if you haven't got supporting legs and pedestals in the way. Small teams could spread out while growing teams could squeeze up a bit."

**Verbatim — CDL split pattern:**
> "When the team is too big, we split it into two smaller teams, each taking functionally half of the backlog to make their own. The beauty of this is each team takes the culture of the old team with them, and they will diverge and grow themselves over time; but you can (with luck!) skip the 'storming' and 'norming' phases of starting a team from scratch."

**Do:**
- Use asymmetric bench placement (closer to one partition) for gathering room.
- Use portable whiteboards that can be repositioned as teams evolve.
- Allow teams to keep their culture when splitting.

**Don't:**
- Don't use symmetric bench placement that wastes gathering space.
- Don't use heavy, immobile partitions that can't be rearranged.

*Ref: Team_Topologies_2nd_Edition.md — "Office Layout at CDL" (Figure 3.4)*

---

### Streaming-Aligned Team Size and Composition Heuristics

**Principle:** Specific heuristics apply to assigning domains to teams based on relative complexity.

**Heuristics (verbatim from the book):**
- Assign each domain to a single team.
- A team of 5-9 can accommodate 2-3 "simple" domains.
- A team responsible for a **complex** domain should have no other domains — not even simple ones (because complex work needs focus; simple work steals time).
- Avoid a single team responsible for two **complicated** domains; the team will behave as two subteams with coordination overhead.

**Do:**
- Compare domains by relative complexity, not by absolute metrics.
- Re-classify when conditions change.

**Don't:**
- Don't shoehorn extra domains into a team because "they're simple."

*Ref: Team_Topologies_2nd_Edition.md — "Limit the Number and Type of Domains per Team"*

---

### OutSystems Case Study — Splitting an Overloaded Team

**Principle:** OutSystems' Engineering Productivity team grew from a 5-year-old team of 5 into an 8-person team responsible for build, CI, CD, test execution, infrastructure, and automation. Sprint planning became "mix and match" with constant context switching. The team split into three microteams.

**Verbatim — OutSystems team structure:**
- IDE productivity microteam (aligned with the IDE product area)
- Platform-server productivity microteam (aligned with platform server product area)
- Infrastructure automation microteam

**Results (verbatim):** "Motivation went up as each microteam could now focus on mastering a single domain... The mission for each team was clear, with less context switching and frequent intra-team communication... Overall, the flow and quality of the work...increased significantly."

**Do:**
- Recognize when a team has grown beyond its cognitive capacity, even if individual team members are still effective.
- Split along product-aligned lines, not just technical lines.

**Don't:**
- Don't grow a single team indefinitely just because the work feels "related."

*Ref: Team_Topologies_2nd_Edition.md — "Cognitive Load" / "Restrict Team Responsibilities to Match Team Cognitive Load"*

---

### IKEA Mobile Team Split — Conway's Law in Action

**Principle:** IKEA's mobile team was high-performing, but kept adding responsibilities. Despite having all intrinsic motivators (autonomy, mastery, purpose), they were cognitively overloaded. The team-lead recognized they had two products in one codebase and split the team in two.

**Verbatim — Bertilsson and Kotte (IKEA):**
> "This high-performing team kept adding more and more responsibilities on their shoulders, as the number of software products they maintained kept increasing. Eventually, they started to run into problems due to some work streams preventing the releases of others. Despite understandable pushback from the team, Bertilsson and Kotte managed to convince team members that they really had two products in the same codebase and needed to split the team in two, following Conway's law."

**Do:**
- Watch for "release prevention" symptoms as a signal of cognitive overload.
- Split by product or domain, even when team members resist (they will).

**Don't:**
- Don't preserve high-performing teams by giving them more responsibility; cognitive overload eventually degrades performance.

*Ref: Team_Topologies_2nd_Edition.md — "Match Software Boundary Size to Team Cognitive Load"*

---

### Poppulo Case Study — Fracture Planes in Practice

**Principle:** Poppulo (employee communications platform) used fracture planes to split a monolithic system. From a single team in 2015, they scaled to eight product teams, one SRE team, and an infra team by 2019.

**Verbatim — Poppulo:**
> "We began by adopting a stronger focus on 'the team' as the means to get work done. Previously we sometimes had bottlenecks around individuals, but by taking a team approach and adopting practices like pairing (and later, mobbing) we began to see better flow of work."

**Their approach:**
- Used DDD techniques, especially event storming, to understand domains.
- Aligned delivery teams to bounded contexts: email, calendar, people, surveys.
- Used Pact for contract testing.
- UX team acts as internal consultants across delivery teams (enabling).

**Verbatim — Poppulo on growth:**
> "Taking the time to understand our business domains and split our monolithic software up to match the domains has helped us to scale our engineering division from sixteen people to seventy people since 2015."

**Do:**
- Use event storming to surface domain boundaries before splitting teams.
- Apply DDD techniques to map bounded contexts to teams.

**Don't:**
- Don't split teams along technical layers; split along domain layers.

*Ref: Team_Topologies_2nd_Edition.md — "Finding Good Software Boundaries at Poppulo"*

---

### Sky Betting & Gaming Case Study — Platform Evolution

**Principle:** Sky Betting & Gaming had a "Platform Evolution" team that grew large enough that product teams couldn't easily consume its services. The team had to change — becoming a product team with services and support capabilities.

**Verbatim — Michael Maibaum (Sky Betting & Gaming):**
> "Platform Evolution became Platform Services and began to work with a very different worldview. Their mission was to provide services designed to support other teams with features and capabilities driven by their customers."

**Verbatim — Sky Betting & Gaming:**
> "Infrastructure reorganized around products and services; smaller teams owned the end-to-end life cycle of a coherent set of related things, with a drive to make them better for their customers around the business."

**Verbatim:** "We now have infrastructure-platform feature teams, just like we have customer-facing product feature teams."

**Do:**
- When a platform team becomes a bottleneck, re-scope it as a product with internal customers.
- Reorganize infrastructure around products and services, not around technical layers.

**Don't:**
- Don't let infrastructure teams remain "outside the product" structure.

*Ref: Team_Topologies_2nd_Edition.md — "Platform Evolution at Sky Betting & Gaming"*

---

### Kodea — Selective Adoption with Limited Budget

**Principle:** Kodea, an NGO promoting technological inclusion in Latin America, had no budget for dedicated platform teams. They selectively adopted Team Topologies patterns.

**Verbatim — Kodea:**
> "Kodea explored the platform pattern as a way to differentiate low-risk needs (e.g., presentations about the NGO to local audiences), which the stream teams could develop themselves using a self-service platform composed of templates, brand assets, and design guidelines. This freed up the communications and marketing team to focus on higher-impact or higher-risk needs, such as presentations to public authorities or international bodies, or the preparation of strategic funding proposals."

**Verbatim:** "Stream alignment, as well as enabling and platform patterns, can be applied outside of technology and be instilled from early stages, even when the organization lacks the capacity to establish dedicated teams neatly matching the team types."

**Do:**
- Apply patterns even when you can't dedicate teams to them; use shared knowledge, wikis, and senior practitioners as informal substitutes.
- Start with patterns; upgrade to dedicated teams when scale warrants.

**Don't:**
- Don't refuse Team Topologies because you can't have "ideal" team structures. Patterns work even without dedicated teams.

*Ref: Team_Topologies_2nd_Edition.md — Foreword (Kodea example)*

---

### Pirate Ship Heuristic — "Are Product Teams Focused on Customers?"

**Verbatim — Susanne Kaiser & Nina Siessegger at Fast Flow Conf 2025:**
> Pirate Ship, a growing tech company, realized that their stream-aligned teams' attention was being diverted as they tried to take care of technical components shared with other teams.

**Heuristic (verbatim):** "Are our product teams spending enough time focused on our end customers' needs?"

**Do:**
- Use this question to decide when to form a platform team: if stream-aligned teams are spending less than ~80% of time on customer-facing work, the platform is missing.

**Don't:**
- Don't ask "do we need more platform engineers?" — ask about what stream-aligned teams are spending time on.

*Ref: Team_Topologies_2nd_Edition.md — Foreword*

---

### The SPACE Framework for Developer Productivity

**Principle:** The SPACE framework (developed with Dr. Nicole Forsgren) evaluates developer effectiveness across five dimensions:

**The five dimensions (verbatim):**
1. **Satisfaction and well-being** — focusing on developer happiness, fulfillment, and growth opportunities.
2. **Performance** — measuring how well the software meets its intended function.
3. **Activity** — examining the volume and frequency of work.
4. **Communication and collaboration** — evaluating the quality and efficiency of communication within and between teams.
5. **Efficiency and flow** — highlighting teams' ability to progress smoothly with minimal interruptions.

**Do:**
- Use SPACE alongside DORA for a holistic view of developer productivity.
- Pair SPACE metrics with qualitative success stories.

**Don't:**
- Don't treat SPACE as a single-number KPI; it's multidimensional by design.

*Ref: Team_Topologies_2nd_Edition.md — "SPACE Framework" (GovTech Singapore case study)*

---

### The 20+ Drivers of Cognitive Load — Teamperature

**Principle:** The Teamperature model (with Dr. Laura Weis) identifies more than 20 drivers of team cognitive load, grouped into 4 clusters. The questions themselves raise team awareness.

**Four clusters (verbatim):**
1. **Team characteristics** — diversity, tenure, distributed vs. co-located, etc.
2. **Work practices and processes** — testing discipline, code review, deployment frequency, etc.
3. **Task characteristics** — domain complexity, code legacy, dependencies on other teams.
4. **Work environments and tools** — IDE quality, CI/CD reliability, on-call burden.

**Verbatim — book:** "People answering the model's survey for the first time often convey that the questions alone made them realize how many factors that can impact their cognitive load were not even on their radar."

**Do:**
- Use Teamperature quarterly to track cognitive load over time at team, group, and org levels.
- Pair quantitative drivers with qualitative interview follow-up.

**Don't:**
- Don't apply Teamperature once and forget it; trends over time are the value.

*Ref: Team_Topologies_2nd_Edition.md — Foreword (Teamperature with Dr. Laura Weis)*

---

### Toyota Kata and Mike Rother's Contribution

**Verbatim — Mike Rother, on Toyota:**
> "The roots of Toyota's success lie not in its organizational structures but in developing capability and habits in its people."

**Toyota Kata influence on Team Topologies:**
- Structured collaborative improvement: small experiments, reflection, adjustment.
- Improvement Kata: what is the target condition? What is the actual condition? What obstacles are preventing us? What is the next experiment?
- Coaching Kata: teaching the Improvement Kata through practice.

**Do:**
- Apply structured improvement routines to team-level challenges (cognitive load, dependency growth).
- Coach teams in improvement routines, not just give them answers.

**Don't:**
- Don't skip the practice of reflection; without it, improvement is accidental.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 7 (Mike Rother reference)*

---

### Heider's Attribution Theory and Team Interactions

**Verbatim — book:** "Our reactive thoughts are filled with emotional baggage, cognitive biases, conditioned responses, misunderstandings, and false narratives."

**Attribution patterns in teams (synthesized from the book):**
- Team A's slow delivery is attributed to Team B's incompetence (not to the API being underspecified).
- Team C's bug is attributed to Team D's carelessness (not to undocumented behavior).
- Team E's friction is attributed to personality (not to misaligned boundaries).

**Do:**
- Before attributing friction to people, attribute it to structure (boundaries, APIs, info flow).
- Apply Heider's principle: explain behavior in terms of structure first, disposition second.

**Don't:**
- Don't let the attribution default to people; structural attribution is the systems-thinker default.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 8" (implicit)*

---

### Scaling Dunbar-Groupings — From 5 to 500

**Principle:** Organizations should compose themselves from Dunbar-compatible groupings, each nested inside the next.

**The Dunbar layers (verbatim):**
- **Single team:** 5-9 people (high-trust: up to 15)
- **Families ("tribes"):** up to 50 people (high-trust: up to 150)
- **Divisions/streams/P&L lines:** up to 150 or 500 people

**Verbatim:**
> "Organizations can be composed from Dunbar-compatible groupings of these sizes; when one of the limits is reached, the need to split off another unit as a semi-independent grouping arises."

**Do:**
- Plan the org chart as nested concentric circles, not a flat hierarchy.
- When a layer hits its limit, split off a new semi-independent grouping.

**Don't:**
- Don't grow tribes beyond 50 without splitting — trust degrades, communication patterns change.

*Ref: Team_Topologies_2nd_Edition.md — "Scaling Teams Using Dunbar's Number" (Figure 3.1)*

---

### DORA Four — Deploy Frequency, Lead Time, MTTR, Change Failure Rate

**Principle:** DORA's four metrics are the canonical "fitness functions" for software delivery performance. Track them to sense flow quality.

**The four metrics (verbatim from Accelerate):**
1. **Deployment frequency** — how often code reaches production.
2. **Lead time for changes** — commit to deploy.
3. **Mean time to restore (MTTR)** — incident to recovery.
4. **Change failure rate** — % of changes causing failures.

**Verbatim — Accelerate:** "In teams which score highly on architectural capabilities, little communication is required between delivery teams to get their work done, and the architecture of the system is designed to enable teams to test, deploy, and change their systems without dependencies on other teams."

**Do:**
- Track all four, not just one or two.
- Use DORA as a leading indicator of topology health.

**Don't:**
- Don't use DORA as a team-level KPI; aggregate to the org level for sense-making.

*Ref: Team_Topologies_2nd_Edition.md — "Combine with DORA / Accelerate"*

---

### Team Boundaries via Promise Theory (Mark Burgess)

**Verbatim — book (Promise Theory):**
> "Promise theory—devised by technologist and researcher Mark Burgess—explains how and why it is preferable to construct inter-team relationships in terms of promises rather than in terms of commands and enforceable contracts."

**Promise Theory applied to teams:**
- Teams make explicit promises about what they will deliver.
- SemVer is a promise: major/minor/patch numbering signals what won't break.
- Teams accept promises voluntarily; non-compliance isn't enforced, it's noticed.

**Do:**
- Use semantic versioning as a "team promise" — never break SemVer expectations.
- Document team promises explicitly (in the team API).

**Don't:**
- Don't treat promises as enforceable contracts; trust is the substrate.

*Ref: Team_Topologies_2nd_Edition.md — Chapter 7 (Mark Burgess Promise Theory)*

---

### Adidas Multi-Platform Reality

**Principle:** Adidas operates three platform groupings: digital platform, enterprise platforms (SAP, Salesforce, Microsoft), and data & analytics platform. The digital platform itself is a logical grouping of multiple platforms.

**Verbatim — Adidas case study:**
> "Adidas also illustrates the multi-platform reality of large enterprises: alongside the digital platform, there are enterprise platforms (for SAP, Salesforce, Microsoft) and a data and analytics platform (supporting advanced analytics, big data, and enterprise reporting). The platform group actively engaged with other teams through enabling and collaborating interaction modes, helping teams learn good practices and effectively utilize the platform through consulting, training, onboarding, and co-creation."

**Verbatim — Fernando Cornago (Adidas):**
> "Adidas invested 80% of its engineering resources to creating in-house software delivery capabilities via cross-functional teams aligned with business needs. The other 20% were dedicated to a central-platform team taking care of engineering platforms and technical evolution, as well as consulting and onboarding new professionals."

**Verbatim — Adidas result:**
> "Adidas was able to increase release frequency of their digital products sixty-fold, while positively impacting software quality as well."

**Do:**
- Use multiple coherent platforms in large organizations.
- Avoid the "one platform to rule them all" anti-pattern.

**Don't:**
- Don't impose a single platform on disparate user personas.

*Ref: Team_Topologies_2nd_Edition.md — Adidas case study*

---

### The TransUnion Three-Year-Plus Evolution

**Principle:** TransUnion's team-topology evolution took **three years longer than originally planned** (2014 → late 2018). The journey went through five stages:

1. **Hybrid DevOps teams** (System Build + Platform Build) collaborating to bridge Dev and Ops.
2. **Awareness focus** — operability in Dev teams via the System-Build team collaborating with Platform-Build.
3. **Merged enabling team** (SB + PB) bringing Dev and Ops together.
4. **Decommission** of the temporary teams; merge back into Dev and Ops.
5. **Steady state** with Platform-as-a-Service provided by Ops.

**Verbatim — Dave Hotchkiss (TransUnion):**
> "Back in 2014, we expected to have evolved the SB and PB teams to a nice enabling team within twelve months. As it happened, this transition took quite a bit longer than we initially thought (three years longer!) as we started to move our services to Azure."

**Do:**
- Plan for longer evolution than initial estimates suggest.
- Treat topology change as a multi-year program, not a quarter.

**Don't:**
- Don't assume a 12-month timeline for major topology evolution.

*Ref: Team_Topologies_2nd_Edition.md — "Case Study: Evolution of Team Topologies at TransUnion"*

---

### Five Principles for Large-Scale Transformation (EBSCO)

**Verbatim — EBSCO lessons:**
1. **Empowering teams via technology** — creating an environment where teams can deliver value autonomously with appropriate support.
2. **Ongoing stewardship over project completion** — moving from "build and move on" to continuous care and evolution of services.
3. **Sociotechnical systems thinking** — recognizing that effective delivery requires alignment of human and technical elements.
4. **Fast flow through clear boundaries** — enabling rapid delivery by defining team interfaces that reduce coordination overhead.
5. **Cognitive load management** — ensuring teams can effectively maintain and evolve their services without becoming overwhelmed.

**Verbatim — Steve Whitaker (EBSCO):**
> "As a result of all of this work, we have a better understanding of our own systems. In order to achieve this, we had to do a lot of mapping that didn't previously exist, and we'll continue to reap benefits from that understanding for quite some time."

**Do:**
- Use all five principles in a major transformation; pick the weakest to focus on first.

**Don't:**
- Don't reduce transformation to "adopt team types." The principles go deeper than the model.

*Ref: Team_Topologies_2nd_Edition.md — EBSCO case study*

---

### Organizational Sensing — Peter Drucker's Synthetic Sense Organs

**Verbatim — Peter Drucker (cited in book):**
> "Without stable, well-defined neural communication pathways, no living organism can effectively sense anything."

**Applied to organizations:**
- Stable teams + well-defined communication = organizational sensing.
- Unstable teams + ill-defined communication = "senseless" organizations.

**Verbatim — book:**
> "Many organizations—those with unstable and ill-defined teams, relying on key individuals and (often) suppressing the voices of large numbers of staff—are effectively 'senseless' in both meanings of the word: they cannot sense their environmental situation, and what they do makes no sense."

**Do:**
- Treat ops teams as high-fidelity sensors for stream-aligned teams.
- Build feedback loops from production back to development.

**Don't:**
- Don't separate ops from dev; that breaks the sense organ.

*Ref: Team_Topologies_2nd_Edition.md — "Treat Teams and Team Interactions as Senses and Signals"*

---

### Three Ways of DevOps (Kim et al.)

**Verbatim — The DevOps Handbook (Gene Kim et al.):**
1. **Systems thinking** — optimize for fast flow across the whole organization, not just in small parts.
2. **Feedback loops** — Development informed and guided by Operations.
3. **Culture of continual experimentation and learning** — sensing and feedback for every team interaction.

**Team Topologies alignment:**
- Way 1 → Stream-aligned teams + reverse Conway maneuver.
- Way 2 → DevOps team-as-enabling-team or platform team providing high-fidelity feedback.
- Way 3 → Communities of practice, internal conferences, learning budgets.

**Do:**
- Apply all three Ways; you can't pick one.

**Don't:**
- Don't treat DevOps as a tool or a team; it's a culture and a structural stance.

*Ref: Team_Topologies_2nd_Edition.md — "IT Operations as High-Value Sensory Input"*

---

### Susanne Kaiser's "Architecture for Flow"

**Verbatim — book:**
> "Susanne Kaiser, for example, has talked and written extensively about evolving adaptive systems with 'Architecture for Flow,' seamlessly bringing together Team Topologies, Wardley Maps, and domain-driven design."

**Architecture for Flow key insight:**
- Use Wardley Maps to understand the evolution of capabilities (Genesis → Custom → Product → Commodity).
- Apply different team topologies at different evolution stages.
- Combine with DDD strategic patterns (bounded contexts, context maps).

**Do:**
- Treat this as a complementary framework for designing team + architecture together.

**Don't:**
- Don't reinvent Wardley Maps / DDD inside Team Topologies; use them as complements.

*Ref: Team_Topologies_2nd_Edition.md — Foreword*

---

### Heyden & Higgins' Team of Teams at ING

**Verbatim — Andy Higgins and Andy Heyden (ING):**
> "[We started] with a 'benched bay' approach for cross-functional teams and gradually introduced platform teams as the need for shared capabilities became clear."

**ING's key practice:**
- Combine stream-aligned, enabling, and platform teams.
- Workspace design supports concentrated teamwork with occasional cross-team learning.
- Scale gradually; don't introduce platform teams before the need emerges.

**Do:**
- Introduce platform teams when stream-aligned teams start doing duplicate infrastructure work.

**Don't:**
- Don't pre-build the platform; introduce when stream-aligned teams feel the pain.

*Ref: Team_Topologies_2nd_Edition.md — ING case study*

---

### The Unfreezing-Steady State Pattern

**Verbatim — book:**
> "Initial close collaboration evolves into more limited collaboration on a smaller number of things as the technology and product is better understood through discovery, and it further evolves into X-as-a-Service once the product or service boundary is more established."

**Three-phase pattern:**
1. **Close collaboration** (discovery).
2. **Limited collaboration** on a smaller subset.
3. **X-as-a-Service** for established, predictable delivery.

**Do:**
- Expect all three phases over the life of a service.
- Plan for transitions; don't stay stuck in collaboration.

**Don't:**
- Don't skip the limited-collaboration phase; it's where boundaries harden.

*Ref: Team_Topologies_2nd_Edition.md — "Evolution of Team Topologies" (Figure 8.6)*

---

### The Platform Wrapper Pattern — When Many Services Underpin One Stream

**Principle:** When multiple business services rely on one large set of underlying services, use a "platform wrapper" with consistent DevEx (correlation IDs, health checks, SLOs, diagnostic APIs).

**The wrapper provides:**
- Consistent logging timestamps and correlation IDs.
- Health-check endpoints.
- Service-level objectives.
- Test harnesses.

**Do:**
- Build the wrapper when stream-aligned teams waste time reconciling inconsistent underlying APIs.
- Give the stream-aligned teams rich telemetry.

**Don't:**
- Don't make stream-aligned teams learn every underlying subsystem's API.

*Ref: Team_Topologies_2nd_Edition.md — "Platform Wrapper" (Figure 8.8)*

---

### Architecture as Enabler (Don Reinertsen)

**Verbatim — Don Reinertsen:**
> "We can also exploit architecture as an enabler of rapid changes. We do this by partitioning our architecture to gracefully absorb change."

**Applied to teams:**
- Architecture decisions must anticipate change at the cadence of business demand.
- Static architecture decisions slow teams; flexible architecture accelerates them.

**Do:**
- Architect for change: defer decisions, prefer reversible ones, decouple parts that change at different speeds.

**Don't:**
- Don't over-architect in advance; let decisions be made by the teams that need them.

*Ref: Team_Topologies_2nd_Edition.md — "Organization Design Requires Technical Expertise"*

---

### Business Vision as the Fourth Gardening Input

**Verbatim — book:**
> "You can think of it like elements needed for creating and maintaining a garden: the Team Topologies approach acts like the instructions for placing the flowers and plants, along with patterns for pruning and training; whereas the cultural, engineering, and financial elements are like the soil, water, and fertilizer that helps the plants grow healthily."

**The four "gardening inputs":**
1. Team Topologies patterns (placement, pruning).
2. Healthy organizational culture (soil).
3. Good engineering practices (water).
4. Healthy funding and financial practices (fertilizer).

**A fifth:**
- Clarity of business vision (sunlight).

**Do:**
- Treat Team Topologies as one ingredient among five. The others matter equally.

**Don't:**
- Don't expect Team Topologies alone to fix a culturally unhealthy organization.

*Ref: Team_Topologies_2nd_Edition.md — Conclusion*

---

### Trust, Accountability, and Team Cohesion

**Principle:** "We need to maximize trust between people on a team, and that means limiting the number of team members."

**Do:**
- Reward the whole team, not individuals (Nokia: muted pay differences, team-based bonuses).
- Treat training budgets as team-level.
- Forbid "team toxic" behavior; remove toxic individuals.

**Verbatim — Nokia example (1990s-2000s):**
> "Pay differences across the organization were muted. Bonuses were small and typically paid on a team basis and on overall company performance, not individually."

**Don't:**
- Don't reward individuals over teams; it fragments collaboration.
- Don't ignore team-toxic individuals; they destroy teams faster than they build them.

*Ref: Team_Topologies_2nd_Edition.md — "Reward the Whole Team, Not Individuals"*

---

### Diversity Within Teams for Better Solutions

**Verbatim — Tom DeMarco and Timothy Lister (Peopleware):**
> "A little bit of heterogeneity can be an enormous aid to create a jelled team."

**Verbatim — Naomi Stanford (Guide to Organisation Design):**
> "People and organizations benefit from a diverse workforce where differences spark positive energy."

**Do:**
- Build diverse teams (background, perspective, seniority).
- Pair diverse team members; they make fewer assumptions about user needs.

**Don't:**
- Don't over-optimize for technical homogeneity; diversity reduces blind spots.

*Ref: Team_Topologies_2nd_Edition.md — "Embrace Diversity in Teams"*

---

### Final Heuristics & Quick References

- **Is this a stream-aligned team?** Does it own the full lifecycle for a value stream? If not, what other type?
- **Is the platform TVP-sized?** Can you point to actual stream-aligned teams that consume it daily?
- **Are interaction modes team habits?** Can the team describe its mode of interaction with each neighboring team?
- **Are awkward interactions tracked?** Are dependency reviews a routine?
- **Does the platform include the four types?** Is it fractal?
- **Is cognitive load measured?** Are Teamperature surveys run quarterly?
- **Are DORA + SPACE + Teamperature tracked together?** Treat them as complementary sensing mechanisms.
- **Is there a stealth enabling team for each new practice?** Can you name who is on it?
- **Are boundaries team-sized?** Is each segment owned by one team?
- **Is ops inside stream-aligned teams?** Are on-call rotations embedded?
- **Are architects embedded?** Or are they external gatekeepers?
- **Is the evolution continuous?** Are sense-and-respond loops operating?

---

### Mission, Vision, and Horizoned Time — From Lean Enterprise

**Verbatim — Jez Humble, Joanne Molesky, Barry O'Reilly (Lean Enterprise):**
> "Horizon 1 covers the immediate future with products and services that will deliver results the same year; Horizon 2 covers the next few periods, with an expanding reach of the products and services; and Horizon 3 covers many months ahead, where experimentation is needed to assess market fit and suitability of new services, products, and features."

**Applied to teams:**
- A team thinking only about Horizon 1 makes myopic decisions.
- A team with all three horizons makes "dirty fix now, clean fix in weeks" decisions.

**Do:**
- Encourage stream-aligned teams to plan across all three horizons.
- Allow short-term dirty fixes when the team owns the cleanup.

**Don't:**
- Don't ban quick fixes when the team owns the long-term cleanup.

*Ref: Team_Topologies_2nd_Edition.md — "The Team Owns the Software"*

---

### Treating Code as Gardening, Not Policing

**Verbatim — book:**
> "Note that team ownership of code should not be a territorial thing. The team takes responsibility for the code and cares for it, but individual team members should not feel like the code is theirs to the exclusion of others. Instead, teams should view themselves as stewards or caretakers as opposed to private owners. Think of code as gardening, not policing."

**Do:**
- Use the language "we steward" rather than "we own."
- Accept outside pull requests with grace; review quickly.

**Don't:**
- Don't treat outside contributors as interlopers.

*Ref: Team_Topologies_2nd_Edition.md — "The Team Owns the Software"*

---

### From Independent Service Heuristics (ISH) at EBSCO

**Verbatim — book:**
> "Conflux guided EBSCO through a methodical diagnostic process using an early version of Independent Service Heuristics (ISH). This approach helped identify natural boundaries for team alignment based on value streams rather than technical architecture."

**ISH key ideas:**
- Identify natural service boundaries from value-stream analysis.
- Don't pre-suppose technical architecture; let boundaries emerge from business flow.
- Test boundaries against ownership ("could we, as a team, effectively consume or provide this subsystem as a service?").

**Do:**
- Use ISH (or value-stream mapping) when boundaries are unclear.

**Don't:**
- Don't impose boundaries before analyzing the value flow.

*Ref: Team_Topologies_2nd_Edition.md — EBSCO case study*

---

### Verbatim: Heuristic for Choosing Team Boundaries

**Verbatim — book:**
> "A simple heuristic that can help guide assessment of your system and team boundaries is simply to ask: Could we, as a team, effectively consume or provide this subsystem as a service? If the answer is yes, then the subsystem is a good candidate for splitting off and assigning to a team to own and evolve."

**Do:**
- Apply this single question when debating any new boundary.

**Don't:**
- Don't split subsystems into teams unless the consuming team can treat them as a service.

*Ref: Team_Topologies_2nd_Edition.md — "Natural Fracture Planes"*

---

### Intermittent Collaboration Beats Constant Collaboration

**Verbatim — Bernstein et al.:**
> "Groups whose members interacted only intermittently...had an average quality of solution that was nearly identical to those groups that interacted constantly, yet they preserved enough variation to find some of the best solutions too."

**Do:**
- Schedule collaboration in bursts (sprints, weeks), then return to focused work.
- Allow intermittent periods for divergent thinking.

**Don't:**
- Don't maintain permanent collaboration; it erodes the diversity benefit.

*Ref: Team_Topologies_2nd_Edition.md — "Intermittent Collaboration" (Note)*

---

### The "Just Big Enough" Platform Heuristic (Verbatim)

**Verbatim — book:**
> "A platform can be 'just big enough' to meet the flow needs for the streams: anything from a set of documentation on a wiki that helps teams use the underlying services to a full, in-house, custom-technology solution built to meet the specialist needs of the stream-aligned teams."

**Do:**
- Scale platform formality to actual demand.
- A wiki is fine until it isn't.

**Don't:**
- Don't engineer the platform beyond what stream-aligned teams actually use.

*Ref: Team_Topologies_2nd_Edition.md — "Identify a Thinnest Viable Platform"*
