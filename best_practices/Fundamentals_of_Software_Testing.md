# Fundamentals of Software Testing, 2nd Edition
**Author:** Bernard Homes
**Publisher:** Wiley / ISTE (Computer Engineering Series) — ISTQB CTFL-aligned
**Topic tags:** `#testing` `#test-management` `#test-design` `#test-levels` `#static-testing` `#risk-based-testing` `#defect-management` `#test-tools` `#istqb`
**Language focus:** Language-agnostic (no implementation-language bias; few small C snippets for coverage illustration)
**Sources:** `markdown_output/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md` · `summaries/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md`

## TL;DR
A ISTQB Foundation-level reference covering the full testing lifecycle: the seven enduring principles of testing, the test process (planning → analysis → design → implementation → execution → completion), four test levels (component, integration, system, acceptance), four test types (functional, nonfunctional, structural, change-related), static techniques (reviews and static analysis), black-box/white-box/experience-based test design techniques, test management (planning, estimation, entry/exit criteria, monitoring), risk-based testing, defect management, and tool selection. Testing shows the *presence* of defects, never their absence; exhaustive testing is impossible, so all testing is risk-based prioritization.

---

## Best Practices by Topic

### The Seven Principles of Testing

**Principle:** These seven principles apply to *every* test project regardless of environment, methodology, or technology.

| # | Principle | Practical implication |
|---|-----------|------------------------|
| 1 | **Testing shows the presence of defects, not their absence** | Passing tests never proves correctness. Tests only reduce the risk of residual defects. |
| 2 | **Exhaustive testing is impossible** | Reduce test count via risk-based selection. Testing is risk-mitigation activity. |
| 3 | **Early testing ("shift-left")** | Cost of a defect grows ~10× per phase: design=1, coding=10, system test=100, production=1000. Find defects early via reviews and static analysis. |
| 4 | **Defect clustering** | A small number of modules/components contain most defects (Pareto). When you find one defect, look for more in the same area. |
| 5 | **Pesticide paradox** | Re-running identical tests stops finding new defects. Revise tests, vary data and execution order. (Regression tests are the exception — they detect side-effects.) |
| 6 | **Testing is context dependent** | Safety-critical ≠ e-commerce ≠ video game. Re-evaluate tests as the software and its context evolve; don't blindly reuse test plans from other projects. |
| 7 | **Absence-of-errors fallacy** | A defect-free system that solves the wrong problem is still a failure. Validate against user needs, not just specifications. |

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.3 Paradoxes and main principles" / "1.3.1"–"1.3.7"*

---

### Test Process — Activities and Testware

**Principle:** Testing is not just execution. It comprises seven grouped activities, repeated at every test level and every iteration:

1. **Test planning** — objectives, scope, resources, schedule, risks, entry/exit criteria → *test plan(s), risk register*.
2. **Test monitoring and control** — compare actual vs planned progress; take corrective actions → *test reports, defect statistics*.
3. **Test analysis** — study test basis (contracts, specs, design, risks, standards); identify test conditions, priorities, testability → *test conditions, traceability, test charters*.
4. **Test design** — derive test cases from conditions; identify test data and environment needs → *test cases, test data design, infrastructure list*.
5. **Test implementation** — sequence cases into procedures/suites; build or automate; finalize concrete data and expected results → *test suites, schedule, test environment*.
6. **Test execution** — run cases, compare actual vs expected, log incidents, re-execute on fixes (confirmation + regression) → *pass/fail status, defect reports, versioned logs*.
7. **Test completion** — confirm exit criteria met; capture lessons learned; archive testware → *summary report, archived testware*.

**Do:**
- Maintain **bidirectional traceability**: test basis ↔ test conditions ↔ test cases ↔ execution ↔ defects. This is the only way to do meaningful impact analysis when requirements change.
- Tailor the process to context — safety-critical software requires far more rigor than an internal tool.
- Treat integrity level (catastrophic → negligible) as the driver for depth/breadth of testing and documentation.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.4 Test activities, testware and test roles"*

---

### Terminology — Error / Defect / Failure

