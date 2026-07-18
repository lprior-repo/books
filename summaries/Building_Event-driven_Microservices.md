# Building Event-Driven Microservices - Adam Bellemare

## Comprehensive Summary

---

## Chapter 1: Why Event-Driven Microservices?

**The core problem:** Organizations need real-time data across business units, but traditional architectures create data silos. Synchronous microservices compound the problem with tight temporal coupling.

**Domain-Driven Design foundations:**
- **Bounded contexts**: Each domain (orders, payments, shipping) has its own model and data
- **Ubiquitous language**: Shared vocabulary within a bounded context
- Microservices align naturally with bounded contexts

**Communication structures (Conway's Law):**
- Business communication: How teams talk to each other
- Implementation communication: How services interact technically
- Data communication: How data flows through the organization
- These structures must align for effective systems

**The event-driven advantage:**
- Events are the basis of communication between services
- Event streams provide the single source of truth
- Consumers perform their own modeling and querying
- Data communication improves across the organization
- Accessible data supports business communication changes

**Synchronous vs asynchronous microservices:**

| Aspect | Synchronous | Event-Driven (Async) |
|--------|-------------|---------------------|
| Coupling | Tight temporal coupling | Loose coupling |
| Failure impact | Cascading failures | Isolated failures |
| Scalability | Limited by slowest service | Independent scaling |
| Data access | Request-response | Event streams |
| Complexity | Simpler call chains | Eventual consistency |

---

## Chapter 2: Event-Driven Microservice Fundamentals

**Microservice topology:** How services connect to event streams as producers and consumers. Each service has a specific role in the data flow.

**Business topology:** How business concepts flow through the organization. Aligns technical topology with business needs.

**Event structure:**
- **Unkeyed events**: No entity association (e.g., system alerts)
- **Entity events**: Associated with a specific entity (customer, order)
- **Keyed events**: Entity events with explicit partition keys for ordering

**Materializing state from events:**
Consumers maintain local state by processing the event stream:
1. Start from the beginning (or a checkpoint)
2. Process each event in order
3. Build up a local materialized view
4. Query the local view for fast access

**Microservice Single Writer Principle:** Only one microservice should produce events to a given event stream. This ensures data ownership and prevents conflicts.

**Event broker vs message broker:**
- **Event broker**: Stores events durably, multiple independent consumers, replay capability (Kafka, Pulsar)
- **Message broker**: Ephemeral delivery, message deleted after consumption (RabbitMQ, ActiveMQ)
- Event brokers are preferred for event-driven microservices

**Managing microservices at scale:**
- Containerize all services (Docker)
- Orchestrate with Kubernetes or similar
- Pay the "microservice tax": logging, monitoring, health checks, configuration management, service discovery

---

## Chapter 3: Communication and Data Contracts

**Schema-driven contracts:**
- Use explicit schemas (Avro, Protobuf, JSON Schema) as contracts between producers and consumers
- Schema registries manage schema versions and evolution
- Code generators create type-safe classes from schemas

**Schema evolution:**
- **Backward compatible**: New schema reads old data (add fields with defaults)
- **Forward compatible**: Old schema reads new data (optional fields)
- **Full compatibility**: Both backward and forward
- **Breaking changes**: Field removals, type changes — require coordination

**Designing events — core principles:**
1. **Tell the truth, the whole truth, and nothing but the truth**: Include all relevant data, nothing fabricated
2. **One event definition per stream**: Don't mix event types in one stream
3. **Use the narrowest data types**: Be precise (use integers for counts, not strings)
4. **Keep events single-purpose**: One event = one business fact
5. **Minimize event size**: Include only necessary data; consumers can enrich
6. **Involve prospective consumers in design**: Get feedback before locking schemas
7. **Avoid events as semaphores/signals**: Events carry data, not just "something happened"

---

## Chapter 4: Integrating with Existing Systems

**Data liberation:** Extracting data from existing systems into event streams. Essential for migrating to event-driven architecture.

**Data liberation patterns:**

1. **Query-based liberation:**
   - Bulk loading: Full table dump initially
   - Incremental timestamp loading: Poll for new/updated rows by timestamp
   - Auto-incrementing ID loading: Track last seen ID
   - Simple but can miss updates, has latency

2. **Change Data Capture (CDC):**
   - Read database transaction logs (binlog, WAL)
   - Capture every insert, update, delete in real-time
   - Tools: Debezium, Maxwell, DynamoDB Streams
   - Low latency, no database impact, but complex setup

3. **Outbox table pattern:**
   - Application writes to business tables AND an outbox table in the same transaction
   - A separate process reads the outbox and publishes to event stream
   - Guarantees atomicity: business operation and event publication succeed or fail together

**Isolating internal data models:**
- Don't expose internal database schemas directly as events
- Transform internal models to public event schemas
- Internal models can change without breaking consumers

**Sinking event data to data stores:**
- Write events back to databases/data warehouses for analytics
- Enables both real-time (streaming) and batch (warehouse) processing

---

## Chapter 5: Event-Driven Processing Basics

**Stateless processing patterns:**

- **Transformations**: Map, filter, enrich events
- **Branching**: Route events to different streams based on content
- **Merging**: Combine events from multiple streams
- **Repartitioning**: Change the partition key (e.g., from order ID to customer ID)
- **Copartitioning**: Ensure two streams are partitioned by the same key for joins

**Partition assignment:**
- Consumer instances are assigned partitions from the event stream
- Each partition is consumed by exactly one instance in a consumer group
- Adding instances increases parallelism (up to the number of partitions)
- Partition assignment strategies: Range, Round-Robin, Sticky

**Failure recovery:**
- Stateless consumers recover by replaying from the last committed offset
- Checkpointing: Periodically save the current offset
- On failure, resume from the last checkpoint

---

## Chapter 6: Deterministic Stream Processing

**Timestamps in event processing:**
- **Event time**: When the event actually occurred (most important for correctness)
- **Processing time**: When the event was processed by the consumer
- **Ingestion time**: When the event entered the broker

**Watermarks:** Define how far behind event time the processing can be. Used to determine when a window is complete and results can be emitted.

**Stream time:** The maximum event time seen so far in the stream. Used for time-based operations.

**Handling out-of-order events:**
- Events may arrive out of order due to network delays, retries
- Use watermarks and allowed lateness to handle late-arriving events
- Late events can be sent to a side output for separate handling

**Request-response in stream processing:**
- Event-driven services occasionally need to call external synchronous APIs
- Do this carefully: it introduces temporal coupling and latency
- Consider caching results in a table for future lookups

---

## Chapter 7: Stateful Processing

**Stateful stream processing:** Maintaining state across multiple events to produce aggregated results.

**Common stateful patterns:**
- **Windowed aggregations**: Count, sum, average over time windows
- **Session windows**: Group events by activity sessions with timeout gaps
- **Joins**: Stream-stream joins, stream-table joins
- **Custom state machines**: Track entity lifecycle through events

**Window types:**
- **Tumbling windows**: Fixed-size, non-overlapping (e.g., every 5 minutes)
- **Hopping windows**: Fixed-size, overlapping (e.g., 5-minute window advancing every 1 minute)
- **Session windows**: Variable-size, based on activity gaps

**Handling state in distributed processing:**
- State must be partitioned the same way as the input stream
- Each partition's state is independent
- State stores: in-memory with persistent backup (RocksDB), or external (Redis)

**Exactly-once processing:**
- Ensures each event is processed exactly once, even with failures
- Implemented through transactional writes and idempotent operations
- Requires coordination between consumer offsets and output writes

---

## Chapter 8: Workflow Patterns

**Choreography:** Each service reacts to events independently. No central coordinator.
- Pros: Simple, loosely coupled, easy to add participants
- Cons: Hard to see the full workflow, difficult to handle errors, no single source of truth for workflow state

**Orchestration:** A central orchestrator service manages the workflow.
- Pros: Clear workflow visibility, centralized error handling, easy to modify workflow
- Cons: More coupling, orchestrator becomes a bottleneck, single point of failure

**The orchestrator pattern in detail:**
- Maintains materialized state of the workflow
- Dispatches events to downstream services
- Collects responses and decides next steps
- Supports long-running processes with compensation logic

**Choosing between choreography and orchestration:**
- Simple workflows (2-3 steps): Choreography
- Complex workflows (many steps, error handling needed): Orchestrationration
- Many systems use both: orchestration for complex flows, choreography for simple notifications

---

## Chapter 9-10: Producer and Consumer Architecture

**Producer considerations:**
- Ensure events are published atomically with business state changes (outbox pattern)
- Handle backpressure from the broker
- Choose appropriate acknowledgment levels (acks=all for durability, acks=1 for performance)
- Implement retry and error handling

**Consumer considerations:**
- Consumer groups for horizontal scaling
- Offset management: auto-commit vs manual commit
- Idempotent processing: handle duplicate events gracefully
- Backpressure: don't consume faster than you can process

**Dead letter queues:** Events that fail processing are sent to a DLQ for investigation. Essential for production systems.

---

## Chapter 11-12: Microservice Patterns and Topologies

**Common microservice patterns:**

1. **Event sourcing**: Store all state changes as events. Reconstruct current state by replaying events.
2. **CQRS (Command Query Responsibility Segregation)**: Separate write model from read model. Events update both.
3. **Saga pattern**: Manage distributed transactions through a sequence of local transactions with compensating actions.
4. **Claim-check pattern**: Store large payloads externally, include only a reference in the event.

**Topology management:**
- Track data dependencies between services
- Visualize producer-consumer relationships
- Use ACLs and permissions to enforce data access
- Self-reporting service metadata for topology discovery

---

## Key Takeaways

1. **Events are the single source of truth**: Immutable, ordered event streams replace shared databases as the integration point between services.

2. **The Single Writer Principle**: Only one service produces to a given stream, ensuring ownership and preventing conflicts.

3. **Schema-driven contracts are essential**: Explicit schemas with evolution rules prevent breaking changes and enable safe growth.

4. **Materialized views replace synchronous queries**: Consumers build their own local state from events, eliminating temporal coupling.

5. **Choose liberation patterns wisely**: CDC for real-time, query-based for simplicity, outbox for atomicity guarantees.

6. **Stateful processing enables powerful patterns**: Windowed aggregations, joins, and session tracking unlock business insights.

7. **Choreography for simplicity, orchestration for complexity**: Match the coordination pattern to the workflow's needs.

8. **Deterministic processing requires careful timestamp handling**: Event time, watermarks, and windowing are fundamental to correct results.

9. **Idempotency is non-negotiable**: Events can be delivered more than once. Consumers must handle duplicates safely.

10. **Pay the microservice tax**: Monitoring, logging, health checks, and dependency tracking are essential for production event-driven systems.
