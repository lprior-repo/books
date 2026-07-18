# Observability Engineering (2nd Ed, Early Release)
**Authors:** Charity Majors, Liz Fong-Jones, George Miranda (Honeycomb / O'Reilly)
**Topic tags:** `#architecture` `#general` `#testing`
**Language focus:** language-agnostic (Go and LLM examples)
**Sources:** `markdown_output/Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md` · `summaries/Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md`

> NOTE: This file is derived from the Early Release (Ch 1 "What Is Observability?", Ch 2 "Performance Engineering with Observability", Ch 22 "AI Observability"). The other chapters are listed in the TOC but were not yet available at the time of capture. Where a chapter is referenced, the best-practice is stated as the books-outline principle; expect a 2nd pass once full content lands.

## TL;DR
Observability is **a property of software dependability**, not a tool category — the ability to understand or debug *any given* system state, including novel ones never before seen. The historical "three pillars" (logs/metrics/traces in separate stores) are giving way to **unified telemetry** in a single store, which is the only real paradigm shift the industry has made on this dimension. Observability is most powerful when it is **high-cardinality**, **wide-event-shaped**, **production-first** — embracing OpenTelemetry, embracing performance engineering (profiling + traces), and now required for LLM-driven systems where TDD and unit tests fundamentally cannot apply.

---

## Best Practices by Topic

### Definitions and Mindset

**Principle:** Observability is a property of dependability. It is not "monitoring spelled differently" and it is not "the three pillars."

> Observability: the ability to understand or debug any given system state.

Adopted from Rudolf E. Kálmán's 1960 control-theory concept but layered with software-specific concerns. Extends Laprie's 1994 framework of dependability (availability, reliability, safety, security, integrity, maintainability) to add **observability**, with techniques spanning fault prevention, fault tolerance, fault removal, and fault forecasting.

**The Litmus Test for a System's Observability (the authors' canonical list):**
- Can you understand any system state, including ones you have never seen before?
- Can you answer open-ended questions about inner workings without hitting investigative dead ends?
- Can you understand what a specific user is experiencing at any given moment?
- Can you see any cross-section — aggregate view down to single request — and *anywhere in between*?
- Can you compare arbitrary groups of requests by attributes?
- Can you find the Nth-most load-generating user (not just the top)?
- Can you isolate a single user's requests to understand why that user is slow?
- Can you find hidden timeouts that percentile metrics miss?
- Can you answer all of these *without having predicted them in advance* (no pre-set dashboards)?
- Can you get answers in seconds (preserving your train of thought)?

**Do:**
- Treat observability as a *property of the software* — built into the system at design time, not bolted on as a vendor purchase.
- Pre-collect the *wide events* (high cardinality) needed to answer unforeseen questions; you cannot retrofit high-cardinality answers if events were collapsed at emission.
- Aim to answer questions the on-call has never thought of before.

**Don't:**
- Don't accept "is the page up?" as observability. Binary up/down monitoring is a 1990s primitive.
- Don't substitute "monitoring worked fine until something inexplicable happened" for actual observability.
- Don't rely solely on intuition ("I could tell you the speed by the feel of the deck plates") — intuition is not observability.

*Ref: Chapter 1 "What Is Observability?"*

---

### Unified Telemetry — the Only Paradigm Shift in the Space

**Principle:** The historical separation of logs, metrics, and traces into different data stores was a workaround, not a virtue. A paradigm shift (the only one the authors identify in this edition of the book) is moving to **unified telemetry**: all debugging-relevant data captured as the same data type in a single store.

**Why this matters:**
- Correlation across separate pillars is error-prone and inefficient — engineers must hold context in their heads while jumping between tools.
- High-cardinality investigation is impossible when each card has been pre-aggregated.
- The unification is the prerequisite for the litmus-test questions above ("find the Nth-most load-generating user", "find the 142nd slowest user", "isolate that one user") — separate stores cannot answer them.

