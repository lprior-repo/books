# Technology Strategy Patterns - Comprehensive Summary

**Author:** Eben Hewitt
**Publisher:** O'Reilly Media

---

## Introduction

*Technology Strategy Patterns* by Eben Hewitt provides architects, product managers, technology managers, and executives with a shared language of repeatable, practical patterns and templates to produce great technology strategies. Hewitt developed 39 patterns over a decade of serving as CTO, CIO, and Chief Architect for several global technology companies. The book bridges the gap between technologists who want their ideas heard, understood, and funded and the business leaders who control budgets and set organizational direction. Hewitt argues that technologists are first and foremost businesspeople, and that the roles of Chief Architect and Chief Strategist are more blurred and more aligned than ever. The patterns are divided into three categories: Analysis (foundational critical thinking tools), Creation (patterns for building the strategy itself), and Communication (patterns for conveying the strategy compellingly).

---

## Part I: Context - Architecture and Strategy

### The Origins of Patterns

Hewitt traces the concept of patterns to Christopher Alexander, a UC Berkeley professor who in the 1970s cataloged common architectural solutions in *A Pattern Language*. The Gang of Four later applied this idea to software design in their seminal *Design Patterns*. Hewitt extends the concept further, taking repeated solutions found in the work of business strategists and applying them to technology strategy work. The use of patterns as a structuring mechanism makes the book easy to use as a reference after reading.

### Applying the Patterns

There are five basic steps to formulating a strategic technology analysis:
1. Establish context (analyze world trends, industry forces, and stakeholders)
2. Understand your competition, the market, and the technology landscape
3. Identify strategic options in your products, services, and technology roadmap
4. Evaluate those options
5. Make a compelling recommendation with a coherent strategy to gain approval and resources

You do not need to use all patterns for every project. The patterns can be picked and chosen depending on the scope of the problem, from a localized database upgrade (needing just MECE, Logic Tree, Stakeholder Matrix, and RACI) to a full multiyear enterprise strategy (needing all patterns).

### Chapter 1: Architect and Strategist

#### Business Strategies

Hewitt opens with three illustrative business strategy examples:

**Marketing at Michelin:** The Michelin Guide, created in 1900, is now the gold standard for fine dining ratings worldwide. But Michelin is a tire company. With only a few thousand cars in France at the time, the company created the guide to inspire people to drive more, thereby selling more tires. This innovative, counterintuitive strategy worked for decades, though today the guides lose the company 19 million euros annually, having become disconnected from their original purpose of driving tire sales.

**Acquisition and Integration at Oracle:** Starting in 2007, Oracle pursued a strategy of making its software number one or two in every category, or buying the market leader. Between 2008 and 2013, Oracle bought nearly 60 companies at a rate of almost one per month, spending $45 billion. Thomas Kurian's technology strategy mandated that all acquired products use Oracle's middleware stack. While this supported the business strategy of aggressive acquisitions, Oracle spent considerable time on refactoring rather than innovation, causing it to miss the cloud and machine learning revolutions entirely.

**Differentiation at Xerox and Canon:** In 1968, Xerox had 95% market share in copiers with machines costing $80,000-$129,000. Canon developed an alternative copying process using its existing capabilities in micro-electronics and optics, designed copiers with only eight basic parts, made the primary assembly disposable, and built copiers around the manufacturing process for robotic assembly. Canon priced its copiers at $700-$1,200, opening an entirely new market segment. Within five years, Xerox's market share dropped from 95% to 14%. This story illustrates how technology and business strategy can work hand in hand as copilots.

#### The Architect's Role

Hewitt defines the architect's work as comprising "the set of strategic and technical models that create a context for position (capabilities), velocity (directedness, ability to adjust), and potential (relations) to harmonize strategic business and technology goals." He identifies three primary concerns:

1. **Contain Entropy:** Drawing from the second law of thermodynamics, the architect defines standards, conventions, and toolsets that prevent systems from degrading into chaos. The architect who contains entropy states a vision, shows a roadmap, garners support through communication of guidelines, and creates clarity to ensure the right things are done right.

