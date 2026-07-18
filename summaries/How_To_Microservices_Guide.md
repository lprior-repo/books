# How To: Get Started with Microservices - Dave Farley's Better Software Faster Guide

## Comprehensive Summary

---

## Introduction

This guide, part of Dave Farley's "Better Software Faster" series, is a concise yet densely packed introduction to microservices architecture. Farley, a pioneer of Continuous Delivery and co-author of the foundational Continuous Delivery book, distills years of practical experience into a focused guide on how to adopt microservices effectively. The guide does not merely describe what microservices are -- it provides a principled, engineering-driven approach to designing, building, and evolving microservice-based systems. Its central thesis is that microservices are not simply about splitting a system into small pieces; they require deliberate design sophistication, a deep understanding of the problem domain, and rigorous attention to the boundaries and contracts between services. The guide covers the nature of microservices, the importance of independent deployability, the role of Bounded Contexts from Domain-Driven Design, a pragmatic approach to system decomposition, the design of messaging and communication between services, and the critical practice of Contract Testing. Throughout, Farley emphasizes iteration, learning, and evolution over upfront planning.

Dave Farley is not merely a commentator on software architecture -- he was one of the original signatories of the Agile Manifesto and has spent decades building real systems at scale. His consulting work and his Continuous Delivery YouTube channel have made his thinking on software engineering practices accessible to a wide audience. This guide reflects that practical orientation: it is not an academic treatment of microservices theory, but a hands-on guide for practitioners who want to adopt microservices in a way that actually works. It focuses on the decisions that matter most and the mistakes that are most commonly made.

The guide is structured around a small number of core ideas, each of which has profound implications for how you design, build, and operate a microservices system. It begins by establishing what microservices are and why they matter, then moves into the practical challenges of identifying service boundaries, designing the communication between services, and verifying that services remain compatible as they evolve independently. Every recommendation is grounded in the principle that microservices exist to enable organizational scalability through independent deployability, and that any practice that undermines independent deployability is working against the fundamental purpose of the architecture.

---

## Chapter 1: What Are Microservices?

### Microservices as a Distributed Systems Architecture

Farley begins by defining microservices as both a distributed systems architecture and a distributed development architecture. This dual nature is essential to understanding why microservices have become one of the most popular architectural approaches in modern software engineering. As a distributed systems architecture, microservices structure an application as a collection of loosely coupled, independently operating services that communicate over a network. As a distributed development architecture, they enable software development work to be distributed across many small, independent teams, each responsible for one or a small number of services.

This dual characterization is critical because it highlights that the benefits of microservices are not purely technical. The organizational scalability -- the ability to grow a large development organization without the coordination overhead of a single monolithic codebase -- is often the primary motivation for adopting microservices. However, Farley is clear-eyed about the costs: the distributed nature of the system introduces significant complexity. You do not get to build, test, and deploy everything together, which means that the engineering practices around integration, testing, and deployment must be significantly more sophisticated than in a monolithic approach.

To appreciate what Farley means by "distributed systems architecture," consider the operational realities. In a monolithic system, a single process handles all business logic. Function calls are local, in-memory, and essentially free in terms of latency. In a microservices architecture, what were once local function calls become remote network calls, with all the attendant challenges: network latency, partial failures, retries, timeouts, message serialization and deserialization, and the need for service discovery. The CAP theorem rears its head. You must reason about eventual consistency rather than strong consistency. These are not minor inconveniences -- they are fundamental shifts in how you think about building software.

On the development side, a distributed development architecture means that multiple teams work on different parts of the system simultaneously, each with their own codebase, their own build pipeline, and their own release schedule. This eliminates many of the coordination bottlenecks that plague large monolithic projects -- merge conflicts, release train delays, and the need for cross-team approval of changes. But it introduces new challenges: how do you ensure that the services work together correctly when no single team has visibility into the entire system? How do you prevent one team from making a change that breaks another team's service? These are the questions that drive Farley's recommendations throughout the guide.

### Microservices Are Small

A defining characteristic of microservices is their small size. Farley offers a concrete heuristic: a microservice should be small enough that it can be rewritten in one to two weeks. This is not an arbitrary measure -- it captures the idea that a microservice should be focused, coherent, and limited in scope. If a service is so large that rewriting it would take months, it is likely doing too many things and has become a mini-monolith.

However, Farley is careful to distinguish between smallness and arbitrary decomposition. The goal is not simply to break a large system into many tiny pieces. Rather, the goal is to create autonomous services that are aligned with the problem domain. Each service should be focused on doing one task -- and doing it well. This principle of cohesion, drawn from decades of software design wisdom, remains central even in the microservices paradigm. The smallness of a microservice is a consequence of its focus, not the other way around.

The rewrite heuristic also has practical implications for risk management. If a service can be rewritten in one to two weeks, the cost of getting the design wrong is relatively low. This encourages experimentation and iterative refinement, which are themes that run throughout the guide. Teams can afford to try a service boundary, observe how well it works in practice, and adjust if necessary, without incurring catastrophic costs.

It is worth noting that the one-to-two-weeks rewrite heuristic is not universally accepted. Some practitioners argue that microservices should be sized based on team capacity (the "two-pizza team" concept popularized by Amazon) rather than on a rewrite estimate. Others argue that the right size depends on the domain and the organizational context. Farley's heuristic is valuable precisely because it is concrete and testable: you can ask, "Could we rewrite this service in two weeks?" and if the answer is no, you have a clear signal that the service may be too large. Whether you adopt this exact heuristic or a variant, the underlying principle is the same: services should be small enough to be manageable by a single team, and their scope should be narrow enough that the cost of changing or even replacing them is bounded.

The emphasis on "doing one task and doing it well" echoes the Unix philosophy, and this is not accidental. The Unix philosophy of small, composable tools has proven its effectiveness over decades, and microservices can be seen as an application of this philosophy to distributed systems. Each service is like a Unix command: focused, composable, and replaceable. The power of the system comes not from the individual services but from the way they are composed together to solve complex problems.

