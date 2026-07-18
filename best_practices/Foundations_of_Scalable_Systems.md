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

*Ref: Foundations_of_Scalable_Systems.md — "Introduction to Scalable Systems", "Scalability and Costs", "Scalability Basic Design Principles"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Scalability and Architecture Trade-Offs", "Performance", "Availability", "Security", "Manageability"*

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

**Delivery semantics spectrum:**
- **At-most-once:** Fast, unreliable (UDP-style). Acceptable for non-critical data.
- **At-least-once:** TCP guarantees — duplicates inevitable.
- **Exactly-once:** Requires idempotence + dedup + retries; trades performance for correctness.

*Ref: Foundations_of_Scalable_Systems.md — "Partial Failures", "Remote Method Invocation", "Time in Distributed Systems", "Consensus in Distributed Systems"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Problems with Threads", "Race Conditions", "Deadlocks", "Thread Coordination", "Barrier Synchronization", "Thread Pools", "Thread-Safe Collections", "An Overview of Concurrent Systems"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Service Design", "State Management", "Applications Servers"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Horizontal Scaling", "Load Balancing", "Load Distribution Policies", "Health Monitoring", "Elasticity", "Session Affinity"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Distributed Caching", "Application Caching", "Web Caching"*

---

### Asynchronous Messaging & Queues (RabbitMQ)

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

**Code: RabbitMQ producer/consumer setup (Java):**
```java
// Producer
channel.exchangeDeclare(EXCHANGE_NAME, "direct");
channel.basicPublish(EXCHANGE_NAME, "France", null, message.getBytes());

// Consumer
String queueName = channel.queueDeclare().getQueue();
channel.queueBind(queueName, EXCHANGE_NAME, "France");
```

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

**Code: RabbitMQ consumer with push model (recommended over polling):**
```java
boolean autoAck = true;
channel.basicConsume(queueName, autoAck, "tag",
    new DefaultConsumer(channel) {
        @Override
        public void handleDelivery(String consumerTag,
            Envelope envelope,
            AMQP.BasicProperties properties,
            byte[] body)
            throws IOException
        {
            // process the message
        }
    });
```

**Code: Per-thread consumer for parallel processing:**
```java
Runnable runnable = () -> {
    try {
        final Channel channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, true, false, false, null);
        // max one message per receiver
        final DeliverCallback threadCallback = (consumerTag, delivery) 
            -> {
            String message = 
                new String(delivery.getBody(), StandardCharsets.UTF_8);
            // process the message 
        };
        channel.basicConsume(QUEUE_NAME, 
            false, threadCallback, consumerTag -> {});
    } catch (IOException e) {
        logger.info(e.getMessage());
    }
};
```

**Data-safety checklist for RabbitMQ:**
1. Publisher-confirms (`confirmSelect()`) — broker ACKs receipt.
2. Persistent messages (`MessageProperties.PERSISTENT_TEXT_PLAIN`).
3. Persistent queues (durable) — survive broker restart.
4. Manual consumer ACKs (`autoAck=false`) — only after processing.

**Idempotency via duplicate detection (publisher side, Artemis):**
```java
ClientMessage msg = session.createMessage(true);
UUID idKey = UUID.randomUUID(); // use as idempotence key
msg.setStringProperty(HDR_DUPLICATE_DETECTION_ID, idKey.toString() );
```

*Ref: Foundations_of_Scalable_Systems.md — "Introduction to Messaging", "Messaging Primitives", "Publish-Subscribe", "Message Replication", "Example: RabbitMQ", "Messaging Patterns", "Competing Consumers", "Exactly-Once Processing", "Poison Messages"*

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

**Code: Spring Boot bulkhead via application.yml:**
```yaml
server:
  tomcat:
    threads:
      max: 200
resilience4j.bulkhead:
  instances:
    OrderService:
      maxConcurrentCalls: 150
      maxWaitDuration: 1000ms
```

**Code: Spring Boot @Bulkhead decorator:**
```java
@Bulkhead(name = "OrderService", fallbackMethod = "newOrderBusy")
public OrderOutcome newOrder(OrderInfo inf){// details omitted}
```

*Ref: Foundations_of_Scalable_Systems.md — "The Movement to Microservices", "Monolithic Applications", "Breaking Up the Monolith", "Deploying Microservices", "Principles of Microservices", "Workflows", "Resilience in Microservices", "Cascading Failures", "Fail fast pattern", "Circuit breaker pattern", "Bulkhead Pattern"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Final Tips for Success", "Observability", "Resilience in Microservices", "Fail fast pattern"*

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

**Three sharding techniques:**
- **Hash key:** `partition = hash(key) mod N` — most balanced; consistent hashing minimizes reshuffling on add/remove.
- **Value-based:** Partition by key value (e.g., country, region) — risks skew.
- **Range-based:** Partition by key range (e.g., zip code ranges) — supports range queries but risks imbalance.

**Code: MongoDB find query with multiple conditions:**
```javascript
db.skiers.find( {
    age: { $gt: 16},
    renew: { $exists: false }} 
)
```

**Code: Graph query with Cypher (Neo4j / openCypher):**
```cypher
MATCH (p:Person)-[rel:VISITED]->(c:Skiresort)
WHERE c.name = 'Mission Ridge'
RETURN p.email
```

*Ref: Foundations_of_Scalable_Systems.md — "Scaling Relational Databases", "Scaling Up", "Scaling Out: Read Replicas", "Scale Out: Partitioning Data", "The Movement to NoSQL", "NoSQL Data Models", "Data Distribution", "The CAP Theorem", "Eventual Consistency", "Read Your Own Writes", "Tunable Consistency", "Quorum Reads and Writes", "Replica Repair", "Handling Conflicts"*

---

### Eventual Consistency & Replica Repair

**Principle:** Many distributed databases offer *tunable* consistency — you choose where on the AP-CP spectrum each operation sits. With N replicas and tunable W (write quorum) and R (read quorum), trade-offs are precise.

**Do:**
- Choose **R + W > N** for guaranteed overlap (read sees latest write).
- **W = N, R = 1** for write-heavy (write to all, read from one) — fast reads, slow writes.
- **W = 1, R = N** for read-heavy (write to one, read all and pick latest) — fast writes, slow reads.
- **W = N/2 + 1, R = N/2 + 1** for balanced — typical choice.
- Apply **read-your-own-writes** consistency where possible — route user's reads to the same partition that handled their writes.
- Use **version vectors** (vector clocks) for conflict resolution when you can tolerate storage of per-replica history.
- Implement **active repair** (Merkle tree comparison, anti-entropy) for periodic reconciliation.
- Apply **passive repair** (read-repair) for on-access reconciliation.
- Use **inconsistency window** (max acceptable time before replica sync) as a target metric.

**Don't:**
- Don't rely on **Last Writer Wins** when skew between nodes is significant — use version vectors instead.
- Don't expect linearizability from "eventually consistent" DBs unless configured.
- Don't conflate **session consistency** with **causal consistency** — session is weaker.
- Don't assume quorum reads are always strong — depends on whether W=N was used on prior write.
- Don't use vector clocks for unbounded replicas — size grows with replica count.

*Ref: Foundations_of_Scalable_Systems.md — "What Is Eventual Consistency?", "Inconsistency Window", "Read Your Own Writes", "Tunable Consistency", "Quorum Reads and Writes", "Replica Repair", "Active Repair", "Passive Repair", "Handling Conflicts", "Last Writer Wins", "Version Vectors"*

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

**Code: YugabyteDB distributed SQL transaction:**
```sql
BEGIN TRANSACTION
UPDATE stock SET in_stock = in_stock - purchase_amount 
WHERE stock_id = purchase_stock_id;
INSERT INTO purchases (cust_id, stock_id, amount)
VALUES (customer, purchase_stock_id, purchase_amount);
END TRANSACTION;
```

**Raft in production:**
- Each Raft node is leader, follower, or candidate.
- Leader sends heartbeats (~300–500 ms) with term value via `AppendEntries`.
- Follower election timer randomizes; expired timer → candidate → `RequestVote` with incremented term.
- Vote rules: only vote if term ≥ local term AND candidate's log is at least as up to date.
- Majority vote → new leader; majority vote on entry commit.
- Implemented in Neo4j, YugabyteDB, etcd, Hazelcast.

*Ref: Foundations_of_Scalable_Systems.md — "Strong Consistency", "Consistency Models", "Distributed Transactions", "Two-Phase Commit", "Distributed Consensus Algorithms", "Raft", "Strong Consistency in Practice", "VoltDB", "Google Cloud Spanner"*

---

### Event-Driven Architecture & Streaming (Kafka)

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

**Code: Kafka producer bootstrap config:**
```java
Properties props = new Properties();
props.put("bootstrap.servers", "IPbroker1,IPBroker2");
```

**Kafka delivery semantics:**
- `acks=0` — fire-and-forget; may lose events.
- `acks=1` — leader persists; transient failures may duplicate.
- `acks=all` + `enable.idempotence=true` — exactly-once.

**Stream processing with Apache Flink (DataStream API):**
```java
final StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

// Kafka source
KafkaSource<LiftRide> source = KafkaSource.<LiftRide>builder()
    .setBootstrapServers(brokerList)
    .setTopics("resort-topic")
    .setGroupId("liftConsumers")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setValueOnlyDeserializer(new LiftRideSchema())
    .build();
DataStream<LiftRide> liftRideStream = 
    env.fromSource(source, WatermarkStrategy.noWatermarks(), 
    "Resort Lifts");

// Windowed aggregation
DataStream<Tuple2<String, Integer>> liftCounts =
    liftRideStream
    .map(i -> Tuple2.of(i.getLiftID(), 1))
    .returns(Types.TUPLE(Types.STRING, Types.INT))
    .keyBy(value -> value.f0)
    .sum(1)
    .window(SlidingProcessingTimeWindows.of(Time.minutes(10), 
        Time.minutes(5)));
```

**Flink state backend config (flink-conf.yaml):**
```yaml
state.backend: rocksdb
state.checkpoints.dir: file:///checkpt-mystream/
```

**Flink operator parallelism:**
```java
.sum(1).setParallelism(10);  // 10 parallel instances of .sum
```

*Ref: Foundations_of_Scalable_Systems.md — "Event-Driven Architectures", "Apache Kafka", "Topics", "Producers and Consumers", "Scalability", "Availability", "Stream Processing Systems", "Stream Processing Platforms", "Data Safety"*

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

