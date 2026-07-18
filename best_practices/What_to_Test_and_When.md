# What to Test, and When?
**Author:** Dave Farley (Continuous Delivery Ltd.)
**Topic tags:** `#testing` `#process` `#continuous-delivery` `#deployment-pipeline` `#observability`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/How To - What to Test and When 22-07-21/How To - What to Test and When 22-07-21.md` · `summaries/How_To_What_to_Test_and_When.md`

## TL;DR
A four-phase testing framework (Commit → Acceptance → Release → Production) for placing each testing technique at the point in the deployment pipeline where it is fastest, cheapest, and most informative. Commit is FAIL FAST, Acceptance defines RELEASABLE, Release SUPPORTS RELEASE, Production INFORMS PRODUCT DESIGN. Apply when designing or auditing a testing strategy inside a CD pipeline.

---

## Best Practices by Topic

### The Four-Phase Testing Framework

**Principle:** Testing is a continuous feedback mechanism spanning the entire delivery lifecycle, not a single gate before release. Each phase has a distinct goal, speed budget, and set of techniques.

| Phase | Goal | Speed budget | Trigger | What runs there |
|-------|------|--------------|---------|-----------------|
| **At Commit** | FAIL FAST | seconds → minutes | every commit | Unit tests, coding standards, static analysis, asserted common-error detection, data-migration unit tests |
| **Acceptance** | RELEASABLE | minutes → tens of minutes | commit-stage pass | BDD-style acceptance tests, deployment tests, configuration tests, security tests, data-migration tests, performance, scalability, resilience, compliance |
| **At Release** | SUPPORTS RELEASE | minutes | deployment | Smoke tests, health checks, canary release testing, monitoring, exception tracking |
| **In Production** | INFORMS PRODUCT DESIGN | continuous | always on | Capacity monitoring, technical monitoring, performance verification, security verification, A/B testing, business experiments, commercial performance |

**Do:**
- Tag every test you write with the phase it belongs to — its goal, scope, and speed dictate which phase.
- Build the Commit stage first. It is the foundation; nothing else works reliably without it.
- Choose the earliest phase that can give meaningful feedback for each technique.

**Don't:**
- Treat testing as a single phase owned by QA at the end.
- Defer a fast, valuable test to a later stage to "be consistent."
- Force a slow, expensive test into the Commit stage and slow everyone's feedback loop.
- Stop testing at release. The most valuable learning happens in production.

*Ref: How To - What to Test and When 22-07-21.md — "Commit / Acceptance / Release / Production"*

---

### Commit Stage — FAIL FAST

**Principle:** The Commit stage is the developer's safety net and the tightest feedback loop in the pipeline. Speed is paramount.

**Do:**
- Run the entire Commit stage in **under five minutes**; the unit-test subset in **under two minutes**.
- Write unit tests that are fast (ms), isolated (no DB / FS / network), repeatable, self-checking, timely (written with the code, ideally test-first via TDD).
- Replace external dependencies with test doubles (mocks, stubs, fakes) so unit tests stay isolated.
- Wire lint, formatter, and static-analysis tools into both the build and the IDE for immediate feedback.
- Add static analysis (SonarQube, Coverity, Clippy, PyLint) to catch structural/security issues tests miss.
- Add asserted common-error detection (null deref, buffer overflow, integer overflow, resource leaks); use fuzz testing at this stage for random-input crash discovery.
- Write **data-migration unit tests** covering: script runs without error, data transforms correctly, migration is idempotent, rollback works.
- Run the Commit suite locally in seconds so developers actually run it after every small change.

**Don't:**
- Allow DB, network, or filesystem I/O into the Commit suite.
- Let the Commit suite grow past five minutes — developers will stop running it locally and the loop dies.
- Skip migration tests; migration failures are among the most common causes of production incidents.

*Ref: How To - What to Test and When 22-07-21.md — "At Commit – Development-supporting tests"*

---

### Acceptance Stage — Define RELEASABLE

**Principle:** The Acceptance stage answers "is this software releasable?" — covering functional correctness plus every non-functional bar (performance, security, resilience, compliance, deployability).

**Do:**
- Write acceptance tests as **BDD-style executable specifications** in the business domain language (Given/When/Then or equivalent). They serve as living documentation validated by the CI system.
- Exercise the SUT through its **public interfaces only** — APIs, UIs, message queues. No back doors for tests.
- Use a **production-like environment** (same deploy tooling, same config regime) so acceptance can detect deployment-, config-, and environment-related defects.
- Add **deployment tests** that verify the install path, config load, service startup, health, and reachability.
- Add **configuration tests** that verify required config is present, well-formed, and within range. Treat config as code: version-control it, test it, ship it through the same pipeline.
- Add **security tests**: dependency scanning, SAST/DAST, authn/authz verification, injection checks (SQLi, XSS, CSRF).
- Add **performance tests** with quantified acceptance criteria (e.g., "95% of requests < 200ms at 1000 rps").
- Add **scalability tests** for horizontal, vertical, and extreme-load behavior.
- Add **resilience tests** that simulate dependency failures and verify graceful degradation (bridges to Chaos Engineering in Production).
- Add **compliance tests** for regulatory requirements (GDPR, HIPAA, PCI-DSS, SOX): encryption, access control, audit logging, retention.
- Add **data-migration integration tests** against realistic data volumes/schemas — the unit tests are not enough.
- Keep acceptance tests reasonably fast — feedback in tens of minutes, not hours.

**Don't:**
- Treat the Acceptance stage as only functional testing. Non-functionals often determine releasability more than correctness.
- Build a separate "staging" environment that tries to fake production; ship the same artifacts the same way.
- Couple acceptance tests to internal implementation — they must survive refactors.
- Allow acceptance tests to grow without bound; maintain the test pyramid (many unit, fewer integration, fewest e2e).

*Ref: How To - What to Test and When 22-07-21.md — "Acceptance – Defining Releasability"*

---

### Release Stage — SUPPORT RELEASE

**Principle:** Release-stage checks are not about finding bugs (earlier stages should have caught them). They verify that the release process itself is sound and that the software behaves as expected in production.

**Do:**
- Run **smoke tests / health checks** immediately post-deploy: app starts, key APIs respond, DB reachable, auth works, critical user journeys complete.
- Use **canary releases** — deploy the new version to a small subset, route a small slice of traffic, compare key metrics vs baseline, auto-rollback on regression.
- Monitor a **small, high-signal metric set** during release: error rate, p99 latency, request rate. Tooling: Spinnaker, Flagger, Argo Rollouts.
- Wire **exception tracking** (Sentry, Rollbar, Bugsnag) into the release process so a new-error spike triggers alert + auto-rollback.
- Choose rollback metrics that are **high-signal, low-noise, fast-responding, actionable**.
- **Decouple deploy from release** — you can deploy to production without exposing users to the new code, then progressively route traffic. This is the enabler for canary, blue-green, and tap-compare.
- Build **automated rollback** triggered by metric degradation. Human response is too slow.

**Don't:**
- Conflate deploy with release — it forces a binary choice and removes progressive-delivery options.
- Rely on humans to detect and roll back canary regressions within seconds.
- Monitor a long tail of metrics during release; signal drowns in noise.
- Ship without a tested rollback path.

*Ref: How To - What to Test and When 22-07-21.md — "At Release – Supporting the Release Process"*

---

### Production Stage — INFORM PRODUCT DESIGN

**Principle:** Production is the most valuable testing environment because it has real users, real data, real conditions. Treat it as a source of learning, not a place to be protected.

**Do:**
- Run **capacity monitoring** (CPU, memory, disk I/O, network, DB connections, queue depths) with alerts as utilization approaches dangerous thresholds.
- Run **technical monitoring** (service health, dependency health, cache hit rates) as the foundation of operational excellence.
- Run **performance verification** on real-user data (RUM) — network latency, geographic effects, and real data patterns surface issues no synthetic test catches.
- Run **security verification** continuously — access patterns, exfiltration attempts, vuln scans, control checks.
- Run **A/B tests** for product/feature decisions. Microsoft's research: ~2/3 of ideas produce zero or negative value.
- Run **business experiments** (pricing, flows, recommendations, layouts) with rigorous experimental design and statistical analysis.
- Track **commercial performance** (conversion, revenue, engagement, churn) — the ultimate measure of whether the software fulfills its purpose.
- Apply the **three pillars of observability**: logs (rich event context), metrics (trends, alerts, macro view), distributed traces (latency, bottlenecks across services).
- Close the loop: when production reveals a bug, add a unit test (Commit), an acceptance test (Acceptance), and a new monitoring metric (Production).

**Don't:**
- Treat production as untouchable. Testing-in-production must be done safely (progressive rollout, instant revert) but it must be done.
- Monitor everything. A few high-signal metrics beat a wall of low-signal dashboards.
- Skip A/B testing and ship features on assumption.

*Ref: How To - What to Test and When 22-07-21.md — "In Production – Learning and Improving"*

---

### The Deployment Pipeline as Organizer

**Principle:** The four phases map to stages of the deployment pipeline. The pipeline is the structure that makes the strategy executable.

| Pipeline stage | Maps to | Speed budget |
|----------------|---------|--------------|
| Commit | Commit stage | seconds → minutes |
| Acceptance | Acceptance stage | minutes → tens of minutes |
| Release | Release stage | minutes |
| Operate | Production stage | continuous |

- Commit failures → reject the commit, notify developer immediately.
- Acceptance failures → do not promote to release candidate.
- Release failures → auto-rollback.
- Production → continuous observation, alerting, experimentation.

*Ref: How To - What to Test and When 22-07-21.md — "How the Four Phases Connect"*

---

### Test Pyramid Reinterpreted

**Principle:** Mike Cohn's pyramid (many unit, fewer integration, fewest e2e UI) is necessary but not sufficient. Add release-time checks and production-time observation on top.

**Do:**
- Maintain the pyramid ratio: many fast unit tests at the base.
- Reserve slow end-to-end tests for the critical user journeys only.
- Extend the pyramid upward with canary/smoke at release and continuous observation at production.
- Use deployment-decoupled release (canary, blue-green) to push testing into production safely.

**Don't:**
- Invert the pyramid (few unit tests, many e2e tests) — slow, brittle, expensive.
- Stop at the top of the classic pyramid and ignore production.

*Ref: How To - What to Test and When 22-07-21.md — "The Test Pyramid Reinterpreted"*

---

### Production Testing Techniques (Advanced)

**Principle:** When deploy is decoupled from release, you can run rich testing techniques against real production conditions without exposing users.

**Do:**
- Apply **Chaos Engineering** (Netflix Simian Army: Chaos Monkey, Latency Monkey, Conformity Monkey, Doctor Monkey, Janitor Monkey, Security Monkey, Chaos Gorilla) to build confidence in failure recovery — treat it as a scientific discipline.
- Use **dark launching / feature flagging** to deploy new code hidden behind a flag, test it in production, dogfood it, A/B test it, then progressively enable for users.
- Use **shadowing / dark traffic** to replay real production traffic against a new version. Best for stateless / idempotent operations; handle stateful writes carefully.
- Use **tap compare** (Twitter Diffy, GitHub Scientist) to multicast requests to old + new versions and compare responses.
- Load-test with **real production traffic**: traffic shifting (LinkedIn Redliner), shadow loading (Facebook McRouter), stress through scale reduction.
- Run **integration tests in production** by deploying to prod without routing traffic, then exercising against real dependencies. Handle stateful writes via test accounts, marked test data, or per-test tables.

**Don't:**
- Skip safety controls (gradual rollout, instant revert) when testing in production.
- Replay stateful writes against a production DB without isolation.
- Run chaos experiments without engineers on call and a rollback path.

*Ref: How To - What to Test and When 22-07-21.md — "Chaos Engineering" / "Dark Launching and Feature Flagging" / "Shadowing" / "Tap Compare" / "Load Testing with Production Traffic" / "Integration Testing in Production"*

---

### Speed vs. Scope Trade-offs

**Principle:** Each phase deliberately trades scope for speed (or vice versa). The framework is designed so cheap, fast tests catch common problems early while expensive, comprehensive tests are reserved for later stages.

| Phase | Speed | Scope |
|-------|-------|-------|
| Commit | maximum | minimum — single units |
| Acceptance | moderate | broad — full system |
| Release | fast | targeted — release process + critical paths |
| Production | continuous | unlimited — real conditions |

*Ref: How To - What to Test and When 22-07-21.md — "Speed vs. Scope Trade-offs"*

---

### Team Structure and Testing Ownership

**Principle:** Quality is a team responsibility, not a separate department. Separate QA teams concentrate testing in one phase and create feedback gaps.

**Do:**
- Embed testing ownership in the development team:
  - Developers own Commit-stage unit tests
  - Team collectively defines and automates acceptance tests
  - Team owns the deployment pipeline, including release automation
  - Team owns production monitoring and observability
- Use test-engineering specialists as enablers (test automation, perf, security expertise) — not as a gate.

**Don't:**
- Hand off testing to a separate QA team that operates only at the Acceptance stage.
- Treat production monitoring as "ops' problem" rather than the team's responsibility.

*Ref: How_To_What_to_Test_and_When.md — "Team Structure and Testing Ownership"*

---

### Metrics for Evaluating the Testing Strategy

**Do:**
- Track **deployment frequency** (high performers deploy multiple times/day).
- Track **lead time for changes** (commit → production).
- Track **change failure rate** (% of deployments causing production failures).
- Track **mean time to recovery**.
- Track **test suite execution time** per phase.
- Track **defect escape rate** (defects found in production that earlier stages missed) — this surfaces gaps.

*Ref: How_To_What_to_Test_and_When.md — "Metrics for Evaluating Your Testing Strategy"*

---

### Cost of Quality vs. Cost of Failure

**Principle:** The framework is a menu, not a mandate. Scale testing investment to the cost of failure.

| Failure cost | Examples | Investment |
|--------------|----------|------------|
| Extreme | Medical devices, aviation, autonomous vehicles | Full framework + formal verification |
| High | Trading platforms, payment processors | Full framework, emphasis on data integrity + compliance |
| Moderate | Consumer web apps | Full framework, emphasis on production testing + rapid recovery |
| Low | Internal tools, prototypes | Commit stage + basic prod monitoring |

*Ref: How_To_What_to_Test_and_When.md — "The Cost of Quality vs. The Cost of Failure"*

---

## Anti-Patterns & Common Mistakes

- **Testing as a separate phase:** Done by a QA team after "development is complete" → feedback is slow and expensive. *Fix:* integrate testing into every pipeline stage.
- **Over-reliance on end-to-end tests:** Slow, brittle, hard to maintain. *Fix:* keep the pyramid — many unit, fewer integration, fewest e2e.
- **Testing only before release:** Misses the most valuable feedback. *Fix:* invest in production observation and experimentation.
- **Monitoring everything:** Noise drowns signal. *Fix:* a few high-signal metrics (e.g., p99 latency + HTTP fatal error rate).
- **Skipping data-migration testing:** Top cause of incidents. *Fix:* unit + integration tests on realistic data, with rollback covered.
- **Ignoring configuration testing:** Misconfig causes disproportionate outages. *Fix:* treat config as code — version-controlled, tested, deployed through the same pipeline.
- **Stopping at unit tests:** Components can pass unit tests and fail integration. *Fix:* layered strategy with acceptance, release, and production checks.

*Ref: How_To_What_to_Test_and_When.md — "Common Anti-Patterns"*

---

## Decision Heuristics / Checklists

- **Where does this test belong?**
  - Runs in ms, tests one unit → Commit stage.
  - Requires DB / FS / network → later stage (or mock the dependency at Commit).
  - Verifies end-to-end user behavior → Acceptance.
  - Verifies the deploy process → Acceptance or Release.
  - Verifies behavior under real production conditions → Production.
- **Is my Commit stage fast enough?** Full suite < 5 min, unit tests < 2 min. If not, redesign.
- **Is my Acceptance stage comprehensive enough?** Functional + deployment + configuration + security + performance + scalability + resilience + compliance.
- **Am I testing in production safely?** Decoupled deploy/release, automated rollback on high-signal metrics.
- **Am I learning from production?** A/B tests, RUM, business experiments feeding back into requirements.

---

## Key Takeaways

1. Testing is a continuous feedback mechanism, not a phase — Commit, Acceptance, Release, Production.
2. Commit stage must FAIL FAST — < 5 min total, unit tests < 2 min.
3. Acceptance stage defines RELEASABLE — BDD-style specs + non-functional + deployment + config.
4. Release stage SUPPORTS RELEASE — smoke, health checks, canary, auto-rollback.
5. Production stage INFORMS PRODUCT DESIGN — monitoring, A/B, business experiments.
6. Unit tests are the foundation, not the ceiling.
7. Test data migrations at unit AND integration levels.
8. Automate every stage; manual testing complements, never replaces.
9. Monitor a few high-signal metrics — not everything.
10. Treat configuration as code.
11. ~2/3 of ideas produce zero or negative value — measure in production.
12. Decouple deploy from release — enables canary, blue-green, tap-compare.
13. Quality is a culture, not a department.
14. Faster feedback → faster delivery — invest in speed at every stage.

---

## Cross-References
- Related: [[../Fundamentals_of_Software_Testing.md]]
- Related: [[../The_Art_of_Unit_Testing.md]]
- Related: [[../Continuous_Deployment.md]]
- Related: [[../TDD_Top_Tips.md]]
- Related: [[../ATDD_Guide.md]]
- Related: [[../The_Feedback-Driven_Developer.md]]