2. **Specify Nonfunctional Requirements:** The architect is responsible for specifying how the system will realize both functional and nonfunctional requirements (the "-ilities": scalability, availability, maintainability, manageability, monitorability, extensibility, interoperability, portability, security, and performance). This is expressed through an architecture definition document structured around business, application, data, and infrastructure perspectives.

3. **Determine Trade-offs:** Every architectural decision involves trade-offs. Adding security reduces performance; sharding databases adds complexity; robust monitoring generates huge log volumes. The architect's role is to make these challenges explicit and make value judgments about how to balance solutions, guided by the broader business strategy.

Hewitt grounds these responsibilities in Vitruvius's principles from *de Architectura* (first century BC): firmitas (solidity), utilitas (utility), and venustas (beauty/delight). An architect must be educated in diverse fields, from optics and philosophy to music and politics.

#### The Strategist's Role

The word "strategy" originates from the Greek *strategos*, referring to the military general's work. Antoine-Henri Jomini, writing about Napoleon's methods in 1803, is considered the founder of modern strategy. His definition divides strategy neatly: "Strategy decides where to act; logistics brings the troops to this point; tactics decides the manner of execution."

For Hewitt, strategy is about determining problems and opportunities, defining them properly, and shaping a course of action that gives the business the greatest advantage. It involves balancing goals, methods, and available resources. Business strategies typically concern organizational goals, operating models, culture, talent strategy, and facilities strategy.

Hewitt introduces the **Triumvirate**: Strategy, Culture, and Execution. Peter Drucker's adage "Culture eats strategy for breakfast" reminds us that even a brilliant strategy fails without the right culture and execution capability. The strategist must create two versions of the strategy: one honest and detailed for the executive team, and a shorter public version for broader teams.

---

## Part II: Creating the Strategy

### A Logical Architecture of the Creation Patterns

Hewitt presents 19 creation patterns organized into five concentric categories of narrowing scope:
- **Analysis** (broadest): MECE, Logic Tree, Hypothesis
- **World**: PESTEL, Scenario Planning, Futures Funnel, Backcasting
- **Industry**: SWOT, Porter's Five Forces, Ansoff Growth Matrix
- **Company**: Stakeholder Alignment, RACI, Life Cycle Stage, Value Chain, Growth-Share Matrix, Core/Innovation Wave, Investment Map
- **Department** (narrowest): Principles/Practices/Tools, Application Portfolio Management

### Chapter 2: Analysis

#### MECE (Mutually Exclusive, Collectively Exhaustive)

MECE is a McKinsey-created tool and one of the most useful in the strategist's toolkit. It dictates the relation of content in your lists but not their format. The single most important thing to improve your chances of making a winning technology strategy is to become good at making lists, because everything in strategy starts as a list. A properly conceived list must answer two questions: Who is the audience, and why do they care?

A MECE list has two properties:
- **Mutually Exclusive:** No element overlaps with any other
- **Collectively Exhaustive:** All elements together completely define the category

Examples of MECE lists: the four suits of cards, the four seasons, Revenue - Cost = Profit. Non-MECE examples include lists that leave out elements, mix levels of abstraction, or include subcategories alongside their parents.

**The Rule of Three:** Find the level of abstraction that keeps lists to three or five items. People naturally understand and remember lists of three or odd-numbered lists better.

**Applying MECE:** When recommending a new database system, create MECE lists of selection criteria, options considered, advantages/disadvantages for each, and rank them as Good/Better/Best. This shows thorough analysis and reduces perceived bias.

#### Logic Tree

The Logic Tree is used by strategy consultants to organize ideas and examine problems quickly. There are two types:

- **Diagnostic Logic Tree:** Starts with a problem and breaks it into possible causes, similar to root cause analysis.
- **Solution Logic Tree:** Starts with a solution requirement and breaks it into component parts that must be built.

