# Tidy First? - A Comprehensive Summary

**Author:** Kent Beck
**Published:** October 2023, O'Reilly Media
**Subtitle:** A Personal Exercise in Empirical Software Design
**Foreword:** Larry Constantine

---

## Overview

"Tidy First?" is the first book in Kent Beck's series on empirical software design. It addresses a question every programmer faces daily: "I have to change this code, but it's messy. Should I tidy it first?" Beck's answer is nuanced -- it depends -- but he provides a framework of concrete techniques, management principles, and economic theory to help programmers make that decision wisely. The book is deliberately small in scope, focusing on software design at the individual level: design by you, for you. Later volumes will address team-level and organization-level design.

The book is organized into three parts: **Tidyings** (what to do), **Managing** (how to fit it into your workflow), and **Theory** (why it works). Beck's core thesis is that software design is fundamentally an exercise in human relationships, and that "tidying first" -- making small, safe structural improvements to code before changing its behavior -- is both a practical technique and a form of self-care for programmers.

---

## Part I: Tidyings

Tidyings are a subset of refactorings. Where refactorings can be large and risky, tidyings are "cute, fuzzy little refactorings that nobody could possibly hate on." Beck deliberately reclaims the term from its corrupted usage, where "refactoring" came to mean long pauses in feature development that produce no new features, might break things, and have nothing to show at the end. Tidyings, by contrast, are small, safe, and immediately useful.

Each tidying follows a simple pattern: if you see code like *this*, change it to code like *that*, then ship it.

### Chapter 1: Guard Clauses

Guard clauses address nested conditional logic. When you see code where the entire body of a routine is wrapped in an `if` condition, or deeply nested `if` blocks, you can transform them by inverting the condition and returning early.

For example, nested code like:

```
if (condition)
    if (not other condition)
        ...some code...
```

Becomes:

```
if (not condition) return
if (other condition) return
...some code...
```

Guard clauses make preconditions explicit and reduce nesting. The old "single return" rule dates back to FORTRAN, where routines could have multiple entry and exit points, making debugging nearly impossible. In modern languages, guard clauses actually make code easier to analyze because preconditions are stated up front.

Beck cautions against overusing guard clauses. A routine with seven or eight guard clauses is not easier to read. The technique only applies cleanly when the condition wraps all remaining code in the routine. If the condition only guards part of the routine, you may need to extract a helper first, then apply the guard clause -- always taking tiny steps.

### Chapter 2: Dead Code

Delete it. If code is never executed, remove it. This is straightforward advice that programmers resist for psychological reasons: someone wrote it, the organization paid for it, and maybe we'll need it someday.

Beck identifies the cognitive biases at play -- sunk cost fallacy, loss aversion, and the illusion that unused code has latent value. Version control systems mean we are never truly deleting anything. The string of conditionals required for deleted code to actually be needed again is remarkably long: we would need code that isn't used now, that we want in the future, in exactly the same form, that still works. Even then, we could retrieve it from version control or rewrite it better.

When dead code is hard to identify (e.g., with extensive reflection), Beck suggests a pre-tidying: add logging to suspected dead code, deploy it, and wait for confidence. As always, delete only a little code per tidying diff so that reverting is easy if you are wrong.

### Chapter 3: Normalize Symmetries

Code grows organically, and the same problem often gets solved differently at different times or by different people. This inconsistency makes reading harder because readers expect that difference means difference -- when two things are done differently but mean the same thing, the reader wastes energy on a false distinction.

Beck uses lazy initialization as an example, showing five different patterns for the same concept. Each has trade-offs, but mixing them creates confusion. The solution: pick one approach and convert the others to match. Tidy one form of unnecessary variation at a time.

Beyond making identical code identical, this tidying also involves looking for routines that are similar but not identical, then separating the different parts from the identical parts.

### Chapter 4: New Interface, Old Implementation

