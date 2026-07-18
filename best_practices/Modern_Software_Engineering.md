# Modern Software Engineering — Doing What Works to Build Better Software Faster
**Author:** David Farley
**Topic tags:** `#architecture` `#general` `#testing`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Modern_Software_Engineering_..._David_Farley.md` · `summaries/Modern_Software_Engineering_-_David_Farley.md`

## TL;DR
Farley anchors "software engineering" in scientific-empirical practice and reduces the discipline to two meta-capabilities — **becoming expert at learning** (iteration, feedback, incrementalism, experimentation, empiricism) and **becoming expert at managing complexity** (modularity, cohesion, separation of concerns, abstraction, loose coupling) — supported by the practical tools of testability, deployability, speed, controlling the variables, and continuous delivery. Treat every change as a small, observable experiment; optimize feedback loops toward sub-hour releasability; design for testability as the primary driver of all design quality.

---

## Best Practices by Topic

### The Definition That Anchors the Discipline

**Principle:** Software engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software. All ten ideas that follow serve that single definition.

**Do:**
- Treat every commit as a tiny, falsifiable experiment ("I predict this test will fail with this exact error").
- Favor evidence (measured outcomes) over authority/intuition when making engineering decisions.
- Anchor decisions in the four-step scientific loop: **Characterize → Hypothesize → Predict → Experiment**.

**Don't:**
- Don't equate engineering with bureaucracy, planning, or "process for its own sake."
- Don't confuse "engineering" with "production engineering" — production in software is essentially free (a push of a button), so the discipline is one of **design engineering**, not manufacturing.
- Don't claim engineering status for practices that do not help you build better software faster ("If our 'software engineering' practices don't allow us to build better software faster, then they aren't really engineering").

**Code:** No code. The definition is the foundation; everything below operationalizes it.

*Ref: Modern_Software_Engineering_..._David_Farley.md — "Preface"; Chapter 1 "Introduction" — "What Is Software Engineering?"*

---

### Optimizing for Learning — The Five Principles

Farley reduces "expert at learning" to five interconnected techniques. Each makes the others more effective; isolate any one and it becomes mere repetition.

#### 1. Working Iteratively

**Principle:** Iteration reduces risk by replacing upfront commitment with successive approximation. Each cycle reveals something that invalidates or refines the previous plan; small cycles accumulate learning at low cost.

**Do:**
- Plan to throw the first implementation away (Brooks) — the cost is borne down to a single iteration.
- Make each cycle's goal small enough that "wrong" is cheap and "right" is informative.
- Treat every plan as a guess that needs validation, never as a contract.

**Don't:**
- Don't equate planning discipline with making big commitments up-front. Planning is about reducing uncertainty, not eliminating iteration.
- Don't ship a "grand plan" and discover it six months later — defend against inaccuracy with iteration, not bigger plans.

*Ref: Chapter 4 "Working Iteratively"*

#### 2. Feedback (Prefer the Fastest, Most Definitive Feedback at Each Level)

**Principle:** Iteration without feedback is repetition. Optimize the speed and determinism of feedback at every layer of the pipeline. Earlier feedback is cheaper, more actionable, and less emotionally loaded than later feedback.

**The Hierarchy (fastest → slowest):**
1. IDE feedback (milliseconds): syntax, types, compilation.
2. Local tests in the area being edited (seconds): from TDD.
3. Full unit test suite (seconds to minutes): local.
4. Continuous integration in a clean environment (minutes).
5. Acceptance / end-to-end / contract tests: feature-level behavior.
6. Performance / load / chaos tests: non-functional behavior.
7. Production monitoring and user feedback: actual user value.

**Do:**
- Target the *fastest* feedback at every layer first; let slowness push you to refactor (not to add staging environments).
- Pair code review with running tests, not as a substitute.
- Treat production feedback as one input among many, not a checkpoint to be feared.

**Don't:**
- Don't gate feedback through other humans when a deterministic machine test would do — humans are too slow, too variable, too expensive.
- Don't defer all testing to the end ("test everything together") — your tests will be cursory and your debugging context lost.

*Ref: Chapter 5 "Feedback"*

#### 3. Incrementalism (Small, Safe Steps)

**Principle:** Progress in many small, safe, working steps rather than a few large, risky ones. Incrementalism **requires** modularity; modularity **enables** incrementalism.

**Tools (the three pillars of incrementalism):**
- **Version control** — track, revert, branch, review, audit every change.
- **Automated testing** — the safety net for "small step then verify."
- **Continuous integration** — validate each step in the context of the whole system.

**Do:**
- Make "design at the last responsible moment" — when you have the most information, no earlier.
- Keep every commit releasable (trunk is always green, always deployable).
- Wire `commit-stage` CI checks that reject any method longer than 20-30 lines or any signature with more than 5-6 parameters — encode your taste in executable policy.

**Don't:**
- Don't accept "design phase" before implementation as a justification for big up-front design. Design emerges from iteration.
- Don't let incomplete work accumulate under feature flags indefinitely — it rots and undermines the safety net.

*Ref: Chapter 6 "Incrementalism"; Chapter 9 "Modularity" (the "guiderails" recommendation)*

#### 4. Empiricism (Grounded in Reality)

**Principle:** Ground decisions in observed reality, not theory, pattern-matching, or authority. Distinguish **empiricism** (guided by observed reality) from **experimentation** (a technique that creates the observations deliberately).

**Do:**
- Build safeguards against self-deception: measurements, automated tests, controlled experiments, willingness to be proven wrong.
- Beware "I know that bug!" — recognizing a pattern is *not* the same as having evidence for its cause. Verify.
- Beware post-hoc rationalizations ("inventing a reality to suit our argument") — instrument your claims.

**Don't:**
- Don't trust averages as a stand-in for tail behavior. Farley: in high-frequency trading, "2ms wasn't an average — that was the limit." Outliers are the failure mode.
- Don't pick the metric that's easiest to game. A team that got paid bonuses for 80% test coverage discovered a quarter of its "tests" contained no assertions. Measure what you actually want.

*Ref: Chapter 7 "Empiricism"; Chapter 8 "Experimental" — the latency/throughput anecdote*

#### 5. Experimentation (TDD as Tiny Empirical Loops)

**Principle:** Organize work as a series of small, controlled experiments — each making a hypothesis, a prediction, and a falsifiable test. Software is unique among engineering disciplines because **the executable simulation IS the system**, not an approximation of it.

**TDD as a tiny application of the scientific method:**
1. *Characterize*: capture desired behavior in a test case.
2. *Hypothesize*: "I expect this test to fail."
3. *Predict*: "It will fail with this exact error message."
4. *Experiment*: run it.

**Do:**
- Treat compilation as an experiment ("I predict my code compiles without warnings").
- Treat every automated test written *before* implementation as an experiment; *after* implementation is just verification.
- Use acceptance/BDD tests as executable specifications that drive the unit-level work.

**Don't:**
- Don't claim to "do TDD" if you write tests after the code — that is unit testing after, not TDD, and it cuts corners, breaks encapsulation, and tightly couples tests to implementation.
- Don't let the size of an experiment intimidate you. The scope ranges from one line (a TDD cycle) to a large architectural change; the same discipline applies at every scale.

*Ref: Chapter 8 "Experimental" — "Automated Testing as Experiments"*

---

### Optimizing for Managing Complexity — The Five Principles

Software development is inseparable from managing complexity. Each of these principles reinforces the others: improving modularity pressures toward better cohesion, better separation of concerns, better abstraction, and looser coupling. The principles apply **fractally** — at every scale from function to enterprise.

#### 6. Modularity (Compartments That Hide Information)

**Principle:** Divide systems into compartments small enough to be understood in isolation, with clear interfaces and minimal dependencies. Modularity is the property most under-valued by the industry; it is what most differentiates expert code from novice code.

**Hallmarks:**
- Code is short enough to be understood as a stand-alone unit.
- Scoped access — clear "inside" and "outside."
- Stable interface for inputs/outputs.
- Reusable in multiple contexts.

**Do:**
- Add CI checks that reject over-long methods (e.g., > 30 lines) and over-wide signatures (> 5-6 params) — turn design taste into automated policy.
- Build services around bounded contexts; align services with the problem domain, not the org chart.
- Design for testability **and** deployability at the same modular boundary — the two converge.

**Don't:**
- Don't write code as a recipe — linear sequences of instructions spanning hundreds of lines, collections of mixed concerns and accidental complexity.
- Don't assume microservices are the only way. A well-structured monolith (loose coupling through clear interfaces) is also valid; the test is "can we make changes independently and deploy them safely?"

*Ref: Chapter 9 "Modularity"*

#### 7. Cohesion (Put Related Code Together; Keep Single Purpose)

**Principle:** Cohesion measures how closely the elements of a module belong together. **One class, one thing. One method, one thing.** Farley's own rule of thumb.

**Coupling & Cohesion — the canonical definitions:**
- *Coupling:* Given two pieces of code A and B, they are coupled when B must change behavior only because A changed.
- *Cohesion:* They are cohesive when a change to A allows B to change so both add new value.

**Do:**
- Treat "if your test for a module requires setting up unrelated concerns, the module has low cohesion" as an invariant — tests are a smell detector for cohesion.
- Keep high-performance hot paths inside a single compartment; hide high-performance concerns inside one side of an abstraction boundary.

**Don't:**
- Don't classify "everything in one big method" as cohesive — that's unstructured, not cohesive. Cohesion requires related-by-purpose, not just related-by-location.
- Don't sacrifice design clarity for performance — Farley's micro-benchmarks (BadCohesion vs. BetterBadCohesion, 50,000 iterations, ~6 ns/call difference) showed complexity-related overhead dominates over call overhead; clean simple code is also fast code.

**Code:**
```java
// Listing 10.2 — "Bad Code, Mildly Better Cohesion"
public class BadCohesion
{
    public boolean loadProcessAndStore() throws IOException
    {
        String[] words = readWords();
        List<String> sorted = sortWords(words);
        return storeWords(sorted);
    }

