# Learning API Styles

**Authors:** Lukasz Dynowski and Marcin Dulak
**Publisher:** O'Reilly Media, July 2025
**Topic tags:** `#api` `#architecture` `#testing` `#grpc` `#graphql` `#rest`
**Language focus:** Language-agnostic (Python examples)
**Sources:** `markdown_output/Learning_API_Styles_-_Lukasz_Dynowski/Learning_API_Styles_-_Lukasz_Dynowski.md` · `summaries/Learning_API_Styles_-_Lukasz_Dynowski.md`

## TL;DR

Seven API styles (REST, GraphQL, Atom/Web Feeds, gRPC, Webhooks, WebSocket, RabbitMQ/broker-based) are each defined by a specific interaction pattern. No single style is "best" — REST wins for cross-platform CRUD, GraphQL for low-bandwidth flexible clients, gRPC for service-to-service RPC, Webhooks for event push, WebSocket for bidirectional, Atom for syndication, and brokers for asynchronous decoupling. Security must be woven into every phase of the API lifecycle, not bolted on at deployment. Versioning, contract testing, and schema/IDL-first design are the load-bearing practices that make APIs evolvable.

---

## Best Practices by Topic

### The API Lifecycle (Iterative, Not Sequential)

**Principle:** The API lifecycle is iterative — every phase (planning → design → implementation → testing → deployment → maintenance → retirement) influences the others; phases run concurrently, not in a waterfall.

**Do:**
- Treat security and documentation as cross-cutting concerns present in every phase, not as a single phase.
- Establish functional requirements (FRs) and nonfunctional requirements (NFRs) during planning; NFRs include availability, performance, security, deployability.
- Drive every change through the ACED model (Agree, Consume, Evolve, Decommission).
- Plan evolution early — adding features when an API has 1000 consumers is far costlier than at 10.
- Embed compliance constraints (GDPR, HIPAA) directly into requirements.

**Don't:**
- Don't do "Big Up Front Design" — complete *enough* design to move on, then iterate.
- Don't defer documentation until maintenance; software is never "finished."
- Don't treat security as a deployment checklist; security decisions belong in design.

**Code (planning questions checklist):**
```
* What is the API scope? (private / partner / public)
* Who are the API user devices? (browser / mobile / IoT / AI agents)
* What are the requirements? (languages, time limits, external deps)
* What versioning strategy will you use?
* Are there regulatory constraints? (GDPR, HIPAA)
* Are there established communication channels for API users?
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Planning"*

---

### API Lifecycle — Testing in CI/CD

**Principle:** Tests live in CI/CD pipelines and run continuously to detect regressions early; the testing strategy depends on what you test (integration vs contract vs E2E).

**Do:**
- Use the Agile testing quadrants: Q1 (unit/component — fast, dev-owned), Q2 (system functionality — supports the team), Q3 (user-facing critique — UAT), Q4 (NFRs — security, performance).
- Apply contract testing to verify evolving consumers/providers still respect the API schema.
- Combine contract testing with API fuzzing — random inputs exercise a larger portion of the contract than handcrafted cases.
- Use record-and-replay testing: dump a real service's response to a file and replay it for repeatable tests.
- Run Docker-based integration tests against real (containerized) dependencies.

**Don't:**
- Don't depend solely on mocks; integration tests against running services reveal real interaction bugs.
- Don't conflate defensive programming (broad input handling) with fail-fast / offensive programming (reject invalid inputs immediately).
- Don't skip the recording when relying on third-party services you can't run locally.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Testing" / "Contract testing and fuzzing" / "End-to-end testing"*

---

### API Retirement and Deprecation

**Principle:** APIs don't last forever — retirement is a normal lifecycle stage, and deprecation must be communicated in-band and out-of-band.

**Do:**
- Set a maximum supported version policy (e.g., max two concurrent API releases; delete v1 when v3 ships).
- Use HTTP `Deprecation` and `Sunset` headers to signal end-of-life to clients.
- Provide a `Link` header pointing to deprecation documentation with migration guides and contact info.
- Maintain zombie-API inventories: routinely scan for unmaintained APIs that still run.

**Don't:**
- Don't ship a public API without a deprecation policy — mistakes are hard to undo once the API is released.
- Don't let sunset dates pass without warning banners on the docs portal and CLI warnings (cf. Kubernetes v1 Ingress warning).

**Code:**
```
Sunset: Wed, 11 Nov 2026 11:11:11 GMT
Deprecation: @1688169599
Link: <https://developer.example.com/deprecation>;
      rel="deprecation"
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Retirement" / "Example 1-4"*

---

### API Design — Interface vs Implementation

