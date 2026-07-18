# Acceptance Test Driven Development Guide - Dave Farley

## Comprehensive Summary

---

## Overview

This is a concise guide from Dave Farley's "Better Software Faster" series, focused on Acceptance Test Driven Development (ATDD) as a cornerstone practice for effective Continuous Delivery testing strategies. The guide outlines a structured approach to writing tests that serve as executable specifications, driving development from the outside in.

---

## Acceptance Test Driven Development Approach

**Core Philosophy:**
In Continuous Delivery, Acceptance Tests are "Business Facing" and "Support Programming" tests. They form part of a systemic, strategic approach to testing. The most effective workflow is:

1. Create an Acceptance Test **before** writing any code
2. The Acceptance Test acts as an "Executable Specification"
3. Developers use fine-grained TDD to create code that meets the specification
4. This combination reduces defects by **often two orders of magnitude**

**Properties of Effective Acceptance Tests:**
- Written from the perspective of an **external user** of the system
- Evaluate the system in **life-like scenarios**
- Evaluated in **production-like test environments**
- Interact with the System Under Test (SUT) through **public interfaces only** (no back-door access)
- Focus only on **what** the system does, not **how** it does it

**Tips for Writing Good Acceptance Tests:**
- Imagine the least technical person who understands the problem domain reading your tests—they should make sense to that person
- Imagine replacing your entire system with something completely different that achieves the same goals—your tests should still make sense
- Example: Testing buying a book on Amazon. Could your tests work just as well for a robot shopping in a physical bookstore?
- Avoid tests that say "fill in this field" or "click this button"—instead say "placeAnOrder" or "payByCreditCard"
- Adopt the **language of the problem domain** exclusively
- Make test scenarios **atomic**—don't share test data between test cases
- Each test case should start from the assumption of a running, functioning system with no data

---

## Four-Layer Separation of Concerns

The guide introduces a four-layer architecture for organizing test code:

### Layer 1: Test Cases
- Written in the language of the problem domain
- From the perspective of an external user
- Example: `shouldBuyBookWithCreditCard()` — a sequence of domain-level actions like `shopping.goToStore()`, `shopping.searchForBook()`, `shopping.checkOut()`

### Layer 2: Domain Specific Language (DSL)
- Shared between test cases
- Designed to make it easy to write test cases
- Allows precision where needed and skims over detail where it's not
- Best practice: use **optional parameters** for nearly everything
- Encodes common start-up tasks (e.g., "registering users", "populating accounts")
- Keeps focus on **domain-level concepts**, free from implementation details
- Example: `checkOut(String... args)` method that parses optional parameters for item, price, card with sensible defaults

### Layer 3: Protocol Drivers
- Translators/adaptors that translate from the DSL to the "language of the system"
- Pattern: mirror the DSL interface (`dsl.checkOut` calls `driver.checkOut` with more specific parameters)
- The DSL parses parameters and fills in detail; Protocol Drivers encode real interactions with the SUT
- Create a new Protocol Driver for **each different channel** of communication supported by the SUT
- Isolate **all test infrastructure knowledge** of the system here
- Example: A web-based Protocol Driver that navigates to cart pages, finds elements by XPath, and asserts visibility

### Layer 4: System Under Test (SUT)
- Deploy the system using the **same tools and techniques** as production deployment
- This allows Acceptance Tests to evaluate any change to production, including config, OS version, DB version
- Use **Infrastructure-as-Code** techniques to manage both test and production environments
- "Production-like" means the SUT **can't tell the difference** in how it's deployed or configured
- Optimize where possible—e.g., make system startup **fast**

---

## Growing the DSL

**Pragmatic approach to building your test infrastructure:**

1. Start by creating **two or three simple test cases** that exercise the most common/valuable behavior of your system
2. Even at this early level, expect some re-use in the DSL
3. Create the infrastructure that allows these tests to execute and pass
4. Adopt the discipline that **every Acceptance Criteria for every User Story** gets a new Acceptance Test
5. Drive all new development from these tests
6. Invent the language needed to express a test case at the time of writing the test—don't worry about implementation

**Who writes what:**
- **Anyone** can write a test case: QA, BA, PO, Dev
- **Developers/Dev teams own the tests**—if a test breaks, a Dev should notice first
- Devs own responsibility for writing the plumbing (DSL and Protocol Drivers) that make the tests work

---

## Key Takeaways

1. **Write Acceptance Tests before code**: Treat them as executable specifications that guide your development.

2. **Think from the outside in**: Write tests from the perspective of an external user, through public interfaces, focused on outcomes not implementation.

3. **Use the language of the problem domain**: Tests should use business language (placeAnOrder, payByCreditCard), not technical language (fillInField, clickButton).

4. **Four-layer separation of concerns**: Test Cases → DSL → Protocol Drivers → System Under Test. Each layer has a clear responsibility.

5. **Make tests atomic and independent**: No shared test data between cases. Each test starts from a clean, running system.

6. **Production-like test environments**: Deploy using the same infrastructure-as-code as production. The SUT shouldn't be able to tell it's in a test environment.

7. **Grow your DSL pragmatically**: Start with a few simple test cases, build the infrastructure, then adopt the discipline of writing an Acceptance Test for every User Story.

8. **Developers own the tests**: While anyone can write test cases, developers are responsible for the plumbing (DSL and Protocol Drivers) and should notice failures first.

9. **ATDD + TDD = orders of magnitude fewer defects**: The combination of Acceptance Tests as specifications with fine-grained TDD for implementation produces dramatically higher quality software.

10. **This takes discipline and time but delivers enormous value**: Organizations that adopt this approach seriously see massive savings in time and significant increases in quality.
