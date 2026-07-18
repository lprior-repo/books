# Building Microservices (2nd Edition) — Sam Newman
**Author:** Sam Newman
**Topic tags:** `#architecture` `#api` `#testing` `#distributed-systems`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/Building Microservices 2nd edition/Building Microservices 2nd edition.md` · `summaries/Building_Microservices_2nd_edition.md`

## TL;DR
The definitive practitioner's guide to fine-grained service architectures. The single most important takeaway is **independent deployability** — everything else (service boundaries, communication style, data ownership, deployment topology, resilience patterns, team structure) follows from it. Microservices are an expensive, opinionated form of SOA; you earn the benefits only by paying the tax of disciplined information hiding, loose coupling, strong ownership, and operational maturity. Start with a well-structured monolith; migrate incrementally via the strangler fig; never attempt a big-bang rewrite.

---

## Best Practices by Topic

### When to Use Microservices (and When NOT To)

**Principle:** Microservices are an opinionated architectural style whose value is conditional on organizational maturity, domain stability, and clear goals. They are *not* a default.

**Do:**
- Have a clear goal for adopting microservices (delivery autonomy, scaling a hot path, organizational scale) before you start.
- Start with a monolith (single-process or modular) when the domain is still being discovered.
- Embrace the concept of microservices "buying you options" — you pay a tax now to keep architectural choices open later.
- Use microservices when you need many teams to ship independently without stepping on each other.
- Match the architecture to your stage: monolith → modular monolith → distributed monolith → microservices, in that order.
- Treat microservices as a dial you turn gradually, not a switch you flip.

**Don't:**
- Don't adopt microservices just because "everyone is doing it."
- Don't use microservices for new products / startups / brand-new domains where the model is still in flux — premature decomposition is more expensive than a temporary rewrite.
- Don't use microservices when you have fewer than ~5 developers; the "microservice tax" (deployment, monitoring, complexity) outweighs the benefit.
- Don't use microservices when you ship on-prem software to customers — they can't run your Kubernetes cluster.
- Don't view microservices as the goal. Faster delivery, organizational scale, or independent scaling are the goal; microservices are a means.

**Code:**
```text
"When you fall into the trap of systematically undermining the monolith
as a viable option for delivering our software, we're at risk of not
doing right by ourselves or by the users of our software."
```
*Ref: Building_Microservices.md — "Should I Use Microservices?" / "The Monolith"*

---

### Service Boundaries, Information Hiding, Cohesion

**Principle:** A good microservice boundary is one that maximizes information hiding and minimizes cross-boundary coupling while keeping related behavior together.

**Do:**
- Apply David Parnas's information hiding: hide as much as possible behind the boundary, expose as little as possible via the interface.
- Use cohesion: "the code that changes together, stays together" — group related behavior so a change touches one place.
- Hide your database behind the service boundary — internal state is implementation detail.
- Embrace Constantine's law: a structure is stable if cohesion is strong and coupling is low.
- Use bounded contexts as the default starting point for service boundaries; subdivide them later only when you see real benefit.
- Make the boundary a unit of information hiding so technology changes inside the boundary are invisible to consumers.

**Don't:**
- Don't split a domain by technical layer (UI team / backend team / DBA team) — that's a distributed monolith.
- Don't let size drive boundary decisions; "as big as your head" is the only useful heuristic.
- Don't let one aggregate be managed by multiple microservices — keep aggregate ownership inside one service.
- Don't make the boundary a place where behavior leaks out — if it's a thin CRUD wrapper over a shared table, it's a sign of weak cohesion.

**Code:**
```text
"We want our microservices to be able to be changed and deployed,
and their functionality released to our users, in an independent
fashion. The ability to change one microservice in isolation from
another is vital."
```
*Ref: Building_Microservices.md — "What Makes a Good Microservice Boundary?" / "Information Hiding" / "Cohesion"*

---

### Types of Coupling (Domain / Pass-Through / Common / Content)

**Principle:** Some coupling is unavoidable (domain coupling). All other coupling must be minimized. Worst-to-best: content → common → pass-through → domain.

**Do:**
- Allow domain coupling (Service A legitimately needs Service B's functionality) — minimize the number of distinct collaborators per consumer.
- Treat pass-through coupling (A → B → C where B doesn't need the data) as a refactoring smell: bypass B, or hide the downstream schema behind B's contract.
- Treat common coupling (multiple services sharing a database or config) as a strong smell: it makes schema changes cross-cutting.
- Treat content coupling (Service A reaches into Service B's internals via DB writes or internal APIs) as pathological and eliminate it immediately.

**Don't:**
- Don't pass data through a service "just in case" a downstream service might want it.
- Don't let upstream services know the internal schema of a downstream database.
- Don't have multiple services writing to the same row of the same table.
- Don't wrap a service around a CRUD database without internal logic — that's a content-coupling smell.

**Code:**
```text
"If you see a microservice that just looks like a thin wrapper
around database CRUD operations, that is a sign that you may have
weak cohesion and tighter coupling, as logic that should be in
that service to manage the data is instead spread elsewhere
in your system."
```
*Ref: Building_Microservices.md — "Types of Coupling" / "Domain Coupling" / "Pass-Through Coupling" / "Common Coupling" / "Content Coupling"*

---

### Bounded Contexts & Domain-Driven Design

**Principle:** DDD is the primary mechanism for finding sensible microservice boundaries; a bounded context maps naturally to a service.

**Do:**
- Start at the bounded-context level when picking service boundaries, then subdivide nested contexts only when you see clear benefit.
- Use a single ubiquitous language inside each bounded context — code, schema, conversation should all use the same terms.
- Pick an aggregate boundary that makes state transitions atomic and self-contained; one aggregate should be managed by one microservice (but one microservice may own many aggregates).
- Use event storming to surface domain events with cross-functional stakeholders; resist the urge to let implementation warp the model.
- Hide aggregate relationships behind explicit references (pseudo-URIs, REST links) rather than bare foreign-key IDs.

**Don't:**
- Don't try to map one business domain object to one microservice — the unit of decomposition is the bounded context or aggregate.
- Don't pretend a bounded context is internal; hidden models and shared models are different and should be named differently.
- Don't let organizational boundaries drive DDD — Conway's law works the other way too: design the architecture you want, then structure teams.
- Don't apply bimodal IT ("Systems of Record" vs "Systems of Innovation") — it becomes an excuse to never change the legacy stuff.

*Ref: Building_Microservices.md — "Just Enough Domain-Driven Design" / "Bounded Context" / "Mapping Aggregates and Bounded Contexts to Microservices" / "Event Storming" / "The Case for Domain-Driven Design for Microservices"*

---

### Alternative Decomposition Axes

**Principle:** DDD is the default, but volatility, data, technology, and organizational realities can each justify splitting boundaries differently.

**Do:**
- Use volatility-based decomposition when your driver is "ship faster" and parts of the system change frequently — extract the hot, changing parts first.
- Use data-based decomposition when the driver is regulatory/compliance (e.g., segregate PII into its own zone to limit PCI audit scope, as PaymentCo did).
- Use technology-based decomposition when a specific runtime or storage is fundamentally incompatible with the rest of the stack.
- Use organizational decomposition (Conway's law in reverse) when you need to align the architecture with team boundaries.
- Mix axes deliberately — document why each boundary was drawn the way it was.

**Don't:**
- Don't dogmatically stick to a single decomposition axis when the problem demands otherwise.
- Don't decompose by technology just because it's "interesting" — gratuitous tech variation is a tax.
- Don't draw a boundary that crosses team ownership lines; that boundary will fail under delivery contention.

*Ref: Building_Microservices.md — "Alternatives to Business Domain Boundaries" / "Volatility" / "Data" / "Technology" / "Organizational"*

---

### Splitting the Monolith (Migration)

**Principle:** Migrate incrementally, never via big-bang rewrite. Use the strangler fig; pick easy wins first; verify before expanding.

**Do:**
- Have a clear, written goal for the migration — what outcome justifies the cost?
- Migrate incrementally via the strangler fig: intercept calls at the edge, route new logic to a microservice, leave old logic in place.
- Run new and old implementations side-by-side (parallel run) and compare results before cutting over.
- Use feature toggles to switch between old and new implementations gradually.
- Pick the first few extractions from the "easy" end of the spectrum to build momentum.
- Reuse code first, then data — extract application code while data still lives in the monolith, then split the database after the code path is proven.
- Be skeptical of premature decomposition — premature microservices from an unstable domain cause expensive churn (Snap CI learned this the hard way).

**Don't:**
- Don't do a big-bang rewrite — "the only thing you're guaranteed of is a big bang" (Fowler).
- Don't migrate from an unstable domain — wait until the model stabilizes.
- Don't split data before you understand what extraction looks like; but don't ignore data decomposition entirely either.
- Don't rely on database joins as a fallback once data is split — replace them with cached lookups or aggregate the data client-side.
- Don't assume ACID transactions will survive the split — they won't.

**Code:**
```sql
-- BEFORE (monolith join)
SELECT l.sku, a.name, SUM(l.amount) AS total
FROM ledger l JOIN albums a ON l.sku = a.sku
WHERE l.sold_at > NOW() - INTERVAL '7 days'
GROUP BY l.sku, a.name ORDER BY total DESC LIMIT 10;

