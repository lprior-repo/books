# The DevOps Handbook — How to Create World-Class Agility, Reliability, and Security in Technology Organizations

**Author:** Gene Kim, Jez Humble, Patrick Debois, John Willis
**Topic tags:** `#devops` `#architecture` `#organization` `#leadership` `#reliability` `#security` `#continuous-delivery`
**Language focus:** Language-agnostic; principles and process patterns
**Sources:** `markdown_output/The_DevOps_Handbook/The_DevOps_Handbook.md` · `summaries/The_DevOps_Handbook.md`

## TL;DR
DevOps applies Lean, Theory of Constraints, and the Toyota Production System to the technology value stream through Three Ways — **Flow** (left-to-right delivery), **Feedback** (right-to-left fast signal), and **Continual Learning & Experimentation** (just culture, blameless post-mortems, fault injection). High performers deploy 30x more frequently, with 200x shorter lead times, 60x higher change success rates, and 168x faster MTTR — and they treat security, compliance, and operability as everyone's daily job rather than end-stage gates. Implement via: small batches, trunk-based CI, automated deployment pipeline, decoupled deploy/release, pervasive telemetry, peer review over external approvals, and loosely-coupled, two-pizza, market-oriented teams.

---

## Best Practices by Topic

### Part I — Foundations: The Three Ways

---

### 1. The Convergence of DevOps (Pre-History)

**Principle:** DevOps is the outcome of many mutually reinforcing management movements, not a single invention. John Willis calls this "the convergence of DevOps."

**Movements that converged:**
- **Lean (1980s):** Toyota Production System → VSM, kanban, Total Productive Maintenance; lead time predicts quality; small batches predict short lead times.
- **Agile Manifesto (2001):** "Deliver working software frequently… preference to the shorter timescale"; small self-motivated teams in high-trust management.
- **Velocity Conference (2007):** O'Reilly conference created by Steve Souders, John Allspaw, and Jesse Robbins for the IT Ops / Web Performance tribe.
- **"10 Deploys per Day: Dev and Ops Cooperation at Flickr" (Allspaw & Hammond, Velocity 2009):** The seminal talk that inspired the community.
- **Agile Infrastructure (Patrick Debois & Andrew Schafer, Agile Toronto 2008):** Birds-of-a-feather session; only two people attended but it seeded the community.
- **DevOpsDays Ghent (2009):** Patrick Debois coined "DevOps" here.
- **Continuous Delivery (Humble & Farley, 2006/2010):** Deployment pipeline; trunk always deployable.
- **Continuous Deployment (Tim Fitz, IMVU blog 2009):** Auto-deploy every good build.
- **Toyota Kata (Mike Rother, 2009):** Improvement kata and coaching kata — daily, habitual practice of improvement.
- **Lean Startup (Eric Ries):** Build-measure-learn loop; validated learning.
- **Lean UX (Jeff Gothelf):** Hypothesis-driven product design.
- **Rugged Computing (Josh Corman & David Rice):** Security as a quality attribute of resilient software.

**Do:**
- Cite the underlying movements when explaining DevOps to non-technologists — it builds a powerful coalition.

*Ref: The_DevOps_Handbook.md — "A BRIEF HISTORY"; Appendix 1 "THE CONVERGENCE OF DEVOPS"*

---

### 2. The Core, Chronic Conflict Between Dev and Ops

**Principle:** Two competing goals — "respond to the rapidly changing competitive landscape" (Dev) and "provide stable, reliable, secure service" (Ops) — must be pursued simultaneously; structurally separating them creates a downward spiral.

**Do:**
- Recognize that Dev and Ops have diametrically opposed incentives; redesign measurements so both share global goals.
- Treat technology work as one value stream from business hypothesis to customer value, not as Dev-then-Ops handoffs.
- Break the spiral by enabling fast flow AND world-class reliability simultaneously (Puppet Labs data proves they correlate positively).

**Don't:**
- Don't optimize Dev feature-completion rates or Ops availability in isolation — these are local optimizations that degrade global outcomes.
- Don't allow learned helplessness to set in when downstream teams are trapped by fragile systems they cannot fix.

*Ref: The_DevOps_Handbook.md — "THE CORE, CHRONIC CONFLICT"; "DOWNWARD SPIRAL IN THREE ACTS"*

---

### 3. The Downward Spiral in Three Acts (Diagnostic Pattern)

**Principle:** The core chronic conflict plays out in a recognizable three-act downward spiral; intervening early reverses it.

**The three acts:**
- **Act 1 (Ops):** Fragile, complex, poorly documented systems (technical debt) — most fragile artifacts support the most important revenue-generating or critical projects.
- **Act 2 (Business commitment):** Business commits Dev to an urgent project requiring shortcuts → adds tech debt with the promise to "fix it later" (which never comes).
- **Act 3 (Slowdown):** Work becomes more tightly coupled; smaller actions cause bigger failures; deployments stretch from minutes to hours to days to weeks; product cycles slow; fewer, less ambitious projects; weaker customer feedback; eventually lose in the marketplace.

**Do:**
- Watch for the spiral's signature: deployment lead times growing, %C/A dropping, change success rates falling, heroics becoming routine.
- Calculate the human cost: burnout, learned helplessness, lost high performers.
- Quantify the economic cost: the authors estimate $520B wasted globally per year on urgent/rework IT, and $2.6T of unrealized annual value creation.

**Don't:**
- Don't treat the spiral as inevitable — DevOps practices demonstrably reverse it (Puppet Labs data).

*Ref: The_DevOps_Handbook.md — "DOWNWARD SPIRAL IN THREE ACTS"; "THE COSTS: HUMAN AND ECONOMIC"*

---

### 4. The Three Ways as the Underpinning Theory

**Principle:** All DevOps practices derive from three principles: **First Way (Flow)** accelerates left-to-right work; **Second Way (Feedback)** amplifies right-to-left signals; **Third Way (Continual Learning)** creates a generative, high-trust, scientific culture.

**Do:**
- Use the First Way to drive down deployment lead time (months → minutes).
- Use the Second Way to detect and recover from problems while still small.
- Use the Third Way to convert local discoveries into global improvements and to deliberately inject stress.
- Sequence them: flow first, then feedback, then learning — each reinforces the others.

**Don't:**
- Don't adopt individual DevOps practices (CI, microservices, telemetry) without the underlying principles — they will not produce the predicted outcomes.

*Ref: The_DevOps_Handbook.md — "THE THREE WAYS: THE PRINCIPLES UNDERPINNING DEVOPS"*

---

### 5. The Technology Value Stream and Deployment Lead Time

**Principle:** Define the value stream as "business hypothesis → technology-enabled service delivering customer value," and measure **lead time** (request to fulfillment) and **process time** (touch time, excluding queue) separately.

**Do:**
- Track lead time from code commit to production-deployed-and-working.
- Recognize that Design/Dev resembles Lean Product Development (variable, creative) while Test/Ops resembles Lean Manufacturing (predictable, mechanistic) — they need different management.
- Drive toward deployment lead times of minutes by shrinking batch sizes and overlap design with testing.
- Track **%C/A (percent complete and accurate)** for every stage — ask downstream customers what fraction of incoming work is "usable as is."

**Don't:**
- Don't confuse process time with lead time — most lead time is queue time, invisible and unmeasured.
- Don't ship work downstream with rework baked in; %C/A below ~90% signals a process defect.

*Ref: The_DevOps_Handbook.md — "THE TECHNOLOGY VALUE STREAM"; "FOCUS ON DEPLOYMENT LEAD TIME"; "OBSERVING '%C/A' AS A MEASURE OF REWORK"*

---

### 6. Theory of Constraints Applied to IT (Goldratt's Five Focusing Steps)

**Principle:** "In any value stream, there is always one and only constraint; any improvement not made at that constraint is an illusion."

**The Five Steps:**
1. Identify the system's constraint.
2. Decide how to exploit it.
3. Subordinate everything else to that decision.
4. Elevate the constraint.
5. Repeat — but don't allow inertia to become the new constraint.

**Typical DevOps constraint progression:**
- Environment creation (weeks-long waits) → automate on-demand.
- Code deployment (1,300 manual steps) → automate self-service.
- Test setup and run (4-week manual regression) → automate and parallelize.
- Overly tight architecture (committee meetings for every change) → decouple.
- Eventually: Development / product owners — exactly where the constraint should sit.

**Do:**
- Move the bottleneck until it lands on "how many good business hypotheses we can generate" — then you have won.

**Don't:**
- Don't improve a non-bottleneck work center — work will merely pile up faster at the bottleneck or starve downstream centers.

*Ref: The_DevOps_Handbook.md — "CONTINUALLY IDENTIFY AND ELEVATE OUR CONSTRAINTS"*

---

### 7. Kingman's Formula — Utilization Drives Queue Explosion

**Principle:** Wait time = (% busy) / (% idle). As utilization approaches 100%, wait time grows asymptotically.

**Concrete math (from *The Phoenix Project*):**
- Resource 50% busy: wait = 50/50 = **1 hour**.
- Resource 90% busy: wait = 90/10 = **9 hours** (9x worse).
- 7 handoffs at 90% busy each: 7 × 9 = **63 hours** of queue time for a "30-second task."

**Implication:** For a 30-minute task with 7 handoffs at 90% utilization, only **0.16%** of total lead time is value-added. The other 99.84% is queue.

**Do:**
- Keep constrained work centers below ~80% utilization to keep queues bounded.
- Reduce the number of handoffs — each one is a queue opportunity.

**Don't:**
- Don't measure "efficiency" as utilization — high utilization of a non-bottleneck is waste; high utilization of a bottleneck is unrecoverable.

*Ref: The_DevOps_Handbook.md — Appendix 4 "THE DANGERS OF HANDOFFS AND QUEUES"*

---

### 8. The Six Myths of Industrial Safety (Besnard & Hollnagel)

**Principle:** Conventional accident-analysis instincts are based on busted myths; replace them with systems thinking.

| Myth | Reality |
|---|---|
| Human error is the largest cause of accidents. | Human error is the **effect** of systemic vulnerabilities deeper inside the organization. |
| Systems will be safe if people comply with procedures. | Procedures are inherently incomplete in complex systems. |
| Safety can be improved by adding more barriers/protection. | More layers add complexity and new failure modes. |
| Accident analysis can identify THE root cause. | Many contributing factors interact; no single "root cause." |
| Accident investigation is logical identification based on facts. | Investigation is shaped by hindsight and counterfactual reasoning. |
| Safety always has the highest priority. | Safety is routinely traded against production pressure. |

**Do:**
- Replace "what should they have done?" with "why did it make sense for them to do what they did?" (Dekker).
- Telling people to "be more careful" never fixes systemic vulnerabilities.

*Ref: The_DevOps_Handbook.md — Appendix 5 "MYTHS OF INDUSTRIAL SAFETY"*

---

### 9. The Eight Categories of Waste and Hardship (Lean Software)

**Principle:** Eliminate hardships in daily work; waste compounds like financial debt.

**Categories (Poppendieck, adapted):**
- Partially done work (obsolete, loses value over time)
- Extra processes (reviews/approvals that add no value)
- Extra features ("gold plating")
- Task switching (multitasking destroys throughput)
- Waiting (delays increase cycle time)
- Motion (effort to move info between teams)
- Defects (longer time-to-detection = harder fix)
- Nonstandard or manual work (snowflake servers, manual configs)
- Heroics (2 a.m. firefights as a normal pattern)

**Do:**
- Make wastes visible; systematically do what is needed to alleviate them.
- Reframe "waste elimination" as "reducing hardship and drudgery" — more humane, less dehumanizing.

**Don't:**
- Don't tolerate heroics as a permanent operating mode — it is a symptom of systemic failure, not dedication.

*Ref: The_DevOps_Handbook.md — "ELIMINATE HARDSHIPS AND WASTE IN THE VALUE STREAM"*

---

### 10. The Westrum Organizational Typology — Predict Culture, Predict Performance

**Principle:** Organizational culture is a top predictor of safety and IT performance; generative cultures outperform bureaucratic and pathological ones.