    private String[] readWords() throws IOException { /* ... */ }
    private List<String> sortWords(String[] words) { /* ... */ }
    private boolean storeWords(List<String> sorted) throws IOException { /* ... */ }
}
```
- The block above is **more** cohesive but still not testable, still mixes concerns, and still hard-codes paths.
*Ref: Chapter 10 "Cohesion"; Listing 10.2 "Bad Code, Mildly Better Cohesion"*

#### 8. Separation of Concerns (Domain Logic Apart from Infrastructure)

**Principle:** Divide a system into distinct sections, each addressing a separate concern. The single most powerful principle in Farley's own design work — he applies it everywhere.

**Essential vs. Accidental complexity (Brooks):**
- *Essential complexity:* inherent to the problem (calculate interest, total a shopping cart).
- *Accidental complexity:* forced by running on a computer (persistence, UI, networks).

**Do:**
- Draw a clean line between essential and accidental complexity at every scope.
- Hide accidental complexity behind a port/adapter boundary so domain logic doesn't know the storage technology, the network protocol, or the UI framework.
- Bake the distinction into your user stories: "One thing, one method" — if you hear "and" in a class or method description, you have two concerns.

**Don't:**
- Don't mix essential and accidental complexity in core domain logic — that kills testability (you can't unit-test the rule without booting a database).
- Don't add the abstraction *only* under test pressure — design with the separation from the outset.

**Code:**
```java
// Listing 11.2 — "Separating Accidental and Essential Complexity"
public interface Accidental
{
    String[] readWords() throws IOException;
    boolean storeWords(List<String> sorted) throws IOException;
}

