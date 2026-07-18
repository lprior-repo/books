# Comprehensive Summary: Tidy Together

## A Team Exercise in Empirical Software Design
### by Kent Beck (O'Reilly, First Edition, Early Release 2025)

---

## Overview

*Tidy Together* is the second book in Kent Beck's series on empirical software design, following *Tidy First?*. Where the first book focused on individual programmers making small, self-directed structural improvements to code, this book expands the circle to teams. It addresses the social dynamics, management challenges, and theoretical underpinnings of collaborative software design at scale. The book's central thesis is stated repeatedly and without apology: **software design is an exercise in human relationships**. Any design improvement that poisons team dynamics has failed, regardless of its technical elegance.

The book is organized into three parts: **Refactorings** (concrete techniques for structural change at team scale), **Management** (the human and organizational challenges of design work), and **Theory** (the deeper forces -- power laws, optionality, survival -- that govern software systems). As an Early Release, only certain chapters are available, but the available material presents a coherent and substantial body of thought.

Beck's framing metaphor for the entire book is that **software is grown, not assembled**. This is the "one startling sentence" he identifies as differentiating his advice from most other design guidance. Software is not a bridge or a car; it is an organic system that evolves iteratively in response to its environment. Accepting this metaphor changes everything: you stop trying to get the design "right" up front and start trying to keep it "growable." You invest in the soil -- tests, tooling, team dynamics -- as much as in the code itself.

This summary is based on the Early Release edition, which includes the Preface, Chapters 1-2 of Part I (Refactorings), the Part II introduction and Chapters 3-4 (Management), and the Part III introduction and Chapters 5-6 (Theory). Many chapters listed in the table of contents are marked UNAVAILABLE in this release, including Fields Object, Collection Mutation Methods, Boolean Parameter to Switches, Make It Run/Right/Fast, Mixing Design and Features, Trough of Despair, Emergent Design, and several others. The summary covers all available content comprehensively.

---

## Preface: How This Book Differs from Tidy First?

Beck explains that *Tidy First?* gave programmers techniques they could apply alone in fifteen minutes. The refactorings in *Tidy Together* are different: they require coordination, span multiple classes and modules, affect multiple people's work, and sometimes require explicit negotiation about priorities and tradeoffs.

The economics are also different. When you tidy by yourself, costs and benefits accrue mostly to you. When you tidy together, you ask others to pay costs today for benefits they may not see until later. That requires a different kind of conversation and a different kind of trust.

Beck traces the origin of this series to a twenty-year-old promise to bring Ed Yourdon and Larry Constantine's insights from *Structured Design* (1979) to a modern audience. The principles -- coupling, cohesion, the relationship between structure and cost -- are eternal, but the examples had become dated. After several false starts trying to write one impossibly large book, Beck sliced the problem into three volumes: individual decision-making (*Tidy First?*), team-scale collaborative design (*Tidy Together*), and the relationship between builders and business stakeholders (a planned third book).

Beck's hope for readers is that they experience the deep satisfaction of working on a system that improves over time, with colleagues who trust each other enough to make bold changes, and that they see how attention to design relationships parallels and enables attention to human relationships. He wants readers to understand that we are not just writing code -- we are growing systems that will outlive our involvement with them, systems that will need to adapt to futures we cannot imagine. The choices we make about structure, process, and how we work together shape not just what we build but who we become in the building.

Beck also describes his personal relationship to the material. He notes that the phrase "human relationships" is a scary one for him -- he does not have a natural understanding of people, social settings, or team dynamics. The good news, he says, is that he does not need a natural understanding. There are a few timeless principles that encourage constructive relationships, and when he sticks to those principles he does okay. He promises to describe those principles in the context of software design, acknowledging that Marcus Aurelius probably said it better but did not know how to refactor.

---

## Part I: Refactorings

### Introduction to Part I

Beck begins with concrete techniques before moving to abstract theory, consistent with his working style. He defines the catalog as "steps at the scale of code that spans multiple people on a team." The motto of empirical software design is: **"large changes in small, safe steps."**

An important terminological note: in *Tidy First?*, Beck refused to call his small design moves "refactorings," using the diminutive "tidyings" instead because the word "refactoring" had drifted so far from its original definition and accumulated so much negative emotion. He gives up that fight here. The design changes in this book are refactorings, plain and simple, going back to Bill Opdyke's thesis.

Beck provides a precise definition of a refactoring:
- A change to the **structure** of the system
- Which will (eventually) make changing the **behavior** of the system easier
- But that preserves the observable **behavior** of the system for now

He draws a critical distinction between "refactoring" (the verb -- applying one or more refactorings in sequence) and "a refactoring" (a single, atomic structural change). He frequently hears stories like "We spent all this time refactoring and everything broke." That is not refactoring. If you compose a series of behavior-preserving transformations, the result is behavior-preserving. The challenge is that it can be hard to get from structure A to structure B solely through behavior-preserving transformations -- but that is the discipline Beck advocates.

He admits to occasionally "cheating" and just editing text for a while, but describes this as the exception, not the rule. He encourages readers to stretch themselves and use only the refactorings to get from the current structure to the desired structure.

The refactoring catalog in this book is considerably larger than what is currently available. The table of contents lists planned chapters on Fields Object, Collection Mutation Methods, Boolean Parameter to Switches, Boolean in Constructor to Subclasses, Common Parameter to Constructor Parameter plus Field, Constructor, Function Call to Event, Move, Literal to Constant, Extract/Inline Function, Increase/Decrease Visibility/Scope, Static to Instance, Global and Local State, and Narrow/Widen Parameter. Each of these represents a reversible structural transformation that can be composed with others to accomplish larger design changes. The two available chapters (One Principle, One Technique and Parameters Object) establish the methodological foundation and a representative example that the remaining chapters will follow.

---

### Chapter 1: One Principle, One Technique

This chapter lays the essential groundwork for all the refactorings that follow. Beck identifies two foundational ideas: the **Safety Principle** and the **Parallels Technique**.

#### The Safety Principle

