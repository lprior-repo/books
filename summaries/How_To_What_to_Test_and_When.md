# Summary: What to Test, and When? -- Dave Farley's Better Software Faster How-To Guide

This summary covers Dave Farley's concise but powerful framework for building a holistic testing strategy within a Continuous Delivery pipeline. The guide presents a four-phase model -- Commit, Acceptance, Release, and Production -- that defines what to test at each stage of the software delivery lifecycle. Farley's central thesis is that testing is not confined to a single moment before release; rather, it is a continuous activity that runs from the first line of code through to live production operation, and each phase demands a distinct set of testing techniques with different goals, scopes, and speeds.

Farley is the co-author of the seminal "Continuous Delivery" book (with Jez Humble), author of "Continuous Delivery Pipelines" and "Modern Software Engineering," and runs the Continuous Delivery YouTube channel. His perspective is grounded in decades of hands-on experience building high-performance engineering organizations, including leading the team that built the Distributed Systems Replacements programme at LMAX (one of the first and most significant examples of modern Continuous Delivery in practice).

---

## Chapter 1: The Core Philosophy -- Continuous Delivery and the Feedback Imperative

### Continuous Delivery as a Learning System

The guide opens with a foundational statement: "Continuous Delivery gets us fast and frequent feedback from our customers and our tests, to enable us to learn, make evidence-based decisions and improve our software." This sentence captures the essence of Farley's approach. Testing is not a phase; it is a feedback mechanism. The entire purpose of a testing strategy is to accelerate learning -- learning whether the code does what the developer intended, whether it does what the user needs, whether it performs adequately, and whether it continues to work correctly once deployed.

This feedback-centric view stands in contrast to traditional testing approaches where testing is a gate-keeping activity performed by a separate QA team at the end of development. In Farley's model, testing is woven into every stage of the delivery pipeline, and each stage serves a different purpose in the feedback loop.

### The Four-Phase Framework

Farley proposes that the testing landscape can be organized into four distinct phases, each aligned with a specific point in the software delivery process:

1. **At Commit** -- Development-supporting tests. Fast, lightweight, technical tests that give developers rapid feedback and confirm that the code behaves as the developer expects.
2. **Acceptance** -- Defining releasability. More user-centered tests that evaluate the code from the users' perspective, plus everything else needed to confirm that the software is sufficiently fast, scalable, secure, and resilient.
3. **At Release** -- What we need to check at the point of releasing software into production.
4. **In Production** -- How to understand software performance once live, what customers make of it, and what can be learned to inform business and technical decisions.

Each phase has a guiding principle. The Commit phase is about anything that can "FAIL FAST." The Acceptance phase covers anything that defines "RELEASABLE." The Release phase covers anything that "SUPPORTS RELEASE." The Production phase covers anything that "Informs PRODUCT DESIGN."

The framework is deliberately simple -- it is meant to be a practical decision-making tool for teams building their testing strategy, not an academic taxonomy.

### Why This Framework Matters

Many organizations struggle with testing because they approach it as an undifferentiated activity -- "we need more tests" or "we need better tests" -- without considering when different types of tests are most effective and what purpose they serve at each stage. Farley's framework brings clarity by attaching each testing technique to a specific moment in the delivery process and a specific goal. This prevents two common failures: over-testing at expensive stages (writing too many slow end-to-end tests) and under-testing at critical stages (neglecting production monitoring or skipping configuration tests).

The framework also helps teams make investment decisions. Resources for testing are finite, and Farley's model provides a rational basis for allocating those resources. A team with limited time and budget should invest first in a strong Commit stage (fast unit tests and static analysis), then build out Acceptance tests for their most critical user journeys, then automate their release process with smoke tests and canary analysis, and finally invest in production observability and experimentation.

### The Distinction Between Testing and Checking

An important nuance in Farley's framework is the implicit distinction between testing as an exploratory, learning-oriented activity and checking as a verification-oriented activity. At the Commit stage, the emphasis is on checking: verifying that the code behaves as specified. At the Acceptance stage, there is a mix of checking (do the acceptance criteria pass?) and testing (does the system actually work in a production-like environment?). At the Release stage, the emphasis shifts back to checking (are the health checks passing?). But at the Production stage, the emphasis is squarely on learning: understanding how real users interact with the system, what performance looks like under real conditions, and which features actually deliver value.

This distinction is important because it explains why no single stage is sufficient on its own. Checking without learning gives you false confidence. Learning without checking gives you no baseline quality. Both are necessary, and Farley's framework provides the structure to do both effectively.

---

## Chapter 2: At Commit -- Development-Supporting Tests

### The Goal: Fail Fast

The Commit stage is the first line of defense and the fastest feedback loop in the entire pipeline. Its guiding principle is "FAIL FAST." The tests and checks at this stage are designed to run quickly (typically within minutes) and to catch problems as early as possible in the development process, ideally within the developer's own workflow before code is even pushed to a shared repository.

The Commit stage is where developers live. It is their safety net. Every time a developer makes a change, the commit-stage tests should give them confidence that their change is correct, that it has not broken anything obvious, and that it meets basic quality standards.

### Unit Tests

Unit tests are the cornerstone of the Commit stage. These are fast, isolated tests that verify the behavior of small units of code -- typically individual functions, methods, or classes. Unit tests are the developer's primary tool for confirming that the code they have written does what they intended it to do.

Farley's approach to unit tests is closely aligned with Test-Driven Development (TDD), a practice he strongly advocates. In TDD, developers write a failing test before they write the implementation code. This ensures that every piece of production code is covered by at least one test, and that the tests serve as a specification for the code's behavior. The TDD cycle -- Red, Green, Refactor -- provides a tight feedback loop that keeps developers focused and confident.

Good unit tests are:
- **Fast**: They should execute in milliseconds. A full suite of thousands of unit tests should complete in seconds, not minutes.
- **Isolated**: Each test should test one thing and should not depend on external systems, databases, file systems, or network calls. Dependencies should be replaced with test doubles (mocks, stubs, or fakes).
- **Repeatable**: Running the same test multiple times should always produce the same result, regardless of the environment or execution order.
- **Self-checking**: The test should automatically determine whether it passed or failed without human judgment.
- **Timely**: Written at the same time as (or before) the production code.

