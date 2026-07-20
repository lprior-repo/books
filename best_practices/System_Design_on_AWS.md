# Per-Book Best Practices — System Design on AWS

> Comprehensive best-practice distillation from Jayanth Kumar and Mandeep
> Singh's *System Design on AWS: Building and Scaling Enterprise Solutions*
> (O'Reilly, Feb 2025). Patterns are cloud-agnostic in principle; AWS service
> mappings are called out explicitly. Topics cover system-design fundamentals,
> distributed-systems trade-offs, storage/compute/database patterns, networking,
> security, the AWS Well-Architected Framework, cost optimization, migration,
> and end-to-end multi-region reference architectures.

---

# System Design on AWS
**Author:** Jayanth Kumar and Mandeep Singh (foreword by Swami Sivasubramanian, VP AI/Data at AWS)
**Topic tags:** `#architecture` `#cloud` `#aws` `#systems`
**Language focus:** Language-agnostic; AWS-centric
**Sources:** `markdown_output/System_Design_on_AWS_Building_and_Scaling_-_Jayanth_Kumar/System_Design_on_AWS_Building_and_Scaling_-_Jayanth_Kumar.md` · `summaries/System_Design_on_AWS_Building_and_Scaling_-_Jayanth_Kumar.md`

## TL;DR
This book is a first-principles + AWS-mapping guide to designing and scaling
distributed systems. It moves from CAP/PACELC, fallacies of distributed
computing, ACID/BASE, and storage formats, through replication, sharding, and
caching, into concrete AWS service choices (VPC, ELB, CloudFront, S3, RDS,
DynamoDB, Lambda, ECS/EKS, Step Functions, MSK/Kinesis, Redshift, EMR,
SageMaker), and finishes with Day-0 → Day-N walkthroughs of a URL shortener,
web crawler, social network, online game leaderboard, video streaming, stock
broker, and chat (WhatsApp-scale) system. Apply when you need an opinionated,
trade-off-driven mental model for picking among AWS services and an
architectural pattern catalogue for large-scale systems.

---

## Best Practices by Topic

### Communication: Synchronous vs. Asynchronous

**Principle:** Pick the communication style by latency and coupling needs, not by habit.

**Do:**
- Use synchronous (blocking) calls for real-time UI/backend interactions where
  the user is waiting.
- Use asynchronous (callback/queue/event) communication for long-running jobs,
  cross-service fan-out, and decoupling.
- Document the timeout and retry policy for every synchronous call site.

**Don't:**
- Don't block the user request thread on a downstream dependency that may stall
  or batch work.
- Don't use async messaging for transactional workflows that need immediate
  commit acknowledgement.

**Code (sequence reference):**
```
Synchronous:  Client ──req──▶ Server ──res──▶ Client
              (sender blocks until response)

Asynchronous: Client ──req──▶ Server ──res──▶ Message bus ──callback──▶ Client
              (sender continues; result arrives later)
```
*Ref: System_Design_on_AWS.md — "Synchronous vs. Asynchronous Communication"*

---

### Consistency Spectrum Model

**Principle:** Choose the weakest consistency level that still satisfies the
business contract.

**Do:**
- Use strong consistency for financial ledgers, inventory, and seat reservation.
- Use eventual consistency for likes, view counts, recommendations, feeds.
- Use monotonic read consistency when "no going backward in time" matters.
- Use causal consistency for collaboration features (chat, comments, edits).

**Don't:**
- Don't promise strong consistency for cross-region replicated data without
  acknowledging the latency tax.
- Don't pick eventual consistency for code paths that assume read-after-write.

**Spectrum (strongest → weakest):**
```
Strong → Monotonic Read → Monotonic Write → Causal → Eventual
```
*Ref: System_Design_on_AWS.md — "Consistency Spectrum Model"*

---

### Availability and the "Nines"

**Principle:** Each additional "nine" is roughly an order-of-magnitude more
infrastructure; tie SLOs to business impact, not to vanity.

**Do:**
- Treat the table below as a budget for RTO/RPO and redundancy design.
- Combine components in parallel (not sequence) to multiply availability:
  `A_total = 1 − ∏(1 − A_i)`.

**Don't:**
- Don't plan for six nines unless revenue/regulation truly demands it.
- Don't chain many serial components without accounting for compounded downtime.

**Availability cheat sheet:**
| SLO | Downtime/year | Downtime/month | Downtime/week |
|-----|---------------|----------------|---------------|
| 99% (2 nines) | 3.65 days | 7.2 hours | 1.68 hours |
| 99.9% (3 nines) | 8.76 hours | 43.8 min | 10.1 min |
| 99.99% (4 nines) | 52.56 min | 4.32 min | 1.01 min |
| 99.999% (5 nines) | 5.26 min | 25.9 sec | 6.05 sec |
| 99.9999% (6 nines) | 31.5 sec | 2.59 sec | 0.605 sec |

*Ref: System_Design_on_AWS.md — "Measuring availability" / Table 1-1*

---

### Reliability: MTBF / MTTR / RTO / RPO

**Principle:** Reliability is the *frequency* of failures (MTBF); recovery is
the *cost* of a failure (MTTR). Design both, not just one.

**Do:**
- Use `MTBF = (Total Elapsed Time − Sum total of time system was down) /
  Total Number of Failures`.
- Use `MTTR = Total Maintenance Time / Total Number of Repairs`.
- Define RPO (acceptable data loss in time) and RTO (acceptable downtime) for
  every tiered service.
- For critical workloads target MTBF ≥ 50,000 hours; consumer workloads may be
  5,000–10,000.

**Don't:**
- Don't conflate availability (uptime %) with reliability (probability of
  working at any instant).
- Don't pick synchronous checkpointing when the dataset is too large to freeze
  writes (use async checkpointing + RPO-bounded replay).

**Code/formula reference:**
```
MTBF = (Total Elapsed Time − Downtime) / Failures
MTTR = Total Maintenance Time / Repairs
Synchronous checkpointing → blocks writes, consistent state
Asynchronous checkpointing → continuous, possible transient inconsistency
```
*Ref: System_Design_on_AWS.md — "Reliability" / "Fault Tolerance"*

---

### CAP and PACELC Theorems

**Principle:** In a partition, choose between consistency and availability;
otherwise, choose between latency and consistency.

**Do:**
- Use PACELC for nuanced design: `if (Partition) { A vs C } else { L vs C }`.
- Pre-decide the failure mode of every distributed datastore (CP or AP).
- Pair every CP system with a degraded mode (read-only, cached, queue).

**Don't:**
- Don't oversimplify CAP to "pick two of three" — partition tolerance is
  mandatory in distributed systems.
- Don't ignore the "else" branch (L vs C) when reasoning about steady-state
  latency.

```
CAP:  during partition → Consistency XOR Availability
PACELC:
  P (partition) → choose A or C
  E (else)       → choose Latency or Consistency
```
*Ref: System_Design_on_AWS.md — "CAP theorem" / "PACELC theorem"*

---

### Fallacies of Distributed Computing

**Principle:** Eight recurring false assumptions break distributed systems.
Each AWS Well-Architected pillar neutralises a specific fallacy.

**Do:**
- Treat the network as unreliable — retry, idempotency, and timeouts are
  mandatory.
- Assume non-zero latency; place compute near data and data near users.
- Treat bandwidth as finite; compress, paginate, use efficient formats.
- Build with security-first defaults (TLS, IAM least privilege, threat model).
- Abstract topology behind service discovery; assume nodes churn.

**Don't:**
- Don't assume a single administrator; build decoupled, team-owned services.
- Don't ignore zero transport cost in capacity plans.
- Don't assume a homogeneous network — interoperability tests are mandatory.

**The eight fallacies → Well-Architected pillar mapping:**
```
1. Reliable network          → Reliability pillar
2. Zero latency              → Performance Efficiency pillar
3. Infinite bandwidth        → Performance Efficiency pillar
4. Secure network            → Security pillar
5. Fixed topology            → Reliability pillar
6. Single administrator      → Operational Excellence pillar
7. Zero transport cost       → Cost Optimization + Sustainability pillars
8. Homogeneous network       → Operational Excellence pillar
```
*Ref: System_Design_on_AWS.md — "Fallacies of Distributed Computing"*

---

### System Design Guidelines

**Principle:** Trade-offs are inevitable; encapsulate them behind simple,
modular, observable interfaces.

**Do:**
- **Isolation (modularity):** split into independently deployable components.
- **Simplicity (KISS):** identify core requirements, minimise components,
  avoid over-engineering, test and refine.
- **Performance (metrics):** measure first; observe latency p50/p90/p99/p999
  before optimizing.
- **Trade-offs (TINSTAAFL):** explicitly capture cost vs scalability,
  performance vs maintainability, latency vs consistency.
- **Use cases ("It always depends"):** avoid silver bullets; pick the simplest
  design that meets today's SLOs.

**Don't:**
- Don't optimize for hypothetical future scale at the expense of today's
  velocity.
- Don't skip benchmarking; "metrics don't lie" — intuition does.

```
Guideline of Isolation    → Microservices + clear interfaces
Guideline of Simplicity   → KISS; ship MVP first
Guideline of Performance  → Capture p50/p90/p99; tune the tail
Guideline of Trade-offs   → TINSTAAFL; no free lunch
Guideline of Use Cases    → "It always depends"
```
*Ref: System_Design_on_AWS.md — "System Design Guidelines"*

