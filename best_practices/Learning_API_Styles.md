# Learning API Styles
**Author:** Lukasz Dynowski and Marcin Dulak
**Topic tags:** `#api` `#architecture`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Learning_API_Styles_-_Lukasz_Dynowski/Learning_API_Styles_-_Lukasz_Dynowski.md` · `summaries/Learning_API_Styles_-_Lukasz_Dynowski.md`

## TL;DR
A hands-on, comparative deep-dive into the dominant network API styles (REST, GraphQL, Web Feeds/Atom, gRPC, Webhooks, WebSocket, broker-based with RabbitMQ). It frames APIs as products, lays out the full lifecycle, grounds every style in the network protocols it depends on, and gives working code in Python (Django, Starlette) so you can compare trade-offs rather than slogans. Apply when you need to pick a style, design contracts around them, or evolve a multi-style API landscape without leaking one style's assumptions into another.

---

## Best Practices by Topic

### 1. Treat security as a force present in every lifecycle phase

**Principle:** Security is not a stage-gate at the end of the API lifecycle; it is a property of every planning, design, implementation, testing, deployment, and maintenance decision.

**Do:**
- Embed encryption, authentication, authorization, and input/output validation into design and implementation discussions.
- Treat every release artifact as something an attacker might consume; design as if the API will be exposed publicly even when it is internal today.
- Include security scanning and dependency/license checks in the CI pipeline so they run on every change.

**Don't:**
- Don't defer security to a "security phase" before release; reviewers will reject work or teams will disable checks.
- Don't assume "shadow APIs" won't be discovered; any unmanaged endpoint is a future incident.
- Don't promise confidentiality without proving it: data must be protected in transit, in processing, and at rest.

**Code:**
```text
A daily build and smoke test is among industry best practices.
- Shift-left DevSecOps pushes scanning into the platform so developers
  do not have to remember to run it. Use shift-down tooling where capacity
  for human shift-left is missing.
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Lifecycle" / "Testing" / "Deployment"*

---

### 2. Define the API as an interaction point, not as code or a URL

**Principle:** An API is the contract that separates behavior from implementation. The toll-gate/bridge analogy is the cleanest mental model: cities are the systems, the bridge is the network, the toll gate is the API style, the truck is the message.

**Do:**
- Treat the API as a discrete, self-contained interaction point; identify it by what flows in and out, not by which library wrote it.
- Specify the API before binding it to a technology stack so implementation churn does not break clients.
- Use the API to separate ownership of behaviour; the system behind it is owned by its provider.

**Don't:**
- Don't conflate "the API" with one specific implementation or with one running instance.
- Don't expose implementation details just because the database makes them convenient.
- Don't skip documentation drafts during early phases; "no time later" almost always means no documentation.

**Code:**
```text
"We define API as an interaction point that allows software components
to communicate. The API provides functionality without exposing the
underlying system's complexity; it separates system behavior from its
implementation details."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Is an API?"*

---

### 3. Speak the customer's language in URLs, schemas, fields, and errors

**Principle:** Names should be expressive, intuitive, pronounceable, consistent, and tested with real users before they ship.

**Do:**
- Use American English for naming by default unless the audience forces another dialect.
- Name resources with plural nouns in REST (`/orders/123`); allow verbs in GraphQL/gRPC where intent is clearer.
- Include units in field names where ambiguity exists (`timeoutMs` over `timeout`).

**Don't:**
- Don't lock in a name in production without feedback; renaming once clients depend on it is expensive.
- Don't reinvent vocabulary across APIs in the same domain; one model of `customer` should serve many services.
- Don't use cryptic abbreviations or framework-internal jargon in public endpoints.

**Code:**
```text
"Making a resource name singular or plural depends on the API style in
which they appear. In a REST API, the norm is to use resource-oriented
names and plurals — for example, /orders/123. On the other hand, GraphQL,
gRPC, and broker-based APIs typically follow the intent-oriented
approach..."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Naming" / "Resource-Oriented Versus Intent-Oriented APIs"*

---

### 4. Pick resource-oriented vs intent-oriented APIs deliberately

**Principle:** REST is declarative (verbs are HTTP verbs, the rest is the noun); gRPC is imperative (the method is the verb); GraphQL mixes the two (declarative queries, imperative mutations).

**Do:**
- Pick resource-oriented APIs when predictability and a small surface of HTTP verbs matter more than custom business operations.
- Pick intent-oriented APIs when each endpoint encodes a specific business action that doesn't fit a CRUD verb (`archiveUser`, `backupServer`, Stripe Payment Intents).
- Let the naming pattern align with the technology, not the other way around.

**Don't:**
- Don't pretend CRUD-HTTP can express every business operation; force-fitting "actions" into a noun is how REST APIs grow verbs in the body.
- Don't invent new HTTP verbs to support intent; extend the resource model with sub-resources or RPC layers instead.
- Don't mix styles blindly inside one API; one style per resource keeps clients sane.

**Code:**
```text
"Resource-oriented APIs focus on data. ... Intent-oriented APIs focus
on the goal of the operation performed on data. Interface names used by
the intent-oriented APIs typically include verbs — for example,
createUser, archiveUser, and backupServer. ... Declarative APIs focus
on the final state of a resource rather than the specific steps needed
to achieve that state. ... gRPC APIs can be thought of as imperative
because they focus on actions/procedures. ... GraphQL APIs are a mix of
declarative and imperative APIs with declarative queries and imperative
mutations."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Resource-Oriented Versus Intent-Oriented APIs"*

---

### 5. Apply the API-first strategy: specification before implementation

**Principle:** The API contract is the source of truth; implementation follows. This works best when the target users of the API can review the shape before code is written.

**Do:**
- Capture the API in OpenAPI (HTTP) or AsyncAPI (asynchronous) before writing the server.
- Generate documentation, mocks, client SDKs, and contract tests from the specification.
- Validate the spec with both implementers (feasibility) and consumers (fitness for purpose).

**Don't:**
- Don't start coding the implementation before the spec exists for greenfield APIs; you will leak implementation details into the contract.
- Don't treat the spec as "documentation that comes later" — it is the contract.
- Don't skip the joint review where implementers confirm the spec is buildable.

**Code:**
```yaml
# OpenAPI 3 fragment — promote to source of truth
openapi: 3.0.3
info:
  title: Weather Forecast Service
  version: 1.0.0
paths:
  /forecasts/{city}:
    get:
      parameters:
        - name: city
          in: path
          required: true
          schema: { type: string }
      responses:
        '200':
          description: 7-day forecast
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Forecast'
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API-First Approach"*

---

### 6. Capture functional and nonfunctional requirements before implementation

**Principle:** FRs (what it does) and NFRs (how well it does it, i.e., the "-ilities") drive every later decision. Naming is fuzzy on purpose: classifying a requirement drives whether design, prioritization, or risk conversation owns it.

**Do:**
- Insist on testable NFRs that name the -ility ("99.9% availability", "p95 latency < 200 ms").
- Re-classify FR/NFR ambiguities by asking: does it provide a function? Does it impact ilities? Does it constrain a process?
- Surface compliance constraints (GDPR, HIPAA, PCI) during planning, not after the demo.

**Don't:**
- Don't treat NFRs as second-class tickets; they accumulate silently and become the cause of late redesign.
- Don't classify a requirement by tribal memory; ask the four FL questions, write down the answer.

**Code:**
```text
"When facing dilemmas between FRs and NFRs, answer questions such as:
- Does the requirement provide a function?
- Does the requirement impact system *ilities*?
- Does the requirement force the system or function to operate in
  a certain way?
- Does the requirement relate to the input or output of the system?"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Functional and Nonfunctional Requirements"*

---

### 7. Plan the API before you write a line of code

**Principle:** Planning is the place where scope, audience, devices, scale, versioning, constraints, and comms channels are agreed. Skipping it is how code-first teams end up with under-designed APIs.

**Do:**
- Answer who, what, for whom, at what scale, with what constraints, on what channels before coding.
- Embed security and compliance into the requirement formulation, not later.
- Choose a versioning strategy up front (semver vs release date vs URL path); clients will plan around it.

**Don't:**
- Don't conflate "we know what we're building" with "we documented what we're building".
- Don't promise unrealistic availability when regulatory or operational constraints will override it.
- Don't pick a versioning scheme lazily; switching schemes mid-flight costs a major version of its own.

**Code:**
```text
"During the planning phase, answer the following questions:
- What is the API scope? ...
- Who are the API user devices? ...
- What are the requirements? ...
- What is the scale that the API should operate with? ...
- What versioning strategy should you use? ...
- Are there any constraints for the API? ...
- Are there already established communication channels for API users?"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Planning"*

---

### 8. Accept that abstractions leak; design for Hyrum's Law

**Principle:** Every nontrivial abstraction leaks (Spolsky's "Law of Leaky Abstractions"). With enough users, all observable behavior is depended on, whether the contract says so or not (Hyrum's Law).

**Do:**
- Treat the implicit interface (what users actually depend on) as part of the API surface.
- Capture regression tests for behavior, error strings, and orderings that are not formally promised.
- When changing an implicit behavior, run a deprecation dance even if the formal contract allows it.

