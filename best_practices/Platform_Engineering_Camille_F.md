# Platform Engineering
**Authors:** Camille Fournier, Ian Nowland (with Michelle Garcia, Heidi Waterhouse, Kassandra Perlongo) — O'Reilly, October 2024
**Topic tags:** `#platform` `#general` `#organization` `#leadership` `#product-management` `#devops` `#sre`
**Language focus:** language-agnostic (organisational + product patterns; light Terraform / Kubernetes references; IDP vendor names mentioned are public record)
**Sources:** `markdown_output/Platform_Engineering_Camille_F/Platform_Engineering_Camille_F.md` · `summaries/Platform_Engineering_Camille_F.md`

## TL;DR

Platform engineering is the **discipline of managing system complexity to deliver leverage to the business**. It is not DevOps, not SRE, not infrastructure engineering — the differentiator is **treating the platform as a product with internal customers**. The four pillars of platform work are **product, software, breadth, and operations**; the four pillars of platform practice are **curated product approach, software-based abstractions, serving a broad base, and operating as a foundation**. Success requires balancing technology, product management, and people leadership — weakness in any one area undermines the others. **Adoption over mandate**: forcing teams to use a platform is a sign of failure; build something so good they choose it. Common failure modes include building platforms nobody uses, over-engineering, neglecting DX, ignoring organisational politics, ignoring migration cost, and forcing adoption. Use **six-pagers**, **bottom-up roadmaps**, **power-interest grids**, and **Wins-and-Challenges** to align platforms to the business and stakeholders. Use the **70/20/10** allocation (core / adjacent / transformational) and the **DORA + adoption + reliability** triad as your measurement baseline. Path to success: **start small, win trust, iterate — measured in quarters and years, not sprints**. Cross-references: Team Topologies (`../Team_Topologies.md`) for stream-aligned / enabling / complicated-subsystem patterns; Mastering Enterprise Platform Engineering (`../Mastering_Enterprise_Platform_Engineering.md`) for strategic framing.

---

## Best Practices by Topic

### 1. Define Platform Engineering by Its Value Proposition — Leverage, Not Tools

**Principle:** Platform engineering is the discipline of **developing and operating platforms to manage overall system complexity in order to deliver leverage to the business** — defined by leverage, not by the tools in your stack.

**Do:**
- Adopt Evan Bottcher's 2018 definition: *"A platform is a foundation of self-service APIs, tools, services, knowledge, and support that are arranged as a compelling internal product. Autonomous application teams can make use of the platform to deliver product features at a higher pace, with reduced coordination."*
- Treat platform engineering as **complexity management** through abstraction and encapsulation — *"more boxes, fewer lines."*
- Define success as **leverage**: the work of a few engineers on the platform should reduce the work of many across the application engineering org.
- Distinguish platform engineering from DevOps (a culture), SRE (Google-specific), and infrastructure engineering (a function with narrower scope) — the differentiator is treating the platform as a product.
- Use Bottcher's framing verbatim when explaining platform engineering to non-engineering leadership.

**Don't:**
- Define platform engineering by the technologies in use (Kubernetes, Terraform, Backstage, etc.) — that's defining by implementation, not by value.
- Treat platform engineering as "DevOps with a different name" — the culture-discipline split matters.
- Assume platform engineering is identical to SRE; SRE was Google-specific and heavyweight; platform engineering is broader.

**Code:**
```
+-------------------------------------------------------+
|  A platform is a foundation of self-service APIs,     |
|  tools, services, knowledge, and support arranged     |
|  as a compelling internal product. Autonomous         |
|  application teams use it to deliver product          |
|  features at higher pace with reduced coordination.   |
+-------------------------------------------------------+
  -- Evan Bottcher (2018), as quoted in the book
```

*Ref: Platform_Engineering_Camille_F.md — "Defining 'Platform' and Other Important Terms"*

---

### 2. The Four Pillars of Platform Work — Product, Software, Breadth, Operations

**Principle:** Successful platform engineering rests on **four pillars**: product, software, breadth, and operations. Weakness in any one pillar undermines the others.

**Do:**
- **Product**: customer-focused approach; user research; roadmaps; KPIs; not ticket-taking.
- **Software**: write the platform as software — versioning, CI/CD, testing, code reviews. Treat it as a codebase, not a config pile.
- **Breadth**: T-shaped profile — networking, security, storage, compute, observability across the stack. Specialist expertise is necessary but never sufficient.
- **Operations**: operate what you build. On-call, incident response, SLOs, runbooks, blameless postmortems.
- Hire across all four pillars — a team of pure engineers without product management fails; a team of pure PMs without engineering depth also fails.
- Make pillar boundaries explicit in role definitions and career ladders.

**Don't:**
- Hire only engineers and assume product thinking will emerge — it rarely does.
- Skip operations because "we're not a critical system" — every platform is critical to its users.
- Treat breadth as "everyone knows everything" — it's T-shaped, not generalist.
- Let pillar #1 (Product) be filled by "glorified scrum masters" doing backlog grooming.

**Code:**
```
+----------+   +----------+   +----------+   +----------+
| Product  | + | Software | + | Breadth  | + |   Ops    |
| (PM, UX, |   | (eng,    |   | (techical|   | (on-call,|
|  research|   |  review) |   |  range)  |   |  SRE)    |
+----------+   +----------+   +----------+   +----------+
       |              |              |              |
       v              v              v              v
       +--------------+--------------+--------------+
                              |
                       THE PLATFORM
```

*Ref: Platform_Engineering_Camille_F.md — "Chapter 2: The Pillars of Platform Engineering"*

---

### 3. The Over-General Swamp — The Problem Platform Engineering Solves

**Principle:** Cloud and OSS primitives generate **glue** (integration code, one-off automation, configuration) that holds systems together but creates stickiness, making future changes expensive. Platform engineering **constrains glue** so the engineering organisation doesn't drown.

**Do:**
- Recognise the swamp: every application team makes independent choices across primitives, creating glue everywhere.
- Track maintenance costs — 60-75% of software lifetime cost is post-development; roughly a quarter of that is migrations / adaptive maintenance.
- Reduce **primitives** in use by curating a small set that meets broad needs.
- Reduce **glue** to those primitives by abstracting them into platform capabilities.
- Use the architectural principle of **abstraction + encapsulation** — the platform provides a stable interface; underlying implementations change without forcing user changes.
- Keep public-cloud surfaces narrow: not every native service deserves an internal platform offering.

**Don't:**
- Let every team pick its own database / queue / monitoring tool — that's the swamp.
- Confuse "more options" with "better engineering" — option proliferation creates coordination tax.
- Skip the abstraction layer because "teams know what they need" — they often don't, or they don't know it consistently.
- Treat Kubernetes YAML as a glueless alternative to Terraform — it's just a different glue; the swamp metric is total glue, not glue by type.

**Code:**
```
THE SWAMP (Figure 1-1 in book):
    Postgres  Kafka  Redis  Cassandra
      \\       \\      |       //
       \\       \\     |      //
        App1   App2   App3   App4   -- each app has its
        glue!  glue!  glue!  glue!     own bespoke integration

THE PLATFORM (Figure 1-2 in book):
      Postgres  Kafka  Redis  Cassandra
              \\      |      //
               PLATFORM ABSTRACTION
                       |
              App1 App2 App3 App4   -- one glue layer,
                                       shared by all
```

*Ref: Platform_Engineering_Camille_F.md — "The Over-General Swamp" / "How We Got Stuck in the Over-General Swamp"*

---

### 4. The 60-Year Cost Tail — Why Platforms Are a Long Game

**Principle:** Most of the lifetime cost of software is **maintenance, not initial development**. Platform engineering amortises that cost by reducing glue per application; the benefit is realised **years later**, not on day one.

**Do:**
- Communicate the **60-75% lifetime maintenance cost** statistic to leadership; it justifies the long payback curve of platforms.
- Plan roadmaps across 12-month horizons, re-evaluating cost/benefit at every inflection.
- Recognise three "ages" of a platform component: Pioneer (optimised for fast feedback), Settler (optimised for scaling), Town Planner (optimised for cost + reliability + security simultaneously).
- Read Simon Wardley's "Pioneers, Settlers, Town Planners" framing — it's the basis for rearchitecture decisions in this book.

**Don't:**
- Expect ROI within one or two quarters — the leverage compounds over **quarters and years**, not sprints.
- Hire senior engineers from much bigger companies who think the current swamp looks like their previous company's v2; the team lacks the full context to use that experience safely for the first 12 months.
- Stop investing in old systems while doing a rearchitecture; old systems continue to need KTLO until **load has significantly fallen**.

*Ref: Platform_Engineering_Camille_F.md — "Different Engineering Mindsets" / "Centralizing the Cost of Migrations"*

---

### 5. Platform Types — IDP, Compute, Data, Networking, DX

**Principle:** Not all platforms are equal. The book covers four major categories; each has different user bases, abstraction boundaries, and operating models.

**Do:**
- Categorise each platform team by **type**:
  - **Compute/deployment platforms** — how code gets built, deployed, run. Most abstract; broadest user base.
  - **Data platforms** — data infrastructure (RDBMS, Kafka, search, object stores).
  - **Networking platforms** — connectivity, DNS, load balancing, security; closest to the hardware.
  - **Developer experience platforms** — unify development workflow; integration-heavy.
  - **Integration / shared-services platforms** — billing, identity, notifications; surface visible to external customer.