---

### Time vs Space / Latency vs Throughput Trade-offs

**Principle:** Pick percentiles (not averages) and reason about p90/p99 for
both latency and throughput.

**Do:**
- Use percentiles to capture latency under load (`p50`, `p90`, `p99`, `p999`).
- Aim for maximum throughput within acceptable latency.
- Use lookup tables / memoisation when read-heavy and recompute is expensive.

**Don't:**
- Don't optimise average latency — outliers dominate user perception.
- Don't treat bandwidth as the throughput ceiling; throughput is empirical.

```
Response Time  = Latency + Processing Time
p90 latency    = 90% of requests complete within this time
Throughput ≤ Bandwidth
```
*Ref: System_Design_on_AWS.md — "Time Versus Space" / "Latency Versus Throughput"*

---

### Storage Formats: File, Block, Object

**Principle:** Choose storage format by access pattern, not by familiarity.

**Do:**
- **File storage** (e.g., Amazon EFS): hierarchical shared filesystem, NFS-style.
- **Block storage** (e.g., Amazon EBS): low-latency, OS-level volumes for
  databases.
- **Object storage** (e.g., Amazon S3): HTTP API, virtually unlimited scale,
  immutable objects.

**Don't:**
- Don't put relational databases on object storage.
- Don't use block storage for static web assets — S3 + CloudFront is cheaper.
- Don't modify objects in place — object storage is write-once-read-many.

| Format | Use | AWS service |
|--------|-----|-------------|
| File | Shared filesystem, lift-and-shift | EFS, FSx |
| Block | Databases, boot volumes, low-latency IO | EBS |
| Object | Backups, static assets, data lake, logs | S3 |

*Ref: System_Design_on_AWS.md — "File-Based Storage" / "Block-Based Storage" / "Object-Based Storage"*

---

### ACID and BASE

**Principle:** Pick ACID for correctness-critical OLTP; pick BASE for
scale-critical OLTP/web.

**Do:**
- Use **ACID** (Atomicity, Consistency, Isolation, Durability) for finance,
  inventory, reservations.
- Use **BASE** (Basically Available, Soft state, Eventually consistent) for
  social feeds, counters, recommendations.

**Don't:**
- Don't assume BASE is "weak ACID" — it is a deliberate trade-off for
  availability and partition tolerance.
- Don't mix isolation levels across services without documenting.

```
ACID:  Atomicity, Consistency, Isolation, Durability  → RDBMS
BASE:  Basically Available, Soft state, Eventually consistent → NoSQL
```
*Ref: System_Design_on_AWS.md — "ACID" / "BASE"*

---

### Relational Database Concepts

**Principle:** Use the relational model when data has well-defined schema,
strong relationships, and transactional integrity requirements.

**Do:**
- Define primary keys, foreign keys, indexes, constraints, views, transactions.
- Choose isolation levels deliberately: Read Uncommitted < Read Committed <
  Repeatable Read < Serializable.
- Normalise to 3NF first; denormalise only with measurable justification.

**Don't:**
- Don't store JSON blobs when relations and joins matter.
- Don't skip foreign key constraints and rely on application-layer integrity.
- Don't over-normalise for read-heavy analytical workloads.

```
SQL categories:
  DDL  → CREATE / ALTER / DROP
  DML  → SELECT / INSERT / UPDATE / DELETE
  DCL  → GRANT / REVOKE
  TCL  → COMMIT / ROLLBACK / SAVEPOINT
```
*Ref: System_Design_on_AWS.md — "Relational Database Concepts"*

---

### RDBMS Architecture Components

**Principle:** Treat the RDBMS as a stack of specialised components — query
planner, executor, storage engine, transaction manager, recovery manager.

**Do:**
- Profile slow queries via `EXPLAIN`/`EXPLAIN ANALYZE`.
- Size the buffer pool and cache for hot pages.
- Use the recovery manager's WAL (write-ahead log) for crash safety.
- Use the concurrency control manager to set isolation level per workload.

**Don't:**
- Don't bypass the query optimiser with ORM-generated SQL blindly.
- Don't disable logging — durability depends on it.

```
Query → Parser → AST → Optimizer → Plan → Executor → Storage Engine → Buffer/Cache
                                  ↑
                       Concurrency + Recovery + Security managers
```
*Ref: System_Design_on_AWS.md — "Relational Database Management System Architecture"*

---

### Indexing (B+ Trees) and SQL Tuning

**Principle:** Indexes speed reads but tax writes; tune for the dominant
workload.

**Do:**
- Index columns used in `SELECT`, `GROUP BY`, `ORDER BY`, `JOIN`.
- Use composite (multi-column) indexes for combined predicates.
- Drop indexes before bulk loads; rebuild after.
- Use B+ tree's sorted leaf nodes for range scans and prefix matches.

**Don't:**
- Don't index low-cardinality columns (e.g., `is_active` boolean).
- Don't write in huge transactions; batch and commit.
- Don't run heavy analytical queries during peak OLTP hours.

```sql
-- Drop indexes before bulk loads (PostgreSQL)
DROP INDEX IF EXISTS idx_orders_user;
COPY orders FROM '/data/orders.csv';
CREATE INDEX idx_orders_user ON orders(user_id);
```
*Ref: System_Design_on_AWS.md — "Indexes" / "SQL tuning"*

---

### Denormalization and Federation

**Principle:** Denormalise for read-heavy workloads; federate queries across
schemas.

**Do:**
- Use denormalisation + cascading triggers / constraints to avoid costly joins.
- Use query federation when queries naturally span multiple schemas/servers.
- Document redundancy, because updates get harder.

**Don't:**
- Don't denormalise prematurely — start normalised and only denormalise on
  measured bottleneck.
- Don't let redundant copies drift; use unique constraints + cascade updates.

```
Read-heavy (100:1 or 1000:1 read:write) → denormalise
Federation → split one logical schema across multiple physical stores
```
*Ref: System_Design_on_AWS.md — "Denormalization" / "Query federation"*

---

### Partitioning (Vertical, Horizontal, Hash, Range)

**Principle:** Partition to scale both query performance and dataset size.

**Do:**
- **Vertical partitioning:** split columns (e.g., `customer_info`,
  `customer_contact`).
- **Horizontal partitioning:** split rows by hash or range.
- Use **hash partitioning** for uniform distribution, no range queries.
- Use **range partitioning** for time/lexicographic range scans.

**Don't:**
- Don't pick a hash partition key with low cardinality (hot partition).
- Don't create range partitions with skewed access (e.g., `email` starting
  with "A" concentrates load).
- Don't expose partition topology to clients without a coordinator/router.

```
Hash:    H(key) mod N       → uniform, no range scans
Range:   [k1,k2), [k2,k3)   → supports range scans, hot-spot risk
```
*Ref: System_Design_on_AWS.md — "Partitioning"*

---

### Sharding

**Principle:** Sharding = horizontal partitioning across independent servers.

**Do:**
- Choose shard key by query pattern (user ID, tenant ID, geographic location).
- Use consistent hashing for minimal data movement during rebalance.
- Plan for shard rebalancing; design the client/router to handle remapping.

**Don't:**
- Don't shard by attributes that grow disproportionately (e.g., a single
  "celebrity" user).
- Don't make cross-shard joins the default — denormalise or co-locate.
- Don't shard before you must; the operational cost is real.

| Shard strategy | Pros | Cons |
|----------------|------|------|
| Hash-based | Even distribution | No range queries |
| Range-based | Range scans | Hot spots |
| Round-robin | Simple | No locality |

*Ref: System_Design_on_AWS.md — "Sharding"*

---

### Replication: Single-Leader, Multi-Leader, Sync vs Async

**Principle:** Replicate for availability, load distribution, and reduced
latency; choose sync vs async by durability vs latency tolerance.

**Do:**
- Use **single-leader** for read-heavy scale-out.
- Use **multi-leader** for write availability across regions.
- Use **synchronous replication** when zero data loss is mandatory (financial).
- Use **asynchronous replication** for performance, accepting bounded staleness.

**Don't:**
- Don't promote an async replica without checking replication lag.
- Don't assume "read replicas are cheap" — they replay writes and add load.

```
Availability (sequential): A_total = ∏ A_i
Availability (parallel):   A_total = 1 − ∏ (1 − A_i)
```
*Ref: System_Design_on_AWS.md — "Replication" / "Synchronous replication" / "Asynchronous replication"*

---

### MySQL vs PostgreSQL

**Principle:** Choose by read/write mix, JSON support, replication model, and
team familiarity.

**Do:**
- Pick **MySQL** for read-heavy OLTP, simpler replication, raw speed.
- Pick **PostgreSQL** for advanced types (jsonb, arrays, user-defined types),
  expression/partial indexes, 2-safe sync replication.
- Use **jsonb** in PostgreSQL for document-style data inside a relational model.

**Don't:**
- Don't pick MySQL just because "everyone uses it"; benchmark for your workload.
- Don't assume PostgreSQL's process-per-connection scales linearly with
  connection count.

| Property | MySQL | PostgreSQL |
|----------|-------|------------|
| Replication | Async, one-way, primary/secondary | Sync 2-safe, primary/secondary |
| Concurrency | Thread per connection | Process per connection |
| JSON | Generated column workaround | Native `jsonb` + indexing |
| Indexes | Up to 16 columns | Up to 32, plus expression/partial |
| Best for | Read-heavy, simple joins | Write-heavy, complex types |

