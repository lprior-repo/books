# Observability Engineering (2nd Edition, Early Release) — MAXIMUM-DEPTH Deep Dive
**Authors:** Charity Majors, Liz Fong-Jones, George Miranda
**Topic tags:** `#observability` `#reliability` `#performance` `#cost-engineering` `#kubernetes` `#llm` `#ai` `#evals` `#profiling` `#flame-graphs` `#slo` `#architecture` `#testing`
**Language focus:** Language-agnostic (Go, Python, JavaScript examples; OTel, Pyroscope, Honeycomb specifics)
**Sources:** `markdown_output/Observability_Engineering_2nd_Ed_ER_-_Charity_Majors/Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md` (1115 lines; Early Release: only Chapters 1, 2, and 22 are available — "What Is Observability?", "Performance Engineering", "AI Observability")

> **Scope:** This edition is an Early Release. Only chapters 1, 19 ("Performance Engineering"), and 22 ("AI Observability") are available. Coverage here is restricted to those three chapters with full fidelity, plus the cross-chapter framing the authors lay down in chapter 1 (dependability properties, Kálmán framing, "How Observable Is Your Software?" litmus test, three-pillars fallacy, qualification levels). Future readings must add: telemetry pipeline (Ch 7-8, 17-18), OpenTelemetry instrumentation (Ch 6), SLO/SLI practice (Ch 11-12), supply chain (Ch 13), ROI/BvB (Ch 15), frontend observability (Ch 23), line-of-code observability (Ch 24), maturity model (Ch 25).

## TL;DR
Observability is *not* a vendor category or synonym for monitoring; it is a qualitative property of dependable software that measures how well any internal state can be inferred from external outputs — even unrepeatable "unknown unknowns." Treat logs, metrics, and traces as **one unified wide-event datastore** rather than three siloed "pillars" — this is observability 2.0 vs the pillars-era observability 1.0. Apply the same discipline to AI/LLM features — design telemetry, run evals + observability together, feed production data back into golden sets, **intervene programmatically on correctable structured outputs** (Honeycomb Query Assistant: 25% → 14% via fix-ups before any prompt-engineering work). For latency mysteries, **CPU profiling** (Go `pprof`, then continuous profilers like Pyroscope / Polar Signals / Blackfire / OTel profiling) often finds what tracing and metrics cannot — *combine* tracing + profiling by indexing profiles per second or per-span to close the "what was slow, for whom, and why" gap. Cost engineering is observability: heatmaps beat percentiles on saturated nodes, "1% off 10%" beats "5% off 1%", plot sum of CPU + memory by service/daemonset. SLOs are connective tissue — alert into Slack/Teams, never PagerDuty; iterated thresholds must actually fire occasionally.

---

## Best Practices by Topic

### Observability as a Property of Dependable Software (Laprie 1995 + Kálmán 1960)

**Principle:** Observability is *not* a vendor category or synonym for monitoring; it is a qualitative property of software dependability. It measures how well any internal state can be inferred from external outputs — even unrepeatable "unknown unknowns."

**Do:**
- Gauge observability qualitatively: low / medium / high, like availability or reliability (Laprie 1995).
- Add observability to Laprie's classic dependability properties (availability, reliability, safety, security, integrity, maintainability).
- Combine observability with all four dependability techniques: fault prevention, fault tolerance, fault removal, fault forecasting.
- Treat observability as sociotechnical — it spans the system, environment, and humans interacting with it.
- Borrow Kálmán's framing when defending telemetry investment: *"a measure of how well internal states of a [system] can be inferred from knowledge of its external outputs."*

**Don't:**
- Don't equate observability with monitoring, dashboards, or "did the alert fire."
- Don't reduce observability to "nines" (99.9% vs 99.99%) — those measure availability, not trustworthiness.
- Don't assume a system with traditional monitoring is "fully observable" in any meaningful sense.

**Dependability properties (Laprie 1995, extended):**
```
Availability     — readiness for usage
Reliability      — continuity of service delivery
Safety           — no catastrophic consequences on the environment
Security         — no unauthorized disclosure of information
Integrity        — no improper alterations of information
Maintainability  — aptitude to undergo repairs and evolution
Observability    — ability to understand or debug any given system state  (added)
```

**Dependability techniques (Laprie):**
```
Fault prevention  — preventing the introduction or occurrence of faults
Fault tolerance   — providing capable service functions despite active faults
Fault removal     — reducing the presence (number, seriousness) of faults
Fault forecasting — estimating the present number or the future incidences
```
**Observability is not "another technique"** — it amplifies all four. Each preventive measure is validated by observable evidence; each tolerant system needs observability to declare what was tolerated; each removal shows up in observability data; each forecast trains on observability-derived trends.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Properties of software dependability" / "The Mathematical Definition of Observability" / "Observability is a property of dependable software"*

---

### Kálmán's Mathematical Definition — Adapted for Software

**Principle:** Rudolf E. Kálmán's 1960 control-theory observability — *"a measure of how well internal states of a [system] can be inferred from knowledge of its external outputs"* — is the right mental model for software, even though the math (linear algebra, sensors, formal methods) doesn't transfer.

**Do:**
- Keep the Kálmán framing in mind when arguing for instrumentation investment with leadership.
- Use the framing to defend end-to-end tracing investments over narrow metric dashboards.
- Recognize that "traditional control theory" treats observability/controllability as duals with linear algebra and sensors; software translation emphasizes *open-ended interrogation*.

**Don't:**
- Don't conflate Kálmán's formal control-theory observability with software observability — they share a name, not a body of practice.
- Don't dismiss the math because you're "just writing CRUD"; the framing is a useful forcing function for *what data you must emit*.

> Adapting Kálmán: the "external outputs" of a microservice are its events — requests served, errors thrown, log lines emitted, traces started, spans finished. The "internal state" includes user-visible behavior, internal state machines, performance counters, anything the engineer wants to know. **Observability = can we infer the state we want, from the outputs we have, in seconds?**

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "The Mathematical Definition of Observability"*

---

### The Three Pillars Fallacy → Unified Data Store (The Paradigm Shift)

**Principle:** "Three pillars" (logs / metrics / traces) emerged historically from separate tools with separate datastores. The cognitive overhead of manually correlating across them is the real cost. **The paradigm shift** is unifying them into one datastore holding wide events — observability 2.0 vs the pillars-era observability 1.0.

**Do:**
- Default to a single wide-event datastore (a single backend, even if visualization layers differ).
- Capture everything about an interesting occurrence in the same event (user, request, env, trace context, business attrs).
- Interrogate data with arbitrary grouping/filtering in seconds, not pre-aggregated dashboards.
- Pick tooling on outcomes enabled, not on which "pillar" it claims to serve.

**Don't:**
- Don't fragment your team across log, metric, and trace vendors that don't share a query layer.
- Don't accept vendor framing that "observability = logs + metrics + traces" without the *unification* part — without unification, you have re-architected the same correlation problem.
- Don't version observability ("Observability 3.0/4.0/5.0") as a marketing contest — the only paradigm shift the authors defend today is unification of external outputs.

> "What sparked the revolution of 'observability' was using a unified data store to gather all external outputs from your software. Unifying external system outputs obviated the need for artificial correlations between different data types."

**A note on multi-store pragmatism:** unified ≠ single-vendor. Unified means a single *query layer*. If you can join log and trace data by a `trace_id` field across two tools, you have the benefits of unification even if storage differs. But three *disconnected* query layers → three observability sub-systems → correlation tax preserved.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Technological Step Changes in Observability"*

---

### Qualitative Self-Assessment — "How Observable Is Your Software?"

**Principle:** You don't need a numeric grade; ask open-ended questions and answer yes/no. A system is highly observable when you can answer new questions about previously-unseen system states within seconds, using only external tools and without shipping new code.

**Litmus-test (verbatim from the chapter):**
```
- Can you answer open-ended questions about the inner workings of your applications
  without investigative dead ends?
- Can you see any user at any given time, in real time?
- Can you slice performance from aggregate → single request, on demand?
- Can you compare arbitrary groups of users to find shared attributes?
- Can you search all requests for similar patterns?
- Can you find the top-N most load-generating users (and which just joined)?
- Can you isolate the 142nd-slowest user's traces specifically?
- Can you find hidden timeouts even when p99.99 looks fine?
- Can you do this without pre-planning specific monitors in advance?
- Can you do this for issues you've never seen before?
- Can you iterate from question to answer in seconds (not minutes)?
- Do debugging investigations routinely surface surprising findings?
- Can you isolate any fault, no matter how complex, within minutes?
```

**Do:**
- Periodically test your team with these questions in the book.
- Track which questions your team *cannot* answer with current tooling — those are gaps.
- Aim for "any engineer, regardless of experience" being able to diagnose, not just Mr.-Scott-style intuition.
- Promote debugging from "weeks of tribal knowledge" to "minutes of data."

**Don't:**
- Don't ship a feature unless you can answer the chapter's mandatory self-check.
- Don't accept "we'll set up another dashboard" as the answer to a question your existing observability can't answer.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "How Observable Is Your Software?"*

---

### The "High-Observable-Software" Conditions (Four Axioms)

**Principle:** Quantify "high observability" with four bullets, then ask the litmus-test questions above.

**A high-degree-of-observability software system lets you:**
1. Understand the inner workings of your application.
2. Understand any system state your application may have gotten itself into, even new ones never seen before or predicted.
3. Understand the inner workings and system state *solely by observing and interrogating with external tools*.
4. Understand the internal state *without* shipping any new custom code to handle it (because that implies you needed prior knowledge to explain it).

