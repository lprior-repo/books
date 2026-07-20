# System Design Interview: An Insider's Guide (2nd Edition)
**Author:** Alex Xu
**Topic tags:** `#architecture` `#systems` `#interview`
**Language focus:** Language-agnostic (architecture diagrams, pseudo-protocols, SQL, REST)
**Sources:** `markdown_output/System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu/System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md` · `summaries/System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md`

## TL;DR
A repeatable 4-step framework (understand → high-level → deep dive → wrap up) applied to twelve classic distributed-system design problems. The book's two non-negotiables: (1) every design is a trade-off — strong consistency vs. availability, push vs. pull, CDN cost vs. latency — and (2) the same handful of primitives (load balancer, cache, CDN, message queue, consistent hashing, sharding, replication, quorum) appear in every design. Use it as the canonical interview playbook and as a primer on Dynamo-style systems, Twitter Snowflake IDs, trie-based autocomplete, YouTube DAG transcoding, and Google Drive block-level sync.

---

## Best Practices by Topic

### The 4-Step Interview Framework

**Principle:** Never jump to a solution — run a deterministic four-step process and treat the interviewer as a teammate.

**Do:**
- Spend 3–10 min on Step 1: understand the problem & establish design scope.
- Spend 10–15 min on Step 2: propose high-level design and get buy-in (box diagram + back-of-envelope + concrete use cases).
- Spend 10–25 min on Step 3: deep dive on the prioritised components the interviewer cares about.
- Spend 3–5 min on Step 4: wrap up — bottlenecks, recap, error cases, operations, next scale curve.

**Don't:**
- Don't dive into a single component's details before the high-level blueprint is agreed.
- Don't think in silence — narrate.
- Don't say the design is perfect; always propose improvements.

**Time allocation (45-min session):**
```
Step 1 Understand the problem and establish design scope: 3 - 10 minutes
Step 2 Propose high-level design and get buy-in:          10 - 15 minutes
Step 3 Design deep dive:                                  10 - 25 minutes
Step 4 Wrap:                                              3 - 5 minutes
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Time allocation on each step"*

---

### Step 1 — Understand & Establish Scope

**Principle:** Asking the right questions is more important than answering fast; "no right answer" exists.

**Do:**
- Ask: *What specific features? How many users? Anticipated scale at 3/6/12 months? Tech stack? Existing services to leverage?*
- Write assumptions on the whiteboard so you can refer back.
- Treat the interviewer as the customer who has the requirements.

**Don't:**
- Don't be "Jimmy" — answering first without understanding the problem is a red flag.
- Don't assume your assumptions are correct; verify.

**Sample clarification exchange (news feed):**
```
Candidate: Is this a mobile app? Or a web app? Or both?
Interviewer: Both.
Candidate: What are the most important features for the product?
Interviewer: Ability to make a post and see friends' news feed.
Candidate: Is the news feed sorted in reverse chronological order or a particular order?
Interviewer: To keep things simple, let us assume the feed is sorted by reverse chronological order.
Candidate: How many friends can a user have?
Interviewer: 5000
Candidate: What is the traffic volume?
Interviewer: 10 million daily active users (DAU)
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Step 1 - Understand the problem and establish design scope" (Ch. 3)*

---

### Step 2 — High-Level Design & Buy-in

**Principle:** Sketch a blueprint with clients/APIs/web servers/data stores/cache/CDN/message queue, then walk through concrete use cases.

**Do:**
- Draw box diagrams; ask for feedback at each layer.
- Do back-of-the-envelope to validate the blueprint fits scale.
- Run through 1–2 happy-path use cases to discover edge cases.

**Don't:**
- Don't include API endpoints or schema for very large problems (e.g. "design Google search"); do include them for bounded problems (e.g. poker backend). Decide with the interviewer.

---

### Step 3 — Deep Dive

**Principle:** Prioritise the components the interviewer hints at; show depth without losing time.

**Do:**
- For a URL shortener, dive into the hash function; for a chat system, into latency and presence; for KV store, into quorum & vector clocks.
- Manage time aggressively — "talking about the EdgeRank algorithm in detail is not ideal."

**Don't:**
- Don't get lost in irrelevant details (e.g. ranking algorithm internals).

---

### Step 4 — Wrap Up

**Principle:** Never claim perfection — surface bottlenecks, recap, and discuss the next scale curve.

**Do:**
- Identify bottlenecks and proposed improvements.
- Recap if multiple solutions were offered.
- Discuss error cases (server failure, network loss), operation issues (monitoring/logging, rollout), and the next scale curve (1M → 10M users).

**Don't:**
- Don't end when you "give the design"; you are done only when the interviewer says so.

---

### Interview Dos and Don'ts

**Dos:**
- Always ask for clarification. Do not assume your assumption is correct.
- Understand the requirements of the problem.
- There is neither the right answer nor the best answer.
- Let the interviewer know what you are thinking. Communicate.
- Suggest multiple approaches if possible.
- Bounce ideas off the interviewer.
- Never give up.

**Don'ts:**
- Don't be unprepared for typical interview questions.
- Don't jump into a solution without clarifying requirements and assumptions.
- Don't go into too much detail on a single component in the beginning. Give the high-level design first then drills down.
- If you get stuck, don't hesitate to ask for hints.
- Don't think in silence.
- Don't think your interview is done once you give the design.

*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Dos" / "Don'ts" (Ch. 3)*

---

### Single Server Setup — Where Every System Starts

**Principle:** Begin with everything on one box, then evolve — but never present single-server as the *final* design at scale.

**Request flow (Figure 1-2):**
```
1. Users access websites through domain names, such as api.mysite.com.
   Usually DNS is a paid service provided by 3rd parties.
2. Internet Protocol (IP) address is returned to the browser or mobile app.
3. Once IP is obtained, HTTP requests are sent directly to your web server.
4. The web server returns HTML pages or JSON response for rendering.
```

**Traffic sources:**
- Web app: server-side (Java/Python) + client-side (HTML/JS).
- Mobile app: HTTP + JSON.

