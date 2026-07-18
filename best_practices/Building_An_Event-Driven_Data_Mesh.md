# Building an Event-Driven Data Mesh
**Author:** Adam Bellemare
**Topic tags:** `#architecture` `#api`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/Building An Event-Driven Data Mesh/Building An Event-Driven Data Mesh.md` · `summaries/Building_An_Event-Driven_Data_Mesh.md`

## TL;DR
Data mesh treats data as a product owned by the producing domain, not a central
data team. Event streams (durable append-only logs with indefinite retention,
partitioning, and compaction) form the single substrate for both operational and
analytical use cases via the Kappa architecture. Federated governance sets
interoperability standards (schemas, partitions, time zones); self-service
platform tooling (schemas, catalog, connectors, IAM, lineage) makes participation
painless. Schema evolution, state-event design, and explicit handling of eventual
consistency are the recurring engineering concerns.

---

## Best Practices by Topic

### Domain Ownership (Data Mesh Pillar 1)

**Principle:** The team that creates the data owns its public model, its quality,
its schema, and its lifecycle; consumers never couple on internal data models.

**Do:**
- Expose data through an *anti-corruption layer* (schema-registry-managed event
  schema) so the internal model can evolve without breaking consumers.
  *Ref: Building An Event-Driven Data Mesh.md — "Anti-corruption layer" (`page-41-0`),*
  *"Selecting the Data to Expose from Your Domain" (`page-40-0`).*
- Apply Domain-Driven Design vocabulary: bounded context, ubiquitous language,
  aggregate root — restrict published events to entities that other domains can
  legitimately couple on.
  *Ref: Building An Event-Driven Data Mesh.md — "Domain-Driven Design in Brief" (`page-40-0`).*
- Ask prospective consumers which data they need; do not model for everyone.
  *Ref: Building An Event-Driven Data Mesh.md — "Selecting the Data to Expose" (`page-40-0`).*

**Don't:**
- Don't let consumers reach directly into your database or couple on your
  internal model — "the database should be directly accessed only by the service
  that owns it, and not used as an integration point."
  *Ref: Building An Event-Driven Data Mesh.md — "Read-only data is readily available" (`page-18-0`).*
- Don't fight multiple copies of data — they are inevitable. Embrace them via
  controlled, governed replication.
  *Ref: Building An Event-Driven Data Mesh.md — "Making Multiple Copies of Data Is Bad" (`page-34-0`).*

---

### Data as a Product (Data Mesh Pillar 2)

**Principle:** A data product is treated like any other product — owner, SLA,
tier, schema, documentation, discovery metadata, deprecation plan, and an
immutable time-stamped event surface.

**Do:**
- Make every data product immutable and time-stamped so any consumer can
  reproduce the same query result later.
  *Ref: Building An Event-Driven Data Mesh.md — "Data Products Provide Immutable and Time-Stamped Data" (`page-43-0`).*
- Build at least one of three alignment types per product:
  - *Source-aligned* (raw facts — closest to source of truth)
  ```text
  Value: {
    sales_id: 8675309,
    item_ids: [4625382, 4625382, 4625382, 100900],
    total_usd: 89.12,
    datetime: "2022-11-12T03:51:19Z",
    shipping_address: "123 Fake Street, Springfield"
  }
  ```
  - *Aggregate-aligned* (pre-computed, e.g. daily sales)
  ```text
  Value: {
    date: "2022-11-12",
    total_items_sold: 41292,
    total_items_value_usd: 1902712.22
  }
  ```
  - *Consumer-aligned* (domain-specific join/transform)
  ```text
  Value: {
    user_id: "UUID-123456789",
    predicted_item_ids_to_advertise: [4625382, 100901],
    cost_tolerance: "high",
    conversion_probability: 0.1233,
    estimated_spend_usd: 500.00,
    ad_bid_limit_usd: 9.75
  }
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Example 2-1 / 2-2 / 2-3" (`page-46-0`).*
- Serve via push (event stream) for low-latency needs; expose via pull (REST /
  Parquet files) only when latency tolerance allows.
  *Ref: Building An Event-Driven Data Mesh.md — "Accessing a Data Product Via Push or Pull" (`page-45-0`).*
