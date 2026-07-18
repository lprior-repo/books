# Technology Strategy Patterns

**Author:** Eben Hewitt
**Topic tags:** `#general` `#strategy` `#architecture` `#leadership`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Technology Strategy Patterns/Technology Strategy Patterns.md` · `summaries/Technology_Strategy_Patterns.md`

## TL;DR
A catalog of 39 patterns for formulating, communicating, and gaining approval for technology strategy. Patterns are organized into three groups: Analysis (foundational critical thinking), Creation (PESTEL, Five Forces, Stakeholder Matrix, etc., narrowing from world to department scope), and Communication (Aristotelian rhetoric, narrative structure, executable templates). Apply when an architect/CTO must align a tech roadmap with business strategy, evaluate build-vs-buy, manage technical debt as a portfolio, or influence executive decisions.

---

## Best Practices by Topic

### The Architect-Strategist Convergence

**Principle:** Technologists are first and foremost businesspeople. The roles of Chief Architect and Chief Strategist are more blurred and more aligned than ever. An architect's work is "the set of strategic and technical models that create a context for position (capabilities), velocity (directedness, ability to adjust), and potential (relations) to harmonize strategic business and technology goals."

**Three primary concerns of the architect:**
1. **Contain entropy** — define standards, conventions, toolsets that prevent systems from degrading into chaos.
2. **Specify nonfunctional requirements** — the "-ilities": scalability, availability, maintainability, manageability, monitorability, extensibility, interoperability, portability, security, performance.
3. **Determine trade-offs** — every decision involves trade-offs; the architect makes them explicit and value-judges them against business strategy.

The Triumvirate: *Strategy, Culture, and Execution.* "Culture eats strategy for breakfast" (Peter Drucker) — even a brilliant strategy fails without the right culture and execution capability.

**Do:**
- Speak business. Frame technology in terms of position, velocity, and potential.
- Tie every architectural decision to the broader business strategy.
- Maintain two versions of the strategy: one detailed for the executive team, one short for broader teams.

**Don't:**
- Don't pretend the architect role is purely technical. The Vitruvian architect was "educated in diverse fields, from optics and philosophy to music and politics."
- Don't accept trade-off discussions without naming the business impact.

*Ref: Technology Strategy Patterns.md — "Chapter 1. Architect and Strategist"*

---

### MECE — Mutually Exclusive, Collectively Exhaustive

**Principle:** McKinsey's foundational analysis tool. The single most important thing to improve a strategy is to become good at making lists, because everything in strategy starts as a list. A MECE list has two properties:

- **Mutually Exclusive:** no element overlaps with any other.
- **Collectively Exhaustive:** all elements together completely define the category.

Examples: the four suits of cards; Revenue - Cost = Profit. Non-MECE: lists that leave out elements, mix levels of abstraction, or include subcategories alongside their parents.

**Rule of Three:** find the level of abstraction that keeps lists to three (or five) items. People remember odd-numbered, short lists better.

**Do:**
- Make lists MECE before evaluating them.
- State the audience and why they care for every list.
- Use MECE for: selection criteria, options considered, advantages/disadvantages, ranked as Good/Better/Best.

**Don't:**
- Don't mix abstraction levels in one list (e.g., "reliability, performance, AWS, security" mixes "the -ilities" with a specific technology).
- Don't accept a list that overlaps with another list.

*Ref: Technology Strategy Patterns.md — "Chapter 2. Analysis" / "MECE"*

---

### Logic Tree — Decompose Problems and Solutions

**Principle:** Two types of Logic Tree:
- **Diagnostic:** starts with a problem, breaks it into possible causes (root cause analysis).
- **Solution:** starts with a solution requirement, breaks it into component parts.

**Do:**
- Start with the problem statement at the top.
- Create a MECE set of branches for possible causes.
- Continue decomposing until reaching actionable items.
- Distinguish problems (broken) from opportunities (new possibilities for growth).

**Don't:**
- Don't mix diagnostic and solution trees. They run in opposite directions.
- Don't stop decomposing at vague categories. Each leaf should be actionable.

*Ref: Technology Strategy Patterns.md — "Chapter 2. Analysis" / "Logic Tree"*

---

### Hypothesis-Driven Analysis — Don't Wait for Perfect Information

**Principle:** Form a hypothesis quickly, gather data to test it, revise if needed. Don't wait for perfect information before acting. Apply Wittgenstein's propositional logic structure:

1. **What is the conjunct of propositions describing the problem?** Verifiable propositions.
2. **What semantics characterize these propositions?** When people say "everyone," they never mean everyone — define the domain of discourse precisely.
3. **What are the possible outcomes?** Inductive (specific → general) and deductive (general → specific) reasoning.
4. **What are the probabilities of each outcome?** Beware Russell's turkey: fed every day for 364 days infers day 365 will be the same — but day 365 is Thanksgiving.
5. **What ease/impact scoring suggests the right strategy?** Plot on a 2x2 grid. Prioritize high-ease + high-impact (green) first; low-ease + low-impact (red) last.

**Signal vs. Noise:** apply the 80/20 (Pareto) rule. "A poker player who folds bad hands, learns basic odds, and makes modest efforts to read opponents can match the decisions of experts 80% of the time."

**Objects and Relations:** determine objects, their necessary vs. contingent relations, and predicates (attributes). Relations exist on a spectrum: identity → equality → association → predicate → correlation → causation. **True causation is rare in business; most relationships are correlations or associations.** Be careful not to overstate causal relationships.

**Strategic Analysis as Machine Learning:** hypothesize a function `Y = f(x)` that explains data and predicts outcomes — the same inductive/deductive structure.

**Do:**
- State hypotheses as verifiable propositions.
- Plot ease × impact early. Avoid the low-impact, high-effort quadrant.
- Distinguish correlation from causation explicitly in recommendations.

**Don't:**
- Don't present a hypothesis as proven fact until evidence supports it.
- Don't wait for complete data; ship the hypothesis, then test.

*Ref: Technology Strategy Patterns.md — "Chapter 2. Analysis" / "Hypothesis"*

---

### PESTEL — World Context

**Principle:** Francis Aguilar (1967) — analyze Political, Economic, Social, Technological, Environmental, Legal climates to determine strategic direction. PESTEL itself is MECE. Each category is viewed through the lens of your specific industry.

**Process:** gather data without mixing in biases → state insights → make local recommendations. Update annually or after major events. The PESTEL goes into the Strategy Deck appendix and is shared with non-technical colleagues to validate findings.

**Do:**
- Run PESTEL at least annually.
- View each category through your specific industry.
- Include in the Strategy Deck appendix.

**Don't:**
- Don't mix biases into the data gathering phase.
- Don't treat PESTEL as one-off. Refresh after major events.

*Ref: Technology Strategy Patterns.md — "Chapter 3. World Context" / "PESTEL"*

---

### Scenario Planning and the Futures Funnel

**Principle:** Originating at RAND in the 1950s. Scenario Planning combats the default "Do Nothing" strategy and its optimism bias. Process:

1. Research and interview key leaders (several weeks).
2. Two-to-three-day workshop with a diverse group.
3. Break into small groups to generate and work through scenarios.
4. Distill ideas through private voting.
5. Have teams argue for their preferred scenarios.
6. Leadership uses this as input for strategic decisions.

**The Futures Funnel** is a single-slide visual: concentric circles — *Possible* (all that could happen) → *Plausible* (reasonable to expect; "giant lizard destroying Portland is possible but not plausible") → *Probable* (likely) → *Preferred* (what you want; smallest intersection). Serves as a quick substitute for full Scenario Planning.

**Do:**
- Use scenario planning when "Do Nothing" is the implicit default.
- Assign levels of uncertainty rather than trying to estimate precise probabilities.
- Combine with the Futures Funnel for a single-slide executive view.

**Don't:**
- Don't promise precise probabilities when the inputs are uncertain.
- Don't run the workshop with homogeneous groups — diversity produces better scenarios.

*Ref: Technology Strategy Patterns.md — "Chapter 3" / "Scenario Planning", "Futures Funnel"*

---

### Backcasting — From Future to Present

**Principle:** Inverse of forecasting. State the desired future as if it has already happened, then work backward to determine what had to occur.

**Steps:**
1. Create a concrete, measurable vision of the Beautiful Future (e.g., "cut the power cord on the legacy system").
2. Hypothesize the immediately prior necessary state (antecedents).
3. Repeat working backward through antecedents until reaching the current state.
4. Consider consequents: ensure true premises cannot produce false consequences (logical validity).

At each step, consider impacts on people, process, and technology. Tag each antecedent hypothesis with a probability. Distinguish dependent variables (unknowns to control) from independent variables (levers to pull).

**Do:**
- Use backcasting when the future is plausible but the path is unclear.
- Tag antecedents with probability and with P/P/T impact.

**Don't:**
- Don't allow consequents to contradict premises. Check logical validity.

*Ref: Technology Strategy Patterns.md — "Chapter 3" / "Backcasting"*

---

### SWOT and Porter's Five Forces — Industry Context

**SWOT** provides a single-slide view across two axes: placement (internal/external) and potential (helpful/harmful).
- Strengths (internal, helpful) | Weaknesses (internal, harmful)
- Opportunities (external, helpful) | Threats (external, harmful)

Create by interviewing people across levels and departments. Use when joining a new organization, planning legacy evolution, or developing departmental strategy.

**Porter's Five Forces (1980):**
1. **Threat of New Entrants** — switching costs, capital requirements, brand loyalty, regulation.
2. **Ease of Substitution** — products using different tech to solve the same economic need.
3. **Bargaining Power of Customers** — dependency on distribution, differentiation, switching costs.
4. **Bargaining Power of Suppliers** — for software, suppliers are compute/storage infrastructure and developers. The *talent life cycle*: emerging tech has incredible differentiation and high salaries → supply grows and differentiation decreases → commoditized and talent easily substituted.
5. **Industry Rivalry** — public perception of product differentiation.

Apply by creating a slide for each force, claiming how your tech supports or defends against it, tagging threats red/yellow/green, making recommendations.

**Do:**
- Combine SWOT (single-slide summary) with Five Forces (deep dive per force).
- Apply the talent life cycle when forecasting talent costs for emerging technologies.
- Use the traffic-light tagging to make priorities immediately visible.

**Don't:**
- Don't treat SWOT as a substitute for analysis. It's a *summary* of analysis.
- Don't omit any of the five forces.

*Ref: Technology Strategy Patterns.md — "Chapter 4. Industry Context"*

---

### Ansoff Growth Matrix — Risk vs. Growth

**Principle:** Four growth strategies, in order of risk:
- **Market Penetration** (lowest risk) — sell more of existing products to existing customers.
- **Market Development** — sell existing products to new markets (Canon copiers to individuals).
- **Product Development** — create new products for current markets (AWS adding new services).
- **Diversification** (highest risk) — new products in new markets; portfolio resilience.

**Do:**
- Default to lower-risk strategies first when the company's life cycle stage doesn't justify higher risk.
- Use Diversification for portfolio resilience, not for the core business.

**Don't:**
- Don't pick Diversification as the default — the risk is highest.

*Ref: Technology Strategy Patterns.md — "Chapter 4" / "Ansoff Growth Matrix"*

---

### Stakeholder Alignment — Do Something That Matters to Someone Who Matters

**Principle:** "The way to be successful is to do something that matters to someone who matters." Misaligned projects get cancelled. Gain alignment from three groups: leaders (fund and champion), teams (execute), peers (otherwise ignore or undermine).

**Stakeholder List:** name, title, organization, contact for 10-30 key stakeholders.

**Stakeholder Matrix:** Influence and Impact scores (1-5) on a 2x2 chart:
- Monitor (low/low) — check in occasionally
- Maintain Confidence (high influence, low impact) — send reports, invite to steering
- Keep Informed (low influence, high impact) — email updates, town halls
- Collaborate (high/high) — actively co-create

**Do:**
- Build the stakeholder matrix before drafting the strategy.
- Identify the "Collaborate" segment first. They are your co-authors.

**Don't:**
- Don't ship a strategy without naming who matters and why.

*Ref: Technology Strategy Patterns.md — "Chapter 5" / "Stakeholder Alignment"*

---

### RACI — One Accountable, Many Responsible

**Principle:** RACI = Responsible / Accountable / Consulted / Informed.

- **Responsible:** hands-on workers completing tasks.
- **Accountable:** *exactly one* person answerable for each item's delivery. (The most common mistake is assigning multiple accountables.)
- **Consulted:** SMEs whose advice changes the work.
- **Informed:** one-way status updates, no decision authority.

**Do:**
- Assign exactly one Accountable per item.
- Use RACI for projects that have many people; ignore for tiny teams.

**Don't:**
- Don't assign multiple Accountables. If you do, you've assigned none.
- Don't confuse Accountable with Responsible — they're different roles.

*Ref: Technology Strategy Patterns.md — "Chapter 5" / "RACI"*

---

### Life Cycle Stage and the Value Chain

**Life Cycle Stage:** introduction, growth, maturity, decline.
- Introduction: survival mode, revenue focus, expand from key customers.
- Growth (20%+): speed to market, strengthen core.
- Maturity (5-8%): alternate growth strategies, platform plays, cross-selling.
- Decline (0-5% or negative): cost-cutting spiral risk, requires holistic strategy.

Companies are not required to grow indefinitely. "The world's oldest companies (some 1,500 years old) are mostly small businesses serving fundamental human needs."

**Value Chain (Porter, 1985):** distinguishes *value creators* (make products and deliver services to customers) from *support departments* (HR, Legal, Finance, Infrastructure). Companies that fail to recognize this distinction "allow support functions to bureaucratize and impede value creators."

**Do:**
- Calibrate strategy to life cycle stage — what works in growth fails in maturity.
- Distinguish value creators from support departments in your org design.

**Don't:**
- Don't grow for growth's sake.
- Don't bureaucratize support departments.

*Ref: Technology Strategy Patterns.md — "Chapter 5" / "Life Cycle Stage", "Value Chain"*

---

### Growth-Share Matrix (BCG) and Core/Innovation Wave

**BCG Growth-Share Matrix:**
- **Stars** (high growth, high share) — invest.
- **Cash Cows** (low growth, high share) — maximize profit.
- **Question Marks** (high growth, low share) — invest selectively or divest.
- **Dogs** (low growth, low share) — divest or liquidate.

**Core/Innovation Wave** — balance investment between maintaining core and pursuing innovation. Three horizons (McKinsey):
- **Horizon 1:** Core business optimization — ~70% of investment.
- **Horizon 2:** Adjacent market expansion — ~20% of investment.
- **Horizon 3:** Transformational new ventures — ~10% of investment.

Today's Horizon 3 becomes tomorrow's Horizon 1. Companies must continuously invest across all three.

**Do:**
- Tag every strategic initiative with its horizon.
- Maintain the 70/20/10 split even when cash flow tempts you to over-invest in Horizon 1.
- Treat Question Marks honestly — invest selectively or divest; don't let them linger.

**Don't:**
- Don't starve Horizon 3 because it doesn't show ROI in the current quarter.
- Don't treat Dogs as pets.

*Ref: Technology Strategy Patterns.md — "Chapter 5" / "Growth-Share Matrix", "Core/Innovation Wave"*

---

### Principles, Practices, Tools — The Three Layers of Tech Direction

**Principle:** Communicate technology direction through three layers:
- **Principles:** enduring rules that guide decisions (e.g., "Data is an asset").
- **Practices:** methods and processes teams follow (e.g., continuous integration).
- **Tools:** specific technologies used to implement practices.

**Process Posture Map** assigns one of five tags to each process:
- **Start** (not doing this but should)
- **Develop** (doing it somewhat)
- **Optimize** (doing it well and improving)
- **Maintain** (doing it well)
- **Sunset** (should stop)

**Current and Future Model:** state both, show the transition. Use a **Sankey diagram** to visualize how principles flow into practices and practices into tools.

**Business Process Mapping:** visual representations of business processes to identify inefficiencies and opportunities for automation.

**Law of the Product of Probabilities:** "If 10 things each need to happen with 90% probability, the chance of all succeeding is only 35%." Each 90%-likely step multiplies the others — long dependency chains are mathematically hostile to delivery.

**Do:**
- Use the three layers (Principles → Practices → Tools) consistently.
- Tag every process with a posture from the Process Posture Map.
- Visualize the current-to-future transition with a Sankey diagram.

**Don't:**
- Don't pick tools before principles. Tools change; principles should be enduring.
- Don't chain 10 dependencies at 90% each.

*Ref: Technology Strategy Patterns.md — "Chapter 6. Department Context" / "Principles, Practices, Tools"*

---

### Application Portfolio Management — Treat Tech Debt as a Portfolio

**Principle:** APM evaluates the full portfolio of applications on two axes: business value and technical quality. Four categories on a 2x2 grid:
- **Invest** (high value, high quality).
- **Tolerate** (high value, low quality — needs modernization).
- **Migrate** (low value, high quality — consider consolidation).
- **Eliminate** (low value, low quality).

**Capability Mapping** links tech investments to business capabilities, ensuring alignment.

**Business and Technology Attributes:** evaluate applications against cost, risk, business value, technical fit, agility to make informed portfolio decisions.

**Do:**
- Inventory every application. (EBSCO: "the first application inventory in the company's history" was a major breakthrough from the Team Topologies adoption.)
- Tag every application with the APM quadrant.
- Map tech investments to business capabilities explicitly.

**Don't:**
- Don't run an APM exercise without executive sponsorship. Eliminations need authority.
- Don't Tolerate indefinitely — Tolerate is a transition category.

*Ref: Technology Strategy Patterns.md — "Chapter 6" / "Application Portfolio Management"*

---

### Build / Buy / Partner — Three Options for Tech Capabilities

**Principle:** Three options for acquiring tech capabilities:
- **Build** — max control, customization, but longest time to market, highest risk. Ask: Is this what you want to spend organizational resources on? Do you have the resources to complete it *better* than what's available? Will you realize meaningful cost savings?
- **Buy** — quickest time to market but least control, customization limits, expensive, requires changing business processes to fit the software.
- **Partner** — shared risk and resources but requires alignment of interests, careful contract negotiation, governance.

Evaluate each option against strategic fit, cost, time to market, risk, capability.

**Do:**
- Default to Buy/Partner for non-differentiating capabilities.
- Reserve Build for capabilities that provide competitive advantage.
- For each Build candidate, ask whether you'll complete it better than what's available.

**Don't:**
- Don't Build because "we can." Build only when Build produces a capability you cannot Buy or Partner your way into.
- Don't Partner without governance — partners drift.

*Ref: Technology Strategy Patterns.md — "Chapter 8. Templates" / "Build/Buy/Partner"*

---

### Technology Radar — Categorize Tech into Four Rings

**Principle:** Inspired by ThoughtWorks' Technology Radar. Four rings:
- **Adopt** — ready for production use.
- **Trial** — worth pursuing actively in projects.
- **Assess** — worth exploring.
- **Hold** — proceed with caution or avoid.

**Do:**
- Maintain a Technology Radar as a living document.
- Move technologies through the rings as evidence accumulates.
- Publish the radar organization-wide.

**Don't:**
- Don't put technologies in Adopt without production evidence.
- Don't leave items stuck in Assess for years — either promote or move to Hold.

*Ref: Technology Strategy Patterns.md — "Chapter 8. Templates" / "Technology Radar"*

---

### Directional Costing — Three Levels of Precision

**Principle:** Cost estimates at three levels of precision:
- **Rough Order of Magnitude (ROM):** -25% to +75% accuracy.
- **Refined Estimate:** -10% to +25% accuracy.
- **Realistic Estimate:** -5% to +10% accuracy.

Categories: people, software licensing, infrastructure, training, contingency.

**Do:**
- Use ROM when scoping; refined at design; realistic only after detailed planning.
- Include contingency even at the ROM stage.

**Don't:**
- Don't promise a Realistic Estimate when you only have ROM data. That's a project planning failure.

*Ref: Technology Strategy Patterns.md — "Chapter 8. Templates" / "Directional Costing"*

---

### The 30-Second Answer — Distillation, Not Simplification

**Principle:** Be able to articulate the essence of your strategy in half a minute. This is not a simplification exercise but a distillation one. If you cannot state your strategy concisely, you do not truly understand it. The 30-Second Answer should state the problem, the proposed solution, and the expected benefit.

**Do:**
- Practice your 30-Second Answer until it's natural.
- Test it on a cold audience (someone unfamiliar with the work).

**Don't:**
- Don't hide behind complexity. If you can't summarize, you don't understand.
- Don't omit the benefit. "What problem does this solve, and for whom?"

*Ref: Technology Strategy Patterns.md — "Chapter 7. Approach Patterns" / "30-Second Answer"*

---

### Ars Rhetorica — Ethos, Pathos, Logos

**Principle:** Aristotle's Rhetoric — three persuasive appeals:
- **Ethos** — credibility and character.
- **Pathos** — emotions and values.
- **Logos** — logical arguments with data.

A compelling strategy presentation uses all three.

**Logical fallacies to avoid:**
- *Affirming the consequent* ("If P then Q. Q is true. Therefore P.")
- *Blind authority fallacy* — citing someone's title or big tech company as proof.

**Do:**
- Open with Ethos (who you are), weave in Pathos (why this matters to the audience's values), close with Logos (data supports the recommendation).
- Test your arguments for common fallacies.

**Don't:**
- Don't rely on Logos alone — engineers often default to data-only arguments and lose the room.
- Don't argue from authority ("Google does it") without the underlying reasoning.

*Ref: Technology Strategy Patterns.md — "Chapter 7" / "Ars Rhetorica"*

---

### Dramatic Structure — Status Quo → Inciting Incident → Rising Action → Climax → Resolution

**Principle:** Borrowed from narrative theory. Structure the strategy presentation as a story:
1. **Establish the Status Quo** — show the current state.
2. **Create an Inciting Incident** — reveal the problem or opportunity.
3. **Rising Action** — build the case with data and analysis.
4. **Climax** — present the strategic recommendation.
5. **Resolution** — show the path forward.

**Shock and Awe:** open with dramatic data that grabs attention (e.g., "60 items of technical debt" or "P1 incidents up 300% over three years").

**Do:**
- Open with Shock and Awe data, not throat-clearing.
- Save the recommendation for the Climax — don't bury it.

**Don't:**
- Don't open with background. Audiences disengage before you reach the point.

*Ref: Technology Strategy Patterns.md — "Chapter 7" / "Dramatic Structure"*

---

### Fait Accompli — Create Inevitability

**Principle:** Create a sense of inevitability around your strategy by demonstrating momentum. Show what has already been accomplished, what is in progress, and what naturally follows. This creates confidence that the strategy is achievable.

**Do:**
- Open with what's already in flight.
- Frame recommendations as the natural next step.

**Don't:**
- Don't claim inevitability when the work isn't already underway. That's hollow.

*Ref: Technology Strategy Patterns.md — "Chapter 7" / "Fait Accompli"*

---

### The Ask Deck — Imperil the Hero, Save the Hero, Ask

**Principle:** Specifically designed to request approval and resources. Structure:
1. **Imperil the Hero** — Shock and Awe showing the dire situation.
2. **Let the Data Drive** — methodical, objective data.
3. **Save the Hero** — offer the Path Forward (vision of salvation).
4. **The Ask** — explicitly ask for a yes decision. "The reason you don't get the sale is you never actually ask."
5. **Appendix** — supporting details (PESTEL, Five Forces, etc.).

**Do:**
- End every strategy presentation with an explicit, specific Ask.
- Tie the Ask to the Imperil-and-Save narrative.

**Don't:**
- Don't be ambiguous about what you're asking for. Resources? Headcount? Approval to proceed?

*Ref: Technology Strategy Patterns.md — "Chapter 9. Decks" / "Ask Deck"*

---

### MergeSort Meeting — The Tactical Plan Generator

**Principle:** Converts strategy into executable work:
1. Call a meeting with clearly stated scope.
2. Have everyone independently create lists organized by project categories.
3. Give people time to populate their lists independently (preventing groupthink).
4. Bring raw material together and merge/sort the lists.
5. Prioritize collaboratively.

Inspired by the computer science algorithm. Ensures all voices are heard, prevents loud voices from dominating, generates more ideas through independent brainstorming before collaborative synthesis.

**Do:**
- Give explicit independent-list-creation time before any group discussion.
- Sort by category, not by voter.

**Don't:**
- Don't brainstorm in a group. Brainstorm alone; synthesize as a group.

*Ref: Technology Strategy Patterns.md — "Chapter 9" / "Tactical Plan"*

---

### Executable Architectures — Architecture as Code

**Principle:** Make architecture definitions executable — write them as code (infrastructure as code, contract testing, architecture fitness functions) so they can be automatically validated rather than becoming shelfware. "Architecture definitions" cover business, application, data, infrastructure perspectives; nonfunctional requirements with measurable targets; principles and constraints; technology stack selections with rationale.

**Do:**
- Convert architectural decisions into fitness functions and run them in CI.
- Use contract testing to enforce service boundaries.
- Express the architecture as testable statements and math, not prose.

**Don't:**
- Don't ship architecture as shelfware. Documents that nobody reads fail.

*Ref: Technology Strategy Patterns.md — "Chapter 8" / "Architecture Definition"*

---

### Deconstruction — Three Causes and the Scalable Business Machine

**Principle:** Hewitt identifies three causes of problems: **people, process, technology.** He also introduces **Scopes Without Center** — the tendency to analyze systems without identifying the true center or core.

**Synthetic Decomposition** (vs. top-down analysis): understand how parts combine to create wholes.

**The Scalable Business Machine:** Hewitt's framework for what makes a business scalable:
- **Standardization** — common patterns and platforms.
- **Automation** — repeatable workflows.
- **Instrumentation** — observability and metrics.
- **Resilience** — graceful degradation, fault tolerance.

Key aspects: modularity, loose coupling, separation of concerns, evolutionary architecture.

**Do:**
- Apply the people/process/technology triad when triaging failures.
- Build a Scalable Business Machine by designing for all four attributes (standardization, automation, instrumentation, resilience).
- Identify the *center* — the most leveraged capability. Most analysis misses it.

**Don't:**
- Don't default to "people" as the cause. Structure often dominates.
- Don't optimize one attribute at the expense of the others.

*Ref: Technology Strategy Patterns.md — "Chapter 7" / "Deconstruction"*

---

## Anti-Patterns & Common Mistakes

- **Adopting without evidence:** Putting a technology in the Adopt ring on the radar before it's proven in production. *Fix:* Require production evidence for Adopt; default to Assess.
- **Build by default:** Choosing Build because the team can, not because the capability is differentiating. *Fix:* Default to Buy/Partner for non-differentiating capabilities.
- **Fait accompli without action:** Claiming inevitability without the work to back it up. *Fix:* Show what's already in flight before claiming momentum.
- **Tolerate forever:** Letting Tolerate applications linger indefinitely. *Fix:* Tolerate is a transition category; every app must move to Invest, Migrate, or Eliminate on a time-boxed plan.
- **Starving Horizon 3:** Investing only in Horizon 1 because it shows current ROI. *Fix:* Maintain 70/20/10 across horizons even when tempted to over-invest.
- **Treating Dogs as pets:** Keeping low-growth, low-share products because "someone loves it." *Fix:* Divest or liquidate based on the matrix.
- **Multiple Accountables:** Assigning more than one Accountable per item. *Fix:* Exactly one Accountable per item.
- **Anecdotal causation:** Claiming "we tried X and Y improved, so X caused Y." *Fix:* Be explicit about whether relationships are causal, correlated, or associative.
- **Data-only arguments:** Relying on Logos alone and losing the room. *Fix:* Use Ethos, Pathos, and Logos together.
- **Shelfware architecture:** Publishing architecture documents nobody reads or validates. *Fix:* Express as fitness functions; run in CI.
- **Bureaucratized support departments:** HR, Legal, Finance impeding value creators. *Fix:* Distinguish value creators from support in org design; protect value creators.
- **Big-bang strategy:** Spending a year on the strategy deck, never shipping. *Fix:* Build a Ghost Deck early; ship incremental Ask Decks.
- **Static adoption of Team Topologies:** Treating a pattern catalog as a destination rather than building blocks. (Same lesson applies to strategy patterns.)
- **Calling without asking:** Presenting analysis without an explicit Ask. *Fix:* End every strategy meeting with a specific Ask.

---

## Decision Heuristics / Checklists

- **Scope of analysis:**
  - Database upgrade → MECE, Logic Tree, Stakeholder Matrix, RACI.
  - Multi-year enterprise strategy → all 39 patterns.
- **List quality:** Mutually Exclusive + Collectively Exhaustive? Three to five items at the right abstraction level?
- **Hypothesis quality:** Plotted on ease × impact 2x2? Tagged with probability? Russell's-turkey-aware (sample size, base rate)?
- **Strategy fitness:**
  - Does it pass the Triumvirate check (Strategy + Culture + Execution)?
  - Does it pass the 30-Second Answer test?
  - Does it pass the Stakeholder Matrix check (someone who matters will support it)?
- **Build vs. Buy vs. Partner:**
  - Differentiating capability? → Build (if you can do it better than available).
  - Commodity capability? → Buy.
  - Capability that requires alignment with another org? → Partner (with governance).
- **Horizon split:** 70% Horizon 1 / 20% Horizon 2 / 10% Horizon 3?
- **APM quadrant:** Every application tagged? Tolerate items have a transition date?
- **Communication readiness:** Does the deck use dramatic structure? Ethos/Pathos/Logos? Ends with an Ask?
- **Tactical plan readiness:** MergeSort Meeting scheduled? Independent list-creation time allocated?

---

## Key Takeaways

1. **Strategy is about making choices** — deciding what to do and, equally important, what not to do.
2. **The architect and strategist roles are converging.** Speak business.
3. **Lists are the foundation of strategy** — make them MECE; the Rule of Three helps recall.
4. **Start with the broadest context** — PESTEL → industry → corporate → department.
5. **Hypothesis-driven analysis accelerates results** — don't wait for perfect information.
6. **Communication is as important as analysis.** Use Aristotle's three appeals + dramatic structure + Shock and Awe.
7. **Alignment is essential** — your strategy must matter to the people who matter.
8. **Every trade-off reduces to time and money.** Make trade-offs explicit.
9. **Use patterns selectively based on scope.** Match the patterns to the problem.
10. **Executable architectures beat shelfware** — fitness functions, contract testing, architecture as code.
11. **The triumvirate of strategy, culture, and execution must be aligned.**
12. **Separate signal from noise** using the 80/20 rule. Good-enough-now beats perfect-too-late.

---

## Cross-References
- Related: [[../Learning_Systems_Thinking.md]] (paradigms, leverage points, organizational communication)
- Related: [[../Team_Topologies.md]] (organizational design for flow, Team API)
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] (platforms as product — Principles/Practices/Tools)
- Related: [[../Platform_Engineering_Camille_F.md]] (platform strategy)
- Related: [[../Crafting_Engineering_Strategy.md]] (engineering strategy specifics)
- Topic index: [[../INDEX.md]]