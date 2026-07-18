# Fundamentals of Software Testing
**Author:** Bernard Homès
**Topic tags:** `#testing` `#general`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md` · `summaries/Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md`

## TL;DR
An ISTQB Foundation Level–aligned deep-dive into the discipline of software testing: definitions, the seven principles, the test process (planning → monitoring → analysis → design → implementation → execution → completion), static testing and reviews, black-box, white-box, and experience-based techniques, risk- and requirement-based test design, test management, tools, and IEEE 829/29119 templates. Apply when you need to institute a test process, choose techniques for a specific project, design a test plan, or align on terminology across teams.

---

## Best Practices by Topic

### 1. Distinguish root cause, error, defect, and failure

**Principle:** The causality chain runs: human **error** → **defect** present in the work product → **failure** observed during execution. Mixing the terms loosens every conversation that follows.

**Do:**
- Train the team on the ISTQB definitions; pin them in shared docs.
- Track defects, not errors; root-causes are useful but secondary.
- Map defects back to errors via taxonomy; map failures back to defects via reproduction.

**Don't:**
- Don't blame the person who introduced the error (systemic causes are systemic).
- Don't conflate "bug" with "defect" when reporting; pick the formal term.
- Don't treat a defect as harmless because no failure was observed; latent defects ship.

**Code:**
```text
"There is a causality link between errors and defects, and between
defects and failures generated. The initial cause — the root cause — of
defects is often found to be caused by the actions (or lack of action)
of humans.

* error: human action at the root of a defect;
* defect: result, present in the test object, of a human action (i.e. error);
* failure: result from the execution of a defect by a process (whether
the process is automated or not)."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.1.2. Causes of software defects"*

---

### 2. Verification is "did we build it right?"; validation is "did we build the right thing?"

**Principle:** Verification and validation are complementary but distinct. ISO 9000 terms worth pinning in every test plan.

**Do:**
- Pair verification (spec → artifact) with validation (artifact → real use) in every test plan.
- Use objective evidence to back both; "looks good" is neither.
- Re-run validation whenever the use case changes, even if spec hasn't.

**Don't:**
- Don't substitute one for the other; they catch different defects.
- Don't claim a system is "verified and validated" without listing the evidence.
- Don't validate against aspirational requirements that the implementation never accepted.

**Code:**
```text
"Verification provides a response to the question: 'have we produced
what is specified?'

Validation provides a response to the question: 'have we built the
correct product?'

Verification and validation are complementary but not identical.
These differences will have an impact on the burden of proof to be
provided by the testers."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.1.5. Terminology"*

---

### 3. Apply the seven principles of testing

**Principle:** Testing shows the *presence* of defects, never their absence. Exhaustiveness is impossible. Early testing saves cost. Defects cluster. Tests decay. Testing is context-dependent. Absence of errors ≠ success.

**Do:**
- Quote principle 1 when stakeholders ask "did testing find everything?".
- Use risk and context to choose what to test, not to convince people you've tested enough.
- Plan for the pesticide paradox: refresh test data and sequences every quarter.
- Re-evaluate risk-driven coverage at every major change.

**Don't:**
- Don't argue "we've tested everything"; you haven't, you can't.
- Don't reuse unchanged test suites release after release; they erode.
- Don't claim a defect-free system is fit for purpose without validation evidence.
- Don't skip early testing; the 1→10→100→1000 cost ratio is real.

**Code:**
```text
"Principle 1: Testing identifies the presence of defects
Principle 2: Exhaustive testing is impossible
Principle 3: Early testing
Principle 4: Defect clustering
Principle 5: Pesticide paradox
Principle 6: Testing is context dependent
Principle 7: Absence-of-errors fallacy"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.3. Paradoxes and main principles"*

---

### 4. Quantify the early-testing cost multiplier

**Principle:** Industry rule-of-thumb: defect caught in design = 1×, in coding = 10×, in test = 100×, in production = 1000×. This is the justification for shift-left.

**Do:**
- Run static testing early (reviews, inspections, linters).
- Adopt test-first (TDD/ATDD) at the unit and acceptance levels.
- Track your own organization's correction cost ratios; validate the rule locally.

**Don't:**
- Don't pretend the rule is precise; it's an empirical anchor, not a formula.
- Don't run only late-cycle test execution; cost asymmetries will bankrupt the team.
- Don't skip defect prevention in favour of detection; design reviews are cheaper than test triage.

**Code:**
```text
"A ratio usually applied in industry (validated numerous times in
Europe, USA and Asia) is as follows: for a specific unit of cost,
the cost of finding (and fixing) a defect in the design phase is
'1'. If the defect is identified in the coding phase, it is
multiplied by '10'. If the defect is found during the test phase
(system test or acceptance test), then the cost is multiplied by
'100'. Finally, if the defect is found in production (by the
customer or by a user), then the cost is multiplied by '1,000'."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.3.3. Early testing"*

---

### 5. Follow the seven-step test process

**Principle:** ISO/IEC/IEEE 29119-2 defines the test process as seven activities: planning, monitoring & control, analysis, design, implementation, execution, completion. Repeat each at every test level.

**Do:**
- Run all seven activities even for small test campaigns; scale the depth, not the breadth.
- Treat planning as a separate activity from analysis; the output is different.
- Document entry and exit criteria for each activity.

**Don't:**
- Don't conflate analysis with design; analysis says what to test, design says how.
- Don't skip completion activities; lessons learned live there.
- Don't treat infrastructure management as a test activity without acknowledgement; it is supportive but distinct.

**Code:**
```text
"These activities are grouped in a number of major fundamental
processes:
* test planning
* test monitoring and control of the test activities
* analysis of work products and creation of test conditions
* design of tests conditions and of test cases
* implementation of tests cases manual or automated in the test
  environment
* execution of tests, evaluation of exit criteria and production
  of test reports
* test completion activities."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.4. Test activities, testware and test roles"*

---

### 6. Plan tests at three horizons: portfolio, version, delivery

**Principle:** Test planning nests three horizons: long-term (overall product), mid-term (current version across levels), short-term (current delivery).

**Do:**
- Build a master test plan for the long-term, level test plans for the version, cycle plans for the delivery.
- Apply the same planning activities at each horizon; change the scope and cadence.
- Define entry and exit criteria at each horizon.

**Don't:**
- Don't produce a single test plan that tries to cover all three horizons.
- Don't skip the long-term plan; you will keep reinventing scope.
- Don't omit entry/exit criteria for short-term delivery; you'll surprise the team with stop/go decisions.

**Code:**
```text
"Test activity planning for software can be evaluated on several levels:
* Long-term, at the overall software application level ...
* At the level of the software application version that is currently
  being prepared ...
* At the level of the current delivery ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.1. Planning and evaluation activities"*

---

### 7. Choose a test approach: analytical, model-based, methodic, dynamic, consultative, regression-adverse

**Principle:** Six canonical test approaches fit different contexts. Pick one consciously; hybrid is allowed.

**Do:**
- Pick analytical when requirements and contracts dominate the risk.
- Pick model-based when modeling is mature and time allows.
- Pick methodic when regulatory compliance is the goal.
- Pick dynamic/heuristic when time is tight and skilled testers are available.
- Pick consultative for short-term specialist engagements; keep knowledge in-house.
- Pick regression-adverse when the system must not change meaningfully (maintenance).

**Don't:**
- Don't rigidly apply one approach across all projects; context rules.
- Don't skip documenting the chosen approach; future hires need the rationale.
- Don't default to "best practices" without understanding which approach fits.

**Code:**
```text
"* analytical
* model-based
* standard or process-based (methodic)
* dynamic and heuristic
* consultative
* regression-adverse"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.1. Planning and evaluation activities"*

---

### 8. Run entry and exit criteria on every activity