When you need to call a routine but its interface makes the call difficult, confusing, or tedious, create the interface you wish existed. Implement the new interface by calling the old one. You can inline the implementation later, after migrating all callers.

This is described as "the micro-scale essence of software design." You want to make a behavior change, and if the design were different, the change would be easier. So make the design like that.

The same impulse applies to coding backward (start from the last line of a routine), test-first development (start with the test), and designing helpers ("if only I had a routine that did X, the rest would be easy").

### Chapter 5: Reading Order

When reading a file, you sometimes reach the end only to find the detail that would have made the entire file understandable. Reorder the code so readers encounter elements in the sequence that best supports comprehension.

Since you just read the code, you know what order you wish you had encountered it in. Give that gift to the next reader. No single ordering is perfect -- sometimes you want primitives first, sometimes the API first. Use judgment based on your recent experience.

Beck cautions against mixing this with other tidyings. Resist the temptation to fix everything at once. Also be careful with languages that are sensitive to declaration order.

### Chapter 6: Cohesion Order

When you need to change behavior and discover the changes are spread across widely dispersed code, reorder the code so the elements you need to change are adjacent. This applies at every scale: routines in a file, files in directories, even code across repositories.

Why not just eliminate the coupling? If you can, that is best, but decoupling may be infeasible because it is intellectually difficult, too expensive in time or money, or socially difficult. Cohesion order is a pragmatic alternative that makes changes easier without requiring full decoupling. Sometimes the clarity from better cohesion unlocks whatever is blocking you from decoupling.

### Chapter 7: Move Declaration and Initialization Together

Variables and their initializations tend to drift apart over time. A variable's name hints at its purpose, but the initialization reinforces that message. When declaration and initialization are separated, readers forget context.

The tidying is simple: move initialization up to the declaration. Experiment with ordering: is it better to declare each variable just before it is used, or to declare all variables together at the top? Think like a mystery writer, leaving clues for readers.

You must respect data dependencies: if variable b depends on variable a, a must be initialized first. Analyzing dependencies by hand leads to mistakes, so work in small steps and back up to a known correct version if something goes wrong.

### Chapter 8: Explaining Variables

Expressions grow over time. What starts small accumulates complexity. When you understand a sub-expression within a large, complex expression, extract it into a variable named after its intention.

For instance, in graphics code, a `Point` constructor with two large expressions becomes clearer when each expression is extracted into a named variable like `width`, `height`, `top`, or `left`.

This tidying takes your hard-won understanding and encodes it back into the code, making future changes easier because the expressions are now separated, and reading faster next time the code needs to change.

### Chapter 9: Explaining Constants

When you encounter a magic number or a repeated literal string whose meaning is not immediately obvious, create a symbolic constant and replace uses of the literal with the symbol.

Beck notes this is ancient advice that still gets ignored (e.g., raw `404` instead of `PAGE_NOT_FOUND`). The point is not to be judgmental about who created the mess; it is to take care of yourself by tidying before making changes.

Be careful that the same literal can mean different things in different contexts. Creating `ONE = 1` everywhere is not helpful. The goal is to take your understanding and put it into the code so you do not have to hold it in your head.

### Chapter 10: Explicit Parameters

When a routine works on data that was not passed explicitly -- perhaps pulled from a map, environment variable, or global state -- make the inputs clear by splitting the routine. The top part gathers parameters and passes them explicitly to the second part.

For example, a function receiving a `params` map and accessing `params.a` and `params.b` can be split into a thin wrapper and an inner function with explicit `a` and `b` parameters. This makes code easier to read, test, and analyze.

### Chapter 11: Chunk Statements

This is described as the simplest tidying: when reading a block of code and realizing "this part does this, and then that part does that," put a blank line between the parts.

Beck uses this to illustrate the philosophy of the book: do not make software design such a big deal that you fail to do it. A little design enables a little ease of change. And design has compound interest: design also makes more design easier. After chunking, you have paths forward -- explaining comments, extracting helpers, explaining variables.

