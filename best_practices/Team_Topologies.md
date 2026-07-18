# Team Topologies (2nd Edition)

**Authors:** Matthew Skelton, Manuel Pais
**Topic tags:** `#general` `#leadership` `#organization` `#architecture` `#platform`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Team_Topologies_2nd_Edition/Team_Topologies_2nd_Edition.md` · `summaries/Team_Topologies_2nd_Edition.md`

## TL;DR
A practical, adaptive model for designing team structures for fast flow of value to customers. Uses Conway's law deliberately (reverse Conway maneuver) and limits cognitive load on teams. Defines four team types (stream-aligned, enabling, complicated-subsystem, platform) and three interaction modes (collaboration, X-as-a-Service, facilitating) that combine to support continuous organizational evolution. Apply when designing team topology, splitting services, building a platform, or restructuring for flow.

---

## Best Practices by Topic

### Conway's Law and the Reverse Conway Maneuver

**Principle:** Conway's Law (1968): *"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."* The homomorphic force ensures that siloed teams produce siloed software; cross-functional teams produce modular architectures. Use this deliberately via the *reverse Conway maneuver* — design the team structure you want and let the software architecture follow.

**Do:**
- Identify the communication paths you want, then design teams around them. The architecture will follow.
- Apply the *inverse Conway maneuver* at the organizational level too — SEFAZ-RJ created a new business area around a citizen tax-refund journey; refunds dropped from multiple months to 24 hours.
- Treat team boundaries as the primary architectural lever; spend more time on team design than on micro-architectural details.
- Design for team-scoped flow: when a single team owns the full lifecycle (build, test, deploy, operate), architecture tends toward modularity and loose coupling.

**Don't:**
- Don't treat Conway's law as a 1:1 mapping between teams and microservices. The deeper point is about communication structure.
- Don't reorganize without a clear understanding of the desired communication patterns. Reorganizations are a blunt instrument.
- Don't use log-aggregation tools or mandated cross-team meetings to *force* the communication you want. Restructure the teams instead.
- Don't assume Conway's law can be defeated by heroic architecture work. The homomorphic force wins.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 2. Conway's Law and Why It Matters"*

---

### The Four Fundamental Team Types

**Principle:** Every team in the organization should gravitate toward one of four types. Most teams should be stream-aligned; the other three exist to support them. In 2nd Edition, "platform" is renamed as a *platform grouping* (a container of multiple teams, not a single team) in organizations larger than ~40–50 people.

#### Stream-Aligned Teams (the primary type)

- Aligned to a single valuable stream of work — a product, service, set of features, user journey, or user persona.
- Own the full lifecycle (build, test, deploy, operate). "You build it, you run it."
- Cross-functional: includes (or has access to) security, commercial analysis, design, development, infrastructure, metrics, product, testing, UX. Not every capability = dedicated individual.
- Close to the customer; receives direct feedback.
- Long-lived and sustainably funded (not project-shaped).
- Types of streams: customer, business-area, geography, product, user-persona, compliance.
- Expected: stable cadence, telemetry in production, attention to security/compliance, collaboration with enabling/platform teams as needed.
- Amazon's "two-pizza team" mandate (2002): every team fully responsible for developing and operating its own service through APIs.

#### Enabling Teams

- Help stream-aligned teams acquire missing capabilities. They *multiply*, not do the work.
- Detect capability gaps; research and try out new tools/practices.
- Temporary and transitional: an enabling team for a specific capability should eventually make itself unnecessary.
- Distinguish from communities of practice (voluntary, self-organizing vs. funded, purposeful).
- Expected: ask questions to find gaps, keep up with industry developments, act as coaches, proactively engage.

#### Complicated-Subsystem Teams

- Handle a component requiring deep specialist expertise (e.g., ML, real-time pricing, complex image processing).
- Provide their capability "as a service" with low interaction with consumers.
- Created only when the domain is genuinely beyond the capability of stream-aligned teams. "Most domains are not as complicated as they first appear."

#### Platform Teams (Platform Grouping)

- Provide internal services that reduce cognitive load for stream-aligned teams.
- *Thinnest viable platform (TVP):* start with the minimum services that actually help stream-aligned teams. Resist building comprehensive platforms before anyone needs them.
- *Managed as a live product:* versioned, with roadmaps, customer feedback, internal product management.
- *Fractal:* inside a platform grouping, the same team types appear (stream-aligned, enabling, complicated-subsystem, inner platform).
- In organizations < 40–50 people, a platform can be one team + a wiki. In larger organizations, a platform grouping contains multiple teams.

**Do:**
- Default most teams to stream-aligned. Platform / enabling / complicated-subsystem teams exist to *reduce cognitive load on stream-aligned teams*.
- Convert traditional team types: component teams → platform teams; infrastructure teams → platform teams; tooling teams → enabling teams; traditional support → part of stream-aligned teams with swarming.
- Embed architects as enablers, not gatekeepers.
- Use the *value stream grouping* concept for any grouping brought together around a common mission (a platform grouping is one specialization of value stream grouping).

**Don't:**
- Don't create enabling or complicated-subsystem teams preemptively. The capability gap must be real.
- Don't let platform teams become isolated silos building what they find interesting. They serve internal customers.
- Don't treat platform as "infrastructure team renamed." The platform is a product for internal customers.
- Don't create a "single platform that does it all" in a large enterprise — prefer "a small number of coherent internal platforms" (NAV model).

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 5. The Four Fundamental Team Topologies"*

---

### The Three Interaction Modes

**Principle:** All inter-team collaboration fits into three modes. Choose the right mode for the situation; expect modes to change over time. The reverse Conway maneuver works at the interaction-mode level: tell teams to collaborate → tight coupling; tell teams to X-as-a-Service → loose coupling with stable APIs.

#### Collaboration Mode
- High communication bandwidth (shared planning, joint retros, cross-team pairing).
- Divergent thinking: explore multiple solutions.
- Temporary by nature. Once discovery is done, transition to a more efficient mode.
- Bernstein et al. research: groups alternating between collaboration and independent work outperform groups in either pure mode.
- Use during the *discovery phase*.
- Costly; use sparingly — only when discovery value justifies coordination overhead.

#### X-as-a-Service Mode
- Low communication overhead; consumers use the service without understanding internals.
- Well-defined service boundaries; clear, versioned, documented API.
- Product-management discipline: the providing team treats the service as a product.
- Convergent thinking: solution space is well-understood.
- Compelling DevEx: easy to use, test, deploy, debug; current documentation.
- Feature requests considered but not always built — purpose evolved for the best interest of all consumers.
- Use during the *execution phase*.

#### Facilitating Mode
- One team coaches/mentors another to remove blockers or fill capability gaps.
- Based on Mark Burgess' promise theory — voluntary commitments, not imposed requirements.
- Don Reinertsen's "overlapping measurement" — both teams share some metrics without full responsibility overlap.
- Enabling teams work with stream-aligned teams primarily in this mode.
- Risk: the facilitating team becomes a crutch (teams stop learning). Step back at the right time.
- Use during the *learning phase*.

**Pairing matrix (interaction mode by team-type pair):**
- Stream-aligned ↔ Stream-aligned: Collaboration (shared features) or X-as-a-Service (shared services)
- Stream-aligned ↔ Platform: X-as-a-Service (primary) or Collaboration (new platform capability)
- Stream-aligned ↔ Enabling: Facilitating (primary)
- Stream-aligned ↔ Complicated-subsystem: X-as-a-Service
- Enabling ↔ Platform: Facilitating or Collaboration

**Do:**
- Make interaction modes explicit. Most people have never experienced a team-first way of working — explain and demonstrate the modes.
- Expect modes to evolve. A platform team may collaborate to discover requirements, then transition to X-as-a-Service once the capability stabilizes.
- Use the awkwardness of an interaction as a signal — if a stream-aligned team is spending hours trying to consume a "service" from a complicated-subsystem team, the boundary or documentation needs work.

**Don't:**
- Don't make collaboration permanent. It is a discovery mode, not an execution mode.
- Don't ship X-as-a-Service with a poor API or unclear documentation. The mode's whole value depends on low-overhead consumption.
- Don't let facilitating teams become a crutch — they should grow capability, not do the work.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 7. Team Interaction Modes"*

---

### Cognitive Load — Minimize Extraneous, Manage Intrinsic, Allocate Germane

**Principle:** Cognitive load is dynamic, not a fixed bucket that fills up (the 2nd-edition river analogy replaces the bucket). John Sweller's three load types apply to teams:

- **Intrinsic:** inherent complexity of the business domain and technical problem.
- **Extraneous:** unnecessary complexity from environment, tooling, processes, inter-team interactions. *Minimize this hardest.*
- **Germane:** effort of learning, improving, developing new capabilities. *Allocate time for this.*

A team should own **no more than one complicated or complex domain**. The 2nd-edition cognitive-load model (developed with Dr. Laura Weis) identifies 20+ drivers across four clusters: team characteristics, work practices and processes, task characteristics, work environments and tools.

**Do:**
- Assess cognitive load systematically (the Teamperature survey, developed with Dr. Laura Weis).
- Heuristic for domain assignment: relative domain complexity matters (a team owning a "complicated" real-time pricing domain should not also own a "complex" ML domain).
- Treat software-boundary size as a cognitive-load concern: if the boundary is too large, split it.
- Apply "Eyes On, Hands Off" — a team monitors a domain but doesn't actively develop it unless necessary.
- Allow temporary load spikes (taking on new ownership, modernizing systems) when there is a clear objective.
- Avoid the creeping, uncompensated load increase that comes from standing still while tools, services, and processes proliferate.

**Don't:**
- Don't add more people to a late project (Brooks's Law) — restrict team responsibilities instead.
- Don't offload work from the "important" team onto already-loaded teams. Cognitive load compounds.
- Don't treat load as a fixed bucket. A temporary increase is fine; chronic increase is not.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 3. Team-First Thinking" / "Cognitive load"*

---

### Team-First Thinking and Team APIs

**Principle:** The team is the smallest unit of delivery, not the individual. Effective teams are small (5–9 people — Dunbar's nested layers: 5, 15, 50, 150), long-lived, end-to-end owned, and have clear APIs to other teams.

**Do:**
- Make the team responsible for the full lifecycle including production operations. DORA research confirms end-to-end ownership produces faster, more reliable, higher-quality delivery.
- Keep teams stable. The Tuckman forming-storming-norming-performing cycle wastes if teams dissolve after each project. Use Heidi Helfand's "Dynamic Reteaming" guidance to change composition without losing effectiveness.
- Design an explicit *Team API*: code repos owned, documentation, versioning practices, communication channels (Slack prefixes like `#team-checkout-`), working hours. The team API should be well-defined, versioned, stable.
- Design workspace for the team. *Benched bay* = dedicated physical space. Virtual: Slack prefixes signal team boundaries and reduce noise.
- Foster communities of practice, guilds, and internal tech conferences — cross-team spaces for trust-building.
- Optimize for team autonomy, limited cognitive load, and clear boundaries. Diversity within teams requires psychological safety to function.

