# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Learning Domain-Driven Design
**Author:** Vlad Khononov (O'Reilly, 2021)
**Topic tags:** `#architecture` `#ddd` `#domain-driven-design`
**Language focus:** Language-agnostic; code samples in C# / .NET (applies equally to Go, Java, Kotlin, Scala, TypeScript)
**Sources:** `markdown_output/Learning Domain-Driven Design/Learning Domain-Driven Design.md` · `summaries/Learning_Domain-Driven_Design_Vlad_Khononov.md` · `summaries/Learning_Domain-driven_design.md`

## TL;DR
DDD is the methodology for aligning software design with business strategy. The strategic phase (subdomains, ubiquitous language, bounded contexts, context mapping) decides *where* the model boundaries go; the tactical phase (value objects, entities, aggregates, domain events, repositories) decides *how* to express those boundaries in code; the architectural patterns (layered, ports/adapters, CQRS) decide *how the dependency arrows point*. Pick the lightest tactical pattern that fits the subdomain's complexity. The book formalizes one decision tree from these axes.

---

## Best Practices by Topic

### Subdomain Classification — The Strategic Lever

**Principle:** Three subdomain types align engineering investment with business value. Core subdomains = competitive advantage (build in-house, skilled engineers, sophisticated patterns). Supporting subdomains = necessary but not differentiating (build simply, possibly outsource). Generic subdomains = solved everywhere (buy / adopt off-the-shelf).

**Do:**
- Classify every subdomain into Core / Supporting / Generic before choosing an implementation pattern. Investment follows classification.
- Treat Core subdomains as the company's "reason for being" — concentrate skilled engineers, deep modeling, sophisticated patterns, language-and-tooling flexibility.
- Treat Generic subdomains as candidates for buying/subscribing (Stripe for payments, Auth0 for auth, Stripe for billing). Build only when no adequate off-the-shelf solution exists.
- Treat Supporting subdomains as candidates for outsourcing or in-house with lighter patterns (Transaction Script, Active Record) — they shouldn't absorb senior engineers.
- Distill subdomains aggressively for Core, loosely for Supporting/Generic — finer-grained Core boundaries let you focus modeling investment.
- Recognize that the same real-world function can change classification over time (email: Generic → Core for a privacy-focused CRM).
- Use organizational departments and Conway's Law as starting heuristics, then refine using "coherent use cases involving the same actor, business entities, and closely related data."

**Don't:**
- Don't apply the Domain Model pattern to Generic subdomains — over-engineering.
- Don't outsource or transaction-script a Core subdomain — under-engineering.
- Don't assume subdomain classification is stable — a once-differentiating function can become generic (example: once Stripe commoditized payments, custom payment processing became a generic subdomain).
- Don't treat an early labeling as permanent; revisit periodically as the business evolves.

*Ref: Learning Domain-Driven Design.md — "Analyzing Business Domains", "What Is a Subdomain?", "Types of Subdomains", "Comparing Subdomains", "Identifying Subdomain Boundaries", "Domain Analysis Examples"*

---

### Ubiquitous Language

**Principle:** A single, rigorous, ubiquitous language shared by domain experts *and* developers — used everywhere: in conversations, code, tests, documentation. Each term has *one* agreed-upon meaning. The language is rooted in the business, not technology.

**Do:**
- Build the language through close work with domain experts (the people who identified the business problem, not analysts or engineers).
- Use the experts' actual terms — if experts say "subscription plan," code uses `SubscriptionPlan` (not `ProductTier`, not `ServiceLevel`).
- Capture the language with glossaries (for nouns) and use cases / Gherkin tests (for behavior and business rules).
- Reject synonyms — `user`, `visitor`, `administrator`, `account` are distinct concepts with different behaviors.
- Resolve ambiguous terms by introducing new vocabulary — "policy" meaning both regulatory rule and insurance contract requires two distinct names.
- Treat the language as continuously validated and evolved as understanding deepens.
- Reject technical jargon in domain discussions — "HTML iframe" and "database records" don't belong; "creative materials" and "campaign placements" do.

**Don't:**
- Don't use different terms in code vs conversation — drift erodes the language.
- Don't invent terms the domain experts don't use — the language is theirs, not ours.
- Don't accept silent synonymy — surface it explicitly.

*Ref: Learning Domain-Driven Design.md — "What Is a Ubiquitous Language?", "Language of the Business", "Model of the Business Domain", "Knowledge Discovery"*

---

### Bounded Contexts

**Principle:** A bounded context is the explicit boundary within which a particular domain model and ubiquitous language apply consistently. Inside: one model, one language. Outside: a different model, a different language. The bounded context is DDD's primary tool for managing complexity.

**Do:**
- Start with subdomains as candidate boundaries; refine based on where the ubiquitous language becomes inconsistent.
- Align bounded contexts with both physical boundaries (separate services / modules / codebases) and ownership boundaries (one team per context).
- Prefer one bounded context per subdomain; accept wider contexts only when domain knowledge is uncertain — decompose as the model matures.
- Recognize that subdomains (problem space) and bounded contexts (solution space) are different concepts — but map 1:1 in mature systems.
- Treat each bounded context as its own deployable microservice in microservices architectures.
- Document every bounded context in a context map with its integration pattern.

**Don't:**
- Don't treat bounded contexts as global — every developer in your org doesn't speak one unified language; they speak within contexts.
- Don't expect subdomains and bounded contexts to align from day one — start loose, decompose as you learn.

*Ref: Learning Domain-Driven Design.md — "Managing Domain Complexity", "Inconsistent Models", "What Is a Bounded Context?", "Bounded Contexts Versus Subdomains", "Boundaries"*

---

### Context Mapping & Bounded Context Integration

**Principle:** Bounded contexts interact through well-defined patterns. Pick the pattern that matches the *power dynamic* between teams and the *strategic importance* of the relationship.

**Do:**
- **Partnership** — when two teams evolve in lockstep. Best for tight collaboration; ad hoc coordination works.
- **Shared Kernel** — extract a co-owned subset of the model. Reduces duplication but creates shared coupling.
- **Customer-Supplier**:
  - **Conformist** — downstream adopts the upstream model verbatim. Use when downstream has no leverage.
  - **Anticorruption Layer (ACL)** — downstream translates the upstream model to protect its own model integrity. *Essential for Core subdomains.*
- **Open-Host Service (OHS)** — upstream publishes an integration-optimized published language separate from the internal implementation. Equivalent to Facade pattern.
- **Separate Ways** — duplicate the functionality when integration costs outweigh benefits. Never for Core subdomains.
- Document the chosen pattern in a **Context Map** — shows contexts, relationships, dependency direction, translation points.
- Establish team ownership for every bounded context and its integration pattern.

**Don't:**
- Don't couple downstream Core subdomains directly to upstream models without an ACL — model integrity is a Core asset.
- Don't maintain one-off integrations (every consumer different) — use OHS with a published language.
- Don't choose Separate Ways for a Core subdomain — losing competitive advantage to avoid integration cost is a bad trade.

*Ref: Learning Domain-Driven Design.md — "Integrating Bounded Contexts", "Cooperation Patterns", "Customer-Supplier Patterns", "Open-Host Service", "Separate Ways", "Context Map"*

---

### Tactical Patterns: Business Logic Implementation

**Principle:** Match implementation pattern to subdomain complexity. Three options:
- **Transaction Script** — procedure per use case. Use for *Generic* and simple *Supporting* subdomains.
- **Active Record** — objects that wrap database access and add light domain logic. Use for simple business logic with complex data structures.
- **Domain Model** — rich objects with behavior and data. Use for *Core* subdomains with complex business rules / invariants / state transitions.
- **Event-Sourced Domain Model** — store events, derive state. Use for Core subdomains with temporal aspects, audit requirements, or deep historical insight.

**Do:**
- Be pragmatic — not every part of the system needs a rich domain model.
- Recognize Active Record as valid for simple business logic (Khononov avoids "anemic domain model" framing — it's the right tool for the right job).
- Use Domain Model only where the complexity justifies the investment.
- Migrate patterns as complexity grows: Transaction Script → Active Record → Domain Model → Event-Sourced Domain Model.

**Don't:**
- Don't apply Domain Model to Generic subdomains — over-engineering hurts velocity.
- Don't apply Transaction Script to Core subdomains — under-engineering loses competitive advantage.
- Don't confuse "simple data, complex logic" (Transaction Script) with "complex data, simple logic" (Active Record) — the patterns target different cases.

*Ref: Learning Domain-Driven Design.md — "Implementing Simple Business Logic", "Transaction Script", "Active Record", "Be Pragmatic", "Tackling Complex Business Logic", "Domain Model", "Modeling the Dimension of Time", "Event Sourcing", "Event-Sourced Domain Model"*

---

### Value Objects

**Principle:** Objects identified solely by their attribute values. They are immutable; a change produces a new instance. Eliminate primitive obsession — represent domain concepts as rich types that encapsulate validation and behavior.

**Do:**
- Default to value objects whenever possible. Start with everything as a value object, upgrade to entity only when you must.
- Make value objects **immutable** — a "mutation" returns a new instance, leaving the original untouched.
- Implement value-based equality (`Equals`, `==`, `GetHashCode`) — two VOs with the same values must compare equal.
- Use value objects especially for entity properties (names, email, phone, money, status, country code, ID).
- Represent **money** as a value object — primitive `decimal`/`float` types lead to rounding/precision bugs.
- Centralize validation and business logic in the value object's constructor and factory methods.
- Allow conversion methods (metric→imperial, parsed string→structured) that return new VOs.
- Use VOs for thread safety — no shared mutable state.

**Don't:**
- Don't add IDs to value objects — two RGB values are equal regardless of identity.
- Don't allow mutation — `MixWith` must return a new `Color`, not modify `this`.
- Don't use raw strings/ints where the language supports rich types — replace every country code, phone number, email with a value object.

**Code: C# value object**
```csharp
public class Color
{
    public readonly byte Red;
    public readonly byte Green;
    public readonly byte Blue;
    public Color(byte r, byte g, byte b) { this.Red = r; this.Green = g; this.Blue = b; }
    public Color MixWith(Color other) =>
        new Color(
            r: (byte) Math.Min(this.Red + other.Red, 255),
            g: (byte) Math.Min(this.Green + other.Green, 255),
            b: (byte) Math.Min(this.Blue + other.Blue, 255)
        );
    public override bool Equals(object obj) {
        var other = obj as Color;
        return other != null &&
            this.Red == other.Red &&
            this.Green == other.Green &&
            this.Blue == other.Blue;
    }
    public static bool operator ==(Color lhs, Color rhs) {
        if (Object.ReferenceEquals(lhs, null))
            return Object.ReferenceEquals(rhs, null);
        return lhs.Equals(rhs);
    }
    public static bool operator !=(Color lhs, Color rhs) => !(lhs == rhs);
    public override int GetHashCode() => ToString().GetHashCode();
}
```
*Ref: Learning Domain-Driven Design.md — "Value object", "Implementation", "When to use value objects"*

---

### Entities

**Principle:** Objects defined by an explicit, stable identity that persists across attribute changes. Entities are mutable — they evolve over time. Entities only exist as part of an aggregate.

**Do:**
- Use entities when the same attributes can belong to different instances of the thing (two people with identical names).
- Choose ID type appropriate to domain (UUID, GUID, social-security number, business-specific key) — make ID immutable for the entity's lifecycle.
- Distinguish "entity ID" (immutable) from "entity attributes" (mutable).
- Treat attributes as private; expose commands (behavior), not setters.
- Treat entities as *aggregate members* — entities never stand alone.

**Don't:**
- Don't use entities where a value object suffices — defaulting to "entity with ID" is over-modeling.
- Don't expose getters/setters for every field (anemic entity) — expose commands that enforce invariants.
- Don't choose a mutable identifier (e.g., email) for a user entity — emails change; IDs shouldn't.

*Ref: Learning Domain-Driven Design.md — "Entities"*

---

### Aggregates — The Consistency Boundary

**Principle:** A consistency enforcement boundary — a hierarchy of entities and value objects sharing one transactional boundary. One aggregate per database transaction. The aggregate root is the only entry point. Reference other aggregates by ID, not object reference.

**Do:**
- Treat aggregates as the consistency unit: all changes to the aggregate's data must succeed or fail together.
- Make the aggregate root the *only* entry to mutate state — all external callers go through its public commands.
- Implement state changes as methods (commands) that validate input and enforce business rules/invariants.
- Keep aggregates **as small as possible** — include only data that *must* be strongly consistent for the aggregate's business logic.
- Use one aggregate per database transaction. The need to commit multiple aggregates is a *symptom of wrong aggregate boundaries*.
- Reference other aggregates **by ID** — not by object reference — to enforce independent consistency boundaries.
- Pick an aggregate root — only one entity in the hierarchy exposes the public interface.
- Implement optimistic concurrency control via a `_version` field and `WHERE agg_version = @expected_version` style updates.
- Publish domain events from the aggregate when commands cross aggregate boundaries.
- Express aggregate names, members, actions, and events in the ubiquitous language.

**Don't:**
- Don't allow direct mutation of aggregate internals from outside — even read access for state mutation is a violation.
- Don't commit multiple aggregates in one transaction — that breaks the "one aggregate per transaction" rule and re-opens distributed transaction problems.
- Don't include business logic in entities that would be safe under eventual consistency — that's a signal to extract a new aggregate.
- Don't load aggregate-by-ID, modify, persist without a version check — concurrent modifications lose data without OCC.
- Don't add a marketing-opt-in checkbox to the Order aggregate — it isn't strongly consistent with order state; extract to its own aggregate.

**Code: C# aggregate root with commands and version**
```csharp
public class Ticket {
    TicketId _id;
    int _version;
    List<Message> _messages;
    // ...

    public void Execute(AddMessage cmd) {
        var message = new Message(cmd.from, cmd.body);
        _messages.Append(message);
    }

    public void Execute(AcknowledgeMessage cmd) {
        var message = _messages.Where(x => x.Id == cmd.id).First();
        message.WasRead = true;
    }

    public void Execute(RequestEscalation cmd) {
        if (!this.IsEscalated && this.RemainingTimePercentage <= 0) {
            this.IsEscalated = true;
            var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
            _domainEvents.Append(escalatedEvent);
        }
    }
}
```
**Application layer orchestrates atomic load → execute → save:**
```csharp
public ExecutionResult Escalate(TicketId id, EscalationReason reason) {
    try {
        var ticket = _ticketRepository.Load(id);
        var cmd = new Escalate(reason);
        ticket.Execute(cmd);
        _ticketRepository.Save(ticket);
        return ExecutionResult.Success();
    } catch (ConcurrencyException ex) {
        return ExecutionResult.Error(ex);
    }
}
```
**Optimistic concurrency SQL:**
```sql
UPDATE tickets
SET ticket_status = @new_status,
    agg_version = agg_version + 1
WHERE ticket_id = @id and agg_version = @expected_version;
```
*Ref: Learning Domain-Driven Design.md — "Aggregates", "Consistency enforcement", "Transaction boundary", "Hierarchy of entities", "Referencing other aggregates", "The aggregate root", "Domain events", "Ubiquitous language"*

---

### Domain Events

**Principle:** Past-tense messages describing significant business events. Part of an aggregate's public interface. Enable loose coupling across aggregates and bounded contexts.

**Do:**
- Name domain events in past tense — `TicketEscalated`, `TicketAssigned`, `MessageReceived`, `CampaignDeactivated`.
- Include all data needed by subscribers in the event payload (so subscribers don't need to query back).
- Emit events from the aggregate — collect during command execution; publish via the application layer / outbox after the aggregate is persisted.
- Use domain events to coordinate eventual consistency between aggregates / bounded contexts.

**Don't:**
- Don't emit events whose names describe commands or capabilities (`SendEmail`, `ProcessOrder`) — events describe things that *have happened*.
- Don't publish events from the aggregate directly to a message bus — leaks infrastructure into domain.
- Don't publish events before the aggregate's state is committed (race condition + subscriber reads inconsistent state).

**Code: C# escalation event with payload**
```csharp
public class Ticket {
    private List<DomainEvent> _domainEvents;
    public void Execute(RequestEscalation cmd) {
        if (!this.IsEscalated && this.RemainingTimePercentage <= 0) {
            this.IsEscalated = true;
            var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
            _domainEvents.Append(escalatedEvent);
        }
    }
}
// Event payload:
{
    "ticket-id": "c9d286ff-3bca-4f57-94d4-4d4e490867d1",
    "event-id": 146,
    "event-type": "ticket-escalated",
    "escalation-reason": "missed-sla",
    "escalation-time": 1628970815
}
```
*Ref: Learning Domain-Driven Design.md — "Domain events"*

---

### Domain Services

**Principle:** Stateless object implementing business logic that doesn't naturally belong to any aggregate or value object — typically orchestrating across multiple sources. Domain services respect the one-aggregate-per-transaction rule (orchestrate reads across aggregates; only modify one aggregate per transaction).

**Do:**
- Use for business logic that operates on multiple aggregates / external sources (e.g., `ResponseTimeFrameCalculationService` reads ticket data + department policy + shift schedule).
- Formulate names in the ubiquitous language.
- Treat as stateless: no internal state beyond injected repositories/clients.
- Use when you find business logic that needs to be implemented outside the aggregate but in the domain layer.

**Don't:**
- Don't put non-business logic ("CRUD orchestration") in a domain service — that's the application service.
- Don't use domain services to skirt the "one aggregate per transaction" rule — they read across, write to one.

**Code: C# domain service reading across sources (read-only):**
```csharp
public class ResponseTimeFrameCalculationService {
    public ResponseTimeframe CalculateAgentResponseDeadline(UserId agentId,
        Priority priority, bool escalated, DateTime startTime) {
        var policy = _departmentRepository.GetDepartmentPolicy(agentId);
        var maxProcTime = policy.GetMaxResponseTimeFor(priority);
        if (escalated) {
            maxProcTime = maxProcTime * policy.EscalationFactor;
        }
        var shifts = _departmentRepository.GetUpcomingShifts(agentId,
            startTime, startTime.Add(policy.MaxAgentResponseTime));
        return CalculateTargetTime(maxProcTime, shifts);
    }
}
```
*Ref: Learning Domain-Driven Design.md — "Domain services"*

---

### Architectural Patterns

**Principle:** Three layers, three dependency rules. Pick the architecture by the business logic pattern in use:

- **Layered Architecture** (Presentation / Business Logic / Data Access) — top-down dependencies. Use for Transaction Script and Active Record.
- **Ports & Adapters / Hexagonal** — business logic defines *ports* (interfaces), infrastructure provides *adapters* (implementations). Use with Domain Model and Event-Sourced Domain Model. The Dependency Inversion Principle inverts the dependency arrow.
- **CQRS** — Command side (write model, enforces business rules, often event-sourced) and Query side (read models, denormalized projections optimized for queries). Use when read/write workloads diverge significantly.

**Do:**
- Match architectural pattern to business logic pattern: Transaction Script → Layered, Domain Model → Ports & Adapters, Event-Sourced → Ports & Adapters + CQRS.
- Apply architectural patterns at the *module* level, not system-wide — different subdomains can use different patterns.
- Plan CQRS read-model projection strategies — synchronous (catch-up subscription with checkpoints) or asynchronous (via message bus).
- Allow commands to return data (success/failure and strongly consistent state) — they must report success/failure and may return strongly consistent state to the caller.

**Don't:**
- Don't combine all three architectures into a single mess — pick one per module.
- Don't treat CQRS as DDD-mandatory — it's a powerful but specialized tool, not always justified.
- Don't claim CQRS isn't DDD — CQRS is about *separating* command and query *responsibilities*; commands can still return data.

*Ref: Learning Domain-Driven Design.md — "Architectural Patterns", "Layered Architecture", "Ports & Adapters", "CQRS"*

---

### Communication Patterns (Cross-Bounded Context)

**Principle:** Use model translation (stateless or stateful) at integration boundaries, the outbox pattern for reliable event publishing, sagas for linear multi-step processes, and process managers for branched workflows.

**Do:**
- **Stateless model translation** — implement the proxy pattern via embedded code, API gateway, or message proxy for async.
- **Stateful model translation** — when the translation requires aggregation or unifying multiple sources (e.g., backend-for-frontend pattern).
- **Open-host vs Anticorruption** — same translation logic, different ends: OHS protects downstream models from upstream internal changes; ACL protects downstream models from upstream *contract* changes.
- **Expose private and public events distinctly**: keep internal domain events private; expose integration events via published language.
- **Use the Outbox Pattern** for reliable event publication:
  1. Commit aggregate state and events in one atomic transaction.
  2. A message relay fetches unpublished events.
  3. Relay publishes to message bus; on success marks as published (or deletes).
- **Use the Saga Pattern** for simple linear multi-aggregate processes. Each step emits an event; saga emits a next command; on failure, saga emits compensating events.
- **Use the Process Manager Pattern** for branched workflows — if a saga needs `if/else` for the next step, it's a process manager. Process managers have explicit instantiation and persistent state; sagas match events to commands.
- For NoSQL without multi-document transactions, embed the outbox inside the aggregate document:
  ```json
  {
    "campaign-id": "364b33c3-2171-446d-b652-8e5a7b2be1af",
    "state": { "name": "Autumn 2017", "publishing-state": "DEACTIVATED", ... },
    "outbox": [
      { "campaign-id": "...", "type": "campaign-deactivated", "reason": "Goals met", "published": false }
    ]
  }
  ```
- Place state-changing logic and command dispatch in separate steps — never publish a domain event from inside an aggregate; never commit then publish without the outbox.
- Use polling publisher or transaction log tailing (push) for the relay.

**Don't:**
- Don't publish domain events from inside the aggregate — `event.Publish()` leaks infrastructure into the domain layer and risks publishing before state is committed.
- Don't commit state and then publish — a crash between the two leaves inconsistent state. Use the outbox.
- Don't use a saga to compensate for improper aggregate boundaries — sagas give *eventual* consistency, not strong consistency.
- Don't use a saga when you need branching stateful logic — that's a process manager.
- Don't couple downstream subscribers to producer's internal domain events — translate to published language via ACL/OHS.

**Code: Saga reacting to events**
```csharp
public class CampaignPublishingSaga {
    private readonly ICampaignRepository _repository;
    private readonly IPublishingServiceClient _publishingService;
    public void Process(CampaignActivated @event) {
        var campaign = _repository.Load(@event.CampaignId);
        var advertisingMaterials = campaign.GenerateAdvertisingMaterials();
        _publishingService.SubmitAdvertisement(@event.CampaignId, advertisingMaterials);
    }
    public void Process(PublishingConfirmed @event) {
        var campaign = _repository.Load(@event.CampaignId);
        campaign.TrackPublishingConfirmation(@event.ConfirmationId);
        _repository.CommitChanges(campaign);
    }
    public void Process(PublishingRejected @event) {
        var campaign = _repository.Load(@event.CampaignId);
        campaign.TrackPublishingRejection(@event.RejectionReason);
        _repository.CommitChanges(campaign);
    }
}
```
*Ref: Learning Domain-Driven Design.md — "Communication Patterns", "Model Translation", "Stateless Model Translation", "Stateful Model Translation", "Integrating Aggregates", "Outbox", "Saga", "Process Manager", "Conclusion"*

---

### Decision Tree: Picking the Right Pattern by Subdomain

**Principle:** A simple decision tree maps subdomain type to business-logic pattern to architectural pattern to testing strategy:

| Subdomain | Business Logic | Architecture | Testing |
|-----------|----------------|--------------|---------|
| Core | Domain Model / Event-Sourced Domain Model | Ports & Adapters (+ CQRS for ES) | Testing Diamond (or Reversed Pyramid for ES) |
| Supporting | Transaction Script / Active Record | Layered | Testing Pyramid |
| Generic | Transaction Script or off-the-shelf | Layered (or buy) | Testing Pyramid |

**Do:**
- Apply the decision tree *at the module level* — different subdomains in the same system can use different patterns.
- Choose testing depth by complexity — Core subdomains with domain models need integration tests (Diamond); simple subdomains need unit-test heavy pyramids.
- Use Event-Sourced Domain Model when temporal aspects, audit requirements, or historical analysis are central.
- Plan for evolution — patterns migrate as complexity grows.

*Ref: Learning Domain-Driven Design.md — "Design Heuristics", "Bounded Contexts Heuristics", "Business Logic Implementation Patterns", "Architectural Patterns Decision Framework", "Testing Strategy"*

---

### Evolving Design Decisions

**Principle:** DDD is not a one-time exercise — design decisions evolve. Subdomain classifications migrate; tactical patterns migrate; integration patterns shift with team changes.

**Do:**
- Migrate tactical patterns as complexity grows: Transaction Script → Active Record → Domain Model → Event-Sourced Domain Model.
- Migrate tactical patterns *retrospectively*: "Active Record → Domain Model" = make all setters private, push logic into the object, identify aggregate boundaries. "Domain Model → Event-Sourced" = model events for all state transitions, generate approximate past events or migration events.
- Migrate context relationships as teams change: Partnership (close teams) → Customer-Supplier (geographically distant) → Separate Ways (integration costs exceed duplication).
- Continually revisit subdomain classifications: previously Core can become Generic (custom auth → buy Auth0); Generic can become Core (privacy becomes differentiator).
- Anticipate "big ball of mud" — let it grow by revisiting boundaries; eliminate accidental complexity.

**Don't:**
- Don't redesign for the future — let patterns evolve as complexity actually emerges.
- Don't apply Tactical Modernization without identifying subdomains first — refactor toward the Core, accept Generic off-the-shelf.

*Ref: Learning Domain-Driven Design.md — "Evolving Design Decisions", "Changes in Domains", "Tactical Design Concerns", "Organizational Changes", "Growth"*

---

### EventStorming

**Principle:** A collaborative, visual, low-tech workshop that brings domain experts and engineers together to explore a business process on a wall of sticky notes. The value is in the *process* — building shared mental models — not in the artifact.

**Do:**
- Use a large wall of butcher paper, sticky notes of multiple colors, markers, no chairs, snacks. Ideal group: up to 10 mixed roles.
- Follow the 10 steps:
  1. Brainstorm domain events (orange, past tense).
  2. Order events on a timeline (happy path first).
  3. Mark pain points (pink diamonds).
  4. Identify pivotal events (potential context boundaries).
  5. Add commands that trigger events (light blue).
  6. Add policies (purple) — automated reactions connecting events to commands.
  7. Add read models (green) — data views needed for decisions.
  8. Add external systems (pink).
  9. Group events/commands into aggregates (large yellow notes).
  10. Group aggregates into bounded context candidates.
- Capture the *language* used by domain experts — it becomes your ubiquitous language baseline.

**Don't:**
- Don't skip participants — EventStorming's value is the conversation, not the artifact.
- Don't let non-experts dominate — balance business and engineering roles.

*Ref: Learning Domain-Driven Design.md — "EventStorming", "What Is EventStorming?", "The EventStorming Process", "Who Should Participate in EventStorming?"*

---

## Anti-Patterns & Common Mistakes

- **Anemic domain model**: entities as data bags with setters — *fix:* push behavior into the entity; expose commands, not setters.
- **One aggregate per table in relational DB**: aggregates can span tables; tie aggregate boundaries to business invariants, not schema.
- **Multi-aggregate transactions**: directly violates the "one aggregate per transaction" rule — *fix:* extract a new aggregate, accept eventual consistency across them.
- **Exposing database IDs to consumers via shared model**: leaks persistence into domain — *fix:* identify by domain IDs (value objects).
- **Coupling downstream Core to upstream model**: contaminates the most valuable subdomain — *fix:* build an Anticorruption Layer.
- **Publishing domain events from inside the aggregate**: leaks infrastructure into domain; can publish before commit — *fix:* collect events, publish via outbox / application layer after successful commit.
- **Over-engineering Generic subdomains with Domain Model**: slows delivery without value — *fix:* use Transaction Script or buy/subscribe.
- **Under-engineering Core subdomains with Transaction Script**: destroys competitive advantage — *fix:* invest in Domain Model.
- **Synchronous saga / distributed transaction across aggregates**: reintroduces the two-phase-commit problem at the application layer — *fix:* use saga / outbox, accept eventual consistency.
- **Identifying bounded contexts with a single team / single tech stack**: DDD contexts are about language models; tech choices follow later.
- **Modeling Money as float**: rounding errors and precision bugs — *fix:* dedicated Money value object.
- **Adding a timestamp OR row ID to a value object**: defeats purpose — equality is value-based.
- **Stating "we use DDD" then treating all code as CRUD**: DDD is strategy + tactics, not just terminology.
- **Maintaining different terms in code vs. conversations**: language drift destroys the whole point.
- **Talking only about technical concerns in code review**: review for language alignment, not just syntactics.

## Decision Heuristics / Checklists

- **Subdomain type unknown?** Start with organizational departments as a coarse-grained first cut; refine via conversations.
- **Aggregates too large?** Check: does every field need strong consistency with every other? If not, extract.
- **Should this be an Entity or Value Object?** Default to value object; upgrade only when identity matters across attribute changes.
- **Transaction Script or Active Record or Domain Model?**
  - Simple business logic, simple data → Transaction Script.
  - Simple business logic, complex data structures → Active Record.
  - Complex business rules / state transitions → Domain Model.
  - Temporal aspects / audit / projection needs → Event-Sourced Domain Model.
- **Where to keep domain events?** Aggregate appends during command; application layer persists via outbox.
- **Which context integration pattern?**
  - Joint evolution + close teams → Partnership.
  - Overlap of model that both teams value → Shared Kernel.
  - Downstream has no leverage → Conformist (or push for ACL if Core).
  - Downstream is Core → Anticorruption Layer.
  - Multiple consumers needing different views → Open-Host Service with published language.
  - Integration costs > duplication → Separate Ways (never for Core).
- **Saga or Process Manager?** `if/else` for next-step routing → Process Manager. Linear event→command → Saga.

## Key Takeaways

1. **DDD = strategic *and* tactical.** Strategic phase (subdomains, bounded contexts) is more impactful than tactical (entities, aggregates).
2. **Subdomain type drives everything.** Core → Domain Model + Ports & Adapters. Supporting/Generic → simpler patterns or buy.
3. **Bounded contexts manage complexity through boundaries.** Each has its own language and model; inconsistencies across contexts are correct, not bugs.
4. **The Ubiquitous Language is the foundation.** Shared, rigorous, ubiquitous, evolving.
5. **Aggregates are consistency boundaries.** One aggregate per transaction; keep them small; reference others by ID.
6. **Domain events enable loose coupling.** Past-tense names; published via outbox to guarantee at-least-once with idempotent consumers.
7. **Architecture serves the business logic pattern.** Transaction Script → Layered. Domain Model → Ports & Adapters. Event-Sourced → + CQRS.
8. **Patterns evolve.** Subdomain classifications migrate; tactical patterns grow in complexity; organizational relationships shift.
9. **EventStorming builds the language.** The conversation is the value; the artifact is by-product.
10. **Boundaries matter most.** Subdomain, model (bounded context), consistency (aggregate), ownership (team) — getting these right *and evolving them* is DDD.

## Cross-References
- Related: [[../Foundations_of_Scalable_Systems.md]] — DDD bounded contexts map cleanly to microservice boundaries.
- Related: [[../Domain_Driven_Design_with_Golang.md]] — DDD applied with concrete Go code for aggregates, repositories, ACL.
- Topic index: [[../INDEX.md]]