The fundamental principle of empirical software design is: **when there is a tradeoff between safety and efficiency, always choose safety.**

In the early stage of a product, design does not matter as much. It is when a product and the team attending it grow large that better designs become noticeably better. When design improvements become valuable and leveraged, the cost of delay has usually dropped enough that being a little slower will not be dramatically more expensive. Hence the bias toward safety at nearly any cost.

Beck is trying to avoid **infrequent, giant costs** by consistently applying the Safety Principle. The challenge is that someone can always say, "I can do that faster if I skip all those intermediate steps," and they will almost be right. The cleverer and more careful they are, the longer they can preserve the illusion that hopping two-footed from rock to wet, slick, moss-covered rock is the quickest way across the river. And then comes the day when nothing could possibly break, and it does anyway. Programs are unforgiving -- they do not care about the strength of our convictions.

When a purely structural change turns out to have behavioral consequences, the costs pile up in three categories:
1. **Debugging costs** -- finding and fixing the error
2. **Remediation costs** -- repairing any damage caused
3. **Social costs** -- the relationship damage from imposing costs on teammates

Social costs are the most insidious. Nothing strains a relationship like interrupting someone else's perfectly good work because you made a mistake, asking them to sacrifice time, energy, and opportunity to your error. The "extra" steps of the Safety Principle are insurance premiums that ensure the team can keep moving forward together.

Beck's reasoning for the Safety Principle also rests on an economic argument about the distribution of costs. He is trying to avoid infrequent, giant costs -- the kind that derail projects and end careers. These giant costs are not just technical; they are social. A broken build that blocks the entire team creates resentment. A design change that introduces a subtle bug erodes trust. The accumulated weight of these incidents can destroy a team's effectiveness far more thoroughly than any single technical mistake. The Safety Principle, applied consistently, keeps these giant costs from materializing.

#### The Parallels Technique

The Parallels Technique implements the Safety Principle: **the old design and the new design temporarily co-exist.** Add the new before removing the old.

Beck provides a detailed worked example: an API that takes a collection argument where analysis shows the collection only ever has a single element. The goal is to change the API to accept a scalar instead. This requires changing many callers and the API definition. Rather than changing everything at once, the Parallels Technique prescribes a sequence:

1. **Add a new parameter** to the API and all callers, initially with a null value. This is deployable with nearly zero chance of error, especially if an automated tool adds the parameter.
2. **Populate the new parameter with correct values** across all callers. Still deployable, still safe.
3. **Use the new parameter in the implementation** instead of the old one.
4. **Delete the old parameter** from the declaration and all callers, since it is no longer referenced.

Each step is independently deployable (if deployments are cheap enough). Could you do it in one two-footed leap? Probably. But why risk a leap when the social cohesion of the team is at stake? Why risk it when you might be interrupted mid-change by something genuinely more important, and risk throwing away half-completed work? Better to put one foot on the new rock while keeping the other on the old, then gradually shift weight.

What if you simply cannot figure out a way to apply the Parallels Technique? Then you either live without changing the structure or you make the leap. But Beck notes that every time he thought a leap was absolutely necessary, he later reflected and discovered a new twist on the Parallels Technique that would have worked.

He offers bonus homework: at the step where you start passing the correct value in the new parameter, you could instead have started using the new parameter in the implementation. Trying it both ways builds intuition for the technique's flexibility.

The Parallels Technique also supports architectural evolution, a topic Beck plans to address in the third book in the series. The same principle -- old and new co-existing temporarily -- applies at every scale from parameter changes to system-wide architectural migrations. This makes it arguably the single most important technique in the entire book: once you internalize the habit of adding before removing, you have a safe path through nearly any structural transformation.

It is worth noting that the Parallels Technique has implications beyond immediate safety. Because each intermediate step is deployable, the technique supports continuous integration and continuous deployment. You never need to maintain a long-lived branch that drifts farther and farther from main. You never need to coordinate a "big bang" merge. The system works at every step along the way, which means you can ship at every step along the way. This property is invaluable in team environments where multiple people are making changes simultaneously.

---

### Chapter 2: Parameters Object

This is the first concrete refactoring pattern in the catalog.

#### Pattern (When to Apply)

You see **the same set of parameters passed through multiple levels of the call graph**, or you see them passed together in several different places in the codebase.

#### Forward (What to Do)

Group the parameters into a single object. Give the fields of the object the names (and types) of the parameters. **Make the Parameters Object immutable** -- the last thing you want is an aliasing error silently changing system behavior behind your back.

#### Example

Beck walks through converting `foo(width, height)` into `foo(new Point(width, height))` using the Parallels Technique step by step:

1. Create the `Point` class with `x, y` fields.
2. Add a formal parameter and null actual parameters: `foo(width, height, null)` / `function foo(x, y, p)`.
3. Create and pass the equivalent Point: `foo(width, height, new Point(width, height))`.
4. Use the Point in the implementation, replacing `x` with `p.x`.
5. Delete the now-unused `x` parameter.
6. Repeat for `y`, replacing it with `p.y`.
7. Delete `y`, arriving at `foo(new Point(width, height))` / `function foo(p)`.

Beck notes that intermediate states may look funky -- for instance, having both `y` and `p` where `p.y` duplicates `y` -- but the code works fine at every step.

#### Discussion

Several important design points emerge:

- **Allocation at the top**: The Parameters Object must be allocated at the top of the call graph. If this becomes a performance bottleneck, there is plenty of time to fix it later. Make it run, make it right, make it fast.

- **Top-down bias**: Beck prefers introducing the Parameters Object top-down through the call graph -- create it in one place, then use it in more and more places.

- **Symmetry**: Parameters Objects illustrate symmetry. The same cluster of parameters appears symmetrically in several parts of the code. By coalescing them into an object, you communicate that symmetry to readers.

- **Almost-the-same parameter lists**: If parameter lists are almost but not quite the same, just hold off. Almost symmetrical means not symmetrical. There will be time later if the lists become (or you make them) identical. Reordering parameters to make lists match is fine.

