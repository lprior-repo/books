# Learning Domain-Driven Design
**Author:** Vlad Khononov
**Topic tags:** `#architecture` `#general`
**Language focus:** Language-agnostic; C# / .NET examples
**Sources:** `markdown_output/Learning Domain-Driven Design/Learning Domain-Driven Design.md` · `summaries/Learning_Domain-Driven_Design_Vlad_Khononov.md` · `summaries/Learning_Domain-driven_design.md`

## TL;DR
Use domain-driven design to align software decisions with business strategy. Discover subdomains and their strategic value before selecting bounded contexts, integration relationships, business-logic patterns, architecture, or tests. Keep the ubiquitous language alive everywhere, protect model and consistency boundaries explicitly, and evolve every decision as the business, organization, and knowledge change.
---
## Best Practices by Topic

#### 1. Let the Business Domain Drive the Design
**Principle:** Agree on the business problem and solution model before choosing implementation details.
**Do:**
- Identify the business domain, customers, value proposition, competitors, and business goals first.
- Use strategic design to answer what to build and why; use tactical design to answer how to implement it.
- Evaluate every technical choice against the business strategy and the complexity it must support.
- Prefer the simplest design that addresses the actual domain.
**Don't:**
- Don't begin with frameworks, databases, service counts, or fashionable architecture.
- Don't translate requirements mechanically without learning the reasoning behind them.
- Don't call the use of aggregates or value objects “DDD” when business strategy did not drive the choice.
*Ref: Learning Domain-Driven Design.md — "Introduction", "Strategic Design", "Closing Words"*
---
#### 2. Define the Business Domain
**Principle:** Treat the business domain as the organization’s main area of activity and the value it provides to customers.
**Do:**
- State the organization’s service in business terms.
- Allow for organizations operating in multiple business domains.
- Revisit the definition when the company changes direction.
- Scope software analysis to the business activities relevant to the system.
**Don't:**
- Don't equate the business domain with a software system, department, or technology.
- Don't assume the domain is permanent; companies can change domains radically.
*Ref: Learning Domain-Driven Design.md — "What Is a Business Domain?", "Understand the Business Domain"*
---
### 3. Decompose the Domain into Subdomains
**Principle:** Model the business domain as interacting fine-grained areas of business activity.
**Do:**
- Treat all subdomains together as the capabilities needed to compete in the business domain.
- Find sets of coherent use cases involving the same actors, business entities, and closely related data.
- Start from departments only as a coarse heuristic, then distill finer capabilities.
- Separate software-relevant subdomains from nonsoftware competitive capabilities.
**Don't:**
- Don't expect one subdomain to deliver the entire business outcome independently.
- Don't stop at an organizational chart when it conceals strategically different capabilities.
- Don't decompose indefinitely when finer boundaries reveal no new design information.
*Ref: Learning Domain-Driven Design.md — "What Is a Subdomain?", "Identifying Subdomain Boundaries", "Subdomains as coherent use cases", "Focus on the essentials"*
---
### 4. Invest in Core Subdomains
**Principle:** Treat a core subdomain as the difficult, volatile capability through which the company differentiates itself.
**Do:**
- Implement core subdomains in-house and close to domain experts.
- Assign the strongest engineers and advanced design techniques where justified.
- Expect experimentation, frequent change, and continuous optimization.
- Distill core boundaries aggressively so supporting and generic concerns do not dilute investment.
- Ask whether the capability could be a sellable business on its own when classification is unclear.
**Don't:**
- Don't outsource the source of competitive advantage.
- Don't expect a simple, easily copied implementation to remain a durable core capability.
- Don't assume every core advantage is technical; expertise, relationships, or design can be core.
- Don't apply a simple transaction script to complex core business rules.
*Ref: Learning Domain-Driven Design.md — "Core subdomains", "Complexity", "Sources of competitive advantage", "Solution strategy"*
---
### 5. Buy or Adopt Generic Subdomains
**Principle:** Reuse established solutions for complex problems that every company solves in essentially the same way.
**Do:**
- Buy an off-the-shelf product, subscribe to a service, or adopt open source when practical.
- Treat authentication, encryption, accounting, and similar capabilities as candidates, not automatic custom builds.
- Compare the cost of integration with the cost of a minimal in-house supporting solution.
- Obtain specialist help when customization of a known problem is unavoidable.
**Don't:**
- Don't confuse “generic” with “simple”; generic solutions can be highly complex.
- Don't invest in proprietary reinvention when competitors can use the same mature solution.
- Don't let a generic capability consume the talent needed by core subdomains.
*Ref: Learning Domain-Driven Design.md — "Generic subdomains", "Complexity", "Solution strategy"*
---
### 6. Keep Supporting Subdomains Simple
**Principle:** Implement necessary but nondifferentiating, obvious business logic with low-ceremony techniques.
**Do:**
- Use rapid application development, transaction scripts, active records, CRUD, or ETL-style processing.
- Consider outsourcing and use the work to develop less experienced engineers.
- Keep implementation economical because change frequency and business leverage are low.
- Reclassify the capability if its rules become complex or begin affecting profitability.
**Don't:**
- Don't use sophisticated domain models merely for consistency with a systemwide standard.
- Don't mistake “must exist” for “provides competitive advantage.”
- Don't retain a custom supporting implementation after an economical generic solution appears.
*Ref: Learning Domain-Driven Design.md — "Supporting subdomains", "Solution strategy", "Supporting to Generic", "Supporting to Core"*
---
#### 7. Compare Subdomains Explicitly
**Principle:** Allocate money, talent, and design effort according to competitive advantage, complexity, volatility, and solution strategy.

| Subdomain type | Competitive advantage | Complexity | Volatility | Implementation | Problem |
|---|---:|---:|---:|---|---|
| Core | Yes | High | High | In-house | Interesting |
| Generic | No | High | Low | Buy/adopt | Solved |
| Supporting | No | Low | Low | In-house/outsource | Obvious |
**Do:**
- Use classification to expose underengineering and overengineering.
- Reconcile business classification with the business-logic pattern the code actually needs.
- Question a “core” capability that can be hacked in a day.
- Question a “supporting” capability that requires complex invariants and advanced modeling.
**Don't:**
- Don't infer strategic importance from technical complexity alone.
- Don't freeze classification; subdomain type is time-dependent.
*Ref: Learning Domain-Driven Design.md — "Comparing Subdomains", "Mapping design decisions to subdomains"*
---
#### 8. Distill Boundaries with Coherent Use Cases
**Principle:** Stop decomposing when each candidate groups coherent use cases over the same actors, entities, and closely related data.
**Do:**
- Drill into apparently generic departments to uncover hidden core and supporting capabilities.
- Distill core subdomains more precisely than generic or supporting ones.
- Keep coarse generic boundaries when deeper analysis changes no design decision.
- Revisit boundaries as functionality grows and previously hidden capabilities emerge.
**Don't:**
- Don't make department names the final domain model.
- Don't split coherent use cases whose requirements and data change together.
- Don't include nonsoftware business activities merely to make the system model exhaustive.
*Ref: Learning Domain-Driven Design.md — "Distilling subdomains", "Subdomains as coherent use cases", "Subdomains"*
---
#### 9. Work Directly with Domain Experts
**Principle:** Obtain domain knowledge from the businesspeople who originate requirements or use the system.
**Do:**
- Identify experts by their knowledge of business processes, rules, edge cases, and goals.
- Include experts with broad domain knowledge and specialists for individual subdomains.
- Use engineers and analysts to transform knowledge, not to impersonate its source.
- Ask questions that reveal implicit assumptions and undefined edge cases.
**Don't:**
- Don't label technical specialists or project-resource managers as domain experts by default.
- Don't route all knowledge through layers of translators.
- Don't expect engineers to become full domain experts; learn enough to model the required problem.
*Ref: Learning Domain-Driven Design.md — "Who Are the Domain Experts?", "Knowledge Discovery"*
---
#### 10. Treat Development as Knowledge Discovery
**Principle:** Regard working code as a side effect of learning how the business problem actually works.
**Do:**
- Learn the rationale behind requirements, not just their written form.
- Test the model against omitted edge cases and future requirements.
- Let questions expose ambiguities in experts’ own mental models.
- Co-create missing definitions with experts rather than silently guessing.
**Don't:**
- Don't rely on a chain from domain knowledge to analysis model to requirements to design to code.
- Don't assume documents preserve tacit knowledge.
- Don't optimize delivery before the team shares an understanding of the problem.
*Ref: Learning Domain-Driven Design.md — "Business Problems", "Knowledge Discovery", "Communication", "Challenges"*
---
### 11. Build a Ubiquitous Language
**Principle:** Use one rigorous business language among all stakeholders within each bounded context.
**Do:**
- Use the language in conversations, requirements, diagrams, documentation, tests, and source code.
- Make domain experts comfortable reasoning with every term.
- Name code after business concepts rather than technical implementation.
- Evolve the language whenever deeper domain knowledge appears.
- Treat everyday use, not documentation, as the mechanism that makes the language ubiquitous.
**Don't:**
- Don't translate repeatedly between business and engineering vocabularies.
- Don't include technical jargon such as table names, iframes, or design patterns in the domain language.
- Don't invent code terms that experts never use.
- Don't define the language once and declare it finished.
*Ref: Learning Domain-Driven Design.md — "What Is a Ubiquitous Language?", "Language of the Business", "Continuous Effort"*
---
#### 12. Express Business Scenarios, Not Technical Mechanisms
**Principle:** Describe behavior through business entities, decisions, and outcomes.
**Do:**
- Say “A campaign can be published only if at least one placement is active.”
- Say “Sales commissions are accounted for after transactions are approved.”
- Use scenarios to expose cause, effect, actors, rules, and invariants.
**Don't:**
- Don't replace business meaning with records, tables, iframes, or joins.
- Don't let a technically accurate statement conceal why the rule exists.
- Don't force experts to reverse-engineer the domain from solution details.
*Ref: Learning Domain-Driven Design.md — "Language of the Business", "Scenarios"*
---
#### 13. Eliminate Ambiguity and Synonymy
**Principle:** Give each term one meaning per bounded context and each concept one preferred term.
**Do:**
- Split ambiguous “policy” into explicit concepts such as `RegulatoryRule` and `InsuranceContract`.
- Distinguish visitor, account, user, and administrator when their behavior differs.
- Ask why multiple names exist before consolidating them; they may reveal hidden models.
- Make context explicit when the same term legitimately has different meanings.
**Don't:**
- Don't depend on conversational context to rescue ambiguous code.
- Don't accept synonyms merely because humans can infer the intended meaning.
- Don't add awkward prefixes to one codebase when the real issue is conflicting bounded contexts.
*Ref: Learning Domain-Driven Design.md — "Consistency", "Ambiguous terms", "Synonymous terms", "Inconsistent Models"*
---
#### 14. Build Purpose-Specific Models
**Principle:** Keep only the information required to solve the model’s specific problem.
**Do:**
- State the model’s purpose and applicability boundary.
- Omit irrelevant reality deliberately.
- Prefer multiple focused models over one enterprise-wide jack-of-all-trades model.
- Judge a model by utility and precision within its context, not resemblance to reality.
**Don't:**
- Don't make a model a copy of the real world.
- Don't remove information necessary for the problem.
- Don't retain noise that raises cognitive load without supporting decisions.
- Don't force sales, marketing, operations, and analytics to share one representation.
*Ref: Learning Domain-Driven Design.md — "What Is a Model?", "Effective Modeling", "Modeling the Business Domain", "Buying a Refrigerator"*
---
### 15. Capture Language with Complementary Tools
**Principle:** Use glossaries for terms and executable scenarios for behavior, but never substitute tools for interaction.
**Do:**
- Maintain the glossary collaboratively rather than through one architect.
- Pair noun-oriented glossaries with use cases or Gherkin scenarios.
- Let experts read scenarios and validate expected business behavior.
- Use static analysis only to reinforce language already used by the team.
**Don't:**
- Don't expect a glossary to capture rules, assumptions, and invariants by itself.
- Don't expect domain experts to author the test suite.
- Don't let documentation replace conversations.

