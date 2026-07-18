# Crafting Engineering Strategy

**Author:** Will Larson
**Topic tags:** `#general` `#architecture`
**Language focus:** Engineering organization / strategy; language-agnostic
**Sources:** `markdown_output/Crafting_Engineering_Strategy_-_Will_Larson/Crafting_Engineering_Strategy_-_Will_Larson.md` · `summaries/Crafting_Engineering_Strategy_-_Will_Larson.md`

## TL;DR
Engineering strategy is a *design problem* accessible to anyone, not a privilege reserved for executives. Larson adapts Rumelt's framework (diagnosis → guiding policy → coherent actions) into a five-step process: **Explore → Diagnose → Refine → Set Policy → Operate**. **Refinement is the kernel** — strategy testing, systems modeling, and Wardley mapping are the three primary tools. Operations make policies real; nudges are the most effective operational mechanism. Apply strategy at the right **altitude** (permissive + low = cheap; prescriptive + high = expensive).

---

## Best Practices by Topic

### Engineering Strategy Is a Design Problem (for Anyone)

**Principle:** "Strategy is not reserved for executives. It is the practice of making thoughtful decisions, and it is accessible to everyone." Every organization *always* has a strategy — the question is whether it's conscious.

**Do:**
- Recognize that strategy work is *intellectual AND mechanical* — even the best policies fail without attention to adoption.
- Document strategy to enable iteration, disagreement, and evolution (oral history depends on who you talk to).
- Achieve **information herd immunity**: every Staff-plus engineer and engineering manager knowing the strategy is enough for the org to function.

**Don't:**
- Don't skip writing strategy because "we have one already" — implicit strategy comes at high cost (misinterpretation, inconsistency across teams and time, hazard to new leaders).
- Don't let executive titles become a precondition for strategy work.

**Engineer-led strategies:**
- **"Take five, then synthesize"** — document how five related decisions have been made in your organization. Synthesize into a diagnosis and policy. You are naming the implicit strategy.
- **"Model, document, and share"** — model the approach you want others to adopt; document and share it.

*Ref: Crafting Engineering Strategy.md — "Chapter 2: Is Engineering Strategy Useful?"*

---

### Always Be Working on Exactly One Strategy

**Principle:** Limit work in progress. Start small, iterate until it works, then expand. What feels unambitious short-term compounds over time.

**Three strategic states an org may be in:**
1. Globally consistent (no need for more strategy work)
2. Consistent within teams (write strategy to unify)
3. Highly varied (urgent need for strategy)

**Do:**
- Assess **context level** first — do you understand the history of the area, the people who made past decisions, and why they were good at the time?
- Watch for degradation signals: rapid hiring, new playbook-driven external leaders, frequent reorganizations, ineffective communication of historical decisions.

**Don't:**
- Don't be the leader who attempts too much strategy — significantly more leaders fail by attempting too much than too little.

*Ref: Crafting Engineering Strategy.md — "Chapter 4: When Should You Write Strategy"*

---

### Strategy Altitude (Permissive × Prescriptive × Org Level)

**Principle:** **Altitude = how permissive a strategy is × where it's implemented.** Lower altitude + more permissive = cheaper strategies; you can write more of them.

**The volume formula:** To increase strategy volume, **reduce altitude, increase permissiveness, or both**.

| Strategy type | Cost | Best for |
|---------------|------|----------|
| Permissive + team-level | Cheapest | Most teams; lower-stakes decisions |
| Permissive + org-level | Medium | Setting direction without forcing consistency |
| Prescriptive + team-level | Medium | Critical team-specific mandates |
| Prescriptive + org-level | Most expensive | Org-wide critical mandates (use sparingly) |

**Do:**
- Roll out broad strategy work by focusing on **permissive strategies with escalation paths** (Carta model).
- Use one highly prescriptive area only when necessary.
- Be deliberate about altitude — if you need more strategy volume, lower the altitude.

**Don't:**
- Don't conflate altitude with importance. A low-altitude strategy can be vital.
- Don't go prescriptive at high altitude when permissive at lower altitude would work.

*Ref: Crafting Engineering Strategy.md — "Chapter 4: Strategy Altitude"*

---

### The Five-Step Strategy Process