#### Coupling and Cohesion

The Parameters Object makes parameter lists more cohesive. If you have `foo(x, y, theta)` and add a parameter, you are adding an element to a list of three. If instead you have `foo(p, theta)` and add a parameter to `p`, a larger percentage of the element changes -- more cohesion.

Parameters Objects can also **decouple changes**. No longer are all functions coupled with respect to changes in the list of related parameters. Change the Parameters Object and where it is allocated, and leave the rest of the functions alone.

Parameters Objects can serve as a **Hinge for change** -- by introducing an object protocol-compatible with the Parameters Object but with a different implementation, you can potentially change system behavior without touching most of the code.

#### Inverse (When to Inline)

If a Parameters Object is only used in one place, has no behavior, and is only passed once -- inline it. Every element in the design carries a cost. If you had something in your backpack you never used, you would take it out. No value, no carry.

Beck warns against a common design error: a parameter list gets long, so someone adds a map at the end called something like "params." This map gradually grows, gets passed deeper and deeper in the call graph, and becomes a source of ugly coupling. Especially when someone decides to mutate the map mid-computation. What values must go in that map? Hard to say. Which are optional? Hard to say. The solution: make the mess obvious. Inline the map. If the parameter list wants to be long, let it be long. If you see clusters of parameters in different orders, reorder them to match, then re-extract a proper Parameters Object with an understandable constructor.

#### Subsequent Refactorings

After extracting a Parameters Object, you may have opportunities to **Move Code to Data** if you have expressions that only use data contained in the Parameters Object.

The Parameters Object refactoring serves as a template for how Beck approaches all the refactorings in this book. Each one is presented with the same structure: Pattern (when to recognize the opportunity), Forward (how to apply it, step by step using the Parallels Technique), Discussion (the deeper design reasoning including coupling and cohesion implications), Inverse (when to apply the reverse transformation), and Subsequent Refactorings (what opportunities the change creates). This structure reflects Beck's empirical philosophy: start with what you can observe, proceed in small safe steps, and let each change reveal the next opportunity.

---

## Part II: Management

### Introduction to Part II

Where *Tidy First?* explored managing tidyings -- small, safe, self-directed design changes -- Part II tackles the more complex challenge of managing refactorings at team scale. These changes take longer (hours, days, sometimes weeks rather than minutes). They touch more code, affecting multiple files, classes, and sometimes systems. Most importantly, **they affect other people**.

When you extract a helper function, you make a decision that mostly impacts your own future self. When you introduce a parameter object passed through six layers of the call stack, you impact everyone who works with that code. When you move from direct function calls to events, you change how the entire team thinks about system interactions.

#### Same Principles, Different Scale

The core principles from *Tidy First?* still apply: work in small, safe steps (just more of them, and slightly larger ones); separate structure changes from behavior changes; prefer reversible decisions.

The Safety Principle becomes even more important. When a tidying goes wrong, you fix it yourself. When a refactoring goes wrong, you have potentially blocked your teammates' work. The social cost of mistakes rises dramatically. Loss of trust compounds the cost of a broken build.

Timing decisions become more complex. "Tidy first?" was a question you could answer in the moment. "Refactor first? Refactor after?" requires coordination, communication, and collective judgment. You must consider: How long will this take? Who will be affected? What features will be delayed? How will we handle the transition period? What if we get interrupted midway?

#### The Collaboration Challenge

Every refactoring decision at this scale touches other people's work, mental models, and deadlines. You must:
- Communicate your intentions clearly
- Build consensus around direction
- Coordinate timing with feature development
- Manage expectations about temporary complexity
- Handle disagreements constructively

This does not mean you need unanimous agreement before making any change. Empirical software design relies not on unanimity but on **coherence** -- while everyone has their own perspective on the design, the team exerts consistent effort to bring those perspectives together.

#### Maintaining Balance

The features-and-options tension becomes more visible at this scale. Spending an hour tidying is easy to justify. Spending a week refactoring makes the opportunity cost visible to everyone -- features not implemented, bugs not fixed, revenue not earned.

But the options value is also more visible. A good refactoring does not just make one feature easier; it makes whole classes of features easier. The parameter object does not just help with the current change; it creates flexibility for future changes not yet imagined.

Your job is to help your team see both sides: the cost of the current design and the value of the improved design. Help them understand this is not about making code "pretty" -- it is about making future work faster, safer, and more predictable.

#### The Rhythm at Scale

In *Tidy First?*, the rhythm was minutes to an hour of structural work, then back to behavioral work. At refactoring scale, the rhythm is different. You might spend days on structural work but still need to maintain balance. You learn to:
- Initiate refactorings gradually
- Sustain progress while delivering features
- Finish cleanly without disrupting the team
- Sometimes abandon changes that are not working out

The key is **never disappearing into a design cave for weeks at a time**. Even large refactorings happen through a series of small, safe steps that keep the system working and the team moving forward together.

Beck also introduces the concept of **coherence** as an alternative to unanimity in team decision-making. While everyone has their own perspective on the design, the team exerts consistent effort to bring those perspectives together. You do not need everyone to agree on the perfect design. You need enough shared understanding that people can make progress without constantly stepping on each other's work. This is a pragmatic, empirical approach to the social side of design: rather than seeking theoretical consensus, you build practical alignment through shared experience and incremental improvement.

The goal is not to eliminate tensions -- they are inherent to software development. The goal is to navigate them artfully, maintaining the relationships that make great software possible while steadily improving the structure that enables future greatness.

Beck emphasizes that the Management section is not just for managers. Every programmer who works on a team needs these skills. The decision to propose a refactoring, to communicate its value, to coordinate its execution -- these are not management-only activities. They are design activities that happen to involve other people. The whole point of the book's title -- Tidy Together -- is that design at this scale is inherently collaborative. You cannot opt out of the human dimension by hiding behind technical arguments. You must engage with the social reality of your team, even if (like Beck) you find that uncomfortable.

