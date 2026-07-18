# Learning Domain-Driven Design -- Comprehensive Summary

**Author:** Vlad Khononov
**Publisher:** O'Reilly Media, 2021
**Subtitle:** Aligning Software Architecture and Business Strategy

---

## Introduction

Domain-driven design (DDD) is a methodology for aligning software design with business strategy. It addresses the root cause of failed software projects: ineffective communication. DDD provides both strategic tools (for analyzing business domains and making high-level design decisions) and tactical tools (for implementing business logic in code that reflects the domain). The methodology can be divided into two parts: **strategic design** answers "what" and "why," while **tactical design** addresses "how."

The book uses a running example company called **WolfDesk**, a help desk ticket management SaaS that charges per ticket, includes a fraud detection system, and offers a support autopilot feature.

---

# Part I: Strategic Design

## Chapter 1: Analyzing Business Domains

### What Is a Business Domain?

A business domain defines a company's main area of activity -- the service it provides to its clients. Companies can operate in multiple business domains (e.g., Amazon operates in both retail and cloud computing). Business domains can change over time (e.g., Nokia moved from wood processing to rubber to telecommunications).

### What Is a Subdomain?

To achieve its business domain goals, a company operates in multiple **subdomains** -- fine-grained areas of business activity. All subdomains together form the business domain. None is sufficient on its own; they must interact. For example, Starbucks needs coffee-making, real estate, hiring, and finance subdomains to succeed.

### Types of Subdomains

DDD distinguishes three types of subdomains:

**Core subdomains** are what a company does differently from competitors. They provide competitive advantage, involve inventions or smart optimizations, and are naturally complex. They must be implemented in-house by the most skilled engineers using advanced techniques. Core subdomains change frequently as companies continuously innovate. Example: Google's search ranking algorithm, Uber's ridesharing and route-matching logic.

**Generic subdomains** are business activities all companies perform the same way. They are complex but already solved -- battle-tested implementations exist. They provide no competitive advantage and should be bought or adopted as off-the-shelf/open source solutions rather than built in-house. Example: authentication, encryption, accounting.

**Supporting subdomains** support the company's business but provide no competitive advantage. Their business logic is simple (CRUD interfaces, ETL operations). They must be implemented in-house since no generic solution exists, but they don't require advanced engineering. They are good candidates for outsourcing and training junior developers. Example: a creative materials catalog at an advertising company.

### Comparing Subdomains

| Subdomain type | Competitive advantage | Complexity | Volatility | Implementation     | Problem     |
|----------------|-----------------------|------------|------------|--------------------|-------------|
| Core           | Yes                   | High       | High       | In-house           | Interesting |
| Generic        | No                    | High       | Low        | Buy/adopt          | Solved      |
| Supporting     | No                    | Low        | Low        | In-house/outsource | Obvious     |

### Identifying Subdomain Boundaries

Subdomains are "already there" -- defined by the company's business strategy. A good starting point is organizational departments, but these are often too coarse-grained. The principle of **distilling subdomains** involves drilling into coarse areas to find finer-grained subdomains of different types. For example, a "customer service" department may contain a core routing algorithm, a generic help desk system, a generic telephone system, and supporting shift management.

From a technical perspective, subdomains resemble **sets of coherent use cases** involving the same actor, business entities, and closely related data. This definition provides the most precise boundaries.

Distillation should be aggressive for core subdomains (to focus effort) but can be relaxed for supporting and generic subdomains when no new strategic insights emerge.

### Domain Experts

Domain experts are subject matter experts who understand the business domain's intricacies. They are the people who identified the business problem and from whom all business knowledge originates. They are neither analysts nor engineers -- they represent the business.

---

## Chapter 2: Discovering Domain Knowledge

### Business Problems and Communication

Software systems solve business problems. Effective knowledge sharing between domain experts and engineers requires effective communication. In traditional software development, domain knowledge passes through multiple "translations" (domain knowledge -> analysis model -> requirements -> system design -> source code), losing information at each step -- like the children's game Telephone.

### The Ubiquitous Language

DDD's solution is the **ubiquitous language** -- a single, shared language for describing the business domain that all stakeholders use consistently. Key principles:

- **Language of the business**: No technical jargon. Terms like "HTML iframe" or "database records" don't belong; instead use "creative materials" and "campaign placements."
- **Consistency**: Each term must have one and only one meaning. Ambiguous terms (e.g., "policy" meaning both a regulatory rule and an insurance contract) must be made explicit with distinct terms.
- **No synonymous terms**: Two terms cannot be used interchangeably. "User," "visitor," "administrator," and "account" represent different concepts with different behaviors.
- **Continuous effort**: The language must be constantly validated and evolved as deeper domain insights emerge.

### Modeling the Business Domain

A model is a simplified representation emphasizing certain aspects while ignoring others. An effective model contains only details needed to fulfill its purpose. The ubiquitous language is effectively a model of the business domain -- capturing domain experts' mental models, business entities, behavior, cause-and-effect relationships, and invariants.

Tools for managing a ubiquitous language include wikis/glossaries (good for nouns), use cases, and Gherkin tests (better for capturing behavior and business rules).

---

## Chapter 3: Managing Domain Complexity

### Inconsistent Models

Different stakeholders naturally form different mental models of the same business domain. For example, in a book publisher's domain, a "book" means different things to different departments: the editorial department thinks of a manuscript, production thinks of physical dimensions, and marketing thinks of a product to sell.

### Bounded Contexts

A **bounded context** is a pattern that defines the boundaries within which a particular model and ubiquitous language apply consistently. Key properties:

- **Model boundary**: Each bounded context has its own ubiquitous language, and the same term can mean different things in different contexts.
- **Scope**: A bounded context can encompass one or more subdomains. Ideally, each bounded context maps to a single subdomain, but pragmatically they often span multiple.
- **Physical boundaries**: Bounded contexts are physical design elements -- they can map to subsystems, services, or modules.
- **Ownership boundaries**: Each bounded context should be owned by one team.

### Bounded Contexts Versus Subdomains

Subdomains and bounded contexts serve different purposes:

- **Subdomains** are discovered through business domain analysis (what the business does). They are part of the problem space.
- **Bounded contexts** are design decisions (how we model the solution). They are part of the solution space.

The interplay between them: ideally, one bounded context per subdomain. When starting, bounded contexts can be wider (encompassing multiple subdomains), and can be decomposed as domain knowledge grows.

### Real-Life Examples

The book uses examples from semantic domains (different meanings of "water" in different contexts), science (different models of atoms in physics vs. chemistry), and buying a refrigerator (different parties need different models of the same product) to illustrate why bounded contexts are natural and necessary.

---

## Chapter 4: Integrating Bounded Contexts

Bounded contexts must interact. DDD defines several integration patterns:

### Partnership

Bounded contexts are integrated in an ad hoc manner. Teams collaborate closely and can coordinate changes on the fly. Best suited for teams with strong communication, but doesn't scale well.

### Shared Kernel

Two or more bounded contexts share a limited overlapping model. All participating teams co-own and co-evolve the shared portion. Risks include mutual dependencies and slower evolution.

### Customer-Supplier

The upstream (supplier) team provides what the downstream (customer) team needs, driven by the supplier's interests. Two sub-patterns:

- **Conformist**: The consumer conforms to the supplier's model. Used when the consumer has no leverage to influence the supplier.
- **Anticorruption Layer (ACL)**: The consumer translates the supplier's model into one that fits its own needs. Essential for core subdomains to protect their model from external influence.

### Open-Host Service (OHS)

The supplier implements a **published language** -- a model optimized for consumers' integration needs, separate from the internal implementation model. This is the DDD equivalent of the Facade pattern.

### Separate Ways

When integration is more expensive than duplicating functionality, teams go their separate ways. This should never be used for core subdomains.

### Context Map

A **context map** is a visual representation plotting bounded contexts and their integration patterns. It provides insight into high-level design, communication patterns among teams, and organizational issues. It should be maintained as a shared effort across teams.

---

# Part II: Tactical Design

## Chapter 5: Implementing Simple Business Logic

### Transaction Script

Organizes business logic as procedures where each handles a single request from the presentation layer. Each operation must be transactional -- it either succeeds or fails, never leaving the system in an inconsistent state.

Common pitfalls include:
- **Lack of transactional behavior**: Multiple updates without an overarching transaction.
- **Distributed transactions**: Changes to a database plus publishing to a message bus can't easily be wrapped in one transaction.
- **Implicit distributed transactions**: Even a single database update communicates success/failure to the caller; network failures can cause duplicate operations.