**Principle:** Entry criteria prevent starting activities that aren't ready. Exit criteria prevent declaring activities done when they aren't. Both use ISO 29119-1.

**Do:**
- Define entry and exit criteria per test level, per activity, per cycle.
- Use measured coverage (requirements covered, risks covered, code covered) as exit criteria.
- Avoid meaningless stop rules (date, effort budget) as the only criterion.

**Don't:**
- Don't declare "exit" without criteria; you will be surprised by what shipped.
- Don't use overly strict exit criteria; they will block valid shipments.
- Don't use date-only or budget-only exit criteria alone; track coverage and defect rate as well.

**Code:**
```text
"Among possible exit criteria, we can mention the following:
* 100% statements, branch or decision coverage by the executed tests.
* reaching a specific detection ratio for new defects per period of
  time ...
* all tests planned for this test level have been successfully
  executed ...
* all tests for 'catastrophic' and 'critical' (or even 'marginal')
  integrity levels have been designed, implemented and executed
  successfully on the last version of the software or system.

Some exit criteria should be avoided:
* Stopping testing when the planned test termination date is reached.
* Stopping testing when the planned test effort has been reached.
* Stopping when all the test cases have been executed without
  finding new defects."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.4. Entry and exit criteria"*

---

### 9. Distinguish test level (component, integration, system, acceptance) from test type (functional, nonfunctional, structural, change-related)

**Principle:** Test level answers "where in the architecture?", test type answers "what characteristic?". Mix and match; don't conflate.

**Do:**
- Plan each test level with its own entry/exit criteria and objectives.
- Pick test types per level based on risk and lifecycle stage.
- Use change-related tests (regression, confirmation) at every level, not just system.

**Don't:**
- Don't skip component or integration testing and call it "we have unit tests".
- Don't run acceptance tests as a final "gate" that hides earlier failures.
- Don't pretend nonfunctional testing (perf, security, usability) is free; it has its own discipline.

**Code:**
```text
"Examples of test levels: component test, integration test, system
test and acceptance test.

Examples of test types:
* Functional tests
* Nonfunctional tests
* Tests based on the structure or architecture of the software
* Tests associated with changes (regression, confirmation, etc.)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.2 / 2.3"*

---

### 10. Distinguish four kinds of change-related tests

**Principle:** Confirmation testing (re-test the fix) and regression testing (unchanged code still works) serve different purposes; maintenance-level modifications need different testing than perfective/adaptive/evolutive changes.

**Do:**
- Always confirm a fix before moving to regression testing.
- Build a regression suite that exercises the most-coupled paths, not the most-popular ones.
- Plan evolutive, corrective, and retirement maintenance tests under a regression policy.

**Don't:**
- Don't skip regression because "we only changed one line".
- Don't use confirmation testing as regression; they answer different questions.
- Don't conflate "retirement" with "delete"; data migration is a maintainability test.

**Code:**
```text
"Maintenance testing ... Evolutive maintenance ... Corrective
maintenance ... Retirement and replacement ... Regression test
policies ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.4. Test and maintenance"*

---

### 11. Implement static testing through reviews

**Principle:** Reviews are the cheapest way to find defects. Caper Jones: formal inspections reduce project duration by 15% and workload by 20% while finding 200% more defects pre-release.

**Do:**
- Adopt a review taxonomy: informal review, walkthrough, technical review, inspection.
- Make every work product reviewable: requirements, design, code, tests, contracts.
- Time-box inspections; insist on written defects; rotate moderators.

**Don't:**
- Don't claim "we don't have time to review"; data shows the opposite.
- Don't conflate walkthroughs with inspections; inspections have stricter roles and metrics.
- Don't let reviews become blame sessions; they exist for defect detection, not performance review.

**Code:**
```text
"According to Caper Jones, 'formal inspections have proven both to
benefit overall projects costs and to shorten project schedule'.
The average reduction in duration is 15% and the workload is
reduced by about 20%, with an average of 200% more defects identified
before delivery of the software.

According to Tom Gilb, inspections are twice as effective at
detecting defects as walk-throughs.

According to Marnie L. Hutcheson and Caper Jones, defect
identification and removal efficiency for design reviews and code
inspections vary between 45% and 68% even though they are in the
37%–60% range for the sum of all formal test activities."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "3.4. Added value of static activities"*

---

### 12. Pick the right review type for the artefact

**Principle:** Informal review for low-stakes; walkthrough for shared understanding; technical review for change impact; inspection for safety-critical.

**Do:**
- Match review formality to defect severity and artefact criticality.
- Document a reviewer checklist per artefact type (requirements, code).
- Always assign a moderator; rotate them for fresh eyes.
- Always include a scribe; never let the moderator also scribe.

**Don't:**
- Don't run inspections for trivial changes; the ceremony exhausts the team.
- Don't run walkthroughs without individual preparation; without it, the meeting is theatre.
- Don't pretend informal review means no review; even peer review needs a checklist.

**Code:**
```text
"Types of reviews: informal review ... walk-through ... technical
review ... inspection.

Roles and responsibilities during reviews: author, moderator,
scribe, reviewer, manager."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "3.2.1. Types of reviews"*

---

### 13. Run static analysis by tools

**Principle:** Static analysis tools inspect source without executing it. They catch a class of defects dynamic tests miss.

**Do:**
- Lint, format, complexity, dependency, security, and data-flow in CI.
- Combine control flow analysis and data flow analysis.
- Use metrics (Halstead, cyclomatic complexity) to identify hot spots.

**Don't:**
- Don't rely on a single tool; coverage of defect classes varies.
- Don't trust static analysis for race conditions in concurrent code; flag, don't claim.
- Don't gate deploys on tools without triage rules; false positives erode trust.

**Code:**
```c
#include <stdio.h>
int main() {
    int x;          // uninitialized
    printf("%d", x); // data-flow defect: undefined content
    return 0;
}
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "3.3.3. Data flow analysis"*

---

### 14. Track defects classified by source, type, and impact

**Principle:** Defect taxonomies enable prevention. Without a taxonomy, you can't recognize repeat defects.

**Do:**
- Adopt or build a defect taxonomy that names common defects (Kaner's appendix A; Beizer's catalogues).
- Track severity, priority, root cause, age, and originator's assessment of urgency.
- Use the data to drive process improvements, not to blame individuals.

**Don't:**
- Don't let "human error" stand as root cause; dig deeper (training gap, missing review, weak spec).
- Don't use severity and priority as synonyms; severity is impact, priority is fix order.
- Don't track defects without disposition; unbounded defect queues are useless.

**Code:**
```text
"Defect disposition ... Actions applied to defects ... Defect
disposition are: deferred, rejected, duplicate, fixed, cannot be
reproduced..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.7. Defect management"*

---

### 15. Use equivalence partitioning to defuse combinatorics

**Principle:** Within an equivalence partition, all values should be processed identically by the system under test. Test one representative per partition.

**Do:**
- Define valid partitions and invalid partitions for each input.
- Apply partitioning to input/output values, internal variables, and field sizes.
- Use partitions as inputs to boundary value analysis (test on the edge of each partition).

**Don't:**
- Don't pick "all positive numbers" as one partition if they don't behave identically (e.g., leap year).
- Don't ignore invalid partitions; they often catch the worst defects.
- Don't use multiple representatives per partition unless you suspect the partition is wrong.

**Code:**
```text
"Equivalence partitioning is a simple technique, applicable for any
and all variables present in the software, whether input or output
values, alphabetical, numerical or other. It is based on the
principle that all values from a same equivalence partition will be
processed the same way by the same instructions."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.1. Equivalence partitioning"*

---

### 16. Layer boundary value analysis on top of equivalence partitioning

**Principle:** Defects cluster at boundaries. Use EP to find classes; BVA to find the edges.

