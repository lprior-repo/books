# Per-Book Best Practices — Lean Enterprise

> Deep dive into *Lean Enterprise: How High Performance Organizations Innovate at Scale* by Jez Humble, Joanne Molesky & Barry O'Reilly (O'Reilly, 2015). Tags: `#organization` `#leadership` `#strategy` `#innovation`.

**Author:** Jez Humble, Joanne Molesky & Barry O'Reilly
**Topic tags:** `#organization` `#leadership` `#strategy` `#innovation`
**Language focus:** Language-agnostic (organization / leadership / enterprise practice)
**Sources:** `markdown_output/Lean_Enterprise_How_High_Performance_Organizations_Innovate_at_Scale/Lean_Enterprise_How_High_Performance_Organizations_Innovate_at_Scale.md` · `summaries/Lean_Enterprise.md`

## TL;DR

Lean Enterprise is a unified, evidence-based playbook for building adaptive high-performance organizations that can *both* explore new business models *and* exploit validated ones at scale. The book stitches together Toyota Production System thinking, the Lean Startup build-measure-learn loop, Continuous Delivery, Mission Command, innovation accounting, governance/risk/compliance as a value stream, Beyond Budgeting financial management, and IT-as-product — all under a single common thread: treat the enterprise as a complex adaptive system, run disciplined experiments, and align through intent rather than control. Apply it when your enterprise must (a) rebalance a portfolio across horizons, (b) escape a project/water-scrum-fall trap, (c) grow or unblock an innovation culture, or (d) modernize governance, finance, and IT for a software-driven world.

---

## Best Practices by Topic

---

### 1. The Lean Enterprise Is Primarily a Human System

**Principle:** Culture — not tooling or process compliance — is the decisive factor in whether an organization can innovate and execute at scale.

