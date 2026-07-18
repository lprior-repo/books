# Software Architecture Metrics
**Author:** Christian Ciceri, Dave Farley, Neal Ford, Andrew Harmel-Law, Michael Keeling, Carola Lilienthal, João Rosa, Alexander von Zitzewitz, Rene Weiss, Eoin Woods
**Topic tags:** `#architecture` `#general` `#measurement`
**Language focus:** language-agnostic (Java/C#/Python for tools)
**Sources:** `markdown_output/Software Architecture Metrics/Software Architecture Metrics.md` · `summaries/Software Architecture Metrics.md`

## TL;DR
A practitioner's tour of architectural metrics spanning the four DORA delivery metrics (Forsgren/Humble/Kim), fitness-function pyramids, the Modularity Maturity Index (MMI), Goal-Question-Metric (GQM) workshops, structural metrics (cycles, ACD, PC, Maintainability Level), runtime telemetry (logs/traces/metrics), and sociotechnical metrics (cognitive load, employee NPS). Apply when you need to argue architecture quality with data rather than opinion, build a feedback loop that catches structural decay early, or operationalize evolutionary architecture.

---

## Best Practices by Topic

### The 10 Authors and What They Actually Contribute

**Principle:** This book is a chorus — each author brings a specific lens, and the value comes from the variation in approaches.

**Do:**
- Read chapters as standalone essays; the overlap between them is intentional, but each author's framing differs.
- Match the chapter to your problem: Ciceri for DevOps transitions, Farley for evolutionary architecture, Ford for fitness functions, Harmel-Law for DORA metrics, Keeling for GQM, Lilienthal for MMI, Rosa for sociotechnical systems, von Zitzewitz for structural metrics, Weiss for fitness functions testing pyramid, Woods for measurement in architecture.
- Expect honest disagreement between authors — e.g., Harmel-Law treats DORA metrics as headline, Woods treats them as one slice of a broader measurement story.
- Treat the case studies (YourFinFreedom, Civis, Equifax) as full worked examples; don't reduce them to bullet points.

**Don't:**
- Don't read it as a single unified thesis — each author's contribution is independent.
- Don't skip the case studies; they're where the abstract principles become concrete.

*Ref: Software Architecture Metrics.md — Preface, "What Will You Learn?", "Who This Book Is For"*

---

### The Book's Five-Part Arc

**Principle:** The book is structured to mirror the lifecycle of measurement work: why, what, how, when, where.

**Do:**
- Read in order: Intro → Four Key Metrics → Fitness Function Pyramid → Evolutionary Architecture → MMI → Private Builds → Sociotechnical Scaling → Measurement in Architecture → Progressing from Metrics to Engineering → Maintainability Metrics → GQM.
- Use the chapters in any order, but lean on the cross-references between them.
- Notice the case-study arc: an unnamed product engineering org, YourFinFreedom, Civis, theoretical ride sharing — each adds context that the principles lack.

**Don't:**
- Don't skip the introductory chapters; they establish the mental models that later chapters depend on.
- Don't read it cover-to-cover without taking notes; the density rewards slow reading.

*Ref: Software Architecture Metrics.md — Table of Contents*

---

### Why Measure Architecture at All

**Principle:** Architecture metrics are early-warning radars for technical debt and, when paired with business outcomes, force a conversation between the engineering tiller and the engineering crew.

**Do:**
- Treat architecture as a journey of learning and discovery; metrics let you see trends over time, not just snapshots.
- Pair structural metrics with business/quality attributes (time-to-market, MTTR, churn).
- Surface raw data, calculations, and definitions alongside the headline figure; transparency deepens engagement.
- Use measurement as a continuous process that informs the next architectural decision; not a one-time audit.

**Don't:**
- Don't defer measurement until after code reaches production; instrument the delivery pipeline from day one.
- Don't grade metrics purely on what is easy to measure — start with metrics that drive action.
- Don't let "mechanism-building" (logging infrastructure) crowd out actual measurement insight.

**Code:** *Ref: Software Architecture Metrics.md — "Chapter 7. The Role of Measurement in Software Architecture"*

---

### Four Key Metrics (DORA) — Deployment Frequency, Lead Time, Change Failure Rate, Time to Restore Service

**Principle:** The four metrics come from a mental model that runs from a developer's commit to a change running in production; the *combination* prevents optimizing throughput at the expense of stability.

**Do:**
- Define each metric explicitly for your circumstances and apply the same scope across all four.
- Track deployment frequency as a *frequency*, not a count — sum successful deploys per day and report a 31-day mean.
- Use lead-time-for-changes = elapsed time for a single change from clock-start (commit/trunk-merge) to clock-stop (final deploy to prod).
- Time-to-restore = time from service-failure ticket *opened* to *closed*; rolling back to recover service is acceptable.
- Use failure = "users unable or disinclined to complete a task" — apply judgment consistently.
- Mean over 120 days for time-to-restore; report median or mean and stay consistent.

**Don't:**
- Don't average an average; compute daily totals then aggregate.
- Don't include failed or scheduled CI runs in the throughput numbers.
- Don't include infra-only builds or time-triggered runs; only count deploys that change the service.
- Don't require manual smoke testing *after* a deploy if you want a clean clock-stop — add a manual gate or close the loop differently.

**Code (Mental Model):**
```
[Commit timestamp] -> [Build/Test/Stage] -> [Deploy timestamp] -> [Production]
                                          (4 instrumentation points)
```
*Ref: Software Architecture Metrics.md — "Four Key Metrics Unleashed"*

---

### The Four Instrumentation Points

**Principle:** You only need four timestamps — commit, deployment, failure detection, failure resolution — to derive all four key metrics.

**Do:**
- Use commit timestamp = when the change is committed (or first merged to main as a proxy).
- Use deployment timestamp = when the *final* production deploy completes.
- Use service-failure timestamps = ticket open/close; tie to monitoring where possible.
- Build an explicit escalation model for ambiguous cases (fan-in pipelines, CAB processes).

**Don't:**
- Don't bury clock-start inside long-lived branches; trunk-based development is the cleanest foundation.
- Don't pick the merge-to-main moment just because it is convenient and call it "best practice" without owning the tradeoff.

*Ref: Software Architecture Metrics.md — "Locating Your Instrumentation Points"*

---

### Pipeline Models for the Four Metrics

**Principle:** Identify which pipeline shape you have — single end-to-end, multiple end-to-end (microservices), subpipelines, or fan-in — because the data-collection cost changes dramatically between them.

**Do:**
- Map your actual pipeline topology before instrumenting; you cannot derive lead-time without knowing where the clock starts and stops.
- For fan-in models, parse each deployment to attribute its originating repo, then walk back to the originating commit.
- Track only successful, service-updating builds; discard failed builds from lead-time math.
- Co-plot deployment counts alongside lead-time to avoid misreading "lots of deploys" as "fast delivery".

**Don't:**
- Don't include infrastructure-only pipelines (e.g., DB backups) or scheduled runs.
- Don't average across wildly different pipeline shapes — that hides the variation you need to see.

*Ref: Software Architecture Metrics.md — "Pipelines as Your First Port of Call"*

---

### Display, Visualization, and Front Page

**Principle:** Display each metric with a bar graph of daily values, the period mean, and one supporting trend line; a "front page" rolls them up so executives can see real-time state in seconds.

**Do:**
- Bar graph: dates on x-axis, daily value on y-axis; show DORA "Elite/High/Low" indicator.
- Co-plot the number of deploys as a faint background line so spikes are contextualized.
- Use PowerBI/Tableau/Metrik/Four-Keys to make the data self-serve and drillable by team.
- Show trend lines (mean, p95) plus a default 31-day window; allow override.
- Encourage teams to read these together — visualizations are starting points for dialogue.

**Don't:**
- Don't put the metric behind access controls; the value is in democratic scrutiny.
- Don't keep raw data, calculations, and definitions secret; opacity kills adoption.

*Ref: Software Architecture Metrics.md — "Visualization", "Front Page", "Discussions and Understanding"*

---

### Ownership, Improvement, and the Architect's Tiller

**Principle:** Once teams see the metrics, they initiate changes themselves — the architect can loosen their grip on the tiller.

**Do:**
- Run a recurring weekly discussion with the team about spikes, ADRs, and the four metrics.
- Use the early weeks to debate *what* the metric means; later weeks to debate *why* the values are where they are; eventually focus on *how* to improve.
- Let teams self-serve their pipeline-specific data.
- Trust that the conversation, not the dashboard, drives improvement.

**Don't:**
- Don't keep the architect as the single owner of architectural decisions; the metrics should empower the team.
- Don't ignore cross-functional feedback (QA, ops, product) — they have skin in the game too.

*Ref: Software Architecture Metrics.md — "Discussions and Understanding", "Ownership and Improvement"*

---

### Fitness Functions as Architectural Metrics

**Principle:** A fitness function is "any mechanism that provides objective evaluation criteria for architecture characteristic(s)" — it turns architectural decisions into testable, automated gates.

**Do:**
- Define the fitness function (target metric + context) at design time, *before* writing the architectural test.
- Make the architectural test part of the CI pipeline so it runs continuously.
- Treat fitness functions as a *checklist of important principles* that run as part of the build, not a complex cabal in an ivory tower.
- Use ArchUnit (Java) or NetArchTest (.NET) for compile-time topology checks.
- Use Scientist-style feature-flagged comparison for runtime fidelity testing.

**Don't:**
- Don't treat the fitness function as documentation; it must be executable code.
- Don't make every possible fitness function a hard gate; allow soft thresholds with warnings.

**Code (ArchUnit — Layer Topology Check):**
```java
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayNotBeAccessedByAnyLayer("Controller")
    .whereLayer("Persistence").mayNotBeAccessedByAnyLayer("Service")
```
*Ref: Software Architecture Metrics.md — "Architecture Fitness Functions", "Case Study: Coupling" (ArchUnit example)*

---

### Fitness Function Categories

**Principle:** Six categories are mandatory (breadth of feedback, trigger, location, metric type, automation, quality attribute); four are optional (temporary/permanent, static/dynamic, audience, applicability).

**Do:**
- Pick categories based on what is *useful for your team*, not for theoretical completeness.
- Use ISO 25010 (or FURPS) to map quality attributes: performance efficiency, compatibility, usability, reliability, security, maintainability, portability, functional suitability.
- Tag every fitness function with its categories so you can audit balance later.
- Continual fitness functions in production (chaos engineering, SLO monitoring) belong in the top layer.

**Don't:**
- Don't include categories that don't drive a decision; they bloat the catalog.
- Don't assume all categories are mandatory — temporary/permanent and static/dynamic are situationally useful.

*Ref: Software Architecture Metrics.md — "Mandatory Fitness Function Categories", "Optional Fitness Function Categories"*

---

### Fitness Function Examples

**Principle:** Examples show how the catalog translates to concrete policy + test combinations.

**Code (Test Coverage — bottom layer):**
```
Example 2-1: Unit Test Coverage > 0.9; 
             Execute on each CI Build; Fail when below target coverage
Example 2-2: Integration Test Coverage > 0.5; 
             Execute on each nightly integration test build; 
             Fail when below target coverage
```

**Code (Network Latency — middle layer):**
```
Example 2-3: Integration test errors = 0% (when network latency is 10s 
             for third-party API call); Execute on each nightly 
             integration test build; Fail when integration test fails
Example 2-4: Integration test errors = 0% ... Fail when test execution 
             duration is > 10 minutes (standard execution time, 
             without network latency is below 5 minutes)
```

**Code (Online Shop Revenue — top layer):**
```
Time frame of day       Min revenue (per min)
01:00 AM – 05:00 AM      € 200
05:01 AM – 07:00 AM      € 400
07:01 AM – 09:00 AM      € 600
09:01 AM – 11:30 AM      € 900
11:31 AM – 01:30 PM      € 1100
01:31 PM – 05:30 PM      € 950
05:31 PM – 07:30 PM      € 1500
07:31 PM – 09:00 PM      € 750
09:01 PM – 00:59 AM      € 300
```
*Ref: Software Architecture Metrics.md — "Fitness Functions: Test Coverage", "Fitness Functions: Integration Tests with Network Latency", "Fully Categorizing Top-Layer Examples"*

---

### The Fitness Function Testing Pyramid

**Principle:** Map fitness functions to a three-layer pyramid — bottom (triggered atomic), middle (triggered holistic OR continuous atomic), top (continuous holistic).

**Do:**
- Build a broad base of cheap bottom-layer tests (lint, complexity, coverage).
- Use middle-layer tests for nightly integration and continuous atomic production monitoring.
- Reserve top-layer tests for holistic checks (full business flow, chaos engineering) and keep their count low.
- Treat "errors in integration test" as a meaningful middle-layer signal because it forces real testing.

**Don't:**
- Don't build a top-heavy pyramid; a few good holistic tests beat many flaky ones.
- Don't try to limit the *number* of bottom-layer tests the way you would for unit tests; cheap and broad is the goal.

*Ref: Software Architecture Metrics.md — "The Fitness Function Testing Pyramid"*

---

### Developing Fitness Functions and Metrics — Process

**Principle:** Align on quality goals with stakeholders *first*, then iterate through backlog, prioritize, define, automate, visualize, and refine.

**Do:**
- Step 1: Identify and document the most important quality attributes with key stakeholders.
- Step 2: Formulate first drafts of fitness functions and target metrics; share in a backlog.
- Step 3: Prioritize for balance — fill gaps, ensure pyramid coverage, start at the bottom.
- Step 4: Finalize definitions and classifications.
- Step 5: Develop the automated test (ideally) that produces the metric.
- Step 6: Visualize results for the team.
- Step 7: Iterate; decommission unused metrics and tighten thresholds as systems improve.

**Don't:**
- Don't automate everything just because you can; some metrics (legal compliance) shouldn't be.
- Don't pick easy-to-measure things first; pick things that change behavior.
- Don't forget to tag categories — they help you select missing dimensions later.

*Ref: Software Architecture Metrics.md — "Developing Your Fitness Functions and Metrics"*

---

### Evolutionary Architecture — Testability and Deployability

**Principle:** The five universal attributes of good software design — modularity, cohesion, separation of concerns, abstraction, coupling — are exactly what makes code testable and systems deployable.

**Do:**
- Use tests to *guide* design; treating testability as a valuable architectural property improves structure.
- Make the deployment pipeline the *definitive* evaluator of releasability; everything affecting releasability must live inside its scope.
- Aim for the deployment pipeline to evaluate exactly the code that reaches production — no parallel "integration later".
- Choose the *independently deployable unit* as the pipeline scope; this is the only sensible scope.

**Don't:**
- Don't over-engineer for scalability, security, or resilience when the system isn't yet there.
- Don't let manual testing substitute for automated tests at scale.

*Ref: Software Architecture Metrics.md — "Evolutionary Architecture: Guiding Architecture with Testability and Deployability"*

---

### Modularity Maturity Index (MMI)

**Principle:** MMI maps three cognitive-science mechanisms (chunking, hierarchy, schema) to three architecture principles (modularity, hierarchy, pattern consistency), producing a 0-10 score that quantifies technical debt.

**Do:**
- Use MMI to decide whether to refactor or replace a system:
  - **MMI 8-10**: low technical debt; stay the course.
  - **MMI 4-8**: considerable debt; refactor selectively.
  - **MMI < 4**: severe erosion; evaluate replacement vs. refactor.
- Calculate the score from weighted criteria in three categories (Modularity 45%, Hierarchy 30%, Pattern Consistency 25%).
- Run architecture review workshops with the architects and developers, not just the metrics tools.
- Maintain target vs. actual architecture comparison (Sotograph, Sonargraph, Lattix, Structure101, TeamScale).

**Don't:**
- Don't rely on metrics alone; nonmeasurable criteria require reviewer judgment.
- Don't allow the same reviewer to score alone — pair reviews and discuss in groups for consistency.

*Ref: Software Architecture Metrics.md — "Improve Your Architecture with the Modularity Maturity Index"*

---

### Architecture Review for MMI

**Principle:** Architecture review compares target vs. actual architecture in a workshop with developers; it surfaces deviations and either prescribes refactorings or redesigns.

**Do:**
- Parse the source code with an analysis tool; capture the actual architecture.
- Model the target architecture alongside the actual.
- Compare; capture technical debt and refactorings.
- Inspect metrics (large classes, cycles, coupling).
- Resolve disagreements: either refactor toward target, or update the target to match the better reality.

**Don't:**
- Don't run architecture reviews in a vacuum — they must involve developers who own the code.
- Don't let the target architecture drift so far from actual that reviews become theater.

*Ref: Software Architecture Metrics.md — "Architecture Review to Determine the MMI"*

---

### Hierarchy and Cycle Detection

**Principle:** Cycles are the most damaging form of structural erosion — they make isolated testing, ownership, and replacement impossible.

**Do:**
- Aim for cycle groups ≤ 5 elements on the component level.
- Treat cycle groups spanning multiple namespaces/packages as zero-tolerance violations.
- Break cycles via the dependency inversion principle (introduce interfaces), by lifting the cycle to a higher level, or by demoting it to a lower-level mediator.
- Track the biggest cycle-group size as your primary cycle metric.
- Run cycle-group-size thresholds as build gates.

**Don't:**
- Don't accept cycles just because "Cassandra has them and seems fine" — at 75% of packages involved, you have a code cancer, not a system.
- Don't wait until cycles are large to refactor; early refactoring is cheap.

*Ref: Software Architecture Metrics.md — "Hierarchy", "The Toxicity of Cyclic Dependencies"*

---

### Pattern Consistency

**Principle:** Pattern consistency is the schema mechanism — when developers recognize a pattern, they reason about unfamiliar code much faster.

**Do:**
- Document design patterns and verify they are consistently applied across the source.
- Model pattern diagrams (e.g., layers, design patterns) in your architecture tool so violations surface.
- Maintain allocation-to-pattern percentages and check for cycle-free relationships among patterns.

**Don't:**
- Don't add patterns ad-hoc; inconsistencies are worse than no patterns at all.

*Ref: Software Architecture Metrics.md — "Pattern Consistency"*

---

### Proportions and Decomposition

**Principle:** Well-balanced proportions at every level — layers, components, packages, classes, methods — indicate a well-modularized system.

**Do:**
- Investigate unusually large modules, classes, and methods; decompose when the proportion is extreme.
- Treat the largest unit's size as an indicator of missed encapsulation.
- Set thresholds for cyclomatic complexity (~15), max indentation (~4), and source-file size (~800 LoC).

**Don't:**
- Don't chase zero violations on legacy code — start with lenient goals that gradually tighten.

*Ref: Software Architecture Metrics.md — "Modularity", "Golden Rules"*

---

### Average Component Dependency (ACD) and Propagation Cost (PC)

**Principle:** Lakos's ACD = sum of "Depends Upon" / node count; PC = ACD / node count, normalized to a percentage representing how coupled the system is.

**Do:**
- Use ACD as a first-look coupling indicator; pair it with component count for context.
- Use PC thresholds based on scale:
  - Small systems (n < 500): high PC less concerning.
  - Midsized (500 ≤ n < 5,000): PC > 20% concerning, > 50% severe.
  - Large (n ≥ 5,000): even 10% is concerning.
- Treat high PC + large ACD as confirmation of structural erosion.

**Don't:**
- Don't interpret low PC alone as healthy; large systems can have low PC despite severe internal coupling.
- Don't compare ACD/PC between systems of wildly different sizes without normalization.

**Code (Formula):**
```
PC = CCD / n²
```
*Ref: Software Architecture Metrics.md — "Average Component Dependency, Propagation Cost, and Related Metrics"*

---

### Cyclicity and Relative Cyclicity

**Principle:** Cyclicity = n² for a cycle group of n; Relative Cyclicity normalizes the sum of cyclicity against the system size.

**Do:**
- Track the largest cycle-group size as a first-line metric.
- Use Relative Cyclicity for portfolio-wide comparison.
- Combine with Structural Debt Index (SDI) for ranking which cycles to fix first.

**Don't:**
- Don't optimize for cycle-group size alone — small but dense cycles (high SDI) may be harder to fix than a larger linear one.

**Code (Formula):**
```
relativeCyclicity = 100 * sqrt(sumOfCyclicity) / n
```
*Ref: Software Architecture Metrics.md — "Cyclicity and Relative Cyclicity"*

---

### Structural Debt Index (SDI)

**Principle:** SDI estimates the effort to break cycles by computing a minimal breakup set, weighted by usage counts.

**Do:**
- Use SDI to rank cycle groups by ease of fix.
- Compute per cycle group and accumulate to module/system levels.

**Don't:**
- Don't use SDI as a sole indicator — pair it with Relative Cyclicity.

**Code (Formula):**
```
SDI = 10 * numberOfLinksToCut + sum(weightOfLinksToCut)
```
*Ref: Software Architecture Metrics.md — "Structural debt index"*

---

### Maintainability Level (ML)

**Principle:** ML condenses cycle structure, verticalization (functional silos), and cyclicity penalty into a single percentage.

**Do:**
- Aim for ML ≥ 90 on well-designed systems.
- Track ML per module; compute a weighted average by component count for the top 75% of components or those with ≥ 100 components.
- Use ML alongside Relative Cyclicity for package-level to capture both component and package structure.
- Compute ML_alt = 100 * (1 - sqrt(sumOfPackageCyclicity) / n_p) to handle package-structure rot that ML alone misses.

**Don't:**
- Don't trust ML alone for small modules (n < 100); use the sliding minimum (ML₃ = (100 - n) + (n/100) * ML₂ when n < 100).
- Don't chase ML on a static codebase; metrics for unchanging code are useless.

**Code (Formulas):**
```
c_i = size(i) * (1 - inf(i) / numberOfComponentsInHigherLevels(i)) / n
ML_1 = 100 * sum(c_i)
penalty(i) = 5/size(i) if size(i) > 5, else 1
ML_2 = 100 * sum(c_i * penalty(i))
ML_3 = (100 - n) + (n/100) * ML_2  if n < 100, else ML_2
```
*Ref: Software Architecture Metrics.md — "Maintainability level"*

---

### Coupling, Cohesion, Connascence

**Principle:** Cohesion lives inside modules; coupling lives between them. Connascence names the strength of coupling between two components (static vs. dynamic, local vs. global, etc.).

**Do:**
- Measure cohesion indirectly through coupling: subunits that depend on outsiders more than on their siblings are poorly cohesive.
- Name modules for their single task; vague names signal unclear responsibilities.
- Use metrics to break module cycles and migrate to well-balanced proportions.

**Don't:**
- Don't measure cohesion directly — it is qualitative.
- Don't assume a "name" is enough; ensure the unit truly has one task.

*Ref: Software Architecture Metrics.md — "Modularity", "Cohesion through coupling"*

---

### Size and Complexity Metrics

**Principle:** Lines of Code, Number of Statements, Cyclomatic Complexity, and Indentation Debt are the workhorses for day-to-day code health.

**Do:**
- Limit files to ~800 LoC (soft threshold).
- Limit Number of Statements per method to ~100.
- Use Cyclomatic Complexity with a threshold of ~15 (error rates rise sharply above 24).
- Use Modified Cyclomatic Complexity if switch statements inflate the metric too aggressively.
- Track maximum indentation ≤ 4 per method.
- Aggregate to Average Cyclomatic Complexity (weighted by Number of Statements).

**Don't:**
- Don't use LoC alone as a complexity measure — it correlates but isn't the same.
- Don't include copyright headers in comment-line counts.

**Code (Cyclomatic Complexity):**
```
CyclomaticComplexity = 1 + count(loops) + count(conditionals) + sum(cases per switch)
```
*Ref: Software Architecture Metrics.md — "Metrics to Measure Size and Complexity", "Cyclomatic complexity", "Indentation debt"*

---

### Change History Metrics (Tornhill)

**Principle:** Version control is a treasure trove — frequent changes, high churn, or single-author files are refactoring candidates.

**Do:**
- Track Number of Changes(d), Code Churn(d), and Number of Authors(d).
- Use Number of Authors (365) = 1 as a knowledge-monopoly red flag.
- Visualize as a "software city" — footprint = file size, height = complexity, shade = change frequency.
- Look for hotspots = tall + dark + large buildings.

**Don't:**
- Don't rely on change frequency alone — pair it with complexity and coupling for richer signals.

*Ref: Software Architecture Metrics.md — "Change History Metrics", "Software city visualization"*

---

### Component Rank (Page Rank for Code)

**Principle:** Apply Google's Page Rank algorithm to the dependency graph; high-rank components are popular (heavily depended on) and are the right starting point when reading unfamiliar code.

**Do:**
- Use Component Rank to prioritize onboarding reading order.
- Combine with complexity and churn for richer views.

**Don't:**
- Don't use Component Rank as a quality metric — it doesn't measure goodness, only centrality.

*Ref: Software Architecture Metrics.md — "Component rank"*

---

### LCOM4 — Lack of Cohesion of Methods

**Principle:** LCOM4 measures the number of disconnected method-field subgraphs in a class; an ideal class has LCOM4 = 1.

**Do:**
- Use LCOM4 > 1 as a hint that a class can be split into smaller, single-responsibility classes.
- Combine with field/method analysis to understand the new class boundaries.

**Don't:**
- Don't rely on LCOM4 in deep class hierarchies — the metric often fails there.
- Don't blindly split a class on LCOM4; understand *why* the methods are disconnected.

*Ref: Software Architecture Metrics.md — "LCOM4"*

---

### Golden Rules for Stopping Structural Erosion

**Principle:** Six enforceable rules prevent >80% of legacy-ball-of-mud outcomes.

**Do:**
- Maintain a formal architectural model that defines parts and allowed dependencies.
- Forbid circular dependencies on namespace/package level.
- Limit circular dependency on source files/classes (cycle groups ≤ 5).
- Avoid code duplication (copy-paste programming).
- Limit source files to ~800 LoC (soft).
- Limit max indentation to 4 and Modified Cyclomatic Complexity to 15 (soft).
- Implement all rules in CI; apply organization-wide.

**Don't:**
- Don't treat these as soft suggestions; tool-enforce them so violations are impossible to ignore.
- Don't let exceptions accumulate; review them.

*Ref: Software Architecture Metrics.md — "A Few Golden Rules for Better Software"*

---

### Track Metrics Over Time

**Principle:** Trend charts of metrics over 90+ days reveal drift before it becomes a crisis.

**Do:**
- Gather metrics nightly in an automated build.
- Feed them to a tracking tool (SonarQube, Sonargraph-Enterprise, Jenkins+Sonargraph-Explorer).
- Render trend charts for key fitness functions and coupling/size metrics.
- Set hard *and* soft thresholds: hard breaks builds, soft warns.

**Don't:**
- Don't track only hard thresholds; trend data is what catches slow drift.
- Don't waste effort on metrics you don't intend to look at — review and prune.

*Ref: Software Architecture Metrics.md — "How to Track Metrics over Time"*

---

### Tools for Gathering Metrics

**Principle:** Don't build your own parser — buy or download; the maintenance cost of language evolution is too high.

**Do:**
- Use Understand, NDepend, Source Monitor, SonarQube, or Sonargraph (Explorer/Architect) depending on language and need.
- Verify tools support build-threshold integration.

**Don't:**
- Don't write a custom tool unless you have a genuinely unique metric need.
- Don't pick tools that don't integrate with your CI pipeline.

*Ref: Software Architecture Metrics.md — "Tools to Gather Metrics"*

---

### Goal-Question-Metric (GQM) Approach

**Principle:** Basili & Weiss's GQM hierarchical model: a goal drives questions, questions drive metrics, metrics drive data — always start with the *why*.

**Do:**
- Write the goal explicitly (purpose, object, issue, viewpoint).
- Brainstorm questions that would tell you whether the goal is achieved.
- Brainstorm metrics that answer each question (allow reuse across questions).
- Prune to strong-signal, cheap-to-compute metrics.
- Identify data sources; flag missing data.
- Run GQM as a workshop (2-5 people) with diverse stakeholders.

**Don't:**
- Don't pick metrics before defining the goal.
- Don't accept "metric by itself can only tell you something is wrong" — that's the reason GQM exists.
- Don't endlessly collect more data to satisfy dissenters; hold the line at one or two requests per stakeholder.

*Ref: Software Architecture Metrics.md — "The Goal-Question-Metric Approach"*

---

### GQM Workshop Mechanics

**Principle:** A 2-hour structured session produces a goal, questions, prioritized metrics, definitions, and data sources.

**Do:**
- Prepare a draft goal statement before the workshop.
- Use a whiteboard (or Miro/Excalidraw) with sticky notes.
- Sequence: goal → questions → metrics → data → prioritize → reflect.
- Cluster and de-duplicate sticky notes; have a participant read them aloud.
- Take a picture of the GQM tree at the end.
- Document metric definitions precisely; link to raw data.

**Don't:**
- Don't skip the goal sanity check after collecting metrics — refine if metrics don't actually evaluate the goal.
- Don't force consensus on every metric; prioritize must-have, big-bang-for-buck, and value/effort tradeoffs.

*Ref: Software Architecture Metrics.md — "Run a GQM Workshop"*

---

### GQM Case Study: "Seeing the Future"

**Principle:** A postmortem-driven GQM workshop exposed gaps in operational visibility; metrics generated by the team later caught a major outage nine months before users noticed.

**Do:**
- Use the GQM approach during postmortems to ask "could we have learned sooner?"
- Brainstorm across categories: API usage, system health, job throughput.
- Define metrics like Remaining API calls, % API quota remaining, Heartbeat, % timeout requests.
- Add a heartbeat component to detect silent-failure modes.
- Capture responsibility for retries in the architecture (ADR), not in jobs.
- Build runbooks alongside alerts to eliminate false positives.

**Don't:**
- Don't leave retry responsibility to individual jobs — uncoordinated retries amplify outages (5 retries × 10 attempts = 50 API calls).
- Don't accept "we found out late" as a permanent constraint; design for proactive detection.

*Ref: Software Architecture Metrics.md — "Case Study: The Team That Learned to See the Future"*

---

### Surviving DevOps Transitions with Private Builds

**Principle:** When DevOps culture hasn't landed (ownership shift, silos), private builds restore the local environment as the locus of validation.

**Do:**
- Run a private build locally (developer machine or dedicated cloud environment) before merging to trunk.
- Treat private builds as private: dedicated environment, distinct from shared infrastructure.
- Combine with API contract tests, manual happy-path tests, and E2E where possible.
- Use metrics: Time to Feedback (qualitative), Evitable Integration Issues per Iteration (quantitative), Time Spent Restoring Trunk Stability per Iteration (direct).
- Diagnose the four combinations: feedback × evitability × trunk stability.

**Don't:**
- Don't assume automations owned by a "DevOps team" substitute for developer discipline — they don't.
- Don't let the local environment complexity become an excuse to skip testing.

*Ref: Software Architecture Metrics.md — "Private Builds and Metrics: Tools for Surviving DevOps Transitions"*

---

### Metrics for DevOps-Transition Diagnostics

**Principle:** Use three signals to pinpoint where validation is failing.

**Do:**
- **Time to Feedback** — qualitative, indirect; measures cost and time-to-market.
- **Evitable Integration Issues in Deployed Application per Iteration** — quantitative, indirect; counts avoidable issues per iteration.
- **Time Spent Restoring Trunk Stability per Iteration** — quantitative, direct; measures debugging time on issues that should have been caught locally.

**Don't:**
- Don't chase efficiency of the current provisioning process if it is fundamentally broken; build a self-service.
- Don't assume "QA finds the bugs" — that masks local-validation gaps.

*Ref: Software Architecture Metrics.md — "Metrics", "Metrics in Practice"*

---

### The YourFinFreedom Case Study as a Walking Example

**Principle:** João Rosa's YourFinFreedom narrative threads through the book; it is the most complete worked example of metric-driven architectural evolution.

**Do:**
- Treat YourFinFreedom as a template: monolith → microservices → distributed big ball of mud → intentional architecture with metrics.
- Re-read the case study when the principles feel abstract.
- Notice how each metric (deployment frequency, change fail rate, MTTD, NPS) is anchored to a specific business decision.
- Use the KPI Value Tree (3 levels: org KPIs → domain KPIs → metrics) when applying the case study to your own context.
- Notice the Anna character arc: senior engineer → Solutions Architect; she grows *with* the metrics work.

**Don't:**
- Don't assume YourFinFreedom's exact prescriptions apply; their contexts (Belgian fintech, PSD2, EU expansion) are unique.
- Don't skip the Big Picture EventStorming step in the case study — it's where the strategy crystallizes.

*Ref: Software Architecture Metrics.md — "Scaling an Organization: The Central Role of Software Architecture"*

---

### DevOps Transition Case Studies — When Culture Hasn't Landed

**Principle:** Christian Ciceri's case studies (Unstable Trunk, Blocked Consultant) show what to do when the "DevOps" label hides an "ownership shift" — the DevOps team owns automation, devs lose validation.

**Do:**
- Diagnose the ownership shift before recommending a fix.
- Restore private builds as the unit of validation when shared CI is broken.
- Make the local environment fully usable (DB, data, scripts) for all engineers.
- Track evitability of integration issues, not just their count.
- Measure time spent restoring trunk stability — direct metric for validation gaps.

**Don't:**
- Don't assume that "more automation" fixes a missing-local-validation problem.
- Don't accept "DevOps team" ownership of build pipelines as a permanent state.

*Ref: Software Architecture Metrics.md — "Private Builds and Metrics"*

---

### Sociotechnical Architecture — Conway's Law and Beyond

**Principle:** Software architecture reflects organizational communication patterns (Conway's Law); architects must work *across* functions, not above them.

**Do:**
- Diagnose sociotechnical forces (mission, KPIs, product launches) alongside technical metrics.
- Connect organizational KPIs (EBITDA, MAU, CLV) to domain KPIs and supporting metrics via a KPI Value Tree.
- Map organizational changes with Big Picture EventStorming; visualize domains, events, and team ownership.
- Distinguish leading indicators (deployment frequency, change failure rate) from lagging indicators (MAU, revenue).
- Track Mean Time to Discover as a leading indicator of operational learning.

**Don't:**
- Don't treat metrics as goals (Goodhart's Law); they are guides, not targets.
- Don't compare team performance across teams with different contexts — DORA classification depends on context.
- Don't assume deployment frequency is universally good — for mobile apps, each deploy triggers user notifications and can hurt NPS.

*Ref: Software Architecture Metrics.md — "Scaling an Organization: The Central Role of Software Architecture"*

---

### Leading vs. Lagging Indicators

**Principle:** Lagging indicators measure past outcomes; leading indicators predict whether the action will result in the outcome.

**Do:**
- Build a KPI Value Tree with three levels: organizational KPIs (lagging), domain KPIs (lagging), metrics (mix of lagging and leading).
- For each lagging indicator, identify 1-2 leading indicators that you can act on now.
- Use trends of leading indicators to detect drift before lagging indicators confirm it.
- Combine metrics (e.g., mean time to discover + change fail rate) to surface weak points.

**Don't:**
- Don't conflate metrics with goals; KPIs become targets and targets become gameable (Goodhart's Law).
- Don't treat SLAs as targets-without-tradeoffs — your team *should* have a target, but call it what it is.