**Steps:**
1. **Explore** — search problem and solution spaces before committing. Understand how 3 similar internal teams and 3 similar external companies have recently solved the same problem.
2. **Diagnose** — recognize the context the strategy must solve. Delay solutions until you understand the problem.
3. **Refine** — test raw ideas against reality (strategy testing, systems modeling, Wardley mapping).
4. **Set policy** — make tradeoffs to solve the diagnosis.
5. **Operate** — implement mechanisms that translate policy into active force.

**Do:**
- Take each step seriously. The biggest risk is skipping steps, especially refinement.
- Recognize the steps are not sacrosanct — the thinking matters more than the labels.
- Use Explore to break out of anchoring on one approach.

**Don't:**
- Don't skip Explore — the "Grand Migration" antipattern (new leaders declaring mass rewrites based on prior employer's stack) is the most common cause of failed strategy.

*Ref: Crafting Engineering Strategy.md — "Chapter 5: Steps to Build an Engineering Strategy"*

---

### Step 1: Explore

**Do:**
- Time-box exploration: < a few hours = suspicious; > a week = questionable.
- Mine your organization for internal precedent.
- Use your professional network — text peers during meetings (one Larson anecdote: got answers before a meeting ended, invalidating assumptions and resolving a multi-week disagreement).
- Read widely and narrowly — 10–20 industry-relevant works per year + targeted deep dives on the current topic.
- Save judgment for later — if no one involved has changed their mind, exploration isn't done.

**Don't:**
- Don't anchor on one approach without considering alternatives (especially common in executives copying their prior employer's stack).
- Don't stop at "I know this works" — internal approach may be imperfect but already implemented and maintained; your strategy can ride along as that team addresses imperfections.

*Ref: Crafting Engineering Strategy.md — "Chapter 6: Exploring"*

---

### Step 2: Diagnose

**Principle:** "Every strategy I've seen fail did so due to a lazy or inaccurate diagnosis." A proper diagnosis is very hard to fail with; almost impossible to succeed without one.

**Five-step diagnostic process:**
1. **Braindump** — write your best understanding from a blank sheet.
2. **Summarize exploration** — pull in diagnoses from similar situations, tag whether each fits.
3. **Mine for distinct perspectives** — talk to stakeholders who disagree with your early thinking.
4. **Synthesize into one internally consistent perspective** — represent all views competently, even disagreeing ones.
5. **Test drafts across perspectives** — sit with the strongest dissenters and iterate until they agree.

**Effective diagnosis traits:**
- Hard to argue against — a web of interconnected observations, facts, data.
- Includes data where possible (but accepts some will be missing — if the data existed, the decision would likely already be made).
- **Self-aware** — acknowledges your own role in creating the problem.
- **Whispers controversial parts** — finds professional, nonjudgmental ways to acknowledge uncomfortable truths.

**Do:**
- **Reframe blockers as part of the diagnosis.** "The executive team changes its mind too often" → "if we don't show concrete progress quickly, our strategy is likely to fail."

**Don't:**
- Don't exclude uncomfortable organizational or individual truths — that makes strategies impossible to evaluate or recreate.
- Don't allow diagnosis to block on missing data — acknowledge gaps and proceed.

*Ref: Crafting Engineering Strategy.md — "Chapter 7: Diagnosis"*

---

### Step 3: Refine (THE KERNEL)

**Principle:** Refinement is the **highest-impact, most-neglected step**. Raw ideas must be tested against reality.

**Why refinement is skipped:**
- Low-altitude teams rarely skip it (they lack authority to force adoption).
- Executives skip it because they can mandate adoption and feel pressure to make early impressions.
- Promotion-driven engineers pursue novel, ambitious projects that fail after initial proof points but secure the promotion.
- Artificial deadlines freeze thinking.

**Three refinement tools:**

| Tool | Use when |
|------|----------|
| **Strategy testing** | You need to verify a specific approach works on a narrow slice |
| **Systems modeling** | You're unsure where leverage points are; you have data; stakeholders disagree on unstated intuitions |
| **Wardley mapping** | Your strategy involves dynamic technology or spans 5+ years |

**Do:**
- Find the narrowest, deepest slice of your strategy and iterate until you see evidence it works.
- Assume people mean well and failures are due to friction and poor ergonomics.
- Measure impact, not just adoption.

