# Crafting Engineering Strategy by Will Larson -- Comprehensive Summary

## Overview

*Crafting Engineering Strategy* by Will Larson (O'Reilly, 2025) presents a structured, practical approach to creating, refining, and operating engineering strategies in software organizations. Drawing on his experiences at Uber, Stripe, Calm, Carta, and other companies, Larson argues that engineering strategy is not reserved for executives -- it is a discipline accessible to anyone willing to think carefully about decisions. The book adapts Richard Rumelt's framework from *Good Strategy, Bad Strategy* (diagnosis, guiding policy, coherent actions) into a five-step process specifically tailored for engineering organizations: Explore, Diagnose, Refine, Set Policy, and Operate. The book is organized into five parts, with ten detailed case studies drawn from Larson's career.

---

## Part I: Introducing Engineering Strategy

### Chapter 1: Introduction

Larson opens with a core conviction: strategy is not reserved for executives. It is the practice of making thoughtful decisions, and it is accessible to everyone. Even if you would prefer to avoid strategy, it is happening all around you. Every organization has a strategy embedded in its repeated decisions, even if it is not written down.

The book is grounded in Larson's direct experience and adapts Rumelt's three pillars of strategy:

1. **Diagnosis** -- A theory describing the nature of the challenge, identifying root causes.
2. **Guiding policy** -- General policies and tradeoffs to address the challenge.
3. **Coherent actions** -- Specific actions directed by the guiding policy.

Larson emphasizes that effective strategy is both iterative and mechanical. Strategies age and must be refined. The intellectual components matter, but the mechanical nuances of how policies are rolled out and adopted are equally critical. The most common reason strategies fail is not flawed thinking but mundane execution errors -- executives assuming strategies will roll themselves out, and teams skipping validation.

### Chapter 2: Is Engineering Strategy Useful?

Larson asserts that there is *always* a strategy, even when people claim there is not. Every organization makes repeated decisions according to some pattern, and that pattern is the strategy. The real question is whether that implicit strategy is any good.

Strategy changes companies in several ways:

- **Creating alignment** -- A documented strategy makes it clear to everyone what sort of game the organization is playing, so people can make informed decisions about whether they want to participate. At Calm, a clear strategy focused on product engineering caused some engineers to leave because they valued experimenting with new technologies more than product progress -- and that was a healthy outcome.
- **Concentrating investment** -- Deciding not to decompose a monolith allows you to invest the majority of tooling efforts into one language, one test suite, and one deployment mechanism.
- **Making valuable properties available through universal adoption** -- Policies like N-1 backfilling or disaster recovery configurations only work when consistently adopted.
- **Focusing execution** -- Stripe's Sorbet strategy allowed ten engineers to push the Ruby monolith toward static typing without distracting the larger organization.
- **Creating a knowledge repository** -- Documented strategy makes onboarding new hires, particularly senior ones, much more effective.

Inappropriate strategy is especially impactful. The Digg V4 rewrite -- moving from a PHP monolith to a PHP frontend with a dozen Python services, switching from MySQL to early Cassandra -- is Larson's example of the worst strategy he participated in. It killed the company. Importantly, Larson uses the term "inappropriate" rather than "bad" because the same strategy might work in different circumstances.

Written strategy drives organizational learning. At Carta, writing down strategy made it possible to iterate, disagree precisely, and evolve over time. Written strategy creates institutional memory, while oral history depends on who you talk to. Implicit strategy comes at a high cost: it is vulnerable to misinterpretation, creates inconsistency across teams and over time, and poses hazards to new leaders.

Larson introduces the concept of **information herd immunity**: you do not need everyone to know something; you just need enough people that confusion does not propagate too far. If every Staff-plus engineer and engineering manager knows the strategy, the organization can function effectively.

Writing strategy also supports personal learning -- building self-awareness, supporting situational awareness in new environments, and serving as a personal archive.

### Chapter 3: Who Gets to Do Strategy?

Anyone can do strategy from any position in an organization. The tools differ by role:

**As an engineer**, Larson recommends two approaches:
1. **"Take five, then synthesize"** -- Document how five related decisions have been made in your organization. Synthesize those into a diagnosis and policy. You are naming the implicit strategy, which forces a conversation.
2. **"Model, document, and share"** -- Model the approach you want others to adopt, document it, and share it. This influence-based approach works because even executive-driven strategies depend on influence.

**As an executive**, you have more latitude to mandate and cajole, but also more constraints (budgets, CEO visions, peers to satisfy). Executives have an easier time doing strategy but a harder time learning to do it *well*, because the appearance of progress is easier to manufacture than actual progress. Mandates only matter if there are consequences.

**In challenging environments**, Larson offers practical guidance:
- In **low-trust environments**, whisper the controversial parts -- translate difficult messages into softer versions.
- In **poor-judgment environments**, write strategy to educate colleagues about tradeoffs.
- When **strategies are missing**, accept the ambiguity as a fact and work around it. Never allow missing information to block forward progress.
- The only times to avoid strategy are when another part of the organization is already working on the same problem, or when you are trying to satisfy an emotional need for immediate impact rather than investing in long-term progress.

### Chapter 4: When Should You Write Strategy -- and How Much?

Organizations exist in one of three strategic states:
1. **Globally consistent** -- There is a clearly agreed-upon strategy, even if unwritten.
2. **Consistent within teams** -- Clear strategy within pockets but inconsistency across them.
3. **Highly varied** -- Little agreement across individuals.

If you are in the first state, more strategy work is unlikely to help. If you are in the latter two, it is time to write strategy. You should also consider trends: rapid hiring, new external leaders with playbook-driven approaches, frequent organizational changes, and ineffective communication of historical decisions can all degrade strategic state.

Before writing strategy, assess your **context level**: Do you understand the history of the area you want to change? Do you understand the individuals who made past decisions and the context that made those good decisions at the time?

On volume, Larson's strongest recommendation is to **always be working on exactly one strategy**. Limit work in progress. Start small, iterate until it works, then expand. What feels unambitious in the short term compounds over time.

**Strategy altitude** is a key concept for managing volume. Altitude refers to how permissive a strategy is and where it is implemented. Permissive strategies are less expensive than prescriptive ones. Lower-altitude (team-level) strategies are less expensive than higher-altitude (organization-level) ones. The formula to increase strategy volume is to reduce altitude, increase permissiveness, or both.

At Carta, Larson rolled out broad strategy work by focusing on permissive strategies with escalation paths, and only one highly prescriptive area (provisioning new services). Significantly more leaders fail by attempting too much strategy than too little.

---

## Part II: Steps for Building Engineering Strategies

### Chapter 5: Steps to Build an Engineering Strategy

Larson introduces five repeatable steps:

1. **Explore** -- Search through the problem and solution spaces before committing to an approach. Understand how others have solved similar problems.
2. **Diagnose** -- Correctly recognize the context the strategy needs to solve before deciding on policies. Delay thinking about solutions until you understand the problem's nuances.
3. **Refine** -- Test raw ideas against reality using strategy testing, systems modeling, and Wardley mapping.
4. **Set policy** -- Make the tradeoffs and decisions to solve the diagnosis.
5. **Operate** -- Implement concrete mechanisms that translate policy into an active force.

Each step flows into the next. The biggest risk is skipping steps, especially refinement. The structure is not sacrosanct -- the thinking behind the sections is what matters.

### Chapter 6: Exploring

A surprising number of strategies are doomed because authors anchor on one approach without considering alternatives. The "Grand Migration" antipattern occurs when a new leader declares a massive migration to their former employer's tech stack, pushing for it even when it becomes clear it does not solve the problem. At Uber, Larson saw new senior leaders initiate massive rearchitectures that copied their prior employer's approach without diagnosing the new environment. Intelligent people become trapped by their initial thinking because they build so much weight on early assumptions that it becomes impossible to acknowledge errors.

Exploration should continue until you know how three similar internal teams and three similar external companies have recently solved the same problem. Time-box exploration: less than a few hours is suspicious; more than a week is questionable.

The exploration process:
1. Gather every resource related to the problem.
2. Do web searching and check with colleagues about missing topics.
3. Summarize and separate what to explore from what to merely reference.
4. Work through the list, collecting notes.
5. Stop when you understand how a handful of teams have approached the problem.

Key exploration techniques include mining your organization for internal precedent, using your professional network (especially for topics like security and compliance where public information is limited), and reading widely and narrowly. Read 10-20 industry-relevant works per year on diverse topics, and read narrowly on the specific topic you are working on. The Uber service provisioning team read papers on Google's Borg and Apache Mesos to understand the state of the industry. Larson also recommends using your network -- in one strategy session, he texted industry peers during a meeting and got answers before the meeting ended, invalidating the room's assumptions and resolving a disagreement that might have taken weeks.

Save judgment for later. If no one involved in a strategy has changed their mind about something they believed, exploration is not done. This is especially true for senior leaders whose beliefs are well-justified by years of experience but who may not realize their prior experiences have gone stale. Sometimes the internal approach is not ideal but is still superior because it is already implemented and maintained by someone else -- your strategy can ride along as that team addresses the imperfections.

### Chapter 7: Diagnosis

Every strategy Larson has seen fail did so due to a lazy or inaccurate diagnosis. It is very challenging to fail once you have a proper diagnosis, and almost impossible to succeed without one.

The structured approach to diagnosis:
1. **Braindump** -- Write your best understanding of the circumstances from a blank sheet.
2. **Summarize exploration** -- Pull in diagnoses from similar situations, tagging whether each fits or needs adjustment.
3. **Mine for distinct perspectives** -- Talk to stakeholders who disagree with your early thinking.
4. **Synthesize into one internally consistent perspective** -- Represent all views competently, even those you disagree with.
5. **Test drafts across perspectives** -- Sit down with people who disagree most fervently and iterate until they agree you have captured their views.

An effective diagnosis is hard to argue against because it is a web of interconnected observations, facts, and data. Incorporate data where possible, but accept that some data will be missing -- if the data existed, the decision would likely already be made.

**Whisper the controversial parts.** When your diagnosis includes uncomfortable truths about the organization or individuals, find professional, nonjudgmental ways to acknowledge those circumstances. Do not exclude them -- that makes strategies impossible to evaluate or recreate.

**Reframe blockers as part of the diagnosis.** When something seems to prevent strategy work, it is actually a condition the strategy needs to address. "The executive team changes its mind too often" becomes "if we don't show concrete progress quickly, our strategy is likely to fail."

**Self-awareness** is crucial. Recognizing your own role in creating the problems your diagnosis identifies demonstrates maturity and improves the strategy.

### Chapter 8: Refining

Refinement is the highest-impact step of strategy creation and the most neglected. It takes raw, unproven ideas and tests them against reality.

At Stripe, a failed Agile rollout illustrates what happens without refinement: the strategy solved the easiest part of the problem (awareness of Agile techniques) without addressing the harder parts (prioritization across stakeholders). At Uber, the service migration strategy succeeded precisely because the team relied heavily on refinement through systems modeling and strategy testing.

Why is refinement skipped?
- **Low-altitude teams** almost always refine because they lack authority to force adoption.
- **Executives** skip refinement because they can mandate adoption and are pressured to make early impressions. They confuse sounding ambitious with being effective.
- **Promotion-driven engineers** in permissive strategy organizations pursue novel, ambitious projects that fail after initial proof points but secure the promotion.
- **Artificial deadlines** cause people to freeze their thinking rather than iterating.

Three refinement tools are introduced:

**Strategy testing** -- Identify the narrowest, deepest slice of your strategy and iterate until you see evidence it works. Find metrics that measure impact, not just adoption. Assume people mean well and that failures are due to friction and poor ergonomics.

**Systems modeling** -- Use stocks and flows to cheaply determine which levers might be effective. Useful when you are unsure where leverage points are, when you have significant data to compare against, or when disagreements are based on unstated intuitions.

**Wardley mapping** -- Plot users, needs, and capabilities on a map showing visibility and commoditization. Excellent for understanding how an evolving ecosystem will impact your approach. Particularly valuable for strategies involving dynamic technology or spanning five-plus years.

Antipatterns in refinement: skipping it entirely (the most common), manufacturing consent to create the illusion of refinement, and discarding counterevidence because of side goals.

### Chapter 9: Setting Policy

Policy is interpreting your diagnosis into a concrete plan -- a collection of decisions, tradeoffs, and approaches. An effective policy solves the entirety of the diagnosis.

Steps to set policy:
1. Review diagnosis for completeness.
2. Select policies that address the diagnosis, matching each to specific diagnoses.
3. Consolidate overlapping or adjoining policies.
4. Backtest against recent decisions.
5. Mine for conflict, emphasizing feedback from those who disagree.
6. Refine if uncertain.

Policies fall into four categories:

1. **Approvals** -- Define the process for making recurring decisions. Who approves, and how?
2. **Allocations** -- Describe how resources are split across investments. These are the most concrete statement of organizational priority.
3. **Direction** -- Explicit instruction on how a decision *must* be made. Appropriate when you value consistency over individual judgment.
4. **Guidance** -- Recommendation about how a decision *should* be made. Useful when you can articulate the destination but not mandate the path.

Criteria for effective policies: they must be **applicable** (useful for navigating real-world tradeoffs) and **enforced** (teams are held accountable). Policies that cannot be applied or enforced will not accomplish anything.

Novel policies are rare. The most likely place to find them is during the widespread adoption of a new technology. Most policies are adaptations of well-known approaches to new circumstances.

**Competing policy proposals** indicate a gap in diagnosis. When teams disagree on policy, the fastest resolution is to align on a diagnosis that invalidates some options.

**Recognizing constraints** is essential. Impractical policies suggest your diagnosis is missing an important pillar. Never propose a policy you cannot possibly fund or enforce.

**Dealing with missing strategies** from other functions: include the absence in your diagnosis and move forward. Leadership requires taking meaningful risks.

### Chapter 10: Operations

Even the best policies fail if teams do not adopt them. Operations is the art of making policies work.

Larson provides a six-factor rubric for evaluating operational mechanisms:
1. **Measurability** -- Can you measure leading and lagging indicators?
2. **Adoption cost** -- How much work to migrate?
3. **User ease/burden** -- Does the mechanism make users' work easier or harder?
4. **Provider ease/burden** -- How much ongoing maintenance for the providing team?
5. **Reliance on authority** -- What happens if the sponsoring executive departs?
6. **Cultural alignment** -- Will the organization fight this at every step?

Effective mechanisms include:

**Approval and advice forums** -- Processes for handling edge cases where policy is unclear. The simplest form: exceptions are granted by a named individual in writing.

**Inspection** -- Mechanisms to evaluate whether a policy is succeeding and needs adjustment. Specify where and how data will be tracked. An inspection mechanism that can silently fail will accomplish nothing.

**Nudges** -- Providing individuals with context about a better way at exactly the moment it would be useful. At Stripe, nudges informed teams when their cloud spend accelerated, directing them to explanatory charts. Nudges are the most effective operational mechanism: they bring information to people exactly when it is useful.

**Automation** -- The most effective and scalable mechanism when paired with good user experience. At Uber, automation moved service provisioning from slow manual negotiations to structured requests.

**Deferral to future work** -- When you want a policy to do something but have no reasonable mechanism, explicitly defer. Acknowledge what is missing and clarify when you will return to it.

**Meetings** -- Universal but expensive. Good starting point but should be iterated toward cancellation.

Antipatterns: top-down pronouncements, education-as-announcement rollouts, mandatory recurring trainings, and "just change the culture." Each can provide some value but there is almost always a better alternative.

Non-executives should focus on mechanisms available to them -- nudges, building real datasets, and model-document-share -- rather than getting frustrated by what they cannot do.

**Cargo-culting** -- recreating a process without understanding the circumstances that made it effective -- is the largest threat to effective strategy operations.

### Chapter 11: Writing Readable Engineering Strategies

The order for writing a strategy (explore, diagnose, refine, set policy, operate) is a poor order for reading. Most strategy readers just want to understand the policy so they can apply it. Larson recommends inverting the structure for readability:

1. **Policy** -- What does the strategy require or allow?
2. **Operation** -- How is it enforced? How are exceptions granted?
3. **Refine** -- What load-bearing details informed the strategy?
4. **Diagnose** -- What general trends steered the thinking?
5. **Explore** -- What is the high-level context?

Strategy refactoring goes further: merge sections where it improves usability. The LLM adoption strategy merges Refine into Diagnose and discards a separate Operation section, folding operational details alongside their policies.

Additional tips: have someone uninvolved read the document before release; include an explicit commenting period and office hours; maintain your own strategy template with consistent metadata; disable in-document commenting after release to move discussion to a better forum.

### Chapter 12: Bridging Theory and Practice

The clean strategy documents in the book emerged from messy processes. Key practical challenges:

- **Unrealistic timelines** -- Deliver the best draft you can, then view yourself as starting the refinement process. Many strategies never leave refinement.
- **Using strategy as a non-executive** -- Effective diagnosis trumps authority. At least as many executive strategies are ravaged by reality as are overridden by higher-altitude strategies.
- **Chaotic environments** -- Strategies do not require stable environments; they require awareness of the environment. In dynamic periods, you might protect capacity in two-week chunks.
- **Unreliable information** -- Acknowledge what is missing and move forward where you can.
- **Surviving other people's bad strategy** -- Write a private strategy that acknowledges the imposed policy as a static, unavoidable truth, then make practical decisions within that context.

---

## Part III: Refinement Tools

### Chapter 13: Strategy Testing for Iterative Refinement

If Larson could popularize only one idea, it would be: prematurely rolling out a strategy prevents evaluating whether it is effective. Pressure changes behavior, creating the impression of compliance while minimizing actual change.

Strategy testing identifies the narrowest, deepest available slice and iterates until confident the approach works. As you iterate, identify impact metrics (not adoption metrics). Assume people mean well and failures are due to friction and ergonomics.

Two roles support testing:
- **Sponsor** -- Provides authority, makes quick decisions, marshals support, prevents scope creep. Must be genuinely authorized and available for rapid escalations.
- **Guide** -- Translates strategy into particulars, tracks workstreams, escalates issues. Must execute at pace without getting derailed.

The only absolute requirement: sponsor, guide, and key folks must meet every week. The meeting should be heavy on debugging and light on presentation.

Untested strategies sound right but do not accomplish much. The telltale sign is "pressure without a plan" -- a strategy that sounds correct but lacks concrete details. Identify these by asking: Are there numbers showing the strategy is driving desired impact? If the numbers are not moving, is there a clear mechanism for debugging?

Recovery from skipped testing requires writing a new strategy and not skipping testing this time. If you cannot officially pause a struggling strategy, find an indirect mechanism to pause it implicitly.

### Chapter 14: Systems Modeling

Systems modeling uses stocks (things that accumulate) and flows (changes to stocks) to understand complex systems cheaply and quickly.

It is most useful when:
1. You are unsure where leverage points might be in a complex system.
2. You have significant data to compare against.
3. Stakeholders' disagreements are based on unstated intuitions.

The modeling process:
1. Sketch stocks and flows on paper or in a diagramming tool.
2. Reason about how potential changes would shift flows.
3. Model in a spreadsheet or specialized tool, starting with the happy path, then exception paths.
4. Exercise the model with different starting values (sensitivity analysis).
5. Document what you learned, focusing on insights first.

Critical cautions:
- When your model and reality conflict, reality is always right.
- Models are immutable, but reality is not.
- Every model omits information; some omit critical information.
- Modeling is a tool to use in tandem with judgment, not a replacement for it.

### Chapter 15: Wardley Maps

Wardley mapping, created by Simon Wardley, ensures strategy is grounded in situational awareness. It is particularly effective at zooming out to understand broader ecosystems.

A Wardley map has three components:
- **Users** at the top, representing cohorts.
- **Needs** directly connected to users, representing tasks to accomplish.
- **Capabilities** connected to needs, representing underlying technical requirements.

The **x-axis** represents commoditization (genesis -> custom -> product -> commodity). The **y-axis** represents visibility to the user. Maps can also include **pipelines** (showing evolution over time), **overlays** (grouping capabilities by team or other attributes), and arrows indicating predicted future changes.

When to use Wardley maps: in highly dynamic environments, when your strategy spans five-plus years, or when any strategy is built on an evolving foundation. They are less helpful for detail-level optimization.

The mapping process:
1. Start small and iterate.
2. List users, needs, and capabilities.
3. Establish value chains connecting them.
4. Plot on a Wardley map.
5. Study the current state.
6. Predict how the map will evolve.
7. Study the future state.
8. Share for feedback.
9. Document what you learned.

Larson notes that Wardley's concepts of **doctrine** (universally applicable practices) and **gameplay** (context-dependent moves) are lightly specialized for business strategy and less directly applicable to engineering problems, which is why he focuses primarily on the mapping technique itself.

---

## Part IV: Case Studies

Ten concrete strategies, all based on Larson's direct experience, illustrate the framework in practice.

### Chapter 16: Service Migration Strategy (Uber)

In 2014, a four-engineer team at Uber was responsible for service provisioning while the organization doubled every six months. The team could not get more headcount. Their strategy used systems modeling to prove that manual provisioning could not scale, and that the only viable path was self-service provisioning.

Key policies: constrain manual provisioning to one engineer while investing in automation; make self-service safely usable by new hires; move to structured requests; prefer good defaults over requiring user input. Systems modeling showed that even eliminating all errors or increasing the team by 500% would not solve the backlog. Only self-service provisioning resolved it. The strategy scored 7/9 on the evaluation rubric.

### Chapter 17: LLM Adoption Strategy (Theoretical Ride Sharing)

A hypothetical ride-sharing company navigates LLM adoption through four documents covering policy, systems modeling, Wardley mapping, and driver onboarding modeling.

Key insight: through modeling the driver lifecycle, the company discovered that improving onboarding speed would have little impact on active drivers. The real leverage was reactivating departed and suspended drivers -- a counterintuitive finding that emerged directly from systems modeling.

The strategy starts with Anthropic as the sole LLM provider (through AWS Bedrock), mandates one developer productivity tool and one internal tooling initiative, and includes a six-month review cycle to learn before committing further.

### Chapter 18: Private Equity Ownership Strategy

A fictional "Fungible Ecommerce Company" prepares for private equity ownership with uncertain cost reduction targets. The strategy acknowledges the ambiguity and acts where it can:

- Move to an "N-1" backfill policy (backfill departures at a less senior level).
- Cap Principal Engineers at one per business unit.
- Continue existing infrastructure efficiency strategy.
- Prioritize post-acquisition infrastructure integration.
- Defer planning around reductions until specific targets arrive.

A systems model of the organization's seniority mix demonstrates that the N-1 policy combined with strict principal caps can reduce headcount costs by approximately 5% per year without layoffs.

### Chapter 19: Customer Data Access Strategy

An IPO-preparing company must strengthen controls around user data access. Previous security initiatives failed because they created friction that teams gradually subverted. The new strategy focuses on simultaneously improving security *and* usability:

- Prioritize mechanisms that both authorize and document rationales automatically.
- Measure progress on the percentage of access justified by user-comprehensible, automated rationales.
- Expose a log of data accesses to users themselves.
- Expire unused roles after 90 days.
- Weekly reviews until progress is clear, then monthly reviews.

The key insight: framing security as a tradeoff with usability is a sign you are having the wrong discussion.

### Chapter 20: Service Architecture Strategy (Theoretical Compliance Company)

A B2B compliance company debates whether to decompose its monolith. The diagnosis reveals complex business and engineering constraints: pressure to reduce platform spend, spinning up new business units, infrastructure that will not grow, and a Ruby codebase.

The policy: business units should operate in their own monoliths; new integrations should use gRPC; no new services except for new business units; merge existing services into business unit monoliths where possible. This is a strategy of *reversing* the decomposition trend.

### Chapter 21: Product Engineering Strategy (Calm)

Larson's first executive strategy work. Calm's engineering team was scattered between infrastructure ambitions, technology experimentation, and a stuck service decomposition. The strategy declared:

- "We are a product engineering company."
- All new code must be written in the monolith.
- New technologies are adopted only to create valuable product capabilities.
- Exceptions are granted by the CTO in writing.

A second document addresses resourcing Engineering-driven projects: only the team can manage the contents of their roadmap, because executives frequently override out-of-band instructions. The solution is team-level prioritization with explicit escalation paths.

### Chapter 22: Developer, API, and Acquisition Strategy (Stripe)

Four Stripe strategies demonstrate enduring, consistent approach over a decade:

1. **API deprecation** -- Stripe never deprecates APIs without unavoidable requirement. They maintain a translation layer to support all prior API versions from a single internal implementation. This is invisible externally but foundational to Stripe's business success, as API changes directly cause customer churn.

2. **Sorbet** -- Rather than decomposing the monolith or migrating to a typed language, Stripe built a custom static type checker for Ruby. This allowed a centralized team of ten engineers to gradually add types without distracting the larger organization. The strategy prioritized short-term product-engineering velocity over a potentially faster migration.

3. **Index acquisition integration** -- When Stripe acquired Index (a point-of-sale company), the strategy focused on launching a joint product within six months while deferring contentious decisions (like introducing Java to Stripe's stack). Escalations went to paired leads from both companies.

---

## Part V: Going Forward

### Chapter 23: Is This Strategy Any Good?

Larson introduces a three-question rubric for evaluating strategies:

1. **Speed (0-3 points)** -- How quickly can the strategy be refined? 3 for daily/weekly iteration, 2 for monthly, 1 for quarterly, 0 for longer.
2. **Cost (0-3 points)** -- How expensive is refinement? 3 for single-team implementation, 2 for small cross-team dependencies, 1 for large cross-team with flexible timing, 0 for large cross-team with rigid timing.
3. **Impact (0-3 points)** -- How well does the strategy solve its diagnosis? 3 for solving the full problem, 2 for the most essential portion, 1 for a simple portion, 0 otherwise.

A score of 6 or higher is a high-quality strategy. Below 6 warrants introspection.

Strategies exist across multiple phases, and a strategy that scores well in its first phase may degrade. Uber's service migration scored 7 in Phase 1 (solving the provisioning bottleneck) but 4 in Phase 2 (dealing with a sprawling service architecture).

**Stopping a strategy is often a good sign.** All strategies compete with strategies at other altitudes. Giving up on high-altitude strategies is almost always the right call unless there is a proven, highly impactful reason to maintain them.

**Evaluating other companies' strategies** is nearly impossible. The missing context is an impenetrable veil: you cannot know how many phases they went through, how much it cost, or whether their blog post reflects reality.

You can learn as much from failed strategies as from successful ones. Apply the rubric to each phase and determine where things went wrong.

### Chapter 24: How to Get Better at Strategy

Sources for learning:
- **Public resources** -- Engineering blogs, books, articles. Read between the lines.
- **Private resources** -- Your professional network. Most companies' strategies are available by asking.
- **Learning circles** -- Ongoing peer groups for bidirectional learning. The best mechanism Larson has found.

To practice:
- If existing strategies are not working, debug and fix one.
- If no strategies are documented, document one.
- If strategies have low adoption, iterate on operational mechanisms.
- If strategies are effective, find a new problem to work on.
- If you cannot share internally, practice with trusted external peers.

Track your work. Review quarterly with a peer. If you are not making progress, sit down with someone more experienced to debug.

If you believe you cannot do strategy in your current role, lower your altitude until you find a scale where you can operate. Only you can forbid yourself from developing personal strategies.

### Chapter 25: Strategy Resources

The appendix collects recommended resources including Larson's prior writing (*Staff Engineer*, *The Engineering Executive's Primer*), foundational strategy books (*Good Strategy, Bad Strategy*, *Thinking in Systems*, *Wardley Maps*), engineering-specific strategy books (*Technology Strategy Patterns*, *The Value Flywheel Effect*, *Architecture Modernization*), and public case studies from Intercom, Liberty Mutual, and Stripe.

---

## Key Themes and Takeaways

1. **There is always a strategy**, even if it is unwritten. Finding and documenting it is the first step toward improvement.

2. **The five-step process** (Explore, Diagnose, Refine, Set Policy, Operate) provides a repeatable structure. Skipping steps, especially refinement and operations, is the most common cause of failure.

3. **Refinement is the kernel of effective strategy.** Strategy testing, systems modeling, and Wardley mapping are the three primary tools. Use strategy testing for ambiguous problems, systems modeling for complex leverage analysis, and Wardley mapping for ecosystem evolution.

4. **Operations matter more than most strategists think.** Policies without operational mechanisms fade quietly. Nudges are the most effective mechanism; top-down pronouncements are the least.

5. **Write for readers, not writers.** Invert the document structure. Lead with policy and operations. The vast majority of readers just want to understand how to apply the strategy.

6. **Strategy is iterative, not waterfall.** Good strategies embrace change and are refined continuously. The best strategies support fast, cheap iteration.

7. **Anyone can do strategy.** Engineers can use "take five, then synthesize" and "model, document, share." Executives have more tools but fewer guardrails. The key is matching your approach to your authority level.

8. **The evaluation rubric** (Speed, Cost, Impact, scored 0-9) provides a structured way to assess strategy quality and identify where to improve.

9. **The details matter enormously.** The same general strategy that works at one company can fail at another. Copying strategies without understanding the diagnosis leads to cargo-culting.

10. **Engineering organizations routinely waste dozens or hundreds of years of their teams' lives by refusing to engage with the reality of their problems.** A bit of rigor in strategic thinking can change this -- and that is the bare minimum we owe ourselves, our colleagues, and our users.