**Code:**
```gherkin
Scenario: Notify the agent about a new support case
 Given Vincent Jules submits a new support case saying:
 """
 I need help configuring AWS Infinidash
 """
 When the ticket is assigned to Mr. Wolf
 Then the agent receives a notification about the new ticket
```
*Ref: Learning Domain-Driven Design.md — "Tools", "Challenges"*
---
### 16. Bound Every Model Explicitly
**Principle:** Define a bounded context as the consistency boundary within which one model and one ubiquitous language apply.
**Do:**
- Split the language when experts hold conflicting models of the same term.
- Allow the same term to mean different things in different bounded contexts.
- Make applicability context part of every model definition.
- Treat the bounded context as a model, lifecycle, and ownership boundary.
**Don't:**
- Don't build an enterprise-wide model intended to work for every problem.
- Don't call the language universal across the organization.
- Don't mix conflicting models and expect prefixes alone to control cognitive load.
*Ref: Learning Domain-Driven Design.md — "What Is a Bounded Context?", "Model Boundaries", "Ubiquitous Language Refined"*
---
### 17. Size Bounded Contexts for Usefulness
**Principle:** Make context size a function of model coherence, domain knowledge, team constraints, and lifecycle needs—not a target in itself.
**Do:**
- Start wider when core-domain knowledge is uncertain or requirements are volatile.
- Decompose logical boundaries later as knowledge stabilizes.
- Extract contexts for independent teams, lifecycles, scaling, or focused models.
- Keep tightly related use cases and data together.
- Balance model consistency against integration overhead.
**Don't:**
- Don't optimize blindly for small contexts or microservices.
- Don't split functionality that always changes and deploys together.
- Don't treat one context per subdomain as a universal law.
- Don't make wide contexts permanent when they lose focus.
*Ref: Learning Domain-Driven Design.md — "Scope of a Bounded Context", "Bounded Contexts", "Domain Knowledge"*
---
### 18. Distinguish Subdomains from Bounded Contexts
**Principle:** Discover subdomains in the problem space; design bounded contexts in the solution space.
**Do:**
- Let business strategy define subdomains.
- Choose bounded-context boundaries according to project constraints and model consistency.
- Use one context per subdomain when useful, but allow one context to span subdomains or multiple models to address one subdomain.
- Revisit both kinds of boundary independently.
**Don't:**
- Don't use “subdomain” and “bounded context” interchangeably.
- Don't assume a one-to-one mapping from day one.
- Don't treat a solution boundary as an immutable fact of the business.
*Ref: Learning Domain-Driven Design.md — "Bounded Contexts Versus Subdomains", "The Interplay Between Subdomains and Bounded Contexts"*
---
### 19. Align Physical and Ownership Boundaries
**Principle:** Give each bounded context one independent lifecycle and one owning team.
**Do:**
- Implement a context as an independently evolved and versioned service, project, or module.
- Use modules, namespaces, or packages as logical subdomain boundaries inside a wider context.
- Allow one team to own multiple contexts.
- Define integration protocols explicitly between team-owned contexts.
**Don't:**
- Don't let two teams co-own one bounded context.
- Don't require all contexts to use one technology stack.
- Don't confuse logical layers with independently deployable physical tiers.
*Ref: Learning Domain-Driven Design.md — "Physical Boundaries", "Ownership Boundaries", "Optional: Layers Versus Tiers"*
---
### 20. Use Partnership for Genuine Cooperation
**Principle:** Integrate ad hoc only when teams have reciprocal goals, excellent communication, and frequent synchronization.
**Do:**
- Coordinate contracts in both directions.
- Solve integration issues jointly.
- Use continuous integration to shorten feedback loops.
- Reassess the relationship when geography or organizational growth weakens communication.
**Don't:**
- Don't impose one team’s model when the relationship is a partnership.
- Don't retain partnership semantics after collaboration becomes unreliable.
- Don't use this loosely coordinated pattern for distant teams that cannot synchronize.
*Ref: Learning Domain-Driven Design.md — "Cooperation", "Partnership", "Partnership to Customer–Supplier"*
---
### 21. Limit a Shared Kernel Aggressively
**Principle:** Share only the model whose duplication costs more than coordinating every change.
**Do:**
- Restrict the kernel to genuinely overlapping contracts and data structures.
- Make changes immediately visible to every participating context.
- Trigger all affected integration tests on every kernel change.
- Use it pragmatically for one team’s multiple contexts or temporary legacy decomposition.
**Don't:**
- Don't share broad domain models casually.
- Don't allow contexts to depend on stale versions.
- Don't ignore that shared ownership violates the normal one-team-per-context rule.
- Don't choose it when a volatile shared model makes coordination more expensive than duplication.
*Ref: Learning Domain-Driven Design.md — "Shared Kernel", "Shared scope", "Implementation", "When to use shared kernel"*
---
### 22. Conform Only When the Upstream Model Fits
**Principle:** Let a downstream context adopt the upstream model only when loss of autonomy is acceptable.
**Do:**
- Conform to a stable industry standard or a supplier model that is good enough.
- Make the power imbalance explicit on the context map.
- Reconsider conformity when upstream churn or model awkwardness harms the downstream.
**Don't:**
- Don't conform a core subdomain to a model that impedes its problem-solving model.
- Don't absorb a legacy mess merely because the supplier has more power.
- Don't mistake lack of leverage for lack of downstream design consequences.
*Ref: Learning Domain-Driven Design.md — "Customer–Supplier", "Conformist"*
---
### 23. Protect Core Models with an Anticorruption Layer
**Principle:** Translate an upstream contract into the downstream context’s own model when conformity would corrupt it.
**Do:**
- Use an ACL when the downstream is core, the upstream is inconvenient, or the supplier changes often.
- Isolate foreign concepts that are irrelevant to the downstream language.
- Keep upstream change impact inside the translation mechanism.
- Implement stateless or stateful translation according to the transformation.
**Don't:**
- Don't let external or legacy vocabulary spread through a core model.
- Don't share one ACL among consumers unless it is deliberately owned as an interchange context.
- Don't treat translation as a field-for-field mapping when models differ semantically.
*Ref: Learning Domain-Driven Design.md — "Anticorruption Layer", "Model Translation", "Stateless Model Translation", "Stateful Model Translation"*
---
### 24. Publish an Integration-Oriented Language
**Principle:** Use an open-host service to decouple the supplier’s implementation model from contracts designed for consumers.
**Do:**
- Translate the internal model into a stable, convenient published language.
- Evolve implementation and integration models at different rates.
- Serve multiple public versions during consumer migration when needed.
- Include public events in the published language instead of leaking internal domain events.
**Don't:**
- Don't require the public interface to mirror the supplier’s ubiquitous language.
- Don't make each consumer maintain a unique one-off integration.
- Don't expose internal schema changes through the service front door.
*Ref: Learning Domain-Driven Design.md — "Open-Host Service", "Asynchronous", "Use public and private events"*
---
### 25. Choose Separate Ways Deliberately
**Principle:** Duplicate functionality when integration and collaboration cost more than independent implementations.
**Do:**
- Consider separate ways for communication failures, easy-to-integrate generic tools, or irreconcilable model differences.
- Compare duplication cost with integration cost explicitly.
- Use local generic libraries when exposing them as a service adds needless complexity.
**Don't:**
- Don't duplicate a core subdomain; it fragments competitive investment and future evolution.
- Don't integrate merely to satisfy a reuse ideal.
- Don't hide organizational dysfunction; show separate-ways concentrations on the context map.
*Ref: Learning Domain-Driven Design.md — "Separate Ways", "Communication Issues", "Generic Subdomains", "Model Differences"*
---
### 26. Maintain a Context Map
**Principle:** Visualize contexts, dependency directions, team relationships, contracts, and translation points as a living strategic artifact.
**Do:**
- Show partnership, shared kernel, conformist, ACL, OHS, and separate ways explicitly.
- Use the map to reveal high-level design and organizational trouble.
- Make each team responsible for keeping its integrations current.
- Allow multiple patterns between contexts when different modules need different relationships.
**Don't:**
- Don't treat the map as a one-time architecture diagram.
- Don't force one relationship label onto all interactions between two wide contexts.
- Don't omit ownership and power dynamics.
*Ref: Learning Domain-Driven Design.md — "Context Map", "Maintenance", "Limitations"*
---
### 27. Use Transaction Script for Simple Procedural Logic
**Principle:** Implement each public business operation as a straightforward procedure that succeeds or fails atomically.
**Do:**
- Use it for simple supporting logic, ETL, generic-solution adapters, and ACL translation.
- Keep abstractions minimal when business logic and data are simple.
- Treat transactional behavior as mandatory, not optional.
- Recognize application-service orchestration as a transaction script even around richer models.
**Don't:**
- Don't use transaction script for core rules, complicated state transitions, or invariants.
- Don't duplicate growing business logic across procedures.
- Don't dismiss it as an antipattern when its context is genuinely simple.

**Code:**
```csharp
DB.StartTransaction();
var job = DB.LoadNextJob();
var json = LoadFile(job.Source);
var xml = ConvertJsonToXml(json);
WriteFile(job.Destination, xml.ToString();
DB.MarkJobAsCompleted(job);
DB.Commit()
```
*Ref: Learning Domain-Driven Design.md — "Transaction Script", "Implementation", "When to Use Transaction Script"*
---
### 28. Enforce Real Transactional Behavior
**Principle:** Leave no partial state when any step fails.
**Do:**
- Enclose related writes in one database transaction when the storage mechanism supports it.
- Roll back all changes on failure.
- Analyze failures at every line between the first effect and final commit.
- Include caller-visible success or failure in the distributed transaction analysis.
**Don't:**
- Don't issue multiple dependent writes without an overarching transaction.
- Don't assume one database method call makes the whole operation safe.

**Code:**
```csharp
01 public class LogVisit
02 {
03 ...
04
05 public void Execute(Guid userId, DataTime visitedOn)
06 {
07 _db.Execute("UPDATE Users SET last_visit=@p1 WHERE user_id=@p2",
08 visitedOn, userId);
09 _db.Execute(@"INSERT INTO VisitsLog(user_id, visit_date)
10 VALUES(@p1, @p2)", userId, visitedOn);
11 }
12 }
```

```csharp
public class LogVisit
{
 ...
 public void Execute(Guid userId, DataTime visitedOn)
 {
 try
 {
 _db.StartTransaction();
 _db.Execute(@"UPDATE Users SET last_visit=@p1
 WHERE user_id=@p2",
 visitedOn, userId);
 _db.Execute(@"INSERT INTO VisitsLog(user_id, visit_date)
 VALUES(@p1, @p2)",
 userId, visitedOn);
 _db.Commit();
 } catch {
 _db.Rollback();
 throw;
 }
 }
}
```
*Ref: Learning Domain-Driven Design.md — "It's Not That Easy!", "Lack of transactional behavior"*
---
### 29. Detect Explicit and Implicit Distributed Transactions
**Principle:** Treat every independently failing effect—including reporting the result to the caller—as a transaction participant.
**Do:**
- Use outbox rather than a database write followed by direct message publication.
- Analyze retries after response loss even when the server completed its write.
- Design for network outage, process failure, database timeout, and message-bus failure.
**Don't:**
- Don't assume a `void` operation communicates nothing; success and exceptions are outputs.
- Don't retry nonidempotent effects blindly.
- Don't depend on fragile distributed transactions across storage systems.