*Ref: System_Design_on_AWS.md — Table 2-1 "MySQL versus PostgreSQL"*

---

### NoSQL: Schema Flexibility, Data Models

**Principle:** NoSQL trades rigid schema and strong consistency for horizontal
scale and developer velocity.

**Do:**
- Choose by access pattern: key-value, document, column-family, graph.
- Use document stores (MongoDB/DocumentDB) for flexible nested JSON.
- Use column-family (Cassandra/Keyspaces/DynamoDB) for wide rows and time series.
- Use graph (Neptune, Neo4j) for highly connected data (social, recommendations).

**Don't:**
- Don't pick NoSQL just because "it scales"; relational may still be right.
- Don't assume NoSQL is "schemaless" — schema design is still essential.

| Type | Example | AWS service |
|------|---------|-------------|
| Key-value | DynamoDB | Amazon DynamoDB |
| Document | MongoDB | Amazon DocumentDB |
| Column | Cassandra | Amazon Keyspaces |
| Graph | Neo4j/TinkerPop | Amazon Neptune |
| Time-series | Influx | Amazon Timestream |
| Search | Elasticsearch | Amazon OpenSearch |

*Ref: System_Design_on_AWS.md — "Nonrelational Database Concepts"*

---

### Key-Value Store Operations

**Principle:** Model data with the right primary key, partition key, and
optional sort key to match access patterns.

**Do:**
- Define a **primary key** (unique) and a **partition key** (for distribution).
- Add a **sort key** for range queries within a partition.
- Use `GetItem`, `PutItem`, `UpdateItem`, `DeleteItem` semantics deliberately.
- Use condition expressions on `PutItem` to avoid silent overwrites.

**Don't:**
- Don't access key-value stores by non-key attributes without a secondary index.
- Don't use a low-cardinality partition key — it becomes a hot partition.

```
Partition key = {short URL}
Sort key      = SU  (constant string allows same partition for other entries)
```
*Ref: System_Design_on_AWS.md — "Key-Value Databases"*

---

### Leaderless Replication: Quorum, Consistent Hashing, Hinted Handoff

**Principle:** Distribute writes across replicas; reconcile with quorum.

**Do:**
- Configure `W + R > N` for strong-read consistency (N replicas, W writes
  acknowledged, R reads).
- Use consistent hashing to minimise data movement on add/remove nodes.
- Use hinted handoff for transient node failures.

**Don't:**
- Don't pick W=R=1 unless you accept potential data loss.
- Don't rebuild cluster topology on every request — cache it.

```
Strong read:  W + R > N
Tunable:      W=R=N/2+1 (sloppy quorum)
```
*Ref: System_Design_on_AWS.md — "DynamoDB internal architecture" / "Wide-Column Stores"*

---

### Caching Strategies

**Principle:** Pick the caching strategy by read/write intensity and tolerance
for staleness.

**Do:**
- **Cache-aside (lazy):** app checks cache, falls back to DB; app writes back
  on miss.
- **Read-through:** cache itself populates from source on miss.
- **Refresh-ahead:** cache pre-fetches hot items before they expire (best
  p999).
- **Write-through:** cache + DB updated synchronously (strong consistency,
  more latency).
- **Write-around:** bypass cache on writes (less pollution).
- **Write-back:** cache updated, DB updated asynchronously (fast writes, risk
  of loss).

**Don't:**
- Don't use write-back for financial data.
- Don't pick cache-aside + TTL only if strict freshness is required — use
  invalidate-on-write.

| Strategy | Read | Write | Freshness |
|----------|------|-------|-----------|
| Cache-aside | Lazy | App populates | TTL-bounded |
| Read-through | Lazy | Cache populates | TTL-bounded |
| Refresh-ahead | Proactive | Cache populates | TTL + warm |
| Write-through | Always fresh | Sync to source | Strong |
| Write-around | Cache miss possible | Bypass | Stale on read |
| Write-back | Async | Cache, then DB | Eventual |

*Ref: System_Design_on_AWS.md — "Caching Strategies" / Figure 4-1*

---

### Cache Invalidation

**Principle:** There are only two hard things in CS — cache invalidation and
naming things.

**Do:**
- Use **active invalidation** for precise, on-event purge.
- Use **invalidate on modification** for immediate freshness.
- Use **invalidate on read** for paranoid freshness.
- Use **TTL** for time-based bounded staleness (e.g., weather data, 30 min).

**Don't:**
- Don't use TTL alone for transactional data.
- Don't forget to invalidate after delete (not just update).

```
Active invalidation     → precise, ops burden
Invalidate on modify    → immediate freshness
Invalidate on read      → always fresh, expensive
TTL-based invalidation  → simple, bounded staleness
```
*Ref: System_Design_on_AWS.md — "Cache Invalidation"*

---

### Content Delivery Networks (Push vs Pull)

**Principle:** Use a CDN to reduce latency, offload origin, and absorb traffic.

**Do:**
- Use **push CDN** when content is known ahead of time (predictable demand).
- Use **pull CDN** for high-traffic, on-demand content (first request to origin,
  subsequent from edge).
- Set appropriate TTL via HTTP headers or DNS records.
- Use CloudFront with Origin Shield for high cache-hit ratio.

**Don't:**
- Don't serve user-specific dynamic data from CDN without edge logic.
- Don't set TTL longer than content staleness tolerance.

```
Pull CDN:  Edge ← origin (on miss); cached for TTL
Push CDN:  origin → edge (proactive); used for known-good content
```
*Ref: System_Design_on_AWS.md — "Push CDN" / "Pull CDN"*

---

### Load Balancer Types (L4 vs L7)

**Principle:** Match LB type to traffic visibility needs.

**Do:**
- Use **L4 (Network LB)** for TCP/UDP, extreme throughput, WebSocket, gaming.
- Use **L7 (Application LB)** for HTTP routing by path/host/header, SSL
  offload, cookie affinity.
- Use **Direct Server Return** (DSR) mode for large response sizes.
- Use **NAT mode** when the LB must be the default gateway.

**Don't:**
- Don't terminate TLS at the LB if backend needs end-to-end encryption.
- Don't use sticky sessions unless required — they hurt horizontal scale.

| Type | L4 (NLB) | L7 (ALB) |
|------|----------|----------|
| OSI layer | Transport | Application |
| Termination | No | Yes |
| Routing | IP/port | HTTP path/host/header |
| Use case | TCP, UDP, WebSocket | HTTP APIs, microservices |

*Ref: System_Design_on_AWS.md — "Network load balancers" / "Application load balancers"*

---

### Load Balancer Algorithms

**Principle:** Match algorithm to traffic stability and server capability.

**Do:**
- **Round-robin** for identical backends.
- **Weighted round-robin** for heterogeneous backends.
- **Least connections** when session length varies.
- **Least response time** for heterogeneous backend speeds.
- **IP hash** for source-affinity (use sparingly — rebalance pain).

**Don't:**
- Don't use IP hash with NAT/CGN — affinity breaks.
- Don't use static algorithms when servers have very different capacities.

*Ref: System_Design_on_AWS.md — "Static vs Dynamic Load Balancing Algorithms"*

---

### Stateful vs Stateless Load Balancers

**Principle:** Prefer stateless LBs; offload session state to Redis/ElastiCache.

**Do:**
- Use **stateless LB** + distributed cache (Redis) for session state.
- Use cookie-based or source-IP affinity only when mandated.
- Reuse SGs; avoid duplicate-rules SGs.

**Don't:**
- Don't store session state on the LB when you can use Redis.
- Don't underestimate the operational cost of stateful LBs at scale.

```
Stateless LB + Redis session  → scalable, simple
Stateful LB (sticky session)   → simpler app, harder ops
```
*Ref: System_Design_on_AWS.md — "Stateful Load Balancers" / "Stateless Load Balancers"*

---

### Network Protocols: OSI and TCP/IP

**Principle:** Match protocol to latency, reliability, and ordering needs.

**Do:**
- Use **TCP** for reliable, ordered, full-duplex (HTTP, DB, SSH).
- Use **UDP** for latency-critical loss-tolerant traffic (VoIP, video, DNS,
  gaming).
- Deploy close to users (same region, low RTT).
- Validate ICMP reachability with `ping` before deeper diagnostics.

**Don't:**
- Don't use UDP where packet loss breaks correctness (financial ledgers).
- Don't use TCP where the 3-way handshake RTT dominates (live video).

```
TCP 3-way handshake:  SYN → SYN-ACK → ACK
UDP:                  no handshake; send-and-forget
```
*Ref: System_Design_on_AWS.md — "OSI Model" / Table 6-1 / "TCP" / "UDP"*

---

### HTTP, REST, and Idempotency

**Principle:** Use the right HTTP verb and make destructive methods idempotent.

**Do:**
- `GET` (idempotent) for retrieval.
- `POST` for create / non-idempotent actions.
- `PUT` for full update (idempotent).
- `DELETE` for removal (idempotent).
- Validate API responses with explicit HTTP status codes.

**Don't:**
- Don't mutate state in a `GET`.
- Don't assume `POST` is naturally idempotent — add idempotency keys for
  payments.