**Principle:** Decouple the API interface from the implementation; leaky abstractions and Hyrum's Law guarantee clients will depend on whatever you ship, even undocumented behavior.

**Do:**
- Plan for evolution from the start — additive changes only when possible; plan breaking changes deliberately.
- Treat the interface as the contract: changes to the interface have higher cost than changes to the implementation.
- Test changes against JSON Schema to determine whether a proposed change is breaking.
- Identify the interface's least-changeable parts first (the ones with the highest coupling cost) and design them last in `create`-stage APIs.

**Don't:**
- Don't promise protocol behavior in the contract and expect it to stay uncovered (Hyrum's Law).
- Don't ignore the "Law of Leaky Abstractions" — implementation details surface through the interface.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Implementation" / "INTERFACE VERSUS IMPLEMENTATION"*

---

### API Design — Naming, Naming Style, and Naming Conventions

**Principle:** A good name is expressive, intuitive, pronounceable, context-matched, intent-conveying, and consistent across the API.

**Do:**
- Use American English (e.g., `durationSeconds`, `temperatureCelsius`, `weightGrams`).
- Include units in scalar fields; assume SI/imperial mix-up is the most expensive class of bug (cf. Mars Climate Orbiter, Tokyo Disneyland roller-coaster).
- Choose singular vs plural based on API style — plurals for REST resources (`/orders/123`), flexible for gRPC/GraphQL/broker.
- Prefer the positive form of booleans: `enabled` over `disabled`; `allowed` over `disallowed`.
- Avoid boolean prefixes — use `activated`, not `isActive`.

**Don't:**
- Don't rely on context alone; provide auxiliary docs for ambiguous terms.
- Don't encode booleans as 0/1 or yes/no strings — stick to standard JSON true/false.

**Code (resource-oriented REST naming):**
```
POST   /api/orders          Create a new order
GET    /api/orders          Retrieve all orders
GET    /api/orders/{id}     Retrieve a single order
PUT    /api/orders/{id}     Update an order
DELETE /api/orders/{id}     Delete an order
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Naming" / "RESOURCE-ORIENTED VERSUS INTENT-ORIENTED APIS"*

---

### Resource-Oriented vs Intent-Oriented APIs

**Principle:** REST = declarative/resource-oriented (nouns + HTTP verbs); gRPC = imperative/intent-oriented (verb-noun methods); GraphQL mixes both. Pick the model that matches your use case.

**Do:**
- Use resource-oriented when many clients benefit from predictability (REST is the universal interface).
- Use intent-oriented when each endpoint represents a specific action (Stripe's Payment Intents).
- For GraphQL: queries are declarative (declarative), mutations are imperative.
- For broker APIs: name routing keys `orders.create`, `orders.get`, etc.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "RESOURCE-ORIENTED VERSUS INTENT-ORIENTED APIS"*

---

### API Versioning

**Principle:** Versioning balances backward compatibility (client-server) with forward compatibility (messaging systems). Avoid breaking changes whenever possible — additive changes are preferred.

**Do:**
- Treat additive changes (new fields, new endpoints, new query params with defaults) as non-breaking.
- Choose a versioning strategy that matches your style: path-based for REST, package/service name changes for gRPC, renamed fields (`updateOrderV2`) for GraphQL.
- Communicate via changelogs, Atom feeds, or in-response metadata sections.
- Document version semantics: SemVer `MAJOR.MINOR.PATCH` (MAJOR = breaking, MINOR = additive, PATCH = bugfix), Calendar (`2024-11-01`), or Hash (`237a2b4f`).

**Don't:**
- Don't combine versioning strategies — `/api/v1/orders?version=1.2.3` complicates routing and caching.
- Don't ship breaking changes without a documented migration path.
- Don't introduce a new "version" just to add features — extend the existing schema first.

**Code (path vs query vs header vs payload):**
```
# Path-based
https://example.com/v1/orders

# Query parameter
https://example.com/orders?api-version=v1

# Header-based
Accept: application/vnd.example+json;api-version=1

# Message payload (broker / event-driven)
{ "version": "v1", "data": { ... } }
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Versioning"*

---

### Backward and Forward Compatibility

**Principle:** Backward compatibility matters in client-server APIs; forward compatibility matters in messaging — both must coexist in messaging-based systems.

**Do:**
- Keep the maximum number of in-flight message versions low in broker-based systems.
- Use idempotent consumers and tolerate multiple message versions in transit simultaneously.
- Provide version negotiation when the API needs both backward and forward compatibility.

**Don't:**
- Don't release a breaking change just because it's "more correct" — the coupling cost may dwarf the design improvement.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API BACKWARD AND FORWARD COMPATIBILITY"*

---

### Encoding and Serialization