The Management section also touches on the planned chapters about "Structure Folks and Feature Folks" (the different worldviews and incentives of people oriented toward architecture versus those oriented toward shipping), "The Trough of Despair" (the inevitable period during a refactoring when things get worse before they get better), "Interface and Implementation Hats" (the cognitive discipline of separating what a component does from how it does it), "Push vs. Pull" (different models for initiating structural change), "Ownership Models" (how code ownership affects design decisions), and "Long-Running Changes" (how to manage refactorings that span multiple development cycles). Though these chapters are not yet available, the introduction to Part II makes clear that they will address the messy human realities that pure technical advice ignores.

---

### Chapter 3: Authority & Responsibility

This chapter (numbered as Chapter 17 in the final book) addresses the human dimension of design decisions head-on.

#### A Cautionary Tale

Beck recounts a personal story: he saw a popular open-source project in need of design improvement and proceeded to "nibble, nibble, nibble away at giant chunks of tangled responsibilities," trying to isolate this stuff here from that stuff there. After a month, he could see progress. The future shape of the software was coming into focus.

Then he got ahead of himself. He made changes that made the design worse (a phenomenon explored elsewhere as "The Trough of Despair"). He knew where he was going, but the other developers did not. The next day, almost all his changes had been undone. He did not even try to figure out who did it. He gave up and never contributed again.

The lesson: **if you improve designs but spoil relationships with your fellow developers, you would have been better off not making the changes.**

#### Power Differentials

Beck acknowledges that not everyone has the same power in organizations. Power can be:
- **Formal** -- a manager can promote or fire someone reporting to them
- **Social** -- your opinion of someone carries greater weight than theirs of you
- **Situational** -- you know more about the technical details of an API than someone else does

You cannot erase power differentials, but you can try to reduce their negative consequences. The fundamental question: what relationships, across these power differentials, set us up for accomplishing the most together while growing individually and as a team?

#### Responsibility

The first characteristic of productive relationships is **responsibility** -- the flow of consequences, both good and bad. If a programmer says "I'm responsible for the quality of this software," that means if something goes wrong, they will experience the consequences: they will fix the error, coordinate repairs, or field angry customer calls.

Responsibility encourages relationships by making it safe for the less powerful person to contribute more. If the more powerful person in an interaction harvests positive consequences while dumping negative consequences on others, those others must protect themselves instead of contributing.

Responsibility manifests in software design because the changes we make impose consequences on other people. If you decide to switch the order of two parameters, all current callers need to change. All future callers must use the new order, a consequence for everyone who has memorized the current signature. Part of software design is not just reducing coupling and increasing cohesion, but **accepting responsibility for the human and business consequences** along the way. That is, if you want to work effectively on software that requires more than one programmer.

Beck is careful to acknowledge that words like "responsibility" and "accountability" are often misused -- hijacked by people with their own agendas. He is aware of this problem but chooses to use the words anyway, in their constructive sense. The principle of responsibility is too important to abandon just because some people weaponize the language.

The story of Beck's failed open-source contribution is a microcosm of the entire chapter's argument. He had the right technical instincts. He was making genuine improvements. But he failed to bring the other developers along. He made changes that made the design temporarily worse (because the others could not see where he was headed), and he lost the social capital needed to continue. The technical improvements did not survive because the human relationships did not survive. This is the central caution of the entire Management section.

#### Authority (Incomplete)

Beck begins to define authority as "the power to make changes" and notes that people try to make authority legible, but then interrupts himself: "Damn it, authority isn't a characteristic of productive relationships." This chapter remains unfinished in the Early Release, signaling that Beck is still working through how authority relates to design relationships. The raw, unedited nature of the text is on full display here -- the reader sees Beck thinking in real time, catching himself mid-thought.

---

### Chapter 4: "Good" Design

This chapter (numbered as Chapter 18 in the final book) tackles the fundamental question: What do we mean when we say a design is "good"?

#### The Definition of "Good"

A design is good if **it supports implementing the next feature with a minimum of extra effort**. Each feature carries **intrinsic complexity** -- a certain number of ifs, whiles, and polymorphic messages that must be written before the feature passes its tests. Each design also imposes **accidental complexity** on each feature -- all the other changes you need to make before the feature can be deployed. Design improvement reduces the cost of this extrinsic, accidental complexity.

#### Cost

You cannot evaluate a design's fitness at a single point in time. You care about the cost of behavior changes plus the cost of structure changes into the future. Beck cites Yourdon and Constantine: **"Our primary objective is minimum-cost systems."** They mean cost over time.

#### Value

Value is not just revenue minus cost. Both sides of the equation are complicated:

**Costs are complicated:**
- The cost of operating the system
- The cost of future behavior changes (features)
- The cost of future structure changes
- Discounting all these costs to present day (net present value)
- Evaluating everything in a fog of uncertainty about what future features you will want and what you will learn about improving the structure

**Revenue is complicated:**
- The unknown effect of unknown future features on revenue
- Again discounted because of net present value
- In a foggy competitive marketplace

**Optionality adds value to systems.** Given two systems with equivalent cash flows, you would pay more for the system with more options for future change. Empirical software design increases optionality, creating value even before you see dollars in accounts.

The final element of value is **survival**. All those future cash flows make no difference if the system does not survive long enough to realize them. Beck notes that a key evolution in his thinking since *Tidy First?* is a deeper understanding of the importance of survival, and the chapter on Survival (not yet available) will go deeper into how software design influences system mortality.

#### People: Who Is the Design Good For?

If software design is an exercise in human relationships, which humans? In *Tidy Together*, the primary interest is relationships between people who are changing the system. But even these folks are not a monolith:
- **Experienced developers focused on future features**
- **Experienced developers focused on structure** (formerly called "architects")
- **Newer developers learning their craft** -- features, structure, and social obligations
- **"Visiting" developers** who need changes to the system without sticking around to live with the consequences

The same design can be good for some of these constituencies and bad for others. Choosing the audience and adapting to their skills, worldview, and incentives is also part of design.

#### Heuristics: The Four Rules of Simple Design