To create a Logic Tree: start with the problem statement at the top, create a MECE set of branches for possible causes, and continue decomposing until reaching actionable items. The tree helps distinguish between problems (things that are broken) and opportunities (new possibilities for growth).

#### Hypothesis

The Hypothesis pattern provides a framework for making educated guesses about root problems. Hewitt draws on Wittgenstein's propositional logic and structures analysis around five key questions:

1. **What is the conjunct of propositions describing the problem?** Define the problem through verifiable propositions. A proposition asserts the existence of a state of affairs and should be expressible as a truth value.

2. **What semantics characterize these propositions?** Examine the language carefully. When people say "everyone," they never mean *everyone*. Define the domain of discourse precisely.

3. **What are the possible outcomes?** Enumerate what could happen. Use inductive reasoning (specific observations to general principles) and deductive reasoning (general principles to specific conclusions).

4. **What are the probabilities of each outcome?** Assign probabilities using techniques from probability theory. Beware of Russell's turkey problem: a turkey that has been fed every day for 364 days might reasonably infer it will be fed on day 365, but that day is Thanksgiving.

5. **What ease and impact scoring suggests the right strategy?** Plot hypotheses on a 2x2 grid with "Ease" and "Impact" axes. Prioritize items in the high-ease, high-impact quadrant (green) first, low-ease, low-impact (red) last.

**Signal and Noise:** Apply the 80/20 (Pareto) rule to separate what matters from what doesn't. Just as a poker player who folds bad hands, learns basic odds, and makes modest efforts to read opponents can match the decisions of experts 80% of the time, strategists can make the same recommendations as the best consultants by focusing on the most impactful data points.

**Objects and Relations:** When conducting analysis, determine what the objects are, their necessary and contingent relations, and their predicates (attributes). Relations exist on a spectrum from identity (A=A, tautological) to causation (one thing directly causing another). In between are equality, association, predicate, and correlation. True causation is rare in business; most relationships are correlations or associations. Be careful not to overstate causal relationships.

**Strategic Analysis as Machine Learning:** Hewitt draws a conceptual parallel between strategic analysis and machine learning. In ML, the goal is to find function *f* such that Y = f(x), where *x* is input data and *Y* is the predicted label. Strategy similarly involves hypothesizing a model that explains data and using it to predict outcomes.

### Chapter 3: World Context

This chapter covers four patterns for understanding the broadest context: PESTEL, Scenario Planning, Futures Funnel, and Backcasting.

#### PESTEL

Created by Harvard professor Francis Aguilar in 1967, PESTEL analyzes Political, Economic, Social, Technological, Environmental, and Legal climates to determine strategic direction. PESTEL itself is MECE. Each category is viewed through the lens of your specific industry.

- **Political:** Government policy, trade and taxation changes, terrorism impacts, regulatory differences across countries
- **Economic:** Consumer discretionary income, financing costs, foreign exchange rates, unemployment, GDP trends
- **Social:** Changing attitudes, generational trends, family and educational trends, health consciousness
- **Technological:** Broad technology trends from a business perspective, including IoT, AI, and emerging platforms
- **Environmental:** Ecological influences, climate changes, sustainability trends
- **Legal:** New and pending legislation, sanctions, GDPR impacts, antitrust considerations

Creating a PESTEL involves three steps: gathering data without mixing in biases, stating insights, and making local recommendations. It should be updated annually or after major events. The PESTEL document primarily serves as a reference guide during strategy creation, goes into the Strategy Deck appendix, and can be shared with non-technical colleagues to validate findings.

#### Scenario Planning

Originating at the RAND Corporation in the 1950s, Scenario Planning is an organized way of asking "What if?" It combats the default "Do Nothing" strategy and the optimism bias it creates. The process involves:

1. Conduct research and interview key leaders (several weeks)
2. Hold a two-to-three-day workshop with a diverse group
3. Break into small groups to generate and work through scenarios
4. Distill ideas through private voting
5. Have teams argue for their preferred scenarios
6. Leadership uses this as input for strategic decisions