### Coding Standards Enforcement

Automated coding standards checks are an important part of the Commit stage. These include tools like linters, formatters, and style checkers that enforce consistent code formatting and naming conventions across the team. While these may seem trivial, consistent code style reduces cognitive load during code reviews, prevents certain classes of bugs, and makes the codebase more maintainable.

Most modern languages have well-established linting and formatting tools (e.g., rustfmt and clippy for Rust, ESLint and Prettier for JavaScript, Checkstyle for Java). These should be automated as part of the build process and ideally integrated into the developer's IDE for immediate feedback.

### Static Analysis

Static analysis tools go beyond style checking to examine the code's structure and patterns without executing it. They can detect potential bugs, security vulnerabilities, code complexity issues, unused variables, unreachable code, and common anti-patterns. Examples include SonarQube, Coverity, and language-specific tools like Clippy (Rust) or PyLint (Python).

Static analysis is valuable at the Commit stage because it catches issues that unit tests might miss -- particularly structural and security-related problems. It is also extremely fast, as it does not require code execution.

### Asserted Common Error Detection

This category covers automated checks that detect common programming errors specific to the language or framework being used. These include null pointer dereferences, buffer overflows, integer overflows, resource leaks, and other classes of bugs that are frequent sources of production failures.

Many modern languages and compilers include built-in checks for these kinds of errors (e.g., Rust's borrow checker, Go's nil pointer checks), but additional tooling can catch more subtle issues. Fuzz testing, for example, can be used at the Commit stage to automatically generate random inputs and detect crashes or unexpected behavior.

### Data Migration Unit Tests

Data migration tests at the Commit stage verify that database schema changes and data transformations are correct. When a developer modifies a database schema or writes a migration script, they should also write unit tests that confirm the migration produces the expected result. This is critically important because incorrect data migrations are one of the most common causes of production incidents.

These tests typically verify that:
- The migration script runs without errors
- Data is transformed correctly from the old schema to the new schema
- The migration is idempotent (running it multiple times produces the same result)
- Rollback migrations work correctly

### The Economics of the Commit Stage

The Commit stage should be optimized for speed. Developers should be able to run these tests locally in seconds, and the CI system should run them within a few minutes of a commit. If the Commit stage takes too long, developers will skip running tests locally, defeating the purpose of fast feedback.

A common guideline is that the entire Commit stage should complete in under five minutes, with the unit test suite itself completing in under two minutes. This requires disciplined test design: avoiding slow tests (database interactions, network calls, file I/O), keeping the test suite lean, and periodically reviewing and removing redundant or slow tests.

### The Psychological Importance of Fast Feedback

The emphasis on speed at the Commit stage is not merely a technical optimization. It has profound psychological implications for developer productivity and morale. When tests run in seconds, developers run them frequently -- often after every small change. This creates a tight feedback loop where errors are caught immediately, when the context is fresh in the developer's mind and the fix is trivial. When tests take minutes or hours, developers batch changes and run tests less frequently, which means errors are discovered later when the developer has moved on to other tasks and the cost of context-switching back to fix the bug is much higher.

Research in developer productivity consistently shows that the most productive developers work in tight feedback loops. The Commit stage is the primary mechanism for creating these tight feedback loops in a CI/CD environment. Investing in fast, reliable unit tests and quick static analysis is one of the highest-return investments a team can make.

### What Belongs in the Commit Stage vs. Later Stages

A common question when implementing Farley's framework is: where does a particular test belong? The answer depends on the test's purpose, speed, and scope:

- If a test runs in milliseconds and tests a single unit of logic, it belongs in the Commit stage.
- If a test requires a database, file system, or network connection, it probably belongs in a later stage (though it might be appropriate at the Commit stage if the dependency is mocked or replaced with an in-memory substitute).
- If a test verifies end-to-end user behavior, it belongs in the Acceptance stage.
- If a test verifies the deployment process, it belongs in the Acceptance or Release stage.
- If a test verifies behavior under real production conditions, it belongs in the Production stage.

The key principle is: tests should run at the earliest stage where they can provide meaningful feedback. Don't defer a fast, valuable test to a later stage, but also don't force a slow, expensive test into the Commit stage where it will slow down the feedback loop for everyone.

---

## Chapter 3: Acceptance -- Defining Releasability

### The Goal: Anything That Defines Releasable

The Acceptance stage is where the testing focus shifts from developer-centric concerns to user-centric and system-centric concerns. The guiding question is: "Is this software releasable?" Releasability means not just functional correctness but also adequate performance, scalability, security, resilience, and compliance with any regulatory or business requirements.

This stage is typically executed in a CI/CD pipeline after the Commit stage passes. It runs against a more production-like environment and exercises the system at a higher level of integration.

### Acceptance Tests (BDD-Style Executable Specifications)

Acceptance tests are the centerpiece of this stage. Farley advocates for Behavior-Driven Development (BDD) style executable specifications as the primary form of acceptance testing. These tests describe the system's behavior from the user's perspective using a structured, readable format (such as Gherkin: Given-When-Then) that serves as both documentation and automated test.

Key characteristics of effective acceptance tests:
- They are written in the language of the business domain, not the language of the implementation
- They describe what the system should do, not how it should do it
- They are automated and executable as part of the deployment pipeline
- They serve as "living documentation" that is always up-to-date because it is validated by the CI system
- They define the minimum bar for releasability -- if all acceptance tests pass, the software should be potentially releasable

Acceptance tests operate at a higher level than unit tests. They typically exercise the system through its external interfaces (APIs, UIs, message queues) and verify end-to-end behavior. However, they should still be reasonably fast -- the goal is to get feedback within tens of minutes, not hours.

Frameworks like Cucumber, SpecFlow, and FitNesse support this style of testing, allowing stakeholders, product owners, and testers to collaborate on defining acceptance criteria in a format that can be automated.

### Deployment Tests

Deployment tests verify that the software can be successfully deployed to the target environment. These tests check that installation scripts work, configuration is correct, services start properly, health checks pass, and the system is reachable after deployment.

Deployment tests are important because deployment failures are a common source of production incidents. By testing the deployment process itself, teams can catch configuration errors, missing dependencies, and environmental issues before they affect users.