**Principle:** Encoding ≠ serialization ≠ compression. Encoding is format conversion; serialization converts data structures to byte streams; compression is a form of encoding that reduces size.

**Do:**
- Use JSON for human-readable, debuggable web APIs; use Protocol Buffers/Avro for size- and speed-critical paths.
- Pick binary formats (protobuf, Avro, MessagePack, Thrift) when bandwidth or CPU matter more than human readability.
- Use ASCII/UTF-8/JSON/XML/YAML for text-encoded payloads; reserve binary for performance paths.
- Establish consistent decisions for null/missing fields (Protobuf defaults: int32→0, string→"", bool→false).
- Pick Booleans as true/false (JSON), not 0/1 or yes/no.
- Beware of cross-language numeric precision (JavaScript `JSON.stringify({number: 9007199254740999})` → `...741000`).

**Don't:**
- Don't rely on `JSON.parse` precision for integers — represent large integers as strings when exact preservation matters.
- Don't confuse compression with encryption — encryption usually *increases* size.

**Code (Apache Avro serialization in Python):**
```python
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

user_avsc = '''{
 "type": "record",
 "name": "User",
 "fields": [
  {"name": "email",       "type": "string"},
  {"name": "active",      "type": "boolean", "default": false},
  {"name": "access_level","type": "int",     "default": 0}
 ]
}'''
schema = avro.schema.parse(user_avsc)
with DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema) as writer:
    writer.append({"email": "ld@example.com", "active": False, "access_level": 0})
    writer.append({"email": "md@example.com", "active": True,  "access_level": 3})
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Encoding" / "Example 2-3"*

---

### Filtering, Counting, Sorting, and Pagination

**Principle:** Pick pagination that scales with your dataset; offset-based pagination is simple but degrades on large datasets; cursor-based is consistent under concurrent inserts/deletes.

**Do:**
- Use **offset-based** (`?page=N&page_size=100`) for small datasets with stable content (admin reports).
- Use **cursor-based** (opaque token) for large or dynamic datasets; the cursor identifies a specific item, making retrieval efficient and consistent.
- Use **field-based filtering** (`country=DK&snowfall>=0.5`) for safe, framework-friendly filters; let the API own validation.
- Add `include_deleted` flag when soft-delete is in play; document non-standard HTTP method behavior.

**Don't:**
- Don't build SQL-injection-vulnerable filter-string parsers; never pass raw SQL through query params.
- Don't use offset-based pagination when items are frequently inserted/deleted — items will be skipped or duplicated across pages.
- Don't expose `count` and `sort` on distributed systems without verifying aggregate support — these can be slow or unavailable.
- Don't release soft-delete behavior without versioning — adding soft-delete is a breaking change.

**Code (offset-based pagination):**
```
curl 'https://example.com/api/v1/orders?page=2&page_size=100'
{
 "count": 1478,
 "next": "https://example.com/api/v1/orders?page=3&page_size=100",
 "previous": "https://example.com/api/v1/orders?page=1&page_size=100",
 "results": [...]
}
```
**Code (cursor-based pagination):**
```
curl 'https://example.com/api/v1/orders?limit=100&next=123abc'
{
 "next": "456cde",
 "results": [...]
}
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Pagination" / "Filtering" / "Counting and Sorting"*

---

### Long-Running Tasks

**Principle:** For tasks that exceed request timeouts, return `202 Accepted` with a task resource URL the client can poll; never block the client indefinitely.

**Do:**
- Define a task resource at the top-level of the API: `/api/v1/tasks`.
- Persist and track task metadata (status, progress, timestamps, errors, result location).
- Support a state machine: pause / resume / cancel where applicable.
- Use `?action=resume` (query param) for custom actions to avoid path-vs-resource ambiguity.

**Don't:**
- Don't tie custom actions into the URI path (`/resource/ID/action`) — `action` can be mistaken for a resource.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Long-Running Tasks"*

---

### Request Deduplication, Retry, and Rate Limiting

**Principle:** Make retries safe (idempotency), bounded (cutoff), and jittered (avoid retry storms); deduplicate via client-side request IDs; rate-limit early in the request path.

**Do:**
- Generate a unique request ID (UUID) per client request and pass it; the server should return the prior response on duplicates.
- Use exponential back-off with a maximum retry cutoff and add timing jitter.
- Honor the server's `Retry-After` header.
- Apply throttling as early as possible on the request path (CDN / API gateway).
- Combine throttling with IP allowlisting and CAPTCHA for sensitive endpoints (e.g., password reset).

**Don't:**
- Don't retry indefinitely — a retry storm extends outages.
- Don't rely on TCP alone to prevent the thundering herd problem.
- Don't try to defend against DDoS by throttling alone — many distributed clients can each make only a few requests.

