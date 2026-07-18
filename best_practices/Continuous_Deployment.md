# Continuous Deployment — Enable Faster Feedback, Safer Releases, and More Reliable Software

**Author:** Valentina Servile (Foreword by David Farley)
**Topic tags:** `#architecture` `#general` `#devops` `#reliability`
**Language focus:** Language-agnostic; examples use JavaScript/React, Java/Spring Boot, and SQL
**Sources:** `markdown_output/Continuous_Deployment/Continuous_Deployment.md` · `summaries/Continuous_Deployment.md`

## TL;DR
Continuous deployment removes the final manual production gate: every trunk commit that passes automated quality gates reaches production. Make that safe through one-piece flow, trunk-based development, small backward-compatible changes, feature toggles, expand-and-contract migrations, zero-downtime rollout, production observability, and rapid recovery. Separate technical deployment from business release, and optimize deployment frequency, lead time, change failure rate, and mean time to recover together.

---

## Best Practices by Topic

### 1. Trace the Lineage: XP → DevOps → CI → Continuous Delivery → Continuous Deployment

**Principle:** Treat continuous deployment as the logical completion of decades of shortening and automating software feedback loops.

**Lineage:**
- Use XP's rule: if integration, testing, review, or deployment hurts, do it more often.
- Use frequent practice to shrink each batch before automating the repeated work.
- Use DevOps to remove the organizational wall between writing and running software.
- Make product teams own code, infrastructure, deployment, and production behavior.
- Use CI to integrate into one shared mainline at least daily.
- Build and test an artifact after every mainline commit.
- Use continuous delivery to keep every successful artifact deployable to any environment.
- Use continuous deployment to remove the final human decision before production.
- Define success as code running for users, not code complete on a workstation.

**Do:**
- Automate build, test, provisioning, configuration, and deployment.
- Version application code, infrastructure code, pipeline configuration, and deployment logic.
- Keep the pipeline as the source of truth for whether a commit is releasable.
- Treat production feedback as the final closure of the development loop.

**Don't:**
- Don't call a CI server installation “continuous integration” while integrating infrequently.
- Don't call automated deployment to staging “continuous deployment.”
- Don't preserve a final manual production button and claim the path is fully automated.
- Don't throw code from development to operations across an organizational handoff.

*Ref: Continuous_Deployment.md — "eXtreme Programming"; "DevOps"; "Continuous Integration"; "Continuous Delivery"; "One Step Further: Continuous Deployment"*

---

### 2. Make the Deployment Pipeline an Executable Release Decision

**Principle:** Let each successful gate trigger the next gate until production, with no manual intervention.

**Required baseline:**
- Keep the software under version control.
- Maintain automated test coverage.
- Run an automated pipeline for every trunk commit.
- Let the pipeline own the complete path from commit to production.
- Deploy the trunk version to preproduction and production.
- Keep total pipeline time reasonable; the book proposes under one hour as a baseline.
- Remove pauses, buttons, sign-offs, and other human decisions from the flow.
- Automate any required approval as a reproducible check where possible.

**Do:**
- Build one immutable artifact and promote the same artifact through environments.
- Fail closed when a quality gate fails.
- Stop new work and restore a red or paused path quickly.
- Keep pipeline configuration reviewable and recoverable like infrastructure code.
- Make pipeline outcomes visible through information radiators.

**Don't:**
- Don't rebuild a different artifact for production.
- Don't hide manual testing inside a nominally automated deployment.
- Don't let commits queue indefinitely behind a stopped production stage.
- Don't create a special, rarely exercised emergency path for urgent fixes.

*Ref: Continuous_Deployment.md — "Implementation"; "Continuous Deployment to…Staging?"; "Implications"*

---

### 3. Apply Toyota Production System One-Piece Flow to Commits

**Principle:** Treat one atomic commit as one unit of software inventory and move it to production without batching.

**Lean chain:**
- Reduce transaction cost first.
- Use lower transaction cost to reduce batch size.
- Use smaller batches to shorten queues.
- Use shorter queues to reduce cycle time and variability.
- Use lower cycle time to enable just-in-time response to demand.
- Optimize the whole value stream, not utilization at one workstation.

**Toyota Production System lessons:**
- Avoid producing inventory from forecasts when demand should pull work.
- Expose defects quickly instead of hiding them behind buffers.
- Prevent local overproduction from starving or flooding downstream workstations.
- Use one-piece flow to shorten the time each item spends waiting.
- Treat quality problems as system signals, not reasons to add more inventory.

**SMED analogy:**
- Remember that Toyota reduced die changeover from 24 hours to under 10 minutes.
- Treat build, test, review, and deploy time as changeover cost.
- Reduce that cost before demanding smaller delivery batches.
- Automate repetitive checks so per-commit processing becomes economical.

**Software inventory:**
- Count discovery boards, designs, stories, local changes, branches, undeployed artifacts, and disabled features as inventory.
- Remember that inventory remains waste until users receive value.
- Measure queues even though information inventory is physically invisible.
- Remove bottlenecks where commits accumulate.

**Don't:**
- Don't celebrate a large backlog or release train as productive inventory.
- Don't maximize one team's output while extending end-to-end lead time.
- Don't batch releases merely because the transaction cost is currently high.
- Don't mistake an enormous commit for one-piece flow merely because it is one commit.

*Ref: Continuous_Deployment.md — "Origins of Lean Manufacturing"; "One-piece flow"; "Lowering transaction costs"; "Inventory in software"; "Batches in software"*

---

### 4. Use the Continuous Flow Ratio and Its Error Budget

**Principle:** Measure how closely commit flow approaches one commit to one production deployment.

```text
Number of production deployments / Total number of commits
```

**Do:**
- Count commits from every source-control branch in the denominator.
- Interpret a ratio near 1:1 as evidence that commits are not batching in branches, reviews, red builds, or paused pipelines.
- Treat the ratio as an SLO if it helps the team manage exceptions.
- Use an error budget to accommodate rare, explicitly justified pauses.
- Stop unrelated changes while a pipeline is intentionally paused.
- Restore continuous flow as soon as the exceptional work is safe.
- Investigate a falling ratio for low confidence, failed builds, long reviews, or branch accumulation.

**Don't:**
- Don't define continuous deployment solely by the absence of a manual task in one pipeline file.
- Don't ignore commits hoarded before the pipeline starts.
- Don't spend the error budget on routine risky changes.
- Don't continue piling commits onto a paused production stage.
- Don't turn a rare exception into a permanent release process.

*Ref: Continuous_Deployment.md — "Continuous flow ratio"*

---

### 5. Optimize All Four DORA Metrics Together

**Principle:** Improve throughput and stability as one system; do not trade one away for the other.

| Dimension | Metric | Operational definition in the book | Continuous deployment effect |
|---|---|---|---|
| Throughput | Deployment frequency | Production code updates per period | Approaches team commit frequency |
| Throughput | Lead time for changes | Remote source-control change to production | Becomes pipeline duration rather than pipeline plus human delay |
| Stability | Change failure rate | Failed changes divided by production changes | Smaller independent deltas avoid contaminating good changes |
| Stability | Mean time to recover | Average restoration time after disruption | Fast deploy, toggle-off, rollback, and fix-forward reduce recovery time |

**Deployment frequency:**
- Count technical deployments, not user-visible releases.
- Measure at team or independently deployable service level.
- Expect a typical product team in the author's experience to produce roughly 10–30 commits and deployments per day.
- Use frequency as evidence of healthy integration and flow, not as an end in itself.

**Lead time:**
- Start the clock when a change is shared to the remote source-control system.
- Stop it when production deployment completes.
- Remove human waiting time to make lead time lower and more predictable.
- Keep the pipeline fast enough that developers retain context.

**Change failure rate:**
- Divide production changes causing downtime, regressions, or disruption by all production changes.
- Reduce blast radius by deploying one commit independently.
- Preserve healthy changes when reverting a faulty one.
- Expect failure and design the process to recover gracefully.

**Mean time to recover:**
- Keep main deployable so an urgent fix never waits for tangled work.
- Use the tiny latest diff to narrow diagnosis.
- Deploy temporary diagnostics when production-only behavior appears.
- Prefer a routinely exercised path over an exceptional emergency path.

**Don't:**
- Don't count repeated no-op deployments to inflate frequency.
- Don't equate feature-release frequency with code-deployment frequency.
- Don't optimize for mean time between failures while neglecting recovery.
- Don't blame individual developers for a process that cannot contain inevitable mistakes.

*Ref: Continuous_Deployment.md — "DORA Metrics"; "Deployment frequency"; "Lead time for changes"; "Mean time to recover"; "Change failure rate"*

---