### Configuration Tests

Configuration tests verify that the software is correctly configured for the target environment. This includes checking database connection strings, API endpoints, feature flags, security settings, and any other environment-specific configuration.

Configuration errors are remarkably common and remarkably dangerous. A single incorrect configuration value can cause a complete outage. Configuration tests catch these errors before the software reaches production by verifying that all required configuration is present, correctly formatted, and within acceptable ranges.

Farley references the importance of treating configuration with the same rigor as code. Configuration should be version-controlled, tested, and deployed through the same pipeline as application code. As Jamie Wilkinson (a Google SRE) has noted: "Config pushes need to be treated with at least the same care as you do with program binaries, and I argue more because unit testing config is difficult without the compiler."

### Security Tests

Security testing at the Acceptance stage includes automated scans for known vulnerabilities (dependency scanning, SAST/DAST), authentication and authorization verification, input validation testing, and checks for common security issues (SQL injection, XSS, CSRF, etc.).

Security testing should not be left until the end of the development process. By integrating security tests into the Acceptance stage, teams can catch vulnerabilities early and prevent them from reaching production. Tools like OWASP ZAP, Snyk, and SonarQube can automate many security checks.

### Data Migration Tests

While data migration unit tests at the Commit stage verify the correctness of individual migration scripts, the Acceptance-stage data migration tests verify that migrations work correctly against realistic data volumes and schemas. These tests may run against a copy of the production database or a synthetic dataset that mimics production characteristics.

### Performance Tests

Performance testing at the Acceptance stage verifies that the software meets its performance requirements. This includes response time tests, throughput tests, and resource utilization tests. Performance tests should be run against a production-like environment with realistic data volumes and load patterns.

Performance testing is not optional. Software that is functionally correct but too slow is not releasable. Performance requirements should be defined as quantifiable acceptance criteria (e.g., "the API must respond to 95% of requests within 200ms under a load of 1000 requests per second") and tested automatically as part of the pipeline.

### Scalability Testing

Scalability testing goes beyond performance testing to verify that the system can handle growth in load, data volume, or user count. This might involve testing horizontal scaling (adding more instances), vertical scaling (increasing resources), or testing the system's behavior under extreme load.

Scalability testing is particularly important for systems that experience variable or rapidly growing load. It answers the question: "Can this system handle ten times the current traffic if we need it to?"

### Resilience Testing

Resilience testing verifies that the system can withstand and recover from failures. This includes testing behavior when dependencies are unavailable, when the network is unreliable, when resources are exhausted, and when individual components fail.

Resilience testing bridges the gap between the Acceptance stage and what is done in production with Chaos Engineering (discussed later). At the Acceptance stage, resilience tests are typically controlled and predictable -- for example, simulating a database failure and verifying that the system degrades gracefully rather than crashing.

### Compliance Testing

For organizations subject to regulatory requirements (GDPR, HIPAA, PCI-DSS, SOX, etc.), compliance testing at the Acceptance stage verifies that the software meets relevant regulatory standards. This might include verifying data encryption, access controls, audit logging, data retention policies, and privacy controls.

Automating compliance checks reduces the cost and risk of compliance audits and ensures that compliance is continuously maintained rather than checked intermittently.

### The Scope of the Acceptance Stage

The Acceptance stage is the broadest and most varied stage in Farley's framework. It encompasses functional testing (acceptance tests, data migration tests), non-functional testing (performance, scalability, resilience, security), operational testing (deployment tests, configuration tests), and regulatory testing (compliance). This breadth is intentional: the Acceptance stage is where the team confirms that the software is not just "working" but "ready for real users."

A common mistake is to treat the Acceptance stage as only functional testing. In practice, the non-functional aspects -- performance, security, resilience -- are often more important determinants of releasability than functional correctness. A feature that works perfectly in isolation but takes ten seconds to respond under load is not releasable. A feature that is functionally correct but exposes user data through an API vulnerability is not releasable. Farley's framework makes this explicit by placing all of these concerns under the umbrella of "defining releasable."

### The Relationship Between Acceptance Tests and Unit Tests

Acceptance tests and unit tests serve complementary purposes. Unit tests verify that individual components work correctly in isolation. Acceptance tests verify that those components work correctly together to deliver user value. Both are necessary, and neither is sufficient on its own.

A team with strong unit tests but weak acceptance tests may have components that work individually but fail when integrated. A team with strong acceptance tests but weak unit tests may have end-to-end functionality that works but is difficult to refactor because there is no safety net at the component level.

The ideal ratio between unit tests and acceptance tests follows the test pyramid: many more unit tests than acceptance tests. This is because unit tests are cheap, fast, and precise (they tell you exactly what broke), while acceptance tests are expensive, slower, and less precise (they tell you something is broken but not necessarily where). However, the acceptance tests provide a different kind of confidence: they verify that the system as a whole delivers the expected behavior from the user's perspective.

### Testing Through External Interfaces

Farley advocates that acceptance tests should exercise the system through its external interfaces -- APIs, user interfaces, message queues, and other entry points. This approach provides several advantages:

First, it decouples the tests from the implementation. Because the tests interact with the system through the same interfaces that users (or other systems) use, they continue to work even when the internal implementation changes. This makes the tests more stable and maintainable.

Second, it tests the system at the right level of abstraction. Users do not care about internal implementation details; they care about behavior. Acceptance tests that exercise external interfaces verify the behavior that users actually care about.

Third, it forces the team to design clean, well-defined interfaces. If the external interfaces are difficult to test, they are probably also difficult to use, which is a signal that the interface design needs improvement.

---

## Chapter 4: At Release -- Supporting the Release Process

### The Goal: Anything That Supports Release

The Release stage focuses on the moment of truth: when software is about to be exposed to real users. The testing at this stage is not about finding bugs (that should have been done in earlier stages) but about verifying that the release process itself is working correctly and that the software is behaving as expected in the production environment.

### Smoke Tests and Health Checks

Smoke tests (also called build verification tests or sanity checks) are a small set of critical tests that verify the most important functionality of the system. They are designed to run quickly and to catch catastrophic failures. The term comes from hardware testing: if the device smokes when you turn it on, you do not need to run more detailed tests.