**Do:**
- Test values just below, on, and just above each boundary.
- For 2-value BVA: nominal and boundary on each side.
- For 3-value BVA: just-below, nominal, just-above.
- Document the partition boundaries in the test design specification.

**Don't:**
- Don't skip the nominal point; "we know it works there" is not a test.
- Don't conflate BVA with EP; they are layered, not interchangeable.
- Don't apply BVA to non-ordered sets (e.g., colour = {red, green, blue}); the model breaks.

**Code:**
```text
"In the example we took previously (sqrt(1/x)), we identified three
series of data and three equivalence partitions:
* All positive numbers ...
* All negative numbers ...
* The zero value ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.1 / 4.3.2"*

---

### 17. Use decision tables for multi-condition logic

**Principle:** When inputs combine conditionally, decision tables enumerate (cause × effect) combinations more compactly than ad-hoc tests.

**Do:**
- Enumerate conditions and their combinations.
- Mark rules as infeasible when the spec excludes them.
- Cover the table with as few test cases as possible (one test may hit multiple columns).
- Reduce the table when columns are duplicates or shadows.

**Don't:**
- Don't enumerate every combination when constraints make some infeasible; document why.
- Don't ship decision tables without an example walk-through; reviewers get lost in rule counts.
- Don't use decision tables to test sequential behaviour; state transition testing is the better tool.

**Code:**
```text
"Decision table testing ... causes and effects shown in a decision
table."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.3. Decision tables"*

---

### 18. Use state transition testing for sequential behaviour

**Principle:** When state changes drive behavior, model and test transitions explicitly. 0-switch coverage is the floor; N-switch grows confidence linearly.

**Do:**
- Build a state transition diagram as part of design and test analysis.
- Cover every valid transition at least once.
- Test invalid transitions and observe rejection.
- Validate sequences of N+1 transitions (N-switch) when ordering matters.

**Don't:**
- Don't test sequences of transactions as if order doesn't matter; it often does.
- Don't skip invalid-transition coverage; it catches authorisation and validation regressions.
- Don't use a state machine that doesn't match the code; update it when you find divergence.

**Code:**
```text
"State transition testing ... valid and invalid state transitions ...
N-switch testing ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.5. State transition testing"*

---

### 19. Use use case testing for business behaviour

**Principle:** Use case testing writes tests from the user's scenario, not from the data model. It catches mismatches between business and system.

**Do:**
- Define use cases from the requirements (not from the implementation).
- Cover the main flow per use case; add secondary, exception, and error flows.
- Reuse use cases across system and acceptance tests; share the language.

**Don't:**
- Don't reuse use cases as test scripts verbatim; test design needs its own choices.
- Don't pretend use case tests replace state transition tests; they overlap but aren't equivalent.
- Don't use use cases as the only technique; combine with EP, BVA, and decision tables.

**Code:**
```text
"Use case testing ... test cases are designed to execute user
scenarios."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.3.6. Use case testing"*

---

### 20. Pick structure-based techniques by coverage goal

**Principle:** Statement, decision/branch, condition, MC/DC coverage each buy more confidence at more cost. Pick by safety level.

**Do:**
- Use statement coverage for low-risk code paths.
- Use decision/branch coverage when every branch matters.
- Use MC/DC for safety-critical software (DO-178B/C Level A).
- Treat 100% statement coverage as a floor, not a ceiling.

**Don't:**
- Don't confuse statement coverage with branch coverage; one missed `if` defeats decision coverage.
- Don't claim path coverage from statement coverage; path coverage is far stronger.
- Don't chase 100% MC/DC for everything; it requires formal proof and is expensive.

**Code:**
```text
"Cyclomatic complexity ... L - N + 2P

Statement coverage ... Decision coverage ... Branch coverage ...
MC/DC coverage ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.4. Structure-based techniques"*

---

### 21. Use experience-based techniques when specs are weak

**Principle:** Error guessing, exploratory testing, checklist-based testing exploit the tester's experience to compensate for thin specifications.

**Do:**
- Use error guessing when past projects have failed in known ways.
- Use exploratory testing with charters when full coverage is unrealistic.
- Build team knowledge through defect taxonomies and attack lists.
- Pair experienced testers with novices on exploratory charters.

**Don't:**
- Don't use experience-based techniques alone when documentation is rich; you will miss "spec but not coded" defects.
- Don't claim exploratory testing replaces formal testing; they cover different grounds.
- Don't skip debriefing after exploratory sessions; lessons are gold.

**Code:**
```text
"Experience-based test technique: A test technique based on the
tester's experience, knowledge and intuition.

Exploratory testing: An approach to testing in which the testers
dynamically design and execute tests based on their knowledge,
exploration of the test item and the results of previous tests."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.5. Experience-based technique"*

---

### 22. Plan attacks and defect taxonomies ahead of security-relevant tests

**Principle:** "Directed and focused attempt to evaluate the quality, and especially the reliability, of a test object by attempting to force specific failures to occur." Combine with known-failure-mode catalogues.

**Do:**
- Build an attack list per category: input boundaries, time-of-check vs time-of-use, privilege escalation, etc.
- Reference Kaner's appendix A as a starter taxonomy.
- Run attack-based tests as a different mindset from requirement-based tests.

**Don't:**
- Don't pretend security testing is requirement testing; threat models drive it.
- Don't skip attacks because the requirements don't forbid them; attackers don't read requirements.
- Don't test security without domain expertise; weak security tests are worse than no tests.

**Code:**
```text
"Attack: Directed and focused attempt to evaluate the quality, and
especially the reliability, of a test object by attempting to force
specific failures to occur.

Defect taxonomies: lists of typical defects."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.5.1 / 4.5.2"*

---

### 23. Apply collaboration-based testing for shared understanding

**Principle:** User stories, acceptance criteria, ATDD, and Three Amigos align developers, testers, and business on what is "done".

**Do:**
- Co-author user stories with business, developer, and tester.
- Express acceptance criteria as Given/When/Then for testability.
- Use ATDD when tests must precede implementation.
- Run Three Amigos sessions to flush ambiguity.

**Don't:**
- Don't accept "the developer wrote the user story" as collaboration.
- Don't use BDD/ATDD as documentation theatre; tests must run.
- Don't pin acceptance criteria to implementation details; they should describe behaviour.

**Code:**
```gherkin
Given a registered user with the "Editor" role
When they save an edited page
Then the page is added to the content owner's review queue
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.6. Collaboration-based test approaches"*

---

### 24. Choose the right technique combination per project

**Principle:** "Whichever test category is envisaged, it is necessary to remember that a single test technique or a single test category is not enough to ascertain a level of quality."

**Do:**
- Combine black-box, white-box, and experience-based techniques per level.
- Re-pick techniques when the project context shifts.
- Use technique coverage as a test design metric; track which technique covers what.

**Don't:**
- Don't pick one technique for the entire project; quality is multi-dimensional.
- Don't pick techniques based on tester convenience; pick on risk.
- Don't under-document the chosen techniques; reviewers will question the choice later.

**Code:**
```text
"To each of these groups of techniques are associated assumptions
and limitations that need to be taken into account when these
techniques are used. ... Whichever test category is envisaged, it
is necessary to remember that a single test technique or a single
test category is not enough to ascertain a level of quality."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.2 / 4.7"*

---

### 25. Make traceability bidirectional

**Principle:** Traceability between requirements, test conditions, test cases, and execution lets you answer "where are we?" without guessing.

**Do:**
- Build horizontal traceability (across test documentation layers).
- Build vertical traceability (between requirements and components).
- Update traceability when requirements, conditions, or cases change.
- Maintain traceability in a tool when scale makes manual tables untenable.

**Don't:**
- Don't skip traceability for short projects; the next handover depends on it.
- Don't change requirements without updating traceability; coverage claims become lies.
- Don't let traceability tables become stale; review them every sprint.

**Code:**
```text
"One solution is to implement traceability from requirements and
specifications, to the test cases and their execution, via the test
conditions. This will enable us to have complete clarity in our
tests and what still needs to be done.