-- AFTER (cross-service): Finance service calls Catalog for each top SKU
SELECT sku, SUM(amount) AS total FROM ledger
 WHERE sold_at > NOW() - INTERVAL '7 days'
 GROUP BY sku ORDER BY total DESC LIMIT 10;
-- then per-SKU lookup against Catalog microservice (prefer batch + cache)
```
*Ref: Building_Microservices.md — "Have a Goal" / "Incremental Migration" / "The Dangers of Premature Decomposition" / "What to Split First?" / "Decomposition by Layer" / "Strangler Fig Pattern" / "Parallel Run" / "Feature Toggle" / "Data Decomposition Concerns"*

---

### Inter-Service Communication: Sync vs Async

**Principle:** Pick request-response when you need an immediate answer; pick event-driven when you want to decouple emitters from reactors. Pick the communication style first, then the technology. Both can (and should) coexist.

**Do:**
- Start with the question: do I need a request-response or an event-driven style? Then narrow to sync/async.
- Use synchronous blocking (REST/gRPC) when you need an immediate answer and the call chain is short.
- Switch to asynchronous nonblocking when work is long-running (hours/days) or the call chain is long.
- Use event-driven collaboration when the emitter doesn't know who (if anyone) cares — broadcasting a fact is the inversion of "tell someone to do something."
- Combine styles in one service: e.g., Order service exposes REST for placement, fires events when state changes.
- Prefer fully-managed brokers over running your own.

**Don't:**
- Don't reach for Kafka if all you need is request-response — Kafka is for event-based interactions.
- Don't make every interaction async — eventual consistency has a real cost, and so does managing messaging infrastructure.
- Don't use async/await as a substitute for nonblocking — `await` still blocks the calling thread (Example 4-1 in the book).
- Don't assume async request-response is straightforward — the response may arrive at a *different* instance of the upstream service, requiring shared state.

**Code:**
```javascript
// Example 4-1: Looks async but is still blocking
async function f() {
  let eurToGbp = new Promise((resolve, reject) => { /* ... */ });
  var latestRate = await eurToGbp;  // blocks here until promise resolves
  process(latestRate);                // doesn't run until then
}
```
*Ref: Building_Microservices.md — "Styles of Microservice Communication" / "Pattern: Synchronous Blocking" / "Pattern: Asynchronous Nonblocking" / "Pattern: Communication Through Common Data" / "Pattern: Request-Response Communication" / "Pattern: Event-Driven Communication" / "Async/Await and When Asynchronous Is Still Blocking"*

---

### Event-Driven Collaboration & Event Payload Design

**Principle:** Events are facts, not commands. The emitter has no idea who consumes them.

**Do:**
- Treat events as a broadcast of a fact about something that happened, with the data downstream consumers would need.
- Prefer fully-detailed events (everything you would share via API goes into the event) so consumers don't have to make a callback to the source.
- Use correlation IDs (saga IDs) on all events of a saga so you can reconstruct flow.
- Run multiple instances via consumer groups when multiple consumers should each see the event (Notifications + Inventory for Order Paid).
- Consider two event variants for PII vs non-PII if data sensitivity varies by consumer.

**Don't:**
- Don't pack events with "just an ID" — downstream consumers will pile up callback requests against your service.
- Don't treat events as commands — "an event is a fact, a message is the medium, the event is the payload."
- Don't make the event payload so big it becomes a PII exposure risk to a wider audience.
- Don't remove fields from an event without considering all downstream consumers — events are part of your public contract.

*Ref: Building_Microservices.md — "Pattern: Event-Driven Communication" / "Events and Messages" / "What's in an Event?" / "Just an ID" vs "Fully detailed events"*

---

### Message Brokers & Communication Infrastructure

**Principle:** Brokers give you guaranteed delivery, ordering (per partition), and durable buffering — but trust the broker's runtime model, manage cluster failure modes, and keep the middleware dumb.

**Do:**
- Use a queue for point-to-point (one consumer per message) and a topic for broadcast (multiple consumer groups each receive a copy).
- Ensure guaranteed delivery by configuring durable storage and cluster-based broker topology.
- Build consumers that are idempotent — duplicates are a fact of life, not a bug.
- Treat "exactly once delivery" claims with skepticism; design for "at-least-once + idempotent consumer."
- Trust Kafka for scale, replay, and stream processing; trust RabbitMQ/ActiveMQ for traditional request/response queuing.
- Set a maximum retry limit and a dead-letter queue (the book tells the cautionary tale of a pricing system that crashed in a loop without one).

**Don't:**
- Don't put smart logic in the middleware — "keep your middleware dumb, and keep the smarts in the endpoints."
- Don't share HTTP connection pools across downstream services — one slow service will starve the others.
- Don't trust any single broker configuration to "just work" — RabbitMQ requires low-latency inter-node links, Kafka ordering is per-partition only.
- Don't introduce a broker just for one use case — the operational overhead is significant.

*Ref: Building_Microservices.md — "Message Brokers" / "Topics and queues" / "Guaranteed delivery" / "Trust" / "Other characteristics" / "Proceed with Caution" (catastrophic failover tale)*

---

### API Design: REST, RPC, GraphQL

**Principle:** Whatever you pick, make the interface explicit, technology-agnostic, easy for consumers, and easy to evolve backward-compatibly.

**Do:**
- Use **REST over HTTP** as the sensible default for synchronous request-response — wide tooling, HTTP caching, ecosystem.
- Use **gRPC** when both ends are under your control and you need high-performance typed contracts.
- Use **GraphQL** when clients (esp. mobile) need to fetch varied subsets of fields without paying for over-fetch — and avoid it for writes.
- Use an explicit schema (OpenAPI for REST, proto for gRPC) — it makes contracts discoverable and reviewable.
- Hide internal implementation detail — clients should not be bound to your storage shape.
- Pick one or two interface styles org-wide; twenty is a nightmare.
- Define how you'll handle verbs vs nouns, pagination, and versioning.

**Don't:**
- Don't use Java RMI — binary stub regeneration creates lockstep client/server deployments.
- Don't promise that "REST = HTTP verbs are used correctly" — many "REST" APIs ignore HTTP semantics entirely.
- Don't put core business logic in client libraries — it leaks server behavior into clients and erodes cohesion.
- Don't rely on HATEOAS in practice — it sounds great, the industry hasn't adopted it, the book calls this out.
- Don't couple client libraries to specific server implementations — the AWS SDK pattern (community-written SDKs over stable web APIs) works better.
- Don't introduce GraphQL if a simple BFF or REST endpoint solves the same problem.

**Code:**
```protobuf
// Example 5-1 (problem): Java RMI binary stubs — adding a method requires
// regenerating stubs and redeploying both client and server in lockstep.
public interface CustomerRemote extends Remote {
  public Customer findCustomer(String id) throws RemoteException;
  public Customer createCustomer(String firstname, String surname,
                                  String emailAddress) throws RemoteException;
}
```
*Ref: Building_Microservices.md — "Looking for the Ideal Technology" / "Remote Procedure Calls" / "REST" / "GraphQL" / "Schemas"*

---

### Schema Discipline & Backward Compatibility

**Principle:** Without an explicit schema, you still have one — it's just implicit in your code. Make it explicit and check compatibility before deploy.

**Do:**
- Use explicit schemas for every endpoint (OpenAPI, JSON Schema, AsyncAPI, CloudEvents, proto, Avro).
- Use schema-comparison tooling that *fails* on incompatibility, integrated into CI (Protolock for proto, openapi-diff for OpenAPI, Confluent Schema Registry for Kafka).
- Pick schema technology that makes additive change easy (proto field numbers, JSON's tolerance for unknown fields).
- Distinguish **structural** breakage (caught by schema diff) from **semantic** breakage (caught by tests/CDCs).
- Have an explicit schema story for events too — CloudEvents / AsyncAPI.

**Don't:**
- Don't conflate "schemaless" with "no contract" — every consumer has implicit expectations about response shape.
- Don't remove or rename fields in a backward-incompatible way without coordinating consumers.
- Don't change the *semantics* of a field (e.g., add vs multiply) without treating it as breaking.
- Don't rely on "we'll just regenerate stubs" — it works against independent deployability.

*Ref: Building_Microservices.md — "Schemas" / "Should You Use Schemas?" / "Structural Versus Semantic Contract Breakages"*

---

### Avoiding Breaking Changes / Versioning

**Principle:** Make backward-compatible changes by default. When you must break, expand before you contract; never lockstep-deploy.

**Do:**
- Prefer expansion changes: add new fields/endpoints, never remove old ones.
- Be a **tolerant reader**: ignore fields you don't care about; allow unknown fields in payloads.
- Use semantic versioning (`MAJOR.MINOR.PATCH`) and mean it: `MINOR` = backward-compatible, `MAJOR` = breaking.
- Coexist old and new endpoints in the same running service (emulation / expand-and-contract) to give consumers time to migrate.
- For HTTP, support both URI versioning (`/v1/customer/`, `/v2/customer/`) and header versioning.
- Use tracking (User-Agent headers, API keys, client identifiers) so you know who is still on the old contract.

**Don't:**
- Don't lockstep-deploy a breaking change across many services — it violates independent deployability and turns one bad release into many.
- Don't leave the old endpoint lying around forever — track usage, give consumers a deadline, retire it.
- Don't break in a subtle way (e.g., flipping `add` to `multiply`) and call it "compatible."
- Don't underestimate the social side — agree with consumers in advance on the change process.

**Code:**
```xml
<!-- Example 5-3: Original payload -->
<customer>
  <firstname>Sam</firstname>
  <lastname>Newman</lastname>
  <email>sam@magpiebrain.com</email>
  <telephoneNumber>555-1234-5678</telephoneNumber>