### Chapter 12: Extract Helper

When you see a block of code inside a routine that has an obvious purpose and limited interaction with the rest of the routine, extract it as a helper named after its purpose (not its implementation).

Special cases include: extracting just the lines you need to change within a larger routine (change them in the helper, then optionally inline back), and expressing temporal coupling (if `a()` must always precede `b()`, create an `ab()` helper that calls both).

New interfaces become tools for thinking about problems. Do not worry about applying the helper everywhere immediately -- that can be another tidying. Automated refactoring tools are invaluable here.

### Chapter 13: One Pile

Sometimes code has been split into many tiny pieces in a way that actually hinders understanding. The solution is counter-intuitive: inline everything into one big pile, then tidy from there.

Symptoms that call for this approach include long repeated argument lists, duplicated code (especially repeated conditionals), poorly named helpers, and shared mutable data structures. The bias toward small pieces is generally correct, but when the pieces interact badly, consolidation reveals the true structure.

As the pile grows, the shape of the computation emerges in your mind. You begin to see natural divisions that were obscured by the existing decomposition. Then you can ask: should I tidy first, or just make the change I can now see?

### Chapter 14: Explaining Comments

When reading code and having the moment of "Oh, so that's what's going on!" -- record it. Write down only what was not obvious from the code. Write to someone specific, thinking from their perspective.

Good times to add comments: when you encounter a file with no header comment, immediately after finding a defect, and when you discover non-obvious coupling. Comments that say "be sure to change ../foo if you add another case" are not ideal but far better than leaving the coupling undocumented.

### Chapter 15: Delete Redundant Comments

When a comment says exactly what the code says, remove it. Such comments provide costs without benefits. They waste the reader's irrecoverable time.

Beck emphasizes he is not anti-comment. He is anti-redundant-comment. The purpose of code is to explain to other programmers what you want the computer to do. Comments are useful for expressing things code cannot, but redundant comments add noise.

Tidyings often chain together: a previous tidying (like introducing a guard clause) may render a previously useful comment redundant. That is the time to delete it.

---

## Part II: Managing

Part II shifts from the mechanics of individual tidyings to the question of how tidying fits into daily development workflow. The emphasis is that tidying should never be a big deal -- never something that must be reported, tracked, planned, and scheduled. You tidy because you need to change code and it is messy, so you tidy first.

### Chapter 16: Separate Tidying

Beck addresses the common tail-chasing pattern: programmers mix tidyings with behavior changes, reviewers complain about large PRs, programmers split them, reviewers complain about pointless PRs, and the cycle repeats.

The recommended approach is to separate tidyings into their own PRs, with as few tidyings per PR as possible. Beck describes the learning progression: first an undifferentiated mass of changes, then an awareness of which changes are structural versus behavioral, then the ability to plan sequences of tidyings followed by behavior changes, and finally the discipline to put each sequence in its own PR.

The size of PRs is a trade-off. Large PRs show the whole picture but overwhelm reviewers. Tiny PRs invite focused feedback but risk going off into the weeds. Review latency creates a reinforcing loop: fast reviews encourage smaller PRs, which encourage faster reviews. Slow reviews encourage larger PRs, which further slow reviews.

Beck's ultimate recommendation: once you are comfortable with tidying, experiment with not requiring reviews for tidying PRs. This reduces latency and incentivizes even smaller tidyings.

### Chapter 17: Chaining

Tidyings are like potato chips -- one leads to another. Managing this urge is a key skill. Beck encourages experimenting with very tiny steps. From the outside it looks like you are running, but like a centipede, you are taking many little steps.

The chapter catalogs how tidyings chain together:

- **Guard clause** leads to explaining helpers or explaining variables.
- **Dead code** removal reveals opportunities for reading order or cohesion order.
- **Normalize symmetries** enables grouping code into reading order.
- **New interface, old implementation** leads to converting all callers (fanout).
- **Reading order** reveals symmetries that were previously too far apart to see.
- **Cohesion order** identifies candidates for extraction into subelements.
- **Explaining variables** produce candidates for explaining helpers and make redundant comments deletable.
- **Explaining constants** lead to cohesion order by grouping constants that change in sync.
- **Explicit parameters** can reveal new abstractions -- some of the most powerful abstractions derive from running code.
- **Chunk statements** precede explaining comments and extracting helpers.
- **Extract helper** enables guard clauses, explaining constants, and deleting redundant comments.
- **One pile** leads to chunking, explaining comments, and extracting helpers.
- **Explaining comments** can often be replaced by explaining variables, constants, or helpers.
- **Deleting redundant comments** helps reveal better reading order or explicit parameters.

Beck concludes by emphasizing that you should practice tidyings like the notes of a scale. When the notes are clean and relaxed, you can form them into melodies.

### Chapter 18: Batch Sizes

How much tidying should you do before integrating and deploying? This is a Goldilocks dilemma. The costs that rise with larger batches include:

- **Collisions:** More tidyings means longer delay before integrating, increasing the chance of merge conflicts. Merge conflicts raise costs by an order of magnitude.
- **Interactions:** The chance of accidentally changing behavior rises with the number of tidyings in a batch.
- **Speculation:** The more tidyings per batch, the more prone you are to tidying "just because," with all the attendant costs.

Despite these costs, Beck observes that many programmers produce large batches of tidyings. Why? Because the fixed cost of getting a change through review and deployment is substantial. Programmers feel this cost and batch more, even as the costs of collisions, interactions, and speculation rise.

The solution is not to accept these cost curves as laws of physics. Reduce the cost of review. In teams with trust and a strong culture, tidyings may not require review at all. Getting to that level of safety and trust takes months of practice, experimentation, and reviewing errors together.

### Chapter 19: Rhythm

How much time does one cycle of tidying followed by a behavior change represent? For the scale of this book -- software design with personal impact -- Beck says minutes to an hour. More than an hour of tidying before a behavior change likely means you have lost track of the minimum set of structural changes needed.

However, sometimes the code is such a mess that you can profitably tidy for hours. If so, it will not be true for long. Software design has a "pave the path" tendency: behavior changes cluster in the code (Pareto principle: 80% of changes occur in 20% of files), and tidyings cluster in exactly those same spots. Eventually, encountering untidy code becomes the exception, even though most of the code has never been touched.

### Chapter 20: Getting Untangled

Even with the best intentions, tidyings and behavior changes sometimes get tangled together. An hour in, you understand all the behavior changes and all the tidyings, but you have a mess of changes all mixed together.

Beck presents three options, none attractive:

1. **Ship it as is.** Quick but impolite to reviewers and error-prone.
2. **Untangle into separate PRs.** More polite but potentially a lot of work.
3. **Discard and start over, tidying first.** More work but leaves a coherent commit chain.

Beck encourages experimenting with the third option. Re-implementation often reveals something new. The sunk cost fallacy makes this hard -- you have working tests, so why throw them away? Because you are not just instructing a computer; you are explaining your intentions to other people. The sooner you notice a tangle, the smaller the job of untangling.

### Chapter 21: First, After, Later, Never

This chapter addresses the timing question directly. When should you tidy?

**Never** -- When you are never going to change the code again. For truly static systems, "if it ain't broke, don't fix it" applies. This is rare but real.

**Later** -- Many believe tidying later is pure fantasy. Beck insists it is possible if you have enough time to do your work. He invites you to examine the assumption that there is never enough time. He has worked with large, successful, highly profitable businesses that still believed there was not enough time, in the face of all evidence to the contrary.

If you can provisionally believe there is enough time, you might create a "Fun List" of messes to tidy later. Then, rather than jumping feverishly to the next feature, you might pick an item from the list. Tidying later also creates value by reducing the "tax of messiness" (e.g., migrating API call sites), as a learning tool (the code "knows" how it wants to be structured), and because it feels good.

