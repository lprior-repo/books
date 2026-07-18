# Building an Event-Driven Data Mesh - Adam Bellemare

## Comprehensive Summary

---

## Chapter 1: Event-Driven Data Communication

**The data problem:** Organizations struggle with data silos. Operational systems (OLTP) need real-time data, while analytical systems (data warehouses, data lakes) need historical data. Traditional approaches create copies, inconsistencies, and organizational friction.

**Schema-on-read vs schema-on-write:**
- **Schema-on-write** (data warehouses): Data must conform to a schema at write time. Good for consistency but rigid.
- **Schema-on-read** (data lakes): Schema applied at query time. Flexible but can lead to data quality issues ("data swamp").

**The data monolith problem:** A single central data team becomes a bottleneck. They can't understand every domain's data needs. Changes require coordination across many teams.

**Can we unify operational and analytical workflows?** Yes, with an event-driven data mesh. Event streams serve as the single source of truth for both operational and analytical use cases.

**Common objections addressed:**
- "Producers can't model data for everyone" → They shouldn't. Producers model for their domain; consumers project as needed.
- "Multiple copies of data is bad" → Copies are unavoidable; what matters is controlled, governed replication.
- "Eventual consistency is too hard" → It's manageable with proper patterns and tools.

---

## Chapter 2: Data Mesh Principles

**The four pillars of data mesh:**

### Principle 1: Domain Ownership
- Data should be owned by the domain that produces it, not a central data team
- Uses Domain-Driven Design concepts: bounded contexts, ubiquitous language
- Each domain team is responsible for the quality and availability of its data products
- Select data to expose based on what other domains actually need

### Principle 2: Data as a Product
- Data products are treated like software products with SLAs, versioning, documentation
- **Properties of data products:**
  - Immutable and time-stamped (event streams are append-only logs)
  - Multimodal (can be consumed as events, materialized views, or aggregated)
  - Accessible via push (subscribe to events) or pull (query a materialized view)

**Three data product alignment types:**
1. **Source-aligned**: Raw events from the domain, closest to the source of truth
2. **Aggregate-aligned**: Pre-computed aggregations (e.g., daily sales totals)
3. **Consumer-aligned**: Transformed for a specific consumer's needs

### Principle 3: Federated Governance
- A central governance team sets standards, not mandates
- Standards cover: schemas, APIs, security policies, data retention, privacy
- Domains implement their own data products within these standards
- Cross-domain polysemes (same term, different meaning) are identified and resolved

### Principle 4: Self-Service Platform
- Data product discovery: catalog of available data products and their schemas
- Data product access controls: who can read what
- Management controls: provisioning, monitoring, alerting
- Compute and storage resources: self-service provisioning
- Often provided as SaaS internally

---

## Chapter 3: Event Streams for Data Mesh

**Events, messages, and records:**
- **Event**: Something that happened (fact) — e.g., "OrderPlaced", "PaymentReceived"
- **Message**: The transport mechanism carrying an event
- **Record**: The serialized form in the event broker

**What is an event stream:**
- An append-only, immutable, ordered log of events
- Identified by a topic name
- Keyed and partitioned for ordering and parallelism
- Retained for a configurable period

**Event stream vs other patterns:**
- **Not ephemeral messaging**: Events are retained, not deleted after consumption
- **Not a queue**: Multiple consumers can read independently; events persist

**State events and event-carried state transfer:**
- **State events**: Carry the full current state of an entity (e.g., full customer record)
- **Delta events**: Carry only what changed (e.g., "address changed from X to Y")
- **Event-carried state transfer**: Consumers maintain local materialized views by processing events

**Materializing events:** Converting an event stream into a queryable state (table, key-value store). Consumers build their own views from shared events.

**The Kappa Architecture:**
- All data flows through event streams as the single source of truth
- Both real-time and batch processing use the same stream processing framework
- Replaces the Lambda Architecture (which uses separate batch and speed layers)
- Benefits: Single processing framework, simpler architecture, easier to maintain

**Selecting an event broker:**
- Apache Kafka: Industry standard, high throughput, strong durability
- Apache Pulsar: Built-in multi-tenancy, geo-replication
- Amazon Kinesis: Managed Kafka-like service
- Consider: throughput, latency, retention, exactly-once semantics, ecosystem

---

## Chapter 4: Federated Governance

**Forming a governance team:**
- Representatives from each domain
- Data architects, security specialists, platform engineers
- Meets regularly to set and review standards

**Implementing standards:**
- Schema format (Avro, Protobuf, JSON Schema)
- API compatibility (REST, gRPC, event streams)
- Programming language and framework support
- Metadata requirements (documentation, lineage, quality metrics)

