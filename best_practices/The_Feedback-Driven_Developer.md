# The Feedback-Driven Developer
**Author:** Ashley Davis
**Topic tags:** `#testing` `#process` `#feedback` `#iteration` `#productivity` `#tdd` `#code-review` `#pomodoro`
**Language focus:** Language-agnostic (examples in JavaScript/TypeScript)
**Sources:** `markdown_output/The_Feedback-Driven_Developer/The_Feedback-Driven_Developer.md` · `summaries/The_Feedback-Driven_Developer.md`

## TL;DR
Maximise value delivered per unit time by building fast, continuous feedback loops into every stage of development. Three foundations: minimise time to feedback, balance value against cost, minimise wasted time. Six philosophical principles: iterate, embed thinking, keep code working, manage complexity not complication, know when to cut corners, actively seek feedback. Apply to individual and team workflows.

---

## Best Practices by Topic

### The Goal — Working, Reliable, Valuable Code

**Principle:** Speed alone is not the goal. The goal is to deliver **working, reliable, and valuable** code at a rapid, sustainable pace.

- Working: code that is not working is at best not useful, at worst counter-productive.
- Reliable: unreliable code wastes time and frustrates consumers.
- Valuable: code that no one uses wastes the time spent building it.
- The fastest way to "write code" is to **not write code that doesn't need to exist** — choose carefully what to write.

*Ref: The_Feedback-Driven_Developer.md — "1.2 The fastest way to write code" / "1.5 The fastest way to write code - the answer"*

---

### Three Foundations of an Effective Process

**Principle:** A sustainable, fast development process rests on three foundations.

#### 1. Minimise Time to Feedback
- The faster you can see your code working, the sooner you can test it from the customer's perspective.
- **Reduce the time** from making a code change to getting feedback.
- Prioritising fast feedback is the most reliable way to operate at a rapid pace.
- Process should consist of techniques, tools, and practices that support, empower, and scale. **Jettison** anything that slows you down or reduces capacity.

#### 2. Balance Value Against Cost
- Prioritise work by both **value to the customer** and **cost to deliver**.
- Slightly valuable code delivered in a day can outrank extremely valuable code that takes a month.
- You often don't know cost until you're building — leave space for feedback so you can re-estimate, re-evaluate, re-prioritise.

#### 3. Minimise Wasted Time
- Developers are masters of wasting time. Common wastes:
  - Automating things that don't need automating.
  - Adopting tools and processes that slow you down.
  - Creating bugs that take time to find and fix.
  - Spending time on features that won't be used.
  - Pursuing unnecessary perfection.
- **Recognise** waste, **identify** it, then **ruthlessly eliminate** it.

*Ref: The_Feedback-Driven_Developer.md — "1.3 Foundations of an effective development process"*

---

### The Six Principles of Effective Development

#### 1. Build Software Through Iterations
- Nothing gets created all at once. Successful development is **iterative and evolutionary**.
- Break big complex tasks into smaller, more easily managed pieces.
- Each break between iterations is an opportunity for **feedback and course correction**.
- Iterations may be personal (e.g., Pomodoro) or team-based (sprints).

#### 2. Embed Thinking in Your Process
- Don't code continuously without stopping. Intersperse thinking between bursts of coding.
- Use the **Pomodoro Technique** (25-minute work, short break) or similar timeboxing to create natural gaps for thinking.
- Tailor iteration length to context:
  - Stable requirements → up to a day per iteration.
  - Moderately stable → at least four iterations per day (with breaks).
  - Unstable (e.g., startups) → shorter iterations for more frequent re-evaluation.
- **Flow state is dangerous when requirements are unstable** — you can run fast in the wrong direction for hours. Train yourself to enter and exit flow on demand.
- Frequent re-evaluation allows dynamic course correction.

#### 3. Keep Your Code Working
- **The most sacred rule:** every commit should be working code (to the best of your ability).
- The natural state of code is **broken** — only testing (feedback) can confirm it is working.
- Development = taking code through a succession of changes **from working state to working state**.
- **Don't tolerate broken code.** Detect it, fix it, return to a working state immediately.
- Achieve this with **short iterations, fast feedback, immediate fixes**.