Given all the complexity and uncertainty, how do you decide whether one proposed design is better than another? Beck returns to the four rules of Simple Design from Extreme Programming, originally posted on Ward's Wiki:

1. **The Working Rule.** The system works. If a new design state breaks the system, it is bad. Bad is not simple. Bad is complicated. Beck notes that it astonishes him how many designers neglect this.

2. **The Communication Rule.** The system expresses all the concepts of interest to readers. Change a design so it is easier to understand, and you have made it simpler. (Beck acknowledges "simple" is not the right word.)

3. **The Duplication Rule.** The system contains no duplication. Beck softens this today -- duplication is coupling, but sometimes eliminating it costs more than carrying it for the moment.

4. **The Backpack Rule.** Given the above properties, the system contains the fewest possible elements and relationships.

Evaluating proposed changes with these prioritized rules tends to produce structure changes that increase the system's value despite all the uncertainties about the future.

Beck adds an important caveat: these rules are not enough on their own. Do not justify straining relationships with fellow developers by reference to these rules. "I was just eliminating duplication." "Yeah, but now I can't read my code." That is a design fail.

It is worth examining the evolution of Beck's thinking about these rules. When he originally wrote them for Extreme Programming, "simple" meant specifically that you did not add design elements on speculation. He now wishes he had used a different word, because "simple" carries connotations of plainness or austerity that he did not intend. What he really means is something closer to "fit for purpose" or "optimized for the current and foreseeable needs." The priority ordering of the rules is critical: the Working Rule always trumps the Communication Rule, which always trumps the Duplication Rule, which always trumps the Backpack Rule. You never sacrifice a higher-priority rule for a lower-priority one. A system that does not work is not "simple" -- it is broken. A system that eliminates duplication but is incomprehensible has not been improved.

Beck's softening of the Duplication Rule is particularly notable. In the original XP formulation, the rule was absolute: no duplication, period. Two decades of experience have taught him that duplication is coupling, yes, but sometimes the cost of eliminating that coupling exceeds the cost of carrying the duplication. This is a more mature, more empirical stance. It acknowledges that design decisions involve tradeoffs and that the theoretically "pure" solution is not always the practically correct one.

---

## Part III: Theory

### Introduction to Part III

The theory section builds on the foundations from *Tidy First?*: software creates value through behavior (what it does) and structure (how it is organized); coupling drives cost through Constantine's Equivalence (cost of software approximately equals cost of change, which approximately equals cost of big changes, which approximately equals coupling); structure changes are generally reversible while behavior changes often are not; and every "tidy first?" decision sits at the intersection of time value of money pushing toward features now and optionality pulling toward structure that enables future features.

Beck explains why more theory is needed: the simple models that work at the scale of tidying -- minutes to hours, changes that affect mainly you -- start to break down at scale. When changes take days or weeks, when they affect whole teams, when they shape system architecture, new phenomena emerge. He uses an analogy: when you are walking, you can ignore air resistance. When you are flying, aerodynamics dominates everything. The same forces are present at both scales, but their relative importance shifts dramatically.

#### The Limits of Linear Thinking

What Beck did not emphasize enough in *Tidy First?* is that **software development is dominated by power laws, not normal distributions**. This is not a minor detail -- it changes everything:
- Most changes are tiny, but the few large changes dominate total cost
- Most coupling is manageable, but the few highly-coupled areas dominate system complexity
- Most design decisions are local, but the few decisions (not necessarily the ones you expect) dominate the system's evolution

Intuitions trained on bell curves and averages lead us astray. The "typical" change does not matter nearly as much as the exceptional one. The average function size tells us almost nothing useful.

#### From Individual to Collective

At the scale of teams and systems, new forces emerge:

- **Emergent Structure**: Certain designs naturally attract more of the same patterns. Understanding this helps us work with the grain of the system rather than against it.
- **Option Interactions**: Options are not independent. They combine and interfere in surprising ways. A bundle of options is not just the sum of individual options.
- **Social Coupling**: Human relationships create their own coupling patterns. Who knows what? Who trusts whom? These invisible connections shape design choices as much as any technical constraint.
- **Survival Dynamics**: All future cash flows mean nothing if the system does not survive. Understanding what threatens survival and how design decisions affect mortality becomes critical.

Theory serves two purposes: it helps handle cases that do not fit the patterns (which multiply at scale), and it advances practice -- every refactoring started as someone's experiment, every architectural pattern began with someone thinking "What if we organized it this way instead?" (Beck calls this the magical designer question.)

Beck promises that some of the theory gets abstract -- mathematics, economics, even a bit of philosophy -- but pledges to keep it grounded. Every concept has changed how he writes code, works with teams, and thinks about software value. The goal is not to make readers theoreticians but to give them better tools for thinking about the complex, human, economic reality of software development. Theory reveals why some teams thrive while others struggle, why some codebases stay healthy while others decay, why some companies create lasting value while others flame out.

---

### Chapter 5: Power Laws

This chapter (numbered as Chapter 27 in the final book) addresses one of the most important and misunderstood statistical properties of software systems.

#### The Central Question

You are an empirical software designer. You see a really long function. Is it a problem? Is it perfectly normal? Or maybe a really big object with lots of fields, or a file with lots of lines. Problem? Unusual? Normal? Beck spent 25 years gaining the intuition he explains here, most of that time figuring out why these great big "outliers" happen. His hint: **they are not outliers**.

The critical distinction: **does more attract more?** If it does, you need to act one way. If more does not attract more, you can act another way. Mixing up which is which is confusing and ineffective.

#### The Normal Distribution Model (and Why It Fails)

Beck uses a Galton Table (bean machine) as his metaphor for how we typically think about code. As a child, he would stand for hours in front of the Galton Table at the Seattle Science Center, watching balls trickle down through pegs. Early in the cycle, one of the "outliers" might spring to an early lead, but when all the balls had been dropped, the familiar bell-shaped curve had more or less appeared.

