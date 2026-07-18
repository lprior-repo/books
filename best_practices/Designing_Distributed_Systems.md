# Designing Distributed Systems — Deep Dive
**Author:** Brendan Burns (O'Reilly, 2018)
**Topic tags:** `#architecture` `#concurrency` `#api`
**Language focus:** language-agnostic; Kubernetes + Go + Python + Bash
**Sources:** `markdown_output/Designing Distributed Systems/Designing Distributed Systems.md` · `summaries/Designing_Distributed_Systems.md`

## TL;DR
Containers + container-orchestrators are the universal objects and interfaces for distributed systems. Burns presents a pattern catalog: three single-node patterns (Sidecar, Ambassador, Adapter), five multi-node serving patterns (Replicated Load-Balanced, Sharded, Scatter/Gather, Functions/FaaS, Ownership Election), and a batch computational toolkit (Work Queue, Copier, Filter, Splitter, Sharder, Merger, Join, Reduce). The patterns compose like Lego; reusable components + a shared vocabulary are the wins.

---

## Best Practices by Topic

### Distributed Systems Today: A Brief Context
**Principle:** Modern applications must be reliable, always-on, instantly scalable distributed systems. Containers are the new reusable component.

**Do:**
- Treat every modern app as a distributed system from day one.
- Use containers and orchestrators as the universal interface — analogous to how objects became the OO fundamental.
- Build on the open-source container ecosystem (Kubernetes, etcd, Helm, kubeless).
- Stand on the shoulders of giants: algorithms → OO patterns → reusable libraries → distributed-system patterns.

**Don't:**
- Build a distributed system from scratch every time — apply known patterns.
- Skip patterns in favor of bespoke solutions (until patterns are genuinely exhausted).

*Ref: Distributed Systems — "Introduction" / "A Brief History of Systems Development" / "A Brief History of Patterns in Software Development"*

---

### Why Patterns Matter in Distributed Systems
**Principle:** Patterns are a shared vocabulary; reuse and community matter.

**Do:**
- Use pattern names ("sidecar", "ambassador", "sharding") to skip definitions and dive into details.
- Build reusable container images that encode patterns + APIs.
- Stand on shoulders: algos (Knuth), OO (Gang of Four), open source, distributed patterns (Burns).

**Don't:**
- Waste time on names instead of problems.
- Invent bespoke patterns before exhausting the canonical vocabulary.

*Ref: Distributed Systems — "The Value of Patterns, Practices, and Components"*

---

### Single-Node Patterns: When and Why
**Principle:** First decomposition target — split a single node into multiple containers even before distribution.

**Three motivations to split a single-node app:**
1. **Resource isolation** — user-facing app vs. background loader; one must not starve the other.
2. **Team scaling** — ideal team size 6-8; small focused containers let small teams own distinct pieces.
3. **Separation of concerns** — easier to test, deploy, update, roll back.

**Do:**
- Co-schedule tightly coupled containers into a *pod* (Kubernetes atomic unit).
- Share filesystem, hostname, network namespaces, PID namespace, IPC namespace among pod members.
- Treat the pod as the single-machine atomic unit of the distributed-system patterns.

**Don't:**
- Distribute tightly-coupled containers across separate hosts (loses single-machine performance).
- Force every container into the same pod (loses modularity and reuse).

*Ref: Distributed Systems — "Single-Node Patterns" / "Motivations"*

---

### Sidecar Pattern: Augment the App Without Modifying It
**Principle:** A sidecar container co-scheduled in the same pod augments or improves the application — often without the application's knowledge.

**Compare to other single-node patterns:**
| Pattern | Role | Co-scheduled? | Talks to app via |
|---|---|---|---|
| **Sidecar** | Augment / extend the application | Yes (same pod) | Shared localhost / PID / filesystem |
| **Ambassador** | Broker communication between app and outside | Yes (same pod) | App calls localhost; ambassador forwards |
| **Adapter** | Modify the app's interface to a standard | Yes (same pod) | Adapter exposes standard interface (Prometheus, Fluentd, health checks) |

*Ref: Distributed Systems — "The Sidecar Pattern" / "Ambassadors" / "Adapters"*

---

### Sidecar Example 1: Adding HTTPS to a Legacy Service
**Principle:** Co-schedule an nginx sidecar that terminates TLS on the external pod IP, proxying plaintext to the legacy app on localhost.

**Do:**
- Bind the legacy app to localhost only (127.0.0.1).
- Place the nginx sidecar in the same network namespace; route HTTPS traffic to it on the external IP.
- Satisfy the security team (plaintext stays on loopback).
- Modernize without recompiling the legacy app or rebuilding the build system.

**Don't:**
- Modify the legacy source code or build system (expensive, brittle).
- Expose the plaintext service on the pod's external IP.

**Code (illustrative):**
```
# Application binds only on localhost (loopback only)
# nginx sidecar lives in the same network namespace
# nginx terminates HTTPS on the external IP, proxies plaintext
# to the legacy app on localhost — plaintext stays on loopback,
# satisfying the network security team.
```
*Ref: Distributed Systems — "An Example Sidecar: Adding HTTPS to a Legacy Service"*

---

### Sidecar Example 2: Dynamic Configuration Sync
**Principle:** A configuration-manager sidecar polls a config API, writes to a shared directory, signals the legacy app (SIGHUP / SIGKILL).

**Do:**
- Use a shared volume between the application container and the config sidecar.
- Pick the right signal mechanism for the app: file-watch, SIGHUP, or SIGKILL-then-restart.
- Decouple the config retrieval from the app's domain code.

**Don't:**
- Modify the legacy app to read config from a cloud API (expensive and brittle).

*Ref: Distributed Systems — "Dynamic Configuration with Sidecars"*

---

### Sidecar Example 3: topz — Modular Process Introspection
**Principle:** Use a sidecar that shares the **PID namespace** with the app to introspect all processes inside the container group.

**Do:**
- Inject the topz sidecar uniformly via the orchestrator for every deployed application.
- Get consistent process and resource introspection (`/topz` endpoint).
- Avoid per-language library rewrites by using one universal introspection image.

**Code (Docker launch — topz sidecar with shared PID namespace):**
```bash
# launch the topz sidecar in the same PID namespace as the app
docker run --pid=container:${APP_ID} \
  -p 8080:8080 \
  brendanburns/topz:db0fa58 \
  /server --addr=0.0.0.0:8080
# browse http://localhost:8080/topz for process / resource view
```
*Ref: Distributed Systems — "Modular Application Containers" / "Hands On: Deploying the topz Container"*

---

### Sidecar Example 4: Building a Simple PaaS
**Principle:** Pair a Node.js + nodemon app container with a `git pull` sidecar sharing a filesystem — push-to-deploy.

**Code (the sidecar):**
```bash
#!/bin/bash
while true; do
  git pull
  sleep 10
done
```
**How it works:**
- Node.js + nodemon container: serves HTTP, auto-reloads when files change.
- Git sync sidecar: shares filesystem, pulls every 10s.
- Each push to the repo → sidecar syncs → nodemon reloads → new version live.

**Do:**
- Reserve this pattern for low-stakes dev environments or simple production services.
- Branch out the script if you need specific branches (the book purposely keeps the example simple).

**Don't:**
- Use it for high-traffic production without testing the reload semantics thoroughly.

*Ref: Distributed Systems — "Building a Simple PaaS with Sidecars"*

---

### Designing Sidecars for Modularity and Reusability
**Principle:** Three disciplines make a sidecar reusable — parameterize, define API, document.

**1. Parameterize containers.**
- Treat them as functions; pass parameters via environment variables (preferred over command-line).
- Every configurable knob is an `ENV` (PROXY_PORT, CERTIFICATE_PATH, UPDATE_FREQUENCY).

**2. Define each container's API.**
- Environment variables, HTTP endpoints, config formats, units — all part of the API.
- Subtle changes (seconds → milliseconds, parameter rename) are breaking API changes.

**3. Document your containers.**
- Use `EXPOSE` for ports (with comments).
- Use `ENV` for defaults and documentation.
- Use `LABEL` per Label Schema conventions:
  ```dockerfile
  # org.label-schema.vendor / org.label-schema.url / org.label-schema.version
  ```

**Do:**
- Document the *unit* of every parameter (the book's example: 10s vs 10ms is a silent breaking change).
- Treat subtle changes as breaking API changes.
- Use common labels so off-the-shelf tools work with your image.

**Don't:**
- Add a parameter without documenting the unit.
- Hide defaults inside the image — surface them as `ENV` defaults.

**Code (parameterize and document):**
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
**Code (CLI parameterization example):**
```bash
docker run -e=PROXY_PORT=8080 -e=CERTIFICATE_PATH=/path/to/cert.crt ...
```
*Ref: Distributed Systems — "Designing Sidecars for Modularity and Reusability" / "Parameterized Containers" / "Define Each Container's API" / "Documenting Your Containers"*

---

### Ambassador Pattern: Broker Communication
**Principle:** An ambassador container brokers interactions between the application and the outside world.

*Ref: Distributed Systems — "Ambassadors"*

---

### Ambassador Example 1: Sharding a Service (twemproxy + Redis)
**Principle:** A sharding ambassador proxy in front of sharded Redis exposes a "single Redis" interface on localhost.

**Do:**
- Use **Kubernetes StatefulSet** for stable DNS names per shard.
- Use **Kubernetes Service (clusterIP: None)** to create DNS names for each replica.
- Configure **twemproxy** (Twitter's open-source proxy) with ketama consistent hashing.
- Listen on `127.0.0.1:6379` so the application can connect to a "single Redis" on localhost.

**Don't:**
- Bake sharding logic into the application code (defeats deployment simplicity).
- Forget that "sharded service with frontend client" and "sharded service with shard-router service" are alternatives with different operational costs.

**Code (Redis StatefulSet):**
```yaml
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
      terminationGracePeriodSeconds: 10
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
        name: redis
```
**Code (Redis headless Service for DNS):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  labels:
    app: redis
spec:
  ports:
  - port: 6379
    name: redis
  clusterIP: None
  selector:
    app: redis
```
**Code (twemproxy config — ketama consistent hashing):**
```
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
**Code (twemproxy ambassador pod):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ambassador-example
spec:
  containers:
  # This is where the application container would go, for example
  # - name: nginx
  # image: nginx
  # This is the ambassador container
  - name: twemproxy
    image: ganomede/twemproxy
    command:
    - "nutcracker"
    - "-c"
    - "/etc/config/nutcracker.yaml"
    - "-v"
    - "7"
    - "-s"
    - "6222"
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: twem-config
```
*Ref: Distributed Systems — "Using an Ambassador to Shard a Service" / "Hands On: Implementing a Sharded Redis"*

---

### Ambassador Example 2: Service Brokering / Service Discovery
**Principle:** The ambassador introspects its environment and brokers the appropriate connection — the app always connects to localhost.

**Do:**
- Deploy an ambassador that does service discovery on behalf of the app.
- App stays blissfully unaware of cloud-vs-on-prem vs. multi-cloud topology.
- Use the ambassador to find MySQL, Redis, etc. on the right backend.

**Don't:**
- Bake service discovery logic into the application container.

*Ref: Distributed Systems — "Using an Ambassador for Service Brokering"*

---

### Ambassador Example 3: Request Splitting / A/B Experimentation
**Principle:** An nginx ambassador splits 90/10 between production and experiment using `ip_hash` + `weight`.

**Do:**
- Use `ip_hash` so each user doesn't flip-flop between experiment and main site (consistent experience).
- Tune `weight` to send the desired percent of traffic to the experiment.
- Consider the alternative of deploying the experiment framework as a separate microservice.

**Don't:**
- Random-route users — every user must have a consistent experience.
- Ignore that experimentation as a service is a long-term commit; experimentation as an ambassador is occasional.

**Code (nginx config for 10% experiment):**
```
worker_processes 5;
error_log error.log;
pid nginx.pid;
worker_rlimit_nofile 8192;
events {
  worker_connections 1024;
}
http {
  upstream backend {
    ip_hash;
    server web weight=9;
    server experiment;
  }
  server {
    listen localhost:80;
    location / {
      proxy_pass http://backend;
    }
  }
}
```
*Ref: Distributed Systems — "Using an Ambassador to Do Experimentation or Request Splitting" / "Hands On: Implementing 10% Experiments"*

---

### Adapter Pattern: Standardize the Interface
**Principle:** An adapter container normalizes a heterogeneous app's interface to a standard the infrastructure expects (Prometheus, Fluentd, health endpoints).

**Why:** Real apps are heterogeneous — different languages, log formats, monitoring protocols. A single tool can't ingest all of them. The adapter provides a uniform output.

**Do:**
- Use an adapter when the app is 3rd-party or off-the-shelf and can't be modified.
- Decouple the adapter from the app — rolling out a new app version doesn't require rolling out a new adapter.
- Reuse the same adapter across many apps.

**Don't:**
- Modify the application container when an off-the-shelf image already exists — prefer an adapter over maintaining a fork.

*Ref: Distributed Systems — "Adapters"*

---

### Adapter Example 1: Prometheus Monitoring for Redis
**Principle:** Add a `redis_exporter` adapter to expose Redis metrics in Prometheus format.

**Code (Pod with adapter):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example
  namespace: default
spec:
  containers:
  - image: redis
    name: redis
  # Provide an adapter that implements the Prometheus interface
  - image: oliver006/redis_exporter
    name: adapter
```
*Ref: Distributed Systems — "Monitoring" / "Hands On: Using Prometheus for Monitoring"*

---

### Adapter Example 2: Fluentd for Logging Normalization
**Principle:** Use Fluentd adapters to normalize heterogeneous log formats into a single structured representation.

**Do:**
- Use community-supported Fluentd plugins for various apps.
- Configure each adapter with `localhost` for connection (shared network namespace).
- Have one log aggregator consume the normalized stream.

**Don't:**
- Modify app containers just to normalize logging — use adapters.

**Code (Redis slowlog adapter):**
```
<source>
  type redis_slowlog
  host localhost
  port 6379
  tag redis.slowlog
</source>
```
**Code (Apache Storm adapter):**
```
<source>
  type storm
  tag storm
  url http://localhost:8080
  window 600
  sys 0
</source>
```
*Ref: Distributed Systems — "Logging" / "Hands On: Normalizing Different Logging Formats with Fluentd"*

---

### Adapter Example 3: Rich Health Checks for MySQL
**Principle:** Add an HTTP health-check adapter that runs application-specific queries against MySQL.

**Code (MySQL adapter — Go):**
```go
package main
import (
  "database/sql"
  "flag"
  "fmt"
  "net/http"
  _ "github.com/go-sql-driver/mysql"
)
var (
  user = flag.String("user", "", "The database user name")
  passwd = flag.String("password", "", "The database password")
  db = flag.String("database", "", "The database to connect to")
  query = flag.String("query", "", "The test query")
  addr = flag.String("address", "localhost:8080",
  "The address to listen on")
)
// Basic usage: db-check --query="SELECT * from my-cool-table"
func main() {
  flag.Parse()
  db, err := sql.Open("localhost",
  fmt.Sprintf("%s:%s@/%s", *user, *passwd, *db))
  if err != nil {
    fmt.Printf("Error opening database: %v", err)
  }
  // Simple web handler that runs the query
  http.HandleFunc("", func(res http.ResponseWriter, req *http.Request) {
    _, err := db.Exec(*query)
    if err != nil {
      res.WriteHeader(http.StatusInternalServerError)
      res.Write([]byte(err.Error()))
      return
    }
    res.WriteHeader(http.StatusOK)
    res.Write([]byte("OK"))
    return
  })
  http.ListenAndServe(*addr, nil)
}
```
**Code (Pod with MySQL adapter):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example-health
  namespace: default
spec:
  containers:
  - image: mysql
    name: mysql
  - image: brendanburns/mysql-adapter
    name: adapter
```
*Ref: Distributed Systems — "Adding a Health Monitor" / "Hands On: Adding Rich Health Monitoring for MySQL"*

---

### Microservices Concept Overview
**Principle:** Microservices: many small services communicating via APIs over a network, contrasting with monoliths.

**Do:**
- Decouple via formal APIs (reduces team synchronization overhead).
- Scale components independently.
- Use the patterns in this book as building blocks.

**Don't:**
- Believe all monoliths are bad — monoliths + modular monoliths have their place.
- Believe the patterns eliminate the complexity — they regularize it.

*Ref: Distributed Systems — "Introduction to Microservices"*

---

### Replicated Load-Balanced Services: Stateless Pattern
**Principle:** Each replica is identical, load balancer distributes requests; the simplest distributed pattern.

**Do:**
- **At minimum 2 replicas** for high availability — even single-replica three-nines (99.9%) requires < 1.4 min downtime/day and < 3.6s for hourly deployments.
- Use **readiness probes** distinct from liveness probes — apps need time to initialize.
- Distinguish **stateless replicated** (every replica serves every request) from **session tracked** (same user → same replica).

**Don't:**
- Rely on a single replica for any production workload.
- Mark a container ready before it can serve real traffic.

**Code (Kubernetes Deployment with readiness probe):**
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
```
**Code (Kubernetes Service — load balancer):**
```yaml
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
*Ref: Distributed Systems — "Replicated Load-Balanced Services" / "Stateless Services" / "Readiness Probes for Load Balancing" / "Hands On: Creating a Replicated Service in Kubernetes"*

---

### Session Tracked Services
**Principle:** Use consistent hashing to bind a user to a specific replica.

**Do:**
- Use IP-based hashing within a cluster (internal IPs).
- Use application-level tracking (cookies) for external IPs because of NAT.
- Minimize replica changes — consistent hashing keeps stable user-to-replica mappings.

**Don't:**
- Use IP-based tracking for external clients (NAT breaks it).

*Ref: Distributed Systems — "Session Tracked Services"*

---

### Caching Layer: Few Large Replicas Beat Many Small
**Principle:** For maximum cache hit-rate, run a few large cache replicas, not many small ones.

**Do:**
- Run 2-3 large Varnish replicas (e.g., 5GB each) — pages stored once, not duplicated.
- Run many small web server replicas to exploit per-core scaling.

**Don't:**
- Run 10 small cache replicas (1GB each) — same page stored 10 times.

**Code (Varnish config pointing at dictionary service):**
```
vcl 4.0;
backend default {
  .host = "dictionary-server-service";
  .port = "8080";
}
```
**Code (Replicated Varnish Deployment with 2GB memory):**
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: varnish-cache
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: varnish-cache
    spec:
      containers:
      - name: cache
        resources:
          requests:
            memory: 2Gi
        image: brendanburns/varnish
        command:
        - varnishd
        - -F
        - -f
        - /etc/varnish-config/default.vcl
        - -a
        - 0.0.0.0:8080
        - -s
        - malloc,2G
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: varnish
          mountPath: /etc/varnish-config
      volumes:
      - name: varnish
        configMap:
          name: varnish-config
```
*Ref: Distributed Systems — "Introducing a Caching Layer" / "Deploying Your Cache" / "Hands On: Deploying the Caching Layer"*

---

### Rate Limiting and DoS Defense at the Cache Layer
**Principle:** Put rate-limiting at the Varnish front layer — anonymous APIs get small limits, logged-in users get higher limits.

**Do:**
- Use Varnish's throttle module for IP+path+login-based throttling.
- Return HTTP 429 when limit hit.
- Populate a rate-limit-remaining header (e.g., `X-RateLimit-Remaining`).

**Don't:**
- Skip rate limiting because "we're not a likely attack target" — misconfigured clients and accidental load tests are real risk.

*Ref: Distributed Systems — "Rate Limiting and Denial-of-Service Defense"*

---

### SSL Termination in nginx (Replication Layer)
**Principle:** Use distinct TLS certs at each layer (edge, internal, services) — they roll independently.

**Do:**
- Generate certs from Let's Encrypt or self-signed for tests (`server.crt`, `server.key`).
- Store as Kubernetes secret.
- Configure nginx to terminate SSL on 443, forward to Varnish on port 80.

**Code (TLS secret):**
```bash
kubectl create secret tls ssl --cert=server.crt --key=server.key
```
**Code (nginx config — SSL termination):**
```
events {
  worker_connections 1024;
}
http {
  server {
    listen 443 ssl;
    server_name my-domain.com www.my-domain.com;
    ssl on;
    ssl_certificate /etc/certs/tls.crt;
    ssl_certificate_key /etc/certs/tls.key;
    location / {
      proxy_pass http://varnish-service:80;
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}
```
**Code (nginx Deployment):**
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ssl
spec:
  replicas: 4
  template:
    metadata:
      labels:
        app: nginx-ssl
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 443
        volumeMounts:
        - name: conf
          mountPath: /etc/nginx
        - name: certs
          mountPath: /etc/certs
      volumes:
      - name: conf
        configMap:
          name: nginx-conf
      - name: certs
        secret:
          secretName: ssl
```
*Ref: Distributed Systems — "SSL Termination" / "Hands On: Deploying nginx and SSL Termination"*

---

### Sharded Services: Stateful Pattern
**Principle:** Each shard serves only a subset of requests; the root router dispatches requests to the right shard.

**Compare:**
- **Replicated** = each replica can serve any request; suited for stateless.
- **Sharded** = each replica (shard) serves a subset; suited for stateful scaling.

**Do:**
- Shard when the data size exceeds a single machine's RAM/disk.
- Mix with replication per shard for fault tolerance (replicated, sharded caches).
- Combine: sharded (scaling by data) + replicated per shard (scaling by request + redundancy).

**Don't:**
- Shard until you actually need to (premature distribution is costly).
- Forget that hot shards cause load imbalance — use hot sharding to scale individual shards.

*Ref: Distributed Systems — "Sharded Services" / "Sharded Caching" / "Hot Sharding Systems"*

---

### Sharded Cache Math: Replicated vs. Sharded Storage Efficiency
**Principle:** A sharded cache stores more unique data than a replicated cache for the same total RAM.

**Example math (book):**
```
10 GB per cache × 10 replicas × 100 RPS each
Total data possible: 200 GB
Request rate needed: 1000 RPS

Replicated (10 replicas each storing same data):
  Stores max: 10 GB (5% of 200 GB)        ← poor utilization
  Serves: 1000 RPS                        ✓

Sharded (10 replicas each storing unique subset):
  Stores max: 100 GB (50% of 200 GB)      ← 10× better
  Serves: 1000 RPS                        ✓
```
**Do:** Choose sharded when (data_set_size > per-replica_RAM × replica_count) AND unique-content-per-replica is acceptable.

**Don't:** Use sharded when the cache hit rate matters more than memory efficiency.
*Ref: Distributed Systems — "Why You Might Need a Sharded Cache" / "Replicated, Sharded Caches"*

---

### Hands On: Sharded Memcache with Ambassador
**Principle:** Reuse the StatefulSet + Service + twemproxy configmap + ambassador pod pattern from Redis.

**Code (Memcache StatefulSet):**
```yaml
apiVersion: apps/v1beta1
kind: StatefulSet
metadata:
  name: sharded-memcache
spec:
  serviceName: "memcache"
  replicas: 3
  template:
    metadata:
      labels:
        app: memcache
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: memcache
        image: memcached
        ports:
        - containerPort: 11211
        name: memcache
```
**Code (Memcache headless service):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: memcache
  labels:
    app: memcache
spec:
  ports:
  - port: 11211
    name: memcache
  clusterIP: None
  selector:
    app: memcache
```
**Code (twemproxy config for memcache):**
```
memcache:
  listen: 127.0.0.1:11211
  hash: fnv1a_64
  distribution: ketama
  auto_eject_hosts: true
  timeout: 400
  server_retry_timeout: 2000
  server_failure_limit: 1
  servers:
  - memcache-0.memcache:11211:1
  - memcache-1.memcache:11211:1
  - memcache-2.memcache:11211:1
```
*Ref: Distributed Systems — "Hands On: Deploying an Ambassador and Memcache for a Sharded Cache"*

---

### Sharding Functions: Determinism + Uniformity
**Principle:** A sharding function deterministically maps a request to a shard; outputs should be uniformly distributed across shards.

**Do:**
```
Shard = Hash(Req) % N
```
- **Determinism** — same input → same output (so the request always goes to the same shard).
- **Uniformity** — outputs spread evenly (so shards balance).

**Don't:**
- Skip modulo when hash outputs are larger than N.
- Use a weak hash (non-uniform) and rely on modulo to fix distribution.

*Ref: Distributed Systems — "An Examination of Sharding Functions" / "Determinism" / "Uniformity"*

---

### Selecting the Right Shard Key
**Principle:** Choose the key that matches what *distinguishes* the response — not the entire request object.

**Examples from the book:**
```
Bad:    hash(whole_request)            → different shards for same logical request
        (time, IP, path vary)
Better: hash(request.path)            → same shard for same path
Good:   hash(country(request.ip),
         request.path)                → same shard for same country + path
```

**Do:** Use country instead of IP — groups identical requests from the same country.
**Don't:** Use a too-specific or too-general key.
*Ref: Distributed Systems — "Selecting a Key"*

---

### Consistent Hashing for Re-sharding
**Principle:** A consistent hashing function remaps only K/N keys when scaling from N shards to N+1, instead of invalidating all keys.

```
Without consistent hashing (modulo + N):
  Scaling from 10 to 11 shards → ~ALL keys remap → cache miss flood

With consistent hashing:
  Scaling from 10 to 11 shards → K/11 (~9%) remap → graceful degradation
```

**Do:** Use consistent hashing for any sharding layer that needs resizing (memcache/Redis/twemproxy/ketama).
**Don't:** Assume plain modulo is fine — it isn't once you have to re-shard.
*Ref: Distributed Systems — "Consistent Hashing Functions"*

---

### Hands On: nginx as Consistent HTTP Sharding Proxy
**Principle:** Use `hash $request_uri consistent;` in nginx as a one-line consistent hashing sharder.

**Code (nginx consistent hash):**
```
worker_processes 5;
error_log error.log;
pid nginx.pid;
worker_rlimit_nofile 8192;
events {
  worker_connections 1024;
}
http {
  upstream backend {
    # Hash the full URI of the request and use a consistent hash
    hash $request_uri consistent;
    server web-shard-1.web;
    server web-shard-2.web;
    server web-shard-3.web;
  }
  server {
    listen localhost:80;
    location / {
      proxy_pass http://backend;
    }
  }
}
```
**Key includes the full URI (path + query + fragment) — but NOT cookies, NOT location.**

*Ref: Distributed Systems — "Hands On: Building a Consistent HTTP Sharding Proxy"*

---

### Hot Sharding Systems
**Principle:** When organic load skews toward one shard, scale just that shard; squash the others.

**How:**
- Set autoscaling per shard.
- When shard A becomes hot → replicate it to a second node.
- Move shard B and C onto a single node (since combined load fits).

**Do:** Use replicated, sharded caches when data-set *and* request-rate scaling are both critical.
**Don't:** Try to scale individual shards unless your orchestrator supports per-shard autoscaling.
*Ref: Distributed Systems — "Hot Sharding Systems"*

---

### Scatter/Gather: Parallelism over Time
**Principle:** Scatter requests to all leaves in parallel; each returns a partial result; the root merges the final response.

**Difference from replicated/sharded:** Scatter/gather requires *every* leaf to respond — total time = slowest leaf (the straggler problem).

**Do:**
- Use for embarrassingly parallel work where the work can be divided into partial results.
- Replication of each leaf shard preserves fault tolerance.
- Tune parallelism: more leaves gives more parallelism but more overhead AND straggler exposure.

**Don't:**
- Use for tight-coupling results that depend on global state.
- Add more leaves than the straggler-probability-vs-overhead trade-off justifies.

*Ref: Distributed Systems — "Scatter/Gather"*

---

### Scatter/Gather Straggler Math
**Principle:** Each leaf added multiplies the per-request straggler probability.

**Example from book:**
```
Single request, 99th percentile latency = 2 sec  (1% chance)
Scatter to N leaves:

  1 leaf:  1% chance of 2-sec latency
  5 leaves: 5% chance of 2-sec latency for at least one
  100 leaves: 99.99...% chance of at least one 2-sec latency
            → user always sees 2 sec!
```

**Conclusion:** Doubling parallelism halves the work but also halves the tolerance for slow leaves. Bound the number of leaves by your latency SLO.

*Ref: Distributed Systems — "Choosing the Right Number of Leaves"*

---

### Scatter/Gather Reliability
**Principle:** With scatter/gather, a single replica per leaf means a single leaf failure causes every request to fail.

**Do:**
- Replicate each leaf (replicated, sharded scatter/gather).
- This makes each leaf request load-balanced across healthy replicas.
- Allows upgrades during production traffic.

**Don't:** Run scatter/gather with a single replica per leaf in production.
*Ref: Distributed Systems — "Scaling Scatter/Gather for Reliability and Scale"*

---

### Functions and Event-Driven Processing (FaaS)
**Principle:** FaaS = stateless functions triggered by events, scaled automatically, billed per-request.

**Benefits:**
- Code → production in seconds (no artifact to build or push).
- Automatic scaling and recovery.
- Functions are the most granular building block.

**Do:** Use FaaS for stateless transformations triggered by events (request/response decorators, event handlers, pipelines).

**Don't:**
- Use FaaS for long-running background jobs (transcoding, log compression).
- Use FaaS for in-memory data sets (loading time hurts latency).
- Use FaaS for sustained high-rate request streams — economics favor VMs.

*Ref: Distributed Systems — "Functions and Event-Driven Processing"*

---

### FaaS Pattern 1: Decorator Pattern
**Principle:** A FaaS can transform requests or responses between the user and the service.

**Do:** Use kubeless to deploy decorators (default value injection, validation, etc.).

**Code (Python default-injection FaaS):**
```python
# Simple handler function for adding default values
def handler(context):
  # Get the input value
  obj = context.json
  # If the 'name' field is not present, set it randomly
  if obj.get("name", None) is None:
    obj["name"] = random_name()
  # If the 'color' field is not present, set it to 'blue'
  if obj.get("color", None) is None:
    obj["color"] = "blue"
  # Call the actual API, potentially with the new default
  # values, and return the result
  return call_my_api(obj)
```
**Code (deploy with kubeless):**
```bash
kubeless function deploy add-defaults \
  --runtime python27 \
  --handler defaults.handler \
  --from-file defaults.py \
  --trigger-http
```
**Code (test invocation):**
```bash
kubeless function call add-defaults --data '{"name": "foo"}'
```
*Ref: Distributed Systems — "The Decorator Pattern: Request or Response Transformation" / "Hands On: Adding Request Defaulting Prior to Request Processing"*

---

### FaaS Pattern 2: Handling Events (Two-Factor Auth)
**Principle:** Handle events asynchronously via FaaS — fire from main app, the FaaS handles slow network work.

**Code (Two-Factor Authentication FaaS):**
```python
def two_factor(context):
  # Generate a random six digit code
  code = random.randint(100000, 999999)
  # Register the code with the login service
  user = context.json["user"]
  register_code_with_login_service(user, code)
  # Use the twillio library to send texts
  account = "my-account-sid"
  token = "my-token"
  client = twilio.rest.Client(account, token)
  user_number = context.json["phoneNumber"]
  msg = "Hello {} your authentication code is: {}.".format(user, code)
  message = client.api.account.messages.create(to=user_number,
  from_="+12065251212",
  body=msg)
  return {"status": "ok"}
```
**Code (deploy):**
```bash
kubeless function deploy add-two-factor \
  --runtime python27 \
  --handler two_factor.two_factor \
  --from-file two_factor.py \
  --trigger-http
```
*Ref: Distributed Systems — "Handling Events" / "Hands On: Implementing Two-Factor Authentication"*

---

### FaaS Pattern 3: Event-Based Pipelines
**Principle:** Decompose complex business flows into FaaS handlers connected by webhooks.

**Do:**
- Build the user-creation service with two lists: required actions, optional actions.
- Implement each action as a FaaS called via webhook.

**Code (event-driven user creation):**
```python
def create_user(context):
  # For required event handlers, call them universally
  for key, value in required.items():
    call_function(value.webhook, context.json)
  # For optional event handlers, check and call them
  # conditionally
  for key, value in optional.items():
    if context.json.get(key, None) is not None:
      call_function(value.webhook, context.json)
```
**Code (email user FaaS):**
```python
def email_user(context):
  user = context.json['username']
  msg = 'Hello {} thanks for joining my awesome service!".format(user)
  send_email(msg, contex.json['email'])

def subscribe_user(context):
  email = context.json['email']
  subscribe_user(email)
```
*Ref: Distributed Systems — "Event-Based Pipelines" / "Hands On: Implementing a Pipeline for New-User Signup"*

---

### Ownership Election — When to Skip It
**Principle:** A single-replica service in Kubernetes has surprisingly good uptime via restart guarantees.

**Math from book:**
```
Container crash + restart in ~2 sec → ~99.99% uptime
Machine failure + Kubernetes move in ~5 min → 2 nines
But: software rollouts kill downtime more than failures do.
```

**Daily deployment of 2-min restart = 2-nines SLA.
Hourly deployment = single-nine SLA (basically unusable for high availability).

**Use master election ONLY when:**
- Four+ nines SLA required.
- Continuous or rapid deployment required.

**Don't:** Add master-election complexity for "background asynchronous processing" where brief downtime is acceptable.
*Ref: Distributed Systems — "Determining If You Even Need Master Election"*

---

### Master Election Basics via etcd
**Principle:** Build master election via a distributed key-value store (etcd, ZooKeeper, Consul) that provides **compare-and-swap** and **TTL**.

**Do:**
- Use etcd, ZooKeeper, or Consul instead of Paxos/Raft from scratch.
- Implement leases for renewable lock ownership.
- Use both compare-and-swap AND TTL to handle process failure.

**Don't:** Implement Paxos/Raft yourself — and "implementing one of these algorithms is akin to implementing locks on top of assembly CAS instructions" (book).
*Ref: Distributed Systems — "The Basics of Master Election"*

---

### Compare-and-Swap Primitives (Go code)
**Principle:** CAS atomically writes a new value iff the existing value matches expected; key-value stores also support TTL.

**Code (CAS in Go — illustrative of underlying primitive):**
```go
var lock = sync.Mutex{}
var store = map[string]string{}
func compareAndSwap(key, nextValue, currentValue string) (bool, error) {
  lock.Lock()
  defer lock.Unlock()
  _, containsKey := store[key]
  if !containsKey {
    if len(currentValue) == 0 {
      store[key] = nextValue
      return true, nil
    }
    return false, fmt.Errorf("Expected value %s for key %s, but found empty", key)
  }
  if store[key] == currentValue {
    store[key] = nextValue
    return true, nil
  }
  return false, nil
}
```
*Ref: Distributed Systems — "The Basics of Master Election"*

---

### Deploying etcd with Helm
**Principle:** The etcd-operator + Helm combination turns etcd deployment into a one-line Kubernetes resource.

**Code (Helm install):**
```bash
# Initialize helm
helm init
# Install the etcd operator
helm install stable/etcd-operator
```
**Code (etcd Cluster resource):**
```yaml
apiVersion: "etcd.coreos.com/v1beta1"
kind: "Cluster"
metadata:
  # Whatever name you want here
  name: "my-etcd-cluster"
spec:
  # 1, 3, 5 are the options for size
  size: 3
  # The version of etcd to install
  version: "3.1.0"
```
**Code (store data in etcd):**
```bash
kubectl exec my-etcd-cluster-0000 -- sh -c "ETCD_API=3 etcdctl
--endpoints=${ETCD_ENDPOINTS} set foo bar"
```
*Ref: Distributed Systems — "Hands On: Deploying etcd"*

---

### Implementing Locks (etcd compare-and-swap)
**Principle:** A distributed lock = a key + precondition write + TTL.

**Code (simple lock — Go):**
```go
func (Lock l) simpleLock() boolean {
  // compare and swap "1" for "0"
  locked, error = compareAndSwap(l.lockName, "1", "0")
  // lock doesn't exist, try to write "1" with a previous value of
  // non-existent
  if error != nil {
    locked, _ = compareAndSwap(l.lockName, "1", nil)
  }
  return locked
}
```
**Code (blocking lock with watch):**
```go
func (Lock l) lock() {
  while (!l.simpleLock()) {
    waitForChanges(l.lockName)
  }
}
```
**Code (unlock — Go):**
```go
func (Lock l) unlock() {
  compareAndSwap(l.lockName, "0", "1")
}
```

**Watch out for the TTL bug:** if Process-1's lock times out and Process-2 acquires it, Process-1's late `unlock()` will unlock Process-2's lock. Use a **resource version** to make `unlock` check both value AND version:
```go
func (Lock l) simpleLock() boolean {
  locked, l.version, error = compareAndSwap(l.lockName, "1", "0", l.ttl)
  if error != null {
    locked, l.version, _ = compareAndSwap(l.lockName, "1", null, l.ttl)
  }
  return locked
}
func (Lock l) unlock() {
  compareAndSwap(l.lockName, "0", "1", l.version)  // version-checked
}
```
*Ref: Distributed Systems — "Implementing Locks"*

---

### etcdctl Lock / Unlock Commands
**Code (etcd lock example — Alice and Bob race for my-lock):**
```bash
# Create the lock
kubectl exec my-etcd-cluster-0000 -- sh -c \
  "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} set my-lock unlocked"

# Alice grabs the lock
kubectl exec my-etcd-cluster-0000 -- sh -c \
  "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} \
  set --swap-with-value unlocked my-lock alice"
# ^ succeeds

# Bob tries — fails
kubectl exec my-etcd-cluster-0000 -- sh -c \
  "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} \
  set --swap-with-value unlocked my-lock bob"
# Error: 101: Compare failed ([unlocked != alice]) [6]

# Alice unlocks
kubectl exec my-etcd-cluster-0000 -- sh -c \
  "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} \
  set --swap-with-value alice my-lock unlocked"
```
*Ref: Distributed Systems — "Hands On: Implementing Locks in etcd"*

---

### Renewable Locks / Leases
**Principle:** For long-lived ownership (active scheduler), renew the lock every TTL/2 seconds.

**Code (renewable lock — Go):**
```go
func (Lock l) renew() boolean {
  locked, _ = compareAndSwap(l.lockName, "1", "1", l.version, ttl)
  return locked
}
```
**Code (renewal loop — Go):**
```go
for {
  if !l.renew() {
    handleLockLost()
  }
  sleep(ttl/2)  // renew at half TTL to avoid timing accidents
}
```
**Code (etcd leased lock creation):**
```bash
kubectl exec my-etcd-cluster-0000 -- \
  sh -c "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} \
  --ttl=10 mk my-lock alice"

# Renewing the lease
kubectl exec my-etcd-cluster-0000 -- \
  sh -c "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} \
  set --ttl=10 --swap-with-value alice my-lock alice"
```
**Important:** If processing could last longer than the lock's TTL, set a watchdog timer that crashes your program if TTL expires before unlock.
*Ref: Distributed Systems — "Implementing Ownership" / "Hands On: Implementing Leases in etcd"*

---

### Handling Concurrent Data Manipulation (Double-Check Before Acting)
**Principle:** Two replicas can briefly both believe they hold the lock (GC pauses, network hiccups). Double-check before acting; carry the resource version with requests.

**Code (isLocked double-check):**
```go
func (Lock l) isLocked() boolean {
  return l.locked && l.lockTime + 0.75 * l.ttl > now()
}
```
**Defense in depth:**
1. Store the hostname of the current owner in the key-value store.
2. Workers receiving requests validate that the requester is still the master.
3. Send the **resource version** with each request; validate both owner AND version.

*Ref: Distributed Systems — "Handling Concurrent Data Manipulation"*

---

### Work Queue Systems: Source Container + Worker Container
**Principle:** Compose a generic work queue from two interfaces — a source container (HTTP API) and a worker container (file-based input).

**The work queue API (HTTP-based, on localhost):**
```
GET http://localhost/api/v1/items       → list of all items
GET http://localhost/api/v1/items/<name> → item details
```
**Code (ItemList response):**
```json
{
  kind: ItemList,
  apiVersion: v1,
  items: [
    "item-1",
    "item-2",
    "..."
  ]
}
```
**Code (Item response):**
```json
{
  kind: Item,
  apiVersion: v1,
  data: {
    "some": "json",
    "object": "here",
  }
}
```

**Worker API (file-based — env var WORK_ITEM_FILE):**
- Orchestrator writes the work item data to a file.
- The file is mounted as a Kubernetes ConfigMap.
- The worker reads the file on startup.

**Do:**
- Always version your APIs (use `/v1/`) — it costs nothing now and is painful to add later.
- Use HTTP for the source container (on localhost — security isn't a concern).
- Use file-based for the worker container (often a shell script — no need to spin a server).

**Don't:**
- Reverse the two (HTTP-based worker = unnecessary complexity for a one-shot script).
- Skip the `/v1/` prefix "because we'll never change it".
*Ref: Distributed Systems — "A Generic Work Queue System" / "The Source Container Interface" / "Work queue API" / "The Worker Container Interface"*

---

### Implementing a Work Queue on Kubernetes (Python)
**Principle:** Use Kubernetes Job objects as the reliable execution mechanism for work items.

**Code (Python work queue orchestrator):**
```python
import requests
import json
from kubernetes import client, config
import time
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
  job.spec.template.spec.containers = [
    make_container(item, obj)
  ]
  return job
def update_queue(batch):
  response = requests.get("http://localhost:8000/items")
  obj = json.loads(response.text)
  items = obj['items']
  ret = batch.list_namespaced_job(namespace, watch=False)
  for item in items:
    found = False
    for i in ret.items:
      if i.metadata.name == item:
        found = True
    if not found:
      # This function creates the job object, omitted for brevity
      job = make_job(item)
      batch.create_namespaced_job(namespace, job)
config.load_kube_config()
batch = client.BatchV1Api()
while True:
  update_queue(batch)
  time.sleep(10)
```
*Ref: Distributed Systems — "The Shared Work Queue Infrastructure"*

---

### Hands On: Video Thumbnailer Work Queue
**Principle:** A Node source lists videos in a shared directory; an ffmpeg worker thumbnails each one.

**Code (Node source container listing `/media/*.mp4`):**
```javascript
const http = require('http');
const fs = require('fs');
const port = 8080;
const path = process.env.MEDIA_PATH;
const requestHandler = (request, response) => {
  console.log(request.url);
  fs.readdir(path + '/*.mp4', (err, items) => {
    var msg = {
      'kind': 'ItemList',
      'apiVersion': 'v1',
      'items': []
    };
    if (!items) { return msg; }
    for (var i = 0; i < items.length; i++) {
      msg.items.push(items[i]);
    }
    response.end(JSON.stringify(msg));
  });
}
const server = http.createServer(requestHandler);
server.listen(port, (err) => {
  if (err) { return console.log('Error starting server', err); }
  console.log(`server is active on ${port}`)
});
```
**Code (worker invocation — ffmpeg every 100 frames):**
```bash
ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png
```
*Ref: Distributed Systems — "Hands On: Implementing a Video Thumbnailer"*

---

### Dynamic Scaling of Work Queues (Interarrival vs. Processing Time)
**Principle:** Keep processing time / parallelism < interarrival time; otherwise the queue grows unbounded.

**Decision table:**
```
interarrival vs processing/parallelism
  1 min/item vs  30 sec    → 2x slack → keep up
  1 min/item vs   1 min    → balanced; not safe for growth
  1 min/item vs   2 min    → queue grows unbounded → SCALE UP
```

**Do:** Track both numbers; build an autoscaler that keeps effective processing time ≤ 90% of interarrival time.
**Don't:** Use "feast or famine" bursty scaling without overprovisioning for safety margin.
*Ref: Distributed Systems — "Dynamic Scaling of the Workers"*

---

### Multi-Worker Pattern (Reuse Across Workers)
**Principle:** Compose multiple worker containers into a single group via the adapter pattern.

**Use case:** Detect faces, tag them with identities, blur them — three different worker functions, one logical pipeline.

**Do:** Implement each step as its own worker, then compose them via an adapter container in the same pod.
**Don't:** Build a single bespoke worker that combines everything — you lose reuse for the next task that needs just one of the steps.
*Ref: Distributed Systems — "The Multi-Worker Pattern"*

---

### Event-Driven Batch Patterns — Overview
**Principle:** Compose work queues into event-driven pipelines using canonical batch patterns.

**Pattern catalogue:**
- **Copier** — duplicate one stream into N identical streams (rendering for multiple formats).
- **Filter** — reduce a stream to a subset (only opted-in users).
- **Splitter** — divide into different streams by criterion (email vs. text notifications).
- **Sharder** — divide uniformly by a sharding function.
- **Merger** — combine multiple streams into one.

**Do:** Chain these patterns to express complex workflows.
**Don't:** Reach for a single mega-queue when a pipeline of small queues is clearer.
*Ref: Distributed Systems — "Event-Driven Batch Processing" / "Patterns of Event-Driven Processing"*

---

### Copier Pattern — Transcoding Example
**Principle:** Use a copier when multiple downstream consumers need the *same* input.

**Example:** One video needs 4K, 1080p, low-resolution, GIF thumbnail — one source item, four queues.

**Don't:** Use a copier when consumers need different items; use a splitter instead.
*Ref: Distributed Systems — "Copier"*

---

### Filter Pattern — Ambassador Around the Source
**Principle:** Wrap the existing source container with a filter adapter that selectively returns items.

**Example:** Filter new-user signups to only those who opted in to email contact.

**Don't:** Filter inside the source container — that mixes domain logic into the source.
*Ref: Distributed Systems — "Filter"*

---

### Splitter Pattern
**Principle:** Use a splitter when you want to divide into different streams, not just drop.

**Example:** Shipping notification splitter — sends each order to either email-queue, text-queue, or both.

**Note:** A splitter + multiple filters = a copier with filtering; sometimes more compact as one splitter than as three pieces.
*Ref: Distributed Systems — "Splitter"*

---

### Sharder Pattern (Batch)
**Principle:** Divide a single queue into evenly-sharded queues by a sharding function.

**Reasons to shard a work queue:**
1. **Reliability** — bad worker update takes out 1/N of users, not all.
2. **Even resource utilization** — spread across regions.
3. **Failure isolation** — region outage only affects that region's shards.

**Do:** Use auto-rebalancing sharding algorithms so unhealthy shards spill over to healthy ones.
*Ref: Distributed Systems — "Sharder"*

---

### Merger Pattern — Multi-Source Build Pipeline
**Principle:** Use a merger to combine multiple work queues into one shared queue.

**Example:** Many source repositories producing commits → merged into one stream for the build system.

**Do:** When you have multiple producers and one consumer, model producers as separate source containers merged into one queue.
*Ref: Distributed Systems — "Merger"*

---

### New-User Signup Flow (End-to-End Example)
**Principle:** A complete pipeline combines sharding, copier, filter.

**Stage 1:** Sharded verification email (reliable, geographic zone isolation).
**Stage 2:** Copier on verification → welcome email queue + notification setup queue.
**Stage 3:** Welcome email sends + exits.
**Stage 4:** Notification queue filtered into email-notifications and text-notifications.
*Ref: Distributed Systems — "Hands On: Building an Event-Driven Flow for New User Sign-Up"*

---

### Publisher/Subscriber Infrastructure (Kafka)
**Principle:** Use Kafka (or equivalent) as the durable pub/sub backbone for event-driven workflows.

**Deploy via Helm:**
```bash
helm init
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name kafka-service incubator/kafka
```
**Create a topic:**
```bash
for x in 0 1 2; do
  kubectl run kafka --image=solsson/kafka:0.11.0.0 --rm --attach --command -- \
  ./bin/kafka-topics.sh --create --zookeeper kafka-service-zookeeper:2181 \
  --replication-factor 3 --partitions 10 --topic photos-$x
done
```
**Producer:**
```bash
kubectl run kafka-producer --image=solsson/kafka:0.11.0.0 --rm -it --command -- \
  ./bin/kafka-console-producer.sh --broker-list kafka-service-kafka:9092 \
  --topic photos-1
```
**Consumer:**
```bash
kubectl run kafka-consumer --image=solsson/kafka:0.11.0.0 --rm -it --command -- \
  ./bin/kafka-console-consumer.sh --bootstrap-server kafka-service-kafka:9092 \
  --topic photos-1 \
  --from-beginning
```
**Parameter guidance:** `--replication-factor 3|5` for redundancy; `--partitions` controls max parallelism.
*Ref: Distributed Systems — "Publisher/Subscriber Infrastructure" / "Hands On: Deploying Kafka"*

---

### Join (Barrier Synchronization)
**Principle:** Unlike a merger, a join blocks downstream processing until *all* upstream work for that stage is complete.

**Use:** Aggregate stages that need full datasets before continuing (sums, averages over entire input).
**Trade-off:** Reduces parallelism and increases latency.
*Ref: Distributed Systems — "Join (or Barrier Synchronization)"*

---

### Reduce Pattern: MapReduce's Reduce Step
**Principle:** Reduce merges two or more outputs into one — can be repeated until a single output remains.

**Three flavors:**
- **Count** — count occurrences of items.
- **Sum** — sum numeric values.
- **Histogram** — combine histograms weighted by population.

**Sample (count) — combine outputs:**
```
Map outputs:
  { a: 50, the: 17, cat: 2 }
  { a: 30, the: 25, dog: 4 }
After reduce:
  { a: 80, the: 42, cat: 2, dog: 4, airplane: 3 }
```
**Do:** Begin reducing in parallel before the map phase finishes — reduces total latency.
*Ref: Distributed Systems — "Reduce" / "Hands On: Count" / "Sum" / "Histogram"*

---

### Hands On: Image Tagging & Processing Pipeline
**Principle:** A complete pipeline from raw URLs to tagged+blurred counts.

**Pipeline stages:**
1. License plate detection worker + blur worker via multi-worker pattern (group in one pod).
2. Shard image URLs across multiple worker queues.
3. After blurring, **join** all shards' output before deleting originals (with join as barrier).
4. **Copier** the blurred results → deletion queue + recognition queue.
5. Inside recognition: shard → multi-worker (vehicle detection + color detection) → join → reduce (final count).

**Output JSON shape per image:**
```json
{
  "vehicles": {
    "car": 12,
    "truck": 7,
    "motorcycle": 4
  },
  "colors": {
    "white": 8,
    "black": 3,
    "blue": 6,
    "red": 6
  }
}
```
*Ref: Distributed Systems — "Hands On: An Image Tagging and Processing Pipeline"*

---

## Anti-Patterns & Common Mistakes
- **Single-replica microservices for high availability:** Even with container-restart, daily deployment cadence makes 99.9% SLA unachievable. *Fix:* go to 2+ replicas; or use master election.
- **Unparameterized sidecars:** Hard-coded values that don't fit reusers. *Fix:* parameterize every configurable knob as an `ENV`.
- **Sidecars that grow into bloat magazzines:** Adding JSONtoXML, Address, Customer to the sidecar. *Fix:* enforce operational-only rule; audit for shared domain classes.
- **Replicated cache when memory efficiency matters more than redundancy:** For 200GB total / 10 shards × 10GB each, replicated = 5% hit rate, sharded = 50%. *Fix:* use sharded for memory-dominated workloads.
- **Plain-hash re-sharding:** Going from `hash % 10` to `hash % 11` remaps 100% of keys. *Fix:* consistent hashing (ketama).
- **Scatter/gather with one replica per leaf:** Single leaf failure = every request fails. *Fix:* replicated, sharded scatter/gather.
- **Scatter/gather with too many leaves:** Straggler problem amplifies — 100 leaves at 1% slowness = 100% slow. *Fix:* bound leaves by SLO.
- **FaaS for long-running background work:** FaaS has time-bounded runtime; transcoding breaks. *Fix:* use containers + VMs for long-running, FaaS for event-driven.
- **Implementing Paxos/Raft yourself:** Book-level discouraged ("an interesting exercise for an undergraduate, but not worth doing in practice"). *Fix:* use etcd/ZooKeeper/Consul.
- **Locks without TTL:** Deadlock-on-process-failure. *Fix:* always use TTL.
- **Locks without resource version:** Subtle TTL-expiration bugs unlock another process's lock. *Fix:* version-check `unlock()`.
- **Foreign keys pointing at moving data:** hard to migrate. *Fix:* business keys, logical references.
- **Treating LATEST as a pinned version (shared library / config):** Bad behavior on hot deploy. *Fix:* pin versions.
- **Forgetting IP vs cookie session tracking:** External clients hit NAT, IP hashing breaks. *Fix:* application-layer cookie tracking.
- **Twemproxy listening only on localhost when you want a shared routing service:** Change `listen: 127.0.0.1` → `listen: 0.0.0.0`. *Fix:* deploy the shared routing service as a separate Deployment + Service.
- **Splitter when filter would do (and vice versa):** Pick the right pattern. *Fix:* if you want to *drop*, use filter; if you want to *divide*, use splitter; if you want to *duplicate*, use copier.

---

## Decision Heuristics / Checklists

### Single-Node Pattern Selection
```
Want to AUGMENT app without modifying it?           → Sidecar
Want to BROKER communication app ↔ outside?         → Ambassador
Want to ADAPT app's interface to a standard?          → Adapter
```

### Replicated vs Sharded
```
State too big for one machine?                      → Shard
Need redundancy for stateless requests?             → Replicate (≥2)
Need both?                                          → Replicated sharded
Both scaling data AND request rate matter?          → Replicated sharded scatter/gather
```

### Sharding Function Selection
```
Single hash space, small key set?                   → hash(Req) % N
Need to resize shards?                              → Consistent hashing (ketama in twemproxy, hash $uri consistent in nginx)
Only specific keys matter?                          → key subset + modulo (hash(country, path) % N)
```

### FaaS Fit Checklist
```
Code-to-deploy in seconds?                          ✓
Event-driven invocations?                           ✓
Stateless, can be parallel?                         ✓
Sustained high-rate requests?                       → consider VM/container
Long-running (>minutes) workload?                   → consider VM/container
Needs significant in-memory data?                   → consider VM/container
Background processing (transcoding)?                → use container batch
```

### Master Election Decision
```
Need 4+ nines SLA?                                  → master election via etcd/ZooKeeper/Consul
Background processing tolerates brief downtime?     → single replica is OK
Continuous deployment + high availability?          → master election
Single-process, no scale required?                  → single replica
```

### FaaS Pattern Selection
```
Transform request before service logic?             → Decorator
Transform response after service logic?              → Decorator
Asynchronous event triggered by app action?          → Handler
Chain of independent transforms per event?           → Pipeline
```

### Lock Discipline Checklist
- TTL > processing time (and processing time known and bounded).
- TTL has resource version to detect lost locks.
- Watchdog timer to crash if TTL expires during processing.
- Renewal every `ttl/2` seconds (renewable leases).
- Workers double-check ownership before acting on requests.

### Work Queue Discipline
- Source container exposes `/api/v1/items` and `/api/v1/items/<name>` on localhost.
- Worker container reads `WORK_ITEM_FILE` (a Kubernetes ConfigMap mount).
- Orchestrator uses Kubernetes Jobs for reliable execution.
- Orchestrator's loop polls sources every N seconds (e.g., 10s).
- Effective processing time / parallelism < interarrival time (with safety margin).

### Kafka Topic Parameters
```
Replication factor: 3 or 5 (redundancy in face of broker crashes)
Partitions:         max parallelism for consumers
                    (e.g., 10 partitions = up to 10 concurrent consumers)
```

### Event-Driven Batch Pattern Selection
```
One input → many parallel outputs (same items)?     → Copier
Reduce items to subset (some drop)?                  → Filter
Divide into distinct streams (no drop)?             → Splitter
Even distribution by hash?                           → Sharder
Combine many streams → one?                          → Merger
Wait for all upstream before next step?             → Join
Combine outputs into aggregate (sum/count/hist)?    → Reduce
```

### Pub/Sub Decision
```
Need durable messages with replay?                  → Kafka
Need at-most-once queue?                            → SQS / pubsub
FaaS as workflow steps?                              → kubeless + webhooks
Full choreographed event pipeline?                   → Kafka + kubeless + Helm
```

### Conclusion Heuristic (the book's main message)
> "*Patterns form a foundation on which modern distributed systems are built. Distributed system developers should no longer be building their systems from scratch as individuals but rather collaborating together on reusable, shared implementations of canonical patterns.*"

---

## Key Takeaways
1. **Containers + orchestrators** are the universal interface; patterns regularize their composition.
2. **Three single-node patterns:** Sidecar (augment), Ambassador (broker), Adapter (normalize).
3. **Five serving patterns:** Replicated Load-Balanced, Sharded, Scatter/Gather, FaaS, Ownership Election.
4. **Two batch patterns chapters:** Work Queue (with Source/Worker interfaces), Event-Driven Batch (Copier/Filter/Splitter/Sharder/Merger), Coordinated Batch (Join + Reduce).
5. **Replicated services** need ≥ 2 replicas for any real SLA; readiness probes are mandatory.
6. **Varnish** = caching layer; **nginx** = SSL termination. Both layered above the application tier.
7. **Consistent hashing** (ketama) is essential for sharding that needs to resize; modulo remaps everything.
8. **Hot shards** = scale just that shard; squash the cold ones together.
9. **Scatter/gather** parallelism is bounded by straggler math: `1 - 0.99^N`.
10. **FaaS** fits stateless, event-driven, request-decorator patterns; avoid for long-running background work or large in-memory data.
11. **Master election** = etcd (or ZooKeeper/Consul); use compare-and-swap + TTL + resource version; never implement Paxos yourself.
12. **Lock with TTL** has a subtle unlock-bug — use resource versions on both `lock` and `unlock`.
13. **Work queues** compose from a generic work-queue manager, a Source (HTTP), a Worker (file-based), and Kubernetes Jobs.
14. **Effective processing time / parallelism < interarrival time** for a stable queue.
15. **Multi-worker pattern** composes multiple worker containers via an adapter into one logical worker.
16. **Copier / Filter / Splitter / Sharder / Merger** are the five canonical event-driven batch patterns; compose them into pipelines.
17. **Join (barrier sync)** waits for *all* upstream before next step; **Reduce** can start in parallel while map still runs.
18. **MapReduce's reduce** = count/sum/histogram; combine outputs iteratively until a single output.
19. **Kafka topic parameters:** `--replication-factor 3|5` + `--partitions N` for max consumer parallelism.
20. **Conclusion:** stop building distributed systems from scratch — share canonical-pattern implementations.

---

## Cross-References
- Related: [[../Software_Architecture_Hardparts.md]] (Neal Ford et al. — the trade-off reasoning complement to Burns' pattern catalog; same architectural domain, complementary lens)
- Related: [[../Microservices_Up_And_Running.md]] (microservices pragmatics; complements Burns' canonical patterns)
- Related: [[../Building_Microservices.md]] (Sam Newman — microservices patterns and team workflow)
- Related: [[../Building_Evolutionary_Architectures.md]] (fitness functions and architectural governance)
- Related: [[../Kubernetes_Up_and_Running.md]] (Burns is co-author — Kubernetes foundations this book assumes)
- Related: [[../Cloud_Application_Architecture_Patterns.md]] (cloud-application-level patterns)
- Topic index: [[../INDEX.md]]