| Term | Meaning |
|------|---------|
| **Error / Mistake** | A human action that produces an incorrect result. |
| **Defect / Fault / Bug** | A flaw in a component or system that can cause it to fail. |
| **Failure** | A deviation of the system from its expected behavior. |
| **Test basis** | Body of knowledge used as the basis for test analysis/design (contracts, specs, code, risks, standards). |
| **Test case** | Preconditions + inputs + actions + expected results + postconditions. |
| **Test condition** | An item/event that could be verified by one or more test cases. |
| **Test oracle** | Source for determining expected results (specs, existing system, heuristics, expert judgment). |

> Testing identifies *failures*; debugging locates and fixes the *defects* that caused them. The two are distinct activities.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.1.5 Terminology" / "1.2.4 Test and debugging"*

---

### Test Levels

**Principle:** Four canonical test levels, each with its own test object, objective, basis, entry, and exit criteria. Apply them in every model (sequential, iterative, agile) — the granularity changes, the goals don't.

#### Component (Unit) Testing
- **Object:** components, modules, functions, classes, SQL requests.
- **Objective:** detect failures in individual units; verify functional and nonfunctional behavior.
- **Basis:** detailed specifications, source code, algorithms.
- **Techniques:** white-box (instructions, branches) + black-box (interface-based).
- **Special note:** often run by developers with source access; defects frequently fixed without entering the defect-tracking system → distorts defect-per-component stats.

#### Integration Testing
- **Object:** interfaces between components, infrastructure, DB, file systems.
- **Objective:** detect failures in interfaces and data exchanges.
- **Integration strategies:**
  - **Big bang** — all components at once. No stubs/drivers needed but isolating root cause is hellish.
  - **Bottom-up** — start with low-level components; needs drivers.
  - **Top-down** — start with high-level; needs stubs.
  - **Sandwich** — combines top-down + bottom-up.
  - **Functional / neighborhood / backbone** — group by functional or technical proximity.

#### System Testing
- **Object:** complete integrated system + documentation + install scripts.
- **Objective:** detect end-to-end failures; verify the system meets requirements; validation (user needs), not just verification (spec compliance).
- **Environment:** as close to production as possible.
- **Run by:** independent test team.

#### Acceptance Testing
- **Objective:** obtain user/customer acceptance; build confidence (defect-finding is a by-product, not the goal).
- **Types:**
  - **UAT** — by end users.
  - **Operational acceptance** — backup/restore, recovery, user mgmt, security, data migration, maintenance tasks.
  - **Contractual / Regulatory** — verify contract or regulatory requirements (FDA, FAA, DoD).
  - **Alpha** — at developer's site, by potential users.
  - **Beta** — at user sites, before general release.
  - **Pilot** — limited rollout to adapt user processes.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.2 Test levels and test types" / "2.2.1"–"2.2.5"*

---

### Test Types

| Type | Focus | When |
|------|-------|------|
| **Functional** | What the system *does* (completeness, correctness, appropriateness per ISO 25010). | All levels. |
| **Nonfunctional** | *How well* it performs: reliability, compatibility, usability, performance efficiency, maintainability, portability, security. | All levels — **don't defer to end of system test**. |
| **Structural (white-box)** | Architecture/structure of the software: instructions, branches, call graphs, frequency of calls. Measure as *coverage*. | All levels; granularity varies. |
| **Change-related** | **Confirmation (retest):** verify a specific defect was fixed. **Regression:** verify the fix/change introduced no side-effects elsewhere. | All levels, especially during maintenance. |

**Do:**
- Run nonfunctional tests *alongside or before* functional tests — root causes of perf/security issues are often architectural and require early redesign.
- Use impact analysis (call-graph, data-flow, control-flow) to focus regression tests on potentially affected components.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.3 Types of tests"*

---

### Static Testing — Reviews

**Principle:** Static testing evaluates work products *without executing* them. Finds defects early when they're cheapest to fix; cost-effective vs. dynamic testing.

**IEEE 1028-2008 / IEEE 20246-2017 review types (least → most formal):**