**After** -- Sometimes you cannot see how to tidy until after you have made the behavior change. Tidy after makes sense when: you are going to change the same area again soon, it is cheaper to tidy now than later, and the cost of tidying is roughly proportional to the cost of behavior changes.

**First** -- The title question. Bias toward tidying first when: it pays off immediately in improved comprehension or cheaper behavior changes, and you know what to tidy and how. Be wary of tidying becoming an end in itself.

**Summary:**
- Tidy **never** when the code will never change again.
- Tidy **later** when there is a big batch without immediate payoff, eventual payoff exists, and you can tidy in little batches.
- Tidy **after** when waiting would be more expensive, or when you need a sense of completion.
- Tidy **first** when it pays off immediately and you know what to do.

---

## Part III: Theory

Having covered *what* to tidy and *how* and *when*, Beck now addresses *why*. Theory does not convince, but it optimizes application. The forever questions of software design -- when to start, when to stop, how to decide -- cannot be answered rationally because the necessary information does not exist at decision time. Theory sharpens judgment and enables constructive disagreement.

### Chapter 22: Beneficially Relating Elements

Beck defines software design as **beneficially relating elements**. Each word carries weight:

**Elements:** Software has a hierarchy of substantial structures with boundaries and subelements. In our world: tokens, expressions, statements, functions, objects/modules, systems. Elements have boundaries -- you know where they start and end.

**Relating:** Elements exist in relation to each other. In software, relationships include invokes, publishes, listens, and refers.

**Beneficially:** Without design, you could have a single gigantic soup of tiny subelements (like assembly language with a global namespace). It would work, and externally it would behave identically to a well-designed program. But you would quickly be unable to change it. When we design, intermediate elements begin benefitting each other. Function A can be simpler because function B handles complexity.

Beck illustrates with a concrete example: moving the expression `box.width() * box.height()` into `box.area()`. This creates a new element (`Box.area()`), reduces the relationship between caller and box from two invocations to one, and produces the benefit of a simpler calling function at the cost of a slightly larger Box object.

From this perspective, designers can only: create/delete elements, create/delete relationships, and increase the benefit of relationships.

### Chapter 23: Structure and Behavior

Software creates value in two ways: what it does today (behavior), and the possibility of what it could do tomorrow (optionality).

Behavior can be characterized as input/output pairs and invariants. Behavior directly creates value -- people pay to avoid calculating numbers by hand. If running software costs $1 in electricity and you can charge $10, you have a business.

But what about tomorrow? The mere presence of a system behaving a certain way changes the desire for how it should behave. However much you would pay for a $10/$1 machine, you would pay more for one that could turn into either a $100/$10 machine or a $20/$1 machine, even if you did not know which it would become. This is optionality.

Options are the economic magic of software, especially the option to expand. If you can send 1,000 notifications, you almost certainly can, with work, send 100,000. The more volatile the environment, the more valuable options become -- which is why Beck subtitled *Extreme Programming Explained* "Embrace Change."

What kills options? Key employees quitting, distance from customers, and skyrocketing costs of change. Tidying addresses the third: we can keep the kitchen clean as we cook.

The structure of a system does not matter to its behavior -- one big function or many small ones produce the same paycheck. But structure creates options. The problem is that structure is not legible in the way behavior is. Product roadmaps are lists of features because a new button is visible; "the code is easier to change" is not.

### Chapter 24: Economics: Time Value and Optionality

Beck recounts how finance-related programming projects in his mid-30s taught him the nature of money. Money has two key properties that profoundly affect software design:

1. **A dollar today is worth more than a dollar tomorrow** -- so earn sooner and spend later.
2. **In a chaotic situation, options are better than things** -- so create options in the face of uncertainty.

These two strategies conflict. Earning money now can reduce future options, but without earning now, you may not survive to exercise those future options. Software design must reconcile these imperatives.

