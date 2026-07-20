# The Value Flywheel Effect

**Author:** David Anderson, with Mark McCann and Michael O'Reilly
**Topic tags:** `#strategy` `#organization` `#leadership` `#devops`
**Language focus:** language-agnostic
**Sources:** `markdown_output/The_Value_Flywheel_Effect_-_David_Anderson/The_Value_Flywheel_Effect_-_David_Anderson.md` · `summaries/The_Value_Flywheel_Effect_-_David_Anderson.md`

---

## TL;DR

*The Value Flywheel Effect* is a sociotechnical framework for aligning business and technology into a self-reinforcing cycle of value creation, demonstrated by Liberty Mutual's serverless transformation (99.98% maintenance-cost reductions, 95%+ runtime savings, 300% deployment increase with 0.5% failure-rate rise). The four phases — Clarity of Purpose, Challenge & Landscape, Next Best Action, and Long-Term Value — repeat continuously, anchored by Wardley Mapping, serverless-first architecture, psychological safety, and the AWS Well-Architected Framework. Apply it when you need to convert a slow, project-focused, IT-as-a-cost-center organization into a product-led, business-aligned, generative enterprise that compounds momentum instead of grinding through one-off initiatives.

---

## Best Practices by Topic

### The Value Flywheel Concept

**Principle:** Transformation happens through accumulated momentum across repeating phases, never in one defining moment.

**Do:**
- Treat transformation as a turning flywheel, not a one-and-done project; each phase feeds the next and the cycle repeats to build compounding momentum.
- Combine Jim Collins' flywheel concept (small wins accumulate), Jeff Bezos' Amazon Virtuous Cycle (lower prices → more customers → more sellers → lower costs), and Simon Sinek's Golden Circle (start with why) into a single organizational operating model.
- Aim for the property of an unbroken cycle: "if you don't have a singular, clear purpose — a guiding light, a north star — the rest is just chaos."
- Use the Value Flywheel as the operating system for change, while mapping (Wardley) supplies the direction and the flywheel supplies the power.

**Don't:**
- Don't treat the flywheel as a hybrid strategy or operational efficiency program; it is "about creating a true bias for action."
- Don't wait for everything in phase two before moving to phase three — momentum and bias for action beat perfection.
- Don't run a single turn of the wheel and stop; "the Value Flywheel is designed to spin many times."

**Code:**
```
Phase 1: Clarity of Purpose  (Persona: CEO)
Phase 2: Challenge & Landscape (Persona: Engineers)
Phase 3: Next Best Action     (Persona: Product Leaders)
Phase 4: Long-Term Value      (Persona: CTO)
   ↑                                        ↓
   └────  return to Phase 1, repeat  ──────┘
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Four Phases of the Value Flywheel"*

---

### Origin Story: Amazon + Collins + Sinek

**Principle:** Borrow proven metaphors from adjacent disciplines and adapt them — never invent your own strategic vocabulary when one already exists.

**Do:**
- Use Bezos' napkin sketch: "Lower prices led to more customer visits. More customers increased the volume of sales and attracted more commission-paying third-party sellers to the site. That allowed Amazon to get more out of fixed costs like the fulfillment centers and the servers needed to run the website. This greater efficiency then enabled it to lower prices further."
- Pair Collins' flywheel with Sinek's "Start With Why" to remind leaders that purpose precedes process precedes product.
- Look for visible, "in the wild" examples of each metaphor when socializing the model with executives who learn from stories.

**Don't:**
- Don't invent new strategic vocabulary when a famous one already travels well.
- Don't isolate the three metaphors; their combination is what produces the Value Flywheel Effect.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Origin of the Value Flywheel Effect"*

---

### Liberty Mutual Origin Story (The "Sensemaking Machine")

**Principle:** A small group of architects using Wardley Mapping can become a sensemaking machine that predicts how cloud technology will evolve and chooses accordingly.

**Do:**
- Carve out a small architect team, give them explicit permission to spend time mapping, and protect their ability to publish predictions internally.
- Ask the hard questions early: "Will we still write thousands of lines of code in this new place? What happens when continuous delivery is in place? How will cloud providers like AWS evolve? What things do we do now that we won't do in the future?"
- Recognize paradigm shifts early — Anderson's team spotted AWS Lambda at launch and pivoted, becoming a "winning poker hand."
- Measure in concrete results: "$50,000 a year to $10 a year" maintenance cost, 95%+ runtime savings, "global roll out in weeks instead of years."

**Don't:**
- Don't treat the cloud as "just another datacenter" — it offers a transformational way of working if you change how you build, not just where you deploy.
- Don't mistake migration for transformation; "migration is not the endpoint."

**Code:**
```
A high-performing, serverless-first team will:
  1. chase a business outcome (KPI)
  2. be secure by design
  3. keep high throughput of work
  4. reliably run a high-stability system
  5. rent/reuse, with build as the final option
  6. continuously optimize the total cost
  7. build event-driven via strong APIs
  8. build solutions that fit in their heads
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Serverless Transformation at Liberty Mutual"*

---

### The Twelve Tenets of the Value Flywheel Effect

**Principle:** Each phase of the flywheel has three anchor tenets, mapped to the persona who would "sleep easy" if the tenets were followed.

**Do:**
- Anchor each phase on a persona: CEO (Phase 1), Engineers (Phase 2), Product Leaders (Phase 3), CTO (Phase 4).
- Use the tenets as a coaching rubric, not a maturity model — they should evolve as your context evolves.
- Pair the tenets with Wardley Maps so they can be visualized, debated, and adapted.

**Don't:**
- Don't assume the listed persona is the sole owner — they are the individual most concerned, not the only stakeholder.
- Don't treat the tenets as eternal; "we are constantly evolving these tenets."

**Code:**
```
Phase 1 (CEO)
  1. Clarity of purpose: a data-informed north star.
  2. Obsess over your time to value: innovation is a lagging metric.
  3. Map the market: can you differentiate in the market?

Phase 2 (Engineers)
  4. Psychological safety: team-first environments always win.
  5. The system is the asset: a sociotechnical systems view.
  6. Map the org for enablement: enable empowered engineers.

Phase 3 (Product Leaders)
  7. Code is a liability: a serverless-first mindset delivers value.
  8. Frictionless developer experience: an easy path to production.
  9. Map your solution: align on how you will serve customers.

Phase 4 (CTO)
 10. A problem-prevention culture: well-architected and engineered systems.
 11. Keep a low carbon footprint: sustainability.
 12. Map the emerging value: next-generation companies can see ahead.
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Key Tenets of the Value Flywheel"*

---

### Code Is a Liability

**Principle:** Every line of code you write is an expense — write less, prefer rent over build, and measure the system, not the lines of code.

**Do:**
- Treat code as a liability: "every line of code that is written is an expense" — engineers are paid well, code must be tested and documented, secured continuously, maintained, and deployed.
- Measure outcomes in systems delivered, not lines written: "the asset is not the code; the asset is the system."
- Use Mark Twain as your mantra: "I didn't have time to write you a short letter, so I wrote you a long one."
- Prefer rent/reuse over build; "the less code you write, the less chance you have to introduce errors and the less you must manage."
- Adopt a serverless-first mindset where the cloud provider absorbs undifferentiated heavy lifting.

**Don't:**
- Don't brag about lines of code; that signals you've created cost, not value.
- Don't assume complexity is a sign of capability; "extraordinary code is elegant and precise."
- Don't reward teams for output volume; reward them for outcome quality.

**Code:**
```
When evaluating build vs rent, ask:
  - Engineers paid well: time × cost per line
  - Code tested + documented: additional cost
  - Code secured continuously: future vulnerability risk
  - Code maintained: libraries change, requirements change
  - Operational cost: deploy, monitor, update, host
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Code Is a Liability"*

---

### The Innovation Theater Trap

**Principle:** Demanding innovation is a sign of a good executive; achieving innovation by capitalizing on the Value Flywheel Effect is the sign of a great executive.

**Do:**
- Become fast, become safe — and you will find innovation: "Amazon isn't an innovation company; it's a high-performing technology organization that repeatedly finds innovative value."
- Tie any innovation effort directly to the organization's clarity of purpose; without that anchor, it's theater.
- Measure leading indicators of innovation (time to value) instead of treating innovation as a vanity metric.

**Don't:**
- Don't create "labs" with fancy offices that rarely impact revenue — they make the people working on the core products "furious and disgruntled."
- Don't let Agile transformation offices obsess over "progress" without actually changing how people get things done.
- Don't confuse "fail fast" with a slogan — it "can't just be rolled out at an all-hands meeting."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Problem with Innovation"*

---

### Rate of Turn (Organizational Maneuverability)

**Principle:** An organization's rate of turn — how fast it can enact change top-down and bottom-up — is the missing indicator between strategy and execution.

**Do:**
- Measure the time from leadership directive to organizational action (top-down rate of turn).
- Measure the time from frontline suggestion to organizational action (bottom-up rate of turn).
- Use the Titanic metaphor as a teaching aid: spotting the iceberg is not enough if the ship's rate of turn cannot avoid it.
- Improve rate of turn with Wardley Maps: "studying these value chains can in many cases highlight areas of inertia, duplication, or opportunity that may be ripe for some strategic gameplay."
- Aim for centralization of strategy, decentralization of execution: "once the high-level strategy is in place, you can let the teams advance at their own pace."

**Don't:**
- Don't let "command and control" be the biggest creator of inertia in your organization.
- Don't tolerate a rate of turn measured in years — that is when you lose to faster competitors.

**Code:**
```
Rate-of-turn improvement example:
  Before:  18 months to roll out countrywide change (duplication problem)
  After:    3 months via central product engine all teams consume
  Mechanism: Wardley Map → spotted duplication → funded platform team
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Rate of Turn"*

---

### Time to Value (End-to-End)

**Principle:** Time to value measures from idea inception to customer feedback, not from epic completion to test-team hand-off.

**Do:**
- Measure "how long it took to see customer feedback from the day the CEO first heard this idea."
- Pair the metric with an event captured at creation (story written, PRFAQ drafted, product spec started) and an event captured at value delivery (customer can access the feature).
- Strive for weeks or months, not years: "a measure in days or weeks is good; a measure in months or years is an issue."
- Track movement through the four phases — slowdowns in the flywheel become visible when time to value grows.

**Don't:**
- Don't confuse delivery speed with value realization: "the challenge for companies now is not delivery; it's value realization."
- Don't celebrate completion of an epic as time-to-value completion.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Time to Value"*

---

### North Star Framework (Amplitude)

**Principle:** Identify a single north star metric, three to five input metrics that influence it, and verify the work in flight actually drives the metric.

**Do:**
- Pick a north star that "is neither a leading nor a lagging metric, it's in the middle" — actionable and important.
- Run a North Star Framework workshop: north star metric → mid/long-term value → input metrics → "the work" check.
- Test the metric against Amplitude's checklist:
  - "It expresses value. We can see why it matters to customers."
  - "It represents vision and strategy."
  - "It's an indicator of success."
  - "It's actionable."
  - "It's understandable."
  - "It's measurable."
  - "It's not a vanity metric."
- Use the framework to expose misalignment — "if you start a mapping session and no one can agree on the purpose, then the only objective of the session is to illustrate the misalignment."

**Don't:**
- Don't accept north stars that are vague sentiment ("be more innovative").
- Don't pick a vanity metric the team can move without moving customer outcomes.

**Code:**
```
North Star Framework workshop sequence:
  1. North star metric   ← single, important, actionable
  2. Mid/long-term value ← strategic test (3-5 years is OK)
  3. Input metrics       ← leading indicators (3-5)
  4. "The work"          ← verify current initiatives drive it
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "North Star Framework"*