*Ref: Software Architecture Metrics.md — "Increasing Software Architecture Intentionality, Guided by Metrics"*

---

### EventStorming and Visual Collaboration

**Principle:** Big Picture EventStorming reveals the actual process, software, and ownership — uncovering misalignment that metrics alone can't.

**Do:**
- Run a Big Picture EventStorming with domain experts, ops, security, and engineers in the room.
- Map domain events on sticky notes and identify emergent domains and their boundaries.
- Overlay current software components and team ownership.
- Add domain KPIs and discuss them explicitly.
- Use Process Modeling EventStorming for one operational value stream at a time.

**Don't:**
- Don't run EventStorming without a facilitator who knows the method.
- Don't skip the domain KPI mapping step — that's where the metric value emerges.

*Ref: Software Architecture Metrics.md — "From Best Effort to Intentional Effort"*

---

### Cognitive Load and Conway's Law

**Principle:** Cognitive load is the limit on information a person can hold in mind; high cognitive load on teams owning software across domains degrades delivery.

**Do:**
- Map teams to domain boundaries, not arbitrary service boundaries.
- When teams own components across domains, treat cognitive load as a diagnosis, not a complaint.
- Apply Team Topologies (Skelton & Pais): stream-aligned teams, platform teams, etc.
- Use "bounded contexts" (DDD) as the unit for team ownership.