Smoke tests typically verify:
- The application starts correctly
- Key API endpoints respond
- The database is accessible
- Authentication works
- Critical user journeys can be completed

Health checks are a related concept: automated endpoints or probes that report whether a service is healthy and ready to receive traffic. In containerized environments (Kubernetes, ECS), health checks are used by the orchestration system to determine whether a container should receive traffic or be restarted.

### Canary Release Testing

Canary release is a deployment strategy where a new version of the software is released to a small percentage of users or servers before being rolled out to everyone. The canary release is monitored closely, and if any problems are detected, the release is automatically rolled back.

Canary release testing involves:
- Deploying the new version to a small subset of infrastructure
- Routing a small percentage of traffic to the new version
- Comparing key metrics (error rate, latency, throughput) between the canary and the baseline
- Automatically rolling back if the canary metrics degrade beyond acceptable thresholds

Tools like Spinnaker, Flagger, and Argo Rollouts support automated canary analysis and rollback. The key metrics to monitor during a canary are typically few in number (3-5) but highly indicative of system health: error rate, response time (e.g., p99 latency), and request rate.

### Monitoring

Monitoring during release is critical. While monitoring is a continuous activity, it takes on heightened importance during a release. The monitoring system should be able to detect regressions in key metrics and alert the team (or the automated deployment system) to roll back if necessary.

Effective release monitoring focuses on a small number of high-signal metrics. Facebook's Kraken system, for example, uses just two topline metrics: the web server's 99th percentile response time and HTTP fatal error rate, as reliable proxies for user experience.

The goal is to detect problems quickly and reliably, not to monitor everything. Too many signals create noise and make it harder to identify real issues.

### Exception Tracking

Exception tracking tools (such as Sentry, Rollbar, or Bugsnag) capture and aggregate unhandled exceptions and errors from the running application. During a release, exception tracking provides immediate visibility into any new errors introduced by the release.

Exception trackers provide rich context for debugging: stack traces, local variables, request parameters, user information, and breadcrumbs showing what happened before the error. This makes them invaluable for quickly diagnosing and triaging issues discovered during a release.

Exception tracking should be integrated into the release process so that a spike in new exceptions triggers an alert and potentially an automatic rollback.

### The Distinction Between Deploy and Release

A crucial concept that Farley's framework highlights is the distinction between deployment and release. Deployment is the process of installing new code on production infrastructure. Release is the process of routing production traffic to that new code. These are separate activities, and decoupling them enables safer, more controlled testing during the release process.

When deployment and release are decoupled, teams can deploy new code to production without immediately exposing users to it. This creates opportunities for testing that would not otherwise be possible:
- The deployed code can be tested in the actual production environment before any traffic is routed to it.
- Traffic can be gradually shifted to the new code using canary releases.
- If problems are discovered, traffic can be immediately shifted back to the old code without a full rollback.

This distinction is essential for implementing canary releases, blue-green deployments, and other progressive delivery strategies. Teams that conflate deployment with release are forced into a binary choice: either the new code is serving users or it is not. Teams that separate them have a continuum of options for gradually and safely rolling out changes.

### Automated Rollback as a Testing Strategy

Automated rollback is not typically thought of as a testing technique, but in Farley's framework it plays a critical role in the Release stage. The ability to automatically detect problems and roll back to a known-good state is what makes progressive delivery strategies safe.

Automated rollback works by:
1. Defining a set of key metrics that indicate system health (error rate, latency, throughput)
2. Comparing these metrics between the new version (canary) and the old version (baseline)
3. If the canary metrics degrade beyond predefined thresholds, automatically routing traffic back to the baseline
4. Alerting the team that a rollback occurred so they can investigate the root cause

This automation is critical because human response times are too slow for production incidents. A canary release that starts causing errors should be rolled back within seconds, not minutes or hours. Only automated systems can achieve this speed of response.

The key metrics for automated rollback should be chosen carefully. They should be:
- **High-signal**: Directly indicative of user experience
- **Low-noise**: Not prone to false positives from normal variance
- **Fast-responding**: Changes should be detectable within seconds to minutes
- **Actionable**: A degradation in the metric should clearly warrant a rollback

Facebook's approach of using just two metrics (p99 response time and HTTP fatal error rate) is a good model. These two metrics capture the most important aspects of user experience and are fast-responding enough to trigger rollback before significant user impact occurs.

---

## Chapter 5: In Production -- Learning and Improving

### The Goal: Anything That Informs Product Design

The Production stage is where the testing strategy extends beyond preventing failures to actively learning and improving. The guiding principle here is "Anything that Informs PRODUCT DESIGN." This is a significant shift in mindset: testing in production is not just about finding bugs but about understanding how the software performs in the real world and using that understanding to make better decisions.

Farley's framework makes explicit something that many organizations overlook: the majority of learning about software quality happens after release. Production is where real users interact with the software under real conditions, and this interaction produces a wealth of information that no pre-release testing can replicate.

### Capacity Monitoring

Capacity monitoring tracks the system's resource utilization and ability to handle current and projected load. This includes CPU usage, memory consumption, disk I/O, network bandwidth, database connections, and other resource metrics. Capacity monitoring answers the question: "Do we have enough headroom to handle expected growth?"

Capacity monitoring should trigger alerts when resource utilization approaches dangerous thresholds, giving the team time to scale up or optimize before users are affected.

### Technical Monitoring

Technical monitoring covers the health and performance of the system's technical infrastructure. This includes server health, network connectivity, service dependencies, message queue depths, cache hit rates, and other infrastructure-level metrics.

Technical monitoring provides the operational visibility needed to keep the system running smoothly and to diagnose issues when they arise. It is the foundation of operational excellence.

### Performance Verification

Performance verification in production goes beyond the synthetic performance tests run during the Acceptance stage. It measures actual performance as experienced by real users, taking into account real network conditions, real data volumes, and real usage patterns.

This includes measuring response times, throughput, and error rates from the user's perspective. Real User Monitoring (RUM) tools capture this data from actual user sessions, providing a ground truth that synthetic tests cannot match.

Performance verification in production can reveal issues that are impossible to detect in testing environments: the impact of network latency on mobile users, the effect of geographic distance on response times, or the performance impact of specific data patterns that only appear in production.