---

### Leading vs Lagging Metrics

**Principle:** Most organizations celebrate lagging outcomes and ignore the leading inputs that produced them.

**Do:**
- Surface leading metrics prominently — they are the levers you actually control.
- Use Impact Mapping or Opportunity Solution Trees to find them.
- Track "specific leading metrics that influence the lagging metrics" — too few teams possess this mindset.

**Don't:**
- Don't hide leading metrics as a "best-kept secret."
- Don't organize teams around workflow instead of purpose; a "common trap for many organizations is to organize around workflow and not around purpose."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Leading and Lagging Metrics"*

---

### Impact Mapping (Gojko Adzic)

**Principle:** Connect deliverables → impacts → actors → business goals with sticky notes, not slide decks.

**Do:**
- Treat Impact Mapping as a lightweight, collaborative planning technique: "the very act of a team visualizing their goal, how it can be impacted via the actor, and what software deliverable will drive it rewards the team."
- Run it as ideation + focus + feedback in a single session.
- Keep it informal — stickies on a wall beat slide decks every time.

**Don't:**
- Don't substitute Impact Mapping for engaging stakeholders; "the time is not wasted" only if stakeholders are in the room.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Leading and Lagging Metrics"*

---

### Opportunity Solution Trees (Teresa Torres)

**Principle:** Continuous discovery replaces big-bang planning; identify desired outcomes, recognize opportunities from research, remain open to solutions, experiment to evaluate.

**Do:**
- Frame work as experiments: "by opening the idea of an 'experiment,' we are accepting that nothing is certain."
- Apply Torres' four steps:
  1. Identify the desired outcome (a single metric).
  2. Recognize opportunities from generative research.
  3. Be open to solutions from everywhere — they must directly link to an opportunity.
  4. Experiment to evaluate and evolve solutions.

**Don't:**
- Don't let solutions crowd the tree without an opportunity parent; "otherwise, it's just a distraction."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Leading and Lagging Metrics"*

---

### The Double Diamond (British Design Council)

**Principle:** Create space to explore the problem before jumping to solutions; diverge then converge, twice.

**Do:**
- Apply the four phases: Discover (diverge), Define (converge), Develop (diverge), Deliver (converge).
- Slow down the desire to build something quickly — Impact Mapping, Opportunity Solution Trees, and North Star Framework all share this property.

**Don't:**
- Don't let Sales/Engineering/Management (delivery-focused roles) skip the discovery diamond; product and design need room to think.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Leading and Lagging Metrics"*

---

### Amazon Working Backwards (PRFAQ)

**Principle:** Write the press release for the new product first, starting with the customer need, and work backwards to the solution.

**Do:**
- Start with the customer: "Instead of proposing a new product by a slide deck or a pitch, Amazon writes the press release for the new product first, including precise details like the release date, accurate stats, and any FAQs."
- Reject weasel words — Amazon's culture polices them.
- Read the press release in silence in review meetings: "the press release is not presented. The written word should be able to communicate everything that is required."
- Plan to publish the same PR you wrote at inception: "the press release for the first Amazon Kindle in 2007 used this process."

**Don't:**
- Don't allow PowerPoint pitches to substitute for narrative depth.
- Don't over-engineer the FAQ or change the press release significantly during delivery.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Working Backwards"*

---

### Single-Threaded Leadership & Two-Pizza Teams

**Principle:** Give one leader one product with a clear single goal; size teams so two pizzas can feed them.

**Do:**
- Assign "a single leader ... responsible for a product" — single-threaded leadership creates accountability and focus.
- Use Amazon's two-pizza team heuristic (ideally 4–7 people).
- Pair single-threaded leadership with a clear, single goal — "it's all very well having a north star, but if your leader has three different priorities or products, you have an immediate problem."

**Don't:**
- Don't overload leaders with multiple products.
- Don't grow teams past the point where pizza stops being a viable metaphor.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Single-Threaded Leadership"*

---

### Jobs to Be Done (Clayton Christensen)

**Principle:** Customers hire products to do a job; understand the job, not the feature.

**Do:**
- Anchor on the job, not the product: "What is the customer need when someone goes into a hardware store to buy a quarter-inch drill? The answer is not a quarter-inch drill bit. What the customer needs is a quarter-inch hole."
- Look for functional, social, and emotional dimensions of the job (the "Milkshake Dilemma" example).
- Use Christensen's framing to break engineers out of the "builder" persona: "people are either aware of this approach or not."

**Don't:**
- Don't let engineering bias pull the team back into feature-thinking before customer jobs are understood.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Start with the Customer Need"*

---

### Mapping the Market (Phase 1 Anchor)

**Principle:** Use a high-level Wardley Map to identify gaps in the market your business can fill, and make your north star real.

**Do:**
- Capture climatic patterns in a bulleted list beside the map: "What about the change in the stock market? What about Amazon? What about 5G?"
- Resist the urge to predict *when* something will move — "the fact that it will move eventually is enough to drive the 'what if' discussion."
- Capture observations at the end of the session — annotate them numerically off to the side.
- Recognize that the market map is a 30,000-foot view: "it will indicate an approach and possible hazards."

**Don't:**
- Don't try to debate how fast a component will move; debate whether it will move.
- Don't dive into implementation in this session — save that for Phase 3.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Map the Market Competition"*

---

### Wardley Map Anatomy (Axes, Components, Anchor)

**Principle:** A Wardley Map is a value chain plotted on visibility (y-axis) and evolution (x-axis), anchored on a user.

**Do:**
- Put the user/persona at the top — that is the anchor and forms the top of the value chain.
- Treat the y-axis as visibility: the higher the component, the more the user can see it.
- Use dependencies between components (lines or arrows), not call relationships.
- Treat components as capabilities: "think about what the thing does, not what it is (e.g., disposes garbage, not sanitary worker)."

**Don't:**
- Don't try to recreate an architectural diagram on a map — "relationships in maps are dependencies, not calls."
- Don't put more than 20 elements on a beginner map; 30 for intermediates, 50 for experts.
- Don't leave the user as a token stick figure; describe them almost like a user persona.

