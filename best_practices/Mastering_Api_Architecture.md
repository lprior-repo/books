# Mastering API Architecture
**Author:** James Gough, Daniel Bryant, Matthew Auburn
**Topic tags:** `#api` `#architecture` `#testing` `#security`
**Language focus:** Language-agnostic (Java/Spring examples most common; Go mentioned for grpc-gateway)
**Sources:** `markdown_output/Mastering Api Architecture/Mastering Api Architecture.md` · `summaries/Mastering_Api_Architecture.md`

## TL;DR
A practical, end-to-end playbook for designing, building, testing, deploying, securing, and evolving API-driven systems. Anchors on a running "conference system" case study evolved from monolith → microservices → cloud/zero-trust, and ships concrete guidance on REST/gRPC/GraphQL selection, OpenAPI Specs, contract testing, API gateways vs. service meshes, OAuth2/JWT, threat modeling (STRIDE), and evolutionary cloud migration. Use it when you need *the* architectural decision (ADR) rationale for any part of an API platform.

---

## Best Practices by Topic

### REST Foundations & Richardson Maturity Model
`#api` `#architecture`

**Principle:** Model interactions as resources identified by URIs, advanced by correct HTTP verbs, with stateless, cacheable, layered, uniform interfaces.

**Do:**
- Target **Richardson Level 2** for service-to-service REST: multiple resource URIs + correct HTTP methods (GET/POST/PUT/DELETE) giving guarantees like GET idempotency.
- Use nouns, not verbs, in URIs (`/attendees` not `/getAttendees`).
- Honor `Accept` / `Content-Type` for content negotiation; only return content a consumer can actually parse.
- Treat REST as a *set of constraints* — client-server, stateless, cacheable, uniform interface, layered system.

**Don't:**
- Use HATEOAS (Level 3) for inter-service machine traffic — too chatty and the controls are usually hard-coded anyway. Reserve for flexible UI-style flows.
- Build only Level 0/1 (RPC-over-HTTP or "resources without verbs") and call it REST.

**Code:**
```http
GET http://mastering-api.com/attendees
Accept: application/json
---
200 OK
Content-Type: application/json
{
 "displayName": "Jim",
 "id": 1
}
```
*Ref: Mastering Api Architecture.md — "Introduction to REST and HTTP by Example"*

---

### REST API Standards & Structure (Microsoft REST API Guidelines)
`#api`

**Principle:** REST is intentionally loose — adopt a published standard early to guarantee consistency, naming, pagination, errors, and compatibility.

**Do:**
- Pick one published standard (book uses the Microsoft REST API Guidelines, RFC-2119 terminology) and supplement with an internal domain data dictionary.
- Keep names consistent; reuse widely-known domain terminology where it exists.
- Plan for filtering/pagination/errors **from day one** — retrofitting them into a raw array response is a breaking change.
- Be critical of existing APIs: are they actually in a format consumers understand?

**Don't:**
- Let every team invent their own REST conventions.

*Ref: Mastering Api Architecture.md — "REST API Standards and Structure"*

---

### Collections, Pagination & Filtering
`#api`

**Principle:** Never return a raw JSON array from a collection endpoint — wrap in an object so pagination metadata can be added later without breaking compatibility.

**Do:**
- Wrap collections in `{ "value": [...], "@nextLink": "{opaqueUrl}" }` from the start.
- Use OData-style filter expressions for queries (e.g., `$filter=displayName eq 'Jim'`).
- Treat pagination as pagination of partial results + instructions for the next page.

**Don't:**
- Return a top-level `[ {...}, {...} ]` — converting to an object later is a breaking change for every consumer.

**Code:**
```http
GET http://mastering-api.com/attendees
---
200 OK
{
 "value": [
   {
     "displayName": "Jim",
     "givenName": "James",
     "surname": "Gough",
     "email": "jim@mastering-api.com",
     "id": 1
   }
 ],
 "@nextLink": "{opaqueUrl}"
}
```
```http
GET http://mastering-api.com/attendees?$filter=displayName eq 'Jim'
```
*Ref: Mastering Api Architecture.md — "Collections and Pagination" / "Filtering Collections"*

---

### PII & URL Hygiene
`#api` `#security`

**Principle:** Never put personally identifiable information in URLs — paths and query params are routinely cached in logs and intermediaries.

**Do:**
- Use opaque internal IDs for resources (e.g., `/attendees/1`), not emails/usernames.
- Be aware paths/query strings persist in proxies, gateways, APM tools, browser history.

**Don't:**
- Use `?email=jim@...` or `/attendees/jim@mastering-api.com` as the resource identifier.

