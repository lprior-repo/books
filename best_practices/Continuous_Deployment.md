# Continuous Deployment — Enable Faster Feedback, Safer Releases, and More Reliable Software
**Author:** Valentina Servile (Foreword by David Farley) (O'Reilly, 2024)
**Topic tags:** `#architecture` `#general`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Continuous_Deployment/Continuous_Deployment.md` · `summaries/Continuous_Deployment.md`

## TL;DR
Continuous deployment is the natural endpoint of continuous delivery: remove the final manual gate so every commit passing all automated quality checks goes to production automatically. The implementation is a one-line change; the implications are profound — feature toggles, the expand-and-contract pattern, trunk-based development, vertical slicing, separate DB-migration deployments, and testing in production become *prerequisites* rather than optional. The DORA throughput metrics (deploy frequency, lead time) and stability metrics (change-failure rate, MTTR) are the targets; culture change is the hardest part.

---

## Best Practices by Topic

### Definitions and the Historical Lineage

**Principle:** Continuous deployment is to continuous delivery what "all green" is to "mostly green." Remove the last manual approval step. Each successful commit becomes a production release automatically.

```
XP ("if it hurts, do it more often", 1990s)
  → DevOps (joined dev + ops, 2000s)
  → Continuous Integration (CI, automated build+test on every commit)
  → Continuous Delivery (CD: pipeline + preprod, manual gate)
  → Continuous Deployment (no manual gate — every commit to prod)
```

**Crucial distinction (the book's cornerstone):**
- **Deployment** = the technical act of putting new code on servers.
- **Release** = the business event of exposing new behavior to users.

Under continuous deployment, most deployments are *not* releases — the code is hidden under feature toggles. Conversely, a release (turning a toggle on) does not require a deployment. This separation is what makes CD safe.

**Do:**
- Treat the deployment pipeline as an *outcome contract*: "if the pipeline says deployable, deployable is true," with **no further sign-offs, integration tests, or human checks**.
- Aim for one commit = one production deploy. Track **continuous flow ratio** = `production deploys ÷ total commits`. Anything less than ≈1.0 signals a batching bottleneck (long branches, manual reviews, red builds, paused pipelines).

**Don't:**
- Don't call "continuous deployment to UAT" continuous deployment. It is continuous delivery.
- Don't conflate deploying (engineering) with releasing (product). Split them.

*Ref: Chapter 1 — "Continuous Deployment"; the continuous flow ratio*

---

### DORA Metrics — Both Throughput AND Stability, Not One or the Other

**Throughput:**
- **Deployment Frequency** — elite teams: on demand, multiple/day.
- **Lead Time for Changes** — commit → production; CD dramatically compresses this.

**Stability:**
- **Change Failure Rate** — % of deploys causing failures; smaller changes ⇒ fewer failures.
- **Mean Time to Recover (MTTR)** — restore service after a failure; frequent deploys ⇒ easy rollback/fix-forward.

> High-performing organizations [were] consistently twice as likely to exceed goals in profitability, market share, and productivity as low performers.

**Do:**
- Optimize all four DORA metrics together — research consistently shows they correlate positively (the "no trade-off" finding).
- Use the DORA metrics as a *telemetry* of your engineering practice, not a scoreboard.

**Don't:**
- Don't optimize lead time at the expense of stability; the research says you actually get both.
- Don't treat the DORA metrics as a report — treat them as SLOs with error budgets.

*Ref: Chapter 2 "Benefits" — DORA Metrics section; the State of DevOps Report 2023*

---

### One-Piece Flow — Lean Applied to Software

**Principle:** Lean manufacturing's "one-piece flow" applies 1:1 to software commits. One commit = one unit of inventory. Aim for "one commit = one production deployment." Queue theory (the *Batch Size Queueing Principle*, Donald G. Reinertsen) tells us cycle time and variability fall as batches shrink — and that the transaction cost must drop first.

**The Lean chain:**
```
Lower transaction cost (automation)  →  Smaller batches  →  Shorter queues
                                                        →  Shorter cycle time
                                                        →  Just-in-time delivery
```

> Toyota's SMED reduced die-changeover from 24 hours to <10 minutes — two orders of magnitude — and unlocked small batches. The analogous moves in CD are investing in build, test, and deploy *automation* so each commit can flow independently.

**Inventory in software is invisible** — features in the backlog, code in branches, designs in tools, features behind OFF toggles. Treat them all as WIP. The less WIP, the faster the feedback.

**Do:**
- Measure and trim WIP at every step (backlog → branch → review → preprod → flag).
- Reduce *transaction cost* (slow manual review, slow CI) before expecting smaller batches to help.
- Hold the line when someone suggests batching for "efficiency" — batch size is *not* economy of scale in software flow.

**Don't:**
- Don't reward teams for "filling the release train." Empty pipelines are the goal.
- Don't treat code in feature branches or behind feature flags as "free" — it's inventory.

*Ref: Chapter 2 — "Origins of Lean Manufacturing"; "Batches in software"; Toyota Production System refs*

---

### Trunk-Based Development (TBD)

**Principle:** Developers merge their work into a shared trunk **at least daily**, ideally multiple times per day, so the integration pain is removed from the value stream.

**Do:**
- Pull from trunk at the start of the day; push small changes throughout the day; never let a branch live more than 24 hours.
- Pair programming or short PRs at the trunk — whichever produces faster feedback.
- Use **merge queues** + **squash-merge** (Maze, TravelPerk examples) to keep trunk green even with concurrent pushes.

**Don't:**
- Don't use long-lived feature branches. They are exactly the batch-and-queue that CD rejects.
- Don't merge trunk to a 4-day-old feature branch without rebasing first — re-integration pain grows with age.

*Ref: Chapter 4 "Prerequisites"; Case Studies — ClimatePartner (direct pushes to main; pair-programming reviews); REA; Maze; TravelPerk*

---

### Feature Toggles vs. Expand-and-Contract — Two Tools, Two Sweet Spots

**Principle:** Feature toggles and the expand-and-contract pattern are the two ways to "hide work in progress" — but they differ on overhead and speed of release/revert.

**Feature Toggle Service / Runtime Pattern:**
- Best for *new features*, especially when product experimentation, progressive rollout, or rapid revert is needed.
- Fast (runtime) flip; slow on the lifecycle (must track active % rollouts, configuration, retirement).
- Frameworks: Unleash, LaunchDarkly, Flagsmith; or in-app `isFeatureEnabled(...)` stubs.

**Expand-and-Contract (parallel change):**
- Three phases: **Expand** (add the new alongside the old) → **Migrate** (switch callers) → **Contract** (remove the old).
- Best for *refactors* of live functionality, where the change spans multiple layers (DB, API, UI).
- Lifecycle is in code only — no toggle to manage.

**Heuristic from the book:**
| | Release/Revert speed | Overhead | New feature | Refactor |
|---|---|---|---|---|
| Feature flag | Very fast (runtime) | High (state, config, lifecycle) | **Use by default** | Risky refactors / cross-cutting CFRs |
| Expand-and-contract | Slow (needs pipeline) | Low (in code only) | When no experimentation needed | **Default choice** |

**Do:**
- Place toggle evaluation in the *outermost* layer only — minimize conditional checks.
- Combine toggles with **per-request override** (cookie/header) so devs can test in production without a config change.
- Build the toggle framework in **iteration 0** — same as CI was a decade ago.

**Don't:**
- Don't gate refactors through feature flags by default; the overhead is rarely worth it.
- Don't accumulate WIP under a long-lived toggle — release it (or remove it) on a defined cadence.
- Don't make the toggle a global network call — pre-fetch state at startup or bundle into config for performance-sensitive paths.

*Ref: Chapter 3 "The Mindset Shift"; Feature toggles vs. expand-and-contract table (Table 3-1)*

---

### Backward Compatibility Is a N × (N − 1) Contract

**Principle:** When N independent services are deploying continuously and independently, every change to a contract must be **backward-compatible with version N − 1 of every other system**.

**Why this is unavoidable:** "Many more permutations of distributed units than stages in a CD pipeline."

**Hyrum's Law is the deeper constraint:**
> With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody.

**Do:**
- Use the **expand → migrate → contract** pattern for *every* contract change (API schema, message format, DB column).
- Adopt **consumer-driven contract (CDC) tests** with tools like **Pact** between services owned by different teams (OTTO's case study).
- Treat *informal* contracts (intra-service, e.g., backend–frontend, backend–DB schema) with the same care; they exist whenever separate executables communicate.

**Don't:**
- Don't deploy a breaking schema or API change expecting "we'll coordinate."
- Don't skip contract testing in monorepos either — there's always a process boundary somewhere (the DB, the message queue, the browser).

*Ref: Chapter 3 "Distributed Systems"; expand-and-contract pattern; Pact/CDC (OTTO, REA case studies)*

---

### Database Migrations — Deploy Schema and Code Separately

**Principle:** Schema and application code should *never* be deployed in the same commit. Rolling updates mean some instances run old code, some new code, against the same database — incompatible changes break the contract for everyone.

**Three common failure modes (Chapter 10):**

1. **Simultaneous rename in code + schema migration** — old instances crash against the new column name during rolling deploy.
2. **Expand and read but don't sync** — data written between expand and migrate is missing from the new column.
3. **Race conditions on multi-instance deploys** — old and new instances writing the same row in different schemas simultaneously.

**Three solutions (parallel-change for data):**

**Solution 1: Temporary Database Trigger**
- Sync old and new columns during transition; pros: simple; cons: logic in SQL is harder to test.

**Solution 2: Double-Write**
```text
1. Expand: ADD COLUMN new_id (nullable)
2. Double-write: code writes to BOTH old_id AND new_id
3. Backfill: migration copies old_id → new_id for existing rows
4. Switch reads: read from new_id only
5. Contract: DROP COLUMN old_id
```

**Solution 3: Double-Read**
```text
1. Expand: ADD COLUMN new_id (nullable)
2. Double-read: code reads new_id first, falls back to old_id
3. Switch writes: write to new_id only
4. Backfill: catch up any rows still missing
5. Contract: DROP COLUMN old_id
```

**NoSQL Considerations:** Same principles, harder mechanics. Options:
- *Migrate on read forever* — keep backward compat in code indefinitely.
- *Migrate on read with eventual cleanup* — convert on read, retire compat later.
- *Custom batch update* — background job for bulk conversion.

**Do:**
- **Always** deploy schema changes and code changes in separate commits (and ideally separate pipelines).
- Use a backward-compatible pattern (double-read, double-write, trigger, or `ChangeDataCapture`).
- Treat schema deploys as forward-only until the contract step — even if you plan to drop a column "soon."
- Write a backfill or migration script that's idempotent and pauseable.

**Don't:**
- Don't combine schema and application code in a single commit. Period.
- Don't delete data or columns before all readers have stopped using them.
- Don't assume no-write periods exist; assume traffic is continuous.

*Ref: Chapter 10 "Data and Data Loss"*

---

### Zero-Downtime Deployments — Blue/Green vs. Rolling vs. Canary

| Strategy | How it works | Pros | Cons | When to pick |
|---|---|---|---|---|
| **Blue/Green** | Two identical fleets (`blue`, `green`); deploy new to inactive; flip traffic; old stays running for instant rollback | Fast rollback, isolation | 2x infra cost, N/(N−1) compat issue across versions | When blast radius must be minimal or you want ops holdback |
| **Rolling** | Replace instances in-place, in waves | Single fleet; container-orchestration-native | N/(N−1) compatibility window; uneven versions during rollout | Container clusters (ECS, Kubernetes) — default pick |
| **Canary** | Deploy new to a subset, route traffic to it, compare metrics; promote on success | Real-traffic validation | Slow, statistical noise, complex to set up well | Large enterprises needing auto-validated rollouts |

**All three share the *N/(N − 1)* compatibility problem:** during the rollout, both versions coexist and must remain compatible.

**Do:**
- **Always** keep version `N` backward-compatible with `N − 1` (and `N + 1`!) for the duration of the rollout.
- Pick the simplest strategy that meets your safety bar. Don't deploy canary until you need it; rolling + good tests + toggles is enough for most teams.
- Use health checks and smoke tests as the floor of automated validation.

**Don't:**
- Don't use partial deployments to "QA" the next version. Replace manual steps with smoke tests + automated checks.
- Don't use partial deployments as an A/B testing tool — feature flags give finer-grained control.
- Don't pay for blue/green if rolling is sufficient; don't skip canary if it's insufficient.

*Ref: Chapter 4 — "Zero-Downtime Deployments"; anti-pattern examples "Blue/green as a QA tool", "Partial deployments as a canary release tool"*

---

### Slicing Work — Vertical vs. Horizontal

**Principle:** Slice the work the way users consume it (a thin slice through all layers), not the way the org chart is structured (a thick layer across one slice). Vertical slices are independently deployable; horizontal slices are not.

**MVP + INVEST for user stories:**
- **I**ndependent — can ship alone.
- **N**egotiable — details adjustable.
- **V**aluable — delivers user- or business value.
- **E**stimable — fit within a commit cycle.
- **S**mall — fits one commit (or one story in one slice).
- **T**estable — has clear acceptance.

**Do:**
- Write user stories as **thin end-to-end slices** — one table + one API + one UI element per story.
- Use the user story template to plan cross-functional requirements (CFRs):
  ```
  As a <user> I want to <action> so that <outcome>
  Given <precondition> When <action> Then <outcome>

  Deployability: <feature toggle / expand-and-contract / other?>
  Testability:  <notes on automated tests, manual testing in prod>
  Observability: <notes on logs, metrics, dashboards, alerts>
  Security:     <new inputs, data, dependencies, infra>
  Performance:  <network requests, data size, persistence>
  ```
- Hold the line on horizontal slicing even when the architecture "supports" it — horizontal slices produce large batches that CD forbids.

**Don't:**
- Don't accept "the database team is building the schema, the backend team the API, the frontend team the UI" as a delivery model. Cross-functional teams own vertical slices.

*Ref: Chapter 6 "Slicing Upcoming Work"; enhanced user story template (cross-functional requirements, CFRs)*

---

### Cross-Functional Requirements per Story

**The five categories every change must explicitly address:**
- **Deployability** — feature toggle, expand-and-contract, branch, or unhidden?
- **Testability** — what automated tests; what manual exploration in prod?
- **Observability** — new logs/metrics/dashboards/alerts?
- **Security** — new inputs, data, dependencies, infrastructure?
- **Performance** — new network requests, data size changes, persistence impact?

**Do:**
- Treat CFRs as **part of the acceptance criteria**, not a separate review.
- Estimate CFRs alongside functional work (they take time too).
- Audit CFR coverage in retrospectives — missing telemetry is a recurring root cause of incidents.

**Don't:**
- Don't defer CFRs to a "reliability sprint" — by then the change is in production with no plan.

*Ref: Chapter 7 "Building for Production"*

---

### Testing in Production (the Real Production, Not a Staging Double)

**Principle:** Pre-production environments are approximations. Production is the only environment with real data volume, real request patterns, real third-party APIs, and real user behavior. The cost of maintaining staging often outweighs the safety it provides.

**Feature Toggle Activation Strategies:**
- *Internal users only* — toggle ON for employees.
- *Specific user IDs* — whitelist test accounts.
- *Percentage rollout* — 1% → 5% → 25% → 100%.
- *By country / device / segment* — targeted cohorts.
- *By user tier / subscription* — restrained.

**Do:**
- Run the same telemetry pipeline in pre-prod as in prod; only the *traffic* differs.
- Treat *test data* as production data: tag it programmatically; isolate it; never confuse a test order with a real order.
- Use **shadow traffic** / replay tools where available to give pre-prod realistic load.
- Drive investigations with the *same* dashboards in any environment.

**Don't:**
- Don't keep a dedicated staging environment as a forced step if your tests and toggles let you test in production safely.
- Don't run "manual QA in production" without a feature-flag-driven strategy — random manual testing is neither reproducible nor safe.

*Ref: Chapter 11 "Testing in Production"; life after staging — REA, ClimatePartner, AutoScout24*

---

### Coordinating Toggles in Distributed Systems

**Principle:** When one logical feature spans multiple services, *avoid* per-service toggle divergence. Two valid models:

- **Centralized feature-flag service** (single source of truth; both services evaluate the same flag).
- **Toggle propagation through the call chain** (provider passes flag context down; consumers honor it).

**Do:**
- Use the same toggle platform across all services contributing to a release.
- Treat per-service toggle state as a coupling risk — they invite inconsistencies and roll-back nightmares.

**Don't:**
- Don't let a release be half-on. Half-on systems produce confusing user-facing incidents.

*Ref: Chapter 12 "Releasing" — Coordinating feature flag releases in distributed systems*

---

### Canary Releases vs. Canary Deployments

> Canary *deployment* = routing new version's traffic to a subset of instances.
> Canary *release* = gradually exposing a feature flag to a growing subset of users (the release side).

The deployment-side canary gives you *technical* validation (error rate, latency). The release-side canary gives you *user* validation (engagement, conversion).

**A/B testing** is a release-side activity: split traffic, measure outcome, choose. It is *product-driven* — needs analytics, statistical rigor, clear hypothesis, success metrics.

**Do:**
- Use release-side canary via feature flags for product-driven questions ("does this improve conversion?").
- Use deployment-side canary for technical questions ("does this code crash on edge cases?").
- Measure statistical significance before "deciding" — premature readouts mislead.

**Don't:**
- Don't conflate canary release with canary deployment; the engineering mechanism differs entirely.
- Don't run "experiments" without a hypothesis or a stop condition.

*Ref: Chapter 12 "Releasing"; A/B test types — simple A/B, multivariate, fractional factorial*

---

### The Prerequisites — "You Must Be This Tall"

**You can't skip these:**
- Cross-functional, autonomous teams (fast decisions, integration autonomy).
- Frequent integration (trunk-based development).
- Frequent code review (PRs / pair).
- Automated code analysis (linting, static analysis, security scanning).
- Strong test automation (unit, integration, e2e, contract).
- Zero-downtime deployments (blue/green, rolling, canary).
- **Observability** (logs, metrics, alerts, dashboards, SLOs).
- Stakeholder trust — built gradually, ideally via a stretch on continuous delivery first.

**Do:**
- Earn trust by demonstrating strong automated quality gates and a culture of accountability.
- Start on continuous delivery; remove the manual gate once the pipeline has earned it.
- Treat each prerequisite as a separate workstream with its own owner and measurable progress.

**Don't:**
- Don't flip the switch to CD without prerequisites in place. The team's trust will break and you'll never get it back.
- Don't skip observability — it's the only way you'll know whether your changes were actually safe.

*Ref: Chapter 4 "You Must Be This Tall (Prerequisites)"*

---

### Adopting CD Where Manual Gates Can't Be Removed (Regulated Industries)

**Reframe the constraint.** N26 (digital bank) and Motability Operations (UK regulated) both practice CD by isolating the regulated components and *finding leaner ways to satisfy compliance* — separate pipelines for services with regulatory approvals, compliance team embedded with engineering.

**Do:**
- Treat the manual gate as a *coupling point*, not a *safety net*. Move it from pre-prod-deployment to a specific, isolated set of riskier components.
- Pair with compliance early; co-design pipelines.

**Don't:**
- Don't refuse CD because some component requires a manual approval; do CD for everything else, isolate the rest.

*Ref: Case Studies — N26, Motability Operations*

---

### Cognitive Load Considerations

The book is honest: CD *raises* cognitive load on engineers. Mitigations:
- Don't let the pipeline become a busy-body — too many quality gates slow commits without proportional safety.
- Don't let "deploy to production" become so routine that nobody pays attention. Set friction (e.g., a one-line commit-message convention, deploy dashboards).
- Train broadly — many humans need many skills (security, perf, ops).
- Onboard to the full stack, not a slice — a developer who understands the whole pipeline doesn't accidentally break it.

**Do:**
- Schedule deep work away from peak deploy windows to reduce conflict.
- Run a "deploy dashboard" so engineers see the impact of their changes in aggregate.

**Don't:**
- Don't accept "the pipeline is too noisy to read" as steady state. Audit gates quarterly.

*Ref: Chapter 5 "Challenges" — Cognitive Load*

---

### Cultural Change — the Hardest Part

Every case-study company reports the same lesson: organizational barriers (distrust, separate QA, manual approvals) were harder than technical ones.

**Do:**
- Embed QA engineers into product teams (OTTO's inflection point: 60+ deploys/day, up from monthly).
- Institute blameless retrospectives and incident reviews.
- Build cross-functional understanding by rotation, shared on-call, and pair investigations.
- Make the deployment dashboard visible to the entire team, not just ops.

**Don't:**
- Don't leave QA as a downstream gate; it becomes a bottleneck and a handoff.
- Don't add a manual "approval" step because one executive doesn't trust the pipeline; address the trust deficit directly.

*Ref: Case Studies — OTTO (QA integration); AutoScout24 ("you build it, you run it"); N26 (compliance + eng co-design)*

---

### Heuristics from Real-World Case Studies

- **OTTO** — integrating QA into dev teams was the pivotal cultural change. Plus consumer-driven contracts via Pact, trunk-based dev, feature toggles.
- **AutoScout24** — 200+ devs, 1,000+ services, 1,500+ pipelines. Trunk-based, blue/green, Kubernetes rolling updates with 0% unavailability. Datadog for observability. *You build it, you run it.* New joiners deploy in week one.
- **N26** — regulated bank, still practices CD on isolated, lean components. Compliance team works with engineering.
- **ClimatePartner** — direct pushes to main, no PRs; pair programming for review; no staging; test accounts programmatically tagged.
- **Motability Operations** — Jenkins + ArgoCD GitOps on OpenShift/Kubernetes/AWS. SonarQube, Snyk, blue/green, LaunchDarkly flags. Pipeline triggered 5-25 times per user story. Risk department came to see CD as *risk mitigation*.
- **REA Group** — 80%+ of fleet continuously deployed. Created Pact for consumer-driven contracts. Many teams eliminated staging.
- **Maze** — moved from Gitflow to trunk-based, then to fully automated CD with GitHub Actions. Merge queue, squash-merge, monorepo with programmatic change detection.
- **TravelPerk** — 1,200 employees, 350+ builders. Adopted CD from startup days. Merge queue with scheduled merges every 20 min for the monolith. 1,000+ monitors for errors, slow endpoints, queue congestion, DB resources.

*Ref: Part V — Case Studies*

---

## Anti-Patterns & Common Mistakes

- **Manual deployment as a release gate.** — *fix:* feature flags + automated tests replace the gate.
- **Long-lived feature branches.** — *fix:* trunk-based, merge at least daily.
- **Simultaneous schema + code deploys.** — *fix:* one commit = schema OR code, never both. Backward-compatible patterns.
- **DRY that couples independently deployed services.** — *fix:* DRY within a deployment pipeline; tolerate duplication across pipelines.
- **Pipelines with too many gates to read.** — *fix:* audit gates; each must earn its place.
- **Per-service feature flags that drift.** — *fix:* centralized flag service OR propagated context.
- **Blue/green used as a manual QA tool.** — *fix:* automated smoke tests + canary or feature flags.
- **Partial deployment used for A/B testing.** — *fix:* feature flags for finer-grained, more reliable controlled rollouts.
- **Skip observability because "we have monitoring."** — *fix:* wide-event telemetry, RED/USE/golden signals, SLOs with budgets.
- **Try to write unit tests for LLMs.** — *fix:* eval-based development with high-quality golden datasets.

## Decision Heuristics / Checklists

- **Should we deploy yet?** CI green + commit-stage green + acceptance green + observability green + SLO budget intact + no active incident + DTO of impact understood.
- **Which deployment strategy?** Default to rolling on container platforms. Step up to canary when traffic is too big to absorb an incident. Step up to blue/green if you need a hard rollback step.
- **One deploy or many?** Per-change. Smaller = safer.
- **One schema migration or paired?** Always separate; always backward-compatible.
- **When to add a feature flag?** When (a) you need runtime control, (b) the feature is risky to release, or (c) you'll iterate based on user response.
- **When to use expand-and-contract?** When refactoring live functionality across multiple layers and you want low-overhead parallel change.
- **Should we test in production?** Yes — with feature flags as guard rails.
- **Should we multi-region?** Only when the business impact of regional outages exceeds the cost of maintaining DR.
- **When to break a manual gate?** When the pipeline has demonstrated for a sustained period that its gate cannot catch what the manual one does.
- **Continuous flow ratio target:** ≥ 0.9 for shipping teams (production deploys ≈ number of commits).

## Key Takeaways

1. **CD is a one-line change with profound implications.** The implications — feature toggles, expand-and-contract, vertical slicing, backward-compatible DB migrations, observability, cultural change — are the work.
2. **Deployment ≠ release.** Decouple them via feature flags.
3. **One commit = one production deploy.** Track the continuous flow ratio.
4. **Backward-compatible everything:** N/(N − 1) compat during rollouts; expand → migrate → contract on every contract change.
5. **Schema changes deploy separately from code.** Double-read or double-write for transitions.
6. **Vertical slicing is essential.** Horizontal slicing makes CD impossible.
7. **CFRs are part of the story.** Plan deployability, observability, security, testability, performance alongside function.
8. **Trust is earned through demonstrated pipeline reliability.** Stakeholder buy-in is the outcome.
9. **DB schema and code deploys are different beasts.** Each change needs its own pipeline.
10. **Observability is non-negotiable.** Wide events + golden signals + SLOs + error budgets.
11. **LLM systems need evals + telemetry working together** — neither alone.
12. **Cultural change is the hardest part.** Embed QA, embrace "you build it you run it," use blameless retros.

## Cross-References
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] (AWS-side deployment safety patterns: blue/green via Route 53 failover, RDS Proxy, canary via FIS)
- Related: [[../Observability_Engineering.md]] (CD needs observability — observability is the feedback loop CD promises)
- Related: [[../Modern_Software_Engineering.md]] (continuous delivery as Farley defines it; the BAPO/OBAP org models that make CD viable)
- Topic index: [[../INDEX.md]]
