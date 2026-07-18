# Building Microservices (2nd Edition) — Sam Newman

**Author:** Sam Newman (independent consultant; author of *Monolith to Microservices*)
**Topic tags:** `#architecture` `#api` `#testing` `#distributed-systems`
**Language focus:** Language-agnostic (Go, Java, JVM, .NET, Node, Clojure, Python, Ruby all appear in examples)
**Sources:** `markdown_output/Building Microservices 2nd edition/Building Microservices 2nd edition.md` · `summaries/Building_Microservices_2nd_edition.md`

---

## TL;DR

Building Microservices 2e is the definitive practitioner guide to designing fine-grained systems: finding service boundaries via information hiding and DDD, choosing between synchronous and asynchronous communication styles, modeling distributed workflows with sagas, replacing shared databases with per-service ownership, splitting the monolith incrementally via the strangler fig, and operating the resulting system with log aggregation, distributed tracing, correlation IDs, and structured observability. The book's recurring thesis is **independent deployability** — every decision (coupling, data ownership, schema versioning, saga rollback, circuit breakers, deployable BFFs, team topology) is judged against whether it preserves the ability to change one service without coordinating changes elsewhere. Read it for the 2014 → 2021 evolution of microservices thinking (Kubernetes, service mesh, FaaS, GraphQL, micro frontends, consumer-driven contracts) and for hard-won case studies (Gilt, Netflix, BBC, REA, realestate.com.au, Monzo, Comcast, FinanceCo, PaymentCo, AdvertCorp).

---

## Best Practices by Topic

### What "Microservices" Actually Means (and Why It Is Different from SOA)

**Principle:** Microservices are *independently releasable* services modeled around a business domain — not just "small services" or "SOA done right."

**Do:**
- Define microservices by *independent deployability*: you must be able to change, deploy, and release one service without coordinating with any other service. *Ref: Building Microservices 2nd edition.md — "Key Concepts of Microservices" / "Independent Deployability"*
- Encapsulate state inside each service (its own database or schema); expose functionality only via network endpoints. *Ref: Building Microservices 2nd edition.md — "Owning Their Own State"*
- Align service boundaries with bounded contexts from domain-driven design. *Ref: Building Microservices 2nd edition.md — "Modeled Around a Business Domain"*
- Treat "micro" as a sizing hint only ("as big as your head"), not a numeric target. *Ref: Building Microservices 2nd edition.md — "Size"*

**Don't:**
- Mistake microservices for any small service. The 2nd edition explicitly calls out the "monolithic distributed monolith" as the failure mode to avoid — services that look separate but must be deployed together. *Ref: Building Microservices 2nd edition.md — "The Distributed Monolith"*
- Share databases across services "to make things easier." This destroys independent deployability. *Ref: Building Microservices 2nd edition.md — "Don't share databases unless you really need to"*

**Code/Diagram:** The hexagonal microservice — each service encapsulates its own data and exposes only network endpoints.

```
┌──────────────────────────────────┐
│ Microservice (own code + data)   │ ← hidden implementation
│ ┌─────┐ ┌──────┐ ┌────────────┐  │
│ │ UI  │ │ Busi│ │  Database  │  │
│ └─────┘ └──────┘ └────────────┘  │
└────────────────┬─────────────────┘
                 │ network endpoint
                 ▼
            Consumers
```

*Ref: Building Microservices 2nd edition.md — Figure 1-1 "A microservice exposing its functionality over a REST API and a topic"*

---

### When to Use Microservices (and When Not To)

**Principle:** Microservices are an option, not a default. The monolith is the sensible starting point for most new systems.

**Do:**
- Adopt microservices when you have a clear, specific goal — improving team autonomy, scaling a known bottleneck, enabling independent release — and that goal justifies the operational complexity. *Ref: Building Microservices 2nd edition.md — "Should I Use Microservices?"*
- Reach for microservices in SaaS / 24-7 / cloud-native contexts where independent deployability directly unlocks business value. *Ref: Building Microservices 2nd edition.md — "Where They Work Well"*
- Wait until the domain has stabilized before splitting — premature decomposition is more costly than a working monolith. *Ref: Building Microservices 2nd edition.md — "The Dangers of Premature Decomposition" (Snap CI case study)*

**Don't:**
- Pick microservices for brand-new products or startups whose domain is still in flux. "Find product-market fit" beats "have microservices." *Ref: Building Microservices 2nd edition.md — "Whom They Might Not Work For" (Uber started as limos; Flickr was a game)*
- Adopt microservices because everyone else is. Cost-driven IT ("cost center") culture will starve them of investment. *Ref: Building Microservices 2nd edition.md — "Cost"*
- Ship microservices as on-premise software that customers deploy. They can't run your "20 pods on Kubernetes." *Ref: Building Microservices 2nd edition.md — "Whom They Might Not Work For"*

---

### Monolith-First and Incremental Migration

**Principle:** Start monolithic; chip away with the strangler fig; never big-bang rewrite.

**Do:**
- Default to a single-process monolith (or modular monolith) at the start. It's the sensible default choice. *Ref: Building Microservices 2nd edition.md — "Advantages of Monoliths" / DHH "The Majestic Monolith"*
- Treat the existing monolith as "a block of marble" — chip away incrementally, learning as you go. *Ref: Building Microservices 2nd edition.md — "Incremental Migration" (Fowler "If you do a big-bang rewrite, the only thing you're guaranteed of is a big bang")*
- Use the strangler fig pattern: intercept calls, route new functionality to a microservice, leave the rest on the monolith until you're done. *Ref: Building Microservices 2nd edition.md — "Strangler Fig Pattern" (Martin Fowler)*
- Run old and new side-by-side with the parallel run pattern when migrating critical paths. *Ref: Building Microservices 2nd edition.md — "Parallel Run"*
- Pick the easiest, highest-confidence first extraction to build momentum; tackle harder extractions once you have lessons learned. *Ref: Building Microservices 2nd edition.md — "What to Split First?"*

**Don't:**
- Decompose by technical layer ("UI tier vs. backend tier vs. database tier") — that's the original sin that produces three-tier monoliths with cross-team coordination. *Ref: Building Microservices 2nd edition.md — "Decomposition by Layer" (MusicCorp favorite-genre example)*
- Extract microservices before understanding the domain — premature decomposition is one of the most expensive mistakes you can make. *Ref: Building Microservices 2nd edition.md — Snap CI case study*

---

### Information Hiding and Cohesion (Parnas Applied to Microservices)

**Principle:** The connections between modules are the assumptions one module makes about another. Minimize those assumptions.