---

## Chapter 2: Independent Deployability -- The Core Property

### What Independent Deployability Means

Farley identifies independent deployability as the single most important property of a microservice architecture. Services must be deployable without requiring coordinated deployments of other services. This is what distinguishes a genuine microservices architecture from a distributed monolith -- a system that has been decomposed into separate services but that still requires tightly coordinated releases because of coupling between them.

Independent deployability is what allows teams to make progress in parallel, without being constrained by dependencies on other services and other teams. When service A can be updated and deployed without any coordination with service B, the teams owning those services can work at their own pace, on their own schedules, without blocking each other. This parallelism is the key to organizational scalability -- it is the most scalable way to grow a large development team.

### The Cost of Independent Deployability

Farley does not shy away from the cost side of this equation. The price of independent deployability is that you cannot build, test, and deploy everything together. In a monolithic system, integration testing is relatively straightforward because all the code runs in the same process. In a microservices system, integration happens across network boundaries, and the testing strategies must account for this.

This is where many organizations stumble. They decompose their system into microservices but continue to rely on integration testing strategies that require all services to be running together in a shared test environment. This leads to slow feedback, fragile tests, and deployment bottlenecks -- exactly the problems that microservices were supposed to solve. Farley's solution, discussed later in the guide, centers on Contract Testing as a way to verify service compatibility without requiring full integration environments.

### Why This Matters for Scaling

The fundamental value proposition of microservices, according to Farley, is organizational scalability. The goal is to enable many teams to work independently on a shared system without stepping on each other's toes. Independent deployability is the mechanism that makes this possible. Without it, you have the complexity of a distributed system without the benefits -- the worst of both worlds.

This insight has important implications for how you evaluate whether a microservices approach is appropriate for your situation. If your organization is small enough that everyone can work on the same codebase without significant coordination overhead, the added complexity of microservices may not be justified. The benefits scale with the size of the organization and the system. Farley implicitly suggests that microservices are a solution to a scaling problem, not a solution to a design problem in and of themselves.

### The Distributed Monolith Anti-Pattern

One of the most valuable warnings implicit in Farley's guide is the danger of the distributed monolith. This is a system that has been decomposed into separate services but where the coupling between services is so tight that they must be deployed together, tested together, and often even developed together. The result is a system that has all the complexity of a distributed system -- network calls, partial failures, deployment coordination -- but none of the benefits. It is, in many ways, worse than a monolith, because you have paid the cost of distribution without reaping the reward of independent deployability.

The distributed monolith typically arises from one of several root causes. First, services may share a database, creating tight coupling through shared schema. Second, services may have chatty, synchronous communication patterns that create temporal coupling -- if service A requires a synchronous response from service B to complete a request, then B must be available whenever A is serving requests. Third, services may be decomposed along technical rather than domain boundaries, leading to artificial decomposition that does not reflect the natural structure of the problem. Farley's emphasis on Bounded Contexts, asynchronous messaging, and independent data stores is precisely targeted at avoiding these failure modes.

### Deployment Independence in Practice

To understand what deployment independence looks like in practice, consider the alternative. In many organizations that have adopted microservices poorly, a release involves coordinating the deployment of multiple services simultaneously. Release windows are scheduled, all affected teams must be ready, and the deployment is treated as a high-risk event. This is the antithesis of what microservices are supposed to achieve.

In a well-designed microservices architecture, deploying a service should be as routine as deploying a single application. The team that owns the service decides when to deploy, runs their automated tests, and pushes to production. If the deployment causes a problem, it is rolled back. Other teams are not involved and may not even be aware that the deployment happened. This is only possible when the service boundaries are well-designed, the messaging contracts are stable and versioned, and Contract Testing is in place to catch breaking changes before they reach production.

---

## Chapter 3: Bounded Contexts -- Aligning Services with the Problem Domain

### The Concept of a Bounded Context

Farley introduces Bounded Contexts as the key design tool for identifying good service boundaries. This concept, drawn from Eric Evans' Domain-Driven Design, is one of the most influential ideas in modern software architecture, and Farley gives it central prominence in his guide.

A Bounded Context is an area of the problem domain within which ideas and concepts have a consistent meaning. Farley illustrates this with a clear example from a bookstore. In the part of the system that helps customers find books they want to buy, the concept of a "book" includes attributes like price, cover art, reviews, and description. In the part of the system that handles shipping and distribution, the concept of a "book" includes attributes like weight, dimensions, and destination. Although both areas deal with "books," the meaning of "book" is different in each context. These are different Bounded Contexts.

### Why Bounded Contexts Make Good Service Boundaries

The reason Bounded Contexts make excellent service boundaries is that they are naturally decoupled from one another. If the shipping context has its own model of a book, changes to the sales context's model of a book do not directly affect it. The coupling between the two contexts is limited to the information that crosses the boundary -- for example, when a book is purchased, the sales context might notify the shipping context that a shipment is needed. But the internal details of how each context models a book are independent.

This natural decoupling is what makes Bounded Contexts such powerful service boundaries. They provide a principled basis for decomposition that is grounded in the problem domain rather than in technical concerns. Services aligned with Bounded Contexts tend to be cohesive (they do one thing well) and loosely coupled (they have minimal dependencies on other services), which are exactly the properties needed for independent deployability.

### The Difficulty of Stable Interfaces

Farley is candid about the difficulty of defining interfaces between services that are sufficiently stable and loosely coupled. The challenge is to prevent change in one service from forcing change in another, while still allowing the services to communicate and collaborate effectively. This is a hard problem, and Farley suggests that it requires ongoing attention and refinement rather than a one-time solution.

The interface between services is, in many ways, the most important part of the system design. It is the seam along which the system can evolve independently, and if it is poorly designed, it becomes the point where change propagates uncontrollably. Farley's advice throughout the guide consistently emphasizes treating these boundaries with special care and investing in the design of the messages and conversations that cross them.