**Don't:**
- Don't promise that "fixing" an undocumented behavior is a non-breaking change; you don't know who depends on it.
- Don't rely on the contract alone to preserve compatibility; observability and analytics of actual usage are the contract reality.
- Don't surprise power users with changes to error responses, timeouts, or pagination shape.

**Code:**
```text
"With a sufficient number of users of an API, it does not matter what
you promise in the contract: all observable behaviors of your system
will be depended on by somebody.
— Hyrum Wright, 2012

... All non-trivial abstractions, to some degree, are leaky.
— Joel Spolsky, 2002"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Interface Versus Implementation"*

---

### 9. Use OpenAPI/AsyncAPI to align interface and implementation

**Principle:** Keep the implementation and the interface synchronized by co-locating them: embed OpenAPI in the codebase, generate code skeletons from it, and run contract tests that prove the implementation still honours the spec.

**Do:**
- Keep the OpenAPI/AsyncAPI description in the same repo as the implementation that serves it.
- Generate types and routers from the spec when your stack supports it; manually-align only where generation fails.
- Run contract tests in CI that fail if the implementation diverges from the spec or vice versa.

**Don't:**
- Don't let the description live in a separate wiki that drifts.
- Don't "generate everything from the spec" when the build chain cannot keep pace; explicit annotations in the code are a valid co-source-of-truth.
- Don't skip the backwards-compatibility check when changing the spec.

**Code:**
```text
"One way to improve your chances of keeping the implementation and
interface synchronized is to integrate the interface description into
your implementation. For example, if you have an API description format
that represents the interface design, you can keep that file in your
code repository or even develop an automated test that verifies your
adherence to the interface. Taking this further, you can even generate
a code skeleton based on the description format — although that's
really only effective for the first release."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API-First Approach" / "Interface Versus Implementation"*

---

### 10. Map messages to the OSI layer and the protocol that carries them

**Principle:** In the OSI model, "message" is the application-layer unit. HTTP, XMPP, MQTT and others are application protocols; understanding the unit of exchange is the prerequisite to choosing an API style.

**Do:**
- Distinguish a discrete message (payload + metadata) from a streaming primitive in your design notes.
- Use HTTP `POST` for synchronous, multi-header requests; MQTT `PUBLISH` for IoT fan-out; XMPP for chat-style XML messages.
- Treat protocol choices as architecture: switching protocol mid-life is a rewrite, not a refactor.

**Don't:**
- Don't assume "we use HTTP" implies synchronous communication; `fetch()` is async from a JavaScript client.
- Don't pick a protocol because it is fashionable; pick the one whose primitives match your delivery semantics.
- Don't write style-agnostic "API code" that works on top of any protocol; the protocol leaks into the contract.

**Code:**
```http
POST /submit HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

comment=Hello
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Message"*

---

### 11. Match transmission mode (simplex / half-duplex / full-duplex) to the use case

**Principle:** Simplex is one-way; half-duplex is two-way but one direction at a time; full-duplex is two-way simultaneously. Picking the wrong one creates needless contention or wasted capacity.

**Do:**
- Use simplex for purely notification surfaces (logs, fire-and-forget telemetry).
- Use half-duplex when coordination is needed but concurrent reads/writes aren't.
- Use full-duplex (WebSocket, gRPC streams) for interactive sessions, live alerts, or bidirectional event streams.

**Don't:**
- Don't open a WebSocket just because "real-time is cool"; a long poll or SSE may be sufficient and cheaper.
- Don't assume HTTP is half-duplex; HTTP/2 multiplexes streams.
- Don't design simplex channels that need acks; add an out-of-band ack or move to half-duplex.

**Code:**
```text
"An example of a device that uses half-duplex mode is a walkie-talkie.
When communicating using a walkie-talkie, both parties must adhere to
a communication protocol (a set of vocabulary like 'over' and 'out')."
"A phone is an example of a device that communicates using full-duplex
mode. In a phone conversation, you can talk and be heard at the same time."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Transmission Modes"*

---

### 12. Choose synchronous or asynchronous communication by the consumer's needs

**Principle:** The communication style is dictated by the consumer's need to coordinate, not by the protocol. Two clients with the same protocol can run sync and async.

**Do:**
- Use synchronous when the next instruction of the caller depends on the response.
- Use asynchronous when the caller can do other work; pair with a callback, queue, or webhook.
- Match the timing model to the UX: API-as-glue often wants sync; API-as-product on mobile often wants async.

**Don't:**
- Don't block a UI thread on a network request you could have issued async.
- Don't issue an async fire-and-forget for a change the caller must verify; the caller is going to add a poll anyway.
- Don't confuse the request/response model with sync execution; `fetch()` from JavaScript is async even when the server responds immediately.

**Code:**
```text
"In synchronous, request-response communication, a sender sends a message
to the receiver and waits for the corresponding response. ... Meanwhile,
in asynchronous message delivery, a truck departs as soon as it
delivers the cargo. The acknowledging receipt is sent back later on a
different truck."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Synchronous and Asynchronous Communication Types"*

---

### 13. Pick the right API style using the comparative characteristics table

**Principle:** API styles differ on protocol, communication type, binary support, responsiveness, and development effort. Make the choice consciously using the Table 1-1 axes, not by language fandom.

**Do:**
- Score each candidate style on protocol fit, comms type fit, binary support, responsiveness, and team effort.
- Reuse the matrix when reviewing new service proposals.
- Document the style choice in the service's ADR (architectural decision record).

**Don't:**
- Don't pick gRPC for a public API where GraphQL or REST gives clients a cheaper on-ramp.
- Don't pick REST for sub-millisecond IoT events where MQTT is the native idiom.
- Don't pick feeds/syndication for transactional state change; use it for "continuously updated content".

**Code:**
```
|              | RESTful | Query | Web feed | RPC       |
|--------------|---------|-------|----------|-----------|
| Technology   | REST    | GraphQL | Atom   | gRPC      |
| Protocol     | HTTP    | HTTP[a] | HTTP  | HTTP      |
| Comm type    | Sync    | Sync   | Async   | Sync      |
| Binary       | Yes     | Partial | Partial | Yes       |
| Responsiveness| Medium  | Medium | Medium  | High      |
| Dev effort   | Medium  | Medium | Low     | High      |
[a] GraphQL can also use WebSocket.
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Are API Styles?" (Table 1-1)*

---

### 14. Use RESTful APIs only when you keep hypermedia honest

**Principle:** REST is the Fielding dissertation: client-server, stateless, cacheable, uniform interface, layered system, **code on demand** — and most importantly hypermedia-driven (HATEOAS). An API that omits hypermedia is not RESTful, it is HTTP-API.

**Do:**
- Add hypermedia links to enable client navigation without out-of-band URL knowledge.
- Use the standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) so caching and intermediaries work as designed.
- Lean on the correct status codes (200, 201, 204, 301, 304, 400, 401, 403, 404, 409, 422, 500, 503).

**Don't:**
- Don't call the API "RESTful" just because it speaks JSON over HTTP.
- Don't invent custom verbs on top of HTTP for business operations; use a sub-resource or RPC layer instead.
- Don't return 200 OK with `{ "error": "..." }`; use 4xx/5xx and RFC 7807 problem details.

**Code:**
```text
"RESTful APIs adhere to six constraints outlined in Roy Fielding's
dissertation. While many APIs claim to be RESTful, the reality is that
they omit the inclusion of hypermedia links, which is a requirement of
RESTful API design."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Are API Styles?" / REST*

---

### 15. Choose GraphQL when clients want flexible shapes

**Principle:** GraphQL exposes one endpoint and lets clients describe the shape they want. It is a Query API; pairs naturally with imperative mutations on the same schema.

**Do:**
- Use GraphQL when consumers want to avoid over-fetching or under-fetching.
- Design the schema to match your domain model, not your database tables.
- Implement persisted queries, query complexity limits, and depth limits to defend the server.

**Don't:**
- Don't expose GraphQL to consumers whose queries cannot be bounded; HTTP/JSON streaming or REST may be cheaper.
- Don't let clients make arbitrary mutations through one endpoint; mutations deserve governance.
- Don't skip schema-stitching or federation decisions up front; they retro-fit badly.

**Code:**
```graphql
# GraphQL query — client asks for the exact shape it needs
query WeatherForCity {
  forecast(city: "Krakow") {
    date
    temperatureC
    summary
  }
}
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Query-based" / "Resource-Oriented Versus Intent-Oriented APIs"*

---

### 16. Use Web Feeds (RSS/Atom) for continuously updated content

**Principle:** Web feeds deliver XML-structured, continuously updated content over HTTP. They are the canonical asynchronous fan-out from publisher to many readers.

**Do:**
- Use Atom (or RSS) for syndicating content where consumers benefit from pull-based polling.
- Honour HTTP caching semantics (`Etag`, `Last-Modified`) so polling costs almost nothing.
- Document the TTL of the feed so clients know how stale the data may be.

**Don't:**
- Don't use a feed for transactional state changes; use REST mutations.
- Don't push binary payloads through feeds; use attachment links and proper MIME types.
- Don't invent a custom XML schema when Atom already covers entries, authors, categories, and links.