**Code (retry with exponential back-off):**
```
Retry 1: +2s
Retry 2: +4s
Retry 3: +8s
Retry 4: +16s → CUTOFF (pause until cutoff timeout expires)
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Request Deduplication" / "Request Retry" / "Rate Limiting"*

---

### Caching and Performance

**Principle:** Caching reduces load and improves latency, but introduces staleness, memory cost, and operational complexity. Cache at client and server side with proper invalidation.

**Do:**
- Use client-side caching for static assets, with TTL or ETag/Last-Modified validation.
- Use server-side caching for hot paths, keeping responses in memory or a distributed cache.
- Compress payloads with gzip or Brotli to reduce transfer size (trade CPU for bandwidth).
- Prefer binary encoding (protobuf, Avro) for performance-critical APIs; JSON/XML for debuggable ones.
- Use HTTP caching headers (ETag, Last-Modified, Cache-Control) consistently.

**Don't:**
- Don't cache sensitive data without encryption and access controls.
- Don't expect vertical scaling to fix performance issues — horizontal scaling is often necessary.
- Don't skip HTTP caching — it is one of the cheapest performance wins.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Caching" / "GENERAL TIPS TO IMPROVE API PERFORMANCE"*

---

### REST — Decision Heuristics

**Principle:** REST is best for cross-platform CRUD over HTTP — for north-south traffic, public APIs, internet-scale distributed systems with stateless components.

**Do:**
- Use REST for stateless, internet-scale distributed systems with cross-platform clients.
- Combine REST with HTTP/2 or HTTP/3 for production efficiency (multiplexing, header compression).
- Use CDNs to cache responses closer to users.
- Use HATEOAS to make APIs self-describing and navigation-friendly (when the trade-offs fit).
- Most "REST" APIs are RESTless (Levels 0–2 of Richardson's maturity model); this is fine — full HATEOAS is rarely worth the complexity.
- Apply defensive programming on inputs (but don't conflate with fail-fast; choose deliberately).
- Use path-based versioning with URL templates — versioning is not standardized in REST.

**Don't:**
- Don't ship code-on-demand (the optional REST constraint) unless you've audited the XSS / injection risk.
- Don't assume REST is the right answer for service-to-service east-west traffic — gRPC or messaging is usually better.
- Don't reinvent CRUD mapping — POST = create, GET = read, PUT = update, DELETE = delete.

**When to Use REST:** distributed systems, cross-platform integration, internal/external APIs over which you have no control, systems requiring caching, low-friction adoption.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "REST API" / "Trade-Offs" / "When to Use REST"*

---

### GraphQL — Decision Heuristics

**Principle:** Use GraphQL when network footprint and battery matter (mobile/IoT), when nested data requires multiple REST calls, when a single endpoint is preferred, or when rapid prototyping is needed.

**Do:**
- Use GraphQL for mobile / IoT / low-bandwidth clients — clients request exactly the data they need.
- Combine multiple operations (queries + mutations) into one request via aliases and selection sets — GraphQL is less chatty than REST.
- Use introspection for self-documentation; if disabled, prefer tools like SpectaQL / Voyager.
- Set query complexity limits to defend against recursive / aliasing / batch abuse.
- Use GraphQL as a facade (BFF or federated) for microservices — one schema, many sources.
- Default to additive (versionless) evolution: add fields, don't version.

**Don't:**
- Don't expose GraphiQL in production without authentication — it's a security hole.
- Don't rely on HTTP status codes — GraphQL returns 200 OK with errors in the body (always inspect `errors`).
- Don't naively trust GraphQL introspection — disable it (or use Clairvoyance-resistant schemas) in production.
- Don't enable multipart/form-data naively — CSRF attack surface increases.
- Don't ignore the N+1 problem — use DataLoader or framework extensions (e.g., Strawberry's `DjangoOptimizerExtension`).

**When to Use GraphQL:** applications requiring low network footprint, mobile/IoT clients, nested data, BFF/federated architectures, rapid prototyping.

**Code (GraphQL schema with Strawberry):**
```python
from strawberry_django.optimizer import DjangoOptimizerExtension
from .queries import Query
from .mutations import Mutation

schema = Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension],
)
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "GraphQL" / "Trade-Offs" / "When to Use GraphQL"*

---

### gRPC — Decision Heuristics

**Principle:** Use gRPC for service-to-service communication in microservices, especially when you need streaming, low latency (HTTP/2 + protobuf), and a typed contract enforced by code generation.