public class Essential
{
    public boolean loadProcessAndStore(Accidental accidental) throws IOException
    {
        List<String> sorted = sortWords(accidental.readWords());
        return accidental.storeWords(sorted);
    }
    private List<String> sortWords(String[] words) { /* ... */ }
}
```
- After this: `Essential` is fully testable against a fake `Accidental`, identical behavior, dramatically more flexible.
- *Ref: Listing 11.2 "Separating Accidental and Essential Complexity"*

```python
# Listing 11.6 → 11.7 — "Storing a String in S3" → "Storing a String in S3 via a Port"
# BEFORE: domain logic references SDK details directly
def doSomething(thing: Thing) -> None:
    processed = process(thing)
    s3client.putObject("myBucket", "keyForMyThing", processed)

# AFTER: domain logic only knows a port
def doSomething(thing: Thing) -> None:
    processed = process(thing)
    store.storeThing("myBucket", "keyForMyThing", processed)
```
- One rename — from `s3client.putObject` to `store.storeThing` — pushed the storage technology out of the abstraction. The `store` is injected, so the method is testable without S3; the SDK can change without touching call sites.
- *Ref: Listings 11.6 & 11.7 "Storing a String in S3" / "… via a Port"; "Ports & Adapters"*

#### 9. Abstraction / Information Hiding (Conceal Implementation, Expose Intent)

**Principle:** Draw lines so consumers of a module need not know, and do not care, about how it works. The abstraction presents the *what*, hides the *how*. Includes behavior, implementation, and data — not just data.

**Do:**
- Default to hiding information — every parameter type, every return type, every field is a candidate.
- Pick abstractions from the problem domain (Customer, Order, LimitOrder) rather than from tech (Record, DTO). Use ubiquitous language (DDD).
- Always isolate third-party code behind your own abstraction — even when the third-party is "stable," you'll thank yourself later when you migrate.
- Treat fresh abstractions as "mostly working simulations" (George Box: "All models are wrong, some models are useful") — useful now is better than perfect never.

**Don't:**
- Don't excuse bad code by saying "all abstractions leak" — Joel Spolsky's quote is about *caring for* the leaks, not abandoning the practice.
- Don't design through accidental-complexity leakage. If your authz service reports HTML on functional failures, you've broken the abstraction at the wrong layer.
- Don't generalize to `Object` in pursuit of "more flexibility." The sweet spot is the most generic *useful* type, not the most generic period.

**Code:**
```java
// Listing 12.3 — "Prefer to Hide Information"
// DO prefer this:
public List<String> doSomething2(Map<String, String> map);