**Code:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example Feed</title>
  <link href="http://example.org/"/>
  <updated>2025-07-18T08:00:00Z</updated>
  <entry>
    <title>Storm warning</title>
    <id>urn:uuid:60a76c80-d399-11e9-b23c-0</id>
    <updated>2025-07-18T08:00:00Z</updated>
    <summary>High winds expected</summary>
  </entry>
</feed>
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Web feed"*

---

### 17. Use gRPC when you need streaming, low overhead, and contract-first IPC

**Principle:** gRPC is RPC over HTTP/2 with Protobuf contracts. It dominates for service-to-service traffic where high responsiveness, binary efficiency, and bidirectional streaming matter.

**Do:**
- Use gRPC for synchronous, low-latency intra-cluster (or intra-VPC) traffic between services you control.
- Generate clients and servers from a single `.proto` so both sides share the contract.
- Use the four streaming modes (unary, server, client, bidirectional) where they buy you something over REST.

**Don't:**
- Don't expose gRPC to browsers without a gateway; the browser still does HTTP/1.1.
- Don't use Protobuf when consumers need human-readable on-wire data (JSON, JSONSchema, or OpenAPI is better).
- Don't pin clients to gRPC features (interceptors, metadata) without versioning them; semantic versioning on the wire is your responsibility.

**Code:**
```protobuf
syntax = "proto3";
package weather;

service WeatherService {
  rpc GetForecast (ForecastRequest) returns (ForecastResponse);
  rpc StreamAlerts (AlertRequest) returns (stream Alert);
}

message ForecastRequest { string city = 1; }
message ForecastResponse {
  string city = 1;
  repeated DailyForecast days = 2;
}
message DailyForecast {
  string date = 1;
  float temperature_c = 2;
  string summary = 3;
}
message AlertRequest  { string region = 1; }
message Alert         { string severity = 1; string message = 2; }
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "RPC" / "Remote Procedure Call"*

---

### 18. Use webhooks for callback-style event delivery

**Principle:** Webhooks are HTTP callbacks: the destination receives an HTTP `POST` from the source whenever an event fires. They combine the event-based model with HTTP transport — but without an intermediary broker.

**Do:**
- Use webhooks to push events to external consumers who cannot poll.
- Sign every webhook payload (HMAC) and document the verification algorithm.
- Make the destination URL configurable; allow per-callback timeouts, retries, and dead-letter handling.

**Don't:**
- Don't ignore the "no intermediary" aspect: webhooks need destination-side availability, retries, and dedup.
- Don't ship webhooks without a stable event schema and an upgrade path; the contract has to evolve.
- Don't expect an HTTP 200 to mean the consumer processed the event; only that it received it.

**Code:**
```text
"In callback APIs, we have two sides: a destination system that creates
and handles the callback (receives messages), and the source system
that calls the callback (sends messages). Every message sent from the
source to the destination system in callback APIs is expected to be
acknowledged. ... Commonly, webhooks are referred to as HTTP callbacks
because when an event occurs, the source system notifies the
destination system by sending a message with an HTTP POST request,
acting as a callback mechanism."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Callback"*

---

### 19. Use WebSocket for bidirectional, low-latency streams

**Principle:** WebSocket is a full-duplex, persistent connection over a single TCP socket. It is ideal for chat, live alerts, collaborative editing, or any session where the server may push.

**Do:**
- Use WebSocket when both sides want to push without polling.
- Implement heartbeats to keep idle connections alive and to detect half-open peers.
- Re-establish connection state on the client (resume from a session id) and replay missed events when feasible.

**Don't:**
- Don't use WebSocket as a replacement for HTTP when polling is acceptable; the connection cost is real.
- Don't forget authentication on the upgrade request — cookies, headers, or subprotocols must be present *before* 101 Switching Protocols.
- Don't rely on TCP alone for ordering guarantees across reconnects; design idempotent messages.

**Code:**
```text
"APIs implemented in this style allow exchanging the data between
client and server in both directions simultaneously (see full-duplex
transmission). APIs built with the WebSocket protocol or gRPC framework
belong to this category because both can exchange data between the
client and the server in a full-duplex mode."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Bidirectional"*

---

### 20. Use broker-based APIs when fan-out and durability matter

**Principle:** A broker (RabbitMQ, Kafka, ActiveMQ, MQTT) is an intermediary that decouples producers from consumers and survives message bursts. Pick a broker-backed API when one publisher has many subscribers, or when neither side can guarantee availability.

**Do:**
- Use a broker when at-least-once delivery and buffering of bursts matter.
- Define the message schema independently of the broker (e.g., Protobuf, Avro, JSON Schema).
- Treat queues, exchanges, and topics as an architecture decision; choose durable + persistent for transactional flows.

**Don't:**
- Don't use a broker as a request/response substitute; you will re-invent RPC with extra latency.
- Don't model identity with addresses inside the message; route on a key, not on a payload field.
- Don't make the queue schema a single point of failure; canonical message formats let consumers come and go.

**Code:**
```text
"APIs implemented in this style are characterized by messages passing
through an intermediary known as a broker. Broker-based APIs deliver
messages by using different protocols. There are many broker-based
messaging systems, including Apache ActiveMQ, Apache Kafka, and
RabbitMQ..."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Broker-based"*

---

### 21. Treat the API as a product, not as glue

**Principle:** "API mandate" shifted APIs from internal glue to financial building blocks. Treating the API as a product is the difference between underdesigned integrations and durable revenue channels.

**Do:**
- Assign an owner. Track adoption, error rates, response time, and power users.
- Build a developer portal (Backstage, Clutch, Cortex) for discoverability and onboarding.
- Decide monetization up front: pay-per-use, subscription, freemium, transaction fee, revenue share.

**Don't:**
- Don't ship a public API without a deprecation policy; reversal is expensive.
- Don't leave the API undocumented in the maintenance phase; "we'll document later" never happens.
- Don't promise revenue before you have observability and SLA enforcement.

**Code:**
```text
"To understand API as a product, you first need to realize that most
organizations treat APIs as an integration technology. This way of
thinking results in APIs that have limited value in terms of scope,
extensibility, and durability, leading to APIs that are underdesigned.
Such an API may be poorly documented and lack design standards,
versioning, and security, or extensibility may be an afterthought."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API as a Product" / "API Monetization"*

---

### 22. Pick a monetization model that matches usage predictability

**Principle:** Pay-per-use, subscription, freemium, transaction fee, and revenue sharing each fit different consumer behaviour. Choose by what users can predict and what they value.

**Do:**
- Pick pay-per-use when consumers cannot predict exact usage and you can meter accurately.
- Pick subscription when you want predictable revenue and can bundle tiers (more calls, more features).
- Pick freemium when network effect or word-of-mouth is part of the growth model.
- Pick transaction fee when each call corresponds to a unit of economic value (payments, bookings).
- Pick revenue sharing when a marketplace or affiliate flow is involved.

**Don't:**
- Don't quote a flat price for usage that can spike — the consumer will underestimate, you will inflate.
- Don't combine pay-per-use and subscription ambiguously; tiers should be predictable on both sides.
- Don't ship freemium with no path to paid; you've made the API a charity, not a product.

**Code:**
```text
"Generating revenues from APIs is called API monetization. There are
several monetization models:
* Pay-per-use
* Subscription
* Freemium
* Transaction fee
* Revenue sharing"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Monetization"*

---

### 23. Run the API lifecycle iteratively, not sequentially

**Principle:** Planning, design, implementation, testing, deployment, maintenance, and retirement are interconnected. "Enough design to move on" beats "big up-front design". Vertically slice the lifecycle to respond to change.

**Do:**
- Treat each phase as informing every other phase; implementation learns, design revises.
- Reference the ACED model (Awareness, Compliance, Engagement, Design) for iterate-not-cascade discipline.
- Run the lifecycle in vertical slices (one slice through all phases) rather than horizontal layers.

**Don't:**
- Don't gate implementation behind a frozen design; freeze it later, with evidence.
- Don't separate security from each phase; security lives in the design conversation.
- Don't defer documentation to the maintenance phase; software is "never finished until retired".

**Code:**
```text
"Often the phases in the API lifecycle (or SDLC) are interpreted as
independent and sequential. The reality is that they all are
interconnected and interact with one another. For example, the
implementation phase may reveal factors not taken into account during
the design phase, leading to changes in the original design."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Lifecycle"*

---

### 24. Match test type to agile testing quadrants

**Principle:** Q1 (technology-facing, team-supporting) is unit/component; Q2 (business-facing, team-supporting) is functional/system; Q3 (business-facing, product-critiquing) is exploratory/UAT; Q4 (technology-facing, product-critiquing) is security/performance.

**Do:**
- Keep Q1 fast and developer-owned.
- Make Q2 the safety net for FRs, automated where possible, manual where it isn't.
- Budget Q3 for UAT and exploratory — slow, judgement-heavy, valuable.
- Specialize Q4 tooling for security and performance.

**Don't:**
- Don't gate releases on Q3 if the failure modes in Q4 haven't been ruled out.
- Don't pretend exploratory testing is dead because you have automation; UAT catches spec gaps that unit tests don't.
- Don't confuse Q1 unit tests with Q3 user acceptance; a passing unit suite doesn't mean the user is satisfied.

**Code:**
```text
"Q1 and Q2 support the development process by ensuring that the
product is built according to FRs. Meanwhile, Q3 and Q4 focus on
evaluating the product to ensure it meets user needs and satisfies
NFRs."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Agile testing quadrants"*

