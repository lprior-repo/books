# System Design Interview: An Insider's Guide (2nd Edition) -- Comprehensive Summary

**Author:** Alex Xu

---

## Overview

This book provides a structured, repeatable framework for tackling system design interview questions. It covers foundational concepts in distributed systems and then walks through detailed designs for twelve classic system design problems. Each chapter follows a consistent four-step process: (1) understand the problem and establish design scope, (2) propose a high-level design and get buy-in, (3) design deep dive, and (4) wrap up. The book emphasizes trade-offs, communication with the interviewer, and the reality that no design is perfect -- every choice involves balancing competing concerns.

---

## Chapter 1: Scale from Zero to Millions of Users

This foundational chapter traces the evolutionary path of a system from a single server to an architecture serving millions of users. It introduces nearly every major building block of distributed systems.

**Single server setup.** Everything begins with one machine running the web app, database, and cache. Users resolve the domain via DNS, obtain an IP address, and send HTTP requests directly to the server. Traffic arrives from web applications (server-side + client-side rendering) and mobile applications (HTTP/JSON APIs).

**Database separation.** As the user base grows, the database is moved to its own server. The chapter explains the relational vs. NoSQL database decision: relational databases (MySQL, PostgreSQL) for structured data with relationships; NoSQL databases (Cassandra, DynamoDB, MongoDB) for unstructured data, super-low latency, or massive scale. NoSQL is divided into key-value stores, graph stores, column stores, and document stores.

**Vertical vs. horizontal scaling.** Vertical scaling (adding CPU/RAM) has hard limits and no failover. Horizontal scaling (adding servers) is essential for large-scale systems. A load balancer is introduced to distribute traffic across multiple web servers using private IPs for security and public IPs only on the load balancer itself.

**Database replication.** Master-slave replication is described: one master handles writes, multiple slaves handle reads. Benefits include better performance (parallel reads), reliability (data survives disasters), and high availability. Failover scenarios are discussed: if a slave dies, reads redirect to the master; if the master dies, a slave is promoted.

**Cache tier.** A cache (e.g., Memcached, Redis) stores frequently accessed data in memory. The read-through cache strategy is explained: check cache first, then database, then populate cache. Key considerations include: deciding what to cache (read-frequently, write-rarely data), expiration policies, consistency between cache and database, mitigating single points of failure, and eviction policies (LRU, LFU, FIFO).

**Content Delivery Network (CDN).** CDNs deliver static content (images, CSS, JS, video) from geographically distributed edge servers. The workflow involves the CDN checking its cache, fetching from the origin on miss, and caching with a TTL. Considerations include cost, appropriate cache expiry, CDN fallback, and cache invalidation via API calls or URL versioning.

**Stateless web tier.** Moving session data out of web servers into a shared data store (NoSQL is recommended) enables horizontal scaling and auto-scaling. Stateful architectures require sticky sessions, which complicate scaling.

**Multiple data centers.** GeoDNS routes users to the nearest data center. Challenges include traffic redirection, cross-data-center data synchronization, and consistent testing/deployment. Netflix's active-active multi-regional architecture is referenced.

**Message queues.** Message queues decouple producers and consumers, enabling independent scaling and failure resilience. The pattern is illustrated with a photo-processing use case where web servers publish jobs and workers consume them asynchronously.

**Logging, metrics, and automation.** At scale, centralized logging, host-level and business-level metrics, and CI/CD automation become essential.

**Database scaling.** Vertical scaling (bigger machines) is contrasted with horizontal scaling (sharding). Sharding distributes data across servers using a sharding key. Challenges include resharding, the celebrity/hotspot key problem, and the difficulty of joins across shards (solved by denormalization).

**Key summary principles:** keep web tier stateless, build redundancy at every tier, cache aggressively, support multiple data centers, host static assets in CDN, scale the data tier by sharding, split tiers into microservices, and invest in monitoring and automation.

---

## Chapter 2: Back-of-the-Envelope Estimation

This chapter teaches the skill of quickly estimating system capacity and performance requirements during an interview.