During the workshop, review trends from the PESTEL, create lists of trends with estimated impacts, build scenarios collaboratively, and assess impacts using Logic Trees. Assign levels of uncertainty rather than trying to estimate precise probabilities.

#### Futures Funnel

The Futures Funnel is a visual representation of the Scenario Planning output, designed to fit on a single slide. It shows concentric circles representing:
- **Possible:** All things that could happen
- **Plausible:** Reasonable to expect (the giant lizard destroying Portland is possible but not plausible)
- **Probable:** Likely to happen
- **Preferred:** What you want to happen (the smallest intersection)

The funnel can also serve as a quick substitute for full Scenario Planning when time is limited. To populate it, consider internal factors (resources, architecture, product portfolio), conceptual factors (correlations, causal chains), and external factors (potential futures, customer behaviors, competitor behaviors).

#### Backcasting

Backcasting is the inverse of forecasting: you state your desired future as if it has already happened, then work backward to determine what had to occur to get there. Steps:

1. Create a concrete, measurable vision of the Beautiful Future (e.g., "cut the power cord on the legacy system")
2. Hypothesize the immediately prior necessary state (antecedents)
3. Repeat the process, working backward through antecedents until reaching the current state
4. Consider consequents: ensure that true premises cannot produce false consequences (logical validity)

At each step, consider impacts on people, process, and technology. Tag each antecedent hypothesis with a probability. Dependent variables (unknowns you want to control) and independent variables (levers you can pull) must be clearly distinguished.

### Chapter 4: Industry Context

#### SWOT

SWOT (Strengths, Weaknesses, Opportunities, Threats) provides a single-slide view organized across two axes: placement (internal vs. external) and potential (helpful vs. harmful).

- **Strengths:** Internal, helpful (competitive advantages)
- **Weaknesses:** Internal, harmful (areas needing improvement)
- **Opportunities:** External, helpful (market possibilities)
- **Threats:** External, harmful (competitive pressures)

Create a SWOT by interviewing people across levels and departments, recording responses tagged as internal/external, and organizing them into the four quadrants. SWOT is applicable when joining a new organization, planning legacy system evolution, creating departmental strategy, or developing broad-based technology strategy.

#### Porter's Five Forces

Developed by Harvard professor Michael Porter in 1980, the Five Forces model identifies pressures bearing down on a business:

1. **Threat of New Entrants:** Risk from new competitors. Consider switching costs, access to distribution channels, government regulations, capital requirements, economies of scale, product differentiation, and brand loyalty.

2. **Ease of Substitution:** Products using different technology to solve the same economic need (e.g., cell phones replacing landlines). Consider perceived differentiation, number of substitutes, availability, propensity to substitute, relative pricing, and switching costs.

3. **Bargaining Power of Customers:** Degree to which customers can influence your business. Consider dependency on distribution channels, product differentiation, bargaining leverage, buyer switching costs, information availability, and price sensitivity.

4. **Bargaining Power of Suppliers:** In software, the two primary suppliers are compute/storage infrastructure and developers. Hewitt describes a talent life cycle: emerging technology has incredible differentiation and high salaries; eventually the supply grows and differentiation decreases; finally the technology becomes commoditized and talent is easily substituted.

5. **Industry Rivalry:** How the public perceives and distinguishes products from competitors. Consider sustainable competitive advantage through innovation, powerful competitive strategies, and transparency levels.

To apply the Five Forces: create a slide for each force, claim how your technology supports or defends against it, tag threats with traffic-light colors (red/yellow/green for high/medium/low), and make recommendations.

#### Ansoff Growth Matrix

Published by Igor Ansoff in the *Harvard Business Review* in 1957, the AGM presents four growth strategies:

- **Market Penetration:** Sell more of existing products to existing customers (lowest risk)
- **Market Development:** Sell existing products to new markets (e.g., Canon selling copiers to individuals)
- **Product Development:** Create new products for current markets (e.g., AWS adding new services)
- **Diversification:** New products in new markets (highest risk, but provides portfolio resilience)

