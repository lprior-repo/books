# Building an Event-Driven Data Mesh
**Author:** Adam Bellemare
**Topic tags:** `#architecture` `#api` `#data` `#events` `#mesh` `#kafka`
**Language focus:** language-agnostic (Java/Protobuf/SQL/Python examples)
**Sources:** `markdown_output/Building An Event-Driven Data Mesh/Building An Event-Driven Data Mesh.md` · `summaries/Building_An_Event-Driven_Data_Mesh.md`

## TL;DR
Data mesh is a sociotechnical shift that distributes ownership of data to the domains that produce it, treats data as a first-class product with SLAs and schemas, governs it via a federated team drawn from across the org, and operates it on a self-service platform. Event streams (durable, append-only, replayable logs on an event broker such as Apache Kafka) are the optimal substrate for these products: they unify real-time and historical access via the Kappa architecture, decouple producers from consumers, and power both operational and analytical use cases from the same source of truth.

---

## Best Practices by Topic

### Data Mesh Philosophy and Origin

**Principle:** Data mesh is a *lingua franca* for talking about how teams create, share, and consume data. It codifies four principles — domain ownership, data as a product, federated governance, self-service platform — and recasts data from "exhaust" into a first-class citizen.

**Do:**
- Frame data mesh as both a social and a technical shift; one without the other collapses back into the data-team bottleneck.
- Use the language of data mesh deliberately — "data product", "anti-corruption layer", "federated governance" — instead of inventing yet another "data-something-something" paradigm.
- Reuse the data communication structure (event streams) across the org; do not build parallel pipelines for "analytics" vs "operational" use cases.
- Acknowledge Zhamak Dehghani (originator of data mesh) and recognize her work as the framework you are implementing.

**Don't:**
- Don't expect the labels alone to fix bad incentives — federated governance must be backed by an institutional mandate.
- Don't promote a data product if your team can't commit to its SLA, on-call support, and deprecation plan.
- Don't introduce a new data paradigm alongside data mesh; the data communication layer terminology (Bellemare's earlier book) is subsumed by data mesh.

*Ref: Building An Event-Driven Data Mesh.md — "What Is Data Mesh?"*

---

### The Four Pillars of Data Mesh (Overview)

**Principle:** The principles hang together — domain ownership establishes *who*, data as a product establishes *what*, federated governance establishes *how*, and self-service platform establishes *who pays the tax*. Skip one and the others warp.

**Do:**
- Implement the principles together, iteratively. Even the MVP self-service platform is useful as long as it forces a real conversation about ownership, quality, and SLA.
- Tie every published data product to a named owner, a schema, an SLA tier, and a quality classification.
- Make federated governance a *real* body with representatives from each domain, an institutional charter, and a steady cadence.

**Don't:**
- Don't build a self-service platform that ignores federation; tooling without standards becomes accidental sprawl.
- Don't let "data as a product" devolve into "data the data team published without consulting consumers."

**The principle hierarchy:**
1. **Domain ownership** — sovereign producers; data is owned by the team that knows it best.
2. **Data as a product** — schemas, SLAs, quality, deprecation; built like any other product.
3. **Federated governance** — cross-cutting standards set by a team drawn from across the org.
4. **Self-service platform** — tooling that makes the right thing easy and the wrong thing hard.

*Ref: Building An Event-Driven Data Mesh.md — "Data Mesh Principles"; "What Does a Governance Meeting Look Like?"*

---

### Anti-Corruption Layer (DDD Translation Surface)

**Principle:** The anti-corruption layer (ACL) is the translation boundary between your internal bounded context and external consumers. It lets you evolve your internal model without breaking the public data contract.

**Do:**
- Translate every internal entity/aggregate into a public representation before it leaves your domain boundary.
- Treat the ACL as part of the data product contract — its shape is what consumers depend on, not your internal schema.
- Document which fields are denormalized, joined, or computed at the ACL.

**Don't:**
- Don't expose internal tables, columns, or relationships directly via the ACL.
- Don't let "just expose the internal model, we'll fix it later" take root — by then, every consumer has coupled on the internal semantics.

**What lives in the ACL:**
- Read-only views over normalized internal tables (especially from a relational DB).
- Joins across entities for aggregate-aligned products.
- Denormalized fields pre-computed for consumer convenience.
- Format conversions (internal Protobuf → public JSON, etc.).
- Schema versioning surface (the contract).

*Ref: Building An Event-Driven Data Mesh.md — "Domain-Driven Design in Brief" / Chapter 8 Eventification*

---

### Source-Aligned vs Aggregate-Aligned vs Consumer-Aligned — Decision Tree

**Principle:** Pick the right alignment type per product. Don't let alignment drift across products.

**Do:**
- Source-aligned first for any new domain — simplest, lets consumers build.
- Aggregate-aligned when ≥2 peers need the same computation.
- Consumer-aligned when one domain needs cross-product composition that no other domain needs.

**Don't:**
- Don't skip directly to consumer-aligned — it locks the producer into one customer's shape.
- Don't aggregate at the source if the components change at different rates.
- Don't denormalize data with very high update rates or very large payloads into other streams — let consumers join when they need it.

**Decision tree:**

1. Does one specific consumer need a fully custom view that combines multiple source streams? → **Consumer-aligned**.
2. Do multiple peers need the same aggregation of the source? → **Aggregate-aligned**.
3. Otherwise → **Source-aligned**.

**Trade-off summary:**
- Source-aligned: general purpose; consumer applies their own logic.
- Aggregate-aligned: domain-owner applies business logic; offloads cross-team work.
- Consumer-aligned: highly customized for one domain; doesn't fit shared use.

*Ref: Building An Event-Driven Data Mesh.md — "The Three Data Product Alignment Types"*

---

### Domain-Driven Design Foundations

**Principle:** Borrow DDD's vocabulary — *domain*, *bounded context*, *ubiquitous language*, *entity*, *aggregate*, *anti-corruption layer* — so that data ownership, boundaries, and shared vocabularies are explicit and stable.

**Do:**
- Define the boundary within which a domain model applies; that boundary contains a ubiquitous language whose terms have one canonical meaning.
- Treat *data in here* (private to the bounded context) and *data out there* (publicly coupled by data products) as fundamentally different.
- Choose entities and aggregates as the natural candidates for first data products — they are the most stable units of meaning.
- Expose anything outside your domain via the *anti-corruption layer* so external parties don't couple directly on your internal model.

**Don't:**
- Don't share the internal implementation model with downstream consumers — always expose the data through an anti-corruption layer.
- Don't let the same term (e.g., "user", "account") drift in meaning across two bounded contexts without explicitly standardizing the polyseme.

**Glossary:**
- **Domain** — area of interest/control; entities + aggregates + business logic + context.
- **Bounded context** — boundary within which the domain model applies; contains the ubiquitous language.
- **Ubiquitous language** — terms whose meaning is consistent inside the bounded context only.
- **Entity** — uniquely identifiable thing/item within a domain (object with unique attributes).
- **Aggregate** — cluster of entities treated as a single unit (e.g., order = coupons + items + deals + shipping + payment).
- **Anti-corruption layer** — translation surface that prevents external coupling on your internal model.

*Ref: Building An Event-Driven Data Mesh.md — "Domain-Driven Design in Brief"*

---

### Producer Responsibility Checklist

**Principle:** Data product ownership is a full-time commitment. It includes publication, evolution, support, and retirement.

**Do:**
- Define and publish the schema.
- Maintain SLA and quality tier.
- Provide on-call support (proportional to tier).
- Communicate deprecation with adequate lead time.
- Manage consumer relationships (notifications, escalations).
- Document the contract (fields, semantics, edge cases).
- Provide test event generators.

**Don't:**
- Don't ship a data product without documentation.
- Don't take ownership without on-call budget.
- Don't deprecate without a migration plan.
- Don't change semantics without versioning or notifying consumers.

**Lifecycle stages:** Draft → Published → Deprecated → Retired.

*Ref: Building An Event-Driven Data Mesh.md — "Principle 2: Data as a Product" / "Establishing Data Product Life Cycle Requirements"*

---

### Domain Ownership (Principle 1)

**Principle:** Whoever produces the data is responsible for publishing it as a discoverable, well-described, SLA-backed data product. Sovereignty over the domain includes responsibility for its export shape.