| Pathological | Bureaucratic | Generative |
|---|---|---|
| Information hidden | Information ignored | Information actively sought |
| Messengers shot | Messengers tolerated | Messengers trained |
| Responsibilities shirked | Compartmented | Shared |
| Bridging discouraged | Allowed but discouraged | Rewarded |
| Failure covered up | Just and merciful | Failure causes inquiry |
| New ideas crushed | Create problems | Welcomed |

**Do:**
- Strive for generative: shared responsibility, inquiry after failure, rewarded cross-team bridging.
- Use Westrum's typology as a leading indicator — it predicts IT performance in the State of DevOps data.

**Don't:**
- Don't expect tooling to fix a pathological or bureaucratic culture; tools amplify the prevailing culture.

*Ref: The_DevOps_Handbook.md — "ENABLING ORGANIZATIONAL LEARNING AND A SAFETY CULTURE"*

---

### 11. DORA / State of DevOps Outcomes (The Four Metrics)

**Principle:** High performers simultaneously achieve throughput AND reliability — the chronic conflict is resolvable.

**The Four Metrics (from Puppet Labs State of DevOps Reports 2013–2016):**
- **Deployment frequency:** 30x more frequent in high performers.
- **Lead time:** 200x faster (minutes/hours vs months/quarters).
- **Change success rate:** 60x higher.
- **MTTR:** 168x faster (minutes vs days).

**Corollary findings:**
- 2x more likely to exceed profitability, market share, and productivity goals.
- 50% higher 3-year market capitalization growth.
- 2.2x more likely to be recommended as a great place to work.
- Spend 50% less time remediating security issues.
- Deploys per developer *increase linearly* with team size for high performers — and *decrease* for low performers.

**Do:**
- Track all four metrics together — optimizing one alone (e.g., deploy frequency) destroys the others if done without discipline.

*Ref: The_DevOps_Handbook.md — "THE BUSINESS VALUE OF DEVOPS"; "DEVOPS HELPS SCALE DEVELOPER PRODUCTIVITY"*

---

### Part II — Where to Start: Value Streams and Organization Design

---

### 12. Selecting the First Value Stream to Transform

**Principle:** Pick the value stream where you can demonstrate early wins with the least risk; "little fish learn to be big fish in little ponds."