In code terms: someone says "functions should be 7 lines, plus or minus 2." Beck models this in JavaScript -- starting at 7, randomly adding or subtracting 1 six times, over 1000 samples. The result is a textbook normal distribution peaking at 7, with counts like 9 functions of length 1, 116 of length 3, 235 of length 5, 308 of length 7, 246 of length 9, 80 of length 11, and 6 of length 13.

So we have a mental model that functions are generally some average size and go up or down a little from there. A tiny function is kind of odd. A great long method means somebody messed up.

**This model does not match reality.** Beck shows the line counts of methods in JUnit5, and the distribution looks nothing like a bell curve. It has an enormous spike at small sizes with a long, fat tail stretching far to the right.

#### The Preferential Attachment Model

What if we use a different model? What if we assume:
- All methods start small
- We add the next line to a random method
- But **the bigger the method, the more likely the next line will attach**

In other words: the big get bigger. This is preferential attachment (also known as the "rich get richer" effect, the Matthew effect, or cumulative advantage). Beck models this in JavaScript with a growth-rate mechanism where size increases the probability of further growth.

The result: lots of little methods and a few really big ones -- out of 1000 samples, 905 are length 1, 83 are length 2, 8 are length 3, and a handful stretch to 4, 5, and even 8. **This matches the real data.**

#### The Log-Log Revelation

Here is the magic trick. Beck spent a long time staring at data with this kind of distribution, trying to make it look like a normal distribution with a few giant outliers and some "normal" size that seemed too small. No amount of squinting answers these questions because **this is a fundamentally different kind of distribution**.

When you change both axes to logarithmic scale, the fat-tailed distribution becomes a **straight line**. No longer does it look like a really skewed normal-ish distribution. It makes perfect sense on its own terms. The JUnit method length data, plotted on log-log axes, also produces that straight line.

This is the hallmark of a **power law distribution**: when plotted on log-log axes, it forms a straight line. Power law distributions have the property that "more attracts more" -- preferential attachment, cumulative advantage. The big get bigger. A few elements dominate the system.

#### Implications for Software Design

The implications are profound. In a power-law world:
- **Outliers are expected, not exceptional.** That giant function is not a mistake; it is a natural consequence of how code grows.
- **Averages are meaningless.** The "Meaningless Mean" chapter (not yet available) will explore this further, but the average function size tells you almost nothing useful about your system.
- **Interventions must target the head of the distribution.** Since the few largest elements dominate cost and complexity, your design efforts should focus there, not on trying to make every function exactly 7 lines.
- **Prevention is about breaking the feedback loop.** The reason big things get bigger is that adding to existing code is easier than creating new abstractions. Design practices that make it easy to create new elements (rather than bolting onto existing ones) interrupt the power-law dynamic.

Understanding power laws fundamentally changes how you read your codebase. You stop asking "why is this function so long?" and start asking "what feedback loop made this function the attractor for all this logic, and how do I break that loop?"

#### Power Laws Beyond Function Length

Beck's analysis focuses on method length, but the power-law pattern applies broadly across software systems. File sizes, class sizes, module dependencies, change frequency, bug concentration -- all tend to follow power-law distributions rather than normal distributions. A small number of files contain most of the code. A small number of modules attract most of the dependencies. A small number of code areas generate most of the bugs. This is not a sign that something has gone wrong; it is the natural shape of grown software.

This has direct implications for where you focus your refactoring efforts. Rather than trying to impose uniform standards across the codebase (all functions must be N lines, all classes must have M methods), you should target the few elements at the head of the distribution. Refactoring the largest, most complex function in the system will yield far more benefit than refactoring a dozen small, clean functions. This is an application of the Pareto principle understood through the lens of power-law dynamics: the vital few dominate the trivial many.

The power-law insight also changes how you evaluate the "health" of a codebase. If you expect a normal distribution of function sizes and you see a few enormous functions, you might conclude that the codebase is unhealthy and its developers are undisciplined. But if you understand that power-law distributions are the natural state of grown software, you can evaluate the codebase more fairly. The question is not whether outliers exist (they always will) but whether the feedback loops that create them are being managed -- whether the team has practices in place to break up concentrations of complexity before they become genuinely problematic.

Beck's use of "folk statistics" is itself a deliberate choice. He acknowledges that a real statistician would have many critiques of his presentation. But his goal is not statistical rigor; it is practical understanding. The key distinction -- does more attract more or not? -- is the one thing empirical designers need to know. If you treat a power-law distribution as if it were a normal distribution, you will waste effort on the wrong problems, set the wrong targets, and draw the wrong conclusions from your data. The folk-statistics framing is sufficient to avoid that error.

---

### Chapter 6: Features & Options Revisited

This chapter (numbered as Chapter 30 in the final book) deepens the economic framework introduced in *Tidy First?*.

#### The Two Sources of Value

Software creates value in two fundamental ways:
- **Features** -- what it does today
- **Options** -- what it could do tomorrow

Features deliver immediate value through behavior: calculating payroll, processing orders, sending notifications. Options preserve our ability to adapt, to respond to the unexpected, to seize opportunities we cannot yet imagine.

#### The Visualization

For years Beck tried to draw the relationship between features and options using time as an axis, but these graphs always obscured more than they revealed. Then he remembered Edward Tufte's trick of abandoning time as an axis. He plots **features on the horizontal axis and options on the vertical axis**.

Each point represents a moment in the life of a software system, showing how many features it has and how much capacity it retains for future change. At first, you have lots of options and no features.

Implementing a feature inevitably reduces options, if for no other reason than you have to keep that feature working. Pleased with the improvement in features and without awareness of the value of options, teams are tempted to just implement the next feature and the next, marching steadily to the right.

Eventually, you approach **no remaining options**. At that point, you either milk the current system for all its remaining dollars or start a big rewrite (complicated by pent-up demand for features). Such rewrite projects are among the most challenging in software because of the many competing constraints. Beck notes, with dry humor, that AI-based coding tools are currently prone to exactly this error -- generating features rapidly while burning through options.

#### Two Paths, Two Destinies

Beck calls the features-only trajectory an error because there is an alternative -- at least for readers of his book series. The empirical approach follows a different path: **alternation**.

