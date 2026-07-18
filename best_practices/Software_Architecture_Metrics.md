# Software Architecture Metrics

**Authors:** Christian Ciceri, Dave Farley, Neal Ford, Andrew Harmel-Law, Michael Keeling, Carola Lilienthal, Joao Rosa, Alexander von Zitzewitz, Rene Weiss, Eoin Woods
**Topic tags:** `#architecture` `#general` `#testing`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/Software Architecture Metrics/Software Architecture Metrics.md` · `summaries/Software_Architecture_Metrics.md`

## TL;DR
A practitioner's playbook for measuring architecture quality. Covers the four DORA metrics, fitness functions and the fitness function testing pyramid, Modularity Maturity Index (MMI), structural metrics (coupling / cohesion / cyclomatic complexity / connascence), private builds for imperfect DevOps, sociotechnical KPIs, GQM for unknown measurements, and golden rules for structural erosion. Use metrics to govern architecture, not to grade people.

---

## Best Practices by Topic

### The Four Key Metrics (DORA)

**Principle:** Pair two throughput metrics with two stability metrics; the combination matters more than any individual value.

**Do:**
- Track deployment frequency, lead time for changes, change failure rate, time to restore service.
- Use rolling 31-day windows for throughput metrics; 120 days for time-to-restore.
- Count "zero" deployment days as deployments so frequency isn't inflated.
- Include only *successful* builds in lead-time calculations.
- Treat the highest non-production environment as a proxy when production data is unavailable.
- Make raw data, calculations, and definitions openly visible to everyone.
- Use mean *and* median for time-to-restore: mean is sensitive to outliers during learning, median is stable for ongoing reporting.

**Don't:**
- Don't compare different teams using the same metric values — context differs.
- Don't average an average (especially for lead time across fan-in pipelines).
- Don't claim a metric without defining "failure in production" (anything preventing users from completing tasks, not cosmetic defects).
- Don't gate the four key metrics behind executive-only access — that kills their biggest strength.

**Code / Measurement Pattern:**
```
Deployment frequency = (sum successful deployments / 31 days), including zero days
Lead time            = mean(per-change commit-to-deploy) then mean over 31 days
Change failure rate  = (resolved failures in window) / (total deployments in window)
Time to restore      = mean AND median time-to-resolution over 120 days
```

*Ref: Software Architecture Metrics.md — "Four Key Metrics Unleashed" / "Capture and Calculation"*

---

### Fitness Functions

**Principle:** An architecture fitness function is any mechanism providing objective evaluation criteria for architecture characteristics. A metric only becomes *engineering* when automated and applied on every code change.

**Do:**
- Categorize every fitness function along six mandatory dimensions: breadth of feedback (atomic/holistic), execution trigger (triggered/continuous), execution location (CI/CD/test/production), metric type (boolean/discrete/time-series), automation, and mapped quality attribute (ISO 25010).
- Add optional categories when useful: temporary/permanent, static/dynamic, target audience, applicability scope.
- Wire fitness functions into CI as build-breaking checks.
- Keep fitness functions outcome-oriented, not implementation-prescriptive.
- Treat fitness functions as automated checklists (Gawande's *Checklist Manifesto*) — codify important-but-skippable-under-pressure principles.

**Don't:**
- Don't overuse fitness functions to the point they impede delivery — they should encode important, not urgent, principles.
- Don't confuse metrics with fitness functions: a dashboard metric is *evidence after the fact*; a fitness function is a *proactive force*.
- Don't ignore the developer ergonomics of the test — failures must be actionable.

**Code (ArchUnit — Java):**
```java
public class CycleTest {
  @Test
  public void test_for_cycles() {
    slices().matching("com.myapp.(*)..")
           .should().beFreeOfCycles();
  }
}
```

*Ref: Software Architecture Metrics.md — "The Fitness Function Testing Pyramid" / "Progressing from Metrics to Engineering"*

---

### The Fitness Function Testing Pyramid

**Principle:** Build a broad base of fast, cheap, triggered-atomic tests; layer on slower holistic and continuous tests; reserve the top layer for the most realistic, highest-fidelity signals.

**Layer definitions:**

| Layer | Trigger × Breadth | Example | When to use |
|-------|-------------------|---------|-------------|
| Bottom | Triggered atomic | Unit test coverage > 90%, cyclomatic complexity checks, static analysis | Broad base — start here |
| Middle | Triggered holistic OR continuous atomic | Integration tests with network latency, periodic load tests, nightly cross-cutting checks | Cross-cutting concerns in test env |
| Top | Continuous holistic | Revenue/minute with time-of-day corridor, chaos engineering, deployment-time regression | Fewest in number; highest signal; least deterministic |

**Do:**
- Start at the bottom layer, learn, then add upward.
- Decompose composite quality attributes (e.g., reliability → availability + data integrity) until each piece is measurable.
- Visualize results on dashboards shared with the team.

**Don't:**
- Don't put everything at the top — nondeterminism and maintenance cost compound.
- Don't skip the bottom layer — without it you lose fast feedback on every commit.

*Ref: Software Architecture Metrics.md — "The Fitness Function Testing Pyramid" / "Examples and Their Full Categorization"*

---

### Modularity Maturity Index (MMI)

**Principle:** Ground technical-debt measurement in cognitive science: chunking (modularity), hierarchical organization, and schemas (pattern consistency). Score 0–10 across 22 weighted criteria.

**Weighting:**

| Principle | Weight | Cognitive basis |
|-----------|--------|-----------------|
| Modularity | 45% | Chunking — brain groups related information |
| Hierarchy | 30% | Hierarchical knowledge organization |
| Pattern consistency | 25% | Schemas — mental models for familiar structures |

**Score interpretation:**

| MMI Range | Action |
|-----------|--------|
| 8 – 10 | Low technical debt — keep monitoring |
| 4 – 8 | Significant debt — plan refactoring |
| < 4 | Refactor OR replace |

**Do:**
- Use tools (Sotograph, Sonargraph, Lattix, Structure101, TeamScale) to compare target vs. actual architecture.
- Run reviews in pairs and discuss results in larger groups to ensure comparability.
- Combine automatic measurements with reviewer judgment in on-site or remote workshops.
- Address implementation debt continuously in daily work; treat design/architecture debt as needing dedicated review cycles.

**Don't:**
- Don't confuse implementation debt (code smells, fixable incrementally) with design/architecture debt (requires full review).
- Don't let architecture erosion continue past the "corridor of low stable maintenance costs" — once outside, every change becomes painful.
- Don't confuse MMI components that are measurable (cycles, layer violations) with those requiring reviewer judgment (responsibility clarity, pattern mapping).

*Ref: Software Architecture Metrics.md — "Improve Your Architecture with the Modularity Maturity Index"*

---

### Structural Metrics — Coupling

**Principle:** Coupling metrics predict how a single change will ripple through the system. Cycle groups grow like "code cancer" once they reach critical size.

**Key formulas:**

| Metric | Formula | Concern threshold (mid-sized 500–5k components) |
|--------|---------|------------------------------------------------|
| Average Component Dependency (ACD) | CCD / component count | High ACD = tight coupling |
| Propagation Cost (PC) | CCD / n² | > 20% concerning, > 50% serious cycle issue |
| Cyclicity | (cycle group elements)² | Use Relative Cyclicity to normalize |
| Relative Cyclicity | Cyclicity normalized to % | One large group much worse than many small |
| Structural Debt Index (SDI) | 10 × links-to-cut + Σ weights | Combined with Relative Cyclicity gives severity + cost |
| Maintainability Level (ML) | Levelized dependency graph, penalty for cycle groups | Good systems > 90, poor systems in 20s |

**Do:**
- Maintain zero package-level cycles.
- Limit component-level cycle groups to ≤ 5 elements.
- Use Robert C. Martin's dependency inversion principle to break any cycle.
- Verify with software-city visualizations (3D: size × complexity × change frequency).

**Don't:**
- Don't let cycle groups grow — Apache Cassandra went from ~450 (v2) → 900 (v3) → 1,300+ (v4) files in one cycle, with 102/113 packages entangled.
- Don't assume cycles are harmless in dynamic languages — they prevent isolated testing, modularization, and replacement.

*Ref: Software Architecture Metrics.md — "Using Software Metrics to Ensure Maintainability"*

---

### Structural Metrics — Size & Complexity

**Principle:** Set hard and soft thresholds; track trends over time; combine multiple metrics into fitness functions.

**Golden thresholds (von Zitzewitz):**

| Metric | Recommended | Limit |
|--------|------------|-------|
| Lines of Code per file | soft threshold | 800 |
| Cyclomatic Complexity (modified) | soft threshold | 15 |
| Maximum indentation depth | soft threshold | 4 |
| Statements per method | soft threshold | 100 |

**Do:**
- Use "Modified" cyclomatic complexity (+1 per switch), "Extended" (+1 per `&&` and `||`).
- Combine metrics into fitness functions: e.g., "fail build if > 10% of code is in files over 800 LoC."
- Use both hard thresholds (break build) and soft thresholds (warning) — see trends, not just absolutes.
- Track metrics daily and render trend charts (Sonargraph-Enterprise, SonarQube, custom dashboards).

**Don't:**
- Don't rely on any single metric — combine LoC, complexity, indentation, and coupling into fitness functions.
- Don't chase LoC for its own sake — meaningful unit size matters more than absolute lines.

*Ref: Software Architecture Metrics.md — "How to Track Metrics over Time" / "A Few Golden Rules for Better Software"*

---

### Change History Metrics

**Principle:** Past volatility predicts future hotspots; track who changes what.

**Metrics:**

| Metric | Definition | Reveals |
|--------|-----------|---------|
| Number of Changes(d) | How often a file changes in d days | Instabilities |
| Code Churn(d) | Lines added/removed in d days | Volatility |
| Number of Authors(d) | Distinct committers | Knowledge monopolies / bus factor |
| Component Rank | PageRank-style over component graph | "Popular" classes to read first |

*Ref: Software Architecture Metrics.md — "Change History Metrics"*

---

### Evolutionary Architecture — Testability & Deployability

**Principle:** The five attributes of testable code (modularity, cohesion, separation of concerns, abstraction, controlled coupling) are *the same* attributes that make code easy to work with and change. Testability is the leading indicator of maintainability.

**Five attributes (universal, not language-specific):**

| Attribute | Definition |
|-----------|-----------|
| Modularity | Parts can change without forcing change in other parts |
| Cohesion | Parts that change together stay close in the code |
| Separation of concerns | Each part solves one problem |
| Abstraction / information hiding | "Seams" that hide implementation from consumers |
| Coupling management | Minimize how often separate parts change together |

**Do:**
- Use tests to drive code design (TDD). Writing tests first produces better-structured code.
- Treat continuous delivery + deployment pipeline as a *first-derivative* — it scopes releasability from commit to independently deployable unit.
- Make pipeline evaluations deterministic — same code, same result, every run.
- Overengineer only for demonstrated needs, not hypothetical futures.

**Don't:**
- Don't try to predict the future of the system — you can't. Build systems that adapt.
- Don't deploy pipelines that cover less than the independently deployable unit — anything less does not determine releasability.
- Don't separate "systems of engagement" from "systems of record" (two-speed IT) — front-end changes always need back-end changes.

*Ref: Software Architecture Metrics.md — "Evolutionary Architecture: Guiding Architecture with Testability and Deployability"*

---

### Private Builds — Surviving Imperfect DevOps

**Principle:** When CI/CD is broken or immature, developers must own validation locally. Private builds are a safety net.

**When to use private builds:**
- QA validates independently without CI integration.
- CI feedback loops are slow or unreliable.
- Automation is happening without understanding.
- A separate team owns CI/CD, so developers have lost the habit of validating locally.

**Survival-mode metrics:**
- Build success rate
- Time to feedback
- Number of bugs found in QA
- Deployment frequency
- Bug density per module, bug resolution time, reopen rate, correlation with code volatility and complexity

**Do:**
- Run private builds including integration tests before pushing to the shared mainline.
- Build broken → fix immediately, never later.

**Don't:**
- Don't automate without understanding why — impressive dashboards with poor quality is the worst outcome.
- Don't cede validation ownership to a separate CI/CD team.

*Ref: Software Architecture Metrics.md — "Private Builds and Metrics: Tools for Surviving DevOps Transitions"*

---

### Sociotechnical Architecture

**Principle:** Architecture decisions are inseparable from team topology and business strategy. Cognitive load (Skelton & Pais) constrains team design; KPIs connect business outcomes to engineering.

**KPI Value Tree (3 levels):**
1. Organizational KPIs — lagging (EBITDA, MAU)
2. Domain KPIs — narrower lagging
3. Metrics — lagging + leading (deployment frequency, change failure rate)

**Do:**
- Use Big Picture EventStorming to map business processes to current software components.
- Use Process-Level EventStorming to map KPIs and hotspots per value stream.
- Add Mean Time to Discover (incident-to-detection) alongside the four DORA metrics.
- Track eNPS (employee Net Promoter Score) for sociotechnical health.

**Don't:**
- Don't treat metrics as targets (Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure").
- Don't compare teams using the same metrics — contexts differ.
- Don't let component ownership changes surprise teams — be explicit about consequences upfront.

*Ref: Software Architecture Metrics.md — "Scaling an Organization: The Central Role of Software Architecture"*

---

### Goal-Question-Metric (GQM)

**Principle:** To measure something well, you must understand *why* you're measuring it. GQM creates traceability from raw data to organizational purpose.

**Hierarchy:** Goal (root) → Questions → Metrics → Data (leaves)

**Goal statement template:** "Improve/Reduce/Detect [object] from the [viewpoint]'s perspective."

**Do:**
- Hold GQM workshops with 2–5 participants (mix technical + non-technical stakeholders).
- Include both positive and negative metrics.
- Look for metrics that answer multiple questions.
- Time-box exploration: < a few hours is suspicious; > a week is questionable.
- Take a photo of the GQM tree — easy to share essence.

**Don't:**
- Don't brainstorm *how* to collect data during metric ideation — defer that step.
- Don't prune prematurely — gather broadly, then prune for strong-signal + low-cost.
- Don't forget to define metrics precisely before data collection.

**Case-study outcome:** A team applied GQM after a third-party rate-limit incident. Nine months later, the same third party had a 14-hour outage; the team detected it in 10 minutes and informed users before anyone noticed.

*Ref: Software Architecture Metrics.md — "Measure the Unknown with the Goal-Question-Metric Approach"*

---

### Architecture Review for MMI (Workshop Process)

**Five-step review process:**
1. Parse source code with analysis tool → record actual architecture
2. Model target architecture
3. Compare target vs. actual → identify deviations
4. Collect technical debt and refactoring candidates
5. Compute metrics → find more debt (large classes, strong coupling, cycles)

**Do:**
- Run reviews with the development team in workshops (not audits).
- Pair reviewers for comparability; discuss in larger groups.
- Treat the team and reviewer as collaborators — often the actual code is better than the original plan.

**Don't:**
- Don't run architecture reviews as surprise audits.
- Don't rely on developers' local IDE view — it can't show the whole system.

*Ref: Software Architecture Metrics.md — "Architecture Review to Determine the MMI"*

---

### Measuring System Qualities (Woods)

**Principle:** Measure throughout the delivery lifecycle — external artifact → internal artifact → external operational → internal operational. Different types give different insights at different points.

**Two-axis classification:**

| | Artifact | Operational |
|---|----------|-------------|
| **External** | Design compliance (weakest, earliest) | Response time, throughput (user-facing) |
| **Internal** | Code complexity, coupling, schema size | Memory, index growth, dev/ops visibility |

**Do:**
- Measure **performance** as latency AND throughput; characterize with mean, median, standard deviation.
- Measure **scalability** at stepped resource levels (e.g., +20% at a time); document ratio behavior.
- Use **MTBF / MTTR** for availability: `Availability = MTBF / (MTBF + MTTR)`. MTTR is designable; MTBF can only be observed.
- Use **RPO** (data loss tolerance) and **RTO** (time to data availability) for disaster-recovery measurement.
- Measure **security** via proxies: static analysis (code), dynamic analysis (deployed), infrastructure scanning; weight by risk (likelihood × impact).

**Don't:**
- Don't chase "five nines" blindly — it's close to meaningless; use failure scenarios instead.
- Don't run security scans only in test environments with the same identities as production.
- Don't include security false positives in trend metrics — they distort the signal.
- Don't use MTBF as the primary availability lever — design for MTTR.

*Ref: Software Architecture Metrics.md — "The Role of Measurement in Software Architecture"*

---

### Pitfalls in Applying Measurement

| Pitfall | Fix |
|---------|-----|
| Focusing on mechanisms rather than measurements | Start with simplest mechanism, add complexity only when value is proven |
| Choosing what is easy rather than what matters | Pick the measurement that drives the most important decision first |
| Focusing on technical over business measurements | Always include at least one business-impact metric |
| Not taking action | Reserve sprint capacity for acting on measurement findings |
| Prioritizing accuracy over usefulness | Stop refining when further precision doesn't change decisions |
| Measuring too much | Periodically audit and switch off low-value measurements |

*Ref: Software Architecture Metrics.md — "Pitfalls"*

---

## Anti-Patterns & Common Mistakes

- **Big Ball of Mud / Distributed Big Ball of Mud:** haphazardly structured sprawling code; arises from accidental complexity. → *fix:* intentional architecture with sociotechnical awareness.
- **Cycle-group "code cancer":** grow continuously once they reach critical size. → *fix:* zero tolerance on package cycles, ≤ 5 elements per component cycle.
- **Resumed four-key-metrics dashboards without shared access:** kills the conversation that drives improvement. → *fix:* open access to definitions, calculations, raw data.
- **Treating metrics as targets (Goodhart's Law):** corrupts the signal. → *fix:* metrics are guides, not goals.
- **"Two-speed IT" / bimodal architecture:** assumes front-end and back-end changes are independent. → *fix:* one speed; design for fast end-to-end change.
- **Fitness functions as documentation, not enforcement:** dashboards ≠ engineering. → *fix:* wire into CI as build-breaking checks.
- **Skipping refinement / strategic-state assessment:** writing strategy or metrics without first checking consistency within the org. → *fix:* ask: globally consistent? consistent within teams? highly varied?
- **Watermelon status (green outside, red inside):** control is an illusion. → *fix:* hard data dashboards over status reports.
- **Resume-driven architecture:** choosing tech for career value, not fit. → *fix:* tie every choice to a measurable diagnosis.

---

## Decision Heuristics / Checklists

- **When to use each DORA metric window:** 31 days for throughput + change failure rate; 120 days for time-to-restore.
- **Picking a fitness-function layer:** start bottom (triggered atomic); add middle (triggered holistic + continuous atomic) for cross-cutting; reserve top (continuous holistic) for highest-fidelity signals.
- **Cycle governance:** zero package-level cycles; ≤ 5 elements per component cycle; dependency inversion to break.
- **MMI action thresholds:** ≥ 8 monitor, 4–8 refactor, < 4 consider replacement.
- **Choosing what to measure:** trace from data → metric → question → goal. If any link is missing, drop or replace.
- **Test-vs-production parity:** identical configuration; different identities for security.
- **Golden-rule set (von Zitzewitz):** (1) enforceable architectural model, (2) zero package-level cycles, (3) component cycles ≤ 5, (4) no copy-paste duplication, (5) < 800 LoC per file, (6) max indentation 4 + modified cyclomatic complexity < 15.
- **DORA + extend:** DORA metrics are foundational but insufficient; supplement with domain-specific metrics, architecture-quality metrics, and sociotechnical measures (MTTD, eNPS).
- **KPI Tree mapping:** every engineering metric should trace to a domain KPI and ultimately an organizational KPI.
- **Static / dynamic thresholds:** static = fixed pass/fail threshold; dynamic = threshold relative to another metric (e.g., response time relative to concurrent users). Use dynamic when the absolute value depends on context.

---

## Key Takeaways

1. **The four key metrics (DORA) are foundational but never sufficient** — pair them with architecture-quality and sociotechnical metrics.
2. **A metric becomes engineering only when automated and applied on every code change** — fitness functions are the unit of architectural governance.
3. **Cyclic dependencies are the primary enemy of maintainability** — zero tolerance at the package level, strict limits at the component level.
4. **Testability and deployability are the same properties under different names** — both reveal and produce good architecture.
5. **Architecture is measurable**: MMI, Maintainability Level, Propagation Cost, Relative Cyclicity, SDI provide objective, comparable scores.
6. **Measure throughout the lifecycle**, not just in production — design analysis, static analysis, runtime telemetry all have a role.
7. **Context matters more than benchmarks** — copy with caution, especially across industries.
8. **Technical metrics must connect to business outcomes** via KPI Value Trees.
9. **Start small and iterate** — 5–6 metric-based rules is the sweet spot; leniency first, then tighten.
10. **Automation and tooling are essential** — SonarQube, Sonargraph, ArchUnit, Structure101, custom CI checks.
11. **Sociotechnical awareness is non-negotiable** — modern architects need facilitation, group dynamics, and business-strategy fluency.
12. **GQM ensures metrics have purpose** — never collect data without a traceable "why."

---

## Cross-References
- Related: [[../Building_Evolutionary_Architectures.md]] — fitness functions evolved from this work
- Related: [[../Head_First_Software_Architecture.md]] — architectural characteristics and trade-offs
- Related: [[../Software_Architect_Elevator.md]] — communicating metrics up and down the org
- Topic index: [[../INDEX.md]]