**Do:**
- Consider both **greenfield** (new) and **brownfield** (existing) services — brownfield often has the highest business benefit. Over 60% of DevOps Enterprise Summit 2014 transformations were brownfield.
- Consider both **systems of record** (correctness-critical, e.g., ERP) and **systems of engagement** (fast-changing, customer-facing). Both deserve speed AND quality — reject "bimodal IT" as a permanent state.
- Start with **innovators and early adopters** (Geoffrey Moore's curve), not the laggards.

**Don't:**
- Don't attempt a big-bang, top-down transformation unless you have relentless executive support (e.g., PayPal Agile 2012). Even then, prefer organic growth.

*Ref: The_DevOps_Handbook.md — "GREENFIELD VS. BROWNFIELD SERVICES"; "CONSIDER BOTH SYSTEMS OF RECORD AND SYSTEMS OF ENGAGEMENT"; "START WITH THE MOST SYMPATHETIC AND INNOVATIVE GROUPS"*

---

### 13. Expanding DevOps: Innovators → Silent Majority → Holdouts

**Principle:** Build a coalition in three phases (adapted from Dr. Roberto Fernandez, MIT).

**Phases:**
1. **Find innovators and early adopters** — kindred spirits who volunteer; ideally people respected and influential.
2. **Build critical mass and silent majority** — expand to receptive teams to create a bandwagon effect; bypass political battles.
3. **Identify the holdouts** — only tackle high-profile detractors after you have protected the initiative with cumulative successes.

**Do:**
- Demonstrate early wins and broadcast successes broadly.
- Break large improvement goals into small, incremental steps so you can detect wrong value-stream choices quickly.

*Ref: The_DevOps_Handbook.md — "EXPANDING DEVOPS ACROSS OUR ORGANIZATION"*

---

### 14. Case Study — Nordstrom (2013–2015)

**Principle:** A traditional retailer optimized for cost can repivot to optimize for speed by picking the right initial value streams and scaling from there.

**Three initial focus areas (Courtney Kissler):**
1. **Mobile application:** Universally negative App Store reviews; releases only twice/year. → Created dedicated product team with single prioritized backlog; integrated testing into daily work; eliminated testing as a separate phase. **Result: 2x features/month, ½ the defects.**
2. **In-store Café Bistro restaurant systems:** Brownfield with planned 4x increase in change rate. → Identified work-intake and deployment bottlenecks. **Result: 60% reduction in deployment lead time, 60–90% reduction in production incidents.**
3. **Digital properties.**

**Scaling (2015):** Across-the-board mandate to reduce cycle times by 20% for all customer-facing services. Kissler: "We have many problems in our current state — process and cycle times are not consistently measured across teams, nor are they visible. Our first target condition requires us to help all our teams measure, make it visible, and perform experiments."

*Ref: The_DevOps_Handbook.md — "Selecting Which Value Stream to Start With" (Nordstrom case study)*

---

### 15. Case Study — Etsy (2009–2014)

**Principle:** A near-death holiday season can be the catalyst for a transformation that ends in IPO and industry admiration.

**2009 starting state:** 35 employees, $87M revenue, "barely survived the holiday retail season," myriad unsupported technologies (lighttpd, Postgres, MongoDB, Scala, CoffeeScript, Python).

**Transformation pillars (Michael Rembetsy, Patrick McDonnell):**
- Standardized on LAMP stack (Linux/Apache/MySQL/PHP) — philosophical choice so Dev and Ops could all read/fix each other's code.
- Created StatsD (one-line code instrumentation) — "the Church of Graphs."
- 200,000 production metrics by 2011; **800,000+ by 2014**.
- Deployments 25–50x/day by 2011; new engineers deploy on day one.
- "Deploy dashboard" with top 30 business metrics; deployment events overlaid on every graph.
- TV screens around the office radiating metrics.
- Blameless post-mortem tooling (Morgue) — P2/P3/P4 post-mortems recorded at far higher rates.

**Outcome:** 2015 IPO; one of the most admired DevOps organizations in the industry.

*Ref: The_DevOps_Handbook.md — "Etsy (2009)" case study; "Case Study Etsy—Self-Service Developer Deployment"; "INSTRUMENTING THE ENVIRONMENT AT ETSY"*

---

### 16. Case Study — Knight Capital (August 1, 2013)

**Principle:** A 15-minute deployment error can destroy a firm; the instinct to "add more change control" makes the next failure more likely, not less.

**What happened:**
- $440M trading loss in approximately 15 minutes.
- Engineering teams unable to disable the production services during the incident.
- Firm sold over the weekend to avoid destabilizing the financial system.

**Two counterfactual narratives (Allspaw):**
- "Change control failure" — better change control could have caught it earlier.
- "Testing failure" — better testing could have identified the risk.

**Why typical responses backfire:**
- Adding more questions to the change request form, more approvals, more stakeholders → longer lead times → larger batch sizes → weaker feedback → **worse** outcomes.
- The further the approver from the work, the worse the decision quality.

**Lesson:** Real safety comes from fast feedback, peer review, automated testing, and small batches — not from heavier external approval gates.

*Ref: The_DevOps_Handbook.md — "THE DANGERS OF CHANGE APPROVAL PROCESSES" (Knight Capital case)*

---

### 17. Case Study — ING (Bimodal Rejection, Market-Oriented Teams)

**Principle:** A bank can rebuild itself in the image of a tech company; explicitly reject "bimodal IT."

**Ron van Kemenade (CIO, ING):**
- "We've adopted a philosophy that rejects bi-modal IT, because every one of our customers deserve speed and quality. This means technical excellence whether the team is supporting a 30-year-old mainframe application, a Java application, or a mobile application."
- Reorganized into ~350 squads of ≤9 people (sound familiar? — Spotify model).
- "Leading change requires courage, especially in corporate environments where people are scared and fight you. But if you start small, you really have nothing to fear."

*Ref: The_DevOps_Handbook.md — "CONSIDER BOTH SYSTEMS OF RECORD AND SYSTEMS OF ENGAGEMENT"; "EXPANDING DEVOPS ACROSS OUR ORGANIZATION"*

---

### 18. Case Study — Salesforce.com (2007–2013)

**Principle:** A SaaS leader can completely reverse from "one release per year" to "five-minute deployment lead times" through systematic DevOps adoption.

**Trajectory:**
- 2006: 4 major customer releases.
- 2007: 1 release despite hiring more engineers — features per team decreasing.
- Waterfall → incremental delivery transformation begins (Karthik Rajan).
- 2009: Dave Mangot and Reena Mathew lead multi-year DevOps transformation.
- 2013: **Deployment lead time: 6 days → 5 minutes.** Transactions/day scaled past 1 billion.

**Key practices:**
- Quality engineering as everyone's job (Dev, Ops, Infosec).
- Created open-source Rouster for functional testing of Puppet modules.
- **Destructive testing:** deliberately load services until they break to learn failure modes — significantly higher quality at normal production loads.
- Infosec worked with QE from earliest project stages.
- Change management agreed: **infrastructure changes via Puppet = standard changes**; manual infrastructure changes still require CAB approval.

*Ref: The_DevOps_Handbook.md — "Case Study Automated Infrastructure Changes as Standard Changes at Salesforce.com"*

---

### 19. Value Stream Mapping (VSM)

**Principle:** Assemble all stakeholders (Product, Dev, QA, Ops, Infosec, Release Mgmt, executives) and map every step from request to customer value, with lead time, process time, and %C/A for each block.

**Do:**
- Run a multi-day workshop; produce 5–15 high-level process blocks within hours (not exhaustive detail).
- Scrutinize where work waits weeks (env. creation, CAB, security review) and where significant rework is generated or received.
- Build a future-state VSM as the 3–12 month target condition.
- After the workshop, run targeted experiments (e.g., Nordstrom's Cosmetics app: deleting one form field cut 4 days of processing time).

**Don't:**
- Don't allow the map to become an end in itself — the goal is to identify and act on impediments to flow.

*Ref: The_DevOps_Handbook.md — "CREATE A VALUE STREAM MAP TO SEE THE WORK"*

---

### 20. The Dedicated Transformation Team

**Principle:** Empower a small team to drive the transformation with a shared goal, short planning horizons, and protected capacity for non-functional requirements.

**Do:**
- Agree on a shared, measurable goal (e.g., "reduce cycle times by 20% across all customer-facing services" — Nordstrom 2015).
- Keep improvement planning horizons short (weeks, not quarters).
- **Reserve ~20% of cycles for non-functional requirements and tech-debt reduction** — perpetual firefighting is the alternative.
- Increase visibility of work and use tools (VCS, deployment pipeline, automated tests) to reinforce desired behaviors.

*Ref: The_DevOps_Handbook.md — "CREATING A DEDICATED TRANSFORMATION TEAM"; "RESERVE 20% OF CYCLES FOR NON-FUNCTIONAL REQUIREMENTS"*

---

### 21. Conway's Law and Organizational Design

**Principle:** "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."

**Organizational archetypes:**
- **Functional** (DBAs, network, etc.) — optimizes for expertise, creates handoffs.
- **Market-oriented** (full-stack teams owning a service end-to-end) — optimizes for speed and autonomy.

**Do:**
- Enable market-oriented teams ("two-pizza teams") whenever possible.
- Make testing, operations, and security **everyone's** job, every day.
- Enable every team member to be a generalist (reduce single-points-of-knowledge).
- **Fund services and products, not projects** — long-lived teams accumulate feedback; project teams disband and lose learning.
- Design team boundaries to produce the architecture you want — Conway's Law is deterministic.
- Keep team sizes small (Amazon "two-pizza" rule).

**Don't:**
- Don't expect a tightly-coupled architecture from a functionally siloed org chart.

*Ref: The_DevOps_Handbook.md — "ORGANIZATIONAL ARCHETYPES"; "ENABLE MARKET-ORIENTED TEAMS"; "FUND NOT PROJECTS, BUT SERVICES AND PRODUCTS"; "KEEP TEAM SIZES SMALL"*

---

### 22. Integrating Operations into Dev's Daily Work

**Principle:** Operations must become a platform that amplifies developer productivity rather than a gate that blocks it.

**Do:**
- Create **shared services** (deployment pipelines, automated test tools, environments) that operate as internal products with Dev as customer.
- Embed Ops engineers into service teams.
- Assign an Ops liaison to each service team.
- Invite Ops to Dev standups, demos, and retrospectives; make relevant Ops work visible on shared Kanban boards.
- Define feature-launch plans jointly across Dev and Ops.

**Don't:**
- Don't isolate Ops in a ticket-driven request queue — that maximizes handoffs and minimizes learning.

*Ref: The_DevOps_Handbook.md — "How to Get Great Outcomes by Integrating Operations into the Development Process"; "CREATE SHARED SERVICES TO INCREASE DEVELOPER PRODUCTIVITY"; "INTEGRATE OPS INTO DEV RITUALS"*

---

### Part III — The First Way: Technical Practices of Flow

---

### 23. On-Demand Creation of Production-Like Environments

**Principle:** Anyone should be able to spin up a production-like environment in minutes, self-service, without a ticket.

**Do:**
- Build one common mechanism that creates dev, test, and production environments from version-controlled definitions (Vagrant, Docker, Terraform, CloudFormation, Puppet, Chef, Ansible, AMIs, Packer).
- Have developers run production-like environments on their workstations daily.
- Codify all environment requirements in automation — not in documents or someone's head.

**Outcome reference:** Em Campbell-Pretty's team cut environment-delivery time at an Australian telco from 8 weeks to 1 day; only 50% of source in dev/test matched production before the fix.

*Ref: The_DevOps_Handbook.md — "ENABLE ON DEMAND CREATION OF DEV, TEST, AND PRODUCTION ENVIRONMENTS"*

---

### 24. The Single Repository of Truth — Everything in Version Control

**Principle:** Version control is not just for application code; it is the source of truth for the entire reproducible system.

**Check into version control:**
- All application code and dependencies
- Database schemas, reference data, migration scripts
- Environment creation tools/artifacts (Puppet manifests, AMIs, Dockerfiles)
- All automated and manual test scripts
- Build, packaging, deployment, provisioning scripts
- Project artifacts (requirements, deployment procedures, release notes)
- Cloud config files (CloudFormation, ARM, HEAT)
- DNS zones, firewall rules, ESB configurations

**Do:**
- Store large binaries in artifact repositories (Nexus, Artifactory, S3, Docker registries) referenced from VCS.
- Put build tools and their environments under VCS too — they must be reproducible.

**Don't:**
- Don't underestimate this finding: **whether Ops used version control was a higher predictor of IT and organizational performance than whether Dev did** — because there are orders of magnitude more configurable settings in environments than in code.

*Ref: The_DevOps_Handbook.md — "CREATE OUR SINGLE REPOSITORY OF TRUTH FOR THE ENTIRE SYSTEM"*

---

### 25. Make Infrastructure Easier to Rebuild Than to Repair

**Principle:** Servers are cattle, not pets — number them, and when they get sick, shoot them.

**Do:**
- Adopt **immutable infrastructure** — the only path to production change is through VCS and a rebuild.
- Disable remote logins to production servers; require changes through configuration management.
- Routinely kill and replace production instances (Netflix average AWS instance age: 24 days; 60% < 1 week old).
- Keep pre-production environments continuously up to date — developers running on stale environments hide problems.

**Don't:**
- Don't allow snowflake servers, "works of art," or configuration drift to accumulate.

*Ref: The_DevOps_Handbook.md — "MAKE INFRASTRUCTURE EASIER TO REBUILD THAN TO REPAIR"*

---

### 26. Expand the Definition of "Done"

**Principle:** Done means running successfully in a production-like environment, not "code complete on a laptop."

**Progressive expansion of Done:**
1. "...working and potentially shippable code..." (Scrum baseline)
2. "...**demonstrated in a production-like environment**..." (after env-on-demand)
3. "...**created from trunk via one-click process and validated with automated tests**..." (after CI)

**Do:**
- Use the same monitoring, logging, and deployment tools in pre-production as production.

*Ref: The_DevOps_Handbook.md — "MODIFY OUR DEFINITION OF DEVELOPMENT 'DONE' TO INCLUDE RUNNING IN PRODUCTION-LIKE ENVIRONMENTS"; Continuous Integration chapter*

---

### 27. The Deployment Pipeline (Humble & Farley)

**Principle:** Every commit triggers an automated build-test-deploy sequence in a dedicated environment; the pipeline becomes the source of truth for deployability.

**Stages:**
- **Commit stage:** build, package, unit tests, static analysis, style/coverage checks.
- **Acceptance stage:** deploy package to production-like env, run acceptance tests.
- **Integration / UAT / performance / security stages** in parallel as appropriate.
- **Production deployment** (manual or automatic).

**Do:**
- Build once, promote the **same artifact** through every environment — never rebuild differently for production.
- Treat pipeline configuration as code (versioned, reviewable, recoverable).
- Capture every test result, deployment, and audit event in pipeline history.

**Don't:**
- Don't hide manual testing inside a "nominally automated" pipeline.
- Don't let commits queue indefinitely behind a stopped production stage.

*Ref: The_DevOps_Handbook.md — "CONTINUOUSLY BUILD, TEST, AND INTEGRATE OUR CODE AND ENVIRONMENTS"; "BUILD A FAST AND RELIABLE AUTOMATED VALIDATION TEST SUITE"*

---

### 28. The Automated Testing Pyramid

**Principle:** Most defects should be caught by fast, numerous unit tests — not slow, brittle end-to-end tests.

**Layers (fast → slow):**
- **Unit tests:** single method/class/function in isolation; stub external dependencies; should run in minutes.
- **Acceptance tests:** whole application against business criteria ("does what the customer meant, not what programmers think").
- **Integration tests:** real interactions with other services; keep these minimal — they are brittle.
- **Manual/exploratory:** only what cannot be automated.

**Do:**
- Aim for the Martin Fowler "ideal pyramid" — broad base of unit tests.
- Run faster stages before slower stages; run performance and security in parallel after acceptance passes.
- Target a **ten-minute commit-stage build** (Fowler) — first stage compiles and runs unit tests with DB stubbed.
- When a defect slips past unit tests, write a new unit test that would have caught it (push tests down the pyramid).

**Don't:**
- Don't write tests that generate false positives (flaky tests erode trust and get disabled).
- Don't accept "non-ideal inverted pyramids" where most tests are manual or integration — that signals a tightly-coupled architecture.
- Don't write a large unreliable suite; a few reliable tests beat many unreliable ones (Gary Gruver at Macy's: 1,300 manual tests every 10 days → 10 trusted automated tests per commit, growing to hundreds of thousands).

*Ref: The_DevOps_Handbook.md — "BUILD A FAST AND RELIABLE AUTOMATED VALIDATION TEST SUITE"; "CATCH ERRORS AS EARLY IN OUR AUTOMATED TESTING AS POSSIBLE"*

---

### 29. Test-Driven Development (TDD) and ATDD

**Principle:** Write the failing automated test first; then write code to pass; then refactor.

**TDD three steps (Kent Beck):**
1. Write a test for the next bit of functionality — ensure it fails. Check in.
2. Write code until the test passes. Check in.
3. Refactor old and new code. Ensure tests still pass. Check in.

**Evidence:** Microsoft Research / IBM / NC State study found TDD teams produce 60–90% better defect density for only 15–35% more development time.

**Do:**
- Treat the test suite as the living specification of the system.
- Practice ATDD (acceptance test-driven development) so the customer-visible behavior drives the work.

*Ref: The_DevOps_Handbook.md — "WRITE OUR AUTOMATED TESTS BEFORE WE WRITE THE CODE ('TEST-DRIVEN DEVELOPMENT')"*

---

### 30. Integrate Performance and Non-Functional Testing

**Principle:** Performance, security, scalability, capacity, and configurability are first-class test categories — automate them in the pipeline.

**Do:**
- Run performance tests across the full stack; fail if results deviate >2% from prior baseline.
- Run infrastructure-as-code tests (Cucumber/Gherkin, ServerSpec, puppet-lint, foodcritic) alongside code tests.
- Log every build/test performance metric so you can detect regressions ("builds suddenly take 2x as long").

*Ref: The_DevOps_Handbook.md — "INTEGRATE PERFORMANCE TESTING INTO OUR TEST SUITE"; "INTEGRATE NON-FUNCTIONAL REQUIREMENTS TESTING INTO OUR TEST SUITE"*

---

### 31. Pull the Andon Cord When the Pipeline Breaks

**Principle:** When a commit breaks the build or any automated test, **stop the line** — no new work enters until green is restored.

**Do:**
- Notify the whole team immediately; anyone may roll back the commit.
- Optionally configure VCS to reject further commits until the commit stage is green.
- Bring in whatever help is needed; swarm the problem like Toyota's assembly line stop.
- When later stages (acceptance, perf) fail, write a new test for an earlier stage to catch the regression next time.
- Use highly visible signals: build lights, lava lamps, klaxons.

**Why:** Without the Andon cord, broken builds cascade: more commits land on broken code, no one sees failing tests, and you regress to a "stabilization phase" at the end of every release.

**Reference behavior (Google):** "There are no hard policies... there is mutual respect between teams and an implicit agreement that everyone does whatever it takes to keep the deployment pipeline running."

*Ref: The_DevOps_Handbook.md — "PULL OUR ANDON CORD WHEN THE DEPLOYMENT PIPELINE BREAKS"; Appendix 6 "THE TOYOTA ANDON CORD"*

---

### 32. The Toyota Andon Cord — 55-Second Rule

**Principle:** The Toyota Andon cord works because the time pressure is short and the response is mechanized — not because workers are exhorted to "stop the line."

**Mechanics:**
- Every work center has an Andon cord (or button).
- When pulled, the team leader is alerted and **has 55 seconds** to resolve the issue.
- If unresolved in 55 seconds, the partially assembled vehicle crosses a physical line on the floor and **the entire assembly line stops**.
- The whole organization mobilizes to assist until a countermeasure is developed.

**Counterintuitive behaviors observed:**
- Toyota pulls the Andon cord thousands of times per day — most pulls do NOT stop the line (resolved within 55 seconds).
- **When Andon cord pulls drop, plant managers decrease tolerances to INCREASE pulls** — to keep finding ever-weaker failure signals and continue learning.

**Translation to software:**
- Set a strict time budget for a broken build (e.g., 10 minutes) before escalating.
- Build automated Andon equivalents: red build light, chat notification, blocked further commits.
- Treat a drop in "broken build" events with suspicion — it may signal hidden problems, not health.

*Ref: The_DevOps_Handbook.md — "SWARM AND SOLVE PROBLEMS TO BUILD NEW KNOWLEDGE"; Appendix 6 "THE TOYOTA ANDON CORD"*

---

### 33. Continuous Integration — Trunk-Based, Daily Commits

**Principle:** All developers commit to trunk at least daily; small batches; the merge is the work.

**Practices:**
- Trunk-based development (or short-lived branches merged daily) over long-lived feature branches.
- Each commit triggers the deployment pipeline.
- **Gated commits:** pipeline confirms the change merges, builds, and passes tests before being accepted into trunk.

**HP LaserJet Firmware case study (Gary Gruver):**
- 400 developers across US, Brazil, India.
- Before: 5% of time on innovation; releases every 6 months; 6-week manual regression; 25% time porting code branches; 20% detailed planning (misattributed to estimation).
- Strategy: trunk-based CI, hardware simulator farm (2,000 printer simulators on 6 racks), single firmware supporting 24 product lines defined at runtime by XML config (replacing compile-time `#ifdef` flags).
- After: 100+ commits/day (was 20, performed by a "build boss"); regression in <1 day (was 6 weeks); innovation time **5% → 40%**; dev costs cut **40%**; programs-in-flight **up 140%**; cost-per-program **down 78%**.

**Bazaarvoice case study (Ernest Mueller):**
- 5M LOC monolithic Java application across 1,500 files, 1,200 servers, 4 datacenters.
- January 2012 biweekly release: **44 customer incidents.**
- Six weeks of CI investment (JUnit unit tests, Selenium regression, TeamCity pipeline) → March 6: 5 incidents → March 22: 1 incident → **April 5, 2012: zero customer incidents.**
- Then weekly, then continuous delivery with one-click deployments.
- Eliminated Staging environment (Dev/Test/Production only).

**Do:**
- Recognize: integration effort grows **exponentially** with the number and age of branches.
- Refactoring thrives on trunk-based dev; large-batch merges freeze refactoring.

*Ref: The_DevOps_Handbook.md — "Enable and Practice Continuous Integration"; "ADOPT TRUNK-BASED DEVELOPMENT PRACTICES"; "Case Study Continuous Integration at Bazaarvoice"*

---

### 34. Automate the Deployment Process

**Principle:** Script every step from package to production; remove handoffs.

**Automate:**
- Code packaging, VM/container image creation
- Middleware deployment and configuration
- File copy/restart/template generation
- Smoke tests
- Database migrations (often the hardest)

**Requirements for the deployment pipeline (deploy stage):**
- Deploy the **same way** to every environment.
- Smoke-test every deployment (DB, message bus, external services, one transaction end-to-end).
- Maintain environment consistency.

**CSG International case (Scott Prugh):**
- Created Shared Operations Team doing daily deployments across all environments.
- Result: incidents down 91%, MTTR down 80%, lead time 14 days → 1 day.
- "Deployments became so routine that the Ops team was playing video games by the end of the first day."

*Ref: The_DevOps_Handbook.md — "AUTOMATE OUR DEPLOYMENT PROCESS"*

---

### 35. Self-Service Deployments

**Principle:** Anyone (Dev or Ops) should be able to push the deploy button; the Puppet Labs 2013 data shows **no statistically significant difference in change success** between Dev-deployed and Ops-deployed organizations.

**Do:**
- Make build packages deployable to any environment.
- Make tests runnable on demand by anyone.
- Make deploy scripts checked into VCS and runnable via the pipeline.
- Provide push-button self-service for any suitable version.

**Etsy case:** New engineers deploy to production on day one — as have board members and dogs. Queue is managed in chat; 25+ changesets before 8 a.m. on a normal business day.

*Ref: The_DevOps_Handbook.md — "ENABLE AUTOMATED SELF-SERVICE DEPLOYMENTS"; "Case Study Etsy—Self-Service Developer Deployment"*

---

### 36. Decouple Deployment from Release

**Principle:** Deployment = installing a version into an environment. Release = exposing a feature to customers. They are different actions; separate them.

**Two release-pattern families:**
- **Environment-based:** blue-green, canary, cluster immune system (no app code changes).
- **Application-based:** feature toggles, dark launches (requires Dev involvement).

*Ref: The_DevOps_Handbook.md — "DECOUPLE DEPLOYMENTS FROM RELEASES"*

---

### 37. Blue-Green Deployment

**Principle:** Maintain two production environments; only one serves live traffic at a time. Deploy to the inactive one, test, switch traffic.

**Do:**
- Switch via load balancer, router, symlink, or DNS — fast and reversible.
- Roll back by switching traffic back.

**Database challenge:** Two app versions may share one DB.
- Option A: blue and green databases; backup-restore-switch (risk: lost transactions on rollback).
- Option B (preferred): **decouple DB changes from app changes** — only additive changes (expand/contract); never mutate existing objects; assume either DB version may be live.

**Dixons Retail POS case (North & Farley):** Blue-green over slow WAN links to thousands of retail POS systems; store managers chose release timing.

*Ref: The_DevOps_Handbook.md — "The Blue-Green Deployment Pattern"; "Dealing with Database Changes"*

---

### 38. Canary Releases and the Cluster Immune System

**Principle:** Deploy to successively larger cohorts, monitoring each; roll back automatically when metrics deviate.

**Facebook canary tiers:**
- **A1:** internal employees only.
- **A2:** small percentage of customers.
- **A3:** rest of production.

**Cluster immune system (IMVU, Etsy, Netflix):** Link production monitoring to release automation; auto-rollback when user-facing metrics (e.g., new-user conversion dropping below 15–20%) deviate from expected.

**Benefit:** Catches defects hard for automated tests to find (e.g., a CSS change hiding a critical element); reduces time-to-detection dramatically.

*Ref: The_DevOps_Handbook.md — "The Canary and Cluster Immune System Release Patterns"*

---

### 39. Feature Toggles and Dark Launches

**Principle:** Wrap new functionality in conditional logic so it can be enabled/disabled per user segment without redeploying.

**Feature toggle benefits:**
- Roll back by toggling off — no redeploy needed.
- Gracefully degrade under load by disabling expensive features.
- Decouple service dependencies — deploy behind a toggle, enable when the dependency is ready.

**Dark launching:** Deploy invisible functionality to production; route real production traffic through it; discard or log results. Use to load-test long before launch.

**Facebook Chat (2008) dark launch:**
- Code in production daily for nearly a year; hidden by Gatekeeper.
- Every Facebook user's browser ran a hidden chat test harness sending traffic to the chat backend.
- On launch day: "went from zero to seventy million users overnight" with no surprises — incremental rollout 1% → 5% → … → 100%.

**Do:**
- Run acceptance tests with all toggles ON.
- Test the toggling mechanism itself.

*Ref: The_DevOps_Handbook.md — "Implement Feature Toggles"; "Perform Dark Launches"; "Case Study Dark Launch of Facebook Chat"*

---

### 40. Continuous Delivery vs Continuous Deployment (Humble's 2015 Definitions)

**Principle:** CDelivery and CDeployment are different — and that's okay; outcomes matter more than labels.

- **Continuous delivery:** trunk always releasable; release on demand at push of a button during business hours; regressions fixed immediately.
- **Continuous deployment:** CDelivery + every good build is deployed to production (typically ≥ once per day per developer, or automatically per commit).

**Do:**
- Recognize CDelivery is the prerequisite for CDeployment, and CI is prerequisite for CDelivery.
- Choose per-team: at Google and Amazon most teams do CDelivery, some do CDeployment — teams choose based on the risks they manage.

*Ref: The_DevOps_Handbook.md — "SURVEY OF CONTINUOUS DELIVERY AND CONTINUOUS DEPLOYMENT IN PRACTICE"*

---

### 41. Architect for Low-Risk Releases — Evolutionary Architecture

**Principle:** Architecture evolves. eBay and Google are each on their fifth full rewrite. "Any successful product or organization will necessarily evolve over its life cycle." (Humble)

**Attributes of architectures that enable productivity, testability, and safety:**
- Loosely-coupled with well-defined interfaces enforcing how modules connect.
- Each service small enough for a "two-pizza" team to own end-to-end.
- Each service has an API enabling contracts/SLAs between teams.
- Layered dependable services (e.g., Google Cloud Datastore on Megastore on Bigtable on Colossus on Cluster Manager) — Cloud Datastore is one of the world's largest NoSQL services and is run by ~8 people.

**Do:**
- Make architecture match your desired team structure (Conway's Law).
- Treat monoliths as a valid early-stage choice — but plan for evolution.

*Ref: The_DevOps_Handbook.md — "AN ARCHITECTURE THAT ENABLES PRODUCTIVITY, TESTABILITY, AND SAFETY"; "ARCHITECTURAL ARCHETYPES: MONOLITHS VS. MICROSERVICES"*

---

### 42. The Strangler Application Pattern

**Principle:** Put legacy functionality behind an API and stop enhancing it; build all new functionality in the new architecture, calling the legacy when necessary. Gradually the new system "strangles" the old.

**When to use:** Migrating away from tightly-coupled monoliths (eBay C++ → Java; Amazon OBIDOS; Twitter Rails; LinkedIn Leo).

**Do:**
- Run small pilot first (eBay: sort pages by revenue, attack the highest-value ones first).
- Never rip-and-replace — that path collapses under its own weight.

*Ref: The_DevOps_Handbook.md — "USE THE STRANGLER APPLICATION PATTERN TO SAFELY EVOLVE OUR ENTERPRISE ARCHITECTURE"; "Case Study Strangler Pattern at Blackboard Learn"*

---

### 43. Designing for Manufacturability — Optimize for the Downstream Work Center

**Principle:** Lean recognizes two customers: external (pays) and **internal** (next step downstream). The most important customer is the next step downstream — design for them with empathy.

**Manufacturing examples (1980s Design for Manufacturability movement):**
- Parts wildly asymmetrical so they cannot be put on backwards.
- Screw fasteners impossible to over-tighten.

**Software translation:**
- Operational NFRs (architecture, performance, stability, testability, configurability, security) prioritized as highly as user features.
- Codify NFRs into every service proactively — not bolted on later.

**Quote:** "Our most important customer is our next step downstream."

**Counter-pattern (British colonial Georgia, 1700s):** Three thousand miles of distance between decision-makers (London) and the work (Georgia land chemistry, topography, water access) produced dismal agricultural outcomes — the command-and-control exemplar.

*Ref: The_DevOps_Handbook.md — "ENABLE OPTIMIZING FOR DOWNSTREAM WORK CENTERS"*

---

### 44. Case Study — Facebook (Daily to Thrice-Daily Deployments)

**Principle:** Increase deployment frequency to handle more changes — Chuck Rossi's observation that there's a fixed number of changes per deployment.

**Facebook 2012 process (Chuck Rossi, Director of Release Engineering):**
- ~1 p.m.: switch to "operations mode."
- All developers with changes going out must be present and check in on IRC.
- Absent developers' changes auto-removed from deployment package.
- Test dashboards and canary tests must be green.
- "Big red button" push delivers new code to the entire Facebook.com fleet.
- Within 20 minutes, thousands of machines on new code with no visible user impact.

**Later that year:** Doubled to twice-daily deployments — gave non-West-Coast engineers equal shipping cadence.

**Kent Beck (Facebook technical coach):** "Chuck Rossi made the observation that there seem to be a fixed number of changes Facebook can handle in one deployment. If we want more changes, we need more deployments."

**PHP-specific note:** PHP code converted to C++ via HipHop compiler → 1.5 GB executable → BitTorrent copy to all servers in 15 minutes.

*Ref: The_DevOps_Handbook.md — "12Automate and Enable Low-Risk Releases" (Facebook case study)*

---

### 45. COTS Software in Version Control

**Principle:** Commercial off-the-shelf software (SAP, WebSphere, Oracle WebLogic) must also be in version control — eliminate graphical installers.

**Procedure:**
1. Install on a clean server image.
2. Diff the file system to capture everything added.
3. Put non-environment-specific files in "base install"; environment-specific files in "test" / "production" directories.
4. Transform any DB-stored application configs into XML files (or vice versa) for VCS storage.

**Outcome:** Software install operations become version-control operations — better visibility, repeatability, and speed.

*Ref: The_DevOps_Handbook.md — Appendix 7 "COTS SOFTWARE"*

---

### Part IV — The Second Way: Technical Practices of Feedback

---

### 46. Create a Culture of Causality via Telemetry

**Principle:** High performers resolve production incidents 168x faster because they have **pervasive telemetry** and treat problems with disciplined cause analysis, not reboot-and-pray.

**Microsoft Operations Framework (2001) finding:** Highest-service-level orgs rebooted servers 20x less often and had 5x fewer blue screens — they diagnosed root cause rather than symptom-mask.

**Do:**
- Make telemetry from application, infrastructure, business, and pipeline visible to everyone.
- Generate telemetry as part of daily work — "If it moves, we track it" (Ian Malpass, Etsy — 800,000+ metrics by 2014).

*Ref: The_DevOps_Handbook.md — "Create Telemetry to Enable Seeing and Solving Problems"; "USE TELEMETRY TO GUIDE PROBLEM SOLVING"*

---

### 47. Centralized Telemetry Infrastructure

**Principle:** Build a telemetry platform with three layers — collection, event router/storage, visualization/alerting/anomaly-detection.

**Architecture (James Turnbull, "The Art of Monitoring"):**
- **Data collection at business logic, application, and environment layers:** events, logs, and metrics sent to a common service (syslog, collectd, Ganglia, AppDynamics, New Relic).
- **Event router (Sensu, Nagios, Logstash, Splunk, Datadog, Riemann):** store, aggregate, transform logs into metrics, enable threshold alerting and anomaly detection.
- **Visualization & analysis:** Graphite, Grafana, Kibana.

**Do:**
- Capture pipeline telemetry too — build status, deploy frequencies, lead times, test pass rates.
- Make everything self-service via APIs (no tickets required to view a graph).
- "Monitoring systems need to be more available and scalable than the systems being monitored" (Adrian Cockcroft).

*Ref: The_DevOps_Handbook.md — "CREATE OUR CENTRALIZED TELEMETRY INFRASTRUCTURE"*

---

### 48. Application Logging for Production

**Principle:** Every significant application event generates a log entry with the right level.

**Logging levels:**
- **DEBUG** — anything that happens (off in prod, on for troubleshooting).
- **INFO** — user-driven or system actions ("beginning credit card transaction").
- **WARN** — conditions that could become errors (DB call slow).
- **ERROR** — error conditions (API failures).
- **FATAL** — must terminate (cannot bind socket).

**Always log (per Anton Chuvakin):** authentication/authorization decisions, system and data access, privileged changes, data changes, invalid input, resource use, health/availability, startups/shutdowns, faults/errors, circuit breaker trips, delays, backup success/failure.

**Rule of thumb (Dan North):** "When deciding whether a message should be ERROR or WARN, imagine being woken up at 4 a.m. Low printer toner is not an ERROR."

*Ref: The_DevOps_Handbook.md — "CREATE APPLICATION LOGGING TELEMETRY THAT HELPS PRODUCTION"*

---

### 49. Self-Service Telemetry and Information Radiators

**Principle:** Anyone in the value stream should get metric data without tickets or privileged access; broadcast prominently.

**Do:**
- Make one-line code instrumentation possible (Etsy StatsD: `StatsD::increment("login.successes")`).
- Display dashboards on TVs in central areas (information radiators — TPS origin).
- Overlay deployment events on every metric graph — most production issues are caused by changes.
- Provide external service-status pages for customer trust (Transparent Uptime, Appendix 10).

**LinkedIn InGraphs case (Eric Wong, 2010 intern project):** Before — 30 minutes and a ticket to view CPU for a service. After — self-serve real-time dashboards featured in engineering offices.

*Ref: The_DevOps_Handbook.md — "ENABLE CREATION OF PRODUCTION METRICS AS PART OF DAILY WORK"; "CREATE SELF-SERVICE ACCESS TO TELEMETRY AND INFORMATION RADIATORS"*

---

### 50. Find and Fill Telemetry Gaps — Five Levels

**Principle:** Cover all five layers; gaps hide outages.

**Required metric coverage:**
1. **Business:** sales, signups, churn, A/B results.
2. **Application:** transaction times, faults, response times.
3. **Infrastructure:** DB, OS, network, storage (CPU, disk, traffic).
4. **Client software:** browser JS errors, mobile crashes, client-measured timings.
5. **Deployment pipeline:** build status, lead times, deploy frequency, environment status.

**Do:**
- Make every business metric **actionable** — vanity metrics should be stored but not alerted on.
- Graph business metrics alongside application and infrastructure metrics so a signup drop and a slow query are visible together.
- Treat infra faults (segfaults, exceptions) as potential security-breach indicators.

*Ref: The_DevOps_Handbook.md — "FIND AND FILL ANY TELEMETRY GAPS"; "APPLICATION AND BUSINESS METRICS"; "INFRASTRUCTURE METRICS"*

---

### 51. Means and Standard Deviations for Anomaly Detection

**Principle:** Use statistical thresholds, not static ones, when data has Gaussian distribution.

**Do:**
- Compute mean and standard deviation for each metric; alert when values exceed 3σ (only 0.3% of expected observations).
- Investigate every severe incident retrospectively to identify leading indicators that should generate future alerts (Tom Limoncelli's "delete all alerts, add back only those that predict outages").

*Ref: The_DevOps_Handbook.md — "USE MEANS AND STANDARD DEVIATIONS TO DETECT POTENTIAL PROBLEMS"; "INSTRUMENT AND ALERT ON UNDESIRED OUTCOMES"*

---

### 52. Anomaly Detection for Non-Gaussian Data

**Principle:** Many Ops data sets are chi-squared / skewed — using σ on them produces over- or under-alerting ("2:37 a.m., 4:13 a.m., 5:17 a.m. wakeups").

**Techniques:**
- **Smoothing / moving averages** — average each point over a sliding window.
- **Fast Fourier Transform** — for periodic data (Netflix Scryer uses FFT + linear regression to predict traffic).
- **Kolmogorov-Smirnov test** — non-parametric; compares distributions; catches "Monday didn't return to normal" patterns invisible to σ rules. Available in Graphite/Grafana.
- **Outlier detection** — Netflix: compute the current "normal" for a herd of cattle (compute nodes), flag and remove nodes that don't fit, automatically.

**Netflix Scryer case (2012):** Predictive auto-scaling that solved three Amazon Auto Scaling problems: slow instance startup, premature scale-in after outages, ignoring known traffic patterns.

**Do:**
- Pair Ops engineers with statisticians (Rally Software has an Ops engineer trained in statistics writing R code on a dedicated backlog).

*Ref: The_DevOps_Handbook.md — "PROBLEMS THAT ARISE WHEN OUR TELEMETRY DATA HAS NON-GAUSSIAN DISTRIBUTION"; "USING ANOMALY DETECTION TECHNIQUES"; "Case Study Auto-Scaling Capacity at Netflix"*

---

### 53. Dev Shares Pager Rotation with Ops

**Principle:** Everyone who touches production code or environments is reachable for incidents — including developers.

**Do:**
- Put developers, managers, and architects on pager rotation (Facebook's Pedro Canahuati, 2009).
- "When we woke up developers at 2 a.m., defects were fixed faster than ever" (Patrick Lightbody, New Relic).

**Don't:**
- Don't allow defect triage to deprioritize operational issues below new features — that creates chronic downstream suffering.

*Ref: The_DevOps_Handbook.md — "DEV SHARES PAGER ROTATION DUTIES WITH OPS"*

---

### 54. Have Developers Follow Work Downstream

**Principle:** UX-style contextual inquiry applied internally — Devs watch how Ops and customers interact with their service.

**Do:**
- Have developers observe production deployments, customer support calls, and operator workflows.
- Convert observations into codified non-functional requirements (deployability, manageability, operability).
- Gene Kim's revelation: a 63-click operation believed routine; 1,300-step product setup — that's why "managing our product was always assigned to the newest engineer."

*Ref: The_DevOps_Handbook.md — "HAVE DEVELOPERS FOLLOW WORK DOWNSTREAM"*

---

### 55. Self-Managed Production Services and the Google LRR/HRR

**Principle:** Development groups self-manage their service in production for at least six months before any centralized Ops/SRE group accepts responsibility.

**Google SRE model (Treynor Sloss, 2004):**
- Functional SRE org embedded in product teams; 7 SREs in 2004 → 1,200+ in 2014.
- **Launch Readiness Review (LRR):** self-reported, required before public launch.
- **Hand-Off Readiness Review (HRR):** more stringent; required when service transitions to SRE-managed.
- **Service Handback:** if a service becomes too fragile, Operations can hand production support back to Development.

**LRR/HRR checklist categories:**
- Defect counts/severity
- Pager alert frequency
- Monitoring coverage
- System architecture (loose coupling)
- Deployment process (predictable, deterministic, automated)
- Production hygiene
- Compliance scope (SOX, PCI, HIPAA, etc.)

**Cultural norm:** SREs volunteer hours to help product teams early — it's "good citizenship" considered in SRE promotions.

*Ref: The_DevOps_Handbook.md — "HAVE DEVELOPERS INITIALLY SELF-MANAGE THEIR PRODUCTION SERVICE"; "Case Study The Launch and Hand-off Readiness Review at Google"*

---

### 56. Hypothesis-Driven Development and A/B Testing

**Principle:** Treat every feature as a hypothesis; run the cheapest, fastest experiment that validates it.

**Intuit / TurboTax case (Scott Cook):**
- 2010: 7 experiments per year → 2012: 165 experiments during the 3-month US tax season.
- Website conversion up 50%.
- Ran experiments **during peak traffic** — the highest-value time, impossible under traditional change freezes.

**Do:**
- Integrate A/B testing into feature planning, development, and release.
- Define acquisition funnels (tire-kickers → active → engaged → deeply engaged) with telemetry at each stage.

**Don't:**
- Don't build the entire product to test demand — that's the most inefficient way to validate a hypothesis (Humble).

*Ref: The_DevOps_Handbook.md — "Integrate Hypothesis-Driven Development and A/B Testing into Our Daily Work"*

---

### 57. The Dangers of Over-Controlling Changes

**Principle:** External change approvals (CAB review of every change) **decrease** IT performance — the more an organization relies on approvals, the worse both stability and throughput.

**Knight Capital failure ($440M loss in 15 minutes):** Two counterfactual narratives — "change control failed" and "testing failed." But in low-trust command-and-control cultures, the typical response (more approvals, more questions, more lead time) **increases** the likelihood of future incidents.

**Why approvals fail:**
- The further the distance between change implementer and change authorizer, the worse the outcome.
- A CAB reading a 100-word summary cannot predictably evaluate hundreds of thousands of lines of code from hundreds of engineers.
- Adding approvals increases batch size and reduces feedback strength.

**Puppet Labs 2014 finding:** High performers relied more on **peer review** and less on **external approval**.

*Ref: The_DevOps_Handbook.md — "THE DANGERS OF CHANGE APPROVAL PROCESSES"; "POTENTIAL DANGERS OF 'OVERLY CONTROLLING CHANGES'"*

---

### 58. Peer Review of Changes (GitHub Flow)

**Principle:** Require fellow engineers close to the work to review changes before they enter trunk — not external authorities.

**GitHub Flow (5 steps):**
1. Create a descriptively named branch off master.
2. Commit regularly and push to the named branch.
3. Open a pull request when ready for feedback/help/merge.
4. Get desired reviews and approvals; merge into master.
5. Deploy to production from master.

**Code review guidelines:**
- Everyone has someone to review their changes before trunk commit.
- Everyone monitors the commit stream of teammates.
- Define which changes are high-risk and require SME review (DB changes, auth modules).
- If a change is too large to reason about at a glance, split it.
- Inspect review statistics to detect rubber-stamping.

**Forms of review:** pair programming, over-the-shoulder, email pass-around, tool-assisted (Gerrit, GitHub PRs).

**Do:**
- Apply small-batch thinking to reviews — review effort is non-linear with change size (Randy Shoup: "10 lines → 100 lines is more than 10x riskier").

**Don't:**
- Don't accept pull requests that lack context ("Fixing issue #3616" is a bad PR per Ryan Tomayko — must explain why, how, risks, countermeasures).

*Ref: The_DevOps_Handbook.md — "ENABLE PEER REVIEW OF CHANGES"; "Guidelines for code reviews include"; "Case Study Code Reviews at Google"; "EVALUATING THE EFFECTIVENESS OF PULL REQUEST PROCESSES"*

---

### 59. Pair Programming as Continuous Review

**Principle:** Two engineers at one workstation — driver writes code, navigator reviews strategically and shares techniques.

**Evidence (Dr. Laurie Williams, 2001):** Pairs are 15% slower than two individuals but produce 85% error-free code (vs 70%); 96% enjoy pairing more.

**When to use:**
- Replace broken code review processes (Pivotal 2011: Gerrit-based reviews were taking a week; switching to mandatory pairing cut that to hours).
- High-risk areas, knowledge transfer, onboarding.

**Pattern:** Pair writes tests, pair implements code (reinforces TDD).

*Ref: The_DevOps_Handbook.md — "ENABLE PAIR PROGRAMMING TO IMPROVE ALL OUR CHANGES"; "Case Study Pair Programming Replacing Broken Code Review Processes at Pivotal Labs"*

---

### 60. Case Study — Google at Scale (Single Repository, Trunk-Based, 25K Engineers)

**Principle:** Trunk-based development with mandatory code review scales to tens of thousands of engineers on a single source tree.

**2013–2015 stats:**
- 13,000+ developers on one trunk.
- 40,000 commits/day.
- 50,000 builds/day (90,000+ on weekdays).
- 120,000 automated test suites; 75 million test cases/day.
- 50% of code changed every month; 20+ changes/minute checked into trunk.
- 100+ engineers on tooling (0.5% of R&D workforce).

**Discipline that makes this work:**
- **Mandatory code review** by someone familiar with the language's readability guide.
- **Code ownership** for sub-trees to maintain consistency.
- **One official compiled language (C++)**, one scripting language (Python, later Go), one UI stack (Java/JavaScript via GWT).
- **Test Certified program** (Level 1 baseline metric → Level 2 policy/coverage → Level 3 long-term goal) — exploited Google's metrics-driven culture.
- **Test Mercenaries** — full-time internal consultants helping product teams improve testing.
- **Testing on the Toilet (TotT)** — weekly newsletter posted in bathrooms globally.
- **Fixit days** — company-wide improvement blitzes; the last involved 100+ volunteers in 20+ offices across 13 countries.

**Quote (Randy Shoup):** "If Google had tried to implement the 1995 equivalent of microservices out of the gate, we would have likely failed, collapsing under our own weight and probably taking the entire company with us."

**Eran Messeri (Google Developer Infrastructure):** "There are no hard policies at Google, such as, 'If you break production for more than ten projects, you have an SLA to fix the issue within ten minutes.' Instead, there is mutual respect between teams and an implicit agreement that everyone does whatever it takes to keep the deployment pipeline running. We all know that one day, I'll break your project by accident; the next day, you may break mine."

*Ref: The_DevOps_Handbook.md — "Case Study Code Reviews at Google (2010)"; "Case Study Internal Technology Conferences" (Google Testing Grouplet)*

---

### 61. Fearlessly Cut Bureaucratic Processes

**Principle:** Actively remove obstacles — "Got Goo?" (Capital One), "Join The Rebellion" (Disney), Target's TEAP-LARB dismantling.

**Adrian Cockcroft's metric:** Publish how many meetings and work tickets are mandatory to perform a release; relentlessly reduce that number.

**Do:**
- Use the "five whys" to question every long-standing approval process (Heather Mickman at Target: no one remembered why TEAP-LARB existed).
- When a Dev team takes Ops responsibility for a technology, exempt them from the central approval process for that technology.

*Ref: The_DevOps_Handbook.md — "FEARLESSLY CUT BUREAUCRATIC PROCESSES"*

---

### Part V — The Third Way: Technical Practices of Continual Learning

---

### 62. Establish a Just, Learning Culture (Sidney Dekker)

**Principle:** "When responses to incidents and accidents are seen as unjust, it can impede safety investigations, promote fear rather than mindfulness... and cultivate professional secrecy, evasion, and self-protection."

**Bad Apple Theory (debunked):** "Human error is not our cause of troubles; instead, human error is a consequence of the design of the tools we gave them."

**Do:**
- Make responses to accidents visibly just — honest mistakes are learning opportunities; reckless behavior has consequences.
- Counter the "name, blame, shame" pattern.

*Ref: The_DevOps_Handbook.md — "ESTABLISH A JUST, LEARNING CULTURE"*

---

### 63. Blameless Post-Mortems

**Principle:** After every accident, run a blameless post-mortem — focus on situational aspects of the failure's mechanism and the decision-making process of individuals proximate to it.

**Required attendees:**
- People involved in decisions contributing to the problem
- People who identified the problem
- People who responded and diagnosed
- People affected
- Anyone interested

**Post-mortem meeting practices:**
- Schedule as soon as possible after resolution, before memories fade.
- Construct a timeline with chat logs, metric graphs (not subjective narratives), investigation paths.
- Empower engineers to give detailed accounts of their contributions.
- Forbid "would have" / "could have" — counterfactuals frame the system-as-imagined, not as-it-exists.
- Capture countermeasures with owner and target date; **if a corrective action isn't top priority at end of meeting, it isn't a corrective action**.
- Disallow "be more careful" as a countermeasure (Dan Milstein: "prepare for a future where we're as stupid as we are today").

**Publish widely:**
- Prohibit incident closure until post-mortem is complete.
- Use tools like Etsy's Morgue to make post-mortems searchable (dramatically increased recording of P2/P3/P4 incidents).
- Consider external publication (Google App Engine 2010; Amazon DynamoDB 2015).

**Quote (Bethany Macri, Etsy):** "By removing blame, you remove fear; by removing fear, you enable honesty; and honesty enables prevention."

*Ref: The_DevOps_Handbook.md — "SCHEDULE BLAMELESS POST-MORTEM MEETINGS AFTER ACCIDENTS OCCUR"; "PUBLISH OUR POST-MORTEMS AS WIDELY AS POSSIBLE"; Appendix 8 "POST-MORTEM MEETINGS"*

---

### 64. Decrease Incident Tolerances to Find Ever-Weaker Failure Signals

**Principle:** As accidents become rare, **lower** the threshold for what counts as a problem — or stop learning.

**Alcoa case (Paul O'Neill, 1987):**
- 2% of workforce injured annually (7/day).
- Goal: zero injuries; notify CEO within 24 hours of any injury.
- Result: 95% reduction in 10 years; eventually reported near-misses too — driving further gains.

**NASA Columbia counter-example (2003):** Foam strikes were normalized as "maintenance problems" because they hadn't caused accidents yet; mid-level engineers' weak failure signals were ignored by a "rigid standardization" culture.

**Rule:** Vigilance alone is insufficient; treat technology work as fundamentally experimental, not standardized.

*Ref: The_DevOps_Handbook.md — "DECREASE INCIDENT TOLERANCES TO FIND EVER-WEAKER FAILURE SIGNALS"*

---

### 65. Redefine Failure and Encourage Calculated Risk-Taking

**Principle:** High performers fail more often in absolute count — that is a sign of health, not carelessness.

**Roy Rapoport (Netflix):** "If high performers are deploying thirty times more frequently but with only half the change failure rate, they're obviously having more failures. DevOps must allow this sort of innovation."

**Netflix story:** An engineer took down Netflix twice in 18 months but in that same window moved operations forward "by light-years." "This is a person we'd never fire."

*Ref: The_DevOps_Handbook.md — "REDEFINE FAILURE AND ENCOURAGE CALCULATED RISK-TAKING"*

---

### 66. Inject Production Failures — Chaos Engineering

**Principle:** Define your failure modes deliberately, or you will get whatever unpredictable — usually dangerous — ones emerge (Michael Nygard).

**Netflix Simian Army (Appendix 9):**
- **Chaos Monkey:** randomly kills processes and compute servers in production.
- **Chaos Gorilla:** simulates loss of an entire AWS availability zone.
- **Chaos Kong:** simulates loss of an entire AWS region.
- **Latency Monkey:** induces delays in service-to-service communication.
- **Conformity Monkey:** shuts down instances not adhering to best practices.
- **Doctor Monkey:** finds unhealthy instances via health checks.
- **Janitor Monkey:** disposes of unused resources.
- **Security Monkey:** finds/terminates instances with security violations.

**Great Amazon Reboot of 2014 (Xen security patch):** Netflix had 2,700+ Cassandra nodes; 218 rebooted; 22 didn't come back. **Zero customer downtime.** "Bring it on!" — Christos Kalantzis.

*Ref: The_DevOps_Handbook.md — "INJECT PRODUCTION FAILURES TO ENABLE RESILIENCE AND LEARNING"; Appendix 9 "THE SIMIAN ARMY"*

---

### 67. Case Study — Netflix Surviving the 2011 AWS US-EAST Outage

**Principle:** Architectural resilience is built deliberately over years, not granted by vendor favors.

**April 21, 2011:** Entire Amazon AWS US-EAST availability zone went down. Reddit, Quora, and many others went dark. **Netflix kept streaming.**

**Popular theory debunked:** Netflix was not given special treatment because of their AWS spend.

**What actually happened (2009 architecture redesign):**
- Migrated from monolithic J2EE in a private datacenter to **cloud-native** on AWS.
- Designed to survive the loss of an entire availability zone.
- Loosely-coupled components with aggressive timeouts.
- Every feature designed to **degrade gracefully** — e.g., during CPU spikes, show cached/un-personalized movie lists instead of personalized ones.

**Architectural patterns implemented:**
- **Fail fasts:** aggressive timeouts so failing components don't crawl the whole system.
- **Fallbacks:** each feature degrades to lower-quality representation.
- **Feature removal:** slow-running non-critical features removed from pages.

**Behavioral outcome:** Netflix went **over six hours** into the outage before declaring a Sev 1 incident — assuming AWS would restore. Only then activated business continuity procedures.

**Lesson:** Resilience is built; it doesn't come from running on a reliable vendor's infrastructure.

*Ref: The_DevOps_Handbook.md — "Enable and Inject Learning into Daily Work" (Netflix case study)*

---

### 68. Game Days — Rehearse Large-Scale Failures

**Principle:** Schedule catastrophic events; give teams time to prepare; execute and observe.

**Jesse Robbins ("Master of Disaster" at Amazon):** "A service is not really tested until we break it in production." At Amazon: literally powered off a facility without notice and let systems and processes fail naturally.

**Google DiRT (Disaster Recovery Testing) — Kripa Krishnan:** Simulated Silicon Valley earthquake, data-center power loss, even "aliens attacking cities where engineers lived." Revealed gaps:
- Engineer workstation failover didn't work.
- Conference call bridges had capacity for 50; needed a new provider to kick off hold-music offenders.
- No procedure for emergency diesel purchase; someone used a personal credit card for $50,000 of fuel.

**Benefit:** People build relationships across teams; conscious actions become unconscious routine.

*Ref: The_DevOps_Handbook.md — "INSTITUTE GAME DAYS TO REHEARSE FAILURES"*

---

### 69. ChatOps — Capture Knowledge in Chat

**Principle:** Put automation tools in the middle of team conversation — transparency, documentation, onboarding all in one place.

**GitHub Hubot:**
- Interacts in chat rooms ("@hubot deploy owl to production").
- Triggers Puppet, Capistrano, Jenkins, resque, graphme.
- Performs health checks, puppet pushes, deployments, alert muting, server rotation, even "apologizing to engineers on call."

**Benefits (Jesse Newland):**
- Everyone sees everything that's happening.
- New engineers can read chat logs to learn how work is done.
- People more likely to ask for help; rapid organizational learning.
- Chat is public by default; email is private and undiscoverable.

**Quote (Mark Imbriaco):** "There was no physical water cooler at GitHub. The chat room was the water cooler."

*Ref: The_DevOps_Handbook.md — "USE CHAT ROOMS AND CHAT BOTS TO AUTOMATE AND CAPTURE ORGANIZATIONAL KNOWLEDGE"*

---

### 70. Automate Standardized Processes in Software for Re-use

**Principle:** Encode organizational standards as executable code, not Word documents.

**GE Capital ArchOps (Justin Arbuckle):** "Enabled our engineers to be builders, not bricklayers. By putting our design standards into automated blueprints that were able to be used easily by anyone, we achieved consistency as a byproduct."

**Principle:** "The actual compliance of an organization is in direct proportion to the degree to which its policies are expressed as code."

*Ref: The_DevOps_Handbook.md — "AUTOMATE STANDARDIZED PROCESSES IN SOFTWARE FOR RE-USE"*

---

### 71. The Single, Shared Source Code Repository

**Principle:** One repository for the entire organization enables knowledge multiplication.

**Google scale (2015):**
- 1+ billion files, 2+ billion lines of code.
- 25,000 engineers on one tree.
- Library owners act as real-world librarians — ensure compilation AND tests for all dependents; migrate users between versions.
- Build everything statically from source — there is always one current version of every library.

**Value (Tom Limoncelli):** "Write a tool once, usable by all projects. 100% accurate knowledge of who depends on a library. I can't express in words how much of a competitive advantage this is for Google."

**Counter-example:** One organization ran 81 different versions of Java Struts in production — all but one with critical CVEs.

*Ref: The_DevOps_Handbook.md — "CREATE A SINGLE, SHARED SOURCE CODE REPOSITORY FOR OUR ENTIRE ORGANIZATION"*

---

### 72. Codify Non-Functional Requirements and Reusable Ops User Stories

**Principle:** Make operability explicit and reusable across projects.

**NFR examples to codify:**
- Sufficient production telemetry
- Accurate dependency tracking
- Graceful degradation under failure
- Forward/backward version compatibility
- Data archiving for production dataset size
- Searchable cross-service logs
- Distributed request tracing
- Centralized runtime configuration (feature flags)

**Ops user stories:** "A high-availability rollout takes 14 steps, requires 4 teams, averages 3 days" — exposes repeatable Ops work alongside Dev work in planning.

*Ref: The_DevOps_Handbook.md — "DESIGN FOR OPERATIONS THROUGH CODIFIED NON-FUNCTIONAL REQUIREMENTS"; "BUILD REUSABLE OPERATIONS USER STORIES INTO DEVELOPMENT"*

---

### 73. Standardize Technology Choices (Buoy, Not Boundary)

**Principle:** Reduce the number of supported technologies so deep expertise can accumulate.

**Etsy (2010):** Retired lighttpd, Postgres, MongoDB, Scala, CoffeeScript, Python — standardized on PHP + MySQL. Why: "both Dev and Ops could understand the full stack so everyone could contribute to a single platform."

**Google (Tom Limoncelli):** "One official compiled language, one official scripting language, one official UI language" → support libraries, tools, easier collaboration.

**Ralph Loura (HP):** "Create buoys, not boundaries — mark deep areas of the channel where you're safe; allow exploration past the buoys."

*Ref: The_DevOps_Handbook.md — "ENSURE TECHNOLOGY CHOICES HELP ACHIEVE ORGANIZATIONAL GOALS"; "Case Study Standardizing a New Technology Stack at Etsy"*

---

### 74. Improvement Blitzes (Kaizen Blitz) and Hack Weeks

**Principle:** Reserve concentrated time to attack one problem — no feature work allowed.

**Forms:** kaizen blitz, spring/fall cleaning, ticket-queue-inversion week, hack day, hackathon.

**Target DevOps Dojo (Ross Clanton):** 30-Day Challenges — internal teams come to the Dojo with a strategic problem and Dojo coaches for a month; "achieve in days what usually takes 3–6 months." 200 learners; 14 challenges completed by publication.

**Facebook HipHop case:** Haiping Zhao's hack-day experiment converting PHP to C++ → 2-year project → 6x capacity improvement → "Hail Mary pass that worked out" (Drew Paroski).

*Ref: The_DevOps_Handbook.md — "INSTITUTIONALIZE RITUALS TO PAY DOWN TECHNICAL DEBT"; "Reserve Time to Create Organizational Learning and Improvement"*

---

### 75. Enable Everyone to Teach and Learn

**Principle:** Engineer = lifelong learner; create forums for internal teaching.

**Mechanisms:**
- **Teaching Thursday** (Nationwide Insurance, 5,000 engineers): 2 hours/week, every associate teaches or learns.
- **Internal conferences:** Nationwide TechCon; Capital One (1,200 attendees, 52 sessions, 28 booths, no vendors); Target internal DevOpsDays (975 followers).
- **Internal consulting/coaches:** Capital One office hours; Google Test Mercenaries (full-time internal consultants); Test Certified roadmap (Level 1 baseline → Level 2 policy/coverage → Level 3 long-term goal).
- **Testing on the Toilet (TotT)** at Google — weekly newsletter in bathrooms.

*Ref: The_DevOps_Handbook.md — "ENABLE EVERYONE TO TEACH AND LEARN"; "SHARE YOUR EXPERIENCES FROM DEVOPS CONFERENCES"; "CREATE INTERNAL CONSULTING AND COACHES TO SPREAD PRACTICES"*

---

### Part VI — Information Security, Change Management, and Compliance

---

### 76. Information Security as Everyone's Job, Every Day

**Principle:** Infosec cannot operate as a silo — the typical Dev:Ops:Infosec ratio is 100:10:1.

**Rugged DevOps / DevSecOps:** Integrate security objectives into every stage of daily work.

**Do:**
- Invite Infosec to iteration demos.
- Track security issues in the same work-tracking system Dev/Ops use (Etsy: all security issues in JIRA, P1 or P2 severity).
- Conduct a security post-mortem after every security incident — educate engineers, transfer knowledge.

*Ref: The_DevOps_Handbook.md — "INTEGRATE SECURITY INTO DEVELOPMENT ITERATION DEMONSTRATIONS"; "INTEGRATE SECURITY INTO DEFECT TRACKING AND POST-MORTEMS"*

---

### 77. Integrate Preventive Security Controls into Shared Source Repositories

**Principle:** Make the secure path the easiest path.

**Provide as shared services/libraries:**
- Pre-blessed authentication, encryption, logging libraries
- Secret management (Vault, Keywhiz, credstash, sneaker, Trousseau, Red October)
- OS packages and builds (NTP, hardened OpenSSL, OSSEC, Tripwire)
- Base cookbook / build image of OS, DBs, middleware (NGINX, Tomcat) in known-secure state

**Benefit:** Engineers using predefined libraries skip separate security design review for that module.

*Ref: The_DevOps_Handbook.md — "INTEGRATE PREVENTIVE SECURITY CONTROLS INTO SHARED SOURCE CODE REPOSITORIES AND SHARED SERVICES"*

---

### 78. Integrate Security Testing into the Deployment Pipeline

**Principle:** Security tests run alongside other automated tests on every commit.

**Tooling (Gauntlt — Gherkin syntax for security tests):**
- Static analysis (Brakeman, Code Climate, banned-function checks)
- Dynamic analysis (Arachni, OWASP ZAP, Nmap, Metasploit)
- Dependency scanning (OWASP Dependency-Check, Gemnasium, bundler-audit, Maven)
- Virus scanning
- Source code integrity and signing (PGP, gpg-signed commits, signed CI artifacts)

**Twitter case (2012, AppSecUSA):**
- Brakeman integrated into Ruby on Rails build process.
- Result: 60% reduction in vulnerabilities found over years.
- Spike pattern correlates with new Brakeman releases.

**Design for sad paths:** Define abuse cases (SQL injection, XSS, buffer overruns) as automated unit/functional tests.

*Ref: The_DevOps_Handbook.md — "INTEGRATE SECURITY INTO OUR DEPLOYMENT PIPELINE"; "ENSURE SECURITY OF THE APPLICATION"; "Case Study Static Security Testing at Twitter"*

---

### 79. Secure the Software Supply Chain

**Principle:** Open-source components are your supply chain — track and patch them.

**Sonatype 2015 findings:**
- Typical org uses 7,601 build artifacts and 18,614 versions.
- 7.5% have known vulnerabilities.
- 66% of those vulnerabilities are over 2 years old.
- Of vulnerable open-source projects in NVD, only 41% are ever fixed; average time to fix: 390 days; CVSS-10 fixes: 224 days.

**Verizon PCI DBIR (2014):** 10 CVEs accounted for 97% of cardholder-data-breach exploits; 8 of those 10 were over 10 years old.

**Do:**
- Inventory all dependencies; alert on known CVEs.
- Prefer projects with demonstrated fast patching.

*Ref: The_DevOps_Handbook.md — "ENSURE SECURITY OF OUR SOFTWARE SUPPLY CHAIN"*

---

### 80. Security of the Environment — Hardening and Continuous Verification

**Principle:** Ensure environments are in a hardened, risk-reduced state; verify continuously.

**Do:**
- Generate automated tests that confirm configuration hardening, DB security settings, key lengths.
- Scan environments with Nmap (open ports), Metasploit (known vuln probes), SQLi tests.
- Compare output of scans to baseline each build; alert on drift.
- Use Netflix Conformity Monkey / Security Monkey to terminate non-compliant instances.

**18F Cloud.gov case:** Platform handles many controls at infrastructure/platform layer; remaining application-layer controls documented via Compliance Masonry (YAML → GitBooks/PDFs); reduced ATO time from 8–14 months to weeks.

*Ref: The_DevOps_Handbook.md — "ENSURE SECURITY OF THE ENVIRONMENT"; "Case Study 18F Automating Compliance for the Federal Government with Compliance Masonry"*

---

### 81. Integrate Security Telemetry into Production Observability

**Principle:** Year after year, breaches are detected months late by external parties because no one reviews logs.

**Application security telemetry:**
- Successful/unsuccessful logins (and ratio)
- Password resets, email resets, credit card changes
- Abnormal program terminations (segfaults, core dumps)
- DB syntax errors (zero tolerance — leading SQLi indicator)
- "UNION ALL" in user input (SQLi signature)

**Environment security telemetry:**
- OS changes, security group changes, configuration changes (OSSEC, Tripwire)
- Cloud infrastructure changes (VPC, security groups, users/privileges)
- XSS attempts, SQLi attempts, web server 4xx/5xx errors

**Quote (Nick Galbreath, Etsy):** "Nothing helps developers understand how hostile the operating environment is than seeing their code being attacked in real-time."

*Ref: The_DevOps_Handbook.md — "INTEGRATE INFORMATION SECURITY INTO PRODUCTION TELEMETRY"; "CREATING SECURITY TELEMETRY IN OUR APPLICATIONS"; "CREATING SECURITY TELEMETRY IN OUR ENVIRONMENT"; "Case Study Instrumenting the Environment at Etsy"*

---

### 82. Protect the Deployment Pipeline Itself

**Principle:** The deployment pipeline is a high-value attack target — protect it.

**Risks:**
- Stolen source code
- Malicious code injection into VCS
- Malicious code hidden in unit tests (no one reads them)
- Compromised CI credentials

**Mitigations:**
- Harden CI/build servers; reproduce them automatically.
- Review all changes (pair programming at commit OR code review before merge).
- Instrument repository to flag test code with suspicious API calls (filesystem/network access).
- Run each CI process in isolated container/VM.
- Use read-only VCS credentials for the CI system.

*Ref: The_DevOps_Handbook.md — "PROTECT OUR DEPLOYMENT PIPELINE"*

---

### 83. Change Management — Standard, Normal, Urgent (ITIL)

**Principle:** Categorize changes by risk; automate as many as possible into "standard" (pre-approved).

**ITIL categories:**
- **Standard changes:** pre-approved, low-risk, follow established process (e.g., monthly tax-table updates). No CAB approval needed; log for traceability.
- **Normal changes:** higher-risk; require CAB review/approval; use a Request for Change (RFC).
- **Urgent changes:** emergency; senior approval; documentation after the fact. Goal: streamline normal-change process until it works for urgent changes too.

*Ref: The_DevOps_Handbook.md — "INTEGRATE SECURITY AND COMPLIANCE INTO CHANGE APPROVAL PROCESSES"*

---

### 84. Re-Categorize Low-Risk Changes as Standard

**Principle:** Once you have a track record of high change-success and low MTTR, get CAB agreement that your changes are pre-approved standard changes.

**Salesforce case (2014, DOES):** After their DevOps transformation (deployment lead time: 6 days → 5 minutes by 2013), change management agreed that infrastructure changes made through Puppet would be **standard changes** — manual changes still required approval.

**Do:**
- Auto-create change records linked to JIRA tickets and pipeline artifacts via lightweight commit-message conventions.
- Provide auditors machine-readable evidence (links to JSON, not screenshots).

*Ref: The_DevOps_Handbook.md — "RE-CATEGORIZE THE MAJORITY OF OUR LOWER RISK CHANGES AS STANDARD CHANGES"; "Case Study Automated Infrastructure Changes as Standard Changes at Salesforce.com"*

---

### 85. Reduce Reliance on Separation of Duty

**Principle:** Separation of duty slows feedback and reduces engineer ownership of quality; replace with peer review, pair programming, and continuous inspection.

**Etsy PCI cautionary tale (Bill Massie, 2014):** To meet PCI DSS 6.3.2, the ICHT payment team instituted designated change approver. Result: "compartmentalization," "fear and reluctance around deployment," "an impenetrable wall between developers and ops... tension that no one at Etsy has had since 2008."

**Lesson:** Even a high-trust DevOps team will regress when low-trust control mechanisms are imposed.

*Ref: The_DevOps_Handbook.md — "REDUCE RELIANCE ON SEPARATION OF DUTY"; "Case Study PCI Compliance and a Cautionary Tale of Separating Duties at Etsy"*

---

### 86. Documentation and Proof for Auditors

**Principle:** Bridge the DevOps/auditor gap by deriving engineering requirements from regulations and emitting evidence continuously into telemetry systems.

**Bill Shinn (AWS) pattern:**
- Assign one control per sprint with auditors to determine required evidence.
- Send all audit data to Splunk/Kibana; auditors self-serve by time range.
- Map controls to specific regulations (e.g., HIPAA 45 CFR Part 160 → Subparts A & C of Part 164 → "technical safeguards and audit controls").

**ATM fraud case:** Developer planted a backdoor to put ATMs in maintenance mode for cash theft. Not found via code review (perpetrators with means/motive/opportunity can hide backdoors). Detected via production telemetry — ATMs in one city entering maintenance mode at unscheduled times.

**Lesson:** Production monitoring catches fraud that separation of duties and code review cannot.

*Ref: The_DevOps_Handbook.md — "ENSURE DOCUMENTATION AND PROOF FOR AUDITORS AND COMPLIANCE OFFICERS"; "Case Study Proving Compliance in Regulated Environments"; "Case Study Relying on Production Telemetry for ATM Systems"*

---

### 87. Case Study — Right Media Deployment Confidence Progression

**Principle:** Fear of deploying is identical on both sides of the Dev/Ops wall — the cure is fast feedback and small batches, not "more testing."

**Nick Galbreath (VP Engineering, Right Media, 2006 — 10B+ ad impressions/day):**
- Business required responding to market changes within minutes.
- Separate testing/deployment group was too slow.
- Integrated functions into one group with shared goals.
- **Biggest challenge:** Getting developers to overcome their fear of deploying their own code!

**The universal progression Galbreath observed:**
1. **No one** willing to push the deploy button (paralyzing fear of bringing down production).
2. Brave volunteer deploys; first production deployment breaks; discovered via customer reports because telemetry is thin.
3. Team urgently fixes code AND adds more production telemetry → next time, problem detected before customers complain.
4. More developers start deploying; complex systems still break, but now visible fast → roll back or fix-forward decision becomes routine.
5. **Developers proactively seek peer reviews** of their changes and help each other write better automated tests.
6. **Smaller and smaller increments** checked in more frequently — confirming each works in production before moving on.
7. Service stability better than ever. Smooth flow rediscovered: small, frequent changes anyone can inspect.

**Galbreath:** "As the person responsible for security, it's reassuring to know we can deploy fixes into production quickly, because changes are going into production throughout the entire day."

*Ref: The_DevOps_Handbook.md — "16Enable Feedback So Development and Operations Can Safely Deploy Code" (Right Media case)*

---

### 88. Case Study — Target DevOps Dojo

**Principle:** A physical space with full-time coaches and intensive engagement model can compress months of improvement into days.

**Target Dojo (Ross Clanton, Heather Mickman):**
- 18,000 sq ft of open office space.
- DevOps coaches work with teams from across Target.
- Three engagement formats:
  - **30-Day Challenges:** internal teams bring a strategic problem (POS, Inventory, Pricing, Promotion); work intensively with Dojo coaches in 2-day sprints; capacity for 8 concurrent teams.
  - **Flash Builds:** 1–3 day events shipping an MVP/capability by end of event.
  - **Open Labs:** biweekly drop-in coaching, demos, training.
- 200 learners; 14 challenges completed by publication.

**Target outcome (Ravi Pandey, Target development manager):** "In the old days, we would have to wait six weeks to get a test environment. Now, we get it in minutes, and we're working side by side with Ops engineers who are helping us increase our productivity and building tooling for us."

**Clanton:** "It is not uncommon for teams to achieve in days what would usually take them three to six months."

**Bonus practice (Target):** Held six internal DevOpsDays events since 2014 with 975 followers inside the internal technology community — modeled after ING Amsterdam's 2013 DevOpsDays.

*Ref: The_DevOps_Handbook.md — "Reserve Time to Create Organizational Learning and Improvement" (Target Dojo case)*

---

## Anti-Patterns & Common Mistakes

- **Big bang, top-down transformation:** Massive risk; instead find innovators and build silently, then broadcast wins. → *fix:* Follow the innovator → silent majority → holdouts path.
- **Long-lived feature branches:** Integration pain grows exponentially. → *fix:* Trunk-based development with daily commits.
- **Water-Scrum-fall:** Claiming Agile while all testing/defect-fixing happens at project end. → *fix:* Integrate testing into daily work; pull Andon cord on every break.
- **Manual testing as primary quality gate:** Slow, expensive, scales linearly with code. → *fix:* Automate per the testing pyramid; reserve humans for exploratory testing.
- **Stabilization / hardening phase:** A separate phase proves defects aren't being found in daily work. → *fix:* Define "done" as "running in production-like env, automated tests green."
- **CAB reviewing every change:** The more approvals, the worse both stability and throughput. → *fix:* Peer review and standard-change classification.
- **Snowflake servers:** Pets, not cattle. → *fix:* Immutable infrastructure; only path to change is VCS.
- **Static thresholds for alerts:** 2:37 a.m. wakeups for non-Gaussian data. → *fix:* Anomaly detection (K-S test, moving averages, outlier detection).
- **Name, blame, shame:** Engineers hide failure signals. → *fix:* Just culture, blameless post-mortems.
- **Inflicting Ops with fragile services:** Dev hands off and disowns. → *fix:* Dev shares pager; self-managed services; Service Handback.
- **Treating Ops as a ticket queue:** Maximizes handoffs. → *fix:* Embed Ops engineers; shared services with Dev as customer.
- **Bimodal IT as permanent state:** Accepting that systems of record must be slow. → *fix:* Apply DevOps to all systems — brownfield transformations are the highest-value.
- **Compliance by PDF:** Static analysis produces 100-page reports emailed and ignored. → *fix:* Pipeline-integrated security tests with developer-actionable output (Twitter Brakeman).
- **Hold music on incident bridges:** No runbook for comms. → *fix:* Game Days reveal latent defects in process and people, not just systems.
- **Mass pomodoro of approvals:** "Got Goo" meetings multiply. → *fix:* Publish and relentlessly reduce meeting/ticket count to release.

---

## Decision Heuristics / Checklists

### When to start a DevOps transformation
- [ ] Identified value stream with measurable business pain.
- [ ] Innovator/early-adopter team willing to volunteer.
- [ ] Executive sponsor — ideally funding the dedicated transformation team.
- [ ] Greenfield OR brownfield with strong urgency.

### Definition of Done (cumulative)
1. Code complete on a workstation ❌
2. Working, potentially shippable
3. **Demonstrated in a production-like environment**
4. **Created from trunk via one-click process, validated with automated tests**
5. Deployed to production, operating as designed, telemetry confirms desired outcome

### Deployment pipeline health checklist
- [ ] Commit-stage build ≤ 10 minutes
- [ ] Same artifact promoted through all environments
- [ ] Andon cord triggers when any stage fails
- [ ] Every commit runs unit + acceptance tests
- [ ] Pipeline status radiated publicly (build lights, chat, dashboards)
- [ ] Pipeline configuration is version-controlled
- [ ] Every deployment emits audit evidence to centralized logging

### Release safety checklist
- [ ] Deployment decoupled from release (toggle or environment-based)
- [ ] Rollback path tested (not theoretical)
- [ ] Production telemetry actively monitored during deploy
- [ ] Database changes are expand/contract (additive only)
- [ ] Feature toggles default OFF; acceptance tests run with all ON

### Incident response checklist
- [ ] On-call rotation includes developers
- [ ] Pager alerts tied to user-impact metrics, not component CPU
- [ ] Roll back / fix forward / toggle off decision tree documented
- [ ] Post-mortem scheduled before memory fades; countermeasures have owners

### Architecture review checklist
- [ ] Two-pizza team can own the service end-to-end
- [ ] Well-defined API between services
- [ ] Each service independently deployable
- [ ] Failure in one service contained (circuit breakers, timeouts, fallbacks)
- [ ] Architecture matches team org chart (Conway's Law)

### Security integration checklist
- [ ] Static analysis on every commit (Brakeman, OWASP Dependency-Check)
- [ ] Dynamic scanning (OWASP ZAP) in pipeline
- [ ] All dependencies inventoried and CVE-scanned
- [ ] All commits PGP-signed; all artifacts signed
- [ ] Security telemetry alongside business/application metrics
- [ ] Secret management via Vault/Keywhiz, not hardcoded credentials

### Change management checklist
- [ ] Standard changes pre-approved by CAB
- [ ] Normal changes have automated, evidence-rich RFCs
- [ ] Auditors self-serve evidence from Splunk/Kibana
- [ ] No reliance on screenshots or CSV exports

### Choosing what to standardize
- [ ] One official compiled language
- [ ] One official scripting language
- [ ] One official UI language
- [ ] One official DB; one official web server; one official queue
- [ ] Deviations allowed past the "buoys" if org principles are followed

---

## Key Takeaways

1. **The Three Ways are the foundation.** Flow (left-to-right), Feedback (right-to-left), and Continual Learning underpin every DevOps practice. Sequence them: flow first, then feedback, then learning.
2. **Small batches are the single most important technical practice.** Reduce batch size to reduce risk, increase flow, enable fast feedback, and shorten lead time.
3. **Automate everything that can be automated.** Build/test/deploy pipeline, environment creation, infrastructure provisioning, security scanning, audit evidence. Manual processes don't scale.
4. **Keep everything in version control.** Especially environments and infrastructure — Ops VCS use predicts IT performance better than Dev VCS use.
5. **Trunk-based development beats long-lived branches.** Daily commits, gated commits, small batches. Integration pain is exponential in branch count.
6. **Make work visible.** Kanban across the value stream; information radiators; deployment markers on every graph.
7. **Limit WIP.** "Stop starting, start finishing." Multitasking destroys throughput and hides problems.
8. **Decouple deployment from release.** Blue-green, canary, feature toggles, dark launches.
9. **Telemetry is how we see.** Cover business, application, infrastructure, client, and pipeline. Use statistics (means, anomaly detection, K-S test) not static thresholds.
10. **Pull the Andon cord.** Stop the line when the build breaks; write earlier-stage tests for any later-stage defect.
11. **Peer review beats external approval.** The further the approver from the work, the worse the outcome.
12. **Culture eats strategy.** Westrum generative culture predicts IT performance. Just culture, blameless post-mortems, rewarded risk-taking.
13. **Dev shares pager with Ops.** Self-managed services; Service Handback; LRR/HRR.
14. **Inject failures before production does.** Chaos Monkey, Game Days, DiRT.
15. **Conway's Law is deterministic.** Design teams to produce the architecture you want.
16. **Fund products, not projects.** Long-lived teams accumulate learning.
17. **Security is everyone's job, every day.** Integrate into demos, defect tracking, pipeline, telemetry.
18. **Standard changes beat CAB review.** Earn trust, then automate and pre-approve.
19. **Codify standards as code, not documents.** ArchOps, Compliance Masonry, shared libraries.
20. **Out-learn the competition.** "The only sustainable competitive advantage is an organization's ability to learn faster than the competition" (Senge).

---

## Cross-References

- Related: [[../Continuous_Deployment.md]] — Farley/Serviles' deeper treatment of CD pipeline mechanics.
- Related: [[../Lean_Enterprise.md]] — Humble/Molesky/O'Reilly's enterprise-scale Lean/DevOps patterns.
- Related: [[../Crafting_Engineering_Strategy.md]] — Larson on strategy, including DevOps adoption at scale.
- Related: [[../Building_Microservices.md]] — Newman on the architectural archetype this book gestures toward.
- Related: [[Continuous_API_Management.md]] — API change velocity enabled by these practices.
- Topic index: [[../INDEX.md]]
