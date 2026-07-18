# Building Event-Driven Microservices
**Author:** Adam Bellemare
**Topic tags:** `#architecture` `#api`
**Language focus:** Language-agnostic (Kafka clients in Java/Python/SQL shown)
**Sources:** `markdown_output/Building Event-driven Microservices/Building Event-driven Microservices.md` · `summaries/Building_Event-driven_Microservices.md`

## TL;DR
Event-driven microservices (EDM) treat the immutable, replayable event stream
as the *single source of truth* between services; bounded contexts own streams
under the *Single Writer Principle*; consumers materialize state and serve it via
REST or FaaS. The book is a pragmatic playbook: data liberation (CDC/outbox),
schema contracts with full-transitive evolution, deterministic stream processing
with watermarks/stream time, state stores + changelogs, effectively-once
processing via idempotent producers + transactions, choreography vs orchestration
tradeoffs, schema-migration deployment patterns, and Kafka-only microservice tax.

---

## Best Practices by Topic

### Why Event-Driven Microservices (Over Synchronous)

**Principle:** Use events as the data communication layer between bounded
contexts; never couple on each other's internal models or APIs.

**Do:**
- Align bounded contexts on **business requirements**, never on technical
  layers (frontend/backend/datalayer splits). "Technical alignment is seldomly
  used in event-driven microservice (EDM) architectures."
  *Ref: Building Event-driven Microservices.md — "Aligning Bounded Contexts with Business Requirements" (`page-22-0`).*
- Bounded contexts should be highly cohesive / loosely coupled.
  *Ref: Building Event-driven Microservices.md — "Bounded context" (`page-21-0`).*
- Publish all shareable data to the event streams; let consumers model it.
  *Ref: Building Event-driven Microservices.md — "Events Are the Basis of Communication" (`page-31-0`).*
- Treat the event stream as the single source of truth.
  *Ref: Building Event-driven Microservices.md — "Event Streams Provide the Single Source of Truth" (`page-31-0`).*

**Don't:**
- Don't build services coupled by *point-to-point request-response APIs* that
  fan out across the org — "the number of connections between services can
  become staggeringly high."
  *Ref: Building Event-driven Microservices.md — "Drawbacks of Synchronous Microservices" (`page-35-0`).*
- Don't create a *distributed monolith* by treating synchronous internal calls
  as the decomposition strategy.
  *Ref: Building Event-driven Microservices.md — "Distributed monoliths" (`page-36-0`).*

---

### Microservice Single Writer Principle

**Principle:** Each event stream has exactly one producing microservice. The
producer owns the schema, the data, and the SLAs of that stream.

**Do:**
- Use the access-control permissions to enforce the Single Writer Principle.
  *Ref: Building Event-driven Microservices.md — "Permissions and Access Control Lists for Event Streams" (`page-261-0`).*
