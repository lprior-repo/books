# Mastering API Architecture
**Author:** James Gough, Daniel Bryant, Matthew Auburn (O'Reilly, 2022)
**Topic tags:** `#api` `#architecture` `#testing` `#security`
**Language focus:** language-agnostic; Java for gRPC/REST-Assured, YAML/Proto for infrastructure, bash for tool invocation
**Sources:** `markdown_output/Mastering Api Architecture/Mastering Api Architecture.md` · `summaries/Mastering_Api_Architecture.md`

## TL;DR
This book is a working architect's field guide to the full API lifecycle: designing REST/RPC specs, writing tests at every layer (quadrant/pyramid), routing north-south traffic via gateways, routing east-west traffic via service meshes, releasing via canary/blue-green/Argo Rollouts, threat-modeling with STRIDE/DREAD, and authenticating with OAuth2/JWT/OIDC. Apply when designing or evolving any networked API surface where loose coupling, observability, and zero-trust security are first-class concerns.

## Best Practices by Topic

### 1. API Definition: Abstraction of Implementation
**Principle:** An API is an abstraction of the underlying implementation, backed by a specification that introduces types and semantics — not just a URL.

**Do:**
- Treat every API as a contract: producer models resources (REST) or methods (RPC), consumer drives behavior.
- Distinguish in-process (same OS process, compile-time-safe) from out-of-process (network-bound, requires serialization / failure handling) APIs.
- Pair every API with documentation, versioning, and a schema (OpenAPI or `.proto`).

**Don't:**
- Conflate "API" with "endpoint" — a properly modeled API has a vocabulary of types, error shapes, and authoritative behavior.
- Build out-of-process APIs that mirror internal data structures (information hiding violation).

**Code:**
```text
A working definition of API:
  - Represents an abstraction of the underlying implementation.
  - Represented by a specification that introduces types; tooling can generate
    code in multiple languages to implement an API consumer.
  - Has defined semantics / behavior to model the exchange of information.
  - Enables extension to customers or third parties for business integration.
```
*Ref: Mastering Api Architecture.md — "A Brief Introduction to APIs"*

### 2. C4 Model for Architecture Communication
**Principle:** Use the C4 model (Context → Container → Component → Code) to communicate architecture at the right level of abstraction for the audience.

**Do:**
- Start every architecture conversation with a System Context diagram (one box, surrounding actors).
- Zoom in with Container diagrams (deployable units — web app, API container, database).
- Resolve "what's inside container X" with a Component diagram (controllers, services, DAOs).
- Use C4 alongside ADRs so diagrams and rationale stay paired.

**Don't:**
- Use UML — most engineers don't remember the dialect, and whiteboard drift destroys value.
- Skip Context and jump straight to deployment topology; you lose stakeholders before they sign off.

**Code:**
```text
C4 levels, in order of zoom:
  1. Context  - system + external actors (one box, whole world view)
  2. Container - deployable units that "must be running for the system to work"
  3. Component - responsibilities and interactions inside one container
  4. Code      - optional UML/class-level; usually skipped in favour of code itself
```
*Ref: Mastering Api Architecture.md — "Using C4 Diagrams"*

### 3. Architecture Decision Records (ADRs)
**Principle:** Capture every significant decision as an immutable record (proposed → accepted/rejected → superseded) with context and consequences, so future engineers stop asking *"what were they thinking?"*

**Do:**
- Use four sections: **Status, Context, Decision, Consequences**.
- Keep ADRs immutable once accepted — even rejected ones are valuable historical record.
- Publish ADRs where key participants can comment; treat them as living artifacts.

**Don't:**
- Treat ADRs as blog posts — context must be a brief, not a novel.
- Use Type 1 (irreversible) decision rigor for Type 2 (easily reversible) choices — slows delivery.

**Code:**
```text
ADR001 Separating attendees from the legacy conference system
Status:        Proposed
Context:       Conference owners need two major features (mobile app + external
               CFP integration) without disrupting current production.
Decision:      Take an evolutionary step to split Attendee into a standalone
               service (Figure I-4). Enables API-First dev against the Attendee
               service and direct access from the external CFP system.
Consequences:  Out-of-process call introduces latency to be measured.
               Attendee becomes a single point of failure (mitigation needed).
               Multiple consumers -> design/versioning/testing discipline.
```
*Ref: Mastering Api Architecture.md — "Using Architecture Decision Records"*

### 4. ADR Guidelines Format: Resolving "It Depends"
**Principle:** Structure decisions in three columns — Decision, Discussion Points, Recommendations — so the rationale travels with the recommendation.

**Do:**
- State the decision crisply at the top.
- Surface the questions that drive the answer (Discussion Points).
- End with a default Recommendation plus the rationale.

**Don't:**
- Open with recommendations and bury the trade-offs.
- Leave the format implicit — different reviewers will invent different ones.

**Code:**
```text
ADR Guideline: Format
| Decision         | Describes a decision you might need to make when considering an
|                  | aspect of this book.
| Discussion Points| Helps identify the key questions; surfaces experience that may
|                  | have influenced past decisions.
| Recommendations  | Specific recommendations to consider when creating your ADR,
|                  | with rationale.
```
*Ref: Mastering Api Architecture.md — "Mastering API: ADR Guidelines"*

### 5. REST Constraints (Fielding)
**Principle:** REST requires stateless, cacheable, layered, uniform-interface interactions where the producer models resources for the consumer.

**Do:**
- Treat the consumer-server interaction as stateless; the consumer passes state on every request.
- Convey cache hints via HTTP headers (Cache-Control, ETag).
- Hide implementation layers behind the uniform interface.
- Return parsable representations (JSON, not application/pdf) for system-to-system exchanges.

**Don't:**
- Assume REST means CRUD over arrays — REST's power is in the resource model + verbs + representations.

**Code:**
```http
GET http://mastering-api.com/attendees
Accept: application/json
200 OK
Content-Type: application/json
{ "displayName": "Jim", "id": 1 }
```
*Ref: Mastering Api Architecture.md — "Introduction to REST" / "Introduction to REST and HTTP by Example"*

### 6. Richardson Maturity Model
**Principle:** Aim for Level 2 (verbs over resource URIs) in nearly every modern API; Level 3 (HATEOAS) is rarely worth the complexity for service-to-service calls.

**Do:**
- Move past Level 0 (RPC over HTTP, single URI) into Level 1 by modeling individual resources.
- Reach Level 2 by using GET/POST/PUT/DELETE against resource URIs.
- Reserve Level 3 (HATEOAS) for highly fluid UIs where the navigator gains value.

**Don't:**
- Stay at Level 0 — it offers none of REST's coupling benefits.
- Force HATEOAS on internal services — short-circuited by static specs and adds chattiness.

**Code:**
```text
Level 0 - HTTP/RPC      One URI; RPC semantics over HTTP.
Level 1 - Resources     Multiple URIs model resources (GET /attendees/1).
Level 2 - Verbs         Methods/verbs give idempotency + cache semantics
                        (DELETE /attendees/1, PUT /attendees/1).
Level 3 - Hypermedia    HATEOAS responses describe navigable actions.
                        "Rarely used in modern RESTful HTTP services."
```
*Ref: Mastering Api Architecture.md — "The Richardson Maturity Model"*

### 7. Adopt a Published REST Standard Early
**Principle:** REST is intentionally loose — choose a published standard (e.g., Microsoft REST API Guidelines, RFC-2119 verb levels) before your first API ships.

**Do:**
- Pick a standard matching your culture / formats; extend it with a domain data dictionary.
- Use a `MUST`/`SHOULD`/`SHOULD NOT`/`MUST NOT` vocabulary so contracts are unambiguous.
- Be critical of existing APIs against the chosen standard before adopting them.

**Don't:**
- Treat REST as "POST with JSON" and let inconsistencies compound.
- Wait until breaking-change pain forces a retrofit.

**Code:**
```text
ADR Guideline: API Standards
Decision:       Which API standard should we adopt?
Discussion:     - Existing org standards re-usable externally?
                - Third-party identity standards to align with?
                - Cost (incompat / churn) of having NO standard?
Recommendation: Pick a standard matching your culture + existing formats.
                Be prepared to evolve it with domain amendments. Start EARLY
                to avoid breaking consumers later for consistency.
```
*Ref: Mastering Api Architecture.md — "ADR Guideline: Choosing an API Standard"*

### 8. PII Hygiene in URLs
**Principle:** Personally Identifiable Information (emails, names) MUST NOT appear in URL paths or query strings — intermediaries, browser histories, and server logs will persist them.

**Do:**
- Use opaque server-generated IDs in URIs.
- Treat PII as request/response body only.
- Audit logs for accidental PII capture from upstream gateways.

**Don't:**
- Use `email` as a path segment ("/users/jim@mastering-api.com").
- Trust that HTTPS alone keeps URLs out of logs.

**Code:**
```http
POST http://mastering-api.com/attendees
{ "displayName": "Jim", "givenName": "James",
  "surname": "Gough", "email": "jim@mastering-api.com" }
201 CREATED
Location: http://mastering-api.com/attendees/1
```
*Ref: Mastering Api Architecture.md — "REST API Standards and Structure"*

### 9. Collections and Pagination (Wrap in Object)
**Principle:** Return collections wrapped in an object from day one — adding `@nextLink`/`@odata.nextLink` later to a bare array would break every consumer.

**Do:**
- Wrap collections: `{"value": [...], "@nextLink": "..."}`.
- Adopt `@nextLink` (or vendor equivalent) for opaque next-page URLs.
- Plan pagination in the first release; retrofitting it is a breaking change.

**Don't:**
- Ship `GET /attendees` returning a raw JSON array.
- Make pagination optional "for now" — every consumer will assume the bare array is the contract.

**Code:**
```http
GET http://mastering-api.com/attendees
200 OK
{ "value": [ { "displayName": "Jim", "id": 1 } ],
  "@nextLink": "{opaqueUrl}" }
```
*Ref: Mastering Api Architecture.md — "Collections and Pagination"*

### 10. OData-Style Filter Expressions
**Principle:** Standardize filtering on a known expression language (OData: `$filter`) so behavior is predictable across services.

**Do:**
- Adopt OData or equivalent for consistency.
- Quote string literals: `$filter=displayName eq 'Jim'`.
- Use `eq`, `ne`, `gt`, `lt`, `and`, `or`, `in` operators.

**Don't:**
- Invent custom query DSLs per service — fragmented filtering is a developer experience killer.

**Code:**
```http
GET http://mastering-api.com/attendees?$filter=displayName eq 'Jim'
```
*Ref: Mastering Api Architecture.md — "Filtering Collections"*

### 11. Error Handling: Honest Status Codes + InnerError
**Principle:** Return accurate HTTP status codes, consistent error shapes, and NEVER leak stack traces or PII to external consumers — use `InnerError` for internal debug detail.

**Do:**
- Use 2xx for success, 3xx for redirects (libraries may auto-follow), 4xx for client error, 5xx for server error.
- Document what a 5xx means: "in a payment system, does 500 mean the payment went through?"
- Strip `InnerError` from external responses; preserve it for debugging internally.

**Don't:**
- Return success (`200 OK`) with an error body.
- Echo stack traces or framework internals to the caller.

**Code:**
```text
"Non-success conditions — developers SHOULD be able to write one piece of
 code that handles errors consistently."

Recommendations:
  - Accurate status codes MUST be provided.
  - Strip stack traces & sensitive info before the response leaves the producer.
  - 5xx often triggers client retries; document the idempotency assumption.
```
*Ref: Mastering Api Architecture.md — "Error Handling"*

### 12. OpenAPI as Infrastructure, Not Afterthought
**Principle:** OpenAPI Specifications (OAS) are the contract, the documentation, the mock, the test generator, and the change detector — treat them as a living artifact.

**Do:**
- Share OAS to consumers from day one.
- Generate client SDKs and server stubs from it.
- Run `openapi-diff` in CI to detect breaking changes.
- Use `swagger-request-validator` to validate live exchanges.

**Don't:**
- Conflate "spec-first" with "behavior-first" — OAS captures shape, not semantics. Pair it with contract tests.

**Code:**
```java
// Using the location of the specification create an interaction validator.
// Base path override helps when used behind a gateway/proxy.
final OpenApiInteractionValidator validator = OpenApiInteractionValidator
 .createForSpecificationUrl(specUrl)
 .withBasePathOverride(basePathOverride)
 .build();
// Requests and Response objects can be converted or created using a builder
final ValidationReport report = validator.validate(request, response);
if (report.hasErrors()) {
 // Capture or process error information
}
```
*Ref: Mastering Api Architecture.md — "OpenAPI Validation"*

### 13. openapi-diff in CI: Catching Breaking Changes
**Principle:** Run `openapi-diff` on every PR to fail the build when an API diff breaks backward compatibility — catch breakage before consumers do.

**Do:**
- Pipe two OpenAPI specs through Docker and parse the result.
- Block merges when "API changes broke backward compatibility".
- Use `--info` for friendly summaries when nothing broke.

**Don't:**
- Rely on humans to spot renamed fields, removed endpoints, or type changes.

**Code:**
```bash
# Breaking: givenName -> firstName (consumer loses data)
$ docker run --rm -t \
   -v $(pwd):/specs:ro \
   openapitools/openapi-diff:latest /specs/original.json /specs/first-name.json
==================================================================
- GET /attendees
   Schema: Broken compatibility
   Missing property: [n].givenName (string)
-- Result --
   API changes broke backward compatibility

# Backward compatible: add new field "age"
$ docker run --rm -t -v $(pwd):/specs:ro \
   openapitools/openapi-diff:latest --info /specs/original.json /specs/age.json
==================================================================
- GET /attendees
   Schema: Backward compatible
-- Result --
   API changes are backward compatible
```
*Ref: Mastering Api Architecture.md — "OpenAPI Specification and Versioning"*

### 14. Mocking & Examples from OAS
**Principle:** Use the `examples` block in OAS to drive mock servers — enables stakeholders to "try out" the API before the producer ships.

**Do:**
- Include realistic examples in every response shape.
- Validate examples with `openapi-examples-validator` (examples are strings; easy to drift out of sync).
- Use mock servers in developer portals so consumers can explore before integration.

**Don't:**
- Treat examples as decorative — they're a testable artifact.

**Code:**
```text
Tool: openapi-examples-validator
Validates that an example matches the OAS for the corresponding
request/response component of the API.

Tool: swagger-request-validator (Atlassian)
Validates JSON REST content; has adapters for popular test frameworks;
can build OpenApiInteractionValidator from a spec URL.
```
*Ref: Mastering Api Architecture.md — "Examples and Mocking"*

### 15. API Versioning Strategies
**Principle:** Pick a versioning approach (URI / header / query) before launch and treat it as a product feature with a consumer-comms plan.

**Do:**
- Couple versioning with SemVer (MAJOR.MINOR.PATCH).
- Pair major-version bumps with deprecation timelines, migration guides, usage telemetry.
- Use Minor versions for additive (backward-compatible) changes; Patch for fixes only.

**Don't:**
- Promise "we'll never break you" — design for inevitable breaking changes with versioning, not avoidance.

**Code:**
```text
Upgrade options when an API must change:
  1. New version in a new location
     - Older apps keep running; producer maintains N versions.
  2. Backward-compatible new version (additive only)
     - A field-name typo fix is BREAKING; additive changes only.
  3. Break compatibility — all consumers must upgrade
     - Triggers lockstep changes; coordinate downtime.

A realistic API platform uses a mix of all three. That mix requires versioning.
```
*Ref: Mastering Api Architecture.md — "API Versioning"*

### 16. Semantic Versioning for APIs
**Principle:** SemVer (MAJOR.MINOR.PATCH) gives producers a vocabulary and consumers a contract — use it everywhere an API is exposed.

**Do:**
- MAJOR: breaking change (consumer action required; migration guide).
- MINOR: additive, backward compatible (consumer does nothing).
- PATCH: bug fix only (no functional change).

**Don't:**
- Skip PATCH versions — they preserve traceability and reduce regression risk.

**Code:**
```text
SemVer rules for an API release:
- MAJOR: noncompatible changes. Migration guide required.
- MINOR: backward-compatible changes. Consumers can adopt passively.
- PATCH: bug fixes on the existing Major.Minor functionality.
Example: 1.5.1 = major 1, minor 5, patch upgrade of 1.
```
*Ref: Mastering Api Architecture.md — "Semantic Versioning"*

### 17. gRPC: Protobuf as the Schema of Truth
**Principle:** gRPC owns east-west high-throughput exchanges — its strength (strict typing, binary encoding, HTTP/2 multiplexing) is also its strictness (field numbers are part of the contract).

**Do:**
- Start services with `.proto` and generate stubs in every consumer language.
- Add new fields as optional; never reuse field numbers; never change field types.
- Document your compatibility rules in a CONTRIBUTING.md for the repo.

**Don't:**
- Remove fields, rename fields, change field numbers, or change types — all break the wire contract.
- Treat `.proto` like OpenAPI ordering — field numbers, not names, identify fields on the wire.

**Code:**
```protobuf
syntax = "proto3";
option java_multiple_files = true;
package com.masteringapi.attendees.grpc.server;

message AttendeesRequest { }

message Attendee {
 int32 id = 1;
 string givenName = 2;
 string surname = 3;
 string email = 4;
}

message AttendeeResponse {
 repeated Attendee attendees = 1;
}

service AttendeesService {
 rpc getAttendees(AttendeesRequest) returns (AttendeeResponse);
}
```
*Ref: Mastering Api Architecture.md — "Implementing RPC with gRPC"*

### 18. gRPC Backward Compatibility Rules
**Principle:** Field numbers are the wire contract; respect them or break every consumer.

**Do:**
- New field → assign a new number; mark as optional implicitly (proto3 default).
- Deprecated fields → mark `reserved 5;` and stop using the number.
- Test schema changes against all stored messages and stub clients.

**Don't:**
- Reorder fields in the source — proto source order can mismatch wire order.
- Rely on openapi2proto style "auto-rebuild a fresh `.proto` from OAS" — alphabetical renumbering breaks everyone.

**Code:**
```text
Compatibility rules for gRPC:
  ADD (new field, new number)        -> backward compatible
  REMOVE (delete a field)            -> BREAKING (use `reserved` instead)
  RENAME (change field name)         -> BREAKING (rename is wire-level delete)
  CHANGE TYPE (string -> int32)      -> BREAKING
  CHANGE FIELD NUMBER (3 -> 8)       -> BREAKING (number is the on-wire id)

"Restrictions of encoding with gRPC mean the definition must be very specific.
 REST and OpenAPI are quite forgiving as the specification is only a guide."
```
*Ref: Mastering Api Architecture.md — "Implementing RPC with gRPC"*

### 19. grpcurl: Command-Line gRPC Debugging
**Principle:** gRPC can't be curl'd from a browser — `grpcurl` (or `gRPC UI`) is the equivalent for service-to-service debugging.

**Do:**
- Install grpcurl in every CI / dev image.
- Use it for canary smoke tests when DNS resolves to a new pod.

**Don't:**
- Spend time wiring custom HTTP/2 probes — grpcurl is the standard.

**Code:**
```bash
$ grpcurl -plaintext localhost:9090 \
   com.masteringapi.attendees.grpc.server.AttendeesService/getAttendees
{
 "attendees": [
  { "id": 1, "givenName": "Jim", "surname": "Gough", "email": "gough@mail.com" }
 ]
}
```
*Ref: Mastering Api Architecture.md — "Implementing RPC with gRPC"*

### 20. Modeling Exchanges: REST vs gRPC Selection
**Principle:** REST fits north-south (low barrier, strong domain model); gRPC fits east-west (high traffic, controlled consumers, big payloads, HTTP/2 wins).

**Do:**
- Use REST when the consumer is external and discovery must be low-friction.
- Use gRPC when producer/consumer are both under your control and performance/bandwidth matter.
- Model them independently — don't generate one from the other if you can avoid it.

**Don't:**
- Use REST for internal high-volume microservices — text JSON parsing is a real cost.
- Use gRPC for browser-facing mobile clients without grpc-gateway or envoy translation.

**Code:**
```text
Exchange modeling factors:
  - North-south (external): low barrier entry, domain model matters most -> REST.
  - East-west (internal): high traffic, payload size, HTTP/2 benefits
                          (HTTP/2 binary compression + multiplexing) -> gRPC.
  - Vintage formats:        SOAP/XML, etc. - isolate and evolve (Ch 8).

"Designing microservices-based architecture (RPC) communication independently
 from the REST representation allows both APIs to evolve freely."
```
*Ref: Mastering Api Architecture.md — "Modeling Exchanges and Choosing an API Format"*

### 21. Don't Couple REST to gRPC via Generation
**Principle:** Generating gRPC from OpenAPI (or REST from gRPC via grpc-gateway) couples two independently-versioned surfaces — version one becomes hard.

**Do:**
- Design REST and gRPC services as siblings if you need both.
- Use `grpc-gateway` only when you have a hard "single source of truth" requirement AND ownership of versioning.

**Don't:**
- Use `openapi2proto` blindly — alphabetical field reordering breaks wire contracts.

**Code:**
```protobuf
// grpc-gateway: reverse-proxy REST from a .proto using HTTP annotations
import "google/api/annotations.proto";
service AttendeesService {
 rpc getAttendees(AttendeesRequest) returns (AttendeeResponse) {
        option(google.api.http) = {
                get: "/attendees"
        };
 }
}
```
*Ref: Mastering Api Architecture.md — "Multiple Specifications"*

### 22. HTTP/2 & Multiplexing for East-West
**Principle:** HTTP/2's binary framing and multiplexing let many requests share one connection — measure before claiming REST is "fast enough".

**Do:**
- Default east-west services to HTTP/2 (gRPC already does).
- Measure parsing cost of large JSON in your language (Java/Python are worse than Go).
- Consider async gRPC streams for huge exchanges.

**Don't:**
- Use HTTP/1.x in new internal services — sequential request/response chains cost network RTTs.

**Code:**
```text
HTTP/2 multiplexing example:
  20 individual attendees as HTTP/1 requests -> 20 TCP handshakes.
  20 individuals as HTTP/2 over one conn    -> 1 connection, 20 streams.

gRPC uses HTTP/2 + Protobuf binary by default; bandwidth matters
most when "content payloads increase significantly in size".

Watch for HTTP/3 (QUIC over UDP) - already supported by 70%+ browsers.
```
*Ref: Mastering Api Architecture.md — "HTTP/2 Performance Benefits"*

### 23. Test Quadrant: Q1–Q4 Coverage Planning
**Principle:** Tests are a 2×2: business-facing vs technology-facing × supporting the team vs critiquing the product. Use all four, with explicit intent.

**Do:**
- Q1 (tech-supporting): unit/component tests, automated.
- Q2 (biz-supporting): pair with stakeholders; BDD scenarios.
- Q3 (biz-critiquing): exploratory + scenario (now automatable).
- Q4 (tech-critiquing): performance, security, scalability.

**Don't:**
- Re-read Lisa Crispin/Janet Gregory advice as a sequence — quadrants are not ordered.
- Skip Q3/Q4 just because Q1/Q2 "feel safe".

**Code:**
```text
Test Quadrant (Crispin & Gregory)
         business-facing        |  business-facing
critique the product           |  support the team
  Q3 - functional acceptance / |  Q2 - story tests /
       exploratory             |       pair-with-biz
  Q4 - performance / security /|  Q1 - unit / component
       SLA                     |

External quality = top half; Internal quality = bottom half.
```
*Ref: Mastering Api Architecture.md — "Test Quadrant"*

### 24. Test Pyramid: Many Units, Few E2E
**Principle:** Bottom = many fast unit tests; middle = fewer service/component tests; top = very few, high-value E2E tests.

**Do:**
- Drive unit tests with TDD.
- Use Test Doubles (stubs return canned values; mocks verify behavior) to keep units isolated.
- Limit E2E to core user journeys.

**Don't:**
- Invert the pyramid (ice-cream cone) chasing "more confidence" — confidence per cost plummets.

**Code:**
```text
Test Pyramid:
        /\
       /  \         UI / E2E  (few, slow, brittle, high ROI on journeys)
      / E2E \
     /------\
    /        \
   / Service  \     component / contract / integration
  /   Tests    \    (medium isolation + medium confidence)
 /--------------\
/                \
/      Unit        \  small, isolated, fast
/____________________\

Alternative shapes (diamond, trophy) are valid contextually;
pyramid is the recommended default.
```
*Ref: Mastering Api Architecture.md — "Test Pyramid"*

### 25. ADR for Test Strategy: Always Pick the Pyramid
**Principle:** Always pair the test quadrant with the test pyramid. Start with the pyramid at minimum, even if the quadrant is team-impossible today.

**Do:**
- Choose a strategy explicitly and document it.
- Account for "all parties having time to discuss" — quadrant fails silently when stakeholders are unavailable.

**Don't:**
- Run E2E only because "they give confidence".

**Code:**
```text
ADR Guideline: Testing Strategies
Decision: Which testing strategy should be part of our process?
Discussion:
  - Stakeholder availability (can you actually pair-with-biz?)
  - Skills & experience (TDD, BDD, proptest?)
  - Internal practices and org constraints
Recommendation:
  USE both test quadrant AND test pyramid.
  At minimum use the test pyramid (automated side of the quadrant).
  You will ALWAYS need someone to help guide the product direction.
```
*Ref: Mastering Api Architecture.md — "ADR Guideline for Testing Strategies"*

### 26. Contract Testing: Why It's Preferable
**Principle:** Contracts verify producer/consumer interaction locally — faster, cheaper, catches breakage earlier than full integration.

**Do:**
- Publish contracts to a shared store (Git, Artifactory, or Pact Broker).
- Auto-generate stub servers for consumers from the contract.
- Run producer verification on every consumer-submitted contract.

**Don't:**
- Treat "conforms to schema" as the same as "fulfills contract" — schemas check shape; contracts check behavior.

**Code:**
```groovy
// Pact-style contract example: GET /conference/1234/attendees
Contract.make {
 request {
   description('Get a list of all the attendees at a conference')
   method GET()
   url '/conference/1234/attendees'
   headers { contentType('application/json') }
 }
 response {
   status OK()
   headers { contentType('application/json') }
   body(
     value: [
       $( id: 123456, givenName: 'James',  familyName: 'Gough'  ),
       $( id: 123457, givenName: 'Matthew',familyName: 'Auburn' )
     ]
   )
 }
}
```
*Ref: Mastering Api Architecture.md — "Contract Testing"*

### 27. Producer vs Consumer-Driven Contracts (Pact)
**Principle:** Use Producer Contracts when the audience is large/external (Microsoft Graph); use CDC when consumers and producers share an organization.

**Do:**
- Default to CDC inside the org — it forces the conversation between consumer and producer.
- Start with Producer Contracts to seed the practice; evolve to CDC.

**Don't:**
- Force CDC for purely external APIs where consumers cannot realistically review PRs.

**Code:**
```text
Producer Contracts:
  Producer defines; used when API is consumed by many external parties.
  Real-world example: Microsoft Graph API has thousands of consumers
  globally - they cannot adjust its contract.

Consumer-Driven Contracts (CDC):
  Consumer writes the contract reflecting what they need.
  Pull request submitted to producer; conversation begins; producer
  accepts or rejects.

"CDC is very much an interactive and social process."
```
*Ref: Mastering Api Architecture.md — "How a Contract Is Implemented"*

### 28. Pact Broker: Centralized Contract Distribution
**Principle:** Use a contract broker when you have a large/evolving contract surface — broker shows producer-validated contracts and which consumers depend on them.

**Do:**
- Use the Pact Broker (or equivalent) as the single source for verified contracts.
- Generate network diagrams of who depends on who.
- Integrate broker with CI/CD to surface "will this change break a consumer?".

**Don't:**
- Store all contracts in a central Git repo with no review — likely to add unimplementable contracts.

**Code:**
```text
Contract storage options:
  - Alongside producer code in Git
       + Producer controls acceptance
       - Hard to discover all services using contracts
  - Centralized Git repo
       + Visibility
       - Easy to push contracts a producer has no intention of fulfilling
  - Pact Broker (recommended when compatible)
       + Shows producer-verified contracts
       + Network diagram of consumers
       + CI/CD integration
       + Track invalidation across versions
```
*Ref: Mastering Api Architecture.md — "API contracts storage and publishing"*

### 29. REST-Assured Component Tests
**Principle:** Component tests verify an API end-to-end in-process with external dependencies mocked — the lowest-cost place to assert behavior.

**Do:**
- Mock the DAO / database, not the network stack.
- Assert behavior (calls were made, status codes, headers), not just shapes.
- Cover: correct status, rejection of bad input, entitlements check, empty-dataset handling, Location header on POST.

**Don't:**
- Use real databases — that's integration, not component.
- Mock + assert only the response shape — that's contract testing.

**Code:**
```java
@Test
void response_for_attendees_should_be_200() {
  given()
   .header("Authorization", VALID_CREDENTIAL)
   .when()
   .get("/conference/conf-1/attendees")
   .then()
   .statusCode(HttpStatus.OK.value());
}

@Test
void response_for_attendees_should_be_403() {
  given()
   .header("Authorization", INVALID_CREDENTIAL)
   .when()
   .get("/conference/conf-1/attendees")
   .then()
   .statusCode(HttpStatus.FORBIDDEN.value());
}
```
*Ref: Mastering Api Architecture.md — "Case Study: Component Test to Verify Behavior"*

### 30. Stub Servers: Generated > Hand-Rolled > Recorded
**Principle:** Generated stubs from contracts are most accurate; hand-rolled stubs drift; recordings are accurate at capture time but stale.

**Do:**
- Generate stubs from the contract (Pact, WireMock).
- Verify stubs against the producer's actual responses on every contract refresh.

**Don't:**
- Hand-roll responses like the typo-prone JSON below — errors hide invisibly.

**Code:**
```jsonc
// ANTI-PATTERN: hand-rolled stub with errors hidden in plain sight
{
 "values": [
  { "id": 123456, "givenName": "James",  "familyName": "Gough"  },
  { "id": 123457, "givenName": "Matthew","familyNane": "Auburn" },  // typo
  { "id": 123456, "givenName": "Daniel", "familyName": "Bryant" }   // duplicate id
 ]
}
```
*Ref: Mastering Api Architecture.md — "Using Stub Servers: Why and How"*

### 31. WireMock & Test Recordings
**Principle:** Recordings (e.g., WireMock mappings) capture traffic verbatim — more accurate than hand-rolling but become stale.

**Do:**
- Refresh recordings on every producer integration test.
- Scrub PII before persisting mappings to source control.

**Don't:**
- Use recordings against production without scrubbing — PII will land in source.

**Code:**
```text
Recorder-based stubbing flow:
  [Producer] --[Capture tool]--> [Mappings file (.json)]
                                          |
                                          v
                                  [Stub server]
                                          |
[Consumer test] --- request ---> [Stub server matches mapping]
                                          |
                                  returns mapped response.

Real examples: WireMock (Java), Camouflage (TypeScript).
```
*Ref: Mastering Api Architecture.md — "Using Stub Servers: Why and How"*

### 32. Testcontainers: Real Deps, Local Speed
**Principle:** Spin up real database/message-broker images in Docker for integration tests — the realism of integration at the cost of unit.

**Do:**
- Use Testcontainers for DAOs, Kafka, Redis, NGINX.
- Trust the container's owner — only verify the boundary, not its internals (don't subscribe to Kafka to verify you published).