// NOT this (over-specific):
public ArrayList<String> doSomething1(HashMap<String, String> map);

// NOT this (over-generic):
public Object doSomething3(Object map);
```
- *Ref: Listing 12.3 "Prefer to Hide Information"*

```python
# Listing 12.2 — "Reducing the Abstraction Leak"
def add_to_cart2(self, item):
    if self.store.store_item(item):
        self.cart.add(item)
    return self.calculate_cart_total()
```
- Stepped back from the fully abstracted `add_to_cart3` to allow a transactional relationship, but kept the technical failure mode as a Boolean, not a leaky implementation exception. Leaks are minimized at the model layer, not thrown over the wall to callers.
- *Ref: Listing 12.2 "Reducing the Abstraction Leak"*

#### 10. Loose Coupling (Minimize Unnecessary Dependencies)

**Principle:** Manage coupling explicitly. Some coupling is necessary (else components cannot communicate); the goal is to choose what to couple and isolate the rest. Costs of tight coupling scale super-linearly (potential interactions ~ N²).

**Farley's call:**
> DRY is too simplistic. Sometimes duplication is preferable to coupling. ... the real question is not "is this code duplicated?" but "does this duplication represent a harmful dependency?"

**Do:**
- Aim for **appropriate** loose coupling. The vast majority of failures lean toward too tight coupling, not too loose.
- Propagate transitions through the **expand → migrate → contract** pattern: add the new, switch callers, remove the old.
- Prefer **independent deployability** at the service level — services that need coordinated releases are not really independent.
- Use asynchronous, event-driven communication across process boundaries to remove the temporal coupling that synchronous calls hide.
- Treat shared libraries across independently deployed services as a coupling point — share code only within the scope of a deployment pipeline.

**Don't:**
- Don't chase extreme decoupling. The "fully abstract generic schema" anti-pattern (an over-decorated, recursive data model) can be worse than coupling; measure before you abstract.
- Don't equate loose coupling with no coupling — components that cannot communicate cannot deliver a system.
- Don't tie a service's release to a shared library bump that other teams didn't ask for — that is "developmental coupling" you can avoid.

**Code:**
```python
# Listing 13.2 — "Reducing Coupling"
# A small step, but two extra lines dramatically improve cohesion, separation of concerns, and coupling.
def add_to_cart(self, item):
    self.cart.add(item)
    self.store_item(item)
    return self.calculate_cart_total()

def store_item(self, item):
    conn = sqlite3.connect('my_db.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO cart (name, price) values (item.name, item.item_price)', item)
    conn.commit()
    conn.close()
