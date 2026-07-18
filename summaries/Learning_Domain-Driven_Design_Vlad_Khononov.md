# Learning Domain-Driven Design - Comprehensive Summary

**Author:** Vlad Khononov
**Publisher:** O'Reilly Media

---

## Introduction

*Learning Domain-Driven Design* by Vlad Khononov is a practical guide to Domain-Driven Design (DDD) that bridges the gap between Eric Evans's foundational concepts and modern software engineering practices. The book uses a sample domain called WolfDesk (a ticket management system for IT support) throughout to illustrate concepts. It is organized into three parts: Strategic Design (analyzing and modeling business domains), Tactical Design (implementation patterns), and real-world application (EventStorming and applying DDD to legacy systems). Khononov emphasizes that DDD is not about writing code -- it is about understanding business domains and making deliberate design decisions based on that understanding.

---

## Part I: Strategic Design

### Chapter 1: Analyzing Business Domains

#### What Is a Business Domain?

A business domain is the problem space that an organization operates in and the specific problems it aims to solve for its customers. It represents the company's area of activity -- what the company does and why it exists. Understanding the business domain is the starting point for all DDD work.

#### What Is a Subdomain?

A subdomain is a fine-grained area of activity within a business domain. A company's business domain is composed of multiple subdomains, each representing a specific business function. For example, an e-commerce company might have subdomains for catalog management, checkout, shipping, and customer support.

#### Types of Subdomains

The book classifies subdomains into three types based on their strategic importance:

- **Core subdomains:** What the company does uniquely well -- its competitive advantage. These are the reasons customers choose this company over competitors. Core subdomains are complex and require significant investment in modeling and implementation. They are neither easy nor obvious to replicate.

- **Supporting subdomains:** Important business functions that do not provide competitive advantage but are necessary for operations. These are often good candidates for off-the-shelf software or outsourcing because they do not differentiate the company. They involve moderate complexity.

- **Generic subdomains:** Business functions common across many companies and industries (e.g., email, authentication, payment processing). These provide no competitive advantage and are best addressed with existing solutions. Generic subdomains are well-understood and widely solved.

#### Comparing Subdomains

The three subdomain types can be compared across three dimensions:
- **Competitive advantage:** Core (high), Supporting (low), Generic (none)
- **Complexity:** Core (high), Supporting (moderate), Generic (low -- solved problems)
- **Volatility:** Core (high -- constantly evolving), Supporting (moderate), Generic (low -- stable)

#### Identifying Subdomain Boundaries

Identifying subdomains is not a scientific process -- it is a heuristic, iterative activity. Start by asking: "What does the company do?" and decompose from there. Use interviews with domain experts, examine organizational structure, and analyze business processes. The goal is to identify a manageable number of subdomains (typically 3-7 for most business domains).

#### Domain Analysis Examples

Two detailed examples illustrate domain analysis:
- **Gigmaster:** An event booking company with subdomains for artist management, event scheduling, ticket sales, and payment processing
- **BusVNext:** A public transportation company with subdomains for route planning, fleet management, ticketing, and real-time tracking

#### Who Are the Domain Experts?

Domain experts are the people who deeply understand the business domain -- not software engineers, but business stakeholders, product managers, operations staff, and end users who live and breathe the domain daily. Effective DDD requires close collaboration between domain experts and software engineers.

---

### Chapter 2: Discovering Domain Knowledge

#### Business Problems

All software exists to solve business problems. Before writing any code, you must understand the problem you are solving. This understanding comes through knowledge discovery -- a collaborative process of learning about the domain.

#### Knowledge Discovery

Knowledge discovery in DDD is not a one-time activity but a continuous process. It involves:
- Interviews with domain experts
- Observation of business processes
- Analysis of existing systems and documentation
- Collaborative modeling sessions

#### Communication

The biggest obstacle to effective knowledge discovery is communication. Domain experts use business language; developers use technical language. This gap leads to misunderstandings, incorrect assumptions, and software that does not solve the right problems.

#### What Is a Ubiquitous Language?

