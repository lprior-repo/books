# Engineering Resilient Systems on AWS
**Authors:** Kevin Schwarz et al. (O'Reilly)
**Topic tags:** `#architecture` `#general`
**Language focus:** language-agnostic (AWS-leaning, Python illustrations)
**Sources:** `markdown_output/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md` · `summaries/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md`

## TL;DR
Resilience is a shared AWS-customer responsibility, pursued by designing for failure using the **SEEMS** model (Single point of failure, Excessive load, Excessive latency, Misconfiguration/bugs, Shared fate), driven by clear **RTO/RPO/BRT** objectives, and proven by continuous testing including AWS **Fault Injection Service (FIS)** chaos experiments. Layer defensive patterns (retries with exponential backoff + jitter, circuit breakers, idempotency, graceful degradation, multi-region failover) — no single pattern delivers resilience, and every defense has its own failure mode to design around.

---

## Best Practices by Topic

### Foundations — Shared Responsibility, RAF, SEEMS, RTO/RPO/BRT

**Principle:** Resilience in the cloud is the customer's responsibility for everything inside the cloud — application architecture, configuration, data. AWS secures the cloud (data centers, network, hardware); you secure your workload inside it.

**AWS Well-Architected Framework — Reliability Pillar (relevant subset):**
- Architectural best practices (HA, fault tolerance, DR strategies).
- Fault tolerance mechanisms (load balancing, replication, graceful degradation).
- Recovery strategies (RTO/RPO-aligned, rehearsed).
- Performance optimization under varying conditions.

**AWS Resilience Analysis Framework (RAF) — the SEEMS model:**
| Failure Category | Resilience Property Violated | Examples |
|---|---|---|
| **S**ingle Point of Failure (SPOF) | Redundancy | One server, one bucket, one region |
| **E**xcessive Load | Sufficient Capacity | Burst, quota exhaustion, throttling |
| **E**xcessive Latency | Timely Output | Tail-latency, slow upstream |
| **M**isconfiguration/Bugs | Correct Output | Bad env var, wrong AMI |
| **S**hared Fate | Fault Isolation | AZ outage, region outage, dependency degradation |

Each failure category maps to a resilient design property (redundancy, sufficient capacity, timely output, correct output, fault isolation). Working backward from "which property is violated?" produces mitigations.

**Recovery Objectives:**
- **RTO** (Recovery Time Objective): maximum acceptable downtime after a disruption.
- **RPO** (Recovery Point Objective): maximum acceptable data loss (in time).
- **BRT** (Bounded Recovery Time): a specific recovery commitment that drives the DR plan.

**The Three Ms (track all three):**
- **MTBF** (Mean Time Between Failures) — informs tolerable failure frequency; sets historic baseline.
- **MTTD** (Mean Time To Detect) — drives monitoring/alerting investment.
- **MTTR** (Mean Time To Repair/Recover) — drives BRT commitments.

**Do:**
- Start with a **BIA (Business Impact Analysis)** and a risk assessment before choosing architecture — set objectives from business impact, then engineer to meet them.
- Use the SEEMS model as a *checklist* when designing or reviewing any service — each category must be explicitly addressed or explicitly out-of-scope.
- Set *coordinated*, *measurable* goals: RTO must align with MTTR baselines; RPO must align with replication frequency.
- Distinguish "downtime" from "unavailable" — downtime can be defined as error rate exceeding X or latency exceeding Y.

**Don't:**
- Don't assume "AWS SLAs" mean your system is reliable — SLAs are baseline; tailor your own objectives to business criticality.
- Don't set RTO without knowing MTTR, or RPO without knowing replication lag — uninformed targets produce uninformed designs.

*Ref: Chapter 1 "Resilience Engineering Foundations" — RAF, SEEMS, well-architected, recovery objectives, three Ms*

---

### Fault Isolation Boundaries (the AZ/Region/Control Plane Triad)

**Principle:** AWS provides layered fault isolation boundaries. Your resilience approach picks which boundaries matter for each workload.

**Hierarchy:**
- **Edge locations** — PoPs worldwide (CloudFront, Lambda@Edge).
- **Regions** — geographically independent; multiple AZs each.
- **Availability Zones (AZs)** — one or more physically separated data centers; independent power, cooling, network.
- **Control planes** — management interfaces isolated from data planes (and often their own failure modes).
- **VPCs / Subnets** — logical isolation within an AZ.

**Do:**
- Plan for AZ failure as the *default* expectation; multi-AZ is table-stakes for any HA workload.
- Use multiple regions only when the business case justifies it (compliance, geographic latency, blast-radius reduction beyond what AZs give).
- Treat control-plane failures (e.g., IAM, EC2 control plane) as real failure modes — data planes can be healthy while their management is impaired.
- Use **Route 53** health-checked failover records as the simplest traffic-routing primitive between regions.

**Don't:**
- Don't over-couple components within the same blast radius (e.g., one Aurora instance + one EC2 in one AZ = SPOF + shared fate).
- Don't treat "single region multi-AZ" as sufficient for all workloads — some businesses require multi-region DR; explicitly opt in or out.

*Ref: Chapter 1 — "AWS Responsibility"; Chapter 10 "Building Resilient Multi-Region Architectures"*

---

### Disaster Recovery Strategies (Cost ↔ Recovery-Time Trade-off)

Spectrum from cheapest/slowest to most-expensive/instantaneous:

1. **Backup & Restore** — periodic data + config backups. Cheapest; recovery takes hours-to-days.
2. **Pilot Light** — minimal core always running in secondary region; scale up on disaster. Sub-hour-to-hours RTO.
3. **Warm Standby** — scaled-down full copy, kept in sync. Minutes-to-hour RTO.
4. **Multi-Region Active-Active** — both regions serving traffic simultaneously; near-zero downtime. Most expensive.

**Do:**
- Choose by RTO/RPO budget first, then by cost. Don't pick a DR strategy and reverse-engineer numbers.
- Rehearse the strategy. "A well-tested and documented disaster recovery plan is critical" — untested recovery is unreliable recovery.

**Don't:**
- Don't confuse *backups* with a *DR strategy*. Backups protect against data corruption; DR is the whole-environment recovery plan.
- Don't assume the strategy you picked at design time still fits a year later — re-evaluate against current RTO/RPO.

*Ref: Chapter 1 "Disaster Recovery Strategies"*

---

### Defense-in-Depth — Pattern Catalog

Farley-style insight: no single pattern gives resilience. Schwarz presents a clean mapping of patterns to failure categories:

| Challenge | Patterns |
|---|---|
| Resource overload | Load shedding, throttling, auto-scaling, connection pooling (RDS Proxy) |
| Service unavailability | Multi-region, failover, HA databases, SPOF elimination |
| Data issues | Replication, backup/restore, idempotency, CDC |
| Network disruption | Retries, circuit breakers, fallbacks, caching (e.g., CloudFront) |
| Misconfiguration | Infrastructure as Code (CDK), config management |
| Dependency failures | Async architectures, message queues, DLQs |

**Do:**
- Layer the patterns. The next three subsections — idempotency, retries+jitter+circuit-breaker, graceful degradation, timeouts — are *composed*, not alternatives.
- Pick the *simplest* layer that addresses the failure mode first. A retry policy beats a circuit breaker if a one-off transient is the only failure; a circuit breaker beats a thundering-herd retry storm if a dependency flapped.

**Don't:**
- Don't apply a pattern "just in case." Each pattern adds complexity; add only what your failure model demands.
- Don't build patterns that contradict each other (e.g., aggressive retries vs. strict timeouts).

*Ref: Chapter 11 "Putting It All Together" — Reliability Patterns table*

---

### Idempotency — Make Operations Safe to Retry

**Principle:** In distributed/failure-prone systems, the same operation may execute more than once. Operations that change shared state must be *idempotent* — the same input produces the same outcome regardless of how many times it's run.

**AWS Lambda Powertools (Python) idiom:**

```python
from aws_lambda_powertools.utilities.idempotency import idempotent_function

@idempotent_function(
    persistence_store=persistence_layer,  # e.g., DynamoDB-backed
    key_decorator=custom_key_builder
)
def process_account_open(request: dict):
    # Duplicate invocations produce the same result;
    # the persistence layer records "this idempotency key already executed".
    ...
```

**Do:**
- Treat every API endpoint that mutates state as potentially retried — design for idempotency even if the client doesn't retry today.
- Persist idempotency keys in a store synchronized across primary/secondary regions (Aurora Global + DynamoDB Global Tables both serve).
- Include a unique client-side request ID; server stores "seen IDs" for the idempotency window.

**Don't:**
- Don't skip idempotency in financial flows to save time. Duplicate writes ≠ duplicate user accounts.
- Don't rely on "we'll never retry that fast" — at the scale of modern AWS, retries happen in milliseconds.

*Ref: Chapter 4 "Account Open Microservice (Serverless)" — Idempotency; AWS Lambda Powertools*

---

### Retries — Exponential Backoff + Jitter

**Principle:** Transient failures (network blip, cold start, brief throttling) should be retried with **exponential backoff** and **jitter**. Synchronized retry storms kill more systems than the original outage.

**Trade Stock service uses the `retry` library:**

```python
from retry import retry_call

result = retry_call(
    execute_trade,
    fargs=[activity.as_dict()],
    fkwargs={"info": "ip"},
    tries=3,
    backoff=0.2,        # exponential base in seconds
    jitter=0.1,          # random jitter factor
)
```

**Key references:**
- AWS Well-Architected best practice **REL05-BP03**: control and limit retry calls.
- Mark Brooker's "Exponential Backoff And Jitter" — AWS blog post (visual explanation).

**Do:**
- Add retries **with** exponential backoff and jitter by default on any external dependency.
- Combine retries with a circuit breaker (next subsection) — retries alone can overwhelm a struggling dependency.
- Document the retry policy per dependency (count, base, max, jitter).

**Don't:**
- Don't retry non-idempotent operations blindly. Retries must compose with idempotency.
- Don't use a constant backoff — synchronized retries across clients will hammer the recovering dependency in waves.

*Ref: Chapter 5 "Dependency Intermittent Failures"; AWS WELL REL05-BP03*

---

### Circuit Breakers — Stop Calling a Failing Dependency

**Principle:** A circuit breaker wraps a dependency call. When failures cross a threshold, the breaker *opens* and short-circuits all subsequent calls (returning immediately) until a recovery timeout, after which it goes *half-open* to probe recovery.

**Lifecycle:** **Closed** → (failures exceed threshold) → **Open** (short-circuit) → (recovery timeout) → **Half-open** (a few test calls) → success → **Closed** / failure → **Open**.

**Farley-tradable Trade Stock implementation:**

```python
@circuit(failure_threshold=15, expected_exception=ConfirmsMaintenanceError, recovery_timeout=60)
def execute_trade(activity: dict) -> Response:
    # ...
```

**Do:**
- Pair each circuit breaker with retries — retry tolerates gray failures; circuit breakers protect against black (persistent) failures.
- Choose `failure_threshold` and `recovery_timeout` from observed behavior (p95 outage duration × 2-3, etc.), not guesswork.
- Half-open deliberately — a single test call can confirm recovery without flooding the dependency.
- Export the circuit state as a metric so SREs can observe it.

**Don't:**
- Don't open immediately on one failure — a single transient blip shouldn't take the dependency out.
- Don't close on one success during half-open — confirm in batches.
- Don't share a circuit breaker across services with different recovery profiles.

*Ref: Chapter 5 — "Circuit Breaker Pattern" (M. Fowler; AWS design patterns)*

---

### Idempotent Credential Rotation (the `@connection_aware` Pattern)

**Real-world subtlety:** even self-healing patterns need attention. Multiuser secret rotation caches `AWSCURRENT`; *after two consecutive rotations* the original cached password is rotated again, breaking the cached connection.

**Solution:** a Python decorator that catches `OperationalError`, refreshes credentials via `SecretsCache`, and retries once.

```python
def connection_aware(func):
    """Refresh DB connection on rotation indicated by OperationalError."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.OperationalError as e:
            logging.exception("db credentials refreshed; retrying request")
            load_db_engine()
            load_ro_db_engine()
            return func(*args, **kwargs)
    return wrapper

@app.route("/db-health/", methods=["GET"])
@connection_aware
def db_health():
    ...
```

**Do:**
- Wrap DB-touching routes with `@connection_aware` (or an equivalent) so secret rotations are invisible to clients.
- Use **SecretsCache** (SecretCacheConfig) to turn Secrets Manager into a soft dependency — if Secrets Manager is briefly unavailable, the cache lets the service survive.
- Alarm on the `OrderApiDbAuthFailure` metric regardless — repeated failures that don't self-heal are a real signal.

**Don't:**
- Don't hard-depend on Secrets Manager; cache locally with bounded TTL.
- Don't assume multiuser rotation alone covers two consecutive rotations; design for the third.

*Ref: Chapter 5 — "Database Password Rotation Login Failures" — figure 5-8 → 5-10*

---

### Database Resilience — RDS Proxy, Aurora Global, Password Rotation

**Principle:** Databases are the most common source of cascading failure. Treat connection management, failover, and credential rotation as first-class resilience concerns.

**Aurora PostgreSQL built-in fault injection (for chaos testing):**

```sql
trades=> SELECT aurora_inject_crash('node');
WARNING: terminating connection because of crash...
HINT: In a moment you should be able to reconnect...
14:11:17 UTC ... database system is ready   -- ~23 seconds recovery
```

**RDS Proxy connection management:**

```python
proxy = cluster.add_proxy("proxy",
    borrow_timeout=cdk.Duration.seconds(30),
    max_connections_percent=95,
    secrets=[order_api_secret],
    vpc=vpc,
)
```

**Do:**
- Always use RDS Proxy in elastic-compute environments (ECS Fargate, Lambda) — without it, scale-out exhausts connection limits.
- Set `max_connections_percent=95` on RDS Proxy to leave room for admin/scaling.
- Use Aurora's **read-only endpoint** for read-only queries to spread load across readers.
- Rehearse Aurora failover with `aurora_inject_crash`; RDS Proxy will queue writes during the brief write outage.
- For multi-region: prefer **Aurora Global Database** (storage-based replication, subsecond lag) over engine-level replication.

**Don't:**
- Don't compute connection pools assuming you'll have headroom. Measure.
- Don't hard-fail on `OperationalError` — wrap with `@connection_aware` style recovery.
- Don't skip the **reader endpoint** when reads outnumber writes.

*Ref: Chapter 5 — Database Connection Exhaustion; Aurora Global; @connection_aware; Chapter 7 "When Recovery Is Required"*

---

### Coordinated Timeouts — The Cascading-Failure Killer

**Principle:** Timeouts along the call stack must be **coordinated** (each downstream smaller than the upstream's timeout) and **aggregate** (caller's timeout ≥ sum of downstream worst cases × retries).

**Trade Stock call-stack timeouts (canonical example):**

| Layer | Timeout | Notes |
|---|---|---|
| PostgreSQL `statement_timeout` | 100 ms | Hard kill slow queries |
| Trade Confirms (with 3 retries) | 300 ms × 3 = 900 ms worst case | Includes retry budget |
| Gunicorn worker (Trade Confirms) | 1 s | Backend kill timeout |
| Gunicorn worker (Trade Order) | 2 s | |
| API Gateway integration timeout | 2,000 ms | |
| Browser `AbortSignal.timeout()` | 3,000 ms | Client give-up |

```js
// JavaScript / Fetch API
return fetch(import.meta.env.VITE_TRADE_STOCK_ENDPOINT, {
    signal: AbortSignal.timeout(3000),
    method: "PUT",
    mode: "cors",
    cache: "no-cache",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request_json)
});
```

**Do:**
- Make every timeout **strictly smaller** than the next-upstream layer's timeout, with margin.
- Set per-call timeouts in milliseconds; don't use "no timeout."
- Communicate the client-side timeout policy in API docs — clients need to know what to expect.
- For trade/financial flows, prefer letting the user decide when to retry (don't auto-retry from the browser for >3 seconds; show a clear message).

**Don't:**
- Don't set "no timeout" anywhere. Unbounded waits *will* cascade.
- Don't set a downstream timeout larger than the upstream gives up — you'll spend that work for nothing.
- Don't configure a high timeout just to "be safe"; it amplifies outages by tying up resources.

*Ref: Chapter 6 — "Configuring Client Timeouts"; Figure 6-5 "Trade Stock API timeouts"*

---

### Graceful Degradation — Statical Stability > Total Failure

**Principle:** When one feature is unavailable, hide it and inform the user; preserve core functionality. A partial experience retains more trust than a broken UI.

**UI-side heartbeat monitor (Pinia / Vue):**

```js
// useDegradingStore
monitorAccountOpenAvailability() {
    setInterval(this.accountOpenHeartbeat, 5000)  // every 5s
    this.account_open_available = this.accountOpenHeartbeat()
}
```

The pattern separates the control plane (account opening) from the data plane (trading) in the UI itself. When the Account Open API is unhealthy, the form hides and the user is shown: "We'll be back soon. In the meantime you can still place trades ... Call (555) GET-WISE."

**Do:**
- Drive the UI heartbeat from a periodic `OPTIONS` (or cheap probe) call into the dependency.
- Provide a **fallback option** — phone, FAQ, alternate path — to keep trust even if you can't fix the dependency in seconds.
- Couple the UI degradation to a feature flag so product can control rollback speed.

**Don't:**
- Don't show a "spinner-of-doom" for an unhealthy dependency; the user thinks the system is broken.
- Don't degrade core revenue-generating paths; degrade ancillary paths first.
- Don't hard-fail without a recovery signal — the user needs to know when things come back.

*Ref: Chapter 6 — "Gracefully Degrading Features" / Figure 6-9 "New account service unavailable"*

---

### Caching for Resilience (Beyond Performance)

**Principle:** Caching provides resilience *as well as* performance. The tail of latency is what kills user trust, not the average. CloudFront, ElastiCache, and in-process caches all soften the dependency failure profile.

**Soft TTL / Hard TTL Pattern:**
- *Hard TTL* — when the entry expires, serve stale while fetching fresh in the background.
- *Soft TTL* — when stale, refresh synchronously (blocking the request).
Pair them: hard TTL bounds staleness; soft TTL triggers the refresh.

**Do:**
- Implement origin failover with CloudFront origin groups (auto-route to secondary S3 bucket on primary errors — *only* for GET/HEAD/OPTIONS).
- Use request coalescing / single-flight semantics to prevent cache stampedes (thundering herd at the moment of expiry).
- Cache at multiple layers: CDN edge → application cache → dependency cache.

**Don't:**
- Don't cache POST/PUT responses or non-idempotent operations at a CDN.
- Don't set TTL=0 — that defeats the buffer. Even 30 s gives huge resilience benefit.
- Don't ignore stale-while-revalidate; the synchronous-refresh path makes your cache unusable as a resilience buffer.

*Ref: Chapter 3 — "Use the soft TTL/hard TTL pattern" / "Cache resilience"; Figure 3-?*

---

### Rate Limiting (Excessive Load Countermeasure)

**Principle:** When traffic spikes (legit or attack), gracefully degrade by shedding load at the edges rather than letting it overwhelm internal services.

**Patterns:**
- **API Gateway throttling** — account-level and per-API limits.
- **AWS WAF rate-based rules** — block IPs exceeding threshold (e.g., >100 req/s).
- **SQS as buffer** — between ingress and processing; bursts absorb into the queue.

**Do:**
- Set CloudWatch alarms on rate-limit counters — a sustained threshold breach is a signal worth investigating.
- Place rate limits at the *first* controllable choke point (CDN, API Gateway).
- Pair rate limiting with circuit breakers: rate-limit at the edge to protect downstream; circuit-break internally to limit damage from a failing dependency.

**Don't:**
- Don't rate-limit user-visible business APIs without an alternate path. A 429 means nothing if the user can't reach the work.
- Don't set the limit so tight you 429 real users during a legitimate burst.

*Ref: Chapter 3 — "Failure Mode 1: Excessive Load"; AWS WAF + API Gateway*

---

### Self-Healing via SQS + Lambda + DLQ for "Poison Pills"

**Principle:** Async work queues (SQS) provide automatic retries with `maxReceiveCount` and a Dead Letter Queue for messages that fail repeatedly ("poison pills"). Lambda's event-source mapping polls SQS and dispatches to your handler; persistent failures land in the DLQ for human inspection.

**Do:**
- Configure `maxReceiveCount` deliberately (3-5 typical) and an alarm on DLQ depth.
- Treat the DLQ as an *operational signal*, not a parking lot — alarm and process it.
- For controlled chaos: introduce a forced failure (e.g., misconfigured connection string) and watch the retry/DLQ cycle execute.

**Don't:**
- Don't let messages spin forever — set a hard ceiling.
- Don't ignore DLQ depth. A growing DLQ during a deploy is the *first* signal something is wrong.
- Don't put unlimited data into messages; large payloads break scaling and ordered processing assumptions.

*Ref: Chapter 4 "Surviving Poison Pills"; SQS retries*

---

### Zonal Shift — Surgical Evacuation of an Impaired AZ

**Principle:** When a single AZ is degraded, route traffic away from it without touching the other AZs. The system self-heals once the impaired AZ recovers.

```bash
aws arc-zonal-shift start-zonal-shift \
    --away-from us-east-1b \
    --duration 20m
```

**Pre-requisites:**
- Cross-zone load balancing **disabled** on the target group (otherwise the ALB keeps spreading traffic across the impaired AZ).
- AZ-dimensioned metrics on every important signal (`OrderApiDbAuthFailure`, request volume, error rate, etc.) so the on-call can see which AZ is the problem.

**Do:**
- Make AZ-level observability the default — add `AvailabilityZone` to every important metric dimension.
- Pre-build the zonal-shift runbook during normal operations (IAM, command, expected outcomes).
- Use zonal shift for *short* impairments (<30 min) — longer means promotion to a fuller failover.

**Don't:**
- Don't mix zonal shift with multi-region failover; pick the right escalation.
- Don't disable cross-zone load balancing without first confirming all targets can absorb full load from the remaining AZs.

*Ref: Chapter 5 — "Availability Zone Impairments"; AWS FIS experiment template `aws:network:disrupt-connectivity`*

---

### Chaos Engineering — Test What You Cannot Reason About

**Principle:** Complex distributed systems have failure modes you cannot reason about statically. Inject failures to discover them before users do.

**AWS FIS experiment template example (Chapter 5):** disrupt connectivity to a single subnet in a single AZ — observe the recovery, observe which metrics alert, observe what stays up.

**Do:**
- Start with the *simplest* experiment that touches the most important failure mode (network partition in one AZ).
- Run experiments with traffic flowing so you observe real production-like behavior.
- Pair every chaos experiment with **observability**: pre-define the metrics you expect to alert, then confirm they do (and only those you expect).
- Reuse experiments as regression tests in the CI/CD pipeline after stabilization.

**Don't:**
- Don't run chaos on production *first* and untested. Run on a non-prod environment with realistic load first.
- Don't stop injecting once one experiment passes — failure modes evolve with the system.
- Don't let chaos be a one-off exercise; institutionalize it as part of the deployment lifecycle.

*Ref: Chapter 1 "Continuous Testing and Chaos Engineering"; Chapter 5 "Availability Zone Impairments"; Chapter 8 "Testing Resilience with AWS FIS"*

---

### Multi-Region Streaming & Search (Distributed Consistency Decisions)

**Patterns:**
- **Aurora Global Database** — storage-based cross-region replication, subsecond lag, up to 15 secondary clusters. Switchover (planned, no data loss) vs. failover (emergency, possible data loss).
- **DynamoDB Global Tables** — automatic multi-region replication; LWW or custom conflict resolution via Lambda.
- **Kafka MirrorMaker** — replicates between regional clusters; active-active needs custom conflict resolution and careful consumer-group design.
- **OpenSearch CCR** — unidirectional (simpler) or bidirectional (writes accepted in multiple regions, conflict resolution required).
- **Caching in multi-region:** regional cache clusters (low latency, sync required) / global cache w/ replication / hybrid.

**Do:**
- Use **switchover** for planned events, **failover** only for emergencies — they have different data-loss profiles.
- Use **Aurora Global Database** for OLTP cross-region; it propagates DDL faster than engine-level replication.
- Reconcile after failover with RPO > 0 via checksums, journaling, timestamp compare, or application-level reconciliation.

**Don't:**
- Don't assume replicated = identical. With any async replication, RPO > 0. Reconcile or design for it.
- Don't over-engineer for global active-active if regional active-passive meets the SLO; cost is quadratic.

*Ref: Chapter 7 "When Recovery Is Required"; Chapter 10 "Multi-Region Architectures"*

---

### Observability as a Resilience Enabler

**Three pillars (each is a window into the system):**
- **Logs** — chronological, detailed, per-event.
- **Metrics** — aggregated, numeric, time-series.
- **Traces** — request flow across components.

**Composite alarms** — combine low-level signals into a single "is the system healthy?" indicator to avoid alert fatigue.

**Tooling that operationalizes this on AWS:**
- **CloudWatch Synthetics (Canaries)** — proactive synthetic monitoring at the page/API level; bridges the gap between system-reported health and real user experience.
- **CloudWatch RUM (Real User Monitoring)** — actual user telemetry including JS errors and Core Web Vitals (LCP, CLS, INP).
- **AWS X-Ray** — distributed tracing across services; integrated with CloudWatch RUM for end-to-end visibility.
- **Composite alarms** — to prevent alarm storms (one underlying failure → dozens of alerts).

**Do:**
- Tag metrics with `AvailabilityZone` so zonal degradations are visible.
- Add `condition_expression` style filters to metric alarms to avoid spurious alerts during known noise (e.g., planned deploys).
- Couple alarms to *runbooks*, not phone numbers, when possible.

**Don't:**
- Don't alert on every transient — alert on symptoms (error budget burn), not causes.
- Don't forget the frontend — RUM and Core Web Vitals matter for user experience.
- Don't rely on a single layer of telemetry — combine logs/metrics/traces plus synthetic checks and real-user checks.

*Ref: Chapter 3 — "Observability with Synthetic Monitoring"; Chapter 6 — "Real User Monitoring"; Chapter 11*

---

### Infrastructure as Code — Change Management

**Principle:** Resilience requires predictable, reviewable, repeatable infrastructure changes. Treat infrastructure like code: check it into Git, review it, test it.

**AWS CDK + grant mechanisms:**
- IAM policies are auto-generated from `grant_*` calls — principle of least privilege by construction.
- Multi-stack CDK apps evaluate stacks in dependency order; outputs feed downstream stacks.
- Snapshots on `cdk destroy` protect databases from accidental data loss.

**Do:**
- Version every infrastructure change. PRs in Git, reviews like code.
- Use CloudFormation deletion policies on data resources (`"Snapshot"`) to prevent accidental data loss on teardown.
- Use Systems Manager Automation documents for orchestrated failover (Aurora switchover → lambda signal → Route 53 health-check update).

**Don't:**
- Don't click around the console for production changes.
- Don't deploy a service stack without first defining its policy and metrics.

*Ref: Chapter 1 "Change Management"; Chapter 5 — "Deployment Circuit Breakers" (ECS)*

---

### Identity, Encryption, and Cross-Region Auth

**Recommendations:**
- **Encryption in transit** — TLS everywhere; ACM-managed certs with automatic rotation.
- **Encryption at rest** — prefer Customer Managed Keys (CMK) over AWS-managed defaults for sensitive data.
- **Authentication** — Cognito doesn't natively replicate identity across regions; use Route 53-based multi-region with identity-provider federation if multi-region matters.
- **Tokenization** — for PCI-DSS scopes.

*Ref: Chapter 2 "Security Considerations"*

---

## Anti-Patterns & Common Mistakes

- **"We have an SLA, so we're fine":** AWS SLAs are baseline; you need your own SLOs and error budgets. → *fix:* define SLOs aligned to business impact; track error budgets.
- **Mistake: relying on averages for latency.** → *fix:* use percentile/heatmap analysis; mean and p99 can diverge wildly.
- **Mistake: testing only the happy path.** → *fix:* routinely inject failures; rehearse failover; run chaos in CI/CD.
- **Mistake: hard-depending on a single AZ/database/secret.** → *fix:* layers of redundancy + RDS Proxy + multiuser secret rotation + multiuser rotation-handling code.
- **Mistake: coordinated timeouts all set "high" or all set "low."** → *fix:* down-the-stack coordination with the table from Chapter 6.
- **Mistake: no graceful degradation.** → *fix:* heartbeats + flag-driven UI degradation + alternate paths.
- **Mistake: deploying with manual steps.** → *fix:* automation; deployment must be reproducible from code.
- **Mistake: ignoring the DLQ.** → *fix:* alarm on DLQ depth; treat DLQ growth as a real operational signal.
- **Mistake: sharing code across pipelines or services.** → *fix:* DRY within pipeline; tolerate duplication across pipelines.
- **Mistake: testing in production without a strategy.** → *fix:* feature-flag activation strategies (internal users, percentage rollout, by-segment).
- **Mistake: alert fatigue from per-component alarms.** → *fix:* composite alarms; alert on user-impacting symptoms, not component blips.

## Decision Heuristics / Checklists

- **Picking a DR strategy:** What is your RTO/RPO budget? Pick the cheapest strategy that fits.
- **Picking an AZ count:** Default to at least 2 (active-active pairs); 3 if your latency budget is tight and you have headroom.
- **Picking a database tier:** Need multi-region RPO < 1 minute? Aurora Global. Need multi-region active-active with conflict resolution? DynamoDB Global Tables. Single region HA? Aurora Multi-AZ.
- **Picking a circuit breaker threshold:** Start at 10-15 consecutive failures or ~1% failure rate over a sliding window; tune from observed data.
- **Picking a retry policy:** Always exponential backoff with jitter. Cap `tries` at 3-5. Pair with idempotency.
- **Picking a timeout:** `downstream_timeout` < `upstream_timeout`; `caller_timeout` > `sum(downstream_timeout × max_tries)`.
- **Picking a chaos experiment:** Start with single-AZ network impairment; measure recovery; only expand blast radius once familiar.
- **Picking an error budget:** SLO-based; page when burn rate exceeds 2× the steady-state burn; warn on 1×.
- **Picking a sync boundary:** If a process boundary's network call can fail, it WILL fail. Prefer async, events, queues.
- **Picking whether to multi-region:** "Does the business case justify the operational cost?" If not, multi-AZ is enough.

## Key Takeaways

1. **Resilience is design + shared responsibility.** Use SEEMS to enumerate failure modes; AWS does its part, you do yours.
2. **Set RTO/RPO first, engineer second.** Unconstrained design produces over-built or under-built systems.
3. **Layer defenses.** Retries + circuit breakers + idempotency + timeouts + degradation + multi-region — composed, not alternative.
4. **Coordinated timeouts prevent cascade failures.** Use the table format from Chapter 6.
5. **Always-retry = amplify outage.** Always-retry-with-backoff+jitter+idempotency+circuit-breaker = resilience.
6. **Test it.** Rehearsed failover is reliable; paper-only failover is wishful thinking.
7. **Graceful degradation beats total failure.** Hide, inform, preserve core.
8. **Databases break most often.** RDS Proxy + Aurora Global + SecretsCache + multiuser rotation handling.
9. **Cache for resilience, not just performance.** CloudFront origin failover, soft/hard TTL, request coalescing.
10. **Multi-region is not free.** Active-passive covers most; only go active-active when the SLOs demand it.
11. **Composite alarms > per-component alarms.** Fewer, higher-signal alerts reduce toil and speed response.
12. **Failover ≠ switchover.** Different data-loss profiles; rehearse both.
13. **DLQs are operational signals.** Alarm on them.
14. **Async reduces coupling.** Sync across process boundaries is a leaky abstraction.

## Cross-References
- Related: [[../Observability_Engineering.md]] (the observability pillars underly every resilience diagnostic here)
- Related: [[../Continuous_Deployment.md]] (CD exposes every weakness; resilience patterns are what makes CD survivable)
- Related: [[../Modern_Software_Engineering.md]] (the complexity principles explain why boundary design matters for resilience)
- Topic index: [[../INDEX.md]]
