# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Foundations of Scalable Systems
**Author:** Ian Gorton (O'Reilly, 2022)
**Topic tags:** `#architecture` `#concurrency` `#distributed-systems` `#scalability`
**Language focus:** Java-centric prose with language-agnostic distributed-systems principles (TCP/IP, RabbitMQ, Kafka, Redis, MongoDB, DynamoDB, Flink)
**Sources:** `markdown_output/Foundations of Scalable Systems/Foundations of Scalable Systems.md` · `summaries/Foundations_of_Scalable_Systems.md`

## TL;DR
A field guide to the design levers that turn a small monolith into a system that survives internet-scale growth: replication and optimization as the two physical levers; load balancing, caching, sharding, and async messaging as the architectural levers; strong vs. eventual consistency, sharding strategies, replication topologies, and event/stream processing as the data-tier levers. Everything is presented as a *trade-off* against other quality attributes (performance, availability, security, manageability). Apply throughout: starting small is fine, but the *foundations* — statelessness, idempotence, timeouts, async backpressure — must be designed in from day one.

---

## Best Practices by Topic

### Scalability Dimensions & Replication vs. Optimization

**Principle:** Scalability = the system's ability to handle growth along an operational dimension (request rate, data volume, derived-value, response-time stability). Every scalability technique reduces to one of two levers: **replication** (add more resources) or **optimization** (do more with existing resources).

**Do:**
- Identify which dimension you need to scale: throughput, data volume, analytical value, or response-time stability — different dimensions require different techniques.
- Prefer replication when adding capacity and latency budgets permit; prefer optimization when latency-critical or when growth is bound to single-node resources (CPU, memory).
- Mirror the "Sydney Harbour Bridge" model — cloud resources can be replicated at the click of a mouse; engineer for elasticity, not static provisioning.
- Recognize that replication creates redundancy which *also* buys availability for free, but at the cost of consistency coordination.

**Don't:**
- Don't scale *up* indefinitely past what a single machine can handle — the cost grows super-linearly (GCP db-n1-highmem-96 = 96 vCPU, 624 GB, US$6K–16K/yr is roughly the ceiling before distributed becomes cheaper).
- Don't introduce distributed complexity before there's a real requirement — sophistication before scale is "deleterious to a project."
- Don't conflate performance (per-request metrics) with scalability (aggregate capacity) — they are related but distinct. Sometimes *slightly slower* per-request improves scalability (e.g., extra hop through LB enables horizontal scale).

**Code:** *(See code patterns below — load balancing, caching, idempotency, async messaging, event-driven.)*

*Ref: Foundations of Scalable Systems.md — "Introduction to Scalable Systems", "Scalability and Costs", "Scalability Basic Design Principles"*

---

### Architecture Trade-Offs

**Principle:** Every scalability decision trades against other quality attributes. The job is to make those trade-offs explicit, not to maximize one attribute unilaterally.

**Do:**
- Treat scalability, performance, availability, security, and manageability as competing forces; document the trade-off for each non-functional decision.
- Use TLS with connection reuse (TLS handshake is 2 round-trips — amortize it); symmetric encryption has negligible cost on modern CPUs with AES-NI.
- Budget 5–10% overhead for data-at-rest encryption; treat it as a non-negotiable compliance cost.
- Invest in observability (Grafana, CloudWatch, JMX/MBeans, Java Melody) *before* you need it — without metrics you cannot tune what you cannot measure.
- Couple scalability engineering with DevOps automation; manual operations don't scale.

**Don't:**
- Don't over-log: each log line consumes CPU and I/O that could serve requests.
- Don't assume "more security" means "more cost forever" — connection reuse mitigates TLS handshake cost; at-rest encryption is 5–10% only.
- Don't dismiss manageability early — "the number of moving parts grows" with every replica; budget observability and automation from the start.

*Ref: Foundations of Scalable Systems.md — "Scalability and Architecture Trade-Offs", "Performance", "Availability", "Security", "Manageability"*

---

### Distributed Systems Foundations (Partial Failures, Time, Idempotence)

**Principle:** Asynchronous networks mean partial failures are inevitable. When a response doesn't arrive you cannot distinguish a slow server, a crashed server, a lost request, or a lost response — every remote operation is a *crash fault* scenario.

**Do:**
- Make every state-mutating API call **idempotent** by including a client-generated idempotency key (composite of session ID + UUID/timestamp).
- Atomically commit both the state change *and* the key insert in the same transaction — otherwise a retry can double-apply (or never apply) the operation.
- Expire idempotency keys after a configurable window (60 minutes – 24 hours) once the operation has been acknowledged.
- Use TLS connection reuse; HTTP/1+ keep-alive amortizes connection-setup latency across requests.
- Distinguish *time-of-day clocks* (jump under NTP) from *monotonic clocks* (always move forward) — use monotonic for elapsed-time, time-of-day for cross-node ordering (and accept drift; don't rely on it).
- Apply Lamport logical clocks (counter incremented on local events, max(local, received+1) on receive) for causal ordering when you can't trust synchronized clocks.
- Tune TCP timeouts via Java's `java.net.SocketTimeoutException`-equivalent and HTTP client read-timeouts so slow downstream services don't tie up threads indefinitely.

**Don't:**
- Don't retry blindly without an idempotency key — a deposit applied twice is a real-world money bug.
- Don't compare timestamps across nodes to determine event order — clock drift of 10–20s/day is common; even one second of drift invalidates orderings.
- Don't accept the FLP impossibility theorem as a reason to skip consensus — real networks provide bounded delays and retries; use Raft/Paxos in practice (see Ch 12).
- Don't trust single replicas for hot state — replicate and use quorum reads.
- Don't build custom consensus or replication — distributed algorithms are extraordinarily hard. Use battle-tested platforms (Kafka, etcd, Redis Sentinel, DynamoDB).

**Code: Java RMI example illustrating the stub/skeleton pattern and `RemoteException`:**
```java
import java.rmi.*;
public interface IGBank extends Remote {
    public float balance (String accNo) throws RemoteException;
    public boolean statement(String month) throws RemoteException;
}
```
*Ref: Foundations of Scalable Systems.md — "Partial Failures", "Remote Method Invocation", "Time in Distributed Systems", "Consensus in Distributed Systems"*

---

### Concurrency Primitives (Threads, Race Conditions, Deadlocks)

**Principle:** Concurrency is the foundation of scalability because I/O-bound work wastes CPU. But concurrent code is inherently nondeterministic — critical sections must be identified, protected, and kept *as small as possible* to minimize the serialized portion that limits Amdahl's-law scalability.

**Do:**
- Encapsulate shared-state mutations inside critical sections protected by a lock (`synchronized` in Java, `sync.Mutex` in Go, channels + ownership in Go CSP).
- Keep critical sections **as small as possible** — every byte inside the lock is serialized time.
- Order lock acquisition globally to prevent circular-wait deadlocks (the dining-philosophers fix).
- Prefer thread pools (`ExecutorService` / Go worker pools) over unbounded thread creation — each thread costs ~1 MB of stack.
- Use `BlockingQueue`-style producer/consumer patterns instead of hand-rolling `wait()`/`notify()` guarded blocks.
- Use `CountDownLatch` for one-shot barrier synchronization; `CyclicBarrier`/`Phaser` for reusable barriers.
- Choose the right concurrency model for the language (Go CSP / goroutines, Erlang actors/mailboxes, Node.js single-threaded event-loop — Java shared-state + locks is *one* model, not the only one).
- Use thread-safe collections (`ConcurrentHashMap`, Java's `java.util.concurrent`) over hand-wrapped `synchronizedList` to gain fine-grained / per-segment locking.

**Don't:**
- Don't rely on absolute time coordination of threads — use `join()` or barrier synchronization, not `sleep(N)`.
- Don't assume thread execution order is deterministic — the scheduler interleaves nondeterministically; design for any interleaving.
- Don't forget that `++` is load-increment-store, not atomic — without protection, lost updates occur (the canonical example in the book is a 50,000-thread counter averaging 49,995 increments — never correct).
- Don't acquire locks in inconsistent order across threads — that's the deadly embrace.
- Don't ignore Amdahl's law: "If 5% executes serially, adding more than 2,048 cores has no effect." Ever-increasing CPU counts cannot rescue high-serialization code.

**Code: Race condition counter (intentionally broken):**
```java
public class RequestCounter {
    final static private int NUMTHREADS = 50000;
    private int count = 0;
    public void inc() { count++; } // <-- not atomic; LOAD-INCREMENT-STORE interleaves
    public int getVal() { return this.count; }
    public static void main(String[] args) throws InterruptedException {
        final RequestCounter counter = new RequestCounter();
        for (int i = 0; i < NUMTHREADS; i++) {
            Runnable thread = () -> { counter.inc(); };
            new Thread(thread).start();
        }
        Thread.sleep(5000);
        System.out.println("Value should be " + NUMTHREADS
            + "It is: " + counter.getVal()); // usually 49,995, never 50,000
    }
}
```
**Fix — synchronize the critical section:**
```java
synchronized public void inc() { count++; }
```
**Dining philosophers deadlock fix — break the circular-wait by acquiring low-numbered chopstick first:**
```java
// Philosopher: try leftChopStick then rightChopStick
// Fix: if (i == NUMPHILOSOPHERS - 1) {
//          ph[i] = new Philosopher(rightChopStick, leftChopStick);
//      } else {
//          ph[i] = new Philosopher(leftChopStick, rightChopStick);
//      }
```
*Ref: Foundations of Scalable Systems.md — "Problems with Threads", "Race Conditions", "Deadlocks", "Thread Coordination", "Barrier Synchronization", "Thread Pools", "Thread-Safe Collections", "An Overview of Concurrent Systems"*

---

### Application Services & Statelessness

**Principle:** HTTP is stateless. Scalable services must be stateless — the client provides all needed information per request, so any replica can handle any request, and the load balancer can distribute freely. Stateful services cause load imbalance and complicate failure recovery.

**Do:**
- Build APIs around resources identified by URIs; HTTP verbs (POST, GET, PUT, DELETE, PATCH) carry semantics.
- Return the whole resource on GET; use PATCH for partial updates (PUT replaces the entire representation).
- Use compression (`Accept-Encoding: gzip`) for large payloads — 50%+ bandwidth/latency reduction with minor CPU cost.
- Avoid chatty APIs (multiple round-trips per logical operation) — design for fewer, fatter requests.
- Specify APIs in OpenAPI 3.0 (YAML) for clarity and tooling support.
- Externalize conversational state to a distributed cache (Redis, memcached) so services remain stateless.
- Set `session.timeout` carefully — too short loses data, too long exhausts memory.
- Specify thread and database pool sizes in configuration files; tune empirically rather than relying on defaults.

**Don't:**
- Don't depend on HTTP literally being stateless — HTTP/1 keep-alive, cookies, HTTP/2 streams all carry state; design accordingly.
- Don't build stateful services for new scalable work — sticky sessions create load imbalance (clients with long sessions stay pinned, causing uneven replica utilization).
- Don't expose every property as a separate GET endpoint — that's CRUD-as-OOP antipattern.

*Ref: Foundations of Scalable Systems.md — "Service Design", "State Management", "Applications Servers"*

---

### Load Balancing & Horizontal Scaling

**Principle:** Horizontal scaling = multiple stateless replicas behind a load balancer. Replicas must be stateless so the LB can freely distribute. Failure is graceful: any replica can fail; traffic reroutes.

**Do:**
- Deploy a load balancer (L4 = network/packet-based NAT or L7 = HTTP reverse-proxy) in front of stateless replicas.
- Pick policies per workload: round-robin, least connections, header-based (e.g., `X-Client-Location:US,Seattle`), HTTP-verb-based.
- Use weights to favor more powerful replicas (e.g., 8-vCPU = weight 2, 4-vCPU = weight 1).
- Enable health checks that periodically ping/connect and remove unhealthy instances.
- Implement elasticity: scale up on a metric threshold (e.g., 70% CPU average) with a *warm-up* delay; scale in when below floor (e.g., 40%).
- Use scheduled scaling for predictable diurnal patterns; reactive scaling for unknown spikes.
- Make the LB itself highly available (multiple instances) — it becomes a SPoF otherwise.
- Use an API Gateway in front of microservices to insulate clients from internal refactors and to centralize auth/throttling/caching/observability.
- Treat the load-balanced cluster as capacity-limited — at saturation, add more replicas; otherwise no amount of LB helps.

**Don't:**
- Don't rely solely on round-robin if backend instance capacities differ — weight them.
- Don't enable sticky sessions ("session affinity") for new scalable services — load imbalance is inevitable because sessions have varying durations.
- Don't put a single API gateway as a single point of failure — stateless gateways (Kong) can be horizontally scaled; managed gateways (AWS API Gateway) have rate limits (10K req/s default) — verify your worst-case fits.
- Don't assume network and application LBs perform similarly — at low load NLB is ~20% faster; at saturation they're equivalent.

*Ref: Foundations of Scalable Systems.md — "Horizontal Scaling", "Load Balancing", "Load Distribution Policies", "Health Monitoring", "Elasticity", "Session Affinity"*

---

### Caching (Application & HTTP)

**Principle:** Caching is one of the most effective scalability techniques — well-designed caches that handle 80%+ of reads buy "extra capacity" at the database, since most requests never touch it. Trade-off: freshness vs. performance.

**Do:**
- Use a distributed in-memory KV cache (Redis, memcached) for frequently-read, rarely-changed data.
- Set a TTL on every cache entry to guarantee freshness; pick TTL by data update tolerance.
- Implement the cache-aside pattern (application checks cache → on miss, query DB and populate cache → return result).
- Use LRU or similar eviction policies when the cache fills; monitor hit/miss/evictions.
- Maximize cache hit rate; monitor `get_hits`, `get_misses`, `evictions` (memcached stats).
- Use HTTP `Cache-Control`, `Expires`, `Last-Modified`, and `ETag` headers to control web caching:
  - `Cache-Control: max-age=N` — freshness seconds.
  - `Cache-Control: no-store` — sensitive data, never cache.
  - `Cache-Control: no-cache` — must revalidate before use.
  - `ETag` + `If-None-Match` — server returns `304 Not Modified` to save bandwidth.
- Use proxy / CDN caches (Varnish, Squid, Cloudflare, Akamai) close to clients for geographic dispersion.

**Don't:**
- Don't choose TTL without empirical data — too short increases DB load; too long returns stale data.
- Don't expect cache freshness *across* process boundaries without explicit invalidation; cache-aside is eventually consistent for write-through.
- Don't forget that `cache-aside` is *resilient to cache failure* (treats unavailable cache as miss), which is why massively-scalable systems prefer it.
- Don't use read-through/write-through caches unless the cache engine supports it (e.g., NCache provider interfaces, DynamoDB DAX).

**Code: Cache-aside LiftWaitService (Java):**
```java
public class LiftWaitService {
    public List getLiftWaits(String resort) {
        List liftWaitTimes = cache.get("liftwaittimes:" + resort);
        if (liftWaitTimes == null) {
            liftWaitTimes = skiCo.getLiftWaitTimes(resort);
            cache.put("liftwaittimes:" + resort, liftWaitTimes, 300); // 300s TTL
        }
        return liftWaitTimes;
    }
}
```
*Ref: Foundations of Scalable Systems.md — "Distributed Caching", "Application Caching", "Web Caching"*

---

### Asynchronous Messaging & Queues

**Principle:** Async messaging decouples producers and consumers, smoothing load spikes through buffer-and-forward. Trade-offs are between data safety (durable messages, manual acks) and performance (transient, auto-ack). Avoid at-most-once unless loss is acceptable.

**Do:**
- Use a message broker (RabbitMQ, ActiveMQ, Kafka, etc.) when the response of a write does not need to be available immediately.
- Prefer **publish-subscribe** (RabbitMQ fanout/topic exchanges, Kafka topics) over point-to-point when many consumers need the same event.
- Configure durable/persistent queues + persistent messages + manual consumer acks + publisher confirms when data safety matters (banking, finance, orders).
- Use the *competing consumers* pattern to scale message processing horizontally (multiple consumers against a queue).
- Implement idempotent consumers with a deduplication cache (broker may set a `redelivered` header) — duplicate processing is the consumer's responsibility.
- Configure dead-letter queues (DLQs) with a redelivery limit (3–5 is typical); alert on messages arriving in the DLQ.
- Pool channels in a thread-pool server (e.g., Tomcat): channels aren't thread-safe; use `borrowObject`/`returnObject` per request.
- Tune RabbitMQ heap thresholds (default 40% memory) — long queues throttle producers; back-pressure is automatic.
- Don't build your own replication algorithm for queues — use quorum queues (Raft-based) or mirrored queues (deprecated).

**Don't:**
- Don't conflate RabbitMQ's per-channel single-threaded delivery with single-threaded processing — spawn consumers per channel to parallelize.
- Don't rely on at-least-once without idempotent consumers — duplicates are inevitable on retries.
- Don't use auto-ack when data safety matters — messages can be lost if the consumer crashes after broker delivery but before processing.
- Don't let poison messages loop forever — they crash every consumer eventually; use redelivery limits + DLQ.
- Don't ignore back-pressure — long queues (>10K messages) slow queue-management threads.

**Code: RabbitMQ channel pool usage in a request thread:**
```java
private boolean sendMessageToQueue(JsonObject message) {
    try {
        Channel channel = pool.borrowObject();
        channel.basicPublish(/* arguments omitted */);
        pool.returnObject(channel);
        return true;
    } catch (Exception e) {
        logger.info("Failed to send message to RabbitMQ");
        return false;
    }
}
```
*Ref: Foundations of Scalable Systems.md — "Introduction to Messaging", "Messaging Primitives", "Publish-Subscribe", "Message Replication", "Example: RabbitMQ", "Messaging Patterns", "Competing Consumers", "Exactly-Once Processing", "Poison Messages"*

---

### Microservices: Coupling, Decomposition, Resilience

**Principle:** Microservices are fine-grained, highly cohesive, loosely coupled services organized around a business capability (DDD bounded contexts). The flip side: distributed systems = inherent failure, complexity, and partial-failure cascades. Apply only when the monolithic symptoms justify it.

**Do:**
- Decompose along business-capability / bounded-context boundaries; size services to a single small team ("two-pizza rule").
- Keep services loosely coupled, highly cohesive, independently deployable, observable, hidden-implementation, decentralized.
- Use an API Gateway as the single external entry — insulates clients from refactors, enables auth/throttling/caching/monitoring in one place.
- Centralize workflows in orchestrators (explicit, easy to monitor) OR distribute via peer-to-peer choreographed events (decoupled, more resilient) — choose by complexity.
- Make every microservice tolerant of dependent service slowness — apply three patterns together: timeouts, circuit breakers, bulkheads.
- Aggregate results across services where excessive chatty calls exist — duplicate data into coupled services to enable local reads.
- Use API gateways (Kong, NGINX Plus, AWS API Gateway) for cross-cutting concerns.

**Don't:**
- Don't blindly follow microservices — the *Istio case study* shows microservices added unnecessary complexity. Apply Conway's Law in reverse: design teams first, services second.
- Don't make chatty cross-service calls — merging microservices is a sensible response when performance suffers.
- Don't skip the failure-handling patterns in the name of simplicity — distributed systems fail, period.

**Code: Retry storm (anti-pattern) — don't do this:**
```java
int retries = RETRY_COUNT;
while (retries > 0) {
    try {
        callDependentService();
        return true;
    } catch (RemoteCallException ex) {
        logError(e);
        retries = retries – 1;
    }
}
return false;
```
*Better: use exponential backoff, circuit breakers, and bulkheads. See "Fail Fast" and "Circuit Breaker" below.*

**Code: Python circuit breaker (decorator pattern):**
```python
from circuitbreaker import circuit

@circuit(failure_threshold=20, expected_exception=RequestException, recovery_timeout=5)
def api_call():
    # ... call protected downstream
    ...
```
**Code: Java Resilience4j bulkhead (limits concurrent threads per dependency):**
```java
BulkheadConfig config = BulkheadConfig.custom()
    .maxConcurrentCalls(150)
    .maxWaitDuration(Duration.ofSeconds(1))
    .build();
BulkheadRegistry registry = BulkheadRegistry.of(config);
Bulkhead newOrderBulkhead = registry.bulkhead("newOrder");

Supplier<OrderOutcome> orderSupplier = () -> OrderService.newOrder(OrderInfo);
Supplier<OrderOutcome> bulkheadOrderSupplier =
    bulkhead.decorateSupplier(newOrderBulkhead, orderSupplier);
```
*Ref: Foundations of Scalable Systems.md — "The Movement to Microservices", "Monolithic Applications", "Breaking Up the Monolith", "Deploying Microservices", "Principles of Microservices", "Workflows", "Resilience in Microservices", "Cascading Failures", "Fail fast pattern", "Circuit breaker pattern", "Bulkhead Pattern"*

---

### Capacity, Failure Detection, and Observability

**Principle:** "You cannot scale what you cannot measure." Long-tail response times, percentiles, and load test data drive real tuning decisions. Systems degrade well before 100% utilization.

**Do:**
- Measure response time *percentiles* (P50, P95, P99), not just averages — averages hide outliers.
- Tune timeouts to the P99 value (or slightly higher) — anything beyond that is nearly certain to fail.
- Use health-check pings (heartbeats) on every load-balanced dependency.
- Monitor thread pools, queue sizes, DB connection pool utilization, JVM heap, GC pauses, network saturation.
- Set utilization targets well below 100% (e.g., 60–70%) to maintain predictable performance.
- Send alerts on failures, not just on thresholds.
- Use distributed tracing across services (Jaeger, Zipkin) — essential for diagnosing latency in microservice architectures.
- Centralize logs (ELK stack) — local files in a microservice fleet are useless.
- Run load tests at, above, and below design point before deployment; collect raw evidence, not intuition.

**Don't:**
- Don't optimize for the average — long-tail requests starve worker threads and crash services.
- Don't dismiss "rare" events in concurrent code — "even if it happens 1 time in 10 million, you still have an incorrect result."
- Don't assume defaults are tuned — every cloud/serverless/platform config must be empirically calibrated.
- Don't treat observability as "Phase 2" — it is foundational for any system that must scale.

*Ref: Foundations of Scalable Systems.md — "Final Tips for Success", "Observability", "Resilience in Microservices", "Fail fast pattern"*

---

### Distributed Database Scaling (Sharding, Replication, Consistency)

**Principle:** Single-machine databases inevitably become the bottleneck. Distribute by sharding and replicating. CAP theorem forces choice between consistency and availability during a network partition — most real systems are tunable between AP/CP.

**Do:**
- Use scale-up (bigger machine) first; it's simple, retains single-point-of-failure semantics, and "gets many real-world applications a long way."
- Add read replicas for read-heavy workloads — writes still hit primary; distribute reads across secondaries. Be aware of the replica lag window.
- Partition (shard) data when a single machine's storage or throughput is exceeded. Pick partition key with even distribution; for new keys, hash-based sharding is most balanced.
- Use at least 3 replicas per shard (typical: `replication factor = 3`) — tolerates single-node failures.
- Choose leader-follower when you need single-writer semantics (RDBMS, MongoDB replica sets) or leaderless when you can tolerate clock-skew-based conflicts (DynamoDB, Cassandra).
- Tune quorum reads/writes: with N=3, W=2, R=2 → strong reads; W=1, R=1 → fast but possibly stale.
- Pick NoSQL when data is unstructured, scaling out is essential, simple query patterns suffice.
- Choose between four NoSQL data models by access pattern: KV (Redis, Oracle NoSQL), Document (MongoDB, Couchbase), Wide-Column (Cassandra, Bigtable), Graph (Neo4j).
- Model data for the *solution domain* (denormalize for the use case's read pattern) — accept storage duplication for query simplicity.

**Don't:**
- Don't shard to a single hot partition by choosing monotonic IDs — use hashed keys or random keys.
- Don't cross multiple aggregate transactions in a distributed SQL DB without 2PC — distributed joins are expensive and require partition-key joins.
- Don't rely on "strong consistency" with replicas unless your DB proves it (linearizability, sequential, causal).
- Don't rely on clock-based conflict resolution (Last-Writer-Wins) — clock skew across nodes makes timestamp orderings unreliable. Use version vectors when possible.
- Don't use NoSQL joins for cross-table aggregations without checking the DB supports them (Cassandra, Redis, DynamoDB, Riak do NOT support joins).
- Don't pick CAP labels blindly — most databases can be tuned AP or CP via configuration.
- Don't recreate replication, leader election, or consensus — use Raft-consensus tools (etcd, MongoDB replica sets, RabbitMQ quorum queues) and proven platforms.

*Ref: Foundations of Scalable Systems.md — "Scaling Relational Databases", "Scaling Up", "Scaling Out: Read Replicas", "Scale Out: Partitioning Data", "The Movement to NoSQL", "NoSQL Data Models", "Data Distribution", "The CAP Theorem", "Eventual Consistency", "Read Your Own Writes", "Tunable Consistency", "Quorum Reads and Writes", "Replica Repair", "Handling Conflicts"*

---

### Strong Consistency (Distributed Transactions, Consensus)

**Principle:** Strong consistency requires coordination. 2PC is blocking; Raft/Paxos are non-blocking consensus algorithms. Raft is the more understandable implementation — VoltDB and Spanner use it (or equivalents).

**Do:**
- Use Two-Phase Commit (2PC) when atomic distributed transactions are non-negotiable — but understand it's a *blocking* protocol: a coordinator failure after prepare phase leaves participants holding locks indefinitely.
- Implement Raft's three sub-problems correctly: leader election (term-incremented, majority vote), log replication (append until majority acks), safety (committed entries survive leader changes).
- Use Google Cloud Spanner's TrueTime for globally distributed strong consistency via tightly synchronized physical clocks (GPS + atomic clocks) returning an `[earliest, latest]` interval.
- Understand the consistency model spectrum: linearizability > sequential > causal > eventual.
- Use single-partition transactions whenever possible (VoltDB SPI) — cross-partition transactions require 2PC and incur severe throughput penalties.

**Don't:**
- Don't assume distributed transactions are fast even when correct — cross-partition coordination is the dominant cost.
- Don't confuse "immediate consistency" with "strong consistency" — even W=N can have brief windows where reads see inconsistent replicas.

*Ref: Foundations of Scalable Systems.md — "Strong Consistency", "Consistency Models", "Distributed Transactions", "Two-Phase Commit", "Distributed Consensus Algorithms", "Raft", "Strong Consistency in Practice", "VoltDB", "Google Cloud Spanner"*

---

### Event-Driven Architecture & Streaming

**Principle:** Events decouple producers and consumers; persistent logs (Kafka) make events replayable. Use Kafka for high-throughput event streams; use stream processors (Flink) for real-time analytics on unbounded data.

**Do:**
- Use Kafka's *topic partitioning* for horizontal scalability — partition count = max parallelism of consumer group.
- Choose partition keys by *semantic partitioning* (e.g., `skierID` ensures all lifts for one skier stay ordered on one partition).
- Configure producers to batch: `linger.ms` + `batch.size` tradeoff latency for throughput (e.g., 256 KB or 5 ms).
- Set `acks=all` with `min.insync.replicas ≥ 2` for data safety on replicated topics.
- Use consumer groups for parallel processing; allocate partitions to consumers with `CooperativeStickyAssignor` to minimize rebalance disruption.
- Match event style to need:
  - *Event notification* — lightweight; subscriber fetches current state.
  - *Event-carried state transfer (ECST)* — full state in event; consumers maintain local copy; eventually consistent.
  - *Domain event* — business-meaningful; modeled in the domain language.
- Differentiate *public* (integration-optimized) from *private* (internal-only) events — only expose public events through the published language; private events stay inside the bounded context.
- Use Flink for stream processing — it provides exactly-once semantics via Chandy-Lamport distributed snapshots + async barrier injection.
- Plan for retention: time-based (default 2 weeks), size-based, or compacted topics (keep latest value per key — write a new event with `null` to mark deletion).
- Build **private** events for bounded-context internal needs; expose **public** events in a published language; do not let subscribers couple to producer's internal model.
- Assume the worst in event-driven design: slow networks, duplicate events, server failures, out-of-order delivery.

**Don't:**
- Don't assume total ordering of events across partitions — Kafka orders within a partition, not across.
- Don't make partitions overly granular — `CooperativeStickyAssignor` reduces rebalance impact; you can grow partitions after creation (but it is risky).
- Don't exceed the number of consumers in a group past the partition count — extra consumers idle.
- Don't commit after events are processed *in a way* that causes loss — `commitSync` *before* processing ⇒ at-most-once; `commitSync` *after* ⇒ at-least-once (default, expected).
- Don't engage both producer timing and broker timing without planning for duplicates — use `enable.idempotence=true` for exactly-once delivery.
- Don't couple subscribers to producer's internal events — change one producer's model, break every dependent system.
- Don't assume default Kafka configs are tuned — partition count, retention, `acks`, `min.insync.replicas` are all workload-dependent.
- Don't expect deletion from immutable logs to be cheap — Kafka provides TTL and compacted topics but not surgical deletion.

**Code: Kafka producer send:**
```java
public Future<RecordMetadata> sendToBroker(final String skierID, final String liftRideEvent) {
    final ProducerRecord<String, String> producerRecord =
        new ProducerRecord<>(resortTopic, skierID, liftRideEvent);
    return producer.send(producerRecord);
}
```
**Code: Kafka consumer event loop:**
```java
while (alive) {
    ConsumerRecords<K, V> liftRideEvents = consumer.poll(LIFT_TOPIC_TIMEOUT);
    analyze(liftRideEvents);
    consumer.commitSync(); // commit after processing => at-least-once
}
```
*Ref: Foundations of Scalable Systems.md — "Event-Driven Architectures", "Apache Kafka", "Topics", "Producers and Consumers", "Scalability", "Availability", "Stream Processing Systems", "Stream Processing Platforms", "Data Safety"*

---

### Serverless & Capacity Planning

**Principle:** Serverless abstracts capacity provisioning; you pay only for what you use. Trade-off: cold-start latency and (for some platforms) limited per-function concurrency.

**Do:**
- Use serverless (Lambda, GAE Standard) for spiky / unpredictable load and for services with long idle periods.
- Tune AWS Lambda memory: more memory = proportionally more CPU + IO = potentially cheaper overall (e.g., 2 GB at 10 ms is 50% cheaper than 1 GB at 40 ms).
- Mitigate cold starts with provisioned concurrency (Lambda) or minimum-instance settings (GAE) when low tail latency is non-negotiable.
- For GAE Standard, jointly tune `target_cpu_utilization` (0.5–0.95), `target_throughput_utilization` (0.5–0.95), and `max_concurrent_requests` (1–80) — defaults are 0.6, 0.6, 10 → instances accept 6 concurrent requests before scaling.
- Empirically measure — non-intuitive parameter combinations are often optimal; intuition over defaults is wrong.

**Don't:**
- Don't expect Lambda to give the same instance to consecutive requests — concurrent requests trigger multiple runtime instances, each paying cold-start cost.
- Don't tune serverless parameters in isolation — the three GAE parameters interact strongly.
- Don't assume autoscaling equals infinite scaling — set a maximum instance count to bound cost.

*Ref: Foundations of Scalable Systems.md — "Serverless Processing Systems", "The Attractions of Serverless", "Google App Engine", "AWS Lambda", "Case Study: Balancing Throughput and Costs"*

---

## Anti-Patterns & Common Mistakes

- **Chatty APIs**: Multiple round-trips to fetch one logical resource — *fix:* use GET for whole resource + PATCH for partial.
- **Anemic cached models**: Coarse cache, coarse invalidation, lots of stale reads — *fix:* cache-aside + per-entry TTL tuned to update cadence.
- **Immediate retries on transient failure**: Tight loop re-fires against an already-overloaded service — *fix:* exponential backoff + circuit breaker.
- **Stateful services behind a load balancer**: Session affinity creates imbalance — *fix:* make services stateless; externalize state to distributed cache.
- **Custom consensus / replication**: Hand-rolled Paxos, Raft, or 2PC — *fix:* use proven platforms (etcd, Mongo replica sets, RabbitMQ quorum, Kafka).
- **Optimistic concurrency without retries**: Throwing `ConcurrencyException` without a retry path causes user-visible failures — *fix:* optimistic concurrency control with retry.
- **Replicating the entire monolith to scale one feature**: All features scale together — *fix:* extract that feature into a microservice.
- **Service coupling through implementation events**: Subscribers read producer's internal events — *fix:* publish integration events in a "published language."
- **Sharing code via shared libraries across microservices**: Couples release cycles — *fix:* share via APIs / messaging, not libraries.
- **Treating idempotence as "applied when convenient"**: Idempotency key writes and state changes must commit *together* in one transaction — *fix:* store key + state atomically.
- **Comparing clock values across nodes for ordering**: Drift invalidates ordering — *fix:* monotonic clocks locally; Lamport timestamps for cross-node causal order.
- **Long unbounded queues in app servers**: When threads/connections exhausted, requests queue; eventually overflow — *fix:* bounded queues + fail fast with 503.
- **ACID transactions across NoSQL stores**: Cross-shard transactions are slow/missing — *fix:* design for one-aggregate-per-transaction (DDD) and accept eventual consistency across aggregates.
- **ORM-driven domain models**: ORM serialization inverts control of your domain — *fix:* keep domain models ORM-free; use an adapter layer.

## Decision Heuristics / Checklists

- **Stateful vs Stateless service?** Default to stateless; externalize state.
- **Push vs Pull messaging?** Push (basicConsume with callback) is almost always preferable to polling (basicGet).
- **Synchronous vs Asynchronous?** Sync when the client needs the result now; async (fire-and-forget to queue) when result can be deferred.
- **Scale Up vs Scale Out?** Scale up first, then scale out when single-node limit is approached.
- **At-most-once vs At-least-once vs Exactly-once?** Match to data safety requirements; exactly-once requires idempotent consumers + dedup.
- **Push-based HTTP vs basicGet poll?** Push for throughput; poll only when push is unavailable.
- **LRU vs explicit TTL?** LRU for unknown access patterns; TTL when freshness guarantees required.
- **Replication factor?** Typical N=3; min.insync.replicas=2 with acks=all for safety.
- **Quorum?** R + W > N guarantees overlap; pick W=N/R=1 (write-heavy) or W=1/R=N (read-heavy).
- **Circuit breaker thresholds?** Trigger on 25% errors or N successive failures; half-open after 5–30 s.
- **Bulkhead thread count?** Size to expected concurrency for non-critical paths; reserve workers for critical APIs.
- **Cache TTL?** Tune to update cadence; shorter = more DB load; longer = more stale data.
- **NoSQL data model?** KV for opaque values; Document for queryable JSON; Wide-Column for many named columns per row; Graph for relationships.

## Key Takeaways

1. **Trade-offs are inevitable.** Consistency vs availability, performance vs scalability, simplicity vs flexibility — every design is a trade-off.
2. **Two physical levers: replication and optimization.** Everything else is a refinement of these.
3. **State is the hard problem.** Stateless scales trivially; state introduces consistency, replication, and partitioning complexity.
4. **Build for failure.** Partial failures, network partitions, clock drift, variable latencies are inevitable. Design to degrade gracefully.
5. **Leverage proven platforms.** Building custom Raft, Paxos, or 2PC is extraordinarily difficult. Use Kafka, Redis, DynamoDB, Mongo replica sets, Flink.
6. **Observe, then tune.** Percentiles, not averages. Load tests, not intuition.
7. **Concurrency limits scalability.** Amdahl's law — keep critical sections small; favor channels/actor/thread-pool models over per-task thread creation.
8. **Idempotency is mandatory.** Every state-mutating remote call must be idempotent via keys.
9. **Microservices ≠ free.** Conway's Law applies; cascade prevention requires timeouts + circuit breakers + bulkheads.
10. **Logs > FIFO queues for events.** Kafka topics persist events; enables replay, new consumers, recovery.

## Cross-References
- Related: [[../Learning_Domain_Driven_Design.md]] — DDD bounded contexts inform microservice boundaries.
- Related: [[../Domain_Driven_Design_with_Golang.md]] — DDD applied with ports/adapters in Go code.
- Topic index: [[../INDEX.md]]