**Don't:**
- Don't ship microservices that cross domain boundaries; you create accidental complexity.
- Don't keep monolithic services that obscure domain boundaries; ownership becomes ambiguous.

*Ref: Software Architecture Metrics.md — "Implementing a Distributed Big Ball of Mud"*

---

### Continuous Architecture and Measurement

**Principle:** Architecture is a continuous process; measurement runs through the lifecycle, not at the end.

**Do:**
- Use artifacts (code, docs) for measurement in early phases; use operational telemetry once deployed.
- Distinguish artifact vs. operational and external vs. internal measurement quadrants.
- Build metrics around quality attributes: performance, scalability, availability, security.
- Use estimates and models for predictive measurement when direct measurement is impossible.
- Treat measurement as a continuous feedback loop tied to architectural decisions.

**Don't:**
- Don't wait for production telemetry to start measuring — external artifact measurements (compliance, design quality) are useful from day one.
- Don't over-engineer predictive models; if you can't validate them quickly, prefer direct measurement.

*Ref: Software Architecture Metrics.md — "The Role of Measurement in Software Architecture", "Adding Measurement to Software Architecture"*

---

### Measurement Approaches — Logs, Traces, Metrics

**Principle:** Logs (timestamped events), traces (cross-component event collections), and metrics (numerical measurements) are the three runtime measurement primitives.