Bidirectional traceability between requirements, test cases and
their execution enables the measurement of test processes and the
identification of the impact when a test case covers more than one
requirement."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "4.1.2. Traceability"*

---

### 26. Pick the right level of independence

**Principle:** Independence of testing scales with risk. No independence for low-risk; full independence (external) for safety-critical.

**Do:**
- Use developers testing their own code for low-risk components.
- Use internal QA for cross-team components.
- Use external QA / certification for safety-critical and regulatory components.
- Match independence level to defect cost and risk class.

**Don't:**
- Don't claim "the developer tested it" is independence; the developer is the author.
- Don't force external QA on every project; cost inflates and skill mismatch grows.
- Don't underfund independence for high-risk products; the cost of missed defects is far higher.

**Code:**
```text
"- Total lack of independence: when developers are the only ones
  testing their codes.
- A limited level of independence, whereby someone in the same team
  and with the same role as the designer is assigned to review the
  produced software. ...
- One person or a small group of individuals, specialized in software
  testing and associated with the development team ...
- A specialized software testing team within the same organization,
  but not in the same hierarchical chain as the development team.
- A specialized software testing team in a separate economic entity
  (other company, freelance consultants, etc.) ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.1.1. Independence levels"*

---

### 27. Build test teams with explicit specialisation

**Principle:** Test analysts, test automation specialists, technical test analysts, and technical specialists all serve distinct purposes; conflate at your peril.

**Do:**
- Hire test analysts for functional/non-functional deep coverage.
- Hire test automation specialists for framework and CI work.
- Hire technical specialists (DBAs, performance, security) for narrow expertise.
- Treat exploratory charters as a specialist activity too.

**Don't:**
- Don't dump all testing work onto "testers"; specialists deliver better signal.
- Don't undervalue technical specialists; they see what generalists miss.
- Don't ignore subcontracting risk; build in-house expertise to retain knowledge.

**Code:**
```text
"In large teams, specialization is more marked. We have:
- test analysts, whose specialization concentrates on one or more
  functional or nonfunctional aspects;
- test automation specialists, focusing on automated tests ...
- technical test analysts, who are specialists in certain specific
  aspects, such as performance testing, security, or maintainability
  testing ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.1.3. Human and contractual aspects"*

---

### 28. Estimate test effort with multiple methods; reject the false-precision ones

**Principle:** Estimation methods include metrics-based (COCOMOII, function points, test points), experience-based, and agile (story points, planning poker). Don't rely on a single one.

**Do:**
- Use COCOMOII / test points for top-down budget alignment.
- Use WBS (work breakdown structure) and bottom-up for detailed planning.
- Use three-point estimation (optimistic, likely, pessimistic) to expose assumptions.
- Cross-check with similar past projects when context allows.

**Don't:**
- Don't pretend LOC-based estimation is comparable across languages.
- Don't trust expert estimates that have no input from the people who will do the work.
- Don't update agile story points mid-iteration; they'll lose meaning.

**Code:**
```text
"There are two main families of approaches for estimation: those
based on metrics and mathematical formulas and those based on
historical references and experience. A third family of approaches
is proposed for the agile world.

... The first experience-based method requires that each individual
who will execute the planned tasks estimate the workload, and these
individual task estimations are summed.

The second ... requires an experienced tester to estimate the
workload. ... three-point estimation.

A third method is based on the similarity between the project to be
estimated and previous projects ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.1.5-5.2.1.7"*

---

### 29. Build the test pyramid consciously

**Principle:** The test pyramid — more unit/component tests at the base, fewer end-to-end at the apex — keeps feedback fast and cost low.

**Do:**
- Heavily invest in unit and component tests.
- Use integration tests at every boundary.
- Keep end-to-end tests small and stable.
- Use contract tests where components cross service boundaries.

**Don't:**
- Don't build an inverted pyramid (mostly E2E); it's slow and brittle.
- Don't use unit tests as integration tests; the scope of failure will mislead.
- Don't add new E2E tests lightly; each new one increases maintenance cost.

**Code:**
```text
"The test pyramid is often shown with different layers, each level
showing the testing effort to be implemented. At the lower level,
we have unit tests or component testing and these are often very
granular, and can be automated. At the higher levels, we have user
acceptance tests, which are often complex, business related and
difficult to automate."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.1.8. The test pyramid"*

---

### 30. Plan test activities with the ISTQB test process

**Principle:** Seven activities: planning, monitoring & control, analysis, design, implementation, execution, completion. Plan each.

**Do:**
- Document test plan, monitor/control plan, test design specs, test cases, test procedures, test logs, defect reports, completion reports.
- Use the IEEE 829-1998 / IEEE 829-2008 templates when formal compliance is needed.
- Treat the plan as a living document; revise it as reality intrudes.

**Don't:**
- Don't pretend one template fits all projects; pick and customize.
- Don't write test plans that no one reads.
- Don't skip test logs; forensically they win post-mortems.

**Code:**
```text
"IEEE 829-2008 ... master test plan ... test plan ... test design
document ... test case ... test procedure ... test log ... defect
report ... test report."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Chapter 8 Templates and Models"*

---

### 31. Use test reports tailored to stakeholder

**Principle:** What to report, to whom, and how differs by audience. Testers, developers, test leads, hierarchy, and customers want different views.

**Do:**
- Show testers coverage and remaining workload.
- Show developers defect-by-component and severity.
- Show test leads defect rate and correction time.
- Show hierarchy quality level, effort spent, delivery risk.
- Show customers test dates and provisional ship dates.

**Don't:**
- Don't send the same report to all stakeholders; context is information.
- Don't confuse visuals with interpretation; trend plots need annotations.
- Don't lie with "all green"; flags should respect reality.

**Code:**
```text
"Testing management is interested in:
* planned software delivery dates by the development team for testing
* functionalities, specifications or requirement changes ...
* the number of defects detected per period of time ...
* the effort spent compared to the effort planned ...

Higher-level hierarchy is interested in:
* the identified quality level
* the use of the planned effort ...
* planned delivery dates and potential risks of slippage
* the improvement of the application maturity ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.4.1. What to report, to whom and how?"*

---

### 32. Recognise when statistics and graphs mislead

**Principle:** "Metrics and measurements, just as statistics, can be misleading: the simple visual representation of the tests can be different from their detailed interpretation."

**Do:**
- Always compare actual progress to the planned progress at the same date.
- Annotate trend lines with anomalies (holiday, deployment, requirements change).
- Use multiple metrics, not one; corroborate trends with defect rate and test execution rate.
- Treat suspicious-looking data as a flag, not as fact.

**Don't:**
- Don't interpret a single chart without reading the underlying counts.
- Don't accept "0% delta" as proof of stasis; the testing might just not have started.
- Don't reward teams for cosmetic metric improvement.

**Code:**
```text
"First, we can conclude that integration seems to have been done
according to the 'big bang' model. However, this is not entirely
true as only 80% of the components have been developed and
integrated. ... A more detailed reading enables us to identify
surprising aspects of this graph, such as the progress from the
fourth week onwards with an incremental step of 5% and then of
10% from the ninth value. This is not statistically realistic and
should have raised a red flag for the customer."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.3. Test progress monitoring"*

---

### 33. Anonymise test data; respect compliance

**Principle:** Production data is confidential; copy to test only after anonymisation.

**Do:**
- Anonymise production data before using it in tests.
- Use synthetic generation for repeated shapes.
- Maintain a test data lineage.
- Honour regulatory notification (GDPR, HIPAA, etc.) when even anonymised data crosses borders.

**Don't:**
- Don't copy production data to test environments by default.
- Don't skip anonymisation because "internal only"; rules travel with the data.
- Don't use the same test dataset across projects.

**Code:**
```text
"Production data are confidential and always protected. Test data
are not subjected to the same restrictions or even to the same
safety measures. If test data are used, it is thus recommended to
ensure that they are 'anonymized'."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.5.1. Test data definition"*

