# Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services

**By Brendan Burns (O'Reilly, 2018)**

A comprehensive summary of the key patterns, concepts, and practices for building reliable distributed systems using containers and container orchestration.

---

## Introduction and Motivation

Brendan Burns, a cofounder of the Kubernetes project and distinguished engineer at Microsoft Azure, wrote this book to address a fundamental problem: distributed system development has historically been a "black art" practiced by specialists. Each system was built from scratch with unique architectures, despite sharing many common problems and solutions. The rise of containers and container orchestrators changed this landscape by providing a universal object and interface for expressing distributed system patterns -- much as object-oriented programming did for software design in the 1990s.

The book draws a direct analogy to three prior transformations in software development:

1. **Donald Knuth's "The Art of Computer Programming" (1962)** formalized algorithms as reusable, language-agnostic concepts that programmers could learn and apply across contexts.
2. **The "Gang of Four" Design Patterns book (1994)** provided a shared vocabulary and interface-based patterns for object-oriented programming, enabling generic reusable libraries.
3. **The open source movement** demonstrated that software development, particularly distributed systems development, is fundamentally a community endeavor.

The value of establishing distributed systems patterns is threefold:

- **Standing on the shoulders of giants**: Learning from others' mistakes without having to make them yourself. Rather than relying on a colleague's anecdotal experience, you can turn to proven patterns.
- **A shared language**: Without common vocabulary, teams waste time in "violent agreement" -- arguing about the same concept known by different names. The term "sidecar container" eliminated the need to redefine the concept every time it came up.
- **Shared components for easy reuse**: Identifying patterns enables building reusable container images with HTTP-based interfaces that work across programming languages. Shared code gets more usage, more testing, and higher quality.

---

## Part I: Single-Node Patterns

Before addressing multi-node distributed systems, the book establishes patterns for groups of containers co-located on a single machine. These patterns assume all containers can be reliably co-scheduled, share filesystems, network namespaces, and shared memory. In Kubernetes, this tight grouping is called a *pod*.

The motivations for splitting a single-node application into multiple containers include:

- **Resource isolation**: A user-facing application server and a background configuration loader have different resource priorities. Separate containers allow different resource limits and ensure the background task cannot starve the user-facing service.
- **Team scaling**: The ideal team size is six to eight people. Small, focused container modules enable small teams to own distinct pieces, and reusable modules can serve many teams.
- **Separation of concerns**: Small, focused containers are easier to understand, test, update, and deploy independently, leading to more reliable rollouts and rollbacks.

---

### Chapter 2: The Sidecar Pattern

The sidecar pattern consists of two containers: the **application container** containing core logic, and the **sidecar container** that augments and improves the application container, often without the application's knowledge. Both are co-scheduled onto the same machine and share filesystem, hostname, network, and other namespaces.

**Adding HTTPS to a Legacy Service**: A legacy web service only served unencrypted HTTP, and the source code could no longer be rebuilt. Using the sidecar pattern, an nginx container was deployed alongside the legacy application in the same network namespace. The nginx sidecar terminates HTTPS on the external IP and proxies unencrypted traffic to the legacy service on localhost. The network security team is satisfied because unencrypted traffic only traverses the loopback adapter.

**Dynamic Configuration**: Many legacy applications read configuration from files on disk, but cloud-native environments benefit from API-driven dynamic configuration. A configuration manager sidecar shares a filesystem directory with the application, periodically polls a configuration API, downloads changes to the shared filesystem, and signals the application to reload (via SIGHUP, file-watching, or in extreme cases SIGKILL to trigger a restart).

**Modular Application Containers**: Rather than requiring every developer to implement monitoring endpoints in every language, a `topz` sidecar container sharing the PID namespace can introspect all running processes and provide a consistent web interface. The orchestration system can automatically inject this container into all deployments.

**Building a Simple PaaS**: A Git-synchronization sidecar polls a repository every few seconds, while a Node.js application server (using nodemon) auto-reloads when files change. Together they form a minimal platform-as-a-service where pushing code to Git automatically deploys it.

**Designing Sidecars for Modularity**: Three critical practices for reusable sidecars:
1. **Parameterize containers**: Treat containers like functions with parameters (e.g., `PROXY_PORT`, `CERTIFICATE_PATH`). Pass parameters via environment variables.
2. **Define the container's API**: Every interaction -- environment variables, HTTP endpoints, configuration formats -- is part of the API. Subtle changes (e.g., changing time units from seconds to milliseconds) can be breaking changes.
3. **Document your containers**: Use `EXPOSE` directives with comments, `ENV` for default parameter values, and `LABEL` directives following the Label Schema project conventions for metadata.

---

### Chapter 3: Ambassadors

The ambassador pattern brokers interactions between the application container and the rest of the world. While the sidecar augments the application, the ambassador acts as a proxy that the application communicates with as if it were the external service.

**Sharding with an Ambassador**: When a storage layer becomes too large for one machine, data must be split (sharded) across multiple machines. Rather than retrofitting sharding logic into existing application code, an ambassador container receives all requests on localhost, routes each to the appropriate shard, and returns results. The application only sees what appears to be a single storage backend. The book demonstrates this with a sharded Redis deployment using Kubernetes StatefulSets (for stable DNS names) and twemproxy (Twitter's lightweight Redis/memcached proxy) configured with ketama consistent hashing.

**Service Brokering**: When rendering an application portable across environments (public cloud, private cloud, physical datacenter), service discovery becomes a challenge. MySQL might be SaaS in the cloud but self-hosted on-premises. An ambassador container introspects the environment, discovers the correct service, and brokers the connection. The application always connects to localhost.

**Request Splitting for Experimentation**: An ambassador can split traffic between production and experimental services. Using nginx with IP hashing and weighted upstream servers (e.g., `weight=9` for production, unweighted for experiment), roughly 10% of traffic routes to the experimental version while IP hashing ensures individual users have a consistent experience.

---

### Chapter 4: Adapters

The adapter pattern modifies the interface of an application container to conform to a predefined interface expected by the infrastructure. Real-world applications are heterogeneous -- written in different languages with different conventions for logging, monitoring, and health checking. The adapter pattern homogenizes this diversity.

**Monitoring**: Different applications expose metrics in different formats (syslog, JMX, custom endpoints). An adapter container transforms the application's native monitoring interface into a standard format. The book demonstrates using the Prometheus `redis_exporter` adapter alongside a Redis container, enabling Prometheus to monitor Redis through its standard metrics API without modifying Redis itself.

**Logging**: Applications log in different formats and to different destinations (files, stdout, custom protocols). A Fluentd adapter container normalizes log output -- for example, using the `fluent-plugin-redis-slowlog` plugin to capture Redis slow queries as time-series logs, or monitoring Apache Storm metrics via REST API and converting them to queryable log streams.

**Health Monitoring**: For off-the-shelf databases where you cannot modify the container, an adapter container implements rich health checks. The book shows a Go-based adapter that connects to MySQL, executes a representative query, and exposes the result as an HTTP health endpoint. This adapter is reusable across any MySQL deployment.

The key insight: even when you *could* modify the application container, decoupling the adapter enables sharing and reuse. A MySQL health-checking adapter developed by one team benefits everyone, and people can use it without deep knowledge of MySQL health-checking procedures.

---

## Part II: Serving Patterns (Multi-Node Distributed Patterns)

This section introduces microservices as the architectural foundation: systems built from many components running in different processes communicating over defined APIs, contrasted with monolithic systems. Benefits of microservices include reliability (small, focused services), agility (independent team release schedules), and independent scaling. Drawbacks include debugging complexity and architectural difficulty. Well-known patterns help address these challenges.

---

### Chapter 5: Replicated Load-Balanced Services

The simplest distributed pattern: every server is identical, all can handle any request, and a load balancer distributes traffic among them.

**Stateless Services**: Stateless services require no saved state to operate correctly. Individual requests can be routed to any replica. Replication provides both redundancy and scale. Even a "never-crashing" service with daily deployments cannot achieve 99.9% availability with a single instance -- you would need to deploy in under 3.6 seconds per hour. Two replicas behind a load balancer solve this trivially.

**Readiness Probes**: Health probes determine when a container needs restarting. Readiness probes determine when a container is ready to serve requests. Many applications need initialization time (connecting to databases, loading plugins, downloading files) before they are ready. A dedicated readiness URL informs the load balancer to stop sending traffic until initialization completes.

**Session Tracked Services**: Some applications need all requests from a particular user to reach the same replica (for in-memory caching or long-lived state). Session tracking is typically implemented via consistent hashing of source/destination IP addresses. Note that IP-based tracking works for internal cluster traffic but not for external traffic due to NAT; for external sessions, application-level tracking via cookies is needed.

**Caching Layer**: When stateless application code is expensive (database queries, rendering, data mixing), a caching web proxy (e.g., Varnish) between users and the application can dramatically improve performance. The book recommends deploying the cache as a separate replicated tier rather than as sidecars alongside each web server. With sidecars, you scale cache at the same rate as web servers, storing the same data redundantly and reducing hit rate. A separate tier of a few large-cache replicas (e.g., two replicas with 5 GB each instead of ten with 1 GB each) maximizes unique data stored and improves hit rate.

**Expanding the Caching Layer**: Beyond caching, the reverse proxy tier can provide rate limiting and denial-of-service defense. Best practice: small rate limits for anonymous access, higher limits requiring authentication. Return 429 status codes with `X-RateLimit-Remaining` headers.

**SSL Termination**: A third replicated layer of nginx servers handles HTTPS termination, forwarding unencrypted traffic to the Varnish cache. Different certificates should be used for edge termination and internal services, with each internal service having its own certificate for independent rollout capability.

The complete pattern forms three tiers: nginx (SSL termination) -> Varnish (caching/rate-limiting) -> Application servers, each as independently scalable replicated services connected by load balancers.

---

### Chapter 6: Sharded Services

In contrast to replicated services where every replica is identical and can serve every request, sharded services split data so each replica (shard) only serves a subset of requests. A root node examines each request and distributes it to the appropriate shard. Sharded services are used when the data is too large for a single machine.

**Sharded Caching**: The book provides a detailed design of a sharded cache system. With a replicated cache of 10 replicas (10 GB each) and 200 GB of total data, each replica stores the same 5% of data. With a 10-way sharded cache, each shard stores unique data, achieving 50% coverage -- a tenfold improvement in memory utilization.

**Cache Criticality**: The hit rate (percentage of requests served from cache) determines overall system capacity. A 50% hit rate doubles your effective RPS. But this means the cache becomes critical infrastructure: if it fails, the backend is overwhelmed. You must rate-limit your service to account for potential cache degradation.

Cache also improves latency. If a cached response takes 10ms versus 100ms from the backend, a 25% hit rate reduces average latency to 77.5ms. However, load testing both with and without cache is recommended.

**Replicated, Sharded Caches**: For systems dependent on cache, each shard can itself be a replicated service. This adds complexity but provides resilience: individual cache shard failures do not cause user-visible degradation, and cache rollouts can happen during peak traffic.

**Sharding Functions**: The sharding function maps requests to shards, typically using `shard = hash(request_key) % number_of_shards`. Two critical properties:
- **Determinism**: Same input always maps to the same shard.
- **Uniformity**: Load is evenly distributed across shards.

**Selecting a Key**: The shard key determines sharding quality. Hashing the entire HTTP request object (including timestamp and IP) means identical content requests map to different shards -- the function is too specific. Hashing only the path may group requests with different responses (e.g., different languages for different regions) -- the function is too general. A well-chosen key (e.g., `country(request.ip), request.path`) balances specificity and generality.

**Consistent Hashing**: When resizing from N to N+1 shards, standard modulo hashing remaps most keys. Consistent hashing guarantees only K/N keys are remapped when resizing to N shards. Moving from 10 to 11 shards remaps less than 10% of keys, versus potentially losing the entire cache with standard hashing.

**Hot Sharding**: When organic traffic patterns create uneven shard load (e.g., a viral photo), replicated shards can be independently scaled. With autoscaling, hot shards grow to handle increased load while cold shards shrink.

---

### Chapter 7: Scatter/Gather

The scatter/gather pattern achieves parallelism for time-intensive computations. A root node simultaneously farms requests to all leaf replicas, each processes a portion, and the root combines partial results into a complete response.

**Scatter/Gather with Root Distribution**: The simplest form uses homogeneous leaves. If a request takes 60 seconds on one core, distributing across 30 machines reduces latency to approximately 2 seconds. Unlike multi-threading on a single machine, scatter/gather avoids memory, network, and disk bandwidth bottlenecks by spreading across machines.

**Scatter/Gather with Leaf Sharding**: When data exceeds a single machine's capacity, each leaf holds a different data shard. All leaves process the query against their shard, and the root combines results. For a document search: leaves return matching documents from their shard, and the root produces the union of all matches.

**Choosing the Right Number of Leaves**: Two critical constraints limit parallelism:
1. **Overhead**: Each leaf request has constant overhead (HTTP parsing, network latency). As leaf count grows, overhead eventually dominates compute time.
2. **The Straggler Problem**: Overall latency equals the slowest leaf response. If individual requests have a 99th-percentile latency of 2 seconds, scattering to 5 leaves means the 99th-percentile becomes the 95th-percentile for the system (0.99^5 = 0.95). Scattering to 100 leaves virtually guarantees every request hits the 2-second tail.

The same problem applies to availability: if each leaf has a 1% failure rate, scattering to 100 leaves guarantees failure.

**Scaling Scatter/Gather**: Replicate each shard so that leaf requests are load-balanced across healthy replicas. This provides fault tolerance and enables safe upgrades under load.

---

### Chapter 8: Functions and Event-Driven Processing

Function-as-a-Service (FaaS) / serverless computing provides ephemeral, event-driven computation. Burns distinguishes FaaS from serverless: FaaS is event-driven and may run on owned infrastructure (not truly serverless), while serverless computing (e.g., container-as-a-service) may not be event-driven.

**When FaaS Makes Sense**: Benefits include zero deployment friction (deploy source code directly), automatic scaling, and forced modularity. Challenges include forced decoupling making debugging difficult, risk of infinite function loops, and the need for rigorous monitoring.

**Limitations**:
- **Background processing**: FaaS is inherently event-based with time-bounded execution, making it poor for long-running background tasks.
- **Data in memory**: Services requiring large in-memory datasets (e.g., search indices) suffer latency spikes when cold-starting.
- **Cost at scale**: Per-request pricing becomes uneconomical compared to VMs once request volume is high enough to keep processors continuously active.

**The Decorator Pattern**: FaaS is ideal for stateless request/response transformations. Example: adding default values to JSON API inputs. A Python function checks for missing fields and populates defaults before forwarding to the API. This is lighter-weight than an adapter container because it scales independently.

**Handling Events**: Events (asynchronous, single-instance occurrences like user signups) are ideal for FaaS. Example: two-factor authentication. When a user logs in, the main server fires an asynchronous webhook to a FaaS that generates a random code, registers it with the login service, and sends it via SMS using Twilio. The main login flow is not blocked.

**Event-Based Pipelines**: Directed graphs of connected functions where each node is a FaaS and edges are HTTP calls. Example: a user signup pipeline where the main service maintains lists of required and optional webhook actions, calling each FaaS handler. Each handler is a few lines of focused code, and the pipeline is easy to extend without modifying the core service.

---

### Chapter 9: Ownership Election

Many systems need a notion of *ownership* where exactly one replica is the designated master for a particular task. Distributed ownership is both the most complicated and most important part of reliable distributed system design.

**Do You Need Master Election?**: A singleton service in a container orchestrator already has pretty good uptime: container crashes trigger restarts in seconds, and machine failures trigger rescheduling in minutes. For daily deployments taking 2 minutes, a singleton achieves roughly two nines of availability. For many background processing tasks, this simplicity is worth the reliability trade-off.

**Master Election via Distributed Key-Value Stores**: Rather than implementing consensus algorithms (Paxos, RAFT) from scratch, use existing distributed stores (etcd, ZooKeeper, Consul) that provide two primitives:
1. **Compare-and-swap**: Atomically write a new value only if the current value matches the expected value.
2. **Time-to-live (TTL)**: Keys automatically expire after a duration.

**Implementing Locks**: A lock is acquired via `compareAndSwap(lockName, "1", "0")`. If the lock does not exist, try `compareAndSwap(lockName, "1", nil)`. To block until acquired, loop with either polling or watching for changes. The lock is released by setting the value back to "0".

**TTL for Safety**: Without TTL, a process that dies while holding a lock creates a permanent deadlock. With TTL, the lock automatically expires. However, TTL introduces a subtle bug: if Process-1 holds the lock, its TTL expires, Process-2 acquires the lock, then Process-1 finishes and calls unlock -- it has now unlocked Process-2's lock. The solution is to use the key-value store's *resource version*: store the version when locking, and verify the version when unlocking.

**Renewable Locks for Ownership**: For long-lived ownership (e.g., an active scheduler), implement a renewable lock that periodically renews its TTL. A background thread renews every TTL/2 seconds, and if renewal fails, the application terminates all activity requiring the lock.

**Concurrent Data Manipulation**: Even with perfect locking, brief periods of dual ownership can occur (e.g., an overloaded processor pauses, TTL expires, another replica grabs the lock). Defenses include:
1. Double-checking the lock before guarded operations.
2. Workers validating that request senders are still the current master by checking the lock server.
3. Using resource versions in requests to detect stale messages from previous ownership epochs.

The book provides a detailed scenario where Request R1 is sent, delayed by network, the sender loses and regains ownership, and R1 finally arrives -- accepted because the sender is again master, but incorrect because a different request (R2) was already processed under different ownership. Resource versions in requests solve this by detecting that R1 was sent under a previous ownership epoch.

---

## Part III: Batch Computational Patterns

Batch processes run for a limited time to process large amounts of data using parallelism. Examples include telemetry aggregation, sales reporting, and video transcoding.

---

### Chapter 10: Work Queue Systems

The simplest batch pattern: each work item is independent, workers process items in parallel, and the goal is completing all work within a time constraint.

**A Generic Work Queue System**: The work queue demonstrates the power of container patterns. Most work queue logic is independent of the actual work, enabling reusable "library containers" that define two interfaces:

1. **Source Container Interface** (ambassador pattern): Provides the stream of work items via HTTP REST API (`GET /api/v1/items` returns a list, `GET /api/v1/items/<name>` returns item details). Generic implementations exist for cloud storage, network filesystems, and pub/sub systems like Kafka.

2. **Worker Container Interface**: A file-based API where the worker receives an environment variable (`WORK_ITEM_FILE`) pointing to a file containing the work item data. This is simpler than HTTP for workers that are often just shell scripts.

**The Shared Work Queue Infrastructure**: The work queue manager loops: get items from the source, compare against existing Kubernetes Jobs, and create new Jobs for unprocessed items. Kubernetes Job objects provide reliable execution (retries on failure, rescheduling on machine failure) and annotations for tracking which work items have been processed.

**Dynamic Scaling**: The book provides queueing theory for autoscaling: track the average interarrival time (time between new work items) and average processing time. For a stable queue, processing time divided by parallelism must be less than interarrival time. If processing time exceeds interarrival time, the queue grows without bound.

**The Multi-Worker Pattern**: Multiple worker containers can be composed into a single worker using a specialization of the adapter pattern. For example, face detection, face identification, and face blurring can each be separate reusable containers composed into a single pipeline. The face blurring container can be reused to blur other objects (license plates, etc.).

---

### Chapter 11: Event-Driven Batch Processing

When batch processing requires more than simple one-to-one transformations, work queues are linked into workflows (directed acyclic graphs of processing stages).

**Copier**: Duplicates a single work stream into multiple identical streams. Example: video transcoding where the same input file needs to be rendered in 4K, 1080p, low-resolution, and animated GIF formats, each as a separate work queue.

**Filter**: Reduces a stream by removing items that do not meet criteria. Example: filtering newly signed-up users to only those who opted into marketing emails. Filters are implemented as ambassadors wrapping existing work queue sources.

**Splitter**: Divides a stream into multiple streams based on criteria without dropping items. Example: shipping notifications split into email and SMS queues based on user preferences. A splitter can also function as a copier (sending the same item to multiple queues).

**Sharder**: A generalized splitter that divides work evenly using a sharding function. Benefits:
- **Reliability**: Staged rollouts of worker updates affect only one shard's users.
- **Load distribution**: Work can be spread across geographic regions.
- **Fault tolerance**: If one shard fails, the sharding algorithm dynamically redirects work to remaining healthy queues.

**Merger**: Combines multiple work queues into a single queue (the opposite of a copier). Example: multiple source repositories each producing commits are merged into a single build queue. This avoids creating separate build infrastructure for each repository.

**Publisher/Subscriber Infrastructure**: Pub/sub services (Kafka, Azure EventGrid, Amazon SQS) provide the backbone for event-driven workflows. Kafka topics represent the output of each workflow module. Each topic has a replication factor (redundancy) and number of partitions (maximum load-balancing distribution).

---

### Chapter 12: Coordinated Batch Processing

When batch processing requires aggregating outputs from parallel stages, coordination patterns ensure completeness before aggregation.

**Join (Barrier Synchronization)**: All parallel work must complete before any output is released. This ensures data completeness for aggregation but reduces parallelism and increases latency, as the entire pipeline waits for the slowest stage.

**Reduce**: The canonical pattern from MapReduce. Unlike join, reduce optimistically merges outputs as they arrive, reducing the total number of outputs at each step. Because each reduce step operates on a range of inputs and produces similar output, it can be repeated until a single output remains. Critically, reduce can begin while the map/shard phase is still running, improving overall throughput.

**Reduce Operations**:
- **Count**: Shard a book across workers, each counting word frequencies. Reduce merges counts by summing: `{a:50, the:17}` + `{a:30, the:25}` = `{a:80, the:42}`. This can be applied repeatedly in parallel until a single output remains.
- **Sum**: Shard population data geographically, sum (town, population) tuples into progressively larger aggregates until the total population is computed.
- **Histogram**: Build distribution models (e.g., family size percentages) per town, then merge by weighting each histogram by its population and dividing by the combined population.

**Complete Pipeline Example**: An image tagging and processing pipeline combines multiple patterns:
1. **Shard** images across multiple work queues for parallel processing.
2. **Multi-worker** pattern: license plate detection + blurring as separate containers in each pod.
3. **Join** all sharded outputs to ensure every image is blurred before proceeding.
4. **Copier** splits the joined output: one stream deletes originals, another runs vehicle/color detection.
5. **Shard** the detection work across additional queues.
6. **Reduce** the per-image vehicle/color counts into final aggregated statistics.

---

## Conclusion

Burns argues that we are at another moment of technological transformation. The need for distributed systems far exceeds our ability to deliver them. The development of containers and container orchestration provides new tools, and the patterns in this book provide the conceptual framework. Patterns like sidecars, ambassadors, sharded services, FaaS, work queues, and coordinated batch processing should form the foundation of modern distributed systems. Developers should no longer build from scratch as individuals but collaborate on reusable, shared implementations of these canonical patterns.

---

## Key Patterns Summary Table

| Pattern | Category | Purpose |
|---------|----------|---------|
| Sidecar | Single-Node | Augment/extend application container |
| Ambassador | Single-Node | Broker communication with external world |
| Adapter | Single-Node | Normalize application to standard interface |
| Replicated Load-Balanced | Multi-Node Serving | Scale requests per second |
| Sharded Service | Multi-Node Serving | Scale data size beyond one machine |
| Scatter/Gather | Multi-Node Serving | Scale computation time via parallelism |
| FaaS/Event-Driven | Multi-Node Serving | Lightweight, ephemeral processing |
| Ownership Election | Multi-Node Serving | Distributed consensus for single-master |
| Work Queue | Batch | Independent parallel work items |
| Copier | Batch | Duplicate work streams |
| Filter | Batch | Remove unwanted work items |
| Splitter | Batch | Divide work by type |
| Sharder | Batch | Distribute work evenly |
| Merger | Batch | Combine work streams |
| Join | Batch Coordinated | Barrier synchronization |
| Reduce | Batch Coordinated | Aggregate parallel outputs |

---

## Core Design Principles

1. **Container modularity**: Every container should do one thing well, with clearly defined APIs and parameterization.
2. **Separation of concerns**: Split functionality into separate containers for independent development, deployment, and scaling.
3. **Consistent interfaces**: Use adapter patterns to normalize heterogeneous systems to common monitoring, logging, and health-checking interfaces.
4. **Defend in depth**: Layer SSL termination, caching, rate limiting, and application logic as independent tiers.
5. **Design for failure**: Assume components will fail; use replication, TTL-based locks, resource versioning, and double-checking to maintain consistency.
6. **Choose appropriate sharding keys**: Balance between too general (incorrect results) and too specific (poor utilization).
7. **Use consistent hashing**: Minimize disruption when scaling shards.
8. **Beware the straggler problem**: In scatter/gather systems, tail latency and failure rates multiply with parallelism.
9. **Right-size your infrastructure**: FaaS for intermittent work, containers for sustained work, VMs for heavy sustained work.
10. **Build reusable components**: Invest in modular, well-documented, well-API'd containers that the community can share.