```
GET /api/orders?id=23234555&customerId=dhfsd348e4
Host: api.myFoodApp.com
Authorization: Bearer MyAccessToken
Accept: application/json
```
*Ref: System_Design_on_AWS.md — "Hypertext Transfer Protocol"*

---

### Containerization and Orchestration

**Principle:** Containers package; orchestrators schedule, scale, heal.

**Do:**
- Use containers for immutable, reproducible deployments.
- Use ECS (AWS-native) or EKS (Kubernetes) for orchestration.
- Use Fargate to remove node management overhead.
- Use EKS spot instances for cost savings (up to 90%).

**Don't:**
- Don't store state inside containers; mount EBS/EFS or use external stores.
- Don't run containers without health checks and restart policies.

*Ref: System_Design_on_AWS.md — "Containerization" (Chapter 7 overview)*

---

### Microservices, Choreography vs Orchestration

**Principle:** Prefer choreography (events) for loosely coupled flows;
orchestration for visibility/control.

**Do:**
- Decompose by subdomain; one bounded context per service.
- Use events (SNS/SQS/EventBridge/Kafka) for cross-service reactions.
- Use orchestrators (Step Functions) when explicit state machine + retries
  matter.
- Keep each service independently deployable and observable.

**Don't:**
- Don't share a single database between services.
- Don't synchronously chain more than a few services in a request path.
- Don't introduce microservices until monolith pain is real.

```
Choreography:  Service A → event → Service B → event → Service C
Orchestration: Coordinator → Service A → Service B → Service C
```
*Ref: System_Design_on_AWS.md — "Microservices" / "Choreography and Orchestration"*

---

### Event-Driven Architecture and Event Sourcing

**Principle:** Treat state changes as immutable events; derive state by replay.

**Do:**
- Keep an append-only event log (event store / Kafka / DynamoDB Streams).
- Apply snapshots for long-running aggregates to keep replay bounded.
- Make consumers idempotent (event IDs).
- Use causal ordering when multiple publishers exist.

**Don't:**
- Don't mutate events; add new ones to correct.
- Don't forget consumer idempotency — duplicates are inevitable.

```
event store: [E1, E2, E3, ...] → fold → current state
snapshot:    every N events → fast hydration
```
*Ref: System_Design_on_AWS.md — "Event-Driven Architecture" / "Event sourcing"*

---

### CQRS and Saga

**Principle:** Separate reads from writes; manage distributed transactions with
compensating steps.

**Do:**
- Use **CQRS** when read/write shapes diverge (e.g., write-normalised, read-
  denormalised).
- Use **Saga** (orchestration or choreography) for multi-service transactions
  with eventual consistency.
- Pair every saga step with a compensating action.

**Don't:**
- Don't use CQRS for trivial CRUD — it adds complexity.
- Don't pick saga for two-step transactions where a single DB transaction
  suffices.

```
Saga orchestration:
  Step 1 → Step 2 → Step 3
       ↘       ↘       ↘
   Compensate Compensate Compensate
```
*Ref: System_Design_on_AWS.md — "Event-Based Patterns: CQRS and Saga"*

---

### Circuit Breaker, Retry with Backoff, Rate Limiter

**Principle:** Fail fast, retry with backoff, cap the request rate.

**Do:**
- Implement circuit breaker (Closed → Open → Half-Open) to prevent cascade.
- Retry with exponential backoff and jitter; cap max retries.
- Rate-limit per user, per service, globally; prioritise critical traffic.

**Don't:**
- Don't retry non-idempotent operations without idempotency keys.
- Don't open circuit breakers on cold start — that's latency, not failure.

```
Retry:   t = base * 2^n ± jitter; cap at max_retries
Breaker: failure_rate > threshold → OPEN; after cooldown → HALF_OPEN
```
*Ref: System_Design_on_AWS.md — "Failure-Tolerant Patterns"*

---

### DDD, BFF, Strangler Fig, Anti-Corruption Layer

**Principle:** Align software boundaries with business boundaries; isolate
legacy and external models.

**Do:**
- Apply **DDD** (bounded contexts, ubiquitous language) for complex domains.
- Use **BFF** for separate mobile vs web backends (different payloads).
- Use **Strangler Fig** to migrate monolith → microservices incrementally.
- Use **Anti-Corruption Layer (ACL)** between old and new systems to keep the
  domain model clean.

**Don't:**
- Don't let a third-party API's schema leak into your domain model.
- Don't do a big-bang migration; do it behind a router.

*Ref: System_Design_on_AWS.md — "Other Cloud Architecture Patterns"*

---

### HDFS Architecture

**Principle:** Use HDFS for big-data batch processing with rack-aware
replication.

**Do:**
- NameNode + DataNodes + Secondary NameNode (or HA NameNode).
- Default replication factor = 3, block size 128 MB.
- Place replicas across racks for fault tolerance.

**Don't:**
- Don't store hot, low-latency data on HDFS — use HBase or DynamoDB.
- Don't run critical jobs on a single NameNode without HA.

```
HDFS:  NameNode (metadata) → DataNodes (blocks, 128 MB, RF=3)
                            Secondary NameNode (metadata checkpoints)
```
*Ref: System_Design_on_AWS.md — "HDFS" / Figure 8-8*

---

### Kafka Architecture

**Principle:** Use Kafka for durable, ordered, replayable streaming.

**Do:**
- Partition topics; key-based partitioning preserves per-key ordering.
- Set `acks=all` for durability; `replication.factor ≥ 3`.
- Use idempotent producers + transactions for exactly-once.
- Configure retention by time (e.g., 7 days) or size (e.g., 100 GB).

**Don't:**
- Don't assume ordering across partitions (only within partition).
- Don't set retention to "forever" without sizing the cluster.

```sql
-- DDL for KGS ticket servers (Flickr-style)
CREATE TABLE `Tickets64` (
  `id`  bigint(20) unsigned NOT NULL auto_increment,
  `stub` char(1) NOT NULL default '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `stub` (`stub`)
) ENGINE=InnoDB;
REPLACE INTO Tickets64 (stub) VALUES ('a');
SELECT LAST_INSERT_ID();
```
*Ref: System_Design_on_AWS.md — "Apache Kafka" / Figure 8-9*

---

### AWS Global Infrastructure

**Principle:** Use regions and AZs as the basis for HA and compliance.

**Do:**
- Pick the region closest to users for latency, or required for data residency.
- Spread workloads across ≥ 2 AZs for HA; consider Local Zones for ultra-low
  latency in metros.
- Use edge locations (CloudFront / Route 53 PoPs) for content and DNS.

**Don't:**
- Don't assume a service is available in every region — check the regional
  product availability first.
- Don't run a single-AZ deployment for production.

```
Region → Availability Zones (us-east-1a, us-east-1b, ...)
Region → Local Zones (specific metros)
Region → Edge Locations (CloudFront / Route 53 PoPs)
```
*Ref: System_Design_on_AWS.md — "AWS Regions" / "AWS Availability Zones" / "AWS Local Zones" / "AWS Edge Locations"*

---

### Amazon VPC, Subnets, Routing

**Principle:** Treat VPC as your private data center; use public/private
subnets deliberately.

**Do:**
- Plan CIDR (RFC 1918) with growth in mind; min /28, max /16 per VPC.
- Use one route table per logical tier; main route table is implicit.
- Use direct IGW route (public subnet) vs NAT gateway route (private subnet).
- Keep one subnet per AZ for high availability.

**Don't:**
- Don't overlap CIDR blocks across peered/transit-gateway VPCs.
- Don't assign public IPs to private-subnet resources.

```
Public subnet  → route 0.0.0.0/0 → igw-id
Private subnet → route 0.0.0.0/0 → nat-gw-id
```
*Ref: System_Design_on_AWS.md — "Creating an Amazon VPC" / "Subnets" / "Route Tables"*

---

### Security Groups and NACLs

**Principle:** Layer defence-in-depth: stateful SGs + stateless NACLs.

**Do:**
- Use **Security Groups** at the instance level (stateful, allow rules only).
- Use **NACLs** at the subnet level (stateless, allow + deny, evaluated in
  rule-number order).
- Restrict SSH (port 22) to specific IPs, not `0.0.0.0/0`.
- Add `Description` to every rule for audit.

**Don't:**
- Don't expect SGs to deny explicitly (no deny rule) — use NACL for explicit
  deny.
- Don't add ephemeral port ranges unless you understand the response path
  (NACL stateless).

```
SG   → stateful, instance-level, allow-only
NACL → stateless, subnet-level, allow + deny, ordered rules
```
*Ref: System_Design_on_AWS.md — "Security Groups" / "Network Access Control Lists"*

---

### NAT Gateway and Internet Gateway

**Principle:** Use IGW for public subnet egress; NAT GW for private subnet
egress.

**Do:**
- Deploy NAT Gateway per AZ for HA and to avoid the 10M pps per-NAT limit.
- Allocate an Elastic IP for each NAT gateway.
- Use NAT gateway public/private variants for VPC + on-prem access.

**Don't:**
- Don't terminate a single NAT gateway in one AZ for the entire VPC.
- Don't use NAT for AWS service access — use VPC endpoints (PrivateLink)
  instead.

*Ref: System_Design_on_AWS.md — "Internet Gateway" / "NAT gateway"*

---

### Cross-VPC Connectivity (Peering, Transit Gateway, PrivateLink)