| Type | Led by | Purpose | Formalism |
|------|--------|---------|-----------|
| **Informal** (pair, buddy, peer desk-check, author check) | Anyone | Quick feedback, problem-solving | No formal process; results may be undocumented. |
| **Walkthrough** | Author | Educate audience; find anomalies; evaluate alternatives; check conformance. | Author presents; scribe records; little preparation. |
| **Technical review** | Moderator (not author) | Technical evaluation; suitability for use; conformance to standards. | Peers + technical experts; preparation required; report issued. |
| **Inspection** | Trained moderator | Find defects (not fix them); collect metrics; entry/exit criteria. | Most formal; checklists; defined roles; metrics-driven. |
| **Management review** | Manager | Progress, plan status, process efficiency. | Focus on conformance to plans. |
| **Audit** | Independent auditor | Conformance to standards, contracts, regulations. | Independent evaluation. |

**Review roles:** manager, moderator (leader), author, reviewer (inspector), scribe (recorder).

**Phases of a formal review:** Planning → Kick-off → Individual preparation → Review meeting → Rework → Follow-up.

**Success factors:**
- Clear objectives; right people; defects found in *preparation*, not just in the meeting.
- Constructive (non-adversarial) atmosphere.
- Management support; metrics collected and used to improve.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "3.2 Review process"*

---

### Static Testing — Static Analysis

**Principle:** Tool-based analysis of code (or documents) without execution. Detects defects that human review misses.

**Categories of defects identified:**
- Variables read before being written; written but never read.
- Unreachable code ("dead code").
- Cyclomatic complexity / nesting depth above threshold.
- Coding-standard violations.
- Security vulnerabilities (buffer overflows, injection risks).
- Duplicate code.

**Control flow analysis** — finds unreachable code, infinite loops, structural issues.

**Data flow analysis** — tracks variable lifecycle: **d**efined / **u**sed / **k**illed.
- Valid pairs: `~d`, `du`, `uu`, `uk`, `kd`, `dd`.
- Suspicious: `ud` (used then defined).
- **Incorrect:** `~u` (used before existing), `ku` (killed then used).
- Note: distinguish global / public / private scope; same name can refer to different memory areas.

**Code:**
```c
#include <stdio.h>
main() {
  int x;             // x is uninitialized
  printf("%d", x);   // content is random — defect caught by data-flow analysis
}
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "3.3 Static analysis" / "3.3.3 Data flow analysis"*

---

### Black-Box Technique — Equivalence Partitioning (EP)

**Principle:** For each variable, divide the input/output domain into classes where all values are processed identically. Test one representative per partition. Reduces test count without losing functional coverage.

**Do:**
- Identify **valid** partitions (correct results) and **invalid** partitions (failures / errors).
- Sub-divide by interaction with other variables — e.g., days of month: `1–28`, `29`, `30`, `31`, plus invalid (`<1`, `>31`, non-numeric, empty, non-integer).
- Pick a representative per partition for valid; combine one invalid with all other valid (so the expected error message is unambiguous).
- Apply to input, output, internal, alphanumeric, and time-related variables.

**Don't:**
- Don't combine multiple invalid partitions in one test — you won't know which one triggered the error.
- Don't make partitions too coarse (misses defects) or too fine (combinatorial explosion).

**EP table example (calendar date):**

| Input | Valid partitions | Invalid partitions |
|-------|------------------|--------------------|
| Day | 1–28; 29; 30; 31 | <1; >31; non-numeric; empty; non-integer |
| Month | 1,3,5,7,8,10,12; 2; 4,6,9,11 | <1; >12; non-numeric; empty |
| Year | 1582–9999; leap years; non-leap ×100; leap ×100 | <1582; >9999; non-numeric; empty |

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.1 Equivalence partitioning"*

---

### Black-Box Technique — Boundary Value Analysis (BVA)

**Principle:** Defects cluster at the edges of equivalence partitions. Test the boundary value and the smallest increment on either side.

**Do:**
- Two coverage levels:
  - **Weak:** boundary value + smallest increment *inside* the partition.
  - **Strong:** also test smallest increment *outside* (i.e., in invalid partitions).
- Apply to loop boundaries (first and last iteration), array indices (0-based vs 1-based!), numeric type limits (`MININT`/`MAXINT`), field sizes, screen/window dimensions.
- Catches: wrong relational operators (`<` vs `<=`), off-by-one errors, incorrect variable types/sizes.

**Don't:**
- Don't apply BVA to Boolean or finite enumerations — EP handles those.
- Don't run BVA on partitions you haven't first correctly identified via EP.

**Code — typical BVA target:**
```c
if (a = b) or (c > d) then y = x + 2     // two conditions — apply BVA per condition
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.2 Boundary value analysis"*

