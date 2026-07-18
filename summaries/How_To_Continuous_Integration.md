# How To - 10 Tips for Continuous Integration - Dave Farley

## Comprehensive Summary

---

## Overview

This is a concise guide from Dave Farley's "Better Software Faster" How To series, focused on Continuous Integration (CI) as a critical practice for effective software development. The guide presents 10 actionable tips for teams to adopt CI discipline, framed within the broader context of Continuous Delivery and Extreme Programming practices.

---

## What Is Continuous Integration?

### The Problem: Integration Hell

When developing software, one of the most complex, difficult, and frustrating tasks is bringing diverse pieces of work together into a functioning system. Teams need to know that the code they're writing works with everyone else's code — and they need to know this **early and often**.

### The CI Solution

Continuous Integration is one of the Extreme Programming disciplines, first described on the C2 wiki by Kent Beck and others. The core assertion: **code ownership conflicts are minimized when engineers don't hold onto a module for more than a moment.** When correct changes are available to everyone almost instantly:

- The system is **always integrated**
- There is only **one interesting version** — the current one
- The route to production stays **open and moving**

### CI vs Branching

CI means **little or no branching**. Instead of dividing up work and working on separate pieces independently:

- Make **small changes to Trunk/Master** and continuously evaluate them
- If branches exist at all, they must be **tiny and short-lived** — no longer than a day
- The DORA (DevOps Research & Assessment) reports found that **merging frequently is a reliable predictor of higher throughput, stability, and overall software performance**

### What "Continuous" Really Means

"Continuous" means **at least very often**:

- Commit **at least once per day** as a minimum, but probably more often than you think
- Evaluate changes **as frequently as possible**
- Get feedback **multiple times a day**
- Have **several chances to fix any problems** that same day

### CI and Continuous Delivery

CI is an extremely important practice for Continuous Delivery because:

- The goal is to maintain software in a **releasable state**
- Keep the **route to production open and moving**
- Don't stall while fixing problems
- Don't leave bugs to be fixed later

### CI Is a Team Discipline, Not Just a Tool

CI is not just a technical discipline. While great CI tools are available, the biggest impact comes from:

- **How we think about making a change**
- **The approach we take as individuals within a team**
- These techniques are an effective way to **build collaborative teams**

---

## The 10 Tips for Continuous Integration

### Tip 1: Work in Small Steps

Commit and test **small changes**, not whole features.

**Why small changes matter:**
- Less likely to hide complex problems
- Simpler to test
- Easier to fix when things go wrong

This is the foundational principle. If you can't commit small changes, none of the other tips work effectively.

### Tip 2: Run Commit Tests Locally First

Before pushing to the shared repository, run commit tests locally to find potential failures **before impacting the rest of the development process**.

This is a courtesy to the team — catching obvious problems locally is faster for everyone and doesn't consume shared CI resources for trivial failures.

### Tip 3: Commit Every 10-15 Minutes, Get Feedback in Under 5 Minutes