You cannot avoid burning options while implementing features. You should not waste options carelessly (Beck's earlier books *Smalltalk Best Practice Patterns* and *Implementation Patterns* address this in detail). But some option-burning will happen.

After adding a feature, you **invest in options**. When you design, change structure, or add options, the system moves vertically on the graph -- more options, same features. This is what a pure structure change looks like in this visualization.

Another feature (move right, lose some options), then more options (move up), then another feature, more options. This **alternating rhythm** is what both books have been building toward. Tidy first, then implement the feature. Or implement the feature, then tidy after. Sometimes batch the tidying for later. But always maintain the balance.

#### The Dynamics of Each Direction

The empirical approach requires awareness. When you are in a feature-adding phase, it is tempting to just keep going: "We are on a roll! Let us just get this next feature in." But each additional feature without corresponding options investment pushes you toward that flat line at the bottom of the graph -- zero options, maximum feature lock-in.

When you are in an options-investing phase, pressure comes from the other direction: "When are we going to ship something users can see?" Options feel abstract and theoretical. Features feel real. But both are forms of value. Beck is trying to teach **rhythm and balance** between the two.

#### Reading the Graph

Once you can see your project's position on this graph, decisions become clearer:
- **Far toward the bottom with few options remaining**: Any significant new feature is probably a mistake. Better to invest in options first, create room to maneuver.
- **High on options but light on features**: You might be overengineering. Are all those options actually real options? Theory without practice is sterile. Features teach you what options you actually need.
- **The sweet spot is not a fixed point** -- it is a dynamic balance. Sometimes you move more horizontally, sometimes more vertically. But you never stay in any one direction too long.

#### The Missing Dimension: Survival

Features and options capture much of the economic reality of software development, but Beck identifies a **third dimension**: survival. All the optionality in the world means nothing if the system (or the team, or the company) does not survive long enough to exercise those options. Survival dynamics -- what threatens system viability and how design decisions affect mortality -- are the subject of a planned chapter that is not yet available in this Early Release.

#### The Features-Options Graph as a Diagnostic Tool

One of the most valuable aspects of Beck's features-options visualization is its use as a diagnostic for teams and organizations. When a team feels stuck -- unable to make progress on features because every change takes too long, requires too many coordinated modifications, and introduces too many regressions -- the graph explains why. They have been moving steadily to the right (adding features) without moving up (investing in options), and they are now pinned against the bottom of the graph with no room to maneuver.

Conversely, when a team is criticized for "not shipping" despite working constantly, the graph can reveal that they are moving vertically (investing in options) without translating those options into features. Their architecture is becoming ever more flexible, but no user is benefiting from that flexibility. The team is building a beautifully designed system that solves no one's problems today.

The diagnostic power of the graph lies in making the invisible visible. Features are visible by nature -- users can see them, product managers can count them, revenue can be attributed to them. Options are invisible by nature -- they represent potential future value that may never be realized. Without a framework like this graph, the options side of the equation tends to be systematically undervalued. Teams that invest in options often struggle to justify the investment. Teams that burn through options often do not realize what they have lost until it is too late.

Beck's comment about AI-based coding tools is particularly pointed. These tools excel at generating features quickly. Left unchecked, they can accelerate the march to the right on the features axis without any corresponding investment in options. The result is software that works today but is brittle, tightly coupled, and resistant to future change. The features-options framework provides a lens for evaluating when AI-generated code is helpful (when you are high on options and need features) and when it is dangerous (when you are already low on options and adding more features without design investment).

---

## Key Themes and Synthesis

### Software Is Grown, Not Assembled

This is the book's foundational metaphor and its most important reframing. Most design advice assumes you can specify what you want, build it, and ship it -- like constructing a bridge. Software is not like that. Software responds to its environment, adapts to new requirements, constraints, and opportunities. The most successful systems are the ones that evolve gracefully, incorporating changes without breaking what came before. They are grown iteratively, shaped by use, pruned and tended like a garden.

This organic metaphor changes everything. In a factory, you want identical parts performing identical functions. In a garden, you want healthy growth patterns that respond to changing seasons. You invest in the soil (tests, tooling, team dynamics) as much as in the plants. You tend the system continuously rather than building it once.

### The Primacy of Human Relationships

Beck returns to this theme relentlessly: software design is an exercise in human relationships. Beautiful software that makes the team miserable is a failure. Elegant architectures that become weapons in power struggles are a failure. Perfect abstractions that nobody understands or wants to maintain are a failure.

The social costs of design mistakes -- debugging, remediation, and especially the erosion of trust -- compound in ways that purely technical analyses miss. The Safety Principle and the Parallels Technique exist not just to prevent bugs but to preserve the social fabric that makes collaborative software development possible.

### The Safety Principle and Parallels Technique

These two ideas form the practical backbone of the book. The Safety Principle (always choose safety over efficiency in design changes) and the Parallels Technique (add the new before removing the old) together enable large structural transformations through sequences of small, independently deployable, behavior-preserving steps. They are the mechanism by which you cross the river one careful step at a time rather than leaping between slippery rocks.

### Power Laws Change Everything

The recognition that software systems exhibit power-law distributions -- not normal distributions -- has profound practical consequences. Averages are meaningless. Outliers are expected, not exceptional. The few largest functions, objects, or modules dominate cost and complexity. Design interventions should target these concentrations rather than trying to enforce uniform standards. And the feedback loops that create these concentrations (the rich get richer, the big get bigger) must be deliberately interrupted through practices that make it easy to create new abstractions rather than endlessly extending existing ones.

### The Features-Options Balance as a Dynamic Rhythm

Beck's features-options graph provides a powerful mental model for navigating the central tension of software development. The path to failure is a straight line to the right -- all features, no options, ending in gridlock and rewrite. The path to success is a zigzag: feature, options, feature, options, maintaining dynamic balance. Neither direction should be pursued too long without the other. The sweet spot is not a fixed point but a rhythm.

### Responsibility Across Power Differentials

Design decisions at team scale inevitably involve power differentials -- formal, social, and situational. Productive relationships across these differentials require responsibility: the flow of both good and bad consequences. When powerful people harvest benefits while imposing costs on others, the less powerful must protect themselves rather than contribute. Responsible design means accepting the human and business consequences of structural changes, not just their technical outcomes.

### Design Evaluation Through the Four Rules

When all the uncertainties of the future make it impossible to evaluate a design definitively, the four prioritized rules of Simple Design provide practical heuristics: the system must work, it must communicate its concepts clearly, it should minimize duplication (with caveats), and given all that, it should contain the fewest possible elements and relationships. These rules reliably guide toward improvements, but they must never be used to justify damaging team relationships.

### The Scale Shift from Tidy First? to Tidy Together

The progression from *Tidy First?* to *Tidy Together* mirrors the progression from individual to team. The principles remain the same -- small safe steps, separate structure from behavior, balance features and options -- but their application becomes qualitatively different. Costs and benefits cross person-boundaries. Timing decisions require coordination. Mistakes have social, not just technical, consequences. The theory required to navigate at this scale goes deeper, into power laws and option interactions and survival dynamics. And the human dimension moves from self-care to the care and feeding of productive team relationships.

### The Role of Incomplete and Unfinished Work

A striking feature of this Early Release is Beck's willingness to show his work in progress. The Authority and Responsibility chapter trails off mid-sentence with Beck catching himself in an error of thinking. Several sections contain TODO markers. The table of contents lists many chapters not yet written. This is not carelessness; it is consistent with Beck's philosophy of empirical, iterative development. He is growing the book the way he advocates growing software: in small steps, with frequent feedback, correcting course as understanding deepens. Readers of the Early Release get to see the process, not just the product, which is itself a lesson in the organic approach to creation that the book advocates.

### Connecting the Parts: From Technique to Theory

The three parts of the book form a coherent whole when read together. Part I gives you the tools -- the Safety Principle, the Parallels Technique, specific refactoring patterns like Parameters Object. Part II gives you the social context -- why these tools matter in a team setting, how to manage the human dynamics of structural change, how to evaluate what "good" means. Part III gives you the theoretical foundation -- why power laws make your intuitions unreliable, why the features-options balance determines long-term success, why survival is the dimension that trumps all others.

Each part informs the others. The Safety Principle from Part I exists because of the social costs identified in Part II and the power-law dynamics identified in Part III. The Parameters Object refactoring from Part I is motivated by the coupling-cost relationship explained in Part III and the team coordination challenges described in Part II. The features-options graph from Part III is the economic justification for the rhythm of tidying and implementing described in Part II, which relies on the techniques from Part I.

This interconnectedness is itself a reflection of Beck's core insight: software design is not a disconnected set of techniques but an integrated practice that spans the technical, the social, and the economic. You cannot be effective at one level while ignoring the others. The programmer who masters refactoring techniques but alienates teammates will fail. The manager who understands team dynamics but cannot evaluate a design will fail. The theoretician who grasps power laws but cannot apply them to concrete code will fail. *Tidy Together* aims to equip readers across all three dimensions.

### Looking Ahead: The Planned Third Book

Beck several times references a planned third book that will address the relationship between people who build software and people who use it -- business stakeholders, customers, the broader organization. That book will tackle "where design becomes political, where the consequences of our technical choices ripple out into the world." The seeds of this direction are visible in the current volume's discussion of survival, optionality, and the economic evaluation of design. The Parameters Object, for instance, is not just a technical pattern; it is a tool that changes the economics of feature development, which directly affects business stakeholders. The features-options graph is a communication tool for explaining design investment to non-technical decision-makers. The theory of power laws helps predict where costs will concentrate, informing planning and budgeting. All of these connect the technical practice of refactoring to the broader organizational context that the third book will explore in depth.

### What This Early Release Reveals About the Complete Vision

Even in its incomplete form, *Tidy Together* reveals the shape of Beck's complete vision for empirical software design. The three-part structure -- Refactorings, Management, Theory -- mirrors the three levels at which design operates: the code, the team, and the system. At the code level, you apply specific techniques to change structure safely. At the team level, you navigate the social dynamics that determine whether those techniques can be applied at all. At the system level, you understand the deep forces -- power laws, optionality, survival -- that make some approaches work and others fail.

The vision is explicitly anti-dogmatic. Beck does not claim to have all the answers. He shows himself thinking, revising, and occasionally catching himself in errors. He invites readers to reach out to the editor to participate in reviewing and commenting on the draft. This openness to feedback is not incidental to the philosophy; it is the philosophy. Empirical software design is grounded in observation, experiment, and revision -- including revision of the advice itself.

The book also continues Beck's long campaign against premature abstraction. The Parameters Object chapter's guidance to hold off when parameter lists are "almost the same," the Backpack Rule's insistence on the fewest possible elements, and the repeated emphasis on "no value, no carry" all point toward a design philosophy that values simplicity born of restraint rather than complexity born of anticipation. This is the mature version of the "You Ain't Gonna Need It" principle from Extreme Programming, refined through decades of practice and now grounded in economic theory.

Finally, the book reinforces a message that runs through all of Beck's work: the importance of caring. Caring about the code, yes, but more importantly caring about the people who work with the code and the people who benefit from it. "Software design is an exercise in human relationships" is not just a slogan or a platitude. It is the organizing principle that determines which techniques to apply, when to apply them, and how to recover when things go wrong. Every chapter in this book -- from the technical mechanics of the Parallels Technique to the economic abstractions of the features-options graph -- is ultimately in service of that principle.

---

## About the Author

Kent Beck is a programmer, creator of Extreme Programming, pioneer of software patterns, co-creator of JUnit, rediscoverer of Test-Driven Development, and observer of the 3X framework (Explore/Expand/Extract). He is alphabetically the first signatory of the Agile Manifesto. He lives in San Francisco and is Chief Scientist at Mechanical Orchard, teaching skills to help geeks feel safe in the world.