### Chapter 5: Corporate Context

#### Stakeholder Alignment

The way to be successful is to "do something that matters to someone who matters." Misaligned projects that don't matter to leadership will be cancelled. You must gain alignment from three groups: leaders who will fund and champion the strategy, teams who will execute it, and peers who might otherwise ignore or undermine it.

**Stakeholder List:** Create a spreadsheet with name, title, organization, and contact information for 10-30 key stakeholders.

**Stakeholder Matrix:** Add Influence and Impact scores (1-5) and plot on a 2x2 chart:
- **Monitor:** Low influence, low impact -- check in occasionally
- **Maintain Confidence:** High influence, low impact -- send reports, invite to steering committees
- **Keep Informed:** Low influence, high impact -- email updates, town halls
- **Collaborate:** High influence, high impact -- actively co-create

#### RACI

RACI (Responsible, Accountable, Consulted, Informed) classifies project participants:
- **Responsible:** Hands-on workers completing tasks
- **Accountable:** Exactly one person answerable for each item's delivery (the most common mistake is assigning multiple accountable parties)
- **Consulted:** Subject matter experts whose advice changes the work
- **Informed:** One-way status updates with no decision-making authority

#### Life Cycle Stage

Companies progress through introduction, growth, maturity, and decline. Identifying your company's stage informs strategy focus:
- **Introduction:** Survival mode, revenue-focused, expand from key customers
- **Growth (20%+ revenue increase):** Focus on speed to market and strengthening core
- **Maturity (5-8% growth):** Look for alternate growth strategies, platform plays, cross-selling
- **Decline (0-5% or negative growth):** Cost-cutting spiral risk, requires careful holistic strategy

Notably, companies are not required to grow indefinitely; the world's oldest companies (some 1,500 years old) are mostly small businesses serving fundamental human needs.

#### Value Chain

Porter's Value Chain (from *Competitive Advantage*, 1985) analyzes how discrete activities contribute to competitive advantage. Two types of departments exist: **value creators** (who make products and deliver services sold to customers) and **support departments** (HR, Legal, Finance, Infrastructure). Companies that don't recognize this distinction allow support functions to bureaucratize and impede value creators.

The Value Chain is expressed visually with primary activities on top (inbound logistics, operations, outbound logistics, marketing and sales, service) and supporting activities below (firm infrastructure, HR management, technology development, procurement).

#### Growth-Share Matrix

The BCG Growth-Share Matrix plots business units on two axes: market growth rate and relative market share. Products fall into four categories:
- **Stars:** High growth, high share -- invest
- **Cash Cows:** Low growth, high share -- maximize profit
- **Question Marks:** High growth, low share -- invest selectively or divest
- **Dogs:** Low growth, low share -- divest or liquidate

#### Core/Innovation Wave

This pattern helps balance investment between maintaining core products and pursuing innovation. Hewitt describes three innovation horizons:
- **Horizon 1:** Core business optimization (70% of investment)
- **Horizon 2:** Adjacent market expansion (20% of investment)
- **Horizon 3:** Transformational new ventures (10% of investment)

The key insight is that as today's Horizon 3 innovations mature, they become tomorrow's Horizon 1 core business. Companies must continuously invest across all three horizons.

#### Investment Map

The Investment Map visually plots where money is being spent across technology domains, helping identify over-invested and under-invested areas. It provides a visual companion to the Application Portfolio Management work.

### Chapter 6: Department Context

#### Principles, Practices, Tools

This pattern helps define and communicate the technology direction at the department level through three layers:
- **Principles:** Enduring rules that guide decisions (e.g., "Data is an asset")
- **Practices:** Methods and processes teams follow (e.g., continuous integration)
- **Tools:** Specific technologies used to implement practices

The pattern includes creating a **Process Posture Map** that assigns one of five tags to each process: Start (not doing this but should), Develop (doing it somewhat), Optimize (doing it well and improving), Maintain (doing it well), and Sunset (should stop doing this).