---

### Black-Box Technique — Decision Tables

**Principle:** Model business rules as a table of conditions × actions. Captures combinations of conditions that EP/BVA (which test variables in isolation) cannot.

**Steps:**
1. Identify conditions and their partitions.
2. Compute total combinations (Cartesian product).
3. Fill the table; identify the resulting action per column.
4. Reduce: merge columns where conditions are impossible or irrelevant; use `–` (don't care); track *weight* per column.
5. Verify combination coverage (sum of weights = original combination count).
6. Identify ambiguous/undefined actions → escalate to stakeholders.

**Reduced decision table example (driving authorization in France):**

| | 01 | 09 | 10 | 12 | 14 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|
| Age (A:<16, 16<B<18, C:18) | A | B | B | B | – | C | C | C | C | C |
| Theory OK? | – | – | Y | Y | N | Y | Y | Y | Y | N |
| Accompanying driver? | – | – | Y | N | – | Y | Y | N | N | – |
| License obtained? | – | Y | N | N | N | Y | N | Y | N | Y |
| Driving authorized? | N(a) | N(b) | Y | N | N(d) | Y | Y | Y | N | N(c) |
| **Weight** | 8 | 4 | 1 | 1 | 4 | 1 | 1 | 1 | 1 | 2 |

Weights sum to 24 = original 3×2×2×2 combinations.

**When to use:** complex business logic; insurance/premium calculators; eligibility rules. Can model hundreds of columns for aerospace/finance.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.3 Decision tables" / Table 4.2 / 4.3*

---

### Other Combinational Techniques

- **N-tuples (pairwise) testing** — assumes defects come from interactions of n (usually 2) values; reduces combinatorial explosion.
- **Orthogonal arrays** — statistical selection of data vectors; covers all partitions with limited cases, but doesn't guarantee every value pair is tested.
- **State transition testing** — model the system as finite state machine; test valid + invalid transitions; coverage levels: all-states, all-transitions, all-transition-pairs (n-switch).
- **Use case testing** — test scenarios from end-to-end actor-system interactions; main path + alternatives.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.4 Other combinational techniques" / "4.3.5 State transition testing"*

---

### White-Box Techniques — Coverage Hierarchy

**Principle:** Coverage measures how thoroughly the code's structure has been exercised. Each stronger level subsumes the weaker ones.

| Coverage type | Definition | Strength |
|---------------|-----------|----------|
| **Statement (instruction)** | Every executable statement run ≥ once. | Weakest — 100% does *not* imply all branches tested. |
| **Decision (branch)** | Every decision's true and false outcomes taken. | Stronger — implies 100% statement. |
| **Condition** | Each Boolean condition takes both T and F. | Independent of decision coverage. |
| **Decision/Condition** | Both combined. | |
| **MC/DC** (Modified Condition/Decision Coverage) | Each condition independently affects the decision outcome. | Required for safety-critical (DO-178B Cat A, medical, automotive). |

**Coverage code samples (C):**
```c
int factorial(int x) {
  int result = -1;
  if (x >= 0) {            // decision
    result = 1;
    for (int i = 2; i <= x; i++) {   // loop decision
      result = result * i;
    }
  } else {
    // empty branch — still must be covered for 100% decision coverage
  }
  return result;
}
```
- 100% instruction coverage with minimum tests: `(-2,-1), (0,1), (4,24)` (three pairs).
- 100% decision coverage also requires exercising the `for` loop's false branch (e.g., `x = 0` or `x = 1`).

**Decisions ≠ just `if`:** also `while`, `until`, `for–next`, `case–of`. Conditions include XOR and AND with identical results.

**Exit-criteria examples:** "100% decision coverage reached"; "all Cat A/B code paths covered by MC/DC."

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.4 Structure-based techniques" / Ref. Questions 66–70*

---

### Experience-Based Techniques

**Principle:** Use tester expertise, defect history, and exploratory skill when systematic techniques are infeasible or insufficient.

- **Attacks (Whittaker):** target the software via its interfaces — UI (force error messages, default values, buffer overflows, repeat inputs, refresh), data/computation (overflow storage, recursive calls, invalid operators), system interfaces (fill device, corrupt files, inject OS faults).
- **Defect taxonomies (Kaner):** categorized lists of known defect types (UI, exception handling, boundary/concurrency, computational, control-flow, data interpretation, load/stress, version/config, hardware/network) — keep the taxonomy updated with new findings.
- **Error guessing / ad hoc:** unstructured guessing by the tester. **Not recommended** as a primary method.
- **Exploratory testing (Bach/Whittaker):** *simultaneous learning, test design, and test execution.* Tester adapts based on observations.
  - Session-based (60–90 min) with a **charter** defining scope, risks, target defects, and tactics.
  - Debrief with the test manager: report defects, identify aspects needing further exploration, give a reliability read.
  - Use when: time-constrained, no detailed traceability needed, defect clustering is observed.

**Don't:**
- Don't rely on exploratory testing as a *replacement* for systematic techniques — it cannot *prevent* defects, only find some.
- Don't skip documenting findings — failures must be reproducible.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.5 Experience-based technique"*

---

### Collaboration-Based Test Approaches

**Principle:** Avoid defects via collaboration rather than only detecting them after the fact.

- **User stories with the 3 C's:** **C**ard (the story), **C**onversation (how it's used), **C**onfirmation (acceptance criteria). Gherkin/`Given-When-Then` formalizes acceptance criteria.
- **ATDD / BDD / TDD** — test-first approaches shift testing into design.
- **INVEST principles** for user stories: Independent, Negotiable, Valuable, Estimable, Small, Testable.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.6 Collaboration-based test approaches"*