Solutions include making operations **idempotent** (producing the same result even if repeated) and using **optimistic concurrency control** (checking version numbers before updates).

Transaction script fits supporting subdomains with simple, ETL-like logic. It should never be used for core subdomains.

### Active Record

An object that wraps a row in a database table, encapsulates database access, and adds domain logic on that data. Used when business logic is simple but data structures are complex (object trees, hierarchies).

Active records separate data structures from behavior -- fields have public getters/setters that allow external procedures to modify state. This is the key difference from the domain model pattern. Active record is also known as the "anemic domain model antipattern," but Khononov avoids this negative framing -- it is a valid tool for simple business logic.

---

## Chapter 6: Tackling Complex Business Logic

### Domain Model

The domain model pattern addresses complex business logic with complicated state transitions, business rules, and invariants. It consists of three main building blocks:

### Value Objects

Objects identified by the composition of their values (no explicit ID needed). They are **immutable** -- changes produce new instances. Value objects eliminate the "primitive obsession" code smell by representing domain concepts as rich types rather than raw strings and integers. They encapsulate validation and business logic, make code more expressive, and are thread-safe. Use them whenever possible, especially for properties that describe entities (names, phone numbers, money, statuses).

### Entities

Objects that require an explicit identification field to distinguish between instances (e.g., two people can have the same name). Entities are mutable and expected to change. They are not used independently but only as part of aggregates.

### Aggregates

An aggregate is a **consistency enforcement boundary** -- a hierarchy of entities and value objects sharing a transactional boundary. Key principles:

- **State can only be modified through the aggregate's public interface** (commands). External objects can only read state.
- **One aggregate per database transaction** -- this forces careful design of boundaries.
- **Keep aggregates as small as possible** -- include only data that must be strongly consistent for the aggregate's business logic.
- **Reference other aggregates by ID**, not by object reference, to maintain independence.
- **Aggregate root**: Only one entity in the hierarchy serves as the public interface.

Aggregates also manage concurrency through version fields, enabling optimistic concurrency control.

### Domain Events

Messages describing significant events in the business domain (named in past tense). They are part of an aggregate's public interface and allow external components to react to changes.

### Domain Services

Stateless objects hosting business logic that doesn't naturally belong to any aggregate or value object. They orchestrate reads from multiple aggregates (but still respect the one-aggregate-per-transaction rule for writes).

### Managing Complexity

Aggregates and value objects reduce complexity by encapsulating invariants, reducing the system's degrees of freedom. Following Eliyahu Goldratt's definition, complexity is measured by degrees of freedom needed to describe a system's state. Encapsulated invariants reduce these degrees.

---

## Chapter 7: Modeling the Dimension of Time

### Event Sourcing

Instead of persisting an aggregate's current state, event sourcing persists every state change as a domain event. The events become the **source of truth**. The current state can always be reconstituted by projecting (replaying) events.

Key advantages of event sourcing:
- **Time traveling**: Reconstitute past states at any point in an aggregate's lifecycle.
- **Deep insight**: Events can be projected into multiple different models optimized for different purposes (search, analysis, reporting).
- **Audit log**: Complete, strongly consistent history of every state change.
- **Advanced concurrency**: Business-driven decisions about whether concurrent events actually collide.

The event store is an append-only database supporting fetching events by aggregate ID and appending new events with optimistic concurrency checks.

### Event-Sourced Domain Model

Combines event sourcing with the domain model pattern. Each operation follows: load events, reconstitute state, execute command (producing new events), commit new events to the event store.

For performance with large event streams, the **snapshot pattern** can cache projected states. For GDPR compliance, the **forgettable payload pattern** encrypts sensitive data in events with a key that can be deleted.

Disadvantages include a steep learning curve, challenges evolving event schemas, and architectural complexity (especially with CQRS).

---

## Chapter 8: Architectural Patterns

### Layered Architecture

Organizes code into horizontal layers:
- **Presentation layer**: User interface, APIs, message subscriptions.
- **Business logic layer**: Implements business logic (transaction scripts, active records).
- **Data access layer**: Databases, external services.

Layers communicate top-down only. A **service layer** can be added as a facade between presentation and business logic. Best suited for transaction script and active record patterns.

### Ports and Adapters (Hexagonal Architecture)

Addresses layered architecture's shortcoming by using the **Dependency Inversion Principle** -- business logic doesn't depend on infrastructure. Instead:

- **Ports**: Interfaces defined by the business logic layer.
- **Adapters**: Concrete implementations in the infrastructure layer.

This is the proper fit for domain model and event-sourced domain model patterns. Also known as hexagonal architecture, onion architecture, or clean architecture.

### CQRS (Command-Query Responsibility Segregation)

Segregates the system's data into:
- **Command execution model**: The single source of truth for writes, implementing business logic and validation.
- **Read models (projections)**: Multiple read-only models optimized for different querying needs.

Read models are projected from the command model either synchronously (catch-up subscription using checkpoints) or asynchronously (via message bus). CQRS is essential for event-sourced systems (since you can't query events by aggregate state) and useful whenever multiple data representations are needed.

Importantly, commands CAN return data -- they should report success/failure and can return strongly consistent state to the caller.

All architectural patterns should be applied at the module level, not necessarily system-wide. Different subdomains within a bounded context can use different patterns.

---

## Chapter 9: Communication Patterns

### Model Translation

When integrating bounded contexts with different models:

- **Stateless translation**: Proxy pattern intercepting requests and mapping models. Can be embedded in code, offloaded to an API gateway, or implemented as a message proxy for asynchronous communication.
- **Stateful translation**: Required for aggregation, batching, or unifying data from multiple sources. Needs its own persistent storage.

### Outbox Pattern

Ensures reliable publishing of domain events:
1. Commit both aggregate state changes and domain events in one atomic transaction.
2. A message relay fetches unpublished events from the database.
3. The relay publishes events to the message bus.
4. Upon success, the relay marks events as published.

Delivery is guaranteed at least once (consumers must handle duplicates). The relay can pull (polling publisher) or push (transaction log tailing).

### Saga

Handles business processes spanning multiple aggregates (respecting the one-aggregate-per-transaction rule). A saga is a reaction plan for each step of the process: when a domain event occurs, the saga decides what command to execute next. If a step fails, the saga executes compensating actions to undo previous steps.

Two implementation approaches:
- **Choreography**: Each component publishes domain events and reacts to events from others. Simple to implement but can become chaotic with complex processes.
- **Orchestration**: A central saga orchestrator manages the process flow. More explicit but introduces a central point of control.

### Process Manager

Similar to saga but can also make routing decisions and is stateless -- it doesn't maintain state between steps. It reacts to incoming events, decides the next action, and routes messages to the appropriate handler.

---

## Chapter 10: Design Heuristics

### Decision Tree

The chapter ties together all patterns into simple rules of thumb:

**Bounded context sizing**: Design one bounded context per subdomain when possible. Multiple subdomains in one context is acceptable when domain knowledge is uncertain.

**Business logic patterns by subdomain type**:
- Core subdomains: Domain model or event-sourced domain model.
- Generic subdomains: Buy/adopt off-the-shelf solutions.
- Supporting subdomains: Transaction script or active record.

**Architectural patterns by business logic**:
- Transaction script / Active record: Layered architecture.
- Domain model: Ports & adapters.
- Event-sourced domain model: Ports & adapters + CQRS.

**Testing strategies**:
- Testing pyramid (many unit tests, fewer integration tests, few E2E tests) for supporting/generic subdomains.
- Testing diamond (more integration tests) for core subdomains with domain models.
- Reversed testing pyramid (mostly E2E tests) for event-sourced systems.

---

## Chapter 11: Evolving Design Decisions

### Changes in Domains

Subdomain types can change over time:
- **Core to Generic**: A once-proprietary solution becomes commoditized (e.g., a custom payment system replaced by Stripe).
- **Generic to Core**: A previously solved problem becomes a competitive differentiator.
- **Supporting to Core**: A simple CRUD feature evolves complex business rules.
- **Core to Supporting**: Optimization efforts shift elsewhere.

### Tactical Design Evolution

Migrating between patterns:
- **Transaction script to Active Record**: Extract complicated data structures into dedicated objects.
- **Active Record to Domain Model**: Make all setters private, move business logic into object boundaries, identify transaction boundaries for aggregates, designate aggregate roots.
- **Domain model to Event-sourced domain model**: Model domain events for all state transitions. Handle existing data by either generating approximate past events or modeling explicit migration events.

### Organizational Changes

Changes in team structure affect bounded context integration patterns:
- **Partnership to Customer-Supplier**: When teams become geographically distant.
- **Customer-Supplier to Separate Ways**: When communication problems make integration more expensive than duplication.

### Growth

Growth can lead to a "big ball of mud" if design decisions aren't re-evaluated. The guiding principle is to identify and eliminate **accidental complexity** (caused by outdated decisions) while managing **essential complexity** (inherent to the business) with DDD tools:

- **Subdomains**: Revisit boundaries to find finer-grained subdomains as functionality grows.
- **Bounded contexts**: Ensure models stay focused; extract new bounded contexts when models lose focus.
- **Aggregates**: Keep as small as possible; extract business logic into new aggregates when data doesn't need strong consistency.

---

# Part III: Applying DDD in Practice

## Chapter 12: EventStorming

### What Is EventStorming?

EventStorming is a low-tech workshop for brainstorming and rapidly modeling a business process. Participants explore the process as a series of domain events represented by sticky notes on a timeline.

### Requirements

A large modeling space (wall covered with butcher paper), sticky notes of different colors, markers, a spacious room without chairs, and snacks. Ideal group size is up to 10 participants including diverse roles.

### The 10-Step Process

1. **Unstructured exploration**: Brainstorm domain events (orange sticky notes, past tense).
2. **Timelines**: Organize events in chronological order, starting with the happy path.
3. **Pain points**: Mark bottlenecks, manual steps, and missing knowledge (pink diamond notes).
4. **Pivotal events**: Identify significant context-changing events (potential bounded context boundaries).
5. **Commands**: Add commands that trigger events (light blue notes) with actors (small yellow notes).
6. **Policies**: Add automation policies connecting events to commands (purple notes).
7. **Read models**: Add data views actors use to make decisions (green notes).
8. **External systems**: Add systems outside the explored domain (pink notes).
9. **Aggregates**: Group related commands and events into aggregates (large yellow notes).
10. **Bounded contexts**: Group related aggregates into bounded context candidates.

The real value is the process itself -- sharing knowledge, aligning mental models, discovering conflicts, and building a ubiquitous language.

---

## Chapter 13: DDD in the Real World

### Brownfield Projects

Applying DDD to existing (brownfield) projects follows a different approach than greenfield:

1. **Understand the business domain**: Analyze the company's business strategy, identify subdomains and their types.
2. **Explore the current design**: Identify existing bounded contexts, ownership boundaries, and integration patterns (chart a context map).
3. **Modernization strategy**: Start with what brings the most business value. Focus on pain points.

### Strategic Modernization

- Focus on subdomains that provide the most business value.
- For core subdomains: invest in refactoring or replacing with properly designed implementations.
- For generic subdomains: replace with off-the-shelf solutions.
- For supporting subdomains: can be addressed with rapid application development.

### Tactical Modernization

- Cultivate a ubiquitous language even on existing projects.
- Extract subdomains into bounded contexts incrementally.
- Gradually introduce tactical patterns (start with identifying value objects and aggregates).

### Pragmatic DDD

DDD can be applied even without organization-wide adoption:
- **Undercover DDD**: Use DDD tools and patterns without explicitly calling it DDD. Focus on the logic and principles behind each pattern.
- **Selling DDD**: When proposing DDD, always tie it to business value -- reduced maintenance costs, faster time to market, better alignment with business strategy.

---

# Part IV: Relationships to Other Methodologies

## Chapter 14: Microservices

### Services and Microservices

A service is an independently deployable software component. A microservice is a service that is "small" -- but "small" is ambiguous. The book introduces the concept of **deep modules**: good software modules have simple interfaces but complex implementations (deep). Shallow modules with trivially simple implementations are a design smell.

### DDD and Microservice Boundaries

Three levels of alignment:
- **Bounded contexts**: The most natural boundary for microservices. Each bounded context can be implemented as a microservice.
- **Aggregates**: Too fine-grained for service boundaries but can be useful for subsystem decomposition within a service.
- **Subdomains**: Can inform service boundaries but require careful analysis since subdomains are discovered, not designed.

### Compressing Public Interfaces

Microservices should expose compressed public interfaces using:
- **Open-Host Service**: Publish a model optimized for consumers, separate from the internal model.
- **Anticorruption Layer**: Protect the microservice from external model influence.

---

## Chapter 15: Event-Driven Architecture

### Event-Driven Architecture (EDA)

EDA defines how components communicate through events. Events, commands, and messages are distinct concepts: events describe something that happened, commands request an action, and messages are the data carriers.

### Types of Events

Three types of events for cross-component communication:

1. **Event notification**: A lightweight message notifying that something happened. The consumer must query the producer for additional information. Useful when the consumer needs strongly consistent (most recent) data.

2. **Event-carried state transfer (ECST)**: Includes all data reflecting the state change, enabling consumers to maintain a local cache. An asynchronous data replication mechanism that improves fault tolerance and performance. However, data is eventually consistent.

3. **Domain events**: Describe business events with full context. Modeled to represent the business domain, not for integration purposes. Can be useful even without external consumers (especially in event-sourced systems).

### Designing Event-Driven Integration

Common pitfalls that create a "distributed big ball of mud":

- **Temporal coupling**: Components depend on strict execution order (e.g., processing delays).
- **Functional coupling**: Multiple components implement the same business logic (duplicate projections).
- **Implementation coupling**: Subscribers depend on producer's internal domain events, breaking when the producer's model changes.

Heuristics for proper event-driven design:
- **Assume the worst**: Network will be slow, servers will fail, events will arrive out of order or duplicated.
- **Use public and private events**: Expose only integration-optimized events through the published language; keep internal domain events private.
- **Evaluate consistency requirements**: Use ECST for eventually consistent needs, event notifications for strongly consistent reads.

---

## Chapter 16: Data Mesh

### Analytical vs. Transactional Data

Operational (OLTP) models serve real-time transactions, are optimized for writes, and model entity lifecycles. Analytical (OLAP) models serve reporting and analysis, are optimized for reads, and use fact tables and dimension tables:

- **Fact tables**: Represent business activities (append-only, never modified or deleted).
- **Dimension tables**: Describe facts' attributes, highly normalized for flexible querying.

Common schemas: **star schema** (facts surrounded by flat dimensions) and **snowflake schema** (multilevel normalized dimensions).

### Traditional Analytical Architectures

**Data warehouse**: ETL processes extract operational data, transform it into analytical models, and load it into a centralized database. Challenges: building an enterprise-wide model is impractical; ETL scripts create strong coupling to operational database schemas.

**Data lake**: Ingests raw operational data without transformation. Analysts and data engineers create ETL scripts to generate analytical models later. Challenges: data becomes chaotic ("data swamp") at scale; multiple ETL script versions are needed for different operational model versions.

### Data Mesh

Data mesh applies DDD principles to analytical data:

1. **Decompose data around domains**: Align analytical models with bounded contexts. Each product team owns both its operational and analytical models.

2. **Data as a product**: Expose analytical data through well-defined output ports (like public APIs). Analytical endpoints have schemas, SLAs, versioning, and discoverability.

3. **Enable autonomy**: Provide a self-serve data infrastructure platform so product teams can create and consume data products without centralized bottlenecks.

4. **Build an ecosystem**: Establish federated governance for interoperability across data products.

### DDD Patterns Supporting Data Mesh

- The **ubiquitous language** provides domain knowledge essential for analytical modeling.
- The **open-host service** pattern exposes analytical models as a published language.
- **CQRS** projects operational data into analytical models and supports multiple schema versions simultaneously.
- Bounded context integration patterns (partnership, ACL, separate ways) apply to analytical model integration as well.

---

## Closing Words

The book emphasizes that DDD is not an all-or-nothing methodology. Even applying individual tools -- a ubiquitous language, bounded contexts, or the right business logic pattern for the subdomain type -- provides significant value. The key insight is that software design decisions should be driven by business strategy: what provides competitive advantage (core subdomains) deserves the most sophisticated engineering, while supporting and generic subdomains should be handled pragmatically with simpler solutions.

The most important lesson is that boundaries matter: subdomain boundaries, model boundaries (bounded contexts), consistency boundaries (aggregates), and ownership boundaries (teams). Getting these boundaries right -- and evolving them as the business and organization change -- is the essence of domain-driven design.

---

*This summary covers all 16 chapters of "Learning Domain-Driven Design" by Vlad Khononov, including the strategic design tools (subdomains, ubiquitous language, bounded contexts, context maps), tactical patterns (transaction script, active record, domain model, event sourcing), architectural patterns (layered, ports & adapters, CQRS), communication patterns (model translation, outbox, saga, process manager), and the relationships between DDD and microservices, event-driven architecture, and data mesh.*
