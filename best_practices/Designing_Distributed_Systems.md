# Designing Distributed Systems
**Author:** Brendan Burns (O'Reilly, 2018)
**Topic tags:** `#architecture` `#concurrency` `#api`
**Language focus:** language-agnostic; Kubernetes + Go + Python + Bash examples
**Sources:** `markdown_output/Designing Distributed Systems/Designing Distributed Systems.md` · `summaries/Designing_Distributed_Systems.md`

## TL;DR
Container + container-orchestrator patterns are the universal objects and interfaces for distributed systems. Burns presents a pattern catalog: three single-node patterns (Sidecar, Ambassador, Adapter), five multi-node serving patterns (Replicated, Sharded, Scatter/Gather, Functions/FaaS, Ownership Election), and a batch computational toolkit (Work Queue, Copier, Filter, Splitter, Sharder, Merger, Join, Reduce). Patterns compose like Lego; reusability + a shared vocabulary are the wins.

---

## Best Practices by Topic

### Single-Node Patterns (Sidecar, Ambassador, Adapter)

**Principle:** Co-schedule one or more auxiliary containers in the same pod to augment, broker, or normalize a primary application container — without modifying it.

**Three patterns:**

| Pattern | Role | Co-schedule? | Talks to app via |
|---|---|---|---|
| Sidecar | Augment / extend the application (often without the app's knowledge) | Yes, same pod | Shared localhost / PID namespace / filesystem |
| Ambassador | Broker communication between the app and the outside world | Yes, same pod | App calls localhost; ambassador forwards to sharded / brokered / split targets |
| Adapter | Modify the app's interface to a standard expected by infrastructure | Yes, same pod | Adapter exposes standard interface (Prometheus, Fluentd, health checks) |

*Ref: Distributed Systems — "Single-Node Patterns" / "Sidecar" / "Ambassador" / "Adapters"*

**Motivations to split a single-node app into multiple containers:**
- **Resource isolation** — user-facing app and background config loader have different resource priorities; one must not starve the other
- **Team scaling** — ideal team size is 6–8; small focused containers let small teams own distinct pieces
- **Separation of concerns** — easier to understand, test, update, deploy, roll back

---

### Sidecar Pattern

**Principle:** A sidecar container augments and improves the application container, often without the app's knowledge. Co-scheduled into the same pod; shares filesystem, hostname, network, namespaces.

**Do:**
- Use to add HTTPS termination to a legacy HTTP service (nginx sidecar terminating TLS on the pod IP, proxying plaintext to localhost).
- Use for dynamic configuration sync — sidecar polls a config API, writes to a shared volume, signals the app (SIGHUP, file-watch, or SIGKILL).
- Use modular utility containers (`topz` reading /proc via shared PID namespace) and inject automatically via the orchestrator.
- Build a minimal PaaS by pairing a Node.js + nodemon app container with a `git pull` sidecar sharing the filesystem.

**Don't:**
- Modify the application container when an off-the-shelf image already exists — prefer a sidecar over maintaining a fork.
- Assume the sidecar's work is invisible — notify the app via SIGHUP / SIGKILL or a shared file when state changes.

**Code (nginx HTTPS sidecar pattern):**
```
# Application binds only on localhost (loopback only)
# nginx sidecar lives in the same network namespace
# nginx terminates HTTPS on the external IP, proxies plaintext
# to the legacy app on localhost — plaintext stays on loopback,
# satisfying the network security team.
```
*Ref: Distributed Systems — "An Example Sidecar: Adding HTTPS to a Legacy Service"*

**Code (topz sidecar with shared PID namespace):**
```bash
# launch the topz sidecar in the same PID namespace as the app
docker run --pid=container:${APP_ID} \
  -p 8080:8080 \
  brendanburns/topz:db0fa58 \
  /server --addr=0.0.0.0:8080
# browse http://localhost:8080/topz for process / resource view
```
*Ref: Distributed Systems — "Modular Application Containers"*

---

### Reusable Sidecar Design

**Principle:** Three disciplines make a sidecar reusable.

1. **Parameterize containers** — treat them as functions with parameters passed via environment variables
2. **Define the container's API** — environment variables, HTTP endpoints, config formats, units
3. **Document your containers** — `EXPOSE` directives + comments, `ENV` for defaults, `LABEL` per Label Schema

**Do:**
- Expose every configurable knob as an `ENV` (e.g. `PROXY_PORT`, `CERTIFICATE_PATH`, `UPDATE_FREQUENCY`).
- Use the Label Schema conventions for `LABEL` directives (`org.label-schema.vendor`, `org.label-schema.url`, `org.label-schema.version`).
- Treat subtle changes (seconds → milliseconds, parameter rename) as breaking API changes.

**Don't:**
- Add a parameter without documenting the unit. (10 seconds vs 10 milliseconds is a silent breaking change.)
- Hide important defaults inside the image — surface them as `ENV` defaults.

**Code:**
```dockerfile
# Main web server runs on port 8080
EXPOSE 8080
# The PROXY_PORT parameter indicates the port on localhost
# to redirect traffic to.
ENV PROXY_PORT 8000

LABEL "org.label-schema.vendor"="name@company.com"
LABEL "org.label.url"="http://images.company.com/my-cool-image"
LABEL "org.label-schema.version"="1.0.3"
```
*Ref: Distributed Systems — "Documenting Your Containers"*

---

### Ambassador Pattern

**Principle:** Ambassador brokers communication between the application and the outside world. The app talks to localhost; the ambassador handles sharding / service discovery / traffic splitting.

**Three common uses:**
1. **Sharding** — client always sees one backend; ambassador routes to the right shard
2. **Service brokering** — discover the right MySQL/Redis endpoint per environment (cloud SaaS vs on-prem VM)
3. **Request splitting / experimentation** — split traffic between production and experimental versions

**Do:**
- Use twemproxy (Twitter) with ketama consistent hashing as a Redis/memcache sharding ambassador.
- For experiments, use IP hashing + weighted upstreams so each user has a consistent experience.
- Use IP-hashing for session stickiness in internal clusters; use cookies/HTTP headers for external traffic (NAT breaks IP-based session tracking).

**Don't:**
- Choose ambassador vs shared shard-router service without weighing trade-offs: ambassador = less ops complexity per pod, but each pod carries the proxy; shared service = less duplication, but extra network hop and scaling coordination.

**Code (sharded Redis via twemproxy):**
```yaml
# StatefulSet gives stable DNS names: sharded-redis-0.redis, ...
apiVersion: apps/v1beta1
kind: StatefulSet
metadata:
  name: sharded-redis
spec:
  serviceName: "redis"
  replicas: 3
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
          name: redis
---
# Ambassador listens on localhost:6379, routes to shards
redis:
  listen: 127.0.0.1:6379
  hash: fnv1a_64
  distribution: ketama
  auto_eject_hosts: true
  redis: true
  timeout: 400
  server_retry_timeout: 2000
  server_failure_limit: 1
  servers:
  - sharded-redis-0.redis:6379:1
  - sharded-redis-1.redis:6379:1
  - sharded-redis-2.redis:6379:1
```
*Ref: Distributed Systems — "Hands On: Implementing a Sharded Redis"*

**Code (nginx ambassador for 10% experiments with IP hashing):**
```nginx
worker_processes 5;
events { worker_connections 1024; }
http {
  upstream backend {
    ip_hash;
    server web weight=9;     # 90% prod
    server experiment;        # 10% experiment
  }
  server {
    listen localhost:80;
    location / {
      proxy_pass http://backend;
    }
  }
}
```
*Ref: Distributed Systems — "Hands On: Implementing 10% Experiments"*

---

### Adapter Pattern

**Principle:** Adapter normalizes a heterogeneous application's interface (monitoring, logging, health) to a single standard expected by infrastructure tooling.

**Three common uses:**
1. **Monitoring** — `redis_exporter` adapter exposes Prometheus metrics for Redis
2. **Logging** — Fluentd adapter with `fluent-plugin-redis-slowlog` or `fluent-plugin-storm`
3. **Health monitoring** — Go-based adapter runs MySQL diagnostic queries, exposes `/health` HTTP endpoint

**Do:**
- Decouple monitoring/logging/health from the application container — even when you could modify the app.
- Reuse one MySQL health-check adapter across every MySQL deployment (the team that builds it benefits everyone).
- Use the adapter pattern to avoid forking off-the-shelf images (Redis, MySQL, Storm).

**Don't:**
- Fork vendor containers to add a Prometheus endpoint when an adapter is available.
- Use the same Fluentd config for both stdout-from-app and slowlog-from-Redis — each source needs its own source block.

**Code (Redis + Prometheus adapter):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example
spec:
  containers:
  - image: redis
    name: redis
  # Provide an adapter that implements the Prometheus interface
  - image: oliver006/redis_exporter
    name: adapter
```
*Ref: Distributed Systems — "Hands On: Using Prometheus for Monitoring"*

**Code (Fluentd source for Redis slowlog):**
```
<source>
  type redis_slowlog
  host localhost
  port 6379
  tag redis.slowlog
</source>
```
*Ref: Distributed Systems — "Hands On: Normalizing Different Logging Formats with Fluentd"*

---

### Replicated Load-Balanced Services

**Principle:** Identical stateless replicas behind a load balancer. Foundation of horizontal scale and redundancy.

**Do:**
- Use at least 2 replicas for any service needing 99.9% SLA — a single instance can't roll out fast enough.
- Add a **readiness probe** (separate from liveness probe) so the load balancer doesn't route to containers that are still initializing (connecting to DBs, loading plugins, downloading files).
- Use consistent hashing (or session cookies) for sticky sessions — IP-hash breaks under NAT.
- Add a reverse-proxy tier with rate limiting + DoS defense above the application tier; small limit for anonymous, larger for authenticated.
- Use different SSL certificates for edge termination vs internal services; each internal service has its own cert for independent rollout.
- Deploy the cache as a separate replicated tier (few large replicas) rather than sidecars next to each web server — cache hit rate improves with fewer, larger replicas.

**Don't:**
- Assume session tracking works externally — IP-hash breaks when external traffic is NATed; use cookies.
- Use the cache's IP addresses for session affinity — caches are few and large, so all requests appear to come from cache IPs. Use cookies or HTTP headers.
- Skip the readiness probe — without it, the load balancer may route to a half-initialized container.

**Code (Kubernetes Deployment + readiness probe + Service):**
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: dictionary-server
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: dictionary-server
    spec:
      containers:
      - name: server
        image: brendanburns/dictionary-server
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
kind: Service
apiVersion: v1
metadata:
  name: dictionary-server-service
spec:
  selector:
    app: dictionary-server
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
```
*Ref: Distributed Systems — "Hands On: Creating a Replicated Service in Kubernetes"*

**Three-tier defense in depth (full pattern):**
```
nginx (SSL termination) → Varnish (caching/rate-limit/DoS defense)
   → Application servers (stateless, replicated)
```
*Ref: Distributed Systems — "Expanding the Caching Layer"*

**Rate limiting best practices:**
- Small limit for anonymous; larger limit requires authentication (auditable + barrier to attackers)
- Return HTTP 429 with `X-RateLimit-Remaining` header

---

### Sharded Services

**Principle:** Each replica (shard) serves a subset of requests. Used when the data exceeds a single machine. A root/shard-router dispatches each request to the right shard.

**Do:**
- Choose the shard key by understanding the request semantics — balance between too-general (groups different responses) and too-specific (groups no requests at all).
- Use consistent hashing when resizing shards (moving from N to N+1 should remap only ~K/N keys, not the whole cache).
- Rate-limit your service at less than peak RPS to account for cache degradation (a 50% hit rate doubles effective capacity, but cache failure overwhelms the backend).
- Treat sharded caches as critical infrastructure — they enable your service to handle the load, so their failure must be survivable.
- Use replicated sharded caches when cache is critical and you can't tolerate cold-start during rollouts.
- Use hot sharding with autoscaling to dynamically grow/shrink shards based on organic traffic patterns.

**Don't:**
- Hash the entire HTTP request object (including timestamp + IP) — too specific.
- Hash only the path when the response varies by user/locale — too general (French IP served English content).
- Lose the entire cache when re-sharding — use consistent hashing.
- Assume all shards are equal — viral content creates hot shards; replicate them independently.
- Re-shard without testing the new sharding function — worst case is total cache miss (equivalent to total cache failure).

**Code (sharding function):**
```
Shard = ShardingFunction(Req)
# most commonly:
Shard = hash(Req) % number_of_shards
```

**Shard key selection — three trade-offs:**
- `shard(request)` — too specific (timestamp + IP differ)
- `shard(request.path)` — too general (cache hit serves wrong language)
- `shard(country(request.ip), request.path)` — balances specificity and generality

*Ref: Distributed Systems — "An Examination of Sharding Functions"*

**Sharded vs Replicated cache memory math:**
- Replicated: 10 replicas × 10 GB = 100 GB total capacity, but each replica stores the same 5% (only 10 GB unique)
- Sharded: 10 replicas × 10 GB = 100 GB total capacity, but each shard stores unique data = 50% coverage (50 GB unique)
- **Tenfold improvement** in cache memory utilization

*Ref: Distributed Systems — "Sharded Caching"*

**Code (consistent-hash nginx sharding proxy):**
```nginx
upstream backend {
  # Has the full URI of the request and uses a consistent hash
  hash $request_uri consistent;
  server web-shard-1.web;
  server web-shard-2.web;
  server web-shard-3.web;
}
```
*Ref: Distributed Systems — "Hands On: Building a Consistent HTTP Sharding Proxy"*

**Cache hit-rate math (50% hit rate doubles effective RPS):**
```
Without cache: 1000 RPS max
With 50% hit cache: 2000 RPS (50% served from cache, 50% from backend)
Rate-limit at 1500 RPS to survive half-cache failure.
```
*Ref: Distributed Systems — "The Role of the Cache in System Performance"*

---

### Scatter/Gather

**Principle:** Root node farms the request to all leaves simultaneously; each leaf processes a portion; root combines partial results. Use for embarrassingly parallel problems.

**Do:**
- Use when data is sharded and you want to compute across all shards in parallel (document search across sharded indexes).
- Replicate each shard (load-balanced) for fault tolerance and safe rollouts under load.

**Don't:**
- Scatter without understanding the **straggler problem** — overall latency equals the slowest leaf.
- Scatter to N leaves when each has 99th-percentile latency 2 s: the system's 99th-percentile becomes the 95th-percentile (0.99^N).
- Scatter to 100 leaves when each has 1% failure rate — guaranteed failure.
- Choose scatter/gather for high-volume/short-latency requests where overhead (HTTP parsing, network) dominates.

**Scatter/gather straggler math:**
- 5 leaves with 0.99 success each → 0.95 overall success (95th percentile)
- 100 leaves → virtually guaranteed every request hits the 2-second tail
- 100 leaves with 1% failure each → guaranteed request failure

*Ref: Distributed Systems — "Choosing the Right Number of Leaves"*

**Example — document search:**
- Root receives "search 'cat and dog'"
- Root scatters to leaf-1 (cat → {doc1, doc2, doc4}) and leaf-2 (dog → {doc1, doc3, doc4})
- Root intersects → returns {doc1, doc4}

*Ref: Distributed Systems — "Hands On: Distributed Document Search"*

---

### Functions and Event-Driven Processing (FaaS)

**Principle:** Ephemeral, event-driven functions. FaaS is a component, not a complete architecture.

**FaaS vs serverless distinction:**
- FaaS = event-driven + ephemeral. May run on your own cluster (e.g. Kubeless on Kubernetes), so not necessarily "serverless".
- Serverless = no server management; could be event-driven or not (e.g. container-as-a-service is serverless but not event-driven).

**Use FaaS when:**
- Lightweight stateless request/response transformations (decorator pattern: add default field values to API inputs).
- Async single-instance events that don't block the main flow (two-factor authentication code generation + SMS).
- Event-based pipelines with each step a small FaaS (user signup → email welcome → notification subscriptions).

**Don't use FaaS when:**
- You need long-running background processing (video transcoding, log compression) — FaaS is time-bounded.
- You need to hold large data in memory (search index) — cold-start latency spikes.
- Sustained request volume keeps processors continuously active — pay-per-request becomes more expensive than VMs.
- You can't afford rigorous monitoring — FaaS debugging is hard due to radical decoupling.

**Do:**
- Watch for infinite function loops (`A → B → C → A`) — these only surface at request timeout.
- Add rigorous monitoring and alerting — debugging is friction that offsets FaaS's deployment simplicity.
- Use the decorator pattern for stateless request/response transforms — scales independently of the API server.
- Decompose user-creation flows into a main service that calls a list of required + optional webhook FaaS handlers.

**Don't:**
- Use FaaS for the long-running parts of your application — switch to long-running processes there.
- Couple the scale of your defaulting service with your API service — that's exactly what the decorator pattern avoids.

**Code (FaaS decorator adding default values):**
```python
# Simple handler function for adding default values
def handler(context):
    obj = context.json
    if obj.get("name", None) is None:
        obj["name"] = random_name()
    if obj.get("color", None) is None:
        obj["color"] = "blue"
    return call_my_api(obj)
```
*Ref: Distributed Systems — "Hands On: Adding Request Defaulting Prior to Request Processing"*

**Code (FaaS event handler — two-factor authentication):**
```python
def two_factor(context):
    code = random.randint(100000, 999999)
    user = context.json["user"]
    register_code_with_login_service(user, code)
    account = "my-account-sid"
    token = "my-token"
    client = twilio.rest.Client(account, token)
    user_number = context.json["phoneNumber"]
    msg = "Hello {} your authentication code is: {}.".format(user, code)
    message = client.api.account.messages.create(
        to=user_number, from_="+12065251212", body=msg)
    return {"status": "ok"}
```
*Ref: Distributed Systems — "Hands On: Implementing Two-Factor Authentication"*

**Code (event-based pipeline with required + optional actions):**
```python
def create_user(context):
    for key, value in required.items():
        call_function(value.webhook, context.json)
    for key, value in optional.items():
        if context.json.get(key, None) is not None:
            call_function(value.webhook, context.json)
```
*Ref: Distributed Systems — "Event-Based Pipelines"*

---

### Ownership Election

**Principle:** Exactly one replica is the designated master for a particular task. Most complicated AND most important part of reliable distributed design.

**Do you even need master election?**
- A singleton in a container orchestrator has decent uptime: container crash → restart in seconds (~3 nines); machine failure → reschedule in ~5 minutes (~2 nines).
- Daily deployments (2 min) → ~2 nines; hourly deployments → less than 1 nine.
- For many background processing tasks, singleton is worth the simplicity.
- Only choose master election when you need 4+ nines.

**Do (when you do need it):**
- Use a distributed key-value store (etcd, ZooKeeper, Consul) — don't implement Paxos/RAFT yourself.
- Use **compare-and-swap** + **TTL** as the primitives for locks and ownership.
- Use a **renewable lock** for long-lived ownership — renew every TTL/2.
- Use the key-value store's **resource version** when unlocking — prevents accidentally unlocking another process's lock after your TTL expired.
- Set a **watchdog timer** when acquiring the lock — crash your program if the TTL expires before you call unlock.
- **Double-check the lock** before any guarded operation (`isLocked` check).
- Store the **hostname** of the current master in the lock — workers double-check with the lock server that the requester is still master.
- Include a **resource version** in each request so stale messages from previous ownership epochs are rejected.

**Don't:**
- Implement Paxos/RAFT from scratch — "interesting exercise for an undergraduate CS course, but not something worth doing in practice."
- Forget the TTL on a lock — a dead holder creates a permanent deadlock.
- Forget the resource version check on unlock — your slow process will unlock someone else's lock and hilarity ensues.
- Trust that you are still master after a long pause — re-check before acting.
- Skip the hostname + version checks — single-master assumptions break under network partitions.

**Resource version bug scenario (the "hilarity"):**
1. Process-1 holds lock with TTL `t`
2. Process-1 stalls for longer than `t` (e.g. overloaded machine)
3. Lock TTL expires
4. Process-2 acquires the lock
5. Process-1 wakes up, calls `unlock()` → unlocks Process-2's lock!
6. Process-3 acquires the lock
7. Now Process-2 and Process-3 both think they own the lock

*Ref: Distributed Systems — "Implementing Locks"*

**Code (compare-and-swap primitive):**
```go
func compareAndSwap(key, nextValue, currentValue string) (bool, error) {
    lock.Lock()
    defer lock.Unlock()
    _, containsKey := store[key]
    if !containsKey {
        if len(currentValue) == 0 {
            store[key] = nextValue
            return true, nil
        }
        return false, fmt.Errorf("Expected value %s for key %s, but found empty", key, currentValue)
    }
    if store[key] == currentValue {
        store[key] = nextValue
        return true, nil
    }
    return false, nil
}
```
*Ref: Distributed Systems — "The Basics of Master Election"*

**Code (simpleLock with TTL and resource version):**
```go
func (Lock l) simpleLock() boolean {
    locked, l.version, error = compareAndSwap(l.lockName, "1", "0", l.ttl)
    if error != null {
        locked, l.version, _ = compareAndSwap(l.lockName, "1", null, l.ttl)
    }
    return locked
}

func (Lock l) unlock() {
    compareAndSwap(l.lockName, "0", "1", l.version)  // version match required
}
```
*Ref: Distributed Systems — "Implementing Locks"*

**Code (renewable lock + lock-lost handler):**
```go
func (Lock l) renew() boolean {
    locked, _ := compareAndSwap(l.lockName, "1", "1", l.version, ttl)
    return locked
}

for {
    if !l.renew() {
        handleLockLost()   // terminate all activity requiring the lock
    }
    sleep(ttl/2)
}
```
*Ref: Distributed Systems — "Implementing Ownership"*

---

### Work Queue Systems (Batch)

**Principle:** Independent work items processed in parallel. Goal: complete all work within a time constraint.

**Generic Work Queue architecture:**
- Source Container (ambassador) exposes HTTP REST API:
  - `GET /api/v1/items` → list of item names
  - `GET /api/v1/items/<name>` → item details
- Worker Container receives `WORK_ITEM_FILE` env var pointing to a file containing the work item data.
- Work queue manager loops: get items → diff with existing Jobs → create new Jobs for unprocessed items.

**Do:**
- Version your API from the start (`/api/v1/`). "Refactoring versioning onto an API without it is very expensive."
- Use Kubernetes `Job` objects for reliable work-item execution — the orchestrator handles retries and rescheduling.
- Annotate each Job with the work item it processes (Kubernetes annotations) so you can track completion.
- Make the source container pluggable: cloud storage, NFS, Kafka, Redis all implement the same ambassador interface.
- Make the worker container simple — often a shell script; file-based API is easier than HTTP for shell workers.
- Cap parallel jobs (limit max Job objects) when you can't over-provision resources — accept higher latency under load.
- Auto-scale based on queueing theory: `processing_time / parallelism < interarrival_time` for a stable queue.
- Use the **multi-worker pattern** — compose reusable single-purpose worker containers (face detection, face identification, face blurring) into one logical worker.

**Don't:**
- Skip versioning on the work queue API.
- Couple the work-queue logic to the actual work being done — keep the source/worker interfaces generic.
- Run the work queue without tracking which items have been processed (the manager must track this).
- Use HTTP for the worker API when a file-based API is simpler.

**Code (Python work queue manager creating Kubernetes Jobs):**
```python
import requests, json, time
from kubernetes import client, config

namespace = "default"

def make_container(item, obj):
    container = client.V1Container()
    container.image = "my/worker-image"
    container.name = "worker"
    return container

def make_job(item):
    response = requests.get("http://localhost:8000/items/{}".format(item))
    obj = json.loads(response.text)
    job = client.V1Job()
    job.metadata = client.V1ObjectMeta()
    job.metadata.name = item
    job.spec = client.V1JobSpec()
    job.spec.template = client.V1PodTemplate()
    job.spec.template.spec = client.V1PodTemplateSpec()
    job.spec.template.spec.restart_policy = "Never"
    job.spec.template.spec.containers = [make_container(item, obj)]
    return job

def update_queue(batch):
    response = requests.get("http://localhost:8000/items")
    items = json.loads(response.text)['items']
    ret = batch.list_namespaced_job(namespace, watch=False)
    for item in items:
        found = any(i.metadata.name == item for i in ret.items)
        if not found:
            job = make_job(item)
            batch.create_namespaced_job(namespace, job)

config.load_kube_config()
batch = client.BatchV1Api()
while True:
    update_queue(batch)
    time.sleep(10)
```
*Ref: Distributed Systems — "The Shared Work Queue Infrastructure"*

**Work queue auto-scaling rule (queueing theory):**
- Track average interarrival time (work items arriving) and average processing time
- For a stable queue: `processing_time / parallelism < interarrival_time`
- If processing time > interarrival time → queue grows without bound
- Scale-down heuristic: reduce parallelism until processing time is ~90% of interarrival time

*Ref: Distributed Systems — "Dynamic Scaling of the Workers"*

**Code (ffmpeg worker using WORK_ITEM_FILE):**
```bash
ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png
```
*Ref: Distributed Systems — "Hands On: Implementing a Video Thumbnailer"*

---

### Event-Driven Batch Patterns (Copier, Filter, Splitter, Sharder, Merger)

**Principle:** Link work queues into workflows (DAG of processing stages). Each pattern has a clear composition role.

| Pattern | Role | Example |
|---|---|---|
| **Copier** | Duplicate one stream into multiple identical streams | Video transcoding: same input → 4K, 1080p, low-res, GIF queues |
| **Filter** | Reduce stream by removing items not meeting criteria | Keep only users who opted into marketing emails |
| **Splitter** | Divide stream into multiple streams by criteria (no drops) | Shipping notifications → email queue vs SMS queue |
| **Sharder** | Generalized splitter that distributes evenly by sharding function | Reliability via staged rollouts; geographic distribution; fault tolerance |
| **Merger** | Combine multiple queues into one (opposite of copier) | Multiple source repos → single build queue |

*Ref: Distributed Systems — "Event-Driven Batch Processing"*

**Do:**
- Compose Copier + Filter to build a Splitter (a copier followed by N filters).
- Use Sharder for reliability — staged rollouts of worker updates affect only one shard's users.
- Use Sharder for load distribution across geographic regions.
- Use Sharder for fault tolerance — remaining healthy queues absorb work from failed shards.
- Use a pub/sub infrastructure (Kafka, Azure EventGrid, Amazon SQS) as the backbone for event-driven workflows.
- Configure Kafka topics with `replication-factor 3` (or 5) and `partitions N` (max load-balancing distribution).

**Don't:**
- Drop work items in a Splitter — that's a Filter; use the right primitive.
- Skip staging sharded rollouts — without sharding, a bad worker update affects all users.

**Code (Kafka topic creation with replication + partitions):**
```bash
for x in 0 1 2; do
  kubectl run kafka --image=solsson/kafka:0.11.0.0 --rm --attach --command -- \
    ./bin/kafka-topics.sh --create --zookeeper kafka-service-zookeeper:2181 \
    --replication-factor 3 --partitions 10 --topic photos-$x
done
# replication-factor 3 → redundancy
# partitions 10 → max load-balancing distribution
```
*Ref: Distributed Systems — "Hands On: Deploying Kafka"*

---

### Coordinated Batch Processing (Join, Reduce)

**Principle:** After parallel processing, you need to aggregate outputs. Join = barrier synchronization; Reduce = optimistic merging.

| Pattern | Behavior | Trade-off |
|---|---|---|
| **Join (barrier sync)** | All parallel work completes before any output is released | Strong completeness guarantees; reduced parallelism; higher overall latency |
| **Reduce** | Optimistically merge outputs as they arrive; repeat until single output | Lower latency; can run in parallel with the map/shard phase; produces single comprehensive result |

*Ref: Distributed Systems — "Coordinated Batch Processing"*

**Do:**
- Use Join when you need guaranteed data completeness before aggregation.
- Use Reduce (sum, count, histogram) when you can produce correct output from partial data.
- Combine patterns: Shard → Join → Copier → Shard → Reduce (image tagging example).
- Choose the right reduce operation for the data: count (sum of occurrences), sum (sum of values), histogram (weighted merge by population).

**Don't:**
- Use Merge when you need completeness — Merge blends output; it doesn't guarantee all sources are present.
- Use Join when the work is fire-and-forget — the barrier overhead is wasted.

**Reduce examples:**
- **Count:** `{a:50, the:17}` + `{a:30, the:25}` = `{a:80, the:42}`
- **Sum:** `(Seattle, 4,000,000)` + `(Northampton, 25,000)` = `(Seattle-Northampton, 4,025,000)`
- **Histogram:** Multiply each histogram by relative population, sum, divide by combined population

*Ref: Distributed Systems — "Reduce"*

**Complete image tagging pipeline (everything composed):**
```
Shard images → Multi-worker (license-plate detect + blur) per pod →
Join (wait for all blurred) → Copier (delete originals / vehicle+color detect) →
Shard (vehicle+color work) → Reduce (per-image counts to aggregate)
```
*Ref: Distributed Systems — "Hands On: An Image Tagging and Processing Pipeline"*

---

### Core Design Principles

1. **Container modularity** — every container should do one thing well, with clearly defined APIs and parameterization.
2. **Separation of concerns** — split functionality into separate containers for independent development, deployment, and scaling.
3. **Consistent interfaces** — use adapter patterns to normalize heterogeneous systems to common monitoring, logging, and health-checking interfaces.
4. **Defend in depth** — layer SSL termination, caching, rate limiting, and application logic as independent tiers.
5. **Design for failure** — assume components will fail; use replication, TTL-based locks, resource versioning, double-checking to maintain consistency.
6. **Choose appropriate sharding keys** — balance between too general (incorrect results) and too specific (poor utilization).
7. **Use consistent hashing** — minimize disruption when scaling shards.
8. **Beware the straggler problem** — in scatter/gather systems, tail latency and failure rates multiply with parallelism.
9. **Right-size your infrastructure** — FaaS for intermittent work, containers for sustained work, VMs for heavy sustained work.
10. **Build reusable components** — invest in modular, well-documented, well-API'd containers that the community can share.

*Ref: Distributed Systems — "Conclusion: A New Beginning?"*

---

## Anti-Patterns & Common Mistakes

- **Sidecar that doesn't notify the app:** App loads config once at startup but doesn't watch for changes — sidecar's updates have no effect. *Fix:* SIGHUP, file-watch, or SIGKILL. *Ref: Distributed Systems — "Dynamic Configuration with Sidecars"*

- **Cache as sidecar next to every web server:** Scales cache with web servers, storing the same data redundantly. *Fix:* Deploy cache as a separate tier of few large replicas. *Ref: Distributed Systems — "Deploying Your Cache"*

- **Session tracking via cache IP:** With a few large caches, all web traffic appears to come from cache IPs → session affinity breaks. *Fix:* Use cookies or HTTP headers for session tracking when caching is above. *Ref: Distributed Systems — "Deploying Your Cache"*

- **Hashing the entire request (timestamp + IP + path):** Two identical-content requests map to different shards — cache never hits. *Fix:* Hash only what determines the response. *Ref: Distributed Systems — "Selecting a Key"*

- **Standard modulo sharding during re-shard:** Going from N to N+1 remaps most keys → equivalent to total cache failure. *Fix:* Use consistent hashing (remaps K/N keys). *Ref: Distributed Systems — "Consistent Hashing Functions"*

- **Scatter/gather to N leaves where each has tail latency:** 5 leaves × 0.99 success = 0.95 system success; 100 leaves → 100% hit the tail. *Fix:* Replicate leaves + use load balancing. *Ref: Distributed Systems — "Choosing the Right Number of Leaves"*

- **Lock without TTL:** Dead process holds lock forever. *Fix:* Always set TTL on distributed locks. *Ref: Distributed Systems — "Implementing Locks"*

- **Unlock without resource-version check:** Your TTL-expired process wakes up and unlocks someone else's lock. *Fix:* Use resource version. *Ref: Distributed Systems — "Implementing Locks"*

- **FaaS for long-running background processing:** FaaS is time-bounded; long jobs get killed. *Fix:* Switch to long-running processes for background work. *Ref: Distributed Systems — "The Need for Background Processing"*

- **FaaS for hot data in memory:** Cold-start spikes latency dramatically. *Fix:* Switch to long-running service for hot-data workloads. *Ref: Distributed Systems — "The Need to Hold Data in Memory"*

- **Sharded work queue without staged rollout capability:** Bad worker update affects all users. *Fix:* Shard + stage rollouts shard-by-shard. *Ref: Distributed Systems — "Sharder"*

- **Merge used where Join is needed:** Merge doesn't guarantee all sources are present. *Fix:* Use Join for completeness-required aggregation. *Ref: Distributed Systems — "Join (or Barrier Synchronization)"*

- **Implementing Paxos/RAFT from scratch:** "An interesting exercise for an undergraduate CS course, but not something worth doing in practice." *Fix:* Use etcd, ZooKeeper, or Consul. *Ref: Distributed Systems — "The Basics of Master Election"*

- **PaaS via `git pull` cron sidecar polling HEAD only:** Misses branch-specific deployments. *Fix:* Parameterize the branch as a sidecar environment variable. *Ref: Distributed Systems — "Building a Simple PaaS with Sidecars"*

- **Single replica with 99.9% SLA and daily deployments:** Single instance can't roll out in < 1.4 min/day. *Fix:* At least 2 replicas behind a load balancer. *Ref: Distributed Systems — "Stateless Services"*

---

## Decision Heuristics / Checklists

**Choosing single-node pattern:**
- Augmenting the application (TLS, config, monitoring) → **Sidecar**
- Brokering communication (sharding, service discovery, A/B traffic) → **Ambassador**
- Normalizing to standard monitoring/logging/health interface → **Adapter**

**Choosing multi-node serving pattern:**
- Need horizontal scale + redundancy, identical stateless replicas → **Replicated Load-Balanced**
- Data exceeds one machine → **Sharded**
- Embarrassingly parallel request processing → **Scatter/Gather**
- Ephemeral event-driven stateless work → **Functions (FaaS)**
- Exactly-one master for a task → **Ownership Election** (or skip and use a singleton)

**Choosing batch pattern by intent:**
- Process independent items in parallel → **Work Queue**
- One input → N outputs of the same data → **Copier**
- Drop items that don't match criteria → **Filter**
- Send different items to different queues (no drops) → **Splitter**
- Evenly distribute work for staged rollouts / load balancing / fault tolerance → **Sharder**
- N sources → single queue → **Merger**
- Aggregate only after ALL parallel work completes → **Join**
- Aggregate optimistically (e.g. count, sum, histogram) → **Reduce**

**Shard-key selection rubric:**
- Identify what varies in the response
- Drop fields that don't affect response (timestamp, request ID, IP when not relevant)
- Include fields that change the response (locale, user segment, country)
- Test for determinism (same input → same shard) and uniformity (load evenly distributed)

**Sharding function choice:**
- Fixed shard count, infrequent resizing → standard modulo hashing
- Frequent resizing or capacity addition → consistent hashing
- Geographic distribution → shard by region
- Sticky sessions for internal traffic → IP-hash
- Sticky sessions for external traffic → cookies

**Master election decision:**
- Background processing, OK with 2–3 nines → singleton
- High availability (4+ nines) required → distributed ownership election
- Daily/hourly deployments with no HA budget → consider singleton + pre-pulled images

**Choosing infrastructure right-size:**
- Intermittent work, low steady state → FaaS
- Sustained moderate load → containers (Kubernetes)
- Heavy sustained load with cost optimization → VMs with reservations

**Cache tier sizing rule:**
- Few large replicas (e.g. 2 × 5 GB) > many small replicas (e.g. 10 × 1 GB)
- Larger replicas store more unique data → higher hit rate
- Application tier wants many small replicas (e.g. single-threaded Node.js) to use multiple cores

**Pub/sub topic sizing (Kafka):**
- `replication-factor 3 or 5` for production redundancy
- `partitions N` = max load-balancing distribution

---

## Key Takeaways

1. Container patterns are the universal objects and interfaces for distributed systems — Knuth (algorithms) → GoF (OO patterns) → Burns (distributed container patterns).
2. Three single-node patterns (Sidecar, Ambassador, Adapter) — co-scheduled in pods, sharing namespaces.
3. Reusable containers require three disciplines: parameterize via `ENV`, define the API surface (env vars, endpoints, units), document with `EXPOSE`/`ENV`/`LABEL`.
4. Sharded cache memory utilization is 10× better than replicated cache at the same total capacity.
5. The straggler problem compounds in scatter/gather — replicate each shard to mitigate.
6. FaaS is a component, not a complete architecture — use for stateless event-driven transforms, not for long-running or hot-data workloads.
7. Distributed ownership = compare-and-swap + TTL + resource version + double-check + hostname + renew.
8. Work queue patterns compose: Shard → Multi-worker → Join → Copier → Shard → Reduce is a canonical image-tagging pipeline.
9. Filter, Splitter, Sharder, Merger, Join, Reduce are six fundamental DAG combinators for batch workflows.
10. Design for failure, defend in depth, choose appropriate shard keys, beware the straggler problem, right-size your infrastructure.

---

## Cross-References
- Related: [[../Software_Architecture_Hardparts.md]] — trade-off analysis, granularity, data ownership, sagas
- Related: [[../Software_Architecture_Patterns.md]] — Layered / Microkernel / Event-Driven / Microservices / Space-Based styles
- Topic index: [[../INDEX.md]]