**Principle:** Match connectivity mechanism to traffic pattern.

**Do:**
- Use **VPC Peering** for 1:1, non-transitive, same- or cross-region.
- Use **Transit Gateway** for hub-and-spoke, transitive, many VPCs.
- Use **PrivateLink** for unidirectional service exposure, no CIDR overlap
  concerns.

**Don't:**
- Don't chain VPC peering (no transitive routing) — use Transit Gateway.
- Don't share resources across VPCs without IAM + SG controls.

*Ref: System_Design_on_AWS.md — "Connectivity Between Amazon VPCs"*

---

### Amazon Route 53

**Principle:** Use Route 53 for DNS, health checks, and traffic policies.

**Do:**
- Use latency-based or geolocation routing for global apps.
- Use weighted routing for blue/green or percentage rollouts.
- Use health checks to fail over away from unhealthy endpoints.

**Don't:**
- Don't rely solely on DNS for HA (clients cache).
- Don't create CNAMEs at the zone apex — use alias records.

*Ref: System_Design_on_AWS.md — "Amazon Route 53" (Chapter 9)*

---

### Elastic Load Balancing (ALB, NLB, GLB)

**Principle:** Pick the LB family by traffic visibility and target type.

**Do:**
- **ALB** for HTTP/HTTPS, path/host/header routing, WAF integration.
- **NLB** for TCP/UDP, ultra-high throughput, static IPs, PrivateLink.
- **GLB (Gateway Load Balancer)** for third-party virtual appliances.

**Don't:**
- Don't use ALB for raw TCP — use NLB.
- Don't expose ALB directly to the internet without WAF + Shield.

*Ref: System_Design_on_AWS.md — "AWS Elastic Load Balancer"*

---

### Amazon API Gateway

**Principle:** Use API Gateway as the public façade for serverless APIs.

**Do:**
- Use API Gateway with Lambda (REST/HTTP/WebSocket).
- Configure caching TTL (0–3600s, default 300).
- Use IAM auth, Lambda authorizers, or Cognito user pools.
- Integrate WAF for SQL injection / XSS protection.
- Connect API Gateway directly to DynamoDB for proxy-without-Lambda patterns.

**Don't:**
- Don't exceed 29s timeout (REST) / 30s (HTTP) — redesign for async.
- Don't put long-running synchronous work behind API Gateway.

```
API Gateway REST timeout: 50 ms – 29 s
HTTP API timeout:        up to 30 s
WebSocket idle timeout:  10 min; max connection 2 h
```
*Ref: System_Design_on_AWS.md — "Amazon API Gateway"*

---

### Amazon CloudFront

**Principle:** Use CloudFront as the global edge cache + DDoS shield.

**Do:**
- Terminate SSL/TLS at CloudFront; use ACM certificates.
- Use Origin Shield between origin and regional edge caches.
- Use signed URLs / signed cookies / georestriction for controlled access.
- Pair with S3 (origin) for static content.

**Don't:**
- Don't bypass CloudFront and hit S3 directly from clients.
- Don't serve personalised dynamic content from cache without cache key
  customisation.

*Ref: System_Design_on_AWS.md — "Amazon CloudFront" / "Origin Shield"*

---

### Amazon S3 Storage Classes

**Principle:** Match storage class to access frequency and durability needs.

**Do:**
- Use **S3 Standard** for frequent access.
- Use **S3 Intelligent-Tiering** when access pattern is unknown.
- Use **S3 Standard-IA / One Zone-IA** for infrequent (≥30/90 days).
- Use **S3 Glacier Instant/ Flexible / Deep Archive** for cold archival.

**Don't:**
- Don't store hot, sub-second data in IA classes (higher per-request cost).
- Don't use One Zone-IA for data you cannot recreate.

| Class | Use | Retrieval |
|-------|-----|-----------|
| S3 Standard | Hot | ms |
| Intelligent-Tiering | Unknown | ms |
| Standard-IA | Infrequent | ms |
| Glacier Instant Retrieval | Archive | ms |
| Glacier Flexible Retrieval | Archive | min–hr |
| Glacier Deep Archive | Long-term | hr |

*Ref: System_Design_on_AWS.md — "Cloud Storage on AWS" (Chapter 10)*

---

### EBS and EFS

**Principle:** Pick block vs file by access pattern.

**Do:**
- Use **EBS** for single-AZ block volumes (databases, boot disks).
- Use **EFS** for shared POSIX file systems across AZs/instances.
- Take EBS snapshots; encrypt at rest with KMS.
- Use gp3 for general, io2 Block Express for high-IOPS.

**Don't:**
- Don't share EBS across AZs (single-AZ).
- Don't run a database on EFS — use EBS or instance store.

*Ref: System_Design_on_AWS.md — "EBS" / "EFS"*

---

### Amazon RDS and Aurora

**Principle:** Use managed relational DBs; lean on Multi-AZ, read replicas,
and parameter groups.

**Do:**
- Use Multi-AZ deployment for HA; read replicas for read scale.
- Enable encryption at rest with KMS; use SSL/TLS in transit.
- Use Aurora for MySQL/PostgreSQL-compatible with storage/compute separation.

**Don't:**
- Don't run primary writes on read replicas.
- Don't skip parameter group tuning; defaults are conservative.

*Ref: System_Design_on_AWS.md — "AWS Relational Databases"*

---

### Amazon DynamoDB

**Principle:** Model around access patterns; choose PK/SK deliberately.

**Do:**
- Pick partition key with high cardinality to avoid hot partitions.
- Use **on-demand** for unknown workloads; **provisioned + autoscaling** for
  predictable.
- Use **GSI** for alternate access; **LSI** only at table creation.
- Use **DAX** for microsecond reads on hot items.
- Use **TTL** for automatic expiry; **Streams** for change data.
- Use **global tables** for multi-region replication (≈1s lag).

**Don't:**
- Don't scan full tables in production — design a key for every query.
- Don't create LSIs after the fact; create at table creation.

| Capacity mode | When |
|---------------|------|
| On-demand | Unknown traffic |
| Provisioned + autoscaling | Predictable traffic |
| Provisioned fixed | Tight cost control |

*Ref: System_Design_on_AWS.md — "Amazon DynamoDB" / Table 10-1*

---

### DynamoDB Hot Partition Mitigations

**Principle:** Detect, then redesign or shim.

**Do:**
- Use CloudWatch Contributor Insights to find hot keys.
- Cache hot reads with ElastiCache / DAX.
- Add random suffix (1–100) to PK for write-heavy hot keys.
- Retry with exponential backoff on `ProvisionedThroughputExceededException`.

**Don't:**
- Don't redesign the schema mid-traffic without dual-write / cutover plan.

*Ref: System_Design_on_AWS.md — "Best practices for partition key design"*

---

### Amazon DocumentDB

**Principle:** Use DocumentDB for MongoDB-compatible document workloads with
transactional guarantees.

**Do:**
- Use ≥ 3 instances for production HA.
- Migrate from MongoDB with DMS.
- Use DocumentDB transactions across multiple documents.

**Don't:**
- Don't assume DocumentDB is wire-compatible with all MongoDB drivers — test.

| SQL term | DocumentDB |
|----------|------------|
| Table | Collection |
| Row | Document |
| Column | Field |
| Primary key | Object ID |

*Ref: System_Design_on_AWS.md — "Amazon DocumentDB" / Table 10-2*

---

### Amazon Neptune

**Principle:** Use Neptune for highly connected graph queries at scale.

**Do:**
- Use Gremlin (Apache TinkerPop) or openCypher for property graphs.
- Use SPARQL for RDF.
- Separate writer endpoint from reader endpoint (round-robin across replicas).
- Enable serverless for variable workloads.

**Don't:**
- Don't use Neptune for tabular OLTP — use RDS/Aurora.
- Don't bypass the dedicated cluster endpoint for writes.

*Ref: System_Design_on_AWS.md — "Amazon Neptune"*

---

### Amazon ElastiCache (Redis vs Memcached)

**Principle:** Choose Redis for persistence + advanced types; Memcached for
simple, multithreaded cache.

**Do:**
- Use **Redis** for persistence, pub/sub, sorted sets, geospatial, streams.
- Use **Memcached** for simple key-value cache with multithreading on big nodes.
- Enable **data tiering** (R6gd) for 20% hot / 80% cold access patterns.
- Use Redis cluster mode for horizontal scale (≤500 nodes).

**Don't:**
- Don't launch Memcached in public subnets (no auth/encryption).
- Don't rely on Memcached for persistence — it is pure cache.

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Persistence | Yes | No |
| Threading | Single | Multi |
| Advanced types | Yes | No |
| Compliance | PCI DSS / HIPAA / FedRAMP | Limited |

*Ref: System_Design_on_AWS.md — "Amazon ElastiCache"*

---

### Amazon OpenSearch

**Principle:** Use OpenSearch for full-text search, log analytics, and
observability.

**Do:**
- Use odd number of dedicated cluster manager nodes (≥ 3) for production.
- Use EBS or instance store; choose based on instance family.
- Use VPC access; restrict via SG.
- Enable SAML or Cognito authentication for dashboards.

**Don't:**
- Don't skip dedicated cluster manager nodes for prod to save cost.
- Don't run heavy indexing traffic during peak read windows.

*Ref: System_Design_on_AWS.md — "Amazon OpenSearch"*

---