---

### 25. Use integration tests with real services when possible

**Principle:** Integration tests catch the seams that unit tests cannot: database drivers, message-bus quirks, third-party edges. Container-orchestrated dependencies (Docker) make integration testing cheap; mocks are a fallback, not a default.

**Do:**
- Use Docker to spin databases, caches, and message queues that mirror production.
- For third-party APIs you cannot locally host, create a "record and replay" fixture from production responses and check against it.
- Treat integration tests as live collaboration with the implementation; pivot them when contracts change.

**Don't:**
- Don't mock what you can run; mocks are for things you cannot make local, not for laziness.
- Don't forget to clean up state between integration tests; shared databases will leak.
- Don't couple integration tests to your CI's ability to run Docker; provide a smoke variant.

**Code:**
```python
# Spin Postgres in Docker for a pytest integration suite
# (excerpted from the book's pattern of bringing up real services)
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def pg_url():
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Integration testing"*

---

### 26. Use contract testing for evolving consumer/provider pairs

**Principle:** Contract testing is regression testing against the API specification. Consumer-Driven Contracts (CDC) let consumers define the shape; Provider-Driven Contracts (PDC) let providers define it. Pick the model based on who has more leverage.

**Do:**
- Combine schema-based contract tests with record/replay of past requests/responses.
- Run contract tests in CI on both sides of every change.
- Use CDC when consumers are many or external; PDC when one provider owns many interfaces.

**Don't:**
- Don't rely on contract tests alone; cover the schema broadly but also fuzz inputs (defensive programming creates wide input space).
- Don't pin past contracts in stone; align them with the current published spec.
- Don't skip mutual negotiation of the contract; consumers and providers must both sign off.

**Code:**
```text
"The contract can be written by the API consumer or provider, respectively
called consumer-driven contract (CDC) and provider-driven contract (PDC).
In CDC, the consumer defines the service behavior, and the provider's
task is to implement the contract in the service API. This approach
puts more effort on the provider, since it has to catch up with the
consumer's specification. In PDC, the effort is reversed; the provider
defines the contract, and the consumer adheres to it."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Contract testing and fuzzing"*

---

### 27. Use fuzzing where the input space is large

**Principle:** Contract tests cover the documented space; fuzzer-generated inputs cover what was never imagined. Defensive programming widens that space further.

**Do:**
- Combine contract tests with random-input fuzzing to exercise the API under unexpected payloads.
- Run the fuzzer with a coverage-guided engine on critical endpoints for hours, not minutes.
- Treat crashes and unhandled exceptions as P1 incidents.

**Don't:**
- Don't fuzz without instrumentation; coverage-blind fuzzers converge slowly.
- Don't ship a fuzzed API without a "fail-safe" default; failing closed is better than failing open.
- Don't assume fuzzing proves correctness — it only proves the absence of certain classes of bugs.

**Code:**
```text
"Together with contract testing, API fuzzing is used, where a set of
inputs includes random values. The API is expected to handle such
inputs gracefully, with the fuzzer exercising a larger part of the API
specification."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Contract testing and fuzzing"*

---

### 28. Automate end-to-end tests but budget for flake

**Principle:** E2E (Cypress, Playwright, Selenium) verifies the system as a whole. They are high value and high flake — there is a real, irreducible flakiness in browser/network automation.

**Do:**
- Use Playwright when flakiness tolerance matters; it is meaningfully less flaky than Selenium.
- Re-run failed E2E tests a bounded number of times with quarantine on persistent failures.
- Pair E2E with reduced Selenium coverage for legacy compatibility.

**Don't:**
- Don't run E2E on every commit without pooling by default; it is slow.
- Don't dismiss flakiness as "the network"; most flakes are test-design problems (race conditions on state).
- Don't E2E-test what unit tests already prove; each layer earns its place.

**Code:**
```text
"Tools like Cypress, Playwright, and Selenium can automate this manual
labor. However, when working with these tools, be prepared for a
certain amount of test flakiness."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "End-to-end testing"*

---

### 29. Run the CI pipeline before the CD/CD pipeline runs

**Principle:** CI lint, scan, build, test, and publish. CD (delivery) then deploys to staging with a manual approval; CD (deployment) deploys automatically after automated tests pass. Stages are not optional.

**Do:**
- Run lint, static analysis, dependency checks, build, tests, and security scans in CI on every commit.
- Promote the same immutable artifact through CD; rebuild per stage only when re-introducing variance.
- Use blue-green or canary for risky changes; smoke, end-to-end, load, and stress for the highest-confidence rollout.

**Don't:**
- Don't conflate continuous delivery (manual approval) and continuous deployment (automatic); the difference is the human in the loop.
- Don't rely on a remote-only, YAML-based CI/CD as if it were testable like code; budget debugging time.
- Don't promote an environment-branch to production without an explicit green-path test matrix.

**Code:**
```yaml
# Conceptual CI/CD pipeline (use your platform's syntax)
stages:
  - ci:
      - lint
      - static_analysis
      - dep_check
      - build
      - test
      - security_scan   # sast, secrets, dast
  - cd_delivery:        # manual approval
      - deploy:staging
  - cd_deployment:      # automatic
      - smoke:e2e
      - load:stress
      - promote:prod
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment"*

---

### 30. Treat stages as similar but not identical to production

**Principle:** "Staging is not production. It will never be production." Each environment will diverge; the higher the production gap, the more "works on staging, breaks in prod" you will see.

**Do:**
- Pin environments to identical base images and OS levels where possible.
- Capture the production network shape (firewalls, routing) at staging boundaries; replication is impossible, parity isn't.
- Use feature flags and shadow traffic to exercise production paths without the production blast radius.

**Don't:**
- Don't try to make staging a perfect production clone; the cost balloons and you still don't have prod's data shape.
- Don't ship to production without staging checkpoints, but do instrument for fast reversal.
- Don't pretend a "production-like test environment" exists; it differs in ways you cannot enumerate.

**Code:**
```text
"Staging is not production. It will never be production.
— Charity Majors, 2019"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment" / Warning box*

---

### 31. Choose maintenance type by trigger, not by feel

**Principle:** ISO/IEC/IEEE 14764 classifies maintenance by trigger: corrective (bug fix), preventive (avoid failure), adaptive (environment changed), additive (new functionality), perfective (improve ilities). Diagnose the trigger before picking the lever.

**Do:**
- Address corrective maintenance with pairing, not patches; understand root cause first.
- Schedule preventive maintenance for software rejuvenation (cache flush, dependency refresh) routinely.
- Plan adaptive maintenance when the runtime environment shifts (OS upgrade, library major version).
- Treat additive maintenance as the largest budget line; it is what the roadmap normally drives.

**Don't:**
- Don't ship preventive changes under the "perfective" label to hide their scope.
- Don't conflate corrective and adaptive; tracking them separately shows where the team bleeds time.
- Don't skip observability hooks when adding perfective changes; they will become the cost of the next emergency.

**Code:**
```text
"Corrective ... Addresses software malfunctions, usually caused by bugs
or errors that require a fix. Corrective maintenance is expensive and
might take a long time.
Preventive ... Focuses on anticipating and preventing software faults.
Adaptive ... Provides corrections or enhancements to the environment in
which the software operates.
Additive ... Is driven by the need to add new functionality or enhance
existing ones. This is usually the most common type of maintenance.
Perfective ... Introduces enhancements to software to improve its
qualities, such as performance, maintainability, and user experience."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Maintenance"*

---

### 32. Plan retirement before you ship; watch for zombie APIs

**Principle:** APIs don't last forever. Without a retirement plan you end up with zombie APIs — abandoned, undocumented, but reachable. Plan for retirement from day one.

**Do:**
- Publish a deprecation timeline at release; standard "two release overlap" works.
- Use `Deprecation` (point to date) and `Sunset` (future date) HTTP headers; document via a `Link` to the migration guide.
- Migrate consumers before sunsetting; keep deprecation and retirement dates visible on the documentation portal.

**Don't:**
- Don't keep a deprecated API alive indefinitely; sunset it once consumers are moved.
- Don't delete `v1` before `v3` is stable; the conventional rule is to retain the last two releases.
- Don't assume silent retirement is acceptable for public APIs; users will revolt and your brand will take the hit.

**Code:**
```http
Sunset: Wed, 11 Nov 2026 11:11:11 GMT
Deprecation: @1688169599
Link: <https://developer.example.com/deprecation>; rel="deprecation"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Retirement" / Example 1-4*

---

### 33. Govern APIs before shadow APIs govern you

**Principle:** Governance is the set of written and unwritten rules that direct the API program. Without it, you get shadow APIs — active, undocumented, unmanaged.

**Do:**
- Establish practices, standards, and policies; propagate them to API teams; enforce them via templates and CI.
- Use monitoring to check adoption of the policies.
- Pick an API platform (Amazon API Gateway, Azure API Management, Google Cloud Apigee, Kong, MuleSoft) that integrates with CI/CD, monitoring, and security tools.