</customer>

<!-- Example 5-4: Restructured but compatible — use XPath, don't bind tightly -->
<customer>
  <naming>
    <firstname>Sam</firstname>
    <lastname>Newman</lastname>
    <nickname>Magpiebrain</nickname>
    <fullname>Sam "Magpiebrain" Newman</fullname>
  </naming>
  <email>sam@magpiebrain.com</email>
</customer>
```
*Ref: Building_Microservices.md — "Avoiding Breaking Changes" / "Expansion Changes" / "Tolerant Reader" / "Semantic Versioning" / "Managing Breaking Changes" / "Lockstep Deployment" / "Coexist Incompatible Microservice Versions" / "Emulate the Old Interface"*

---

### DRY vs Code Reuse Across Microservices

**Principle:** Sharing code across service boundaries creates the coupling you're trying to avoid. Different versions of the same library across services are fine. Different *behavior* across services is what matters.

**Do:**
- Treat logging libraries, common utility code, etc. as safe to share — they're invisible to consumers.
- Copy a service template into each new service if it would otherwise couple services (realestate.com.au does this).
- Accept that multiple versions of the same library will exist in production.
- Use a shared binary dependency for service templates; treat the template as optional.
- If you must share runtime behavior across services, prefer a service mesh over a shared library.

**Don't:**
- Don't share domain objects across services — when one changes, every consumer breaks.
- Don't create a "shared everything library" that every microservice depends on — it's the gateway back to lockstep deployments.
- Don't make client libraries mandatory — it caps consumer technology choice and traps them on the server's release schedule.
- Don't extract an abstraction at two uses — wait for three (rule of thumb the book cites).

*Ref: Building_Microservices.md — "DRY and the Perils of Code Reuse in a Microservice World" / "Sharing Code via Libraries" / "Client libraries"*

---

### Service Discovery

**Principle:** Discovery is two problems: register, then find. Pick the simplest solution that survives disposability.

**Do:**
- Start with DNS — it's universally understood; let DNS point at a load balancer that fronts your instances.
- Use a TTL on DNS, and keep it low enough that you don't get stuck with stale IPs.
- Have the load balancer detect unhealthy instances and remove them automatically.
- Consider dynamic registries (Consul, etcd via Kubernetes) when instances are highly disposable.
- Tag instances with rich metadata (service, env, version) so humans and tooling can query them.

**Don't:**
- Don't use DNS round-robin pointing directly at hosts — clients can't take a sick host out of rotation.
- Don't build your own service discovery — the tooling is mature; reinventing the wheel just makes a worse wheel.
- Don't forget the human registry — a humane registry (wiki, Backstage, Biz Ops) is essential even with machine-readable discovery.
- Don't underestimate JVM DNS caching — you may need to override defaults.

*Ref: Building_Microservices.md — "Service Discovery" / "Domain Name System (DNS)" / "Dynamic Service Registries" / "Don't Forget the Humans!"*

---

### API Gateways vs Service Meshes

**Principle:** API gateways handle north-south (perimeter); service meshes handle east-west (inter-service). Keep the pipes dumb; push smarts to endpoints.

**Do:**
- Use an API gateway for external traffic, north-south only.
- Use a service mesh (Istio/Linkerd on Kubernetes) when you need mTLS, tracing, retries across many services written in different languages.
- Make any shared behavior in a proxy **totally generic** — no per-service logic in the gateway.
- Be very explicit about what you want from an API gateway; many vendor features are overkill.

**Don't:**
- Don't put call aggregation, filtering, or protocol rewriting in an API gateway — that's business logic in a pipe.
- Don't use an API gateway as the single hop between microservices — it doubles latency and creates contention.
- Don't treat the gateway as a single point of failure — defense in depth still applies.
- Don't bake business rules into a third-party gateway product — extraction later becomes a rewrite, not a refactor.

*Ref: Building_Microservices.md — "Service Meshes and API Gateways" / "API Gateways" / "Where to use them" / "What to avoid" / "Service Meshes" / "Aren't service meshes smart pipes?" / "Do you need one?"*

---

### Data Ownership & Database Per Service

**Principle:** Each service owns its data. Sharing a database across services is one of the worst things you can do for independent deployability.

**Do:**
- Give each microservice a private database (or at minimum a private schema) — implementation detail hidden from the world.
- Allow multiple instances of the *same* microservice to share a database — that's not a violation.
- Use data partitioning (sharding) only when a single instance can't handle the load.
- Replace cross-service joins with cache + lookup, batch lookup, or aggregate the data on the writer side.
- For reporting, build a dedicated reporting database owned by the source microservice, exposed as a service endpoint.

**Don't:**
- Don't expose your database directly to other services — that turns your schema into a public contract.
- Don't have multiple services reading and writing the same row — split ownership instead.
- Don't rely on database joins to bridge service boundaries — joins don't cross them.
- Don't use stored procedures or triggers that span services — same coupling problem.
- Don't co-locate production microservices on the same shared DB infrastructure without an isolation plan.

*Ref: Building_Microservices.md — "Owning Their Own State" / "The Database" / "Reporting Database"*

---

### Data Integrity, Joins & Transactions Across Services

**Principle:** You will lose referential integrity and ACID guarantees across service boundaries. Replace them with compensating patterns; don't paper over with 2PC.

**Do:**
- Use soft deletes on the "many" side of a former relationship so dangling references are obvious.
- Copy the data you need at write time (e.g., copy album name into ledger row) and reconcile changes asynchronously.
- Reorder workflow steps so that likely-to-fail steps come first (fewer rollbacks to design).
- Use the saga pattern instead of distributed transactions for cross-service processes.

**Don't:**
- Don't rely on foreign keys across service boundaries — the database can't enforce them.
- Don't rely on ACID transactions across services — you can't, and 2PC won't save you.
- Don't introduce distributed transactions for "convenience" — Pat Helland's lesson: "when flying an airplane that needs all of its engines to work, adding an engine reduces the availability."

*Ref: Building_Microservices.md — "Data Integrity" / "Transactions" / "Performance"*

---

### Distributed Transactions (Two-Phase Commit) — Avoid

**Principle:** Two-phase commit is not a fix for cross-service consistency — it's a new, worse problem.

**Do:**
- Recognize that 2PC loses isolation guarantees because the commit phase isn't atomic across participants.
- Recognize that 2PC effectively coordinates distributed locks, which scale terribly.
- Treat the "I lost 700 LOC writing a 2PC coordinator" anecdote as a cautionary tale.

**Don't:**
- Don't use distributed transactions across microservices — they don't deliver the guarantees you expect.
- Don't write your own distributed transaction coordinator — even Spanner required satellite atomic clocks and bespoke datacenters.
- Don't use 2PC to "regain ACID" — at best you get a strict subset; at worst you cascade failures across your system.

*Ref: Building_Microservices.md — "Distributed Transactions—Two-Phase Commits" / "Distributed Transactions—Just Say No" / "Database Distributed Transactions"*

---

### Sagas for Cross-Service Workflows

**Principle:** A saga is a sequence of local transactions, each with a compensating action. Model business processes explicitly. Mix orchestration and choreography by team ownership.

**Do:**
- Model every cross-service business process as a saga.
- Implement each step inside a local ACID transaction inside the owning service.
- Add a correlation ID to every event/call in the saga so you can reconstruct state.
- Reorder workflow steps so likely failures happen early (e.g., check credit before payment).
- Use **orchestrated** sagas (central coordinator) when one team owns the entire process — visibility is a huge win.
- Use **choreographed** sagas (events between services) when multiple teams are involved — looser coupling.
- For choreographed sagas, build a "saga state view" by consuming all events with the correlation ID.
- Write compensating transactions as *semantic* rollbacks — it's OK if you can't fully revert (e.g., send a follow-up email rather than unsending).

**Don't:**
- Don't expect ACID atomicity at the saga level — only at the individual transaction level.
- Don't use a saga to handle *technical* failures (timeouts, 500s) — sagas assume components are reliable; add circuit breakers/retries separately.
- Don't put all logic in the orchestrator — services should still own their own state machines; the orchestrator just sequences calls.
- Don't use a BPM tool that the team isn't comfortable with — if developers write it, let them use code.
- Don't mix fail-forward and fail-backward rules ad-hoc — explicitly decide per step.

*Ref: Building_Microservices.md — "Sagas" / "Saga Failure Modes" / "Backward recovery" / "Saga rollbacks" / "Reordering workflow steps to reduce rollbacks" / "Mixing fail-backward and fail-forward situations" / "Implementing Sagas" / "Orchestrated sagas" / "BPM Tools" / "Choreographed sagas" / "Tracing Calls" / "Should I use choreography or orchestration (or a mix)?" / "Sagas Versus Distributed Transactions"*

---

### Event Sourcing & CQRS

**Principle:** Event sourcing stores state as an append-only log of events; CQRS separates the read model from the write model. Both are powerful but expensive in cognitive load.

**Do:**
- Consider event sourcing when the audit/history of state changes is itself valuable.
- Pair CQRS with event sourcing when you genuinely need different read and write scaling.
- Treat CQRS as an internal implementation detail — consumers of the microservice shouldn't know.
- If you must use CQRS, push complexity into the *aggregate* boundary, not into each state transition (which drags you into saga territory unnecessarily).

**Don't:**
- Don't introduce CQRS just because you're read-constrained — a read replica may suffice with much less risk.
- Don't break an aggregate into per-state-transition functions — it pulls you into sagas without justification.
- Don't expect CQRS to "beat" CAP — every system trades consistency somewhere.

*Ref: Building_Microservices.md — "Implementing Sagas" sidebar, "CQRS and Event Sourcing"*

---

### Continuous Integration, Trunk-Based Development, Pipelines

**Principle:** Integrate daily. Fix broken builds immediately. Treat every commit as a release candidate.

**Do:**
- Check in to trunk at least daily — even short-lived feature branches delay integration and risk painful merges.
- Keep the build green as the #1 priority — broken builds block everyone.
- Use build pipelines: fast tests first, slow tests after, then deployment to production-like environments.
- Build your deployable artifact once, once only — the same artifact through every stage.
- Keep environment-specific config outside the artifact.
- Measure pipeline stages against both *fast feedback* and *production-likeness* — these forces trade off.

**Don't:**
- Don't keep the build broken — fix it immediately or block check-ins.
- Don't use long-lived feature branches — they delay integration and bloat PRs.
- Don't rebuild the artifact per environment — "build once, deploy everywhere."
- Don't skip tests because they take too long — the answer is a faster test suite, not fewer tests.

*Ref: Building_Microservices.md — "A Brief Introduction to Continuous Integration" / "Are You Really Doing CI?" / "Branching Models" / "Build Pipelines and Continuous Delivery" / "Continuous Delivery Versus Continuous Deployment" / "Artifact Creation" / "Trade-Offs and Environments"*

---

### Source Code Layout: Monorepo vs Multirepo

**Principle:** Multirepo (one repo per microservice) is the safer default; monorepo is OK for small organizations but creates organizational lock-in as you scale.

**Do:**
- Map each microservice to its own CI build pipeline, regardless of repo structure.
- Use a multirepo when your organization is past the "10–20 developer" sweet spot.
- Use CODEOWNERS / Perforce-equivalent controls if you go monorepo, to keep ownership boundaries clear.
- Keep your repository layout consistent and discoverable.

**Don't:**
- Don't make cross-service atomic commits the norm — it warps toward distributed monoliths.
- Don't treat "Google uses monorepo" as license to do the same without Google's tooling, scale, and investment.
- Don't centralize the build of all services into one artifact — it couples everything.
- Don't let the monorepo hide ownership lines — code ownership needs to remain explicit.

*Ref: Building_Microservices.md — "Mapping Source Code and Builds to Microservices" / "One Giant Repo, One Giant Build" / "Pattern: One Repository per Microservice (aka Multirepo)" / "Pattern: Monorepo" / "Which Approach Would I Use?"*

---

### Deployment Principles & Infrastructure as Code

**Principle:** Isolate each microservice execution. Automate everything. Treat infrastructure as code. Aim for zero-downtime deploys and desired-state management.

**Do:**
- Run one service per host/container/VM — sharing hosts undermines isolation and independent deployability.
- Aim for zero-downtime deployment (rolling updates, blue/green) so you can ship during business hours.
- Use desired state management (Kubernetes, AWS autoscaling groups) to recover from instance death automatically.
- Use infrastructure as code (Terraform, Pulumi) — version control everything, make it reproducible.
- Keep deployment topology varying per environment through configuration, not through different artifacts.
- Offload work to public cloud / FaaS whenever it makes economic sense — don't "tinker with every last setting."
- Make adoption of your platform optional — that forces the platform team to keep it good.

**Don't:**
- Don't co-locate microservices from different teams on the same host — it creates configuration contention and uneven deployment.
- Don't use vertical scaling alone — bigger machines still fail and don't give horizontal scaling benefits.
- Don't skip the zero-downtime deploy capability if your team is on-call at 3 a.m. — Sarah Wells at the FT calls this the single biggest delivery improvement.
- Don't keep the autoscale group active in dev — autoscaling "fixed" a thing the operator forgot existed, in the book's anecdote.
- Don't run your own Kubernetes cluster unless you have dedicated ops — use a managed one.

*Ref: Building_Microservices.md — "Principles of Microservice Deployment" / "Isolated Execution" / "Focus on Automation" / "Infrastructure as Code (IAC)" / "Zero-Downtime Deployment" / "Desired State Management" / "Prerequisites" / "GitOps"*

---

### Containers & Kubernetes

**Principle:** Containers are the default deployment unit for microservices. Kubernetes wins the orchestration space, but use a managed cluster and treat it as hidden infrastructure.

**Do:**
- Use containers (Docker) as the standard artifact — they're portable, fast, and isolate well.
- Use Kubernetes only when you have enough services to justify the operational overhead (probably > ~5 services, depending on team).
- Prefer managed Kubernetes (EKS/GKE/AKS) over self-hosted.
- Design your artifact to be environment-agnostic — config lives outside.
- Treat container images as immutable — re-deploy rather than patch in place.
- Consider Firecracker, Hyper-V isolation, or Windows process isolation if your threat model needs stronger sandboxing.
- Remember that Kubernetes and FaaS are not mutually exclusive — Knative brings FaaS-style workflows on top of Kubernetes.

**Don't:**
- Don't run Kubernetes for 3 services and 2 developers — overhead dwarfs benefit.
- Don't think "Kubernetes gives portable apps" — your platform/operators/workflow is not portable, only the runtime is.
- Don't let container images become a permanent stale state — patch and rebuild regularly (Equifax breach shows the cost).
- Don't try to deploy CRDs you don't understand — Kubernetes' "extensibility" can quickly become a tar pit.

*Ref: Building_Microservices.md — "Containers" / "Kubernetes and Container Orchestration" / "The Case for Container Orchestration" / "A Simplified View of Kubernetes Concepts" / "Platforms and Portability" / "Helm, Operators, and CRDs, Oh My!" / "Should You Use It?"*

---

### Serverless / FaaS

**Principle:** FaaS is the most developer-friendly deployment abstraction we have. Use it for appropriate workloads; "function per microservice" is the safe starting point.

**Do:**
- Try FaaS before reaching for Kubernetes — "explore FaaS first, it may give you everything you need while hiding significant complexity."
- Start with one function per microservice; keep a coarser-grained external interface.
- Use FaaS for low/predictable/unpredictable load — pay only for what runs.
- Watch for mismatch between FaaS scaling and downstream (e.g., Bustle's Lambda-vs-Redis overload incident).

**Don't:**
- Don't build per-state-transition functions for one aggregate — it pulls you into saga complexity for no win.
- Don't pick FaaS if you need fine-grained control over CPU/I/O — you only control memory allocation.
- Don't chain Lambdas with Step Functions for long-running workflows without thinking — Azure Durable Functions exists for a reason.
- Don't ignore cold-start times for runtimes like JVM/.NET — Go/Node/Python/Ruby are safer.

*Ref: Building_Microservices.md — "Function as a Service (FaaS)" / "Mapping to microservices" / "Function per microservice" / "Function per aggregate" / "Challenges" / "The way forward"*

---

### Progressive Delivery (Blue-Green, Canary, Feature Toggles, Parallel Run)

**Principle:** Decouple *deployment* from *release*. You can deploy without releasing, then release progressively.

**Do:**
- Implement blue-green or canary deployments — deploy new version, switch traffic incrementally.
- Use feature toggles to hide incomplete work in trunk-based development.
- Use parallel runs (with tools like GitHub Scientist) when migrating critical functionality and need true comparison.
- Automate canary ramp-up based on metrics (Spinnaker does this).
- Be willing to deploy during business hours if you can roll back fast — fewer off-hours incidents.

**Don't:**
- Don't conflate deployment with release — they are different concepts (Humble).
- Don't use feature toggles as a permanent architecture — clean them up.
- Don't run a parallel run on actual side-effecting operations without a designated "source of truth" implementation.

*Ref: Building_Microservices.md — "Progressive Delivery" / "Separating Deployment from Release" / "Feature Toggles" / "Canary Release" / "Parallel Run" / "Smoke tests"*

---

### Testing Microservices

**Principle:** Optimize for fast feedback. End-to-end tests across many services and many teams become an anti-pattern; replace with smaller-scope tests and consumer-driven contracts.

**Do:**
- Use the test pyramid: many unit tests, fewer service tests, far fewer end-to-end tests (rough ratio ~10× per layer).
- Have each team own and run tests for their service — including its end-to-end tests where possible.
- Use test doubles for service tests: stubs (don't care if called) over mocks (verify call counts) where possible.
- Run service tests with only the microservice under test + stubbed collaborators.
- Track and remove flaky tests immediately — "the normalization of deviance" lets bugs slip.
- Use the right tool: mountebank for general stubbing, Pact for consumer-driven contracts.
- Run tests on demand, not on shared integrated environments (Accelerate research).
- Prefer peer review of changes (or pair programming) over external review boards — they correlate with higher delivery performance.

**Don't:**
- Don't let your end-to-end test suite balloon across teams — it forces coordination and undermines independent deployability.
- Don't have a dedicated test team write E2E tests for service code — it distances the developers from the tests.
- Don't use shared test environments as a default — they become coordination bottlenecks.
- Don't let an E2E test suite run for hours — that's a sign of insufficient curation or over-reliance on E2E.
- Don't use the "metaversion" trick (versioning all services together) — that's a distributed monolith in disguise.
- Don't wait for production-quality testing to happen — accept MTTR (mean time to repair) as a primary metric alongside MTBF.

*Ref: Building_Microservices.md — "Types of Tests" / "Test Scope" / "Trade-Offs" / "Implementing Service Tests" / "Mocking or Stubbing" / "A Smarter Stub Service" / "Implementing (Those Tricky) End-to-End Tests" / "Flaky and Brittle Tests" / "Who Writes These End-to-End Tests?" / "How Long Should End-to-End Tests Run?" / "The Great Pile-Up" / "The Metaversion" / "Lack of Independent Testability" / "Should You Avoid End-to-End Tests?" / "Contract Tests and Consumer-Driven Contracts (CDCs)" / "Pact" / "The Final Word" / "Developer Experience"*

---

### Consumer-Driven Contract Testing (CDCs)

**Principle:** Consumers specify their expectations of providers; providers verify they meet them. CDCs replace cross-team E2E tests for verifying compatibility.

**Do:**
- Use CDCs to detect breaking changes before deploy, without standing up an integrated environment.
- Pair producer and consumer teams on writing the contract.
- Use Pact (multi-language, multi-protocol) or Spring Cloud Contract (JVM-only).
- Run CDCs in the *producer's* build to ensure backward compatibility.
- Store contracts in a Pact Broker so producers can see which consumers depend on them.
- Recognize that CDCs are a conversation trigger as much as a test — they surface change discussions early.

**Don't:**
- Don't try to use CDCs between organizations with no communication or trust — they require collaboration.
- Don't assume CDCs replace ALL E2E tests — they're one tool for verifying *compatibility*, not behavior end-to-end.
- Don't manually maintain a brittle in-house schema-diff tool — Pact already exists and works.

*Ref: Building_Microservices.md — "Contract Tests and Consumer-Driven Contracts (CDCs)" / "Pact" / "Other options" / "It's about conversations"*

---

### Performance & Robustness Testing

**Principle:** Performance must be tested early and continuously. Robustness tests prove your stability patterns work.

**Do:**
- Run performance tests at least weekly — they're expensive but indispensable when latency regresses.
- Set explicit targets ("90th percentile < 2s at 200 concurrent connections") — without targets, results are noise.
- Run a subset of perf tests daily and a broader set weekly.
- Test robustness by deliberately inducing failures (timeouts, slow responses) to verify your circuit breakers / timeouts / bulkheads actually fire.
- Track CFRs (cross-functional requirements) at the individual microservice level — payment can have stricter SLOs than recommendations.

**Don't:**
- Don't defer performance testing until just before launch — you'll be firefighting with no baseline.
- Don't run performance tests without checking the results.
- Don't share performance infrastructure with services that have very different load profiles.
- Don't underestimate how much a 1ms-per-call degradation compounds across many hops in microservices.

*Ref: Building_Microservices.md — "Cross-Functional Testing" / "Performance Tests" / "Robustness Tests"*

---

### Testing in Production

**Principle:** Pre-production testing cannot cover everything. Testing in production is a feature, not a failure.

**Do:**
- Separate deployment from release; test deployed-but-not-released code.
- Use synthetic transactions for semantic monitoring — they catch real-user-impacting failures faster than low-level metrics.
- Use canary releases as "testing in production" — small percentage of users on new version.
- Use real user monitoring (RUM) to compare actual behavior against your semantic model.
- Use feature toggles to test new functionality with a beta group.
- Run Game Days / chaos engineering exercises (Netflix's Simian Army) to validate responses.
- Use parallel runs (GitHub Scientist) when re-implementing critical functionality.
- Optimize MTTR (mean time to repair) — fast rollback + good monitoring beats preventing every outage.

**Don't:**
- Don't inject fake orders into production without proper isolation — one team shipped real washing machines to their office.
- Don't dismiss testing in production as reckless — you're already doing it (ping checks are tests).
- Don't optimize only for MTBF — incident response capability matters equally.

*Ref: Building_Microservices.md — "From Preproduction to In-Production Testing" / "Types of In-Production Testing" / "Making Testing in Production Safe" / "Mean Time to Repair over Mean Time Between Failures?" / "Synthetic transactions" / "A/B testing" / "Canary release" / "Parallel run" / "Smoke tests" / "Chaos engineering" / "Game Days" / "Production Experiments"*

---

### Observability (Logs, Metrics, Tracing, SLOs)

**Principle:** Build log aggregation first. Add correlation IDs from day one. Distributed tracing follows when complexity demands. Observability is a property of the system, not a tool you buy.

**Do:**
- Treat log aggregation as a *prerequisite* for adopting microservices — "if you can't do this, you can't do microservices."
- Use a standardized log format internally so queries work across services.
- Implement correlation IDs from day one (pass them through HTTP headers, message metadata, log entries) — retrofitting is painful.
- Capture host metrics (CPU, memory, I/O) plus per-instance application metrics (response times, downstream call counts).
- Distinguish SLA (customer-facing commitment), SLO (team's objective), and SLI (the measured signal).
- Use error budgets to balance reliability work against feature work — when under budget, take risks.
- Use semantic monitoring — define what "the system is working" means and alert on that, not on low-level metrics.
- Use synthetic transactions as the primary signal of "is the user-facing system healthy?"
- Adopt OpenTelemetry for vendor-neutral instrumentation.

**Don't:**
- Don't ship without log aggregation in place.
- Don't try to retrofit correlation IDs later — it's painful; do it from the start.
- Don't rely solely on log timestamps for causality across services — clock skew makes them unreliable.
- Don't mistake the "three pillars of observability" for the goal — observability is the property; metrics/logs/traces are inputs.
- Don't alert on every little blip — Three Mile Island and Boeing 737 Max show alert fatigue kills.
- Don't pick monitoring tools without considering whether they're democratic (usable by all) and easy to integrate (OpenTelemetry standards).
- Don't skip high-cardinality data — it's what lets you ask questions you didn't know to ask.

**Code:**
```
15-02-2020 16:01:01 Gateway   INFO [abc-123] Signup for streaming
15-02-2020 16:01:02 Streaming INFO [abc-123] Cust 773 signs up ...
15-02-2020 16:01:03 Customer  INFO [abc-123] Streaming package added ...
15-02-2020 16:01:03 Email     INFO [abc-123] Send streaming welcome ...
15-02-2020 16:01:03 Payment   ERROR [abc-123] ValidatePayment ...
```
*Ref: Building_Microservices.md — "Single Microservice, Single Server" / "Single Microservice, Multiple Servers" / "Multiple Services, Multiple Servers" / "Observability Versus Monitoring" / "The Pillars of Observability? Not So Fast" / "Building Blocks for Observability" / "Log Aggregation" / "Common format" / "Correlating log lines" / "Timing" / "Implementations" / "Shortcomings" / "Metrics Aggregation" / "Low versus high cardinality" / "Implementations" / "Monitoring and Observability Systems Are Production Systems" / "Distributed Tracing" / "How it works" / "Implementing distributing tracing" / "Are We Doing OK?" / "Service-level agreement" / "Service-level objectives" / "Service-level indicators" / "Error budgets" / "Alerting" / "Some problems are worse than others" / "Alert fatigue" / "Toward better alerting" / "Semantic Monitoring" / "Real user monitoring" / "Testing in Production" / "Synthetic transactions" / "Standardization" / "Selecting Tools" / "Democratic" / "Easy to Integrate" / "Provide Context" / "Real-Time" / "Suitable for Your Scale" / "The Expert in the Machine" / "Getting Started"*

---

### Resilience & Stability Patterns (Timeouts, Retries, Bulkheads, Circuit Breakers)

**Principle:** Anything can fail. Latency kills. Apply layered stability patterns everywhere; never let one bad citizen take down the system.

**Do:**
- Put timeouts on **every** out-of-process call — defaults are fine to start, tune per call.
- Set both per-call and overall-operation timeouts — propagate remaining time budget downstream.
- Retry only on transient errors (5xx, 504), not deterministic errors (404).
- Use exponential backoff with jitter for retries; cap max retries; respect the overall time budget.
- Implement bulkheads: separate connection pools per downstream service, so one slow service can't exhaust all workers.
- Mandate circuit breakers on all synchronous downstream calls — they fail fast when downstream is unhealthy.
- Degrade functionality gracefully: hide the shopping cart if Inventory is down rather than failing the whole page.
- Spread risk across availability zones / data centers (AWS SLA requires it).
- Implement idempotency on all write operations using a unique request ID.
- Know the difference between MTBF and MTTR — and invest in both.

**Don't:**
- Don't default-disable timeouts on connection pools — the book's case study shows this kills a system in 5 minutes.
- Don't make retry-after-failure loops without a maximum retry limit — classic catastrophic failover.
- Don't share connection pools across downstream services — the book shows this exactly.
- Don't retry on 4xx (deterministic client errors) — retrying a 404 is pointless.
- Don't keep retrying after exceeding the overall time budget.
- Don't bring down all traffic to a failing service — give it room to recover.
- Don't trust your broker to deliver *exactly once* — design for at-least-once + idempotent consumer.

**Code:**
```xml
<!-- Example 12-1: NOT idempotent -->
<credit>
  <amount>100</amount>
  <forAccount>1234</account>