---

### Test Organization — Independence Levels

**Principle:** Some independence between testers and developers improves defect detection, but each level has trade-offs.

| Level | Description | Pros / Cons |
|-------|-------------|-------------|
| 0 | Developers test their own code | Fast; biased ("author as judge"); misses defects. |
| 1 | Peer in same team (pair programming, peer review) | More defects found than L0; dev background only. |
| 2 | Specialized tester embedded in dev team (agile/Scrum) | Test expertise in-team; risk of co-optation into dev tasks; isolated skill growth. |
| 3 | Independent test team in same org, separate reporting line | Independence + coaching/career path; risk of communication gap with dev. |
| 4 | External test org / consultancy | Highest independence; risks: knowledge drains away, contract interfaces. |

**Roles:** test manager (planning, control, reporting), test analyst (design, analysis), test automator (framework/scripts), test technician (execution, logging), technical specialists (DB, UX, security, performance, configuration management).

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.1.1 Independence levels"*

---

### Test Planning & Estimation

**Do:**
- Define **test policy** (org-level), **test strategy** (project-level approach), **master test plan**, **level test plans**, test design specs, test case specs, test procedure specs, test logs, test reports.
- Choose a test approach: *analytical, model-based, methodic/standard-compliant, dynamic/heuristic (exploratory), consultative, regression-adverse.*
- Estimate via **expert-based**, **metrics-based** (historical data), or **algorithmic** methods.
- Prioritize: validate the "happy path" first, then critical, major, then important based on risk analysis.
- Use smoke tests on each delivery to verify basic functionality before deeper testing.

**Don't:**
- Don't use "planned test termination date" or "planned effort spent" as exit criteria — they say nothing about quality.
- Don't use "all tests executed without finding defects" — it incentivizes weak tests.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2 Test planning and estimation"*

---

### Entry, Exit, and Resumption Criteria

**Entry criteria** (when testing can start): test basis available and stable; test object of acceptable quality (previous exit criteria met); environment/harness/drivers/stubs ready; resources, tools, scripts, test data available.

**Resumption criteria** (after an interruption): delivery notice present; no uncontrolled changes; open defects below threshold (e.g., <50); defect-review cadence in place (e.g., twice weekly).