**Don't:**
- Don't buy an API gateway as your governance strategy; governance is a practice, not a product.
- Don't write a 100-page style guide and assume teams will read it; embed rules in linters and code generators.
- Don't ignore internal APIs in your governance model; shadow APIs love to hide there.

**Code:**
```text
"Governance is the set of written and unwritten rules and processes by
which an organization is directed and controlled. ... To govern APIs
means to create practices, standards, and policies; propagate them to
API teams; and implement them in the API. To ensure that policies are
met, governance requires monitoring of APIs and teams to adhere to the
processes."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Governance, Management, and Platform"*

---

### 34. Recognize private, partner, and public APIs and their trade-offs

**Principle:** APIs are private (internal glue), partner (selected counterparties), or public (anyone). Each tier demands different security, monitoring, and SLAs.

**Do:**
- Default to private; promote to partner only when there is a written commercial relationship.
- Promote to public only with documentation, versioning, deprecation, and security runbooks.
- Apply threat modeling at each tier; the threat model scales with the audience.

**Don't:**
- Don't expose internal-only debug endpoints "for partners"; auth-by-IP is rarely sufficient.
- Don't skip security reviews on the way to public; one breach retroactively poisons the partner tier.
- Don't treat OpenAI-style "free for noncommercial, paid for commercial" as a tier; it's a monetization choice.

**Code:**
```text
"Private - These APIs are known as internal APIs and are developed
internally within an organization. The intended use of these APIs is to
exchange data among organizational units.

Public - These APIs are exposed by an organization to the general
public. Services or data exposed by public APIs can be provided for
free or monetized by the organization that owns them.

Partner - These APIs are accessible only to the organization that
develops them and the organization's partners."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Private, Public, and Partner APIs"*

---

### 35. Run DevOps and DevSecOps without surprises

**Principle:** DevOps merges development and operations into a shared pipeline with shared accountability. DevSecOps shifts security left (or shifts it down into the platform) so that it runs every commit.

**Do:**
- Apply shift-left only where developers have the capacity to absorb it; otherwise shift down into the platform.
- Maintain pipelines that build, test, scan, and deliver automatically; keep humans for the go/no-go decision unless you've earned automatic deploys.
- Couple security runbooks with on-call rotations; security without ops is a stale playbook.

**Don't:**
- Don't disable security checks when they fail often; you have an alert-fatigue problem, not a security problem.
- Don't conflate "we have a DevOps team" with "we are doing DevOps" — culture beats team name.
- Don't push security so far left that teams disable it to ship features.

**Code:**
```text
"DevOps teams also try to address security challenges by following a
shift-left approach, which moves the security focus early into the
product lifecycle rather than to the end (shift right). This approach
is called DevSecOps."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment"*

---

### 36. Choose between code-first, design-first, or YAML-on-CI deliberately

**Principle:** Local code-based CI/CD is debuggable; remote-only YAML-based CI/CD is cheaper but harder to fix. Pick by how often your pipeline fails and how skilled your team is at debugging it.

**Do:**
- Use a code-based pipeline definition (Dagger, Buildkite, custom) if you have engineers who want to test it locally.
- Use a YAML-only platform if the team is small and the failure rate is low.
- Treat the build pipeline as production code: tests, version control, ownership, on-call.

**Don't:**
- Don't pick the remote-only YAML system for a team that will bleed time debugging it on every outage.
- Don't pretend YAML is code; it lacks the refactorability of a real language.
- Don't change CI/CD strategy mid-project; the migration is brutal.

**Code:**
```text
"A choice also needs to be made for the CI/CD system. Will you spend
labor costs on debugging deployment failures in a remote-only,
YAML-based CI/CD system, or instead invest in the development of a
local, code-based CI/CD environment?"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment" / footnote 20*

---

### 37. Make deployment reversible, especially for stateful APIs

**Principle:** Migrations and schema changes break consumers. Backwards-compatible reads, blue-green, and reversible deploys are the only way to make deployment boring.

**Do:**
- Treat every database change as if it needs a backward-compatible read path; old code and new code must coexist.
- Use feature flags to gate risky behaviour behind kill switches.
- Keep deployments reversible within a known SLA (minutes, not days).

**Don't:**
- Don't drop or rename columns on the same deploy that stops writing them; wait a generation.
- Don't rely on "we can roll back"; roll-back is rarely the right answer for state changes.
- Don't introduce async work without idempotency keys; retries double-charge.

**Code:**
```text
"Jez Humble's goal is to make deployments 'predictable, routine
affairs that can be performed on demand.'"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment" / "Designing Resilient Software"*

---

### 38. Manage the buy-vs-build deployment trade-off

**Principle:** Cloud-vendor platforms give you proxying, logging, secrets, and security out of the box. Self-hosting (Kubernetes, Kamal) buys you control at the cost of higher operations labour.

**Do:**
- Pick a cloud-native API gateway when your team is small and procurement is more valuable than control.
- Pick Kubernetes when scale, customization, and portability outweigh the operations cost.
- Pick Kamal-style tools when you want deployment simplicity and have capacity to manage capacity manually.

**Don't:**
- Don't run your own Kubernetes cluster to "save money" before you have the team to operate it.
- Don't pick a vendor lock-in when your exit cost exceeds your lock-in savings.
- Don't assume platform choice is permanent; migration cost is real.

**Code:**
```text
"Depending on your needs, an API artifact could be deployed to a
proprietary cloud-vendor platform, a self-hosted cloud native
environment, or on-premises machines. If you choose the build path,
will you incur the higher labor cost of setting up and maintaining a
platform like Kubernetes, which supports highly available deployment
and scaling of containerized applications? Or will you opt for the
lower initial labor cost needed by a simpler tool like Kamal, knowing
it may lead to higher labor costs later due to manual capacity
management?"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Deployment"*

---

### 39. Treat confidentiality, integrity, and availability as a checklist, not a slogan

**Principle:** The three security pillars (CIA — Confidentiality, Integrity, Availability) translate directly into engineering controls. Skim them and your API will be the next news headline.

**Do:**
- Enforce authentication on every endpoint; rate-limit by identity, not just IP.
- Sign everything transport-level (TLS) and selectively payload-level (HMAC for webhooks).
- Provide availability via redundancy, circuit breakers, and rate-limited upstream calls.

**Don't:**
- Don't use "we use HTTPS" as the entirety of your security story; HTTPS protects transit, not authn/authz, not rate, not validation.
- Don't return 200 OK on auth failure; return 401/403 with reason codes that don't leak the username enumeration.
- Don't accept unbounded request bodies; stream and bound them.

**Code:**
```text
"There are more doors to enter, and the treasure is bigger! ...
The API openness of APIs makes them a potential target and presents a
new kind of attack surface."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Security" (intro)*

---

### 40. Defend with standardized 12 API security principles

**Principle:** Twelve principles cluster into the three CIA goals plus design hygiene. Apply them to every API review.

**Do:**
- Apply API confidentiality, integrity, and availability as the top-level gates.
- Adopt fail-safe defaults (deny by default), complete mediation (every endpoint authorized), and least privilege (scope to what each consumer needs).
- Document openly; verify everything (CMII / MFA / IP allowlists); fail securely.
- Use zero-trust: treat internal and external callers as untrusted by default.
- Maintain and test fixes; don't paper over root causes.

**Don't:**
- Don't invent new security goals when these twelve cover the common cases.
- Don't impose heavy security on low-risk endpoints; psyche-of-acceptability matters.
- Don't skip defense in depth; one control alone will fail.

**Code:**
```text
"1. API confidentiality
2. API integrity
3. API availability
4. Economy of mechanism
5. Fail-safe API defaults
6. Complete mediation
7. Open API design
8. Least API privilege
9. Psychological acceptability
10. Minimize API attack surface area
11. API defense in depth
12. Zero-trust policy
13. Fail APIs securely
14. Fix API security issues correctly"
```
*Ref: Continuous_API_Management_2e.md — "12 API security principles"; referenced alongside in Learning_API_Styles_-_Lukasz_Dynowski.md*

---

### 41. Pin a clear access-type taxonomy at the package boundary

**Principle:** Encode identity claims at the edge. Bad identity hand-offs are the single most common root cause of API breaches.

**Do:**
- Centralize authentication (OAuth/OIDC) at the gateway; push authorization decisions into the API.
- Use scopes/claims to enforce least privilege per consumer.
- Audit authorization decisions; log the identity, the action, the resource, the verdict.

**Don't:**
- Don't roll your own token format; use JWT or PASETO with a vetted library.
- Don't accept identity from query strings; they will be logged everywhere.
- Don't store raw credentials in the application; delegate to an identity provider.

**Code:**
```text
"Authentication - identifying who is making a call. Authorization -
what they are allowed to do. ... Avoiding 'we made it up' identity
protocols."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Security" (intro)*

---

### 42. Look at REST, GraphQL, gRPC through one framework

**Principle:** All three are about shaping a contract. They differ on transport verbosity, on contract expressiveness, and on who chooses the response shape (server vs client).