*Ref: Mastering Api Architecture.md — "REST API Standards and Structure"*

---

### Error Handling & Status Codes
`#api`

**Principle:** Provide accurate HTTP status codes plus a consistent, machine-parseable error structure so consumers can write one piece of code that handles errors uniformly.

**Do:**
- Use 2xx success, 3xx redirect, 4xx client error, 5xx server error; consumers build logic (retry, redirect) on these.
- Document what happens on unexpected failure (e.g., in a payment system, does a 500 mean the charge went through?).
- Keep an `InnerError` structure for internal stack traces/debugging and **strip it before external delivery**.

**Don't:**
- Return errors in the body alongside a 2xx success code.
- Leak stack traces, server versions, or sensitive details to external consumers.

*Ref: Mastering Api Architecture.md — "Error Handling"*

---

### OpenAPI Specification (OAS) as Core Infrastructure
`#api`

**Principle:** Treat the OpenAPI Specification (JSON/YAML) as a living artifact — it captures API structure, models, security, and metadata and powers codegen, validation, mocking, change detection, and docs.

**Do:**
- Use OAS for: code generation (client SDKs + server stubs via OpenAPI Generator), runtime validation, mocking, change detection, and auto-generated interactive docs.
- Validate examples with `openapi-examples-validator` — the `example` field is a free-form string.
- Use request/response validators (e.g., Atlassian `swagger-request-validator`) in the DMZ to terminate traffic that doesn't match the spec.
- Model the *full range of behaviors* in tests — OAS captures the shape but not the semantics.

**Don't:**
- Treat the spec as an afterthought generated once at the end.

**Code (Java, request/response validation):**
```java
// Using the location of the specification create an interaction validator
// The base path override is useful if the validator will be used
// behind a gateway/proxy
final OpenApiInteractionValidator validator = OpenApiInteractionValidator
 .createForSpecificationUrl(specUrl)
 .withBasePathOverride(basePathOverride)
 .build;
//Requests and Response objects can be converted or created using a builder
final ValidationReport report = validator.validate(request, response);
if (report.hasErrors()) {
 // Capture or process error information
```
*Ref: Mastering Api Architecture.md — "Specifying REST APIs Using OpenAPI" / "Practical Application of OpenAPI Specifications"*

---

### API Versioning & Semantic Versioning
`#api`

**Principle:** Exposed APIs **must** be versioned; communicate the nature of changes via SemVer (MAJOR.MINOR.PATCH) and have a documented mechanism for conveying version to consumers.

**Do:**
- **MAJOR** = incompatible change (active consumer decision to migrate; provide migration guide).
- **MINOR** = backward-compatible addition (consumer receives transparently).
- **PATCH** = bug fix on an existing MAJOR.MINOR (no shape change).
- Pick a version mechanism and stick to it: URI versioning (`/v1/attendees`), header (`Version: v1`), or query (`?version=2`). URI is most visible; header keeps the resource clean.
- Run `openapi-diff` in CI to **fail builds** on accidental breaking changes.

**Don't:**
- Treat versioning as an afterthought for externally exposed APIs.
- Mix minor additive fields that quietly change the meaning of an existing field.

**Code (detecting breaking vs. backward-compatible changes):**
```bash
$ docker run --rm -t \
 -v $(pwd):/specs:ro \
 openapitools/openapi-diff:latest /specs/original.json /specs/first-name.json
==========================================================================
...
- GET /attendees
 Return Type:
 - Changed 200 OK
 Media types:
 - Changed */*
 Schema: Broken compatibility
 Missing property: [n].givenName (string)
--------------------------------------------------------------------------
-- Result --
--------------------------------------------------------------------------
 API changes broke backward compatibility
--------------------------------------------------------------------------
```
```bash
$ docker run --rm -t \
 -v $(pwd):/specs:ro \
 openapitools/openapi-diff:latest --info /specs/original.json /specs/age.json
==========================================================================
...
- GET /attendees
 Return Type:
 - Changed 200 OK
 Media types:
 - Changed */*
 Schema: Backward compatible
--------------------------------------------------------------------------
-- Result --
--------------------------------------------------------------------------
 API changes are backward compatible
--------------------------------------------------------------------------
```
*Ref: Mastering Api Architecture.md — "API Versioning" / "Semantic Versioning" / "OpenAPI Specification and Versioning"*

---

### RPC with gRPC (East–West / High-Traffic)
`#api` `#architecture`

**Principle:** Use gRPC (protobuf + HTTP/2) for high-traffic, internal, producer-controlled service-to-service exchanges where smaller payloads and multiplexing pay off.