### Security Verification

Security verification in production includes ongoing monitoring for security threats, detection of unauthorized access attempts, vulnerability scanning of the production environment, and verification that security controls are functioning as intended.

This also includes monitoring for security incidents, such as unusual access patterns, data exfiltration attempts, or denial-of-service attacks. Security in production is not a one-time check but a continuous activity.

### A/B Testing

A/B testing is a powerful technique for making evidence-based decisions about product design. It involves releasing two versions of a feature (version A and version B) to different subsets of users and measuring which version performs better against predefined metrics.

Farley references research from Microsoft showing that approximately two-thirds of ideas produce zero or negative value. This statistic underscores the importance of A/B testing: without it, teams are flying blind, making assumptions about what users want without evidence. A/B testing provides the evidence needed to make informed product decisions.

A/B testing in the context of a testing strategy is not just a marketing or product management tool. It is a testing technique that validates hypotheses about user behavior and software quality in the most realistic possible environment: with real users, real data, and real conditions.

### Business Experiments in Production

Beyond simple A/B tests, production environments enable more sophisticated business experiments. These might include testing different pricing models, different user flows, different recommendation algorithms, or different content layouts. The key insight is that production is the only environment where you can get statistically valid data about how changes affect real business outcomes.

Business experiments in production require careful experimental design, proper statistical analysis, and a culture of evidence-based decision making. They represent the highest maturity level of the testing strategy: using production data not just to prevent failures but to actively improve the product.

### Commercial Performance Monitoring

Commercial performance monitoring tracks business-level metrics: conversion rates, revenue, user engagement, churn, and other KPIs. These metrics provide the ultimate feedback on whether the software is fulfilling its purpose.

While technical metrics tell you whether the system is working correctly, commercial metrics tell you whether it is working effectively. A system can be technically flawless but commercially unsuccessful if it does not meet user needs.

### The Three Pillars of Observability

Farley's Production stage implicitly relies on what the observability community calls the "three pillars": logs, metrics, and distributed traces. Each provides a different lens through which to understand production behavior:

- **Logs** record discrete events with rich contextual information. They are essential for debugging specific incidents and understanding the sequence of events that led to a problem.
- **Metrics** aggregate numerical data over time (counters, gauges, histograms). They are essential for detecting trends, setting alerts, and understanding system behavior at a macro level.
- **Distributed traces** follow a request as it travels through multiple services, recording the time spent at each step. They are essential for understanding latency and identifying bottlenecks in distributed systems.

Together, these three pillars provide the visibility needed to understand production behavior, diagnose issues, and make informed decisions about system improvements.

### Production Testing as a Mindset Shift

Perhaps the most significant contribution of Farley's framework is the explicit recognition that production is not just where software runs -- it is where the most valuable testing happens. This requires a mindset shift for many organizations that have historically viewed production as a place to be protected from testing rather than a place to conduct it.

This shift involves several changes in thinking:
- From "testing is something we do before release" to "testing is something we do continuously, including in production"
- From "production is fragile and must not be disturbed" to "production is a source of learning that should be observed and experimented with"
- From "bugs in production are failures" to "bugs in production are feedback that informs improvement"
- From "we know what users want" to "we need to measure what users actually do"

This mindset shift does not mean being careless in production. Farley is explicit that production testing must be done safely, with proper controls, gradual rollouts, and the ability to instantly revert changes. But it does mean recognizing that the most reliable information about software quality comes from production, and that teams that do not leverage production as a testing environment are missing their most valuable source of feedback.

### The Observability-Informed Testing Loop

One of the most powerful aspects of Farley's four-phase framework is the feedback loop it creates between production observation and pre-production testing. When production monitoring reveals a new failure mode or performance issue, that information should flow back into the earlier testing stages:

1. A production incident reveals a bug that was not caught by pre-release tests
2. A unit test is written to reproduce the bug at the Commit stage
3. An acceptance test is added to verify the fix at the system level
4. A new monitoring metric or alert is added to catch similar issues in production

This feedback loop ensures that the testing strategy continuously improves. Every production incident is an opportunity to strengthen the pre-release testing, and every pre-release improvement reduces the likelihood of future production incidents. Over time, this creates a testing strategy that becomes progressively more effective at catching issues before they reach users.

---

## Chapter 6: The Deployment Pipeline as the Organizing Structure

### How the Four Phases Connect

Farley's four-phase testing framework is designed to be implemented within a deployment pipeline -- the automated system that takes code from commit to production. Each phase of testing corresponds to a stage in the pipeline:

1. **Commit Stage**: Triggered by every code commit. Runs in seconds to minutes. Provides immediate feedback to developers. If this stage fails, the commit is rejected and the developer is notified immediately.

2. **Acceptance Stage**: Triggered after the Commit stage passes. Runs in minutes to tens of minutes. Provides confidence that the software is potentially releasable. If this stage fails, the build is not promoted to the release candidate stage.

3. **Release Stage**: Triggered when a release is initiated. Runs during the deployment process. Provides confidence that the release is proceeding correctly. If this stage fails, the release is rolled back automatically.

4. **Production Stage**: Ongoing, continuous monitoring and experimentation. Provides continuous feedback on system health, user behavior, and business performance.

The deployment pipeline creates a rigorous, repeatable, and automated path from code commit to production release. Each stage acts as a quality gate, and the testing at each stage is specifically designed to catch the types of issues that are most efficiently caught at that point in the process.

### The Test Pyramid Reinterpreted

Farley's framework aligns with and extends the classic test pyramid concept. The test pyramid (originally described by Mike Cohn) suggests that teams should have many fast unit tests at the base, fewer integration/service tests in the middle, and very few end-to-end UI tests at the top. The pyramid shape reflects both the speed and cost of different test types and the confidence they provide.

Farley's framework adds two additional layers beyond the traditional pyramid:

- **Release-time testing** (canary testing, smoke tests, health checks) -- these are fast, targeted tests that verify the release process itself.
- **Production-time testing** (monitoring, A/B testing, chaos engineering) -- these are continuous, real-world observations that inform ongoing improvement.

This extended view recognizes that testing does not stop at release. The most valuable feedback often comes from production, and the most impactful testing happens when real users interact with real software under real conditions.

