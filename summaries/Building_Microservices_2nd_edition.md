# Building Microservices (2nd Edition) - Sam Newman

## Comprehensive Summary

---

## Part I: Foundation

### Chapter 1: What Are Microservices?

**Microservices defined:** Small, autonomous services that work together. Each runs its own process, communicates via lightweight mechanisms (HTTP, events), and is independently deployable.

**Key concepts:**
- **Independent deployability**: The single most important characteristic. You can change and deploy one service without touching others.
- **Modeled around a business domain**: Services align with business capabilities, not technical layers.
- **Owning their own state**: Each service manages its own data store. No shared databases.
- **Size**: "Small enough that a single team can own it." No strict size limits.
- **Flexibility**: Mix technologies, scale independently, evolve at different paces.
- **Alignment with organization**: Conway's Law—your architecture mirrors your org structure.

**The monolith spectrum:**
1. **Single-process monolith**: All code in one deployable unit. Simplest to start, hardest to scale.
2. **Modular monolith**: Single process with well-defined module boundaries. Can evolve toward microservices.
3. **Distributed monolith**: Multiple services that are tightly coupled. Worst of both worlds—complexity of distributed systems without the benefits.

**Advantages of microservices:**
- Technology heterogeneity: Use the right tool for each job
- Robustness: Failure in one service doesn't bring down everything
- Scaling: Scale individual services based on their own load
- Ease of deployment: Small, focused deployments reduce risk
- Organizational alignment: Teams own services end-to-end
- Composability: Services can be combined in new ways

**Pain points:**
- Developer experience complexity
- Technology overload (too many tools)
- Cost of distributed systems
- Reporting across service boundaries
- Monitoring and troubleshooting difficulty
- Security complexity
- Testing challenges
- Latency from network calls
- Data consistency (eventual consistency)

**When to use microservices:** When the benefits of independent deployability and organizational alignment outweigh the complexity cost. Not for small teams or simple domains.

### Chapter 2: How to Model Microservices

**What makes a good microservice boundary:**

**Information hiding** (David Parnas): Hide implementation details behind well-defined interfaces. Changes to internals don't affect other services.

**Cohesion**: Related behavior should live together. High cohesion = all related functionality in one service. Low cohesion = related functionality scattered across services.

**Coupling**: Services should have minimal knowledge of each other. Types of coupling (from weakest to worst):

1. **Domain coupling**: Service A needs something from Service B's domain. Acceptable and unavoidable, but minimize it.
2. **Pass-through coupling**: Service A passes data through Service B to reach Service C. Service B doesn't need the data. Bad—restructure.
3. **Common coupling**: Services share a database or configuration. Changes to the shared thing affect all consumers. Dangerous.
4. **Content coupling**: Service A reaches into Service B's internals (database, private API). Catastrophic—eliminate immediately.

**Domain-Driven Design concepts:**
- **Ubiquitous language**: Shared vocabulary within a bounded context
- **Aggregate**: A cluster of domain objects treated as a single unit (e.g., Order + OrderLines)
- **Bounded context**: A boundary within which a particular domain model applies consistently

**Mapping bounded contexts to microservices:**
- Ideal: One bounded context = one microservice
- Aggregates within a bounded context can be split into separate services only if they're truly independent
- Event storming: Collaborative workshop to identify domain events and bounded contexts