- Adopt the medallion quality tiers *Bronze / Silver / Gold* (or equivalent) so
  consumers know what to trust.
  *Ref: Building An Event-Driven Data Mesh.md — "Data quality classifications" (`page-92-0`).*

**Don't:**
- Don't expose events whose meaning can change as the domain evolves (deltas).
  See "Designing Events" below.
- Don't add SLA / quality metadata as an afterthought — make them mandatory at
  registration in the metadata catalog.
  *Ref: Building An Event-Driven Data Mesh.md — "Metadata Standards and Requirements" (`page-91-0`).*

---

### Federated Governance (Data Mesh Pillar 3)

**Principle:** A representative body sets *standards*, not *mandates* —
languages, frameworks, schema tech, partition conventions, time handling — while
domain teams keep implementation autonomy.

**Do:**
- Form a small federated governance team (representatives from each domain +
  data architects + security). Run it like a parliament: agendas, proposals,
  review, archive.
  *Ref: Building An Event-Driven Data Mesh.md — "Forming a Federated Governance Team" (`page-86-0`),*
  *"What Does a Governance Meeting Look Like?" (`page-97-0`).*
- Standardize on a T-shirt sizing for partition counts (xsmall=1, small=4,
  medium=8, large=16, xlarge=32, xxlarge=64, jumbo=256) and require the same
  partition count for streams keyed on the same common entity.
  *Ref: Building An Event-Driven Data Mesh.md — "Event Stream Keying and Partitioning" (`page-95-0`).*
- Standardize on one schema technology per data product type (e.g. Avro for
  streams, Parquet for batch files); justify exceptions.
  *Ref: Building An Event-Driven Data Mesh.md — "Supporting Data Product Schemas" (`page-89-0`).*
- Use UTC-0 as the primary time zone for time-based data products.
  *Ref: Building An Event-Driven Data Mesh.md — "Time and Time Zones" (`page-96-0`).*
- Make data product access *disabled by default*; consumers must register
  (defense in depth).
  *Ref: Building An Event-Driven Data Mesh.md — "Disable Data Product Access by Default" (`page-100-0`).*

**Don't:**
- Don't accept a wide range of programming languages "for the sake of novelty"
  — write data products only in languages officially supported.
  *Ref: Building An Event-Driven Data Mesh.md — "Supporting Programming Languages and Frameworks" (`page-90-0`).*

---

### Self-Service Platform (Data Mesh Pillar 4)

**Principle:** Maturity-Laddered tooling — *Level 1 (MVP)*: event broker +
schema registry + spreadsheet catalog + connectors. *Level 2 (EP)*: full metadata
catalog + identity + RBAC + management UI. *Level 3 (MP)*: OAuth2/OIDC, IaC
(Terraform), programmatic API, multiregion, alerting.

**Do:**
- Bootstrap the MVP with a cloud spreadsheet catalog gated by write
  permissions; expect owners to register topics, owners, SLA, quality, schema
  URI, description.
  *Ref: Building An Event-Driven Data Mesh.md — "An Extremely Basic Metadata Catalog" (`page-113-0`).*
- Adopt Apache-licensed self-service building blocks (Kafka, Schema Registry,
  Kafka Connect, Apache Atlas / Amundsen, Apache Pinot, Apache Flink, Apache
  Spark, ksqlDB) instead of in-house replicas.
  *Ref: Building An Event-Driven Data Mesh.md — "The Schema Registry" (`page-112-0`),*
  *"Selecting an Event Broker" (`page-80-0`).*
- Use OAuth2 / OIDC to unify identity across GitHub/GitLab, Kubernetes, Kafka,
  and cloud IAM.
  *Ref: Building An Event-Driven Data Mesh.md — "Authentication, Identification, and Access Management" (`page-131-0`).*
