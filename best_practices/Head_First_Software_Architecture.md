# Head First Software Architecture

**Authors:** Raju Gandhi, Mark Richards, Neal Ford
**Publisher:** O'Reilly Media, Inc. — Head First series (March 2024, First Edition)
**Topic tags:** `#architecture` `#general`
**Language focus:** Language-agnostic; architectural thinking, styles, trade-offs, and decision-making
**Sources:** `markdown_output/Head First Software Architecture/Head First Software Architecture.md` · `summaries/Head_First_Software_Architecture.md`

## TL;DR

A learner's guide to architectural thinking built on the **Four Dimensions** (architectural characteristics, architectural decisions, logical components, architectural style) and the **Two Laws** (everything is a trade-off; understanding *why* matters more than knowing *how*). Learn to extract characteristics (FURPS+), identify components via workflow or actor/action, evaluate monoliths (layered, modular, microkernel) and distributed systems (microservices, event-driven), capture decisions as ADRs, and choose styles by context, not hype. The book pairs each style with its superpowers, kryptonite, and a star-rating sheet for trade-off analysis. Includes two "do it yourself" chapters (TripEZ monolithic, Make the Grade distributed), ADR mechanics, diagramming techniques, and an appendix on coding architect, soft skills, and architectural katas.

---

## Best Practices by Topic

### 1. Treat Architecture as Four Aligned Dimensions

**Principle:** Every architecture is described by four inseparable dimensions. Skip any one and the picture is incomplete.

| Dimension | Purpose | Example |
|---|---|---|
| Architectural characteristics | Non-domain capabilities the system must support ("ilities") | scalability, performance, availability, security |
| Architectural decisions | Rules and constraints that guide implementation (style, protocols, persistence) | "UI must not access DB directly" |
| Logical components | Functional building blocks of the domain (rooms in a house) | Order Placement, Bid Capture, Inventory Management |
| Architectural style | Overall shape and deployment pattern (Victorian, ranch, microservices) | layered, modular monolith, microservices, EDA |

The metaphor: just as a house needs a blueprint before construction, software needs architecture before development. The structure — its components, relationships, organization — is its architecture. Architecture is the set of decisions that are hard to change.

**Puzzling out the dimensions:** You can think of software architecture as a puzzle, with each dimension representing a separate puzzle piece. They must all fit together and interact to build a complete picture. The architectural style must align with the architectural characteristics you choose as well as the architectural decisions you make. Similarly, the logical components you define must align with the characteristics and the architectural style as well as the decisions you make.

> One common mistake software architects make is using only one or two of these dimensions when describing their architecture. "Our architecture is microservices" describes a single dimension — the architectural style — but leaves too many unanswered questions.

**Do:**
- Demand all four dimensions in every architecture description.
- Derive characteristics before selecting a style ("Our architecture is microservices" leaves too much unstated).
- Realign components when decisions, characteristics, or style change.
- Understand that all four dimensions are interconnected — you cannot skip any.

**Don't:**
- Don't describe a system as "microservices" and stop there — that is a single dimension.
- Don't choose a style before identifying characteristics and components.
- Don't let one dimension (typically style) drive all the others.

*Ref: Head First Software Architecture.md — "Software Architecture Demystified" / "The Four Dimensions of Software Architecture" / "Puzzling out the dimensions" / "The first/second/third/fourth dimension"*

---

### 2. Architecture Versus Design — A Spectrum, Not a Line

**Principle:** Architecture and design exist on a spectrum, not as a binary. Architecture decisions are structural, have broad impact, are difficult to reverse, and affect the entire system. Design decisions are more localized, easier to change, and affect specific components or features.

**Three criteria for determining where a decision falls on the spectrum:**

1. **Strategic versus tactical:** Strategic decisions (affecting the whole system) are more architectural; tactical decisions (affecting specific parts) are more design-oriented.
2. **High versus low effort:** Decisions requiring significant effort to change are more architectural; those easy to change are more design-oriented.
3. **Significant versus less-significant trade-offs:** Decisions involving major trade-offs are more architectural.

**A design perspective (UML class diagram):** Shows how classes interact to implement functionality but says nothing about physical structure — how classes are organized and deployed.

**An architectural perspective:** Shows the structure of the system — services, databases, communication. From an architectural perspective, you might decide to create separate services for each payment type within the order payment process and have an orchestrator service to manage the payment processing part.

> Knowing where along the spectrum between architecture and design your decision lies helps determine *who* should be responsible for ultimately making that decision. Some decisions the development team should make (designing classes), some an architect should make (choosing the architectural style), and others should be made together (breaking apart services).