### Amazon Timestream and Keyspaces

**Principle:** Use Timestream for time-series, Keyspaces for Cassandra-compatible.

**Do:**
- Timestream: enable retention policies; tier to magnetic store.
- Timestream: use interpolation/smoothing SQL functions for trends.
- Keyspaces: pick provisioned + autoscaling or on-demand; data encrypted by
  default, replicated across AZs.

**Don't:**
- Don't delete/update Timestream records; rely on retention.
- Don't manage Keyspaces with Cassandra internals (JVM tuning) — it's serverless.

*Ref: System_Design_on_AWS.md — "Amazon Timestream" / "Amazon Keyspaces"*

---

### Amazon EC2: AMI, Instance Type, Tenancy

**Principle:** Choose instance type by workload shape; use AMIs as immutable
baselines.

**Do:**
- Use Nitro for performance + security; bare metal when compliance requires.
- Bake dependencies into a base AMI (vs post-launch script).
- Use **dedicated tenancy** only for compliance or licensing; default **shared**.
- Pick instance family by workload:
  - General purpose (M family)
  - Compute optimised (C family)
  - Memory optimised (R/X family)
  - Storage optimised (I family)
  - Accelerated / GPU (P/G family)

**Don't:**
- Don't bake secrets into AMIs.
- Don't run a single EC2 for production — use ≥ 2 across AZs.

*Ref: System_Design_on_AWS.md — "Amazon Elastic Compute Cloud"*

---

### Auto Scaling and Spot Instances

**Principle:** Scale horizontally with metrics; use spot for fault-tolerant
workloads.

**Do:**
- Define min/desired/max in the ASG; cooldown defaults to 300s.
- Scale on CPU, network, or custom CloudWatch metrics.
- Use **spot instances** for up to 90% discount on fault-tolerant workloads.
- Use **reserved instances / Savings Plans** (1- or 3-year) for steady-state.
- Mix spot + on-demand for capacity certainty + cost.

**Don't:**
- Don't rely solely on autoscaling for spiky traffic — prescale for known
  events.
- Don't put HDFS on spot (data loss risk on reclamation).

*Ref: System_Design_on_AWS.md — "Autoscaling" / "Instance Type"*

---

### AWS Lambda

**Principle:** Use Lambda for event-driven, short-lived, bursty workloads.

**Do:**
- Package as zip (≤ 250 MB) or container image (≤ 10 GB).
- Choose ARM64 (Graviton) for cost + perf efficiency.
- Use **provisioned concurrency** to eliminate cold starts.
- Configure destinations (SQS, SNS, Lambda, EventBridge) for async failures.
- Use layers to share common code across functions.

**Don't:**
- Don't run long jobs (max 15 min) — use ECS/Batch/Fargate.
- Don't put secrets in environment variables unencrypted — use Secrets Manager
  / SSM Parameter Store.

```
Invocation modes:
  Sync  → API Gateway, ALB, CLI  (caller waits)
  Async → S3, SNS, EventBridge    (immediate ack)
  Poll  → SQS, Kinesis, Kafka     (Lambda polls)
```
*Ref: System_Design_on_AWS.md — "AWS Lambda"*

---

### Containers: ECS, EKS, Fargate

**Principle:** Choose by Kubernetes familiarity and operational appetite.

**Do:**
- **ECS**: AWS-native, simpler, lower ops burden.
- **EKS**: managed Kubernetes, when portability or K8s ecosystem matters.
- **Fargate**: serverless containers — no EC2 management.
- Use EKS Fargate or ECS Fargate for variable workloads; EC2 for steady-state
  cost efficiency.

**Don't:**
- Don't run stateful pods without persistent volumes.
- Don't mix EKS + custom CNI without testing.

*Ref: System_Design_on_AWS.md — "Amazon ECS / EKS / Fargate" (Chapter 11)*

---

### AWS Step Functions

**Principle:** Use Step Functions to model complex multi-step workflows with
explicit state.

**Do:**
- Choose **Standard** for long-running (≤ 1 year), auditable.
- Choose **Express** for high-volume, short (≤ 5 min), event processing.
- Use **Map state** (inline ≤ 40 concurrent; distributed 10,000+).
- Add retry + redrive + catch for failure handling.

**Don't:**
- Don't use Step Functions for trivial single-step orchestration (use Lambda
  alone).
- Don't store huge payloads in state input — use S3 references.

```json
{
  "Comment": "ASL Example",
  "StartAt": "Hello World",
  "States": {
    "Hello World": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:12345:function:HelloWorld",
      "End": true
    }
  }
}
```
*Ref: System_Design_on_AWS.md — "AWS Step Functions" / Table 12-4*

---

### Amazon MWAA (Managed Workflows for Apache Airflow)

**Principle:** Use MWAA for batch DAG orchestration when you need Airflow.

**Do:**
- Use IAM Identity Center for SSO; restrict Apache Airflow UI per access mode
  (public/private).
- Encrypt data with KMS (default).

**Don't:**
- Don't run interactive queries in DAGs without separate executor tuning.

*Ref: System_Design_on_AWS.md — "Workflow Orchestration"*

---

### Amazon SQS and SNS

**Principle:** SQS for queueing; SNS for fan-out; combine for pub/sub.

**Do:**
- SQS Standard: unlimited throughput, at-least-once, best-effort order.
- SQS FIFO: ≤ 3,000 TPS (300 × 10 batch), exactly-once, ordered.
- Visibility timeout 0–12 h; retention 1 min–14 days; DLQ for failures.
- SNS topics fan out to SQS / Lambda / HTTP / Email / SMS / KDF.
- Use FIFO SNS topics for ordered, deduplicated fan-out.
- Use KMS server-side encryption for sensitive messages.

**Don't:**
- Don't use SNS to deliver payloads > 256 KB — store in S3 / DynamoDB and
  reference.
- Don't put sensitive data in topic/message metadata (only body is encrypted).

```
SQS = poll-based queue
SNS = push-based pub/sub
SNS + N SQS queues = fan-out pattern
```
*Ref: System_Design_on_AWS.md — Tables 12-2 and 12-3*

---

### Amazon Kinesis (Data Streams, Data Analytics, Firehose, Video Streams)

**Principle:** Use the right Kinesis service by ingestion + processing pattern.

**Do:**
- **KDS**: real-time streaming, replay, ordered per shard.
  - 1 MB/s ingest, 2 MB/s fan-out per shard; use EFO for higher fan-out.
  - Retention 24 h – 7 d; shard split/merge for hot/cold.
- **KDA**: Apache Flink managed, near real-time SQL/stateful processing.
- **KDF**: zero-storage streaming ETL to S3/OpenSearch/Redshift/Splunk.
- **KVS**: video/audio ingestion with low-latency consumers.

**Don't:**
- Don't pick KDS if MSK/Kafka is already deployed — migrating is heavy.
- Don't exceed shard throughput; split shards when nearing limits.

| Service | Use | Storage |
|---------|-----|---------|
| KDS | Replayable streams | 24 h – 7 d |
| KDA | Real-time analytics | None (compute) |
| KDF | Stream to S3/search | None (delivery only) |
| KVS | Video/audio ingest | Configurable |

*Ref: System_Design_on_AWS.md — Table 12-1*

---

### Amazon CloudWatch and EventBridge

**Principle:** Use CloudWatch for metrics/logs/alarms; EventBridge for
event-driven integration.

**Do:**
- Use CloudWatch alarms with actions: SNS, autoscaling, EC2, Systems Manager.
- Use EventBridge for SaaS integrations (private, no polling).
- Use content-based filtering at EventBridge (cheaper than consumer logic).
- Use Schema Registry to discover/infer event shapes.

**Don't:**
- Don't put credentials in event payloads.
- Don't use CloudWatch Events for new designs — use EventBridge.

*Ref: System_Design_on_AWS.md — "Amazon CloudWatch" / "EventBridge"*

---

### AWS IAM (Identity and Access Management)

**Principle:** Least privilege; roles over users; MFA everywhere.

**Do:**
- Use **IAM roles** (temporary credentials) for services and cross-account.
- Use **IAM Identity Center** + IdP for human users (SAML/OIDC).
- Apply **SCPs** to limit org-wide permissions.
- Rotate access keys regularly; prefer short-lived credentials.