A ubiquitous language is a shared, rigorous language used by all team members -- domain experts and developers alike -- to describe the domain model. It is:
- **Ubiquitous:** Used everywhere -- in conversations, code, tests, documentation
- **Rigorous:** Precise and unambiguous; every term has a single, agreed-upon meaning
- **Based on the domain:** Uses business terminology, not technical jargon

The ubiquitous language evolves as the team's understanding of the domain deepens.

#### Language of the Business

The ubiquitous language should be rooted in the language used by domain experts. If domain experts say "subscription plan," the code should use `SubscriptionPlan` -- not `ProductTier` or `ServiceLevel`. This alignment ensures that conversations about business requirements translate directly into implementation.

#### Model of the Business Domain

A domain model is a simplified representation of the business domain that captures the essential concepts and rules needed to solve specific problems. It is not a complete picture of reality -- it is a useful abstraction. Effective models:
- Focus on the essential aspects of the problem
- Ignore irrelevant details
- Are expressed in the ubiquitous language
- Can be validated by domain experts

---

### Chapter 3: Managing Domain Complexity

#### Inconsistent Models

As a business domain grows, different teams and contexts naturally develop different mental models. The word "product" means different things to a sales team (something sold) and a warehouse team (a physical item to be shipped). These inconsistencies are not errors -- they reflect genuine differences in perspective and purpose.

#### What Is a Bounded Context?

A bounded context is an explicit boundary within which a particular domain model applies consistently. Inside a bounded context:
- The ubiquitous language has one consistent meaning
- The domain model is unified and coherent
- All team members share the same understanding of terms

Bounded contexts are the primary tool for managing complexity in DDD. They allow different parts of an organization to use different models appropriate to their specific needs.

#### Bounded Contexts Versus Subdomains

Subdomains and bounded contexts are related but distinct concepts:
- **Subdomains** are discovered through analysis of the business domain (they exist in the problem space)
- **Bounded contexts** are designed as part of the solution (they exist in the solution space)

In an ideal world, each subdomain maps to one bounded context. In practice, the mapping may be more complex due to organizational, technical, or historical constraints.

#### Boundaries

Bounded context boundaries have two dimensions:
- **Physical boundaries:** Typically implemented as separate codebases, services, or modules
- **Ownership boundaries:** Teams or individuals responsible for the bounded context's model and implementation

The ideal is for bounded contexts to align with both physical and ownership boundaries, enabling autonomous teams to work independently.

---

### Chapter 4: Integrating Bounded Contexts

#### Cooperation Patterns

When bounded contexts need to interact, several relationship patterns are available:

**Partnership:** Two teams work closely together, with frequent synchronization. Best when both contexts are evolving rapidly and changes in one immediately affect the other.

**Shared Kernel:** A subset of the domain model is shared between bounded contexts. This reduces duplication but creates a coupling point that both teams must agree on.

#### Customer-Supplier Patterns

**Conformist:** The downstream (customer) team conforms to the upstream (supplier) team's model. Used when the downstream team has no leverage to influence the upstream API.

**Anticorruption Layer (ACL):** The downstream team builds a translation layer between their model and the upstream model. This protects the downstream bounded context's model integrity from external influence. The ACL translates incoming data from the supplier's model to the consumer's model.

**Open-Host Service:** The upstream team publishes a well-defined integration protocol (an API or event schema) for all consumers. This standardizes integration and prevents the upstream team from maintaining one-off integrations.

#### Separate Ways

When integration costs outweigh benefits, bounded contexts can operate independently with no direct communication. Each implements its own version of the overlapping functionality.

#### Context Map

A context map is a visual representation of the relationships between bounded contexts. It shows:
- The bounded contexts and their boundaries
- The relationship patterns between them (Partnership, Customer-Supplier, etc.)
- The direction of dependencies
- Translation points (ACLs, open-host services)

The context map should be maintained and updated as the system evolves.

---

## Part II: Tactical Design

### Chapter 5: Implementing Simple Business Logic

#### Transaction Script

The Transaction Script pattern organizes business logic as a set of procedures, each handling one use case (one "transaction"). It follows a procedural programming style: receive input, execute business logic, return output. This is the simplest pattern, suitable for CRUD operations and straightforward business logic.

**When to use:** Simple business logic with few business rules, limited domain complexity, and no need for rich domain models. Typical in supporting and generic subdomains.

#### Active Record