**Don't:**
- Replace contracts with Testcontainers — they catch different things.
- Use mocks or in-memory DBs when the real one is available as a container.

**Code:**
```text
Testcontainers use cases in the case study:
  1. gRPC stub server as a container
     - Stub is generated, packaged, published.
     - Consumer devs call the real stub via container locally.

  2. Real DB (instead of mock or H2):
     - With mocks you can mock the wrong value.
     - With H2 you assume impl = real DB.
     - With Testcontainers -> same version as prod -> reliable boundary test.

Other common deps: Kafka, Redis, NGINX.
```
*Ref: Mastering Api Architecture.md — "Containerizing Test Components: Testcontainers"*

### 33. End-to-End Tests: Boundaries, Realism, Real Payloads
**Principle:** E2E tests must traverse meaningful boundaries with realistic payloads — and only for critical journeys.

**Do:**
- Launch the Attendee service + DB, but stub things outside your domain (e.g., external S3).
- Use production-sized payloads (catches buffer issues a 1-row payload won't).
- Run in like-for-like environments for performance E2E.

**Don't:**
- Try to clone a third-party UI — futile and out of your domain.
- Disable security (TLS, auth) in E2E — misrepresents metrics.

**Code:**
```text
Performance tools referenced:
  Gatling, JMeter, Locust, K6

Performance tests must run on like-for-like hardware of production.
Driving BDD-style scenario tests is recommended for user-journey E2E.
```
*Ref: Mastering Api Architecture.md — "End-to-End Testing"*

### 34. API Gateway: Single Point of Entry
**Principle:** An API gateway is a reverse proxy with API-specific capabilities (routing, authn/z, rate limiting, observability, lifecycle) deployed at the system edge.

**Do:**
- Use a gateway when cross-cutting concerns (auth, rate limiting, observability) need centralization.
- Pick gateway type to match scale: Enterprise / Microservice / Service-Mesh.

**Don't:**
- Use a gateway for everything — start with a proxy or LB if cross-cutting is small.

**Code:**
```text
Capability comparison:
                Reverse proxy  Load balancer  API gateway
Single backend  *              *              *
TLS/SSL         *              *              *
Multiple back.  *              *              *
Service disc.   *              *              *
API composition                                 *
Authorization                                   *
Retry logic                                     *
Rate limiting                                   *
Logging+tracing                                 *
Circuit breaking                                *
```
*Ref: Mastering Api Architecture.md — "What Functionality Does an API Gateway Provide?"*

### 35. Proxy vs Load Balancer vs Gateway Selection
**Principle:** Use the simplest technology that meets your requirements.

**Do:**
- Pick a proxy for single backend + simple routing.
- Pick a load balancer when spreading load across many identical backends.
- Pick an API gateway when API-specific features (auth, lifecycle, monetization) are needed.

**Don't:**
- Skip "is there an existing org-wide mandate?" check first.

**Code:**
```text
ADR Guideline: Proxy / LB / API Gateway
Decision: Which should we use for ingress?
Discussion:
  - Single backend or many?
  - Cross-cutting requirements (authn/z, rate limit)?
  - API management needs (keys, monetization)?
  - Existing edge stack in the org?
Recommendation:
  Always use the simplest solution for your requirements.
  Advanced cross-cutting -> API gateway.
  Enterprise -> API Management-capable gateway.
  Always check existing mandates first.
```
*Ref: Mastering Api Architecture.md — "Guideline: Proxy, Load Balancer, or API Gateway"*

### 36. API Gateway History & Generations
**Principle:** Knowing the lineage (HW LB → ADCs → 1st-gen → 2nd-gen cloud-native → Service-Mesh gateways) explains today's confusion and avoids past anti-patterns.

**Do:**
- 1990s HW LB (F5) for TCP spreading.
- 2000s SW LB (HAProxy, NGINX) for cheaper flexibility.
- 2000s ADCs for L7 features on commodity HW.
- 2010s 1st-gen API Gateways (Kong, Apigee) targeting developers.
- 2015+ 2nd-gen microservices gateways (Ambassador, Gloo, Traefik) on Envoy.
- 2020+ Service-Mesh gateways (Istio, Consul).

**Don't:**
- Re-implement L7 routing at every tier — pick one layer to own it.

**Code:**
```text
Historical progression of edge tech:
  1990s  -> F5 HW load balancers (TCP/IP layer)
  2001   -> HAProxy (open source SW LB)
  2002   -> NGINX
  Mid-2000s -> ADCs (compression, SSL offload, caching, mux) by F5/Citrix/Cisco
  Early 2010s -> Kong (Lua/OpenResty), Apigee, 3Scale  -> 1st-gen API gateways
  2013   -> Docker; 2015 -> Kubernetes
  Mid-2010s -> Microservices gateways: Ambassador (Envoy),
              Gloo, Traefik, Tyk
  2020s  -> Service-mesh gateways (Istio, Consul)
```
*Ref: Mastering Api Architecture.md — "A Modern History of API Gateways"*

### 37. API Gateway Taxonomy
**Principle:** Three flavors exist (Enterprise, Microservices, Service-Mesh) — choose by ownership, scope, and APIM requirements.

**Do:**
- Enterprise gateway (Kong, Apigee) for monetization + lifecycle + developer portal.
- Microservices gateway (Ambassador, Gloo) for routing microservices, open source.
- Service-mesh gateway for ingress into a mesh — only if you're already running a mesh.

**Don't:**
- Choose a service-mesh gateway "to save on ops" if you don't otherwise need a mesh.

**Code:**
```text
| Use case               | Enterprise GW     | Microservices GW  | Service-Mesh GW |
| Primary purpose        | Expose & manage   | Expose services   | Expose mesh     |
| Publishing             | Admin API / mgmt  | Service team,     | Service team,   |
|                        | team via pipeline | declarative code  | declarative     |
| Monitoring             | Admin/operations  | Developer (latency| Platform        |
|                        | (meter per cons.) | / traffic / err)  | (util / sat)    |
| Issue handling         | L7 error pages    | L7 + failover +   | L7 + traffic    |
|                        |                   | payload + shadow  | tapping         |
| Testing                | Multiple envs,    | Canary + dark     | Canary only     |
|                        | CDC versioning    | launch + contract |                 |
| Local dev              | Vagrant/Docker,   | Container/K8s     | K8s             |
|                        | language mocks    |                   |                 |
| UX                     | Web admin UI,     | IaC / CLI,        | IaC / CLI,      |
|                        | developer portal  | simple portal     | limited catalog |
```
*Ref: Mastering Api Architecture.md — "Comparing API Gateway Types"*

### 38. Ambassador Edge Stack Mapping Configuration
**Principle:** The path-prefix Mapping CRD is the most common routing primitive — `service.namespace:port` with optional rewrite & host.

**Do:**
- Use `prefix: /` for default route (legacy).
- Use specific paths (`/attendees`) for new microservices.
- Use `rewrite: /` to strip the matching prefix when the upstream expects `/`.

**Don't:**
- Route on payload content — leaks domain coupling into the gateway and burns CPU.

**Code:**
```yaml
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: legacy-conference
spec:
 hostname: "*"
 prefix: /
 rewrite: /
 service: conferencesystem.legacy:8080
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: attendees
spec:
 hostname: "*"
 prefix: /attendees
 rewrite: /
 service: attendees.nextgen:8080
# Host-based routing
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: attendees-host
spec:
 hostname: "attendees.conferencesystem.com"
 prefix: /
 service: attendees.nextgen:8080
```
*Ref: Mastering Api Architecture.md — "Configuring Mappings from URL Paths to Backend Services"*

### 39. Coupling Reduction: Facade/Adapter at the Edge
**Principle:** The gateway should make backend identity opaque to clients — change backend location, language, or topology without touching consumers.

**Do:**
- Use the gateway as a facade (single entry, stable contract).
- Use the gateway as an adapter when translating protocols (SOAP → REST).

**Don't:**
- Put business logic in the gateway — that recreates the ESB antipattern.

**Code:**
```text
Loose coupling / high cohesion / information hiding:

A facade defines a new simpler interface for a system.
An adapter reuses an old interface to support interoperability.

Gateway as adapter -> clients integrate with a stable contract;
backend services can change location, language, framework.

"When you have a technology hammer, everything looks like a nail" —
the API gateway is not the place for business logic.
```
*Ref: Mastering Api Architecture.md — "Reduce Coupling: Adapter/Facade Between Frontends and Backends"*

### 40. Aggregation, Translation, and Protocol Conversion
**Principle:** Use the gateway for aggregation/translation only when you understand the cost.

**Do:**
- Parallelize independent calls in the gateway to reduce fan-out latency.
- Use GraphQL upstream of multiple services if consumers need flexible queries.

**Don't:**
- Couple gateway ordering decisions with backend idempotency assumptions.
- Implement heavy payload translation in a hot path (compute cost).

**Code:**
```text
Aggregation / translation at the edge:
  + Orchestrating concurrent API calls.
  + Protocol translation (e.g., SOAP -> REST).

Risks:
  - Business logic spreads across gateway + backend.
  - Operation coupling: changing call order can change results when
    calls are NOT idempotent.
  - Translation has design, implementation, testing, and compute cost.
```
*Ref: Mastering Api Architecture.md — "Simplify Consumption: Aggregating/Translating Backend Services"*

### 41. Edge Threat Detection & Rate Limiting
**Principle:** The gateway is typically the first line of defense for north-south — apply WAF, authn/z, IP lists, rate limiting, load shedding.

**Do:**
- Rate-limit per IP / per client ID / per geo.
- Implement load shedding (reject when DB or workers are saturated).
- Fail closed for security-sensitive systems; fail open for availability-critical (medical emergency data).

**Don't:**
- Default to "no rate limiting" — DoS becomes trivial.

**Code:**
```text
Rate-limit strategies:
  Fixed window    e.g., 2,400 requests/day
  Sliding window  e.g., 100 requests in the last hour
  Token bucket    Bucket of tokens; each request takes one;
                  refilled periodically
  Leaky bucket    Same as token bucket, but processed at a fixed rate

Load shedding example: when DB at capacity or no worker threads -> reject.
```
*Ref: Mastering Api Architecture.md — "Protect APIs from Overuse and Abuse: Threat Detection and Mitigation"*

### 42. Edge Observability: Correlation IDs
**Principle:** The edge is the natural place to inject correlation IDs that propagate across services.

**Do:**
- Have the gateway inject a request ID (e.g., OpenZipkin b3 headers).
- Ensure each upstream service propagates the header.
- Emit RED metrics at the edge for top-line visibility.

**Don't:**
- Rely on application-emitted IDs as the only correlation — edge-emitted IDs are universal.

**Code:**
```text
Edge-stack observability layers:
  CDN / WAF -> metrics on top of CDN/WAF hits
  Edge LB   -> throughput / connection metrics
  Gateway   -> per-route requests, latency, status codes
  Services  -> internal RED/golden-signal metrics
  Mesh      -> service-to-service mesh metrics

Correlation IDs are typically injected by the API gateway and propagated
by each upstream service (e.g., OpenZipkin b3 or W3C tracecontext).
```
*Ref: Mastering Api Architecture.md — "Understand How APIs Are Being Consumed: Observability"*

### 43. API Lifecycle Management
**Principle:** Treat APIs as products with a full lifecycle: build → test → publish → secure → manage → onboard → analyze → promote → monetize → retirement.

**Do:**
- Build a developer portal.
- Document and publish retirement timelines.
- Track metrics per API consumer.

**Don't:**
- Expose undocumented APIs ("shadow APIs") — they become attack surface.

**Code:**
```text
10 top stages of an API lifecycle (Axway / industry consensus):
  1. Building      Designing & building the API
  2. Testing       Verifying functionality, performance, security
  3. Publishing    Exposing APIs to developers
  4. Securing      Mitigating security risks
  5. Managing      Maintaining + managing APIs to meet business reqs
  6. Onboarding    OpenAPI / AsyncAPI doc + portal + sandbox
  7. Analyzing     Observability + monitoring analysis
  8. Promoting     Listing in API marketplace
  9. Monetizing    Charging for / collecting revenue from API use
 10. Retirement    Supporting deprecation + removal
```
*Ref: Mastering Api Architecture.md — "Manage APIs as Products: API Lifecycle Management"*

### 44. Service Mesh Fundamentals
**Principle:** A service mesh intercepts every service-to-service call through sidecar proxies (data plane) coordinated by a control plane — for traffic, observability, and security.

**Do:**
- Use a mesh when you have many services, polyglot stacks, or need consistent cross-cutting concerns.
- Expect to grow into it: start with routing, then observability, then security.

**Don't:**
- Adopt a mesh for 2-3 services — operational overhead dwarfs benefit.
- Use it as a replacement for an API gateway — different scope (east-west vs north-south).

**Code:**
```text
Service mesh topology:
  +------------- Control plane ---------------+
  | (istiod, linkerd-control-plane, consul)   |
  +------|-------|-------|-------|-------------+
         |       |       |       | (xDS / policy)
         v       v       v       v
  +------+--+ +---+----+ +--+----+ +---+------+
  | svc A  |  | svc B  |  | svc C |  | svc D    |
  | +side  |  | +side  |  | +side |  | +side    |
  +--------+  +--------+  +-------+  +----------+
       ^          ^           ^         ^
       +----------+-----------+---------+  (mTLS, retries, telemetry)
```
*Ref: Mastering Api Architecture.md — "What Is Service Mesh?"*

### 45. Sidecar vs Full Proxy
**Principle:** Service mesh data planes are full proxies (two network stacks, client-side and server-side) — more powerful, more expensive than half proxies.

**Do:**
- Use full proxies for full traffic manipulation (retries, mTLS, header rewrites).
- Account for the resource cost in capacity planning.

**Don't:**
- Assume sidecar overhead is negligible — 100 pods × 60MB = 6GB just for proxies.

**Code:**
```text
"Full proxy" vs "half proxy":
  A full proxy:
    - Two network stacks (client + server)
    - Manipulates traffic on both sides
    - Required for retries, mTLS, header injection on both sides
    - Trade-off: MORE CPU/MEM per pod, MORE latency hop

Service mesh data planes operate as full proxies, enabling
retries, timeouts, circuit breaking, mTLS -- all centrally managed.
```
*Ref: Mastering Api Architecture.md — "Service Meshes Use Full Proxies to Intercept All Service Traffic"*

### 46. 8 Fallacies of Distributed Computing
**Principle:** All eight fallacies bite in modern systems; design for failure.

**Do:**
- Assume: network not reliable, latency > 0, bandwidth finite, network insecure, topology changes, multiple admins, transport cost > 0, network heterogeneous.
- Bake retries, timeouts, circuit breakers, fallbacks into the mesh.

**Don't:**
- Treat distributed computing as a special case — these are defaults.

**Code:**
```text
The 8 Fallacies of Distributed Computing (Peter Deutsch, Sun, 1990s):
  1. The network is reliable.
  2. Latency is zero.
  3. Bandwidth is infinite.
  4. The network is secure.
  5. Topology doesn't change.
  6. There is one administrator.
  7. Transport cost is zero.
  8. The network is homogeneous.

Peter: these "all prove to be false in the long run and all cause big
trouble and painful learning experiences."
```
*Ref: Mastering Api Architecture.md — "Early History and Motivations"*

### 47. Istio VirtualService & DestinationRule
**Principle:** Istio's two routing CRDs together enable canary, A/B testing, and version subsets — model the version semantics in `DestinationRule`, the split in `VirtualService`.

**Do:**
- Define subsets per version (v1, v2) in DestinationRule.
- Drive the split via VirtualService.
- Combine with retries, timeouts, outlier detection.

**Don't:**
- Drive subsets only by labels — be explicit (`labels: version: v2`).

**Code:**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
 name: attendees
spec:
 hosts:
 - attendees
 http:
 - route:
   - destination:
      host: attendees
      subset: v1
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
 name: attendees
spec:
 host: attendees
 subsets:
 - name: v1
   labels:
    version: v1
 - name: v2
   labels:
    version: v2
```
*Ref: Mastering Api Architecture.md — "Routing with Istio"*

### 48. Linkerd Observability (Golden Signals Auto)
**Principle:** Linkerd provides golden-signal metrics, TCP metrics, and service topology out of the box — no application code change.

**Do:**
- Install `linkerd viz` and use the dashboard during pre-prod soak.
- Wire Prometheus to scrape Linkerd's built-in instance for SLOs.

**Don't:**
- Skimp on Linkerd's "Service Profiles" for per-route metrics.

**Code:**
```bash
linkerd viz install | kubectl apply -f -
linkerd viz dashboard
```
*Ref: Mastering Api Architecture.md — "Observing Traffic with Linkerd"*

### 49. Consul ServiceIntentions for Zero-Trust mTLS
**Principle:** Deny-all by default; explicitly `allow` each required pair — identity-based, enforced by the sidecar.

**Do:**
- Start with a `deny-all` wildcard intention.
- Add one intention per allowed pair (e.g., legacy → attendee, attendee → sessions).
- Encode identities as SPIFFE X.509 certificates.

**Don't:**
- Rely on "we trust the network" — use the mesh for zero trust.

**Code:**
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata:
 name: deny-all
spec:
 destination:
   name: '*'
 sources:
   - name: '*'
   action: deny
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata:
 name: legacy-app-to-attendee
spec:
 destination:
   name: attendee
 sources:
   - name: legacy-conf-app
   action: allow
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata:
 name: attendee-to-sessions
spec:
 destination:
   name: sessions
 sources:
   - name: attendee
   action: allow
```
*Ref: Mastering Api Architecture.md — "Network Segmentation with Consul"*

### 50. Proxyless gRPC (Service Mesh Future)
**Principle:** Sidecars are expensive at scale — proxyless gRPC connects gRPC libraries directly to the control plane (Traffic Director) via xDS.

**Do:**
- Use proxyless gRPC for resource-efficient, high-perf gRPC apps.
- Mix sidecar and proxyless services transparently (Traffic Director supports hybrid).

**Don't:**
- Force proxyless when you need non-gRPC traffic in the same mesh.

**Code:**
```text
Proxyless gRPC + Traffic Director:
  [App process]
     |
     | (gRPC library holds xDS client)
     v
  [Google Traffic Director / external control plane]
     |
     | global routing, regional failover
     v
  [Other gRPC apps + Envoy sidecars (hybrid)]

Use cases:
  - Resource efficiency in large meshes
  - High-performance gRPC apps
  - Mesh in environments where sidecars can't run
```
*Ref: Mastering Api Architecture.md — "Is the Future of Service Mesh Proxyless?"*

### 51. eBPF / Cilium Kernel-Based Mesh
**Principle:** Push networking concerns into the OS kernel via eBPF; per-node Envoy handles L7. Reduces latency and resource use.

**Do:**
- Evaluate Cilium for greenfield clusters when sidecar cost is too high.
- Combine with a single Envoy per node for L7 features.

**Don't:**
- Assume eBPF support in all kernels; verify.

**Code:**
```text
eBPF / Cilium data plane:
  +---- Node (shared kernel) ----+
  |  [Cilium agent]  [Envoy L7]  |
  |        |             |      |
  |   eBPF programs   app/sidecar|
  +--------------------------+
                ^
                | kernel-level hooks
                v
   pods share the same kernel -> consistent enforcement

Goodbye Sidecars: kernel-level visibility/removal of L4 bypass risks.
```
*Ref: Mastering Api Architecture.md — "Sidecarless: Operating system kernel (eBPF) implementations"*

### 52. Mesh Anti-Patterns (ESB, Too Many Layers)
**Principle:** Avoid reusing mesh plug-ins as business-logic engines; avoid stacking gateways/meshes redundantly.

**Do:**
- Keep the mesh dumb (retries, mTLS, metrics) — only.
- Coordinate with lower-level networking (CNI, NetworkPolicy) to avoid duplicated circuit breakers.

**Don't:**
- Put payload transformation in WASM filters and call it "infrastructure".
- Run a service mesh "for the gateway feature alone" — install only what you need.

**Code:**
```text
Service mesh anti-patterns:
  - Mesh as ESB: business logic in Wasm / Lua filters.
  - Mesh as gateway: using only the mesh ingress -- lacks APIM features.
  - Too many networking layers: mesh on top of L4 LB on top of another
    proxy -- duplicate functionality, added latency, header stripping.

Best practice: all teams coordinate. Pick ONE source of truth per concern.
```
*Ref: Mastering Api Architecture.md — "Common Service Mesh Implementation Challenges"*

### 53. Gateway as Single Point of Failure
**Principle:** An API gateway is on the critical path of nearly all user traffic — design for HA, monitor rigorously, and own it with on-call.

**Do:**
- Multi-AZ / multi-region deployment; active-active if possible.
- Define SLOs and codify into SLAs.
- Run blameless postmortems.

**Don't:**
- Single gateway instance in one zone.
- Silence alerts to "reduce noise".

**Code:**
```text
Failure management for gateways (and meshes):
  Detect:  Health checks, RED/golden-signal metrics
           (USE method / RED method / Google's four golden signals).
  Own:     Clear owner team, defined on-call rotation.
  Resolve: Runbooks, escalation paths, blameless postmortems.
  Mitigate: HA topology, health-checked failover,
            active/passive or active/active.

Common failover pitfalls:
  - State migration bugs (sticky sessions break).
  - Geo mis-routing (EU users routed to US west).
  - Cascading failure from faulty leader election.
```
*Ref: Mastering Api Architecture.md — "API Gateway as a Single Point of Failure"*

### 54. Gateway Loopback Antipattern
**Principle:** Don't route internal service-to-service traffic back through the public gateway — egress + ingress costs, latency, and a real SPOF.

**Do:**
- Use Kubernetes DNS or the service mesh for internal service discovery.

**Don't:**
- Use the external FQDN for internal calls.

**Code:**
```text
Anti-pattern:
  [legacy app] --(public DNS)--> [API Gateway --> Attendee service]
  This means:
    - traffic leaves the cluster to come back in
    - extra latency
    - extra cost (cloud egress + ingress)
    - gateway is a SPOF for INTERNAL traffic
    - observability polluted by multiple cycles

Correct: use internal service discovery (K8s Service, mesh DNS).
```
*Ref: Mastering Api Architecture.md — "API Gateway Loopback"*

### 55. Turtles (Gateways) All the Way Down
**Principle:** Don't chain multiple gateways to "separate concerns" — coordination cost dwarfs theoretical cleanliness.

**Do:**
- One gateway tier at the edge; let internal routing use mesh + DNS.

**Don't:**
- Have separate "TLS gateway, auth gateway, logging gateway" — when one changes, all change.

**Code:**
```text
If one API gateway is good, more must be better, right?

Common pitfalls:
  - Coordination tax to release one simple upgrade
  - "Who owns tracing?" => understandability issues
  - Every network hop costs latency + failure chance

"One source of truth per concern" beats drawn-out ownership debates.
```
*Ref: Mastering Api Architecture.md — "Turtles (API Gateways) All the Way Down"*

### 56. Separating Deployment from Release
**Principle:** "Deployment" = code is running; "Release" = users see it. The two MUST be separable via feature flags and traffic management.

**Do:**
- Deploy all changes behind feature flags; release incrementally.
- Use Thoughtworks terminology strictly: Deployment ≠ Release.

**Don't:**
- Couple deploy and release — outages propagate and lockstep releases emerge.

**Code:**
```text
TechRadar (2016):

"We recommend strictly using the term Deployment when referring to the
act of deploying a change to application components or infrastructure.
The term Release should be used when a feature change is released to
end users, with a business impact.

Using techniques such as feature toggles and dark launches, we can
deploy changes to production systems more frequently without releasing
features."
```
*Ref: Mastering Api Architecture.md — "Separating Deployment and Release"*

### 57. Feature Flags: Granular + Tidy
**Principle:** Feature flags decouple deploy from release and enable per-user experiments — but every flag must be cleaned up.

**Do:**
- Use unique flag names; remove code paths when the flag is retired.
- Cache last-known flag value to survive a flag-service outage.
- Roll out in tiny batches and toggle back if KPIs drop.

**Don't:**
- Reuse flag names — Knight Capital's famous failure cost ~$460M.
- Make the flag service a single point of failure.

**Code:**
```java
LDUser user = new LDUser("jim@masteringapi.com");
boolean newAttendeesService =
 launchDarklyClient.boolVariation("user.enabled.modern", user, false);
if (newAttendeesService) {
 // Retrieves the attendee from the modern store
} else {
 // Retrieves the attendee from the legacy store
}
```
*Ref: Mastering Api Architecture.md — "Case Study: Feature Flagging"*

### 58. Canary Releases
**Principle:** Route a small slice (1–10%) of traffic to the new version; monitor and slowly increase — automate rollback on SLO breach.

**Do:**
- Start with 1–5% canary.
- Drive from a control plane (Argo, Istio, Spinnaker) — not from raw pod ratios.

**Don't:**
- Rely on pod-count ratios for traffic split (1 v2 of 100 means 1%, which is hard to dial).

**Code:**
```yaml
# Argo Rollouts canary example
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
 name: attendees
spec:
 replicas: 5
 strategy:
   canary:
     steps:
     - setWeight: 20
     - pause: {}
     - setWeight: 40
     - pause: {duration: 10}
     - setWeight: 60
     - pause: {duration: 10}
     - setWeight: 80
     - pause: {duration: 10}
 revisionHistoryLimit: 2
 selector:
   matchLabels:
     app: attendees-api
 template:
   metadata:
     labels:
       app: attendees-api
   spec:
     containers:
     - name: attendees
       image: jpgough/attendees:v1
```
*Ref: Mastering Api Architecture.md — "Canary Releases" / "Performing Rollouts with Argo Rollouts"*

### 59. Argo Rollouts AnalysisTemplate (Prometheus-Gated Promotion)
**Principle:** Replace manual `pause: {}` with metric-driven promotion — if success rate stays ≥ 0.95, continue; else abort.

**Do:**
- Encode SLOs (success rate, p99 latency) as `successCondition`.
- Tie the canary's success criteria to the same metrics you alert on.

**Don't:**
- Manually click "promote" when you have well-defined SLOs.

**Code:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
 name: success-rate
spec:
 args:
 - name: service-name
 - name: prometheus-port
   value: "9090"
 metrics:
 - name: success-rate
   successCondition: result[0] >= 0.95
   provider:
     prometheus:
       address: "http://prometheus.example.com:{{args.prometheus-port}}"
```
*Ref: Mastering Api Architecture.md — "Performing Rollouts with Argo Rollouts"*

### 60. Traffic Mirroring (Dark Launch)
**Principle:** Mirror real traffic to the new version without the user seeing the response — observe operational behavior and compare results.

**Do:**
- Use mirroring to validate new search/recommendation logic against real user queries.
- Compare the existing-vs-mirrored responses out-of-band for correctness.

**Don't:**
- Use mirroring when the call is non-idempotent and side-effectful.

**Code:**
```text
Traffic mirroring ("dark launch"):
  User --> [gateway]
              |     --> v1 (real response back to user)
              +---> v1.1 (mirror, response discarded, observed out-of-band)

Side-effect-free services (search, ranking) are ideal candidates.
DO NOT mirror calls that write to a database or send emails -- side effects
double-fire.
```
*Ref: Mastering Api Architecture.md — "Traffic Mirroring"*

### 61. Blue-Green Deployments
**Principle:** Run two full environments; flip the gateway when "green" is verified; keep "blue" warm for rollback.

**Do:**
- Use blue-green for tight-coupling releases where v1 + v2 must move together.
- Verify green against production-like traffic before flipping.

**Don't:**
- Accept the 2× resource cost as a permanent state — phase out blue.

**Code:**
```text
Blue-green:
  [Router/Gateway/LB] ---> Blue  (v1.0 live, current prod)
                       \-> Green (v1.1 candidate, not yet serving)

After verification:
  [Router/Gateway/LB] ---> Blue  (idle, retained as rollback)
                       \-> Green (live)

Roll-back = flip back to blue.
```
*Ref: Mastering Api Architecture.md — "Blue-Green"*

### 62. API Lifecycle (Planned → Beta → Live → Deprecated → Retired)
**Principle:** Adopt the PayPal-style lifecycle and put MAJOR.MINOR versions against lifecycle states.

**Do:**
- Planned: not yet exposed; advertise shape early.
- Beta: consumers can integrate; producer reserves the right to break.
- Live: ONE live major.minor.
- Deprecated: still up; migration guide + telemetry.
- Retired: dead.

**Don't:**
- Keep multiple "Live" versions indefinitely — the live lane is exactly one.

**Code:**
```text
API lifecycle (PayPal-adapted):
  Planned     Not exposed yet; collecting design feedback
  Beta        Consumer can integrate; producer can break
  Live        THE single live major.minor
  Deprecated  Live + migration guide + usage tracking
  Retired     Gone

Major bumps -> weeks/months of deprecation with guide + telemetry.
Minor bumps -> brief deprecation until new minor is validated.
Patch bumps -> transparent, no deprecation.
```
*Ref: Mastering Api Architecture.md — "API Lifecycle"*

### 63. Three Pillars of Observability
**Principle:** You need metrics + logs + traces to reason about distributed systems. Each has gaps the others fill.

**Do:**
- Standardize on OpenTelemetry (CNCF) for vendor neutrality.
- Adopt the RED method (Rate, Errors, Duration) and Google's four golden signals (Latency, Traffic, Errors, Saturation).

**Don't:**
- Use logs alone for distributed debugging — too slow.

**Code:**
```text
Three Pillars:
  Metrics    - Regular-interval numeric samples; cheap, alertable.
               RED = Rate, Errors, Duration
               Golden = Latency, Traffic, Errors, Saturation
  Logs       - Discrete events; great for forensics but not for correlation.
  Traces     - End-to-end request path; injected at edge, propagated
               through services (W3C tracecontext / b3).

OpenTelemetry (CNCF) = the converged standard for all three.
"Logging is slightly more difficult due to the variety of emitters,
but also covered in OpenTelemetry."
```
*Ref: Mastering Api Architecture.md — "Three Pillars of Observability"*

### 64. Context Matters More Than RED Numbers
**Principle:** RED/golden signals tell you *what* is happening; context tells you *why*. Filter before alerting.

**Do:**
- Investigate WHY before alerting on high error rates.
- Differentiate 4xx (client) from 5xx (server) — a 4xx spike may be a malicious actor.

**Don't:**
- Treat every metric in isolation — fail-open rate-limit configs cause silent breaches.

**Code:**
```text
Important context for API metrics:
  - 5xx = server-side issue (infrastructure / service).
  - 4xx = client issue, BUT:
      - 403 spike = possible auth probing by a malicious actor.
      - 401 spike from CFP integration = may be vendor compromise or stolen token.
  - 0 traffic may be normal (bank holiday); only alert during business hours
    or weighted by active sessions.

Examples of metrics to capture:
  - requests/minute for attendees
  - latency SLO deviation
  - 401s from a specific integration
  - availability/uptime of Attendee service
  - memory + CPU usage
  - total registered attendees
```
*Ref: Mastering Api Architecture.md — "Important Metrics for APIs"*

### 65. Application Decisions for Safe Releases
**Principle:** Microservice-era gotchas: response caching, header propagation, idempotency.

**Do:**
- Set `Cache-Control: no-cache, no-store` during canary launches.
- Propagate tracing headers downstream.
- Forward OAuth2 bearer tokens downstream; never forward raw auth headers (impersonation risk).

**Don't:**
- Trust upstream caches to invalidate when your code changes.

**Code:**
```text
Gotchas during rollouts:
  1. Cached response masking breakage
     The first release LOOKED healthy because cached responses were served.
     Mitigation: Cache-Control: no-cache, no-store on the test client.

  2. Header propagation
     Downstream services need tracing + correlation headers.
     Auth: forwarding OAuth bearer is OK; forwarding internal auth header
     risks impersonation.

  3. Idempotency
     Non-idempotent backend calls during canary/mirroring double-fire.
```
*Ref: Mastering Api Architecture.md — "Application Decisions for Effective Software Releases"*

### 66. Opinionated Platform / Paved Path
**Principle:** Standardize decisions (where to log, how to instrument, how to deploy) once per org; keep the path paved.

**Do:**
- Build a platform team treating developers as customers.
- Default to "newest features" for new apps; document upgrade path for existing apps.

**Don't:**
- Hide platform opinions — friction accumulates.

**Code:**
```text
ADR Guideline: Opinionated Platforms
Decision: Adopt an opinionated platform for deploys/releases?
Discussion:
  - Languages in the org -> can they live within opinionated defaults?
  - Empowered developer-customer model?
  - Constraints (monitoring, auth) you want enforced out of the box?
  - Update cadence for platform users?
Recommendation:
  Treat developers as customers of the platform; create a feedback loop.
  Make key features transparent (auto-OTel, structured logs).
  New apps = latest stack; existing apps need a clear upgrade story.
```
*Ref: Mastering Api Architecture.md — "Considering an Opinionated Platform"*

### 67. Threat Modeling Process (6 Steps)
**Principle:** Make threat modeling a recursive activity, not a one-off.

**Do:**
- 1. Identify objectives (business + security).
- 2. Gather info (people from each component).
- 3. Decompose the system (DFDs).
- 4. Identify threats (STRIDE per element).
- 5. Evaluate risk (DREAD or CVSS).
- 6. Validate + iterate.

**Don't:**
- Threat-model once and shelve the artifact — re-run on new functionality.

**Code:**
```text
Threat modeling steps:
  1. Objectives    What are we protecting? Business + security goals.
  2. Information   Architecture, data flows, stack, access controls.
  3. Decompose     Data Flow Diagrams (DFDs).
  4. Threats       Apply STRIDE per element.
  5. Risk          Score (DREAD or CVSS) and prioritize.
  6. Validate      Team review, mitigation verification, iterate.

DFDs capture DYNAMIC (data flow); C4 captures STATIC (structural).
```
*Ref: Mastering Api Architecture.md — "How to Threat Model"*

### 68. STRIDE Methodology
**Principle:** Apply STRIDE per element on the DFD — S/T/R/I/D/E.

**Do:**
- Spoofing: broken auth, password replay, cert forgery.
- Tampering: payload injection, mass assignment.
- Repudiation: insufficient logging & monitoring.
- Information disclosure: excessive data exposure, improper asset management.
- DoS: rate-limit, load shedding, fail-closed for sensitive APIs.
- Elevation of privilege: broken object-level (BOLA) / function-level (BFLA) authz.

**Don't:**
- Treat STRIDE as a checklist of categories to mention; "STRIDE per element" means every DFD node.

**Code:**
```text
STRIDE per element (each DFD node + edge):
  S - Spoofing                Replaying authentication / impersonating
  T - Tampering               Modifying data/code in transit or at rest
  R - Repudiation             Denying an action was performed
  I - Information Disclosure  Exposing info to unauthorized parties
  D - Denial of Service       Making system unavailable
  E - Elevation of Privilege  Gaining access beyond authorization

"Apply STRIDE to each process and connection."
```
*Ref: Mastering Api Architecture.md — "Step 4: Identify Threats—Taking This in Your STRIDE"*

### 69. Payload Injection Mitigation (Schema Validation at Edge)
**Principle:** Reject requests at the API gateway that don't conform to the OpenAPI schema — multiple lines of defense.

**Do:**
- Use `swagger-request-validator` (or equivalent) at the gateway.
- Reject malformed payloads before they hit the backend.
- ALSO sanitize in the backend (defense in depth).

**Don't:**
- Trust the gateway as the sole defense — gateways fail-open; backends must still validate.

**Code:**
```text
Defense-in-depth for injection:
  1. API gateway validates against OpenAPI schema -> reject early.
  2. Attendee service uses prepared statements (still!).
  3. Database driver parameterizes inputs.

Example rejected payload (SQL injection attempt):
  POST /attendees
  { "name": "Danny B", "age": 35,
    "profile": "Hax; DROP ALL TABLES; --" }
Schema says profile accepts letters/numbers/special chars but the
gateway + service both constrain and parameterize.
```
*Ref: Mastering Api Architecture.md — "Tampering" / "Payload injection"*

### 70. Mass Assignment Prevention
**Principle:** Internal fields (e.g., `devices`) must NEVER be writable via input — bind only explicit fields.

**Do:**
- Define explicit DTOs that enumerate writable properties.
- Ignore (or 400) requests that try to set read-only fields.

**Don't:**
- Use ORM "bind this whole object" APIs at the controller boundary.

**Code:**
```text
Mass assignment example:
  Read response (intentional):
    { "name": "Danny B", "age": 35,
      "devices": ["iPhone","Firefox"]    <-- READ-ONLY, populated by app }
  Attacker attempts:
    PUT /attendees/123456
    { "name": "Danny B", "age": 36,
      "devices": ["vulnerableDevice"]   <-- MUST be ignored on save }
Mitigation: explicitly enumerate write fields in the DTO.
Active Record / ORM auto-binding is a common source of this vulnerability.
```
*Ref: Mastering Api Architecture.md — "Mass assignment"*

### 71. Information Disclosure (Excessive Data Exposure)
**Principle:** APIs quietly evolve — defensive defaults must prevent unintentional PII exposure.

**Do:**
- Limit fields in default response DTOs; offer opt-in `expand=` style parameters.
- Strip server version / framework details from 500 responses.

**Don't:**
- Return the underlying entity verbatim — schema leakage = PII leakage.

**Code:**
```text
Anti-pattern (excessive exposure):
  { "values": [
      { "id":"0","name":"Danny B","age":65,
        "email":"danny.b@masteringapis.com",
        "passport":"Abc12408NJUILM"     <-- PII leak },
      ...
  ] }
Mitigation:
  - API returns ONLY the fields needed for the use case.
  - Gateway validates the response shape as a last-resort check.
  - Strip stack traces + server versions from 5xx responses.
```
*Ref: Mastering Api Architecture.md — "Information disclosure"*

### 72. Improper Assets Management (Shadow APIs)
**Principle:** Track every exposed API/version — undeleted beta endpoints are routine breach sources.

**Do:**
- Maintain a single registry of exposed APIs (gateway config, APIM catalog).
- Schedule and enforce retirement of stale endpoints.
- Run anomaly detection on access logs.

**Don't:**
- Forget `/beta/attendees` after it served its purpose — it likely still leaks the original data model.

**Code:**
```text
Hypothetical leak path:
  Old /beta/attendees (still deployed, undocumented):
    returns full attendee model INCLUDING fields the current
    /attendees masks (passport, SSN, ...).

If your API gateway has registration / catalog, you can find these.
A developer portal with proper ownership metadata helps track them.
```
*Ref: Mastering Api Architecture.md — "Improper assets management"*

### 73. DoS Mitigation (Rate Limiting, Load Shedding)
**Principle:** Every public API MUST rate limit and shed load on saturation.

**Do:**
- Combine fixed window + token bucket for tiered customers.
- Implement load shedding on backend saturation (DB pool full, worker starvation).
- Pair with CDN-level DoS protection for L3/L4 attacks.

**Don't:**
- Default to "no limit" and hope for the best.

**Code:**
```text
Rate-limit strategies (recap):
  Fixed window    N requests per period (resetting counter)
  Sliding window  N requests in the LAST period
  Token bucket    Bucket of N tokens, refilled regularly, 1 per request
  Leaky bucket    Like token bucket; fixed-rate processing

Load shedding example:
  -> When the database connection pool is at 100%,
     reject new requests with 503 + Retry-After.

Combine: CDN-level DoS protection + gateway IP / geo / client rules.
```
*Ref: Mastering Api Architecture.md — "Denial of service"*

### 74. Security Misconfiguration (TLS, CORS, Header Hardening)
**Principle:** TLS, CORS, header allowlisting — all required, all configured at the gateway front door.

**Do:**
- Use TLS 1.2+.
- Implement CORS by handling browser preflight at the gateway.
- Maintain an HTTP-header allowlist (strip X-Assert-Role=Admin, X-Impersonate=Admin, etc.).

**Don't:**
- Allow headers you've not enumerated — assume everything else is an attack.

**Code:**
```text
TLS:
  Gateway terminates TLS; central certificate management vs scattered.
  TLS 1.2+ recommended.

CORS:
  Browser-driven preflight (OPTIONS) handled by gateway.
  Allow only the origins you trust.

Header allowlist:
  Reject X-Assert-Role=Admin / X-Impersonate=Admin / unknown headers.
  Strip server version + framework trace from 5xx responses.
```
*Ref: Mastering Api Architecture.md — "Security misconfiguration"*

### 75. DREAD Risk Scoring (1–10 per Category)
**Principle:** DREAD gives a coarse, comparative risk score: Damage, Reproducibility, Exploitability, Affected Users, Discoverability. Sum, divide by 5, prioritize.

**Do:**
- Define scoring rubrics ("all users = 10; internal = 7; half = 3; none = 0").
- Re-score after mitigations.

**Don't:**
- Use Discoverability as a security-through-obscurity proxy (use DREAD-D which drops D).

**Code:**
```text
DREAD scoring (1-10 per category):
  D - Damage            How bad would the attack be?
  R - Reproducibility   Can it be repeated easily?
  E - Exploitability    How easy to mount?
  A - Affected Users    How many users impacted?
  D - Discoverability   How likely to be found?

Risk = (D + R + E + A + D) / 5.

Example: DDoS on a gateway with NO rate limiting:
  D=8 (full outage), R=8, E=5, A=10, D=10 -> 8.2 -> HIGH

DREAD-D drops Discoverability (security through obscurity -> not a metric).
```
*Ref: Mastering Api Architecture.md — "Step 5: Evaluate Threat Risks"*

### 76. OWASP API Security Top 10 as Threat Brainstorm
**Principle:** Use OWASP API Security Top 10 as an input to STRIDE — it pairs naturally with each STRIDE category.

**Do:**
- Map OWASP items into STRIDE during threat modeling.
- Treat the list as inspiration + mitigation — not exhaustive.

**Don't:**
- Use OWASP as a "scan and you're done" — attackers evolve.

**Code:**
```text
OWASP API Security Top 10 -> STRIDE mapping (illustrative):
  BOLA / BFLA                 -> E (Elevation of privilege)
  Broken User Authentication  -> S (Spoofing)
  Excessive Data Exposure     -> I (Information disclosure)
  Lack of Resources & Rate Lim-> D (Denial of service)
  Mass Assignment             -> T (Tampering)
  Security Misconfiguration  -> multiple (esp. I and D)
  Improper Assets Management -> I
  Injection (incl. SQL)       -> T

The 2019 OWASP API Security Top 10 is the baseline; check for updates.
```
*Ref: Mastering Api Architecture.md — "Case Study: Applying OWASP to the Attendee API"*

### 77. Authentication vs Authorization
**Principle:** Authentication = WHO; Authorization = WHAT THEY MAY DO. Apply both, at multiple layers.

**Do:**
- Authenticate at the gateway (cheap, central).
- Authorize at the service (fine-grained, with access to the user/resource).

**Don't:**
- Trust the gateway to enforce per-object authorization — it doesn't see the relationship between user and object.

**Code:**
```text
OWASP API Security Top 10 -- authorization failures:
  BOLA  (Broken Object-Level Authorization):
    User tampers with object ID to access someone else's resource.
    E.g., /attendees/123456 returns another user's data.
  BFLA  (Broken Function-Level Authorization):
    User invokes admin-only endpoint with a standard user token.
Mitigation:
  - Scope validation at the gateway.
  - Per-resource permission check in the service.
  - Per-object ownership check in the data layer.
```
*Ref: Mastering Api Architecture.md — "Authorization Enforcement"*

### 78. Authentication Methods: From Basic to Tokens
**Principle:** Use HTTP Basic only over TLS, and only inside a trusted control plane — never hand credentials to a third-party app.

**Do:**
- Use bearer tokens (opaque or JWT) for user-facing APIs.
- Use API keys for system-to-system identification, never for user identity.
- Keep credentials short-lived.

**Don't:**
- Allow a third-party (e.g., CFP) to hold user passwords and impersonate users.
- Build a custom security layer — pick OAuth2 + OIDC.

**Code:**
```text
Authentication ladder:
  HTTP Basic        Username + password in Authorization header.
                    Do NOT allow for third-party app access to user data.
                    Send only over TLS.
  API keys          Shared secret; passed in a header (X-API-KEY).
                    Use ONLY for system-to-system.
                    256-bit cryptographically random value.
                    Do NOT mix with user identity.
  Tokens            Opaque or structured (JWT) bearer tokens.
                    Short lifetime (1-60 minutes typical).
                    OAuth2 is the standard issuance/management framework.
```
*Ref: Mastering Api Architecture.md — "Authentication" / "End-User Authentication with Tokens"*

### 79. JWT Structure & Reserved Claims
**Principle:** JWTs are an RFC-standard token format with reserved claims — use them correctly.

**Do:**
- Use reserved claims: `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`.
- Keep subjects stable (UUID, not email — email changes).
- Sign with JWS for integrity; encrypt with JWE for confidentiality.

**Don't:**
- Store secrets in the JWT payload — base64 is not encryption.
- Use long-lived tokens.

**Code:**
```jsonc
{
 "iss":  "http://mastering-api/",
 "sub":  "18f913b1-7a9d-47e6-a062-5381d1e21ffa",
 "aud":  "Attendee-Service",
 "exp":  1618146900,
 "nbf":  1618144200,
 "iat":  1618144200,
 "jti":  "4d13ba71-54e4-4583-9458-562cbf0ba4e4"
}

// Reserved claims:
//   iss = issuer (e.g., auth server)
//   sub = subject (user/app; stable UUID, NOT email)
//   aud = intended audience (this resource server)
//   exp = expiration (epoch seconds)
//   nbf = not before
//   iat = issued at
//   jti = unique JWT ID
```
*Ref: Mastering Api Architecture.md — "JSON Web Tokens (JWT)"*

### 80. JWS vs JWE: Integrity vs Confidentiality
**Principle:** Choose encoding by sensitivity — JWS for tamper detection, JWE for confidentiality.

**Do:**
- Default to JWS (signed JWT) — claims are readable but tamper-evident.
- Use JWE when the claims themselves are sensitive.
- Sign with private key; verify with public key.

**Don't:**
- Assume "JWS is secure enough" when claims contain PII — anyone with the token can read the claims.

**Code:**
```text
JWT encoding:
  JSON Web Signature (JWS):
    - Integrity provided via digital signature.
    - Claims are visible to anyone who has the token.
    - Most common default; "JWT" usually means JWS.
  JSON Web Encryption (JWE):
    - Confidentiality + integrity.
    - Claims are not readable without the decryption key.
Rule of thumb:
  If putting secrets in claims -> JWE.
  If claims are non-sensitive metadata -> JWS.
```
*Ref: Mastering Api Architecture.md — "Encoding and verifying JSON Web Tokens"*

### 81. OAuth2 Roles
**Principle:** OAuth2 decouples authentication from the resource server — third parties never see user passwords.

**Do:**
- Resource Owner: the user granting access.
- Client: the app requesting access.
- Authorization Server: issues tokens after authentication + consent.
- Resource Server: hosts the protected resources.

**Don't:**
- Build your own identity layer when OAuth2/OIDC offers it.

**Code:**
```text
OAuth2 roles (RFC 6749):
  Resource Owner       Entity granting access. A person -> "end-user".
  Authorization Server Issues access tokens after authenticating the
                       resource owner and obtaining authorization.
                       e.g., Google, Auth0, Okta.
  Client               Application making protected resource requests on
                       behalf of the resource owner.
  Resource Server      Server hosting the protected resources; accepts
                       and responds to requests using access tokens.
                       Often the API gateway in a microservices system.
```
*Ref: Mastering Api Architecture.md — "OAuth2"*

### 82. OAuth2 Abstract Protocol Flow (A–F)
**Principle:** OAuth2 is six orthogonal steps; different grants implement them differently.

**Do:**
- A: client requests authorization from the resource owner.
- B: resource owner grants/denies.
- C: client asks for access token.
- D: auth server issues token.
- E: client calls resource server with token.
- F: resource server returns resource.

**Don't:**
- Couple resource acquisition to how the token was obtained — the resource server doesn't care which grant was used.

**Code:**
```text
OAuth2 abstract protocol:
  [Client] ---(A) request auth---> [Resource Owner]
  [Client] <--(B) grant/deny----- [Resource Owner]
  [Client] ---(C) code/token---> [Authorization Server]
  [Client] <--(D) access token---
  [Client] ---(E) request + token---> [Resource Server]
  [Client] <--(F) resource---------

"The resource server will return the resource if the access token is
 valid. Each step is isolated and does not require information about
 the previous step."
```
*Ref: Mastering Api Architecture.md — "Terminology and Mechanisms of OAuth2 Grants"*

### 83. Authorization Code Grant (Confidential Web Client)
**Principle:** The default grant for server-side web apps — the client can protect a secret.

**Do:**
- Use Auth Code Grant for confidential clients.
- Combine with PKCE for public clients (mobile, SPA) — see next cluster.

**Don't:**
- Use the deprecated Implicit Grant for new SPAs.

**Code:**
```text
Auth Code Grant:
  A. Client -> User Agent (browser) -> Authorization Server
     (client_id, response_type=code)
  B. Auth Server authenticates the resource owner.
  C. Authorization code returned to client (via redirect).
  D. Client -> Auth Server (code + client_secret) -> access token.
  E. Client calls Resource Server with access token.

This is what runs when you click "Allow LinkedIn to access your Gmail
contacts".
```
*Ref: Mastering Api Architecture.md — "Authorization Code Grant"*

### 84. Authorization Code Grant + PKCE (Public Clients)
**Principle:** PKCE prevents authorization-code interception attacks for SPAs and mobile apps.

**Do:**
- Generate `code_verifier` (cryptographically random).
- Send hashed `code_challenge` in the auth request.
- Send `code_verifier` + code in the token exchange.

**Don't:**
- Skip PKCE for "low-risk" clients — interception doesn't care about your risk model.

**Code:**
```text
Auth Code Grant + PKCE:
  A. Authorization request includes code_challenge = t(code_verifier)
     transformation t_m is a hash (e.g., SHA-256 + base64url).
  B. Authorization code returned (same as plain Auth Code).
  C. Token request: client sends code + code_verifier (NOT client_secret).
  D. Auth Server hashes verifier, compares to challenge; issues token.

PKCE protects against interception: only the original client knows verifier.
MUST use for public clients; SHOULD use for confidential clients too.
```
*Ref: Mastering Api Architecture.md — "Authorization Code Grant (+ PKCE)"*

### 85. Refresh Tokens & Revocation
**Principle:** Refresh tokens are long-lived credentials that mint new access tokens — keep them scarce, detect reuse, revoke on demand.

**Do:**
- Issue refresh tokens only when needed (silent re-auth, no UI prompt).
- Treat refresh token reuse as compromise — revoke the chain.
- Store refresh tokens in secure storage (e.g., HttpOnly cookies, mobile Keychain).

**Don't:**
- Use refresh tokens with the Client Credentials Grant — clients just request a new access token.

**Code:**
```text
Refresh token mechanics:
  Short-lived access token (1-60 minutes typical).
  Long-lived refresh token (days / months).
  Client uses refresh token to mint new access tokens w/o user re-auth.

  Modern best practice:
    Refresh token reuse detected -> revoke the entire chain.
    Refresh tokens are extra credentials; MUST be stored securely.

For the Client Credentials Grant:
  No refresh token -- the client just requests a new access token.
```
*Ref: Mastering Api Architecture.md — "Refresh Tokens"*

### 86. Client Credentials Grant (System-to-System)
**Principle:** When there is no user, the Client Credentials Grant is the answer — pre-authorize the client for what it can do.

**Do:**
- Use Client Credentials for machine-to-machine flows.
- Pre-arrange scopes (the report generator can read attendees who submitted talks).
- Consider mTLS (RFC 8705) instead of shared secrets for stronger security.

**Don't:**
- Use Client Credentials when a user is involved — pick Auth Code.

**Code:**
```text
Client Credentials Grant:
  [Client] ---(client_id, client_secret, grant=client_credentials)-->
  [Authorization Server]
  [Client] <--- access token (no refresh token)---

No user consent UI; access is pre-arranged when the client is registered.

Alternative: Mutual TLS (RFC 8705) -> replace shared secrets with
client certificates for stronger authentication.
```
*Ref: Mastering Api Architecture.md — "Client Credentials Grant"*

### 87. OAuth2 Scopes for Coarse-Grained Access
**Principle:** Scopes = the user's consent for what the client may do. Pair with fine-grained per-resource checks.

**Do:**
- Make scopes meaningful to users (they consent).
- Use read/write separation (`AttendeeRead`, `AttendeeAccount`).
- Encode as `scope` claim in JWT.
- Enforce at the gateway for early rejection.

**Don't:**
- Use scopes as the only authorization layer — combine with per-object checks.

**Code:**
```text
Scope modeling for the Attendee API:
  GET /attendees                -> AttendeeRead
  GET /attendees/{id}           -> AttendeeRead
  POST /attendees               -> AttendeeAccount
  PUT /attendees/{id}           -> AttendeeAccount
  GET /conferences              -> Conference
  POST /conferences             -> Conference

User consent screen explains scopes in plain language.
JWT scope claim: { ..., "scope": "AttendeeRead AttendeeAccount" }
```
*Ref: Mastering Api Architecture.md — "OAuth2 Scopes"*

### 88. Additional OAuth2 Grants (Device, Implicit, ROPC)
**Principle:** Pick only the grants you need — defaults: Auth Code (+PKCE) and Client Credentials.

**Do:**
- Device Authorization Grant for IoT / CLI / smart-fridge-style devices.
- Auth Code + PKCE for SPAs and mobile.
- Client Credentials for M2M.

**Don't:**
- Use the Implicit Grant for new projects (deprecated; replaced by PKCE).
- Use Resource Owner Password Credentials Grant — assume compromised.

**Code:**
```text
Available OAuth2 grants:
  Authorization Code (+ PKCE)  - confidential + public clients; default
  Client Credentials           - system-to-system
  Device Authorization         - IoT / CLI / no browser
  Implicit                     - DEPRECATED; use Auth Code + PKCE
  ROPC (Password)              - DEPRECATED; only acceptable as a bridge
                                 from legacy HTTP Basic
```
*Ref: Mastering Api Architecture.md — "Additional OAuth2 Grants"*

### 89. OIDC for Identity (Not Access)
**Principle:** Use OIDC when the client needs to know WHO the user is — never substitute ID tokens for access tokens.

**Do:**
- Request the `openid` scope to get an ID token.
- Use OIDC flows (Authorization Code Flow preferred) for SPA/mobile/web.
- Add `profile`, `email`, `address`, `phone` for richer ID claims.

**Don't:**
- Use ID tokens to call APIs — they aren't access tokens.
- Build your own ID layer.

**Code:**
```text
OIDC scopes for richer ID token claims:
  openid    -> subject (UUID), required base
  profile   -> name, family_name, given_name, nickname, picture, ...
  email     -> email, email_verified
  address   -> address
  phone     -> phone_number, phone_number_verified

OIDC flows: Authorization Code Flow (preferred), Implicit, Hybrid.
Auth Code Flow is preferred for the same reasons as OAuth2 Auth Code.
```
*Ref: Mastering Api Architecture.md — "Introducing OIDC"*

### 90. SAML 2.0 Federation with OAuth2
**Principle:** When enterprise users authenticate via SAML, bridge SAML to OAuth2 via the SAML 2.0 Profile — don't expose SAML to APIs.

**Do:**
- Use the OAuth2 SAML 2.0 Profile at the authorization server.
- Keep SAML for SSO/web flows, OAuth2 for API access.

**Don't:**
- Speak SAML to APIs directly — it's not designed for it.

**Code:**
```text
SAML 2.0 Profile for OAuth 2.0 Client Authentication
and Authorization Grants:

  Use when migrating from SAML-based SSO to OAuth2 API access.
  Authorisation server must implement the SAML extension.

  SAML itself is XML; not aligned to API use; bridge to OAuth2.
```
*Ref: Mastering Api Architecture.md — "SAML 2.0"*

### 91. Cohesion: 7 Types to Balance
**Principle:** Aim for high cohesion — but know there are 7 types (functional through coincidental) and pick deliberately.

**Do:**
- Functional cohesion (single purpose) is the gold standard.
- Sequential cohesion (output feeds next step) is good.
- Communicate via well-defined interfaces.

**Don't:**
- Create a "utils" API that hides cross-cutting logic (low cohesion in disguise).

**Code:**
```text
Cohesion types (steepest-to-weakest):
  - Functional   Operations on a single well-defined task (best)
  - Sequential   Output of one op feeds the next
  - Communicational Ops work on the same data
  - Procedural   Ops grouped by the order they're executed
  - Temporal     Ops at the same time (init/shutdown)
  - Logical      Ops grouped by category only
  - Coincidental Ops with no real relationship (worst)

Counter-example: a "utils" API with cross-cutting conveniences
quickly creates low cohesion at high coupling cost.
```
*Ref: Mastering Api Architecture.md — "There Are Many Types of Cohesion to Consider!"*

### 92. Loose Coupling & Information Hiding
**Principle:** Loose coupling enables mocking, swapping, and independent evolution.

**Do:**
- Hide implementation decisions behind stable interfaces.
- Make components replaceable per the Liskov Substitution Principle.
- Use interfaces for substitutability in tests.

**Don't:**
- Leak the data model into the API contract.

**Code:**
```text
Loose coupling enables:
  - Easier mocking/virtualizing in tests
  - Swap implementations without touching consumers
  - Polyglot (replace a service in another language)
  - Multi-platform, multi-cloud portability

Information hiding:
  "Principle of segregation of implementation decisions that are most
   likely to change."
  Stable interface protects the system from the changeable internals.
  Use business/domain-focused API endpoints; do NOT leak the
  implementation-specific schema or data model.
```
*Ref: Mastering Api Architecture.md — "Clarifying Domain Boundaries: Promoting Loose Coupling"*

### 93. Fitness Functions for Architecture Governance
**Principle:** Architectural properties must be measured continuously — fitness functions are the unit test for architecture.

**Do:**
- Embed fitness functions in CI: code quality, resiliency, observability, performance, compliance, security, operability.
- Use existing tooling (SonarQube, OWASP scans, dependency CVE checks).

**Don't:**
- Let "ilities" be aspirational — measure or they degrade.

**Code:**
```text
Fitness function categories (Thoughtworks):
  Code Quality    Tests + complexity + duplication metrics
  Resiliency      Synthetic traffic; inject faults via gateway/mesh;
                  assert error rate < threshold
  Observability   Verify services publish required metrics/traces
  Performance     Latency + throughput targets asserted in pipeline
  Compliance      Audit trail, data residency
  Security        CVE scan; OWASP scans; mTLS verification;
                  authorization policies
  Operability     Onboarding: monitoring + alerting in place?

"An ADR around fitness functions is a good place to start."
```
*Ref: Mastering Api Architecture.md — "Using Fitness Functions"*

### 94. Strangler Fig Pattern
**Principle:** Gradually replace an old system by routing around it — the new components grow until the old is fully consumed.

**Do:**
- Use a gateway / proxy to route between legacy and modern implementations.
- Remove the old once parity is proven.

**Don't:**
- Make the gateway hold business logic — that's permanent migration debt.

**Code:**
```text
Strangler Fig:
  [Gateway]
   /     \
  /       \
 v         v
[Legacy]-->[Modern]
<--redirect or feature-flag over time.
Once Modern covers all functionality, Legacy is removed.
"Do not let the proxy take on business logic or removing at end of
 migration becomes impossible."
```
*Ref: Mastering Api Architecture.md — "Strangler Fig"*

### 95. Facade & Adapter Patterns
**Principle:** Facade simplifies an interface; adapter makes incompatible interfaces work together — both are valuable during migration.

**Do:**
- Use adapters for SOAP → REST bridging in legacy land.
- Use a grpc-gateway adapter when REST + gRPC must coexist.
- Distinguish facade vs adapter clearly (facade simpler).

**Don't:**
- Use a facade where an adapter is needed (or vice versa) — increase coupling.

**Code:**
```text
Facade vs Adapter:
  Facade   - Defines a new simpler interface for an existing system.
             Hides complexity.
  Adapter  - Reuses an old interface to support interoperability.
             Converts one representation to another (SOAP->REST,
             REST->gRPC).
  "If an API gateway steps over the line from facade to adapter,
   coupling immediately increases."
```
*Ref: Mastering Api Architecture.md — "Facade and Adapter"*

### 96. Avoid the API Layer Cake
**Principle:** The legacy "presentation/application/domain/datastore" tiering (Pace-Layered) is a known antipattern — short-circuits dominate.

**Do:**
- Use DDD + hexagonal architecture inside services.
- Avoid presentation-layer calls directly into the datastore.

**Don't:**
- Duplicate logic across tiers to "save" a hop.
- Layer without clear single-directional dependency.

**Code:**
```text
API Layer Cake (Pace-Layered - generally avoid):
  Presentation      SoE  - Systems of Engagement
  Application       SoD  - Systems of Differentiation
  Domain            SoR  - Systems of Record
  Datastore

Anti-pattern dynamics:
  - Duplication across tiers to avoid one hop
  - Presentation calling datastore directly
  - End-to-end slice requires touching all tiers

"We generally recommend avoiding the use of this pattern."
```
*Ref: Mastering Api Architecture.md — "API Layer Cake"*

### 97. End-State Architecture: Pick Deliberately
**Principle:** Set your destination before you start — Monolith, SOA, Microservices, or Functions. Each has trade-offs.

**Do:**
- Monolith for proof-of-concept + market discovery.
- Microservices for scale + autonomy; DDD-defined boundaries.
- Functions for highly event-driven systems.

**Don't:**
- Microservices-by-default — they cost operational complexity.

**Code:**
```text
| Style         | Best for                                  | Trade-off                |
|---------------|-------------------------------------------|--------------------------|
| Monolith      | POC, market discovery, single team       | Scales poorly; high coupling risk |
| SOA           | Cross-team reuse                          | ESB anti-pattern; vendor lock-in |
| Microservices | Scale, team autonomy                      | Operational complexity  |
| Functions     | Event-driven, short-lived ops             | Coupling via orchestration |

"Smart endpoints and dumb pipes" -- Lewis & Fowler.
Use lightweight tech: REST, gRPC, AMQP, STOMP, WebSockets.
```
*Ref: Mastering Api Architecture.md — "End State Architecture Options"*

### 98. 6 Rs of Cloud Migration
**Principle:** Pick from Retain, Rehost, Replatform, Repurchase, Refactor, Retire — most projects need a mix.

**Do:**
- Retain: stable, compliant-bound, or underwhelming ROI.
- Rehost ("lift-and-shift"): fast consolidation.
- Replatform ("lift-tinker-shift"): drop-in cloud services (e.g., MySQL → RDS).
- Repurchase: SaaS replaces homegrown.
- Refactor / Re-architect: full rewrite to cloud-native.
- Retire: decommission unused systems.

**Don't:**
- Skip Repurchase analysis because the homegrown is "good enough".

**Code:**
```text
6 Rs of cloud migration (AWS adaptation of Gartner):
  1. Retain       Keep on-prem; revisit later
  2. Rehost       Lift and shift, no redesign
  3. Replatform   Lift, tinker, shift (drop-in cloud services)
  4. Repurchase   SaaS replaces homegrown
  5. Refactor     Re-architect cloud-native
  6. Retire       Decommission unused systems

Case study choice: Replatform the Attendee service to gain a managed DB
without re-architecting.
```
*Ref: Mastering Api Architecture.md — "Choosing a Cloud Migration Strategy"*

### 99. Zonal Architecture (PZ / PAZ / OZ / RZ)
**Principle:** Traditional network zoning mitigates blast radius — but assumes internal trust that cloud doesn't honor.

**Do:**
- Cascade zones (Public → Public Access → Operations → Restricted).
- Apply defense-in-depth at zone boundaries.

**Don't:**
- Trust the "castle walls" once in cloud — supply chain and insider risk invalidate the assumption.

**Code:**
```text
Zonal architecture (Canadian govt ITSG-22):
  PZ  Public Zone        Open public networks
  PAZ Public Access Zone DMZ between PZ and internal networks
  OZ  Operations Zone    Standard ops, sensitive but not "vault" data
  RZ  Restricted Zone    Business-critical; large sensitive data repos

  "Castle and moat" -- once past the perimeter, attacker has free range.
  Cloud invalidates this: location abstraction, supply chain, insider risk.
```
*Ref: Mastering Api Architecture.md — "Getting in the Zone"*

### 100. Zero Trust Architecture (8 Principles)
**Principle:** "Never trust, always verify" — applies to every request, every service, every network.

**Do:**
- Know your architecture (users, devices, services, data).
- Verify identity, device, and service health at every layer.
- Use policies for authorization everywhere.
- Don't trust any network — including your own.

**Don't:**
- Single authenticate at the edge and trust the rest.

**Code:**
```text
Eight principles of zero trust (NCSC-aligned):
  1. Know your architecture
  2. Know your user, service, device identities
  3. Assess user behavior, device, service health
  4. Use policies to authorize requests
  5. Authenticate and authorize EVERYWHERE
  6. Focus monitoring on EVERY aspect of access
  7. Don't trust any network, including your own
  8. Choose/design services for zero trust
```
*Ref: Mastering Api Architecture.md — "Trust No One and Verify"*

### 101. Kubernetes NetworkPolicy: Default-Deny Microsegmentation
**Principle:** Lock down all pod traffic by default; allow only the flows your mesh needs.

**Do:**
- Apply a deny-all NetworkPolicy as the baseline.
- Add explicit egress for DNS, then for each required service pair.

**Don't:**
- Rely on default-allow pod networking in production.

**Code:**
```yaml
# Default deny-all for every pod
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
 name: default-deny-all
spec:
 podSelector: {}
 policyTypes:
 - Egress
 - Ingress

# Allow DNS for service mesh discovery
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
 name: allow-dns
spec:
 podSelector:
   matchLabels:
     app: legacy-conference
 policyTypes:
 - Egress
 egress:
 - ports:
   # allow DNS resolution
   - port: 53
     protocol: UDP

# Allow legacy -> attendees egress (mesh-routed, but needs L4 allow)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
 name: allow-conference-egress
spec:
 podSelector:
   matchLabels:
     app: legacy-conference
 policyTypes:
 - Egress
 egress:
 - to:
   - namespaceSelector:
       matchLabels:
         kubernetes.io/metadata.name: attendees
```
*Ref: Mastering Api Architecture.md — "Augmenting Service Mesh with Network Policies"*

### 102. Conway's Law: Socio-Technical Architecture
**Principle:** Architecture mirrors organizational communication — design teams AND code together.

**Do:**
- Align team boundaries with service boundaries (inverse Conway maneuver).
- Treat architecture as a socio-technical decision.

**Don't:**
- Assume 4 teams building microservices gives 4-layer architecture (it does).

**Code:**
```text
Conway's Law:

  "Any organization that designs a system will produce a design whose
   structure is a copy of the organization's communication structure."

  Often rephrased: "If you have four groups working on a microservice
   system, you'll get four layers of APIs."

  Recommended reads:
    - Team Topologies (IT Revolution Press)
    - Agile IT Organization Design (Addison-Wesley)
    - The Art of Scalability (Addison-Wesley)
```
*Ref: Mastering Api Architecture.md — "APIs, Conway's Law, and Your Organization"*

### 103. Jeff Bezos Decision Types: Type 1 vs Type 2
**Principle:** Type 1 (irreversible) decisions need rigor; Type 2 (easily reversible) should be made quickly.

**Do:**
- Treat gateway and mesh adoption as Type 1.
- Treat endpoint URL design as Type 2.

**Don't:**
- Use Type 1 process on Type 2 decisions — kills speed and experimentation.

**Code:**
```text
Jeff Bezos (1997 letter):

  Type 1: Irreversible (or very costly to reverse). Choose API gateway,
          service mesh, programming language, etc. with appropriate
          rigor.

  Type 2: Easily reversible. Like walking through a door. Most day-to-day
          API design decisions fall here.

  Anti-pattern: applying Type 1 process to Type 2 decisions => slowness,
  risk aversion, failure to experiment, diminished invention.
```
*Ref: Mastering Api Architecture.md — "Understanding Decision Types"*

### 104. Multicluster Service Mesh for Cross-Network Zero-Trust
**Principle:** Peer service meshes across clusters (on-prem ↔ cloud) to apply uniform zero-trust during migration.

**Do:**
- Use mesh peering for cross-cluster communication that respects cluster identity.
- Bridge on-prem and cloud under a single control plane for security consistency.

**Don't:**
- Assume "hybrid" means "we'll just open a firewall" — preserves zonal assumptions.

**Code:**
```text
Multicluster mesh peering:

  [On-prem cluster]  <--- peer --->  [Cloud cluster]
   |                                     |
   v                                     v
  [Mesh control plane A]          [Mesh control plane B]
        \         combined via peering /
         v                           v
      Unified zero-trust identity, mTLS, ABAC

Provides a secure evolutionary architecture:
  cloud + on-prem work the same; remaining on-prem services can move
  to the cloud when ready without redesigning security.
```
*Ref: Mastering Api Architecture.md — "Role of Service Mesh in Zero Trust Architectures"*

### 105. API Management in the Migration Era
**Principle:** API management (developer portal, monetization, OAuth2 policies) becomes a central pivot for partial migrations.

**Do:**
- Offer "old" and "new" APIs through the same developer portal during migration.
- Keep contracts stable and evolve implementations behind the gateway.

**Don't:**
- Treat API management as optional — it's how you monetize, govern, and discover APIs.

**Code:**
```text
API management role in migration:
  + Central OAuth2 challenges.
  + Content validation.
  + Rate limiting, throttling.
  + Developer portal + service catalog.
  + Monetization (external chargebacks + internal chargebacks).
  + Discovery of APIs while implementations change behind.

"Perhaps the most important part of API management is that it can
 offer a central point to discover APIs, while you continue to make
 changes behind the scenes."
```
*Ref: Mastering Api Architecture.md — "Role of API Management"*

### 106. Future-Tech Watchlist (AsyncAPI, HTTP/3, SMI)
**Principle:** Three trends will reshape the next phase — track and pilot.

**Do:**
- AsyncAPI for event-driven specs (Kafka, etc.).
- HTTP/3 (QUIC/UDP) for head-of-line blocking fixes.
- Service Mesh Interface (SMI) for mesh abstraction.

**Don't:**
- Drop everything for these — pilot behind opt-in.

**Code:**
```text
Emerging tech watchlist:

  AsyncAPI          Specification for asynchronous APIs (broker, pub/sub)
                    emerging to complement OpenAPI for sync REST.
                    Watch adoption as event-driven architectures grow.

  HTTP/3            Uses QUIC (UDP transport) -- fixes HTTP/2 head-of-line
                    blocking. Already supported by 70%+ browsers. Will
                    require ingress proxy + networking upgrades.

  Platform-based    Service mesh absorbed into managed Kubernetes
  Mesh               offerings (SMI, vendor integrations). Mesh choice
                    may become a platform decision, not an application
                    decision.
```
*Ref: Mastering Api Architecture.md — "Preparing for the Future"*

### 107. Always Use the Simplest Solution That Meets Requirements
**Principle:** The book's overarching mantra: simple > complex, until simple cannot satisfy requirements.

**Do:**
- Start with proxy or LB for ingress; add gateway only when needed.
- Start with shared libraries; add service mesh only when polyglot.
- Start with monolith; extract only when pain points demand.

**Don't:**
- Choose microservices / mesh / gateway as the default when not needed.

**Code:**
```text
Recurring recommendation across the book:

"Always use the simplest solution for your requirements, with an eye
 to the immediate future and known requirements."

Repeated for:
  - Proxy vs LB vs Gateway
  - Libraries vs Sidecar mesh vs eBPF
  - Monolith vs Microservices
  - Custom vs Open-source/COTS for both gateway and mesh
  - Build vs Buy
```
*Ref: Mastering Api Architecture.md — multiple ADR Guidelines*

### 108. Documentation as a Living Artifact
**Principle:** Specs, ADRs, runbooks, and threat models decay — keep them versioned and reviewed.

**Do:**
- Version OpenAPI specs alongside code.
- Update ADRs when superseded (don't edit; add a new ADR).
- Re-run threat models when functionality or external threats change.

**Don't:**
- Let docs go stale — they become a liability.

**Code:**
```text
Living artifact checklist:

  OpenAPI spec      Versioned; diff'd in CI; examples validated
  ADRs              Immutable; superseded with new ADR + reference
  Threat models     Recursive; trigger on new feature or new risk
  Runbooks          Reviewed quarterly; on-call rotation changes owner
  Fitness functions Added to build pipeline; alerts when violated
```
*Ref: Mastering Api Architecture.md — multiple chapters*

## Anti-Patterns & Common Mistakes

- **API Gateway Loopback:** Routing internal service traffic back through the public gateway — egress cost, latency, and SPOF. *Fix:* Use mesh or DNS for internal discovery.
- **API Gateway as ESB:** Putting business logic in gateway plug-ins (Lua, WASM, Groovy). *Fix:* Keep gateway dumb; move business logic to services.
- **Turtles (Gateways) All the Way Down:** Chaining multiple gateways to "separate concerns" — coordination cost is brutal. *Fix:* Pick one tier per concern.
- **Service Mesh as ESB:** Payload transformation in WASM filters. *Fix:* Keep mesh focused on L4/L7 traffic concerns.
- **Service Mesh as Gateway:** Using only the mesh ingress because "we'll add the mesh eventually." *Fix:* Adopt a full API gateway; add mesh for east-west.
- **Mass Assignment:** ORM auto-binding clients can update `devices` (or any internal field). *Fix:* Use explicit DTOs with write-fields only.
- **Improper Assets Management:** `/beta/attendees` from 2019 still in production, leaking the old data model. *Fix:* Single registry (gateway config / API catalog) of exposed APIs.
- **Excessive Data Exposure:** Returning the entire entity because "we might need it." *Fix:* DTO per use case; gateway response validation as belt-and-braces.
- **Fail-Open Security by Default:** "If the auth service is down, let traffic through." *Fix:* Match defaults to risk profile — financial = fail-closed, weather = fail-open.
- **gRPC Field Renumbering:** Adding a field alphabetically shifts wire numbers. *Fix:* Always use `reserved` for removed numbers; explicitly assign new numbers.
- **Combine REST and gRPC via Generation:** Coupling two independently-versioned surfaces. *Fix:* Design both independently when possible.
- **Hand-Rolled Stubs:** Typos hidden in plain sight (look at the duplicate `id` in the case-study "values" array). *Fix:* Generate stubs from contracts; record real interactions.
- **Testcontainers Replacing Contracts:** Testcontainers tests verify integration — they don't define an interaction. *Fix:* Use contracts for behavior; Testcontainers for boundary correctness.
- **E2E for Everything:** The ice-cream cone. *Fix:* Use the test pyramid; reserve E2E for critical journeys.
- **Microservices Before Product-Market Fit:** Operational complexity before value validation. *Fix:* Monolith first, extract on pain.
- **Use Both OpenAPI and gRPC Independently:** Means two specs to version; document the cost. *Fix:* Use grpc-gateway only when single-source-of-truth is non-negotiable.
- **Per-Payload Routing:** Routing on body content leaks domain coupling and burns CPU. *Fix:* Use path/host/header routing only.
- **No Rate Limiting:** Trivial DoS. *Fix:* Apply fixed window + token bucket; load-shed on saturation.
- **Unenforced OWASP API Security Top 10:** Treating OWASP as a checkbox. *Fix:* Map each item into STRIDE per element in every threat model.
- **Improper Cache-Control During Canary:** Cache masks canary failures. *Fix:* Set `Cache-Control: no-cache, no-store` on canary test traffic.
- **Single Architecture/Endpoint, No API Lifecycle:** Multiple "live" versions, no retirement, no deprecation timeline. *Fix:* Apply Planned → Beta → Live → Deprecated → Retired states explicitly.
- **Centralized Trust in Cloud:** Cloud invalidates "castle and moat." *Fix:* Zero trust + mTLS mesh + default-deny NetworkPolicies.
- **Custom AuthN/Z:** Reimplementing OAuth2/OIDC. *Fix:* Adopt an OAuth2/OIDC provider; do not build your own.
- **API Keys as User Identity:** CFP system holding an attendee's API key + asserting who the user is. *Fix:* Use OAuth2 scopes + user consent.
- **Long-Lived JWTs:** Tokens valid for weeks = weeks of abuse if stolen. *Fix:* 1-60 minute access tokens; refresh tokens with reuse detection.
- **ID Tokens Used as Access Tokens:** They are long-lived and not designed for API access. *Fix:* Always use access tokens for API calls; ID tokens only for identity.
- **Implicit Grant for New SPAs:** Deprecated; PKCE replaces it. *Fix:* Auth Code Grant + PKCE.
- **HTTP Basic for Third Parties:** Handing the password to a third party is unacceptable. *Fix:* OAuth2 + consent.
- **Stacked Networking Layers:** Mesh on top of L4 LB on top of another proxy — duplicate circuit breakers, header stripping. *Fix:* One tier per concern; coordinate teams.
- **Const-Reducing Decisions Without ADR:** OpenAPI spec, gateway choice, mesh choice with no ADR. *Fix:* Capture significant decisions; Type-1 decisions especially.
- **One Team Designing for Four Teams:** Conway's law in action — you get four layers of APIs. *Fix:* Align team topology with service topology.
- **Speculative APIs ("Future-Proofing"):** Designing space-shuttle controls for a car. *Fix:* Cohesive, opinionated APIs over feature lists.
- **Build-Your-Own Gateway/Mesh:** Reasonable only at hyperscaler scale; almost always wrong elsewhere. *Fix:* Default to open source / commercial.

## Decision Heuristics / Checklists

- **Choosing an API standard:** Pick a standard matching your culture; amend with domain dictionary; start early. Avoid retrofitting.
- **Testing strategy:** Use the test pyramid at minimum; couple with the test quadrant only when stakeholder availability is real.
- **Contract testing:** Use producer contracts for large/external APIs; work toward CDC for internal ones.
- **Component vs contract test:** Use component tests for behavior; contracts for shape; component tests are not a contract substitute.
- **Stub server choice:** Generated-from-contract > recording > hand-rolled. Always scrub PII from recordings.
- **Testcontainers vs E2E:** Testcontainers stops at the integration boundary; don't subscribe-and-verify your own publishes.
- **Proxy / LB / Gateway:** Match the smallest tech that meets your requirements; check org mandate first.
- **API gateway type:** Enterprise = monetization + portal; Microservices = routing; Service-Mesh = only if already in a mesh.
- **Service mesh or libraries:** Single language → libraries are sufficient. Polyglot or many cross-cutting reqs → service mesh.
- **gRPC vs REST:** North-south external consumers = REST. East-west high-traffic controlled = gRPC.
- **Versioning:** URI / header / query — pick one. Combine with SemVer. Major bump = deprecation + migration guide + telemetry.
- **OAuth2 grant selection:** Auth Code (+ PKCE) for users; Client Credentials for M2M; Device for IoT/CLI; ignore Implicit/ROPC.
- **Scope design:** Coarse-grained per API surface; meaningful to humans at consent time; pair with per-resource checks at the service.
- **JWT encoding:** JWS when claims are non-sensitive; JWE when sensitive. Always short-lived (1-60 min).
- **Threat-model methodology:** STRIDE per element; DREAD for priority; OWASP API Security Top 10 as input.
- **DoS posture:** Rate limit per IP/client/geo; load shed on saturation; fail closed for financial; fail open for availability-critical.
- **Release strategy:** Canary for incremental risk; blue-green for tight-coupling releases; mirroring for behavior comparison.
- **Deployment vs release:** Always separate via flags or traffic shifts. Lockstep releases indicate over-coupling.
- **Feature flags:** Unique names; clean up after full rollout; last-known-value cache for resilience.
- **Observability:** Metrics + logs + traces via OpenTelemetry; alert on RED/golden signals with context; never logs alone for distributed debugging.
- **Zonal vs zero trust:** Default zero trust for new systems; bridge with multicluster mesh during migration.
- **NetworkPolicy:** Default-deny-all at the base; allow DNS first; allow each pair via selector-based egress rules.
- **Architecture end-state:** Pick Monolith / SOA / Microservices / Functions based on pain and team boundaries — don't microservice first.
- **Fitness functions:** Embedded in CI; cover code quality, resiliency, observability, performance, compliance, security, operability.
- **Cloud migration:** Mix of the 6 Rs; default to replatform when possible; repurchase often overlooked.
- **Type 1 vs Type 2 decisions:** Treat gateway, mesh, language adoption as Type 1; daily API design as Type 2.

## Key Takeaways

1. **APIs are architectural building blocks, not just endpoints.** Design for coupling, cohesion, and information hiding — REST vs gRPC is a tool choice, not the architecture.
2. **Adopt an API standard + OpenAPI early.** Standards shortcut design decisions; OAS powers codegen, validation, mocking, diffing, docs.
3. **Treat the OAS as infrastructure.** `openapi-diff`, `swagger-request-validator`, OpenAPI Generator, examples validation — all the tools.
4. **gRPC has stricter rules than OpenAPI.** Field numbers are the wire contract; reserve removed slots; never renumber.
5. **REST for north-south, gRPC for east-west.** Different traffic patterns, different coupling tolerances, different tools.
6. **Use the test pyramid.** Many unit tests, fewer service tests, very few E2E. Add the quadrant only when stakeholders participate.
7. **Contract testing pays for itself.** Pact + Pact Broker catch breaking changes locally; CDC for internal APIs; producer contracts for external.
8. **Use Testcontainers at integration boundaries.** Real DB/Kafka/Redis beats mock or in-memory; never conflate with E2E.
9. **Pick the smallest ingress tech that meets requirements.** Proxy < LB < Gateway; micro GW < Enterprise GW; mesh GW only with mesh.
10. **Coupling/Cohesion/Information Hiding at the gateway.** Facade/Adapter reduce coupling; do not let it become an ESB.
11. **Service mesh = consistent cross-cutting for east-west.** Routing, observability, security for polyglot services.
12. **Sidecars have cost; proxyless gRPC and eBPF are emerging.** Pick deliberately based on scale.
13. **Decouple deploy from release.** Feature flags + canary + Argo Rollouts make ship-without-breaking routine.
14. **Observability is the three pillars, not just logs.** OpenTelemetry; RED method; contextual alerting.
15. **Threat model with STRIDE per element + DREAD for priority.** Pair with OWASP API Top 10 as inspiration.
16. **Authn = who; Authz = what. JWTs, scopes, RBAC for coarse; per-object checks for fine.**
17. **OAuth2 + OIDC + Authorization Code (+ PKCE) is the default.** Short-lived access tokens; refresh-token reuse detection.
18. **Zero trust > zonal in cloud.** mTLS mesh + default-deny NetworkPolicy + scope checks everywhere.
19. **Evolve via Strangler Fig + feature flags + fitness functions.** Track "ilities" with measurement or they degrade.
20. **6 Rs for cloud, but most projects need a mix.** Repurchase is often overlooked.
21. **Architecture is socio-technical (Conway's Law).** Service boundaries mirror team boundaries.
22. **Type 1 decisions need rigor; Type 2 decisions need speed.** Don't confuse them.
23. **Watch AsyncAPI, HTTP/3, Service Mesh Interface.** Pilot, don't re-platform.
24. **Always pick the simplest solution that meets requirements.** Repeated across every ADR Guideline in the book.

## Cross-References
- Related: [[../Building_Microservices.md]]
- Related: [[../Building_Event-driven_Microservices.md]]
- Related: [[../Communication_Patterns.md]]
- Related: [[../Continuous_API_Management.md]]
- Related: [[../Software_Architecture_Patterns.md]]
- Related: [[../Software_Architecture_Hardparts.md]]
- Topic index: [[../INDEX.md]]

*Generated by opencode on 2026-07-18.*