### A Worked Example: The Online Bookstore

To make the Bounded Context concept concrete, consider a more detailed exploration of Farley's bookstore example. An online bookstore has several distinct areas of concern:

- **Catalog/Browsing**: This is the part of the system that helps customers find books. Its model of a "book" includes the title, author, cover art, synopsis, price, customer reviews, and recommendations. The primary operations are searching, browsing, and reading reviews.

- **Order Management**: This is the part of the system that handles the purchasing process. Its model of a "book" might be reduced to a SKU, a title (for display on receipts), and a price. The primary operations are adding to cart, checking out, and payment processing.

- **Shipping/Fulfillment**: This is the part of the system that handles getting physical books to customers. Its model of a "book" includes the SKU, weight, dimensions, and warehouse location. The primary operations are picking, packing, and shipping.

- **Inventory Management**: This is the part of the system that tracks how many copies of each book are in stock. Its model of a "book" is essentially a SKU and a quantity. The primary operations are decrementing stock on sale and reordering from suppliers.

Each of these areas has a different model of "book" with different attributes and different operations. They are different Bounded Contexts, and they make excellent service boundaries. The Catalog Service does not need to know about shipping weights. The Shipping Service does not need to know about customer reviews. The only information that crosses boundaries is what is necessary for the services to collaborate -- for example, when an order is placed, the Order Service sends a message to the Shipping Service with just enough information to create a shipment (the SKU, the shipping address, and the customer name). It does not send the entire "book" model because the Shipping Service does not need it.

This example illustrates why Farley insists on translation at boundaries. The "Order Placed" message that goes from the Order Service to the Shipping Service is not just a copy of the Order Service's internal data -- it is a purpose-built message that contains exactly what the Shipping Service needs, expressed in terms that make sense in the shipping context. This translation insulates the services from each other's internal design decisions.

---

## Chapter 4: Design -- A Pragmatic, Iterative Approach

### The Misguided Rush to Separate Repositories

Farley opens his design advice with a strong warning against a common mistake: rushing to set up a separate repository for each new service at the beginning of a project. He describes this as misguided because it is almost impossible to comprehensively define the services, their interfaces, and their messaging upfront. By prematurely decomposing services into separate repositories, the process of learning about the problem domain and evolving the system becomes much more complex and risky.

This advice is rooted in a deep understanding of software development as an inherently uncertain and exploratory activity. Farley recognizes that you do not know the optimal service boundaries at the start of a project. You have to discover them through experimentation and learning. When services are in separate repositories, the cost of restructuring boundaries -- moving functionality from one service to another, merging services, or splitting them differently -- is much higher. You have to coordinate changes across multiple repositories, manage cross-repository dependencies, and deal with the logistical overhead of multi-repo development.

This is one of the most counter-intuitive pieces of advice in the guide, because it goes against the common practice of creating a new repository for each new service. Many teams interpret "microservices" to mean "separate codebases from day one," and they set up their project scaffolding accordingly. Farley argues that this is premature optimization of the wrong thing. You are optimizing for the final state of the system (separate services in separate repositories) before you understand what the system should look like. This is analogous to optimizing code for performance before you have measured where the bottlenecks are -- it is effort spent in the wrong place at the wrong time.

The practical difference is significant. Consider a team that needs to move a piece of functionality from Service A to Service B because they have discovered that the boundary is in the wrong place. In a single-repository setup, this is a refactoring operation: move the code, update the tests, verify that everything still works. In a multi-repository setup, this requires coordinating changes across two repositories, potentially updating shared libraries or message schemas, and ensuring that both services remain compatible throughout the transition. The cost is orders of magnitude higher, which means teams are much less likely to do it -- even when they know the boundary is wrong.

### Start with a Single Repository

Instead, Farley advocates starting with a single repository. This allows the team to think about the problem, play with different models, and create an initial best guess at a good design without the overhead of multi-repo coordination. The idea is to identify concepts that seem like good candidates for separate services, create them within the single repository, and then evaluate how well the boundaries work in practice.

This approach has several advantages. First, it reduces the cost of experimentation. Restructuring code within a single repository is vastly easier than restructuring across multiple repositories. Second, it enables faster feedback. All the code is in one place, so it is easier to run comprehensive tests and observe how the services interact. Third, it supports collaborative learning. When everything is in one repository, it is easier for team members to see and understand the full system, which facilitates the kind of cross-team learning that leads to better designs.

Farley's recommendation to "write some code" is also significant. He is not advocating for extensive upfront modeling sessions or design documentation. He wants teams to build something tangible quickly, test it in a shared deployment pipeline, and learn from the results. This is consistent with the engineering mindset that pervades his work: design is validated by building and testing, not by analysis and discussion. The code is the design, and the test results are the validation.

The single-repository approach also has implications for team organization. In the early stages, the team should be working closely together, sharing knowledge and building a collective understanding of the domain. This is not the time for each team to retreat into its own silo. The eventual goal is independent teams owning independent services, but the path to that goal goes through a period of close collaboration and shared learning. Farley's process acknowledges this by keeping everything together until the team has developed enough shared understanding to make informed decisions about how to split.

### Iterate and Refine

Farley's design process is fundamentally iterative. You make your best guess at the initial service boundaries, implement them, test them, and then refine them based on what you learn. This is a form of empirical design -- you learn by doing rather than by planning. The goal is to iterate quickly, and by keeping everything in the same repository, you can evaluate and evolve your ideas more easily.

This iterative approach aligns with the broader principles of Continuous Delivery and Agile development, both of which Farley has long championed. The idea is to create fast feedback loops that allow you to learn quickly and adapt. In the context of microservices design, this means being willing to change service boundaries as your understanding of the problem domain deepens.

### Event Storming as a Design Tool

Farley recommends Event Storming as a technique for the creative exploration of service boundaries. Event Storming, invented by Alberto Brandolini, is a collaborative workshop format in which participants model a business process by identifying the domain events that occur within it. Domain events are things that happen in the business -- for example, "Order Placed," "Payment Received," "Book Shipped." By mapping out these events and the relationships between them, participants gain a shared understanding of the business process and can identify natural boundaries between different areas of concern.