**Do:**
- Define APIs IDL-first in `.proto` files; commit the `.proto` as the source of truth.
- Use streaming RPCs only when needed (server-stream, client-stream, bidirectional); default to unary.
- Use `protoc` plugins (e.g., `buf` for linting, breaking-change detection; `ghz` for load testing).
- Enable gRPC reflection for runtime documentation/introspection in dev environments.
- Set request deadlines and use cancellation contexts for client-side timeout control.
- Use status codes with structured error details (don't overload `OK`).
- Apply server-side caching only when the cached request is genuinely reusable (status code caching semantics matter).
- Distinguish protocol semantics from wire format: gRPC requires HTTP/2 trailers, which the browser fetch API lacks — use gRPC-Web or Connect Protocol.

**Don't:**
- Don't append `V2` to method names — version the package/service name instead.
- Don't store one message in one file for tiny projects — balance readability.
- Don't share generated code without controlling the protoc version; pin tool versions in CI/CD.
- Don't expose gRPC to browsers directly — use gRPC-Web, Connect, or a gateway.
- Don't make protobuf defaults implicit in your domain — set defaults explicitly.

**Code (gRPC unary RPC protobuf):**
```protobuf
syntax = "proto3";
package echo.v1;
option go_package = "github.com/ldynia/learning-api-styles/grpc/src/echo/echo/proto/echo/v1";

message EchoRequest  { string content = 1; }
message EchoResponse { string content = 1; }

service EchoService {
  rpc DemoUnary(EchoRequest) returns (EchoResponse);
}
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "gRPC" / "Trade-Offs" / "When to Use gRPC"*

---

### gRPC — Four RPC Types

**Principle:** Choose the simplest RPC type that solves the problem; prefer unary; reach for streaming only when the workload is naturally stream-shaped.

**Types:**
- **Unary** — single request, single response. Default for most use cases.
- **Server streaming** — single request, stream of responses (e.g., LLM token streams, market data feeds).
- **Client streaming** — stream of requests, single response (e.g., batch uploads, telemetry aggregation).
- **Bidirectional streaming** — both sides stream independently (e.g., chat, multiplayer game state sync).

**Code (server with all four types):**
```python
class EchoServicer(echo_pb2_grpc.EchoServiceServicer):
    def DemoUnary(self, request, context):
        return echo_pb2.EchoResponse(content=request.content)

    def DemoServerStreaming(self, request, context):
        for i in range(3):
            yield echo_pb2.EchoResponse(content=f"{request.content}-{i}")

    def DemoClientStreaming(self, request_iterator, context):
        msgs = [r.content async for r in request_iterator]
        return echo_pb2.EchoResponse(content=" ".join(msgs))

    def DemoBidirectionalStreaming(self, request_iterator, context):
        async for r in request_iterator:
            yield echo_pb2.EchoResponse(content=r.content.upper())
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "The Four RPC Types" / "Example 8-10"*

---

### Webhooks — Decision Heuristics

**Principle:** Use webhooks for one-to-one or one-to-many event push — when the source knows when an event happened and the destination should react without polling.

**Do:**
- Require HMAC-signed payloads with a shared secret (use the `standard-webhooks` spec).
- Include `Webhook-Id`, `Webhook-Signature`, `Webhook-Timestamp` headers on every delivery.
- Validate the timestamp (e.g., reject if older than 5 seconds) to prevent replay attacks.
- Validate payload size (reject oversized payloads with `413 Payload Too Large`).
- Implement retries with exponential back-off and dead-letter queues on the source side.
- Document webhooks with OpenAPI 3.1's `webhooks:` field (or 3.0's `callbacks:` for in-band registration).
- Acknowledge on success (HTTP 2xx); treat any non-2xx as a failed delivery on the source side.

**Don't:**
- Don't expose detailed error messages on public webhook endpoints (only on internal ones).
- Don't skip the timestamp check — it enables replay attacks.
- Don't assume CSRF protection — webhook endpoints typically need `csrf_exempt`.
- Don't treat webhooks as guaranteed delivery — retries are necessary but not infinite.
- Don't couple webhook URLs and payload formats across breaking changes without versioning both.