**The rhythm of CI:**
- Aim to commit every **10-15 minutes**
- Get feedback in **under 5 minutes**
- **Wait patiently** for test results (it's only 5 minutes!)

**Why wait?** If there are any failures, you (as the committer) are the best person to understand the problem, find, and implement a solution. Your context is freshest immediately after writing the code.

### Tip 4: Own Your Changes

It is **your responsibility** to see if your changes are successful. Monitor progress through all evaluations:

- Fast **unit tests**
- Longer-running **acceptance tests**
- Other evaluations

Don't "fire and forget" your commits. Stay engaged with the build pipeline until your changes pass all evaluations.

### Tip 5: Fix Any Failure in 10 Minutes (Or Revert)

**The 10-minute rule:**
- Aim to fix any failure within **10 minutes**
- If you can't fix it in 10 minutes, **revert the change**
- Work offline to solve the problem
- Don't impede others' progress

This is crucial: **keeping the build green is more important than any individual change.** A broken build blocks everyone.

### Tip 6: Revert Teammates' Changes If They Don't Fix Failures

If a teammate does not stick around to see the results of their tests or fix a failure:

- **Revert their change** to keep the route to production open
- This is not punitive — it's about protecting the team's velocity
- They can always re-commit once they've fixed the problem

### Tip 7: Collaborate to Resolve Ambiguous Failures

As a team, **prioritize finding and fixing failures quickly** to keep the software in a releasable state.

If it's not clear whose change caused a failure:
- Get together with the other committers who could have caused the problem
- Agree who will fix it
- Fix it quickly, together if needed

### Tip 8: Gamify Build Discipline

The team can encourage adherence to good CI behaviors through gamification of "Build Sins":

- **Wear a silly hat** when you break the build
- **Put money in the build sin jar** (like a swear jar)
- Have an **instant alert system** to notify the whole team about a failure

The goal is to create positive social pressure around build discipline without being punitive.

### Tip 9: Adopt Test-Driven Development (TDD)

Farley strongly recommends TDD as a complementary practice to CI:

- Write tests **before** writing code
- This ensures every change has test coverage
- TDD provides the rapid feedback loop that CI depends on
- TDD and CI together create a powerful discipline for producing working software

### Tip 10: Build a Deployment Pipeline

Farley promotes building and using a **Continuous Delivery Deployment Pipeline**:

- The best way to organize software development and testing processes into one efficient "machine"
- A deployment pipeline automates the progression from commit through various stages of testing
- Each stage provides increasing confidence that the change is safe to release
- The pipeline makes the state of the software **visible** to everyone

---

## The Underlying Philosophy

### Small Batches Are Everything

The recurring theme across all 10 tips is the power of **small batches**:

- Small commits are easier to understand, test, and fix
- Frequent integration reduces merge conflicts to near zero
- Fast feedback means problems are caught when context is fresh
- A releasable codebase is always maintained

### The Build as a Shared Resource

The build (the state of trunk/master) is a **shared team resource**:

- Keeping it green is everyone's responsibility
- Breaking it blocks everyone
- Fixing it is the team's highest priority
- Individual changes are subordinate to the health of the build

### CI as Collaborative Culture

CI is fundamentally about **team collaboration**:

- It forces communication (whose change broke the build?)
- It creates shared accountability (we all own the build)
- It encourages helping each other (pairing on fixes)
- It builds trust (the codebase is always in a known-good state)

---

## Connections to Broader Practices

### Extreme Programming (XP)

CI originated as one of the core XP practices. The other XP practices that support CI:

- **Pair programming**: Real-time code review catches issues before commit
- **Collective code ownership**: Anyone can change any code, enabled by frequent integration
- **Sustainable pace**: Frequent commits prevent crunch-time integration hell
- **Refactoring**: Safe refactoring depends on a comprehensive test suite run by CI

### Continuous Delivery

CI is the **foundation** of Continuous Delivery:

- Without CI, you can't maintain a releasable codebase
- Without a releasable codebase, you can't release on demand
- The deployment pipeline extends CI into a full delivery workflow

### DevOps Research & Assessment (DORA)

The DORA reports provide **empirical evidence** that CI practices correlate with:

- Higher **deployment frequency**
- Lower **lead time for changes**
- Lower **change failure rate**
- Faster **mean time to recovery**

These are the four key metrics that distinguish high-performing technology organizations.

---

## Key Takeaways

1. **CI is the antidote to integration hell**: Integrate continuously, not in big-bang merges. The system should always be integrated.

2. **Small changes, committed frequently**: Every 10-15 minutes. Small changes are simpler to test, understand, and fix.

3. **No long-lived branches**: If branches exist at all, they should be tiny and short-lived (no more than a day). Work on trunk.

4. **Commit at least daily, ideally much more**: Multiple commits per day means multiple chances to catch and fix problems.

5. **Run tests locally first**: Catch trivial failures before they consume shared CI resources or block teammates.

6. **Own your changes end-to-end**: Monitor your commit through all pipeline stages. Don't fire and forget.

7. **Fix or revert within 10 minutes**: A broken build blocks everyone. If you can't fix quickly, revert and solve offline.

8. **Revert teammates' broken changes**: Not punitive — protective. The build's health is more important than any individual change.

9. **Adopt TDD**: Test-driven development provides the rapid feedback loop that makes CI practical and effective.

10. **Build a deployment pipeline**: Automate the progression from commit through testing stages. Make the software's state visible to all.

11. **CI builds collaborative teams**: The discipline of CI forces communication, shared accountability, and mutual trust.

12. **The build is a shared resource**: Keeping it green is the team's highest priority. Everything else is secondary.

---

## Further Resources

- **Dave Farley's Continuous Delivery YouTube channel**: Video content on CI, TDD, and deployment pipelines
- **Dave Farley's online courses**: In-depth training on Continuous Delivery practices
- **Continuous Delivery** (book): Jez Humble and Dave Farley's comprehensive guide to the discipline
- **DORA State of DevOps Reports**: Empirical research on what distinguishes high-performing engineering organizations