### Speed vs. Scope Trade-offs

Each phase of the framework makes different trade-offs between speed and scope:

- **Commit stage**: Maximum speed, minimum scope. Tests are fast and focused but only cover individual units of code.
- **Acceptance stage**: Moderate speed, broad scope. Tests cover the full system but take longer to run.
- **Release stage**: Fast, targeted scope. Tests verify the release process and critical functionality but do not attempt comprehensive coverage.
- **Production stage**: Continuous, unlimited scope. Observation and experimentation run continuously but cannot be "run" in the traditional sense of a test suite.

These trade-offs are deliberate. The framework is designed so that cheap, fast tests catch common problems early, while more expensive, comprehensive tests are reserved for later stages where they provide the most value.

---

## Chapter 7: Advanced Concepts in Production Testing

### Chaos Engineering

Chaos Engineering, popularized by Netflix's Simian Army, is the discipline of experimenting on a distributed system in order to build confidence in its capability to withstand turbulent conditions in production. Farley references the Netflix Simian Army as a prime example of production-phase testing.

Netflix's approach includes several specialized tools:
- **Chaos Monkey**: Randomly disables production instances to verify that the system can survive individual node failures
- **Latency Monkey**: Introduces artificial delays to simulate service degradation and test whether upstream services respond appropriately
- **Conformity Monkey**: Identifies instances that do not adhere to best practices and shuts them down
- **Doctor Monkey**: Taps into health checks and external health signals to detect and remove unhealthy instances
- **Janitor Monkey**: Searches for and disposes of unused resources to prevent clutter and waste
- **Security Monkey**: Finds security violations or vulnerabilities and terminates offending instances
- **Chaos Gorilla**: Simulates an outage of an entire availability zone to verify that services automatically rebalance

The philosophy behind Chaos Engineering is captured by the flat tire analogy: the best way to ensure you can change a flat tire on the freeway in the rain at 3 AM is to practice changing tires in your driveway on Sunday afternoons. By intentionally inducing failures in a controlled manner with engineers standing by, teams learn about their system's weaknesses and can build automatic recovery mechanisms before a real crisis occurs.

Chaos Engineering is treated as a scientific discipline. It uses precise engineering processes and is best undertaken once a baseline of resilience is already established. The goal is to discover new information about system vulnerabilities by performing controlled experiments.

### Dark Launching and Feature Flagging

Dark launching (also known as feature flagging) is the practice of deploying new code to production behind a feature flag, so it is not visible to users. Once deployed, the feature can be gradually enabled for testing purposes and then progressively rolled out to users.

Dark launching enables several testing techniques:
- The new code can be tested for correctness and performance in the actual production environment without affecting users
- Internal users (dogfooding) can test the feature before external users see it
- The feature can be A/B tested against the existing behavior
- If problems are discovered, the feature can be instantly disabled by toggling the flag, without requiring a rollback

Feature flagging should be managed carefully. Without discipline, feature flags can accumulate and create technical debt. Teams should establish practices for regularly cleaning up feature flags that are no longer needed.

### Shadowing (Dark Traffic Testing)

Shadowing is the technique of capturing production traffic and replaying it against a new version of the service. This can happen in real time (bifurcating incoming traffic to both the released and deployed versions) or asynchronously (replaying previously captured traffic).

Shadowing provides high-fidelity testing because it uses real production traffic rather than synthetic test data. It is particularly effective for testing stateless services and idempotent requests. However, it requires careful handling of stateful operations and side effects, as replayed writes to a production database can cause data corruption.

### Tap Compare

Tap compare is a technique where production requests are sent to both the old and new versions of a service, and the responses are compared for correctness and performance. This is similar to shadowing but adds an explicit comparison step.

Twitter has used tap compare extensively when re-implementing existing systems. Their tool, Diffy, acts as a proxy that multicasts requests to both old and new instances, compares the responses, and reports any regressions. The premise is that if two implementations return similar responses for a sufficiently large and diverse set of requests, the new implementation can be treated as regression-free.

GitHub's Scientist library provides similar functionality for comparing the results of two code paths at the application level.

### Load Testing with Production Traffic

Farley's emphasis on production testing also extends to load testing. Traditional load testing is performed in staging or test environments with synthetic traffic, but these tests often fail to replicate the conditions that cause real production issues. The traffic patterns, data distributions, and concurrent access patterns in production are difficult to simulate artificially.

Several organizations have developed techniques for load testing with real production traffic:

- **Traffic shifting**: Routing a larger-than-normal percentage of production traffic to a specific cluster or instance and monitoring its behavior. LinkedIn's "Redliner" tool does this automatically, gradually increasing load until performance degrades, establishing the system's actual capacity limits.
- **Shadow loading**: Sending a copy of production traffic to a dedicated test instance and measuring its performance under real load. Facebook's McRouter supports this for memcached traffic, allowing teams to test new cache hardware with a complete copy of production traffic.
- **Stress testing through scale reduction**: Intentionally reducing the number of serving instances while maintaining the same traffic level, effectively increasing the per-instance load. This reveals how the system behaves under stress without requiring additional traffic generation.

These techniques provide far more accurate capacity measurements than synthetic load tests because they use real traffic patterns, real data, and real network conditions. They also reveal emergent behaviors that only appear at production scale -- behaviors that cannot be predicted through analysis or testing at smaller scales.

### Integration Testing in Production

One of the more provocative aspects of Farley's framework (and the associated work by Cindy Sridharan that he references) is the idea of integration testing in production. Traditional wisdom says that integration testing should be done in a test or staging environment, but the argument for doing it in production is compelling:

Production integration testing becomes possible when deployment is separated from release. A new version of a service can be deployed to the production environment without receiving any user traffic. Integration tests can then be run against this deployed version, exercising its interactions with real production dependencies (databases, caches, other services) under real conditions.

This approach has several advantages over staging-environment integration testing:
- The test runs in the actual production environment, with real configuration, real data volumes, and real network conditions
- The test exercises interactions with real production services that are serving real traffic, not isolated test instances
- There is no need to maintain a separate staging environment that attempts (and inevitably fails) to replicate production

The key challenge is handling stateful operations (writes) during production integration testing. Several strategies exist: using test-specific accounts or users, marking test data at the application layer, or routing test writes to separate tables or collections. Service mesh architectures can help by allowing proxies to intercept and modify test requests.