**Do:**
- Use infrastructure telemetry first (cloud providers ship it for free).
- Layer application telemetry (APM tools, custom metrics) for context-specific insight.
- Combine for business-relevant metrics (revenue, conversion) — not just technical ones.
- Strive for proactive use of audit logs, not just post-incident analysis.

**Don't:**
- Don't log without a strategy; overwhelming log volume hides signal in noise.
- Don't rely solely on infrastructure metrics — application context matters.
- Don't assume logs replace metrics; you need both for different questions.

*Ref: Software Architecture Metrics.md — "Runtime Measurement of Applications and Infrastructure"*

---

### Performance Metrics

**Principle:** Performance = latency (time per request) and throughput (requests per unit time); measure the distribution, not just the mean.

**Do:**
- Measure distribution of response times (mean, median, standard deviation, percentiles).
- Compare to requirements; decide whether the gap needs architectural attention.
- Model with spreadsheets when direct measurement is too costly.
- Recognize intermittent phenomena as learning opportunities, not noise.

**Don't:**
- Don't measure a single request — performance varies.
- Don't rely on models alone — calibrate against reality as early as possible.
- Don't skip logging for performance measurement during development.

*Ref: Software Architecture Metrics.md — "Performance"*

---

### Scalability Metrics

**Principle:** Scalability = workload capacity vs. resources; linear scaling is ideal but rarely achieved.

**Do:**
- Measure throughput at acceptable performance for specific resource levels.
- Increase resources in steps (e.g., 20%) and measure throughput ratios.
- Model storage scalability (size required for indexing, retention).
- Measure people-cost scalability (ops staff required per workload).
- Track bottlenecks you find in exploration testing.

**Don't:**
- Don't claim scalability without testing non-linear behavior; surprises await.
- Don't assume a single resource dimension — most workloads need mix (CPU + memory + I/O).

*Ref: Software Architecture Metrics.md — "Scalability"*

---

### Availability Metrics — MTTR, MTBF, RPO, RTO

**Principle:** MTTR > MTBF for design priorities (Allspaw); design for fast recovery rather than rare failure.

**Do:**
- Model and test MTTR, RPO, RTO during development; estimate MTBF in operation.
- Use RPO/RTO to express data-loss vs. downtime tradeoffs.
- Watch for varying failure modes — single metrics hide compound complexity.
- Avoid "the tyranny of the nines" — use failure scenarios, not abstract percentages.

**Don't:**
- Don't promise "five nines" without defining what counts as downtime.
- Don't chase MTBF early — it can only be estimated once you have failure data.
- Don't confuse RTO with MTTR; RTO is about data availability, MTTR about service restoration.

*Ref: Software Architecture Metrics.md — "Availability"*

---

### Security Metrics

**Principle:** Measure proxies (static analysis, dynamic scanning, infra scanning) weighted by risk; never wait for an incident to assess security.

**Do:**
- Run static analysis, dynamic analysis, and infrastructure scanning continuously.
- Weight findings by risk (likelihood × impact).
- Maintain test environment parity with production for security results.
- Use a different set of security identities in test vs. production.

**Don't:**
- Don't include high false-positive rates in security metrics — they distort the picture.
- Don't try to "prove" absence of vulnerabilities; you can't. Use expert judgment with good data.

*Ref: Software Architecture Metrics.md — "Security"*

---

### Getting Started with Measurement

**Principle:** Start small, measure what matters, act on results, make it visible, make it continuous.

**Do:**
- Start small — measure one or two actionable metrics.
- Measure something that matters, not what's easy.
- Act on what you measure — allocate sprint time for optimization work.
- Make measurement visible — share regularly, not in private.
- Make measurement continuous — embed in delivery cadence.

**Don't:**
- Don't build elaborate measurement infrastructure before proving value.
- Don't accept "good enough" accuracy when iteration cycles could improve it.

*Ref: Software Architecture Metrics.md — "Getting Started"*

---

### Common Pitfalls in Architecture Metrics

**Principle:** Six common mistakes undermine measurement work; avoid them by deliberate design.

**Do:**
- Focus on the measurement, not the mechanism.
- Pick measurements based on impact, not ease.
- Mix technical and business metrics to keep stakeholders engaged.
- Reserve sprint capacity for acting on measurement findings.

**Don't:**
- Don't prioritize accuracy over usefulness; refine only until decisions improve.
- Don't measure too much — review and prune regularly.

*Ref: Software Architecture Metrics.md — "Pitfalls"*

---

### From Metrics to Engineering — Fitness Function Operations

**Principle:** A fitness function becomes engineering only when it is automated and applied regularly; otherwise it's a metric that gathers dust.

**Principle:** Fitness functions unify the validation of architecture characteristics under a single umbrella — they used to be split across build-time checks, production monitors, forensic logs, etc.

**Do:**
- Use ArchUnit for compile-time topology validation in Java.
- Use NetArchTest for .NET.
- Hand-roll fitness functions for distributed architectures (no off-the-shelf tool exists).
- Implement zero-day security fitness functions as a "security slot" in every deployment pipeline.
- Use Scientist-style fidelity testing for major refactors.

**Don't:**
- Don't wait for the perfect tool; small ad hoc fitness functions are valuable.
- Don't forget that fitness functions are *code* — they keep architects close to the system.

**Code (Pseudocode — Distributed Architecture Fitness Function):**
```python
def ensure_domain_services_communicate_only_with_orchestrator
    list_of_services = List.new()
        .add("orchestrator")
        .add("order placement")
        .add("payment")
        .add("inventory")
    list_of_services.each { |service|
        service.import_logsFor(24.hours)
        calls_from(service).each { |call|
            unless call.destination.equals("orchestrator")
                raise FitnessFunctionFailure.new()
        end
    }
end
```

**Code (Scientist — Fidelity Fitness Function):**
```ruby
def create_merge_commit(author, base, head, options = {})
    commit_message = options[:commit_message] || "Merge #{head} into #{base}"
    now = Time.current
    science "create_merge_commit" do |e|
        e.context :base => base.to_s, :head => head.to_s, :repo => repository.nwo
        e.use { create_merge_commit_git(author, now, base, head, commit_message) }
        e.try { create_merge_commit_rugged(author, now, base, head, commit_message) }
    end
end
```
*Ref: Software Architecture Metrics.md — "From Metrics to Engineering", "Case Study: Coupling", "Case Study: Zero-Day Security Check", "Case Study: Fidelity Fitness Functions"*

---

### ArchUnit and Topological Validation

**Principle:** ArchUnit treats package layout as an executable specification; layered architecture becomes a JUnit test.

**Do:**
- Use ArchUnit to enforce layer boundaries (controller → service → persistence).
- Use Hamcrest matchers inside ArchUnit for English-like policy assertions.
- Build domain-specific layer names that map to your architecture's actual seams.

**Don't:**
- Don't rely on ArchUnit for runtime validation — it's compile-time only.
- Don't enforce layers without first making sure the codebase already follows them (start with a baseline).

*Ref: Software Architecture Metrics.md — "Case Study: Coupling"*

---

### Zero-Day Security Fitness Functions

**Principle:** Treat every project — even idle ones — as having a deployment pipeline; insert a security slot that can fire when new vulnerabilities are disclosed.

**Do:**
- Make security fitness functions part of every project's CI pipeline.
- Configure pipelines to wake on ecosystem changes (code, schema, deploy config, fitness functions).
- When zero-days hit (e.g., Apache Struts CVE-2017-5638 at Equifax), run the fitness function across all projects at once.
- Notify security teams automatically when dangerous versions are detected.