**Cross-domain data product compatibility:**
- **Common entities**: Define shared concepts (Customer, Order, Product) across domains
- **Event stream keying**: Use consistent entity IDs across streams
- **Partitioning strategies**: Partition by entity key for co-location and ordering
- **Time handling**: Use UTC, include timestamps, handle time zones explicitly

**Data security and access policies:**
- Disable data product access by default
- Consider end-to-end encryption
- Field-level encryption for sensitive data (PII, financial data)
- Access logging and auditing

---

## Chapter 5: Event Design Patterns

**Event types:**

1. **Fact events**: Record something that happened (immutable truth)
   - "OrderPlaced", "PaymentProcessed"
   - Cannot be changed after creation

2. **Delta events**: Record a change in state
   - "AddressChanged", "QuantityUpdated"
   - Must include both old and new values

3. **Command events**: Represent a request for action
   - "PlaceOrder", "CancelSubscription"
   - May be accepted or rejected

**Event design considerations:**
- **Payload size**: Include enough context but don't over-stuff events
- **Versioning**: Schema evolution strategy (forward/backward compatible)
- **Idempotency**: Consumers should handle duplicate events safely
- **Ordering**: Events for the same entity key are ordered within a partition

**Schema evolution:**
- **Backward compatible**: New schema can read old data (safe to add fields with defaults)
- **Forward compatible**: Old schema can read new data (safe to add optional fields)
- **Breaking changes**: Require coordination with all consumers
- Use schema registries to manage versions

---

## Chapter 6: Building Data Products

**From event streams to data products:**

1. **Source-aligned data products**: Raw events from a domain's event stream
2. **Aggregate-aligned**: Processed events producing materialized aggregates
3. **Consumer-aligned**: Filtered, transformed events for specific consumers

**Implementing data products:**
- Use stream processing frameworks (Kafka Streams, Flink, ksqlDB)
- Materialize to queryable stores (key-value, document, relational)
- Expose via APIs for pull-based consumers
- Publish to event streams for push-based consumers

**Data product lifecycle:**
1. **Proposal**: Define the data product, schema, consumers
2. **Development**: Build the producer and schema
3. **Testing**: Validate data quality, schema compatibility
4. **Deployment**: Register in the catalog, grant access
5. **Operation**: Monitor quality, handle schema evolution
6. **Deprecation**: Communicate retirement plan, migrate consumers

---

## Chapter 7: Handling Privacy and Compliance

**Privacy in event streams:**
- Events are immutable and often retained for long periods
- GDPR "right to be forgotten" is challenging with immutable logs
- Strategies: encryption with deletable keys, redaction topics, retention policies

**Data handling policies:**
- Classify data sensitivity levels
- Apply appropriate controls per classification
- Audit data access and usage
- Regular compliance reviews

**Regulatory considerations:**
- GDPR, CCPA, HIPAA requirements
- Data residency (where data is stored)
- Cross-border data transfer
- Audit trails and lineage tracking

---

## Chapter 8: Scaling and Operating

**Scaling event-driven data mesh:**
- Partition event streams for parallel processing
- Scale consumers horizontally (consumer groups)
- Monitor consumer lag (how far behind each consumer is)
- Handle backpressure when consumers can't keep up

**Operational concerns:**
- **Consumer lag monitoring**: Alert when consumers fall behind
- **Schema compatibility checks**: Validate schema changes before deployment
- **Data quality monitoring**: Validate events against expected schemas and values
- **Event broker operations**: Broker health, replication, partition rebalancing

**Handling failures:**
- Producer failures: At-least-once vs exactly-once semantics
- Consumer failures: Checkpointing, replay from last committed offset
- Broker failures: Replication factor, min.insync.replicas
- Network partitions: Split-brain scenarios, quorum-based decisions

---

## Key Takeaways

1. **Data mesh treats data as products owned by domains**, not a central team. This scales with organizational growth.

2. **Event streams are the foundation**: Immutable, ordered, replayable logs serve as the single source of truth for both operational and analytical needs.

3. **The Kappa Architecture unifies processing**: Use one stream processing framework for both real-time and batch, replacing the complex Lambda Architecture.

4. **Federated governance sets standards, not mandates**: A central team ensures compatibility across domains while letting domain teams own their data.

5. **Self-service platforms are essential**: Data product discovery, access control, and provisioning must be easy for teams to use independently.

6. **Schema evolution requires planning**: Design schemas for backward/forward compatibility from the start. Use schema registries.

7. **Privacy and compliance are first-class concerns**: Immutable event streams create unique challenges for regulations like GDPR. Plan for encryption and redaction.

8. **Event design matters**: Choose fact, delta, or command events appropriately. Include enough context but keep payloads manageable.

9. **Three alignment types guide data product design**: Source-aligned (raw), aggregate-aligned (pre-computed), consumer-aligned (transformed).

10. **Operational excellence is non-negotiable**: Monitor consumer lag, data quality, schema compatibility, and broker health continuously.