```
- *Ref: Listing 13.2 "Reducing Coupling"* — note "8 lines → 10 lines" and the punchline: "more code, but less coupled, more cohesive, better SoC." Code is communication to humans, not to computers.

#### The Nygard Model of Coupling (classify all five kinds)

| Type | Effect |
|------|--------|
| **Operational** | Consumer can't run without provider |
| **Developmental** | Changes in producer and consumer must be coordinated |
| **Semantic** | Change together because of shared concepts |
| **Functional** | Change together because of shared responsibility |
| **Incidental** | Change together for no good reason (e.g., a breaking API change) |

Treat each kind as a design lever: design choices can reduce some and not others; choose intentionally. *Ref: Chapter 13 "Managing Coupling" — Table 13.1 "The Nygard Model of Coupling"*

---

### The Practical Engineering Tools

These are the four (or five) tools that operationalize the ten ideas above. Treat them as qualifiers for any decision: technology, process, organization.

#### Testability as the Primary Design Driver

**Principle:** If your code is hard to test, your design is bad — full stop. TDD is a **talent amplifier**, not a magic wand: it doesn't replace skill, but it amplifies whatever skill exists.

**Do:**
- Strive for testability first. The "self-healing" BI integration Farley worked on changed their RDBMS in a single morning because everything was separable and testable in isolation.
- Use TDD to detect missing concepts: a hard test often means you're missing a domain concept (his `GameSheet` was doing both positioning and rules — extracted `Rules` as the missing concept, reduced 9-10 lines of validation, opened future flexibility).
- Optimize for **measurement points**: parameter + return values for fine-grained tests, dependency injection + fake external services for system-level tests.

**Don't:**
- Don't test through private fields. If your test needs to see into the object, the design needs measurement points (constructor injection).
- Don't write tests after the code and call it "TDD." The two are different activities; "TDD doesn't work" complaints are almost always complaints about post-hoc unit testing.

**Code:**
```java
// Listing 14.1 → 14.3 — "Simple Car" vs "BetterCar"
// BEFORE: untestable — no way to observe whether the engine actually started
public class Car {
    private final Engine engine = new PetrolEngine();
    public void start() {
        putIntoPark();
        applyBrakes();
        this.engine.start();
    }
    // ...
}

// AFTER: better testable — engine is injected, a FakeEngine can record outcomes
public class BetterCar {
    private final Engine engine;
    public BetterCar(Engine engine) {
        this.engine = engine;
    }
    public void start() {
        putIntoPark();
        applyBrakes();
        this.engine.start();
    }
}

@Test
public void shouldStartBetterCarEngine() {
    FakeEngine engine = new FakeEngine();
    BetterCar car = new BetterCar(engine);
    car.start();
    assertTrue(engine.startedSuccessfully());
}
```
- One constructor change made the class testable, more flexible (Petrol / Electric / Fake / Jet), and more cohesive.
- *Ref: Listings 14.1, 14.3, 14.4 — "Simple Car Example", "BetterCar", "Test for a BetterCar"*

#### Deployability as the Architectural Frame

**Principle:** The scope of evaluation is always an **independently deployable unit of software**. If you can't release a change into production without further work, the unit of evaluation (the deployment pipeline) is wrong.

> The scope of evaluation should always be an independently deployable unit of software. If we cannot confidently release a change into production without further work, then the unit of evaluation ... is incorrect.

**Do:**
- Choose either whole-system evaluation or fully decomposed independent deployables; nothing in between is useful.
- Use the deployment pipeline as the natural scope for DRY; don't share code across pipelines.
- Treat microservices as a coupling-reduction tool for *between* teams, not as a default for everything.

**Don't:**
- Don't deploy a unit whose behavior across pipeline time you can't verify end-to-end in a reasonable timeframe.

#### Speed as the Fitness Function

**Principle:** Target a releasable, production-quality artifact in less than one hour from commit, with the commit stage completing in ~5 minutes. This single number is a "fitness function" that drives every other good practice.

> Consider what such a target implies. You cannot have teams that are too large ... cannot have siloed teams ... must have a great position on automated testing ... need feedback mechanisms like CI and CD ... have to have good architecture ... and you need to be evaluating independently deployable units of software.

**Do:**
- Optimize for feedback speed alone and watch the rest of the engineering practice line up automatically.
- Aim for a pipeline that runs multiple times per day with a sub-hour target.

#### Controlling the Variables

**Principle:** Where you can control, automate and version; where you cannot, isolate behind abstractions. Determinism is the property of well-engineered systems — it emerges from modularity.

**Do:**
- Version everything: code, config, data, infrastructure (IaC).
- Make tests deterministic — same input, same output, every run.
- Isolate concurrency to controlled boundaries; deterministic modules don't contain concurrency.
- Discard early measurements in benchmarks to remove JIT/JVM warmup effects.

**Don't:**
- Don't run performance tests on the corporate network and trust the results — one team did, and the variance was so wide they couldn't tell what the numbers meant. All the work was waste.
- Don't accept "test results vary" — that is a signal to exert more control, not a property of the test.

#### Continuous Delivery as the Organizing Philosophy

**Principle:** CD is not "automating deployment" — it is *organizing work* so the artifacts are always in a releasable state. It defines an outcome (always releasable + optimized for fast feedback), not a mechanism.

**Do:**
- Treat CI, deep testing, deployment automation, IaC, monitoring as prerequisites — CD unifies them.
- Apply CD's principles to non-software domains where physical constraints prohibit the targets (Tesla retools a factory, SpaceX cycles rocket designs in days).
- Distinguish **deployability** (safe to release) from **releasability** (feature complete) — CD's scope is the former.

**Don't:**
- Don't confuse CD with "I just click the deploy button." The change is in the entire value stream.

---

### Complexity-Driven Design (Putting It All Together)

#### Farley's Lists of Cohesion — Three `add_to_cart` Variants

```python
# Listing 11.1 — "Three Separation of Concern Examples"