### Chapter 25: A Dollar Today > A Dollar Tomorrow

A dollar today is worth more than a dollar tomorrow because you can spend it or invest it immediately, and because a promised future dollar carries the risk that it may never arrive.

To value a software system, its internal characteristics (lines of code, cyclomatic complexity) are irrelevant. What matters is how money flows: how much, when, and how certain. Beck provides a sharpening exercise: which is more attractive, a system that over 10 years costs $10M and brings in $20M, or one that costs $10M and brings in $12M? It is a trick question because "over 10 years" is financially equivalent to "until the heat death of the universe." The key variables are *when* and *how sure*.

At the scale of tidying (minutes to hours), discounted cash flows do not make a huge difference, but practicing with time value prepares you for larger scales. In this book's scope, time value slightly favors tidying *after* rather than *before*, since tidying after means earning money sooner and spending later.

### Chapter 26: Options

Beck discovered options pricing theory while working on Wall Street trading software and implementing pricing formulas test-first. The lessons he absorbed:

- "What behavior can I implement next?" has value all by itself, even before implementing it. Beck was not getting paid for what he had done; he was getting paid for what he could do next.
- The more behaviors in the portfolio, the more valuable the option.
- The more valuable the behaviors, the more valuable the option.
- You do not need to know which behavior will be most valuable, as long as you keep the option open.
- The more uncertain your predictions of value, the *greater* the value of the option. Embracing change maximizes value precisely where conventional development fails most spectacularly.

Beck provides a primer on financial options using a potato analogy. A call option is the right, but not the obligation, to purchase something in the future at a fixed price. The parameters include the underlying thing, its price and volatility, the premium (what you pay today), and the duration.

For software design: the behavior changes we *could* make next are the potatoes. Design we do today is the premium we pay for the option of implementing the behavior change tomorrow. This reframing turned Beck's thinking upside-down. Volatility became exciting rather than terrifying. The less design work needed to create an option, the better.

### Chapter 27: Options Versus Cash Flows

This is the core economic tension of the book:

- **Discounted cash flow** says: earn sooner, spend later. Do not tidy first. That is spending sooner and earning later.
- **Options** say: spend now to make more money later. Absolutely tidy first (when it creates options).

When `cost(tidying) + cost(behavior change after tidying) < cost(behavior change without tidying)`, then tidy first is clearly correct.

When tidying costs more in the short term, it may still be justified if: you are implementing a series of behavior changes that all benefit from the tidying, the value of options created exceeds the time-value cost, or tidying is pleasant and you are worth it (self-care).

At the scale of minutes to hours, you cannot precisely calculate these economics. You are practicing two forms of judgment: awareness of the incentives affecting design decisions, and relationship skills you will later use with colleagues.

### Chapter 28: Reversible Structure Changes

Structure changes are generally reversible in a way behavior changes are not. Extract a helper and do not like it? Inline it. A bad haircut grows out; a bad tattoo is forever.

Reversible and irreversible decisions should be treated differently. Irreversible decisions deserve careful review and deliberation. Reversible decisions -- which is most software design -- have little downside because they can be easily reversed. Since there is little value in avoiding mistakes, do not invest much in preventing them. This is why Beck chose "tidying" -- it is no big deal.

Code review processes typically do not distinguish between reversible and irreversible changes, which is wasteful. For design changes that are not easily reversible (like extracting a service), make them reversible: implement a prototype in production, use feature flags, tidy first to minimize the number of flag checks.

Another way decisions become irreversible is when they propagate throughout the codebase. The antidote is the same: tidy your way out, one small step at a time.

Beck confesses to having once worshipped at the "altar of If Only I Were Infinitely Smart" and having since learned the value of making decisions reversible instead.

### Chapter 29: Coupling

This chapter introduces the central concept driving software cost. Yourdon and Constantine observed that expensive programs shared one property: changing one element required changing other elements. They called this "coupling."