**Code (manual HMAC verification per `standard-webhooks`):**
```python
wh_received_signature = request.headers.get("Webhook-Signature")
wh_timestamp          = request.headers.get("Webhook-Timestamp")
timestamp = datetime.fromtimestamp(int(wh_timestamp), tz=timezone.utc)
if int((datetime.now(timezone.utc) - timestamp).total_seconds()) >= 5:
    return JsonResponse({"errors": ["Request is too old."]}, status=400)

payload  = request.body.decode("utf-8")
secret   = WEBHOOK_SECRET.encode("utf-8")
sig_scheme = f"{wh_id}.{int(wh_timestamp)}.{payload}".encode("utf-8")
signature  = hmac.new(secret, msg=sig_scheme, digestmod="SHA256").digest()
signature_b64 = base64.b64encode(signature).decode("utf-8")
expected = f"v1,{signature_b64}"
if wh_received_signature != expected:
    return JsonResponse({"errors": ["HMAC mismatch."]}, status=401)
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Webhooks" / "Security" / "Trade-Offs"*

---

### WebSocket — Decision Heuristics

**Principle:** Use WebSocket only when bidirectional full-duplex communication at low latency is required — chat, live dashboards, alerts, multiplayer games, collaborative editing.

**Do:**
- Authenticate during the opening handshake (JWT, mTLS) — there's no built-in auth model per-message.
- Use ping/pong frames for keepalive; implement client reconnect with back-off (avoid thundering herd).
- Validate the `Origin` header — but know that malicious clients can spoof it.
- Run WebSocket over WSS (TLS) on port 443 to pass through proxies/firewalls.
- Use Redis pub/sub (or similar) to scale WebSocket across multiple server instances.
- Document the WebSocket API with AsyncAPI.
- Apply application-level compaction (data aggregation, compression, deduplication, pruning) for backpressure.
- Track your budget per message and per connection; cap both.

**Don't:**
- Don't expect HTTP-style caching — WebSocket doesn't support it.
- Don't assume message acknowledgment — WebSocket inherits TCP reliability but no app-level ACK.
- Don't reuse a connection across users; track per-connection state carefully.
- Don't expose WebSocket to the public without origin validation and authentication.
- Don't assume unlimited connection counts — limit per server, use a load balancer for scale.
- Don't use WebSocket for one-way streams — Server-Sent Events (SSE) is simpler.

**When to Use WebSocket:** notifications, online chat, multiplayer games, visualization dashboards, interactive collaboration.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "WebSocket" / "Trade-Offs" / "When to Use WebSocket"*

---

### Broker-Based APIs (RabbitMQ) — Decision Heuristics

**Principle:** Use broker-based messaging when message delivery must be guaranteed, when decoupling components matters, or when synchronous interaction would block users unnecessarily.

**Do:**
- Pick the pattern that matches the problem:
  - **Work queue** — competing consumers, single-delivery per message, parallel processing.
  - **Pub/Sub** — broadcast to multiple consumers (alerting, notifications).
  - **Routing** — selective delivery by routing key.
  - **Topics** — wildcard patterns in routing keys (`*`, `#`).
  - **Request-Response** — correlation IDs match request to response.
- Use **manual acknowledgment** for at-least-once delivery; never leave messages unacknowledged (broker memory leaks).
- Set `delivery_mode=PERSISTENT_DELIVERY_MODE` and use **durable queues** to survive broker restart.
- Enable **publisher confirms** to avoid message loss during publishing.
- Use `prefetch_count=1` to distribute work evenly among consumers.
- Encrypt in transit with TLS (separate ports for AMQP vs AMQPS) and authenticate with SASL.
- Use a Correlation ID (CID) for request-response; route mismatched responses to a dead-letter queue.
- Use AsyncAPI to document message schemas; include a `version` field in payload for forward compatibility.
- Cluster brokers for HA; use federation for cross-region.

**Don't:**
- Don't use automatic acknowledgment (`auto_ack=True`) — message is removed from queue immediately, no retry safety.
- Don't trust persistent delivery alone — there's a window where the broker accepted but didn't fsync; use publisher confirms.
- Don't assume exactly-once delivery — it's hard natively; use at-least-once + consumer-side deduplication.
- Don't bind multiple slow consumers to one queue without considering cumulative latency.
- Don't use online message brokers for synchronous payment confirmation — it's slow and doesn't block.