# v1: poor cohesion, mixes essential + accidental complexity
def add_to_cart1(self, item):
    self.cart.add(item)
    conn = sqlite3.connect('my_db.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO cart (name, price) values (item.name, item.price)')
    conn.commit()
    conn.close()
    return self.calculate_cart_total()

# v2: cohesive; storage is a separate "seam"
def add_to_cart2(self, item):
    self.cart.add(item)
    self.store.store_item(item)
    return self.calculate_cart_total()

# v3: most cohesive; domain code knows nothing about storage or totals
def add_to_cart3(self, item, listener):
    self.cart.add(item)
    listener.on_item_added(self, item)
```
- **Rule of thumb from Farley:** v1 is bad — separation rules it out. v2 vs v3 is a design choice; he prefers v3 for the maximum freedom of choice at the smallest penalty.
- *Ref: Listings 10.5 & 11.1; Chapter 11 "Separation of Concerns"*

#### Iteration on Cohesion — Python Example

```python
# Listing 10.3 → 10.4
# BEFORE: poor cohesion (two unrelated instance variables in same class)
class PoorCohesion:
    def __init__(self):
        self.a = 0
        self.b = 0
    def process_a(self, x):
        self.a += x
    def process_b(self, x):
        self.b *= x

# AFTER: better cohesion, better modularity, better SoC
class BetterCohesionA:
    def __init__(self):
        self.a = 0
    def process_a(self, x):
        self.a += x

class BetterCohesionB:
    def __init__(self):
        self.b = 0
    def process_b(self, x):
        self.b *= x
```
- *Ref: Listings 10.3 and 10.4 "More Poor Cohesion" / "Better Cohesion"*

#### The "Missing Concept" Diagnostic

```python
# Listing 11.4 → 11.5 — "Missing a Concept" → "Listening to the Code"
# BEFORE: GameSheet is doing both ship placement and rules
class GameSheet:
    def __init__(self):
        self.sheet = {}
        self.width = MAX_COLUMNS
        self.height = MAX_ROWS
        self.ships = {}
        self._init_sheet()
    def add_ship(self, ship):
        self._assert_can_add_ship(ship)
        ship.orientation.place_ship(self, ship)
        self._ship_added(ship)

# AFTER: extract Rules; clean separation, easier to evolve, easier to test
class GameSheet:
    def __init__(self, rules):
        self.sheet = {}
        self.width = MAX_COLUMNS
        self.height = MAX_ROWS
        self.rules = rules
        self._init_sheet()
    def add_ship(self, ship):
        self.rules.assert_can_add_ship(ship)
        ship.orientation.place_ship(self, ship)
        self._ship_added(ship)
```
- The trigger was the test smell — 6 of 11 tests were about validation; the design was missing a `Rules` concept. TDD surfaced it.
- *Ref: Listings 11.4 and 11.5 "Missing a Concept" / "Listening to the Code"*

---

### Tools & Heuristics for Evaluations

> Use the ideas in this chapter, and the rest of the book, as qualifiers. Is the tech deployable? Is it testable? Does it allow us to control the variables? Is it fast enough for continuous delivery? Does it allow us to maintain modular, well-designed code? **The wrong answer to any of these questions should almost certainly disqualify the technology.**

A model for any tool decision in software — third-party component, framework, even an internal service.

*Ref: Chapter 14 "Tools of an Engineering Discipline" — "General Tools to Support Engineering"*

---

### Complexity at the Edges — Testing Web/UI/External Hardware

```js
// Listings 14.6, 14.7, 14.8 — "Stuff to Display" / "Testing" / "Displaying Stuff"
public interface Display {
    void show(String stringToDisplay);
}