**Code:**
```
y-axis: visibility to user (web page high, database low)
x-axis: evolution (left=rare/novel → right=mature/commodity)
top:    anchor (the user)
flow:   user → needs → dependencies (lines or arrows)
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Anatomy of a Map"*

---

### The Four Evolutionary Stages

**Principle:** Every component sits somewhere on a four-stage evolution axis; labels can change, but the progression should not.

**Do:**
- Use the standard labels: **Genesis** (rare, poorly understood, potential competitive advantage) → **Custom Built** (market forming, learning focus) → **Product/Rental** (rapid consumption, profitable, refinement) → **Commodity/Utility** (widespread, mature, operational efficiency is king).
- Substitute labels when mapping with non-technical audiences — Anderson often uses Novel, Emerging, Good, Best.
- Use a process of elimination when placing components — "usually, a process of elimination works."

**Don't:**
- Don't mistake the placement as a precise act — "it should feel about right."
- Don't fight the labels; the labels can change, but the progression is the point.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Four Stages of Evolution"*

---

### Movement and Inertia

**Principle:** Movement arrows show future evolution; inertia blocks show what is preventing evolution.

**Do:**
- Add rightward arrows to show components moving toward Commodity.
- Use vertical black lines/boxes to depict inertia blocks.
- Capture the reason for inertia directly on the map (regulation, culture, cost, immature technology, leadership empire-building).
- Remember that "when something moves to Commodity, it can enable a new component in the Genesis space."

**Don't:**
- Don't ignore inertia because it is uncomfortable — "it's important to know what they are ahead of time."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Movement and Inertia"*

---

### Pioneers, Settlers, Town Planners (PST)

**Principle:** Three organizational archetypes are equally important; mismatches between archetype and work are a source of pain.

**Do:**
- Use the PST lens to label components or products:
  - **Pioneers:** "love uncertainty and thrive in building the new. ... likely to create 'the first-ever X.'"
  - **Settlers:** "can scale; they will refine, harden, and understand the concept. ... likely to create 'that fantastic product.'"
  - **Town planners:** "build well-defined things well. ... likely to make things that are fast, cheap, and failure-proof."
- Combine the PST overlay with the team overlay to detect mismatches: "you might find that a pioneering team is working on a commodity, or a town planner team is working on a custom build."

**Don't:**
- Don't rank the three archetypes — "all three groups are equally important, skilled, and critical."
- Don't try to make a single team fill all three roles simultaneously.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Team and Pioneer/Settler/Town Planner (PST) Overlay"*

---

### The Wardley Mapping Canvas (Ben Mosior)

**Principle:** Six steps take you from purpose to map: Purpose → Scope → Users → User Needs → Value Chain → Map.

**Do:**
- Walk through each step in order, even if you can skip ahead intuitively.
- For Purpose, capture "a sentence (avoid jargon) about what your goal is."
- For Scope, narrow up front: "We'll focus on the consumer within electric automobiles, only cars (not vans or bikes) and not infrastructure or support services."
- For Users, "decide on one user type to start with."
- For User Needs, "describe the needs as a capability."
- For Value Chain, "keep it very simple ... three to six components."
- For Map, "start by putting the whole chain in the Product phase" and adjust left/right via discussion.

**Don't:**
- Don't try to map the world; narrow scope ruthlessly up front.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Getting Started"*

---

### Mapping with the CEO

**Principle:** When mapping with executives, drop technical syntax and use non-technical labels; let the conversation drive the map.

**Do:**
- Use a PowerPoint slide (not a dry-erase board) if the CEO is unfamiliar with mapping.
- Replace Genesis/Custom Built/Product/Commodity with **Novel, Emerging, Good, Best** for non-technical audiences.
- Stick to a single value chain.
- "Let the conversation dictate the pace. Don't be afraid to pause and be comfortable in the silent contemplation of the room."
- Provoke by moving a component on the map: "audience participation is always a good icebreaker."

**Don't:**
- Don't go in with a primer; keep the introduction invisible.
- Don't send a heavy preread — describe a basic value chain and a simple evolutionary axis.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping with the CEO"*

---

### Mapping with Technical Experts

**Principle:** Give experts time to create value chains first; the x-axis placement is harder and benefits from facilitation.

**Do:**
- Use an online whiteboard for cocreation.
- Send a preread (a basic Wardley Map explaining the shape) and acknowledge that "even very technical individuals will struggle with Wardley Mapping."
- "Starting with value chains always results in a fruitful conversation."
- Allocate 60–90 minutes per session; consider splitting into two or three sessions.

**Don't:**
- Don't lead with evolution/positioning — let value chains come first.
- Don't assume the preread has been read — capture climatic patterns from the team instead.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping with the Experts"*

---

### The Three Styles of Maps

**Principle:** Match map scope to the question being asked — stack, organization, or market.

**Do:**
- Use **Mapping the Stack** within a software team to predict movement and inertia in a tech stack.
- Use **Mapping the Organization** after the stack, to assess if teams have the right structure or capability for the work.
- Use **Mapping the Market** at the highest level to make sense of disruption and competitive landscape.

**Don't:**
- Don't use market mapping for tactical tech-stack decisions.
- Don't use stack mapping when you need to make sense of competitive disruption.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Three Styles of Maps"*

---

### Mapping the Stack (Low-level)

**Principle:** A stack map shows the technology stack within a team, identifies components, team alignment, differentiators, and inertia points.

**Do:**
- Start from the customer (user) and draw the value chain of UX from front end through APIs to downstream systems.
- Look for the "big ball of mud" pattern — "everything depends on everything else, and everyone is doing everything."
- Add inertia points to expose system constraints: "We can't replace X because it depends on Y."
- Ask the team the right questions after mapping:
  - "What are the key components of the tech stack?"
  - "Are the teams correctly aligned?"
  - "Which components are differentiators to our business?"
  - "What do we need to move to evolve the architecture?"
  - "What are the inertia points?"

**Don't:**
- Don't map a "big ball of mud" as fungible — "fungibility only works when everything is a commodity; it's a disaster when there are complicated or complex systems."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping the Stack"*

---

### Mapping the Organization (Medium-level)

**Principle:** Map how teams are organized around a product or event to assess capabilities and answer "Are we working on the right thing?"

**Do:**
- Use this map to ask: "Is it worth training a software architect in marketing, communications, and PR, or is it more efficient to hire an expert?"
- Use it to make continuous scales explicit (e.g., speaker quality is a pipeline, not a single point).
- Use it to identify where capabilities need to be hired vs. developed.

**Don't:**
- Don't try to make every team member an expert in every adjacent discipline.
- Don't map scope you cannot influence.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping the Organization"*

---

### Mapping the Market (High-level)

**Principle:** The highest-level map answers questions about disruption, inertia, and emerging trends.

**Do:**
- Use pipelines to predict how components will evolve, drawing examples from other industries.
- Ask "what if" questions: "What happens when banking is embedded in a watch? What about identity, security, and user experience? What else can we do? Payments, approvals, notifications?"
- Keep scope focused on user needs, not your company.

**Don't:**
- Don't "boil the ocean" — the first question must focus on the customer, not the company.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping the Market"*

---

### The Wardley Mapping Grid (A1–D4)

**Principle:** A 4×4 Battleship-style grid makes mapping accessible to engineers who resist the full technique.

**Do:**
- Mark Genesis as A, Custom Built as B, Product/Rental as C, Commodity/Utility as D.
- Mark visibility as 1 (Visible), 2 (Aware), 3 (Unaware), 4 (Invisible).
- Use engineering-friendly framings: "the logging system is in D4: the user neither sees it nor cares about it, and it's totally a commodity. Please tell me we didn't build this ourselves."
- Describe moves in grid coordinates: "We need to refactor those rules, which will move the component from B3 to C3; then we can upgrade it, which will be cheaper to run."

**Don't:**
- Don't make the grid formal; "it works best when it's not too formal, drawn roughly on a board with sticky notes."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Wardley Mapping Grid"*

---

### Mapping Antipatterns

**Principle:** Mapping is fragile; eight common antipatterns corrupt the output and erode trust in the technique.

**Do:**
- Avoid gaming the system — "Don't preempt or influence what the map will look like."
- Co-create, don't present — "if you bring a map into a team, then it's your map — not the team's map."
- Simplify ruthlessly — experts max at 50, intermediates 30, beginners 15.
- Start with the conversation and observations, not the map — "show the map to new people" only after you have a story.

**Don't:**
- Don't recreate an architectural diagram and squeeze it into a map.
- Don't endlessly debate "what is a component?" — "it's an art form, not a science."
- Don't make everything a map; "you'll drive your coworkers crazy!"
- Don't map in a top-down environment without first establishing psychological safety.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Antipatterns of Mapping"*

---

### Team Antipatterns (Dysfunctional Patterns)

**Principle:** Six classic team antipatterns destroy delivery; recognize and remediate them early.

**Do:**
- Watch for these patterns and coach out of them:
  - **The rock star:** "an individual who is bigger than the team."
  - **Tiny team:** "a collection of pairs is just that; it's not a collection of teams."
  - **Huge team:** "once a team grows to over ten people, it's two or three sub-teams."
  - **Bob's team:** "all the people who report to Bob are a team — all six of them. ... A team needs to have team working agreements, interactions, discussions, debates, a common purpose, and togetherness."
  - **My work:** "if a team has a bunch of tasks that individuals own, there will be no shared sense of achievement."
  - **The magic manager:** "every successful delivery is due to the skill of the manager."
  - **Johnny's bonus:** replace individual awards with team incentives.

**Don't:**
- Don't conflate reporting lines with team membership.
- Don't tolerate a single-point-of-failure "magic manager."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Team"*

---

### Team Topologies (Matthew Skelton & Manuel Pais)

**Principle:** Four team types and three interaction patterns create the adaptive organizational design for fast flow.

**Do:**
- Identify your team's type — self-identify by answering honestly:
  - **Stream-aligned team:** "focused on a single flow of work from (usually) a segment of the business domain."
  - **Enabling team:** "helps a stream-aligned team overcome obstacles and shore up missing or lacking capabilities."
  - **Complicated-subsystem team:** "a team of specialists with significant mathematics/calculation/technical expertise."
  - **Platform team:** "a grouping of other team types that provide a compelling internal product to accelerate stream-aligned teams."
- Coach teams to "do one thing and do it well."

**Don't:**
- Don't let stream-aligned teams also try to build platforms or help other teams — they will overextend.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Clarifying Team First with Team Topologies"*

---

### Wardley's Doctrine (Behaviors)

**Principle:** Doctrine is a set of universally useful patterns categorized into Communication, Development, Operation, Learning, Leading, and Structure.

**Do:**
- Use the doctrine as a group exercise: "Ask the team to identify all the patterns that the organization practices."
- Recognize that doctrine behaviors are organized by phase — a new team uses Phase I behaviors; a mature team uses them through Phase V.
- Use doctrine phrases as common language: "that's a commodity," "this feels like custom build," "that's an inertia point."

**Don't:**
- Don't treat doctrine as a maturity model — it's a checklist for conversation.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Behaviors Supporting Challenge"*

---

### Westrum Organizational Culture

**Principle:** Three culture types (pathological, bureaucratic, generative) determine whether information flows and learning happens.

**Do:**
- Aim for a generative (performance-oriented) culture: "High cooperation / Messengers trained / Risks are shared / Bridging encouraged / Failure leads to inquiry / Novelty implemented."
- Use the model as an indicator of culture, especially in DevOps and DORA contexts.
- Recognize that "only generative organizations can truly innovate and adapt."

**Don't:**
- Don't tolerate pathological or bureaucratic cultures in teams that need to ship and learn.
- Don't shoot messengers — that's the fastest way to kill information flow.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Learning or Generative Organizations"*

---

### Psychological Safety (Amy Edmondson)

**Principle:** Psychological safety is the belief that one will not be punished for speaking up with ideas, questions, concerns, or mistakes.

**Do:**
- Build the foundational dependencies — slowing down to speed up, leveraging diversity, measuring progress — before expecting psychological safety to emerge.
- Map psychological safety explicitly: "the team member needs trust, clarity of purpose, work environment, and being heard."
- Connect psychological safety to the team's confidence to slow down when they need to — "it's quite rare, in my experience, but it can be powerful."
- Use Wardley Mapping to visualize the dependencies and how mature they are.

**Don't:**
- Don't confuse psychological safety with permissiveness — feedback must still be direct.
- Don't treat "fail fast" as a slogan; require "an adequate number of people" and a clear business objective to make it safe.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping Psychological Safety"*

---

### Shreyas Doshi's Three Levels of Work

**Principle:** Teams fixated on a single level — execution, impact, or optics — create conflict; recognize the levels mismatch.

**Do:**
- Identify which level each person is fixated on:
  - **Execution:** "We execute to keep the manager happy. Not a flawed approach, but a little outdated and traditional."
  - **Impact:** "We create impact for the customer. A very product-centric approach."
  - **Optics:** "Regardless of what happens, we don't look bad. This is self-serving. Unfortunately, it works but doesn't move the company forward."
- State the level mismatch out loud: "If we don't clearly express our bias, there will be conflict and we will challenge the minutia."

**Don't:**
- Don't hide which level you are operating at; make it explicit.
- Don't assume your favorite level is universally correct.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Work Level Mismatches"*

---

### Project to Product Movement (Mik Kersten)

**Principle:** Shift from project thinking (completing tasks) to product thinking (delivering customer value) to define the flow of value in your company.

**Do:**
- Organize around value (the value the end product brings the customer), not function.
- Allow anyone in the organization to challenge the thinking and the value proposition.
- Recognize the shift is hard: "We have one-hundred-year-old product companies ... and five-year-old project companies."

**Don't:**
- Don't let a project manager's plan become unchallengeable — "they are never allowed to challenge the plan itself."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Culture Shift"*

---

### Sociotechnical System (Four Guiding Principles)

**Principle:** Combine people (socio) and technology (technical) into a cohesive whole, ordered as Socio → Technical → Problem Prevention → Time to Value.

**Do:**
- Build **Socio** first: "the people in the system must have a specific mindset that contributes, collaborates, and enables."
- Then align **Technical** to purpose: "the technology approach fits the purpose (north star metric) and enables the company to move quickly."
- Add **Problem Prevention**: "team members anticipate problems in the system's architecture and eradicate them proactively."
- Reach **Time to Value**: "feedback cycles will become shorter, leading to true agility and a low time to value."
- Treat architects as risk-reducers, not diagram-drawers: "their ability to do this requires extensive system building, designing, and hard work — often decades' worth."

**Don't:**
- Don't let technology run wild: "do not let the tech team run wild; technology is the business."
- Don't incentivize problem-solving over problem prevention (the problem-prevention paradox).

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Sociotechnical System"*

---

### Fred Emery's Design Principles (DP1 vs DP2)

**Principle:** DP1 (redundancy of parts) is disastrous for software; DP2 (redundancy of functions) is the only viable structure for creative work.

**Do:**
- Recognize DP1: "people are classified by function, there is coordination and control required to 'do the work,' ... fragmented work, unclear purpose, and a hierarchical, controlling environment."
- Aim for DP2: "we train people with the skills required, and they self-manage to complete a goal. Organized into groups of people (teams), there is negotiation, responsibility, and a sense of purpose."
- Pair DP2 with Daniel Pink's Drive: "autonomy, mastery, and purpose (intrinsic motives), not by 'fear of punishment or the promise of a reward' (extrinsic motivation)."

**Don't:**
- Don't apply DP1 to software creation — "applying a DP1 system to the creation of software is wholly disastrous."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Purpose vs. Function (DP1 and DP2)"*

---

### Cynefin Framework (Dave Snowden)

**Principle:** Decisions live in five domains — Clear, Complicated, Complex, Chaotic, Confused — and require different actions.

**Do:**
- Use Clear → best practice; Complicated → governance and analysis; Complex → "probe, sense, and respond"; Chaotic → act to establish constraints; Confused → break down to a known domain.
- Recognize that "in organizations, people are usually in the Complex domain and the software is only in the Complicated domain, not the other way around."
- Build feedback loops that probe, sense, and respond.

**Don't:**
- Don't apply best-practice recipes to complex problems.
- Don't pretend you are in a domain you are not.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Your Organization Is a System"*

---

### Complex Adaptive Systems (CAS)

**Principle:** Every organization is a complex adaptive system — a collection of semi-autonomous agents producing system-wide patterns.

**Do:**
- Lead through patterns of thought, not control: "creating similar patterns of thought is more important than control, or purpose over function."
- Use Kevin Dooley's definition: "a group of semi-autonomous agents who interact in interdependent ways to produce system-wide patterns, such that those patterns then influence behavior of the agents."

**Don't:**
- Don't fall for the illusion of control over a CAS.
- Don't let history, traditions, and expectations lock the organization into patterns that no longer serve customers.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Your Organization Is a System"*

---

### Mapping Org Capability

**Principle:** Use a different evolutionary axis (Concept → Hypothesis → Theory → Accepted) to map an industry-standard capability to your reality.

**Do:**
- Take a description of the capability from a trusted third party (vendor or standards body).
- Map the components by how much work is needed to introduce them.
- Add supporting components.
- Apply to security (Microsoft SDL), cloud-native development (.NET definition), or any framework you trust.

**Don't:**
- Don't invent your own capability framework when a recognized one exists.
- Don't overcomplicate a new capability map — "don't over complicate things at the start."

**Code:**
```
Evolutionary axis for capability mapping:
  Concept → Hypothesis → Theory → Accepted
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping a Capability"*