- Choose the right mix of paved path vs. railway (see cluster #6) per type.
- Track the type when discussing operating model — networking teams and IDP teams have different on-call expectations.

**Don't:**
- Build the same abstract platform for all four types; abstraction level must match the problem domain.
- Assume the integration platforms can be built the same way as DX platforms — they have external-customer surface area, which changes the PM profile you need.
- Conflate **integration platforms** (horizontal, serve every product) with **infrastructure platforms** (compute, network).

*Ref: Platform_Engineering_Camille_F.md — "Chapter 1: Types of platforms" (covers compute, data, networking, developer experience)*

---

### 6. Paved Path vs. Railway — Two Strategic Shapes of Platform

**Principle:** Curated platform offerings fall into two distinct shapes: **paved paths** (multi-system workflow bundles built on top of an infrastructure curation) and **railways** (gap-filling infrastructure built from scratch because the gap is widespread). Build the right shape, not both at once.

**Do:**
- **Paved path**: layer multiple curated offerings into a workflow. Follow Pareto (20% of use cases cover 80% of needs). Say no to outliers — the path is **optional**, not mandatory.
- **Railway**: discover a meaningful gap that no existing product fills; generalise from one team's prototype; provide the new capability as broadly usable infrastructure (e.g., batch job platform, notification system, global config).
- Pick **one** shape per platform; trying to be both is the "sh*terating" failure mode.
- Use **revealed preferences** (how teams actually use the system) to choose shape; don't just take feature requests at face value.

**Don't:**
- Try to be both a paved path and a railway at the same time — generic-system + drag-and-drop UI is the worst of both worlds.
- Force the paved path on teams with outlier needs; they will step off (and that's fine).
- Skip the **discovery** phase for a railway — pattern recognition across teams must precede generalisation.

**Code:**
```
PAVED PATH (Figure 2-1 in book):
    Multiple curated lower-level offerings
    -> PLATFORM WORKFLOW LAYER
    -> Hides complexity for 80% of use cases
    -> Optional for the 20%

RAILWAY (Figure 2-2 in book):
    Existing in-house primitive (e.g., ZooKeeper)
      + observed gap (e.g., global service discovery)
      -> BUILT AS NEW PLATFORM INFRASTRUCTURE
      -> Used across many product teams
```

*Ref: Platform_Engineering_Camille_F.md — "Taking a Curated Product Approach" (curated product approach, paved paths, railways)*

---

### 7. The Lifecycle: Stage 1 Ad Hoc → Stage 2 Somewhat Managed → Stage 3 Centralised → Maturity → Decline

**Principle:** Every platform moves through predictable stages. The book describes a 5-stage lifecycle (Ad Hoc → Somewhat Managed → Formally Centralised → Transformed Infrastructure → Maturity) and warns of the **decline** stage when the platform starts losing leverage.

**Do (Stage 1 / Ad Hoc, &lt;25 engineers):**
- Use source control; automate continuous deployment; pick off-the-shelf platforms (Heroku, Netlify, Vercel) over Kubernetes.
- Apply Kevin Stewart's "Use a process. Not too much. Mostly agile."
- Invest baseline in ticket-tracking; feature/debt ratio as a velocity signal.
- Let cooperative part-time efforts solve infra problems; do **not** create a platform team yet.

**Do (Stage 2 / Somewhat Managed, 25-50 engineers):**
- Automate local dev environments (colocate setup in the repo; publish container images; simplify wrapper scripts).
- Add branch-based deployments, basic test coverage gating, feature flagging, observability primitives.
- Use ADRs or RFCs for any non-trivial decision (e.g., React, Rust, Swift).

**Do (Stage 3 / Centralisation, ~50-150 engineers):**
- Replace cooperation with a small platform team (start at ~5-7 people).
- Focus on **solving pressing problems**, not new architecture; deliver value fast to earn trust.
- Pick a universally-acknowledged painful problem (deployment, storage provisioning) as the first target.
- Avoid hiring project managers or product managers before the engineering team has delivered something — optics matter.

**Do (Stage 4 / Transforming an Infrastructure Org):**
- Recognise that the change is cultural, not technical: cost / process / scale mindset → product / usability / customer mindset.
- Identify the most promising teams first; transform from there.
- Update interview processes for **customer empathy**; update promotion criteria to reward usability work.

**Do (Stage 5 / Maturity):**
- Run KTLO (Keep The Lights On) under 40% of team capacity; reserve 60% for feature + improvement work.
- Maintain per-platform **system improvement** stack-rank lists across reliability, efficiency, security.
- Recognise the **decline** stage: load falls (because teams are moving to a newer platform) — keep investing in the old until load has significantly fallen, otherwise customer trust evaporates.

**Don't:**
- Build a platform team before you have application teams that need it — premature centralisation creates waste.
- Hire platform leadership from much bigger companies and immediately let them rewrite to their previous company's architecture — they need 12 months to learn your context.
- Skip the "build trust through quick wins" phase; a platform team without goodwill cannot survive its first outage.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 3: How and When to Get Started" (all three stages) / "Chapter 8: Maintain Old Systems to Retain Trust"*

---

### 8. Operating Models — Centralised, Federated, Hybrid, Embedded

**Principle:** Platform operating models vary on the spectrum from a **single central team** to **federated** specialist teams to **embedded** engineers in product teams. Pick the model your current maturity supports; evolve as the org grows.

**Do:**
- **Centralised** — single team owns the platform end-to-end. Best for Stage 3, when cooperation is breaking down. Start here for most startups / growth companies.
- **Team-of-teams** — multiple specialised teams (compute, storage, data) under a shared platform leader. Best for **multi-product** companies with distinct platform surfaces.
- **Embedded platform engineers** — platform specialists sitting inside product teams. Best for very large companies where platform needs vary per product line.
- **Federated** — a small central team sets standards; specialists distributed across the org. Best when product teams have predictable, similar needs.
- Treat product management as **independent of engineering management** at scale; PM should report up to a separate platform PM leader who partners with the engineering leader (collaborative, not dictatorial).
- Use the **principal / distinguished engineer** in the platform org to advocate for cross-platform coherence — they have the authority to push back across silos.

**Don't:**
- Reorganise to fix product strategy; reorgs cause engineering churn and confuse customers about where to get support. Use strategic alignment first; reorg only when costs are high and benefits clear.
- Concentrate product management under engineering management — it loses product independence.
- Use reorgs as the first response to misalignment; the inverse Conway maneuver is real but expensive.

**Code:**
```
RECOMMENDED STRUCTURE (at scale):
+---------------------------------------------------+
|             Senior Platform Eng Leader             |
+---------------------------------------------------+
       |                       |
       v                       v
+----------+         +-----------------------+
| Eng Mgmt |         | Platform PM Leader    |
+----------+         +-----------------------+
   |        |               |        |
   v        v               v        v
Compute  Storage        PM-Compute  PM-Storage
   |        |                |         |
   v        v                v         v
Engineers (with T-shaped breadth)

Independent PM reporting = independent product judgment.
```

*Ref: Platform_Engineering_Camille_F.md — "Foster Cross-Platform Architecture with Independent Lead ICs" / "Chapter 9: Organizing Platform Teams"*

---

### 9. Team Topologies and Stream-Aligned Teams

**Principle:** Platform teams exist to **unburden stream-aligned teams** (Team Topologies). Without that frame, platforms become empire-building. Use Team Topologies' four team types as your mental model.

**Do:**
- Identify the **stream-aligned teams** first — the teams that own customer-facing value streams and need to ship without platform friction.
- Staff the platform team as an **enabling team** (initially) or **platform team** (when productised) to unburden stream-aligned teams.
- Recognise **cognitive load** — stream-aligned teams shouldn't need deep K8s / networking expertise to deliver value.
- Use complicated-subsystem teams for the deep-specialist work; don't force platform teams to do everything.
- For the full Team Topologies treatment, see `../Team_Topologies.md` (this repo).

**Don't:**
- Build a "platform team" as a ticket-driven service desk for any stream-aligned team that asks — that's the **feature shop**.
- Assume the platform team can be the only team; the moment stream-aligned teams lack product / customer focus because the platform owns it, you've over-centralised.
- Use the platform team as a "shadow IT police"; missing capabilities will go to shadow platforms.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 3 + Chapter 10" (cross-references Team Topologies framing on cognitive load); cf. `../Team_Topologies.md`*

---

### 10. Single-Focus Platform Teams — Why They Fail

**Principle:** Platforms staffed by **all-software** or **all-systems** engineers fail. The book describes two failure modes (Chapter 4) that capture the phenomenon.

**Do (avoiding systems-only failure):**
- Recognise that systems-only teams reach for **rules and process** over better abstractions.
- Pair every systems engineer with software engineers who can build the underlying abstractions.
- Require some hiring of generalist senior software engineers — even if your needs are operational today.

**Do (avoiding software-only failure):**
- Resist the urge to chase the next shiny technology; software-focused engineers over-estimate project velocity.
- Pair every software engineer with systems engineers who understand operational reality.
- Hire or grow people with both skills; don't treat them as "less real" engineers.

**Don't:**
- Hire only engineers that pass your current favourite whiteboard test — that biases the team toward whichever mindset that test measures.
- Keep "haunted graveyards" of legacy systems; the new team will refuse to touch them, and you'll be stuck with whoever wrote them.
- Promote only engineers who ship new code; you lose the people who keep the lights on.

**Code:**
```
SYSTEMS-ONLY FAILURE:
- Good at operations (paged at 2am, awake, mitigation in prod)
- BAD: build mostly automation/templates, not new abstractions
- Reach for rules + wikis to control users
- Customers "constantly run afoul of these rules"
=> "No software engineers need apply" interview filter
=> Cultural filter that excludes generalists

SOFTWARE-ONLY FAILURE:
- Builders; love "vNext", "next-gen", "golden paths"
- BAD: treat existing platform as "haunted graveyard" to poke
- Optimistic project estimates; miss operational reality
- 2am alert wakes the on-call twice before they respond
=> Manager upset that you thought escalating would fix it
```

*Ref: Platform_Engineering_Camille_F.md — "The Risks of Single-Focus Platform Teams"*

---

### 11. The Four Engineering Roles on a Platform Team

**Principle:** Build the team with **four distinct roles** balanced appropriately: software engineer, systems engineer, reliability engineer, systems specialist. Each has different strengths, weaknesses, and motivations.

**Do:**
- **Software engineer**: drawn to systems; comfortable on-call for business-critical systems; comfortable shipping at deliberate pace; talks to users.
- **Systems engineer**: true generalist on systems side; bridges storage, networking, Linux, observability; saves launches by spotting config tricks.
- **Reliability engineer**: focus on reliability; incident management; SLO / chaos / game-day ownership; needs to be embedded close to the platform team to keep skills current.
- **Systems specialist**: deep specialist (kernel, network, performance). Hire only when the need is clear; keep the bar high; don't hire many at once.

**Don't:**
- Hire specialists in the form of "specialist as evangelist" — research / conferences / open source contributions with no internal deliverable. They undermine credibility fast.
- Push systems engineers into pure specialisation prematurely; you lose the T-shaped breadth.
- Skip the software-vs-systems interview process calibration; a software-engineer process that emphasises toy algorithms will systematically reject the systems engineers you need.

**Code:**
```
ROLE TABLE (paraphrased Table 4-1 in book):

| Role                | Best Title            | Interview variation                | Level matrix                    |
|---------------------|-----------------------|------------------------------------|---------------------------------|
| Software Engineer   | "software engineer"   | Code + systems-design + behavioral  | Same as app-engineering ladder  |
| Systems Engineer    | "DevOps" OK           | Less strict code; more design depth | One shared systems ladder       |
| Reliability Engineer| "SRE" OK              | Same; design covers SRE depth      | Same systems ladder             |
| Systems Specialist  | e.g., "kernel engineer"| Design deep in the speciality      | Same systems ladder             |
```

*Ref: Platform_Engineering_Camille_F.md — "The Different Roles of Platform Engineers"*

---

### 12. Ladders — One Matrix for Systems Roles, Don't Fork Software Ladder

**Principle:** Don't create a "platform software engineer" ladder; do create **at most one** systems-role ladder. Forks are expensive to create and even more expensive to maintain.

**Do:**
- Keep software engineers on the same ladder as application engineers; specify level criteria in **outcomes achieved**, not methods used.
- Stretch **within the system**: in promotion discussions, find someone at the next level up outside of platform engineering who can attest to impact.
- Have evidence ready: wikis / dashboards / quality of customer interactions / postmortem leadership / ticket handling depth.
- Allow role-specific titles even if sharing one matrix — kernel engineer, SRE, performance engineer can all be on the same ladder.
- One shared systems ladder (e.g., Meta's "Production Engineer", Amazon's "Systems Development Engineer") is the right pattern when mature.

**Don't:**
- Fork the ladder per specialisation; every fork is a long-term maintenance burden.
- Use the systems-engineer's "non-coding" status as a reason to demote them relative to pure-software hires — their leverage is different, not lower.
- Make systems-engineer promotions depend on writing the same kind of code as software engineers; they won't, but their impact is still high.

*Ref: Platform_Engineering_Camille_F.md — "Avoid Creating a New Software Engineer Level Matrix"*

---

### 13. Hiring Platform Engineers — The Custom Interview

**Principle:** Use a **custom interview loop** for the platform engineer profile — one coding interview that emphasises bookkeeping (error handling, testing), one coding interview that surfaces systems understanding, one application-design and one platform-design interview, plus a customer-empathy behavioural round.

**Do:**
- One coding interview with a brute-force solution that can be optimised; evaluate both the optimisation **and** the bookkeeping.
- One coding interview that spends 30+ minutes discussing assumptions about scale-up, testing, observability — surfaces systems thinking.
- One **platform-design** interview (not application-design) — designing platforms, not apps.
- One **inverted design** interview — deep into the candidate's prior designs.
- One behavioural/values interview with explicit weight on **operational experience** and **customer empathy**.
- For systems roles: replace live whiteboard coding with a **time-boxed take-home** then a discussion; validates real coding without whiteboard stress.

**Don't:**
- Use a single interview loop for everyone and hope it fits.
- Skip the calibration period; expect 6 months of hands-on iteration with interviewers.
- Hire senior engineers from much bigger companies and immediately let them propose their last employer's architecture — they lack context on your platform and culture.

*Ref: Platform_Engineering_Camille_F.md — "If Needed, Create a New Software Engineer Interview Process"*

---

### 14. Customer Empathy — Interview for It, Then Enforce It

**Principle:** Customer empathy is coachable. Interview for it, set goals around it, and put engineers on a customer-support rotation to enforce it. Customers are tough, busy, sometimes condescending — empathy isn't niceness, it's a survival trait for the platform.

**Do:**
- Use behavioural questions: *"Tell me about a time when you helped a user understand the system"*; *"Tell me about a time when you used customer feedback to change direction."*
- Set quarterly/yearly goals including adoption, satisfaction, engagement.
- Invite users to all-hands / team meetings to share honest feedback.
- Put engineers (PMs and senior engineers, not just juniors) on support rotations; the live exposure is what builds empathy.
- Use the term "customer" not "user" — to paraphrase Camille: *"Customer implies obligations; users are just some schmucks."*

**Don't:**
- Try to detect "jerks" with a single rubric — the failure mode is defensive-aren't-helpful, not aggressive.
- Let the PM be the only one talking to users; engineering needs to be present for engineering concerns.
- Hide customer complaints from the team; engineers fix what they feel.
- Promote only feature-shippers; you'll lose the people who smooth usability pain.

*Ref: Platform_Engineering_Camille_F.md — "Interview for Customer Empathy"*

---

### 15. What Makes a Great Platform Engineering Manager

**Principle:** A platform engineering manager needs **operational experience on platforms**, **experience on big long-running projects**, and **attention to detail**. Engineering managers from application backgrounds typically lack these.

**Do:**
- Hire managers with operational experience on platforms (specifically on foundational systems), not application engineering leaders who "want to learn operations."
- Value project-and-process-management personal involvement in the early years of a manager's transition — until instincts build, this beats delegation.
- Take criticism and justify the slower delivery pace; resilience is part of the job.
- Build relationships — handle tough stakeholder discussions in 1:1s, not in writing.

**Don't:**
- Hire a strong manager from a customer organisation without verifying their operational maturity — they will underestimate ops load and alienate strong engineers.
- Hire a software-engineering manager who thinks operational discipline is "process theatre" — they will skip on-call until the platform burns.
- Hire a "brilliant engineer" type who leads by heroic fixes; each brilliant fix costs ten failed ones in operational systems.

*Ref: Platform_Engineering_Camille_F.md — "What Makes a Great Platform Engineering Manager?"*

---

### 16. Product Managers for Platforms — Different From SaaS PMs

**Principle:** Most PM orgs have **no PMs experienced with internal platforms**. Hire carefully: a SaaS PM will over-weight business metrics and under-invest in reliability. About 1 PM per 2-3 engineering managers is the rule of thumb.

**Do:**
- Aim for **1 PM per 2-3 managers-of-managers** (low end) up to 1 PM per engineering-manager-level (high end). Same range as the SaaS world.
- Hire **PMs from engineering backgrounds** (about 2:1 ratio versus formal PMs in practice) — they understand technical reality. Pair them with experienced PMs for calibration.
- Hire PMs only after the platform team has shipped something; otherwise optics signal "we can't talk to customers."
- Make the engineering management own the **bottom-up roadmap**; PMs lead the product roadmap; both collaborate on the merge.

**Don't:**
- Hire a PM in the first 12 months of a new platform team — the optics signal "we can't talk to customers ourselves."
- Hire only formal PMs; many will default to short-term business-obsessed thinking that undermines reliability work.
- Take a PM from a customer-facing product team and assume they "get platforms"; the role changes.
- Have PMs **own** execution — PMs do strategy + customer research + communication; engineering manages delivery.
- Treat "product owner" (SAFe) and "product manager" as synonyms; the former tends to be backlog-groomer; the latter needs latitude to do strategy.

*Ref: Platform_Engineering_Camille_F.md — "Product Managers"*

---

### 17. TPMs and Project Managers — Hire Rarely, Late, and Purposefully

**Principle:** Project managers are a **last resort**, not a default. Most platform engineering should be run with engineering managers + technical leads. Hire TPMs only when there are hard deadlines, many dependencies, or bureaucratic processes that require formal coordination.

**Do:**
- Hire the **first PM at the engineering manager level**, then every ~50 engineers a TPM if cross-team execution gets hard.
- Use TPMs on the **final 20%** of large migrations where machines and humans must work together.
- Use project managers to **unblock**, not to **own**: their value is freeing up engineers.

**Don't:**
- Bring in project managers at the start of a project — it creates scheduling bureaucracy and disengages engineering leads.
- Hire a project manager so the engineering manager doesn't have to do project tracking themselves; the engineering manager must own delivery.
- Assume project managers understand product strategy; they often turn priorities into schedule problems.

*Ref: Platform_Engineering_Camille_F.md — "Project Managers/Technical Program Managers"*

---

### 18. Internal Customers — Small, Captive, Conflicting Incentives

**Principle:** Internal customers are **trickier** than external ones. Build intuition about their traits so you can serve them right.

**Do:**
- Recognise the four characteristics of internal customers: **small** (no large-sample metrics), **captive** (can't easily switch vendors), **conflicting** (may control your budget), **moving-target** (complacency the moment you fix one pain).
- Treat them as **customers** not just stakeholders — *"A business would never just make customers use its product, so why would we expect to take that approach with our internal systems?"*
- Read **revealed preferences** (what they do) over **stated preferences** (what they say) — ask specific questions like "how quickly do you need X" instead of "do you want real-time."

**Don't:**
- Let customers as **competitors** go unaddressed — they'll build their own thing if you can't keep up.
- Treat high-NPS customers as the only ones to satisfy — small numbers can be influential.
- Use "Adoption metrics" as a stick for captive audiences — they will adopt something they hate when forced, and you'll lose the leverage.

*Ref: Platform_Engineering_Camille_F.md — "Characteristics of Internal Customers"*

---

### 19. Internal SLAs — Define Tiering, Eliminate False Positives

**Principle:** An **SLA is a contract** with a small number of high-confidence SLOs the customer can understand. **SLIs are internal monitoring instruments** — many, broad, accept false positives. **Error budgets are an expensive optional layer** — use them only when chronic problems warrant the cost.

**Do:**
- For **internal observability** (SLIs): use many SLOs, accept false positives, treat false positives and false negatives as needing improvement.
- For **customer-facing** SLOs: use **a handful at most**, **minimise false positives** ("boy who cried wolf"), accept false negatives (and address them transparently).
- Tier SLAs by **application tier** (Tier 0 vs Tier 1 vs Tier 2) — Tier 0 applications get notified pre-customer; Tier 2 may be customer-driven.
- Map SLOs to high-confidence business signals — if stakeholders can't tell the difference between your "red" and your normal state, the SLO has failed.
- When error budgets are used, treat violation as triggering a **conversation about options**, not a hard stop to all feature work.

**Don't:**
- Confuse SLOs with SRE's error budget gospel. The book argues error budgets are oversold; treat them as optional tooling.
- Have customers and on-call engineers looking at the same dashboard — customer dashboards should be **simpler** than engineer dashboards, by design.
- Use error budgets as a hard feature freeze. The book argues for a "fail minutes" conversation, not a contractual blocker.

*Ref: Platform_Engineering_Camille_F.md — "SLOs and SLAs Are Necessary; Error Budgets Are Optional"*

---

### 20. Platform Observability — The Custom Layer

**Principle:** Platforms need **observability custom to them**: user observability for customers, application-tier-aware instrumentation, and synthetic monitoring as a **major investment** (25% of dev time + 10% of resource cost, per Ian's AWS experience).

**Do:**
- Build **user observability** so a platform user can tell "did I do something wrong, or is the platform doing something wrong." That's the ideal; instrument even if you can never fully reach it.
- Require **Tier 0/1 customer teams to have their own 24/7 on-call** so they can be reached as quickly as the platform team reaches them.
- Invest **25% of ongoing dev time** and **10% of resource cost** in **synthetic monitoring** (active checks, not just passive metrics/logs/traces).
- Use synthetic monitoring for **end-to-end scenarios** that compose multiple APIs the way your customers do.
- Run synthetic tests in **triangulation**: shared load profiles surface the same issue the customer sees.

**Don't:**
- Rely only on passive "three pillars" observability for platforms — synthetic fills gaps.
- Skip instrumentation that lets customers debug themselves; building a "human dashboard" in the platform team becomes the default.
- Spend more than **12 dev-months/year** on release engineering automation — that's a shadow deployment platform.

*Ref: Platform_Engineering_Camille_F.md — "Synthetic Monitoring" (Ian: "this cost 25% of dev time and 10% of resource cost at AWS")*

---

### 21. Self-Serve Golden Paths — Mandatory for Adoption

**Principle:** Self-service is the **only** way a platform supports a **broad base** of customers without becoming a bottleneck. Without self-service provisioning, configuration, and observability, your team will drown in tickets.

**Do:**
- Offer **self-service provisioning** via UI, CLI, or CI/CD integration. Whatever the team prefers — many engineers want CLI, others want a web UI.
- Provide **easy defaults for novice users** plus **power-user access** to the underlying primitives.
- Build **golden-path templates** that combine multiple platform capabilities into a single workflow.
- Reduce support load by **investing in self-service over hiring support specialists** — it's usually cheaper in the long run.
- Aim for the Amazon Apollo model's design: same workflow from one team to the next, even when their application structures differ — **standardisation = leverage**.

**Don't:**
- Offer self-service as a UI-only surface; engineers want CLI / API access.
- Skip the golden paths and tell engineers "do it however you want" — that's the swamp returning.
- Hire support specialists to absorb the load of a platform that's hard to use — fix the platform instead.
- Build golden paths without a **20% escape hatch** to handle teams with outlier needs.

*Ref: Platform_Engineering_Camille_F.md — "Self-service interfaces" / "Love Just Works" (Apollo case study)*

---

### 22. Paved Road vs. Two Roads Debate — Choose Carefully

**Principle:** The "paved road or two roads" debate is about **how much optionality** to preserve. Paved road only forces the 80% case; two-road (paved + alternative) keeps the long tail happy but doubles maintenance.

**Do:**
- **Paved road only** when 80% of teams fit; explain that the path is optional, not mandatory.
- **Two roads** when you have a long tail of complex legacy use cases that can't be migrated cheaply; accept the maintenance burden.
- Use **pierceable abstractions** (Will Larson's "Providing Pierceable Abstractions"): a few well-supported exits from the paved path for the 20%, rather than a fully separate road.
- Re-evaluate periodically; legacy cases can be sunset as the ecosystem evolves.

**Don't:**
- Mandate the paved path — that's a feature-shop failure mode.
- Build two roads by default; double the maintenance is rarely worth it.
- Pretend the 80% is 95% — the 20% will find you and you need a plan for them.
- Run two paved roads in the same area (e.g., five different compute platforms, two of which are deprecated). Pick one and migrate.

**Code:**
```
PIERCEABLE ABSTRACTION (Will Larson, ref'd in book):

+------------------+
|  PAVED PATH UI    |
+--------+---------+
         |
    +----+----+    <-- "Pierceable" abstraction:
    |  CORE   |         workflows for 80% of customers
    |  PLATFORM|        + ONE exposed escape hatch for 20%
    +----+----+            (e.g., `run_as` Linux account
         |                  in Waiter; in our case, raw
    +----+----+            SQL access underneath)
    | RAW    |
    | PRIMITIVES
    +---------+
```

*Ref: Platform_Engineering_Camille_F.md — "Paved path" / "Pierceable opinionation" in "Love Just Works"*

---

### 23. Adoption — Marketing the Platform Internally

**Principle:** Adoption isn't automatic. Build a **marketing discipline** for the platform: landing pages, mailing lists, roadshows, communities of practice, **early adopters**. Without marketing, even great platforms go unused.

**Do:**
- Build an **internal landing page** that clearly describes each platform offering.
- Use **mailing lists, chat rooms** for feature announcements.
- Run **roadshows** to walk through new launches with customer orgs.
- Cultivate a **community of customer developers** given early access; they evangelise.
- Treat **early adopters as partners** — invest in their success and learn from their feedback.

**Don't:**
- Expect adoption to follow launch without marketing — *"if you build it, they will come"* fails for internal platforms.
- Confuse **high utilisation** (people forced to use the platform) with **adoption** (people chose it). The former can hide dissatisfaction.
- Let platform discoverability suffer — `Glengarry` instead of `Billing Platform` is an anti-pattern.
- Choose platform names that obscure purpose; aim for searchable, descriptive names.

*Ref: Platform_Engineering_Camille_F.md — "Product marketing" / "Look for products with realistic paths to adoption"*

---

### 24. Enabling and On-Call Support — Where Adoption Goes to Die

**Principle:** Adoption requires **enablement** (helping teams use the platform) and **responsive support** (helping them when it's broken). Without both, organic adoption stalls.

**Do:**
- Put platform engineers (yes, including seniors) on support rotations regularly — empathy training for the team.
- Use the **support tier model**: Tier 1 (initial contact, common issues) → Tier 2 (deep expertise, escalation to platform engineers) → platform engineer.
- Build a **community of advanced users** as a T2 expert network — train them, give them direct channels to platform engineers.
- At scale, formalise an **Engineering Support Organisation** (ESO) — they own T1 across all platforms.
- Biweekly review of **ESO + on-call**; turn repetitive tasks into tooling investments.

**Don't:**
- Filter support to "junior engineers only" — senior engineers must own the customer empathy culture.
- Allow the PM to do all the support triage — engineering ownership matters for operational issues.
- Hire a dedicated T1/T2 split team until you have scale (Stage 4+); use contract or rotating support first.
- Confuse "support" with "feature requests"; use Triaging tags to separate.

*Ref: Platform_Engineering_Camille_F.md — "Stage 1-4 of Support Practices" / "ESOs"*

---

### 25. Self-Service Migration Paths — Adoption Through Code, Not Mandates

**Principle:** Adoption improves when users can self-service their own migration. Provide **on-ramps** (pathways to the new system) and **off-ramps** (paths away from the old), not just docs.

**Do:**
- Build **partial migration paths** so customers can experiment with the new platform alongside the old.
- Document the **off-ramp** from each legacy system explicitly.
- Allow customer teams to **build their own extensions** that you can later promote to the platform.
- Use **dogfooding** + **partnership** as the discovery process: pick alpha testers, embed engineers with them, observe pain points.
- Use **maintenance windows** (yes, even in cloud-native) for changes that genuinely require downtime — much better than ad-hoc negotiation.

**Don't:**
- Force a big-bang migration — there is no compression algorithm for experience; users will hit edge cases.
- Skip the off-ramp documentation — the most disruptive part of a migration is the user's exit from the old system.
- Assume every team will use the new tool the same way; observe their workflows before declaring migration done.

*Ref: Platform_Engineering_Camille_F.md — "Document On-Ramps and Off-Ramps" / "Push Through the Final 20%"*

---

### 26. Tech Radar for Platforms — Prefer Established, Ride Trends Selectively

**Principle:** Choose **established, widely-used tools** for core infrastructure. Evaluate the ecosystem, not just the technology. Be cautious about tech that requires deep operational expertise (Kubernetes). Re-evaluate decisions yearly — yesterday's right answer isn't today's.

**Do:**
- Prefer **managed Kubernetes (EKS / GKE / AKS)** over self-managed unless you have very specific needs.
- Evaluate the **ecosystem and community** for any candidate technology — hiring market, support options, longevity.
- Plan to re-evaluate decisions — track them like stocks in a **tech radar** (CNCF-style: Adopt / Trial / Assess / Hold).
- Use the **"you aren't Google"** rule: don't adopt big-company architectures out of admiration; verify your problem matches their context.
- Recognise that **PaaS failed to win the broad market**; aim for narrow abstractions over generalized PaaS.

**Don't:**
- Adopt bleeding-edge tools for core infrastructure — operational risk is too high.
- Choose a tech based on hype alone; ecosystem abandonment has sunk many tools.
- Lock in technology without an exit strategy.
- Run your own Kubernetes control plane when managed offerings have caught up — operational burden is often worse than cost difference.
- Force deep-expertise tools on teams without adequate support; they'll be abandoned.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 4: Technology Choices"*

---

### 27. The Over-General Swamp — Choose the Right Cure

**Principle:** The swamp (each team picking their own DB / queue / monitoring) can be cured either by **standardising** (top-down mandate) or by **curating** (platform team offers curated alternatives). Curating wins because it preserves team autonomy while reducing option sprawl.

**Do:**
- **Curate, don't mandate.** Mandating creates resentment without addressing the underlying "why was this team using the unusual thing?" question.
- Use customer-empathy research to find out *why* teams use the tools they use (habit vs. must-have feature).
- Apply iterative product discovery to converge on a smaller set.
- Provide **2-3 offerings** in each major category (compute, storage, messaging), not 1.
- Track **OSS operations pain** — if your DRE team is paging on PostgreSQL + Kafka + Cassandra + MongoDB + FoundationDB, you have a curation problem.

**Don't:**
- Mandate removal of popular external tools without an internal alternative that addresses the gap.
- Let every Database-as-a-Service offering into the corporate catalogue — that's just the swamp with a different procurement process.
- Cut choices down to one when there are legitimate workload differences.

*Ref: Platform_Engineering_Camille_F.md — "Managing Complexity Through Product Discovery"*

---

### 28. IDP Comparisons — Backstage, Crossplane, Kratix, Humanitec

**Principle:** Internal Developer Portals (IDPs) are a **controversial pillar**. The book argues IDPs are **not required** for great platform engineering — wikis + APIs may suffice until you can show IDP-sized value. When you do adopt, the prominent options differ in **architecture philosophy**.

**Do (IDP decision):**
- **Spotify Backstage** (open-source, plugin model): central catalog for services + plugin-host for platform UIs; CNCF-incubated as the OSS reference.
- Use Backstage when your biggest customer pain is **discoverability** ("where do I go to use the platform?").
- **Crossplane** (open-source control plane): turns cloud-provider APIs into Kubernetes-style custom resources; strong fit when you want **infrastructure-as-control-plane** rather than infrastructure-as-code.
- **Kratix** (open-source, Syntasso): "Platform-as-a-Service framework" — provide Kubernetes-based internal platforms with **promise + resource** model for multi-team self-service.
- **Humanitec** (commercial): Internal Developer Platform orchestrator — declarative workloads with dependency graph; well-suited when you want a **single pane** for multi-cloud, multi-runtime workloads.

**Don't:**
- Adopt an IDP as a default because it's fashionable; the book explicitly calls the IDP trend a "fad" and warns about "look at what the shiny UI could do someday" as a poor argument.
- Replace simple wikis with an IDP before the platform team can populate it — backends are hard, plugins are hard, and your users will see an empty front page.
- Choose Backstage for a multi-cloud control-plane problem (that's Crossplane's strength). Choose Crossplane for a UI catalogue problem (that's Backstage's strength).

**Code:**
```
APPROXIMATE FIT (this repo's reading of public material):

                     Backstage     Crossplane    Kratix       Humanitec
                     --------      ----------    ------       ---------
Primary purpose      Service       Cloud-        Internal     Multi-cloud
                     catalog +     provider      platform     workload
                     UI plugins    control       framework    orchestrator
                                   plane
Strong when ...      Discover-     IaC at scale, Multi-        Polyglot
                     ability,      multi-cloud   team self-   workloads
                     developer     primitives    service      at scale
                     portals
Weak when ...        You want      You need a   You want a    You prefer
                     multi-cloud   service      single pane  OSS-only
                     orchestration catalogue     of glass
License              Apache 2.0    Apache 2.0    Apache 2.0   Commercial
Maintainer           Spotify +     Upbound       Syntasso      Humanitec
                     CNCF
```

*Ref: Platform_Engineering_Camille_F.md — "Integrating Metadata Registries" (refers to Backstage); user-facing guidance = "Is an IDP a Required Component?" `../Mastering_Enterprise_Platform_Engineering.md` for adjacent coverage*

---

### 29. Metadata Registries — The Foundation Most Platforms Skip

**Principle:** Without **metadata about who owns / uses / accesses each resource**, you cannot answer the four critical questions: ownership, access control, cost attribution, migrations. Build the registry early; retrofit is far worse.

**Do:**
- Build the **ownership metadata registry** in your platform's early days. Capture team membership, source code ownership, deployment ownership.
- Track **tag management** for resources (cloud tags, OTel resource attributes).
- Track an **API/schema registry** for compile-time API metadata (provenance, governance).
- Build an **Internal Developer Portal** as the programmable UI on top of the registry — only when the registry is actually populating.
- Use metadata-driven migration tooling so every migration tool knows its owner per resource.

**Don't:**
- Ask engineers to manually populate registries; they will not, and the data will rot.
- Defer ownership tracking to HR tooling alone — tech asset ownership is bigger than employment status.
- Use a separate notion of ownership per platform; cross-platform consistency requires central ownership.
- Let an IDP launch without populating data from the registries; the UI is useless without the data.

*Ref: Platform_Engineering_Camille_F.md — "Integrating Metadata Registries" / "Centrally Track Ownership Metadata"*

---

### 30. Six-Pagers and Long-Form Planning Documents

**Principle:** Use **structured documents** (Amazon-style six-pagers, design docs, RFCs, ADRs) for any major decision. The document replaces meetings with reading; the meeting replaces debate with decisions.

**Do:**
- Write **six-pagers** for any significant project: *background / tenets*, *details of the problem* (Lamport: state the problem before the solution), *overview of possible solutions* (before preferred), *proposed solution + rationale*, *plan of action* (with milestones).
- Review in meetings that start with **20 minutes of silent reading** then walk the doc section-by-section.
- Make documents reviewable by anyone — open decision-making builds trust.
- Use the same template across teams — consistency builds review efficiency.
- Distinguish **design docs** (problem + approach) from **one-pagers** (status updates).

**Don't:**
- Replace documents with meetings; meetings without prior reading waste everyone's time.
- Write five-page intros before getting to the meat; readers abandon long-winded docs.
- Skip the review meeting — the document's value is in the debate, not just the writing.
- Use design docs as bureaucracy; they're a tool, not a process gate.
- Hire a project manager at this stage — *bringing in PMs too early disengages the engineering lead*.

*Ref: Platform_Engineering_Camille_F.md — "Design documents / six-pagers"*

---

### 31. Roadmaps — Product Roadmap + Bottom-Up Roadmap, Merged

**Principle:** Platform teams need **two roadmaps**: a customer-facing **product roadmap** (top-down: features + customer value) and an internal **bottom-up roadmap** (KTLO + mandates + system improvements). Merge into one prioritised plan.

**Do:**
- Maintain **two artifacts**: customer-facing roadmap + internal bottom-up roadmap.
- Limit customer-facing timelines to **user-visible feature delivery**; keep technical milestones internal.
- Revise **quarterly**, not on every change — too-frequent revisions signal lack of direction.
- Use impact metrics to validate that delivered features achieve expected value.
- Apply the **70/20/10** model: 70% core / 20% adjacent innovation / 20% transformational — but don't treat it as a hard budget.

**Don't:**
- Let the product roadmap become a wishlist; ground it in engineering capacity.
- Let the bottom-up roadmap stay siloed; share themes with product leadership.
- Show internal technical milestones to customers — invites debate about engineering decisions that aren't their concern.
- Revise weekly — creates whiplash.

**Code:**
```
ROADMAP STACK:

  +----------------------+   <-- Customer-facing roadmap
  | Product roadmap      |       (features, dates for customers)
  +----------------------+
  | Bottom-up roadmap    |   <-- Internal
  |  KTLO (40% cap)      |
  |  Mandates            |
  |  System improvements |       70% core / 20% adjacent / 10% new
  +----------------------+
              v
  Merge into prioritised plan visible to all stakeholders.
```

*Ref: Platform_Engineering_Camille_F.md — "Roadmaps" / "Bottom-up roadmap"*

---

### 32. Bottom-Up Planning — KTLO / Mandates / System Improvements

**Principle:** Cap KTLO at **40%** of team capacity; apportion the rest using **70/20/10**. Treat individual system-improvement projects as **≤3 dev-months** unless they are critical (then they get the bigger rearchitecture treatment).

**Do:**
- Estimate KTLO from historical data — drop events that took >2 months because "they aren't planned future events."
- Track three separate stack-rank lists: **reliability/operability**, **efficiency/performance**, **security/compliance**.
- Use **mandates** sparingly; expect some "claimed essential" mandates to be killed and plan accordingly.
- Apply **FinOps discipline** once you reach ~200 engineers (tagging, rightsizing, spend reports).
- Treat **performance engineering** as systems-engineers' job; resist creating a full-time performance team unless you have thousands of engineers.

**Don't:**
- Let KTLO exceed 40% — burnout follows.
- Reach for a performance team composed of one mid-level engineer; they'll become "specialist as evangelist."
- Conflate **FinOps** (dedicated, specialised) with **performance engineering** (done by systems engineers); they are different.
- Run multi-quarter security work as a separate fire — security is a per-quarter discipline.

*Ref: Platform_Engineering_Camille_F.md — "Bottom-Up Roadmap Planning"*

---

### 33. Wins-and-Challenges — Biweekly Status That Scales

**Principle:** Use **Wins and Challenges** (W&C) — biweekly bullet-point updates that walk up the management tree and are rewritten for broader audiences. Essential because platform work looks invisible from sprint cadence alone.

**Do:**
- Write **situations, actions, results** (STAR-style) for each win or challenge.
- Have line managers write the updates; directors aggregate; VPs select highlights to share.
- Share the high-level highlights with peers + stakeholders + boss by email — publishing builds the team's reputation.
- Set a hard day/time (e.g., Wed 3pm EST) and a template; consistency matters.
- Surface **challenges internally** for collaboration; pick a **meaningful subset** for external trust-building (don't shame partners publicly).

**Don't:**
- Write wall-of-text updates; bullets are scannable.
- Publish only wins — stakeholders see through one-sided reporting.
- Skip W&C during holiday slowdowns; the habit must survive slack weeks.
- Use W&C purely as a status report — it must drive decisions and feedback.
- Treat collaboration challenges as public call-outs of partner teams; warn the partner first.

*Ref: Platform_Engineering_Camille_F.md — "Communicating Status with Biweekly Wins and Challenges"*

---

### 34. On-Call Practices — 24/7, Merged DevOps, ≤5 Pages/Week

**Principle:** Run **24/7 on-call** with a **merged DevOps** team (not split SRE/DevOps). Aim for **sustainable load**: one week on every 4-8 weeks, **≤5 business-impacting pages/week**. More than that = operational hell.

**Do:**
- Establish **24x7 on-call coverage** even for "non-critical" platforms (deployment tools, dev tools). Off-hours deploys will break things.
- Run **merged DevOps** — software engineers and systems engineers on the **same rotation**. Most platform teams can't afford a separate SRE team.
- Cap pages at **≤5 business-impacting pages/week** per on-call. (Five pages correlates with happy engineers; >5 pages correlates with attrition.)
- Pair platform teams for **secondary rotation** — but make incidents-to-secondary rare.
- Pay on-call (EU companies: ~€500/week) only if you can't make the load sustainable; payment subsidises bad operational discipline.

**Don't:**
- Skip on-call because your platform is "internal" — outages still affect real customers.
- Try to staff a separate SRE team when you have 4-5 engineers and need at least 4-5 dedicated SREs to make a split rotation work.
- Tolerate false alarms as a "pulse"; they erode trust in your dashboards.
- Add payment to compensate for an unsustainable load — fix the load instead.

*Ref: Platform_Engineering_Camille_F.md — "On-Call Practices"*

---

### 35. Change Management, Synthetic Monitoring, Operational Reviews

**Principle:** Three operational feedback practices close the loop: **change management** (documented + reviewed + tested), **synthetic monitoring** (active checks against complex dependencies), **operational reviews** (weekly cross-team discussion).

**Do:**
- Document, review, and test every change to production.
- Use synthetic monitoring to exercise end-to-end flows the way customers do.
- Run **weekly operational reviews** at the team level; use **monthly** org-level reviews.
- Have the **outgoing on-call** curate the operational review (pager load, support queue, postmortems, recent changes, SLO dashboards).
- Drive ops improvements through **small project investments** that show up in the next quarter's reliability story.

**Don't:**
- Skip change management because "we have CI/CD"; complex platforms still need explicit review of state-affecting changes.
- Use operational reviews as pure reporting theatre; **leadership must engage and decide**.
- Run ops reviews without blameless language; blame stifles the data you need.
- Spend >12 dev-months/year on release engineering — that's an over-engineered shadow deployment platform.

*Ref: Platform_Engineering_Camille_F.md — "Operational Reviews" / "Change Management"*

---

### 36. Migrations — Engineering, Coordination, Antipatterns

**Principle:** Migrations are a **strategic opportunity**, not a tax. Prepare engineering (chaos tests + acceptance tests + maintenance windows + metadata tracking + migration tooling) before asking customers to do work. Push through the final 20% with perseverance; use mandates sparingly.

**Do:**
- **Engineer toward transparent migrations**: container packaging + autoscale + canary/blue-green + acceptance tests + maintenance windows.
- Build **dependency tracking** (who uses what) before migrations are needed.
- Build **migration tooling** that automates the bulk of the work for the customer.
- Provide **on-ramps (off-ramp)** so customers can move incrementally.
- Use **progress dashboards** fed by automation (Camille's Linux migration case study).
- **Scope migrations backward from 12-month** OSS / vendor deadlines; longer horizons are nominal.
- **Limit coupling** between concurrent migrations — don't stack OS + DB + auth in one quarter.
- **Communicate early and publicly** — let customers have a year of warning before they must act.
- Reserve **engineering automation capacity** for the final 20% even if you think it will end sooner.

**Don't:**
- Announce with **context-free deadlines** ("migrate by Friday").
- Skip testing the migration before users see it.
- Rely on **clipboard-carrying scolds** as your primary migration tool.
- Send "wall of shame" dashboards — they only amplify defensiveness.
- **Stack migrations** in the same quarter.
- Issue mandates for non-security reasons — it damages trust.

**Code:**
```
MIGRATION ANTIPATTERNS (ref: "Migration Antipatterns"):
* Context-free deadlines     (e.g., "migrate by Friday")
* Unclear requirements       (e.g., "If you use Product X version Y...")
* "Did anyone test this?"   (broken in customer hands)
* Clipboard-carrying scolds  (project managers as chasers)
```

*Ref: Platform_Engineering_Camille_F.md — "Migration Antipatterns" / "Chapter 9"*

---

### 37. Sunsetting Platforms — When and How

**Principle:** True sunsetting (removing without a near-equivalent) is **rare and at the very tail end** of a migration. Three legitimate reasons: very few users, high cost-to-support, or strategic focus elsewhere.

**Do:**
- Try **transferring** the system back to a consuming team before sunsetting.
- Provide **off-ramp documentation** and **migration tooling** even for sunsettings.
- Pair with consuming teams during the transition; train them.
- **Negotiate timeline** with the impacted users — quarters to years depending on criticality.
- Tie sunsetting to **where the freed engineers will reinvest** — that message is part of the comms plan.

**Don't:**
- Sunset because the team that built the system is attached to it (sunsetters' sunk-cost problem).
- Sunset without giving users as much warning as possible.
- Make the consuming team feel they've been abandoned; pair on the transition.
- Skip the impact assessment — a critical-but-small user group can derail a sunset badly.

*Ref: Platform_Engineering_Camille_F.md — "Sunsetting Platforms" / "Sometimes It's the Builders Who Resist Sunsetting"*

---

### 38. Rearchitecture over v2 — Why and How

**Principle:** Rearchitect **incrementally**, don't rebuild v2. The second-system effect (Brooks) warns that v2 designs grow as teams over-correct; big-bang rarely ships. **Rearchitecting = changing architecture while serving load**.

**Do:**
- Recognise the **three mindsets**: Pioneers (innovate, scrappy), Settlers (turn prototypes into products), Town Planners (industrialise, optimise). Re-architecting requires Settler mindset.
- Use the **architectural maturity model**: scrappy → scalable → robust. Different mindsets for different stages.
- Use **incremental delivery** with **12-month wins** that prove value.
- Plan **three goals per cycle**: audacious + smaller + shipping to production.
- **Coordinate** multiple rearchitectures across teams (alignment process).

**Don't:**
- Build v2; the second-system effect is real.
- Allow **new hires** to lead the rearchitecture during their first 12 months — they need context first.
- Wait for **perfect greenfield** conditions — they never come.
- Promise "this will be done next year" without a 12-month intermediate win.
- Take the "**kill it with fire**" approach to legacy systems.

*Ref: Platform_Engineering_Camille_F.md — "Why Rearchitecting Is Preferred to Building a v2" / "Planning for Rearchitectures"*

---

### 39. Rearchitecture Planning — Think Big, Migration Costs, 12-Month Wins

**Principle:** A rearchitecture plan must **balance ambition** (think big) against **migration cost reality** (factor in) and **incremental delivery** (12-month wins). Without the 12-month wins, leadership will kill the project.

**Do:**
- **Think Big**: ask about all four capability categories (features, efficiency, reliability, security), not just one.
- Look to **subsume adjacent systems** — does the rearchitecture make any smaller platforms redundant?
- Look for **big OSS/vendor bets** — is there a rising ecosystem you could ride?
- **Factor in migration costs** — if migrations would take 1000 dev-years, scale down.
- Deliver **3 goals** per 12-month cycle: audacious + smaller + ship-to-prod.
- **Get leadership buy-in early**, even if it means waiting.

**Don't:**
- Hide migration costs to make the rearchitecture look cheap — this is the #1 cause of leadership killing the plan.
- Accept "let's wait until next year" indefinitely — if you've scraped by on incremental improvements, that's evidence leadership uses against you.
- Pin the entire rearchitecture on a single bet; spread risk across multiple goals.

*Ref: Platform_Engineering_Camille_F.md — "Planning for Rearchitectures"*

---

### 40. Stakeholder Management — Power-Interest Grid

**Principle:** Map stakeholders on a **power-interest grid**: high power/high interest (manage closely), high power/low interest (keep satisfied), low power/high interest (keep informed), low power/low interest (monitor). The **most important stakeholders are usually senior leaders, not daily users**.

**Do:**
- Use the grid to identify where to invest political capital.
- Identify **managers-in-common** and use them as escalation channels.
- Treat **disengagement as a warning sign** — if the powerful stakeholders stop engaging, they have quietly lost confidence.
- Pair **quarterly 1:1s with "Keep Satisfied/Keep Informed"** and **monthly 1:1s with "Manage Closely"**.
- Identify the **high-power + low-interest** stakeholders proactively — they're your biggest threat.
- Recognise that **stakeholder management is not product management** — one is political (about who decides), the other is about what to build.

**Don't:**
- Treat your own engineering team as the most important stakeholder; senior stakeholders can sideline you.
- Ignore high-power + low-interest until they re-engage suddenly in a downturn — by then you've lost.
- Skip the power-interest map as "corporate overhead" — it's the single highest-leverage stakeholder tool.

*Ref: Platform_Engineering_Camille_F.md — "Stakeholder Mapping: The Power-Interest Grid"*

---

### 41. Communicating with Stakeholders — Interlocks, Demos, Newsletters

**Principle:** Stakeholder communication must be **structured and proactive**: **interlock meetings** (cross-team coordination), **demos** (transparency), **newsletters** (broadcast), **RFCs** (collaboration).

**Do:**
- Establish **interlock meetings** with key stakeholders (biweekly / monthly / quarterly).
- Run **regular demos** to showcase progress — visibility builds trust.
- Use **newsletters** for broadcast updates.
- Use **RFCs** for changes that affect other teams.
- Have **engineers own operational/engineering discussions**, PMs own the roadmap.
- Keep meetings **lightweight and as infrequent as needed**.
- **Communicate proactive during rough patches**; goodwill becomes a deposit you can withdraw.

**Don't:**
- Leave all communication to PMs; engineers own their work.
- Communicate only when things go wrong.
- Send wall-of-text updates; keep them scannable.
- Forget to **track commitments in writing** — meetings have a way of erasing what was agreed.

*Ref: Platform_Engineering_Camille_F.md — "Communication"*

---

### 42. Saying No Gracefully — Scripts, Yes-with-Compromises

**Principle:** Saying **no** requires care; saying **yes** strategically is also a discipline. "Yes-with-compromises" is usually the safest move.

**Do:**
- Use **specific scripts** for declining requests without damaging relationships.
- Offer **alternatives** when saying no.
- Explain the **roadmap rationale** — show why "this" isn't on it.
- Track stakeholder request patterns — repeated requests signal roadmap gaps.
- Say **yes** when business needs genuinely align.
- Use the **"Not yet (priority call)"** / **"Not yet (technical call)"** / **"No, product strategy call"** / **"No, technical call"** taxonomy.

**Don't:**
- Say "no" without explanation — that's how resentment builds.
- Capitulate to every special request — that's the Feature Shop Trap.
- Hide the roadmap — stakeholders can't negotiate without knowing it.
- Be inflexible on small asks when a "yes" preserves a larger relationship.

*Ref: Platform_Engineering_Camille_F.md — "Saying No / Saying Yes strategically"*

---

### 43. Shadow Platforms — When to Push Back and When to Partner

**Principle:** Application teams **will** build shadow platforms. Recognise the reasons (can't wait, novel demand, don't want to collaborate, don't appreciate the operational cost, just want to build) and respond pragmatically.

**Do:**
- Identify the **driver** before responding (urgent need vs. frustration vs. empire-building).
- **Partner on urgent issues** — even lend settler-type engineers, with CTO-political cover.
- **Watch and wait** when the shadow platform is harmless; you may learn from it.
- After ~18 months, **integrate** the pioneer-built system into existing platforms (even at the cost of unhappiness).
- Set clear boundaries about whether you'll **take over operations** of the shadow platform later.

**Don't:**
- Fight every shadow platform immediately — most die on their own.
- Use the "you can't do this" position without senior stakeholder support.
- Let the pioneer team expand to **duplicate** existing platforms without a clear integration plan.
- Lose your pioneer engineers — they may leave when you integrate; treat them respectfully.

*Ref: Platform_Engineering_Camille_F.md — "Compromising on Shadow Platforms"*

---

### 44. Platform Funding Models — Central, Showback, Chargeback

**Principle:** Platform funding shape affects platform behaviour. **Central cost centre** keeps adoption friction low early. **Showback** drives awareness without political friction. **Chargeback** drives accountability once adoption is mature.

**Do:**
- Start with **central cost centre** — keeps the platform team aligned to leverage, not to budget politics.
- Use **showback** when cost awareness is the goal (typically Stage 2-3 maturity).
- Use **chargeback** when you want to drive accountability for usage (Stage 3-4 maturity).
- Track platform cost **separately from application cost** — visibility matters.
- Communicate cost trends to stakeholders proactively.
- Re-evaluate funding models as the platform matures.

**Don't:**
- Chargeback in early-stage platforms — friction before adoption is established.
- Hide platform costs from stakeholders.
- Forget the **value side** of the equation — platform cost is offset by leverage.
- Use funding models as a political weapon — they corrupt adoption incentives.

*Ref: Platform_Engineering_Camille_F.md — "Operating the Platform" / "Money Troubles: Cost and Budget Management"*

---

### 45. Common Failure Modes — What Kills Platforms

**Principle:** These five failure modes kill most platforms: **platforms nobody uses, over-engineering, under-investing in DX, ignoring organisational politics, forcing adoption, neglecting maintenance**.

**Do:**
- Validate demand **before** building.
- Start small and grow based on actual usage.
- Invest in **DX, documentation, observability** early.
- Treat **maintenance** (KTLO) as a first-class concern.
- Build **relationships** proactively, including with senior stakeholders.
- Make adoption the **path of least resistance**.

**Don't:**
- Build platforms nobody asked for.
- Over-engineer before validating.
- Force adoption before the platform is ready — mandates without quality create resentment.
- Ignore organisational politics — they're as important as technical decisions.

*Ref: Platform_Engineering_Camille_F.md — "Common Failure Modes"*

---

### 46. Getting Started — Practical Steps From Zero

**Principle:** Start small. Pick a **universally-acknowledged painful problem**. Build trust through **quick wins**. Be patient — meaningful platform results take **quarters, not sprints**.

**Do:**
- Start with a small focused team addressing a **specific high-value problem**.
- Pick a problem **universally acknowledged** as painful (deployment is the classic first target).
- Build trust through **quick wins** before tackling larger initiatives.
- Invest in **relationships with early adopters** — they become advocates.
- Document decisions and learnings for the next wave of platform builders.
- Be realistic with stakeholders on timelines — months to years, not weeks.

**Don't:**
- Start with a grand platform vision.
- Pick an esoteric problem nobody cares about.
- Rush to scale before validating the model — **premature scaling kills platforms**.
- Skip early adopter cultivation.

*Ref: Platform_Engineering_Camille_F.md — "Getting Started"*

---

### 47. The Three Pillars of Success — Tech, Product, People

**Principle:** Success requires balancing **technology, product management, and people leadership**. Weakness in any one area undermines the others. Platform engineering is a **leadership discipline**, not just technical work.

**Do:**
- Hire and develop across all three pillars.
- Recognise when one pillar is lagging and invest accordingly.
- Cross-pollinate — engineers learn product, PMs learn engineering, leaders learn both.
- Make pillar responsibilities explicit in roles and reviews.
- Recognise that this balance takes **years** to develop — it's a long game.

**Don't:**
- Hire only engineers and assume product thinking emerges.
- Skip people leadership — even great technology fails with poor people practices.
- Treat PMs as "support" to engineers; they're co-leaders.
- Underestimate the difficulty of balancing all three.

*Ref: Platform_Engineering_Camille_F.md — "Three Pillars of Success"*

---

### 48. Migration Planning — When to Force, When to Persuade

**Principle:** Most migrations are **persuasive**; some need to be **forced**. Distinguish **security-critical** migrations (forced) from **enhancement** migrations (persuaded).

**Do:**
- **Force** migrations for security (deprecated crypto, EOS OS, severe vulnerabilities).
- **Persuade** migrations for enhancements (better UX, performance, cost).
- Give **6-12 months** notice for forced migrations.
- Provide **migration tooling** + documentation for all migrations.
- Track **migration progress** and intervene when customers are stuck.

**Don't:**
- Force migrations for non-security reasons — damages trust.
- Skip migration tooling — manual migrations are adoption blockers.
- Hide the timeline — customers need lead time.
- Forget **edge cases** — customers always have unusual configurations.

*Ref: Platform_Engineering_Camille_F.md — "Migrations and Sunsetting of Platforms"*

---

### 49. Capacity Planning — Anticipate Before Crashes

**Principle:** **Capacity planning is the difference between proactive scaling and reactive firefighting.**

**Do:**
- Track **growth patterns** — usage trends, peak loads, seasonality.
- Plan capacity **ahead** of demand, not reactively after outages.
- Build **buffer** into capacity plans — never run at 100%.
- Communicate **capacity trends** to leadership — they need visibility.
- Test scaling behaviour with **load tests** and **game days**.

**Don't:**
- Run at 100% capacity — one spike and you're down.
- Skip capacity reviews — they're the cheapest insurance.
- Assume **linear growth** — capacity must handle spikes.
- Treat capacity planning as ops-only — engineering and product need to participate.

*Ref: Platform_Engineering_Camille_F.md — "Operating Platforms / Capacity planning"*

---

### 50. Compliance and Security as Platform Features

**Principle:** **Compliance** (SOC2, HIPAA, PCI, GDPR) and **security** should be **built into the platform** rather than added afterwards.

**Do:**
- Map compliance requirements to platform **capabilities** up-front.
- Build compliance controls into the **default configuration**.
- Provide compliance documentation (architecture diagrams, control mappings) as platform deliverables.
- Make compliance the **easy path** — secure defaults, audit trails, access logs.
- Train platform engineers on relevant frameworks.
- Embed security in **CI/CD pipelines** as well as runbooks.
- Track **security incidents** with the same rigour as availability incidents.

**Don't:**
- Treat compliance as a separate audit project — integrate into platform design.
- Skip compliance work because "we'll get to it" — customers need it before they'll adopt.
- Make customers implement compliance on top — that's broken incentives.
- Forget that **compliance requirements evolve** — plan for ongoing work.
- Treat security as "someone else's job" — it's the platform team's job.

*Ref: Platform_Engineering_Camille_F.md — "Operating Platforms / Compliance + Security"*

---

### 51. Case Study — Compute Platform + Icicle Team (Trust Through Flexibility)

**Principle:** When two teams reach a **stalemate** on what's "right," force flexibility from the platform team — build a **new offering** that meets the customer's critical need, even at the cost of efficiency.

**Situation:**
- Icicle team needed **no-oversubscription** low-latency compute for sensitive workloads.
- Compute platform's standard offering was oversubscribed (better economics, unpredictable latency).
- The team proposed to **build a shadow platform** to meet their needs.

**Resolution:**
- Compute team **ripped out oversubscription** for a new "high-perf" offering.
- Shipped first to **data science users** (lower bar) to build operational confidence.
- After 6 months of demonstrated success, Icicle committed to migrating.

**Key Lessons:**
- **Trust takes operational evidence**, not arguments. Deploy, run, demonstrate.
- **Flexibility on what's "right"** unlocks stalemates.
- Pick **less-critical early adopters** to gain operating experience.

*Ref: Platform_Engineering_Camille_F.md — "Gaining Trust Requires Flexibility on What Is 'Right'" (Icicle team case study)*

---

### 52. Case Study — DRE Team and the OSS-Swap Reset

**Principle:** When a platform team is **burning out on OSS operations** across PostgreSQL + Kafka + Cassandra + MongoDB + FoundationDB, the cure is **product discovery** — find the narrower surface area of common needs and sunset the extras.

**Situation:**
- DRE team had ~50 high-severity incidents/week.
- Three fix attempts failed: (1) move to vendor-hosted OSS, (2) SLA documentation, (3) full encapsulation.
- Application teams had begun building **shadow platforms** to get what they needed.

**Resolution:**
- Brought in managers with **product-oriented infrastructure experience**.
- Did **product discovery**; found two narrower opportunities:
  - **Cross-app config platform** (key-value) powered by FoundationDB.
  - **Limited SQL** (PostgreSQL + search + caching).
- Eliminated two offerings (Cassandra + MongoDB) over a multi-year migration.

**Key Lessons:**
- Don't compete with OSS by surfacing every OSS feature; **curate**.
- **Shadow platforms reset the conversation**; they become proof points.
- Multi-year migrations with end state visible are worth the time.

*Ref: Platform_Engineering_Camille_F.md — "Balancing Internal and External Complexity" (DRE case study)*

---

### 53. Case Study — Pioneers, Settlers, and Town Planners (Cloud Platform Integration)

**Principle:** When a **pioneer team** must build cloud capability your town-planner team can't deliver, **track the integration** explicitly; after 18 months, fold the pioneer's offering into the existing platform.

**Situation:**
- Existing platform team was years from public cloud support.
- Application teams needed elastic compute; pioneer team was staffed (small, fast-moving).
- Pioneer team built quickly, made a mess with their OSS choices.

**Resolution:**
- Communicated a **clear integration plan** to all sides — even though timeline was unclear.
- After 18 months, **transitioned** duplicate capabilities into the existing platform teams.
- Some pioneers left to find new green fields — that's expected.

**Key Lessons:**
- **Don't fight pioneers**; let them prove the value, then integrate.
- Pioneer teams leave when integrating — recruit them as your scouts.
- Pioneer mindset ≠ generalisable architecture; settlers do the integration.

*Ref: Platform_Engineering_Camille_F.md — "Getting Pioneer Agility on Robust Platforms"*

---

### 54. Case Study — Apollo (Love Just Works)

**Principle:** Build the platform so it **"just works"** with strong UI/automation interfaces, opinionation, and **one pierceable escape hatch** (e.g., arbitrary scripts on deploy).

**Situation:**
- Amazon Apollo (deployed c. 2004) was Ian's most-loved platform for ~7 years.
- Predated containers; did equivalent work.
- 5,000+ engineer scale.

**What Made Apollo Loved:**
- **Great UI and automation interfaces** — UI never lied about state; everything possible via API.
- **Strong opinionation** — paved path was the default for 80%.
- **Pierceable opinionation** — at deploy time, users could execute arbitrary scripts; covered the 20% edge cases.

**Key Lesson:** Love comes from **standardisation with one escape hatch**, not from open-ended flexibility.

*Ref: Platform_Engineering_Camille_F.md — "Love Just Works" (Apollo case study)*

---

### 55. Case Study — Waiter (Love Looks Like a Hack)

**Principle:** Beloved platforms often have **hacky-looking implementations** that solve real user friction. Don't rewrite them just because they look ugly — **survey users first**.

**Situation:**
- Waiter was a compute platform at a major company.
- Key feature was "**run as the caller**" — the workload ran as the same Unix account as the calling user.
- Implementation required complex coordination between load balancer and orchestrator.
- Beloved because data scientists no longer had to debug permission mismatches between dev and prod.

**Key Lessons:**
- **Productivity for end users** beats implementation beauty.
- The pioneer mindset ("just make this work") may produce hacky but beloved platforms.
- Before rewriting such systems, **survey** to confirm users actually want the rewrite.

*Ref: Platform_Engineering_Camille_F.md — "Love Can Look Like a Hack" (Waiter case study)*

---

### 56. Case Study — Internal S3 (Love Can Be Obvious)

**Principle:** Sometimes **love is obvious** — when you bring known, popular external tech inside, with awareness + compatibility + engineering quality + fast time-to-market.

**Situation:**
- On-prem company had no S3-compatible object store.
- Storage PM bet that **internal S3 would see massive adoption** without needing a customer ask first.
- Within months: massive adoption.

**Why It Worked (4 conditions):**
- **Awareness**: S3 was already known to every engineer.
- **Compatibility**: most tools already supported S3.
- **Engineering quality**: stable because built on production-hardened components.
- **Time to market**: < 1 year from research to alpha.

**Key Lesson:** Outside tech sometimes delivers obvious value *inside* — but only when those four conditions align.

*Ref: Platform_Engineering_Camille_F.md — "Love Can Be Obvious" (S3-compatible object store case study)*

---

### 57. Case Study — Building Blocks vs. Batteries Included

**Principle:** When "batteries included" platforms become **over-coupled** and lose trust, switch to **"building blocks"** (well-defined APIs over component-level integration).

**Situation:**
- "Batteries included" vision meant every workflow integrated component-level.
- As features grew, integrations became tightly coupled, breaking releasability.
- v2 attempts hit the **second-system effect** (expanded scope, missed deadlines).

**Resolution (OKR-driven):**
- "Building blocks, not batteries included" OKR.
- Decouple components via well-defined APIs.
- Allow customers to "pierce" the abstraction when needed (Larson's pattern).

**Key Lessons:**
- **Coupling at the component level is fragile**; coupling at the API level is stable.
- "Batteries included" can win initial trust; "building blocks" sustains it.
- A good platform lets **customers extend the platform** themselves when they have outliers.

*Ref: Platform_Engineering_Camille_F.md — "Building blocks, not batteries included"*

---

### 58. Case Study — Apollo + Tying It Together (The Overcoupled Platform)

**Principle:** When a platform team has lost trust through over-coupling, **decisively** change the product strategy; don't just tweak.

**Situation (cross-reference):**
- The five-compute-platforms situation in Chapter 11 shows what happens without alignment: **five competing compute platforms**, none robust, customers frustrated.
- The OS vs. build-tools rearchitecture deadlock (Chapter 11) shows the cost of unaligned leaders.

**Resolution:**
- "Building blocks, not batteries included" applied org-wide.
- **Forthright confrontation** of misalignment with peer leaders; trust-bound.
- Three goals per rearchitecture cycle (audacious + smaller + ship).
- Cuts to **whole projects**, not uniform headcount trimming.

**Key Lessons:**
- When platforms are misaligned across teams, **reorganise last**; realign first.
- Big projects need explicit buy-in from above; otherwise they get killed.
- Don't trim proportionally across teams — **cut whole initiatives** to preserve the rest.

*Ref: Platform_Engineering_Camille_F.md — "Tying It Together: The Case of the Overcoupled Platform" / "Final Alignment Comes from Principled Leadership"*

---

### 59. Culture Change — Transforming Infrastructure Teams

**Principle:** Changing from **infrastructure** (cost + process mindset) to **platform** (product + usability mindset) is a **cultural change** that requires explicit action across people, processes, and rewards.

**Do:**
- Start with the most promising team (modern offerings + software engineers + high change rate).
- **Update the interview process** to screen for customer empathy.
- **Update recognition and rewards** so usability work is celebrated.
- **Restructure** as needed; remove leaders who won't make the transition.
- **Have engineers do support**; senior engineers must own it.
- **Keep it fun** — celebrate wins, share kudos, never let the relationship become antagonistic.

**Don't:**
- Try to change everything at once — start with eager teams and expand.
- Add PMs without changing culture — they'll become "glorified backlog groomers".
- Underinvest in PMs and assume the engineering team owns product — they don't.
- Hire many project managers — limit them; force engineers to share the customer load.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 3: Transforming a Traditional Infrastructure Organization"*

---

### 60. Internal Developer Portals (IDPs) — Required, Optional, or Fad?

**Principle:** The book explicitly argues IDPs are **not required**. Use them when discoverability is the dominant customer pain, and only after you can populate them with real data.

**Do:**
- Use **wikis + API docs** for small platform estates.
- Use **Backstage** when service catalogue + plugin UI is your dominant customer pain.
- Treat any IDP adoption as a **major data-population effort** — empty UIs are worse than no UI.
- Use **metadata registries** to feed the IDP automatically; users do not curate by hand.
- Recognise IDP is one of the **four pillars of platform work** (alongside self-service, golden paths, infrastructure abstraction) — but a small pillar relative to the others.

**Don't:**
- Adopt an IDP because **the trend** says so — the book explicitly calls this a fad.
- Stand up an IDP before your platforms have stable APIs and known owners.
- Promise customers "look what the shiny UI could do someday" without a real backend story.

*Ref: Platform_Engineering_Camille_F.md — "Is an IDP a Required Component of a Platform Engineering Offering?"*

---

### 61. Generative AI / MLOps and Platforms

**Principle:** Generative AI is a **new platform surface** that creates new requirements. Apply the same platform-engineering principles: model-training tooling + observability + cost control + access controls.

**Do:**
- Recognise that **MLOps** is the next platform surface — many toolchains repeat the same DevOps mistakes.
- Invest in **observability** for AI training runs; mandatory for cost control.
- Provide **data entitlements** controls for training data access (compliance needs these).
- Build platforms that **adapt on demand** — the attacker-vs-defender dynamic.
- Provide **MLOps platforms** that mirror the developer experience of "good DevOps".

**Don't:**
- Treat AI/MLOps as outside the platform team's charter — it's the next frontier.
- Build an AI platform without the **instrumentation and data entitlements** required for compliance.
- Apply old IDE-pipeline DevOps habits to ML workflows — researcher workflows differ.

*Ref: Platform_Engineering_Camille_F.md — "What Does Generative AI Mean for Platform Engineering?"*

---

### 62. Innersourcing and Away Teams — Why They Mostly Fail

**Principle:** **Innersourcing** (letting other teams commit to your codebase) often fails for platforms. The **Amazon "away team" model** (formal contract-driven) is better but expensive. Avoid relying on either.

**Do (Camille's lessons from innersourcing):**
- Recognise the **Hyrum's law** risk: every observable behaviour becomes dependent on.
- Maintain ownership of platform code; don't externalise support for innersourced contributions.
- If you must use **away teams**, formalise the contract — there's a real management overhead.

**Don't:**
- Open the codebase and expect non-platform engineers to contribute meaningfully — most won't.
- Assume "**build it and contribute it back**" avoids hard prioritisation conversations — it just delays them.
- Default to an away-team model — it's only valuable when the application team has unique context.

**Code:**
```
Hyrum's Law (paraphrased):
  "All observable behaviours of your system will be depended
   on by somebody, no matter what you promise in the contract."

Implication for platforms:
  A single bug fix in an innersourced client can take down the
  whole service-discovery system.
```

*Ref: Platform_Engineering_Camille_F.md — "Platform Antipattern: Relying on Innersourcing"*

---

### 63. Bug-Bard Square Pegs — The Bike Shed Problem on Integration Platforms

**Principle:** **Integration platforms** (billing, identity, notifications) have customer-facing surfaces. The **bike-shed vs nuclear plant** problem: visible UI details get disproportionate attention; the underlying architecture (high leverage) is neglected.

**Do:**
- Hire **PMs early** for integration platforms (they have external-customer surface).
- Coach PMs to evaluate trade-offs (UX quality vs. architectural quality) explicitly.
- Resist the temptation to spend months on small UI details when the architecture is fragile.
- **Be "stuck in the middle"** deliberately; manage the tension between core platform and application teams.

**Don't:**
- Hire a business-focused PM and assume they grasp platform concerns — they often don't.
- Spend months on UI polish while the underlying system has reliability problems — that's a recipe for outages.
- Let the platform team be a stranger to the core platform team — alignment matters even when org-chart positions are different.

*Ref: Platform_Engineering_Camille_F.md — "Bonus Problems for Integration/Shared Services Platforms"*

---

### 64. Ad Hoc vs. Centralisation — The Right Time to Form a Platform Team

**Principle:** Don't create a platform team on a schedule — create one when **cooperation has demonstrably failed**. The book's signal is **Dunbar's number** crossed (50-250 people in a cooperative group): processes no longer scale; ownership must be assigned.

**Do:**
- Watch for **rising coordination cost** (PR review conflicts, integration glue spread).
- Watch for **a single sentinel event** (e.g., acquisition, big migration) that exposes unmanageable complexity.
- Form the platform team with **a small, focused brief**: pick one universally-acknowledged painful problem.
- Recognise that forming the team is a **major change** — collective cooperation dynamic disappears.
- **Deliver value fast** in the first 12 months — give time to collect goodwill.

**Don't:**
- Form a platform team before you have **multiple application teams** that need it.
- Promise a grand central platform in the first 12 months — promise and ship one specific pain.
- Skip the user research; even with cooperation, build the team around real customer need.
- Replace the previous cooperation with formal process in the first 6 months — let the team earn trust.

*Ref: Platform_Engineering_Camille_F.md — "Creating the Platform Teams That Replace Cooperation"*

---

### 65. Architecture Astronauts vs. Pragmatic Architecture

**Principle:** Rearchitectures must balance **architectural ambition** ("think big") against **migration reality** and **12-month delivery**. Avoid "**architecture astronauts**" who envision futures they can never deliver.

**Do:**
- **Think big** on the design — what's the boldest architecture that supports all four capabilities (features, efficiency, reliability, security)?
- **Filter** through migration cost analysis, 12-month wins, and leadership buy-in.
- Be wary of "**second-system effect**" — teams over-correct after one success.
- Treat **principal engineers** as cross-team advocates for architectural coherence.
- Keep **architectural decisions** documented (ADRs).
- Plan for the **end-state migration cost** before pitching a rearchitecture.

**Don't:**
- Treat architecture as **endless meetings** disconnected from day-to-day reality.
- Promise "this rearchitecture will solve everything" — it's a 3-5 year programme.
- Let new hires lead the rearchitecture — they lack context.
- Build "**building blocks, not batteries included**" without first knowing your customer workflow deeply.

*Ref: Platform_Engineering_Camille_F.md — "Architecture and Design Principles" / "Chapter 8: Rearchitecting Platforms"*

---

### 66. Proactivity and Operational Discipline

**Principle:** Platform teams must invest in **operations continually, including when times are good**. Feature-driven teams can defer ops; platform-driven teams cannot.

**Do:**
- Treat operations as a **continuing investment**: on-call + SLO + change management + postmortems.
- Be **proactive in operational practice**: surface unknown-unknowns early.
- Run **operational reviews** weekly (team) and monthly (org).
- Run **synthetic monitoring** as a first-class observability investment (25% dev time + 10% resource at AWS scale).
- Maintain a **system risk register** to surface latent problems.
- Take operational excellence as a **promotable** path for engineers.

**Don't:**
- Defer ops work to "after the next feature ships" — that's how complexity compounds.
- Treat ops reviews as theatre — they're a forcing function for action.
- Skip blameless language — blame kills the data.
- Underinvest in synthetic monitoring; passive "three pillars" alone aren't enough.

*Ref: Platform_Engineering_Camille_F.md — "Operating Platforms: Essential Practices, Not Processes"*

---

### 67. Fair-Weather Stakeholders and "Power-Interest Drift"

**Principle:** Stakeholders are **most engaged when times are bad** and disappear when times are good. Plan accordingly. **Increase communication during rough patches** — that's your deposit on future goodwill.

**Do:**
- **Increase communication** during rough patches (operational instability, missed features, budget pressure).
- Use the **Wins-and-Challenges** format to make the rough patches visible without theatrics.
- Watch for **disengagement as a warning sign** — quiet stakeholders often mean quiet loss of confidence.
- Always have at least one **executive sponsor** for any major project — they can defend you in downturns.

**Don't:**
- Treat communication as a "**when things go wrong**" trigger; go proactive.
- Rely on the stakeholder to tell you they care; assume they don't, until you've made it easy.
- Forget to plan W&C ahead of a downturn — the rituals must survive slack weeks.

*Ref: Platform_Engineering_Camille_F.md — "Increase Communication During Rough Patches"*

---

### 68. Operational Trust Erosion — Three Vectors

**Principle:** Platforms lose operational trust in three ways: **operations** (instability at scale), **big investment buy-in** (no consultation), **being a bottleneck** (slow delivery).

**Do (against operations):**
- Staged adoption — early adopters are less critical; later tranches are.
- Operational excellence OKRs with measurable key results.
- Empower leaders with operational experience at scale.

**Do (against big investment buy-in):**
- Build a **yearly project proposal** (similar to Action Plan).
- Seek **technical stakeholder buy-in** before starting rearchitectures.
- Maintain old systems throughout the rearchitecture.

**Do (against bottleneck):**
- Create a **culture of velocity** — agile response to unplanned demands.
- **Prioritise projects to free up team capacity** (Diego Quiroga's "self-serve" case study).
- **Challenge assumptions about product scope** — limit scope to common 80%, build escape hatches.

**Don't:**
- Assume trust from past delivery — it requires constant renewal.
- Begin a big investment without **senior IC and management buy-in**.
- Trade flexibility for control on the bottleneck — flexible scope wins.

*Ref: Platform_Engineering_Camille_F.md — "Your Platforms Are Trusted" (Chapter 12)*

---

### 69. Adoption Metrics as a Red Herring

**Principle:** Treat **adoption metrics as a red herring** when you have a captive audience. High adoption under mandate tells you nothing about whether the platform is loved.

**Do:**
- Use adoption as a **secondary** metric.
- Pair adoption with **impact metrics** (DORA, time-to-deploy, NPS).
- Avoid driving adoption through **mandatory migrations**.
- Treat **gold-plated** adoption as a sign of over-coercion.

**Don't:**
- Use adoption as your **single success metric**.
- Make adoption the basis for a captive audience's stick.
- Optimise platforms for "people will be forced to use this" — that's empire-building.

*Ref: Platform_Engineering_Camille_F.md — "A Success Red Herring: Adoption Metrics"*

---

### 70. CSAT / NPS Surveys Done Right

**Principle:** Customer satisfaction surveys are a **valid but flawed tool**. Use them rigorously — they can be biased by sample or used to justify pre-decided outcomes.

**Do:**
- Ensure a **good sample population** with high response rates.
- **Be willing to act** on the results — survey fatigue is real.
- Ask **specific questions** (rank/rate use cases) rather than "would you like X? Y? Z?" with a long list.
- Use surveys to **make the case** for big changes when users already complain.
- Pair with **behavioural data** (time-to-deploy, completion rates) — surveys alone aren't enough.

**Don't:**
- Use a biased survey to **justify a pre-decided outcome** — it backfires.
- Skew the population (e.g., only fans fill it out → results meaningless).
- Survey without a plan to follow through; users notice.

*Ref: Platform_Engineering_Camille_F.md — "A Success Red Herring: Lies, Damn Lies, and CSAT Scores"*

---

## Anti-Patterns & Common Mistakes

- **Building a platform nobody uses:** the most common failure; usually because the team didn't treat it as a product. *Fix:* validate demand first; pick a universally-acknowledged painful problem; build trust through quick wins. *Ref: "Common Failure Modes"*

- **Over-engineering:** building a grand unified platform before validating. *Fix:* start small; iterate based on usage; resist premature abstraction. *Ref: "Over-engineering"*

- **Under-investing in DX:** technically excellent platforms that are painful to use. *Fix:* apply UX principles to internal tools; invest in documentation, error messages, feedback loops. *Ref: "Under-investing in DX"*

- **Ignoring organisational politics:** failing to build the relationships. *Fix:* use power-interest grids; invest in stakeholder relationships; communicate proactively. *Ref: "Ignoring Organizational Politics"*

- **Forcing adoption:** mandating platform use before the platform is ready. *Fix:* build something so good teams choose it; treat mandates as a sign of failure. *Ref: "Forcing Adoption"*

- **Neglecting maintenance:** building new features while letting existing ones decay. *Fix:* reserve KTLO time in roadmaps; track tech debt; maintain operational discipline. *Ref: "Neglecting Maintenance"*

- **Conflating product and project management:** treating PMs as glorified scrum masters. *Fix:* PMs focus on strategy + research + communication; engineering manages execution. *Ref: "Product management is not project management"*

- **Centralised Terraform-writing team as a feature shop:** pulling engineers into a central team without platform thinking. *Fix:* apply product thinking; build a platform with abstractions, not just a service that writes Terraform. *Ref: "Reducing Per-Application Glue"*

- **Platform team superiority complex:** viewing themselves as more sophisticated than product engineers. *Fix:* humility in culture; service mindset; recognise you're supporting, not controlling. *Ref: "Cultural attributes"*

- **Big-bang platform launch:** releasing everything at once. *Fix:* staged rollouts; less critical applications first; gather data and iterate. *Ref: "Staged Approach"*

- **Skipping cross-platform coordination:** each platform team drifts independently. *Fix:* cross-team product strategy sessions; principal engineer role for cross-platform advocacy. *Ref: "Cross-Platform Coherence"*

- **Communicating only when things go wrong:** reactive communication breaks trust. *Fix:* proactive Wins-and-Challenges; interlock meetings; demos; newsletters. *Ref: "Communication"*

- **Leadership trusting too much in details:** SLO dashboards with 24 greens + 1 red; stakeholders fixate on the red. *Fix:* keep customer-facing SLOs to a handful; minimise false positives. *Ref: "SLOs"*

- **V2 / second-system effect:** big-bang rewrite to fix everything. *Fix:* rearchitect incrementally; 12-month wins; escape hatches. *Ref: "Second-System Effect"*

- **Single-pane-of-glass delusion:** one UI to rule all. *Fix:* API-first; one size fits no one. *Ref: "Single Pane of Glass"*

- **CD-as-free-passes for legacy platforms:** "we have CI/CD, change management is bureaucracy". *Fix:* invest in change management as a precursor to safer CI/CD on platforms. *Ref: "Change Management"*

- **Migration by clipboard:** chasing users with deadlines. *Fix:* engineering migration tooling first; automate; reserve TPMs for the long tail. *Ref: "Migration Antipatterns"*

- **Innersourcing-as-delegation:** "anyone can write the code!" — but they don't. *Fix:* don't open the codebase for non-platform engineers; reserve away teams for special cases. *Ref: "Innersourcing"*

- **PM fetishism:** "we'll just add product managers and call it a day." *Fix:* paired PM + engineering culture change; customer empathy across the team. *Ref: "Recognize That You Can't Just Rub Product Managers on It"*

- **Adoption-only metrics:** measuring mandate compliance as success. *Fix:* impact metrics; trust + love + alignment. *Ref: "A Success Red Herring: Adoption Metrics"*

- **Hiring engineers without customer empathy:** "here's the system, ask if you have questions." *Fix:* interview for empathy; put engineers on support. *Ref: "Interview for Customer Empathy"*

- **Forcing the platform as a build-vs-buy decision:** "we'll build it because we're Google." *Fix:* the platform-as-product lens is value-based, not technology-based. *Ref: "Defining 'Platform'"*

- **Conflating platform engineering with k8s:** Kubernetes isn't the platform — it's a primitive. *Fix:* understand that the platform abstracts primitives and orchestrates them. *Ref: "Change #1: Explosion of Choice"*

---

## Decision Heuristics / Checklists

**When to start a platform team:**
- Multiple application teams in place ✓
- Cooperative mechanisms are failing (Dunbar threshold crossed) ✓
- Glue costs exceed platform investment ✓
- Operational complexity consuming engineering time ✓
- Senior leadership support ✓
- Universally-acknowledged painful problem to start with ✓

**Platform type vs. shape:**
- 80% of use cases fit one workflow → **paved path**
- A gap exists not filled by existing product → **railway**
- Long tail of legacy unsupportable on the paved path → **two roads / pierceable abstraction**

**Build vs. buy vs. integrate:**
- Core competitive advantage and no good option → **build**
- Mature commercial solution exists → **buy**
- Open source with community → **integrate and contribute**

**Funding-model evolution (Stage 1 → 4):**
- Stage 1-2 → **central cost centre** (no friction)
- Stage 3 → **showback** (awareness, low politics)
- Stage 4+ → **chargeback** (accountability, but only after adoption is stable)

**Re-architecture decision:**
- Architecture blocks new capabilities ✓
- Maintenance costs growing exponentially ✓
- Operational incidents traceable to architectural limits ✓
- 12-month win identified ✓
- Migration cost estimated in years, not months ✓
- Leadership buy-in present ✓
- New-hire leadership NOT driving plan ✓

**Migration decision (persuade vs. force):**
- Security-required → **force** (give 6-12 months notice)
- UX/perf/cost → **persuade** (with incentives + migration tooling)
- Migration is incremental, not big-bang ✓
- Escape hatch to legacy exists ✓
- Customer impact is bounded ✓
- Lead time is sufficient ✓

**Stakeholder quadrants → communication strategy:**
- High power / high interest → manage closely; interlock meetings; demos
- High power / low interest → keep satisfied; periodic updates; executive summaries
- Low power / high interest → keep informed; newsletters; documentation
- Low power / low interest → monitor; minimal investment

**Stakeholder "say yes" criteria:**
- Aligns with roadmap direction ✓
- Has broad applicability beyond the requester ✓
- Won't create unsustainable support burden ✓
- Resource capacity exists without sacrificing higher-priority work ✓

**Hiring triggers:**
- **Engineer** when: code volume > 30% of team work, NOT just automation
- **Systems engineer** when: support load + glue reduction > 40% of team work
- **Reliability engineer** when: incident management, on-call burden, or SLO chasing requires dedicated focus
- **Specialist** when: you can name 3+ problems that only deep expertise solves
- **PM** when: engineering team can't talk to customers themselves OR >5 customer teams consuming
- **TPM** when: cross-team execution requires formal contracts or bureaucratic coordination

**On-call trigger to switch to operational-hell mode:**
- Pages/week > 5 → stabilise; cut features
- Customer-facing incident frequency growing quarter-over-quarter → stabilise
- Engineer attrition > 20%/year → stabilise
- Team expressing frustration with operational load → stabilise

**Tech radar (CNCF-style) for platforms:**
- **Adopt (default)**: established, widely-used, broad community, hireable expertise
- **Trial**: 1-2 year old tech, narrow community, interesting potential
- **Assess**: emerging tech, no track record, watch and discuss
- **Hold**: deprecated, problematic, or inappropriate for our scale

---

## Key Takeaways

1. **Platform engineering is a discipline, not a toolset** — defined by leverage, not by the technology stack.
2. **Treat the platform as a product** with internal customers — full PM discipline, even for captive audiences.
3. **Three pillars for success**: technology, product management, people leadership. Weakness in any one undermines the others.
4. **Four pillars of platform work**: product, software, breadth, operations.
5. **Adoption over mandate** — building something so good teams choose it.
6. **Avoid the Feature Shop Trap** — strategic roadmap over request triage.
7. **Six-pagers and bottom-up roadmaps** — structured decisions and grounded planning.
8. **Power-interest grid** — senior leaders, not daily users, are the most important stakeholders.
9. **Blameless culture and operational discipline** drive trust — and 70% / 20% / 10% allocates non-KTLO work.
10. **Staged rollouts and partner-led adoption** beat big-bang launches.
11. **DX is a first-class concern** — internal tools deserve the same UX investment as external products.
12. **Path to success is quarters and years, not sprints** — patience compounds.
13. **Manage cross-platform coherence** with independent PM + principal engineer alignment.
14. **Recognise organisational politics as a real engineering constraint** — invest in relationships.
15. **Start small, win trust, iterate** — pick a universally-painful problem; solve it well; expand.
16. **Rearchitecture, not v2** — incremental change with 12-month wins beats big-bang rewrites.
17. **Architecture security as a design force** — paved-path security by default, not bolted-on.
18. **Migrations are leverage opportunities** — engineering tooling, on-ramps, metadata tracking.
19. **Self-service + golden paths + observability + IDP (optional)** — the four pillars' daily expression.
20. **IDP and Kubernetes aren't the platform** — they're tools; the discipline is the product.
21. **Operational excellence OKRs** + **synthetic monitoring at 25% dev time** are the trust builders.
22. **Settlers and town planners, not pioneers, build platforms** at scale.
23. **Wins-and-Challenges** biweekly is the highest leverage communication ritual.
24. **Pioneer agility + town-planner integration** — let small teams innovate, integrate after 18 months.
25. **Pierceable abstractions** — one escape hatch to the 20% edge case keeps paved paths beloved.

---

## Cross-References

- Related: `../Mastering_Enterprise_Platform_Engineering.md` — Strategic framing of platform engineering for enterprise contexts.
- Related: `../Team_Topologies.md` — Stream-aligned / enabling / complicated-subsystem patterns; cognitive load.
- Related: `../Modern_Software_Engineering.md` — Modern engineering practices, DORA metrics, deployment frequency.
- Related: `../Building_Microservices.md` — Building platforms as microservices; the SOA debate.
- Related: `../Building_Multi-Tenant_SAAS.md` — Multi-tenancy is the canonical platform abstraction for SaaS.
- Related: `../Observability_Engineering.md` — Operational feedback practices (SLOs, synthetic monitoring, postmortems).
- Related: `../Fundamentals_of_Software_Architecture.md` — Architecture-astronaut avoidance; building-block thinking.
- Related: `../Software_Architecture_Metrics.md` — Impact metrics and measurement discipline.
- Related: `../Software_Architect_Elevator.md` — Communicating architecture to senior stakeholders.
- Related: `../Crafting_Engineering_Strategy.md` — Six-pagers, roadmaps, and the platform engineering strategy.
- Related: `../Technology_Strategy_Patterns.md` — Tech radar, buy/build, vendor evaluation.
- Topic index: `../INDEX.md`
