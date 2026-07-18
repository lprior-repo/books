# RESTful Web API Patterns and Practices Cookbook
**Author:** Mike Amundsen
**Topic tags:** `#api` `#architecture` `#testing`
**Language focus:** Language-agnostic (HTML, Collection+JSON, SIREN, HAL, JSON, ALPS; JavaScript/Node.js examples for client/service)
**Sources:** `markdown_output/Restful Web API Patterns and Practices Cookbook/Restful Web API Patterns and Practices Cookbook.md` · `summaries/Restful_Web_API_Patterns_and_Practices_Cookbook.md`

## TL;DR
A cookbook of 70+ recipes for designing RESTful hypermedia APIs that machines built by strangers can use reliably over decades. The guiding principle — *"Leverage global reach to solve problems you haven't thought of, for people you have never met"* — is operationalized through four separable layers: **protocol (HTTP) · message format (registered media types) · vocabulary (property names) · actions (hypermedia controls resolved at runtime)**. Where *Mastering API Architecture* tells you *how to choose and operate* an API platform, this book tells you *how to design messages and interactions* so that platform decisions remain reversible. Apply when you need the day-to-day design rules for hypermedia, idempotency, content negotiation, caching, RFC 7807 errors, or evolvable data models.

---

## Best Practices by Topic

### Separation of Layers (Protocol · Format · Vocabulary · Actions)
`#api` `#architecture`

**Principle:** Keep the four communication layers independent — change one without breaking the others.

**Do:**
- Use HTTP as the protocol contract (methods, status codes, headers).
- Use a *registered structured media type* (HTML, Collection+JSON, SIREN, HAL) as the message contract.
- Pull property names from published vocabularies (Schema.org, Microformats, Dublin Core, FHIR, ACORD, PSD2).
- Express available actions only via runtime hypermedia controls (links + forms).
- Implement an anti-corruption layer that translates between internal models and the published external vocabulary.

**Don't:**
- Embed internal object/data models directly into messages.
- Mix vocabulary terms with media-type structural elements (e.g., putting `person` as a JSON key rather than a rel).

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Establishing a Foundation with Hypermedia Designs" / "The Power of Vocabularies"*

---

### Registered Media Types (Recipe 3.1)
`#api`

**Principle:** Adopt one or more open, IANA-registered media types so clients can bind to the format without understanding the content.

**Do:**
- Default to **HTML** — 30+ year track record, universal browser support, vast tooling, great for testing.
- Document every media type your service supports; allow consumers to discover and express preferences.
- Prefer media types that (a) support hypermedia natively and (b) support custom extension.

**Don't:**
- Author your own media type unless your audience is small (single company), huge (Google/Facebook/Amazon), or you lead a vertical (FHIR-style).
- Commit to unstructured JSON/XML alone — no stable structure to bind to.

*Ref: Cookbook.md — "Recipe 3.1: Creating Interoperability with Registered Media Types"*

---

### Structured Media Types & Well-Formedness vs. Validity (Recipe 3.2)
`#api`

**Principle:** Separate message *well-formedness* (compliance with format rules) from *validity* (compliance with content rules) so messages stay well-formed when content evolves.

**Do:**
- Use SMTs whose structure is invariant (e.g., HTML `<ul>/<li>`, Collection+JSON `items/data[]`).
- Two-phase client parsing: validate structure first, then extract data — unknown properties never crash the client.

**Don't:**
- Use plain JSON and assume the schema won't drift — adding a property changes the JSON *structure*.

**Code (structure invariant under content change):**
```html
<ul name="Person">
 <li name="givenName">Marti</li>
 <li name="familyName">Contardi</li>
 <!-- adding <li name="emailAddress">…</li> does NOT change the structure -->
</ul>
```
Contrast with JSON, where adding `emailAddress` changes the structural schema.
*Ref: Cookbook.md — "Recipe 3.2: Ensuring Future Compatibility with Structured Media Types"*

---

### Published Vocabularies (Recipe 3.3)
`#api`

**Principle:** Use well-known property names from published vocabularies so strangers understand your messages.

**Do:**
- Pull from Schema.org (general), Microformats.org, Dublin Core, or industry vocabs (PSD2 payments, FHIR health, ACORD insurance).
- Publish your own vocabulary document listing every "magic string" (id/name/rel values) your service emits, with definitions and source URLs.
- Keep vocabulary terms disconnected from any software/hardware dependencies.

**Don't:**
- Use proprietary internal names that require NDA'd docs.

*Ref: Cookbook.md — "Recipe 3.3: Sharing Domain Specifics via Published Vocabularies" / "Richardson's Magic Strings"*

---

### Semantic Profiles & ALPS (Recipe 3.4)
`#api`

**Principle:** Publish a Semantic Profile Document (SPD) covering all three information-architecture pillars — ontology (properties), taxonomy (object groupings), choreography (actions/state transitions). SPDs describe the *problem space*, not the implementation.

**Do:**
- Use **ALPS** (Application-Level Profile Semantics) — simple, JSON/XML/YAML, maps cleanly to the three pillars.
- Tag each descriptor: `ontology`, `taxonomy`, or `choreography`.
- Type each action: `safe` (read-only), `unsafe` (non-idempotent write), `idempotent` (repeatable write) — plus `rt` (return type).
- Advertise the profile via `Link: <…>; rel="profile"` in every response.
- Make profiles broadly reusable; prefer general over specific.