**Don't:**
- Don't dissolve teams after a project. Forming new teams has the highest cost in the Tuckman cycle.
- Don't hide the team API behind informal channels. If new engineers can't discover how to engage with a team, the API is broken.
- Don't conflate org-chart reporting lines with team communication paths. Org charts represent "how the organization looked at some time in the past" (Mark Schwartz).
- Don't optimize for cross-team communication across everyone. Restricted communication is *more* valuable than unrestricted communication.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 3. Team-First Thinking"*

---

### Fracture Planes — Where to Split the Software

**Principle:** Fracture planes are natural seams along which a software system can be split. Choosing the right fracture plane is the architectural decision; the team boundary follows. Nine fracture planes, ranked roughly by frequency of use:

1. **Business domain bounded context** (DDD) — primary fracture plane. Each bounded context has its own ubiquitous language.
2. **Regulatory compliance** — e.g., PCI DSS applies only to the subsystem handling card data, not the entire monolith.
3. **Change cadence** — parts that change at different speeds.
4. **Team location** — geographically distributed teams have different communication patterns.
5. **Risk** — high-risk components (payment, auth) may need different deployment, testing, security practices.
6. **Performance isolation** — heavy reporting load must not degrade real-time user-facing services.
7. **Technology** — Java back-end, React front-end, Python data pipeline = natural seams.
8. **User personas** — internal vs. external, admin vs. end-user.
9. **Natural fracture planes** — physical topology (e.g., manufacturing IoT along factory floor).

