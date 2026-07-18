# Engineering Resilient Systems on AWS — Best Practices Deep Dive

> Deep-dive extracted from the O'Reilly book *Engineering Resilient Systems on AWS* by Kevin Schwarz, Jennifer Moran, and Nate Bachmeier (O'Reilly, 2024, ISBN 978-1-098-16242-9). Every pattern below is grounded in the book's hands-on "AvailableTrade" brokerage example and quoted source. All code/Python/YAML/JSON snippets are verbatim from the book or its companion GitHub repository. References cite the section heading as it appears in `Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md`.

**Author:** Kevin Schwarz, Jennifer Moran, Nate Bachmeier
**Topic tags:** `#architecture` `#general` `#cloud` `#reliability`
**Language focus:** Python-first (CDK + Lambda), with SQL, YAML, JSON, JavaScript (Vue.js)
**Sources:** `markdown_output/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md` · `summaries/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md`

---

## TL;DR

This book is a hands-on, end-to-end playbook for engineering resilience on AWS using a fictitious brokerage ("AvailableTrade"). It centers the **AWS Resilience Analysis Framework (RAF)** with its **SEEMS** failure-mode taxonomy (Single point of failure, Excessive load, Excessive latency, Misconfigurations/bugs, Shared fate), ties every pattern to a concrete failure mode, and progressively builds defenses — CloudFront origin failover + WAF rate limiting, serverless fire-and-forget with Lambda Powertools idempotency + SQS + DLQ, ECS deployment circuit breakers, Aurora max_connections discipline + RDS Proxy + Secrets Cache + `@connection_aware` self-healing decorator, retries-with-jitter + circuit-breaker lifecycle, end-to-end coordinated timeout stacks, graceful degradation with heartbeats, CloudWatch RUM + X-Ray, the **STOP (Standby Takes Over Primary)** regional switchover pattern orchestrated by SSM Automation, multi-region Aurora Global + DynamoDB Global Tables + Route 53 health-check failover + zonal shift via AWS FIS, and streaming patterns (Kafka partitions/rebalancing, poison pills + DLQ, optimistic vs pessimistic concurrency, Producer-Consumer with Redis leader election, Bulkhead + EventBridge, CDC+CQRS, Kafka MirrorMaker, OpenSearch CCR, multi-region caching, CAP/PACELC, anti-fragility). Apply when you are building customer-facing, regulated, or revenue-critical workloads on AWS where bounded recovery time matters more than absolute availability.

---

## Best Practices by Topic

### Cluster 1 — AWS Shared Responsibility Model for Resilience

**Principle:** Resilience is a shared contract: AWS guarantees "of the cloud" (physical data centers, AZs, regions, regional service SLAs), customers own "in the cloud" (architecture, configuration, data, recovery processes).

**Do:**
- Map every workload to the **AWS Well-Architected Framework**'s six pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability).
- Layer customer-managed resilience on top of AWS-managed fault isolation boundaries (regions, AZs, control planes).
- Establish a Business Impact Analysis (BIA) and a risk assessment *before* setting resilience goals.

**Don't:**
- Treat AWS SLAs as your resilience target — they are baselines that must be complemented with business-aligned RTO/RPO.
- Assume managed services are infinitely resilient; configure multi-AZ, backup, and failover yourself.
- Skip documenting cross-team dependencies in the Shared Responsibility Model.

**Code:**
```text
# AWS Region / AZ hierarchy (from the book's Fig 1-2 mental model)
Region
└── Availability Zone 1 (independent power, cooling, networking)
└── Availability Zone 2
└── Availability Zone N
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Shared Responsibility Model", "AWS Responsibility", "Customer Responsibility"*

---

### Cluster 2 — Recovery Objectives: RTO, RPO, BRT, Downtime

**Principle:** Define bounded recovery commitments tied to the business impact of downtime, not to what is technically convenient.

**Do:**
- Use **RTO** (Recovery Time Objective — max acceptable downtime) and **RPO** (Recovery Point Objective — max acceptable data age lost) for *every* critical service.
- Establish a **Bounded Recovery Time (BRT)** as the hard target — a commitment to recover within a specific timeframe.
- Convert business expectations into measurable thresholds: "downtime" includes error-rate breaches and latency over SLO, not just outages.

**Don't:**
- Pick RTO/RPO from defaults — derive them from a BIA + risk assessment.
- Treat RTO as a single number; tie it to specific user journeys and tiers.
- Define "downtime" as binary up/down — most modern systems degrade gradually.

**Code (example from the book for AvailableTrade):**
```text
System logs reveal:
- MTBF: 2 weeks (336 hours)
- MTTR: 2 hours
- Recovery objective (RTO): 4 hours (1x MTTR buffer)
- BRT target: 1 hour (to minimize financial impact)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Recovery objectives", "Bounded Recovery Time (BRT)"*

---

### Cluster 3 — The Three Ms: MTBF, MTTD, MTTR

**Principle:** Track three time-based metrics to drive continuous improvement: Mean Time **Between** Failures, Mean Time **To Detect**, Mean Time **To Repair/Recovery**.

**Do:**
- Baseline historical MTBF/MTTD/MTTR before setting goals.
- Set improvement targets: **raise MTBF**, **shorten MTTD**, **shorten MTTR**.
- Use MTTR trends to inform your BRT — if MTTR is 30 min, a 15 min BRT is unrealistic.
- Couple MTBF + MTTD with recovery objectives to set realistic RTOs.

**Don't:**
- Optimize one M in isolation (e.g., low MTTD with high MTTR means fast alerts and slow fixes).
- Use averages without confidence intervals; outlier incidents skew the mean.

**Code (relationship on an availability timeline):**
```text
|--- MTBF (uptime between incidents) ---| X |--- MTTD ---|--- MTTR ---|
                                          failure detected          recovered
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "The three Ms"*

---

### Cluster 4 — Resilience Analysis Framework (RAF) and the SEEMS Model

**Principle:** Categorize every failure mode with the SEEMS taxonomy to ensure your defenses map to the property they violate.

**Do:**
- Use RAF's five resilience properties as the audit checklist: **redundancy**, **sufficient capacity**, **timely output**, **correct output**, **fault isolation**.
- Use **SEEMS** to categorize every failure:
  - **S**ingle point of failure (SPOF) → violates redundancy
  - **E**xcessive load → violates sufficient capacity
  - **E**xcessive latency → violates timely output
  - **M**isconfigurations and bugs → violates correct output
  - **S**hared fate → violates fault isolation
- Apply preventive, detective, and corrective controls for each SEEMS category.

**Don't:**
- Treat SEEMS as a one-time checklist — re-run it whenever architecture changes.
- Confuse "S" #2 (excessive latency) with "S" #5 (shared fate) — keep both E's distinct.

**Code (SEEMS cheat sheet):**
```text
Property Violated     SEEMS Category         Typical Mitigations
-----------------     --------------         ------------------
Redundancy            Single Point of Failure  Multi-AZ, replicas, failover, OAC
Sufficient Capacity   Excessive Load          WAF, throttling, autoscaling, queues
Timely Output         Excessive Latency       Caching, timeouts, retries+backoff, CDN
Correct Output        Misconfigurations/Bugs  IaC, JSON Schema, deployment circuit breakers
Fault Isolation       Shared Fate             Bulkheads, regional/AZ partitioning, sharding
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "AWS Resilience Analysis Framework", "AWS Well-Architected Framework"*

---

### Cluster 5 — Disaster Recovery Strategies (Backup/Restore → Multi-Region Active-Active)

**Principle:** Match DR strategy to business criticality — cost and complexity grow with each tier.

**Do:**
- Choose deliberately across the four strategies:
  1. **Backup and Restore** — cheapest, longest RTO. For non-critical workloads.
  2. **Pilot Light** — minimal core always on; scale on disaster. Mid-cost, mid-RTO.
  3. **Warm Standby** — scaled-down replica. Lower RTO than pilot light at higher cost.
  4. **Multi-Region Active-Active** — fastest RTO (near-zero), highest cost and complexity.
- Treat DR as a **process + people** concern, not just infrastructure. Rehearse it.

**Don't:**
- Confuse "data backup" with "backup and restore strategy" — backups are one component; recovery is the whole process.
- Skip testing the DR runbook until a real disaster — untested plans fail.
- Default to active-active when multi-AZ within one region suffices.

**Code (DR strategy comparison):**
```text
Strategy            Cost    RTO          Use case
------------------  ------  -----------  --------------------------------
Backup/Restore      $       hours-days   Non-critical, compliance-only
Pilot Light         $$      minutes-hrs  Important but tolerates downtime
Warm Standby        $$$     minutes      Important, downtime is costly
Multi-Region A/A    $$$$    seconds      Mission-critical, revenue-impacting
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Disaster recovery strategies"*

---

### Cluster 6 — High Availability: Redundancy and Self-Healing

**Principle:** HA focuses on preventing/minimizing downtime from small failures; DR handles large-scale events. Use both.

**Do:**
- Build self-healing: ECS task replacement, RDS failover, Aurora read replica promotion.
- Use horizontal scalability and centralized monitoring with real-time alerting.
- Apply redundancy across AZs and (where needed) regions.

**Don't:**
- Conflate HA and DR — they have different objectives and tools.
- Rely on vertical scaling for HA — it caps at hardware limits.

**Code (HA pattern for a service):**
```text
ALB (multi-AZ)
├── ECS Task AZ-a (healthy)
├── ECS Task AZ-b (healthy)
└── ECS Task AZ-c (healthy)
    ↓ unhealthy
   ECS replaces task; ALB stops routing
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "High availability"*

---

### Cluster 7 — Quotas and Service Limits

**Principle:** Exceeding AWS service quotas is a "shared fate" failure mode; treat quotas as code.

**Do:**
- Continuously monitor usage with CloudWatch + CloudTrail.
- Set alarms that trigger **automatic quota-increase requests** via the Service Quotas API.
- Tag resources by priority/business unit to allocate quotas intentionally.

**Don't:**
- Treat default quotas as sufficient for production.
- Wait until throttling to discover quota limits.

**Code (monitoring and auto-increase pattern):**
```python
# Pseudocode for quota management
import boto3
quotas = boto3.client("service-quotas")
current = quotas.get_service_quota(ServiceCode="lambda", QuotaCode="L-B99A9384")
if current["Quota"]["Value"] * 0.8 < current_usage:
    quotas.request_service_quota_increase(
        ServiceCode="lambda",
        QuotaCode="L-B99A9384",
        DesiredValue=int(current["Quota"]["Value"] * 1.5)
    )
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Quotas"*

---

### Cluster 8 — Change Management for Resilience

**Principle:** Most outages are self-inflicted. A formal change control process prevents the largest category of incidents.

**Do:**
- Require documented rationale, implementation details, and risks for every change.
- Mandate **rollback plans** or **fix-forward / isolation / degradation** alternatives.
- Use **two-person verification** for manual changes that cannot be automated.

**Don't:**
- Allow ad-hoc changes during incidents without post-change review.
- Skip change documentation because "it's small."

**Code (change control template, paraphrased from book):**
```text
Change Request:
- Rationale:        <why>
- Implementation:   <steps>
- Risks:            <downtime, data loss, security>
- Rollback plan:    <documented and tested>
- Verifier:         <two-person rule>
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Change Management"*

---

### Cluster 9 — Failure Management with Response Playbooks

**Principle:** Response is a process, not a hero. Codify it with playbooks and automation.

**Do:**
- Define monitoring thresholds and alarms per failure type.
- Author **response playbooks** cross-functionally; define escalation paths.
- Automate remediation: restart, reallocate, rollback, failover.
- Run **tabletop exercises and simulations** to validate the system.
- Perform blameless **Root Cause Analysis (RCA)** after every incident.

**Don't:**
- Rely on tribal knowledge ("ask Alice, she knows").
- Skip post-incident reviews because "we fixed it."

**Code (failure management flow):**
```text
metric threshold breached
  → alarm fires → SNS notify
    → on-call runs playbook OR Lambda auto-remediates
      → resolve
        → RCA within 5 business days
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Failure Management"*

---

### Cluster 10 — Observability: Logs, Metrics, Traces

**Principle:** You cannot be resilient to what you cannot see. Three pillars — **logs**, **metrics**, **traces** — must coexist.

**Do:**
- Capture all three pillars for every service.
- Use metrics for trend alerts, logs for context, traces for cross-service latency.
- Power **postmortems** with logs+metrics+traces from the incident window.
- Apply metrics as early-warning — they detect degradation before user-visible failure.

**Don't:**
- Skip traces for synchronous multi-service flows.
- Log at INFO in production for hot paths — use structured JSON with sampling.

**Code (three pillars — when to use which):**
```text
Pillar    Use for                          Example
-------   ----------------------------     --------------------------------
Logs      Chronological debugging          "Order rejected at 12:04:33 by validator"
Metrics   Trend, threshold alerting        "p99 latency 480ms > 200ms SLO"
Traces    Cross-service latency            "API Gateway → SNS → SQS → Lambda took 720ms total"
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Observability"*

---

### Cluster 11 — Continuous Testing and Chaos Engineering

**Principle:** Resilience is perishable; you must continuously test it. Chaos engineering is resilience's empirical laboratory.

**Do:**
- Run traditional unit/integration/regression tests in CI/CD.
- Start chaos experiments **small** (one instance termination) → grow complex.
- Define clear **hypotheses and metrics** for each experiment.
- Implement **blast-radius controls**; stop conditions; safety halts.
- Use **AWS Fault Injection Service (FIS)** for managed, in-AWS chaos.

**Don't:**
- Run chaos experiments without hypotheses — you learn nothing.
- Skip blast-radius controls "just this once."
- Treat chaos as production-only — pre-prod chaos is acceptable and lower-risk.