---

### 34. Treat configuration management as a test asset

**Principle:** Without configuration management, test failures are unreproducible. Track testware like code.

**Do:**
- Apply configuration management to all test artefacts: scripts, fixtures, environment.
- Reproduce failures by environment pinning.
- Use CM (configuration management) tools the team already uses.
- Track test scripts, environments, and data; not just code.

**Don't:**
- Don't let testers manually clone test scripts across environments.
- Don't pretend "test environment" is out of scope; it is part of testing.
- Don't pin your tests to specific tooling without CM; one migration away, you lose the tests.

**Code:**
```text
"Configuration management must also be ensured for all hardware
components necessary for testing, as well as for software tools and
operating systems."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.5.2. Configuration management"*

---

### 35. Build change management into the test lifecycle

**Principle:** Industry estimates "~2% change per month for evolutions in requirements". Treat change requests as routine.

**Do:**
- Use a change control board; evaluate impacts across specs, code, tests, and documentation.
- Document the test impact of each change.
- Re-prioritise test execution after every change request.

**Don't:**
- Don't ignore small change requests; they compound.
- Don't batch changes for "less disruption"; the impact analysis is per change.
- Don't ship change-impacted code without re-running the impacted tests.

**Code:**
```text
"The industry estimates at about 2% change per month for evolutions
in requirements. It is important to ensure a consistent
implementation of these changes, with the evaluation of their
impacts on specifications, architecture, code, tests and
documentation."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.5.3. Change management"*

---

### 36. Plan risk-based testing for prioritisation

**Principle:** Use product risks as the basis for selecting, prioritising, and assigning depth of testing.

**Do:**
- Identify product risks; classify by likelihood × impact (RPN).
- Trace risk to test coverage; let risk be the test rationale.
- Re-evaluate the risk register periodically.

**Don't:**
- Don't pretend all defects are equal; they aren't.
- Don't skip risk management when "everything must be tested"; you can't.
- Don't let the risk register become an annual exercise; it lives in the project.

**Code:**
```text
"Risk = ((impacts) × (likelihood)) [5.1]

Risk level matrix (1-16 RPN):
1 | 2 | 3  | 4
2 | 4 | 6  | 8
3 | 6 | 9  | 12
4 | 8 | 12 | 16

Risk-based testing ... risk-driven test selection and prioritisation."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.6. Risk management"*

---

### 37. Distinguish project risks from product risks

**Principle:** Project risks hit schedule/cost/staffing; product risks hit quality/correctness/availability. Mix them and you target the wrong lever.

**Do:**
- Identify project risks from calendar, staffing, scope, geography, dependencies.
- Identify product risks from features, complexity, integration, change history.
- Map risk response to the right category: mitigate, transfer, accept, reduce impact.

**Don't:**
- Don't pretend project risk is irrelevant to test; a delayed delivery isn't tested at all.
- Don't accept product risk without owner accountability.
- Don't act on a risk before identifying it; that is panic, not risk management.

**Code:**
```text
"A project-related risk is a risk whose initial and main impact
will be on the project, on its cost or its duration, on the effort
required, or the use of the resources associated with the project.

A risk related to the product will have an initial and principal
impact on the software, its quality level, limitations or on its
availability."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.6.2. Project risks and product risks"*

---

### 38. Use the full set of risk-response options

**Principle:** Risk response is not just "mitigate". You can also accept, transfer, reduce impact, or ignore (when impact is minimal).

**Do:**
- Accept when the impact is low and no action is justified.
- Reduce probability via testing, reviews, training.
- Reduce impact via backups, fallback designs.
- Transfer via EULA, insurance, contracts with suppliers.
- Re-evaluate after mitigation; risk evolves.

**Don't:**
- Don't pretend mitigate-only is sufficient; some risks are not mitigatable.
- Don't transfer risk without checking that the recipient accepts it.
- Don't accept a risk that's still rising; revisit it.

**Code:**
```text
"Risk responses:
* accept this risk
* reduce the occurrence probability
* reduce the impact
* transfer the risk to another team or organization"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Response to risks"*

---

### 39. Build test tools selection around process maturity, not promises

**Principle:** Tool ROI depends on process maturity. Mature processes extract more value from tools.

**Do:**
- Pre-select 3-5 candidate tools; check their fit for your process.
- Run a proof-of-concept in your environment; do not trust demos.
- Pilot on a single project; measure benefits; then generalize.

**Don't:**
- Don't buy a tool before defining what you need it for.
- Don't over-rely on a single demo; salespeople have rehearsed paths.
- Don't skip the pilot; full rollouts of unfit tools erode trust.

**Code:**
```text
"We have to be very wary of editor promises and of the capacity of
a single tool to meet all our needs. In fact, it might be necessary
to select several tools."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "6.3.2. Tool selection process"*

---

### 40. Use the right tool class per task

**Principle:** Tool classes: management, requirement management, static, design/data, execution, environment, comparison, coverage, modelling, defect management. Match to need.

**Do:**
- Pick the right class for the job (e.g., coverage tool for coverage; not a defect management tool).
- Build small toolchains that interop; avoid lock-in.
- Treat the probe effect seriously; performance tests with a profiler on may differ.

**Don't:**
- Don't buy a tool suite and then figure out how to use each piece.
- Don't underestimate the probe effect (testers changing what they measure).
- Don't skip tool retirement; dead tools pollute the chain.

**Code:**
```text
"Types of test tools ... tools supporting test management ...
requirement management ... static tests ... modeling ... test design
... test execution ... test environment management ... test data
comparison ... test coverage measurement ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "6.1. Types of test tools"*

---

### 41. Test the test tools

**Principle:** "Test tools must themselves be tested before being relied upon."

**Do:**
- Validate tool outputs against known cases; reject mismatches.
- Use version pinning; tool behaviour drifts by version.
- Sandbox the toolchain; CI/CD failures shouldn't crash your laptops.

**Don't:**
- Don't trust tool outputs blindly; tools misread specs.
- Don't enable "experimental" features in regulated contexts.
- Don't ignore tool-specific failure modes (probe effect, false negatives).

**Code:**
```text
"Advantages and risks of the tools ... Specific considerations for
some tools ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "6.2.1 / 6.2.2"*

---

### 42. Apply test data definition before execution

**Principle:** Test data is more than "input"; it includes pre-conditions, expected results, and large-volume data for perf.

**Do:**
- Pick data to exercise every planned combination.
- Capture expected results for every input — oracles.
- Pre-generate large datasets for performance and load.
- Anonymise production-derived data.

**Don't:**
- Don't reuse inputs blindly across EP/BVA classes; the boundary is the lesson.
- Don't fabricate expected results during execution; verify offline.
- Don't forget hardware-software co-dependencies for testing environments.

**Code:**
```text
"We must identify the necessary input data to exercise all planned
data combinations, depending on the techniques we use. For each
equivalence partition, we must identify the representatives and
design test data (in files, database tables or transactions) which
will enable us to identify potential failures."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.5.1"*

---

### 43. Use oracles wisely; pick sources that disagree

**Principle:** Oracles — sources of expected results — are limited. Combine sources to detect blind spots.

**Do:**
- Use requirements/specs as primary oracle.
- Use heuristics + a previous version of the system when specs are thin.
- Use user manuals and industry standards as cross-checks.
- Build a partial oracle per category; you won't have a perfect one.

**Don't:**
- Don't use the code itself as an oracle (Adrion); you'll propagate defects.
- Don't rely on a single oracle; multiple sources catch orthogonal defects.
- Don't promise oracle coverage you don't have; missing oracles hide bugs.

**Code:**
```text
"Test oracle: A source to determine expected results to compare with
the actual result of the software under test. An oracle may be the
existing system (for a benchmark), a user manual or an individual's
specialized knowledge, but should not be the code (from Adrion)."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.5. Oracles"*