**Do:**
- Score REST against GraphQL on consumer flexibility vs server predictability.
- Pick gRPC for low-overhead internal traffic; OpenAPI for human-readable contracts.
- Match the framework to your team's ability to operate (debug, version, document) it.

**Don't:**
- Don't run gRPC for browser clients without an HTTP/JSON gateway.
- Don't run GraphQL without rate limits, persisted queries, and depth limits.
- Don't run REST without CORS, caching, and pagination conventions.

**Code:**
```text
"REST is a resource-oriented paradigm with HTTP verbs; GraphQL exposes
a single endpoint with declarative shape; RPC/gRPC invokes a remote
procedure through a contract-first IDL."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Are API Styles?"*

---

### 43. Decide continuity of message by use case: not every "message" needs a broker

**Principle:** XMPP is a chat-style XML envelope. MQTT is a binary packet. HTTP is a request/response message. They shape the design as much as any style does.

**Do:**
- Pick the message protocol whose on-wire format matches your payload shape.
- Treat XML envelopes (SOAP/XMPP) as a deliberate choice for regulated, schema-rich domains.
- Use compact binary (Protobuf, MQTT) for IoT and high-fanout channels.

**Don't:**
- Don't use SOAP for new greenfield APIs unless something in your stack mandates it.
- Don't assume HTTP message size is unlimited; cap it server-side.
- Don't pick MQTT for low-fanout RPC; it is a pub/sub plumbing.

**Code:**
```xml
<?xml version='1.0'?>
<stream:stream ...>
 <message from='sender@example.com' to='receiver@example.net'
   xml:lang='en'>
  <body>Hello</body>
 </message>
</stream:stream>
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Message" / XMPP*

---

### 44. Adopt lifecycle outputs that create durable feedback loops

**Principle:** Documentation should be drafted during every phase, observability maintained during maintenance, alerting during operations, retirement planned during design.

**Do:**
- Draft documentation continually; review it during the maintenance phase.
- Instrument every endpoint with logs, metrics, and traces during implementation.
- Plan retirement and deprecation dates during design; revisit them during maintenance.

**Don't:**
- Don't produce documentation only at the end; you'll never get to it.
- Don't treat observability as a separate "ops concern"; ship it with the code.
- Don't retire APIs without a migration guide and per-consumer comms.

**Code:**
```text
"Security is a force that is present in all phases of the API
lifecycle ... A more realistic approach to documentation is to draft
at least some of it during all phases of the API lifecycle."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Lifecycle" / Security & Documentation*

---

### 45. Use semantic versioning for breaking-change hygiene

**Principle:** Semver (MAJOR.MINOR.PATCH) is the most common contract for API versioning. Major versions are when you break clients; minor versions are additive; patches are bug-fixes.

**Do:**
- Bump MAJOR for breaking changes; bump MINOR for additive new features; bump PATCH for backward-compatible fixes.
- Publish what is in each version in release notes; include the data they need to migrate.
- Maintain the last two versions: deprecate the older one when the third is released.

**Don't:**
- Don't ship silent breaking changes inside a PATCH; clients upgrade and break.
- Don't promise "we will never break you" until you have the operational discipline to back it (Stripe/Salesforce style).
- Don't reset the version when you rebrand; clients depend on the string.

**Code:**
```
# Semver for public APIs
MAJOR.MINOR.PATCH
# 2.4.1 -> 3.0.0 when any field is removed or renamed
# 2.4.1 -> 2.5.0 when fields are added or behaviour is extended
# 2.4.1 -> 2.4.2 when only bugs are fixed
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Retirement" / version policy*

---

### 46. Mind the ethics and code-of-conduct around test data

**Principle:** "Production data are confidential and always protected. Test data are not subjected to the same restrictions." When you copy production data into test, you have moved classified data outside its perimeter.

**Do:**
- Anonymize or synthesize production-shaped test data; never copy PII by default.
- Track test data lineage just like production data.
- Honour regulatory notification when even test data crosses borders.

**Don't:**
- Don't assume "internal team" means "no compliance obligation"; the rules travel with the data, not the audience.
- Don't reuse a single test dataset across projects; leakage compounds.
- Don't generate test data with no constraint; randomly unbounded strings will hit parsing limits.

**Code:**
```text
"Production data are confidential and always protected. Test data are
not subjected to the same restrictions or even to the same safety
measures. If test data are used, it is thus recommended to ensure
that they are 'anonymized'."
```
*Ref: Fundamentals_of_Software_Testing_2nd_Ed_-_Bernard_Homes.md — "Test data definition" (cross-reference); Learning_API_Styles_-_Lukasz_Dynowski.md — "Test and debugging" intent*

---

### 47. Treat the API ecosystem as a multi-style language landscape

**Principle:** API styles differ the way natural languages differ: each has its own grammar and idioms. A multi-style landscape is a polyglot environment, not a single one.

**Do:**
- Maintain a service catalog mapping each service to its style, audience, lifecycle.
- Encourage style specialisation for teams who will own many services of one style.
- Document interoperability contracts (how the broker and the WebSocket and the REST API talk).

**Don't:**
- Don't punish variety for variety's sake; rule out shadow-API duplication.
- Don't force one style onto all teams; you will get a poor copy of every style.
- Don't let style choices drift without governance review at major version boundaries.

**Code:**
```text
"Even though various API styles can use the same instruments, such as
protocols, communication types, principles governing it, or design
constraints, what defines an API style is the set of its most dominant
characteristics. ... A band often identifies itself with a dominant
music style, not a set of instruments used to create it."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Are API Styles?"*

---

### 48. Invest in client SDK generation and codegen hygiene

**Principle:** When the OpenAPI/AsyncAPI/Protobuf description is the contract, code generators keep clients honest. They are most effective for the first release; you need other mechanisms to keep downstream clients updated.

**Do:**
- Generate SDKs from the contract; never hand-roll a client SDK.
- Version SDKs in lockstep with the contract.
- Distribute via a registry your consumers already use.

**Don't:**
- Don't hand-write clients that diverge from the description; the description is the source of truth.
- Don't sign up to maintain SDKs in five languages unless your revenue justifies it.
- Don't publish an SDK that is not exercised by your own tests.

**Code:**
```bash
# Example: regenerate client after OpenAPI change
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o clients/python
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API-First Approach"*

---

### 49. Watch the future: HTTP/3, WebTransport, MCP, AI-driven APIs

**Principle:** New protocols (HTTP/3, WebTransport, Model Context Protocol) reshape what's possible. APIs are growing fastest where AI agents are clients. Watch the protocol layer, not just the application layer.

**Do:**
- Plan to upgrade HTTP/1.1 stacks to HTTP/2 and HTTP/3 over time; the perf gains are not free.
- Evaluate WebTransport for cases where WebSocket falls short (datagrams, multi-stream).
- Build APIs that AI agents can discover; standard descriptions beat bespoke scraping.

**Don't:**
- Don't freeze your protocol choice on legacy beliefs; HTTP/3 has been RFC since 2022.
- Don't gate AI features on the absence of MCP; treating AI as a first-class consumer is now table stakes.
- Don't forget the security implications of every new protocol; each adds surface.

**Code:**
```text
"HTTP is evolving and reached its third release (HTTP/3) in June 2022.
The WebTransport protocol aims to address shortcomings of the
WebSocket protocol. Model Context Protocol (MCP) aims to facilitate
resource discovery and use by LLMs and agentic AI."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Future of APIs"*

---

### 50. Use the WFS example to compare styles on a single problem

**Principle:** Implementing the same Weather Forecast Service in REST, GraphQL, Atom, gRPC, WebSocket, webhook, and broker lets you experience the trade-offs in code rather than in slides.

**Do:**
- Pick a single domain and implement multiple styles to feel the trade-offs.
- Compare binary support, development effort, and responsiveness with the same team.
- Document the choices and their outcomes in an architectural decision record.

**Don't:**
- Don't accept second-hand style comparisons; try them in your context.
- Don't assume your team's skill set is portable across styles; gRPC requires protobuf fluency, WebSocket requires asynchrony literacy.
- Don't pick a style to fit a single use case; APIs grow outward.

**Code:**
```python
# WFS REST endpoint (Django / Starlette pattern from the book)
from django.urls import path
from django.http import JsonResponse

def forecast(request, city):
    # 7-day forecast for the requested city
    return JsonResponse({"city": city, "days": [...]})

urlpatterns = [path("forecasts/<str:city>/", forecast)]
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Weather Forecast Service" / WFS*

---

### 51. Engineer for the legacy of API mandates, not their letter

**Principle:** The 2002 Amazon API mandate condensed service-data-exposure-through-API into a single rule. Its spirit (everything via API, technology-independent, designed for externalization) still drives modern architectures; ignore it and your org will leak glue code into the public.

**Do:**
- Treat "all service interactions via API" as the floor, not the ceiling.
- Keep APIs technology-agnostic so the implementation can swap without breaking clients.
- Design the API to be externalizable, even when you have no public API plans; the cost is small, the option value is large.

**Don't:**
- Don't reach for shared databases or RPC tunnels because they are convenient; they will become a maintenance anchor.
- Don't package business logic in client libraries that bypass the API; the network boundary is also your governance boundary.
- Don't read the mandate as an excuse for monolith-served-as-API; services must own their data.