**Don't:**
- Put URLs/HTTP methods/protocol details in an SPD — those belong in OpenAPI/AsyncAPI.
- Make breaking changes to a published profile — version it at a new URI (`/profiles/personV2`).
- Confuse SPDs with API definitions (OpenAPI, WSDL, AsyncAPI).

**Code (ALPS person profile):**
```json
{ "$schema": "https://alps-io.github.io/schemas/alps.json",
 "alps" : {
 "title": "Person Semantic Profile Document",
 "descriptor": [
   {"id": "givenName", "def": "https://schema.org/givenName", "tag": "ontology"},
   {"id": "familyName", "def": "https://schema.org/familyName", "tag": "ontology"},
   {"id": "Person", "tag": "taxonomy",
    "descriptor": [
      {"href": "#givenName"}, {"href": "#familyName"}
    ]},
   {"id": "goHome",    "type": "safe",       "tag": "choreography", "rt": "#Home"},
   {"id": "goList",    "type": "safe",       "tag": "choreography", "rt": "#List"},
   {"id": "doCreate",  "type": "unsafe",     "tag": "choreography", "rt": "#Item"},
   {"id": "doUpdate",  "type": "idempotent", "tag": "choreography", "rt": "#Item"},
   {"id": "doRemove",  "type": "idempotent", "tag": "choreography", "rt": "#Item"}
 ]}}
```
*Ref: Cookbook.md — "Recipe 3.4: Describing Problem Spaces with Semantic Profiles"*

---

### Embedded Hypermedia Controls (Recipe 3.5)
`#api`

**Principle:** Express every available action via runtime links/forms so clients never hardcode URLs, methods, or input shapes.

**Do:**
- Forms carry URL, method, content type, and typed input fields — clients read them at runtime.
- Use context-dependent forms (e.g., admin sees 5 fields, anonymous sees 3).
- Service-location changes become non-breaking (extreme late binding).

**Don't:**
- Hardcode action URLs in client code.

**Code (HTML form with validation constraints):**
```html
<form name="doCreate" action="http://api.example.org/person/"
    method="post" enctype="application/x-www-form-urlencoded">
 <fieldset>
   <hidden name="identifier" value="q1w2e3r4" />
   <input name="givenName" placeholder="givenName" required/>
   <input name="familyName" placeholder="familyName" required/>
   <input name="telephone" placeholder="telephone" pattern="[0-9]{10}"/>
   <input type="submit" />
 </fieldset>
</form>
```
**Code (Collection+JSON template):**
```json
{ "collection" : {
 "template" : {
   "data" : [
     {"name" : "identifier", "value": "q1w2e3r4"},
     {"name" : "givenName", "value" : "", "required":true},
     {"name" : "familyName", "value" : "", "required":true},
     {"name" : "telephone", "value" : "", "regex":"[0-9]{10}"}
   ]}}}
```
*Ref: Cookbook.md — "Recipe 3.5: Expressing Actions at Runtime with Embedded Hypermedia"*

---

### Idempotent Writes — PUT-Create (Recipes 3.6, 5.15)
`#api`

**Principle:** Use **HTTP PUT (not POST)** for all writes — PUT is idempotent by design and solves the *lost-response problem* ("did my POST succeed?").

**Do:**
- **PUT-Create**: `PUT /person/{client-supplied-id}` with `If-None-Match: *` → server creates if absent (201) or returns 409 Conflict if it exists.
- **PUT-Update**: `PUT /person/{id}` with `If-Match: "{current-ETag}"` → server replaces only if the ETag matches; otherwise 412 Precondition Failed.
- Clients supply their own IDs (UUIDs) → enables offline operation, reliable retries, throughput.
- Bake `createResource()` / `updateResource()` cover methods into client/server libraries.
- If you must POST, add an Idempotency-Key header (IETF draft).

**Don't:**
- Use POST for writes when network reliability matters — POST is not safely repeatable.
- Use increments ("add 5%") in update bodies — use replacement values with validators ("if current=100, set to 105").

**Code (PUT-Create):**
```http
**** REQUEST
PUT /person/q1w2e3 HTTP/2.0
Host: api.example.org
Content-Type: application/x-www-form-urlencoded
If-None-Match: *
givenName=Mace&familyName=Morris
**** RESPONSE
HTTP/2.0 201 CREATED
Content-Type: application/vnd.collection+json
ETag: "p0o9i8u7y6t5r4e3w2q1"
```
**Code (PUT-Update with optimistic locking):**
```http
**** REQUEST
PUT /person/q1w2e3 HTTP/2.0
Host: api.example.org
Content-Type: application/x-www-form-urlencoded
If-Match: "p0o9i8u7y6t5r4e3w2q1"
givenName=Mace&familyName=Morris
**** RESPONSE
HTTP/2.0 200 OK
Content-Type: application/vnd.collection+json
ETag: "o9i8u7y6t5r4e3w2q1p0"
```
*Ref: Cookbook.md — "Recipe 3.6: Designing Consistent Data Writes with Idempotent Actions" / "Recipe 5.15: Improving Reliability with Idempotent Create"*

---

### Repeatable & Reversible Actions (Recipes 3.8, 3.9)
`#api`

**Principle:** Design writes to be safely repeatable (network + operation idempotence) and reversible (rollback/undo).