---

### Secure Development Mapping (Microsoft SDL)

**Principle:** Map the twelve Microsoft SDL practices to your reality to find the gap between industry standard and your reality.

**Do:**
- Map the twelve practices:
  1. Provide Training
  2. Define Security Requirements
  3. Define Metrics and Compliance Reporting
  4. Perform Threat Modeling
  5. Establish Design Requirements
  6. Define and Use Cryptography Standards
  7. Manage the Security Risk of Using Third-Party Components
  8. Use Approved Tools
  9. Perform Static Analysis Security Testing (SAST)
  10. Perform Dynamic Analysis Security Testing (DAST)
  11. Perform Penetration Testing
  12. Establish a Standard Incident Response Process
- Add an anchor (a senior leader) and order components by how much work is needed to introduce them (e.g., penetration testing off-the-shelf vs. threat modeling requiring training).

**Don't:**
- Don't confuse renting a vendor service with adopting a practice — adoption requires training and experimentation.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Secure Development"*

---

### Cloud-Native Development Mapping (.NET Definition)

**Principle:** Map Microsoft's six cloud-native areas (cloud infrastructure, modern design, microservices, containers, backing services, automation) to find your capability gap.

**Do:**
- Anchor on an engineering leader; order components along the axis based on how much "change of hearts and minds" is needed.
- Use this map to identify dependencies and enabling components.

**Don't:**
- Don't try to map the entire organization in one go; start with one engineering leader's perspective.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Cloud-Native Development"*

---

### Serverless-First Mindset

**Principle:** Serverless is a consequence of focusing on business value; functions, managed services, cost, code, technology, events, architecture, mapping, data, innovation, and even sustainability are not the point.

**Do:**
- Adopt Ben Kehoe's framing: "The point is not functions, managed services, operations, cost, code, or technology. The point is focus — that is the why of serverless."
- Make serverless the default first choice; "if that's not a good fit, then you work backward (i.e., introduce more infrastructure, like containers)."
- Recognize that "the perfect manifestation of DevOps is serverless."
- Treat every non-serverless implementation as a deviation that requires a good reason.

**Don't:**
- Don't adopt serverless because it's a trend; adopt it because it aligns with focus on business value.
- Don't mandate serverless everywhere — "we don't care if your organization chooses to go serverless or not."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Serverless-First Edge"*

---

### Modern Cloud Inertia Points

**Principle:** Three inertia points consistently derail cloud transformations; recognize and address each.

**Do:**
- Combat **Legacy Cloud** by treating "migration is not the endpoint" — measure, then transform, then modernize continuously. "Modernization begins, it never ends, but the value unlocked ... should show a huge return on investment."
- Combat **Lack of Business Alignment** by deconstructing the IT facade: "You must have a single-team mentality to get the most out of your modern cloud."
- Combat **Fear of Vendor Lock-In** by investing in API and service boundaries: "It's easier to migrate a well-designed serverless system than a poorly designed traditional system."

**Don't:**
- Don't believe the sunk cost fallacy about your previous cloud investment; "if it no longer makes sense, then let go of it and modernize."
- Don't create cloud-agnostic abstractions as a hedge: "Ask any company that goes out of business with an agnostic cloud solution — was the extra spend worth it?"

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Modern Cloud Inertia Points"*

---

### Serverless Myths (Engineering/Technical)

**Principle:** Five engineering/technical myths must be debunked before teams can embrace serverless.

**Do:**
- Counter "Serverless has a cold-start problem" with "cold starts are a solved problem."
- Counter "Serverless is impossible to test" with "the system under test lives in the cloud and should be tested in the cloud."
- Counter "You can't see what's happening" with "you must also use an event-driven monitoring system, not an execution monitoring system."
- Treat engineering experience as a spectrum — "two of the most challenging situations in software are a very experienced engineer with a legacy skill set and a very inexperienced engineer with a modern skill set. You need both the scars and the curious mind."

**Don't:**
- Don't let outdated beliefs about Lambda's early days block modern adoption.
- Don't run serverless locally as a substitute for testing in the cloud.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Engineering/Technical Myths"*

---

### Serverless Myths (Architectural)

**Principle:** Three architectural myths distract from the next-best-action decision.

**Do:**
- Counter "Serverless/Kubernetes is not the next big thing" with "taking the hit on simplification and upskill may have a much better return on investment than business as usual."
- Counter cloud-agnostic vendor lock-in fear with a simple analogy: "It's a little like saying, 'I won't drive a car because fuel prices might go up. I'll just walk everywhere.'"
- Counter custom standards with industry standards: "Use industry standards. They are public, hardened, and understood by all. Custom standards need to be created and communicated; teams need to be trained and maintained."

**Don't:**
- Don't write code in a cloud-agnostic manner as a hedge — "there's a very high chance that they will never change cloud providers."
- Don't build custom standards for problems that industry standards have already solved.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Architectural Myths"*

---

### Serverless Myths (Engineering Management)

**Principle:** Five management myths reveal organizational dysfunction masquerading as technical concern.

**Do:**
- Address "serverless is more expensive" with a coherent cloud management strategy.
- Address "engineers won't do what I tell them to" by giving engineers outcomes to create, not classes or functions to write.
- Address "engineers are disconnected from the business" by including them in crucial discussions and metrics.
- Address "we only work on the cool stuff" by ensuring technical leadership drives decisions, not managers or engineers alone.
- Address "Technology X worked like a charm for me" by assessing every project with its own context.

**Don't:**
- Don't let VP-of-engineering bias drive technology choices the engineers don't believe in.
- Don't withhold metrics or context from engineers.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Engineering Management Myths"*

---

### Serverless Myths (Organizational)

**Principle:** Five organizational myths hide structural problems.

**Do:**
- Counter "we are under capacity" with: "Building an empire does not drive business outcomes. If a team is given ownership of the problem and has an adequate number of people, they will find a solution."
- Counter "Security is blocking serverless" by reverting control to the previous process and reimplementing it cloud-native.
- Counter "Our financial model does not support OpEx" by reframing to "the additional revenue that the cloud will generate."
- Counter "We spent two years building X. Was that a waste?" by treating what you learn during the build as more important than the build itself.
- Counter "Consultancy X will engage for twelve weeks and set direction" by owning your strategy and just evaluating externally.

**Don't:**
- Don't tolerate the word "resources" used for people — it's a tell-tale sign of insufficient focus on the work.
- Don't relinquish control of your technology and business strategy.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Organizational Myths"*

---

### DORA Four Key Metrics

**Principle:** Throughput (deployment frequency, lead time) and stability (change fail rate, mean time to resolution) are the four key metrics that distinguish high-performing teams.

**Do:**
- Measure both throughput and stability — "you can be either fast or safe. With software, it's a little different. You can move very quickly with safety."
- Use small, continuous corrections: "with continuous, minor corrections, you will stay on track and keep making progress."
- Couple DORA with Well-Architected and SCORPS for organizational improvement.

**Don't:**
- Don't trade speed for safety — they are not opposites in well-architected systems.
- Don't measure DORA once and forget; track the trend.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "DORA and the Four Key Metrics"*

---

### Engineering Excellence Characteristics

**Principle:** Define engineering excellence as goals or pillars, not as a fixed checklist that becomes redundant.