**Current and Future Model:** Create both a current-state and future-state operating model showing the transition from existing processes to desired ones. Use a **Sankey diagram** to visualize how principles flow into practices and practices into tools.

**Business Process Mapping:** Create visual representations of business processes to identify inefficiencies and opportunities for automation.

**Law of the Product of Probabilities:** The probability of a series of independent events occurring is the product of their individual probabilities. This mathematical principle applies to project planning: if 10 things each need to happen with 90% probability, the chance of all succeeding is only 35%.

#### Application Portfolio Management

APM provides a framework for evaluating and managing the full portfolio of applications. Applications are categorized by business value and technical quality, plotted on a 2x2 grid:
- **Invest:** High value, high quality
- **Tolerate:** High value, low quality (needs modernization)
- **Migrate:** Low value, high quality (consider consolidation)
- **Eliminate:** Low value, low quality

**Capability Mapping** links technology investments to business capabilities, ensuring alignment between what the technology organization builds and what the business needs.

**Business and Technology Attributes:** Evaluate applications against attributes like cost, risk, business value, technical fit, and agility to make informed portfolio decisions.

---

## Part III: Communicating the Strategy

### Chapter 7: Approach Patterns

#### 30-Second Answer

The 30-Second Answer pattern demands that you be able to articulate the essence of your strategy in half a minute. This is not a simplification exercise but a distillation one: if you cannot state your strategy concisely, you do not truly understand it. The 30-Second Answer should state the problem, the proposed solution, and the expected benefit.

#### Rented Brain

The Rented Brain pattern involves seeking expertise from people outside your immediate team. This includes reading widely across disciplines (philosophy, economics, military strategy, psychology) and consulting with experts in other departments. The strategist benefits enormously from renting other people's brains through interviews, workshops, and collaborative sessions.

Hewitt introduces the concept of **facing a cold audience** -- an audience that is skeptical, impatient, and uninformed about your work. To warm them up, establish credibility quickly, show empathy for their concerns, and connect your strategy to objectives they already care about.

#### Ars Rhetorica

Drawing from Aristotle's *Rhetoric*, this pattern identifies three persuasive appeals:
- **Ethos:** Establishing credibility and character
- **Pathos:** Appealing to emotions and values
- **Logos:** Presenting logical arguments with data