*Ref: Foundations_of_Scalable_Systems.md — "Serverless Processing Systems", "The Attractions of Serverless", "Google App Engine", "AWS Lambda", "Case Study: Balancing Throughput and Costs"*

---

### Redis — Data Structure Store

**Principle:** Redis = in-memory data structure store (single-threaded event loop). Supports strings, lists, sets, sorted sets, hashes. Durability via snapshots and AOF logging.

**Do:**
- Use Redis for distributed caching, session storage, leaderboards, real-time analytics.
- Configure **both** snapshot (RDB) and AOF (append-only file) for data safety.
- Use Redis **transactions** (`multi`/`exec`) for atomic multi-key operations (note: Redis transactions are NOT ACID — no rollback, can leave server in unknown state on crash).
- Use Redis Cluster for horizontal scalability (auto-sharding across nodes).
- Use Redis Sentinel for automatic failover (HA).
- Use Lua scripting for server-side atomic operations.

**Don't:**
- Don't treat Redis as a primary database — durability is configurable but not bulletproof.
- Don't store large values (>1 MB) in Redis — it's optimized for small, fast values.
- Don't use Redis without bounded maxmemory — unbounded memory leads to OOM.
- Don't rely on Redis transactions as ACID — they provide atomicity only when all commands succeed.

**Code: Redis transaction example:**
```redis
multi
lpush neworders "orderid 600066 customer 89788 item 788990 amount 11 date 12/24/21"
hmset user:89788 lastorder 600066
exec
```

*Ref: Foundations_of_Scalable_Systems.md — "Redis", "Data Model and API", "Distribution and Replication", "Strengths and Weaknesses"*

---

### MongoDB — Document Database

**Principle:** MongoDB stores JSON-like documents in collections; sharded via `mongos` router + `mongod` shards + config servers. Replica sets (Raft-based leader election) provide HA.

**Do:**
- Use **shard key** carefully — picks partition distribution; bad keys = hot partitions.
- Deploy **config servers as replica sets** — cluster metadata must survive failure.
- Use **majority write concern** (default in 5.0+) for data safety — writes durable on quorum.
- Use **read preferences** to control staleness tradeoffs:
  - `primary` — strong consistency, higher latency.
  - `primaryPreferred` — strong but falls back to secondary.
  - `secondary` — eventually consistent, lower latency.
  - `nearest` — geographically closest; can be stale.
- Enable ACID multi-document transactions when needed (requires replica set or sharded cluster).
- Use **embedded documents** for one-to-few relationships; use references for one-to-many.
- Run **balancer** to redistribute chunks across shards as data grows.

**Don't:**
- Don't use MongoDB without replica sets — single points of failure.
- Don't exceed **chunk size** (default 64 MB) without resizing — balancer kicks in but adds overhead.
- Don't use read preferences for critical reads that require fresh data.
- Don't use `linearizable` read concern + `majority` write concern unless required — it's the most expensive combination.
- Don't rely on `$lookup` (MongoDB join) for hot aggregations — it's slow.

**MongoDB deployment configurations:**
- **(A)** `mongos` on each application server — local routing, low latency.
- **(B)** `mongos` on each database shard — local to data, balanced.
- **(C)** `mongos` on dedicated hosts — highest isolation, extra network hops.

*Ref: Foundations_of_Scalable_Systems.md — "MongoDB", "Data Model and API", "Distribution and Replication", "Strengths and Weaknesses"*

---

### DynamoDB — Managed NoSQL

**Principle:** DynamoDB = fully managed AWS NoSQL with automatic sharding, 3× replication across availability zones, on-demand or provisioned capacity modes.

**Do:**
- Use DynamoDB for AWS-native workloads with predictable single-digit-millisecond latency needs.
- Choose **partition key** that distributes load evenly — avoid hotkeys.
- Use **composite keys** (partition + sort) for related-item queries.
- Configure **auto scaling** with min/max provisioned capacity for predictable traffic.
- Use **DAX (DynamoDB Accelerator)** for read-heavy workloads that need sub-millisecond latency.
- Enable **point-in-time recovery** for accidental deletes — 35-day rolling window.
- Use **batch operations** (`BatchGetItem`, `BatchWriteItem`) to reduce round trips.
- Use **global tables** for multi-region replication (multileader; last-writer-wins on conflict).

**Don't:**
- Don't rely on hotkey patterns — partition is bounded at 3,000 RCU/1,000 WCU per second; one item maxes a partition.
- Don't use strongly consistent reads + global tables naively — strong consistency is per-region; global is eventually consistent.
- Don't exceed 400 KB per item — hard limit.
- Don't assume automatic scaling prevents throttling — burst capacity helps but isn't infinite.
- Don't use transactions without doubling capacity — each transaction consumes 2× the normal RCU/WCU.

**Code: DynamoDB GetItem API (Java):**
```java
Table table = dynamoDB.getTable("Skiers"); 
Item item = table.getItem("skierID", "6788321471");
```

**Code: DynamoDB item structure:**
```json
{
  "skierID": "6788321471",
  "Name": {
    "last": "Gorton",
    "first": "Ian"
  },
  "location": "USA-WA-Seattle",
  "skiresorts": [
    "Crystal Mountain",
    "Mission Ridge"
  ],
  "numdays": "2",
  "season21": {
    "day1": {
      "date": "12/1/2021",
      "vertical": 30701,
      "lifts": 27,
      "resort": "Crystal Mountain"
    },
    "day2": {
      "date": "12/8/2021",
      "vertical": "17021",
      "lifts": 10,
      "resort": "Mission Ridge"
    }
  }
}
```

*Ref: Foundations_of_Scalable_Systems.md — "Amazon DynamoDB", "Data Model and API", "Distribution and Replication", "Strengths and Weaknesses"*

---

### Stream Processing Platforms

**Principle:** Stream processing = data-in-motion analytics. Batch processes bounded data; streaming processes unbounded data with subsecond-to-second latency.

**Do:**
- Use streaming for time-sensitive analytics (fraud detection, real-time recommendations, IoT).
- Use **windows** (sliding, tumbling, session) to bound computation over unbounded streams.
- Implement **stateful operators** for aggregations (counts, sums, averages).
- Use **checkpointing** for fault tolerance (Flink: barrier-based; Spark: lineage-based).
- Plan for **backpressure** — slow consumers shouldn't OOM producers.
- Use **Lambda architecture** (batch + speed layer) only if needed; modern Kappa (streaming only) often suffices.
- Choose platforms by feature needs:
  - **Flink:** Low latency, exactly-once, complex event processing.
  - **Spark Streaming:** Micro-batch, integration with MLlib/GraphX.
  - **Kafka Streams:** Lightweight, in-JVM, Kafka-native.
  - **Storm:** Pure streaming, mature but less actively developed.

**Don't:**
- Don't use streaming when batch suffices — complexity isn't worth the latency.
- Don't skip backpressure handling — slow downstream causes cascading failures.
- Don't assume exactly-once is free — it requires coordination; expect throughput impact.
- Don't store unbounded state in memory — use RocksDB or external state backends.
- Don't use Lambda architecture unless you actually need both batch correctness and streaming speed — most modern systems work with Kappa.

**Lambda vs Kappa:**
- **Lambda:** Batch layer (Hadoop, accurate but slow) + Speed layer (Storm, fast but approximate). Serving layer merges results.
- **Kappa:** Stream-only (Kafka + Flink). Replay topic when logic changes.

*Ref: Foundations_of_Scalable_Systems.md — "Stream Processing Systems", "Introduction to Stream Processing", "Stream Processing Platforms", "Case Study: Apache Flink", "DataStream API", "Scalability", "Data Safety"*

---

### Network Communication Essentials (TCP/IP, Sockets)

**Principle:** All distributed systems communicate over networks with fundamental properties that must be understood. The TCP/IP stack provides reliability on top of an unreliable underlying IP layer.

**Do:**
- Use **TCP** for reliable, ordered, connection-oriented communication (most distributed systems).
- Use **UDP** for low-latency, lossy-tolerant workloads (video, gaming, DNS, telemetry).
- Use **TLS** for encryption in transit — amortize handshake cost via connection reuse.
- Use **HTTP** for service-to-service communication (the de-facto standard).
- Understand **sockets**: bidirectional pipe = `<client IP, client port, server IP, server port>`. Each connection = 1 socket per side.
- Apply **keep-alive** to amortize TCP connection-setup cost.
- Use **DNS** for service discovery; remember DNS is eventually consistent (caches).

**Don't:**
- Don't use sockets directly for application logic — use higher-level RPC/REST/messaging.
- Don't trust raw UDP for critical data — packet loss is real.
- Don't rely on DNS for load balancing (TTL caches mean stale endpoints).
- Don't assume LAN latency is free — even 0.5 ms adds up across N calls.
- Don't ignore network failures — build for asynchronous, lossy reality.

**RPC/RMI technology timeline:**
- **DCE RPC** (early 1990s) — C/C++.
- **CORBA** (early 1990s) — language-neutral via IDL.
- **Java RMI** (late 1990s) — Java-only.
- **XML Web Services** (2000) — HTTP+XML+WSDL.
- **gRPC** (2015) — HTTP/2 + Protobuf.

*Ref: Foundations_of_Scalable_Systems.md — "Communications Basics", "Communications Hardware", "Communications Software", "Remote Method Invocation"*

---

### Scalability and Architecture Trade-Offs (Detailed)

**Principle:** Scalability cannot be achieved in isolation. Every design decision trades against other quality attributes.

**Quality attributes competing with scalability:**
- **Performance:** Often align (better performance = more capacity).
- **Availability:** Often align (replication gives both).
- **Security:** Often oppose (encryption costs CPU; TLS handshake costs RTTs).
- **Manageability:** Inverse correlation (more replicas = more to manage).
- **Cost:** Often inverse (scale up = cost grows super-linearly).

**Do:**
- Quantify trade-offs — calculate the cost of each design choice.
- Use **TLS connection reuse** — handshake cost is 2 RTTs, amortize across many requests.
- Treat **5–10% data-at-rest encryption overhead** as a non-negotiable cost.
- Apply **observability** early — Grafana, CloudWatch, JMX/MBeans.
- Couple scalability engineering with **DevOps automation**.

**Don't:**
- Don't ignore manageability early — "the number of moving parts grows" with every replica.
- Don't treat security as infinitely costly — connection reuse mitigates TLS overhead.
- Don't over-log — each log line is CPU and I/O stolen from request handling.
- Don't dismiss observability as "Phase 2" — it's a prerequisite for scaling safely.

*Ref: Foundations_of_Scalable_Systems.md — "Scalability and Architecture Trade-Offs"*