**Code (FIS experiment template — MSK broker terminate):**
```python
# Verbatim from Ch 8 testing section
experiment = fis.CfnExperiment(
    self, "MyFISExperiment",
    experiment_template=fis.CfnExperimentTemplate(
        actions={
            "terminate-msk-broker": fis.CfnExperimentTemplate.ExperimentTemplateAction(
                action_id="aws:msk:broker-terminate",
                description="Terminate an MSK broker",
                parameters={
                    "brokerIds": ["<REPLACE_WITH_BROKER_ID>"],
                    "clusterArn": "<REPLACE_WITH_CLUSTER_ARN>",
                },
            ),
        },
        stop_conditions=[fis.CfnExperimentTemplate.ExperimentTemplateStopCondition(
            source="none", value="PT10M"
        )],
        targets={
            "msk-cluster": fis.CfnExperimentTemplate.ExperimentTemplateTarget(
                resource_type="AWS::MSK::Cluster",
                resource_targets=<broker ids>,
            ),
        },
        role_arn=<FISRole.arn>,
    ),
)
```

**FIS best-practice guidance (from book):**
- Simplified experiments (managed service).
- Safe fault injection (scoped).
- Comprehensive insights (metrics).
- Automated chaos testing (CI/CD).
- Scalable across accounts/regions.

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Continuous Testing and Chaos Engineering", "Testing Resiliency" (Ch 8)*

---

### Cluster 12 — CI/CD and Automation Discipline

**Principle:** Standardize, repeat, and audit. Variability is the enemy of resilience.