**Don't:**
- Don't rely on manual security audits after a vulnerability is disclosed.
- Don't let dormant projects slip through — they are the easiest targets.

*Ref: Software Architecture Metrics.md — "Case Study: Zero-Day Security Check"*

---

### The Fitness Function Checklist Mentality

**Principle:** Fitness functions are the architect's executable checklist — they prevent "we know this is bad, but we'll come back to fix it later" from being the cause of tech debt.

**Do:**
- Treat fitness functions as Gawande-style checklists for important-but-not-urgent principles.
- Codify rules about code quality, structure, and other safeguards against decay.
- Run them continuously so developers can't skip them under schedule pressure.

**Don't:**
- Don't build an interlocking cabal of fitness functions that frustrates developers; keep them useful and focused.
- Don't retreat to ivory-tower architecting — fitness functions are code, and code keeps you close to the system.

*Ref: Software Architecture Metrics.md — "Conclusion" of Chapter 8*

---

### Cross-Cutting Quality Attributes (ISO 25010)

**Principle:** Quality attributes are the goals; fitness functions are the means; without the former, the latter are decoration.

**Do:**
- Map fitness functions to ISO 25010 quality attributes: functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability.
- Spend time and effort on attributes with big impact on overall goals.
- Limit to ≤ 3 architecture characteristics plus maintainability — too many produces unmanageable complexity.

**Don't:**
- Don't chase all attributes simultaneously — the tension between them is real (e.g., security vs. performance).
- Don't pick attributes because they're standard; pick the ones that affect your business goals.

*Ref: Software Architecture Metrics.md — "Mandatory Fitness Function Categories" (Quality attribute requirements)*

---

### Mental Models and Paradigms (Meadows)

**Principle:** Donella Meadows: "Paradigms are the sources of systems. From them come system goals, information flows, feedbacks, stocks and flows." Metrics reveal paradigm shifts, not just point-in-time issues.

**Do:**
- Recognize that paradigm shifts in your engineering org (e.g., from "ship and forget" to "continuous delivery") require both new metrics and new mental models.
- Use metrics to point at anomalies in the old paradigm.
- Speak and act from the new paradigm with assurance.
- Show teams, don't tell them — let metrics reveal what works.

**Don't:**
- Don't assume metrics will change behavior on their own — the paradigm must shift first.
- Don't dismiss anomalies as noise; they are often the most informative signal.

*Ref: Software Architecture Metrics.md — Donella Meadows epigraphs throughout Chapter 1*

---

### The Hybrid Case Study — Digg V4 as Inappropriate Strategy

**Principle:** Digg's V4 rewrite (PHP monolith → PHP + Python services + Cassandra) is the cautionary tale: clear, consistent strategy that nonetheless failed because the strategy was inappropriate for the business context.

**Do:**
- Recognize that "inappropriate" beats "bad" — every approach works in *some* context.
- Ask whether the strategy fits the business context, not just whether it's internally consistent.
- Preserve internal consistency (architecture, language, data store) — Digg had it, but it didn't save them.
- Recognize that even well-executed strategies fail when the context shifts faster than the strategy.

**Don't:**
- Don't assume a coherent architecture equals a successful strategy.
- Don't copy a successful strategy from one company to another without diagnosing your own context.

*Ref: Software Architecture Metrics.md — "Inappropriate Strategy Is Especially Impactful"*

---

### Strategy Refinement Antipatterns — Manufactured Consent

**Principle:** When senior leaders "refine" a strategy by collecting opinions they already know will support their preferred direction, the result is consensus theater, not refinement.

**Do:**
- Seek out skeptics when refining a strategy.
- Test your strategy against opposing views; if they agree too easily, you haven't found the real skeptics.
- Publish counterevidence and side-goals explicitly when you evaluate strategies.
- Watch for "refinement" that's actually justification.

**Don't:**
- Don't adopt a refinement technique without testing it in practice.
- Don't discard counterevidence because it conflicts with a side goal (e.g., wanting to use Erlang for fun).

*Ref: Software Architecture Metrics.md — "Antipatterns in Refinement"*

---

### Couchbase / Apache Cassandra — A Practical Cycle Story

**Principle:** Apache Cassandra's cycle-group growth from 450 → 900 → 1,300 elements across v2 → v3 → v4 illustrates the "code cancer" metaphor: cycles grow monotonically and resist cleanup.

**Do:**
- Use Cassandra as a cautionary tale; 75% of all elements in large cycle groups is not aspirational.
- Set early warnings on cycle-group size before they become irreversible.
- Treat package cycles as existential threats; namespace cycles of 102/113 packages (Cassandra) make the system opaque.

**Don't:**
- Don't accept "Cassandra is doing fine" as evidence that cycles are acceptable.
- Don't assume big-bang cycle-breaking works; small, frequent refactorings beat large rewrites.

*Ref: Software Architecture Metrics.md — "Entropy Kills Software", Sonargraph visualization of Cassandra*

---

### The Spring Framework as a Positive Example

**Principle:** Spring Framework is widely cited as having limited small cycle groups and well-structured architecture; that hygiene is one reason it's been sustainable for so long.