#### 4. Manage Complexity, Avoid Complication
- **Complexity is inevitable** in modern software — applications grow, requirements grow, users demand more.
- **Manage complexity** via abstractions, componentization, common conventions/patterns/terminology, supporting tools/processes.
- **Complication is unnecessary** and slows you down. Build complex products from simple parts.
- Strive for simplicity — simple code is easier to understand, easier to test, easier to keep working.
- **Avoid premature optimization** (Donald Knuth: "premature optimization is the root of all evil").
- **Avoid over-engineering / future-proofing** — code for now, not for situations that never happen.
- Aim for good performance code, but only when it doesn't sacrifice simplicity.

#### 5. Know When to Cut Corners
- "Perfection is the enemy of productivity."
- "Ok and useful is preferable to almost perfect and not yet published."
- Learn where the acceptable boundaries are in your organisation.
- If a shortcut generates technical debt, **keep a list** to prioritise and pay down later.

#### 6. Actively Seek Feedback
- Don't wait for feedback to come to you. **Construct** the process to create frequent feedback opportunities.
- Ask questions that elicit feedback — from yourself, colleagues, managers, customers:
  - "Will my design work? What's the cheapest way to find out?"
  - "Do my latest changes work as intended? What tests prove it?"
  - "Will the customer find value? How can I measure that value?"

*Ref: The_Feedback-Driven_Developer.md — "1.4 A philosophy for effective development"*

---

### Two Levels of Feedback

**Principle:** Recognise and use both internal and external feedback; rely more on internal because it is faster.

| Level | Source | Speed |
|-------|--------|-------|
| **Internal / personal** | Self-review, testing your own code, thought experiments | Fast — operates moment-to-moment during the working day |
| **External / team** | Manager reviews, peer code reviews, customer feedback | Slow — hours to days |

- If you rely on external feedback to know where to head, you will move slowly.
- Create your own **internal feedback loops** for self-correction wherever possible.
- External feedback remains necessary — it reveals blind spots. Just don't make it your only feedback.

*Ref: The_Feedback-Driven_Developer.md — "1.6 Feedback-driven development"*

---

### Starting a New Project — Minimum Viable Feedback

**Principle:** Get the simplest possible thing running and observable. That is your first feedback loop.

**Do:**
- Ask: *"What's the next simplest thing I can do to move forward?"*
- Set up a basic HTTP server with the smallest possible endpoint and a hardcoded response — get it running and test it immediately.
- Establish the pipeline: **edit code → save → reload/auto-reload → test (curl, browser, automated test) → see result → repeat**.
- Automate common tasks via npm scripts / Make / equivalent to reduce friction.
- Use **live reload** to minimise the distance between coding and feedback.
- **Use Git from the very start** — `git init` immediately, small frequent commits, meaningful commit messages, branches for experiments. The commit history tells the story of the application's evolution.

**Don't:**
- Spend days designing before writing any code. Get something observable first.
- Skip version control. Start with `git init` from day one.
- Make the first iteration big.

*Ref: The_Feedback-Driven_Developer.md — "2 From little things, big things grow"*

---

### Building Incrementally — Each Step Testable

**Principle:** Add features in small, testable steps. Each step must produce feedback before the next step.

**Do:**
- Apply the same loop at every level: hardcoded → test → add real data → test → add processing → test → …
- Test after every change (manual smoke + automated where it pays off).
- Build database tables incrementally as needed; keep DB code separate from route handlers (separation of concerns).
- Handle file uploads with multipart middleware (e.g., `multer`); validate type/size; generate thumbnails automatically; extract EXIF metadata; store in organised directory structure.
- Apply consistent **error handling** discipline: appropriate HTTP status codes (400 / 404 / 500), meaningful messages, internal error logging, no internal error leakage to clients.

**Don't:**
- Implement several features before testing any of them.
- Mix concerns (DB code in route handlers, business logic in storage layer).

*Ref: The_Feedback-Driven_Developer.md — "2 From little things, big things grow"*

---

### Frontend Feedback Loop

**Principle:** The browser is the developer's test harness. Make the loop as short as possible.

**Do:**
- Start with **plain HTML/CSS/JS** (no framework initially). Progressive enhancement — add complexity only when needed.
- Frontend loop: edit → refresh (or live reload) → inspect DevTools → iterate.
- Build UI in stages: static mockup with hardcoded data → style it → replace hardcoded with API calls → test each stage.
- Use **CSS Grid or Flexbox** for responsive layout; media queries for screen sizes; lazy loading and progressive image loading for performance.
- Configure **CORS** on the backend to enable frontend on a different port.
- Handle frontend errors gracefully: network failures (retry), API errors (meaningful messages), loading states (progress indicators).

