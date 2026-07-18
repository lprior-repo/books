# Building Event-Driven Microservices

**Author:** Adam Bellemare
**Topic tags:** `#architecture` `#api` `#concurrency` `#reliability` `#testing`
**Language focus:** Language-agnostic (Kafka/Pulsar/RabbitMQ examples; Java/Scala for frameworks)
**Sources:** `markdown_output/Building Event-driven Microservices/Building Event-driven Microservices.md` · `summaries/Building_Event-driven_Microservices.md`

## TL;DR
Event-driven microservices replace direct, synchronous, point-to-point connections between services with **immutable event streams** that act as the organization's single source of truth. Producers publish to event streams (each event a statement of fact); consumers build their own materialized state from those streams at their own cadence. Boundaries are *bounded contexts* (DDD), not technical layers. Reliable messaging requires idempotency, transactions or dedupe, copartitioning for stateful joins, schema evolution, sagas for distributed transactions, and rigorous testing of the topology. The medium *is* the message: this architecture reshapes teams and businesses.

---

## Best Practices by Topic

### The Medium Is the Message — Why Async Changes Everything

**Principle:** Asynchronous, replayable, indefinitely-retained event streams are a *new medium* that reshapes how teams and businesses communicate — not just a transport swap. Adoption at scale requires a cultural shift as much as a technical one (Conway's law in reverse).

**Do:**
- Treat event streams as the central nervous system of the organization.
- Recognize that adoption changes how the *business* operates, not just how services are wired.
- Anchor engineering investment on durable data, on-demand compute, and microservices with flexible storage — these together make event-driven microservice architectures possible.

**Don't:**
- Don't sell event-driven as a "drop-in replacement for request-response" — it isn't.
- Don't underestimate the cultural shift; without executive buy-in, projects stall.

**Code:**
> "The tools that we use shape and influence our inventions significantly. Event-driven microservice architectures are made possible by a whole host of technologies that have only recently become readily accessible. Distributed, fault-tolerant, high-capacity, and high-speed event brokers underpin the architectures and design patterns in this book."

*Ref: Building Event-driven Microservices.md — "Preface"*

---

### Bounded Contexts First; Technology Layers Last

**Principle:** Align microservices on **business bounded contexts** (DDD), not technical layers (e.g., "data layer" / "application layer"). Cross-cutting technical alignment distributes responsibility across teams and couples bounded contexts on every change. Sole ownership (one team owning one bounded context end-to-end) enables autonomous service evolution.

**Do:**
- Pick business requirements → derive subdomain → derive bounded context → derive service.
- Ensure high *cohesion* (most comms internal) and low *coupling* (changes bounded to one context).
- Promote code duplication over premature coupling on data sources.
- Give vertical teams full-stack expertise; centralize common tooling (operationalize).

**Don't:**
- Don't organize teams along technical layers (UI / business logic / DB).
- Don't make every team a "data team" — decouple ownership of data from access to it.
- Don't break bounded context boundaries in the name of DRY.

**Code:**
> "Modeling event-driven microservices architectures around business requirements is preferred, though there are tradeoffs with this approach. Code may be replicated a number of times, and many services may use similar data access patterns. Product developers may try to reduce repetition by sharing data sources with other products or by coupling on boundaries. In these cases, the subsequent tight coupling may be far more costly in the long run than repeating logic and storing similar data."

*Ref: Building Event-driven Microservices.md — "Aligning Bounded Contexts with Business Requirements"*

---

### Communication Structures: Business, Implementation, Data

**Principle:** Three communication structures exist in any organization: **business** (teams), **implementation** (code/data), **data** (how data flows between implementations). Traditional setups blur data comm into implementation comm — poor data sharing, monolithic pressure, slow change.

**Do:**
- Distinguish the three structures explicitly in architecture review.
- Invest in the *data communication structure*: a formalized event-stream backbone.
- Use the absence of a data communication structure as a diagnostic indicator — if data is hard to get or monoliths scope-creep, you have one.
- Make events the data, not just signals — they are both storage and comm.

**Don't:**
- Don't conflate implementation communication structure and data communication structure.
- Don't rely on databases with read-replicas or batch dumps as "data sharing" — they expose internal models.
- Don't assume Conway's law applies only to monolithic orgs.

**Code:**
> "If you find that it is too hard to access data in your organization or that your products are scope-creeping because all the data is located in a single implementation, you're likely experiencing the effects of poor data communication structures. This problem will be magnified as the organization grows, develops new products, and increasingly needs to access commonly used domain data."

*Ref: Building Event-driven Microservices.md — "Communication Structures in Traditional Computing"*

---

### Event Streams Are the Single Source of Truth

**Principle:** Adopt the event stream narrative as the **single source of truth** for any data other teams or services need. Producers' job is *only* to publish well-defined data into their streams; consumers pull as needed. Implementation structures no longer serve data-sharing dual duty.

**Do:**
- Commit org-wide to "any cross-context data goes through the broker."
- Mark a stream as deprecated when retiring a feed; grandfather consumers until migrated.
- Use the event stream as the implementation's data backbone, not just a side-channel.
- Ensure stream data is the *authoritative* version — disagreements between stream and source DB are producer failures.

**Don't:**
- Don't let teams quietly fork data into other stores.
- Don't make consumers interpret data they should be getting structurally.
- Don't treat the event broker as one option among many — for the organization it's the *default* for cross-context data.

**Code:**
> "Adopting the event broker as the single source of truth requires a culture shift in the organization. Whereas previously a team may simply have written direct SQL queries to access data in a monolith's database, now the team must also publish the monolith's data to the event broker. The developers managing the monolith must ensure that the data produced is fully accurate, because any disagreement between the event streams and the monolith's database will be considered a failure of the producing team."

*Ref: Building Event-driven Microservices.md — "Providing a Single Source of Truth"*

---

### Event-Driven vs Synchronous Microservices (Tradeoffs)

**Principle:** Synchronous microservices have well-known benefits (ease of tracing, fast requests, hiring pool, real-time UI). Event-driven offers unparalleled flexibility for *data-heavy* organizations. The choice isn't "EDM always wins" — most shops run *hybrid* architectures.

**Do:**
- Use direct-call for: authenticating a user, A/B test reporting, third-party HTTP integrations, browser/mobile UIs that need timely responses.
- Use event-driven when: data is core to the business, multiple teams need it, scale/independence/flexibility matter.
- Foresee a hybrid architecture and pick the right tool per job.

**Don't:**
- Don't promise that EDM solves everything.
- Don't underestimate the value of fast synchronous tracing for transactional flows.

**Code:**
> "Neither point-to-point request-response microservices nor asynchronous event-driven microservices are strictly better than the other. Both have their place in an organization, as some tasks are far better suited to one over the other."

*Ref: Building Event-driven Microservices.md — "Synchronous Microservices"*

---

### Event Types — Unkeyed, Keyed, Entity

**Principle:** Three event types organize the universe. **Unkeyed** events are facts (no partition association). **Entity** events describe a keyed entity's state (current value reconstructible from latest). **Keyed** events are facts about a key without being entities (used for partitioning/co-location).

**Do:**
- Use entity events for state that other consumers materialize.
- Use keyed events when you need partition-local processing for non-entity streams (e.g., per-user click stream).
- Use unkeyed events only for non-aggregating signals.

**Don't:**
- Don't produce entity events without tombstone support for deletions (key + null value).
- Don't mix event types in the same stream.

**Code:**
```
TypeEnum: Book, Movie
ActionEnum: Click
ProductEngagement {
 productId: Long,
 productType: TypeEnum,
 actionType: ActionType
}
```
*(Anti-pattern: a "type" field in an event — see "Single-Purpose Events" below.)*

*Ref: Building Event-driven Microservices.md — "The Structure of an Event"*

---

### Table-Stream Duality: Materialization Is Everywhere

**Principle:** A table is the latest-event projection of a keyed entity stream. Conversely, every change to a table can become an event. This duality is *fundamental* to state in event-driven microservices — every materialized view is a continuous projection of a stream.

**Do:**
- Treat *every* stateful backing as materialization from events.
- Use **tombstones** (keyed event with null value) to mark deletions.
- Use **compaction** (event-broker feature) for entity streams — keep only the latest per key.
- Build apps so that any local state is reconstructible by re-reading the stream.

**Don't:**
- Don't write to a state store without a corresponding event — that's an unobservable mutation.
- Don't keep deleted data after compaction without explicit retention policy.

**Code:**
> "Append-only immutable logs may grow indefinitely unless they are compacted. Compaction is performed by the event broker to reduce the size of its internal logs by retaining only the most recent event for a given key. Older events of the same key will be deleted, and the remaining events compacted down into a new and smaller set of files."

*Ref: Building Event-driven Microservices.md — "Materializing State from Entity Events"*

---

### Microservice Single-Writer Principle

**Principle:** One and only one microservice owns each event stream. The owner is authoritative. ACLs enforce ownership (the producer permits READ; ACLs prevent anyone else from writing).

**Do:**
- Make ownership explicit (microservice-to-team assignment system).
- Use ACLs to prevent accidental dual writes.
- Use single-writer to ensure data lineage.

**Don't:**
- Don't allow multiple services to write to the same stream.
- Don't let a "convenience" co-producer creep in — it breaks lineage.

*Ref: Building Event-driven Microservices.md — "Microservice Single Writer Principle"*

---

### Event Broker Required Capabilities (Storage & Serving)

**Principle:** Production-grade event brokers expose: **partitioning**, **strict ordering within partition**, **immutability**, **indexing (offsets)**, **infinite retention**, **replayability**. Without these you can't build the patterns in the book.

**Do:**
- Validate each capability in your broker of choice.
- Use offsets in monitoring (consumer lag) and scale triggers.
- Lean on infinite retention to provide replay durability.

**Don't:**
- Don't choose a queue-only broker and expect to satisfy all the book patterns.
- Don't assume a 7-day retention is sufficient — that constrains replay fundamentally.

*Ref: Building Event-driven Microservices.md — "Event Storage and Serving"*

---

### Event Brokers vs Message Brokers (Crucial Distinction)

**Principle:** Event brokers are not message brokers. Message brokers delete on ack; event brokers retain; message brokers split consumption (each consumer sees a subset), event brokers give every independent consumer the full stream via offsets.

**Do:**
- Choose event broker (Kafka / Pulsar) for any "single source of truth" use case.
- Choose message broker for ephemeral work distribution (SQS-style).
- Don't try to bend a message broker into a replayable log.

**Don't:**
- Don't mistake an SQS-style queue for a stateful event stream — message brokers delete on ack.
- Don't believe "we have Kafka, we have event-driven" if your consumers are treated as queues.

**Code:**
> "Event brokers, on the other hand, are designed around providing an ordered log of facts. Event brokers meet two very specific needs that are not satisfied by the message broker. For one, the message broker provides only *queues* of messages, where the consumption of the message is handled on a per-queue basis."

*Ref: Building Event-driven Microservices.md — "Event Brokers Versus Message Brokers"*

---

### The Microservice Tax — Pay It or Stay Small

**Principle:** Microservices impose a "tax" (financial, manpower, opportunity) — event broker, CMS, deployment pipelines, monitoring, logging. Pay it centrally via a platform team; don't let each team reimplement independently or you get fragmented unsustainability.

**Do:**
- Centralize: event-broker, schema registry, CMS, monitoring/logging platform.
- Provide self-service tooling on top of central infrastructure.
- Plan long-term operational costs (cluster, networking, expertise).

**Don't:**
- Don't try to adopt microservices before paying enough of the tax.
- Don't undersize the team — small orgs may do better with a modular monolith.

**Code:**
> "Paying the microservice tax is not a trivial matter, and it is one of the largest impediments to getting started with EDM. Small organizations would likely do best to stick with an architecture that better suits their business needs, such as a modular monolith."

*Ref: Building Event-driven Microservices.md — "Paying the Microservice Tax"*

---

### Containers vs VMs for Microservices

**Principle:** Containers (Docker) win on speed and resource overhead; VMs win on isolation. Newer micro-VM tech (gVisor, Firecracker, Kata) blurs the line. Choose based on security vs performance/operational tradeoff.

**Do:**
- Default to containers for typical workloads.
- Use micro-VMs when shared-tenant security demands better isolation.
- Pick a CMS that supports both (Kubernetes + Kata/gVisor; ECS + Firecracker).

**Don't:**
- Don't write off containers because of shared-kernel concerns if the threat model doesn't warrant it.
- Don't insist on VMs everywhere — operational cost is much higher.

*Ref: Building Event-driven Microservices.md — "Managing Microservices at Scale"*

---

### Explicit Schemas (Avro / Protobuf) Over JSON

**Principle:** Strongly-defined formats (Avro, Protobuf, Thrift) give schema evolution and code generation. JSON lacks full-compatibility schema evolution. Plain-text "flexible" formats shift the burden to consumers — don't.

**Do:**
- Use Avro or Protobuf for production event formats.
- Store schemas in a registry (Confluent Schema Registry, etc.).
- Generate typed classes from the schema.
- Treat schema IDs as part of the event envelope.

**Don't:**
- Don't ship JSON-only events without an explicit schema and evolution rules.
- Don't depend on tribal knowledge to evolve implicit formats.

*Ref: Building Event-driven Microservices.md — "Selecting an Event Format"*

---

### Event Schema Design Principles

**Principle:** Events are statements of fact that must be the **whole truth** of what happened. Each stream has **one** event definition. Use narrow types. Keep events single-purpose. Minimize size. Involve consumers. Don't use events as semaphores.

**Do:**
- Encode the *complete* business occurrence (no partial messages + lookup).
- Use one definition per stream; never mix evolutionarily-incompatible types.
- Use enums (not strings) for fixed value sets; Protobuf/Avro handle unknown enum tokens.
- Carry keys for partition association; values for *the* truth of the event.

**Don't:**
- Don't add a `type` field to overload an event — split it into separate event types/streams.
- Don't use string for numerics, integer for boolean, string for enum.
- Don't return "thou shalt fetch elsewhere" — events *are* the data.
- Don't make events act as flags/semaphores — they create dual sources of truth.

**Code:** Anti-pattern (split it instead):
```
TypeEnum: Book, Movie
ActionEnum: Click
ProductEngagement {
 productId: Long,
 productType: TypeEnum,
 actionType: ActionType
}
```

Good pattern (single-purpose):
```
MovieClick {
 movieId: Long,
 watchedPreview: Boolean
}
BookClick {
 bookId: Long
}
BookBookmark {
 bookId: Long,
 pageId: Int
}
```

*Ref: Building Event-driven Microservices.md — "Designing Events"*

---

### Schema Compatibility Types (Forward / Backward / Full)

**Principle:** Compatibility types determine who-can-update-when. **Forward compatibility**: newer producer data readable as older consumer. **Backward**: older producer data readable as newer consumer. **Full** = both. Default to full; loosen later if needed.

**Do:**
- Default to **full compatibility** (union of forward+backward).
- Add fields with defaults (not required) for forward compat.
- Always support older consumers if you've deployed widely (mobile, embedded).

**Don't:**
- Don't expect consumers to upgrade every time the producer changes the schema.
- Don't rename or change types incompatibly — that's breaking.

*Ref: Building Event-driven Microservices.md — "Full-Featured Schema Evolution"*

---

### Breaking Schema Changes — Two Patterns

**Principle:** When a breaking change is unavoidable, choose between (a) contended entity schema — leave old on old stream, create new; (b) non-entity events — new stream for new format, old stream eventually purged.

**Do:**
- Coordinate early and clearly with consumers.
- For entities: keep old entities under old schema *and* old stream (forensic); emit new entities on new stream under new schema.
- For non-entities: create a new stream for the new event; let consumers self-migrate; let retention purge.

**Don't:**
- Don't expect consumers to interpret divergent schemas — push resolution to the producer.
- Don't mix evolutionarily-incompatible event types in one stream.
- Don't break the data contract without renegotiation and approval.

*Ref: Building Event-driven Microservices.md — "Breaking Schema Changes"*

---

### Code Generators Make Producers and Consumers Honest

**Principle:** A code generator compiles your schema into typed classes; the producer's compiler enforces non-null fields and types. Consumers deserialize and convert via version-coercion rules. Reduces data quality issues at compile-time.

**Do:**
- Generate code for both producer and consumer sides.
- Run code-gen as part of CI; check the generated source into the repo.
- Use the schema-registry-provided ID rather than embedding the full schema on the wire.

**Don't:**
- Don't rely on language-level `Any`/`Map<string,string>` instead of typed classes.
- Don't skip integration testing of the conversion logic.

*Ref: Building Event-driven Microservices.md — "Code Generator Support"*

---

### Data Liberation (Query / Log / Outbox / Triggers)

**Principle:** Four patterns liberate existing data into event streams: **query-based** (poll + publish), **CDC-log-based** (read replication log), **outbox tables** (transactional write to outbox + outbox poller), **trigger-based** (DB triggers). Pick by data store capability and SLA needs.

**Do:**
- Prefer CDC logs (binlog, WAL) where available — low latency, low source impact, captures deletes.
- Use outbox tables when you need atomic commit-with-the-business-write.
- Use query-based when there's no log/CDC option; bulk-load then incremental-update.
- Use the same standard schema format (Avro/Protobuf) for liberated and native data.

**Don't:**
- Don't use query-based if CDC exists — it adds load and misses hard deletes.
- Don't expose internal relational models directly — denormalize / eventify for downstream public-format.
- Don't skip *bootstrap* (initial snapshot) before streaming from logs.

*Ref: Building Event-driven Microservices.md — "Data Liberation Patterns"*

---

### Query-Based Liberation — Bulk + Timestamp + Autoinc + Custom

**Principle:** Query-based liberation can do **bulk** (initial), **incremental timestamp** (last updated_at), **autoinc ID** (strict monotonic), or **custom queries** (denormalize at the source). Always: bulk-load first, then incremental updates per poll interval.

**Do:**
- Add `updated_at` (and ideally `is_deleted` flag) if missing.
- Issue queries with sufficient interval to avoid races (old overwriting new).
- Customize queries to expose only the public-facing subset.

**Don't:**
- Don't start incremental updates without first doing a bulk load.
- Don't rely on hard deletions (they're invisible in polling queries).
- Don't expose internal data models — use views / projections to hide them.