**Don't:**
- Don't manufacture consent to create the illusion of refinement.
- Don't discard counterevidence because of side goals.

*Ref: Crafting Engineering Strategy.md — "Chapter 8: Refining"*

---

### Strategy Testing (Refinement Tool #1)

**Principle:** Identify the narrowest, deepest available slice and iterate until confident the approach works. "Prematurely rolling out a strategy prevents evaluating whether it is effective. Pressure changes behavior, creating the impression of compliance while minimizing actual change."

**Two roles for testing:**
- **Sponsor** — provides authority, makes quick decisions, marshals support, prevents scope creep. Must be genuinely authorized and available for rapid escalations.
- **Guide** — translates strategy into particulars, tracks workstreams, escalates issues. Must execute at pace without getting derailed.

**The only absolute requirement:** sponsor, guide, and key folks must meet every week. The meeting should be heavy on debugging and light on presentation.

**Telltale sign of untested strategy:** "pressure without a plan" — sounds correct but lacks concrete details.

**Ask:** Are there numbers showing the strategy is driving desired impact? If numbers aren't moving, is there a clear mechanism for debugging?

**Do:**
- Identify impact metrics (not adoption metrics).
- Establish a weekly sponsor/guide/key-folks cadence.

**Don't:**
- Don't roll out prematurely. If you can't officially pause, find an indirect mechanism to pause implicitly.

*Ref: Crafting Engineering Strategy.md — "Chapter 13: Strategy Testing for Iterative Refinement"*

---

### Systems Modeling (Refinement Tool #2)

**Principle:** Use **stocks and flows** to cheaply determine which levers might be effective in complex systems.

**Use when:**
1. Unsure where leverage points are in a complex system.
2. Significant data to compare against.
3. Stakeholders' disagreements are based on unstated intuitions.

**Modeling process:**
1. Sketch stocks and flows on paper.
2. Reason about how potential changes would shift flows.
3. Model in a spreadsheet, starting with happy path then exception paths.
4. Sensitivity analysis — exercise model with different starting values.
5. Document what you learned, focusing on insights first.

**Five critical cautions:**
- When your model and reality conflict, **reality is always right**.
- Models are immutable, but reality is not.
- Every model omits information; some omit critical information.
- Use modeling in tandem with judgment, not as a replacement.

**Real outcome from Larson:** A ride-share company's driver-lifecycle model revealed that improving onboarding had little impact on active drivers — the real leverage was reactivating departed and suspended drivers. This counterintuitive insight drove strategy.

*Ref: Crafting Engineering Strategy.md — "Chapter 14: Systems Modeling"*

---

### Wardley Mapping (Refinement Tool #3)

**Principle:** Map **users → needs → capabilities** with axes for **commoditization (genesis → custom → product → commodity)** and **visibility**.

**Components of a Wardley map:**
- **Users** (top) — cohorts.
- **Needs** (directly connected to users) — tasks to accomplish.
- **Capabilities** (connected to needs) — underlying technical requirements.
- **Pipelines** — show evolution over time.
- **Overlays** — group capabilities by team or attribute.
- **Arrows** — predicted future changes.

**When to use:**
- Highly dynamic technology environment.
- Strategy spans 5+ years.
- Strategy is built on an evolving foundation.
- Less useful for detail-level optimization.

**Mapping process:**
1. Start small and iterate.
2. List users, needs, capabilities.
3. Establish value chains connecting them.
4. Plot on a Wardley map.
5. Study current state.
6. Predict how the map will evolve.
7. Study the future state.
8. Share for feedback.
9. Document what you learned.

**Do:**
- Use Wardley mapping for ecosystem evolution (e.g., LLM ecosystem is likely to consolidate to fewer, broader platforms).
- Skip Wardley's "doctrine" and "gameplay" distinctions — they're specialized for business strategy, less directly applicable to engineering.

**Don't:**
- Don't try to use Wardley mapping for fine-grained operational decisions — use it for ecosystem-level situational awareness.

*Ref: Crafting Engineering Strategy.md — "Chapter 15: Wardley Maps"*

---

### Step 4: Set Policy