**Don't:**
- Pull in a framework on day one without evidence it is needed.
- Skip the static-mockup step and jump straight to API integration.
- Leave the user without feedback during loading or on error.

*Ref: The_Feedback-Driven_Developer.md — "3 The other side of the equation"*

---

### Navigating Uncertainty

**Principle:** Requirements change. The path from idea to working software is twisted, not straight. Build a process that accommodates this.

**Do:**
- **Build a throwaway prototype** to test ideas — not meant to last.
- **Create a testbed application** — a separate minimal app to experiment with new techniques before incorporating them into the main product.
- Use **spikes** — time-boxed investigations to answer technical questions ("Can this library handle our use case?").
- **Reassess priorities regularly** based on new feedback.
- Prefer high-value / low-cost items (quick wins). Break down high-value / high-cost items. Deprioritise low-value items unless they are also low-cost.

**Don't:**
- Pretend requirements are stable when they aren't.
- Spend weeks on a "perfect" design before getting something observable.
- Treat the initial plan as immutable.

*Ref: The_Feedback-Driven_Developer.md — "4 The twisted path of development"*

---

### Managing Technical Debt

**Principle:** Some debt is acceptable; track it explicitly so it can be paid down deliberately.

**Do:**
- Recognise debt: shortcuts, code-that-works-but-isn't-well-structured, missing tests / error handling, hard-coded values.
- Maintain a **technical debt list** — write down every shortcut taken.
- Prioritise debt items **alongside** feature work.
- Pay down debt in **small increments**, not big refactoring projects.
- Use judgement: some debt is acceptable, some is not.

**Don't:**
- Pretend there is no debt. Hidden debt is the most expensive kind.
- Schedule a "big refactoring week" — debt is paid down continuously, not in big bangs.

*Ref: The_Feedback-Driven_Developer.md — "4 The twisted path of development"*

---

### When to Automate

**Principle:** Automate to reduce repeated effort and errors — but only when it pays off.

**Do automate when:**
- The task is repeated frequently.
- The cost of automation is less than the accumulated cost of manual repetition.
- Automation reduces errors.
- Targets include: build and deployment pipelines, testing (unit + integration), code formatting and linting, database migrations.

**Don't automate when:**
- It is a one-time task.
- The automation itself is complex and error-prone.
- The return on investment is uncertain.

*Ref: The_Feedback-Driven_Developer.md — "4 The twisted path of development"*

---

### Working with Others — Communication as Feedback

**Principle:** People are feedback sources, too. Use them deliberately.

**Do:**
- **Show working code to stakeholders early and often** — use demos as feedback opportunities.
- Use **pair programming** for real-time feedback.
- Use **code reviews** as a feedback loop (see next section).
- Identify your customer: end users, boss / lead dev / PM, or colleagues (if you build tools for them).

**Don't:**
- Code in isolation for days without showing anyone.
- Treat customer contact as a phase-gated activity — it should be continuous.

*Ref: The_Feedback-Driven_Developer.md — "4 The twisted path of development"*

---

### Code Review as Feedback Loop

**Principle:** Code review is one of the most valuable team-level feedback mechanisms — treat it as such.

**Do:**
- Submit small, focused, reviewable units of change.
- Write meaningful commit messages and PR descriptions so reviewers understand intent.
- Respond to review feedback as **course-correction data**, not as judgment.
- Use reviews to spot the same signals you'd spot yourself with internal feedback: design smells, missing tests, unclear naming, premature complexity.
- Pair review with automated checks (lint, tests, CI) so reviewers can focus on design and behaviour, not syntax.

**Don't:**
- Submit massive multi-day change-sets — review quality collapses with size.
- Skip review because "CI is green" — green tests don't catch design problems.
- Treat reviewer comments as criticism rather than data.

*Ref: The_Feedback-Driven_Developer.md — "1.6 Feedback-driven development" (external feedback) / "4 The twisted path of development" (Working with Others)*

---

### The AI Era — What Doesn't Change

