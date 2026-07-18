# Crafting Engineering Strategy

**Author:** Will Larson (CTO at Imprint; prior: Carta, Calm, Stripe, Uber; also author of *Staff Engineer*, *The Engineering Executive's Primer*, *An Elegant Puzzle*)
**Topic tags:** `#strategy` `#leadership` `#general`
**Language focus:** Engineering organization, leadership, decision-making, people and process
**Sources:** `markdown_output/Crafting_Engineering_Strategy_-_Will_Larson/Crafting_Engineering_Strategy_-_Will_Larson.md` · `summaries/Crafting_Engineering_Strategy_-_Will_Larson.md`

## TL;DR

Engineering strategy is a *design problem* accessible to anyone in the organization. Larson adapts Richard Rumelt's diagnosis → guiding policy → coherent actions into a five-step process: **Explore → Diagnose → Refine → Set Policy → Operate**, with **strategy altitude** (permissive vs. prescriptive × team vs. org) and a **3-question rubric** (Speed × Cost × Impact, 0–9, threshold 6) for evaluation. Refinement is the kernel; nudges are the most effective operational mechanism. Always be working on **exactly one strategy**; accept ambiguity; whisper the controversial parts; treat policy as a subset of strategy; treat operation as the mechanism that makes policy real; document for readers, not writers.

---

## Best Practices by Topic

### 1. Treat Engineering Strategy as a Design Problem (Not an Executive Perk)

**Principle:** *There is always a strategy*, even when no one has written one. Strategy work is the practice of making thoughtful decisions; it is accessible to anyone in the engineering organization willing to do it.

**Do:**
- Use Larson's "take five, then synthesize": document how five related current or historical decisions have been made, then synthesize a diagnosis and policy. You are naming the implicit strategy, which makes it possible to evaluate and improve it.
- Use the "model, document, and share" approach when you lack authority: do the work, write it up, and let adoption follow from the work's success.
- Recognize that every organization follows a strategy embedded in its repeated decisions, even if no one has written it down. *Recognition is the first step toward improvement.*
- Adopt a maintenance strategy before anything else: *William Gibson has said, "The future is already here—it's just not very evenly distributed."* In the same sense, there is *always* a strategy embedded into an organization's decisions—even if that strategy is only visible to a small group and is quickly forgotten.
- Understand the five ways strategies change companies: create alignment, concentrate investment, make valuable properties available only through universal adoption (e.g., N-1 backfill, DR config), focus execution, create a knowledge repository.

**Don't:**
- Don't treat strategy as reserved for executives or Staff-plus engineers—anyone can do it.
- Don't "snack" on strategy as a way to avoid more impactful work; treat it as a real investment of time.
- Don't avoid strategy because your organization's culture would frown on the diagnosis; the workaround is to *whisper the controversial parts*, not to abandon strategy work.
- Don't assume a missing strategy means a missing-strategy organization; unbundle from "no strategy exists" and look for *which* implicit policy is actually being enforced.

*Ref: Crafting_Engineering_Strategy.md — "There's Always a Strategy" / "Strategy Changes Companies" / "Doing Strategy as an Engineer" / "It's Always Been Your Strategy"*

---

### 2. Apply Rumelt's Three Pillars: Diagnosis, Guiding Policy, Coherent Actions

**Principle:** Good strategy starts with diagnosis—the hardest part, the one most often skipped, and the one on which the rest depends. Strategy is meaningless without a diagnosis because policy without diagnosis is decoration and diagnosis without policy is observation.

**Do:**
- Invest the majority of your strategy time in diagnosis; once the diagnosis is correct, the policy is often inevitable (and sometimes boring).
- Frame the diagnosis in terms of "if we don't recognize X, we will continue to suffer Y" so that the consequences of not acting are concrete.
- Use data to support or critique perspectives, not to win arguments; data speaks louder than passion.
- Acknowledge uncomfortable truths about the organization in the diagnosis; if you omit them, the strategy becomes impossible to evaluate and replicate.
- Capture perspectives you initially disagree with; they often reveal what you missed.
- Treat guiding policy as a *tradeoff*. If a guiding policy doesn't imply a tradeoff, be suspicious: "working harder to get it done" isn't really a guiding policy.

**Don't:**
- Don't start with policy or solution; defer thinking about solutions until you understand the problem.
- Don't pretend the data exists when it doesn't; missing data is the norm in interesting strategy work, and the absence of data is itself a constraint.
- Don't accept the lazy diagnosis that "we just need to work harder" or "if only leadership would decide"—reframe the thing preventing you as a condition your strategy must address.

**Code/Diagram (Rumelt's three pillars, paraphrased by Larson):**

```
1. DIAGNOSIS
   A theory describing the nature of the challenge. Identify root causes.
   Example: "high work-in-progress is preventing us from finishing any
   tasks, so we are increasingly behind each sprint."

2. GUIDING POLICY
   A series of general policies to grapple with the challenge. Implicit
   or explicit tradeoffs.
   Example: "Only hire for the most urgent team; do not spread hires
   across all teams." If a guiding policy doesn't imply a tradeoff,
   be suspicious of it.

3. COHERENT ACTIONS
   A set of specific actions to address the challenge, directed by the
   guiding policy. The most important part—strategy is only meaningful
   if it leads to aligned action.
```

*Ref: Crafting_Engineering_Strategy.md — "Adapting Rumelt for Engineering" / "Diagnosis Is Strategy's Foundation" / "How to Develop Your Diagnosis" / "Reframe Blockers as Part of Your Diagnosis" / "Whisper the Controversial Parts"*

---

### 3. Use the Five-Step Process: Explore → Diagnose → Refine → Set Policy → Operate

**Principle:** Strategy fails more often from skipped steps than from unsound thinking. The order exists because each step feeds the next.

**Do:**
- Always start with **Exploration** before committing to an approach.
- Move through Diagnose, Refine (with strategy testing, systems modeling, or Wardley mapping), Set Policy, and Operate in that order—each step is an input to the next.
- End every strategy document with **operations**; policy without mechanisms fades quietly.
- Always treat policy as a *subset* of strategy (it depends on the diagnosis) and operation as the mechanism that makes policy real.
- Remember that the structure is *not* sacrosanct—it can be refined or merged for readability once written.

**Don't:**
- Don't skip refinement; it's the highest-impact step and the most neglected.
- Don't freeze your thinking under artificial deadlines; treat the deadline as the start of refinement, not the end.
- Don't let the structure become lumbering and callous: if a section doesn't serve the document's user, discard it—as long as you can explain what that section was meant to accomplish.

```
STEP 1: EXPLORING   – search problem and solution spaces before
                       committing; understand how three similar
                       internal teams and three similar external
                       companies have solved this problem.
STEP 2: DIAGNOSING  – correctly recognize the context the strategy
                       needs to solve before deciding on policies.
                       Delay thinking about solutions.
STEP 3: REFINING    – take raw ideas and test them against reality.
                       Three techniques: strategy testing, systems
                       modeling, Wardley mapping.
STEP 4: SET POLICY  – make the tradeoffs and decisions to solve the
                       diagnosis.
STEP 5: OPERATE     – implement concrete mechanisms that translate
                       policy into an active force.
```

*Ref: Crafting_Engineering_Strategy.md — "Steps to Build an Engineering Strategy" / "Step 1: Exploring" through "Step 5: Operations" / "How the Steps Become Strategy"*

---

### 4. Explore Before You Anchor (and Time-Box It)

**Principle:** A surprising number of strategies are doomed because their authors anchor on one approach without considering alternatives. Exploration is the antidote to early anchoring, especially when senior leaders "port their prior employer's playbook" via a **Grand Migration**.

**Do:**
- Explore until you know how **three similar internal teams** and **three similar external companies** have recently solved the same problem. Be able to explain the *thinking* behind those decisions.
- Time-box exploration: less than a few hours is suspicious; more than a week is questionable.
- Follow the five-step exploration process:
  1. Gather every resource related to the problem.
  2. Do web/search/prompt work and check with current/prior colleagues about what's missing.
  3. Summarize resources, separating ones to explore from ones merely worth mentioning.
  4. Work through the list one by one, collecting notes.
  5. Stop once you understand how a handful of similar teams have approached the problem.
- Mine your organization for internal precedent ("take five, then synthesize"). Sometimes the internal approach isn't ideal but is still superior because it's already implemented and maintained by someone else; your strategy can *ride along* as that team addresses imperfections.
- Use your professional network—especially for topics with limited public information (security, compliance, scaled operations). Larson has texted industry peers *during* a meeting to invalidate the room's assumptions before the meeting ended.
- Read widely (10–20 industry-relevant works per year on diverse topics) AND read narrowly (e.g., reading Borg and Mesos papers before Uber's service migration).
- *Save judgment for later*: if no one involved in the strategy has changed their mind about something they believed, exploration is not done. This is especially true for senior leaders whose beliefs are well-justified by years of experience but whose prior experiences have gone stale.

**Don't:**
- Don't run the Grand Migration pattern: a new leader declares a massive migration to their prior employer's tech stack and pushes it even when it becomes clear it doesn't solve the problem.
- Don't pass "good/bad" judgment on approaches during exploration; pass it after, when you've actually compared enough.
- Don't refuse to look at internal precedent; most organizations have existing internal solutions you've never heard of.

*Ref: Crafting_Engineering_Strategy.md — "What Is Exploration?" / "When to Explore" / "How to Explore" / "Mine Your Organization for Internal Precedent" / "Using Your Network" / "Read Widely; Read Narrowly" / "Save Judgment for Later"*

---

### 5. Diagnosis Is Strategy's Foundation (and Reframe Blocker as Part of Diagnosis)

**Principle:** *Every strategy I've seen fail did so due to a lazy or inaccurate diagnosis. It is very challenging to fail once you have a proper diagnosis, and almost impossible to succeed without one.*

**Do:**
- Use Larson's five-step structured approach to diagnosis:
  1. **Braindump** from a blank sheet—write your best understanding of the circumstances.
  2. **Summarize exploration**—pull in every diagnosis from similar situations (internal/external), tag whether it fits or needs adjustment.
  3. **Mine for distinct perspectives**—talk to stakeholders who disagree with your early thinking; don't agree with them, *understand* them (anchor in *The Crux* by Richard Rumelt: "testing, adjusting, and changing the frame").
  4. **Synthesize into one internally consistent perspective**—represent all views competently, even those you disagree with, so the policy can be evaluated against each. Hold **one author** accountable for the unified synthesis (joint ownership tends to fracture perspectives).
  5. **Test drafts across perspectives**—sit with the people who disagree most fervently until they agree you've accurately captured their views.
- Incorporate data into diagnosis: include data analysis with links to raw sources, so readers don't have to interpret the data themselves. Include data to *support* a perspective *and* to *critique* an overstated view.
- **Whisper the controversial parts**: find professional, nonjudgmental ways to acknowledge circumstances that created the problem you're solving, even if executives or peers will be unhappy. *Excluding critical parts makes strategies impossible to evaluate, copy, or recreate.*
- **Reframe blockers as part of the diagnosis**: when something seems to prevent strategy work, transform it: "the executive team changes its mind too often" → "if we don't show concrete progress quickly, our strategy is likely to fail."
- Demonstrate **self-awareness** by recognizing your own role in creating the problems your diagnosis identifies. *Changing your mind without new data is chaotic leadership; with new data is thoughtful leadership.*

**Don't:**
- Don't accept the lazy diagnosis that "we just need to work harder"; reframe the prevention as a condition to address.
- Don't get caught up in *perfecting* diagnosis details before refining; *allow yourself to be directionally correct rather than perfectly correct* to cover a lot of territory quickly.
- Don't allow requests for data to prevent forward progress indefinitely; fulfill one or two requests per stakeholder and then hold the line.
- Don't pretend the data exists when it doesn't—the absence of data is itself a diagnostic constraint, and the data you wish existed is often exactly the data that would have settled the decision already.

**Verbatim diagnosis examples from the book:**

```
UBER PROVISIONING (whisper pattern):
"Within infrastructure engineering, there is a team of four engineers
responsible for service provisioning today. While our organization is
growing at a similar rate as product engineering, none of that
additional headcount is being allocated directly to the team working
on service provisioning. We do not anticipate this changing."
— author found a factual, nonjudgmental way to acknowledge an
uncomfortable constraint.

PRIVATE EQUITY (whisper pattern):
"Based on general practice, it seems likely that our new Private Equity
ownership will expect us to reduce R&D headcount costs through a
reduction. However, without concrete details, we cannot yet make
structured decisions. Our strategy will depend significantly on the
scale of any proposed reductions."
```

*Ref: Crafting_Engineering_Strategy.md — "Diagnosis Is Strategy's Foundation" / "How to Develop Your Diagnosis" / "Incorporating Data into Your Diagnosis" / "Whisper the Controversial Parts" / "Reframe Blockers as Part of Your Diagnosis" / "The Role of Self-Aareness"*

---

### 6. Refinement Is the Kernel of Effective Strategy

**Principle:** Refinement is the highest-impact step of strategy creation and the most neglected. It takes raw, unproven ideas and tests them against reality. Skipping refinement is the most damning antipattern.

**Do:**
- Remember why refinement matters: Stripe's failed Agile rollout solved the easiest part of the problem (awareness) without addressing the harder parts (prioritization across stakeholders). Uber's service migration succeeded precisely because the team relied on refinement through systems modeling and strategy testing.
- Understand why refinement gets skipped so you can fight those pressures:
  - **Low-altitude teams** almost always refine because they lack authority to force adoption.
  - **Executives** skip refinement because they can mandate adoption and are pressured to make early impressions. They confuse *sounding ambitious* with being effective.
  - **Promotion-driven engineers** in permissive-strategy organizations pursue novel, ambitious projects that fail after initial proof points but secure the promotion.
  - **Artificial deadlines** cause people to freeze thinking rather than iterating.
- Use the right tool for the right refinement job:
  - **Strategy testing** — for ambiguous problems where diagnosis is difficult (e.g., "what is code quality?").
  - **Systems modeling** — when unsure where leverage points are in a complex system, when you have significant data to compare against, or when stakeholders' disagreements are based on unstated intuitions.
  - **Wardley mapping** — for ecosystem-aware strategies, dynamic technologies, or five-plus-year time horizons.
- Build your toolkit slowly: "skim over all of them and pick one that seems most applicable to a current problem you're working on … It's extraordinarily powerful to unlock your first tool, and worthwhile to slowly expand your experience with other tools over time."
- Share what you *learn* from techniques, not the techniques themselves. Techniques are inputs into strategy, never a reliable sole backer.

**Don't:**
- Don't skip refinement entirely—the most common antipattern.
- Don't manufacture consent to create the illusion of refinement (e.g., citing surface-level internal leader agreement that you know is actually skepticism).
- Don't discard counterevidence because it conflicts with a side goal (e.g., adopting Erlang at Yahoo! to learn Erlang rather than to solve the actual problem; only 3 of 15 engineers would touch it, but that counterevidence was ignored).

*Ref: Crafting_Engineering_Strategy.md — "What Is Strategy Refinement?" / "Does Refinement Matter?" / "If It Matters, Why Is It Skipped?" / "Building Your Toolkit" / "Antipatterns in Refinement" / "Strategy Testing" / "Systems Modeling" / "Wardley Mapping"*

---

### 7. Set Policy with Four Categories and Two Criteria

**Principle:** Policy is interpreting your diagnosis into a concrete plan. An effective policy solves the *entirety* of the strategy's diagnosis. Policies that can't be applied or enforced won't accomplish anything.

**Do:**
- Follow the six steps to write policy:
  1. Review diagnosis for completeness.
  2. Select policies that address the diagnosis; explicitly match each to one or more diagnoses.
  3. Consolidate overlapping or adjoining policies.
  4. Backtest against recent decisions (a decision log helps).
  5. Mine for conflict, emphasizing feedback from those who disagree.
  6. Refine if uncertain (deploy a refinement technique to increase conviction).
- Choose the right kind of policy for the problem:
  - **Approvals** — define the process for making recurring decisions (who approves, how).
  - **Allocations** — describe how resources are split across investments. *The most concrete statement of organizational priority.*
  - **Direction** — explicit instruction on how a decision *must* be made. Use when you value consistency more than individual judgment.
  - **Guidance** — recommendation about how a decision *should* be made. Use when you can articulate the destination but not mandate the path.
- Match policy kind to role:
  - Developer productivity teams → lean on **guidance** with platform support.
  - Executives → lean on **direction** (often *too* heavily; guidance often works better when you understand the direction but not the path).
  - Product engineering orgs → narrow direction to engineers within that org to handle complex cross-org dynamics.
- Evaluate policies against two core criteria: **applicable** (useful for navigating complex real-world tradeoffs) and **enforced** (teams are held accountable). Plus optional **leverage** for executive contexts.
- Stop yourself from including any policy that, for some reason, **can't be applied or enforced**.
- Remember most "novel" policies are adaptations of well-known approaches to new circumstances. Adapt, don't invent; the most likely place to find truly novel policies is during the **widespread-adoption phase of a new technology** (mobile, cloud, LLMs).

**Don't:**
- Don't propose more than one bundle of competing policies in the core of the strategy document; if multiple bundles are alive, that's a sign of a gap in the diagnosis. Move alternatives to an appendix.
- Don't propose an impractical policy (one you can't fund or enforce); an impractical policy also suggests your diagnosis is missing an important pillar. *Never propose a policy you cannot possibly fund or enforce.*
- Don't demand perfect clarity from peer functions before setting policy. Include the absence in your diagnosis and move forward; *leadership requires taking meaningful risks.*
- Don't add a policy you suspect can't be applied or enforced just because it sounds aspirational.

```
POLICY KIND QUICK REFERENCE:

  Approvals   | who decides + how             | "Escalations come to paired leads"
  Allocations | how resources are split      | "1 FTE on manual, rest on automation"
  Direction   | must be made this way        | "All new code in the monolith"
  Guidance    | should be made this way      | "Minimize changes to tokenization env"
```

*Ref: Crafting_Engineering_Strategy.md — "What Is Policy?" / "How to Set Policy" / "How Many Policies?" / "Kinds of Policies" / "Maintaining Strategy Altitude" / "Criteria for Effective Policies" / "Developing Novel Policies" / "Are Competing Policy Proposals an Antipattern?" / "Recognizing Constraints" / "Dealing with Missing Strategies"*

---

### 8. Operations: The Most-Skipped Step, and the Six-Factor Rubric

**Principle:** Even the best policies fail if teams don't adopt them. Operations is the art of making policies work. *Policies without operations fade quietly into your organization's history.*

**Do:**
- Use the **six-factor rubric** to evaluate any operational mechanism:
  1. **Measurability** — can you measure leading and lagging indicators?
  2. **Adoption cost** — how much work to migrate?
  3. **User ease (or burden)** — does the mechanism make users' work easier or harder?
  4. **Provider ease (or burden)** — how much ongoing maintenance for the providing team?
  5. **Reliance on authority** — what happens if the sponsoring executive departs?
  6. **Cultural alignment** — will the organization fight this at every step?
- Choose mechanisms from these effective patterns:
  - **Approval and advice forums** — for edge cases where policy is unclear; the simplest form is "exceptions are granted by a named individual in writing."
  - **Inspection** — concretely specify *where* and *how* data will be tracked. An inspection that silently fails accomplishes nothing.
  - **Nudges** — *the most effective operational mechanism*: bring information to people exactly when it would be useful. Limit the total count, ensure each nudge has an explicit action, and include clear instructions. Pair with inspection (e.g., Stripe's cloud-cost nudge informed teams whenever spend accelerated).
  - **Automation** — most effective and scalable when paired with good UX (e.g., Uber's structured service-provisioning requests replacing ticket-based back-and-forth).
  - **Deferral to future work** — explicitly defer what you can't currently address; acknowledge what's missing and clarify when you'll return.
  - **Meetings** — universal but expensive. Good starting point, but iterate toward cancellation.
- Document operational plans: review policies, match mechanisms, pool to avoid redundancy, validate with users/providers, and reflect after three months.
- Focus on what you *can* do: as a nonexecutive, add nudges, focus on real dynamics, build real datasets.

**Don't:**
- Don't rely on the antipatterns (each provides some value, but there's almost always a better alternative):
  - Top-down pronouncements ("Return to office" without motivation).
  - Education-as-announcement rollouts (one-time all-company announcements).
  - Mandatory recurring trainings (low attendance, low effort from trainers).
  - "Just change the culture" (simplistic; needs visible leaders + reinforcement mechanisms).
- Don't confuse *binding* mechanisms (CTO-required architecture reviews) with effective ones. Authoritative mechanisms technically shift accountability but often don't change behavior.
- Don't cargo-cult: avoid recreating a process that previously solved a problem without understanding the circumstances that made it effective. *The longer I work in the software industry, the more I am surprised by how few strategists seem to care if their approaches actually work.*

*Ref: Crafting_Engineering_Strategy.md — "What Are Operational Mechanisms?" / "How to Evaluate Mechanisms: A Rubric" / "Composing an Operational Plan" / "Effective Mechanisms and Patterns" / "Antipatterns and Ineffective Mechanisms" / "What If You're Not an Executive?" / "Beware Cargo-Culting"*

---

### 9. Strategy Altitude: Permissive vs. Prescriptive × Team vs. Org

**Principle:** Altitude is how permissive a strategy is and where it's implemented. The formula to increase strategy volume: reduce altitude, increase permissiveness, or both.

**Do:**
- Choose altitude deliberately:

```
|                          | Permissive                                                           | Prescriptive                                                  |
|--------------------------|----------------------------------------------------------------------|---------------------------------------------------------------|
| Organization<br>altitude | CI/CD nudges pull<br>request authors<br>that reduce code<br>coverage | CI/CD blocks pull<br>requests that<br>reduce code<br>coverage |
| Team<br>altitude         | Team runs internal<br>training about<br>security practices           | Team planning<br>process schedules<br>security work first     |
```
- Use altitude to cover more topics at lower cost: at Carta, Larson rolled out broad strategy work by combining permissive strategies + escalation paths, with only one highly prescriptive area (provisioning new services, escalated to CTO).
- Recognize that *looking* effective and *being* effective tend to be only lightly correlated; significantly more leaders fail by attempting too much strategy than too little.

**Don't:**
- Don't try to write many high-altitude prescriptive strategies simultaneously; they'll fail.
- Don't underestimate communication loss at high altitude (e.g., engineering-wide chat channels are at best ineffective).

*Ref: Crafting_Engineering_Strategy.md — "Strategy Altitude" / "Are You Doing Too Much?" / "Maintaining Strategy Altitude" / "How Much Strategy to Write"*

---

### 10. Everyone Can Do Strategy (Engineer, Executive, and In-Between)

**Principle:** Anyone can do strategy from any position. The tools differ by role, the authority differs by role, but the practice is identical.

**Do (as an engineer or non-executive):**
- **Take five, then synthesize**: document five related decisions, then synthesize diagnosis + policy. You're *naming* the implicit strategy, which forces a conversation.
- **Model, document, and share**: (1) Model the approach you want others to adopt. (2) Document the approach, the thinking, and how to adopt it. (3) Share around. Adoption comes from your success.
- Remember that executive strategies are also fundamentally influence-based; the same influence dynamic works without title.

**Do (as an executive):**
- Mandates only matter if there have consequences. Without consequences, your mandate isn't a mandate.
- You can be more visible and have more latitude to mandate, but you are constrained by budgets, CEO visions, peers to satisfy, and a team to motivate. *An executive strategy can be technically shifted to the wider organization but often doesn't change anyone's behavior at all.*

**Do (in challenging environments):**
- **Low-trust environments**: whisper the controversial parts; translate difficult messages into softer, less direct versions.
- **Poor-judgment environments**: write strategy to educate colleagues about the tradeoffs they are making.
- **Missing peer strategies**: accept the ambiguity as a fact, include the absence in your diagnosis, work around it. *Leadership is about finding a way to move forward despite those issues.*
- **Watch for the Karpman Drama Triangle**: persecutor, rescuer, victim. When diagnosis is obvious and others disagree, you might be wrong.
- **When not to do strategy**: when another part of your organization is already working on the same problem, or when you're trying to satisfy an emotional need for immediate impact (strategy is the slow, incremental work of changing beliefs).

*Ref: Crafting_Engineering_Strategy.md — "Doing Strategy as an Engineer" / "Doing Strategy as an Executive" / "Doing Strategy in Other Roles" / "Doing Strategy in Challenging Environments" / "Who Shouldn't Do Strategy?" / "Strategy Archaeology" / "Karpman Drama Triangle"*

---

### 11. When to Write Strategy (and Always Be Working on Exactly One)

**Principle:** Diagnose your current strategic state, decide whether to write, and limit work-in-progress ruthlessly.

**Do:**
- Diagnose your current strategic state (one of three):
  - **Globally consistent** — unlikely that more strategy work helps (unless you're consistently deciding undesirable approaches).
  - **Consistent within teams** — clear strategy within pockets, inconsistency across pockets. Time to write strategy.
  - **Highly varied** — little agreement across individuals. Time to write strategy.
- Watch for trends that push you toward a worse state and warrant strategy work:
  - Rapid hiring (e.g., Uber doubled eng headcount every six months).
  - New external leaders who are playbook-driven and forget to diagnose before sweeping changes.
  - Frequent reorganizations/layoffs (which break the mechanisms propagating culture).
  - Ineffective documentation/communication of historical decisions.
- Assess your **context level** before writing strategy: do you understand the history of the area and the individuals who made past decisions? If not, slow down and build the relationships.
- *Limit WIP at any time*: always be working on exactly one strategy. Start small, iterate until it works, then expand. *Always be working on exactly one strategy. Doing more feels like progress, but usually fails. Doing less is always a missed opportunity.*
- Pair your focused approach with broader, proactive storytelling to stakeholders—incremental work can otherwise look unambitious from outside.
- Ask the debugging question: *Has your prior strategy work affected subsequent decisions?* If not, scale back. Get a single strategy working deeply and only then return.

**Don't:**
- Don't start working on a strategy you don't have context for. Anxiety-and-ego-driven grand migrations are how leaders derail.
- Don't accept "we just need to write nothing" as your perpetual state forever; sometimes the most valuable moment is when the strategy is *missing*.

*Ref: Crafting_Engineering_Strategy.md — "When to Write Strategy" / "Current Strategic State" / "Trends in Strategic State" / "Your Context Level" / "How Much Strategy to Write" / "Always Be Working on Exactly One Strategy" / "Are You Doing Too Much?"*

---

### 12. Strategy Testing: Sponsor + Guide + Weekly Meeting

**Principle:** *Prematurely rolling out a strategy prevents evaluating whether it's effective. Pressure changes behavior in profound ways*—creating the impression of compliance while minimizing actual change. Strategy testing identifies the narrowest, deepest slice of a strategy and iterates until confident the approach works.

**Do:**
- Test before finalizing. Two most important pieces: testing *before* finalizing the strategy, and testing *narrowly* on the underlying mechanics (not on broad adoption/incentive issues).
- Identify the *narrowest, deepest available slice* of your strategy. Iterate until you see evidence it works.
- Use **impact metrics** (not just adoption metrics). Try to avoid proxy metrics—look at the actual thing that matters.
- Operate from the belief that *people mean well*, and that strategy failures are usually due to **excess friction and poor ergonomics**. If people aren't using new tooling, assume the tooling is too complex—*don't* assume they're resistant.
- Define two roles:
  - **Sponsor** — provides organizational authority, makes quick decisions, marshals support, prevents scope creep, sets pace, identifies when to change phases. Must be *genuinely authorized* and available for rapid escalations.
  - **Guide** — translates strategy into particulars, identifies slowdowns, escalates frequently, tracks goals/workstreams, maintains pace. Needs nuanced judgment and resistance to derailment. The *worst* guides are ideological (they reject test results) or easily derailed.
- Run a **weekly meeting** between sponsor, guide, and key folks—*the only absolute requirement for the testing phase*. Heavy on debugging, light on presentation.

**Don't:**
- Don't *broaden* to chase higher-impact-feeling areas when iteration cycles are slower.
- Don't force adoption hard enough to distract from improving the underlying mechanics.
- Don't get attached to your current approach—strategy testing is only valuable because many strategies *don't* work as intended.
- Don't claim you've tested when you haven't; "pressure without a plan" is a strategy that *sounds right* but lacks concrete details. Identify untested strategies with two questions:
  1. *Are there numbers showing the strategy is driving the desired impact?* Look at the actual thing that matters, not a commitment spreadsheet.
  2. *If the numbers aren't moving, is there a clear mechanism for debugging, and is the team actually making progress?* Look for new software running in a meaningful environment, and talk with skeptics (but beware: they're almost always right, but often aren't describing current problems).
- Don't keep a stuck strategy moving: when recognizing a strategy that skipped testing and is struggling, write a new strategy and don't skip testing this time. *Sometimes you can't pause officially—then pause implicitly* (e.g., delay new services for a month to invest in improvements).

*Ref: Crafting_Engineering_Strategy.md — "Strategy Testing for Iterative Refinement" / "When to Test Strategy" / "How to Test Strategy" / "Testing Roles: Sponsors and Guides" / "Meetings and Metrics" / "Identifying Untested Strategies" / "Recovering from Skipped Testing"*

---

### 13. Systems Modeling with Stocks and Flows

**Principle:** Systems modeling uses stocks (things that accumulate) and flows (changes to stocks) to understand complex systems *cheaply and quickly*. Best when you're unsure where leverage points might be, when you have significant data to compare against, or when disagreements are based on unstated intuitions.

**Do:**
- Master the basic concepts: in the load balancer model, *Requests* is a stock; an arrow labeled "OK" or "Error in server" is a flow.
- Follow the modeling process:
  1. Sketch stocks and flows on paper or in a diagramming tool.
  2. Reason about how potential changes shift the flows.
  3. Model in a spreadsheet or specialized tool, starting with the happy path (left-to-right), then exception paths (right-to-left).
  4. Exercise the model with different starting values (sensitivity analysis).
  5. Document what you learned, focusing on *insights first*.
- Pick a tool and practice: SageModeler, Insight Maker, lethain/systems, or spreadsheets. The most important thing is building models quickly; don't overthink tooling.
- For documentation, put *learning* first, then sketch, then reasoning, then model details, then exercise. *Most people don't care how you built the model—they just want the insights.*
- Decouple models from specific strategies; link from strategies to standalone model write-ups only when a reader is surprised by a conclusion.

**Don't:**
- Don't confuse model and reality. *When your model and reality conflict, reality is always right.* (Stripe's reliability model was intuitively good but real-world results were mixed; attachment to the model delayed impactful work.)
- Don't overcommit: *models are immutable, but reality isn't.*
- Don't fall for omitted information; *every model omits information; some omit critical information.* Uber's service migration model captured what my team cared about but did nothing to evaluate whether the migration was a good idea overall.
- Don't let modeling slow you down—practice makes it faster than asking peers for advice.

```
EXAMPLE: lethain/systems syntax for driver onboarding (Larson):

  # 100 folks apply to become drivers per round
  [PotentialDrivers] > AppliedDrivers @ 100
  # 25% of applied drivers become eligible each round
  AppliedDrivers > EligibleDrivers @ Leak(0.25)
  # 10% of folks in Eligible move backward (missing info)
  EligibleDrivers > AppliedDrivers @ Leak(0.1)
  # 25% of eligible drivers onboard each round
  EligibleDrivers > OnboardedDrivers @ Leak(0.25)
  # 50% of onboarded drivers become active
  OnboardedDrivers > ActiveDrivers @ Leak(0.50)
  # 10% of active drivers depart voluntarily and involuntarily
  ActiveDrivers > DepartedDrivers @ Leak(0.10)
  ActiveDrivers > SuspendedDrivers @ Leak(0.10)
  # 5% of DepartedDrivers become active
  DepartedDrivers > ActiveDrivers @ Leak(0.05)
  # 1% of SuspendedDrivers are reactivated
  SuspendedDrivers > ActiveDrivers @ Leak(0.01)

Note: @ Leak(0.25) vs @ 0.25 (@ Conversion):
  Leak(0.25) on 100 applied, 100 eligible:
    => 75 applied, 125 eligible.
  Conversion(0.25):
    => 0 applied, 125 eligible (destroys the unconverted portion).
```

*Ref: Crafting_Engineering_Strategy.md — "Systems Modeling" / "A Two-Minute Primer" / "When Is Systems Modeling Useful?" / "Tooling" / "How to Model" / "Deeper Exploration" / "How to Document a Model" / "What Systems Modeling Isn't"*

---

### 14. Wardley Mapping: Components, Axes, Pipelines, Overlays

**Principle:** Wardley mapping ensures strategy is grounded in situational awareness, particularly at ecosystem-level scope and over multi-year horizons. Created by Simon Wardley in 2005.

**Do:**
- Read a Wardley map by understanding its three components and two axes:
  - **Components**: users (top), needs (connected to users), capabilities (connected to needs; cannot connect directly to users).
  - **X-axis**: commoditization stages — **genesis** → **custom** → **product** → **commodity**.
  - **Y-axis**: visibility to the user (top = highly visible; bottom = invisible).
- Use extras for clarity:
  - **Pipelines** — boxes describing expected evolution over time (e.g., typical editing → AI-assisted creation → AI-led creation).
  - **Overlays** — group boxes by team/owner or any interesting denominator.
  - **Arrows** for predicted future changes.
- Follow the mapping process:
  1. Commit to starting small and iterating.
  2. List users, needs, capabilities.
  3. Establish value chains connecting them.
  4. Plot on a Wardley map.
  5. Study the current state.
  6. Predict how the map will evolve.
  7. Study the future state.
  8. Share the map for feedback.
  9. Document what you learned.
- For reading: use the **three-section reading-optimized format**:
  - *How things work today* (current map + interesting placements).
  - *Transition to future state* (second map, perhaps several for different scenarios).
  - *Users and value chains* (often brief; the map implicitly explains most of it).
- Use maps when: highly dynamic environments, strategies spanning 5+ years, or any strategy built on an evolving foundation (the in-the-moment perspective is almost always too stable).
- Pick a tool and start: pen and paper, Mapkeep, Miro, Figma, or OmniGraffle. *Tools for Wardley mapping aren't the obstacle they are for systems modeling.*

**Don't:**
- Don't expect Wardley mapping to help with detail-level optimization—it's less helpful for issues like looping to optimize your onboarding funnel.
- Don't forget doctrine (universally applicable practices like knowing your users) and gameplay (context-dependent moves like talent raiding or bundling); Larson notes these are *lightly specialized* for business strategy and less directly applicable to engineering, so he focuses primarily on the map technique.

```
WARDLEY MAP EXAMPLE (knowledge-base management):

  Visibility ^
             |
   [Reader]-->[Discover content]---[Search Index]    [custom→product]
   [Reader]-->[Read content]-------------------------[Commodity]
   [Author]-->[Create / edit content]-------[Doc editing]    [custom→product]
   [Author]-->[Feedback]--------------------[User feedback process]
             +------------------------------------------------>
                                                  Commoditization  →
              genesis     custom      product     commodity
```

*Ref: Crafting_Engineering_Strategy.md — "Wardley Maps" / "Wardley Mapping: A 10-Minute Primer" / "X-axis" / "Y-axis" / "Tools for Wardley Mapping" / "When Are Wardley Maps Useful?" / "How to Wardley Map" / "How to Document a Wardley Map" / "What About Doctrines and Gameplay?"*

---

### 15. Write for Readers, Not Writers (Invert the Document Structure)

**Principle:** The order for *writing* a strategy (explore → diagnose → refine → set policy → operate) is a poor order for *reading*. Most strategy readers just want to understand the policy so they can apply it. *The vast majority just want to understand how it will impact them or their function. These are your least motivated readers.*

**Do:**
- Invert the structure for readers:
  ```
  1. POLICY      – What does the strategy require or allow?
  2. OPERATION   – How is it enforced? How are exceptions granted?
  3. REFINE      – What load-bearing details informed the strategy?
  4. DIAGNOSE    – What general trends and observations steered thinking?
  5. EXPLORE     – What is the high-level, wide-ranging context?
  ```
- **Refactor further** when useful. The LLM adoption strategy merges Refine into Diagnose and discards a separate Operation section, folding operational details alongside their policies.
- Find an uninvolved reader before release; ask them to point out anything difficult to understand.
- Roll out with **explicit commenting period + office hours**; disable in-document commenting after release to move discussion to a better forum.
- Maintain your own strategy template with consistent metadata (creation date, approval status, durable question channel). The most important metadata is *where to ask questions*.

**Don't:**
- Don't keep writer-oriented structure for reader-oriented documents. Most strategy writers resist restructuring, but the cost of skipping it is that your least-motivated readers never find the policy.
- Don't ship reader-oriented docs that omit the *rationale*. Without diagnosis and exploration, new hires dismiss policies as "the previous engineers were just dumb." Use *transient alignment* prevention.
- Don't use a template without owning it; the secret to a good template is *someone cares about the template's user* first, not about the various constituencies that want to insert requirements.

*Ref: Crafting_Engineering_Strategy.md — "Why Writing Structure Inhibits Reading" / "Inverting the Document Structure for Reading" / "Strategy Refactoring" / "Additional Tips for Writing Effective Strategy Documents"*

---

### 16. Bridging Theory and Practice: Timelines, Chaos, Bad Strategy

**Principle:** The clean strategy documents in the book emerged from messy processes. Strategy documents often *look* pristine because they're trying to communicate clearly about a complex topic—but praxis is messier.

**Do:**
- **Despite unrealistic timelines**: deliver the best draft you can, then view yourself as *starting* the refinement process. Many strategies never leave refinement and are tweaked throughout their lifespans.
- **As a nonexecutive**: *effective diagnosis trumps authority.* At least as many executive strategies are ravaged by reality's details as are overridden by higher-altitude strategies.
- **In chaotic environments**: strategies don't require stable environments—they require awareness of the environment. In a dynamic period, the strategy authors might know they can only *protect capacity in two-week chunks*.
- **With unreliable information**: rather than blocking on missing information, your strategy should acknowledge what's missing and *move forward where you can*. Sometimes that means taking risks; sometimes delaying for clarity; it never means being stuck without options beyond pointing a finger.
- **Surviving other people's bad strategy**: write a *private strategy* of your own that acknowledges the imposed policy in its diagnosis as a static, unavoidable truth, then make practical decisions within that context. Generally don't share unless a colleague asks.

*Ref: Crafting_Engineering_Strategy.md — "Clear, Definitive Documents" / "Doing Strategy Despite Unrealistic Timelines" / "Using Strategy as a Nonexecutive" / "Doing Strategy in Chaotic Environments" / "Unreliable Information" / "Surviving Other People's Bad Strategy Work"*

---

### 17. Case Study: Service Migration Strategy (Uber, 2014)

**Context:** Four engineers on a team of ~2,000 engineers; org doubling every six months; team could not get more headcount. Strategy leader: Larson (then Eng Manager).

**Policy excerpt:**

```
*Constrain manual provisioning allocation to maximize investment in
self-service provisioning.* The service provisioning team will maintain
a fixed allocation of one full-time engineer on manual service-
provisioning tasks. We will move the remaining engineers to work on
automation to speed up future service provisioning. This will degrade
manual provisioning in the short term, but the alternative is
permanently degrading provisioning by the influx of new service requests
from newly hired product engineers.

*Self-service must be safely usable by a new hire without Uber context.*

*Move to structured requests, and out of tickets.* Missing or
incorrect information in provisioning requests create significant
delays in provisioning. ...we can get paid twice by reducing errors
in manual provisioning while also creating the interface for self-
service workflows.

*Prefer initializing new services with good defaults rather than
requiring user input.* Most new services are provisioned for new
projects with strong timeline pressure but little certainty on their
long-term requirements. These users cannot accurately predict their
future needs, and expecting them to do so creates significant friction.
```

**Sequenced tasks (excerpt):**
1. Internal tool that coordinates service provisioning, replacing Phabricator tickets, with a schema of required fields.
2. Same tool serves as the interface for automating future provisioning steps.
3. Extend the tool to generate Puppet scaffolding for new services.
4. Port allocation: move the port registry to a database, automate.
5. Replace manual server assignment with an automated system.

**Refine (systems modeling) learnings:**
- We're increasingly falling behind.
- Hiring onto the service provisioning team is *not* a viable solution (even +500% capacity doesn't clear the backlog).
- Moving to a self-service approach is *the only* option.

**Diagnose (excerpt):** "Within infrastructure engineering, there is a team of four engineers responsible for service provisioning today. While our organization is growing at a similar rate as product engineering, none of that additional headcount is being allocated directly to the team working on service provisioning. We do not anticipate this changing."

**Explore:** Reading Borg ("Large-Scale Cluster Management at Google with Borg") and Mesos/Aurora ("Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center"). Wardley map of service orchestration in 2014 (pre-Kubernetes dominance).

**Rubric evaluation (Chapter 23):**
- Speed: 3 (daily iteration behind structured requests interface).
- Cost: 2 (mostly single-team; service migration needs flexible cross-team coordination).
- Impact: 2 (solves the most pressing subset; defers the harder portion).
- **Total: 7/9** — high-quality strategy (Phase 1).
- **Phase 2 (operating the sprawling services)** scores only 4/9 — strategy degrades across phases.

**Verbatim systems model (lethain/systems):**

```
HiringRate(10)
ProductEngineers(1000)
[PotentialHires] > ProductEngineers @ HiringRate
[PotentialServices] > RequestedServices(10) @ ProductEngineers / 10
RequestedServices > InflightServices(0, 10) @ Leak(1.0)
InflightServices > PortNameAssigned @ Leak(1.0)
PortNameAssigned > PuppetGenerated @ Leak(0.8)
PortNameAssigned > RequestedServices @ Leak(0.2)
PuppetGenerated > PuppetConfigMerged @ Leak(0.8)
PuppetGenerated > InflightServices @ Leak(0.2)
PuppetConfigMerged > ServerCapacityAllocated @ Leak(0.8)
PuppetConfigMerged > PuppetGenerated @ Leak(0.2)
```

```
WHAT "STRATEGY ARCHAEOLOGY" LEARNED:
- Hiring of product engineers drives up service-provisioning requests,
  but no counterbalancing infra hiring. Implicit deadline to scale
  this independently of the size of infra team.
- Error rates will influence results a great deal—particularly
  "Missing/incorrect information" errors, the most valuable place
  to start looking for efficiency improvements.
- Missing-information errors are more expensive than the model implies
  (cross-team coordination); Puppet testing errors are probably cheaper
  (single-team iteration loop).
```

*Ref: Crafting_Engineering_Strategy.md — "Chapter 16: Service Migration Strategy" / "Document 16-1: Service Migration Strategy: Uber" / "Document 16-2: Service Onboarding Model" / "Document 16-3: Wardley Mapping the Service Orchestration Ecosystem" / "Is This Strategy Any Good?"*

---

### 18. Case Study: LLM Adoption Strategy (Theoretical Ride Sharing)

**Context:** 2,000 employees, 300 engineers, raised $400M, $50M ARR, 200 cities in NA/EU. A ride-sharing business reinventing public transit with larger vehicles.

**Policy (excerpt):**

```
*Develop an LLM-backed process for reactivating departed and suspended
drivers in mature markets.* Through modeling our driver lifecycle, we
determined that improving onboarding time will have little impact on
the total number of active drivers. Instead, we are focusing on
mechanisms to reactivate departed and suspended drivers, which is the
only opportunity to meaningfully impact active drivers.

*Start with Anthropic.* We use Anthropic models, which are available
through our existing cloud provider via AWS Bedrock. ... Exceptions
will be reviewed by the Machine Learning Review in #ml-review.

*Developer Experience team (DX) must offer at least one LLM-backed
developer productivity tool.* This tool should enhance the experience,
speed, or quality of writing software in TypeScript... Adopt one tool
is the required baseline.

*Internal Tools team (INT) must offer at least one LLM-backed ad hoc
prompting tool.* This tool should support arbitrary nonengineering use
cases for LLMs, such as text extraction, rewriting notes, etc.

*Refresh policy in six months.* Our primary goal is to quickly learn
about this unfamiliar domain where we have limited internal expertise,
then review whether we should increase our investment afterward.
```

**Diagnose (key points):**
- Three distinct needs: productivity for non-engineers, productivity for engineers, product extensions.
- Product extensions are *strategic differentiation*; the other two are workflow optimizations.
- Reactivating departed/suspended drivers is the *largest lever* to increasing active drivers.
- Faster driver onboarding will *not* increase active drivers but may reduce operating costs.
- Limited in-house expertise; switching costs across foundational models are *both economically and integration-wise low*; future evolution is unclear.

**Systems model learnings (LLM impact on DX):**
- *Insight #1*: LLMs may cause us to spend *more* time writing/testing code, but *less* time fixing issues discovered after going to production.
- *Insight #2*: If production-error rate is a function of shipped volume, shipping faster doesn't increase velocity. The only meaningful lever is reducing production-error rate.
- *Insight #3*: Don't focus on the "Testing found error" flow (which should increase) — focus on the "Error found in production" flow.

**Driver onboarding systems model:**
- Even doubling the rate that qualified applicant drivers become eligible has *little* impact on active drivers over time.
- Efforts to reengage *departed* drivers have significant impact.
- Surprisingly, increasing the reactivation rate of *suspended* drivers is more impactful than reactivating departed drivers (because the suspended pool grows without both reactivating at healthy rates).
- *Counterintuitive result*: increasing both rates is more impactful than either alone; otherwise you keep an in-growing backlog.

**Cost-of-training facts:**
- LLaMa 1 ~ $3M, LLaMa 2 ~ $20–30M.
- OpenAI GPT-4 allegedly ~ $100M.
- Anthropic: $0.25–$15 per million tokens (input); OpenAI: $0.50–$60.
- Average English word ≈ 1.3 tokens.

*Ref: Crafting_Engineering_Strategy.md — "Chapter 17: LLM Adoption Strategy" / "Document 17-1: How Should We Adopt Large Language Models?" / "Document 17-2: Modeling LLMs' Impact on the Developer Experience" / "Document 17-3: Wardley Mapping the LLM Ecosystem" / "Document 17-4: Modeling Driver Onboarding"*

---

### 19. Case Study: Private Equity Ownership Strategy (Fungible Ecommerce Co.)

**Context:** PE-owned ecommerce platform; expect cost reduction pressures; unclear reduction scale.

**Policy (excerpt):**

```
*We aim to accomplish that reduction through a series of policies and
one-off infrastructure projects, without requiring a major reduction
in headcount spend.*

*We will move to an "N-1" backfill policy*, where departures are
backfilled with a less senior level. We will also institute a strict
maximum of one Principal Engineer per business unit, with any
exceptions approved in writing by the CTO—this applies for both
promotions and external hires.

We commit to this policy of reducing headcount costs by approximately
5% YoY every year for the foreseeable future.

*We are not changing our geographical hiring strategy at this time.*

*We will continue our current infrastructure efficiency strategy.* ...
We commit to growing infrastructure spend at no more than 5% YoY,
significantly lower than our projected revenue increase of 25% YoY.

*We will prioritize the post-acquisition integration work next quarter*
...We commit to a one-time reduction in infrastructure of 3% YoY.

*We will kick off a working group to identify the features with the
highest support load.*
```

**Diagnose (excerpt):** "Our Engineering headcount costs have grown by 15% YoY this year, and 18% YoY the prior year. Headcount grew 7% and 9% respectively, with the difference between headcount and headcount costs explained by salary band adjustments (4%), a focus on hiring senior roles (3%), and increased hiring in higher cost geographic regions (1%)."

**Seniority-mix model: three policy scenarios.**
- Backfill-at-level → organization becomes *increasingly top-heavy* with senior engineers over time.
- Backfill at N-1 (without cap) → turns exponential growth into linear but still too expensive.
- Backfill at N-1 + capped senior level (1 Principal per BU) → ratio of senior to other levels looks healthy.

**Verbatim systems model — Base:**

```
HiringRate(2)
[Candidates] > SWE1(10) @ HiringRate
SWE1 > DepartedSWE1 @ Leak(0.1)
DepartedSWE1 > SWE1 @ Leak(0.5)
[Candidates] > SWE2(10) @ HiringRate
SWE1 > SWE2 @ Leak(0.1)
SWE2 > DepartedSWE2 @ Leak(0.1)
DepartedSWE2 > SWE2 @ Leak(0.5)
[Candidates] > SWE3(10) @ HiringRate
SWE2 > SWE3 @ Leak(0.1)
SWE3 > DepartedSWE3 @ Leak(0.1)
DepartedSWE3 > SWE3 @ Leak(0.5)
[Candidates] > SWE4(0) @ HiringRate
SWE3 > SWE4 @ Leak(0.1)
SWE4 > DepartedSWE4 @ Leak(0.1)
DepartedSWE4 > SWE4 @ Leak(0.5)
```

**Verbatim systems model — N-1 backfill (key change):**

```
# Original (replace)
DepartedSWE2 > SWE2 @ Leak(0.5)
# N-1 (with this)
DepartedSWE2 > SWE1 @ Leak(0.5)
# SWE1s backfilled at SWE1 (no level below)
```

**Verbatim systems model — Cap senior level:**

```
SWE4(10, 20)
[Candidates] > SWE4 @ HiringRate
```

**Reasoning insights from the model:**
- If promotion rates at any level exceed the rate of hiring + N-1 backfill at that level, that level's proportion will grow over time.
- A company that does little hiring and has high retention cannot promote frequently.
- The "career level" policy is likely a *financial constraint* in disguise.

*Ref: Crafting_Engineering_Strategy.md — "Chapter 18: Private Equity Ownership Strategy" / "Document 18-1: Navigating Private Equity Ownership" / "Document 18-2: Engineering Organization Seniority-Mix Model"*

---

### 20. Case Study: Customer Data Access Strategy (IPO-Readiness)

**Context:** IPO-bound company with failed prior security initiatives; controls degraded UX and were subverted over time.

**Policy (excerpt):**

```
*Controls for accessing user data must be significantly stronger prior
to our IPO.* ... Our Security team is accountable for the exact
mechanisms and approach to addressing this risk.

*We will continue to prioritize a hybrid solution to resource-access
controls.*

*Directly expose the log of our resource-level accesses to our users.*

Good security discussions don't frame decisions as a compromise between
security and usability. We will pursue multi-dimensional tradeoffs to
simultaneously improve security and efficiency. Whenever we frame a
discussion as trading off between security and utility, it's a sign
that we are having the wrong discussion, and that we should rethink our
approach.

*Measure progress on percentage of customer data access requests
justified by a user-comprehensible, automated rationale.* This will
anchor our approach on simultaneously improving the security of user
data and the usability of our colleagues' internal tools.

*Expire unused roles to move toward the principle of least privilege.*
...we will automatically remove roles from colleagues after 90 days of
not using the role's permissions.

*Weekly reviews until we see progress; monthly access reviews in
perpetuity.* ... This is explicitly a forum for ongoing strategy
testing, with the CISO serving as the meeting's sponsor, and the
Principal Security Engineer serving as the meeting's guide.

*Exceptions must be granted in writing by the CISO.*
```

**Three patterns of resource-level access control (Explore):**
1. **Third-party enrichment** (e.g., Zendesk-driven; tight coupling with platform vendor).
2. **First-party tool implementation** (manage everything in your product).
3. **Hybrid solutions** (third-party for most actions + permits resource-level access in first-party system).

**Insight (from Chapter 23 commentary):** Security and efficiency are *not* a tradeoff—they are a multi-dimensional optimization. The framing itself is a sign you're having the wrong discussion.

*Ref: Crafting_Engineering_Strategy.md — "Chapter 19: Customer Data Access Strategy" / "Document 19-1: How Should We Control Access to User Data?"*

---

### 21. Case Study: Service Architecture Strategy (Should We Decompose Our Monolith?)

**Context:** Theoretical Compliance Company (B2B compliance, 2,000 people, 500 eng, 150 infra); spinning up new business units; pressure to reduce platform spend; Ruby monolith.

**Policy (excerpt):**

```
*Business units should always operate in their own code repository and
monolith.* They should not provision many different services. They
should rarely work in other business units' monoliths.

*New integrations across business unit monoliths should be done using
gRPC.* The emphasis here is on *new* integrations; it's desirable but
not urgent to migrate existing integrations.

*Except for new business unit monoliths, we don't allow new services.*
... Provisioning a new service, unless it corresponds with a new
business unit, always requires approval from the CTO in #eng-strategy.

*Merge existing services into business unit monoliths where you can.*
We believe that each choice to move existing services back into a
monolith should be made "in the details" rather than from a top-down
strategy perspective.
```

**Diagnose (business constraints, abbreviated):**
- Revenue growth 10–20% YoY; board expects 5–10% free cash flow improvement or 5–10% additional growth.
- Spinning up new business units with budget pulled from core business or platform teams.
- Methodology allocates platform costs proportional to revenue, so *core business is accountable for majority of platform costs* even if new business lines motivate them.

**Diagnose (engineering constraints, abbreviated):**
- Infra will not grow significantly.
- Each new business unit is led by a general manager; CTO/CPO set practice standards, but BU GM often has last word.
- *It's more overhead for infra to support more services.* *It's even more overhead to have irresponsible business units breaking a shared monolithic service.*
- Compliance/security requirements on payments service have *significantly higher blast radius*.
- Ruby generally relies on blocking IO; service architectures spend more time on blocking IO than monoliths.

**Insight:** Strategy is essentially a *reversal* of the prior monolith-decomposition trend. *The same general strokes can be ported across companies; the details would have been quite different in every case. Copying the general strokes worked quite well.*

*Ref: Crafting_Engineering_Strategy.md — "Chapter 20: Service Architecture Strategy" / "Document 20-1: Should We Decompose Our Monolith?"*

---

### 22. Case Study: Calm — "We Are a Product Engineering Company!"

**Context:** Calm's engineering team was scattered between infrastructure ambitions, technology experimentation, and a stuck service decomposition. Larson's *first* executive strategy work.

**Policy:**

```
*We are a product engineering company.* Users write in every day to
tell us that our product has changed their lives for the better. Our
technical infrastructure doesn't get many user letters—and this is
unlikely to change going forward as our infrastructure is relatively
low-scale and low-complexity.

*We exclusively adopt new technologies to create valuable product
capabilities.* We believe our technology stack as it exists today can
solve the majority of our current and future product roadmaps.

*We write all code in the monolith.* ... This is no longer ambiguous:
all new code must be written in the monolith.

*Exceptions are granted by the CTO, and must be in writing.* ...
All exceptions must be written. If they are not written, then you
should operate as if it has not been granted.

Proving the point about exceptions, there are two confirmed exceptions:
1. We are incrementally migrating to TypeScript.
2. We are evaluating Postgres Aurora as our primary database.
```

**Diagnose highlights:**
- *Product not limited by missing infrastructure*; nothing in current/next year constrained by tech infra.
- *Uptime, stability, latency are OK but not great.*
- *Infrastructure team split between supporting monolith and service workflows.*
- *Product and executive stakeholders experience us as competing factions.*
- *Outsized time debating technology adoptions and rewrites.*
- *Spending more time on infrastructure and platform work than product work.*

**Result:** "This strategy eliminated the cause of ongoing friction … It also caused several engineers to leave the company, because experimenting with new technologies was more important to them than making progress on Calm's product. A clear, documented strategy made it clear to everyone involved what sort of game we were playing."

*Ref: Crafting_Engineering_Strategy.md — "Chapter 21: Product Engineering Strategy" / "Document 21-1: 'We're a Product Engineering Company!': Engineering Strategy at Calm"*

---

### 23. Case Study: Resourcing Engineering-Driven Projects at Calm

**Context:** Calm product engineers saturated by incoming requests; no bandwidth for engineering-driven improvements; infrastructure team *can* prioritize but lacks product-development experience.

**Policy:**

```
We will protect one Engineering-driven project per product engineering
team, per quarter. These projects should represent a maximum of 20% of
the team's bandwidth. Each project must advance a measurable metric,
and execution must be designed to show progress on that metric within
four weeks.

These projects must adhere to Calm's existing Engineering strategies.

We resource these projects first in the team's planning, rather than
last. However, only concrete projects are resourced. If there are no
concrete proposals, then the team won't have time budgeted for
Engineering-driven work.

The team's engineering manager is responsible for deciding on the
project, ensuring the project is valuable, and pushing back on
attempts to defund the project.

Project selection does not require CTO approval, but you should
escalate to the CTO if there's friction or disagreement.
```

**Two concrete examples:** code-free media release (eliminate high-urgency pull requests with low judgment) and machine learning content placement (improve engagement by surfacing best content).

**Insight:** *Match strategy altitude to your reality*. Executives' altitudes don't always work because executives may override out-of-band instructions. Resourcing had to be managed by the *team* directly (paired Eng Mgr + PM).

*Ref: Crafting_Engineering_Strategy.md — "Document 21-2: How to Resource Engineering-Driven Projects at Calm"*

---

### 24. Case Study: Stripe — API Deprecation, Sorbet, and Index Acquisition

**Context:** Three Stripe strategies that demonstrate *enduring*, detail-oriented, first-principles thinking over a decade.

**(a) API deprecation policy (Document 22-1, summary):**
- *Design for long API lifetime.* Migrate to your own API before release; identify early adopters.
- *All new and modified APIs must be approved by API Review.*
- *We never deprecate APIs without an unavoidable requirement to do so.* Even if expensive to maintain, we incur the support cost. *Define API deprecation as any change that would require customers to modify an existing integration.* Exception requires API Review + CEO sign-off. (TLS 1.2 → 1.3 was an example.)
- *When significant new functionality is required, we add a new API.*
- *We manage implied technical debt via an API translation layer* (one implementation internally; version transformations above).
- *In the future, SDKs may allow us to soften this policy.*

**Verbatim diagnosis excerpt:** "If you are a small startup composed of mostly engineers, integrating a new payments API seems easy. However, for a small business without dedicated engineers—or a larger enterprise involving numerous stakeholders—handling external API changes can be particularly challenging."

**API deprecation systems model (key result):**
- *Eliminating API-deprecation churn alone won't significantly increase integrated customers.*
- *We can't fully benefit from reducing baseline churn without simultaneously reducing API deprecations.*
- *Biggest takeaway: meaning fully increasing integrated customers requires lowering both types of churn in tandem.*

**(b) Sorbet strategy (Document 22-3, summary):**
- Choose Ruby-with-static-typing over migrating to Java/Golang for product codebase.
- Dedicated ~10-engineer Product Infrastructure team absorbs the cost; product engineers stay focused.
- Six-month priorities refreshed every half after developer productivity survey.
- Selective test execution + test failure instrumentation as supporting priorities.
- *Take on both, despite fixed size*: hybrid approach of deep-dives for complex portions and AST-rewrite scripts for less complex portions.
- Advocated CQRS to provide high-leverage interfaces for incremental typing.

**Diagnose (key facts):** 1,000 people, 400 software engineers; ~70% YoY growth target. Test coverage > 99%. *Tests are slow to run locally; an increasing number of developers run overly narrow subsets, or skip tests until pushing changes*—losing focus during the 20–30 minute merge/build/test cycle. *Long-tenured Stripe engineers find themselves highly productive; newly hired engineers with long tenures at other companies find themselves unproductive.*

**(c) Index acquisition integration (Document 22-4, summary):**
- *Meet at least weekly until the initial release is complete.* Owned jointly by Stripe's Head of Traffic Engineering and Index's Head of Engineering.
- *Minimize changes to tokenization environment.*
- *All other functionality must exist in standard environments.*
- *Defer making a decision regarding the introduction of Java to a later date.*
- *Escalations come to paired leads.*
- *Security review of changes impacting tokenization environment.* We must not cut corners on security.

*Ref: Crafting_Engineering_Strategy.md — "Chapter 22: Developer, API, and Acquisition Strategy at Stripe" / "Document 22-1: How Should Stripe Deprecate APIs?" / "Document 22-2: A Systems Model of API Deprecation" / "Document 22-3: Why Did Stripe Build Sorbet?" / "Document 22-4: How to Integrate Stripe's Acquisition of Index?"*

---

### 25. Speed × Cost × Impact: The Strategy Evaluation Rubric

**Principle:** Strategy is a living endeavor; a strategy that improves quickly is better than a perfect-but-static one. The rubric is intentionally lightweight and dimensioned so it can apply per phase.

**Do:**
- Score every strategy 0–3 on three dimensions:
  - **Speed** — how quickly can the strategy be refined? 3 = daily/weekly iteration; 2 = monthly; 1 = quarterly; 0 = longer.
  - **Cost** — how expensive is refinement (especially cross-team impact)? 3 = single team; 2 = small cross-team deps with flexible timing; 1 = large cross-team with flexible timing; 0 = large cross-team with rigid timing.
  - **Impact** — how well does this iteration solve the diagnosis? 3 = full problem; 2 = the most essential portion; 1 = a simple portion; 0 = nothing.
- Add the three scores; ≥ 6 means high-quality strategy that warrants pursuit; < 6 means strong introspection needed.

**Recognize strategy phases:**
- Uber's service migration: Phase 1 = 7 (provisioning bottleneck); Phase 2 = 4 (sprawling service architecture). High in one phase doesn't mean *the strategy* is good—it means *one phase of the strategy* is good.
- **Stopping a strategy is often a good sign.** All strategies compete with strategies at other altitudes; giving up on high-altitude strategies is *almost* always the right call unless there's a proven, highly impactful reason to maintain them.
- **External evaluation is impossible.** *The missing context is an impenetrable veil* — phases, costs, true operational mechanisms, and blog posts versus reality are all unknowable.
- **Learn from failed strategies** as much as from successful ones. Apply the rubric per phase to determine where things went wrong.

**Don't:**
- Don't grade strategy *only* on outputs (Google's services ≠ a default for you).
- Don't grade strategy *only* on inputs (Caution: an LLM strategy rooted in great diagnosis and effective policies can still be wrong if revenue suffers).
- Don't confuse lack of stub test (Phase 1 testing) with a working Phase 2 rollout.

```
RUBRIC TEMPLATE:

  Strategy: ______________________________________
  Phase:    ______________________________________

  Speed (0–3): ___  (3 daily/weekly, 2 monthly, 1 quarterly, 0 longer)
  Cost  (0–3): ___  (3 single team, 2 small flex cross-team,
                      1 large flex cross-team, 0 large rigid cross-team)
  Impact (0–3): ___  (3 full problem, 2 essential portion,
                      1 simple portion, 0 nothing)

  TOTAL: ___/9
  Decision: pursue if ≥ 6; introspect otherwise.
```

*Ref: Crafting_Engineering_Strategy.md — "How Are Strategies Evaluated Across the Industry?" / "A Rubric for Evaluating Strategy" / "Does Stopping a Strategy Mean It's a Bad Strategy?" / "The Unpierceable Veil" / "Learning from Failed Strategies"*

---

### 26. How to Get Better at Strategy (and Five Deep Dives)

**Principle:** Strategy is a long-term practice; build a personal repository, find sources, debug your work, and operate your own improvement.

**Do (exploration):**
- Search **public resources** (engineering blogs, books, articles); read between the lines—everyone has an agenda.
- Use **private resources** via your professional network—most companies' strategies are available by asking. Read job postings for surprising signal.
- Form or join a **learning circle** for ongoing, bidirectional, trusted sharing. *Many people get stuck on how they can get invited to an existing learning circle, but that's almost always the wrong question. If you want to join a learning circle, make one.*

**Do (diagnosis of your own work):**
- Apply the rubric to each strategy you've collected; split each into phases.
- Ask questions like: How long to discover the initial phase could be improved? Why was the strategy replaced? Did it fail in exploration, diagnosis, policy, or operations? Did it outlive the tenure of its author? Would you repeat it?

**Do (policy for improving):**
- If existing strategies are broken, debug one. (Lower altitude until you can act.)
- If no strategies are documented, document one.
- If strategies have low adoption, iterate on operational mechanisms.
- If strategies are effective, find a new problem to work on.
- If you can't share internally, practice with trusted external peers.

**Do (operations for your improvement):**
- Track the strategies you've implemented, refined, documented, or read (document, spreadsheet, or folder).
- Review your tracked strategies every quarter (ideally in community with a peer or learning circle).
- If you're not making progress, sit with someone more experienced and debug what's wrong *before* the next review.
- Set personal goals and track them (Larson cites his annual "year in review" practice).

**The "five deep dives" pattern:**
- Treat every strategy you encounter as a deep-dive opportunity: *explore* (who else has done this?), *diagnose* (what's their actual problem?), *refine* (what's their leverage?), *set policy* (what would you do differently?), *operate* (what mechanism would you use?). Apply the rubric per phase.

**Don't:**
- Don't believe the hype that "you're not allowed to do strategy"; lower your altitude. *Only you can forbid yourself from developing personal strategies.*
- Don't accept "too busy" if you haven't tracked strategy creation at all; start there.

*Ref: Crafting_Engineering_Strategy.md — "Exploring Strategy Creation" / "Diagnosing Your Prior and Current Strategy Work" / "Policy for Improving at Strategy" / "Operating Your Strategy Improvement Policies" / "What If You're Not Allowed to Do Strategy?" / "Too Busy for Strategy"*

---

### 27. First-Principles Thinking, Intellectual AND Mechanical

**Principle:** Effective strategy is at least as dependent on the **mechanical nuances of reality** as it is on intellectual frameworks. Strategies commonly fail because executives assume strategies will roll themselves out, or because teams skip validating the details.

**Do:**
- Treat strategy as both iterative and intellectual and mechanical.
- Recognize that entropy is natural; good strategy *embraces* change rather than fighting it.
- Apply **first-principles** thinking by grounding strategy in your organization's actual diagnosis, not in patterns cribbed from prior employers.
- Run strategies like building a building: *you go fast by making most of your mistakes where it's cheapest* (in refinement, in modeling, in testing) and fewer where they're difficult (after product commitment).

**Don't:**
- Don't trust candidates who describe strategy as a personal strength while drawing a sharp distinction between directing how work should be done and being in the weeds. *Strategy as a fundamentally intellectual endeavor about how things ought to work* is a flag for underestimating mechanical reality.
- Don't assume the most obvious strategic failure mode is complex decision-making; the most common is *mundane execution errors* (assuming roll-out, skipping validation).

*Ref: Crafting_Engineering_Strategy.md — "This Book's Ambition" / "Iterative, Intellectual, and Mechanical" / "Adapting Rumelt for Engineering" / Strategy archetype description*

---

### 28. The Five-Step Process at a Glance (Driving Decisions Through Iteration)

**Principle:** Each step is an input that flows into the next. *Strategies fail more often due to avoidable errors than to fundamentally unsound thinking. Busy people skip steps—especially steps they dislike or have failed at before.*

**Do:**
- **Step 1 — Explore.** Continue until you know how three similar internal teams and three similar external companies have recently solved the same problem. Time-box (less than a few hours is suspicious; more than a week is questionable). Don't pass judgment yet.
- **Step 2 — Diagnose.** Braindump, summarize exploration, mine for distinct perspectives, synthesize (one author accountable), test drafts across perspectives. *If no one involved has changed their mind, you're not done exploring.*
- **Step 3 — Refine.** Apply strategy testing / systems modeling / Wardley mapping to test raw ideas against reality. *This is the highest-impact step.*
- **Step 4 — Set Policy.** Six steps: review diagnosis → match policies to diagnoses → consolidate → backtest → mine for conflict → refine if uncertain.
- **Step 5 — Operate.** Compose an operational plan (mechanisms across measurability, adoption cost, user/provider ease, reliance on authority, cultural alignment). Inspect and iterate.

**Don't:**
- Don't treat the structure as sacrosanct. Discard every element that gets in your way, *as long as you can explain what that element was intended to accomplish.*

*Ref: Crafting_Engineering_Strategy.md — "Step 1: Exploring" through "Step 5: Operations" / "How the Steps Become Strategy" / "Is the Structure Sacrosanct?"*

---

### 29. Strategy Altitude: When Lower Beats Higher

**Principle:** Permissive strategies are less expensive than prescriptive ones. Lower-altitude strategies are less expensive than higher-altitude ones. *The formula to increase strategy volume is to either reduce altitude, increase permissiveness, or both.*

**Do:**
- Use team-altitude strategies when possible. They have local mechanisms for rollout and maintenance.
- Cover a broad range of topics at high altitude by combining permissive strategies + escalation paths (Carta's Navigators pattern).
- Recognize that mechanisms for wider communication are often **oversaturated and lossy**: communicating in engineering-wide chat channels is, at best, ineffective.
- Maintain explicit altitude when setting policy. Two opposing examples:
  - **Stripe's Sorbet** (org altitude): centralize investment by taking away individual teams' freedom to select preferred tech stacks.
  - **Calm's resourcing Engineering-driven projects** (team altitude): empower only teams to manage the contents of their roadmap because executives are routinely overridden by other executives' out-of-band instructions.

**Don't:**
- Don't try to scale high-altitude prescriptive strategy broadly; it's both expensive and brittle.
- Don't confuse louder communication with deeper adoption.

*Ref: Crafting_Engineering_Strategy.md — "Strategy Altitude" / "Are You Doing Too Much?" / "Maintaining Strategy Altitude"*

---

### 30. Quality, Velocity, Reliability as Strategy Dimensions

**Principle:** Quality, velocity, and reliability are routinely framed as tradeoffs but are actually *multi-dimensional* tradeoffs that can often be optimized simultaneously.

**Do:**
- Treat *security ↔ usability* as a multi-dimensional optimization, not a tradeoff (Document 19-1 customer data access strategy): *framing a discussion as trading off between security and utility is a sign that we are having the wrong discussion.*
- Test the multi-dimensional hypothesis with systems modeling: e.g., increasing *testing time* (which sounds bad) is actually a positive outcome when it correlates with reduced production-error rate.
- Use strategy altitude to choose where to invest in quality/velocity/reliability improvements: org-altitude (CI blocks low-coverage PRs) vs. team-altitude (team planning schedules bug fixes first).

**Don't:**
- Don't accept the lazy framing: *faster onboarding doesn't equal better*—in mature markets, re-engagement often beats onboarding speed (Document 17-4).
- Don't accept *more testing time* as a failure signal; it can be a success indicator that the testing error loop found more issues before they reached production.

*Ref: Crafting_Engineering_Strategy.md — "Direction" / "Approval and Advice Forums" / "Modeling LLMs' Impact on Developer Experience" / "Why Does Refinement Matter?"*

---

### 31. Technical Debt as Portfolio (Allocations = Strategy)

**Principle:** Tech debt is most usefully framed as a *portfolio* of decisions, not a single kind of accumulation. Allocations are the most concrete statement of organizational priority.

**Do:**
- Treat allocations as the highest-leverage policy lever: who/what gets headcount and budget?
- Use **N-1 backfill** as a deliberate allocation tool (Document 18-1): backfilling at one level below the departed role, combined with strict senior-level caps, reduces headcount cost growth without layoffs.
- Translate tech-debt conversations into diagnosis: which flows are growing? Where are the *real* levers? (Strategy testing avoids paying for tech-debt-fixing migrations that don't actually move the needle.)
- Use systems modeling to find the leverage point (e.g., reducing *Missing/incorrect information* errors in service provisioning was the highest-leverage improvement, not faster deployment).

**Don't:**
- Don't fight tech debt with grand migrations driven by anxiety and ego (the Grand Migration antipattern).
- Don't accept N-1 backfill silently; hiring managers will quietly ignore softer versions, which is why the policy pairs with hard caps (e.g., one Principal per BU).

*Ref: Crafting_Engineering_Strategy.md — "Inappropriate Strategy Is Especially Impactful" / "What Is Exploration?" / "Allocations" / "Seniority-Mix Model: Backfill at N-1"*

---

### 32. Developer Productivity (DX): Diagnose and Refine Before Deciding

**Principle:** DX improvements need the same Explore → Diagnose → Refine → Set Policy → Operate discipline as any other strategy.

**Do:**
- Reach for measurable signals: deploy time, deploy stability, test coverage, test time, test flakiness, developer productivity survey results (Stripe's twice-a-year survey).
- Refine DX strategies with systems modeling *before* rollout: in Document 17-2, modeling LLMs' impact on DX showed that *faster testing* is the wrong goal—*reducing production-error rate* is the right one.
- Select narrow strategies (e.g., "selective test execution" + "instrument test failures" + "add static typing to highest-value portions") with concrete impact metrics and define success/failure within 4 weeks.
- Use the **Lethain/systems simulation** (or spreadsheet) to model constraints before paying for change.

**Don't:**
- Don't confuse activity with progress; changing the testing rate alone won't change the integrated customers stock if the real constraint is elsewhere.
- Don't roll out without impact metrics; adoption metrics alone aren't DX improvements.

*Ref: Crafting_Engineering_Strategy.md — "Modeling LLMs' Impact on Developer Experience" / "Why Did Stripe Build Sorbet?" / "Strategy Testing for Iterative Refinement"*

---

### 33. Engineering Planning: Resourcing, Prioritization, and Pairings

**Principle:** Planning is organizational, not algorithmic. The most important rule is that the **team is responsible for the contents of its own roadmap**, because out-of-band executive instructions will defeat any other system.

**Do:**
- Pair engineering managers with product managers (the Calm "joint pairs" pattern).
- Apply the **resourcing Engineering-driven projects** policy (1 protected project per team per quarter, ≤ 20% bandwidth, must advance a measurable metric with measurable progress within 4 weeks).
- Resource Engineering-driven projects *first*, not last—but only if concrete proposals exist.
- Plan for ambiguity: protect capacity in two-week chunks during chaotic periods.

**Don't:**
- Don't let product or engineering prioritization be hijacked by side discussions; explicit escalation paths are mandatory.
- Don't mandate tools or processes from above that teams can't actually carry; pair mandates with cost/burden analysis.

*Ref: Crafting_Engineering_Strategy.md — "Document 21-2: How to Resource Engineering-Driven Projects at Calm" / "Doing Strategy in Chaotic Environments"*

---

### 34. Cognitive Load (Team Topologies Echo)

**Principle:** Cognitive load is bounded; the strategies that succeed concentrate investment rather than scattering it. *Concentrate company investment into a smaller space.*

**Do:**
- Pick a small set of technologies to support deeply. Stripe's Sorbet strategy worked only because Stripe enforced a single programming language across (essentially) all teams.
- Adopt the same pattern at a smaller scale: Calm declared *all new code in the monolith*; backfilling that resolves cognitive-load problems at the boundary.
- Reduce cognitive load through **universal-adoption properties**: N-1 backfill, disaster-recovery configurations, and lint defaults only work when *consistently adopted*.
- Match strategy altitude to the cognitive-load cost: high-altitude permissive strategies spread lightly; high-altitude prescriptive strategies risk overload.

**Don't:**
- Don't add a new programming language lightly—the centralization tax it imposes (build, deploy, monitoring, hiring, support) compounds over time.
- Don't be fooled by local simplification: a "drift" between monolith services and macrolith services still has the cognitive cost of *both* paradigms.

*Ref: Crafting_Engineering_Strategy.md — "Strategy Changes Companies" / "Direction" / "Why Did Stripe Build Sorbet?" / "Strategy Altitude"*

---

### 35. Asking the Right Questions (Calibrating Strategy)

**Principle:** *If you've shared out a bunch of strategy work, but it doesn't seem to be changing how your software is written, scale back.* The best single diagnostic question: *Has your prior strategy work affected subsequent decisions?*

**Do:**
- Run the **debugging questions** on every strategy:
  - *What is the current strategic state?* (Globally consistent / consistent within teams / highly varied.)
  - *Is the state trending up or down?* (Hiring ramp, new leaders, organizational change, doc quality.)
  - *Do you understand the history well enough to act?*
- Run the **eval rubric** per phase.
- Ask: *Who needs to know?* If a Staff-plus engineer + engineering manager knows the strategy, *information herd immunity* is typically sufficient. *You don't need everyone to know something; you just need enough people to know it that any confusion doesn't propagate too far.*
- Track policies you *can* apply and *can* enforce; if you can't do either, the policy won't accomplish anything.

**Don't:**
- Don't ask "do we have strategy?" without also asking "what is the implicit strategy?"
- Don't ask "is the strategy right?"—ask "is the *phase* of the strategy right?"

*Ref: Crafting_Engineering_Strategy.md — "Are You Doing Too Much?" / "Information Herd Immunity" / "Criteria for Effective Policies" / "A Rubric for Evaluating Strategy"*

---

### 36. Organizational Design (Strategy as Decision Rights)

**Principle:** Strategy doesn't merely describe what gets built; it embodies how decisions are made. *Two-headed organizations* (paired manager + Staff-plus leader) are a deliberate design choice to reduce communication errors.

**Do:**
- Maintain pairs of leaders in each area (manager + senior engineer) where possible, even though the cost is non-trivial. *Errors in one-to-one communication are so prevalent, and the cost of communication errors is so high, that I now structure organizations and communication mechanisms to ensure that I always convey important updates (like those related to strategy) to at least two people in each area of the organization.*
- Use the **Navigators** pattern: explicitly named technical leaders with executive authority for technical decisions (Carta). Designed to make it possible to iterate strategy without negotiating with hundreds of engineers directly.
- Make communication-of-context a recurring discipline: communication during onboarding is key; some companies drill new hires on how decisions are made, others expect team-level training. *Both approaches can work well. Both can work poorly.*

**Don't:**
- Don't rely on a single leader-to-leader communication channel for important updates.
- Don't let promotion criteria reward ambitious projects with hidden costs to the organization (Document 18-1 / Yahoo! Erlang adoption example).

*Ref: Crafting_Engineering_Strategy.md — "Implicit Strategy Comes at a Cost" / "Written Strategy Drives Organizational Learning" / "Two-Headed Organizations"*

---

### 37. Compensation & Incentives as Strategy Lever

**Principle:** Incentives often determine the actual strategy, regardless of the written one. If promotions reward ambitious projects over solid execution, organizations will ship ambitious-but-net-negative work.

**Do:**
- Audit the **incentive system** when a strategy fails despite being directionally correct: many senior leaders are *desperate to make an early impact* and pursue initiatives that establish their reputation over initiatives that work.
- Recognize that the *appearance* of progress is easier to manufacture than actual progress; executive strategies can fail so spectacularly because executive authority masks weak diagnosis.
- Look for promotion criteria that reward side-goal projects (e.g., Yahoo! Erlang adoption: 3 of 15 engineers would touch it, but counterevidence was ignored because the project advanced personal goals).
- When designing your own promotion criteria, be mindful of the tradeoff: *an organization that innovates too much while empowering individuals* OR *an organization with little waste but restricted room for creativity*. Pick consciously and adjust when needed.

**Don't:**
- Don't use promotion bars as a hidden strategy mechanism; senior leaders' sincere beliefs often go stale.
- Don't accept "the executive can stop this" as the binding constraint—often the actual binding constraint is the promotion rubric.

*Ref: Crafting_Engineering_Strategy.md — "If It Matters, Why Is It Skipped?" / "Antipatterns in Refinement" / "Doing Strategy as an Executive"*

---

### 38. Role-Based Strategy Toolkits (Who Uses What)

**Principle:** Different roles at different altitudes get different toolkits. The same Explore → Diagnose → Refine → Set Policy → Operate applies, but the *tools within each step* differ.

**Do (IC engineer):**
- Use **take five, then synthesize** (Document 21-5 in *Staff Engineer*).
- Use **model, document, share**.
- Build a network of peers (Document 30-9 in *Staff Engineer*).
- Focus on nudges + real datasets + model-document-share; the executive toolkit isn't required.

**Do (Engineering Manager):**
- Pair Eng Managers with PMs; protect capacity for engineering-driven projects (Calm resourcing pattern).
- Use N-1 backfill with team-level exceptions.
- Replace grand migrations with model-document-share or architecture-advice-process substitutes.

**Do (Senior / Staff engineer):**
- Lead strategy-testing cycles.
- Refine with strategy testing + systems modeling (use lethain/systems for rapid iteration).
- Run weekly meetings sponsor/guide style.

**Do (Director / VP Engineering):**
- Manage strategy altitude (org- vs. team-level) explicitly.
- Set policy across allocations, approvals, direction, guidance.
- Operate via nudges at scale; inspect via leading indicators, not just lagging adoption.

**Do (CTO / VP Engineering):**
- Treat organization as paired leaders (manager + senior) where possible.
- Maintain first-90-days discipline: *diagnose before changing things*; resist the playbook-driven urge to Grand-Migrate.
- Maintain high-altitude strategy carefully (Carta approach: permissive + escalation + one prescriptive exception).
- Maintain a private catalogue of strategy artifacts (Carta Navigators team's annual cycle).

**Do (Founder):**
- Treat strategy as the durable artifact of the company's most important decisions.
- Document *why* decisions were made (it's the only mechanism that survives you).
- When PE/IPO arrives, move with the seniority-mix model + geography/infrastructure review pattern (Document 18-1).

*Ref: Crafting_Engineering_Strategy.md — "Doing Strategy as an Engineer" / "Doing Strategy as an Executive" / "Policy for Improving at Strategy" / "Strategy Altitude" / "Maintaining Strategy Altitude"*

---

### 39. Calibrating Strategy: The Five Deep Dives (Explicit)

**Principle:** Treat every strategy problem as a five-step deep dive. *Each step is an input that flows into the next.*

**Do (per strategy work, every time):**
```
DEEP DIVE 1 — EXPLORE
  Q: What 3 internal teams + 3 external companies have solved this?
  Q: What did they read? Who do they talk to?
  Q: What could invalidate their approach in your environment?

DEEP DIVE 2 — DIAGNOSE
  Q: What's the *actual* problem (not the loud one)?
  Q: Which perspectives am I missing? Who's the loudest skeptic?
  Q: Where do I have skin in the game?

DEEP DIVE 3 — REFINE
  Q: What's the narrowest, deepest slice I can test?
  Q: What model would tell me which lever matters?
  Q: What evolution could surprise my 5-year plan?

DEEP DIVE 4 — SET POLICY
  Q: Does each policy address a specific diagnosis?
  Q: Is it applicable AND enforceable?
  Q: Am I solving an N-1 problem?

DEEP DIVE 5 — OPERATE
  Q: What's the inspection mechanism? Where? How?
  Q: What's the nudge? Limit count, action, instruction.
  Q: What's the silent-failure guard?
```

**Don't:**
- Don't skip deep dives; *the biggest risk for most strategies is not that you model too early or map too late, but that you skip both steps entirely.*

*Ref: Crafting_Engineering_Strategy.md — "Steps to Build an Engineering Strategy" / "Antipatterns in Refinement"*

---

### 40. Engineering Strategy: The Implementation Kernel (Repeat for Emphasis)

**Principle:** Six rules to remember:

1. *There is always a strategy.* Recognition is the first step toward improvement.
2. *Always be working on exactly one strategy.* Doing more feels like progress, but usually fails.
3. *Save judgment for later* during exploration; *whisper the controversial parts* in diagnosis.
4. *Refinement is the kernel.* Use strategy testing, systems modeling, Wardley mapping.
5. *Nudges are the most effective operational mechanism*; pair them with inspection.
6. *Write for readers.* Invert the document structure so policy + operation come first.

**Don't:**
- Don't let cultural distaste for uncomfortable truths prevent you from including them in the diagnosis.
- Don't roll out a strategy without a measurement plan; "pressure without a plan" sounds right but accomplishes nothing.

*Ref: Crafting_Engineering_Strategy.md — "Preface" / "Part I summary" / "Chapter 23 closing" / "Chapter 24 closing"*

---

## Anti-Patterns & Common Mistakes

- **The Grand Migration:** A new leader declares a massive migration to their former employer's tech stack, pushing for it even when it becomes clear it does not solve the problem. *This is anxiety and ego wrapped in a Gantt chart.* → **Fix:** Time-box exploration; require diagnosis; treat prior organization's solutions as data, not template.
- **Digg V4-style inappropriate strategy:** Rewriting from PHP monolith to PHP frontend + Python services + early Cassandra; replacing decade-old nuanced algorithms with a hack written days before launch. → **Fix:** Confirm "inappropriate" via diagnosis, not just "bad"—the same approach could work in different circumstances.
- **Skipping refinement:** Stripe's failed Agile rollout solved awareness without tackling prioritization across stakeholders. → **Fix:** Use strategy testing on a narrow, deep slice.
- **Manufactured consent:** Citing internal leaders' surface-level agreement to push a rearchitecture they privately doubted. → **Fix:** Probe for explicit skepticism; hold one author accountable for synthesis.
- **Discarding counterevidence:** Yahoo! adopted Erlang for a team that only 3 of 15 engineers would touch—the counterevidence was ignored because of a side goal. → **Fix:** Document counterevidence and its impact on the diagnosis.
- **Skipping exploration:** "Less than a few hours is suspicious, more than a week is questionable." → **Fix:** Time-box; explore until three teams + three companies are mapped.
- **Stopping diagnosis at the lazy answer:** "We just need to work harder" or "if only leadership would decide." → **Fix:** Reframe the prevention as a condition the strategy must address.
- **Top-down pronouncements:** Return-to-office mandates that ignore motivation. → **Fix:** Pair mandates with consequences (and consequences with enforcement); otherwise it's not a mandate.
- **Education-as-announcement rollouts:** One-time all-company announcement; updated training for new hires. → **Fix:** Combine with reminders, role models, inspection.
- **Mandatory recurring trainings:** Required by compliance; produce low-quality content because attendance is enforced. → **Fix:** Use for true legal/regulatory needs; never as the only mechanism for behavioral change.
- **"Just change the culture":** Frame everything as cultural; simplify the cure. → **Fix:** Pair with visible leader role-modeling and reinforcement mechanisms.
- **Pressure without a plan:** Strategy that *sounds right* but lacks concrete details (e.g., service migrations modeled after apocryphal Amazon top-down mandates). → **Fix:** Are there numbers showing impact? Is there a clear debugging mechanism?
- **Cargo-culting:** Recreating a process that previously solved a problem without understanding what made it effective. → **Fix:** Remain skeptically optimistic; force borrowed patterns to prove their merit.
- **Skipping the operational plan:** Best policies die quietly. → **Fix:** Compose explicit operational plan; review every three months.
- **Reading like an essay:** Leaving the policy at the bottom of writer-oriented docs. → **Fix:** Invert the structure; lead with Policy + Operation.
- **Strategy on autopilot:** Treat strategy as a single-iteration exercise. → **Fix:** Split strategies into phases; evaluate each phase; remember the rubric.

---

## Decision Heuristics / Checklists

### When to write strategy
- ☐ Organization is in "consistent within teams" or "highly varied" state.
- ☐ Strategic state is trending toward worse (rapid hiring, playbook-driven leaders, reorgs, broken onboarding communication).
- ☐ I have context on the history (people + decisions).
- ☐ I am not currently over-committed (> 1 strategy in flight).
- ☐ A senior sponsor (or explicit skip of sponsorship) exists.

### Evaluating operational mechanism
- ☐ Measurability — leading + lagging indicators identified.
- ☐ Adoption cost reasonable.
- ☐ User and provider ease/burden balanced.
- ☐ Authority reliance not fragile.
- ☐ Cultural alignment plausible.

### Setting policy
- ☐ Each policy maps to ≥ 1 diagnosis.
- ☐ Policy is applicable (clear tradeoffs).
- ☐ Policy is enforceable (with consequences).
- ☐ Backtested against recent decisions.
- ☐ Mined for conflict; refined if uncertain.

### Diagnosing strategy
- ☐ Braindump complete.
- ☐ Exploration summarized.
- ☐ Distinct perspectives captured (esp. those I disagree with).
- ☐ One author synthesizes the unified perspective.
- ☐ Tested drafts against the most fervent disagreers.

### Refining strategy
- ☐ Refinement chosen for the problem type:
  - Ambiguous problem → strategy testing.
  - Complex leverage analysis → systems modeling.
  - Ecosystem evolution → Wardley mapping.
- ☐ Sponsor + Guide identified with weekly meeting on calendar.
- ☐ Impact metrics (not adoption metrics) selected.

### Writing a strategy document
- ☐ Reader-oriented structure: Policy → Operation → Refine → Diagnose → Explore.
- ☐ Document reviewed by an uninvolved reader.
- ☐ Commenting period + office hours announced.
- ☐ Disabled in-document commenting after release.
- ☐ Question channel is durable and obvious.

### Strategy evaluation rubric (per phase)
| Dimension | 3 | 2 | 1 | 0 |
|-----------|---|---|---|---|
| Speed | daily/weekly | monthly | quarterly | > quarterly |
| Cost | single team | small flex cross-team | large flex cross-team | large rigid cross-team |
| Impact | full problem | essential portion | simple portion | nothing |

→ Total ≥ 6: pursue. < 6: introspect.

---

## Key Takeaways

1. **There is always a strategy**, even if it is unwritten. *Recognition is the first step toward improvement.*
2. **The five-step process** (Explore → Diagnose → Refine → Set Policy → Operate) is the repeatable structure. Skipping steps—especially refinement and operations—is the most common cause of failure.
3. **Refinement is the kernel.** Strategy testing, systems modeling, and Wardley mapping are the three primary tools. Use strategy testing for ambiguous problems, systems modeling for complex leverage analysis, and Wardley mapping for ecosystem evolution.
4. **Operations matter more than most strategists think.** Policies without operational mechanisms fade quietly. *Nudges are the most effective mechanism*; top-down pronouncements, mandatory recurring trainings, and "just change the culture" are the least.
5. **Write for readers, not writers.** Invert the document structure. Lead with policy and operations. *The vast majority of strategy readers just want to understand how to apply the strategy.*
6. **Strategy is iterative, not waterfall.** Good strategies embrace change and are refined continuously. The best strategies support fast, cheap iteration.
7. **Anyone can do strategy.** Engineers can use "take five, then synthesize" and "model, document, share." Executives have more tools but fewer guardrails. The key is matching your approach to your authority level.
8. **The evaluation rubric** (Speed, Cost, Impact, scored 0–9, threshold 6) provides a structured way to assess strategy quality and identify where to improve. *Evaluate per phase, not per strategy.*
9. **The details matter enormously.** The same general strategy that works at one company can fail at another. Copying strategies without understanding the diagnosis leads to cargo-culting.
10. **Communication errors are expensive.** Maintain two-headed organizations (manager + senior) to reduce channel loss; treat strategy as a repository to combat oral-history fragility.

> *"Engineering organizations today routinely waste dozens or hundreds of years of their teams' lives by refusing to engage with the reality of their problems. … A bit of rigor in our thinking can change this — and that is the bare minimum we owe ourselves, our colleagues, and our users."* — Will Larson, *Crafting Engineering Strategy*

---

## Cross-References

- Related engineering leadership perspectives: *Staff Engineer* (Will Larson), *The Engineering Executive's Primer* (Will Larson), *An Elegant Puzzle* (Will Larson).
- Foundational strategy text: *Good Strategy, Bad Strategy* (Richard Rumelt) — Diagnosis / Guiding Policy / Coherent Actions.
- Strategy environments: *Wardley Maps* (Simon Wardley), *The Value Flywheel Effect* (David Anderson), *Technology Strategy Patterns* (Eben Hewitt).
- Systems modeling: *Thinking in Systems: A Primer* (Donella Meadows), *Business Dynamics* (John Sterman).
- Architecture/library patterns: *Fundamentals of Software Architecture* (Richards/Ford), *Building Evolutionary Architectures*, *Team Topologies*, *Software Architecture Metrics*.
- Operations/scaling: *Scaling People* (Claire Hughes Johnson), *The Phoenix Project*, *Recoding America* (Jennifer Pahlka).
- Topic index: see `best_practices/INDEX.md`.

---

## Appendix A — Common Decision Traps and How to Recognize Them

**Principle:** Strategy work is full of recurring cognitive traps; recognizing them in flight is the cheapest way to recover.

**Traps to watch for:**

- **Prior-success anchoring:** "It worked at my last company, so…" Companies that looked similar from the outside operate on very different internal dynamics. *Your prior approach was correct for those dynamics, not these.*
- **Silent carrier of cargo:** A leader who deployed an idea that succeeded is now in a new context; the cultural and operational environment that made it succeed is absent. The result looks like cargo-culting.
- **Promotion-via-ambition loop:** Engineers build novel, ambitious projects primarily to clear the senior promotion bar. They may solve some easier proof points first to secure the promotion before the rollout stalls out.
- **Diagnosis performed through a funnel:** A senior writes the diagnosis alone and then "consults" stakeholders. The result is a *funnel* rather than a *synthesis*. Hold one author accountable for the unified synthesis, but iterate the draft against disagreeing voices.
- **Operational silence:** A mechanism that lacks an inspection that *cannot silently fail*. Most failure modes for policies begin here.
- **Diagnostic impatience:** Skipping refinement to ship under an artificial deadline. Convert the deadline into the *start* of refinement.
- **Strategy-document trap:** Letting the document template grow so heavy that writing strategy becomes *more* painful than executing strategy. Treat templates as owned artifacts whose custodian cares about the user.

*Ref: Crafting_Engineering_Strategy.md — "If It Matters, Why Is It Skipped?" / "Antipatterns and Ineffective Mechanisms" / "Cargo-Culting" / "Whisper the Controversial Parts" / "What If You're Not an Executive?"*

---

## Appendix B — Verbatim Examples of Strategy Documents (Reader-Oriented Refactors)

The book repeatedly demonstrates how a *reader-oriented* refactor improves the doc without weakening the substance. Two patterns appear across most case studies:

**(a) The Uber service-migration strategy refactor** (Document 16-1): folds *Operation* into *Policy*, so the user sees the seven sequenced tasks in the same section as the principles driving them.

```
[Reader-Oriented]

POLICY AND OPERATION (combined)
  *Constrain manual provisioning allocation...*
  *Self-service must be safely usable by a new hire without Uber context.*
  *Move to structured requests, and out of tickets.*
  *Prefer initializing new services with good defaults...*

  Sequenced tasks:
    1. Internal tool...
    2. Extend tool to automation interface...
    3. Generate Puppet scaffolding...
    4. Automate port allocation...
    5. Replace manual server assignment...

REFINE (systems model study)
DIAGNOSE
EXPLORE (papers, Wardley map)
```

**(b) The LLM adoption strategy refactor** (Document 17-1): merges *Refine* into *Diagnose* (because models and maps felt closer to diagnoses), and discards a separate *Operation* section (because operations sit naturally next to their policies).

```
[Reader-Oriented]

POLICY (one block, with operations inline)
  *Reactivate departed and suspended drivers...* (report progress monthly in Exec Weekly)
  *Start with Anthropic.* (exceptions reviewed in ML Review)
  *DX team offers an LLM-backed dev-productivity tool...* (vendor approvals in #cto)
  *Internal Tools offers an LLM-backed ad hoc prompting tool...* (approvals in #coo)
  *Refresh policy in six months.* (questions in #cto)

DIAGNOSE (with refine folded in: counter-intuitive from systems modeling)
EXPLORE (with Wardley map of LLM ecosystem)
```

**General rules for refactoring:**

- Drop Operation as a section if its content fits naturally with each policy.
- Merge Refine into Diagnose if your refinements tightly inform specific diagnoses.
- Always keep Policy + the rest-of-document contrast (in that order for readers).
- Don't refactor before writing the writer-oriented version first; the writer-oriented artifact is how the strategy *thinks* and how future consultants will *understand* it.

*Ref: Crafting_Engineering_Strategy.md — "Strategy Refactoring" / "Inverting the Document Structure for Reading" / "Document 16-1" / "Document 17-1"*

---

## Appendix C — Operational Mechanism Patterns by Scenario

When you reach for an operational mechanism, reach for the right one:

```
SCENARIO                              PREFERRED MECHANISM
─────────────────────────────────────────────────────────────────
Permissive policy, attention issues   Nudges + Inspection
Mandatory compliance (PCI/SOX)        Approval forums + Audits
High-volume recurring decisions       Automation (+ UX investment)
Cross-functional governance           Weekly meetings + Escalation
New tech adoption in greenfield        Pilot team + Documentation + Training
Tech debt convergence                 Time-bounded working group
Sensitive policy (security, data)     Approval forum + Inspection
Ambiguous diagnosis requiring fudge   Deferral to future work
High-altitude directives              Top-down pronouncements + Inspection
                                       (intentionally limited utility)
```

**Conditions to escalate to a different mechanism:**

- Nudges become noise → reduce count or improve targeting.
- Automation has poor UX → pair with a UX designer before rollout.
- Inspections silently fail → add named accountable owner; replace with synchronous moment.
- Approval forums become bottlenecks → loan authority to a named working group (Facilitating Software Architecture / Andrew Harmel-Law).
- Meetings multiply → time-box every meeting; assign exit criteria.

*Ref: Crafting_Engineering_Strategy.md — "Effective Mechanisms and Patterns" / "Approval and Advice Forums" / "Inspection" / "Nudges" / "Automation" / "Deferral to Future Work" / "Meetings"*

---

## Appendix D — Example Systems Models (Verbatim Excerpts)

Three systems models from the book deliver the heavy lifting in their respective case studies. The patterns below show how each model encodes a real business question.

### D.1 — Service onboarding (Uber, 2014)

```
HiringRate(10)
ProductEngineers(1000)
[PotentialHires] > ProductEngineers @ HiringRate
[PotentialServices] > RequestedServices(10) @ ProductEngineers / 10
RequestedServices > InflightServices(0, 10) @ Leak(1.0)
InflightServices > PortNameAssigned @ Leak(1.0)
PortNameAssigned > PuppetGenerated @ Leak(0.8)        # 20% info-error rate
PortNameAssigned > RequestedServices @ Leak(0.2)       # bounces back
PuppetGenerated > PuppetConfigMerged @ Leak(0.8)
PuppetGenerated > InflightServices @ Leak(0.2)         # bounces back
PuppetConfigMerged > ServerCapacityAllocated @ Leak(0.8)
PuppetConfigMerged > PuppetGenerated @ Leak(0.2)        # bounces back
```

**Insights:** Status quo grows the backlog. +500% manual capacity doesn't clear it. *Only self-service clears it.* All error rates contribute, but the *first* error rate (port/name) is highest-leverage because compounding errors downstream mean fixing the earliest lever gives the largest absolute lift.

### D.2 — Developer experience with LLMs (spreadsheet)

Configuration values (for round-by-round simulation):

```
TicketOpenRate        = 1
StartCodingRate       = 1
MaxConcurrentCodingNum = 3
TicketTestRate        = 1
ErrorsInProd          = 0.25
ErrorsInDeploy        = 0.25
ErrorsInTest          = 0.25
```

Excel-style formulas used:

```
= IF(C2 >= Config!$B$3, 0, Config!$B$2)        # StartCodingMore?
= A2 + Config!$B$1 - B2 + J2                   # Open Tickets (with prod-error flow back)
= C2 + B3 - D2 + J2 + F2                       # Started Coding (with error inflows)
= E2 + D3 - G2 - F2                            # Tested Code
= G2 + F3 - H2 - I2                            # Deployed Code
= FLOOR(I3 * Config!$B$5)                      # ErrorsFoundInProd?
= FLOOR(G3 * Config!$B$6)                      # ErrorsFoundInDeploy?
= FLOOR(E3 * Config!$B$7)                      # ErrorsFoundInTest?
```

**Insight:** Reducing ErrorsInProd from 0.25 to 0.1 still reaches equilibrium at a higher Closed-Tickets value but eventually hits an equilibrium. Tripling TicketTestRate alone doesn't change the equilibrium (because the constraint is in starting tickets). The only meaningful lever is reducing production-error rate.

### D.3 — Driver onboarding (LLM strategy)

```
CityPop(10000)
CityPop > AppliedDrivers @ 100
AppliedDrivers > EligibleDrivers @ Leak(0.25)
EligibleDrivers > AppliedDrivers @ Leak(0.10)        # right-to-left: missing info
EligibleDrivers > OnboardedDrivers @ Leak(0.25)
OnboardedDrivers > ActiveDrivers @ Leak(0.50)
ActiveDrivers > DepartedDrivers @ Leak(0.10)
ActiveDrivers > SuspendedDrivers @ Leak(0.10)
DepartedDrivers > ActiveDrivers @ Leak(0.05)         # base case
SuspendedDrivers > ActiveDrivers @ Leak(0.01)        # base case
```

**Counterintuitive insights (Document 17-4):**

1. Doubling eligibility rate (Leak(0.25) → Leak(0.50)) has *little* long-run impact on active drivers (city's potential driver pool is finite).
2. Eliminating the missing-info right-to-left flow has minimal impact on active drivers.
3. Increasing *departed* reactivation (Leak(0.05) → Leak(0.20)) shifts active-driver equilibrium upward significantly.
4. **Most surprising:** increasing *suspended* reactivation (Leak(0.01) → Leak(0.025)) has a *larger* impact than increasing *departed* reactivation by the same magnitude—because suspended drivers are a much larger slowly-deflating pool.
5. Increasing *both* reactivation rates together beats increasing either individually, because a slowly-deflating stock in either direction still drains the system.

*Ref: Crafting_Engineering_Strategy.md — "Document 16-2" / "Document 17-2" / "Document 17-4" / "How to Document a Model" / "Building Your Toolkit"*

---

## Appendix E — Five Public Resources to Pair with This Book

Larson's own extended work doubles the actionable surface area:

- ***Staff Engineer*** — *Take Five, Then Synthesize*, Build a Network of Peers chapters. Most directly applicable for individual contributors.
- ***The Engineering Executive's Primer*** — *Writing an Engineering Strategy* chapter. Most directly applicable for new executives.
- ***An Elegant Puzzle*** — practical operational wisdom (calibration, hiring, performance management, organizational design). Many of the operational mechanism patterns in this book trace back to *An Elegant Puzzle*.
- **lethain.com/blog** — extended notes, systems models, Wardley maps, and reflections on each career phase.
- **craftingengstrategy.com** — companion site with code, models, and supplementary materials (e.g., the lethain/systems library, eng-strategy-models GitHub repositories referenced in chapters 16, 17, 18, 22).

**Foundational strategy resources:**

- *Good Strategy, Bad Strategy* — Richard Rumelt (Diagnosis / Guiding Policy / Coherent Actions).
- *The Crux* — Richard Rumelt (iterative diagnosis through "testing, adjusting, and changing the frame").
- *Thinking in Systems: A Primer* — Donella Meadows.
- *Wardley Maps* — Simon Wardley (free on Medium).
- *How Big Things Get Done* — Flyvbjerg & Gardner (cheap mistakes early, expensive ones never).

**Adjacent engineering resources:**

- *Facilitating Software Architecture* — Andrew Harmel-Law (advisory architecture process).
- *Choose Boring Technology* — Dan McKinley (the underlying philosophy of Calm's stack discipline).
- *Run Less Software* — Rich Archbold (Intercom's stack discipline).
- *The Phoenix Project* / *The Goal* — useful as a modeling narrative (constraint optimization, stocks, and flows in narrative form).

*Ref: Crafting_Engineering_Strategy.md — "Strategy Resources"*

---

## Appendix F — Selected Quoted Material (For Review and Citation)

These quotes are pulled verbatim from the book and capture Larson's strongest framings. Use them for review and citation.

> "Strategy is the practice of making thoughtful decisions, and it is accessible to everyone—including you." — Chapter 1

> "Every organization follows a strategy embedded in its repeated decisions, even if no one has written it down. Recognition is the first step toward improvement." — Chapter 2

> "William Gibson has said, 'The future is already here—it's just not very evenly distributed.' In the same sense, there is always a strategy embedded into an organization's decisions—even if that strategy is only visible to a small group and is quickly forgotten." — Chapter 2

> "Engineering organizations today routinely waste dozens or hundreds of years of their teams' lives by refusing to engage with the reality of their problems." — Preface

> "Every strategy that I've seen fail did so due to a lazy or inaccurate diagnosis. It is very challenging to fail once you have a proper diagnosis, and it's almost impossible to succeed without one." — Chapter 7

> "Look with some suspicion at any week where you're not learning something that informs subsequent testing or making a decision that modifies your approach to testing." — Chapter 13

> "Prematurely rolling out a strategy prevents you from evaluating whether the strategy is effective. Pressure changes people's behavior in profound ways, and they often make those changes to create the impression that they're complying with your strategy while minimizing changes to the status quo." — Chapter 13

> "When your model and reality conflict, reality is always right." — Chapter 14

> "Modeling is a powerful tool to use in tandem with judgment, not a replacement for judgment." — Chapter 14

> "No strategy, even a cleverly written one, can guarantee business growth, hire a particular individual, or guarantee that lobbying will change an existing legal framework like GDPR." — Chapter 2

> "Always be working on exactly one strategy. Doing more feels like progress, but usually fails. Doing less is always a missed opportunity." — Chapter 4 summary

> "Information herd immunity: you don't need everyone to know something; you just need enough people to know it that any confusion doesn't propagate too far." — Chapter 2

> "Most engineers will claim their company doesn't have a clear strategy—even though all companies follow some strategy, even if it's undocumented." — Chapter 5 intro

> "Refinement is the kernel of effective strategy." — Chapter 8

> "Strategy thrives when its practitioners understand it is a living endeavor." — Chapter 23

> "The missing context is an impenetrable veil." — Chapter 23 (on evaluating others' strategies)

> "Looking effective and being effective tend to be only lightly correlated." — Chapter 4

> "Good security discussions don't frame decisions as a compromise between security and usability. We will pursue multi-dimensional tradeoffs to simultaneously improve security and efficiency." — Document 19-1

> "Mandates only matter if there are consequences. ... If an executive can't or won't enforce consequences for not complying with a mandate, it isn't a meaningful mandate." — Chapter 3

*Ref: Crafting_Engineering_Strategy.md — All chapters.*

---

## Appendix G — Mid-Semester Bookshelf Reference (Subject Mapping)

If you're pairing this book with adjacent reading on architecture, leadership, or operations:

| This Book Section                                | Best Companion                                      |
| ------------------------------------------------ | --------------------------------------------------- |
| Diagnosis                                        | *The Crux* (Rumelt); *Scaling People* (Hughes Johnson) |
| Refinement / Strategy Testing                    | *The Phoenix Project* (Kim et al.)                  |
| Refinement / Systems Modeling                    | *Thinking in Systems* (Meadows); *Business Dynamics* (Sterman) |
| Refinement / Wardley Mapping                     | *Wardley Maps* (Wardley); *The Value Flywheel Effect* (Anderson) |
| Setting Policy / Allocation                      | *Good Strategy, Bad Strategy* (Rumelt)              |
| Operations / Nudges                              | *An Elegant Puzzle* (Larson)                        |
| Operations / Architecture Advice                 | *Facilitating Software Architecture* (Harmel-Law)    |
| Strategy Altitude / Organizational Design        | *Team Topologies* (Skelton & Pais)                  |
| Case Study: Service Architecture                 | *Fundamentals of Software Architecture* (Richards/Ford); *Building Evolutionary Architectures* (Ford et al.) |
| Case Study: LLM Adoption                         | *AI Engineering* (Huyen)                            |
| Case Study: PE / Cost Discipline                 | *The Engineering Executive's Primer* (Larson); *Scaling People* (Hughes Johnson) |
| Case Study: Stripe API Stability / Type Checker  | *Staff Engineer* (Larson)                           |
| Calibrating Your Strategy Practice               | *An Elegant Puzzle* (Larson); *The Engineering Executive's Primer* (Larson) |

*Ref: across chapters — "Strategy Resources" / "Books" / "Case Studies" / "Public Resources"*

---

## Appendix H — Engineering Strategy as a Universal Language

By the end of the book, strategy is reframed as a **universal language** for decision-making — not an executive perk:

- **For any conversation that risks grinding to a halt without a shared vocabulary** (allocation of headcount, technology choice, refactor sequencing, marketing-vs-eng time slices), reaching for strategy language (exploration, diagnosis, refinement, policy, operation) gives the room a five-step way to converge.
- **For any disagreement between senior leaders**, ask "What's the diagnosis? What's the policy? What's the mechanism?" If the disagreement cannot be reduced to those three things, escalate to exploration, not authority.
- **For any new leader joining**, the earliest opportunity to contribute is to *write down* what the current strategy is. Recognition precedes improvement.

> "Strategy isn't reserved for executives. It's the practice of making thoughtful decisions, and it's accessible to everyone—including you."

*Ref: Crafting_Engineering_Strategy.md — closing of Chapter 1 and Chapter 24*

---

*Last line of supporting evidence (verbatim, Document 17-1 summary): "When these strategies were written in 2024, dreams of LLM adoption were everywhere, but there was no certainty about how LLMs would actually evolve over time. Similarly, there were extremely few teams or leaders with meaningful experience adopting these technologies, but a great deal of pressure from the industry to incorporate them as quickly and broadly as possible. These documents show how strategy, particularly the refinement techniques, can support leaders in finding a reasonable path forward despite the impossible combination of urgency and uncertainty."*

---

## Appendix I — Quick-Reference Card

A printable summary for strategy meetings:

```
┌──────────────────────────────────────────────────────────────────────┐
│  WILL LARSON'S CRAFTING ENGINEERING STRATEGY — QUICK CARD            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. EXPLORE — three internal teams + three external companies.       │
│     Time-box: a few hours to a week. Save judgment for later.       │
│                                                                      │
│  2. DIAGNOSE — braindump, summarize, mine distinct perspectives,     │
│     synthesize (one author), test across disagreeing stakeholders.   │
│     Whisper the controversial parts. Reframe blockers as conditions. │
│                                                                      │
│  3. REFINE — the kernel of strategy. Use ONE of:                    │
│       • Strategy testing  (ambiguous problems, narrow slices)        │
│       • Systems modeling  (leverage points, complex systems)        │
│       • Wardley mapping   (ecosystems, 5+ year horizons)            │
│                                                                      │
│  4. SET POLICY — match each policy to a diagnosis.                   │
│     Pick the right kind: APPROVALS • ALLOCATIONS • DIRECTION •      │
│     GUIDANCE. Both APPLICABLE and ENFORCED.                          │
│                                                                      │
│  5. OPERATE — pick mechanisms by rubric:                             │
│     Measurability · Adoption cost · User ease · Provider ease ·     │
│     Authority reliance · Cultural alignment.                        │
│     Effective mechanisms: APPROVAL FORUMS · INSPECTION · NUDGES ·   │
│     AUTOMATION · DEFERRAL · MEETINGS. (Nudges win.)                 │
│                                                                      │
│  ALTITUDE — Permissive + low altitude = max volume.                 │
│  Always be working on exactly one strategy.                          │
│                                                                      │
│  EVALUATION — Speed × Cost × Impact, 0–9. Threshold ≥ 6.            │
│  Evaluate PER PHASE, not per strategy.                               │
│                                                                      │
│  WRITING — Policy → Operation → Refine → Diagnose → Explore.        │
│  Invert the order for readers; refactor while you rewrite.          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

*Ref: Crafting_Engineering_Strategy.md — full book, cross-chapter synthesis.*

---

## Appendix J — Practice Prompts (for Your Own Strategy Work)

Use these prompts as working language in your next strategy exercise:

**Exploration prompt:** "Before diagnosing, who else has solved this problem? Who disagrees with my read? What changed about this problem in the last year?"

**Diagnosis prompt:** "If we don't act, what happens? Whose perspective am I missing? What's the polite version of the uncomfortable truth?"

**Refine prompt:** "What's the narrowest, deepest slice I can test this week? What would invalidate my approach? Which lever from the model matters most?"

**Policy prompt:** "What diagnosis does this policy address? Who enforces it? What happens when enforcement fails?"

**Operation prompt:** "What's the silent-failure guard? What does my inspection dashboard measure? Is my nudge earning attention or burning it?"

**Rubric prompt (per phase):** "What was the speed, cost, and impact of this phase? What's the next phase, and what will it cost to operate?"

**Habit prompt:** "What three strategies did I touch this month? Which did I document? Which phase degraded?"

*Ref: Crafting_Engineering_Strategy.md — chapters 5, 7, 8, 9, 10, 13, 14, 15, 23, 24.*

---

## Appendix K — Closing Frame (the Book's Final Argument)

Larson's most memorable closing:

> *"Even the best ideas here are wrong in interesting ways, and will be surpassed by better ones."* — Chapter 24 closing

> *"I'd never ask you to wholly agree with my ideas. They are my best thinking on this topic, but strategy is a topic where I'm certain Hegel's worldview is the correct one."* — Final Words

> *"Right" or "wrong" is the wrong binary for strategy.* Strategies live across multiple phases. Each phase has its own speed, cost, and impact. A 7/9 in Phase 1 may become a 4/9 in Phase 2. Stopping a strategy is often a good sign. The strategist's job is to recognize phases, score them, and consciously trade high-altitude strategies for low-altitude ones when the cost of learning outpaces the rate of value.

This book is most successful when its core ideas become obvious enough that they're no longer worth discussing. *If this book is particularly successful, a few years from now the ideas in this book will be obsolete through their own ubiquity.*

*Ref: Crafting_Engineering_Strategy.md — "Final Words" / "Preface" / closing pages.*