**Power of two.** A table of data volume units is provided: KB (2^10), MB (2^20), GB (2^30), TB (2^40), PB (2^50).

**Latency numbers every programmer should know.** Based on Jeff Dean's famous numbers: L1 cache reference (0.5 ns), L2 cache reference (7 ns), main memory reference (100 ns), disk seek (10 ms), round trip within a datacenter (0.5 ms), packet from CA to Netherlands and back (150 ms). Key conclusions: memory is fast, disk is slow, compress data before sending over the network, and data centers in different regions add significant latency.

**Availability numbers.** SLAs are measured in "nines." 99% availability means 3.65 days of downtime per year; 99.9999% means 31.56 seconds. Cloud providers typically target 99.9% or higher.

**Example estimation: Twitter.** Given 300M MAU, 50% DAU, 2 tweets/day, 10% with media, 5-year retention: QPS is approximately 3,500, peak QPS about 7,000, and 5-year media storage is roughly 55 PB.

**Tips:** Round and approximate (precision is not expected), write down assumptions, label units explicitly, and practice common estimation types (QPS, peak QPS, storage, cache, number of servers).

---

## Chapter 3: A Framework for System Design Interviews

This chapter provides the meta-framework used throughout the rest of the book.

**Step 1: Understand the problem and establish design scope (3-10 minutes).** Do not jump to solutions. Ask clarifying questions: what features to build, how many users, anticipated scale, technology stack, existing services to leverage. The chapter illustrates this with a sample news feed conversation.

**Step 2: Propose high-level design and get buy-in (10-15 minutes).** Draw a blueprint with key components (clients, APIs, web servers, data stores, cache, CDN, message queues). Do back-of-the-envelope calculations. Walk through concrete use cases. Collaborate with the interviewer as a teammate.

**Step 3: Design deep dive (10-25 minutes).** Identify and prioritize components with the interviewer. Focus on the most interesting areas (e.g., hash functions for URL shorteners, latency for chat systems). Avoid getting lost in irrelevant details. Time management is critical.

**Step 4: Wrap up (3-5 minutes).** Identify bottlenecks and propose improvements. Recap the design. Discuss error cases, operation issues (monitoring, deployment), and how to handle the next scale curve.

**Dos and Don'ts.** Do: ask for clarification, communicate your thinking, suggest multiple approaches, bounce ideas off the interviewer. Don't: jump in without understanding requirements, go into excessive detail too early, think in silence, or give up.

---

## Chapter 4: Design a Rate Limiter

A rate limiter controls the rate of traffic sent by a client or service. Benefits include preventing DoS attacks, reducing cost (especially for paid third-party APIs), and preventing server overload.

**Where to place the rate limiter.** Client-side is unreliable (easily forged). Server-side or as API gateway middleware are the practical options. The choice depends on technology stack, algorithm needs, existing infrastructure, and engineering resources.

**Five rate limiting algorithms are covered in detail:**

1. **Token bucket:** A bucket holds tokens that refill at a fixed rate. Each request consumes one token. Pros: simple, memory efficient, allows bursts. Cons: tuning bucket size and refill rate is challenging. Used by Amazon and Stripe.

2. **Leaking bucket:** Requests enter a FIFO queue and are processed at a fixed rate. Pros: stable outflow rate. Cons: burst traffic fills the queue with old requests, blocking recent ones. Used by Shopify.

3. **Fixed window counter:** Divides time into fixed windows with a counter per window. Pros: simple. Cons: allows up to 2x the limit at window boundaries.

4. **Sliding window log:** Stores timestamps of all requests and removes outdated ones. Pros: very accurate. Cons: high memory usage.

5. **Sliding window counter:** Hybrid of fixed window and sliding log. Uses weighted count from the previous window. Pros: smooths spikes, memory efficient. Cons: approximate, not perfectly strict (though Cloudflare found only 0.003% error across 400M requests).

**High-level architecture.** Uses Redis (INCR + EXPIRE commands) as an in-memory counter store. Rules are stored in configuration files and cached by workers.

**Distributed environment challenges:** Race conditions (solved with Lua scripts or Redis sorted sets) and synchronization across multiple rate limiter instances (solved with centralized Redis rather than sticky sessions).