Two elements are coupled with respect to a particular change if changing one necessitates changing the other. The nuance is critical: we cannot just say two elements are coupled; we must say coupled *with respect to which changes*. If the coupling is with respect to a change that never happens, it is irrelevant.

Coupling has two properties that make it expensive:

1. **1-N:** One element can be coupled to any number of other elements. Tooling (automated refactoring) can mitigate this.
2. **Cascading:** A change ripples from element to element, each triggering further changes. This is the bigger issue and the source of the power law distribution of change costs.

The word "coupling" has lost precision over time, coming to mean any relationship. Beck insists on specificity: not just that services are coupled, but how, and with respect to what changes.

Beck shares an anecdote from Facebook where two services sharing a physical rack were coupled through a shared network switch. One team changed their backup policy, saturating the switch, and the other team's service failed. The teams were not even aware of each other.

### Chapter 30: Constantine's Equivalence

Beck recalls hearing that 70% of software costs went to maintenance and thinking that was terribly high. In reality, that estimate is far too low. You can release value-creating software after only a few percent of its eventual development cost. The sooner you get feedback from real usage, the less you spend on behavior that does not matter.

This leads to the first part of what Beck calls Constantine's Equivalence:

```
cost(software) ~= cost(change)
```

The initial development period is economically insignificant compared to the total cost of changes over the system's lifetime.

Not all changes cost the same. Most changes cost roughly the same, but occasionally a superficially similar change costs 10 or 100 or 1,000 times as much. The cost per time grows slowly, then rapidly, then shrinks as other opportunities become more profitable. This follows a power law distribution: the few biggest events outweigh the far more numerous small events. The five biggest storms cause more damage than ten thousand small ones.

What makes expensive changes expensive? Cascading coupling. So:

```
cost(change) ~= cost(big changes) ~= coupling
```

The full Constantine's Equivalence:

```
cost(software) ~= cost(change) ~= cost(big changes) ~= coupling
```

Or simply:

```
cost(software) ~= coupling
```

To reduce the cost of software, reduce coupling. But decoupling is not free and involves trade-offs.

### Chapter 31: Coupling Versus Decoupling

Why not just decouple everything? Several reasons:

- **Coupling is often invisible** until you step on it. You may not know what unconscious assumptions you are making.
- **Discounted cash flows justify some coupling.** There was a quick, coupled way to implement behavior and a slower, decoupled way. At the time, the coupled approach was economically correct.
- **Some coupling was not a problem until now.** The boulder was perched on the hill and decided to roll.
- **Some coupling is inevitable.** (Beck admits this is a confident assertion without a strong argument.)

You face a trade-off: pay the cost of coupling or pay the cost of decoupling. "Tidy first?" is this decision in miniature.

Beck provides a concrete example: sender and receiver functions for a communication protocol are coupled. After the hundredth modification, you might introduce an interface definition language that eliminates the coupling. But the coupling is not truly "gone" -- adding a new field still requires the sender to compute it and the receiver to use it.

Beck shares a belief he cannot fully prove: the more you reduce coupling for one class of changes, the greater the coupling becomes for other classes. The practical implication is to not squeeze out every last bit of coupling. The trade-off space is real, and the exact costs are unknowable in advance, evolve over time, and involve discounted cash flows and uncertain optionality.

### Chapter 32: Cohesion

Coupled elements should be subelements of the same containing element. That is cohesion's first implication: "shovel all the manure into one pile." The second implication: elements that are not coupled should go elsewhere.

If a module has 10 functions and 3 are coupled, you have two options: extract the coupled three into their own subelement, or move the uncoupled seven elsewhere. Extracting a helper function is this kind of extraction -- if the lines have to change together, the helper is cohesive, with benefits of easier analysis, easier change, and resistance to accidental behavior modification.

Beck advises making no sudden moves. You are working with incomplete and changing information about what is coupled with what. Move one element at a time. Follow the Scout rule: leave it better than you found it.

