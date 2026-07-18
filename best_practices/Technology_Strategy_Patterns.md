# Technology Strategy Patterns
**Author:** Eben Hewitt
**Topic tags:** `#strategy` `#leadership` `#general`
**Language focus:** Language-agnostic technology strategy
**Sources:** `markdown_output/Technology Strategy Patterns/Technology Strategy Patterns.md` · `summaries/Technology_Strategy_Patterns.md`
## TL;DR
Treat technology strategy as the purposive allocation of limited resources toward business advantage, not as a shopping list of fashionable tools.
Build it from disciplined analysis, widen the frame from world to industry to company to department, convert findings into explicit choices, and communicate those choices in a form that can win approval and guide execution.
Use the 39 patterns individually for local decisions, in clusters for medium-scope problems, or comprehensively for an organizational Strategy Deck or Ask Deck.
Keep strategy, culture, and execution aligned; a funded deck without an executable plan is not a strategy outcome.
### Source-Coverage Boundary
- Use the book's Opportunity Cost, Hypothesis, Scenario Planning, Futures Funnel, Investment Map, and portfolio patterns to reason about strategic options.
- Do not attribute formal **real-options theory** to this book; it does not present that framework by name.
- Use the book's supplier-talent life cycle and its observation that a technology's “hype cycle settles” when discussing technology maturation.
- Do not attribute the named **Gartner Hype Cycle** model to this book; Gartner appears only as a suggested research source.
- Do not attribute **Wardley Mapping** to this book; it is not presented in the source.
- Treat these boundaries as a safeguard against importing adjacent strategy concepts into Hewitt's pattern catalog.
---
## Best Practices by Topic
### 1. Scale the Pattern Set to the Strategic Problem
**Principle:** Use only the patterns required by the size, expense, novelty, risk, and complexity of the decision.
**Do:**
- Start every technology strategy with a clearly bounded problem or opportunity.
- Ask what concerns the sponsor expects the strategy to address.
- Ask what scope of recommendation the sponsor expects.
- Establish context before selecting a solution.
- Analyze external trends, industry forces, organizational forces, departmental forces, and stakeholders as the scope requires.
- Understand the competitive, market, and technology landscape.
- Identify multiple strategic options in products, services, and the technology roadmap.
- Evaluate those options rather than defending a predetermined favorite.
- Make one coherent, cohesive, comprehensive recommendation.
- State the resources required to execute it.
- Use MECE, Logic Tree, Stakeholder Matrix, RACI, and selected Principles/Practices/Tools elements for a localized database upgrade.
- Add department, company, and industry patterns for a larger method or architecture change.
- Use the complete catalog for a broad organizational or multiyear strategy.
- Expect comprehensive work to take weeks of reading, writing, consultation, and refinement.
**Don't:**
- Don't instantiate every pattern merely because it exists.
- Don't use a multiyear-enterprise process for a narrow technical choice.
- Don't begin with a preferred product and reverse-engineer the analysis.
- Don't confuse a framework with an answer.
- Don't submit a recommendation without an explicit resource ask and execution path.
**Five-step working sequence:**
1. Establish context.
2. Understand competition, market, and technology landscape.
3. Identify strategic options.
4. Evaluate the options.
5. Recommend a coherent strategy and gain resources to execute it.
*Ref: Technology Strategy Patterns.md — “Applying the Patterns”; “A Logical Architecture of the Creation Patterns”; “Patterns Map”*
---
### 2. Act as a Businessperson Who Uses Technology
**Principle:** Use technology as a means of constructing the business; do not treat the business as an external customer of an autonomous technology function.
**Do:**
- Learn the language executives use to discuss investment, cost, growth, risk, and timing.
- Translate technical concerns into business position, velocity, and potential.
- Empathize with the people whose approval and money the strategy requires.
- Frame every technology proposal as a request to spend someone else's money.
- Connect technical choices to competitive advantage.
- Integrate technology and business leadership rather than making technology a subservient order-taking function.
- Raise your visor from one project to the portfolio and from one team to interrelated systems.
- Use shared pattern names to create a common language among architects, product managers, executives, and strategists.
- Learn quickly across disciplines; the book expects effective strategists to become synthetic interdisciplinarians.
**Don't:**
- Don't put a warning on a wiki and assume the organization will act.
- Don't expect technically correct ideas to fund themselves.
- Don't present architecture as a private technical concern.
- Don't hide ignorance of business terminology; ask what unfamiliar terms mean.
- Don't mistake activity in technology for progress in the business.
**Author's strategic frame:**
> “But we're in the business of building a business.”
*Ref: Technology Strategy Patterns.md — “This Is Water”; “Discovering Strategy”; “The Architect's Role”*
---
### 3. Learn from Michelin, Oracle, and Canon
**Principle:** Test whether technology and business strategy reinforce each other, consume each other's capacity, or redefine the market together.
**Do:**
- Use Michelin to test whether a once-powerful strategic mechanism remains connected to its original economic purpose.
- Remember that Michelin created its guide in 1900 to encourage driving and therefore tire consumption.
- Notice that the guide became a global authority and brand asset.
- Notice also that the paper guide later lost about €19 million per year after becoming disconnected from its original demand-creation role.
- Use Oracle to test whether integration discipline is crowding out adaptation.
- Remember Oracle's principle: make software number one or two in each category, or buy the market leader.
- Remember that Oracle acquired nearly 60 companies between 2008 and 2013 and spent $45 billion on acquisitions between 2004 and 2014.
- Recognize the strategic alignment in mandating Oracle middleware across acquired products.
- Recognize the opportunity cost: years of internal refactoring were not spent on cloud and machine-learning innovation.
- Use Xerox and Canon to test whether a challenger can redefine cost, reliability, service, manufacturing, and customer segment together.
- Remember Xerox's 95% market share and $80,000–$129,000 machines.
- Remember Canon's use of microelectronics and optics, eight basic parts, a disposable primary assembly, robotic assembly, and $700–$1,200 pricing.
- Look for strategies that alter the market rather than merely improving the incumbent product.
**Don't:**
- Don't preserve a strategic artifact after its economic mechanism has disappeared.
- Don't make integration uniformity an unquestioned permanent constraint.
- Don't optimize an incumbent operating model while a competitor changes who can buy the product.
- Don't separate product architecture from manufacturing, service, distribution, and pricing strategy.
**Case-study test:**
- Michelin: Has the mechanism drifted from its purpose?
- Oracle: Is standardization consuming the capacity needed for the next wave?
- Xerox: Are current scale and market share concealing a substitute?
- Canon: Can a different architecture create a different customer and cost structure?
*Ref: Technology Strategy Patterns.md — “Marketing at Michelin”; “Acquisition and Integration at Oracle”; “Differentiation at Xerox and Canon”*
---
### 4. Fulfill the Architect's Three Concerns
**Principle:** Contain entropy, specify nonfunctional requirements, and determine trade-offs through concrete deliverables.
**Do:**
- Define standards, conventions, and toolsets that improve speed, understandability, and maintainability.
- Treat tool, framework, language, and platform choices as decisions with consequences for flexibility, acquisitions, training, hiring, and business strategy.
- State a unifying vision.
- Show the path in a roadmap.
- Communicate guidelines and standards.
- Create clarity about doing the right things and doing things right.
- Specify scalability, availability, maintainability, manageability, monitorability, extensibility, interoperability, portability, security, and performance.
- Structure the Architecture Definition across business, application, data, and infrastructure perspectives.
- Express requirements as valid, testable propositions and quantitative targets.
- Put nonfunctional requirements into acceptance criteria where practical.
- Make every material trade-off visible.
- State the new problem introduced by the proposed solution.
- Reduce the final trade-off to time and money.
**Don't:**
- Don't operate through remembered hallway conversations.
- Don't declare standards without explaining the business consequences.
- Don't let nonfunctional requirements remain implied.
- Don't pretend an architectural choice only solves problems.
- Don't answer every trade-off with a fashionable tool.
**Vitruvian quality test:**
- **Firmitas:** Make it solid enough to endure and flexible enough to adapt.
- **Utilitas:** Make it fit for its actual purpose.
- **Venustas:** Make the proportions harmonious and the result delightful.
**Trade-off examples:**
- More security can reduce performance.
- Database sharding can increase performance and distribution while increasing operational complexity.
- More monitoring can create storage, rotation, security, and cleansing burdens.
- Apparent simplicity can defer flexibility costs into a more expensive future.
> “You're never quite solving a problem. You're only trading it for one that you'd rather have.”
*Ref: Technology Strategy Patterns.md — “Vitruvius and the Principles of Architecture”; “Three Concerns of the Architect”*
---
### 5. Balance Goals, Methods, and Means
**Principle:** Define strategy as a course of action that balances goals, methods, and available resources to create advantage.
**Do:**
- Determine the problems and opportunities in front of the organization.
- Define them precisely before choosing a course.
- Balance problem solving with the imagination required to create opportunities.
- Separate strategy, logistics, and tactics.
- Use strategy to decide where to act.
- Use logistics to bring resources to that point.
- Use tactics to decide the manner of execution.
- Create strategies at corporate, business-unit, department, and portfolio levels.
- Set revision cadence according to the volatility of each level.
- Revisit three- and five-year direction as the environment changes.
- Preserve enough continuity that revision does not degrade into reaction.
**Don't:**
- Don't “set and forget” a long-range strategy.
- Don't revise so constantly that only disconnected tactics remain.
- Don't define strategy as aspiration without resource allocation.
- Don't define strategy as a collection of projects.
- Don't confuse a goal with a method or a method with a resource.
**Strategist's scope:**
- Organizational goals.
- Operating model and processes.
- Culture and communication modes.
- Talent sourcing, retention, and training.
- Facilities, local laws, and cost.
- Business-development opportunities.
- Partnerships and joint ventures.
- Merger and acquisition opportunities.
- Strategic capabilities.
- Fact-based long-term direction.
*Ref: Technology Strategy Patterns.md — “The Strategist's Role”; “The History of Strategy”*
---
### 6. Align Strategy, Culture, and Execution
**Principle:** Treat strategy, culture, and execution as a triumvirate; weakness in any one can defeat the other two.
**Do:**
- Map the technology strategy to current business emphasis.
- If the business is cutting cost, inspect labor location, automation, release processes, open-source substitutions, and other people/process/technology levers.
- If the strategy is an integrative platform, address territorial and competitive team behavior.
- Define metrics that show whether execution is producing the intended outcome.
- Learn the corporate strategy-and-budget calendar.
- Enter strategy season early enough to influence budget season.
- Build regular conversations for narrower or faster-moving concerns.
- Create an honest, detailed executive version of the strategy.
- Create a shorter public version focused on the changes teams must drive.
- Protect confidential financial, transaction, and personnel information.
- Confirm that teams possess the capabilities required to execute.
**Don't:**
- Don't publish lofty goals without execution mechanics.
- Don't assume stated principles describe the lived culture.
- Don't ask for major funding after the allocation calendar has closed.
- Don't disclose sensitive context merely to make the public version complete.
- Don't ignore culture because the technical plan is sound.
**Business-outcome inventory from the book:**
- Grow shareholder value.
- Grow earnings per share.
- Increase revenue.
- Manage costs.
- Diversify revenue.
- Cross-sell.
- Increase market share.
- Increase share of wallet.
- Increase yield.
- Improve retention.
- Reduce defects.
- Improve safety.
- Improve time to market.
- Grow through acquisition.
*Ref: Technology Strategy Patterns.md — “The Triumvirate: Strategy, Culture, and Execution”*
---
### 7. Make Every Strategic List MECE
**Principle:** Make lists mutually exclusive and collectively exhaustive because the strategy is ultimately a list of lists.
**Do:**
- Name the audience before constructing the list.
- State why that audience cares.
- Ensure the list enables a decision or an action.
- Keep private analysis detailed.
- Keep executive-facing lists lean.
- Check that no item overlaps another.
- Check that the items together cover the defined category.
- Keep every item at the same level of abstraction.
- Remove subcategories placed beside their parents.
- Define the category tightly enough that “collectively exhaustive” is useful rather than infinite.
- Prefer three or five categories when that abstraction remains accurate.
- Use the Rule of Three to improve comprehension and recall.
- Refine MECE lists with the team until the habit becomes automatic.
**Don't:**
- Don't use a list merely to “help people understand.”
- Don't mix revenue, cost, profit, and an unrelated financial measure in one equation-level list.
- Don't list “internal stakeholders,” “external stakeholders,” and “development teams” as peers.
- Don't include Southwest beside North, South, East, and West.
- Don't preserve technically MECE detail that overwhelms the executive audience.
- Don't interpret “exhaustive” as “include thousands of options.”
**Canonical formulas:**
- `Opportunity Cost = Return of Most Lucrative Option – Return of Chosen Option`
- `Profit = Revenue – Cost`
**Database-selection application:**
1. Define three or five selection criteria.
2. Survey open-source and commercial alternatives.
3. Record the full considered set.
4. Narrow to a presentable set.
5. State why rejected options were rejected.
6. Compare functional and nonfunctional requirements.
7. Compare training, staffing, popularity, and ease of use.
8. Present acceptable finalists as Good, Better, and Best.
9. Show the reasoning so the decision maker can defend the choice.
*Ref: Technology Strategy Patterns.md — “MECE”; “The Rule of Three”; “Applying MECE Lists”*
---
### 8. Minimize Opportunity Cost Through Explicit Options
**Principle:** Compare viable alternatives and choose the one whose return exceeds the best forgone return.
**Do:**
- Survey the landscape before recommending.
- Treat cloud versus data center, build versus buy, train versus acqui-hire, vendor selection, and speed versus quality as option decisions.
- Record the option set before narrowing it.
- State what each selected path prevents the organization from pursuing.
- Evaluate reversibility, cost, and one-shot risk.
- Gather enough evidence to make a reasoned call under imperfect knowledge.
- Prefer the decision with the highest probability of organizational advantage.
- Keep unselected plausible outcomes available for later investigation.
- Revisit the option set when material evidence changes.
**Don't:**
- Don't imply that the book provides a financial real-option valuation method.
- Don't equate a list of ideas with an evaluated option set.
- Don't conceal the best rejected alternative.
- Don't omit the opportunity cost of internal capacity.
- Don't optimize return while ignoring organizational damage or positional disadvantage.
**Option-review questions:**
- What return does the selected option create?
- What is the most lucrative rejected option?
- What capability does the choice consume?
- What capability does it create?
- How difficult is reversal?
- What evidence would cause a revisit?
*Ref: Technology Strategy Patterns.md — “Analysis”; “MECE”; “Possible Outcomes”*
---
### 9. Separate Diagnostic and Solution Logic Trees
**Principle:** Diagnose why the issue exists before mapping how to solve it.
**Do:**
- Put the agreed problem statement at the root of a Diagnostic Logic Tree.
- Ask why the condition exists.
- Group possible causes into MECE branches.
- Repeat the analysis to roughly five levels where useful.
- Identify actionable root causes.
- Preserve the diagram in digital form for the Strategy Deck.
- Create a separate Solution Logic Tree.
- Start the solution tree with the ideal end state.
- Ask how that state can be realized.
- Regress through prior necessary conditions toward the current state.
- Use the resulting path to formulate a plan.
- Distinguish customer pain from an unrecognized opportunity for gain.
**Don't:**
- Don't jump from a symptom to a solution.
- Don't mix diagnostic causes and proposed work in the same tree.
- Don't accept the first “why” as the root.
- Don't spend hard work on a poorly defined or unimportant problem.
- Don't focus only on restoring the status quo.
**Jefferson Monument case:**
- Monument erosion required harsh cleaning.
- Cleaning responded to pigeon residue.
- Pigeons followed spiders.
- Spiders followed midges.
- Midges followed dusk lighting.
- Turning the lights on one hour later addressed the root at negligible cost.
**Opportunity reminder:**
- The 2007 customer did not report “lack of smartphone apps” as a pain.
- Apple created a gain that customers had not articulated.
- The colorful 1998 iMac similarly created distinction beyond an expressed functional deficiency.
*Ref: Technology Strategy Patterns.md — “Logic Tree”; “Diagnostic Logic Tree”; “Solution Logic Tree”; “Problems Versus Opportunities”*
---
### 10. Form Hypotheses with Five Questions
**Principle:** Make an early, testable claim that focuses investigation without pretending certainty.
**Do:**
- Treat a hypothesis as a starting point for investigation.
- Base it on limited but concrete data.
- Put a stake in the ground quickly.
- Maintain several competing hypotheses.
- Ask what conjunct of propositions describes the problem.
- Ask what semantics characterize those propositions.
- Enumerate possible outcomes.
- Assign approximate probabilities.
- Score options by ease and impact.
- Update the hypothesis as evidence arrives.
- Reject it quickly when the evidence does not support it.
- Keep the evidence trail transparent.
**Don't:**
- Don't wait for certainty before hypothesizing.
- Don't treat a hypothesis as a fact.
- Don't hide the initial bias that framed the investigation.
- Don't force later evidence to preserve the original claim.
- Don't present a tautology as an insight.
**Five questions:**
1. What is the conjunct of propositions that describes the problem?
2. What semantics characterize those propositions?
3. What are the possible outcomes?
4. What are the probabilities of those outcomes?
5. What ease-and-impact scores suggest the right strategy?
**Evidence hierarchy:**
- Gather data points.
- Add intellectual and creative interpretation to form insights.
- Combine supported insights into subhypotheses.
- Combine subhypotheses into the working hypothesis.
*Ref: Technology Strategy Patterns.md — “Hypothesis”; “The Five Questions”; “Insights”*
---
### 11. Define the Domain of Discourse
**Principle:** Define terms, quantifiers, sets, objects, and boundaries before treating a proposition as meaningful.
**Do:**
- State each problem as propositions capable of truth evaluation.
- Connect the propositions explicitly.
- Define ambiguous nouns such as customer, resource, system, and platform.
- Record a data dictionary or glossary.
- Ask what “everyone,” “always,” “all,” and “never” actually quantify.
- Identify the domain in which the claim is intended to hold.
- Identify the members of each relevant set.
- Examine overlap between adjacent domains.
- Use boundary analysis to inform system decomposition.
- Align business and technical meanings before committing to delivery.
**Don't:**
- Don't assume shared words imply shared meanings.
- Don't call a system a platform merely because it is important.
- Don't promise an AI platform when the technical team means background machine-learning algorithms.
- Don't decompose systems before examining business-domain boundaries.
- Don't universalize an observation about a small user group.
**Platform test from the book:**
- Provide APIs.
- Allow customers to build something new on top.
- Allow that creation without requiring a conversation with the provider.
- Recognize Android, Alibaba, AWS, and Salesforce as examples.
- Reject “platform” as a synonym for system or application.
> “When people say ‘everything,’ they never mean everything.”
*Ref: Technology Strategy Patterns.md — “The Conjunct of Propositions”; “The Semantics Characterizing These Propositions”; “Objects and Relations”*
---
### 12. Distinguish Induction, Deduction, and Bayesian Revision
**Principle:** Match the reasoning mode to the claim and preserve uncertainty.
**Do:**
- Use induction to generalize cautiously from observed data.
- Label inductive conclusions as probable rather than certain.
- Use deduction to test whether a conclusion follows from assumed premises.
- Test premises independently.
- Assign High, Medium, or Low probability when numeric precision is unjustified.
- Estimate a prior probability before considering a new event.
- Estimate the event's likelihood if the hypothesis is true.
- Estimate the event's likelihood if the hypothesis is false.
- Revise to a posterior probability.
- Hold multiple hypotheses at once.
- Update them frequently as evidence changes.
- Use probability ranges instead of fake point estimates.
**Don't:**
- Don't let an unfamiliar event become “improbable” merely because it is unfamiliar.
- Don't infer tomorrow from a long unbroken run without considering changing conditions.
- Don't assume a coin is “due” to reverse its last result.
- Don't filter data through an undefined term such as “active customer.”
- Don't use precise numbers to make estimates look factual.
**Russell's turkey warning:**
- Repeated feeding supports an inductive expectation.
- Thanksgiving changes the governing condition.
- A long history does not make the next event certain.
**Practical Bayesian sequence:**
1. Recognize the open-ended question.
2. Form the first hypothesis.
3. Estimate its probability without false precision.
4. State the prior.
5. Estimate the new event under truth.
6. Estimate the new event under falsity.
7. Revise the probability.
*Ref: Technology Strategy Patterns.md — “Possible Outcomes”; “Probability of Each Outcome”; “Bayesian Probability”; “Deductive Reasoning”*
---
### 13. Separate Signal from Noise and Prioritize
**Principle:** Reach a good-enough, high-impact conclusion quickly, then refine it.
**Do:**
- Define signal as evidence pointing toward the true and material state of affairs.
- Define noise as random or competing patterns that can be mistaken for signal.
- Use the Pareto rule as a filter, not as a law.
- Find the few data points that materially change the recommendation.
- Generate several hypotheses quickly.
- Investigate the most promising first.
- Plot work by ease and impact.
- Put easy, high-impact work first.
- Put hard, low-impact work last.
- Use the middle quadrants as judgment inputs rather than automatic ranks.
- Let the impact of being wrong determine how much analysis precedes action.
- Ask trusted, independent thinkers to attack the hypothesis.
**Don't:**
- Don't spend months evaluating every tool in a mature category.
- Don't wait for “all the data”; no such complete set exists.
- Don't let thoroughness consume the opportunity.
- Don't treat the 2×2 as a decision maker.
- Don't preserve a hypothesis after disconfirming evidence appears.
**Ease/impact quadrants:**
- Easy + high impact: green; prioritize first.
- Easy + low impact: yellow; usually second.
- Hard + high impact: important but not a quick win; usually third.
- Hard + low impact: red; usually last.
**Poker analogy:**
- Learn the hands.
- Learn rough odds.
- Fold the worst hands.
- Consider opponents modestly.
- Reach many expert-equivalent decisions without mastering every detail.
*Ref: Technology Strategy Patterns.md — “Ease and Impact Scoring”; “Signal and Noise”; “Context”*
---
### 14. Analyze Objects and Relations Without Overclaiming Causation
**Principle:** Identify objects, predicates, and relation strength before drawing a strategic conclusion.
**Do:**
- Define each object as a useful focus of inquiry.
- Decompose objects until further division no longer helps the analysis.
- Identify necessary relations.
- Identify necessary-but-not-sufficient conditions.
- Identify contingent relations.
- Distinguish identity from equality.
- Identify directional and bidirectional associations.
- List predicates explicitly.
- Record correlations that may support prediction.
- Treat business causation as rare and demanding.
- Describe multiple contributing causes when the situation is overdetermined.
- Make only the claim required for useful action.
**Don't:**
- Don't mistake `A = A` for an insight.
- Don't treat a metaphorical equality as literal identity.
- Don't infer causation from frequent co-occurrence.
- Don't use “this causes that” where many vectors operate at different intensities.
- Don't spend unlimited time proving a causal chain when a qualified action claim is sufficient.
**Relation spectrum:**
- Identity.
- Equality.
- Association.
- Predicate.
- Correlation.
- Causation.
**Organizational identity test:**
- Why does the company exist?
- Who are its customers?
- Who are its partners?
- Who are its competitors?
- How does it make money?
*Ref: Technology Strategy Patterns.md — “Objects and Relations”; “Identity”; “Equality”; “Association”; “Predicate”; “Correlations”; “Causation”*
---
### 15. Use Strategic Analysis as a Model-Finding Process
**Principle:** Treat strategy analysis as finding a model that best explains evidence and supports a probabilistic prediction.
**Do:**
- Define the label or strategic question.
- Identify internal and external data sources.
- Prepare and clean the data.
- Account for missing values.
- Select an appropriate mental model or combination of models.
- Fit the model to observed evidence.
- Predict likely outcomes.
- Translate model outputs into recommendations across people, process, and technology.
- Keep the analogy conceptual; strategy remains a human judgment process.
**Don't:**
- Don't confuse the model with reality.
- Don't skip data cleaning.
- Don't rely on one model when an ensemble of perspectives is stronger.
- Don't present a prediction without its assumptions.
**Code from the book:**
```
Output = f(Input)
```
**Equation from the book:**
$$Y = f(x)$$
**Five-step analogy:**
1. Determine the hypothesis and desired label.
2. Determine and prepare data sources.
3. Determine the model.
4. Fit the model.
5. Predict.
*Ref: Technology Strategy Patterns.md — “Strategic Analysis as Machine Learning”*
---
### 16. Build a PESTEL Before Narrowing to Local Technology
**Principle:** Analyze political, economic, social, technological, environmental, and legal conditions through the lens of the specific industry.
**Do:**
- Treat PESTEL as broad context that precedes resource allocation.
- Keep its six categories MECE.
- Translate every broad trend into a possible industry or customer effect.
- Research government policy, taxation, trade, sanctions, and geopolitical effects.
- Research disposable income, financing, foreign exchange, unemployment, and GDP.
- Research generational, family, education, health, and behavior trends.
- Research technology adoption by country, generation, and customer segment.
- Research climate, sustainability, ecology, weather, and supplier effects.
- Research enacted, pending, and debated laws.
- Include GDPR, antitrust, sanctions, and industry-specific regulation where relevant.
- Cite every external source.
- Use two- to five-year projections for long-range analysis.
- Build a raw-material scrapbook first.
- Distill it into a concise analysis.
- Put the PESTEL slides in the Strategy Deck appendix.
- Validate the draft with strategy, product, sales, and executive colleagues.
- Update it annually or after a major disruptive event.
**Don't:**
- Don't analyze “the economy” as an abstract object disconnected from the industry.
- Don't stay inside the technologist's daily field of view.
- Don't mix facts, assumptions, and recommendations in the research stage.
- Don't put the long PESTEL before the executive conclusion.
- Don't skip business-strategy alignment because the analysis is independently researched.
**Three-part output:**
1. Gather data while separating bias and assumption.
2. State insights.
3. Make local recommendations.
*Ref: Technology Strategy Patterns.md — “PESTEL”; “Creating the PESTEL”; “Researching for PESTEL”; “Applying the PESTEL”*
---
### 17. Use Scenario Planning to Break the Do-Nothing Default
**Principle:** Ask “What if?” collaboratively so the leadership team can perceive weak signals and prepare for materially different futures.
**Do:**
- Recognize status quo as the default strategy.
- Use PESTEL as the research backdrop.
- Interview key leaders before the workshop.
- Bring a diverse group together.
- Present findings and hypotheses to establish a shared starting point.
- Break into small groups.
- Generate many scenarios.
- Distill them through private voting.
- Have teams build the case for the most important scenarios.
- Map first- and second-order impacts.
- Assign relative uncertainty rather than false numeric precision.
- Include weak but plausible signals.
- Use Logic Trees to explore alternate paths.
- Capture results in slides for later use.
- Feed the results into Futures Funnel and Backcasting.
**Don't:**
- Don't delegate scenario construction entirely to junior staff.
- Don't let the most dramatic scenario crowd out less vivid but plausible alternatives.
- Don't pick the preferred future while claiming to forecast.
- Don't get trapped estimating unknowable probabilities.
- Don't run the exercise alone.
**Full-scale process:**
1. Conduct research and leadership interviews for several weeks.
2. Hold a two- or three-day workshop.
3. Generate and explore scenarios in small groups.
4. Distill through private voting.
5. Build arguments around the finalists.
6. Give leadership the result as decision input.
**Lean version:**
- Run a half-day workshop.
- Invite experts from business and technology.
- Ask directors to present short future-view decks.
- Look for weak but plausible signals.
- Forecast impacts with qualified induction.
*Ref: Technology Strategy Patterns.md — “Scenario Planning”; “Steps for Scenario Planning”*
---
### 18. Distill Scenarios into a Futures Funnel
**Principle:** Put possible, plausible, probable, and preferred futures on one slide to focus executive discussion.
**Do:**
- Treat each region as a set.
- Put all possible futures in the widest set.
- Put reasonable futures in the plausible subset.
- Identify probable futures, including unwanted ones.
- Identify the preferred intersection explicitly.
- Focus on futures that are both plausible or probable and relevant to preference.
- Populate the funnel from internal, conceptual, and external factors.
- Include resources, architecture, and product portfolio as internal factors.
- Include correlations and causal chains as conceptual factors.
- Include customer behavior, competitor behavior, and potential futures as external factors.
- Use SWOT and Five Forces to supply material.
- Use the funnel as a lightweight substitute when full Scenario Planning is unjustified.
**Don't:**
- Don't devote planning capacity to preferred but implausible fantasies.
- Don't confuse “possible” with “worth preparing for.”
- Don't place only desirable outcomes on the funnel.
- Don't allow more than one slide.
**Set definitions:**
- **Possible:** Could happen.
- **Plausible:** Reasonable to expect.
- **Probable:** Likely to happen.
- **Preferred:** Desired by the organization.
*Ref: Technology Strategy Patterns.md — “Futures Funnel”*
---
### 19. Backcast from a Concrete Beautiful Future
**Principle:** Define a measurable future state, then work backward through necessary antecedents to the current state.
**Do:**
- Bring architecture, strategy, and product participants together.
- State the desired future without initially constraining it by today's circumstances.
- Make the vision observable and decidable.
- Use a metric or concrete image such as cutting the power cord on the legacy system.
- Hypothesize the immediately prior necessary state.
- Repeat until the chain reaches the status quo.
- Inspect people, process, and technology at every step.
- Distinguish dependent variables from levers the strategist can control.
- Test whether the consequent logically follows.
- Tag each antecedent hypothesis with probability.
- Turn the resulting conclusions into prioritized project work.
**Don't:**
- Don't mistake a necessary condition for a sufficient one.
- Don't assign causation casually.
- Don't make the future state abstract or inspirational only.
- Don't trace technology steps while omitting people and process changes.
- Don't assume a valid proposition is therefore true.
**Logic from the book:**
$$P \Rightarrow Q$$
**Variable distinction:**
- **Dependent variables:** Outcomes or unknown moving parts.
- **Independent variables:** Levers controlled by the strategist.
*Ref: Technology Strategy Patterns.md — “Backcasting”*
---
### 20. Use SWOT as a Fast Internal/External Lens
**Principle:** Separate internal/external and helpful/harmful forces on one slide.
**Do:**
- Interview people across levels, departments, and roles.
- Ask about competitive advantage in people, process, and technology.
- Ask about internal weaknesses.
- Ask about underserved markets, stubborn competitors, and adjacent opportunities.
- Record responses under Strengths, Weaknesses, Opportunities, and Threats.
- Tag the source material as internal or external.
- Remove duplicates, anecdotes, and biased items.
- Distill the most important points into one slide.
- Start corrective action with internal factors where control is highest.
- Use SWOT when joining an organization.
- Use it for legacy evolution.
- Use it for departmental strategy.
- Use it for partner updates, customer meetings, and major pursuits.
- Use it in long-range technology strategy.
**Don't:**
- Don't treat an external threat as an internal weakness.
- Don't make the four lists without interviews.
- Don't preserve every raw observation.
- Don't let competitor watching substitute for getting the internal house in order.
**Quadrants:**
- Strengths: internal and helpful.
- Weaknesses: internal and harmful.
- Opportunities: external and potentially helpful.
- Threats: external and harmful.
*Ref: Technology Strategy Patterns.md — “SWOT”*
---
### 21. Analyze Threat of Entry and Ease of Substitution
**Principle:** Distinguish direct new competitors from alternatives that satisfy the same economic need through different technology.
**Do:**
- Assess switching cost.
- Assess access to distribution.
- Assess government policy and regulation.
- Assess capital requirements.
- Assess economies of scale.
- Assess product differentiation.
- Assess customer loyalty and brand equity.
- Assess industry profitability.
- Identify patents and rights without assuming they are permanent barriers.
- Look outside the incumbent product category for substitutes.
- Assess perceived differentiation.
- Count available substitutes.
- Assess availability of close substitutes.
- Assess customers' propensity to switch.
- Compare relative price.
- Identify channel strategies that reduce substitution risk, such as broad APIs.
**Don't:**
- Don't define competitors only as companies using the same technology.
- Don't rely on regulatory barriers that a new operating model can bypass.
- Don't assume a familiar product label means the underlying solution category is unchanged.
- Don't omit buyer switching costs.
**Cases:**
- Google entered search against Yahoo.
- Amazon entered grocery retail through Whole Foods.
- Gig-economy services disrupted taxi-medallion barriers.
- Cell phones substituted for landlines.
- Canon's low-cost copier substituted for the high-cost corporate copier model.
- Netflix and Amazon used APIs to reduce exposure to new device and channel substitutes.
*Ref: Technology Strategy Patterns.md — “Threat of New Entrants”; “Ease of Substitution”*
---
### 22. Analyze Customer, Supplier, and Rivalry Power
**Principle:** Evaluate who can change terms, who supplies scarce inputs, and how the market distinguishes competitors.
**Do:**
- Assess customer dependence on current distribution channels.
- Assess alternative channels.
- Assess bargaining leverage.
- Assess buyer information and education.
- Assess price sensitivity.
- Treat compute/storage and developers as the two primary software inputs.
- Assess employee solidarity and labor constraints.
- Assess differentiation among talent sources.
- Assess substitutes for scarce skills.
- Assess supplier concentration.
- Assess suppliers' alternative customers.
- Assess innovation as a source of sustainable advantage.
- Assess pricing, marketing, online/offline competition, advertising, concentration, and transparency.
- Create one slide per force.
- State how the proposed technology supports or defends against each force.
- Tag threats red, yellow, or green.
- End with concise positioning recommendations.
**Don't:**
- Don't treat people as an unlimited commodity.
- Don't equate current salary with long-term talent availability.
- Don't analyze industry rivalry through product features alone.
- Don't stop at describing the force; connect it to a technology action.
**Five Forces implementation:**
1. Document current position for each force.
2. Connect the proposed technology response.
3. Rate threat level.
4. Recommend action.
*Ref: Technology Strategy Patterns.md — “Bargaining Power of Customers”; “Bargaining Power of Suppliers”; “Industry Rivalry”; “Applying the Five Forces”*
---
### 23. Match Technology and Talent to Their Life Cycle
**Principle:** Expect skill scarcity, differentiation, hype, commoditization, and automation to change as a technology matures.
**Do:**
- Treat emerging-technology talent as scarce and highly differentiated.
- Distinguish “has done it” from “has heard of it.”
- Expect salaries and competition to rise while experienced supply remains small.
- Expect training companies and accessibility tools to expand the supplier pool.
- Wait for failed startups and practical experience to reveal true utility.
- Expect mature technology talent to become easier to substitute.
- Expect some mature tasks to be automated away.
- Factor the talent stage into build, buy, partner, and roadmap decisions.
- Use PESTEL research to track adoption across populations and customer segments.
- Use the Technology Radar to communicate what to adopt, trial, assess, or hold.
**Don't:**
- Don't describe the source's generic “hype cycle settles” phrase as the named Gartner Hype Cycle framework.
- Don't attribute Wardley Mapping stages to the book.
- Don't budget emerging skills at commodity rates.
- Don't pay pioneering premiums after the capability has become undifferentiated.
- Don't preserve human roles after the work has become automatable.
**Book-grounded life cycle:**
1. Few pioneers; extreme differentiation.
2. Interest expands; experience remains scarce.
3. Training and tooling increase accessibility.
4. Hype settles; useful applications become clearer.
5. Widespread use reduces differentiation.
6. Automation removes some dedicated work.
*Ref: Technology Strategy Patterns.md — “Bargaining Power of Suppliers”; “Technological”; “Technology Radar”*
---
### 24. Use the Ansoff Growth Matrix to Choose Growth Direction
**Principle:** Classify growth by whether products and markets are current or new.
**Do:**
- Use market penetration for more share with current products in current markets.
- Consider acquisition, loyalty, sales capacity, and stickiness for penetration.
- Use market development to bring current products into new markets.
- Account for localization, internationalization, naming, labels, and market-specific features.
- Use product development to add new products in current markets.
- Test whether a real platform or ecosystem can extend the current customer relationship.
- Use diversification for new products in new markets.
- Recognize diversification's higher risk and portfolio-resilience benefit.
- Use the matrix to converse with product and marketing peers.
**Don't:**
- Don't call every adjacent feature diversification.
- Don't enter a new market without adapting the current product where required.
- Don't call an important application a platform unless customers can build on it.
- Don't pursue diversification without acknowledging cost and risk.
**Examples:**
- Canon reached individuals and small businesses with current copier capability adapted to a new market.
- AWS repeatedly adds capabilities for the same customer base.
- Diversification can reduce exposure to one market's changing tide.
*Ref: Technology Strategy Patterns.md — “Ansoff Growth Matrix”*
---
### 25. Align Stakeholders Before Building the Strategy
**Principle:** Do work that matters to someone who matters and secure support above, below, and beside the strategy team.
**Do:**
- Identify the CEO and business-unit president.
- Understand the organization chart and real power structure.
- Secure the strongest technical leader's support.
- Secure the highest relevant executive's support.
- Identify leaders who fund and champion.
- Identify teams who execute.
- Identify peers who can ignore or undermine.
- Include product, sales, account management, legal, project management, operations, and HR as relevant.
- Consider customers, franchisees, vendors, and suppliers.
- Track 10–30 key stakeholders in a spreadsheet.
- Record name, title, organization, and contact information.
- Score influence and impact from 1 to 5.
- Update the map as roles and personnel change.
**Don't:**
- Don't consult everyone.
- Don't let broad consultation reduce choices to platitudes.
- Don't assume formal title equals practical influence.
- Don't associate yourself with projects no important leader can explain.
- Don't proceed when the sponsor is openly hostile to strategy without recognizing the low probability of success.
**Stakeholder quadrants:**
- **Monitor:** Low influence, low impact; check periodically.
- **Maintain confidence:** High influence, low impact; review milestones, metrics, funding, and direction.
- **Keep informed:** Low influence, high impact; prepare communication, training, and departmental updates.
- **Collaborate:** High influence, high impact; co-create continuously.
**Meaningful-choice test:**
> If no reasonable person could argue against the statement, it is probably not a consequential strategic choice.
*Ref: Technology Strategy Patterns.md — “Stakeholder Alignment”; “Determining Stakeholders”; “Determining Drivers”; “Stakeholder List”; “Stakeholder Matrix”*
---
### 26. Assign One Accountable Owner with RACI
**Principle:** Clarify who does the work, who answers for it, who changes it through advice, and who receives one-way updates.
**Do:**
- List broad work categories down the left side.
- List participants across the columns.
- Assign Responsible people to perform hands-on work.
- Assign exactly one Accountable person per work item.
- Assign Consulted subject-matter experts whose advice can change the work.
- Assign Informed stakeholders who receive status but do not decide.
- Split an item when two accountable owners appear genuinely necessary.
- Otherwise choose the owner with the most control or vested interest.
- Refine the RACI as the project becomes clearer.
- Use it to inform work streams, roadmap, backlog, town halls, steering committees, customer forums, vendor updates, and one-to-ones.
**Don't:**
- Don't make accountability democratic.
- Don't use “Consulted” for people whose input cannot change the work.
- Don't give Informed stakeholders hidden decision rights.
- Don't dismiss the RACI as obvious busywork.
- Don't combine it with the Stakeholder Matrix merely to save a document.
**Four project questions:**
- What are we doing?
- Who is doing it?
- When must it be done?
- Why are we doing it?
*Ref: Technology Strategy Patterns.md — “RACI”; “Alignment Meetings”*
---
### 27. Match Strategy to the Company's Life-Cycle Stage
**Principle:** Use revenue trajectory, market position, and innovation appetite to adapt the technology strategy.
**Do:**
- Use public filings and earnings material to establish the stage where available.
- Treat the thresholds as rough guidance, not mechanical rules.
- Inspect multiple years rather than one result.
- In introduction, focus on survival, customer acquisition, timing investment, and revenue.
- In growth, focus on expansion, automation, quality, process efficiency, decision flow, culture, reuse, and cost management.
- At 20% or more growth, emphasize time to market and strengthening the core.
- At 8–15%, inspect whether the business is accelerating or slowing and prepare for a pivot.
- At 5–8%, examine mature-company alternatives such as cross-selling, stickiness, platforms, and add-ons.
- At 0–5% or negative growth, address both top-line revenue and bottom-line cost.
- In maturity, use PESTEL and Five Forces to confront reinvention and substitution.
- In decline, break the cost-cutting/no-innovation spiral.
- Respect sustainable small-company longevity; growth is not a natural law.
**Don't:**
- Don't infer stage from one revenue number.
- Don't apply a growth-stage spending posture to decline.
- Don't cut all innovation in response to declining revenue.
- Don't pursue growth for its own sake into markets the organization does not understand.
- Don't assume a mature company must decline.
**Cases:**
- IBM reinvented around services as mainframe dominance changed.
- Microsoft incorporated Linux products that were once strategically unthinkable.
- Long-lived companies often remain small and serve durable human needs.
*Ref: Technology Strategy Patterns.md — “Life Cycle Stage”; “Mature Tech Companies”; “Growth for Growth's Sake”*
---
### 28. Use the Value Chain to Tie Technology to Value
**Principle:** Map technology action to the discrete activities that create margin, differentiation, or cost.
**Do:**
- Understand inbound logistics, operations, outbound logistics, marketing and sales, and service.
- Identify owners and knowledgeable participants at each point.
- Ask about each activity through people, process, and technology.
- Find ways to sustain, maximize, and discover value.
- Reduce debilitating technical debt when it improves time to market, time to value, or labor efficiency.
- Rework inefficient code or architecture where it lowers server and network cost.
- Automate manual processes where turnaround, quality, or labor use improves.
- Evaluate open-source substitutions for expensive enterprise contracts.
- Improve digital delivery, training, tracking, and customer transparency.
- Design modular products to reduce service cost.
- Keep differentiating activity in-house and become expert at it.
- Consider outsourcing nondifferentiating activity.
- Remove false requirements created by “how we've always done it.”
- Establish baseline cost and performance before change.
- Measure the realized difference afterward.
**Don't:**
- Don't claim payroll cost savings unless payroll actually changes.
- Don't call reassigned capacity a cash saving.
- Don't let supporting departments optimize their own process at the expense of value creators.
- Don't leave revenue effects out of a cost-focused strategy.
- Don't apply Porter's diagram rigidly where the software product changes the role of technology.
**Value modes:**
- **Sustain value:** Keep current operations and necessary plumbing working.
- **Maximize value:** Improve current systems and processes.
- **Discover value:** Create new products, markets, and channels.
**Reality check from the CFO case:**
- Automation reduced work from ten people to six.
- No one was to be removed from payroll.
- Therefore the proposal could claim benefit or capacity, not direct cost savings.
*Ref: Technology Strategy Patterns.md — “Value Chain”; “Maximizing Efficiency”; “Maximizing Value”; “Get Real”; “Applying the Value Chain”*
---
### 29. Map the Real Revenue and Partner Ecosystem
**Principle:** Understand every material revenue source, strategic bet, joint venture, partner, and licensing relation before choosing architecture.
**Do:**
- Investigate how each business unit actually earns money.
- Distinguish popular brand perception from revenue mix.
- Identify cross-subsidies.
- Identify products that exist to produce strategic data rather than current revenue.
- Identify joint ventures and partnerships that alter “competitor” relationships.
- Design data models and services around the real business relationships.
- Keep the Value Chain coherent within a business unit while adapting it where useful.
- Baseline revenue and cost by activity.
**Don't:**
- Don't assume the flagship product is the entire business.
- Don't classify a company as only competitor or only partner without checking executive arrangements.
- Don't discard non-revenue products that supply a critical strategic capability.
- Don't architecture around an incomplete revenue model.
**Cases:**
- PepsiCo's portfolio extends far beyond Pepsi cola.
- Coca-Cola owned Columbia Pictures for a period.
- Nestlé owns thousands of brands and participates in pet food and cosmetics.
- Hotels can earn substantial revenue outside rooms.
- Las Vegas shifted from predominantly gaming to predominantly nongaming revenue.
- Google's non-ad businesses can supply data for its broader AI strategy.
- Waymo was projected as a future top-line contributor.
*Ref: Technology Strategy Patterns.md — “Revenue Diversity”; “Value Chain”*
---
### 30. Allocate Product Investment with the Growth-Share Matrix
**Principle:** Classify products by market growth and relative share to guide resource allocation.
**Do:**
- Milk cash cows while avoiding unnecessary growth investment.
- Use cash generated by mature high-share products to fund innovation.
- Investigate why question marks have low share in growing markets.
- Decide whether to invest enough to create a star or stop.
- Continue investing in stars to protect growth and share.
- Aim for successful stars to become cash cows.
- Stop investing in dogs and plan retirement.
- Align placement with the business strategy team.
- Use the matrix during portfolio planning and strategy season.
- Keep the matrix as a conversation aid.
**Don't:**
- Don't plan grand upgrades for dogs.
- Don't treat a cherished product as strategic merely because it is familiar.
- Don't keep funding a question mark indefinitely without a path to share.
- Don't treat the 2×2 too seriously.
**Quadrants:**
- Cash cows: low growth, high share.
- Question marks: high growth, low share.
- Stars: high growth, high share.
- Dogs: low growth, low share.
> “If you are attacked by a wild strategy consultant, do not run: simply show him a PowerPoint slide with a 2×2 matrix on it.”
*Ref: Technology Strategy Patterns.md — “Growth-Share Matrix”*
---
### 31. Balance Core Proximity and Innovation with the Wave
**Principle:** Prioritize proposed products, acquisitions, projects, and features by proximity to the core and degree of innovation.
**Do:**
- List applications, acquisition targets, projects, and candidate activities.
- Score proximity to the core.
- Use revenue, expected revenue, mission criticality, customer importance, and enabling power to assess core proximity.
- Score innovation by novelty and differentiation.
- Put extra nurturing, time, talent, and risk capacity around innovative work.
- Bias funding toward initiatives that are both innovative and close to the core.
- Use the waves to discuss next-year and two- or three-year work.
- Use the result to guide architecture attention and staffing.
- Carve out 5–10% of a team for R&D where justified.
- Use the tool within one project as a fractal prioritization aid.
- Combine it with Growth-Share Matrix, Investment Map, Ansoff, and APM.
**Don't:**
- Don't fund maintenance and pioneering work with identical staffing assumptions.
- Don't expect R&D to happen around fully committed daily roadmaps.
- Don't use the Wave alone to decide.
- Don't mistake novelty far from the core for strategic priority.
**Decision dimensions:**
- Proximity to core business and applications.
- Degree of innovation or first-of-kind work.
- Time horizon.
- Talent and management posture.
- Funding and risk profile.
*Ref: Technology Strategy Patterns.md — “Core/Innovation Wave”*
---
### 32. Temper Ideas with the Investment Map
**Principle:** Compare implementation difficulty with market readiness before committing portfolio investment.
**Do:**
- List the current portfolio and candidate new work.
- Include new products, enhancements, technology trials, and major architecture changes.
- Score implementation difficulty.
- Include novelty, risk, complexity, effort, budget, and unknowns in difficulty.
- Score customer and market readiness.
- Generate a labeled 2×2.
- Use it in product, strategy, development, and architecture discussions.
- Feed the result into roadmap, budget, and priority decisions.
- Put the concise result in the Strategy Deck.
- Update it during strategy, budget, and roadmap planning; twice yearly can be sufficient.
**Don't:**
- Don't equate executive enthusiasm with market readiness.
- Don't ignore physical, operational, or adoption dependencies.
- Don't make a pioneering investment merely because the idea is elegant.
- Don't interpret the map as a money-allocation algorithm.
**Digital hotel-key case:**
- Smartphone adoption was incomplete.
- Guests could run out of battery.
- Hotels still needed conventional locks.
- Early technology was imperfect.
- Failure would block room access, not merely inconvenience a game player.
- Market and franchisee readiness therefore constrained investment despite an attractive idea.
*Ref: Technology Strategy Patterns.md — “Investment Map”*
---
### 33. Connect Principles, Practices, and Tools
**Principle:** Make tools implement practices and make practices realize explicit strategic principles.
**Do:**
- State principles as propositions that guide local decisions.
- Derive principles from the corporate vision.
- Explain each principle in actionable terms.
- Define practices as daily processes.
- Name tools as concrete products or technologies.
- Trace every tool to a practice.
- Trace every practice to one or more principles.
- Look for missing elements.
- Look for mismatches.
- Look for improvement and upgrade opportunities.
- Use the pattern when establishing a department, methodology, process, toolset, platform, portfolio plan, or turnaround.
- Build competitive differentiators.
- Buy capabilities that do not differentiate.
**Don't:**
- Don't publish “Global cloud” without operational meaning.
- Don't let a principle remain unsupported by practice.
- Don't let a tool exist without a strategic rationale.
- Don't allow the department to become a collection of overlapping tools.
- Don't substitute tools for operating-model design.
**Book example — “Global cloud” implications:**
- Build services and applications for cloud operation.
- Use autoscaling and auxiliary cloud capabilities.
- Preserve portability in application structure.
- Externalize configuration.
- Use infrastructure as code.
- Plan for global, multiple-data-center deployment.
- Externalize localization and internationalization.
- Keep services stateless.
- Partition data for concurrent global deployments.
**Named example tools and practices:**
- Practices: infrastructure as code, CI/CD, service design review, governance, DevOps, chaos engineering.
- Tools: TensorFlow, Ansible, Log4J, Kafka, Python, CloudFormation, Gruntwork.
*Ref: Technology Strategy Patterns.md — “Principles, Practices, Tools”; “Principles”; “Practices”; “Tools”*
---
### 34. Assess Process Posture Correctly
**Principle:** Tag each process with a current action posture, then use the set to create a slate of improvement work.
**Do:**
- List processes in MECE categories.
- State each process's goal.
- State the value it creates.
- Name the business-process owner where one exists.
- Assign one of the source's five postures.
- Use Start when the capability is absent but should be established.
- Use Continue when it is generally on track and needs normal improvement.
- Use Invest when a nascent capability has strong potential.
- Use Assess when an existing capability needs efficiency examination.
- Use Revise when the capability is clearly weak and requires overhaul.
- Inspect the overall distribution of tags.
- Use many Start tags as evidence of missing capability.
- Use many Revise tags as evidence of broad damage.
- Validate the assessment with other leaders.
**Don't:**
- Don't use the invented labels “Develop,” “Optimize,” “Maintain,” or “Sunset” as if they came from this source.
- Don't reengineer every weak process alone.
- Don't tag without defining goal and value.
- Don't ignore missing ownership.
- Don't treat process posture as a maturity score detached from action.
**Exact source taxonomy:**
- Start.
- Continue.
- Invest.
- Assess.
- Revise.
*Ref: Technology Strategy Patterns.md — “Process Posture Map”*
---
### 35. Move from Current State to Future Operating Model
**Principle:** Show the current and desired operating model, then let managers define concrete transition work.
**Do:**
- Examine trends in new practices.
- Build the current Process Posture Map.
- Build Current State and Future State Operating Model slides.
- Make the future state understandable to teams.
- Ask managers to propose concrete actions connecting current and future states.
- Put ownership into a RACI.
- Track the transition.
- Build a Sankey diagram connecting principles, practices, and tools.
- Confirm every principle has implementing practices.
- Confirm every practice has supporting tools.
- Use line magnitude to show degree of support where useful.
- Use BPMN 2.0 to map problematic business processes.
- Map current state before collaboratively mapping the improved state.
- Prioritize process candidates by ease and impact.
**Don't:**
- Don't turn a five-year strategy into a static publication that is obsolete on arrival.
- Don't let unsupported principles remain decorative.
- Don't map detailed process before agreeing which process matters.
- Don't omit people and ownership from operating-model change.
**NASA case:**
- Use NASA's public CIO strategy as an example of vision → mission → principles → goals → outcomes.
- Notice its explicit “secure,” “integrated,” and “cost-effective” principles.
- Adapt the structural lesson without assuming a government five-year publication format fits a competitive technology company.
*Ref: Technology Strategy Patterns.md — “Example: NASA Strategy”; “Current and Future Model”; “The Principles, Practices, Tools Sankey Diagram”; “Business Process Mapping”*
---
### 36. Multiply Process Probabilities Instead of Averaging Them
**Principle:** For independent steps that must all succeed, multiply their probabilities to estimate the whole process.
**Do:**
- Identify independent events in one process instance.
- Estimate the relevant success or optimization measure for each.
- Multiply them.
- Compare the product with the misleading arithmetic average.
- Use the result to expose hidden process weakness.
- Apply the reasoning to deployment, methodology, defect leakage, and technical-debt-related process measures.
- Use it as a reminder that a chain can be much weaker than its average step.
**Don't:**
- Don't average sequential independent probabilities.
- Don't apply the product rule to repeated instances when the question concerns one process chain.
- Don't add false precision to rough input measures.
- Don't conclude that individually healthy steps imply a healthy end-to-end process.
**Book example:**
- Step optima: 80%, 85%, 90%, 85%, 90%.
- Arithmetic average: 86%.
- Product: approximately 47%.
- Strategic implication: the overall process has farther to improve than the average suggests.
*Ref: Technology Strategy Patterns.md — “The Law of the Product of Probabilities”*
---
### 37. Manage Applications as a Portfolio
**Principle:** Assess all applications together by business value, technical risk, cost, ownership, and future fit.
**Do:**
- Use APM when the application set is too large or disputed to manage mentally.
- Start with agreed business goals.
- State technology goals.
- Build the agreed application list.
- Name business and technical owners.
- Define weighted business and technology questions.
- Score each application numerically.
- Preserve the spreadsheet as the “long math.”
- Generate a bubble chart and 2×2.
- Transfer conclusions into a deck.
- Review with owners and stakeholders.
- Identify redundant and unused applications.
- Consolidate similar applications.
- Retire expensive legacy applications with low value.
- Map data flow to optimize security controls.
- Map applications to business capabilities.
- Decompose a large application into logical modules when different modules support different capabilities.
**Don't:**
- Don't run a heavy APM exercise for six obvious applications.
- Don't score before agreeing what counts as an application.
- Don't accept open-ended answers where a comparable score is required.
- Don't let the spreadsheet replace stakeholder negotiation.
- Don't treat current value as expected future value.
**Asset classes:**
- **Strategic:** Creates advantage, serves many customers, is expected to grow, or is competitively necessary.
- **Informational:** Must provide reliable, comprehensive, timely decision data.
- **Transactional:** Runs the business; optimize cost, throughput, stability, and modernization.
- **Infrastructure:** Enable internal customers with reliability, cost control, flexibility, and useful standardization.
*Ref: Technology Strategy Patterns.md — “Application Portfolio Management”; “Planning with Asset Classes”; “Capability Mapping”*
---
### 38. Treat Technical Debt as One Portfolio Dimension
**Principle:** Evaluate debt and technical risk relative to business alignment; do not rank debt in isolation.
**Do:**
- Score code adherence to strategy.
- Score infrastructure and data adherence.
- Score modularity.
- Score fault tolerance.
- Score monitoring and management completeness.
- Score automated testing.
- Score provisioning and deployment automation.
- Score training and documentation.
- Score security implementation.
- Score three-year technology relevance.
- Score skill sustainability.
- Score core application and integration SLA performance.
- Compare those technical factors with strategic differentiation, mission criticality, outage impact, feature alignment, adaptability, governance, and process fit.
- Grow, evolve, and maintain high-value/low-risk applications.
- Tolerate low-value/low-risk applications while minimizing cost and planning consolidation, outsourcing, or retirement.
- Retire low-value/high-risk applications.
- Reengineer, modernize, or replace high-value/high-risk applications.
- Use internal Due Diligence to create a product-level debt roadmap.
**Don't:**
- Don't call the source's portfolio quadrants Invest/Migrate/Eliminate; those are not the labels used in the book.
- Don't modernize every indebted application.
- Don't retire a high-debt application without assessing strategic business value.
- Don't keep strategic applications in a high-risk state through feature-only investment.
- Don't mistake current-state assessment for action.
**Exact APM postures:**
- Grow/evolve/maintain.
- Tolerate.
- Retire.
- Reengineer/modernize/replace.
**Project Heat Map extension:**
- List projects.
- Estimate net business value through measures such as ROI or IRR.
- Assess quality through technology, capability, cost, and schedule.
- Kill low-quality/low-value projects.
- Continue high-quality work.
- Investigate question marks according to their heat-map position.
*Ref: Technology Strategy Patterns.md — “Business and Technology Attributes”; “APM Application Assessment Quadrant”; “Project Heat Map”; “Internal Use”*
---
### 39. Give the 30-Second Answer
**Principle:** State the answer, give three supporting reasons, then stop.
**Do:**
- Map three bullets mentally.
- Lead with a simple, declarative, definitive answer.
- Give three high-level reasons.
- Imagine one headline and three large-font support points.
- Stop and let the executive decide or drill down.
- Infer whether the executive wants status, help needed, or a recommendation.
- Practice until leaving out detail feels responsible rather than incomplete.
**Don't:**
- Don't answer “it depends” without first giving direction.
- Don't narrate every uncertainty to display expertise.
- Don't force the executive to identify the conclusion.
- Don't keep talking after the decision maker has enough.
**Example structure:**
- Answer: Delay one week.
- Reason 1: Customers are entering peak season.
- Reason 2: Load-test results are inconclusive.
- Reason 3: Holiday support coverage may be incomplete.
*Ref: Technology Strategy Patterns.md — “30-Second Answer”*
---
### 40. Adopt the Rented-Brain Posture
**Principle:** Speak truth to power as if objectivity and candor were the explicit terms of your engagement.
**Do:**
- Know your own book of business.
- Tell leaders bad news early.
- Ask teams for bad news.
- Make it safe to surface delay, risk, and failure.
- Pretend each day that you are an independent adviser.
- Expose the elephant in the room.
- Give the hard recommendation even when it challenges a prior decision.
- Build internal analytical capability instead of reflexively outsourcing thought.
- Use external consultants where independent expertise is truly required.
**Don't:**
- Don't hire consultants merely to avoid accountability for a plan.
- Don't train people to hide bad news by punishing messengers.
- Don't go along to get along.
- Don't assume famous consulting firms are infallible.
- Don't mistake access, templates, and pedigree for truth.
**Cases:**
- A successful retailer's CEO required the vice president to produce his own plan rather than substitute consultants for leadership.
- Enron paid McKinsey while leadership and governance failed catastrophically.
- The lesson is neither “always hire” nor “never hire”; it is to preserve accountability, objectivity, and judgment.
> “Speak truth to power. Tell powerful people what they need to hear, not what they want to hear.”
*Ref: Technology Strategy Patterns.md — “Rented Brain”; “The Smartest Guys in the Room”*
---
### 41. Persuade with Logos, Ethos, and Pathos
**Principle:** Combine logical, ethical, and emotional appeals without manipulation.
**Do:**
- Use charts, graphs, data, syllogisms, hypotheses, methods, metrics, probabilities, and ranges for logos.
- Establish credibility through relevant expertise and trustworthy conduct for ethos.
- Cite respected sources only where their authority is relevant.
- Build emotional commitment to the outcome for pathos.
- Use demonstrations and town halls to create energy.
- Balance all three appeals according to the setting.
- Audit every argument for logical fallacies.
**Don't:**
- Don't assume facts alone guarantee approval.
- Don't use title or company prestige as proof.
- Don't substitute excitement for an investment case.
- Don't overload the audience with irrelevant technical detail.
- Don't manipulate emotion.
**Fallacies to reject:**
- **Ad hominem:** Attack the person rather than the claim.
- **Affirming the consequent:** Infer P from “If P then Q” and Q.
- **Blind authority:** Treat a title, famous person, or large company as sufficient proof.
- **Blinding with science:** Use jargon and volume to force deference.
- **Hasty generalization:** Infer a broad rule from thin or biased evidence.
- **Petitio principii:** Reword the premise as its own conclusion.
- **Post hoc, ergo propter hoc:** Infer causation from sequence.
**Antidotes:**
- Ask for evidence.
- Ask for definitions.
- Ask why the technical detail matters to the outcome.
- Separate a troubleshooting lead from a proven cause.
- Verify authority relevance.
*Ref: Technology Strategy Patterns.md — “Ars Rhetorica”; “Logical Fallacies”*
---
### 42. Make Approval a Fait Accompli Through Inclusion
**Principle:** Hold the meeting before the meeting so the formal decision contains no avoidable surprise.
**Do:**
- Use Stakeholder Matrix and RACI to build the invite list.
- Identify the most powerful participants.
- Identify the people most affected by the proposal.
- Identify likely skeptics, showboaters, and threatened owners.
- Meet each key stakeholder privately.
- Explain the direction.
- Ask what is missing.
- Ask how the proposal can improve.
- Incorporate valid feedback.
- Ask explicitly whether the revised direction can be supported.
- Credit stakeholder contributions in the formal meeting.
- State the formal agenda and decision clearly.
- Aim for a calm, unsurprising approval meeting.
**Don't:**
- Don't unveil weeks of work to a cold audience.
- Don't imitate a dramatic product reveal.
- Don't act as a sage returning from the mountaintop.
- Don't impose change without giving affected people a voice.
- Don't describe this pattern as manipulation; use it to improve the work materially.
**Change insight:**
- People change willingly.
- People resist change imposed without consultation.
- Inclusion converts an external imposition into a shared direction.
> “If you don't give them power, they will take yours.”
*Ref: Technology Strategy Patterns.md — “Fait Accompli”; “Facing a Cold Audience”; “The Meeting Before”*
---
### 43. Structure the Ask as a True Story
**Principle:** Use dramatic structure as an invisible organizing frame for truthful evidence and a clear recommendation.
**Do:**
- Establish the status quo and shared current state.
- Show the inciting incident that makes status quo untenable.
- Quantify the problem or opportunity.
- Show the consequence of doing nothing.
- Reduce the consequence to cost, quality, speed, revenue, customers, or employees.
- State one path forward.
- Describe people, process, and technology changes.
- Show duration, cost, and ownership.
- Define done.
- Define progress metrics.
- Define reporting and governance.
- Use Shock and Awe only as a sequence of brutal, true facts.
- Use inability to fit the structure as a diagnostic for a solution looking for a problem.
**Don't:**
- Don't fictionalize.
- Don't use hyperbole.
- Don't tell the audience you are applying a movie plot.
- Don't manufacture urgency.
- Don't recommend a tool if nothing material happens when the organization declines it.
**Basic arc:**
1. Status quo.
2. Inciting incident.
3. Problem and unavoidable challenge.
4. Struggle and path discovery.
5. Resolution and new normal.
**Definition-of-done close:**
1. Show the concrete end state.
2. Show how success and progress will be measured.
3. Show how stakeholders retain visibility and control.
*Ref: Technology Strategy Patterns.md — “Dramatic Structure”; “Establish the Status Quo”; “Create an Inciting Incident”; “The Plan”; “Shock and Awe”*
---
### 44. Deconstruct the Problem and Your Own Model
**Principle:** Solve the local issue while examining the category, context, assumptions, and repeated organizational mechanism that creates it.
**Do:**
- Inspect the local problem.
- Inspect the category that contains it.
- Inspect associations with the same problem in other contexts.
- Ask how not to have the problem rather than how to solve it repeatedly.
- Externalize specialist knowledge.
- Share it quickly.
- Template and automate repeated work.
- Argue against your own hypothesis.
- Put it through a mock trial and Logic Tree.
- Examine bias and assumed constraints.
- Synthesize people, process, technology, time, velocity, and force.
- Build a new model that allows others to solve the recurring problem without you.
- Treat the architect and strategist as context creators.
**Don't:**
- Don't optimize only the local cluster.
- Don't turn the most skilled troubleshooter into a permanent single point of failure.
- Don't reward heroics without removing the mechanism that requires them.
- Don't confuse job preservation with valuable work.
- Don't let inherited labels fix the solution space.
**Code-formatted quotation preserved from the book:**
```
It ain't what you don't know that gets you into trouble. It's what you
know for sure that just ain't so.
```
**Five-step metamodel:**
1. Discover and decompose problems and opportunities.
2. Hypothesize and search for broader context and global maxima.
3. Observe and undermine your own model.
4. Synthesize across frames.
5. Build and externalize a reusable context.
*Ref: Technology Strategy Patterns.md — “Deconstruction”; “Three Levels of Problems”; “Three Causes of Problems”; “The World as System: Synthetic Decomposition”*
---
### 45. Build a Scalable Business Machine
**Principle:** Design the organization as a system of actions, deliverables, outputs, outcomes, roles, processes, tools, and metrics.
**Do:**
- Detect hero culture and single points of knowledge or process failure.
- Treat culture symptoms as connected to strategy and execution design.
- Apply architecture qualities to the business system.
- Use fitness to purpose, portability, scalability, extensibility, availability, monitorability, manageability, maintainability, resilience, security, auditability, performance, testability, and elegance.
- Hide details behind interfaces.
- Apply least knowledge.
- Separate concerns.
- Keep coupling loose.
- Isolate independent change.
- Reuse deliberately.
- Manage risk explicitly.
- Apply SOLID principles to processes and departments as well as software.
- Start with external customer outputs and outcomes.
- Work inward to departmental outputs.
- Define actions and deliverables only after the outcomes.
- Define roles and decision rights.
- Define metrics and the data required to calculate them.
- Create reusable templates.
- Identify process hotspots.
- Communicate and manage the change.
**Don't:**
- Don't celebrate repeated all-nighters as a scalable model.
- Don't let support departments behave as though value creators exist to serve support processes.
- Don't expose internal deliverables to customers as if they were outcomes.
- Don't start process design from today's internal activity.
- Don't make a metric without asking what behavior it drives and how it can be gamed.
**Core terms:**
- **Action:** Atomic work inside a department; create, approve, or review.
- **Tool:** Concrete means used to create a deliverable.
- **Deliverable:** Internal work product needed to build an output.
- **Output:** Product or coherent service visible and valuable to customers.
- **Outcome:** Benefit the output creates.
- **Department:** Logical group producing outputs of the same kind.
- **Business unit:** Owner of product SKUs and a P&L.
- **Company:** Legal container for units and departments.
**Execution sequence:**
1. Define vision and scope.
2. Define departments and customer outcomes.
3. Define activities and deliverables.
4. Define customers and personas.
5. Define principles.
6. Define outputs.
7. Assess the Value Chain.
8. Define processes.
9. Define tools.
10. Define roles and RACI.
11. Define metrics and source data.
12. Create templates.
13. Determine hotspots.
14. Communicate the machines.
15. Manage the change.
*Ref: Technology Strategy Patterns.md — “Scalable Business Machines”; “Business as System”; “Aspects of the Scalable Business Machine”; “Executing”*
---
### 46. Summarize Strategy with the One-Slider and Use Case Map
**Principle:** Distill the strategic system without losing the line from vision to execution, culture, customer outcome, and measurement.
**Do:**
- Put a one- to three-year vision at the top of the One-Slider.
- Put three or five strategic goals beneath it.
- Make each goal support the vision.
- List concrete initiatives or practices that execute the goals.
- Name accountable owners.
- State the culture required across all initiatives.
- Put supporting detail on later slides.
- Make an initiative table with initiative, actions, deliverables, and accountable role.
- Turn major system ideas into one Use Case Map per use case.
- State the customer outcome.
- List major features.
- List required data components.
- List major system components.
- Define a SMART customer-success measure.
- Decompose the map into product epics and architecture work.
**Don't:**
- Don't make the One-Slider a decorative executive summary.
- Don't put every analytical detail on one slide.
- Don't use “winning teams” or similar culture platitudes.
- Don't call internal activity a customer outcome.
- Don't omit data and system components from the use-case view.
**One-Slider layers:**
- Vision.
- Strategic goals.
- Initiatives/practices.
- Culture.
**Use Case Map components:**
- Customer outcome.
- Features.
- Data components.
- System components.
- Customer success measure.
*Ref: Technology Strategy Patterns.md — “One-Slider”; “Use Case Map”*
---
### 47. Cost Directionally and Prioritize Strategically
**Principle:** Set estimate expectations explicitly and use ranges, stages, assumptions, and reusable templates.
**Do:**
- Treat estimation as a project when decision stakes justify it.
- Build a reusable estimation form.
- Use a funnel with stage gates.
- Produce a Rough estimate in days and communicate a broad range.
- Produce a Refined estimate after discovery and requirements work.
- Produce a Realistic estimate after architecture and requirement commitment.
- Allow later estimates to fall outside earlier ranges.
- Narrow confidence as evidence improves.
- Always include contingency.
- Use ranges rather than false precision.
- State assumptions that can change cost materially.
- Estimate development teams and supporting roles.
- Include data-center or cloud cost.
- Identify serial work and parallel work.
- Front-load possible showstoppers.
- Distinguish capex and opex where useful.
- Use the Priority Map with Ansoff, Investment Map, or weighted scoring.
- Use Priority Map for strategic initiatives, not sprint backlog.
**Don't:**
- Don't promise a one-night estimate for a multiyear transformation as if it were a commitment.
- Don't preserve the original rough number after better evidence appears.
- Don't estimate coding only.
- Don't omit testing, error handling, instrumentation, documentation, deployment, clarification, refactoring, profiling, and alternate paths.
- Don't give a precise number for an uncertain multi-year effort.
- Don't assume the executive wants precision; often the decision is whether the cost is closer to $1 million or $10 million.
**Estimate stages from the book:**
- **Rough:** A few days; perhaps within 50%.
- **Refined:** A couple of weeks; perhaps within 25%.
- **Realistic:** Substantial homework; perhaps within 5–10%.
**Margarita Mix team example:**
- Four developers.
- Two testers.
- One analyst.
- Seven FTEs total.
- At $70/hour for two 40-hour weeks: $39,200, rounded to $40,000 per sprint.
*Ref: Technology Strategy Patterns.md — “Directional Costing”; “Rough, Refined, Realistic Estimates”; “Estimate Template”; “Priority Map”*
---
### 48. Operate an Evolving Technology Radar
**Principle:** Communicate current technology and practice direction as an evolving, inclusive, transparent radar rather than a frozen target state.
**Do:**
- Divide the radar into Tools, Techniques, Languages & Frameworks, and Platforms.
- Place entries in Adopt, Trial, Assess, or Hold.
- Use Adopt for technologies teams should use now.
- Use Trial for active project experimentation.
- Use Assess for learning and evaluation.
- Use Hold for containment or avoidance.
- Adapt the radar's categories where organizational needs differ.
- Show teams what to research.
- Collect feedback from teams.
- Update the radar methodically.
- Use movement between rings to show strategic progress.
- Combine the radar with Priority Map when useful.
- Treat it as guidance or dictum according to culture, but make that posture explicit.
**Don't:**
- Don't publish a single pristine architecture future and freeze it.
- Don't make the radar only an inventory.
- Don't omit a feedback mechanism.
- Don't leave ring meaning ambiguous.
- Don't confuse platform quadrant placement with proof that the organization owns a platform.
> “The Technology Radar will evolve over time, in a methodical, inclusive, transparent manner.”
*Ref: Technology Strategy Patterns.md — “Technology Radar”*
---
### 49. Choose Build, Buy, or Partner Deliberately
**Principle:** Align acquisition mode with differentiation, capability, time, control, risk, and long-term intent.
**Do — Build:**
- Build when the organization is or wants to be a market pioneer.
- Build when owning intellectual property matters.
- Build when skilled technologists and sufficient time exist.
- Build when the capability is core and long-lived.
- Build when ownership enables future expansion.
- Build when patenting, licensing, or asset value is plausible.
- Ask whether this is the best use of organizational capacity.
- Ask whether the team can complete it materially better than available alternatives.
- Ask whether meaningful cost savings are real.
**Do — Buy:**
- Buy for fastest access to an existing capability.
- Buy off-the-shelf software for noncore functions.
- Buy a company or technology where capability, people, customers, or competitive denial justify it.
- Account for integration.
- Account for contract negotiation.
- Account for process changes required by the product.
- Perform Due Diligence.
**Do — Partner:**
- Partner when each company contributes a distinct leading capability.
- Use partnership to share risk and extend reach.
- Test the partner's financial health.
- Test strategic importance to both parties.
- Test relationship and operating compatibility.
- Test each party's ability to execute.
- Test whether speed is the dominant objective.
- Use partnership to test a market where evidence remains insufficient.
**Don't:**
- Don't build a nondifferentiating capability by default.
- Don't treat “buy” as integration-free.
- Don't customize purchased software until it recreates an expensive internal product.
- Don't partner without acknowledging loss of control and revenue share.
- Don't preserve a partnership indefinitely when the organization should choose whether to own the business.
**Control continuum:**
- Build: most control, longest time to market, ongoing maintenance, asset ownership.
- Buy: fast access, limited customization, vendor and contract dependence.
- Partner: shared capability and risk, least control over fate, potential market test.
*Ref: Technology Strategy Patterns.md — “Build/Buy/Partner”; “Build”; “Buy”; “Partner”*
---
### 50. Perform Due Diligence Externally and Internally
**Principle:** Score technology and operational quality before acquisition, licensing, or product investment.
**Do:**
- Build a reusable spreadsheet template.
- Create a summary sheet.
- Assess maintainability.
- Assess manageability.
- Assess portability.
- Assess security.
- Assess compliance.
- Assess privacy.
- Assess resiliency.
- Assess compatibility.
- Assess performance.
- Assess usability.
- Assess functional suitability.
- Add strategy and roadmap alignment.
- Create drill-down questions for each characteristic.
- Score each item from 0 to 4.
- Aggregate characteristic scores on the summary page.
- Use the result to buy, reject, reprice, license, or acquire only part of a target.
- Offer the same structure to enterprise customers assessing your product.
- Run the assessment on your own products as a Rented Brain.
- Use internal results to prioritize technical debt and lagging features.
- Designate an architect to lead the internal assessment.
**Don't:**
- Don't reduce Due Diligence to architecture, scalability, security, business, and culture labels not present in this template.
- Don't rely on demonstrations or deal momentum.
- Don't let business-development enthusiasm suppress technical findings.
- Don't score without definitions.
- Don't use the aggregate score without examining critical individual failures.
**Scoring legend:**
- 0: Unsupported and not on the roadmap.
- 1: Unsupported but on the roadmap.
- 2: Implemented but weak.
- 3: Implemented and suitable.
- 4: Implemented and world-class.
*Ref: Technology Strategy Patterns.md — “Due Diligence”; “Internal Use”*
---
### 51. Write the Architecture Definition as a Directive Contract
**Principle:** Record nonfunctional requirements in clear, measurable, testable, executable, directive language.
**Do:**
- Use the document for architecturally significant work.
- Weigh in when work crosses data-center or major network boundaries.
- Weigh in when work crosses system boundaries.
- Weigh in for high business value, visibility, or technical risk.
- Weigh in for material budget or business risk.
- Weigh in when key stakeholders have unresolved concerns.
- Weigh in for first-of-kind components.
- Weigh in when quality-of-service requirements differ from the existing architecture.
- Scale the document from a few pages to subsystem and system definitions.
- Allow child Architecture Definitions beneath an overarching one.
- Record system name, author, date, reviewers, and contributors.
- Use RFC 2119 terms MUST, SHOULD, MAY, and their negative forms.
- Capitalize those terms to signal requirement level.
- Put Business Architecture first.
- Follow with Application, Data, and Infrastructure Architecture.
**Don't:**
- Don't run architecture through email and meetings alone.
- Don't equate Agile with absence of requirements or design.
- Don't create thousands of pages when a middle level of formality is enough.
- Don't specify every local coding choice.
- Don't use architecture only after implementation to explain what happened.
**Five primary sections:**
1. Metadata or Front Matter.
2. Business Architecture.
3. Application Architecture.
4. Data Architecture.
5. Infrastructure Architecture.
*Ref: Technology Strategy Patterns.md — “Architecture Definition”; “The Template”; “Metadata”*
---
### 52. Complete the Business Architecture Section
**Principle:** Show how organizations, capabilities, processes, information, initiatives, products, people, constraints, and metrics support the strategic system.
**Do:**
- Identify relevant organizations.
- Identify capabilities.
- Map Value Chains and processes.
- Record current process posture.
- Identify information flows.
- Record laws, regulations, rules, and policies.
- Identify stakeholders and decision ownership.
- Record events generated by decisions.
- List current initiatives and their alignment.
- List products and services from APM.
- Identify training requirements.
- Define outcome metrics and required data.
- Ask what business constraints alter the technology design.
- Ask what business changes are required to support the technology.
- Record major features.
- State strategic fit.
- List business drivers.
- State priority biases such as time to market versus quality.
- List assumptions across people, process, and technology.
- List constraints.
- List business and customer risks.
- List organizational and process impacts.
- List internal and external stakeholders.
- Define governance cadence, membership, and purpose.
**Don't:**
- Don't stop at an inventory of organizations and capabilities.
- Don't omit the effect of technology on organization and training.
- Don't leave priority trade-offs implicit.
- Don't hide assumptions.
- Don't name a steering committee without decision purpose.
**Business section prompts:**
- Major Features.
- Strategic Fit.
- Business Drivers.
- Business Priorities.
- Assumptions.
- Constraints.
- Risks.
- Impacts.
- Stakeholders.
- Governance.
*Ref: Technology Strategy Patterns.md — “Business Architecture”*
---
### 53. Complete the Application, Data, and Infrastructure Sections
**Principle:** Specify the full operational system, not only software components.
**Do — Application:**
- Link applicable standards and policies.
- Link coding and design conventions.
- Specify UI/UX impact, method, and libraries.
- List services to create or reuse and their owners.
- Specify data security at rest, in transit, and in processing.
- Specify authentication, authorization, credentials, keys, and two-factor requirements.
- Specify availability targets and supporting mechanisms.
- Specify scalability units, throughput, latency, utilization, and thresholds.
- Specify extension points, APIs, configuration, and customer variation.
- Specify test types, tools, automation, load, chaos, and resilience plans.
- Specify maintainability guidance, repositories, and upgrade schedules.
- Specify monitoring, logging, dashboards, alerts, and thresholds.
**Do — Data:**
- Name sources, services, databases, and instances.
- State hard row and transaction-size limits.
- State eventual-consistency tolerance.
- State warehouse, storage, management, and transfer requirements.
- State transaction and two-phase-commit requirements.
- State volatility.
- State maintenance, retention, restoration, truncation, and encryption.
- State migration, replication, ETL, Kafka, or other mechanisms.
- State migration duration and synchronization period.
- State daily growth, total volume, and number of stores.
- State logging and rotation requirements.
- State analytics exposure.
- State caching locations and technology.
**Do — Infrastructure:**
- Name cloud and data centers.
- Specify inter-data-center communication.
- Specify cost management.
- Specify deployment-pipeline requirements.
- Specify infrastructure as code, containers, and orchestration.
- Specify deployment method, including blue/green and CI/CD.
- Specify disaster recovery.
- Diagram firewalls, gateways, load balancers, VIPs, zones, routing, and DNS.
**Don't:**
- Don't define availability without a measurable target.
- Don't define scalability without a unit of scale.
- Don't say “secure” without data states and controls.
- Don't omit migration from data architecture.
- Don't omit cost and deployment from infrastructure architecture.
*Ref: Technology Strategy Patterns.md — “Application Architecture”; “Data Architecture”; “Infrastructure Architecture”*
---
### 54. Make Architecture Executable Through Teams
**Principle:** Translate the formal definition into acceptance criteria, stories, conversation, review, and revised implementation guidance.
**Do:**
- Put NFRs into functional-story acceptance criteria where possible.
- Write specific NFR stories only when necessary.
- Keep NFRs measurable, demonstrable, and testable.
- Talk to teams with the document as the center of discussion.
- Hold a Definition Defense meeting.
- Invite architects, development leaders, analysts, product managers, and relevant technical stakeholders.
- Attach the definition to the invite.
- Give participants days to review.
- Present major decisions and unusual aspects.
- Welcome questions and criticism.
- Take notes without defensiveness.
- Revise and redistribute the definition.
- Follow up until feedback appears in implementation work.
- Use the document and local requirements together as the reusable department output.
**Don't:**
- Don't hand off a document and disappear.
- Don't make separate NFR stories in a way that tells feature teams they do not own architecture quality.
- Don't confuse “executable” with generating the whole architecture from a commercial modeling tool.
- Don't let architecture software become slower and more outdated than the system.
- Don't make the review board a “star council” passing judgment on a passive architect.
**Definition Defense sequence:**
1. Write the definition.
2. Schedule a clearly named review.
3. Attach the document and allow reading time.
4. Review key decisions.
5. Open discussion.
6. Record criticism.
7. Revise and resend.
8. Verify incorporation.
*Ref: Technology Strategy Patterns.md — “Executable Architectures”; “The Definition Defense”; “Dissertation Defense”*
---
### 55. Build the Deck Before Filling It
**Principle:** Use a Ghost Deck as a storyboard whose headlines alone carry the complete argument.
**Do:**
- Start with an outline outside PowerPoint.
- Work one inch deep across the whole field.
- Write every slide headline before slide bodies.
- Make each headline a bold claim.
- Review the sequence for rhetorical force and dramatic structure.
- Make the headline set tell the complete story.
- Fill bodies with evidence supporting the claims.
- Assign research and chart work after the structure is accepted.
- Request frequent shoulder checks.
- Use the deck to align cross-functional contributors before expensive production.
- Treat the headline sequence like a backlog for analysis.
**Don't:**
- Don't begin by decorating one finished slide.
- Don't use passive labels such as “The Plan.”
- Don't let different contributors create a patched-together narrative.
- Don't invest in charts before the claims are coherent.
- Don't use a Ghost Deck by itself; it exists to structure another deck.
**Ghost Deck sequence:**
1. Outline the whole argument.
2. Write all headlines.
3. Validate the headline story.
4. Research and populate evidence.
5. Review incrementally.
*Ref: Technology Strategy Patterns.md — “Ghost Deck”*
---
### 56. Put the Ask First
**Principle:** Tell the executive the decision, cost, duration, resources, milestones, and outcome on slide one.
**Do:**
- Write slide one last.
- Put the requested action in one headline sentence.
- State three dramatic current-state facts.
- Name the project.
- List milestones.
- State duration.
- State team count.
- State capex and opex.
- State the end state purchased by the investment.
- Treat the rest of the deck as a drill-down of slide one.
- Imperil the hero with true evidence.
- Let data drive the conclusion.
- Save the hero with the path forward.
- Ask explicitly for a yes decision.
- Put supporting query results, charts, and analysis in the appendix.
- Keep the main deck around 12–15 slides.
- Keep the appendix as long as substantiation requires.
**Don't:**
- Don't save the cost for a dramatic reveal.
- Don't force the CFO to flip to the last slide.
- Don't continue presenting if slide one wins the decision.
- Don't hide technical debt detail; put the full list in the appendix.
- Don't fail to ask for approval.
**Slide-one contents:**
1. Current state.
2. Requested action.
3. Milestones.
4. Duration, teams, capex, and opex.
5. End state.
**Ask Deck arc:**
- The ask.
- Imperil the hero.
- Let the data drive.
- Save the hero.
- The explicit decision.
- Appendix.
*Ref: Technology Strategy Patterns.md — “Ask Deck”*
---
### 57. Assemble the Strategy Deck from Pattern Outputs
**Principle:** Make the Strategy Deck a synthesis step, not a new round of unsupported invention.
**Do:**
- Execute the applicable creation patterns.
- Preserve outputs as working artifacts.
- Merge and sort the outputs.
- Build one smooth, comprehensive story.
- Apply communication patterns to every claim.
- Lead with executive-level conclusions.
- Keep broad context and long math in the appendix.
- Connect recommendations to roadmap, cost, ownership, metrics, culture, and execution.
**Don't:**
- Don't start the Strategy Deck from a blank slide without analysis artifacts.
- Don't repeat every pattern in presentation order when the audience needs a shorter story.
- Don't confuse analytical completeness with slide volume.
- Don't omit rejected options and decision rationale from supporting material.
**Comprehensive flow:**
- Analysis.
- World.
- Industry.
- Company.
- Department.
- Recommendation.
- Execution.
- Cost.
- Governance.
- Evidence appendix.
*Ref: Technology Strategy Patterns.md — “Strategy Deck”*
---
### 58. Turn Strategy into a Roadmap and Tactical Plan
**Principle:** Define outcome-oriented milestones first, then durations, dates, ownership, and executable work.
**Do:**
- Fit the Roadmap on one slide.
- Use it for executive alignment.
- Show major deliverable milestones rather than detailed tasks.
- Make each milestone useful independently where possible.
- Start from the end state.
- Backcast to necessary predecessor milestones.
- Show team ramp-up and cross-team dependencies where relevant.
- Build the Tactical Plan after roadmap and conceptual architecture.
- Estimate durations before dates.
- Identify serial and parallel work.
- Use the plan to support Directional Costing.
- Transfer the approved plan into project-management execution.
**Don't:**
- Don't use the executive Roadmap as the development team's detailed plan.
- Don't start with hard dates that distort duration estimates.
- Don't stop after strategy approval.
- Don't claim strategy execution without named deliverables and owners.
**Roadmap relationship:**
- Approved strategic direction.
- Conceptual architecture.
- Outcome milestones.
- Tactical durations.
- Resource and dependency model.
- Directional cost.
- Ask Deck.
- Project execution.
*Ref: Technology Strategy Patterns.md — “Roadmap”; “Tactical Plan”*
---
### 59. MergeSort the Tactical Work
**Principle:** Generate independent lists before group synthesis to reduce groupthink and increase coverage.
**Do:**
- State the meeting scope clearly.
- Give every participant a common outer category set.
- Use categories such as business, data, and infrastructure where appropriate.
- Use people, process, and technology as an inner lens where appropriate.
- Let participants populate lists independently.
- Preserve contributions from quieter participants.
- Merge the raw lists.
- Remove duplicates and repair MECE problems.
- Prioritize with likelihood/impact or other book lenses.
- Have the project manager assign ownership and dates after prioritization.
- Produce one merged, prioritized, executable list of lists.
**Don't:**
- Don't brainstorm aloud from the first minute.
- Don't allow the loudest voice to define the initial option set.
- Don't assign dates before the work set and priorities are coherent.
- Don't leave the merged result without an execution owner.
**Process:**
1. Call the meeting and bound scope.
2. Create independent lists of lists.
3. Populate them separately.
4. Merge the raw material.
5. Prioritize.
6. Assign who does what by when.
7. Execute and track.
*Ref: Technology Strategy Patterns.md — “MergeSort Meeting”*
---
### 60. Use the Pattern Map Individually, in Clusters, or Comprehensively
**Principle:** Compose patterns according to dependency and purpose.
**Do:**
- Use Architecture Definition, SWOT, Technology Radar, or APM independently when one artifact answers the need.
- Combine patterns in groups of three or five for medium-scope work.
- Use industry patterns together for an industry recommendation.
- Use Build/Buy/Partner + Use Case Map + Architecture Definition + Due Diligence for a focused technology pursuit.
- Use Stakeholder Alignment + Roadmap + Directional Costing + Tactical Plan for project-oriented preparation.
- Use most or all patterns for a broad organizational Strategy Deck or a major Ask Deck.
- Let size, expense, novelty, risk, and complexity decide depth.
- Spend less time policing developers and more time connecting technology to product, sales, business development, and strategy.
**Don't:**
- Don't use Investment Map in a vacuum.
- Don't use Ghost Deck without a target deck.
- Don't force comprehensive analysis where an individual pattern closes the decision.
- Don't skip foundational analysis when the decision is expensive or hard to reverse.
**Pattern catalog — creation:**
1. MECE.
2. Logic Tree.
3. Hypothesis.
4. PESTEL.
5. Scenario Planning.
6. Futures Funnel.
7. Backcasting.
8. SWOT.
9. Porter's Five Forces.
10. Ansoff Growth Matrix.
11. Stakeholder Alignment.
12. RACI.
13. Life Cycle Stage.
14. Value Chain.
15. Growth-Share Matrix.
16. Core/Innovation Wave.
17. Investment Map.
18. Principles, Practices, Tools.
19. Application Portfolio Management.
**Pattern catalog — approach and communication:**
20. 30-Second Answer.
21. Rented Brain.
22. Ars Rhetorica.
23. Fait Accompli.
24. Dramatic Structure.
25. Deconstruction.
26. Scalable Business Machines.
**Pattern catalog — templates:**
27. One-Slider.
28. Use Case Map.
29. Directional Costing.
30. Priority Map.
31. Technology Radar.
32. Build/Buy/Partner.
33. Due Diligence.
34. Architecture Definition.
**Pattern catalog — decks and execution:**
35. Ghost Deck.
36. Ask Deck.
37. Strategy Deck.
38. Roadmap.
39. Tactical Plan.
*Ref: Technology Strategy Patterns.md — “Patterns Map”; “Conclusion”*
---
## Anti-Patterns & Common Mistakes
- **Shopping List of Shiny Objects:** Select fashionable technologies without a business problem. → *Fix:* Start with context, options, business value, and trade-offs.
- **Solution Looking for a Problem:** Lead with a tool and invent urgency. → *Fix:* Build the Diagnostic Logic Tree and test whether doing nothing causes a material outcome.
- **Wiki Warning:** Publish correct advice without persuasion, funding, or execution. → *Fix:* Use stakeholder alignment, decks, roadmap, and tactical ownership.
- **Pattern Maximalism:** Apply all 39 patterns to a small decision. → *Fix:* Scale pattern use to expense, novelty, risk, and complexity.
- **Pattern Minimalism:** Make a major irreversible decision with one preferred option. → *Fix:* Use full context, options, evaluation, and communication work.
- **Non-MECE Taxonomy:** Mix levels, omit categories, or overlap items. → *Fix:* Define the category, audience, action, and abstraction level.
- **Executive Detail Dump:** Preserve analyst-level detail in the main narrative. → *Fix:* Use three or five headline points and put long math in the appendix.
- **Cold-Audience Reveal:** Surprise key stakeholders at the decision meeting. → *Fix:* Hold individual meetings first and incorporate feedback.
- **Platitude Strategy:** State values no informed person could oppose. → *Fix:* Make falsifiable choices with opportunity cost.
- **False Precision:** Use exact estimates or probabilities without supporting knowledge. → *Fix:* Use ranges, confidence stages, and assumptions.
- **Status-Quo Forecast:** Assume the future resembles the past. → *Fix:* Run Scenario Planning, Futures Funnel, and Backcasting.
- **Preferred-Future Forecast:** Report what leadership wants as what is likely. → *Fix:* Separate probable and preferred futures.
- **Unbounded Language:** Say everyone, always, platform, or customer without a domain. → *Fix:* Define terms and quantifiers.
- **Tautological Insight:** Reword a definition and present it as discovery. → *Fix:* Add evidence, interpretation, and a non-obvious actionable claim.
- **Causal Overreach:** Infer cause from correlation, sequence, or association. → *Fix:* Qualify the relation and investigate multiple vectors.
- **One-Hypothesis Lock-In:** Preserve the first explanation. → *Fix:* Hold competing hypotheses and revise probabilities.
- **Analysis Paralysis:** Wait for all data. → *Fix:* Let the cost of being wrong determine analysis depth.
- **2×2 Automation:** Let a chart make the decision. → *Fix:* Use it as structured input to judgment.
- **Technical-Only PESTEL:** List technology trends while ignoring world conditions. → *Fix:* Research all six categories through the industry's lens.
- **Committee-Washed Strategy:** Consult everyone until no real choice remains. → *Fix:* Consult key stakeholders and preserve decision sharpness.
- **Multiple Accountables:** Assign two or more A owners. → *Fix:* Split the work or choose the owner with greatest control.
- **Stage-Blind Investment:** Use the same posture in growth, maturity, and decline. → *Fix:* Match strategy to revenue trajectory and market position.
- **Fake Cost Savings:** Count reassigned labor as cash removed. → *Fix:* Distinguish cash saving, capacity, quality, and avoided cost.
- **Unknown Revenue Model:** Architecture around the flagship brand only. → *Fix:* Map all revenue, data, partnership, and cross-subsidy relationships.
- **Dog Modernization:** Invest deeply in low-share, low-growth products. → *Fix:* Retire unless another strategic analysis changes the classification.
- **Perpetual Question Mark:** Keep funding low-share products without a path to growth. → *Fix:* Make the invest-or-exit decision.
- **Innovation Without Capacity:** Assign pioneering work to fully loaded maintenance teams. → *Fix:* Create explicit R&D capacity and a different risk posture.
- **Market-Readiness Blindness:** Build because executives are early adopters. → *Fix:* Score broad customer and operational readiness.
- **Tool-First Operating Model:** Standardize products without linking practice and principle. → *Fix:* Build the Principles → Practices → Tools chain.
- **Invented Process-Posture Labels:** Replace the source taxonomy. → *Fix:* Use Start, Continue, Invest, Assess, Revise.
- **Average-of-Probabilities Error:** Average steps that all must succeed. → *Fix:* Multiply independent probabilities.
- **Debt-Only Portfolio:** Modernize the most indebted application regardless of value. → *Fix:* Combine technical risk and business alignment.
- **Gatekeeper Infrastructure:** Use standardization to constrain internal customers. → *Fix:* Provide reliable, economical, enabling infrastructure.
- **Rented-Brain Abdication:** Hire a consultant instead of knowing the business. → *Fix:* Retain accountability and use outside expertise deliberately.
- **Blind Authority:** Copy Amazon, Google, Facebook, a CTO, or a consultant as proof. → *Fix:* Test relevance to local evidence and goals.
- **Blinding with Science:** Use jargon to force assent. → *Fix:* Explain the relationship to the business outcome plainly.
- **Hero Culture:** Reward repeated rescue without removing root causes. → *Fix:* Externalize knowledge, redesign process, and measure outcomes.
- **Deliverable-as-Outcome:** Celebrate architecture documents or project plans as customer value. → *Fix:* Trace deliverables to outputs and outcomes.
- **One-Night Commitment:** Turn a directional estimate into a contract. → *Fix:* Label Rough, Refined, or Realistic and state ranges.
- **Frozen Technology Future:** Publish one permanent target architecture. → *Fix:* Maintain an evolving Technology Radar.
- **Build-by-Default:** Spend scarce engineering capacity on nondifferentiating software. → *Fix:* Apply Build/Buy/Partner and opportunity cost.
- **Buy-Means-Done:** Ignore integration, process adaptation, contract, and control. → *Fix:* Include full acquisition and operating cost.
- **Partnership Without Exit Logic:** Share control indefinitely. → *Fix:* Use partnership as a conscious operating mode or market test.
- **Deal-Led Due Diligence:** Score after the acquisition outcome is socially fixed. → *Fix:* Run technical assessment before price and structure are final.
- **Architecture by Conversation:** Keep NFRs in the architect's head. → *Fix:* Write the Architecture Definition.
- **Architecture Shelfware:** Write the definition but do not translate it into team work. → *Fix:* Use acceptance criteria, stories, and Definition Defense.
- **Commercial Executable-Architecture Fantasy:** Expect one model to generate and stay synchronized with reality. → *Fix:* Use testable requirements and active team conversation.
- **Passive Ghost Headline:** Label slides “Background” or “Plan.” → *Fix:* Make each headline advance a claim.
- **Price Reveal:** Hide the ask until the end. → *Fix:* Put cost and decision on slide one.
- **Roadmap as Task Plan:** Fill an executive slide with detailed work. → *Fix:* Show outcome milestones and dependencies.
- **Dates Before Durations:** Fit estimates to desired calendar dates. → *Fix:* estimate duration first, then schedule.
- **Groupthink Planning:** Brainstorm aloud under dominant voices. → *Fix:* create independent lists before MergeSort.
- **Strategy Without Tactics:** Stop when funding is approved. → *Fix:* hand off a prioritized, owned Tactical Plan.
- **Adjacent-Framework Contamination:** Add real options, Wardley Mapping, or named Gartner stages as Hewitt content. → *Fix:* state source boundaries and use only the book's named models.
---
## Decision Heuristics / Checklists
### Strategy Intake
- [ ] What problem or opportunity must be addressed?
- [ ] Who requested the strategy?
- [ ] What decision must they make?
- [ ] What action must another audience take?
- [ ] What level is in scope: project, department, company, industry, or world?
- [ ] What is the expense?
- [ ] What is the novelty?
- [ ] What is the risk?
- [ ] How reversible is the decision?
- [ ] What is the expected output: recommendation, deck, architecture, roadmap, or ask?
- [ ] What is the deadline relative to strategy and budget season?
### Five-Step Strategic Analysis
- [ ] Establish context.
- [ ] Analyze external trends.
- [ ] Analyze industry, company, department, and stakeholder forces as required.
- [ ] Understand competition, market, and technology landscape.
- [ ] List strategic options.
- [ ] Evaluate options.
- [ ] State the selected recommendation.
- [ ] State rejected options.
- [ ] State opportunity cost.
- [ ] State resource requirements.
- [ ] State execution and governance.
### MECE Audit
- [ ] Is the audience named?
- [ ] Is the reason they care named?
- [ ] Can the list drive a decision or action?
- [ ] Is the category bounded?
- [ ] Are entries mutually exclusive?
- [ ] Are entries collectively exhaustive for that category?
- [ ] Are all entries at one abstraction level?
- [ ] Are subcategories separated from parent categories?
- [ ] Can the executive view be reduced to three or five points?
- [ ] Is deeper analysis preserved outside the main narrative?
### Hypothesis Audit
- [ ] What data points exist?
- [ ] What insight mixes evidence with interpretation?
- [ ] What proposition is being asserted?
- [ ] Can it be true or false?
- [ ] What terms need definition?
- [ ] What domain does it quantify?
- [ ] What competing hypotheses exist?
- [ ] What are the possible outcomes?
- [ ] What is the prior probability?
- [ ] What evidence changes it?
- [ ] Is probability expressed without false precision?
- [ ] What action tests the claim?
- [ ] What is the cost of being wrong?
### World and Future Context
- [ ] Political conditions researched.
- [ ] Economic conditions researched.
- [ ] Social conditions researched.
- [ ] Technological adoption researched.
- [ ] Environmental conditions researched.
- [ ] Legal conditions researched.
- [ ] Industry implications stated.
- [ ] Sources cited.
- [ ] PESTEL validated with business peers.
- [ ] Weak signals identified.
- [ ] Scenarios created by a diverse group.
- [ ] First- and second-order impacts mapped.
- [ ] Possible, plausible, probable, and preferred futures separated.
- [ ] Beautiful Future made concrete.
- [ ] Antecedents backcast to current state.
- [ ] People, process, and technology changes included.
### Five Forces
- [ ] New entrants: switching cost.
- [ ] New entrants: distribution access.
- [ ] New entrants: regulation.
- [ ] New entrants: capital and scale.
- [ ] New entrants: differentiation and loyalty.
- [ ] Substitution: alternate technology for same need.
- [ ] Substitution: availability and price.
- [ ] Substitution: propensity and switching cost.
- [ ] Customers: bargaining leverage.
- [ ] Customers: information and price sensitivity.
- [ ] Suppliers: compute and storage.
- [ ] Suppliers: talent scarcity and differentiation.
- [ ] Rivalry: innovation and competitive strategy.
- [ ] Rivalry: pricing, marketing, concentration, transparency.
- [ ] Technology response stated for every force.
- [ ] Threat tagged red, yellow, or green.
### Stakeholder and RACI
- [ ] CEO or highest relevant leader identified.
- [ ] Technical executive sponsor identified.
- [ ] Funders and champions identified.
- [ ] Executing teams identified.
- [ ] Potential underminers identified.
- [ ] External stakeholders considered.
- [ ] 10–30 key names recorded where scale warrants.
- [ ] Influence scored 1–5.
- [ ] Impact scored 1–5.
- [ ] Monitor plan defined.
- [ ] Maintain-confidence plan defined.
- [ ] Keep-informed plan defined.
- [ ] Collaborate plan defined.
- [ ] Responsible owners assigned.
- [ ] Exactly one Accountable owner per item.
- [ ] Consulted experts can alter work.
- [ ] Informed recipients have no hidden decision right.
### Portfolio and Technical Debt
- [ ] Business goals agreed.
- [ ] Technology goals agreed.
- [ ] Application list agreed.
- [ ] Business owner named.
- [ ] Technical owner named.
- [ ] Total cost of ownership measured.
- [ ] Technical-risk attributes weighted.
- [ ] Business-value attributes weighted.
- [ ] Current and future business alignment scored.
- [ ] Capability map built where useful.
- [ ] Data flows identified.
- [ ] Asset class assigned.
- [ ] Grow/evolve/maintain candidates identified.
- [ ] Tolerate candidates have a cost and exit posture.
- [ ] Retire candidates have consolidation or shutdown plans.
- [ ] Reengineer/modernize/replace candidates have stakeholder decisions.
- [ ] Debt work is tied to time, value, cost, risk, or market outcome.
### Platform and Ecosystem
- [ ] Does the system expose APIs?
- [ ] Can customers build something new?
- [ ] Can they do so without negotiating bespoke work?
- [ ] Is the platform aligned with the current market or a new one?
- [ ] Which products extend the ecosystem?
- [ ] Which partner relationships alter architecture decisions?
- [ ] Which data-producing products support future strategy?
- [ ] Does the team culture support integration?
- [ ] Are platform services cloud-ready where required?
- [ ] Are configuration, statelessness, partitioning, and global deployment addressed?
### Build / Buy / Partner
- [ ] Is the capability a competitive differentiator?
- [ ] Is intellectual-property ownership important?
- [ ] Does the organization have the skill?
- [ ] Does it have the time?
- [ ] Can it complete the product better than the market?
- [ ] What internal opportunity is forgone?
- [ ] What is long-term maintenance cost?
- [ ] What integration cost follows a purchase?
- [ ] What business-process changes follow a purchase?
- [ ] Is acquisition of a company more valuable than licensing software?
- [ ] Is the partner financially healthy?
- [ ] Is the deal strategically important to the partner?
- [ ] Are operating styles compatible?
- [ ] Can both sides execute?
- [ ] Is shared control acceptable?
- [ ] Is the partnership a market test or enduring model?
- [ ] Has Due Diligence been completed?
### Technology Radar
- [ ] Tools quadrant populated.
- [ ] Techniques quadrant populated.
- [ ] Languages & Frameworks quadrant populated.
- [ ] Platforms quadrant populated.
- [ ] Adopt meaning explicit.
- [ ] Trial meaning explicit.
- [ ] Assess meaning explicit.
- [ ] Hold meaning explicit.
- [ ] Evidence for placement recorded.
- [ ] Team feedback channel defined.
- [ ] Update cadence defined.
- [ ] Ring movement reviewed.
- [ ] Radar connected to strategy priorities.
### Architecture Definition
- [ ] System name, author, date, reviewers, contributors.
- [ ] RFC 2119 terms defined.
- [ ] Major features.
- [ ] Strategic fit.
- [ ] Business drivers and priorities.
- [ ] Assumptions.
- [ ] Constraints.
- [ ] Risks.
- [ ] Impacts.
- [ ] Stakeholders.
- [ ] Governance.
- [ ] Standards and conventions.
- [ ] UI and services.
- [ ] Security.
- [ ] Availability.
- [ ] Scalability and performance.
- [ ] Extensibility.
- [ ] Testability.
- [ ] Maintainability.
- [ ] Monitorability and metrics.
- [ ] Data sources and strategy.
- [ ] Transactions and consistency.
- [ ] Volatility and maintenance.
- [ ] Migration and volume.
- [ ] Logging, analytics, and caching.
- [ ] Cloud and data-center requirements.
- [ ] Deployment and disaster recovery.
- [ ] Network design.
- [ ] NFRs translated into acceptance criteria or stories.
- [ ] Definition Defense completed.
- [ ] Feedback incorporated.
### Directional Costing
- [ ] Estimate labeled Rough, Refined, or Realistic.
- [ ] Confidence range stated.
- [ ] Assumptions stated.
- [ ] Contingency included.
- [ ] Development-team labor included.
- [ ] Supporting roles included.
- [ ] Infrastructure or cloud included.
- [ ] Integration included.
- [ ] Testing and deployment included.
- [ ] Serial work identified.
- [ ] Parallel work identified.
- [ ] Showstoppers front-loaded.
- [ ] Capex and opex separated if useful.
- [ ] Estimate template retained for reuse.
### Ask Deck
- [ ] Ghost Deck created first.
- [ ] Headlines alone tell the story.
- [ ] First slide written last.
- [ ] Requested action appears first.
- [ ] Current-state evidence appears first.
- [ ] Milestones listed.
- [ ] Duration listed.
- [ ] Teams listed.
- [ ] Capex and opex listed.
- [ ] End state listed.
- [ ] Status quo consequence is true and quantified.
- [ ] Path forward covers people, process, technology.
- [ ] Explicit yes/no decision requested.
- [ ] Main deck kept concise.
- [ ] Appendix contains long math and evidence.
- [ ] Meetings before the meeting completed.
### Execution and Learning
- [ ] Roadmap starts from the end state.
- [ ] Milestones are outcome-oriented.
- [ ] Dependencies visible.
- [ ] Durations estimated before dates.
- [ ] Independent planning lists collected.
- [ ] Lists merged and made MECE.
- [ ] Work prioritized.
- [ ] Owners and dates assigned.
- [ ] Metrics and source data defined.
- [ ] Templates stored for reuse.
- [ ] Process hotspots tagged Start/Continue/Invest/Assess/Revise.
- [ ] Strategy, culture, and execution reviewed together.
- [ ] Evidence triggers revision without destroying strategic continuity.
---
## Key Takeaways
1. Technology strategy is business strategy expressed through technical capability and resource choices.
2. The architect's durable responsibilities are to contain entropy, specify nonfunctional requirements, and expose trade-offs.
3. Every material trade-off eventually becomes a question of time and money.
4. Strategy balances goals, methods, and means; it is not a goal statement or project list.
5. Strategy, culture, and execution must reinforce one another.
6. The strategy calendar matters because funding follows organizational planning rhythms.
7. Lists are the raw material of strategy; make them MECE and useful to a named audience.
8. Opportunity cost makes rejected alternatives part of the decision, even though the book does not teach formal real-options theory.
9. Diagnose with one Logic Tree and design the path with another.
10. Form hypotheses early, hold several, and revise them as evidence changes.
11. Define terms and domains before treating propositions as shared truths.
12. Use ranges and Bayesian revision instead of false precision.
13. Find signal quickly; do not lose the opportunity while seeking complete data.
14. Treat causation cautiously in complex business systems.
15. Start broad with PESTEL and narrow through industry, company, and department context.
16. Scenario Planning counters the optimism and inertia of the Do-Nothing strategy.
17. Futures Funnel separates possible, plausible, probable, and preferred states.
18. Backcasting turns a concrete future into antecedent work.
19. Five Forces connects technology choices to competitive pressure.
20. Technology talent moves from scarce pioneering skill through accessible commodity toward automation.
21. The source does not present Wardley Mapping or the named Gartner Hype Cycle.
22. Ansoff distinguishes penetration, market development, product development, and diversification.
23. A true platform lets customers build something new through APIs without bespoke negotiation.
24. Stakeholder support must come from funders, executors, and peers.
25. Every RACI work item has exactly one Accountable owner.
26. Company life-cycle stage changes the appropriate technology posture.
27. Value Chain analysis ties technical debt, automation, architecture, and sourcing to economic outcomes.
28. Cost savings are real only when costs actually leave the system.
29. Architecture must reflect the full revenue and partner ecosystem.
30. Growth-Share Matrix, Core/Innovation Wave, Investment Map, and APM provide distinct portfolio lenses.
31. Technical debt is a portfolio dimension, not a standalone priority function.
32. Principles must produce practices; practices must select tools.
33. The source's Process Posture labels are Start, Continue, Invest, Assess, and Revise.
34. Multiply sequential independent process probabilities; do not average them.
35. The 30-Second Answer is answer + three reasons + silence.
36. The Rented-Brain posture means candor without abandoning ownership.
37. Logos, ethos, and pathos work together; fallacies destroy trust.
38. Fait Accompli wins approval through prior inclusion, not surprise.
39. Dramatic Structure organizes truthful evidence around status quo, rupture, plan, and resolution.
40. Deconstruction attacks repeated context, not merely repeated symptoms.
41. Scalable Business Machines distinguish actions, deliverables, outputs, and outcomes.
42. Directional Costing is expectation management supported by ranges, stages, and assumptions.
43. Technology Radar is an evolving communication and feedback mechanism.
44. Build differentiators, buy noncore capability, and partner only with explicit control trade-offs.
45. Due Diligence can assess both acquisition targets and the organization's own products.
46. Architecture Definition makes NFRs clear; team acceptance criteria and review make them executable.
47. Ghost Deck headlines carry the argument before expensive evidence production.
48. Ask Deck puts the decision and cost first.
49. Roadmap communicates outcomes; Tactical Plan assigns executable work.
50. Use patterns individually, in clusters, or comprehensively according to the decision's real stakes.
---
## Cross-References
- Related: [[../Crafting_Engineering_Strategy.md]]
- Related: [[../Building_Evolutionary_Architectures.md]]
- Related: [[../Fundamentals_of_Software_Architecture.md]]
- Related: [[../Software_Architecture_Hardparts.md]]
- Related: [[../Platform_Engineering.md]]
- Related: [[../Team_Topologies.md]]
- Related: [[../Learning_Systems_Thinking.md]]
- Related: [[../Communication_Patterns.md]]
- Topic index: [[../INDEX.md]]