---

### 44. Make oracles explicit in the test design

**Principle:** When an oracle is weak, the test is weak. Document the oracle for every test.

**Do:**
- Specify which oracle applies to each test.
- Mark tests that rely on tester judgement (e.g., usability).
- For AI/ML oracles, define what's "good enough".

**Don't:**
- Don't pretend every test has an objective oracle; some need human review.
- Don't use the code as oracle even indirectly (e.g., "test that the function returns what it returned yesterday").
- Don't treat oracles as an afterthought; they are test design work.

**Code:**
```text
"Problems with oracles ... Sources of oracles ... Oracle usage ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.5"*

---

### 45. Reuse the test process for maintenance, not just delivery

**Principle:** Test process improvement (TPI) and CMMI-style maturity apply to maintenance as much as delivery.

**Do:**
- Apply the test process (planning → completion) to maintenance releases.
- Use retrospectives to drive improvements.
- Track metrics and feed them back into the next iteration.
- Adopt processes that match organisational maturity.

**Don't:**
- Don't apply different test processes for delivery and maintenance; you will create drift.
- Don't pursue process maturity the team can't operate.
- Don't skip retrospectives; improvements die without them.

**Code:**
```text
"Process improvements ... Objectives ... Measurements ...
Retrospectives and improvements ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.6"*

---

### 46. Plan specific tests for performance and maintainability

**Principle:** Performance testing is a nonfunctional test with its own discipline (load, stress, spike, soak, scalability). Maintainability testing checks code structure and documentation over time.

**Do:**
- Define performance criteria up front; baseline and compare.
- Plan load tests with realistic data and traffic shapes.
- Track maintainability via metrics (complexity, duplication, comment ratio).
- Treat maintainability tests as prevention, not detection.

**Don't:**
- Don't run performance tests without a hypothesis; you'll learn nothing.
- Don't maintain load tests for years without review; they silently rot.
- Don't stop measuring maintainability because no one complains; you will feel it later.

**Code:**
```text
"Specific cases ... Performance tests ... Maintainability tests ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.7"*

---

### 47. Use test process improvement frameworks when scaling

**Principle:** TPI, TMM, CMMI, ISTQB — pick a framework that matches your organisation's appetite for structure.

**Do:**
- Pick a single framework; spread is overhead.
- Use the framework's maturity model to set the next improvement target.
- Re-baseline every 12-18 months.

**Don't:**
- Don't pursue Level 5 maturity when Level 3 is realistic.
- Don't skip process definition before measurement; you will measure noise.
- Don't drop the framework when under pressure; that's the moment it matters.

**Code:**
```text
"Mature processes, according to capability maturity model integration
(CMMI) and a coherent organization where each process is defined
and perfectly fits within the organization's development scheme,
could lead to a significant decrease in workload, while delivering
the same level of quality."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2.1.1. Process-dependent factors"*

---

### 48. Apply tester's code of ethics and professional practice

**Principle:** ISTQB's code of ethics covers public, client/employer, product, judgement, management, profession, colleagues, self. Use it when in doubt.

**Do:**
- Reference ISTQB when resisting "ship it without testing" pressure.
- Maintain client confidentiality; anonymise defect details when sharing.
- Document conflicting pressures; escalate to management.

**Don't:**
- Don't test in secret; testing is collaborative work.
- Don't sign off on a product you have doubts about.
- Don't accept work that compromises your professional judgement.

**Code:**
```text
"1.7. Testers and code of ethics (FL 1.6)
1. Public
2. Client and employer
3. Product
4. Judgment
5. Management
6. Profession
7. Colleagues
8. Self"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.7"*

---

### 49. Apply whole-team approach with the right test skills

**Principle:** Generic skills (analytical, communication, team) plus specific skills (domain knowledge, test techniques, tool fluency). Whole-team approach means quality is shared.

**Do:**
- Embed testers in product teams; cross-train on requirements and code.
- Track which skills each team member brings.
- Pair junior + senior testers on exploratory charters.

**Don't:**
- Don't isolate testers from delivery; integration is the bug catcher.
- Don't under-value domain knowledge; testers without context miss relevant defects.
- Don't pretend every developer is a tester; the perspective differs.

**Code:**
```text
"Generic skills ... Specific skills ... Whole team approach ...
Independence of testing ... Levels of independence ... Adapt to
objectives ... Destructive or constructive? ... People skills ...
Change of perspective"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "1.6"*

---

### 50. IEEE 829-1998 vs. IEEE 829-2008 templates: pick the right one for context

**Principle:** IEEE 829-1998 had multiple separate documents; IEEE 829-2008 reorganised into fewer, larger documents (Master/Level variants).

**Do:**
- Use IEEE 829-2008 in regulated environments where it is referenced.
- Tailor templates; drop fields that don't apply to your context.
- Keep your templates under version control.

**Don't:**
- Don't apply 1998 templates verbatim; field names changed.
- Don't apply 2008 templates without renaming fields for your org.
- Don't skip template customisation; over-strict templates produce poor-quality data.

**Code:**
```text
"IEEE 829-2008 ... master test plan ... test plan ... test design
document ... test case ... test procedure ... test log ... defect
report ... test report.

The templates section of Chapter 8 reproduces both versions for
each artefact with their canonical sections."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Chapter 8 Templates and Models"*

---

### 51. Build a master test plan to drive multi-level programmes

**Principle:** "Master test plan" addresses multiple test levels and acts as a "project test plan". Required when several test levels run together.

**Do:**
- Cover scope, approach, resources, schedule, level-specific deliverables.
- Tie the master plan to the project's overall plan.
- Refresh quarterly.

**Don't:**
- Don't have a master plan that contradicts level plans.
- Don't skip a master plan in multi-product programmes; coordination will suffer.
- Don't write a master plan once; treat it as a snapshot.

**Code:**
```text
"Master Test Plan (IEEE 829-2008): Master Test Plan ... 1.
Introduction ... 2. Details of the master test plan ... 3. General
... 3.1 Glossary ... 3.2 Document change procedures and history"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.1"*

---

### 52. Use test design specifications to plan tests before cases

**Principle:** Test design specifications capture the test conditions, the detailed test approach, and the high-level test cases — before the cases themselves.

**Do:**
- Document test conditions per item being tested.
- Document the approach refinements (which techniques, which level, which exit).
- Reference high-level test cases that derive from the design.

**Don't:**
- Don't skip the design specification when going straight to test cases.
- Don't duplicate conditions; reference shared conditions across design specs.
- Don't let design specs become design-by-committee docs.

**Code:**
```text
"Test Design Specification (IEEE 829-1998):
1. Test design specification identifier
2. Features to be tested
3. Approach refinements
4. Test identification
5. Feature pass/fail criteria"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.3"*

---

### 53. Use level test plans for version-level organisation

**Principle:** When a master plan spans levels, each level gets a "level test plan" that the team owns.

**Do:**
- Tie level test plans to test cycles.
- Keep level plans smaller than the master plan.
- Update level plans on architectural changes.

**Don't:**
- Don't treat a level test plan as a master plan in disguise.
- Don't have level plans without a master plan; coverage and consistency drift.
- Don't let level plans fall behind the codebase; treat them as living.

**Code:**
```text
"Test Plan (IEEE 829-2008):
1. Introduction (1.1 Identifier, 1.2 Scope, 1.3 References)
2. Details (Items, Features, Risks, ...)
3. General (Glossary, Document change procedures and history)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.2"*