**Exit criteria** (when testing is complete):
- Coverage targets met (statements, branches, MC/DC, requirements, risks).
- All planned tests executed on the release-candidate version.
- All "must-fix" defects fixed and confirmation/regression tested.
- Test metrics indicate product stability/reliability.
- Stakeholder sign-off.

**Sample system-test exit criteria (Rex Black):**
1. No design/code/characteristic changes in last 3 weeks except defect fixes.
2. No crashes or unexplained process terminations on any server in last 3 weeks.
3. No client rendered unusable by a failed update during system test.
4. All planned tests run on the release candidate.
5. All "must-fix" defects resolved.
6. All defects closed or formally deferred (and verified where applicable).
7. Metrics show stability, completeness, adequate coverage of critical risks.
8. Product management accepts that the product meets reasonable customer expectations.
9. End-of-phase review meeting held and signed off.

**Don't:**
- Don't have entry/exit/SLA criteria you don't enforce — that's worse than having none.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.4 Entry and exit criteria for test activities"*

---

### Test Monitoring, Control & Reporting

**Metrics to track:**
- Test progress % (planned vs actual).
- Coverage: requirements, risks, code, conditions, test cases designed/executed.
- Defect statistics: detection/fix trends, defects per module, age, reopen rate, defect detection percentage (DDP).
- Subjective quality evaluation by testers.
- Cost/risk trade-off to prioritize coverage of highest risks.

**Reading defect curves:** vertical gap between opened and closed defect curves = open backlog; horizontal gap = average time-to-fix. A diverging trend or plateau in detection suggests blocking issues or a need for new techniques.

**Report by audience:** testers need workload + coverage; developers need defects per module + delivery dates; managers need milestones, effort variance, risk evolution; customers need delivery dates + scope changes.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.3 / 5.4"*

---

### Risk-Based Testing

**Principle:** Risk = Impact × Likelihood. Classify, prioritize, and respond to risks; allocate test effort proportionally. Risks come in two flavors:

- **Product risks** — software fails to perform; security holes; perf/reliability issues. → Mitigate via testing.
- **Project risks** — schedule, scope, staffing, supplier, tooling, organizational issues that threaten delivery. → Mitigate via planning, contingency, escalation.

**Risk likelihood scale (Table 5.1):** Critical ≥90%, High 60–90%, Average 30–60%, Low 0–30%.

**Impact severity (cost / performance / planning):** Critical / High / Average / Low (Table 5.2).

**Risk priority number (RPN):** 1–16 matrix of likelihood × severity; group into CAT I (1–2), CAT II (3–6), CAT III (7–12), CAT IV (13–16). CAT I is escalated to upper management.

**Four responses to a risk:** accept / mitigate (reduce probability) / contain (reduce impact via safeguards) / transfer (insurance, contract, escalation).

**Risk identification techniques:** brainstorming; FMEA/FMECA; fault tree analysis; hazard analysis; "Hyperspace of danger."

**Do:**
- Re-evaluate risks periodically (e.g., top-10 risks every period); track evolution.
- Tie traceability to *risks*, not just requirements — every test should cover a requirement or a risk.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.6 Risk management"*

---

### Defect Management

**Principle:** Defects have a lifecycle; not all defects get fixed (impact/priority/cost trade-off). Link user-support tools to defect management to catch field-escaped defects and feed process improvement.

**Three lifecycle phases (IEEE 1044-1993):**
1. **Recognition** — assert reality, assess causes and impact.
2. **Action** — decide what to do (fix, defer, reject).
3. **Disposal** — closure steps.

**Classification criteria:** impact on users (criticality/severity), effort to fix, component of origin, type (per defect taxonomy), priority/urgency.

**Mandatory fields in a defect report (per IEEE 829):** identifier, summary, inputs, expected results, actual results, anomalies, date/time, procedure step, environment, attempts to repeat, tester, observers, impact, urgency assessment, status, conclusions/recommendations.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.7 Defect management"*

---

### IEEE 829 Test Documentation Templates

**Test plan (IEEE 829-1998):** identifier; introduction; test items; features to be tested; features *not* to be tested; approach; pass/fail criteria; suspension/resumption; deliverables; testing tasks; environmental needs; responsibilities; staffing/training; schedule; risks; approvals.