**Do:**
- Apply the three-question test (strategic? effort? trade-offs?) to every non-trivial decision.
- Ask "is it hard to change later?" (Martin Fowler's definition).
- Distinguish architectural from design decisions early to assign ownership correctly.
- Recognize that most decisions fall in the middle of the spectrum, not at the extremes.

**Don't:**
- Don't treat architecture vs. design as binary.
- Don't let developers make architectural decisions alone, or architects make design decisions alone.

*Ref: Head First Software Architecture.md — "A design perspective" / "An architectural perspective" / "The spectrum between architecture and design" / "Strategic versus tactical" / "High versus low levels of effort" / "Significant versus less-significant trade-offs"*

---

### 3. Honor the Two Laws of Software Architecture

**First Law:** *Everything in software architecture is a trade-off.* No "best practices," only context-appropriate decisions. If you find a decision without a trade-off, you haven't looked hard enough.

**Second Law:** *Understanding why you made a decision is more important than knowing how to implement it.* Capture the reasoning so future architects (including future you) can adapt it when context changes.

**Trade-off analysis framework (5 steps):**
1. Identify the options (what are the possible choices?)
2. Evaluate each option (benefits and costs)
3. Consider the context (specific requirements and constraints)
4. Make a decision (best balance for this context)
5. Document the decision (ADR — see Topic 7)

**Worked example — Two Many Sneakers (queue vs. topic):**
The sneaker resale app needed to communicate with downstream services (notification, analytics). Team evaluated queues vs. topics:

| Option | Pros | Cons |
|---|---|---|
| **Queues** | Point-to-point, simpler semantics, one consumer per message, trading service aware of all subscribers | Heterogeneous messages harder, coupling to trading service for new consumers |
| **Topics** | Multiple consumers, more flexible, broadcast | More complex, looser security boundary |

Trade-off depends on context: if only one consumer needs each message, queues are simpler; if multiple consumers need the same message, topics are necessary. Initial decision: queues (better security because trading service aware of subscribers). Three months later, requirements changed → topics became a better fit → supersede ADR 012 with ADR 021.

> The First Law shows that architecture is not about finding the "right answer" — it's about finding the *best answer for your context*. The Second Law shows that even when context changes, the *why* you recorded lets future-you or your successor adapt rather than re-litigate.

**Do:**
- Apply the five-step framework to every non-trivial decision.
- Question every "best practice" until you understand its underlying context.
- Use ADR statuses (Proposed, Accepted, Superseded) to surface context shifts.
- Default to "it depends" when asked architectural questions.

**Don't:**
- Don't copy architectural patterns because they are popular.
- Don't let outcome bias override process evaluation.
- Don't accept a decision in isolation from its context.

*Ref: Head First Software Architecture.md — "The Two Laws of Software Architecture" / "Communicating with downstream services" / "Analyzing trade-offs" / "Trade-off analysis: Queue edition" / "Trade-off analysis: Topic edition" / "The first law of software architecture" / "It always comes back to trade-offs" / "The second law of software architecture"*

---

### 4. Sourcing Architectural Characteristics (FURPS+)

**Principle:** Architectural characteristics are non-domain design considerations that influence structural decisions. They are critical or important to application success, synergistic with one another, overabundant, and impossible to standardize across organizations.

**FURPS+ classification (canonical academic mapping):**
- **Functional:** the domain features the system must perform
- **Usability:** human factors, aesthetics, consistency, documentation
- **Reliability:** frequency/severity of failure, recoverability, predictability, availability
- **Performance:** throughput, latency, response time, recovery time
- **Supportability:** testability, extensibility, adaptability, maintainability, configurability, installability, localizability

The "+" in FURPS+ covers additional constraints like implementation (resource limits, languages/tools), interface (external systems), physical (hardware constraints), and design (constraints that must be met by the design itself).

**Three sources for architectural characteristics:**
1. **The problem domain** — the business domain itself implies certain characteristics. A financial trading system requires ultra-low latency; a healthcare system requires strict privacy and auditability.
2. **Environmental awareness** — the deployment environment, team structure, and operational context reveal characteristics that may not be obvious from requirements alone.
3. **Holistic domain knowledge** — the architect's broad experience across domains helps identify characteristics that stakeholders may not think to mention but are critical for success.

**Composite characteristics:** Some characteristics cannot be measured directly but are composed of more specific, measurable sub-characteristics. "Performance" is a composite; "first contentful paint" (the time for a web page to render its first content) is a measurable sub-characteristic. Make characteristics specific enough to be objectively measured.

**Implicit vs. explicit:** Explicit characteristics are stated in requirements. Implicit characteristics are factors that influence an architect's decisions but aren't called out — security is often implicit: even if it isn't mentioned, architects know we shouldn't design an insecure system.

**Do:**
- Derive characteristics from all three sources: problem domain, environmental awareness, holistic domain knowledge.
- Treat implicit characteristics (security, maintainability, observability, feasibility) as candidates; promote them to *driving* characteristics only when they influence structural decisions.
- Decompose composite characteristics into measurable sub-characteristics ("performance" → "first contentful paint").
- Limit driving characteristics to 3–5 (the book's worksheet uses 7 to filter, then narrows to top 3) to prevent overengineering.
- Translate business English into architectural terms: "Lafter changes constantly" → modularity, extensibility.

**Don't:**
- Don't accept business requirements literally without asking "but why?" — users often bring solutions, not requirements (F-16 Mach 2.5 story).
- Don't maximize characteristics — more characteristics force more complex designs.
- Don't let every characteristic become driving — implicit characteristics stay implicit unless they shape structure.

*Ref: Head First Software Architecture.md — "Defining architectural characteristics" / "Characteristics are nondomain design considerations" / "Characteristics influence architectural structure" / "Limit characteristics to prevent overengineering" / "Sourcing architectural characteristics from the problem domain" / "Sourcing architectural characteristics from environmental awareness" / "Sourcing architectural characteristics from holistic domain knowledge" / "Composite architectural characteristics" / "Consider explicit and implicit capabilities" / "Lost in translation" / "Priorities are contextual" / "Limiting architectural characteristics"*

---

### 5. Categorize Characteristics by Type (Zoo of -ilities)

**Principle:** Characteristics cluster into process, structural, operational, and cross-cutting categories. Each category implies different design choices.

| Category | Examples | Implication |
|---|---|---|
| Process | modularity, testability, agility, deployability, extensibility | Shape how the team builds and ships |
| Structural | maintainability, extensibility, portability, localization | Shape internal organization |
| Operational | availability, scalability, recoverability, robustness, reliability, performance | Shape runtime topology |
| Cross-cutting | security, accessibility, privacy, legal, auditability, authentication/authorization | Span multiple categories |

**Operational characteristics detail:**
- **Availability:** percentage of time the system is up; "nines" (99.999% = 5 nines, ~6 minutes/year downtime)
- **Recoverability:** how quickly the system can get online again after a disaster; affects backup strategy and duplicated hardware
- **Robustness:** ability to handle errors and boundary conditions while running (power, internet, hardware failures)
- **Reliability/safety:** whether the system is fail-safe or mission-critical (medical, hospital, airplane apps)
- **Performance:** how well the system achieves timing requirements using available resources
- **Scalability:** how well the system performs as users/requests increase

**Cross-cutting characteristics detail:**
- **Security:** encryption (at rest, in transit), authentication, network protection
- **Authentication/authorization:** ensuring users are who they claim; restricting access by use case, subsystem, page, rule, or field
- **Privacy:** hiding/encrypting transactions so internal employees cannot see them
- **Accessibility:** ease of access for users with disabilities (colorblindness, hearing loss)
- **Usability:** how easily users achieve goals; whether training is required

**Synergy:** Architectural characteristics are synergistic — combining them yields something different than the sum of parts (think peanut butter + chocolate, or emulsions). When you change one, you typically must change others. Security improvements usually degrade performance. Adding payment info changes security *and* data integrity.

**Do:**
- Distinguish implicit cross-cutting characteristics (security) from context-specific driving ones.
- Use the "International Zoo of -ilities" as a checklist, knowing the list is never complete (and varies by organization — create a ubiquitous language).
- Map characteristics to style superpowers and kryptonite.
- Acknowledge that some characteristics are composite and need decomposition.

**Don't:**
- Don't try to maximize every characteristic — choose 3–5 driving ones.
- Don't assume "everyone's list is the same" — there's no universal standard.
- Don't accept overabundance — overengineering follows.

*Ref: Head First Software Architecture.md — "Process architectural characteristics" / "Structural architectural characteristics" / "Operational architectural characteristics" / "Cross-cutting architectural characteristics" / "The International Zoo of -ilities" / "Synergy can be dangerous!"*

---

### 6. Identify Logical Components via Workflow or Actor/Action

**Principle:** Logical components are the building blocks of the system. They are represented as directory structures/namespaces; many can coexist in a single deployment, and many can map to a single service. Architectural decisions restrict how they fit into layers or services.

**Logical vs. physical architecture:**
- **Logical architecture** describes what the components are and how they interact, without specifying how they are deployed. It is concerned with responsibilities, boundaries, and relationships.
- **Physical architecture** describes how components are deployed and communicate at runtime — servers, containers, network calls, technology implementation.

The logical architecture should be designed first, and the physical architecture should follow from it.

**Workflow approach (best for clear user journeys):** Group functionality by major use-case steps. Output: workflow-step → component mapping.

For the auction system (Adventurous Auctions case study):
- Step 1: Register online users → User Registration
- Step 2: List items for auction → Item Listing
- Step 3: Place bids → Bid Capture
- Step 4: Determine winner → Bid Resolution
- Step 5: Charge credit card → Payment Processing

**Actor/action approach (best for multiple user types):** List actors and their actions, then group related actions into components.

For the auction system:
- Sellers: list items, manage auctions, view bids → Auction Management
- Bidders: search items, place bids, make payments → Bid Capture / Payment
- System: close auctions, notify winners → Notification

**Four-step process for creating logical architecture:**
1. **Step 1: Identify Initial Core Components** — workflow or actor/action approach; output is initial "empty jars" representing rough guesses
2. **Step 2: Assign Requirements** — map each functional requirement to a component; if a requirement doesn't fit any component, either a component is missing or the existing components need expansion
3. **Step 3: Analyze Roles and Responsibilities** — refine component boundaries (does the name describe what it does? single cohesive responsibility? no duplication?)
4. **Step 4: Analyze Characteristics** — components may need splitting or merging for performance, scalability, or fault tolerance (e.g., split Bid Capture from Auction Management during peak load)

**The Entity Trap:** Don't model components after domain entities ("BidManager" that handles everything related to bids). This leads to vague component names, components with too many responsibilities, poor cohesion, and difficulty scaling. Components should be organized around cohesive responsibilities, not around entities.

Watch for words like *manager* or *supervisor* in component names — those are good indicators that you've fallen into the entity trap. Other telltale words: *handler*, *processor*, *system*, *controller* (sometimes), *service* (vague). Reference data may legitimately be "Reference Data Manager" — context matters.

**Do:**
- Use workflow approach when the system has one or few user types with well-defined journeys.
- Use actor/action when the system has many distinct user types with overlapping functionality.
- Combine approaches: actor/action first, workflow second.
- Assign each requirement to exactly one component to surface missing components.
- Use the system metaphor (Kent Beck) to choose a component metaphor that names and explains it.
- Iterate Step 4: analyze characteristics — components may need splitting or merging.

**Don't:**
- Don't fall into the **entity trap** (naming components like "BidManager" that bundle every responsibility of an entity).
- Don't use entity decomposition as the primary approach.
- Don't stop refining after the first guess — initial core components are deliberately rough.

*Ref: Head First Software Architecture.md — "Step 1: Identifying initial core components" / "Workflow approach" / "Actor/action approach" / "The entity trap" / "Step 2: Assign requirements" / "Step 3: Analyze roles and responsibilities" / "Sticking to cohesion" / "Step 4: Analyze characteristics" / "The Bid Capture component"*

---

### 7. Manage Coupling and Cohesion

**Principle:** High cohesion within components and loose coupling between them is the goal. Components must talk to immediate friends, not strangers.

**Coupling types:**
- **Afferent coupling (Ca):** Incoming — how many other components depend on this one. High Ca means the component is widely used; changes have broad impact.
- **Efferent coupling (Ce):** Outgoing — how many other components this one depends on. High Ce means the component is vulnerable to dependency changes.
- **Instability:** Ce / (Ca + Ce); 0 = stable, 1 = unstable.
- **Total coupling (CT):** Ca + Ce.
- **Abstractness:** ratio of abstract types to total types.
- **Distance from the main sequence:** how far a component deviates from the ideal balance of abstractness and instability.

**Law of Demeter (Principle of Least Knowledge):** Components should talk only to immediate friends. Avoid `a.getB().getC().doSomething()` chains. Reducing such chains reduces coupling and improves maintainability.

**The tightly coupled system anti-pattern:** A monolithic or distributed system where every component depends on every other (the "big ball of mud"). High coupling means changing one part requires understanding and changing many others.

**A balancing act:** Coupling cannot be eliminated — components must interact to form a system. The goal is to manage coupling: keep it where it is necessary and minimize it where it is not. Trade workflow visibility for coupling reduction: loosely coupled systems distribute knowledge, making workflows harder to follow but each component less risky to change.

**Do:**
- Move outlier functionality to its own component rather than overloading existing ones.
- Compute CT for your architecture; aim for balance.
- Apply cohesion check: are all of a component's operations related?
- For microservices: ensure no shared databases; use physical bounded contexts.

**Don't:**
- Don't interpret high coupling as inherently bad — shared stable components may legitimately have high Ca.
- Don't create a tightly coupled "Order Placement" component that knows the entire workflow.
- Don't use chains of method calls to traverse structure.

*Ref: Head First Software Architecture.md — "Component coupling" / "Afferent coupling" / "Efferent coupling" / "Measuring coupling" / "A tightly coupled system" / "Applying the Law of Demeter" / "A balancing act"*

---

### 8. Capture Decisions with Architecture Decision Records (ADRs)

**Principle:** ADRs are immutable records that capture the *what*, *why*, and *consequences* of every significant decision. They build institutional memory and prevent re-litigation of settled questions. ADRs are the formal embodiment of the Second Law.

**Seven-section ADR template:**
1. **Title** — noun phrase with three-digit prefix for sequencing (e.g., `012: Use queues for asynchronous messaging`)
2. **Status** — Proposed / Accepted / Superseded (link to new ADR when superseded)
3. **Context** — the forces at play, constraints, and concerns (why the decision is on the table)
4. **Decision** — the choice and its justification in an authoritative voice ("We will use…")
5. **Consequences** — honest trade-offs, both positive and negative
6. **Governance** — how the decision will be enforced (code reviews, fitness functions, automation)
7. **Notes / metadata** — author, approval date, supersedes relationship

**Example — Two Many Sneakers ADR 012:**

| Section | Content |
|---|---|
| **Title** | 012: Use of queues for asynchronous messaging between order and downstream services |
| **Status** | Accepted |
| **Context** | The trading service must inform downstream services (notification and analytics) about new items and transactions. Can be done via REST, queues, or topics. |
| **Decision** | We will use queues. Queues make the system more extensible since each queue can deliver a different kind of message. Furthermore, since the trading service is acutely aware of all subscribers, adding a new consumer involves modifying it — which improves security. |
| **Consequences** | Queues mean a higher degree of coupling between services. We will need to provision queuing infrastructure, requiring clustering for HA. If additional downstream services need to be notified, we will have to make modifications to the trading service. |

Three months later, requirements changed. Topics became a better fit. ADR 012 was superseded by ADR 021.

**Do:**
- Number ADRs sequentially (001, 002, …) so chronological order is preserved.
- Supersede rather than edit when a decision changes — history matters.
- Keep ADRs short; put detail in an "Alternatives" section rather than bloating Context.
- Reject architectural changes that arrive without an ADR.
- Be opinion-neutral: an ADR is a journalist's article, not an op-ed.
- Disable in-document comments after release; move discussion to issues or chat.
- Distinguish *Context* (the situation) from *Decision justification* (the rationale).

**Don't:**
- Don't skip the Consequences section — "every architectural decision has consequences."
- Don't edit an Accepted ADR; write a new one and mark the old as Superseded.
- Don't let in-document ADR comments accumulate forever.
- Don't confuse Context with the decision's justification (use the Decision section for justification).

*Ref: Head First Software Architecture.md — "Architectural decision records (ADRs)" / "Writing ADRs: Getting the title right" / "Writing ADRs: What's your status?" / "Writing ADRs: Establishing the context" / "Writing ADRs: Communicating the decision" / "Writing ADRs: Considering the consequences" / "Writing ADRs: Ensuring governance" / "Writing ADRs: Closing notes" / "The benefits of ADRs"*

---

### 9. Categorize Styles by Partitioning and Deployment

**Principle:** Architectural styles are categorized along two axes: how code is partitioned and how the system is deployed. Each style has a philosophy; match the philosophy to the problem.

**Partitioning axis:**
- **Technical** — split by concern (presentation, business, persistence). Example: layered.
- **Domain** — split by business subdomain (orders, payments, inventory). Examples: modular monolith, microservices.

**Deployment axis:**
- **Monolithic** — all components deployed as one unit. Simpler and cheaper, harder to scale.
- **Distributed** — components deployed independently. Scales and fails independently, adds network and operational complexity.

**The 2×2 matrix:**

|  | Technical Partitioning | Domain Partitioning |
|---|---|---|
| **Monolithic** | Layered architecture | Modular monolith |
| **Distributed** | (rare) | Microservices, event-driven |

**Monolithic deployment models:**

| Pros | Cons |
|---|---|
| Simpler development, testing, and deployment | Limited scalability (must scale the entire application) |
| No network latency between components | Single point of failure |
| Easier transaction management | Longer deployment cycles |
| Lower operational complexity | Technology lock-in |

**Distributed deployment models:**

| Pros | Cons |
|---|---|
| Independent scalability of components | Network latency and reliability issues |
| Fault isolation | Distributed transaction complexity |
| Technology diversity (different services can use different technologies) | Operational complexity (monitoring, logging, debugging) |
| Independent deployment | Contract management between services |

**Do:**
- Place each style you consider in this matrix and verify it against the philosophy.
- Recognize that hybrid architectures combining multiple styles are common and often correct.
- Distinguish technical partitioning (easier reuse, smeared domain) from domain partitioning (clean bounded contexts, harder cross-cutting reuse).

**Don't:**
- Don't assume a style is universally better — context determines the choice.

*Ref: Head First Software Architecture.md — "Architectural Styles — Categorization and Philosophies" / "Partitioning: technical versus domain" / "Deployment model: monolithic versus distributed" / "Monolithic deployment models: the pros/cons" / "Distributed deployment models: the pros/cons" / "And that's a wrap!"*

---

### 10. Choose the Layered Architecture for Simple, Time-Critical Systems

**Principle:** Layered architecture is technically partitioned into Presentation, Workflow/Business, and Persistence layers, deployed as a monolith. It mirrors the Model-View-Controller design pattern and is the simplest style for small systems.

**Layer structure:**
1. **Presentation layer** — handles user interface, HTTP requests, response formatting (V in MVC)
2. **Workflow (Business) layer** — contains business logic and orchestrates business processes (C in MVC)
3. **Persistence layer** — manages data access, database queries, mapping (often maps to M)
4. **Database layer** — the actual data storage

**Design patterns leveraged:**
- **MVC (Model-View-Controller)** — separates presentation concerns from business logic
- **Layers of isolation** — each layer only communicates with adjacent layers
- **Sinkhole anti-pattern** — requests pass through layers without adding value (e.g., business layer simply delegates to persistence layer)
- **Layers should apply to every request** — don't add a layer (services, integration) unless every request passes through it

**Code preserved verbatim (Python-like pseudocode from the book):**

```python
def UI_layer(request):
    data = request.get_data()
    return business_logic_layer(data)
```

```python
def business_logic_layer(data):
    processed_data = process_data(data)
    return data_access_layer(processed_data)
```

```python
def data_access_layer(data):
    retrieved_data = retrieve_data(data)
    return retrieved_data
```

**Naan & Pop namespace structure (preserved verbatim):**

```text
com.naanpop.orderapp.presentation

com.naanpop.orderapp.workflow

com.naanpop.orderapp.model

com.naanpop.orderapp.persistence
```

**Physical architecture variations:**
- **Single-tier (embedded/mobile)** — all layers in one process; constrained environments
- **Two-tier (client/server)** — UI separated from database; medium scalability, simple
- **Three-tier (web)** — UI, business logic, database as separate tiers; highest scalability, most complex

**The domain smearing problem:** Logical components (organized by domain behavior) don't naturally map to layers (organized by technical concern). The system must decompose domain components into technical concerns. A single domain change (e.g., adding pizza to the menu) may require changes across multiple layers — that's why pizza in Naan & Pop touches presentation (new menu category), workflow (new customization rules), persistence (new schema), and promotion (new item eligibility).

**Do:**
- Choose layered when time-to-market dominates, the team is small, the domain is not expected to change much, and the work maps cleanly to MVC.
- Add layers (e.g., integration) only when *every* request needs to pass through them.
- Use this style for small bakeries, throwaway systems, and projects that just need to work.
- Recognize feasibility and quick-to-build as superpowers.

**Don't:**
- Don't use layered for systems with frequent domain changes — the domain gets smeared across layers.
- Don't assume layered means "simple forever" — as the system grows, scalability and deployability become painful.
- Don't expect a 500-feature monolith to keep its layered elegance without strong governance.

**Layered star ratings:**

| Characteristic | Rating |
|---|---|
| Overall agility | ★ |
| Ease of deployment | ★ |
| Testability | ★ |
| Performance | ★ |
| Scalability | ★ |
| Ease of development | ★★★★ |

**Superpowers:** Feasibility, technical partitioning, performance (in-process calls), quick to build.
**Kryptonite:** Scalability, elasticity, deployability, testability, big ball of mud.

*Ref: Head First Software Architecture.md — "Layered Architecture" / "Drivers for layered architecture" / "Domains, components, and layers" / "Translating layers into code" / "Layering it on" / "Layers, meet the real world: Physical architectures" / "Physical architecture trade-offs" / "One final caveat about domain changes" / "Layered architecture superpowers" / "Layered architecture kryptonite" / "Layered architecture star ratings"*

---

### 11. Use Modular Monoliths for Domain-Heavy Monoliths

**Principle:** A modular monolith is a single deployment partitioned by business subdomain. Each module encapsulates its own domain logic and often its own data, but they ship together. It is the best of both worlds when distributed deployment is not yet needed.

**Why modular monoliths?**
- **Better alignment with business concerns** — changes to a domain are contained within a single module
- **Better team autonomy** — teams can own entire domain modules
- **Easier evolution** — modules can be independently refactored
- **Path to microservices** — well-defined module boundaries make it easier to extract services later

**The burger metaphor:** A modular monolith is like biting through a burger vertically — you don't organize the application in horizontal layers separated by technical concern, but in vertical slices scoped by business concern. Each vertical slice aligns with a piece of the domain and is encapsulated in a module.

**Show me the code (preserved verbatim from the book):**

```text
Flip back to page 192 in the previous chapter and compare these to the namespaces for the layered architecture.
```

A modular monolith is one codebase with code organized in different namespaces; each namespace represents a separate module.

**Keeping modules modular (avoiding the big ball of mud):**
- **Encapsulation** — modules expose clean APIs and hide internal implementation
- **Separate packages/namespaces** — physical separation reinforces logical separation
- **Database separation** — each module should ideally have its own database schema or tables
- **Language features** — Java Platform Module System (JPMS), .NET `internal` keyword
- **Multimodule projects** — break up project into separate folders/subprojects
- **Governance tools** — ArchUnit (Java), ArchUnitNET (.NET)
- **Watch the auto-import IDE feature** — it's too easy to accidentally reference another module

**Taking modularity to the database:**
- **Shared database, separate schemas:** modules share a database instance but have their own schemas
- **Separate databases:** each module has its own database entirely

Shared databases enable joins across modules but create coupling; separate databases require data synchronization but enforce independence.

**Beware of joins:** Database joins across module boundaries create hidden coupling. If Module A joins with Module B's data, changes to Module B's schema can break Module A. Reference other modules by ID, not by foreign key, and fetch details via their API. Copy data via events rather than joining across module tables.

**The Grains of Sand antipattern:** Shared dependencies between modules (just because they share a database) create entanglement. Each module should be treated as a separate service with a public API.

**Do:**
- Choose modular monoliths when the domain is rich, frequent domain change is expected, and operational scaling can wait.
- Treat each module as a separate service: public API, hidden implementation.
- Enforce boundaries with language features, multimodule projects, or governance tools.
- Extend modularity to the database with per-module schemas/tables and avoid cross-module joins.
- Reference other modules by ID, not by foreign key, and fetch details via their API.

**Don't:**
- Don't allow IDE auto-imports to leak references across modules — enforce boundaries.
- Don't perform SQL joins across module tables; copy or sync via events instead.
- Don't share dependencies between modules just because they share a database.

**Modular monolith star ratings:**

| Characteristic | Rating |
|---|---|
| Maintainability | ★★★ |
| Testability | ★★★ |
| Deployability | ★★★ |
| Simplicity | ★★★★ |
| Evolvability | ★★★ |
| Performance | ★★★ |
| Scalability | ★ |
| Elasticity | ★ |
| Fault Tolerance | ★ |
| Overall Cost | $$ |

**Superpowers:** Domain-aligned organization, team autonomy, path to microservices, simpler than distributed, performance (in-process calls).
**Kryptonite:** Hard to reuse, single set of architectural characteristics, fragile modularity, operational characteristics limited.

*Ref: Head First Software Architecture.md — "Modular Monoliths" / "Why modular monoliths?" / "Show me the code!" / "Keeping modules modular" / "Taking modularity all the way to the database" / "Beware of joins" / "Modular monolith superpowers" / "Modular monolith kryptonite" / "Modular monolith star ratings"*

---

### 12. Use Microkernel Architecture for Customization and Extensibility

**Principle:** A microkernel architecture has a stable core system and one or more plug-in modules that customize behavior. It is the world champion of customization when changes are isolated to plug-ins.

**The two parts:**
- **Core System:** contains the essential, unchanging business logic; defines extension points (contracts) that plug-ins implement
- **Plug-in Components:** independent modules that extend the core; each plug-in implements a specific contract and can be added, removed, or updated independently

**Spectrum of microkern-ality:** Evaluate by how functional the core is without plug-ins (Eclipse IDE = pure; web browser = minimal) and how volatile the core is (low volatility = better fit). Examples:
- **Eclipse IDE** — pure microkernel; facilitates languages and tools via plugins
- **Insurance application** — medium microkern-ality; standard rules with customization
- **Web browser** — works fine without plugins (low microkern-ality)
- **Linter (e.g., ESLint)** — pure microkernel for parsing source code
- **Jenkins CI** — works standalone, supports plugins for extensibility

**Plugin communication:**
- **Point-to-point** — core calls a specific plug-in
- **Publish-subscribe** — core publishes events, plug-ins respond
- **Registry pattern** — central registry tracks available plug-ins

**Encapsulated (monolithic) vs. distributed plug-ins:**

|  | Encapsulated (Monolithic) | Distributed |
|---|---|---|
| Pros | Best performance (in-process calls) | Better scalability, language diversity |
| Cons | Limited scalability, single language | Network overhead, more complex |
| Deployment | Core and plugins in one unit | Plugins deployed separately |
| Communication | Synchronous calls (in-process) | Sync (REST) or async (messaging) |

**Plugin contracts:**
- **Input contracts** — what data the plug-in expects
- **Output contracts** — what data the plug-in returns
- **Behavioral contracts** — what the plug-in promises to do

**Inter-plugin communication:** Generally avoid. When plug-ins must communicate, the core should mediate and manage versioning. Eclipse's complexity is a cautionary tale — when plug-ins talk to each other freely, dependency nightmares follow.

**Do:**
- Choose microkernel for systems where the core rarely changes but customization is constant (device assessment, insurance rules, IDEs, linters, CI servers, payment integrations).
- Define clear plug-in contracts and version them carefully.
- Use encapsulated (monolithic) or distributed plug-ins based on operational needs.
- Use synchronous calls when response must be quick; asynchronous when fire-and-forget works.
- Avoid letting plug-ins talk directly to each other — the core should mediate.

**Don't:**
- Don't let the core change frequently — misaligned volatility is the most common microkernel failure.
- Don't share dependencies between plug-ins — it creates hidden coupling.
- Don't allow plug-in-to-plug-in communication without explicit mediation.

**Microkernel star ratings:**

| Characteristic | Rating |
|---|---|
| Maintainability | ★★★ |
| Testability | ★★★ |
| Deployability | ★★★ |
| Simplicity | ★★★★★ |
| Evolvability | ★★★ |
| Performance | ★★★ |
| Scalability | ★ |
| Elasticity | ★ |
| Fault Tolerance | ★ |
| Overall Cost | $ |

**Superpowers:** Customization, extensibility, testability, deployment flexibility.
**Kryptonite:** Plugin complexity, contract versioning, limited scalability, plugin interdependency.

*Ref: Head First Software Architecture.md — "Microkernel Architecture" / "The two parts of microkernel architectures" / "The spectrum of microkern-ality" / "Encapsulated versus distributed plugins" / "Plugin communication" / "Plugin contracts" / "Microkernel superpowers" / "Microkernel kryptonite" / "Microkernel star ratings"*

---

### 13. Apply Microservices for Independent Scaling and Agility

**Principle:** A microservice is a single-purpose, separately deployed unit of software that does one thing really well. Microservices require *physical bounded contexts* (each service owns its data) and *cross-functional teams*.

**What's a microservice?** The prefix *micro* refers to *what the service does*, not physical size. A Monitor Heart Rate service is single-purpose and does one thing really well.

**It's my data, not yours:** Each microservice is the *only* one that can directly access its data. If other services need that data, they must ask. This is a *physical bounded context*.

**Granularity — how micro is "micro"?**

**Granularity disintegrators (reasons to make services smaller):**
- **Cohesion** — if functionalities lack cohesion, break apart
- **Fault tolerance/availability** — failures in one part shouldn't affect others
- **Access control** — sensitive data isolated in its own service
- **Code volatility** — fast-changing parts isolated for safer deploys
- **Scalability/throughput** — parts with different throughput needs scale independently

**Granularity integrators (reasons to make services bigger):**
- **Database transactions** — operations requiring transactional consistency are simpler in one service
- **Data dependencies** — highly coupled data (foreign keys, related entities) is hard to break apart
- **Workflow/choreography** — tightly coupled workflows are simpler in a single service

> Make it Stick: Keep them coarse-grained when you begin, then move to fine-grained for the win!

**Sharing functionality:**

| Approach | Pros | Cons |
|---|---|---|
| **Shared service** | No version conflicts; cross-language; one place to change | Network latency, single point of failure, scales when callers scale |
| **Shared library** | Better performance, availability, scalability, fault tolerance; versioned for backward compatibility | One library per language; must retest/redeploy when changed |

**Code preserved verbatim:**

```java
package monitorme.common;

Temperature

public class AlertNurse {
    public static void sendAlert(AlertType type, String data) {
        ...
    }

"41 degrees Celsius"
```

**Managing workflows:**

| Pattern | Pros | Cons |
|---|---|---|
| **Orchestration** (central conductor) | Centralized workflow, easy to understand, clear error handling, easy workflow state | Bottleneck, single point of failure, tight coupling to orchestrator |
| **Choreography** (services dance together) | Loose coupling, high responsiveness, independent scalability | Complex error handling, hard restart/recovery, distributed state management |

The Front Controller antipattern occurs when a choreography "service" quietly becomes the orchestrator. Watch for it.

**Conway's Law:** Microservices architecture requires cross-functional teams. Each team owns its own group of microservices, all the way from the UI to the database. Technically partitioned teams (UI devs, backend devs, DBAs) cannot build microservices effectively.

**Do:**
- Choose microservices when you need independent scalability, fault isolation, technology diversity, and high deployment frequency.
- Start coarse-grained and split later as forces become clear.
- Balance granularity disintegrators against granularity integrators.
- Use physical bounded contexts: each service is the *only* one that writes its data; others must ask.
- Default to **choreography**; introduce **orchestration** only when explicit control is needed.
- Use the shared library approach for performance-critical shared code.

**Don't:**
- Don't pick microservices as the default for small systems — the complexity tax is too high.
- Don't share a database across services; that violates the physical bounded context.
- Don't decompose a tightly coupled workflow into many small services — it becomes distributed mud.
- Don't allow technically partitioned teams to build microservices.
- Don't use orchestration just because it looks centralized.

**Microservices star ratings:**

| Characteristic | Rating |
|---|---|
| Maintainability | ★★★★ |
| Testability | ★★★★ |
| Deployability | ★★★★ |
| Simplicity | ★ |
| Evolvability | ★★★★ |
| Performance | ★★ |
| Scalability | ★★★★★ |
| Elasticity | ★★★★ |
| Fault Tolerance | ★★★★ |
| Overall Cost | $$$$$ |

**Superpowers:** Independent scalability, fault isolation, independent deployment, technology diversity, evolvability.
**Kryptonite:** Complexity, performance (network overhead), data consistency, operational overhead, monolithic databases that can't be broken, semantic coupling.

*Ref: Head First Software Architecture.md — "Microservices Architecture" / "What's a microservice?" / "It's my data, not yours" / "How micro is 'micro'?" / "Granularity disintegrators" / "Granularity integrators" / "It's all about balance" / "Sharing functionality" / "Code reuse with a shared service" / "Code reuse with a shared library" / "Managing workflows" / "Orchestration: Conducting microservices" / "Choreography: Let's dance" / "Microservices architecture superpowers" / "Microservices architecture kryptonite" / "Microservices star ratings"*

---

### 14. Use Event-Driven Architecture for High-Throughput, Decoupled Systems

**Principle:** Event-driven architecture (EDA) is built on **events** (broadcast notifications of things that have already happened), **asynchronous communication** (fire-and-forget), and **event processors** (services of any size that react to events).

**Restaurant metaphor:** If one person takes orders, cooks food, and makes shakes sequentially, the restaurant can only serve a few customers per hour. If different people handle different tasks simultaneously (asynchronously), throughput increases dramatically. That's EDA.

**What is an event?**
- Events are facts — "Order placed," "payment received," "item shipped"
- Events are immutable — once an event occurs, it cannot be changed
- Events are decoupled — the producer doesn't know who consumes the event

**Events vs. messages:**

| Aspect | Events | Messages |
|---|---|---|
| Direction | Broadcast (one-to-many) | Directed (one-to-one) |
| Mechanism | Topics | Queues |
| Timing | Something that has already happened | Request for something to happen |
| Response | None expected | May expect response |
| Coupling | Loose | Tighter |

**Initiating and derived events:**
- **Initiating events** — triggered by external actors (user actions, sensor readings, time triggers)
- **Derived events** — generated by the system as a result of processing other events (e.g., "order validated" derived from "order placed")

Any action a service performs should trigger a derived event to provide *architectural extensibility* — the ability to extend the system by adding new consumers without changing producers.

**Asynchronous communication (fire-and-forget):** Services don't wait for a response. Architects use a dotted line to represent async communication between services and a solid line for sync communication.

**When to use asynchronous vs. synchronous:**

| Use async when… | Use sync when… |
|---|---|
| High throughput requirements | Real-time response requirements |
| Decoupled processing | Complex request-response patterns |
| Parallel execution of independent tasks | Caller needs an immediate answer |
| Variable load | Real-time decisions |

**Database topologies:**

| Topology | Coupling | Best for |
|---|---|---|
| **Monolithic database** | Loose service coupling, simple | Low-scale, simple systems |
| **Domain-partitioned databases** | Balance | Moderate scale with natural domain boundaries |
| **Database-per-service** | Tight bounded contexts, expensive | Services that truly own their data |

**EDA vs. microservices:**
- Microservices define how services are structured and deployed (single-purpose, physical bounded contexts)
- EDA defines how services communicate (asynchronous, broadcast events)
- They can be combined: event-driven microservices use async event communication within a microservices architecture

**Do:**
- Choose EDA for high-throughput, parallel, decoupled systems (online ordering, social media, IoT).
- Treat events as immutable facts; use initiating and derived events.
- Match database topology to your coupling budget.
- Use **event-driven microservices** as a hybrid combining the best of both.
- Validate EDA when the workflow has many parallel actions with limited synchronous dependencies.

**Don't:**
- Don't try to make EDA work when most actions are synchronous — it underperforms.
- Don't choose EDA for low-scale simple systems — complexity overhead dominates.
- Don't let database coupling undermine the decoupling.
- Don't confuse events with messages.

**EDA star ratings:**

| Characteristic | Rating |
|---|---|
| Maintainability | ★★★★ |
| Testability | ★★ |
| Deployability | ★★★ |
| Simplicity | ★ |
| Evolvability | ★★★★ |
| Performance | ★★★★ |
| Scalability | ★★★★ |
| Elasticity | ★★★ |
| Fault Tolerance | ★★★★ |
| Overall Cost | $$$ |

**Superpowers:** High performance, high scalability, loose coupling, extensibility.
**Kryptonite:** Complexity, error handling, data consistency (eventual), workflow management (sagas needed).

*Ref: Head First Software Architecture.md — "Event-Driven Architecture" / "What is an event?" / "Events versus messages" / "Initiating and derived events" / "Asynchronous communication" / "Fire-and-forget" / "Database topologies" / "EDA versus microservices" / "Hybrids: Event-driven microservices" / "Event-driven architecture superpowers" / "Event-driven architecture kryptonite" / "Event-driven architecture star ratings"*

---

### 15. Match Style to Problem Domain (Decision Process)

**Principle:** Architectural style selection is a five-step process that must precede coding.

1. **Identify architectural characteristics** (3–5 driving, with implicit candidates)
2. **Identify logical components** (workflow or actor/action)
3. **Choose an architectural style** using the four-dimension model and star-rating charts
4. **Document your decision** in an ADR with context, decision, and consequences
5. **Diagram your architecture** at the appropriate level of detail

**Style selection matrix (problem domain → recommended style):**

| Problem Type | Recommended Style | Why |
|---|---|---|
| Small bakery taking online orders | **Layered** | Simple problem, small scale, time-to-market |
| Modular, domain-rich, infrequent change | **Modular monolith** | Domain partitioning without distributed complexity |
| High scalability and independence | **Microservices** | Independent scaling, fault isolation |
| High throughput, parallel processing, broadcast | **EDA** | Async, decoupled, fire-and-forget |
| Customization and isolation | **Microkernel** | Stable core + plugins for customization |
| International wire transfers overnight | **Modular monolith** | Rich domain, doesn't need scalability or elasticity |
| Standardized testing for 200K students | **Microservices** | Independent scaling, elasticity, fault tolerance |

**Do:**
- Use the star-rating sheet for each style (1–5 stars per characteristic).
- Verify that the chosen style's superpowers match the system's driving characteristics.
- Verify that the style's kryptonite does not align with the system's driving characteristics.
- Reject "shiny object syndrome" (picking microservices because it's fashionable).

**Don't:**
- Don't pick a style by counting votes in a group without driving characteristics.
- Don't pick a style because it's fashionable; pick it because its philosophy fits.
- Don't ship code before completing the five-step process.

*Ref: Head First Software Architecture.md — "Do It Yourself: The TripEZ Travel App" / "Do It Yourself: Testing Your Knowledge" / "Architectural Styles — Categorization and Philosophies"*

---

### 16. Use Trade-off Analysis and Star-Rating Sheets

**Principle:** A reusable trade-off template compares pros and cons of each candidate style against the system's driving characteristics.

**Trade-off analysis steps:**
1. Identify the options
2. Evaluate each option's benefits and costs
3. Consider the context (requirements, constraints)
4. Make a decision
5. Document the decision (ADR)

**Distribution trade-off table (synchronous vs. asynchronous communication):**

|  | Synchronous | Asynchronous |
|---|---|---|
| Coupling | Tight (caller knows callee) | Loose (caller doesn't know consumers) |
| Latency | Caller blocks until response | Caller continues immediately |
| Error handling | Immediate response, easy error propagation | Deferred, requires compensating actions |
| Complexity | Simpler conceptually | Harder to debug and trace |
| Throughput | Limited by slowest service in chain | High (parallel processing) |
| Consistency | Strong (immediate state propagation) | Eventual |
| Use when | Real-time response, immediate decisions | Fire-and-forget, high throughput, decoupling |

**Communication pattern selection:**
- **Use synchronous** when the caller needs an immediate response or value
- **Use asynchronous** when fire-and-forget is acceptable, throughput matters, or decoupling is required
- **Use queues** when point-to-point is required
- **Use topics** when broadcast is required
- **For microservices workflows**: default to choreography; introduce orchestration only when central state and control are required
- **For events**: never wait for a response; never expect a specific consumer; never confuse with messages

**Do:**
- Use the book's star-rating sheets (1 star = poor support, 5 stars = strong support) for: maintainability, testability, deployability, simplicity, evolvability, performance, scalability, elasticity, fault tolerance, overall cost.
- Compare ratings against the driving characteristics of your system.
- Use trade-off analysis for binary decisions like queues vs. topics, sync vs. async, shared service vs. shared library.

**Don't:**
- Don't accept "this is what we always do" as a valid trade-off.
- Don't treat any decision as having no consequences.
- Don't pick a style whose kryptonite matches a driving characteristic.

*Ref: Head First Software Architecture.md — "Analyzing trade-offs" / "The first law of software architecture" / "It always comes back to trade-offs" / "Microservices star ratings" / "Layered architecture star ratings" / "Modular monolith star ratings" / "Microkernel star ratings" / "Event-driven architecture star ratings"*

---

### 17. Combine Styles for Hybrid Architectures

**Principle:** Real systems often combine multiple architectural styles. The book explicitly endorses hybrid architectures.

**Event-driven microservices (most common hybrid):**
- Services are independently deployable (microservices)
- Services communicate via events (EDA)
- Each service owns its own data (microservices)
- Events enable loose coupling and parallel processing (EDA)

**Other hybrid patterns:**
- Microkernel inside a monolith for stable cores with plug-in extensibility
- Microkernel UI on top of an event-driven backend when the UI is the most volatile layer
- Modular monolith for the core domain, with microservices for specific high-scaling functions

**When to hybridize:** When one style doesn't fit the entire system — different parts have different driving characteristics (e.g., high-throughput checkout vs. low-throughput admin).

**Do:**
- Combine microservices and event-driven architecture for systems that need both bounded contexts and asynchronous decoupling.
- Use the microkernel style inside a monolith for stable cores with plug-in extensibility.
- Layer a microkernel UI on top of an event-driven backend when the UI is the most volatile layer.
- Verify that the hybrid still addresses the critical architectural characteristics.
- Document the hybrid in an ADR.

**Don't:**
- Don't be dogmatic about a single style when a hybrid fits better.
- Don't combine styles without understanding each component's role.
- Don't add styles that don't serve a driving characteristic.

*Ref: Head First Software Architecture.md — "Hybrids: Event-driven microservices" / "Do It Yourself: Testing Your Knowledge" / "Microkernel superpowers" / "Event-driven microservices"*

---

### 18. Translate "Business Speak" into Architectural Characteristics

**Principle:** Architects translate plain-English business requirements into measurable architectural characteristics.

| Business statement | Architectural characteristic |
|---|---|
| "Lafter is constantly changing to meet new marketplace demands." | Modularity, extensibility |
| "We must perform well but also recover quickly in case of error." | Performance, recoverability |
| "Due to new regulatory requirements, we must complete end-of-day processing on time." | Recoverability, scalability |
| "The ability to update your résumé." | Résumé-ability (figurative; demonstrates hidden characteristics) |
| "Our plan is to engage heavily in mergers and acquisitions in the next three years." | Interoperability, integratability |
| "We have a very tight time frame and a fixed budget." | Simplicity, feasibility |
| "Nobody should ever ask for whether something is possible." | Feasibility-evaluating |

**The F-16 story:** In the 1970s, the US Air Force required the F-16 to fly at Mach 2.5. Technology couldn't deliver. They went back and asked "why?" — the answer was "we want it to be able to flee a fight." The result: F-16 max speed Mach 2.1, but the most maneuverable and fastest-accelerating jet ever created. Lesson: when users bring solutions, imitate an annoying toddler and keep asking "but why?" to uncover the actual requirements.

**Solutions vs. requirements:**
- "We need a system to track user preferences and save them between sessions." → **Requirement** (what they want to achieve)
- "Do we really need to build our own survey service?" → **Requirement** (questioning the approach)
- "An enterprise service bus would solve our current problems" → **Solution** (proposing a tool)
- "This software package does all the things accounting needs" → **Solution** (recommending a tool)

**Do:**
- Treat every business requirement as a potential source of hidden architectural characteristics.
- Question the user's solution; ask "but why?" repeatedly until you reach the underlying need.
- Use examples like the F-16 Mach 2.5 story to teach the pattern of "solutions vs. requirements."

**Don't:**
- Don't accept business statements at face value.
- Don't skip the "why?" questioning even when you think you know.

*Ref: Head First Software Architecture.md — "Lost in translation" / "Solutions versus requirements"*

---

### 19. Diagramming Techniques

**Principle:** Architecture diagrams illustrate structure, topology, communication, dependencies, and integration points. They are complementary to ADRs (ADRs capture the analysis and decision; diagrams capture the structure).

**Best practices:**
- **Keep it simple** — don't try to include every detail; suffer from the "hairball effect" if you do
- **Always include a title** — make the view or perspective explicit
- **Use unidirectional arrows** — double-headed arrows are ambiguous (two-way communications vs. default arrow)
- **Use real labels, not acronyms** — only insiders understand acronyms; spell things out
- **Use solid lines for sync and dotted for async** — solid line = synchronous; dotted = asynchronous
- **Use consistent shapes and colors** — consistent shapes cut down on visual noise
- **Always include a key** — the only universal shape is the database cylinder; add a key for everything else
- **Color-code by ownership** — event handler written and maintained by internal team; external system accessed through a standard API; operational database

**Diagram key conventions (preserved from the book):**

| Element | Convention |
|---|---|
| User interface | Computer screen |
| Component | Rounded box (matches logical components) |
| Layer | Box (matches architectural layers) |
| Database | Cylinder (universal) |
| Synchronous call | Solid line with single-headed arrow |
| Asynchronous call | Dotted line |
| Event handler (internal) | Distinct color/shape |
| External system (standard API) | Distinct color/shape |

**Do:**
- Sketch a high-level physical view showing UIs, services, databases, communication types, and how they all connect.
- Annotate diagrams to clarify points or describe things.
- Use the book's diagramming key conventions consistently.

**Don't:**
- Don't create comprehensive diagrams that include every detail.
- Don't use double-headed arrows.
- Don't assume acronyms are universally understood.

*Ref: Head First Software Architecture.md — "Diagramming techniques" (Appendix #4)*

---

### 20. Practice Architectural Thinking with Katas

**Principle:** Architectural skill is developed through deliberate practice, katas, and exposure to multiple business domains.

**Architectural katas:** Simulate the process of designing a real architecture. Intended for several small groups of 3–5 people (odd numbers so disputes can be decided by majority). Each group becomes a project team and works on a different kata. People who work together in the real world should not be on the same teams — this stresses collaborating with other architects you don't already know.

**How to run katas:**
1. **Preparation** — gather supplies (poster paper, whiteboards); a kata can take 45 minutes or several weeks
2. **Discussion** — teams work through the exact process outlined in the book: analyzing architectural characteristics, determining logical components, choosing an architectural style, documenting their decisions
3. **Presentation** — each team presents its solution and answers questions; listening teams ask balanced questions (don't focus only on the good or only on the deficiencies)

**Do:**
- Practice with katas: groups of 3–5 people work a realistic architecture problem end-to-end.
- Build knowledge depth (mastery in one or more technologies) and knowledge breadth (awareness of many solutions and their trade-offs).
- Stay technical by writing proof-of-concept code, paying down technical debt, and joining outage response.
- Read existing architectures with a critical eye — match their style to the problem they solve.

**Don't:**
- Don't pick teams based on existing working relationships.
- Don't let katas become theoretical exercises without concrete artifacts (diagrams, ADRs).

*Ref: Head First Software Architecture.md — "Practicing architecture with katas" (Appendix #6) / "How to run katas"*

---

### 21. Be a Coding Architect (Stay Technical)

**Principle:** Software architects should still write source code. Not only does it help maintain technical skills, but it also shows how architectural decisions play out in real life.

**How to balance hands-on coding with architecture:**
- **Don't become a bottleneck** — be careful not to take ownership of code on the product's critical path
- **Write proof-of-concept code** — having trouble making an architectural decision? Write code to demonstrate each option
- **Pay down technical debt** — help your team out; if you get called away, it won't hold them up
- **Get involved during production outages** — step in to assist; see the detailed implementation of your architecture
- **Do lots of code reviews** — stay involved, ensure source code stays aligned with architectural decisions

**Knowledge pyramid (junior → senior → architect):**

| Stage | "Stuff you know" | "Stuff you know you don't know" | "Stuff you don't know you don't know" |
|---|---|---|---|
| Junior developer | Small | Large | Hidden |
| Senior developer / tech lead | Large | Growing | Smaller |
| Architect | Deep in specialty | Broad awareness | Smaller still (cultivate diverse exposure) |

**Do:**
- Stay deep in your specialty while broadening across technologies.
- Don't become a purely theoretical architect who never writes code.
- Don't become a coding bottleneck on the product's critical path.

**Don't:**
- Don't lock yourself into a single technology stack; explore broadly.
- Don't stop doing code reviews.

*Ref: Head First Software Architecture.md — "The Coding Architect" (Appendix #1) / "Knowledge depth versus breadth" (Appendix #5) / "Expectations for Architects" (Appendix #2)*

---

### 22. Communicate, Lead, and Navigate Office Politics

**Principle:** At least half of architecture is people work. The book devotes significant attention to soft skills: "demonstrate, don't discuss," "know when to fight and when to let go," "focus on business value," "involve developers," "divide and conquer."

**Soft skill techniques:**
- **Demonstrate, don't discuss** — rather than arguing, *demonstrate* in a production-like environment. Say it: "Demonstration defeats discussion."
- **Know when to fight and when to let go** — fight to the death for something crucial; let things go if they're not so important. Choosing your battles gains respect.
- **Focus on business value** — business stakeholders care about time to market, regulatory compliance, mergers and acquisitions. Translate technical concerns into business ones.
- **Involve developers in decisions** — Rule #1: if developers don't know *why*, they're less likely to agree. Rule #2: if developers aren't *involved*, they're less likely to follow. Use ADRs with RFC status to invite feedback.
- **Divide and conquer** — Sun Tzu: "If your enemy's forces are united, separate them." Dividing monolithic requirements into parts with different characteristics makes negotiation easier.
- **Keep things simple, clear, and concise** — the "four Cs of architecture": be **C**lear, be **C**oncise, **C**ommunicate, **C**ollaborate.
- **Be available to your team** — keep mornings or afternoons open for collaboration.

**Expectations for architects (regardless of title):**
- Make architectural decisions
- Keep current with the latest trends
- Continually analyze the architecture (architectural vitality)
- Ensure compliance with the architecture (architectural governance)
- Cultivate diverse exposures (know a little about a lot)
- Possess exceptional interpersonal skills (Gerald Weinberg: "No matter how it looks at first, it's always a people problem")
- Know the business domain
- Understand and navigate office politics

**Do:**
- Demonstrate decisions in production-like environments; "demonstration defeats discussion."
- Choose your battles — fight for what's critical, let go of the rest.
- Translate technical concerns into business value for stakeholders.
- Use ADRs to involve developers (RFC status invites feedback).
- Divide and conquer: split monolithic requirements into parts with different characteristics.
- Be available to your team: keep mornings or afternoons open for collaboration.
- Cultivate diverse exposure: know a little about a lot of things.

**Don't:**
- Don't use jargon and acronyms to confuse rather than inform.
- Don't rely solely on diagrams — some decisions need conversation.
- Don't ignore office politics.

*Ref: Head First Software Architecture.md — "The Soft Skills of Architecture" (Appendix #3) / "Expectations for Architects" (Appendix #2) / "Know the business domain" / "Understand and navigate office politics"*

---

## Anti-Patterns & Common Mistakes

- **Entity trap:** Modeling components after domain entities ("BidManager") bundles too much responsibility. → *Fix:* name by responsibility, not entity; watch for words like "manager," "supervisor," "handler," "processor."
- **Big ball of mud:** A monolithic or distributed system where every component depends on every other. → *Fix:* enforce boundaries with layering, modularity, or bounded contexts.
- **Grains of Sand:** Microservices that are too fine-grained, generating excessive network chatter. → *Fix:* start coarse, split only when forces demand.
- **Two-headed architecture:** Architecture diagrams without clear relationships, leaving "what does it look like?" unanswered. → *Fix:* draw semantic lines and label them with unidirectional arrows.
- **Entity decomposition:** Choosing "OrderManager" or "CustomerService" as a component because of its noun. → *Fix:* "Name that component" exercise — use verbs and responsibilities, not entity names.
- **In-document ADR comments forever:** Letting comments pile up on ADRs. → *Fix:* disable in-document comments after release; move discussion to issues or chat.
- **Editing an Accepted ADR:** Changing an accepted decision. → *Fix:* supersede with a new ADR; preserve history.
- **Skip the consequences section:** Pretending a decision has no trade-offs. → *Fix:* every architectural decision has consequences — document them.
- **Microservices-by-default:** Reaching for microservices for a small bakery. → *Fix:* start with modular monolith or layered; evolve when forces demand.
- **Bimodal IT / two-speed architecture:** Front-end fast, back-end slow. → *Fix:* align system rates; modern companies know one speed.
- **Sync everything:** Using REST for every communication in microservices. → *Fix:* introduce queues, events, and backpressure for throughput.
- **Shared database across services:** Violates the physical bounded context. → *Fix:* per-service database, copy via events or API.
- **Plug-ins talking to each other:** Versioning and dependency nightmare. → *Fix:* core mediates all inter-plug-in communication.
- **Event-vs-message confusion:** Broadcasting a message (directed) or sending an event to a single consumer. → *Fix:* events are immutable facts broadcast to many; messages are commands or requests directed to one.
- **Front Controller antipattern:** A choreography "service" that quietly becomes an orchestrator. → *Fix:* explicitly mark orchestrators as orchestrators; keep choreography pure.
- **Oracle-style architect:** "All-knowing" architect who makes decisions from filtered information. → *Fix:* stay close to the engine room, observe consequences, and combine personas (Matrix, Gardener, Guide, Superglue).
- **Watermelon status:** "Green" status with red reality. → *Fix:* live dashboards, hard data, fast feedback loops.
- **Layered "domain changes" pain:** A new menu category (e.g., pizza) forces changes across all layers. → *Fix:* migrate to modular monolith when domain changes become routine.
- **Theoretical architect:** No code, no recent context, no observed consequences. → *Fix:* write proof-of-concept code, do code reviews, join outage response.
- **Boiler-pressure transformation:** Throwing more resources at the old engine instead of redesigning. → *Fix:* change processes, organization, and technology together.
- **Sinkhole anti-pattern:** Requests passing through layers without adding value. → *Fix:* only add layers if every request passes through them.
- **Cross-module SQL joins:** Hidden coupling that breaks module boundaries. → *Fix:* reference by ID, fetch details via API.
- **Ignoring business context:** Picking a style by fashion rather than by driving characteristics. → *Fix:* derive style from characteristics and components.
- **Accepting "best practices" without context:** The First Law warns there are no best practices. → *Fix:* analyze trade-offs for every decision.
- **Auto-import dependency leaks:** IDE features that inadvertently reference other modules. → *Fix:* enforce boundaries with language features (JPMS, `internal`), multimodule projects, or governance tools (ArchUnit).

---

## Decision Heuristics / Checklists

### Architecture Significance Checklist

- Does the decision affect multiple components, teams, or stakeholders?
- Is the decision hard or expensive to reverse?
- Does the decision involve significant trade-offs?
- Does the decision impact architectural characteristics?
- Does the decision influence system structure?
- If "no" to all, the decision is design, not architecture.

### ADR Mandatory Checklist

- Three-digit title prefix and noun-heavy description
- Status with the supersedes relationship when applicable
- Context explaining forces and constraints (not the decision itself)
- Decision with active-voice justification ("We will use…")
- Consequences with both positives and negatives (honest trade-offs)
- Governance mechanism (how compliance is ensured)
- Notes with author, approval date, approver, modification log
- Stored in version control, separate from source code if possible
- Reviewed with developers before marking Accepted
- Active-voice writing in the Decision section

### Architecture Style Selection Checklist

- Did you identify 3–5 driving characteristics first?
- Did you list 2–3 candidate styles with superpowers, kryptonite, and star ratings?
- Did you reject "shiny object syndrome" (picking a style because it is fashionable)?
- Did you verify the chosen style's superpowers match the driving characteristics?
- Did you verify the chosen style's kryptonite does not align with the driving characteristics?
- Did you consider a hybrid architecture when one style does not fit?
- Did you produce a star-rating comparison for at least two candidates?
- Did you place the styles in the partitioning × deployment matrix?

### Architectural Characteristics Checklist

- Are characteristics measurable? (Decompose composites like "performance" → "first contentful paint")
- Are they non-domain design considerations?
- Do they influence architectural structure?
- Are they critical or important to application success?
- Are they synergistic with one another?
- Are they limited to 3–5 driving, with implicit candidates?
- Did you derive them from the problem domain, environmental awareness, and holistic knowledge?
- Did you translate business speak into architectural terms?

### Component Identification Checklist

- Workflow approach: did you cover major workflow steps with at least one component each?
- Actor/action approach: did you list each actor's primary actions before grouping?
- Did you assign every requirement to a component?
- Did you split or merge components based on characteristics in Step 4?
- Did you avoid entity decomposition (no "Manager" components)?
- Did you name components by responsibility, not entity?
- Did you perform all four steps (initial components, assign requirements, analyze roles, analyze characteristics)?
- Did you check for cohesion (all of a component's operations related)?

### Coupling Checklist

- Compute afferent (Ca), efferent (Ce), and total (CT) coupling for each component
- Avoid Law of Demeter violations (no `a.getB().getC().doSomething()` chains)
- Move outliers to new components rather than overloading existing ones
- Apply cohesion check: are all of a component's operations related?
- For microservices: ensure no shared databases; use physical bounded contexts
- Use unidirectional arrows in diagrams; use dotted for async, solid for sync

### Communication Pattern Selection Checklist

- Use synchronous communication when the caller needs an immediate response or value
- Use asynchronous communication when fire-and-forget is acceptable, throughput matters, or decoupling is required
- Use queues when point-to-point is required
- Use topics when broadcast is required
- For microservices workflows: default to choreography; introduce orchestration only when central state and control are required
- For events: never wait for a response; never expect a specific consumer; never confuse with messages
- Use solid lines for sync and dotted for async in diagrams

### Database Topology Selection Checklist

- Pick the simplest topology that meets your coupling, fault tolerance, and scalability goals
- Use monolithic database for low-scale, simple systems
- Use domain-partitioned databases for moderate scale with natural domain boundaries
- Use database-per-service when services truly own their data and can afford the cost
- For modular monoliths: avoid cross-module joins; reference by ID, fetch via API

### Hybrid Architecture Checklist

- Does the hybrid address every driving characteristic?
- Does each style's role in the hybrid make sense?
- Are the boundaries between styles clear?
- Is the team structure (Conway's Law) compatible with the hybrid?
- Have you documented the trade-offs in an ADR?

### Coding Architect Checklist

- Are you writing code that does not block the team's critical path?
- Are you writing proof-of-concept code for architectural decisions?
- Are you doing code reviews to stay close to implementation?
- Are you participating in production outage response?
- Are you paying down technical debt?
- Are you staying deep in your specialty while broadening across technologies?

### Soft Skills Checklist

- Are you demonstrating decisions rather than arguing them?
- Are you choosing which battles to fight?
- Are you focusing on business value when speaking with stakeholders?
- Are you involving developers in decisions?
- Are you dividing monolithic requirements into parts with different trade-offs?
- Are you keeping the four Cs of architecture: Clear, Concise, Communicate, Collaborate?
- Are you available to your team (with calendar blocks for collaboration)?
- Are you navigating office politics honestly?

### Diagramming Checklist

- Have you kept the diagram simple (avoiding the "hairball effect")?
- Have you included a title?
- Are all arrows unidirectional?
- Have you used real labels, not acronyms?
- Are solid lines for sync and dotted for async?
- Are shapes and colors consistent?
- Have you included a key?

### Kata Checklist

- Did you form groups of 3–5 people (odd numbers)?
- Did you separate teams who work together in the real world?
- Did you work through the four-step architectural process (characteristics, components, style, ADR)?
- Did you produce concrete artifacts (diagrams, ADRs)?
- Did you present and answer balanced questions from other teams?

---

## Key Takeaways

1. **Architecture has four dimensions** that must all be addressed: characteristics, decisions, components, and style. Skipping any one leaves an incomplete picture.
2. **Architecture and design are a spectrum**, not a binary. Use strategic/effort/trade-off criteria to assign decision ownership.
3. **Everything is a trade-off;** the *why* matters more than the *how* (Two Laws of Software Architecture).
4. **Limit driving characteristics to 3–5**; implicit characteristics stay implicit unless they shape structure.
5. **Characteristics come from three sources**: the problem domain, environmental awareness, and holistic domain knowledge.
6. **Composite characteristics must be decomposed** to be measurable ("performance" → "first contentful paint").
7. **Use ADRs to capture the *why***; make them immutable and supersede rather than edit.
8. **Use the workflow or actor/action approach** to identify components; avoid the entity trap.
9. **Apply the Law of Demeter** to reduce coupling; use cohesion checks to validate components.
10. **Choose a style by matching philosophy to problem**, not by fashion: layered for simple, modular monolith for domain-heavy, microkernel for customization, microservices for independent scaling, EDA for high-throughput async.
11. **Start coarse-grained and split only when forces demand** — avoid the Grains of Sand antipattern.
12. **Default to choreography;** introduce orchestration only when central state and control are required.
13. **Physical bounded contexts are non-negotiable** in microservices; physical data sharing is acceptable in EDA.
14. **Hybrid architectures are valid and common** (event-driven microservices).
15. **Communication style is a major driver**: async for fire-and-forget, sync for immediate response, queues for point-to-point, topics for broadcast.
16. **Diagrams complement ADRs**: ADRs capture analysis and rationale; diagrams capture structure.
17. **Practice with katas** to develop deliberate architectural skill.
18. **Architects must code, demonstrate, and stay close to the engine room** to avoid ivory-tower failures.
19. **At least half of architecture is people work**: soft skills, office politics, and developer involvement are mandatory.
20. **Use the four Cs**: Clear, Concise, Communicate, Collaborate.
21. **Ask "but why?"** repeatedly to translate business speak into architectural characteristics and uncover requirements hidden in solutions.
22. **Use the star-rating sheets** (1–5 stars per characteristic) to compare candidate styles objectively against driving characteristics.

---

## Cross-References

- Related: [[../Software_Architect_Elevator.md]] — the architect's role, communication, and the elevator metaphor
- Related: [[../Crafting_Engineering_Strategy.md]] — strategy, diagnosis, refinement, and operations
- Related: [[../Fundamentals_of_Software_Architecture.md]] — deeper coverage of the same foundational concepts
- Related: [[../Building_Evolutionary_Architectures.md]] — fitness functions and evolutionary change
- Related: [[../Communication_Patterns.md]] — deeper treatment of sync/async communication patterns
- Related: [[../Designing_Distributed_Systems.md]] — distributed architecture patterns
- Related: [[../Building_Microservices_2nd_edition.md]] — microservices in depth
- Related: [[../Building_Event-driven_Microservices.md]] — event-driven microservices in depth
- Related: [[../Cloud_Application_Architecture_Patterns_ER.md]] — cloud architecture patterns
- Related: [[../Building_Micro-Frontends.md]] — micro-frontends as a modular approach
- Topic index: [[../INDEX.md]]

---

## Appendix A: Comprehensive Code & Diagram Reference

### A.1 Layered Architecture Code (Preserved Verbatim from Chapter 6)

**Naan & Pop namespace structure:**

```text
com.naanpop.orderapp.presentation

com.naanpop.orderapp.workflow

com.naanpop.orderapp.model

com.naanpop.orderapp.persistence
```

**The fully qualified names of these layers will appear as packages in Java, namespaces in NET, or whatever namespacing mechanism your language of choice uses.** Like the logical components, the architectural layers use the component implementation of the underlying platform, which often maps to the underlying filesystem.

**Presentation layer (topmost):**

```python
def UI_layer(request):
    data = request.get_data()
    return business_logic_layer(data)
```

The user interface layer, or presentation layer, is responsible for interacting with the user, serving the same purpose as the view part of MVC.

**Workflow / business layer:**

```python
def business_logic_layer(data):
    processed_data = process_data(data)
    return data_access_layer(processed_data)
```

The workflow layer (sometimes called the business rules layer) is responsible for processing each request from the UI layer and returning a response.

**Persistence / data access layer:**

```python
def data_access_layer(data):
    retrieved_data = retrieve_data(data)
    return retrieved_data
```

The persistence layer (or data access layer) is responsible for accessing the data from the database and returning it to the workflow layer.

### A.2 Microservices Sharing Functionality Code (Preserved Verbatim from Chapter 10)

**MonitorMe common alert functionality:**

```java
package monitorme.common;

Temperature

public class AlertNurse {
    public static void sendAlert(AlertType type, String data) {
        ...
    }

"41 degrees Celsius"
```

This is the common alert functionality that all of MonitorMe's vital-sign monitoring microservices share. If we create three separate microservices for monitoring blood pressure, temperature, and heart rate, each one needs this common alert functionality. The decision is where to put the source code for the common alert functionality — a shared service or a shared library.

### A.3 Modular Monolith Namespace Comparison (Preserved Verbatim from Chapter 7)

The book directs readers to compare modular monolith namespaces to the layered architecture namespaces:

```text
Flip back to page 192 in the previous chapter and compare these to the namespaces for the layered architecture.
```

A modular monolith is one codebase with code organized in different namespaces; each namespace represents a separate module. Naan & Pop's namespaces follow this modular structure, with each module encapsulating its own domain logic.

### A.4 Common Modular Monolith Pitfall — Cross-Module Joins

When different tables (perhaps in different schemas) belong to different modules, it's easy to slip up and perform a SQL join across tables belonging to different modules. Then you're back to tight coupling. It's OK to store the IDs of records that belong to one module in another module's tables. For example, the Naan & Pop Order domain is allowed to store "recipe item" IDs in its tables within the order_schema. If it ever needs more information about a particular item, it calls the Recipe module's API and provides it with the recipe item's ID.

> This is not a foreign key reference.

### A.5 Module Boundary Enforcement Mechanisms

A modular monolith's module boundaries are not self-enforcing — they require deliberate mechanisms:

1. **Language features:** Java Platform Module System (JPMS), .NET `internal` keyword, Rust module privacy
2. **Multimodule projects:** Gradle subprojects, Maven modules, separate folders in the repository
3. **Different repositories:** Stitch the complete application together at build time
4. **Architectural governance tools:** ArchUnit (Java), ArchUnitNET (.NET), custom lint rules
5. **Code review discipline:** Catch cross-module references before they ship
6. **Database-level separation:** Per-module schemas, no cross-module joins

---

## Appendix B: Complete ADR Examples

### B.1 Two Many Sneakers — Full ADR Lifecycle

**ADR 012: Initial Decision — Use Queues**

| Section | Content |
|---|---|
| **Title** | 012: Use of queues for asynchronous messaging between order and downstream services |
| **Status** | Accepted |
| **Context** | The trading service must inform downstream services (notification and analytics services, for now) about new items available for sale and about all transactions. This can be done through synchronous messaging (using REST) or asynchronous messaging (using queues or topics). |
| **Decision** | We will use queues for asynchronous messaging between the trading and downstream services. Using queues makes the system more extensible, since each queue can deliver a different kind of message. Furthermore, since the trading service is acutely aware of any and all subscribers, adding a new consumer involves modifying it — which improves the security of the system. |
| **Consequences** | Queues mean a higher degree of coupling between services. We will need to provision queuing infrastructure. It will require clustering to provide for high availability. If additional downstream services (in addition to the ones we know about) need to be notified, we will have to make modifications to the trading service. |

**Three months later:** The requirements changed. The team's latest trade-off analysis reveals that topics would be a better fit. Everyone has signed off.

**ADR 012 status update:**

| Field | New Value |
|---|---|
| **Title** | 012: Use of queues for asynchronous messaging between order and downstream services |
| **Status** | Superseded by 021 |

**ADR 021: New Decision — Use Topics**

| Section | Content |
|---|---|
| **Title** | 021: Use of topics for asynchronous messaging between order and downstream services |
| **Status** | Accepted, Supersedes 012 |
| **Context** | Same as ADR 012, but requirements have evolved. The downstream consumer base is growing and includes multiple consumers needing the same events. |
| **Decision** | We will use topics for asynchronous messaging between the trading and downstream services. |
| **Consequences** | Topics will require topic-based broker infrastructure (e.g., Kafka, RabbitMQ with topic exchanges). Each downstream service can subscribe independently without modifying the trading service. |

### B.2 TripEZ ADR — Layered Monolith

| Section | Content |
|---|---|
| **Title** | 011: Use of the layered monolith architectural style for the TripEZ system |
| **Status** | Proposed |
| **Context** | TripEZ is a fast-growing startup that requires a simple architecture to ensure feasibility. Additionally, the company needs to ensure extensibility to accommodate multiple third-party integrations. |
| **Decision** | We will use the layered monolith architectural style. Since TripEZ doesn't need separate architectural characteristics for different parts of its system, a layered monolith will suffice for the required architectural characteristics. The main constraint is scalability. Additionally, separating the system by technical capabilities makes extensibility easier. |
| **Consequences** | Because we chose a monolithic architecture, scalability may eventually grow to be a concern. Building a layered architecture makes some domain-centric changes harder because the effort will affect multiple layers. Architects will be able to change technical capabilities (such as adding support for new user interfaces) easily thanks to this architectural style's technical partitioning. |

### B.3 TripEZ ADR — Modular Monolith

| Section | Content |
|---|---|
| **Title** | 011: Use of the modular monolith architectural style for the TripEZ system |
| **Status** | Proposed |
| **Context** | TripEZ is a fast-growing startup that wants to make sure to model its architecture in a way that allows for the easiest possible migration to a distributed architecture, while still being simple enough to build on a tight schedule. |
| **Decision** | We will use the modular monolith architectural style. We've chosen a development process that aligns well with the domain partitioning exhibited by this architecture. Keeping each bounded context within a component boundary helps developers understand the system's organization. Additionally, the system can grow in a similar way to the problem domain. Our organization has adopted domain-driven design, and this architectural style aligns nicely with that approach. |
| **Consequences** | Because we've chosen a monolithic architecture, scalability may eventually grow to be a concern. Holistic changes to technical capabilities (such as user interfaces) are more difficult in this architecture, since the UI is handled by a part of each bounded context. |

### B.4 TripEZ ADR — Microkernel

| Section | Content |
|---|---|
| **Title** | 011: Use of the microkernel architectural style for the TripEZ system. |
| **Status** | Proposed |
| **Context** | TripEZ is essentially an integration architecture, managing similar information from a variety of integration partners. This architecture will easily facilitate both isolation and customization for each integration point via plugins. |
| **Decision** | We will use the microkernel architectural style. Time to market and extensibility are important to the company, so modeling the architecture around a simple core with plugins for future additional integration partners will make it easy for developers to understand and implement. We decided that the simplicity of a monolithic system outweighed the benefits (but added complexity) of distributed plugins. |
| **Consequences** | In a monolithic architecture, scalability may eventually grow to be a concern. The team may consider distributing the plugins in the future, but we decided that it would be overengineering for now. The core can be split so that the UI is handled by another microkernel, with different plugins for different UI types. We should avoid adding fast-changing requirements to the core. It should be as stable as possible. |

### B.5 Make the Grade ADR — Microservices

| Section | Content |
|---|---|
| **Title** | 011: Use of the microservices architectural style for the Make the Grade system |
| **Status** | Proposed |
| **Context** | Make the Grade is a test-taking system that needs high levels of responsiveness, fault tolerance, elasticity, and data integrity. Because there are separate parts of the system (admin, reporting, grading, and test taking) that require different architectural characteristics, a distributed architecture is appropriate. The two choices are microservices and event-driven architecture. |
| **Decision** | We will use the microservices architectural style. Microservices provides the necessary fault tolerance, elasticity, and scalability. Performance deficiencies and high responsiveness needs are addressed through minimal inter-service communication, caching to minimize data retrieval needs (student information, test questions, and test answer keys), and asynchronous communication for automatic grading and storing students' answers. Data integrity (preventing data loss) is addressed by using persistent queues between the Capture Answer and Automatic Grading components, along with client acknowledgment mode in the Automatic Grading component, to make sure that each student answer stays on the queue until it is persistent in the Student Answer Database. The test administration functionality will be a single microservice that combines the test scheduling, test maintenance, and student maintenance functionalities. Reporting will be a single microservice as well. |
| **Consequences** | Technically partitioned teams will need to be reorganized into cross-functional teams and will work in parallel in order to finish the system in six months. We will need to use in-memory caching to address the system's performance, elasticity, and data sharing needs. We will need additional infrastructure to support microservices: specifically, a service orchestrator like Kubernetes and a more effective CI/CD deployment pipeline. |

---

## Appendix C: Comprehensive Style Comparison

### C.1 Star Rating Comparison Matrix

This comprehensive matrix compares all five architectural styles covered in the book across ten architectural characteristics:

| Characteristic | Layered | Modular Monolith | Microkernel | Microservices | EDA |
|---|---|---|---|---|---|
| Maintainability | ★ | ★★★ | ★★★ | ★★★★ | ★★★★ |
| Testability | ★★ | ★★★ | ★★★ | ★★★★ | ★★ |
| Deployability | ★ | ★★★ | ★★★ | ★★★★ | ★★★ |
| Simplicity | ★★★★ | ★★★★ | ★★★★★ | ★ | ★ |
| Evolvability | ★ | ★★★ | ★★★ | ★★★★ | ★★★★ |
| Performance | ★★★ | ★★★ | ★★★ | ★★ | ★★★★ |
| Scalability | ★ | ★ | ★ | ★★★★★ | ★★★★ |
| Elasticity | ★ | ★ | ★ | ★★★★ | ★★★ |
| Fault Tolerance | ★ | ★ | ★ | ★★★★ | ★★★★ |
| Overall Cost | $ | $$ | $ | $$$$$ | $$$ |

**Reading the matrix:**
- **Monolithic styles** (layered, modular monolith, microkernel) generally have ★ for scalability, elasticity, and fault tolerance — they share resources and deployment
- **Distributed styles** (microservices, EDA) excel at operational characteristics but suffer in simplicity
- **Microkernel** is uniquely high on simplicity (★★★★★) because the core is small and stable
- **EDA** has lower testability (★★) because asynchronous processing is harder to test
- **Microservices** is most expensive ($$$$$) due to operational complexity

### C.2 When to Use Each Style

| Use case | Best style | Why |
|---|---|---|
| Small bakery taking online orders | **Layered** | Simple problem, small scale, time-to-market |
| Modular, domain-rich, infrequent change | **Modular monolith** | Domain partitioning without distributed complexity |
| High customization, stable core | **Microkernel** | Plugins handle variability, core stays simple |
| International wire transfers overnight | **Modular monolith** | Rich domain, doesn't need scalability or elasticity |
| Standardized testing for 200K students | **Microservices** | Independent scaling, elasticity, fault tolerance |
| Online ordering with high throughput | **EDA** | Async, decoupled, parallel processing |
| Online auction with high concurrency | **Microservices** or **EDA** | Scalability + fault tolerance needed |
| Trouble ticket for electronics support | **Microservices** | Independent functions, simple workflows |
| Company expecting constant change | **Modular monolith** (start) → **Microservices** (later) | Start simple, evolve when forces demand |
| IDE, linter, build tool | **Microkernel** | Plugins for extensibility, stable core |

### C.3 Style Philosophy Summary

| Style | Philosophy | When to apply |
|---|---|---|
| **Layered** | Technical partitioning + monolithic deployment = simplicity | Simple systems, technical specialization |
| **Modular Monolith** | Domain partitioning + monolithic deployment = balance | Rich domains, growing teams, future microservices migration |
| **Microkernel** | Stable core + customizable plugins = flexibility | Customization, extensibility, stable core |
| **Microservices** | Domain partitioning + distributed deployment = independence | Independent scaling, fault isolation, technology diversity |
| **EDA** | Event broadcast + asynchronous communication = throughput | High throughput, parallel processing, decoupled services |

---

## Appendix D: EDA vs. Microservices Comparison

### D.1 Key Differences

| Aspect | Microservices | EDA |
|---|---|---|
| Bounded context | Required (physical) | Optional (services can share data) |
| Database | Database-per-service (typical) | Monolithic, domain-partitioned, or database-per-service |
| Communication | Mostly synchronous (REST) | Mostly asynchronous (events) |
| Processing | Request processing (commands) | Event processing (things that have already happened) |
| Service granularity | Fine-grained, single-purpose | Any size |
| Data sharing | Forbidden (must ask) | Allowed (services can share data) |
| Performance | Moderate (network overhead) | High (parallel processing) |
| Complexity | High (many hard decisions) | Very high (asynchronous, parallel) |
| Testability | High | Moderate (async is hard to test) |
| Cost | $$$$$ | $$$ |

### D.2 Hybrid: Event-Driven Microservices

When EDA and microservices are combined, the resulting hybrid gets the best of both worlds:

- **Microservices aspects:** Single-purpose services, physical bounded contexts, independent deployment
- **EDA aspects:** Asynchronous communication, broadcast events, derived events for extensibility
- **The difference from pure EDA:** Each service is single-purpose (not multi-purpose); each service owns its data (not shared)
- **The difference from pure microservices:** Communication is asynchronous (not REST); events drive the workflow

The book's worked example: EDA's Order Submission service (which accepts, validates, applies payment, adjusts inventory) is *not* a single-purpose service. That's acceptable in EDA but not in microservices. To make it event-driven microservices, you split it into separate single-purpose services, each triggering its own events.

---

## Appendix E: Architectural Decision Lifecycle

### E.1 Status Transitions

```
                ┌──────────────┐
                │   Proposed   │
                └──────┬───────┘
                       │ (sign-off)
                       ▼
                ┌──────────────┐
                │   Accepted   │◀─────────────┐
                └──────┬───────┘              │
                       │ (decision           │
                       │  superseded)        │
                       ▼                      │
                ┌──────────────┐              │
                │  Superseded  │──────────────┘
                └──────────────┘    (new ADR
                                    Accepted)
```

### E.2 ADR Workflow Best Practices

1. **Create** ADR with `Proposed` status when initiating a decision
2. **Circulate** for feedback (especially if using RFC pattern)
3. **Mark** `Accepted` when sign-off is complete
4. **Never edit** an Accepted ADR — write a new one instead
5. **Mark old** as `Superseded by X` and link to the new ADR
6. **Preserve history** — supersession preserves the chain of decisions

### E.3 ADR Tools and Storage

- **Plain-text files in version control** — Markdown or AsciiDoc; commit history shows changes
- **Separate repository** — keep ADRs separate from source code
- **Wikis** — more accessible to non-developers; ensure change tracking is enabled
- **ADR tools** — see https://adr.github.io/#decision-capturing-tools for a list
- **File naming convention:** `042-use-queues-between-the-trading-and-downstream-services.md` (three-digit prefix, all lowercase, hyphens for spaces)
- **Sequence advantage:** Three-digit prefix means sorting files alphabetically puts them in chronological order

---

## Appendix F: Further Reading

The book recommends:

- **Fundamentals of Software Architecture** by Mark Richards and Neal Ford — same authors; deeper coverage of foundational concepts
- **Software Architecture: The Hard Parts** by Neal Ford, Mark Richards, Pramod Sadalage, and Zhamak Dehghani — advanced trade-off analysis
- **Building Evolutionary Architectures** by Neal Ford, Rebecca Parsons, and Patrick Kua — fitness functions for architectural governance
- **Head First Design Patterns** by Eric Freeman and Elisabeth Robson — for design patterns that show up in architecture (MVC, layers)
- **ISO/IEC 25010** — standards for software product quality (https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)
- **Martin Fowler's architecture site** — https://martinfowler.com/architecture
- **ADR tools** — https://adr.github.io/#decision-capturing-tools
- **Event storming** — https://en.wikipedia.org/wiki/Event_storming (related to actor/action approach)

The book's own website: https://www.headfirstsoftwarearchitecture.com

---

## Appendix G: Glossary

| Term | Definition |
|---|---|
| **Afferent coupling (Ca)** | Incoming coupling — how many other components depend on this one |
| **Architectural characteristic** | Non-domain design consideration that influences structural decisions (the "-ilities") |
| **Architectural decision** | Choice about structural aspects with long-term implications |
| **ADR** | Architecture Decision Record — immutable record of a decision, its context, and consequences |
| **Architectural style** | Overarching structural pattern that defines topology and deployment |
| **Bounded context** | Domain boundary where a particular model applies (DDD term) |
| **Choreography** | Decentralized workflow where services react to events independently |
| **Composite characteristic** | Architectural characteristic that combines multiple sub-characteristics |
| **Conway's Law** | Organizations design systems that mirror their communication structures |
| **Derived event** | Event generated by a system as a result of processing other events |
| **Distributed architecture** | Components deployed independently across multiple units |
| **Domain partitioning** | Organizing components by business domain |
| **Efferent coupling (Ce)** | Outgoing coupling — how many other components this one depends on |
| **Elasticity** | Ability to dynamically scale up and down based on demand |
| **Entity trap** | Anti-pattern of organizing components around domain entities instead of responsibilities |
| **Event** | Immutable fact that something has happened; broadcast to multiple consumers |
| **Fitness function** | Mechanism to objectively evaluate architectural conformance |
| **Four Dimensions** | Characteristics, decisions, components, style |
| **FURPS+** | Functional, Usability, Reliability, Performance, Supportability (plus implementation, interface, physical, design) |
| **Grains of Sand** | Anti-pattern of microservices that are too fine-grained |
| **Granularity disintegrators** | Forces that push you to make services smaller |
| **Granularity integrators** | Forces that push you to make services bigger |
| **Hybrid architecture** | Combination of two or more architectural styles |
| **Initiating event** | Event triggered by external actors (users, sensors, time) |
| **Law of Demeter** | Components should only talk to immediate friends, not strangers |
| **Layered architecture** | Technical partitioning into Presentation, Workflow, Persistence |
| **Logical architecture** | What components are and how they interact (independent of deployment) |
| **Microservice** | Single-purpose, separately deployed unit of software that does one thing really well |
| **Microkernel** | Architecture with stable core and plug-in components for customization |
| **Modular monolith** | Single deployment partitioned by business domain |
| **Monolithic architecture** | All components deployed as a single unit |
| **Orchestration** | Centralized workflow management with a dedicated orchestrator service |
| **Physical architecture** | How components are deployed and communicate at runtime |
| **Physical bounded context** | Microservice plus its exclusively-owned data |
| **Pluggable architecture** | See Microkernel |
| **REST** | Representational State Transfer — synchronous HTTP-based communication |
| **Shared library** | Reusable code artifact (JAR, DLL) included with each service at compile time |
| **Shared service** | Separate microservice providing shared functionality via remote calls |
| **Sinkhole anti-pattern** | Request passing through layers without adding value |
| **Style selection matrix** | Decision matrix placing candidate styles against driving characteristics |
| **Technical partitioning** | Organizing components by technical concern (presentation, business, persistence) |
| **Trade-off analysis** | Process of identifying options, evaluating pros/cons, considering context, deciding, and documenting |
| **Workflow approach** | Identifying components by major use-case steps |
| **Actor/action approach** | Identifying components by actors and their primary actions |