Event Storming is particularly well-suited to microservices design because it naturally reveals the seams in the business process -- the points where different concerns intersect and where information flows from one area to another. These seams often correspond to Bounded Context boundaries and therefore to good service boundaries.

A typical Event Storming session involves a diverse group of participants: developers, domain experts, product owners, testers, and anyone else who has knowledge of the business process. The group works together on a large wall (physical or virtual), using colored sticky notes to represent different types of elements: domain events (orange), commands (blue), external systems (pink), and aggregates (yellow). The process starts with a chaotic exploration of all the events that occur in the business process, and then gradually organizes them into a timeline. As the timeline takes shape, clusters of related events emerge, and the boundaries between these clusters often reveal natural service boundaries.

The power of Event Storming lies in its ability to surface hidden assumptions and disagreements. When a domain expert says "Order Placed" and a developer says "Payment Initiated," they may be talking about the same thing -- or they may not. The collaborative, visual nature of the workshop forces these discrepancies into the open, where they can be resolved. This shared understanding is invaluable when it comes to designing service boundaries, because the quality of the boundaries depends on the quality of the team's understanding of the domain.

### Identifying Common Concepts Across Contexts

Farley advises paying attention to common ideas that occur across different parts of the problem domain. Using the bookstore example, he notes that "customer" and "book" are both important concepts that appear in multiple parts of the system, but with different meanings. In the sales context, a book has attributes like price and cover art. In the distribution context, a book has attributes like weight and destination. The fact that the same concept has different attributes in different contexts is a strong signal that these are different Bounded Contexts, and therefore good candidates for separate services.

This approach to identifying service boundaries is fundamentally domain-driven. Rather than decomposing the system along technical lines (for example, separating the database layer from the business logic layer from the presentation layer), you decompose it along domain lines, aligning each service with a coherent area of the business. This leads to services that are more stable, more cohesive, and more aligned with the way the business actually operates.

### Creating Separate Repositories Only When Stable

The final step in Farley's design process is to create separate repositories for services only as the design stabilizes. This is a deliberately conservative approach. By waiting until the service boundaries are well-understood and well-tested before splitting into separate repositories, you minimize the risk of getting the boundaries wrong and then having to pay the high cost of restructuring across repositories.

This does not mean that you should never have separate repositories -- Farley is clear that microservices should eventually live in their own repositories. The key is timing: do it when you have confidence in your boundaries, not before. This is a practical application of the principle of deferring commitment -- you delay irreversible (or high-cost) decisions until you have enough information to make them wisely.

---

## Chapter 5: Messaging -- Designing Communication Between Services

### The Inevitable Coupling of Communication

When services need to communicate to do useful work, there is inevitably some degree of coupling. Farley acknowledges this as a fundamental reality of distributed systems. The question is not whether there will be coupling between services, but how much coupling there will be and where it will be concentrated. The goal is to minimize coupling, particularly the kind of coupling that forces changes to propagate from one service to another.

Farley's approach to managing this coupling is multi-faceted, encompassing the structure of messages, the design of translation layers, and the use of testing strategies to verify compatibility without full integration.

### Messages as a Separate Bounded Context

One of Farley's most important recommendations is to treat the messages that pass between services as a separate Bounded Context, distinct from the services themselves. This is a subtle but powerful insight. The messages that a service sends and receives represent a contract -- an agreement about what information will be exchanged and in what format. This contract is conceptually separate from the internal implementation of the service.

By treating messages as a separate concern, you can keep the code that translates inputs and formulates outputs distinct from the internal business logic. Farley identifies this as the Ports and Adapters pattern (also known as Hexagonal Architecture), originally described by Alistair Cockburn. In this pattern, the core business logic of a service is surrounded by adapters that handle the translation between external message formats and internal data structures.

### The Ports and Adapters Pattern in Detail

The Ports and Adapters pattern provides a clean separation between the inside and the outside of a service. The "inside" is the domain model and business logic -- the code that implements the service's core functionality. The "outside" is everything else: the messages that come in from other services, the protocols used to communicate, the data formats, and so on. "Ports" are interfaces that define how the inside communicates with the outside, and "Adapters" are implementations of those interfaces that handle the specifics of particular communication mechanisms.

In the context of microservices, this pattern has several important benefits. First, it keeps the internal logic of a service independent of the format and structure of the messages it exchanges with other services. This means that the internal logic can change without affecting the external contract, and vice versa. Second, it allows a service to support multiple versions of its message formats simultaneously, by providing multiple adapters. This is crucial for independent deployability -- when you deploy a new version of a service with a changed message format, you can continue to support the old format while consumers migrate at their own pace. Third, it makes testing easier, because you can test the internal logic in isolation from the external communication concerns.

To illustrate how this works in practice, consider a service that processes orders. Internally, the service might represent an order as a rich domain object with methods like `addItem()`, `calculateTotal()`, and `submit()`. Externally, however, the service receives messages in a specific format -- perhaps a JSON payload over HTTP. The adapter layer receives the JSON, validates it, and translates it into the internal domain model. When the service needs to notify other services about a state change (for example, that an order has been submitted), another adapter translates the internal state into the appropriate outgoing message format.

This separation means that if the team decides to change the internal domain model -- perhaps refactoring `Order` into `DraftOrder` and `SubmittedOrder` -- the external message format remains unchanged. The adapter simply maps the new internal model to the existing external format. Similarly, if the team decides to change the external API -- perhaps adding a new field to the "Order Submitted" message -- the adapter can be updated to populate the new field from the existing internal model, without any changes to the business logic.

### Versioning and Backward Compatibility

One of the most challenging aspects of microservices is managing the evolution of message schemas over time. When a service changes its API, existing consumers may break if the change is not backward-compatible. The Ports and Adapters pattern helps with this by providing a natural place to manage versioning.