**Don't:**
- Don't use the root user for daily tasks.
- Don't share AWS access keys; use roles.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::samplebucket"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::samplebucket/*"]
    }
  ]
}
```
*Ref: System_Design_on_AWS.md — "AWS Identity and Access Management"*

---

### Amazon Cognito

**Principle:** Use Cognito for end-user AuthN/AuthZ; keep it serverless.

**Do:**
- Use **User Pools** for sign-in directory; **Identity Pools** for temporary
  AWS credentials.
- Federate with Google / Facebook / Amazon / Apple.
- Use Cognito Hosted UI; customise with CSS / logo.
- Use Lambda triggers for pre-/post-authentication custom logic.

**Don't:**
- Don't use Cognito if you need to migrate users cross-cloud with passwords
  — passwords aren't exportable. Force resets for active users.

*Ref: System_Design_on_AWS.md — "Amazon Cognito"*

---

### AWS AppSync (GraphQL)

**Principle:** Use AppSync to fan GraphQL queries to multiple data sources.

**Do:**
- Define GraphQL schema + resolvers per data source.
- Use merged APIs for team autonomy.
- Use real-time subscriptions via WebSockets (chat, leaderboards, sports).

**Don't:**
- Don't self-host GraphQL when AppSync's managed features (auth, caching,
  WAF) suffice.

*Ref: System_Design_on_AWS.md — "AWS AppSync"*

---

### Amazon EMR

**Principle:** Use EMR for Hadoop/Spark/Hive/Presto at scale; use EMRFS for
decoupling compute and storage.

**Do:**
- Use **EMRFS** (S3-backed) to share data across clusters; decouple compute
  lifecycle.
- Use EC2 spot for task nodes; on-demand for core nodes (HDFS).
- Store Hive metastore externally (RDS Multi-AZ) to survive cluster
  termination.
- Configure auto-termination after job completion.

**Don't:**
- Don't run iterative ML jobs with HDFS only — use EMRFS for cost.
- Don't put critical data only on HDFS — replicate to S3.

*Ref: System_Design_on_AWS.md — "Amazon Elastic MapReduce"*

---

### AWS Glue

**Principle:** Use Glue for serverless ETL with a managed catalog.

**Do:**
- Use Glue Data Catalog as the central metadata source.
- Choose engine by workload: Spark (distributed), Ray (Python scale),
  Python Shell (small).
- Use Data Quality rules; enable autoscaling; use Flex jobs for ≤34% savings.

**Don't:**
- Don't use Glue Studio for complex DAGs requiring branching — use Step
  Functions or MWAA.

*Ref: System_Design_on_AWS.md — "AWS Glue"*

---

### Amazon Athena

**Principle:** Use Athena for ad-hoc SQL on S3 without infrastructure.

**Do:**
- Define tables via Glue crawler or Hive metastore.
- Use columnar formats (Parquet/ORC) for compression + speed.
- Use federated query (Lambda connectors) for non-S3 sources.
- Use UDFs (Java on Lambda) for masking sensitive data.

**Don't:**
- Don't use Athena for low-latency, high-QPS — use Redshift or DynamoDB.

*Ref: System_Design_on_AWS.md — "Amazon Athena"*

---

### Amazon Redshift

**Principle:** Use Redshift for petabyte-scale columnar data warehousing.

**Do:**
- Choose distribution style (AUTO/EVEN/KEY/ALL) based on join patterns.
- Use sort keys + zone maps for column-pruned range queries.
- Use Redshift Spectrum for queries on S3 without loading.
- Use RA3 instances (decoupled storage via RMS) for elastic scaling.

**Don't:**
- Don't use DS2 instance types (legacy).
- Don't over-distribute small tables (use ALL or EVEN).

| Distribution | Use |
|--------------|-----|
| AUTO | Default; switches by table size |
| EVEN | No joins |
| KEY | Co-locate joined rows |
| ALL | Small, infrequently updated tables |

*Ref: System_Design_on_AWS.md — "Amazon Redshift"*

---

### Amazon SageMaker

**Principle:** Use SageMaker for end-to-end ML — prepare, build, train,
deploy.

**Do:**
- Choose inference type by latency/payload:
  - Real-time (low latency)
  - Serverless (intermittent, cold-start tolerant)
  - Asynchronous (≤ 1 GB payloads)
  - Batch transforms
- Use SageMaker Pipelines for CI/CD; Clarify for bias; Debugger for
  profiling.
- Use Ground Truth for labelling; AMT for hyperparameter tuning.

**Don't:**
- Don't host large models on real-time endpoints without testing cold start
  cost.

*Ref: System_Design_on_AWS.md — "Amazon SageMaker"*

---

### AWS Well-Architected Framework

**Principle:** Design and review against the six pillars; the pillars also map
to the eight fallacies.

**Pillars:**
1. **Operational Excellence** — monitors, runbooks, IaC, continuous improvement.
2. **Security** — least privilege, defence in depth, encryption, audit.
3. **Reliability** — recover from failure, scale, plan for partitions.
4. **Performance Efficiency** — right resource, monitor, evolve.
5. **Cost Optimization** — right-size, pay for value, iterate.
6. **Sustainability** — minimise environmental impact.

**Do:**
- Run a Well-Architected Review (WAR) at major milestones.
- Apply the Serverless Application Lens or SaaS Lens as appropriate.

**Don't:**
- Don't treat pillars as checklist items — they interact (security vs cost,
  performance vs sustainability).

*Ref: System_Design_on_AWS.md — "AWS Well-Architected Framework"*

---

### Cost Optimization and TCO

**Principle:** Compute TCO across the product lifecycle, not just the cloud
bill.

**Do:**
- TCO components: initial, operational, support/scaling, migration, retirement.
- Use **Reserved Instances** / **Savings Plans** for steady-state.
- Use **Spot** for fault-tolerant workloads.
- Move cold data to S3 IA / Glacier / Deep Archive.
- Right-size instances after observing CloudWatch metrics.
- Use DynamoDB Standard-IA for infrequent access (60% storage savings).
- Use CloudFront for free egress to AWS origins.

**Don't:**
- Don't chase the cheapest instance type without measuring performance
  regressions.
- Don't keep retired resources running (orphan snapshots, unused EIPs).

```
Storage:        S3 Standard → S3 IA → Glacier IR → Glacier FR → Glacier DA
Compute:        Spot < Savings Plans < Reserved < On-Demand (cost)
Egress to CF:   $0
Egress to net:  ~$0.09/GB
```
*Ref: System_Design_on_AWS.md — "Total cost of ownership"*

---

### Migration Strategies (Day 0 → Day N)

**Principle:** Migrate incrementally with traffic replication and dual writes;
prefer strangle over big-bang.

**Do:**
- **Traffic replication** on new system; compare responses.
- **A/B / canary** rollouts: 1% → 10% → 30% → 50% → 100%.
- **Database migration**: offline batch load + dual write + dual read +
  verification + cutover + retire old.
- Use **strangler fig** to incrementally replace legacy components.
- Run new and old side-by-side for ~2 weeks before turning off the old.

**Don't:**
- Don't migrate without a verification layer.
- Don't retire old resources until parity is proven.

```
Migration stages:
  Offline batch load  → Dual write  → Dual read + verify
  → Cutover           → Stabilise   → Retire old
```
*Ref: System_Design_on_AWS.md — "Moving from Day 0 to Day N"*

---

### Multi-Region Deployments

**Principle:** Multi-region for compliance, resiliency, or latency — never
just for vanity.

**Do:**
- Make each region fully independent (no shared services).
- Replicate state asynchronously; use DynamoDB global tables, Aurora global,
  ElastiCache global.
- Buffer deployments across regions to catch issues before propagating.
- Use DNS-based gradual failover; add jitter to client retries to avoid
  thundering herd.
- Use load shedding (drop telemetry, keep playback) when one region carries
  another's load.

**Don't:**
- Don't assume zero replication lag; design for bounded staleness.
- Don't switch all traffic to one region at once.

*Ref: System_Design_on_AWS.md — "Multiregion deployments"*

---

### Reference Architecture: URL Shortener

**Principle:** Day 0 monolith → Day N microservices; separate read-heavy
(reader) from write-heavy (creator).

**Day 0:** Single EC2 + RDS, no scaling concerns.
**Day N:**

```
Frontend service (public subnet)
  ├─ URL creator service (private)
  │    ↳ DynamoDB (mappings)
  │    ↳ ElastiCache (hot short URLs)
  │    ↳ SQS → analytics pipeline
  ├─ URL reader service (private)
  │    ↳ DynamoDB
  │    ↳ ElastiCache (DAX or Redis)
  └─ KGS (Key Generation Service)
       ↳ Aurora/Snowflake-style ticket servers
       ↳ ElastiCache buffer
```

**Do:**
- Use `PutItem` with `ConditionExpression` to prevent duplicate `customUrl`.
- Return 302 for short URL lookup; 200 for create.
- Use DynamoDB TTL for expiry; reconcile cache via DynamoDB Streams.

**Don't:**
- Don't put the URL creator and reader on the same service once traffic
  diverges significantly.

```json
POST /v1/createShortUrl
{
  "longUrl": "...",
  "customUrl": "...",
  "expiry": "...",
  "userMetadata": {...}
}