The Active Record pattern represents business entities as objects that encapsulate both data and data access logic. Each entity knows how to load and save itself from/to the database. It adds a thin layer of domain behavior on top of data access.

**When to use:** When business logic involves validation rules and simple computations on data entities, but the complexity does not warrant a full domain model. More structured than Transaction Script, but still relatively simple.

#### Be Pragmatic

Not every subdomain needs a rich domain model. For generic and supporting subdomains, simpler patterns (Transaction Script, Active Record) are more appropriate and cost-effective. Reserve complex patterns for core subdomains where the investment pays off.

---

### Chapter 6: Tackling Complex Business Logic

#### Domain Model Pattern

The Domain Model pattern represents business concepts as rich objects with both data and behavior. It follows object-oriented design principles: encapsulation, polymorphism, and separation of concerns. This pattern is the heart of DDD's tactical design.

#### Building Blocks

The Domain Model pattern uses several building blocks defined by Eric Evans:

- **Value Objects:** Immutable objects identified by their attributes, not by identity. Two value objects with the same attributes are considered equal. Examples: `Money`, `DateRange`, `Address`.

- **Entities:** Objects with a distinct identity that persists over time, even if their attributes change. Examples: `Customer`, `Order`, `Ticket`.

- **Aggregate:** A cluster of entities and value objects treated as a single unit of consistency. Each aggregate has a root entity (the aggregate root) and a defined boundary. All access to objects within the aggregate must go through the root. Aggregates enforce business invariants (rules that must always be true).

- **Domain Events:** Records of things that have happened in the domain. They are named in past tense (e.g., `TicketCreated`, `PaymentProcessed`). Domain events enable loose coupling between aggregates and bounded contexts.

- **Repositories:** Interfaces for retrieving and persisting aggregates. Repositories abstract the data access mechanism, allowing the domain model to remain focused on business logic.

- **Factories:** Encapsulate complex object creation logic, ensuring that aggregates are always created in a valid state.

- **Domain Services:** Operations that do not naturally belong to any entity or value object. They coordinate between multiple aggregates or encapsulate cross-cutting domain logic.

#### Managing Complexity

The Domain Model pattern manages complexity through:
- **Encapsulation:** Business rules are encapsulated in domain objects
- **Ubiquitous Language alignment:** Code structure mirrors business concepts
- **Explicit boundaries:** Aggregates define consistency boundaries
- **Testability:** Business logic can be tested independently of infrastructure

---

### Chapter 7: Modeling the Dimension of Time

#### Event Sourcing

Event Sourcing is a pattern where instead of storing the current state of an aggregate, you store the sequence of domain events that led to that state. The current state is derived by replaying (folding) all events from the beginning.

Key concepts:
- **Events as source of truth:** Every state change is recorded as an immutable event
- **Event replay:** The aggregate's current state is computed by applying all historical events in order
- **Projections:** Different views of the event stream can be built for different query needs

#### Event Store

An event store is a specialized database optimized for storing and retrieving event streams. It supports:
- Appending new events to a stream
- Reading all events for a particular aggregate
- Subscribing to new events as they are appended

#### Advantages and Disadvantages

**Advantages:** Complete audit trail, ability to reconstruct any past state, natural fit for temporal queries, enables event-driven architectures.

**Disadvantages:** Increased complexity, eventual consistency challenges, event schema evolution, learning curve, storage growth.

**When to use:** Core subdomains with complex business rules involving temporal aspects, audit requirements, or the need to analyze historical data.

---

### Chapter 8: Architectural Patterns

#### Business Logic vs. Architectural Patterns

Business logic patterns (Transaction Script, Active Record, Domain Model) define how business logic is organized. Architectural patterns define how components interact and how dependencies flow. The two dimensions are independent and can be combined.

#### Layered Architecture

The classic three-layer architecture:
- **Presentation Layer:** Handles user interface, API endpoints, request/response formatting
- **Business Logic Layer:** Contains domain logic (using Transaction Script, Active Record, or Domain Model)
- **Data Access Layer:** Manages database interactions, ORM, repositories

Layers communicate top-down only: Presentation calls Business Logic, which calls Data Access. This keeps business logic independent of presentation concerns and data storage details.