---

### Concurrency Models Across Languages

**Principle:** Different languages make different concurrency model choices. Knowing them helps you pick the right tool.

| Language | Concurrency Model | Notes |
|---|---|---|
| **Java** | Shared-state threads + locks | Lowest-level abstraction; `java.util.concurrent` for high-level |
| **Go** | CSP via goroutines + channels | "Share memory by communicating" |
| **Erlang/Elixir** | Actor model | Mailbox-based messaging; lightweight processes |
| **Node.js** | Single-threaded event loop + nonblocking I/O | I/O-bound; CPU-bound blocks everything |
| **Rust** | Ownership + async/await | Memory-safe without GC; async runtimes (Tokio) |
| **Python** | GIL limits threads; multiprocessing or asyncio | Use multiprocessing for CPU; asyncio for I/O |
| **C/C++** | OS threads (pthreads) | Low-level; lock-free via atomics |

**Do:**
- Pick a language whose **concurrency model fits the workload** — Go for concurrent servers, Erlang for fault-tolerant messaging, Java for shared-state libraries.
- Use the language's **idiomatic primitives** — Go channels, Erlang mailboxes, Rust `Arc<Mutex<T>>`.
- Learn the model's **failure modes** — CSP: blocking channels; Actors: mailbox overflow; event loops: blocking calls.

**Don't:**
- Don't fight the language model — Java + locks work, but Go + locks fights the runtime.
- Don't mix models without understanding — Go goroutines + Java-style locks can deadlock.
- Don't assume "more parallelism" = "faster" — Amdahl's law applies; serial sections dominate.

*Ref: Foundations_of_Scalable_Systems.md — "Concurrency Models"*

---

### Thread Coordination Patterns

**Principle:** Beyond locks, Java (and similar runtimes) provide coordination primitives that solve common concurrency patterns elegantly.

**Primitives:**
- **`CountDownLatch`:** One-shot barrier; threads await N signals before proceeding.
- **`CyclicBarrier`:** Reusable barrier; N threads rendezvous then all proceed.
- **`Phaser`:** Multi-phase barrier with dynamic party registration.
- **`Semaphore`:** Permits-based access (generalized lock).
- **`Exchanger`:** Pair-wise handoff between two threads.
- **`BlockingQueue`:** Thread-safe FIFO; producer/consumer pattern.

**Do:**
- Use `CountDownLatch` for "wait for N events to complete before proceeding."
- Use `CyclicBarrier` for repeated coordination phases (e.g., map-reduce iterations).
- Use `BlockingQueue` instead of hand-rolled `wait`/`notify`.
- Use thread-safe collections (`ConcurrentHashMap`, `CopyOnWriteArrayList`) instead of wrapping `synchronizedList`.

**Don't:**
- Don't use `Thread.sleep` for coordination — it's not a synchronization mechanism.
- Don't use object `wait`/`notify` directly — error-prone; use `java.util.concurrent`.
- Don't hand-roll condition variables when `BlockingQueue` suffices.
- Don't forget that `notify` vs `notifyAll` matters — `notify` wakes one (may starve); `notifyAll` wakes all (re-check condition).

*Ref: Foundations_of_Scalable_Systems.md — "Thread Coordination", "Barrier Synchronization", "Thread Pools", "Thread-Safe Collections"*

---

### CAP Theorem & PACELC

**Principle:** During a network partition, you choose consistency (CP) or availability (AP). Beyond CAP, **PACELC** extends the trade-off: even when there is no partition (Else), there is a Latency vs. Consistency trade-off.

**CAP:**
- **CP (Consistency + Partition tolerance):** Return errors during partitions. Examples: HBase, MongoDB (with `majority` write concern).
- **AP (Availability + Partition tolerance):** Accept writes/read on partitioned side, reconcile later. Examples: Cassandra, DynamoDB (default).

**PACELC:**
- If **P**artition → choose A or C.
- **E**lse (no partition) → choose **L**atency or **C**onsistency.

**Do:**
- Choose CP when correctness is non-negotiable (banking, inventory).
- Choose AP when availability is non-negotiable (social feeds, analytics).
- Configure **read/write concern** levels (DynamoDB, MongoDB) per use case, not globally.
- Communicate the choice via ADR — CAP trade-offs are architectural decisions.

**Don't:**
- Don't claim CP without proving it — most "CP" databases aren't during network partitions.
- Don't claim AP without defining reconciliation — eventual consistency requires schema for conflict resolution.
- Don't pick CAP labels for marketing — most databases are tunable across the spectrum.
- Don't ignore PACELC — latency vs. consistency applies even in healthy networks.

*Ref: Foundations_of_Scalable_Systems.md — "The CAP Theorem", "Consistency Models"*

---

### Idempotence Implementation

**Principle:** Idempotence = operation produces the same result regardless of how many times applied. Essential for safe retries in distributed systems.

**Implementation approaches:**
1. **Idempotency key:** Client generates unique key; server stores it post-operation.
2. **Natural idempotence:** Some operations are inherently idempotent (`PUT` with full state, `DELETE`).
3. **Conditional update:** `UPDATE ... WHERE status = 'pending'` — second update is no-op.
4. **Versioning/optimistic locking:** Update only if version matches.

**Do:**
- Use **composite key** = session ID + UUID/timestamp.
- **Atomically** commit state change and key insertion in the same transaction.
- **Expire** keys after operation acknowledgment (60 minutes – 24 hours).
- Implement client-side **exponential backoff** on retry (1s, 2s, 4s, 8s + jitter).
- Use **idempotency key** in HTTP header (`Idempotency-Key: <uuid>`) for mutating endpoints.

**Don't:**
- Don't store idempotency key in a separate transaction from state change — race conditions allow double-application.
- Don't keep idempotency keys forever — memory bloat.
- Don't rely on natural idempotence for non-idempotent operations (`POST` is NOT naturally idempotent).
- Don't ignore duplicate detection at the broker — ActiveMQ, RabbitMQ can detect duplicates via `MessageID`.

*Ref: Foundations_of_Scalable_Systems.md — "Partial Failures" (idempotency discussion)*

---

### Load Distribution Policies

**Principle:** Load balancers distribute requests across replicas. The right policy depends on workload characteristics.

**Policies:**
- **Round-robin:** Equal distribution, simple, doesn't account for capacity differences.
- **Weighted round-robin:** Honor replica capacity differences (8-vCPU = weight 2, 4-vCPU = weight 1).
- **Least connections:** Route to replica with fewest active connections — good for long-lived connections.
- **Least response time:** Route to fastest replica — handles heterogeneous performance.
- **Header-based:** Route by request attribute (`X-Client-Location: US,Seattle`).
- **Random:** Simple but statistically balanced for large pools.

**Do:**
- Choose **weighted** policies when replica capacities differ.
- Use **least connections** for variable-duration requests (chatty vs. quick).
- Use **header-based** for geographic / multi-tenant routing.
- Enable **active health checks** to remove unhealthy replicas.
- Combine policies: weighted least-connections for typical workloads.

**Don't:**
- Don't use **round-robin** for heterogeneous replicas — wasted capacity on slow ones.
- Don't enable **sticky sessions** unless absolutely required — load imbalance.
- Don't rely on **DNS load balancing** for dynamic environments — TTL caches stale endpoints.
- Don't configure LB without **health checks** — failed replicas still receive traffic.

*Ref: Foundations_of_Scalable_Systems.md — "Load Distribution Policies"*

---

### Web Caching Headers (HTTP)

**Principle:** HTTP caching reduces server load and latency by serving cached responses when possible.

**Key headers:**
- **`Cache-Control: max-age=N`** — Fresh for N seconds.
- **`Cache-Control: no-store`** — Never cache (sensitive data).
- **`Cache-Control: no-cache`** — Must revalidate before use.
- **`Cache-Control: public`** — Cacheable by any cache.
- **`Cache-Control: private`** — Cacheable only by browser, not CDN.
- **`Expires`** — Absolute expiration time (HTTP/1.0 fallback).
- **`Last-Modified`** + **`If-Modified-Since`** — Validator-based freshness.
- **`ETag`** + **`If-None-Match`** — Strong validator; 304 Not Modified if match.

**Do:**
- Use `ETag` for entities that change unpredictably.
- Use `Last-Modified` for entities with regular updates.
- Use `Cache-Control: no-cache` for personalized pages (still cached, revalidated).
- Use `Cache-Control: public, max-age=3600` for static assets.
- Use `Cache-Control: no-store` for authenticated responses with PII.

**Don't:**
- Don't confuse `no-cache` (revalidate) with `no-store` (don't cache).
- Don't use `Expires` alone — `Cache-Control` takes precedence in modern browsers.
- Don't cache `POST` responses (caching them violates HTTP semantics).
- Don't use `private` for shared CDN-cacheable resources.

*Ref: Foundations_of_Scalable_Systems.md — "Web Caching", "Cache-Control", "Expires and Last-Modified", "Etag"*

---

### Distributed Systems Failures — Liveness vs Safety

**Principle:** Two Generals' Problem proves consensus is impossible with bounded time on asynchronous networks with crash faults. FLP impossibility extends this.

**Two Generals' Problem:** Two generals must coordinate attack via messengers, but messengers can be lost. They can never be *certain* the other received the message.

**FLP Impossibility:** Consensus is impossible in bounded time on asynchronous networks with even one faulty process.

**Why consensus works in practice:**
- Real networks provide **bounded delays** (most of the time).
- **Retries** eventually succeed.
- Raft/Paxos use timeouts as practical bounds.

**Properties of consensus:**
- **Safety:** Nothing bad happens (no two values chosen).
- **Liveness:** Something good eventually happens (a value is chosen).
- **Validity:** The chosen value was proposed by some participant.

**Do:**
- Use proven consensus algorithms (Raft, Paxos) instead of inventing.
- Design for **partial failures** — every remote call may silently fail.
- Use **timeouts** everywhere — never wait forever.
- Build **retry + idempotency** into every external interaction.

**Don't:**
- Don't build custom consensus — extremely hard to get right.
- Don't assume network failures are detectable — distinguish crash, network partition, slow server, lost response.
- Don't rely on FLP impossibility to skip consensus — bounded networks make it practical.
- Don't accept Byzantine failures in most enterprise systems — exclude via secure networks; focus on crash faults.

*Ref: Foundations_of_Scalable_Systems.md — "Consensus in Distributed Systems" (Two Generals, FLP)*

---

### Thread Pools & Executor Frameworks