**Principle:** Policy interprets your diagnosis into a concrete plan. An effective policy solves the entirety of the diagnosis.

**Steps:**
1. Review diagnosis for completeness.
2. Select policies that address the diagnosis.
3. Consolidate overlapping policies.
4. Backtest against recent decisions.
5. Mine for conflict (emphasize feedback from those who disagree).
6. Refine if uncertain.

**Four policy categories:**

| Category | Definition | When |
|----------|-----------|------|
| **Approvals** | Define process for recurring decisions | Repeated decisions with named approver |
| **Allocations** | Describe how resources split across investments | The most concrete statement of priority |
| **Direction** | Explicit instruction on how decision *must* be made | You value consistency over individual judgment |
| **Guidance** | Recommendation on how decision *should* be made | You can articulate destination but not path |

**Two criteria for effective policies:**
- **Applicable** — useful for navigating real-world tradeoffs.
- **Enforced** — teams are held accountable.

**Do:**
- Match each policy to a specific diagnosis.
- Recognize that **competing policy proposals indicate a gap in diagnosis** — align on diagnosis to invalidate some options.
- Use guidance where direction would be premature.
- Recognize constraints — never propose a policy you cannot fund or enforce.

**Don't:**
- Don't propose novel policies when adaptations of well-known approaches suffice.
- Don't ignore missing strategies from other functions — include the absence in your diagnosis and move forward.

*Ref: Crafting Engineering Strategy.md — "Chapter 9: Setting Policy"*

---

### Step 5: Operate

**Principle:** Operations make policies work. Six-factor rubric for operational mechanisms:

| Factor | Question |
|--------|----------|
| Measurability | Can you measure leading and lagging indicators? |
| Adoption cost | How much work to migrate? |
| User ease/burden | Does it make users' work easier or harder? |
| Provider ease/burden | How much ongoing maintenance? |
| Reliance on authority | What happens if the sponsoring executive departs? |
| Cultural alignment | Will the org fight this at every step? |

**Effective mechanisms (ranked, strongest first):**

1. **Automation** — most effective when paired with good UX (Uber service provisioning).
2. **Nudges** — most effective operational mechanism. Bring information to people at exactly the moment it's useful.
3. **Inspection mechanisms** — evaluate whether policy is succeeding. Specify where/how data will be tracked; an inspection mechanism that can silently fail accomplishes nothing.
4. **Approval and advice forums** — handle edge cases where policy is unclear. Simplest form: exceptions granted by a named individual in writing.
5. **Deferral to future work** — explicitly defer what you can't yet do, with a clear return date.
6. **Meetings** — universal but expensive. Iterate toward cancellation.

**Do:**
- Write a Slack-nudge when teams' cloud spend accelerates, pointing them to explanatory charts.
- Limit total number of nudges — each should have an explicit, actionable recipient action.
- Use Carta's Navigator program pattern: grant executive authority for technical decisions to named engineers in each area.
- Use *automated nudges* over *authoritative mandates* when possible.

**Don't:**
- Don't rely on top-down pronouncements, education-as-announcement rollouts, mandatory recurring trainings, or "just change the culture" — they all have better alternatives.
- Don't punish the black market — fix the underlying process that drove people to bypass it.

*Ref: Crafting Engineering Strategy.md — "Chapter 10: Operations"*

---

### Strategy in Challenging Environments

**Do:**
- **Low-trust environments:** whisper the controversial parts. Translate difficult messages into softer versions.
- **Poor-judgment environments:** write strategy to educate colleagues about tradeoffs.
- **Missing strategies:** accept the ambiguity as fact and work around it. Never allow missing info to block forward progress.
- **Chaotic environments:** strategies do not require stability; they require awareness. In dynamic periods, protect capacity in two-week chunks.
- **Surviving others' bad strategy:** write a private strategy that acknowledges the imposed policy as a static, unavoidable truth, then make practical decisions within that context.

**Don't:**
- Don't do strategy to satisfy an emotional need for immediate impact — invest in long-term progress instead.
- Don't do strategy when another part of the organization is already working on the same problem.

*Ref: Crafting Engineering Strategy.md — "Chapter 12: Bridging Theory and Practice"*

---

### Writing Readable Engineering Strategies (Inverted Structure)