**Test design spec:** identifier; features to be tested; approach refinements; test identification; feature pass/fail criteria.

**Test case spec:** identifier; test items; input specifications; output specifications; environmental needs; special procedural requirements; intercase dependencies.

**Test procedure spec:** identifier; purpose; special requirements; procedure steps.

**Test log:** identifier; description; activity and event entries.

**Defect (incident) report:** identifier; summary; incident description (inputs, expected, actual, anomalies, date/time, procedure step, environment, attempts to repeat, testers, observers); impact.

**Test summary report:** identifier; summary; variances; comprehensive assessment; summary of results; evaluation; summary of activities; approvals.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.2–8.8 (IEEE 829 templates)"*

---

### Test Tools — Categories

| Category | Examples |
|----------|---------|
| Test management | Planning, scheduling, tracking |
| Defect management | Logging, tracking, reporting |
| Configuration management | Version control of testware |
| Requirement management | Traceability, coverage analysis |
| Static analysis | Code quality, security |
| Review platforms | Collaborative review |
| Test design | Generating cases from models |
| Test data generation | Synthetic data |
| Test execution (automation) | Capture/replay, unit frameworks (JUnit, NUnit, pytest), performance, security |
| Environment management | Provisioning, virtualization, containers |
| Coverage measurement | Statement/branch/path coverage |
| Comparison | File/DB actual vs expected |

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "6.1 Types of test tools"*

---

### Test Tools — Automation Strategy

**Three families of test-execution automation:**
1. **Record/replay** — script per data set; massive maintenance on any UI change.
2. **Data-driven** — separate script from data files; loop over data sets; compare actual vs expected.
3. **Keyword-driven** — abstract UI into business-action keywords; functional testers compose scenarios without code; technical testers maintain keyword→script mappings.

**Advantages of tools:** reduced repetitive manual work; reliability/repeatability; ability to simulate load/complex environments; metrics; objective coverage measurement; faster reporting.

**Risks of tools:**
- Underestimating training/coaching/maintenance effort.
- **Probe effect** — instrumentation changes the measured behavior (e.g., recorder consumes bandwidth).
- Unrealistic expectations; over-confidence in vendor claims.
- Tool/script/data version-management gaps.
- Vendor bankruptcy or buyout; lack of interoperability; restrictive open-source licenses.

**Selection process:**
1. Evaluate org maturity and expected benefits (cost/benefit short-mid-long term).
2. Pre-select via research, forums, conferences, ISTQB national boards (beware hidden vendor affiliations).
3. Run a **proof of concept** in your own environment; evaluate all candidates against the same weighted criteria.
4. Pilot project → lessons learned → incremental generalization project-by-project.

**Build vs. Buy:**
- Open-source: low initial cost; restrictive licenses; weak support; you maintain it.
- Commercial: expensive initial + yearly maintenance; longer-term support; vendor risk.

*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "6.2 / 6.3"*

---

## Anti-Patterns & Common Mistakes

- **Equating testing with debugging:** testing finds failures; debugging locates and fixes the causing defect. They are distinct activities.
- **Believing "tests pass = no defects":** Principle 1 — testing shows presence, never absence.
- **Trying to test everything:** Principle 2 — exhaustive testing is impossible; everything must be risk-prioritized.
- **Deferring all testing to the end:** Principle 3 — cost of defect grows ~10× per phase; shift left.
- **Ignoring defect clustering:** Principle 4 — if one module is buggy, expect more there.
- **Re-running the same stale regression suite forever:** Principle 5 — pesticide paradox; refresh data and techniques.
- **Applying one-size-fits-all tests across projects:** Principle 6 — context dependence.
- **Treating low defect count as success:** Principle 7 — the system might solve the wrong problem.
- **Big-bang integration:** isolating root cause among hundreds of new interfaces is brutal.
- **Mixing valid + invalid partitions in one test:** ambiguous error attribution.
- **Statement coverage as proof of completeness:** 100% statement ≠ 100% decision; safety-critical needs MC/DC.
- **Cosmetic exit criteria** (date reached, budget spent, "no new defects found") — they measure nothing about quality.
- **Unenforced entry/exit criteria or SLAs:** worse than none.
- **Treating tools as silver bullets:** ignore training, maintenance, probe effect, vendor risk.
- **Production data copied as test data unmodified:** confidentiality/privacy breaches (GDPR/CNIL); anonymize.
- **Reusing test plans verbatim across projects:** violates context dependence.