**Do:**
- Treat software creation as "a never-ending journey of discovery and improvement. The trend is more important than the number. Marginal gains over a long period are an excellent and optimal result."
- Enable, don't control: "engineering excellence is a mechanism to help teams, not control them."
- Set two levels of quality control: within-team (well-defined, technical-lead-driven) and department (probing conversation that highlights gaps or celebrates excellence).
- Celebrate engineering excellence alongside business outcomes.

**Don't:**
- Don't define "excellence" so precisely it becomes redundant with the next technology change.
- Don't let engineering excellence feel like "someone is marking your homework."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Engineering Excellence?"*

---

### Daniel Pink's Drive (Autonomy/Mastery/Purpose)

**Principle:** Once people are compensated fairly, true motivation comes from autonomy, mastery, and purpose — not pay raises.

**Do:**
- Give teams autonomy — "the freedom to build what is needed by the team."
- Support mastery — "the support to develop their skills."
- Anchor on purpose — "the compelling vision or reason why they build what they build."
- Bring engineers to meet the end users to build empathy.

**Don't:**
- Don't confuse pay with motivation; "companies that follow this advice end up paying huge sums of money for teams that build the wrong thing."
- Don't strip autonomy by micromanaging the technical approach.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Motivation and Drive"*

---

### AWS Cloud Development Kit (CDK)

**Principle:** Define cloud resources in familiar programming languages instead of fighting with YAML, and reuse community-tested patterns.

**Do:**
- Use CDK for infrastructure as code — "developers do not manually configure cloud infrastructure."
- Use a delivery pipeline for everything.
- Combine CDK with TypeScript or Python so the IDE catches errors at write time.
- Pull down CDK Patterns from GitHub and execute them to remove friction: "You can have an API with the infrastructure to deploy it within thirty seconds."

**Don't:**
- Don't keep hand-configuring AWS consoles.
- Don't fight with 1,500-line YAML files; switch to CDK.

**Code:**
```
2010:  weeks  — pre-cloud, multiple teams, handoffs
2017:  2 days — CloudFormation YAML, ~98% correct on copy
2022:  1 hour — 14 lines of CDK (TypeScript), correct on copy
```
*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Cloud Development Kit"*

---

### CDK Patterns (Matt Coulter, Liberty Mutual)