**Principle:** The order for writing (Explore → Diagnose → Refine → Set Policy → Operate) is a poor order for reading. Most strategy readers just want to understand the policy so they can apply it.

**Recommended document order (for readers):**
1. **Policy** — what does the strategy require or allow?
2. **Operation** — how is it enforced? How are exceptions granted?
3. **Refine** — what load-bearing details informed the strategy?
4. **Diagnose** — what general trends steered the thinking?
5. **Explore** — what is the high-level context?

**Strategy refactoring:** merge sections where it improves usability (e.g., LLM adoption strategy merges Refine into Diagnose and folds Operation alongside Policy).

**Do:**
- Have someone uninvolved read the document before release.
- Include explicit commenting period and office hours.
- Maintain your own strategy template with consistent metadata.
- Disable in-document commenting after release; move discussion to a better forum.

**Don't:**
- Don't write in chronological order — write in reader-priority order.

*Ref: Crafting Engineering Strategy.md — "Chapter 11: Writing Readable Engineering Strategies"*

---

### Who Should Do Strategy (Role-Specific Approaches)

| Role | Approach | Tools available |
|------|----------|-----------------|
| **Engineer** | Take five + synthesize; model-document-share | Nudges, building real datasets |
| **Executive** | Mandate + cajole + more latitude | Authority + budget + peers to satisfy |
| **Low-trust environment** | Whisper controversial parts | Translation, not suppression |
| **Poor-judgment environment** | Write to educate | Documented strategy |

**Executives have an easier time doing strategy but a harder time learning to do it *well*** — the appearance of progress is easier to manufacture than actual progress. Mandates only matter if there are consequences.

*Ref: Crafting Engineering Strategy.md — "Chapter 3: Who Gets to Do Strategy?"*

---

### Strategy Quality Evaluation Rubric (Speed × Cost × Impact)

**Three-question rubric, 0–3 points each, max 9:**

| Dimension | 3 points | 2 points | 1 point | 0 points |
|-----------|----------|----------|---------|----------|
| **Speed** (refinement cycle time) | Daily/weekly | Monthly | Quarterly | Longer |
| **Cost** (refinement cost) | Single-team | Small cross-team | Large cross-team flexible | Large cross-team rigid |
| **Impact** (diagnosis coverage) | Full problem | Most essential portion | Simple portion | None |

**Threshold:** 6+ is a high-quality strategy. Below 6 warrants introspection.