**Do:**
- Adopt wide events: structured records that capture rich, contextual attributes per occurrence.
- Push as much *context* into each event as you can — make the event the source of truth, not the dashboard.
- Use tools that index and let you query arbitrary groupings (Honeycomb, Lightstep, Datadog's newer log query model, etc.) — anything that flattens or pre-aggregates barriers will return.

**Don't:**
- Don't normalize away identifying attributes before you need them — that loses dimensions you cannot recover.
- Don't confuse "lots of metrics" with observability. Counters + gauges + percentiles on five dimensions is not high cardinality.
- Don't let the marketing conflation of "observability == monitoring" reach your engineering culture. Tooling is means, outcome is end.

*Ref: Chapter 1 — "Are monitoring and observability one and the same?"; "Why A High Degree of Observability Matters Now"; the books-versioning aside*

---

### Performance Engineering + Observability

**Principle:** Performance engineering is observability applied to latency and cost. The core loop is **measure → improve → measure → improve**, with the same empirical discipline as any other engineering practice.

**Case study — December 2021 (Honeycomb):** `regexp.Compile` path was consuming 17% of CPU because the HTTP router was being discarded and recreated per request rather than reused. The fix was five lines of code. The bug was *invisible* to distributed tracing because tracing hooks fire after the router is instantiated.

**Do:**
- Adopt **continuous profiling** (Grafana Pyroscope, Polar Signals, Blackfire) so you can interrogate profiles retroactively rather than "catching them in the act."
- Index profiles at the **trace span level** — combine profiles (what was slow) with traces (for whom, in which call path). The combination reveals "what was slow, for whom, and why" — none of those alone tell you all three.
- Use **flame graphs** for profile visualization (width = total time including children; stacks = call hierarchy).
- Treat **cost optimization** as a performance-engineering outcome, not a finance-only exercise. Inferring decisions between cloud purchasing models (CapEx / reserved / on-demand / spot / persistent elastic / serverless functions) should be data-driven, not opinion.

**Don't:**
- Don't assume tracing hooks cover everything — they fire at well-defined tracepoints; CPU-intensive code outside those points is invisible without a profile.
- Don't use percentiles alone for saturation analysis. Use **heatmaps** (the authors explicitly recommend this) when the underlying distribution has high variance.
- Don't put a separate "perf team" between the system and the engineer. Spread the knowledge.

*Ref: Chapter 2 "Performance Engineering with Observability" — the regexp.Compile story, flame graphs, profile indexing*

---

### AI / LLM Observability (New in 2nd Ed)

**Principle:** LLMs force observability because traditional debugging is impossible. LLM systems are open-ended (natural language inputs), opaque, and nondeterministic. Failure is a question of *when*, not *if*.

> Failure will happen — it is a question of *when*, not *if.*
> Users will do things you can't possibly predict.
> You will ship a "bug fix" that breaks something else.
> You can't write unit tests for LLMs (or practice test-driven development).
> Early access programs won't really help.

**Do:**
- Build a **virtuous cycle**: ship feature → collect telemetry → analyze errors/inputs/outputs → update evals with production data → experiment on prompts/models → re-evaluate → promote.
- Instrument the LLM pipeline with **OpenTelemetry spans** at three levels for a static-prompt call: the overall tracking span, the LLM call span, and the output parsing/validation span. Add spans for embedding calculation, vector retrieval (RAG), and parent spans for chained/agentic flows.
- Track at minimum: user input, raw LLM output, parsed/validated output, every error (network/timeout/LLM/parse), user feedback if any, token counts (cost), prompt-construction details.
- Set **non-urgent SLO alerts** for LLMs — Slack/Teams, never page. LLM failures inform planned corrective action, not emergency response.
- **Programmatic correction of LLM outputs:** when most of an LLM output is "almost right" but fails a parse, fix it in code first. Honeycomb's Query Assistant went from 25% error rate to <1% largely by structurally fixing the parse (e.g., stripping an invalid column from a `COUNT`).
- Treat the eval dataset as living: golden data + larger synthetic/curated data; track task function + scoring function; **do not chase 100% pass rate** (regular 100% = not enough representative inputs).

**Don't:**
- Don't ship "bug fixes" without re-running evals and observing production error rate.
- Don't rely on out-of-the-box generic metrics ("helpfulness", "tone", "groundedness"); they report green while saying nothing about your use case.
- Don't page on LLM SLO alerts. Page should always be actionable; LLM failures usually aren't.
- Don't feed LLM outputs into downstream code without **parsing/validation** — untrusted LLM output in your trust boundary is the prompt-injection-by-default posture.

**Code:**
```jsonc
// Honeycomb Query Assistant — LLM produced "almost right" JSON, structurally wrong in
// the COUNT clause (COUNT doesn't take a column).
{
  "calculations":[
    {"op":"COUNT", "column":"exception.message"}    // bug: extra column
  ],
  "filters":[
    {"column":"exception.message","op":"exists"},
    {"column":"parent_name","op":"exists"}
  ],
  "breakdowns":["exception.message","parent_name"],
  "orders":[{"op":"COUNT","order":"descending"}]
}

// Corrected programmatically before parse validation:
{
  "calculations":[
    {"op":"COUNT"}                                   // fix applied: drop column
  ],
  "filters":[
    {"column":"exception.message","op":"exists"},
    {"column":"parent_name","op":"exists"}
  ],
  "breakdowns":["exception.message","parent_name"],
  "orders":[{"op":"COUNT","order":"descending"}]
}
```
- This is exactly the kind of structural fixup that pushed Query Assistant from 25% → 14% error rate without prompt engineering.
- *Ref: Chapter 22 "AI Observability" — "Intervening on Correctable Errors"*

---

### Golden Signals (Google SRE) and RED/USE

**Principle:** When in doubt about what to monitor, start with Google SRE's four **golden signals**:
- **Latency** — time to service a request.
- **Traffic** — demand on the system (req/s, msgs/s, transactions/s).
- **Errors** — rate of failures, in absolute terms and as a fraction of traffic.
- **Saturation** — how "full" the service is; memory, CPU, disk, scaling limits.

**RED method (for services):** **Rate** · **Errors** · **Duration** (latency).
**USE method (for resources):** **Utilization** · **Saturation** · **Errors**.

**Do:**
- Mix the four (or all of RED+USE) into dashboards by audience: business health for product, error budget for SRE, capacity for ops.
- For frontends, also track **Core Web Vitals** — LCP (load speed), CLS (visual stability), INP (responsiveness).
- Distinguish *latency to user* from *latency to service* — load-balancer time vs application time.

**Don't:**
- Don't measure only what's easy. The most-relevant signals often take work to surface.

*Ref: Trade-offs of method choice are a recurring theme in the book; golden signals via Google SRE as cited in "Putting It All Together" (Schwarz) and the Observability Engineering chapter 1 framing*

---

### Production First — Test In Production, Not Just In Staging

**Principle:** Pre-production environments can never fully replicate production conditions: data volumes, request shapes, third-party API versions, the long tail. Production is the only true environment, and you should structure systems to let you observe real traffic in real time.

> If a system has high observability, it allows you to continually answer open-ended questions about the inner workings of your applications to explain any anomalies, without hitting investigative dead ends.

**Do:**
- Emit the same telemetry to your pre-prod as you do to prod. The observability pipeline should not branch on environment.
- Use **feature flags** with progressive activation strategies (internal users → percentage rollout → by segment) to test in production with bounded blast radius.
- Capture *high-cardinality* signals from production traffic; tail sampling is fine for traces but not for events you need to slice by user.

**Don't:**
- Don't trust a staging environment to validate production behavior under load — it doesn't.
- Don't treat flaky production as "tolerable" — every flaky event is a forensics loss.
- Don't pull telemetry out of the loop at deploy time — the most-interesting moments are during and after deploys.

*Ref: Chapter 1 — philosophy throughout; "How Observable Is Your Software?"*

---

### Wide Events — The Unit of Observability

**Principle:** A **wide event** is a single structured record that carries rich context — user id, request id, build version, deployment id, environment, route, status, latency, error code, retry count, dependency call graph, business attributes, etc. The more *wide* (contextual and high-cardinality) the event, the more questions it can answer.

**Do:**
- Prefer **structured wide events** that include as much context as useful — emit once, query many ways later.
- Include *business* attributes alongside technical ones — `customer_id`, `transaction_type`, `region`, `feature_flag_state`. These are the dimensions the on-call will want at 2am.
- Use OpenTelemetry-compatible attributes to keep the data portable across stacks.

**Don't:**
- Don't optimize storage by stripping "unneeded" attributes at emission — you cannot predict which dimension the next incident will require.
- Don't store telemetry only as pre-aggregated metrics — those lose the dimensions you'd need to investigate.

*Ref: Chapter 1; tied to "high-cardinality" theme throughout*

---

### The "Two Modes" of Debugging in Distributed Systems

**Two failure modes the authors highlight:**

1. **Single-thread-of-control debugging** — local reasoning over a single request. Tracing serves this excellently.
2. **Statistical debugging across many requests** — "the 142nd slowest user", "the hidden timeouts hidden by p99.9". Trace slicing + high-cardinality events serve this.

**Do:**
- Use **traces** for single-request path analysis ("why was THIS request slow?").
- Use **wide events** + multidimensional queries for cohort analysis ("why are THESE requests slow?").

**Don't:**
- Don't conflate the two. Traces are not the right tool for "what's the Nth most load-generating customer"; pre-aggregated metrics are not the right tool for "show me a single customer's experience."

*Ref: Chapter 1 "How Observable Is Your Software?" — the bullet list; Chapter 22 for the multi-dimensional angle*

---

### Performance Engineering — Infrastructure Purchasing Models (Six-Step Spectrum)

> Six models for obtaining compute capacity, in increasing cost-per-flexibility tradeoff:
> 1. Capital expenditure (own datacenter, e.g., Oxide Computer)
> 2. Reserved capacity (AWS Savings Plans, Azure Savings Plan, Google Committed/Sustained Use Discount)
> 3. Persistent, defined capacity (EC2, VMs, Compute Engine)
> 4. Interruptible, defined capacity (Spot, Azure Spot, Preemptible)
> 5. Persistent, elastic capacity (Fargate, Container Apps, Cloud Run)
> 6. Interruptible, flexible, for short requests (Lambda, Functions, Cloud Functions)

**Do:**
- Use observability data to drive the mix; not all workloads are right for serverless.
- For Kubernetes, use **Karpenter** + spot/interruptible for stateless workloads; pack workloads efficiently; size machines to common pod configurations; use OTel Collector daemonsets for utilization metrics.

**Don't:**
- Don't default to one model out of habit. Cost and capability profiles differ; let the workload choose.

*Ref: Chapter 2 — "Optimizing cost without modifying code"*

---

### Operational Discipline — Team, Culture, Buy-in

**Observability is a team sport.** LLMs force this; performance engineering does too. Spreading knowledge across the team is faster than building a "perf team" bottleneck.

**Do:**
- Pair senior ICs with junior ICs on investigations — observability is more equitable than intuition, and the data should be available to everyone.
- Treat investigations and evals as a learning loop — every error in production becomes a candidate for an eval update or a code change.

**Don't:**
- Don't gate observability behind a separate ops or perf team; it's a general engineering skill.

*Ref: Chapter 22 "Observability Is a Team Sport"; Chapter 2 "Building a Performance Engineering Practice"*

---

### Anti-Patterns (Stated or Implied)

- **Three-pillar pilots:** still writing each event to three systems because "that's observability now." → *fix:* unify.
- **Dashboards as the answer:** pre-built dashboards by "what we thought we'd care about" → *fix:* wide events you can group arbitrarily.
- **P50 thinking:** measuring only means and standard p99s on top-line "health" while the actual user complaints are in the tail. → *fix:* heatmaps, percentiles you choose for the right reason, *and* the ability to slice.
- **Test-after-the-incident observability:** "we need better dashboards" after a problem, then nothing changes until the next incident. → *fix:* invest in instrumentation depth *before* the next incident; "all-modes data" trumps "best-guess dashboards."
- **Out-of-the-box LLM metrics:** "helpfulness", "tone", "groundedness" reporting green while the user experience is broken. → *fix:* domain-specific evals *and* production telemetry.
- **Single-strategy retries:** retry without backoff or jitter. → *fix:* exponential backoff + jitter; cap retries; pair with circuit breakers.
- **Implicit, undocumented SLIs.** → *fix:* write them down; calibrate against incidents.

## Decision Heuristics / Checklists

- **Picking a telemetry store:** must support high-cardinality grouping and slow queries over weeks. If it can't answer "the 142nd slowest user", it's not observability 2.0.
- **Picking a profiling strategy:** prefer continuous + indexed to trace spans over one-off captures.
- **Picking an LLM eval data strategy:** start with golden data hand-curated by humans; generate synthetic datasets; feed in real production data once stable enough; aim for ~50%+ pass rate, not 100%.
- **Picking an SLO budget policy:** page when burn is 2x steady-state; warn at 1x; remind at 0.5x. (Conventional but worth restating.)
- **Picking a perf-investment cutoff:** when cloud bill × fraction saved < engineer salaries saved, consider whether to optimize at all. Performance for performance's sake is the wrong default.
- **Picking a vendor vs. build:** the goal is the property (observability), not the tool. Adopt whichever path gets you to the litmus test faster.

## Key Takeaways

1. **Observability is a property of the software**, not a category of tool. Adopt it that way.
2. **Unified telemetry** is the only paradigm shift the authors recognize — wide events in a single store beat the three pillars.
3. **You cannot set up the data in advance** for every question you'll be asked at 2am. Pre-collect wide, high-cardinality events.
4. **Profile + trace + heatmap** are complementary. Each alone leaves you blind; all three together answer "what was slow, for whom, why."
5. **LLM systems force observability** because traditional testing cannot apply. Build the eval ↔ telemetry virtuous cycle.
6. **Evals ≠ observability.** Use both. Evals iterate in controlled environments; observability reveals reality.
7. **Programmatic correction** of mostly-right LLM output is a quick win before prompt engineering.
8. **Set non-urgent alerts on LLM SLOs** — they signal planned corrective work, not emergencies.
9. **Treat observability as a general engineering skill**, not a specialist's. Spread the knowledge.
10. **Don't conflate observability with monitoring, vendor pitches, or dashboards.** Judge by the litmus test.

## Cross-References
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] (AWS-side observability primitives: CloudWatch Synthetics, RUM, X-Ray)
- Related: [[../Continuous_Deployment.md]] (CD exposes every observability gap; observability is the feedback loop CD needs)
- Related: [[../Modern_Software_Engineering.md]] (the "feedback" and "empiricism" principles are observability before the term)
- Topic index: [[../INDEX.md]]