**Do:**
- Treat culture as a measurable, modifiable system (Westrum typology: pathological / bureaucratic / generative) and shift reward signals toward cooperation, enquiry, and risk sharing.
- Study Toyota Production System as a *cultural* system (andon cord, jidoka, kaizen, genchi genbutsu) rather than copying its tools.
- Hire and grow people who thrive on mastery, autonomy, and purpose (Dan Pink's intrinsic motivators).
- Recognize that extrinsic rewards (bonuses, rating people, MBO) *reduce* performance on heuristic / creative work.

**Don't:**
- Mandate a methodology or toolchain and expect cultural change to follow.
- Treat NUMMI-style "andons on the wall" as the goal — Larry Spiegel's reflection on the GM copy: "There were too many people convinced that they didn't need to change."
- Assume "smart people" save you from a bad system — Deming: "A bad system will beat a good person every single time."

**Code (verbatim, Toyota's open-secret quote on learning faster than the thief):**
> "Certainly the thieves may be able to follow the design plans and produce a loom. But we are modifying and improving our looms every day. So by the time the thieves have produced a loom from the plans they stole, we will have already advanced well beyond that point. And *because they do not have the expertise gained from the failures it took to produce the original*, they will waste a great deal more time than us as they move to improve their loom."

**Reference diagram (paraphrased) — Westrum Table 1-1:**
- Pathological: low cooperation / messengers shot / responsibilities shirked / bridging discouraged / failure → scapegoating / novelty crushed.
- Bureaucratic: modest cooperation / messengers neglected / narrow responsibilities / bridging tolerated / failure → justice / novelty leads to problems.
- Generative: high cooperation / messengers trained / risks shared / bridging encouraged / failure → enquiry / novelty implemented.

*Ref: Lean_Enterprise.md — "Chapter 1: Introduction — A Lean Enterprise Is Primarily a Human System"*

---

### 2. Mission Command (Auftragstaktik) over Command and Control

**Principle:** Napoleon defeated the Prussians because his officers could decide locally; create alignment by communicating *intent* (what & why) and let teams decide *how*.

**Do:**
- Specify the *end state*, its *purpose*, and *minimum constraints* — not the detailed means (Donald Reinertsen's Principle of Mission).
- Apply the doctrine at multiple levels: budgeting, program management, process improvement, security, finance.
- Teach decision-makers how to write intent statements; budget for training, not for controls.
- Replace Napoleonic plan cascades with *catchball* — bidirectional translation of intent at each level.

**Don't:**
- Tell people "what to do" so often that "they will fail to do it when you aren't looking."
- Increase detail to fix the knowledge, alignment, and effects gaps — Bungay proves more detail makes complex adaptive systems *worse*.
- Treat command and control as "how the military works" — the modern military uses Mission Command because the 1806 Prussian defeat taught them the opposite.

**Code (verbatim quotes from von Moltke's 1869 *Guidance for Large Unit Commanders*):**
> "In war, circumstances change very rapidly, and it is rare indeed for directions which cover a long period of time in a lot of detail to be fully carried out."
> "The higher the level of command, the shorter and more general the orders should be. The next level down should add whatever further specification it feels to be necessary … an order should contain all, but also only, what subordinates cannot determine for themselves to achieve a particular purpose."

*Ref: Lean_Enterprise.md — "Chapter 1: Mission Command: An Alternative to Command and Control"*

---

### 3. Friction, Complex Adaptive Systems, and Three Gaps

**Principle:** Enterprises are CASs whose global behavior *emerges* from interactions; friction is irreducible, so don't try to engineer it away — design for it.

**Do:**
- Expect the three gaps that Bungay identifies (knowledge, alignment, effects) and reduce them through *direction* plus *feedback*, not more controls.
- Use the OODA loop (Observe–Orient–Decide–Act) as a thinking model and avoid the misreading that it must run sequentially and quickly.
- Use the Deming / PDCA cycle as the universal learning primitive — apply it to process, product, and culture.
- Develop *repertoire* (organizational implicit guidance) — the culture-internalized way to act that Boyd says determines whether you operate "inside" the competitor's loop.

**Don't:**
- Apply scientific management remedies (more detail, more rules, more controls) to a CAS — they make things worse.
- Treat orientation as a static briefing — it is "determined by a complex series of factors including our genetics, our habits and experiences, and the cultures within which we grew up and are currently operating."
- Forget that IGT (System 1) and conscious feed-forward (System 2) operate at the organizational level, not just the individual level.

**Code (Boyd, via Chet Richards, on what makes orientation win):**
> "The basic pattern is simple: An organization uses its better understanding of—clearer awareness of—the unfolding situation to set up its opponent by employing actions that fit with the opponent's expectations, which Boyd, following Sun Tzu, called the *zheng*. When the organization senses … that the time is ripe, it springs the *qi*, the unexpected, extremely rapidly. … The key idea is to emphasize implicit over explicit in order to gain a favorable mismatch in friction and time."

*Ref: Lean_Enterprise.md — "Chapter 1: Friction and Complex Adaptive Systems"*

---

### 4. Your People Are Your Competitive Advantage

**Principle:** In a knowledge economy, the long-term value of the enterprise is the capability to *continuously increase* value to customers, not the static asset base.

**Do:**
- Make "find, grow, keep" the central HR agenda; pay people for *learning ability*, not a list of skills.
- Operate from the premise that organizational culture dwarfs individual differences — even the 10× engineer debate is dwarfed by system effects.
- Reward *collaboration, system-level outcomes, and reduction of complexity* — never reward "dev complete" or "more code."
- Publish data on tenure, promotion rates, and job satisfaction by demographic; close gaps you find.

**Don't:**
- Hire only "purple squirrels" with exact skills — rapidly-learnable skills + growth mindset > memorized facts.
- Use stack-ranking, brainteasers, or test scores — Google found them "worthless as a criteria for hiring" and "don't predict anything."
- Punish failure — the authors quote Ackoff: "It's our treatment of error that leads to a stability which prevents significant change."

**Code (verbatim, Malcolm Gladwell, on the talent myth):**
> "The talent myth assumes that people make organizations smart. More often than not, it's the other way around…Our lives are so obviously enriched by individual brilliance. Groups don't write great novels, and a committee didn't come up with the theory of relativity. But companies work by different rules. They don't just create; they execute and compete and coordinate the efforts of many different people, and the organizations that are most successful at that task are the ones where the system is the star."

*Ref: Lean_Enterprise.md — "Chapter 1: Your People Are Your Competitive Advantage"*

---

### 5. Manage the Dynamics of the Enterprise Portfolio (Three Horizons)

**Principle:** Enterprises survive by *continuously* rebalancing exploration (H3), scaling (H2), and exploitation (H1) — and by *self-disrupting* their own franchises.

**Do:**
- Adopt Baghai's three-horizons model and Moore's growth/materiality matrix as the visible portfolio frame.
- Allocate intentionally (Google ~70/20/10; Intuit 60/30/10) and revisit the ratio with executive discipline.
- Fund teams and products, not projects (Google: 70% H1, 20% H2, 10% H3).
- Demand "balanced ambidexterity" — independent structures, compensation, and metrics for H3 — or spin out a maximally independent unit (Aetna's Healthagen).

**Don't:**
- Allow H1 managers' clout to silently cannibalize H2 and H3 budgets.
- Try to "acqui-hire" innovation into existence — placing horizon-3 startups into horizon-1 governance "breaks the people."
- Ignore Kodak's digital camera, Xerox PARC's GUI, Blockbuster's Netflix moment — past success is a liability, not an asset.

**Code (verbatim, Geoffrey Moore on the chasm):**
> "Geoffrey Moore, who introduced the concept of the 'chasm,' a logical divide between uptake by early adopters and the early majority. This chasm was inspired by Moore's observation that many innovations flounder once they are no longer seen as a source of competitive advantage by visionaries, but are not yet sufficiently established to be seen as a safe bet or proven practice by people in the early majority."

*Ref: Lean_Enterprise.md — "Chapter 2: Manage the Dynamics of the Enterprise Portfolio"*

---

### 6. Exploring New Ideas: Build-Measure-Learn in the Enterprise

**Principle:** Apply Eric Ries' Lean Startup loop *internally*: validate value and growth hypotheses before scaling; minimize investment in software while exploring.

**Do:**
- Use the value hypothesis ("does this solve a real problem the customer will pay to have solved?") and the growth hypothesis ("can we acquire customers rapidly and profitably?") as the dual gates.
- Run cheap experiments (MVPs) every week or two; treat every feature as a hypothesis.
- Apply the *Principle of Optionality* — limit downside per idea, expect most to fail, let a few pay off big.
- Promote to exploit only when product/market fit is achieved (not when executives are tired of waiting).

**Don't:**
- Mandate big up-front project plans for new products — "Most of these have low information value … the single most important unknown is whether the project will be cancelled" (Douglas Hubbard).
- Treat requirements as "the customer's requirements" — they are *hypotheses* you must test.
- Confuse an MVP's job (learning) with the job of a beta (engagement) — they are different.

**Code (verbatim, on Steve Blank's customer development stages):**
> "Once we have found a repeatable and scalable sales process—in other words, if our customer base can rapidly move up the 'hockey stick' … and whether we have a sufficiently low customer acquisition cost. If we pass these tests, we have a *product/market fit* and can proceed to the final two stages in Steve Blank's customer development process: *customer creation*, where we launch our business in earnest, followed by *company building* where we attempt to cross the chasm."

*Ref: Lean_Enterprise.md — "Chapter 2: Exploring New Ideas"*

---

### 7. Effectuation: The Logic of Expert Entrepreneurs

**Principle:** Real entrepreneurs reason from *means* (not goals) and create options through commitments — a countermeasure to HiPPO-driven causal planning.

**Do:**
- Apply the five effectuation principles: Bird-in-Hand, Affordable Loss, Crazy Quilt, Lemonade (leverage contingency), Pilot-in-the-Plane.
- Pre-commit to resource caps per idea ("affordable loss"), so failure is bounded and learning is the upside.
- Use constraints (people, money, time) as catalysts for creativity — Herman Hauser's ARM story: "no money and no people — they had to keep it simple."
- Form "crazy quilt" partnerships with stakeholders willing to commit — co-create with customers and suppliers.

**Don't:**
- Start with a market-size goal and back-solve resources — that's causal reasoning that fails in uncertainty.
- Allow senior stakeholders to rewrite your affordable-loss cap midstream.
- Forget that effectuation complements, not replaces, causation — use each in the right domain.

**Code (verbatim, Hauser on the ARM CPU):**
> "When we decided to do a microprocessor, in hindsight, I think I made two great decisions. I trusted the team, and gave them two things that Intel and Motorola had never given their people: the first was no money and the second was no people. They had to keep it simple."

*Ref: Lean_Enterprise.md — "Chapter 2: Effectuation (Tip box)"*

---

### 8. Minimize Software Investment While Exploring

**Principle:** When validating business models, *do not* pre-invest in scalable software. Use Concierge, Wizard of Oz, landing pages, and mockups.

**Do:**
- Hard-code country-specific tax and currency logic on a mainframe for a single store — the 8-week integration estimate was a multi-month boondoggle until they tried cheap options.
- Use JustGiving's pattern: prototyped sessions → concierge launch → validate repeatable business model → automate only after traction.
- Recognize that in a fully equipped internal IT department the most expensive asset is *wait time*, not code.
- Reuse operational excellence "tools" (kanban, value stream, continuous delivery) on the validation pipeline, not on the production system.

**Don't:**
- Confuse the prototype with the production system — they're optimized for different things (learning vs. reliability).
- Run a six-month internal COTS evaluation before talking to a real pilot user.
- Treat exploratory prototypes as "real" code — accumulate technical debt deliberately, pay it down only after validation.

**Code (verbatim, the 2008 retail international expansion):**
> "One large retail organization we worked with wanted to open a store in a new market—their first international expansion. The IT team were given eight weeks to adapt their point-of-sale system to work in the new country, calculating a different sales tax and using a different currency. We estimated that changing the existing system to work in multiple currencies and tax regimes would be a substantial multi-month IT project requiring significant investment. Forced to seek options to validate that the solution was actually possible, the team hard-coded the new sales tax into the existing mainframe system and implemented a simple proxy that replaced the currency symbols in real time for systems in the new store."

*Ref: Lean_Enterprise.md — "Chapter 2: When Exploring New Business Models, Minimize Investment in Software Development"*

---

### 9. Balancing the Enterprise Portfolio with Economics, Not HiPPO

**Principle:** Replace opinion-driven prioritization with an economic model that exposes *cost of delay*.

**Do:**
- Forbid "decision by HiPPO" (Highest-Paid-Person's-Opinion) — only 24% of firms use an economic model, 13% admit HiPPO drives decisions, 47% rely on committees.
- Use CD3 (Cost of Delay Divided by Duration) to schedule work; smaller batches *raise* the CD3 score.
- Recognize that H2 businesses are starved by H1's corporate clout; protect them with separate management, capital, and metrics.
- Define explicit cross-horizon transition criteria (problem/solution fit → product/market fit → scale).

**Don't:**
- Let a 47% "decision-by-committee" outcome be celebrated as "alignment."
- Continue funding H2 businesses with H1 metrics — they require fundamentally different talent.
- Confuse "we've shipped it" with product/market fit — that's when H2 *begins*, not ends.

**Code (verbatim, Ronny's "humbling statistics"):**
> "Ronny Kohavi … reveals the 'humbling statistics': 60%–90% of ideas *do not improve the metrics they were intended to improve*. Based on experiments at Microsoft, 1/3 of ideas created a statistically significant positive change, 1/3 produced no statistically significant difference, and 1/3 created a statistically significant negative change. *All* of the ideas tested were thought to be good ones—but neither intuition nor expert opinion are good gauges of the value our ideas have for users."

*Ref: Lean_Enterprise.md — "Chapter 2: Balancing the Enterprise Portfolio"*

---

### 10. Model Investment Risk with Measurement and EVI

**Principle:** Apply the scientific method to product development: hypothesize → experiment → analyze → pivot/persevere.

**Do:**
- Replace "requirements" with *hypotheses* — *"We believe that [target customer] has [problem] and will use [solution]."*
- Use *Expected Value of Information* (EVI) to cap how much to spend on reducing uncertainty: EVI = P(wrong) × cost-of-being-wrong.
- Run a Monte Carlo simulation on every business case; expect the result distribution to be wide and skewed.
- Treat "is the project cancelled?" and "system utilization?" as the two variables with the highest information value — not developer hours.

**Don't:**
- Spend weeks estimating development hours for a project that will be killed in two weeks for a business reason.
- Confuse precision with accuracy — a 1-meter GPS reading is more accurate than a 500-mile one, regardless of decimal places.
- Plan detailed requirements for *non-trivial* features — they are hypotheses.

**Code (verbatim, Hubbard on the IT measurement inversion):**
> "The vast majority of variables had an information value of zero… The variables that had high information values were routinely those that the client never measured. 3) The variables that clients used to spend the most time measuring were usually those with a very low … information value."
> "Even in projects with very uncertain development costs, we haven't found that those costs have a significant information value for the investment decision… The single most important unknown is whether the project will be canceled… The next most important variable is utilization of the system."

*Ref: Lean_Enterprise.md — "Chapter 3: Model and Measure Investment Risk"*

---

### 11. Apply Lean Startup Internally (Every Endeavor)

**Principle:** Lean Startup is not just for startups — every internal system, tool, process, or methodology adoption is an experiment.

**Do:**
- For every internal investment (process change, tool, COTS, methodology), state the *measurable downstream customer outcome* first.
- Find a pilot team willing to *opt in* — never mandate.
- Time-box ruthlessly (days to weeks, not months) for the MVP; success = "users use it voluntarily."
- Run MVPs on COTS by deploying the package to *one* team and measuring their outcome.

**Don't:**
- Mandate internal tools — "mandating the use of a particular solution makes it much harder to gather feedback."
- Treat "the perfect tool" as a goal — the perfect tool for one team is wrong for another.
- Allow the MVP to become the production system before the experiment is complete.

**Code (verbatim, on internal tooling MVPs):**
> "For an internal test automation tool, we might aim to reduce the lead time for full regression testing to 8 hours. … To determine if we have a problem/solution fit, we look for a customer willing to work with us to pilot the new system, tool, process, or software. This is a critical step which is often skipped by enterprises. Indeed for internal tools it's common to *mandate* their use—a disastrous policy which often results in enormous amounts of waste, unhappy users, and little value to the organization."

*Ref: Lean_Enterprise.md — "Chapter 3: Applying the Lean Startup Approach Internally Within Enterprises"*

---

### 12. Principles for Exploration

**Principle:** Five non-negotiable rules for any exploration in conditions of uncertainty.

**Do:**
1. Focus on outcomes, not outputs — measure value created, not features delivered.
2. Start with the customer — *discover* need before designing solutions.
3. Hypothesize, experiment, learn — every feature is a hypothesis.
4. Fail fast, learn faster — the goal of failure is *learning*, not blame.
5. Minimize the cost of learning — use the cheapest possible experiment.

**Don't:**
- Celebrate "shipping features" as the success metric.
- Treat "we always knew this would work" as evidence — Deming: "whenever there is fear, you get the wrong numbers."
- Use a one-time big launch as the validation event.

*Ref: Lean_Enterprise.md — "Chapter 3: Principles for Exploration"*

---

### 13. Discovery: Lean Startup + Design Thinking at the Front Door

**Principle:** *Discovery* is a rapid, time-boxed, iterative set of activities that fuses design thinking and Lean Startup.

**Do:**
- Form small, cross-functional, multi-disciplinary, dedicated, co-located teams — they own delivery.
- Build a *shared understanding* of the problem before arguing about solutions (Saint-Exupéry: "do not begin by gathering wood … awaken within the heart of man the desire for the vast and endless sea").
- Use Gamestorming techniques and visual artefacts to externalize ideas; depersonalize debate.
- Distinguish *customers* (pay) from *users* (use and co-create); engage both.

**Don't:**
- Assume "everyone knows the problem" — quality of the problem statement drives solution quality.
- Use a 30-person Discovery workshop and call it "lean."
- Skip the divergent phase — "If you want to have good ideas you must have many ideas" (Pauling).

**Code (verbatim, from lastminute.com):**
> "For two days, they ran co-creation workshops that generated over 80 new ideas for online products aligned to their business goals. The team then set up an innovation lab in a hotel lobby for a week, rapidly experimenting with each idea to discard it or validate it as a viable customer problem to implement. Within days, the team identified three winning ideas to invest further effort in developing—resulting in an over 100 percent increase in conversion for their product."

*Ref: Lean_Enterprise.md — "Chapter 4: Discovery"*

---

### 14. The Business Model Canvas and Strategic Mastery

**Principle:** Make the business hypothesis visible and debateable; pick a "level of strategy" deliberately.

**Do:**
- Populate all nine blocks of the Business Model Canvas (CS, VP, channels, relationships, activities, resources, partnerships, cost, revenue) — each is a hypothesis.
- Time-box canvas exercises to 30 minutes — speed beats precision at the explore stage.
- Choose your strategy level explicitly: Level 0 (Oblivious), Level 1 (Beginner), Level 2 (Master), Level 3 (Invincible).
- Augment with Lean Canvas (assumes PMF is the riskiest hypothesis), Opportunity Canvas, or Value Proposition Canvas as appropriate.

**Don't:**
- Write a 50-page business plan before talking to a customer.
- Assume you already know which assumption is riskiest — test it.
- Skip the *cost structure* block — the most expensive hidden assumption is often *how* you pay for it.

*Ref: Lean_Enterprise.md — "Chapter 4: Understanding Our Business Problem to Inform Our Business Plan"*

---

### 15. Understand Customers and Users (Personas, Empathy, Insights)

**Principle:** Put a face on the customer; empathy + data + experiments win over opinions.

**Do:**
- Iterate personas quickly; "the most objective measure of how valuable our solution is or can be" comes from real users.
- Practice *genchi genbutsu* / *getting out of the building* — observe, interview, and co-create in their context.
- Use big-data analytics to *invert* discovery — look at how customers actually behave before asking what they want.
- Beware confirmation bias (System 1 IGT) — your IGT shapes what you observe.

**Don't:**
- Build "luxury personas" with demographic depth that no one reads.
- Treat analytics as a replacement for empathy — "Data, like a flashlight, is only as useful as the person wielding it."
- Ask leading questions or use language your customers wouldn't.

**Code (verbatim, the Royal Pharmaceutical Society):**
> "The Royal Pharmaceutical Society knew that their clinical drug database was the best in the world. They also knew that there must be many more uses for it than just a stack of printed books. But where should they start? Instead of guessing, or building an expensive platform for products, or trying to sign a deal without a product, they used their other major asset: a building full of pharmacists. … By starting with an app that they themselves would use, they were able to understand what international customers might want and to build a great marketing tool."

*Ref: Lean_Enterprise.md — "Chapter 4: Understanding Our Customers and Users"*

---

### 16. MVPs: The Right Tool for the Right Question

**Principle:** Match MVP type to what you need to learn — and remember Marty Cagan's three properties: valuable, usable, feasible (+ delightful).

**Do:**
- Use Paper / Interactive prototypes to test design and usability cheaply.
- Use *Concierge* MVPs to validate qualitative assumptions with minimal code (Airbnb's air beds, JustGiving's YIMBY).
- Use *Wizard of Oz* MVPs to validate a working solution behind a human (Zappos buying shoes for customers).
- Use *Micro-niche* and *Working software* MVPs only when you need real customer behavior.
- Clarify MVP definition up front — Ries' MVP ≠ Cagan's MVP ≠ "any validation activity."

**Don't:**
- Wait for a fully integrated release candidate to gather learning.
- Treat "feature completeness" as the MVP definition.
- Conflate MVP with beta or public launch.

**Code (verbatim, on the MVP definition debate):**
> "Confusingly, people often refer to any validation activity anywhere along on this spectrum as an MVP, overloading the term and understanding of it in the organization or wider industry. Marty Cagan … notably uses the term 'MVP test' to refer to what Eric Ries calls an MVP. Cagan defines an MVP as 'the smallest possible product that has three critical characteristics: people choose to use it or buy it; people can figure out how to use it; and we can deliver it when we need it with the resources available—also known as valuable, usable, and feasible,' to which we add 'delightful.'"

*Ref: Lean_Enterprise.md — "Chapter 4: Accelerate Experimentation with MVPs"*

---

### 17. The One Metric That Matters (OMTM)

**Principle:** At any moment, *one* metric drives decisions — and it changes as you learn.

**Do:**
- Pick a *leading* metric tied to your riskiest hypothesis (not lagging ROI).
- Choose stage-appropriate metrics: empathy (qual), stickiness (retention), virality (K-factor), revenue (LTV/CAC), scale (CAC vs growth).
- Optimize for *customer lifetime value* (Kohavi's recommendation), not short-term revenue.
- Use OMTM to focus conversations, surface problems, and stimulate improvement.

**Don't:**
- Track 30 KPIs at once — that signals you have no priority.
- Optimize for lagging indicators in early stages — you need leading signals.
- Stick with an OMTM that has outlived its useful life.

**Code (verbatim, on LinkedIn's metric discipline):**
> "As a good example of OMTM, at LinkedIn, the team does not talk about 'total page views' but only 'profile views'—the number of people using LinkedIn who search for and find other people, and the number of LinkedIn profiles they viewed."

*Ref: Lean_Enterprise.md — "Chapter 4: The One Metric That Matters"*

---

### 18. Innovation Accounting: Stop Measuring Outputs, Start Measuring Learning

**Principle:** Traditional financial KPIs kill early-stage innovation; use innovation accounting instead.

**Do:**
- Use the three-step loop: establish baseline → tune the engine → pivot or persevere.
- Replace *vanity metrics* (raw page views, raw downloads) with *actionable metrics* (cohort conversion, retention, activation).
- Use pirate metrics (AARRR) by *cohort*, not by aggregate.
- Track customer acquisition cost, viral coefficient (K), CLV, and monthly burn rate for H3 businesses.
- Hold a regular (weekly/fortnightly) review meeting with external stakeholders to challenge progress.

**Don't:**
- Demand ROI from a Horizon 3 idea before it has product/market fit.
- Compare team velocities across teams — they're not designed for that.
- Use number-of-trained-people as a measure of capability.

**Code (verbatim, vanity vs. actionable):**
> "Number of visits. Is this one person who visits a hundred times, or a hundred people visiting once? → Funnel metrics, cohort analysis. We define the steps of our conversion funnel, then group users and track their usage lifecycle over time."

*Ref: Lean_Enterprise.md — "Chapter 5: Innovation Accounting"*

---

### 19. Energize Internal Advocates and Do Things That Don't Scale

**Principle:** Inside the enterprise, you must *manufacture* allies — early adopters who are willing to back a winner.

**Do:**
- Seek out people who are "frustrated and curious for change" and give them cover, context, and confidence.
- Create visible, early wins to build momentum.
- Tell compelling stories that connect innovation to business outcomes.
- "Do things that don't scale" — manually onboard first customers, hand-craft first solutions.
- Develop customer intimacy by *deliberately* narrowing your market.

**Don't:**
- Mistake political maneuvering for advocacy — advocates stand up when it costs them.
- Automate what you should still be learning from.
- Force wide adoption before you have advocates.

**Code (verbatim, on intra-enterprise energy):**
> "Energizing and engaging these people is key. As they become early adopters of our ideas and initiatives, they will provide a feedback loop enabling us to iterate and improve our product. They are also our sponsors within the wider organization. In bureaucratic environments, people tend to protect their personal brand and not back the losing horse. Our goal is to give them the confidence, resources, and evidence that encourages them to be advocates for our initiative throughout the organization."

*Ref: Lean_Enterprise.md — "Chapter 5: Energizing Internal Advocates in the Enterprise"*

---

### 20. Build a Runway of Questions, Not Requirements

**Principle:** Replace the requirements backlog with a *hypothesis backlog*.

**Do:**
- Write your runway as questions to answer, not features to build.
- Use Story Maps (Jeff Patton) to externalize the *narrative* of your vision — backbone + skeleton.
- Continually ask "what is the riskiest assumption right now?" and design the smallest experiment to test it.
- Hardening, integration, and automation kick in *after* validation — not before.

**Don't:**
- Pre-commit to a release plan before you have validated learning.
- Hire a full team for a feature you're still testing.
- Let "completeness" of the story map become a vanity proxy.

**Code (verbatim, Patton via the book):**
> "Story maps help with planning and prioritizing by visualizing the solution as a whole. Story mapping is not designed to generate stories or create a release plan—it is about understanding customers' objectives and jobs-to-be-done. Story maps provide an effective means to communicate the narrative of our solution to engage the team and wider stakeholders and get their feedback."

*Ref: Lean_Enterprise.md — "Chapter 5: Build a Runway of Questions, Not Requirements"*

---

### 21. Engineering Practices for Exploration

**Principle:** Even in exploration, two practices pay for themselves later: continuous integration and a *small* set of user-journey tests.

**Do:**
- Prudently accumulate technical debt in the MVP phase (Fowler's Technical Debt Quadrant).
- The moment the feature is *validated*, kill momentum and switch to TDD, modularization, and aggressive refactoring.
- Hire engineers with the discipline to switch gears — "embarrassingly crappy code" → "battle-tested code."

**Don't:**
- Spend weeks building acceptance tests for an unvalidated idea.
- Refactor your MVP into a rewrite during the exploration phase.
- Confuse "exploring quickly" with "no engineering discipline" — CI is non-negotiable from day one.

**Code (verbatim, Fowler via the book):**
> "When we start working on validating a new product idea or a new feature in an existing product, we want to try out as many ideas as fast as possible. Ideally we will do this without writing any software at all. But for the software we do write, we don't want to spend a ton of time building acceptance tests and refactoring our code. We will (as Martin Fowler puts it) deliberately and prudently accumulate technical debt in order to run experiments and get validation."

*Ref: Lean_Enterprise.md — "Chapter 5: Engineering Practices for Exploring"*

---

### 22. Engines of Growth (Viral, Paid, Sticky, Expand, Platform)

**Principle:** Every product must pick a growth engine explicitly — without one, you have none.

**Do:**
- *Viral* — design so customer usage *necessarily* invites others (Facebook, PayPal); measure K-factor.
- *Paid* — measure the spread between LTV and blended CAC (Amazon, Netflix).
- *Sticky* — minimize churn; exponential growth follows (eBay).
- *Expand* — sequence geography, category, and adjacency (Amazon: books → everything).
- *Platform* — open an ecosystem around a successful core (MS Windows, App Store, Salesforce).

**Don't:**
- Run all five engines at once — pick one.
- Measure growth without a matching engine strategy.
- Assume growth is "the team's job" — it's a *product* property.

*Ref: Lean_Enterprise.md — "Chapter 5: Engines of Growth"*

---

### 23. Transitioning Between Horizons (Explore → Exploit)

**Principle:** Crossing the chasm requires a *metamorphosis* of skills, metrics, and management — not just a bigger budget.

**Do:**
- Define explicit criteria for promotion: problem/solution fit → product/market fit → scale.
- Keep the team together as you scale to protect culture and tacit knowledge.
- "Contain the fire" with alpha/beta cohorts; broaden only after success.
- Use the five growth enablers (market, monetization, customer adoption, no-big-bang, team engagement) as a checklist.

**Don't:**
- Hire a sales team before product/market fit.
- Replace the discovery team with operators — you'll lose the culture.
- Force a single customer's pricing concessions into the product — that limits later growth.

**Code (verbatim, Amazon Marketplace):**
> "Amazon auctions (later known as zShops) were launched in March 1999 in response to the success of eBay. … Despite the promotion, one year after launch it had only achieved a 3.2% share of the online auction market compared to 58% for eBay, and subsequently declined. … In November 2000, zShops was renamed to 'Amazon Marketplace' … In 2012, Amazon's Marketplace service produced 12% of revenues with total unit sales increasing 32% from the previous year."

*Ref: Lean_Enterprise.md — "Chapter 5: Transitioning Between Horizons to Grow and Transform"*

---

### 24. Deploy the Improvement Kata at Scale

**Principle:** The Improvement Kata (Mike Rother) is a *meta-methodology* — a routine of routines for working under uncertainty.

**Do:**
- Run the four-step cycle daily: understand direction → grasp current condition → establish target condition → experiment via PDCA.
- Ask the five daily questions (target / actual / obstacles / next step / when we'll go see).
- Use SMART, 1-week-to-3-month target conditions; prefer shorter for beginners.
- Pair with the *Coaching Kata* so managers learn to develop people, not dictate.

**Don't:**
- Treat the Improvement Kata as a methodology to install — it's a pattern to practice.
- Skip the discipline of PDCA cycles or run them too slowly.
- Assume 100% achievement of target conditions — in a generative culture we *expect* to miss some.

**Code (verbatim, Mike Rother):**
> "The Improvement Kata, as described by Mike Rother, is a general-purpose framework and a set of practice routines for reaching goals where the path to the goal is uncertain. It requires us to proceed by iterative, incremental steps, using very rapid cycles of experimentation. Following the Improvement Kata also increases the capabilities and skills of the people doing the work, because it requires them to solve their own problems through a process of continuous experimentation."

*Ref: Lean_Enterprise.md — "Chapter 6: Deploy Continuous Improvement"*

---

### 25. Activity Accounting Reveals Waste (HP LaserJet Case Study)

**Principle:** Don't argue about waste — measure it. Activity accounting shows where the money actually goes.

**Do:**
- Snapshot where engineering time and money are spent — code integration, planning, porting, support, manual testing, innovation.
- Track "failure demand" (Seddon) vs "value demand" separately — a 25% support line item screams "build quality in."
- Use activity accounting to make improvement work *visible* — otherwise it gets crowded out.
- Adopt the Improvement Kata to migrate spend toward innovation (HP went from 5% → 40% innovation spend).

**Don't:**
- Trust teams that say "we don't have waste" — show them the data.
- Treat activity accounting as a one-time audit — repeat it annually.
- Increase utilization past the point of no slack; improvement work needs *slack*.

**Code (verbatim, HP FutureSmart before/after):**
- 2008: 10% CI, 20% planning, 25% branch porting, 25% support, 15% manual test, 5% innovation.
- 2011: 2% CI, 5% agile planning, 15% one branch, 10% support, 5% manual test, 23% test automation, **~40% innovation**.
- Outcomes: ~40% cost reduction, ~140% more programs, 78% lower per-program cost, 8× innovation spend.

*Ref: Lean_Enterprise.md — "Chapter 6: The HP LaserJet Firmware Case Study"*

---

### 26. Manage Demand Through WIP-Limited Kanban and Programs

**Principle:** Improvement work is squeezed out by demand unless you *manage* demand at the program level.

**Do:**
- Use program-level target velocity (HP FutureSmart) as a WIP limit — accept work only up to that target per iteration.
- Set WIP limits per process block *and* per queue — make the pain visible.
- Coordinate cross-cutting work through *virtual feature teams* (HP FutureSmart pattern).
- Use the dynamic priority list (Maersk) instead of project batches — pull the highest-CDV item when capacity is free.

**Don't:**
- Compare team velocities across teams — they're designed to compare a team to *itself*.
- Allow product marketing to bypass the program-level process and feed work directly to teams.
- Punish managers for not meeting targets — instead, use metrics as a conversation starter ("Management by Wandering Around").

**Code (verbatim, HP on metric misuse):**
> "Specifying a target velocity at the program level does *not* require that we attempt to measure or manage velocity at the team level, or that teams must use Scrum. … In any case, it doesn't matter how many stories we complete if we don't achieve the business outcomes we set out to achieve in the form of program-level target conditions."

*Ref: Lean_Enterprise.md — "Chapter 6: Managing Demand"*

---

### 27. Make the Enterprise Agile, Not Small Teams in a Big Enterprise

**Principle:** Scaling agile is not "more Scrum" — it's evolving the *enterprise* under agile principles.

**Do:**
- Let teams choose and evolve their own methodologies, as long as they hit program-level target conditions (HP FutureSmart).
- Move metrics from control to *conversation* — "we use the metrics to understand where to have conversations about what is not getting done" (Gruver).
- Pair "Management by Wandering Around" with gemba walks.
- Take *small bites* every iteration — Apple Macintosh team showed weekly hardware/OS/integration demos.

**Don't:**
- Impose Scrum on every team — HP FutureSmart deliberately didn't.
- Treat process compliance as the goal — the goal is outcomes.
- Standardize for standardization's sake — process should adapt to obstacles.

*Ref: Lean_Enterprise.md — "Chapter 6: Creating an Agile Enterprise"*

---

### 28. Identify Value and Map Value Streams

**Principle:** Lean thinking distilled into five principles: *precisely specify value, identify the value stream, make value flow, let the customer pull, pursue perfection* (Womack & Jones).

**Do:**
- Run a value stream mapping workshop with 5–15 process blocks; gather 1–3 days; include all stakeholders including authorizers.
- Capture Lead Time, Process Time, and %C/A per process block; calculate flow efficiency (PT/LT).
- Compute the *true* %C/A — rework is the biggest hidden waste.
- Build a future-state VSM that *radically* challenges the current state; don't accept local optimization.
- Use the current/future-state VSM as the Improvement Kata's challenge.

**Don't:**
- Map a value stream without the people who actually do the work — the data must come from the gemba.
- Hide rework behind idealized numbers.
- Optimize a single block — it rarely moves the overall.

**Code (verbatim, Maersk):**
> "In 2010, median lead time for a feature was 150 days, with 24% of requirements taking over a year to deliver (from conception to software in production). At the point of analysis, in October 2010, more than 2/3 of the 4,674 requirements identified as being in process were in the 'fuzzy front end,' waiting to be analyzed in detail and funded. In one case, 'a feature that took only 82 hours to develop and test took a total of 46 weeks to deliver end-to-end. Waiting time consumed over 38 weeks of this.'"

*Ref: Lean_Enterprise.md — "Chapter 7: Identify Value and Increase Flow"*

---

### 29. Limit WIP — Little's Law in Action

**Principle:** WIP limits are the single most powerful lever for increasing flow.

**Do:**
- Apply Little's Law (Lead Time = WIP / Throughput): reducing WIP *mathematically* reduces lead time.
- Make WIP limits *hurt* — the pain reveals systemic problems.
- Use Kanban Method's practices: visualize, limit WIP, define classes of service, create pull, hold operational reviews.
- Follow Kanban's four principles: start with what you do now, agree to evolutionary change, respect current roles, encourage leadership at all levels.

**Don't:**
- Relax WIP limits to relieve short-term pressure — address the systemic blocker.
- Assign people to multiple projects — context switching destroys throughput and quality.
- Aim for 100% utilization — slack is required for improvement.

**Code (verbatim, on WIP-limits-hurt):**
> "Part of the purpose of WIP limits is to reveal opportunities for improvement. Imposing WIP limits will focus attention on work which is blocked or hard to complete, since our inability to complete it prevents us picking up new work. At this point, it's tempting to relax WIP limits to make sure 'something is getting done.' It's essential to avoid this temptation and address the sources of the problem instead."

*Ref: Lean_Enterprise.md — "Chapter 7: Limit Work in Process"*

---

### 30. Cost of Delay (CoD) and CD3 — Decentralize Economic Decisions

**Principle:** Quantify the *time value* of work so teams can make transparent prioritization decisions without command-and-control.

**Do:**
- Calculate CoD for every feature — even rough dollar estimates reveal assumptions.
- Use *CD3 = CoD / Duration* to push work toward smaller batches (smaller batches raise CD3).
- Match work to urgency profiles (constant / deadline-driven / use-it-or-lose-it).
- Restructure the PMO's role from "deciding" to "creating the framework for decisions."
- Surface and *validate* the assumptions behind CoD — that's where the real conversation happens.

**Don't:**
- Use CoD as a heavyweight process sitting alongside existing prioritization — kill the old process.
- Pretend CoD works on small queues — its payoff is largest when queues are large.
- Confuse precision with accuracy; "aim for accuracy, not precision" — Hubbard.
- Default to "MoSCoW" without the underlying dollars.

**Code (verbatim, Maersk CD3 outcome):**
> "By July 2011, median cycle time had been reduced by about 50% on the two services piloted. (One of the pilot services was a centralized SAP accounting system.) Arnold and Yüce present two factors causing the reduction in cycle time: increased urgency generated by the Cost of Delay calculation exercises, and decreased batch size caused by people breaking work into smaller chunks to increase the CD3. Furthermore, customer satisfaction increased significantly on the pilot projects."

*Ref: Lean_Enterprise.md — "Chapter 7: Cost of Delay: A Framework for Decentralizing Economic Decisions"*

---

### 31. Continuous Delivery (CD): Safe, Quickly, Sustainably

**Principle:** Continuous Delivery is the ability to get changes of all types into production *safely, quickly, and sustainably*.

**Do:**
- Keep *everything* in version control (code, config, infra, tests, deployment scripts).
- Automate everything: builds, tests, deployments, infrastructure.
- Build quality in — automated tests at every layer.
- Apply the two golden rules: (1) "done" = on trunk + releasable + (for features) tested on real users; (2) prioritize keeping the system in a deployable state.
- Decouple *deployment* (technical decision) from *release* (business decision).

**Don't:**
- Aim for "deploy to production multiple times a day" — that's an effect, not a goal.
- Let "release" and "deployment" be synonyms — that injects politics into ops.
- Hide bad changes — *anyone* can revert (Google's rule).

**Code (verbatim, Amazon's deployment cadence):**
> "In May of 2011, Amazon achieved a mean time between deployments *to production systems* of 11.6 seconds, with up to 1,079 such deployments in a single hour, aggregated across the thousands of services that comprise Amazon's platform. Some of these deployments affected upwards of 10,000 hosts. Amazon, of course, is subject to regulations such as Sarbanes-Oxley and PCI-DSS."

*Ref: Lean_Enterprise.md — "Chapter 8: Adopt Lean Engineering Practices"*

---

### 32. Trunk-Based Development, CI, and Test Automation

**Principle:** Continuous integration is the *single most important* technical practice in the agile canon.

**Do:**
- Require all developers to commit into trunk *at least daily* (trunk-based development).
- Trigger an automated build + test on every change; give feedback in minutes.
- *Anyone* can revert a bad change — system working > new work.
- Build small, fast, reliable test suites; design for parallelization.
- Co-locate testers and developers — testing skills + dev skills = maintainable suites.

**Don't:**
- Tolerate long-lived branches at scale — they end in integration hell.
- Write flaky tests — better to delete them.
- Automate test coverage for *experiments* — only for validated features.
- Test in a "dev complete" vacuum — optimize for *overall* lead time, not "done-in-isolation."

**Code (verbatim, Google's CI scale):**
> "Almost all of Google's 10,000+ developers distributed over 40 offices work off a single code tree. Everyone working off this tree develops and releases from trunk, and all builds are created from source. 20 to 60 code changes are submitted every minute, and 50% of the codebase changes every month. Google engineers have built a powerful continuous integration system that, in 2012, was running over 4,000 builds and 10 million test suites (approximately 60 million tests) every day."

*Ref: Lean_Enterprise.md — "Chapter 8: Continuous Integration and Test Automation"*

---

### 33. The Deployment Pipeline as Audit Trail

**Principle:** The deployment pipeline is the *system of record* for every change — and your compliance gift.

**Do:**
- Move every change (code, schema, config, infra) through version control → pipeline → environments.
- Use the pipeline as a *lightweight change control* process (ITIL "standard changes").
- Capture metrics from the pipeline: cycle time, mean, standard deviation, bottlenecks.
- Use it as the audit trail for compliance — "every command, every box, who approved."

**Don't:**
- Run manual deployment steps — they defeat the purpose of the pipeline.
- Skip pipeline stages "because we trust the developer" — even good code needs guardrails.
- Treat the deployment pipeline as a developer tool only — it's a compliance tool too.

**Code (verbatim, FutureSmart scale):**
> "The FutureSmart team's deployment pipeline allows a 400-person distributed team to integrate 100–150 changes—about 75–100 *thousand* lines of code—into trunk on their 10-million-line codebase every day. Each day, the deployment pipeline produces 10–14 good builds of the firmware out of Level 1."

*Ref: Lean_Enterprise.md — "Chapter 8: The Deployment Pipeline"*

---

### 34. Decouple Deployment and Release (Blue-Green, Canary, Feature Flags)

**Principle:** Make the technical decision (deploy) and the business decision (release) separate — kill political coupling.

**Do:**
- Use blue-green deployments for instant rollback — flip a router.
- Use canary releases to ramp traffic to a small percentage of users.
- Use feature flags / dark launching to ship code "already in production" but invisible.
- Pair every flag with monitoring and a kill switch.

**Don't:**
- Treat "deploy = release" — it couples tech and business decisions.
- Hide behind manual "go/no-go" meetings for routine deploys.
- Skip the rollback drill — practice it.

**Code (verbatim, Facebook's release process):**
> "In his talk on the Facebook release process, release manager Chuck Rossi says that all the major features that will launch in the next six months are *already* in production—you just can't see them yet. Developers protect new features with 'feature flags' so that administrators can dynamically grant access to particular sets of users on a per-feature basis."

*Ref: Lean_Enterprise.md — "Chapter 8: Decouple Deployment and Release"*

---

### 35. Impact Mapping: Outcomes, Not Solutions

**Principle:** At the program level, specify *outcomes* — never features or "epics."

**Do:**
- Run an Impact Mapping session for every program-level target condition.
- Answer the four questions: Why? / Who? / How? / What?
- List multiple "hows" for each stakeholder; treat the list as assumptions, not deliverables.
- Prefer non-software solutions (marketing, process) before code.
- Keep iterations short (2–4 weeks) so target conditions can adapt.

**Don't:**
- Maintain a "program backlog" of features — features are a means, not the goal.
- Estimate "epics" in months at the program level — it's theatre.
- Allow "architectural epics" — architecture is a means to a measurable target.

**Code (verbatim, Gojko Adzic via the book):**
> "Gojko Adzic presents a technique called *impact mapping* to break down high-level business goals at the program level into testable hypotheses. Adzic describes an impact map as 'a visualization of scope and underlying assumptions, created collaboratively by a cross-functional group of stakeholders. It is a mind-map grown during a discussion facilitated by answering the following questions: 1. Why? 2. Who? 3. How? 4. What?'"

*Ref: Lean_Enterprise.md — "Chapter 9: Using Impact Mapping to Create Hypotheses for the Next Iteration"*

---

### 36. Hypothesis-Driven Development and User Research

**Principle:** "We do no major new development work without first creating a hypothesis."

**Do:**
- Use the Lean UX hypothesis template: "We believe that [building this feature] [for these people] will achieve [this outcome]. We will know we are successful when we see [this signal from the market]."
- Run the cheapest viable user research (interviews, usability, analytics, surveys).
- Triangulate qualitative and quantitative methods.
- Iterate the hypothesis when evidence disagrees — don't defend it.

**Don't:**
- Skip user research because "we know our users."
- Use surveys to confirm what you already believe.
- Treat failed hypotheses as failures — they're validated *learning*.

**Code (verbatim, the hypothesis template):**
> "We believe that [building this feature] [for these people] will achieve [this outcome]. We will know we are successful when we see [this signal from the market]."

*Ref: Lean_Enterprise.md — "Chapter 9: Performing User Research"*

---

### 37. Online Controlled Experiments (A/B Testing) — Most Ideas Fail

**Principle:** Most good ideas deliver *zero or negative* value — only experiments tell us which.

**Do:**
- Run randomized, controlled experiments with random allocation to control (A) vs treatment (B).
- Define the Overall Evaluation Criterion (OEC) *before* launching — often weighted customer lifetime value.
- Apply Twyman's Law — "if a statistic looks interesting or unusual it is probably wrong."
- Pre-agree on control limits so the team can abort safely.
- Run experiments for the cohort (date user first saw the experiment), not aggregates.

**Don't:**
- Skip the OEC definition.
- Run experiments that overlap or "talk" to each other.
- Apply sunk-cost reasoning when an experiment shows the feature is broken.
- Trust your designer's gut more than 95% confidence data.

**Code (verbatim, Kohavi's "humbling" data):**
> "60%–90% of ideas *do not improve the metric they were intended to improve*. Based on experiments at Microsoft, 1/3 of ideas created a statistically significant positive change, 1/3 produced no statistically significant difference, and 1/3 created a statistically significant negative change. *All* of the ideas tested were thought to be good ones."
> "Kohavi, who coined the term 'HiPPO,' says his job is 'to tell clients that their new baby is ugly,' and carries around toy rubber hippos to give to these people."

*Ref: Lean_Enterprise.md — "Chapter 9: Online Controlled Experiments"*

---

### 38. Make It Safe to Fail (Blameless Postmortems, Twyman's Law)

**Principle:** Safety to fail = willingness to learn; the cost of *not* failing safely is invisible failure everywhere.

**Do:**
- Run a *blameless postmortem* after every incident.
- Open every postmortem with the *Retrospective Prime Directive*: "Regardless of what we discover, we understand and truly believe that everyone did the best job they could, given what they knew at the time, their skills and abilities, the resources available, and the situation at hand."
- Hunt for *multiple contributing factors*, never "the root cause" (Dekker: complex systems "drift into failure").
- Schedule follow-up tests for the proposed improvements — run a simulated failure.

**Don't:**
- Identify a single root cause — that's a misreading of complex systems.
- Punish the person who "broke" the system — almost always a confluence.
- Skip follow-up — without verifying the fix, nothing is learned.

**Code (verbatim, Dekker / Hollnagel / Woods / Cook):**
> "Our understanding of how accidents happen has undergone a dramatic development over the last century. Accidents were initially viewed as the conclusion of a sequence of events (which involved 'human errors' as causes or contributors). This is now being increasingly replaced by a systemic view in which accidents emerge from the complexity of people's activities in an organizational and technical context."

*Ref: Lean_Enterprise.md — "Chapter 9: Making It Safe to Fail"*

---

### 39. Innovation Requires a Culture of Experimentation

**Principle:** Without measurement, HiPPO rules. With measurement, ideas can compete on data.

**Do:**
- Make it normal for every intern to CTO to run an A/B test (Greg Linden at Amazon pushed a checkout-recommendation A/B test against an SVP's orders).
- Pair the experimental platform with cheap rollback so wild ideas are cheap to try.
- Cultivate "strong opinions, weakly held" — Paul Sao of Palo Alto Institute.
- Run dozens or hundreds of experiments concurrently (Amazon, Bing — Bing users are in ~15 experiments at any time).

**Don't:**
- Centralize experimentation behind a "research" group — it bottlenecks learning.
- Fire people whose experiments fail (but do discuss poor designs).
- Treat experiments as a phase — they are the way of working.

**Code (verbatim, Linden on Amazon's culture):**
> "Creativity must flow from everywhere. Whether you are a summer intern or the CTO, any good idea must be able to seek an objective test, preferably a test that exposes the idea to real customers. Everyone must be able to experiment, learn, and iterate. Position, obedience, and tradition should hold no power. For innovation to flourish, measurement must rule."

*Ref: Lean_Enterprise.md — "Chapter 9: Innovation Requires a Culture of Experimentation"*

---

### 40. Mission Command: Two-Pizza Teams + Service-Oriented Architecture

**Principle:** Conway's Law means your architecture *is* your org chart — design both together.

**Do:**
- Apply Amazon's "two-pizza rule" — 5–10 people per team; limit growth rate of the product.
- Mandate Bezos-style service interfaces: "all teams will henceforth expose their data and functionality through service interfaces … no other form of interprocess communication allowed."
- Align API boundaries with team boundaries (Conway's Law leveraged, not fought).
- Decompose systems so each feature typically changes only one service (Parnas); avoid chatty services.

**Don't:**
- Split teams by function across floors/timezones — destroys shared context.
- Tolerate shared-memory or back-door coupling — it's the path to a big-ball-of-mud.
- Impose process-level ownership that crosses team boundaries — that's *your* Conway violation.

**Code (verbatim, Bezos's API mandate via Steve Yegge):**
> "All teams will henceforth expose their data and functionality through service interfaces. Teams must communicate with each other through these interfaces. There will be no other form of interprocess communication allowed: no direct linking, no direct reads of another team's data store, no shared-memory model, no back-doors whatsoever. The only communication allowed is via service interface calls over the network. … Anyone who doesn't do this will be fired."

*Ref: Lean_Enterprise.md — "Chapter 10: Amazon's Approach to Growth"*

---

### 41. Velocity at Scale Through Mission Command (Etsy, Netflix, Amazon)

**Principle:** Highly aligned, loosely coupled — and the alignment comes from intent + data, not meetings.

**Do:**
- Push authority to push to production down to the team or engineer (Etsy, Netflix, Amazon).
- Embed specialists (UX, DBA, security) in product teams as "T-shaped" people.
- Ensure teams can self-service infrastructure (PaaS/IaaS via API) — no tickets.
- Use fitness functions (per-team OEC) instead of feature backlogs.
- Maintain technical independence: services must be deployable independently.

**Don't:**
- Make cross-team changes through a centralized release board.
- Compare cost of internal chargeback vs. team-level P&L visibility — both can be done.
- Treat "DevOps" as a separate team — it's a property of all teams.

**Code (verbatim, Amazon's "fitness function" model):**
> "Each two-pizza team (2PT) is as autonomous as possible. The team's lead, working with the executive team, would decide upon the key business metric that the team is responsible for, known as the *fitness function*, that becomes the overall evaluation criteria for the team's experiments. The team is then able to act autonomously to maximize that metric, using the techniques we describe in Chapter 9."

*Ref: Lean_Enterprise.md — "Chapter 10: Create Velocity at Scale Through Mission Command"*

---

### 42. Evolve Architecture via the Strangler Application Pattern

**Principle:** Don't big-bang rewrite — strangle the old system with the new one.

**Do:**
- Start with new functionality the legacy *can't* support; prioritize by CD3.
- Don't port existing functionality *unless* it supports a business process change.
- Deliver something fast — measure success in weeks, not features.
- Design for testability and deployability; run on PaaS.
- Map "surface area" of systems to retire; make it visible; relentlessly reduce it.

**Don't:**
- "Big bang" re-architect — it almost always fails or ships late.
- Port features 1:1 from legacy — that reproduces yesterday's accidental complexity.
- Start by replacing *existing* functionality — there's nothing to validate there.

**Code (verbatim, on incremental replacement):**
> "Amazon did not replace their monolithic Obidos architecture in a 'big bang' replacement program. Instead, they moved to a service-oriented architecture incrementally, while continuing to deliver new functionality, using a pattern known as the 'strangler application.' … Over time, the old application is 'strangled'—just like a tree enveloped by a tropical strangler fig."

*Ref: Lean_Enterprise.md — "Chapter 10: Evolving Your Architecture Using the Strangler Application Pattern"*

---

### 43. Architect for Continuous Delivery (Testability + Deployability)

**Principle:** Treat testability and deployability as *first-class* architectural qualities — alongside performance, security, scalability, reliability.

**Do:**
- Make every component independently deployable.
- Co-locate teams that own services with the teams that operate them.
- Treat architects as enablers of intent — "create architectural alignment through specifying target conditions, not standardization and architectural epics."
- Use Conway's Law as a tool, not an enemy.

**Don't:**
- Confuse architectural cleanliness with end-to-end testability.
- Impose standardization without specifying *measurable* outcomes.
- Plan top-down "rationalization" diagrams that no team can deliver against.

*Ref: Lean_Enterprise.md — "Chapter 10: Architecting for Continuous Delivery"*

---

### 44. Model and Measure Organizational Culture (Westrum + Schein)

**Principle:** Culture is intangible but *measurable* — measure it, surface it, and act.

**Do:**
- Apply the Westrum typology (pathological / bureaucratic / generative) to characterize teams.
- Use Schein's three layers (artifacts, espoused values, underlying assumptions) to find the *real* values.
- Run anonymous, aggregated, de-coupled-from-pay culture surveys (DLOQ, Gallup Q12, custom Likert).
- Look for *inconsistencies* between espoused values and observed behavior — observed wins.

**Don't:**
- Run anonymous surveys that turn into witch hunts (people punished for poor results).
- Couple culture surveys to compensation.
- Treat culture as "set by the founders" — it's constantly evolving.

**Code (verbatim, Schein on culture):**
> "Culture is 'a pattern of shared tacit assumptions that was learned by a group as it solved its problems of external adaptation and internal integration, that has worked well enough to be considered valid and, therefore, to be taught to new members as the correct way to perceive, think, and feel in relation to those problems.'"

*Ref: Lean_Enterprise.md — "Chapter 11: Model and Measure Your Culture"*

---

### 45. Theory X vs. Theory Y — Change Through Behavior, Not Belief

**Principle:** Change behavior, and beliefs follow. The opposite rarely works.

**Do:**
- Recognize Theory X assumptions as self-fulfilling prophecies (passive employees because managers treat them as passive).
- Default to Theory Y: people will link their goals to the organization's if the environment supports it.
- Lead by *demonstrating* the new behavior, not by slogans (NUMMI: define desired behaviors, train, then reinforce).
- Use the Improvement Kata to safely reduce *learning anxiety* without ratcheting up *survival anxiety*.

**Don't:**
- Try to change minds first — Shook: "the way to change culture is not to first change how people think, but instead to start by changing how people behave."
- Increase fear — "Schein postulates that for change to succeed, survival anxiety must be greater than learning anxiety, and to achieve this, 'learning anxiety must be reduced rather than increasing survival anxiety.'"

**Code (verbatim, Shook on NUMMI):**
> "What my NUMMI experience taught me that was so powerful was that the way to change culture is not to first change how people think, but instead to start by changing how people behave—what they do. Those of us trying to change our organizations' culture need to define the things we want to do, the ways we want to behave and want each other to behave, to provide training and then to do what is necessary to reinforce those behaviors. The culture will change as a result."

*Ref: Lean_Enterprise.md — "Chapter 11: Change Your Culture"*

---

### 46. Dweck's Growth Mindset — Hire for Learning, Not Skills

**Principle:** Hire people who believe ability can be developed; reward effort on hard problems.

**Do:**
- Reward effort on challenging problems — Dweck shows this shifts people to a growth mindset.
- Hire for *learning ability* (Google's #1), *emergent leadership* (#2), and *mindset* (#3).
- Hire people with "strong opinions, weakly held" (Paul Sao).
- Invest in people — competitive advantage over startups.

**Don't:**
- Hire for fixed checklists of skills — the field changes too fast.
- Reward for "demonstrating existing ability" — that creates a fixed mindset.
- Confuse "talent shortage" with culture problems (toxicity, bias, no training).

**Code (verbatim, Dweck via the book):**
> "In a fixed mindset, students believe their basic abilities, their intelligence, their talents are just fixed traits. They have a certain amount and that's that, and then their goal becomes to look smart all the time and never look dumb. In a growth mindset, students understand that their talents and abilities can be developed through effort, good teaching, and persistence."

*Ref: Lean_Enterprise.md — "Chapter 11: There Is No Talent Shortage"*

---

### 47. Eliminate Hidden Bias — Equitable Pay, Equitable Promotion

**Principle:** Implicit bias is *measurable* and self-inflicts the "talent shortage."

**Do:**
- Examine average salary by role, race, gender — correct disparities (Netlix "top of market" is a viable model).
- Use target conditions on the *list* of candidates (e.g., "50% women short-listed") rather than quotas.
- Monitor tenure, promotion rate, and job satisfaction by demographic.
- Hire an external reviewer for HR processes periodically.

**Don't:**
- Allow subjective words like "abrasive" to creep into performance feedback without challenge.
- Treat "culture fit" as a cover for bias.
- Promote people into management because they're great individual contributors without coaching them.

**Code (verbatim, Level Playing Field Institute survey):**
> "A representative survey of 19,000 people carried out in the USA by the Level Playing Field Institute between 2001 and 2006 found that the annual cost to US businesses attributable to voluntary turnover of managers and professionals due solely to unfairness was \$64 billion. Respondents cited the following behaviors: rudeness, having coworkers at a similar or higher level who are less educated or less experienced, others taking credit for your work, being given assignments that are usually considered below your job level, feeling excluded from the team, and being stereotyped."

*Ref: Lean_Enterprise.md — "Chapter 11: Eliminate Hidden Bias"*

---

### 48. Governance vs. Management — Distinct, Both Essential

**Principle:** Governance = direction + monitoring; Management = planning + running. Conflating them kills delivery.

**Do:**
- Define responsibility, authority/accountability, visibility, and empowerment at every level.
- Use COBIT 5 framing to separate governance from management.
- Apply lean to GRC processes like any other value stream.
- Default to *outcomes* ("are we mitigating risk?") over *activities* ("did we tick the box?").

**Don't:**
- Use governance as an excuse for micromanagement.
- Treat segregation-of-duties as a Sarbanes-Oxley requirement — "nowhere in the act … is segregation of duties mentioned."
- Build "wouldn't it be horrible if" risk management without prioritization.

**Code (verbatim, COBIT 5):**
> "Governance ensures that stakeholder needs, conditions, and options are evaluated to determine balanced agreed-on enterprise objectives to be achieved; sets direction through prioritization and decision making; and monitors performance and compliance against agreed-on direction and objectives. Management plans, builds, runs, and monitors activities in alignment with the direction set by the governance body to achieve the enterprise objectives."

*Ref: Lean_Enterprise.md — "Chapter 12: Understanding Governance, Risk, and Compliance"*

---

### 49. Apply Lean Principles to GRC — Trust but Verify

**Principle:** GRC processes must be designed as *value streams* — not as command-and-control scaffolds.

**Do:**
- Map the value stream of compliance activities end-to-end; find the waits and the handoffs.
- Embed InfoSec as cross-functional team members (not gatekeepers at the end).
- Use *compensating controls* (e.g., deployment pipeline + audit trail) to replace manual gates.
- Favor detective controls + monitoring over preventive controls (which only push risk around).

**Don't:**
- Run "wouldn't it be horrible if" risk management — Tippet: "since every area has a 'wouldn't it be horrible if…' all things need to be done. There is no sense of prioritization."
- Add preventive controls without considering their effect on team flow.
- Use "risk management theater" — paperwork that nobody reads.

**Code (verbatim, the Etsy PCI-DSS playbook):**
> "1. Minimize the fallout of the required compliance. … 2. Establish and limit the blast radius of frameworks and regulations. Always start by asking, 'What's the smallest possible set of changes we can make to our ideal architecture and culture while still achieving compliance with regulations we are subject to?' 3. Use compensating controls. It's essential to respect the outcomes the regulations are trying to achieve, while recognizing there are many ways to achieve those outcomes."

*Ref: Lean_Enterprise.md — "Chapter 12: Apply Lean Principles to GRC Processes"*

---

### 50. Lean Financial Management (Beyond Budgeting)

**Principle:** Replace centralized annual budgeting with rolling forecasts, dynamic resource allocation, and team-level trust.

**Do:**
- Separate the goals of budgeting: targets, plans, forecasts, coordination, evaluation — each deserves its own mechanism.
- Use rolling forecasts and dynamic resource allocation (Figure 13-2).
- Fund *teams and products*, not projects.
- Use activity-based costing to expose the *true* cost of products.
- Avoid using budgets as performance targets — Deming: "abolishment of the annual or merit rating."
- Treat CapEx/OpEx as an *accounting* choice, not a *business* choice.

**Don't:**
- Tie executive bonuses to meeting budget targets (creates use-it-or-lose-it behavior).
- Distort technology choices to fit CapEx/OpEx rules (e.g., buying hardware to capitalize vs. using SaaS).
- Punish teams that improve cost — "if you achieve a 10% efficiency gain, your budget gets cut 10%."
- Have procurement drive procurement decisions; technology choice belongs to teams.

**Code (verbatim, on Borealis):**
> "When European petrochemicals giant Borealis took this approach, they expected that costs would go up. Instead, they went down. Although Borealis was well positioned and prepared for the change with a culture that supported the move, CFO Bjarte Bogsnes attributes most of the outcome to better visibility into cost drivers through the use of activity-based accounting principles."

*Ref: Lean_Enterprise.md — "Chapter 13: Liberating Ourselves from the Annual Budget Cycle"*

---

### 51. Sample Funding Models Match Complexity to Scrutiny

**Principle:** Local initiatives get less review; enterprise-level initiatives get more.

**Do:**
- Match funding model to relationship complexity:
  - Simple (1:1) / fast change: 2-week sprints, tiny teams, temporary infra.
  - 2–3 product team / moderate: 2–4 week sprints, mixed teams, small blocks.
  - Enterprise-level / slower change: 3–6 month horizons, started small, continued funding decisions every 4–6 weeks.
- Bonuses are shared equally — WestJet model works because everyone has skin in the game.
- Make P&L visible at the service level — "the cost of the service is simply the cost of the resources consumed by the team, plus their salaries."

**Don't:**
- Send everything through the same 6-month procurement process.
- Confuse "internal chargeback precision" with actual cost accuracy.
- Reward only executives while telling everyone else the change is "for the greater good."

**Code (verbatim, WestJet):**
> "Twice a year, a portion of the company profits are distributed to all employees, prorated on their base salary. All employees are invited to attend the profit share party where physical cheques are handed to team members by their managers—face-to-face whenever possible, so managers can personally recognize every employee for their contribution. … In 2012, over 85% of employees participated in this program, becoming part owners of WestJet."

*Ref: Lean_Enterprise.md — "Chapter 13: Sample Funding Models"*

---

### 52. Modify IT Procurement for Real Outcomes

**Principle:** RFP-based procurement is a poor way to manage innovation risk; collaboration beats contract negotiation.

**Do:**
- Apply Deming Point 4: "End the practice of awarding business on the basis of price tag. Instead, minimize total cost. Move toward a single supplier for any one item, on a long-term relationship of loyalty and trust."
- Pay incrementally for *working software*, not for contract milestones.
- Mix small, frequent contracts with innovative suppliers (UK government: <£100m, 2-year hosting, no auto-renew).
- Collaborate daily with suppliers — "customer collaboration over contract negotiation."

**Don't:**
- Award solely on price — lowest bid usually means highest change-request cost.
- Auto-renew incumbent contracts — "the perceived costs and risks associated with finding a new supplier are often thought to be greater than renewing existing contracts."
- Offshore work *only* because of unit cost without accounting for communication delay.

**Code (verbatim, UK government procurement reform):**
> "No contracts over £100m would be rewarded except under exceptional circumstances. Companies with a contract for service provision will not be allowed to provide system integration in the same part of the government. New hosting contracts will be for a maximum period of two years. No contracts will be automatically renewed."

*Ref: Lean_Enterprise.md — "Chapter 13: Modify IT Procurement Processes"*

---

### 53. Rethink the IT Mindset — "You Build It, You Run It"

**Principle:** IT is not a cost center — it's a competitive advantage. Make teams own outcomes.

**Do:**
- Adopt Werner Vogels's rule: "You build it, you run it."
- Apply Google's production-readiness review before launch; transfer to SRE only after handover review.
- Make developers + ops rotate on-call for what they build.
- Measure throughput *and* stability: change lead time, deployment frequency, MTTR, change fail rate.

**Don't:**
- Treat IT as "the business" vs. "IT" — eliminate the distinction.
- Let "no-ops" rhetoric scare ops folks — demand for ops skills *grows* in the new model.
- Ship "dev complete" features that the team wouldn't be willing to be paged for.

**Code (verbatim, *2014 State of DevOps Report*):**
> "High-performing IT organizations are able to achieve both high *throughput*, measured in terms of change lead time and deployment frequency, and high *stability*, measured as the time to restore service after an outage or an event that caused degraded quality of service. High-performing IT organizations also have 50% lower change fail rates than medium- and low-performing IT organizations."

*Ref: Lean_Enterprise.md — "Chapter 14: Rethinking the IT Mindset"*

---

### 54. Platforms Are Products — With Internal Customers

**Principle:** Treat internal infrastructure/platforms as products, not as plumbing.

**Do:**
- Apply product development to platform creation — internal customers are real.
- Use SDP (Service Delivery Platform) principles: automate build/test/deploy, infra provisioning.
- Demand "self-service in seconds" via API; if not, the project failed.
- Run real failure injection (Game Days, DiRT, Chaos Monkey) and blameless postmortems.
- Use *value chain maps* (Simon Wardley) to drive to-be platform architecture.

**Don't:**
- Use "private cloud" as a label for slow ticket-based infra provisioning.
- Customize COTS packages — change your business process to fit the package.
- Pretend the CIA shouldn't outsource — strong encryption + key hygiene beat corporate firewalls.

**Code (verbatim, on the success criterion of a cloud):**
> "Any cloud implementation project not resulting in engineers being able to self-service environments or deployments instantly on demand using an API must be considered a failure. The only criterion for the success of a private cloud implementation should be a substantial increase in overall IT performance using the throughput and stability metrics presented above: change lead time, deployment frequency, time to restore service, and change fail rate."

*Ref: Lean_Enterprise.md — "Chapter 14: Creating and Evolving Platforms"*

---

### 55. Manage Legacy Systems via Coupling Mitigation, Abstraction, Strangler

**Principle:** Three horizons of legacy work — short (transparency), medium (abstraction), long (rearchitect).

**Do:**
- Short-term: prioritize transparently across teams; meet weekly to align coupled work.
- Medium-term: virtualize or test-double the remote systems to break integration dependencies.
- Long-term: strangler-pattern replacement; map value chain; use SaaS for utilities, COTS for non-strategic, custom for strategic.
- Keep systems-of-record on COTS/mainframe + minimal customization.

**Don't:**
- Customize COTS packages — once you start, you can't stop.
- Plan a "rationalize the architecture" big diagram — the ecosystem always outruns you.
- Treat Suncorp's 580-process redesign as a one-off — it's the *result* of aggressive simplification.

**Code (verbatim, Suncorp outcomes):**
> "In the process, Suncorp has reduced 15 complex personal and life insurance systems to 2 and decommissioned 12 legacy systems. Technical upgrades are done once and rolled out across all brands. … The simpler system has allowed 580 business processes to be redesigned and streamlined. … Suncorp's 2014 annual report notes that 'simplification has enabled the Group to operate a more variable cost base, with the ability to scale resources and services according to market and business demand. Simplification activity is anticipated to achieve savings of \$225 million in 2015 and \$265 million in 2016.'"

*Ref: Lean_Enterprise.md — "Chapter 14: Managing Existing Systems"*

---

### 56. Hoshin Kanri / Strategy Deployment — Catchball, Not Cascade

**Principle:** Strategic alignment is *translation* with feedback at every level — not a top-down cascade.

**Do:**
- Define a clear, inspiring, even unattainable direction ("10× productivity").
- Choose what *not* to focus on.
- Set 10–15 KPIs; prefer *relative* targets tied to baselines.
- Use *catchball* — each layer translates intent, not transcribes it.
- Hold monthly cross-functional review meetings; update target conditions based on what you learn.
- Use QCDMS (Quality, Cost, Delivery, Morale, Safety) as the canonical "lean metrics."

**Don't:**
- Translate Hoshin into a one-way cascade — it kills alignment.
- Use absolute targets ("reduce cost 10%") without a baseline — meaningless.
- Skip the cross-functional reviews.

**Code (verbatim, on catchball):**
> "In strategy deployment, this process is described as *catchball*, a word chosen to evoke a collaborative exercise. The target conditions from one level should not be transcribed directly into the direction for teams working at the level below; catchball is more about *translation* of strategy, with 'each layer interpreting and translating what objectives from the level above mean for it.' We should expect that feedback from teams will cause the higher-level plan to be updated."

*Ref: Lean_Enterprise.md — "Chapter 15: Aim Towards Strategy Deployment"*

---

### 57. The UK Government Digital Service (GDS) Playbook

**Principle:** Civil servants, given the right principles and autonomy, can out-ship private vendors.

**Do:**
- Start with a small cross-functional team (GDS started with 14 people).
- Build an *Alpha* in 12 weeks for £261k as a snapshot — not a final product.
- Apply continuous delivery (GDS: ~6 deploys/day, >1,000 deploys in the first months).
- Adopt principle-based governance: "Don't slow down delivery. Decide, when needed, at the right level. Do it with the right people. Go see for yourself. Only do it if it adds value. Trust and verify."
- Replace big-bang legacy systems via strangler pattern.

**Don't:**
- Start with a 140-person team — start with 14.
- Believe the GDS only works in tech — it works in highly regulated environments.
- Let outsourcing vendors set the price of innovation — GDS saved £42m+ in year one.

**Code (verbatim, GDS operating principle):**
> "1. Don't slow down delivery. 2. Decide, when needed, at the right level. 3. Do it with the right people. 4. Go see for yourself. 5. Only do it if it adds value. 6. Trust and verify. … People are trusted to make the best decisions in their context, but are accountable for those decisions—in terms of both the achieved outcomes and knowing when it is appropriate to involve others."

*Ref: Lean_Enterprise.md — "Chapter 15: The UK Government Digital Service"*

---

### 58. Toyota Production System — "Building People Before Building Cars"

**Principle:** Lean is a *cultural* system for learning under uncertainty — the practices emerge from it.

**Do:**
- Embed the *andon cord* philosophy — anyone can stop the line.
- Use jidoka (build quality in) — never delegate quality to a later phase.
- Apply *kaizen* (continuous improvement) at every level, every day.
- Practice *kaikaku* (radical change) as an experiment with a small, capable team.
- Train *Improvement Kata* across the organization; pair it with the *Coaching Kata* for managers.

**Don't:**
- Adopt the *tools* (kanban boards, andon cords) without the culture.
- Reduce lean to "cut costs" — it's a *worker-led* reinvestment in quality and capability.
- Treat it as a one-off project — kaizen must be habitual.

**Code (verbatim, Toyota's view of people):**
> "When everybody in the organization has been trained to employ the scientific approach to innovation as part of their daily work, we will have created a generative culture. … Toyota calls this 'building people before building cars.'"

*Ref: Lean_Enterprise.md — "Chapter 1: Introduction" (NUMMI + TPS) + Chapter 6 (Improvement Kata)*

---

### 59. Christensen's Innovator's Dilemma — Cannibalize Thyself

**Principle:** Profitable enterprises are reluctant to cannibalize themselves — until they go bankrupt doing so.

**Do:**
- Establish separate, separately-compensated, separately-managed subsidiaries to attack your own core (Aetna's Healthagen).
- Continually experiment and test theories — Amazon's disruption of its own book business via Kindle and Marketplace.
- Set explicit innovation-from-self KPIs (3M's target of 30%+ revenue from products <5 years old; 40% by 2017).
- Appoint someone whose *career* is tied to the new business, not the legacy.

**Don't:**
- Ask the manager of your profit center to greenlight the disruption of it.
- Treat Christensen's "disruption" as a marketing slogan — it's an organizational choice.
- Wait for a competitor to do it to you (Kodak, Blockbuster, Xerox PARC).

**Code (verbatim, Aetna):**
> "160 years old at the time the bill was signed into law, Aetna decided to create a new company called Healthagen, 'a separate organization, separately capitalized, separately compensated, and separately managed, so they're not subject to the same management process at Aetna' with the purpose of disrupting the healthcare provider market with new technology and business models. Healthagen has a goal to drive \$1.5bn–\$2bn of revenue per year initially."

*Ref: Lean_Enterprise.md — "Chapter 2: How Aetna Created New Companies to Disrupt Its Core Businesses"*

---

### 60. Deming's "14 Points" as the Cultural Underlay

**Principle:** Lean at enterprise scale inherits Deming's management philosophy — not his tools.

**Do:**
- Point 4: "End the practice of awarding business on the basis of price tag. Instead, minimize total cost."
- Point 8: "Drive out fear, so that everyone may work effectively for the company."
- Point 13: "Encourage education and self-improvement for everyone."
- Replace annual merit ratings with continuous coaching.
- Institute a leadership commitment to "cease dependence on mass inspection to achieve quality."

**Don't:**
- Copy Japanese-specific practices without adaptation — adapt them to your context.
- Confuse Deming with Six Sigma — Deming warned against the latter's narrow application.
- Reduce Deming to slogans — he called that out as "instant pudding."

**Code (verbatim, Deming):**
> "Cease dependence on mass inspection to achieve quality. Improve the process and build quality into the product in the first place."
> "Remove barriers that rob people in management and in engineering of their right to pride of workmanship. This means, *inter alia*, abolishment of the annual or merit rating and of management by objective."

*Ref: Lean_Enterprise.md — "Chapter 1 (NUMMI) + Chapter 8 (Deming) + Chapter 13 (procurement)"*

---

### 61. Boyd's OODA + Ries' Build-Measure-Learn = The Universal Loop

**Principle:** Observe → Orient → Decide → Act (and its offspring Build → Measure → Learn) is the same loop at every scale.

**Do:**
- Apply OODA as a thinking model at the individual, team, and organizational levels.
- Use *Build-Measure-Learn* as the product-development instantiation of OODA.
- Use *PDCA* (Deming) as the process-improvement instantiation.
- Make IGT (implicit guidance) strong enough that most decisions happen without waiting for permission.
- Use the *last responsible moment* to delay decisions until optionality is exhausted.

**Don't:**
- Read OODA as "go through the cycle as fast as you can" — multiple feedback loops run in parallel.
- Separate OODA between functions (strategy vs. execution) — they're entangled.
- Conflate orientation with information — orientation is shaped by culture, history, and identity.

**Code (verbatim, on the misreading of OODA):**
> "A common misconception (primarily by people who have not actually seen the diagram) is that these activities are carried out one after the other in a loop, and that disruption is achieved by going through the cycle faster than your opponent. There are two important flaws with this interpretation. First, in reality both humans and organizations are performing all of these activities simultaneously, and there are multiple feedback and feed-forward loops between each of them. Second, it is often advantageous to *delay* making decisions until the 'last responsible moment.'"

*Ref: Lean_Enterprise.md — "Chapter 3: Principles for Exploration"*

---

### 62a. Customer vs. User — Always Disambiguate

**Principle:** Customers pay; users use — and both are co-creators of value.

**Do:**
- Distinguish customers (who pay or commission) from users (who actually use the product).
- Engage both as stakeholders in co-creation — particularly in the enterprise where users are *required* to use systems.
- Treat users as a real source of value, not "labor that the system makes happy."
- Look for examples where users' value creation is invisible — social networks being the textbook case.

**Don't:**
- Conflate customer development with user research.
- Optimize for the paying customer's KPIs while the users revolt.
- Ignore enterprise-internal "users" because they didn't choose the system.

**Code (verbatim, from the book):**
> "Although we often use the terms interchangeably, it is useful to distinguish between the *customers* of a product or service, who pay for it or invest in its development, and the *users*. Users do not pay for the product, but they contribute a great deal of value to the organization that builds the product, and often to the product itself (social networks are one obvious example). In an enterprise, people are *required* to use particular systems in order to get their work done, and organizations suffer real negative consequences when systems are hard to use."

*Ref: Lean_Enterprise.md — "Chapter 4: Customers and Users"*

---

### 62b. Make Solutions, Not Requirements — The Hypothesis Backlog

**Principle:** Backlogs are full of solutions; what you need is a list of unresolved questions.

**Do:**
- Convert every "requirement" in your backlog into a hypothesis + smallest test.
- Identify the *riskiest* hypothesis for each iteration; design one experiment around it.
- Group experiments into themes — feature hypothesis, usability hypothesis, business-model hypothesis.
- Review the runway at every iteration planning; promote what was learned to the next plan.

**Don't:**
- Treat a fully built feature as "delivered value" — it's "delivered output" pending validation.
- Carry requirements forward unchanged across iterations without re-validating them.
- Let the backlog be a proxy for delivery confidence.

*Ref: Lean_Enterprise.md — "Chapter 5: Build a Runway of Questions, Not Requirements"*

---

### 62c. Story Mapping to Externalize the Narrative

**Principle:** Story maps show the *backbone* and *skeleton* of the product — not a release plan.

**Do:**
- Use Jeff Patton's story map to show the *narrative* of your user's journey.
- Place the highest-risk hypotheses near the top; the smallest increment across the whole stack at the next "sprint slice."
- Re-validate the map every iteration — let evidence reshape the narrative.
- Use it as a *conversation* tool with stakeholders and users, not a delivery contract.

**Don't:**
- Turn the story map into a Gantt chart.
- Hide unfinished horizontal slices — they're honest signals of incomplete learning.
- Treat it as a substitute for customer development.

**Code (verbatim, from the book on Patton):**
> "Your software has a backbone and a skeleton—and your map shows it. … Story mapping is not designed to generate stories or create a release plan—it is about understanding customers' objectives and jobs-to-be-done. Story maps provide an effective means to communicate the narrative of our solution to engage the team and wider stakeholders and get their feedback."

*Ref: Lean_Enterprise.md — "Chapter 5: Create a Story Map to Tell the Narrative of the Runway of Our Vision"*

---

### 62d. Conway's Law — Architect Teams to Architect Systems

**Principle:** Architecture mirrors communication; design both intentionally.

**Do:**
- Align API boundaries with team boundaries.
- Place engineers, designers, and testers *together* (co-located when possible) so they share context.
- Avoid split teams by function or layer — front-end, business-logic, and DB on three continents is asking for pain.
- Reorganize *only* if it solves a problem — it's expensive and disruptive.

**Don't:**
- Try to *fight* Conway's Law — it's physics.
- Conflate reporting lines with team membership — reporting lines are administrative; team membership is operational.
- Punish teams for boundary-related friction; redesign the boundaries instead.

**Code (verbatim, from the book):**
> "Organizations often try to fight Conway's Law. A common example is splitting teams by function, e.g., by putting engineers and testers in different locations (or, even worse, by outsourcing testers). Another example is when the front end for a product is developed by one team, the business logic by a second, and the database by a third. Since any new feature requires changes to all three, we require a great deal of communication between these teams, which is severely impacted if they are in separate locations. Splitting teams by function or architectural layer typically leads to a great deal of rework, disagreements over specifications, poor handoffs, and people sitting idle waiting for somebody else."

*Ref: Lean_Enterprise.md — "Chapter 10: A Brief Introduction to Service-Oriented Architectures"*

---

### 62e. Two-Pizza Teams — The Right Size for Shared Context

**Principle:** Team size limits shared context; Amazon's two-pizza rule encodes a combinatorial truth about communication.

**Do:**
- Keep teams at 5–10 people.
- Use the rule as a *rate-limiter* on how fast any one product can grow — that's a feature.
- Grow by adding *new* two-pizza teams, not by expanding existing ones.
- Recognize that leading a 2PT is a leadership training ground for entrepreneurial talent.

**Don't:**
- Let one team grow to 30 people because the project got "important."
- Confuse "two pizzas" with arbitrary — it's a combinatorial argument about context.

**Code (verbatim, Amazon's four effects):**
> "This limit on size has four important effects: 1. It ensures the team has a clear, shared understanding of the system they are working on. … 2. It limits the growth rate of the product or service being worked on. … 3. Perhaps most importantly, it decentralizes power and creates autonomy … 4. Leading a 2PT is a way for employees to gain some leadership experience in an environment where failure does not have catastrophic consequences."

*Ref: Lean_Enterprise.md — "Chapter 10: Create Velocity at Scale Through Mission Command"*

---

### 62f. T-Shaped People — Cross-Functional with Depth

**Principle:** Small teams need broad skills; deep specialization comes from a few *centers* of expertise per team.

**Do:**
- Hire "T-shaped" people — broad generalists with 1–2 deep specialisms.
- Pair domain experts (DBAs, UX, security) with generalists — everyone learns from each other.
- Rotate specialists across teams to spread knowledge.
- Build *internal communities of practice* so specialists don't become isolated.

**Don't:**
- Build teams entirely from specialists — they lack shared context.
- Build teams entirely from generalists — depth suffers.
- Confuse "I do everything" with "T-shaped" — T-shape means depth in at least one area.

*Ref: Lean_Enterprise.md — "Chapter 10: Create Velocity at Scale Through Mission Command"*

---

### 62g. Cloud Success = Self-Service in Seconds

**Principle:** A "cloud" that still requires a ticket to provision an environment is a failure, not a cloud.

**Do:**
- Define the cloud's success criterion in *measurable throughput and stability*: change lead time, deployment frequency, MTTR, change fail rate.
- Make provisioning fully self-service via API.
- Pair each cloud service with a deployment pipeline that uses it.
- Run real disaster recovery exercises (Game Days, DiRT, Chaos Monkey).
- Be willing to use external public cloud — the CIA does.

**Don't:**
- Accept "private cloud" as a label without measuring throughput/stability.
- Lock in long contracts without testing resilience.
- Pretend corporate firewalls beat strong encryption + key management.

**Code (verbatim, on the bar):**
> "The only criterion for the success of a private cloud implementation should be a substantial increase in overall IT performance using the throughput and stability metrics presented above: change lead time, deployment frequency, time to restore service, and change fail rate. This, in turn, results in higher quality and lower costs, as well as freeing up capital to invest in new product development and improving of the existing services and infrastructure."

*Ref: Lean_Enterprise.md — "Chapter 14: Creating and Evolving Platforms"*

---

### 62h. A3 Thinking — Problem Solving on One Page

**Principle:** A3 Thinking (Sobek/Smalley) compresses PDCA into a single page that *teaches* the discipline.

**Do:**
- Use the seven-element A3: Background, Current Condition + Problem Statement, Goal, Root-Cause Analysis, Countermeasures, Check/Confirmation Effect, Follow-up Actions.
- Tie the goal statement to the *Background* — keeps scope honest.
- Use A3 as a *learning* tool, not a status report.
- Combine with Improvement Kata iterations.

**Don't:**
- Use A3 as a 12-page document.
- Write problem statements like "we need a CMS" (that's a solution).
- Skip the root-cause analysis — that defeats the purpose.

*Ref: Lean_Enterprise.md — "Chapter 4: Use A3 Thinking as a Systematic Method"*

---

### 62i. Pull Systems for Knowledge Work

**Principle:** Replace work-pushing with work-pulling; capacity pulls work, not the other way around.

**Do:**
- Use Kanban's pull mechanics — new work starts when capacity frees.
- Apply pull at the program level (Dynamic Priority List) and at the team level (Kanban WIP limits).
- Use the demand-pulled-by-customer logic — when demand is uncertain, pull replaces forecasts.
- Replace quarterly planning festivals with continuous, rolling reprioritization.

**Don't:**
- Push work into a team because a stakeholder shouted loudly.
- Build features because "we have to use our budget."
- Treat pull as a tool for manufacturing only — it works for knowledge work too.

*Ref: Lean_Enterprise.md — "Chapter 7: Increase Flow"*

---

### 62j. Innovation Takes Time — Amazon Auctions → Marketplace

**Principle:** Most "next big things" are pivots from a failed earlier attempt — preserve that knowledge.

**Do:**
- Document failed experiments in a place visible to the next team.
- Apply the *Principle of Optionality* — every failed bid is information.
- Pivot the original idea rather than killing it — Amazon auctions → Marketplace → ~12% of revenue.
- Honor the elapsed time — innovation doesn't show up on a quarterly report.

**Don't:**
- Confuse a single failed experiment with strategic failure.
- Kill an idea before you've preserved what you learned.
- Demand instant ROI from the explore domain.

**Code (verbatim, Amazon pivot):**
> "Amazon auctions (later known as zShops) were launched in March 1999 in response to the success of eBay. The site was promoted heavily from the home, category, and individual product pages. Despite the promotion, one year after launch it had only achieved a 3.2% share of the online auction market compared to 58% for eBay, and subsequently declined. … In 2012, Amazon's Marketplace service produced 12% of revenues with total unit sales increasing 32% from the previous year."

*Ref: Lean_Enterprise.md — "Chapter 5: Innovation Takes Time"*

---

### 62k. Subsidy-of-the-Many for the Few — Horizon 3 Capital Strategy

**Principle:** H3 ideas fail; the few that succeed pay for the rest. Limit downside; preserve optionality.

**Do:**
- Cap per-idea investment (affordable loss).
- Run many small bets in parallel.
- Use the law of large numbers — Taleb's optionality.
- Stop ideas quickly when evidence goes against them.
- Reinvest winners without inflating bureaucracy.

**Don't:**
- Bet the firm on a single H3 idea.
- Punish fast failure — it's the engine of H3.
- Hoard capital in the hope of finding a sure thing.

**Code (verbatim, Taleb via the book):**
> "Investing a fixed amount of time and money to investigate the economic parameters of an idea—be it a business model, product, or an innovation such as a process change—is an example of using optionality to manage the uncertainties of the decision to invest further. We limit our maximum investment loss ('downside') on any individual idea, with the expectation that a small number of ideas will pay off big time, and offset or negate investments in those that did not."

*Ref: Lean_Enterprise.md — "Chapter 2: Build-Measure-Learn and Optionality"*

---

### 62l. Five Lean Principles (Womack & Jones) at Every Scale

**Principle:** Value, value stream, flow, pull, perfection — these five ideas apply to manufacturing *and* software.

**Do:**
- Specify *value* from the customer perspective (not the producer's).
- Map the value stream *end to end*, including wait time.
- Make value *flow* — eliminate handoffs, queues, and rework.
- Let customers *pull* — build only when there's demand.
- Pursue *perfection* — continuous improvement is a habit, not a project.

**Don't:**
- Optimize the producer's view of value.
- Map only the parts of the value stream you control.
- Push work to customers (cold calls, mandatory onboarding).
- Treat perfection as a destination — it's a direction.

*Ref: Lean_Enterprise.md — "Chapter 7: Identify Value and Increase Flow" (Womack & Jones)*

---

### 62m. The Pareto of Features — 80/20 for Experimentation

**Principle:** The 80/20 rule is a multiplier for experimental throughput.

**Do:**
- Build the 20% of functionality that delivers 80% of the expected benefit.
- Don't build for scale during an experiment — only a tiny fraction of users will see it.
- Don't worry about cross-browser — filter users with simple code.
- Don't write comprehensive test coverage for an experiment — good monitoring beats it.

**Don't:**
- Spend 100% of the effort to ship 100% of the feature when 20% of the feature answers the question.
- Over-engineer the experiment — it must be disposable.
- Mistake "thrown together" for "won't scale later" — the experiment's job is to learn.

*Ref: Lean_Enterprise.md — "Chapter 9: Using A/B Testing to Calculate the Cost of Delay"*

---

### 62n. Westrum Reprise — From Pathological to Generative

**Principle:** Make the cultural shift from pathological/bureaucratic to *generative*; everything else follows.

**Do:**
- Start with measurement — Likert-style questions about "messengers," "responsibility," "bridging," "failure response," "novelty."
- Treat *job satisfaction* as a leading indicator of org performance (2014 State of DevOps Report).
- Run the survey annually/semi-annually, anonymously, aggregated.
- Use the data to start *conversations*, not to assign blame.

**Don't:**
- Couple the survey to compensation — it kills honesty.
- Treat culture as a "program" with a start and end date.
- Use it to target individuals — use it to find system-level patterns.

**Code (verbatim, the survey headlines):**
> "The most important of these turned out to be whether people were satisfied with their jobs, based on the extent to which they agreed with the following statements … I would recommend this organization as a good place to work. I have the tools and resources to do my job well. I am satisfied with my job. My job makes good use of my skills and abilities."

*Ref: Lean_Enterprise.md — "Chapter 1: A Lean Enterprise Is Primarily a Human System"*

---

### 62o. Edward Deming's System Profundity

**Principle:** The system is the star — and you improve the system, not the people.

**Do:**
- Attribute outcomes to systems, not individuals.
- Use activity accounting and value stream mapping to expose the system.
- Coach managers to develop people rather than rate them.
- Recognize that fear distorts every number it touches — "whenever there is fear, you get the wrong numbers."

**Don't:**
- Reward or punish people based on metrics they can't control.
- Assume that an excellent individual in a bad system produces excellent results.
- Treat cultural change as a "people problem" — it's a system problem.

**Code (verbatim, Deming):**
> "A bad system will beat a good person every single time."
> "Whenever there is fear, you get the wrong numbers." (Attributed to Deming in Chapter 3 of the book.)

*Ref: Lean_Enterprise.md — "Chapter 1: Mission Command" + Chapter 3 (OODA IGT)*

---

### 62p. Build Your Repertoire — The Antidote to Disruption

**Principle:** Boyd's "repertoire" is the organization's accumulated habits, tools, and processes for acting under uncertainty.

**Do:**
- Continuously add to your repertoire via process improvement, product evolution, and new business creation.
- Refresh the orientation that drives the repertoire.
- Use the OODA repertoire-generation loop.
- Apply the Improvement Kata as a daily practice that *expands* your repertoire.

**Don't:**
- Lock in a single "best practice" for years.
- Treat the existing repertoire as a competitive moat — competitors copy practices faster than you upgrade them.
- Wait for a crisis to update your repertoire.

**Code (verbatim, Boyd on repertoire):**
> "Boyd refers to the implicit guidance and control pathways within an organization, determined by its culture and existing institutional knowledge and processes, as its *repertoire*. … In order to improve performance and avoid disruption, we must be constantly creating new repertoire of our own."

*Ref: Lean_Enterprise.md — "Chapter 3: Principles for Exploration"*

---

### 62q. Reduce Batch Sizes — Reinertsen's Universal Lever

**Principle:** Reducing batch size is the single most important lever for systemic flow improvement.

**Do:**
- Slice requirements into smaller independent pieces.
- Unbundle projects — fund features, not projects.
- Use the CD3 incentive to push for smaller batches.
- Recognize that the "large batch death spiral" Reinertsen identifies drives cost and date overruns.

**Don't:**
- Wait until the project is "done" to deliver value.
- Pack the project with "just one more feature" because "we won't get another chance."
- Treat smaller batches as riskier — they're actually lower risk per change.

*Ref: Lean_Enterprise.md — "Chapter 7: Increase Flow" + Chapter 2 (planning fallacy)*

---

### 62r. The Improvement Kata vs. Other Methodologies

**Principle:** The Improvement Kata is a *meta-methodology* — it teaches teams how to evolve their own playbook.

**Do:**
- Treat the Kata as a routine to practice, not a procedure to install.
- Combine with PDCA cycles that should happen *daily*, not monthly.
- Recognize that the goal is process improvement becoming *habit*.
- Pair the Improvement Kata with the Coaching Kata to grow new managers.

**Don't:**
- Implement the Improvement Kata without teaching managers to coach it.
- Run retrospectives infrequently — continuous means much more often than you think.
- Mandate a specific playbook (Scrum, XP, Kanban) — let teams evolve.

**Code (verbatim, Mike Rother via the book):**
> "You can think of the Improvement Kata as a *meta-methodology* since it does not apply to any particular domain, nor does it tell you what to do. It is not a playbook; rather, as with the Kanban Method, it teaches teams how to *evolve* their existing playbook."

*Ref: Lean_Enterprise.md — "Chapter 6: How the Improvement Kata Differs from Other Methodologies"*

---

### 62s. Learn Faster Than the Thief — Toyota's Open Secret

**Principle:** Continuous improvement makes copying irrelevant.

**Do:**
- Make continuous, incremental change a habit.
- Treat the cost of failures as the price of expertise (Kiichiro Toyoda's quote).
- Welcome visitors and competitors into your plant — they'll copy tools, not the system.
- Invest in people — "building people before building cars."

**Don't:**
- Hoard IP at the cost of progress.
- Treat competitor imitation as a threat — it's a lagging indicator.
- Use the playbook as a competitive moat.

**Code (verbatim, Kiichiro Toyoda):**
> "Certainly the thieves may be able to follow the design plans and produce a loom. But we are modifying and improving our looms every day. So by the time the thieves have produced a loom from the plans they stole, we will have already advanced well beyond that point. And *because they do not have the expertise gained from the failures it took to produce the original*, they will waste a great deal more time than us as they move to improve their loom."

*Ref: Lean_Enterprise.md — "Chapter 1: Your People Are Your Competitive Advantage"*

---

### 62t. The Litmus Test: Can Your People Do This Without Permission?

**Principle:** The ultimate sign of a generative culture: people know the right thing *and* don't need permission to do it.

**Do:**
- Communicate intent (purpose, mission, principles) relentlessly.
- Push authority to the lowest appropriate level (subsidiarity).
- Equip teams with feedback loops so they can self-correct.
- Tolerate mistakes made in good faith — Ackoff's "treatment of error."

**Don't:**
- Use permission as a default gate.
- Mistake "compliance" for "alignment."
- Centralize decisions that the team is better positioned to make.

**Code (verbatim, Bungay on Mission Command culture):**
> "Mission Command embraces a conception of leadership which unsentimentally places human beings at its center. It crucially depends on factors which do not appear on the balance sheet of an organization: the willingness of people to accept responsibility; the readiness of their superiors to back up their decisions; the tolerance of mistakes made in good faith. … At its heart is a network of trust binding people together up, down, and across a hierarchy. Achieving and maintaining that requires constant work."

*Ref: Lean_Enterprise.md — "Chapter 1: Mission Command"*

---

### 62. Start Where You Are — The Lean Transformation Playbook

**Principle:** You can't transform everything at once; begin with a small, focused effort that delivers measurable results.

**Do:**
- Apply Kotter's eight steps (urgency → coalition → vision → communicate → empower → wins → sustain → anchor) — but never as an event.
- Use the Improvement Kata + Coaching Kata as the daily practice that makes the change habitual.
- Choose a *small* initial scope — one product, one team, one value stream.
- Adopt the Diffusion of Innovations curve: start with innovators, then early adopters, then early majority.
- Measure early wins — "If we achieve the results by ignoring the process, we do not learn how to improve the process" (Poppendieck).

**Don't:**
- Mandate the change organization-wide in a "big bang."
- Expect 100% adoption of target conditions — surprises drive learning.
- Forget to keep moving forward — "Fear, uncertainty, and discomfort are your compasses toward growth."

**Code (verbatim, the GDS Alpha):**
> "By late 2013 the team running GOV.UK had over 100 people—but it didn't start that way. In fact, the first version wasn't even called GOV.UK. An Alpha version was built by 14 people working from a small back room in a large government building. Its aim wasn't to be a finished product but to provide a snapshot of what a single government website could be, and how it could be built quickly and cheaply. In total, the Alpha took 12 weeks and cost £261,000."

*Ref: Lean_Enterprise.md — "Chapter 15: Begin Your Journey"*

---

## Anti-Patterns & Common Mistakes

- **HiPPO-driven prioritization:** 13% of firms admit HiPPO decides; 47% use decision-by-committee — both are economic nihilism. → *fix:* require explicit Cost-of-Delay / CD3 reasoning at the work-item level.
- **Mandating internal tools:** Mandating use destroys the feedback loop that Lean Startup requires. → *fix:* find a pilot team and let them opt in.
- **Big-bang rewrite:** "Replace the legacy" projects almost always overrun, get cancelled, or deliver less than promised. → *fix:* strangler application pattern.
- **Big-bang launches:** "Forget 'big bang' launches" — play it safe with alpha/beta cohorts. → *fix:* cohort-based rollout.
- **Tailoring for the HiPPO:** "If you tailor your product to a large customer's spec, you will not be able to sell to anyone else." → *fix:* price concessions require product concessions only as a last resort; protect the vision.
- **Confusing science management with scientific method:** Taylorism vs. Toyota Kata — totally different. → *fix:* practice the Improvement Kata daily.
- **Vanity metrics:** "Total page views" tells you nothing; cohort funnel analysis does. → *fix:* every metric must answer "what will we do differently?"
- **Theory X management:** "They end up with employees who are passive, resistant to change, unwilling to accept responsibility, and make 'unreasonable demands for economic benefits.'" → *fix:* mastery, autonomy, purpose; Theory Y.
- **Activity accounting theatre:** Don't measure activity because you can — measure what reveals *failure demand*. → *fix:* map %C/A and rework.
- **Risk-management theater:** Seven-tab spreadsheets nobody reads. → *fix:* detective controls + compensating controls via deployment pipeline.
- **Process compliance over outcome:** "Many organizations have found it hard to embrace running experiments … executives worry that it threatens their job as decision makers." → *fix:* outlaw HiPPO; use A/B testing.
- **Comparing team velocities across teams:** Designed for within-team, not across. → *fix:* measure program-level outcomes instead.
- **Punishing failure:** Ackoff: "It's our treatment of error that leads to a stability which prevents significant change." → *fix:* blameless postmortems + Improvement Kata.
- **Confusing CapEx/OpEx with business value:** "Funding allocation … should be performed by accountants *after* the business decisions are made." → *fix:* let product teams decide; finance classifies afterward.
- **Cloud labels without cloud behavior:** "Many companies that claim to have implemented 'private clouds' still require engineers to raise tickets." → *fix:* "engineers being able to self-service environments or deployments instantly on demand using an API" is the *only* success criterion.
- **Project-based funding in a product world:** "Funding allocation of a product's development into CapEx or OpEx should be performed by accountants after the business decisions are made." → *fix:* fund teams and products.
- **Acqui-hiring innovation:** "Putting great people into a pathological or bureaucratic culture does not change the culture—it breaks the people." → *fix:* transform your own culture.
- **Customizing COTS:** "Once you get beyond a certain amount of customization, the original vendor will often no longer support the package." → *fix:* change business processes to fit the package.
- **Sunk-cost fallacy on failed experiments:** "They ignore the data and deploy the product as is because shelving the work is considered a total failure." → *fix:* "validated *learning*" is the success metric.
- **Putting 100 people in a Discovery workshop:** Discovery is small + cross-functional. → *fix:* 7–10 people max.
- **Rewarding "dev complete":** Hero culture emerges. → *fix:* "done" = deployed + tested on real users.
- **Friction theatre:** "Complex sets of rules and controls punish the innocent but can be evaded by the guilty." → *fix:* Mission Command + detective controls.
- **Stack ranking:** "Stack-ranking employees … encourage employees to compete rather than cooperate with each other." → *fix:* separate performance review from compensation.
- **Reactive hand-offs across silos:** Splits by function destroys shared context. → *fix:* T-shaped people + Mission Command.

---

## Decision Heuristics / Checklists

- **Choosing explore vs. exploit:** If you don't yet know who the customer is, explore; once you have product/market fit, exploit.
- **Choosing a horizon investment ratio:** Google 70/20/10, Intuit 60/30/10 — but always *intentional*.
- **Choosing an MVP type:** Cheapest experiment that *could* falsify the riskiest hypothesis.
- **Choosing how to prioritize:** Use Cost of Delay + CD3; never HiPPO.
- **Choosing between fix vs. rewrite:** Always strangler, never big-bang.
- **Choosing where to start a transformation:** A single value stream, with a sponsor at every level, and a measurable outcome in <6 months.
- **Choosing between preventive and detective controls:** Detective + monitoring wherever possible; preventive only when truly necessary.
- **Choosing between architectural standardization and intent-based alignment:** Always intent-based — never standard for standardization's sake.
- **Choosing a metric:** "What will we do differently based on changes in the metric?" — Ash Maurya.
- **Choosing a budget model:** Match funding-model complexity to relationship complexity (Table 13-1).
- **Choosing whether to release to production:** OEC + 95% CI; never "looks promising."
- **Choosing an experiment size:** If uncertainty is high, very little data is needed to *significantly reduce* it.
- **Checklist — Continuous Delivery basics:**
  - Everything in version control?
  - CI on every commit?
  - Anyone can revert?
  - Deployment pipeline runs tests in parallel?
  - Deployments are boring, not ordeals?
  - Trunk-based, not branch-based?
- **Checklist — Becoming a Mission Command organization:**
  - Can teams run experiments without funding approval?
  - Can teams choose their toolchain?
  - Can teams deploy without external change-approval boards?
  - Are rewards aligned with system-level outcomes?
  - Is decision-making authority *subsidiary* — local first?
- **Checklist — Hoshin Kanri kickoff:**
  - Inspiring, measurable direction (even if unattainable)?
  - Limited list of problems to focus on?
  - 10–15 KPIs with relative targets?
  - Catchball meetings with cross-functional feedback?
  - Monthly review cadence?
- **Checklist — Becoming a generative (Westrum) culture:**
  - Failure → enquiry (not scapegoating / justice)?
  - Messengers trained, not shot / neglected?
  - Risks shared, responsibilities broad?
  - Bridging encouraged?
  - Novelty implemented?
- **Checklist — Strategy Deployment at program level:**
  - Target conditions SMART (specific, measurable, achievable, relevant, time-bound)?
  - Target conditions are *outcomes*, not features?
  - No "architectural epics" at the program level?
  - Teams free to choose how?
  - Impact Map exists for every target condition?

---

## Key Takeaways

1. **Balance exploration and exploitation** — three horizons, three different management regimes.
2. **Apply the scientific method everywhere** — hypothesize, experiment, measure, decide.
3. **Replace command-and-control with Mission Command** — communicate intent, delegate how, enable feedback.
4. **People are the competitive advantage** — mastery, autonomy, purpose; Theory Y; growth mindset.
5. **Continuous Delivery is the substrate** — version control everything, automate everything, build quality in.
6. **Limit WIP** — Little's Law; WIP limits hurt; that pain reveals systemic problems.
7. **A/B testing and experimentation are non-optional** — most ideas deliver zero or negative value.
8. **Lean applies to GRC** — trust but verify; detective over preventive; compensating controls.
9. **Lean financial management** — Beyond Budgeting; rolling forecasts; fund teams, not projects.
10. **IT is a competitive advantage** — "You build it, you run it"; platforms are products; one success criterion for clouds.
11. **Culture change is behavior change** — start with Improvement Kata + Coaching Kata; survive learning anxiety.
12. **Start where you are** — small, focused, measurable; iterate relentlessly; let the early wins do the persuasion.

---

## Cross-References

- Related: `[[Lean_Startup.md]]` — Ries' lean startup loop applied inside the enterprise
- Related: `[[Continuous_Delivery.md]]` — engineering practices the book assumes
- Related: `[[Toyota_Kata.md]]` — Improvement Kata & Coaching Kata origin
- Related: `[[Beyond_Budgeting.md]]` — Bogsnes' financial management framework
- Related: `[[The_Art_of_Action.md]]` — Bungay on Mission Command and the three gaps
- Topic index: `[[../INDEX.md]]`