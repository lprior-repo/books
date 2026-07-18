# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Fundamentals of Software Architecture
**Authors:** Mark Richards & Neal Ford
**Topic tags:** `#architecture` `#testing` `#api`
**Language focus:** language-agnostic (Java/C# examples where they appear)
**Sources:** `markdown_output/Fundamentals of Software Architecture/Fundamentals of Software Architecture.md` · `summaries/Fundamentals_of_Software_Architecture.md`

## TL;DR
Foundational engineering-discipline treatment of software architecture: how to think architecturally, define and govern architecture characteristics, decompose systems into components, choose among the eight core styles (layered, pipeline, microkernel, service-based, event-driven, space-based, orchestration-SOA, microservices), capture decisions in ADRs, quantify risk via the risk matrix and risk storming, diagram with C4/UML/ArchiMate, and lead teams via the 4 C's. Apply whenever shaping system structure, evaluating style trade-offs, or establishing architectural governance.

---

## Best Practices by Topic

### Architect Role & Laws of Software Architecture

**Principle:** Architecture is the set of structural decisions, architecture characteristics ("-ilities"), architecture decisions (rules), and design principles (guidelines) — guided by two immutable laws.

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

**Don't:**
- Don't try to maintain deep expertise in a wide variety of areas — you'll succeed in none.
- Don't let *stale expertise* masquerade as current knowledge; large companies suffer when founder-developers make decisions with decade-old criteria.
- Don't separate architect from developers with virtual/physical barriers — they form a bidirectional loop, not a waterfall handoff.

*Ref: Fundamentals_of_Software_Architecture.md — "Architectural Thinking", "Technical Breadth", "Frozen Caveman Anti-Pattern", "Analyzing Trade-Offs"*

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

**Don't:**
- Don't mistake LCOM for logical-cohesion detection — it's purely structural.
- Don't let shared utility classes accumulate; they bind unrelated code via incidental coupling.

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

---

## Cross-References
- Related: `Building_Evolutionary_Architectures.md` (extends fitness-function concept)
- Related: `Designing_Data-Intensive_Applications.md` (extends data architecture / distributed transactions)
- Related: `Software_Architecture_The_Hard_Parts.md` (extends trade-off analysis, modular decomposition)
- Topic index: `../INDEX.md`