**Do:**
- **Network idempotence**: prefer PUT/GET/DELETE over POST.
- **Operation idempotence**: bodies carry `productId, currentPrice, newPrice` (validators) so partial-failure retries are safe.
- **Reversibility option 1**: re-PUT previous values (assumes no concurrent modification — combine with `If-Match`).
- **Reversibility option 2**: special actions like `undoDelete` that restore via PUT + ETag.
- For DELETE, save the resource so it can be restored (HTTP has no UNDELETE).

**Code (replacement-value update body — safely repeatable):**
```http
PUT /catalog/priceUpdate HTTP/1.1
Content-Type: text/csv
....
productId, currentPrice,newPrice
q1w2e3, 100,105
t5y6u7, 200,210
i8o9p0, 250,265
```
*Ref: Cookbook.md — "Recipe 3.8: Designing for Repeatable Actions" / "Recipe 3.9: Designing for Reversible Actions"*

---

### Extensible Messages & "Don't Change It, Add It" (Recipe 3.10)
`#api`

**Principle:** Evolve messages without breaking existing consumers by *adding*, never *removing or redefining*.

**Do:**
- Bake a name-value-pair (NVP) collection into the initial design: `{"name":"…","value":…}`.
- Add parallel properties alongside old ones (`givenName` + `familyName` while keeping `name`).
- Use a root wrapper (`{"message":{...}}`) to host multiple output format versions.

**Don't:**
- Strip or rename existing fields.

**Code (NVP extension pattern):**
```json
{
 "name": "Merk Muffly",
 "region": "southwest",
 "age": 21,
 "nvp" : [
   {"hatsize" : "3"},
   {"phoneNumbers": ["123-456-7890","980-657-3421"]},
   {"address": {"street":"...","city":"...","state":"...","zip":"..."}}
 ]
}
```
*Ref: Cookbook.md — "Recipe 3.10: Designing for Extensible Messages"*

---

### Modifiable Interfaces — Three Rules (Recipe 3.11)
`#api`

**Principle:** Once published, every URL, property, and method is a promise. Three rules: **(1) Take nothing away. (2) Don't redefine things. (3) Make additions optional.**

**Do:**
- New optional inputs must have sensible defaults.
- For breaking changes, **fork** the interface — run old and new in parallel until migration completes.
- Honor Hyrum's Law: with enough users, every observable behavior will be depended on.

**Don't:**
- Redefine `?size` from "page size" to "hat size" — that's a removal in disguise.
- Make new arguments required on existing forms; define a *new* form instead.

**Code (add optional input with default):**
```html
<!-- updated search form — region is optional, defaults to "all" -->
<form action="..." method="GET" name="findUsers">
 <input name="givenName" value="" required="true" />
 <input name="familyName" value="" required="true" />
 <input name="regions" value="all" required="false" />
 <input type="submit" />
</form>
```
*Ref: Cookbook.md — "Recipe 3.11: Designing for Modifiable Interfaces"*

---

### Hypermedia Clients — Limit Hardcoded URLs (Recipes 4.1, 4.9)
`#api` `#testing`

**Principle:** Client applications should hardcode **exactly one URL** — the service's stable home/entry point. Everything else is discovered at runtime via links/forms.

**Do:**
- Treat the entry-point URL as the single promise; cache and reuse discovered URLs locally.
- Find elements by `id`, `name`, `rel`, or `tag` identifiers (Recipe 4.8).
- Code clients to be HTTP-aware: honor cache headers, content negotiation, conditional requests.

**Don't:**
- Hardcode multiple endpoint paths — couples the client to URL structure.

*Ref: Cookbook.md — "Recipe 4.1: Limiting the Use of Hardcoded URLs" / "Recipe 4.8" / "Recipe 4.9"*

---

### Message-Centric Clients & "Must Ignore" (Recipes 4.3, 6.8)
`#api` `#testing`