**Performance optimization:** Multi-data center setup with edge servers, eventual consistency for data synchronization.

**Monitoring:** Track effectiveness of rate limiting algorithms and rules. Adjust based on data (e.g., switch to token bucket for burst-heavy traffic).

**HTTP headers for rate limiting:** X-Ratelimit-Remaining, X-Ratelimit-Limit, X-Ratelimit-Retry-After, and HTTP 429 status code for throttled requests.

---

## Chapter 5: Design Consistent Hashing

**The problem.** Traditional hashing (`hash(key) % N`) redistributes nearly all keys when a server is added or removed, causing a storm of cache misses.

**Consistent hashing** maps both servers and keys onto a hash ring (using SHA-1, range 0 to 2^160 - 1). To locate a key, walk clockwise from the key's position until a server is found. When servers are added or removed, only a fraction of keys are remapped.

**Two issues with the basic approach:** (1) Partitions on the ring may be unequal in size, causing uneven load. (2) Key distribution may be non-uniform.

**Virtual nodes (replicas).** Each real server is represented by multiple virtual nodes on the ring. With 100-200 virtual nodes, the standard deviation of load is 5-10%. More virtual nodes means more balanced distribution at the cost of more metadata storage.

**Finding affected keys:** When a server is added, the affected range is from the new node anticlockwise to the previous server. When removed, the range is from the removed node anticlockwise to the previous server.

**Real-world usage:** Amazon Dynamo, Apache Cassandra, Discord, Akamai CDN, Google Maglev load balancer.

---

## Chapter 6: Design a Key-Value Store

The chapter designs a distributed key-value store supporting `put(key, value)` and `get(key)`, targeting small values (<10KB), big data, high availability, high scalability, tunable consistency, and low latency.

**CAP theorem.** A distributed system can provide at most two of: Consistency, Availability, Partition Tolerance. Since network partitions are unavoidable, the real choice is between CP (block writes during partition) and AP (accept writes, accept stale reads). CA systems cannot exist in practice.

**System components (based on Dynamo, Cassandra, BigTable):**

- **Data partition:** Consistent hashing distributes data evenly and minimizes movement when nodes change. Supports automatic scaling and heterogeneous server capacities (more virtual nodes for bigger servers).

- **Data replication:** Data is replicated to N servers by walking clockwise from the key's position on the ring. Replicas are placed in distinct data centers for reliability.

- **Consistency (Quorum consensus):** N = number of replicas, W = write quorum, R = read quorum. If W + R > N, strong consistency is guaranteed (at least one overlapping node has the latest data). Configuration examples: W=1, R=N for fast reads; W=N, R=1 for fast writes; N=3, W=R=2 for balanced strong consistency.

- **Consistency models:** Strong consistency (blocks until all replicas agree), weak consistency (may return stale data), eventual consistency (all replicas converge given enough time). Dynamo and Cassandra use eventual consistency.

- **Inconsistency resolution via versioning and vector clocks.** Each data modification creates a new immutable version. A vector clock is a list of [server, version] pairs. It detects whether one version is an ancestor of another (no conflict) or a sibling (conflict requiring reconciliation). Downsides: complexity pushed to clients, and vector clock pairs can grow large (mitigated by pruning oldest entries).

- **Failure detection:** Gossip protocol -- each node maintains a membership list with heartbeat counters, periodically sends heartbeats to random nodes, and marks nodes as down when heartbeats stop increasing.

- **Handling temporary failures:** Sloppy quorum and hinted handoff -- route requests to the next healthy servers, and push data back when the failed server recovers.

- **Handling permanent failures:** Anti-entropy protocol using Merkle trees. Each leaf node is a hash of a bucket's keys; parent nodes are hashes of children. Comparing root hashes allows efficient detection of inconsistent buckets, minimizing data transfer.

- **Write path:** Data is written to a commit log (for durability) and a memory cache (memtable). When the memtable is full, it is flushed to an SSTable on disk.

- **Read path:** Check memory cache first. If missed, check a Bloom filter to determine which SSTables might contain the key, then read from those SSTables.