*Ref: Building Event-driven Microservices.md — "Liberating Data by Query"*

---

### CDC Log Liberation (Debezium / Maxwell)

**Principle:** Read the database's binary log / write-ahead log to capture inserts, updates, deletes, and even DDL. **Debezium** is the leading cross-DB connector (MySQL, Postgres, MongoDB); **Maxwell** is MySQL-only.

**Do:**
- Use CDC for any DB with an available log stream.
- Bootstrap from a snapshot before streaming (with overlap).
- Checkpoint the log position for resumability.
- Decide which DDL changes to surface.

**Don't:**
- Don't expect CDC to handle all DDL changes — only some tools support DDL capture.
- Don't neglect idempotency (CDC is at-least-once).

*Ref: Building Event-driven Microservices.md — "Liberating Data Using Change-Data Capture Logs"*

---

### Outbox Tables — Atomic Business + Event Emission

**Principle:** Wrap business write + outbox-row insert in a single transaction. A separate process reads outbox rows, publishes to the event stream, deletes the outbox row on success. Provides at-least-once without distributed transactions.

**Do:**
- Bind outbox writes to the business transaction (single ACID commit).
- Use autoincrement ID for ordering; capture `created_at` for event time.
- Prefer a single, generic outbox (`serialized_key`, `serialized_value`, `output_stream`) when serialization happens before insert.
- Validate/serialize *before* insert for strongest consistency.

**Don't:**
- Don't allow business write without outbox insert (they must be atomic).
- Don't serialize after insert if schema enforcement matters — incompatible rows pile up.
- Don't expose internal data model — denormalize at outbox-write time.

**Code:**
| id (autoincrement) | created_at          | serialized_key | serialized_value | output_stream |
|--------------------|---------------------|----------------|------------------|---------------|
| 8273               | 2020-07-07T07:43:10 | A0 FB 24       | 0112 C5 BB D4    | Accounts      |
| 8274               | 2020-07-07T07:43:10 | DE A8 EF       | 25 6B EA F9 76   | Users         |