**Principle:** Thread pools decouple task submission from execution. They bound resource usage (max threads), reduce per-task overhead (no thread creation cost), and centralize lifecycle management.

**Java ExecutorService:**
- `newFixedThreadPool(n)` — fixed pool, bounded.
- `newCachedThreadPool()` — unbounded, shrinks when idle.
- `newSingleThreadExecutor()` — single thread with unbounded queue.
- `newScheduledThreadPool(n)` — delayed/periodic execution.
- `newWorkStealingPool()` — ForkJoinPool-based for parallel work.

**Do:**
- **Size pools based on workload type:**
  - **CPU-bound:** N threads ≈ N cores (Amdahl's law).
  - **I/O-bound:** N threads ≈ N cores × (1 + W/C) where W = wait time, C = compute time.
- Set **bounded queues** with explicit rejection policy (`CallerRunsPolicy` to back-pressure the producer).
- Name threads (`ThreadFactory` with meaningful names) for debuggability.
- **Monitor** pool metrics: queue size, active threads, completed tasks.
- **Prefer `ExecutorService`** over hand-rolling thread creation in application code.

**Don't:**
- Don't use `newCachedThreadPool()` without bounds — unbounded thread creation under load.
- Don't use unbounded `LinkedBlockingQueue` — memory blowup on producer > consumer.
- Don't size for "thread per request" — wrong model for I/O-bound servers.
- Don't ignore `RejectedExecutionException` — handle rejection explicitly (DLQ, backoff, fail-fast).

**Code: Java thread pool best practice:**
```java
// Custom ThreadFactory for named threads
ThreadFactory namedThreadFactory = new ThreadFactory() {
    private final AtomicInteger counter = new AtomicInteger(1);
    @Override
    public Thread newThread(Runnable r) {
        return new Thread(r, "worker-" + counter.getAndIncrement());
    }
};

// Bounded thread pool with rejection policy
ExecutorService executor = new ThreadPoolExecutor(
    10,                                  // core threads
    50,                                  // max threads
    60L, TimeUnit.SECONDS,               // idle timeout
    new ArrayBlockingQueue<>(1000),       // bounded queue
    namedThreadFactory,
    new ThreadPoolExecutor.CallerRunsPolicy()  // back-pressure
);
```

*Ref: Foundations_of_Scalable_Systems.md — "Thread Pools", "Barrier Synchronization"*

---

### Java RMI (Remote Method Invocation) — Pattern Details

**Principle:** Java RMI provides RPC semantics for Java-to-Java communication. The stub-skeleton pattern makes remote calls look like local ones, but failures (network, server crash) surface as `RemoteException`.

**Do:**
- Use **RMI Registry** (`LocateRegistry.createRegistry(1099)`) to advertise server objects.
- Implement `Remote` interface on remote objects; throw `RemoteException` from every method.
- Extend `UnicastRemoteObject` to enable remote invocation.
- Use **`Naming.lookup()`** on the client to obtain a stub reference.
- Choose **JRMP** (Java Remote Method Protocol) for Java-only; **IIOP** for cross-language.

**Don't:**
- Don't use RMI for new systems — REST/gRPC is simpler, cross-platform.
- Don't return complex object graphs — marshalling overhead is high.
- Don't change method signatures without coordinating stubs — stub-server compatibility breaks.
- Don't catch `RemoteException` and swallow — every remote call needs error handling.

**Code: Java RMI server setup:**
```java
import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

public class IGBankServer extends UnicastRemoteObject 
    implements IGBank {
    // constructor/method implementations omitted
    public static void main(String args[]) {
        try {
            IGBankServer server = new IGBankServer();
            // create a registry in local JVM on default port
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.bind("IGBankServer", server);
            System.out.println("server ready");
        } catch(Exception e) {
            // code omitted for brevity
        }
    }
}
```

**Code: Java RMI client:**
```java
// obtain a remote reference to the server
IGBank bankServer = (IGBank)Naming.lookup("rmi://localhost:1099/IGBankServer");
// now we can call the server
System.out.println(bankServer.balance("00169990"));
```

**RMI call sequence:**
1. Server starts, binds logical reference in RMI Registry.
2. Client looks up stub via Registry.
3. Client invokes method on stub.
4. Stub marshalls request into network packets → sends to skeleton.
5. Skeleton unmarshalls → calls server implementation.
6. Result marshalled and returned.

*Ref: Foundations_of_Scalable_Systems.md — "Remote Method Invocation"*

---

### Java RMI vs REST vs gRPC

**Principle:** Choose the right RPC style for your use case.

| Feature | Java RMI | REST/JSON | gRPC/Protobuf |
|---|---|---|---|
| Language | Java only | Any | Any |
| Format | Java objects | JSON | Protobuf (binary) |
| Speed | Fast (Java-native) | Slow (text parsing) | Fast (binary) |
| Streaming | No | Limited (chunked) | Yes (bi-directional) |
| Schema | Implicit (Java types) | OpenAPI (optional) | Required (.proto) |
| Browser support | No | Yes | Limited (grpc-web) |
| Use case | Java-only legacy | Public APIs | Microservices |

**Do:**
- Use **REST/JSON** for public APIs and browser clients.
- Use **gRPC** for internal microservice communication (high performance, streaming).
- Use **RMI** only for legacy Java systems (consider migration to gRPC).
- Specify OpenAPI 3.0 for REST contracts; `.proto` for gRPC.

**Don't:**
- Don't use REST for high-frequency internal calls — gRPC is faster.
- Don't use gRPC for browser-facing APIs without grpc-web proxy.
- Don't build new systems on Java RMI.

*Ref: Foundations_of_Scalable_Systems.md — "Remote Method Invocation"*

---

### IPC Mechanisms (Sockets, Pipes, Message Queues)

**Principle:** Inter-process communication lets processes exchange data. Multiple mechanisms with different trade-offs.

**Sockets:**
- Bidirectional pipe between two endpoints (`<client IP, client port, server IP, server port>`).
- TCP (SOCK_STREAM) or UDP (SOCK_DGRAM).
- Each IP supports 65,535 TCP + 65,535 UDP ports.
- 4-tuple identifies each connection uniquely.

**Pipes (named and unnamed):**
- Unnamed: parent-child processes only, one-way, dies with processes.
- Named (FIFO): filesystem entity, unrelated processes, FIFO order.

**Message Queues (POSIX):**
- FIFO with multi-producer/multi-consumer.
- Decouples producers from consumers.
- Survives process termination (until system reboot).

**Do:**
- Use **sockets** for network-extensible, bidirectional communication.
- Use **named pipes** for same-machine, related-process coordination.
- Use **message queues** for cross-process task handoff on same machine.
- Use **high-level abstractions** (gRPC, HTTP) over raw sockets when possible.

**Don't:**
- Don't use raw sockets in application code — error-prone.
- Don't use message queues for synchronous request-reply — high latency.
- Don't use unnamed pipes across unrelated processes — they won't have access.

*Ref: Foundations_of_Scalable_Systems.md — "An Overview of Sockets", IPC discussion*

---

### Lamport Timestamps & Logical Clocks

**Principle:** Physical clocks drift across nodes; logical clocks provide causal ordering without synchronized time.

**Lamport timestamps:**
- Each process keeps a counter, initialized to 0.
- On local event: `counter = counter + 1`.
- On send: `counter = counter + 1`; attach to message.
- On receive: `counter = max(local, received) + 1`.

**Vector clocks:**
- Each process keeps a vector of size N (one entry per node).
- On local event: increment own entry.
- On send: increment own entry; attach vector.
- On receive: `local[i] = max(local[i], received[i]) for all i`; increment own entry.

**Do:**
- Use **Lamport clocks** for total ordering (sufficient for most causal needs).
- Use **vector clocks** when you need to detect concurrent events (e.g., conflict resolution).
- Apply logical clocks to **message ordering** in async systems.
- Combine with **physical time** when global ordering matters.

**Don't:**
- Don't use Lamport clocks when you need conflict detection — use vector clocks.
- Don't compare physical timestamps across nodes for ordering — use logical clocks.
- Don't scale vector clocks to thousands of nodes — size grows linearly.

*Ref: Foundations_of_Scalable_Systems.md — "Time in Distributed Systems"*

---

### Network Communication Layers

**Principle:** The Internet Protocol (IP) suite has 4 layers, each building on the previous. Understanding them helps debug distributed systems.

**Layer 1: Data Link (Network cards, device drivers)**
- Single network segment communication.

**Layer 2: Internet (IP)**
- Host addressing (IPv4 32-bit, IPv6 128-bit).
- Routing via routers.
- Best-effort delivery (no guarantees).

**Layer 3: Transport (TCP, UDP)**
- TCP: connection-oriented, reliable, ordered, stream.
- UDP: connectionless, unreliable, datagram.

**Layer 4: Application (HTTP, FTP, SMTP, etc.)**
- Higher-level protocols.
- Built on top of transport layer.

**Do:**
- Choose **TCP** for reliability (most distributed systems).
- Choose **UDP** for latency-tolerant, lossy workloads (video, gaming, DNS, telemetry).
- Use **HTTP/1.1+ keep-alive** to amortize connection-setup cost.
- Plan for **TLS** encryption (2 RTT handshake cost; amortize via connection reuse).

**Don't:**
- Don't confuse **TCP** (connection-oriented, reliable) with **UDP** (connectionless, lossy).
- Don't rely on **IP-level** ordering or reliability — both are best-effort.
- Don't use **raw UDP** for critical data — packet loss is real.
- Don't assume **LAN latency is zero** — even 0.5 ms × N hops adds up.

*Ref: Foundations_of_Scalable_Systems.md — "Communications Hardware", "Communications Software"*

---

### Reactive Systems & Backpressure

**Principle:** Reactive systems handle load variations gracefully via message-driven, elastic, resilient, responsive design. Backpressure propagates load information back through the system.

**Reactive Manifesto principles:**
- **Responsive:** System responds in reasonable time.
- **Resilient:** Stays responsive under failure.
- **Elastic:** Stays responsive under varying load.
- **Message-driven:** Async messages with backpressure (Reactive Streams).

**Backpressure mechanisms:**
- **Bounded queues + reject:** Reject new requests when queue full.
- **Throttling:** Limit rate of incoming requests.
- **Sampling:** Process subset of requests; drop the rest.
- **Load shedding:** Drop low-priority requests first.
- **Adaptive concurrency:** Slow producers when consumer is overwhelmed.

**Do:**
- Implement **bounded queues** with explicit overflow handling.
- Use **reactive streams** (Reactor, RxJava, Akka Streams) for async pipelines with built-in backpressure.
- Design for **graceful degradation** under load — prioritize critical paths.
- Monitor **queue depth** and set alerts before overflow.
- Apply **circuit breakers** to short-circuit load on failing dependencies.

**Don't:**
- Don't use **unbounded queues** — memory exhaustion under load.
- Don't ignore backpressure — cascading failures follow.
- Don't process every request when overloaded — shed load strategically.
- Don't implement custom reactive frameworks — use battle-tested ones.

*Ref: Foundations_of_Scalable_Systems.md — "Elasticity", "Cascading Failures", Resilience patterns*

---

### Couchbase & Dynamo-Style Databases

**Principle:** Couchbase, Cassandra, and DynamoDB all share the **Dynamo-style** approach: leaderless replication, eventual consistency, vector clocks / LWW for conflict resolution.

**Couchbase:**
- Document database with N1QL (SQL-like) query language.
- Uses **XDCR (Cross Data Center Replication)** for multi-region.
- Supports joins with limitations (similar to MongoDB's $lookup).
- Memory-first with disk persistence.

**Cassandra:**
- Wide-column store; CQL (Cassandra Query Language) is SQL-like.
- Partition key + clustering key for primary key.
- **Tunable consistency** per query: `ONE`, `QUORUM`, `ALL`.
- No joins; no subqueries.
- LWW with timestamps (or user-defined conflict resolution).

**Do:**
- Choose Cassandra for write-heavy workloads with eventual consistency tolerance.
- Choose Couchbase for document workloads with SQL-like query needs.
- Always tune consistency per query based on data criticality.
- Use **Quorum** (`QUORUM`) for balanced consistency; `ONE` for fastest but possibly stale.
- Pre-aggregate or denormalize data — joins don't exist.

**Don't:**
- Don't try to use Cassandra as a transactional database — it isn't.
- Don't assume LWW resolves correctly — clock skew invalidates timestamp ordering.
- Don't put Cassandra on shared-everything hardware — it's designed for shared-nothing commodity nodes.
- Don't use Cassandra without understanding partition key distribution — uneven keys = hot spots.

*Ref: Foundations_of_Scalable_Systems.md — "Movement to NoSQL", "NoSQL Data Models", "Data Distribution"*

---

### Microservices Architecture — Detailed Patterns

**Do:**
- Implement **service discovery** (Consul, Eureka, Kubernetes DNS) for dynamic registration.
- Apply **circuit breakers** (Resilience4j, Polly) at every service boundary.
- Use **distributed tracing** (OpenTelemetry, Jaeger) to follow requests across services.
- Implement **centralized logging** (ELK, Loki, Splunk) for cross-service debugging.
- Apply **bulkheading** — separate thread pools per dependency.
- Use **API composition** at the BFF layer to aggregate backend calls.
- Build **service mesh** (Istio, Linkerd) when operational concerns dominate business logic.
- Implement **distributed transactions** via **Saga pattern** when ACID spans services.
- Apply **choreography** for simple workflows; **orchestration** for complex workflows.
- Use **CQRS** + **Event Sourcing** for systems with high read/write asymmetry.
- Design for **graceful degradation** — when a service is down, the system still works (degraded).

**Don't:**
- Don't build microservices without mature CI/CD and observability — chaos.
- Don't use synchronous chains more than 3-4 deep — latency compounds.
- Don't share databases across services — defeats the whole purpose.
- Don't skip the **fallback** design for each circuit-breaker-protected call.
- Don't underestimate operational complexity — 10 services = 10× the ops work.

*Ref: Foundations_of_Scalable_Systems.md — "Microservices", "Resilience in Microservices", "Cascading Failures"*

---

### Idempotent Consumers & Deduplication

**Principle:** At-least-once delivery is the norm. Idempotent consumers handle duplicates by detecting them and skipping reprocessing.

**Approaches:**
1. **Idempotency table:** Store processed message IDs in DB; check before processing.
2. **Broker redelivered flag:** Check `message.getJMSRedelivered()` or AMQP `redelivered` header.
3. **Business idempotence:** Make the operation itself idempotent (e.g., "set status to shipped" not "increment shipped count").
4. **Versioning:** Process message only if its version > stored version.

**Do:**
- Combine **broker duplicate detection** + **consumer idempotence** for defense in depth.
- Implement **idempotency key table** with TTL (don't grow forever).
- Use **broker-native** features where available (ActiveMQ Artemis duplicate detection, Kafka idempotent producer).
- Document which messages are processed idempotently — for auditors.

**Don't:**
- Don't rely solely on `redelivered` flag — it only indicates broker-side detection, not consumer-side processing.
- Don't grow idempotency tables forever — use TTL.
- Don't make idempotence tables the bottleneck — separate fast cache from durable log.
- Don't ignore **out-of-order** delivery — version stamps or timestamps required.

*Ref: Foundations_of_Scalable_Systems.md — "Exactly-Once Processing"*

---

### Quorum Reads & Writes — Math

**Principle:** With N replicas, choose W (write quorum) and R (read quorum). The invariant R + W > N guarantees reads see the latest write (overlap).

**Scenarios with N=3:**
- **R=3, W=3** — Always strong; can fail if any replica down.
- **R=2, W=2** — Strong; tolerant of one failure per side.
- **R=1, W=3** — Write to all, read from one; strong but slow writes.
- **R=3, W=1** — Write to one, read all; fast writes, slow reads, strong.
- **R=1, W=1** — Fast, eventually consistent; risks stale reads.

**Do:**
- Pick **W = R = ⌊N/2⌋ + 1** for balanced strong consistency.
- Pick **W = N, R = 1** for write-heavy with strong reads.
- Pick **W = 1, R = N** for read-heavy with strong reads.
- Use **sloppy quorums** (R/W from *different* replicas than the canonical set) for availability.
- Document the choice — quorum math is non-obvious.

**Don't:**
- Don't use **W=R=1** for data you can't tolerate being stale.
- Don't use **W=R=N** if you can't tolerate write latency from majority acks.
- Don't assume "consistent reads" mean strong consistency unless W=N was used on prior write.

*Ref: Foundations_of_Scalable_Systems.md — "Quorum Reads and Writes"*

---

### NoSQL Data Modeling Patterns

**Principle:** NoSQL requires *solution-domain* modeling — design tables per use case, denormalize for query patterns. Trade flexibility for efficiency.

**Patterns:**
1. **Aggregates:** Group related entities into one document (one-to-few relationships).
2. **Bucket pattern:** Group time-series data into buckets (e.g., per-day documents).
3. **Versioning:** Store multiple versions for audit / temporal queries.
4. **Outlier pattern:** Keep common fields in main document; rare large fields in separate collection.
5. **Computed pattern:** Pre-compute aggregations at write time.
6. **Tree/aggregation pattern:** Tree structure embedded in single document.
7. **Subset pattern:** Only include frequently-accessed subset of related items.

**Do:**
- Model for **read patterns** — denormalize for queries.
- Use **aggregates** for transactional consistency boundaries.
- Use **bucket pattern** for time-series (avoid unbounded array growth).
- Apply **versioning** for audit/replay needs.
- Compute aggregations eagerly for read-heavy workloads.

**Don't:**
- Don't normalize NoSQL — joins are expensive or missing.
- Don't put unbounded arrays in documents — use bucket or reference pattern.
- Don't store large blobs inline — use references or object storage.
- Don't compute on every read if the result rarely changes — pre-compute.

*Ref: Foundations_of_Scalable_Systems.md — "The Movement to NoSQL", "NoSQL Data Models"*

---

### Load Balancer L4 vs L7

**Principle:** L4 (network) LBs operate on packets; L7 (application) LBs operate on HTTP semantics. Choice depends on flexibility vs performance needs.

**L4 (network-layer):**
- Operates on TCP/UDP packets.
- Faster (~20% less latency at low load).
- No content inspection.
- Examples: AWS NLB, F5 BIG-IP, Linux Virtual Server (LVS).

**L7 (application-layer):**
- Inspects HTTP headers, URLs, cookies.
- Can route by path, host, headers.
- Slower (parses HTTP).
- Examples: AWS ALB, NGINX, HAProxy, Envoy.

**Do:**
- Use L4 for raw TCP/UDP performance (gRPC, gaming, video).
- Use L7 for HTTP routing needs (path-based, host-based, header-based).
- Use L7 when you need **TLS termination** at LB.
- Combine: L4 in front of multiple L7 instances.

**Don't:**
- Don't use L7 if all you need is round-robin TCP distribution — L4 is faster.
- Don't use L4 if you need URL/header-based routing — impossible.
- Don't assume L4 lacks TLS — modern L4 LBs support TLS passthrough.
- Don't add L7 features you don't need — every feature adds latency.

*Ref: Foundations_of_Scalable_Systems.md — "Load Balancing", "Load Distribution Policies"*

---

### Chandy-Lamport Distributed Snapshots (Flink)

**Principle:** Distributed snapshot algorithms capture consistent global state without stopping the system. Flink uses Chandy-Lamport variant via async barrier injection.

**Mechanism:**
1. Job manager injects **barrier** events into source streams.
2. Barriers flow through the pipeline with the data.
3. When an operator receives a barrier on **all inputs**, it snapshots its state.
4. Barrier is forwarded downstream.
5. Snapshot completes when the sink receives the barrier on all inputs.

**Do:**
- Use Flink's checkpointing for fault tolerance in streaming apps.
- Tune checkpoint interval — too frequent = overhead; too rare = longer recovery.
- Use **incremental checkpoints** for large state.
- Configure **state backend** (RocksDB for large state; memory for small).

**Don't:**
- Don't checkpoint too frequently — overhead dominates throughput.
- Don't checkpoint too rarely — long recovery time.
- Don't store large state in memory — OOM risk.
- Don't skip barrier tracking — debug checkpointing issues with barrier metrics.

*Ref: Foundations_of_Scalable_Systems.md — "Stream Processing Systems", "Data Safety"*

---

### Couchbase — Detailed

**Principle:** Couchbase = distributed document database with N1QL (SQL-like) query language, memory-first architecture, and XDCR for multi-region.

**Do:**
- Use Couchbase for low-latency document workloads with SQL-like queries.
- Configure XDCR for multi-region replication.
- Design documents with **denormalization** for query efficiency.
- Use **N1QL** with appropriate indexes; profile slow queries.
- Apply **TTL** on documents that should auto-expire.

**Don't:**
- Don't expect cross-document transactions to be fast — design for one-aggregate-per-transaction.
- Don't use Couchbase as a primary system of record without proper backup.
- Don't ignore index maintenance cost — too many indexes slow writes.

*Ref: Foundations_of_Scalable_Systems.md — "Couchbase" referenced in NoSQL section*

---

### Database Scaling Approaches (Decision Tree)

**Principle:** Choose scaling approach based on workload characteristics.

```
                    Is single-node scaling sufficient?
                    /                              \
                  Yes                                No
                   |                                 |
            Scale up (bigger                     Read-heavy workload?
            machine)                              /          \
                                            Yes              No
                                             |               |
                                    Add read replicas    Scale up first
                                                         + Then shard
                                                         + Then replicate shards
```

**Do:**
- **Always scale up first** — simpler, retains single-machine semantics.
- Add **read replicas** when reads dominate and staleness is acceptable.
- **Shard** when storage OR throughput exceeds single machine.
- **Replicate** shards for availability (typically 3 replicas per shard).
- Choose **leader-follower** for single-writer consistency; **leaderless** for write scalability.

**Don't:**
- Don't shard prematurely — operational complexity is significant.
- Don't use read replicas for write scaling — they don't help.
- Don't shard on monotonic IDs — creates hot partitions.
- Don't replicate after sharding — both should be designed together.

*Ref: Foundations_of_Scalable_Systems.md — "Scaling Relational Databases", "Scaling Up", "Scaling Out"*

---

### Consistent Hashing

**Principle:** Consistent hashing minimizes data movement when nodes are added/removed in a distributed system (cache, database, message broker).

**Standard hashing:** `node = hash(key) mod N` — adding/removing a node reshuffles ALL keys (catastrophic).

**Consistent hashing:**
- Hash both nodes and keys onto a circular hash space (0 to 2^32-1).
- Each key is stored on the **next node clockwise** from its hash.
- Adding/removing a node only affects keys between that node and its predecessor.

**Do:**
- Use consistent hashing for distributed caches (Redis Cluster, memcached) and databases.
- Use **virtual nodes** (VNodes) — multiple hash positions per physical node — for better load distribution.
- Apply **replication factor** consistently across the ring.

**Don't:**
- Don't use standard mod-N hashing for distributed systems — reshuffles are expensive.
- Don't skip VNodes — without them, load distribution can be very uneven.

*Ref: Foundations_of_Scalable_Systems.md — "Data Distribution", "Scale Out: Partitioning Data"*

---

### Saga Pattern — Detailed

**Principle:** Saga = sequence of local transactions across services, coordinated via events (choreography) or a central orchestrator. Each local transaction has a compensating transaction for rollback.

**Two flavors:**
- **Choreography:** Each service emits events; next service subscribes and reacts.
- **Orchestration:** Central orchestrator explicitly calls each service and triggers compensations on failure.

**Saga components:**
- **Forward action:** Local transaction in a service.
- **Compensating action:** Undo for the forward action.
- **Saga log:** Records saga state for debugging and recovery.

**Do:**
- Design compensating actions as **idempotent** — they may be retried.
- Use **timeouts** — if a step doesn't complete in N seconds, invoke compensation.
- Track saga state via **correlation ID** flowing through events.
- Use **saga log** (separate table) for monitoring and recovery.
- Choose choreography for simple workflows; orchestration for complex ones.

**Don't:**
- Don't use sagas for trivial workflows — overhead exceeds benefit.
- Don't put business logic in orchestrators — they're for coordination only.
- Don't assume compensation always succeeds — design for orphan management.
- Don't forget **idempotency** — retries will happen.

*Ref: Foundations_of_Scalable_Systems.md — Microservices Workflows*

---

### Distributed Tracing — Concepts

**Principle:** Distributed tracing follows a request across service boundaries. Essential for diagnosing latency in microservice architectures.

**Concepts:**
- **Trace:** End-to-end journey of a request through all services.
- **Span:** Single unit of work within a trace (one service call).
- **Trace ID:** Identifier shared across all spans in a trace.
- **Span ID:** Identifier for a specific span.
- **Parent Span ID:** Identifies the calling span.
- **Context propagation:** Pass trace/span IDs across service boundaries (HTTP headers, message metadata).

**Tools:**
- **Jaeger** (CNCF): Distributed tracing platform.
- **Zipkin** (Twitter): Distributed tracing.
- **Tempo** (Grafana): Tracing backend.
- **OpenTelemetry:** Vendor-neutral instrumentation standard.
- **DataDog APM, New Relic, Dynatrace:** Managed solutions.

**Do:**
- Use **OpenTelemetry** for instrumentation — vendor-neutral.
- Propagate trace context via standard headers (`traceparent`, `tracestate`).
- Sample traces (head-based or tail-based) — full tracing is expensive.
- Tag spans with relevant metadata (user ID, request size, errors).
- Trace through **message brokers** — propagate trace ID via message headers.

**Don't:**
- Don't sample 100% — costs scale with traffic.
- Don't use head-based sampling for error traces — they get dropped.
- Don't skip context propagation — broken traces are useless.
- Don't rely on tracing alone — combine with metrics and logs.

*Ref: Foundations_of_Scalable_Systems.md — "Observability"*

---

### Distributed Logging Patterns

**Principle:** Logs in distributed systems must be centralized for correlation and search.

**Patterns:**
- **Structured logging:** JSON logs with consistent fields (timestamp, level, service, trace_id, message, context).
- **Log shipping:** Agent on each host ships logs to centralized store (Fluentd, Filebeat, Promtail).
- **Log aggregation:** Centralized store (Elasticsearch, Loki, Splunk).
- **Log search:** Kibana, Grafana, Splunk search UIs.

**Do:**
- Use **structured logging** (JSON) — parseable, queryable.
- Include **trace ID** in every log line — correlate with traces.
- Use **log levels** consistently (ERROR, WARN, INFO, DEBUG).
- Apply **log sampling** for high-volume DEBUG logs.
- **Centralize logs** — local files in 50 services are useless.

**Don't:**
- Don't log PII (names, emails, credit cards) — log IDs only.
- Don't use unstructured text logs — impossible to query.
- Don't log everything at INFO — overwhelms storage.
- Don't skip trace correlation — breaks observability.

*Ref: Foundations_of_Scalable_Systems.md — "Observability"*

---

### Health Checks & Heartbeats

**Principle:** Health checks enable load balancers to remove unhealthy instances. Three types: liveness, readiness, startup.

**Liveness:** Is the process running?
- Kills and restarts the process if fails.
- Should be cheap (just process check).

**Readiness:** Can the process serve traffic?
- Removes from LB rotation if fails.
- Checks dependencies (DB, cache, downstream services).

**Startup:** Has the process finished initializing?
- Delays liveness/readiness checks during startup.
- Prevents premature restarts during slow startup.

**Do:**
- Implement **separate** liveness, readiness, and startup checks.
- Make readiness checks **comprehensive** (dependencies actually reachable).
- Make liveness checks **cheap** (no external dependencies).
- Apply **grace periods** during startup.
- Use **graceful shutdown** — drain in-flight requests before terminating.

**Don't:**
- Don't combine liveness and readiness — different purposes.
- Don't include expensive operations in liveness checks.
- Don't return 200 OK on readiness when a critical dependency is down.
- Don't ignore health check failures — investigate root cause.

*Ref: Foundations_of_Scalable_Systems.md — "Health Monitoring"*

---

### Statelessness & Session Affinity

**Principle:** Stateless services scale freely. Stateful services require careful handling (session affinity has problems).

**Stateless service:**
- No client-specific state in the process.
- All state in external store (DB, cache, message broker).
- Any replica can handle any request.
- LB can freely distribute.

**Stateful service:**
- Holds client state in process (sessions, in-memory caches).
- Requires affinity to route same client to same replica.
- Imbalanced load (long sessions pin replicas).

**Do:**
- Build **stateless** services whenever possible.
- Externalize session state to **Redis, memcached, or DB**.
- Use **sticky sessions** only as last resort (with documented trade-offs).
- Design for **graceful session migration** when affinity changes.

**Don't:**
- Don't store session state in process memory — kills scalability.
- Don't rely on session affinity without measuring load imbalance.
- Don't put large state in cookies — bandwidth and security issues.

*Ref: Foundations_of_Scalable_Systems.md — "Session Affinity", "State Management"*

---

### Connection Pooling

**Principle:** Creating connections is expensive. Reuse them via pools. Bound pool size to prevent resource exhaustion.

**Java connection pooling:**
- **HikariCP** (JDBC): High-performance JDBC pool.
- **Apache Commons Pool** (general purpose): Configurable object pool.
- **Lettuce** (Redis): Netty-based, async, thread-safe.
- **Jedis** (Redis): Synchronous, requires external pooling.

**Do:**
- Size pools based on **expected concurrency** + **downstream capacity**.
- Set **timeouts** for `borrowObject` (don't wait forever).
- Implement **validation** on borrow (cheap query to verify connection).
- Monitor pool metrics: active, idle, waiting, total.
- Set **max lifetime** to recycle connections (avoid stale connections).

**Don't:**
- Don't create connections on every request — connection setup is expensive.
- Don't set pool size too high — exhausts downstream resources.
- Don't ignore connection leaks (unreturned connections) — common bug.
- Don't skip validation — stale connections cause errors.

**Code: Apache Commons Pool for RabbitMQ channels:**
```java
private boolean sendMessageToQueue(JsonObject message) {
    try {
        Channel channel = pool.borrowObject();
        channel.basicPublish(/* arguments */);
        pool.returnObject(channel);
        return true;
    } catch (Exception e) {
        logger.info("Failed to send message to RabbitMQ");
        return false;
    }
}
```

*Ref: Foundations_of_Scalable_Systems.md — "Distribution and Concurrency" (channel pooling)*

---

### Event-Driven Integration Patterns

**Principle:** Three primary event-driven patterns for service integration.

**1. Event Notification:**
- Producer emits lightweight event ("OrderPlaced").
- Subscribers fetch current state if needed.
- Minimal coupling.
- Risk: subscribers may not have full context.

**2. Event-Carried State Transfer (ECST):**
- Event contains all needed state ("OrderPlaced" with full order details).
- Subscribers maintain local copy.
- Eventually consistent.
- Higher bandwidth, lower coupling.

**3. Event Sourcing:**
- All state changes are events.
- State = function(events).
- Full audit trail; temporal queries.
- Complex; not for simple CRUD.

**Do:**
- Choose **event notification** for simple, fire-and-forget scenarios.
- Choose **ECST** when subscribers need data without re-querying.
- Choose **event sourcing** when audit history matters (finance, compliance).
- Document **event schema** with versioned contracts.
- Use a **published language** for public events; keep private events internal.

**Don't:**
- Don't make every event an ECST — bandwidth cost.
- Don't expose implementation events publicly — couples subscribers to producer's internal model.
- Don't skip event versioning — breaking changes affect all subscribers.

*Ref: Foundations_of_Scalable_Systems.md — "Event-Driven Architectures"*

---

### Two-Phase Commit (2PC) — Detailed

**Principle:** 2PC achieves atomic distributed transactions via prepare + commit phases. It's blocking — coordinator failure after prepare leaves participants waiting.

**Phases:**
1. **Prepare:** Coordinator asks all participants to prepare to commit. Participants acquire locks and persist intent. Reply yes/no.
2. **Commit:** If all yes, coordinator sends commit. If any no, sends abort. Participants apply or roll back.

**Failure modes:**
- **Participant failure before prepare:** Transaction aborted by coordinator.
- **Participant failure after prepare:** Recovered participant asks coordinator for outcome.
- **Coordinator failure after prepare:** Participants block until coordinator recovers (problem!).

**Do:**
- Use 2PC when atomic distributed transactions are non-negotiable.
- Implement **coordinator replication** to avoid single point of failure.
- Set **timeouts** on prepare/commit phases.
- Log transaction context for recovery.
- Combine with Raft/Paxos for non-blocking (Spanner-style).

**Don't:**
- Don't use 2PC for high-throughput cross-service transactions — coordination cost dominates.
- Don't assume 2PC is fast — even when correct, it's expensive.
- Don't rely on 2PC without handling coordinator failure — participants will block.
- Don't use 2PC for >3 participants — coordination cost grows.

*Ref: Foundations_of_Scalable_Systems.md — "Two-Phase Commit"*

---

### Raft Consensus — Detailed

**Principle:** Raft is a leader-based consensus algorithm. Leader accepts updates, replicates to followers, commits on majority vote.

**Sub-problems:**
1. **Leader election:** Followers time out → become candidates → request votes → majority wins.
2. **Log replication:** Leader appends → replicates via AppendEntries → commits on majority ack.
3. **Safety:** Only leaders with all committed entries can win election.

**Properties:**
- Safety: all committed entries survive leader changes.
- Liveness: cluster makes progress as long as majority available.
- Fault tolerance: tolerates ⌊(N-1)/2⌋ failures.

**Do:**
- Use Raft-implemented systems (etcd, MongoDB replica sets, RabbitMQ quorum queues) instead of building custom.
- Size clusters odd (3, 5, 7) — even numbers waste capacity.
- Use 3-node clusters for most production needs; 5 for higher availability.
- Monitor leader changes — frequent elections indicate instability.
- Implement proper **election timeouts** (randomized 150–300 ms typically).

**Don't:**
- Don't use Raft for read-heavy, low-consistency workloads — too much overhead.
- Don't deploy 2-node Raft clusters — no fault tolerance.
- Don't ignore network partition scenarios — leader in minority must step down.
- Don't expose Raft implementation details to application code — use the database's API.

*Ref: Foundations_of_Scalable_Systems.md — "Raft", "Distributed Consensus Algorithms"*

---

### Cloud Spanner's TrueTime

**Principle:** Google Cloud Spanner achieves global strong consistency via TrueTime — a service that returns `[earliest, latest]` time intervals with bounded uncertainty (typically <7 ms).

**Mechanism:**
- Each data center has **GPS receivers** and **atomic clocks**.
- TrueTime returns a time interval, not a single value.
- Transaction commit waits for `wait = uncertainty` to ensure commit timestamp is in the past everywhere.

**Do:**
- Trust the system's guarantees — Spanner's external consistency is mathematically proven (modulo TrueTime assumptions).
- Use Spanner for globally distributed strong consistency requirements.
- Apply TrueTime's pattern conceptually — accept bounded uncertainty in distributed time.
- Document consistency assumptions per use case.

**Don't:**
- Don't use Spanner for workloads that don't need global strong consistency — it's expensive.
- Don't assume TrueTime precision is infinite — there's still a wait period (small but non-zero).
- Don't try to replicate TrueTime's hardware — use the managed service.

*Ref: Foundations_of_Scalable_Systems.md — "Google Cloud Spanner"*

---

### Data Lake & Data Warehouse Patterns

**Principle:** Historical data management needs different storage and query models from operational systems.

**Data Warehouse:**
- Structured, schema-on-write.
- Optimized for analytical queries (OLAP).
- Examples: Snowflake, BigQuery, Redshift.

**Data Lake:**
- Raw, schema-on-read.
- Stores any format (JSON, Parquet, images).
- Examples: S3 + Athena, ADLS + Synapse.

**Lambda Architecture:**
- Batch layer (Hadoop) + Speed layer (Storm) + Serving layer.
- Combines accurate batch with fast streaming.

**Kappa Architecture:**
- Stream-only (Kafka + Flink).
- Replay topic when logic changes — no separate batch.

**Do:**
- Use **data warehouse** for OLAP and business intelligence.
- Use **data lake** for raw data exploration and machine learning.
- Use **Kappa** architecture for new systems unless you genuinely need both batch and speed.
- Apply **retention policies** (GDPR compliance requires data deletion).
- Use **parquet/ORC** for analytical storage — columnar compression.

**Don't:**
- Don't use data lake as primary store — no consistency guarantees.
- Don't use data warehouse for OLTP — wrong tool.
- Don't skip data cataloging — data lakes become data swamps without metadata.
- Don't store PII without encryption and access controls.

*Ref: Foundations_of_Scalable_Systems.md — "Data Lakes"*

---

### Chaos Engineering

**Principle:** Inject failures deliberately to validate system resilience. Netflix's Chaos Monkey pioneered this approach.

**Do:**
- Start chaos experiments in **staging**; graduate to production with safety controls.
- Define **steady state hypothesis** ("P99 latency < 200ms with 1000 RPS").
- Limit **blast radius** — start with single instance, single AZ.
- Have **automatic rollback** if SLOs degrade.
- Use **controlled experiments** — kill one instance at a time, not the entire cluster.
- Document experiments as **game days** — scheduled, rehearsed.

**Don't:**
- Don't run chaos experiments in production without safeguards.
- Don't skip the hypothesis — "let's break stuff" isn't science.
- Don't run chaos experiments during peak traffic.
- Don't run without rollback plan — chaos can become catastrophe.

**Tools:**
- **Chaos Monkey** (Netflix): Random instance termination.
- **Chaos Kong** (Netflix): Multi-AZ failures.
- **Gremlin:** Commercial chaos platform.
- **LitmusChaos:** CNCF chaos engineering.

*Ref: Foundations_of_Scalable_Systems.md — "Simian Army" references in fundamentals, Engineering Practices*

---

### Multi-Region & Global Distribution

**Principle:** Multi-region deployment reduces latency for global users and provides disaster recovery. Cost: consistency complexity.

**Multi-region patterns:**
- **Active-passive:** Primary region serves; secondary on standby for DR.
- **Active-active:** All regions serve traffic; cross-region replication.
- **Geo-routing:** Route users to nearest region (DNS-based or anycast).

**Do:**
- Use **multi-region** for global user base (latency) and DR (resilience).
- Choose **active-active** when low latency is critical everywhere.
- Choose **active-passive** when consistency matters more than latency.
- Apply **geo-partitioning** for data residency (GDPR).
- Use **CDN** for static content to reduce origin load.

**Don't:**
- Don't deploy multi-region unless you actually have global users — cost is high.
- Don't use active-active without conflict resolution — concurrent writes cause conflicts.
- Don't rely on cross-region replication for strong consistency — eventual is the norm.
- Don't skip testing — region failures are real and tested.

*Ref: Foundations_of_Scalable_Systems.md — "Distributing the Database", Multi-region references*

---

### Capacity Planning Process

**Principle:** Capacity planning = matching resources to expected load. Done correctly, it prevents outages and controls costs.

**Process:**
1. **Measure current load:** Requests/second, data volume, peak hours, growth rate.
2. **Project future load:** Apply growth multipliers (50%, 100%, 10x).
3. **Identify bottlenecks:** Profile current system to find the limiting resource.
4. **Model resource needs:** Calculate compute, memory, storage, network for projected load.
5. **Provision with headroom:** 60-70% utilization target (not 100%).
6. **Test under load:** Load tests at, above, below design point.
7. **Monitor and adjust:** Continuously measure and re-plan.

**Do:**
- Set utilization targets **below 100%** — leave room for spikes.
- Plan for **3x peak load** — peaks are unpredictable.
- Monitor **saturation** (queue depth, thread utilization) — that's what fails first.
- Use **statistical models** for scaling decisions — not arbitrary thresholds.
- Document **capacity assumptions** in ADRs.

**Don't:**
- Don't plan for average — peak is what breaks systems.
- Don't size for current peak — peak will grow.
- Don't skip load testing — "it works" ≠ "it scales".
- Don't ignore downstream dependencies — they're part of capacity planning.

*Ref: Foundations_of_Scalable_Systems.md — "Scalability and Costs", Operational Measures references*

---

### Service Decomposition — Detailed Approaches

**Principle:** Decomposing a monolith into microservices is a major architectural decision. Multiple approaches with different trade-offs.

**By business capability:**
- Each service = one business capability (DDD bounded context).
- Most common starting point.
- Aligns with Conway's Law.

**By subdomain:**
- Core, Supporting, Generic subdomains per DDD.
- Different investment per subdomain.

**By transaction:**
- Each service = ACID boundary.
- Avoids distributed transactions.

**By verb/noun:**
- "Place Order", "Process Payment" — action-based.
- Risk: anemic services.

**By team:**
- Two-pizza team per service.
- Aligns with team boundaries.

**Do:**
- Start with **business capabilities** (DDD bounded contexts).
- Iterate on decomposition — first attempt is rarely right.
- Validate with **event storming** workshops.
- Use **bounded context mapping** (Context Map) to identify relationships.

**Don't:**
- Don't decompose by **technical layer** (UI service, DB service) — wrong direction.
- Don't decompose by **CRUD entity** — entity trap.
- Don't decompose prematurely — modular monolith is a valid state.
- Don't try to perfect decomposition upfront — refactor as you learn.

*Ref: Foundations_of_Scalable_Systems.md — "Principles of Microservices", "Breaking Up the Monolith"*

---

### Microservices Communication Styles

**Principle:** Microservices communicate via three primary styles. Choice affects coupling, performance, and complexity.

**1. Synchronous HTTP (REST/RPC):**
- Request-reply semantics.
- Easy to reason about.
- Tight coupling (caller must know endpoint).
- Failure cascades (caller blocks on slow downstream).

**2. Asynchronous messaging:**
- Fire-and-forget or pub/sub.
- Loose coupling.
- Buffer-and-forward handles spikes.
- Eventual consistency.

**3. Event-driven:**
- Services emit events; others subscribe.
- Maximum decoupling.
- Complex debugging (causality tracing).

**Do:**
- Default to **synchronous HTTP** for simple request-reply.
- Use **async messaging** for state changes that don't need immediate response.
- Use **events** for cross-cutting concerns (notifications, analytics).
- Document communication patterns in architecture diagrams.
- Use **API Gateway** as single entry point for clients.

**Don't:**
- Don't use sync HTTP for everything — latency compounds.
- Don't use events for synchronous queries — polling defeats the purpose.
- Don't expose all internal services — use BFF or API Gateway.

*Ref: Foundations_of_Scalable_Systems.md — "Communication", "Workflows"*

---

### CQRS (Command Query Responsibility Segregation)

**Principle:** Separate read and write models. Optimizes each independently. Common with event sourcing.

**Components:**
- **Write side:** Commands → write model (often event-sourced).
- **Read side:** Queries → read model (denormalized, query-optimized).
- **Projections:** Update read model from event stream.

**Do:**
- Use CQRS when **read/write access patterns differ dramatically** (e.g., 1000× more reads than writes).
- Apply when read model benefits from **denormalization** that's painful for write model.
- Combine with **event sourcing** for full audit trail.
- Update read model **asynchronously** for eventual consistency.

**Don't:**
- Don't use CQRS for simple CRUD — added complexity exceeds benefit.
- Don't expect immediate consistency between write and read sides — eventual.
- Don't put business logic in projections — they're for transformation only.
- Don't make read model updates synchronous if writes are hot — kills write throughput.

*Ref: Foundations_of_Scalable_Systems.md — "Event-Driven Architectures" (implicit), CQRS referenced*

---

### Event Sourcing — Detailed

**Principle:** Event sourcing stores state as a sequence of events. Current state = function(events). Provides full audit trail and temporal queries.

**Components:**
- **Events:** Immutable facts ("OrderPlaced", "OrderShipped").
- **Event store:** Append-only log of events.
- **Aggregates:** Current state, built by replaying events.
- **Snapshots:** Periodic state captures to avoid replaying all events.
- **Projections:** Read models built from event stream.

**Do:**
- Use event sourcing when **audit history** matters (finance, compliance).
- Design events as **immutable past-tense facts**.
- Use **snapshots** for aggregates with long event histories.
- Version your event schema — events must be readable forever.
- Use **upcasting** to evolve event schemas without breaking history.

**Don't:**
- Don't use event sourcing for simple CRUD — overkill.
- Don't delete or modify events — append-only is sacred.
- Don't put transient state in events — events are facts, not state.
- Don't ignore event schema migration — old consumers must still work.

*Ref: Foundations_of_Scalable_Systems.md — Event sourcing references*

---

### Lambda vs Kappa Architecture

**Principle:** Lambda = batch + speed layers; Kappa = stream-only. Kappa is simpler; Lambda handles more complex requirements.

**Lambda:**
- Batch layer: accurate but slow (Hadoop).
- Speed layer: fast but approximate (Storm).
- Serving layer: merges batch and speed results.

**Kappa:**
- Single streaming layer (Kafka + Flink).
- Replay events when logic changes.
- Simpler; relies on stream processing maturity.

**Do:**
- Use **Kappa** for new systems — simpler, faster iteration.
- Use **Lambda** when batch results are required for correctness (regulatory, financial).
- Use Kappa when **stream processing** has matured enough for your needs.
- Migrate Lambda → Kappa when batch layer becomes unnecessary.

**Don't:**
- Don't use Lambda without explicit need for batch accuracy — adds complexity.
- Don't use Kappa when stream processing can't meet accuracy requirements.
- Don't deploy both without clear separation of concerns.

*Ref: Foundations_of_Scalable_Systems.md — "The Lambda Architecture"*

---

### Streaming Window Operations

**Principle:** Windows bound computations on unbounded streams. Three primary types.

**Tumbling windows:**
- Non-overlapping fixed-size windows.
- Each event belongs to exactly one window.
- Use for periodic aggregations (count per minute).

**Sliding windows:**
- Overlapping fixed-size windows with slide interval.
- Each event may belong to multiple windows.
- Use for moving averages, trend detection.

**Session windows:**
- Dynamic windows based on activity gaps.
- Events within N seconds of inactivity form a session.
- Use for user activity analysis.

**Do:**
- Use **tumbling** for periodic metrics (requests per minute).
- Use **sliding** for moving averages (P95 over last 10 minutes).
- Use **session** for user-behavior analytics.
- Tune window size based on **cardinality** and **memory**.

**Don't:**
- Don't use **sliding** windows when tumbling suffices — more computation.
- Don't use **session** windows without clear activity-gap definition.
- Don't set window size too large — memory pressure.
- Don't forget window state cleanup — old windows must be evicted.

*Ref: Foundations_of_Scalable_Systems.md — "DataStream API"*

---

### Distributed Cache Invalidation Strategies

**Principle:** Caches become stale when underlying data changes. Choose invalidation strategy based on update patterns.

**Strategies:**
1. **TTL-based:** Expire after N seconds. Simple; may serve stale data within TTL.
2. **Event-driven invalidation:** Publish invalidation event when data changes. Proactive; requires pub/sub.
3. **Write-through cache:** Cache updated atomically with DB. Consistent; write latency cost.
4. **Cache-aside lazy:** Application invalidates on write. Simple; cache-miss storm risk.

**Do:**
- Use **TTL** as a baseline safety net — always set it.
- Combine TTL with **event-driven invalidation** for freshness.
- Use **cache-aside** for read-heavy workloads.
- Monitor **hit ratio** — <80% means cache is poorly tuned.

**Don't:**
- Don't rely on TTL alone for rapidly changing data — staleness window too long.
- Don't invalidate caches during writes without batching — performance impact.
- Don't skip TTL — caches without TTL grow unbounded.

*Ref: Foundations_of_Scalable_Systems.md — "Distributed Caching", "Application Caching"*

---

### Quorum Tuning — Detailed

**Principle:** Tune R (read quorum) and W (write quorum) for workload. Trade off latency, consistency, availability.

**Common configurations (N=3):**
- **R=2, W=2:** Strong consistency, balanced. Tolerates 1 failure.
- **R=1, W=3:** Strong consistency on reads; slow writes. Tolerates 0 failures during writes.
- **R=3, W=1:** Fast writes; slow reads. Strong on reads.
- **R=1, W=1:** Fast; eventual consistency. No fault tolerance.

**For higher availability:**
- **N=5, R=3, W=3:** Tolerates 2 failures; slower.
- **Sloppy quorum:** R/W from different replicas than canonical set (Cassandra-style).

**Do:**
- Default to **R=W=⌊N/2⌋+1** for balanced strong consistency.
- Choose **R=1, W=N** for write-heavy with strong reads.
- Choose **R=N, W=1** for read-heavy with strong reads.
- Use **sloppy quorums** for high availability (Cassandra-style).

**Don't:**
- Don't use R=W=1 for data requiring consistency — stale reads likely.
- Don't use R=W=N if single failure stops all operations.
- Don't confuse "consistent reads" with strong consistency — depends on prior write W.

*Ref: Foundations_of_Scalable_Systems.md — "Quorum Reads and Writes"*

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
- **Architectural Quantum Violations**: Treating all communication as asynchronous just because it uses a queue — *fix:* align quantum with synchronous connascence.
- **CAP Letter Worship**: Picking AP or CP for marketing — *fix:* tune consistency per use case, document choices.
- **Layered Architecture Sinkhole**: >80% requests pass through without logic — *fix:* switch to different style or accept trade-off of open layers.
- **Entity Microservice**: One service per table — *fix:* use bounded contexts.
- **Distributed Monolith**: Independently deployable but coupled at release — *fix:* enforce data isolation.
- **Shared Database**: Multiple services sharing one DB — *fix:* one DB per service.
- **No Backpressure**: Slow consumer causes producer OOM — *fix:* implement bounded queues + fail fast.
- **Missing Idempotency on Non-idempotent Operations**: Retried POST creates duplicates — *fix:* use idempotency keys.
- **Untested DR Plans**: Backups you haven't restored are guesses — *fix:* quarterly DR drills.
- **Magic Number Concurrency**: Thread pool size = `Runtime.getRuntime().availableProcessors()` without measurement — *fix:* empirical load testing.
- **Synchronous Microservice Chains**: A → B → C → D in request path — *fix:* async where possible; aggregate responses.

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
- **ACID needed across services?** Use Saga; design for one-aggregate-per-transaction; embrace eventual consistency.
- **Strong consistency required?** Use 2PC + Raft/Paxos; expect throughput cost.
- **High write throughput required?** Use leaderless replication (Cassandra, DynamoDB); tune write concern low.
- **Hot partition detected?** Use write-sharding (split hot key into N) or cache layer.
- **Time to migrate to microservices?** When team size > 20-30 OR release cadence varies by component OR scaling varies by component.

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
11. **Asynchronous is not always better.** Synchronous request-reply is fine for queries; async for state changes.
12. **NoSQL joins are expensive or missing.** Denormalize for query patterns; model for solution domain.
13. **CAP is tunable, not categorical.** Most modern databases let you choose consistency level per operation.
14. **Idempotence keys + transactions = exactly-once semantics.** The combination, not one alone.
15. **Quorum math = consistency.** R + W > N guarantees strong consistency; choose W and R for workload.

## Cross-References
- Related: `Learning_Domain_Driven_Design.md` — DDD bounded contexts inform microservice boundaries.
- Related: `Domain_Driven_Design_with_Golang.md` — DDD applied with ports/adapters in Go code.
- Related: `Building_Microservices.md` — Deeper coverage of microservices patterns.
- Related: `Building_Event-driven_Microservices.md` — Event-driven architecture deep dive.
- Related: `Building_An_Event-Driven_Data_Mesh.md` — Data mesh + event-driven architecture.
- Related: `Engineering_Resilient_Systems_on_AWS.md` — Resilience patterns on AWS.
- Related: `Communication_Patterns.md` — Service communication patterns.
- Topic index: `INDEX.md`