---

## Chapter 7: Design a Unique ID Generator in Distributed Systems

Requirements: unique, sortable by time, 64-bit, numeric, capable of 10,000+ IDs per second.

**Four approaches evaluated:**

1. **Multi-master replication:** Auto-increment by k (number of servers) instead of 1. Drawbacks: hard to scale across data centers, IDs not time-ordered across servers, difficult to add/remove servers.

2. **UUID:** 128-bit, generated independently per server. Pros: simple, no coordination. Cons: 128-bit (not 64-bit), not sortable by time, non-numeric.

3. **Ticket server:** A single centralized auto-increment database. Pros: numeric, easy to implement. Cons: single point of failure.

4. **Twitter Snowflake (chosen):** A 64-bit ID divided into: 1 bit sign (always 0), 41 bits timestamp (milliseconds since custom epoch, ~69 years of lifetime), 5 bits datacenter ID (32 datacenters), 5 bits machine ID (32 machines per datacenter), 12 bits sequence number (4096 IDs per millisecond per machine). Datacenter and machine IDs are assigned at startup; timestamp and sequence are generated at runtime.

**Additional considerations:** Clock synchronization across servers (NTP), tuning section lengths for different concurrency/longevity trade-offs, and ensuring high availability since the ID generator is mission-critical.

---

## Chapter 8: Design a URL Shortener

Two primary use cases: URL shortening (long URL to short URL) and URL redirecting (short URL back to long URL).

**Back-of-the-envelope estimation:** 100M URLs/day, 10:1 read-to-write ratio, 365 billion records over 10 years, 365 TB storage.

**API design:** POST /api/v1/data/shorten (with longUrl parameter) returns shortUrl. GET /api/v1/{shortUrl} returns longUrl for redirection.

**301 vs 302 redirect.** 301 (permanent) is cached by the browser, reducing server load but losing analytics. 302 (temporary) always hits the shortener service first, enabling click tracking.

**Hash function design.** The hashValue uses [0-9, a-z, A-Z] = 62 characters. With length 7, 62^7 = ~3.5 trillion combinations (sufficient for 365 billion URLs).

**Two approaches:**

1. **Hash + collision resolution:** Use MD5/CRC32/SHA-1, take the first 7 characters, and resolve collisions by appending a predefined string and rehashing. Bloom filters can optimize collision checks.

2. **Base 62 conversion (chosen):** Convert a unique numeric ID to base 62 representation. No collisions possible since IDs are unique. The trade-off is that IDs are predictable (potential security concern).

**URL shortening flow:** Input longUrl -> check if exists in DB -> if new, generate unique ID -> base 62 encode to shortUrl -> store (id, shortUrl, longUrl).

**URL redirecting flow:** User clicks shortUrl -> load balancer -> web server -> check cache -> if miss, check DB -> return longUrl for redirect.

---

## Chapter 9: Design a Web Crawler

A web crawler systematically browses the web to collect content for search engine indexing, web archiving, data mining, and copyright monitoring.

**Characteristics of a good crawler:** Scalability (billions of pages via parallelization), robustness (handle bad HTML, unresponsive servers, traps), politeness (do not overwhelm hosts), and extensibility (plug in new content types).

**Key components in the high-level design:**

- **Seed URLs:** Starting points for crawling, selected by locality or topic.
- **URL Frontier:** A FIFO queue storing URLs to be downloaded.
- **HTML Downloader:** Fetches web pages from the internet.
- **DNS Resolver:** Translates URLs to IP addresses.
- **Content Parser:** Validates and parses HTML (separated from the downloader to avoid slowing the crawl).
- **Content Seen?:** Eliminates duplicate content by comparing hash values of pages (~29% of web pages are duplicates).
- **URL Extractor:** Parses links from HTML pages, converting relative paths to absolute URLs.
- **URL Filter:** Excludes blacklisted sites, error links, and unwanted file extensions.
- **URL Seen?:** Bloom filter or hash table to avoid re-crawling.
- **Content Storage and URL Storage:** Disk for bulk data, memory for popular content.

**Deep dive topics:**