**Do:**
- Ask prospective consumers what they need *before* designing the data product. Treat it as a customer-focused, consultative exercise.
- Enumerate the entities and aggregates that your domain owns, then ask consumers which of those they actually need (you'll be surprised how few).
- Document the responsibilities the producer takes on: schema evolution, on-call, deprecation communication, quality metrics.
- Use DDD's vocabulary to set explicit boundaries and ownership — don't rely on tribal knowledge.

**Don't:**
- Don't reach into another team's database or event stream to "grab what you need" — that's the failure mode this principle is designed to eliminate.
- Don't assume the producer knows what's needed; consumers will reveal requirements that don't surface in the producer's own road map.
- Don't break down the responsibility: if you own the data, you own the schema, the SLA, the on-call, and the deprecation.

**Selection criteria for what to expose:** Start with entities (often good first candidates). Add aggregates (often the natural unit). Add select foreign relationships (e.g., payment info as its own data product, linked by unique ID mappings).

*Ref: Building An Event-Driven Data Mesh.md — "Principle 1: Domain Ownership"; "Selecting the Data to Expose from Your Domain"*

---

### Data as a Product (Principle 2)

**Principle:** Treat data with the same rigor as any product: dedicated ownership, minimum quality, SLAs, feature request handling, and lifecycle management.

**Do:**
- Provide a stable API (event schema), a service tier, a quality bar, and a deprecation plan — for *every* data product.
- Decide what kind of product each one is at design time: source-aligned, aggregate-aligned, or consumer-aligned.
- Ensure the public model is decoupled from the internal implementation via the anti-corruption layer.
- Treat data as a formal commitment: time, resources, and know-how to make domain data usable to external customers.

**Don't:**
- Don't expose your internal schema as the data product's contract — your internal model must be free to evolve.
- Don't publish without a consumer story ("who uses this, and for what decision or action?").
- Don't ship a data product without specifying its SLA tier, quality tier, and deprecation plan.

**Four major factors to consider when building data products:**
1. **Immutable and time-stamped** — so consumers obtain consistent, reproducible results.
2. **Multimodal** — event stream, batch Parquet, REST API; choose per use case.
3. **Push or pull access** — push (subscribe) for real-time; pull (REST/Parquet) for ad-hoc queries.
4. **Alignment type** — source-, aggregate-, or consumer-aligned.

*Ref: Building An Event-Driven Data Mesh.md — "Principle 2: Data as a Product"; "The Three Data Product Alignment Types"*

---

### Immutable, Time-Stamped Data Products

**Principle:** A data product must be immutable and time-stamped so that any query — today or in a year — returns the same answer for the same range of events.

**Do:**
- Publish new events for corrections; never mutate past events.
- Stamp every event with the time of occurrence (event time), not just the producer's wall-clock write time.
- Decide a policy for late-arriving events up front: publish-as-soon-as-known, drop, or grace period + drop.
- Treat any modification to a published data set as a new, incremental event.

**Don't:**
- Don't expose mutable query APIs as the data product — they can't be replayed or reconciled later.
- Don't assume wall-clock ordering is the same as event-time ordering.

**Why immutability + time-stamping unlocks reproducibility:** A query today on a given date range and the same query in a month must yield identical results. Two separate consumers reading the same data product must obtain precisely the same data. This is only achievable if the data is immutable and time-stamped.

*Ref: Building An Event-Driven Data Mesh.md — "Data Products Provide Immutable and Time-Stamped Data"*

---

### Multimodal Data Products

**Principle:** One logical data product may have multiple ports (event stream, batched Parquet files, REST API). Decide which to support *before* building self-service around them.

**Do:**
- Support the smallest number of modes your consumers actually need (often: just event streams, plus Parquet for analytics).
- Document each mode of the same data product as one canonical product with multiple ports — singular ownership, multiple delivery mechanisms.
- Treat new modes as candidates for federation-wide standards via the governance team before adding them.

**Don't:**
- Don't enable every mode "just in case" — every supported mode is a maintenance, security, and access-control surface.
- Don't claim two products are "the same product just on different ports" if they have different owners.

**Typical multimodal example:**
- Same product produced to an event stream (real-time updates).
- Same data composed into Parquet files in cloud storage (batch analytics).
- Same data optionally exposed via REST API (request-response clients).

*Ref: Building An Event-Driven Data Mesh.md — "Data Products Are Multimodal"; "Supporting Multimodal Data Product Types"*

---

### Push vs Pull Access

**Principle:** Push (subscribe) creates self-updating consumers; pull (REST/Parquet) creates bespoke queries. The choice ripples across the organization — *like begets like*.

**Do:**
- Default to push (event stream) for real-time operational and analytical needs.
- Use pull for ad-hoc data science over historical data or for cases where push is inappropriate.
- When both are needed, expose both from the same source-aligned event stream via sink connectors.

**Don't:**
- Don't use pull APIs to serve hot-path operational decisions — you'll poll too aggressively and grow query load.
- Don't mix a push product with consumers who expect a pollable API; they will rebuild a streaming offset on top.

**Pull API overhead:** Tight-polling loops on a relational DB for new records every second will make DBAs deeply uncomfortable. Push (event streams) have very low overhead for managing consumer subscriptions.

**Like begets like:** The more data products served via pull APIs, the more pull APIs you'll have. The more push, the more push. The choice you make ripples across the org, not just your immediate consumers.

*Ref: Building An Event-Driven Data Mesh.md — "Accessing a Data Product Via Push or Pull"*

---

### The Three Data Product Alignment Types

**Principle:** Source-aligned = raw public state; aggregate-aligned = pre-aggregated; consumer-aligned = customized for a single domain.

**Do:**
- Start with source-aligned products; they're simple and let consumers build whatever they need.
- Promote a successful consumer-aligned aggregation *upstream* into an aggregate-aligned product when peers start replicating the same computation.
- Consult your governance team before standardizing on alignment types and naming.

**Don't:**
- Don't denormalize *everything* into a source-aligned product — leave highly dynamic or large-payload dimensions for separate products.
- Don't require every consumer to use aggregate or consumer-aligned products if source-aligned would do.

**Code (source-aligned sales event):**
```
Value: {
 sales_id: 8675309,
 item_ids: [4625382, 4625382, 4625382, 100900],
 total_usd: 89.12,
 datetime: "2022-11-12T03:51:19Z",
 shipping_address: "123 Fake Street, Springfield"
}
```
*Ref: Building An Event-Driven Data Mesh.md — "The Three Data Product Alignment Types"*

**Code (aggregate-aligned daily sales):**
```
Value: {
 date: "2022-11-12",
 total_items_sold: 41292,
 total_items_value_usd: 1902712.22
}
```

**Code (consumer-aligned ad-targeting):**
```
Value: {
 user_id: "UUID-123456789",
 predicted_item_ids_to_advertise: [4625382, 100901],
 cost_tolerance: "high",
 conversion_probability: 0.1233,
 estimated_spend_usd: 500.00,
 ad_bid_limit_usd: 9.75
}
```

**Trade-offs between alignments:**
- Source-aligned: easy to construct; consumers apply their own logic; general purpose.
- Aggregate-aligned: reduces cross-team duplication; consumers can rely on a single source of truth.
- Consumer-aligned: highly customized for one domain; useful when no single producer could have provided it.

*Ref: Building An Event-Driven Data Mesh.md — "The Three Data Product Alignment Types"*

---

### Federated Governance (Principle 3)

**Principle:** A team with mandate and representation sets cross-cutting standards (schemas, formats, access, security) instead of mandating implementation choices.

**Do:**
- Form a charter that covers data concerns, technology concerns, legal/security concerns, and self-service platform concerns.
- Pull domain representatives into the group; rotate them every few months to spread context.
- Drive decisions through the propose → review → implement → archive lifecycle, with archived proposals visible to all.
- Pick tooling based on existing technical debt, not theoretical merit.

**Don't:**
- Don't dictate implementation languages for everyone.
- Don't skip legal/compliance when scoping data products; bake encryption and PII handling into tooling defaults.
- Don't let standards proliferate — the governance team is the cabinet for choosing what stays in the toolbox.

**Code (real-world permission request):**
```
Hi Seedle!

Can you please add the following Kafka permissions to our microservice?

service name: ShippableOrdersResolver

topic name: Shopping.Orders.v1 permissions: read, describe

topic name: Shopping.Payments.v2 permissions: read, describe

topic name: Sales.ShippableOrders.v1

permissions: write, describe

Thanks!
```
*Ref: Building An Event-Driven Data Mesh.md — "Federated Governance"; "Forming a Federated Governance Team"; "Implementing Standards"; "What Does a Governance Meeting Look Like?"*

**Charter domains:**
- Data concerns: metadata, schemas, support, discoverability, lineage, quality, interoperability.
- Technology concerns: languages, frameworks, processes.
- Legal, business, security concerns: regulatory compliance, financial, PII, internal security.
- Self-service platform concerns: monitoring, logging, access controls, compute, storage.

**Governance meeting flow (five-step):**
1. Identify existing problems (cards/sticky notes; cluster; prioritize).
2. Draft proposals (problem framing; proposed solution; scope).
3. Review proposals (individual review; group discussion; vetting).
4. Implement proposals (work-ticket decomposition; iterative delivery).
5. Archive proposals (cloud file drive; transparency; revisitable).

*Ref: Building An Event-Driven Data Mesh.md — "Forming a Federated Governance Team"; "What Does a Governance Meeting Look Like?"*

---

### Metadata Standards and Required Fields

**Principle:** A data product cannot be discovered, trusted, or routed without minimum metadata. Enforce registration-time metadata requirements so that only well-defined products reach the catalog.

**Do:**
- Mandate: domain/owner (a real human), tiered SLA (Tier 1–4), quality classification (bronze/silver/gold), PII/financial tags, schema URI.
- Apply tags so governance policies can run automatically per-tag (e.g., "PII consumer must show compliance").
- Make minimum upstream tiers a gate for production use: "Tier 1 services may depend on Tier 1 or Tier 2 only."

**Don't:**
- Don't let "all data is Tier 1" creep in — reserve Tier 1 for get-out-of-bed-on-call material.
- Don't treat quality tier as orthogonal to SLA: a gold-tier consumer can still depend on bronze tier upstream, that's fine.

**Tier definitions:**
- **Tier 1:** Critical; failure impacts customers/finances; 24-hour on-call.
- **Tier 2:** Important; failure degrades but doesn't prevent customer interaction; often real-time ops.
- **Tier 3:** Background; not visible to consumers; intervention if time-sensitive.
- **Tier 4:** Largest recovery window; can wait until next business day.

**Quality tier definitions:**
- **Bronze:** Unstructured or raw; may couple to internal model; intermittent quality.
- **Silver:** Well-structured, sanitized, denormalized; ~99.99% pass rate.
- **Gold:** Authoritative; rigorously tested; ~99.9999% pass rate.

**Upstream dependency rule:** A service cannot offer Tier 1 support when it depends on Tier 4 products. Convention: only Tier 1 or Tier 2 SLA guarantees in production.

*Ref: Building An Event-Driven Data Mesh.md — "Metadata Standards and Requirements"*

---

### Cross-Domain Compatibility and Interoperability

**Principle:** Without explicit interop rules, every team builds the same foreign keys, partition sizes, and time zones differently — and consumers spend more time reconciling than using.

**Do:**
- Standardize common entities (e.g., `base_user`, `base_item`) in a shared schema repo and `import` them across products.
- Choose a T-shirt partition sizing convention (1/4/8/16/32/64/256) and pick the size that matches other products keyed on the same entity.
- Require UTC-0 timestamps and timezone metadata on aggregate-aligned products.
- Use a primitive (string, int, long) for event keys, preferably the common entity's unique ID.

**Don't:**
- Don't use a custom partitioner when consumers must join across streams — use a shared partition-assignment algorithm.
- Don't let domain-specific foreign keys (auto-increment long vs string UUID) leak across products; standardize once at the federation.
- Don't invent partition sizes per stream — pick T-shirt sizes that match products on the same entity.

**Code (common entity imports):**
```
package myorg.common;
message base_user {
 String uuid = 1;
}
```
```
import "common_schemas/base_user.proto"
import "common_schemas/base_item.proto"
import "google/protobuf/timestamp.proto";
message user_clicked_on_item {
 myorg.common.base_user user = 1;
 myorg.common.base_item item = 2;
 google.protobuf.Timestamp timestamp = 3;
 String websiteURI = 4;
}
```

**Hot partition warning:** Be careful about disproportionate event distribution to a single partition. 99% on one partition = bad key space or bad partitioner.

*Ref: Building An Event-Driven Data Mesh.md — "Ensuring Cross-Domain Data Product Compatibility and Interoperability"; "Common Entities"; "Event Stream Keying and Partitioning"; "Time and Time Zones"*

---

### Data Security and Access Policies

**Principle:** Defense in depth — disable by default, encrypt in motion and at rest, and never trust data without an access decision.

**Do:**
- Disable data product access by default; require explicit registration as a consumer.
- Use a KMS for keys; consider end-to-end encryption for highly sensitive data.
- Restrict sensitive PII to consumers with documented infosec approval; field-level encryption preserves utility for analytics while preserving confidentiality.
- Audit access logs for all PII data products.

**Don't:**
- Don't broadcast access to "read-only data" without registration — you lose lineage and provenance.
- Don't invent your own encryption; use purpose-built crypto formats and a managed KMS.
- Don't store decryption keys on the same backend as decrypted data.

**Code (Table 4-1 — field-level encryption example):**

| Field name | Original event      | Partially encrypted event |
|------------|---------------------|---------------------------|
| email      | adam@bellemare.com  | n2Zl@p987NhB4.L0P         |
| user       | abellemare          | 9ajkpZp2kH                |
| account    | VD8675309           | 0PlwW81Mx                 |
| amount     | \$777.77            | \$777.77                  |
| datetime   | 2022-02-22:22:22:22 | 2022-02-22:22:22:22       |

*Ref: Building An Event-Driven Data Mesh.md — "Disable Data Product Access by Default"; "Consider End-to-End Encryption"; "Field-Level Encryption"*

**Format-preserving encryption:** Maintains the original field's format (alphanumeric, spacing, character count) without exposing PII — useful when applying encryption after the fact because schemas don't need renegotiation.

---

### Privacy, GDPR, and Crypto-Shredding

**Principle:** Immutable event streams make GDPR "right to be forgotten" hard *unless* data is encrypted with a key the data subject can revoke (crypto-shredding).

**Do:**
- Encrypt PII fields, hold keys in a KMS, and expose only the decryption key to consumers who need PII.
- On a deletion request, delete (shred) the key — every historical event becomes unreadable without re-processing any storage tier.
- Keep non-PII fields in the same event intact so downstream aggregates retain utility.

**Don't:**
- Don't try to delete from immutable storage as the primary mechanism — backups, offsite tapes, and tiered storage make that brittle.
- Don't store decryption keys on the same backend as decrypted data — defeats the purpose.
- Don't let consumers hold decrypted keys longer than necessary — apply tight retention (e.g., 10 minutes) before re-requesting.

**Why crypto-shredding beats deletion:**
- Large amounts of data exist in backups, tape drives, cold cloud storage — searching and deleting is expensive.
- Partial deletion (PII only) still leaves utility for analytics on the remaining fields.
- Deletion across multiple systems is slow and error-prone — key deletion is instant.

*Ref: Building An Event-Driven Data Mesh.md — "Data Privacy, the Right to Be Forgotten, and Crypto-Shredding"*

---

### Data Product Lineage

**Principle:** Lineage must be derivable from real permissions and identity, not from opt-in self-reporting.

**Do:**
- Build topology-based lineage from real ACLs and client identities (the source of truth is what they actually use).
- Track both *current* and point-in-time lineage so audits and impact analyses work.
- Use record-based lineage only when required by regulation; be honest about its cost (joins, aggregations, multi-consumer fanout are hard).

**Don't:**
- Don't rely on voluntary self-reporting — gaps will silently corrupt the topology graph.
- Don't claim lineage you can't back up with an actual read or write audit record.
- Don't pick record-based lineage by default — its complexity grows with consumer fanout, joins, and transformations.

**Topology vs record-based lineage:**
- **Topology-based:** graph of data products and their consumers; derived from real ACLs; cheap.
- **Record-based:** tracking a single record through services; requires per-record metadata; expensive at scale.

*Ref: Building An Event-Driven Data Mesh.md — "Data Product Lineage"; "Topology-Based Lineage"; "Record-Based Lineage"*

---

### Self-Service Platform (Principle 4)

**Principle:** Make the right thing easy and the wrong thing hard — for the data product owner and the data product consumer.

**Do:**
- Start with a minimum viable platform: event broker + schema registry + minimal catalog + a connector service.
- Fulfill the three user roles: prospective consumers (find/subscribe), creators (publish/test/deploy), owners (manage lifecycle, deprecation).
- Use what your organization already runs (CI/CD, identity, KMS) — don't reinvent.

**Don't:**
- Don't build Level-3 features before Level-2 pain is real. YAGNI: build when usage tells you to.
- Don't be a heavy-handed gatekeeper — the platform's job is to make compliance effortless, not to inspect every commit.

*Ref: Building An Event-Driven Data Mesh.md — "Principle 4: Self-Service Platform"; "The Self-Service Platform Maturity Model"; "Providing Self-Service Through SaaS"*

---

### Self-Service Platform Maturity Levels

**Principle:** Build the platform in three levels — MVP, EP, MP — and only progress when pain drives it.

**Do:**
- MVP (Level 1): event broker, schema registry, spreadsheet-as-catalog, connector service (Kafka Connect).
- EP (Level 2): real data catalog, data product management UI, service/user identities, basic ACLs, stream processing.
- MP (Level 3): unified IAM via OAuth2/OIDC, programmatic management API, monitoring/alerting, multiregion/multicloud.
- Keep the loop tight: each level must solve at least one outstanding pain point.

**Don't:**
- Don't try to deliver MP on day one — the gap to MVP is too far, and you'll never start.
- Don't let MVP sprawl — by Level 2 you must enforce identities, otherwise you'll never reach MP.
- Don't treat levels as a strict sequence — implement Level-3 features from Level-2 systems if pain demands.

**Example spreadsheet (Table 5-1):**

| Name          | Topic       | Bootstrap URI       | Owner       | SLA    | Quality | Schema URI     | Description                                                   |
|---------------|-------------|---------------------|-------------|--------|---------|----------------|---------------------------------------------------------------|
| Sales         | gold_sales  | k1.brk.kek:9093     | @bondolabs  | Tier 1 | Gold    | ../gold_sales  | Canonical sales data, including sanitized payment types       |
| Orders        | gold_orders | k1.brk.kek:9093     | @smahmood   | Tier 1 | Gold    | ../gold_orders | Canonical orders data, excluding PII                          |
| Page views    | page_views  | x3.brk.uwu:9093     | @vsalamanca | Tier 3 | Bronze  | ../page_views  | Page view metrics piped in from Google Analytics             |

*Ref: Building An Event-Driven Data Mesh.md — "Level 1: The Minimal Viable Platform"; "Level 2: The Expanded Platform"; "Level 3: The Mature Platform"*

---

### Event Streams as the Foundation of Data Mesh

**Principle:** Event streams (durable, append-only, replayable logs hosted by an event broker) are the optimal substrate for data products because they power real-time and historical access from one place.

**Do:**
- Use event streams as the default product mode for both operational and analytical use cases.
- Provide all four essentials: immutable, durable/replayable, scalable, indefinite storage.
- Lean on event ordering, partitioning, and key-based locality for downstream ops.

**Don't:**
- Don't use ephemeral messaging or queue-based delivery for data products — both lack replay and indefinite retention.
- Don't assume the queue is "close enough" to a log; it isn't.

**The four essential properties of an event stream:**
- Immutable: events cannot be modified once written; only new events may be added.
- Durable and replayable: events are durable for both immediate and future consumption; consumers can replay as needed.
- Scalable: high availability, scalability, indefinite retention.
- Append-only log: the underlying data structure permits only appending; written data cannot be altered.

*Ref: Building An Event-Driven Data Mesh.md — "Event Streams for Data Mesh"; "What's an Event Stream? What Is It Not?"*

---

### Events, Messages, and Records

**Principle:** Avoid "message" — use "event" or "record". A message implies a private recipient; an event is broadcast and replayable.

**Do:**
- Use a key/value/header structure for events. The key enables partitioning and locality; the value carries the data; the header carries metadata (timestamps, tracing IDs).
- Partition by key so all events of the same key land on the same partition.
- Make events immutable — never mutate; always emit a new corrected event.

**Don't:**
- Don't use the term "message" in products, code, or runbooks; it causes confusion and doubt about durability semantics.
- Don't return an event that's merely a signal — every event must carry the data.

**Code (key/value/header event example):**
```
Key: 12309131238218
Value: {
 status: "NEW_MESSAGE"
 source: "messaging_app"
 application_uri: "/user/chat/192873163812392"
}
```
*Ref: Building An Event-Driven Data Mesh.md — "Events, Messages, and Records"*

**Event structure components:**
- **Key:** Optional but useful; unique ID; partitions events of the same key.
- **Value:** Bulk of the data; well-defined schema.
- **Header (record properties):** Metadata (timestamps, tracking IDs, custom fields).

---

### Event-Carried State Transfer (ECST)

**Principle:** State events carry the full *current public state* of an entity. Each consumer materializes its own copy via ECST, decoupling data ownership from data access.

**Do:**
- Use current-state events by default — they're lean, simple, compactable, and agnostic to the reason for change.
- Ingest, materialize, and aggregate from the stream instead of reaching into the source database.
- Place consumers and producers on the same partitioning basis so a state event and a downstream entity event land on the same partition.

**Don't:**
- Don't use before/after state events as a default — they complicate compaction and roughly double storage and network traffic.
- Don't expose internal transitions ("why" the state changed) — they couple consumers to the source's internal semantics.

**ECST pattern:** A state event contains the entire *public state* of an entity at the time it was created — like a row in a DB table. Any change results in a new event with a full copy of the updated state. Consumers re-create the state through *materialization*.

*Ref: Building An Event-Driven Data Mesh.md — "State Events and Event-Carried State Transfer"; "Current State Events"; "Before/After State Events"*

---

### Materialization and Aggregation

**Principle:** Materialization is reading an event and merging it into a local store. Aggregation composes multiple state events into a new derived entity.

**Do:**
- Store only the subset of event data your service actually needs — keep the consumer footprint small.
- Build your own aggregates from source-aligned data; promote them to aggregate-aligned products only when peers converge on the same computation.
- Use the event broker's stream time/offsets to reason about consumer progress.

**Don't:**
- Don't maintain more materialized state than necessary — disk is cheap, but the cognitive cost of caching invalid data is high.
- Don't compute the same aggregation in N downstream teams — promote it to a shared aggregate-aligned product.

**Operational freedom from local aggregation:** Consumers can change their computation and replay the event stream to rebuild results instead of relying on the upstream owner to redefine aggregates. The trade-off: you must do the work; the benefit: you can evolve independently.

*Ref: Building An Event-Driven Data Mesh.md — "Materializing Events"; "Aggregating Events"*

---

### Kappa Architecture

**Principle:** Use the event stream as the single source of both current and historical data. Restart consumers from offset zero and replay — don't run parallel batch/speed layers.

**Do:**
- Rely on indefinite retention and replays for historical rebuilds.
- Snapshot+offset a consumer's local state and offsets so it can resume after a failure.
- Choose a single processing framework (Flink, Kafka Streams, Spark) that can do both real-time and batch replay.

**Don't:**
- Don't stand up separate batch and speed layers (Lambda) for data products — the seams multiply unreconcilably.
- Don't *pretend* to do Kappa with a broker that has a retention cap — you'll eventually need historical data you don't have.

**Code (Kappa with Kafka Streams):**
```java
StreamsBuilder builder = new StreamsBuilder();
//Materialized state of the "inventory" stream
KTable inventory = builder.table("inventory")
//Materialized state of the "items" stream
KTable sales = builder.table("items")
//Join events on primary key and apply custom business logic
//Note that inventory and items need to be keyed on the same itemId
KTable enrichedItemInventory = inventory.join(items, ...)
```

**Code (Kappa with Flink SQL):**
```sql
CREATE TABLE Inventory (
 item_id VARCHAR,
 quantity BIGINT,
 timestamp TIMESTAMP(3),
 PRIMARY KEY (item_id) ENFORCED,
) WITH (
 'connector' = 'kafka',
 'topic' = 'inventory',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'my_app_group_id',
 'format' = 'avro',
 'scan.startup.mode' = 'earliest-offset'
);
CREATE TABLE Items (
 item_id VARCHAR PRIMARY KEY,
 name VARCHAR,
 description VARCHAR,
 brand VARCHAR,
 timestamp TIMESTAMP(3),
 PRIMARY KEY (item_id) ENFORCED,
) WITH (
 'connector' = 'kafka',
 'topic' = 'items',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'my_app_group_id',
 'format' = 'avro',
 'scan.startup.mode' = 'earliest-offset'
);
CREATE TABLE Enriched_Item_Inventory AS
 SELECT *
 FROM INVENTORY
 INNER JOIN ITEMS
 ON ITEMS.item_id = INVENTORY.item_id;
```

*Ref: Building An Event-Driven Data Mesh.md — "The Kappa Architecture"*

---

### Lambda Architecture Anti-Pattern

**Principle:** The Lambda architecture fails at scale for data mesh because each data product introduces its own *seam* between batch and stream, and reconciling seams is exponential.

**Do:**
- Migrate Lambda-style solutions to Kappa as soon as your broker supports indefinite retention.
- Treat seam reconciliation as a dead-end signal — you're scaling the wrong thing.

**Don't:**
- Don't run a speed layer alongside a batch layer as a long-term strategy — N data products → N² pairs of seams.
- Don't maintain two codepaths for read and write in producer and consumer.

**Why Lambda doesn't scale for data mesh:**
- Producer maintains two code paths (batch insertion + event publishing); non-atomic.
- Consumer maintains two code paths (batch resolution + stream resolution); non-convergent.
- Batch and stream data models must evolve in sync.
- Merging multiple Lambda data products multiplies seams: 2 → 4; 3 → 8; N → 2^N.

*Ref: Building An Event-Driven Data Mesh.md — "The Lambda Architecture and Why It Doesn't Work for Data Mesh"*

---

### Supporting the Kappa Architecture

**Principle:** Kappa requires indefinite retention, infinite storage, compaction, and tombstones. Confirm your broker provides all four.

**Do:**
- Choose a broker with unlimited retention (Kafka, Pulsar) — Kinesis/Event Hubs/Pub/Sub are capped.
- Configure compaction lag long enough to cover outages and weekend restart windows (often >24h default).
- Use tombstones for deletes so compaction can remove older entries.

**Don't:**
- Don't pick a broker with retention caps for a data mesh — you'll eventually need history you can't get back.
- Don't try to backdoor "delete" via before/after events; brokers can't compact a non-null value with a null `after`.

**Code (Kafka topic config for compaction):**
```
{'$topic': 'users',
 'retention.ms': -1,
 'cleanup.policy': 'compact',
 'min.cleanable.dirty.ratio': 0.5,
 'segment.ms': 3600000,
 'min.compaction.lag.ms': 86400000}
```

*Ref: Building An Event-Driven Data Mesh.md — "Supporting the Requirements for Kappa Architecture"; "Compaction"; "Deletions"*

**Compaction semantics:** Compaction deletes older events for a given key if a newer event with the same key exists in the partition. Tombstones (key + null value) signal deletion. Compaction lag is the minimum age before an event can be compacted; default 24h, often increased for weekend-restart safety.

---

### Selecting an Event Broker

**Principle:** Choose a broker with unlimited retention, scalable throughput, tool ecosystem, and operational maturity. Retention is a deal-breaker.

**Do:**
- Default to Apache Kafka (or Confluent Cloud) for proven durability and community.
- Verify tiered storage (KIP-405) is available if you need truly massive retention.
- Check support for schema registry, code generators, processing frameworks, and catalog integration.

**Don't:**
- Don't pick a cloud-only broker with hard retention caps (Kinesis: 365 days, Event Hubs Premium: 90 days, Pub/Sub: 31 days) for a data mesh.
- Don't pick an obscure broker — you need engineering talent and a community.

**Table 3-1 (broker retention):**

| Broker name                  | Retention period |
|------------------------------|------------------|
| Kafka                        | Unlimited        |
| Pulsar                       | Unlimited        |
| Amazon Kinesis               | 365 days         |
| Microsoft Event Hubs Premium | 90 days          |
| Google Pub/Sub               | 31 days          |

*Ref: Building An Event-Driven Data Mesh.md — "Selecting an Event Broker"*

**Event broker selection criteria:**
- Unlimited durable data capacity.
- Scalability (throughput, clients, write-one/read-many performance).
- Support tooling (schema registry, metadata catalog, governance, lineage).
- Broker-as-a-service option (Confluent Cloud, etc.).
- Retention period (must be unlimited for data mesh).

---

### Event Schemas

**Principle:** A schema is the *contract* between producer and consumer. Without explicit schemas, you have tribal knowledge and brittle implicit contracts.

**Do:**
- Pick one schema framework (Avro, Protobuf, or JSON Schema) and stick to it across the org.
- Embed documentation (`doc` fields, comments) directly in the schema.
- Generate typed classes from the schema for compile-time safety.
- Keep schemas public and versioned alongside the data product.

**Don't:**
- Don't use schemaless JSON for data products — interpretation becomes each consumer's problem.
- Don't ship a producer without a schema registry gate that rejects incompatible writes.

**Code (Protobuf Person schema):**
```protobuf
message Person {
 //The person's unique ID
 int32 id = 1;
 //The person's full legal name
 string name = 2;
 //Measured in centimeters, rounded to the nearest centimeter
 int32 height = 3;
 enum CountryCode {
  ABW = 0;
  AFG = 1;
  ...
  ZWE = 248;
 }
 //ISO3166-1-alpha-3 standard. AAA=OTHER
 CountryCode country = 4;
}
```

**Code (Avro Person schema):**
```json
{
 "type": "record",
 "name": "Person",
 "namespace": "com.event.driven.datamesh",
 "doc": "Example of a Person record",
 "fields": [
  {
   "name": "id",
   "type": "integer",
   "doc": "The person's unique ID"
  },{
   "name": "name",
   "type": "string",
   "doc": "The person's full legal name"
  },{
   "name": "height",
   "type": "integer",
   "doc": "Measured in centimeters, rounded to the nearest centimeter"
  },{
   "name": "countryCode",
   "type": "enum",
   "symbols": ["AAA", "ABW", ... "ZWE"],
   "doc": "ISO3166-1-alpha-3 standard. AAA=OTHER"
  }
 ]
}
```

**Code (JSON Schema Person):**
```json
{
 "$id": "https://example.com/person.schema.json",
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "title": "Person",
 "type": "object",
 "properties": {
  "id": { "type": "number", "description": "The person's unique ID" },
  "name": { "type": "string", "description": "The person's full legal name" },
  "height": {
   "type": "number",
   "description": "Measured in centimeters, rounded to the nearest centimeter",
   "minimum": 1,
   "maximum": 300
  },
  "countryCode": {
   "type": "string",
   "enum": ["AAA", "ABW", ... "ZWE"],
   "description": "ISO3166-1-alpha-3 standard. AAA=OTHER"
  }
 }
}
```

**Why explicit schemas matter:**
- Standardized data contract — producers blocked from sending malformed data.
- Foundation for discussion — explicit schemas enable productive PR review.
- Code generation — typed classes in each consumer language.
- Schema evolution — controlled change with backward/forward/full compatibility.
- Test event generators — produce sample events matching schemas for testing.

*Ref: Building An Event-Driven Data Mesh.md — "Event Schemas"; "What Is a Schema?"*

---

### Schema Evolution: Backward / Forward / Full

**Principle:** Evolve schemas by adding fields with defaults (backward) and supporting readers of newer schemas (forward). Aim for full-transitive compatibility when possible.

**Do:**
- Add fields with sensible defaults (text: empty string, number: 0, enum: an "OTHER" sentinel).
- Enforce compatibility rules at the schema registry — reject breaking writes.
- Document compatibility level per topic.

**Don't:**
- Don't delete a non-nullable field without a default — old readers will fail.
- Don't rely on full compatibility when you really have a breaking change — negotiate, then migrate.

**Compatibility modes:**
- **Backward:** New schema reads old data. Achieved by removing fields (old readers can't access removed data; new readers ignore missing data).
- **Forward:** Old schema reads new data. Achieved by adding fields with defaults (old readers get default for missing field).
- **Full:** Convertible both forward and backward simultaneously.
- **Full-transitive:** Convertible between any two versions in the stream — strongest guarantee.

**Code (Avro backward-compatibility example):**
```json
{
 "type": "record",
 "name": "Example",
 "doc": "This is Version 1, but with a default value for foobar",
 "fields":
 [
 {
  "name": "id",
  "type": "integer"
 },{
  "name": "foobar",
  "type": "string",
  "default": "DEFAULT_VALUE_STRING"
 }
 ]
}
```

**Default value semantics:** In Avro/Protobuf/JSON Schema, default values are populated at *read time*, not write time. They apply only when the field is missing from the record.

*Ref: Building An Event-Driven Data Mesh.md — "Schema Evolution: Changing Your Schemas Through Time"*

---

### Negotiating a Breaking Schema Change

**Principle:** When evolution can't keep up with the domain shift, treat the breaking change as a *negotiation* — design, iterate with consumers, schedule, deprecate, execute.

**Do:**
- Step 1: Design the new data model alongside existing consumers and the federation governance team.
- Step 2: Iterate with existing consumers; involve governance for the first few breaches.
- Step 3: Create release schedule + data migration plan + deprecation plan.
- Step 4: Execute; run both old and new data products during the migration window.
- Document `deprecation` tags on the old product; block new consumers.

**Don't:**
- Don't surprise consumers with breaking changes — communicate early.
- Don't run old and new products indefinitely — noncompliance is the common failure mode.

**Code (User → User_v2 breaking change):**
```json
{
 "type": "record",
 "name": "User_v2",
 "namespace": "user.namespace",
 "fields": [
  { "name": "first_name", "type": "string" },
  { "name": "last_name", "type": "string" },
  { "name": "home_address",
  "type": {
  "type" : "record",
  "name" : "Address",
  "namespace": "user.namespace.inner",
  "fields" : [
  {"name": "phone_number", "type": ["null", "string"]},
  {"name": "address", "type": "string"},
  {"name": "city", "type": "string"},
  {"name": "country", "type": "string"}
  ]
  }
  }, {
  "name": "work_address",
  "type": "user.namespace.inner.Address"
  }
 ]
}
```

**Migration window recommendation:** 8–12 weeks of running both old and new data products. Coordinate migration; noncompliance should escalate via the federation governance team.

*Ref: Building An Event-Driven Data Mesh.md — "Negotiating a Breaking Schema Change"*

---

### Schema Registry as Gatekeeper and Documentation

**Principle:** Use the schema registry as both a gate (rejecting incompatible writes) and a discovery surface (humans can browse schemas).

**Do:**
- Store schema IDs once per event, not the entire schema, to shrink event payload size.
- Configure the registry to enforce compatibility rules (backward/forward/full) at write time.
- Treat the registry as a discoverable artifact: searchable, documented, with notifications on change.

**Don't:**
- Don't ship events with the schema embedded in every record — huge waste.
- Don't let anyone bypass the registry and submit ad-hoc events to a topic.

**Confluent Schema Registry default:** Replaces schema with a 5-byte prefix for compact event payloads.

**Beyond gating, the registry provides:**
- Data discovery (humans/search tooling query schemas).
- Schema evolution validation (rejects breaking writes).
- Automatically updated documentation (schemas carry `doc` fields).
- Downloadable schemas for code generation.

*Ref: Building An Event-Driven Data Mesh.md — "The Role of the Schema Registry"*

---

### Managing Schemas in Code

**Principle:** Keep the schema with the producer code; share common entities through a central schemas repo.

**Do:**
- Store the data product's schema alongside its producing service's code, so PRs review schema changes alongside business logic.
- Pull shared entities (`base_user`, `base_item`, timestamp) from a central common-schemas repo.
- Make each consumer approve schema changes that affect them.

**Don't:**
- Don't centralize all schemas in one mega-repo — schema ownership becomes unclear.
- Don't release schema changes without explicit consumer review.

**Schema composition code (Protobuf):**
```protobuf
import "common_schemas/base_user.proto"
import "common_schemas/base_item.proto"
import "google/protobuf/timestamp.proto";
message user_clicked_on_item {
 myorg.common.base_user user = 1;
 myorg.common.base_item item = 2;
 google.protobuf.Timestamp timestamp = 3;
 String websiteURI = 4;
}
```

*Ref: Building An Event-Driven Data Mesh.md — "Best Practices for Managing Schemas in Your Codebase"*

---

### Choosing a Schema Technology

**Principle:** Schema choice is mostly a tooling-and-existing-investment decision. Adopt one standard via the federation, don't proliferate.

**Do:**
- Adopt Apache Avro or Google Protobuf as the federation's standard.
- Use Avro if you want dynamic deserialization; Protobuf if your org is .NET-flavored (Saxo Bank's precedent).
- Use the schema's annotation mechanism to tag PII and encryption metadata.

**Don't:**
- Don't choose based on theoretical merits alone — look at integration with the broker, your languages, and code generators.
- Don't roll your own — adopt existing tools with strong community support (Buf for Protobuf).

**Saxo Bank case (Protobuf over Avro):**
- .NET shop had Avro integration friction (lagging C# and Python clients).
- Protobuf had clean code generation and no (de)serialization issues.
- Buf provided linting, style guides, naming conventions, enum usage tooling.
- Protobuf annotations enabled embedding PII and encryption metadata in schemas.

*Ref: Building An Event-Driven Data Mesh.md — "Choosing a Schema Technology"; "Why Saxo Bank Chose Protobuf over Avro"*

---

### Event Type Taxonomy

**Principle:** Most events are either *state* (current state of an entity) or *delta* (a specific transition). Pick the right type for the right job.

**Do:**
- Default to state events for any external data product (ECST-friendly, compactable, simpler).
- Use delta events *internally* within a private bounded context where coupling is intentional.
- Use measurement events for analytics-IoT-style snapshots; explicitly accept lossiness.
- Avoid notifications pointing to mutable external state — they race and miss transitions.

**Don't:**
- Don't expose internal delta events across bounded contexts — they're an unbounded set with cascading complexity.
- Don't use notifications as a lazy shortcut to "real" state events.

**The three event stages:**
1. Initial state.
2. Delta that alters initial state to final state.
3. Final state (which is also initial state for the next change cycle).

*Ref: Building An Event-Driven Data Mesh.md — "Introduction to Event Types"; "Expanding on State Events and Event-Carried State Transfer"*

---

### State Events (Current State vs Before/After)

**Principle:** Current state events are the default for data products. Before/after events double your storage and complicate compaction.

**Do:**
- Default to current state events; consumers will materialize and detect transitions themselves.
- Use before/after only when an internal CDC system already produces them or when the simplicity-for-producers outweighs the cost.

**Don't:**
- Don't use before/after when you can materialize cheaply — the broker-side complexity isn't worth it.
- Don't write compensation logic for before/after leaks — switch to current-state events.

**Code (before/after state event):**
```
Value: {
 before: { name: "Adam", country: "Atlantis" },
 after: { name: "Adam", country: "Canada" }
}
```
```
Key: 26
Value: {
 before: { name: "Adam", country: "Canada" },
 after: null
}
```

**Compaction problem with before/after:** Deletion via before/after sets `after` to null, but the entire value isn't null. Brokers won't recognize this as a tombstone. CDC tools like Debezium work around this by emitting a separate tombstone record.

*Ref: Building An Event-Driven Data Mesh.md — "Current State Events"; "Before/After State Events"*

---

### Delta Events — Use Cases and Anti-Patterns

**Principle:** Delta events are great *inside* a private bounded context (event sourcing). They're terrible across domains.

**Do:**
- Use delta events for event sourcing within a single domain where the logic to interpret them is colocated.
- Publish domain-internal events as state events for any external coupling.

**Don't:**
- Don't expose delta events to other bounded contexts — the receiving team must replicate your aggregation logic, and changes to your domain silently break them.
- Don't add new delta events over time as business expands — the consumer's interpretation logic must keep up, an unsustainable surface.

**Five reasons delta events fail for cross-domain data products:**
1. Infinite set of possible event types (the aggregation logic has unbounded surface).
2. Interpretation logic must be replicated to every consumer.
3. New event types map poorly to existing event streams and require consumer coordination.
4. Inversion of ownership — consumer-specific logic gets pushed into the producer.
5. Historical data maintenance becomes impractical (compaction impossible).

**Code (measurement-style user event — observation at a point in time):**
```
Key: "USERID-8271949472726174"
Value: {
 utc_timestamp: "2022-01-22T15:39:19Z"
 ad_id: 1739487875123
 page_id: 364198769786
 url: https://www.somewebsite.com/welcome.html
}
```

*Ref: Building An Event-Driven Data Mesh.md — "Delta Events"; "Event Sourcing with Delta Events"; "Why Delta Events Don't Work for Event-Driven Data Products"*

---

### Measurement Events

**Principle:** Measurement events record an *observation at a point in time*. They're perfect for analytics, lossy by nature, and may be aggregate-aligned.

**Do:**
- Expect measurement lossiness — ad-blockers, dropped packets, sensor outages will occur.
- Use them to power aggregate-aligned data products (counts per hour, percentiles, etc.).
- Decide if your SLO tolerates outage-induced lag or demands perfect completeness, and design accordingly.

**Don't:**
- Don't try to perfectly replay lost measurements — better to publish aggregates from what you have.
- Don't use them for stateful domain entities — they're not the public state of anything.

**Real-world measurement example (RIM/BlackBerry, Bellemare's early career):**
- Internal dev devices emitted measurement dumps on "bad things" (dropped calls, messenger failures, modem resets).
- Schema was essential — automated post-processing relied on it.
- Completeness > real-time. Hours/days/weeks of delayed arrivals were tolerated.
- Daily SLO satisfied dependent consumers.

*Ref: Building An Event-Driven Data Mesh.md — "Measurement Events"*

---

### Hybrid Events

**Principle:** Hybrid events (state with a bit of "why") trade coupling for expressiveness — use them sparingly and only when the "why" is stable.

**Do:**
- Use a hybrid event when the "how" is immutable and unlikely to drift (e.g., a one-time sign-up mechanism).
- Keep the embedded delta semantics small and well-documented in the schema.

**Don't:**
- Don't embed transition semantics when the underlying process is likely to change — every change becomes a breaking change.
- Don't use hybrid events as a shortcut for "I don't want to maintain state in the consumer."

**Code (hybrid sign-up event):**
```
Key: "USERID-9283716596927463"
Value: {
 name: "Randolf T. Bandit"
 signup_time: "2022-02-22T22:22:22Z"
 birthday: "2000-01-01T00:00:00Z"
 //An enum of (MAIN, VIA_AD_EMAIL, THIRD_PARTY, or ADMIN)
 method_of_signup: "VIA_AD_EMAIL"
}
```

**Risk calculus:** Use hybrid events only when:
- The "how" is essentially binary or one-shot (sign-up mechanism).
- The logic populating the field is simple and unlikely to drift.
- Drift in meaning can be mitigated by clear documentation in the schema.

*Ref: Building An Event-Driven Data Mesh.md — "Hybrid Events—State with a Bit of Delta"*

---

### Notification Events (Anti-Pattern)

**Principle:** Notifications — "something happened, fetch it elsewhere" — violate the immutability-of-the-event principle and reintroduce two sources of truth.

**Do:**
- Treat notifications as anti-patterns by default for data products.
- If you must use them, ensure they reference immutable storage and contain enough data to be useful without a back-channel.

**Don't:**
- Don't point a notification at a mutable store — race conditions make "full state transition" unrecoverable.
- Don't make consumers reconcile late events by polling the mutable target.

**Code (notification example — anti-pattern):**
```
Key: 12309131238218
Value: {
 status: "PARTIAL_RETURN"
 utc_timestamp: "2021-21-13T13:11:42Z"
 access_uri: "serverURI:8080/orders/values/12309131238218"
}
```

**Race-condition example:** A sale transitions SOLD → PARTIAL_RETURN → FULL_RETURN, emitting three events. A lagging consumer may miss PARTIAL_RETURN entirely because the mutable store has moved on. A new consumer replaying the backlog will only see FULL_RETURN.

*Ref: Building An Event-Driven Data Mesh.md — "Notification Events"*

---

### Bootstrapping Data Products with Connectors

**Principle:** Connectors (Kafka Connect, Debezium) are a pragmatic bootstrap path from existing systems to event-driven data products, *not* a final destination.

**Do:**
- Negotiate ownership and responsibilities clearly when standing up a connector — who owns the connector, who owns the produced events, who owns the SLA?
- Snapshot safely using a read-only replica where possible, or nonblocking incremental snapshotting.
- Treat the connector as a starting point; migrate to native event-driven producers when the domain matures.

**Don't:**
- Don't rely on the connector framework as the permanent solution — it's a stepping stone.
- Don't push schema changes through the connector without coordination — internal models leak.

*Ref: Building An Event-Driven Data Mesh.md — "Getting Started: Bootstrapping with Connectors"*

---

### Dual Writes (Anti-Pattern)

**Principle:** Dual-writing a database and an event stream is non-atomic; intermittent failures will silently leave one side behind.

**Do:**
- Treat dual writes as a temporary measure only for loss-tolerant data (measurements).
- For all other events, use an outbox, CDC, or query-based liberation.

**Don't:**
- Don't try to paper over dual writes with two-phase commit — it's complex and brittle.

**Why dual writes are insidious:** They work most of the time. Without explicit failure-mode testing and monitoring, missing events surface weeks/months later when downstream consumers notice discrepancies.

*Ref: Building An Event-Driven Data Mesh.md — "Dual Writes"*

---

### Query-Based Liberation (Polling the Database)

**Principle:** Use query-based polling when the data store has no log API (legacy DBs), when you can't modify the source, and when the loss from missing intermittent updates is acceptable.

**Do:**
- Require and maintain `updated_at` timestamps (or autoincrement IDs).
- Snapshot off a read replica where live load is too sensitive to lock.
- Use views or materialized views to expose only the data products' required fields, never the internal schema.
- Acknowledge the trade-offs (missing hard deletes, intermittent capture, production load).

**Don't:**
- Don't assume you'll capture every change — series of rapid edits may collapse.
- Don't expose internal table schemas directly via poll results.

*Ref: Building An Event-Driven Data Mesh.md — "Polling the Database to Create Data Products"*

---

### Change-Data Capture (CDC)

**Principle:** CDC reads the database's write-ahead log (WAL) or binlog and emits every INSERT/UPDATE/DELETE as an event. Low latency, hard delete tracking, low source-impact.

**Do:**
- Default to CDC for relational databases with a WAL or binlog (PostgreSQL, MySQL, MongoDB Change Streams).
- Use watermarked, non-blocking incremental snapshots (Netflix DBLog, Debezium) to avoid lock contention.
- Convert hard deletes into tombstones so compacted event streams drop them cleanly.

**Don't:**
- Don't assume CDC will let you hide your internal schema — logs expose the schema verbatim; convert via views or eventification.
- Don't ignore the source-impact of bulk snapshotting — even nonblocking snapshots take time and resources.

**CDC trade-offs:**
- Pros: nonblocking snapshots, minimal performance penalty, very low latency, hard delete tracking.
- Cons: exposes internal data model, produces highly normalized event streams requiring downstream denormalization.

*Ref: Building An Event-Driven Data Mesh.md — "Change-Data Capture"*

---

### Transactional Outbox (Atomic Internal Model + Event)

**Principle:** Write the business update and a corresponding outbox record in a single transaction. A separate process publishes the outbox to the event stream. This is the strongest guarantee for atomic, consistent event production.

**Do:**
- Wrap `UPDATE internal; SELECT sub-model; INSERT outbox; COMMIT` in one transaction.
- Validate the schema *before* committing the transaction (before-the-fact serialization) for the strongest guarantees.
- Choose NOT NULL, defaults, and CUR_TIMESTAMP carefully on outbox columns.
- Clean up the outbox after publishing (delete the row, or use a BLACKHOLE storage engine in MySQL).

**Don't:**
- Don't apply outbox writes after the transaction commits — you've already given up atomicity.
- Don't skip schema validation at the outbox boundary — published events become the contract.

**Code (Python outbox pattern):**
```python
try:
 conn = mysql.connector.connect(host='localhost',
 database='python_db',
 user='abellemare',
 password='definitelynotpassword')
 conn.autocommit = False
 cursor = conn.cursor()
 # Perform the internal domain model update
 internal_model_update = """
 Update EcomItem
 set price = 1299.99
 where id = 4291"""
 cursor.execute(internal_model_update)
 # Select the subdomain of the internal model we want to write to
 # the transactional outbox
 internal_sub_model_query = """
 Select name, price
 from EcomItem
 where id = 4291"""
 cursor.execute(internal_sub_model_query)
 name_and_price = cursor.fetchone()
 if (name_and_price == None):
 raise Exception("Unexpected missing record. Can't get name_and_price")
 # Insert the selected data into the outbox
 outbox_insert = """INSERT INTO EcomItem_Outbox (id, name, price)
 VALUES (4291, %s, %s)"""
 # Pass the name and price in to replace the query wildcards
 cursor.execute(outbox_insert, name_and_price)
 # Commit the internal and outbox updates atomically
 conn.commit()
except mysql.connector.Error as error:
 # reverting changes because of exception
 conn.rollback()
finally:
 # Close the database connection
 if conn.is_connected():
 cursor.close()
 conn.close()
```

**Outbox trade-offs:**
- Pros: internal data model isolation, exactly-once outbox semantics, early schema enforcement, denormalized data at write time.
- Cons: database must support transactions, application code updates required, outbox write can fail transaction, performance impact.

*Ref: Building An Event-Driven Data Mesh.md — "Change-Data Capture Using a Transactional Outbox"*

---

### Denormalization and Eventification

**Principle:** Eventification (denormalizing at write time) makes consumer joins unnecessary. Choose what to denormalize based on consumer needs, update frequency, and payload size.

**Do:**
- Denormalize within the outbox transaction to shield consumers from foreign-key joins.
- Re-emit denormalized events when any underlying component changes (especially with SCDs).
- Balance degree of denormalization against event size and update rate — don't join in high-velocity or large-payload streams.

**Don't:**
- Don't auto-join everything in the source model — frequently changing fields will spam consumers.
- Don't denormalize data that is rarely used by any consumer; let them fetch it themselves.

**Code (denormalization at the outbox):**
```python
...
 # Assume that we have just updated the internal model
 # Next, we select fields from the internal model and denormalize it
 # by joining against the Merchant table.
 internal_model_query = """
 select e.name, e.price, m.name as merchant_name, m.premium_partner
 from EcomItem as e, Merchant as m,
 join on e.merchant_id = Merchant.id
 where e.id = 4291"""
 cursor.execute(internal_sub_model_query)
 result = cursor.fetchone()
 # Create the insert statement for the outbox table
 outbox_insert = """
 INSERT INTO
 Enriched_EcomItem_Outbox (id, name, price, merchant_name, premium_partner)
 VALUES (4291, %s, %s, %s, %s)"""
 cursor.execute(outbox_insert, result)
 # Commit the internal and outbox updates atomically
 conn.commit()
...
```

**Reminder:** If you denormalize, re-emit on every underlying change — otherwise the denormalized event is permanently inaccurate.

*Ref: Building An Event-Driven Data Mesh.md — "Denormalization and Eventification"; "Eventification at the Transactional Outbox"*

---

### Eventification in a Dedicated Service

**Principle:** When you cannot modify the source database, spin up an eventification service (Kafka Streams, Flink SQL) that joins the normalized streams into a denormalized output.

**Do:**
- Use Kafka Streams or Flink SQL to keep the join logic localized to one team.
- Use copartitioning so all records for a key are processed by the same instance.
- Publish the enriched result as a new data product with its own owner.

**Don't:**
- Don't make consumers re-implement the join — that's the trap this service exists to escape.

**Code (Kafka Streams joiner):**
```java
public Topology buildTopology(Properties envProps) {
 //Configuration code not shown for brevity
 //Create the Serdes
 MerchantSerde merchantSerde = new MerchantSerde(...);
 EcomItemSerde ecomItemSerde = new EcomItemSerde(...);
 EnrichedEcomItemSerde enrichedEcomItemSerde = new EnrichedEcomItemSerde(...);
 //Create the application builder and create two tables.
 KStreamBuilder builder = new KStreamBuilder();
 //A KTable is the materialization of a state-modeled event stream
 KTable<Long, Merchant> merchantTable =
 builder.table(Serdes.Long(), merchantSerde, merchantTopic);
 KTable<Long, EcomItem> ecomItemTable =
 builder.table(Serdes.Long(), ecomItemSerde, ecomItemTopic);
 ecomItemTable
 .join( merchantTable,
 EcomItem::getMerchantId,
 new EcomToMerchantJoiner() )
 .toStream()
 .to(enrichedEcomItemTopic, Produced.with(Serdes.Long(), enrichedEcomItemSerde));
 return builder.build();
}
```

**Code (ValueJoiner for the join):**
```java
public class EcomToMerchantJoiner implements
 ValueJoiner<EcomItem, Merchant, EnrichedEcomItem> {
 public EnrichedEcomItem apply(EcomItem e, Merchant m) {
 return EnrichedEcomItem.newBuilder()
 .setId(e.getId())
 .setName(e.getName())
 .setPrice(e.getPrice())
 .setMerchantName(m.getMerchantName())
 .setPremiumPartner(m.getPremiumPartner())
 .build();
 }
}
```

**Code (Flink SQL equivalent):**
```sql
SELECT *
FROM EcomItem
INNER JOIN Merchant
ON EcomItem.merchantId = Merchant.id
```

*Ref: Building An Event-Driven Data Mesh.md — "Eventification in a Dedicated Service"*

---

### Slowly Changing Dimensions (SCD)

**Principle:** Slow-changing data (e.g., merchant status, address) requires deliberate modeling — Type 1 overwrites history; Type 2 keeps it.

**Do:**
- Default to Type 1 in state events (only the latest value is stored; broker compaction handles the rest).
- Use Type 2 when consumers need historical context (e.g., engagement analysis); ensure the schema carries a `version` field.
- Re-emit denormalized events when an SCD field changes — silent staleness is unacceptable.

**Don't:**
- Don't mix Type 1 and Type 2 within the same product without clearly labeling.
- Don't ship Type 2 products by default — most use cases don't need the history overhead.

**Type 1 vs Type 2:**
- **Type 1 (overwrite):** Only the latest value is retained. New event overwrites old. Event broker can compact away the old event.
- **Type 2 (append):** All versions retained in the event with version IDs. Consumer can query historical state. Operational consumers usually take the latest; analytical consumers query historical.

*Ref: Building An Event-Driven Data Mesh.md — "Slowly Changing Dimensions"*

---

### Bootstrapping Cloud Storage Files Into Event Streams

**Principle:** Read cloud-stored batch files (Parquet, Avro, etc.) into event streams as a transitional step. Pick the bootstrap path that matches your tolerance for dual writes.

**Do:**
- Add a downstream step that reads the batch output, converts to events, writes to the stream — minimum coupling with the legacy job.
- Use a connector that watches for new files (S3 sink/source) for fully decoupled bootstrapping.
- Treat bootstrapped streams as a stepping stone to real-time event production.

**Don't:**
- Don't refactor the legacy job to dual-write — saves refactoring but reintroduces dual-write risk.

**Bootstrap options ranked:**
1. **Add post-job step (recommended):** read batch output, convert to events, write to broker — minimum coupling, language freedom.
2. **Use S3 sink connector:** fully decoupled; the broker watches for new files; producer untouched.
3. **Refactor the legacy job to emit events:** saves reading data twice, but introduces dual-write risk and refactoring cost.

*Ref: Building An Event-Driven Data Mesh.md — "Bootstrapping Cloud Storage Files to an Event Stream"*

---

### Integrating Event-Driven Data Into Data at Rest (Medallion)

**Principle:** Meet batch/analytics users where they are: sink event streams to Parquet in cloud storage partitioned by time, alongside the Medallion (bronze/silver/gold) tiers.

**Do:**
- Convert event schemas to columnar formats (Parquet) for batch processors.
- Partition by time intervals that match existing big-data conventions (1m/5m/30m/1h).
- Amalgamate many small files into fewer large ones after the initial low-latency window.
- Treat the Parquet output and the event stream as two modes of one data product — with a single owner.

**Don't:**
- Don't write tiny files every second and expect batch consumers to love it — give them fewer, larger files.
- Don't dual-manage the same data product with different owners via different modes.

**Code (source-aligned click-stream event):**
```
Key: String, //user_account
Value: {
 user_account: String,
 utc_timestamp: Datetime,
 ad_id: long,
 page_id: String,
 bid_in_cents: int
}
```

*Ref: Building An Event-Driven Data Mesh.md — "Analytics and the Medallion Architecture"; "Connecting Event Streams Into Existing Batch-Data Flows"*

---

### Through-the-Lens-of-Data-Mesh Diagnostic

**Principle:** Diagnose broken cross-team data pipelines by asking whether they violate the four principles and the data-as-product model.

**Do:**
- Push shared, divergent business logic (session definitions, unique-user attribution) *upstream* into a common data product.
- Identify missing data product owners and call them out via the federation.
- Let ops tooling reflect the data product ownership graph.

**Don't:**
- Don't keep reconciling reports downstream because "that's how it's always been" — even a partial migration upstream breaks the divergence.

**Symptoms of missing data product thinking:**
- Source data sets are not data products (no SLA, no owner, no schema contract).
- No domain ownership — relying on tribal knowledge.
- Protective/siloed culture; everyone copies "close to the source" because upstream is unreliable.
- Divergent downstream business logic for the same concepts (sessions, unique users).

*Ref: Building An Event-Driven Data Mesh.md — "Through the Lens of Data Mesh: What's Going On?"; "Through the Lens of Data Mesh: How Do We Solve It?"*

---

### File Size, SLA, and Latency Balancing

**Principle:** Decide the latency/file-size tradeoff per data product and stick to it. Optimize it once and share the rule across consumers.

**Do:**
- Publish raw events within minutes via small frequent files for low-latency consumers.
- Periodically amalgamate small files into larger ones for batch consumers.
- Make the SLA explicit: "every 5 minutes" or "every hour", with the bucket owner.

**Don't:**
- Don't pick the cadence without consulting analytics — each user has a tolerable max latency.
- Don't ratchet cadence up every quarter without driving the change through governance.

**Post-connect file amalgamation pattern:**
- Low-latency consumers get fresh small files (e.g., every minute).
- Hourly batch job combines small files into fewer larger ones (e.g., 100 MB+).
- Update the cloud filesystem metadata (Hive, Glue, Unity Catalog) to redirect batch jobs to amalgamated files.

*Ref: Building An Event-Driven Data Mesh.md — "Balancing File Sizes, SLAs, and Latency"; "Implementing post-connect file amalgamation"*

---

### Eventual Consistency Strategies

**Principle:** Two independent contexts, independent clocks, and asynchronous propagation mean you will get inconsistency. Plan for it instead of denying it.

**Do:**
- Use event-driven data products *instead of* request-response calls to avoid cross-context clock mismatches.
- Expose eventual consistency in server responses when responding to synchronous queries (HTTP 503 + `Retry-After`, stale-data flag, callback API).
- Use offsets, not timestamps alone, to detect lag (compacted streams may be idle for hours).

**Don't:**
- Don't rely on `event_time` of the most recent event for lag detection — false positives will abound.
- Don't treat "two services in a cluster" as the same time bubble — they're not.

**Convergence definition (Pat Helland's framing):** A system is convergent or "eventually consistent" if, when all messages have been delivered, all replicas agree on the set of stored values.

**Two reasons services don't converge:**
1. Service is lagging behind (data is consistent; consumer is slow).
2. Data product is lagging behind (data is not consistent; producer/broker unavailable).

*Ref: Building An Event-Driven Data Mesh.md — "Eventual Consistency"; "Strategies for Dealing with Eventual Consistency"*

---

### Preventing Failures to Avoid Inconsistency

**Principle:** The fastest way to be eventually consistent is to never be inconsistent — prevent failures via good DevOps and sufficient resource scaling.

**Do:**
- Monitor consumer lag, scale up before SLAs are missed.
- Apply sufficient resources to producer/connector/broker so they don't drop events.
- Use read-only replicas for query-based polling to isolate operational load.
- Identify and fix single points of failure.

**Don't:**
- Don't try to "design around" eventual consistency by adding synchronous calls — you'll reintroduce coupling.

*Ref: Building An Event-Driven Data Mesh.md — "Prevent Failures to Avoid Inconsistency"*

---

### Out-of-Order and Late-Arriving Events

**Principle:** Events are inherently out-of-order across producers and partitions. Tie late-event handling to the data product's SLA, not to "best effort".

**Do:**
- Treat *event time* (when the event actually happened) as first-class.
- Allow some grace period (drop / wait / grace) on windows and joiners — and tie the grace to the data product SLA.
- Use broker-recorded or producer-recorded event time (preferably producer-recorded).

**Don't:**
- Don't rely on broker ingestion time as event time — it papers over clock skew.
- Don't have every consumer independently decide what counts as "late" — codify it.

**Three late-event handling strategies:**
- **Discard:** Drop events for closed windows; aggregations are complete.
- **Delay output:** Keep window open for a grace period; lose some latency for higher completeness.
- **Multiple updates:** Output threshold-triggered result, keep window open for grace period, emit updated result if late events arrive, then close.

*Ref: Building An Event-Driven Data Mesh.md — "Out-of-Order Events"; "Resolving Late-Arriving Events"*

---

### Reprocessing and New Services

**Principle:** New consumers replay from the beginning; services with bugs may need to reprocess. Both must be designed for, not tolerated.

**Do:**
- Reprocess from the beginning of the entity event stream; inform downstream consumers about expected output spikes.
- Plan for the time and downstream impact of reprocessing; use quotas if needed.
- For bugs: prefer producing corrected events over purging-and-recreating (lighter blast radius).
- Plan downstream consumer handling for the duplicate-replay volume.

**Don't:**
- Don't reply on partial reprocessing that starts in the middle of a stream — you'll end up with phantom states.
- Don't send duplicate business emails/charges simply because events get reprocessed — guard with idempotency keys.

**Bad-data fix options:**
- **Publish corrected events** to existing output streams. Suitable when consumers can reverse downstream effects.
- **Purge and recreate** the data product. Heavyweight; requires stop-the-world coordination.

*Ref: Building An Event-Driven Data Mesh.md — "Plan for New Services and Reprocessing of Data"*

---

### Synchronize Data Products on Time Boundaries

**Principle:** Batch consumers benefit from time-partitioned Parquet mirroring of the event stream. Use the same partitioning scheme as the rest of your big-data ecosystem.

**Do:**
- Pick partitioning intervals (1m / 5m / 30m / 1h) that match existing big-data partitions.
- Use connector-provided partitioning options (hourly, daily, time-based) where possible.
- Keep the partitioning metadata accessible to big-data consumers (Hive, Glue, Unity Catalog).

**Don't:**
- Don't invent a new partitioning scheme — it will conflict with every other batch consumer.

*Ref: Building An Event-Driven Data Mesh.md — "Synchronize Data Products on Time Boundaries"*

---

### Cost of Bad Data (The Trillion-Dollar Wakeup Call)

**Principle:** Quantify the cost of doing nothing — the data-team bottleneck and schema-on-read pitfalls are economically massive.

**IBM/HBR 2016 estimates (cited by Bellemare):**
- $3.1 trillion USD annual impact of bad data in the US alone.
- 50% of knowledge worker time wasted hunting for data, fixing errors, and finding confirmatory sources.
- 60% of data scientist time spent cleaning and organizing data.

**Symptom checklist — your data org may be in the "bad data" trap:**
- Reports diverge between teams for the same metric.
- Customer complaints about incorrect billing or engagement numbers.
- Schema changes silently break downstream pipelines.
- Reconciliation jobs run nightly to "fix" divergence.
- Engineers spend more time fixing broken data jobs than building features.

**Do:**
- Treat data quality as a first-class engineering investment.
- Measure the cost (engineer-hours, customer-impact incidents, lost revenue) of bad data.
- Use that cost to justify data mesh investments.

**Don't:**
- Don't accept "data is messy, that's just how it is" as a final answer.
- Don't assume your org is immune because "we have a data team".

*Ref: Building An Event-Driven Data Mesh.md — "Bad Data: The Costs of Inaction"*

---

### Objections to Data Mesh (and Why They Miss the Mark)

**Principle:** Three common objections to data mesh have ready answers. Don't let them block adoption.

**Objection 1 — "Producers can't model data for everyone's use cases":**
- *Reality:* Producer exposes the public model for *their* domain. Consumers build their own models on top.
- *Why it misses:* Producers don't have to model for everyone — they expose what's authoritative. Consumers compose and join.
- *Action:* Tell producers to ask consumers what they need (consultative exercise).

**Objection 2 — "Multiple copies of data is bad":**
- *Reality:* Multiple copies already exist (smash-and-grab ETL, OLAP warehouses, etc.) — they're just unmanaged.
- *Why it misses:* Data mesh formalizes copies with explicit ownership, schemas, SLAs.
- *Action:* Frame copies as "data products" with owners, not as accidental drift.

**Objection 3 — "Eventual consistency is too hard to manage":**
- *Reality:* Most business processes don't need perfect consistency; those that do stay within one service boundary.
- *Why it misses:* Confuses internal (strong) and cross-context (eventual) consistency.
- *Action:* Use event-driven products *instead of* sync request-response calls; expose eventual consistency in HTTP responses.

*Ref: Building An Event-Driven Data Mesh.md — "Common Objections to an Event-Driven Data Mesh"*

---

### Through-the-Lens-of-Mesh Adoption Path

**Principle:** Adoption is incremental. Identify the worst-affected business use case, fix it in place, evangelize, repeat.

**Do:**
- Start where bad data is actively costing money or trust (billing divergence, fraud, etc.).
- Make the smallest end-to-end slice work before expanding.
- Celebrate wins — feed the adoption loop.
- Use the federation to formalize what works.

**Don't:**
- Don't attempt a complete refactor upfront — you'll exhaust the org before you finish.
- Don't ignore social change — technical wins need cultural reinforcement.

*Ref: Building An Event-Driven Data Mesh.md — "Bringing It All Together"*

---

## Anti-Patterns & Common Mistakes

- **The Data Monolith:** A single central data team becomes a bottleneck because it can't understand every domain's data needs. *Fix:* adopt domain ownership; redistribute data modeling and publication to domain teams. *Ref: "The Data Monolith"*

- **Schema-on-read (Data Swamp):** Validating data at query time means downstream users either fail or interpret silently wrong. *Fix:* require schemized, validated, versioned data products at write time. *Ref: "The Organizational Impact of Schema on Read"*

- **Smash-and-Grab ETL:** Teams reach into other teams' databases for "just one column". *Fix:* route through published data products with explicit owner, schema, SLA. *Ref: "Do-it-yourself and custom point-to-point data connections"*

- **Synchronous Microservices fanout:** Synchronous request-response multiplies temporal coupling and causes cascading failures. *Fix:* replace with event-driven data products; preserve sync APIs only where genuinely needed. *Ref: "The Difficulties of Communicating Data for Operational Concerns"*

- **Delta Events for Cross-Domain:** Coupling on internal transitions means your domain's refactor is everyone's emergency. *Fix:* publish state events; let consumers compute their own transitions. *Ref: "Why Delta Events Don't Work for Event-Driven Data Products"*

- **Notification with a Mutable Target:** "Something happened, look it up here" races and breaks with state transitions. *Fix:* emit the full state in the event. *Ref: "Notification Events"*

- **Dual Writes to DB and Stream:** Without atomicity, intermittent failures will silently diverge. *Fix:* use the outbox pattern or CDC. *Ref: "Dual Writes"*

- **Lambda Architecture for Data Mesh:** Reconciling batch/stream seams across N products is exponential. *Fix:* commit to Kappa with a broker that has infinite retention. *Ref: "The Lambda Architecture and Why It Doesn't Work for Data Mesh"*

- **Before/After State by Default:** Doubles storage and breaks log compaction. *Fix:* default to current-state events. *Ref: "Before/After State Events"*

- **Schema Changelog with Schemaless JSON:** Implicit contracts breed inconsistent views of truth. *Fix:* explicit schemas with evolution rules. *Ref: "Selecting an Event Format"; "Designing Events"*

- **Event Sprawl & Per-stream Naming Chaos:** Without a federation-picked standard, every team invents their own. *Fix:* the governance team narrows down to ~2 formats; tooling enforces them. *Ref: "Supporting Data Product Schemas"*

- **Tracking Lineage via Self-Reporting:** Opt-in lineage has gaps and becomes misleading. *Fix:* derive topology from real ACLs and client identities. *Ref: "Topology-Based Lineage"*

- **Consumer Manages Schema Upgrades for Producer:** Coupling producer release cadence to consumer upgrades. *Fix:* full-transitive compatibility or coordinated breaking change. *Ref: "Schema Evolution"*

- **Not Using Federal Governance:** Without governance, every team invents a different pattern; "internal data model" leaks everywhere. *Fix:* charter the team; tie standards to the platform defaults. *Ref: "Federated Governance"*

- **Selling Event-Stream Lag by Event Time Only:** Compacted streams can be idle for hours — false lag signals. *Fix:* rely on offsets. *Ref: "Expose Eventual Consistency in the Server Response"*

- **Bad Data Outliving Detection:** Schema-on-read pipelines silently propagate an Int32-as-String or boolean-to-long change for months. *Fix:* schema-at-write with strict registry enforcement; nightly quality checks. *Ref: "The Organizational Impact of Schema on Read"*

- **Records Coupling on Mutation:** A before/after event's `before` field holds stale data indefinitely if subsequent deletes are not tombstoned. *Fix:* emit explicit tombstones on deletes; rely on broker compaction. *Ref: "Before/After State Events"*

- **Bootstrap Connector Left in Place Forever:** Connectors are stepping stones, not the final form. *Fix:* migrate to native event-driven producers once the domain matures. *Ref: "Getting Started: Bootstrapping with Connectors"*

---

## Decision Heuristics / Checklists

**Event Broker Checklist:**
- [ ] Unlimited retention?
- [ ] Replayable from arbitrary offset?
- [ ] Tooling ecosystem (schema registry, code generators, connectors, processing frameworks)?
- [ ] SaaS option acceptable, or self-hostable?
- [ ] Tiered storage for cold data?
- [ ] Mature community and hiring pool?

**Data Product Creation Checklist:**
- [ ] Named human owner assigned?
- [ ] SLA tier (1–4) declared?
- [ ] Quality tier (bronze/silver/gold) declared?
- [ ] Schema registered with the schema registry?
- [ ] Compatibility level (backward/forward/full) chosen?
- [ ] Tags (PII, financial, region, deprecation) applied?
- [ ] Deprecation plan exists?

**Schema Evolution Checklist:**
- [ ] Default values supplied on new fields?
- [ ] No removed fields without negotiation?
- [ ] No type changes without breaking-change review?
- [ ] Compatibility rule (backward/forward/full) enforced at registry?
- [ ] Consumers can keep their schemas during the migration window?

**Data Liberation Decision Tree:**
- [ ] Can you modify the source code? → **Transactional outbox** (atomic, strongest guarantees).
- [ ] Does the source have a log (WAL/binlog/Change Streams)? → **CDC** (low-latency, hard delete tracking).
- [ ] Can you only query the database? → **Polling with `updated_at`** (or autoincrement ID).
- [ ] Is event loss acceptable and volume low? → **Dual writes** (measurements only).

**Bootstrap Pattern Decision:**
- [ ] Add real-time value over current batch? → **Sink connector** feeding existing Parquet consumers, *while* you build event-native consumers in parallel.
- [ ] Need strong consistency atomic with internal updates? → **Outbox** with before-the-fact serialization.
- [ ] Source has no log? → **Query-based polling + a CDC-table where supported**.

**Eventual Consistency Tactic:**
- [ ] Can both contexts read from the same product? → **Use the product, never the request-response call**.
- [ ] Is the system internal-facing, exposed as HTTP? → Return 503 + Retry-After, expose `stale_data` flag, or accept callbacks.
- [ ] Reprocessing historical data? → Reset offsets to the beginning of each input; warn downstream; consider quotas.

**Self-Service Platform Build Order:**
- [ ] Level 1 MVP: event broker + schema registry + spreadsheet catalog + connectors.
- [ ] Level 2 EP: real catalog + UI + identities + ACLs + stream processing.
- [ ] Level 3 MP: unified IAM via OAuth2/OIDC + programmatic API + monitoring + multiregion.

---

## Key Takeaways

1. **Data is a first-class product.** Owned by the domain, with a schema, SLA, tier, and a real on-call. *Ref: "Principle 2: Data as a Product"*
2. **Event streams are the substrate.** Durable, append-only, replayable, indefinitely retained, partitioned. They unify ops and analytics. *Ref: "Event Streams for Data Mesh"*
3. **Commit to Kappa, not Lambda.** A single broker-as-source-of-truth eliminates batch/stream reconciliation seams. *Ref: "The Kappa Architecture"*
4. **Federation, not centralization.** Set standards via charter; let domains own implementation. *Ref: "Principle 3: Federated Governance"*
5. **Default to state events, never deltas.** State events scale; deltas couple consumers to internal transitions. *Ref: "Why Delta Events Don't Work for Event-Driven Data Products"*
6. **Atomic event publication via outbox.** Don't dual-write; wrap internal update and outbox in one transaction. *Ref: "Change-Data Capture Using a Transactional Outbox"*
7. **Encrypt sensitive data and crypto-shred on deletion.** Immutability meets GDPR. *Ref: "Data Privacy, the Right to Be Forgotten, and Crypto-Shredding"*
8. **Use offsets, not timestamps, for lag detection.** Compacted streams may be deliberately idle for hours. *Ref: "Expose Eventual Consistency in the Server Response"*
9. **Build the data catalog into operations, not docs.** Derive lineage from real ACLs; never self-reported. *Ref: "Topology-Based Lineage"*
10. **Adopt iteratively.** MVP data products and MVP platforms; let usage drive the next iteration. *Ref: "Bringing It All Together"*
11. **Schemas are contracts.** Use full-transitive compatibility; negotiate and migrate for true breaking changes. *Ref: "Schema Evolution: Changing Your Schemas Through Time"*
12. **Connectors are stepping stones.** Bootstrap with Kafka Connect / Debezium, but migrate to native producers once the domain matures. *Ref: "Getting Started: Bootstrapping with Connectors"*
13. **Lineage from reality, not self-reporting.** Real ACLs and client identities are the source of truth. *Ref: "Topology-Based Lineage"*
14. **Choose retention up front.** Only Kafka and Pulsar offer unlimited retention — other brokers cap at 31/90/365 days. *Ref: "Selecting an Event Broker"*
15. **Indefinite retention + compaction + tombstones = Kappa.** All four are required to make a single broker the source of truth for both history and real-time. *Ref: "Supporting the Requirements for Kappa Architecture"*

---

## Cross-References
- Related: [[../Building_Event-driven_Microservices.md]] — the same author (Adam Bellemare) on the implementation side: aggregates, ECST, schemas, and consumer mechanics.
- Related: [[../Software_Architecture_Patterns.md]] — architecture style selection (event-driven, microservices) that underpins data-mesh implementations.
- Topic index: [[../INDEX.md]]