**Why these are the right axioms:** Condition #4 is the disqualifier. If you have to push a new code path to debug a state, you didn't have observability — you had monitoring + the ability to ship code.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "In a software system with a high degree of observability you would be able to do the following"*

---

### Cloud-Era Failure Modes — Partial Failures & "Inexplicable Slowness"

**Principle:** In distributed-by-default systems, partial failures and "inexplicable slowness" are the *most common* failure mode — not binary up/down. Traditional monitoring was built for the latter and is "woefully inadequate" for the former.

**Do:**
- Treat latency variance and "no smoking gun" as first-class failure states.
- Look for partial-failure patterns: regional config drift, partial LB degradation, progressive-delivery skew, opaque third-party SLAs.
- Build the *why* (root cause) into your instrumentation, not just whether the system responded.
- Acknowledge the alerting-system weakness: "more sophisticated monitoring can attempt to correlate or collapse [alerts] into a more meaningful signal (with varying degrees of success)."

**Don't:**
- Don't only alert on aggregate state (up/down).
- Don't assume 100% availability means user happiness — "Availability is still 100%, but your users are unhappy because transactions are slow."
- Don't rely solely on tribal knowledge ("the speed that we were traveling by the feel of the deck plates").

**Common partial-failure scenarios (read with empathy):**
- A file you didn't know about has a default config pointing to `us-east-1` → users outside NA suffer.
- A partially degraded load balancer — one-hundredth of requests see retries → 100% availability, slow users.
- Progressive-delivery skew — only the new (deployed) version is slow.
- Third-party SaaS dependencies where you can't even observe their internals.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Observability is a property of dependable software"*

---

### Profiling-Instrumentation for Latency Mysteries — Honeycomb PProf Case Study

**Principle:** When load-balancer latency and trace-span latency disagree and "time is going missing," CPU/heap profiling (e.g., Go `pprof`) often fingerpoints the framework code (router regex compilation, JSON serialization in tight loops). Profiling finds what tracing and metrics *can't* — per-function, per-line, per-instruction.