**Principle:** AI assistants don't change the fundamentals of working, reliable, valuable code.

- Current AIs have no notion of *working code* and can't test what they produce — humans still test and fix.
- Future AIs may test their own code, but humans must still define what *working* means in the domain and communicate it precisely.
- AIs cannot identify **value** — humans must decide priorities.
- Fast feedback loops and well-built tests **remain as important as ever**.

*Ref: The_Feedback-Driven_Developer.md — "1.7 Can't AI just do it all for me?"*

---

## Anti-Patterns & Common Mistakes

- **Big-bang development:** Coding for hours (or longer) before testing → discover the code doesn't work, or worse, has hidden bugs users find. *Fix:* iterate; test each small piece.
- **Coding without thinking first:** "Code first, think later" is prone to errors. *Fix:* embed thinking in the process (Pomodoro, timeboxing).
- **Entering flow on unstable requirements:** Hours of productive-feeling work heading the wrong direction. *Fix:* short iterations with regular re-evaluation when requirements are unstable.
- **Tolerating broken code:** "We'll fix it later." *Fix:* every commit should be working code; fix breaks immediately on detection.
- **Premature optimisation:** Complicates code without measured benefit. *Fix:* only optimise when measured and necessary.
- **Over-engineering / future-proofing:** Designing for situations that never happen. *Fix:* code for now.
- **Pursuing perfection:** Polish that delays delivery without clear value. *Fix:* "ok and useful" beats "almost perfect and not yet published."
- **Automating one-off tasks:** Adds complexity for no payoff. *Fix:* automate only repeated, error-prone, valuable tasks.
- **Big refactoring projects:** Stop-the-world debt pay-down. *Fix:* continuous small increments, tracked in a debt list.
- **Waiting for external feedback:** Slow loops; slow learning. *Fix:* create internal feedback loops; ask the question yourself first.
- **Manual version-control-free work:** "Just this once, I'll commit later." *Fix:* `git init` from day one, commit often.

*Ref: The_Feedback-Driven_Developer.md — "1.4.1"–"1.4.6" / "1.6 Feedback-driven development" / "4 The twisted path of development"*

---

## Decision Heuristics / Checklists

- **What's the next step?** Always answer: *"What's the next simplest thing I can do to move forward?"*
- **Is my iteration small enough?** If a long break would put significant work at risk, the iteration is too long.
- **Am I keeping code working?** Every commit green; every break fixed immediately on detection.
- **Is this complication or complexity?** If it can be simplified without losing capability, simplify it.
- **Should I cut this corner?** Is "ok and useful" good enough? If yes, ship and track debt.
- **Should I automate this?** Repeated? Error-prone? Cost-savings > automation cost?
- **Where is my feedback coming from?** Internal (tests, self-review, thought experiments) for speed; external (peers, customer) for blind spots.
- **Am I wasting time?** Anything that consumes time but is not necessary or valuable is waste — eliminate it.

---

## Key Takeaways

1. **Feedback is the core of effective development.** Speed alone isn't the goal — produce working, reliable, valuable code fast.
2. **Three foundations:** minimise time to feedback, balance value against cost, minimise wasted time.
3. **Six principles:** iterate, embed thinking, keep code working, manage complexity not complication, know when to cut corners, actively seek feedback.
4. **The most sacred rule:** every commit should be working code.
5. **The fastest code is the code you don't write** — choose carefully what to build.
6. **Use both internal and external feedback** — internal is faster; external reveals blind spots.
7. **Start with the simplest possible thing running** — that's your first feedback loop.
8. **Iterate at the right cadence** — Pomodoro / timeboxing for unstable requirements.
9. **Manage complexity, avoid complication** — simple code is easier to test, easier to keep working.
10. **Track technical debt in a list, pay it down in small increments.**
11. **Automate only when it pays off** — repeated, error-prone, valuable.
12. **AI doesn't change the fundamentals** — defining "working" and identifying "valuable" remain human skills.
13. **Your process is a product** — continuously improve it via the same feedback-driven approach.

---

## Cross-References
- Related: [[../TDD_Top_Tips.md]]
- Related: [[../What_to_Test_and_When.md]]
- Related: [[../ATDD_Guide.md]]
- Related: [[../Fundamentals_of_Software_Testing.md]]
- Related: [[../The_Art_of_Unit_Testing.md]]