**When to use:** Simple to moderate complexity, especially with Transaction Script or Active Record patterns.

#### Ports & Adapters (Hexagonal Architecture)

Ports & Adapters isolates the business logic from external concerns through:
- **Ports:** Interfaces defining how the application interacts with the outside world (driven ports for incoming requests, driving ports for outgoing interactions)
- **Adapters:** Implementations of ports that connect to specific technologies (REST controllers, database repositories, message queues)

The Dependency Inversion Principle ensures that the business logic defines interfaces (ports) and infrastructure provides implementations (adapters). The business logic has no dependencies on frameworks or external systems.

**When to use:** Domain Model pattern, especially for core subdomains where protecting the domain model from infrastructure concerns is important.

#### Command-Query Responsibility Segregation (CQRS)

CQRS separates the model into:
- **Write model (command side):** Optimized for processing commands and enforcing business rules. Uses the Domain Model pattern.
- **Read model (query side):** Optimized for querying data. Uses denormalized projections tailored to specific query needs.

**Polyglot Modeling:** The write and read models can use different data stores optimized for their respective workloads.

**Projecting Read Models:** As events are committed, projections update the read model in real-time (or near real-time).

**When to use:** High-complexity core subdomains where the read and write workloads have significantly different optimization needs.

---

### Chapter 9: Communication Patterns

#### Model Translation

When bounded contexts communicate, their different models must be translated. Two approaches:

- **Stateless Model Translation:** Translates data structures on the fly without maintaining state. The Anticorruption Layer is a stateless translator.

- **Stateful Model Translation:** Maintains state to track the relationship between models. Used when translation requires historical context (e.g., mapping external IDs to internal IDs).

#### Integrating Aggregates

Aggregates within and across bounded contexts need to communicate. Patterns include:
- **Outbox Pattern:** Ensures reliable event publishing by storing events in a database outbox table alongside business data, then a separate process publishes them to the message broker.
- **Saga Pattern:** Coordinates a long-running business transaction across multiple aggregates or services. Each step publishes an event that triggers the next step. Sagas handle compensation (rollback) through compensating events.
- **Process Manager:** A more sophisticated coordinator that maintains state and makes routing decisions. Unlike sagas, process managers have central intelligence and can choose different execution paths.

---

### Chapter 10: Design Heuristics

#### Bounded Contexts Heuristics