### 6. Separate Defining a Change from Exposing Its Behavior

**Principle:** Under continuous deployment, committing to trunk defines and applies production code nearly simultaneously; use runtime control to separate that deployment from release.

**Do:**
- Treat every trunk commit as an imminent production-system modification.
- Plan temporary redundancy and diversion before touching live behavior.
- Keep incomplete code isolated in a nonexecuted path.
- Define a deployment as putting code and configuration into production.
- Define a release as changing behavior observable by users.
- Let engineering own deployment cadence.
- Let product own release timing and experimentation.
- Classify any unintended visible effect of a deployment as a regression.

**Don't:**
- Don't assume a later human will catch a non-self-contained commit.
- Don't call work “done” before it has operated under production conditions.
- Don't ask product to delay a technical deployment because an experiment is running.
- Don't wait until release day to deploy the feature's code.
- Don't equate continuous deployment with uncontrolled continuous release.

*Ref: Continuous_Deployment.md — "Defining a Change Versus Applying a Change"; "A Deployment Is Not a Release"; "Differences"*

---

### 7. Build Cross-Functional, Autonomous Product Teams

**Principle:** Give one team the skills and authority to deliver and operate a vertical slice end to end.

**Do:**
- Include the development, infrastructure, testing, security, design, and product capabilities needed by the product.
- Make decisions without recurring dependency on outside approvers.
- Own frontend, backend, persistence, and operational behavior together where they form one value stream.
- Use stream-aligned teams for customer value.
- Use enabling, complicated-subsystem, and platform teams as self-service support rather than gates.
- Follow “you build it, you run it.”
- Share responsibility for incidents and learning.
- Use blameless reviews to improve safeguards.

**Don't:**
- Don't split ownership by technical layer when one feature requires all layers.
- Don't make QA a detached gatekeeping department.
- Don't require a platform team to perform ordinary deployments for product teams.
- Don't make one role accountable for production behavior it cannot influence.
- Don't make autonomy an excuse to ignore shared contracts.

*Ref: Continuous_Deployment.md — "Cross-Functional, Autonomous Teams"; "Fast Decision Making"; "Implementation Autonomy"*

---

### 8. Integrate Frequently with Trunk-Based Development

**Principle:** Merge small, coherent changes into one shared trunk at least daily, preferably many times per day.

**Do:**
- Push small, atomic, demonstrable commits.
- Keep trunk green and deployable.
- Prefer direct trunk work where team and regulatory context permit it.
- Use branches lasting less than a day when a pull request is required.
- Merge a large feature repeatedly while hiding incomplete behavior in execution branches.
- Rebase frequently when using short branches.
- Squash interdependent commits when that clarifies which change maps to one deployment.
- Write meaningful messages with task identifiers and coauthors where needed for traceability.
- Use pair programming for continuous review and rapid integration.
- Use responsive small pull requests when pair programming is not the team's choice.

**Don't:**
- Don't use Gitflow-style long-lived feature branches for product-team work.
- Don't equate a short branch mechanism with a feature branch containing a whole initiative.
- Don't let a branch become a private code garden.
- Don't add code-freeze or stabilization periods as routine practice.
- Don't delay integration to simulate simultaneous deployments across services.

*Ref: Continuous_Deployment.md — "Frequent Integration"; "Short-lived branches"; "Short-lived branches versus feature branches"; "Trunk-based development"*

---

### 9. Make Code Review Continuous and Psychologically Safe

**Principle:** Keep human review early and frequent without turning it into a queue in the path to production.

**Do:**
- Review design, intent, requirement understanding, abstraction, and architecture fit.
- Let static analysis handle repeatable low-level checks.
- Use pair programming to review code while assumptions and design are still forming.
- Use tiny pull requests and immediate reviewer attention if asynchronous review is required.
- Let junior engineers question senior engineers.
- Debate code quality openly without ruinous empathy.
- Rotate pairs to spread product and production knowledge.
- Use mob programming selectively for learning and exploration.

**Don't:**
- Don't assume green tests prove that the developer understood the requirement.
- Don't reserve review until after a large implementation is complete.
- Don't let pull requests wait for days.
- Don't make feedback socially unsafe.
- Don't treat junior work as requiring a slower deployment path when safeguards apply equally to everyone.

*Ref: Continuous_Deployment.md — "Frequent Code Reviews"; "Pull requests"; "Pair programming"; "Psychological safety"*

---

### 10. Shift Quality Left with Layered Automated Checks

**Principle:** Complete production-readiness work during implementation because there is no safe “later” after a commit reaches production.

**Do:**
- Run linting, static analysis, security scanning, and resource checks early.
- Maintain many fast unit tests and fewer slow high-level tests.
- Use the testing pyramid to balance speed, confidence, and maintenance cost.
- Use the Swiss cheese model to let different layers catch different defects.
- Write tests first so the code's first consumer shapes a testable API.
- Start a feature with a high-level acceptance test, then drive internals with unit tests.
- Temporarily ignore a still-failing new acceptance test only while the incomplete behavior remains isolated.
- Re-enable and commit the acceptance test when the feature becomes complete.
- Add a failing regression test before fixing each defect.
- Build characterization tests around legacy behavior before refactoring internals.
- Start legacy protection with high-level black-box coverage when the code is too tangled for unit seams.

**Don't:**
- Don't rely on repetitive manual regression testing.
- Don't leave high-level automation for a later QA phase.
- Don't deploy untested code and “edit and pray.”
- Don't duplicate every detailed unit assertion at expensive end-to-end levels.
- Don't tolerate permanently flaky red checks that train the team to ignore failures.

*Ref: Continuous_Deployment.md — "Automated Code Analysis"; "Test Automation"; "The testing pyramid model"; "The Swiss cheese model"; "Test-first"; "Outside-in"; "What about legacy?"*

---

### 11. Hide Work in Execution Branches, Not Long-Lived Version-Control Branches

**Principle:** Keep unfinished code on trunk but prevent ordinary users from invoking it.

**Two execution-branch tools:**
- Use feature toggles to select old or new behavior at runtime.
- Use expand and contract to move callers between old and new behavior through code changes.
- Recognize both as forms of branch by abstraction.
- Keep both execution paths tested while both remain possible.
- Remove the old path when migration and release are complete.

**Verbatim feature-toggle snippet:**
```javascript
const useNewAlgorithm = ... // <- retrieve toggle
if (useNewAlgorithm) { // <- toggling behavior
 return newWayOfCalculatingResult();
} else {
 return oldWayOfCalculatingResult();
}
```

**Do:**
- Introduce the branch point before adding incomplete behavior.
- Place the branch point at the outermost place where behavior diverges.
- Keep hidden code compilable, tested, and harmless.
- Release hidden inventory promptly.
- Track stale toggles and incomplete expand phases as WIP.

**Don't:**
- Don't change live behavior in place when a safe parallel path is needed.
- Don't scatter toggle checks through every layer.
- Don't assume hidden code is free of inventory cost.
- Don't leave disabled code to rot.

*Ref: Continuous_Deployment.md — "Hiding Work in Progress"; "Execution Branches"; "Feature toggles"*

---

### 12. Use Runtime Feature Toggles for New Features and Progressive Delivery

**Principle:** Use a runtime toggle when release speed, rapid disablement, production testing, or experimentation matters.

**Toggle anatomy:**
- Add decision points in code.
- Store ON, OFF, or richer targeting state outside the request path where appropriate.
- Provide an interface for authorized changes.
- Support targeting by user, request, cookie, header, percentage, or location when the platform allows it.
- Reconfigure one toggle across development, QA, canary, A/B test, and release stages.

**Do:**
- Build or adopt toggle infrastructure early, like pipeline infrastructure.
- Default a new top-level feature toggle to OFF.
- Put the decision at the outermost consumer.
- Use one nested level only when an increment needs an independent experiment.
- Test all meaningful ON/OFF combinations.
- Create cleanup work before release work is considered complete.
- Remove the toggle after the feature has been stable long enough for the team.
- Convert long-lived business configurability into explicit domain logic and administration.
- Consider a static toggle only when runtime lookup latency or availability is unacceptable.
- Add per-request overrides to a static toggle when production exploration is needed.

**Don't:**
- Don't use a toggle service as unmodeled permanent business configuration.
- Don't nest toggles deeply.
- Don't leave independent service flags inconsistent during a release.
- Don't let the toggle platform become an unhandled single point of failure.
- Don't use a static toggle when product experimentation requires persistent cohort assignment.

*Ref: Continuous_Deployment.md — "Feature toggles"; "What about static feature toggles?"; "Hiding with Feature Toggles"; "Deployment 5: Toggle cleanup"*

---