A compelling strategy presentation uses all three. Hewitt warns against common logical fallacies including affirming the consequent ("If P then Q. Q is true. Therefore P"), blind authority fallacy (citing someone's title or big tech company as proof), and many others.

#### Fait Accompli

The Fait Accompli pattern involves creating a sense of inevitability around your strategy by demonstrating momentum. Show what has already been accomplished, what is in progress, and what naturally follows. This creates confidence that the strategy is achievable.

#### Dramatic Structure

Borrowed from narrative theory, this pattern structures your presentation like a story:
1. **Establish the Status Quo:** Show the current state
2. **Create an Inciting Incident:** Reveal the problem or opportunity
3. **Rising Action:** Build the case with data and analysis
4. **Climax:** Present the strategic recommendation
5. **Resolution:** Show the path forward

**Shock and Awe:** Open with dramatic data that grabs attention (e.g., "60 items of technical debt" or "P1 incidents up 300% over three years").

#### Deconstruction

This pattern involves breaking complex systems or problems into their component parts for analysis. Hewitt identifies **three causes of problems**: people, process, and technology. He also introduces **Scopes Without Center** -- the tendency to analyze systems without identifying the true center or core.

**The World as System: Synthetic Decomposition:** Rather than analyzing systems top-down, decompose them synthetically by understanding how parts combine to create wholes.

**Business as System:** View the business as a system with inputs, processes, outputs, and feedback loops. Understanding these relationships is crucial for strategic positioning.

**The Scalable Business Machine:** Hewitt describes the attributes of a scalable business: standardization, automation, instrumentation, and resilience. A technology strategy should aim to create a scalable business machine.

**Aspects of the Scalable Business Machine:** Key aspects include modularity, loose coupling, separation of concerns, and evolutionary architecture. The strategist should aim to create systems that can adapt as business conditions change.

### Chapter 8: Templates

#### One-Slider

The One-Slider is a single-slide summary of your entire strategy, containing the problem statement, proposed solution, key benefits, timeline, and investment required. It serves as both an executive summary and a leave-behind document after meetings.

#### Use Case Map

A visual representation of use cases showing how different user types interact with the proposed system. It helps stakeholders quickly understand the scope and impact of the proposed technology changes.

#### Directional Costing

This template provides cost estimates at three levels of precision:
- **Rough Order of Magnitude (ROM):** -25% to +75% accuracy
- **Refined Estimate:** -10% to +25% accuracy
- **Realistic Estimate:** -5% to +10% accuracy

The estimate template includes categories for people costs, software licensing, infrastructure, training, and contingency. Directional costing helps executives understand the financial commitment without requiring detailed budgeting too early.

#### Priority Map

A visual tool that plots strategic initiatives on a 2x2 grid based on urgency and importance, helping teams decide what to do first, what to schedule, what to delegate, and what to eliminate.

#### Technology Radar

Inspired by ThoughtWorks' Technology Radar, this template categorizes technologies into four rings:
- **Adopt:** Ready for production use
- **Trial:** Worth pursuing actively in projects
- **Assess:** Worth exploring
- **Hold:** Proceed with caution or avoid

#### Build/Buy/Partner

This template helps evaluate three options for acquiring technology capabilities:

- **Build:** Maximum control and customization but longest time to market and highest risk. Ask: Is this what you want to spend organizational resources on? Do you have the resources to complete it better than what's available? Will you realize meaningful cost savings?

- **Buy:** Quickest time to market but least control, potential customization limitations, expensive, and requires changing business processes to fit the software.

- **Partner:** Shared risk and resources but requires alignment of interests, careful contract negotiation, and governance.

Evaluate each option against criteria including strategic fit, cost, time to market, risk, and capability.

#### Due Diligence

A structured template for evaluating vendors, partners, or acquisition targets. It includes technical assessment (architecture, scalability, security), business assessment (financials, market position, customer base), and cultural assessment (team quality, development practices, values alignment).

#### Architecture Definition

The Architecture Definition is the architect's primary deliverable, structured around four perspectives: business, application, data, and infrastructure. It should be expressed with clarity and decisiveness using primarily testable statements and math. Hewitt provides a comprehensive template covering:

- Business context and requirements
- Application architecture (component diagrams, interaction patterns)
- Data architecture (models, flows, storage)
- Infrastructure architecture (deployment, networking, security)
- Nonfunctional requirements with measurable targets
- Architecture principles and constraints
- Technology stack selections with rationale

**Executable Architectures:** Hewitt advocates for making architecture definitions executable -- writing them as code (infrastructure as code, contract testing, architecture fitness functions) so they can be automatically validated rather than becoming shelfware.

### Chapter 9: Decks

#### Ghost Deck

The Ghost Deck is a draft presentation created early in the strategy process. It contains placeholder slides with headlines and bullet points but no data. Its purpose is to:
- Create a narrative structure before filling in details
- Identify gaps in analysis early
- Provide a framework for gathering supporting data
- Test the story with trusted colleagues before formal presentation

#### Ask Deck

The Ask Deck is specifically designed to request approval and resources. It follows this structure:
1. **Imperil the Hero:** Use Shock and Awe to show the dire situation
2. **Let the Data Drive:** Present methodical, objective data
3. **Save the Hero:** Offer the Path Forward (vision of salvation)
4. **The Ask:** Explicitly ask for a yes decision (the reason you don't get the sale is you never actually ask)
5. **Appendix:** Supporting details including PESTEL, Five Forces, and other analysis

#### Strategy Deck

The Strategy Deck is the complete, comprehensive presentation of the technology strategy. It incorporates elements from all the patterns and tells the full story from world context through industry analysis to specific recommendations. It should include an executive summary, current state analysis, future state vision, roadmap, investment requirements, and risk mitigation strategies.

#### Tactical Plan

The Tactical Plan converts strategy into executable work. It includes a **MergeSort Meeting** process:
1. Call a meeting with clearly stated scope
2. Have everyone independently create lists organized by project categories
3. Give people time to populate their lists independently (preventing groupthink)
4. Bring raw material together and merge/sort the lists
5. Prioritize collaboratively

The MergeSort approach, inspired by the computer science algorithm, ensures all voices are heard, prevents loud voices from dominating, and generates more ideas through independent brainstorming before collaborative synthesis.

#### Roadmap

The Roadmap is a visual timeline showing when strategic initiatives will be executed. It should show dependencies between initiatives, resource requirements, milestones, and decision points. The Roadmap is a living document that gets updated as conditions change.

#### Patterns Map

The Patterns Map is a visual summary showing which patterns were used in creating the strategy and how they relate to each other. It helps the audience understand the rigor behind the recommendations.

---

## Conclusion

Hewitt concludes by emphasizing that technology strategy is fundamentally about making choices -- deciding what to do and, equally important, what not to do. The patterns in this book provide a toolkit for making those choices thoughtfully, systematically, and persuasively. He encourages readers to practice these patterns, adapt them to their own contexts, and share them with colleagues to build a common language for technology strategy.

The ultimate goal is not to create perfect strategies but to create better strategies through structured thinking, rigorous analysis, and compelling communication. As Hewitt writes, "We are making uncreditable assumptions all the time about all the things, such that we make equally uncreditable claims, such that we make bad decisions about architecture and strategy and suffer bad outcomes." The patterns in this book are designed to combat that tendency.

---

## Key Takeaways

1. **Strategy is about making choices.** It determines what to do and what not to do, balancing goals, methods, and resources. The best strategies minimize opportunity cost and maximize competitive advantage.

2. **The architect and strategist roles are converging.** Technologists must learn the language and frameworks of business strategy to be effective. You are already a businessperson; you need the tools to act like one.

3. **Lists are the foundation of strategy.** Every strategy document is essentially a list of lists. Making those lists MECE (Mutually Exclusive, Collectively Exhaustive) is the single most important thing you can do to improve your strategy work.

4. **Start with the broadest context.** Analyze world trends (PESTEL), then industry forces (Five Forces, SWOT), then corporate context (Value Chain, Stakeholders), then department needs. Each level narrows the focus.

5. **Hypothesis-driven analysis accelerates results.** Form a hypothesis quickly, gather data to test it, and revise if needed. Do not wait for perfect information before acting.

6. **Communication is as important as analysis.** A brilliant strategy that no one understands, cares about, or approves is worthless. Use narrative structure, Aristotle's rhetorical appeals, and visual templates to make your case compelling.

7. **Alignment is essential.** Your strategy must matter to the people who matter. Without executive support, team buy-in, and peer engagement, even the best strategy will fail.

8. **Every trade-off reduces to time and money.** The architect's job is to make trade-offs explicit, evaluate them against business strategy, and recommend the path that best supports competitive advantage.

9. **Use patterns selectively based on scope.** Not every project needs all 39 patterns. Match the patterns to the problem's scope -- from a simple MECE analysis for a local project to the full framework for a multiyear enterprise strategy.

10. **Executable architectures beat shelfware.** Make your architecture definitions testable and automatable. Write them as code, create fitness functions, and validate them continuously rather than publishing documents that gather dust.

11. **The triumvirate of strategy, culture, and execution must be aligned.** A strategy unsupported by culture or unexecutable by teams will fail regardless of its analytical rigor.

12. **Separate signal from noise using the 80/20 rule.** Focus on the few things that make the biggest difference. Perfect analysis is impossible; good enough analysis done quickly beats perfect analysis done too late.