- Use line-of-business ownership (Conway's law): "domain ownership … data,
  schemas, support, discoverability, lineage, quality, interoperability."
  *Ref: Building Event-driven Microservices.md — "Forming a Federated Governance Team" (`page-86-0`) [from companion book].*

**Don't:**
- Don't have two services both `CREATE,WRITE` on the same output stream —
  pick one writer and grant everyone else `READ`.
  *Ref: Building Event-driven Microservices.md — "Table 14-1" (`page-262-0`).*

---

### Event Schema Contracts and Evolution

**Principle:** Schemas are the *data contract*. They must be explicit, evolved
under compatibility rules, and produce typed code for both producer and consumer.

**Do:**
- Use strongly typed schemas (Avro, Protobuf, Thrift) — they provide both an
  evolution framework and code generators for typed classes.
  *Ref: Building Event-driven Microservices.md — "Event Data Definitions and Schemas" (`page-45-0`).*
- Embed schema comments that document the *triggering logic* and field
  semantics (UTC vs ISO timestamp etc.).
  *Ref: Building Event-driven Microservices.md — "Schema Definition Comments" (`page-58-0`).*
- Target **full compatibility** (both backward and forward) by default.
  *Ref: Building Event-driven Microservices.md — "Full compatibility" (`page-59-0`).*
- Check schema compatibility in CI as part of the deployment pipeline.
  *Ref: Building Event-driven Microservices.md — "Predeployment Validation Tests: Schema Validation" (`page-294-0`).*
- Lean on a schema registry that *trails the schemas in an event stream* so
  consumers can look up the schema by ID — "registering the schemas to a
  dedicated event stream frees the schema registry implementation from having
  to provide durable storage."
  *Ref: Building Event-driven Microservices.md — "Schema registry" (`page-258-0`).*

**Don't:**
- Don't rely on *implicit* or "well-known" key/value schemas — "any
  implementation of event-based communication between a producer and consumer
  that lacks an explicit predefined schema will inevitably end up relying on an
  implicit schema."
  *Ref: Building Event-driven Microservices.md — "Using Explicit Schemas as Contracts" (`page-57-0`).*
- Don't overload events with a generic `type` field — the example `productType /
  actionType / watchedPreview / pageId` collapses three events (`MovieClick`,
  `BookClick`, `BookBookmark`) into one and is **explicitly condemned**.
  *Ref: Building Event-driven Microservices.md — "Example: Overloading event definitions" (`page-65-0`).*
- Don't use plain JSON for data products — "I do not recommend JSON, as it
  does not provide full-compatibility schema evolution."
  *Ref: Building Event-driven Microservices.md — "Selecting an Event Format" (`page-63-0`).*
- Don't signal with events (semaphores that just say "data is ready
  elsewhere") — events must *be* the data.
  *Ref: Building Event-driven Microservices.md — "Avoid Events as Semaphores or Signals" (`page-51-0`).*

### Event Design Principles

**Principle:** One logical event per stream; tell the whole truth; use narrowest
types; keep events single-purpose.

**Do:**
- **Tell the truth, the whole truth, nothing but the truth** — an event is the
  complete description of what happened.
  *Ref: Building Event-driven Microservices.md — "Designing Events" (`page-64-0`).*
- One event definition per stream — never mix event types in one stream.
  *Ref: Building Event-driven Microservices.md — "Use a Singular Event Definition per Stream" (`page-64-0`).*
- Use the **narrowest data type** — `int` not string for counts, `long` not `string`
  for IDs, `enum` not `string` for enums.
  *Ref: Building Event-driven Microservices.md — "Use the Narrowest Data Types" (`page-64-0`).*
- Single-purpose events, one business action each. Example shown:
  ```text
  MovieClick  { movieId: Long, watchedPreview: Boolean }
  BookClick   { bookId: Long }
  BookBookmark{ bookId: Long, pageId: Int }
  ```
  *Ref: Building Event-driven Microservices.md — "Example 3-1 / 3-2" (`page-66-0`).*
- **Minimize event size**; consider *claim-check* (pointer to external store) if
  too large, but do it sparingly.
  *Ref: Building Event-driven Microservices.md — "Minimize the Size of Events" (`page-68-0`).*
- Involve prospective consumers in event schema design (joint review).
  *Ref: Building Event-driven Microservices.md — "Involve Prospective Consumers in the Event Design" (`page-51-0`).*

### Event Structure (key/value)

**Principle:** A logical event record has three parts: *key* (entity / partition),
*value* (full public state under a schema), *header* (timestamp, tracing IDs).
Events are immutable.

**Do:**
- Use unkeyed events for singular occurrences.
  ```text
  N/A | ISBN: 372719, Timestamp: 1538913600
  ```
- Use **entity events** keyed on the entity's unique ID — "particularly
  important in event-driven architectures. They provide a continual history
  of the state of an entity and can be used to materialize state."
  *Ref: Building Event-driven Microservices.md — "Entity Event" (`page-41-0`).*
- Use keyed events when you need to **guarantee partition locality** for an
  aggregation/join.
  ```text
  ISBN: 372719 | UserId: A537FE
  ISBN: 372719 | UserId: BB0012
  ```
  *Ref: Building Event-driven Microservices.md — "Keyed Event" (`page-42-0`).*
- Use tombstones (null value for a key) to communicate deletion.
  *Ref: Building Event-driven Microservices.md — "Materializing State from Entity Events" (`page-43-0`).*

---

### Event Brokers vs Message Brokers

**Principle:** Use a **durable, ordered, replayable, indefinitely retained
event log** (Kafka, Pulsar) — *not* a transient message queue.

**Do:**
- Verify infinite retention, tiered storage, replayability, partitioning,
  strict per-partition ordering, immutability, indexing, and replication.
  *Ref: Building Event-driven Microservices.md — "Event Storage and Serving" (`page-46-0`).*
- Use the consumer-group / offset model — each consumer maintains its own
  pointer, multiple consumers each get full copies.
  *Ref: Building Event-driven Microservices.md — "Consuming from the Immutable Log" (`page-50-0`).*
- Hosted services (e.g., Confluent Cloud) are reasonable to outsource; pick ones
  with tiered storage, schema registry, connectors, monitoring.
  *Ref: Building Event-driven Microservices.md — "Hosted services / Tooling" (`page-47-0`).*

**Don't:**
- Don't use ephemeral messaging (NATS) for data communication — "completely
  unsuited for providing the means to communicate data products."
  *Ref: Building Event-driven Microservices.md — "Ephemeral Message-Passing" (`page-66-0`) [companion book by same author, paraphrased here].*
- Don't pick time-capped brokers (e.g., 7-day AWS/GCP/Azure)
  for event products — "MSK / Kinesis / Pub/Sub" not sufficient for indefinite retention.

---

### Data Liberation (Lifting Existing Systems)

**Principle:** Get the data out of legacy systems into streams incrementally.
Choose the liberation strategy based on real-time needs and DB capability.

**Do:**
- Use **change-data capture** (Debezium-class) for low-latency, change-complete
  capture with non-blocking snapshots (DBLog watermark).
  *Ref: Building Event-driven Microservices.md — "Liberating Data Using Change-Data Capture Logs" (`page-78-0`).*
- Use **transactional outbox** for atomic write-the-DB-and-emit-an-event in one
  transaction; query the outbox via a poller or CDC.
  ```python
  conn.autocommit = False
  cursor.execute("Update EcomItem set price = 1299.99 where id = 4291")
  cursor.execute("Insert into EcomItem_Outbox (id, name, price) Values (..., ..., ...)")
  conn.commit()
  ```
  *Ref: Building Event-driven Microservices.md — "Liberating Data Using Outbox Tables" (`page-81-0`).*
- Use **query-based polling** when CDC isn't an option and you control the source
  table; require `updated_at` and use soft-deletes for hard-delete tracking.
  *Ref: Building Event-driven Microservices.md — "Liberating Data by Query" (`page-75-0`).*
- **Eventify** (denormalize) at the outbox or in a downstream service so
  consumers don't have to do joins across normalized streams.
  *Ref: Building Event-driven Microservices.md — "Denormalization and Eventification" (`page-83-0`).*
- *Ref: Building Event-driven Microservices.md — "Kafka Streams / Flink SQL join" (`page-204-0`).*
  ```java
  ecomItemTable.join(merchantTable, EcomItem::getMerchantId, new EcomToMerchantJoiner())
              .toStream()
              .to(enrichedEcomItemTopic, Produced.with(Serdes.Long(), enrichedEcomItemSerde));
  ```
- Validate and serialize **before** writing to the outbox so schema violations
  cause the business transaction to fail (instead of contaminating the outbox).
  *Ref: Building Event-driven Microservices.md — "Ensuring Schema Compatibility" (`page-83-0`).*

**Don't:**
- Don't dual-write to DB and event stream from the application without
  transactional guarantees — "most of the time you won't have a problem"
  right up until network timeouts / broker hiccups silently drop events.
  *Ref: Building Event-driven Microservices.md — "Dual Writes" (`page-189-0`) [companion book].*
- Don't expose internal data models in liberated streams — consumers
  shouldn't have to join all the foreign keys themselves.
  *Ref: Building Event-driven Microservices.md — "Isolating Internal Data Models" (`page-82-0`).*
- Don't rely on CDC as a destination state of architecture — "CDC tools are
  not the final destination in moving to an event-driven architecture, but
  instead are primarily meant to help bootstrap the process."
  *Ref: Building Event-driven Microservices.md — "The Impacts of Sinking and Sourcing on a Business" (`page-92-0`).*

---

### Stream Processing Building Blocks (Stateless)

**Principle:** Compose simple stateless transforms: filter, map, mapValues,
branch, merge, repartition.

**Do:**
- Use Map and Filter for stateless transformation:
  ```text
  myInputStream
   .filter(myFilterFunction)
   .map(myMapFunction)
   .to(outputStream)
  ```
  *Ref: Building Event-driven Microservices.md — "Stateless Functions" (`page-256-0`).*
- **Repartition** when you change the key or partition count for downstream
  copartitioning.
  *Ref: Building Event-driven Microservices.md — "Repartitioning Event Streams" (`page-98-0`).*
- **Copartition** (same partition count + same partitioner + keyed by same
  key) when streams must be joined or aggregated by key.
  *Ref: Building Event-driven Microservices.md — "Copartitioning Event Streams" (`page-100-0`).*
- Use branch / merge carefully — when merging, "define a new unified schema
  representative of the merged event stream domain."
  *Ref: Building Event-driven Microservices.md — "Branching and Merging Streams" (`page-98-0`).*

**Don't:**
- Don't put very large events in a stream — "may want to use a pointer to the
  external store" (claim-check).
  *Ref: Building Event-driven Microservices.md — "Minimize the Size of Events" (`page-68-0`).*

---

### Deterministic Stream Processing (Time + Watermarks + Stream Time)

**Principle:** Aim for the same output whether running real-time or replaying
from the beginning. Pick *event time*; use watermarks or stream time to
track progress; never let wall-clock time or external requests undermine
determinism.

**Do:**
- Pre-process with NTP (sub-millisecond accuracy expected; LAN skew < 15 min);
  accept small skew.
  *Ref: Building Event-driven Microservices.md — "Synchronizing Distributed Timestamps" (`page-109-0`).*
- Pick the right time: *event time* > ingestion time > processing time > wall clock.
  *Ref: Building Event-driven Microservices.md — "Processing Based on Event Time, Processing Time, and Ingestion Time" (`page-94-0`).*
- Use the framework event scheduler that picks the lowest-timestamp unprocessed
  event from all assigned input partitions.
  *Ref: Building Event-driven Microservices.md — "Event Scheduling and Deterministic Processing" (`page-110-0`).*
- Understand watermark vs stream-time tradeoffs:
  - **Watermarks** — declare "all events ≤ *t* have been processed". Node event
    time = min of input sources. (Spark/Flink/Beam)
  - **Stream time** — highest event-time seen so far; never decreases. (Kafka
    Streams). Subtopologies maintain their own stream time across repartition.
  *Ref: Building Event-driven Microservices.md — "Watermarks" (`page-112-0`), "Stream Time" (`page-114-0`).*
- Coalesce duplicates by *idempotent producer* writes (preferred) or
  *dedupe-ID* consumer stores with TTL.
  *Ref: Building Event-driven Microservices.md — "Generating duplicate events" (`page-146-0`).*
- Request-response calls inside the topology make the workflow *nondeterministic*
  — cache results and document the trade-off.
  *Ref: Building Event-driven Microservices.md — "Request-Response Calls to External Systems" (`page-95-0`).*
- Handle late events with one of:
  1. **Drop** — simplest; tolerable for measurement-style data.
  2. **Wait** — bounded delay before emitting window.
  3. **Grace period** — emit immediately + continue correcting during grace.
  *Ref: Building Event-driven Microservices.md — "Handling Late Events" (`page-122-0`).*
- Reprocessing: always start entity streams from *the beginning of time* —
  "if you reprocessed someone's bank balance and accidentally omitted previous
  paychecks" you'd be wrong.
  *Ref: Building Event-driven Microservices.md — "Reprocessing Versus Processing in Near-Real Time" (`page-124-0`).*

**Don't:**
- Don't let producer/broker connectivity outages corrupt your late-event logic
  silently — events buffered locally during outage will look "late" on the
  consumer side.
  *Ref: Building Event-driven Microservices.md — "Producer/Event Broker Connectivity Issues" (`page-125-0`).*
- Don't create nondeterministic custom event schedulers unless you must — they
  usually can't reproduce results under reprocessing.
  *Ref: Building Event-driven Microservices.md — "Custom Event Schedulers" (`page-94-0`).*

---

### Stateful Streaming & Materialized Views

**Principle:** Materialize entity event streams into local state stores. Use
changelogs for durability; rely on the broker's compacted topic support.

**Do:**
- Distinguish *materialized state* (immutable projection) from *state store*
  (mutable) — both required.
  *Ref: Building Event-driven Microservices.md — "State Stores and Materializing State" (`page-128-0`).*
- Use **changelogs** for state backup. Compacted changelogs need only the
  most-recent key/value pair to rebuild.
  *Ref: Building Event-driven Microservices.md — "Recording State to a Changelog Event Stream" (`page-129-0`).*
- Use **internal state stores** (RocksDB) for throughput (15.4k req/s on SSD
  vs 939 req/s with 1 ms network latency).
  *Ref: Building Event-driven Microservices.md — "Advantages of Using Internal State" (`page-131-0`).*
- Use **hot replicas** (Kafka Streams `replication-factor=2`) for zero-downtime
  scaling/failure recovery.
  *Ref: Building Event-driven Microservices.md — "Using hot replicas" (`page-134-0`).*
- For external state stores, ensure strict logical separation from other
  microservices — "Do not share direct state access with other microservices."
  *Ref: Building Event-driven Microservices.md — "Materializing State to an External State Store" (`page-137-0`).*
- When rebuilding state: stop instance, reset offsets to the beginning,
  delete intermediate state, rebuild from input streams.
  *Ref: Building Event-driven Microservices.md — "Rebuilding" (`page-141-0`).*
- For **windowed aggregations**: use stateful operators (Kafka Streams,
  Flink). Sample session-window code:
  ```java
  clickStream.union(viewStream)
              .keyBy(...)
              .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
              .aggregate(...)
              .addSink(<producer>);
  ```
  *Ref: Building Event-driven Microservices.md — "Example: Session Windowing of Clicks and Views" (`page-211-0`).*

**Don't:**
- Don't rebuild state for trivial schema changes — fix the change rather than
  the migration logic.
  *Ref: Building Event-driven Microservices.md — "Migrating" (`page-141-0`).*
- Don't use **global** materialization for event-driven logic — every instance
  would produce duplicates.
  *Ref: Building Event-driven Microservices.md — "Materializing Global State" (`page-131-0`).*

---

### Effectively-Once Processing

**Principle:** Process each input *effectively once* (at-least-once delivery
+ idempotent operations = exactly-once effect). Use the broker's transactional
features where available.

**Do:**
- Combine output + state + offset updates in **one transaction** when the
  broker supports it (Kafka does, Pulsar is catching up):
  *Ref: Building Event-driven Microservices.md — "Effectively Once Processing with Client-Broker Transactions" (`page-142-0`).*
- Use **idempotent producer** writes — broker dedupes retries.
  *Ref: Building Event-driven Microservices.md — "Idempotent writes" (`page-141-0`).*
- When transactions aren't available, maintain a *local transaction* between
  state and offsets in the same DB.
  *Ref: Building Event-driven Microservices.md — "Maintaining consistent state" (`page-149-0`).*
- If you can't dedupe upstream, generate a *dedupe ID* from high-cardinality
  fields and keep a TTL-bounded dedup cache keyed by it.
  *Ref: Building Event-driven Microservices.md — "Identifying duplicate events" (`page-147-0`).*
- Build dedup stores *within a single event stream partition* — partition-local.
  *Ref: Building Event-driven Microservices.md — "Guard against duplicates" (`page-148-0`).*

**Don't:**
- Don't try to dedup events without a key — "no guarantee of partition
  locality."
  *Ref: Building Event-driven Microservices.md — "Identifying duplicate events" (`page-147-0`).*
- Don't depend on exactly-once broker writes *and* on non-transactional
  state-store updates — they won't both be atomic.
  *Ref: Building Event-driven Microservices.md — "Maintaining consistent state" (`page-149-0`).*

---

### Workflows: Choreography vs Orchestration

**Principle:** Pick the coordination pattern that matches your complexity.

**Do:**
- Use **choreography** for 2–3 step simple workflows with stable ordering —
  "each service knows its own role and performs it independently."
  *Ref: Building Event-driven Microservices.md — "The Choreography Pattern" (`page-153-0`).*
- Use **orchestration** when workflow changes are likely, observability is
  needed, and many steps/saga compensation are required.
  *Ref: Building Event-driven Microservices.md — "The Orchestration Pattern" (`page-156-0`).*
- Keep the orchestrator *only* in charge of workflow logic — no business
  fulfillment, no retry policy duplication. Workers own their own retries, error
  handling, and intermittent-failure management.
  *Ref: Building Event-driven Microservices.md — "Ensure the orchestrator's bounded context is limited" (`page-157-0`).*
- For distributed transactions, use the **saga pattern**: each service owns
  reversal of its own work; both forward and reverse actions must be
  *idempotent*.
  *Ref: Building Event-driven Microservices.md — "Distributed Transactions" (`page-161-0`).*
- For customer-facing workflows, prefer **compensating workflows** (e.g.,
  notify + offer discount on oversold tickets) over strict rollbacks when
  customer experience matters.
  *Ref: Building Event-driven Microservices.md — "Compensation Workflows" (`page-165-0`).*

**Don't:**
- Don't build a "God orchestrator" that issues granular commands to weak
  workers — "this anti-pattern spreads workflow business logic between the
  orchestrator and the worker services, making for poor encapsulation."
  *Ref: Building Event-driven Microservices.md — "Creating and Modifying an Orchestration Workflow" (`page-160-0`).*
- Don't mix choreographed and orchestrated transactions within the same saga
  silently — listeners need both *output* and *failure* streams for full
  status.
  *Ref: Building Event-driven Microservices.md — "Choreography Example" (`page-162-0`).*

---

### Microservice Implementation Patterns

**Principle:** Choose per-service implementation style by need: BPC for
simplicity, FaaS for spiky/integration use, lightweight frameworks for
stateful joins, heavyweight only when you truly need big-data engines.

**Do:**
- Use **Basic Producer/Consumer (BPC)** for integration with legacy systems,
  stateful business logic not reliant on event order (gating pattern), and
  data-layer-does-most-of-the-work scenarios.
  *Ref: Building Event-driven Microservices.md — "Where Do BPCs Work Well?" (`page-187-0`).*
- Use **FaaS** for stateless, highly variable workloads; commit offsets *after
  processing* to get at-least-once delivery.
  *Ref: Building Event-driven Microservices.md — "Ensure Strict Membership to a Bounded Context" (`page-168-0`).*
- Run FaaS functions in **orchestrated synchronous chains** when ordering
  matters across multiple function calls.
  *Ref: Building Event-driven Microservices.md — "Functions Calling Other Functions" (`page-178-0`).*
- For FaaS, "fewer functions are better than many granular functions" — one
  function per microservice when feasible.
  *Ref: Building Event-driven Microservices.md — "Less Is More" (`page-170-0`).*
- For **stateful stream joins**, use lightweight frameworks (Kafka Streams,
  Samza Embedded) so joins, copartitioning, and state are first-class:
  ```java
  KTable<Long, Merchant> merchantTable = builder.table(Serdes.Long(), merchantSerde, merchantTopic);
  KTable<Long, EcomItem> ecomItemTable = builder.table(Serdes.Long(), ecomItemSerde, ecomItemTopic);
  ecomItemTable.join(merchantTable, EcomItem::getMerchantId, new EcomToMerchantJoiner())
              .toStream()
              .to(enrichedEcomItemTopic, Produced.with(Serdes.Long(), enrichedEcomItemSerde));
  ```
  *Ref: Building Event-driven Microservices.md — "Stream-Table-Table Join: Enrichment Pattern" (`page-222-0`).*
- Use heavyweight (Spark/Flink/Storm/Heron/Beam) only if your org already
  operates one and the workload genuinely requires big-data engines.
  *Ref: Building Event-driven Microservices.md — "Heavyweight Framework Microservices" (`page-194-0`).*
- For heavyweight frameworks, prefer *CMS-integrated* deployment (e.g., Flink
  on Kubernetes session cluster) over dedicated cluster.
  *Ref: Building Event-driven Microservices.md — "Create Clusters with CMS Integration" (`page-200-0`).*

**Don't:**
- Don't write custom libs to mimic built-in event scheduling if you can pick a
  lightweight framework that gives it to you for free.
  *Ref: Building Event-driven Microservices.md — "Conclusion: Microservice Implementation Options" (`page-306-0`).*

---

### Idempotency, Dead-Letter & Retry

**Principle:** All side-effects must tolerate retries; failures must go to a
dead-letter queue without blocking the consumer.

**Do:**
- Retry idempotently; commit offsets only after processing — "this strategy
  provides the strongest guarantee that events will be processed at least once."
  *Ref: Building Event-driven Microservices.md — "When the function has completed its processing" (`page-169-0`).*
- Route failures to a dead-letter output stream for later inspection.
  *Ref: Building Event-driven Microservices.md — "Branching and Merging Streams" (`page-98-0`).*

**Don't:**
- Don't commit offsets *before* processing completes when data loss is
  unacceptable — "if the function is unable to successfully process an event,
  and numerous retries fail, then data loss is likely."
  *Ref: Building Event-driven Microservices.md — "When the function has first started" (`page-169-0`).*

---

### Request-Response + Async Hybrid

**Principle:** Use event streams for the data communication layer; use REST
APIs to expose materialized state and to receive external client traffic.

**Do:**
- Convert external synchronous analytical events into event-stream events
  via an *event-receiver* service.
  *Ref: Building Event-driven Microservices.md — "Handling Autonomously Generated Analytical Events" (`page-229-0`).*
- Use a *smart load balancer* that applies the partitioner to route GET
  requests to the instance that owns the partition.
  ```text
  success-rate = 1 / number of instances
  ```
  *Ref: Building Event-driven Microservices.md — "Serving Real-Time Requests with Internal State Stores" (`page-234-0`).*
- For hot-replica serving, expect stale reads proportional to replication
  lag.
  *Ref: Building Event-driven Microservices.md — "Hot replicas of state stores" (`page-235-0`).*
- Externalize state to *one bounded context only* — materializing state for
  another microservices' state store is an anti-pattern.
  *Ref: Building Event-driven Microservices.md — "Materializing State to an External State Store" (`page-137-0`).*
- For BPC, parse external REST responses into your own schematized event and
  route via DLQ on non-200 responses.
  *Ref: Building Event-driven Microservices.md — "Integrating with Third-Party Request-Response APIs" (`page-232-0`).*

**Don't:**
- Don't have UI assume synchronous-success response when async; show
  "please-wait" affordance; "research and implement best practices for
  asynchronous UIs."
  *Ref: Building Event-driven Microservices.md — "Processing Events for User Interfaces" (`page-241-0`).*
- Don't let UIs cause duplicate events via network-retry storms without
  idempotent upstream consumers.
  *Ref: Building Event-driven Microservices.md — "Intermittent network failures" (`page-242-0`).*

---

### Supportive Tooling (Automation)

**Principle:** Pay the microservice tax: schema registry, ownership/ACL system,
stream metadata, lag monitor, offset reset, multi-cluster replication tool, and
topology visualization, all programmatically exposed to teams.

**Do:**
- Tag streams with `owner`, `PII`, `financial`, `namespace`, `deprecated`.
  *Ref: Building Event-driven Microservices.md — "Event Stream Metadata Tagging" (`page-257-0`).*
- Use a microservice-to-team assignment system for all ownership decisions.
  *Ref: Building Event-driven Microservices.md — "Microservice-to-Team Assignment System" (`page-256-0`).*
- Monitor *consumer-group lag* with hysteresis to drive autoscaling.
  *Ref: Building Event-driven Microservices.md — "Consumer Offset Lag Monitoring" (`page-263-0`).*
- Drive topology visualization off the permissions/ACL structure — *not*
  self-reporting; self-reporting is voluntary and incomplete.
  *Ref: Building Event-driven Microservices.md — "Dependency Tracking and Topology Visualization" (`page-267-0`).*
- Send schema-change notifications to teams whose services depend on the
  changed schema (cross-referenced via ACLs).
  *Ref: Building Event-driven Microservices.md — "Schema Creation and Modification Notifications" (`page-260-0`).*
- Treat consumer-group offset mutations as a privileged, audited operation
  owned by the application's team.
  *Ref: Building Event-driven Microservices.md — "Offset Management" (`page-260-0`).*

---

### Testing Event-Driven Microservices

**Principle:** Modularity means testability. Unit-test pure topology functions;
topology-test the framework; integration-test end-to-end.

**Do:**
- Unit-test stateless (filter/map/reduce) functions first.
  ```text
  myInputStream.filter(myFilterFunction).map(myMapFunction).to(outputStream)
  ```
  *Ref: Building Event-driven Microservices.md — "Stateless Functions" (`page-256-0`).*
- For stateful units, either mock the data store or run a temporary instance.
  *Ref: Building Event-driven Microservices.md — "Stateful Functions" (`page-256-0`).*
- Use framework topology testing (Kafka Streams `TopologyTestDriver`,
  Flink `StreamExecutionEnvironment`, Beam) — no full broker required.
  *Ref: Building Event-driven Microservices.md — "Testing the Topology" (`page-257-0`).*
- For integration, bring up broker + schema registry + microservice in
  either the test runtime or a container (preferred).
  *Ref: Building Event-driven Microservices.md — "Create a Temporary Environment Within the Runtime of Your Test Code" (`page-260-0`).*
- Use production data (de-sensitized) or schema-derived mock events; reserve
  shared test environments for emergency use only ("dumping ground of confusing
  event streams").
  *Ref: Building Event-driven Microservices.md — "Testing Using a Shared Environment" (`page-285-0`).*
- Make sure you can simulate broker outages, repartition rebalances, schema
  compatibility failures.
  *Ref: Building Event-driven Microservices.md — "Local Integration Testing" (`page-276-0`).*

**Don't:**
- Don't test *only* against production smoke data — add controlled
  out-of-order, malformed, time-skewed, and boundary events.
  *Ref: Building Event-driven Microservices.md — "Testing the Topology" (`page-257-0`).*

---

### Deployment Patterns

**Principle:** Pick the deployment pattern by compatibility risk.

**Do:**
- **Rolling update** when there are no breaking changes to topology or schemas.
  *Ref: Building Event-driven Microservices.md — "The Rolling Update Pattern" (`page-295-0`).*
- **Basic full-stop** when topology or state shape changes (rebuilds required).
  *Ref: Building Event-driven Microservices.md — "The Basic Full-Stop Deployment Pattern" (`page-293-0`).*
- **Breaking-schema change**: prefer **eventual migration via two event
  streams** (deprecated + new) so consumers can migrate at their own pace;
  tag the old stream `deprecated` and warn new consumers.
  *Ref: Building Event-driven Microservices.md — "Eventual Migration via Two Event Streams" (`page-297-0`).*
- **Synchronized migration** only when the old schema truly cannot coexist
  and inconsistency is intolerable.
  *Ref: Building Event-driven Microservices.md — "Synchronized Migration to the New Event Stream" (`page-298-0`).*
- **Blue-green** is fine for stream-consumers but does NOT work for services
  that produce events in response to inputs — they will "create duplicated
  events in the case of event streams."
  *Ref: Building Event-driven Microservices.md — "Blue-Green Deployment Pattern" (`page-299-0`).*
- CI pipeline must include: event-stream validation, schema evolution
  validation.
  *Ref: Building Event-driven Microservices.md — "Predeployment Validation Tests" (`page-294-0`).*
- Communicate downstream impact: SLA, downstream reprocessing spike, new
  streams, breaking changes.
  *Ref: Building Event-driven Microservices.md — "Consider event stream reprocessing impacts" (`page-291-0`).*

**Don't:**
- Don't do rolling updates when topology would break — "inadvertently
  altering the internal microservice topology is one of the most common
  mistakes."
  *Ref: Building Event-driven Microservices.md — "The Rolling Update Pattern" (`page-295-0`).*
- Don't let migrations stall — "one of the main risks of eventual migration
  is that the migration is never finished."
  *Ref: Building Event-driven Microservices.md — "Eventual Migration via Two Event Streams" (`page-298-0`).*

---

## Anti-Patterns & Common Mistakes
- **Implicit / schemaless events.** *fix:* explicit schema-registry-backed
  schemas with full-transitive compatibility.
- **Delta events across domain boundaries.** Producer encodes internal
  state-transitions; consumers must replicate producer's aggregation logic;
  ownership inverts.
  *Ref: Building Event-driven Microservices.md — "Chapter 6" [from companion Data Mesh book].*
- **Dual writes (DB + event stream).** *fix:* transactional outbox or CDC.
- **Two writers for the same stream.** *fix:* enforce Single Writer via ACLs.
- **Global materialization for event-driven logic.** *fix:* partition-local
  state with hot replicas for HA.
- **Boundaries on technical layers instead of business boundaries.**
  *fix:* realign bounded contexts on business requirements.
- **Distributed monolith of synchronous point-to-point microservices.**
  *fix:* event-driven microservices + 1:1 bounded-context alignment.
- **Heavyweight framework chosen for a single microservice** that could
  have been a BPC.
  *fix:* BPC for integration, lightweight framework for stateful joins,
  heavyweight only when you really have big-data engines.
- **Migration-without-deprecation-tag** — new consumers accidentally
  subscribe to the dying stream.
  *fix:* metadata tag + blocked-on-deprecated.
- **Subscribing via shared DB** because "the request-response is easier."
  *fix:* materialize via event streams, expose via REST.

---

## Decision Heuristics / Checklists
- **Choreography vs Orchestration?**
  - 2–3 services, stable ordering: **choreography**.
  - Many steps, saga compensations, frequent workflow change: **orchestration**.
- **CDC vs Polling vs Outbox?**
  - Need < 1 s latency + DB exposes WAL/binlog: **CDC**.
  - No WAL + you control DB: **Outbox**.
  - Read-only, large-volume + soft deletes acceptable: **Polling**.
- **State store internal vs external?**
  - Hot data + sub-15 ms reads + single tenant: **internal**.
  - Shared, queryable, scalable independent: **external**.
- **Stream-time vs Watermarks?**
  - Need shuffle via internal broker topic: **stream time** (Kafka Streams).
  - Heavyweight shuffle via cluster: **watermarks** (Flink/Spark/Beam).
- **Full-stop vs Rolling vs Blue-Green?**
  - No breaking changes: **Rolling**.
  - Topology change: **Full-stop**.
  - Pure read-side change: **Blue-Green** is OK.
- **FaaS cold start tolerance?** If > 100 ms latency ok, fine; otherwise
  keep a warm function or use BPC.

---

## Key Takeaways
1. Use the **event broker** as the single source of truth; never let
   service code depend on another service's DB.
2. Adopt the **Single Writer Principle** for every stream — enforced via
   event-broker ACLs tied to a team-ownership registry.
3. Define **explicit schemas** with full-transitive compatibility;
   use a schema registry that tails a dedicated schemas stream.
4. Prefer **state events (ECST)** for cross-boundary data products; reserve
   delta events for in-domain event-sourcing.
5. Pick the right **liberation strategy**: CDC for hot paths, transactional
   outbox for atomicity, polling for legacy/greenfield.
6. Materialize into **partition-local state stores** + changelogs; design
   around copartitioning for joins.
7. Use **idempotent producers + deduplication IDs** for effectively-once;
   combine output+state+offsets in a single transaction when supported.
8. Default to **choreography**; reach for orchestration/saga/compensation
   only as workflow complexity grows.
9. Pay the **microservice tax**: schema registry, lag monitoring, offset
   reset, multi-cluster replication, topology visualization.
10. Pick deployment patterns by **compatibility risk**: rolling for safe
    changes, full-stop for topology changes, eventual migration for schema
    breaks; never blue-green a service that produces events from inputs.

---

## Cross-References
- Related: `../Building_An_Event-Driven_Data_Mesh.md` (companion volume —
  data-product/event-design guidelines).
- Related: `../Communication_Patterns.md` (channel / routing patterns that
  map to event-broker topologies).
- Related: `../Flow_Architectures.md` (streaming SQL, backpressure,
  composition of flow services).
- Related: `../Monolith_To_Microservices.md` (practical migration tactics
  that often start from a monolithic backend service).
- Topic index: `../INDEX.md`