---

### 54. Specify test cases with environment, special procedural requirements, and intercase dependencies

**Principle:** IEEE 829 captures the eight fields for a test case. Don't skip the boring ones.

**Do:**
- Specify inputs, expected outcomes, environmental needs, special procedural requirements, intercase dependencies.
- Reuse cases in multiple procedures when possible.
- Version cases with the implementation.

**Don't:**
- Don't forget environmental needs; many "intermittent" failures are environment.
- Don't skip intercase dependencies; one case's output feeds another's input.
- Don't freelance special procedural requirements; make them explicit.

**Code:**
```text
"Test Case Document (IEEE 829-2008):
1. Introduction (Identifier, Scope, References, Context, Notation)
2. Details (per test case: Identifier, Objective, Inputs, Outcome(s),
   Environmental needs, Special procedural requirements, Intercase
   dependencies)
3. Global (Glossary, Document change procedures and history)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.4"*

---

### 55. Specify test procedures as ordered steps

**Principle:** A test procedure is a sequence of actions for executing one or more test cases; capture them explicitly.

**Do:**
- Order test procedure steps for deterministic execution.
- Tie procedures to cases by reference, not duplication.
- Detail inputs, outputs, and special requirements per procedure.

**Don't:**
- Don't duplicate test case detail in procedures; reference, not copy.
- Don't skip "relationship to other procedures" — dependencies matter.
- Don't make procedures so rigid they resist legitimate variation.

**Code:**
```text
"Test Procedure Specification (IEEE 829-2008):
1. Introduction ...
2. Details (Inputs, outputs, special requirements; Ordered
   description of the steps to execute the test cases)
3. General (Glossary, Document change procedures and history)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.5"*

---

### 56. Use test logs to drive observability and forensics

**Principle:** Test logs are chronological records of execution detail; reuse them in post-mortems.

**Do:**
- Capture activity and event entries with timestamps and identifiers.
- Persist test logs per cycle, with version control.
- Cross-reference defects found to entries in the log.

**Don't:**
- Don't let logs only live on a single machine; back them up.
- Don't store logs without context; they must be readable in isolation.
- Don't skip logs for "trivial" cycles; they become critical during incidents.

**Code:**
```text
"Test Log (IEEE 829-2008):
1. Introduction (Identifier, Scope, References)
2. Details (Description; Activity and event entries)
3. General (Glossary)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.6"*

---

### 57. Write defect reports that developers can act on

**Principle:** "The first action of defect identification should thus consist of determining the reality of the error."

**Do:**
- Capture inputs, expected results, actual results, environment, attempts to repeat, observers.
- Give every defect a unique, traceable identifier.
- Reproduce the defect before reporting it; pre-filter test errors.
- Include the procedure step the defect was caught in.

**Don't:**
- Don't write vague defect reports ("the system is broken"); developers won't act.
- Don't bundle multiple defects in one report; one defect per report.
- Don't include speculative root causes; stick to observed facts.

**Code:**
```text
"Defect Report (IEEE 829-2008):
1. Introduction (Identifier, Scope, References)
2. Details (Summary, Date anomaly discovered, Context, Description
   of anomaly, Impact ... with Inputs, Expected results, Actual
   results, Unexpected outcomes, Procedure step, Environment,
   Attempts to repeat, Testers, Observers, Originator's urgency,
   Corrective action, Status, Conclusions)
3. General (Document change procedures and history)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.7"*

---

### 58. Run defensible defect triage

**Principle:** Triage decides which defects to fix, in what order, and which to defer or reject.

**Do:**
- Decide severity and priority; they are independent.
- Reject duplicate and "not reproducible" defects politely with evidence.
- Plan a triage schedule (daily in big projects, weekly in small ones).
- Document the triage decisions in the defect or in a log.

**Don't:**
- Don't conflate severity with priority; a crash may be low priority if no one uses the path.
- Don't reject a defect without trying to reproduce it; "works on my machine" is a flag, not a verdict.
- Don't defer critical defects forever; they accumulate tech debt.

**Code:**
```text
"Defect disposition ... Actions applied to defects ... Defect
disposition are: deferred, rejected, duplicate, fixed, cannot be
reproduced..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.7"*

---

### 59. Capture lessons learned in test completion activities

**Principle:** The test process ends with completion activities: lessons learned, environment cleanup, deliverables handover.

**Do:**
- Run a completion report at every level (Master/Level Test Report per IEEE 829).
- Capture strengths and weaknesses; both are valuable.
- Hand over testware to the next team; document the handover.

**Don't:**
- Don't skip completion reports; future projects will pay for the gap.
- Don't throw away test assets at the end of a project; archive them.
- Don't pretend no lessons were learned; "everything went well" is suspicious.

**Code:**
```text
"Test Report (IEEE 829-2008):
1. Introduction (Identifier, Scope, References)
2. Details (Test status summary, Changes from plans, Test status
   metrics)
3. General (Document change procedures and history)"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "8.8"*

---

### 60. Pick test automation by purpose, not by trend

**Principle:** Record/replay, data-driven, keyword-driven, model-based, robotic — each is suited to a different job.

**Do:**
- Use record/replay for quick smoke; abandon once the UI stabilises.
- Use data-driven for parameterized regression.
- Use keyword-driven for cross-tool teams.
- Use model-based for systems with rich state machines.

**Don't:**
- Don't let record/replay become a maintenance nightmare; refactor to data-driven quickly.
- Don't pick keyword-driven for tiny teams; the keyword overhead isn't worth it.
- Don't chase model-based if you don't have the modeling maturity.

**Code:**
```text
"Let us consider the following techniques:
I. Exploratory
II. Data-driven
III. Keyword-driven
IV. Portability
V. Record/replay
VI. TPI

... II and III are recognized as efficient and profitable
techniques for automated test management ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Sample exam questions / 6.x"*

---

### 61. Tailor scripts to scope and reuse

**Principle:** Scripts come in three flavours: procedural (step-by-step), data-driven (data drives behaviour), keyword-driven (keywords + data + scripts).

**Do:**
- Pick the script type by reuse pattern: more re-use → more abstraction.
- Use data tables to drive hundreds of variants of one script.
- Use keywords when business and tech teams share a common vocabulary.

**Don't:**
- Don't script what you can run from the API; UI is fragile.
- Don't write procedural scripts for large test suites; they don't scale.
- Don't skip maintenance of scripts; they are code.

**Code:**
```python
# Data-driven test (typical pattern)
@pytest.mark.parametrize(
    "amount, expected_grade",
    [(0, "failed"), (50, "failed"), (51, "fair"),
     (70, "satisfactory"), (90, "excellent"), (100, "excellent")],
)
def test_grade_boundaries(amount, expected_grade):
    assert grade(amount) == expected_grade
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Data-driven testing"*

---

### 62. Plan performance, load, and stress tests as separate phases

**Principle:** Performance: response time under expected load. Load: behaviour at peak load. Stress: behaviour at or beyond capacity.

**Do:**
- Define baselines for performance, load, stress, spike, soak.
- Run tests in production-like environments; probe effects distort measurements.
- Capture duration, throughput, error rate, and tail latency.

**Don't:**
- Don't call "the app feels slow" a performance test.
- Don't extrapolate from 100 RPS to 1,000 RPS; the failure modes differ.
- Don't run performance tests with production data without anonymisation.