A common approach is to have one adapter per supported version of the API. When a new version is introduced, a new adapter is created alongside the existing one. The service then routes incoming messages to the appropriate adapter based on the version identifier in the message. Old adapters can be retired when all consumers have migrated to the new version. This approach allows services to evolve their APIs without forcing immediate migration on all consumers, which is essential for independent deployability.

Farley explicitly mentions this capability when he notes that "we can even support multiple versions of messages with multiple translators." This is a direct benefit of the Ports and Adapters pattern and one of the key reasons he recommends it so strongly. Without this separation, version management becomes entangled with business logic, making both harder to understand and maintain.

### Translating Concepts Across Bounded Contexts

Farley emphasizes the importance of translating the concepts that cross boundaries between Bounded Contexts. This is a key principle from Domain-Driven Design: when information flows from one Bounded Context to another, it must be translated into the terms and models of the receiving context. There is no universal "book" model that works perfectly for every context. Instead, each context has its own model, and the translation between models happens at the boundary.

This approach prevents the need for a massive, universal data structure that tries to work in every possible context. Such a structure is impossible to design well (because different contexts have different needs) and creates maximum coupling (because any change to the structure affects every context that uses it). By translating at the boundary instead, each context remains free to evolve its own model independently.

The practical implication is that each service should have a clear translation layer at its boundary. Incoming messages are translated from the external format into the service's internal model. Outgoing messages are translated from the internal model into the external format. This translation layer is where versioning, backward compatibility, and schema evolution are managed.

### Avoiding Technically-Focused Messages

Farley advises against technically-focused messages and recommends modeling the "conversations" that messages represent at the level of the problem domain. This means that messages should be expressed in terms that a non-technical person can understand. Instead of sending a message like "UpdateRecord(table='orders', id=123, fields={status: 'shipped'})", you should send a message like "OrderShipped(orderId=123, shippedDate=...)". The former is a technical operation that exposes the internal structure of the service. The latter is a domain event that communicates what happened in business terms.

This principle has several benefits. First, it makes the communication between services more understandable and auditable. Anyone who understands the business can read the messages and understand what is happening. Second, it reduces coupling, because domain-level messages tend to be more stable than technical operations. The business events in a domain change less frequently than the internal implementation details of the services. Third, it aligns the technical architecture with the business architecture, which makes the system easier to reason about and evolve.

### Treating Boundaries with Special Care

Farley repeatedly emphasizes that the boundary between services is an important part of the design of the system and should be treated with special care. Microservices only really make sense as a way to scale up development, so deployment independence and loose coupling are critical to achieving that goal. Every design decision at the boundary should be evaluated in terms of its impact on deployment independence and coupling.

This means investing in the design of interfaces, message schemas, and versioning strategies. It means being thoughtful about what information crosses boundaries and how. It means treating the boundary as a first-class part of the design, not an afterthought. And it means being willing to refactor boundaries when they are not working well, even if that requires significant effort.

### Contract Testing

Farley recommends Contract Testing as a way to verify service compatibility without requiring full integration testing. Contract Testing is a technique in which each service consumer defines a contract that specifies the messages it expects to send and receive from a service provider. The provider then verifies that it satisfies all of its consumers' contracts. This allows you to detect breaking changes -- changes to a service's interface that would cause its consumers to fail -- without having to run all the services together in a shared test environment.

Contract Testing is a crucial enabler of independent deployability. Without it, the only way to verify that a change to one service does not break its consumers is to run integration tests that exercise the real interactions between services. This requires a shared test environment with all services running, which is slow, expensive, and fragile. Contract Testing replaces this with a faster, more reliable approach: each service is tested in isolation against the contracts defined by its consumers, and compatibility is verified without needing to run any other service.

The guide points to Pact as a tool for Contract Testing. Pact is a consumer-driven contract testing framework that allows consumers to define their expectations and providers to verify against them. In the Pact model, the consumer writes a test that specifies what requests it will make and what responses it expects. This test generates a contract file. The provider then runs a verification step that replays the consumer's expected requests against the provider and verifies that the responses match the expectations.

### How Contract Testing Works in Practice

To understand the value of Contract Testing, consider a concrete scenario. Suppose you have an Order Service (consumer) and an Inventory Service (provider). The Order Service needs to check whether a book is in stock before allowing a customer to place an order. It does this by sending a request to the Inventory Service and receiving a response that includes the stock level.

In a traditional integration test, you would stand up both services in a test environment, have the Order Service send a real request to the Inventory Service, and verify the response. This requires both services to be running, both databases to be populated with test data, and the network to be functioning correctly. It is slow, fragile, and expensive to maintain.

With Contract Testing, the process is different. The Order Service team writes a contract test that specifies: "When I send a GET request to /inventory/SKU123, I expect to receive a 200 response with a JSON body containing {"sku": "SKU123", "inStock": true, "quantity": 5}." This test generates a contract file that is shared with the Inventory Service team. The Inventory Service team then runs a provider verification that takes this contract and replays the specified request against their service, verifying that the actual response matches the expected response.

If the Inventory Service team makes a change that breaks the contract -- for example, renaming "inStock" to "available" -- the provider verification fails immediately, alerting them to the breaking change before it reaches production. The Order Service team never has to run the Inventory Service, and the Inventory Service team never has to run the Order Service. Compatibility is verified through the contract, not through direct integration.

### Contract Testing vs. Integration Testing

It is important to understand that Contract Testing is not a replacement for all integration testing. Contract Testing verifies that the messages a service sends and receives conform to the expected format and structure. It does not verify the end-to-end behavior of the system -- for example, that placing an order in the Order Service correctly decrements inventory in the Inventory Service and triggers a shipment in the Shipping Service.

End-to-end integration testing still has a role, but it should be used sparingly and strategically. The bulk of your confidence should come from unit tests, contract tests, and the fast feedback loops they provide. End-to-end tests should cover only the most critical business scenarios and should be treated as a small, targeted complement to the broader testing strategy, not as the primary source of confidence.