**Lifecycle insight:** A strategy can score well in Phase 1 and degrade in Phase 2 (Uber's service migration scored 7 in Phase 1, 4 in Phase 2). Apply the rubric to each phase.

**Do:**
- Stop strategies that no longer score well — stopping is often a good sign. Giving up on high-altitude strategies is almost always right.

**Don't:**
- Don't evaluate other companies' strategies — missing context is an impenetrable veil.

*Ref: Crafting Engineering Strategy.md — "Chapter 23: Is This Strategy Any Good?"*

---

### Engineering Strategy Changes Companies (5 Ways)

**The five ways strategy changes companies:**
1. **Creating alignment** — clear strategy makes it clear what game is being played; people can decide whether to participate.
2. **Concentrating investment** — not decomposing the monolith lets you invest the majority of tooling in one language, one test suite, one deployment mechanism.
3. **Making valuable properties available through universal adoption** — policies like N-1 backfilling or DR configurations only work when consistently adopted.
4. **Focusing execution** — Stripe's Sorbet strategy let 10 engineers push the Ruby monolith toward static typing without distracting the larger org.
5. **Creating a knowledge repository** — documented strategy makes onboarding, especially of senior hires, much more effective.

*Ref: Crafting Engineering Strategy.md — "Chapter 2: Is Engineering Strategy Useful?"*

---

### Real Case Study Patterns (Lessons from 10 Cases)

**Uber service migration (Document 16-1) — lessons:**
- Use systems modeling to prove manual provisioning can't scale.
- Constrain manual provisioning to one engineer while investing in automation.
- Make self-service safely usable by new hires.
- Prefer good defaults over requiring user input.
- Scored 7/9 on the rubric.

**LLM adoption (Document 17-1) — lessons:**
- Pick one provider (Anthropic via AWS Bedrock) to avoid multi-implementation maintenance.
- Mandate one developer productivity tool and one internal tooling initiative.
- Include a six-month review cycle before committing further.
- Counterintuitive insight from modeling: reactivation of departed drivers matters more than onboarding.

**Private equity ownership (Document 18-1) — lessons:**
- N-1 backfill policy + principal caps can reduce headcount costs by ~5% per year without layoffs.
- Defer planning around reductions until specific targets arrive.

**Customer data access (Document 19-1) — lessons:**
- Frame security and usability as *complementary*, not opposed. "Framing security as a tradeoff with usability is a sign you are having the wrong discussion."
- Measure progress on % of access justified by user-comprehensible, automated rationales.
- Expose a log of data accesses to users themselves.
- Expire unused roles after 90 days.

**Service architecture (Document 20-1) — lessons:**
- A strategy of *reversing* the decomposition trend (e.g., merge existing services into business unit monoliths) can be the right call.
- "No new services except for new business units" is a valid allocation policy.

**Calm product engineering (Document 21-1) — lessons:**
- "We are a product engineering company" as a clear directional policy.
- All new code in the monolith, new technologies only for valuable product capabilities.
- Exceptions granted by the CTO in writing — explicit approval forum.

**Stripe strategies (Document 22) — lessons:**
- API deprecation: never deprecate APIs without unavoidable requirement. Maintain translation layer for all prior API versions.
- Sorbet: custom static type checker for Ruby > monolith decomposition.
- Acquisition integration: launch joint product within 6 months; defer contentious decisions; paired-lead escalations.

*Ref: Crafting Engineering Strategy.md — "Part IV: Case Studies"*

---

### Cargo Culting — The Largest Threat to Strategy Operations

**Principle:** "Cargo-culting" = recreating a process without understanding the circumstances that made it effective.

**Do:**
- Apply the strategy rubric to each phase of historical strategies — learn from failed strategies as much as successful ones.

**Don't:**
- Don't copy strategies from blog posts — missing context (how many phases, cost, reality vs. blog) is an impenetrable veil.

*Ref: Crafting Engineering Strategy.md — "Chapter 10: Operations"*

---

### Practice & Improvement Loop

**Do:**
- If existing strategies aren't working — debug and fix one.
- If no strategies are documented — document one.
- If strategies have low adoption — iterate on operational mechanisms.
- If strategies are effective — find a new problem to work on.
- If you can't share internally — practice with trusted external peers.

**Always:**
- Track your work.
- Review quarterly with a peer.
- If not making progress, sit down with someone more experienced to debug.

**If you believe you cannot do strategy in your current role:** lower your altitude until you find a scale where you can operate. Only *you* can forbid yourself from developing personal strategies.

*Ref: Crafting Engineering Strategy.md — "Chapter 24: How to Get Better at Strategy"*

---

## Anti-Patterns & Common Mistakes

- **"Grand Migration" antipattern:** new leader declares mass rewrite using prior employer's stack. → *fix:* Explore phase must surface 3 similar internal + 3 similar external solutions.
- **Skipping refinement:** executives confuse sounding ambitious with being effective. → *fix:* mandate refinement with systems modeling or strategy testing.
- **Promotion-driven strategy:** pursue novel, ambitious projects that fail after initial proof points. → *fix:* measure impact, not adoption.
- **Manufactured consent:** creating the illusion of refinement. → *fix:* real sponsor/guide cadence, real data.
- **Counterevidence discarded because of side goals.** → *fix:* Whack-a-mole the political pressure; focus on data.
- **Cargo-culting strategies from blog posts.** → *fix:* you cannot know the context — apply the rubric to your own situation.
- **Authority without operational mechanisms:** policies that fade quietly. → *fix:* pick from the 6 mechanism types (automation, nudges, inspection, approval forums, deferral, meetings).
- **Strategy as emotional need for immediate impact.** → *fix:* invest in long-term progress instead.
- **Stopping strategies that should continue (or vice versa).** → *fix:* apply the rubric (Speed/Cost/Impact) to each phase.
- **Over-strategizing:** significantly more leaders fail by attempting too much than too little. → *fix:* always be working on exactly one strategy; use altitude to manage volume.
- **Bad timing of operational rollouts.** → *fix:* sprint capacity, office hours, dedicated roll-out phase.

---

## Decision Heuristics / Checklists

- **Should we write strategy?**
  - Globally consistent → no.
  - Consistent within teams OR highly varied → yes.
  - Rapid hiring / playbook-driven new leaders / frequent reorganizations → yes (trend-based triggers).
- **How much strategy?**
  - Always be working on exactly one strategy.
  - To increase volume: lower altitude, increase permissiveness, or both.
- **Picking altitude:** team-level permissive for most cases; org-level prescriptive sparingly for critical mandates.
- **Exploring time-box:** < a few hours = suspicious; > a week = questionable.
- **Refinement tool selection:**
  - Specific narrow approach → Strategy testing
  - Leverage points in complex system → Systems modeling
  - Dynamic ecosystem / 5+ year strategy → Wardley mapping
- **Policy category selection:**
  - Repeated decisions with named approver → Approvals
  - How to split resources → Allocations
  - Consistency valued over judgment → Direction
  - Destination clear, path unclear → Guidance
- **Operational mechanism selection (in order of effectiveness):**
  1. Automation (best with good UX)
  2. Nudges (most effective overall)
  3. Inspection (must specify data location)
  4. Approval forums (named individual in writing)
  5. Deferral (acknowledge missing mechanism)
  6. Meetings (iterate toward cancellation)
- **Strategy quality threshold:** rubric score ≥ 6 (out of 9).
- **Nudge hygiene:** limit total nudges; each must have explicit recipient action with clear instructions.
- **Strategic state assessment:** ask "globally consistent / consistent within teams / highly varied?"
- **Compromising time horizon:** 70% per-step transition × 9 steps = 4% completion (50% per-step = 0.2%). Plan for long arcs.
- **Whisper controversial parts in low-trust environments.**
- **Reformat documents for readers:** Policy → Operation → Refine → Diagnose → Explore.
- **Self-assessment for strategy makers:** are you treating it as intellectual + mechanical? Are you skipping refinement?

---

## Key Takeaways

1. **There is always a strategy**, even if it's unwritten. Finding and documenting it is step one.
2. **The five-step process** (Explore → Diagnose → Refine → Set Policy → Operate) provides repeatable structure. Skipping steps — especially refinement — is the most common cause of failure.
3. **Refinement is the kernel.** Strategy testing, systems modeling, Wardley mapping. Use strategy testing for ambiguous problems; systems modeling for complex leverage; Wardley mapping for ecosystem evolution.
4. **Operations matter more than most strategists think.** Policies without operational mechanisms fade quietly. Nudges are most effective; top-down pronouncements are least.
5. **Write for readers, not writers.** Invert document structure. Lead with policy and operations.
6. **Strategy is iterative, not waterfall.** Good strategies embrace change and refine continuously.
7. **Anyone can do strategy.** Engineers use "take five, then synthesize" and "model, document, share." Executives have more tools but fewer guardrails.
8. **The evaluation rubric** (Speed × Cost × Impact, 0–9, threshold 6) structures strategy assessment.
9. **Strategy altitude** controls cost: permissive + low altitude = cheap, high-volume strategy work.
10. **Strategy aging is real.** A strategy that scores 7 in Phase 1 may score 4 in Phase 2.
11. **The details matter enormously.** The same general strategy that works at one company can fail at another. Cargo-culting is the largest operational threat.
12. **There is no SKU for transformation.** Money can't buy organizational capability. Internal staff must do the learning cycles.
13. **Engineering organizations routinely waste decades of their teams' lives** by refusing to engage with the reality of their problems. A bit of rigor in strategic thinking is the bare minimum.
14. **Stopping a strategy is often a good sign** — all strategies compete with strategies at other altitudes.
15. **Nudges over authority.** When in doubt, build a nudge before asking for a mandate.

---

## Cross-References

- Related: [[../Software_Architecture_Metrics.md]] — measuring strategic state and consistency
- Related: [[../Building_Evolutionary_Architectures.md]] — fitness functions as automated strategy enforcement
- Related: [[../Software_Architect_Elevator.md]] — communicating strategy up and down the org
- Related: [[../Head_First_Software_Architecture.md]] — architectural decisions and ADRs
- Topic index: [[../INDEX.md]]