---

## Chapter 8: Practical Implementation Considerations

### Building a Testing Strategy Step by Step

Farley's framework provides a structure, but implementing it requires careful planning. Here is a practical approach:

1. **Start with the Commit stage**: Ensure every developer writes unit tests, uses static analysis, and can run the full commit-stage suite locally in under two minutes. This is the foundation.

2. **Add Acceptance tests incrementally**: Begin with the most critical user journeys and expand coverage over time. Use BDD-style executable specifications to engage stakeholders and create shared understanding.

3. **Automate deployment and add Release tests**: Automate the deployment process and add smoke tests and health checks. Implement canary releases with automated rollback based on key metrics.

4. **Invest in Production observability**: Set up comprehensive monitoring, exception tracking, and alerting. Begin with the basics (error rate, latency, throughput) and expand over time.

5. **Gradually introduce advanced techniques**: Once the basics are solid, add A/B testing, chaos engineering, shadowing, and other advanced production testing techniques.

### Common Anti-Patterns

Several anti-patterns can undermine a testing strategy:

- **Testing as a separate phase**: When testing is done by a separate QA team after development is "complete," feedback is slow and expensive. Testing should be integrated into the development process.

- **Over-reliance on end-to-end tests**: End-to-end tests are slow, brittle, and hard to maintain. They should be used sparingly to verify critical user journeys, not as the primary form of testing.

- **Testing only before release**: The most valuable learning happens in production. Teams that stop testing at release miss critical feedback.

- **Monitoring everything**: Monitoring too many signals creates noise. Focus on a small number of high-signal metrics that reliably indicate system health.

- **Skipping data migration testing**: Data migration failures are among the most common and impactful production incidents. Always test migrations with realistic data.

- **Ignoring configuration testing**: Configuration errors cause a disproportionate number of outages. Treat configuration as code and test it with the same rigor.

### The Role of Automation

Automation is essential to making Farley's framework work in practice. Every stage of the testing strategy should be automated:

- **Automated builds and tests on every commit** (CI)
- **Automated acceptance test execution** in the pipeline
- **Automated deployment with canary analysis and rollback** (CD)
- **Automated monitoring, alerting, and incident response**

Manual testing still has a role -- particularly exploratory testing, where human creativity and intuition can discover issues that automated tests miss. But manual testing should complement the automated pipeline, not replace it.

### Metrics for Evaluating Your Testing Strategy

How do you know if your testing strategy is working? Key metrics include:

- **Deployment frequency**: How often can you deploy to production? High-performing teams deploy multiple times per day.
- **Lead time for changes**: How long does it take from code commit to production release? The Commit and Acceptance stages are the primary determinants.
- **Change failure rate**: What percentage of deployments cause failures in production? This measures the effectiveness of pre-release testing.
- **Mean time to recovery**: How quickly can you recover from a failure? This measures the effectiveness of release-stage and production-stage testing.
- **Test suite execution time**: How long does each stage take? Faster feedback loops enable faster delivery.
- **Defect escape rate**: How many defects are found in production that were not caught by earlier stages? This helps identify gaps in the testing strategy.

### The Cost of Quality vs. The Cost of Failure

A practical consideration when implementing Farley's framework is balancing the cost of testing against the cost of failures. Not every system requires the same level of testing investment. The appropriate level of testing depends on the cost of failure:

- **Safety-critical systems** (medical devices, aviation software, autonomous vehicles): The cost of failure is extremely high (loss of life). These systems require the most rigorous testing at every stage, including formal verification methods that go beyond what Farley describes.
- **Financial systems** (trading platforms, payment processors): The cost of failure is high (financial loss, regulatory penalties). These systems require strong testing at every stage, with particular emphasis on data integrity and compliance.
- **Consumer-facing web applications**: The cost of failure is moderate (user dissatisfaction, lost revenue). These systems benefit from Farley's full framework, with particular emphasis on production testing and rapid recovery.
- **Internal tools and prototypes**: The cost of failure is low (inconvenience, wasted time). These systems may need only a subset of the framework, focused on Commit-stage testing and basic production monitoring.

The key insight is that the framework is a menu, not a mandate. Teams should adopt the practices that are appropriate for their specific risk profile, and they should revisit those choices as the system evolves and the risk profile changes.

### Team Structure and Testing Ownership

Farley's framework has implications for team structure. In organizations where testing is owned by a separate QA team, the natural tendency is to concentrate testing in the Acceptance stage (where QA teams typically operate) and neglect the Commit and Production stages. This creates gaps in the feedback loop and slows down the delivery process.

Farley's approach works best when testing is embedded in the development team:
- Developers write and maintain their own unit tests (Commit stage)
- The team collectively defines and automates acceptance tests (Acceptance stage)
- The team owns their deployment pipeline, including release automation (Release stage)
- The team is responsible for monitoring and observing their software in production (Production stage)

This does not mean that there is no role for testing specialists. Test engineers can provide expertise in test automation, performance testing, security testing, and other specialized areas. But their role should be to enable and support the development team, not to act as a separate quality gate.

---

## Chapter 9: The Bigger Picture -- Continuous Delivery and Organizational Learning

### Testing as an Engineering Culture

Farley's framework is not just a technical guide; it is a statement about engineering culture. The best teams have a "laser focus on testing" that extends beyond pre-release testing to encompass the entire software lifecycle. This focus reflects a culture of continuous learning, evidence-based decision making, and relentless improvement.

In this culture:
- Developers are responsible for testing their own code (not delegating to a QA team)
- Testing is automated and integrated into the development workflow
- Quality is everyone's responsibility, not a separate function
- Production is viewed as a source of learning, not just a deployment target
- Failures are learning opportunities, not blame opportunities

### The Relationship Between Testing Speed and Delivery Speed

There is a direct relationship between testing speed and delivery speed. Faster tests enable faster feedback, which enables faster fixes, which enables faster delivery. This is why Farley emphasizes speed at every stage:

- **Commit stage**: Seconds to minutes
- **Acceptance stage**: Minutes to tens of minutes
- **Release stage**: Minutes (during deployment)
- **Production stage**: Continuous (real-time)