### Chapter 33: Conclusion

The forces that affect "tidy first?" are:

- **Cost:** Will tidying make costs smaller, later, or less likely?
- **Revenue:** Will tidying make revenue larger, sooner, or more likely?
- **Coupling:** Will tidying reduce the number of elements that need changing?
- **Cohesion:** Will tidying concentrate the elements you need to change into a smaller scope?

Most important is you. Will tidying bring peace, satisfaction, and joy to your programming? If you are your best self, you are a better programmer. You cannot be your best self if you are always rushing, always changing code that is painful to change.

But do not get carried away. Once you realize tidying improves your life, you can get giddy. Unlike features, where you can do what you think is right and still dissatisfy people, you are the audience for your tidying, and you are very likely to be satisfied. Resist the urge to keep eating the Pringles of software design. Tidy to enable the next behavior change. Save the tidying binge for later.

This book focuses on software design by and for individuals. The next book in the series examines relationships between programmers. The book after that addresses the most fraught and consequential relationship: between business and technology. The ultimate goal is to make software design truly an exercise in human relationships.

The book ends with Beck's answer to the title question: "Tidy first? Likely yes. Just enough. You're worth it."

---

## Key Takeaways

1. **Tidyings are tiny, safe structural changes.** They are a subset of refactorings that are small enough to be uncontroversial and immediately useful. Examples include guard clauses, deleting dead code, normalizing symmetries, creating new interfaces, reordering for reading or cohesion, moving declarations next to initializations, explaining variables and constants, making parameters explicit, chunking statements, extracting helpers, consolidating into one pile, adding explaining comments, and deleting redundant comments.

2. **Separate structural changes from behavioral changes.** Do not mix tidyings with feature work in the same commit or PR. Keep them separate so reviewers can easily assess each type of change. Ideally, make tidying PRs small enough and safe enough that they do not require review.

3. **Tidyings chain together and compound.** One tidying reveals opportunities for the next. Guard clauses lead to explaining helpers. Dead code removal reveals better reading order. Chunking leads to extracting helpers. This compound interest means small steps accumulate into large improvements, but it also means you must consciously stop tidying and get back to behavior changes.

4. **The timing question has no single answer.** Tidy first when it pays off immediately and you know what to do. Tidy after when waiting would be more expensive or when you need the context from having made the change. Tidy later when there is no immediate payoff and you have enough time to do your work well. Tidy never when the code will genuinely never change again.

5. **Software design is beneficially relating elements.** Elements are the structures (functions, modules, systems), relationships connect them (invokes, publishes, refers), and benefits are what make the relationships worth having. Designers create and delete elements and relationships, and increase the benefit of relationships.

6. **Structure creates optionality; behavior creates cash flow.** These are the two sources of software value, and they are in tension. Time value of money favors earning sooner and spending later (tidy after). Optionality favors spending now to enable uncertain future gains (tidy first). Good judgment requires balancing both.

7. **Coupling drives the cost of software.** Constantine's Equivalence states: cost(software) equals cost(change) equals cost(big changes) equals coupling. The power law distribution of change costs means a few cascading changes dominate total expense. Reducing coupling reduces cost, but decoupling itself has costs, and eliminating all coupling is neither possible nor desirable.

8. **Most design decisions are reversible, so treat them as such.** Unlike behavior changes (where sending 100,000 wrong tax notices is costly to fix), most structural changes can be easily reversed. This means you should not over-invest in preventing mistakes in design. Just tidy. If it does not work out, revert.

9. **Cohesion is coupling's complement.** Coupled elements should live together; uncoupled elements should live apart. Follow the Scout rule: leave the code better than you found it, one element at a time.

10. **Tidying is self-care, and you are worth it.** The ultimate justification for tidying is that it makes your work easier, more pleasant, and more effective. A programmer who is happy and working with clean code is a better programmer. Bias toward tidying first, just enough, because you deserve to work with code that does not cause unnecessary pain.