public class MyClassWithStuffToDisplay {
    private final Display display;
    public MyClassWithStuffToDisplay(Display display) {
        this.display = display;
    }
    public void showStuff(String stuff) {
        display.show(stuff);
    }
}

@Test
public void shouldDisplayOutput() throws Exception {
    Display display = mock(Display.class);
    MyClassWithStuffToDisplay displayable = new MyClassWithStuffToDisplay(display);
    displayable.showStuff("My stuff");
    verify(display).show(eq("My stuff"));
}
```
- Abstracting the act of displaying decouples the class from any device (Console, LaserBoard, 3DGameEngine, …) and makes it unit-testable without a real browser or DOM.
- *Ref: Listings 14.6–14.8; "Testing at the Edges"*

---

### Optimizing for Learning, End-to-End

**The Causal Chain (Farley's most condensed argument):**

> By working so that our software is always in a releasable state, the core tenet of continuous delivery, we are forced to consider deployability and the scope of our deployment pipelines. By optimizing our approach so that we can learn quickly and fail fast ... then we are forced to address the testability of our systems. This guides us to create code that is more modular, more cohesive, has better separation of concerns, and has better lines of abstraction that keep change isolated and loosely coupled.

Use this when you argue with skeptics: every other good practice is downstream of optimizing for feedback and managing complexity.

*Ref: Chapter 13 end of "Managing Coupling"; Chapter 15 "The Modern Software Engineer"*

---

### Performance Is Not an Excuse for Bad Code

Farley, from Chapter 10:
> High-performance systems demand simple, well-designed code. ... Modern compilers will look at the code in [Listing 10.2] and inline the methods. ... The route to fast code is to write simple, easy-to-understand code.

In his benchmark (50,000 iterations of `loadProcessAndStore`), the difference between `BadCohesion` (1 long method) and `BetterBadCohesion` (split into helpers) was ≤ 300 ms total — about **6 nanoseconds per call** — and was occasionally *faster* with the helper version. Method-call overhead is dwarfed by I/O; the optimizer inlines.

**Do:** Draw the seams of abstraction so that high-performance parts fall on one cohesive side; pay the boundary cost at the seam, not inside the hot path.

**Don't:** Use "performance" as an excuse for unreadable code. Most perceived performance problems are caused by complexity that hides the simple path from the optimizer.

*Ref: Chapter 10 "High-Performance Software"*

---

### Embracing Change — Software Half-Life

A metric Farley borrows from Dan North:

> The quality of the software produced by a team is a function of its software half-life — the time that it takes the team to rewrite half of the software that they are responsible for. Good teams will probably rewrite half the software they are responsible for in months; low-performing teams may never rewrite half.

If a team cannot rewrite half their software in months, they've let complexity accumulate to the point where they cannot learn from it. Kent Beck's "Embrace Change" subtitle is the deeper commitment: keep the door open to changing the code continuously.

*Ref: Chapter 12 "Information Hiding and Abstraction" — the Dan North "software half-life" sidebar*

---

### The Scientific Method, Quoted and Operationalized

Wikipedia, via Farley:
- Characterize: make an observation of the current state.
- Hypothesize: create a description, a theory that may explain your observation.
- Predict: make a prediction based on your hypothesis.
- Experiment: test your prediction.

Feynman, quoted approvingly:
> We look for a new law by the following process: first we guess it!

**Implication:** Engineering is *institutionalized guessing*. The guess is the hypothesis; the test is the experiment; the artifact is the validated result. The discipline is in being explicit and consistent about all four steps.

*Ref: Chapter 1 "Engineering—The Practical Application of Science"; Feynman epigraph in Chapter 8*

---

## Anti-Patterns & Common Mistakes

- **Waterfall-as-engineering:** treating software like a production-engineering discipline with up-front design, rigid phases, and big batches. → *fix:* iterative + incremental + empirical + experimental; deliver one-piece flow.
- **"Big balls of mud":** no architecture, mixed concerns, hidden dependencies, schedule pressure normalizing it. Causes are *cultural* ("design is a luxury") and *technical* (failure to apply modularity/SoC/abstraction). → *fix:* aim for the ten ideas; let testability be your diagnostic; "if the test is hard to write, the design is bad."
- **DRY-by-stealth:** sharing a library between independently deployed services to remove "duplication" — creates developmental coupling that costs more than the duplication saved. → *fix:* apply DRY within the scope of a deployment pipeline, not across pipelines.
- **Over-decorating abstractions:** a "fully abstract schema" that loads with hundreds of roundtrips per query. → *fix:* draw seams that *contain* the high-performance parts; abstraction has costs; favor the simple route.
- **Average as a stand-in for tail:** averages are meaningless for latency in any system with bursty load — measure, e.g., 99.999th percentile, and inspect outliers. → *fix:* heatmaps or histograms, not means.
- **Production-style bureaucracy:** manual approvals, stage gates, separate QA teams as proxies for untrustworthy automation. → *fix:* make the automation trustworthy (TDD + characterization tests + CI + CD); trust follows.
- **"We tried TDD" (after-the-code unit testing):** "TDD doesn't work" complaints almost always mean post-hoc unit testing, not TDD. → *fix:* write the test first, let the test design pressure reveal coupling and missing concepts.
- **Future-proofing / over-engineering:** YAGNI is the answer to nervousness about changing code. → *fix:* make the code changeable (modular, tested, abstracted) instead of fixed-in-time.
- **Craft masquerading as engineering:** extraordinarily talented humans producing 1/10 mm work, while computers do 39 million ops in the time a human notices a change. → *fix:* engineering harnesses machines (verification, automation, reproducibility) rather than replacing them with humans.
- **Measuring the wrong thing:** "80% test coverage" bonuses that produced tests with no assertions. → *fix:* measure stability directly; DORA change-failure rate and MTTR.

## Decision Heuristics / Checklists

- **Is this design good?** Try writing a test for it. If the test is hard to write, the design is bad. Testability is the diagnostic.
- **What's the right cohesion here?** Are you adding "just one more thing" to this module? Stop — extract.
- **Should I share this code?** Are the two consumers in the same deployment pipeline? If not, the duplication may be cheaper than the coupling.
- **What's the deployment-pipeline scope?** Independently deployable unit. If you can't release alone, the unit is wrong.
- **How fast is the feedback slow?** Aim sub-hour end-to-end; sub-5-minute commit stage; every slowness is a force pushing toward smaller modules, fewer silos, and better tests.
- **Concurrency or not?** Reliably testable code is *not* multithreaded within the scope of a test. Move concurrency to the controlled edges.
- **Third-party code:** default to wrap; the cost of the wrapper is far less than the cost of being locked in.
- **Abstraction level:** the most generic type that is still *useful*. Not `Object`, not `HashMap<String, String>`.
- **Is engineering actually happening?** "If our practices don't allow us to build better software faster, then they aren't really engineering." Test the claim.

## Key Takeaways

1. **The definition:** Software engineering = empirical, scientific, practical, efficient, economic problem-solving applied to software.
2. **Two meta-skills:** expert at learning (iteration, feedback, incrementalism, experimentation, empiricism) + expert at managing complexity (modularity, cohesion, separation of concerns, abstraction, loose coupling).
3. **Production is not our problem:** a build trigger is the extent of production in software. Apply *design engineering*, not manufacturing thinking.
4. **TDD is a design tool, not a testing tool.** If the test is hard to write, the design is wrong. If your tests are coupled to your code, write them *first*.
5. **DRY has a scope.** DRY within the deployment pipeline; tolerate duplication across pipelines. Coupling is the cost, not lines of code.
6. **Speed is a fitness function.** Sub-hour releasable and sub-5-minute commit stage drive every other good practice into place automatically.
7. **Asynchronous, not synchronous, between processes.** Synchrony across process boundaries is a leaky, fragile abstraction.
8. **Microservices are for scaling teams**, not for fun; independence of deployment is the only thing that matters.
9. **High performance is simple code.** Method-call overhead is dwarfed by I/O; compilers and CPUs reward simple, predictable code.
10. **Outcomes > mechanisms.** "Always releasable" and "fast feedback" survive when specific tools don't.
11. **Engineering is "the stuff that works."** If your process slows you down without improving quality, it is not engineering.

## Cross-References
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] (operationalizes many of the same ideas in cloud/AWS contexts)
- Related: [[../Continuous_Deployment.md]] (Farley & Humble's earlier work; CD is the operational manifestation of these principles)
- Related: [[../Observability_Engineering.md]] (observability as the feedback loop these principles require)
- Topic index: [[../INDEX.md]]