**Do:**
- Commit code frequently; automate unit + integration + end-to-end tests.
- Use **immutable infrastructure patterns** (rebuild, don't mutate).
- Sequence **configure → build → test → deploy** in pipelines.
- Embed security testing (SAST/DAST) in the pipeline.

**Don't:**
- Allow manual deployment to production.
- Reuse mutable AMIs / golden images — replace them.

**Code (CDK stack dependency orchestration):**
```python
# AvailableTrade style: stacks are evaluated in dependency order
app = cdk.App()
secondary_bucket = FrontEndSecondaryBucketStack(app, "FrontEnd-BucketStack-Secondary",
    env=secondary_environment)
website_stack = FrontEndWebsiteStack(app, "FrontEnd-WebsiteStack",
    env=primary_environment, secondary_region=..., domain_name=...)
canary_primary = FrontEndCanaryStack(app, "FrontEnd-CanaryStack-Primary",
    env=primary_environment, endpoint_url=website_domain_name)
canary_secondary = FrontEndCanaryStack(app, "FrontEnd-CanaryStack-Secondary",
    env=secondary_environment, endpoint_url=website_domain_name)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "CI/CD and Automation", "Deploying the AWS CDK Application"*

---

### Cluster 13 — CloudFront + S3 Origin Failover (Single Point of Failure mitigation)

**Principle:** Eliminate the S3 origin as a SPOF by configuring **origin groups** in CloudFront with Origin Access Control (OAC).

**Do:**
- Always pair CloudFront with **multiple S3 origins** (primary + secondary, ideally in different regions).
- Enable **Origin Access Control (OAC)** to restrict direct S3 access — SigV4-authenticated, only CloudFront can read.
- Use origin group failover for `GET`, `HEAD`, `OPTIONS` requests only.
- Configure **failover criteria** on specific HTTP error codes (e.g., 500/403).

**Don't:**
- Rely on CloudFront alone if the origin is a SPOF — you need origin failover.
- Allow public S3 access when CloudFront is in front.
- Assume origin failover is instant — CloudFront **always tries the primary first**, even when it's known to be impaired.

**Code (origin group failover setup — book procedure):**
```text
CloudFront distribution
├── Behavior (default) → Origin Group
│   ├── Primary origin (S3 primary-region bucket)
│   └── Failover origin (S3 secondary-region bucket)
└       Failover criteria: select all relevant HTTP error codes
```

**S3 bucket policy allowing CloudFront OAC (denying all other access):**
```json
{
  "Effect": "Allow",
  "Principal": { "Service": "cloudfront.amazonaws.com" },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::<your-bucket-name>/*",
  "Condition": {
    "StringEquals": {
      "AWS:SourceArn": "arn:aws:cloudfront::<AWS_ACCOUNT_ID>:distribution/<DISTRIBUTION_ID>"
    }
  }
}
```

> "Amazon CloudFront origin failover is a feature that can help mitigate disruptions caused by origin failures. It allows you to automatically reroute requests to an alternate origin server if your primary origin becomes unavailable. However, it's important to note that Amazon CloudFront will only failover for specific HTTP error responses and only for `GET`, `HEAD`, or `OPTIONS` requests."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Addressing Single Points of Failure", "Implementing Amazon CloudFront origin failover"*

---

### Cluster 14 — CloudFront Caching for Resilience (not just performance)

**Principle:** Caching at the edge is a **resilience** control — it buffers against origin failures and tail-latency spikes.

**Do:**
- Set appropriate TTLs based on content change cadence.
- Implement the **soft TTL / hard TTL** pattern: refresh at soft TTL, but serve stale until hard TTL if origin is unavailable.
- Use **request coalescing** to prevent thundering-herd cache stampedes.
- **Cache warming** for predictable traffic events.
- Monitor cache hit rate, error rate, latency distribution.

**Don't:**
- Treat caching as purely a performance tool — the book emphasizes: *"the true value in resilience lies in its ability to ensure consistent latency, even at the tail end of your request distribution."*
- Serve stale data without a hard TTL ceiling.
- Forget to invalidate cache when testing origin failures.

**Code (cache miss vs hit on the same large file):**
```text
# Cold (cache miss) — origin fetched
x-cache: Miss from cloudfront
{ [16026 bytes data] 100 214M 100 214M 0 0 46.1M 0 0:00:04 }

# Warm (cache hit) — served from edge
x-cache: Hit from cloudfront
age: 13
{ [32387 bytes data] 100 214M 100 214M 0 0 183M 0 0:00:01 }
```

> "Even if your origin server (the S3 bucket) became temporarily inaccessible, your users would still be able to retrieve the file."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Balancing caching and resilience for consistent latency", "Observing the impact of caching on resilience"*

---

### Cluster 15 — AWS WAF Rate Limiting (Excessive Load mitigation)

**Principle:** Push back on excessive load at the edge with WAF **rate-based rules** before traffic reaches your origin.

**Do:**
- Create WAF **rate-based rule groups** keyed on IP address, with thresholds like 100 req/sec.
- Attach the rule group to the WebACL **and** to the CloudFront distribution.
- Set CloudWatch alarms on **BlockedRequests** metric to know when throttling fires.

**Don't:**
- Rely on origin throttling as your only defense — by then, you have already paid origin-compute costs.
- Set the rate too low — it will block legitimate users.

**Code (rate-limit rule on WAF):**
```text
WAF WebACL
└── RateLimitRuleGroup
    └── RateLimitRule  →  Block requests > 100/sec from same source IP
```

**Artillery.io load injection (test pattern from book):**
```yaml
# website-load-test.yml
config:
  phases:
    - duration: 60  # warm-up for initial scaling
      arrivalRate: 5
    - duration: 120 # ramp-up to steady state
      arrivalRate: 25
      rampTo: 50
    - duration: 60  # spike phase
      arrivalRate: 100
scenarios:
  - flow:
      - get:
          url: "{url}"
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Preventing excessive load with rate limiting", "Implement AWS Web Application Firewall with rate limiting"*

---

### Cluster 16 — CloudWatch Synthetics Canaries for Differential Observability

**Principle:** Synthetic monitoring bridges the gap between **system-reported health** and **actual user experience**.

**Do:**
- Deploy canaries in **both primary and secondary regions**.
- Always associate canaries with alarms tied to **SNS topics** for human notification.
- Use canaries for proactive change validation before full rollout.

**Don't:**
- Skip canary alarms because "we'll see it in metrics" — canaries catch what metrics miss.
- Run canaries only in production — pre-prod canaries prevent regressions.

**Code (canary benefit matrix — from book):**
```text
Benefit                  What it solves
-----------------------  -------------------------------------------------
Differential observability System vs user experience discrepancies
Proactive issue detection  Subtle degradations before user impact
Resilient infrastructure  Multi-region monitoring redundancy
Validation of changes     Test new releases before exposing users
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Implementing Observability"*

---

### Cluster 17 — Synchronous vs Asynchronous Request Flow (Fire-and-Forget)

**Principle:** Decouple HTTP receipt from business processing with **fire-and-forget** queues to keep API responses fast and avoid cascading failures.

**Do:**
- Use **API Gateway → SNS → SQS → Lambda** for control-plane operations (e.g., account opening).
- Return HTTP 200 as soon as the message is durably captured in the queue.
- Provide a callback or polling mechanism for completion notification.

**Don't:**
- Block the HTTP response on long-running work — tail latency kills availability.
- Mix synchronous and async patterns without clear contracts.

**Code (synchronous vs asynchronous request flow — book Fig 4-1 vs 4-2):**
```text
Synchronous (data plane):
Client → API Gateway → Lambda → DB → Response → Client
[blocked for entire transaction]

Asynchronous (control plane / fire-and-forget):
Client → API Gateway → SNS → SQS → (200 OK) → Client
                            ↓
                          Lambda (process out-of-band)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Technical Requirements" (Ch 4), "Architecture Overview: An AWS Serverless Approach"*

---

### Cluster 18 — Lambda Powertools Idempotency (verbatim)

**Principle:** Make every mutating endpoint **idempotent** — duplicate requests (retries, network glitches) must produce exactly one outcome.

**Do:**
- Use Lambda Powertools `idempotent_function` decorator with `event_key_jmespath` keyed on a client-supplied `request_token` UUID.
- Backed by a **DynamoDB global table** for cross-region idempotency tracking.
- Set `expires_after_seconds` to bound the idempotency window (the book uses 3 hours via DynamoDB TTL).
- Document the API contract: use **HTTP PUT** to signal idempotency to consumers.
- Include `DynamoDB ReplicationLatency` and `PendingReplicationCount` in observability since cross-region idempotency is only reliable **within a region** due to eventual consistency.

**Don't:**
- Rely on idempotency across regions during steady state without accounting for replication lag.
- Use SQS FIFO when ordering is not required — standard queues are cheaper and idempotency + retries handle duplicates.

**Code (verbatim from book — idempotency setup):**
```python
from aws_lambda_powertools.utilities.idempotency import (
    idempotent_function, IdempotencyConfig, DynamoDBPersistenceLayer, DataclassSerializer
)

persistence_store = DynamoDBPersistenceLayer(table_name="idempotency_table")
config = IdempotencyConfig(
    event_key_jmespath="request_token",   # match on the client-supplied UUID
    expires_after_seconds=60 * 60 * 3,   # 3 hours
)

@idempotent_function(
    data_keyword_argument="account_event",
    config=config,
    persistence_store=persistence_store,
    output_serializer=DataclassSerializer,
)
def create_brokerage_account(account_event: dict):
    # ... business logic ...
    return {"account_id": "...", "status": "submitted"}
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Idempotent Responses"*

---

### Cluster 19 — SQS Self-Healing Retries + DLQ (Poison Pills)

**Principle:** SQS + Lambda ESM gives you **retries with backoff** for transient errors and **DLQ sideline** for poison pills.

**Do:**
- Set SQS `visibility_timeout = 6 × Lambda timeout` when `report_batch_item_failures=True` (book's hard rule).
- Configure `max_receive_count` on the DLQ so poison pills don't loop forever.
- Enable `report_batch_item_failures` so partial failures don't replay the whole batch.
- Set `max_concurrency` on the ESM to bound parallel consumption.
- Test the DLQ sideline behavior explicitly — submit a known-bad message.

**Don't:**
- Use DLQ as an afterthought — operational processes (fix/resubmit/discard/redrive) must be defined.
- Set `max_concurrency` too low, or queues back up under load.

**Code (verbatim CDK for SQS + ESM):**
```python
self.queue = sqs.Queue(
    self, "NewAccountQueue",
    dead_letter_queue=dead_letter_queue,
    encryption=sqs.QueueEncryption.UNENCRYPTED,
    visibility_timeout=cdk.Duration.seconds(6 * function_timeout),
)

self.new_account_function.add_event_source(
    eventsources.SqsEventSource(
        self.queue,
        batch_size=10,
        max_concurrency=15,
        report_batch_item_failures=True,
        max_batching_window=cdk.Duration.seconds(1),
    )
)
```

**DLQ definition:**
```python
dead_letter_queue = sqs.DeadLetterQueue(
    max_receive_count=3,
    queue=sqs.Queue(self, "NewAccountDLQ"),
)
```

**Batch item failure reporting (Lambda):**
```python
batch_item_failures = []
sqs_batch_response = {}
for record in event.records:
    try:
        body = json.loads(record["body"])
        account_event = json.loads(body["Message"])
        create_brokerage_account(account_event=account_event)
    except Exception as exc:
        batch_item_failures.append({"itemIdentifier": record["messageId"]})
sqs_batch_response["batchItemFailures"] = batch_item_failures
return sqs_batch_response
```

**Operational DLQ disposition (from book):**
```text
- Fix the message contents and resubmit using the SQS API
- Discard it from the queue by purging it
- Update your code and redrive messages back to the main queue
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Self-Healing with Message Queue Retries", "Surviving a Poison Pill"*

---

### Cluster 20 — API Gateway Throttling (Excessive Load mitigation)

**Principle:** API Gateway throttles via a **token-bucket algorithm** to absorb bursts up to a quota, then reject over-quota traffic with HTTP 429.

**Do:**
- Set per-API throttle limits (the book: 100 RPS sustained, 25 burst).
- Account-level quotas must be considered — one runaway API cannot starve others.
- Configure **CloudWatch Logs Insights** queries for `429` codes to monitor throttle events.
- Consider **bounded queue length** or **sideline queues** to shed inbound work when backed up.

**Don't:**
- Leave throttling at the default and hope for the best.
- Ignore 429s in your error metrics — they signal the need for capacity or design changes.

**Code (token-bucket diagram — book Fig 4-13):**
```text
            refill at throttle_rate/sec
        ┌──────────────────────────┐
        │  ███ ████████ ████ ███   │  ← bucket holds tokens
        │  ░░░ ░░░░░░░░ ░░░░ ░░░   │  ← tokens consumed per request
        └──────────────────────────┘
            bucket empty → 429 Too Many Requests
```

**Logs Insights query for 429 throttling:**
```text
fields @timestamp, @message
| filter @message like /429/
| stats count(*) as rateLimitCount by bin(15s)
| sort rateLimitCount desc
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Rate Limiting: Throttle Unanticipated Load"*

---

### Cluster 21 — JSON Schema Validation at the Edge (Misconfigurations mitigation)

**Principle:** Reject invalid input **at the front door** with declarative JSON Schema in API Gateway. Garbage in must not become garbage out.

**Do:**
- Attach JSON Schema models to the REST API request.
- Return **HTTP 400** on schema failure with a clear validation reason.
- Combine with client-side (vee-validate) AND Lambda-side validation — defense in depth.

**Don't:**
- Rely on Lambda-side validation alone — wasted compute and queue pollution.
- Skip schema validation because "the UI validates" — clients can be bypassed.

**Code (JSON Schema principle — book rationale):**
```text
A valid 200 response requires that API Gateway was able to transmit a
message to SNS and receive a 200 from SNS.

A 400 response with validation reason (e.g. "missing account_type")
is returned immediately without calling SNS — saves compute, queue
space, and downstream retries.
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Strongly Typed Service Contracts"*

---

### Cluster 22 — ECS Deployment Circuit Breaker (Misconfigurations/Bugs mitigation)

**Principle:** Detect bad container deployments within **minutes** instead of waiting up to 3 hours for CloudFormation timeout.

**Do:**
- Enable **ECS deployment circuit breaker** with **rollback on failures** on every service.
- Tie to **CloudWatch alarms** for application-level health (not just task launch).
- Run these checks in **CI/CD** — failures stop deployment promotion.

**Don't:**
- Leave deployment circuit breaker off because "we test in lower envs" — production-only bugs happen.
- Disable rollback — automatic rollback reduces MTTD and MTTR for deployment issues.

**Code (CloudFormation/console config — verbatim book):**
```text
Deployment failure detection
├── Use the Amazon ECS deployment circuit breaker         → ENABLED
│   "If the service can't reach a steady state because a task failed to launch, the deployment fails."
└── Rollback on failures                                  → ENABLED
    "If the current deployment fails, the service is rolled back to the last completed deployment state."
```

> "Without circuit breakers, CloudFormation waits up to three hours before timing out. Enabling circuit breakers with rollback reduces MTTD and MTTR from deployment issues."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Container Deployment Failures"*

---

### Cluster 23 — Aurora `max_connections` Discipline (Excessive Load mitigation)

**Principle:** In elastic compute (ECS Fargate), each task opens its own pool — scaling out explodes connection count. Manage it deliberately.

**Do:**
- Use Aurora's default formula: `LEAST({DBInstanceClassMemory/9531392}, 5000)` — connections scale with ACU/memory.
- Route **read-only** queries through the Aurora **read-only endpoint** to spread load across readers.
- Configure **CloudWatch metric filters** for `psycopg2.OperationalError` with text `*remaining connection slots are reserved*`.
- Track `OrderApiConnectionExhaustion` metric with the AZ dimension.

**Don't:**
- Hardcode a low `max_connections` to "be safe" — you'll trigger exhaustion on small traffic spikes.
- Send all reads to the writer — readers exist for a reason.

**Code (CloudWatch metric filter — verbatim book):**
```python
logs.MetricFilter(
    self, "TradeOrderConnectionExhaustion",
    log_group=container.log_group,
    metric_name="OrderApiConnectionExhaustion",
    metric_namespace="TradeOrder",
    metric_value="1",
    unit=cloudwatch.Unit.COUNT,
    filter_pattern=logs.FilterPattern.string_value(
        json_field="$.exec_info", comparison="=",
        value="*remaining connection slots are reserved*",
    ),
    dimensions={"AvailabilityZone": "$.az"},
)
```

**The exhaustion error signature:**
```text
psycopg2.OperationalError: connection to server at
"stock.cluster-...us-east-1.rds.amazonaws.com", port 5432 failed:
FATAL: remaining connection slots are reserved for non-replication
superuser and rds_superuser connections
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Database Connection Exhaustion"*

---

### Cluster 24 — RDS Proxy + Secrets Cache + `@connection_aware` (Self-Healing Decorator)

**Principle:** Convert a **hard** dependency on Secrets Manager + DB into a **soft** dependency that self-heals across password rotations.

**Do:**
- Set `max_connections_percent=95` on RDS Proxy — caps total open connections under all load.
- Use the **Secrets Cache** library (`SecretCacheConfig(max_cache_size=5, secret_refresh_interval=300)`) for soft dependency on Secrets Manager.
- Implement `@connection_aware` decorator that catches `OperationalError`, refreshes the engine, and retries once.
- Tag metrics with `availability_zone` dimension to detect per-AZ credential issues.

**Don't:**
- Cache credentials forever — accept eventual password rotation failures if you do.
- Reconnect on **every** DB call — defeats the connection pool.
- Wrap with `@connection_aware` on operations that are NOT credential-related.

**Code (Secrets Cache — verbatim book):**
```python
def get_db_credentials_from_cache() -> str:
    global secrets_cache, secret_id
    try:
        if secrets_cache is None:
            boto_session = boto3.session.Session()
            secrets_client = boto_session.client("secretsmanager")
            cache_config = SecretCacheConfig(
                max_cache_size=5,
                secret_refresh_interval=300,
            )
            secrets_cache = SecretCache(
                config=cache_config,
                client=secrets_client,
            )
    except ClientError as e:
        raise e
    return secrets_cache.get_secret_string(secret_id)
```

**RDS Proxy configuration (verbatim book):**
```python
proxy = cluster.add_proxy(
    "proxy",
    borrow_timeout=cdk.Duration.seconds(30),
    max_connections_percent=95,
    secrets=[order_api_secret],
    vpc=vpc,
)
```

**`@connection_aware` self-healing decorator (verbatim book):**
```python
def connection_aware(func):
    """Refresh DB connection on credential rotation (OperationalError)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.OperationalError as e:
            logging.exception("db credentials refreshed due to rotation")
            load_db_engine()
            load_ro_db_engine()
            return func(*args, **kwargs)
    return wrapper
```

**Decorate a route (verbatim book):**
```python
@app.route("/db-health/", methods=["GET"])
@connection_aware
def db_health():
    with Session(ro_db_engine) as session:
        statement = select(Customer).where(...)
        customer = session.scalars(statement).one()
        return customer.as_dict()
```

> "The Secrets Cache library turns a hard dependency on Secrets Manager into a soft dependency, tolerating temporary Secrets Manager unavailability."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Database Connection Exhaustion", "Database Password Rotation Login Failures"*

---

### Cluster 25 — Secrets Manager Multiuser Rotation Strategy

**Principle:** Multiuser rotation with `order_api_user` and `order_api_user_clone` plus `AWSCURRENT`/`AWSPREVIOUS` labels lets you maintain availability across **one** rotation. The second consecutive rotation breaks the cached credential — handle that with `@connection_aware`.

**Do:**
- Use `add_rotation_multi_user` for the application user.
- Use `add_rotation_single_user` for the admin user (only accessed from admin client).
- Configure rotation cadence daily.
- Document that **two consecutive rotations without code refresh cause login failures** — this is the scenario `@connection_aware` solves.

**Don't:**
- Assume multiuser rotation is invisible — the second rotation breaks anything without self-healing.
- Rotate more frequently than you can refresh caches.

**Code (CDK for multiuser rotation):**
```python
cluster.add_rotation_single_user(
    automatically_after=cdk.Duration.days(1),
    cluster=cluster,
)
cluster.add_rotation_multi_user(
    order_api_user_name,
    automatically_after=cdk.Duration.days(1),
    secret=order_api_secret,
)
```

**Rotation lifecycle (from book Fig 5-8/9/10):**
```text
Rotation 1 (clone becomes AWSCURRENT):
  AWSCURRENT → order_api_user_clone (new password C)
  AWSPREVIOUS → order_api_user       (cached password A)  ← still works

Rotation 2 (clone becomes AWSCURRENT again):
  AWSCURRENT → order_api_user       (new password D)
  AWSPREVIOUS → order_api_user_clone (old password C)
  Cached password A is now INVALID → OperationalError fires
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Database Password Rotation Login Failures"*

---

### Cluster 26 — Aurora PostgreSQL Fault Injection (Shared Fate / Failure Drills)

**Principle:** Aurora ships **built-in fault injection queries** to validate cluster failover and recovery behavior.

**Do:**
- Use `SELECT aurora_inject_crash('node')` to simulate a writer crash.
- Use `SELECT aurora_inject_disk_congestion(100, 15, true)` to slow response times for latency testing.
- Use AWS Console or CLI for managed failover: `aws rds failover-db-cluster --db-cluster-identifier ...`.
- Capture the recovery time and validate against your BRT.

**Don't:**
- Inject faults without a hypothesis.
- Test failover with stale connections in the application — RDS Proxy is the recommended path.

**Code (fault injection queries):**
```sql
-- Crash the writer node
SELECT aurora_inject_crash('node');

-- Disk congestion for latency testing (100% slowdown for 15s)
SELECT aurora_inject_disk_congestion(100, 15, true);
```

**Expected recovery behavior (verbatim book):**
```text
14:10:54 UTC: ... Simulating DB Instance node crash
14:10:54 UTC: ... select aurora_inject_crash('node');
14:10:54 UTC: ... Aurora Runtime process exited with exit code 1
14:10:54 UTC: ... FATAL: Can't handle storage...
14:10:54 UTC: ... database system is shut down
...
14:11:17 UTC: ... database system is ready  ← recovered ~23 seconds later
```

> "Aurora created a new instance, and did not failover to another instance. The RDS Proxy attempts to queue up requests to provide the highest possible application availability during the write availability interruption."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Database Primary Writer Failures"*

---

### Cluster 27 — Retries with Exponential Backoff + Jitter (Gray Failure mitigation)

**Principle:** AWS APIs already retry with exponential backoff and jitter; replicate the pattern in your code for third-party dependencies.

**Do:**
- Use exponential backoff **plus jitter** to prevent synchronized retry storms from many clients.
- Apply at the boundary of external API calls (e.g., Trade Confirms).
- Pair with **circuit breaker** (next cluster) — retries handle gray failures, circuit breaker handles persistent failures.

**Don't:**
- Retry synchronously without backoff — amplifies outages.
- Retry without jitter — synchronized clients create thundering-herd patterns.
- Retry non-idempotent operations unless you have idempotency keys.

**Code (retry library — verbatim book):**
```python
from retry import retry_call

# Pair retry + circuit breaker; the @circuit decorator stays on execute_trade
result = retry_call(
    execute_trade,
    fargs=[activity.as_dict()],
    fkwargs={"info": "ip"},
    tries=3,
    backoff=0.2,
    jitter=0.1,
)
```

> "An exponential backoff algorithm gradually decreases the rate of retries... Implementing retries without jitter can result in many clients calling a service at the time of an interruption and then synchronizing spikes of retries. Jitter provides variation in the time delay between retries."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Dependency Intermittent Failures"*

---

### Cluster 28 — Circuit Breaker Lifecycle (Closed → Open → Half-Open → Closed)

**Principle:** A circuit breaker protects against **persistent dependency failures** by short-circuiting requests when a failure threshold is breached.

**Do:**
- Configure `failure_threshold` (the book uses 15 failures).
- Set `recovery_timeout` for the half-open window (the book: 60 seconds).
- Track circuit state via a custom CloudWatch metric per AZ.
- Match the trigger exception to the failure mode (`ConfirmsMaintenanceError`, etc.).

**Don't:**
- Apply circuit breakers to every dependency — they are case-by-case.
- Forget the half-open test phase — you need a recovery probe.
- Keep the circuit open forever — recovery is the goal.

**Code (circuit breaker decorator — verbatim book):**
```python
@circuit(
    failure_threshold=15,
    expected_exception=ConfirmsMaintenanceError,
    recovery_timeout=60,
)
def execute_trade(activity: dict) -> Response:
    # ... call Trade Confirms ...
    pass
```

**Lifecycle (book Figs 5-17 through 5-20):**
```text
              failure_threshold breached
       ┌────────────────────────────────────┐
       ▼                                    │
   ┌────────┐    test fails     ┌────────┐  │
   │ CLOSED │ ────────────────▶ │  OPEN  │  │
   └────────┘                   └────────┘  │
       ▲                            │       │
       │ test succeeds              │ recovery_timeout
       │                            ▼       │ elapsed
       │                       ┌──────────┐ │
       └───────────────────────│ HALF-OPEN│─┘
                               └──────────┘
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Dependency Outages"*

---

### Cluster 29 — End-to-End Coordinated Timeout Stack

**Principle:** Each successive timeout in the call stack must be **larger** than the downstream maximum so the downstream can complete or abort before the upstream gives up.

**Do:**
- Apply timeouts at every layer; document them in a call-stack diagram.
- Tune from the data store outward.
- Test with **fault injection** (Aurora disk congestion) that the chain still aborts cleanly.
- Combine with retries+backoff and circuit breakers.

**Don't:**
- Set a client timeout shorter than the server-side SLA — you'll false-positive on slow requests.
- Leave any layer with its default timeout — implicit defaults surprise you.

**Code (AvailableTrade timeout stack — verbatim book Fig 6-5):**
```text
Component                              Timeout
--------------------------------------  -------------
PostgreSQL statement_timeout           100 ms
Trade Confirms HTTP call + retries      300 ms × 3 attempts = 900 ms worst case
Gunicorn worker timeout (Trade Confirms) 1,000 ms
Gunicorn worker timeout (Trade Orders)  2,000 ms
API Gateway integration timeout        2,000 ms
JavaScript AbortSignal.timeout          3,000 ms (client)
```

**Verbatim JavaScript fetch with timeout (book):**
```javascript
async function postTrade(data = {}, options = {}) {
  const request_json = { ... };
  return fetch(import.meta.env.VITE_TRADE_STOCK_ENDPOINT, {
    signal: AbortSignal.timeout(3000),  // 3-second client-side timeout
    method: "PUT",
    mode: "cors",
    cache: "no-cache",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request_json),
  });
}
```

**Verbatim server-side statement_timeout (book):**
```python
db_engine = create_engine(
    db_conn_string,
    pool_size=10,
    connect_args={"options": "-c statement_timeout=100"},  # 100 ms
)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Configuring Client Timeouts"*

---

### Cluster 30 — Graceful Degradation via UI Heartbeat

**Principle:** A partial customer experience beats a hard outage. Detect degradation early and hide the broken features while keeping the rest working.

**Do:**
- Use a **Pinia store** (or equivalent) for a heartbeat monitor.
- Probe the impaired API via `OPTIONS` requests on `setInterval` (book: 5,000 ms).
- On failure: hide the form, display an informative message + fallback option (e.g., phone support).
- Separate **control plane** (account open) from **data plane** (trading) in the UI.

**Don't:**
- Fail hard — confused users will abandon or repeatedly click.
- Couple non-core features to core ones — degradation should isolate impact.

**Code (Pinia store heartbeat — verbatim book):**
```javascript
actions: {
  monitorAccountOpenAvailability() {
    setInterval(this.accountOpenHeartbeat, 5000);
    this.account_open_available = this.accountOpenHeartbeat();
  },
  // ... heartbeats check via fetch OPTIONS to the API endpoint ...
}
```

**UI disable pattern (book):**
```text
When Account Open API is impaired:
  - Hide the New Account form
  - Display: "Our account open service is currently unavailable.
    We'll be back soon. In the meantime, you can still place trades,
    gain insights and use utilities. If you need to open your account
    now, you can still do so with our agent based telephone support.
    Please call (555) GET-WISE [(555) 438-9473]."
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Gracefully Degrading Features"*

---

### Cluster 31 — CloudWatch RUM (Real User Monitoring) for Frontend Errors

**Principle:** RUM complements synthetic monitoring — it tells you what **real users** experience, broken down by device, browser, geography.

**Do:**
- Create **one RUM app monitor per SDLC environment** (dev/prod).
- Use a Cognito identity pool with `allow_unauthenticated_identities=True` for guest telemetry.
- Wire `onErrorCaptured` (Vue.js) to `monitorStore.recordError` for JavaScript error capture.
- Set CloudWatch alarms on the `JsErrorCount` metric.

**Don't:**
- Use a single RUM monitor across environments — you lose segmentation.
- Skip Web Vitals (loading, interactivity, visual stability).

**Code (CDK RUM monitor — verbatim book):**
```python
local_js_error_metric = cloudwatch.Metric(
    metric_name="JsErrorCount",
    namespace="AWS/RUM",
    dimensions_map={"application_name": local.name},
)
cloudwatch.Alarm(
    self, "LocalRumJavascriptErrorsAlarm",
    metric=local_js_error_metric,
    threshold=5,
    evaluation_periods=3,
    datapoints_to_alarm=1,
)
```

**Vue.js error capture (book):**
```javascript
import { useUserMonitorStore } from "@/stores/monitor";
const monitorStore = useUserMonitorStore();
onErrorCaptured((error) => { monitorStore.recordError(error); });
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Real User Monitoring"*

---

### Cluster 32 — X-Ray for End-to-End Tracing

**Principle:** Active tracing surfaces bottlenecks and correlates logs to request segments across services.

**Do:**
- Enable X-Ray on all relevant services (RUM client → API Gateway → SNS → SQS → Lambda).
- Use **Service Map** + **segment timelines** + **integrated logs**.
- Filter traces via refiners: `http.url = ... AND http.method = "PUT"`.

**Don't:**
- Skip X-Ray on busy traces to save cost — sample deliberately, but do trace.

**Code (X-Ray trace map observation from book Fig 6-12):**
```text
RUM Client → API Gateway → SNS → SQS → Lambda (Account Open)
                                       └── ListObjectsV2 consumed > 50% of processing time
                                           ← bottleneck identified via segment timeline
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "X-Ray for End-to-End Tracing"*

---

### Cluster 33 — STOP Pattern (Standby Takes Over Primary) for Regional Switchover

**Principle:** Drive regional failover from the **secondary region** so you can always initiate a switchover even when the primary is impaired.

**Do:**
- Use an indicator file (`failover.txt`) in a secondary-region S3 bucket to signal active/passive mode.
- The Lambda checks the indicator at message processing time — if present, switch behavior.
- Pair with cross-region SNS delivery so messages are not lost during transition.
- Run a "failover.txt" upload step as part of SSM Automation (Ch 7).

**Don't:**
- Drive failover from the primary region when primary is impaired.
- Lose messages during switchover — ensure cross-region SNS subscriptions.

**Code (recovery mode check — verbatim book):**
```python
def in_recovery_mode():
    objects = s3_client.list_objects_v2(Bucket=failover_bucket)
    for obj in objects.get('Contents', []):
        if 'failover.txt' in obj['Key']:
            return True
    return False

# In the Lambda handler:
if active_in_recovery or passive_in_primary:
    # ... wait for record to replicate, then purge safely ...
    pass
else:
    # ... normal processing ...
    pass
```

> "No matter which custom component or AWS service is not working properly in the primary AWS Region, the failure is mitigated by a data plane operation in the recovery AWS Region to drive the secondary region taking over as primary."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "STOP: Business Continuity Regional Switchover"*

---

### Cluster 34 — Aurora Global Database (Cross-Region Replication + Switchover)

**Principle:** Aurora Global uses **storage-based replication** (not engine-level) with subsecond latency; primary + up to 15 secondaries across regions.

**Do:**
- Use Aurora Global for cross-region read replicas with very low replication lag.
- Distinguish **failover** (emergency, possible data loss) from **switchover** (planned, no data loss).
- Implement data reconciliation methods if RPO > 0: checksums, journaling, delta replication, timestamps, application-level reconciliation, manual verification.

**Don't:**
- Use failover for planned maintenance — use switchover instead.
- Assume failover is zero data loss — unreplicated writes are lost.

**Code (SSM Automation step — verbatim book, abridged):**
```json
{
  "inputs": {
    "Service": "rds",
    "Api": "SwitchoverGlobalCluster",
    "GlobalClusterIdentifier": "global-trade-cluster"
  },
  "name": "SwitchoverGlobalCluster",
  "action": "aws:executeAwsApi",
  "nextStep": "SToPFile"
}
```

**Failover vs switchover (book):**
```text
Failover   = unplanned, emergency. Possible data loss.
            Managed: seamless topology-preserving promotion.
            Manual:   topology disrupted, manual rebuild needed.

Switchover = planned, controlled, no data loss.
            Stops writes, waits for replication, promotes secondary.
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Database Failover and Switchover", "Failover", "Switchover"*

---

### Cluster 35 — DynamoDB Global Tables

**Principle:** Multi-active replication across regions; two conflict strategies: **Last Writer Wins (LWW)** or **custom Lambda resolution**.

**Do:**
- Enable point-in-time recovery (PITR) on top of Global Tables for per-second backups (35 days).
- Choose LWW for simplicity; use custom Lambda only when business rules demand it.
- Monitor `ReplicationLatency` and `PendingReplicationCount` metrics.

**Don't:**
- Assume writes to multiple regions are consistent — they are eventually consistent.
- Skip PITR — Global Tables do not replace backups.

**Code (DatasourceStack note from book):**
```text
DatasourcesStack installs in primary:
  - DynamoDB global table for Lambda Powertools idempotency
  - DynamoDB global table for brokerage accounts
  - Both have PITR enabled (35 days, per-second granularity)
  ReplicationLatency ~ 1-2 seconds (typical)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "DatasourcesStack", "Amazon DynamoDB global tables"*

---

### Cluster 36 — Route 53 DNS Failover with CloudWatch Alarm Health Checks

**Principle:** Tie Route 53 failover records to a CloudWatch alarm (which can monitor any custom metric) — this gives **programmatic control** of failover.

**Do:**
- Use **CloudWatch alarm health checks** for fine-grained control.
- Create **failover record sets**: primary → primary-region endpoint, secondary → secondary-region endpoint.
- Monitor primary health from the **secondary region** for independence.
- Validate the alarm transition by publishing a custom metric that breaches its threshold.

**Don't:**
- Use only endpoint health checks — they only see HTTP availability, not application health.
- Run the Route 53 health check from the primary region when primary may be impaired.

**Code (SSM Automation — Signal Route 53 failover via custom metric, verbatim book):**
```json
{
  "inputs": {
    "Service": "cloudwatch",
    "Api": "PutMetricData",
    "Namespace": "AvailableTrade",
    "MetricData": [{
      "MetricName": "AvailableTradeFailoverMetric",
      "Value": 3
    }]
  },
  "name": "PutMetricData",
  "action": "aws:executeAwsApi",
  "isEnd": true
}
```

> "Unlike standard endpoint health checks, custom metrics offer the flexibility to define specific conditions tailored to your application's unique health indicators. This allows you to proactively trigger a failover by simply sending metric data that breaches the alarm's threshold, providing you with more control and adaptability in managing failover scenarios."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "DNS Failover"*

---

### Cluster 37 — SSM Automation Runbooks for Orchestrated Failover

**Principle:** SSM Automation documents let you orchestrate complex, multi-step failover as a single auditable runbook.

**Do:**
- Break recovery into discrete steps: Aurora Global switchover → upload failover.txt → trigger Route 53 alarm.
- Run failover **from the secondary region** (when primary is impaired).
- Rehearse the runbook regularly — recovery plans that exist only on paper are unreliable.
- Coordinate with humans for the **decision** to failover; automate the **execution**.

**Don't:**
- Make the decision to failover fully automatic — humans should own this call.
- Run SSM automation in primary region when primary is impaired.

**Code (full SSM document — verbatim book, abridged):**
```json
{
  "mainSteps": [
    {
      "name": "SwitchoverGlobalCluster",
      "action": "aws:executeAwsApi",
      "inputs": {
        "Service": "rds",
        "Api": "SwitchoverGlobalCluster",
        "GlobalClusterIdentifier": "global-trade-cluster"
      },
      "nextStep": "SToPFile"
    },
    {
      "name": "SToPFile",
      "action": "aws:executeScript",
      "inputs": {
        "Runtime": "python3.10",
        "Script": "import boto3\nwith open('failover.txt','w') as f: f.write('test'); s3 = boto3.client('s3'); s3.upload_file('failover.txt', event['InputPayload']['bucket_name'], 'failover.txt')"
      },
      "nextStep": "PutMetricData"
    },
    {
      "name": "PutMetricData",
      "action": "aws:executeAwsApi",
      "inputs": {
        "Service": "cloudwatch",
        "Api": "PutMetricData",
        "Namespace": "AvailableTrade",
        "MetricData": [{
          "MetricName": "AvailableTradeFailoverMetric",
          "Value": 3
        }]
      },
      "isEnd": true
    }
  ]
}
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Deploying the AWS CDK Orchestration Stack", "Database Failover and Switchover"*

---

### Cluster 38 — Configuration Drift Prevention

**Principle:** Drift between primary and secondary region configurations causes unpredictable failover behavior — eliminate it.

**Do:**
- Use **Infrastructure as Code** (CloudFormation/CDK) to define identical stacks across regions.
- Use **AWS CloudFormation StackSets** for cross-account/region deployment.
- Track configurations with **AWS Config** rules; alert on deviation from baseline.
- Set **CloudWatch alarms** on service-quota usage.
- Use the **AWS Service Quotas API** for automated quota increases.
- Conduct regular **audits** and exercise **change management**.

**Don't:**
- Allow manual console changes that don't go through IaC.
- Assume StackSets alone prevent drift — you still need monitoring.

**Code (drift mitigation matrix — book):**
```text
Strategy                   Use case
-------------------------  ------------------------------------------------
Infrastructure as Code     Version-controlled, reproducible stacks
AWS Config                 Detect deviations; alert on baseline changes
CloudFormation StackSets   Cross-account/region consistency
Service Quotas monitoring  Proactive throttling prevention
Automated quota increases  Triggered by CloudWatch alarms
Automated testing          Verify config in all regions pre-deploy
Regular audits             Catch manual drift
Change management          Make changes go through code review
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Avoiding Configuration Drift"*

---

### Cluster 39 — Zonal Shift with ARC for Gray Failures

**Principle:** When one AZ is impaired but services can't self-evacuate, use **ARC zonal shift** to exclude the AZ temporarily.

**Do:**
- Disable **cross-zone load balancing** on ALB/NLB target groups (`load_balancing.cross_zone.enabled = false`).
- Run the zonal shift: `aws arc-zonal-shift start-zonal-shift --away-from <AZ> --resource-identifier <ALB_ARN>`.
- Track metrics **per AZ** (dimension: `AvailabilityZone`) — required to detect zonal degradation.
- Set a default zonal shift window (e.g., 20 min) and renew as needed.

**Don't:**
- Use zonal shift without disabling cross-zone load balancing.
- Run shifts without per-AZ observability — you cannot detect the impaired AZ otherwise.

**Code (verbatim CDK for cross-zone off):**
```python
def use_service(self, service):
    target_group = self.alb_listener.add_targets(
        self._parent_service.id,
        deregistration_delay=Duration.seconds(10),
        port=80,
        targets=[service],
    )
    target_group.set_attribute("load_balancing.cross_zone.enabled", "false")
```

**Initiate zonal shift (book command):**
```bash
export ORDER_ALB_ARN=$(aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[?contains(LoadBalancerName,`order`)].LoadBalancerArn' \
  --output text)
aws arc-zonal-shift start-zonal-shift \
  --away-from us-east-1b \
  --resource-identifier $ORDER_ALB_ARN
```

> "Zonal shifts can be for longer periods of time or extended as needed. Once you can confirm that a zonal impairment has ended, you can resume normal activity in that AZ by cancelling your zonal shift or letting it expire."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Detecting and Handling Availability Zone Issues"*

---

### Cluster 40 — Apache Kafka Topic Design: Partitions + Replication

**Principle:** Tune partitions for throughput parallelism, replication factor for fault tolerance.

**Do:**
- Pick **partition count** to allow consumer parallelism (the book: 6 partitions for stock trades).
- Pick **replication factor ≥ 3** for production durability.
- Use Kafka's **quorum controller** for metadata consistency.
- Plan **data retention** with tiered storage for cost optimization.

**Don't:**
- Over-partition (unnecessary overhead) or under-partition (limits parallelism).
- Skip replication — single-replica topics are SPOFs.

**Code (CDK MSK cluster + topic — verbatim book):**
```python
kafka_cluster = msk.Cluster(
    self, "KafkaCluster",
    cluster_name="RealTimeMarketData",
    kafka_version=msk.KafkaVersion.V2_8_1,
    vpc=self.get_or_create_vpc(),
)

stock_trades_topic = kafka_cluster.add_topic(
    topic_name="stock-prices",
    partition_count=6,
    replication_factor=3,
)
```

> "Kafka's partitioning, replication, and fault tolerance capabilities allow you to design a data ingestion layer that meets your SLOs, ensuring reliable and consistent data delivery with minimal data loss or staleness."

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Designing the Kafka Topic Structure"*

---

### Cluster 41 — MSK Security: Authentication + Encryption

**Principle:** AuthN, AuthZ, encryption-in-transit, and encryption-at-rest are baseline for financial data.

**Do:**
- Choose auth: **IAM** (leverage existing IAM roles), **SASL/SCRAM** (granular client auth), or **mTLS** (strict encryption+auth).
- Encrypt in transit (TLS) and at rest (AES-256).

**Don't:**
- Skip encryption-at-rest on MSK for production.
- Mix auth methods within one cluster without clear boundaries.

**Code (CDK SASL/SCRAM setup — verbatim book):**
```python
kafka_cluster = msk.Cluster(
    self, ...,
    encryption_in_transit=msk.EncryptionInTransit(...),
    client_authentication=msk.ClientAuthentication.sasl(
        msk.SaslScram(scram_secret_key_arn=self.get_or_create_secret("kafka-scram-key"))
    ),
)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Securing the Kafka Cluster"*

---

### Cluster 42 — Kafka Consumer Groups + Auto-Scaling on Lag

**Principle:** Consumer groups automatically **rebalance partitions** on failure or scale-out. Auto-scale on **consumer lag**.

**Do:**
- Set max capacity for the ECS service task count.
- Define the `ConsumerLag` metric for the consumer group as the scaling trigger.
- Use step scaling: add tasks when lag > 100, remove when lag < 100.

**Don't:**
- Run more consumers than partitions — extras are idle.
- Forget to commit offsets — replay from beginning after restart.

**Code (auto-scaling — verbatim book):**
```python
scaling = order_book_service.auto_scale_task_count(max_capacity=10)
scaling.scale_on_metric(
    "ScaleOnConsumerLag",
    metric=cloudwatch.Metric(
        namespace="AWS/Kafka",
        metric_name="ConsumerLag",
        dimensions={
            "Cluster Name": kafka_cluster.cluster_name,
            "Consumer": "order-book-consumer-group",
        },
        period=cdk.Duration.minutes(1),
    ),
    scaling_steps=[
        cloudwatch_actions.ScalingInstruction(change=+1, lower=100, upper=300, min_adjustment_magnitude=1),
        cloudwatch_actions.ScalingInstruction(change=-1, lower=0, upper=100, min_adjustment_magnitude=1),
    ],
)
```

**Consumer-group partition assignment (from book):**
```text
3 consumer instances × 6 partitions  →  2 partitions per instance
New instance joins              →  Kafka rebalances: 4 × 1.5 partitions
Instance fails                  →  Kafka rebalances partitions to survivors
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Implementing Reliable Consumers", "Ensuring Fault Tolerance and Scalability"*

---

### Cluster 43 — Kafka Consumer with Commit-Based Recovery

**Principle:** Commit offsets for successfully processed events; resume from last commit on failure.

**Do:**
- For **Lambda** consumers: ESM handles offset commits on success.
- For **containerized** consumers: explicitly commit after processing each batch.
- Use `enable_auto_commit=False` and explicit commits for predictable recovery.

**Don't:**
- Auto-commit before processing — duplicates on restart.
- Skip checkpointing for long-running containers.

**Code (Lambda consumer pattern — verbatim book):**
```python
import json, base64
def lambda_handler(event, context):
    records = event["records"]
    for record in records:
        payload = base64.b64decode(record["data"])
        do_stuff(payload)
    return {"statusCode": 200, "body": json.dumps("Message batch processed")}
```

**Containerized consumer with explicit commit — verbatim book:**
```python
import asyncio, time
from kafka import KafkaConsumer
kafka_config = {
    "bootstrap_servers": ["broker:9092"],
    "group_id": "my-consumer-group",
    "auto_offset_reset": "earliest",
}
consumer = KafkaConsumer(topic_name="my-topic", **kafka_config)
checkpoint_interval = 60

async def read_and_checkpoint():
    last_checkpoint = time.time()
    while True:
        try:
            messages = await asyncio.wait_for(consumer.getmany(timeout_ms=1000), timeout=2)
            if not messages:
                if time.time() - last_checkpoint > checkpoint_interval:
                    await consumer.commit(); last_checkpoint = time.time()
                await asyncio.sleep(1); continue
            for tp, message in messages.items():
                for record in message:
                    message_value = json.loads(record.value.decode())
                    print(f"Received message: {message_value}")
        except asyncio.TimeoutError:
            continue
        except KeyboardInterrupt:
            await consumer.stop(); break
    await consumer.commit()
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Consumer Groups and Record Processing"*

---

### Cluster 44 — Kafka Poison Pill Handling with Schema Validation

**Principle:** Validate every message against schema **before** processing; route failures to DLQ.

**Do:**
- Use `jsonschema` library to validate against a strict schema.
- Wrap processing in `try/except`, log the bad message, route to DLQ.
- Categorize strategies: retry with backoff, skip + log, DLQ, fallback.

**Don't:**
- Crash on poison pills — they halt all subsequent messages.
- Skip DLQ for "intermittent" failures — operator needs a record.

**Code (verbatim book poison pill handler):**
```python
import json, jsonschema
STOCK_TRADE_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol":    {"type": "string"},
        "price":     {"type": "number"},
        "volume":    {"type": "integer"},
        "timestamp": {"type": "string", "format": "date-time"},
    },
    "required": ["symbol", "price", "volume", "timestamp"],
}

def is_invalid_payload(payload):
    try:
        payload_data = json.loads(payload)
        jsonschema.validate(instance=payload_data, schema=STOCK_TRADE_SCHEMA)
    except (json.JSONDecodeError, jsonschema.exceptions.ValidationError):
        return True
    return False
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Handling Invalid Messages"*

---

### Cluster 45 — Optimistic vs Pessimistic Concurrency in State Management

**Principle:** Match concurrency strategy to contention frequency and consistency requirements.

**Do:**
- Use **optimistic concurrency** (etag/version + conditional update) when conflicts are infrequent — high performance, no lock overhead.
- Use **pessimistic concurrency** (distributed lock via ZooKeeper/etcd/Redis) when conflicts are frequent and strong consistency is mandatory.
- Choose **NoSQL** (DynamoDB) for high-velocity state; **SQL** when you need strong consistency and complex queries.

**Don't:**
- Use locks when you don't have high contention — overhead without benefit.
- Use optimistic concurrency when conflicts are likely — constant retries hurt throughput.

**Code (DynamoDB optimistic concurrency — verbatim book):**
```python
import uuid
def lambda_handler(event, context):
    payload = json.loads(event["body"])
    stock_symbol = payload["symbol"]
    response = state_table.get_item(Key={"stock_symbol": stock_symbol})
    current_state = response.get("Item", {"total_shares": 0, "etag": str(uuid.uuid4())})
    current_volume = payload["volume"]
    total_shares = current_state["total_shares"] + current_volume
    new_etag = str(uuid.uuid4())
    try:
        response = state_table.update_item(
            Key={"stock_symbol": stock_symbol},
            UpdateExpression="SET total_shares = :val, etag = :new_etag",
            ExpressionAttributeValues={":val": total_shares, ":new_etag": new_etag,
                                      ":etag": current_state["etag"]},
            ConditionExpression="etag = :etag",
            ReturnValues="UPDATED_NEW",
        )
        updated_state = response["Attributes"]
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {"statusCode": 409,
                "body": json.dumps({"message": "Concurrent update detected"})}
```

**Decision matrix (from book):**
```text
Conflict Frequency     Preferred Strategy
-------------------   --------------------------------
Low                   Optimistic (etag + ConditionExpression)
High                  Pessimistic (distributed lock — ZooKeeper/etcd/Redis)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Handling Concurrency"*

---

### Cluster 46 — Schema Evolution with Message Envelopes

**Principle:** Use envelopes + version declarations so consumers can evolve independently of producers.

**Do:**
- Wrap payloads in envelopes with explicit version fields (use date-based versioning like `2024-06-09`).
- Make new properties nullable to preserve backward compatibility.
- Centralize schemas in **AWS Glue Schema Registry** for cross-team sharing.

**Don't:**
- Make breaking schema changes without a migration plan.
- Use generic versions like `v1` — they lose context.

**Code (message envelope — verbatim book):**
```json
{
  "Version": "2024-06-09",
  "Payload": {
    "symbol": "AMZN",
    "market": "NYSE",
    "price": "185.12",
    "volume": "12345678",
    "timestamp": "1704383560"
  }
}
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Designing Consumer State"*

---

### Cluster 47 — Restartability via Offset Reset

**Principle:** Recover from code defects by **resetting consumer-group offsets** to a point before the defect.

**Do:**
- Document offset reset as a recovery step in runbooks.
- For complex state, pair with **checkpoint + replay** mechanism (persist app state + offsets to durable storage).

**Don't:**
- Reset offsets without knowing the downstream impact.
- Reset to a point where data has already been overwritten.

**Code (AWS CLI offset reset — verbatim book):**
```bash
PARTITION='"TopicPartition":{"Topic":"stock_prices","Partition":0}'
STRATEGY='"ConsumerGroupStrategy":"UseConsumerGroupOffsets"'
OFFSET='{"ConsumerGroupOffset":{"Offset":12345}}'
METADATA='"ConsumerGroupOffsetMetadata":${OFFSET}'
aws kafka reset-consumer-group-offsets \
  --cluster-arn "arn:aws:kafka:us-east-1:123456789012:cluster/..." \
  --group-id "stock_price_reader" \
  --execute-service-action "{ ${PARTITION},${STRATEGY},${METADATA} }" \
  --region us-east-1
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Using Restartability"*

---

### Cluster 48 — Producer-Consumer Pattern with SQS

**Principle:** Decouple Producer (Scheduler) from Consumers (Worker Nodes) for independent scaling and fault isolation.

**Do:**
- Use SQS as the durable buffer between producer and consumers.
- Plan for each failure mode: producer failure (ECS restart, SQS retains), consumer failure (visibility timeout retries), SQS outage (retry with backoff), external source outage (circuit breaker + DLQ), storage outage (local cache + retry).

**Don't:**
- Couple producer and consumer — they must fail and scale independently.

**Code (Producer pattern — verbatim book):**
```python
import os, boto3, json, requests
sqs = boto3.client("sqs")
def get_sitemap_urls():
    with open("sitemap_config.json", "r") as f:
        return json.load(f)["sitemap_urls"]
def process_sitemaps():
    for article_url in get_articles():
        for url in get_sitemap_urls():
            article_metadata = fetch_and_process_sitemap(url)
            sqs.send_message(
                QueueUrl=os.environ["NEWS_INGEST_QUEUE_URL"],
                MessageBody=json.dumps(article_metadata),
            )
def fetch_and_process_sitemap(url):
    response = requests.get(url)
    return parse_sitemap(response.text)
```

**Consumer pattern (verbatim book):**
```python
from redis import Redis
import boto3, json, os
REDIS_ENDPOINT = os.environ["REDIS_ENDPOINT"]
BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def handle_message(message):
    article_metadata = json.loads(message["Body"])
    fetch_and_store_article(article_metadata)

def store_article_metadata(metadata, content):
    redis = Redis(host=REDIS_ENDPOINT, port=6379)
    url = metadata["url"].replace("/", "-")
    redis.hset(f"article:{metadata['url']}", mapping={
        "title": metadata["title"],
        "author": metadata["author"],
        "publication_date": metadata["publication_date"],
        "s3_uri": f"s3://{BUCKET_NAME}/{url}.html",
    })

def store_article_content(url, content):
    boto3.client("s3").put_object(
        Bucket=os.environ["S3_BUCKET_NAME"],
        Key=f"{url.replace('/', '-')}.html",
        Body=content,
    )
```

**Failure-mode matrix (book Table 9-1):**
```text
Producer failure          → ECS restarts Producer; SQS retains unprocessed
Consumer failure          → ECS restarts Consumer; visibility timeout retries
SQS unavailable           → Producer/Consumer retry with exponential backoff
External source down      → Circuit breaker + DLQ for later retry
MemoryDB/S3 outage        → Local cache failed writes + retry when up
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Producer-Consumer Pattern for Article Processing"*

---

### Cluster 49 — Leader Election with Redis Lock

**Principle:** For singleton schedulers, run **multiple instances** across AZs with a distributed lock — only the lock holder is active.

**Do:**
- Set a short lock timeout so failures release the lock quickly.
- Have standby instances poll every ~5s for leadership takeover.
- Use Redis `SET key value NX EX seconds` for atomic lock acquisition.

**Don't:**
- Use a single scheduler without failover plan — it's a SPOF.
- Hold the lock forever — set TTL.

**Code (verbatim book):**
```python
import redis, time, os, logging
logger = logging.getLogger(__name__)
class LeaderElector:
    def __init__(self, redis_host, redis_port, scheduler_name):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.scheduler_name = scheduler_name
        self.lock_name = f"scheduler_lock_{scheduler_name}"
        self.lock_timeout = 30

    def acquire_lock(self):
        try:
            return self.redis.set(self.lock_name, self.scheduler_name, ex=self.lock_timeout, nx=True)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error acquiring scheduler lock: {e}"); return False

    def release_lock(self):
        try:
            self.redis.delete(self.lock_name)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error releasing scheduler lock: {e}")

    def is_leader(self):
        try:
            return self.redis.get(self.lock_name)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error checking scheduler lock: {e}"); return False

def main():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    scheduler_name = os.getenv("SCHEDULER_NAME", "scheduler-1")
    elector = LeaderElector(redis_host, redis_port, scheduler_name)
    while True:
        if elector.acquire_lock():
            logger.info(f"{scheduler_name} is the leader")
            do_stuff()
            time.sleep(60)
            elector.release_lock()
        else:
            logger.info(f"{scheduler_name} is not the leader, standby")
            time.sleep(5)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Leader Election for Scheduler High Availability"*

---

### Cluster 50 — Bulkhead Pattern + EventBridge Choreography

**Principle:** Isolate resources by work type (financial / sports / tech) so one stream's failure doesn't starve another.

**Do:**
- Run separate ECS task definitions/services per bulkhead with dedicated CPU/memory.
- Pair Bulkhead with **EventBridge** for choreographed, filtered event routing (vs. tight SQS coupling).
- Use `deployment_circuit_breaker.rollback` + `min_healthy_percent` / `max_percent` per bulkhead.

**Don't:**
- Share a single pool across heterogeneous workloads — bulkheads prevent cascading failure.

**Code (verbatim book — Bulkhead ECS setup):**
```python
cluster = ecs.Cluster(self, "BulkheadCluster")

# Dedicated finance bulkhead
finance_task_def = ecs.Ec2TaskDefinition(self, "FinanceTaskDef")
finance_task_def.add_container("FinanceContainer",
    image=ecs.ContainerImage.from_registry("finance-consumer"),
    memory_reservation_mib=4096,
    cpu=2048)
finance_service = ecs.Ec2Service(self, "FinanceService",
    cluster=cluster, task_definition=finance_task_def, desired_count=2)
deployment_config = finance_service.node.default_container.deployment_config
deployment_config.deployment_circuit_breaker.rollback = True
deployment_config.min_healthy_percent = 50
deployment_config.max_percent = 200
```

**EventBridge publish pattern (verbatim book):**
```python
import boto3
eventbridge = boto3.client('events')
response = eventbridge.put_events(Entries=[{
    "Source": "news-scheduler",
    "DetailType": "sitemap URL",
    "Detail": '{"url": "https://example.com/sitemap-main.xml"}',
}])
```

**Combined benefits (book):**
```text
Flexibility   — Easy add/remove of bulkheads
Scalability   — Per-bulkhead scaling; EventBridge auto-scales
Resilience    — Failures contained per bulkhead; EventBridge HA
Decoupling    — Independent deploy; EventBridge mediates
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Additional Resiliency Strategies"*

---

### Cluster 51 — CDC + CQRS for Heterogeneous Data Sync

**Principle:** Decouple writes (MemoryDB) from reads (OpenSearch) with **Change Data Capture** to bridge them.

**Do:**
- Use Redis Streams to capture changes; containerized process reads streams and writes to OpenSearch.
- Enable OpenSearch **replicas** + **shard allocation filtering** + **quorum-based operations** + **cluster auto-scaling**.
- Use OpenSearch **ISM** for lifecycle automation.

**Don't:**
- Synchronously dual-write to MemoryDB and OpenSearch — coupling reduces availability.
- Skip replica configuration — single-shard indices lose data on node failure.

**Code (verbatim book — CDC consumer):**
```python
import os, json, boto3
from opensearchpy import OpenSearch, AWS4Auth, RequestsHttpConnection
from redis import Redis

redis_endpoint = os.environ["REDIS_ENDPOINT"]
opensearch_endpoint = os.environ["OPENSEARCH_ENDPOINT"]
s3_bucket = os.environ["S3_BUCKET"]

def consume_redis_stream(event, context):
    redis = Redis(host=redis_endpoint, port=6379)
    events = redis.xread({"news-updates": "0-0"}, count=100)
    for stream, messages in events:
        for message in messages:
            index_article(message, opensearch_endpoint, s3_bucket)

def index_article(message, opensearch_endpoint, s3_bucket):
    article_id = message[0].decode("utf-8")
    article_data = json.loads(message[1][b"data"].decode())
    s3 = boto3.client("s3")
    s3_key = f"articles/{article_id.replace('/', '-')}.html"
    article_content = s3.get_object(Bucket=s3_bucket, Key=s3_key)["Body"].read()
    region = os.environ["AWS_REGION"]
    service = "es"
    credentials = boto3.Session().get_credentials()
    http_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service,
                         session_token=credentials.token)
    opensearch = OpenSearch(hosts=[{"host": opensearch_endpoint, "port": 443}],
                            http_auth=http_auth, use_ssl=True, verify_certs=True,
                            connection_class=RequestsHttpConnection)
    opensearch.index(index="articles", id=article_id, body={
        "title": article_data["title"],
        "author": article_data["author"],
        "publication_date": article_data["publication_date"],
        "content": article_content.decode("utf-8"),
    }, refresh=True)
```

**OpenSearch indexing failure-mode matrix (book Table 9-3):**
```text
Network partitions       → quorum-based ops + rack-aware
Node failures            → replica shards + shard allocation filtering
Disk failures            → distributed filesystem
Resource exhaustion      → cluster auto-scaling + indexing throttling
Shard unavailability     → force merge + shard reallocation
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Syncing Articles to OpenSearch"*

---

### Cluster 52 — Search API Decoupling via ALB + ECS

**Principle:** Add a Search API broker between clients and OpenSearch for caching, fine-grained access control, multi-source aggregation.

**Do:**
- Use ALB + ECS service as the broker.
- Use Secrets Cache for OpenSearch credentials.
- Handle each failure mode (ECS task failures, OpenSearch issues, network disruption).

**Don't:**
- Let clients hit OpenSearch directly — you lose access control and rate limiting.

**Code (Search API Flask app — verbatim book):**
```python
from flask import Flask, request, jsonify
from opensearchpy import OpenSearch
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
import json

app = Flask(__name__)
OPENSEARCH_ENDPOINT = app.config["OPENSEARCH_ENDPOINT"]
SECRET_ARN = app.config["SECRET_ARN"]
secrets_cache = SecretCache(config=SecretCacheConfig(max_cache_size=5, secret_refresh_interval=300),
                             secret_id=SECRET_ARN)
secret = json.loads(secrets_cache.get_secret_string(SECRET_ARN))
opensearch_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_ENDPOINT, "port": 443}],
    http_auth=(secret.get("username"), secret.get("password")),
    use_ssl=True, verify_certs=True,
)

@app.route("/search", methods=["GET"])
def search_articles():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing search query"})
    try:
        response = opensearch_client.search(index="articles", body={
            "query": {"multi_match": {"query": query, "fields": ["title", "content"]}}
        })
        return jsonify(response["hits"]["hits"])
    except Exception as e:
        app.logger.error(f"Error searching articles: {e}")
        return jsonify({"error": "Error executing search"})
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Serving Search Traffic"*

---

### Cluster 53 — Kafka MirrorMaker for Multi-Region Replication

**Principle:** MirrorMaker consumes from source cluster and produces to target cluster — bridges regional Kafka clusters.

**Do:**
- Use MirrorMaker as a managed connector on MSK.
- Consider Confluent Replicator or IBM Aspera for bidirectional replication with custom filtering.
- Design consumers to handle **duplicates and out-of-order events** introduced by cross-region replication.

**Don't:**
- Assume MirrorMaker alone solves consistency — it's eventual.
- Skip idempotency on consumers — duplicates are inevitable.

**Code (CDK MSK MirrorMaker connector — verbatim book):**
```python
mirror_maker_config = {
    "name": "MyMirrorMaker",
    "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "source.cluster.alias": "source",
    "target.cluster.alias": "target",
    "source.cluster.bootstrap.servers": source_cluster.bootstrap_servers,
    "target.cluster.bootstrap.servers": target_cluster.bootstrap_servers,
    "topics": ".*",
}
msk.CfnConnector(
    self, "MirrorMakerConnector",
    connector_name="MyMirrorMaker",
    kafka_cluster=target_cluster,
    connector_configuration=mirror_maker_config,
)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Replicating Kafka Data Across Regions"*

---

### Cluster 54 — OpenSearch Cross-Cluster Replication (CCR)

**Principle:** OpenSearch CCR creates **read-only** index copies in remote clusters; choose unidirectional (simpler) or bidirectional (write-capable, conflict resolution required).

**Do:**
- Use CCR for read-scaling across regions.
- Plan conflict resolution (custom merge script via index template) for bidirectional setups.
- Use snapshot-based or plug-in replication for other topologies.

**Don't:**
- Use CCR and assume zero replication latency — it has lag.
- Skip conflict resolution in bidirectional mode.

**Code (OpenSearch CCR setup — verbatim book):**
```python
source_domain = opensearch.Domain(self, "SourceDomain", ...)
target_domain = opensearch.Domain(self, "TargetDomain", ...)
replication_config = {
    "source_cluster": source_domain.domain_endpoint,
    "target_cluster": target_domain.domain_endpoint,
    "indices": ["my-index"],
}
opensearch.CfnReplicationGroup(
    self, "ReplicationGroup",
    replication_group_description="My replication group",
    replication_config=replication_config,
)
```

**CLI for outbound connection (verbatim book):**
```bash
aws opensearch create-outbound-connection \
  --source-domain-info DomainName="primary-domain-name",Region="us-east-1" \
  --destination-domain-info DomainName="secondary-domain-name",Region="us-west-2" \
  --connection-alias "primary-to-secondary-replication"

aws opensearch start-outbound-connection \
  --source-domain-name "primary-domain-name" \
  --connection-id "<id from create>"
```

**Conflict resolution via merge script (book):**
```python
template = {
    "index_patterns": ["stock-*"],
    "template": {
        "settings": {
            "index.merge.policy.merge_strategy": {
                "type": "script",
                "source": """
                    if (ctx._source.last_updated > params.last_updated) {
                        ctx._source = params;
                    }
                """
            }
        }
    }
}
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Cross-Region Data Replication with OpenSearch", "Handling Conflict Resolution"*

---

### Cluster 55 — Multi-Region Caching Strategies

**Principle:** Pick a cache topology aligned to access pattern; balance latency, consistency, and fault tolerance.

**Do:**
- **Regional cache clusters** for low-latency, isolated caches per region — accept synchronization complexity.
- **Global cache with replication** for simplicity and consistency — accept cross-region latency.
- **Hybrid** for the best of both: regional for hot region-specific data, global for shared data.
- Use **Amazon ElastiCache** with Multi-AZ + cross-region replication.

**Don't:**
- Run a global cache when regional isolation is the priority — cross-region links create coupling.
- Forget cache invalidation rules during failover.

**Code (CDK ElastiCache Multi-Region Replication — verbatim book):**
```python
primary_cluster = elasticache.CfnCacheCluster(
    self, "PrimaryCluster", engine="redis",
    cache_node_type="cache.r7g.large", num_cache_nodes=1,
    auto_minor_version_upgrade=True, multi_az_enabled=True)

secondary_cluster = elasticache.CfnReplicationGroup(
    self, "SecondaryCluster",
    replication_group_description="Secondary cluster",
    engine="redis", cache_node_type="cache.r6g.large",
    num_node_groups=1, replicas_per_node_group=1,
    automatic_failover_enabled=True, multi_az_enabled=True)

elasticache.CfnGlobalReplicationGroup(
    self, "GlobalReplicationGroup",
    members=[
        elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMember(
            replication_group_id=primary_cluster.ref, role="PRIMARY"),
        elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMember(
            replication_group_id=secondary_cluster.ref, role="SECONDARY"),
    ])
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Caching in Multi-Region Architectures"*

---

### Cluster 56 — CAP and PACELC Consistency Models

**Principle:** Make trade-offs explicit using CAP (under partition) and PACELC (also normal operation).

**Do:**
- Apply CAP during partitions: choose **availability** or **consistency** deliberately.
- Apply PACELC normally: choose **latency** or **consistency** deliberately.
- For trading platforms: prioritize strong consistency for trades/balances; eventual consistency for news/preferences.

**Don't:**
- Claim a system is "CA" — distributed systems **must** tolerate partition.

**Code (decision heuristics):**
```text
Workload type                CAP choice    PACELC choice
---------------------------  ------------  ---------------
Stock trades/balances        Consistency   Consistency
Order book reads             Availability  Latency
Stock news (display)         Availability  Latency
User preferences             Availability  Latency
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Understanding Consistency Models"*

---

### Cluster 57 — Replication Strategies: Active-Passive vs Active-Active

**Principle:** Pick replication topology by consistency needs and write latency tolerance.

**Do:**
- Use **active-passive** for one-region-writes-only with strong consistency and clear write path.
- Use **active-active** for lowest write latency globally; require conflict resolution.
- Choose **active-active** for AvailableTrade if write latency matters most and eventual consistency is acceptable.

**Don't:**
- Use active-active without a conflict resolution strategy.
- Use active-passive when distant users face unacceptable write latency.

**Code (decision matrix):**
```text
Topology          Pros                          Cons
---------------   --------------------------    ---------------------------------
Active-Passive    Simple consistency; clear     Higher write latency for distant users;
                  write path                     potential data loss during failover
Active-Active     Lowest write latency; HA      Conflict resolution complexity;
                                                consistency challenges
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Replication Strategies"*

---

### Cluster 58 — Firehose + Athena Failure Modes and Mitigations

**Principle:** Firehose batches streaming data to S3; Athena queries it via serverless SQL. Both have distinct failure modes to handle.

**Do:**
- Implement retries, fallback mechanisms, data buffering, circuit breakers, health checks, automatic restarts.
- Validate data quality at ingestion.
- Use partitioning (date, symbol) for query performance.
- Use Parquet format for cost-efficient storage.

**Don't:**
- Skip data validation — bad data poisons queries.
- Use Athena without understanding DPU/cost model.

**Code (Firehose to S3 in Parquet — verbatim book):**
```python
processed_data_bucket = s3.Bucket(...)
kinesis_firehose = firehose.DeliveryStream(
    self, "ProcessedDataDeliveryStream",
    destinations=[firehose.S3Bucket(processed_data_bucket)],
)
athena_database = athena.Database(self, "ProcessedDataDatabase")
athena_table = athena_database.add_table(
    table_name="processed_market_data",
    bucket=processed_data_bucket,
    data_format=athena.DataFormat.PARQUET,
    partition_keys=[
        athena.String.from_json_path("$.date"),
        athena.String.from_json_path("$.stock_symbol"),
    ],
)
```

**Firehose failure-mode matrix (book Table 8-7):**
```text
Network connectivity issues       → Retry, connection monitoring, failover
Firehose service outage          → Retries, fallback, data buffering
Data transformation errors       → Data validation, error handling, logging
Firehose throttling              → Backpressure, rate limiting, load balancing
Destination service outage       → Retries, fallback, data buffering
Encryption/decryption failures   → Key management, error handling
Insufficient Firehose throughput → Monitor and scale, buffering
Serialization/deserialization    → Data validation, error handling, logging
Firehose destination config errs → Automated testing, config management
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Storing and Querying Processed Market Data", "Handling Firehose Failure Modes"*

---

### Cluster 59 — Athena Query Failure Modes

**Principle:** Athena is serverless but not free of failures; design for retryable queries and resource limits.

**Do:**
- Retry failed queries with backoff.
- Implement circuit breakers around Athena calls.
- Use **query result caching** and **materialized views** for cost/perf.
- Set resource limits on DPUs and concurrent queries.

**Don't:**
- Run unbounded concurrent queries — Athena throttles.
- Skip query result caching on frequently-asked questions.

**Code (Athena query — verbatim book):**
```python
import boto3, pandas as pd
athena_client = boto3.client("athena")
query = """
SELECT date, stock_symbol, AVG(price) as avg_price
FROM "processed_market_data"
WHERE date >= DATE('2023-04-01') AND date <= DATE('2023-04-30')
GROUP BY date, stock_symbol
ORDER BY date, stock_symbol;
"""
response = athena_client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={"Database": "processed_data_database"},
    ResultConfiguration={"OutputLocation": "s3://your-output-bucket/"},
)
query_execution_id = response["QueryExecutionId"]
while True:
    state = athena_client.get_query_execution(QueryExecutionId=query_execution_id)["QueryExecution"]["Status"]["State"]
    if state == "SUCCEEDED": break
result_data = athena_client.get_query_results(QueryExecutionId=query_execution_id)
df = pd.DataFrame([row["Data"] for row in result_data["ResultSet"]["Rows"][1:]])
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Querying Athena"*

---

### Cluster 60 — Kafka Monitoring (Consumer Lag, Processing Rate, Fetch Latency)

**Principle:** Track the three core Kafka consumer metrics; alarm on consumer lag before it causes business impact.

**Do:**
- Monitor **consumer lag** per partition per consumer instance.
- Monitor **processing rate** (messages/sec) to detect slow consumers.
- Monitor **fetch latency** for broker/network issues.
- Set CloudWatch alarms with appropriate `treat_missing_data` settings.

**Don't:**
- Rely on cluster-wide lag only — per-partition visibility catches localized issues.
- Set thresholds without baseline data.

**Code (CloudWatch ConsumerLag alarm — verbatim book):**
```python
consumer_lag_metric = cloudwatch.Metric(
    namespace="AWS/Kafka",
    metric_name="ConsumerLag",
    dimensions={
        "Cluster Name": kafka_cluster.cluster_name,
        "Consumer": "stock-trades-consumer-group",
    },
    period=cdk.Duration.minutes(1),
)
cloudwatch.Alarm(
    self, "ConsumerLagAlarm",
    alarm_name="ConsumerLagAlarm",
    metric=consumer_lag_metric,
    threshold=100,
    evaluation_periods=1,
    datapoints_to_alarm=1,
    treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
)
```

**Three core metrics (book Table 8-10):**
```text
Consumer lag       — Latest offset − last processed offset. High = stale data.
Processing rate    — Messages/sec per consumer. Low = bottleneck.
Fetch latency      — Time to fetch from brokers. High = network/IO issue.
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Monitoring and Observability"*

---

### Cluster 61 — FIS Built-in Chaos Experiments

**Principle:** AWS FIS provides prebuilt experiment templates for common AWS services — use them before writing custom ones.

**Do:**
- Use built-in MSK broker termination, network latency, packet loss experiments.
- Set stop conditions (e.g., 10 min timeout) and blast-radius controls.
- Send FIS experiment logs to CloudWatch for analysis.

**Don't:**
- Run FIS experiments without stop conditions.
- Disable autoscaling during experiments unless the goal is to test degraded scaling.

**Code (book Table 8-12 — built-in AWS FIS experiments):**
```text
Chaos experiment                                       Action
----------------------------------------------------   -------------------------------------
Terminate Amazon MSK broker instances                  aws:msk:broker-terminate
Induce network latency (producers/consumers/MSK)      aws:ec2:network-latency-interference
Induce network packet loss                             aws:ec2:network-bandwidth-interference
Disable Amazon MSK autoscaling                         aws:msk:cluster-scale-in-stop
Corrupt Amazon MSK topic data                          aws:kafka:topic-data-corruption
Delete Amazon MSK topic data                           aws:kafka:topic-data-deletion
Increase Lambda function timeout exceptions            aws:lambda:function-throttle
Corrupt Amazon S3 bucket data                          aws:s3:object-data-corruption
Delete Amazon S3 bucket data                           aws:s3:object-data-deletion
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Testing Resiliency" (Ch 8)*

---

### Cluster 62 — Blue-Green Testing via Regional Switchover

**Principle:** Use the secondary region as the **green** environment — deploy new code there, validate with synthetic traffic, then switch DNS for production rollout.

**Do:**
- Deploy new code to secondary region; validate via test users with `greentest_` prefix.
- Switch traffic via DNS failover records; switch back after primary deployment.
- Use Lambda aliases + API Gateway stages for fine-grained version control.

**Don't:**
- Skip the green-test prefix — it lets you isolate synthetic test traffic.

**Code (Lambda green-test predicate — verbatim book):**
```python
green_test = "greentest_" in message["user_id"]
if (active_in_recovery or passive_in_primary) and not green_test:
    # normal recovery mode
    pass
else:
    # green-test user → process even in recovery mode
    process_new_account(message)
```

**Blue-green via regional switchover (book procedure):**
```text
1. Site-switch production traffic to secondary region
2. Deploy new code to primary region, validate with test user
3. Switch back to primary with new code deployed
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Blue-Green Testing"*

---

### Cluster 63 — Anti-Fragility: Systems That Gain from Disorder

**Principle:** Anti-fragile systems don't just survive stress — they **improve** from it. Cultivate this through experimentation, learning, and adaptation.

**Do:**
- Treat incidents as **learning fuel** — run blameless postmortems.
- Invest in **continuous resilience** — tests, chaos experiments, SLO reviews.
- Cross-pollinate teams via workshops and resilience champion networks.
- Maintain a dedicated **resilience improvement backlog**.

**Don't:**
- Treat failure as a personal failing — the system is the unit of analysis.
- Skip the "what did we learn?" step in incident response.

**Code (resilience culture practices — book):**
```text
Friday resilience hour     — Rotate teams analyzing failure modes monthly
Monthly resilience roundup — Review metrics, incidents, improvement initiatives
Quarterly cross-pollination — Workshops across teams for shared learnings
Resilience champions network — Local advocates per team
Resilience improvement backlog — Always-on backlog of improvements
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Leading Resiliency Initiatives"*

---

### Cluster 64 — Resilience Observability at Every Layer

**Principle:** Resilience observability goes beyond traditional monitoring — capture differential observability (system vs. user), per-AZ, per-region, per-bulkhead.

**Do:**
- Tag metrics with **AvailabilityZone** dimension for zonal analysis.
- Tag metrics with **application** and **environment** for SDLC segmentation.
- Build composite alarms to summarize health without alarm fatigue.
- Wire X-Ray through every service that participates in critical paths.

**Don't:**
- Average metrics across AZs — you hide zonal issues.
- Skip composite alarms when you have many leaf metrics.

**Code (composite alarms):**
```text
# Recommended by book for summarization
Service Health = ALARM(
    AND(API Gateway 5xx > threshold,
        OR(AuroraConnections > 90% capacity, TradeConfirmsErrorRate > 5%),
        JsErrorCount > threshold)
)
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Observability" (Ch 1), "Composite Alarms" references throughout*

---

### Cluster 65 — Backup Strategy Beyond Replication

**Principle:** Replication is not a substitute for backups — you need both. Backups handle data corruption, accidental deletion, ransomware.

**Do:**
- Schedule backups with frequency aligned to your RPO.
- Store backups offsite or cross-region.
- Test restore procedures regularly.
- Use **AWS Backup** for centralized, multi-service backup management.
- Enable DynamoDB **PITR** (per-second, 35 days).

**Don't:**
- Rely on replication alone — logical corruption replicates too.
- Skip restore tests — backup integrity is unknown until restore.

**Code (book guidance):**
```text
AWS Backup capabilities:
  - Centralized multi-service backup (EC2, EBS, RDS, DynamoDB, EFS, Storage Gateway)
  - Scheduled (hourly/daily/weekly/monthly/yearly)
  - Cross-region / cross-account copy
  - Point-in-time recovery
  - Automatic transition to S3 Glacier for archival
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Importance of Backups"*

---

### Cluster 66 — Multi-Region Business Decision Heuristics

**Principle:** Multi-region is not for every workload. Reserve it for workloads where the business case justifies cost and complexity.

**Do:**
- Use multi-region for **latency-sensitive global apps**, **data sovereignty** requirements, **regional disaster recovery**.
- Weigh ROI against additional infrastructure, operational complexity, and consistency challenges.
- Apply only to specific workloads within your portfolio, not all.

**Don't:**
- Adopt multi-region "to be safe" without a clear driver.
- Underestimate cross-region data transfer costs.

**Code (decision matrix):**
```text
Workload characteristic              Multi-region warranted?
-------------------------------      ------------------------
Global user base + low latency req   Yes
Data sovereignty compliance          Yes
Mission-critical + zero-downtime     Yes
Single-region user base              No — multi-AZ suffices
Low traffic, non-critical            No — single AZ may suffice
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — "The Business Case for Multi-Region Architectures"*

---

### Cluster 67 — Anti-Patterns to Avoid

**Pattern: Hardcoded service endpoints in code**
- *Why bad:* Production code can point to test endpoints — financial consequences.
- *Fix:* Use SSM Parameter Store + Python script (Vite `import.meta.env`) for environment-specific config.

**Pattern: Multi-AZ not configured**
- *Why bad:* Single-AZ deployment is a SPOF.
- *Fix:* Multi-AZ for ALB, ECS, RDS, Aurora, ElastiCache.

**Pattern: Synchronous chain of cross-service calls**
- *Why bad:* One slow service blocks the whole chain.
- *Fix:* Async fire-and-forget with SNS+SQS for control-plane operations.

**Pattern: No idempotency on mutating endpoints**
- *Why bad:* Network retries cause duplicate charges/accounts.
- *Fix:* Lambda Powertools idempotency + DynamoDB persistence layer.

**Pattern: Credentials cached forever**
- *Why bad:* Secrets Manager rotation breaks the app.
- *Fix:* Secrets Cache + `@connection_aware` decorator for self-healing.

**Pattern: Connection pool per task with no proxy**
- *Why bad:* ECS scale-out exhausts DB connections.
- *Fix:* RDS Proxy at 95% of available connections.

**Pattern: Health checks without alarms**
- *Why bad:* Alarms need thresholds and notifications.
- *Fix:* Always pair CloudWatch Synthetics / RUM / metric filters with SNS alarms.

**Pattern: No per-AZ metrics**
- *Why bad:* Zonal impairments go unnoticed.
- *Fix:* Add `AvailabilityZone` dimension to all metrics.

**Pattern: No circuit breaker for known-flaky dependencies**
- *Why bad:* Persistent failures saturate threads/connections.
- *Fix:* Circuit breaker with `failure_threshold`, `recovery_timeout`, half-open testing.

**Pattern: No deployment circuit breaker**
- *Why bad:* Bad container deploys wait 3 hours for CloudFormation timeout.
- *Fix:* Enable ECS deployment circuit breaker + rollback on failures.

**Pattern: Manual failover**
- *Why bad:* Humans make errors under pressure.
- *Fix:* SSM Automation runbooks, rehearsed quarterly.

**Pattern: Single-region with manual DR**
- *Why bad:* RTO is hours/days.
- *Fix:* Aurora Global + DynamoDB Global Tables + Route 53 failover + STOP pattern.

**Pattern: Untested DR plan**
- *Why bad:* Paper plans fail at the worst time.
- *Fix:* Regular game days + AWS FIS chaos experiments.

**Pattern: Configuration drift between regions**
- *Why bad:* Failover behavior becomes unpredictable.
- *Fix:* IaC (CloudFormation/CDK/StackSets) + AWS Config + audits.

*Ref: Engineering_Resilient_Systems_on_AWS.md — all chapters*

---

### Cluster 68 — Decision Heuristics Quick Reference

| Question | Choose |
|---|---|
| Async or sync request flow for control plane? | **Async** (fire-and-forget SNS+SQS) |
| Throttle strategy for inbound API? | **API Gateway throttle + WAF rate limit** (defense in depth) |
| Need to handle duplicate submissions? | **Lambda Powertools idempotency** (always) |
| Poison pill handling? | **SQS + Lambda ESM + DLQ** with `report_batch_item_failures=True` |
| Bad container deploy detection? | **ECS deployment circuit breaker + rollback** |
| DB connection exhaustion in Fargate? | **RDS Proxy at 95% + Aurora defaults + read-only endpoint** |
| Hard dep on Secrets Manager? | **Secrets Cache** for soft dependency |
| Multi-rotation password refresh? | **`@connection_aware` decorator** for self-healing |
| Intermittent dependency failure? | **Retry with exponential backoff + jitter** |
| Persistent dependency failure? | **Circuit breaker** (closed → open → half-open → closed) |
| Timeouts across stack? | **Coordinated stack**: each upstream > downstream max |
| Frontend unhealthy dependency? | **Graceful degradation + heartbeat + hide form + fallback message** |
| Frontend error visibility? | **CloudWatch RUM + JsErrorCount alarms** |
| Cross-service debugging? | **X-Ray** (RUM → API GW → SNS → SQS → Lambda) |
| Regional failover decisioning? | **STOP pattern** (secondary-driven switchover) |
| Cross-region DB replication? | **Aurora Global Database** (storage-based, subsecond) |
| Cross-region NoSQL? | **DynamoDB Global Tables** (LWW or custom Lambda resolution) |
| DNS failover trigger? | **Route 53 + CloudWatch alarm on custom metric** |
| Orchestrate multi-step failover? | **SSM Automation** (run from secondary region) |
| Config drift prevention? | **IaC + AWS Config + StackSets + audits** |
| Zonal impairment mitigation? | **ARC zonal shift + cross-zone LB disabled + per-AZ metrics** |
| Kafka partitions tuning? | **Partition count = peak consumer parallelism; replication factor ≥ 3** |
| Kafka consumer scaling? | **Auto-scale on ConsumerLag metric** (add > 100, remove < 100) |
| Poison pill in Kafka? | **Schema validation (jsonschema) + DLQ + structured error logging** |
| High-contention state updates? | **Pessimistic concurrency** (Redis lock / ZooKeeper / etcd) |
| Low-contention state updates? | **Optimistic concurrency** (DynamoDB etag + ConditionExpression) |
| Singleton service HA? | **Leader election with Redis lock** (TTL, polling standby) |
| Heterogeneous workload isolation? | **Bulkhead pattern** (separate ECS services per work type) |
| Decoupled event routing? | **EventBridge + choreographed filtering** (vs SQS) |
| Heterogeneous data sync? | **CDC + CQRS** (Redis Streams → OpenSearch) |
| Multi-region search? | **OpenSearch CCR** (unidirectional or bidirectional with merge script) |
| Multi-region Kafka? | **Kafka MirrorMaker** + consumer-side idempotency |
| Multi-region cache topology? | **Regional / Global / Hybrid** per access pattern |
| Consistency model? | **CAP during partitions; PACELC normally** (be explicit) |
| Replication topology? | **Active-passive** for strong consistency; **active-active** for write latency |
| Test resilience continuously? | **AWS FIS** (built-in experiments first) |
| Safe deployment? | **Blue-green via regional switchover** + `greentest_` prefix |
| Incident learning? | **Blameless postmortems + resilience backlog + champions network** |

*Ref: Engineering_Resilient_Systems_on_AWS.md — entire book*

---

### Cluster 69 — Key Takeaways

1. **Resilience is a shared responsibility.** AWS guarantees "of the cloud"; you own "in the cloud." Misunderstanding this division is the root of most outages.
2. **Use RAF/SEEMS as your taxonomy.** Every failure mode is S, E, E, M, or S. Every defense should map to one.
3. **Layer your defenses.** No single pattern is sufficient — combine WAF + throttling + retries + circuit breaker + DLQ + failover.
4. **Coordinate timeouts.** Each upstream timeout must exceed the downstream maximum; cascading failures start with uncoordinated timeouts.
5. **Make mutating endpoints idempotent.** Lambda Powertools + DynamoDB persistence + `request_token` is the gold standard.
6. **SQS + Lambda ESM + DLQ is your asynchronous self-healing chassis.** `visibility_timeout = 6 × Lambda timeout` is the rule.
7. **Treat the database as a SPOF risk.** Aurora defaults, RDS Proxy, Secrets Cache, `@connection_aware` are not optional in elastic compute.
8. **Use ECS deployment circuit breaker.** Bad deploys detected in minutes, not hours.
9. **Graceful degradation is a UX feature.** Hide broken forms, show fallback paths, keep core functionality.
10. **STOP (Standby Takes Over Primary) is your regional switchover pattern.** Drive from secondary; use S3 indicator file.
11. **SSM Automation runbooks for orchestrated failover.** Switchover → SToP file → alarm trigger, all in one document.
12. **Per-AZ metrics are non-negotiable.** Add `AvailabilityZone` dimension to everything.
13. **Configuration drift kills failover.** Use IaC, StackSets, AWS Config, audits.
14. **Zonal shift requires cross-zone LB disabled** + per-AZ metrics + ARC.
15. **Kafka partitions and replication factor matter.** 6 partitions × 3 replicas in the book; tune to your consumer parallelism and durability needs.
16. **Optimistic vs pessimistic concurrency** is a workload decision — don't default.
17. **Producer-Consumer + leader election** decouples concerns but requires idempotent consumers.
18. **Bulkhead + EventBridge** isolates failure domains with flexible routing.
19. **CDC + CQRS** bridges heterogeneous data stores without coupling writes to reads.
20. **Multi-region is a tool, not a silver bullet.** Match the strategy to the workload.
21. **Test resilience continuously** — FIS experiments, regular game days, blameless postmortems.
22. **Anti-fragility is the goal.** Systems should *improve* from disorder, not just survive it.

*Ref: Engineering_Resilient_Systems_on_AWS.md — "Putting It All Together" (Ch 11)*

---

### Cluster 70 — Reliability Pattern Lookup by Failure Mode

```text
SEEMS Category        Reliability Patterns                                  AWS Services
------------------    ----------------------------------------------------  --------------------------------------
Single Point of       Multi-AZ, multi-region, OAC, failover                 CloudFront, S3 CRR, ALB, ECS, Aurora
Failure                                                                       Global, DynamoDB Global Tables, Route 53

Excessive Load        Rate limiting, throttling, autoscaling, queues,       WAF, API Gateway, SQS, Lambda ESM,
                      load shedding                                         DynamoDB, Aurora Serverless v2

Excessive Latency     Caching (edge + application), timeouts, retries,      CloudFront, ElastiCache, RDS Proxy,
                      circuit breakers, async architecture                  Lambda async, AbortSignal.timeout

Misconfigurations/    IaC, JSON Schema validation, deployment circuit       CDK, CloudFormation, API Gateway
Bugs                  breakers, blue-green deploys, feature toggles         JSON Schema, ECS deployment CB,
                                                                             Lambda aliases, API Gateway stages

Shared Fate           Multi-region, multi-AZ, bulkheads, sharding,          Aurora Global, DynamoDB Global,
                      graceful degradation                                  ElastiCache, EventBridge, CDC+CQRS
```

*Ref: Engineering_Resilient_Systems_on_AWS.md — Ch 11 Table 11-1*

---

## Anti-Patterns & Common Mistakes

| Pattern | Why It's Bad | Fix |
|---|---|---|
| Hardcoded API endpoints in code | Cross-env misconfig = prod→test | SSM Parameter Store + Vite `import.meta.env` + CI/CD automation |
| Single-AZ deployment | One AZ outage = total outage | Multi-AZ for all data plane services |
| Synchronous long chains | Slow service blocks whole chain | Async SNS+SQS for control plane; circuit breakers for sync calls |
| No idempotency on mutations | Retries cause duplicate writes | Lambda Powertools + DynamoDB persistence + client UUIDs |
| Cached creds forever | Password rotation breaks app | Secrets Cache + `@connection_aware` |
| No RDS Proxy in Fargate | ECS scale-out exhausts DB conns | RDS Proxy @ 95% of available connections |
| Health checks without alarms | Nothing fires when health degrades | Pair every canary/RUM/metric filter with SNS alarm |
| Aggregated AZ metrics | Zonal issues hidden | Add `AvailabilityZone` dimension to every metric |
| No deployment circuit breaker | 3-hour CloudFormation timeout on bad deploys | ECS deployment CB + rollback on failures |
| Manual failover under pressure | Humans make errors during incidents | SSM Automation runbooks, rehearsed quarterly |
| Cross-zone load balancing always on | Zonal shift can't exclude impaired AZ | `load_balancing.cross_zone.enabled = false` on target groups |
| Single-region with paper DR plan | Untested DR fails in real disaster | Game days + AWS FIS chaos experiments |
| Configuration drift between regions | Failover becomes unpredictable | IaC (CDK/StackSets) + AWS Config + audits |
| Consumer groups without lag monitoring | Lag spikes go unnoticed | CloudWatch ConsumerLag alarm per consumer group |
| Synchronous multi-region writes | High latency, conflict complexity | Active-passive (single writer) or active-active with conflict resolution |
| Consumers auto-commit before processing | Duplicates on restart | `enable_auto_commit=False`, explicit commit after processing |
| Schema-less message contracts | Breaking changes fail consumers | Message envelope + version declaration + Glue Schema Registry |
| Polling on tight loops without jitter | Synchronized spikes | Jitter + exponential backoff |
| Skipping rehearsal of runbooks | Plans fail at the worst time | Quarterly game days + FIS experiments |
| Treating alarms as failure signals only | Miss leading indicators | Composite alarms + SLI dashboards |

---

## Cross-References

- Related book deep-dive: *(none yet in this collection)*
- Topic index: `best_practices/INDEX.md`

---

## Source Citation Index (for fast reference)

| Cluster | Book section |
|---|---|
| 1–4 | Ch 1: "Shared Responsibility Model", "Setting Objectives", "AWS Resilience Analysis Framework" |
| 5–7 | Ch 1: "Disaster recovery strategies", "High availability", "Quotas" |
| 8–10 | Ch 1: "Change Management", "Failure Management", "Observability" |
| 11–12 | Ch 1: "Continuous Testing and Chaos Engineering", "CI/CD and Automation" |
| 13–16 | Ch 3: "Addressing Single Points of Failure", "Implementing Amazon CloudFront origin failover", "Balancing caching and resilience for consistent latency", "Preventing excessive load with rate limiting", "Implementing Observability" |
| 17–21 | Ch 4: "Technical Requirements", "Architecture Overview", "Strongly Typed Service Contracts", "Idempotent Responses", "Self-Healing with Message Queue Retries", "Rate Limiting: Throttle Unanticipated Load" |
| 22 | Ch 5: "Container Deployment Failures" |
| 23–25 | Ch 5: "Database Connection Exhaustion", "Database Password Rotation Login Failures" |
| 26 | Ch 5: "Database Primary Writer Failures" |
| 27–28 | Ch 5: "Dependency Intermittent Failures", "Dependency Outages" |
| 29 | Ch 6: "Configuring Client Timeouts" |
| 30 | Ch 6: "Gracefully Degrading Features" |
| 31–32 | Ch 6: "Real User Monitoring", "X-Ray for End-to-End Tracing" |
| 33 | Ch 4 + Ch 7: "STOP: Business Continuity Regional Switchover" |
| 34–35 | Ch 7: "Database Failover and Switchover", "Amazon DynamoDB global tables" |
| 36–37 | Ch 7: "DNS Failover", "Deploying the AWS CDK Orchestration Stack" |
| 38 | Ch 7: "Avoiding Configuration Drift" |
| 39 | Ch 5: "Detecting and Handling Availability Zone Issues" |
| 40–41 | Ch 8: "Designing the Kafka Topic Structure", "Securing the Kafka Cluster" |
| 42–43 | Ch 8: "Implementing Reliable Consumers", "Consumer Groups and Record Processing" |
| 44 | Ch 8: "Handling Invalid Messages" |
| 45–47 | Ch 8: "Handling Concurrency", "Designing Consumer State", "Using Restartability" |
| 48–49 | Ch 9: "Producer-Consumer Pattern for Article Processing", "Leader Election for Scheduler High Availability" |
| 50 | Ch 9: "Additional Resiliency Strategies" |
| 51–52 | Ch 9: "Syncing Articles to OpenSearch", "Serving Search Traffic" |
| 53–54 | Ch 10: "Replicating Kafka Data Across Regions", "Cross-Region Data Replication with OpenSearch", "Handling Conflict Resolution" |
| 55–57 | Ch 10: "Caching in Multi-Region Architectures", "Understanding Consistency Models", "Replication Strategies" |
| 58–59 | Ch 8: "Storing and Querying Processed Market Data", "Handling Firehose Failure Modes", "Querying Athena" |
| 60 | Ch 8: "Monitoring and Observability" |
| 61 | Ch 8: "Testing Resiliency" |
| 62 | Ch 4: "Blue-Green Testing" |
| 63–64 | Ch 11: "Leading Resiliency Initiatives", "Sharpening Your Resilience Radar" |
| 65 | Ch 7: "Importance of Backups" |
| 66 | Ch 10: "The Business Case for Multi-Region Architectures" |