**Do:**
- Define `.proto` schemas with explicit field numbers; protobuf binary layout depends on field order/number.
- Adding a new optional field or new service method = backward compatible.
- Use `grpcurl` or gRPC UI for ad-hoc testing.
- Lean on HTTP/2 multiplexing (many requests over one TCP connection).

**Don't:**
- Remove, rename, or renumber a protobuf field — breaks wire compatibility.
- Change a field's data type, or promote an optional field to mandatory.
- Generate proto files alphabetically from OAS (`openapi2proto`) — adding a new alphabetically-earlier field renumbers everything.

**Code (`.proto`):**
```protobuf
syntax = "proto3";
option java_multiple_files = true;
package com.masteringapi.attendees.grpc.server;
message AttendeesRequest {
}
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
**Code (server impl, Java/Spring):**
```java
@GrpcService
public class AttendeesServiceImpl extends
 AttendeesServiceGrpc.AttendeesServiceImplBase {
 @Override
 public void getAttendees(AttendeesRequest request,
   StreamObserver<AttendeeResponse> responseObserver) {
   AttendeeResponse.Builder responseBuilder
     = AttendeeResponse.newBuilder();
   //populate response
   responseObserver.onNext(responseBuilder.build());
   responseObserver.onCompleted();
 }
}
```
**Code (testing):**
```bash
$ grpcurl -plaintext localhost:9090 \
 com.masteringapi.attendees.grpc.server.AttendeesService/getAttendees
{
 "attendees": [
   {
     "id": 1,
     "givenName": "Jim",
     "surname": "Gough",
     "email": "gough@mail.com"
   }
 ]
}
```
**Anti-pattern (alphabetical proto generation breaks compatibility):**
```protobuf
message Attendee {
 string a_new_field = 1;
 string email = 2;
 string givenName = 3;
 int32 id = 4;
 string surname = 5;
}
```
*Ref: Mastering Api Architecture.md — "Implementing RPC with gRPC" / "Multiple Specifications"*

---

### Choosing REST vs gRPC vs GraphQL — Modeling Exchanges
`#api` `#architecture`

**Principle:** Match the API style to the exchange context — REST for external/loose-coupling, gRPC for internal/high-throughput, GraphQL for cross-service querying/mobile.

**Decision heuristics:**
- **North–south / external consumers:** REST (low barrier to entry, strong domain model, loose coupling).
- **East–west / internal high-traffic, large payloads, producer controls both ends:** gRPC (HTTP/2 binary, multiplexing).
- **Cross-service querying, mobile clients, reporting/data warehouse:** GraphQL (client picks exact fields, single version across services).
- **Multiple specs:** You *can* expose REST + gRPC + GraphQL facades, but generating one from another (e.g., `grpc-gateway`, `openapi2proto`) creates versioning pain. **Design them independently.**

**Don't:**
- Conflate RPC's function-call style with REST's resource model when converting specs — coupling will haunt you.
- Quote "JSON is human-readable" as the primary reason for REST — modern tracing tools handle inspection; what matters is performance and parsing cost.

*Ref: Mastering Api Architecture.md — "Modeling Exchanges and Choosing an API Format" / "Multiple Specifications"*

---

### Testing APIs — Quadrant + Pyramid
`#api` `#testing`

**Principle:** Use the Test Quadrant (business vs. technology × support vs. critique) and the Test Pyramid (many unit tests, fewer service/component tests, very few E2E tests) to balance confidence, isolation, and speed.

**Do:**
- More unit tests (foundation, TDD), then service/component tests, then a thin layer of E2E for core user journeys.
- Q3 exploratory testing and Q4 non-functional (security, performance) are valid — automate where you can.
- Use BDD to write user journeys as scenario tests.

**Don't:**
- Build the "ice-cream cone" — many slow E2E tests on top of few unit tests. It gives a false sense of security and is slow/flaky to maintain.

*Ref: Mastering Api Architecture.md — "Testing Strategies" / "Test Quadrant" / "Test Pyramid"*

---

### Contract Testing (Producer + Consumer-Driven Contracts)
`#api` `#testing`

**Principle:** A contract is a defined interaction (request + response) between consumer and producer; verify both sides against it instead of spinning up full integration environments.

**Do:**
- **Producer contracts** for external/public APIs (producer owns the contract, breaking changes need migration plans).
- **Consumer-driven contracts (CDC)** when consumer + producer are in the same org — consumer submits the contract, discussion ensues, producer accepts/rejects via PR.
- Use **Pact** (default HTTP contract framework; CDC-enforcing, language-agnostic intermediate representation) and the **Pact Broker** for storage/publishing/CI integration.
- Generate a stub server from the contract so consumers can develop against it before the producer is ready.
- Run generated contract tests against the running API (producer) using test doubles for external dependencies.