Farley's approach is consistent with the testing pyramid: many fast, reliable unit tests at the base, a moderate number of contract tests in the middle, and a small number of end-to-end integration tests at the top. This provides fast feedback on most issues (unit and contract tests) while still catching the rare end-to-end problems that can only be detected by running the full system.

---

## Chapter 6: A Practical Workflow for Getting Started

### Putting It All Together

Farley's guide can be read as a step-by-step workflow for adopting microservices. The following synthesis draws together the threads from each section into a coherent process.

**Step 1: Explore the Problem Domain**
Begin by understanding the problem domain deeply. Use techniques like Event Storming to map out the business processes, identify the key domain events, and reveal the natural boundaries between different areas of concern. Engage domain experts, stakeholders, and the development team in this exploration. The goal is to develop a shared understanding of the problem space and to identify candidate Bounded Contexts.

**Step 2: Start with a Single Repository**
Resist the temptation to immediately split into multiple repositories. Begin with a single repository where you can experiment freely with different service boundaries and models. Write code, test it, and evaluate how well your design guesses work out. Keep everything in a single Deployment Pipeline shared between teams to get fast feedback.

**Step 3: Identify Candidate Services**
Based on your domain exploration, identify concepts that make good candidates for separate services. Look for areas where the same concept has different meanings in different contexts -- these are strong indicators of Bounded Context boundaries. For each candidate service, consider whether it can be rewritten in one to two weeks and whether it aligns with a coherent area of the business.

**Step 4: Design the Messaging**
For each pair of services that need to communicate, design the messages and conversations between them. Treat messages as a separate Bounded Context, distinct from the services. Use the Ports and Adapters pattern to keep message translation separate from business logic. Model messages at the level of the problem domain, not at the technical level. Avoid technically-focused messages.

**Step 5: Test and Iterate**
Run the services together (still in the single repository) and observe how well the boundaries work. Are the services cohesive? Are they loosely coupled? Do changes in one service frequently force changes in another? Use this feedback to refine the boundaries. Be willing to merge services, split them differently, or move functionality between them.

**Step 6: Introduce Contract Testing**
As the design stabilizes, introduce Contract Testing to verify service compatibility. Have each consumer define its expectations, and have each provider verify that it satisfies those expectations. This creates a safety net that catches breaking changes early and enables confident independent deployment.

**Step 7: Split into Separate Repositories**
Once you have confidence in the service boundaries and the messaging design, create separate repositories for each service. At this point, the boundaries should be stable enough that the cost of cross-repository restructuring is unlikely to be needed. Continue to use Contract Testing to maintain compatibility as services evolve independently.

---

## Chapter 7: Key Principles and Themes

### Independent Deployability Is Paramount

The single most important property of a microservice architecture is independent deployability. Every design decision should be evaluated in terms of whether it supports or undermines this property. If a design choice creates coupling that requires coordinated deployment, it is working against the fundamental goal of the architecture.

### Domain-Driven Decomposition

Service boundaries should be aligned with Bounded Contexts from the problem domain, not with technical concerns. This ensures that services are cohesive, loosely coupled, and stable. Domain-driven boundaries also make the system more understandable to both developers and business stakeholders.

### Iteration Over Upfront Design

Farley consistently advocates for an iterative, empirical approach to microservices design. You cannot know the optimal boundaries upfront, so you must discover them through experimentation and learning. This requires fast feedback loops and a willingness to change course when evidence suggests that a boundary is not working well.

### Separate Repositories Are a Maturity Step, Not a Starting Point

Creating separate repositories for each service should be a late step in the adoption process, not an early one. Premature separation into multiple repositories makes it harder to learn, experiment, and evolve the design. Wait until the boundaries are stable before splitting.

### The Boundary Is a First-Class Design Concern

The interface between services -- the messages, contracts, and translation layers -- deserves the same level of design attention as the internal logic of each service. Treat the boundary as a separate Bounded Context, use the Ports and Adapters pattern, and model messages at the domain level.

### Contract Testing Enables Independent Deployment

Contract Testing is the key testing strategy for microservices. It allows you to verify service compatibility without requiring full integration environments, enabling fast feedback and confident independent deployment.

---

## Chapter 8: Connections to Broader Practices

### Continuous Delivery

Farley's approach to microservices is deeply informed by his work on Continuous Delivery. The emphasis on fast feedback loops, deployment pipelines, and iterative refinement are all hallmarks of the Continuous Delivery philosophy. In many ways, the guide can be read as an application of Continuous Delivery principles to the specific challenge of microservices architecture.

The guide's recommendation to share a single Deployment Pipeline between teams in the early stages is particularly noteworthy. This ensures that all services are continuously integrated and tested together, providing fast feedback on the quality of the design decisions. As the design stabilizes and services move to separate repositories, each service will have its own pipeline, but the principle of continuous integration and fast feedback remains.

The Deployment Pipeline concept is central to Continuous Delivery. A Deployment Pipeline is an automated process that takes code from commit to release through a series of stages: build, unit test, integration test, acceptance test, and deployment. Each stage provides increasing confidence that the code is ready for production. In the context of microservices, the Deployment Pipeline for each service should include contract testing as a stage, so that breaking changes are caught before the service is deployed.

Farley's recommendation to start with a shared Deployment Pipeline in a single repository is a direct application of the Continuous Delivery principle of fast feedback. When all services are built and tested together, problems are detected immediately. As the design matures and services move to separate repositories, each service gets its own pipeline, but the contract testing stage ensures that compatibility is continuously verified across service boundaries.

### The Relationship Between CI and Microservices

Continuous Integration (CI) and microservices have a symbiotic relationship. Microservices are difficult to manage without robust CI practices, because the distributed nature of the system makes manual integration impractical. Conversely, microservices make CI easier in some respects, because each service is small and can be built and tested quickly.