**Do:**
- Default to the business-domain bounded context as the first fracture plane to consider.
- Recognize monoliths in all their forms (not just the obvious application monolith): joined-at-the-database, hidden, monolithic thinking, monolithic workplace, monolithic rebuild, coupled releases, single view of the world.
- Treat software boundary size as a cognitive-load concern.
- Use *ecosystem tuning* — adjust boundaries over time as the system evolves.
- Allow a single stream-aligned team to own a bounded context. If it's too big for one team, split along another fracture plane.

**Don't:**
- Don't default to technology as the first fracture plane — it produces technical silos that map poorly to value delivery.
- Don't split monoliths into distributed monoliths (microservices that share a database or coordinate via chatty synchronous calls). Creditas hit this: "an overly complicated microservices architecture that was effectively a 'distributed monolith.'"
- Don't insist on one fracture plane per service. The right service may live on the intersection of two.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 6. Software Boundaries and Fracture Planes"*

---

### Thinnest Viable Platform (TVP)

**Principle:** Build the minimum platform capabilities that actually help stream-aligned teams. Resist the urge to build a comprehensive platform before anyone needs it. Treat the platform as a product with internal customers.

**Do:**
- Ask stream-aligned teams "what slows you down the most?" Build only that.
- Iterate the platform based on actual consumption, not anticipated requirements. (Trade Me's TVP started with deployment pipelines, shared logging, and a few self-service infra components — then grew as stream-aligned teams consumed and identified gaps.)
- Apply product-management discipline: versioning, roadmaps, customer feedback.
- Make the platform fractal: inside the platform grouping, the same team types appear.
- Use Wardley Maps to understand the evolution of platform capabilities and inform team-topology decisions.
- Use a small number of coherent internal platforms (NAV model) rather than one mega-platform in large enterprises.
- Identify platforms by value-stream cluster: digital platform, enterprise platform (SAP, Salesforce, Microsoft), data & analytics platform. (Adidas model.)

**Don't:**
- Don't build a comprehensive platform before teams need it. Empty platforms are expensive.
- Don't treat the platform as "infrastructure renamed." Infrastructure teams must adopt platform-thinking (product-management discipline).
- Don't grow the platform team in isolation. The platform is a product; it needs customers.
- Don't expect a single platform to serve all needs at scale.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 5. The Four Fundamental Team Topologies" / "Platform Teams"; Trade Me, Adidas case studies*

---

### Sensing and Continuous Evolution

**Principle:** Team topologies are not a static target. Organizations must continuously sense (monitor cadence, cognitive load, dependencies, wait times) and respond (adjust types, modes, boundaries).

**Do:**
- Apply formal sensing: DORA metrics (deployment frequency, lead time, MTTR, change failure rate), SPACE framework (Satisfaction, Performance, Activity, Communication, Efficiency), dependency tracking (Physical Dependency Matrix / dependency tags on kanban cards).
- Apply informal sensing: guilds, communities of practice, internal tech conferences, hallway conversations.
- Watch for the three evolution triggers:
  1. **Delivery cadence slowing down** (cognitive overload, wrong boundaries, too many dependencies).
  2. **Software too large for one team** (split along fracture planes).
  3. **Multiple business services relying on one large set of underlying services** (introduce platform teams or additional stream-aligned teams).
- Evolve interaction modes over time. Discovery → X-as-a-Service as a service matures. Sky Betting's complicated-subsystem team collaborated closely during requirement discovery, then transitioned to X-as-a-Service as the component stabilized.
- Plan evolution as a long journey. TransUnion's transition took three years longer than expected; the benefits accumulated gradually.
- Combine team topologies — multiple stream-aligned, multiple platform, enabling teams surfaced when gaps appear.
- Use the *self-steering design and development* principle: empower teams to sense and respond to their own needs within organizational guardrails.
- Use a *side-by-side* approach when transitioning ownership: new team takes on a new service while the existing team continues with the legacy system, with a planned transition period.
- Apply *environmental scanning* — monitor external trends (IoT, AI, regulation) that may require organizational adaptation.

**Don't:**
- Don't treat the initial design as the destination. "There is no autopilot for organizational change."
- Don't skip the "side-by-side" transition when handing ownership between teams.
- Don't create BAU teams ("new feature" teams separate from "maintenance" teams). The handoffs destroy flow.
- Don't reorganize without a clear hypothesis about which communication patterns will improve.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 8. Sensing the Organization"; "Conclusion — The Road Ahead"*

---

### Anti-Pattern: Component Teams

**Principle:** Component teams own a slice of technology across the entire organization (e.g., "the database team," "the front-end team"). They produce component-driven software, handoffs, and bottlenecks. Convert to platform or stream-aligned teams.

**Do:**
- Convert component teams to platform teams when their component is widely consumed as a service.
- Convert component teams to stream-aligned teams when the component is naturally bounded by a single value stream.
- Use EBSCO's approach: from component teams (front-end, back-end, DB) → full-stack stream-aligned teams owning the entire vertical slice.

**Don't:**
- Don't accept "we need the front-end team's approval to deploy." That's a component team in disguise.
- Don't accept a "DevOps team" as a permanent home for tooling expertise. That becomes an anti-pattern (Accenture healthcare case: tooling team became an anti-pattern, eventually evolved to an evangelizing role that made itself obsolete).

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 4. Choosing Team Topologies for Fast Flow"; EBSCO case study*

---

### Anti-Pattern: BAU vs. Feature Teams

**Principle:** Splitting "new feature" teams from "maintenance / BAU" teams creates artificial handoffs and slows flow. Stream-aligned teams should handle their own operational concerns with support from enabling and platform teams.

**Do:**
- Make stream-aligned teams responsible for their own production operations.
- Use *swarming* when a stream-aligned team needs help on an incident — bring in experts from enabling/complicated-subsystem teams temporarily.

**Don't:**
- Don't have a "Tier 1 support team" that filters tickets for stream-aligned teams. That adds a layer and creates second-class citizens.
- Don't have a "maintenance team" that takes services away from stream-aligned teams. Use side-by-side transition instead.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 8" / "Business as usual (BAU) teams"*

---

### Conway's Law Naive Uses to Avoid

**Principle:** Common naive uses of Conway's law fail because they miss the deeper point about communication structures.

**Do:**
- Understand that team-scoped flow, focused communication, and the homomorphic force are the real levers.
- Use the reverse Conway maneuver as a targeted architectural intervention, not a one-time re-org.

**Don't:**
- Don't assume a 1:1 team-to-microservice mapping solves the problem.
- Don't force cross-team communication via log-aggregation tools, mandatory stand-ups, or shared chat channels. Restructure instead.
- Don't reorganize without first understanding which communication patterns need to change.

*Ref: Team_Topologies_2nd_Edition.md — "Chapter 2" / "Naive uses of Conway's law"*

---

### Organizational Sizing and the Fractal Pattern

**Principle:** The Team Topologies patterns repeat at multiple zoom levels. A value stream grouping contains multiple teams; a platform grouping contains multiple teams; inside each, the same four team types appear. The organization is *fractal*.

**Do:**
- Apply the same thinking at every zoom level. Inside a platform grouping, you have stream-aligned teams (specific platform services), enabling teams (helping onboard), complicated-subsystem teams (specialized platform components), and inner platform teams (further-down capabilities).
- Adjust the level of investment by organizational size. A startup of 30 people might have a "platform" that's a wiki maintained by the most senior engineer. An enterprise of thousands needs dedicated enabling and platform teams.
- Use this heuristic: "Are our product teams spending enough time focused on end customers' needs?" If not, the platform isn't doing its job.

**Don't:**
- Don't apply a one-size-fits-all structure. The patterns scale; the level of investment doesn't.
- Don't treat the four team types as an end state. The 2nd-edition clarifies: team types are building blocks.

*Ref: Team_Topologies_2nd_Edition.md — "Note on the Second Edition" / "Fractal organization"*

---

### Results the Approach Produces

**Real-world outcomes (2nd-edition foreword):**
- **EBSCO:** 26% faster feature delivery; >$9M in cost savings.
- **KFC UK&I:** 3× increase in digital sales.
- **Yassir:** 230% increase in employee satisfaction over two years.
- **SEFAZ-RJ:** Tax refunds dropped from multiple months to 24 hours; citizen complaints drastically reduced.
- **ING Netherlands:** Digital transformation at scale, with regulatory compliance aligned to specific stream-aligned teams.

**Common success factors across these cases:**
- Driven by clear business needs and competitive pressure.
- Continuous evolution, not big-bang re-org.
- Focus on cognitive load measurement (Teamperature).
- Adaptation to context (e.g., Kodea applying selectively without budget for dedicated platform teams).

*Ref: Team_Topologies_2nd_Edition.md — "Foreword to the Second Edition"; Appendix case studies*

---

## Anti-Patterns & Common Mistakes

- **Component team anti-pattern:** "The database team," "the front-end team" — produces handoffs and bottlenecks. *Fix:* Convert to platform or stream-aligned teams.
- **Static adoption anti-pattern:** Map existing teams to the four types without understanding flow, cognitive load, and evolution principles. *Fix:* Diagnose the underlying communication patterns first.
- **Platform as "infrastructure renamed":** Infrastructure team is told it's now a platform team, but no product-management discipline is adopted. *Fix:* Apply product management; treat internal teams as customers; iterate based on consumption.
- **Enabling team as a crutch:** Stream-aligned teams stop learning because the enablers will do it for them. *Fix:* Define explicit graduation criteria; enable until the capability spreads.
- **Permanent collaboration:** Two stream-aligned teams stuck in collaboration mode forever. *Fix:* Transition to X-as-a-Service once the discovery is done.
- **BAU vs. feature teams:** Splitting maintenance from new development creates handoffs. *Fix:* Stream-aligned teams own their services end-to-end; swarming for help.
- **Distributed monolith:** Microservices that share a database or coordinate via chatty synchronous calls. *Fix:* Identify the fracture plane that wasn't crossed (usually bounded context or data ownership).
- **Naive Conway:** Treating Conway's law as 1:1 mapping between teams and microservices. *Fix:* Focus on communication paths, not headcount.
- **Mega-platform:** One platform that does everything in a large enterprise. *Fix:* "A small number of coherent internal platforms" (NAV model).
- **Architect as gatekeeper:** Centralized architecture team blocks changes. *Fix:* Embed architects as enablers in stream-aligned teams.
- **Big-bang re-org:** Reorganize teams, hope it improves architecture. *Fix:* Use the reverse Conway maneuver as a targeted intervention tied to specific communication patterns.
- **Empty platform:** Built the platform before anyone asked for it. *Fix:* TVP — start with what stream-aligned teams actually need.
- **Tiered support:** Tier 1 → Tier 2 → Tier 3 → engineer. *Fix:* Swarming — stream-aligned team owns incidents; enabling teams provide specialized help on demand.

---

## Decision Heuristics / Checklists

- **Is this team a stream-aligned team?** Checklist: owns end-to-end lifecycle (build, test, deploy, operate); cross-functional; close to customer; long-lived; aligned to a single stream. If yes → stream-aligned. If you have to add qualifiers → it's probably one of the other three.
- **Should we create an enabling team?** Heuristic: are multiple stream-aligned teams struggling with the same capability (CI/CD, security, observability, mobile, data engineering)? If yes → enabling team may be warranted.
- **Should we create a complicated-subsystem team?** Heuristic: is the domain genuinely beyond the capability of stream-aligned teams (real ML, real-time pricing, complex search, image processing)? If no → don't create one. "Most domains are not as complicated as they first appear."
- **Should we create a platform team?** Heuristic: "Are our product teams spending enough time focused on end customers' needs?" If not, the platform isn't doing its job — either expand the platform or build a new one.
- **Which interaction mode?** Discovery → Collaboration. Execution → X-as-a-Service. Learning → Facilitating. If modes aren't shifting over time, the team topology is stagnating.
- **What's the right fracture plane?** Default to business-domain bounded context (DDD). Technology is a weak default. PCI DSS, change cadence, geographic location, risk, performance isolation are all valid when they apply.
- **Is the platform thinnest viable?** Checklist: did we ask stream-aligned teams what slows them down? Is the platform evolving based on consumption? Is it managed as a product with versioned APIs?
- **Cognitive load check:** Is the team owning more than one complicated or complex domain? Is extraneous load growing without compensation? Use the Teamperature survey or similar.
- **Evolution trigger:** Delivery cadence slowing? Software too large for one team? Multiple business services blocked on one shared set of underlying services? If any → restructure.
- **Side-by-side transition:** When handing ownership between teams, run both teams in parallel for a planned period. Don't cut over cold.

---

## Key Takeaways

1. **The team is the smallest unit of delivery.** Optimize everything around team effectiveness — size (5–9), lifespan (long), ownership (end-to-end), and boundaries (clear).
2. **Conway's law is the central lever.** Software architecture mirrors communication structure. Use the reverse Conway maneuver to shape architecture via team design.
3. **Four team types cover everything.** Stream-aligned (default), enabling (multipliers), complicated-subsystem (specialists), platform (cognitive-load reducers). Most teams should be stream-aligned.
4. **Three interaction modes.** Collaboration (discovery), X-as-a-Service (execution), Facilitating (learning). Choose by phase; expect evolution.
5. **Cognitive load is dynamic, like a river.** Minimize extraneous, manage intrinsic, allocate germane. A team should own no more than one complicated or complex domain.
6. **Use fracture planes to split software.** Bounded context is the default; PCI DSS, change cadence, geographic location, risk, performance isolation, technology, persona, natural domain boundaries are all valid.
7. **Platforms should be thinnest viable.** Build only what stream-aligned teams actually need; iterate based on consumption. Treat the platform as a product.
8. **Team topologies must evolve continuously.** Sense (DORA, SPACE, dependency tracking); respond (adjust types, modes, boundaries); repeat. There is no final state.
9. **Avoid common anti-patterns.** Component teams, BAU/feature splits, mega-platforms, empty platforms, permanent collaboration, distributed monolith, naive Conway, architects as gatekeepers.
10. **Fast flow means fast flow of customer value,** not just fast delivery from idea inception. Validate that customers benefit.
11. **Humanistic outcomes are real.** EBSCO 26% faster delivery and $9M+ saved; KFC 3× digital sales; Yassir 230% employee satisfaction. The approach works for humans, not just software.
12. **The pattern is fractal.** Stream-aligned, enabling, complicated-subsystem, and platform teams appear at every zoom level — inside value stream groupings, inside platform groupings.

---

## Cross-References
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] (platform engineering as Team Topologies platform teams)
- Related: [[../Platform_Engineering_Camille_F.md]] (platform-as-product fits stream-aligned + platform grouping)
- Related: [[../Technology_Strategy_Patterns.md]] (org design as technology strategy)
- Related: [[../Learning_Systems_Thinking.md]] (sociotechnical systems, leverage points, communication design)
- Related: [[../Building_Microservices.md]] (fracture planes applied to microservices)
- Topic index: [[../INDEX.md]]