**Don't:**
- Confuse contract testing with "conforms to a schema" — a contract is about a *specific interaction with examples*, not schema validity.
- Use contracts as scenario tests (e.g., "create attendee then list and verify"). Use component tests for that.
- Hand-roll contracts when a framework exists — Pact, Spring Cloud Contracts (JVM-centric).

**Code (Pact/Groovy DSL contract):**
```groovy
Contract.make {
 request {
   description('Get a list of all the attendees at a conference')
   method GET()
   url '/conference/1234/attendees'
   headers {
     contentType('application/json')
   }
 }
 response {
   status OK()
   headers {
     contentType('application/json')
   }
   body(
     value: [
       $(
         id: 123456,
         givenName: 'James',
         familyName: 'Gough'
       ),
       $(
         id: 123457,
         givenName: 'Matthew',
         familyName: 'Auburn'
       )
     ]
   )
 }
}
```
*Ref: Mastering Api Architecture.md — "Contract Testing" / "Why Contract Testing Is Often Preferable" / "How a Contract Is Implemented"*

---

### Component Testing (Behavior)
`#api` `#testing`

**Principle:** Component tests validate that multiple units work together to produce correct behavior in isolation, using mocks/test doubles for external dependencies.

**Do:**
- Verify status code, response body, content negotiation, authZ rejection, location header on create, and empty-dataset behavior (200 + `[]`, not 404).
- Use a request-client DSL (REST-Assured for Java, `httptest` for Go).
- Mock DAOs and external services — component tests stay within the service boundary.

**Code (REST-Assured):**
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
```
*Ref: Mastering Api Architecture.md — "API Component Testing" / "Case Study: Component Test to Verify Behavior"*

---

### Integration Testing, Stub Servers & Testcontainers
`#api` `#testing`

**Principle:** Verify the communication across a boundary (DB, external API, message broker) — prefer generated stub servers (from contracts), recordings of real traffic over hand-rolled stubs, and real instances via Testcontainers.