- Provide a programmatic data product management API for publishing,
  deprecating, deleting, with identity, permissions, lineage, and messaging
  sub-APIs.
  *Ref: Building An Event-Driven Data Mesh.md — "Programmatic Data Product Management API" (`page-133-0`).*
- Track *both* topology-based and record-based lineage; record-based via
  per-stage header metadata is sufficient for many audit needs.
  *Ref: Building An Event-Driven Data Mesh.md — "Data Product Lineage" (`page-105-0`).*
- Alert on the two SLA pillars: update frequency and time-since-last-event;
  pick smart thresholds from historical patterns.
  *Ref: Building An Event-Driven Data Mesh.md — "Monitoring and Alerting" (`page-135-0`).*

**Don't:**
- Don't build everything before you start — "you aren't gonna need it"
  (YAGNI). Solve pain points iteratively.
  *Ref: Building An Event-Driven Data Mesh.md — "Level 1 Wrap-Up" (`page-115-0`).*
- Don't write your own notification system; integrate Slack/Teams/email.
  *Ref: Building An Event-Driven Data Mesh.md — "Messaging" (`page-134-0`).*

**Code:**
```text
Schema technology example (Protobuf, Person):
message Person {
  int32 id = 1;
  string name = 2;
  int32 height = 3;
}
```
*Ref: Building An Event-Driven Data Mesh.md — "Example 5-1" (`page-112-0`).*

---

### Event Streams as the Backbone

**Principle:** An event stream is a *durable, append-only, ordered,
replayable* log — not a queue, not ephemeral messaging, not transient RPC.
Properties: immutability, indefinite retention (via tiered storage), partitioning
by key, compaction + tombstones.

**Do:**
- Use a broker with *unlimited retention* (Kafka, Pulsar). Cap-bounded brokers
  (Kinesis, Event Hubs, Pub/Sub) cannot host data products.
  *Ref: Building An Event-Driven Data Mesh.md — "Table 3-1: Maximum event retention" (`page-81-0`).*
- Key events on a common entity ID (e.g. `user_id`) so every consumer group
  gets all partitions of a key in order.
  *Ref: Building An Event-Driven Data Mesh.md — "Event Stream Keying and Partitioning" (`page-95-0`).*
- Use a *tombstone* (key present, value null) to delete a key from ECST
  materialization; make tombstones themselves eligible for compaction.
  *Ref: Building An Event-Driven Data Mesh.md — "Deletions" (`page-79-0`),*
  *"Figure 3-12: Compacting older events" (`page-80-0`).*
- Stay alert for *hot partitions* when an unsuitable partitioner forces 99% of
  events to one partition.
  *Ref: Building An Event-Driven Data Mesh.md — "Be careful about hot partitions" (`page-96-0`).*

**Don't:**
- Don't confuse *ephemeral message-passing* (NATS, at-most-once) with event
  streams. "Ephemeral communication... is completely unsuited for providing the
  means to communicate data products."
  *Ref: Building An Event-Driven Data Mesh.md — "Ephemeral Message-Passing" (`page-66-0`).*
- Don't pick a queue broker that requires time-based retention; even queue
  brokers that grew replay (RabbitMQ Streams, Solace) "struggle to support the
  strict ordering semantics, indefinite replayability, and scalability
  requirements of a modern data mesh."
  *Ref: Building An Event-Driven Data Mesh.md — "Queuing" (`page-67-0`).*

**Code (Kappa-style join in Kafka Streams):**
```java
StreamsBuilder builder = new StreamsBuilder();
KTable inventory = builder.table("inventory");
KTable sales = builder.table("items");
KTable enrichedItemInventory = inventory.join(sales, ...);
```
*Ref: Building An Event-Driven Data Mesh.md — "Example 3-1" (`page-73-0`).*