**Code:**
```csharp
01 public class LogVisit
02 {
03 ...
04
05 public void Execute(Guid userId, DataTime visitedOn)
06 {
07 _db.Execute("UPDATE Users SET last_visit=@p1 WHERE user_id=@p2",
08 visitedOn,userId);
09 _messageBus.Publish("VISITS_TOPIC",
10 new { UserId = userId, VisitDate = visitedOn });
11 }
12 }
```

```csharp
public class LogVisit
{
 ...
 public void Execute(Guid userId)
 {
 _db.Execute("UPDATE Users SET visits=visits+1 WHERE user_id=@p1",
 userId);
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Distributed transactions", "Implicit distributed transactions"*
---
### 30. Make Retries Idempotent or Concurrency-Aware
**Principle:** Ensure repeated execution cannot silently apply the same intent twice.
**Do:**
- Prefer assigning an intended final value when that matches the domain.
- Use optimistic concurrency when an update depends on previously read state.
- Reject stale decisions rather than overwriting concurrent work.
- Make the caller supply enough information to identify the intended transition.
**Don't:**
- Don't convert every increment into an assignment without checking lost-update semantics.
- Don't ignore a failed conditional update; surface the concurrency result.

**Code:**
```csharp
public class LogVisit
{
 ...
 public void Execute(Guid userId, long visits)
 {
 _db.Execute("UPDATE Users SET visits = @p1 WHERE user_id=@p2",
 visits, userId);
 }
}
```

```csharp
public class LogVisit
{
...
 public void Execute(Guid userId, long expectedVisits)
 {
 _db.Execute(@"UPDATE Users SET visits=visits+1
 WHERE user_id=@p1 and visits = @p2",
 userId, visits);
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Implicit distributed transactions", "When to Use Transaction Script"*
---
### 31. Use Active Record for Simple Logic over Complex Data
**Principle:** Encapsulate persistence mapping in data objects when business behavior is simple but object trees or relational structures are not.
**Do:**
- Put CRUD access and mapping in active record objects.
- Orchestrate the atomic operation in a transaction script or service layer.
- Allow validation and simple calculations while keeping expectations modest.
- Use it for supporting subdomains and generic integrations.
**Don't:**
- Don't use public setters and external procedures for complex invariants.
- Don't condemn active record as “anemic” when it is the right tool.
- Don't force a rich domain model onto straightforward CRUD.

**Code:**
```csharp
public class CreateUser
{
 ...
 public void Execute(userDetails)
 {
 try
 {
 _db.StartTransaction();
 var user = new User();
 user.Name = userDetails.Name;
 user.Email = userDetails.Email;
 user.Save();
 _db.Commit();
 } catch {
 _db.Rollback();
 throw;
 }
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Active Record", "Implementation", "When to Use Active Record", "Be Pragmatic"*
---
#### 32. Expose Transaction-Script Failure Paths in Review
**Principle:** Review every effect ordering for partial writes, duplicate retries, and missing notifications.
**Do:**
- Ask what happens if execution fails after each persistence call.
- Include duplicate creation after caller retry.
- Treat agent counters, ticket persistence, and alerts as independently failing effects.
**Don't:**
- Don't stop after finding the first inconsistency.
- Don't assume application-level sequencing supplies atomicity.

**Code:**
```csharp
01. public void CreateTicket(TicketData data)
02. {
03. var agent = FindLeastBusyAgent();
04. 
05. agent.ActiveTickets = agent.ActiveTickets + 1;
06. agent.Save();
07. 
08. var ticket = new Ticket();
09. ticket.Id = Guid.New();
10. ticket.Data = data;
11. ticket.AssignedAgent = agent;
12. ticket.Save();
13. 
14. _alerts.Send(agent, "You have a new ticket!");
15. }
```

```csharp
01. public void CreateTicket(TicketData data)
02. {
03. var agent = FindLeastBusyAgent();
04. 
05. agent.ActiveTickets = agent.ActiveTickets + 1;
06. agent.Save();
07.
08. var ticket = new Ticket();
09. ticket.Id = Guid.New();
10. ticket.Data = data;
11. ticket.AssignedAgent = agent;
12. ticket.Save();
13. 
14. _alerts.Send(agent, "You have a new ticket!");
15. }
```
*Ref: Learning Domain-Driven Design.md — "Implementing Simple Business Logic — Exercises", "Answers to Exercise Questions — Chapter 5"*
---
### 33. Use a Domain Model for Complex Business Logic
**Principle:** Put data and behavior together in plain domain objects when rules, invariants, algorithms, and state transitions are entangled.
**Do:**
- Keep the model free of database, framework, and external-system concerns.
- Make code names and operations speak the bounded context’s ubiquitous language.
- Use value objects, aggregates, domain events, and domain services as building blocks.
- Centralize business decisions instead of duplicating them across application procedures.
**Don't:**
- Don't use CRUD-oriented active records for rules that must hold at all times.
- Don't make tactical DDD patterns mandatory for simple subdomains.
- Don't confuse a domain model with a data model.
*Ref: Learning Domain-Driven Design.md — "Domain Model", "Implementation", "Building Blocks"*
---
### 34. Replace Primitive Obsession with Value Objects
**Principle:** Model domain concepts as immutable values identified by their attributes.
**Do:**
- Use rich types for names, IDs, phone numbers, email addresses, height, country codes, status, and money.
- Put parsing, validation, conversion, comparison, and domain operations inside the value.
- Make invalid values hard or impossible to construct.
- Default to value objects whenever identity is unnecessary.
**Don't:**
- Don't add an ID to a value whose attributes already determine equality.
- Don't scatter validation conventions across callers.
- Don't represent money with a primitive type that invites rounding and precision defects.

**Code:**
```csharp
class Color
{
 int _red;
 int _green;
 int _blue;
}
```

```csharp
class Person
{
 private int _id;
 private string _firstName;
 private string _lastName;
 private string _landlinePhone;
 private string _mobilePhone;
 private string _email;
 private int _heightMetric;
 private string _countryCode;
 public Person(...) {...}
}
static void Main(string[] args)
{
 var dave = new Person(
 id: 30217,
 firstName: "Dave",
 lastName: "Ancelovici",
 landlinePhone: "023745001",
 mobilePhone: "0873712503",
 email: "dave@learning-ddd.com",
 heightMetric: 180,
 countryCode: "BG");
}
```

```csharp
class Person {
 private PersonId _id;
 private Name _name;
 private PhoneNumber _landline;
 private PhoneNumber _mobile;
 private EmailAddress _email;
 private Height _height;
 private CountryCode _country;
 public Person(...) { ... }
}
static void Main(string[] args)
{
 var dave = new Person(
 id: new PersonId(30217),
 name: new Name("Dave", "Ancelovici"),
 landline: PhoneNumber.Parse("023745001"),
 mobile: PhoneNumber.Parse("0873712503"),
 email: EmailAddress.Parse("dave@learning-ddd.com"),
 height: Height.FromMetric(180),
 country: CountryCode.Parse("BG"));
}
```
*Ref: Learning Domain-Driven Design.md — "Value object", "Ubiquitous language", "When to use value objects"*
---
### 35. Give Value Objects Rich, Immutable Behavior
**Principle:** Return new values from operations and implement equality by value.
**Do:**
- Decouple a concept from one representation or unit.
- Centralize valid transformations in the value object.
- Override equality and hash behavior consistently.
- Use immutability for side-effect freedom and thread safety.
**Don't:**
- Don't mutate a value in place.
- Don't compare value objects by reference or synthetic identifier.

**Code:**
```csharp
var heightMetric = Height.Metric(180);
var heightImperial = Height.Imperial(5, 3);
var string1 = heightMetric.ToString(); // "180cm"
var string2 = heightImperial.ToString(); // "5 feet 3 inches"
var string3 = heightMetric.ToImperial().ToString(); // "5 feet 11 inches"
var firstIsHigher = heightMetric > heightImperial; // true
```

```csharp
var phone = PhoneNumber.Parse("+359877123503");
var country = phone.Country; // "BG"
var phoneType = phone.PhoneType; // "MOBILE"
var isValid = PhoneNumber.IsValid("+972120266680"); // false
```

```csharp
var red = Color.FromRGB(255, 0, 0);
var green = Color.Green;
var yellow = red.MixWith(green);
var yellowString = yellow.ToString(); // "#FFFF00"
```

```csharp
public class Color
{
 public readonly byte Red;
 public readonly byte Green;
 public readonly byte Blue;
 public Color(byte r, byte g, byte b)
 {
 this.Red = r;
 this.Green = g;
 this.Blue = b;
 }
 public Color MixWith(Color other)
 {
 return new Color(
 r: (byte) Math.Min(this.Red + other.Red, 255),
 g: (byte) Math.Min(this.Green + other.Green, 255),
 b: (byte) Math.Min(this.Blue + other.Blue, 255)
 );
 }
 ...
}
```

```csharp
public class Color
{
 ...
 public override bool Equals(object obj)
 {
 var other = obj as Color;
 return other != null &&
 this.Red == other.Red &&
 this.Green == other.Green &&
 this.Blue == other.Blue;
 }
 public static bool operator == (Color lhs, Color rhs)
 {
 if (Object.ReferenceEquals(lhs, null)) {
 return Object.ReferenceEquals(rhs, null);
 }
 return lhs.Equals(rhs);
 }
 public static bool operator != (Color lhs, Color rhs)
 {
 return !(lhs == rhs);
 }
 public override int GetHashCode()
 {
 return ToString().GetHashCode();
 }
 ...
}
```
*Ref: Learning Domain-Driven Design.md — "Value object", "Implementation", "When to use value objects"*
---
### 36. Use Entities Only When Identity Persists
**Principle:** Model a mutable thing as an entity when it must remain the same instance across attribute changes.
**Do:**
- Give the entity a unique, normally immutable identifier.
- Use a domain-specific value object for the identifier.
- Let value objects describe entity properties.
- Implement entities only inside an aggregate boundary.
**Don't:**
- Don't infer sameness from matching attributes when namesakes can exist.
- Don't mutate the identity during the entity lifecycle.
- Don't make every domain noun an independent entity.

**Code:**
```csharp
class Person
{
 public Name Name { get; set; }
 public Person(Name name)
 {
 this.Name = name;
 }
}
```

```csharp
class Person
{
 public readonly PersonId Id;
 public Name Name { get; set; }
 public Person(PersonId id, Name name)
 {
 this.Id = id;
 this.Name = name;
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Entities"*
---
### 37. Make the Aggregate a Consistency Boundary
**Principle:** Permit state changes only through commands that enforce every relevant invariant.
**Do:**
- Encapsulate all state-modifying business logic inside the aggregate.
- Expose behavior, not public field mutation.
- Validate command input and invariants at the public interface.
- Keep the application layer to load, execute, save, and return the result.
**Don't:**
- Don't let external objects modify aggregate state directly.
- Don't duplicate aggregate rules in controllers, services, stored procedures, or subscribers.
- Don't call a data structure an aggregate when it defines no consistency boundary.

**Code:**
```csharp
public class Ticket
{
 ...
 public void AddMessage(UserId from, string body)
 {
 var message = new Message(from, body);
 _messages.Append(message);
 }
 ...
}
```

```csharp
public class Ticket
{
 ...
 public void Execute(AddMessage cmd)
 {
 var message = new Message(cmd.from, cmd.body);
 _messages.Append(message);
 }
 ...
}
```

```csharp
01 public ExecutionResult Escalate(TicketId id, EscalationReason reason)
02 {
03 try
04 {
05 var ticket = _ticketRepository.Load(id);
06 var cmd = new Escalate(reason);
07 ticket.Execute(cmd);
08 _ticketRepository.Save(ticket);
09 return ExecutionResult.Success();
10 }
11 catch (ConcurrencyException ex)
12 {
13 return ExecutionResult.Error(ex);
14 }
15 }
```
*Ref: Learning Domain-Driven Design.md — "Aggregates", "Consistency enforcement", "The aggregate root"*
---
### 38. Protect Aggregate Writes with Optimistic Concurrency
**Principle:** Reject a write when the aggregate version used for the decision is stale.
**Do:**
- Store a version on each aggregate.
- Increment it atomically with state changes.
- Include the expected version in the write predicate.
- Retry by reloading and re-evaluating business logic, not by blindly resubmitting state.
**Don't:**
- Don't overwrite another process’s committed decision.
- Don't use a store for aggregates unless it can enforce concurrency.

**Code:**
```csharp
class Ticket
{
 TicketId _id;
 int _version;
 ...
}
```

```sql
01 UPDATE tickets
02 SET ticket_status = @new_status,
03 agg_version = agg_version + 1
04 WHERE ticket_id=@id and agg_version=@expected_version;
```
*Ref: Learning Domain-Driven Design.md — "Consistency enforcement", "Transaction boundary"*
---
### 39. Draw Aggregate Boundaries around Strong Consistency
**Principle:** Include only entities and values that the business rules must evaluate and change atomically.
**Do:**
- Commit one aggregate instance per database transaction.
- Treat a required multi-aggregate transaction as evidence of a boundary problem.
- Keep aggregates as small as possible while preserving invariants.
- Reference external aggregates by ID.
- Include child entities only when eventual consistency would create invalid behavior.
**Don't:**
- Don't equate aggregate boundaries with tables.
- Don't traverse object references across the whole domain.
- Don't include data for convenience when rules can tolerate eventual consistency.
- Don't split one aggregate across services.

**Code:**
```csharp
01 public class Ticket
02 {
03 ...
04 List<Message> _messages;
05 ...
06
07 public void Execute(EvaluateAutomaticActions cmd)
08 {
09 if (this.IsEscalated && this.RemainingTimePercentage < 0.5 &&
10 GetUnreadMessagesCount(for: AssignedAgent) > 0)
11 {
12 _agent = AssignNewAgent();
13 }
14 }
15
16 public int GetUnreadMessagesCount(UserId id)
17 {
18 return _messages.Where(x => x.To == id && !x.WasRead).Count();
19 }
20
21 ...
22 }
```

```csharp
public class Ticket
{
 private UserId _customer;
 private List<ProductId> _products;
 private UserId _assignedAgent;
 private List<Message> _messages;
 ...
}
```

```csharp
public class Ticket
{
 ...
 List<Message> _messages;
 ...
 public void Execute(AcknowledgeMessage cmd)
 {
 var message = _messages.Where(x => x.Id == cmd.id).First();
 message.WasRead = true;
 }
 ...
}
```
*Ref: Learning Domain-Driven Design.md — "Transaction boundary", "Hierarchy of entities", "Referencing other aggregates", "The aggregate root"*
---
### 40. Publish Meaningful Domain Events
**Principle:** Record significant business facts in past tense with all data needed to understand what happened.
**Do:**
- Name events `TicketAssigned`, `TicketEscalated`, or `MessageReceived`.
- Include identity, event identity, reason, and occurrence time where relevant.
- Add events to the aggregate’s internal event collection during command handling.
- Treat events as part of the aggregate’s public interface.
- Translate private events before exposing them across bounded contexts.
**Don't:**
- Don't name an event like a command.
- Don't omit context that forces a consumer to reconstruct the event’s meaning.
- Don't publish directly to infrastructure from the aggregate.

**Code:**
```json
{
 "ticket-id": "c9d286ff-3bca-4f57-94d4-4d4e490867d1",
 "event-id": 146,
 "event-type": "ticket-escalated",
 "escalation-reason": "missed-sla",
 "escalation-time": 1628970815
}
```

```csharp
01 public class Ticket
02 {
03 ...
04 private List<DomainEvent> _domainEvents;
05 ...
06
07 public void Execute(RequestEscalation cmd)
08 {
09 if (!this.IsEscalated && this.RemainingTimePercentage <= 0)
10 {
11 this.IsEscalated = true;
12 var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
13 _domainEvents.Append(escalatedEvent);
14 }
15 }
16
17 ...
18 }
```
*Ref: Learning Domain-Driven Design.md — "Domain events", "Ubiquitous language"*
---
### 41. Use Domain Services for Stateless Domain Calculations
**Principle:** Put business logic in a stateless domain service only when it belongs naturally to neither an aggregate nor a value object.
**Do:**
- Use a service to combine read-only data from multiple aggregates or sources.
- Name it in the ubiquitous language.
- Keep state in domain objects and stores, not the service.
- Respect one aggregate write per transaction.
**Don't:**
- Don't use a domain service as a loophole for multi-aggregate writes.
- Don't confuse a domain service with a microservice or application service.
- Don't move logic out of an aggregate when the aggregate owns the invariant.

**Code:**
```csharp
public class ResponseTimeFrameCalculationService
{
 ...
 public ResponseTimeframe CalculateAgentResponseDeadline(UserId agentId,
 Priority priority, bool escalated, DateTime startTime)
 {
 var policy = _departmentRepository.GetDepartmentPolicy(agentId);
 var maxProcTime = policy.GetMaxResponseTimeFor(priority);
 if (escalated) {
 maxProcTime = maxProcTime * policy.EscalationFactor;
 }
 var shifts = _departmentRepository.GetUpcomingShifts(agentId,
 startTime, startTime.Add(policy.MaxAgentResponseTime));
 return CalculateTargetTime(maxProcTime, shifts);
 }
 ...
}
```
*Ref: Learning Domain-Driven Design.md — "Domain services"*
---
### 42. Reduce Complexity by Reducing Degrees of Freedom
**Principle:** Encapsulate invariants so fewer independent values are needed to describe and control valid state.
**Do:**
- Measure complexity by the difficulty of predicting and controlling behavior.
- Derive dependent values from a smaller set of independent inputs.
- Use value objects and aggregates to prevent invalid combinations.
**Don't:**
- Don't equate fewer methods or shorter code with lower domain complexity.
- Don't expose five independently mutable fields when invariants derive three of them.

**Code:**
```csharp
public class ClassA
{
 public int A { get; set; }
 public int B { get; set; }
 public int C { get; set; }
 public int D { get; set; }
 public int E { get; set; }
}
public class ClassB
{
 private int _a, _d;
 public int A
 {
 get => _a;
 set {
 _a = value;
 B = value / 2;
 C = value / 3;
 }
 }
 public int B { get; private set; }
 public int C { get; private set; }
 public int D
 {
 get => _d;
 set {
 _d = value;
 E = value * 2
 }
 }
 public int E { get; private set; }
}
```
*Ref: Learning Domain-Driven Design.md — "Managing Complexity"*
---
### 43. Use Event Sourcing to Model Time
**Principle:** Persist every aggregate state transition as an immutable domain event and derive state by replay.
**Do:**
- Make events the source of truth.
- Capture why a transition occurred, not only which fields changed.
- Replay a prefix to reconstruct a past state.
- Build new task-specific projections from the same event history.
- Use it for core subdomains needing audit, temporal reasoning, deep analysis, or money tracking.
**Don't:**
- Don't use a current-state table plus logs as an equivalent source of truth.
- Don't assume a database history trigger preserves business intent.
- Don't introduce event sourcing when its insight does not justify the learning and architecture costs.

**Code:**
```json
{
 "lead-id": 12,
 "event-id": 0,
 "event-type": "lead-initialized",
 "first-name": "Casey",
 "last-name": "David",
 "phone-number": "555-2951",
 "timestamp": "2020-05-20T09:52:55.95Z"
},
{
 "lead-id": 12,
 "event-id": 1,
 "event-type": "contacted",
 "timestamp": "2020-05-20T12:32:08.24Z"
},
{
 "lead-id": 12,
 "event-id": 2,
 "event-type": "followup-set",
 "followup-on": "2020-05-27T12:00:00.00Z",
 "timestamp": "2020-05-20T12:32:08.24Z"
},
{
 "lead-id": 12,
 "event-id": 3,
 "event-type": "contact-details-updated",
 "first-name": "Casey",
 "last-name": "Davis",
 "phone-number": "555-8101",
 "timestamp": "2020-05-20T12:32:08.24Z"
},
{
 "lead-id": 12,
 "event-id": 4,
 "event-type": "contacted",
 "timestamp": "2020-05-27T12:02:12.51Z"
},
{
 "lead-id": 12,
 "event-id": 5,
 "event-type": "order-submitted",
 "payment-deadline": "2020-05-30T12:02:12.51Z",
 "timestamp": "2020-05-27T12:02:12.51Z"
},
{
 "lead-id": 12,
 "event-id": 6,
 "event-type": "payment-confirmed",
 "status": "converted",
 "timestamp": "2020-05-27T12:38:44.12Z"
}
```
*Ref: Learning Domain-Driven Design.md — "Event Sourcing", "Source of Truth"*
---
### 44. Project Events into Purpose-Specific State
**Principle:** Fold the same event stream into operational, search, and analytical models optimized for different questions.
**Do:**
- Keep deterministic projection logic for each event type.
- Advance the version as every event is processed.
- Ignore events irrelevant to a projection without losing stream position.
- Persist query-oriented projections through CQRS.
**Don't:**
- Don't constrain an event stream to one state representation.
- Don't put query needs back into the write aggregate when a projection fits.

**Code:**
```csharp
public class LeadStateProjection
{
 public long LeadId { get; private set; }
 public string FirstName { get; private set; }
 public string LastName { get; private set; }
 public LeadStatus Status { get; private set; }
 public PhoneNumber PhoneNumber { get; private set; }
 public DateTime? FollowupOn { get; private set; }
 public DateTime CreatedOn { get; private set; }
 public DateTime UpdatedOn { get; private set; }
 public int Version { get; private set; }
 public void Apply(LeadInitialized @event)
 {
 LeadId = @event.LeadId;
 Status = LeadStatus.NEW_LEAD;
 FirstName = @event.FirstName;
 LastName = @event.LastName;
 PhoneNumber = @event.PhoneNumber; 
 CreatedOn = @event.Timestamp;
 UpdatedOn = @event.Timestamp; 
 FollowupOn = null;
 Version = 0;
 }
 public void Apply(Contacted @event)
 {
 UpdatedOn = @event.Timestamp;
 FollowupOn = null;
 Version += 1;
 }
 public void Apply(FollowupSet @event)
 {
 UpdatedOn = @event.Timestamp;
 FollowupOn = @event.FollowupOn;
 Status = LeadStatus.FOLLOWUP_SET;
 Version += 1;
 }
 public void Apply(ContactDetailsChanged @event)
 {
 FirstName = @event.FirstName;
 LastName = @event.LastName;
 PhoneNumber = @event.PhoneNumber;
 UpdatedOn = @event.Timestamp;
 Version += 1;
 }
 public void Apply(OrderSubmitted @event)
 {
 UpdatedOn = @event.Timestamp;
 Status = LeadStatus.PENDING_PAYMENT;
 Version += 1;
 }
 public void Apply(PaymentConfirmed @event)
 {
 UpdatedOn = @event.Timestamp;
 Status = LeadStatus.CONVERTED;
 Version += 1;
 }
}
```

```csharp
public class LeadSearchModelProjection
{
 public long LeadId { get; private set; }
 public HashSet<string> FirstNames { get; private set; }
 public HashSet<string> LastNames { get; private set; }
 public HashSet<PhoneNumber> PhoneNumbers { get; private set; }
 public int Version { get; private set; }
 public void Apply(LeadInitialized @event)
 {
 LeadId = @event.LeadId;
 FirstNames = new HashSet<string>();
 LastNames = new HashSet<string>();
 PhoneNumbers = new HashSet<PhoneNumber>();
 FirstNames.Add(@event.FirstName);
 LastNames.Add(@event.LastName);
 PhoneNumbers.Add(@event.PhoneNumber);
 Version = 0;
 }
 public void Apply(ContactDetailsChanged @event)
 {
 FirstNames.Add(@event.FirstName);
 LastNames.Add(@event.LastName);
 PhoneNumbers.Add(@event.PhoneNumber);
 Version += 1;
 }
 public void Apply(Contacted @event) {
 Version += 1;
 }
 public void Apply(FollowupSet @event) {
 Version += 1;
 }
 public void Apply(OrderSubmitted @event) {
 Version += 1;
 }
 public void Apply(PaymentConfirmed @event) {
 Version += 1;
 }
}
```

```text
LeadId: 12
FirstNames: ['Casey']
LastNames: ['David', 'Davis']
PhoneNumbers: ['555-2951', '555-8101']
Version: 6
```

```csharp
public class AnalysisModelProjection
{
 public long LeadId { get; private set; }
 public int Followups { get; private set; }
 public LeadStatus Status { get; private set; }
 public int Version { get; private set; }
 public void Apply(LeadInitialized @event)
 {
 LeadId = @event.LeadId;
 Followups = 0;
 Status = LeadStatus.NEW_LEAD;
 Version = 0;
 }
 public void Apply(Contacted @event)
 {
 Version += 1;
 }
 public void Apply(FollowupSet @event)
 {
 Status = LeadStatus.FOLLOWUP_SET;
 Followups += 1;
 Version += 1;
 }
 public void Apply(ContactDetailsChanged @event)
 {
 Version += 1;
 }
 public void Apply(OrderSubmitted @event)
 {
 Status = LeadStatus.PENDING_PAYMENT;
 Version += 1;
 }
 public void Apply(PaymentConfirmed @event)
 {
 Status = LeadStatus.CONVERTED;
 Version += 1;
 }
}
```

```text
LeadId: 12
Followups: 1
Status: Converted
Version: 6
```
*Ref: Learning Domain-Driven Design.md — "Search", "Analysis"*
---
### 45. Make the Event Store Append-Only and Concurrent
**Principle:** Fetch streams by aggregate identity and append only against the expected version.
**Do:**
- Reject appends to stale streams.
- Keep all events for one aggregate together when sharding.
- Treat the event store as the only strongly consistent source of truth.
- Add subscriptions and projection endpoints without weakening append semantics.
**Don't:**
- Don't update or delete events except exceptional migration or regulated-erasure mechanisms.
- Don't trust a secondary projection as the write source of truth.

**Code:**
```csharp
interface IEventStore
{
 IEnumerable<Event> Fetch(Guid instanceId);
 void Append(Guid instanceId, Event[] newEvents, int expectedVersion);
}
```
*Ref: Learning Domain-Driven Design.md — "Event Store", "Source of Truth"*
---
### 46. Execute an Event-Sourced Aggregate as Load–Rehydrate–Decide–Append
**Principle:** Rebuild state from history, execute a command against that state, and persist only newly produced events.
**Do:**
- Record the original version before command execution.
- Apply historical and new events through the same state projection.
- Express state transitions by appending events rather than assigning fields directly.
- Commit new events using optimistic concurrency.
**Don't:**
- Don't bypass event creation for any state transition.
- Don't mix direct state persistence with event-stream truth.

**Code:**
```csharp
01 public class TicketAPI
02 {
03 private ITicketsRepository _ticketsRepository;
04 ...
05
06 public void RequestEscalation(TicketId id, EscalationReason reason)
07 {
08 var events = _ticketsRepository.LoadEvents(id);
09 var ticket = new Ticket(events);
10 var originalVersion = ticket.Version;
11 var cmd = new RequestEscalation(reason);
12 ticket.Execute(cmd);
13 _ticketsRepository.CommitChanges(ticket, originalVersion);
14 }
15
16 ...
17 }
```

```csharp
18 public class Ticket
19 {
20 ...
21 private List<DomainEvent> _domainEvents = new List<DomainEvent>();
22 private TicketState _state;
23 ...
24
25 public Ticket(IEnumerable<IDomainEvents> events)
26 {
27 _state = new TicketState();
28 foreach (var e in events)
29 {
30 AppendEvent(e);
31 }
32 }
```

```csharp
33 private void AppendEvent(IDomainEvent @event)
34 {
35 _domainEvents.Append(@event);
36 // Dynamically call the correct overload of the "Apply" method.
37 ((dynamic)state).Apply((dynamic)@event);
38 }
```

```csharp
39 public void Execute(RequestEscalation cmd)
40 {
41 if (!_state.IsEscalated && _state.RemainingTimePercentage <= 0)
42 {
43 var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
44 AppendEvent(escalatedEvent);
45 }
46 }
47 
48 ...
49 }
```

```csharp
50 public class TicketState
51 {
52 public TicketId Id { get; private set; }
53 public int Version { get; private set; }
54 public bool IsEscalated { get; private set; }
55 ...
56 public void Apply(TicketInitialized @event)
57 {
58 Id = @event.Id;
59 Version = 0;
60 IsEscalated = false;
61 ....
62 }
63
64 public void Apply(TicketEscalated @event)
65 {
66 IsEscalated = true;
67 Version += 1;
68 }
69
70 ...
71 }
```
*Ref: Learning Domain-Driven Design.md — "Event-Sourced Domain Model"*
---
### 47. Justify Event Sourcing against Its Costs
**Principle:** Use event sourcing when time travel, deep insight, a consistent audit log, or business-aware concurrency outweigh learning and architecture costs.
**Do:**
- Use past-state reconstruction for analysis and retroactive debugging.
- Add projections to exploit historical insight.
- Inspect concurrently appended events to decide whether operations truly conflict.
- Benchmark realistic aggregate lifetimes before optimizing replay.
- Use snapshots only when measured event counts make replay costly.
- Use forgettable encrypted payloads when deletion requirements demand key erasure.
**Don't:**
- Don't snapshot preemptively; recheck oversized aggregate boundaries first.
- Don't treat immutable event schema evolution as trivial.
- Don't mistake filesystem logs, log tables, or row snapshots for business-event truth.
- Don't ignore team training and additional moving parts.
*Ref: Learning Domain-Driven Design.md — "Advantages", "Disadvantages", "Frequently Asked Questions", "Performance", "Deleting Data", "Why Can't I Just...?"*
---
### 48. Use Layered Architecture for Simple Business Logic
**Principle:** Separate presentation, business logic, and data access with top-down dependencies when the logic uses transaction scripts or active records.
**Do:**
- Treat UI, CLI, APIs, subscriptions, and outgoing message topics as presentation concerns.
- Keep business decisions in the business logic layer.
- Put databases, object storage, message buses, and external providers in data access/infrastructure.
- Let each layer depend only on the layer directly below.
**Don't:**
- Don't scatter business logic through UI and database components.
- Don't use physical tier terminology for logical layers.
- Don't force domain objects to depend on infrastructure when a richer model is required.
*Ref: Learning Domain-Driven Design.md — "Layered Architecture", "Presentation Layer", "Business Logic Layer", "Data Access Layer", "Communication Between Layers"*
---
### 49. Add a Service Layer Only to Encapsulate Orchestration
**Principle:** Use the service/application layer as a façade over use cases when it removes presentation duplication or coordinates active records.
**Do:**
- Expose operations corresponding to the public application interface.
- Reuse orchestration across GUI and API adapters.
- Keep presentation details out of the service API.
- Omit the layer when transaction scripts already provide the same façade.
**Don't:**
- Don't confuse the logical service layer with a physical service.
- Don't add a pass-through layer that repeats an existing interface.
- Don't let controllers own transactions and domain orchestration when multiple interfaces need them.

**Code:**
```csharp
namespace MvcApplication.Controllers
{
 public class UserController: Controller
 {
 ...
 [AcceptVerbs(HttpVerbs.Post)]
 public ActionResult Create(ContactDetails contactDetails)
 {
 OperationResult result = null;
 try
 {
 _db.StartTransaction();
 var user = new User();
 user.SetContactDetails(contactDetails);
 user.Save();
 _db.Commit();
 result = OperationResult.Success;
 } catch (Exception ex) {
 _db.Rollback();
 result = OperationResult.Exception(ex);
 }
 return View(result);
 }
 }
}
```

```csharp
interface CampaignManagementService
{
 OperationResult CreateCampaign(CampaignDetails details);
 OperationResult Publish(CampaignId id, PublishingSchedule schedule);
 OperationResult Deactivate(CampaignId id);
 OperationResult AddDisplayLocation(CampaignId id, DisplayLocation newLocation); 
 ...
}
```

```csharp
namespace ServiceLayer
{
 public class UserService
 {
 ...
 public OperationResult Create(ContactDetails contactDetails)
 {
 OperationResult result = null;
 try
 {
 _db.StartTransaction();
 var user = new User();
 user.SetContactDetails(contactDetails);
 user.Save();
 _db.Commit();
 result = OperationResult.Success;
 } catch (Exception ex) {
 _db.Rollback();
 result = OperationResult.Exception(ex);
 }
 return result;
 }
 ...
 }
}
namespace MvcApplication.Controllers
{
 public class UserController: Controller
 {
 ...
 [AcceptVerbs(HttpVerbs.Post)]
 public ActionResult Create(ContactDetails contactDetails)
 {
 var result = _userService.Create(contactDetails);
 return View(result);
 }
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Variation", "Service layer"*
---
### 50. Put the Domain at the Center with Ports and Adapters
**Principle:** Make business logic define abstract ports and make infrastructure supply technology-specific adapters.
**Do:**
- Apply dependency inversion so high-level domain logic never depends on low-level infrastructure.
- Resolve adapters through dependency injection or bootstrapping.
- Keep application use cases as the public façade.
- Use this architecture for domain models and event-sourced domain models.
- Recognize hexagonal, onion, and clean architecture as variants of the same dependency idea.
**Don't:**
- Don't let persistence or messaging interfaces be defined by infrastructure and imported into the domain.
- Don't debate variant names while ignoring dependency direction.

**Code:**
```csharp
namespace App.BusinessLogicLayer
{
 public interface IMessaging
 {
 void Publish(Message payload);
 void Subscribe(Message type, Action callback);
 }
}
namespace App.Infrastructure.Adapters
{
 public class SQSBus: IMessaging { ... }
}
```
*Ref: Learning Domain-Driven Design.md — "Ports & Adapters", "Dependency Inversion Principle", "Integration of Infrastructural Components", "Variants"*
---
### 51. Use CQRS for Multiple Persistent Models
**Principle:** Keep one strongly consistent command model and derive any number of read-only projections.
**Do:**
- Use the command model to validate commands, enforce invariants, and serve as source of truth.
- Build read models for UI, integration, search, analytics, or performance needs.
- Make every projection disposable and rebuildable from the command model.
- Use synchronous catch-up subscriptions with durable checkpoints as the baseline.
- Add asynchronous projection only when its scaling benefit justifies distributed-systems complexity.
- Return success, failure, and strongly consistent data from commands when useful.
**Don't:**
- Don't update read models directly.
- Don't claim CQRS means commands cannot return data.
- Don't return immediately expected data from eventually consistent projections.
- Don't assume out-of-order or duplicate asynchronous messages are harmless.
- Don't apply one architecture systemwide; choose per subdomain module.
*Ref: Learning Domain-Driven Design.md — "Command-Query Responsibility Segregation", "Implementation", "Projecting Read Models", "Challenges", "Model Segregation", "Scope"*
---
### 52. Translate Models at Context Boundaries
**Principle:** Select stateless or stateful translation based on whether transformation requires memory, aggregation, or multiple sources.
**Do:**
- Embed synchronous translation in the context or an API gateway.
- Use a message proxy for asynchronous translation and filtering.
- Use persistent state when batching messages, combining fine-grained events, or unifying sources.
- Consider stream-processing or batching products instead of custom stateful machinery.
- Use a backend-for-frontend when a UI needs a unified model from several contexts.
**Don't:**
- Don't use an API gateway for transformations requiring durable aggregation state.
- Don't expose domain events unchanged while claiming the public model is decoupled.
- Don't mix integration complexity with core business logic when an ACL can isolate it.
*Ref: Learning Domain-Driven Design.md — "Model Translation", "Stateless Model Translation", "Stateful Model Translation"*
---
### 53. Publish Events Reliably with an Outbox
**Principle:** Commit aggregate state and outgoing events atomically, then relay events independently with at-least-once delivery.
**Do:**
- Store state and outbox entries in one database transaction.
- Poll indexed unpublished records or tail the transaction log.
- Mark or delete an event only after successful publication.
- Embed the outbox in an aggregate document when multidocument transactions are unavailable.
- Make consumers deduplicate because relay failure can republish an event.
**Don't:**
- Don't publish from inside the aggregate before commit.
- Don't commit state and then publish directly from the application process.
- Don't promise exactly-once delivery from the outbox.

**Code:**
```csharp
01 public class Campaign
02 {
03 ...
04 List<DomainEvent> _events;
05 IMessageBus _messageBus;
06 ...
07
08 public void Deactivate(string reason)
09 {
10 for (l in _locations.Values())
11 {
12 l.Deactivate();
13 }
14
15 IsActive = false;
16
17 var newEvent = new CampaignDeactivated(_id, reason);
18 _events.Append(newEvent);
19 _messageBus.Publish(newEvent);
20 }
21 }
```

```csharp
01 public class ManagementAPI
02 {
03 ...
04 private readonly IMessageBus _messageBus;
05 private readonly ICampaignRepository _repository;
06 ...
07 public ExecutionResult DeactivateCampaign(CampaignId id, string reason)
08 {
09 try
10 {
11 var campaign = repository.Load(id);
12 campaign.Deactivate(reason);
13 _repository.CommitChanges(campaign);
14
15 var events = campaign.GetUnpublishedEvents();
16 for (IDomainEvent e in events)
17 {
18 _messageBus.publish(e);
19 }
20 campaign.ClearUnpublishedEvents();
21 }
22 catch(Exception ex)
23 {
24 ...
25 }
26 }
27 }
```

```json
{
 "campaign-id": "364b33c3-2171-446d-b652-8e5a7b2be1af",
 "state": {
 "name": "Autumn 2017",
 "publishing-state": "DEACTIVATED",
 "ad-locations": [
  ...
 ]
 ...
 },
 "outbox": [
 {
 "campaign-id": "364b33c3-2171-446d-b652-8e5a7b2be1af",
 "type": "campaign-deactivated",
 "reason": "Goals met",
 "published": false
 }
 ]
}
```
*Ref: Learning Domain-Driven Design.md — "Integrating Aggregates", "Outbox", "Fetching unpublished events"*
---
### 54. Coordinate Linear Cross-Aggregate Work with a Saga
**Principle:** Map events to subsequent commands and compensations across multiple transactions while accepting eventual consistency.
**Do:**
- Use a saga for a long-running process measured in transactions, not elapsed time.
- React to committed events and issue the next command.
- Define compensating actions for failed steps.
- Persist saga state when compensation depends on execution history.
- Separate saga state transitions from command execution with an outbox-like relay.
**Don't:**
- Don't use a saga to repair an aggregate that was split incorrectly.
- Don't claim transactions across participants are atomic.
- Don't put branching workflow intelligence in a simple event-to-command saga.

**Code:**
```csharp
public class CampaignPublishingSaga
 private readonly ICampaignRepository _repository;
 private readonly IPublishingServiceClient _publishingService;
 ...
 public void Process(CampaignActivated @event)
 {
 var campaign = _repository.Load(@event.CampaignId);
 var advertisingMaterials = campaign.GenerateAdvertisingMaterials();
 _publishingService.SubmitAdvertisement(@event.CampaignId,
 advertisingMaterials);
 }
 public void Process(PublishingConfirmed @event)
 {
 var campaign = _repository.Load(@event.CampaignId);
 campaign.TrackPublishingConfirmation(@event.ConfirmationId);
 _repository.CommitChanges(campaign);
 }
 public void Process(PublishingRejected @event)
 {
 var campaign = _repository.Load(@event.CampaignId);
 campaign.TrackPublishingRejection(@event.RejectionReason);
 _repository.CommitChanges(campaign);
 }
}
```

```csharp
public class CampaignPublishingSaga
{
 private readonly ICampaignRepository _repository;
 private readonly IList<IDomainEvent> _events;
 ...
 public void Process(CampaignActivated activated)
 {
 var campaign = _repository.Load(activated.CampaignId);
 var advertisingMaterials = campaign.GenerateAdvertisingMaterials();
 var commandIssuedEvent = new CommandIssuedEvent(
 target: Target.PublishingService,
 command: new SubmitAdvertisementCommand(activated.CampaignId,
 advertisingMaterials));
 _events.Append(activated);
 _events.Append(commandIssuedEvent);
 }
 public void Process(PublishingConfirmed confirmed)
 {
 var commandIssuedEvent = new CommandIssuedEvent(
 target: Target.CampaignAggregate,
 command: new TrackConfirmation(confirmed.CampaignId,
 confirmed.ConfirmationId));
 _events.Append(confirmed);
 _events.Append(commandIssuedEvent);
 }
 public void Process(PublishingRejected rejected)
 {
 var commandIssuedEvent = new CommandIssuedEvent(
 target: Target.CampaignAggregate,
 command: new TrackRejection(rejected.CampaignId,
 rejected.RejectionReason));
 _events.Append(rejected);
 _events.Append(commandIssuedEvent);
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Saga", "Consistency"*
---
### 55. Use a Process Manager for Stateful Branching Workflows
**Principle:** Model an explicitly instantiated business process that owns routing state and decides the next step.
**Do:**
- Switch from saga to process manager when next-step choice requires `if/else` business logic.
- Give the process explicit identity and persistent state.
- Implement it as a state-based or event-sourced aggregate.
- Emit command-issued events and execute commands asynchronously.
**Don't:**
- Don't bind a multipath process to one implicit initiating event when the process itself is the entity.
- Don't execute remote commands inside the same state transition that records the routing decision.

**Code:**
```csharp
public class BookingProcessManager
{
 private readonly IList<IDomainEvent> _events;
 private BookingId _id;
 private Destination _destination;
 private TripDefinition _parameters;
 private EmployeeId _traveler;
 private Route _route;
 private IList<Route> _rejectedRoutes;
 private IRoutingService _routing;
 ...
 public void Initialize(Destination destination,
 TripDefinition parameters,
                       EmployeeId traveler)
 {
 _destination = destination;
 _parameters = parameters;
 _traveler = traveler;
 _route = _routing.Calculate(destination, parameters);
 var routeGenerated = new RouteGeneratedEvent(
 BookingId: _id,
 Route: _route);
 var commandIssuedEvent = new CommandIssuedEvent(
 command: new RequestEmployeeApproval(_traveler, _route)
 );
 _events.Append(routeGenerated);
 _events.Append(commandIssuedEvent);
 }
 public void Process(RouteConfirmed confirmed)
 {
 var commandIssuedEvent = new CommandIssuedEvent(
 command: new BookFlights(_route, _parameters)
 );
 _events.Append(confirmed);
 _events.Append(commandIssuedEvent);
 }
 public void Process(RouteRejected rejected)
 {
 var commandIssuedEvent = new CommandIssuedEvent(
 command: new RequestRerouting(_traveler, _route)
 );
 _events.Append(rejected);
 _events.Append(commandIssuedEvent);
 }
 public void Process(ReroutingConfirmed confirmed)
 {
 _rejectedRoutes.Append(route);
 _route = _routing.CalculateAltRoute(destination,
 parameters, rejectedRoutes);
 var routeGenerated = new RouteGeneratedEvent(
 BookingId: _id,
 Route: _route);
 var commandIssuedEvent = new CommandIssuedEvent(
 command: new RequestEmployeeApproval(_traveler, _route)
 );
 _events.Append(confirmed);
 _events.Append(routeGenerated);
 _events.Append(commandIssuedEvent);
 }
 public void Process(FlightBooked booked)
 {
 var commandIssuedEvent = new CommandIssuedEvent(
 command: new BookHotel(_destination, _parameters)
 );
 _events.Append(booked);
 _events.Append(commandIssuedEvent);
 }
```
*Ref: Learning Domain-Driven Design.md — "Process Manager"*
---
### 56. Select Tactics with a Decision Tree
**Principle:** Choose business-logic pattern first from actual complexity, then architecture and testing strategy.
**Do:**
- Use event-sourced domain model for money, consistent audit, temporal behavior, or deep analysis.
- Otherwise use domain model for complex rules and invariants.
- Otherwise use active record for complex data structures.
- Otherwise use transaction script.
- Pair transaction script with minimal layered architecture.
- Pair active record with layered architecture plus service layer.
- Pair domain model with ports and adapters.
- Pair event-sourced domain model with CQRS.
- Add CQRS independently when multiple persistent representations are required.
**Don't:**
- Don't treat the heuristic as a proof or replace critical thinking.
- Don't standardize one pattern across all modules.
- Don't infer business classification without validating it with domain experts.
*Ref: Learning Domain-Driven Design.md — "Business Logic Implementation Patterns", "Architectural Patterns", "Tactical Design Decision Tree"*
---
### 57. Match Testing Shape to the Business-Logic Pattern
**Principle:** Test at the boundary where the chosen design concentrates behavior.
**Do:**
- Use a testing pyramid for domain models and event-sourced domain models; aggregates and values are effective units.
- Use a testing diamond for active record; emphasize service-to-data integration.
- Use a reversed testing pyramid for transaction scripts; verify simple end-to-end flows.
- Derive test investment from business complexity rather than a universal ratio.
**Don't:**
- Don't call one testing shape correct for every module.
- Don't over-mock an active record flow whose behavior spans application and storage.
- Don't omit end-to-end verification of procedural workflows.
*Ref: Learning Domain-Driven Design.md — "Testing Strategy", "Testing Pyramid", "Testing Diamond", "Reversed Testing Pyramid"*
---
### 58. Evolve Design Decisions with the Domain
**Principle:** Treat subdomain classification, bounded contexts, relationships, and implementation patterns as changeable decisions.
**Do:**
- Reclassify core to generic when a commodity solution overtakes custom advantage.
- Reclassify generic to core when an in-house capability becomes differentiating.
- Reclassify supporting to core when profitable complexity grows.
- Move implementation in-house when a capability becomes core; consider outsourcing after it ceases to be core.
- Treat implementation pain as a signal to reassess both domain classification and tactical design.
**Don't:**
- Don't gold-plate every subdomain for hypothetical future complexity.
- Don't cling to a design after current needs invalidate it.
- Don't ignore increasing change frequency, duplicated rules, and consistency defects.
*Ref: Learning Domain-Driven Design.md — "Changes in Domains", "Strategic Design Concerns", "Tactical Design Concerns", "Don't ignore pain"*
---
### 59. Refactor Up the Tactical Complexity Ladder
**Principle:** Move from transaction script to active record to domain model to event-sourced domain model in controlled steps as complexity demands.
**Do:**
- Extract complicated data structures into active records when mapping dominates scripts.
- Identify value objects first when moving from active record to domain model.
- Make setters private to expose every external state mutation as a compilation failure.
- Move mutation logic inside object boundaries.
- Find the smallest strong-consistency boundaries, designate roots, and reference other aggregates by ID.
- Establish sound state-based aggregates before adopting event sourcing.
**Don't:**
- Don't jump from active records straight to event sourcing in a brownfield model.
- Don't preserve external setter logic after calling an object an aggregate.
- Don't migrate before understanding transactional boundaries.

**Code:**
```csharp
public class Player
{
 public Guid Id { get; set; }
 public int Points { get; set; }
}
public class ApplyBonus
{
 ...
 public void Execute(Guid playerId, byte percentage)
 {
 var player = _repository.Load(playerId);
 player.Points *= 1 + percentage/100.0;
 _repository.Save(player);
 }
}
```

```csharp
public class Player
{
 public Guid Id { get; private set; }
 public int Points { get; private set; }
}
public class ApplyBonus
{
 ...
 public void Execute(Guid playerId, byte percentage)
 {
 var player = _repository.Load(playerId);
 player.Points *= 1 + percentage/100.0;
 _repository.Save(player);
 }
}
```

```csharp
public class Player
{
 public Guid Id { get; private set; }
 public int Points { get; private set; }
 public void ApplyBonus(int percentage)
 {
 this.Points *= 1 + percentage/100.0;
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Transaction Script to Active Record", "Active Record to Domain Model", "Domain Model to Event-Sourced Domain Model"*
---
### 60. Make Event-Sourcing Migration Honest
**Principle:** Either reconstruct approximate events explicitly or record one migration event that admits missing history.
**Do:**
- Test reconstructed streams by projecting and comparing them with original state.
- State clearly that generated historical events are incomplete.
- Prefer a migration event when pretending to know past transitions would mislead analysis.
- Keep projection logic able to process migration events permanently.
**Don't:**
- Don't claim approximate event history is a complete audit trail.
- Don't invent events whose count or sequence cannot be recovered.
- Don't hide legacy provenance from future consumers.

**Code:**
```json
{
 "lead-id": 12,
 "event-id": 0,
 "event-type": "lead-initialized",
 "first-name": "Shauna",
 "last-name": "Mercia",
 "phone-number": "555-4753"
},
{
 "lead-id": 12,
 "event-id": 1,
 "event-type": "contacted",
 "timestamp": "2020-05-27T12:02:12.51Z"
},
{
 "lead-id": 12,
 "event-id": 2,
 "event-type": "order-submitted",
 "payment-deadline": "2020-05-30T12:02:12.51Z",
 "timestamp": "2020-05-27T12:02:12.51Z"
},
{
 "lead-id": 12,
 "event-id": 3,
 "event-type": "payment-confirmed",
 "status": "converted",
 "timestamp": "2020-05-27T12:38:44.12Z"
}
```

```json
{
 "lead-id": 12,
 "event-id": 0,
 "event-type": "migrated-from-legacy",
 "first-name": "Shauna",
 "last-name": "Mercia",
 "phone-number": "555-4753",
 "status": "converted",
 "last-contacted-on": "2020-05-27T12:02:12.51Z",
 "order-placed-on": "2020-05-27T12:02:12.51Z",
 "converted-on": "2020-05-27T12:38:44.12Z",
 "followup-on": null
}
```
*Ref: Learning Domain-Driven Design.md — "Generating Past Transitions", "Modeling Migration Events"*
---
### 61. Control Growth-Driven Complexity
**Principle:** Revisit every boundary as the system grows, eliminating accidental complexity while modeling essential business complexity.
**Do:**
- Redistill growing subdomains into coherent use-case sets.
- Extract focused contexts when models become jacks of all trades.
- Treat chatty contexts as evidence of ineffective boundaries.
- Extract data and behavior from an aggregate when they no longer require strong consistency.
- Change integration relationships when team communication changes.
**Don't:**
- Don't distribute new functionality among existing components merely because they already exist.
- Don't let old decisions become untouchable architecture.
- Don't confuse successful growth with permission for unregulated growth.
*Ref: Learning Domain-Driven Design.md — "Organizational Changes", "Domain Knowledge", "Growth", "Subdomains", "Bounded Contexts", "Aggregates"*
---
### 62. Run EventStorming for Shared Discovery
**Principle:** Model a scoped business process collaboratively as a timeline of events, commands, policies, reads, systems, aggregates, and contexts.
**Do:**
1. Brainstorm past-tense domain events on orange notes.
2. Order the happy path, then alternatives.
3. Mark bottlenecks, manual work, and knowledge gaps as pain points.
4. Mark pivotal events that indicate context changes.
5. Add imperative commands and relevant actors.
6. Add policies that connect observed events to commands.
7. Add read models actors need before decisions.
8. Add external systems that issue commands or receive events.
9. Group commands and events into aggregate candidates.
10. Group related aggregates into bounded-context candidates.
**Do:**
- Invite diverse experts, engineers, testers, product, UX, and operations participants.
- Keep in-person groups small enough for everyone to contribute.
- Use the process for language building, requirements exploration, knowledge recovery, improvement, and onboarding.
- Treat the resulting model as a bonus; value the shared mental model most.
**Don't:**
- Don't begin by enforcing order or removing duplicate events during brainstorming.
- Don't force every command to have a human actor.
- Don't use EventStorming for an obvious linear process with no interesting logic.
- Don't infer that an EventStorming result requires event sourcing.
*Ref: Learning Domain-Driven Design.md — "EventStorming", "The EventStorming Process", "When to Use EventStorming", "Facilitation Tips"*
---
### 63. Modernize Brownfield Systems Strategically
**Principle:** Understand the business and current design, then modernize the highest-value pain points incrementally.
**Do:**
- Identify business domains, customers, value, competition, subdomains, and types.
- Find current lifecycle boundaries even inside a monorepo or monolith.
- Chart the current system as a context map.
- Look for multiple teams in one component, duplicated core logic, outsourced core work, failing integrations, and foreign models.
- Introduce logical subdomain boundaries before extracting physical contexts.
- Use EventStorming to recover lost knowledge.
**Don't:**
- Don't start with a big rewrite.
- Don't modernize uniformly; accept that not all of a large system deserves equal design investment.
- Don't extract services before identifying the business boundary and value.
*Ref: Learning Domain-Driven Design.md — "Strategic Analysis", "Understand the Business Domain", "Explore the Current Design", "Modernization Strategy"*
---
### 64. Strangle or Refactor in Small Steps
**Principle:** Replace legacy behavior gradually behind a façade or improve it in place while preserving business continuity.
**Do:**
- Route new behavior to a new context while freezing nonessential legacy development.
- Remove the façade and legacy system after migration completes.
- Permit temporary database sharing only with an explicit retirement path.
- Introduce value objects and aggregate encapsulation incrementally during in-place refactoring.
- Protect new models with ACLs and consumers with published languages.
**Don't:**
- Don't let temporary shared storage become permanent context coupling.
- Don't refactor to an event-sourced model before validating state-based aggregate boundaries.
- Don't sell DDD by authority; explain the consistency, coupling, and business reasons.
*Ref: Learning Domain-Driven Design.md — "Strategic Modernization", "Tactical Modernization", "Strangler pattern", "Refactoring tactical design decisions", "Undercover Domain-Driven Design"*
---
### 65. Design Deep Microservices, Not Tiny Services
**Principle:** Minimize the service’s public interface relative to the complexity it encapsulates, while balancing local and global system complexity.
**Do:**
- Treat a service’s prescribed interface as its front door.
- Encapsulate the database behind a compact public protocol.
- Prefer deep modules with simple interfaces over shallow wrappers.
- Use bounded contexts as the widest safe boundaries and subdomains as a strong microservice heuristic.
- Consider aggregate-sized services only after evaluating their interactions and nonfunctional needs.
- Compress interfaces with OHS and isolate incoming complexity with ACLs.
**Don't:**
- Don't define “micro” by lines of code, team size, or one method.
- Don't optimize local service simplicity while creating global integration complexity.
- Don't assume every bounded context must be a microservice.
- Don't split an aggregate across services.

**Code:**
```csharp
int AddTwoNumbers(int a, int b)
{
 return a + b;
}
```
*Ref: Learning Domain-Driven Design.md — "What Is a Microservice?", "Design Goal", "System Complexity", "Microservices as Deep Services", "Domain-Driven Design and Microservices' Boundaries"*
---
### 66. Distinguish Events, Commands, and Messages
**Principle:** Treat a command as a rejectable request and an event as an immutable fact that already happened; both can travel as messages.
**Do:**
- Name events in past tense and commands in the imperative.
- Include event identity, correlation, subject identity, time, and payload as needed.
- Use compensation commands to counteract completed events.
- Separate event sourcing inside a service from event-driven integration across services.
**Don't:**
- Don't let a consumer “reject” a historical event.
- Don't publish internal event-sourced transitions merely because the integration is event-driven.
- Don't use event, command, and message as synonyms.

**Code:**
```json
{
 "type": "delivery-confirmed",
 "event-id": "14101928-4d79-4da6-9486-dbc4837bc612",
 "correlation-id": "08011958-6066-4815-8dbe-dee6d9e5ebac",
 "delivery-id": "05011927-a328-4860-a106-737b2929db4e",
 "timestamp": 1615718833,
 "payload": {
 "confirmed-by": "17bc9223-bdd6-4382-954d-f1410fd286bd",
 "delivery-time": 1615701406
 }
}
```
*Ref: Learning Domain-Driven Design.md — "Event-Driven Architecture", "Events, Commands, and Messages", "Structure"*
---
### 67. Select the Correct Integration Event Type
**Principle:** Choose event notification, event-carried state transfer, or public domain event according to consumer data and consistency needs.
**Do:**
- Use a terse notification plus query when authorization or latest-state consistency matters.
- Use ECST to replicate enough state for a local cache and tolerate producer outages.
- Use a public domain event when the business occurrence itself, with full context, is the contract.
- Design public and private events separately.
- Use version information when consumers maintain replicated state.
**Don't:**
- Don't call ECST a domain event merely because both carry data.
- Don't expose every internal domain event to external consumers.
- Don't use a notification when consumers cannot query the producer reliably.
- Don't use ECST when the consumer must read the producer’s last committed write synchronously.

**Code:**
```json
{
 "type": "paycheck-generated",
 "event-id": "537ec7c2-d1a1-2005-8654-96aee1116b72",
 "delivery-id": "05011927-a328-4860-a106-737b2929db4e",
 "timestamp": 1615726445,
 "payload": {
 "employee-id": "456123",
 "link": "/paychecks/456123/2021/01"
 }
}
```

```json
{
 "type": "customer-updated",
 "event-id": "6b7ce6c6-8587-4e4f-924a-cec028000ce6",
 "customer-id": "01b18d56-b79a-4873-ac99-3d9f767dbe61",
 "timestamp": 1615728520,
 "payload": {
 "first-name": "Carolyn",
 "last-name": "Hayes",
 "phone": "555-1022",
 "status": "follow-up-set",
 "follow-up-date": "2021/05/08",
 "birthday": "1982/04/05",
 "version": 7
 }
}
```

```json
{
 "type": "customer-updated",
 "event-id": "6b7ce6c6-8587-4e4f-924a-cec028000ce6",
 "customer-id": "01b18d56-b79a-4873-ac99-3d9f767dbe61",
 "timestamp": 1615728520,
 "payload": {
 "status": "follow-up-set",
 "follow-up-date": "2021/05/10",
 "version": 8
 }
}
```

```javascript
eventNotification = {
 "type": "marriage-recorded",
 "person-id": "01b9a761",
 "payload": {
 "person-id": "126a7b61",
 "details": "/01b9a761/marriage-data"
 }
};
ecst = {
 "type": "personal-details-changed",
 "person-id": "01b9a761",
 "payload": {
 "new-last-name": "Williams"
 }
};
domainEvent = {
 "type": "married",
 "person-id": "01b9a761",
 "payload": {
 "person-id": "126a7b61",
 "assumed-partner-last-name": true
 }
};
```
*Ref: Learning Domain-Driven Design.md — "Types of Events", "Event notification", "Event-carried state transfer", "Domain event", "Event types: Example"*
---
### 68. Prevent the Distributed Big Ball of Mud
**Principle:** Design asynchronous contracts to remove temporal, functional, and implementation coupling.
**Do:**
- Replace timing delays with an event emitted after the prerequisite calculation completes.
- Put duplicated projection logic behind the producing context’s consumer-driven published language.
- Expose a restrained integration model rather than all internal events.
- Assume network slowness, server failure, duplicates, and out-of-order delivery.
- Use outbox, deduplication, ordering metadata, sagas, and process managers.
**Don't:**
- Don't coordinate consumers with arbitrary sleep periods.
- Don't make multiple consumers implement the same projection with the same reason to change.
- Don't couple subscribers to every internal event schema.
- Don't expect asynchronous delivery to create loose coupling automatically.
*Ref: Learning Domain-Driven Design.md — "Distributed Big Ball of Mud", "Temporal Coupling", "Functional Coupling", "Implementation Coupling", "Event-Driven Design Heuristics"*
---
### 69. Apply DDD Boundaries to Analytical Data
**Principle:** Give each bounded-context team ownership of both operational and analytical models, and expose analytical data as a product.
**Do:**
- Distinguish OLTP models of entity lifecycles from OLAP models of business activities.
- Model analytical facts as append-only activities and dimensions as descriptive attributes.
- Use star or snowflake schemas according to query and maintenance trade-offs.
- Publish discoverable, versioned analytical output ports with schemas and SLAs.
- Supply a self-service platform for interoperable data products.
- Establish federated governance across product and platform owners.
- Use OHS for analytical published languages and CQRS for regenerable projections.
**Don't:**
- Don't build one enterprise-wide analytical model.
- Don't let ETL depend silently on operational database internals.
- Don't turn a schema-less lake into an ungoverned data swamp.
- Don't separate analytical ownership from the teams holding the domain knowledge.
*Ref: Learning Domain-Driven Design.md — "Analytical Data Model Versus Transactional Data Model", "Fact Table", "Dimension Table", "Data Warehouse", "Data Lake", "Data Mesh", "Combining Data Mesh and Domain-Driven Design"*
---
### 70. Learn from the Marketnovus Case Study
**Principle:** Prefer ubiquitous language everywhere over aggregates everywhere, and let observed business complexity—not labels—select the pattern.
**Do:**
- Preserve a strong language even when time-to-market requires a simple architecture.
- Keep one team and one language around an aggregate and its rules.
- Reclassify a supporting capability when business rules become profitable and complex.
- Use language complexity as an early signal that active records no longer fit.
- Start with wider safe boundaries and extract services after learning.
- Reverse-check subdomain classification against the implementation pattern the requirements actually need.
**Don't:**
- Don't pronounce every noun an aggregate.
- Don't split one aggregate’s logic between application code and a database team.
- Don't let simple supporting logic inherit event sourcing merely because management calls the initiative core.
- Don't draw one service boundary around every aggregate without analyzing chatty interactions.
- Don't ignore implementation pain; it signals a mismatched model or tactic.
*Ref: Learning Domain-Driven Design.md — "Applying DDD: A Case Study", "Five Bounded Contexts", "Discussion", "Ubiquitous Language", "Subdomains", "Boundaries of Bounded Contexts"*
---
## Anti-Patterns & Common Mistakes

- **Technology-first design:** Choose tools before understanding the business → *fix:* analyze the domain, strategy, and subdomain types first.
- **Enterprise-wide ubiquitous language:** Force one meaning across incompatible mental models → *fix:* define bounded contexts.
- **Translation chain:** Pass knowledge through analysts, documents, designs, and code → *fix:* connect engineers and domain experts directly.
- **Primitive obsession:** Encode concepts as raw strings and numbers → *fix:* introduce immutable value objects.
- **Identity everywhere:** Add IDs to values → *fix:* use attribute-based identity unless lifecycle identity matters.
- **Anemic aggregate:** Expose setters and keep rules in services → *fix:* move all state mutation behind aggregate commands.
- **Aggregate per table:** Follow persistence layout instead of invariants → *fix:* draw consistency boundaries from business rules.
- **One giant aggregate:** Include every reachable entity → *fix:* keep only strongly consistent data and reference others by ID.
- **Multi-aggregate transaction:** Depend on atomic changes across roots → *fix:* redesign boundaries or coordinate eventual consistency.
- **Stored-procedure rule duplication:** Split one model across code and database teams → *fix:* keep one implementation of each invariant inside the owning boundary.
- **Outbox omission:** Commit then publish → *fix:* commit state and event together, relay later.
- **Event publication inside aggregate:** Publish before commit → *fix:* collect domain events and persist them atomically.
- **Saga as boundary repair:** Coordinate data that must be strongly consistent → *fix:* put it in one aggregate.
- **CQRS dogma:** Prevent commands returning data → *fix:* return strongly consistent results when useful.
- **Asynchronous projection by default:** Accept duplicate and ordering risk without need → *fix:* implement synchronous catch-up first.
- **Internal event leakage:** Publish every event-sourced transition → *fix:* design public integration events.
- **Timing-based orchestration:** Add arbitrary processing delays → *fix:* publish completion notifications.
- **Shared kernel sprawl:** Share broad volatile models → *fix:* minimize scope and run all affected integration tests.
- **One-method microservices:** Minimize local code while maximizing integration → *fix:* design deep services around coherent capabilities.
- **Aggregate-sized services by default:** Turn every root into a network boundary → *fix:* evaluate subdomain coherence and global complexity.
- **Big rewrite:** Replace a legacy system atomically → *fix:* strangle or refactor incrementally.
- **Premature event sourcing:** Add temporal architecture to simple logic → *fix:* use the lightest fitting pattern.
- **Fake event history:** Manufacture a complete past from current state → *fix:* mark approximation or use a migration event.
- **Universal architecture:** Apply one pattern to every module → *fix:* choose per subdomain.
- **Static classification:** Keep yesterday’s core/supporting/generic label → *fix:* review business value and complexity continuously.
- **Data warehouse trespass:** Read operational internals as analytical contracts → *fix:* publish owned analytical data products.

## Decision Heuristics / Checklists

### Domain Analysis
- What service and value does the organization provide?
- Who are the customers and competitors?
- Which capabilities differentiate the company?
- Which capabilities are solved generically?
- Which capabilities are necessary but obvious?
- Which apparently broad capability hides different subdomain types?
- Which coherent use cases share actors, entities, and data?
- Which business advantages are nontechnical?

### Ubiquitous Language
- Can domain experts use every term comfortably?
- Is each term unambiguous inside its bounded context?
- Are synonyms hiding distinct concepts?
- Does code use the same nouns and verbs as conversation?
- Do tests capture behavior and invariants, not just nouns?
- Has new knowledge been reflected everywhere?

### Bounded Context
- What exact problem makes this model useful?
- Where does the language become inconsistent?
- Does one team own the context?
- Can its lifecycle evolve independently?
- Are changes repeatedly crossing multiple contexts?
- Are contexts chatty because one coherent model was split?
- Is domain uncertainty high enough to justify wider initial boundaries?

### Integration Pattern
- Reciprocal goals and strong communication → **Partnership**.
- Shared model cheaper than duplication → **Shared Kernel**.
- Upstream model acceptable → **Conformist**.
- Downstream model requires protection → **Anticorruption Layer**.
- Supplier protects many consumers → **Open-Host Service**.
- Duplication cheaper and capability noncore → **Separate Ways**.

### Business-Logic Pattern
- Money, temporal history, consistent audit, deep behavioral analysis → **Event-Sourced Domain Model**.
- Complex rules, invariants, algorithms, state transitions → **Domain Model**.
- Simple behavior over complex data structures → **Active Record**.
- Simple behavior and simple data flow → **Transaction Script**.

### Architecture
- Transaction script → **minimal layered architecture**.
- Active record → **layered architecture plus service layer**.
- Domain model → **ports and adapters**.
- Event-sourced domain model → **CQRS plus ports and adapters**.
- Multiple persistent views needed independently → **consider CQRS**.

### Aggregate Review
- What invariant does this aggregate protect?
- Which data must be strongly consistent for that invariant?
- Can any child move out and be referenced by ID?
- Is every mutation reachable only through the root?
- Does one transaction modify only one aggregate instance?
- Is every write protected by an expected version?
- Are domain events business facts in the ubiquitous language?

### Event Integration
- Must the consumer read the latest producer state → **notification plus query**.
- Can the consumer use eventual consistency and a local cache → **ECST**.
- Is the business occurrence itself the contract → **public domain event**.
- Can every message be duplicated or reordered safely?
- Are publication and state commit atomic through an outbox?
- Are internal and public events explicitly separated?

### Modernization
- Which core pain point yields the most business value?
- Can logical subdomain boundaries be established first?
- Should the component be strangled or refactored in place?
- Can value objects reduce complexity immediately?
- Are aggregate boundaries understood before event sourcing?
- Is shared storage explicitly temporary?
- Does every migration step preserve behavior and ownership clarity?

## Key Takeaways

1. Start with business strategy, not architecture.
2. Classify subdomains to allocate engineering investment rationally.
3. Build a ubiquitous language in every subdomain, regardless of tactical sophistication.
4. Discover subdomains; design bounded contexts.
5. Keep one coherent model, lifecycle, and owner inside each bounded context.
6. Choose context integration from collaboration, power, and model-protection needs.
7. Use value objects to replace conventions with types and behavior.
8. Treat aggregates as minimal strong-consistency boundaries, not object graphs.
9. Persist and publish domain events reliably; never confuse internal and integration contracts.
10. Use event sourcing only when the dimension of time creates material business value.
11. Make dependency direction protect complex domain logic from infrastructure.
12. Use CQRS for multiple persistent models, not as a universal command/query fashion.
13. Model cross-aggregate workflows with eventual consistency and explicit compensation.
14. Prefer deep services and safe boundaries to arbitrary microservice smallness.
15. Evolve classifications, models, boundaries, relationships, tactics, and tests as reality changes.
16. Modernize incrementally and direct effort toward the core.
17. Use EventStorming to share knowledge; do not confuse its artifact with the outcome.
18. Replace “aggregates everywhere” with “ubiquitous language everywhere.”

## Cross-References
- Related: [[../Domain_Driven_Design_with_Golang.md]]
- Related: [[../Building_Event-driven_Microservices.md]]
- Related: [[../Monolith_To_Microservices.md]]
- Related: [[../Fundamentals_of_Software_Architecture.md]]
- Topic index: [[../INDEX.md]]