### 13. Use Expand → Migrate → Contract for Live Refactoring

**Principle:** Add a compatible new path, move every client, then remove the old path.

**Phases:**
1. **Expand:** Add the alternative implementation, operation, field, type, or system beside the old one.
2. **Migrate:** Move callers one at a time while both paths remain valid.
3. **Contract:** Delete the old path only after no client depends on it.

**Expansion choices:**
- Use an alternative system for a legacy rewrite or vendor replacement.
- Use an alternative operation for a new endpoint, event, table, or message.
- Use an alternative field for a payload field, column, event attribute, or XML attribute.
- Generify a field type temporarily when the smallest footprint outweighs its higher ambiguity risk.
- Prefer alternative operation or alternative field for common pragmatic migrations.

**Trade-off:**
- Duplicate more surface area to isolate existing behavior more safely.
- Duplicate less surface area only when the increased bug risk is acceptable and temporary code is controlled.

**Do:**
- Use expand-and-contract by default for refactoring live behavior.
- Keep the new implementation uncalled while building it.
- Prove equivalence before moving callers.
- Remove the old path immediately after all callers migrate.
- Use a runtime toggle as an extra safeguard only for a particularly risky refactor or cross-functional concern.

**Don't:**
- Don't refactor a shared contract in place.
- Don't contract while unknown consumers remain.
- Don't preserve temporary generic parsing indefinitely.
- Don't add API versioning casually if it will encourage permanent old-version support.

*Ref: Continuous_Deployment.md — "Expand and contract"; "Feature toggles versus expand and contract by type of change"; "Hiding with Expand and Contract"*

---

### 14. Preserve N and N−1 Compatibility Across Every Process Boundary

**Principle:** Make version N+1 of each independently deployed component compatible with production version N of every component it communicates with.

**Contracts include:**
- API shapes and status behavior.
- Message and event schemas.
- Database schemas.
- Files, pipes, sockets, and caches.
- Response time and security properties when consumers rely on them.
- Ordering and every other observable behavior covered by Hyrum's Law.
- Browser JavaScript already loaded before a backend deployment.

**Do:**
- Treat backend-to-database and frontend-to-backend boundaries as contracts even inside one repository and team.
- Deploy providers before consumers when adding optional capability.
- Use a consumer-side toggle to tolerate development in another order.
- Use expand-and-contract when no deployment order can make a changed contract compatible.
- Use consumer-driven contract tests for formal interteam contracts.
- Coordinate changes without synchronizing deployment moments.
- Keep old and new application instances compatible during blue/green and rolling updates.

**Don't:**
- Don't assume two steps in one pipeline execute simultaneously.
- Don't assume a monorepo removes distributed execution boundaries.
- Don't accept a brief burst of 500 errors as normal deployment behavior.
- Don't pause pipelines to simulate simultaneous updates.
- Don't delay integration until all repositories are ready.

*Ref: Continuous_Deployment.md — "Contract Compatibility Beyond Data Shape"; "Informal contracts"; "Contracts Between Paths to Production"; "Adding New Features: When Order Matters"; "Refactoring: When Timing Matters"*

---

### 15. Choose Zero-Downtime Deployment by Trade-off

**Principle:** Keep at least one healthy version serving traffic throughout every deployment.

| Strategy | Mechanism | Strength | Cost or risk | Best fit in the book |
|---|---|---|---|---|
| Blue/green | Deploy to an identical inactive environment, then switch traffic | Rapid traffic switch-back and isolated validation | Temporary or permanent duplicate infrastructure; N/N−1 compatibility | Strong rollback need and affordable duplicate capacity |
| Rolling | Replace old instances as new instances become healthy | Lower infrastructure cost and native container support | Mixed versions coexist; rollout depends on readiness | ECS, Kubernetes, and similar clusters |
| Canary deployment | Put a subset of instances on the new version and compare metrics | Real-traffic technical validation before full rollout | Setup complexity, stable metrics, statistical delay | High-risk or large-scale systems needing automated comparison |

**Do:**
- Require readiness and health checks before serving traffic.
- Configure rolling updates so available capacity never drops below the safe floor.
- Keep N compatible with N−1 throughout overlap.
- Use application error rate and performance for canary promotion decisions.
- Pick rolling plus tests, toggles, and observability when sophisticated canary analysis is unnecessary.
- Automate all rollout stages.

**Don't:**
- Don't expose a maintenance window on every deployment.
- Don't use blue/green's inactive side as a manual QA environment.
- Don't pause a rolling deployment for product feedback.
- Don't use partial infrastructure deployment as an A/B test.
- Don't conflate a canary deployment of code with a canary release of behavior.

*Ref: Continuous_Deployment.md — "Zero-Downtime Deployments"; "Blue/green deployments"; "Rolling deployments"; "Canary deployments"; "Deployment strategies and manual steps"*

---

### 16. Build Production Safety Checks into Every Change

**Principle:** Make the safety net detect mistakes early and recovery fast rather than demanding impossible human perfection.

**Pre-deployment checks:**
- Verify the commit is small and self-contained.
- Verify review occurred through pairing or a responsive pull request.
- Run static code, dependency, vulnerability, and configuration checks.
- Run the agreed unit, integration, component, acceptance, contract, and visual checks.
- Build the immutable artifact.
- Apply infrastructure and database changes through reviewed automation.
- Verify backward compatibility with coexisting versions.
- Verify required toggle defaults are safe.

**Deployment checks:**
- Require successful instance readiness and health checks.
- Maintain zero downtime and adequate capacity.
- Run automated smoke or synthetic tests against production.
- Attach deployment/version information to telemetry.
- Publish success or failure to team-visible channels.
- Keep technical and business dashboards available.

**Post-deployment checks:**
- Watch latency, traffic, errors, and saturation.
- Watch Largest Contentful Paint, Cumulative Layout Shift, and Interaction to Next Paint for frontend behavior.
- Watch relevant business behavior, not only infrastructure.
- Alert on user-visible symptoms rather than hypothetical causes.
- Keep alerts few, actionable, and maintained with the code.
- Make detailed logs and traces searchable after a dashboard indicates trouble.

**Don't:**
- Don't page on high load when users still receive acceptable service.
- Don't add an alert for every metric.
- Don't tolerate alerts that repeatedly cry wolf.
- Don't add observability after implementation if doing so requires redesign.
- Don't make humans watch dashboards continuously instead of using alerts.

*Ref: Continuous_Deployment.md — "You Must Be This Tall"; "Observability and Monitoring"; "Alerts"; "Information versus noise"*

---

### 17. Design Deployment-Sensitive Systems for Replacement

**Principle:** Make instances disposable, stateless, quick to start, and safe to stop.

**Long-running work:**
- Move asynchronous or interruption-sensitive work to queues or event systems.
- Store resumable job state externally.
- Use graceful shutdown only with explicit bounds.
- Accept slower processing when durable checkpoints are more important than in-memory speed.
- Evaluate whether very long job locks make continuous deployment impractical.

**Sessions:**
- Externalize session and cart state.
- Treat critical in-memory state as a deployment and scaling defect.
- Avoid sticky-session dependence where instance replacement can lose state.

**Caches:**
- Set deliberate cache-control and expiry policies for client assets.
- Evaluate every cache between client and origin for invalidation behavior.
- Prepare for extra misses and origin load after frequent deployments.
- Use external caches when cold-instance behavior is unacceptable.
- Account for network latency, cost, security, and schema evolution introduced by external caches.

**Scaling and startup:**
- Keep startup work minimal.
- Measure startup in seconds rather than minutes where possible.
- Avoid mandatory downstream calls and data ingestion before readiness.
- Understand whether deployment and autoscaling can overlap.
- Use temporarily generous scaling or planned pre-scaling only when faster startup cannot solve the problem.

**Don't:**
- Don't run irreplaceable long-lived work inside traffic-serving instances.
- Don't let frequent deployments continually erase essential warm state without mitigation.
- Don't use pre-scaling as a routine manual coordination mechanism.
- Don't ignore deployment effects on autoscaling metrics.

*Ref: Continuous_Deployment.md — "Systems That Are Sensitive to Deployments"; "Interruption of Long-Running Processes"; "Sticky Sessions"; "Invalidation of Client-Side Caches"; "Scaling Interruptions"; "A Constant Stream of Cold Instances"*

---

### 18. Know When Full Continuous Deployment Does Not Fit

**Principle:** Evaluate control of the production environment, deployment disruption, regulation, team load, and product expectations before removing the gate.

**User-installed software:**
- Use self-applying desktop updates only when user expectations permit them.
- Expect mobile users to remain on old versions for months or years.
- Preserve backend compatibility for the mobile long tail.
- Consider web views, progressive web apps, or server-driven UI only as deliberate architectural choices.
- Prefer explicit delivery cadence for safety-critical appliances and devices.
- Avoid flooding library consumers with versions they must manually adopt.