The challenge arises at the integration points between services. Traditional CI focuses on integrating code changes within a single codebase. Microservices require a broader notion of integration that includes verifying compatibility between independently developed services. This is where Contract Testing fills the gap -- it provides the fast feedback that CI demands, without requiring all services to be running together.

Farley's emphasis on sharing a Deployment Pipeline in the early stages can be understood as a way to maintain the benefits of traditional CI (fast feedback on integration problems) while the team is still learning the optimal service boundaries. Once the boundaries are stable and Contract Testing is in place, the team can safely transition to separate pipelines with confidence that integration problems will still be caught early.

### DRY in the Context of Microservices

One of Farley's recommended video resources is titled "DRY Software Patterns and Microservices," which touches on a subtle and often misunderstood point. The DRY principle ("Don't Repeat Yourself") is one of the most well-known in software engineering, but its application in a microservices context requires careful thought.

In a monolithic system, DRY typically means sharing code through libraries or base classes. In a microservices system, sharing code across service boundaries can create tight coupling. If two services share a library that defines data structures or business logic, then a change to that library may require coordinated changes to both services -- undermining independent deployability.

The microservices-appropriate interpretation of DRY is to apply it within service boundaries but not across them. Within a service, you should absolutely eliminate duplication through well-factored code, shared libraries, and common abstractions. But between services, some duplication is acceptable -- even desirable -- if it preserves independence. Having two services each define their own model of a "book" is not a violation of DRY; it is a recognition that they have different needs and should be free to evolve independently.

This is directly related to Farley's emphasis on Bounded Contexts. Within a Bounded Context, concepts have a single, consistent meaning, and DRY applies fully. Across Bounded Contexts, the same concept may have different meanings, and the models should be separate. The translation layer at the boundary handles the mapping between these different models, and this translation is not "duplication" in the DRY sense -- it is a necessary part of maintaining loose coupling.

---

## Appendix: A Decision Framework for Microservices Adoption

Drawing on Farley's guide, the following decision framework can help teams determine whether and how to adopt microservices:

**When to consider microservices:**
- Your organization has reached a size where multiple teams need to work on the same system simultaneously, and coordination overhead is becoming a bottleneck.
- Different parts of your system have different scaling requirements, technology needs, or release cadences.
- You have robust CI/CD practices already in place, including automated testing, deployment pipelines, and monitoring.
- Your team has experience with distributed systems or is willing to invest in learning.

**When to avoid microservices:**
- Your team is small (typically fewer than 10-15 developers) and can work effectively in a single codebase.
- Your domain is not well-understood and you are still in the early stages of exploration.
- You do not have mature CI/CD practices. Microservices amplify the need for automation.
- You are building a prototype or MVP where speed of delivery matters more than scalability.

**How to start, if you decide to proceed:**
1. Use Event Storming or similar collaborative modeling to explore the domain.
2. Start with a single repository and a single deployment pipeline.
3. Identify candidate Bounded Contexts and implement them as separate modules.
4. Design the messaging between modules using the Ports and Adapters pattern.
5. Test and iterate, refining boundaries based on what you learn.
6. Introduce Contract Testing as the design stabilizes.
7. Split into separate repositories only when boundaries are proven and stable.
8. Maintain Contract Testing as a safety net for ongoing independent deployment.

This framework is consistent with Farley's guidance throughout the guide and provides a structured approach to making the adoption decision.

### Domain-Driven Design

The influence of Domain-Driven Design (DDD) on Farley's approach is pervasive. The concepts of Bounded Contexts, the translation of concepts between contexts, and the alignment of services with the problem domain are all drawn directly from DDD. Farley recommends Eric Evans' book "Domain-Driven Design" as essential reading, along with Sam Newman's "Building Microservices."

The connection between DDD and microservices is not coincidental. DDD provides the conceptual tools for identifying good service boundaries -- boundaries that are aligned with the business, naturally decoupled, and stable over time. Without these tools, microservices decomposition tends to be arbitrary and fragile, leading to the distributed monolith anti-pattern.

### Event Storming

Farley's recommendation of Event Storming as a design tool connects his approach to the broader community of DDD practitioners. Event Storming provides a collaborative, visual way to explore the problem domain and identify candidate service boundaries. It is particularly valuable in the early stages of a microservices project, when the team is still forming its understanding of the domain and the optimal decomposition is unclear.

It is worth noting that Event Storming is not the only collaborative modeling technique available. Other approaches, such as Domain Storytelling (where participants tell stories about how the business works using simple pictograms) and Example Mapping (where scenarios are broken down into rules and examples), can serve a similar purpose. Farley specifically recommends Event Storming, likely because of its proven track record in the DDD community and its natural affinity for identifying the event flows that connect different parts of a business process. The key point is not the specific technique, but the principle: collaborative, domain-focused exploration should precede technical decomposition.

### The Modular Monolith as an Alternative

Although Farley does not discuss it in this guide, his approach to starting with a single repository and well-defined module boundaries is closely related to the concept of a modular monolith. A modular monolith is a single deployable unit that is internally organized into well-defined modules with clear interfaces between them. This provides many of the organizational benefits of microservices (clear ownership boundaries, domain-aligned decomposition) without the operational complexity of a distributed system.

Many practitioners now advocate for starting with a modular monolith and extracting services only when there is a clear need for independent deployment or independent scaling. Farley's approach is consistent with this philosophy, even though he frames it in terms of a path to microservices rather than as an end state. The key insight is the same: get the boundaries right first, and the deployment architecture (monolith or microservices) is a secondary concern that can be adjusted later.

---

## Chapter 9: Recommended Reading and References

Farley provides a curated set of references for further study:

### Video Resources (Continuous Delivery YouTube Channel)
- "The Problem with Microservices" -- Farley's analysis of common pitfalls and anti-patterns in microservices adoption.
- "Getting Started with Microservices" -- A companion video to this guide, providing additional context and examples.
- "DRY Software Patterns and Microservices" -- An exploration of how the DRY (Don't Repeat Yourself) principle applies (and sometimes misapplies) in a microservices context.

### Books
- **"Building Microservices: Designing Fine-Grained Systems" by Sam Newman** -- The definitive guide to microservices architecture, covering design, deployment, testing, and evolution in depth.
- **"Domain-Driven Design" by Eric Evans** -- The foundational text on DDD, introducing Bounded Contexts, Ubiquitous Language, and the strategic patterns that underpin effective microservices design.

### Online Resources
- **Event Storming** (eventstorming.com) -- Alberto Brandolini's collaborative workshop technique for exploring business domains and identifying service boundaries.
- **What is Contract Testing?** (Pactflow blog) -- An introduction to Contract Testing concepts and the Pact framework.

---

## Key Takeaways

1. **Microservices are small, focused services aligned with business domains.** The "rewrite in one to two weeks" heuristic provides a concrete measure of appropriate size. Smallness is a consequence of focus, not an arbitrary target.

2. **Independent deployability is the defining property.** If your services cannot be deployed independently, you have a distributed monolith, not a microservices architecture. Every design decision should be evaluated against this criterion.

3. **Align services with Bounded Contexts.** Bounded Contexts from Domain-Driven Design provide the most principled basis for identifying service boundaries. Each context has its own model, and the boundaries between contexts are naturally decoupled.

4. **Start with a single repository and iterate.** Do not rush to create separate repositories for each service. Begin with a single repo, experiment with boundaries, and split only when the design stabilizes. This reduces the cost of learning and evolution.

5. **Treat messages as a separate concern.** Use the Ports and Adapters pattern to separate message translation from business logic. This allows internal logic and external contracts to evolve independently, supports versioning, and enables independent deployment.

6. **Model messages at the domain level.** Messages should be expressed in business terms that non-technical stakeholders can understand. Avoid technically-focused messages that expose internal implementation details.

7. **Translate concepts at boundaries.** Do not try to create a universal data model that works everywhere. Instead, translate concepts as they cross Bounded Context boundaries, allowing each context to maintain its own model.

8. **Use Contract Testing to verify compatibility.** Contract Testing allows you to detect breaking changes without requiring full integration environments. It is the key enabler of confident independent deployment.

9. **Invest in boundary design.** The interfaces between services are the most important part of the system design. Treat them with special care, invest in their design, and be willing to refactor them when they are not working.

10. **Microservices are primarily about scaling development.** The main value of microservices is organizational scalability -- the ability to have many teams working independently on a shared system. This is the problem they solve, and their complexity is only justified when this scaling benefit is needed.

11. **Adoption is an iterative, learning-driven process.** You cannot design a microservices architecture upfront. You must discover the optimal boundaries through experimentation, feedback, and refinement. Embrace uncertainty and design your process to learn quickly.

12. **Decomposition is domain-driven, not technical.** Do not decompose your system along technical layers. Decompose it along domain boundaries, where each service corresponds to a coherent area of the business with its own model and its own language.

---

## Appendix: Common Anti-Patterns and Pitfalls

### Anti-Pattern 1: Premature Decomposition

The most common mistake Farley identifies is decomposing into separate services and separate repositories too early. This locks in design decisions before they have been validated and makes it expensive to change course. The antidote is to start with a single repository and iterate on the design before splitting.

### Anti-Pattern 2: The Shared Database

Although not explicitly called out in this short guide, the shared database is one of the most common sources of coupling in microservices systems. When multiple services read from and write to the same database, any change to the schema affects all of them, and coordinated deployments become necessary. The principle of independent deployability demands that each service own its own data store.

### Anti-Pattern 3: Technically-Focused Service Boundaries

Decomposing a system along technical lines -- for example, having a "data access service," a "business logic service," and a "presentation service" -- creates services that are tightly coupled by nature. A change to a business rule may require changes in all three services. Farley's emphasis on Bounded Contexts and domain-driven decomposition is a direct response to this anti-pattern.

### Anti-Pattern 4: Chatty Synchronous Communication

When services communicate through frequent, synchronous request-response calls, they become temporally coupled. If service A makes a synchronous call to service B, then B must be available whenever A needs it. This undermines resilience and independent deployability. While Farley does not explicitly advocate for asynchronous messaging in this guide, his emphasis on treating messages as domain-level conversations and translating at boundaries is consistent with an event-driven approach that minimizes temporal coupling.

### Anti-Pattern 5: Ignoring the Boundary as a Design Concern

Many teams focus exclusively on the internal design of each service and neglect the design of the interfaces between them. This leads to interfaces that are tightly coupled to internal implementation details, making it difficult to change one service without breaking others. Farley's consistent emphasis on treating boundaries with special care is a direct response to this tendency.

---

## Appendix: The Guide in Context -- How It Relates to the Broader Microservices Literature

Farley's guide is a concise, opinionated introduction to microservices that complements the broader literature. Sam Newman's "Building Microservices," which Farley recommends, provides a much more comprehensive treatment of the topic, covering topics like service discovery, API gateways, observability, security, and deployment strategies in far greater detail. Eric Evans' "Domain-Driven Design" provides the theoretical foundation for the Bounded Context concept that Farley relies on so heavily.

What Farley's guide provides that these longer works do not is a focused, step-by-step approach to getting started. It answers the question "What should I do on Monday morning if I want to adopt microservices?" with a clear, actionable answer: start with a single repository, explore the domain, experiment with boundaries, and split only when you are confident in the design. This pragmatism is the guide's greatest strength.

The guide also reflects Farley's particular perspective as a Continuous Delivery practitioner. His emphasis on deployment pipelines, fast feedback, and Contract Testing is not universally shared in the microservices community, where the focus is often on containerization, orchestration, and infrastructure. Farley's contribution is to remind us that the hardest problems in microservices are not infrastructure problems -- they are design problems. Getting the boundaries right, managing the contracts between services, and maintaining independent deployability are the challenges that determine whether a microservices architecture will succeed or fail.