**Code (Flink SQL join):**
```sql
CREATE TABLE Inventory (
  item_id VARCHAR,
  quantity BIGINT,
  timestamp TIMESTAMP(3),
  PRIMARY KEY (item_id) ENFORCED
) WITH (
  'connector' = 'kafka',
  'topic' = 'inventory',
  'properties.bootstrap.servers' = 'localhost:9092',
  'format' = 'avro',
  'scan.startup.mode' = 'earliest-offset'
);

CREATE TABLE Enriched_Item_Inventory AS
SELECT *
FROM Inventory
INNER JOIN Items
ON Items.item_id = Inventory.item_id;
```
*Ref: Building An Event-Driven Data Mesh.md — "Example 3-2" (`page-74-0`).*

---

### State Events vs. Delta Events vs. Measurement vs. Notification

**Principle:** Across domains use *state events*. Delta events are internal
event-sourcing primitives; measurement events power aggregation; notification
events are a pointer anti-pattern.

**Do:**
- Use **current-state** events (ECST) by default. Includes full public state per
  event; previous state derives from a prior event.
  ```text
  Key: 20
  Value: { name: "Adam", country: "Canada" }   // current state only
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Current State Events" (`page-166-0`).*
- Use **measurement events** for occurrences (clicks, sensor reads, ad views)
  and let aggregates be computed downstream.
  ```text
  Key: "USERID-8271949472726174"
  Value: {
    utc_timestamp: "2022-01-22T15:39:19Z",
    ad_id: 1739487875123,
    page_id: 364198769786,
    url: https://www.somewebsite.com/welcome.html
  }
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Measurement Events" (`page-181-0`).*

**Don't:**
- Don't cross domain boundaries with **delta events** — there are infinitely
  many, every consumer must replicate the producer's aggregation logic, and
  ownership ends up inverted. "Do not use delta events for cross-domain
  coupling."
  *Ref: Building An Event-Driven Data Mesh.md — "Why Delta Events Don't Work for Event-Driven Data Products" (`page-172-0`).*