**Principle:** Combine an architectural pattern (e.g., from Gregor Hohpe's Enterprise Integration Patterns) with CDK to make the pattern executable in your cloud.

**Do:**
- Treat patterns as higher-order constructs: "They take an architectural pattern ... and implement it using CDK. The pattern is now executable in a language that will work in your cloud environment."
- Lower the barrier to entry: "Why write your own code from scratch when you could use expert written and tested code that was already created for you?"
- Use internal forks of CDK Patterns to encode organizational standards (tagging, security policies, etc.).
- Open source your patterns to build community and accelerate industrial adoption.

**Don't:**
- Don't reimplement what Gregor Hohpe, AWS, and the community have already battle-tested.
- Don't keep CDK Patterns locked inside one team — share them.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Cloud Development Kit"*

---

### Single Path to Production (Liberty Mutual)

**Principle:** One deployment pipeline with consistent controls enables teams to ship quickly while preserving governance.

**Do:**
- Establish a single path to production early: "There was control and it required partnership, as newer services needed to be added quickly."
- Require infrastructure as code from day one.
- Use CDK/CDK Patterns to lower the barrier of entry.
- Treat guardrails as buffers, not blockers: "you can go as fast or slow as you like, but stay on the freeway!"

**Don't:**
- Don't let every team build its own pipeline.
- Don't require manual configuration steps in the path.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Case Study — Liberty Mutual Insurance"*

---

### The Knowledge Value Chain (Developer Experience Map)

**Principle:** A developer's experience is a value chain: developer → knowledge → code → systems → business value.

**Do:**
- Map the developer experience to expose constraints and unblock the business goal.
- Treat knowledge as a pull-through capability: "knowledge value chain must contain a self-serve solution, and there needs to be a good team around the engineer to create a safe space to innovate."
- Convert market constraints (security, financial audit) into enabling constraints (infrastructure as code, no console access).
- Establish fast feedback loops via DORA scores and observability.
- Enable alignment with the larger strategy: "knowing that the business goal they're working toward and the tech choices and standards they adhere to align with the overall org/division/team strategies."

**Don't:**
- Don't leave the engineer "flying blind" with no observability data.
- Don't let silos hide the engineer's work from peers.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Map"*

---

### AWS Well-Architected Framework (Six Pillars)

**Principle:** An industry-standard framework provides a consistent approach to evaluating architectures; use it instead of inventing your own standards.

**Do:**
- Apply the six pillars:
  1. Operational Excellence
  2. Security
  3. Reliability
  4. Performance Efficiency
  5. Cost Optimization
  6. Sustainability
- Recognize portability: "if a developer moves from one team to another, or indeed from one supporting organization to another separate organization, their experience and expectations remain consistent."
- Treat the framework as continuous improvement, not a one-off audit.
- Meet teams where they are (experience and capability-wise) and bring them together in the spirit of learning.

**Don't:**
- Don't invent custom architecture standards; "Custom standards need to be created and communicated; teams need to be trained and maintained. It's rarely worth the extra effort."
- Don't apply all standards equally to every workload.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "What Is the AWS Well-Architected Framework?"*

---

### The SCORPS Process

**Principle:** A lightweight, two-cadence review (quarterly well-architected review + biweekly SCORPS dashboard review) creates problem prevention without bureaucracy.

**Do:**
- Run two cadences:
  - **Quarterly:** Well-architected review with a solutions architect (likely external to the team).
  - **Biweekly:** SCORPS team dashboard review (Security, Cost, OpEx, Reliability, Performance + Sustainability).
- Keep sessions short: "around one and a half to two hours (ideally about ten to fifteen minutes per team)."
- Focus on deltas from the previous report, cross-team collaboration, and celebrating small wins.
- Put an experienced facilitator (architect, senior principal, engineering director) in charge — they must be able to influence prioritization.
- Use a wiki page or dashboard; "don't wait for automation. ... this will encourage automation."

**Don't:**
- Don't turn SCORPS into a once-a-year audit.
- Don't let senior management turn the session into a stadium event.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "What Is the SCORPS Process?"*

---

### Problem-Prevention Culture

**Principle:** Reward engineers who prevent problems; don't reward only the heroes who fix them.

**Do:**
- Recognize the problem-prevention paradox: "many companies incentivize solving problems over problem prevention ... thus, they are incentivizing the creation of the problem in the first place."
- Use postmortems and premortems to recognize systems appropriately: "Why don't we give equal merit to the steady heads who check and triple check limits? Those who audit and test the system? The engineers who prevent problems from happening?"
- Adopt pre- and postmortems: "Adopting pre- and postmortems for engineering problems will create an environment of psychological safety, challenge, and learning."
- Celebrate quiet success.

**Don't:**
- Don't create an "Oracle" who is the only one who knows the system — "Allow all to be informed and invested."
- Don't praise the fixers of problems; praise the prevention of problems.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Problem-Prevention Culture"*

---

### Innovate/Leverage/Commoditize (ILC) Cycle

**Principle:** Any growth story starts with innovation; leverage what works, then commoditize to create space for the next wave.

**Do:**
- Recognize the three stages: Innovate → Leverage → Commoditize → Innovate again.
- Study Amazon's books example: "online ordering → marketplace → Kindle → Audible."
- Counter "second season syndrome" — "When a team moves up a division, they can survive the first season, but are often relegated and drop back down again in the second season."
- Use Wardley Mapping to spot the right moment to commoditize.

**Don't:**
- Don't sit on your laurels after one success.
- Don't confuse leverage with stagnation — leverage must enable commoditization.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Innovate Using ILC Cycle"*

---

### Domain-Driven Design and Outside-In Discovery

**Principle:** Use DDD and outside-in discovery to align software structure with the problem domain, enabling future offloading.

**Do:**
- Adopt DDD's bounded contexts: "a subsection of a business domain that has clear boundaries."
- Use outside-in discovery (Nick Tune's approach): "starts with the business model, the user needs, and step-by-step zooms into the inner-workings of domains."
- Build capability that supports the primary goal while keeping "the option to offload that capability in the future."

**Don't:**
- Don't create a structure and force every opportunity into it: "you'll end up one of two ways: either you miss the opportunity, or you must reorganize on the fly."
- Don't let domains sprawl into a "mess of dependencies and inefficiencies."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Business Domain Discovery"*

---

### Observability and Dashboards

**Principle:** Combine business, operational, and application metrics into a single view; avoid dashboard overload.

**Do:**
- Build high-level and low-level dashboards: "If there is a dashboard for customer experience/system availability/service performance, everyone looks at the same dashboard."
- Co-create dashboards with business stakeholders.
- Evolve KPIs as the system evolves: "A metric is not a directive; it's a signal that requires investigation."
- Use leading metrics (like Amazon Prime subscribers) that predict lagging outcomes.

**Don't:**
- Don't build competing dashboards per department.
- Don't capture data without a plan for action.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Observability & Metrics"*

---

### Reactive vs Proactive Thinking (The Big Tenet Table)

**Principle:** Convert each Value Flywheel tenet from reactive to proactive thinking; awareness of the contrast is the first step to evolving.

**Do:**
- Phase 1, Clarity of purpose: reactive "Each department has its own metrics" → proactive "Agree on the right KPIs ahead of time for the organization as a whole."
- Phase 1, Time to value: reactive "If we can deliver all our features by the end of the quarter, it will be great" → proactive "Promote effective execution."
- Phase 1, Map the market: reactive "We need to build this because our competitor just announced it" → proactive "Team spots a market opportunity and are the first movers."
- Phase 2, Psychological safety: reactive "Hasn't been an issue yet" → proactive "Create a good environment for future work."
- Phase 2, Sociotechnical: reactive "Let's review the headcount and hire more people" → proactive "Let's review our team goals and ensure our strategy aligns."
- Phase 2, Map the org: reactive "The team gut-feels estimates" → proactive "Team uses mapping to find blind spots."
- Phase 3, Serverless-first: reactive "We're within budget" → proactive "Work to lower future operations and cost."
- Phase 3, DevEx: reactive "Developers are always complaining" → proactive "Remove friction and cognitive load that is unseen."
- Phase 3, Map the solution: reactive "We don't measure technical debt" → proactive "Plan ahead to avoid unnecessary work."
- Phase 4, Problem-prevention: reactive "We don't have time for gold-plating" → proactive "Celebrate by testing with chaos."
- Phase 4, Sustainability: reactive "One person knows the whole thing" → proactive "Allow all to be informed and invested."
- Phase 4, Emerging value: reactive "We are awash with vanity metrics" → proactive "Ensure that gut feel and emotion don't drive the business."

**Don't:**
- Don't accept reactive statements as "normal."
- Don't let a culture of "we'll fix it later" hide a culture of blind spots.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Key Tenets of Value Flywheel Effect: Reactive vs. Proactive Thinking"*

---

### Sustainability in Software (Carbon as a Leading Metric)

**Principle:** Carbon usage is becoming a leading metric for cloud efficiency; design systems with sustainability in mind.

**Do:**
- Recognize that cloud providers "are starting to measure how much carbon their datacenters produce."
- Anticipate carbon usage appearing on quarterly earnings calls.
- Treat inefficient software as a sustainability risk: "carbon usage could become a leading metric for modern cloud efficiency."
- Aim for sustainable architectures: "An effective, cost-optimized system design will also result in a more sustainable system."
- Use serverless patterns and off-peak scheduling to reduce carbon burn.

**Don't:**
- Don't ignore sustainability as a future concern — "How would this affect your attempts to recruit the software engineers of the future at graduate fairs?"
- Don't keep inefficient code because it's cheaper than the alternative today.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Sustainability in Software"*

---

### Wardley's Gameplay Patterns

**Principle:** Gameplay patterns are context-specific maneuvers you can apply once your map is drawn; pick the right one for your position.

**Do:**
- Use the categories as a checklist:
  - **User Perception:** Education, Bundling, Creating Artificial Needs, Confusion of Choice, Brand and Marketing, Fear/Uncertainty/Doubt, Artificial competition, Lobbying/counterplay
  - **Accelerators:** Market enablement, Open approaches, Exploiting network effects, Co-operation, Industrial policy
  - **De-accelerators:** Exploiting constraint, IPR, Creating constraint
  - **Dealing with toxicity:** Pig in a poke, Disposal of liability, Sweat and dump, Refactoring
  - **Market:** Differentiation, Pricing policy, Buyer/supplier power, Harvesting, Standards game, Last man standing, Signal distortion, Trading
  - **Defensive:** Threat acquisition, Raising barriers to entry, Procrastination, Defensive regulation, Limitation of competition, Managing inertia
  - **Attacking:** Directed investment, Experimentation, Center of gravity, Undermining barriers to entry, Fool's mate, Press release process, Playing both sides
  - **Ecosystem:** Alliances, Cocreation, Sensing Engines (ILC), Tower and moat, Two-factor markets, Co-opting and intercession, Embrace and extend, Channel conflicts & disintermediation
  - **Competitor:** Ambush, Fragmentation play, Reinforcing competitor inertia, Sapping, Misdirection, Restriction of movement, Talent raid, Circling and Probing
  - **Positional:** Land grab, First mover, Fast follower, Weak signal/horizon
  - **Poison:** Licensing play, Insertion, Designed to fail

**Don't:**
- Don't apply gameplay without understanding your map's position.
- Don't pick poison patterns by accident.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Table 19.1: Wardley's Gameplay Patterns"*

---

### Mapping Emerging Value (Pipelines)

**Principle:** Add pipelines to your maps to show how components evolve over time; pipelines unlock gameplay.

**Do:**
- Use three pipelines to evolve toward modern cloud:
  - **Technology:** IT systems → technology → IaaS → serverless architecture
  - **Mindset:** Project focus → task focus → results focus → product focus
  - **People:** Role focus → input focus → output focus → outcome/mission focus
- Recognize that "when all three pipelines are evolved, the organization achieves 'rapid progress.'"
- Use pipelines to predict gameplay: "Companies that have this sorted can move quickly."

**Don't:**
- Don't treat pipelines as a single component — they show a continuous evolution.
- Don't evolve one pipeline without the others; "all three pipelines are evolved" is the goal.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Mapping the Emerging Value"*

---

### The Two Value Chains (Sustainable Operations & Long-Term Goals)

**Principle:** Map two parallel value chains that anchor any modern cloud organization.

**Do:**
- Build **Sustainable Operations** = situational awareness + adaptation + stability + resilience.
- Build **Long-Term Goals** = generative organization + diversity + ethics + experimentation + psychological safety.
- Recognize their dependency: "they also depend on the company's mindset, focus, and cloud systems."
- Sense-check combinations:
  - "Project mindset + role focus + legacy cloud implies sustainable operations will require more effort and budget."
  - "Product mindset + mission focus + modern cloud implies sustainable operations will be more achievable."

**Don't:**
- Don't optimize one value chain at the expense of the other.
- Don't ignore that both chains depend on the three evolving pipelines.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Analyzing the Map"*

---

### Case Study: A Cloud Guru (Serverless Bootstrap)

**Principle:** Serverless enables a single founder to build a production-grade platform in four weeks with near-zero compute costs.

**Do:**
- Take a four-week build to prove the platform (Sam Kroonenberg): "founder ... famously decided to take four weeks to build a platform — in the cloud, of course."
- Aim for zero compute bill on early customers: "A Cloud Guru had a zero-dollar cloud compute bill for the first 300,000 customers."
- Use Simon Wardley's market map to identify "content" as the differentiator — "architecture or content??" → content.
- Sell product-led to developers (small recurring transactions, individual subscriptions) instead of waiting for enterprise procurement.
- Stand up conferences (ServerlessConf) to engage the community and validate direction.

**Don't:**
- Don't lift-and-shift legacy architecture to the cloud and call it a startup.
- Don't sell to enterprise procurement if your customers are developers.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Case Study — A Cloud Guru"*

---

### Case Study: Workgrid (The Compute Experiment)

**Principle:** Psychological safety enables teams to choose the right architecture through experimentation, not mandate.

**Do:**
- Run a "compute experiment" — give the team space to try EC2 vs Lambda and reach consensus: "After a day of deliberation, the consensus was to go serverless."
- Define initial architecture drivers explicitly: speed, low cost, autonomy, scalability.
- Codify an evolving architecture philosophy: serverless-first, managed services over managed infrastructure, pragmatic architecture, evolving architecture, modular/"Lego™" design, security as everyone's job, cost-aware, industry-aware.
- Aim to "remove as many Lambda instances as possible from their serverless architecture" — what's next is the point.
- Build a multi-tenant SaaS on serverless with IAM-based access control.
- Upskill existing engineers instead of hiring 25 serverless unicorns: "Building high-performing serverless-first teams is a journey."

**Don't:**
- Don't force a serverless decision from the top down; use psychological safety and experimentation.
- Don't conflate "serverless teams" with infrastructure teams; they are "product teams."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Case Study — Workgrid"*

---

### Case Study: Liberty Mutual (Six-Pager, Manifesto, 300% Deployments)

**Principle:** A technology manifesto + six-pager + CDK Patterns + DORA tracking creates a self-reinforcing serverless-first enterprise.

**Do:**
- Publish a six-pager technology manifesto with executive commitment (CIO James McGlennon, "Our Technology Manifesto — Accelerating Our IT Transformation").
- Adopt targets like "75% of technology staff writing code" and "same-day production deployments for new code."
- Use a single path to production with consistent controls.
- Require infrastructure as code from day one (CloudFormation, then CDK).
- Shift left — give teams more responsibility, reduce handoffs.
- Invest in training (coding dojos, open-space events, Lean coffees, internal conferences like Dev Days).
- Celebrate problem prevention through peer validation.
- Track the metric: "In 2020, Liberty Mutual observed a 300% increase in deployments with only a 0.5% increase in failure rate."
- Use design thinking + DDD + serverless-first for complex modernization (Excite program): 200+ integrations, event-based architecture, minimal custom build.
- Offload event support to AWS EventBridge, AppSync, X-Ray.

**Don't:**
- Don't treat modernization as a five-year waterfall — break it into experiments.
- Don't let silos separate teams from the value they create.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Case Study — Liberty Mutual Insurance"*

---

### Case Study: BBC (Production-Ready Serverless at Scale)

**Principle:** Serverless-first at a publicly funded media giant delivers 20-minute release cadence, real-time features, and 50% lower maintenance overhead.

**Do:**
- Apply a "serverless-first" default: "Consider serverless as the default option until you've seen otherwise."
- Use serverless to "remove the overhead of configuring and maintaining VMs."
- Achieve rapid delivery: "the BBC releases an update to its website every twenty minutes on average."
- Upgrade Node.js versions within two weeks of release — "easy to test in parallel with the existing version."
- Adopt the DevOps model with golden paths: "a 'golden path' can be created — a standard way to do everyday tasks so that product teams don't have to reinvent things. ... the 80:20 rule should apply — a common service will work for 80% of projects."
- Build a "Developer Experience" team to own CD pipelines.
- Use infrastructure as code (Terraform, CDK) for every account.
- Acknowledge serverless limits honestly: traffic management with many open connections, specialized video transcoding.
- Build real-time features cheaply: "100% serverless service to count real-time viewers in under two months. It has now been running for four years."
- Cost-justify serverless with total cost of ownership: "The single biggest expense most organizations pay is employees. Even when serverless does cost more, it's probably a better value overall."

**Don't:**
- Don't over-customize for the 20% that doesn't fit the golden path.
- Don't lose control over the producer of the platform; "Serverless means giving up control. The cloud provider ultimately decides what features to offer."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Case Study — BBC"*

---

### Applying Mapping to the Value Flywheel Effect

**Principle:** The ideal map shows the business goal in Genesis while all supporting components are in Commodity.

**Do:**
- Position the business goal to the left (Genesis = unique, valuable) and supporting components to the right (Commodity = cheap, abundant).
- Aim for "a goal that is unique on the market and potentially highly valuable (in Genesis on the map) but can be easily supported through the consumption of products and commodities."
- Use Tesla as the canonical example: "the idea (business goal) was to produce electric vehicles ... was firmly in Genesis. Tesla also recognized that three underlying components would need to evolve ... so it could pull the electric car into Product."
- Apply the same pattern to map your Value Flywheel: ideal = your business goal is Genesis, everything else is Product/Commodity.

**Don't:**
- Don't try to build in Commodity components — that's the highest cost path.
- Don't assume components will remain in their current stage; movement is the point.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Applying the Value Flywheel Effect to Wardley Mapping"*

---

### The Software Engineer's Mindset

**Principle:** Software engineering is about solving problems and creating value, not writing code; remember Margaret Hamilton coined the term.

**Do:**
- Hire "to solve problems and create value for the business."
- Remember: "Code written 'on the job' should be part of a larger value creation effort, not an effort to write X lines of code in X hours."
- Push back when IT managers want code instead of system improvements — "writing code is important, but improving the system is more important."

**Don't:**
- Don't measure engineers by lines of code.
- Don't treat the business and IT as separate entities — "Today, every leader is a technology leader."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Introduction"*

---

### The Fourth Industrial Revolution Frame

**Principle:** In the Fourth Industrial Revolution, every leader is a technology leader; the business/IT split is a fatal flaw.

**Do:**
- Recognize the era: "characterized 'by a fusion of technologies that is blurring the lines between the physical, digital, and biological spheres.'"
- Absorb the World Economic Forum's framing: "the speed of current breakthroughs has no historical precedent … evolving at an exponential rather than a linear pace."
- Move technology and business strategy to "power and drive each other, turning the organization into a sensemaking machine."
- Address the question: "Is technology really driving your business?"

**Don't:**
- Don't treat technology as overhead: "the building is seen as little more than a necessary cost of doing business."
- Don't silo IT from the business.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Value Flywheel Effect Materializes"*

---

### Why Wardley Mapping (vs SWOT, BMC, OKRs, PowerPoint)

**Principle:** Traditional strategy tools are static; Wardley Mapping is dynamic, anchors on user need, and tracks movement.

**Do:**
- Use Wardley Mapping when SWOT fails because SWOT is too easy to game and lacks situational awareness.
- Use it instead of Business Model Canvas for non-SaaS businesses.
- Replace "the strategy deck" with a six-pager or a map.
- Use it when OKRs are vague and don't help you figure out what to do.

**Don't:**
- Don't try to draw a value chain from SWOT alone.
- Don't rely on a PowerPoint slide that takes days to revise when a map can be redrawn in minutes.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Why Do We Need Mapping?"*

---

### Principles of Wardley Mapping (Courage, Collaboration, Empathy, Perspective, Narrative, Focus, Dialogue, Challenge)

**Principle:** Eight principles keep mapping sessions productive; lean on them when facilitation gets hard.

**Do:**
- Lead with **Courage**: "Admit we are unsure of what to do next. Embrace the unknown."
- Foster **Collaboration**: "Mapping in the open reduces tension and creates alignment."
- Center on **Empathy**: "Every mapping session starts with the question, 'Who is the user and what do they need?'"
- Set **Perspective**: "Set the scope at the start of the conversation and try to stick to it."
- Find the **Narrative**: "Part of the joy of mapping is that it's difficult to predict what that story will be."
- Maintain **Focus**: "It's very tempting to put everything down as a component. Once you have more than twenty elements, it's gone too big — break it down."
- Prioritize **Dialogue**: "The conversation is more important than the map."
- Invite **Challenge**: "Compare these two statements: 'I think that component should be more to the right,' versus 'I think this slide is incorrect.'"

**Don't:**
- Don't mistake drawing a map for the work — the conversation is the work.
- Don't pre-build a map and present it; cocreate it.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Principles of Wardley Mapping"*

---

### Working in the Complex Domain (Probe, Sense, Respond)

**Principle:** In the Complex domain, probe with safe-to-fail experiments, sense what works, respond by amplifying.

**Do:**
- Treat experimentation as a feedback loop: "Probe, sense, respond."
- Look for weak signals that supply early warnings.
- Build leading metrics you believe will influence lagging metrics.
- Shorten your time to value — it's the fourth principle of a sociotechnical system.

**Don't:**
- Don't apply best practice recipes to complex problems.
- Don't wait for certainty before acting — probe first.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "What Are Feedback Loops?"*

---

### The Frozen 2 Evolutionary Architecture Strategy

**Principle:** Pragmatic architecture accepts that some choices will need to change later — tactical is sometimes best.

**Do:**
- Ask: "Is this the simplest version of what can be built today?"
- Recognize the Frozen 2 reference: "It recognizes that sometimes the group will make choices that they know they'll need to change in the longer term."
- Revisit the architecture every quarter and remove code that no longer fits.

**Don't:**
- Don't over-engineer for hypothetical futures.
- Don't hold onto previous architectural investments when they no longer serve.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Architecture Philosophy"*

---

### The Miner's Canary (Engineering Quality Signal)

**Principle:** Every organization needs a method to surface engineering quality issues without waiting for outages.

**Do:**
- Treat cross-team peer review as clinical peer review in medicine: "The review would be transparent, constructive, and meaningful."
- Pair a direct leader (potentially biased) with a technical expert from a different area for impartial feedback.
- Build a cadence of reviews (weekly or quarterly) where the whole team participates transparently.
- Provide a company engineering standard with metrics in a dashboard.
- Balance formality: not so formal that discussion suffers, not so informal that it becomes optional.

**Don't:**
- Don't rely on the team to police itself alone — they are "too close to the problem and solution."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Sense Checking: The Miner's Canary"*

---

### Achieving Speed and Reliability (Reference Architecture vs. Building Block)

**Principle:** Building blocks (CDK Patterns) beat reference architectures because they are executable and customizable.

**Do:**
- Recognize that "this is more powerful than a reference architecture as it gives you a working component to start with."
- Use "the only quick way to make software engineers go fast is to teach them quickly. Using building blocks ... will help them understand what is happening under the hood."
- Watch for the inertia point: "a culture of command and control. The engineering department is not a factory."
- Treat governance and acceleration as complementary, not combined.

**Don't:**
- Don't settle for static reference architectures that require weeks of interpretation.
- Don't make software engineers "faster" by restricting their choices — "you restrict the creativity in what they can produce and introduce fear, uncertainty, and doubt."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Achieving Speed and Reliability"*

---

### Day Zero of the SCORPS Process

**Principle:** Meet the teams where they are; let lead engineers own the process.

**Do:**
- Establish a working agreement with timeline, safe-space commitment, attendance, sample minutes.
- Use a SCORPS report template structured around the six Well-Architected pillars.
- Don't wait for automation — start with a wiki page.
- Pair the report with role-based outcomes:
  - Teams develop automated dashboards (DataDog, Splunk).
  - Teams improve performance focus on critical workloads.
  - Testing techniques improve through cross-collaboration.
  - Security becomes front and center with threat modeling.
  - Operational excellence investment improves release and support.

**Don't:**
- Don't force a uniform starting point — "meet the teams where they're at."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "SCORPS Process Day Zero"*

---

### The Facilitator's Role in SCORPS

**Principle:** The facilitator's authority, curiosity, and ability to connect teams determine SCORPS success.

**Do:**
- Ask probing questions about trending areas.
- Connect engineers and teams for knowledge sharing: "if one team has a fantastic behavior-driven design technique and another could benefit from it, then the facilitator should suggest that they pair up."
- Constantly evolve the SCORPS process.
- Celebrate successes — "no matter how small. Progress is progress!"

**Don't:**
- Don't let the facilitator become an enforcer; the role is enabling, not policing.
- Don't let the session become negative — "Failures are never negative. They are opportunities to learn."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Role of the Facilitator"*

---

### Architectural Leadership (Gregory Hohpe)

**Principle:** The architect's job is to connect the penthouse (business strategy) with the engine room (technical implementation).

**Do:**
- Take Gregory Hohpe's framing: "Rather than focus on technical implementations alone, they must connect the organization's penthouse, where the business strategy is set, with the technical engine room, where the enabling technologies are implemented."
- Architect for risk reduction through communication, not just diagrams.

**Don't:**
- Don't assume diagrams are obsolete; "even if you have no architects, there is still architecture. The problem is you can't see it."

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Problem Prevention"*

---

### Resilience and Ephemeral Computing

**Principle:** Resilience is the ability to adapt to change; ephemeral computing gives it to you for free.

**Do:**
- Use serverless's ephemeral behavior as a forcing function for resilience: "Services only run when called and then disappear. This makes your services more resilient, because you repeatedly test their ability to start up and shut down."
- Use chaos testing to practice continuous resilience: "the process, unfortunately, makes some stakeholders very nervous! The primary goal is to practice continuous resilience; it's not a once-a-year activity."
- Treat 637-day uptimes as a code smell, not a badge of honor: "It sounds great, but it might not switch on so easily when it eventually switches off."

**Don't:**
- Don't build systems designed to "never fail" — "everything fails all the time."
- Don't let security be an afterthought — "secure by design" is the principle.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Resilience"*

---

### Time to Value as a Quarterly Narrative

**Principle:** Make time to value a dashboard-level metric that the executive narrative tracks.

**Do:**
- Display time to value on a dashboard visible to executives.
- Pair it with stability and outage metrics.
- Be transparent about outages.
- Celebrate problem prevention.

**Don't:**
- Don't let "we'll fix it later" hide poor time to value.
- Don't confuse delivery speed with time to value.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Rubber Stamp the Cultural Changes"*

---

### Approximation and Momentum (Phase 1 Pragmatism)

**Principle:** Move through the flywheel quickly; approximate and iterate, instead of perfecting before moving on.

**Do:**
- "Don't focus only on the technology; it's essential, but your people are more important."
- "Don't be afraid to approximate something and move on. Focus on momentum over perfection."
- Recognize that "progress will be disjointed at first, but keep moving forward. The importance of a quick win cannot be understated."

**Don't:**
- Don't wait for full alignment before starting.
- Don't mistake paralysis for rigor.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Conclusion: Getting Started"*

---

### Gerald Weinberg's Laws (Always a Problem; Law of the Hammer)

**Principle:** Two timeless aphorisms: there is always a problem, and the wrong tool makes everything look like a nail.

**Do:**
- Carry Weinberg's wisdom: "In spite of what your client may tell you, there's always a problem."
- Carry Weinberg's "law of the hammer": "The child that receives a hammer for Christmas will discover that everything needs pounding."
- Use them to break the assumption that you already know the problem and the solution.

**Don't:**
- Don't assume the stated problem is the real problem.
- Don't reach for serverless as your hammer for every nail.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Clarity of Purpose Purpose (Phase 1)"*

---

### Enabling vs. Command and Control

**Principle:** Enable and empower, don't command and control.

**Do:**
- "Look outside the IT department. What challenges are the traditional departments having?"
- "Educate yourself about security and compliance functions. Help remove friction; don't fight against it."
- Coach engineers to solve the right problem: "Many engineers will try and solve everything. Coach them to solve the correct problems."

**Don't:**
- Don't fight against friction — remove it.
- Don't be a threat to other functions.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Collaboration, Not Conflict"*

---

### Diversity, Ethics, and Inclusion (Beyond Tagline)

**Principle:** Diversity is more than a tagline — it produces better outcomes, but only in psychologically safe environments.

**Do:**
- Recognize neurodiversity as a strength: "all human brains are different and have different strengths."
- Embed ethics in system design: "ethics requires deep thought about the systems you are building and how they affect users."
- Use Amy Edmondson's framing to demand candor and trust.

**Don't:**
- Don't add "do no evil" to a list of 43 company principles — "it's not going to work."
- Don't treat diversity hiring as complete without the environment to speak up.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "Diversity"*

---

### Situational Awareness as a Superpower

**Principle:** Good situational awareness is a superpower; use Wardley Mapping to find yours.

**Do:**
- Ask the mapping questions reflexively: "Who is this for? Do they really care about this detail? This thing we are building, how will it evolve, will it get replaced? How can I speed up that replacement? What's stopping that acceleration?"
- Use maps as a mental checklist, not just an artifact.
- Recognize that "Mapping is a superpower. We often joke that you can predict the future with maps. I believe you can, but the maps don't tell you when things will happen."

**Don't:**
- Don't rely on gut feel when a map can be drawn.
- Don't mistake observation for prediction.

*Ref: The_Value_Flywheel_Effect_-_David_Anderson.md — "The Importance of Mapping"*

---

## Anti-Patterns & Common Mistakes

- **One-and-done thinking:** Treating the Value Flywheel as a project instead of a cycle that turns many times → *fix:* Plan the next three turns of the wheel up front; expect to revisit Phase 1 after each turn.
- **Innovation theater:** Building a lab with a fancy office instead of accelerating delivery → *fix:* Make innovation a lagging metric; track leading metrics like time to value.
- **IT as separate from the business:** Treating IT as a cost center → *fix:* Merge strategy, integrate architects into business conversations, adopt Hohpe's penthouse↔engine room framing.
- **Lift-and-shift to "legacy cloud":** Calling a migration a transformation → *fix:* Plan for continuous modernization; "migration is not the endpoint."
- **Cloud-agnostic abstraction as a hedge:** Spending millions to keep switching optional → *fix:* Invest in API and service boundaries; treat provider switching as a future, optional contingency.
- **Custom architecture standards:** Inventing your own when industry standards exist → *fix:* Use the AWS Well-Architected Framework; don't reinvent.
- **Micromanaging engineers with pseudo-waterfall Agile:** Pseudo-waterfall "Agile" with PI planning + WIP limits → *fix:* Set outcomes, not tasks; empower engineers.
- **Big rockstar culture:** Celebrating the hero who lands the plane → *fix:* Celebrate problem prevention; reward the steady heads who audit and test.
- **The Oracle problem:** One person who knows the whole system → *fix:* Spread knowledge; make all teams informed and invested.
- **The Magic Manager:** Manager takes credit for delivery → *fix:* Recognize team performance; replace individual awards with team incentives.
- **Bob's team fallacy:** Reporting lines ≠ team → *fix:* Codify team working agreements, common purpose, and togetherness.
- **YAML hell:** Hand-editing 1,500-line CloudFormation files → *fix:* Adopt CDK and CDK Patterns.
- **The single map as the plan:** Bringing a map into the team meeting instead of co-creating it → *fix:* Cocreate maps in real-time with sticky notes or virtual whiteboards.
- **Mapping the world:** Trying to capture every component → *fix:* Beginners: max 15 components; intermediates: 30; experts: 50.
- **Mapping the architecture diagram:** Squeezing an architecture diagram into a Wardley Map → *fix:* Map value chains and dependencies, not calls.
- **Gaming the system:** Mapping to influence rather than explore → *fix:* Treat the session as discovery, not persuasion.
- **Recreating SWAT for every strategy decision:** Using SWOT when you need movement → *fix:* Use Wardley Mapping for situational awareness that tracks change.
- **Show me the strategy deck:** Believing a slide deck creates alignment → *fix:* Write a six-pager or run a mapping session.
- **Force mapping on people:** Mandating mapping without context → *fix:* Lead with conversation and observations; only show the map when there's a story.
- **Treating Doctrine as a maturity model:** Scoring the organization against doctrine → *fix:* Use doctrine as a discussion prompt.
- **Time to value measured from epic completion:** Counting delivery as value → *fix:* Measure from idea inception to customer feedback.
- **Organizing around workflow:** Teams owning tasks instead of value → *fix:* Adopt project-to-product and Team Topologies stream-aligned teams.
- **Complex decisions treated as Clear:** Applying best practice to novel problems → *fix:* Use Cynefin; recognize Complex and probe-sense-respond.
- **Failure as scapegoating:** Pathological culture that shoots messengers → *fix:* Move toward Westrum generative culture; use blameless postmortems.
- **Hoarding context:** Letting the Oracle be the only one who knows the system → *fix:* Document, share, pair, rotate.
- **Sustainability as a buzzword:** Treating green engineering as marketing → *fix:* Track carbon usage as a leading metric; optimize architectures for sustainability.
- **Ad-hoc Well-Architected reviews:** One-off audits instead of continuous improvement → *fix:* Adopt the SCORPS process; run quarterly reviews plus biweekly dashboards.
- **Forced DevOps hand-offs:** Splitting dev and ops in spite of a "DevOps" label → *fix:* Move to a single-team model with shared golden paths (BBC model).
- **Hero culture:** Celebrating the engineer who fixed the outage → *fix:* Reward the engineer who wrote the postmortem preventing the next one.
- **Big-bang transformation:** Five-year plan driven by consultants → *fix:* Run experiments, ship learning, compound momentum.

---

## Decision Heuristics / Checklists

### Should you start a Value Flywheel turn right now?
- Do you have a single north star metric? (If no → fix that first.)
- Is your environment psychologically safe? (If no → invest in people first.)
- Do you have a serverless-first or equivalent next-best-action? (If no → map the stack to find it.)
- Are you running SCORPS or equivalent problem-prevention reviews? (If no → institute them.)

### Is serverless the right answer for this workload?
- Does it require persistent open connections (traffic management, video transcoding)? → *probably not.*
- Does it require specialized hardware (GPU, custom networking)? → *probably not.*
- Is the workload bursty, event-driven, or variable traffic? → *yes, try serverless first.*
- Are there 80/20 patterns where managed services will suffice? → *yes, offload to vendor.*

### Should you adopt a new framework or build a custom standard?
- Does an industry-recognized framework (AWS Well-Architected, Microsoft SDL, .NET cloud-native) cover it? → *use it.*
- Will your custom standard require ongoing training and maintenance? → *probably not worth it.*
- Will engineers need to relearn standards when they switch teams? → *use the portable industry standard.*

### Is your team ready for Phase 2 (Challenge and Landscape)?
- Do people challenge ideas in a respectful, idea-focused way? → *yes, ready.*
- Are decisions made via command and control? → *no, fix leadership first.*
- Are incidents celebrated as heroism rather than inquiry? → *no, fix culture first.*
- Is there diversity (gender, ethnicity, neurotype, role, background)? → *yes, ready.*

### Is your time to value healthy?
- Idea → customer feedback in days or weeks? → *good.*
- Idea → customer feedback in months? → *warning sign.*
- Idea → customer feedback in years? → *urgent problem; investigate value stream.*

### Should you map with the CEO?
- Is the audience non-technical? → *yes, use Novel/Emerging/Good/Best labels.*
- Is the conversation about org-wide strategy? → *yes, use a PowerPoint slide.*
- Is the conversation about a specific tech stack? → *no, map the stack with engineers.*

### Should you map with technical experts?
- Are you starting from value chains? → *yes, that's the easy part.*
- Are you placing on the evolutionary axis? → *that's the hard part; expect debate.*
- Are you capturing climatic patterns? → *always; capture the team's emotional signals.*

### When to use Impact Mapping vs. Opportunity Solution Trees
- Have you identified the deliverable and need to align it to a goal? → *Impact Mapping.*
- Are you in continuous discovery and want to test solutions? → *Opportunity Solution Trees.*

---

## Key Takeaways

1. **The flywheel is self-reinforcing** — each phase feeds the next; the more turns, the faster it spins.
2. **Situational awareness is a superpower** — Wardley Mapping provides shared language; the conversation matters more than the map.
3. **Serverless is a mindset, not a technology** — "the point is focus" (Ben Kehoe). Offload everything that is not core.
4. **Code is a liability** — write less, prefer rent over build, measure the system.
5. **Sociotechnical alignment is non-negotiable** — technology and business strategy must merge; the IT/business split is a fatal flaw.
6. **Psychological safety enables everything else** — without it, challenge becomes conflict, experimentation dies.
7. **Problem prevention over incident management** — celebrate quiet excellence; use SCORPS for continuous review.
8. **Momentum over perfection** — move through phases quickly; quick wins compound.
9. **Every leader is a technology leader** — in the Fourth Industrial Revolution, no executive can be disconnected from tech strategy.
10. **The Value Flywheel exists in every organization** — the question is whether you will spin it fast or leave it grinding.
11. **Map everything that matters** — market, org, stack. Each level answers different questions.
12. **Doctrine, not maturity models** — Wardley's doctrine is a conversation prompt, not a scorecard.
13. **Watch for PST mismatches** — a town-planner team on a custom build is a pain point waiting to happen.
14. **Avoid legacy cloud technical debt** — migration is the start, modernization is forever.
15. **Make time to value a dashboard-level metric** — weeks is good, years is not.
16. **Architects reduce risk through communication** — Gregory Hohpe's elevator metaphor: penthouse ↔ engine room.
17. **Use industry-standard frameworks** — Well-Architected, SDL, Team Topologies beat custom standards.
18. **Carbon usage is becoming a leading metric** — design for sustainability now, not later.
19. **ILC beats one-hit-wonder** — innovate, leverage, commoditize, repeat.
20. **Don't mistake activity for progress** — "developers are always complaining. It's what they do" is a sign of friction, not a feature.

---

## Cross-References

- Related: [[../Accelerate_(Forsgren,_Humble,_Kim).md]] (DORA metrics)
- Related: [[../Team_Topologies_(Skelton,_Pais).md]] (four team types)
- Related: [[../Domain-Driven_Distilled_(Vernon).md]] (bounded contexts)
- Related: [[../Building_Microservices_2nd_edition.md]] (modern cloud patterns)
- Related: [[../Continuous_Deployment.md]] (deployment pipelines)
- Related: [[../Building_Evolutionary_Architectures_2nd_edition.md]] (evolutionary architecture)
- Related: [[../Crafting_Engineering_Strategy_-_Will_Larson.md]] (engineering strategy)
- Related: [[../How_To_Organise_SW_Dev_Teams.md]] (organizational design)
- Related: [[../Lean_Enterprise.md]] (innovation in large orgs)
- Related: [[../Building_an_Event-Driven_Data_Mesh.md]] (event-driven patterns)
- Related: [[../Enabling_Microservice_Success.md]] (sociotechnical enablement)
- Related: [[../Fundamentals_of_Software_Architecture.md]] (architectural fundamentals)
- Topic index: [[../INDEX.md]]