**Regulation:**
- Isolate critical components into separately deployable units.
- Identify whether the constraint is law, framework, company policy, or inherited risk aversion.
- Satisfy segregation of duties through peer review or pair programming where permitted.
- Use pipeline records as an automatic audit trail.
- Record requirement, author, reviewer, tests, artifact, dependencies, deployment tooling, and production version.
- Accept a real unavoidable manual gate when public harm makes it necessary.

**Cognitive load:**
- Split oversized monoliths and teams when one pipeline becomes continuously busy.
- Keep teams near a two-pizza size as the book's practical heuristic.
- Keep pipelines fast so the author retains context.
- Train engineers across testing, security, infrastructure, observability, and release practices.
- Use pairing to onboard engineers into real production changes.
- Establish core development hours when solo changes would create unacceptable support risk.

**Don't:**
- Don't force continuous deployment onto user-controlled devices by definition alone.
- Don't assume every regulation mandates a heavyweight release board.
- Don't continuously deploy a monolith receiving an unmanageable stream of unrelated changes.
- Don't trade healthy flexible work arrangements away without discussing the operational constraint.

*Ref: Continuous_Deployment.md — "User-Installed Software"; "Regulated Industries"; "Cognitive Load"*

---

### 19. Slice Product Work Vertically and Thinly

**Principle:** Deliver a small user-valued behavior through every necessary layer instead of completing one technical layer at a time.

**Use vertical slices to:**
- Exercise persistence, backend, and frontend together early.
- Test from the user's perspective.
- Reveal contract mistakes while context is fresh.
- Release a minimum valuable capability before optional refinements.
- Stop an initiative without discarding completed value.
- Run narrower experiments on independent increments.
- Prevent unreleased code from accumulating under one giant toggle.

**Use MVP reasoning:**
- Identify the simplest form that satisfies the user's goal.
- Ask whether the slice would still be worth releasing if funding stopped immediately afterward.
- Treat every nonessential enhancement as a later increment.

**Use INVEST:**
- Make the story Independent.
- Keep implementation details Negotiable.
- Make it Valuable to the user.
- Make it Estimable.
- Make it Small enough for hours or days, not weeks or months.
- Make its external behavior Testable.

**Don't:**
- Don't create “database story,” “backend story,” and “frontend story” for one user capability.
- Don't call a technical layer task a user story.
- Don't build a complete deep layer that has no user entry point for production testing.
- Don't let a story consume an entire sprint when it can be split further.
- Don't park code in production indefinitely just because a toggle hides it.

*Ref: Continuous_Deployment.md — "Horizontal Versus Vertical Slicing"; "With Continuous Deployment"; "Effective Vertical Slicing"; "MVP"; "INVEST"; "Small Slices"*

---

### 20. Add Cross-Functional Requirements to Every Story

**Principle:** Treat deployability, testability, observability, security, and performance as layers of every production-ready vertical slice.

**Verbatim summary template:**
```
As a <user> I want to <do thing> So that I <achieve objective>
Given <precondition> When <action> Then <outcome>
Deployability: <feature toggle / expand and contract / other?>
Testability: <notes on automated tests, manual testing in production>
Observability: <notes on logs, metrics, dashboards, alerts>
Security: <new inputs, data, dependencies, infrastructure>
Performance: <network requests, data size, persistence layer>
```

**Deployability:**
- Decide between a new top-level toggle, a nested toggle, an existing toggle, expand-and-contract, an unhidden change, a rare branch, or a rare pipeline pause.
- Define the outermost branch point before implementation.
- Define cleanup and release ownership.

**Testability:**
- Select the right layers of automation.
- Define test data and stubs.
- Explain how a human can trigger and observe the behavior in production.
- Revisit the slice if it cannot be verified as user behavior.

**Observability:**
- Add or revise logs, metrics, dashboards, and alerts.
- Decide which edge cases are warnings, errors, or valid outcomes.
- Include business metrics proving the story's intended value.
- Test that triggering the feature produces the expected telemetry.

**Security:**
- Sanitize every new input.
- Recheck authentication and authorization.
- Protect sensitive data at rest, in transit, and in logs.
- Assess direct and transitive dependencies.
- Review permissions for new infrastructure.

**Performance:**
- Identify new synchronous network calls.
- Add timeouts, error handling, circuit breakers, or bulkheads where needed.
- Predict data growth with product input.
- Set collection limits, pagination, or lazy loading.
- Assess query shape, indexes, read/write balance, denormalization, sharding, and replicas.

**Don't:**
- Don't postpone cross-functional work to a hardening sprint.
- Don't add a cache before evidence justifies its complexity.
- Don't assume internal or admin users are trusted.
- Don't let a product story go to development with unresolved production-critical questions.

*Ref: Continuous_Deployment.md — "Building for Production"; "Deployability Requirements"; "Testability Requirements"; "Observability Requirements"; "Security Requirements"; "Performance Requirements"; "A (More) Complete User Story Template"*

---

### 21. Add New Features Outside-In Under a Toggle

**Principle:** Start at the outermost user-visible layer, use mocks or stubs for unavailable providers, and deploy every safe intermediate state.

**Workflow:**
1. Read the story and acceptance criteria.
2. Inspect the current architecture and code.
3. Sketch the desired target state.
4. Plan a sequence of tiny deployments from current to target state.
5. Add the outermost toggle first.
6. Build the UI against stubs.
7. Build backend operations incrementally.
8. Add the database evolution separately.
9. Exercise the complete feature in production.
10. Release by changing runtime toggle state.
11. Remove the toggle after stability is established.

**Why outside-in:**
- Validate visible requirements before speculative internals.
- Let each consumer drive the provider API beneath it.
- Align with London-style outside-in TDD.
- Make each deployed UI increment available for production exploration.
- Use the toggle to neutralize temporary provider/consumer incompatibility.

**Verbatim table evolution snippet:**
```sql
CREATE TABLE LAST_MINUTE_ITEMS (
 PRODUCT_ID UUID NOT NULL,
 SHOP_ID UUID NOT NULL,
 CONSTRAINT FK_PRODUCT
 FOREIGN KEY (PRODUCT_ID)
 REFERENCES PRODUCTS(PRODUCT_ID),
 CONSTRAINT FK_SHOP
 FOREIGN KEY (SHOP_ID)
 REFERENCES SHOPS(SHOP_ID)
 );
```

**Do:**
- Evaluate the toggle once in the outermost component.
- Deploy a stub first to verify placement and routing.
- Deploy intermediate visual states for designer and QA feedback.
- Keep a high-level test as the completion guide.
- Seed controlled test or pilot data for end-to-end production verification.
- Release without a deployment when the runtime toggle is ready.

**Don't:**
- Don't begin at the database merely because providers must exist before an unhidden consumer.
- Don't wait until all layers are complete to test integration.
- Don't wrap every backend layer in another copy of the same toggle without a security reason.
- Don't retain the release toggle as permanent domain configuration.

*Ref: Continuous_Deployment.md — "Adding New Features"; "Multiple layers: Outside in"; "Implementing with a Feature Toggle"; "Deployment 1: Introducing the toggle"; "Release"*

---

### 22. Refactor Multilayer Systems Inside-Out

**Principle:** Expand from the innermost provider outward, migrate the outermost consumer, then contract inward only after every client has moved.

**Do:**
- Start the outer cycle at the database or deepest provider.
- Expand the backend operation to expose the new database path.
- Migrate the frontend or outermost client.
- Contract the backend's old contract.
- Contract the database only after all backend clients stop using the old field.
- Nest an expand-and-contract cycle for each layer.
- Repeat nested cycles for every endpoint, table, or consumer.
- Keep new feature work compatible with both paths while a long migration runs.

**Nesting rule:**
- Expand all providers from inside out.
- Migrate from the outermost consumer.
- Contract only when the dependency graph proves the old path unused.

**Verbatim expansion snippet:**
```sql
-- new category table
CREATE TABLE CATEGORIES (
 CATEGORY_ID UUID UNIQUE NOT NULL PRIMARY KEY
 DEFAULT gen_random_uuid(),
 NAME TEXT NOT NULL
);
-- seed category table with current categories
INSERT INTO CATEGORIES (name)
```