**Principle:** Clients parse message *structure* first (well-formedness), then extract known data and **silently ignore the rest** (Postel's Law / Robustness Principle).

**Do:**
- Two-phase processing: structural validation → data extraction.
- When passing records through to another service, exchange the *complete* record — never strip fields you don't understand.
- Forward the original `ETag` / `If-Match` through pass-through proxies.

**Don't:**
- Reject messages with unknown fields.
- Strip data on read — you may corrupt integrity when writing back.

*Ref: Cookbook.md — "Recipe 4.3: Coding Resilient Clients" / "Recipe 6.8: Ignoring Unknown Data Fields"*

---

### Stable Entry-Point URL (Recipe 5.1)
`#api`

**Principle:** Every service promises **at least one stable URL** (typically `rel="home"`); all other URLs may move.

**Do:**
- Emit the home URL as a `Link` header in *every* response.
- When the service moves, honor the old URL with `301 Moved Permanently` + `Location`.
- Optionally register a well-known URL (RFC 8615, RFC 7595).

**Code (Link header for stable home):**
```http
**** REQUEST
GET / HTTP/1.1
Host: api.example.org
**** RESPONSE
HTTP/1.1 200 OK
Content-Type: application/vnd.collection+json
ETag: "p0o9i8u7y6t5r4e3w2q1"
Link: <http://api.example.org/home>; rel="home"
```
**Code (relocation via 301):**
```http
**** RESPONSE
HTTP/1.1 301 Moved Permanently
Location: http://new.example.org/home
```
*Ref: Cookbook.md — "Recipe 5.1: Publishing at Least One Stable URL"*

---

### Hide Internal Models (Recipe 5.2)
`#api`

**Principle:** The API is an independent design effort — your data model is not your object model is not your resource model is not your message model.

**Do:**
- Treat the interface as its own design — not a serialization of internal objects.
- Model API properties as a single flat collection when possible (denormalized externally; normalized internally).
- Services can use any storage model internally; the external contract is stable.

**Don't:**
- Expose ORM/ActiveRecord models directly (mass-assignment risk + tight coupling).

*Ref: Cookbook.md — "Recipe 5.2: Preventing Internal Model Leaks"*

---

### Content Negotiation (Recipe 5.6)
`#api`

**Principle:** Support multiple representation formats and pick one at runtime via the `Accept` header (proactive/server-driven) or `300 Multiple Choices` (reactive/agent-driven).

**Do:**
- **Proactive (PCN)** is the default — client sends `Accept`, server picks.
- Support `q` values for preference weighting: `application/vnd.hal+json;q=0.8, application/json;q=0.4`.
- Document supported formats; advertise via Recipe 5.5 (Prefer).
- Return `406 Not Acceptable` when no format matches.

**Don't:**
- Use reactive negotiation for M2M unless both parties pre-arrange details.
- Dedicate URL spaces per format unless necessary (more URLs to maintain).

**Code (proactive with q values):**
```http
**** REQUEST ****
GET /list HTTP/1.1
Accept: application/vnd.siren+json, application/vnd.hal+json, application/json
**** RESPONSE ****
200 OK HTTP/1.1
Content-Type: application/json
```
**Code (reactive — 300 Multiple Choices):**
```http
**** RESPONSE ****
HTTP/1.1 300 Multiple Choices
Link: <http://api.example.org/html/search>;rel="alternate html"
Link: <http://api.example.org/api/search>;rel="alternate api"
Location: http://api.example.org/html/search
```
*Ref: Cookbook.md — "Recipe 5.6: Supporting HTTP Content Negotiation"*

---

### Service Health Monitoring (Recipe 5.11)
`#api`

**Principle:** Expose a health-check endpoint using the draft "Health Check Response Format for HTTP APIs" (`application/health+json`).

**Do:**
- Expose `/health` returning `status` (pass/fail/warn), `version`, `releaseId`, `serviceId`, `checks` (downstream dependency detail).
- Always include `Cache-Control` + `ETag` so frequent polling doesn't DOS your own service.
- Advertise via `Link: <…>; rel="health-check"` in `OPTIONS` and service-meta responses.
- Reflect *interface* health, not internal debugging state.

**Don't:**
- Set up callback/subscription endpoints for health — polling with cache directives scales better.

**Code (health response):**
```http
HTTP/1.1 200 OK
Content-Type: application/health+json
Cache-Control: max-age=3600
ETag: "w\i8u7y6t5r4e3w2"
{
 "status": "pass",
 "version": "1",
 "releaseId": "1.2.2",
 "serviceId": "f03e522f-1f44-4062-9b55-9587f91c9c41",
 "description": "health of authz service",
 "checks": {
   "cassandra:responseTime": [
     {"componentId": "dfd6cf2b-...",
      "componentType": "datastore",
      "observedValue": 250,
      "observedUnit": "ms",
      "status": "pass",
      "affectedEndpoints": ["/users/{userId}", "/shopping/{anything}"],
      "time": "2018-01-17T03:36:48Z"}]
 }
}
```
*Ref: Cookbook.md — "Recipe 5.11: Supporting Service Health Monitoring"*

---

### Standardized Error Reporting — RFC 7807 (Recipe 5.12)
`#api`

**Principle:** Treat errors as alternate responses, not failures. Use **RFC 7807 Problem Details** (`application/problem+json`) so clients recognize and resolve errors consistently.

**Do:**
- Always include: `type` (URI to human-readable problem def), `title` (short summary), `status` (HTTP code as number), `detail` (specific explanation), `instance` (this occurrence URI).
- Default `type` is `about:blank`; point `type` to a semantic profile for the error.
- Extend with custom properties (`balance`, `accounts`, …) documented at the `type` URI.
- Optionally add `Retry-After` for retryable errors.

**Don't:**
- Use Problem Details when a plain 4xx/5xx status suffices (e.g., simple 403 on a forbidden PUT).
- Return debugging/internal details via this format — it's for *interface* errors.

**Code (basic Problem Details):**
```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
Content-Language: en
{
 "type": "https://example.com/probs/out-of-credit",
 "title": "You do not have enough credit.",
 "detail": "Your current balance is 30, but that costs 50.",
 "instance": "/account/12345/msgs/abc",
 "status": 403
}
```
**Code (extended Problem Details with custom props):**
```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
{
 "type": "https://example.com/probs/out-of-credit",
 "title": "You do not have enough credit.",
 "detail": "Your current balance is 30, but that costs 50.",
 "instance": "/account/12345/msgs/abc",
 "status": 403,
 "balance": 30,
 "accounts": ["/account/12345", "/account/67890"]
}
```
*Ref: Cookbook.md — "Recipe 5.12: Standardizing Error Reporting"*

---

### Runtime Service Registry (Recipe 5.13)
`#api` `#architecture`

**Principle:** Services self-register at startup, ping health periodically, and unregister on shutdown — enabling runtime "find and bind" by capability.

**Do:**
- Self-register on startup with: `serviceURL`, `serviceName`, `semanticProfile` URIs, `mediaType` list, `apiDefinitions` links, `tags`.
- Send periodic keep-alive pings (with optional usage stats).
- Unregister on graceful shutdown (`SIGTERM`); RSR evicts stale entries after max-ping window.
- These actions are *internal* — not part of the public API surface.

**Code (Node.js self-registration):**
```javascript
var srsResponse = null;
var srsRegister({Url:"...","name":"...", .....});
discovery.register(srsRegister, function(data, response) {
 srsResponse = JSON.parse(data);
 initiateKeepAlive(srsResponse.href, srsResponse.milliseconds);
 http.createServer(uuidGenerator).listen(port);
});
```
**Code (graceful unregister with force-timeout):**
```javascript
process.on('SIGTERM', function () {
 discovery.unregister(null, function(response) {
   try {
     uuidGenerator.close(function() { process.exit(0); });
   } catch(e){}
 });
 setTimeout(function() { process.exit(1); }, 10000);
});
```
*Ref: Cookbook.md — "Recipe 5.13: Improving Service Discoverability with a Runtime Service Registry"*

---

### Runtime Fallbacks for Dependent Services (Recipe 5.16)
`#api` `#architecture`

**Principle:** Assume dependencies will fail — implement mitigations in this order: automatic retry → static fallback → dynamic fallback (RSR lookup) → queue for replay → give up.

**Do:**
- Retry only safe/idempotent methods (GET, HEAD, PUT, DELETE); never auto-retry POST/PATCH.
- Use exponential backoff with a max retry count (typically 3).
- For queuing, return `202 Accepted` + status URL (Recipe 7.15).
- Implement mitigations *locally* — turning them into external services makes them fatal dependencies too.
- Best candidate status codes for retry/fallback: 500, 502, 503, 504, 408.

**Don't:**
- Retry non-idempotent methods without an idempotency key.

**Code (parameterized retry/fallback request):**
```javascript
var reqParams = {}
reqParam.host = "https:/api.example.com"
reqParams.url = "/users/q1w2e3";
reqParams.body = "mork=mamund&name=Mike Morkelsen";
reqParams.method = "PUT";
reqParams.waitMS = 300;
reqParams.retryAttempts = 3;
reqParams.successFunction = requestSucceeded;
reqParams.failFunction = requestFailed;
reqParams.alternateHost = "https://alternate-api.example.com";
reqParams.queuingFunction = queueRequest;
httpLib.request(reqParams);
```
*Ref: Cookbook.md — "Recipe 5.16: Providing Runtime Fallbacks for Dependent Services"*

---

### Semantic Proxies for Noncompliant Services (Recipe 5.17)
`#api` `#architecture`

**Principle:** Wrap non-hypermedia/third-party services in a compliant proxy rather than rewriting them.

Three proxy types:
- **Enterprise-Level Proxy (ELP)** — algorithmic translation of a related-service family.
- **Custom One-Off Proxy (COP)** — single-service wrapper (e.g., RESTful facade over FTP upload).
- **Semantic Profile Proxy (SPP)** — vocabulary/media-type normalization (e.g., CSV → SIREN, XML → Collection+JSON).

**Do:**
- Each proxy needs its own semantic profile, API definition document, and action implementations.
- Use sparingly — proxies add latency and failure points.

**Code (COP wrapping FTP upload as HTTP/HTML):**
```javascript
function httpUpload(file) {
 var uploader = new httpService();
 return uploader.read();
}
function ftpUpload(file) {
 var client = new ftpService();
 return client.put(file);
}
function proxyUpload(file) {
 var results = null;
 var f = httpUpload(file);
 if(f) { results = ftpUpload(f); }
 return results;
}
```
*Ref: Cookbook.md — "Recipe 5.17: Using Semantic Proxies to Access Noncompliant Services"*

---

### Hiding Data Storage Internals (Recipes 6.1, 6.3)
`#api`

**Principle:** Never leak storage technology, schema, or relationships through the API.

**Do:**
- Express queries via domain vocabulary (`?active=true`), not SQL (`?filter=status='active'`).
- Express relationships via hypermedia links (`rel="customer"`), not foreign keys (`customerId: 123`).
- Each service owns its own data storage; services interact via messages, not shared DBs.

*Ref: Cookbook.md — "Recipe 6.1: Hiding Your Data Storage Internals" / "Recipe 6.3: Hiding Data Relationships"*

---

### URL-Based "Contains" and "AND" Queries (Recipe 6.4)
`#api`

**Principle:** Use URL paths + query strings for common query patterns — they're intuitive, cacheable, and storage-agnostic.

**Do:**
- AND queries via query string: `/customers?region=east&status=active`.
- Containment queries via path segments: `/customers/east/active`.

*Ref: Cookbook.md — "Recipe 6.4: Leveraging HTTP URLs to Support 'Contains' and 'AND' Queries"*

---

### Query Response Metadata (Recipe 6.5)
`#api`

**Principle:** Return metadata *alongside* results so clients can evaluate quality and tune queries.

**Do** (return some/all of): `q-status`, `q-sent`, `q-executed`, `q-returned`, `q-count`, `q-seconds`, `q-datetime`, `q-score`, `q-source`, `q-suggest`, `q-location` (replay URL).
- Carry via headers, body, or a separate linked `query-metadata` resource.
- Communicate truncation explicitly (`q-status=truncated`).

**Don't:**
- Leak `q-executed` (raw SQL/internal query) or `q-source` carelessly — security/coupling risk.

**Code (metadata in body via Collection+JSON):**
```json
{"collection": {
 "title": "Person",
 "metadata" : [
   {"name": "q-sent", "value": "?id=q1"},
   {"name": "q-datetime", "value": "2024-12-12:00:12:0012TZ"},
   {"name": "q-status", "value": "result set too large, query canceled"},
   {"name": "q-seconds", "value": "120"},
   {"name": "q-count", "value": "10000+"},
   {"name": "q-suggest", "value": "reduce return set with additional query parameters"}
 ]}}
```
*Ref: Cookbook.md — "Recipe 6.5: Returning Metadata for Query Responses"*

---

### HTTP 200 vs 4xx for Empty Results (Recipe 6.6)
`#api`

**Principle:** An empty collection from a valid query is **200 OK**, not 4xx.

**Decision table:**
- **200 OK** — well-formed collection query returns empty set.
- **404 Not Found** — single-resource URL (`/persons/q1w2e3`) doesn't exist.
- **400 Bad Request** — malformed query / unknown property (`?hatsize=13` when no such field).
- **5xx** — valid query, server/data store can't fulfill (timeout, unreachable).

**Don't:**
- Echo a downstream 404-as-empty-collection verbatim — normalize to 200 OK at your interface.

**Code (200 + empty collection + metadata):**
```http
**** REQUEST ****
GET /persons/?status=pending HTTP/1.1
Accept: application/vnd.collection+json
**** RESPONSE ***
HTTP/1.1 200 OK
Content-Type: application/vnd.collection+json
{"collection": {
 "metadata": [
   {"name": "q-status", "value": "success"},
   {"name": "q-count", "value": "0"}],
 "items": []
}}
```
*Ref: Cookbook.md — "Recipe 6.6: Returning HTTP 200 Versus HTTP 400 for Data-Centric Queries"*

---

### Caching Directives (Recipe 6.9)
`#api` `#architecture`

**Principle:** Mark every response with caching metadata so consumers/proxies/CDNs can reduce latency and load.

**Provider directives:**
- `Cache-Control: public, max-age=600` — cacheable by any proxy for 10 min.
- `Cache-Control: private, max-age=300, must-revalidate, stale-if-error` + `ETag` — conditional requests via `If-None-Match` / `If-Match`.
- `immutable` (RFC 8246) for long-lived static content.
- Use `Vary: Authorization` (etc.) to prevent wrong cached representation replay.

**Consumer directives:**
- `max-age=600, min-fresh=300` — accept response ≤10 min old with ≥5 min freshness left.
- `no-cache` — force fresh copy (use sparingly; only when editing).
- `max-stale, stale-if-error` — accept stale copy for reads when fresh unavailable.

**Do:**
- Match cache lifetime to data volatility (static lists: days; shopping cart: seconds).
- Always include `ETag` to enable conditional requests and optimistic locking.

**Code (provider response with conditional-request caching):**
```http
GET /user/q1w2e3r4 HTTP/1.1
**** RESPONSE ****
HTTP/1.1 200 OK
Content-Type: application/vnd.siren+json
ETag: "w/p0o9i8u7y6t5"
Cache-Control: public, max-age=300, must-revalidate, stale-if-error
```
*Ref: Cookbook.md — "Recipe 6.9: Improving Performance with Caching Directives"*

---

### Modifying Data Models in Production (Recipe 6.10)
`#api`

**Principle:** Design data storage for change from day one via a **two-tier explicit + implicit (NVP) model**.

**Do:**
- Explicit strongly-typed fields for known properties + an `nvp: [{name, value}]` array for future ones.
- New properties land in `nvp` first; no schema migration needed for consumers.
- If a release backs out, the NVP data is retained — no loss.
- Provide a single-access `find({name, message})` function that checks both tiers.

**Don't:**
- Set `additionalProperties: false` on schemas *and* require strict rollouts.

**Code (two-tier model with NVP):**
```json
{
 "givenName": "John",
 "familyName": "Doe",
 "age": 23,
 "nvp" : [
   {"name" : "middleName", "value" : "Seymore"},
   {"name" : "nicknames", "value" : ["J","JJ","Johnboy","Jack"]},
   {"name" : "address", "value": {"street":"123 main","city":"Byteville","state":"MD","zip":"12345"}}
 ]
}
```
**Code (single-access function — JavaScript):**
```javascript
function find(args) {
 var a = args || {};
 var n = a.name || "";
 var m = (a.message || local.m) || {};
 var p = (a.nameValuePair || local.p) || "nvp";
 var r = undefined;
 if(m==={} || n==="") { r=undefined; }
 else {
   if(m.hasOwnProperty(n)) { r=m[n]; }
   else if(m.hasOwnProperty(p)) {
     try { r = m[p].filter(function(i) {return i.name===n})[0].value; }
     catch { r = undefined; }
   }
 }
 return r;
}
```
*Ref: Cookbook.md — "Recipe 6.10: Modifying Data Models in Production"*

---

### Limiting Large-Scale Responses (Recipe 6.12)
`#api`

**Principle:** Always enforce a default maximum record count; communicate limits via query metadata.

**Do:**
- **Direct limit**: pass engine-native directive (`$top=100`, `first:100`, `LIMIT 100`, `rows=100`).
- **Truncated limit**: service code slices the result collection (use when engine lacks native limits).
- Always validate/override client-supplied limits (reject `?limit=1000000`).
- Distinguish **query limits** from **page sizes** (Recipe 7.11).

**Code (truncation in service code):**
```javascript
function executeQuery(dataStoreAddress, dataQuery) {
 var ix=0, maxLimit=100;
 var responseCollection = [];
 var dataCollection = httpRequest(dataStoreAddress, dataQuery);
 for (let item of dataCollection) {
   if(ix>maxLimit) { break; }
   responseCollection.push(item);
   ix++;
 });
 return responseCollection;
}
```
*Ref: Cookbook.md — "Recipe 6.12: Limiting Large-Scale Responses"*

---

### Workflow-Compliant Services (Recipe 7.1)
`#api` `#architecture`

**Principle:** Every service enlisted in a workflow must support a composable 4-action interface: **Execute · Repeat · Revert · Cancel**. Jobs (collections of tasks) add **Continue · Restart · Cancel**.

**Do:**
- Make each action a hypermedia affordance with stable semantics.
- Share state as strongly-typed *documents* (Recipe 7.2), never shared data models or shared DBs.
- State transfer modes: by value (inline forms), by value (import/export ops), or by reference (shared URL).

**Code (ALPS for shopping cart import/export):**
```json
{
 "$schema": "https://alps-io.github.io/schemas/alps.json",
 "alps": {
   "version": "1.0",
   "title": "Simple Shopping Cart",
   "descriptor": [
     {"id": "doCartImport", "type": "idempotent", "rt": "#cartCollection",
      "tag": "choreography",
      "descriptor": [{"href": "#cartCollection"}]},
     {"id": "doCartExport", "type": "idempotent", "rt": "cartCollection",
      "tag": "choreography"}
   ]
 }
}
```
*Ref: Cookbook.md — "Recipe 7.1: Designing Workflow-Compliant Services" / "Recipe 7.2: Supporting Shared State for Workflows"*

---

### Async / Delayed Responses — 202 Accepted (Recipe 7.15)
`#api`

**Principle:** For long-running work, return `202 Accepted` immediately with a status document the client can poll.

**Do:**
- Initial response carries: `identifier`, `acceptedURL`, `completedURL`, `failedURL`, `description`, `refresh` (ms), `percentCompleted`, `status`, `dateCreated`, `dateUpdated`, `dateEstimated`.
- Actions: `goAccepted` (safe), `doCancel` (DELETE, idempotent), `goCompleted`/`goFailed`/`goHome` (safe).
- Emit `Link: <…>; rel=self; refresh=60000` and `Link: <…>; rel=cancel` headers.
- Support `maxTTL` — auto-cancel work exceeding the limit.
- Document ahead-of-time which actions may return 202 so clients are prepared.

**Don't:**
- Stuff transient metadata (percentCompleted, dateUpdated) in headers — it breaks caching.

**Code (initial 202 response):**
```http
**** REQUEST
PUT /services/compute-results HTTP/1.1
Content-Type: application/vnd.collection+json
**** RESPONSE
202 Accepted HTTP/1.1
Content-Type: application/vnd.collection+json
Link: <http://api.example.org/services/compute-results/q1w2e3>;rel=self; refresh=60000
Link: <http://api.example.org/services/cancel-form/q1w2e3>;rel=cancel
{"collection": {
 "items": [{
   "data": [
     {"name":"identifier", "value":"q1w2e3"},
     {"name":"refresh", "value":"60000"},
     {"name":"percentCompleted", "value":"10"},
     {"name":"status", "value":"working"},
     {"name":"dateEstimated", "value":"2024-02-01:22:15:00"}
   ]}]}}
```
*Ref: Cookbook.md — "Recipe 7.15: Synchronous Reply for Incomplete Work with 202 Accepted"*

---

### Automatic Retries with Exponential Backoff (Recipe 7.16)
`#api` `#architecture`

**Principle:** For transient failures, retry idempotent requests with exponential backoff — capped at ~3 attempts.

**Do:**
- Exponential backoff (EBO): wait 2s → 4s → 16s; max 3 retries.
- Add jitter to prevent thundering-herd.
- Only retry idempotent methods (GET, HEAD, PUT, DELETE) automatically.
- Inspect status: 4xx = don't retry (client error); 5xx or connection loss = retry candidate.

**Don't:**
- Retry POST/PATCH without an idempotency key.

*Ref: Cookbook.md — "Recipe 7.16: Short-Term Fixes with Automatic Retries"*

---

### Local Undo / Rollback (Recipe 7.17) & Calling for Help (Recipe 7.18)
`#api`

**Principle:** Each service supports local undo; when automation fails, escalate to a human.

**Do:**
- Maintain enough history (snapshots/event logs) to support `undoDelete` and similar.
- For multi-service workflows, each service implements its own Revert; the coordinator orchestrates.
- "Call for help" = create a support ticket / pause workflow / capture full context (job state, error, task history) for human review.

*Ref: Cookbook.md — "Recipe 7.17: Supporting Local Undo or Rollback" / "Recipe 7.18: Calling for Help"*

---

### Standard List Navigation / Pagination (Recipe 7.11)
`#api`

**Principle:** Expose a fixed set of navigation affordances on every list resource: `list`, `first`, `previous`, `next`, `last`, `select`, `exit`, `home`.

**Do:**
- Omit `previous` on the first page and `next` on the last page (affordance visibility = state).
- Use opaque href values — no need for human-readable `page1`/`page2`.
- Use `rel="exit"` for confirmation/cleanup when leaving a costly list.

**Code (Collection+JSON list with navigation links):**
```json
{"collection" : {
 "title" : "Customer List",
 "links" : [
   {"rel" : "self list collection", "href" : "/customers/list"},
   {"rel" : "home", "href" : "/customers/"},
   {"rel" : "first", "href" : "/customers/list/q1w2"},
   {"rel" : "next", "href" : "/customers/list/t5y6"},
   {"rel" : "exit", "href" : "/customers/p0o9"}
 ]}}
```
*Ref: Cookbook.md — "Recipe 7.11: Enabling Standard List Navigation"*

---

## Anti-Patterns & Common Mistakes

- **Exposing internal data/object models directly** → *fix:* design the API as its own artifact; use anti-corruption layer (Recipe 5.2).
- **Using POST for all writes** → *fix:* PUT-Create with `If-None-Match: *` (Recipes 3.6, 5.15).
- **Returning a 4xx for an empty valid query** → *fix:* 200 OK + empty collection + metadata (Recipe 6.6).
- **Plain JSON as the only format** → *fix:* adopt a structured media type so structure ≠ content (Recipe 3.2).
- **Hardcoding every URL in the client** → *fix:* one stable entry URL; discover the rest (Recipes 4.1, 5.1).
- **Rejecting messages with unknown fields** → *fix:* Must Ignore rule; pass complete records through (Recipe 6.8).
- **Stripping unfamiliar fields before forwarding** → *fix:* forward the complete record + ETag (Recipe 6.13).
- **Removing or redefining published properties** → *fix:* "Don't Change It, Add It" + parallel properties (Recipes 3.10, 3.11).
- **Breaking changes to a published semantic profile** → *fix:* version at a new URI.
- **No caching metadata on responses** → *fix:* always emit `Cache-Control` + `ETag` (Recipe 6.9).
- **Retrying POST/PATCH on transient failure** → *fix:* only retry idempotent methods; use idempotency keys otherwise.
- **No fallback strategy for dependent services** → *fix:* retry → static fallback → dynamic fallback → queue → give up (Recipe 5.16).
- **Stuffing workflow transient state into headers** → *fix:* put it in the body; headers break caching (Recipe 7.15).
- **Confusing query limits with page sizes** → *fix:* they're separate controls (Recipes 6.12 vs 7.11).

## Decision Heuristics / Checklists

- **Media type selection:** Default HTML. Add Collection+JSON/SIREN/HAL for richer M2M. Avoid custom media types unless you're a vertical leader.
- **Write method:** PUT for create/update (idempotent); POST only when forced (e.g., browser-only HTML forms) — then add Idempotency-Key.
- **Status code for empty result:** Collection query empty → 200. Single-resource URL missing → 404. Malformed → 400. Server can't fulfill → 5xx.
- **Cache lifetime:** Match data volatility. Static lists = hours/days. Shopping cart = seconds.
- **Retry policy:** Only idempotent methods; exponential backoff (2s → 4s → 16s); max 3; add jitter.
- **State transfer between services:** Inline FORM (simplest) → import/export ops (larger) → shared URL reference (most coupled).
- **Error format:** Plain status code when sufficient → RFC 7807 Problem Details when the client needs to programmatically resolve the error.
- **Workflow style:** Few steps, little branching → orchestration. Many steps, async, parallel → choreography. Hybrid → hypermedia workflow (RJCL).
- **Proxy type:** COP for a single noncompliant service; ELP for a service family; SPP for vocab/format normalization only.
- **Modify-or-fork:** Non-breaking addition → modify in place (3 rules). Breaking change → fork the interface, run both, migrate.

## Key Takeaways

1. **Hypermedia is the glue** — links + forms embedded in responses let clients discover actions at runtime; this is the foundation of evolvability.
2. **Separate the four layers** — protocol, message format, vocabulary, actions — so each evolves independently.
3. **Use structured media types** — HTML, Collection+JSON, HAL, SIREN keep message structure stable while content changes.
4. **Publish vocabularies + semantic profiles (ALPS)** — ontology, taxonomy, choreography in a machine-readable doc.
5. **PUT, not POST, for writes** — PUT-Create + `If-None-Match: *` eliminates the lost-response problem.
6. **Design for repeatability, reversibility, extensibility** — idempotent bodies, undo support, "Don't Change It, Add It."
7. **Clients are runtime-driven** — one stable URL, discover everything else, maintain own state, validate by structure not content.
8. **Services are good web citizens** — stable entry point, hidden internals, content negotiation, published metadata/vocab/health, RFC 7807 errors, runtime fallbacks.
9. **Data hides behind the interface** — no storage/relationship leakage; idempotent changes; honor caching; Must Ignore unknown fields.
10. **Workflow needs composable interfaces** — Execute/Repeat/Revert/Cancel per task; Continue/Restart/Cancel per job; state shared as documents.
11. **Start small, iterate** — apply recipes incrementally; wrap legacy via proxies; "smallest thing that teaches the most, over and over."
12. **The guiding principle dominates** — design for strangers, on the scale of decades, assuming everything will change.

## Cross-References
- Related: [[../Mastering_Api_Architecture.md]] (REST/gRPC/GraphQL selection, OpenAPI, contract testing, OAuth2, gateway/mesh, threat modeling)
- Topic index: [[../INDEX.md]]
