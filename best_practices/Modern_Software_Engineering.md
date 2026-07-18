# Modern Software Engineering: Doing What Works to Build Better Software Faster
**Author:** David Farley
**Topic tags:** `#architecture` `#testing` `#general`
**Language focus:** language-agnostic (examples in C#/Java/Python)
**Sources:** `markdown_output/Modern_Software_Engineering_Doing_What_Works_to_Build_Better_Software_Faster_-_David_Farley/Modern_Software_Engineering_Doing_What_Works_to_Build_Better_Software_Faster_-_David_Farley.md` · `summaries/Modern_Software_Engineering_-_David_Farley.md`

## TL;DR
David Farley's manifesto for software engineering as an empirical, scientific discipline: software development is design engineering, not production engineering, so the whole craft is one of learning and managing complexity. The book distills the discipline into two pillars — *experts at learning* (iteration, feedback, incrementalism, empiricism, experimentation) and *experts at managing complexity* (modularity, cohesion, separation of concerns, abstraction, loose coupling) — supported by the practical tools of testability, deployability, speed, controlling the variables, and continuous delivery. The data is unambiguous: teams that adopt these ideas ship higher-quality software faster, while ordinary "software engineering" practice (waterfall, change boards, hero-programmers, undocumented "strategy groups") wastes the entire category. Apply this whenever you are choosing architecture, writing code, organizing a team, evaluating a process change, or selecting a technology.

---

## Best Practices by Topic

### 1. The Definition of Software Engineering

**Principle:** Engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems. "Software engineering" is that same discipline applied to software.

**Do:**
- Adopt Farley's working definition verbatim: *"Software engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software."* Every word is deliberate — empirical (grounded in observation), scientific (structured reasoning), practical (not theoretical), efficient (minimizing waste), economic (constrained by real-world limits).
- Distinguish *engineering != code*: engineering is the whole process — process, tools, culture, philosophy — not just the output.
- Apply the four-step scientific method to every change: **Characterize → Hypothesize → Predict → Experiment**.
- Treat shipping better software faster as the only valid success criterion; if your practice does not improve outcomes, change the practice.

**Don't:**
- Don't equate "engineering" with bureaucracy or ceremony — those are the opposite of engineering ("If when I say *engineering* it makes you think bureaucracy, please read this book and think again.").
- Don't confuse software engineering with computer science — chemistry is to chemical engineering as computer science is to software engineering.
- Don't reach for mathematical proof (formal methods) when iteration + tests will do — math is too rigid once concurrency, real I/O, or complex domains intrude.
- Don't accept "no silver bullet" (Brooks 1986) as an excuse for stagnation: the anomaly is that **hardware** is staggeringly fast, not that software is slow.

> "If our 'software engineering' practices don't allow us to build better software faster, then they aren't really engineering, and we should change them!"
*Ref: Modern_Software_Engineering.md — "1. Introduction"*

---

### 2. Production Is Not Our Problem — Software Is Design Engineering

**Principle:** For digital systems, *production is automatic, push-button, essentially free*. The hard problem is **design**, which means waterfall-style "production lines for software" are a category error.

**Do:**
- Treat every project as discovery and exploration first; the activity you are paying for is design.
- Apply the techniques of *exploration* (modeling, simulation, iteration), not the techniques of *mass production*.
- Use mathematical models where they help, then **test the things you build** — like SpaceX pressurizing Starship prototypes to destruction even after crunching the numbers.
- Recognize that "the models we create as software, our computer simulations of a problem, are our product." Your simulation **is** the real thing; verify it directly.

**Don't:**
- Don't let industrial-age reflexes push you into plan-driven, phase-gated processes for software.
- Don't use a manufacturing metaphor (e.g., "production line," "factory," "workforce") to justify heavy process — Glenn Vanderburg: *"In other disciplines, 'engineering means stuff that works.'… in software, almost the opposite has become true."*
- Don't treat outputs as more important than discovery. "Software development, unlike all physical production processes, is wholly an exercise in discovery, learning, and design."

> "Production is not our problem. This makes our discipline unusual."
*Ref: Modern_Software_Engineering.md — "Production Is Not Our Problem", "Design Engineering, Not Production Engineering"*

---

### 3. The Limits of Craft — Why Precision and Scalability Matter

**Principle:** Craft is bounded by human capability (≈ 1/10 mm precision, perceptual cycles ≈ 13 ms); engineering scales by delegating precision to machines. Software is run on machines that process ~3 billion operations/sec, so any practice that limits verification to human-scale perception samples reality at 1:39,000,000.

**Do:**
- Exploit the machine: one Farley team ran ~30,000 test cases in 2 minutes; Google claims ~104,166 tests/minute (150 M/day). Use that capacity.
- Treat engineering as the *scalable, more effective offspring of craft* — not its replacement.
- Make precise measurement (microseconds, even nanoseconds) possible by isolating the unit under test.
- Recognize that craft-based production is fundamentally low-quality compared to machine-based production.

**Don't:**
- Don't limit quality to human-scale perception of correctness — that is a 39-million-to-one sampling miss.
- Don't romanticize handcraft while ignoring that "even the most masterful of craftspeople will create items with only human levels of precision and tolerance."
- Don't let "creativity" be an excuse to reject measurement; engineering amplifies creativity, it doesn't suppress it.

> "The art of programming is the art of organizing complexity." — Dijkstra
*Ref: Modern_Software_Engineering.md — "The Limits of 'Craft'", "Precision and Scalability"*

---

### 4. DORA Metrics — Stability & Throughput Are Not in Tension

**Principle:** The best available measurement framework for software teams comes from the DORA / State of DevOps research. Two dimensions — **stability** and **throughput** — predict team and organizational performance. Counterintuitively, optimizing for throughput *also* improves stability; speed and quality are positively correlated in the data.

**Do:**
- Track **Stability** with `Change Failure Rate` and `Time to Restore Service`.
- Track **Throughput** with `Lead Time for Changes` and `Deployment Frequency`.
- Use stability + throughput as a "fitness function" to evaluate any process, org, or technology change ("did this move the dial?").
- Apply as evidence: *"If your stability and throughput numbers are good, your technical delivery is good. So if you are not successful with good stability and throughput, your product ideas or business strategy is at fault."*

**Don't:**
- Don't reach for vanity metrics (lines of code, story points, test coverage without assertion count) — they're not correlated with success.
- Don't trade "speed vs quality" as a binary — the data shows this is false ("better software faster" beats "worse software slower").
- Don't add change-approval boards (CABs) hoping to improve stability — Accelerate research shows CABs *hurt* lead time, deployment frequency, and restore time and have **no** correlation with change fail rate.

> "We found that external approvals were negatively correlated with lead-time, deployment frequency, and restore-time, and had no correlation with change fail rate."
*Ref: Modern_Software_Engineering.md — "The Importance of Measurement", "Applying Stability and Throughput"*

---

### 5. The Ten Foundational Ideas (Farley's Model)

**Principle:** A discipline grounded in just ten ideas — five about *learning*, five about *managing complexity* — and they apply universally.

```text
EXPERTS AT LEARNING              EXPERTS AT MANAGING COMPLEXITY
─────────────────────            ──────────────────────────────────
1. Iteration                     6. Modularity
2. Feedback                      7. Cohesion
3. Incrementalism                8. Separation of Concerns
4. Empiricism                    9. Abstraction (Information Hiding)
5. Experimentation              10. Loose Coupling
```

**Do:**
- Treat the list as a coherent, mutually-reinforcing framework — "applying any one principle tends to reinforce the others."
- Use the tools (testability, deployability, speed, controlling the variables, continuous delivery) as practical levers for these ten ideas.
- Reach for the framework when you don't know the answer: *"This book provides mental tools that help us structure our thinking when we don't have the answers."*

**Don't:**
- Don't treat the principles as a checklist or a methodology — they are a way of thinking.
- Don't pick one principle in isolation and apply it dogmatically; the principles only pay off together.
- Don't confuse "no recipe" with "no discipline" — there is a real framework, you must apply it thoughtfully.

> "These are not new ideas. The power comes from organizing them into a coherent, intellectually consistent framework and applying them deliberately as the guiding principles of software development."
*Ref: Modern_Software_Engineering.md — "The Foundations of a Software Engineering Discipline", "Experts at Learning", "Experts at Managing Complexity"*

---

### 6. Iteration as a Defensive Design Strategy

**Principle:** Iteration is "a procedure in which repetition of a sequence of operations yields results successively closer to a desired result." Working iteratively *flattens the cost-of-change curve* (Dan North's framing).

**Do:**
- Make every change releasable (the CD principle): "each change is finished, because it is releasable."
- Adopt the Red-Green-Refactor cycle as the fine-grained, code-level instantiation of iteration.
- Use TDD micro-iterations to keep your options open: *"At each point in the process, I can re-evaluate and change my mind and the direction of my design and code easily. I keep my options open!"*
- Embrace Kent Beck's discipline: "Embrace change."

**Don't:**
- Don't plan to "build the system to throw away — because you will anyway" (Brooks). Iterate instead.
- Don't assume you can get everything right up front: *"if we only think/work hard enough, we can get things right at the beginning"* is a waterfall fantasy.
- Don't conflate waterfall with "we should be diligent"; iteration is the more diligent, more professional approach for software.

> "Approaches that are so inefficient that improving them by an order of magnitude is perfectly possible. Waterfall, when applied to software development, is such a candidate."
*Ref: Modern_Software_Engineering.md — "4. Working Iteratively", "Practical Advantages of Working Iteratively", "Iteration as a Defensive Design Strategy"*

---

### 7. Feedback Loops — Prefer the Earliest, Fastest Signal

**Principle:** Without feedback, iteration is just repetition. Earlier feedback is always cheaper and more effective — from milliseconds (compiler/IDE) to seconds (unit tests) to minutes (CI) to days (production).

**Do:**
- Use a layered feedback stack in order: IDE syntax/type checks → unit test in your area → full local suite → CI commit stage → acceptance tests → production telemetry.
- Aim for sub-second feedback on coding changes ("I generally take a test-driven approach… and run it in order to see it fail").
- Adopt *shift-left* / "fail fast" — discover compile errors before unit tests, unit tests before integration tests.
- Use telemetry from production to feed product design, not just diagnostics.

**Don't:**
- Don't rely on a separate QA team discovering problems weeks later — that's not feedback, it's archaeology.
- Don't treat "feed back to users" as a release-only event; closing the production loop is the *real* value of continuous delivery.
- Don't pretend that subjective judgement of team velocity is a substitute for stability/throughput metrics.

> "Continuous delivery and DevOps practitioners sometimes refer to this process of preferring early failures as *shift-left*, though I prefer the less obscure 'Fail fast!'"
*Ref: Modern_Software_Engineering.md — "5. Feedback", "Feedback in Coding", "Feedback in Integration", "Prefer Early Feedback"*

---

### 8. Continuous Integration vs Feature Branching (CI Is Definitional)

**Principle:** CI is "merging all developers' working copies to a shared mainline several times a day." Feature branching, by definition, *isolates* change; CI *exposes* it. They are not compatible — one defers the integration pain, the other pays it incrementally.

**Do:**
- Merge to trunk at least daily; commit in atomic steps that don't break the build.
- Use shared mainline + feature flags (trunk-based development) over long-lived branches.
- Make your CI pipeline the definitive evaluation of releasability.

**Don't:**
- Don't argue that "merge tools are good enough." Merge tools can combine code that *behaves* badly (e.g., two independent "increment by 1" changes collapsing to "increment by 2") — "merging code is not necessarily the same as merging behavior."
- Don't believe that long-lived branches reduce pain — they convert a known small pain into a larger, unpredictable merge.

> "In basic, definitional terms, CI and FB then are not really compatible with each other. One aims to expose change as early as possible; the other works to defer that exposure."
*Ref: Modern_Software_Engineering.md — "Feedback in Integration"*

---

### 9. Incrementalism & Its Tools (Version Control, Tests, CI)

**Principle:** Incrementalism is about building value progressively — each small step adds real, working value. It is enabled by modularity and protected by three tools: **version control**, **automated testing**, and **continuous integration**.

**Do:**
- Decompose work so each increment *adds value* (incremental), then *refine the increment* (iterative). You need both.
- Couple incrementalism with refactoring tools (IDE "extract method," "introduce parameter") to make step sizes near-zero.
- Treat "changing things safely" as a defensive design strategy: small, reversible, well-versioned changes lose little when invalidated.

**Don't:**
- Don't confuse velocity ("throughput of changes") with "amount of typing." Real progress requires limiting scope, not typing faster.
- Don't make changes without version control — the ability to back out is what makes increments small.
- Don't attempt organizational re-engineering in leaps; extend modularity to "Organizational Incrementalism" — small, reversible changes to team structure and process.

> "A test-driven approach to automated testing demands that we create mini executable specifications for the changes that we make to our systems… Since *testable code* is modular with a good separation of concerns, that means automated testing creates a positive feedback loop that enhances our ability to design better systems."
*Ref: Modern_Software_Engineering.md — "6. Incrementalism", "Importance of Modularity", "Organizational Incrementalism", "Tools of Incrementalism"*

---

### 10. Limiting the Impact of Change — Ports & Adapters and Speed

**Principle:** Two strategies make incremental change safe: **decompose the system into more independent pieces** (Ports & Adapters) or **make the feedback so fast** that integration friction disappears (CI/CD).

**Do:**
- Define a **port** at every interface between two components you want to decouple; write an **adapter** that translates I/O so the underlying implementation can change safely.
- Treat ports as integration points deserving *more care* than the surrounding code — "these cause more pain when things need to change here."
- Use the speed of CI feedback as the other half of the equation; combining the two lets teams "safely make incremental progress in this part of the code and then deal with the significantly trickier and costly changes in the agreed-upon protocols of information exchange between components."

**Don't:**
- Don't share protocols across teams without versioning them — protocols change more rarely than implementations only if you *make* them change rarely.
- Don't underestimate the value of velocity alone: "if we only discover that I broke something months later, then the implications may be serious… If we find out within a few minutes of me making the change, then it is no big deal."

> "Ports & Adapters is just as useful, probably more useful, for binary information sent through a socket as it is structured text sent via a REST API call."
*Ref: Modern_Software_Engineering.md — "Limiting the Impact of Change"*

---

### 11. Incremental Design — Work Without a Complete Answer

**Principle:** Design should evolve incrementally alongside the code at the *last responsible moment* — when we have the most information. Design is not big-up-front; it is a continuously updated map of the territory we are exploring.

**Do:**
- Treat all complex systems as the *product of evolution*, not of genius: "Complex systems don't spring fully formed from the mind of some genius creator."
- Acknowledge change as inevitable: "Complaints that 'they' always get the requirements wrong are one symptom of this. Yes, no one knows what to build at the start!"
- Use rules of thumb to police design quality — e.g., no functions > ~10 lines, < ~4 params (Farley's, not gospel).
- Aim to "optimize for thinking, not for typing."

**Don't:**
- Don't ask permission to do a good job — that is your *duty of care*.
- Don't trust big-up-front design — even the most thorough analysis doesn't survive first contact with reality.
- Don't over-engineer defensively — YAGNI applies, but so does change-readiness via abstraction and tests.

> "If your code is hard to change, it is low quality, whatever it does!"
*Ref: Modern_Software_Engineering.md — "Incremental Design", "The Lure of the Plan"*

---

### 12. Empiricism — Don't Fool Yourself

**Principle:** Empiricism means grounding decisions in observation, not in theory, authority, or pattern-matching. The most dangerous failure mode is *jumping to conclusions that "obviously" explain the symptoms* — which is how a "weird messaging failure" can waste hours because everyone was sure it was the messaging code.

**Do:**
- Write down facts first; check the hypothesis against them.
- Be skeptical of every idea, even your own: *"It doesn't matter who has an idea, how much we would like the idea to be true… if the idea is bad, it is bad."*
- Apply Feynman's first principle: *"you must not fool yourself — and you are the easiest person to fool."*
- Distinguish **empirical** (grounded in observed reality) from **experimental** (deliberate test of hypothesis); experiment without empiricism is just expensive guessing.

**Don't:**
- Don't treat correlation of symptoms as proof of cause — *"It was obvious that we must have committed something that broke the build. Instead, we joined together various facts and jumped to the wrong conclusion because there was a sequence of events that led us down the wrong path."*
- Don't confuse confidence with evidence; let data, not intuition, drive decisions.
- Don't let your conscious "story" overwrite what the logs say.

> "Science works! Make a hypothesis. Figure out how to prove or disprove it. Carry out the experiment. Observe the results and see they match your hypothesis. Repeat!"
*Ref: Modern_Software_Engineering.md — "7. Empiricism", "'I Know That Bug!'", "Avoiding Self-Deception"*

---

### 13. The Cost of Concurrency — An Empirical Experiment

**Principle:** Intuition about performance is wrong without measurement. Farley's team *measured* the cost of multi-threaded integer increment and discovered locks are extraordinarily expensive.

**Do:**
- Measure before optimizing. *"If you are really interested in the performance of your code, don't guess about what will be fast and what will be slow; measure it!"*
- Prefer single-threaded algorithms where work doesn't decompose cleanly; reserve concurrency for trivially parallelizable work.
- Account for Amdahl's law: *"Amdahl's law shows that there is a harsh limit to the number of concurrent operations that make sense, unless they are wholly independent of one another."*
- Read CPU cache behavior as the primary performance lever, not clock speed; avoid cache misses.

**Don't:**
- Don't parallelize work that has to be joined back together — costs dominate gains.
- Don't assume modern compilers/CPUs need complex code; performance "is an excuse for a big ball of mud."
- Don't trust "average" latency — outliers dominate high-frequency systems (2 ms *is* the limit, not the mean).

**Code (the experiment that disproves the parallelism-is-always-faster myth):**
```text
Operation: increment a 64-bit int 500 million times

Single thread                                  300 ms
Single thread + lock                       10,000 ms
Two threads + lock                        224,000 ms
Single thread + CAS (compare-and-swap)       5,700 ms
Two threads + CAS                         30,000 ms
```
*Ref: Modern_Software_Engineering.md — "Inventing a Reality to Suit Our Argument"*

---

### 14. Experimentation — Feedback + Hypothesis + Measurement + Control Variables

**Principle:** Being experimental is the practical application of the scientific method: structure work around testing hypotheses and *controlling the variables*.

**Do:**
- Treat every work stream as a series of small experiments; even a TDD cycle is one.
- Always predict the specific failure mode of a test before running it ("expected x but was 0…") — this is a tiny application of the scientific method.
- Defer guesswork to hypotheses; institutionalize it so others can challenge it.
- Invest in A/B-tested measurement rigs: the C++/Scala experiment at Farley's previous team shaved a 9.5-hour build to 52 minutes and immediately improved both stability and frequency of green builds.

**Don't:**
- Don't debate tools by faith; run experiments. *"Why not do a little trial and measure the stability and throughput of the result?"*
- Don't trust "metrics" without checking what they actually measure — Farley saw a team paid bonuses on 80% coverage, where 25% of the tests had no assertions.
- Don't ignore measurement noise — averages hide outliers; latencies must be characterized by *the worst case that matters*.

> "The 'war story' in the box 'The Need for Speed'… we had no other changes in organization, process, or tooling, beyond speeding up the build… Making no other change than improving the speed of the feedback gave the teams the tools that they needed to fix the underlying instability."
*Ref: Modern_Software_Engineering.md — "8. Experimental", "What Does 'Being Experimental' Mean?", "Feedback", "Hypothesis", "Measurement"*

---

### 15. TDD — A Talent Amplifier, Not Just a Test Technique

**Principle:** Test-Driven Development (Red-Green-Refactor) is the most powerful design tool Farley has used, because *the act of writing the test forces the public interface into existence*, which drives modularity, cohesion, separation of concerns, and loose coupling.

**Do:**
- Always write the failing test first. If a test passes before any code exists, your test is wrong.
- Predict the *exact* failure message before running — that closes the loop on "is the test actually testing?"
- Use TDD pressure to expose design smells: *"If our tests are difficult to write, it means that our design is poor."*
- Keep tests as the executable specification — *"TDD doesn't make bad software developers great, but it does make 'bad software developers' better and 'great software developers' greater."*

**Don't:**
- Don't conflate TDD with "unit tests written after the code"; that's a fundamentally different practice and largely *worsens* design.
- Don't accept "TDD didn't work" without checking whether the team actually wrote tests before code.
- Don't use tests to break encapsulation after the fact; write the spec *first* and let it guide the abstraction.

> "TDD was not a new idea when Kent Beck described it in his book in the late 1990s. Alan Perlis had described something similar at the NATO Software Engineering Conference in 1968."
*Ref: Modern_Software_Engineering.md — "Feedback in Design", "Driving High Cohesion with TDD"*

---

### 16. Modularity — Hallmarks, Hall of Shame

**Principle:** A modular system has clear boundaries, interfaces, and limited dependencies. Modularity is fractal — it applies at every scale from functions to services. Most code is *not* modular; it is written as a recipe.

**Do:**
- Establish build-time "guiderails" in the commit stage: reject methods > 20–30 lines, signatures with > 5–6 params. "Whatever the time pressure, writing bad code is never a time-saver!"
- Add tests as a forcing function: *"It is simply not possible to test a system… that is not, in some way, modular."*
- Treat services as modules — independent deployable units of code.
- Use deployability as the boundary detector: "the scope of evaluation should always be an *independently deployable unit of software*."

**Don't:**
- Don't confuse "I have files" with "I have modules." A bag of unrelated code in a file is not modular.
- Don't make the modularity of your design stop at the service boundary; each class, method, function should also be cohesive.
- Don't treat microservices as a magic bullet; they are an *organizational-scaling pattern*, valuable only when you need to scale teams.

> "Modularity as a design idea is fractal. It is more than only the 'modules,' whatever their form… At its heart, the idea that we must retain our ability to change code and systems in one place, without worrying about the impact of those changes elsewhere."
*Ref: Modern_Software_Engineering.md — "9. Modularity", "Hallmarks of Modularity", "Modularity at Different Scales"*

---

### 17. Cohesion — Put Related Things Together

**Principle:** Cohesion is the degree to which elements within a module belong together. Naive cohesion ("everything is in one function!") is *bad*; it just hides the mess. Real cohesion means keeping concepts that change together close together and forcing costs of complexity into structured form.

**Do:**
- Aim for one class, one thing; one method, one thing.
- Refactor "load/process/store" recipes into separate, testable concerns (read, sort, store).
- Treat low cohesion as an early warning sign: *"If you have ever read a piece of code and thought 'I don't know what this code does,' it is probably because the cohesion is poor."*
- Allow that *very* low cohesion (a listener/observer model) trades clarity for flexibility — choose contextually.

**Don't:**
- Don't optimize for less code; *less code* is not the same as *simpler code*.
- Don't add logging or persistence into the business module "just this once" — each addition erodes cohesion.
- Don't pick abstractions based on aesthetics; "the choice of abstraction between these two is really a design choice that should be driven by the context in which this code exists."

**Code — Listing 10.1 *Really Bad Code, Naively Cohesive*:**
```java
public class ReallyBadCohesion
{
    public boolean loadProcessAndStore() throws IOException
    {
        String[] words;
        List<String> sorted;
        try (FileReader reader = new FileReader("./resources/words.txt"))
        {
            char[] chars = new char[1024];
            reader.read(chars);
            words = new String(chars).split(" |\0");
        }
        sorted = Arrays.asList(words);
        sorted.sort(null);
        try (FileWriter writer = new FileWriter("./resources/test/sorted.txt"))
        {
            for (String word : sorted)
            {
                writer.write(word);
                writer.write("\n");
            }
            return true;
        }
    }
}
```

**Code — Listing 10.2 *Bad Code, Mildly Better Cohesion*:**
```java
public class BadCohesion
{
    public boolean loadProcessAndStore() throws IOException
    {
        String[] words = readWords();
        List<String> sorted = sortWords(words);
        return storeWords(sorted);
    }
    private String[] readWords() throws IOException
    {
        try (FileReader reader = new FileReader("./resources/words.txt"))
        {
            char[] chars = new char[1024];
            reader.read(chars);
            return new String(chars).split(" |\0");
        }
    }
    private List<String> sortWords(String[] words)
    {
        List<String> sorted = Arrays.asList(words);
        sorted.sort(null);
        return sorted;
    }
    private boolean storeWords(List<String> sorted) throws IOException
    {
        try (FileWriter writer = new FileWriter("./resources/test/sorted.txt"))
        {
            for (String word : sorted)
            {
                writer.write(word);
                writer.write("\n");
            }
            return true;
        }
    }
}
```
*Ref: Modern_Software_Engineering.md — "10. Cohesion", "A Basic Reduction in Cohesion", "Context Matters"*

---

### 18. Cohesion Examples — Separating Essential and Accidental

**Principle:** Walking the same problem (add item to cart) through levels of cohesion shows how separating essential from accidental complexity moves the needle on quality.

```python
def add_to_cart1(self, item):
    self.cart.add(item)
    conn = sqlite3.connect('my_db.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO cart (name, price) values (item.name, item.price)')
    conn.commit()
    conn.close()
    return self.calculate_cart_total()

def add_to_cart2(self, item):
    self.cart.add(item)
    self.store.store_item(item)
    return self.calculate_cart_total()

def add_to_cart3(self, item, listener):
    self.cart.add(item)
    listener.on_item_added(self, item)
```

**Do:**
- Prefer `add_to_cart2` or `add_to_cart3` over `add_to_cart1` — they hide accidental complexity (storage) from the essential domain (cart).
- Use `add_to_cart3` (event/observer) when the storage and total-calculation truly belong to other concerns; it is "the most flexible solution of all."
- Version 2 is also defensible — the choice is contextual and "should be driven by the context in which this code exists."

**Don't:**
- Don't mix business logic with database code in a single method — `add_to_cart1` is "very poor code, even at this essentially trivial scale."
- Don't pick abstraction level on faith; let the trade-offs (transactional needs, observers' guarantees) decide.
*Ref: Modern_Software_Engineering.md — "Costs of Poor Cohesion"*

---

### 19. Cohesion in Different Scales (Python Class Example)

**Principle:** Cohesion shows up the same way at micro scale: a class with two unrelated members per method has poor cohesion, no matter how neatly it parses.

**Code — Listing 10.3 *More Poor Cohesion*:**
```python
class PoorCohesion:
    def __init__(self):
        self.a = 0
        self.b = 0
    def process_a(x):
        a = a + x
    def process_b(x):
        b = b * x
```

**Code — Listing 10.4 *Better Cohesion*:**
```python
class BetterCohesionA:
    def __init__(self):
        self.a = 0
    def process_a(x):
        a = a + x

class BetterCohesionB:
    def __init__(self):
        self.b = 0
    def process_b(x):
        b = b * x
```

**Do:**
- Use the class-level rule "one class, one thing" — pair fields with their methods.
- Recognize that improving cohesion often *also* improves modularity and separation of concerns; the three are intertwined.

**Don't:**
- Don't accidentally couple unrelated state just because they're "near" each other.
*Ref: Modern_Software_Engineering.md — "How to Achieve Cohesive Software"*

---

### 20. Separation of Concerns — "One Class, One Thing"

**Principle:** Separation of Concerns is the most powerful design principle for Farley. It is the tool that "reminds me to keep my focus small." The most useful expression is the *summary level of abstraction* test: each scope should be at one level of abstraction.

**Do:**
- Strip storage/persistence/db calls out of business methods and into your abstractions.
- Use the "and" smell: "Having an 'and' in the description of a class or a method is a warning sign. It says that I have two concerns rather than one."
- Make every change's "essential complexity" stand out clearly from its "accidental complexity."

**Don't:**
- Don't claim to have applied SoC when your method has multiple *levels* of abstraction in two adjacent lines.
- Don't accept hard-coded filenames as "the way the API was" — that is accidental complexity leaking into your domain logic.

> "If you put something in a real shopping cart, you don't then need to 'persist' it!"
*Ref: Modern_Software_Engineering.md — "11. Separation of Concerns", "What Is an API?"*

---

### 21. Dependency Injection — The Pressure for Modularity

**Principle:** Dependency injection is the single most effective tool at smaller scales to provide pressure on code to be composed of small pieces. It is the practical mechanism that lets TDD produce modular code.

**Do:**
- Inject every dependency a piece of code needs — including storage, listeners, loggers, clocks.
- Use constructor injection for required collaborators; consider parameter injection for "one-off" collaborators like listeners.
- Treat DI as a *design* tool, not a framework. "Dependency injection is something that you can do in most languages… natively, and it is a powerful approach to design. I have even seen it used, to very good effect, in Unix shell scripts."

**Don't:**
- Don't mix version 1 (`create your own dependencies`) with a microservice mindset; that approach is inflexible by design.
- Don't confuse DI with "use Spring/Hilt/etc." — the pattern is the discipline; the framework is optional.

> "At smaller scales, dependency injection is the most effective tool to provide pressure on our code that encourages us to create systems composed of many small pieces. The dependencies are the calipers, the points of measurement, that we can inject into our system to achieve a more thoroughly testable outcome."
*Ref: Modern_Software_Engineering.md — "Dependency Injection"*

---

### 22. Separating Essential vs Accidental Complexity — Java Listing

**Principle:** Fred Brooks' essential vs accidental distinction is the foundation for separating concerns. Essential complexity is the problem; accidental complexity is everything the computer forces on you.

**Code — Listing 11.2 *Separating Accidental and Essential Complexity*:**
```java
public interface Accidental
{
    String[] readWords() throws IOException
    boolean storeWords(List<String> sorted) throws IOException
}
public class Essential
{
    public boolean loadProcessAndStore(Accidental accidental) throws IOException
    {
        List<String> sorted = sortWords(accidental.readWords());
        return accidental.storeWords(sorted);
    }
    private List<String> sortWords(String[] words)
    {
        List<String> sorted = Arrays.asList(words);
        sorted.sort(null);
        return sorted;
    }
}
```

**Do:**
- Name the accidental-complexity side honestly (`Accidental`) — the naming makes the violation visible.
- Promote "what should this code know?" to a first-class design question.

**Don't:**
- Don't bury SQL/IO in business methods — let the compiler enforce that the essential side has no knowledge of accidental reality.
*Ref: Modern_Software_Engineering.md — "Separating Essential and Accidental Complexity"*

---

### 23. Listening to the Code — DDD-Driven Refactor

**Principle:** Code tells you when you've separated concerns wrongly. Farley's battleship `GameSheet` had growing pain because it owned *both* positioning and rules. Extracting `Rules` was the fix.

**Code — Listing 11.4 *Missing a Concept* (problem):**
```python
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
```

**Code — Listing 11.5 *Listening to the Code* (refactored):**
```python
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

**Do:**
- Treat test growth and "what does this class actually do?" as design feedback.
- Use Bounded Contexts to identify coarse-grained modules and let the language of the domain name the abstractions.
- Adopt a low tolerance for complexity: "as soon as it begins to feel like hard work, you should pause and start looking for ways to simplify and clarify the part in front of you."

**Don't:**
- Don't ignore creeping "and" responsibilities inside a class — every new concern deserves a name and a home.
*Ref: Modern_Software_Engineering.md — "Importance of DDD"*

---

### 24. Ports & Adapters — A Concrete Example

**Principle:** Even tiny methods should hold a *consistent level of abstraction*. The S3 example shows the difference between two alien abstraction levels and one consistent level.

**Code — Listing 11.6 *Storing a String in S3* (mixed abstraction):**
```java
void doSomething(Thing thing) {
    String processedThing = process(thing);
    s3client.putObject("myBucket," "keyForMyThing," processedThing);
}
```

**Code — Listing 11.7 *Storing a String in S3 via a Port* (clean):**
```java
void doSomething(Thing thing) {
    String processedThing = process(thing);
    store.storeThings("myBucket," "keyForMyThing," processedThing);
}
```

**Do:**
- Always translate information that crosses between bounded contexts (Eric Evans).
- Treat the entry point to a service as a small defensive barrier that validates inputs and assembles outputs.
- Even within a single class, prefer consistent abstraction levels — "even if we don't yet know the details of how something will be communicated, stored, or interacted with in general, we can write code and make progress."

**Don't:**
- Don't pass raw HTTP/XML/JSON across a service boundary and have downstream code parse it; translate first.
- Don't treat ports as overkill for small systems — "even where you don't make the port polymorphic, this code is better!"

> "Each service or module should have its own view of the world and should defend that perspective. If information is sent that breaks that view, that is a serious problem for the code."
*Ref: Modern_Software_Engineering.md — "Ports & Adapters", "When to Adopt Ports & Adapters"*

---

### 25. Abstraction as Design-by-Contract (TDD Outside-In)

**Principle:** Because TDD writes the spec first, the test *is* the abstraction. If your tests are fragile, your abstractions are fragile — that is the diagnostic that improves design.

**Do:**
- Write tests that describe behavior without leaking implementation; if your spec needs implementation details, your abstraction is broken.
- Use this as a deliberate design lever — "I need to think harder about better abstractions."
- Aim to maintain a stable, well-defined abstraction even when the underlying implementation changes.

**Don't:**
- Don't write tests after code and call it TDD. "Unit testing, after the code is written, encourages us to cut corners, break encapsulation, and tightly couple our test to the code that we already wrote."
- Don't excuse "all abstractions are leaky" as a reason not to bother — "Computers and software would not exist without abstraction."
*Ref: Modern_Software_Engineering.md — "Improving Abstraction Through Testing"*

---

### 26. Information Hiding, Leaky Abstractions, Modeling

**Principle:** All non-trivial abstractions are leaky (Joel Spolsky). That doesn't invalidate them — it requires you to design around the leaks.

**Do:**
- Know your leaks: GC-pause variance, RAM-vs-cache latency, network synchrony illusions, exceptions leaking from frameworks into business code.
- Maintain consistent abstraction level: an HTML error from a remote service is OK; an HTML error from a business validator is a leak.
- Use George Box's mantra: "All models are wrong, some models are useful." Aim for usefulness, not truth.
- Distinguish "always leaks" (cache timing, GC pauses) from "designed leaks" (NullPointerException from a business method).

**Don't:**
- Don't use HTML/business exceptions to mask the boundary between technical and business failure.
- Don't treat "the world is leaky" as license for sloppy abstraction.
*Ref: Modern_Software_Engineering.md — "Leaky Abstractions"*

---

### 27. Picking Abstractions — Be Specific, Not Generic

**Principle:** The best abstractions come from the **problem domain**, not the implementation. Generic to the point of useless (`Object`) is just as bad as overly specific (`ArrayList<String>`).

**Code — Listing 12.3 *Prefer to Hide Information*:**
```java
public ArrayList<String> doSomething1(HashMap<String, String> map);
public List<Sting> doSomething2(Map<String, String> map);
public Object doSomething3(Object map);
```

**Do:**
- Prefer the middle path — `List<String>` over `ArrayList<String>`, `Map<String,String>` over `HashMap<String,String>`.
- Hide information unless you have a specific reason to expose it.
- Use event storming (Alberto Brandolini) to discover natural lines of abstraction in the domain.

**Don't:**
- Don't pick `Object` for "maximum abstraction" — generic to the point of being unhelpful.
- Don't import all-encompassing frameworks that impose their programming model and resist your own seams.

> "Modeling the problem domain will give your design some guide-rails."
*Ref: Modern_Software_Engineering.md — "Picking Appropriate Abstractions", "Abstractions from the Problem Domain"*

---

### 28. Abstracting Accidental Complexity — The Listener Pattern Refined

**Principle:** Once accidental complexity is hidden behind an abstraction, you can still be confronted by leaks (e.g., "what if storage fails?"). Farley's response is to *let the abstraction fail gracefully* — return a boolean, or shift to a guaranteed-delivery event stream.

**Code — Listing 12.2 *Reducing the Abstraction Leak*:**
```python
def add_to_cart2(self, item):
    if (self.store.store_item(item))
        self.cart.add(item)
    return self.calculate_cart_total();
```

**Do:**
- For transactional needs, let the accidental side return a Boolean success/failure and keep the abstraction coarse.
- For non-transactional needs, lean into `on_item_added` semantics with retry-on-failure and accept the extra infrastructure complexity.
- Treat "thinking like an engineer" as the habit of modeling the failure modes of your own abstractions.

**Don't:**
- Don't let the accidentals leak through domain exceptions or error codes into your essential complexity.
*Ref: Modern_Software_Engineering.md — "Abstract Accidental Complexity"*

---

### 29. Isolate Third-Party Code — Always Behind a Facade

**Principle:** Allow *only* your language's standard library inside your domain code. Everything else goes behind your own facade.

**Do:**
- Use your own thin wrapper around third-party APIs (especially DB drivers, ORM frameworks, HTTP clients).
- Be wary of all-encompassing frameworks that impose their programming model — they tend to defeat testability and audit-ability of your design.
- Tolerate duplication between services if it preserves independence (see DRY §37).

**Don't:**
- Don't import `sqlite3` (or your database driver) into your domain methods.
- Don't treat "third-party" libraries as free — every one is a coupling point waiting to break.
*Ref: Modern_Software_Engineering.md — "Isolate Third-Party Systems and Code"*

---

### 30. Coupling — The Nygard Model

**Principle:** "Coupling" sounds binary but is multi-dimensional. Michael Nygard's model gives five kinds, each fixable by design:

| Type            | Effect                                                          |
|-----------------|-----------------------------------------------------------------|
| **Operational** | A consumer can't run without a provider                         |
| **Developmental** | Changes in producers and consumers must be coordinated        |
| **Semantic**    | Change together because of shared concepts                      |
| **Functional**  | Change together because of shared responsibility                |
| **Incidental**  | Change together for no good reason (e.g., breaking API changes) |

**Do:**
- Recognize which kind you're facing — operational coupling via deployment plumbing, developmental coupling via shared libraries, semantic coupling via shared schema, functional coupling via split responsibilities.
- Eliminate incidental coupling aggressively — versioning APIs removes the most pointless coupling.
- Plan for the cost of *each* kind separately.

**Don't:**
- Don't treat "loose coupling" as one switch; each dimension needs its own response.
- Don't accept that "the components of your software system" must "communicate" — design for asynchronous or self-sufficient operation when possible.
*Ref: Modern_Software_Engineering.md — "Loose Coupling Isn't the Only Kind That Matters"*

---

### 31. DRY Is Too Simplistic

**Principle:** DRY is excellent advice within the scope of a single deployment pipeline; it is *often harmful* across pipelines.

**Do:**
- Apply DRY inside a function, service, module, or a single deployment pipeline.
- Encourage duplication *between* services that are independently deployable: "Don't share code between microservices."
- Use the deployment pipeline as the *scope* of canonical representation: "DRY should be the guiding principle within the scope of a deployment pipeline, but should be actively avoided between pipelines."
- Reconsider any "shared library" being added to two services developed by different teams on different cadences.

**Don't:**
- Don't create "one source of truth" across teams if it forces them to coordinate releases.
- Don't assume that removing duplication reduces coupling — *shared dependency* is itself a coupling point.
- Don't translate "duplication" into "harmful dependency" reflexively; ask "does this duplication represent a harmful dependency?"

> "The real question is not 'is this code duplicated?' but 'does this duplication represent a harmful dependency?'"
*Ref: Modern_Software_Engineering.md — "DRY Is too Simplistic"*

---

### 32. Async Communication as a Loose-Coupling Tool

**Principle:** Synchronous distributed calls are an illusion that always fails; asynchronous messaging aligns the abstraction with reality (which is async).

**Do:**
- Treat process boundaries as asynchronous in distributed systems.
- Build communication around events, not request/response, wherever possible.
- Allow Service A to fire an event and move on; let the eventual redelivery/resume logic live in B.

**Don't:**
- Don't call a remote service synchronously and pretend the call is reliable.
- Don't let technical failures (network drop, B down) leak into the business conversation — "this kind of leak can be mitigated significantly by more closely representing what is really going on."

**The Nine Failure Points of Synchronous Communication:**
```text
1. Bug in A
2. A fails to connect to network
3. Message lost in transmission
4. B fails to connect to network
5. Bug in B
6. Connection fails before B responds
7. Response lost in transmission
8. A loses connection before getting response
9. Bug in A's response handling
```
*Ref: Modern_Software_Engineering.md — "Async as a Tool for Loose Coupling"*

---

### 33. Microservices as Organizational Pattern

**Principle:** Microservices are **not** about technology — they are an organizational-scaling pattern. The actual definitions Farley uses:

```text
Microservices are:
  - Small
  - Focused on one task
  - Aligned with a bounded context
  - Autonomous
  - Independently deployable
  - Loosely coupled
```

**Do:**
- Adopt microservices *to scale teams*, not because the marketing is good.
- Make services independently deployable so that teams can ship at their own pace.
- Apply Conway's Law in reverse — your team topology should be a deliberate variable.

**Don't:**
- Don't call something a microservice if you must test it with another service before deploying it. It isn't independently deployable, so it isn't a microservice.
- Don't expect microservices to "fix" coupling problems you haven't designed out — they require genuinely better design upfront.
*Ref: Modern_Software_Engineering.md — "Microservices"*

---

### 34. Decoupling May Mean More Code (and That's OK)

**Principle:** "More code" is not the right way to evaluate design quality. Optimize for *thinking*, not for *typing*.

**Code — Listing 13.2 *Reducing Coupling*:**
```python
def add_to_cart1(self, item):
    self.cart.add(item)
    self.store_item(item)
    return self.calculate_cart_total()

def store_item(self, item):
    conn = sqlite3.connect('my_db.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO cart (name, price) values (item.name, item.price)')
    conn.commit()
    conn.close()
```

**Do:**
- Refuse to optimize for line count; "the kind of unstructured, coupled code in [Listing 13.1] may be fewer lines of code if we are looking at eight lines. If this function was 800 lines, though, it is much more likely that there will be duplication and redundancy."
- Treat "more code" as the cost of making concerns separate, testable, and replaceable.
- Commit to making code *readable* as the primary engineering virtue — readability has a "direct economic impact on the value of that code."

**Don't:**
- Don't reject TDD or DI because "I have to type more." Those programmers "are optimizing for the wrong things."
- Don't confuse clear with concise; "ICanWriteASentenceOmittingSpaces is shorter, but it is also much less pleasant to read!"

> "We should optimize for thinking, not for typing!"
*Ref: Modern_Software_Engineering.md — "Decoupling May Mean More Code"*

---

### 35. Testability — A Diagnostic for Design

**Principle:** Testability is not just verification — it is the *most sensitive diagnostic for design quality* we have. If your code is hard to test, your design is bad.

**Do:**
- Use difficulty-of-testing as a real-time signal to refactor.
- Make testability a *requirement*: design for it from the start, and you'll get modularity, cohesion, separation of concerns, abstraction, and appropriate coupling for free.
- Inject everything — including DB handles, loggers, clocks.

**Don't:**
- Don't accept "we can't unit-test this" as a sentence-ending fact about the world; it is a sentence-ending fact about your design.
- Don't add a test framework and assume you're doing TDD — that's test-after.
*Ref: Modern_Software_Engineering.md — "12. Information Hiding and Abstraction", "14. Tools of an Engineering Discipline — Testability as a Tool"*

---

### 36. The Car/BetterCar Worked Example (Testability Drives Design)

**Principle:** When the test cannot observe internal state, dependency injection fixes both the test and the abstraction — at the same time.

**Code — Listing 14.1 *Simple Car Example* (untestable):**
```java
public class Car {
  private final Engine engine = new PetrolEngine();
  public void start() {
      putIntoPark();
      applyBrakes();
      this.engine.start();
  }
  private void applyBrakes() { }
  private void putIntoPark() { }
}
```

**Code — Listing 14.2 *Test for a Simple Car* (impossible to assert):**
```java
@Test
public void shouldStartCarEngine() {
    Car car = new Car();
    car.start();
    // Nothing to assert!!
}
```

**Code — Listing 14.3 *BetterCar* (testable via DI):**
```java
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
    private void applyBrakes() { }
    private void putIntoPark() { }
}
```

**Code — Listing 14.4 *Test for a BetterCar*:**
```java
@Test
public void shouldStartBetterCarEngine() {
    FakeEngine engine = new FakeEngine();
    BetterCar car = new BetterCar(engine);
    car.start();
    assertTrue(engine.startedSuccessfully());
}
```

**Code — Listing 14.5 *FakeEngine to Help Test a BetterCar*:**
```java
public class FakeEngine implements Engine {
    private boolean started = false;
    @Override
    public void start() {
        started = true;
    }
    public boolean startedSuccessfully() {
        return started;
    }
}
```

**Do:**
- Inject every collaborator you need to verify behavior of.
- Use a real mocking library in production code (Farley wrote `FakeEngine` for clarity).
- Notice that the *injection* made the class more abstract — `Engine`, not `PetrolEngine` — automatically.

**Don't:**
- Don't break encapsulation to test internal state; *inject* a fake/seam instead.
- Don't reach for "backdoor hacks that allow our test to read a private variable."
*Ref: Modern_Software_Engineering.md — "Testability as a Tool"*

---

### 37. Testability at System Edges — Display Example

**Principle:** System edges (UI, hardware, network) are the hardest place to test. Push them to the margins and inject the actor.

**Code — Listing 14.6 *Stuff to Display*:**
```java
public interface Display
{
    void show(String stringToDisplay);
}
public class MyClassWithStuffToDisplay
{
    private final Display display;
    public MyClassWithStuffToDisplay(Display display)
    {
        this.display = display;
    }
    public void showStuff(String stuff)
    {
        display.show(stuff);
    }
}
```

**Code — Listing 14.7 *Testing Stuff to Display*:**
```java
@Test
public void shouldDisplayOutput() throws Exception
{
    Display display = mock(Display.class);
    MyClassWithStuffToDisplay displayable = new MyClassWithStuffToDisplay(display);
    displayable.showStuff("My stuff");
    verify(display).show(eq("My stuff"));
}
```

**Code — Listing 14.8 *Displaying Stuff* (real adapter):**
```java
public class ConsoleDisplay implements Display
{
    @Override
    public void show(String stringToDisplay)
    {
        System.out.println(stringToDisplay);
    }
}
```

**Do:**
- Wrap even simple I/O (screen writes, file I/O) behind a port.
- For web UIs that don't yet have great unit-testing support, write your own DOM facade so logic can be tested without a browser.
- Treat the edge as small as possible, push complexity into a swap-in adapter.

**Don't:**
- Don't tolerate "we have to spin up a real browser" as the unit testing strategy.
- Don't give up on testability at system edges — there is *always* a level of indirection that works.
*Ref: Modern_Software_Engineering.md — "Problems with Achieving Testability"*

---

### 38. Deployability — The Right Scope of Evaluation

**Principle:** A *deployment pipeline* is not "a build script"; it is the *definitive evaluation of releasability* for an *independently deployable unit of software*. If the pipeline says "good," there is no more work.

**Do:**
- Aim for releasable change in < 1 hour from commit; commit-stage feedback in ~5 minutes.
- Treat deployment and configuration as code (infrastructure-as-code).
- Decide between "monolith with everything together" and "modular with independent units" — there is no middle ground.
- Apply the rule: "We can choose to include everything within the scope of our deployment pipeline, or decompose the system into independently deployable units, but nothing else makes sense."

**Don't:**
- Don't define deployability as "after the pipeline, we run more checks." That is undefined scope.
- Don't pretend a system is modular if the deployment process can't actually exercise one piece at a time.
*Ref: Modern_Software_Engineering.md — "Deployability"*

---

### 39. Speed as a Fitness Function

**Principle:** Speed of feedback acts as a *fitness function* that drives every other good practice into place. Just optimize for it iteratively and watch the rest follow.

**Do:**
- Set the < 1 hour releasable target; observe what it forces.
- Treat it as iterative — every improvement to your feedback loop surfaces another invisible tax (slow build, manual test, silo'd team, monolithic deployment).
- Recognize: "If you take an iterative, experimental approach to only improving the speed of feedback in your development process, it acts as a kind of fitness function for all of agile theory, all of lean theory, and all of continuous delivery and DevOps."

**Don't:**
- Don't pick "speed" alone without "quality"; they are correlated.
- Don't accept "fast feedback" as an excuse to skip practice — fast feedback is the *result* of good practice.
*Ref: Modern_Software_Engineering.md — "Speed"*

---

### 40. Controlling the Variables — Determinism Comes from Modularity

**Principle:** Digital systems are deterministic *in the absence of concurrency*. By isolating concurrency and using version-controlled environments, you get testable, deterministic systems.

**Do:**
- Reproduce production *exactly* in test (infrastructure-as-code, recorded inputs replayable). Farley's exchange: "we could record the production inputs and replay them some time later to get the system into precisely the same state in a test environment."
- Treat non-determinism as a *design* problem to be fixed, not a property of computing to be lived with.
- Move concurrency to controlled edges; refuse to allow it inside the unit-of-test.

**Don't:**
- Don't put your performance test on the corporate network and call its results useful — Farley saw exactly that and "all the work to create these tests, and to execute them, was essentially waste."
- Don't trust concurrency as easy; "Reliably testable code is not multithreaded within the scope of a test, except for some very particular kinds of test."
*Ref: Modern_Software_Engineering.md — "Controlling the Variables"*

---

### 41. Continuous Delivery as an Outcome (Not a Mechanism)

**Principle:** Continuous delivery is *not* automated deployment — it is "work so that your software is always in a releasable state." That goal outlasts every specific tool.

**Do:**
- Treat CD as an organizing philosophy that ties testability, deployability, speed, and variance control together.
- Compose target outcomes from the goal: "releasable every hour," "optimize for fast feedback," "reject any change that fails a test."
- Apply even in domains with physical constraints (cars, rockets): the principles hold even if the targets must move.

**Don't:**
- Don't treat "we do CD" as a tool claim; it's an outcome claim.
- Don't enforce one CD recipe across the industry — "If we take these ideas seriously, we can use them to come up with unique, innovative solutions to problems that we haven't encountered before."
*Ref: Modern_Software_Engineering.md — "Continuous Delivery", "Outcomes vs. Mechanisms"*

---

### 42. General Tools — A Checklist for Evaluating Any Technology Choice

**Principle:** Use the book's tools as *qualifiers* for any decision: framework, language, library, third-party service, organizational structure.

**Do:**
- Ask: *Is it deployable?* Can we automate its deployment?
- Ask: *Is it testable?* Can we confirm it does what we need?
- Ask: *Does it allow us to control the variables?* Repeatable, deterministic?
- Ask: *Is it fast enough to fit continuous delivery?*
- Ask: *Does it let us maintain modularity?* Or does it impose a programming model?
- Treat "wrong answer to any of these" as near-disqualifying.

**Don't:**
- Don't adopt tech because it's "cool" without running it through the checklist.
- Don't accept that a third party's model must dominate your design — *"there is always a level of indirection that works."*
*Ref: Modern_Software_Engineering.md — "General Tools to Support Engineering"*

---

### 43. BAPO vs OBAP — Organization Should Be Designed Last

**Principle:** Most firms fix the Organization first, then Business strategy, then Architecture, then Process (OBAP). Farley/JBosch: instead design **Business** first, then **Architecture**, then **Process**, then **Organization** (BAPO).

**Do:**
- Treat organizational structure as a tool, not a constraint.
- Design teams to be small, autonomous, and informationally decoupled — that is the hallmark of high performers.
- Use the engineering principles ("modular, cohesive organizations with a sensible separation of concerns") to design team topology.

**Don't:**
- Don't allow an existing org chart to dictate the architecture of your software. *"The business vision and goals are constrained by organizational structure!"*
- Don't assume adding more people scales output linearly; small teams per QSM research are ~4× more productive per person than teams of 20+.
*Ref: Modern_Software_Engineering.md — "Digitally Disruptive Organizations"*

---

### 44. The Duty of Care — Professionalism Is Not Optional

**Principle:** Quality is part of the job. Cutting corners is not "going faster"; it is going *slower* over time.

**Do:**
- Own the duty of care like a chef owns a clean kitchen: refuse to ship untested, unreviewed, or rushed code.
- Lean on DORA evidence: *"There is **no** trade-off between speed and quality."*
- Push back on estimates that assume bad quality.
- Educate your colleagues: managers usually want better+cheaper, not worse+cheaper; the difference is real.

**Don't:**
- Don't ask for permission to do good work — it's your job.
- Don't let "they made me cut corners" be a story you tell; it's the mark of an unprofessional team.
- Don't preserve a "reverence" for existing code that forbids changing it; "As soon as one freezes a design, it becomes obsolete." (Brooks)

> "It is the professional duty of a software engineer to recognize this truth and to always offer advice, estimates, and design thoughts based on a high-quality outcome."
*Ref: Modern_Software_Engineering.md — "Organizational and Cultural Problems", "Engineering as a Human Process"*

---

### 45. The Sustainability Dividend — 44% More Time on New Work

**Principle:** Teams taking a disciplined engineering approach spend ~44% of their time on *new work* (vs. rework and unplanned maintenance). Cutting quality is not a shortcut to speed; it is the surest way to *lose* speed.

**Do:**
- Treat the "44% more time on new work" benchmark as a measurable target — it is achievable.
- Track `Lead Time for Changes` and `Deployment Frequency` as proxies for whether the discipline is working.
- Reward quality of design; punish overwork.

**Don't:**
- Don't measure "developer days" or "velocity"; they have no causal relation to outcome.
- Don't let quality reductions hide in the name of "delivery targets."
*Ref: Modern_Software_Engineering.md — "Why Does Engineering Matter?", "Engineering as a Human Process"*

---

### 46. Over-Engineering & Future-Proofing — YAGNI, with a Twist

**Principle:** "Future-proofing" is a sign of design immaturity. The real engineering answer is to make your code so easy to change that you can future-proof it at the time you need to.

**Do:**
- Apply YAGNI: write code for *the problem in front of you right now*, no more.
- Replace future-proofing with three strategies: (1) abstraction, (2) tests, (3) skill.
- Recognize the trap of "we may not need this now, but we probably will in future."

**Don't:**
- Don't freeze your design in time. Frozen designs are obsolete by Brooks' law.
- Don't hero-program — "If you have a hero in your organization, she needs to be working to spread her knowledge."
- Don't pursue "technically shiny ideas" as the cornerstone of an architecture — try them as experiments first.

> "The real solutions to the problem of being afraid to change our code are **abstraction** and **testing**."
*Ref: Modern_Software_Engineering.md — "Fear of Over-Engineering"*

---

### 47. Engineering Applies Everywhere (Including ML)

**Principle:** The ten ideas are technology-agnostic and durable. Farley demonstrates this by *applying the framework to machine learning* — a domain he openly admits to not being expert in. The framework asks good questions; the answers come from ML people.

**Do:**
- Apply iteration, feedback, incrementalism, empiricism, experimentation to ML training pipelines (short cycles, fast accuracy feedback, version-controlled data and scripts).
- Apply modularity, separation of concerns to training data itself: "Applying these ideas to the data… would allow developers of ML systems to iterate more quickly."
- Treat ML fitness functions as you would any test: predict outcomes, define error bounds, run the experiment.
- Recognize that bias in ML models can be analyzed as "a poor separation of concerns in the training data."

**Don't:**
- Don't assume the framework ends at conventional software — "These ten things give me this framework, and I have seen many individuals and teams benefit from applying them."
*Ref: Modern_Software_Engineering.md — "Durable and Generally Applicable"*

---

### 48. The 39 Million Operations Perception Gap (Engineer vs Human-Test)

**Principle:** If you can only test at human perception rates, you sample at 1:39,000,000 of computer operations. Build automation into your process or accept vast under-testing.

**Do:**
- Run tests as aggressively as the machine allows. Farley's team: 30,000 tests in 2 minutes. Google: 150 M/day.
- Recognize that the only limit on testing speed is test *design* and execution budget — not your hardware.

**Don't:**
- Don't run tests manually when you could automate them; humans are "too slow, too variable in what they do, and too expensive to rival an automated approach."
- Don't constrain yourself to human-perceivable timelines in production systems that don't care.
*Ref: Modern_Software_Engineering.md — "Precision and Scalability"*

---

### 49. The Broom-Balancing Metaphor for Feedback

**Principle:** Feedback-driven control is more *effective* than predictive planning. Balancing a broom by hand (PID-controller-with-feedback) is how rockets stabilize themselves.

**Do:**
- Think of your development process as a real-time control system: characterize → predict → act → observe → correct.
- Prefer feedback loops over detailed up-front planning; one succeeds on a wobbling broom, the other only on a perfect one.

**Don't:**
- Don't assume that "less rigor" = "less effective." The broom-balancer wins.

> "This second approach feels more ad hoc… but it is profoundly more effective and more stable in terms of outcome."
*Ref: Modern_Software_Engineering.md — "5. Feedback — A Practical Example"*

---

### 50. "Write Code to Communicate to Humans"

**Principle:** Code is a communication tool first. Readability is the professional duty of a software engineer.

**Do:**
- Optimize for thinking, not typing.
- Treat code clarity as an economic property: it directly reduces the cost of ownership.
- Use names and method extraction to make intent clear.

**Don't:**
- Don't measure simplicity by character count.
- Don't privilege machine-readability over human-readability; *"that is not really its primary goal."*

> "The primary goal of code is to communicate ideas to humans!"
*Ref: Modern_Software_Engineering.md — "10. Cohesion — A Basic Reduction in Cohesion"*

---

## Anti-Patterns & Common Mistakes

- **"Strategy group" grand architecture with no working code:** Farley's consulting experience — a "grand plan for a distributed, service-based component architecture" that "existed only as documents and a fair amount of code that didn't work." Three years late, 40+ people, no project ever used it. → *fix:* design iteratively with working increments; ship minimum-viable architectures and validate.

- **CABs ("change approval boards"):** Proven in Accelerate to *not* improve change-fail rate, while *worsening* lead time, deployment frequency, and restore time. → *fix:* replace external approvals with automated deployment pipelines.

- **Coverage-gamed tests without assertions:** A team hit their 80% target — and 25% of their tests had no assertions. → *fix:* measure *stability* (change-failure rate, MTTR) instead of coverage.

- **"Test-after" unit testing passed off as TDD:** "Unit testing, after the code is written, encourages us to cut corners, break encapsulation, and tightly couple our test to the code that we already wrote." → *fix:* write the test first; if you can't make the test pass with a clean abstraction, refactor.

- **Premature parallelism:** "the only thing that concurrency is good for is fanning out to fully independent work." The experiment table in §13 demonstrates how wrong the default is. → *fix:* measure; isolate concurrency to controlled edges.

- **Big-balls-of-mud from "we'll refactor later":** The default outcome without discipline. Costs accumulate invisibly until they dominate. → *fix:* treat design quality as a real-time concern.

- **Over-engineering via "future-proofing":** "I was as guilty of this as anyone else in the past, but I have come to regard it as a sign of design and engineering immaturity." → *fix:* YAGNI + test-backed abstraction.

- **Story-point velocity as a metric:** Not defensible measurement of productivity. → *fix:* track lead time, deployment frequency, change-failure rate, MTTR — the DORA metrics.

- **Synchronous inter-service calls treated as reliable:** "as soon as we establish such a boundary, whatever its nature, any idea of synchrony is an illusion." → *fix:* async messaging between modules.

- **DRY across services:** Reduces independence, forces coordination, and ironically *increases* coupling. → *fix:* allow duplication between independently deployable services.

- **"We tried TDD and it didn't work":** Farley has never met a team that truly did — what they call "TDD" is usually test-after unit testing. → *fix:* actually write the test before the code.

- **Pseudo-agile "faux agile":** ceremonies without a learning mindset. "Inspect and adapt" is the *only* test of agility. → *fix:* instrument outcomes; iterate on the data.

- **Hero-programmers:** A single person who "saves the day" — usually a sign of unrepeatable, unscalable practice. → *fix:* spread knowledge; reduce system coupling so the hero isn't needed.

- **Pretending waterfall is "diligent":** "What if we could change our minds, discover new ideas, discover errors, and fix them, all at roughly the same cost whenever that happened?" → *fix:* iterate; flatten the cost-of-change curve.

- **Code review as a substitute for tests:** Proofreading a book reveals some errors; you still need automated checks for every printing. → *fix:* automate, especially in CI.

- **"We just don't know how to measure software":** Use DORA — it's the best we have and it works.

- **Naive precision ("we need to prove it"):** Formal methods don't scale beyond narrow problems because "the 'provability' quickly explodes to become impractical" once concurrency, real I/O, or complex domains intrude. → *fix:* iterative empirical approach like aerospace — model, then test the device.

---

## Decision Heuristics / Checklists

- **Technology selection qualifier (Chapter 14):**
  - Is it deployable? Is it testable? Is it controllable? Is it fast enough? Does it preserve our modularity?
  - If any answer is "no," treat that as near-disqualifying.

- **Design pressure checklist (Feynman of design):** When stuck, ask
  - What is the *essential* complexity here?
  - What is the *accidental* complexity we can hide?
  - At which *scale* (function, class, service, system) does this concern naturally live?
  - Which abstraction lets me test it without dragging in the real world?

- **Cohesion rule of thumb:**
  - "Having an 'and' in the description of a class or a method is a warning sign."
  - If concepts change together, keep them together; otherwise, split them.

- **CD scope test:** If the pipeline says "good to go," is there *no more work* before production? If not, your scope is wrong.

- **Iteration cadence target:** Aim for < 1 hour to releasable, ~5 minutes for commit-stage feedback.

- **Dependency inversion rule:** If a class creates a dependency, it cannot be tested in isolation. Inject the dependency.

- **DORA measurement:** Track Change Failure Rate, MTTR, Lead Time for Changes, Deployment Frequency.

- **DRY scope rule:** DRY inside a deployment pipeline, not across them. Don't share libraries between microservices.

- **TDD diagnostic:** If your test is hard to write, your design is bad. Refactor and re-test.

- **Refactor trigger:** "as soon as [code] begins to feel like hard work, you should pause and start looking for ways to simplify and clarify the part in front of you" — even for ~10 lines of growth.

- **Async over sync rule:** Any distributed call that *could* be modeled as an event should be.

- **"Hero" detection:** If only one person can change this code, the design has failed — even if it's "high quality."

---

## Key Takeaways

1. **Production is not your problem.** Software is design engineering. The hard problem is *design and learning*, not manufacturing.

2. **Two meta-skills define the discipline:** experts at learning (iteration, feedback, incrementalism, empiricism, experimentation) and experts at managing complexity (modularity, cohesion, separation of concerns, abstraction, loose coupling). These are the only ten foundational ideas you need.

3. **Engineering ≠ bureaucracy.** The discipline is "the stuff that works." If your practice doesn't help you build better software faster, change it.

4. **Testability is the most powerful diagnostic.** Hard to test = poor design. TDD makes testability the *first* design pressure in your code.

5. **Speed is a fitness function.** < 1 hour from commit to releasable forces every good practice; iterate toward it and watch your org improve.

6. **Deployment pipelines are scope-bound.** They evaluate *independently deployable units*. Anything else is undefined; clarify scope.

7. **DRY is too simplistic.** Apply DRY inside one pipeline; tolerate duplication between pipelines.

8. **Loose coupling is not a single switch.** Operational, developmental, semantic, functional, incidental — five different problems, five different solutions.

9. **Async messaging models reality.** Synchronous distributed calls are an illusion; design for failure from the start.

10. **No trade-off between speed and quality.** The data says the opposite — teams that move fast also fix less, and spend 44% more time on new work.

11. **Modern SE is a discipline of evidence.** "We don't have a defensible measure for productivity" — but DORA stability and throughput, plus disciplined experiments, fill that gap sufficiently.

12. **Engineer for thinking, not for typing.** Optimize for the reader, not the writer; more code is OK if it makes the design clearer.

13. **Models are useful, not true.** Leaky abstractions, even formal ones, are unavoidable; manage them; don't excuse bad code with them.

14. **Organization is the result, not the constraint.** BAPO (business → architecture → process → organization), not OBAP.

15. **Code is communication first.** "The primary goal of code is to communicate ideas to humans."

16. **Iteration, not perfection, is the path.** "If we always optimize your work and how you undertake it to maximize your ability to learn efficiently you will do a better job."

---

### 51. Margaret Hamilton's "How Things Fail" Discipline

**Principle:** The original "software engineer" — Margaret Hamilton, who led Apollo flight-control software — operated from a *specific* engineering mindset: imagine how things could fail, then code defensively against that.

**Do:**
- Use this as the inspiration for your own failure-mode modeling: "the habit of imagining how things could possibly go wrong."
- Build systems that can fail safely (Apollo 11's 1201/1202 alarms didn't abort the landing because of asynchronous scheduling).
- Treat errors as a *first-class* design concern — "What was the focus… was the focus on how things fail — the ways in which we get things wrong."
- Add error-detection-and-recovery at design time, not as an afterthought.

**Don't:**
- Don't design only for the happy path; pre-mortem each significant component.
- Don't assume any single error mode is "too unlikely to handle."

> "We had been running this code for more than a week… we had been running all of these tests in our deployment pipeline repeatedly and successfully for more than a week, with the messaging changes."
*Ref: Modern_Software_Engineering.md — "Engineering as Math", "First Software Engineer" sidebar*

---

### 52. The Birth of Software Engineering — Paradigm Shift, Not Improvement

**Principle:** Farley invokes Thomas Kuhn: treating software development as a genuine engineering discipline is a *paradigm shift*, not a tweak. That requires discarding old ideas that the shift supersedes (waterfall, big-up-front planning, etc.).

**Do:**
- Recognize when an idea must be *replaced*, not improved. The shift from production-engineering to design-engineering is conceptual.
- Look for the durable ideas from the 1968 NATO conference — many are still true (e.g., Perlis on feedback loops, d'Agapeyeff on module shaping and simulation).
- Accept that paradigm shifts mean *discarding* techniques, not just adding new ones.

**Don't:**
- Don't try to "improve" waterfall. The model is wrong; iteration replaces it.
- Don't treat "we're doing agile now" as a configurable behavior. It's a recognition that production-engineering metaphors don't apply.

> "The idea of paradigm shift implicitly includes the idea that when we make such a shift, we will, as part of that process, discard some other ideas that we now know are no longer correct."
*Ref: Modern_Software_Engineering.md — "Shifting the Paradigm", "The Birth of Software Engineering"*

---

### 53. The 1968 NATO Conference — Durability of Fundamental Ideas

**Principle:** Many ideas floated in 1968 (Perlis, d'Agapeyeff, Selig) about feedback, modularity, and simulation remain the best practice today. The durable parts of any engineering idea outlive the technology that birthed them.

**Do:**
- Anchor your practices on fundamental, durable ideas — they're more likely to translate to new languages, tools, and platforms.
- When evaluating a new technique, ask: "Is it an idea or a mechanism?" Mechanisms age; outcomes endure.

**Don't:**
- Don't pile up current-year frameworks and call that progress. Most are mechanisms; few are ideas.
- Don't assume a new idea is fundamentally novel just because nobody has used it before.

> "There is something different, something more profound, in saying 'Establish feedback loops' or 'Assume that you will get things wrong' compared to 'Use language X' or 'Prove your designs with diagramming technique Y.'"
*Ref: Modern_Software_Engineering.md — "5. Feedback — NATO Conference sidebar"*

---

### 54. DORA-Accelerate Decoded — Speed *Improves* Quality

**Principle:** The research in *Accelerate* (Forsgren, Humble, Kim) has a counterintuitive headline: there is **no trade-off** between speed and quality. Improving speed also improves quality.

**Do:**
- Treat the correlation as a fact, not a question. Optimize for speed; trust that quality follows.
- Apply the same insight to micro decisions — fast code reviews, fast merges, fast deploys — and notice how each forces quality-improving practices.
- Read DORA as "an enormous, measurable advantage" in choosing engineering investment.

**Don't:**
- Don't offer "trade-off" as an excuse for cutting corners.
- Don't treat velocity (story points, lines of code) as a measure of speed; it has no causal correlation with outcome.
- Don't use DORA findings as a weapon against colleagues without using the same data to argue for the practices that produce them.

> "There is no single development, in either technology or management technique, which by itself promises even one order of magnitude improvement within a decade in productivity, in reliability, in simplicity." — Brooks
*Ref: Modern_Software_Engineering.md — "The Importance of Measurement", "Applying Stability and Throughput"*

---

### 55. "Inspect and Adapt" as the Only Real Test of Agile

**Principle:** Agile thinking's deepest signal is "inspect and adapt." Faux-agile (e.g., "index cards + daily standups + sprint demo") that lacks a feedback-driven inspection is just waterfall in disguise.

**Do:**
- Measure the actual feedback loops in your process — how fast are they, and how informative?
- Replace ceremonies that don't improve learning (status update standups, mandated estimates) with experiments and reviews.
- Treat every team process change as an experiment (hypothesis → measure → learn).

**Don't:**
- Don't mistake process compliance for actual empirical learning.
- Don't keep ceremonies alive just because the team is "used to them."

> "Most organizations are still, at heart, dominated by waterfall thinking at the organizational level, if not also at the technical level."
*Ref: Modern_Software_Engineering.md — "4. Working Iteratively — Agile Revolution"*

---

### 56. The "Beginning of Infinity" Argument for Iterative Approaches

**Principle:** Farley borrows David Deutsch's argument that some approaches are inherently unbounded and some are inherently bounded — alphabetic writing vs. pictographic writing; iterative dev vs. plan-driven. Choose the unbounded.

**Do:**
- Embrace tools that compose: alphabets of tests, primitives of code, building blocks of services.
- Prefer practices where adding one more step extends the reach of the methodology.

**Don't:**
- Don't invest in practices with a hard ceiling (you can only "perfect" a plan so far before reality wins).
- Don't confuse scope with complexity — small iterative steps can address arbitrarily large problems.

*Ref: Modern_Software_Engineering.md — "The Lure of the Plan"*

---

### 57. Apollo LEM's Pragmatic Decomposition

**Principle:** Modular decomposition isn't an academic exercise; the Apollo Lunar Excursion Module was four task-specific modules so each piece could be lighter and simpler. Decompose by problem, not by layer.

**Do:**
- Identify task-shaped modules (servicemodule, commandmodule, descent, ascent) and let each focus on its job.
- Let interfaces between modules absorb the cost of variation so modules don't.
- Use the same idea in your services — one bounded context per service.

**Don't:**
- Don't decompose by *technology* (UI module, DB module, business module); that's accidental layering over essential problems.
- Don't try to share code between task-shaped modules; embrace independent ownership.

*Ref: Modern_Software_Engineering.md — "Importance of Modularity"*

---

### 58. Conway's Law as Information-Science Outcome

**Principle:** Conway's Law is observed ("any organization that designs a system will produce a design whose copy of the organization's communication structure") but the deeper truth is that *organizations are information systems*, and the same coupling/concurrency issues affect them as affect code.

**Do:**
- Apply the same complexity-management ideas (modularity, separation of concerns, loose coupling) to team topology.
- Treat team boundaries as code boundaries — small teams own small, decoupled, coherent systems.
- Use *modular organizations* as a deliberate engineering choice.

**Don't:**
- Don't accept that "we have org-chart constraints" as inevitable. Restructure deliberately.

> "If we buy in to this fundamental philosophy that we must retain our ability to change our ideas, our teams, our code, or our technology, as we learn more, then nearly everything else… follows on as a natural consequence."
*Ref: Modern_Software_Engineering.md — "Digitally Disruptive Organizations", "Modularity in Human Systems"*

---

### 59. The Apollo-11 Save — Fail-Safe Engineering

**Principle:** Hamilton's team built *capability* without specific prediction of how it would be used. The 1201/1202 alarms didn't abort Apollo 11 because they could reboot partial work — failure modes had been coded by replay priority, not by checklist.

**Do:**
- Treat unexpected failure as an expected category; design for graceful degradation.
- Choose mechanisms that fail safe (priority drops, async retries, eventual consistency) — these absorb the "unknown unknowns" of production.

**Don't:**
- Don't ship features without their failure paths. Each feature has at least one.
- Don't optimize for code paths that "couldn't possibly fail" — they can.

*Ref: Modern_Software_Engineering.md — "Engineering as Math"*

---

### 60. The Wright Brothers — Iterative Engineering in Metals

**Principle:** The Wright Brothers succeeded where many failed because they combined *craft* (build a real artifact) with *engineering* (build a wind tunnel, measure, iterate). Their glide ratio went from 8.3:1 (1903) to 70:1 (modern sailplanes) under that regime.

**Do:**
- Combine physical prototyping with measurement rigs (wind tunnels for wings; CI for code).
- Expect your first attempts to be wrong; design for fast cycles of artifact → measure → refine.
- Use the same engineering discipline for code: the artifact, the test rig, the measurement are all part of your practice.

**Don't:**
- Don't treat your first cut as definitive. Even the Wrights upgraded the wings every season.
- Don't let "we already built it that way" stop iteration.

*Ref: Modern_Software_Engineering.md — "The Journey from Craft to Engineering"*

---

### 61. The Software Half-Life Heuristic (Dan North)

**Principle:** Dan North's "software half-life" is the time it takes a team to rewrite half of its software. Good teams are measured in months; bad teams in years (or never).

**Do:**
- Treat rewrite-ability as a quality metric.
- Continually refactor to keep the half-life low; every cluster of code that you "rebuild" reveals successes.

**Don't:**
- Don't hoard software under "we can't risk it." That's the legacy-code trap.

*Ref: Modern_Software_Engineering.md — "Technical Problems and Problems of Design"*

---

### 62. "Sub-system of One" — The Whole System As a Module

**Principle:** Farley's team treated their entire exchange as "a single system" — but inside it, they defined integration points at every external boundary and faked the rest. They could then test the whole system as a black box via those fakes.

**Do:**
- Choose your *scope of evaluation* deliberately — full system or module. Pick one.
- Treat integration points as ports, regardless of the scope of testing.
- Add fakes at any external dependency you don't want in your test rig.

**Don't:**
- Don't try to test "everything together" without also testing "this module alone." Both are needed.

*Ref: Modern_Software_Engineering.md — "Designing for Testability Improves Modularity"*

---

### 63. Failing Fast — A Culture, Not Just a Practice

**Principle:** "Fail fast" isn't just about pushing defects left; it's a culture that *rewards* surfacing problems early because early failure is the cheapest.

**Do:**
- Cheer when a TDD cycle fails — that's its purpose.
- Treat design friction as a positive signal you can act on now.
- Use data to remove blame: "the system" surfaced a defect, not a person.

**Don't:**
- Don't punish teams for surfacing problems early; you'll teach them to hide them.
- Don't conflate "fail fast" with reckless shipping.

*Ref: Modern_Software_Engineering.md — "Prefer Early Feedback"*

---

### 64. The 39 Million Operations Insight — Embrace Speed-of-Test

**Principle:** At ~3 GHz with ~13 ms human perception, a human-perceived cycle contains ~39 M operations. Anything less than machine-speed testing is profound under-sampling.

**Do:**
- Push tests to the machine's actual capabilities.
- Use parallel builds, fan-out test runners, deterministic fixtures.
- Profile the test rig the same way you profile production.

**Don't:**
- Don't tolerate single-threaded, single-machine test rigs at the team scale.
- Don't mistake a quick-test environment for a fully-tested system; sample size matters.

*Ref: Modern_Software_Engineering.md — "Precision and Scalability"*

---

### 65. Domain-Specific Languages As Executable Specifications

**Principle:** DSLs lift abstractions effectively *because* they're narrow — exactly what's needed for testing. Farley: "there is no better way to create effective test cases than to create a DSL that allows you to express the desirable behaviors of your system as 'executable specifications.'"

**Do:**
- Use BDD/ATDD frameworks that read like domain language.
- Sketch DSLs for test setup (fixtures) when they reduce duplication.

**Don't:**
- Don't mistake a DSL for general-purpose language; they're tools, not a destination.
- Don't build DSLs that pre-commit the system to one architecture.

*Ref: Modern_Software_Engineering.md — "Abstractions from the Problem Domain"*

---

### 66. Event Storming — Discovering Bounded Contexts

**Principle:** Alberto Brandolini's event storming technique (mentioned by Farley) surfaces *bounded contexts* by mapping domain events. It is the practical entry point to DDD-driven decomposition.

**Do:**
- Run an event storming session with domain experts before designing services.
- Identify clusters of events that belong together; each cluster is a candidate bounded context.
- Use this to inform both microservice boundaries and module boundaries.

**Don't:**
- Don't decompose on purely technical lines; let the domain name its own modules.
- Don't skip event storming just because the team "already knows the domain."

*Ref: Modern_Software_Engineering.md — "Abstractions from the Problem Domain"*

---

### 67. Mechanical Sympathy — Code that Knows the Hardware

**Principle:** "Mechanical sympathy" is Farley's term for designing code *with* deep awareness of the hardware. It is the high-performance corollary to testability: cache-misses dominate performance in modern computers.

**Do:**
- Understand the cost model of your hardware (cache line size, branch prediction, memory bandwidth).
- Optimize data structures and access patterns, not premature cleverness.
- Test at the granularity your tools claim (microseconds, even nanoseconds).

**Don't:**
- Don't assume "single-threaded" means slow on modern CPUs — modern hardware is "marvelous" at unconnected work.

*Ref: Modern_Software_Engineering.md — "Inventing a Reality to Suit Our Argument"*

---

### 68. The "Plain Text" Abstraction's Hidden Work

**Principle:** JSON, XML, HTML are "plain text" — and "plain" is a lie. Behind the obvious interface is an enormous engineering consensus (encoding, byte ordering, semantics). All abstractions are made.

**Do:**
- Appreciate the value of widely-supported, semantically tagged formats (JSON, Protobuf, SBE).
- Choose binary encodings (Protobuf, SBE) only when the cost of plain text is genuinely prohibitive.
- Inspect the abstraction when you need to: where does it leak?

**Don't:**
- Don't reach for binary formats because they're "fast"; most workflows don't need it.

*Ref: Modern_Software_Engineering.md — "Power of Abstraction"*

---

### 69. CSS/Per-System Tests, Not Just Global Ones

**Principle:** Tests should be graded for *power*. Acceptance tests describe behavior from outside-in; unit tests verify the abstraction layer-by-layer; performance tests measure non-functional properties. Each is needed.

**Do:**
- Use acceptance tests as the executable specification of a feature.
- Use unit tests to verify the abstraction is testable and the design holds.
- Use performance and security tests as part of the deployability conversation.

**Don't:**
- Don't replace unit tests with "lots of acceptance tests" — the abstraction can rot invisibly.

*Ref: Modern_Software_Engineering.md — "Feedback in Architecture"*

---

### 70. Sophisticated Telemetry As Product Strategy

**Principle:** Modern systems gather telemetry for diagnostics *and* for product strategy. Farley: "the information that is gathered is often more valuable than the services provided and can provide insights into customer wants, needs, and behavior that even the customers themselves are not conscious of."

**Do:**
- Treat telemetry as a first-class product capability.
- Couple it to short feedback cycles so insight flows quickly to designers.
- Use telemetry to *question*, not confirm, assumptions about user behavior.

**Don't:**
- Don't ship a feature without a way to learn if anyone uses it.
- Don't trust your team's intuition about user behavior; gather data.

*Ref: Modern_Software_Engineering.md — "Feedback in Product Design"*

---

### 71. Continuous Delivery Beyond Software

**Principle:** The CD principles apply even where physics constrains the targets. Tesla "is a continuous delivery company"; cars and rockets test "thoroughly, rejecting any change immediately if a single test fails."

**Do:**
- Translate the goals ("releasable," "fast feedback," "control the variables") into your domain.
- Run experiments (e.g., SpaceX pressurizing steel prototypes) instead of debating.

**Don't:**
- Don't constrain continuous delivery to "software stuff."

*Ref: Modern_Software_Engineering.md — "Outcomes vs. Mechanisms"*

---

### 72. Stop Reaching for "10x Languages"

**Principle:** Farley is unimpressed by language-level improvements because few have produced Brooks' 10x. The big steps were "machine code → C" and "procedural → OO" — the rest is mostly syntactic.

**Do:**
- Judge languages and frameworks by how they support the ten foundational ideas.
- Spend your energy on practices, not on language choice.

**Don't:**
- Don't expect the next language to save you.
- Don't pick a language to put on a CV.

> "These were issues more to do with the philosophy of our discipline and the application of some foundational principles that hold true whatever the nature of the technology."
*Ref: Modern_Software_Engineering.md — "Engineering != Code"*

---

### 73. Engineering != Computer Science

**Principle:** "Software engineering is often treated as a branch of computer science. This is akin to regarding chemical engineering as a branch of chemistry. We need both chemists and chemical engineers, but they are different." — Parnas

**Do:**
- Treat engineering as the *applied* discipline; CS as the *foundational* discipline.
- Hire for curiosity about applied problems, not just theory.

**Don't:**
- Don't privilege one over the other; they have different jobs.

*Ref: Modern_Software_Engineering.md — "Repeatability and Accuracy of Measurement"*

---

### 74. Treating Code As A Habitable Space

**Principle:** Code is a place you'll live in for years. Design for habitability — clarity, navigability, changeability — not just for the current feature.

**Do:**
- Read your own code a year later and ask "would I recognize this?"
- Optimize for future readers, including future-you.
- Treat cruft as a real cost; pay it down.

**Don't:**
- Don't ship a feature without also making the surrounding code a *bit* better (the "boy scout rule" applied at the smallest scale).

*Ref: Modern_Software_Engineering.md — "Technical Problems and Problems of Design"*

---

### 75. Kanban for Software Half-Life

**Principle:** Visualizing the work-in-progress exposes bottleneck. While Farley doesn't dwell on Kanban, the underlying idea (limit WIP, expose flow) is consistent with iteration and continuous delivery.

**Do:**
- Use a board that exposes the *state* of every commit, not just what's "in progress."
- Visualize deployment-pipeline steps as states.

**Don't:**
- Don't optimize the board instead of the system.

*Ref: Modern_Software_Engineering.md — "Feedback in Organization and Culture"*

---

### 76. "Reasonable Concurrency" — A Subset of Operations

**Principle:** Not every concurrent operation is bad — only those whose results must be joined. Trivially independent work (image rendering, ML inference batches) benefits hugely from parallel hardware.

**Do:**
- Reserve concurrency for "trivially parallel" workloads.
- Decompose-then-join is fine for embarrassingly parallel problems; not fine for tight algorithmic dependencies.

**Don't:**
- Don't throw threads at a problem with a serial kernel.
- Don't let concurrency into your unit-of-test.

*Ref: Modern_Software_Engineering.md — "Cost of Concurrency (Empirical Experiment)"*

---

### 77. The Discipline of Empirical Process Control

**Principle:** The phrase "empirical process control" (vs. "defined process control") is the formal distinction between agile and waterfall. Defined processes require complete understanding up-front; empirical processes embrace discovery.

**Do:**
- Prefer empirical control when the answer is uncertain — most software is.
- Use defined control only where steps are well-understood, repeatable, and predictable (e.g., production deployment with infrastructure-as-code).

**Don't:**
- Don't run a defined process against an empirical problem.

*Ref: Modern_Software_Engineering.md — "5. Feedback" — agile calls covered*

---

### 78. "Things That We Don't Talk About" — Coupling Examples in Code

**Principle:** Real-world coupling shows up in places code doesn't usually discuss: configuration, secrets, observability, deployment topology. These are part of the surface area too.

**Do:**
- Treat secrets and config as part of the architecture; review them in design.
- Use abstraction to keep sensitive values out of the core domain.

**Don't:**
- Don't smuggle configuration into business logic; inject it.

*Ref: Modern_Software_Engineering.md — "Designing for Loose Coupling"*

---

### 79. APIs As Information, Not Just Signatures

**Principle:** "An API is all of the information that is exposed to consumers of a service." Beyond signatures: schema, contents, ordering, semantics, timing. All are part of the contract.

**Do:**
- Document the *information* the API exposes, including implicit fields.
- Version APIs and validate inputs at boundaries.
- Treat binary streams with semantics as APIs (e.g., the first 8 bytes encode length).

**Don't:**
- Don't treat "signature" as the whole API; rely on integration tests for behavioral guarantee.

*Ref: Modern_Software_Engineering.md — "11. Separation of Concerns — What Is an API?"*

---

### 80. The "Catalyst" Mindset — TDD As Discovery

**Principle:** Each TDD cycle is a catalyst for design decisions you would otherwise defer. The act of writing the test accelerates the moment of design.

**Do:**
- Embrace the discomfort of writing the test first; it's the design's first draft.
- Use the test signature to negotiate the API.
- Notice "and" responsibilities that grow in your test setup; that's the code shouting that you need a new abstraction.

**Don't:**
- Don't skip TDD because "I already know the implementation" — that's a deferred design decision.
- Don't write tests that don't challenge the design.

*Ref: Modern_Software_Engineering.md — "Driving High Cohesion with TDD"*

---

### 81. The Lure of Plan — Why We Underestimate Discovery

**Principle:** Two-thirds of ideas at the best software companies produce zero or negative value. Even when you "ask your users," they don't know what they want. Plan-based approaches to discovery have a fundamental informational disadvantage.

**Do:**
- Treat plan-based valuation as best-case assumption; validate with shipping small increments.
- Expect most ideas to fail and design for that.
- Use the lean/startup pattern of measured experiments.

**Don't:**
- Don't let a "business case" convince you that shipping the feature is the safe bet.
- Don't accept "we knew it would work" from teams that didn't ship it.

*Ref: Modern_Software_Engineering.md — "The Lure of the Plan"*

---

### 82. Choosing Feedback Loops By Latency

**Principle:** Choose the *shortest* feedback loop that gives you the signal you need.

**Do:**
- Compile-level feedback at first; type-check as part of "syntax."
- Unit-test in milliseconds for behavior.
- CI feedback in minutes for whole-system dynamics.
- Production telemetry for actual usage.

**Don't:**
- Don't use a slow feedback loop for a question a fast one could answer.
- Don't merge "fast feedback" with "good feedback" — you need both.

*Ref: Modern_Software_Engineering.md — "5. Feedback"*

---

### 83. The Minimum Useful Model

**Principle:** Modeling is always a tradeoff. Farley's maps metaphor: a constant-bearing chart and Beck's Tube map are *both* useful for different questions. Pick the abstraction for the question you're asking.

**Do:**
- Pick the model that solves the problem you have, not the most accurate one.
- Validate your model against empirical reality.

**Don't:**
- Don't expect one model to serve every purpose.
- Don't mistake model fidelity for model utility.

*Ref: Modern_Software_Engineering.md — "Picking Appropriate Abstractions"*

---

### 84. "Code Reviews Are Not Enough"

**Principle:** Code review catches *some* defects but not most. Farley explicitly: "Software is intolerant of errors; proofreading and code review is not enough."

**Do:**
- Pair review with automated checks (linters, type checkers, tests).
- Run reviews alongside, not instead of, deterministic checks.

**Don't:**
- Don't use reviews as a substitute for automated tests.
- Don't assume review is the bottleneck; it often is *because* automation is missing.

*Ref: Modern_Software_Engineering.md — "14. Tools of an Engineering Discipline — What Is Software Development?"*

---

### 85. The "44% Time on New Work" Target

**Principle:** High-performing teams spend 44% more time on new work because disciplined engineering amortizes the cost of change.

**Do:**
- Set a target for "time on new work" in your team; measure it.
- Treat rework budget as a *symptom* of poor design.

**Don't:**
- Don't let quality reductions hide in delivery targets — the long-run cost always exceeds the short-run gain.

*Ref: Modern_Software_Engineering.md — "Why Does Engineering Matter?"*

---

### 86. Adapt, Don't Adopt (Toyota Kata Influence)

**Principle:** Mike Rother's *Toyota Kata* thinking: characterize where you are → where you want to be → next step → measure.

**Do:**
- Apply the same to engineering improvements: where is our testability today? Where does it need to be? What's the next concrete step?
- Don't adopt wholesale; adapt to your context.

**Don't:**
- Don't copy a recipe; apply the framework.

*Ref: Modern_Software_Engineering.md — "Feedback in Organization and Culture"*

---

### 87. Limited "Future-Proofing" Means Limited Architectural Flexibility

**Principle:** Future-proofing often means designing for imagined requirements. The actual engineering cost is in the *abstraction* and the *tests*, not in features you might need.

**Do:**
- Invest in abstractions and tests today; future features will plug into them.
- Build for the next 6 months, not the next 5 years.

**Don't:**
- Don't add a "framework" or "infrastructure" "in case we need it."

*Ref: Modern_Software_Engineering.md — "Fear of Over-Engineering"*

---

### 88. The "Iron Triangle" — Quality, Speed, Cost? (No: All Correlated)

**Principle:** The classic iron triangle (quality / cost / speed) is a myth for software. Farley's data (DORA-Accelerate) shows all three correlate positively.

**Do:**
- Quote the data when stakeholders insist on trade-offs.
- Manage quality, time, and cost together.

**Don't:**
- Don't accept "we'll go fast now and fix it later" — the cost of later is higher than the cost of now.

*Ref: Modern_Software_Engineering.md — "Undervaluing the Importance of Good Design"*

---

### 89. Headless Refactoring As Continuous Improvement

**Principle:** Refactoring should be part of every change, not a separate phase. IDE-level refactorings (extract method, introduce parameter, rename) make this nearly free.

**Do:**
- Refactor in the same commit as the feature, but commit them as separate logical steps.
- Use IDE-provided safe refactorings whenever possible.

**Don't:**
- Don't schedule a "refactor sprint" — that means you've been neglecting refactoring.

*Ref: Modern_Software_Engineering.md — "Tools of Incrementalism"*

---

### 90. "Test Rig" Mental Model

**Principle:** A test rig has measurement probes (calipers) at the system under test's boundaries. Build the test rig with the system, not after.

**Do:**
- Treat the testing interface as a first-class design artifact.
- Pick your scope of measurement deliberately (unit, integration, system).

**Don't:**
- Don't retrofit testing access; design with measurement points from the start.

*Ref: Modern_Software_Engineering.md — "Designing for Testability Improves Modularity"*

---

### 91. "It's Just Code" Is The Wrong Frame

**Principle:** Software is *incredibly* complex. Farley: a Volvo truck has ~80M LOC, vs. a modern passenger plane's ~4M parts. You're not "just typing."

**Do:**
- Treat your craft with the seriousness that the complexity demands.
- Plan for years-long maintenance, not just shipping the feature.

**Don't:**
- Don't trivialize the work; engineering is hard.

*Ref: Modern_Software_Engineering.md — "Feedback in Design"*

---

### 92. The Friendly Reception of "Just Refactor It"

**Principle:** Real engineering teams welcome refactoring as professional practice. "Anyone can write code; that is not our job. Software development is more than that. Our job is to solve problems."

**Do:**
- Reframe "writing code" as "solving problems."
- Treat the absence of refactoring as a *bug* in your process.

**Don't:**
- Don't treat refactoring as "gold-plating" — it's hygienic work.

*Ref: Modern_Software_Engineering.md — "Engineering != Code", "Organizational and Cultural Problems"*

---

### 93. "Data is Code" in ML

**Principle:** Managing the complexity of ML means managing data complexity. Module-cohesive datasets, separated-by-concern, version-controlled.

**Do:**
- Version your training data; treat it as code.
- Scope training datasets to specific concerns.
- Use the same SoC vocabulary for data engineering as for code engineering.

**Don't:**
- Don't let data drift unobserved.

*Ref: Modern_Software_Engineering.md — "Durable and Generally Applicable"*

---

### 94. "Talent Amplifier" — TDD Improves Skill Range

**Principle:** TDD doesn't make bad devs good, but it widens the skill range: "great devs become greater, bad devs become less bad."

**Do:**
- Adopt TDD as a *baseline*, not a finishing touch.
- Use it to lift junior developers' code quality.

**Don't:**
- Don't expect TDD alone to fix everything; combine with PR review, mentoring.

*Ref: Modern_Software_Engineering.md — "12. Information Hiding and Abstraction", "Improving Abstraction Through Testing"*

---

### 95. "Ony of These Things Is Not Like the Other" — Cohesion Detection

**Principle:** Cohesion is contextual. A good heuristic is "are all of these things the same?"

**Do:**
- Use the Sesame Street heuristic to spot low-cohesion classes: "look for a member that doesn't belong."
- Listen to the code; it tells you when you've conflated concerns.

**Don't:**
- Don't argue about cohesion abstractly; the answer is in the specifics.

*Ref: Modern_Software_Engineering.md — "Context Matters"*

---

### 96. Symmetric Engineering Levels

**Principle:** The same ideas apply at every scale — every method, every class, every service, every system, every organization. There is no fundamental change of discipline as scope changes.

**Do:**
- Look for the same fractal pattern at each level.
- Adopt practices at the smallest scale you can.

**Don't:**
- Don't apply "process" at the org level and "code style" at the method level as if they were different disciplines.

*Ref: Modern_Software_Engineering.md — "Modularity at Different Scales", "Testability as a Tool"*

---

### 97. The "Scientifically Rational" Mindset Over Fads

**Principle:** Replace decision-by-authority with decision-by-evidence. "Move away from decisions based on authority, charisma, or fame."

**Do:**
- Be ready to refute any idea, even one you love.
- Run actual experiments before adopting tools.

**Don't:**
- Don't pick tools because of brand or status.

*Ref: Modern_Software_Engineering.md — "8. Experimental — What Does 'Being Experimental' Mean?"*

---

### 98. Apparent Progress vs. Real Progress (Hardware vs Software)

**Principle:** Farley's provocation: a software team that hasn't shipped in 5+ years lost *10×* progress to competitors. There are no silver bullets — but there are 10× losses.

**Do:**
- Use DORA to spot stalls early.
- Modernize practice *before* crisis.

**Don't:**
- Don't mistake treadmill activity for progress.

*Ref: Modern_Software_Engineering.md — "An Industry of Change?"*

---

### 99. "Pseudo-Modular" Refactoring Preserves Bad Decisions

**Principle:** Pulling a class out of a ball of mud without redesigning the seams is a worse trap than leaving the mud. The seams are what matter.

**Do:**
- Refactor at the *seams* (boundary-level), not just at the file level.
- Use tests to enforce the seams are real.

**Don't:**
- Don't extract a class without designing what its interface looks like.

*Ref: Modern_Software_Engineering.md — "Undervaluing the Importance of Good Design"*

---

### 100. "Sustainability" — The Lasting Argument for Engineering

**Principle:** The whole book is an argument for *sustainable* development: the ability to keep learning and adapting indefinitely. That's the difference between engineering and craft.

**Do:**
- Optimize every practice for sustainability — can you keep doing this in 5 years?
- Treat "we can keep going" as the success metric.

**Don't:**
- Don't optimize for the current sprint at the cost of the next 50.

> "If you always optimize your work and how you undertake it to maximize your ability to learn efficiently you will do a better job. If you always work, at every scale, to manage the complexity of the work in front of you, you will be able to sustain your ability to do a better job indefinitely."
*Ref: Modern_Software_Engineering.md — "Engineering as a Human Process", "Foundations of an Engineering Discipline"*

---

## Cross-References
- Related: [[../Building_Evolutionary_Architectures.md]] — evolutionary principles for software
- Related: [[../Crafting_Engineering_Strategy.md]] — engineering strategy at the org level
- Related: [[../Continuous_Deployment.md]] — operational counterpart of continuous delivery
- Related: [[../Software_Architecture_Metrics.md]] — building-block measures aligned with DORA
- Related: [[../Team_Topologies.md]] — team structure as an engineering variable (BAPO/OBAP adjacent)
- Related: [[../The_Art_of_Unit_Testing.md]] — deep dive into unit testing discipline
- Related: [[../TDD_Top_Tips.md]] — supplemental TDD practice
- Related: [[../Learning_Systems_Thinking.md]] — systems thinking as a complement to Farley's framework
- Related: [[../Fundamentals_of_Software_Testing.md]] — testing fundamentals that align with Farley's testability argument
- Topic index: [[../INDEX.md]]