```sql
 VALUES ('Fruit and vegetables'),
 ('Bathroom products'),
 ('Bakery'),
 ('Deli'),
 ('Fish'),
 ('Meat'),
 ('Prepared foods'),
 ('Pharmacy'),
 ('Frozen food');
-- new product uuid with default value
ALTER TABLE PRODUCTS
 ADD COLUMN PRODUCT_UUID UUID UNIQUE NOT NULL
 DEFAULT gen_random_uuid();
-- new reference to category table (nullable for 
ALTER TABLE PRODUCTS
 ADD COLUMN CATEGORY_ID UUID
 REFERENCES CATEGORIES(CATEGORY_ID);
```

**Don't:**
- Don't replace all layers with their target-state contracts at once.
- Don't migrate one apparent client and overlook other endpoints or foreign keys.
- Don't drop the outer provider field while any nested cycle remains.
- Don't synchronize deployments; preserve compatibility instead.

*Ref: Continuous_Deployment.md — "Refactoring Live Features"; "Multiple Layers: Inside Out"; "Implementing with Expand and Contract"*

---

### 23. Evolve Database Contracts Without Data Loss

**Principle:** Deploy database and application changes separately, and synchronize both old and new representations throughout the transition.

**Failure mode — simultaneous rename:**
```sql
ALTER TABLE USERS
 RENAME COLUMN NAME TO USERNAME;
```

- Reject this combined with application code that immediately uses `USERNAME`.
- Expect old and new application instances to coexist during zero-downtime rollout.
- Expect old instances to fail after the rename.
- Deploy database evolutions on their own even when schema and application share a repository.

**Failure mode — simple expand and contract:**
- Reject “add new column, copy current data, later switch code” without ongoing synchronization.
- Expect rows written between expand and migration to leave gaps in the new column.
- Do not repair the gap by coupling expand and migration into one deployment.

**Solution A — temporary database trigger:**
- Add the new field.
- Backfill current data.
- Add a trigger synchronizing inserts and updates in both directions.
- Migrate application readers and writers.
- Remove the old field and trigger.
- Use this when database-side logic is acceptable.

**Verbatim trigger excerpt from the source:**
```sql
ALTER TABLE Customer ADD FirstName VARCHAR (4
COMMENT ON Customer.FirstName 'Renaming of FN
COMMENT ON Customer.FName 'Renamed to FirstNa
dropdate = November 14 2007';
UPDATE Customer SET FirstName = FName;
CREATE OR REPLACE TRIGGER SynchronizeFirstNam
BEFORE INSERT OR UPDATE
ON Customer
REFERENCING OLD AS OLD NEW AS NEW
FOR EACH ROW
DECLARE
BEGIN
IF INSERTING THEN
IF :NEW.FirstName IS NULL THEN
:NEW.FirstName := :NEW.FName;
END IF;
IF :NEW.Fname IS NULL THEN
```

```sql
:NEW.FName := :NEW.FirstName;
END IF;
END IF;
IF UPDATING THEN
IF NOT (:NEW.FirstName=:0LD.FirstName) THEN
:NEW.FName:=:NEW.FirstName;
END IF;
IF NOT (:NEW.FName=:0LD.FName) THEN
:NEW.FirstName:=:NEW.FName;
END IF;
END IF;
END;
```

**Solution B — double-write:**
1. Expand with a nullable new column and relax old constraints needed for migration.
2. Change application writes to populate old and new columns.
3. Backfill historical rows after new writes are synchronized.
4. Add strong constraints to the new column.
5. Move reads and writes to the new column.
6. Drop the unused old column.

**Verbatim expansion and contraction snippets:**
```sql
ALTER TABLE USERS ADD COLUMN USERNAME TEXT;
ALTER TABLE USERS ALTER COLUMN NAME DROP NOT NULL
```

```sql
UPDATE USERS SET USERNAME = NAME WHERE USERNAME I
ALTER TABLE USERS ALTER COLUMN USERNAME SET NOT N
```

```sql
ALTER TABLE USERS DROP COLUMN NAME;
```

**Solution C — double-read:**
1. Expand with a nullable new column.
2. Move writes to the new column.
3. Read the new column first and fall back to the old column.
4. Backfill historical rows.
5. Add strong constraints to the new column.
6. Remove fallback reads.
7. Drop the old column.

**Verbatim double-read repository fragment:**
```java
 public User create(CreateUserPayload payload) {
 String insert = "INSERT INTO USERS(USERNAME) 
 return jdbcTemplate.queryForObject(insert, ne
 }
 public User findBy(UUID id) {
 String query = "SELECT COALESCE(USERNAME, NAM
 return jdbcTemplate.queryForObject(query, new
 }
```

**NoSQL:**
- Preserve the same compatibility rules even without an enforced write schema.
- Migrate on read forever for immutable stores only when permanent conversion logic is acceptable.
- Migrate on read and convert on write when old data expires or is naturally rewritten.
- Run a custom background batch update after new-format writes are active when old records persist.
- Version immutable events and apply ordered upgraders before domain-object deserialization.

**Don't:**
- Don't drop an old field before every reader and writer has migrated.
- Don't add `NOT NULL` to the new field before future and historical data are complete.
- Don't run a batch migration before the application stops producing the deprecated shape.
- Don't assume NoSQL removes data-shape contracts.
- Don't treat a destructive database rollback as equivalent to switching application traffic back.

*Ref: Continuous_Deployment.md — "Data and Data Loss"; "Failure Mode: Simultaneous Change"; "Failure Mode: Simple Expand and Contract"; "Solution: Temporary Database Trigger"; "Solution: Double-Write"; "Solution: Double-Read"; "NoSQL"*

---

### 24. Test in Production with Precise Isolation

**Principle:** Use production because only production has the real data, traffic, topology, configuration, dependencies, and user behavior.

**Production advantages:**
- Validate real data volume and distribution.
- Encounter old and unusual data shapes.
- Exercise real request sequences and user mistakes.
- Observe real incoming and outgoing traffic.
- Exercise the actual number and size of instances.
- Use real application and network configuration.
- Integrate with production versions of internal and third-party services.
- Reduce staging infrastructure and engineering cost.
- Avoid copying sensitive production data into weaker preproduction controls.

**Precise activation strategies:**
- Use a query parameter for one convenient request or page.
- Use custom request headers for APIs or browser-extension-controlled flows.
- Use cookies for browser-visible state that must persist across requests.
- Allow-list specific authenticated users.
- Use an application role or test account.
- Require precision and ease of use for technical and nontechnical testers.

**Test data:**
- Mark synthetic data explicitly.
- Filter it from normal reads.
- Restrict synthetic writes to controlled users or request signals.
- Keep payment and other sensitive test flows incapable of real external effects.
- Decide whether APIs hide test data, return it on request, or always return it flagged.
- Coordinate the contract if downstream systems receive flagged test data.

**Frontend debugging:**
- Publish source maps when the organization's security model permits it.
- Do not rely on minification as security.
- Keep true secrets and sensitive logic off user devices.
- Host source maps behind restricted production access if public publication is unacceptable.

**Life after staging:**
- Keep only the preproduction infrastructure automated tests genuinely need.
- Spin up dependencies and stubs without reproducing the entire production ecosystem.
- Let developers, QA, product, and stakeholders inspect the same production behavior.
- Remove staging as a mandatory release gate when the production-testing safety net is mature.

**Don't:**
- Don't expose test data to normal users accidentally.
- Don't let synthetic transactions leak into unaware downstream systems.
- Don't copy production data into staging merely to improve realism.
- Don't remove staging before tests, toggles, observability, and production-data isolation are mature.
- Don't call unguarded ad hoc testing in production a mature practice.

*Ref: Continuous_Deployment.md — "Testing in Production"; "Why You Should Test in Production"; "Feature Toggle Activation Strategies"; "Managing test data"; "Life After Staging"*

---

### 25. Use Progressive Delivery for Releases, Not for Holding Deployments

**Principle:** Deploy code completely, then expose behavior gradually through runtime controls.

**Coordinate distributed flags:**
- Reject independent per-service cohort decisions for one logical feature.
- Propagate the chosen flag state down the call chain, or use a central flag service.
- Combine central evaluation and propagation when repeated lookups cost too much.
- Keep one user's group assignment consistent through the session.

**Canary release:**
- Start with a small traffic percentage and ramp gradually.
- Target by device when platform-specific risk matters.
- Target by country when markets differ or lower-risk markets can pilot.
- Target by user segment, role, demographics, behavior, feedback history, or friends-and-family status when relevant.
- Watch technical and business dashboards after every ramp.
- Use canaries primarily to find unexpected release problems.

**A/B testing:**
- Randomly assign control and experiment groups.
- Define the hypothesis and outcome before starting.
- Instrument analytics with experiment assignment.
- Measure user behavior such as sessions, page views, heatmaps, funnels, conversion, or engagement as relevant.
- Test one variable at a time.
- Avoid overlapping experiments in the same product area.
- Run long enough to achieve a sufficient sample size.
- Schedule delivery around the experiment calendar so hidden code does not age.
- Use split or redirect tests for substantially different flows.
- Use full-factorial multivariate tests to measure every combination when traffic permits.
- Use fractional-factorial tests to reduce traffic requirements at the cost of precision.

