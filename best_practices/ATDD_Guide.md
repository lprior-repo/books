# ATDD Guide — Acceptance Test Driven Development
**Author:** Dave Farley (Continuous Delivery Ltd.)
**Topic tags:** `#testing` `#process` `#atdd` `#bdd` `#executable-specifications` `#collaboration`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/ATDD Guide 26-03-21/ATDD Guide 26-03-21.md` · `summaries/ATDD_Guide_26-03-21.md` · `summaries/ATDD_Guide.md`

## TL;DR
ATDD combines Acceptance Tests as **Executable Specifications** written before code with fine-grained TDD to satisfy them. The result: defects drop by two orders of magnitude. Tests are organized into a **four-layer separation of concerns** (Test Cases → DSL → Protocol Drivers → SUT), written in **domain language**, against a **production-like environment**, with **developers owning the plumbing**.

---

## Best Practices by Topic

### The ATDD Approach

**Principle:** Write an acceptance test *before* any code. The acceptance test is the executable specification that guides development. Fine-grained TDD then produces the code that satisfies it.

**Do:**
- Create an acceptance test before writing any code.
- Treat the acceptance test as an **executable specification** — a guide that organises the work until satisfied.
- Use TDD at a finer grain to write code that meets the specification.
- Adopt the discipline: **every acceptance criterion on every user story** gets a new acceptance test.

**Don't:**
- Write acceptance tests after the code — they lose their specification role.
- Skip TDD at the unit level once acceptance tests exist; the two are complementary.

*Ref: ATDD Guide 26-03-21.md — "Approach"*

---

### Properties of Effective Acceptance Tests

**Principle:** Acceptance tests are *business-facing* and *support programming* — they specify outcomes, not mechanics.

**Do:**
- Write tests from the **perspective of an external user** of the system.
- Evaluate the system in **life-like scenarios** — realistic data, realistic flows.
- Run tests in **production-like environments** (same deploy tools, same config regime).
- Interact with the SUT through **public interfaces only** — no back-door access.
- Focus on **what** the system does, not **how** it does it.
- Imagine the **least-technical domain expert** reading your test — they should understand it.
- Imagine **throwing away your SUT** and replacing it with something completely different that achieves the same goals — your test should still make sense (e.g., would buying-a-book tests work for a robot shopping in a physical store?).
- Adopt the **language of the problem domain exclusively** — `placeAnOrder`, `payByCreditCard`, not `fillInField`, `clickButton`.
- Make scenarios **atomic** — don't share test data between cases. Each test starts from a running, functioning system with **no data**.

**Don't:**
- Use UI mechanics ("click this button") or storage mechanics ("insert into this table") in acceptance tests.
- Share test data across cases — each test must be independent.
- Touch internal/private interfaces for test setup.

*Ref: ATDD Guide 26-03-21.md — "Properties of Effective Acceptance Tests" / "Tips"*

---

### Four-Layer Separation of Concerns

**Principle:** Organize test code in four layers, each with a single responsibility. This keeps tests in domain language while isolating implementation knowledge.

```
Test Cases (domain language, external user view)
       ↓
Domain Specific Language (DSL) (shared helpers, optional params, defaults)
       ↓