**Code (producer with persistent delivery):**
```python
from pika import BlockingConnection, BasicProperties
from pika.spec import PERSISTENT_DELIVERY_MODE

class RabbitMQProducer:
    queue = "die"
    properties = BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE)

    def publish(self, msg: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=to_json(msg),
            properties=self.properties,
        )
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Messaging" / "Messaging Patterns" / "Trade-Offs"*

---

### Atom / Web Feeds — Decision Heuristics

**Principle:** Use Atom/RSS feeds when content is read by heterogeneous aggregators (feed readers), when syndication matters, or when timely updates to subscribers are needed.

**Do:**
- Use Atom (RFC 4287) over RSS — Atom is a ratified IETF standard with non-breaking extensibility.
- Provide `id`, `title`, `updated` (RFC 3339) as required elements; `link` and `author` recommended.
- Use ETags and Last-Modified headers for efficient polling.
- Use UUIDs for entry IDs to avoid collisions when titles change.
- Use token-based authentication for restricted feeds (basic auth is discouraged).
- Deploy geoblocking, rate limiting, load balancing for DoS resistance.
- Sanitize feed content to prevent RSS feed injection / XSS attacks.

**Don't:**
- Don't use RSS for transactional, real-time updates — feeds are pull-based with polling overhead.
- Don't reinvent auth — use known standards (basic auth, tokens) and document them.
- Don't let web feeds leak sensitive data via logs (IP, user-agent, query parameters).

**Code (Atom feed structure):**
```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>https://example.com/</id>
  <title>Captain's log</title>
  <updated>2024-03-13T08:30:00Z</updated>
  <link rel="self" href="/captainslog"/>
  <entry xml:lang="en">
    <id>https://example.com/captainslog/2024/03/13</id>
    <title>Copenhagen vs Warsaw Mermaid</title>
    <updated>2024-03-13T08:30:00Z</updated>
  </entry>