**Canary versus A/B:**
- Use a canary to answer: “Did this release introduce an unexpected problem?”
- Use an A/B test to answer: “Is the product hypothesis correct?”
- Expect a canary to progress toward 100% after safety is demonstrated.
- Accept that an A/B test may lead to removing the feature entirely.

**Don't:**
- Don't use before/after comparison when seasonality, events, marketing, competitors, or other releases can confound results.
- Don't keep version N and N+1 partially deployed while waiting for product feedback.
- Don't let experiments block unrelated code deployments.
- Don't read results before statistical evidence is sufficient.
- Don't leave experiment toggles accumulating because release scheduling was ignored.

*Ref: Continuous_Deployment.md — "Using Feature Flags for Releases"; "Coordinating Feature Flag Releases in Distributed Systems"; "Canary Releases"; "A/B Testing"; "Experiment Best Practices"; "Do You Need a Canary Release or an A/B Test?"*

---

### 26. Recover Quickly: Toggle Off, Route Back, Revert, or Fix Forward

**Principle:** Expect faults, preserve a deployable mainline, and choose the smallest safe recovery action.

**Runtime release recovery:**
- Turn the feature toggle OFF when the new behavior causes harm.
- Stop a percentage ramp without rolling application code back.
- Preserve unrelated deployed improvements.
- Diagnose after user impact is contained.

**Infrastructure recovery:**
- Route traffic back to the previous blue/green environment when it remains compatible.
- Redeploy a known-good version when production code must move backward.
- Use a pipeline workflow that can deploy a selected commit or service.
- Keep artifact and telemetry version identifiers correlated.

**Source recovery:**
- Revert the faulty commit to trigger the ordinary deployment pipeline.
- Fix forward when the small defect is understood and pipeline lead time is short.
- Deploy diagnostics first when production-only evidence is missing.
- Keep every recovery on the routinely exercised path.

**Database caution:**
- Prefer forward-compatible transitional schema changes.
- Do not assume rerouting application traffic reverses data migration.
- Preserve old fields and representations until rollback windows and all clients no longer require them.
- Use idempotent synchronization steps where repeated execution is possible.

**Do:**
- Contain user impact before completing root-cause analysis.
- Keep changes so small that rollback does not remove unrelated value.
- Record incidents and improve tests, alerts, or architecture afterward.
- Optimize MTTR rather than pretending failures can be eliminated.
- Maintain break-glass access with audit and later review where regulated response requires it.

**Don't:**
- Don't create an undeployable mainline that blocks emergency fixes.
- Don't wait for an approver during an active incident if the approved process supports automatic recovery.
- Don't roll back a large batch that mixes healthy and faulty changes.
- Don't blame the engineer instead of repairing the safety net.

*Ref: Continuous_Deployment.md — "Mean time to recover"; "Blue/green deployments"; "ClimatePartner's Implementation of Continuous Deployment"; "REA's Implementation of Continuous Deployment"; "Maze's Implementation of Continuous Deployment"; "TravelPerk's Implementation of Continuous Deployment"*

---

## Case-Study Deep Dives

### 27. AutoScout24

**Context:**
- Operate a pan-European vehicle marketplace serving over 30 million monthly users and 43,000 dealer partners.
- Support over 200 developers, more than 2,000 repositories, more than 1,000 services, and more than 1,500 pipelines.
- Average roughly six minutes for deployment and fifteen minutes for build in the case study.

**Adoption:**
- Replace monolithic data-center systems, shared Oracle integration, unreliable shared environments, manual promotion, and dedicated downstream QA.
- Move to autoscaling AWS microservices and autonomous Agile teams.
- Adopt trunk-based development, blue/green deployment, feature toggles, and automatic production deployment for new services.

**Safety:**
- Use least privilege, secret management, vulnerability scans, dependency checks, and secure configuration management.
- Optimize MTTR with fast fix-forward pipelines.
- Parallelize pipeline work, cache dependencies, optimize scripts, and use lightweight containers.
- Run local, unit, integration, production smoke, user-journey, load, and disaster-recovery tests as appropriate.
- Use Kubernetes rolling updates with 0% unavailability and 25% maximum surge by default.
- Centralize metrics, traces, logs, dashboards, alerts, and SLOs in Datadog.
- Let teams see cross-service telemetry.
- Put new engineers into production deployment early and support them with pairing and onboarding material.

**Don't:**
- Don't impose one review mechanism on every service regardless of criticality.
- Don't optimize mean time between failures at the expense of recovery.

*Ref: Continuous_Deployment.md — "Case Study: AutoScout24"*

---

### 28. OTTO

**Context:**
- Operate a major European ecommerce platform with 60 autonomous Agile teams.
- Achieve more than 60 production deployments per day in the case-study context, with later observation around 100 per day.

**Adoption:**
- Start from long QA cycles and deployments spanning months.
- Optimize mean time to delivery and recovery instead of maximizing time between failures.
- Remove the shared deployment pipeline that serialized all teams.
- Embed QA professionals in product teams.
- Let QA shape testing during planning, automate manual checks with developers, and remove duplicated tests.
- Use feature toggles to separate technical deployment from business release.
- Use trunk-based development and comprehensive automated tests.

**Safety:**
- Use consumer-driven contracts; evolve from fragile JAR-based tests to network-triggered consumer tests.
- Let teams tailor pipelines to service risk.
- Use static analysis only when configuration prevents ignored permanent red states.
- Use unit, component, integration, JavaScript, visual regression, CDC, and production smoke tests.
- Use circuit breakers, aggressive timeouts, and graceful degradation.
- Prefer rolling updates in AWS while keeping database changes backward compatible.
- Use pair or mob programming for the four-eyes principle.
- Keep the pipeline green so fixes can move immediately.

**Don't:**
- Don't make a detached QA team responsible for bugs in systems it cannot influence.
- Don't let asynchronous PR review add days of wait for tiny refactors.

*Ref: Continuous_Deployment.md — "Case Study: OTTO"*

---

### 29. N26

**Context:**
- Operate a regulated digital bank with more than eight million customers in 24 markets at the time described.
- Adopt continuous deployment while moving from a monolith to service-oriented architecture around 2016.

**Regulatory approach:**
- Keep multiple lines of defense.
- Require peer review and traceability from ticket to production.
- Record version, author, reviewer, tests, product request, and promotions.
- Automate compliance and security checks.
- Use declarative GitOps with Kubernetes and ArgoCD.
- Limit the attack surface of automation that can update application manifests.

**Flow and safety:**
- Use short-lived branches and responsive pull requests.
- Pair to make mandatory approval immediate without losing evidence.
- Build container artifacts, promote automatically through environments, and run E2E, security, and health checks.
- Use feature flags to split large work and separate release.
- Complete common service paths in roughly 20–40 minutes in the case study.
- Use unit, integration, component, and E2E tests with regulated execution evidence.
- Use Argo Workflows and blue/green deployment for non-Kubernetes services.
- Define monitoring and alerting as code.
- Permit audited break-glass incident access followed by peer and security review.
- Let junior engineers deploy after initial team onboarding because safeguards apply to every contributor.

**Don't:**
- Don't bypass the four-eyes rule with an overprivileged deployment component.
- Don't confuse regulation with a requirement for manual production promotion.

*Ref: Continuous_Deployment.md — "Case Study: N26"*

---

### 30. ClimatePartner

**Context:**
- Operate diverse climate-action products with about 50 product engineers in six teams and roughly 25 independently deployable units.
- Adopt continuous deployment with a new service-oriented stack during rapid growth in 2020.

**Flow:**
- Push directly to main.
- Run GitHub Actions for build, test, package, and automatic production deployment.
- Identify the application version with the commit SHA.
- Manage infrastructure with Terraform.
- Keep broader infrastructure changes in a separate, reviewable pipeline.
- Run static analysis and coverage checks as nonblocking parallel work in the described implementation.
- Deploy ordinary stories two or three times per pair per day; deploy complex stories more than ten times before completion.

**Safety:**
- Rely on test-driven unit and service coverage.
- Integrate services directly in production.
- Use Datadog golden-signal dashboards and alerts.
- Use rolling updates on ECS/Fargate.
- Use feature toggles for WIP and service toggles for customer module access.
- Use pair programming as the primary review mechanism.
- Omit staging for most systems.
- Isolate production test data by account and explicit test attributes.
- Add staging only when third-party environment and release cycles require it, and deploy staging and production in parallel rather than gating production.
- Pair with junior engineers for their first two or three months.