---

## Decision Heuristics / Checklists

**Choosing a test design technique:**
1. *Type of system* — safety-critical → MC/DC + formal reviews; e-commerce → EP/BVA + exploratory.
2. *Documentation available* — good specs → black-box; sparse → experience-based.
3. *Risk level* — higher → more thorough (decision tables, state transition, MC/DC).
4. *Time/budget* — tight → exploratory + pairwise; generous → systematic.
5. *Tester experience* — senior → exploratory/attacks; junior → scripted black-box.
6. *Combinatorial complexity* — many interacting variables → decision tables or pairwise.
7. *Stateful behavior* — finite state machine → state transition testing.

**Coverage-level exit-criteria checklist:**
- What coverage type is required (statement / decision / condition / MC/DC)?
- What's the regulatory minimum (e.g., DO-178B Cat A = MC/DC)?
- Have I correctly identified all decisions (`if`/`while`/`until`/`for`/`case`) and conditions (including XOR, AND, NOT)?
- Does the residual uncovered code represent genuinely unreachable/dead code, or untested paths?

**Risk response decision tree:**
- Probability × Impact = RPN ≥ CAT I/II → mitigate or contain actively, escalate to management.
- High impact, low probability → contingency plan (safeguards).
- Low impact, low probability → accept and monitor.
- Legal/contractual → transfer (insurance, EULA).

**Review type selection:**
- Quick sanity / learning → informal / pair / buddy.
- Educate team on a doc → walkthrough.
- Evaluate technical fitness → technical review.
- Defect hunting in safety/regulated code → inspection (with metrics).
- Conformance to contracts/standards → audit.

**Tool selection checklist:**
- Define the problem before the tool.
- Evaluate org test-process maturity first.
- Short-list via multiple independent sources.
- Run a proof of concept in your environment.
- Score candidates against pre-weighted criteria.
- Pilot → lessons learned → generalize incrementally.

---

## Key Takeaways

1. **Seven principles govern all testing** — presence-not-absence, impossibility of exhaustive testing, early testing, defect clustering, pesticide paradox, context dependence, absence-of-errors fallacy.
2. **Testing is a process, not an event** — seven activities from planning to completion, repeated at every level and iteration, with bidirectional traceability throughout.
3. **Four test levels** (component, integration, system, acceptance) and **four test types** (functional, nonfunctional, structural, change-related) compose the test space.
4. **Static testing (reviews + static analysis) finds defects earliest and cheapest** — shift left.
5. **Black-box techniques** (EP, BVA, decision tables, state transition, use case) provide systematic, specification-based coverage.
6. **White-box techniques** (statement → decision → condition → MC/DC) measure code coverage; the right level depends on risk and regulation.
7. **Experience-based techniques** (attacks, taxonomies, exploratory) complement — never replace — systematic techniques.
8. **Risk-based testing** prioritizes effort: Risk = Impact × Likelihood; classify into CAT I–IV; respond via mitigate/contain/transfer/accept.
9. **Entry/exit criteria must be measurable and enforced** — never cosmetic, never date/budget-only.
10. **Independence improves defect detection** but has communication overhead — choose the level deliberately.
11. **Defect management is a lifecycle** — recognize, act, dispose; classify by severity/priority/type; not every defect must be fixed.
12. **Test tools amplify, not replace, human judgment** — watch for probe effects, vendor lock-in, training gaps, and the build-vs-buy trade-off.
13. **Documentation discipline (IEEE 829)** makes testing auditable and reproducible — essential for regulated domains.

---

## Cross-References
- Related: [[../The_Art_of_Unit_Testing.md]] — practitioner-level unit-test techniques (AAA, USE naming, stubs/mocks, isolation frameworks, async patterns, test recipes) that operationalize many of these principles at the component level.
- Topic index: [[../INDEX.md]]