**Code:**
```text
"1. Service data and functionality are exposed through APIs.
2. Services communicate through APIs only.
3. No other ways of communication apart from network-based APIs are allowed.
4. APIs are implemented using a technology that fits the context.
5. APIs are to be designed so that they are externalizable to public clients."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Mandate" (Bezos)*

---

### 52. Make monitoring and observability design-time, not bolt-on

**Principle:** Observability is "are we running?" but it is also "how are users using us?". Both shapes have to be designed.

**Do:**
- Track successful vs unsuccessful responses, traffic volume, callers, freshness of last use.
- Build metrics dashboards that owners actually check; alerts on SLO breaches.
- Add request/response logging selectively; full logging halves RTT and inflates costs.

**Don't:**
- Don't ship an API without a single observability signal; you will debug blind.
- Don't log PII by default; sanitize before persistence.
- Don't pretend sampling is free; you can miss the one bad request that triggered the outage.

**Code:**
```text
"In the maintenance phase, observability and analytics are part of the
maintenance phase. Observability is about monitoring effects of
requests and responses generated by the API — for instance, successful
and unsuccessful responses, the volume of traffic coming in, who sends
the traffic, where it's coming from, and when the API was last used.
The collected telemetry is then visualized via metrics dashboards. In
the maintenance phase, maintainers also set up alerting tools to help
them respond to urgent situations."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Maintenance"*

---

### 53. Adopt a release cadence that supports safe-but-fast change

**Principle:** "Deploy changes as quickly as possible should be a goal for your deployment work", but only when safety mechanisms (immutable artifacts, canary, feature flags, automatic rollback) are real.

**Do:**
- Practice trunk-based development with feature flags; main is always deployable.
- Use canary releases for APIs that have external consumers; observe before promoting.
- Keep the same immutable artifact through staging and production; only configuration varies.

**Don't:**
- Don't freeze changes to "reduce risk"; you'll freeze accrual, not risk.
- Don't roll forward on green and roll back on red; the system that detects red may itself be broken.
- Don't merge long-lived branches; they guarantee merge hell at the worst moment.

**Code:**
```text
"One kind of uncertainty that you'll be forced to accept comes in the
form of changes to the API. While it would be nice to freeze all
changes once you've got your API working reliably, change is an
inevitability that you'll need to prepare for. In fact, deploying
changes as quickly as possible should be a goal for your deployment
work."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Designing Resilient Software"*

---

### 54. Map your service's dataflow and lock down broker topology

**Principle:** For broker-based APIs, the exchange/queue/topic topology *is* the architecture. Document it and version it.

**Do:**
- Use direct exchanges for explicit routing; topic exchanges for pattern routing; fanout for broadcasts.
- Make queue/exchange names follow naming standards (`service.entity.action`).
- Persist messages for transactional work; transient for telemetry.

**Don't:**
- Don't use `auto-delete` and `exclusive` for queues that carry business events; you'll lose messages on broker restart.
- Don't pour binary frames through dead-letter exchanges without a triage process.
- Don't skip dead-letter queues; they are the difference between recoverable and unrecoverable.

**Code:**
```python
# RabbitMQ topology declaration (excerpt pattern from the book)
import pika

