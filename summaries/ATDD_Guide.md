# ATDD Guide - Dave Farley's How-To Guide

## Comprehensive Summary

---

## What is Acceptance Test-Driven Development?

ATDD is an approach where **acceptance tests are written before any code**. These tests act as "Executable Specifications" that guide development until the specification is met. Developers then use more granular TDD to write the code that satisfies the acceptance test.

The combination of ATDD and TDD can reduce defects by **two orders of magnitude**.

---

## Properties of Effective Acceptance Tests

- Written from the perspective of an **external user** of the system
- Evaluate the system in **life-like scenarios**
- Run in **production-like test environments**
- Interact through **public interfaces only** (no back-door access)
- Focus on **What** the system does, not **How** it does it

**Key tests:**
- Could a non-technical domain expert read your test and understand it?
- If you threw away the entire system and rebuilt it differently, would your tests still make sense?

Avoid UI-specific instructions like "click this button" or "fill in this field." Instead use domain language: `placeAnOrder()`, `payByCreditCard()`.

Make each test case atomic: no shared test data, each test starts from a clean running system with no data.

---

## The Four-Layer Architecture

ATDD tests are organized in four layers:

### Layer 1: Test Cases
Written in the language of the problem domain, from the perspective of an external user. These are the executable specifications.

```
shouldBuyBookWithCreditCard():
    shopping.goToStore()
    shopping.searchForBook("title: Continuous Delivery")
    shopping.selectBook("author: David Farley")
    shopping.addSelectedItemToShoppingBasket()
    shopping.checkOut("item: Continuous Delivery")
    shopping.assertItemPurchased("item: Continuous Delivery")
```

### Layer 2: Domain Specific Language (DSL)
The DSL is shared between test cases. It makes writing tests easy by:
- Using optional parameters for flexibility
- Encoding common setup tasks (registering users, populating accounts)
- Staying focused on domain concepts, clean from implementation details

```
checkOut(String... args):
    item = params.optional("item", default: "Continuous Delivery")
    price = params.optional("price", default: "£10.00")
    card = parseCard(params.optional("card", default: "..."))
    driver.checkOut(item, price, card)
```

### Layer 3: Protocol Drivers
Translators/adaptors that convert from DSL to the "language of the system." Create one for each communication channel (REST API, web UI, CLI). Isolate all knowledge of system internals here.

### Layer 4: System Under Test
Deploy using the same tools and techniques as production. "Production-like" means the SUT can't tell the difference in how it's deployed. Optimize for fast startup.

---

## Growing the DSL

1. Start with 2-3 simple test cases exercising the most common/valuable behavior
2. Build the infrastructure to make those tests execute and pass
3. Adopt the discipline: **create a new acceptance test for every acceptance criteria on every user story**
4. Invent DSL language at the time of writing the test—don't worry about implementation
5. Anyone can write test cases (QA, BA, PO, Dev), but **developers own the tests** and the plumbing (DSL and Protocol Drivers)

---

## Key Takeaways

1. **Write tests first**: Acceptance tests are executable specifications that guide all development
2. **Domain language only**: Tests should make sense to domain experts, not just developers
3. **Four-layer separation**: Test Cases → DSL → Protocol Drivers → SUT isolates concerns
4. **Production-like testing**: Use the same deployment tools and techniques as production
5. **Atomic tests**: No shared data, each test starts clean
6. **Developer ownership**: If a test breaks, a developer should notice first
7. **Discipline pays off**: ATDD takes time to adopt but results in enormous quality improvements