**Alternative decomposition axes:**
- **Volatility**: Split by rate of change (volatile features separated from stable ones)
- **Data**: Split by data ownership and access patterns
- **Technology**: Split by technology requirements (real-time vs batch, different data stores)
- **Organizational**: Split by team structure (Conway's Law)

### Chapter 3: Splitting the Monolith

**Have a goal:** Know why you're splitting—performance, team autonomy, scaling? The goal drives what to split first.

**Incremental migration:** Never attempt a big-bang rewrite. Use the strangler fig pattern:
1. Identify a piece to extract
2. Route traffic to the new service incrementally
3. Verify correctness
4. Remove the old implementation

**What to split first:**
- Start with loosely coupled, high-cohesion boundaries
- Easiest splits first to build confidence
- High-value splits: areas with frequent changes or scaling needs

**Decomposition patterns:**
- **Strangler fig**: Incrementally replace monolith functionality
- **Parallel run**: Run old and new simultaneously, compare results
- **Feature toggle**: Deploy new implementation behind a flag, switch traffic gradually

**Data decomposition concerns:**
- **Foreign key relationships**: Cross-service joins become impossible. Use API calls or eventual consistency.
- **Transactions**: Distributed transactions (two-phase commit) are expensive and brittle. Use sagas instead.
- **Reporting**: Can't query across service databases. Use data replication or a reporting database.

### Chapter 4: Microservice Communication Styles

**From in-process to inter-process:**
- Performance: Network calls are orders of magnitude slower than in-process calls
- Interface changes: Harder to evolve across service boundaries
- Error handling: Network failures, timeouts, retries add complexity

**Communication patterns:**

1. **Synchronous blocking** (REST, gRPC):
   - Request-response: Client waits for response
   - Advantages: Simple mental model, easy to debug
   - Disadvantages: Temporal coupling (both must be available), cascading failures
   - Use when: You need an immediate response

2. **Asynchronous nonblocking** (message queues, event streams):
   - Fire and forget or request-async response
   - Advantages: Decoupled in time, resilience, natural buffering
   - Disadvantages: Complexity, eventual consistency, harder to debug
   - Use when: Operations can tolerate delay, need resilience

3. **Communication through shared data**:
   - Services read/write to a shared store (database, filesystem)
   - Advantages: Simple, handles large data transfers
   - Disadvantages: Tight data coupling, schema coordination
   - Use when: Bulk data transfer, reporting integration

---

## Part II: Implementation

### Chapter 5: Implementing Microservice Communication

**Technology choices:**
- **REST**: HTTP-based, widely understood, good tooling. Best for synchronous request-response.
- **gRPC**: Binary protocol, strongly typed, efficient. Best for internal service-to-service.
- **GraphQL**: Client-driven queries. Best for external-facing APIs with varied consumers.
- **Message brokers**: RabbitMQ, ActiveMQ for point-to-point async communication.
- **Event brokers**: Kafka, Pulsar for event streaming with replay capability.

**Service discovery:**
- **Client-side discovery**: Client queries a service registry (Eureka, Consul)
- **Server-side discovery**: Load balancer routes to available instances
- **Service mesh**: Sidecar proxy handles discovery and routing (Istio, Linkerd)

**Reliability patterns:**
- **Circuit breaker**: Stop calling a failing service to prevent cascade (Hystrix, Resilience4j)
- **Bulkhead**: Isolate resources per downstream service to prevent one failure from exhausting all resources
- **Timeout**: Always set timeouts; never make unbounded network calls
- **Retry with backoff**: Retry transient failures with exponential backoff and jitter

**Idempotency**: Design operations to be safely retried. Use idempotency keys for write operations.

### Chapter 6: Data Management

**Each service owns its data:**
- Private database per service (or at minimum, private schema)
- No direct database access across service boundaries
- Data needed by other services is exposed via APIs or events

**Saga pattern for distributed transactions:**
- A sequence of local transactions, each with a compensating action for rollback
- **Choreography-based sagas**: Each service emits events; others react
- **Orchestration-based sagas**: A central orchestrator coordinates the steps

**Event sourcing:**
- Store all state changes as an immutable sequence of events
- Current state is derived by replaying events
- Natural fit for microservices: events serve as both state and integration mechanism
- Requires event store and snapshot optimization

**CQRS (Command Query Responsibility Segregation):**
- Separate write model from read model
- Commands mutate state, queries read from materialized views
- Optimizes read and write independently
- Often paired with event sourcing

### Chapter 7: Testing Microservices

**Test types (pyramid adapted for microservices):**

1. **Unit tests**: Test individual functions/methods. Fast, numerous.
2. **Integration tests**: Test service interactions with external dependencies (databases, APIs). Use test containers.
3. **Component tests**: Test a single microservice in isolation with mocked dependencies.
4. **Contract tests**: Verify API contracts between services. Consumer-driven contracts (Pact).
5. **End-to-end tests**: Test complete user journeys across multiple services. Expensive, few.
6. **Exploratory testing**: Manual testing for edge cases and usability.

**Consumer-driven contract testing:**
- Consumers define their expectations (contracts)
- Providers verify they satisfy all consumer contracts
- Decouples service testing: no need for full integration environment
- Tools: Pact, Spring Cloud Contract

**Testing in production:**
- Canary releases: Route small % of traffic to new version
- Blue-green deployments: Switch between two environments
- Feature toggles: Test new features with limited exposure
- Observability: Use monitoring as a continuous test

### Chapter 8: Deployment and Infrastructure

**Deployment options:**
- **Physical machines**: Maximum control, high overhead
- **Virtual machines**: Isolation, moderate overhead
- **Containers (Docker)**: Lightweight isolation, fast startup, portable
- **Serverless/Functions**: Zero infrastructure management, event-triggered

**Kubernetes as the standard orchestrator:**
- Container scheduling and scaling
- Service discovery and load balancing
- Self-healing (restart failed containers)
- Rolling updates and rollbacks
- ConfigMaps and Secrets for configuration

**Infrastructure as code:**
- Terraform, Pulumi, CloudFormation for infrastructure provisioning
- Ansible, Chef, Puppet for configuration management
- All infrastructure changes version-controlled and reviewable

**Zero-downtime deployment strategies:**
- Blue-green: Two identical environments, instant switch
- Canary: Gradual traffic shift with monitoring
- Rolling update: Incremental replacement of instances

### Chapter 9: Security

**Authentication and authorization:**
- **Service-to-service**: mTLS, API keys, JWT tokens
- **User-to-service**: OAuth2, OpenID Connect
- **Service mesh**: Automatic mTLS between services (Istio, Linkerd)

**Defense in depth:**
- Network segmentation
- API gateway for rate limiting and authentication
- Input validation at every boundary
- Secrets management (Vault, AWS Secrets Manager)

### Chapter 10: Monitoring and Observability

**The three pillars of observability:**
- **Logs**: Discrete event records (ELK, Loki)
- **Metrics**: Numeric measurements over time (Prometheus, Grafana)
- **Traces**: Request flow across services (Jaeger, Zipkin)

**Distributed tracing essential for microservices:**
- Assign correlation IDs to every request
- Propagate IDs across service boundaries
- Tools: OpenTelemetry standardizes trace collection

**Monitoring patterns:**
- Health check endpoints
- Circuit breaker state monitoring
- Consumer lag monitoring for event-driven services
- SLA/SLO monitoring (latency percentiles, error rates)
- Alerting: Alert on symptoms (user impact), not causes

### Chapter 11: User Interfaces

**UI composition patterns:**
- **Monolithic frontend**: Single UI calls multiple services
- **Micro frontends**: Each team owns a UI fragment, composed at runtime
- **BFF (Backend for Frontend)**: Dedicated backend service per UI type (web, mobile)

### Chapter 12: Organizational Considerations

**Conway's Law in practice:**
- Organizations that designed software using loosely coupled structures produced more modular software
- Microsoft Vista study: Organizational metrics (number of engineers per component) were the strongest predictor of quality
- **Reverse Conway Maneuver**: Design your organization structure to produce the architecture you want

**Team topologies:**
- Stream-aligned teams: Aligned to a business domain, own microservices end-to-end
- Platform teams: Provide internal platform capabilities (CI/CD, infrastructure)
- Enabling teams: Help other teams adopt new practices
- Complicated-subsystem teams: Own specialized complex components

**Team size**: 5-9 people per team (Amazon's "two-pizza team" rule)

---

## Key Takeaways

1. **Independent deployability is the defining characteristic**: If you can't deploy services independently, they're not microservices.

2. **Model services around business domains, not technical layers**: Bounded contexts from DDD provide natural boundaries.

3. **Coupling kills microservices**: Minimize domain coupling, eliminate pass-through, common, and content coupling.

4. **Each service owns its data**: No shared databases. Use APIs, events, or sagas for cross-service data needs.

5. **Split incrementally, never rewrite**: Strangler fig pattern. Extract one piece at a time, verify, repeat.

6. **Contract testing decouples service testing**: Consumer-driven contracts ensure compatibility without integration environments.

7. **Observability is not optional**: Distributed tracing, metrics, and logging are essential for understanding distributed systems.

8. **Conway's Law is real**: Your architecture mirrors your organization. Design both deliberately.

9. **Start with a monolith (or modular monolith)**: Don't start with microservices unless you have a clear reason. Extract when you have enough understanding of domain boundaries.

10. **The distributed monolith is the worst outcome**: Multiple services that are tightly coupled give you all the complexity with none of the benefits. Prefer a well-structured monolith.