connection = pika.BlockingConnection(pika.URLParameters("amqp://localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="weather", exchange_type="topic", durable=True)
channel.queue_declare(queue="alerts.eu", durable=True)
channel.queue_bind(exchange="weather", queue="alerts.eu", routing_key="alerts.eu.*")
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Broker-based" / RabbitMQ example*

---

### 55. Treat all API decisions through one lens: HTTP verb semantics

**Principle:** Pick the verb by what the client intends, not by what your ORM does.

**Do:**
- Use `GET` for read-only idempotent operations.
- Use `POST` for actions that lack a standard verb or change server state without a clear verb match.
- Use `PUT` for full replacement; `PATCH` (or `POST` with body) for partial updates.
- Use `DELETE` for delete; check whether the operation is soft-delete and what idempotency you support.

**Don't:**
- Don't use `GET` for state-changing side effects; crawlers and prefetch will write to your database.
- Don't return a `200 OK` on a successful `POST` that should be `201 Created`.
- Don't overload `PUT` with `PATCH` semantics; clients will misread.

**Code:**
```http
GET     /forecasts/krakow     200 OK
POST    /forecasts            201 Created + Location: /forecasts/42
PUT     /forecasts/42         200 OK (full replace)
PATCH   /forecasts/42         200 OK (partial update)
DELETE  /forecasts/42         204 No Content
POST    /forecasts/42:alert   200 OK (custom action via sub-resource)
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Resource-Oriented Versus Intent-Oriented APIs"*

---

### 56. Score gRPC adoption by team maturity and tooling fit

**Principle:** gRPC earns its keep when the team has Protobuf fluency and the runtime supports HTTP/2 framing.

**Do:**
- Train the team on `.proto`, the codegen pipeline, and the streaming modes.
- Provide a JSON gateway (`grpc-gateway`, `grpc-web`) if your clients cannot speak HTTP/2.
- Use `grpcurl` and `grpc_cli` for debug-by-curl-feel; document them in the runbook.

**Don't:**
- Don't expose Protobuf without a defined `.proto` package and version policy.
- Don't hand-craft JSON in client code that talks to a gateway; use the generated stub.
- Don't ignore server reflection; it's the equivalent of OpenAPI for gRPC and slashes debugging cost.

**Code:**
```bash
# gRPC tooling footnotes
grpcurl -plaintext localhost:50051 list                # list services
grpcurl -plaintext -d '{"city":"Krakow"}' \
   localhost:50051 weather.WeatherService/GetForecast   # invoke method
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "RPC" / gRPC*

---

### 57. Treat webhooks as a contract, not a configuration value

**Principle:** A webhook URL is part of your public surface. Change it and you break consumers; sign it and you let them trust you.

**Do:**
- Document the payload schema; deprecate with a header (e.g., `Webhooks-Version`).
- Sign with HMAC-SHA256 of the timestamp + body; publish the verification snippet.
- Allow consumers to set a secret per endpoint; rotate via overlap window.
- Replay-attack defence: include `X-Webhook-Timestamp`; reject messages whose age exceeds a window.

**Don't:**
- Don't accept arbitrary JSON shapes from webhooks; reject unknown fields silently.
- Don't forget to deduplicate on the consumer side; at-least-once means duplicates are real.
- Don't return a 5xx on consumer rejection unless you intend to retry forever.

**Code:**
```http
POST /your/webhook HTTP/1.1
Host: receiver.example.com
Content-Type: application/json
X-Webhook-Signature: t=1689132911,v1=4e1e...e7a3
X-Webhook-Timestamp: 1689132911

{"event":"alert.published","data":{"city":"Krakow","severity":"high"}}
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Callback" / webhooks*

---

### 58. Treat WebSocket subprotocols as a contract

**Principle:** The WebSocket handshake carries a `Sec-WebSocket-Protocol` header that names the application protocol. Negotiate it; never assume `wss://example/socket` is enough.

**Do:**
- Pick a subprotocol name (`wfs.v1.station`), advertise it, and version it.
- Document the message envelope (frame format) inside that subprotocol.
- Heartbeat every 30s or so; close on three missed pings.

**Don't:**
- Don't rely on TCP keepalive alone; many middleboxes close idle sockets fast.
- Don't bake in JSON-with-no-schema; document the message types and validators.
- Don't store session state in a single server process; the second connection after a reconnect will lose context.

**Code:**
```javascript
const ws = new WebSocket("wss://api.example.com/wfs", "wfs.v1.station");
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  // expected: { type: "alert", severity, message }
};
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Bidirectional" / WebSocket*

---

### 59. Make every API "API first" the same shape regardless of style

**Principle:** Description-first is style-agnostic. OpenAPI for HTTP/REST, AsyncAPI for messaging, Protobuf for gRPC, GraphQL SDL for GraphQL. Each pins a contract; tooling around it is mature.

**Do:**
- Author the description (`.yaml`, `.proto`, `.graphql`, `.asyncapi.yaml`) before coding.
- Validate the description in CI: lint, breakage checks, and example rendering.
- Host the contract in source control; tag releases alongside the implementation.

**Don't:**
- Don't accept a "later" description; you will rewrite it from scratch.
- Don't split a service's contract across multiple description files unless forced.
- Don't allow hand-edits to consumer-generated stubs that diverge from the description.

**Code:**
```text
"Software tools available to support these formats also help in
implementing and testing the API, as well as generating the API
documentation."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API-First Approach"*

---

### 60. Plan AI-agent first-party consumers from day one

**Principle:** Gartner predicts 30% of API demand growth comes from AI/LLMs by 2026. APIs will be consumed by LLMs and agentic code, not just humans and CLIs.

**Do:**
- Make API descriptions machine-readable and discoverable (OpenAPI tagged, documented).
- Provide rich examples; agents imitate what they see.
- Treat MCP (Model Context Protocol) as a candidate adapter for resource discovery.

**Don't:**
- Don't gate AI features on absence of MCP; treat AI as a first-class consumer.
- Don't assume a human UI is the primary surface; agentic APIs need simpler affordances.
- Don't bury essential endpoints behind authentication designed only for humans.

**Code:**
```text
"Training of LLMs requires consuming data, such as text, images, audio,
and video, that largely come from APIs. As companies create their own
LLM-based services, existing and new API styles will enable their
growth, acting as funnels through which data will enter and leave."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Future of APIs"*

---

### 61. Engineer for cross-style interoperability, not single-style purity

**Principle:** Real systems mix styles. A REST service may fan out via Kafka, receive events via webhooks, and stream to humans via WebSocket. Plan for the seams.

**Do:**
- Make interop boundaries explicit (gateway → Kafka, HTTP → SSE).
- Translate protocols at the boundary; don't propagate one style's semantics into another.
- Use a dedicated adapter per interop seam; test it heavily.

**Don't:**
- Don't assume one style's clients will tolerate another's semantics; verify.
- Don't translate twice; one gateway per seam is enough.
- Don't expect consumer-friendly debugging across style boundaries without tracing across all of them.

**Code:**
```text
"In practice you'll see API ecosystems where each service picks the
style that suits its data shape and traffic pattern; the artistry is
in how they interop."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "What Are API Styles?"*

---

### 62. Use the Bezos Mandate's "externalizable by default" rule

**Principle:** Mandate #5 — design APIs to be externalizable to public clients — means picking your API as if a stranger will read it tomorrow.

**Do:**
- Document, version, secure, and deprecate even private APIs.
- Treat internal consumers as anonymous: their code is theirs, your contract is yours.
- Refactor internal-only conveniences into the implementation, not the contract.

**Don't:**
- Don't assume "internal" means "no review"; the audit you skip today becomes the breach tomorrow.
- Don't expose privileged parameters just because "no one" sees them; the WFS alert has no `?admin=1`.
- Don't promise things in the contract because "it's just internal"; you will eventually expose.

**Code:**
```text
"5. APIs are to be designed so that they are externalizable to public
clients."
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Mandate"*

---

## Anti-Patterns & Common Mistakes

- **Shadow APIs:** unmanaged, undocumented endpoints keep serving traffic. *Fix:* catalogue, classify, and sunset, or adopt and document them.
- **"RESTful" without hypermedia:** HTTP/JSON APIs labeled RESTful that ignore HATEOAS. *Fix:* add `Link` headers; document affordances.
- **Code-first APIs shipped without a contract:** implementation freeze is implicit; consumers cannot validate. *Fix:* OpenAPI/AsyncAPI first, implementation after.
- **Treating security as a stage:** a single security review at the end cannot catch decisions made during design. *Fix:* security as a force in every phase.
- **Big up-front lifecycle:** sequential phases that block each other. *Fix:* vertical slices and ACED-style iteration.
- **Production traffic on staging-like environments:** pretending staging is production. *Fix:* parity + feature flags + blue-green; accept the irreducible gap.
- **Migrating the CI/CD strategy mid-project:** debugging remote YAML forever. *Fix:* settle the build pipeline before scaling the team.
- **Silent breaking changes inside PATCH:** clients upgrade and break. *Fix:* strict semver discipline in release notes.
- **Hyrum's Law surprise:** undocumented behaviours change and break consumers. *Fix:* capture them in regression tests; deprecate before removing.
- **One HTTP verb for everything:** custom verbs in REST URLs. *Fix:* use sub-resources or RPC; never invent a verb.
- **Webhooks without destination durability:** expecting at-least-once without retries and dead-letter. *Fix:* pair with proper retry + dedup at the destination.
- **Broker-as-RPC:** using queues for synchronous request/response. *Fix:* pick the right primitive; queues are for fan-out, not RPC.
- **Single style forced onto the org:** every team must use REST. *Fix:* match style to team capability and use case; govern interoperability instead.
- **Frameworks as architecture:** choices made because the framework is convenient. *Fix:* evaluate frameworks against the architecture, not the other way around.
- **Doc-once-at-the-end:** documentation that never lands. *Fix:* draft documentation in every phase; review during maintenance.
- **Pinning gRPC to public browsers:** expecting browsers to speak HTTP/2 framing. *Fix:* gateway in front.

---

## Decision Heuristics / Checklists

- **Style selection:** map (data shape × audience × responsiveness × protocol) before picking. REST for resources + verbs; GraphQL for shape flexibility; gRPC for high-fanout, low-latency internal RPC; WebSocket for full-duplex; MQTT for IoT; broker for fan-out + durability; feeds for syndicated content; webhooks for callback push.
- **Name selection:** plural nouns for REST resources; verbs in GraphQL/gRPC; units in scalar names; consistency over the entire domain.
- **Versioning policy:** semver with two-version overlap; explicit `Sunset` and `Deprecation` headers; per-consumer migration tracking.
- **Contract first:** OpenAPI/AsyncAPI/Proto authored before implementation; both ends generated/synced.
- **Security checklist:** confidentiality, integrity, availability, fail-safe defaults, complete mediation, least privilege, defense in depth, zero-trust, fail-secure; twelve principles + OWASP API Top 10.
- **CI/CD:** CI lint, scan, build, test, publish. CD (delivery) on approval. CD (deployment) for vetted services.
- **Retirement:** old version deprecated at new version release; sunset within a documented window; retirement kills the instance.
- **API landscape:** variety with purpose; curation by C4E; "design for consumers, producers, sponsors"; never let style drift silently.
- **Test layering:** Q1 unit tests; Q2 functional; Q3 UAT; Q4 perf/security; contract tests at every boundary; fuzzing at the public surface.

---

## Key Takeaways

1. APIs are interaction points — define them with a contract, not a code path.
2. Security is a force in every phase; treat it like correctness, not a checklist.
3. Multiple styles coexist; pick by protocol fit, audience, responsiveness, and binary needs — not by fashion.
4. Implement, then compare on the same problem; the WFS example is your homework.
5. Plan retirement before shipping; zombie APIs are the natural decay of unmanaged endpoints.
6. OpenAPI/AsyncAPI/Proto is the contract; both sides must read from the same source of truth.
7. Hyrum's Law rules everything: every observable behaviour is depended on by someone.
8. Document in every phase; review during maintenance; retire with ceremony.
9. CI/CD pipelines are production code; test them, version them, assign them to a team.
10. Versioning is semver with two-version overlap; deprecate before sunsetting; never silently break.

---

## Cross-References

- Related: `../Continuous_API_Management.md` (lifecycle, governance, developer experience)
- Related: `../Restful_Web_API_Patterns_and_Practices.md` (deeper REST patterns)
- Related: `../Mastering_Api_Architecture.md` (API architecture patterns)
- Related: `../Communication_Patterns.md` (cross-component async vs sync patterns)
- Related: `../Building_Event-driven_Microservices.md` (event-driven implementation)
- Related: `../Building_An_Event-Driven_Data_Mesh.md` (event meshes built on broker APIs)
- Related: `../Domain_Driven_Design_with_Golang.md` (modelling API resources from domain primitives)
- Related: `../Fundamentals_of_Software_Testing.md` (testing the contracts you ship)
- Related: `../What_to_Test_and_When.md` (risk-driven test selection across the lifecycle)
- Topic index: `../INDEX.md`

---

## Quick Reference Card

| Decision                              | Pick                                                                 |
|---------------------------------------|----------------------------------------------------------------------|
| Public REST for resources + verbs     | OpenAPI 3.0/3.1 contract, HTTP, semantics-driven status codes        |
| Public GraphQL for shape flexibility  | Single endpoint, depth/complexity limits, persisted queries          |
| Internal RPC, low latency, streaming | gRPC + Protobuf, HTTP/2 framing, four streaming modes                |
| Public webhook push                   | HMAC signing, `Sunset`/`Deprecation`, retries with idempotency        |
| IoT fan-out                           | MQTT topics, QoS levels, retained messages, broker vs broker bridge  |
| Live UI updates                       | WebSocket subprotocol, heartbeats, resumable sessions                |
| High-fanout durable fan-in            | RabbitMQ / Kafka with persistent messages + DLQs                      |
| Syndicated content                    | Atom/RSS over HTTP with proper caching headers                        |
| Single domain, multiple styles        | API-first descriptions, codegen, contract tests in CI                 |
| Public consumers including AI         | OpenAPI tag discovery, examples, MCP for resource discovery           |
| Style selection neutral               | Use Table 1-1 axes (protocol, comm type, binary, latency, dev cost)  |
| Versioning                            | Semver with two-version overlap, `Sunset`/`Deprecation` headers       |
| Lifecycle output                      | Documentation drafted each phase, observability shipped with code    |

## Reading Order (for new API architects)

1. Chapter 1 — API concepts, history, lifecycle, governance.
2. Chapter 2 — Design patterns (naming, error handling, versioning).
3. Chapter 3 — Network protocols (TCP/IP, OSI) and Chapter 4 — Web protocols (HTTP).
4. Chapter 5 — REST; then chapters 6–11 for GraphQL, Atom, gRPC, Webhooks, WebSocket, RabbitMQ.
5. Cross-cut: chapters 9 and 12 — when stuck on a single style, return to landscape thinking.