- **DFS vs BFS:** BFS is preferred. Standard BFS has two problems: most links point to the same host (impolite), and all URLs have equal priority. The URL frontier solves both.

- **URL Frontier design:** Front queues manage prioritization (by PageRank, traffic, update frequency). Back queues manage politeness (one queue per host, one worker thread per queue, delay between downloads).

- **Freshness:** Recrawl based on update history and URL priority. Not all pages need the same recrawl frequency.

- **Storage for URL Frontier:** Hybrid approach -- most URLs on disk, buffers in memory for enqueue/dequeue operations, periodically flushed to disk.

- **Robots.txt:** Must be checked before crawling any site. Results are cached to avoid repeated downloads.

- **Performance optimizations:** Distributed crawl (partition URL space across servers), cached DNS resolver (avoid synchronous DNS bottlenecks), geographical locality (place servers near target hosts), short timeouts.

- **Robustness:** Consistent hashing for load distribution, persistent crawl state, exception handling, data validation.

- **Spider traps:** Infinite URL structures. Mitigated by URL length limits and manual identification. No fully automatic solution exists.

---

## Chapter 10: Design a Notification System

Supports three notification types: mobile push (APNS for iOS, FCM for Android), SMS (Twilio, Nexmo), and email (Sendgrid, Mailchimp).

**Contact info gathering:** Device tokens, phone numbers, and emails are collected at signup/install and stored in user and device tables.

**Initial design problems:** Single point of failure (one notification server), hard to scale, performance bottleneck during peak hours.

**Improved design:** Separate database and cache from notification servers, add multiple notification servers with horizontal scaling, introduce message queues (one per notification type to isolate failures). Workers pull events from queues and send to third-party services.

**Deep dive considerations:**

- **Reliability:** Notifications must never be lost. Persist notification data in a log database and implement retry mechanisms. Exact-once delivery is impossible in distributed systems; deduplication using event IDs reduces duplicates.

- **Notification templates:** Pre-formatted templates with customizable parameters ensure consistency, reduce errors, and save time.

- **Notification settings:** Users can opt out of specific notification types. Settings are checked before every send.

- **Rate limiting:** Prevent overwhelming users with too many notifications.

- **Security:** AppKey and AppSecret authenticate push notification API callers.

- **Monitoring:** Track queue depth (add workers if backlog grows) and event metrics (open rate, click rate, engagement).

---

## Chapter 11: Design a News Feed System

The news feed system supports two flows: feed publishing (creating a post) and news feed retrieval (viewing the feed).

**APIs:** POST /v1/me/feed (publish), GET /v1/me/feed (retrieve).