- Don't ship **before/after state events** as cross-domain contracts. Compaction
  is hard (Kafka can't recognize the null-valued-after as a tombstone), payload
  size doubles, and stale `before` data leaks unless you also emit a tombstone
  (e.g. Debezium's two-record DELETE).
  *Ref: Building An Event-Driven Data Mesh.md — "Before/After State Events" (`page-167-0`).*
- Don't deploy **notification events** as a stand-in for state. The mutable
  `access_uri` can be re-updated before a consumer reads it — events can be
  missed, even the *latest* state can be wrong.
  *Ref: Building An Event-Driven Data Mesh.md — "Notification Events" (`page-185-0`).*
- Don't use **hybrid events** for transition-heavy, frequently-added business
  logic (e.g. "userReturnedItemAfterTelephoneComplaint" deltas). Static
  one-shot context (e.g. `method_of_signup: VIA_AD_EMAIL`) is the safe boundary
  case.
  *Ref: Building An Event-Driven Data Mesh.md — "Hybrid Events—State with a Bit of Delta" (`page-183-0`).*

---

### Schema Evolution

**Principle:** Aim for *full-transitive* compatibility so every version can
convert to every other version in either direction.

**Do:**
- Document compatibility modes for the chosen schema tech:
  - *Backward* — new schema reads old data (safe to drop fields).
  - *Forward* — old schema reads new data (requires default values for added
    fields).
  - *Full-transitive* — every version interchangeable.
  *Ref: Building An Event-Driven Data Mesh.md — "Schema Evolution" (`page-150-0`).*
- Use Avro or Protobuf v2 to get explicit default-value support for forward
  compatibility:
  ```json
  {
    "type": "record",
    "name": "Example",
    "doc": "Version 1, but with a default value",
    "fields": [
      { "name": "id", "type": "integer" },
      { "name": "foobar", "type": "string", "default": "DEFAULT_VALUE_STRING" }
    ]
  }
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Example 6-1/6-2" (`page-152-0`).*
- Run schema compatibility checks during deployment; never accept a
  full-compiled topic that fails them.
  *Ref: Building An Event-Driven Data Mesh.md — "Schema evolution must be enforced" (`page-148-0`).*

**Code (Java producer using a Protobuf-generated class):**
```java
Person mack = Person.newBuilder()
    .setId(4291)
    .setName("Mackenzie Bellemare")
    .setHeight(45)
    .setCountryCode("CAD")
    .build();
output = new FileOutputStream("ProtoPerson.data");
mack.writeTo(output);
```
*Ref: Building An Event-Driven Data Mesh.md — "Example 6-2" (`page-144-0`).*

**Don't:**
- Don't reach for Protobuf v3 "for the JSON-encoding support" and lose custom
  default values — evolution gets much harder.
  *Ref: Building An Event-Driven Data Mesh.md — "Protobuf" (`page-146-0`).*
- Don't use *schemaless JSON* for any data product — "schemaless JSON is not
  suitable for use in data products as it leaves too much room for errors."
  *Ref: Building An Event-Driven Data Mesh.md — "JSON Schema" (`page-149-0`).*
- Don't let breaking changes ship unannounced. Walk the 4-step process:
  *Design* → *Iterate with consumers + governance* → *Migration +
  deprecation plan* → *Execute release*.
  *Ref: Building An Event-Driven Data Mesh.md — "Negotiating a Breaking Schema Change" (`page-153-0`).*

---

### Bootstrapping Data Products from Existing Systems

**Principle:** Meet existing systems where they are. Dual writes work *most of
the time* — the failure modes must be designed for.

**Do:**
- Prefer *CDC* (Debezium-class) for low-latency, change-complete capture with
  non-blocking snapshots; can use watermark-interleave for live snapshots
  without table locks.
  *Ref: Building An Event-Driven Data Mesh.md — "Change-Data Capture" (`page-192-0`).*
- Use the *transactional outbox* pattern (write internal change + outbox row in
  one transaction) when you control the source application and the DB supports
  ACID:
  ```python
  conn.autocommit = False
  cursor = conn.cursor()
  cursor.execute("Update EcomItem set price = 1299.99 where id = 4291")
  cursor.execute("Select name, price from EcomItem where id = 4291")
  name_and_price = cursor.fetchone()
  cursor.execute(
      "INSERT INTO EcomItem_Outbox (id, name, price) VALUES (4291, %s, %s)",
      name_and_price)
  conn.commit()
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Example 8-1" (`page-196-0`).*
- Use *eventification* (denormalize + remodel at the outbox or in a dedicated
  Kafka Streams / Flink SQL service) when consumers need a join already baked
  in.
  ```java
  // Kafka Streams
  ecomItemTable.join(merchantTable, EcomItem::getMerchantId, new EcomToMerchantJoiner())
               .toStream()
               .to(enrichedEcomItemTopic, Produced.with(Serdes.Long(), enrichedEcomItemSerde));
  ```
  ```sql
  -- Flink SQL
  SELECT *
  FROM EcomItem
  INNER JOIN Merchant
  ON EcomItem.merchantId = Merchant.id;
  ```
  *Ref: Building An Event-Driven Data Mesh.md — "Example 8-3 / 8-5" (`page-204-0`).*
- Verify connector ownership before signing up to run it; failure ownership
  tends to surface late.
  *Ref: Building An Event-Driven Data Mesh.md — "Getting Started: Bootstrapping with Connectors" (`page-189-0`).*

**Don't:**
- Don't dual-write. "Most of the time you won't have a problem" right up until
  network timeouts / broker hiccups silently drop events.
  *Ref: Building An Event-Driven Data Mesh.md — "Dual Writes" (`page-189-0`).*
- Don't publish CDC events from a highly-normalized schema as-is —
  internal-model coupling forces every consumer to denormalize downstream.
  *Ref: Building An Event-Driven Data Mesh.md — "Highly normalized event streams" (`page-194-0`).*
- Don't denormalize extremely volatile data (e.g. inventory count) or very
  large payloads (e.g. top-100 reviews) into every event — "a lot of data with
  a high rate of change. This can cause a compounding high load."
  *Ref: Building An Event-Driven Data Mesh.md — "What Should Go In the Event?" (`page-205-0`).*
- Don't use DB polling when hard deletes matter — polling won't see them. Use
  soft deletes + tombstones or move to CDC.
  *Ref: Building An Event-Driven Data Mesh.md — "Will miss hard deletes" (`page-191-0`).*

---

### Kappa Architecture (Stream-Only Source of Truth)

**Principle:** Use one stream processing framework for both real-time and
historical replays. Avoid the Lambda two-layer seam.

**Do:**
- Build consumer state by replaying from offset 0; use stream processors
  (Kafka Streams, Flink, Spark Structured Streaming) with built-in snapshot
  support.
  *Ref: Building An Event-Driven Data Mesh.md — "The Kappa Architecture" (`page-71-0`).*
- Rely on broker *compaction* to keep ECST streams proportional to the keyspace
  (default lag ~24h; raise it for consumers that may be offline over a long
  weekend).
  *Ref: Building An Event-Driven Data Mesh.md — "Compaction" (`page-78-0`).*

**Don't:**
- Don't use the Lambda architecture for data products. Every Lambda source
  compound-explodes reconciliation: "Two Lambda data products result in four
  unique relationships... three Lambda data products result in eight(!)
  unique relationships... I've never seen widespread successful use of
  Lambda-based data products."
  *Ref: Building An Event-Driven Data Mesh.md — "The Lambda Architecture and Why It Doesn't Work for Data Mesh" (`page-75-0`).*

---

### Eventual Consistency

**Principle:** Two independent consumer replicas eventually converge on the
same stored values; aim to *prevent* the causes, *expose* the lag when
unavoidable, *plan* for reprocessing.

**Do:**
- Use offsets (not last-event-time alone) to detect lag. A compacted
  state-stream has long gaps between events and last-event-time would falsely
  look like lag.
  *Ref: Building An Event-Driven Data Mesh.md — "Expose Eventual Consistency in the Server Response" (`page-236-0`).*
- Expose consistency to synchronous callers via:
  - **Halt serving when lag > threshold** (return HTTP 503 with Retry-After),
  - **Provide stale data + a flag** so clients can act,
  - **Callback API** when the lag clears.
  *Ref: Building An Event-Driven Data Mesh.md — "Expose Eventual Consistency in the Server Response" (`page-236-0`).*
- Synchronize cloud-storage batch outputs on consistent time boundaries (e.g.
  hourly) so partitioning policies align across data products.
  *Ref: Building An Event-Driven Data Mesh.md — "Synchronize Data Products on Time Boundaries" (`page-239-0`).*
- Choose one of three late-arrival strategies and document it in the SLA:
  - *Discard* — drop events past the window cutoff,
  - *Delayed close* — wait N seconds before emitting,
  - *Parallel windows* — keep old window open for the grace period, output
    updates.
  *Ref: Building An Event-Driven Data Mesh.md — "Resolving Late-Arriving Events" (`page-241-0`).*

**Don't:**
- Don't promote synchronous API calls to cross-system "data access" — pull the
  same data through event streams instead and let each consumer materialize.
  *Ref: Building An Event-Driven Data Mesh.md — "Use Event-Driven Data Products Instead of Request-Response Server API Calls" (`page-235-0`).*
- Don't fix bad-data incidents by *assuming* you can rewind the world — warn
  downstream consumers, throttle, and possibly purge + re-create.
  *Ref: Building An Event-Driven Data Mesh.md — "Purge and re-create the data product" (`page-238-0`).*

---

### Privacy, Compliance, Encryption, Crypto-Shredding

**Principle:** Build *defense in depth*: identity, access policy,
end-to-end / field-level encryption, crypto-shredding for "right to be
forgotten."

**Do:**
- Require consumer registration before data product access is granted.
  *Ref: Building An Event-Driven Data Mesh.md — "Disable Data Product Access by Default" (`page-100-0`).*
- Apply end-to-end encryption at the producer; cipher-text sits on disk;
  consumers fetch keys from KMS.
  *Ref: Building An Event-Driven Data Mesh.md — "Consider End-to-End Encryption" (`page-101-0`).*
- Apply field-level encryption (preferably *format-preserving* on PII columns
  like email, account, user) so consumers without decrypt rights can still
  aggregate the non-PII fields.
  *Ref: Building An Event-Driven Data Mesh.md — "Field-Level Encryption" (`page-103-0`), "Table 4-1" (`page-103-0`).*
- Implement *crypto-shredding* for GDPR Article 17: deleting the KMS key
  invalidates all retained encrypted copies across backups, consumers, and
  cold storage.
  *Ref: Building An Event-Driven Data Mesh.md — "Data Privacy, the Right to Be Forgotten, and Crypto-Shredding" (`page-104-0`).*

**Don't:**
- Don't read everyone in via a single master credential — enforce
  per-consumer identities and ACLs so the dependency graph is *real*, not
  opt-in.
  *Ref: Building An Event-Driven Data Mesh.md — "Disable Data Product Access by Default" (`page-100-0`).*

---

### Multi-region / Multi-cloud

**Principle:** Governance writes the rules for where data may live; the
self-service platform enforces them.

**Do:**
- Bake regional / cloud / PII / financial tags into data product metadata; the
  platform rejects replication requests that violate them.
  *Ref: Building An Event-Driven Data Mesh.md — "Multiregion and Multicloud Data Products" (`page-137-0`).*
- Use Kafka MirrorMaker 2.0 or Confluent Replicator for stream replication;
  track the replication process itself as a data product with its own owner.
  *Ref: Building An Event-Driven Data Mesh.md — "Streamlined data product replication" (`page-137-0`).*

---

## Anti-Patterns & Common Mistakes
- **Schema on read (data lake without write-time schema enforcement):** leaks
  bad data into every downstream pipeline. Enforce at write-time via
  schema-registry-gated producers. *fix:* enforce schemas, run compatibility
  checks at publish.
  *Ref: Building An Event-Driven Data Mesh.md — "The Organizational Impact of Schema on Read" (`page-26-0`).*
- **Central data team monolith bottleneck:** "Changes require coordination
  across many teams." *fix:* apply Domain Ownership — distribute to producing
  domains. *Ref: Building An Event-Driven Data Mesh.md — "The Data Monolith Problem" (`page-15-0`).*
- **Coupling on the internal data model of a source system.** *fix:* expose
  only via the anti-corruption layer / data product schema.
  *Ref: Building An Event-Driven Data Mesh.md — "Strategy 1: Replicate data between services" (`page-19-0`).*
- **Dual writes (DB + event stream) for atomicity.** *fix:* transactional
  outbox or CDC. *Ref: Building An Event-Driven Data Mesh.md — "Dual Writes" (`page-189-0`).*
- **Delta events as cross-domain contracts.** *fix:* use state events; reserve
  deltas for internal event sourcing. *Ref: Building An Event-Driven Data Mesh.md — "Why Delta Events Don't Work" (`page-172-0`).*
- **Before/after state events for ECST.** *fix:* use current-state only; emit
  tombstone alongside CDC if you need deletes.
  *Ref: Building An Event-Driven Data Mesh.md — "Before/After State Events" (`page-167-0`).*
- **Notification events that point to mutable data.** *fix:* publish the state
  itself. *Ref: Building An Event-Driven Data Mesh.md — "Notification Events" (`page-185-0`).*
- **Lambda architecture dual layers.** *fix:* Kappa with compaction +
  indefinite retention. *Ref: Building An Event-Driven Data Mesh.md — "The Lambda Architecture and Why It Doesn't Work for Data Mesh" (`page-75-0`).*
- **Treating the event stream as ephemeral transport.** *fix:* use a
  no-time-cap broker (Kafka / Pulsar) so the stream can hold full history.
  *Ref: Building An Event-Driven Data Mesh.md — "Selecting an Event Broker" (`page-80-0`).*
- **Sprawl of languages / frameworks "for novelty."** *fix:* standardize via
  federated governance proposals with trials.
  *Ref: Building An Event-Driven Data Mesh.md — "Supporting Programming Languages and Frameworks" (`page-90-0`).*
- **Bypassing upstream access controls by copying a sibling data set.**
  Surfaced in Chapter 1 — Predictions team copied sales data from User
  Insights instead of the source, leading to drift. *fix:* centralize with
  managed access via the self-service platform; never publish a copy without
  governance. *Ref: Building An Event-Driven Data Mesh.md — "Do-it-yourself and custom point-to-point data connections" (`page-29-0`).*

---

## Decision Heuristics / Checklists
- **Push vs. pull:** pull APIs only when SLA tolerates periodic polling and
  bulk throughput; push for real-time operations.
  *Ref: Building An Event-Driven Data Mesh.md — "Accessing a Data Product Via Push or Pull" (`page-45-0`).*
- **Source vs. aggregate vs. consumer-aligned:** start with source-aligned
  (cheapest, most general); build aggregate-aligned when multiple teams hit
  the same repeated join; only build consumer-aligned when *no* single
  upstream can supply the mix.
  *Ref: Building An Event-Driven Data Mesh.md — "The Three Data Product Alignment Types" (`page-46-0`).*
- **State vs. delta:** delta only *inside* a bounded context; state across
  boundaries.
  *Ref: Building An Event-Driven Data Mesh.md — "Why Delta Events Don't Work" (`page-172-0`).*
- **CDC vs. polling vs. outbox:** CDC for change-complete + low latency;
  polling for one-off / simple queries; transactional outbox when you own the
  source app and want atomicity.
  *Ref: Building An Event-Driven Data Mesh.md — "Bootstrapping Data Products" (`page-188-0`).*
- **Schema tech:** pick one (Avro preferred for streams; Parquet for batch).
  Multi-format sprawl needs explicit proposal and trial.
  *Ref: Building An Event-Driven Data Mesh.md — "Supporting Data Product Schemas" (`page-89-0`).*
- **Late-arrival policy:** tie implementation to the SLA so consumers stay
  resilient within its guarantees. *Ref: Building An Event-Driven Data Mesh.md — "Resolving Late-Arriving Events" (`page-241-0`).*

---

## Key Takeaways
1. Make data a first-class product owned by the producing domain, not a
   side-effect of a monolith.
2. Build on event streams with unlimited retention, partitioning by entity
   key, and tombstones — not queues, not ephemeral messaging.
3. Use *current-state* events (ECST) for cross-domain data products; reserve
   delta events for event sourcing inside a single bounded context.
4. Adopt the Kappa architecture with compaction so one stream serves both
   real-time and historical consumption.
5. Standardize via federated governance (T-shirt partition sizes, UTC-0,
   schema technology) and operationalize via a self-service platform
   (schema registry, catalog, connectors, OAuth2/IAM, lineage, monitoring).
6. Design for schema evolution: aim for full-transitive compatibility,
   explicit default values, mandatory registry checks at deploy.
7. For event-driven feeds from existing systems, meet them where they are:
   CDC, transactional outbox, or eventification — never dual-write.
8. Bake privacy and compliance in: per-consumer access control,
   end-to-end/field-level encryption, and crypto-shredding for GDPR
   "right to be forgotten."
9. Treat eventual consistency as a feature: detect lag via offsets, expose
   it to callers via 503 / stale flag / callback, and pick a documented
   late-arrival strategy per data product.
10. Use the medallion (bronze / silver / gold) quality tiers and tiered
    SLAs (Tier 1 = wake-up, Tier 4 = fix-it-next-day) so consumers can
    select data products with the right trust levels for their use case.

---

## Cross-References
- Related: `../Building_Event-driven_Microservices.md` (same author — covers
  the event-driven microservices layer that populates many data products).
- Related: `../Communication_Patterns.md` (channel/datatype routing choices
  for multi-data-product event streams).
- Related: `../Flow_Architectures.md` (continuous-flow processors that
  materialize data products).
- Topic index: `../INDEX.md`
