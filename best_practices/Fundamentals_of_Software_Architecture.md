# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Fundamentals of Software Architecture
**Authors:** Mark Richards & Neal Ford
**Topic tags:** `#architecture` `#testing` `#api` `#distributed-systems`
**Language focus:** language-agnostic (Java/C# examples where they appear)
**Sources:** `markdown_output/Fundamentals of Software Architecture/Fundamentals of Software Architecture.md` · `summaries/Fundamentals_of_Software_Architecture.md`

## TL;DR
Foundational engineering-discipline treatment of software architecture: how to think architecturally, define and govern architecture characteristics, decompose systems into components, choose among the eight core styles (layered, pipeline, microkernel, service-based, event-driven, space-based, orchestration-SOA, microservices), capture decisions in ADRs, quantify risk via the risk matrix and risk storming, diagram with C4/UML/ArchiMate, and lead teams via the 4 C's. Apply whenever shaping system structure, evaluating style trade-offs, or establishing architectural governance.

---

## Best Practices by Topic

### Architect Role & Laws of Software Architecture

**Principle:** Architecture is the set of **structural decisions**, **architecture characteristics** ("-ilities"), **architecture decisions** (rules), and **design principles** (guidelines) — guided by two immutable laws.

**Do:**
- Treat architecture as the combination of **structure + characteristics + decisions + principles**; never answer "what's the architecture?" with only the structural style.
- Define architecture decisions as **rules** that constrain structure, and design principles as **guidelines** that nudge technology choice within those rules.
- Apply the **First Law** ("everything in software architecture is a trade-off") — and if you think you've found a non-trade-off, assume you haven't *identified* the trade-off yet.
- Apply the **Second Law** ("why is more important than how") — capture rationale so future architects can adapt decisions when context changes.
- Hold the eight core expectations simultaneously: make decisions, continually analyze, keep current, ensure compliance, have diverse exposure, possess business domain knowledge, possess interpersonal skills, navigate politics.
- Guide teams toward technology categories ("use a reactive-based web framework") rather than mandating products ("use React.js") — unless a specific characteristic (e.g., scalability, performance) forces a choice.
- Continue coding: POCs (production-quality), tech-debt stories, bug fixes, fitness-function automation, code reviews — never become an armchair architect.

**Don't:**
- Don't define the architecture role in one sentence — refuse the question (à la Martin Fowler / Ralph Johnson: *"Architecture is about the important stuff… whatever that is"*).
- Don't let structural decisions drift without rationale — that's how *Groundhog Day* decisions recur forever.
- Don't freeze architecture at design time — continuously analyze for "architecture vitality" (3+ years out, the original design must still meet today's needs).
- Don't let a single bad experience become a *frozen caveman* obsession that distorts every future decision.

*Ref: Fundamentals_of_Software_Architecture.md — "Introduction", "Laws of Software Architecture", "Expectations of an Architect"*

---

### Architectural Thinking & Knowledge Pyramid

**Principle:** An architect's value is **breadth** (knowing many things exist) more than **depth** (mastery of one thing); pair breadth with hands-on coding to stay credible.

**Do:**
- Build the middle of the knowledge pyramid ("stuff you know you don't know") aggressively once you transition to architect — that *is* technical breadth.
- For every solution candidate, ask "Programmers know the benefits of everything and the trade-offs of nothing. Do I understand both?"
- For every decision, ask "What is more important here: extensibility or security?" — the question is always answerable only in context.
- Practice analyzing trade-offs by enumerating advantages AND disadvantages on both sides of any choice (see auction system topic-vs-queue example).
- Avoid the **bottleneck trap**: don't own code in the critical path of a project. Delegate framework code to the team; write a business service 1–3 iterations behind.

**Don't:**
- Don't try to maintain deep expertise in a wide variety of areas — you'll succeed in none.
- Don't let *stale expertise* masquerade as current knowledge; large companies suffer when founder-developers make decisions with decade-old criteria.
- Don't separate architect from developers with virtual/physical barriers — they form a bidirectional loop, not a waterfall handoff.

*Ref: Fundamentals_of_Software_Architecture.md — "Architectural Thinking", "Technical Breadth", "Frozen Caveman Anti-Pattern", "Analyzing Trade-Offs"*

---

### Trade-Off Analysis: Auction System Topics vs Queues

**Principle:** Every decision has advantages AND disadvantages; identifying them all is the job.