**Don't:**
- Don't require pull requests merely to imitate review when continuous pairing already provides it.
- Don't keep staging by default when it adds cost and carbon impact without confidence.

*Ref: Continuous_Deployment.md — "Case Study: ClimatePartner"*

---

### 31. Motability Operations

**Context:**
- Support more than 710,000 people with disabilities and their families through mobility services.
- Replace about 95% of legacy software with cloud-first microservices and micro-UIs in the case study.

**Organizational change:**
- Educate Business Risk until continuous deployment is recorded as a release-risk mitigation control.
- Work with Change and Release management to explain small-batch risk reduction and rapid recovery.
- Create a self-documenting pipeline that preserves visibility.
- Replace fragmented Jenkins instances with an orchestrated and then simplified path.
- Add ArgoCD for GitOps.

**Pipeline:**
- Trigger Jenkins from a Bitbucket push.
- Run unit tests, build, SonarQube, and Snyk.
- Build a final image and promote it through Nexus repositories.
- Commit desired state to GitOps repositories.
- Let ArgoCD and OpenShift roll out blue/green pods.
- Run journey automation where required.
- Update Jira, Bitbucket, ownership records, deployment records, and release-note records automatically.
- Trigger the full path approximately 5–25 times per story in the reported implementation.

**Safety:**
- Use unit through UI journey tests plus production synthetic monitoring.
- Use blue/green deployment on OpenShift/Kubernetes/AWS.
- Keep two pairs of eyes through pairing or review.
- Use Dynatrace, Opsgenie, and Splunk.
- Use LaunchDarkly and adopt canary releases.
- Maintain a DevX Path to Prod library with supported, customizable templates.

**Don't:**
- Don't centralize the platform so tightly that teams cannot tailor legitimate differences.
- Don't treat risk stakeholders as opponents; show the controls and evidence.

*Ref: Continuous_Deployment.md — "Case Study: Motability Operations"*

---

### 32. REA Group

**Context:**
- Operate a major Australian property digital platform.
- Begin deployment automation experiments in 2012 and continuous deployment experiments in 2013.
- Make continuous delivery the default and continuous deployment preferred by 2014.
- Formalize “Deploy continuously” as an architectural principle in 2021.
- Report more than 80% of the fleet continuously deployed in the case study.

**Adoption:**
- Use cross-functional pilots with QA and product included from the start.
- Shift quality left and spread pilot learning.
- Use no-blame post-incident reviews.
- Move from SOP documents and ClickOps to scripted deployment.
- Store pipeline configuration as code after learning from pipeline loss.
- Move infrastructure code closer to system code.
- Build internal zero-downtime deployment tooling.
- Create Pact to manage consumer-driven compatibility as reliance on staging decreases.

**Safety and recovery:**
- Run security scans, linting, static analysis, tests, configuration checks, and artifact publication in parallel.
- Use canary or dark launch when appropriate.
- Use red/black deployment with health checks.
- Use feature toggles from internal platform defaults.
- Preserve backward compatibility, API versioning, expand-and-contract, facades, and long-tail consumption monitoring.
- Prefer fast isolated tests and consumer contract tests.
- Correlate requests with transaction IDs.
- Alert on error rates and response times.
- Recover through a known-good build, git revert, or previous-version redeployment.
- Keep mobile delivery on a weekly release train while distributing continuous internal builds to real test devices.

**Don't:**
- Don't require a permanent staging environment when on-demand load testing is sufficient.
- Don't let pipeline configuration become an unrecoverable external artifact.

*Ref: Continuous_Deployment.md — "Case Study: REA Group"*

---

### 33. Maze

**Context:**
- Operate a user-research platform with about 35 engineers across seven teams in the case study.
- Move from Gitflow and weekly releases to trunk-based delivery and several daily releases.
- Replace the final manual trigger by migrating to GitHub Actions.

**Adoption:**
- Require a sequential build/deployment queue for each releasable trunk commit.
- Improve test coverage and flaky acceptance-test stability before removing the gate.
- Validate the new pipeline in staging alongside the old production pipeline.
- Shadow-build with the old pipeline temporarily as fallback.
- Provide on-demand workflows for deploying one service or rolling the whole product back.

**Monorepo flow:**
- Detect changed packages and transitive dependents programmatically.
- Build and deploy only affected packages.
- Use small stacked pull requests and feature flags.
- Run PR checks, require approval, and enter a merge queue.
- Let the queue retest combinations, reject failing PRs, rebase survivors, and squash-merge up to five approved PRs into a commit.
- Serialize trunk releases with a lock.
- Deploy changed services to staging, run acceptance tests, then deploy production.
- Keep a failed release lock so an engineer can restart it before later releases proceed.

**Safety:**
- Deprecate API endpoints and generate schemas to detect breaking changes.
- Run package unit, integration, and endpoint E2E tests plus whole-product browser acceptance tests.
- Reuse the same Docker artifact across environments.
- Use Kubernetes rolling updates with ArgoCD and direct Lambda deployments.
- Use Datadog synthetic monitoring, Watchdog, APM, and RUM.
- Attach deployed version to every telemetry signal.

**Don't:**
- Don't let monorepo size force rebuilding and deploying unaffected services.
- Don't remove manual fallback workflows merely because ordinary deployment is automatic.

*Ref: Continuous_Deployment.md — "Case Study: Maze"*

---

### 34. TravelPerk

**Context:**
- Operate a hyper-growth travel platform with roughly 1,200 employees and more than 350 “builders” in the case study.
- Run web, iOS, and Android clients backed by monoliths and dozens of microservices.
- Adopt continuous deployment around 2017 while moving from Heroku to AWS.

**Flow:**
- Hide long-running work behind flags selectable by user, group, percentage, or company.
- Trigger the complete path for each merged pull request in smaller repositories.
- Run build, lint, type, dependency, format, security, and unit checks.
- Deploy nonproduction and production environments in parallel from main.
- Use merge queues for heavily shared monoliths.
- Batch monolith changes into scheduled deployments every 20 minutes because per-commit deployment volume is unsuitable.
- Produce immutable artifacts and configure environments separately.

**Safety and recovery:**
- Use feature flags, API versioning, field redundancy, and expand-and-contract.
- Use CODEOWNERS and require domain-owner review for sensitive areas.
- Run unit, integration, E2E, contract, visual regression, micro-frontend interoperability, security, and production synthetic tests.
- Use ECS blue/green deployment and backward-compatible database migrations.
- Version frontend assets on S3/CDN for quick rollback.
- Build toward canary frontend delivery and automated rollback tied to synthetic tests.
- Maintain more than 1,000 monitors for HTTP errors, endpoint and query latency, queue congestion, and database resources.
- Connect monitors to incident management and SLOs from endpoints to user workflows.
- Onboard engineers to production contribution within days through buddies and guardrails.

**Don't:**
- Don't insist on per-commit deployment for a monolith when queue density defeats observability and recovery.
- Don't abandon continuous-flow principles; choose the smallest safe batch the architecture can currently support.

*Ref: Continuous_Deployment.md — "Case Study: TravelPerk"*

---

## Anti-Patterns & Common Mistakes