**Do:**
- Study positive examples (Spring, Linux kernel's subsystem boundaries) alongside negative ones.
- Aim for "few small cycle groups" rather than "zero cycles"; small cycles are tolerable if confined.
- Treat architecture hygiene as a long-term investment; Spring's structure pays off decade after decade.

**Don't:**
- Don't copy Spring's specifics (DI containers, XML configs) without diagnosing why it works.
- Don't assume architecture hygiene alone explains Spring's success — modularity, testability, and community all contribute.

*Ref: Software Architecture Metrics.md — "Entropy Kills Software"*

---

### "The code doesn't lie" — Code Analysis as Ground Truth

**Principle:** Once written, code is a rich source of measurement — but it only reveals what is, not what should be.

**Do:**
- Use static analysis for complexity, coupling, and structural characteristics.
- Use static analysis as a proxy for security (vulnerability count).
- Combine with design analysis to get predictive measurements before code is written.

**Don't:**
- Don't use static analysis alone — it can't measure qualities like security fully.
- Don't skip capturing design intent (design docs, ADRs) for predictive measurement.

*Ref: Software Architecture Metrics.md — "Software Analysis", "Design Analysis"*

---

### The Caveats of Predictive Models

**Principle:** Models (spreadsheets, simulations) are valuable when calibrated; without calibration, they're just elaborate guesses.

**Do:**
- Use models when direct measurement is impossible (e.g., scalability at scale you can't reach).
- Calibrate models against real measurements as early as possible.
- Treat model output as one input to a decision, not the decision itself.

**Don't:**
- Don't build complex models when simple observation will do.
- Don't trust models that aren't validated against reality.

*Ref: Software Architecture Metrics.md — "Estimates and Models"*

---

### Fitness Function Categories by Layer — Worked Examples

**Principle:** Categorize each fitness function by pyramid layer and you'll see whether you have a balanced portfolio.

**Do:**
- Audit your fitness function catalog quarterly; aim for a balanced pyramid.
- Use breadth (atomic vs. holistic) and trigger (triggered vs. continuous) as the primary layer determinants.
- Tag every function with quality attribute (ISO 25010) and metric type.
- Identify gaps: are you missing continuous holistic top-layer tests? Atomic atomic tests?

**Don't:**
- Don't measure static vs. dynamic only; mix the two dimensions intentionally.
- Don't assume atomic = unimportant; atomic functions are the foundation.

*Ref: Software Architecture Metrics.md — "Fitness Function Categories: Catalog Overview"*

---

### The Top Layer in Practice — Chaos Engineering

**Principle:** Chaos engineering (e.g., Netflix's Simian Army) is the canonical continuous-holistic fitness function: it tests production resilience by introducing failures.

**Do:**
- Run chaos experiments in production, not just pre-prod.
- Define the health indicators that will tell you whether chaos caused harm.
- Start small (single instance failure) before compound scenarios.
- Treat chaos results as fitness function outputs — they drive architectural decisions.

**Don't:**
- Don't run chaos without alerting; silent chaos is worse than no chaos.
- Don't assume your architecture is resilient until you've tested it.

*Ref: Software Architecture Metrics.md — "Principles of Chaos Engineering" reference, "The Top Layer"*

---

### The Middle Layer in Practice — Integration Tests

**Principle:** Middle-layer fitness functions (triggered holistic OR continuous atomic) cover most real engineering concerns: API contract, data integrity, end-to-end flows.

**Do:**
- Use triggered integration tests for nightly validation of third-party interactions.
- Use continuous atomic monitoring for response times, error rates, throughput.
- Pair integration tests with explicit failure-injection to test resilience.
- Treat "missing/incorrect information" failures as the largest source of provisioning delay.

**Don't:**
- Don't rely solely on unit tests for integration concerns; you'll catch them in production.
- Don't ignore integration tests because they're "slow" — they are the highest-signal automated tests you have.

*Ref: Software Architecture Metrics.md — "The Middle Layer", "Fitness Functions: Integration Tests with Network Latency"*

---

### The Bottom Layer in Practice — Unit Tests

**Principle:** Bottom-layer fitness functions (triggered atomic) are cheap, fast, and easy to maintain — code coverage, complexity, and linting.

**Do:**
- Build a broad base of bottom-layer tests; they prevent regressions cheaply.
- Wire them into CI; don't allow them to be bypassed.
- Treat build failures as urgent — broken pipelines cascade.

**Don't:**
- Don't limit the *number* of unit tests the way you would for fitness functions; broad coverage is the goal.
- Don't accept build failures as "expected" — they erode trust in the pipeline.

*Ref: Software Architecture Metrics.md — "The Bottom Layer"*

---

### The Quality Attribute Triad — Performance, Scalability, Availability

**Principle:** Three quality attributes (performance, scalability, availability) are deeply linked and need coordinated metrics.

**Do:**
- Measure latency AND throughput for performance — they're inversely proportional but not interchangeable.
- Distinguish scalability from performance; scalability is capacity vs. resources, performance is latency.
- Use MTTR + MTBF + RPO + RTO together to capture availability comprehensively.
- Track bottlenecks found in exploratory testing; they will dominate scalability.

**Don't:**
- Don't promise "five nines" without defining failure scenarios.
- Don't optimize one attribute at the expense of others without explicit tradeoffs.

*Ref: Software Architecture Metrics.md — "Measuring System Qualities"*

---

### Fitness Function Maturity Model

**Principle:** Fitness functions mature as they move from manual to automated, from local to continuous, from individual to portfolio.

**Do:**
- Track which fitness functions are manual vs. automated; aim to automate.
- Track which fitness functions run locally vs. in CI vs. continuously in production.
- Aim for a portfolio where most critical functions run continuously.
- Move fast on automating cheap, high-signal functions; defer expensive ones.

**Don't:**
- Don't try to automate everything at once; prioritize.
- Don't let manual fitness functions be the long-term state for critical checks.

*Ref: Software Architecture Metrics.md — "From Metrics to Engineering"*

---

### When to Skip Strategy Testing

**Principle:** Strategy testing is almost always worth it, but a few scenarios genuinely don't need it.

**Do:**
- Skip testing when the strategy is highly permissive and cheap to apply (you can re-run it if it fails).
- Treat "we did this before" as a yellow flag, not a green one; circumstances change.
- Reserve testing for strategies whose cost-of-failure exceeds the cost of testing.

**Don't:**
- Don't convince yourself that testing isn't worthwhile; that's a red flag.
- Don't skip testing just because leadership set a deadline; testing extends past deadlines.

*Ref: Software Architecture Metrics.md — "When to Test Strategy" (implicit in Chapter 8)*

---

### Evolving Architecture via Testability and Deployability

**Principle:** Testability and deployability are the two tools for sustainable change; they enable the evolutionary approach.

**Do:**
- Treat testability as a design tool, not a verification afterthought.
- Use deployment pipelines as the definitive evaluation of releasability.
- Let tests guide design; testability-focused code is naturally modular, cohesive, abstracted.
- Choose the independently deployable unit as your pipeline scope.

**Don't:**
- Don't separate testability from design quality; they are the same thing viewed differently.
- Don't rely on long integration phases; aim for releasability at every commit.

*Ref: Software Architecture Metrics.md — "Testability: Creating High-Quality Systems"*

---

### The Decoupling Level (DL) Metric — An Alternative Worth Knowing

**Principle:** Mo, Cai, Kazman, Xiao, and Feng (Drexel + U. Hawaii, 2016) developed Decoupling Level as a complexity-measuring metric similar in spirit to Maintainability Level.

**Do:**
- Be aware of DL as an alternative when ML doesn't fit your codebase.
- Watch for tooling that supports DL; patents have historically limited availability.
- Compare ML and DL on the same codebase if you can.

**Don't:**
- Don't pick metrics based on tool availability alone; pick what fits the problem.
- Don't dismiss DL just because it's not in your tool today; ML and DL complement each other.

*Ref: Software Architecture Metrics.md — "Maintainability level" (Decoupling Level reference)*

---

### "Why metrics are not more widely used?" — The Industry's Resistance

**Principle:** Alexander von Zitzewitz identifies five reasons metrics adoption is slow: lack of awareness, niche tooling, need for context, dim returns past 5-6 rules, and capacity loss from tech debt.

**Do:**
- Acknowledge that metric adoption requires cultural change, not just tool installation.
- Pick the 5-6 most important rules; don't chase every available metric.
- Build tools into your CI pipeline; metric rules without automation don't fire.
- Educate developers on metric purpose, not just metric values.

**Don't:**
- Don't expect metrics to fix code without team understanding.
- Don't accumulate metrics; prune ruthlessly.

*Ref: Software Architecture Metrics.md — "Why Are Metrics Not More Widely Used?"*

---

### The CI/CD as the Operational Backbone

**Principle:** Modern CI/CD isn't just deployment; it's the substrate for fitness functions, metric collection, and operational verification.

**Do:**
- Make CI the canonical location for fitness function execution.
- Use CI to capture commit and deployment timestamps for the four key metrics.
- Treat CI failures as architecture signals — a build that fails more often is signaling coupling or complexity.
- Distinguish CI for application code from CI for infrastructure changes.

**Don't:**
- Don't conflate CI failures with code quality issues; sometimes CI is the problem.
- Don't include scheduled, infrastructure-only, or non-service-updating runs in your four-metrics calculation.

*Ref: Software Architecture Metrics.md — "CI/CD", "Locating Your Instrumentation Points"*

---

### Migrations and Big Ball of Mud Recovery

**Principle:** When a system has accumulated into a Big Ball of Mud, the path back is incremental refactoring; replacement is rarely cheaper.

**Do:**
- Use MMI to assess before deciding refactor vs. replace.
- Refactor to break cycles first (highest-leverage structural metric).
- Refactor to remove coupling second.
- Reassess MMI quarterly; track trajectory, not just snapshots.

**Don't:**
- Don't assume a complete rewrite will solve the problem — Digg V4 proved otherwise.
- Don't refactor without measuring; you can't tell if you're making progress without metrics.

*Ref: Software Architecture Metrics.md — "Conclusion" of Chapter 4*

---

### The Cycle-Group Trip-Wire

**Principle:** A cycle group of more than 5 elements is a code cancer that grows; set it as a build-breaker and the cost of fixing cycles is bounded.

**Do:**
- Set cycle group size ≥ 6 as a build breaker.
- Use Sonargraph-Explorer or similar tools for cycle detection.
- Treat cycle-group size growth as a regression; fail the build.

**Don't:**
- Don't accept cycle group size > 5 just because removing them is hard.
- Don't combine cycles across namespaces; namespace-level cycles must be zero.

*Ref: Software Architecture Metrics.md — "How Metrics Can Help"*

---

### Strangler Pattern Hidden in Cycle-Breaking

**Principle:** Breaking a cycle via the dependency inversion principle is a form of the Strangler Fig pattern — you introduce an interface that decouples existing code.

**Do:**
- Use dependency inversion to break cycles (introduce an interface, invert the dependency).
- Apply "lift" or "demote" techniques to break other cycle patterns.
- Combine with existing functionality moves to simplify cycle-breaking.

**Don't:**
- Don't break cycles via copy-paste code; that's a code smell itself.
- Don't accept "hard to break" as a reason to leave cycles.

*Ref: Software Architecture Metrics.md — "The Toxicity of Cyclic Dependencies"*

---

### Wardley Maps vs. Maintainability Level — Complementary Tools

**Principle:** ML measures the *current state* of your codebase; Wardley Maps measure the *ecosystem* in which your code lives.

**Do:**
- Use ML for internal architecture decisions (refactor or replace).
- Use Wardley Maps for external architecture decisions (build vs. buy, when to adopt).
- Combine the two when assessing a major architectural shift.

**Don't:**
- Don't substitute one for the other; they answer different questions.
- Don't conflate "code is complex" with "ecosystem is unstable."

*Ref: Software Architecture Metrics.md — Compare with Wardley Mapping in Crafting Engineering Strategy*

---

### System Thinking Caveats — Reality Wins

**Principle:** "When your model and reality conflict, reality is always right." — even good models mislead when over-trusted.

**Do:**
- Treat models as inputs to a decision, not the decision itself.
- Watch for situations where your model's "intuition" doesn't match reality.
- Update models aggressively when reality contradicts them.
- Build models with stakeholder debate in mind; expose hidden assumptions.

**Don't:**
- Don't fall in love with your model; it's a model, not reality.
- Don't ignore model-reality conflicts because the model "feels right."

*Ref: Software Architecture Metrics.md — "What Systems Modeling Isn't" (also Crafting Engineering Strategy)*

---

### The "Boring Metrics" Principle

**Principle:** Most useful metrics are boring — they're the same measurements you've always taken, validated rigorously.

**Do:**
- Pick metrics that already exist in your organization when possible.
- Apply rigorous process (GQM) to existing metrics before adding new ones.
- Aim for boring metrics that survive across teams and years.

**Don't:**
- Don't chase novelty in metrics; boring means "well understood."
- Don't replace existing metrics just because new ones exist.

*Ref: Software Architecture Metrics.md — Discussion in Chapter 2*

---

### Cross-Reference: Process Modeling EventStorming

**Principle:** Process Modeling EventStorming (Alberto Brandolini) zooms into a single operational value stream; KPIs and hotspots are mapped at this level.

**Do:**
- Use Process Modeling EventStorming for a single value stream at a time.
- Map KPIs explicitly in the workshop.
- Identify hotspots in the process (slow, error-prone, ambiguous steps).
- Use the output to drive metrics (GQM) and architectural changes.

**Don't:**
- Don't try to map everything; one value stream at a time.
- Don't skip the hotspot identification step; it's where the value lives.

*Ref: Software Architecture Metrics.md — "From Best Effort to Intentional Effort"*

---

### The Truth-Truth-Told Architecture of Sociotechnical Metrics

**Principle:** João Rosa explicitly observes that "software architecture, metrics, and KPIs should support the evolution of the organization" — architecture is not just a technical artifact.

**Do:**
- Tie architecture decisions to organizational evolution.
- Recognize that architecture exists *because* the organization exists; it serves the business.
- Build a new generation of architects who can facilitate workshops, understand group dynamics, and contribute to business strategy.

**Don't:**
- Don't treat architecture as "above" the business; it's part of it.
- Don't delegate architecture to a single ivory-tower group; it lives with the team.

*Ref: Software Architecture Metrics.md — "Conclusion" of Chapter 6*

---

### Reflection as Part of the Workflow

**Principle:** GQM workshops, EventStorming sessions, and architecture reviews all close with reflection — "what did we learn that informs the next iteration?"

**Do:**
- Reserve the last 10-15 minutes of any strategy session for reflection.
- Capture lessons in a shared document; review before the next session.
- Use dot voting or similar lightweight techniques to surface consensus quickly.
- Treat reflection as a forcing function, not a nicety.

**Don't:**
- Don't skip reflection under time pressure; that's when you need it most.
- Don't treat reflection as confession; it's diagnosis.

*Ref: Software Architecture Metrics.md — GQM Workshop steps, Step 8*

---

### The "Diagnosis First, Refine Second" Heuristic

**Principle:** Almost every failed strategy skipped diagnosis. Refinement only matters once the diagnosis is solid.

**Do:**
- Form your diagnosis before deciding how to solve the problem.
- Try especially hard to capture perspectives you initially disagree with.
- Supplement intuition with data where you can.
- Accept that sometimes the data you need will be missing — refinement tools help here.

**Don't:**
- Don't let urgency push you past diagnosis.
- Don't treat diagnosis as a formality; it's the foundation.

*Ref: Software Architecture Metrics.md — "Summary" of Chapter 7*

---

### The Three Perspectives Test in Diagnosis

**Principle:** "If you ask five engineers about whether it's possible to merge a given service back into a monolithic codebase, you'll probably get five different answers. That's fine." Capture divergent views in diagnosis; consensus on diagnosis comes after.

**Do:**
- Seek out 3-5 distinct perspectives on every diagnosis.
- Document each perspective faithfully, even those you disagree with.
- Mine for the disagreements that hide the real problem.

**Don't:**
- Don't force consensus on diagnosis; convergence happens at policy, not diagnosis.
- Don't let your own perspective dominate the written diagnosis.

*Ref: Software Architecture Metrics.md — "How to Develop Your Diagnosis"*

---

### Persona-Based Refinement Targets

**Principle:** Different roles should use different refinement techniques — executives default to Wardley, technical leads default to systems modeling, engineers default to strategy testing.

**Do:**
- Match the refinement technique to the role and the audience.
- Use strategy testing when you need to validate narrow mechanics.
- Use systems modeling when leverage points are unclear.
- Use Wardley mapping when ecosystem evolution matters.

**Don't:**
- Don't mandate one technique for everyone; let specialists pick their tool.
- Don't use Wardley maps for narrow mechanics; that's the wrong level of zoom.

*Ref: Software Architecture Metrics.md — "Building Your Toolkit"*

---

### The "Permissive Strategy" Compounding Effect

**Principle:** Permissive strategies cost less to implement but offer less enforcement; pick permissiveness based on what you can afford to fail.

**Do:**
- Use permissive strategies for widely-applicable, low-stakes decisions.
- Use prescriptive strategies when you need uniform adoption (e.g., security).
- Pair permissive strategy with escalation paths to a senior decision-maker.
- Aim for the highest-permissive altitude that still delivers your outcomes.

**Don't:**
- Don't pick permissiveness to avoid conflict; some conflicts need prescription.
- Don't rely on permissive strategies for security-critical decisions.

*Ref: Software Architecture Metrics.md — "Strategy Altitude"*

---

### Hard vs. Soft Thresholds

**Principle:** Hard thresholds break the build; soft thresholds only warn. Choose the level based on the cost of false positives vs. false negatives.

**Do:**
- Use hard thresholds for cycle-group size, package cycles, security vulnerabilities.
- Use soft thresholds for complexity, file size, code duplication.
- Track trends of soft-threshold metrics separately; slow drift matters.

**Don't:**
- Don't hard-threshold metrics with high variance; you'll desensitize the team.
- Don't soft-threshold metrics where the cost of regression is catastrophic.

*Ref: Software Architecture Metrics.md — "How to Track Metrics over Time"*

---

### Metrics Without Organizational Buy-In

**Principle:** A perfectly designed metric that nobody looks at is worthless; organizational buy-in is a prerequisite for impact.

**Do:**
- Involve stakeholders in metric definition (GQM).
- Make metric dashboards visible and self-serve.
- Hold weekly discussions about the metrics.
- Reward teams that improve the metrics through natural work, not gaming.

**Don't:**
- Don't launch a metric in a vacuum.
- Don't assume dashboards drive change; conversations do.

*Ref: Software Architecture Metrics.md — "Discussions and Understanding"*

---

### The Internal Tooling Trap

**Principle:** Building internal metrics infrastructure is absorbing; resist the urge to build the perfect tool when an existing one suffices.

**Do:**
- Use commercial or open-source tools (Understand, NDepend, SonarQube, Sonargraph).
- Use cloud-provider telemetry first (CloudWatch, Azure Monitor).
- Build custom tools only for genuinely unique metrics.

**Don't:**
- Don't write a parser from scratch unless nothing exists.
- Don't over-invest in tooling at the expense of measurement value.

*Ref: Software Architecture Metrics.md — "Tools to Gather Metrics"*

---

### The Boring Technology Choice (Calm Engineering Strategy)

**Principle:** Dan McKinley's "Choose Boring Technology" principle applies to metrics: pick well-understood tools over shiny new ones.

**Do:**
- Default to existing telemetry (logs, traces, metrics) before custom solutions.
- Use ISO 25010 or FURPS for quality attributes rather than inventing your own taxonomy.
- Reuse the four DORA metrics rather than designing bespoke delivery metrics.

**Don't:**
- Don't invent a new metric when an existing one works.
- Don't pick a metric because it's novel; pick it because it's actionable.

*Ref: Software Architecture Metrics.md — "Choose Boring Technology" reference, Dan McKinley*

---

### The Incident-Driven Metrics Opportunity

**Principle:** Postmortems expose weaknesses in operational visibility; use them as opportunities to introduce new metrics.

**Do:**
- Run a GQM workshop during postmortems.
- Ask "what metrics, if they existed, would have caught this earlier?"
- Implement the top 1-2 metrics immediately.
- Treat the postmortem as a metrics expansion opportunity, not just a retrospective.

**Don't:**
- Don't treat postmortems as blame sessions; they're measurement opportunities.
- Don't promise all the metrics at once; pick the highest-value.

*Ref: Software Architecture Metrics.md — Case Study: "The Team That Learned to See the Future"*

---

### The Cross-Functional KPI Tree

**Principle:** Anna's KPI Value Tree at YourFinFreedom connected EBITDA → domain KPIs → metrics; this is the canonical structure for sociotechnical measurement.

**Do:**
- Start with organizational KPIs (financial or business outcomes).
- Decompose into domain KPIs (one level down, still lagging).
- Decompose into metrics (mixed lagging and leading).
- Refresh the tree quarterly; let it evolve with the business.

**Don't:**
- Don't skip the lagging indicators; they prove you moved the right needle.
- Don't overpopulate the leading-indicator layer; too many signals = noise.

*Ref: Software Architecture Metrics.md — "KPI Value Tree", Figure 6-11*

---

### The Recurring Cadence for Architecture Review

**Principle:** Architecture review isn't a one-off; it must recur to maintain target vs. actual alignment.

**Do:**
- Schedule architecture review workshops quarterly or biannually.
- Use the same review framework (MMI, hierarchy, pattern consistency) each time.
- Compare scores across reviews to track trajectory.
- Invite new developers to broaden the review's coverage.

**Don't:**
- Don't treat architecture review as a one-time audit.
- Don't let the review get derailed by tactical issues; focus on structural drift.

*Ref: Software Architecture Metrics.md — "Architecture Review to Determine the MMI"*

---

### The "Less Is More" Architecture Rule

**Principle:** The book's authors consistently favor restrictive policies with explicit exception paths over permissive ones with vague guidance.

**Do:**
- Write restrictive policies (e.g., "all code in the monolith") with clear exception paths.
- Make exceptions written, not verbal.
- Use the same exception mechanism consistently.
- Treat each exception as a learning opportunity.

**Don't:**
- Don't write policies that are "guidance-only" when the situation calls for prescription.
- Don't allow verbal-only exceptions; they erode policy.

*Ref: Software Architecture Metrics.md — Calm's monolith-only policy, Stripe's API stability policy*

---

### A Practitioner's Library of Architecture Metric Tools

**Principle:** Build familiarity with a small set of tools rather than a broad but shallow set.

**Do:**
- Master one general-purpose tool (Sonargraph-Architect or SonarQube).
- Master one cycle-detection tool (Sonargraph-Explorer is free for Java/C#/Python).
- Use cloud-native telemetry as your first-pass infrastructure metrics.
- Layer domain-specific tools (ArchUnit for Java, NetArchTest for .NET).

**Don't:**
- Don't adopt every new metric tool that appears.
- Don't neglect tool maintenance; language evolution breaks parsers.

*Ref: Software Architecture Metrics.md — Tools catalog, Table 9-1*

---

### Codifying Architecture Decisions

**Principle:** ADRs (Architecture Decision Records, Michael Nygard) capture decisions in writing; they create accountability and historical context.

**Do:**
- Write ADRs for major architectural changes.
- Include the context, decision, and consequences.
- Make ADRs publicly available within the org.
- Treat them as living documents (updates, not just appends).

**Don't:**
- Don't rely on verbal decisions; they decay.
- Don't let ADRs grow stale; review them annually.

*Ref: Software Architecture Metrics.md — "Discussions and Understanding" (ADRs)*

---

### Operational Visibility Gaps as Architecture Signals

**Principle:** When you can't measure something, you usually can't change it; operational gaps are architectural debt signals.

**Do:**
- Treat "we don't have data on X" as a red flag.
- Add metrics for things you wish you could measure; the cost of measurement is usually less than the cost of blindness.
- Use missing metrics as a focus area in retrospectives.

**Don't:**
- Don't accept "we don't know" as the answer to important questions.
- Don't build new features without first ensuring you can measure their impact.

*Ref: Software Architecture Metrics.md — Case study "Incident #1: Too Many Requests"*

---

### Engineering Strategy as Iteration Over Time

**Principle:** Will Larson (Crafting Engineering Strategy) and Eoin Woods agree that even great strategies go stale; treat strategy as a living artifact.

**Do:**
- Re-read your architecture strategy quarterly.
- Update it as the business evolves.
- Use the DORA four metrics to detect when the strategy needs updating.
- Treat strategy updates as part of the architectural practice, not extra work.

**Don't:**
- Don't write a strategy once and forget it.
- Don't let strategies age without periodic refresh.

*Ref: Software Architecture Metrics.md — Chapter 7 cross-reference; Crafting Engineering Strategy*

---

### The Forgotten Principle — "Slower is Faster"

**Principle:** João Rosa's heuristic: "slower is faster." Time invested in deeply understanding the KPIs and constraints pays off when building the architecture.

**Do:**
- Take time to align on KPIs and hotspot analysis before deciding.
- Use EventStorming to slow down and discover the real process.
- Run multiple workshops if the first one doesn't converge.

**Don't:**
- Don't rush to architectural decisions without shared understanding.
- Don't assume consensus on the problem equals consensus on the diagnosis.

*Ref: Software Architecture Metrics.md — "Increasing Software Architecture Intentionality, Guided by Metrics"*

---

### Reference: Eight Wastes of Lean (in Software Architecture)

**Principle:** Nawras Shkmot's "8 Wastes of Lean" applied to software: defects, overproduction, waiting, non-utilized talent, transportation, inventory, motion, extra-processing.

**Do:**
- Use Lean principles as a lens for architectural decisions.
- Identify which waste is most prominent in your process (waiting for approvals? inventory of unmerged code?).
- Treat "waste" as something to be reduced, not eliminated — some waste is structural.

**Don't:**
- Don't apply Lean mechanically; software has different dynamics than manufacturing.
- Don't chase waste elimination at the cost of clarity or quality.

*Ref: Software Architecture Metrics.md — "Eight types of waste" reference, Figure 6-9*

---

### The Measure-Act Loop in Architecture

**Principle:** Without action, measurement is decoration; build a closed loop where measurement drives action and action is reflected in subsequent measurements.

**Do:**
- For each metric, define the action it triggers.
- Make the action visible (e.g., a Slack notification when a threshold is crossed).
- Track action outcomes as separate metrics.
- Iterate the loop continuously.

**Don't:**
- Don't collect metrics without an associated action.
- Don't rely on humans to notice dashboards; use alerts and nudges.

*Ref: Software Architecture Metrics.md — "Nudges", "Inspection"*

---

### The Lean Measurement Loop — Plan, Do, Check, Act

**Principle:** PDCA applied to measurement: Plan what to measure, Do collect it, Check the results, Act on insights.

**Do:**
- Plan metrics in advance (GQM).
- Collect automatically (CI, telemetry, dashboards).
- Check by reviewing with stakeholders weekly.
- Act by changing architecture, policies, or processes.

**Don't:**
- Don't skip the Plan step; ad-hoc metrics rarely have stakeholders.
- Don't skip the Check step; metrics decay into irrelevance.

*Ref: Software Architecture Metrics.md — General principle; not explicit but consistent throughout*

---

### The Multiplicative Effect of Coupling and Complexity

**Principle:** High coupling AND high complexity multiply pain; each alone is manageable, both together is catastrophe.

**Do:**
- Track coupling (ACD, PC) and complexity (Cyclomatic Complexity, Indentation) separately.
- Set thresholds for each.
- Watch for systems that exceed thresholds on both axes.
- Refactor the most-complex AND most-coupled modules first.

**Don't:**
- Don't optimize one while ignoring the other; they're multiplicative.

*Ref: Software Architecture Metrics.md — Coupling and Complexity Metrics chapters*

---

### The Team Topologies Cross-Reference

**Principle:** Matthew Skelton and Manuel Pais (Team Topologies) define team types (stream-aligned, platform, enabling, complicated-subsystem) that interact with architectural metrics.

**Do:**
- Use stream-aligned teams as the default; align them to value streams.
- Distinguish platform teams (internal services) from product teams.
- Measure cognitive load per team as a leading indicator.
- Pair Conway's Law with team topology decisions.

**Don't:**
- Don't ship microservices without team topology alignment.
- Don't blame architecture for organizational mismatch.

*Ref: Software Architecture Metrics.md — Skelton & Pais citations; Team Topologies reference*

---

### The Team Topologies "Cognitive Load" Measurement

**Principle:** Cognitive load = limit on what a person/team can hold in mind; teams owning software across multiple domains have higher cognitive load.

**Do:**
- Map team ownership against domain boundaries.
- Treat "team owns components in multiple bounded contexts" as a red flag.
- Use Mean Time to Discover as a leading indicator of cognitive overload.
- Restructure teams when cognitive load is too high.

**Don't:**
- Don't measure cognitive load directly; use proxies (mean time to discover, change fail rate).
- Don't assume stable cognitive load over time.

*Ref: Software Architecture Metrics.md — "Implementing a Distributed Big Ball of Mud", Skelton & Pais citation*

---

### The DORA Performance Scale Caveats

**Principle:** The Elite/High/Medium/Low classifications in the DORA report are useful but context-dependent.

**Do:**
- Use the levels as a starting point, not a target.
- Adjust the levels for your context (on-prem vs. cloud, mobile vs. web).
- Watch for trends rather than absolute levels.

**Don't:**
- Don't classify teams with widely different contexts as "the same."
- Don't let DORA levels drive hiring or promotion decisions in isolation.

*Ref: Software Architecture Metrics.md — "Visualization", Figure 1-7 through 1-10*

---

### The Strategy Refinement Checklist

**Principle:** When adopting any strategy, run it through: Is the diagnosis solid? Has the policy been backtested? Have we refined it? Is the operational mechanism in place?

**Do:**
- Use refinement as a checklist item; treat it as a required step.
- Pair refinement with explicit deliverables (a model, a map, or a tested policy).
- Make refinement a team activity, not a one-person show.

**Don't:**
- Don't treat refinement as a luxury; it's the kernel of effective strategy.
- Don't skip refinement because executives want results.

*Ref: Software Architecture Metrics.md — "Refining" (general principle)*

---

### The "Pressure Without a Plan" Antipattern

**Principle:** Many failing strategies sound right but lack concrete details; pressure without a plan = guaranteed failure.

**Do:**
- Refuse to start a strategy without a tested approach.
- Distinguish "this feels right" from "this has been tested."
- Run a strategy testing phase before broad rollout.

**Don't:**
- Don't accept "pressure without a plan" as an excuse for skipping refinement.
- Don't let executive pressure force premature rollout.

*Ref: Software Architecture Metrics.md — Strategy Testing chapter*

---

### The MMI Decision Tree — When to Refactor vs. Replace

**Principle:** Use MMI scores to decide whether to refactor or replace; the cost of replacement rarely justifies itself below MMI 4.

**Do:**
- Refactor when MMI is 4-8; the system is salvageable with effort.
- Replace when MMI < 4; the cost of refactoring exceeds replacement.
- Maintain when MMI > 8; the system is already in good shape.
- Track MMI trajectory, not just snapshots.

**Don't:**
- Don't replace a system with MMI > 4 unless business context demands it.
- Don't assume replacement is cheaper; it rarely is.

*Ref: Software Architecture Metrics.md — "Conclusion" of Chapter 4*

---

## Anti-Patterns & Common Mistakes

- **Vanity metrics without action:** Tracking metrics that no one acts on → *fix:* tie each metric to a decision and an owner.
- **Goodhart's Law violation:** Letting a metric become a target → *fix:* use metrics as guides, not targets; call targets "targets", not "metrics".
- **Big Ball of Mud denial:** Accepting cycle groups because Cassandra has them → *fix:* zero tolerance on package cycles; ≤ 5 elements on component cycles.
- **Diffused ownership of validation:** "DevOps team" owns automation, devs lose feedback → *fix:* restore private builds and local validation.
- **Metric theater:** Impressive dashboards with no decision tie-in → *fix:* make each metric either drive an action or be removed.
- **Strategy without refinement:** Waterfall strategy rollout with no testing phase → *fix:* sponsor + guide + weekly meetings + metrics before broad rollout.
- **Compass without direction:** Apply metrics but no architecture model → *fix:* pair metrics with an explicit, enforceable architectural model.
- **Architectural monotony:** No intentional architecture, just drift → *fix:* diagnose, set KPIs, make architecture decisions intentional.
- **Premature optimization:** Optimizing for scalability before users exist → *fix:* optimize for evolvability (modularity, testability, deployability).
- **Vanity fitness functions:** Many tests, no signal → *fix:* ≤ 5–6 metrics-based rules; sweet spot.
- **Skipping tests for speed:** "We know this is bad, we'll fix later" → *fix:* codify as fitness functions that run on every build.
- **ISO 25010 theater:** Adopting all attributes without focus → *fix:* pick the 3 (+ maintainability) that matter.
- **Comparing teams' DORA scores across contexts:** Penalizes teams with hard domains → *fix:* treat DORA metrics as guides for individual team improvement, not cross-team ranking.
- **Information silos:** One leader communicates strategy verbally → *fix:* two-headed leadership (manager + senior engineer) for context redundancy.
- **Headless Strategy:** Strategy documents without operational mechanisms → *fix:* always pair policy with mechanisms (nudges, inspections, approvals).
- **The "Five Nines" trap:** Demanding 99.999% availability as a number → *fix:* use failure scenarios, not percentages.
- **The Cassandra-is-fine fallacy:** Modeling after systems with massive cycle groups → *fix:* study both positive (Spring) and negative examples.
- **Refactoring without measuring:** "I refactored, so it must be better" → *fix:* track MMI or ML before and after.
- **Coverage-as-quality:** Using test coverage as a quality proxy → *fix:* pair coverage with mutation testing or behavioral coverage.
- **Single-author files ignored:** Files with Number of Authors (365) = 1 → *fix:* flag as knowledge monopolies; pair or document.
- **Manufacturing consent for refinement:** Collecting opinions that support your preferred approach → *fix:* seek real skeptics.
- **The "should we deprecate?" knee-jerk:** Removing APIs to reduce technical debt → *fix:* measure churn impact first (Stripe-style).
- **Spreadsheet-only systems modeling:** Modeling complex dynamics in spreadsheets → *fix:* use `lethain/systems` or similar tools.
- **The "we don't need metrics" stance:** Senior engineers claiming experience replaces measurement → *fix:* pair experience with trends.
- **Production-deployed untested strategies:** Rolling out without a testing phase → *fix:* always run a strategy testing cycle.
- **Architect as bottleneck:** Architect as the only decision-maker → *fix:* document the architecture and let teams decide within it.
- **Architecture reviews as theater:** Recurring reviews with no follow-through → *fix:* track MMI trajectory over reviews.
- **CIO/VP-level dashboards without engineering context:** Dashboards that hide technical reality → *fix:* pair executive dashboards with engineering drill-downs.
- **The "roll our own" metric trap:** Building bespoke metrics when standard ones exist → *fix:* start with DORA + MMI + standard coupling metrics.
- **Cross-team policy without local mechanisms:** Org-wide policy that teams don't know how to apply → *fix:* pair policy with team-level operational mechanisms.
- **Manual-only quality gates:** Quality gates that require humans to remember → *fix:* automate via fitness functions in CI.

## Decision Heuristics / Checklists

- **When you don't know where to start measuring:** Run GQM with 2-5 stakeholders; force one explicit goal before any metric.
- **When choosing metrics-based rules:** Sweet spot is 5-6 rules; more = diminishing returns.
- **When a cycle group is large but stable:** Investigate SDI; you may be able to fix cheaply.
- **When selecting between DORA classification schemes:** Pick a context-relevant scheme (mobile vs. web, on-prem vs. cloud).
- **When deciding whether to refactor or replace:** Use MMI threshold of 4 (replace) vs. 8 (stay course).
- **When on a tight cycle time budget:** Reduce cycle group size to ≤ 5 first; it's the highest-leverage cycle-group metric.
- **When the team's Mean Time to Discover increases:** Combine with change fail rate to find weak architecture spots.
- **When picking a fitness function framework:** ArchUnit for Java/compile-time; hand-rolled for distributed systems; Scientist for runtime fidelity.
- **When auditing organization for missing strategies:** Look for the absence as part of diagnosis, not as a blocker.
- **When two leaders disagree on strategy:** Use a KPI Value Tree to make disagreement precise.
- **When your test coverage metric looks suspicious:** Distinguish happy-path tests from meaningful behavioral tests; coverage alone is meaningless.
- **When you're inheriting a messy codebase:** Run architecture review first, get MMI baseline, then prioritize refactoring by structural impact.
- **When picking a metric tool:** Evaluate build-threshold integration before depth of metrics.
- **When a metric value is suspicious:** Check whether data collection has gaps; the metric is only as good as its inputs.
- **When strategy failure is rapid:** Usually a diagnosis problem — re-do diagnosis before re-doing policy.
- **When the org wants more metrics:** Pause; fewer metrics with action are better than more metrics without.
- **When picking between event-based and continuous fitness functions:** Use ISO 25010 quality attributes to map; cycle through categories to balance.
- **When designing a fitness function for a new system:** Start at the bottom layer (triggered atomic); build up.
- **When measuring technical debt for an executive audience:** Use MMI; pair with cycle-group size for a one-slide story.
- **When a fitness function fails repeatedly:** Suspect the implementation before the policy; refine the test before abandoning the rule.
- **When your architecture strategy is stale:** Refresh KPIs first; policy often follows naturally.
- **When rolling out new fitness functions:** Pair with documentation; pair documentation with training; pair training with runbooks.
- **When choosing between metrics and observation:** Use observation first; metrics should confirm what you already suspect.
- **When a strategy test reveals failure:** Don't double down; pause the strategy and write a new one.
- **When you're the only one who understands the strategy:** Document it; the strategy is institutional, not personal.
- **When the cycle-group metric goes up:** Treat it as urgent; small changes now save big rewrites later.
- **When you see inconsistent deployment frequency across teams:** Check whether scope is consistent before drawing conclusions.
- **When a fitness function has high false-positive rate:** Reduce its priority; don't disable it silently.
- **When metrics contradict each other:** The contradiction is a feature; dig into the divergence.
- **When leadership asks for "one number":** Resist; the four DORA metrics work as a set.

## Key Takeaways

1. **Measure architecture to make decisions, not to make dashboards.** Metrics are guides; goals are targets.
2. **Use the four DORA metrics + their instrumentation points as your baseline**, then layer structural, runtime, and sociotechnical metrics on top.
3. **Fitness functions are the bridge from metrics to engineering** — automate them, wire them into CI, treat them as a checklist of important-not-urgent principles.
4. **The MMI score quantifies technical debt** — use it to decide refactor vs. replace.
5. **Cycle groups are the most damaging structural metric** — zero tolerance on packages, ≤ 5 elements on components.
6. **ML, ACD, PC, and SDI** are the complementary coupling/complexity metrics that complete the structural picture.
7. **GQM is the go-to method for gnarly, hard-to-measure problems** — workshop it, not workshop-around it.
8. **Private builds + metrics restore local validation** when DevOps culture hasn't landed.
9. **Sociotechnical architecture matters as much as technical architecture** — Conway's Law makes it inevitable.
10. **Conway's Law + KPI Value Tree + EventStorming** are the practical tools for connecting software architecture to business outcomes.
11. **The fitness function testing pyramid** mirrors the testing pyramid and creates a balanced metric portfolio.
12. **GQM's four instrumentation points (commit, deploy, failure detected, failure resolved)** are the minimal data to derive all four DORA metrics.
13. **Testability and deployability** are the two tools for evolutionary architecture — design for both.
14. **The DORA four metrics work as a pair**: deployment frequency + lead time = throughput; change failure rate + time to restore = stability.
15. **Maintaining architecture hygiene (cycles, coupling, complexity) is the highest-leverage structural investment**; tooling pays for itself.

## Cross-References

- Related: [[../Team_Topologies.md]]
- Related: [[../Building_Evolutionary_Architectures.md]]
- Related: [[../Software_Architecture_Patterns.md]]
- Related: [[../Modern_Software_Engineering.md]]
- Topic index: [[../INDEX.md]]