**Topic advantages:**
- Architectural extensibility (no producer changes for new consumers)
- Service decoupling (producer doesn't know consumers)

**Topic disadvantages:**
- Data access / data security concerns (anyone with topic access can read all data)
- No heterogeneous contracts (all subscribers accept same payload)
- No per-queue programmatic load balancing/monitoring (AMQP allows it for queues)

**Decision heuristic:**
- Need extensibility + loose coupling → topic
- Need heterogeneous contracts + per-queue scaling + security → queue

*Ref: Fundamentals_of_Software_Architecture.md — "Analyzing Trade-Offs" (the auction example)*

---

### Conway's Law & Team Topology

**Principle:** System structure mirrors the communication structure of the producing organization. To get a desired architecture, evolve team structure accordingly.

**Do:**
- Use the **Inverse Conway Maneuver** (Jonny Leroy, ThoughtWorks) — consciously evolve team boundaries to promote the architecture you want.
- Prefer **domain-partitioned** teams (around workflows / bounded contexts) over technical-partitioned teams (UI team, DB team, backend team) when targeting microservices or modular monoliths.
- Align team size to ~12 or fewer (4 or fewer is small; >12 is big) — bigger teams incur process loss, pluralistic ignorance, and diffusion of responsibility.
- Co-locate (sit with) the development team — physical walls signal "do not disturb."

**Don't:**
- Don't organize teams by technical layer and expect domain-partitioned architecture to emerge.
- Don't add a developer without first checking there's a parallel work stream — adding people to a late project makes it later (Brooks's law).
- Don't let group-think (pluralistic ignorance) survive in meetings; watch facial expressions and explicitly invite dissent.

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Partitioning", "Conway's Law", "Making Teams Effective"*

---

### Architecture Characteristics ("-ilities") — Definition & Categories

**Principle:** An architecture characteristic meets three criteria: (1) specifies a nondomain design consideration, (2) influences some structural aspect of the design, (3) is critical or important to application success. Without all three, it's not an architecture characteristic.

**Do:**
- Pick the **top 3–5** characteristics that matter; ask stakeholders to pick their top three rather than argue priority orderings (Vasa lesson).
- Distinguish **explicit** (in requirements) from **implicit** (rarely written but required) characteristics; both must be discovered.
- Define characteristics precisely inside the organization — establish a ubiquitous language to prevent "performance" meaning different things to different teams.
- Recognize that operational characteristics heavily overlap with DevOps concerns; treat them as a first-class intersection.

**Don't:**
- Don't chase the "Italy-ility" anti-pattern — inventing a unique named characteristic to satisfy one past incident.
- Don't build a generic architecture that supports *all* characteristics; complexity explodes. Strive for the **least worst architecture**, not the best.
- Don't use the self-denigrating term "nonfunctional requirements" — "architecture characteristic" or "quality attribute" frames it correctly.

| Category | Examples |
|---|---|
| **Operational** | availability, continuity, performance, recoverability, reliability/safety, robustness, scalability, elasticity |
| **Structural** | configurability, extensibility, installability, leverageability/reuse, localization, maintainability, portability, supportability, upgradeability |
| **Cross-Cutting** | accessibility, archivability, authentication, authorization, legal, privacy, security, usability/achievability |

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Characteristics Defined", "Architectural Characteristics (Partially) Listed"*

---

### Identifying Architecture Characteristics

**Principle:** Characteristics come from **domain concerns** (translate business language → "-ilities"), **explicit requirements**, and **implicit domain knowledge** (e.g., university students procrastinate → scalability spike at registration close).

**Do:**
- Translate domain concerns using this mapping table:

| Domain concern | Architecture characteristics |
|---|---|
| Mergers and acquisitions | interoperability, scalability, adaptability, extensibility |
| Time to market | agility, testability, deployability |
| User satisfaction | performance, availability, fault tolerance, testability, deployability, agility, security |
| Competitive advantage | agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | simplicity, feasibility |

- Remember **agility ≠ time to market**: it's agility + testability + deployability. Forgetting one ingredient ruins the recipe.
- Try the litmus test: "Does it require domain knowledge to implement, or is it an abstract architecture characteristic?" Abstract ones (e.g., elasticity) belong in the architecture; domain-specific ones (e.g., "reputation index") need SME clarification first.
- Once identified, try the **eliminate-one** exercise: which characteristic can you drop? Often the explicit ones are culled first.

**Don't:**
- Don't treat scalability and elasticity as the same: scalability is concurrent-user throughput; elasticity is burst handling.
- Don't over-specify; one bad call ("this must be 5-nines when 3-nines is fine") drives complexity, cost, and negotiation overhead for years.

*Ref: Fundamentals_of_Software_Architecture.md — "Identifying Architectural Characteristics", "Case Study: Silicon Sandwiches", "Case Study: Going, Going, Gone"*

---

### Measuring & Governing Architecture Characteristics

**Principle:** Architecture characteristics must be measurable to be governable. Operational measures, structural measures, process measures — combined with automated fitness functions.

**Do:**
- Use **cyclomatic complexity (CC)**: keep methods under 10 (better: under 5). For an algorithmically complex domain, verify the complexity is essential not accidental.
- Establish **performance budgets** (e.g., K-weight budgets for page bytes, first contentful paint targets, 95th–99th percentile latency).
- Track **statistical models** for scalability/elasticity rather than arbitrary thresholds; alert on drift outside prediction intervals.
- Compute LCOM to expose incidental coupling in classes; use afferent/efferent coupling to analyze dependency direction.
- Track D = |A + I − 1| (distance from main sequence) and avoid the **zone of pain** (concrete + stable = brittle) and **zone of uselessness** (abstract + unstable = unused).
- Add K-weight budgets and 95th–99th percentile latency SLOs to the CI pipeline.

**Don't:**
- Don't report only *average* response time — outliers at 10× the average will kill users; always measure the long tail.
- Don't confuse structural measures (code-internal) with operational measures (system-in-production).
- Don't trust LCOM to detect *logical* lack of cohesion — it's a structural metric only.

*Ref: Fundamentals_of_Software_Architecture.md — "Measuring and Governing Architecture Characteristics", "Cyclomatic Complexity", "Operational Measures", "Structural Measures"*

---

### Fitness Functions & Governance

**Principle:** A **fitness function** is *any mechanism that provides an objective integrity assessment of some architecture characteristic or combination of characteristics* — a unit test, metric, monitor, or chaos experiment.

**Do:**
- Use a **triggered** fitness function (on commit) for static checks; **continuous** (in production) for runtime checks; **temporal** (scheduled) for security scans.
- Wire **JDepend**-style cycle detection into CI to prevent accidental cyclic dependencies (the IDE auto-import reflex destroys modularity).
- Use **ArchUnit** (Java) / **NetArchTest** (C#) to enforce layered architecture constraints as unit tests.
- Apply the **Simian Army** style: Conformity Monkey, Security Monkey, Janitor Monkey — Netflix's chaos approach to architecture governance.
- Design fitness functions **collaboratively** with developers — ivory-tower metrics get ignored.

**Don't:**
- Don't ascend to the ivory tower to design esoteric fitness functions developers don't understand.
- Don't wait for code reviews to catch architecture violations — by then damage is already in the codebase.
- Don't skip the developer buy-in step; tools that don't align with team mental models will be subverted.

```java
// ArchUnit fitness function to govern layered architecture
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")

// JDepend cycle test
@Test
void testAllPackages() {
    Collection packages = jdepend.analyze();
    assertEquals("Cycles exist", false, jdepend.containsCycles());
}
```

*Ref: Fundamentals_of_Software_Architecture.md — "Governance and Fitness Functions", "Cyclic dependencies", "Distance from the main sequence fitness function"*

---

### Modularity, Cohesion & Coupling

**Principle:** Modularity is an organizing principle; entropy is the natural state — architects must continually expend energy to maintain it. Cohesion + coupling + connascence form the vocabulary.

**Cohesion levels (best → worst):** functional → sequential → communicational → procedural → temporal → logical → coincidental.

**Do:**
- Prefer **functional cohesion**: every part of the module relates to a single well-defined task.
- Compute **LCOM** to find classes where field/method pairings don't share access — refactor them apart.
- Use **afferent** (incoming) and **efferent** (outgoing) coupling to analyze dependency graphs; remember the *a*-before-*e* mnemonic for afferent vs efferent.
- Continually refactor toward the **main sequence** (abstractness vs instability ideal line).
- Treat modularity as a *first-class implicit characteristic* — sustainable codebases require order and consistency.

**Don't:**
- Don't mistake LCOM for logical-cohesion detection — it's purely structural.
- Don't let shared utility classes accumulate; they bind unrelated code via incidental coupling.
- Don't lump many classes into a monolithic app for convenience — when restructuring, the loose partitioning becomes an impediment.

**LCOM definition:** the sum of sets of methods not shared via sharing fields. A class with two fields accessed by disjoint method groups scores high (lacks cohesion).

*Ref: Fundamentals_of_Software_Architecture.md — "Modularity", "Cohesion", "Coupling", "Abstractness, Instability, and Distance from the Main Sequence"*

---

### Connascence

**Principle:** Connascence = two components are connascent if a change in one requires the other to change to maintain correctness. Three properties govern its use: **strength** (weaker is better), **locality** (close-together connascence is fine), **degree** (count matters).

**Do:**
- Prefer **static** connascence (analyzable via source code) over **dynamic** (runtime-only).
- Apply the **Rule of Degree** (Jim Weirich): convert strong forms of connascence into weaker forms.
- Apply the **Rule of Locality** (Jim Weirich): as distance between software elements increases, use weaker forms of connascence.
- Follow Page-Jones's three guidelines:
  1. Minimize overall connascence by encapsulating
  2. Minimize connascence crossing encapsulation boundaries
  3. Maximize connascence within encapsulation boundaries

**Connascence cheat sheet (weakest → strongest):**

| Static | Dynamic |
|---|---|
| Name (CoN) — strongest static | Execution (CoE) — order matters |
| Type (CoT) | Timing (CoT-dynamic) — race conditions |
| Meaning / Convention (CoM/CoC) — magic numbers | Values (CoV) — multi-field transactions |
| Position (CoP) — argument order | Identity (CoI) — same entity reference |
| Algorithm (CoA) — strongest static | |

**Don't:**
- Don't accept magic numbers in arguments; convert to named constants (CoM → CoN).
- Don't use the 1990s connascence vocabulary as a proxy for synchronous vs asynchronous concerns in modern distributed systems — that distinction matters more.

*Ref: Fundamentals_of_Software_Architecture.md — "Connascence", "Connascence properties", "Unifying Coupling and Connascence Metrics"*

---

### Architecture Quantum

**Principle:** An **architecture quantum** = *an independently deployable artifact with high functional cohesion and synchronous connascence.* Quantum count determines monolith-vs-distributed decision.

**Do:**
- Scope architecture characteristics to the **quantum level**, not the system level — different quanta can have different characteristics.
- Use the quantum to decide monolith vs distributed: one set of characteristics → monolith; differing characteristics per component → distributed.
- Align quanta with DDD **bounded contexts** — they share the same boundary semantics.
- Treat the database as part of the quantum if it shares synchronous connascence with services; otherwise services with their own DB are separate quanta.

**Don't:**
- Don't treat all communication as asynchronous simply because it uses a message queue; if a synchronous request-reply is required, those services belong to one quantum.
- Don't assume microservices guarantees more quanta; a single quantum can still exist if services share a database.

*Ref: Fundamentals_of_Software_Architecture.md — "Scope of Architecture Characteristics", "Architectural Quanta and Granularity", "Domain-Driven Design's Bounded Context"*

---

### Component-Based Thinking

**Principle:** Components are the building blocks (between classes and services). Architects own component identification; developers own class design within components. **Iterate, don't finalize.**

**Do:**
- Identify top-level partitioning first: **technical** (layers: presentation/business/persistence) or **domain** (workflows/bounded contexts).
- Use the **component identification flow** iteratively:
  1. Identify initial components
  2. Assign requirements to components
  3. Analyze roles and responsibilities
  4. Analyze architecture characteristics (often forces subdivision)
  5. Restructure components (feedback loop)
- Apply discovery techniques: **Actor/Actions**, **Event Storming**, **Workflow approach**, **Naked Objects** (for pure CRUD).
- Start **coarse-grained** and split — splitting is easier than merging.
- Treat the component as the lowest level the architect owns; class design is the developer's.

**Don't:**
- Don't fall into the **entity trap** — designing one component per database table yields an ORM, not an architecture.
- Don't make components too fine (excessive inter-component communication) or too coarse (high internal coupling, poor deployability).
- Don't take initial architect designs as gospel — iteration with developers refines them.
- Don't architect class diagrams and design patterns (that's the developer's job).

*Ref: Fundamentals_of_Software_Architecture.md — "Component-Based Thinking", "Component Identification Flow", "Component Granularity", "Entity trap", "Actor/Actions approach", "Event storming", "Workflow approach"*

---

### Architecture Decision Records (ADRs)

**Principle:** An ADR is a short text file documenting one architectural decision. ADRs are the durable solution to the *Groundhog Day* and *Email-Driven Architecture* anti-patterns.

**Do:**
- Use the standard sections: **Title** (numbered, descriptive), **Status**, **Context**, **Decision**, **Consequences**; add **Compliance** and **Notes**.
- Status values: **Proposed**, **Accepted**, **Superseded** (with link to replacement ADR), **Request for Comments** (with deadline date).
- Write the Decision in commanding voice: *"We will use…"*, not *"I think…"* — passive phrasing signals indecision.
- Document both **technical** and **business** justifications; without business value, the decision shouldn't exist.
- Self-approval gate by **cost** (e.g., €5,000), **cross-team impact**, **security implication**.
- Store ADRs in a wiki (recommended) with directory layout: `application/{common, app1, app2}/`, `integration/`, `enterprise/`.
- Use **Superseded by X** / **supersedes Y** links to preserve history — avoid "what about using messaging?" revisits forever.
- Apply ADRs to **standards** too: forced justification of a standard often reveals the standard shouldn't exist.

**Don't:**
- Don't put architecture decisions in email bodies — create multiple systems of record.
- Don't notify everyone — only people the decision directly impacts.
- Don't include all detail in the email; provide a single link to the canonical ADR.
- Don't add every ADR to Git if your org has many non-developer stakeholders — wikis are easier to consume.

```
ADR 76. Asynchronous Pub/Sub Messaging Between Bidding Services

STATUS
  Accepted

CONTEXT
  The Bid Capture Service, upon receiving a bid from an online bidder or from a live
  bidder via the auctioneer, must forward that bid onto the Bid Streamer Service
  and the Bidder Tracker Service. This could be done using asynchronous
  point-to-point (p2p) messaging, asynchronous publish-and-subscribe (pub/sub)
  messaging, or REST via the Online Auction API Layer.

DECISION
  We will use asynchronous pub/sub messaging between the Bid Capture Service,
  Bid Streamer Service, and the Bidder Tracker Service.
  - Bid Capture Service does not need any information back.
  - Bid Streamer must receive bids in exact order → queues guarantee FIFO.
  - Async pub/sub increases performance and allows extensibility.

CONSEQUENCES
  - Requires clustering and high availability of message queues.
  - Internal bid events bypass security checks done in the API layer.
  - UPDATE: ARB Apr 14, 2020 — acceptable trade-off, no additional checks needed.

COMPLIANCE
  Periodic manual code and design reviews to ensure async pub/sub is being used.

NOTES
  Author: Subashini Nadella
  Approved By: ARB Meeting Members, 14 APRIL 2020
  Last Updated: 15 APRIL 2020 by Subashini Nadella
```

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Decision Records", "Basic Structure", "Storing ADRs", "ADRs as Documentation", "Using ADRs for Standards", "Example"*

---

### Architecture Decision Anti-Patterns

**Do:**
- Make decisions at the **last responsible moment** — enough info to justify, not so late you cause Analysis Paralysis.
- Continually collaborate with developers to validate decisions can be implemented.
- Communicate using **direct impact**: *"Hi Sandra, I've made an important decision about service communication that directly impacts you. Link…"*
- Justify decisions with **both technical and business** rationale (cost, time-to-market, user satisfaction, strategic positioning).
- Make only **architecturally significant** decisions: structure, characteristics, dependencies, interfaces, construction techniques.

**Don't:**
- Don't fall into the progressive anti-pattern chain: **Covering Your Assets** → **Groundhog Day** → **Email-Driven Architecture**.
- Don't repeat the same decision debate because the original rationale was lost — write it down as an ADR.
- Don't make technology decisions that aren't architectural significance (structure, characteristics, dependencies, interfaces, construction techniques).

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Covering Your Assets | Avoiding/deferring decisions | Last responsible moment + collaborate |
| Groundhog Day | Same decision relitigated forever | ADR with rationale |
| Email-Driven Architecture | Decisions lost in email | Single ADR link in email body |
| Ivory Tower | Dictating without developer input | Justify decisions; ask developers to arrive at solution themselves |

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Decision Anti-Patterns", "Architecturally Significant"*

---

### Risk Matrix & Risk Storming

**Principle:** Quantify architecture risk with a 3×3 matrix (Low/Med/High × Likelihood × Impact). Use **risk storming** for collaborative discovery.

**Risk matrix:** Impact ∈ {1,2,3} × Likelihood ∈ {1,2,3} → risk ∈ {1,2,3,4,6,9}. 1-2=low (green), 3-4=medium (yellow), 6-9=high (red).

**Do:**
- Apply **impact first, then likelihood** when scoring.
- Restrict each risk storming to **one dimension** (availability, elasticity, security, etc.) to keep focus.
- Begin with **individual identification** (no collaboration) so participants don't influence each other; follow with **collaborative consensus** and **mitigation**.
- For unproven or unknown technologies, **always assign the highest risk (9)** — the matrix can't measure what you don't understand.
- Show direction with **+ / −** signs (NOT arrows — ~50% of readers misinterpret arrows).
- Include senior developers and tech leads in risk storming — they catch what architects miss.
- Re-run risk storming after major features or at iteration end; risk identification is continuous.

**Don't:**
- Don't single-handedly assess risk; collaboration catches blind spots.
- Don't use arrows to show direction without a key (ambiguous).
- Don't skip the negotiation step — key stakeholders decide whether cost outweighs risk.

| Phase | Activity | Participants |
|---|---|---|
| Identification (individual) | Score each area on the matrix | Each participant alone |
| Consensus (collaborative) | Place Post-its, debate, agree | All together |
| Mitigation (collaborative) | Propose refactors | All together + stakeholders |

**Agile story risk analysis:**
- Add a *Risk* column to the story card with values 1, 3, 6, 9 (the matrix scores).
- Sum all risks on the iteration backlog → adjust iteration commitment accordingly.

*Ref: Fundamentals_of_Software_Architecture.md — "Risk Matrix", "Risk Assessments", "Risk Storming", "Agile Story Risk Analysis"*

---

### Architecture Styles — Decision Heuristics

**Principle:** Choose styles based on (1) domain, (2) architecture characteristics, (3) data architecture, (4) organizational factors, (5) knowledge of process/teams/ops, (6) domain/architecture isomorphism.

**Top-level partitioning decision:**
- **One quantum?** → monolith possible (modular monolith, layered, microkernel, pipeline)
- **Differing quanta?** → distributed required (service-based, event-driven, space-based, microservices, SOA)
- **Bursty load?** → space-based or event-driven
- **Semantic coupling (multipage forms with inter-page context)?** → avoid microservices; use service-based

**Communication style:**
- **Default to synchronous**; use **asynchronous when necessary** (responsiveness, decoupling, back-pressure).
- 95th–99th percentile latency is the design constraint, not average.

**Don't:**
- Don't pick a style based on fashion; let trade-off analysis drive it.
- Don't over-engineer a simple system with microservices.

*Ref: Fundamentals_of_Software_Architecture.md — "Shifting Fashion in Architecture", "Decision Criteria", "Choosing the Appropriate Architecture Style"*

---

### Architecture Style Comparison Matrix

| Style | Partitioning | Quanta | Deploy | Elastic | Evolut. | Fault tol. | Modularity | Cost | Perf. | Reliab. | Scalab. | Simpl. | Test | Use when |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Layered** | Technical | 1 | ☆ | ☆ | ☆ | ☆ | ☆ | ★★★★★ | ☆☆ | ☆☆☆☆ | ☆ | ★★★★★ | ☆☆ | Small/simple apps; tight budget; starting point |
| **Pipeline** | Technical | 1 | ☆☆ | ☆ | ☆☆☆☆ | ☆ | ☆☆☆☆ | ★★★★★ | ☆☆ | ☆☆☆☆ | ☆ | ★★★★★ | ☆☆☆☆ | ETL, EDI, data processing, Unix-style composability |
| **Microkernel** | Both | 1 | ☆☆☆ | ☆ | ☆☆☆ | ☆ | ☆☆☆ | ★★★★★ | ☆☆☆ | ☆☆☆ | ☆ | ☆☆☆☆ | ☆☆☆ | Product apps with plug-ins; high customization |
| **Service-Based** | Domain | 1-many | ★★★★★ | ☆☆ | ☆☆☆☆ | ★★★★★ | ★★★★★ | ☆☆☆☆ | ☆☆☆☆ | ★★★★★ | ☆☆☆☆ | ☆☆☆☆ | ☆☆☆☆ | Domain-aligned coarse services (4–12); pragmatic middle ground |
| **Event-Driven** | Technical | 1-many | ☆☆☆ | ☆☆☆ | ★★★★★ | ★★★★★ | ☆☆☆☆ | ☆☆☆☆ | ★★★★★ | ☆☆☆ | ★★★★★ | ☆ | ☆☆ | Asynchronous, highly scalable, dynamic workflows |
| **Space-Based** | Both | 1-many | ☆☆☆ | ★★★★★ | ☆☆☆ | ☆☆☆ | ☆☆☆ | ☆☆ | ★★★★★ | ☆☆☆☆ | ★★★★★ | ☆ | ☆ | High concurrent users (10k+), variable load, ticketing/auctions |
| **SOA** | Technical | 1 | ☆ | ☆☆☆ | ☆ | ☆☆☆ | ☆☆☆ | ☆ | ☆☆ | ☆☆ | ☆☆☆☆ | ☆ | ☆ | Avoid — historical context only |
| **Microservices** | Domain | 1-many | ☆☆☆☆ | ★★★★★ | ☆☆☆☆ | ☆☆☆☆ | ★★★★★ | ☆ | ☆☆ | ☆☆☆☆ | ☆☆☆☆ | ☆ | ☆☆☆☆ | High decoupling, independent release cadences, polyglot |

*Ref: Fundamentals_of_Software_Architecture.md — Chapter 10 (Layered), 11 (Pipeline), 12 (Microkernel), 13 (Service-Based), 14 (Event-Driven), 15 (Space-Based), 16 (SOA), 17 (Microservices)*

---

### Layered Architecture

**Do:**
- Use **closed layers** to enforce layers-of-isolation; open a layer only for shared services (e.g., logging) that everyone needs.
- Document open/closed status per layer — undocumented layer rules create brittle systems.
- Accept up to 20% sinkhole requests; if >80% are sinkholes, the layered style is wrong.
- Keep object hierarchies shallow and reuse minimal if you may need to migrate to a different style later.

**Don't:**
- Don't let the **sinkhole anti-pattern** dominate (>80% pass-through layers without logic).
- Don't be misled by the "fast-lane reader pattern" — opening all layers to bypass violates layers-of-isolation and makes change risky.
- Don't use layered for high-performance systems; closed layering and lack of parallel processing hurt throughput.

*Ref: Fundamentals_of_Software_Architecture.md — "Layered Architecture Style"*

---

### Pipeline Architecture

**Do:**
- Keep filters **single-purpose, stateless, self-contained**.
- Use **unidirectional point-to-point pipes** with small payloads for performance.
- Apply four filter types correctly: **Producer** (source), **Transformer** (map), **Tester** (reduce/route), **Consumer** (terminal).
- Leverage compositional reuse (Unix philosophy) — pipeline encourages elegant composition.

**Don't:**
- Don't put multiple responsibilities in a single filter — split into a sequence.
- Don't use bidirectional pipes; the architecture is one-way.

*Ref: Fundamentals_of_Software_Architecture.md — "Pipeline Architecture Style"*

---

### Microkernel Architecture

**Do:**
- Keep the **core system minimal** — just the happy path / minimum required to run.
- Use the **registry** pattern (in-memory map or external ZooKeeper/Consul) for plug-in discovery.
- Standardize plug-in **contracts** (AssessmentPlugin-style interfaces); create adapters for third-party plug-ins with non-standard contracts.
- Use shared-library plug-ins (JAR/DLL/Gem) for compile-time; OSGi/Jigsaw/Prism for runtime add/remove.
- Use namespacing convention `app.plugin.<domain>.<context>` for plug-in organization.
- Isolate volatile logic in plug-ins; let the core system stay stable.

**Don't:**
- Don't let plug-ins directly access a central shared database; the core should mediate data to keep change isolated to the core.
- Don't allow plug-ins to depend on each other — they must remain independent.
- Don't skip the registry or contract — without them the architecture becomes Big Ball of Mud.
- Don't turn this into a distributed architecture by making plug-ins remote unless you accept the cost/complexity.

*Ref: Fundamentals_of_Software_Architecture.md — "Microkernel Architecture Style"*

---

### Service-Based Architecture

**Do:**
- Keep services **coarse-grained and domain-scoped** (4–12 services, average ~7).
- Share a single database but logically partition it and use **federated shared libraries** per domain to localize schema-change impact.
- Lock **common entity** changes (used by all services) under restricted access — only DB team.
- Use **API gateway** for cross-cutting concerns (auth, rate limiting, routing) when exposing externally.
- Choose service-based when you want **ACID transactions** preserved without full microservices cost.

**Don't:**
- Don't use a single shared library for all entity objects — every schema change cascades to every service.
- Don't use interservice communication between domain services — avoid with shared DB.
- Don't pursue fine-grained microservices if you don't need the elasticity/extreme decoupling — service-based is the pragmatic middle ground.

*Ref: Fundamentals_of_Software_Architecture.md — "Service-Based Architecture Style"*

---

### Event-Driven Architecture (Broker vs Mediator)

**Do:**
- Choose **broker topology** for simple event flows needing high responsiveness/scalability; use topics (publish-subscribe) with federated brokers.
- Choose **mediator topology** for complex workflows needing workflow control, error handling, and restart capability.
- Have each event processor **always advertise** what it did — enables architectural extensibility (new consumers just subscribe).
- In mediator topology, use **multiple mediators per domain** to avoid single-point-of-failure and bottleneck.
- Use **delegate-classification** for mixed events: simple (Camel/Mule) → hard (BPEL/ODE) → complex (BPM/jBPM).

**Don't:**
- Don't expect the broker to provide error handling or recoverability — no one owns the state.
- Don't use the broker for complex multi-step business transactions — restart and data consistency suffer.
- Don't fall into "no one knows when the workflow completes" with the broker — that's the fundamental broker weakness.

| Topology | Use when | Avoid when |
|---|---|---|
| Broker | Simple flows, max responsiveness, high decoupling | Need workflow control, error handling, restart |
| Mediator | Complex workflows, ACID-like guarantees, error recovery | Need max scalability — single mediator bottleneck |

**Async error handling (Workflow Event Pattern):**
1. Consumer delegates error to a *workflow processor* and moves on (preserves queue throughput)
2. Workflow processor repairs data and resubmits to original queue
3. If unrecoverable, send to "dashboard" queue for human review

**Don't:**
- Don't synchronously block the consumer on error — kills throughput.
- Don't ignore message order implications — re-submitted messages may arrive out of sequence; per-context queuing may be needed.

**Preventing data loss:**
- Use **persistent message queues** + **synchronous send** (Issue 1: producer → queue).
- Use **client acknowledge mode** — message stays in queue until consumer ACKs (Issue 2: consumer crash).
- Use **ACID DB transactions** + **last participant support** (Issue 3: queue → DB persistence).

**Hybrid event-driven:** use event-driven for most communication but allow **request-reply** for query-style operations (e.g., Bid History Service querying current bid). Hybrid is a valid topology.

*Ref: Fundamentals_of_Software_Architecture.md — "Event-Driven Architecture Style"*

---

### Space-Based Architecture

**Do:**
- Use when concurrent users > 10,000 and load is variable/unpredictable.
- Deploy the deployment manager to **scale processing units before** load spikes (pre-warm).
- Replicate cache asynchronously between processing units (typically <100 ms replication latency).
- Compute data collision rate: `CollisionRate = N * (UR²/S) * RL`. At >0.1%, replicated caching becomes infeasible.
- Use **distributed caching** for highly dynamic/inconsistent data (inventory counts); **replicated** for static reference data.
- Calculate replication latency in production — vendors rarely publish it.

**Don't:**
- Don't use replicated caching for cache sizes >100 MB or update rates that outpace replication.
- Don't use the near-cache model — front caches diverge, creating inconsistent performance per processing unit.
- Don't confuse partitioning type: space-based is BOTH domain AND technical partitioned.
- Don't expect high testability — simulating extreme loads is costly and usually done in production (high risk).

*Ref: Fundamentals_of_Software_Architecture.md — "Space-Based Architecture Style", "Data Collisions", "Replicated Versus Distributed Caching"*

---

### Service-Oriented Architecture (Classic / Orchestration-Driven)

**Do:**
- Recognize this style as historical context — avoid building new systems this way.
- Learn from its lessons: the **reuse-vs-coupling** trap, the technical-partitioning sprawl that ground domains like *CatalogCheckout* "to dust".

**Don't:**
- Don't consolidate everything into a canonical *Customer* service — the disability division doesn't need driver's-license fields, but the unified Customer service forces them.
- Don't rely on orchestration engines for transactional coordination — finding correct transaction granularity becomes unmanageable as services grow.
- Don't accept single-quantum coupling via a shared database *and* an orchestration engine — that's the worst of both worlds.

*Ref: Fundamentals_of_Software_Architecture.md — "Orchestration-Driven Service-Oriented Architecture"*

---

### Microservices Architecture

**Do:**
- Build each service as a **bounded context** with its own data — DDD's bounded context is the architectural primitive.
- Treat "microservice" as a **label, not a description** (Fowler). Capture a domain or workflow, not a tiny entity.
- Use three granularity signals: **purpose** (single significant behavior), **transactions** (boundaries where ACID needs would emerge), **choreography** (if services need heavy communication, bundle them back).
- Use **sidecars** for operational coupling (monitoring, logging, circuit breakers) — they enable service-mesh upgrades without code changes.
- Build **service meshes** via sidecar wiring for unified operational control.
- Use **choreography** (events) by default for loose coupling; use **orchestration** (mediator) for complex workflows.
- Apply **Backends for Frontends (BFF)** pattern for client-specific API translation.
- Use **synchronous by default, asynchronous when necessary**.

**Don't:**
- Don't do transactions across services — fix granularity instead.
- Don't overuse the saga pattern: "if transactions are the dominant feature, mistakes were made."
- Don't use the API layer as a mediator/orchestrator — it violates bounded context.
- Don't be afraid to enforce heterogeneity — different stacks per team prevent accidental coupling.
- Don't expect high performance out of the box — too much orchestration, too aggressive data separation, and security checks at every endpoint all hurt throughput.
- Don't do transactions across services — use sagas only when truly necessary.

**Saga pattern (use sparingly):**
- Implement *do/undo* operations per service (undo is often 2× the complexity of do)
- OR use **compensating transactions** — mediator tracks success/failure, sends undo requests on partial failure

*Ref: Fundamentals_of_Software_Architecture.md — "Microservices Architecture"*

---

### Monolithic vs Distributed Architectures — 8 Fallacies of Distributed Computing

**Do:**
- Treat the fallacies as design constraints, not warnings:
  1. **Network is reliable** → add timeouts, circuit breakers, retries, idempotency
  2. **Latency is zero** → measure 95th–99th percentile, not average; chained calls compound (10 calls × 100ms = 1s)
  3. **Bandwidth is infinite** → avoid stamp coupling (sending 500KB for 200B of needed data)
  4. **Network is secure** → secure every endpoint; threat surface grows by magnitudes
  5. **Topology never changes** → stay in constant communication with network admins
  6. **Only one administrator** → expect dozens of admins; coordination is non-trivial
  7. **Transport cost is zero** → budget for additional hardware, subnets, proxies
  8. **Network is homogeneous** → heterogeneous vendors introduce packet loss

**Resolve stamp coupling:**
- Create private RESTful API endpoints
- Use field selectors in contracts
- Use GraphQL
- Use consumer-driven contracts (CDCs)
- Use internal messaging endpoints

**Distributed-specific concerns to plan for:**
- **Distributed logging** — use Splunk or similar to consolidate
- **Distributed transactions** — use **transactional sagas** (event sourcing for compensation or finite-state machines) or **BASE transactions** (Basic availability, Soft state, Eventual consistency)
- **Contract maintenance and versioning** — establish deprecation strategy

*Ref: Fundamentals_of_Software_Architecture.md — "Monolithic Versus Distributed Architectures", "Fallacy #1" through "Fallacy #8", "Other Distributed Considerations"*

---

### Diagramming & Communication

**Do:**
- Practice **representational consistency** — always show where the current view sits in the larger architecture before drilling in.
- Build diagrams on **whiteboards / tablets** early, formalize later — avoid *Irrational Artifact Attachment*.
- Use the **C4 model** (Context, Container, Component, Class) as a default — Simon Brown's modern replacement for UML.
- Use **UML class and sequence diagrams** for structure and workflow; other UML types have fallen into disuse.
- Consider **ArchiMate** for enterprise-architecture modeling — "as small as possible" lightweight notation.
- Follow diagram guidelines: clear titles, consistent shapes, legend included, monochrome with color only to distinguish important artifacts.
- Use **solid lines for synchronous, dotted lines for asynchronous** — the only widespread convention.

**Don't:**
- Don't overuse color; monochrome with selective color reads better in print.
- Don't skip labels or keys; ambiguous diagrams cause misinterpretation, which is worse than no diagram.
- Don't commit to UML outside mandated contexts — UML failed outside committee-mandated organizations.

**When presenting:**
- Manipulate **time** via transitions and animations; hide slide boundaries with dissolve; use a distinct transition between thoughts.
- Use **incremental builds** rather than bullet-riddled corpse slides; maintain suspense, build gradually.
- Insert a **blank black slide** (invisibility pattern) to refocus attention on the speaker.
- Treat presentations as **half the story** — slides are for the visual channel, the speaker owns the verbal channel.
- Distinguish **infodecks** (read at the reader's pace, comprehensive) from **presentations** (presented at speaker's pace, slides are half).

*Ref: Fundamentals_of_Software_Architecture.md — "Diagramming and Presenting Architecture", "Diagramming Standards: UML, C4, and ArchiMate", "Presenting"*

---

### Team Effectiveness & Elastic Leadership

**Do:**
- Apply the 5 control factors to determine arm-chair vs control-freak stance:

| Factor | More control (+20) | Less control (−20) |
|---|---|---|
| Team familiarity | New team members | Know each other well |
| Team size | Large (>12) | Small (≤4) |
| Overall experience | Mostly junior | All experienced |
| Project complexity | Highly complex | Relatively simple |
| Project duration | Long (2 years) | Short (2 months) |

- Recognize the three team-size warning signs:
  - **Process loss** (Brooks's law) — frequent merge conflicts, lack of parallel work streams
  - **Pluralistic ignorance** — silent agreement masking dissent; watch facial expressions
  - **Diffusion of responsibility** — confusion about who owns what; things get dropped
- Use the **Hawthorne effect** to enforce checklist usage (announce spot-checks; verify occasionally).
- Sit **with** the team, not in a separate cubicle.

**Don't:**
- Don't write pseudocode for developers — that's design theft, not architecture.
- Don't restrict the use of open-source libraries without justification; ask developers to provide both technical and business justification.
- Don't write a checklist of **procedurally dependent tasks** (e.g., "verify table once created" requires "submit request form" first) — checklists are for non-ordered, error-prone steps.
- Don't make every process a checklist — diminishing returns sets in fast.

**Effective checklists (when checklists help):**
- **Developer Code Completion Checklist** — definition of done
- **Unit and Functional Testing Checklist** — edge cases developers forget
- **Software Release Checklist** — deployment failure root-causes added after each incident

**Don't:**
- Don't state the obvious? Yes, do — *"the obvious stuff is usually what's missed"* (Gawande).

*Ref: Fundamentals_of_Software_Architecture.md — "Making Teams Effective", "Architect Personalities", "How Much Control?", "Team Warning Signs", "Leveraging Checklists"*

---

### Negotiation & Leadership Skills

**Do:**
- Use these negotiation techniques with stakeholders:
  - **Leverage grammar** ("lightning fast", "yesterday") to surface real concerns
  - **Gather info before negotiating** (e.g., five nines = 5 min 35 sec/year downtime — translate nines to hours/minutes)
  - **Save cost/time arguments for last** — other justifications matter more
  - **Divide and conquer** — does the *entire system* need five nines, or only the order-placement path?
- With developers:
  - **Provide justification, not dictation**: *"Since change control is most important to us, all calls go through the business layer"* — not *"You must go through the business layer"*
  - **Have the developer arrive at the solution on their own** — set up the criterion, let them reach the conclusion
- With other architects:
  - **Demonstration defeats discussion** — build a POC rather than argue
  - **Avoid personal arguments** — pause and resume when calm

**Don't:**
- Don't say "you must" or "you need to" — use grammar that turns demands into collaborative statements.
- Don't dictate from the **Ivory Tower** — earn respect through collaboration.
- Don't expect hugs to substitute for handshakes in professional settings.

**4 C's of Architecture:**
- **Communication** — clear, concise
- **Collaboration** — work with, not above
- **Clarity** — make decisions and rationale clear
- **Conciseness** — avoid accidental complexity

**Be pragmatic, yet visionary** — apply practical constraints (budget, time, team skill, trade-offs, technical limits) to strategic thinking.

*Ref: Fundamentals_of_Software_Architecture.md — "Negotiation and Facilitation", "Negotiating with Business Stakeholders", "Negotiating with Other Architects", "Negotiating with Developers", "The Software Architect as a Leader", "The 4 C's of Architecture", "Be Pragmatic, Yet Visionary"*

---

### Managing Meetings

**Do:**
- When invited to a meeting, ask **why you're needed** and review the **agenda** before accepting.
- **Take one for the team** — substitute for tech leads in meetings to keep developers in flow state.
- When calling a meeting, ask *"Is this more important than the work I'm pulling them away from?"* — often an email suffices.
- Schedule meetings **first thing in the morning, right after lunch, or toward end of day** — avoid disrupting developer flow.

**Don't:**
- Don't schedule meetings mid-day during peak flow time.
- Don't accept meeting invites reflexively — qualify them.
- Don't allow your calendar to become a wall-to-wall meeting grid (Figure 23-4 anti-pattern).

*Ref: Fundamentals_of_Software_Architecture.md — "Integrating with the Development Team"*

---

### Evolutionary Architecture & Fitness Functions

**Do:**
- Treat architecture as supporting **incremental change** — microservices was designed for evolutionary change; legacy monoliths weren't.
- Build architectures that pair with **Agile engineering practices** (CI, CD, automated provisioning, chaos engineering).
- Use **fitness functions** to protect architectural characteristics as the system evolves (the central insight of *Building Evolutionary Architectures*).
- Recognize the **symbiotic relationship** between architecture style and engineering practices — microservices without automation fails.
- Migrate monoliths using the **Strangler Pattern** and **feature toggles** — Agile supports restructuring better than waterfall.

**Don't:**
- Don't design architecture assuming known unknowns are the only unknowns — unknown unknowns always appear.
- Don't ignore the engineering-practices requirement when choosing a distributed style.
- Don't couple architecture decisions to obsolete axioms — question them (the "Invalidating Axioms" preface).

*Ref: Fundamentals_of_Software_Architecture.md — "Engineering Practices", "The Path from Extreme Programming to Continuous Delivery", "Process", "History: Pets.com"*

---

### Architecture for Agility

**Do:**
- Drive **agility = testability + deployability** — never forget one ingredient.
- Apply **modularity and isolation** at the architecture level when ease of deployment and testability are priorities.
- Use **evolutionary architecture** principles: change is a first-class design consideration (microservices).
- Recognize Agile's iterative loop favors **just-in-time architecture decisions** rather than Big Design Up Front.

**Don't:**
- Don't equate agility with time-to-market alone — without testability and deployability, agility collapses.
- Don't build monoliths using waterfall — Agile's tight feedback loop fits architecture iteration better.
- Don't design for "easy to change" without committing to the engineering practices that make change cheap.

*Ref: Fundamentals_of_Software_Architecture.md — "Process", "Engineering Practices", "Expectations of an Architect"*

---

### Architect Career Development & Personal Radar

**Do:**
- Apply the **20-Minute Rule** — spend 20 minutes/day learning something new *before* checking email, *after* morning coffee. Breadth over depth.
- Maintain a **Personal Technology Radar** with 4 quadrants (Tools, Languages & Frameworks, Techniques, Platforms) and 4 rings (Hold, Assess, Trial, Adopt).
- Diversify your technology portfolio like a financial portfolio.
- Leverage social media's **weak links** — your next opportunity comes from people outside your strong-link circle.
- Practice architecture via **architecture katas** (Ted Neward / Neal Ford / Mark Richards) — small teams, 45-minute design, peer review.
- Be skeptical of **technology bubbles** — including your own.

**Don't:**
- Don't schedule 20-minute learning at lunch or evening — life intervenes; morning-before-email is the only reliable slot.
- Don't adopt a laissez-faire attitude to technology selection — formalize it via the radar.
- Don't live inside a vendor memetic bubble — challenge it before collapse.
- Don't search for an "answer key" to architecture katas — there are no right answers, only trade-offs.

*Ref: Fundamentals_of_Software_Architecture.md — "Developing a Career Path", "The 20-Minute Rule", "Developing a Personal Radar", "The ThoughtWorks Technology Radar", "Using Social Media", "Parting Words of Advice"*

---

### Architecture Partitioning — Technical vs Domain

**Principle:** Top-level partitioning decision drives the rest of the architecture. The two fundamental approaches are **technical partitioning** (presentation/business/persistence) and **domain partitioning** (workflows/bounded contexts).

**Do:**
- Choose **technical** when:
  - User stories are small, simple CRUD operations
  - Domain is small, well understood
  - Limited business-domain expertise on team
  - No clear domain boundaries yet
- Choose **domain** when:
  - Workflows span technical layers (e.g., "Place Bid" → DB → Web Service → messaging)
  - Domain is complex
  - Business domain expertise exists
  - Workflows are the primary unit of change
- For microservices, **always** use domain partitioning — Conway's law says otherwise.

**Don't:**
- Don't use technical partitioning for complex domains — you'll end up with a tightly coupled "modular monolith" where every change touches every layer.
- Don't use domain partitioning for trivial domains — over-engineering.
- Don't forget technical partitioning traps: in a layered architecture, even an order (with workflow) crosses all layers; teams must coordinate.

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Partitioning"*

---

### Component Granularity — Finding the Sweet Spot

**Principle:** Component granularity drives coupling/cohesion trade-offs. Too fine → excessive inter-component communication. Too coarse → high internal coupling, poor deployability.

**Do:**
- Start **coarse-grained** — easier to split than merge.
- Look for **accidental coupling** (shared utility classes binding unrelated functionality) — use LCOM to detect.
- Look for **transaction boundaries** as granularity hints — components that always participate in the same transaction should be one component.
- Look for **deployment units** as granularity hints — independently deployable → independent component.

**Don't:**
- Don't make components mirror database tables (entity trap).
- Don't merge components just because they share a database — shared DB ≠ same component.
- Don't split components simply because they're large — measure coupling first.

*Ref: Fundamentals_of_Software_Architecture.md — "Component Granularity", "Component Design"*

---

### Discovering Components — Techniques

**Do:**
- **Actor/Actions approach:** Identify the actors (users, systems) and the actions they perform; group related actions into components.
- **Event Storming:** Workshop where domain experts walk through business events; group events by lifecycle phase → components.
- **Workflow approach:** Identify workflows (sets of actions producing an observable result); each workflow is a candidate component.
- **Naked Objects pattern:** Build pure CRUD UIs exposing domain objects; component boundaries emerge from object clusters.

**Don't:**
- Don't use the entity trap (one component per table).
- Don't rely solely on user stories — they underrepresent cross-cutting concerns.
- Don't skip the iteration step — initial discovery is rarely right.

*Ref: Fundamentals_of_Software_Architecture.md — "Discovering Components"*

---

### Case Study: Silicon Sandwiches (Monolith)

**Context:** Online sandwich-ordering startup. Tight budget, time-to-market critical. Limited staff.

**Architecture choices:**
- **Style:** Layered monolith (no distributed concerns needed initially)
- **Quantum:** Single (shared DB, single deploy unit)
- **Domain:** Simple CRUD workflows; technical partitioning chosen
- **Characteristics:** Time-to-market (agility), simple workflows

**Lessons:**
- Modular monolith is a valid start — distributed comes later if characteristics demand it.
- Don't over-engineer for future scale you may never need.
- The "least worst architecture" principle: optimize for current characteristics, not theoretical future ones.

*Ref: Fundamentals_of_Software_Architecture.md — "Case Study: Silicon Sandwiches", "Case Study: Silicon Sandwiches: Partitioning"*

---

### Case Study: Going, Going, Gone (Online Auction)

**Context:** Online auction platform with high concurrency (10,000+ bidders), high data volume, complex event workflows.

**Architecture choices:**
- **Style:** Event-driven (asynchronous auction events) with hybrid request-reply for queries
- **Quantum:** Multiple — Bid Capture, Bid Streamer, Bidder Tracker, Online Auction API each have different characteristics
- **Broker topology:** For high-throughput fan-out of bid events
- **Asynchronous pub/sub:** Between Bid Capture, Bid Streamer, Bidder Tracker (see ADR 76)
- **Mediator (jBPM):** For complex multi-step auction workflows

**Lessons:**
- High concurrency + variable load + complex workflows = event-driven is the natural fit.
- ADR captured the "Why" — even a decade later, the architect can re-evaluate the decision without losing context.
- Asynchronous-first design forces decoupling; new event consumers (analytics, fraud detection) added without touching producers.

*Ref: Fundamentals_of_Software_Architecture.md — "Case Study: Going, Going, Gone", "Architecture Quantum Redux"*

---

### Architectural Significant Requirements (ASRs)

**Principle:** Not all requirements are architecturally significant. Identify which ones *actually* influence structure.

**ASRs:**
- Affect structure (component boundaries, communication patterns)
- Influence cross-cutting concerns (security, observability)
- Constrain technology choice (performance SLAs dictate DB type)
- Drive deployment topology (multi-region for availability)

**Non-ASRs (don't architect around these):**
- Pure business logic that lives inside one component
- UI-level changes
- Cosmetic requirements
- One-off user preferences

**Do:**
- Tag ASRs explicitly in the requirements backlog.
- Track ASRs through their lifecycle (proposed → accepted → deprecated).

**Don't:**
- Don't treat every requirement as architecturally significant — designer overreach.
- Don't assume an ASR stays ASR forever — context changes.

*Ref: Fundamentals_of_Software_Architecture.md — "Architecturally Significant"*

---

### API Design & Layered Contracts

**Principle:** APIs define architectural boundaries. They must be designed with the same care as components and services. Three foundational concerns: **discovery** (URI structure), **contract** (verbs, payloads), **evolution** (versioning, deprecation).

**Do:**
- Use **resource-oriented URIs** (`/customers/123/orders`) with HTTP verbs carrying semantics (`POST` = create, `GET` = read, `PUT` = replace, `PATCH` = partial update, `DELETE` = remove).
- Prefer **`/resource/collection/{id}/sub-resource/{subId}`** for hierarchy over query parameters.
- Use **plural nouns** (`/orders`, not `/order`).
- Return **whole resource** on GET; use **PATCH** for partial updates (PUT replaces entire representation).
- Apply the **Postel's Law** for APIs: *be liberal in what you accept, conservative in what you send*.
- Version APIs at the URI (`/v1/orders`) or via header (`Accept: application/vnd.company.orders.v2+json`).
- Document with **OpenAPI 3.0** (formerly Swagger) — generates client SDKs, validates payloads.
- Use **idempotency keys** for state-mutating endpoints (POST/PUT/DELETE).
- Paginate with **cursor-based** pagination (stable across insertions) over offset (unstable).
- Specify **content negotiation** (`Accept`, `Content-Type`).
- Implement **ETag** for optimistic concurrency control on updates.

**Don't:**
- Don't expose **verbs in URIs** (`/createOrder`) — use HTTP verbs.
- Don't return **stack traces** or internal error details to clients.
- Don't use **different field names for the same concept** across endpoints.
- Don't break the API contract on minor version bumps (use major versions).
- Don't expose **stamps** (entire objects) when only a subset is needed (returns 500KB to deliver 200B).
- Don't build **chatty APIs** (multiple round-trips for one logical operation).
- Don't return **mixed-case JSON** (snake_case vs camelCase) inconsistently.

**Stamp coupling remediation:**
- **Field selectors** in contracts (`GET /orders?fields=id,total`)
- **GraphQL** (client specifies needed fields)
- **Private RESTful endpoints** (dedicated fine-grained resource)
- **Consumer-Driven Contracts (CDCs)** (provider only returns what consumer needs)
- **Internal messaging endpoints** (instead of HTTP APIs)

*Ref: Fundamentals_of_Software_Architecture.md — "Foundations" of API design, Microservices API Layer, Distributed Considerations*

---

### Distributed Transactions & Sagas

**Principle:** ACID transactions don't span services. Use sags for eventual consistency across services. Sagas = a sequence of local transactions coordinated via events.

**Saga types:**
- **Choreography:** Each service emits events; next service subscribes. Decentralized, eventually consistent.
- **Orchestration:** A central orchestrator (mediator) coordinates the saga steps. Easier to monitor but adds a coordinator service.

**Do:**
- Use **compensating transactions** — every forward action has an undo action (cancel order → restore inventory).
- Design compensations to be **idempotent** — they may be retried.
- Track saga state via **correlation IDs** flowing through events.
- Build a **saga timeout** — if a step doesn't complete in N seconds, invoke compensation.
- Make saga definitions **declarative** when possible (jBPM, Camunda).
- Document saga flows in ADRs — they're load-bearing decisions.

**Don't:**
- Don't use sags for trivial workflows — they add complexity for limited benefit.
- Don't put **long-running sagas** (hours/days) in core request paths — human-in-the-loop needed.
- Don't assume saga guarantees **atomic visibility** — observers see intermediate states.
- Don't forget **orphan management** — handle cases where compensation never executes (use a sweeper job).

**Trade-off:** "If transactions are the dominant feature, mistakes were made" (Ford/Richards) — usually the granularity is wrong; merge services.

*Ref: Fundamentals_of_Software_Architecture.md — "Transactions and Sagas", Microservices*

---

### Component Identification Techniques (Detailed)

**Principle:** Component discovery is one of the hardest architectural tasks. Multiple techniques exist; use them in combination.

**1. Actor/Actions approach:**
- Identify **actors** (users, external systems, time).
- For each actor, identify **actions** (verb-noun phrases).
- Group related actions into **use cases** (or stories).
- Use cases → components (each component serves a coherent set of use cases).

**2. Event Storming (Alberto Brandolini):**
- Workshop with domain experts.
- Use sticky notes for **domain events** (orange), **commands** (blue), **aggregates** (yellow), **policies** (purple), **read models** (green).
- Walk through a business scenario temporally.
- Group events by **lifecycle phase** → components.
- Identify **swim lanes** (parallel business processes) → potential bounded contexts.

**3. Workflow approach:**
- Identify **workflows** = sets of actions producing an observable result.
- Each workflow → candidate component.
- Workflows that share actions → share a component.
- Workflows that are independent → separate components.

**4. Naked Objects pattern:**
- Build pure CRUD UIs exposing domain objects.
- Object clusters → component boundaries.
- Best for simple CRUD domains only.

**5. Class responsibility collaboration (CRC) cards:**
- Brainstorm **classes** with **responsibilities** and **collaborators**.
- Group classes by **strong collaboration** → components.

**Do:**
- Use **multiple techniques** on the same problem; compare results.
- Iterate: **identify → analyze roles → analyze characteristics → restructure**.
- Include **domain experts** (not just architects/developers).
- Focus on **business capabilities** (not technical components).

**Don't:**
- Don't use a single technique exclusively — each has blind spots.
- Don't skip the iteration loop — first pass is rarely right.
- Don't use technical partitioning as a starting point for microservices.

*Ref: Fundamentals_of_Software_Architecture.md — "Discovering Components", "Actor/Actions approach", "Event storming", "Workflow approach"*

---

### C4 Model (Simon Brown)

**Principle:** C4 is a hierarchical diagramming approach with 4 levels: Context, Container, Component, Code. Each level zooms in on one aspect.

**Levels:**
1. **Level 1: System Context** — shows the system as a black box in its environment; users and external systems; what does the system do?
2. **Level 2: Containers** — applications, databases, file systems, message brokers; how is it deployed?
3. **Level 3: Components** — major structural building blocks inside each container (controllers, services, repositories); how is each container built?
4. **Level 4: Code** (optional) — class diagrams, ER diagrams for the most important components; how is each component implemented?

**Do:**
- Start with **Level 1**; only add detail that aids the conversation.
- Use **consistent notation** (boxes for processes, cylinders for data stores, parallelograms for external systems).
- Label **every element** (no "?").
- Include **technology choices** in container diagrams (`Spring Boot`, `PostgreSQL`).
- Use a **legend** with shapes/symbols.
- Use **colors sparingly** (one or two for emphasis only).
- Annotate **technology and purpose** (e.g., "Spring Boot REST API — handles customer CRUD").

**Don't:**
- Don't draw all four levels for every diagram — most meetings need 1-2 levels.
- Don't use UML symbols (C4 is deliberately UML-free).
- Don't combine levels in one diagram — purpose is lost.
- Don't ignore context — always show where the current view fits.

**Tooling:** Structurizr (DSL + rendering), draw.io with C4 plugin, PlantUML with C4-PlantUML.

*Ref: Fundamentals_of_Software_Architecture.md — "Diagramming Standards: UML, C4, and ArchiMate"*

---

### Microservices Granularity — Three Signals

**Principle:** "Microservice" is a label, not a description. Use three signals to determine if you've got the granularity right.

**Signal 1: Purpose (single significant behavior)**
- A microservice captures a **domain** or **workflow**, not a tiny entity.
- Test: can you explain the service's purpose in one sentence without using "and"? If not, split or merge.

**Signal 2: Transactions (where ACID would naturally live)**
- A microservice should not span what would naturally be a single ACID transaction.
- Test: if your service participates in many distributed transactions, you probably split too fine.

**Signal 3: Choreography (if services communicate heavily, merge)**
- A microservice should be loosely coupled.
- Test: if removing/changing one service requires touching many others, merge them.

**Do:**
- Use the **Rule of Three** — if you've built the same kind of service three times with different code, it's a candidate to extract.
- Use the **Rule of One** — one service = one bounded context (DDD).
- Allow services to **grow** until they violate one of the three signals — then split.

**Don't:**
- Don't use team size as the granularity signal — two-pizza teams don't make two-pizza services.
- Don't use technology as the granularity signal — "everything Java" or "everything Python" doesn't define a service boundary.
- Don't start with microservices — start with a modular monolith, extract services as needed.

*Ref: Fundamentals_of_Software_Architecture.md — "Microservices Architecture", "Granularity"*

---

### Service Mesh & Sidecar Pattern

**Principle:** A service mesh decouples **business logic** (your code) from **operational concerns** (observability, traffic management, security). Each service has a **sidecar proxy** that handles cross-cutting traffic concerns.

**Do:**
- Use a service mesh when you have:
  - Many services (typically >10) requiring consistent observability, security, traffic management
  - Multi-language environment (mesh language-agnostic)
  - Operational complexity that grows non-linearly with service count
- Choose a mesh based on **operational maturity** (Istio = full-featured but complex; Linkerd = simpler; Consul Connect = HashiCorp-native).
- Migrate incrementally — not all services need mesh from day one.

**Don't:**
- Don't adopt a service mesh for <10 services — operational overhead exceeds value.
- Don't put **business logic** in sidecars — they're for operational concerns only.
- Don't run mesh without **observability** (you can't debug what you can't see).

**Trade-off:** Service mesh adds **latency** (sidecar hop), **complexity** (control plane), and **resource usage** (one proxy per service). Justified at scale; over-engineered at small scale.

*Ref: Fundamentals_of_Software_Architecture.md — "Operational Reuse", "Sidecars"*

---

### Choreography vs Orchestration

**Principle:** Two patterns for coordinating services. Choose by complexity.

**Choreography:**
- Each service emits **events**; others react.
- No central coordinator.
- Decentralized, eventually consistent.
- Best for: simple workflows, high decoupling, scale-out.

**Orchestration:**
- A **central orchestrator** (mediator) calls each service in sequence.
- Centralized control, easier to monitor.
- Best for: complex workflows, error handling, ACID-like guarantees.

**Do:**
- Use **choreography by default** — simpler, more decoupled.
- Use **orchestration** when:
  - Workflow complexity justifies central coordination
  - You need explicit retry/cancel semantics
  - Step ordering matters (and is hard to enforce via event chains)
- Apply **Saga pattern** when using choreography for long-running transactions.
- Document **workflow diagrams** for orchestration — complex flows are hard to remember.

**Don't:**
- Don't use orchestration for trivial workflows (over-engineering).
- Don't use choreography for tightly-coupled workflows (causality becomes impossible to reason about).
- Don't expect choreography to provide **strong consistency** — it's inherently eventual.
- Don't tightly couple orchestrators to service implementations.

*Ref: Fundamentals_of_Software_Architecture.md — "Choreography and Orchestration", "Event-Driven Architecture"*

---

### Observability & Telemetry

**Principle:** You can't manage what you can't measure. Observability = the ability to ask arbitrary questions about your system from its outputs.

**Three pillars:**
- **Metrics:** Numeric time-series (request rate, error rate, latency percentiles).
- **Logs:** Discrete events with context (errors, state changes).
- **Traces:** Causal chains of operations across services (request → service A → service B → DB).

**Do:**
- Instrument code with **OpenTelemetry** (CNCF standard, vendor-neutral).
- Adopt **RED method** (Rate, Errors, Duration) for services — gives the right SLOs.
- Adopt **USE method** (Utilization, Saturation, Errors) for resources — finds bottlenecks.
- Track **percentiles**, not averages (P50, P95, P99) — averages hide the long tail.
- Use **distributed tracing** (Jaeger, Zipkin, Tempo) for microservice architectures.
- Centralize logs (ELK, Loki, CloudWatch) — local logs in 50 services are useless.
- Set alerts on **symptoms** (latency, errors), not **causes** (CPU, memory) — symptoms drive user pain.
- Use **structured logging** (JSON) — parseable, queryable, context-rich.

**Don't:**
- Don't log **PII** (names, emails, credit cards) — log IDs only.
- Don't rely on **log-based metrics** — use proper metrics systems.
- Don't sample traces blindly — head-based sampling misses errors; use tail-based.
- Don't over-instrument — every span costs latency and storage.
- Don't use averages for SLOs — they hide the failures users care about.

*Ref: Fundamentals_of_Software_Architecture.md — "Operational Measures", "Engineering Practices", "Process"*

---

### Capacity Planning & Performance Engineering

**Principle:** Capacity planning answers: "Do we have enough resources for expected load?" Performance engineering answers: "Can we make this faster with the resources we have?"

**Capacity planning process:**
1. **Profile current load** — request rate, data volume, peak times.
2. **Project future load** — apply growth multipliers (1.5×, 2×, 10×).
3. **Model resource needs** — CPU cores, memory, storage, network.
4. **Provision for headroom** — 60–70% utilization target (not 100%).
5. **Test under load** — load tests at, above, and below design point.
6. **Re-plan regularly** — capacity needs shift.

**Do:**
- Measure **percentiles** (P95, P99) for response time.
- Identify **long-tail latency** — outliers at 10× average will kill users.
- Use **load tests** to validate design (not just smoke tests).
- Plan for **3× the expected peak** — peaks are unpredictable.
- Monitor **saturation** (queue depth, thread pool utilization) — that's what fails first.
- Use **statistical models** (prediction intervals) for scaling decisions, not arbitrary thresholds.
- Document **capacity assumptions** in ADRs — context for future architects.

**Don't:**
- Don't optimize for the **average** — long-tail requests starve workers.
- Don't size for **current peak** — peak will grow.
- Don't skip load testing — "it works" is not "it scales."
- Don't ignore **downstream dependencies** (DB, message broker, third-party APIs).

*Ref: Fundamentals_of_Software_Architecture.md — "Operational Measures", "Capacity"*

---

### Resilience Patterns — Circuit Breaker, Bulkhead, Timeout

**Principle:** Distributed systems fail. The question isn't *if* but *when*. Apply resilience patterns to **fail fast** and **isolate failures**.

**1. Timeout:**
- Every remote call needs a **timeout** — without it, slow services tie up threads forever.
- Tune timeout to **P99 + buffer** — anything beyond that is nearly certain to fail.
- Use **cascading timeouts** — service A's timeout > service B's timeout > DB timeout.

**2. Circuit breaker:**
- Track **failure rate** over a window (e.g., 25% errors in 5 seconds).
- When threshold exceeded → **open circuit** (fail fast without calling the dependent service).
- After cooldown → **half-open** (allow one test request).
- If test succeeds → **close circuit** (resume normal).
- If test fails → **re-open**.

**3. Bulkhead:**
- Isolate resources per dependency (separate thread pools per external service).
- Failure of one dependency can't exhaust resources for another.
- Configurable: max concurrent calls, max wait duration.

**4. Retry with exponential backoff:**
- Transient failures often self-heal — retry.
- **Exponential backoff** (1s, 2s, 4s, 8s) avoids stampeding a recovering service.
- Add **jitter** (±20%) to avoid synchronized retry storms.
- Set **max retries** — don't retry forever.

**5. Fallback:**
- Provide **degraded behavior** (cached value, default response) when dependency fails.
- Read-heavy services often use cache fallback.

**Do:**
- Apply **all three together** (timeouts + circuit breakers + bulkheads) — they reinforce each other.
- Make circuit breaker **state visible** — emit metrics, alerts on state changes.
- Use **libraries** (Resilience4j, Polly, Hystrix) rather than rolling your own.
- Treat **dependencies asymmetrically** — critical paths have stricter timeouts.

**Don't:**
- Don't apply these only to "external" services — internal services fail too.
- Don't retry non-idempotent operations without an idempotency key.
- Don't open the circuit for "rare" events — failure rate must exceed a threshold.
- Don't set circuit-breaker thresholds based on a single incident — calibrate empirically.

```python
# Pseudocode for combined resilience
@circuit_breaker(failure_threshold=0.25, window_seconds=10)
@bulkhead(max_concurrent=150)
@retry(max_attempts=3, backoff=exponential(base=1, jitter=0.2))
@timeout(seconds=2)
def call_dependency(request):
    return dependent_service.call(request)
```

*Ref: Fundamentals_of_Software_Architecture.md — "Resilience", "Engineering Practices", Microservices Cascading Failure*

---

### Caching Patterns

**Principle:** Cache reads scale; cache correctness is hard. Three primary caching patterns.

**1. Cache-aside (lazy loading):**
- Application checks cache → on miss, queries DB → populates cache → returns.
- Most flexible; resilient to cache failure (cache miss = slow, not broken).
- Invalidation is the application's responsibility.

**2. Read-through:**
- Cache itself loads from DB on miss.
- Application always reads from cache.
- Tighter coupling to cache library.

**3. Write-through:**
- Application writes through cache → cache writes to DB.
- Cache and DB always consistent.
- Higher write latency.

**4. Write-behind (write-back):**
- Application writes to cache → cache asynchronously writes to DB.
- Lowest write latency.
- Risk of data loss if cache fails before async write.

**Do:**
- Set **TTL** on every cache entry — guarantees eventual freshness.
- Implement **cache invalidation** for write-heavy data — TTL alone is too slow.
- Use **LRU/LFU** eviction policies; size cache appropriately.
- Monitor **hit ratio** — <80% means cache is poorly tuned.
- Use **cache-aside** by default — most flexible.
- Store **whole objects** (avoid partial-object caching).
- Use **namespacing** in cache keys (`user:123`, `order:456`).

**Don't:**
- Don't cache **transient data** (one-off calculations, error responses).
- Don't cache **PII** without encryption — caches are often less protected than DBs.
- Don't rely on cache freshness for **correctness** — assume staleness.
- Don't use **cache-aside** without TTL — stale data lives forever.
- Don't cache **large objects** (>1 MB) — memory pressure; consider compression.

*Ref: Fundamentals_of_Software_Architecture.md — "Distributed Caching", "Performance"*

---

### Event Sourcing & CQRS

**Principle:** Event sourcing stores state as a sequence of events rather than current state. CQRS (Command Query Responsibility Segregation) separates read and write models.

**Event sourcing:**
- Persist **events** (CustomerCreated, OrderPlaced, OrderShipped).
- **State** = function(events) — replay events to reconstruct state.
- Events are **immutable** (append-only log).
- Built-in audit trail; supports temporal queries (state at time T).
- Enables **event replay** to fix bugs or populate new read models.

**CQRS:**
- **Write side:** Commands → write model (often event-sourced).
- **Read side:** Queries → read model (denormalized views).
- Read and write models can be **different stores** (write: event store; read: SQL/NoSQL).
- Eventually consistent.

**Do:**
- Use event sourcing when **audit history matters** (finance, compliance, regulated domains).
- Pair event sourcing with **CQRS** when read and write access patterns differ.
- Use **snapshots** to avoid replaying millions of events.
- Design events as **immutable facts** ("OrderPlaced at 10:32 by user 123").
- Version your **event schema** — events must be readable forever.

**Don't:**
- Don't use event sourcing for simple CRUD — overkill.
- Don't expose **events as API** — they're internal representation.
- Don't lose events — durability is non-negotiable.
- Don't put read-model logic in the write side — they have different scaling needs.
- Don't assume event sourcing automatically gives you CQRS — they're complementary but independent.

*Ref: Fundamentals_of_Software_Architecture.md — "Choreography and Orchestration", Event Sourcing references in microservices*

---

### Backends for Frontends (BFF) Pattern

**Principle:** Different clients (mobile, web, partner API) have different needs. A single API forces compromises. BFF = one API per client type.

**Do:**
- Use BFF when:
  - Different clients need **different response shapes** (mobile wants summary; web wants details).
  - Different clients have **different performance constraints** (mobile wants compressed; web wants rich).
  - Different clients need **different auth** (mobile uses OAuth; partner uses API key).
- Deploy BFF as a **separate service** — not a shared library.
- Treat BFF as **client-owned** — frontend team maintains it.
- Use **API composition** in BFF to aggregate multiple backend calls.

**Don't:**
- Don't have a single API "supporting all clients" — leads to bloated payloads and complex auth.
- Don't put **business logic** in BFF — only client-specific translation/aggregation.
- Don't deploy BFF per developer — group by client type (web, mobile, partner).

*Ref: Fundamentals_of_Software_Architecture.md — "Frontends"*

---

### Hybrid Event-Driven Architecture

**Principle:** Pure event-driven loses request-reply semantics. Hybrid = event-driven for most communication + request-reply for query-style operations.

**Do:**
- Use event-driven for **state changes** (order placed, payment received).
- Use request-reply for **queries** (current bid amount, account balance).
- Use **request-reply eventing** pattern for query events:
  1. Query service sends a query event
  2. State-owning services respond with reply events
  3. Query service correlates responses
- Limit query-event scope to **bounded contexts** (don't query across all services).

**Don't:**
- Don't try to make all operations asynchronous — query semantics often need request-reply.
- Don't use query events for transactional updates — eventual consistency breaks invariants.
- Don't broadcast query events to all consumers — narrow the audience.

*Ref: Fundamentals_of_Software_Architecture.md — "Hybrid Event-Driven Architectures", "Choosing Between Request-Based and Event-Based"*

---

### Stamp Coupling & Field Selection

**Principle:** Returning more data than the client needs (stamp coupling) wastes bandwidth, increases latency, and exposes internal data unnecessarily.

**Do:**
- Use **field selectors** (`GET /orders?fields=id,total,status`).
- Use **sparse fieldsets** (`fields[orders]=id,name` for related resources).
- Use **GraphQL** for client-specified queries.
- Create **purpose-specific endpoints** (`/orders/summary` vs `/orders/details`).
- Use **Consumer-Driven Contracts** — providers only return what each consumer needs.
- Document **field semantics** — what each field means and when it changes.

**Don't:**
- Don't return whole database rows by default — model the response shape.
- Don't expose internal IDs that clients shouldn't see.
- Don't change field semantics without an API version bump.
- Don't add fields to responses "in case they're useful" — clients depend on what's documented.

*Ref: Fundamentals_of_Software_Architecture.md — "Fallacy #3: Bandwidth Is Infinite", Stamp Coupling*

---

### DevOps & Continuous Delivery for Architects

**Principle:** Architecture and operations are inseparable. Microservices without automation fails; CD without architectural discipline fails.

**CD Pipeline:**
1. **Commit** — code push triggers pipeline.
2. **Build** — compile, package.
3. **Unit tests** — fast feedback (<5 min).
4. **Static analysis** — linting, security scans.
5. **Integration tests** — test against dependencies.
6. **Performance tests** — load tests on representative data.
7. **Deploy to staging** — full integration environment.
8. **Acceptance tests** — business validation.
9. **Deploy to production** — blue/green, canary, or rolling.
10. **Monitor** — observability in production.

**Architect's role in CD:**
- Define **deployment topology** (how many environments, promotion path).
- Set **deployment budgets** (time, risk tolerance).
- Design for **deployability** (stateless services, schema migrations, backward compatibility).
- Specify **rollback strategy** (blue/green, feature flags, compensating migrations).
- Advocate for **infrastructure as code** (Terraform, CloudFormation, Pulumi).

**Do:**
- Adopt **continuous delivery** (deployment-ready code always) before **continuous deployment** (auto-deploy).
- Use **feature flags** for risk mitigation — decouple deploy from release.
- Implement **database migrations** as backward-compatible (add column → dual-write → migrate → drop column).
- Use **trunk-based development** — long-lived branches make integration painful.

**Don't:**
- Don't deploy on Friday — leave time for recovery before the weekend.
- Don't skip **smoke tests** in production — synthetic transactions verify deploys.
- Don't break **schema compatibility** — concurrent clients break.
- Don't rely on **manual deployment** — humans make mistakes.

*Ref: Fundamentals_of_Software_Architecture.md — "Engineering Practices", "Continuous Delivery", "DevOps"*

---

### Architecture Katas & Practice

**Principle:** Architectural judgment improves with deliberate practice. Architecture katas = structured exercises for improving design skills.

**Format:**
- **Team:** 3-6 architects/developers.
- **Duration:** 45 minutes (hard cap).
- **Problem:** Pre-defined scenario (often fictional, e.g., online auction for used cars).
- **Process:**
  1. Identify architecture characteristics (5 min).
  2. Sketch domain components (10 min).
  3. Choose architecture style (5 min).
  4. Define communication patterns (10 min).
  5. Sketch diagram (10 min).
  6. Present + peer review (5 min per team).

**Do:**
- Practice katas with **diverse teams** — different perspectives reveal different assumptions.
- Time-box strictly — architectural decisions under constraint mirror real-world pressure.
- Focus on **trade-offs**, not "right answers" — every decision has alternatives.
- Rotate facilitators — leadership shouldn't be the only person running katas.
- Use katas to **calibrate** architectural judgment across teams.
- Pick problems with **domain familiarity** and **technical unfamiliarity** (or vice versa).

**Don't:**
- Don't search for "the right answer" — there isn't one.
- Don't let the loudest voice dominate — explicitly invite dissent.
- Don't skip the time-box — endless katas teach nothing about constraint.
- Don't use kata problems that mirror your exact current work — too close to be instructive.

*Ref: Fundamentals_of_Software_Architecture.md — "Parting Words of Advice" (architecture katas reference)*

---

### Space-Based Architecture — Detailed Patterns

**Principle:** Space-based (a.k.a. tuple space, cloud architecture pattern) handles extreme concurrency by removing the database from the synchronous request path.

**Components:**
- **Processing Unit:** Application logic + in-memory data grid (IMDG) cache.
- **Virtualized Middleware:** Replaces the traditional database as the coordination layer.
- **Data Grid:** In-memory distributed cache (GemFire, Coherence, GigaSpaces).
- **Data Pumps:** Async readers/writers between data grid and persistent storage.
- **Deployment Manager:** Orchestrates processing unit scaling based on load.

**Do:**
- Use when **concurrent users > 10,000** AND **load is variable/unpredictable**.
- Replicate cache **asynchronously** between processing units (<100ms typical).
- Use **distributed caching** for dynamic/inconsistent data; **replicated** for static reference.
- Pre-warm processing units **before** load spikes.
- Use **data pumps** to persist to DB asynchronously.

**Don't:**
- Don't use replicated caching for cache sizes >100 MB — replication breaks.
- Don't use near-cache model — front caches diverge.
- Don't expect **strong consistency** — space-based is eventually consistent.
- Don't use space-based for systems with **complex transactional semantics**.
- Don't deploy space-based without **observability** — the in-memory nature hides state.

*Ref: Fundamentals_of_Software_Architecture.md — "Space-Based Architecture Style", "Processing Unit", "Virtualized Middleware", "Data Pumps"*

---

### Microservices Anti-Patterns to Avoid

**1. Entity Microservice:**
- Each entity = service → ORM-as-architecture.
- Result: chatty services, distributed joins.
- Fix: Bounded context per service, not entity per service.

**2. Distributed Monolith:**
- Services deployed independently but **coupled at release** (must deploy together).
- Result: you have all the downsides of microservices + all the downsides of monoliths.
- Fix: enforce data isolation; avoid shared libraries.

**3. Smart Endpoints, Dumb Pipes:**
- Pushing logic into ESBs/messaging (the SOA mistake).
- Result: business logic scattered, hard to change.
- Fix: Logic in services, messaging = transport only.

**4. Chatty Services:**
- Services call each other many times for one logical operation.
- Result: high latency, cascading failures.
- Fix: Aggregate data; merge services that chat.

**5. Shared Database:**
- Multiple services sharing one database.
- Result: tight coupling, can't deploy independently.
- Fix: One database per service.

**6. Shared Libraries for Domain Logic:**
- Domain logic in shared JARs across services.
- Result: must redeploy all services to change domain.
- Fix: Share via APIs / events, not libraries.

**7. Using ESBs / Orchestrators for Business Logic:**
- Orchestrators contain logic.
- Result: same as distributed monolith.
- Fix: Orchestrators coordinate; logic stays in services.

*Ref: Fundamentals_of_Software_Architecture.md — Microservices anti-patterns*

---

### Architecture in Agile Iterations

**Principle:** Architecture is iterative, not Big Design Up Front (BDUF). But not all architecture is "just-in-time" — some decisions must be made early (foundational) while others can wait (deferrable).

**Decision timing matrix:**
- **Decide early (foundational):** Architecture style, database technology, deployment topology, programming language.
- **Decide iteratively:** Component boundaries, API contracts, specific algorithms.
- **Defer as long as possible:** Internal class design, framework-specific patterns.

**Do:**
- Practice **Agile architecture** — make decisions when they have to be made, not before.
- Conduct architecture review at **iteration boundaries** (start + end of each).
- Use **architecture spikes** (POCs) to validate risky decisions before committing.
- Hold **just-in-time design sessions** when the team needs to know.
- Make **reversible decisions** easy to change; make **irreversible decisions** carefully.

**Don't:**
- Don't skip architecture decisions at the start — some are foundational.
- Don't make every decision at the start — over-engineering.
- Don't change foundational decisions casually — switching language mid-project is expensive.
- Don't hide architecture work — it must be visible to stakeholders.

*Ref: Fundamentals_of_Software_Architecture.md — "Process", "Engineering Practices", "Expectations of an Architect"*

---

### Conway's Law & Inverse Conway Maneuver — Deep Dive

**Principle:** Organizations design systems that mirror their communication structures. The Inverse Conway Maneuver deliberately restructures teams to produce the desired architecture.

**Three forms of Conway's Law:**

1. **Conway's Law (1968):** "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."
2. **Reverse Conway Maneuver (Jonny Leroy):** Change team structure first → architecture follows.
3. **Inverse Conway Maneuver (pragmatic variant):** Deliberately align team boundaries with desired architecture (regardless of which changed first).

**Do:**
- Audit team boundaries when planning architecture changes.
- Use **team topology** (Skelton & Pais) — stream-aligned, platform, enabling, complicated-subsystem teams.
- Match team count to **architectural seams** (each bounded context = one team).
- Co-locate teams with strong domain ownership.
- Document team-to-component mapping in the architecture diagram.

**Don't:**
- Don't fight Conway's Law — the system you build will mirror your org.
- Don't reorganize for the sake of reorganization — Conway alignment is the goal.
- Don't assume team boundaries are permanent — they should evolve with architecture.
- Don't ignore HR constraints — reorganizations have real costs.

**Team size warning signs:**
- **Process loss** — adding people doesn't add productivity (Brooks's law).
- **Pluralistic ignorance** — silent agreement masking dissent.
- **Diffusion of responsibility** — unclear ownership.

*Ref: Fundamentals_of_Software_Architecture.md — "Architecture Partitioning", "Conway's Law", "Making Teams Effective"*

---

### Architectural Katas — Reference Problems

**Principle:** Architecture katas give architects and developers a structured way to practice architectural judgment under time pressure.

**Sample kata topics:**
- Online auction for used cars (event-driven, high concurrency)
- Smart home device management (IoT, microservices)
- Hotel booking system (consistency, integration with external systems)
- Medical records system (compliance, security, audit)
- Real-time analytics dashboard (streaming, time-series)
- Social media platform (eventual consistency, fan-out)
- E-commerce platform (transactional + analytics)

**Process:**
1. **Read problem** (5 min) — requirements + characteristics.
2. **Identify characteristics** (10 min) — list top 5.
3. **Sketch domain components** (10 min) — main bounded contexts.
4. **Choose style** (5 min) — based on characteristics.
5. **Define communication** (10 min) — sync/async, topics, APIs.
6. **Sketch diagram** (10 min) — at least 2 levels of C4.
7. **Present** (5 min/team) — trade-offs + alternatives.

**Variation:** "Architecture tennis" — one person presents, another challenges.

*Ref: Fundamentals_of_Software_Architecture.md — architecture katas referenced*

---

### Architecture Reviews — Conducting Them

**Principle:** Architecture reviews are how teams align on the direction. Done well, they prevent costly mistakes. Done poorly, they become bureaucratic theater.

**Do:**
- Schedule reviews at **natural decision points** (start of major features, before irreversible changes).
- Use **agenda-driven reviews** — circulate materials 24h before.
- Time-box presentations — 30 min present, 30 min Q&A.
- Focus on **trade-offs** — what was considered, what was rejected, why.
- Include **non-architect reviewers** — developers, ops, security.
- Document outcomes as **ADRs** with action items.
- Make reviews **safe** — dissension is welcome; personal attacks are not.

**Don't:**
- Don't surprise the team with a review of completed work.
- Don't review trivia (variable naming) — focus on architecture.
- Don't let senior architects dominate — explicit time for junior voices.
- Don't end a review without **documented outcomes**.
- Don't skip post-implementation reviews — learn from deviations.

*Ref: Fundamentals_of_Software_Architecture.md — "Integrating with the Development Team", Negotiation chapters*

---

### Multi-Tenancy & SaaS Architecture

**Principle:** Multi-tenancy serves multiple customers (tenants) from one codebase. Trade-offs in **isolation** (security, performance) vs **density** (cost efficiency).

**Three multi-tenancy models:**

1. **Single-tenant (one DB per tenant):**
   - Strongest isolation; easiest to migrate out.
   - Lowest density (most expensive).

2. **Shared DB, separate schemas:**
   - Schema-level isolation; reasonable density.
   - Migrations are per-schema (operational complexity).

3. **Shared DB, shared schema, tenant ID column:**
   - Highest density; cheapest.
   - Highest risk: missing tenant_id in WHERE clause = data leak.
   - Requires row-level security at DB.

**Do:**
- Use **tenant ID** in every query, every log, every metric.
- Implement **row-level security** in the database when using shared schema.
- Use **shared services** with **per-tenant config** (feature flags, quotas).
- Apply **tenant-aware observability** — segment metrics/logs/traces by tenant.
- Design for **tenant migration** (out of your platform) — schema/data portability.

**Don't:**
- Don't assume tenant isolation from app code alone — defense in depth.
- Don't use **shared credentials** across tenants — separate auth per tenant.
- Don't ignore **noisy neighbor** — one tenant's load affects others.
- Don't store tenant data in **shared caches** without keying by tenant.

*Ref: Fundamentals_of_Software_Architecture.md — implicit in Microservices, Architectural Characteristics (security, scalability)*

---

### Serverless & FaaS Architecture

**Principle:** Serverless abstracts infrastructure; you pay per execution. Trade-offs in **cold starts**, **execution time limits**, and **per-function scaling**.

**Do:**
- Use serverless for:
  - **Spiky workloads** (marketing campaigns, IoT event bursts).
  - **Stateless APIs** with low average utilization.
  - **Event-driven** processing (file uploads → thumbnail generation).
  - **Cron-like** jobs (daily reports).
- Optimize **memory size** (more memory = more CPU = sometimes cheaper overall).
- Mitigate **cold starts** with provisioned concurrency (when latency matters).
- Design functions as **stateless and short-lived**.
- Use **step functions** for orchestration of multi-step serverless workflows.

**Don't:**
- Don't use serverless for:
  - **Long-running** processes (functions have execution time limits).
  - **CPU-intensive** work (per-second cost is high).
  - **Stateful** applications (state must be external).
- Don't assume infinite scaling — **concurrent execution limits** apply (Lambda: 1000 per region default).
- Don't ignore **cost at scale** — serverless can be more expensive than provisioned for steady loads.

*Ref: Fundamentals_of_Software_Architecture.md — implied in cloud architecture, Engineering Practices*

---

### Operational Excellence — Day-2 Architecture

**Principle:** Architecture is for Day 2, not just Day 1. The system must be **operable** by humans and tools, not just **buildable** by the original developers.

**Day-2 concerns:**
- **Deployment:** Can we deploy without downtime? Roll back safely?
- **Observability:** Can we see what's happening?
- **Debugging:** Can we diagnose issues from logs/traces?
- **Scaling:** Can we handle load changes?
- **Updates:** Can we apply security patches without service disruption?
- **Disaster recovery:** Can we recover from data loss, region failure?
- **Compliance:** Can we audit access, prove data handling?

**Do:**
- Treat **Day-2 capabilities** as architectural requirements from day 1.
- Apply the **operational readiness review** (ORR) before production launch.
- Build **runbooks** for common incidents (deployment, rollback, scaling).
- Use **chaos engineering** (Netflix Chaos Monkey style) to test failure modes.
- Practice **disaster recovery drills** — DR plans untested are useless.
- Document **SLOs** (Service Level Objectives) — error budget drives priorities.

**Don't:**
- Don't build features and assume operations — design for ops from start.
- Don't skip the ORR — Day-2 gaps are discovered under fire.
- Don't ignore **dependency failures** — third-party services fail too.
- Don't rely on **manual runbooks** for frequent operations — automate.

*Ref: Fundamentals_of_Software_Architecture.md — "Operations/DevOps", "Engineering Practices"*

---

### Architecture Documentation — What to Write

**Principle:** Documentation supports decision-making. It should be **as simple as possible** but cover the **load-bearing decisions**.

**Documentation hierarchy:**
1. **README** — what is this system, who owns it, how do I run it.
2. **Architecture overview** — style, characteristics, diagrams (C4 L1+L2).
3. **Component documentation** — what each component does, its API, its data.
4. **ADRs** — why decisions were made (not just what).
5. **Runbooks** — operational procedures (deploy, rollback, incidents).
6. **ADRs as Documentation** — search-friendly historical record.

**Do:**
- Use **arc42** or **C4** as a structure template.
- Keep diagrams **near code** (in the same repo, ideally).
- Generate docs from code when possible (OpenAPI, AsyncAPI).
- Link ADRs to **specific decisions** in code (e.g., ADRs in `docs/adr/`).
- Document **non-obvious things** (why, not what).
- Update docs **as part of the PR** that changes the architecture.

**Don't:**
- Don't write **comprehensive docs that nobody reads** — keep it focused.
- Don't write **future-state docs** — they lie when the future arrives.
- Don't duplicate information across many places — single source of truth.
- Don't write **process documentation** for things that should be automated.

*Ref: Fundamentals_of_Software_Architecture.md — "ADRs as Documentation"*

---

### Cost as an Architecture Characteristic

**Principle:** Cost is a quality attribute like scalability or performance. Architecture decisions have cost implications that must be analyzed.

**Cost dimensions:**
- **Infrastructure** — compute, storage, network.
- **Operational** — humans to run the system.
- **Development** — humans to build and maintain.
- **Opportunity cost** — what we're not building because of this.

**Do:**
- Apply the **finops principle** — engineering, finance, and business collaborate on cost.
- Track cost per **transaction / request / customer** — unit economics.
- Use **right-sizing** for compute (don't over-provision).
- Use **spot instances** for fault-tolerant workloads (60-90% cheaper).
- Set **budgets** and alerts — surprises are bad.
- Tag resources by **team, service, environment** — understand attribution.

**Don't:**
- Don't treat cost as a **Phase 2 concern** — design for cost from day 1.
- Don't ignore **hidden costs** — data transfer, log storage, third-party APIs.
- Don't optimize prematurely — measure first.
- Don't sacrifice **availability/security** for cost — those have hard floors.

*Ref: Fundamentals_of_Software_Architecture.md — "Scalability and Costs", Manageability*

---

### Process & Workflow Architecture

**Principle:** Process (how teams work) is part of architecture. Process decisions have leverage similar to technical decisions.

**Do:**
- Define a **branching strategy** (trunk-based preferred; gitflow for some compliance contexts).
- Define a **PR review process** — required reviewers, automated checks.
- Define a **deployment cadence** — daily, weekly, on-demand.
- Define a **release process** — feature flags, gradual rollouts, A/B tests.
- Use **definition of done** — covers code, tests, docs, monitoring.
- Define **incident response** — on-call, escalation, post-mortems.
- Use **GitOps** (infrastructure as code, declarative config in git).

**Don't:**
- Don't make process decisions ad-hoc — codify them.
- Don't gate releases on manual approval (humans are slow and inconsistent).
- Don't skip **post-mortems** — failures are learning opportunities.
- Don't use **hero culture** — sustainable pace beats heroics.
- Don't allow process to bypass technical standards (architecture fitness functions).

*Ref: Fundamentals_of_Software_Architecture.md — "Process", "Engineering Practices"*

---

### Data Architecture (Beyond Polyglot Persistence)

**Principle:** Data architecture = decisions about storage, movement, transformation, and access patterns. It interacts tightly with system architecture.

**Data architecture decisions:**
- **Transactional store:** Where do committed business facts live?
- **Read models:** Denormalized views for queries.
- **Cache layer:** What's worth caching, where, how long?
- **Search index:** Text search, faceting (Elasticsearch, Solr).
- **Time-series store:** Metrics, events (InfluxDB, TimescaleDB).
- **Data warehouse:** Analytics, historical (Snowflake, BigQuery).
- **Data lake:** Raw data for future analysis (S3 + Athena).

**Do:**
- Match **data model** to **access pattern** (relational for transactional; document for hierarchical; wide-column for sparse).
- Use **polyglot persistence** — different stores for different needs.
- Make data **immutable when possible** — easier to reason about.
- Apply **data partitioning** — vertical (columns), horizontal (rows).
- Plan for **data retention** — GDPR, regulatory, archival.
- Document **data flows** — data lineage, transformations, ownership.

**Don't:**
- Don't use **one database for everything** — polyglot persistence is a thing.
- Don't store **derived data** in the source of truth — calculate on read or materialize separately.
- Don't ignore **data gravity** — large datasets attract processing (move compute to data).
- Don't skip **backup and recovery testing** — backups you haven't restored are guesses.

*Ref: Fundamentals_of_Software_Architecture.md — "Data", Microservices Data Isolation*

---

### When NOT to Adopt Microservices

**Principle:** Microservices have a cost. Apply only when the benefits exceed the cost.

**Don't adopt microservices if:**
- **Team size < 5-7** — coordination overhead exceeds benefits.
- **Domain is not well understood** — boundaries will be wrong; monolith → refactor first.
- **Engineering practices are not mature** — without CI/CD, monitoring, automation, microservices fail.
- **Traffic is low** — single instance can handle load.
- **Strong consistency across many entities is required** — chatty distributed transactions.
- **No clear bounded contexts** — boundaries will be technical, not domain.

**Do adopt microservices if:**
- **Team size > 20-30** — communication overhead demands decentralization.
- **Independent release cadences** matter (different teams deploy different features).
- **Scaling varies by component** (e.g., high-write component needs 100× the resources of others).
- **Polyglot** is required (different stacks for different problems).
- **Resilience** requires isolation (one component failing shouldn't take down everything).

**Alternative: Modular Monolith:**
- Single deploy unit, but **disciplined module boundaries**.
- Each module has clear API, owns its data table(s).
- Modules can be extracted to services later.
- **Best of both worlds** for many use cases.

*Ref: Fundamentals_of_Software_Architecture.md — "Modular Monolith", Microservices*

---

### Team Topologies (Skelton & Pais)

**Principle:** Team structure drives architecture. Four team types per Skelton & Pais:

1. **Stream-aligned team:** Aligned to a flow of work (e.g., Customer Onboarding team).
2. **Enabling team:** Helps stream-aligned teams overcome obstacles (e.g., Test Automation team).
3. **Complicated-subsystem team:** Owns subsystems requiring specialist expertise (e.g., ML models team).
4. **Platform team:** Provides internal services that stream-aligned teams consume (e.g., authentication platform).

**Team interaction modes:**
- **Collaboration:** Two teams work closely together.
- **X-as-a-Service:** One team provides a service, another consumes with minimal interaction.
- **Facilitating:** One team helps another (enabling team pattern).

**Do:**
- Identify **cognitive load** — what must each team hold in their heads?
- Default to **stream-aligned teams** — they're the primary delivery units.
- Apply **Thinnest Viable Platform** (TVP) — platform provides only what stream-aligned teams can't build faster themselves.
- Use **team APIs** — explicit contracts between teams, like service APIs.
- Bound team size by **cognitive load**, not headcount.

**Don't:**
- Don't create **component teams** (UI team, DB team) — they're anti-pattern.
- Don't have teams **owned by managers** — teams are owned by missions.
- Don't let **big team** inertia persist — split when coordination costs exceed delivery speed.

*Ref: Fundamentals_of_Software_Architecture.md — "Conway's Law", "Architecture Partitioning" (related to Team Topologies book)*

---

### Architectural Spikes — POCs for Risky Decisions

**Principle:** Architectural spikes are time-boxed investigations to reduce risk on specific decisions. They're not throwaway code.

**Do:**
- Use spikes for **risky, expensive-to-change decisions**: language, framework, database, architecture style.
- **Time-box spikes** strictly (1-3 days, max).
- **Production-quality code** when possible — throwaway code becomes reference architecture.
- Document spike results as **ADRs** with evidence.
- Include spikes in **iteration planning** — they're not free.
- Use **multiple spikes** when comparing alternatives.

**Don't:**
- Don't spike everything — only high-uncertainty, high-impact decisions.
- Don't let spikes become **undisciplined exploration** — set goals.
- Don't skip spike results documentation — the learning is the value.
- Don't promote spike code to production without review — it's a POC.

*Ref: Fundamentals_of_Software_Architecture.md — "Balancing Architecture and Hands-On Coding", "Expectations of an Architect"*

---

### Architecture Decision Records — Lifecycle Management

**Principle:** ADRs have a lifecycle. Managing them properly keeps documentation trustworthy.

**ADR statuses:**
- **Proposed:** Drafted, under discussion.
- **Accepted:** Approved and active.
- **Superseded:** Replaced by a newer ADR (with link).
- **Deprecated:** No longer applicable but kept for history.
- **Rejected:** Not adopted (kept for "why not" context).

**Lifecycle stages:**
1. **Draft** — author writes initial ADR.
2. **Review** — team, ARB, stakeholders provide feedback.
3. **Decision** — status set to Accepted/Rejected.
4. **Active** — guides current work.
5. **Supersession** — replaced by newer ADR when context changes.
6. **Archival** — moved to `docs/adr/archive/` after years.

**Do:**
- Use **GitOps-style** ADR storage (in repo, versioned with code).
- Reference ADRs from code comments when relevant.
- Review ADRs **annually** — context changes, decisions may need updating.
- Use **templates** for consistency (Context/Decision/Consequences).
- Link ADRs to **architecture fitness functions** when applicable.
- Make ADR numbers monotonic — never renumber.

**Don't:**
- Don't delete superseded ADRs — they're history.
- Don't skip the **Consequences** section — it's the most useful for future readers.
- Don't write ADRs as **personal opinions** — they should be team/ARB decisions.
- Don't let ADRs grow indefinitely — keep them short (1-2 pages).

*Ref: Fundamentals_of_Software_Architecture.md — "ADRs as Documentation", "Using ADRs for Standards"*

---

## Anti-Patterns & Common Mistakes

- **Covering Your Assets:** Architect avoids/deferring decisions out of fear → *fix:* Make decisions at the last responsible moment; collaborate with developers continuously.
- **Groundhog Day:** Same architecture decision revisited repeatedly because rationale wasn't documented → *fix:* Use ADRs with full Context/Decision/Consequences.
- **Email-Driven Architecture:** Decisions communicated only via email threads → *fix:* Single canonical ADR, link from email, only notify directly-impacted people.
- **Big Ball of Mud:** Haphazardly structured system with no discernible architecture → *fix:* Establish governance via fitness functions, modular boundaries.
- **Architecture by Implication:** "We're just starting to code" → defaults to layered → *fix:* Deliberately select style via trade-off analysis.
- **Accidental Architecture:** Same as above, by accident rather than intent.
- **Ivory Tower Architect:** Dictates from on high, doesn't collaborate → *fix:* Provide justifications, ask developers to arrive at solutions themselves.
- **Control Freak Architect:** Makes every decision, micromanages implementation → *fix:* Apply Elastic Leadership (5-factor scoring) to determine appropriate control.
- **Armchair Architect:** Disconnected from implementation details → *fix:* Continue coding, sit with the team, do code reviews.
- **Frozen Caveman:** Single past incident distorts every future decision → *fix:* Recognize and counter ("Italy-ility" lesson).
- **Sinkhole Anti-Pattern:** >80% of requests pass through layers without logic → *fix:* Switch to different style or accept trade-off of open layers.
- **Entity Trap:** Components mirror database tables (ORM-as-architecture) → *fix:* Use Actor/Actions, Event Storming, or Workflow approach for component identification.
- **Stamp Coupling:** Returning 500 KB to deliver 200 B → *fix:* Field selectors, GraphQL, private RESTful endpoints, CDCs.
- **Bullet-Riddled Corpse:** Slides full of speaker notes → *fix:* Use incremental builds; slides are half the story.
- **Irrational Artifact Attachment:** Attachment scales with time invested → *fix:* Iterate on low-fidelity artifacts first.
- **Cookie-Cutter:** Forcing content to fit a slide → *fix:* Use multiple slides with dissolves; ideas don't have predetermined word counts.
- **Pluralistic Ignorance:** Silent dissent in meetings → *fix:* Architect as facilitator; explicitly invite dissent.
- **Diffusion of Responsibility:** Confused ownership → *fix:* Smaller teams; check ownership boundaries.
- **Process Loss:** Adding people makes project later (Brooks's law) → *fix:* Find parallel work streams; question new hires when no parallelism exists.
- **Analysis Paralysis:** Forever discussing, never deciding → *fix:* ADR with RFC status + deadline date.
- **Technical Partitioning for Domain Logic:** Forcing workflow concepts into layered architecture → *fix:* Use modular monolith or domain partitioning.
- **Italy-ility:** Inventing a unique characteristic for one past incident → *fix:* Distinguish genuine from perceived risk.

*Ref: Fundamentals_of_Software_Architecture.md — Distributed across Chapters 1, 9, 10, 12, 14, 19, 21, 22, 23*

---

## Decision Heuristics / Checklists

### When to choose each architecture style

- **Monolith possible (single quantum)?** → Modular Monolith, Layered, Pipeline, Microkernel
- **Multiple quanta needed?** → Service-Based, Microservices
- **Bursty, highly elastic load (>10k concurrent users)?** → Space-Based or Event-Driven
- **Heavy domain coupling (multipage forms, semantic chains)?** → Avoid microservices; choose Service-Based
- **Customization-heavy product?** → Microkernel
- **ETL/data processing?** → Pipeline
- **Small/simple web app, tight budget?** → Layered
- **Independent release cadence per workflow needed?** → Microservices
- **Pragmatic middle ground (don't need full microservices cost)?** → Service-Based
- **Real-time, dynamic workflow?** → Event-Driven (mediator) or hybrid

### Architectural quantum decision

- **One quantum?** → Single deploy unit, shared DB, synchronous connascence → monolith
- **Multiple quanta?** → Different characteristics per component → distributed

### Communication style

- **Default to synchronous**; use asynchronous when:
  - High decoupling needed
  - Responsiveness under load matters (responsiveness ≠ performance)
  - Back-pressure required (event buffering)
  - Variable operational characteristics between services

### ADR self-approval gate

Self-approve if ALL are true:
- Cost below threshold (e.g., €5,000)
- No cross-team impact
- No security implication

Otherwise → status: **Proposed**, escalate to ARB or chief architect.

### Architecture characteristic identification

- Top 3–5 only
- Cover operational + structural + cross-cutting as needed
- Distinguish explicit (in requirements) from implicit (domain knowledge)
- Eliminate-one exercise to confirm priority

### Risk assessment (per dimension)

1. Identify individually (no collaboration) → score 1–9
2. Consensus collaboratively → agree on rating
3. Mitigate collaboratively → propose changes
4. Restrict to one dimension per session

### Architect control factors (5 × ±20)

Sum the five factors; positive = control freak, negative = armchair. Target: stay in the band appropriate for the team.

### Checklists that help (not procedural flows)

- Developer Code Completion Checklist (definition of done)
- Unit and Functional Testing Checklist (edge cases)
- Software Release Checklist (incident-learned items)

---

## Key Takeaways

1. **Architecture = structure + characteristics + decisions + principles** — name all four, not just the structure.
2. **Everything in architecture is a trade-off** (First Law); **why is more important than how** (Second Law).
3. **Pick 3–5 architecture characteristics** and design for the *least worst* — not the *best*.
4. **Architectural quantum** = independently deployable + high functional cohesion + synchronous connascence — use it to decide monolith vs distributed.
5. **Conway's Law is inescapable** — use the **Inverse Conway Maneuver** to align teams with desired architecture.
6. **Technical depth for developers, technical breadth for architects** — apply the 20-Minute Rule.
7. **Capture decisions in ADRs** with Context/Decision/Consequences/Compliance/Notes; avoid Covering Your Assets → Groundhog Day → Email-Driven Architecture.
8. **Use fitness functions** to govern architecture characteristics — automate compliance where possible.
9. **Component identification is iterative** — start coarse-grained, split as needed; avoid the entity trap.
10. **Each architecture style embodies known trade-offs** — the ratings matrix tells you when to use each.
11. **Default to synchronous, asynchronous when necessary** — measure 95th–99th percentile latency.
12. **Never do transactions across microservices** — fix granularity instead; use sagas sparingly.
13. **Risk storm collaboratively** with senior developers, restrict to one dimension per session.
14. **Soft skills (4 C's) are 50% of the architect role** — Communication, Collaboration, Clarity, Conciseness.
15. **Stay hands-on** — POCs, code reviews, fitness functions, technical-debt stories.
16. **Architecture is iterative, not waterfall** — all architectures become iterative because of unknown unknowns; Agile just recognizes it sooner.
17. **Treat the 8 fallacies of distributed computing as design constraints** — every network call needs timeouts, idempotency, and security.
18. **Partition by domain for microservices, by technique for simple CRUD** — Conway's law cuts both ways.
19. **Architecture style choice is reversible early and costly late** — make the monolith→distributed transition while characteristics still support either.

---

## Cross-References
- Related: `Building_Evolutionary_Architectures.md` (extends fitness-function concept)
- Related: `Designing_Data-Intensive_Applications.md` (extends data architecture / distributed transactions)
- Related: `Software_Architecture_The_Hard_Parts.md` (extends trade-off analysis, modular decomposition)
- Related: `Team_Topologies.md` (extends Conway's law and team boundaries)
- Related: `Foundations_of_Scalable_Systems.md` (extends distributed-systems fundamentals)
- Topic index: `INDEX.md`