Guidelines for identifying bounded contexts:
- Start with subdomains as initial boundaries
- Consider organizational structure (Conway's Law)
- Watch for areas where the ubiquitous language becomes inconsistent
- Align with team boundaries where possible

#### Business Logic Implementation Patterns

Decision framework for choosing implementation patterns:
- **Core subdomains:** Domain Model or Event-Sourced Domain Model
- **Supporting subdomains:** Active Record or Transaction Script
- **Generic subdomains:** Transaction Script or off-the-shelf solutions

#### Architectural Patterns Decision Framework

- **Layered Architecture:** Transaction Script, Active Record, simple Domain Model
- **Ports & Adapters:** Domain Model, especially core subdomains
- **CQRS:** Event-Sourced Domain Model, high-complexity domains with divergent read/write needs

#### Testing Strategy

The book recommends different testing strategies based on the pattern:
- **Testing Pyramid:** For Transaction Script/Active Record (many unit tests, fewer integration tests)
- **Testing Diamond:** For Domain Model (balanced unit and integration tests, with emphasis on domain logic testing)
- **Reversed Testing Pyramid:** For CQRS/Event Sourcing (fewer unit tests, more integration and behavioral tests)

---

### Chapter 11: Evolving Design Decisions

#### Changes in Domains

Subdomains are not static -- they evolve over time. A subdomain's classification can change:
- **Core to Generic:** What was once a competitive advantage becomes commoditized (e.g., email systems)
- **Generic to Core:** A previously generic function becomes a differentiator
- **Supporting to Generic/Core:** As the business grows, previously minor functions gain importance
- **Core to Supporting:** What once differentiated the company becomes table stakes

#### Tactical Design Concerns

As complexity grows, implementation patterns can evolve:
- **Transaction Script to Active Record:** When data validation rules become more complex
- **Active Record to Domain Model:** When business rules become too complex for simple CRUD patterns
- **Domain Model to Event-Sourced Domain Model:** When temporal aspects and audit requirements become critical

#### Organizational Changes

Bounded context relationships evolve:
- **Partnership to Customer-Supplier:** As teams grow and need more independence
- **Customer-Supplier to Separate Ways:** When integration costs exceed benefits

---

## Part III: Applying DDD

### Chapter 12: EventStorming

#### What Is EventStorming?

EventStorming is a collaborative, visual workshop format for exploring business domains and designing event-driven systems. It brings together domain experts and engineers around a shared visual model using sticky notes on a wall.

#### The EventStorming Process

The process follows 10 steps:
1. **Unstructured Exploration:** Brainstorm domain events freely
2. **Timelines:** Organize events in chronological order
3. **Pain Points:** Identify problems and friction areas
4. **Pivotal Events:** Mark events that represent important business milestones
5. **Commands:** Add the actions that trigger each event
6. **Policies:** Add business rules and automated reactions
7. **Read Models:** Add data views needed for decisions
8. **External Systems:** Identify interactions with systems outside the bounded context
9. **Aggregates:** Group related events and commands into aggregates
10. **Bounded Contexts:** Identify boundaries where different languages/models apply

---

### Chapter 13: Domain-Driven Design in the Real World

#### Strategic Analysis

Applying DDD to real-world systems starts with strategic analysis:
- **Understand the business domain:** Identify the company's core business and subdomains
- **Explore the current design:** Map existing systems to subdomains and identify misalignments
- **Modernization strategy:** Develop a plan for evolving the system toward better domain alignment

#### Strategic Modernization

Large-scale modernization efforts should be business-driven, not technology-driven. Approaches include:
- **Strangler Fig pattern:** Gradually replace legacy components by routing new functionality to new systems
- **Event-based modernization:** Introduce events to decouple legacy and new systems

#### Tactical Modernization

Incremental improvements within bounded contexts:
- Refactor toward a ubiquitous language
- Introduce bounded context boundaries in code
- Evolve from simpler to more complex patterns as needed

#### Cultivate a Ubiquitous Language

Building a ubiquitous language in existing systems requires:
- Documenting current terminology
- Identifying inconsistencies and ambiguities
- Establishing glossaries and shared definitions
- Refactoring code to use consistent naming

---

## Key Takeaways

1. **DDD is about understanding business domains, not writing code.** The strategic design phase (analyzing subdomains, establishing bounded contexts, defining ubiquitous language) is more impactful than tactical implementation choices.

2. **Three subdomain types drive three different strategies.** Core subdomains warrant the highest investment in modeling and implementation. Supporting subdomains should use simpler patterns. Generic subdomains should use existing solutions when possible.

3. **Bounded contexts manage complexity through explicit boundaries.** Each bounded context has its own ubiquitous language and domain model. Inconsistencies between contexts are not errors -- they reflect different perspectives serving different purposes.

4. **The ubiquitous language is the foundation.** A shared, rigorous language used by both domain experts and developers ensures that software accurately reflects business needs. It must be consistent within a bounded context.

5. **Choose implementation patterns based on complexity.** Not every subdomain needs a rich domain model. Transaction Script and Active Record are appropriate for simpler subdomains. Reserve the Domain Model and Event Sourcing for core subdomains where the complexity justifies the investment.

6. **Aggregates define consistency boundaries.** Each aggregate enforces business invariants within its boundary. Design aggregates to be small, focused, and aligned with business transactions.

7. **Bounded contexts integrate through well-defined patterns.** Anticorruption Layers protect model integrity. Open-Host Services standardize integration. Context Maps visualize the overall integration landscape.

8. **Architecture patterns serve the business logic pattern.** Layered Architecture for simple logic, Ports & Adapters for Domain Models, and CQRS when read and write workloads diverge significantly.

9. **Design decisions evolve over time.** Subdomains change classification, implementation patterns grow in complexity, and organizational relationships shift. DDD is not a one-time exercise but an ongoing discipline.

10. **EventStorming is the most effective discovery tool.** The collaborative, visual workshop format breaks down communication barriers between domain experts and engineers, producing both domain knowledge and design artifacts in a single session.