**Honeycomb incident (Dec 2021, the book's case study):**
> "We expose the net/http/pprof endpoint on our pods, so it was a matter of running the go tool pprof utility as a one-off to obtain a flame graph … The regexp.Compile path shouldn't have been 17% of all CPU … Why were we re-initializing the http router mux and reparsing its configuration over and over? A dive into the code confirmed that the HTTP router was being discarded after each request rather than being reused as a singleton. **The fix to the slow performance impacting our customers was just 5 lines of code.**"

**Do:**
- Always expose `net/http/pprof` (or equivalent) on a *non-internet-visible* port in production pods.
- Sample on the order of ~10 ms in prod (lightweight, statistically representative).
- Use flame graphs for at-a-glance identification: width = total time in function; stacking = child calls.
- Interpret a wide flame-bottomed, tall-leafy framework block as "your hot path is in shared library code, not yours."
- Extend profiling to fleet-wide continuous profiling (Grafana Pyroscope, Polar Signals, Blackfire, OpenTelemetry profiling signal).

**Don't:**
- Don't ship re-creating-the-router-on-every-request code paths.
- Don't pin blame only on your code — profiling will routinely show 17% of CPU in regex/mux/stdlib.
- Don't interpret profiles in isolation; *correlate with traces* (a slow function in a profile may not lie on the slow path for a particular request).
- Don't over-sample (every-ms profiling in prod introduces overhead and skews results).

**Why the bug evaded tracing alone:** "we could not have caught the problem with tracing alone, as the tracing hook is called by the mux router *after* it has already been instantiated, for each request once it has already been matched to a route." Tracing hooks into the *boundary*, profiling hooks into the *runtime* — different observation points catch different bugs.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "A dive into the code confirmed" (Performance Engineering chapter) / "The Case for Performance Engineering"*

---

### Cost vs. Performance — Routing Decisions Beyond Speed

**Principle:** Performance engineering optimizes *outcomes* — cost and customer experience — not raw latency. Optimizing for speed first is usually right because faster execution is most visible and most directly translates to a lower bill, *but* faster memory, faster network, and right-sized instances also matter. Some performance wins won't show up as latency reduction at all.

**Do:**
- Ask "is this faster because of more/faster memory or network?" as a routine engineering question — instances with the same CPU class can have radically different memory bandwidth and NIC speeds.
- Use serverless as a built-in optimization — shorter Lambda execution = lower bill; convert span duration into additive cost surfaces in your observability tool.
- Ingest the cloud bill into your observability tool to spot the largest spend buckets and drill into common tags/attributes.

**Don't:**
- Don't treat "faster" as the only optimization axis — sometimes doubling memory bandwidth at +20% cost halves request time and reduces compute spend.
- Don't skip the cost dimension when the AWS bill dwarfs your LLM bill — engineering time is the most expensive line item.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Observing the cost profile"*

---

### Compute Cost Is Multi-Dimensional — Memory + Network + Time

**Principle:** Cost optimization isn't "make it faster." Memory bandwidth, network, and instance family materially change $/request. Observability must surface cost dimensions alongside request metrics.

**Do:**
- Ingest cloud-bill data into your observability tool to spot the largest spend buckets and drill into common attributes.
- Treat "is this faster because of more/faster memory or network?" as a routine engineering question.
- Use serverless as a built-in optimization: shorter Lambda execution = lower bill; convert span duration into additive cost.

**Don't:**
- Don't settle for "time" as the only cost dimension.
- Don't trust dashboards that aggregate cost without attribution to specific services/tenants/regions.

> "It's important to consider that there are multiple dimensions to the cost profile of your compute layer. It's not simply 'time', since the different machines and instance sizes also have an impact on price which is where we can use performance engineering to optimise beyond just 'make it faster'."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Observing the cost profile"*

---

### Performance Engineering as a Continuous, Team-Wide Practice

**Principle:** Performance engineering isn't a one-and-done activity: it's a scale with diminishing returns at the top, large gains early, and continuous reinforcement. The core loop is **measure → change → measure → repeat**. By late 2024 at Honeycomb, **6 teams** were each finding value from continuous profiling — the practice broadens, not narrows.

**Do:**
- Run as a continuous iteration, not a one-off initiative.
- Give the practice to many teams (don't silo it into a performance engineering team).
- Fuse performance + cost + observability into one platform (fin-eng collaboration on AWS bill + telemetry + cluster data).
- Quantify optimizations in latency, data size, dollars, **or effective tons of CO₂ emission**.
- Use Brendan Gregg's *BPF Performance Tools* / *Systems Performance* for further depth.

**Don't:**
- Don't think continuous optimization is "squeeze one bug, done."
- Don't keep performance engineering a separate discipline — it shares the goal, tooling, and culture with observability.
- Don't confuse infrastructure laziness ("fewer instances") with cost engineering ("cheaper outcomes").

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Performance Engineering Introduction / Conclusion*

---

### CPU Profiling — Sampling, Ring Buffers, Statistical Aggregation

**Principle:** Profilers interrupt the program with OS signals, capture the program counter + stack, and write to a ring buffer; periodic readers aggregate counts and reconstruct flame graphs. Same statistical principle as distributed-trace sampling.

**Sampling math:**
- Every 1 ms → too much overhead, distorts behavior.
- Every ~10 ms → statistically representative, minimal overhead.
- Below 10 ms → profiling cost dominates run cost.
- Above 100 ms → miss the actual hot functions.

**Don't:**
- Don't over-sample (1 ms = lots of overhead).
- Don't under-sample (the cliff between 10 ms and 100 ms is steep).
- Don't profile a binary without symbols — provide the original source AND the original binary for assembly-level detail.

**How to invoke `pprof`:**
```bash
# Grab a profile over 30s while reproducing the slowness.
curl 'http://localhost:6060/debug/pprof/profile?seconds=30' > cpu.pprof
go tool pprof -http :8080 cpu.pprof
# interactive web UI: choose flame graph view from the visualization menu
```
*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Introducing CPU profiling tools" / "Setting up and interpreting profiling data"*

---

### Flame Graphs — The Primary Lens for Profiling Data

**Principle:** Flame graphs reveal two things at a glance: (1) is your code or library code the bottleneck, (2) is the time attributable to a function vs its children.

**Reading:**
- **Width** = total time spent in function AND its children.
- **Stacking** of one function beneath another = child function call.
- **Icicles / flames** = collections of full stack traces sharing the same call order.
- **Wide-at-the-bottom, tall-on-top** = leaf-level hotspots in your code (lowest-hanging fruit).
- **Wide-at-the-top** = heavy framework / library code dominating your stack.

**Do:**
- Run `go tool pprof -http :8080` (or equivalent) for an interactive web UI; choose flame graph view.
- Look for wide, hot functions with little child time (often functions near the flame root).
- Optimize functions called *often with medium size* — they dwarf thin-slice functions.

**Don't:**
- Don't settle for raw source listings or full DAG renderings for at-a-glance insight.
- Don't spend time optimizing a function that only contributes a thin slice of the total bar — pick wide, hot functions.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Setting up and interpreting profiling data" / flame graph descriptions*

---

### Profiling + Tracing Combined — "Magic" Together

**Principle:** Profiling gives *inner-function* but *process-wide* granularity; tracing gives *outer-function* but *per-request* granularity. Combining them (per-trace-span profiles, or per-second indexed profiles) closes the gap: you get *what was slow*, *for whom*, and *why/how*.

**Do:**
- Adopt tools that index profiles at per-second granularity (Pyroscope-style) or tie profiles to specific trace spans.
- Use combined data to attribute slow requests to specific user behaviors (per-customer CPU hotspots).
- Let this guide "optimize where it matters" — feature teams can ship inscrutable dense code in cold paths, while the profiler shows you exactly where to ratchet tight loops.

**Don't:**
- Don't settle for either-or. Profiles without per-request attribution miss user-specific hotspots. Tracing without inner-function detail misses CPU hotspots.
- Don't *pre-optimize* dense code without a profiler — you'll guess wrong.

**Honeycomb example — customer-specific hot spot in serializing from protobuf to JSON:**
> User's query which took so long to encode was also slow running on Lambda because it contained so many distinct abstract syntax tree (AST) nodes. … The customer was using an if { } else { if { } else { if { } else { if { } else { … } else { … } } } } } pattern, which we could simplify by offering a switch statement. Once we transformed away the complexity of the query and refactored the customer's query to use the new syntax, execution was dramatically faster.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Blending performance engineering and observability"*

---

### Continuous Profiling — Always-On, Not On-Call

**Principle:** Profiles aren't a "pull when paged" tool. Continuous profiling agents (Grafana Pyroscope, Polar Signals, Blackfire, OpenTelemetry profiling) capture even brief misbehaviors that disappear by the time you `curl /debug/pprof`. Data is highly redundant (function calls repeat) and compresses well (2 hours ≠ 120× a 1-minute profile).

**Do:**
- Adopt continuous profiling agents (Pyroscope / Polar Signals / Blackfire / OTel profiling).
- Co-locate profiling with traces (per-second indexed, or per-span) so you get request-level + per-function attribution in the same tool.
- Look for user-specific hot spots (a single customer's query shape pinning a CPU core is invisible at aggregate service-level).

**Don't:**
- Don't keep `pprof` exclusively for on-call — the bug will not be there at 2am.
- Don't fear disk cost; profiles compress dramatically.
- Don't replace tracing with profiling — they're complementary lenses (forest vs tree rings).

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Scaling out profile collection and analysis" / "Blending performance engineering and observability"*

---

### Compose Compute Model to Workload — Six Purchasing Tiers

**Principle:** The medium is the model. The cost-vs-performance-vs-developer-ergonomics tradeoffs of compute options (CapEx, reserved, persistent, interruptible, elastic, FaaS) are not one-size-fits-all. **Pick per workload, revisit based on observability.**

**Compute procurement models (verbatim):**
```
- Capital expenditure (building your own datacenter, e.g. Oxide Computer)
- Reserved capacity (AWS Savings Plans, Azure Savings Plan, Google Committed/Sustained Use Discount)
- Persistent, defined capacity (AWS EC2, Azure VMs, Google Compute Engine)
- Interruptible, defined capacity (AWS Spot, Azure Spot, Google Preemptible)
- Persistent, elastic capacity (AWS Fargate, Azure Container Apps, Google Cloud Run)
- Interruptible & flexible, for short requests (AWS Lambda, Azure Functions, Google Cloud Functions)
```

**Do:**
- Mix models: persistent VMs (or managed RDS) for databases, serverless frontends, Fargate/Cloud Run for batch/stream workers.
- Use FaaS for *spiky revenue-correlated* workloads — even if cold starts / refusals on big spikes happen, it can be acceptable.
- Use interruptible instances (Spot, Preemptible) with **Karpenter + Node Termination Handler** for stateless, fault-tolerant workloads.
- Switch to Arm (Graviton/Cobalt/Axion) when ROI is positive — re-build container images, test to breakage (SMT difference matters).
- Revisit models based on production telemetry — load profile, contention, cost per CPU-second.

**Don't:**
- Don't lock into a single compute model for the whole org.
- Don't pay perfect-utilization FaaS prices for steady-state workloads (reserved is cheaper).
- Don't claim a cloud vendor's "utilization" benefit makes the unit price irrelevant — compare actual TCO on observed workloads.
- Don't assume cognitive cost of operating physical servers is zero — it isn't.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Infrastructure purchasing models"*

---

### Cost Engineering Hooked to Observability — Squeezing, Optimizing, Migrating

**Principle:** Performance engineering complements (rather than competes with) observability. Both want lower costs and faster customer experiences; both share tooling. Optimization without measurement is "educated guesswork"; measurement without iteration stalls.

**Four fleet-wide levers (in order):**
1. **Squeezing** — reduce task counts, reduce CPU and memory allocations per task.
2. **Optimizing** — better algorithms; bin-pack harder.
3. **Migrating architectures** — compute-model swap; highest leverage, hardest, most disruptive.
4. **Measuring** — observability tells you which lever to pull.

**Do:**
- Set SLOs first (see "see how few machines you actually need to still achieve those SLOs").
- Plot *sum* of CPU + memory consumed per service/daemonset to find the biggest optimization opportunities (**1% × 10% > 5% × 1%**).
- Test against the latest-generation hardware and *until latency degrades* — don't trust "standard" SMT/SMT-off recommendations.
- Adopt Arm (AWS Graviton / Cobalt / Axion) for cost wins; re-pack containers for the new arch; test to breakage.
- For Kubernetes: enable interruptible instances with Karpenter + Node Termination Handler for stateless fault-tolerant workloads.
- Remove excess boot-volume size when logs are offloaded; consider local NVMe vs remote block storage.

**Don't:**
- Don't optimize without baseline measurements.
- Don't allocate *both* reserved capacity and persistent state blindly — match the workload's cost model (FaaS / reserved / interruptible / persistent).
- Don't run observability on the critical request path without ensuring it's well-instrumented (percentiles mislead for saturated nodes — heatmaps are preferable).
- Don't deploy new architecture without a cost-observability feedback loop.

> "While in the past standard practice was to run Intel architecture based instances with hyperthreading or simultaneous multi-threading (SMT) at 40% utilization, and Arm instances or those with SMT disabled at 70%–80%, that recommendation may no longer hold for the kinds of cores you are using. Test until latency actually begins to degrade."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "The Case for Performance Engineering" / "Fleet-wide optimization" / "Cost-optimizing Kubernetes"*

---

### Kubernetes Observability Toolkit — Heatmaps > Percentiles

**Principle:** When pod saturation varies wildly, percentiles mislead (a few hotspots skew p99). Heatmaps expose the *saturation profile* across instances — useful to spot clipping (100% saturation) on tail pods.

**Do:**
- Plot pod CPU + memory as heatmaps across nodes.
- Track kubeletstats via OTel Collector (**DaemonSet**) + k8sattributes processor for full attribution.
- Look for daemonsets overshooting 1 vCPU; pods stranding cores due to bin-packing failures.
- Trim excess boot volume when logs are exported off-node.

**Don't:**
- Don't rely on summary percentile dashboards for K8s saturation signals.
- Don't keep persistent boot volumes sized for log retention when logs are cloud-exported.

**OTel Collector DaemonSet for K8s:**
```yaml
receivers:
  kubeletstats:
    collection_interval: 10s
processors:
  k8sattributes: {}
exporters:
  otlphttp:
    endpoint: https://collector.example:4318
```

**Bin-packing arithmetic (verbatim):**
> "If a given machine has 32 cores, and you have pods that require 20 cores each, then 11 to 12 out of the 32 cores will be potentially wasted once daemonsets are accounted for, because you cannot fit two 20-core pods on the same machine, and daemonsets should take up a maximum of 1 vCPU in total. It's better in that case to up-size to 64-core machines so 3x 20 vCPU jobs will fit on one machine, or to run fewer, smaller tasks eg 15 vCPU per pod, to allow better bin-packing."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Cost-optimizing Kubernetes"*

---

### Why the "3 Pillars" Came To Be — Historical Context

**Principle:** The split into logs/metrics/traces isn't intentional design — it's historical accident driven by separate vendors with separate storage models. The "3 pillars" framing is descriptive of legacy tools, not prescriptive of how telemetry *should* be organized.

**Do:**
- Treat "pillars" as a useful *thinking tool* (each pillar highlights a different signal shape) but reject the implication that they belong in separate stores.
- Migrate toward the unified model incrementally; start with the new services.

**Don't:**
- Don't reorganize your teams around "the three pillars" — that's the model maintaining itself.
- Don't dismiss ML/GenAI tag enrichment as a substitute for unification — it's correlation-on-read, which is brittle and slow.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Technological Step Changes in Observability"*

---

### Observability vs Monitoring — Why the Distinction Matters

**Principle:** Marketing has flattened "observability = monitoring + LMT" when the deeper distinction is whether you can answer *new questions* about *unseen* system states without shipping code. Two vendors equally "covering the pillars" can have radically different observability depending on storage and query model.

**Do:**
- Judge observability tools by *the outcomes they enable*, not the dashboards they ship.
- Treat "vendor X tells me everything" with skepticism: full coverage of the three pillars without unification leaves you with the same correlation problem.
- Insist on the freedom to interrogate without prior instrumentation (i.e., not "you should have set that up in advance").

**Don't:**
- Don't accept vendors that say "observability has no special meaning" or "it's just another word for monitoring" — those are the ones with the lowest capabilities.
- Don't conflate "we use an observability tool" with "our systems are observable" — the latter is a property of the system, the former is just procurement.
- Don't let tool proliferation fragment your team's ability to diagnose.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Are monitoring and observability one and the same?"*

---

### The Reactive-Monitoring Trap and Why It Fails Now

**Principle:** For decades, monitoring meant "robots checking thresholds, alerting on deviation, humans react." The pattern was effective when systems were simple and binary (up/down). Modern distributed cloud systems demand *proactive* observation rooted in external outputs and open-ended interrogation — not pasted-on thresholds and arbitrary robot armies.

**Do:**
- Recognize that managing "the squishy virtual space between the physical and their code" was the best we had — but it has outlived its usefulness.
- Replace "watch thresholds" with "interrogate behavior freely" via unified data.
- Acknowledge the cultural paradigm shift away from "small robot army" alert tuning toward team-wide investigation skills.

**Don't:**
- Don't dismiss modern approaches by saying "monitoring always worked." The unspoken assumptions that worked for monoliths are no longer true for distributed systems (SaaS, K8s, microservices).
- Don't invest engineer-time in *pruning/tweaking noisy thresholds* — invest in better data so the signal is no longer noisy.

> "Focusing on predefined metrics and thresholds to ensure system health made operations reactive. Deviations from those thresholds would trigger alerts and responders could then inspect the change in behavior. That approach conditioned teams to investigate only when the system crossed specified thresholds."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Why A High Degree of Observability Matters Now"*

---

### LLM Observability — Why Standard Practices Insufficient

**Principle:** LLMs are nondeterministic, opaque, un-debuggable, and accept an *infinite* class of natural-language inputs. Early-access programs offer biased confidence; unit testing is largely infeasible. Observability is the only tractable path to making LLM features reliable.

**Do:**
- Ship LLM features *to learn*, but pair that with a tight prod-data-to-improvement feedback loop (telemetry).
- Distinguish *deterministic* evals (e.g., "no profanity") from *fuzzy* evals (quality of response).
- Treat LLM output as *untrusted input* — parse and validate it before downstream use; mitigate prompt-injection.
- Expect failures ("Failure will happen—it's a question of *when*, not *if*").
- Build for the realities: "users will do things you can't possibly predict"; "you will ship a 'bug fix' that breaks something else"; "you can't write unit tests for LLMs"; "early access programs won't really help you."

**Don't:**
- Don't rely on general-purpose public benchmarks or "helpfulness, tone, truthfulness, bias, conciseness, toxicity" out-of-the-box scores to gauge product fit.
- Don't release LLM features without observability — observability "ramp[s] up significantly when building products that use LLMs."
- Don't trust LLM output structurally — it's injection-prone by definition.

> "The very things that make LLMs so useful also give rise to the biggest challenges. End users expect powerful capabilities with reliable behavior, but steering an LLM to reliability for all possible inputs is challenging. Furthermore, the tools that product engineers traditionally lean on for improving reliability—step-by-step debugging and unit testing aren't feasible with LLMs."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Why Observability Matters for LLMs"*

---

### Bias in Early-Access Programs — Why They Don't De-Risk LLM Features

**Principle:** Early-access programs and limited user testing can introduce *selection bias* and create a *false sense of security*. They fail to capture the full range of user behavior and edge cases that arise in real-world usage. When gauging ambiguous criteria like UX, they suffer from who-tried-the-feature-and-in-what-context biases that organizations tend to report positively on.

**Do:**
- Treat early-access results as anecdotal data, not signal.
- Pair limited launches with telemetry-driven sampling; expand the user base once telemetry tells you which axes are stable.
- Ask: *what input classes didn't the early-access sample touch?* Refuse to extrapolate.
- Adopt "ship to learn" but back it with telemetry so you actually *learn* from what was shipped.

**Don't:**
- Don't tie a launch decision to early-access sentiment alone.
- Don't accept "users loved it in alpha" as evidence of reliability.
- Don't assume extensive user testing will work around nondeterminism — selection bias + experimental demand bias limit what user testing can find.

> "Effectively working around these problems requires significant time and money. Couple this with widespread organizational tendencies to always report successful results from expensive time investments, and you'll be left with a sense of security that comes crashing down when you truly go live. Instead, it's better to embrace a 'ship to learn' mentality and release features earlier, but you need a way to systematically 'learn' from what was shipped."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Why Observability Matters for LLMs"*

---

### Debugging Limitations of LLMs — Step-Through Is Meaningless

**Principle:** Unlike single-threaded client applications, LLMs *cannot* be debug-stepped. You can't load debug symbols and walk through each phase of execution. You have:
- **Temperature** and **top_p sampling** (randomness controls) — these affect output variety but don't guarantee repeatability.
- **Infinite input space** — natural-language is orders of magnitude more expressive than any programming language, query language, or UI.

**Do:**
- Treat the LLM as a black box with inputs and outputs; instrument around it, not into it.
- Lean on OTel spans + structured output validation as your "debug stepping" tools.
- Save raw prompt + completion pairs in your data store — this is your LLM-call-stack equivalent.

**Don't:**
- Don't ask on-call engineers to "explain why the LLM emitted X" — there's no good answer without telemetry.
- Don't conflate `temperature=0` with deterministic output — it isn't, due to batching, infrastructure effects, and model-side nondeterminism.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Why Observability Matters for LLMs"*

---

### Evals — The Foundation for LLM Reliability

**Principle:** An *eval* is a test whose expected output is *fuzzy* rather than strictly pass/fail. An *eval system* is the suite (data, task function, scoring function, executor, dashboard). 100% pass rate is a red flag — it means your data isn't representative.

**Eval system components:**
- **Data** — (1) *Golden data*, hand-crafted ideal pairs; (2) *Larger datasets*, generated or curated from production.
- **Task function** — the LLM call (with your prompt) that the data flows through.
- **Scoring function** — pass/fail judgment, deterministic or fuzzy.

**Do:**
- Build your eval system around these three components.
- Aim for a baseline pass rate of 50%+ (not 100%) — your goal is real, not exhaustive.
- Use golden data first (hand-crafted, ideal pairs), then synthesize larger datasets for stress.
- Use evals for experiments: switching models, prompts, RAG pipelines.
- Tightly couple evals with observability — observability data feeds golden data, evals gate changes.

**Don't:**
- Don't skip a working prototype — you need end-to-end runs before you can build golden data.
- Don't over-engineer evals before launch; "good enough for production" beats exhaustive-but-stale.
- Don't let golden data drift from real user behavior; periodically prune non-representative cases.
- Don't conflate pass-rate with business value — sometimes a 60% pass rate is plenty.

```text
For example, let's say you want to use an LLM to translate natural-language to SQL:

  You are an AI that turns natural language into SQL queries.
  The table you are querying is: <table_name>
  The columns in this table are: <column_list>
  
  Given user input, the table, and its columns, produce a valid SELECT.
  Input: Get all posts
  select * from blog_posts
  Input: Get posts from Alice
  select * from blog_posts where author = 'Alice'
  Input: <user_input>
  ...
```

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Using Evals for LLM Reliability" / "Building evals that are good enough for production"*

---

### Designing Telemetry for LLM Pipelines — Spans Hierarchy

**Principle:** A typical LLM pipeline has one *overall* span plus child spans for each subsystem interaction; collect wide-context telemetry with user input, raw LLM output, parsed/validated output, errors, and user feedback.

**Three-span floor (simple LLM call):**
```
[overall tracking span]                ← end-to-end UX, primary lookup key
   ├── [LLM call span]                 ← auto-instrumentation (e.g., OpenAI SDK)
   └── [parse/validate span]           ← your typed struct + validation
```

**RAG spans:**
```
[overall tracking span]
   ├── [embedding-generation span]     ← vector for user input
   ├── [retrieval span]                ← which docs were picked
   ├── [LLM call span]
   └── [parse/validate span]
```

**Agents / chained calls:**
```
[parent iteration span]
   ├── [iteration 1 span]  ↳ [LLM] ↳ [parse]
   ├── [iteration 2 span]  ↳ [LLM] ↳ [parse]
   └── ...
```

**Do:**
- Use the overall tracking span as the primary "find the user's trace" key.
- Treat the LLM call span as automatic-instrumentation territory (e.g., OpenAI SDK).
- Emit a child parse/validate span with the parsed/validated values, *especially* whether parsing succeeded.
- Capture user inputs, LLM output, parsed/validated value(s), errors (LLM and parsing), user feedback signals.
- Treat every LLM output as untrusted — parse to a typed structure, validate, then route downstream.
- Track both *LLM output* (raw) and *final output* (what the user sees) — they may differ after parsing/composition.
- For prompt-assembly logic: emit a span when prompt assembly is complex (e.g., parameterized by user signal).
- Capture cost: count tokens (input + output) per request; vendor token-based pricing is straightforward to compute.

**Don't:**
- Don't let unbounded agents/chains produce unbounded spans without consideration — design for variable step counts.
- Don't forget to wire application errors explicitly into the relevant span (OpenTelemetry captures auto-instrumentation errors but not your own).
- Don't conflate "raw LLM output" with "final answer" — log both.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Designing Your Telemetry"*

---

### Distinguishing Deterministic vs. Fuzzy Evals

**Principle:** Two eval flavors exist. *Deterministic evals* are tests (e.g., "no foul language"). *Fuzzy evals* evaluate whether a response is "good" given context — these are the bulk of LLM-quality work and the harder, more valuable ones.

**Do:**
- Use deterministic evals as guardrails for hard rules (no profanity, JSON parses, schema valid).
- Invest most of your eval work in fuzzy-scoring — these gate quality improvements.
- Treat 100% pass rate on a fuzzy eval as a *signal* (test data isn't hard enough), not a *success*.

**Don't:**
- Don't conflate deterministic and fuzzy evals when reasoning about pass rates.
- Don't treat fuzzy eval scores as objective ground truth; they reflect the scoring function's biases.

> "Evals come in two primary categories: Deterministic outputs — these are just tests, and can be created and run much like any other software test. … Fuzzy outputs — these examine if a given response is 'good' for a given input, where the exact characteristics of 'good' are driven by a collection of factors."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Using Evals for LLM Reliability"*

---

### Parsing & Validating LLM Output — The Defensive Discipline

**Principle:** Parsing structured LLM outputs gives a defense-in-depth: even if the model is subverted, the parsed result is constrained. Combined with programmable fix-ups (next section), you dramatically reduce exploit surface.

**Do:**
- Always parse structured LLM outputs to typed objects before passing downstream.
- Validate against schema, including presence of required fields and absence of forbidden ones.
- Apply programmatic fix-ups to recover from malformed-but-recognizable outputs.

**Don't:**
- Don't pass raw LLM text directly to UI or other services.
- Don't skimp on validation just because "the prompt says to return JSON."

> "LLM outputs should be considered *untrusted inputs to your system*. In particular, *prompt injection attacks* are a common way for malicious actors to try to exfiltrate data, manipulate outputs for other users, or reprogram a part of your application to do all kinds of bad things."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Parsed and/or Validated LLM Outputs"*

---

### Intervening on Correctable Errors — The 25% → 14% Trick

**Principle:** When an LLM produces "mostly correct" structured output that fails validation, **programmatically correct the output** instead of failing the request. This is the fastest way to lift success rate from 75% → 96% *before* tuning prompts.

**Do:**
- Group telemetry by `error × user input × LLM output × parse/validation output` to find correctable patterns.
- Implement programmatic fix-ups that go from a malformed but recognizable structure to a valid one.
- Treat each fixup as a great test case: you have the bad LLM output and the expected post-fix output.
- Reach for prompt engineering *only* when fix-ups can't cover the case.

**Don't:**
- Don't use prompt engineering as your first lever — fix-ups are higher leverage when applicable.
- Don't rely solely on free-form-text LLM outputs; you can't validate them programmatically.
- Don't ignore that fix-ups treat symptoms, not root causes — eventually you must also tune prompts and/or fine-tune.

**Honeycomb Query Assistant — before / after fix-up:**

Before:
```json
{
  "calculations": [
    {"op":"COUNT", "column":"exception.message"}
  ],
  "filters": [
    {"column":"exception.message","op":"exists"},
    {"column":"parent_name","op":"exists"}
  ],
  "breakdowns": ["exception.message","parent_name"],
  "orders": [
    {"op":"COUNT","order":"descending"}
  ]
}
```

After (corrected by removing `column` from the COUNT calculation):
```json
{
  "calculations": [
    {"op":"COUNT"}
  ],
  "filters": [
    {"column":"exception.message","op":"exists"},
    {"column":"parent_name","op":"exists"}
  ],
  "breakdowns": ["exception.message","parent_name"],
  "orders": [
    {"op":"COUNT","order":"descending"}
  ]
}
```

**Result:** error rate dropped from 25% → 14% via fix-ups; later prompt engineering brought it to <1% (excluding timeouts or other uncontrollable errors).

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Intervening on Correctable Errors"*

---

### SLOs for Latency and Error Rate (LLM-Specific)

**Principle:** The two fundamental SLIs for LLM-backed features are *latency* (full lifecycle: prompt assembly, RAG retrieval, LLM call, parse/validate) and *error rate* (network, timeout, LLM output error, parse/validation error). A 95% success rate over 7 days is a good starting latency SLO.

**Do:**
- Define latency SLO around the *entire* operation, not just the LLM call.
- Set initial thresholds from observed development-mode performance (e.g., "3s").
- Calibrate error-rate SLO to development pass rate (e.g., 75% if 3 of 4 responses succeed in tests).
- Send SLO alerts to chat (Slack/Teams), *never* PagerDuty — they're informational, not page-worthy.
- Iterate SLO thresholds so they fire periodically — never-firing SLOs are too loose.
- Track SLIs that distinguish between *controllable* (LLM output + parse) and *uncontrollable* (API rate-limited, network blips) error sources.

**Don't:**
- Don't tighten SLOs based on "this looks nice on paper" — calibrate them to real prod behavior.
- Don't page on SLO budget exhaustion — reserve paging alerts for directly-actionable events.
- Don't gate latency on a single threshold; consider p95 or p99 and window sizes.

> "An SLO for an error rate is very simple: if the overall operation contains an error, it fails. Otherwise, it succeeds. … One of the most impactful ways to improve the success rate of your feature using SLOs is to correct a 'mostly correct' output from an LLM when it's considered correctable."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Monitoring Service-Level Objectives" / "Latency SLOs" / "Error Rate SLOs"*

---

### SLO Budget Burn as a Planning Trigger

**Principle:** SLO breach is non-urgent info; it should trigger *planning* ("we need to fix this next"), not panic. Use budget burn to schedule work, not to fire pages.

**Do:**
- Route SLO alerts to chat channels with structured routing (e.g., per-team channels).
- Use budget-trend alerts (e.g., "burning 2x faster than refill rate") for early warning.
- Make sure each SLO alert has an owner and a runbook even if the runbook says "no urgent action."

**Don't:**
- Don't make SLO alerts pageable. Reserve pages for directly actionable events.
- Don't keep SLOs that never fire — they're too loose to be useful.

> "If no alert is ever triggered, then the SLI is probably too broad and should be adjusted. In the case of latency, maybe you need a lower latency threshold. Or perhaps your success rate should be increased for an error rate SLO."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "SLO Monitoring and Alerting"*

---

### Watch-Point Telemetry — Five Things to Track Per Event

**Principle:** Modeling telemetry isn't *just* final output and inputs — it spans the whole journey. Five things to track per LLM event:
1. **User inputs**
2. **LLM output** (raw, before parsing)
3. **Parsed/validated values** (after the validation step)
4. **Errors** (LLM errors and parse/validation errors, tagged)
5. **User feedback** (thumbs up/down, if relevant)

**Do:**
- For each LLM-feature event: capture all 5 dimensions in one event.
- Invest in user-feedback signals (thumbs up/down) when possible — they pump your golden data.
- Cross-link user feedback events to the LLM-feature events to enable correlation by signal class.

**Don't:**
- Don't rely solely on click-through / completion rate as feedback — those measure outcomes, not quality.
- Don't drop the LLM-output field after parsing — you need raw data to refine prompts later.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Inputs and Outputs"*

---

### The Virtuous Loop — Production Data → Evals → Production

**Principle:** Once your eval system is "good enough for production," kick off a closed loop: prod telemetry → curate/annotate → update golden + larger data → re-run evals → push experiments → monitor prod. This is how LLM features reach reliability *and* keep up with user behavior shifts.

**Do:**
- Treat prod data as ground truth about *how users actually use your feature*.
- Use a rule-of-thumb: **>10 users × >100 uses/day** is representative enough to act on prompt changes.
- Curate prod data: decide which inputs/outputs to add to golden; hand-craft ideal outputs for ambiguous cases; remove outdated golden rows; tune the "LLM-as-Judge" against real examples.
- Run the boring work: experiment with prompts/RAG/models, score against evals, push to prod, mine prod.
- Use "grounding in facts" as the one out-of-the-box-ish metric worth investing in for RAG.

**Don't:**
- Don't treat public LLM benchmarks or generic metrics dashboards as proxies for *your* product's correctness.
- Don't optimize for "grounding in facts" in isolation — it's necessary but not sufficient for product helpfulness.
- Don't let your golden data go stale; review it against prod regularly.

> "What remains now is the boring, arduous work of: Experimenting with different prompts, retrieval steps for RAG, new models, etc. Evaluating the effectiveness of these changes in your eval system. Promoting these experiments to production to see how they behave with real usage. Using production data to better inform and understand how to run more experiments in the future."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Feeding Observability Data Back into Development" / "Using Evals and Observability Together"*

---

### LLM Cost Tracking — Inexpensive, Easy, Lower Priority

**Principle:** For external LLMs, cost = token count × rate per token (input vs output). It's easy to compute from telemetry — and today, *not critical* (LLM costs are low, vendor rate limits already constrain spend). Don't let cost tracking distract from quality.

**Do:**
- Count input and output tokens per request; compute cost; graph it.
- Rely on vendor rate limits as a safety bound on spend (along with your own).
- Treat cost as a secondary SLO when budget-tight; prioritize latency / error SLOs first.

**Don't:**
- Don't over-engineer cost dashboards while LLM quality/reliability remains the binding constraint.
- Don't ignore rate limits — they're the cheapest, most reliable cost gate.

> "Most LLMs are quite inexpensive to use today, and they'll likely just get cheaper over time as they become more efficient and face external pressures from competition. Additionally, to protect their infrastructure, vendors apply rate limiting, and these rate limits place boundaries on usage that are extremely economical."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Cost Tracking" / "LLM Cost, Rate Limits, and Vendor Boundaries"*

---

### Prompt Engineering — A Subtle, Experimental Discipline

**Principle:** Prompt engineering is *"a rigorous approach to experimentation and interaction."* Small word changes produce dramatic behavior changes; treat prompts as code with version control, testing, and observability around them.

**Do:**
- Treat prompts as evolving artifacts with explicit version control and rollbacks.
- Pair every prompt change with an eval run.
- Pair every prompt deploy with telemetry to detect regressions in production.

**Don't:**
- Don't treat prompt tweaking as casual — it's the lever that determines LLM behavior.
- Don't ship prompt changes without explicit evaluation harnesses (an "evals" check before merge and a "telemetry" check post-deploy).

> "Even slight modifications to the prompts can yield dramatic differences in the outputs produced by the model. The choice of wording, phrasing, or context within the prompt can significantly impact the generated responses. Prompt engineering requires a rigorous approach to experimentation and interaction."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Sidebar: Quick Primer on Prompt Engineering"*

---

### AI Observability Is a Team Sport

**Principle:** LLM products add new stakeholders (AI engineers, ML engineers, data scientists) but the disciplines are still observability, applied to a different problem. Existing teams must expand scope: SWEs take on data quality and probabilistic systems; ML engineers focus on user behavior; PMs learn Python/Jupyter to participate in prompt-engineering experiments.

**Do:**
- Involve all relevant roles from day one: instrumenting, analyzing, monitoring, dealing with user feedback, classifying data, building eval/feedback pipelines, owning prompt-engineering tooling.
- Provide *small enough* systems where a few people can do it all; large surface area requires role diversification.
- Invest in prompt-lifecycle management, eval infrastructure, and production-data pipelines.

**Don't:**
- Don't try to buy your way out — "there is no 'easy button' to press."
- Don't assume a single tool or practice solves all LLM reliability problems.
- Don't hire only specialists — people must *adapt* responsibilities not traditionally tied to their role.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Observability Is a Team Sport"*

---

### Public LLM Benchmarks vs Your Own — Don't Confuse Them

**Principle:** Public benchmarks gauge *general* model capability. They're nearly useless for *your* product. Out-of-the-box metrics dashboards ("helpfulness, tone, truthfulness, bias, conciseness, toxicity") can report high scores while your product is unhelpful.

**Do:**
- Treat public benchmarks as smoke tests for the model itself, not as product metrics.
- Invest in your own evals + a custom "grounding in facts" metric for RAG.
- Combine well-known measurement techniques to gauge grounding — combine statistical + retrieval-relevance + LLM-judge as appropriate.

**Don't:**
- Don't ship LLM features based on vendor benchmark numbers.
- Don't equate "high helpfulness score" with "useful product."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Public benchmarks and generic metrics aren't very helpful"*

---

### Future Tooling for AI Observability

**Principle:** Expect innovation in: auto-instrumentation for LLMs; prompt-lifecycle management; production-to-dev data pipelines; specialized observability products; fine-tuning tools; turnkey eval frameworks. None will solve LLM reliability alone.

**Do:**
- Track the OTel LLM-instrumentation effort (semi-built-in spans, semconv for LLMs).
- Subscribe to feedback from production data to keep eval golden sets fresh.
- Build vendor-neutral open instrumentation patterns (OTel) so you're not locked.

**Don't:**
- Don't bet on a single tool or vendor for LLM reliability — the field is too immature.
- Don't skip your own observability just because "the new tool claims to handle it."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Conclusion"*

---

### Compute Cost Is Multi-Dimensional, Not Just Time

**Principle:** Cost optimization isn't "make it faster." Memory bandwidth, network, and instance family materially change $/request. Observability must surface cost dimensions alongside request metrics.

**Do:**
- Ingest cloud-bill data into your observability tool to spot the largest spend buckets and drill into common attributes.
- Treat "is this faster because of more/faster memory or network?" as a routine engineering question.
- Use serverless as a built-in optimization: shorter Lambda execution = lower bill; convert span duration into additive cost.

**Don't:**
- Don't settle for "time" as the only cost dimension.
- Don't trust dashboards that aggregate cost without attribution to specific services/tenants/regions.

> "It's important to consider that there are multiple dimensions to the cost profile of your compute layer. It's not simply 'time', since the different machines and instance sizes also have an impact on price which is where we can use performance engineering to optimise beyond just 'make it faster'."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Observing the cost profile"*

---

### Async vs. Sync Workloads — Spiky Workloads Favor FaaS

**Principle:** FaaS shines for spiky traffic where you tolerate cold-start/refusal costs (and may even monetize them via latency-cost). Steady workloads cost more per second on FaaS than on reserved capacity.

**Do:**
- Use FaaS for spiky, latency-tolerant, revenue-correlated workloads.
- Use reserved for steady baseline.
- Use elastic-persistent (Fargate/Cloud Run) for variable background workers.

**Don't:**
- Don't put a database on FaaS.
- Don't pay FaaS unit costs for steady workloads if reserved will cost less.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Infrastructure purchasing models"*

---

### Sampling Profile Tradeoffs — Statistical Reliability vs Overhead

**Principle:** Sampling every ~10 ms captures most of the picture without skewing results via overhead. Profilers interrupt the program with OS signals, capture the program counter + stack, and statistically aggregate — same principle as distributed-trace sampling.

**Do:**
- Sample less frequently in noisy environments (~10 ms is a sensible default).
- Increase sampling for short incident windows when you want fuller coverage.
- Use statistical aggregation: one sample tells you little; millions tell the truth.

**Don't:**
- Don't over-sample (1 ms = lots of overhead, can distort behavior).
- Don't under-sample (the cliff between 10 ms and 100 ms is steep).

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Introducing CPU profiling tools"*

---

### LLM Error Tracking — Distinguish Controllable vs. Uncontrollable

**Principle:** Error-rate SLIs should *include any error* — network, timeout, LLM-side, parse-side. Distinguishing controllable vs uncontrollable helps prioritize engineering work.

**Do:**
- Bucket errors as: API rate-limiting (third-party), timeouts (network), parse/validation errors (your code), LLM-side errors (model output).
- Track controllable errors with SLOs; track uncontrollable errors separately for capacity planning.

**Don't:**
- Don't lump all errors into one SLO without separating controllable and uncontrollable sources — it makes prioritization impossible.

> "The great thing about an error rate SLO is that it's one of the measures that you have the most control over. As I elaborate later, one of the most impactful ways to improve the success rate of your feature using SLOs is to correct a 'mostly correct' output from an LLM when it's considered correctable."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Error Rate SLOs"*

---

### Performance Engineering Across the Org — Cultural Levers

**Principle:** As of late 2024, Honeycomb's continuous-profiling usage spread from one engineer to half a dozen teams. Cost engineering is now collaboration between finance and engineering, using AWS bill + telemetry to predict future spend.

**Do:**
- Cross-pollinate performance / cost / observability ownership.
- Let telemetry guide where the org invests (e.g., one team's finding may apply fleet-wide).
- Build a finance+engineering cost model with telemetry ingestion.

**Don't:**
- Don't silo performance or cost in a single team — they intersect with observability, which is everyone's job.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Performance Engineering Conclusion*

---

### Latency SLOs Calibrate From Development Mode

**Principle:** Start SLOs from observed dev-mode performance. The 95% / 7-days rule is a sensible starting *default*, but the *specific* latency threshold should match the median-plus-tail you observe in development. Calibrate from there.

**Do:**
- Measure dev-mode performance for the full lifecycle (prompt assembly, RAG retrieval, LLM call, parse/validate).
- Set your initial latency SLO at the 95th percentile of that measured distribution.
- Adjust up when you can consistently exceed it (raises the bar).
- Adjust down only when targets are unrealistic — don't lie about feasibility.

**Don't:**
- Don't pick SLO thresholds based on "what's a good number" without measurement.
- Don't fail to act on never-firing SLOs (they're effectively absent — either tighten or remove).

> "In particular, it's critical to track latency for the entire lifecycle of user interactivity with a feature using LLMs. This includes the entirety of the process: the time it takes to gather input, build up or gather the prompt to an LLM, make additional API calls (such as that to fetch a vector embedding), make the call to an LLM, and parse/validate results."

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Latency SLOs" / "Sizing SLO Thresholds to Reality"*

---

### Application Error Capture — OpenTelemetry Is Half the Story

**Principle:** OpenTelemetry captures errors from *automatic* instrumentation (HTTP failures, gRPC failures, database errors) but **does NOT capture errors from your own application code**. To track logic-level failures, you must explicitly wire them into the relevant span.

**Do:**
- Use the SDK's API to attach `setStatus({ code: SpanStatusCode.ERROR })` + `recordException(...)` for every custom failure path.
- Add a synthetic attribute (e.g., `error.kind = "validation_failed"`) so dashboards can group by application error type.
- Treat application errors as first-class telemetry events — they're often more important than infrastructure errors for product reliability.

**Don't:**
- Don't assume auto-instrumentation covers your business-rule failures.
- Don't let untyped exceptions leak past spans; always associate them with the trace of the request that triggered them.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Application Errors"*

---

### Dynamic Prompts Are Span-Worthy

**Principle:** If your prompt-assembly logic is non-trivial (parameterized by user signal, assembled at runtime from multiple sources), that assembly process is itself an instrumentable unit of work. A user signal that affects prompt structure can change LLM behavior — but without a span, you'll never see *why*.

**Do:**
- Emit a span when prompt assembly involves more than string concatenation.
- Capture how the prompt was built (which signals, which templates, which tools).
- Treat prompt engineering as a first-class telemetry concern.

**Don't:**
- Don't conflate "the prompt is a string" with "the prompt has no telemetry story." The *construction* of the prompt is observable, debuggable code.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Dynamic Prompts"*

---

### Tracing as Investigation Loop — The Three Questions

**Principle:** Tracing provides the bird's-eye view; combined with high-cardinality data analysis, it lets you explore individual fields and outliers. Ask these questions to drive an investigation:

1. **Is this endpoint *normally* slow** (aggregate baseline)?
2. **Is this database query slow only when called for this specific API endpoint**?
3. **When this endpoint is slow, is it *always* this database call causing it**?

Use these three axes to bound the search before pulling out the profiler.

**Do:**
- Start broad (aggregate), narrow to feature (per-endpoint), narrow to function (per-span), narrow to inner execution (per-profiler-sample).
- Use tracing to *validate hypotheses quickly* — the trace tree either confirms or rules out your theory in seconds.

**Don't:**
- Don't drop into profiling before asking the aggregate questions — most latency mysteries have outlier answers visible in trace data.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Using the correct observability signals"*

---

### Datastores for Telemetry — Wide Events Beat Pre-Aggregation

**Principle:** A *wide event* is one record carrying every field relevant to an event (user, request, env, trace context, business attrs, response). Pre-aggregated metrics compress this away; wide events preserve the freedom to ask arbitrary questions later.

**Do:**
- Emit wide events from your application code (single record per request).
- Ingest wide events into a queryable storage that supports `GROUP BY` over arbitrary fields.
- Use the storage's query layer to derive dashboards *on read* (Honeycomb BubbleUp, Datadog Notebooks, etc.) instead of pre-computing.

**Don't:**
- Don't pre-aggregate for performance — modern columnar stores handle wide-event queries efficiently.
- Don't fragment your query layer across vendors (each pillar gets its own query UI) — that recreates correlation tax.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Technological Step Changes in Observability"*

---

### Detecting Latent Faults — "Inexplicable Slowness" Diagnosis

**Principle:** When p99.99 looks fine but specific users complain, the question is "where is the *time going*?" Heatmaps and per-user trace slicing surface failures that aggregates smooth over.

**Do:**
- Slice trace data by individual user IDs to find slow users.
- Use heatmaps on latency — long tails compress into the visualization.
- Compare arbitrary groups of users (by attribute) to find shared characteristics in slow cohorts.
- Use latency distributions, not single-number summaries.

**Don't:**
- Don't accept "the average is fine" as evidence the system is fine.
- Don't analyze latency only at the request-mean level — the tail is where the user pain lives.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Chapter 1 "How Observable Is Your Software?" / Question 8 ("Can you find hidden timeouts even when p99.99 looks fine?")*

---

### Heatmap vs Percentile Decision Tree

**Principle:** Heatmaps win for saturation & variability (K8s, A/B experiments, instance fleets); percentiles win for *single*-fleet, *aggregate* SLI dashboards. The choice is "what am I trying to see?"

**Heatmap when:**
- Saturation varies wildly across instances (K8s pod CPU).
- You suspect skew (one instance clipping at 100% while others idle).
- You have to answer "what's the worst-case pod?" not "what's the 99th-percentile user?"

**Percentile when:**
- You're reporting a single SLI to stakeholders.
- The variable under measurement has a unimodal distribution (user latency).
- You want a number you can put in a status email.

**Do:**
- Default to heatmaps during investigations; switch to percentiles for SLI reporting.
- Pair both: percentile for the SLI, heatmap for the operational truth.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Cost-optimizing Kubernetes"*

---

### Production Data Curation — A Discipline of Its Own

**Principle:** Production data is the *source* of your eval system's refresh cycle. Curating it has its own pitfalls — staleness, bias, privacy. Treat it like any other CI artifact with rules.

**Do:**
- Periodically prune outdated golden cases (the prompt has changed; the case no longer represents the right answer).
- Hand-craft ideal outputs for ambiguous cases (don't trust the LLM-only answer).
- Consider a "tuning the LLM-as-Judge" step before using real examples; synthetic and real data are not interchangeable.
- Decide which *user input* classes go into the golden (representative inputs), not just which produce good outputs.

**Don't:**
- Don't just dump production data into evals unfiltered.
- Don't keep golden rows that test deprecated behavior.
- Don't treat the LLM-as-Judge as infallible — its biases become your evals' biases.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Feeding Observability Data Back into Your Evals"*

---

### Multi-Dimensional Error Analysis — "Group By Four"

**Principle:** When looking at error events, group by *error × input × LLM output × parse/validation output*. A single dimension ("most common error") is shallow; the *intersection* surfaces fixable patterns.

**Do:**
- Ask: which error has the most cases? Which inputs correlate? Which LLM outputs correspond to which errors?
- Look for patterns where the same input → same LLM output → specific error (fixable).
- Look for patterns where similar inputs → different outputs → different errors (data drift; need golden-data refresh).

**Don't:**
- Don't stop at "top-N most common errors." That's the surface; the *correlations* are the value.
- Don't analyze one dimension at a time when your observability tool supports multidimensional grouping.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Analyzing Telemetry for AI Applications"*

---

### Latent-Fault Visibility Loop — Per-Investigation Minute Cost

**Principle:** Each minute of "investigation time" spent sifting through separate logs/metrics/traces is a minute not available to root-cause engineering. Telemetry *correlations that fail* are the silent productivity tax of observability 1.0.

**Do:**
- Eliminate the "go back to the alert tool to check whether this log error is in the same time window" loop.
- Force every interesting piece of telemetry to share a single query layer.
- Measure "time to first finding" as a leading metric for observability tooling.

**Don't:**
- Don't accept "ML/GenAI tag enrichment" as a substitute for unification — it's correlation-on-read, which is brittle and slow.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Technological Step Changes in Observability"*

---

### Performance as an Org-Wide Cultural Practice

**Principle:** Performance engineering is most effective when practiced by many teams, not one. The skill spreads through shared tooling, shared dashboards, and visible wins.

**Do:**
- Create shared profiling infrastructure any team can use.
- Publish per-team perf wins in eng-wide channels.
- Embed performance engineers as consultants, not gatekeepers.

**Don't:**
- Don't centralize performance under a single team — it becomes a bottleneck.
- Don't keep profiling skills siloed — train multiple people per service.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Building a Performance Engineering Practice" / Conclusion*

---

### Step-Through Debugging Is Impossible on LLMs — Design Around It

**Principle:** You can't step-debug an LLM call. There's no symbol table, no source line, no call stack. When an LLM emits output X, the chain of computation that produced it is hidden.

**Implications:**
- You must instrument *around* the LLM call (input, output, span context).
- You must capture the *full* prompt + completion pairs in storage.
- You must enable *post-hoc* analysis via wide-event querying.
- You cannot rely on "reproduce locally" the way you can with deterministic code.

**Do:**
- Treat every LLM call as a black box with rich telemetry around it.
- Replay captured (prompt, completion) pairs against new models/prompts offline to test changes safely.
- Use OTel + structured output parsing as your "call stack for LLMs."

**Don't:**
- Don't promise on-call engineers "you can reproduce this locally" for LLM bugs — you can't reliably.
- Don't trust post-mortem verbal accounts without telemetry backing them up.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Why Observability Matters for LLMs"*

---

### Performance Engineering as Continuous Reinforcement

**Principle:** Not every change is a 30% saving. The practice is *continuous*; small wins compound. Squeeze one bug, find the next one. The optimization frontier is rarely the ceiling — there's almost always another 5-15% available.

**Do:**
- Treat the practice as a habit, not a project.
- Re-baseline after each big change; new floors imply new ceilings.
- Document wins (and the data behind them) so others can imitate the technique.

**Don't:**
- Don't expect diminishing returns to be a sign of completion.
- Don't let profiling data accumulate without reviewing it.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Performance Engineering Conclusion*

---

### Dependency on PProf Endpoints — Operational Hygiene

**Principle:** An exposed `pprof` endpoint is a powerful diagnostic tool but also a small attack surface. Treat it like a private admin endpoint.

**Do:**
- Listen on a different port than your application (e.g., `:6060` not `:8080`).
- Restrict access via network policy to on-call engineers and dev infra (not public-internet reachable).
- Disable `/debug/pprof` in customer-facing environments if not needed.
- Set timeouts on profile captures (e.g., 30s) to avoid runaway collection.

**Don't:**
- Don't expose `pprof` to the public internet.
- Don't leave `pprof` enabled in production by default if you don't need it — it's a memory cost (heap profile = full heap walk).

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Setting up and interpreting profiling data"*

---

### Vendor Rate Limits as a Cost-Bound Mechanism

**Principle:** For LLM vendors (OpenAI, Anthropic, etc.), vendor rate limits are the cheapest cost gate. They bound spend by design; pair them with your own application rate limiting and you have predictable monthly bills.

**Do:**
- Treat vendor rate limits as a hard ceiling.
- Add your own rate limiting on top of vendor limits for end-user fairness.
- Surface rate-limit hits in your telemetry (otherwise they're invisible).

**Don't:**
- Don't rely on cheap-vendor pricing alone to bound spend.
- Don't assume vendor rate limits are stable — they can change without notice.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "LLM Cost, Rate Limits, and Vendor Boundaries"*

---

### Cost-Aware Vendor Comparison

**Principle:** Cheapest per-token vendor isn't always the cheapest *operationally*. Compare on:
- Per-token rates (input vs output).
- Rate-limit headroom.
- Latency tail at your prompt size.
- Reliability (uptime, incident history).
- Feature support (structured output, tool use, fine-tuning).

**Do:**
- Re-evaluate vendors quarterly; rates change.
- Track time-to-recovery on each vendor's status page.
- Treat the "cost" axis as a vector, not a scalar.

**Don't:**
- Don't change vendors reactively during an incident.
- Don't swap vendors without updating evals + golden data.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Cost Tracking" / "Why Observability Matters for LLMs"*

---

### Onboarding Your Telemetry Investment to Leadership

**Principle:** "Why invest in observability when we have a monitoring tool?" is the question you'll face. The answer isn't dashboard counts — it's the failure modes the *current* tool can't see.

**Do:**
- Prepare a quick demo: a recent incident, the data the current tool had, and the unanswered questions.
- Show leadership the four-conditions litmus test ("could the team answer this without shipping code?").
- Talk in terms of unaddressed failure modes, not observability "buzz."
- Quantify the cost of slow debugging (engineer hours × incidents × hourly cost).

**Don't:**
- Don't lead with vendor comparisons — they trigger skepticism.
- Don't promise observability will prevent incidents — it surfaces them earlier, which is different but related.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Chapter 1 "Why A High Degree of Observability Matters Now"*

---

### Continuous Profiling & Cardinality — Per-User Profiling Power

**Principle:** Continuous profilers can index profiles per-user (high cardinality), surfacing user-specific hot spots invisible at aggregate service-level. A single customer's query shape pinning a CPU core is invisible at the *service* median.

**Do:**
- When onboarding a continuous profiler, ask how it indexes profiles (process-wide? per-user? per-tenant?).
- Use per-tenant profiles to attribute shared cost to specific customers.
- Couple profiling with traces so per-customer CPU hotspots correlate to per-customer slow traces.

**Don't:**
- Don't settle for process-wide profiling only — it's a missed opportunity.
- Don't expose per-user profiles to anyone who can see all users' traces — privacy implications.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — "Blending performance engineering and observability"*

---

### Wrap-Up — The Unified Discipline

Observability, performance, cost, and LLM-reliability engineering are not separate disciplines. They share data, tooling, and culture. The Honeycomb narrative is *fuse them* — let one platform serve all four audiences (SWE, SRE, finance, ML eng) and let each audience ask the questions only their domain cares about.

*Ref: Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md — Performance Engineering Conclusion / AI Observability Conclusion*

---

## Anti-Patterns & Common Mistakes

- **"More dashboards = more observability":** Adding panels without unifying the underlying datastore adds cognitive overhead. *Fix:* unify into one wide-event store; write ad-hoc queries instead of dashboards.
- **"Availability nines = trustworthiness":** 99.99% uptime + 1-second tail-latency death = unhappy users. *Fix:* measure *user experience* via percentiles and SLOs based on user-impacting errors and latencies.
- **"All my pillars are covered":** Three different vendors for logs/metrics/traces with no shared query layer is observability 1.0 in practice. *Fix:* consolidate behind one wide-event datastore + cross-pillar visualization.
- **"I'll add a fourth observability vendor (razor)":** Don't open the door to an arms race. *Fix:* demand paradigm-shift outcomes (unification) rather than incremental telemetry scope.
- **"Mr. Scott diagnosed the Enterprise by feel":** Tribal-knowledge debugging is not a substitute for external instruments. *Fix:* ensure any engineer can answer any open-ended question in seconds with data alone.
- **Per-request mutex/router recompilation:** Routers that build regex per request quietly pin a chunk of CPU. *Fix:* singleton routers, profile in prod with continuous profiling agents.
- **"We'll rely on public LLM benchmarks":** General benchmarks ignore your domain. *Fix:* invest in your own evals + grounding-in-facts metric.
- **"LLM outputs are trusted":** Prompt injection is a real, exploitable attack surface. *Fix:* parse to typed structure; validate before downstream/UI exposure.
- **"100% pass rate = great evals":** 100% pass means your test data isn't representative. *Fix:* expand to larger datasets; aim for realistic mid-range pass rates.
- **"I'll A/B test in prod without telemetry":** You have no observability into the LLM call's contribution vs user expectation. *Fix:* instrument every phase; correlate telemetry with user feedback and error patterns.
- **"FaaS profiling = on-call debugging":** The bug will be gone by 2am. *Fix:* adopt continuous profiling agents (Pyroscope/Polar Signals/OTel profiling).
- **"I'll always alert on SLO breach":** SLO alerts should be informational, never paging. *Fix:* route to chat channels; iterate thresholds so they actually fire.
- **"Trust that new framework auto-instruments everything":** OTel auto-instruments only what it sees; your own application errors aren't captured unless you wire them into spans. *Fix:* add explicit `span.setStatus({ code: SpanStatusCode.ERROR })` for app-level failures.
- **Premature optimization without a profiler:** Optimizing based on hunches is educated guesswork. *Fix:* profile first, then optimize the wide-at-the-bottom bars.
- **Bin-packing pods to half-machines:** "20 vCPU on 32-core host = 11 cores wasted." *Fix:* size hosts and pods for the predominant workload shape (3× 20 vCPU on 64-core).
- **"I tightened my SLO to look stringent":** Tightening without measurement just guarantees budget burnouts. *Fix:* start at dev-mode performance; iterate based on real prod behavior.

---

## Decision Heuristics / Checklists

**Adopting observability?**
- **First, decide whether you're staying in the three-pillar camp or moving to a unified datastore** — *the rest of your choices follow from that one decision.*

**Adding vendor feature X?**
- Ask: does X support interrogation without pre-aggregation?

**SLI choice for an LLM feature?**
- Latency (full lifecycle: prompt assembly + RAG retrieval + LLM call + parse/validate) + error rate (anything that yields an error to the user). Calibrate to dev-mode pass rate.

**SLO alert?**
- Slack/Teams, not PagerDuty. Thresholds should fire occasionally — never-firing = too loose.

**Cost optimization for K8s?**
- Plot sum of CPU + memory by pod/daemonset; look for clip-on-100%-saturation in heatmaps; pack for the worst-shape jobs.

**Architecture for cost?**
- FaaS for spiky workloads paying for actual compute; reserved for steady baseline; interruptible for stateless, fault-tolerant, migratable workloads (with Node Termination Handler).

**Profiling in incident?**
- `pprof` endpoint on a non-internet port; 10 ms sampling is enough; share the binary + sources for symbolization; always render as a flame graph.

**LLM error 25%?**
- Try *fixups* on the malformed-but-recognizable structure before prompting; track the four dimensions (`error × input × LLM output × parsed output`) to find fixable patterns.

**Adding an LLM to a feature?**
- Pre-define SLOs, parse/validate outputs, ship to learn (with telemetry), commit to a closed loop with evals.

**Sufficient rep data to act on prompt changes?**
- **>10 users and >100 uses/day** as a rule of thumb.

**Continuous profiling choice?**
- Pick based on language support + observability backend integration — OTel profiling signal is the vendor-neutral future.

**Sizing a pod?**
- 20 vCPU pod + 32-core host = 11 cores wasted. Either upsize the host or split into 15 vCPU pods.

**Which eval layer covers which concern?**
- Deterministic evals → guardrails (no profanity, schema valid, parses).
- Fuzzy evals → quality (does the response actually serve the user).
- Telemetry → unknown unknowns in production.
- Together → virtuous loop.

---

## Key Takeaways

1. **Observability is a property, not a product.** Laprie's 1995 framework is the right starting point; Kálmán's framing is the right mental model.
2. **Unify telemetry into one wide-event datastore.** Don't keep paying correlation tax across log/metric/trace siloed vendors.
3. **Qualitatively self-assess.** Use the chapter's open-ended question checklist; iterate on the gaps.
4. **Profile continuously, not on-call.** Bugs don't wait for you; agents like Pyroscope / Polar Signals / OTel profiling do.
5. **Cost optimization is observability.** Plot pod consumption, heatmap node saturation, measure before you optimize. "1% off 10%" beats "5% off 1%."
6. **LLMs demand evals + observability, not either alone.** Evals gate changes; observability tells you what to change.
7. **Ship to learn — but with telemetry.** Don't ship and pray; don't ship-and-A/B-test without insight.
8. **Treat LLM outputs as untrusted.** Parse to typed structure, validate before downstream/UI exposure.
9. **Try fix-ups before prompt engineering** for structured outputs — they deliver the 25% → 14% wins quickly.
10. **SLOs are connective tissue** between reliability and business; alerts go to chat, not pages.
11. **AI observability is a team sport.** Roles blur; everyone adapts. There's no easy button.
12. **Build a virtuous loop:** prod data → golden + larger eval datasets → evals → re-deploy → mine prod.
13. **Three telemetry spans for static LLM, four+ for RAG, parent + child iterations for agents.**
14. **CPU profiling complements tracing** — profiles find hot *inner* functions; tracing finds slow *outer* boundaries. Combined (per-second indexed, per-span profile), they show *what was slow, for whom, and why*.
15. **Bin-packing is arithmetic, not vibes.** 32-core host + 20 vCPU pod + daemonset → 11 wasted cores.
16. **Arm migration beats SMT tuning** when you re-pack + test to breakage.
17. **Don't page on SLO burn.** Iterated SLO thresholds must actually fire occasionally.

---

## Cross-References

- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] — SRE practice, error budgets, incident response (overlap with the SLO-burn-as-planning-triggers principle).
- Related: [[../Building_Event-driven_Microservices.md]] — distributed systems + tracing in async pipelines (event-driven systems demand distributed observability).
- Related: [[../Building_Microservices.md]] — service boundaries make seams easier; "unknown unknowns" emerges with microservice decomposition.
- Related: [[../Modern_Software_Engineering.md]] — feedback-driven engineering; production telemetry as truth.
- Related: [[../Building_Evolutionary_Architectures.md]] — adaptive designs; observability is the change-data for evolutionary architectures.
- Related: [[../Microservices_Up_And_Running.md]] — production observability across service boundaries; partial-failure patterns.
- Related: [[../The_Art_of_Unit_Testing.md]] — test pillars (trustworthy/maintainable/readable) vs observability pillars (Latency/Error/Trace semantics).
- Topic index: [[../INDEX.md]]

> **Reminder:** Only Chapters 1, 19 ("Performance Engineering"), and 22 ("AI Observability") are available in this Early Release. When the full text is published, expand sections covering telemetry pipeline (Ch 7-8, 17-18), OTel instrumentation (Ch 6), SLO/SLI practice (Ch 11-12), supply chain (Ch 13), ROI/BvB (Ch 15), frontend observability (Ch 23), line-of-code observability (Ch 24), and maturity model (Ch 25).