**Do:**
- Use contract-generated stub servers first; if not available, record real req/res pairs (Wiremock, camouflage) over hand-typing them.
- Use **Testcontainers** to spin up real databases / Kafka / Redis / NGINX in Docker during tests — same version as prod.
- Keep the boundary tight: trust the external system does its job (don't subscribe to Kafka in your test to check the message was correct — that belongs in E2E).

**Don't:**
- Hand-roll stub JSON — easy to introduce subtle errors (duplicate IDs, misspelled `familyNane`).
- Assume an in-memory DB (H2) matches production DB behavior.

**Code (subtle stubbing errors to avoid):**
```json
{
 "values": [
   {
     "id": 123456,
     "givenName": "James",
     "familyName": "Gough"
   },
   {
     "id": 123457,
     "givenName": "Matthew",
     "familyNane": "Auburn"
   },
   {
     "id": 123456,
     "givenName": "Daniel",
     "familyName": "Bryant"
   }
 ]
}
```
*Ref: Mastering Api Architecture.md — "API Integration Testing" / "Using Stub Servers" / "Containerizing Test Components: Testcontainers"*

---

### End-to-End (E2E) Testing
`#api` `#testing`

**Principle:** E2E validates full user journeys through real versions of *your* services; keep them few, scenario-driven, and representative of real usage.

**Do:**
- Automate E2E for core user journeys only (BDD style).
- Use realistic payloads — small test payloads miss buffer/serialization issues seen in production.
- Run performance tests against a like-for-like production environment; tools: Gatling, JMeter, Locust, K6.
- Keep TLS and authentication on — turning them off makes tests unrepresentative.

**Don't:**
- Replicate third-party UIs — outside your domain, hugely wasteful.
- Try to test every edge case at the E2E layer.

*Ref: Mastering Api Architecture.md — "End-to-End Testing" / "Automating End-to-End Validation" / "Types of End-to-End Tests"*

---

### API Gateways — North–South Ingress
`#api` `#architecture`

**Principle:** An API gateway is a reverse proxy with API-specific management features (routing, authn/z, rate limiting, observability, lifecycle, monetization), used for north–south traffic.

**Do:**
- Use a gateway to reduce coupling (facade/adapter), aggregate/translate backends, detect threats, observe consumption, manage the API lifecycle, and monetize.
- Deploy gateways as highly available, multi-AZ/region; treat them as a single point of failure with clear owners and on-call.
- Use **path-based** and **host-based** routing; nest prefixes or use regex as services get extracted (Strangler Fig pattern).

**Don't:**
- Route on request payloads — leaks domain coupling into the gateway and is expensive to parse.
- Put business logic in gateway plug-ins (Lua/Wasm/Groovy) — recreates the ESB anti-pattern.
- Chain gateways "turtles all the way down" — every hop adds latency and a failure point.
- Use a service mesh's ingress as a full API gateway — lacks enterprise features.

**Code (Ambassador Mapping, path-based):**
```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: legacy-conference
spec:
 hostname: "*"
 prefix: /
 rewrite: /
 service: conferencesystem.legacy:8080
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: legacy-conference
spec:
 hostname: "*"
 prefix: /attendees
 rewrite: /
 service: attendees.nextgen:8080
```
**Code (host-based routing):**
```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
 name: attendees-host
spec:
 hostname: "attendees.conferencesystem.com"
 prefix: /
 service: attendees.nextgen:8080
```
*Ref: Mastering Api Architecture.md — "API Gateways: Ingress Traffic Management"*

---

### Service Mesh — East–West Service-to-Service Traffic
`#api` `#architecture`

**Principle:** A service mesh provides routing, observability, and security (mTLS, authZ policies) for service-to-service traffic via a data plane (sidecar proxies, proxyless gRPC, or eBPF) controlled by a control plane.

**Do:**
- Use Istio `VirtualService` + `DestinationRule` for fine-grained routing, canary subsets, connection pooling, outlier detection.
- Use Linkerd for turn-key golden metrics (request volume, success rate, latency) + topology graphs.
- Use Consul `ServiceIntentions` (or OPA) for least-privilege network segmentation (deny-all default, explicit allow).
- Standardize on one mesh across the org; coordinate with existing networking to avoid double circuit-breaking / stripped headers.

**Don't:**
- Use the mesh as an ESB (business logic in Wasm filters).
- Use the mesh ingress as your only API gateway.
- Stack multiple proxy layers — adds latency and complexity.

**Code (Istio VirtualService + DestinationRule for canary):**
```yaml
---
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
---
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
**Code (Consul ServiceIntentions, deny-all then explicit allow):**
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
---
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
```
*Ref: Mastering Api Architecture.md — "Service Mesh: Service-to-Service Traffic Management"*

---

### Deploying vs. Releasing APIs
`#api` `#architecture`

**Principle:** **Deployment** = put new code in production. **Release** = direct user traffic to it. Decouple them via feature flags and traffic management.

**Do:**
- Use **feature flags** (per-user, per-%, per-env) toggled at runtime; cache last-known values for graceful degradation; clean up flags after migration with unique names.
- Use **API lifecycle states** (Planned → Beta → Live → Deprecated → Retired) tied to SemVer: only one Live major.minor; minors can deprecate briefly; majors stay deprecated for weeks/months with a migration guide.
- Major changes require simultaneous Live + Deprecated versions; URI version (`/v1/attendees`) or header (`Version: v1`).
- Choose a release strategy: **Canary** (small %, monitor, ramp), **Traffic mirroring** (dark launch, observe only), **Blue-green** (flip entire stack, easy rollback).

**Don't:**
- Reuse feature flag names/IDs (Knight Capital lost $460M this way).
- Treat minor/patch releases like majors — they should be consumer-transparent.
- Skip monitoring for canaries — you need golden signals + business KPIs to auto-promote/rollback.

**Code (LaunchDarkly feature flag, Java):**
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
**Code (Argo Rollouts canary with manual + auto promotion):**
```yaml
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
**Code (Argo AnalysisTemplate driven by Prometheus success rate):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
 name: success-rate
spec:
 args:
 - name: service-name
 - name: prometheus-port
   value: 9090
 metrics:
 - name: success-rate
   successCondition: result[0] >= 0.95
   provider:
     prometheus:
       address: "http://prometheus.example.com:{{args.prometheus-port}}"
```
*Ref: Mastering Api Architecture.md — "Deploying and Releasing APIs"*

---

### Observability — Three Pillars & API Metrics
`#api` `#architecture`

**Principle:** Metrics, logs, and traces are the operational minimum for reasoning about distributed API systems — implement all three via OpenTelemetry.

**Do:**
- Capture **RED** (Rate, Errors, Duration) / **Four Golden Signals** (latency, traffic, errors, saturation) but **add context** — a 403 storm may indicate an attack, not just a client mistake.
- Use **structured logging** with a `type` field (journal vs. diagnostics) for fast filtering.
- Propagate trace headers across every hop; if a service terminates a request and starts a new one, **copy headers downstream** (especially trace IDs).
- Tie alerts to baselines and beware false positives (weekend/holiday traffic dips).

**Don't:**
- Use RED/golden signals blindly — context matters.
- Send auth headers downstream carelessly — OAuth2 bearer tokens are safe; impersonation risks aren't.
- Allow response caching (`Cache-Control: no-cache, no-store` on the GET client) to mask broken canaries.

*Ref: Mastering Api Architecture.md — "Three Pillars of Observability" / "Important Metrics for APIs" / "Reading the Signals" / "Application Decisions for Effective Software Releases"*

---

### Threat Modeling (STRIDE) & OWASP API Security Top 10
`#api` `#security`

**Principle:** Shift security left — systematically apply STRIDE per element using DFDs, and use OWASP API Security Top 10 as both threat inspiration and mitigation checklist.

**6-step process:**
1. Identify objectives (business + security; e.g., "mitigate OWASP Top 10 for external exposure").
2. Gather information (right experts, all components).
3. Decompose the system (DFD: external entities, processes, datastores, data flows, boundaries).
4. Identify threats (STRIDE per element).
5. Evaluate risk (DREAD scoring: Damage + Reproducibility + Exploitability + Affected Users + Discoverability, each 1–10, /5).
6. Validate (re-run periodically; threat landscape evolves).

**STRIDE:**
- **S**poofing → authenticate every request (mitigate Broken User Authentication).
- **T**ampering → input validation at the gateway (OAS schema) **and** in the service; guard against mass assignment (whitelist bindable fields); use prepared statements.
- **R**epudiation → log and monitor all requests (Insufficient Logging & Monitoring).
- **I**nformation disclosure → don't leak PII (passport numbers, stack traces, server versions); use API management to track all deployed versions (Improper Assets Management).
- **D**enial of Service → rate limit + load shed (fixed window, sliding window, token bucket, leaky bucket); know your fail-open vs. fail-closed policy.
- **E**levation of privilege → enforce Object Level + Function Level Authorization on every endpoint (BOLA / BFLA).

**Do:**
- TLS termination at the gateway; modern protocol, TLS 1.2+.
- HTTP header allowlist in the gateway (strip `X-Assert-Role`, `X-Impersonate`).
- CORS preflight support for browser clients.
- Defense in depth: validate at the gateway **and** sanitize in the service.

**Don't:**
- Trust internal traffic by default (move toward zero trust).
- Default to fail-open for security tools without conscious decision (medical = fail-open OK; financial = fail-closed).
- Use security-through-obscurity (DREAD-D drops Discoverability for this reason).

**Code (mass assignment exploit — `devices` should be ignored on save):**
```http
PUT /attendees/123456
{
 "name": "Danny B",
 "age": 36,
 "devices": [
   "vulnerableDevice"
 ]
}
```
*Ref: Mastering Api Architecture.md — "Operational Security: Threat Modeling for APIs"*

---

### Authentication & Authorization (OAuth2, JWT, OIDC)
`#api` `#security`

**Principle:** Use OAuth2 as the standard authorization framework; JWT (JWS) as the compact signed token; OIDC for the identity layer; never mix API keys with user identity.

**Do:**
- **Authorization Code Grant + PKCE** for all user-facing clients (web SPA = public client = PKCE mandatory; server-side = confidential client = secret OK; PKCE adds protection either way).
- **Client Credentials Grant** for machine-to-machine (no refresh token; client re-requests access tokens).
- **Refresh tokens** for smooth UX; revoke on second-use detection; keep access tokens short-lived (1–60 min).
- **OAuth2 scopes** for coarse-grained authZ (e.g., `AttendeeRead`, `AttendeeAccount`); enforce at the gateway + service + data layers.
- **OIDC** when the client needs user identity — request `openid` scope to get an ID token; never substitute ID tokens for access tokens.
- Enforce authZ on **every endpoint** (BOLA + BFLA are top OWASP issues).

**Don't:**
- Use HTTP Basic for third-party API access (forces credential sharing).
- Use the Implicit Grant or Resource Owner Password Credentials Grant (legacy).
- Put confidential data in a JWS — it's signed but readable; use JWE for encryption.
- Use email/username as the JWT `sub` — they change; use a stable UUID.
- Mix API keys with user identity (a system holding an API key should not assert user identity without user consent).

**Code (example JWT claims):**
```json
{
 "iss": "http://mastering-api/",
 "sub": "18f913b1-7a9d-47e6-a062-5381d1e21ffa",
 "aud": "Attendee-Service",
 "exp": 1618146900,
 "nbf": 1618144200,
 "iat": 1618144200,
 "jti": "4d13ba71-54e4-4583-9458-562cbf0ba4e4"
}
```
**Scope mapping pattern (HTTP Method – endpoint – scope):**
```
GET  /attendees               AttendeeRead
GET  /attendees/{attendee_id} AttendeeRead
POST /attendees               AttendeeAccount
PUT  /attendees/{attendee_id} AttendeeAccount
```
*Ref: Mastering Api Architecture.md — "API Authentication and Authorization"*

---

### Evolving Toward API-Driven Architectures
`#api` `#architecture`

**Principle:** Use APIs as boundaries to increase cohesion and promote loose coupling (information hiding) — enabling guided, incremental evolution.

**Do:**
- Strive for **high cohesion** (functional, sequential, communicational, temporal) — APIs become focused points of change.
- Promote **loose coupling** so provider internals (datastore, algorithms) can change without breaking consumers; this also makes mocking/virtualizing in tests far easier.
- Use **fitness functions** (Code Quality, Resiliency, Observability, Performance, Compliance, Security, Operability) as automated architectural tests in CI.
- Use the **Strangler Fig** pattern (gateway routes new traffic to extracted services over time), **Facade/Adapter** for stable interfaces during migration, **API Layer Cake** for layered responsibilities.

**Don't:**
- Create "utils" APIs (low cohesion — change ripples everywhere).
- Expose internal data schemas/ORM models directly (mass assignment + coupling risk).
- Choose microservices/functions without DDD context mapping / event storming first.

*Ref: Mastering Api Architecture.md — "Redesigning Applications to API-Driven Architectures"*

---

### Cloud Migration & Zero Trust
`#api` `#architecture` `#security`

**Principle:** Migrate incrementally using the 6 Rs; API gateways provide location transparency; service mesh + network policies implement zero trust across hybrid environments.

**6 Rs:** Retain · Rehost (lift & shift) · Replatform · Repurchase · Refactor/Re-architect · Retire.

**Do:**
- Start at the edge: deploy a duplicate API gateway in cloud, configure it without disrupting prod, then incrementally shift traffic.
- Use multicluster service mesh peering for seamless on-prem ↔ cloud routing.
- Layer Kubernetes `NetworkPolicy` (Calico) under the mesh: default deny-all, then explicit DNS + egress/ingress allow rules matching mesh intentions.
- Adopt the 8 zero-trust principles (know architecture/identities/health; authorize everywhere; don't trust any network — including your own).

**Don't:**
- Trust cloud perimeter by default — supply-chain attacks and malicious insiders exist.
- Leave DNS unlocked when locking down a pod.

**Code (default-deny all ingress+egress):**
```yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
 name: default-deny-all
spec:
 podSelector: {}
 policyTypes:
 - Egress
 - Ingress
```
**Code (allow DNS for legacy conference app):**
```yaml
---
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
```
**Code (allow conference → attendees namespace egress):**
```yaml
---
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
*Ref: Mastering Api Architecture.md — "Using API Infrastructure to Evolve Toward Cloud Platforms"*

---

### Emerging Tech & Continuous Learning
`#api` `#architecture`

**Watch:**
- **AsyncAPI** — spec for event-driven/message-based APIs complementing OpenAPI.
- **HTTP/3 (QUIC over UDP)** — fixes HTTP/2 head-of-line blocking; requires ingress proxy upgrades; already 70%+ browser support.
- **Platform-based mesh** + **SMI** (Service Mesh Interface) — mesh as a platform decision, not an app decision.
- **eBPF / Cilium** — sidecarless mesh via kernel.
- **Proxyless gRPC** — back to language libraries connecting to external control planes.

**Do:**
- Treat API gateway/mesh selection as a **Type 1 decision** (irreversible/costly) — apply rigor and ADRs.
- Honor Conway's Law — your architecture mirrors your org chart; read *Team Topologies*.
- Keep learning: fundamentals (cohesion/coupling), analyst radars (ThoughtWorks, Gartner, CNCF), conferences (QCon, APIDays, KubeCon).

*Ref: Mastering Api Architecture.md — "Wrap-up" / "Preparing for the Future"*

---

## Anti-Patterns & Common Mistakes

- **Returning a raw JSON array from a collection endpoint** → *fix:* wrap in `{ "value": [...] }` from day one so you can add `@nextLink` without breaking compatibility.
- **PII in URLs (email, name)** → *fix:* use opaque internal IDs.
- **Errors returned as 2xx + body, or stack traces leaked externally** → *fix:* accurate HTTP status codes + consistent error structure + stripped `InnerError`.
- **Generating protobuf from OAS alphabetically** → *fix:* design REST and RPC independently; never autogenerate one from the other.
- **HATEOAS for inter-service traffic** → *fix:* target Richardson Level 2 for M2M.
- **Ice-cream-cone test pyramid** → *fix:* more unit/contract tests, fewer E2E.
- **Treating "conforms to schema" as "contract tested"** → *fix:* contracts define specific interactions with examples.
- **Gateway loopback** (routing internal S2S traffic out through the edge gateway) → *fix:* use internal service discovery / mesh.
- **Gateway as ESB** (business logic in plug-ins) → *fix:* keep gateway cross-cutting only.
- **Turtles all the way down** (stacked gateways) → *fix:* consolidate edge layers.
- **Routing on request payloads** → *fix:* route on host/path/query only.
- **Feature flag reuse** → *fix:* unique names, clean up after migration.
- **Mixing API keys with user identity** → *fix:* OAuth2 + user consent.
- **ID tokens used as access tokens** → *fix:* OIDC ID token is for client identity only.
- **Confidential data in JWS** → *fix:* use JWE for encryption.
- **Trusting internal traffic by default** → *fix:* zero trust, mTLS everywhere, deny-all network policies.
- **Fail-open security without conscious decision** → *fix:* pick fail-open vs. fail-closed based on business needs.

## Decision Heuristics / Checklists

- **REST vs. gRPC vs. GraphQL:** External/loose coupling → REST. Internal/high-throughput/producer-owns-both-ends → gRPC. Cross-service querying/mobile/reporting → GraphQL.
- **Versioning mechanism:** URI (`/v1/...`) for visibility; header (`Version: v1`) for resource-clean URLs; query (`?version=2`) rarely. Pick one and document it.
- **Test type by question:** "Does the API conform to an interaction?" → contract. "Does the service behave correctly in isolation?" → component. "Does the boundary to DB/external work?" → integration (Testcontainers). "Does the full user journey work?" → E2E (few).
- **OAuth2 grant selection:** User-facing confidential client (server-side web) → Auth Code Grant. User-facing public client (SPA/mobile) → Auth Code Grant + PKCE. Machine-to-machine → Client Credentials. IoT → Device Authorization. (Avoid Implicit & ROPO.)
- **API gateway type:** External/business-API monetization → Traditional Enterprise. Microservices ingress → Micro gateway. Already on a mesh → Service Mesh gateway.
- **Service mesh adoption:** Single language + simple routing → library. Multi-language + advanced XFN (authN/Z, rate limit, observability) → mesh.
- **Type 1 vs. Type 2 decisions:** API gateway, service mesh, OAuth2 provider = Type 1 (rigor, ADR). Day-to-day API field choices = Type 2 (move fast).

## Key Takeaways

1. **APIs are architectural building blocks, not endpoints** — design for cohesion, coupling, and domain boundaries; the technology choice is secondary.
2. **Adopt an API standard early** — Microsoft REST API Guidelines or similar; retrofitting is painful.
3. **OpenAPI Specifications are essential infrastructure** — codegen, validation, mocking, change detection, docs. Treat as living artifacts.
4. **Test rigorously via the pyramid** — many unit + contract, fewer component + integration, very few E2E. Contract testing catches breaking changes early.
5. **Gateway ≠ Mesh** — gateway manages north–south; mesh manages east–west; both provide routing/observability/security at different points.
6. **Decouple deployment from release** — feature flags + canary/mirror/blue-green via gateway or mesh.
7. **Shift security left with threat modeling** — STRIDE + OWASP API Top 10; security is not an afterthought.
8. **OAuth2 + JWT + OIDC is the standard** — Authorization Code (+PKCE) for users, Client Credentials for M2M, scopes for coarse authZ, OIDC for identity.
9. **Evolve incrementally via Strangler Fig** — facades + adapters; API infra provides location transparency.
10. **Cloud migration is incremental and reversible** — 6 Rs + gateway-driven traffic shifting + multicluster mesh + zero trust.
11. **Architecture is socio-technical** — Conway's Law; team boundaries shape system boundaries.
12. **Document decisions with ADRs** — context, decision, consequences; immutable; keep rejected ones.
13. **There is no free lunch** — every decision is a trade-off; the architect's job is to make trade-offs explicit.
14. **Keep learning continuously** — AsyncAPI, HTTP/3, eBPF meshes, platform integration.

## Cross-References
- Related: [[../Restful_Web_API_Patterns_and_Practices.md]] (deeper hypermedia, RFC 7807, PUT-create, ALPS)
- Topic index: [[../INDEX.md]]