- **Continuous deployment only to staging:** A production human gate still batches commits. → *Fix:* remove the final gate after safety checks earn trust.
- **Long-lived feature branch:** Integration and risk accumulate invisibly. → *Fix:* integrate at least daily and hide behavior in execution branches.
- **Big commit called one-piece flow:** A single VCS object can still contain a huge risky batch. → *Fix:* make commits atomic and demonstrable.
- **Manual blue/green QA:** The inactive environment becomes another queue. → *Fix:* automate regression, smoke, or canary checks.
- **Partial deployment for A/B testing:** Product experiments block unrelated code. → *Fix:* deploy fully and split behavior with runtime flags.
- **Independent feature flags per service:** Cohort assignments drift. → *Fix:* centralize state or propagate one decision.
- **Deeply nested toggles:** Combinations become untestable. → *Fix:* limit nesting and clean up promptly.
- **Permanent release toggle as domain logic:** Business capability is reduced to hidden booleans. → *Fix:* model explicit configuration in the product.
- **Simultaneous contract change:** One executable always updates first. → *Fix:* preserve N/N−1 compatibility.
- **Coordinated “simultaneous” deployment:** A brief failure window remains and batches grow. → *Fix:* expand, migrate, contract.
- **Schema and code in one commit:** Old instances fail against the new schema. → *Fix:* deploy database evolutions separately.
- **Simple column duplication without synchronization:** Writes during migration disappear from the new representation. → *Fix:* trigger, double-write, or double-read.
- **Contracting too early:** Unknown consumers break. → *Fix:* inventory consumers and verify usage before deletion.
- **NoSQL means schemaless:** Readers still depend on shape. → *Fix:* keep read compatibility and plan data migration.
- **Horizontal feature slicing:** Nothing user-valued is testable until every layer finishes. → *Fix:* deliver thin vertical slices.
- **Cross-functional requirements deferred:** Production receives unobservable, insecure, or slow code. → *Fix:* include CFRs in story refinement.
- **Detached QA gate:** Responsibility and context cross a handoff. → *Fix:* embed QA capability in the team.
- **Noisy alerts:** Developers learn to ignore the safety system. → *Fix:* page on meaningful user-visible symptoms.
- **Slow pipeline:** Context fades and commits queue. → *Fix:* parallelize, cache, remove redundant tests, and push checks down the pyramid.
- **Stateful disposable instances:** Deployments lose jobs or sessions. → *Fix:* externalize durable state and use queues.
- **Cold cache ignored:** Frequent replacement degrades latency and overloads dependencies. → *Fix:* evaluate warm-up and external caching trade-offs.
- **Overloaded monolith pipeline:** Continuous deployments become indistinguishable. → *Fix:* split ownership/services or use a justified small scheduled batch.
- **Big-bang release:** All users receive risk and before/after analytics remain confounded. → *Fix:* canary or A/B release through flags.
- **Before/after product experiment:** Seasonality and unrelated events distort attribution. → *Fix:* compare simultaneous randomized cohorts.
- **Experiment backlog:** Hidden code and flags age while waiting. → *Fix:* schedule experiments with delivery and clean up immediately.
- **Manual approval treated as trust:** A person repeats automation without adding signal. → *Fix:* expose evidence and automate the decision.
- **Absolute error prevention:** Human fallibility is denied. → *Fix:* contain blast radius and optimize MTTR.

---

## Decision Heuristics / Checklists

### Continuous Deployment Readiness

- [ ] Can the team deliver and operate the product without routine outside handoffs?
- [ ] Does every contributor integrate at least daily?
- [ ] Is trunk green and deployable?
- [ ] Does every production line receive human review through pairing or pull request?
- [ ] Are static, security, and dependency checks automated?
- [ ] Does the test strategy cover critical behavior at several layers?
- [ ] Are legacy critical paths protected by characterization or black-box tests?
- [ ] Is production rollout zero downtime?
- [ ] Are N and N−1 compatible during rollout?
- [ ] Are logs, metrics, traces, dashboards, and alerts maintained?
- [ ] Can the team detect user-visible failure quickly?
- [ ] Can the team toggle off, route back, revert, or fix forward quickly?
- [ ] Does the manual gate catch defects automation still misses?
- [ ] Do stakeholders understand the safeguards and recovery path?
- [ ] Does the manual gate now feel redundant rather than lifesaving?

### Per-Change Deployment Safety

- [ ] Is the commit atomic and self-contained?
- [ ] Is incomplete behavior hidden before code reaches trunk?
- [ ] Is the outermost toggle OFF by default?
- [ ] Is each changed contract backward compatible?
- [ ] Is the provider available before an unhidden consumer uses it?
- [ ] Is every database evolution in a separate deployment?
- [ ] Is transition data synchronized continuously?
- [ ] Are automated tests green at the agreed layers?
- [ ] Are security and dependency checks green?
- [ ] Are performance implications understood?
- [ ] Are required telemetry and alerts included?
- [ ] Are readiness and health checks meaningful?
- [ ] Is production capacity sufficient throughout rollout?
- [ ] Is the recovery action known before deployment?
- [ ] Is the deployment version visible in telemetry?

### Feature Toggle Choice

- [ ] Use a runtime toggle for a new visible feature.
- [ ] Use a runtime toggle when immediate disablement matters.
- [ ] Use a runtime toggle for production exploration, canary release, or A/B testing.
- [ ] Use expand-and-contract for ordinary live refactoring.
- [ ] Use a refactoring toggle only when runtime rollback or gradual traffic adds justified safety.
- [ ] Use a nested toggle only when the increment needs an independent release.
- [ ] Put the toggle at the outermost behavior divergence.
- [ ] Define test cohorts and every meaningful state combination.
- [ ] Create cleanup work before release.
- [ ] Replace permanent business toggles with domain configuration.

### Deployment Strategy Choice

- [ ] Use rolling deployment when one fleet and mixed-version compatibility are acceptable.
- [ ] Use blue/green when rapid traffic switch-back justifies duplicate capacity.
- [ ] Use canary deployment when real-traffic technical comparison justifies complexity and delay.
- [ ] Use a feature-flag canary release for gradual user exposure after code is fully deployed.
- [ ] Never use partial deployment as a manual release gate.
- [ ] Require N/N−1 compatibility for every strategy.

### Database Migration Choice

- [ ] Use a database trigger when database-side synchronization is acceptable.
- [ ] Use double-write when application write duplication is simpler to test and observe.
- [ ] Use double-read when fallback reads simplify migration.
- [ ] Backfill only after future writes cannot recreate the deprecated gap.
- [ ] Add strong constraints only after current and future data satisfy them.
- [ ] Contract only after every reader, writer, and foreign key migrates.
- [ ] For NoSQL, choose permanent migrate-on-read, convert-on-write, or a background batch based on mutability and data lifetime.

### Recovery Choice

- [ ] Toggle OFF first when only released behavior is faulty.
- [ ] Stop percentage ramp when exposure is still partial.
- [ ] Route back in blue/green when the old environment and data remain compatible.
- [ ] Revert the commit when ordinary deployment can safely restore source behavior.
- [ ] Fix forward when the issue is understood and the pipeline is fast.
- [ ] Deploy diagnostics when evidence is insufficient.
- [ ] Treat database changes separately from application rollback.
- [ ] Follow every incident with a blameless safety-net improvement.

### Error-Budget Use

- [ ] Define the continuous-flow SLO explicitly if the team uses one.
- [ ] Reserve the budget for rare changes that cannot yet be automated safely.
- [ ] Stop unrelated commits during a pause.
- [ ] Measure the impact on deployment/commit ratio.
- [ ] Restore the automated path immediately after the exception.
- [ ] Investigate recurring budget consumption as missing automation or architecture work.

---

## Key Takeaways

1. Remove the final manual production gate only after the continuous-delivery safety net is credible.
2. Make one small commit flow to one production deployment.
3. Reduce transaction cost before demanding one-piece flow.
4. Optimize deployment frequency, lead time, change failure rate, and MTTR together.
5. Separate deployment from release through runtime control.
6. Integrate at least daily; prefer trunk-based development and continuous review.
7. Hide unfinished work in execution branches, not long-lived source branches.
8. Use runtime feature toggles for new features and progressive delivery.
9. Use expand, migrate, contract for live refactoring.
10. Preserve N/N−1 compatibility across every API, message, browser, cache, and database boundary.
11. Deploy schema evolutions separately from application changes.
12. Prevent migration data loss with a trigger, double-write, or double-read.
13. Use blue/green, rolling, or canary deployment according to actual trade-offs.
14. Keep instances stateless, replaceable, quick to start, and safe to stop.
15. Slice work vertically into thin user-valued increments.
16. Include deployability, testability, observability, security, and performance in each story.
17. Add new features outside-in under a toggle.
18. Refactor multilayer systems inside-out with nested expand-and-contract cycles.
19. Test guarded behavior in production because staging cannot reproduce production.
20. Use canary releases for risk and A/B tests for product hypotheses.
21. Coordinate feature state across distributed systems.
22. Keep alerts actionable and centered on user-visible symptoms.
23. Optimize recovery through toggle-off, route-back, revert, or fix-forward.
24. Use the continuous-flow error budget for rare exceptions, not routine batching.
25. Build stakeholder trust with transparent evidence rather than repeated manual approval.
26. Let junior engineers use the same safe production path as everyone else.
27. Accept contexts where continuous deployment is unsuitable or must be scoped.
28. Treat cultural change—autonomy, embedded QA, shared ownership, and blameless learning—as core implementation work.

---

## Cross-References

- Related: [[../Modern_Software_Engineering_Doing_What_Works_to_Build_Better_Software_Faster_-_David_Farley.md]]
- Related: [[../The_DevOps_Handbook.md]]
- Related: [[../Lean_Enterprise_How_High_Performance_Organizations_Innovate_at_Scale.md]]
- Related: [[../Building_Evolutionary_Architectures_2nd_edition.md]]
- Related: [[../Observability_Engineering_2nd_Ed_ER_-_Charity_Majors.md]]
- Topic index: [[../INDEX.md]]