</credit>

<!-- Example 12-2: Idempotent via reference key -->
<credit>
  <amount>100</amount>
  <forAccount>1234</account>
  <reason>
    <forPurchase>4567</forPurchase>
  </reason>
</credit>
```
*Ref: Building_Microservices.md — "What Is Resiliency?" / "Robustness" / "Rebound" / "Graceful Extensibility" / "Sustained Adaptability" / "How Much Is Too Much?" / "Degrading Functionality" / "Stability Patterns" / "Time-Outs" / "Retries" / "Bulkheads" / "Circuit Breakers" / "Isolation" / "Redundancy" / "Middleware" / "Idempotency" / "Spreading Your Risk" / "CAP Theorem" / "Antifragility" / "Chaos Engineering" / "Game Days" / "Production Experiments" / "Blame"*

---

### Security (Defense in Depth, Zero Trust, Secrets, JWTs)

**Principle:** Microservices increase attack surface but also enable more fine-grained defense in depth. Operate under zero trust by default; automate security hygiene.

**Do:**
- Apply the principle of least privilege to every credential — minimum scope, minimum time.
- Use defense in depth: network segmentation, per-service auth, mix of runtimes.
- Threat-model before building — know your attackers and assets (NIST: Identify/Protect/Detect/Respond/Recover).
- Use mutual TLS (service mesh can automate it) for service-to-service auth.
- Store secrets in a vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault); rotate frequently; revoke on demand.
- Limit credential scope per microservice instance (one per instance if possible).
- Use OpenID Connect for end-user SSO (SAML is dying).
- Use JWTs with short expiration, per-request regeneration at the gateway, for decentralized authorization.
- Use salted password hashing — never reversible encryption for passwords.
- Encrypt data at rest and in motion; encrypt backups too.
- Automate patching; use tools (Snyk, GitHub code scanning, Trivy, Aqua) to find vulnerable dependencies.
- Be frugal with data — if you don't store PII, it can't be stolen (Datensparsamkeit).
- Run pre-commit secret scanners (git-secrets, gitleaks).
- Build security into delivery, not as a gate after.

**Don't:**
- Don't bury your head in technical controls while leaving obvious physical/organizational holes — the CCTV-vs-broken-door anecdote.
- Don't hand out credentials with broad scope "for simplicity" — that's exactly what attackers exploit.
- Don't store keys in the same database they protect.
- Don't roll your own encryption — use vetted libraries.
- Don't make JWTs valid for days — short-lived, per-request tokens prevent replay.
- Don't put fine-grained authorization logic in the directory service — keep authorization decisions local to the owning microservice.
- Don't put all authorization in a single gateway — that creates a single point of failure and defeats defense in depth.
- Don't ship to customers who can't run your Kubernetes cluster — pick deployment models they can operate.
- Don't conflate implicit trust and zero trust — they're a spectrum; pick by zone (MedicalCo's zone example).
- Don't forget the human side — open culture post-incident, not blame culture.

*Ref: Building_Microservices.md — "Core Principles" / "Principle of Least Privilege" / "Defense in Depth" / "Types of Security Controls" / "Automation" / "Build Security into the Delivery Process" / "The Five Functions of Cybersecurity" / "Identify" / "Protect" / "Detect" / "Respond" / "Recover" / "Foundations of Application Security" / "Credentials" / "User credentials" / "Secrets" / "Rotation" / "Revocation" / "Scanning for Keys" / "Limiting scope" / "Patching" / "Backups" / "Rebuild" / "Implicit Trust Versus Zero Trust" / "Implicit Trust" / "Zero Trust" / "It's a Spectrum" / "Securing Data" / "Data in Transit" / "Server identity" / "Client identity" / "Visibility of data" / "Manipulation of data" / "Data at Rest" / "Go with the well known" / "Pick your targets" / "Be frugal" / "It's all about the keys" / "Encrypt backups" / "Authentication and Authorization" / "Service-to-Service Authentication" / "Human Authentication" / "Common Single Sign-On Implementations" / "Single Sign-On Gateway" / "Fine-Grained Authorization" / "The Confused Deputy Problem" / "Centralized, Upstream Authorization" / "Decentralizing Authorization" / "JSON Web Tokens" / "Format" / "Using tokens" / "Challenges"*

---

### Scaling (Vertical, Horizontal, Data Partitioning, Functional Decomposition)

**Principle:** Do the easy stuff first. Scale along one axis at a time. Combine axes as needed.

**Do:**
- Try **vertical scaling** (bigger machine) first — on the cloud it's quick, cheap, and risk-free.
- Try **horizontal duplication** (more instances behind a load balancer) next — often the cheapest big win.
- Use **data partitioning** when you're write-constrained; pick partition keys carefully (e.g., sign-up ID, not family name — see China surname anecdote).
- Use **functional decomposition** as a last resort and only when other scaling paths are exhausted — it's invasive.
- Combine axes: functional decomposition enables horizontal duplication; horizontal duplication pairs with data partitioning.
- Combine CQRS / event sourcing only when simpler techniques (read replicas) have failed.
- Cache sparingly, in as few places as possible — nested caches are a freshness nightmare.
- Use TTLs, conditional GETs (ETag / If-None-Match), notification-based invalidation, or write-through as appropriate.

**Don't:**
- Don't partition by something with skewed distribution (surname, geographic region with uneven population).
- Don't do premature optimization — the only "real" need is a measured bottleneck.
- Don't try to "beat CAP" — pick AP or CP per capability, and know that "eventually consistent" means you tolerate staleness.
- Don't push read consistency too high for things that don't need it.
- Don't ignore that data partitioning reduces robustness per partition (1/N of traffic fails if a partition dies).
- Don't put a cache between every call — golden rule is "cache in as few places as possible."
- Don't use Cache-Control: Expires: Never on anything you might need to change — the book's "cache poisoning" tale shows how badly this ends.

*Ref: Building_Microservices.md — "The Four Axes of Scaling" / "Vertical Scaling" / "Horizontal Duplication" / "Data Partitioning" / "Functional Decomposition" / "Combining Models" / "Start Small" / "CQRS and Event Sourcing" / "Caching" / "For Performance" / "For Scale" / "For Robustness" / "Where to Cache" / "Client-side" / "Server-side" / "Request cache" / "Invalidation" / "Time to live (TTL)" / "Conditional GETs" / "Notification-based" / "Write-through" / "Write-behind" / "The Golden Rule of Caching" / "Freshness Versus Optimization" / "Cache Poisoning: A Cautionary Tale" / "Autoscaling" / "Starting Again"*

---

### User Interfaces (Micro Frontends, BFFs)

**Principle:** Decompose the UI like you decompose the backend. Break the frontend monolith. Use BFFs only when you need them.

**Do:**
- Use **stream-aligned teams** that own UI + supporting microservice end-to-end — eliminates handoffs.
- Use **micro frontends** (widget-based or page-based decomposition) for web SPAs — different teams ship independently.
- Prefer page-based decomposition as your default for traditional websites — simple, no JS framework needed.
- Use a **BFF** when you need server-side aggregation/filtering for a specific UI type (especially mobile).
- Apply the "one experience, one BFF" guideline — diverging experiences deserve diverging BFFs.
- Use GraphQL if you need fine-grained query control without per-screen BFF endpoints.
- Embed user interface specialists via enabling teams, not via dedicated frontend teams.

**Don't:**
- Don't let a dedicated frontend team own the entire UI — it becomes a coordination bottleneck and silos.
- Don't shoehorn SPAs into a use case better served by page-based websites ("looking at you, Sydney Morning Herald").
- Don't put a BFF in front of a single UI when simple page-based decomposition works.
- Don't merge BFFs across diverging mobile platforms owned by different teams.
- Don't use iFrames for widget splicing — sizing and cross-frame communication are painful.
- Don't fall back to a central aggregating gateway once multiple teams need it — that's the gateway anti-pattern.
- Don't let a third-party API gateway product own your call aggregation logic — extraction becomes a rewrite.

*Ref: Building_Microservices.md — "Ownership Models" / "Toward Stream-Aligned Teams" / "Sharing Specialists" / "Ensuring Consistency" / "Working Through Technical Challenges" / "Pattern: Monolithic Frontend" / "Pattern: Micro Frontends" / "Self-Contained Systems" / "Pattern: Page-Based Decomposition" / "Pattern: Widget-Based Decomposition" / "Pattern: Central Aggregating Gateway" / "Pattern: Backend for Frontend (BFF)" / "How Many BFFs?" / "Reuse and BFFs" / "BFFs for Desktop Web and Beyond" / "A Hybrid Approach"*

---

### Conway's Law & Organizational Structure

**Principle:** Your architecture will mirror your organization. To get a loosely coupled architecture, build a loosely coupled organization. Use Conway's law in reverse to design the org you want.

**Do:**
- Use **stream-aligned teams** (per Team Topologies) — small teams owning end-to-end slices of user-facing functionality.
- Adopt **strong ownership** of microservices — one team per service for independent deployability.
- Keep teams small: 5–10 people ("two-pizza team"); don't scale a single team — scale by adding more teams.
- Move specialists out of dedicated teams into enabling teams (or embed in stream-aligned teams).
- Use communities of practice to share knowledge across teams.
- Pick a "paved road" platform that's optional but easy — adoption correlates with platform quality.
- Use geographically distributed teams only when timezone differences are small.
- Plan for cross-cutting changes — accept that some pain is unavoidable; minimize it via good boundaries.
- Encourage internal open source for shared codebases with clear committer boundaries.

**Don't:**
- Don't adopt microservices without changing the org structure — you'll pay the cost without getting the benefit.
- Don't use **collective ownership** at scale — it forces coordination and undermines independent deployability.
- Don't make ownership cross team lines for a single microservice — that boundary will fail under delivery contention.
- Don't have a dedicated test team write end-to-end tests — it distances developers from quality.
- Don't let a single team own a shared microservice by virtue of many inbound PRs — that's a sign to transfer ownership or split.
- Don't copy the "Spotify model" or "Amazon model" blindly — understand the why.
- Don't allow the architecture to dictate Conway's law in the wrong direction — the example of the print firm that grew into its arbitrary 3-tier design is cautionary.
- Don't throw people at a late project (Brooks's Law) — split the work so it can be done in parallel, or it gets worse.

*Ref: Building_Microservices.md — "Loosely Coupled Organizations" / "Conway's Law" / "Evidence" / "Team Size" / "Understanding Conway's Law" / "Small Teams, Large Organization" / "On Autonomy" / "Strong Versus Collective Ownership" / "Strong Ownership" / "How far does strong ownership go?" / "Collective Ownership" / "At a Team Level Versus an Organizational Level" / "Balancing Models" / "Enabling Teams" / "Communities of Practice" / "The Platform" / "The platform team" / "The paved road" / "Shared Microservices" / "Too Hard to Split" / "Cross-Cutting Changes" / "Delivery Bottlenecks" / "Internal Open Source" / "Role of the Core Committers" / "Maturity" / "Tooling" / "Pluggable, Modular Microservices" / "Change Reviews" / "The Orphaned Service" / "Case Study: realestate.com.au" / "Geographical Distribution" / "Conway's Law in Reverse" / "People"*

---

### Architectural Leadership (Evolutionary Architect)

**Principle:** The architect's role is town planner, not ivory-tower designer. Architect as part of an enabling team.

**Do:**
- Think like a town planner: define zones (boundaries, inter-service contracts) and let teams decide inside them.
- Be worried about what's between the boxes, liberal about what's inside.
- Spend time embedded with teams — pair program, do real work, see the day-to-day.
- Make governance a group activity with the people doing the work.
- Define strategic goals → principles → practices (in that order) and keep them under 10 principles.
- Build the paved road / platform to make doing the right thing easy, not mandatory.
- Use exemplars (real microservices doing things right) rather than fictional template code.
- Treat architecture as a social construct (per Ralph Johnson) — it's what people collectively agree is important.
- Adapt the architecture as you learn — fitness functions help measure architectural drift.
- Have a "good citizen microservice" checklist: monitoring standards, interface standards, safety patterns applied.

**Don't:**
- Don't issue ivory-tower mandates — the developer will simply ignore them.
- Don't create diagrams instead of helping teams ship — architecture is what happens, not what's planned (Grady Booch).
- Don't over-engineer the standard microservice template — it will become a bloated, mandatory framework that everyone resents.
- Don't pull governance into a separate authority — it must be a collaborative, distributed activity.
- Don't overrule groups without a clear "duck pond" reason — micromanagement kills autonomy.
- Don't ignore Conway's law — the org and the architecture must evolve together.
- Don't ask an architect to spend all their time in meetings — they need to actually code and embed.

*Ref: Building_Microservices.md — "What's in a Name?" / "What Is Software Architecture?" / "Making Change Possible" / "An Evolutionary Vision for the Architect" / "Defining System Boundaries" / "A Social Construct" / "Habitability" / "A Principled Approach" / "Strategic Goals" / "Principles" / "Practices" / "Combining Principles and Practices" / "A Real-World Example" / "Guiding an Evolutionary Architecture" / "Architecture in a Stream-Aligned Organization" / "Building a Team" / "The Required Standard" / "Monitoring" / "Interfaces" / "Architectural Safety" / "Governance and the Paved Road" / "Exemplars" / "Tailored Microservice Template" / "The Paved Road at Scale" / "Technical Debt" / "Exception Handling"*

---

## Anti-Patterns & Common Mistakes

- **Distributed monolith:** Multiple services that must be deployed together — you have all the complexity, none of the benefits. *Fix:* revisit boundaries, hide state, reduce coupling. *Ref: "The Distributed Monolith"*
- **Big-bang rewrite:** Trying to extract all microservices at once. *Fix:* strangler fig, extract one at a time. *Ref: "Incremental Migration"*
- **Premature decomposition:** Extracting microservices before the domain has stabilized. *Fix:* wait for stability; start with a modular monolith. *Ref: "The Dangers of Premature Decomposition" (Snap CI)*
- **Shared database across services:** Turns the schema into a public contract. *Fix:* give each service its own data, expose via API or events. *Ref: "Owning Their Own State" / "Common Coupling"*
- **Content coupling (Service A writes directly to Service B's database):** "Pathological coupling." *Fix:* Service B owns the data; Service A calls Service B. *Ref: "Content Coupling"*
- **Thin CRUD wrapper as a microservice:** Logic that should be in the service is spread across consumers. *Fix:* push behavior into the service; reject invalid requests. *Ref: "Content Coupling"*
- **Lockstep deployments across microservices:** Violates independent deployability and triggers distributed-monolith dynamics. *Fix:* prefer expand-and-contract over lockstep. *Ref: "Lockstep Deployment"*
- **Distributed transactions (2PC):** Don't deliver ACID and bring cascading failure risk. *Fix:* use sagas. *Ref: "Distributed Transactions—Just Say No"*
- **Shared connection pool across downstream services:** One slow service starves the others. *Fix:* bulkhead per downstream. *Ref: "Bulkheads"*
- **Missing timeouts on out-of-process calls:** A single slow downstream can bring down the system. *Fix:* put timeouts on every call. *Ref: "Time-Outs" (AdvertCorp case study)*
- **Catastrophic failover:** No max retry limit; a crashing worker re-delivers the same poison message forever. *Fix:* set max retries, use a dead-letter queue. *Ref: "Proceed with Caution"*
- **Excessive end-to-end tests across teams:** Creates coordination, undermines independence. *Fix:* consumer-driven contracts, schema diffs, testing in production. *Ref: "Should You Avoid End-to-End Tests?"*
- **Test snow cone (inverted pyramid):** Few unit tests, lots of broad-scoped tests. *Fix:* invest in smaller-scoped tests. *Ref: "Trade-Offs"*
- **Flaky tests ignored:** Normalization of deviance lets bugs through. *Fix:* track them down or remove them; never accept flakiness. *Ref: "Flaky and Brittle Tests"*
- **Dedicated frontend team:** Creates silos and handoffs. *Fix:* stream-aligned teams; micro frontends. *Ref: "Toward Stream-Aligned Teams"*
- **Central aggregating gateway:** Becomes a bottleneck when multiple teams share it. *Fix:* use BFFs. *Ref: "Pattern: Central Aggregating Gateway" / "When to Use It"*
- **Domain-coupling-induced tight binding to many collaborators:** A service that needs many downstream calls might be doing too much. *Fix:* simplify; consider it a cohesion smell. *Ref: "Domain Coupling"*
- **Bimodal IT:** Dumps hard-to-change stuff in "Mode 1" forever. *Fix:* mode-neutral decomposition. *Ref: "Volatility"*
- **"Microservice = CRUD wrapper over a database":** Signals logic is leaking to consumers. *Fix:* push behavior into the service. *Ref: "Content Coupling"*
- **Trusting a single health check or low-cardinality metric:** You can't ask questions you didn't know to ask. *Fix:* high-cardinality data, correlation IDs, semantic monitoring. *Ref: "Low versus high cardinality" / "Semantic Monitoring"*
- **Cookies/cache headers stuck in intermediate proxies:** "Cache poisoning" — the only fix is changing URLs. *Fix:* understand the full path of cached data, especially user browsers and ISP caches. *Ref: "Cache Poisoning: A Cautionary Tale"*
- **CCTLD-style partitioning by biased key (surname):** Produces wildly uneven load. *Fix:* use uniformly-distributed IDs (sign-up ID, hash). *Ref: "Data Partitioning" / "Key benefits" / "Limitations"*
- **Blaming people after outages:** Creates fear culture; same outages recur (Telstra). *Fix:* blameless post-mortems; learn from incidents. *Ref: "Blame"*
- **Static-only thinking: building infra as a "monolithic microservice admin team":** Trade-off siloed expertise for cross-team enablement. *Fix:* platform team as an enabling function. *Ref: "The Platform" / "Enabling Teams"*
- **Calling soap/REST/RPC/gRPC/MQTT all in one system:** Integration nightmare. *Fix:* one or two interface standards org-wide. *Ref: "Interfaces" / "Looking for the Ideal Technology"*

---

## Decision Heuristics / Checklists

### "Should I use microservices?" checklist
- [ ] Do I have a clear, measurable goal (team autonomy, hot-path scaling, etc.)?
- [ ] Is my domain stable enough that boundary churn is bounded?
- [ ] Is my team big enough that coordination overhead is the bottleneck (≥ ~5 teams)?
- [ ] Can I commit to log aggregation, CI/CD, and observability before I start?
- [ ] Am I OK with significant upfront complexity for long-term optionality?
- If any answer is "no," start with a modular monolith and reconsider later.

### "Is my microservice boundary correct?" checklist
- [ ] Does one team own it (strong ownership, not collective)?
- [ ] Can I change the implementation without breaking consumers?
- [ ] Is the database hidden behind the boundary?
- [ ] Does the data ownership make ACID violations between services impossible?
- [ ] Is the interface stable (low churn) while the implementation is free to evolve?
- [ ] Are related behaviors that change together inside the boundary?
- [ ] Is it aligned with a bounded context or aggregate?

### "Is my service ready to extract?" checklist
- [ ] Is it loosely coupled with high cohesion internally?
- [ ] Does it have a clear, well-defined interface?
- [ ] Have I extracted the code first, leaving data in the monolith temporarily?
- [ ] Do I have a clear plan for the data decomposition step?
- [ ] Have I implemented parallel run / feature toggle to verify behavior?

### "Should I use sync or async?" decision tree
- Need an immediate response to proceed? → Synchronous blocking (REST/gRPC)
- Long-running operation (hours/days)? → Asynchronous request-response (queue)
- Multiple consumers should each react independently? → Event-driven (topic)
- Need to buffer load spikes / decouple availability? → Asynchronous (any)
- All above: combine multiple styles in the same service.

### "Should I use a BFF?" checklist
- [ ] Are you supporting multiple distinct UI types (web, iOS, Android)?
- [ ] Does each UI need different aggregation/filtering of underlying microservices?
- [ ] Do you have multiple teams, each owning one UI experience?
- If yes → BFF per UI type, owned by the team that owns the UI.

### "Stability patterns — which to apply?" default
- Every out-of-process call: timeout (yes), bulkhead (yes), circuit breaker (yes).
- Retries: only on transient errors, with exponential backoff + jitter, capped.
- Idempotency: every write operation, using a unique request key.
- Bulkhead: separate connection pools per downstream.
- Circuit breaker: open on N failures / timeouts within a window; half-open after cooldown.

### "Observability minimum bar"
- [ ] Log aggregation tool live and standardized log format.
- [ ] Correlation IDs propagated across all calls.
- [ ] Host and per-instance metrics collected.
- [ ] SLA / SLO / SLI defined and surfaced.
- [ ] Alerting rule against symptoms, not causes.
- [ ] Synthetic transactions on critical journeys.
- [ ] Distributed tracing once complexity justifies it.

---

## Key Takeaways

1. **Independent deployability is the defining property.** If you can't deploy one service without changing others, you don't have microservices — you have a distributed monolith.
2. **Information hiding + hidden databases = independent deployability.** Expose the minimum; hide the rest.
3. **Service boundaries follow bounded contexts.** Start with one bounded context per service; subdivide aggregates only when needed.
4. **Sync vs async vs events is a design decision first, technology second.** Pick the communication style, then pick the tool.
5. **Sagas, not 2PC.** Model business processes as a sequence of local transactions with compensations; orchestration when one team owns it, choreography when many do.
6. **Six stability patterns on every out-of-process call:** timeout, retry (with backoff), bulkhead, circuit breaker, idempotency, degradation.
7. **CDCs replace cross-team E2E tests.** Consumer specifies expectations; producer verifies them in their build.
8. **Log aggregation + correlation IDs are prerequisites.** Not "nice to have" — required.
9. **Containerize, but don't Kubernetes-for-3-services.** Match the deployment technology to operational scale.
10. **Organizational structure drives architecture (Conway's law).** Strong ownership, stream-aligned teams, optional paved-road platform.
11. **BFFs beat central gateways.** Per-UI-type backend, owned by the UI team.
12. **The architect is a town planner, not an emperor.** Define zones, enable teams, ship code with them.
13. **Avoid technology fetishes and big-bang rewrites.** Incremental, evolutionary, measured.
14. **Make it easy to do the right thing.** Paved roads, exemplars, platform defaults — not mandates.
15. **Optimize for MTTR as well as MTBF.** Fast rollback + good observability often beats trying to prevent every failure.

---

## Cross-References
- Related: [[../Mastering_Api_Architecture.md]]
- Related: [[../Learning_API_Styles.md]]
- Related: [[../Restful_Web_API_Patterns_and_Practices.md]]
- Related: [[../Continuous_API_Management.md]]
- Related: [[../Fundamentals_of_Software_Testing.md]] (testing pyramid + microservices)
- Related: [[../The_Art_of_Unit_Testing.md]] (service test stubs and mocks)
- Topic index: [[../INDEX.md]]