</feed>
```
*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "Web Feeds" / "Trade-Offs"*

---

### API Security — Layered, Lifecycle-Wide

**Principle:** Security is a force present in all API lifecycle phases; combine encryption, authentication, authorization, input validation, sanitization, and rate limiting.

**Do:**
- Use TLS for all API traffic; consider mTLS for service-to-service auth.
- Apply the principle of least privilege — return only the data the caller needs.
- Sanitize (strip unwanted input) AND validate (enforce constraints) on every input.
- Use serializers / ORM validators for both model and request validation.
- Use UUIDv4 (not sequential integers) for resource identifiers — prevents scraping.
- Provide a `validate_only` flag for testing input handling — must be both idempotent and safe.
- Deny by default (`fail-safe API defaults`); every endpoint must have an authorization check (`complete mediation`).
- Apply zero-trust policy — treat internal APIs as if external.
- Fix security issues at the root cause, with regression tests.

**Don't:**
- Don't trust input data — ever. Validate type, range, format.
- Don't expose excessive data in output — sensitive fields leak without output filtering.
- Don't use `robots.txt` as the only protection against scraping — well-behaved bots only.
- Don't trust the `Origin` header alone in browsers.
- Don't ship secrets in URLs or unencrypted bodies.
- Don't disable security checks that fail too often — fix the underlying issue.

**OWASP API Top 10 categories:** authentication/authorization, inventory management, resource management.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Security" / "OWASP Top 10 API Security" / "Examples of API Security Patterns"*

---

### API Design — Best Practices (the Bloch Maxims)

**Principle:** APIs are among your greatest assets or liabilities; design for the long term.

A network API should be: tailored to the audience, intuitive (navigable without docs), maintainable (evolves without breaking clients), documented, hard to misuse (principle of least surprise), testable, secure, efficient, and communicates errors.

**Do:**
- Tailor the API to client needs — web, mobile, IoT, AI agents each have different patterns.
- Provide comprehensive documentation (reference + tutorial + examples + FAQ).
- Use standard error codes appropriate to the API style (HTTP status for REST, gRPC status codes for gRPC).
- Provide human-readable error messages with context and resolution guidance.
- Follow the principle of least surprise — simple tasks should be straightforward; errors should be hard to make.

*Ref: Learning_API_Styles_-_Lukasz_Dynowski.md — "API Design Best Practices"*

---

## Anti-Patterns & Common Mistakes

- **Big Design Up Front (BDUF):** Spending disproportionate time on design before any feedback. → *Fix:* slice the lifecycle vertically; iterate.
- **Documenting only at maintenance:** Documentation never gets written because software is "never finished." → *Fix:* Draft docs in every phase.
- **Treating security as a deployment concern:** Security must be in the design and planning phases. → *Fix:* Make security a cross-cutting pillar.
- **Hyrum's Law in action:** Documenting "internal" behaviors becomes de-facto contract. → *Fix:* Document *everything* observable; expect users to depend on it.
- **Shadow APIs:** Unmanaged, undocumented APIs deployed without oversight. → *Fix:* API governance, discovery catalogs, gateway enforcement.
- **Zombie APIs:** Abandoned APIs that still run. → *Fix:* Routine scans; sunset policies; HTTP Sunset headers.
- **Excessive data exposure:** APIs leak sensitive fields via verbose responses. → *Fix:* Field-level authorization; serializer output filtering.
- **Offset pagination on dynamic data:** Insertions/deletions cause skipped or duplicated records across pages. → *Fix:* Cursor-based pagination.
- **gRPC auto_ack=True:** Messages removed before consumption is verified. → *Fix:* Use manual acknowledgment; never leave messages un-acked.
- **Broker without publisher confirms:** Messages lost during publishing. → *Fix:* Enable publisher confirms for at-least-once delivery.
- **Webhook without timestamp check:** Replay attacks possible. → *Fix:* Reject requests older than 5 seconds.
- **GraphQL introspection in production:** Schema exposed to attackers. → *Fix:* Disable introspection (but know Clairvoyance can still extract it); require auth.
- **gRPC method-versioned via name suffix (`UpdateOrderV2`):** Less common; version the package/service instead.
- **Soft-delete without versioning:** Adding soft-delete is a breaking change. → *Fix:* Release soft-delete under a new API version.
- **Sequential integer IDs:** Scrapers enumerate `?id=1,2,3,...`. → *Fix:* Use UUIDv4.
- **Treating REST as a single style:** REST has many sub-variants; default to RESTless (Levels 0–2) unless HATEOAS is justified.

---

## Decision Heuristics / Checklists

### Choosing an API Style
- **Cross-platform public CRUD?** → REST.
- **Low-bandwidth mobile/IoT with nested data?** → GraphQL.
- **Service-to-service in microservices with streaming?** → gRPC.
- **Event push from source to N destinations?** → Webhooks (1:1 / 1:N) or Pub/Sub broker (M:N).
- **Bidirectional real-time?** → WebSocket.
- **Asynchronous work distribution with guaranteed delivery?** → Broker (RabbitMQ/Kafka).
- **Content syndication to many readers?** → Atom/RSS feeds.

### Versioning Decisions
- Add fields/endpoints → non-breaking (no version bump).
- Remove field or change type → breaking (MAJOR bump).
- Internal refactor with no contract change → bugfix (PATCH bump).
- Combine strategies? Don't — pick one and stick to it.

### Security Baseline
- TLS everywhere, mTLS for service-to-service.
- UUIDv4 IDs.
- Validate + sanitize all input.
- Rate-limit at the gateway.
- HMAC sign webhook payloads with timestamp check.
- Disable schema introspection in production (GraphQL).
- Fix security issues at root cause, with regression tests.

### Performance Quick Wins
- Enable compression (gzip/Brotli) for text responses.
- Use binary encoding (protobuf/Avro) on performance paths.
- Cache responses (client-side with ETag/Last-Modified; server-side with Redis/memory).
- Set `Cache-Control` headers consistently.
- Profile before optimizing — don't add caching/memory until measured.

### gRPC Service Design
- Start with unary RPCs; reach for streaming only when needed.
- One message per `.proto` method (separate small messages).
- Document most fields/messages precisely.
- Use protovalidate for field validation.
- Pin protoc version in CI; use `buf` for linting and breaking-change detection.

### Broker (RabbitMQ) Service Design
- Manual acknowledgments (`auto_ack=False`); ack only after successful processing.
- `prefetch_count=1` for even workload distribution.
- Durable queues + `PERSISTENT_DELIVERY_MODE` messages.
- Publisher confirms enabled.
- Separate encrypted (AMQPS) and plain (AMQP) ports.
- Dead-letter exchange for failed messages.
- AsyncAPI for documentation.

---

## Key Takeaways

1. **No single API style is best.** Match the style to the problem (CRUD → REST, low-bandwidth → GraphQL, RPC → gRPC, events → Webhooks, real-time → WebSocket, async → broker).
2. **Security is a force across every lifecycle phase**, not a deployment checklist. Apply OWASP API Top 10 categories (auth, inventory, resource management).
3. **Versioning prefers additive changes.** Path-based, header-based, query, or payload — pick one strategy and stick to it.
4. **Schema/IDL-first APIs (OpenAPI, GraphQL SDL, protobuf, AsyncAPI) are testable, generatable, and evolvable.** Keep them as the source of truth.
5. **Cursor-based pagination beats offset-based** for large/dynamic datasets.
6. **gRPC defaults: unary RPCs, manual ack, manual cancellation, deadlines, server reflection only in dev.**
7. **RabbitMQ: manual ack + durable queues + persistent delivery + publisher confirms = at-least-once delivery.**
8. **Webhooks need HMAC + timestamp + payload size limits.** Follow the `standard-webhooks` spec.
9. **Hyrum's Law + Law of Leaky Abstractions = document what you ship, expect users to depend on it.**
10. **The lifecycle is iterative, not sequential.** Security and documentation are cross-cutting; BDUF is anti-pattern.

---

## Cross-References

- Related: [[../Continuous_API_Management.md]] (full lifecycle, governance, product thinking, monetization)
- Related: [[../Mastering_Api_Architecture.md]]
- Related: [[../Restful_Web_API_Patterns_and_Practices.md]]
- Topic index: [[../INDEX.md]]