*Ref: Building Event-driven Microservices.md — "Liberating Data Using Outbox Tables"*

---

### Eventification (Denormalization Done Right)

**Principle:** Don't release 1:1 normalized streams into the public namespace — denormalize to a public-shape event (one User event containing location + employer) by writing a small processor over the normalized private streams.

**Do:**
- Use separate private + public namespaces; keep internal data model hidden.
- Materialize tables for User/Location/Employer so the join logic is reusable.
- Emit public events on the public namespace; isolate the private streams.

**Don't:**
- Don't expose normalized table-as-stream directly to consumers.
- Don't couple the public event to internal schema.

*Ref: Building Event-driven Microservices.md — "Isolating Internal Data Models"*

---

### Schema Enforcement: Before vs After the Outbox

**Principle:** Serializing **before** the outbox insert gives the strongest consistency guarantee — failure rolls back the transaction. Serializing **after** is cheaper but accumulates incompatible rows in the outbox that humans must reconcile.

**Do:**
- Default to before-the-fact serialization for data consistency.
- Accept the serialization cost as part of correctness.
- Single outbox with serialized bytes works well when serializing before insert.

**Don't:**
- Don't mix strategies — pick one and stick.
- Don't rely on after-the-fact validation when schema evolves frequently.

*Ref: Building Event-driven Microservices.md — "Ensuring Schema Compatibility"*

---

### Triggers — Last Resort for Legacy, Acceptable When Modern Isn't Available

**Principle:** Database triggers (AFTER INSERT/UPDATE/DELETE) can populate change-data tables, but they're brittle, schema-versioning-changes-easily-missed, and performance-overhead-heavy. Prefer CDC logs; reach for triggers only when nothing else exists.

**Do:**
- Use triggers when working with old RDBMS that lack CDC.
- Match the CDC table schema to the output event schema (so no after-the-fact transformation is needed).
- Test for trigger drift across schema changes.

**Don't:**
- Don't scale triggers to hundreds of tables.
- Don't forget to keep trigger logic in lockstep with application schema changes.

*Ref: Building Event-driven Microservices.md — "Capturing Change-Data Using Triggers"*

---

### DDL Changes — Detect Before vs After

**Principle:** Schema-liberation mechanisms differ in whether they detect DDL before or after. Query-based and CDC-log capture DDL *after* the fact (must validate); outbox-table is *before* the fact (validation rejects breaking changes at commit).

**Do:**
- Use CDC tables / outbox when you want breaking-change rejection early.
- Carefully version data-definition changes under capture.

**Don't:**
- Don't expect post-hoc tools to infer schema changes — they often can't.
- Don't drop non-nullable columns without a default on a stream whose consumers use the old schema.

*Ref: Building Event-driven Microservices.md — "Handling After-the-Fact Data Definition Changes"*

---

### Sinking Events Downstream (Back to Legacy Stores)

**Principle:** Some applications can't consume from event streams (legacy, tooling). Use a sink — a process that reads the stream and writes to the destination store. A common pattern for integrating without rewriting.

**Do:**
- Sink to legacy / search indexes / big-data lakes via standalone services or Kafka Connect.
- Document the sink's coupling; treat as one-way data flow.
- Use Kafka Connect / Flink SQL / NiFi for managed sinks.

**Don't:**
- Don't let sinks silently diverge from the source-of-truth stream.
- Don't bypass event validation when sinking — events should still pass the schema.

*Ref: Building Event-driven Microservices.md — "Sinking Event Data to Data Stores"*

---

### CDC Frameworks Aren't the Destination

**Principle:** CDC framework/connector usage is good for *bootstrap*, not as a final destination. The end-game is native event publication by the owning service. Otherwise you create cross-team coupling and miss the "event-first" mindset shift.

**Do:**
- Use CDC for legacy bootstrapping.
- Migrate producers to outbox-pattern event publication over time.
- Acknowledge that CDC connectors couple teams (stability, schema, rate-limiting) — minimize that footprint.

**Don't:**
- Don't treat CDC as a permanent solution — it's a transitional mechanism.
- Don't let CDC's ease of use discourage migration to first-party event publication.

**Code:**
> "CDC tools are *not* the final destination in moving to an event-driven architecture, but instead are primarily meant to help bootstrap the process. The real value of the event broker as the data communication layer is in providing a robust, reliable, and truthful source of event data decoupled from the implementation layers, and the broker is only as good as the quality and reliability of its data."

*Ref: Building Event-driven Microservices.md — "The Impacts of Sinking and Sourcing on a Business"*

---

### Stateless Event-Driven Processing (Transformations)

**Principle:** A stateless topology consumes, applies filter / map / mapValue / custom transformations, and produces. Each event is processed independently. Operations are simple data-driven pipelines.

**Do:**
- Compose transformations: `filter`, `map` (changes key+value), `mapValue` (changes value only), `custom` (synchronous side-lookups, third-party calls).
- Use `map` only when a key change is intentional (signals a repartition).
- Use `mapValue` when partition locality should be preserved.

**Don't:**
- Don't use `map` to change keys without considering repartition impact.

*Ref: Building Event-driven Microservices.md — "Composing Stateless Topologies"*

---

### Branching, Merging, Repartitioning

**Principle:** Branching: emit events to different streams based on a logical operator (e.g., country, dead-letter). Merging: combine multiple streams into one — but only with a well-defined unified schema. Repartitioning: produce a new stream with new key/partitions.

**Do:**
- Branch for routing (cleanly); for failures, prefer DLQ over dropping.
- Repartition when changing keys or matching partition count of another stream.
- Define a unified schema before merging.

**Don't:**
- Don't merge streams without a unified schema.
- Don't repartition more than necessary.

*Ref: Building Event-driven Microservices.md — "Branching and Merging Streams"*

---

### Copartitioning for Joins

**Principle:** Two keyed event streams must be **copartitioned** (same partition count, same partitioner, same key) to be joined on key. This is the keystone of stream-table joins and stream-stream joins in distributed processing.

**Do:**
- Verify event streams have equal partition counts before joining (fail fast if not).
- Use copartitioned streams for any keyed join to guarantee locality.
- Treat copartitioning as a contract between producer and join-consumer.

**Don't:**
- Don't join streams on key without verifying copartitioning — performance will die.
- Don't repartition mid-pipeline without documenting the dependency.

*Ref: Building Event-driven Microservices.md — "Copartitioning Event Streams"*

---

### Partition Assignment Strategies (Round-Robin / Static / Custom)

**Principle:** Brokers/clients pick a partition assignor. Defaults are often round-robin (good for elasticity), static (good for large materialized state per partition), custom (lag-based or other signals).

**Do:**
- Use round-robin for most elastic workloads.
- Use static when state size would make rebalance too costly.
- Use custom assignors when lag-driven scaling requires it.

**Don't:**
- Don't rebalance a static assignor unnecessarily.
- Don't ignore copartitioned partition assignment constraints in your assignor.

*Ref: Building Event-driven Microservices.md — "Partition Assignment Strategies"*

---

### Deterministic Stream Processing — Time and Ordering

**Principle:** Event time (producer-assigned), ingestion time (broker-stamped), processing time (consumer wall-clock) are different. Use event time for business ordering. Custom schedulers may break determinism — be careful.

**Do:**
- Use event time for business-ordering decisions.
- Synchronize clocks with NTP (sufficient for most cases).
- Document any nondeterministic logic (wall-clock, external system calls).

**Don't:**
- Don't mix the time semantics; pick and document.
- Don't assume NTP accuracy is enough for fine-grained ordering across regions.

*Ref: Building Event-driven Microservices.md — "Timestamps" and "Synchronizing Distributed Timestamps"*

---

### Event Scheduling — Order Across Multiple Partitions

**Principle:** When consuming from multiple partitions, scheduling picks the event with the oldest timestamp first. Default: ascending event-time from all assigned input partitions. Custom schedulers (e.g., Apache Samza `MessageChooser`) must still produce reproducible results.

**Do:**
- Implement event-scheduling when processing order matters across streams.
- Keep schedulers deterministic if you may reprocess.
- Document any prioritization logic.

**Don't:**
- Don't write a custom scheduler that depends on wall-clock or external state if you may ever need to reprocess.

*Ref: Building Event-driven Microservices.md — "Event Scheduling and Deterministic Processing"*

---

### Watermarks vs Stream Time — Two Models for "Done"

**Principle:** **Watermarks** (Spark/Flink/Beam): declaratively close windows; downstream nodes track min(input event times). **Stream time** (Kafka Streams): monotonic high-watermark per subtopology; one-event-at-a-time depth-first. Both track progress; choose based on framework.

**Do:**
- Use watermark-based frameworks when windowing patterns dominate.
- Use stream-time frameworks (Kafka Streams) for simplicity + single-event-at-a-time semantics.
- Document which model your team uses.

**Don't:**
- Don't mix watermark and stream-time mental models.

*Ref: Building Event-driven Microservices.md — "Watermarks" and "Stream Time"*

---

### Out-of-Order and Late-Arriving Events

**Principle:** Out-of-order events are normal in distributed systems (producer retries, network delays, broker outages). Each consumer must define what's "late" relative to its deadline.

**Do:**
- Use event-time windows with a tunable grace period.
- Document the late-event strategy (drop, wait, grace, replay).
- For critical data (financial): keep state for a grace window.
- For measurement-style: drop after window close.

**Don't:**
- Don't rely on offset order across partitions.
- Don't wait indefinitely — eventually you must commit.
- Don't assume single-producer = in-order across regions.

**Code:**
> "An event is late only when it has missed a deadline specific to the consumer. … Eventually the service will need to give up, as it cannot wait indefinitely. Other factors to consider include how much state to store, the likelihood of late events, and the business impact of not using the late events."

*Ref: Building Event-driven Microservices.md — "Out-of-Order and Late-Arriving Events"*

---

### Windowing: Tumbling / Sliding / Session

**Principle:** Three window types cover most use cases. **Tumbling** (fixed, no overlap) for "peak hour"-style queries. **Sliding** (fixed size, sliding step) for "users active in past hour"-style. **Session** (inactivity-driven) for "user browsing session"-style.