HTTP/1.1 200 OK
{ "shortUrl": "https://oreil.ly/SystemDesignOnAWS" }
```
*Ref: System_Design_on_AWS.md — "Chapter 14: Designing a URL Shortener"*

---

### Reference Architecture: Web Crawler + Search

**Principle:** Use Step Functions + Lambda + DynamoDB for the crawler; OpenSearch
for the index.

**Do:**
- Step Functions Map state for parallel page fetches.
- Redis with TTL for URL deduplication (politeness).
- S3 for raw HTML; OpenSearch for inverted index; Lambda for transformation.
- URL frontier routes by priority (SNS topic → SQS FIFO by priority).

**Don't:**
- Don't re-fetch the same domain too frequently — politeness.
- Don't store the entire URL list in Step Functions input — use DynamoDB.

*Ref: System_Design_on_AWS.md — "Chapter 15: Designing a Web Crawler"*

---

### Reference Architecture: Social Network

**Principle:** Separate fan-out (write) from timeline (read); handle celebrity
users specially.

**Do:**
- Fan-out on write for normal users; fan-out on read for celebrities.
- Store timelines per user; cache aggressively in ElastiCache.
- Use multi-region async replication for posts; primary in user home region.

**Don't:**
- Don't fan-out celebrity posts on write (millions of followers → write storm).
- Don't use a single chatty DB call to compose a timeline — denormalise.

*Ref: System_Design_on_AWS.md — "Chapter 16: Designing a Social Network"*

---

### Reference Architecture: Online Game Leaderboard

**Principle:** Use Redis sorted sets for ranking; eventual consistency
acceptable; reads < 100 ms, writes < 1 s.

**Do:**
- Use Redis ZADD/ZRANGE for O(log N) ranking.
- Store full history in DynamoDB (player scores table) + leaderboard summary
  in Redis.
- Write score → API Gateway → Lambda → DynamoDB + SQS → ranking processor
  → Redis update + SNS notification.

**Don't:**
- Don't recompute full leaderboard on every write.
- Don't serve leaderboard directly from primary DB — always cache.

*Ref: System_Design_on_AWS.md — "Chapter 17: Designing an Online Game Leaderboard"*

---

### Reference Architecture: Video Streaming (Netflix-like)

**Principle:** Ingest → transcode → package → CDN; use per-user adaptive
bitrate.

**Do:**
- Ingest via S3 → MediaConvert (multi-format encode) → S3.
- Package as HLS (Apple) / DASH (Android).
- Distribute via CloudFront; consider Origin Shield.
- Capture device metrics (rebuffer rate, startup time) for QoE.

**Don't:**
- Don't stream from origin — always via CDN.
- Don't encode per request; pre-encode all renditions.

*Ref: System_Design_on_AWS.md — "Chapter 20: Video Streaming"*

---

### Reference Architecture: Chat at WhatsApp Scale

**Principle:** Stateful servers (Mnesia + application on same instance) trade
operational complexity for latency; modern systems move to remote DBs.

**Do:**
- Co-locate DB with app instance to avoid cross-node chatter.
- Use end-to-end encryption at the client.
- Optimise for read-your-write for the active user.

**Don't:**
- Don't rely on single-region durability for chat history — replicate.

*Ref: System_Design_on_AWS.md — "Chapter 19: Chat Application at WhatsApp Scale"*

---

### Reference Architecture: Stock Broker

**Principle:** Use Local Zones / edge for low-latency order routing; in-memory
stores for hot path.

**Do:**
- Use Local Zones near exchanges/major trading hubs.
- Use in-memory stores (ElastiCache / DynamoDB DAX) on hot order path.
- Use ElastiCache with write-through to durable store (DynamoDB / Aurora).
- Capture all trades for audit; replicate to a separate compliance account.

**Don't:**
- Don't make a synchronous cross-region DB call on the order path.

*Ref: System_Design_on_AWS.md — "Chapter 21: Stock Broker Application"*

---

### Anti-Patterns and Common Mistakes

- **Single AZ for production:** one AZ down = full outage → *fix:* ≥ 2 AZs.
- **Sharing databases across microservices:** coupling in disguise → *fix:*
  per-service data ownership.
- **Synchronous chains across services:** tail latency compounds → *fix:*
  async, queues, sagas.
- **No idempotency on retries:** duplicates create duplicates → *fix:*
  idempotency keys.
- **No backpressure:** consumers drown → *fix:* bounded queues + DLQ +
  rate limiters.
- **Hot partition in DynamoDB:** single PK overloaded → *fix:* cache, random
  suffix, redesign PK.
- **Synchronous checkpointing on large datasets:** writes stall → *fix:*
  async checkpointing + RPO-bounded replay.
- **Eager microservices:** distributed monolith → *fix:* keep modular monolith
  until pain is real.
- **Public Memcached:** no auth/encryption → *fix:* private subnet only.
- **Lambda with cold-start on critical path:** p99 spikes → *fix:*
  provisioned concurrency.
- **Sharing root credentials:** god-mode blast radius → *fix:* IAM users +
  roles + MFA.
- **Big-bang migration:** all-or-nothing → *fix:* strangler fig + traffic
  replication.
- **EIP leak:** idle elastic IPs cost money → *fix:* release on teardown.
- **CloudFront bypassed:** S3 hit directly from clients → *fix:* front S3
  with CloudFront for caching + DDoS protection.
- **No throttling on public APIs:** bill shock + DoS → *fix:* API Gateway +
  WAF rate limiting.
- **Treating BASE as ACID:** strong-consistency reads on eventually
  consistent data → *fix:* design for staleness.
- **Sticky sessions on every LB:** scaling pain → *fix:* stateless + Redis
  session.
- **No circuit breaker:** cascading failures → *fix:* Closed/Open/Half-Open.
- **Cross-region strong-consistency reads without acknowledging latency:**
  → *fix:* local reads, async replication.
- **Schema-less thinking for key-value:** same key returning different shapes
  → *fix:* schema + validators.

*Ref: System_Design_on_AWS.md — distributed throughout*

---

## Decision Heuristics / Checklists

- **Synchronous vs Asynchronous?** Real-time UI → sync. Batch / fan-out →
  async.
- **Which storage class?** Daily access → Standard. Monthly → IA. Yearly
  archive → Glacier.
- **Which database?** See decision flowchart (Chapter 3, Figure 3-4): data
  type → query pattern → access pattern.
- **EC2 vs Lambda vs Containers?** Predictable + control → EC2. Bursty +
  event-driven → Lambda. Portable + complex → ECS/EKS/Fargate.
- **RDS vs DynamoDB?** Relational schema + joins + transactions → RDS/Aurora.
  Massive scale + simple access pattern → DynamoDB.
- **ALB vs NLB?** HTTP routing + WAF → ALB. Raw TCP/UDP + static IP → NLB.
- **SQS vs SNS?** Queue (poll) → SQS. Fan-out (push) → SNS. Pub/sub fan-out →
  SNS → N × SQS.
- **MSK vs KDS vs KDF?** Replay + Kafka compat → MSK. Custom real-time
  processing → KDS. ETL to S3/Redshift → KDF.
- **API Gateway direct to DynamoDB vs via Lambda?** Single-table key lookup
  → direct. Complex transformation → Lambda.
- **Multi-region or not?** Compliance / latency / resilience → yes. Cost-only
  → no.
- **Reserved vs Savings Plans vs On-Demand?** Steady state + 1-3 yr commit →
  Reserved / Savings Plans. Bursty → On-Demand (or Spot for fault-tolerant).
- **Cache choice:** TTL acceptable + low-cardinality hot keys → ElastiCache
  Redis. Sub-millisecond DynamoDB reads → DAX. Microsecond pure cache →
  Memcached.

*Ref: System_Design_on_AWS.md — distributed throughout*

---

## Key Takeaways

1. **Systems design is trade-off reasoning.** Capture cost, latency,
   consistency, availability, operability, and modifiability explicitly for
   every decision.
2. **CAP + PACELC + the eight fallacies** form the mental model; the AWS
   Well-Architected pillars map directly to the fallacies.
3. **Storage formats, database types, and caching strategies** are about
   access pattern matching — not buzzwords.
4. **Replication + partitioning + sharding** are the three scale levers;
   pick by consistency and access locality.
5. **On AWS:** model VPC as your private DC, use IGW/NAT deliberately, layer
   SGs + NACLs, and choose L4/L7 LBs by traffic visibility.
6. **Pick the right database:** RDS for relational, DynamoDB for scale, Neptune
   for graphs, OpenSearch for search, Timestream for time-series, Keyspaces
   for Cassandra, ElastiCache for cache, DocumentDB for Mongo.
7. **Compute choice is workload-shaped:** EC2 for control, Lambda for events,
   Fargate for managed containers, ECS/EKS for orchestration at scale.
8. **Caching is layered:** client → CDN → ElastiCache → DB → DAX for
   DynamoDB. Choose strategy (cache-aside, read-through, write-through,
   write-back) by read/write mix.
9. **Security is layered and least-privilege:** IAM roles over users, VPC
   isolation, encryption at rest + in transit, WAF + Shield at edge.
10. **Cost optimization is a discipline:** Right-size after measuring, use
    Reserved/Savings Plans for steady state, Spot for fault-tolerant,
    S3 storage class tiering for cold data, free CloudFront egress.
11. **Migration is incremental:** strangler fig, traffic replication,
    dual-write, dual-read with verification, percentage rollout, retire old.
12. **Multi-region is for compliance, latency, or resilience** — never just
    for vanity; design for bounded staleness and gradual failover with jitter.
13. **Step Functions for orchestration; SNS+SQS for choreography; Kafka for
    streaming; EventBridge for SaaS integration; MWAA for batch DAGs.**
14. **Observability is non-negotiable:** CloudWatch metrics, alarms, logs;
    X-Ray for tracing; dashboards for SLOs.
15. **Architecture evolves:** Day 0 monolith → multi-AZ + read replicas + cache
    + CDN → multi-service → multi-region; revisit continuously.

*Ref: System_Design_on_AWS.md — distributed throughout, esp. Part I conclusions and Part III case studies*

---

## Cross-References
- Related: [[../Building_Microservices.md]]
- Related: [[../Designing_Distributed_Systems.md]]
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]]
- Related: [[../Cloud_Application_Architecture_Patterns.md]]
- Related: [[../Foundations_of_Scalable_Systems.md]]
- Related: [[../Software_Architecture_Patterns.md]]
- Topic index: [[../INDEX.md]]