**Code:**
```text
"Performance testing ... Load testing ... Stress testing ... Spike
testing ... Soak testing"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.7.1 / 6.x"*

---

### 63. Capture oracles from multiple sources to verify complex systems

**Principle:** AI/ML, scientific computing, and embedded systems often have weak oracles. Combine sources.

**Do:**
- Cross-check physical models, simulation outputs, and prior outputs.
- Use statistical tolerance bands where exact matches are impossible.
- Document the oracle's confidence per test.

**Don't:**
- Don't pretend every test has an objective oracle; some never will.
- Don't claim precision the oracle can't deliver.
- Don't skip oracle documentation; reviewers will question the test.

**Code:**
```text
"Problems with oracles ... Sources of oracles ... Oracle usage ..."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "2.5"*

---

### 64. Treat test planning as iterative, not one-shot

**Principle:** The test plan is a record of test planning; it evolves with the project.

**Do:**
- Re-plan when risk, scope, or staffing changes.
- Capture the rationale for each revision.
- Treat the test plan as a living document; revision history matters.

**Don't:**
- Don't treat the test plan as a contractual commitment frozen at start.
- Don't skip revisions when small things change; you will lose alignment.
- Don't freeze the plan at the project gate; release the plan with the product.

**Code:**
```text
"Test plan: A document describing the scope, approach, resources
and schedule of intended test activities. ... It is a record of the
test planning process (from ISO 29119-1)."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "5.2 / 8.2"*

---

### 65. Distinguish individual test judgement from team heuristics

**Principle:** Team heuristics (checklists, taxonomies, attack lists) plus individual judgement produce coverage you can defend.

**Do:**
- Capture individual judgement in charters (exploratory testing).
- Capture team heuristics in checklists and attack lists.
- Cross-feed: taxonomies inform heuristics; charters reveal new defect patterns.

**Don't:**
- Don't pretend checklists replace judgement; they augment it.
- Don't pretend judgement replaces checklists; it forgets lessons.
- Don't keep the lessons private; share at retrospectives.

**Code:**
```text
"Test charter ... SBTM (Session-based test management) ... checklist-
based testing"
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Glossary / 4.5"*

---

## Anti-Patterns & Common Mistakes

- **Conflating levels and types:** component test as acceptance test; system test that pretends to be unit. *Fix:* clarify at planning.
- **Exhaustive-testing claims:** "we've tested everything". *Fix:* report risks covered, not coverage of infinity.
- **Reliance on absence of errors:** "no defects found, ship it". *Fix:* also report validation evidence.
- **Date-only exit criteria:** stops tests on the calendar, not on quality. *Fix:* also criteria on coverage and rate.
- **Tester as gatekeeper:** QA rejects at the end; everyone else is innocent. *Fix:* whole-team approach; shift-left.
- **Static = review = informal:** skipping inspections where they matter. *Fix:* choose review type by artefact criticality.
- **One technique fits all:** EP for everything. *Fix:* combine EP, BVA, decision tables, state transition, use cases.
- **No traceability:** "yes, we covered it". *Fix:* trace requirements to cases and to executions.
- **Defect triage = rejection theater:** reject without reproducing. *Fix:* reproduce first; reject politely with evidence.
- **Tool purchase before need:** tool-first, process-second. *Fix:* process maturity and need first.
- **YAML CI heroics:** remote-only CI gates; debugging at midnight. *Fix:* testable CI/CD; on-call.
- **Production data as test data:** leak confidential data. *Fix:* anonymise or synthesise.
- **100% statement coverage as "done":** missing branches, missing paths. *Fix:* set coverage targets per level.
- **Vague defect reports:** "the system is broken". *Fix:* apply the IEEE 829 fields.
- **Tester-only "nonfunctional" testing:** perf/security as siloed skills. *Fix:* shift to the team; keep specialists.
- **Giant release; tiny confidence:** "we'll catch it in UAT". *Fix:* pyramid; testing at each level.
- **Skipping completion activities:** lessons lost, artefacts thrown away. *Fix:* make completion a milestone.

---

## Decision Heuristics / Checklists

- **Independent test team size:** 1 developer for low-risk; QA-aligned within team for medium; dedicated QA team for high; external QA for safety-critical.
- **Review formality:** informal < walkthrough < technical review < inspection. Match to artefact criticality.
- **Test technique mix:** EP + BVA for boundary defects; decision tables for combinatorics; state transitions for sequences; use cases for business flows.
- **Coverage requirement:** Component 100% branch; integration boundary coverage; system user-flow coverage; acceptance acceptance-criteria coverage.
- **Regression policy:** Always re-run impacted tests; expand to full regression for high-risk changes; spot-check otherwise.
- **Risk-driven exit:** multiply risk RPN by planned test cost; ship if benefits outweigh residual risk.
- **Tool ROI:** buy when the process is at Level 2+; otherwise the tool won't help.
- **Test data sourcing:** anonymise production; otherwise synthesise.
- **Defect triage cadence:** daily in production projects; weekly in maintenance.
- **Documentation format:** use IEEE 829 when regulated; use lean templates in agile; never freelance fields.

---

## Key Takeaways

1. Apply the seven principles of testing; pin them in your team's working contract.
2. Follow the seven-step test process; do not skip activities.
3. Layer techniques: black-box on specs; white-box on code; experience-based on judgement.
4. Use equivalence partitioning and boundary value analysis as a layered pair.
5. Build traceability in both directions; it pays off in audits and changes.
6. Match independence level to risk; safety-critical needs external QA.
7. Pick entry and exit criteria that are measurable, not "feels good".
8. Anonymise test data; respect regulatory constraints.
9. Use IEEE 829 templates where required; tailor otherwise.
10. Defects have lifecycles; triage them on a schedule, not ad hoc.

---

## Cross-References

- Related: `../The_Art_of_Unit_Testing.md` (unit-level depth; complements Chapter 4)
- Related: `../What_to_Test_and_When.md` (risk-driven test selection)
- Related: `../ATDD_Guide.md` (collaborative acceptance-test-driven development)
- Related: `../TDD_Top_Tips.md` (test-first unit-level tactics)
- Related: `../The_Feedback-Driven_Developer.md` (test feedback loops)
- Related: `../Modern_Software_Engineering.md` (test process in modern delivery)
- Related: `../Building_Evolutionary_Architectures.md` (test as fitness function for architecture)
- Topic index: `../INDEX.md`

---

## Quick Reference Card

| Decision                                    | Pick                                                         |
|---------------------------------------------|--------------------------------------------------------------|
| Technique for boundaries                    | EP + BVA layered pair                                        |
| Multi-condition logic                       | Decision tables                                              |
| Sequential behaviour                        | State transition testing (0-switch minimum)                 |
| Business scenarios                          | Use case testing                                             |
| Risk-driven test selection                  | Product RPN × test cost                                      |
| Independence for safety-critical            | External (separate economic entity)                          |
| Coverage target per level                   | 100% branch (component), boundary (integration), user-flow (system), acceptance-criteria (acceptance) |
| Review type per artefact                    | Informal < Walkthrough < Technical review < Inspection       |
| Test data                                   | Anonymised production OR synthesised                         |
| Tool class per need                         | Static (lint/SCA), design (model), execution (capture/replay), coverage, comparison, management, defect |
| Exit criteria                               | Coverage + risk + defect rate + planned-cases completed, not date alone |
| Defect triage                               | Daily in delivery; weekly in maintenance                     |
| Test reporting                              | Tailor by audience: testers / developers / leads / hierarchy / customers |

## Reading Order (for ISTQB Foundation prep)

1. Chapter 1 — Fundamentals, principles, process.
2. Chapter 2 — Lifecycle, levels, types, maintenance.
3. Chapter 3 — Reviews and static analysis.
4. Chapter 4 — Test design techniques (black-box, white-box, experience-based).
5. Chapter 5 — Management, planning, estimation, risk, defect.
6. Chapter 6 — Tools selection and use.
7. Chapter 7 — Mock exam for self-check.
8. Chapter 8 — IEEE 829 templates for documentation practice.
9. Chapter 9 — Answers review.

The fundamentals are the safest place to start; everything else layers on them.