**Do:**
- Use tumbling for periodic aggregations (per-minute, per-hour).
- Use sliding for "rolling" metrics.
- Use session for behavior-period analytics.
- Configure a sensible gap for session windows.

**Don't:**
- Don't keep state for windows longer than business value warrants — it bloats storage.

*Ref: Building Event-driven Microservices.md — "Time-Sensitive Functions and Windowing"*

---

### Reprocessing — Rewind and Replay

**Principle:** Reprocessing is the keystone value of immutable logs. Reset consumer offsets to a past point and let the consumer re-process. Some downstream effects (e.g., "send shipping email") must NOT be re-triggered.

**Do:**
- Set start point to beginning of each entity stream.
- Scale consumer parallelism to maximum for fast catch-up.
- Make business logic re-trigger-safe (idempotent) where replay must be visible downstream.
- For business logic with side effects, gate those effects on whether the input event is freshly seen (dedupe or "replay" flag).

**Don't:**
- Don't re-trigger side effects (emails, charges) on a casual reprocess — segment production from replay.
- Don't skip downstream-consumer notification when reprocessing will produce many events.

**Code:**
> "Some microservices perform actions that you may not want to occur when reprocessing. For instance, a service that emails users when their packages have shipped should *not* re-email users when reprocessing events, as it would be a terrible user experience and completely nonsensical from a business perspective."

*Ref: Building Event-driven Microservices.md — "Reprocessing Versus Processing in Near-Real Time"*

---

### Stateful Streaming — Changelogs and Materialization

**Principle:** Internal-state backing comes with a **changelog** (a stream of all state changes) so a recovering instance can rebuild. Changelogs are compacted streams. Recovery is identical to scaling.

**Do:**
- Use changelogs for internal state stores (RocksDB-class).
- Use changelogs as compacted streams.
- Treat recovery = scaling (same rebalance logic).
- Load changelog fully before processing new events.

**Don't:**
- Don't process new events while loading state — produces nondeterministic results.

*Ref: Building Event-driven Microservices.md — "Recording State to a Changelog Event Stream"*

---

### Internal vs External State — When to Pick Which

**Principle:** **Internal** (RocksDB on local SSD): ultra-fast but locked to the runtime. **External** (any DB): flexible, less performant, costly at scale. Pick internal for hot-state; external for less-critical or relational state.

**Do:**
- Use internal state for hot tables (joins, aggregations, deduplication).
- Use external state for less-time-critical lookups, relational queries, full-text search, geospatial.
- Use external state when you need to share or back up data outside the framework.

**Don't:**
- Don't put internal state on network-attached disk (latency kills throughput).
- Don't share external state between microservice instances — defeats the decoupling.

*Ref: Building Event-driven Microservices.md — "Materializing State to an Internal State Store" and "Materializing State to an External State Store"*

---

### Hot Replicas for Stateful Failover

**Principle:** Maintain N copies of internal state per partition (typically 2). On failover, the partition is reassigned to whichever instance already holds the up-to-date copy. Drop the original; build a new replica.

**Do:**
- Use hot replicas to fail-over with zero downtime (where supported).
- Configure based on framework (Kafka Streams has this built in).
- Trade off disk cost for failure recovery speed.

**Don't:**
- Don't rely on hot replicas without monitoring staleness.
- Don't forget to build new hot replicas after a failover.

*Ref: Building Event-driven Microservices.md — "Scaling and Recovery of Internal State"*

---

### Transactions — Effectively Once / Exactly Once

**Principle:** **Effectively-once** processing guarantees that updates to the source of truth are consistent regardless of failure, even though the *processing logic* may run more than once. Enable via **idempotent writes** + **broker transactions** (Kafka) wrapping output events + state changes (in changelogs) + offset updates.

**Do:**
- Use idempotent produces (Kafka / Pulsar) when available.
- Wrap output events + offset updates + state changes in a single atomic transaction where supported.
- Use deterministic logic wherever the framework relies on it.

**Don't:**
- Don't depend on wall-clock or external side-effects for deterministic bookkeeping.
- Don't try to "guarantee exactly once" for non-transactional brokers by guesswork — use a dedupe store.

**Code:**
> "In the case of permanent failure by the producer, the broker will ensure that none of the events in the transaction is committed. Event stream consumers typically abstain from processing events that are in uncommitted transactions."

*Ref: Building Event-driven Microservices.md — "Effectively Once Processing with Client-Broker Transactions"*

---

### Effectively-Once Without Broker Transactions

**Principle:** When transactions aren't supported, do your own at-least-once — idem-produce, dedupe consumption (id store), and store offsets alongside state in a single DB transaction for consistency.

**Do:**
- Use a dedupe-ID store scoped to a TTL (not forever).
- Pair the dedup store with a single key+partition scope.
- Handle producer retries and producer-crashes (both generate duplicates).

**Don't:**
- Don't expect dedupe to work across partitions (it's prohibitively expensive).
- Don't keep dedupe IDs forever — bound by TTL or max-size.

*Ref: Building Event-driven Microservices.md — "Effectively Once Processing Without Client-Broker Transactions"*

---

### Choreography vs Orchestration (Workflows)

**Principle:** **Choreography** (reactive / no central controller): services emit/consume events independently. **Orchestration** (single conductor): a central service directs workers and tracks state. Each has tradeoffs.

**Do:**
- Choose **choreography** for loose coupling, low coordination overhead, small workflows.
- Choose **orchestration** for complex workflows, visibility, timeouts, human inputs, monitorability.
- Mix and match carefully — document each chosen flow.

**Don't:**
- Don't try to make a single "God orchestrator" that knows everything.
- Don't split orchestration across multiple services.
- Don't expect choreography to provide free monitoring — materialize state from each event stream.

**Code (orchestration):**
```
while (true) {
 Event[] events = consumer.consume(streams)
 for (Event event : events) {
  if (event.source == "Input Stream") {
   //process event + update materialized state
   producer.send("Stream 1", ...)
  } else if (event.source == "Stream 1-Response") {
   producer.send("Stream 2", ...)
  } else if (event.source == "Stream 2-Response") {
   producer.send("Stream 3", ...)
  } else if (event.source == "Stream 3-Response") {
   producer.send("Output", ...)
  }
 }
 consumer.commitOffsets()
}
```

*Ref: Building Event-driven Microservices.md — "Building Workflows with Microservices"*

---

### Sagas — Distributed Transactions with Reversal

**Principle:** Distributed transactions in event-driven systems = **sagas**. Each participating service has a forward and reversal action, both idempotent. Failure of any step triggers ordered rollbacks.

**Do:**
- Implement each service with both processing *and* reversal actions.
- Make every action idempotent.
- Use choreography for simple, stable-order sagas; orchestration for visibility/transparency.
- Use timeouts at the orchestrator to detect stuck transactions.

**Don't:**
- Don't put reversal logic in a separate service — each service owns its own compensating action.
- Don't assume rollback is free — limit saga complexity to what's necessary.

*Ref: Building Event-driven Microservices.md — "Distributed Transactions"*

---

### Compensation Workflows When Strict Rollback Is Wrong

**Principle:** Not every workflow needs strict transactional reversal. Customer-facing flows often benefit from *compensation* (offering a discount, shipping later) rather than immediate rollback.

**Do:**
- Use compensation workflows for retail/ticketing scenarios where users are involved.
- Make compensations easy to implement; don't try to make strict transactions work where they hurt UX.

**Don't:**
- Don't force rollback-based sagas when compensation is more humane (or profitable).

*Ref: Building Event-driven Microservices.md — "Compensation Workflows"*

---

### FaaS Microservice Design (Strict Bounded Context, Offset Discipline)

**Principle:** A FaaS service is a basic producer-consumer that *regularly fails*. Strict bounded-context membership + commit-after-processing semantics matter. Fewer functions = better.

**Do:**
- Keep functions strictly within one bounded context.
- Commit offsets *after* processing (not before) for at-least-once.
- Prefer fewer functions over many granular ones — easier to debug.
- Treat cold starts as a fact of life.

**Don't:**
- Don't commit offsets at function start (data loss is likely on retry failure).
- Don't write shared helper functions used across bounded contexts (couples them).

*Ref: Building Event-driven Microservices.md — "Designing Function-Based Solutions as Microservices"*

---

### FaaS Triggers: New Events, Lag, Schedule, Webhook, Resource

**Principle:** Functions trigger via: **on-new-event** (stream-listener), **on-consumer-lag** (poll lag then start function), **on-schedule** (cron), **on-webhook** (HTTP), **on-resource-event** (file/blob changes).

**Do:**
- Pick on-new-event for typical stream processing.
- Use on-lag for event-driven *scaling* (and for non-FaaS services too).
- Tune batch size and batch window to amortize startup cost.
- Use synchronous triggers when ordering matters; asynchronous only for fire-and-forget.

**Don't:**
- Don't use on-new-event when order matters but you've turned on async.
- Don't fire on-webhook without rate limits.

*Ref: Building Event-driven Microservices.md — "Starting Functions with Triggers"*

---

### FaaS Scaling — Hysteresis and Re-Thrashing Avoidance

**Principle:** Aggressive FaaS scaling with high churn causes consumer-group thrashing. Use **hysteresis** (cool-down) and step-based scaling to avoid the loop.