Protocol Drivers (translators — DSL → SUT's actual interface)
       ↓
System Under Test (deployed via the same tools & techniques as production)
```

#### Layer 1 — Test Cases
- Written in the **language of the problem domain**, from the external user's perspective.
- These are the executable specifications.

```java
@Test
@Channel(Amazon)
public void shouldBuyBookWithCreditCard()
    shopping.goToStore();
    shopping.searchForBook( ...args: "title: Continuous Delivery");
    shopping.selectBook( ...args: "author: David Farley");
    shopping.addSelectedItemToShoppingBasket();
    shopping.checkOut( ...args: "item: Continuous Delivery");
    shopping.assertItemPurchased( ...args: "item: Continuous Delivery");
```

#### Layer 2 — Domain Specific Language (DSL)
- **Shared** between test cases. Makes writing tests easy.
- Allows **precision where needed**, skims over detail where not — achieved with **optional parameters** for nearly everything.
- Encodes **common start-up tasks** (registering users, populating accounts).
- Keeps focus on domain concepts, clean from implementation details.

```java
public void checkOut(String... args)
    Params params = new Params(args);
    String item = params.Optional( name: "item", defaultValue: "Continuous Delivery");
    String price = params.Optional( name: "price", defaultValue: "£10.00");
    Card card = parseCard(params.Optional( name: "card", defaultValue: "1234 5678 9101 0001 12/23 007"));
    driver.checkOut(item, price, card);
```

#### Layer 3 — Protocol Drivers
- **Translators / adaptors** — convert DSL calls into the actual SUT interface.
- Pattern: **mirror the DSL interface** (`dsl.checkOut` calls `driver.checkOut` with more specific parameters).
- DSL parses parameters and fills in detail; Protocol Drivers encode **real interactions with the SUT**.
- Create **a new Protocol Driver for each channel** (web UI, REST API, CLI, message queue) supported by the SUT.
- **Isolate all test-infrastructure knowledge of the system here** — the only layer that knows how the SUT actually works.

```java
@Override
public void assertListedInShoppingBasket(String item)
    gotoPage( page: "https://www.amazon.co.uk/qp/cart/view.html/ref=nav_cart",
             expectedTitle: "Amazon.co.uk Shopping Basket");
    List<WebElement> found = driver().findElements(
            By.xpath("//span[@class=\"a-list-item\"]/*[contains(., \"Continuous Delivery\")]"));
    assertEquals(String.format("Item '%s' not found in shopping basket", item),
             expected: 1, found.size());
```

#### Layer 4 — System Under Test
- Deploy using the **same tools & techniques as production**. This lets acceptance tests evaluate any change — config, OS version, DB version, etc.
- Use **Infrastructure-as-Code** to manage test and production environments → **Full Control**.
- "Production-like" means: from the SUT's perspective, **it can't tell the difference** in how it is deployed or configured.
- **Optimize** where it makes testing easy — e.g., make system startup **fast**.

*Ref: ATDD Guide 26-03-21.md — "Four Layer Separation of Concerns" / "Domain Specific Language (DSL)" / "Protocol Drivers" / "System Under Test (SUT)"*

---

### Growing the DSL Pragmatically

**Principle:** Don't try to design the DSL upfront. Let it emerge from the test cases.

**Do:**
- Start by creating **two or three simple test cases** that exercise the most common / valuable behaviour. Expect some DSL reuse even at this early stage.
- Build the infrastructure that lets those tests execute and pass.
- Then adopt the discipline: a new acceptance test for **every acceptance criterion on every user story**.
- **Invent the language** needed to express a test case *at the time of writing the test*. Don't worry about implementation.

**Don't:**
- Design the full DSL upfront before any tests exist.
- Let the DSL become a dumping ground for system-implementation knowledge — keep it domain-focussed.

*Ref: ATDD Guide 26-03-21.md — "Growing the DSL"*

---

### Collaboration and Ownership

**Principle:** Anyone can write test cases; developers own the tests and the plumbing.

**Do:**
- Allow **anyone** (QA, BA, PO, Dev) to write test cases.
- **Developers and dev teams own the tests** — if a test breaks, a developer should notice first.
- Developers own responsibility for writing the **plumbing** (DSL and Protocol Drivers) that makes the tests work.
- Treat this as a **team discipline** — set expectations together.

**Don't:**
- Let test cases live in a separate QA team's silo, invisible to developers.
- Have non-developers write the Protocol Drivers — knowledge of system internals belongs with the dev team.

*Ref: ATDD Guide 26-03-21.md — "Growing the DSL"*

---

### The ATDD + TDD Combination

**Principle:** Acceptance tests as executable specifications plus fine-grained TDD for implementation produce **two orders of magnitude fewer defects** than either alone. The acceptance test defines *what*; TDD defines *how*; together they catch defects at multiple grains.

*Ref: ATDD Guide 26-03-21.md — "Approach"*

---

## Anti-Patterns & Common Mistakes

- **Writing acceptance tests after the code:** Loses the specification role; tests become documentation that lags reality. *Fix:* write acceptance test first, every time, before any production code.
- **UI-mechanic or storage-mechanic language in tests:** "fill in this field", "click this button" → tests break on every redesign. *Fix:* use domain language (`placeAnOrder`, `payByCreditCard`).
- **Shared test data between cases:** One test pollutes another's setup; failures cascade confusingly. *Fix:* make every scenario atomic, starting from a clean system with no data.
- **Back-door test access to the SUT:** Direct DB writes, internal API calls. *Fix:* interact through public interfaces only.
- **Staging environments that diverge from production:** Acceptance tests pass in staging but fail in production. *Fix:* deploy via the same tools/config as production; use Infrastructure-as-Code.
- **Non-developers owning the plumbing:** Protocol Drivers and DSL rot without dev ownership. *Fix:* developers own plumbing; non-developers contribute test cases.
- **Designing the full DSL upfront:** Big design upfront yields a DSL that doesn't fit real test cases. *Fix:* grow the DSL pragmatically from 2–3 starting test cases.
- **Skipping TDD once acceptance tests exist:** Coarse-grained acceptance tests alone produce working but poorly-designed internals. *Fix:* keep using TDD at unit level for implementation.

*Ref: ATDD_Guide_26-03-21.md — "Properties of Effective Acceptance Tests" / "Growing the DSL"*

---

## Decision Heuristics / Checklists

- **Is this an acceptance test?** Yes if it specifies user-visible behaviour in domain language and runs through a public interface.
- **Is my acceptance test atomic?** It must not depend on data from another test.
- **Is my test in domain language?** Would the least-technical domain expert understand it? Would the test still make sense with a different SUT?
- **Am I touching the SUT through public interfaces only?** No back doors.
- **Is the test environment production-like?** Same deploy, same config regime.
- **Do I have one Protocol Driver per channel?** All system-internal knowledge isolated there.
- **Are developers owning the plumbing?** If a Protocol Driver is broken, a dev should know first.
- **Have I written this test before any code?** That is what makes it a specification.

---

## Key Takeaways

1. **Write acceptance tests before code** — they are executable specifications.
2. **ATDD + TDD = two orders of magnitude fewer defects.**
3. **Domain language only** — `placeAnOrder`, `payByCreditCard`, not "click button".
4. **Four layers** — Test Cases / DSL / Protocol Drivers / SUT, each with one job.
5. **Make tests atomic** — no shared test data; each starts from a clean system.
6. **Use public interfaces only** — no back-door access.
7. **Production-like test environments** — same deploy tools, Infrastructure-as-Code.
8. **Grow the DSL pragmatically** — start from 2–3 test cases; invent language at write-time.
9. **Developers own the tests and the plumbing** — anyone can author test cases.
10. **Take discipline seriously** — ATDD pays back enormously in time saved and quality gained.

---

## Cross-References
- Related: [[../What_to_Test_and_When.md]]
- Related: [[../TDD_Top_Tips.md]]
- Related: [[../Fundamentals_of_Software_Testing.md]]
- Related: [[../The_Art_of_Unit_Testing.md]]
- Related: [[../The_Feedback-Driven_Developer.md]]