**Do:**
- Hide as much as possible behind each microservice boundary; expose only what is needed. This is Parnas's information hiding applied at the service level. *Ref: Building Microservices 2nd edition.md — "Information Hiding" (Parnas 1971)*
- Group behavior that changes together ("code that changes together, stays together" — even though the original source is unknown). *Ref: Building Microservices 2nd edition.md — "Cohesion"*
- Aim for "strong cohesion, low coupling" (Constantine's law, as refined by Endres & Rombach). *Ref: Building Microservices 2nd edition.md — "The Interplay of Coupling and Cohesion"*

**Don't:**
- Let a service that does "a thin slice of all three tiers" smuggle in technical-layer decomposition in disguise — that's still fine *internally*, but the *external* boundary must be business-domain. *Ref: Building Microservices 2nd edition.md — "Layering Inside Versus Layering Outside"*

---

### The Four Types of Coupling (Domain, Pass-Through, Common, Content)

**Principle:** Coupling is not binary. There are flavors, ranked from loose (acceptable) to pathological (eliminate).

**Do:**
- Allow **domain coupling** — one microservice calling another because it needs its domain functionality. Minimize the number of dependencies, send only the minimum data, and "be conservative in what you do, be liberal in what you accept from others." *Ref: Building Microservices 2nd edition.md — "Domain Coupling" / Postel's law*
- Treat **pass-through coupling** as a code smell: when Service A sends data to Service B purely because Service C needs it downstream, restructure. Either have A call C directly, or — preferred — have B accept the upstream input as opaque data and construct what C needs locally. *Ref: Building Microservices 2nd edition.md — "Pass-Through Coupling"*
- Eliminate **content coupling** (Service A reaching directly into Service B's database or private API). It destroys information hiding. *Ref: Building Microservices 2nd edition.md — "Content Coupling" (Lamport: "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable")*

**Don't:**
- Treat **common coupling** (shared databases, shared configuration) as harmless. Even read-only shared reference data eventually evolves and the schema change cascades across all consumers. *Ref: Building Microservices 2nd edition.md — "Common Coupling"*
- Treat incoming requests as guaranteed-successful — every external request is a request that the downstream microservice *can reject*. *Ref: Building Microservices 2nd edition.md — "Make sure you see a request … as something that the downstream microservice can reject if it is invalid"*

**Decision rule:**

| Coupling type | Action |
|---|---|
| Domain | Minimize, accept |
| Pass-through | Restructure |
| Common | Avoid, especially for read/write |
| Content | Eliminate immediately |

*Ref: Building Microservices 2nd edition.md — "Types of Coupling"*

---

### Temporal Coupling — The Hidden Killer

**Principle:** Two services must both be up at the same time for a synchronous call to succeed — and the caller blocks until the response arrives.

**Do:**
- Recognize that chains of synchronous calls (Order Processor → Payment → Fraud Detection → Customer) create exponential fragility: any failure or slowness in any hop cascades. *Ref: Building Microservices 2nd edition.md — Figure 4-3*
- Take long-running or slow paths (e.g., warehouse dispatch) out of the synchronous chain — move Fraud Detection to background processing. *Ref: Building Microservices 2nd edition.md — Figure 4-4*
- Use asynchronous communication (message brokers) when temporal coupling is the dominant constraint. *Ref: Building Microservices 2nd edition.md — "A Brief Note on Temporal Coupling"*

**Don't:**
- Hide the network from developers with abstractions that obscure synchronous remote calls — they will write chatty, fragile code. *Ref: Building Microservices 2nd edition.md — "Local calls are not like remote calls"*

---

### Domain-Driven Design for Microservice Boundaries

**Principle:** Bounded contexts and aggregates map naturally onto microservice boundaries.

**Do:**
- Start with **ubiquitous language** — use the same words in code as in conversation. Avoid the "IBM banking model" trap of generic abstractions that obliterate domain meaning. *Ref: Building Microservices 2nd edition.md — "Ubiquitous Language"*
- Model an **aggregate** as a real-world concept (Order, Invoice, Stock Item) with state, identity, and a managed life cycle. One microservice can own one or more aggregates; one aggregate must never be split across microservices. *Ref: Building Microservices 2nd edition.md — "Aggregate"*
- Target a **bounded context** as your initial microservice — start coarse, subdivide later, hiding the subdivision behind the same external interface. *Ref: Building Microservices 2nd edition.md — "Mapping Aggregates and Bounded Contexts to Microservices" (Figure 2-16: Warehouse internally split into Inventory + Shipping, consumers unaware)*
- Make cross-aggregate references explicit with a URI or pseudo-URI (e.g., `soundcloud:tracks:123`) rather than opaque foreign-key IDs. *Ref: Building Microservices 2nd edition.md — Figure 2-13 (Calçado at SoundCloud)*
- Use **event storming** workshops to discover the domain model collaboratively: identify domain events (orange sticky notes), commands (blue), then aggregates (yellow) and bounded contexts. *Ref: Building Microservices 2nd edition.md — "Event Storming" (Brandolini)*

**Don't:**
- Treat bounded contexts as technical-layer boundaries; they are semantic ownership boundaries. *Ref: Building Microservices 2nd edition.md — Hidden models vs. shared models (MusicCorp Stock Item)*

---

### Alternative Decomposition Axes (Volatility, Data, Technology, Organizational)

**Principle:** Domain-first is the default, but other axes are legitimate when the goal demands them.

**Do:**
- Use **volatility-based decomposition** when the dominant driver is time-to-market and you want to extract the parts of the system changing most frequently. *Ref: Building Microservices 2nd edition.md — "Volatility"*
- Use **data-based decomposition** when regulatory/compliance concerns (e.g., PCI scope reduction) dictate boundary placement. *Ref: Building Microservices 2nd edition.md — Figure 2-17 PaymentCo (PCI Level 1: split out credit-card processing to a red zone to shrink audit scope)*
- Use **technology-based decomposition** when performance or runtime characteristics force a different language (e.g., Rust for a hot path). *Ref: Building Microservices 2nd edition.md — "Technology"*
- Use **organizational decomposition** to mirror your team boundaries — and reshape teams to match the architecture you want. *Ref: Building Microservices 2nd edition.md — "Organizational" (Conway's law in reverse)*

**Don't:**
- Worship a single axis dogmatically. Most real microservice architectures mix several. *Ref: Building Microservices 2nd edition.md — "Mixing Models and Exceptions"*

---

### Shared vs. Private Data — Draw the Line

**Principle:** Each microservice owns its data. Cross-service joins become API calls; cross-service integrity becomes eventual consistency or sagas.

**Do:**
- Give each microservice its own private database or schema; never expose it directly across service boundaries. *Ref: Building Microservices 2nd edition.md — "Don't share databases"*
- Use **soft delete** (or copy-the-data-into-the-ledger) when referential integrity across services was previously enforced by FKs in a single DB. *Ref: Building Microservices 2nd edition.md — "Data Integrity" (MusicCorp Albums → Ledger)*
- Treat the foreign-key relationship *itself* as the cross-service coupling to break, not the data. *Ref: Building Microservices 2nd edition.md — Figure 3-6 vs 3-7 (database join → service calls)*
- Build a **reporting database** (read-only, owned by the microservice, populated by it) when legitimate reporting needs require SQL joins across services. The microservice owns the schema mapping and is responsible for keeping it current. *Ref: Building Microservices 2nd edition.md — Figure 3-8 "Reporting database pattern"*

**Don't:**
- Promise ACID transactions across service boundaries — that path leads to two-phase commit hell. *Ref: Building Microservices 2nd edition.md — "Distributed Transactions—Just Say No"*

---

### Performance — Databases Aren't Free Anymore

**Principle:** Cross-service joins are slower than in-DB joins; measure and mitigate.

**Do:**
- Replace in-DB joins with bulk lookup APIs when the join is hot (e.g., bulk SKU lookup against Catalog, not 1-by-1). *Ref: Building Microservices 2nd edition.md — Figure 3-7 (Finance microservice bestsellers report)*
- Cache monthly reports aggressively; a per-month workload tolerates minutes of latency if you cache the result. *Ref: Building Microservices 2nd edition.md — "Performance"*
- Use tooling that can handle schema-change tracking with versioned delta scripts (Flyway, Liquibase). *Ref: Building Microservices 2nd edition.md — "Tooling"*

**Don't:**
- Assume "just add a service call" is harmless — measure the latency before declaring victory. *Ref: Building Microservices 2nd edition.md — "I'd be very surprised if the overall latency of this operation didn't increase"*

---

### From In-Process to Inter-Process — The Honest Truth

**Principle:** A network call is orders of magnitude slower than a method call. Stop pretending otherwise.

**Do:**
- Design APIs knowing that payloads must be serialized, transmitted, and deserialized. *Ref: Building Microservices 2nd edition.md — "Performance" (inter-process overhead)*
- Run independent calls in parallel rather than sequentially — sum of latencies → max latency. Use reactive extensions / async-await. *Ref: Building Microservices 2nd edition.md — "Parallel Versus Sequential Calls" (MusicCorp stockist prices)*
- Make the network visible to developers. Hide it too much and they will accidentally N+1. *Ref: Building Microservices 2nd edition.md — "Developers should be aware if they are doing something that will result in a network call"*

**Don't:**
- Believe "the network is reliable." It's not. It's the first fallacy of distributed computing. *Ref: Building Microservices 2nd edition.md — Fallacies of distributed computing*

---

### Five Failure Modes You Will Hit

**Principle:** Distributed systems fail in five ways; expect each.

| Mode | Symptom | Example |
|---|---|---|
| **Crash failure** | Server died | Reboot |
| **Omission failure** | No response (timeout) | Downstream unreachable |
| **Timing failure** | Too late or too early | Sluggish DB |
| **Response failure** | Response malformed/wrong | Missing fields |
| **Arbitrary (Byzantine) failure** | Participants disagree | Corrupted state |

*Ref: Building Microservices 2nd edition.md — Tanenbaum & Steen, "Five failure modes"*

**Do:**
- Use HTTP 4xx (client error — don't retry) vs 5xx (server-side — may be retryable) semantics. *Ref: Building Microservices 2nd edition.md — "Error Handling"*

---

### Picking the Right Inter-Service Communication Style

**Principle:** Decide on style first, technology second.

**Do:**
- Default to **event-driven** when you want loose coupling, broadcast, and inversion of intent. The emitter doesn't know (or care) who consumes. *Ref: Building Microservices 2nd edition.md — "Event-Driven Communication" (Newman: "I see far more teams replacing request-response interactions with event-driven interactions than the reverse")*
- Use **synchronous blocking** only when you genuinely need the immediate response and the call chain is short. Familiarity is a real advantage. *Ref: Building Microservices 2nd edition.md — "Pattern: Synchronous Blocking"*
- Use **request-response asynchronous** (queues) for long-running processes where the response comes back later to a different instance (state-store the correlation). *Ref: Building Microservices 2nd edition.md — "Pattern: Request-Response Communication" (Figure 4-10 stock reservation)*
- Use **common-data** (file/dwh drop) for bulk transfers and interop with legacy systems that can't speak your protocols. *Ref: Building Microservices 2nd edition.md — "Pattern: Communication Through Common Data"*

**Don't:**
- Treat `async/await` as asynchronous in the distributed-systems sense — it still blocks the calling thread until the promise resolves. *Ref: Building Microservices 2nd edition.md — "Async/Await and When Asynchronous Is Still Blocking" (Example 4-1 eurToGbp)*

---

### Request vs. Command — Reject What Doesn't Make Sense

**Principle:** A microservice gets to reject any incoming request. Commands imply obligation; requests do not.

**Do:**
- Use the term *request*, not *command*. A request can be denied; a command implies obedience. *Ref: Building Microservices 2nd edition.md — "Commands Versus Requests"*

---

### Events — Just an ID or Fully Detailed?

**Principle:** Put in the event everything consumers would otherwise have to call back for — unless PII or size concerns stop you.

**Do:**
- Prefer **fully detailed events** (the whole customer object, not just the ID). Consumers become self-sufficient and don't pile back onto the source microservice. *Ref: Building Microservices 2nd edition.md — Figure 4-14 (Notifications/Loyalty both self-sufficient)*
- Treat events as part of the **contract**: removing a field breaks consumers. *Ref: Building Microservices 2nd edition.md — "once we put data into an event, it becomes part of our contract"*

**Don't:**
- Send PII in widely-broadcast events. Solve with two event types (one with PII, one without) and accept the dual-emission complexity. *Ref: Building Microservices 2nd edition.md — PII example*

---

### Event-Driven Implementation — Kafka, Brokers, Brokers Without Smart Middleware

**Principle:** Use a message broker for pub/sub durability; keep the middleware dumb.

**Do:**
- Use **Apache Kafka** for large-volume, replayable, partitioned event streams. Use **RabbitMQ / ActiveMQ** for classic point-to-point messaging. *Ref: Building Microservices 2nd edition.md — "Choices" (Figure 5-1 vs 5-2 queue vs topic)*
- Distinguish **queues** (one consumer group = load distribution) from **topics** (multiple consumer groups = broadcast). *Ref: Building Microservices 2nd edition.md — Figure 5-1 vs 5-2*
- Trust the broker's **guaranteed delivery**, but read the docs — RabbitMQ needs low-latency cluster networks or it loses data. *Ref: Building Microservices 2nd edition.md — "Guaranteed delivery"*
- Always configure a **max retry limit** and a **dead letter queue** (message hospital) for poison messages. *Ref: Building Microservices 2nd edition.md — 2006 pricing system anecdote*
- **Keep middleware dumb, smarts in the endpoints.** Avoid the Enterprise Service Bus trap. *Ref: Building Microservices 2nd edition.md — "Do be wary, though, about the world of middleware"*

**Don't:**
- Rely on **exactly-once delivery** as a guarantee. Build idempotent consumers instead (check event ID before processing). *Ref: Building Microservices 2nd edition.md — "Exactly once delivery"*

---

### RPC, REST, GraphQL — Pick by Audience and Constraints

**Principle:** REST is the sensible default for synchronous service-to-service; gRPC for controlled internal use; GraphQL for constrained mobile/external clients; avoid Java RMI / SOAP-era RPC for new work.

**Do:**
- Use **REST over HTTP** for sync request-response; benefit from caching, ecosystem, security tooling. Sensible default. *Ref: Building Microservices 2nd edition.md — "REST and HTTP"*
- Use **gRPC** when you control both client and server, want strong typing and binary efficiency over HTTP/2. Top of the list for internal use. *Ref: Building Microservices 2nd edition.md — "Where to use it" (gRPC)*
- Use **GraphQL** at the perimeter for mobile/external clients that need aggregation and field selection. Beware: GraphQL doesn't mix well with CDNs/caches, and "GraphQL makes it feel like you are just working with data" — don't slip into microservices-as-DB-wrappers. *Ref: Building Microservices 2nd edition.md — "Challenges"*
- Use **Pact / consumer-driven contracts** (Pact + Pact Broker) when consumer and producer are in different repos/builds. The Pact file is the artifact. *Ref: Building Microservices 2nd edition.md — "Pact"*

**Don't:**
- Hide the network so well with RPC that developers don't know they are making remote calls (Java RMI's failure mode). *Ref: Building Microservices 2nd edition.md — Figure 5-2 example "createCustomer" brittleness*
- Hype HATEOAS as the cure-all — most teams don't actually practice it. *Ref: Building Microservices 2nd edition.md — "Despite intellectually appreciating the goals behind HATEOAS, I haven't seen much evidence that … it delivers worthwhile benefits"*

---

### Avoiding and Managing Breaking Changes

**Principle:** Make backward-compatible changes the default; expand, don't break.

**Do:**
- Add new fields; never remove old ones. *Ref: Building Microservices 2nd edition.md — "Expansion Changes"*
- Apply Postel's law: be conservative in what you send, liberal in what you accept. *Ref: Building Microservices 2nd edition.md — "Tolerant Reader"*
- Use an explicit schema and compare versions on every build (`Protolock` for protocol buffers, `openapi-diff`, `json-schema-diff-validator`). Fail the build on incompatible changes. *Ref: Building Microservices 2nd edition.md — "Catch Accidental Breaking Changes Early"*
- Track usage of endpoints (log identifiers in `User-Agent` headers or via API gateway keys) before you remove anything. *Ref: Building Microservices 2nd edition.md — "Tracking Usage"*

**Don't:**
- Use **lockstep deployment** (force consumer + producer to ship together) as your default — it poisons independent deployability. Reserve for genuinely trivial one-offs within a single team. *Ref: Building Microservices 2nd edition.md — "Lockstep Deployment"*
- Coexist whole microservice versions long-term — it forks your codebase. Coexist **endpoints** in the same service instead (expand + contract pattern). *Ref: Building Microservices 2nd edition.md — Figure 5-3 vs Figure 5-4 / Newman prefers emulation*

**Emulation pattern code-ish:**
```
V3 service:
  POST /v1/customer → translate to V2 internally → discard
  POST /v2/customer → handle directly
```

---

### DRY vs. Microservices — Coupling Is the Real Cost

**Principle:** Duplication across microservices is fine; coupling from shared codebases is not.

**Do:**
- Tolerate cross-service code duplication; multiple teams using slightly different field validations is OK. *Ref: Building Microservices 2nd edition.md — "DRY and the Perils of Code Reuse in a Microservice World"*
- Use **libraries** only for internal concerns (logging, metrics) that don't leak outside the service boundary. Accept that you'll have multiple versions in flight. *Ref: Building Microservices 2nd edition.md — "Sharing Code via Libraries" (realestate.com.au copies template per-service)*
- Make **client libraries optional**, and let consumers control upgrade timing. If you must share, separate transport-handling code (discovery, retries, auth) from domain code. *Ref: Building Microservices 2nd edition.md — "Client libraries" (Netflix cautionary tale, AWS SDK model)*

**Don't:**
- Share domain models across services via a "common types" library. Changing the `Order` field on one service will pull the other along. *Ref: Building Microservices 2nd edition.md — common-types library horror story*

---

### Service Discovery — Start Simple, Layer Up

**Principle:** DNS + load balancer is good enough for many cases; Consul/etcd/Consul-template add dynamic capabilities when you need them.

**Do:**
- Use **DNS + a load balancer** for a small number of relatively stable instances. Point the LB at instances; remove on failure. *Ref: Building Microservices 2nd edition.md — Figure 5-5*
- Use **Consul** when you want a registry + DNS server + KV store + health checks in one tool; integrate with `consul-template` for dynamic config updates (HAProxy pools, nginx upstream blocks). *Ref: Building Microservices 2nd edition.md — "Consul"*
- Use **etcd + Kubernetes service** when you're on Kubernetes — services are dynamically matched via pod metadata. *Ref: Building Microservices 2nd edition.md — "etcd and Kubernetes"*
- Roll your own (AWS instance tags + APIs) only as a last resort. Newman: "this is not the route I would go." *Ref: Building Microservices 2nd edition.md — "Rolling your own"*

**Don't:**
- Use DNS round-robin — clients can't remove sick hosts. *Ref: Building Microservices 2nd edition.md — "DNS round-robining … is extremely problematic"*

---

### API Gateways vs. Service Meshes — Where Each Belongs

**Principle:** API gateway on the perimeter (north-south); service mesh in-perimeter (east-west). Don't mix.

**Do:**
- Use an **API gateway** (Ambassador, AWS API Gateway, etc.) for routing external traffic, terminating HTTPS, API keys, rate limiting, dev portals. *Ref: Building Microservices 2nd edition.md — "API Gateways"*
- Use a **service mesh** (Istio, Linkerd) to push common inter-service behavior (mTLS, correlation IDs, retries, service discovery) into local sidecar proxies colocated with each pod. *Ref: Building Microservices 2nd edition.md — Figure 5-7 (Envoy-based service mesh)*
- Pick a service mesh committed to **OpenTelemetry** so you can swap vendors. *Ref: Building Microservices 2nd edition.md — "OpenTelemetry"*

**Don't:**
- Stuff call aggregation, protocol rewriting, or business logic into API gateways — keep pipes dumb, endpoints smart. *Ref: Building Microservices 2nd edition.md — "What to avoid"*
- Interpose an API gateway for **east-west** traffic — the latency penalty is real and you should solve in-mesh concerns with a service mesh. *Ref: Building Microservices 2nd edition.md — "The last issue is the use of an API gateway as an intermediary for all inter-microservice calls"*
- Adopt a service mesh with fewer than ~10 services — the complexity overhead dwarfs the benefit. *Ref: Building Microservices 2nd edition.md — "if you have five microservices, I don't think you can easily justify a service mesh"*

---

### Documenting Services — Self-Describing Systems

**Principle:** A humane registry + OpenAPI/CloudEvents > static wikis that rot.

**Do:**
- Use **OpenAPI** for REST endpoints; combine with portals (Ambassador Developer Portal) for autodiscovery and search. *Ref: Building Microservices 2nd edition.md — "Explicit Schemas"*
- Use **CloudEvents** (CNCF) for event-based interface documentation — it has the broadest vendor support. *Ref: Building Microservices 2nd edition.md — "CloudEvents"*
- Build a humane registry: pull from service discovery (Consul/etcd) + source code metadata + health check status into one dashboard. The Financial Times' **Biz Ops** with its System Operability Score is the gold standard. *Ref: Building Microservices 2nd edition.md — Figures 5-8, 5-9*
- Also look at **Spotify Backstage** (pluggable service catalog). *Ref: Building Microservices 2nd edition.md — "Backstage"*

---

### ACID, Two-Phase Commit, and Why You Will Avoid Both

**Principle:** Per-service local ACID is fine; cross-service atomicity is a trap.

**Do:**
- Keep ACID transactions strictly inside a single microservice. *Ref: Building Microservices 2nd edition.md — "Still ACID, but Lacking Atomicity?"*
- Use a single-request version: a database UPDATE within one service is one transaction; if you must span, span it inside one service. *Ref: Building Microservices 2nd edition.md — Figure 6-1 vs 6-2*

**Don't:**
- Implement distributed transactions via **two-phase commit** in microservices. Locks across processes + cascading stalls = Pat Helland's "airplane needs all engines" failure mode. *Ref: Building Microservices 2nd edition.md — "Distributed Transactions—Just Say No" / Pat Helland quote*
- Trust that 2PC gives you ACID — it sacrifices isolation (the coordinator commits at different times, leaving a window of inconsistency). *Ref: Building Microservices 2nd edition.md — Figure 6-4*

---

### Sagas — Long-Running Transactions Without Locks

**Principle:** A saga is a sequence of local transactions + compensating actions for rollback. It gives you *enough information to reason about state*, not ACID.

**Do:**
- Model long-running business processes as sagas explicitly. *Ref: Building Microservices 2nd edition.md — "Sagas" (Garcia-Molina & Salem 1987)*
- Identify and write **compensating transactions** for each step; understand they are *semantic* rollbacks (you cannot un-send an email; you send a second email apologizing). *Ref: Building Microservices 2nd edition.md — Figure 6-7*
- **Reorder saga steps** to put likely-to-fail work earlier, and put irreversible side effects (loyalty points) later — eliminates some compensations. *Ref: Building Microservices 2nd edition.md — Figure 6-8*
- Mix **fail-forward** and **fail-backward** — once you've taken payment and packaged the order, don't roll back the whole saga on a courier failure; just queue the dispatch for tomorrow. *Ref: Building Microservices 2nd edition.md — "Mixing fail-backward and fail-forward situations"*

**Don't:**
- Use sagas to recover from **technical failures** (HTTP 500). The saga assumes healthy underlying components — handle tech failures separately (retries, circuit breakers). *Ref: Building Microservices 2nd edition.md — "Saga allows us to recover from business failures, not technical failures" (Friedrichsen "The Limits of the Saga Pattern")*

---

### Orchestration vs. Choreography

**Principle:** Pick by team boundary, not by taste.

**Do:**
- Use **orchestrated sagas** (central orchestrator) when one team owns the whole saga — coupling is contained within the team. The orchestrator makes the process visible in one place. *Ref: Building Microservices 2nd edition.md — Figure 6-9 / "Should I use choreography or orchestration"*
- Use **choreographed sagas** (events, no central brain) when multiple teams are involved. Coupling drops dramatically, but you lose a single place to view the saga state. *Ref: Building Microservices 2nd edition.md — Figure 6-10*
- Use **correlation IDs** propagated through every event/log/call so you can reconstruct the saga's path. A separate "saga view" service can vacuum up events and project saga state. *Ref: Building Microservices 2nd edition.md — "Tracing Calls"*

**Don't:**
- Put every possible behavior into the orchestrator until services become anemic. If logic has a place to centralize, it will. *Ref: Building Microservices 2nd edition.md — "If logic has a place where it can be centralized, it will become centralized!"*
- Use **BPM tools** (Camunda, Zeebe) without weighing the trade-offs — they're often hostile to version control, GUI-driven, and testing-first workflows. Newman admits Zeebe/Camunda are the dev-friendlier options if you must. *Ref: Building Microservices 2nd edition.md — "BPM Tools"*

---

### The Build Pipeline — Trunk-Based, Build Once, One Pipeline per Service

**Principle:** Every microservice has its own CI build, its own pipeline, its own artifact.

**Do:**
- Verify CI is real (Jez Humble's three questions: check into mainline daily? tests to validate? broken build = #1 priority?). *Ref: Building Microservices 2nd edition.md — "Are You Really Doing CI?"*
- Practice **trunk-based development** with short-lived branches (<1 day, <3 active branches). The 2016/2019 State of DevOps reports back this up empirically. *Ref: Building Microservices 2nd edition.md — "Branching Models" / DORA*
- Build the artifact **once**, promote it through every environment — never rebuild for prod. Keep environment-specific config out of the artifact. *Ref: Building Microservices 2nd edition.md — Figure 7-4*
- Model pipelines as multi-stage (unit tests → service tests → perf tests → prod). The same artifact at each stage. *Ref: Building Microservices 2nd edition.md — Figure 7-1*

**Don't:**
- Use **GitFlow** for closed-source internal teams — it's optimized for open-source trust dynamics that don't apply. *Ref: Building Microservices 2nd edition.md — "Branch-heavy approach is still common in open source"*
- Long-lived feature branches for cross-team work — frequent integration prevents integration hell. *Ref: Building Microservices 2nd edition.md — "Be Careful About Branches"*

---

### Repository Strategy — Multirepo Beats Monorepo at Scale

**Principle:** One repository per microservice. Monorepo is fine for small teams; it hurts at scale.

**Do:**
- Default to **multirepo**: separate repo + build + ownership per microservice. The pain of cross-repo changes forces you to evaluate whether the boundary is right. *Ref: Building Microservices 2nd edition.md — "Pattern: One Repository per Microservice" / Figure 7-6*
- Use **CODEOWNERS** (GitHub) or equivalent to map ownership to paths even within a monorepo. *Ref: Building Microservices 2nd edition.md — Example 7-1*

**Don't:**
- Default to a **monorepo**: cross-service changes become the norm, fine-grained ownership blurs, build complexity explodes (you'll end up needing something Bazel-class). *Ref: Building Microservices 2nd edition.md — "Pattern: Monorepo" (Microsoft Windows GVFS, Google's Piper — Google can afford this, you probably can't)*
- Let "atomic commits across services" become "atomic deploys across services" — that violates independent deployability. *Ref: Building Microservices 2nd edition.md — "Atomic Commits Versus Atomic Deploy"*

---

### Deployment Principles — The Five Pillars

**Principle:** Isolate, automate, IaC, zero-downtime, desired-state.

**Do:**
- **Isolate execution** — one microservice instance per host (VM/container), its own ring-fenced resources. Packing multiple services on a host undermines independent deployability. *Ref: Building Microservices 2nd edition.md — Figure 8-10 vs 8-11*
- **Automate** everything; manual ops at scale = wrong team to hire. *Ref: Building Microservices 2nd edition.md — REA case study: 2 services in 3 months, 10-15 in next 3 months, 70 in 18 months*
- **Infrastructure as Code** — Terraform / Pulumi / Ansible / Chef, version-controlled. The REA court-case story (3 months rebuilding a 2-year-old environment from email) is the cautionary tale. *Ref: Building Microservices 2nd edition.md — "Infrastructure as Code (IAC)"*
- **Zero-downtime deployment** — Sarah Wells (Financial Times): zero-downtime is the single biggest release-velocity unlock. Blue-green + load balancer is sufficient; you don't need Kubernetes. *Ref: Building Microservices 2nd edition.md — "Zero-Downtime Deployment"*
- **Desired state management** — declare N instances across AZs, let Kubernetes/autoscaling groups reconcile. *Ref: Building Microservices 2nd edition.md — Figure 8-13*

**Don't:**
- Run multiple microservices per host just to optimize for "scarcity of resources" — virtualization/containers made that argument obsolete. *Ref: Building Microservices 2nd edition.md — "Many of our working practices around deployment and host management are an attempt to optimize for scarcity"*

---

### Picking a Deployment Platform — Sam's Three Rules

**Principle:** "If it ain't broke, don't fix it." Then give up control incrementally. Then containerize.

**Do:**
- Apply Sam's Really Basic Rules of Thumb:
  1. If it ain't broke, don't fix it.
  2. Give up control. Use Heroku/FaaS if it fits.
  3. Containerize + Kubernetes when the complexity overhead is justified.
  *Ref: Building Microservices 2nd edition.md — "Which Deployment Option Is Right for You?"*

**Don't:**
- Adopt Kubernetes for 5 microservices. Use FaaS / Heroku / a managed container platform first. *Ref: Building Microservices 2nd edition.md — "Kubernetes for just a few microservices … brings with it its own sources of complexity"*

---

### Containers — Use Them, But Know Their Limits

**Principle:** Containers are the sweet spot for microservice isolation; trust them for trusted code.

**Do:**
- Use **Linux containers** (Docker) — fast spin-up (seconds vs minutes for VMs), efficient resource sharing, technology-agnostic packaging. *Ref: Building Microservices 2nd edition.md — "Containers"*
- Use Windows Hyper-V isolation when running untrusted multi-tenant workloads. *Ref: Building Microservices 2nd edition.md — "Windows containers"*

**Don't:**
- Treat containers as perfect isolation. For malicious untrusted code, do your own threat assessment. *Ref: Building Microservices 2nd edition.md — "you should view containers as a great way of isolating execution of trusted software"*
- Ignore image vulnerability scanning (Aqua) — you inherit whatever's in your base image. *Ref: Building Microservices 2nd edition.md — "Patching"*

---

### Kubernetes — Use It, But Understand the Trade-Offs

**Principle:** Kubernetes has won the orchestrator race — but it's not for everyone, and most apps don't need its full power.

**Do:**
- Learn the core concepts: **Pod** (≥1 containers), **Service** (stable routing endpoint), **Deployment** (rolling upgrades, replica set management). *Ref: Building Microservices 2nd edition.md — "A Simplified View of Kubernetes Concepts"*
- Use a **managed** Kubernetes (EKS, GKE, AKS) — running your own cluster is a significant operational commitment. *Ref: Building Microservices 2nd edition.md — "Even better, use a fully managed cluster"*
- Use **federation** when you need cross-cluster redundancy or staged cluster upgrades. *Ref: Building Microservices 2nd edition.md — Figure 8-24*
- Match the value of **Helm** / **Operators** / **CRDs** to your use case. Use OpenShift when you need out-of-the-box multitenancy. *Ref: Building Microservices 2nd edition.md — "Helm, Operators, and CRDs, Oh My!"*

**Don't:**
- Adopt **Knative** in production yet — it's still in flux, requires Istio, and Google has (controversially) kept it out of CNCF. *Ref: Building Microservices 2nd edition.md — "And Knative"*
- Believe Kubernetes portability is automatic — your platform (CI/CD, observability, secrets, ingress) is custom; moving requires rebuilding. *Ref: Building Microservices 2nd edition.md — "Platforms and Portability"*

---

### FaaS — Serverless Without the Hype

**Principle:** FaaS is the developer experience we want; the current implementations have constraints you must accept.

**Do:**
- Map a microservice to **one function per microservice** initially. *Ref: Building Microservices 2nd edition.md — Figure 8-18*
- Use **one function per aggregate** when DDD aggregates are clear — preserves aggregate life-cycle integrity. Hide the split behind a coarser-grained external interface. *Ref: Building Microservices 2nd edition.md — Figure 8-19/8-20*
- Use languages with fast cold-start (Go, Python, Node, Ruby) to mitigate cold-start latency. *Ref: Building Microservices 2nd edition.md — "Challenges"*

**Don't:**
- Break an aggregate into **one function per state transition** — reintroduces saga complexity for no gain. *Ref: Building Microservices 2nd edition.md — "I struggle … to see the value in adding this complexity at the level of managing a single aggregate"*
- Mix dynamic-scaling FaaS with non-scaling dependencies (e.g., Bustle's Redis meltdown from Lambda surge). *Ref: Building Microservices 2nd edition.md — "Bustle" anecdote*

---

### Progressive Delivery — Deploy ≠ Release

**Principle:** Deployment is installation; release is making functionality available. Separate them.

**Do:**
- Use **blue-green deployments** for instant rollback and working-hours releases. *Ref: Building Microservices 2nd edition.md — "Separating Deployment from Release"*
- Use **canary releases** to roll out to 1% → 10% → 100% of traffic, gated on error-rate metrics. Spinnaker automates this. *Ref: Building Microservices 2nd edition.md — "Canary Release"*
- Use **parallel runs** when correctness matters most — run old and new side-by-side, compare results, only trust the old until you've proven the new. GitHub's **Scientist** library is a great reference. *Ref: Building Microservices 2nd edition.md — "Parallel Run"*
- Use **feature toggles** (LaunchDarkly, Split, or a config file) to hide unfinished work in trunk-based development and to do targeted betas. *Ref: Building Microservices 2nd edition.md — "Feature Toggles" (Pete Hodgson)*

---

### Testing — The Test Pyramid and Where It Breaks

**Principle:** Aim for an order-of-magnitude-more tests as you descend the pyramid. Watch out for the inverted "test snow cone."

**Do:**
- Unit tests (single function, no I/O) — most numerous, fastest.
- Service tests (single microservice, mocked collaborators) — middle layer.
- End-to-end tests (multiple services through UI) — fewest, slowest, brittlest.
- Cross-functional tests (performance, robustness) — track alongside CFRs/SLOs.
  *Ref: Building Microservices 2nd edition.md — Figure 9-1 (Marick), Figure 9-2 (Cohn), "Trade-Offs"*

**Don't:**
- Skip unit tests and rely on end-to-end — you get the "test snow cone" (slow, flaky, hard to diagnose). *Ref: Building Microservices 2nd edition.md — "Antipattern: test snow cone"*
- Let end-to-end tests span multiple teams — undermines independent deployability. *Ref: Building Microservices 2nd edition.md — "What is one of the key problems we are trying to address when we use the end-to-end tests outlined previously?"*

---

### Service Tests — Stubs, Not Mocks (Mostly)

**Principle:** Use stubs (don't care about call counts) over mocks (assert on call counts) for service tests.

**Do:**
- Use **mountebank** (Brandon Byars) for HTTP/TCP/HTTPS/SMTP stubs. Single process can stub many downstream services. *Ref: Building Microservices 2nd edition.md — "A Smarter Stub Service"*
- Stub downstream collaborators with realistic canned responses; mock only when asserting side effects matters. *Ref: Building Microservices 2nd edition.md — "Mocking or Stubbing" (Gerard Meszaros: "Test Doubles")*

---

### End-to-End Tests — Make Them Earn Their Place

**Principle:** End-to-end tests are training wheels. Reduce them over time as CDCs + in-production testing mature.

**Do:**
- Hunt down and **fix or delete flaky tests** immediately — they erode trust (Diane Vaughan's *normalization of deviance*). *Ref: Building Microservices 2nd edition.md — "Flaky and Brittle Tests" (Fowler "Eradicating Non-Determinism in Tests")*
- Use **fan-in** pipelines so multiple microservice builds trigger a shared e2e stage (avoid duplicating the suite per service). *Ref: Building Microservices 2nd edition.md — Figure 9-8*
- Assign e2e tests to specific teams where possible (Emily Bache model). Shared e2e suites with no clear owner = ignored when broken. *Ref: Building Microservices 2nd edition.md — "Who Writes These End-to-End Tests?"*
- Make e2e tests genuinely different from unit tests — if a unit test could catch it, write a unit test. *Ref: Building Microservices 2nd edition.md — "What is one of the key problems we are trying to address?"*

**Don't:**
- Let end-to-end test suites take a day, or six weeks (the worst case Newman cites). Curate, parallelize, delete duplicates. *Ref: Building Microservices 2nd edition.md — "How Long Should End-to-End Tests Run?"*
- Treat versioned-together deployment as acceptable — that's the metaversion trap. *Ref: Building Microservices 2nd edition.md — "The Metaversion" (Brandon Byars: "Now you have 2.1.0 problems")*

---

### Consumer-Driven Contracts — Pact and Friends

**Principle:** A consumer encodes its expectations as a contract; the producer verifies all consumer contracts on every build.

**Do:**
- Use **Pact** (Ruby, JVM, JS, Python, .NET, messaging) — generate the Pact spec on the consumer side via a local mock server; verify on the producer side using the JSON spec. *Ref: Building Microservices 2nd edition.md — "Pact"*
- Use the **Pact Broker** to store contracts centrally and surface dependency graphs. *Ref: Building Microservices 2nd edition.md — "Pact Broker"*
- Treat CDCs as **codified conversations** between teams — the explicit trigger for cross-team collaboration. *Ref: Building Microservices 2nd edition.md — "It's about conversations"*

**Don't:**
- Use **Spring Cloud Contract** unless you're pure JVM — it's not multi-platform like Pact. *Ref: Building Microservices 2nd edition.md — "Other options"*

---

### Testing in Production — Yes, Really

**Principle:** Some defects can only be caught in production. Plan for it.

**Do:**
- Use **smoke tests** post-deploy, pre-release. *Ref: Building Microservices 2nd edition.md — "Making Testing in Production Safe"*
- Use **synthetic transactions** (inject fake user behavior, verify the system processes it) — often just running existing end-to-end tests continuously. *Ref: Building Microservices 2nd edition.md — "Synthetic transactions" (MusicCorp £20K/hour example, Nagios)*
- Use **real user monitoring** against semantic models ("customers can register, we sell ≥ $20K/hour, shipping is normal"). *Ref: Building Microservices 2nd edition.md — "Semantic Monitoring"*
- Use **chaos engineering** (Netflix Chaos Monkey, Chaos Gorilla, Latency Monkey; Chaos Toolkit) to verify your robustness assumptions. *Ref: Building Microservices 2nd edition.md — "Chaos Engineering"*
- Choose **MTTR over MTBF** when forced to trade off — fast rollback + monitoring beats preventing every failure. *Ref: Building Microservices 2nd edition.md — "Mean Time to Repair over Mean Time Between Failures?"*

**Don't:**
- Inject fake orders into prod without flag-isolating them — the washing-machines-at-head-office cautionary tale. *Ref: Building Microservices 2nd edition.md — "Synthetic transactions" anecdote*

---

### Cross-Functional Requirements / Performance / Robustness Tests

**Principle:** CFRs (Sarah Taraporewalla's preferred term over "nonfunctional") need their own tests.

**Do:**
- Define CFRs per service: latency targets, durability, availability, throughput. *Ref: Building Microservices 2nd edition.md — "Cross-Functional Testing"*
- Run performance tests **continuously** (subset daily, full weekly) — debugging a 3-month-old regression is hell. *Ref: Building Microservices 2nd edition.md — "Performance Tests"*
- Treat performance tests like an SLO tripwire — fail the build if latency drifts >X% from baseline. *Ref: Building Microservices 2nd edition.md — "fail the test if the delta in performance from one build to the next varies too much"*
- Build robustness tests by simulating downstream failures (timeouts, broken connections) — especially for shared infrastructure (service mesh, default client). *Ref: Building Microservices 2nd edition.md — "Robustness Tests"*

---

### Observability — Logs First, Tracing When Needed

**Principle:** Observability is a *property* of the system, not an activity. Logs are your starting point.

**Do:**
- Make **log aggregation** a prerequisite for adopting microservices — without it, debugging distributed systems is impossible. *Ref: Building Microservices 2nd edition.md — "Before Anything Else" / Humio recommendation*
- Pick a standard log format (date, time, microservice, log level, correlation ID in fixed positions); let the source emit the format. Avoid log-shipper reformatting on hot paths. *Ref: Building Microservices 2nd edition.md — Example 10-1*
- Propagate **correlation IDs** from the gateway through every downstream call; log them at every step. *Ref: Building Microservices 2nd edition.md — Example 10-2 / Figure 10-6*
- Capture **metrics** with low-cardinality (Prometheus for CPU) AND high-cardinality (Honeycomb, Lightstep for request_id, customer_id, build, etc.). Low-cardinality systems will fall over on the latter. *Ref: Building Microservices 2nd edition.md — "Low versus high cardinality" (Charity Majors)*
- Adopt **distributed tracing** (Jaeger, Zipkin, OpenTelemetry) when correlation IDs aren't enough — span/trace model, sampling (1/1000 default in Jaeger), dynamic sampling for errors. *Ref: Building Microservices 2nd edition.md — "Distributed Tracing" (Figure 10-7 Honeycomb screenshot)*
- Pick observability tools committed to **OpenTelemetry**. *Ref: Building Microservices 2nd edition.md — "OpenTelemetry"*

**Don't:**
- Trust log timestamps across machines — clock skew (NTP only reduces, doesn't eliminate). Use logical clocks or trace IDs. *Ref: Building Microservices 2nd edition.md — "Timing" (Lamport 1978)*
- Treat observability as the "three pillars" (logs/metrics/traces) — those are implementation details, not the goal. Aim for high-cardinality, explorable systems. *Ref: Building Microservices 2nd edition.md — "The Pillars of Observability? Not So Fast"*
- Index every log on Elasticsearch — the SaaS team that hit 6-week log retention with a single product's logs. Use ingestion-focused stores (Humio) or sample. *Ref: Building Microservices 2nd edition.md — "Shortcomings"*

---

### SLOs, SLAs, SLIs, Error Budgets

**Principle:** "Are we doing OK?" — binary up/down is useless. Track against service-level objectives.

**Do:**
- Define **SLIs** (measurable indicators: response time, error rate, throughput).
- Set **SLOs** (what you commit to — 99.9% availability, p95 < 200ms).
- Track **error budgets** (downtime allowance per quarter). *Ref: Building Microservices 2nd edition.md — "Are We Doing OK?" (Google SRE book)*
- Treat your observability/monitoring tools as **production systems** — SolarWinds-style breaches target them. *Ref: Building Microservices 2nd edition.md — "Monitoring and Observability Systems Are Production Systems"*

**Don't:**
- Use the public cloud's SLA as your real target — AWS EC2 single-instance SLA is 90% (effectively meaningless). *Ref: Building Microservices 2nd edition.md — "Service-level agreement"*

---

### Alerting — The Three Mile Island Lesson

**Principle:** Alert on symptoms (user impact), not causes. Quality > quantity.

**Do:**
- Follow the **EEMUA** rules: Relevant, Unique, Timely, Prioritized, Understandable, Diagnostic, Advisory, Focusing. *Ref: Building Microservices 2nd edition.md — "Toward better alerting" (Shorrock "Alarm Design: From Nuclear Power to WebOps")*
- Use **semantic monitoring** with simple value statements (e.g., "new customers can register", "we sell ≥ $20K/hour") rather than low-level CPU alerts. *Ref: Building Microservices 2nd edition.md — "Semantic Monitoring"*
- Implement **synthetic transactions** (per-minute) as a leading indicator of real-user health. *Ref: Building Microservices 2nd edition.md — "Synthetic transactions"*

**Don't:**
- Send every anomaly to a human. The 737 Max alert fatigue contributed to two crashes killing 346 people. The TMI control room "was greatly inadequate for managing an accident." *Ref: Building Microservices 2nd edition.md — "Alert fatigue"*

---

### Security Principles — Least Privilege, Defense in Depth

**Principle:** Microservices expand both attack surface and defense options — balance them.

**Do:**
- Apply **principle of least privilege**: scope credentials narrowly, rotate frequently, revoke immediately. *Ref: Building Microservices 2nd edition.md — "Principle of Least Privilege" (Verizon DBIR: credentials used in 80% of hacking cases)*
- Implement **defense in depth** — multiple independent controls across network, service, application layers. Microservices give you more places to defend. *Ref: Building Microservices 2nd edition.md — Dover Castle analogy*
- Use all three control types: **preventative** (TLS, secrets), **detective** (IDS, Aqua), **responsive** (automated rebuild, backups, comms). *Ref: Building Microservices 2nd edition.md — "Types of Security Controls"*
- Walk through the **NIST five functions**: Identify, Protect, Detect, Respond, Recover. *Ref: Building Microservices 2nd edition.md — "The Five Functions of Cybersecurity"*
- **Threat-model before designing controls** — your developers are reaching for JWTs while an unlocked front door sits open. *Ref: Building Microservices 2nd edition.md — "Identify"*

---

### Credentials, Secrets, Patching, Backups, Rebuild

**Principle:** Even in microservices, basic security hygiene is non-negotiable.

**Do:**
- Use **HashiCorp Vault** for secrets management (time-limited DB credentials, public-key rotation). *Ref: Building Microservices 2nd edition.md — "Secrets"*
- Scan commits for leaked secrets with **git-secrets** or **gitleaks** as pre-commit hooks. *Ref: Building Microservices 2nd edition.md — "Scanning for Keys"*
- Use **salted password hashing** (Argon2, bcrypt) — never encrypt passwords. *Ref: Building Microservices 2nd edition.md — "Data at Rest"*
- Layer each instance with **unique credentials** (not shared across instances) so you can revoke one credential when compromised. *Ref: Building Microservices 2nd edition.md — Figure 11-2*
- Run **Snyk** or GitHub Code Scanning on every build to catch vulnerable dependencies (Equifax/Apache Struts — 160M records, $700M settlement). *Ref: Building Microservices 2nd edition.md — "Patching"*
- Avoid the **Schrödinger backup** — actually restore backups regularly (e.g., into perf test data). Store them on a separate account/region/provider. *Ref: Building Microservices 2nd edition.md — "Backups"*
- Automate **rebuild** from source — same process as normal deploy makes recovery almost a non-event. *Ref: Building Microservices 2nd edition.md — "Rebuild"*

**Don't:**
- Store backups in the same compromised account (Code Spaces — entire company destroyed). *Ref: Building Microservices 2nd edition.md — "Backups" anecdote*

---

### Implicit Trust vs. Zero Trust

**Principle:** It's a spectrum. Pick by data sensitivity.

**Do:**
- Adopt **zero trust** for sensitive data zones. MedicalCo pattern: data classified Public/Private/Secret, microservices run in the matching zone, never reach downward to more sensitive data. *Ref: Building Microservices 2nd edition.md — Figure 11-5 (Jan Schaumann quote)*
- Treat inbound calls from other microservices as hostile by default. *Ref: Building Microservices 2nd edition.md — "When a Stranger Calls" pull quote*

**Don't:**
- Adopt implicit trust inside your perimeter without thinking — most organizations do this by accident, not design. *Ref: Building Microservices 2nd edition.md — "Implicit Trust"*

---

### Data in Transit — Four Concerns

**Principle:** Server identity, client identity, visibility, integrity.

**Do:**
- Use **HTTPS/TLS** for server identity + data visibility. *Ref: Building Microservices 2nd edition.md — "Server identity"*
- Use **mutual TLS** for service-to-service identity (especially in zero-trust). Service meshes make this trivial. *Ref: Building Microservices 2nd edition.md — "Client identity"*
- Encrypt data at rest **on first sight**, decrypt only on demand, never store decrypted. *Ref: Building Microservices 2nd edition.md — "Encrypt data when you first see it"*

**Don't:**
- Roll your own encryption. "Friends don't let friends write their own crypto." *Ref: Building Microservices 2nd edition.md — "Go with the well known"*

---

### Authentication, Authorization, JWT

**Principle:** Centralize user authentication, decentralize authorization to each microservice.

**Do:**
- Use **SSO gateways** (OpenID Connect preferred over SAML — simpler, more modern) for human authentication. *Ref: Building Microservices 2nd edition.md — "Common Single Sign-On Implementations"*
- Use **JSON Web Tokens** to pass claims about the authenticated user to downstream microservices. Generate per-request in the gateway, sign with a private key, validate with the public key (rotate via Vault). *Ref: Building Microservices 2nd edition.md — Example 11-1 / Figure 11-9*
- Use **coarse-grained roles** modeled on how the org actually works — not `CALL_CENTER_50_DOLLAR_REFUND` nightmare roles. *Ref: Building Microservices 2nd edition.md — "Fine-Grained Authorization"*
- Push **fine-grained authorization** down to the microservice that owns the resource (avoid the confused deputy). *Ref: Building Microservices 2nd edition.md — "The Confused Deputy Problem"*

**Don't:**
- Store roles in LDAP that describe specific microservice behavior — couples the microservice to the directory. *Ref: Building Microservices 2nd edition.md — "Fine-Grained Authorization"*

---

### Resiliency — Robustness, Rebound, Graceful Extensibility, Sustained Adaptability (Woods)

**Principle:** Resiliency ≠ robustness. Resiliency is 80% people and culture.

**Do:**
- **Robustness** — handle expected perturbations (retries, redundancy, health checks).
- **Rebound** — recover fast (backups, rebuild automation, runbooks).
- **Graceful extensibility** — handle the unexpected (avoid brittle optimization).
- **Sustained adaptability** — keep questioning your assumptions (chaos engineering).
  *Ref: Building Microservices 2nd edition.md — Woods "Four Concepts for Resilience and the Implications for the Future of Resilience Engineering"*

---

### Stability Patterns — Time-Outs, Retries, Bulkheads, Circuit Breakers

**Principle:** "In a distributed system, latency kills." Fail fast.

**Do:**
- Set time-outs on **every** out-of-process call. Don't disable pool-waiter time-outs (the AdvertCorp 800-connection spike). *Ref: Building Microservices 2nd edition.md — "Time-Outs" (turnip ad system, 30s → 1s + 1s pool wait)*
- Implement **two-level time-outs**: per-call + per-overall-operation. Pass remaining budget downstream. *Ref: Building Microservices 2nd edition.md — "Don't just think about the time-out for a single service call"*
- Use **bulkheads** (separate connection pools per downstream) so one slow downstream doesn't exhaust all workers. *Ref: Building Microservices 2nd edition.md — Figure 12-4 (fix for AdvertCorp)*
- Implement **circuit breakers** (Hystrix/Resilience4j equivalents) per downstream to fail fast after N failures. Auto-reset after cool-down. *Ref: Building Microservices 2nd edition.md — Figure 12-5 (open/closed/half-open states)*
- **Retry transient errors** (5xx, 504) with exponential backoff and jitter; never retry 4xx. *Ref: Building Microservices 2nd edition.md — "Retries"*
- Use **load shedding** (reject requests) to protect critical services. *Ref: Building Microservices 2nd edition.md — "Bulkheads"*
- Build **idempotent** operations — add a `forPurchase` ID, check before processing. *Ref: Building Microservices 2nd edition.md — Example 12-1 vs 12-2*

**Don't:**
- Wait 30 seconds for a page that humans refresh after 5. *Ref: Building Microservices 2nd edition.md — "Time-Outs"*

---

### CAP Theorem — You Don't Beat It, You Pick

**Principle:** In a partition, choose AP or CP per capability — not per system.

**Do:**
- Understand that **CA** is impossible in distributed systems (you can't sacrifice partition tolerance).
- Choose **AP** (eventually consistent) for catalogs, recommendations, browsing.
- Choose **CP** (strongly consistent) for inventory sellability, financial balances.
- Pick per-microservice-capability: Points Balance could be CP on writes but AP on reads. *Ref: Building Microservices 2nd edition.md — "It's Not All or Nothing"*
- Don't roll your own CP system. Use Consul, etcd, or Spanner-class tools. *Ref: Building Microservices 2nd edition.md — "Friends don't let friends write their own distributed consistent data store"*

**Don't:**
- Trust consistency claims without understanding the model — real-world inventory systems can't know about dropped CDs or smashed albums. *Ref: Building Microservices 2nd edition.md — "And the Real World"*

---

### Chaos Engineering — Discipline, Not Tooling

**Principle:** Chaos engineering is the discipline of experimenting on a system to build confidence in its capability to withstand turbulent conditions in production.

**Do:**
- Run **Game Days** for people + process (Bob the indispensable engineer scenario). Google runs full DiRT exercises (earthquake simulations). *Ref: Building Microservices 2nd edition.md — "Game Days" (Russ Miles "Learning Chaos Engineering")*
- Use **production experiments** (Netflix Chaos Monkey / Simian Army) — turn off instances, AZs, inject latency. *Ref: Building Microservices 2nd edition.md — "Production Experiments"*
- Treat chaos engineering as a habit, not a tool deployment. *Ref: Building Microservices 2nd edition.md — "Running a chaos engineering tool doesn't make you resilient"*

---

### Blame-Free Culture — The Telstra Lesson

**Principle:** Blame kills learning. Use blameless post-mortems.

**Do:**
- Adopt **blameless post-mortems** (John Allspaw, Etsy). *Ref: Building Microservices 2nd edition.md — "Blame"*
- Recognize that "human error" post-mortems (Telstra COO blaming one engineer for nationwide outage) hide systemic issues — and Telstra kept having outages. *Ref: Building Microservices 2nd edition.md — Telstra anecdote*

---

### Scaling — The Four Axes

**Principle:** Start simple; combine axes as needed.

**Do:**
- Apply **vertical scaling** first (bigger machine, low effort, on public cloud = resize VM in minutes). *Ref: Building Microservices 2nd edition.md — "Vertical Scaling"*
- Apply **horizontal duplication** next (load balancer + N instances; competing consumers for queues; read replicas for DBs). *Ref: Building Microservices 2nd edition.md — Figure 13-1 / 13-2 / 13-3*
- Apply **data partitioning** when write-throughput is the constraint (Cassandra, Kafka partitions). Pick partition keys carefully (uniform distribution > alphabetic surname). *Ref: Building Microservices 2nd edition.md — "Data Partitioning"*
- Apply **functional decomposition** (extract microservice) when scaling for delivery speed or organizational autonomy. *Ref: Building Microservices 2nd edition.md — Figure 13-6*

**Don't:**
- Partition without combining with horizontal duplication per partition — a partition failure takes 1/Nth of your traffic down. *Ref: Building Microservices 2nd edition.md — "Limitations"*
- Use **CQRS + event sourcing** as a first response — try read replicas first. CQRS is "one of the harder forms of scaling." *Ref: Building Microservices 2nd edition.md — "CQRS and Event Sourcing"*

---

### Caching — The Golden Rule

**Principle:** Cache in as few places as possible. Zero is ideal.

**Do:**
- Cache for **performance** (reduce latency, offload origin), **scale** (offload contention), or **robustness** (operate when origin down — Guardian's static crawl example). *Ref: Building Microservices 2nd edition.md — "For Performance / For Scale / For Robustness"*
- Use **TTL-based invalidation** as the simple default; HTTP `Cache-Control` and `Expires` headers let the origin guide clients. *Ref: Building Microservices 2nd edition.md — "Time to live (TTL)"*
- Use **conditional GETs with ETags** (`If-None-Match`) when the cost of regenerating the resource is high. *Ref: Building Microservices 2nd edition.md — "Conditional GETs"*
- Use **notification-based invalidation** when staleness windows matter (event-driven, e.g., Stock Changed events). Add heartbeats to detect broken notification paths. *Ref: Building Microservices 2nd edition.md — "Notification-based"*
- Use **write-through** caches server-side for minimal staleness windows.

**Don't:**
- Cache in too many places — nested caches compound staleness (1-min Inventory cache × 1-min Recommendation cache = up to 2-min staleness). *Ref: Building Microservices 2nd edition.md — "The Golden Rule of Caching"*
- Trust `Expires: Never` headers in caches you don't control (CDN, ISP, browser) — the AdvertCorp `Squid` + `Expires: Never` bug bit hard. *Ref: Building Microservices 2nd edition.md — "Cache Poisoning: A Cautionary Tale"*

---

### Autoscaling — Start with Failure, Not Load

**Principle:** Use autoscaling for failure conditions first; load-based scaling requires data and care.

**Do:**
- Autoscaling group: "N instances minimum" → handles instance death automatically.
- Layer predictive scaling (cron-like for known daily peaks) with reactive scaling (metric-driven) for surprise spikes.
- Run load tests frequently to verify your scaling rules actually work. *Ref: Building Microservices 2nd edition.md — "Autoscaling"*

**Don't:**
- Scale down too aggressively — having more capacity than needed is much better than not enough. *Ref: Building Microservices 2nd edition.md — "make sure you are very cautious about scaling down too quickly"*

---

### User Interfaces — Toward Stream-Aligned Teams

**Principle:** End-to-end teams need full-stack ownership. The UI must decompose with the backend.

**Do:**
- Break apart frontend into per-team slices; eliminate dedicated frontend teams. *Ref: Building Microservices 2nd edition.md — "Ownership Models" (Figure 14-2)*
- Use **specialists as enabling-team members** (e.g., Financial Times Origami) — they spread expertise and free specialists for hard problems. *Ref: Building Microservices 2nd edition.md — "Sharing Specialists"*
- Trade strict consistency for some UI variation (Amazon/AWS model) if delivery speed matters more than UX polish. *Ref: Building Microservices 2nd edition.md — "Ensuring Consistency" (AWS panel example)*

**Don't:**
- Put specialists in a dedicated team "because they're rare" — it concentrates knowledge and creates bottlenecks. The DB-to-developer analogy: pull DBAs into teams, let them focus on hard DB problems. *Ref: Building Microservices 2nd edition.md — "Sharing Specialists"*

---

### UI Decomposition Patterns

**Principle:** Pick the right decomposition for your UI architecture.

| Pattern | When to Use | Trade-off |
|---|---|---|
| **Monolithic frontend** | Single team owns everything | Can't scale across teams |
| **Page-based** | Web UI; classic navigation | Loses to SPAs |
| **Widget-based** | SPAs; multiple teams in one UI | Dependency bloat, page size |
| **Central aggregating gateway** | Single team, no multiple device needs | Coordination bottleneck |
| **Backend for frontend (BFF)** | Multiple device types, stream-aligned teams | More services to manage |
| **GraphQL** | Constrained mobile/external clients, dynamic queries | Caching complexity, "feels like a DB" |

*Ref: Building Microservices 2nd edition.md — Chapters 14*

**Do:**
- Use **"one experience, one BFF"** (Stewart Gleadow). Different iOS/Android BFFs if different teams own them. *Ref: Building Microservices 2nd edition.md — Figure 14-12 / Figure 14-13 (SoundCloud shared mobile BFF)*
- Use **page-based** decomposition as the default for non-SPA websites. Web pages are a natural decomposition seam. *Ref: Building Microservices 2nd edition.md — "Where to Use It" (page-based)*
- Use **custom events** between in-page widgets (like microservices emit events) instead of iFrames. *Ref: Building Microservices 2nd edition.md — Figure 14-7 / "Communication between in-page widgets"*
- Extract common functionality to a new microservice when the **third** caller appears (rule of three). *Ref: Building Microservices 2nd edition.md — "Reuse and BFFs" (MusicCorp Wishlist example)*

**Don't:**
- Let a central gateway become a coordinator of business logic — that should live in a saga or a microservice. *Ref: Building Microservices 2nd edition.md — "If you find yourself needing to do call aggregation and filtering, then look at the potential of GraphQL or the BFF pattern"*
- Use iFrames to splice widgets — sizing and cross-frame communication are painful. *Ref: Building Microservices 2nd edition.md — "Although iFrames have been a heavily used technique in the past"*

---

### Organizational Structure — Conway's Law in Both Directions

**Principle:** Architecture mirrors organization; organization can be reshaped to produce the architecture you want.

**Do:**
- Aim for **stream-aligned teams** (Skelton & Pais) — end-to-end slice of user-facing functionality, full life-cycle ownership. *Ref: Building Microservices 2nd edition.md — "Toward Stream-Aligned Teams"*
- Use **Amazon's two-pizza team** rule (5–10 people). Empirical evidence: productivity drops sharply past 9. *Ref: Building Microservices 2nd edition.md — "Team Size" / Rodriguez et al. 2012*
- Provide **enabling teams** for cross-cutting concerns (security, UX, observability). They're internal consultancies, not gatekeepers. *Ref: Building Microservices 2nd edition.md — "Enabling Teams"*
- Establish **communities of practice** for ongoing learning (Kubernetes CoP, security CoP). *Ref: Building Microservices 2nd edition.md — "Communities of Practice" (Emily Webber)*
- Provide a **platform** as a paved road (optional, well-supported, not enforced) — Paul Ingles: "We didn't change our organization because we wanted to use Kubernetes; we used Kubernetes because we wanted to change our organization." *Ref: Building Microservices 2nd edition.md — "The Platform"*

**Don't:**
- Mandate strong ownership + central command-and-control — they contradict team autonomy. *Ref: Building Microservices 2nd edition.md — "Organizations have increasingly recognized that if you want to scale your organization but still want to move quickly, you need to distribute responsibility"*
- Concentrate specialists — it starves other teams of those skills. *Ref: Building Microservices 2nd edition.md — DB-to-developer analogy*

---

### Strong vs. Collective Ownership

**Principle:** Strong ownership per service; collective ownership within teams.

**Do:**
- Default to **strong ownership** at the inter-team level — one team per microservice. *Ref: Building Microservices 2nd edition.md — "Strong Ownership"*
- Allow **collective ownership within a team** — any member can change any service the team owns. *Ref: Building Microservices 2nd edition.md — "At a Team Level Versus an Organizational Level"*
- Pursue **full life-cycle ownership** as the aspirational goal — design, build, deploy, run, decommission. *Ref: Building Microservices 2nd edition.md — "How far does strong ownership go?"*

**Don't:**
- Apply collective ownership across teams at scale — coordination overhead destroys the benefits. *Ref: Building Microservices 2nd edition.md — "Collective Ownership"*

---

### Shared Microservices — When You Can't Split

**Principle:** Inherit the cost when forced; explore alternatives first.

**Do:**
- Consider **internal open source** — core committers vet PRs from outside teams. *Ref: Building Microservices 2nd edition.md — "Internal Open Source"*
- Consider **pluggable frameworks** — each team runs its own variation built on a shared skeleton (FinanceCo country teams). *Ref: Building Microservices 2nd edition.md — Figure 15-4*
- Consider **library contributions** to a central microservice for country-specific logic. *Ref: Building Microservices 2nd edition.md — Figure 15-5*
- Watch for signs that a microservice is "really shared": many inbound PRs, slow code review. *Ref: Building Microservices 2nd edition.md — "Pluggable, Modular Microservices"*

---

### Change Reviews — Peer, Not External

**Principle:** Peer review correlates with delivery performance; external review correlates against it.

**Do:**
- Pair program or use synchronous review immediately after submission. Async multi-day PR review destroys context. *Ref: Building Microservices 2nd edition.md — "Synchronous versus asynchronous code reviews" (Accelerate finding)*
- Consider ensemble programming for tricky problems — but be mindful of neurodiversity and power dynamics. *Ref: Building Microservices 2nd edition.md — "Ensemble programming"*

**Don't:**
- Require approval by an external body — Accelerate: "achieved lower performance." *Ref: Building Microservices 2nd edition.md — "Change Reviews"*

---

### The Evolutionary Architect — Town Planner, Not Ivory Tower

**Principle:** Architecture is a social construct; the architect shepherds, not dictates.

**Do:**
- Adopt the **town planner** mindset (Erik Doernenburg): define zones, not specific buildings. Focus on what happens between zones. *Ref: Building Microservices 2nd edition.md — "An Evolutionary Vision for the Architect"*
- State vision in **principles** (fewer than 10, memorable) and **practices** (more detailed, change more often). Heroku's Twelve Factors is the canonical example. *Ref: Building Microservices 2nd edition.md — Figure 16-3 (Evan Bottcher)*
- Use **fitness functions** (Building Evolutionary Architectures) to verify architectural properties — e.g., enforce p95 latency in tests. *Ref: Building Microservices 2nd edition.md — "Guiding an Evolutionary Architecture"*
- Embed with teams: half a day per team per 4 weeks. Work on normal tasks, not artificial ones. *Ref: Building Microservices 2nd edition.md — "Habitability"*
- Be **embarrassed to overrule the group** — sometimes you must (the duck pond), but rarely. *Ref: Building Microservices 2nd edition.md — "Architecture in a Stream-Aligned Organization" (bike/duck-pond analogy)*

**Don't:**
- Issue edicts from an ivory tower. The architecture that emerges will have nothing to do with your diagrams. *Ref: Building Microservices 2nd edition.md — "No plan survives contact with the enemy"*
- Treat technical governance as a control function — make the right thing easy (paved road / templates) instead. *Ref: Building Microservices 2nd edition.md — "Governance and the Paved Road"*

---

### Architectural Safety — Standardize What Must Be Standard

**Principle:** Be worried about what happens between boxes; be liberal inside.

**Do:**
- Standardize across services: monitoring, interfaces, error codes (HTTP 4xx vs 5xx for circuit-breaker correctness), graceful degradation. *Ref: Building Microservices 2nd edition.md — "The Required Standard"*
- Pick one (or two) interface technologies — not twenty. *Ref: Building Microservices 2nd edition.md — "Interfaces"*
- Provide **exemplars** (real services people can mimic) and **tailored microservice templates** (Spring Boot scaffolding, etc.). Make contribution back to the template easy. *Ref: Building Microservices 2nd edition.md — "Exemplars / Tailored Microservice Template"*
- Document technical debt and review it. *Ref: Building Microservices 2nd edition.md — "Technical Debt"*

**Don't:**
- Mandate frameworks that bloat over time. Make the template pull its weight — ease of use is the survival criterion. *Ref: Building Microservices 2nd edition.md — "Caution warranted"*
- Let the architecture guild become a control body — distribute it. Comcast's Architecture Guild (IETF-style) is the positive example. *Ref: Building Microservices 2nd edition.md — "A Social Construct"*

---

### Conway's Law — Evidence

**Principle:** Loosely-coupled orgs produce loosely-coupled systems.

**Do:**
- Heed the empirical evidence:
  - MacCormack/Baldwin/Rusnak: loosely-coupled orgs → more modular software. *Ref: Building Microservices 2nd edition.md — "Evidence"*
  - Microsoft Vista study: organizational metrics (engineers per component) were the strongest predictor of quality. *Ref: Building Microservices 2nd edition.md — "Evidence"*
  - Amazon two-pizza teams, Netflix founding on small teams. *Ref: Building Microservices 2nd edition.md — "Netflix and Amazon"*

---

### Conway's Law in Reverse

**Principle:** System design can reshape the organization over time.

**Do:**
- Use architecture to deliberately grow the org structure that supports it (the print firm's three-stage pipeline drove three divisions; eventually had to rebuild both). *Ref: Building Microservices 2nd edition.md — "Conway's Law in Reverse"*

---

### Cross-cutting Concern: When the Monolith Refuses to Die

**Principle:** The modular monolith is a legitimate destination, not a stepping stone to microservices.

**Do:**
- Recognize that **Shopify** and similar companies thrive on modular monoliths. *Ref: Building Microservices 2nd edition.md — "The Modular Monolith" (Shopify/Kirsten Westeinde reference)*

---

### People — The Final Frontier

**Principle:** Microservice success is 80% people and culture.

**Do:**
- Recognize the rude awakening for developers moving from monolithic (single language, no ops awareness) to microservices (cross-service calls, failure modes, multiple stacks). *Ref: Building Microservices 2nd edition.md — "People"*
- Start with willing people, expand gradually. Hire experienced outsiders to show what's possible. *Ref: Building Microservices 2nd edition.md — "People"*

---

## Anti-Patterns & Common Mistakes

- **Distributed monolith** — multiple services that must be deployed together. The worst of both worlds. *Ref: "The Distributed Monolith"*
- **Premature decomposition** — extracting microservices before the domain has stabilized (Snap CI case study). *Fix:* wait, or extract one, learn, iterate.
- **Sharing databases** — even "for convenience." *Fix:* hide state behind APIs/events.
- **Content coupling** — reaching into another service's database. *Fix:* route through the service's contract.
- **Pass-through coupling** — passing data through B because C needs it. *Fix:* either have A call C directly, or have B accept and reinterpret the data.
- **Three-tier architecture** — UI/backend/data layers as service boundaries. *Fix:* end-to-end slices per bounded context.
- **Lockstep deployment** — forcing consumer + producer to ship together as the default. *Fix:* emulation/expand-contract + Pact/CDCs.
- **Shared domain types via library** — coupling the moment the Order type changes. *Fix:* tolerate duplication; share only transport/utility code.
- **Metaversion** — versioning the whole system, deploying all services together. *Fix:* independent versioning + expand-contract.
- **The "front door / back door" trap** — spending on JWTs while leaving the unlocked front door. *Fix:* threat modeling first.
- **Test snow cone** — inverted pyramid: lots of e2e, few units. *Fix:* replace e2e with units + CDCs + in-prod tests.
- **Blaming humans in incident postmortems** — Telstra pattern: more outages follow. *Fix:* blameless post-mortems.
- **FaaS-per-state-transition** — too granular, reintroduces saga complexity. *Fix:* one function per aggregate or per microservice.
- **Multitenant Kubernetes before you have 10 services** — operational overhead dwarfs benefit. *Fix:* FaaS/PaaS/managed service.
- **BPM tool for saga orchestration** — hostile to VCS, testing, developer workflow. *Fix:* code, or Camunda/Zeebe if you must.
- **Knative in production** — immature, requires Istio, Google kept it out of CNCF. *Fix:* OpenFaaS or wait.
- **Bypassing the platform** by mandate instead of by quality. *Fix:* make the platform better than the bypass.
- **Adopting microservices for brand-new domains.** *Fix:* monolith first.
- **Sharing one auth credential across microservice instances** (one DB user for Inventory × N pods). *Fix:* per-instance credentials via Vault.
- **Cache poisoning with `Expires: Never`** (AdvertCorp story). *Fix:* set explicit cache headers; URL-bust poisoned entries.
- **Alerting on causes instead of symptoms.** *Fix:* semantic monitoring + synthetic transactions.
- **Caching in five nested layers.** *Fix:* minimal caches; understand the staleness compounding.
- **Two-phase commit across microservices.** *Fix:* sagas.
- **Bulkhead-less shared connection pool.** *Fix:* separate pools per downstream (the AdvertCorp 800-connection disaster).
- **Custom CP distributed data store.** *Fix:* buy one (Consul, etcd).
- **Ensemble programming without considering neurodiversity.** *Fix:* give people opt-outs; many will thrive, some won't.
- **The "ivory tower architect"** who issues diagram-only mandates. *Fix:* town planner + embed with teams.
- **Apollo "we've decided to use Kafka for request-response"** — using the wrong tool for the job. *Fix:* match style to problem.
- **SOAP-era RPC hiding the network.** *Fix:* explicit network awareness.
- **Custom encryption.** *Fix:* use vetted libraries.
- **BPM-style deterministic e2e tests across multiple teams.** *Fix:* fan-in ownership, CDCs, in-prod testing.
- **Letting logging and metrics tools be anything less than hardened production systems** — they're the next breach target (SolarWinds). *Fix:* patch, audit, treat as production.

---

## Decision Heuristics / Checklists

### "Should I adopt microservices?" decision flow

1. **Do I have a specific, justified goal?** (team autonomy, scale, independent release) — if no, **stay with the monolith**.
2. **Has the domain stabilized?** — if no, **modular monolith**.
3. **Is the org > ~50 devs with delivery contention?** — if no, **monolith + clear modules**.
4. **Are you a SaaS running 24/7 on cloud?** — microservices start to make sense.
5. **Can the customer install/operate it themselves?** — if yes, **stay monolithic**.

### "Where to deploy?" checklist

1. *Is the workload suited to FaaS?* → FaaS
2. *Will a PaaS (Heroku) suffice?* → PaaS
3. *Do you need fine control?* → containers
4. *Do you have many containers across many machines?* → Kubernetes
5. *Always:* isolated execution, automation, IaC, zero-downtime, desired state.

### "Should this be its own microservice?" checklist

- Single team can own it? ✓
- Independent deploy from siblings? ✓
- Bounded context is clear? ✓
- Cohesion of business functionality? ✓
- Coupling to siblings is domain-only? ✓
- No shared database with siblings? ✓

If 5+ ✓, extract. If most ✗, keep in the monolith or merge with siblings.

### "Sync vs async?" checklist

- Need immediate response? → sync request-response
- Long-running process? → async request-response with correlation
- Multiple consumers care about the same fact? → event-driven
- Single consumer wants a command done? → sync request-response
- Broadcast + high latency tolerance? → event-driven on a topic
- Legacy interop? → common-data (file/dwh drop)

### "How much caching?" checklist

1. Can you avoid the cache entirely? → no cache.
2. Cache only at one place if possible.
3. Document the staleness budget in the response (TTL / Expires).
4. Pick the simplest invalidation that meets the staleness budget (TTL → conditional GET → notification).
5. If you cache in two places, understand the staleness compounding.

### "Alert?" checklist

1. Does waking someone at 3 a.m. *prevent* user pain? — If yes, alert.
2. Is this symptom (user impact) or cause (CPU, queue)? — Alert on symptoms.
3. Could a synthetic transaction catch this earlier? — If yes, replace the alert.
4. Does the alert uniquely identify the action needed? — If no, fix it.
5. Will the alert fire on a known-acceptable state? — If yes, silence or scope it.

### "Coupling check" for a proposed service boundary

| Check | Red Flag |
|---|---|
| Service A reads from Service B's DB | Content coupling |
| Service A and B share a DB schema column | Common coupling |
| Service A passes data to B purely for B-to-C use | Pass-through coupling |
| Service A→B call requires A to know about C | Pass-through coupling |
| Service A→B call needed because A genuinely needs B's domain | Domain coupling ✓ |

---

## Key Takeaways

1. **Independent deployability is the defining characteristic.** Every architectural decision — coupling, data ownership, versioning, sagas, CI/CD, team topology — is judged against whether it preserves the ability to change one service alone. *Ref: "Key Concepts of Microservices" / Independent Deployability*

2. **Information hiding is foundational, not optional.** Hide as much as possible behind stable interfaces; expose only what consumers need. Both Parnas (1971) and the microservices community converge on this. *Ref: "Information Hiding"*

3. **Start monolithic; chip away with the strangler fig.** Microservices are an evolutionary destination, not a starting point. Big-bang rewrites fail. Premature decomposition (Snap CI) is expensive. *Ref: "Splitting the Monolith" / "Incremental Migration"*

4. **Coupling has flavors — rank and eliminate the bad.** Domain coupling is acceptable; pass-through is a smell; common (shared DB) is dangerous; content (reaching into internals) is pathological. *Ref: "Types of Coupling"*

5. **Each microservice owns its data. ACID is local; cross-service atomicity is a saga.** No shared databases. No distributed transactions. Use compensations. *Ref: "Owning Their Own State" / "Workflow"*

6. **Sagas over distributed transactions, always.** Orchestrate when one team owns the saga; choreograph when multiple teams do. Mix and match inside a saga. Use correlation IDs. *Ref: "Sagas"*

7. **Backwards compatibility is the default; expand-and-contract beats lockstep deployment.** Use schemas (OpenAPI, protocol buffers) and diff tools to catch breakages in CI. *Ref: "Avoiding Breaking Changes" / "Managing Breaking Changes"*

8. **Communicate by style first, technology second.** Match event-driven, sync, async, common-data to the problem — not to familiarity. *Ref: "Styles of Microservice Communication"*

9. **Log aggregation is a prerequisite for microservices. Correlation IDs are a prerequisite for log aggregation. Distributed tracing comes later.** Build this stack as you adopt microservices, not after. *Ref: "Log Aggregation" / "Before Anything Else"*

10. **Conway's law is real and bidirectional.** Loosely-coupled orgs produce loosely-coupled systems; small systems can grow into org-defining shapes. Design both deliberately. *Ref: "Conway's Law" / "Conway's Law in Reverse"*

11. **Cap chaos engineering to a discipline, not a tool.** Game Days for people + process; production experiments for the system; blameless post-mortems to capture learning. *Ref: "Chaos Engineering" / "Blame"*

12. **Strong ownership per service; collective ownership within a team.** Stream-aligned teams own end-to-end; enabling teams provide specialist support. *Ref: "Strong Versus Collective Ownership"*

13. **The architect is a town planner, not an architect of buildings.** Define zones, not specific buildings. Use principles + practices + fitness functions. Embed with teams. *Ref: "The Evolutionary Architect"*

14. **Resiliency is 80% people and culture.** Bulkheads, circuit breakers, timeouts are the technical part. Graceful extensibility and sustained adaptability come from blameless learning. *Ref: "Resiliency" / Woods*

15. **Separate deployment from release.** Blue-green, canary, feature toggles, parallel runs — release is a business decision, deployment is a technical one. *Ref: "Progressive Delivery"*

---

## Cross-References

- Related: [[../Monolith_To_Microservices.md]] (Newman's companion deep-dive on extraction patterns)
- Related: [[../Building_Event-driven_Microservices.md]] (event-driven patterns this book references)
- Related: [[../Communication_Patterns.md]] (deeper dive on the async/sync trade-offs)
- Related: [[../Cloud_Application_Architecture_Patterns.md]] (the deployment/observability patterns)
- Related: [[../Observability_Engineering.md]] (the observability and SLO practices)
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] (CAP, chaos, resilience in cloud context)
- Related: [[../Fundamentals_of_Software_Architecture.md]] (architect role, modularity, team topology)
- Related: [[../Designing_Distributed_Systems.md]] (the sidecar/ambassador patterns referenced)
- Related: [[../Learning_Domain_Driven_Design.md]] (DDD substrate for Chapter 2)
- Topic index: [[../INDEX.md]]

---

## Extended Topic Clusters — Deeper Dives From the Book

### The Microservices Journey — A Phased Path

**Principle:** Treat the migration to microservices as a phased journey with explicit checkpoints, not a single leap.

**Phase 1 — Apply the principles even before extracting anything.**
- Even in a monolith, identify bounded contexts, draw seams between modules, and respect information hiding. *Ref: "Layering Inside Versus Layering Outside"*
- Map every cross-team change to understand whether your monolithic system is asking to become distributed. *Ref: "Dangers of Premature Decomposition"*

**Phase 2 — Extract one or two non-critical services.**
- Pick a low-risk slice (MusicCorp's Wishlist extraction is the canonical example). *Ref: Figure 3-2*
- Prove the operational machinery (CI/CD, observability, deployment) before extracting anything load-bearing. *Ref: "Implementation"*
- Confirm the extracted service reduces delivery contention or improves scale before declaring victory. *Ref: "Have a Goal"*

**Phase 3 — Extract services in priority order, sized to deliver value.**
- Start with the easy extractions that build confidence. *Ref: "What to Split First?"*
- Tackle the high-value extractions (frequently changing, scaling-constrained) when the team has the muscle. *Ref: "What to Split First?"*
- Revisit goals quarterly — are you closer to them? *Ref: "Have a Goal"*

**Phase 4 — Operate as a microservice-native organization.**
- Adopt stream-aligned teams, enabling teams, a paved-road platform. *Ref: "Organizational Structures"*
- Replace shared-database antipatterns that survived the migration with proper bounded-context boundaries. *Ref: "Owning Their Own State"*

**Don't:** try to skip phases. The Snap CI team went straight to microservices, hit 100% rework, and rebuilt as a monolith for a year before re-attempting. *Ref: Snap CI case study*

---

### Data Storage Topology — Multiple Logical Databases on Shared Infrastructure

**Principle:** Per-service data ownership does not require per-service hardware.

**Do:**
- Share database infrastructure across logically isolated databases (different DB instances or different schemas) when the cost of dedicated infrastructure outweighs the isolation benefit. The MusicCorp pattern. *Ref: "Database deployment and scaling" / Figure 8-6*
- Use **read replicas** to scale read load off the primary, transparently inside the microservice. *Ref: "Database deployment and scaling" / Figure 8-5*
- Apply **multi-AZ deployment** for databases in the cloud (AWS RDS does this automatically) — single AZ has no SLA. *Ref: "Database deployment and scaling"*

**Don't:**
- Treat shared infrastructure as an excuse to skip isolation at the *logical* level. Logically isolated databases on shared hardware that fail together are still a coupling risk. *Ref: "Database deployment and scaling" — "we cannot interfere with each other (unless you allow that)"*
- Put stateful databases in a container without proper volume and HA strategy. *Ref: "Containers"*

---

### Granularity of the FaaS Mapping

**Principle:** Pick the FaaS granularity that matches your change-rate and cohesion goals.

**Granularity ladder:**

| Level | Mapping | Pros | Cons |
|---|---|---|---|
| Function per microservice | One function = whole service | Simple, retains "microservice as unit of deploy" | Loses intra-service cohesion benefits of FaaS |
| Function per aggregate | Multiple functions, one per aggregate | Aggregates stay cohesive, independently deployable | Microservice becomes "logical" not "physical" |
| Function per state transition | One function per change | Maximum isolation | Reintroduces saga complexity for no benefit |

*Ref: "Mapping to microservices" — Figure 8-18/8-19*

**Do:** Default to function-per-microservice or function-per-aggregate. Hide the choice behind a coarser-grained interface. *Ref: "Mapping to microservices" — "I would strongly urge you to maintain a coarser-grained external interface"*

---

### Continuous Integration Done Right — Humble's Three Questions

**Principle:** You are not "doing CI" just because you have a CI tool.

**Humble's three questions:**
1. **Do you check in to mainline once per day?** Integrate frequently. If you have long-lived branches, you are delaying integration. *Ref: "Are You Really Doing CI?"*
2. **Do you have a suite of tests to validate your changes?** Tests = CI. Without tests, CI is just compilation. *Ref: "Are You Really Doing CI?"*
3. **When the build is broken, is it the #1 priority of the team to fix it?** Stop the line. Don't pile check-ins on top of a broken build. *Ref: "Are You Really Doing CI?"*

**Don't:**
- Confuse using a CI tool with doing CI (Jenkins ≠ CI). *Ref: "Are You Really Doing CI?"*
- Use "GitFlow" for closed-source teams — it optimizes for open-source trust dynamics. *Ref: "Branching Models"*

---

### Build Pipeline Stages — Concrete Example

**Principle:** Model the entire path to production as stages; use the same artifact throughout.

**Reference pipeline (Catalog service example):**
```
Stage 1: Compile + Unit Tests + Create Artifact (build-123)  ─┐
Stage 2: Slow Tests (uses build-123)                         │
Stage 3: Performance Tests (uses build-123)                 │ Same artifact
Stage 4: Manual UAT (uses build-123)                        │ throughout
Stage 5: Production Deploy (uses build-123)                  ─┘
```

*Ref: "Build Pipelines and Continuous Delivery" / Figure 7-1 / Figure 7-4*

**Do:**
- Create the artifact **once**, as early in the pipeline as possible. *Ref: "Artifact Creation"*
- Keep environment-specific config out of the artifact (DEBUG vs INFO logging, etc.). *Ref: "Artifact Creation"*
- Model manual stages (UAT) too — the CD tool supports hybrid pipelines. *Ref: "Tooling"*

---

### The Monorepo / Multirepo Trade-Off — Detailed Decision Framework

**Principle:** Both work in the right context. Choose by team size and tooling maturity.

| Context | Recommendation |
|---|---|
| < 20 devs, small codebase | Either works; pick what you know |
| 20–100 devs, multiple services | Multirepo (per-service repos + builds) |
| Hundreds of devs, like Google | Monorepo with custom tooling (Piper, Bazel) |
| Open source with untrusted committers | Monorepo + GitFlow-style branching |

*Ref: "Which Approach Would I Use?"*

**Why Newman prefers multirepo:**
- Cross-service changes become "a smell to investigate" rather than the norm. *Ref: "If you are continually making changes across multiple microservices, then your service boundaries might not be in the right place"*
- Organizations that started with monorepo and grew into the pattern's pain find migration cost-prohibitive (sunk-cost trap). *Ref: "Which Approach Would I Use?"*

**Monorepo hardening — if you must:**
- Use folder-based build triggers (changes to `user-service/` trigger only the User build). *Ref: Figure 7-10*
- Use **CODEOWNERS** (GitHub) to map ownership to paths. *Ref: Example 7-1*
- Adopt graph-based build tools (Bazel) if you hit scale issues. *Ref: "Mapping to build"*

---

### Deployment Environments — Calibration by Speed vs Production-Likeness

**Principle:** Earlier in the pipeline = faster feedback, less production-like. Later = more production-like, slower.

**Tuning matrix (MusicCorp Catalog example):**
| Env | Instances | Hardware | Goal |
|---|---|---|---|
| Dev laptop | 1 | Different from prod | Speed (build in seconds) |
| CI | 2 on same machine | Minimal | Fast test feedback |
| Preproduction | 4 across 2 DCs | Production-like | Catch integration issues |
| Production | N across 2+ DCs | Production | Real users |

*Ref: "Environments" / Figure 8-9*

**Do:** Fast feedback early (cheap to fix), production-like later (expensive to fix). *Ref: "Trade-Offs and Environments" / Figure 7-3*

---

### Database Choices in Microservices — Polyglot Persistence

**Principle:** Different microservices can (and often should) use different datastores.

**Datastore selection by use case:**
| Use case | Consider |
|---|---|
| Transactional, relational, mature tooling | PostgreSQL, MySQL |
| Graph traversal (social networks) | Neo4j, graph DB |
| Document-oriented, varied schemas | MongoDB, Couchbase |
| High-volume writes, eventual consistency | Cassandra, ScyllaDB |
| Time-series | InfluxDB, TimescaleDB |
| Search | Elasticsearch (with skepticism — see index-poisoning risk) |
| Caching | Redis, Memcached |

*Ref: "What About the Real World" — Netflix case study, Gilt scaling*

**Do:** Let each service pick the datastore that matches its access patterns. *Ref: "Technology Heterogeneity"*

**Don't:** Lock the entire organization into one datastore for consistency's sake if a use case clearly needs something different. *Ref: "Technology Heterogeneity"*

---

### Hot Paths — When Latency Demands Different Tech

**Principle:** Some functionality needs Rust/C++ for raw performance; the rest can stay on the JVM.

**Do:**
- Allow teams to pick the language/runtime when there's a measurable justification (Gilt moved from Ruby/Rails to JVM microservices to scale). *Ref: Gilt case study / Figure 13-6 (extracting Order)*
- Treat the choice as a "differentiator" not a "tax" — Netflix standardizes on the JVM precisely because they can't afford to debug bespoke failure-handling in 10 languages. *Ref: "Standardization"*

---

### Producer-Side Log Aggregation Architecture

**Principle:** Your microservice should not need to know it is being logged.

```
Microservice instance
    │ (writes to local filesystem)
    ▼
Local log shipper (Fluentd, Filebeat, Vector)
    │ (forwards batched)
    ▼
Log aggregation store (Elasticsearch, Humio, Loki, Splunk)
    │ (queried by)
    ▼
Operators / dashboards / alerting
```

*Ref: "Log Aggregation" / Figure 10-4*

**Do:**
- Let the microservice write to local filesystem only; the shipper handles routing. *Ref: "Log Aggregation"*
- Format logs at the source; don't have the shipper reformat on hot paths (CPU cost). *Ref: "Log Aggregation"*
- Pick a log format and standardize across services (date, time, microservice, log level, correlation ID in fixed positions). *Ref: "Common format"*

**Don't:** ship logs synchronously per-line; batch. *Ref: "Log Aggregation"*

---

### Correlation ID Propagation Pattern

**Principle:** A single ID traces a request across every service boundary.

**Mechanism:**
1. Gateway (or first hop) generates a unique ID (e.g., `abc-123`).
2. Every outbound call carries the ID (HTTP header, message metadata).
3. Every log line emitted by every downstream service includes the ID in a fixed position.
4. Aggregator queries `correlationId:abc-123` to reconstruct the entire call chain.

*Ref: "Correlating log lines" / Example 10-2 / Figure 10-6*

**Do:** Implement correlation IDs from day one — retrofitting them later is painful. *Ref: "Once you have log aggregation, get correlation IDs in as soon as possible"*

**Don't:** Assume clock-sync across machines for ordering. Use Lamport logical clocks or rely on the trace ID. *Ref: "Timing" / Leslie Lamport 1978*

---

### Span / Trace Model for Distributed Tracing

**Principle:** Local activity within a thread = span; correlated spans = trace.

**Anatomy:**
- **Span:** start time, end time, logs, key-value tags (customer_id, request_id, hostname, build_number)
- **Trace:** correlated set of spans sharing a trace ID
- **Sampling:** capture 1 in 1,000 by default (Jaeger); use dynamic sampling for errors and rare events (Honeycomb, Lightstep)

*Ref: "Distributed Tracing" / Figure 10-7 Honeycomb screenshot / "How it works"*

**Do:**
- Choose OpenTelemetry as the instrumentation API for portability. *Ref: "Implementing distributing tracing" / OpenTelemetry*
- Use a local agent (sidecar or in-process) for buffering and dynamic config. *Ref: "Implementing distributing tracing"*
- Run a central collector (Jaeger, Zipkin) for storage and querying.

**Don't:** Try to capture everything — sampling is required for system health. *Ref: "How it works" — "we need some form of sampling"*

---

### SLO / Error Budget Mechanics

**Principle:** An error budget makes reliability a tradeoff you can spend.

**Example:**
- SLO: 99.9% availability per quarter
- Quarter = ~90 days × 24h = 2,160 hours
- Error budget = 0.1% × 2,160 hours = 2.16 hours of downtime allowance per quarter

*Ref: "Error budgets"*

**Do:**
- Use error budget burn-rate to gate risky changes (new language, big refactor). *Ref: "Error budgets"*
- Make product owners aware of the budget — they decide whether to spend it on experimentation or save it. *Ref: "Error budgets" — "Error budgets are as much about giving teams breathing room to try new things"*

---

### Chaos Engineering Maturity Ladder

**Principle:** Don't jump to "unplug prod" before you have basic hygiene.

**Levels (in increasing maturity):**
1. **Baseline hardening** — health checks, retries, circuit breakers, bulkheads. *Ref: "Stability Patterns"*
2. **Game Days** — surprise exercises for people + process. *Ref: "Game Days"*
3. **Production experiments (controlled)** — Chaos Monkey / Litmus in non-critical environments first.
4. **Production experiments (broad)** — Chaos Gorilla (whole AZ), Latency Monkey.

*Ref: "Chaos Engineering" / "Game Days" / "Production Experiments"*

**Do:** Remember that chaos engineering is "the discipline of experimenting on a system to build confidence in the system's capability to withstand turbulent conditions in production" — discipline, not tool deployment. *Ref: "Chaos Engineering" — Principles of Chaos Engineering quote*

---

### Multi-Region and Data Sovereignty

**Principle:** Geographic partitioning can be mandatory (GDPR) or tactical (latency reduction).

**Do:**
- Treat geographic partitioning as a **data decomposition** axis when the data legally cannot leave a jurisdiction (EU citizen data). *Ref: "Limitations" — "if you need to ensure that data cannot leave certain jurisdictions"*
- Deploy across multiple AZs inside a single region for AWS — single AZ has no SLA. *Ref: "Spreading Your Risk"*
- Consider a federated Kubernetes model (multiple clusters) when organizational/geographic boundaries demand it. *Ref: Figure 8-24*

**Don't:** Assume "multi-region" = "more reliable." Multi-region adds complexity and consistency challenges. Match the deployment to the requirement. *Ref: "Spreading Your Risk"*

---

### Saga Compensations — Semantic, Not Mechanical

**Principle:** Compensating transactions are new transactions that *revert* prior effects, not undo operations.

**MusicCorp order example:**
- Original: `TakePayment → ReserveStock → AwardPoints → DispatchPackage`
- Stock not found at dispatch → Compensate: `CancelPayment → ReleaseStock → RevokePoints` (but the email confirming dispatch was already sent — send a second email apologizing).

*Ref: "Saga rollbacks" / Figure 6-7*

**Do:**
- Recognize that some side effects cannot be undone (emails sent, third-party APIs called) — the compensation is a new, opposite effect. *Ref: "Saga rollbacks" — "we cannot roll back time"*
- Reorder saga steps to push high-failure-risk steps earlier and irreversible side effects later. *Ref: "Reordering workflow steps to reduce rollbacks" / Figure 6-8*

**Don't:**
- Try to make compensations atomic. They are new business events, not rollbacks. *Ref: "Saga rollbacks"*

---

### Saga State Reconstruction — The Correlation-ID Service

**Principle:** In choreographed sagas, you can't see state from a single microservice — build a view.

**Pattern:**
- Every saga event carries a correlation ID.
- A separate saga-view service subscribes to all events, projects state per saga, exposes status queries.
- Operations dashboard reads saga-view to show "where is order 123?"

*Ref: "Choreographed sagas"*

**Do:** This is the *only* sane way to debug choreographed sagas. Without it, you grep logs across services. *Ref: "The lack of a central place to interrogate around the status of a saga is a big problem"*

---

### Spring Boot / Service Template — Optional, Not Mandated

**Principle:** A tailored microservice template makes the right thing easy; mandatory templates become bloated frameworks.

**Do:**
- Provide a template that handles the **standard requirements** out of the box: health checks, metrics, circuit breakers, JWT validation. *Ref: "Tailored Microservice Template"*
- Treat the template as an **internal open source** project — teams contribute back. *Ref: "Caution warranted"*
- Allow teams to **fork the template** if they need something different (realestate.com.au copies it per-service). *Ref: "DRY and the Perils of Code Reuse in a Microservice World"*

**Don't:** Mandate a template that doesn't earn its keep. Developers will work around it. *Ref: "Caution warranted" — "I have seen many a team's morale and productivity destroyed by having a mandated framework thrust upon it"*

---

### Cross-Functional Requirements in CFRs

**Principle:** Non-functional requirements are functional — they require cross-cutting work.

**Sarah Taraporewalla's preferred term: CFRs.** *Ref: "Cross-Functional Testing"*

**Examples of CFRs:**
- Acceptable latency (e.g., 2s p90 at 200 concurrent users)
- Availability (24/7 SLA?)
- Durability of data (years of financial records, days of session logs)
- Throughput
- Security (encryption at rest, PII handling)
- Accessibility (WCAG, keyboard navigation)

*Ref: "Cross-Functional Testing"*

**Do:**
- Define CFRs per service (payment service needs 99.99% uptime, recommendation service can tolerate 10 min downtime). *Ref: "Cross-Functional Testing"*
- Track CFRs as SLOs that surface automatically. *Ref: "Are We Doing OK?"*
- Test CFRs in the pyramid too — HTML accessibility markup can be tested with fast unit tests. *Ref: "Cross-Functional Testing"*

---

### The Microservice "Required Standard" Checklist

**Principle:** Each microservice must be a "good citizen" so one bad apple doesn't poison the system.

**Mandatory behaviors:**
- Emits standardized health/monitoring metrics.
- Logs in standard format, with correlation IDs.
- Implements circuit breakers around downstream calls.
- Uses consistent error semantics (HTTP 4xx vs 5xx; or equivalent).
- Reports health endpoint for load balancers.
- Implements graceful degradation when dependencies are unhealthy.

*Ref: "The Required Standard"*

**Do:** Write these as a **paved road** — exemplars + template + tests that fail if a microservice deviates. *Ref: "Exemplars" / "Tailored Microservice Template"*

---

### Exception Handling — Track Deviations, Update the Rules

**Principle:** When teams routinely deviate from a rule, the rule is probably wrong.

**Mechanism:**
- Log exceptions to a centralized registry.
- Quarterly review: are 80% of exceptions in the same area? Time to update the principle.
- Example: "Always use MySQL" → "Use MySQL except for > 1TB scale, where Cassandra is appropriate." *Ref: "Exception Handling"*

**Do:** Use exceptions as data about your own guidelines. *Ref: "Exception Handling"*

**Don't:** Punish teams for exceptions. Use them as learning signals. *Ref: "Exception Handling"*

---

### Conway's Law — The Microsoft Vista Evidence in Detail

**Principle:** Org metrics predicted Vista quality better than code metrics.

**Study details:**
- Looked at error-proneness of Windows Vista components.
- Considered many technical metrics (code complexity, churn, dependencies).
- Found that **organizational metrics** (number of engineers per component) were the strongest predictor.
- Vista was famously error-prone → consistent with the finding.

*Ref: "Evidence" — Nagappan, Murphy, Basili 2008 ICSE*

**Implication:** Restructuring teams is more impactful than restructuring code, when seeking quality improvements.

---

### Conway's Law — Loose vs. Tight Coupling Empirical Study

**Principle:** Organizational coupling predicts software coupling.

**Study (MacCormack/Baldwin/Rusnak 2012):**
- Compared similar product pairs from "loosely coupled" (open source) vs. "tightly coupled" (commercial product firms) orgs.
- Loosely coupled orgs produced **more modular, less coupled software**.
- Tightly coupled orgs produced the opposite.

*Ref: "Evidence"*

**Implication:** If you want a loosely coupled architecture, you must first accept a loosely coupled organization.

---

### The Two-Pizza Team Origin Story

**Principle:** Amazon's 5–10 person team constraint was a forcing function for service independence.

**Context:** Bezos wanted teams to own their services end-to-end without central coordination. The two-pizza rule wasn't about pizza — it was about ensuring teams stayed small enough to communicate face-to-face and self-coordinate. This drove:
- The creation of AWS (so teams could self-provision infrastructure).
- Service ownership at the team level.
- Standardized interfaces (so teams could consume each other without meetings).

*Ref: "Netflix and Amazon" / "Think Like Amazon" — Rossman*

---

### The Spotify Model — What It Was and Wasn't

**Principle:** "Spotify model" was a misunderstood snapshot of an internal org at one moment.

**Reality (per Newman's source):** Even Spotify doesn't use "the Spotify model" anymore. Squads/tribes/chapters/guilds were useful inspiration but copying them without context produced dysfunction.

**Do:** Learn from others, but understand the why before copying. *Ref: "On Autonomy" — "copying what someone else does and expecting the same results, without actually understanding *why* the other organization does the things it does, may not result in the outcome you want"*

---

### Architectural Fitness Functions

**Principle:** Architectural properties should be measured continuously, like unit tests.

**Examples:**
- Performance: every build verifies p95 latency < 100ms in a representative load test.
- Coupling: static analysis ensures no service imports another service's internal types.
- Modularity: cyclomatic complexity, dependency fan-in/fan-out within budget.
- Security: every container image scanned for CVEs above threshold.

*Ref: "Guiding an Evolutionary Architecture" — Building Evolutionary Architectures, Ford/Parsons/Kua*

**Do:** Implement fitness functions in CI so the architectural property is enforced automatically. *Ref: "Fitness functions work best when combined with close collaboration with the people building the system"*

---

### The Architect's Bike-Riding Analogy

**Principle:** Step in only for the duck pond or the oncoming truck.

**Quote:** "Think about teaching a child to ride a bike. You can't ride it for them. You watch them wobble, but if you step in every time it looks like they might fall off, then they'll never learn... But if you see them about to veer into traffic or into a nearby duck pond, then you have to step in." *Ref: "Architecture in a Stream-Aligned Organization"*

**Do:** Default to letting the team decide. Reserve overrides for genuine existential risks, not taste differences.

---

### Capabilities, Not Stories — Framing Architecture Work

**Principle:** Architectures should support user-visible capabilities, not internal layering.

**Do:**
- Frame work as "what user outcome does this enable?" — not "we need a new service." *Ref: Newman generally*
- When reviewing proposed changes, ask "what capability does this preserve or extend?"
- Avoid architecturally pure refactors that don't unlock a user-visible outcome. *Ref: "Technical Debt"*

---

### The Afterword's "Microservices 101" Distilled

**Principle:** A condensed checklist from the book's final chapter.

**The book's own TL;DR (paraphrased):**

1. **What are microservices?** Independently deployable services modeled around business domains, with their own state, hidden internals, and stable interfaces. *Ref: Afterword "What Are Microservices?"*

2. **Move to microservices incrementally.** Identify a goal; chip away; never big-bang rewrite. *Ref: Afterword "Moving to Microservices"*

3. **Communication styles** — sync for short request-response, async for everything else. Mix as needed. *Ref: Afterword "Communication Styles"*

4. **Workflow** — use sagas, not distributed transactions. *Ref: Afterword "Workflow"*

5. **Build** — one CI pipeline per microservice. Avoid monorepo coupling. *Ref: Afterword "Build"*

6. **Deployment** — one process per service, isolated, containerized. Use FaaS or K8s as appropriate. *Ref: Afterword "Deployment"*

7. **Testing** — pyramid with unit/service/e2e; replace e2e with CDCs + in-prod as you scale. *Ref: Afterword "Testing"*

8. **Monitoring/observability** — focus on the property (observability), not the activity (monitoring). High-cardinality tools win. *Ref: Afterword "Monitoring and Observability"*

9. **Security** — defense in depth, least privilege, zero-trust when data is sensitive. *Ref: Afterword "Security"*

10. **Resiliency** — bulkheads, circuit breakers, timeouts for robustness; people + culture for sustained adaptability. *Ref: Afterword "Resiliency"*

11. **Scaling** — vertical → horizontal → partitioning → decomposition. *Ref: Afterword "Scaling"*

12. **UIs** — break them apart; use BFF or GraphQL for aggregation. *Ref: Afterword "User Interfaces"*

13. **Organization** — stream-aligned teams, enabling teams, paved-road platform. *Ref: Afterword "Organization"*

14. **Architecture** — town planner, not ivory tower; principles + fitness functions; embed with teams. *Ref: Afterword "Architecture"*

**The book's own final words:**
> "Microservice architectures give you more options, and more decisions to make. Making decisions in this world is a far more common activity than in simpler, monolithic systems. You won't get all of these decisions right, I can guarantee that. So, knowing you are going to get some things wrong, what are your options? Well, I would suggest finding ways to make each decision small in scope... Think not of big-bang rewrites, but instead of a series of changes made to your system over time to keep it supple." *Ref: "Final Words"*

---

### Microservices vs. Mainstream Adoption — A Frank Postscript

**Principle:** Microservices have gone mainstream — both rightly and wrongly.

**Newman's concern (paraphrased from Afterword):** Many teams adopt microservices because "everyone else is doing it," not because they're a fit. Expect:
- More horror stories (failure cases being slowly collected).
- A backlash at some point.
- Technology vendors selling complexity dressed as solutions.

**Mitigations:**
- Apply critical thinking to your context.
- Start with a monolith if you can.
- Reach for microservices when the goal justifies the complexity. *Ref: "Looking Forward"*

---

### The Case Study Lineup — When to Reference Each

| Case study | When to invoke |
|---|---|
| MusicCorp | Fictional but illustrative — domain modeling, bounded contexts, saga rollback |
| AdvertCorp (turnip ads) | Latency kills, bulkheads, circuit breakers, timeouts |
| PaymentCo (PCI) | Data-driven decomposition, regulatory scoping |
| FoodCo | Vertical → horizontal → partitioning → decomposition progression |
| Gilt | Rails monolith → 450 microservices on JVM |
| Snap CI | Premature decomposition recovery (microservice → monolith → microservice) |
| REA | Stream-aligned teams, delivery services team, strong ownership, LOB-based integration |
| realestate.com.au | Tailored service template copied per-service, delivery support team |
| FinanceCo | Multi-team shared service (the Wishlist-style saga example) |
| PaymentCo | PCI Level 1 audit scope reduction via zoning |
| Monzo | Service mesh migration (Linkerd v1 → Envoy-based internal mesh) |
| Comcast | Architecture Guild (IETF-inspired cross-team governance) |
| BBC | Lambda + EC2 mix — FaaS where it fits |
| Netflix | Chaos Monkey / Simian Army; Cassandra standardization |
| Gilt | 6,000–7,000 RPS at peak; cache-heavy |
| Tyro (Dave Coombes) | Microservice migration lessons |
| Uswitch / RVU | Kubernetes adoption to enable organizational change |
| Money Supermarket (Dave Halsey) | Microservice migration lessons |
| Lloyds Banking Group (Sarah Wells at FT) | Zero-downtime deployment for delivery velocity |
| Capital One | mountebank for performance-test mocking |
| Bustle | FaaS scaling mismatch with Redis |
| Code Spaces | Backups in same compromised AWS account = total loss |
| Telstra | Blame culture + human-error postmortems = recurring outages |
| Equifax | $700M settlement from unpatched Apache Struts |
| CNN | 7.9 MB page weight (large-micro-frontend bloat) |
| Slack | Public ZTS work, etc. |

*Ref: Throughout the book*

---

### Distributed Transactions vs. Sagas — Detailed Comparison

**Principle:** Sagas always win for cross-service business processes.

| Property | Distributed transactions (2PC) | Sagas |
|---|---|---|
| Atomicity | True ACID (with isolation caveats) | Compensating actions; no atomicity at saga level |
| Failure mode | Stall on any node failure → entire transaction blocked | Each step fails independently; saga decides next action |
| Latency | Locks held for full duration; long pauses | Local transactions only; fast |
| Coupling | Tight — all participants must agree | Loose — each step is a local concern |
| Tooling | Database-internal | Application-level; requires explicit coordination |
| Use case | Single logical database spanning machines (Spanner) | Cross-microservice business processes |

*Ref: "Distributed Transactions—Just Say No" / "Sagas" / Pat Helland quote*

**Do:** Use sagas for any cross-microservice business process. Reserve 2PC for genuinely single-database-with-multi-machine scenarios (rare).

---

### Saga Failure Recovery — Forward vs. Backward

**Principle:** Sagas support both forward and backward recovery.

| Recovery type | When | How |
|---|---|---|
| Backward (compensate) | Irrecoverable error at a step | Trigger compensating transactions for each completed step |
| Forward (retry) | Transient error | Retry the failing step (with backoff and retry limit) |

*Ref: "Saga Failure Modes" / Garcia-Molina & Salem*

**MusicCorp order example — mixed recovery:**
- Stock find fails → **fail backward**: compensate payment + loyalty.
- Courier dispatch fails (no space) → **fail forward**: queue for tomorrow, escalate to humans if persistent.

*Ref: "Mixing fail-backward and fail-forward situations"*

---

### Saga vs. Distributed Transactions — Detailed Trade-Offs

**Principle:** Sagas give you eventual consistency, not transactional consistency.

**Comparison:**
| Aspect | Sagas | 2PC |
|---|---|---|
| Consistency | Eventual (with intermediate inconsistent states) | Stronger (but not full ACID isolation) |
| Resource locks | None held across the saga | Locks held across all participants |
| Failure handling | Each step has explicit compensation | Requires all-or-nothing abort |
| Coupling | Each service independent | All participants in tight coordination |
| Suitable for | Long-running business processes | Short, fast cross-resource operations |

*Ref: "Sagas Versus Distributed Transactions"*

**When to use which:**
- 2PC: rare cases where you genuinely need atomicity across machines of a single logical database (Spanner-class).
- Sagas: everything else across microservices.

---

### Workflow Anti-Pattern: The Anemic Service

**Principle:** Centralized logic turns services into CRUD wrappers.

**The danger:** "If this begins to happen, you may find that your services become anemic, with little behavior of their own, just taking orders from orchestrators." *Ref: "Orchestrated sagas"*

**Do:**
- Have the orchestrator send a *request* (which the service can reject), not a *command* (which implies obedience). *Ref: "Commands Versus Requests"*
- Keep significant business logic in the services themselves. *Ref: "Orchestrated sagas" — "ensure that your services still play a role"*
- Use different orchestrators for different flows (Order Processor for placing orders, Returns for returns, Goods Receiving for stock receipt) so logic stays distributed. *Ref: "Orchestrated sagas"*

---

### Workflow Anti-Pattern: The Distributed Monolith Saga

**Principle:** Sagas that span teams without clear ownership become coordination nightmares.

**The anti-pattern:**
- Team A owns order placement.
- Team B owns payment.
- Team C owns inventory.
- Team D owns loyalty.
- They all must coordinate on a saga.
- Each team's release cadence conflicts with others'.
- The saga becomes effectively a distributed monolith.

**Do:**
- When one team owns the whole saga → orchestrate.
- When multiple teams own parts → choreograph (or break the saga into smaller owned pieces).
- Make the saga owner explicit in service contracts. *Ref: "Should I use choreography or orchestration"*

---

### Avoiding CAP Confusion — Consistency Levels

**Principle:** CAP is binary in failure, nuanced in normal operation.

**Cassandra consistency levels (illustrative):**
- `ALL`: wait for all replicas — strongest, slowest
- `QUORUM`: wait for majority — balanced
- `ONE`: wait for any single replica — fastest, weakest

*Ref: "It's Not All or Nothing"*

**Do:** Pick the right consistency level per operation, not per service. *Ref: "It's Not All or Nothing"*

---

### Real-World Failure Pattern — "Slowness Kills"

**Principle:** Slow downstream services are worse than unavailable ones.

**Mechanism:**
- Slow service holds connections open.
- Caller waits (timeout-bound).
- Caller's connection pool exhausts.
- New requests can't even try.
- Cascading failure.

*Ref: "Time-Outs" / AdvertCorp story*

**Mitigations (all together):**
- Aggressive timeouts (advertising 30s → 1s in AdvertCorp).
- Per-downstream bulkheads (separate connection pools).
- Circuit breakers (fail fast after N failures).
- Graceful degradation (degrade rather than block).

---

### Database Lock Contention — Beyond 2PC

**Principle:** Multi-master replication locks across data centers are extremely hard to coordinate.

**Pattern (MusicCorp-style inventory):**
```
DC1: primary node (writes)
DC2: read replica (reads)
  ↓ replication
```

*Ref: "Database deployment and scaling" / Figure 8-5*

**Do:**
- Use read replicas for read scaling.
- Accept that the replica is eventually consistent (replication lag).
- For write-heavy multi-region, use Cassandra-style AP designs, not relational CP. *Ref: "Data Partitioning"*

---

### Saga State Visibility — Three Approaches

**Principle:** Without state visibility, choreographed sagas are undebuggable.

| Approach | Pros | Cons |
|---|---|---|
| Central orchestrator state | Easy to query, single source of truth | Couples services to orchestrator |
| Correlation IDs + log queries | No coupling | Requires log aggregation infrastructure |
| Dedicated saga-view service (event projector) | Decoupled, rich queries | Extra service to run; possible lag |

*Ref: "Choreographed sagas"*

**Do:** The third option is the most sustainable at scale.

---

### Event Storming Logistics — Practical Tips

**Principle:** Event storming is a workshop, not an architect's solo activity.

**Logistics from Newman's account:**
- Get everyone in a room. *Ref: "Event Storming"*
- Remove chairs (or don't). *Ref: "Event Storming" — "as someone with a bad back, while this strategy is something I understand, I recognize that it may not work for everyone"*
- Use brown paper on walls, sticky notes in color-coded conventions. *Ref: "Event Storming"*
- One disagreement: orange sticky notes are surprisingly hard to source; consider alternatives. *Ref: "Event Storming" — "I have another disagreement with Alberto's structure"*
- Avoid letting current implementation warp the model. *Ref: "Event Storming" — "don't let any current implementation warp the perception of what the domain is"*

**Sticky note colors (Brandolini convention):**
- Orange = domain events
- Blue = commands
- Yellow = aggregates
- (plus more for other concepts)

*Ref: "The process"*

---

### Aggregates Don't Want to Be Split

**Principle:** An aggregate is a single unit of consistency. Splitting it across microservices reintroduces 2PC problems.

**Why:** Aggregates have identity, state, and a managed life cycle. Splitting them means multiple services must coordinate to manage one aggregate's state — that's a saga waiting to happen.

**Do:** Keep an aggregate owned by one microservice. *Ref: "Mapping Aggregates and Bounded Contexts to Microservices"*

**Don't:** Break a single aggregate into multiple microservices just because you can. *Ref: "Get even more fine-grained" — "I struggle to see the value in adding this complexity at the level of managing a single aggregate"*

---

### The "Hidden Models" Pattern

**Principle:** Different contexts can have different models of the same concept.

**MusicCorp example:** Stock Item inside warehouse = name + shelf locations + quantity. Stock Item shared with finance = count + value. *Ref: "Hidden models" / Figure 2-15*

**Do:**
- Name shared models differently per context if they have different meanings.
- Avoid forcing one universal "Stock Item" model across the organization. *Ref: "Hidden models"*

---

### Conway's Law Reverse in Practice — The Print-to-Digital Pivot

**Principle:** A system's design, once in place, can shape the organization that grows around it.

**Case study (Newman):** A print firm originally built a 3-stage web pipeline (input, core, output). As digital overtook print, IT grew into 3 divisions matching the pipeline. The system design inadvertently shaped the org. *Ref: "Conway's Law in Reverse"*

**Do:** Recognize that early architectural decisions have organizational lock-in effects. *Ref: "Conway's Law in Reverse"*

---

### The Real-estate.com.au Case Study — Detailed

**Principle:** Delivery tooling must precede, not follow, microservice adoption.

**REA's journey (2010–2014):**
- Started with a handful of services.
- Heavy investment in delivery tooling (AWS, CI/CD pipelines).
- 3 months to get 2 microservices live (front-loading the investment).
- 3 months after that: 10–15 services.
- 18 months: 70+ services.

*Ref: REA case study / "Two case studies on the power of automation"*

**Key insight:** The first 3 months were infrastructure, not feature work. Without this front-loading, the subsequent scaling was impossible.

**Do:** Budget the first few months of microservice adoption as "infrastructure tax" — you will move slowly at first, then fast. *Ref: "Two case studies on the power of automation"*

---

### The Monzo Service Mesh Story

**Principle:** Service mesh adoption is iterative and painful, but enables polyglot microservices.

**Monzo's journey (per Newman's account):**
- Started with Linkerd v1 — worked well for their scale.
- Hit Linkerd v1's limits; needed to migrate.
- Built internal Envoy-based mesh.
- Migration was painful but necessary.

*Ref: "Service Meshes" — Monzo Linkerd v1 to Envoy anecdote*

**Do:**
- Expect to migrate mesh solutions at least once in your microservice journey.
- Use OpenTelemetry for portability. *Ref: "Implementing distributing tracing"*

---

### The Health Check Endpoint — Required, Not Optional

**Principle:** Every microservice must expose a health endpoint for load balancers and orchestrators.

**What goes in:**
- Liveness: "Am I running?"
- Readiness: "Am I ready to receive traffic?" (dependencies healthy)
- (Optional) Startup: "Have I finished initializing?"

*Ref: "Single Microservice, Multiple Servers"*

**Do:**
- Implement both liveness and readiness separately.
- Have readiness check downstream dependencies.
- Have liveness check only internal state (don't kill the pod if a downstream is down — that's readiness's job).

---

### Microservice Chassis / Sidecar Pattern

**Principle:** Cross-cutting concerns (logging, metrics, retries) can be pushed into a sidecar process.

**Service mesh as the modern implementation:**
- Envoy sidecar in each pod handles mTLS, retries, tracing. *Ref: "Service Meshes" / Figure 5-7*
- Your microservice no longer needs to implement these directly.

*Ref: "Service Meshes"*

**Do:**
- Use a service mesh when you have many services in different languages. *Ref: "Do you need one?"*
- Don't use one if you have 5 services. *Ref: "Do you need one?" — "it is arguable as to whether you can justify Kubernetes"*

---

### Observability Cost Trade-Offs

**Principle:** Observability has real costs (storage, query compute, ingest bandwidth).

**The Elasticsearch scaling trap:**
- The SaaS dev-tools team: 6 weeks of logs for one product exhausted the largest cluster they could run.
- Solution: continuous ingest-focused tools (Humio) over index-heavy stores.

*Ref: "Shortcomings"*

**Do:**
- Budget observability costs as part of your infrastructure spend.
- Sample, filter, or summarize where full fidelity isn't needed.
- Prefer ingestion-focused stores for high-volume logs.

---

### Self-Describing System — Beyond Documentation

**Principle:** Documentation rots; programmatic discovery doesn't.

**Build a humane registry:**
- Source code metadata (CODEOWNERS, service manifests) + service discovery (Consul/etcd) + health checks + deployment registry = single dashboard. *Ref: "The Self-Describing System"*
- Financial Times' Biz Ops + Spotify Backstage are the canonical examples. *Ref: Figures 5-8, 5-9*

**Do:** Treat the humane registry as a product, not a side project.

---

### HATEOAS — Why It Doesn't Matter in Practice

**Principle:** HATEOAS is theoretically appealing but rarely delivers value in microservices.

**Newman's honest assessment:** "Despite intellectually appreciating the goals behind HATEOAS, I haven't seen much evidence that the additional work to implement this style of REST delivers worthwhile benefits in the long run." *Ref: "REST" — HATEOAS section*

**Do:** Skip HATEOAS unless you have a specific reason to believe in it for your context.

---

### OpenAPI, AsyncAPI, CloudEvents — When to Use Each

**Principle:** Match the schema standard to the communication style.

| Style | Schema standard |
|---|---|
| REST request-response | OpenAPI (Swagger) |
| Event-driven async | AsyncAPI or CloudEvents (CNCF) |

*Ref: "Documenting Services" / "Explicit Schemas"*

**Do:**
- Use OpenAPI for REST — best tooling support.
- Use CloudEvents for events — broadest vendor support.
- Avoid the schemaless trap: even dynamic consumers have implicit expectations. *Ref: "Should You Use Schemas?"*

---

### DRY — The Microservices Edition

**Principle:** DRY is about *behavior and knowledge*, not code.

**When DRY hurts in microservices:**
- Sharing a Customer type library across Order and Customer services. Changing Customer.OrderHistoryLimit breaks Order. *Ref: "Sharing Code via Libraries"*
- Sharing a database schema. *Ref: "Common Coupling"*

**When DRY is fine:**
- Within a microservice.
- For transport/utility concerns (logging, metrics) that don't leak outside the service boundary.

*Ref: "DRY and the Perils of Code Reuse in a Microservice World"*

**Do:** Default to tolerating duplication across service boundaries. Extract only when you have three callers and the cost of duplication clearly exceeds the cost of coupling. *Ref: "Reuse and BFFs" — "rule of thumb"

---

### API Versioning — URIs vs. Headers

**Principle:** Either approach works; pick by team preference.

**URI versioning:**
- `/v1/customer/` vs `/v2/customer/`
- Pros: explicit, easy to route
- Cons: discourages opaque URI handling (REST ideal)

**Header versioning:**
- `Accept: application/vnd.myapi.v2+json`
- Pros: opaque URIs
- Cons: harder to debug, more header manipulation

*Ref: "Emulate the Old Interface"*

**Do:** Pick one, document it, use it consistently.

---

### Pact Workflow — Detailed

**Principle:** Consumer-driven contracts need a tool and a workflow.

**Steps:**
1. Consumer defines expectations via Pact DSL.
2. Local Pact mock server captures the contract as a JSON file.
3. Pact file is published (CI artifact repo or Pact Broker).
4. Producer picks up the file, replays the interactions, verifies responses.
5. Pact Broker tracks contract versions and consumer-provider relationships.

*Ref: "Pact"*

**Do:** Use the Pact Broker — its dependency-graph view alone justifies it.

---

### The Real Benefit of End-to-End Tests — Decreasing Returns

**Principle:** End-to-end tests have a diminishing return in distributed systems.

**Why:** As services multiply, the cartesian explosion of test scenarios and the brittleness from environmental dependencies (any service instance can fail) grow superlinearly. *Ref: "The Great Pile-Up"*

**Do:** Treat end-to-end tests as training wheels — useful at small scale, replaceable as you mature. *Ref: "The Final Word"*

---

### Testing in Production — Comprehensive List

| Technique | Purpose | When |
|---|---|---|
| Smoke test | Verify deployment worked | Every deploy |
| Canary release | Verify with real users in low-risk way | Every risky deploy |
| Parallel run | Verify equivalence with old implementation | Major refactor / migration |
| A/B test | Compare UX variants | UI/product decisions |
| Synthetic transaction | Detect breakage proactively | Always-on |
| Chaos experiment | Verify resilience | Periodic / on demand |
| Real user monitoring | Detect symptom-level issues | Always-on |

*Ref: "Testing in Production"*

---

### Performance Testing Pitfalls

**Principle:** Performance tests can be misleading.

**Traps:**
- Performance environment isn't production-like → false negatives/positives. *Ref: "Performance Tests"*
- Failing to look at results — surprising how common this is. *Ref: "Performance Tests"*
- Tests run on infrequent schedules (weekly/monthly) → hard to bisect regressions. *Ref: "Performance Tests"*

**Do:** Run a subset of performance tests daily. Fail builds on latency drift >X%. *Ref: "Performance Tests"*

---

### Idempotency Mechanics

**Principle:** Idempotent operations can be retried safely.

**Mechanism:** Add a natural-key identifier to the operation so the receiver can detect duplicates.

**Example — crediting loyalty points:**
```xml
<!-- Non-idempotent: re-execution adds 100 again -->
<credit>
  <amount>100</amount>
  <forAccount>1234</account>
</credit>

<!-- Idempotent: tied to specific order, re-execution is safe -->
<credit>
  <amount>100</amount>
  <forAccount>1234</account>
  <reason>
    <forPurchase>4567</forPurchase>
  </reason>
</credit>
```

*Ref: Example 12-1 vs 12-2*

**HTTP note:** GET, PUT, DELETE are defined as idempotent in the spec — but only if you handle them that way in code. *Ref: "Idempotency"*

---

### Stability Pattern Combinations

**Principle:** Patterns work best in combination.

**The AdvertCorp fix bundle:**
1. Pool-wait timeouts enabled.
2. Aggressive per-call timeouts (30s → 1s).
3. Separate connection pools per downstream (bulkheads).
4. Circuit breakers per downstream (fail fast + auto-recovery).
5. Graceful degradation in UI (turnip ads show "unavailable" message).

*Ref: "Time-Outs" / "Bulkheads" / "Circuit Breakers"*

**Do:** Apply patterns as a bundle, not piecemeal. Each one addresses a different failure mode.

---

### Bulkhead Sizing

**Principle:** Bulkhead sizes should be tuned to expected traffic, not set arbitrarily.

**Trade-off:**
- Too small → false positives (legitimate requests rejected under load)
- Too large → wasted resources (you'd need a circuit breaker too)

*Ref: "Bulkheads"*

**Do:** Start with the pool size that handles 2x normal peak, add circuit breaker, iterate based on production behavior.

---

### Circuit Breaker State Transitions — Concrete

**Principle:** Circuit breakers have three states, with timing.

```
Closed (normal) —→ failures exceed threshold —→ Open (fail fast)
   ↑                                                  │
   └──── cool-down elapsed + probe succeeds ←──── Half-Open (test)
```

*Ref: "Circuit Breakers" / Figure 12-5*

**Do:**
- Tune threshold (e.g., 5 consecutive timeouts).
- Set cool-down (e.g., 30 seconds).
- Use the half-open state to probe recovery without flooding a still-broken service.

---

### Cache Invalidation Strategy Selection

**Principle:** Pick the simplest invalidation that meets your staleness budget.

| Strategy | Staleness window | Complexity |
|---|---|---|
| TTL | Up to TTL duration | Lowest |
| Conditional GET | Per-check (must re-fetch) | Low |
| Notification (events) | Propagation time + processing | High |

*Ref: "Invalidation"*

**Do:** Start with TTL. Add conditional GET when regeneration cost is high. Move to notification only when staleness windows are unacceptable.

---

### The Write-Through vs. Write-Behind Decision

**Principle:** Each cache update direction has trade-offs.

| Direction | Consistency | Complexity | Failure mode |
|---|---|---|---|
| Write-through | Strong | High (atomicity required) | Origin write fails → cache wrong |
| Write-behind | Eventual | Lower | Cache write fails → data loss |
| Cache-aside | Eventual | Lowest | Caller must handle cache misses |

*Ref: "Write-through" / "Write-behind"*

**Do:** Server-side write-through for minimum staleness. Cache-aside for client-side. Avoid write-behind in microservices (origin ambiguity). *Ref: "Write-behind"*

---

### The Four "Reasons for Microservices"

**Principle:** Be explicit about which benefits you are optimizing for.

**Top reasons from Newman's account:**
1. **Independent deployability** → team autonomy, faster delivery
2. **Data isolation** → better security/compliance scoping
3. **Technology heterogeneity** → right tool for each job
4. **Scaling** → scale what needs scaling, not the whole app

**Less common but valid:**
- Robustness (bulkhead isolation)
- Organizational alignment (Conway's law)
- Composability (recombine services for new products)

*Ref: "Advantages of Microservices"*

**Do:** If you can't name a reason beyond "everyone else is doing it," stay with the monolith.

---

### Microservice Tax — The Hidden Cost

**Principle:** Microservices impose a tax before delivering benefits.

**Components of the tax:**
- Deployment infrastructure
- CI/CD pipeline per service
- Service discovery
- Observability infrastructure
- Distributed tracing
- Schema registries
- Service mesh (eventually)
- Team training

*Ref: "Microservice Pain Points"*

**Do:** Budget for the tax explicitly. If the benefit doesn't justify the tax, don't adopt. *Ref: "Microservice tax" / "Whom They Might Not Work For"*

---

### Anti-Pattern Audit — Quick Checklist

Run this against your proposed or existing microservice architecture:

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Distributed monolith | All services deploy together | Find and break the coupling |
| Shared DB | Multiple services query same DB | Split data ownership |
| Content coupling | Service A reaches into Service B's DB | Route through B's API |
| Lockstep deploy | Consumer + producer forced to ship together | CDCs + expand-contract |
| Central orchestrator over-control | Services are anemic CRUD wrappers | Push logic into services |
| Mega-monorepo | Cross-service changes are routine | Split into per-service repos |
| Hype-driven adoption | No clear goal beyond "modern" | Write down the goal; revisit |
| Inverted test pyramid | Slow e2e, no units | Push tests down the pyramid |
| Manual ops at scale | Pager burnout, slow deploys | Invest in automation early |

*Ref: Throughout the book*

---

### The Decision Pattern — Small Scope, Frequent Reversal

**Principle:** Make each architectural decision small in scope so reversals are cheap.

**From the book's final words:** "I would suggest finding ways to make each decision small in scope; that way, if you get one wrong, you impact only a small part of your system. Learn to embrace the concept of evolutionary architecture, in which your system bends and flexes and changes over time as you learn new things." *Ref: "Final Words"*

**Do:**
- Prefer extract-and-rename over big rewrites.
- Prefer per-team decisions over org-wide mandates.
- Prefer multiple small experiments over one big bet.

---

### The Five Words to Memorize

From the book, the five most important words for microservice architects:

1. **Independent deployability** — the defining characteristic.
2. **Information hiding** — the foundational principle.
3. **Don't share databases** — the most violated rule.
4. **Incremental migration** — the only safe path.
5. **Stream-aligned teams** — the org structure that unlocks everything else.

*Ref: Throughout the book, especially the Afterword*

---

### Single Source of Truth — Bibliographic

**Authoritative sources cited by the book:**

- *Domain-Driven Design* — Eric Evans (2004)
- *Domain-Driven Design Distilled* — Vaughn Vernon (2016)
- *Implementing Domain-Driven Design* — Vaughn Vernon (2013)
- *Monolith to Microservices* — Sam Newman (2019) — Newman's companion deep-dive
- *Accelerate* — Nicole Forsgren, Jez Humble, Gene Kim (2018)
- *Team Topologies* — Matthew Skelton, Manuel Pais (2019) — described by Newman as "one of the two most useful books on software development written in the last ten years"
- *Building Evolutionary Architectures* — Neal Ford, Rebecca Parsons, Patrick Kua (2017)
- *Continuous Delivery* — Jez Humble, David Farley (2010)
- *Release It!* — Michael Nygard (2018) — bulkhead + circuit breaker origins
- *Enterprise Integration Patterns* — Gregor Hohpe, Bobby Woolf (2003)
- *Observability Engineering* — Charity Majors, Liz Fong-Jones, George Miranda (2022)
- *Site Reliability Engineering* — Betsy Beyer et al. (2016)
- *Designing Data-Intensive Applications* — Martin Kleppmann (2017)
- *The Art of Scalability* — Martin Abbott, Michael Fisher (2015) — Scale Cube
- *Software Architecture Elevator* — Gregor Hohpe (2020)
- *Practical Process Automation* — Bernd Ruecker (2021) — orchestration patterns
- *Learning Chaos Engineering* — Russ Miles (2019)
- *Threat Modeling: Designing for Security* — Adam Shostack (2014)
- *REST in Practice* — Jim Webber, Savas Parastatidis, Ian Robinson (2010)

*Ref: Bibliography*