**Do:**
- Add a tolerance band (don't scale up/down on tiny lag deltas).
- Use static partition assignment where viable (no rebalance churn).

**Don't:**
- Don't use aggressive scale-up-and-down policies that thrash consumer groups.

*Ref: Building Event-driven Microservices.md — "Scaling Your FaaS Solutions"*

---

### BPC (Basic Producer/Consumer) — When It's the Right Choice

**Principle:** BPC microservices use bare consumer/producer clients; they have no event scheduling, watermarks, materialization, changelogs. They excel at: integration with legacy (incl. sidecar), gating/order-insensitive stateful logic, when the data layer does the work.

**Do:**
- Use BPC for legacy integration and sidecar patterns.
- Use BPC for gating logic where order doesn't matter but all events must arrive.
- Use BPC when a fully-managed data layer (geo, search, ML) does the heavy lifting.

**Don't:**
- Don't try to implement deterministic streaming with BPC without writing your own scheduling library.

*Ref: Building Event-driven Microservices.md — "Basic Producer and Consumer Microservices"*

---

### Sidecar Pattern for Legacy Without Code Changes

**Principle:** When you can't modify a legacy app, attach a sidecar (its own container, part of the same deployable) that does event-stream I/O. The legacy app continues to read/write its own DB; the sidecar mirrors state through events.

**Do:**
- Co-locate sidecar with the legacy app in a single deployable.
- Test sidecar together with the legacy app.
- Use sidecars to bootstrap legacy into event-driven without invasive changes.

**Don't:**
- Don't put sidecar in a separate deployment lifecycle (breaks testability).
- Don't rely on sidecars for *primary* event sourcing — use first-class publishers.

*Ref: Building Event-driven Microservices.md — "Example: Sidecar pattern"*

---

### Heavyweight Frameworks (Spark / Flink / Storm / Heron / Beam)

**Principle:** Heavyweight frameworks (Spark, Flink, Storm, Heron, Beam) require a separate cluster; they dominate analytical workloads but have weaker microservice ergonomics. Pick when: large ETL, session/window analytics, anomaly detection, bulk aggregations.

**Do:**
- Use heavyweight frameworks for established big-data / batch workloads.
- Use Kubernetes-native mode (Flink session cluster on K8s, Spark on K8s) for microservice-like isolation per job.
- Use Beam API for portability across runners.

**Don't:**
- Don't use heavyweight framework when a lightweight or BPC would do.
- Don't assume autoscaling — most heavyweight frameworks lack it; use manual scaling or external metrics.

*Ref: Building Event-driven Microservices.md — "Heavyweight Framework Microservices"*

---

### Checkpoints for Heavyweight Frameworks

**Principle:** A checkpoint is a snapshot of internal state, persisted externally (HDFS, durable storage). Checkpoints persist operator state (partitionId → offset) and key state (key → value). On failure or scaling, the framework restores from the latest checkpoint.

**Do:**
- Persist checkpoints durably (external to worker nodes).
- Synchronize operator and key state in a single checkpoint.
- Test restore behavior on every deploy.

**Don't:**
- Don't checkpoint only key state or only offsets — they must agree.
- Don't lose checkpoints on worker failure.

*Ref: Building Event-driven Microservices.md — "Handling State and Using Checkpoints"*

---

### Heavyweight Scaling — In-Place vs Restart

**Principle:** Scaling can be **in-place** (Spark dynamic resource allocation with External Shuffle Service) or by **restarting** (Flink REST, Storm rebalance). Restart is universally supported; in-place is faster but framework-specific.

**Do:**
- Prefer restart-scaling for guaranteed correctness.
- Use in-place scaling only with an External Shuffle Service for shuffle data.

**Don't:**
- Don't auto-scale heavyweight cluster sizes without understanding framework support.
- Don't let multiple instances simultaneously occupy partitions.

*Ref: Building Event-driven Microservices.md — "Scaling Applications and Handling Event Stream Partitions"*

---

### Lightweight Frameworks (Kafka Streams / Samza Embedded)

**Principle:** Lightweight frameworks (Kafka Streams, Samza embedded) leverage the broker + CMS to provide stream processing without a dedicated cluster. They shine for materializing tables and stream-stream joins inside JVM microservices.

**Do:**
- Use Kafka Streams for indefinite retention of materialized tables; primary-key and foreign-key joins.
- Use Samza embedded when its specific runtime fits.
- Lean on internal event streams + changelogs (broker-built durability).

**Don't:**
- Don't reuse a heavyweight cluster when a lightweight framework would do.
- Don't assume lightweight frameworks are portable across brokers (Kafka Streams requires Kafka).

*Ref: Building Event-driven Microservices.md — "Lightweight Framework Microservices"*

---

### Stream-Table-Table Joins (Enrichment Pattern)

**Principle:** Lightweight frameworks make stream-table-table joins easy: a stream of click events enriched by a table of users and a table of companies — copartitioned on the join key.

**Do:**
- Repartition the stream to match the table's partition count.
- Apply the join via framework DSL.
- Compute tombstones for null inputs (foreign-key join semantics).

**Don't:**
- Don't join without copartitioning — the framework can't guarantee locality.

**Code:**
```
KStream<WindowKey,Actions> userSessions = ...
KTable<AdvertisementId,Long> conversions = userSessions
 .transform(...)
 .groupByKey()
 .aggregate(...)
KTable<AdvertisementId,Advertisement> advertisements = ...
conversions
 .join(advertisements, joinFunc)
 .to("AdvertisementEngagements")
```

**SQL equivalent:**
```
SELECT adConversionSumTable.sum, adTable.name, adTable.type
FROM adConversionSumTable FULL OUTER JOIN adTable
ON adConversionSumTable.id = adTable.id
```

*Ref: Building Event-driven Microservices.md — "Stream-Table-Table Join: Enrichment Pattern"*

---

### Request-Response Integration Patterns

**Principle:** Three patterns integrate EDM with HTTP APIs: **autonomously generated analytical events** (mobile → ingest endpoint), **reactively generated events** (service calls API, parses response into event), and **event-driven microservice hosting a REST endpoint** (serving from internal/external state).

**Do:**
- Parse external API responses into typed events; validate schema at the consumer.
- Treat external calls as nondeterministic (don't rely on them in reprocessing).
- Use quotas to throttle when reprocessing could overload third-party APIs.

**Don't:**
- Don't put confidential PII in events without explicit consent/regulation governance.
- Don't trust third-party API responses as ground truth — they're "snapshots."

*Ref: Building Event-driven Microservices.md — "Integrating Event-Driven and Request-Response Microservices"*

---

### Serving State for Read APIs (Internal vs External Stores)

**Principle:** When serving from **internal** state: the request must route to the instance holding the data (partition locality; smart load balancer optional). When serving from **external** state: any instance can serve (no routing needed).

**Do:**
- Use internal state + smart load balancer for tight latency SLAs (no extra hop).
- Use external state for simpler scaling, fewer cross-instance hops, simpler failover.
- Use the *composite service* pattern (single bounded context; separate event processor + request-responder executables) when language/runtime needs differ.

**Don't:**
- Don't expose the external state store directly to consumers — go through the bounded-context API.

*Ref: Building Event-driven Microservices.md — "Processing and Serving Stateful Data"*

---

### Microfrontends Composability

**Principle:** Microfrontends are frontend components aligned to bounded contexts. Pair with event-driven microservice backends: each microfrontend is the UI for one microservice. Use a compositional layer to stitch them.

**Do:**
- Align microfrontends by business context (matching backend services).
- Provide a strict style-guide / shared UI element library to avoid inconsistency.
- Treat common UI library changes as cross-team changes (with stewardship).

**Don't:**
- Don't have each microfrontend reinvent design.
- Don't expect microfrontends to behave identically under failure — design for partial degradation.

*Ref: Building Event-driven Microservices.md — "Micro-Frontends in Request-Response Applications"*

---

### Asynchronous UI Patterns

**Principle:** Convert requests to events; surface "request received, processing" UI; commit/aggregate updates later. Set user expectations.

**Do:**
- Show spinners / disable actions during async processing.
- Update the UI when materialization completes (not when the request hits the service).
- Manage user expectations with clear visual cues.

**Don't:**
- Don't leave users wondering what happened after a click.

*Ref: Building Event-driven Microservices.md — "Processing Events for User Interfaces"*

---

### Microservice-to-Team Assignment + Stream Metadata Tagging

**Principle:** A central system tracks who owns what (services, streams). Streams are tagged with metadata (owner, PII, financial, namespace, deprecated). Permissions are granted based on ownership.

**Do:**
- Tag streams with owner, PII flag, financial flag, namespace, deprecation status.
- Use ACLs (READ/CREATE/WRITE/DELETE/MODIFY/DESCRIBE) to enforce boundaries.
- Grant consumer access per-microservice, not per-user.
- Audit orphaned streams/services (no consumers).

**Don't:**
- Don't let teams self-report dependencies — use ACL-recorded access patterns.
- Don't grant WRITE without explicit "single writer" justification.

*Ref: Building Event-driven Microservices.md — "Supportive Tooling"*

---

### Schema Registry and Notification Stream

**Principle:** A schema registry catalogs schemas for each stream; producers register and get IDs; consumers fetch via ID. A schema changelog stream notifies consumers of changes.

**Do:**
- Run a schema registry (Confluent Schema Registry or compatible).
- Track schema IDs in events (or storage layer) for size efficiency.
- Notify downstream consumers when compatible (or breaking) schema changes are published.

**Don't:**
- Don't embed full schema in each event — use IDs.
- Don't change a schema without coordinating with consumers.

*Ref: Building Event-driven Microservices.md — "Schema Registry"*

---

### Offset Management & Quotas

**Principle:** Operators must be able to reset offsets (rewind, advance, set to time-N-minutes-ago). Quotas prevent noisy neighbors from starving the cluster.

**Do:**
- Offer self-service offset tools to microservice owners.
- Set quotas at universal and per-team levels; tune for spiky producers.
- Track replication-tool behavior: offset/partition/timestamp parity, latency, scalability.

**Don't:**
- Don't let one service consume 90% of cluster I/O.
- Don't grant other teams the ability to reset your offsets.

*Ref: Building Event-driven Microservices.md — "Offset Management" and "Quotas"*

---

### Consumer Lag = Scale Trigger

**Principle:** Lag (head offset − consumer group offset) signals "behind." Use a lag monitor to scale consumers up/down. Use historical deviation (e.g., Burrow for Kafka) to avoid reacting to "natural" lag at high-volume streams.

**Do:**
- Define lag thresholds per microservice.
- Use hysteresis (cool-down) to prevent thrashing.
- Use deviation-from-history for high-volume streams that "always look lagging."

**Don't:**
- Don't use a single threshold without hysteresis (oscillation kills the cluster).

*Ref: Building Event-driven Microservices.md — "Consumer Offset Lag Monitoring"*

---

### Streamlined Microservice Creation

**Principle:** Standardize the bring-up flow: repo → CI integration → webhooks → team assignment → access permissions → output streams → template/skeleton. Automation removes tribal knowledge.

**Do:**
- Wire CI/CD to pull latest templates.
- Bake schema/stream conventions into the skeleton.
- Make ownership-transfer and ACLs a one-step operation.

**Don't:**
- Don't let each new service reimplement its own bring-up.

*Ref: Building Event-driven Microservices.md — "Streamlined Microservice Creation Process"*

---

### Topology Visualization and Cross-Boundary Connections

**Principle:** Visualize data lineage (event-stream graph). Track streams + owners + permissions graph. Measure cross-boundary connections; minimize them.

**Do:**
- Build a topology graph based on ACLs (auto-generated from permissions).
- Track each team's incoming/outgoing stream counts and cross-team connections.
- Use the topology to reassign services to reduce cross-boundary coupling.

**Don't:**
- Don't rely on self-reported dependencies (always under-reported).
- Don't ship topology changes without team-affected review.

*Ref: Building Event-driven Microservices.md — "Dependency Tracking and Topology Visualization"*

---

### Testing — General Principles

**Principle:** Test modularly: unit test transformation/reduction functions; topology-test the framework wiring; integration-test with real or mocked brokers; schema-evolution-test; load/stress/recovery-test.

**Do:**
- Test boundary conditions (nulls, max values).
- Use framework-provided topology-test utilities (Spark `MemoryStream`, Flink topology test, Kafka Streams `TopologyTestDriver`).
- Cover schema evolution compatibility as part of CI.

**Don't:**
- Don't skip integration tests because "tests pass locally" — isolated tests miss framework/event-broker interaction bugs.
- Don't test on shared prod-cluster — use disposable environments.

*Ref: Building Event-driven Microservices.md — "Testing Event-Driven Microservices"*

---

### Integration Testing Strategies (Local vs Remote)

**Principle:** Test in **local** (in-runtime or containerized), **fully remote** (temp cluster), **shared environment** (low-overhead but tragic-commons), or **production** (smoke only). Disposable, isolated environments are best.

**Do:**
- Default to disposable / programmatic environments.
- Use production data copies *only* if you have replication tools and access controls.
- For performance tests, run in fully remote (production-like) environments.
- Never run performance/load tests against prod.

**Don't:**
- Don't be the "shared testing cluster" — orphaned data, accidental coupling, slow signal.
- Don't copy production data through inadequate security controls.

*Ref: Building Event-driven Microservices.md — "Integration Testing of Event-Driven Microservices"*

---

### Deploying — Base Principles

**Principle:** Microservice teams have deployment autonomy; deployment is standardized; tooling is provided; reprocessing impact is considered; SLAs respected; dependent changes minimized; breaking changes negotiated.

**Do:**
- Give each team full deployment autonomy for their bounded context.
- Document SLA + reprocessing impact of every deploy.
- Negotiate breaking changes with downstream consumers before deploying.

**Don't:**
- Don't make deployments require manual work across teams.
- Don't introduce tight cross-team deploy dependencies (anti-pattern: indicates ill-defined contexts).

*Ref: Building Event-driven Microservices.md — "Principles of Microservice Deployment"*

---

### Deployment Patterns — Full-Stop, Rolling, Breaking-Schema, Blue-Green

**Principle:** Four patterns: **basic full-stop** (halt, redeploy; default), **rolling update** (one instance at a time; safe only if no state/topology/schema break), **breaking schema** (two-stream or sync migration), **blue-green** (parallel run; switch traffic; great for read-only / event-from-API sources; NOT good for event-producing services).

**Do:**
- Use rolling updates when state, topology, and schemas are unchanged.
- Use eventual two-stream migration when producers can emit both formats.
- Use blue-green when the service generates events only from request-response (no event-stream input).
- Roll forward or rollback, but ensure the path is documented and tested.

**Don't:**
- Don't change the topology under a rolling update (breaks processor assumptions).
- Don't try blue-green on a service with input-event-stream-driven output (duplicate or overwritten events).

**Code (blue-green caveat):**
> "Blue-green deployments *do not work* when the microservice produces events to an output stream in reaction to an input event stream. The two microservices will overwrite each other's results in the case of entity streams or will create duplicated events in the case of event streams."

*Ref: Building Event-driven Microservices.md — "Deploying Event-Driven Microservices"*

---

### Multitenancy and Namespaces in Heavyweight Clusters

**Principle:** Heavyweight clusters need tenant isolation to prevent starvation. Use **per-team clusters** (high cost, simple) or **namespaces with resource quotas** (cost-effective, fragmentation risk).

**Do:**
- Use namespaces with resource quotas for stable multitenant workloads.
- Use per-team clusters for very large or contentious workloads.

**Don't:**
- Don't share one cluster with no quotas — first big workload starves everyone.

*Ref: Building Event-driven Microservices.md — "Multitenancy Considerations"*

---

### Microservices Need Common Artifacts and Skills

**Principle:** Pay the **microservice tax** deliberately: event broker, schema registry, CMS, CI/CD, monitoring/logging. These are non-negotiable foundations.

**Do:**
- Build the essential platform artifacts before scaling microservices widely.
- Outsource where it makes sense (Confluent Cloud, Datadog, etc.).

**Don't:**
- Don't scale microservices beyond the platform's ability to support them.

*Ref: Building Event-driven Microservices.md — "Shareable Tools and Infrastructure"*

---

### CDC Pattern Selection Heuristic (Query vs Log vs Outbox vs Trigger)

**Principle:** Each liberation pattern optimizes for a different constraint — pick by data-store capability, latency, multi-tenancy constraints, and team capability.

**Decision matrix:**

| Pattern | Latency | Hard Deletes | Schema Validation | Data Store Coverage | Required Code Changes |
|---|---|---|---|---|---|
| **Query** | High (poll interval) | Soft only | At query time | Universal | None |
| **CDC Log** | Low (sub-second) | Yes | Generally after-the-fact | Limited to RDBMS with logs | None |
| **Outbox Table** | Tunable | Yes | Before-the-fact | Universal transactional | Required (modify app) |
| **Trigger** | Low | Yes | Mostly after-the-fact | Most RDBMS | Required |

**Do:**
- Use **CDC log** when the source DB has a binary/WAL log (MySQL binlog, Postgres WAL, MongoDB change streams).
- Use **outbox** when you control the application AND want atomicity AND can tolerate a slight DB performance hit.
- Use **query** when neither above is available and the data set fits comfortably.
- Use **trigger** for legacy systems where code modification is impossible.

**Don't:**
- Don't pick a pattern that exposes the internal data model.
- Don't pick a pattern that misses hard deletes if your business cares.
- Don't trigger where a CDC log exists.

*Ref: Building Event-driven Microservices.md — "Data Liberation Patterns"*

---

### Pre-/Post-Fact Schema Validation Tradeoff

**Principle:** Pre-fact (before outbox insert) gives data consistency at the cost of transaction failure. Post-fact (after outbox insert) gives throughput at the cost of mismatched rows requiring manual reconciliation.

**Do:**
- Default to pre-fact validation for first-class event streams; the cost of failing the transaction is small relative to the cost of corrupt data downstream.
- Switch to post-fact only for high-volume, high-throughput legacy liberation with stable schemas.
- Always keep the serialize-before outbox pattern when correctness matters more than micro-perf.

**Don't:**
- Don't mix pre/post within one event type — pick a strategy and stick.
- Don't pick post-fact if you're going to skip human reconciliation — incompatible rows pile up indefinitely.

*Ref: Building Event-driven Microservices.md — "Ensuring Schema Compatibility"*

---

### Micro-Batch Polling Patterns

**Principle:** Query-based liberation uses two phases: **bulk load** (initial), then **incremental updates** (poll interval). Race conditions arise when incremental-update queries overlap with previous batches — tune poll interval to be larger than expected query runtime.

**Do:**
- Bulk-load every full table at the start; then poll incrementally.
- Use a field that monotonically identifies newness (`updated_at`, autoincrement id).
- Set the polling interval greater than the worst-case query duration.
- Bulk-load again after a long downtime (capture missed rows).

**Don't:**
- Don't start incremental updates before the bulk load completes.
- Don't run overlapping polls that could overwrite newer rows with stale older rows.

*Ref: Building Event-driven Microservices.md — "Bulk Loading", "Incremental Timestamp Loading"*

---

### Data Liberation Anti-Pattern: Cross-Stream Brittle Coupling

**Principle:** Brittle dependencies between the source app and the connector (schema, query, throughput) are an anti-pattern. Producers should aim for first-party event publication; connectors should be a transition tool only.

**Do:**
- Document the connector's dependencies on app schema/query — keep them small and stable.
- Migrate high-volume / high-criticality streams to native publication (outbox) ASAP.
- Treat connector breakage as a signal to migrate, not as a "fix the connector" task.

**Don't:**
- Don't pile more and more connectors onto a centralized framework team.
- Don't let connector operations out-evolve event-first culture (it should reduce over time).

*Ref: Building Event-driven Microservices.md — "The Impacts of Sinking and Sourcing on a Business"*

---

### FaaS Function-Trigger Map (Internal Decoupling)

**Principle:** Define a function-trigger map: function ↔ event stream(s) ↔ trigger type ↔ policies + metadata. Centralize the metadata to surface scaling, retry, and consumer-group policy.

**Do:**
- Define the function-trigger map in tooling, not source code.
- Treat each FaaS-implementation microservice as its own bounded context with its own consumer group.
- Persist the trigger map for inspection (and/or generate code from it).

**Don't:**
- Don't reuse function code across bounded contexts; share semantics at the schema level, not at the code level.

**Code:**
| Function    | Event stream(s) | Trigger    | Policies and metadata |
|-------------|-----------------|------------|-----------------------|
| myFunction  | myInputStream   | onNewEvent | < … >                 |

*Ref: Building Event-driven Microservices.md — "Building Microservices Out of Functions"*

---

### FaaS Cold vs Warm Starts

**Principle:** Cold starts cost non-trivial work (container bootstrap, broker connection, external resource handshake). Warm keeps connections intact. FaaS frameworks *try* to reuse warm instances — but you cannot rely on it.

**Do:**
- Treat each function invocation as potentially cold — design for it.
- Take advantage of warm starts (e.g., reduce reconnect cost).
- Measure cold-start latency against your SLA budget.

**Don't:**
- Don't persist critical state in a function's memory assuming warm-start.
- Don't depend on broker connection surviving across invocations.

*Ref: Building Event-driven Microservices.md — "Cold Start and Warm Starts"*

---

### FaaS Stateful Functions — Use External Stores

**Principle:** FaaS has short lifespans; local state is ephemeral. Most stateful FaaS needs external stateful services (DBs, durable caches, event-sourced state from the broker itself).

**Do:**
- Use external state stores for any durable FaaS state.
- Use **durable functions** (Azure Durable Functions, etc.) where the platform abstracts state.
- Lean on the broker's event streams as your state (write events; rebuild from there).

**Don't:**
- Don't keep state in function-local memory — it's not durable.
- Don't rely on warm-start guarantees for state.

*Ref: Building Event-driven Microservices.md — "Maintaining State"*

---

### FaaS Choreographed Functions — Order Trap

**Principle:** Asynchronous direct-call choreography in FaaS often violates per-event ordering guarantees. Multiple instances of B run independently of A's per-event ordering.

**Do:**
- For in-order processing: orchestrate synchronously per event (one at a time).
- For out-of-order tolerance: accept it (the business doesn't care).

**Don't:**
- Don't assume async direct calls preserve order — fire-and-forget breaks ordering even if you batch.

**Code:**
```python
# AVOID — promotes out-of-order processing
def functionA(events, context):
    for event in events:
        async_functionB(event)  # many parallel Bs, no order guarantee
```

*Ref: Building Event-driven Microservices.md — "Choreography and asychronous function calling"*

---

### FaaS Orchestrated Functions — Synchronous per Event

**Principle:** Orchestrate strictly per event: invoke one function, await result, invoke the next. Each event is fully processed before the next one starts.

**Do:**
- Synchronously orchestrate within a single function execution per event.
- Commit consumer offsets only after the entire workflow for the event is complete.

**Don't:**
- Don't spawn child functions asynchronously inside an orchestration.

*Ref: Building Event-driven Microservices.md — "Orchestration and synchronous function calling"*

---

### Heavyweight Framework Cluster Setup Options

**Principle:** Three deployment modes for heavyweight clusters: **hosted** (manage nothing), **DIY full cluster** (legacy), **CMS-integrated** (deploy on K8s; static master nodes; or per-job session). Pick by team capability and SLA.

**Do:**
- Use hosted for low-overhead, fast time-to-value.
- Use CMS-integrated for microservice-style isolation per job.
- Bake config-as-code into CI/CD for any mode.

**Don't:**
- Don't operate your own Zookeeper-clusters-and-masters without a dedicated ops team.

*Ref: Building Event-driven Microservices.md — "Cluster Setup Options and Execution Modes"*

---

### Heavyweight Application Submission (Driver vs Cluster)

**Principle:** **Driver mode** (Spark/Flink): a local driver coordinates; termination of the driver halts the job — microservice-friendly. **Cluster mode** (Spark/Flink default for Storm/Heron): submit to cluster, use the cluster API to stop — not directly compatible with CMS shutdown.

**Do:**
- Use **driver mode** when integrating with the CMS.
- Use **cluster mode** when you want cluster-managed liveness.

**Don't:**
- Don't rely on the driver for HA unless the underlying cluster provides it.

*Ref: Building Event-driven Microservices.md — "Application Submission Modes"*

---

### Heavyweight Languages & Syntax (SQL-ish + MapReduce)

**Principle:** Heavyweight frameworks increasingly provide SQL-like DSLs and MapReduce-style APIs. SQL lowers the cognitive overhead; MapReduce + Java/Scala covers advanced cases.

**Do:**
- Use SQL DSLs for ETL-style transformations.
- Use MapReduce / DataStream API for stateful, custom logic.

**Don't:**
- Don't expect every feature in every DSL — check the framework's feature matrix.

*Ref: Building Event-driven Microservices.md — "Languages and Syntax"*

---

### Heavyweight Framework Selection

**Principle:** Choose by: required operational expertise, ecosystem maturity, available SLA controls, autoscaling story. Spark is most popular; Flink/Storm active; Heron least; Beam API for portability.

**Do:**
- Pick the most popular mature option unless you have specific constraints.
- Consider Beam API as a portability layer.

**Don't:**
- Don't commit to a heavyweight framework for simple, small workloads.

*Ref: Building Event-driven Microservices.md — "Choosing a Framework"*

---

### Heavyweight Session Windowing Example (Flink)

**Principle:** For "30-minute inactivity" session windows, Flink's `EventTimeSessionWindows.withGap(Time.minutes(30))` provides exactly this. The pattern is: union streams → keyBy → session window → aggregate → sink.

**Do:**
- Use session windows for user-behavior aggregates.
- Configure gap duration explicitly.
- Document the gap-duration rationale.

**Don't:**
- Don't use session windows for fixed-period aggregation — use tumbling windows.

**Code:**
```java
DataStream clickStream = ...
DataStream viewStream = ...
clickStream
 .union(viewStream)
 .keyBy(<key selector>)
 .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
 .aggregate(<aggregator function>)
 .addSink(<producer to output stream>)
```

*Ref: Building Event-driven Microservices.md — "Example: Session Windowing of Clicks and Views"*

---

### Lightweight Framework Materialization: Kafka Streams

**Principle:** Kafka Streams uses internal event streams for repartitioning + broker-stored changelogs for durability. Foreign-key and primary-key joins are first-class.

**Do:**
- Use Kafka Streams for any event-driven microservice that needs table materialization + joins in JVM.
- Configure internal streams partition count explicitly.

**Don't:**
- Don't assume Kafka Streams' stateless features are "free" — they still incur processing cost.

*Ref: Building Event-driven Microservices.md — "Apache Kafka Streams"*

---

### Apache Samza Embedded — Lightweight Mode Caveat

**Principle:** Samza's embedded mode = microservice-style deployment; its cluster mode = heavyweight-style. Embedded may lack some cluster-mode features.

**Do:**
- Use Samza embedded for stateful streams of events in JVM.

**Don't:**
- Don't assume feature parity between embedded and cluster mode.

*Ref: Building Event-driven Microservices.md — "Apache Samza: Embedded Mode"*

---

### Replication Tool Selection (Cross-Cluster)

**Principle:** Replication tools must handle: auto-add of new streams, deletion/modification of streams, offset/partition/timestamp parity, replication latency, scalability. Each tool (MirrorMaker, etc.) has different answers.

**Do:**
- Pick replication tools that survive stream add/remove gracefully.
- Measure replication latency against your DR RTO/RPO.

**Don't:**
- Don't rely on a tool that requires manual re-add on every new stream.
- Don't accept replication that drops partition affinity.

*Ref: Building Event-driven Microservices.md — "Cross-Cluster Event Data Replication"*

---

### Microservice Creation Best Practices (Operational)

**Principle:** Streamline microservice bring-up: repo, CI integration, webhooks, ownership assignment, ACLs, stream creation, template/skeleton. Bake every "must-have" into the skeleton.

**Do:**
- Bake CI, schema conventions, and stream-creation into a single bring-up command.
- Track ownership transfer in your microservice-to-team assignment system.

**Don't:**
- Don't let new teams reimplement the bring-up.
- Don't ship non-standard service templates.

*Ref: Building Event-driven Microservices.md — "Streamlined Microservice Creation Process"*

---

### Container Management Controls (Self-Service)

**Principle:** Expose a minimum-viable set of CMS controls to developers: env vars, cluster selection, resources, scaling (manual or auto), autoscaling triggers. The CMS team guards access; the developer drives the service.

**Do:**
- Provide self-service CMS controls.
- Track who owns what (microservice-to-team assignment).
- Bake autoscaling triggers (CPU/memory/lag).

**Don't:**
- Don't centralize all CMS configuration in a single ops team — bottlenecks follow.
- Don't expose every CMS feature (just enough for self-service).

*Ref: Building Event-driven Microservices.md — "Container Management Controls"*

---

### Streamlined Microservice Creation Checklist

**Principle:** A single, predictable creation flow prevents tribal knowledge and off-standard services.

**Do:**
- Walk a checklist in CI for every new service:
  - [ ] Repo exists; CI pipeline wired
  - [ ] Webhooks configured
  - [ ] Team assignment recorded
  - [ ] ACLs requested for input streams
  - [ ] Output streams created with permissions
  - [ ] Skeleton/template applied
- Automate the creation through tooling.

**Don't:**
- Don't let "tribal knowledge" create uneven service setups.

*Ref: Building Event-driven Microservices.md — "Streamlined Microservice Creation Process"*

---

### Programmatic Environment Bringup for Disaster Recovery

**Principle:** Programmatic environment bringup (broker + compute + tooling) is invaluable for both CI/CD and DR. Investment here pays back dramatically.

**Do:**
- Use the same bring-up tooling for testing environments *and* DR scenarios.
- Keep cluster-creation tooling idempotent and version-controlled.

**Don't:**
- Don't operate a manual bring-up process — it's slow and error-prone under stress.

*Ref: Building Event-driven Microservices.md — "Programmatic Bringup of Event Brokers"*

---

### Testing — Unit Tests for Topology Functions

**Principle:** Topology functions (filter, map, reduce) are the smallest testable units. Mock external stores for stateful function tests; test boundary cases.

**Do:**
- Unit-test stateless functions thoroughly.
- Mock or instantiate a local store for stateful functions.
- Test boundary cases (nulls, max values).

**Don't:**
- Don't skip the unit tests because "we have integration tests."

**Code (stateful):**
```java
public Long addValueToAggregation(String key, Long eventValue) {
 Long storedValue = datastore.getOrElse(key, 0L);
 Long sum = storedValue + eventValue;
 datastore.upsert(key, sum);
 return sum;
}
```

*Ref: Building Event-driven Microservices.md — "Unit-Testing Topology Functions"*

---

### Testing — Topology Integration

**Principle:** Topology testing exercises the framework wiring: time-based aggregations, event scheduling, stateful operations. Each framework provides utility libraries (Spark `MemoryStream`, Flink test, Beam test, Kafka Streams `TopologyTestDriver`).

**Do:**
- Use framework-provided topology test utilities.
- Inject out-of-order events to test scheduling.
- Inject invalid timestamps to test watermark behavior.

**Don't:**
- Don't ship topology without testing time-based code paths.

*Ref: Building Event-driven Microservices.md — "Testing the Topology"*

---

### Schema-Evolution CI Check

**Principle:** Pull schemas from the registry; run evolutionary rule checks in CI before merge. Reject breaking changes that aren't part of a coordinated migration.

**Do:**
- Generate schemas from code when possible (compile-time generation).
- Run compatibility checks in CI.

**Don't:**
- Don't ship a schema change that fails evolution rules.

*Ref: Building Event-driven Microservices.md — "Testing Schema Evolution and Compatibility"*

---

### Integration Testing — Event Stream Population Strategies

**Principle:** Three strategies for populating test streams: **production data** (most realistic, security-constrained), **curated data** (controlled, maintenance overhead), **schema-generated mocks** (exhaustive, joint-relations-a-pain).

**Do:**
- Default to schema-generated mocks with carefully crafted relationships.
- Use curated sets for known regression scenarios.
- Use production data for performance/load tests only — with quotas/security.

**Don't:**
- Don't use **production data** blindly — PII and secrets constraints apply.
- Don't forget the FK relationships in mocks (your service may join on them).

*Ref: Building Event-driven Microservices.md — "Populating with events from production", "Populating with events from a curated testing source", "Creating mock events using schemas"*

---

### Integration Testing — Local External (Containerized Dependencies)

**Principle:** A container with all dependencies (broker, schema registry, …) lets any team test in isolation. Run the microservice outside the container, pointed at the container's addresses.

**Do:**
- Provide an internal Docker image with broker + schema registry pre-wired.
- Make the schema/topics creation part of the container startup.

**Don't:**
- Don't rely on every teammate's local install — version drift is inevitable.

*Ref: Building Event-driven Microservices.md — "Create a Temporary Environment External to Your Test Code"*

---

### Integration Testing — Hosted Service Emulation

**Principle:** For services with no local implementation (e.g., AWS Event Hubs, Azure Event Hubs lack emulators), use what's available: local substitutes (Kafka instead of Event Hubs for Kafka-protocol-compatible clients), emulators (Google PubSub), or LocalStack for AWS services.

**Do:**
- Pick broker technologies with local emulation support when possible.
- Document how to test your service without remote dependencies.

**Don't:**
- Don't adopt services with no local testing option without considering the per-dev overhead.

*Ref: Building Event-driven Microservices.md — "Integrate Hosted Services Using Mocking and Simulator Options"*

---

### Multi-Cluster Operations

**Principle:** Multi-cluster needs are real (regional residency, scale, redundancy). Strategies include per-team clusters or shared clusters with quotas; cross-cluster replication tools vary widely.

**Do:**
- Pick replication tools with strong offset/partition parity.
- Mirror data explicitly to disaster-recovery clusters.

**Don't:**
- Don't run single-cluster setups for highly regulated data without a documented DR plan.

*Ref: Building Event-driven Microservices.md — "Cluster Creation and Management"*

---

### Asynchronous UI — What to Disclose

**Principle:** In async-UI designs, telegraph state to users. Provide spinners; disable conflicting actions; surface completion events.

**Do:**
- Disable conflicting actions during async processing.
- Show clear "request received, working…" message.
- Plan for duplicate events on retries.

**Don't:**
- Don't sync-UI-wrap an async-feature — users will think the click did nothing.

*Ref: Building Event-driven Microservices.md — "Processing Events for User Interfaces"*

---

### Schema-Change Communication Discipline

**Principle:** Schema evolution without explicit communication = silent breakage. Notify consumers of *any* schema change (even compatible ones) via a schema registry's changelog stream.

**Do:**
- Auto-notify via the schema registry when schemas change.
- Build warning dashboards (consumer service X uses schema X.0; schema X.1 published).

**Don't:**
- Don't rely on consumers to "just check" — telemetry the *registration*.

*Ref: Building Event-driven Microservices.md — "Schema Creation and Modification Notifications"*

---

### Choosing a Heavyweight Framework — Decision Heuristic

**Principle:** Spark is the most popular; Flink mature and growing; Storm mature but legacy; Heron advanced-Storm; Beam portable API on top of others. Pick by team skills, framework fit, and operational tolerance.

**Do:**
- Default to Spark if the team has data-engineering background; many tools/training available.
- Default to Flink for low-latency stream processing.
- Use Beam if multi-runner portability matters.
- Use Storm only when migrating an existing Storm system.

**Don't:**
- Don't pick Heron for greenfield — community momentum is low.
- Don't pick heavyweight frameworks without checkpointing / HA enabled for any stateful workload.

*Ref: Building Event-driven Microservices.md — "Choosing a Framework"*

---

## Anti-Patterns & Common Mistakes

- **Event as semaphore:** Emitting an event that says "work done, look elsewhere for result." → Always include the full fact; events *are* the data.
- **Mixing event types in one stream:** Producer overloads `type` field; schema becomes union → Split into separate streams per single-purpose event.
- **JSON-only events with no schema:** Consumers interpret implicitly → Adopt Avro/Protobuf + schema registry.
- **Sharing state directly between services:** Two services read same DB → Each materializes its own copy; expose via bounded-context API.
- **Aggregate layer with creeping business logic:** "Tragedy of the commons" → Strict stewardship or event-first composition.
- **Distributed monolith:** Synchronous point-to-point microservices mimic monolith boundaries → Move to event-driven; align on bounded contexts.
- **CDC framework as the destination:** Long-term connector-based reliance on legacy → Migrate to native outbox publication.
- **Big monolithic backend + separate frontend:** Cross-team dependencies for product changes → Adopt microfrontends + event-driven backends.
- **Reverse-compatible new field without defaults:** Old consumers break on missing fields → Always provide defaults for new optional fields.
- **Compaction on non-keyed streams:** Logically deletes the only copy → Only compact keyed streams.
- **Profiling on FaaS as a permanent solution:** Cold starts make continuous profiling impractical → Migrate to always-on or accept cloud profile tools.
- **Wall-clock-windowed aggregations as SLO-grounded:** Non-reproducible on reprocess → Use event-time + watermarks or stream time.
- **Synchronous direct calls between teams:** Couples bounded contexts → Replace with events; or accept that pattern explicitly.
- **Sidecar with cross-team deploy lifecycle:** Breaks "single deployable" → Keep sidecar in the same pod / lifecycle as the legacy app.
- **Per-event offsets without copartitioning on joins:** Performance collapse → Copartition before joining on key.
- **Rollback automation that doesn't preserve new schema:** Composite state-or-schema drift → Use two-stream eventual migration.
- **Test in shared cluster:** Orphaned event streams, vague ownership → Programmatic disposable test environments.
- **Schema change without producer/consumer negotiation:** Silent break → Renegotiate data contract; schedule migration.
- **Heavyweight framework used for simple work:** Unjustified operational cost → Switch to lightweight or BPC.

## Decision Heuristics / Checklists

- **New service:** Start by writing the event schema, getting consensus, then the service. Not the other way around.
- **Schema change:** First ask: Can this stay within full compatibility? If yes, add field with default. If no, two-stream eventual migration; never silent breakage.
- **Where to put business logic:** Same bounded context as the data owner; reject "data team owns the data, others query it."
- **State store:** Hot tables → internal (RocksDB); relational / less-hot → external; per-instance, never shared.
- **Heavyweight vs lightweight framework?** Heavyweight for analytics-heavy, big data ETL; lightweight for stateful microservices with joins.
- **FaaS?** Stateless, simple, queue-style work; spiky and latency-tolerant.
- **CDC framework?** Use as bootstrap; move toward native outbox for first-party publications.
- **Saga or compensation?** Saga if strict reversal needed (financial); compensation if customer-facing (retail).
- **Schema evolution locks vs deploys:** Single responsibility > emergency override; if you must override, plan a migration.
- **Topologies (choreography vs orchestration):** Choreography for ≤ few services with stable order. Orchestration for complex / frequently changing workflows.
- **Deployment pattern choice:** Full-stop by default; rolling only if (topology + schema + state unchanged); blue-green only for HTTP-driven producers, never for stream-reactive producers.
- **SLO windows for LLM-style latency:** 95% over 7 days initial.
- **Dedupe store TTL:** Bound by business risk-of-duplicate; max-bytes / rolling-window.
- **Schema registry or not?** Always, in production. Save on bandwidth and discovery.

## Key Takeaways

1. **The medium is the message.** Event-driven is a cultural shift, not a tech swap.
2. **Bounded context first; technology second.** Sole ownership > shared layers.
3. **Events are the data, not signals.** Avoid semi-events; embed the full fact.
4. **One stream, one event type.** Single-purpose events simplify evolution and consumer logic.
5. **Singletons of writers per stream** = lineage and clarity.
6. **Unify data liberation with business events**: query → CDC → outbox → triggers as a journey.
7. **Copartition keyed streams for joins.** No locality → no correctness, no perf.
8. **Event-time + watermarks (or stream-time) for deterministic processing.**
9. **Choreography for simple flows; orchestration for complex / observable workflows.**
10. **Sagas only when needed; compensations when kinder to users.**
11. **Heavyweight frameworks for analytical scale; lightweight for stateful microservice materialization.**
12. **Test deployment + state restore + schema evolution explicitly.**
13. **Blue-green only when the producer is HTTP-driven.** Never for stream-reactive services.
14. **Centralize event broker, schema registry, CMS, CI/CD — pay the microservice tax in full or stay small.**
15. **Materialize state from events, period** — even for HTTP-read services. The single source of truth is the stream.

## Cross-References

- Related: [[../Building_Microservices.md]] (microservice design; bounded-context alignment)
- Related: [[../Communication_Patterns.md]] (async patterns; saga compensation interplay)
- Related: [[../Software_Architecture_Patterns.md]] (event-driven, CQRS, event sourcing)
- Related: [[../Building_An_Event-Driven_Data_Mesh.md]] (data-mesh takes the same stream-first worldview)
- Related: [[../Observability_Engineering.md]] (event-stream observability via SLOs / traces / wide events)
- Related: [[../Microservices_Up_And_Running.md]] (operational concerns; CMS, CI/CD)