**Feed publishing flow:** User -> load balancer -> web servers -> post service (persist to DB/cache) -> fanout service (push to friends' feeds) -> notification service.

**Fanout strategies:**

- **Fanout on write (push model):** Pre-compute feeds at write time. Fast reads, but slow for users with many friends (hotkey problem), and wasteful for inactive users.

- **Fanout on read (pull model):** Compute feeds on demand at read time. Efficient for inactive users, no hotkey problem, but slow reads.

- **Hybrid approach (chosen):** Push for most users; pull for celebrities/users with many followers. Consistent hashing mitigates hotkey issues.

**Fanout service details:** Fetch friend IDs from graph database -> filter based on user settings (muted friends, selective sharing) -> send to message queue -> fanout workers store (post_id, user_id) pairs in news feed cache. Only IDs are cached (not full objects) to conserve memory.

**News feed retrieval:** Fetch post IDs from news feed cache -> hydrate with full user and post data from user cache and post cache -> return JSON to client. Media content served from CDN.

**Cache architecture (5 layers):** News Feed (IDs), Content (post data, hot cache for popular), Social Graph (relationships), Action (likes, replies), Counters (like count, follower count).

---

## Chapter 12: Design a Chat System

Supports one-on-one chat, small group chat (max 100), online presence, multiple device support, and push notifications. Scale: 50M DAU.

**Communication protocols:**

- **Polling:** Client periodically asks for new messages. Wasteful.
- **Long polling:** Client holds connection open until messages arrive or timeout. Drawbacks: sender/receiver may hit different servers, no good way to detect disconnection, inefficient for inactive users.
- **WebSocket (chosen):** Bidirectional, persistent, initiated as HTTP then upgraded. Works through firewalls (ports 80/443). Used for both sending and receiving, simplifying the design.

**System architecture:** Stateless services (login, signup, profile) behind load balancers using HTTP. Stateful chat service (persistent WebSocket connections). Third-party integration for push notifications.

**Storage:** Generic data (user profiles, settings) in relational databases. Chat history in key-value stores (HBase for Facebook Messenger, Cassandra for Discord) because: easy horizontal scaling, low latency, good for the long tail of data, and 1:1 read/write ratio.

**Data models:** Message table for 1-on-1 chat (message_id as primary key). Group message table with composite key (channel_id, message_id). Message IDs must be unique and sortable by time (Snowflake or local sequence generators).

**Service discovery:** ZooKeeper recommends the best chat server based on geography and capacity. Clients connect to the recommended server via WebSocket.

**Message flows:**

- **1-on-1:** Sender -> chat server -> ID generator -> message sync queue -> key-value store. If receiver is online, forward via their chat server's WebSocket. If offline, send push notification.
- **Multi-device sync:** Each device maintains cur_max_message_id. New messages have IDs greater than this value. Each device syncs independently.
- **Group chat:** Sender's message is copied to each recipient's message sync queue (inbox model). Good for small groups; WeChat uses this with a 500-member cap.

**Online presence:** Presence servers manage status via WebSocket. Login sets online + last_active_at. Logout sets offline. Heartbeat mechanism (client sends heartbeat every 5 seconds; if no heartbeat for 30 seconds, mark offline) handles flaky connections gracefully. Presence fanout uses pub-sub channels per friend pair. For large groups, presence is fetched on demand rather than pushed.

---

## Chapter 13: Design a Search Autocomplete System

Returns the top 5 most frequently searched queries as a user types. Requirements: <100ms response time, relevance by popularity, scalable, highly available.

**Estimation:** 10M DAU, 10 searches/day, 20 characters per query, ~24,000 QPS, ~48,000 peak QPS, 0.4 GB new data per day.

**High-level design:** Data gathering service (aggregates query frequencies) + Query service (returns top results for a prefix).

**Trie data structure (the core optimization):**

- Basic trie stores characters in nodes. To support ranking, each node also stores frequency information.
- Naive algorithm: find prefix node O(p), traverse subtree O(c), sort and get top k O(c log c). This is too slow.
- **Optimization 1:** Limit prefix length (users rarely type long queries; cap at ~50 characters, making prefix lookup O(1)).
- **Optimization 2:** Cache top k queries at every node. This reduces total lookup to O(1) but increases space. The trade-off is worthwhile because response time is critical.

**Data gathering service (redesigned):** Analytics logs -> Aggregators (batch process weekly or real-time depending on use case) -> Aggregated data -> Workers (build trie) -> Trie DB (persisted) -> Trie Cache (distributed cache with snapshot of DB).

**Trie DB storage options:** Document store (serialize and snapshot the trie) or key-value store (map each prefix to its data).

**Query service (optimized):** Client -> load balancer -> API servers -> Trie Cache. Browser caching (1-hour TTL) and AJAX requests further reduce latency. Data sampling (log 1 in N requests) reduces processing overhead.

**Trie operations:** Created weekly by workers from aggregated data. Updated either by full replacement (weekly) or individual node updates (slow, requires updating all ancestors). Deletion uses a filter layer in front of the cache to remove unwanted suggestions immediately; physical deletion from DB happens asynchronously.

**Scaling the trie:** Sharding by first letter is naive (uneven -- 'c' has far more queries than 'x'). A shard map manager uses historical data distribution to create balanced shards (e.g., combining 'u' through 'z' into one shard if their combined volume matches 's' alone). Multi-level sharding extends this for further subdivision.

**Extensions:** Multi-language support (Unicode in trie nodes), country-specific tries stored in CDNs, real-time trending queries (streaming data processing with Apache Spark/Kafka/Storm).

---

## Chapter 14: Design YouTube

Design a video streaming service supporting fast uploads, smooth streaming, quality changes, low cost, high availability, and multiple clients.

**Back-of-the-envelope:** 5M DAU, 5 videos/day per user, 300MB average video size, 150 TB daily storage, ~$150,000/day CDN cost. CDN cost is the dominant expense.

**High-level architecture (three components):** Client, CDN (video streaming), API servers (everything else).

**Video uploading flow (two parallel processes):**

- **Flow A (upload video):** Client uploads to original storage (blob storage like S3). Transcoding servers fetch and convert to multiple formats/resolutions. Transcoded videos go to transcoded storage, then CDN. Completion events go to a message queue, pulled by completion handlers that update metadata DB and cache.

- **Flow B (update metadata):** Client sends metadata (filename, size, format) to API servers, which update the metadata DB and cache.

**Video streaming:** Videos stream from CDN. Streaming protocols (MPEG-DASH, Apple HLS, Microsoft Smooth Streaming, Adobe HDS) control data transfer. The protocol choice determines supported encodings and players.

**Video transcoding deep dive:** Raw video is too large and format-limited. Transcoding produces multiple bitrates and formats for compatibility, quality adaptation, and bandwidth optimization. Containers (.mp4, .mov) hold video, audio, and metadata. Codecs (H.264, VP9, HEVC) handle compression.

**DAG (Directed Acyclic Graph) model:** Inspired by Facebook's SVE, a DAG defines processing stages (inspection, video encoding, audio encoding, thumbnail generation, watermarking) that can execute sequentially or in parallel.

**Video transcoding architecture:** Preprocessor (split video by GOP, generate DAG, cache segments) -> DAG scheduler (split DAG into task stages, enqueue) -> Resource manager (task queue, worker queue, running queue, task scheduler) -> Task workers (execute encoding tasks) -> Temporary storage -> Encoded video output.

**System optimizations:**

- **Speed:** Parallelize video upload by splitting into GOP-aligned chunks. Place upload centers (CDN as upload endpoints) near users. Introduce message queues to decouple pipeline stages and enable parallelism.
- **Safety:** Pre-signed upload URLs (time-limited, scoped access). DRM (FairPlay, Widevine, PlayReady), AES encryption, visual watermarking to protect content.
- **Cost-saving:** Only serve popular videos from CDN; serve long-tail content from high-capacity storage servers. Encode less popular videos on-demand. Store popular videos only in relevant regions. For very large scale, build your own CDN and partner with ISPs (Netflix model).

**Error handling:** A comprehensive playbook covers recoverable errors (retry) and non-recoverable errors (stop and report) for every component: upload, split, transcode, preprocessor, DAG scheduler, resource manager, task workers, API servers, cache, and database.

---

## Chapter 15: Design Google Drive

A file storage and synchronization service supporting upload, download, sync across devices, file revisions, sharing, and notifications. Scale: 50M users, 10M DAU, 10 GB free per user.

**Evolution from single server:** Start with Apache + MySQL + local storage. Shard by user_id as data grows. Move file storage to Amazon S3 with cross-region replication for durability. Add load balancers, scale web servers horizontally, replicate and shard the metadata database.

**APIs:** Upload (simple and resumable), download, list revisions. All require authentication and HTTPS.

**Sync conflicts:** First processed version wins; later version receives a conflict notification and is presented with both copies for manual resolution.

**High-level design components:**

- **Block servers:** Split files into blocks (~4MB max, following Dropbox), compress, encrypt, and upload to cloud storage. Enable **delta sync** (only modified blocks are transferred) and **compression** (file-type-specific algorithms). This saves significant bandwidth.
- **Cloud storage (S3):** Stores file blocks.
- **Cold storage (S3 Glacier):** For infrequently accessed data.
- **API servers:** Handle everything except file upload (authentication, profiles, metadata).
- **Metadata database:** Stores user, device, namespace, file, file_version, and block metadata. Files are stored in S3; the DB holds only metadata.
- **Metadata cache:** Cached metadata for fast retrieval.
- **Notification service:** Uses long polling (not WebSocket) because communication is one-directional (server to client) and infrequent. Notifies clients of file changes made on other devices.
- **Offline backup queue:** Stores changes for offline clients; syncs when they reconnect.

**High consistency requirement:** Strong consistency is mandatory (a file must appear the same on all devices). Achieved by: using relational databases (native ACID support), keeping cache replicas consistent with the master, and invalidating caches on database writes.

**Database schema:** User, Device (with push_id), Namespace, File, File_Version (read-only for revision integrity), Block tables.

**Upload flow (parallel):** (1) Add file metadata to DB (status: pending), notify notification service. (2) Upload file to block servers -> split, compress, encrypt -> upload blocks to S3 -> callback updates status to "uploaded" -> notify notification service -> notify other clients.

**Download flow:** Notification service informs client -> client fetches metadata via API servers -> client requests blocks from block servers -> block servers fetch from S3 -> client downloads and reconstructs the file.

**Storage space optimization:** De-duplicate blocks by hash value. Limit version count (weight recent versions more heavily). Move inactive data to cold storage.

**Failure handling:** Detailed playbook for each component: load balancer (failover via heartbeat), block server (other servers pick up jobs), cloud storage (cross-region replication), API server (stateless, redirect traffic), metadata cache (replicated, replace failed node), metadata DB (promote slave if master fails), notification service (clients reconnect to new server, slow process due to many connections), offline backup queue (replicated, re-subscribe).

---

## Chapter 16: The Learning Continues

This short chapter provides a curated collection of real-world architecture references from major companies (Facebook, Amazon, Netflix, Google, YouTube, Instagram, Twitter, Uber, Pinterest, LinkedIn, Dropbox, WhatsApp) and a list of engineering blogs for continued learning. The author emphasizes studying both the shared principles and the specific technologies these companies use.

---

## Key Takeaways

1. **Follow the four-step framework religiously:** Understand the problem, propose high-level design, deep dive on priority areas, and wrap up with bottleneck analysis. This structure signals methodical thinking to interviewers.

2. **Every design involves trade-offs:** There is no perfect system. Strong consistency sacrifices availability. Caching improves reads but introduces staleness. Push models are fast for reads but expensive for writes with many followers. Always articulate the trade-offs you are making.

3. **Core building blocks appear repeatedly:** Load balancers, caches (multi-layer), CDNs, message queues, consistent hashing, database sharding/replication, key-value stores, and microservices are the fundamental primitives. Mastering how and when to apply each one is essential.

4. **Estimation is a skill, not a talent:** Practice back-of-the-envelope calculations for QPS, storage, bandwidth, and CDN cost. Round aggressively, label units, and state assumptions clearly.

5. **Communication is as important as technical depth:** Ask clarifying questions before designing. Think out loud. Treat the interviewer as a teammate. Do not dive into details before establishing the high-level architecture.

6. **Stateless services scale horizontally; stateful services require special care:** Move session data out of web servers. Use WebSocket for real-time communication. Use service discovery (ZooKeeper) for stateful server assignment.

7. **Data layer decisions matter most:** Choose between SQL and NoSQL based on data structure and access patterns. Choose between strong and eventual consistency based on business requirements. Use quorum consensus for tunable consistency in distributed stores.

8. **Failure is inevitable -- design for it:** Every component needs a failure handling strategy. Replication, retries, failover, and graceful degradation are non-negotiable at scale.

9. **Optimize based on actual usage patterns:** CDN for popular content only, delta sync for file storage, browser caching for autocomplete, GOP-aligned chunking for video. Understanding how users actually interact with your system drives the most impactful optimizations.

10. **Leverage existing cloud infrastructure:** Building blob storage, CDNs, and message queues from scratch is impractical for most companies. Know what managed services exist (S3, CloudFront, SQS, DynamoDB) and when to use them versus building custom solutions.

11. **The best preparation is practice:** Work through each chapter's design problem multiple times. Study real-world architectures from engineering blogs. The goal is not to memorize solutions but to internalize the decision-making process so you can adapt to novel problems.