Organizations that invest in fast, reliable tests at every stage can deploy more frequently, with more confidence, and recover more quickly from failures. This creates a virtuous cycle: faster delivery enables faster learning, which enables better decisions, which leads to better software.

### Evidence-Based Decision Making

Throughout the framework, Farley emphasizes evidence-based decision making. At every stage, the testing strategy is designed to produce evidence that supports better decisions:

- **Commit stage evidence**: Does this code change work as intended?
- **Acceptance stage evidence**: Is this software releasable?
- **Release stage evidence**: Is this release proceeding safely?
- **Production stage evidence**: Is this software meeting user needs and business goals?

This evidence-based approach stands in contrast to decision making based on assumptions, opinions, or hierarchy. Farley's framework gives teams the tools to make decisions based on data, not guesswork.

The Microsoft research Farley cites -- that two-thirds of ideas produce zero or negative value -- is a powerful argument for this approach. Without evidence from production (A/B testing, user behavior analysis, commercial performance monitoring), teams cannot know which of their ideas are actually valuable.

### Continuous Improvement Through the Testing Feedback Loop

The ultimate goal of Farley's framework is not just to catch bugs but to enable continuous improvement. Each phase of the framework feeds information back into the others, creating a self-reinforcing cycle:

1. Production monitoring reveals how users actually behave and what performance looks like in the real world. This information informs what should be tested in the Acceptance stage.
2. Acceptance testing reveals gaps in the unit test coverage. When acceptance tests catch bugs that unit tests missed, new unit tests should be written to catch those bugs earlier.
3. Commit-stage testing catches errors that would otherwise be found in acceptance testing or production, reducing the cost and time of fixing those errors.
4. Release-stage testing (particularly canary analysis) catches issues that slip through pre-release testing, and these issues should flow back into improvements in both the Acceptance and Commit stages.

This feedback loop means that the testing strategy is never "done." It is a living, evolving system that improves over time as the team learns more about their software, their users, and their failure modes. The best teams are those that treat their testing strategy as a product that needs continuous investment, refinement, and improvement -- not as a one-time implementation that can be checked off and forgotten.

### The Connection to Modern Software Engineering Principles

Farley's testing framework is deeply connected to the broader principles he articulates in "Modern Software Engineering." In that work, he identifies several core engineering practices that distinguish high-performing teams: working in small batches, creating fast feedback loops, automating relentlessly, and making decisions based on evidence rather than opinion. The testing framework is a concrete manifestation of all of these principles:

- **Working in small batches** is enabled by fast Commit-stage tests that allow developers to commit and deploy small changes with confidence.
- **Creating fast feedback loops** is the explicit goal of every stage in the framework, from the sub-second unit test to the real-time production dashboard.
- **Automating relentlessly** is essential because manual testing cannot keep pace with the speed of modern software delivery.
- **Making evidence-based decisions** is what the Production stage is all about: using real data from real users to inform product and technical decisions.

The testing framework is not an isolated technique. It is an integral part of a coherent approach to software engineering that, when practiced consistently, enables teams to deliver better software faster. The "better software faster" goal is not a trade-off between quality and speed. Rather, it is the recognition that quality and speed are mutually reinforcing: better testing practices enable faster delivery, and faster delivery enables faster learning and improvement.

---

## Key Takeaways

1. **Testing is a continuous feedback mechanism, not a phase.** Farley's four-phase framework (Commit, Acceptance, Release, Production) recognizes that testing happens throughout the entire software delivery lifecycle, with each phase serving a distinct purpose.

2. **The Commit stage must FAIL FAST.** Unit tests, static analysis, coding standards checks, and common error detection should give developers immediate confidence in their changes. Speed is paramount -- the entire Commit stage should complete in under five minutes.

3. **The Acceptance stage defines RELEASABLE.** Acceptance tests (preferably BDD-style executable specifications), deployment tests, configuration tests, security tests, performance tests, scalability tests, resilience tests, and compliance tests collectively determine whether software is fit for release.

4. **The Release stage SUPPORTS RELEASE.** Smoke tests, health checks, canary release testing, monitoring, and exception tracking verify that the release process is working and catch any regressions before they affect all users.

5. **The Production stage informs PRODUCT DESIGN.** Capacity monitoring, technical monitoring, performance verification, security verification, A/B testing, business experiments, and commercial performance monitoring provide continuous feedback from the real world.

6. **Unit tests are the foundation, but not the ceiling.** While unit tests provide fast, focused feedback at the Commit stage, they are insufficient on their own. A complete testing strategy requires acceptance tests, release verification, and production observation.

7. **Test data migrations rigorously.** Data migration failures are a leading cause of production incidents. Test migrations at both the unit level (Commit stage) and the integration level (Acceptance stage) with realistic data.

8. **Automate everything.** Every stage of the testing strategy should be automated and integrated into the deployment pipeline. Manual testing should complement, not replace, automated testing.

9. **Focus monitoring on a few high-signal metrics.** Monitoring too many signals creates noise. Facebook's Kraken system monitors just two metrics for canary analysis: p99 response time and HTTP fatal error rate.

10. **Two-thirds of ideas produce zero or negative value.** This finding from Microsoft research underscores the importance of production-phase testing (especially A/B testing) for evidence-based product decisions. Without production data, teams are guessing.

11. **Treat configuration as code.** Configuration errors cause a disproportionate number of outages. Configuration should be version-controlled, tested, and deployed through the same pipeline as application code.

12. **Production is the ultimate test environment.** No staging environment can fully replicate production. Techniques like shadowing, tap compare, canary releases, and chaos engineering enable testing against real conditions with real traffic while minimizing risk to users.

13. **Chaos Engineering builds confidence in resilience.** By intentionally inducing failures in a controlled manner, teams learn about their system's weaknesses and can build automatic recovery mechanisms before real failures occur.

14. **Speed of feedback determines speed of delivery.** The faster tests run, the faster developers get feedback, the faster they can fix problems, and the faster the team can deliver. Invest in fast tests at every stage.

15. **Quality is a culture, not a department.** The most effective testing strategies emerge from cultures where every engineer takes responsibility for quality, where testing is integrated into the development workflow, and where failures are treated as learning opportunities.