**Sample API:**
```
GET /users/12 – Retrieve user object for id = 12
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Single server setup" (Ch. 1)*

---

### Relational vs NoSQL — Database Choice

**Principle:** Default to relational; switch to NoSQL only when one of these is true.

**Use NoSQL when:**
- Your application requires super-low latency.
- Your data are unstructured, or you do not have any relational data.
- You only need to serialize and deserialize data (JSON, XML, YAML, etc.).
- You need to store a massive amount of data.

**NoSQL categories:** key-value stores, graph stores, column stores, document stores. Join operations are generally *not* supported.

**Don't:**
- Don't default to NoSQL for transactional/ACID workloads (banks, billing).

*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Which databases to use?" (Ch. 1)*

---

### Vertical vs Horizontal Scaling

**Principle:** Vertical ("scale up") is simple but bounded; horizontal ("scale-out") is the only path to large scale.

**Do:**
- Use vertical scaling when traffic is low.
- Plan horizontal scaling from day one for any service expected to grow.

**Don't:**
- Vertical scaling has a hard limit — "it is impossible to add unlimited CPU and memory to a single server."
- Vertical scaling has no failover/redundancy — one server down = whole site down.

---

### Load Balancer

**Principle:** Distribute traffic across a server pool using private IPs; the load balancer is the only public-facing endpoint.

**Do:**
- Put web servers behind a load balancer; communicate between servers via private IPs.
- Add servers to the pool elastically; the LB routes automatically.

**Failure handling:**
- If server 1 goes offline, all traffic routes to server 2; spin up a replacement.
- If traffic grows, add more servers — LB handles it gracefully.

*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Load balancer" (Ch. 1)*

---

### Database Replication (Master-Slave)

**Principle:** Master handles writes; slaves handle reads. Replication gives performance, reliability, and high availability.

**Advantages:**
- **Better performance:** reads distributed across slaves; writes parallel on master.
- **Reliability:** data survives natural disasters.
- **High availability:** site stays up when a DB node is offline.

**Failover model:**
- One slave down → reads redirect to master (or other slaves).
- Master down → promote a slave; new slave replaces it; missing data recovered via scripts.
- Multi-master / circular replication exist but are more complex.

*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Database replication" (Ch. 1)*

---

### Cache Tier — Read-Through Pattern

**Principle:** Use a cache for read-frequently, write-rarely data; never treat cache as a persistent store.

**Read-through flow:**
1. Web server checks cache.
2. Hit → return to client.
3. Miss → query DB → store response in cache → return.

**Cache considerations:**
- **Decide when to cache:** read-frequently, modify-infrequently. Volatile memory loses everything on restart — keep important data in persistent stores.
- **Expiration policy:** not too short (DB thrash) and not too long (stale data).
- **Consistency:** keeping cache and DB in sync is hard, especially multi-region (see Facebook's "Scaling Memcache at Facebook").
- **Mitigating failures:** a single cache is a SPOF — use multiple cache servers across data centers; over-provision memory.
- **Eviction policy:** LRU (most popular), LFU, FIFO.

---

### CDN — Content Delivery Network

**Principle:** CDNs deliver static content (images/CSS/JS/video) from edge servers geographically close to users.

**Workflow (Figure 1-10):**
```
1. User A requests image.png via CDN URL (e.g. https://mysite.cloudfront.net/logo.jpg).
2. If miss, CDN fetches from origin (web server or S3).
3. Origin returns image.png with optional TTL header.
4. CDN caches the image; returns to User A. Cached until TTL expires.
5. User B requests same image.
6. Returned from cache (no origin hit).
```

**Considerations:**
- **Cost:** charged for data transfer in/out. Don't cache infrequently used assets.
- **Cache expiry:** neither too long (stale) nor too short (origin reload).
- **CDN fallback:** clients must detect CDN failure and fall back to origin.
- **Invalidation:** either call CDN vendor API, or use object versioning (`image.png?v=2`).

**Sample CDN URLs:**
```
https://mysite.cloudfront.net/logo.jpg
https://mysite.akamai.com/image-manager/img/logo.jpg
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Content delivery network (CDN)" (Ch. 1)*

---

### Stateless Web Tier

**Principle:** Move session state out of web servers into a shared data store (NoSQL recommended); only then does horizontal autoscaling work.

**Stateful (anti-pattern):**
- Server 1 stores User A's session; all A's requests must hit Server 1 → requires sticky sessions, harder to add/remove servers, harder to handle failure.

**Stateless:**
- HTTP requests routed to any web server; state fetched from shared store.
- "A stateless system is simpler, more robust, and scalable."
- Enables autoscaling — add/remove servers based on traffic.

---

### Multi-Data-Center Architecture

**Principle:** Geo-route users to the nearest DC (GeoDNS); replicate data across DCs; automate deployment.

**Challenges:**
- **Traffic redirection:** GeoDNS based on user location.
- **Data synchronization:** replicate across DCs so traffic can fail over. Netflix uses asynchronous multi-DC replication (active-active).
- **Test and deployment:** automated deployment tools keep services consistent across DCs.

**Failover:** if DC2 (US-West) goes offline, 100% of traffic routes to DC1 (US-East).

---

### Message Queue — Decouple Producers/Consumers

**Principle:** Use a message queue to decouple components so producer and consumer scale and fail independently.

**Model (Figure 1-17):**
- Producers/publishers create messages, publish to queue.
- Consumers/subscribers connect, perform actions.
- Queue is durable, in-memory, asynchronous buffer.

**Use case:** photo customization (crop/sharpen/blur). Web servers publish jobs; workers pull and process asynchronously. Scale workers up when queue grows; down when empty.

---

### Logging, Metrics, Automation

**Principle:** At scale, these are mandatory, not optional.

**Do:**
- **Logging:** per-server error logs OR aggregated to a centralized service.
- **Metrics:**
  - Host-level: CPU, memory, disk I/O.
  - Aggregated: database tier, cache tier performance.
  - Key business: DAU, retention, revenue.
- **Automation:** CI per check-in; automate build/test/deploy.

---

### Database Scaling — Vertical vs Sharding

**Principle:** Vertical scaling (bigger box) is bounded and a SPOF risk; sharding distributes data across servers using a sharding key.

**Sharding key rules:**
- Choose a key that distributes data evenly (e.g. `user_id`).
- Hash function: `user_id % 4` → shard 0/1/2/3.

**Sharding challenges:**
- **Resharding data:** needed when (1) a single shard overflows, or (2) shards exhaust unevenly. Consistent hashing solves this (Ch. 5).
- **Celebrity / hotspot key problem:** Katy Perry, Justin Bieber, Lady Gaga on one shard = read overload. Allocate a shard per celebrity; sub-partition further.
- **Joins & de-normalization:** joins across shards are hard; denormalize so queries fit one table.

**Reference data point:** Stack Overflow in 2013 had 10M+ monthly uniques on one master DB; Amazon RDS offers up to 24 TB RAM machines. Single-box works until it doesn't.

---

### Power of Two — Memory Units

**Principle:** Always reason in powers of two for storage math.

```
| Power | Approximate value | Full name  | Short name |
|-------|-------------------|------------|------------|
| 10    | 1 Thousand        | 1 Kilobyte | 1 KB       |
| 20    | 1 Million         | 1 Megabyte | 1 MB       |
| 30    | 1 Billion         | 1 Gigabyte | 1 GB       |
| 40    | 1 Trillion        | 1 Terabyte | 1 TB       |
| 50    | 1 Quadrillion     | 1 Petabyte | 1 PB       |
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Power of two" (Ch. 2)*

---

### Latency Numbers Every Programmer Should Know

**Principle:** Memorize Jeff Dean's 2010 numbers (still directionally correct). Conclusions: memory is fast, disk is slow, compress before sending, cross-region round trips are expensive.

```
| Operation name                                | Time                    |
|-----------------------------------------------|-------------------------|
| L1 cache reference                            | 0.5 ns                  |
| Branch mispredict                             | 5 ns                    |
| L2 cache reference                            | 7 ns                    |
| Mutex lock/unlock                             | 100 ns                  |
| Main memory reference                         | 100 ns                  |
| Compress 1K bytes with Zippy                  | 10,000 ns = 10 us       |
| Send 2K bytes over 1 Gbps network             | 20,000 ns = 20 us       |
| Read 1 MB sequentially from memory            | 250,000 ns = 250 us     |
| Round trip within the same datacenter         | 500,000 ns = 500 us     |
| Disk seek                                     | 10,000,000 ns = 10 ms   |
| Read 1 MB sequentially from the network       | 10,000,000 ns = 10 ms   |
| Read 1 MB sequentially from disk              | 30,000,000 ns = 30 ms   |
| Send packet CA ->Netherlands->CA              | 150,000,000 ns = 150 ms |
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Latency numbers every programmer should know" (Ch. 2)*

---

### Availability Numbers — The Nines

**Principle:** SLAs are measured in "nines"; each nine costs exponentially more.

```
| Availability % | Downtime per day    | Downtime per year |
|----------------|---------------------|-------------------|
| 99%            | 14.40 minutes       | 3.65 days         |
| 99.9%          | 1.44 minutes        | 8.77 hours        |
| 99.99%         | 8.64 seconds        | 52.60 minutes     |
| 99.999%        | 864.00 milliseconds | 5.26 minutes      |
| 99.9999%       | 86.40 milliseconds  | 31.56 seconds     |
```
Cloud providers (Amazon, Google, Microsoft) typically set SLAs at 99.9% or above.
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Availability numbers" (Ch. 2)*

---

### Estimation Walkthrough — Twitter QPS & Storage

**Assumptions:**
- 300M MAU.
- 50% use daily.
- 2 tweets/day per user.
- 10% of tweets contain media.
- 5-year retention.

**QPS:**
```
Daily active users (DAU) = 300 million * 50% = 150 million
Tweets QPS = 150 million * 2 tweets / 24 hour / 3600 seconds = ~3500
Peek QPS = 2 * QPS = ~7000
```

**Storage (media only):**
```
Average tweet size:
  tweet_id 64 bytes
  text     140 bytes
  media    1 MB
Media storage: 150 million * 2 * 10% * 1 MB = 30 TB per day
5-year media storage: 30 TB * 365 * 5 = ~55 PB
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Example: Estimate Twitter QPS and storage requirements" (Ch. 2)*

---

### Back-of-the-Envelope Tips

**Do:**
- **Round and approximate** — precision is not expected. `99987 / 9.1` → `100,000 / 10`.
- **Write down assumptions** on the board for later reference.
- **Label units** — "5" means nothing; "5 MB" is unambiguous.
- **Practice common types:** QPS, peak QPS, storage, cache, number of servers.

**Don't:**
- Don't waste time on complicated arithmetic.

---

### Rate Limiter — Why and Where

**Principle:** Control request rate to prevent DoS, reduce cost (paid third-party APIs), and prevent server overload.

**Placement options:**
- **Client-side:** unreliable — clients can forge requests.
- **Server-side:** classic placement (Figure 4-1).
- **API gateway middleware:** fully managed; supports rate limiting, SSL termination, auth, IP whitelisting, static content.

**Decision guidelines:**
- Evaluate current tech stack (language efficiency for server-side).
- Identify the right algorithm — server-side gives full control; gateway may limit options.
- If you already use microservices + API gateway, add rate limiter to the gateway.
- If you lack engineering resources, a commercial gateway is better.

**Examples:**
- Twitter: 300 tweets / 3 hours.
- Google Docs: 300 read requests / user / 60 seconds.

---

### Rate Limiting Algorithms — Decision Matrix

| Algorithm              | Pros                                              | Cons                                                       | Used by          |
|------------------------|---------------------------------------------------|------------------------------------------------------------|------------------|
| Token bucket           | Simple, memory efficient, allows bursts           | Tuning bucket size + refill rate                           | Amazon, Stripe   |
| Leaking bucket         | Stable outflow rate                               | Bursts fill queue with old requests → recent ones dropped  | Shopify          |
| Fixed window counter   | Simple, memory efficient                          | Up to 2x limit at window boundaries                        | —                |
| Sliding window log     | Very accurate                                     | High memory usage (rejected timestamps still stored)       | —                |
| Sliding window counter | Smooths spikes, memory efficient                  | Approximate (Cloudflare: 0.003% error over 400M requests)  | Cloudflare       |

---

### Token Bucket Algorithm

**Principle:** Bucket of fixed capacity; tokens refill at fixed rate; each request consumes one token.

**Parameters:**
- Bucket size (max tokens).
- Refill rate (tokens/sec).

**Multi-bucket rules:**
- Different buckets per API endpoint (1 post/sec + 150 friends/day + 5 likes/sec = 3 buckets/user).
- IP-based throttling → one bucket/IP.
- Global cap (10,000 req/sec) → one shared bucket.

**Pros:** easy to implement, memory efficient, allows bursts. **Cons:** tuning is hard.

---

### Leaking Bucket Algorithm

**Principle:** FIFO queue; requests processed at a fixed rate regardless of arrival.

**Parameters:**
- Bucket size = queue size.
- Outflow rate (req/sec).

**Pros:** memory efficient, stable outflow. **Cons:** burst fills queue with old requests, blocking recent ones; tuning hard.

---

### Fixed Window Counter

**Principle:** Divide timeline into fixed windows; counter per window; reject when threshold reached.

**Major flaw:** bursts at window edges allow 2x limit (5 req between 2:00:00–2:01:00 + 5 req between 2:01:00–2:02:00 = 10 req in the minute 2:00:30–2:01:30).

**Pros:** simple, memory efficient. **Cons:** spike at edges.

---

### Sliding Window Log

**Principle:** Store timestamps of all requests; remove outdated; accept if log size ≤ limit.

```
Algorithm:
- Keep request timestamps in cache (Redis sorted sets).
- On new request: remove all outdated timestamps (older than current window start).
- Add new timestamp.
- If log size <= limit: accept. Else: reject (timestamp remains).
```

**Pros:** very accurate. **Cons:** high memory usage — even rejected requests' timestamps are stored.

---

### Sliding Window Counter

**Principle:** Hybrid of fixed window + sliding log; weighted count of previous window.

**Formula:**
```
Requests in current window + requests in previous window * overlap % of rolling window & previous window
```

**Example:** limit 7 req/min, 5 in previous, 3 in current, 30% position:
```
3 + 5 * 0.7% = 6.5 -> rounded down to 6
```
Under 7 → accept; next request will hit limit.

**Pros:** smooths spikes, memory efficient. **Cons:** approximate (assumes even distribution). Cloudflare measured only 0.003% errors over 400M requests.

---

### Rate Limiter High-Level Architecture

**Principle:** Use Redis as in-memory counter store; rules on disk, cached by workers.

**Redis commands:**
```
INCR:   increases the stored counter by 1.
EXPIRE: sets a timeout; counter auto-deleted when expired.
```

**Flow (Figure 4-12):**
1. Client → rate limiting middleware.
2. Middleware fetches counter from Redis bucket, checks limit.
3. Limit reached → reject.
4. Not reached → forward to API servers, increment counter, save to Redis.

---

### Rate Limiting Rules (Lyft-Style Config)

**Principle:** Declarative configuration files rule the limiter; workers pull from disk into cache.

**Marketing messages (5/day):**
```yaml
domain: messaging
descriptors:
 - key: message_type
 Value: marketing
 rate_limit:
 unit: day
 requests_per_unit: 5
```

**Login attempts (5/minute):**
```yaml
domain: auth
descriptors:
 - key: auth_type
 Value: login
 rate_limit:
 unit: minute
 requests_per_unit: 5
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Rate limiting rules" (Ch. 4)*

---

### Rate Limiter HTTP Headers

**Principle:** Communicate throttling state to clients via standard headers.

```
X-Ratelimit-Remaining:   remaining allowed requests within the window.
X-Ratelimit-Limit:       how many calls per time window are allowed.
X-Ratelimit-Retry-After: seconds to wait before a non-throttled request.
```
On throttle → HTTP **429 Too Many Requests** + `X-Ratelimit-Retry-After`.

---

### Rate Limiter in Distributed Environments

**Race condition:**
- Counter read → check +1 → increment + write back. Concurrent threads can both read 3, write 4 → should be 5.
- **Don't** use locks (slow). **Do** use **Lua script** or **Redis sorted sets**.

**Synchronization:**
- Sticky sessions are neither scalable nor flexible.
- **Use centralized Redis** (Figure 4-16) — all limiter instances share state.

---

### Rate Limiter Performance & Monitoring

**Performance:**
- Multi-data center with edge servers (Cloudflare: 194 edge locations as of 5/20/2020).
- Synchronize with eventual consistency.

**Monitoring:**
- Algorithm effectiveness.
- Rule effectiveness (too strict → valid requests dropped; flash sale → switch to token bucket).

---

### Consistent Hashing — The Rehashing Problem

**Principle:** `hash(key) % N` redistributes nearly all keys when N changes — "a storm of cache misses."

**Example (Table 5-1, 4 servers, 8 keys):**
```
| key  | hash     | hash % 4 |
|------|----------|----------|
| key0 | 18358617 | 1        |
| key1 | 26143584 | 0        |
| key2 | 18131146 | 2        |
| key3 | 35863496 | 0        |
| key4 | 34085809 | 1        |
| key5 | 27581703 | 3        |
| key6 | 38164978 | 2        |
| key7 | 22530351 | 3        |
```

After `server 1` removed, `hash % 3`:
```
| key  | Hash     | hash % 3 |
|------|----------|----------|
| key0 | 18358617 | 0        |
| key1 | 26143584 | 0        |
| key2 | 18131146 | 1        |
| key3 | 35863496 | 2        |
| key4 | 34085809 | 1        |
| key5 | 27581703 | 0        |
| key6 | 38164978 | 1        |
| key7 | 22530351 | 0        |
```
Most keys are redistributed → cache miss storm.
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "The rehashing problem" (Ch. 5)*

---

### Consistent Hashing — Hash Space and Ring

**Principle:** Map both servers and keys onto the same ring (SHA-1, range 0..2^160-1); only k/n keys move on resize.

**Lookup:** walk clockwise from key's position until a server is found.

**Add server 4:** only `key0` moves from server 0 to server 4. Others stay.

**Remove server 1:** only `key1` moves to server 2. Others stay.

---

### Consistent Hashing — Two Issues & Virtual Nodes

**Issue 1:** partitions can be wildly unequal (server 2's partition can be 2x server 0's).

**Issue 2:** key distribution can be non-uniform — most keys may land on server 2, leaving server 1/3 idle.

**Fix — virtual nodes (replicas):**
- Each real server represented by multiple virtual nodes (`s0_0`, `s0_1`, `s0_2` for server 0).
- With 100–200 virtual nodes, standard deviation = 5–10% of mean.
- More virtual nodes = more balanced + more metadata to store. Trade-off tunable.

---

### Consistent Hashing — Find Affected Keys

**On add `s4`:** affected range starts from `s4` (new node), moves **anticlockwise** until a server is found (`s3`). Keys between `s3` and `s4` redistribute to `s4`.

**On remove `s1`:** affected range from `s1` anticlockwise until `s0`. Keys between `s0` and `s1` redistribute to `s2`.

---

### Consistent Hashing — Real-World Usage

**Benefits:** minimised redistribution, easy horizontal scaling, mitigates hotspot key problem.

**Used in:**
- Amazon Dynamo (partitioning).
- Apache Cassandra (cluster-wide data partitioning).
- Discord chat application.
- Akamai CDN.
- Google Maglev network load balancer.

---

### Key-Value Store — CAP Theorem

**Principle:** A distributed system can provide at most **two** of: Consistency, Availability, Partition tolerance. Since partitions are unavoidable, the real choice is CP vs AP.

**Definitions:**
- **Consistency:** all clients see the same data at the same time.
- **Availability:** any client gets a response even if some nodes are down.
- **Partition Tolerance:** system operates despite network partitions.

**System types:**
- **CP:** blocks writes during partition to preserve consistency (banks).
- **AP:** accepts writes during partition; returns stale reads (Dynamo, Cassandra).
- **CA:** cannot exist in real-world distributed systems (network failure is unavoidable).

---

### Key-Value Store — Data Partition

**Principle:** Use consistent hashing to spread data evenly and minimise movement on topology changes.

**Advantages of consistent hashing for partitioning:**
- **Automatic scaling:** add/remove servers based on load.
- **Heterogeneity:** virtual nodes proportional to server capacity — bigger servers get more virtual nodes.

---

### Key-Value Store — Data Replication

**Principle:** Replicate data to N servers by walking clockwise from the key's position.

**With virtual nodes:** only choose *unique physical servers* during the clockwise walk (the first N virtual nodes may belong to fewer than N physical servers).

**Reliability:** replicas placed in distinct data centers connected by high-speed networks (so a single DC outage doesn't lose all replicas).

---

### Key-Value Store — Quorum Consensus (N, W, R)

**Definitions:**
- `N` = number of replicas.
- `W` = write quorum (acks required for write success).
- `R` = read quorum (responses required for read success).

**Strong consistency rule:**
```
If W + R > N, strong consistency is guaranteed because at least one overlapping node has the latest data.
```

**Common configurations:**
```
W = 1, R = N : fast read
W = N, R = 1 : fast write
N = 3, W = R = 2 : balanced strong consistency
W + R <= N  : strong consistency NOT guaranteed
```
The coordinator is a proxy between client and nodes; it does not mean only one node holds the data.

---

### Key-Value Store — Consistency Models

| Model              | Behaviour                                                        |
|--------------------|------------------------------------------------------------------|
| Strong             | Read returns most recent write; blocks until replicas agree      |
| Weak               | Subsequent reads may not see most recent value                   |
| Eventual           | Given enough time, all replicas converge (Dynamo, Cassandra)     |

**Trade-off:** strong consistency blocks new ops during agreement → bad for highly available systems. Dynamo & Cassandra use eventual consistency.

---

### Key-Value Store — Versioning & Vector Clocks

**Principle:** Each modification = new immutable version. Vector clocks `[server, version]` detect ancestor vs sibling (conflict).

**Rules for write to server `Si`:**
- Increment `vi` if `[Si, vi]` exists.
- Otherwise create new entry `[Si, 1]`.

**Worked example (Figure 6-9):**
```
1. Client writes D1 to Sx  -> D1[(Sx, 1)]
2. Client updates to D2 (via Sx) -> D2([Sx, 2])
3. Client updates to D3 (via Sy) -> D3([Sx, 2], [Sy, 1])
4. Client updates to D4 (via Sz) -> D4([Sx, 2], [Sz, 1])
5. Client reads D3 & D4 -> conflict detected -> resolved by client
   -> D5([Sx, 3], [Sy, 1], [Sz, 1]) via Sx
```

**Ancestor rule:** `X` is ancestor of `Y` if every participant's counter in `Y` ≥ counter in `X`. Example: `D([s0,1],[s1,1])` is ancestor of `D([s0,1],[s1,2])`.

**Sibling rule:** if any participant's counter in `Y` < in `X`, they are siblings (conflict). Example: `D([s0,1],[s1,2])` vs `D([s0,2],[s1,1])`.

**Downsides:** client must implement conflict resolution; clock pairs grow — prune oldest entries above threshold (Dynamo reports no production issues).

---

### Key-Value Store — Failure Detection (Gossip Protocol)

**Principle:** Don't trust a single source to mark a server down — use decentralised gossip.

**Algorithm:**
1. Each node maintains a membership list (member IDs + heartbeat counters).
2. Each node periodically increments its own heartbeat counter.
3. Each node periodically sends heartbeats to a random set of nodes; those propagate further.
4. Receivers update membership list to latest.
5. If heartbeat hasn't increased for a predefined period → member marked offline.

**All-to-all multicasting** is the simple alternative but does not scale.

---

### Key-Value Store — Handling Temporary Failures

**Sloppy quorum:** instead of strict quorum, pick first W healthy servers (write) / first R healthy servers (read) on the ring. Offline servers ignored.

**Hinted handoff:** if `s2` is unavailable, `s3` handles requests temporarily. When `s2` returns, `s3` pushes data back.

---

### Key-Value Store — Handling Permanent Failures (Merkle Trees)

**Principle:** Anti-entropy protocol using Merkle trees (hash trees) to detect differences efficiently; only divergent buckets are synced.

**Building a Merkle tree (key space 1–12):**
1. Divide key space into buckets (e.g. 4).
2. Hash each key in a bucket.
3. Create a single hash node per bucket.
4. Build the tree upwards to root by hashing children.

**Comparison:** start at root. Match → identical. Mismatch → recurse left then right. Sync only divergent buckets.

**Savings:** data synced proportional to *differences*, not total data. Real config: 1M buckets / 1B keys = 1000 keys per bucket.

---

### Key-Value Store — Write Path (Cassandra-Style)

**Principle:** Persistence comes from commit log + memtable + SSTable.

```
1. Write request persisted on commit log file (durability).
2. Data saved in memory cache (memtable).
3. When memtable is full/reaches threshold, flush to SSTable on disk.
```
SSTable = Sorted-String Table, a sorted list of `<key, value>` pairs.

---

### Key-Value Store — Read Path (Bloom Filter)

**Principle:** Memory cache first; on miss, use Bloom filter to find candidate SSTables.

```
1. Check memory cache. If hit -> return.
2. Check bloom filter.
3. Bloom filter identifies which SSTables might contain the key.
4. SSTables return data set.
5. Result returned to client.
```

---

### Key-Value Store — Summary Table

| Goal/Problem                | Technique                                                |
|-----------------------------|----------------------------------------------------------|
| Ability to store big data   | Consistent hashing to spread load                        |
| High availability reads     | Data replication; multi-data center setup                |
| Highly available writes     | Versioning & conflict resolution with vector clocks      |
| Dataset partition           | Consistent hashing                                       |
| Incremental scalability     | Consistent hashing                                       |
| Heterogeneity               | Consistent hashing                                       |
| Tunable consistency         | Quorum consensus                                         |
| Handling temporary failures | Sloppy quorum + hinted handoff                           |
| Handling permanent failures | Merkle tree                                              |
| Handling data center outage | Cross-data center replication                            |

*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Summary" (Ch. 6)*

---

### Unique ID Generator — Requirements

- IDs must be unique.
- Numerical values only.
- Fit into 64-bit.
- Ordered by date (but not necessarily +1 per record).
- Generate > 10,000 IDs/second.

---

### Unique ID — Approach 1: Multi-Master Replication

**Principle:** Use database `auto_increment` stepping by `k` (server count) instead of 1.

**Drawbacks:**
- Hard to scale across multiple data centers.
- IDs do not go up with time across servers.
- Doesn't scale well when servers are added/removed.

---

### Unique ID — Approach 2: UUID

**Principle:** 128-bit, generated independently per server, no coordination.

**Example:** `09c93e62-50b4-468d-bf8a-c07e1040bfb2`

**Pros:** simple, no sync issues, scales with web servers.
**Cons:** 128-bit (not 64-bit), not time-ordered, possibly non-numeric.

Probability of collision: "after generating 1 billion UUIDs every second for approximately 100 years would the probability of creating a single duplicate reach 50%".

---

### Unique ID — Approach 3: Ticket Server

**Principle:** Centralized `auto_increment` database (Flickr's approach).

**Pros:** numeric IDs, easy to implement, fine for small/medium scale.
**Cons:** single point of failure. Multiple ticket servers add data sync challenges.

---

### Unique ID — Approach 4: Twitter Snowflake (Chosen)

**Principle:** 64-bit ID split into sections; datacenter/machine fixed at startup, timestamp/sequence generated at runtime.

**Layout (Figure 7-5):**
```
| sign (1 bit) | timestamp (41 bits) | datacenter ID (5 bits) | machine ID (5 bits) | sequence (12 bits) |
```
- **Sign:** always 0 (reserved for future use).
- **Timestamp:** milliseconds since custom epoch (Twitter's default epoch = `1288834974657` = Nov 04, 2010, 01:42:54 UTC). Max value `2^41 - 1 = 2199023255551 ms ≈ 69 years`.
- **Datacenter ID:** `2^5 = 32` datacenters.
- **Machine ID:** `2^5 = 32` machines per datacenter.
- **Sequence:** `2^12 = 4096` IDs/ms/machine; resets every millisecond.

**Don't:** change datacenter/machine IDs after startup — accidental changes cause ID conflicts.

**Additional concerns:**
- **Clock synchronization:** NTP is the standard solution; multi-core and multi-machine both have skew.
- **Section length tuning:** fewer sequence bits + more timestamp bits for low-concurrency, long-lived apps.
- **High availability:** the ID generator is mission-critical.

---

### URL Shortener — Scope & Estimation

**Use cases:**
1. URL shortening: long URL → short URL.
2. URL redirecting: short URL → original.
3. High availability, scalability, fault tolerance.

**Back-of-envelope:**
```
Write:    100M URLs/day
Write QPS: 100M / 24 / 3600 = 1160
Read:    Assume 10:1 ratio -> 11,600 QPS
10-year records: 100M * 365 * 10 = 365 billion
Avg URL length: 100 bytes
10-year storage: 365 billion * 100 bytes = 365 TB
```

---

### URL Shortener — APIs

**Shorten:**
```
POST api/v1/data/shorten
  request parameter: {longUrl: longURLString}
  return shortURL
```

**Redirect:**
```
GET api/v1/shortUrl
  Return longURL for HTTP redirection
```

---

### URL Shortener — 301 vs 302 Redirect

**301 (Permanent):**
- Browser caches → subsequent requests skip the shortener.
- Reduces server load.
- Loses analytics (no further hits).

**302 (Temporary):**
- Always hits shortener first.
- Enables click-rate and source tracking.
- Higher server load.

**Heuristic:** use 301 for pure cost reduction; 302 if analytics matter.

---

### URL Shortener — Hash Value Length

**Character set:** `[0-9, a-z, A-Z]` = 62 chars.

```
| N | 62^N                                          |
|---|-----------------------------------------------|
| 6 | 62^6 = 56,800,235,584                         |
| 7 | 62^7 = 3,521,614,606,208 = ~3.5 trillion      |
```
365 billion URLs needs `n=7` (3.5T capacity).

---

### URL Shortener — Hash + Collision Resolution

**Principle:** Hash long URL with MD5/CRC32/SHA-1; take first 7 chars; rehash on collision.

```
CRC32: 5cb54054
MD5:   5a62509a84df9ee03fe1230b9df8b84e
SHA-1: 0eeae7916c06853901d9ccbefbfcaf4de57ed85b
```
Even CRC32 is too long → take first 7 chars → collisions.

**Resolution:** recursively append predefined string, rehash.

**Optimisation:** use Bloom filter (space-efficient probabilistic membership test) to avoid DB lookups for every collision check.

---

### URL Shortener — Base 62 Conversion (Chosen)

**Mapping:** `0-0,...,9-9, 10-a, 11-b,...,35-z, 36-A,...,61-Z` (so `a`=10, `Z`=61).

**Example — convert 11157 to base 62:**
```
11157 = 2 * 62^2 + 55 * 62^1 + 59 * 62^0
      = [2, 55, 59]
      -> [2, T, X]
Short URL: https://tinyurl.com/2TX
```

**Pros:** no collisions (ID is unique). **Cons:** predictable IDs = potential security concern.

---

### URL Shortener — Comparison

| Hash + collision resolution                                  | Base 62 conversion                                                       |
|--------------------------------------------------------------|--------------------------------------------------------------------------|
| Fixed short URL length                                       | Length grows with ID                                                     |
| No unique ID generator needed                                | Depends on a unique ID generator                                         |
| Collision possible, must resolve                             | Collision impossible                                                     |
| Cannot predict next short URL                                | Predictable next short URL (security risk)                               |

---

### URL Shortener — Shortening Flow (Figure 8-7)

```
1. longURL is the input.
2. Check if longURL is in the database.
3. If yes -> fetch existing shortURL, return.
4. If no -> generate new unique ID via unique ID generator.
5. Convert ID to shortURL via base 62.
6. Insert row (ID, shortURL, longURL) into DB.
```

**Example:**
```
longURL: https://en.wikipedia.org/wiki/Systems_design
ID:      2009215674938
shortURL: zn9edcu  (base 62 of ID)
```

---

### URL Shortener — Redirecting Flow

```
1. User clicks https://tinyurl.com/zn9edcu
2. Load balancer forwards to web servers.
3. Check cache for shortURL -> if hit, return longURL.
4. If miss, fetch longURL from DB. If not in DB, invalid shortURL.
5. Return longURL to user (with 301 or 302).
```
More reads than writes → cache the `<shortURL, longURL>` mapping.

---

### Web Crawler — Characteristics of a Good Crawler

- **Scalability:** billions of pages via parallelization.
- **Robustness:** handle bad HTML, unresponsive servers, crashes, malicious links, traps.
- **Politeness:** don't overwhelm hosts.
- **Extensibility:** minimal changes to support new content types.

**Back-of-envelope (1B pages/month):**
```
QPS:      1B / 30 / 24 / 3600 = ~400 pages/sec
Peak QPS: 2 * QPS = 800
Avg page size: 500 KB
Storage:  1B * 500 KB = 500 TB/month
5-year storage: 500 TB * 12 * 5 = 30 PB
```

---

### Web Crawler — High-Level Components

| Component          | Role                                                                |
|--------------------|---------------------------------------------------------------------|
| Seed URLs          | Starting points; chosen by locality or topic                        |
| URL Frontier       | FIFO queue of URLs to download                                      |
| HTML Downloader    | Fetches pages from the internet                                     |
| DNS Resolver       | Translates URL → IP                                                 |
| Content Parser     | Validates/parses HTML (separated from downloader)                   |
| Content Seen?      | Eliminates duplicates via hash (~29% of pages are duplicates)       |
| Content Storage    | Disk for bulk, memory for popular                                   |
| URL Extractor      | Parses links; converts relative → absolute                          |
| URL Filter         | Excludes blacklisted sites, error links, unwanted extensions        |
| URL Seen?          | Bloom filter / hash table to avoid re-crawl                         |
| URL Storage        | Stores visited URLs                                                 |

---

### Web Crawler — Workflow (Figure 9-4)

```
Step 1:  Add seed URLs to URL Frontier.
Step 2:  HTML Downloader fetches URLs from Frontier.
Step 3:  Downloader gets IP from DNS Resolver, starts downloading.
Step 4:  Content Parser parses HTML, checks malformed.
Step 5:  Pass parsed content to "Content Seen?".
Step 6:  If duplicate -> discard. Else pass to Link Extractor.
Step 7:  Link Extractor extracts links.
Step 8:  Filter links via URL Filter.
Step 9:  Pass filtered links to "URL Seen?".
Step 10: If seen -> nothing. Else ->
Step 11: Add to URL Frontier.
```

---

### Web Crawler — DFS vs BFS

**DFS:** rarely used — depth can be unbounded.

**BFS:** standard, implemented as FIFO queue. Two problems:
1. **Impoliteness:** most links from one page point to the same host (e.g. Wikipedia internal links) → flooding that host.
2. **No priority:** all URLs treated equally though quality/importance differs.

**Solution:** URL Frontier (front queues = priority, back queues = politeness).

---

### Web Crawler — URL Frontier: Politeness

**Principle:** Download one page per host at a time with a delay between downloads.

**Components (Figure 9-6):**
- **Queue router:** each back queue `b1..bn` holds URLs from a single host.
- **Mapping table:** host → queue.
```
| Host          | Queue |
| wikipedia.com | b1    |
| apple.com     | b2    |
| nike.com      | bn    |
```
- **FIFO queues `b1..bn`:** URLs from same host.
- **Queue selector:** each worker thread mapped to one FIFO queue.
- **Worker threads `1..N`:** download one page at a time, with delay.

---

### Web Crawler — URL Frontier: Priority

**Prioritizer:** takes URLs, computes priority (PageRank, traffic, update frequency).
- **Front queues `f1..fn`:** each with assigned priority; higher-priority queues selected with higher probability.
- **Queue selector:** random biased toward higher-priority queues.

**Combined URL Frontier:**
- Front queues manage prioritization.
- Back queues manage politeness.

---

### Web Crawler — Freshness & Storage

**Freshness:**
- Recrawl based on update history.
- Prioritize important pages for more frequent recrawl.

**Storage for URL Frontier (hybrid):**
- Majority of URLs on disk (durable, scalable).
- Buffers in memory for enqueue/dequeue (avoid disk bottleneck).
- Periodically flush buffer to disk.

---

### Web Crawler — Robots.txt & Performance

**Robots.txt:** standard for sites to communicate what crawlers may download. Cache results to avoid repeat downloads.

**Amazon example:**
```
User-agent: Googlebot
Disallow: /creatorhub/*
Disallow: /rss/people/*/reviews
Disallow: /gp/pdp/rss/*/reviews
Disallow: /gp/cdp/member-reviews/
Disallow: /gp/aw/cr/
```

**Performance optimisations:**
1. **Distributed crawl:** partition URL space across servers, each with multiple threads.
2. **Cache DNS Resolver:** DNS is synchronous (10–200 ms); keep DNS cache updated via cron.
3. **Locality:** place crawl servers geographically close to target hosts.
4. **Short timeout:** stop slow/non-responding hosts after predefined wait.

---

### Web Crawler — Robustness & Extensibility

**Robustness:**
- **Consistent hashing** to distribute load (Ch. 5).
- **Persist crawl state and data** so disrupted crawls can restart.
- **Exception handling** — don't crash on errors.
- **Data validation** — prevent system errors.

**Extensibility:** plug-in new modules — e.g. PNG Downloader for images, Web Monitor for copyright/trademark issues.

---

### Web Crawler — Spider Traps & Data Noise

**Spider traps:** pages causing infinite loops (e.g. `www.spidertrapexample.com/foo/bar/foo/bar/…`).
- Mitigation: maximal URL length.
- No automatic solution; manually verify and exclude or apply custom URL filters.

**Redundant content:** ~30% of web is duplicates → hashes/checksums.

**Data noise:** ads, code snippets, spam URLs — exclude when possible.

---

### Notification System — Channels

| Channel        | Provider examples                  |
|----------------|------------------------------------|
| iOS push       | Apple Push Notification Service (APNS) |
| Android push   | Firebase Cloud Messaging (FCM)     |
| SMS            | Twilio, Nexmo                      |
| Email          | Sendgrid, Mailchimp                |

**iOS push components:** Provider (sends request with device token + JSON payload) → APNS → iOS device.

**Daily volume example:** 10M mobile push + 1M SMS + 5M email.

---

### Notification System — Initial Design Flaws

Three problems with a single notification server:
- **Single point of failure (SPOF).**
- **Hard to scale** — DB, cache, and processing all coupled in one server.
- **Performance bottleneck** — HTML construction + third-party API waits, especially during peaks.

---

### Notification System — Improved Design

**Changes:**
- Move DB and cache out of the notification server.
- Add multiple notification servers with horizontal autoscaling.
- Introduce message queues (one per notification type to isolate failures).

**Flow:**
1. Service calls notification server API.
2. Server fetches user info, device token, notification setting from cache/DB.
3. Event sent to corresponding queue (e.g. iOS PN queue).
4. Workers pull from queue.
5. Workers send to third-party service.
6. Third-party delivers to user device.

---

### Notification System — Reliability

**No data loss:** notifications can be delayed or re-ordered but **never lost**.
- Persist notification data in DB (notification log DB).
- Implement retry mechanism.

**Exactly-once is impossible** in distributed systems → deduplicate using event ID:
```
When event arrives: check event ID. If seen -> discard. Else -> send.
```

---

### Notification System — Templates, Settings, Rate Limiting, Security, Monitoring

- **Templates:** pre-formatted; customizable parameters.
  ```
  BODY: You dreamed of it. We dared it. [ITEM NAME] is back — only until [DATE].
  CTA:  Order Now. Or, Save My [ITEM NAME]
  ```
- **Notification settings:** `user_id`, `channel`, `opt_in` — check before sending.
- **Rate limiting:** cap notifications/user to avoid opt-outs.
- **Retry mechanism:** on third-party failure, re-enqueue; alert devs if persistent.
- **Security:** `appKey` + `appSecret` authenticate push API callers.
- **Monitor queued notifications:** queue depth large → add workers.
- **Events tracking:** open rate, click rate, engagement via analytics service.

---

### News Feed — Two Flows

- **Feed publishing:** post → write to DB/cache → fanout to friends' feeds → notification.
- **News feed building:** aggregate friends' posts in reverse chronological order.

**APIs:**
```
POST /v1/me/feed   Params: content, auth_token
GET  /v1/me/feed   Params: auth_token
```

---

### News Feed — Fanout Models

| Model             | Pros                                                              | Cons                                                                  |
|-------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------|
| Fanout on write   | Real-time feed; fast reads (pre-computed)                         | Hotkey problem for popular users; wasted work for inactive users      |
| Fanout on read    | No wasted work for inactive; no hotkey problem                    | Slow reads                                                            |
| **Hybrid (chosen)** | Push for most; pull for celebrities/many-followers              | Implementation complexity; consistent hashing mitigates hotkeys       |

---

### News Feed — Fanout Service Steps

```
1. Fetch friend IDs from graph database.
2. Get friends info from user cache; filter by user settings (muted, selective sharing).
3. Send friends list + new post ID to message queue.
4. Fanout workers fetch from queue; store <post_id, user_id> in news feed cache.
5. News feed cache stores only IDs (configurable limit) to keep memory small.
```

**Cache table example:**
```
| post_id | user_id |
| post_id | user_id |
| ...     | ...     |
```

---

### News Feed — Retrieval Deep Dive

```
1. User requests /v1/me/feed.
2. Load balancer → web servers.
3. Web servers → news feed service.
4. Service fetches post IDs from news feed cache.
5. Service hydrates IDs from user cache + post cache (full objects).
6. Return JSON to client.
```
Media content served from CDN.

---

### News Feed — 5-Layer Cache Architecture

```
| Layer        | Stores                                                       |
|--------------|--------------------------------------------------------------|
| News Feed    | IDs of news feeds                                            |
| Content      | Every post data; popular in hot cache                        |
| Social Graph | User relationship data                                       |
| Action       | Like, reply, other actions                                   |
| Counters     | Like, reply, follower, following counts                      |
```
*Ref: System_Design_Interview_An_Insiders_Guide_2nd_Ed_-_Alex_Xu.md — "Cache architecture" (Ch. 11)*

---

### Chat System — Polling vs Long Polling vs WebSocket

| Technique     | Pros                                          | Cons                                                                         |
|---------------|-----------------------------------------------|------------------------------------------------------------------------------|
| Polling       | Simple                                        | Wasteful; server answers "no" most of the time                               |
| Long polling  | Holds connection until message or timeout     | Sender/receiver may hit different servers; can't detect disconnects; inefficient for inactive users |
| **WebSocket** | Bidirectional, persistent, ports 80/443 (firewall-friendly) | Server-side connection management critical                                  |

**WebSocket lifecycle:** starts as HTTP, upgraded via handshake → persistent bidirectional.

**Decision:** use WebSocket for both sending and receiving — simpler, more straightforward.

---

### Chat System — Service Categories

- **Stateless services:** login, signup, profile — behind load balancer, HTTP.
- **Stateful service:** chat service (persistent WebSocket per client).
- **Third-party integration:** push notification (Ch. 10).

**Single-server reality check:** 1M concurrent users × 10K memory each = ~10 GB → fits in one box. But single-server is a SPOF and a "red flag" — start there, then move on.

---

### Chat System — Storage Choices

**Generic data (profiles, settings, friends):** relational DB with replication + sharding.

**Chat history:** key-value store. Justifications:
- Easy horizontal scaling.
- Low latency.
- Relational DBs don't handle long tail of data well (large indexes → expensive random access).
- Proven at scale: Facebook Messenger uses HBase; Discord uses Cassandra.

**Read/write pattern:** 1:1 for 1-on-1 chat. Recent chats accessed frequently; old chats rarely.

---

### Chat System — Data Models

**1-on-1 message table:**
```
| message      |           |
| message_id   | bigint    |  <- primary key (decides sequence, NOT created_at)
| message_from | bigint    |
| message_to   | bigint    |
| content      | text      |
| created_at   | timestamp |
```

**Group message table:**
```
| group_message |           |
| channel_id    | bigint    |  <- partition key
| message_id    | bigint    |  <- composite primary key (channel_id, message_id)
| user_id       | bigint    |
| content       | text      |
| created_at    | timestamp |
```

**Message ID requirements:** unique + sortable by time. Options: global Snowflake (Ch. 7) or **local sequence number** (unique within a channel — easier to implement).

---

### Chat System — Service Discovery (ZooKeeper)

**Role:** recommend the best chat server based on geography and capacity.

**Flow (Figure 12-11):**
```
1. User A logs in.
2. Load balancer → API servers.
3. Backend authenticates -> service discovery picks best chat server (e.g. server 2).
4. User A connects to chat server 2 via WebSocket.
```

---

### Chat System — 1-on-1 Message Flow

```
1. User A sends message to Chat server 1.
2. Chat server 1 gets message ID from ID generator.
3. Chat server 1 sends message to message sync queue.
4. Message stored in key-value store.
5a. If User B online -> forward via Chat server 2 (WebSocket).
5b. If User B offline -> push notification from PN servers.
6. Chat server 2 forwards to User B.
```

---

### Chat System — Multi-Device Sync

Each device maintains `cur_max_message_id`. New messages satisfy:
- Recipient ID = logged-in user ID.
- Message ID in KV store > `cur_max_message_id`.

Each device syncs independently.

---

### Chat System — Small Group Chat Flow

**Inbox model:** sender's message copied to each recipient's message sync queue.

**Pros:**
- Simplifies sync (each client checks only its inbox).
- Inexpensive when group is small.

**WeChat uses this with a 500-member cap.** Larger groups need different strategies.

---

### Chat System — Online Presence

**User login:** WebSocket established → `{status: online, last_active_at: <ts>}` saved to KV store.

**User logout:** status → offline.

**Disconnections (flaky connections):** naive approach updates status on every disconnect/reconnect → poor UX (e.g. tunnel flicker). Use **heartbeat mechanism** instead.

**Heartbeat (Figure 12-18):**
- Client sends heartbeat every 5 seconds.
- If no heartbeat within `x` seconds (e.g. 30s), mark offline.

---

### Chat System — Presence Fanout

**Pub-sub model:** each friend pair maintains a channel. User A's status change publishes to channels A-B, A-C, A-D, which B/C/D subscribe to.

**Limitation:** WeChat caps this approach at 500 members. For 100K-member groups, fetching presence on demand (when entering group/refreshing) is more practical.

---

### Search Autocomplete — Scope & Estimation

**Requirements:**
- Fast response (< 100 ms or "stuttering").
- Relevant (by historical query frequency).
- Sorted by popularity.
- Scalable.
- Highly available.

**Assumptions:** 10M DAU, 10 searches/day, 20 bytes/query (4 words × 5 chars ASCII).

**QPS:**
```
10M users * 10 queries * 20 chars / 24 / 3600 = ~24,000 QPS
Peak QPS = ~48,000
New data/day: 10M * 10 * 20 B * 20% = 0.4 GB
```

---

### Search Autocomplete — Trie Data Structure

**Principle:** Tree-like structure; root = empty string; each node stores a character + 26 children.

**Augmented trie:** nodes also store frequency for ranking.

**Algorithm (top-k):**
```
p = length of prefix
n = total nodes
c = children of a given node

1. Find the prefix          -> O(p)
2. Traverse subtree         -> O(c)
3. Sort children, get top k -> O(c log c)
Total: O(p) + O(c) + O(c log c)
```

Too slow in the worst case — traverse the entire trie.

---

### Search Autocomplete — Trie Optimisations

**Optimisation 1 — Limit prefix length:**
- Users rarely type long queries → cap at ~50 chars.
- Reduces `O(p)` → `O(1)`.

**Optimisation 2 — Cache top-k at each node:**
- Each node stores top 5 (or 10) queries by frequency.
- Lookup reduces to `O(1)` + `O(1)` = `O(1)`.
- Trade-off: significantly more space. Worth it because response time is critical.

---

### Search Autocomplete — Redesigned Data Gathering Service

```
Analytics Logs -> Aggregators (weekly or real-time) -> Aggregated Data
   -> Workers (build trie) -> Trie DB (persisted) -> Trie Cache (snapshot)
```

**Aggregation frequency:**
- Real-time for Twitter-like use cases.
- Weekly for stable Google-like keywords.

---

### Search Autocomplete — Trie DB Storage Options

| Option            | Approach                                                              |
|-------------------|-----------------------------------------------------------------------|
| Document store    | Periodic snapshot, serialized, stored (MongoDB)                       |
| Key-value store   | Map each prefix → data; trie as hash table                            |

**Hash table mapping:** every prefix is a key; node data is the value.

---

### Search Autocomplete — Query Service Optimisations

```
1. Search query -> load balancer.
2. LB -> API servers.
3. API servers fetch trie data from Trie Cache, construct suggestions.
4. On cache miss -> replenish cache; subsequent requests hit cache.
```

**Speed:**
- **AJAX** requests — no full-page refresh.
- **Browser caching** — Google caches autocomplete 1 hour (`Cache-Control: private, max-age=3600`).
- **Data sampling** — log 1 in N requests to reduce processing.

---

### Search Autocomplete — Trie Operations

**Create:** workers build trie from aggregated data weekly.

**Update — two options:**
1. Replace the whole trie weekly.
2. Update individual node (slow) — updates must propagate to all ancestors up to root.

**Delete:** add filter layer in front of Trie Cache to remove unwanted (hateful/violent/explicit) suggestions immediately. Physical deletion from DB is asynchronous.

---

### Search Autocomplete — Scaling the Trie

**Naive sharding** by first letter: a-m → server 1, n-z → server 2. **Problem:** uneven (`c` has far more queries than `x`).

**Smarter sharding:** shard map manager uses historical distribution to balance — e.g. combine `u` through `z` into one shard if their combined volume matches `s` alone.

**Multi-level sharding:** `a` → `aa-ag`, `ah-an`, `ao-au`, `av-az`.

**Extensions:**
- Multi-language: store Unicode in trie nodes.
- Country-specific tries stored in CDNs.
- Real-time trending: streaming systems — Spark Streaming, Storm, Kafka.

---

### YouTube — Scope & Estimation

**Scope:** fast upload, smooth streaming, quality changes, low cost, high availability, multi-client.

**Estimation (5M DAU):**
```
Storage:    5M * 10% upload * 300 MB = 150 TB/day
CDN cost:   5M * 5 videos * 0.3 GB * $0.02 = $150,000/day
```
CDN cost dominates — covered in cost-saving deep dive.

---

### YouTube — Three-Component High-Level Design

```
Client  <->  CDN (video streaming)  +  API servers (everything else)
```

**Why leverage cloud (not build from scratch):**
- Building scalable blob storage or CDN is extremely complex/costly.
- Even Netflix (uses AWS) and Facebook (uses Akamai CDN) don't build everything themselves.

---

### YouTube — Video Uploading Flow (Two Parallel Processes)

**Flow A — upload the actual video:**
```
1. Videos uploaded to original storage (blob/S3).
2. Transcoding servers fetch and convert.
3. In parallel:
   3a. Transcoded videos -> transcoded storage -> CDN.
   3b. Completion events -> completion queue -> completion handler
        -> updates metadata DB and cache.
4. API servers inform client: video ready for streaming.
```

**Flow B — update metadata:**
- Client sends filename, size, format to API servers in parallel.
- API servers update metadata DB + cache.

---

### YouTube — Video Streaming Protocols

| Protocol                          | Notes                                  |
|-----------------------------------|----------------------------------------|
| MPEG-DASH                         | Dynamic Adaptive Streaming over HTTP   |
| Apple HLS                         | HTTP Live Streaming                    |
| Microsoft Smooth Streaming        | —                                       |
| Adobe HDS                         | HTTP Dynamic Streaming                 |

Choice of protocol dictates supported encodings and players. Streaming ≠ download — client receives streams continuously, starts playback immediately.

---

### YouTube — Video Transcoding (Container vs Codecs)

**Why transcode:**
- Raw video is huge (1 hr HD @ 60fps → hundreds of GB).
- Compatibility across devices/browsers.
- Adaptive bitrate for varying network conditions.

**Two parts of an encoding format:**
- **Container:** basket for video + audio + metadata. Identified by extension (`.avi`, `.mov`, `.mp4`).
- **Codecs:** compression/decompression. Common: H.264, VP9, HEVC.

---

### YouTube — DAG Model (Facebook SVE-Inspired)

**Principle:** Define tasks in stages via a Directed Acyclic Graph for sequential or parallel execution.

**Tasks (Figure 14-8):**
- Inspection: validate quality, malformed check.
- Video encodings: multiple resolutions/codecs/bitrates.
- Audio encoding.
- Thumbnail: user-uploaded or auto-generated.
- Watermark: identifying image overlay.

---

### YouTube — Video Transcoding Architecture

**Six components:**
1. **Preprocessor:** video splitting by GOP alignment, DAG generation, cache segments.
2. **DAG scheduler:** split DAG into task stages, enqueue.
3. **Resource manager:** task queue, worker queue, running queue, task scheduler.
4. **Task workers:** execute encoding tasks.
5. **Temporary storage:** memory for metadata, blob for video/audio.
6. **Encoded video:** final output (e.g. `funny_720p.mp4`).

**Resource manager flow:**
```
1. Task scheduler picks highest priority task from task queue.
2. Picks optimal worker from worker queue.
3. Instructs worker to run task.
4. Binds task/worker, puts in running queue.
5. Removes from running queue on completion.
```

---

### YouTube — Speed Optimisations

1. **Parallelize upload by GOP-aligned chunks** — resumable, fast.
2. **Place upload centers close to users** — use CDN as upload endpoints.
3. **Parallelism everywhere** — decouple pipeline stages with message queues:
   - Before queue: encoding waits for download output.
   - After queue: encoding consumes events independently → parallel.

---

### YouTube — Safety Optimisations

**Pre-signed upload URL:**
```
1. Client requests pre-signed URL from API servers (time-limited, scoped).
2. API server responds with pre-signed URL.
3. Client uploads video using pre-signed URL.
```
(Azure equivalent: Shared Access Signature.)

**Video protection options:**
- **DRM:** Apple FairPlay, Google Widevine, Microsoft PlayReady.
- **AES encryption:** decrypt on playback for authorized users.
- **Visual watermarking:** company logo/name overlay.

---

### YouTube — Cost-Saving Optimisations

**Observation:** YouTube video streams follow **long-tail distribution** — few popular videos accessed frequently, many have few/no viewers.

**Optimisations:**
1. Only serve most popular videos from CDN; others from high-capacity storage servers.
2. Encode less popular videos on-demand.
3. Store popular videos only in their relevant regions.
4. Build your own CDN (Netflix model) and partner with ISPs (Comcast, AT&T, Verizon).

**Always:** analyze historical viewing patterns before optimising.

---

### YouTube — Error Handling Playbook

| Component              | Failure handling                                                       |
|------------------------|------------------------------------------------------------------------|
| Upload                 | Retry a few times                                                      |
| Split video            | If old client can't split by GOP, pass whole video to server           |
| Transcoding            | Retry                                                                  |
| Preprocessor           | Regenerate DAG diagram                                                 |
| DAG scheduler          | Reschedule task                                                        |
| Resource manager queue | Use replica                                                            |
| Task worker            | Retry on new worker                                                    |
| API server             | Stateless; redirect to different server                                |
| Metadata cache         | Replicated; replace failed node                                        |
| Metadata DB (master)   | Promote slave to master                                                |
| Metadata DB (slave)    | Use another slave for reads; bring up replacement                      |

**Two error classes:** recoverable (retry) vs non-recoverable (stop, return error code).

---

### Google Drive — Scope & Estimation

**Features:** upload/download, sync across devices, revisions, sharing, notifications.
**Non-functional:** reliability (data loss unacceptable), fast sync, low bandwidth, scalability, high availability.

**Estimation (50M users, 10M DAU, 10 GB free):**
```
Total allocated: 50M * 10 GB = 500 PB
Upload QPS:      10M * 2 / 24 / 3600 = ~240
Peak QPS:        2 * 240 = 480
```

---

### Google Drive — APIs

**1. Upload (simple and resumable):**
```
https://api.example.com/files/upload?uploadType=resumable
Params: uploadType=resumable, data
```
Resumable upload steps:
1. Initial request → retrieve resumable URL.
2. Upload data, monitor state.
3. If disturbed, resume.

**2. Download:**
```
https://api.example.com/files/download
Params: path
{ "path": "/recipes/soup/best_soup.txt" }
```

**3. List revisions:**
```
https://api.example.com/files/list_revisions
Params: path, limit
{ "path": "/recipes/soup/best_soup.txt", "limit": 20 }
```
All APIs require auth + HTTPS.

---

### Google Drive — Sync Conflict Resolution

**Strategy:** first processed version wins; later version gets a conflict notification.

**Resolution UX:** system presents both copies (user 2's local + latest server). User 2 chooses to merge or override.

---

### Google Drive — Block Servers (Delta Sync + Compression)

**Principle:** Split files into blocks (~4 MB max, per Dropbox), compress per file type, encrypt, upload only modified blocks.

**Pipeline:**
```
1. Split file into blocks.
2. Compress each block (gzip/bzip2 for text; specific algos for media).
3. Encrypt each block.
4. Upload to cloud storage.
```

**Delta sync:** only modified blocks transferred (highlighted blocks `block 2` and `block 5` in Figure 15-12).

---

### Google Drive — High Consistency Requirement

**Principle:** A file must appear identical on all devices — strong consistency is mandatory.

**Achieve via:**
- Relational DB (native ACID).
- Cache replicas kept consistent with master.
- Invalidate caches on DB writes.

**Don't:** use NoSQL by default — ACID must be programmatically incorporated.

---

### Google Drive — Metadata DB Schema (Simplified)

| Table           | Purpose                                                        |
|-----------------|----------------------------------------------------------------|
| User            | Username, email, profile photo                                |
| Device          | Device info, `push_id` for notifications (1 user N devices)   |
| Namespace       | Root directory of a user                                       |
| File            | Latest file metadata                                           |
| File_Version    | Version history (existing rows read-only for integrity)       |
| Block           | Block metadata; reconstruct file by joining blocks in order   |

---

### Google Drive — Upload Flow (Parallel)

```
Add file metadata:
  1. Client 1 sends request to add metadata.
  2. Store metadata in DB; status -> "pending".
  3. Notify notification service.
  4. Notification service informs Client 2.

Upload file to cloud storage:
  2.1 Client 1 uploads to block servers.
  2.2 Block servers chunk, compress, encrypt, upload to S3.
  2.3 Cloud storage triggers callback on completion.
  2.4 Status -> "uploaded" in DB.
  2.5 Notify notification service.
  2.6 Notification service informs Client 2.
```

---

### Google Drive — Download Flow

```
1. Notification service informs Client 2 of change.
2. Client 2 requests metadata via API servers.
3. API servers fetch metadata from DB.
4. Metadata returned.
5. Client 2 gets metadata.
6. Client 2 requests blocks from block servers.
7. Block servers fetch from cloud storage.
8. Cloud storage returns blocks.
9. Client 2 downloads blocks, reconstructs file.
```

---

### Google Drive — Notification Service (Long Polling)

**Choice:** long polling (Dropbox), not WebSocket.

**Reasons:**
- Communication is one-directional (server → client); not bi-directional.
- Notifications are infrequent, no burst — WebSocket is overkill.

**Mechanism:** each client holds a long-poll connection. On change → close connection → client reconnects to metadata server to download changes → immediately re-establishes long poll.

---

### Google Drive — Save Storage Space

1. **De-duplicate blocks** by hash value (account-level).
2. **Intelligent backup strategy:**
   - Set a limit on version count; replace oldest when reached.
   - Weight recent versions more heavily (avoid 1000+ versions of heavily-edited docs).
3. **Move inactive data to cold storage** (e.g. Amazon S3 Glacier).

---

### Google Drive — Failure Handling Playbook

| Component                | Failure handling                                                              |
|--------------------------|-------------------------------------------------------------------------------|
| Load balancer            | Secondary becomes active via heartbeat                                        |
| Block server             | Other servers pick up pending jobs                                            |
| Cloud storage            | Cross-region replication; fetch from other region                             |
| API server               | Stateless; LB redirects traffic                                               |
| Metadata cache           | Replicated; replace failed node                                               |
| Metadata DB (master)     | Promote slave, bring up new slave                                             |
| Metadata DB (slave)      | Use another slave, bring up replacement                                       |
| Notification service     | Clients reconnect to new server (slow — many connections per machine)         |
| Offline backup queue     | Replicated; consumers re-subscribe to backup queue                            |

**Dropbox scale:** over 1 million connections per machine (2012 talk).

---

### Database Choices — Decision Heuristics

**Relational (RDBMS / SQL):** MySQL, PostgreSQL, Oracle. Tables/rows, joins, ACID. Default for structured data + transactions.

**NoSQL:** CouchDB, Neo4j, Cassandra, HBase, DynamoDB. Choose for super-low latency, unstructured data, JSON/XML serialization, massive data volume.

**NewSQL:** distributed SQL with horizontal scaling + ACID (mentioned indirectly via systems like Spanner, CockroachDB).

---

### Database Sharding — Heuristics

**Do:**
- Pick a sharding key that distributes data evenly.
- Combine with consistent hashing for elasticity (Ch. 5).

**Don't:**
- Don't choose a key with natural skew (celebrity user IDs in one shard).
- Don't assume joins will be easy — denormalize.
- Don't forget resharding is inevitable — plan for it.

---

### Replication Patterns

- **Master-slave:** writes to master, reads from slaves. Simple. Single master is a bottleneck & SPOF.
- **Multi-master:** multiple masters accept writes. Complex conflict resolution.
- **Circular:** chain of masters; subset of multi-master.
- **Synchronous vs asynchronous:** sync = strong consistency + latency; async = eventual + low latency (Netflix active-active).

---

### Cache Strategies — When to Use Each

| Strategy       | Use case                                                        |
|----------------|-----------------------------------------------------------------|
| Read-through   | Read-heavy, modify-rarely data (default in the book)            |
| Write-through  | Strong consistency requirements                                 |
| Write-behind   | Tolerate staleness for write throughput                         |
| Cache-aside    | Application explicitly manages cache population                 |

**Eviction policies:** LRU (most popular), LFU, FIFO.

---

### API Design — REST Conventions

**Principle:** REST-style endpoints; clear verbs and resources.

**Examples across chapters:**
```
POST /api/v1/data/shorten             (URL shortener)
GET  /api/v1/shortUrl                 (URL shortener redirect)
POST /v1/me/feed                      (news feed publish)
GET  /v1/me/feed                      (news feed retrieve)
POST https://api.example.com/v/sms/send  (notification system)
GET  /api/v1/users/12                 (single server example)
```

**Do:** use HTTPS, require auth tokens, return JSON, version APIs (`/v1/`).
**Don't:** expose unauthenticated internal APIs.

---

### Error Handling — Universal Patterns

**Recoverable errors:** retry N times; if persistent, classify as non-recoverable.

**Non-recoverable errors:** stop task, return proper error code.

**Per-tier patterns:**
- Stateless tier: redirect traffic.
- Stateful tier: reconnect to healthy server (chat), or promote slave (DB).
- Queue: replicate, re-subscribe consumers.
- Cache: replicate, replace node.
- Worker: re-enqueue task.

---

### Hotkey Problem — Multiple Manifestations

| Context                | Hotkey manifestation                              | Mitigation                                          |
|------------------------|---------------------------------------------------|-----------------------------------------------------|
| Sharded DB             | Celebrity user ID overloads one shard             | Dedicated shard per celebrity; sub-partition        |
| News feed fanout       | User with millions of followers slows fanout      | Hybrid fanout (pull for celebrities)                |
| Cache                  | Single key hammered                               | Consistent hashing + replicas                        |
| Consistent hashing     | Uneven partition sizes                            | Virtual nodes                                       |

---

### Monitoring — What to Track

- **System health:** QPS, peak QPS, latency (especially tail), error rate.
- **Queue depth:** large depth → add workers (notifications, fanout, completion).
- **Cache hit rate:** low → resize cache or revisit eviction policy.
- **Rate limiter effectiveness:** algorithm and rules.
- **Business metrics:** DAU, retention, revenue; notification open/click rates.

---

### Evolvability & Extensibility

**Principle:** Plug-in architecture for new content types / providers.

**Examples:**
- Web crawler: PNG Downloader module, Web Monitor module.
- Notification system: pluggable third-party services (FCM unavailable in China → JPush, PushY).
- YouTube: DAG stages customizable per content creator.
- Search autocomplete: filter layer for unwanted suggestions (independent of trie).

---

### Reference Architectures (Ch. 16 Reading List)

Real-world references cited for further study:
- Facebook: Timeline (denormalization), Erlang chat, Haystack photo storage, Scaling Memcache, TAO social graph.
- Amazon: Dynamo key-value store.
- Netflix: 360-degree stack, A/B testing, recommendations, Open Connect.
- Google: File System, Differential Synchronization (Docs), Bigtable, YouTube.
- Instagram: 14M users, terabytes of photos.
- Twitter: scaling to 150M active users, 10000% faster.

**Heuristic:** study both shared principles and specific technologies; understand what problem each technology solves.

---

## Anti-Patterns & Common Mistakes

- **Jimmy syndrome (jumping to solution):** answering fast without understanding requirements → *fix:* ask 4–6 clarifying questions first.
- **Vertical scaling as strategy:** bounded + SPOF → *fix:* plan horizontal scaling from day one.
- **Stateful web tier:** sticky sessions complicate autoscaling → *fix:* externalize session state to shared store.
- **Single notification server:** SPOF + hard to scale + performance bottleneck → *fix:* multiple servers + message queues + cache + DB.
- **`hash(key) % N`:** near-total redistribution on resize → *fix:* consistent hashing with virtual nodes.
- **Sticky sessions for distributed rate limiting:** neither scalable nor flexible → *fix:* centralized Redis.
- **Locks for rate-limit race conditions:** significantly slow → *fix:* Lua scripts or Redis sorted sets.
- **Fixed-window counter alone:** allows 2x traffic at boundaries → *fix:* sliding window counter (smooth, ~0.003% error).
- **Hashing URL with MD5 + first 7 chars without collision handling:** collisions certain → *fix:* recursion with predefined string or base 62 conversion.
- **301 redirect for analytics-heavy products:** browser caches → loses click data → *fix:* 302 for analytics, 301 for cost.
- **Storing full objects in news feed cache:** memory blow-up → *fix:* store IDs only, hydrate from per-object caches.
- **Fanout on write for celebrities:** hotkey problem → *fix:* hybrid (pull for celebrities).
- **Storing whole file on each edit:** bandwidth waste → *fix:* block servers with delta sync.
- **Encrypting on client side:** client easily hacked → *fix:* centralize encryption in block servers.
- **Serving all videos from CDN:** cost explodes for long-tail content → *fix:* popular on CDN, long-tail from storage servers.
- **Updating presence on every disconnect/reconnect:** tunnel flicker causes UX churn → *fix:* heartbeat with grace period.
- **Inbox model for huge groups:** 100K members × 1 message = 100K copies → *fix:* fetch presence on demand; or use write-amplification-aware design.
- **Per-character first-letter sharding for trie:** uneven distribution (`c` >> `x`) → *fix:* shard map manager using historical distribution.
- **Assuming exactly-once delivery in notifications:** impossible in distributed systems → *fix:* dedupe via event ID.
- **Trusting a single source for failure detection:** false positives → *fix:* gossip protocol requiring independent confirmations.
- **Designing without considering the next scale curve:** 1M → 10M → 100M changes architecture → *fix:* discuss explicitly in wrap-up.

---

## Decision Heuristics / Checklists

### Interview Execution Checklist
- [ ] Asked 4–6 clarifying questions before designing.
- [ ] Wrote assumptions on the board.
- [ ] Drew box diagram with clients, APIs, web servers, data stores, cache, CDN, message queue.
- [ ] Did back-of-envelope (QPS, storage, bandwidth).
- [ ] Walked through 1–2 concrete use cases.
- [ ] Identified prioritised components for deep dive with interviewer.
- [ ] Surfaced trade-offs at every decision.
- [ ] Closed with bottleneck analysis + next scale curve.

### Scaling Checklist (Per Tier)
- [ ] Web tier is stateless; autoscaling configured.
- [ ] Data tier has replication (master-slave or quorum).
- [ ] Cache tier is replicated across DCs (no SPOF).
- [ ] Static assets in CDN with sensible TTL + invalidation plan.
- [ ] Message queues decouple producers/consumers.
- [ ] Logging centralized; metrics (host + aggregated + business) collected.
- [ ] CI/CD automated.

### CAP Decision
- **CP** (banks, billing, config): block writes during partition.
- **AP** (social, chat history, news feed): accept stale reads, converge eventually.
- **CA** is not a real distributed-system option.

### Communication Protocol Choice
| Need                                  | Pick                       |
|---------------------------------------|----------------------------|
| Sender (client-initiated)             | HTTP with keep-alive       |
| Receiver (server-initiated, periodic) | Long polling               |
| Bidirectional real-time (chat)        | WebSocket                  |
| One-directional infrequent (Drive)    | Long polling               |

### Rate-Limiting Algorithm Choice
| Workload                          | Algorithm                |
|-----------------------------------|--------------------------|
| Bursty (API, marketing)           | Token bucket             |
| Stable outflow required           | Leaky bucket             |
| Strict accuracy                   | Sliding window log       |
| Memory-constrained + smooth       | Sliding window counter   |
| Simple counter, low precision     | Fixed window             |

### ID Generator Choice
| Need                                | Pick                       |
|-------------------------------------|----------------------------|
| 64-bit, sortable, distributed       | Twitter Snowflake          |
| 128-bit, no coordination            | UUID                       |
| Small/medium scale, numeric         | Ticket server              |
| Multi-DB, time-ordered acceptable   | Multi-master replication   |

### Cache Layer Choice (News Feed Pattern)
1. **IDs/handles layer** (news feed) — small, hot.
2. **Content layer** — post data, hot cache for popular.
3. **Social graph layer** — relationships.
4. **Action layer** — likes, replies.
5. **Counter layer** — aggregated counts.

### CDN Cost Optimisation Checklist
- [ ] Only popular content on CDN.
- [ ] Long-tail content on high-capacity storage servers.
- [ ] Encode less popular videos on-demand.
- [ ] Region-scoped distribution for regionally popular content.
- [ ] At very large scale: own CDN + ISP partnerships.

### Failure Handling Pattern (Per Component)
- **Stateless (API server):** redirect via LB.
- **Stateful (chat server):** service discovery provides replacement; clients reconnect.
- **Master DB:** promote slave, spin up new slave.
- **Slave DB:** use another slave, replace.
- **Cache:** replicated; replace node.
- **Queue:** replicated; consumers re-subscribe.
- **Worker:** re-enqueue task on new worker.
- **Cloud storage:** cross-region replication.

---

## Key Takeaways

1. **Follow the 4-step framework religiously:** understand → high-level → deep dive → wrap up. The structure itself is the signal.
2. **Every design is a trade-off:** strong consistency vs. availability, push vs. pull, 301 vs. 302, CDN cost vs. latency. Always articulate.
3. **The same handful of primitives recur:** load balancers, multi-layer caches, CDNs, message queues, consistent hashing, sharding, replication, quorum, key-value stores. Master when to use each.
4. **Estimation is a skill:** round aggressively, label units, state assumptions, practice QPS/storage/bandwidth/cache/server-count.
5. **Communication is as important as depth:** ask, narrate, suggest multiple approaches, bounce ideas off the interviewer.
6. **Stateless services scale horizontally; stateful services need special care:** externalize sessions, use WebSocket for real-time, ZooKeeper for service discovery.
7. **Data-layer decisions matter most:** SQL vs NoSQL, strong vs eventual, replication topology, sharding key — these shape everything above.
8. **Design for failure at every tier:** replication, retries, failover, graceful degradation are non-negotiable at scale.
9. **Optimise based on real usage patterns:** CDN for popular only, delta sync for files, GOP-aligned chunking for video, browser caching for autocomplete.
10. **Leverage managed cloud infrastructure:** building blob storage / CDN / message queues from scratch is impractical for most companies.
11. **Quorum formula `W + R > N` is the lever for tunable consistency:** W=1/R=N fast read; W=N/R=1 fast write; W=R=2, N=3 balanced strong.
12. **Snowflake's bit allocation is the canonical distributed ID design:** sign(1) + timestamp(41) + datacenter(5) + machine(5) + sequence(12).
13. **Vector clocks are how Dynamo detects sibling conflicts:** `[server, version]` pairs; ancestor rule + sibling rule.
14. **Merkle trees make anti-entropy cheap:** compare root hashes; only divergent buckets sync.
15. **Trie + cached top-k per node = `O(1)` autocomplete:** trade space for time; response time is critical.
16. **DAG pipelines (Facebook SVE) make video transcoding flexible and parallel:** preprocessor → DAG scheduler → resource manager → task workers.
17. **Block servers + delta sync = bandwidth-efficient file sync:** 4 MB blocks (Dropbox), compress, encrypt, deduplicate.
18. **Long polling beats WebSocket when communication is one-directional and infrequent** (Google Drive notifications).
19. **Hybrid fanout (push for most, pull for celebrities) avoids hotkey meltdowns** in news feed systems.
20. **Spider traps have no automatic fix:** set URL length limits + manual verification; everything else (deduplication, politeness, freshness) is automatable.

---

## Cross-References
- Related: `[[../best_practices/Foundations_of_Scalable_Systems.md]]` — deeper building-block treatment of the same primitives.
- Related: `[[../best_practices/Designing_Distributed_Systems.md]]` — patterns for distributed system composition.
- Related: `[[../best_practices/Building_Microservices.md]]` — service decomposition beyond what this book covers.
- Related: `[[../best_practices/Cloud_Application_Architecture_Patterns.md]]` — cloud-native patterns referenced implicitly via S3/CDN/Queue choices.
- Related: `[[../best_practices/Software_Architecture_Patterns.md]]` — architectural pattern catalogue.
- Topic index: `[[../INDEX.md]]`
