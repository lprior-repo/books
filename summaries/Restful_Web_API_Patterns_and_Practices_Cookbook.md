# RESTful Web API Patterns & Practices Cookbook -- Comprehensive Summary

**Author:** Mike Amundsen | **Publisher:** O'Reilly Media, 2022 | **Subtitle:** *Connecting and Orchestrating Microservices and Distributed Data*

This book is a cookbook of over 70 proven recipes for designing, building, and maintaining RESTful web APIs that can operate reliably at scale on the open web. Mike Amundsen draws on decades of experience to provide patterns for creating service interfaces that machines built by different people -- who have never met -- can use to communicate successfully. The recipes are technology-agnostic and focus on HTTP, hypermedia, and web standards as the foundation for resilient distributed systems.

The book is organized as a traditional cookbook: each recipe follows a consistent structure of Problem, Solution, Example, Discussion, and Related Recipes. The recipes are grouped into five chapters covering design, clients, services, data, and workflow. While each recipe is self-contained, many reference and build upon other recipes, reflecting the interconnected nature of distributed systems. The author emphasizes that the challenges of software design rarely change -- only the solutions do, driven by technology advances and fashion trends. The recipes therefore focus on enduring challenges rather than specific tools or frameworks.

The book is dedicated to architect and design theorist Christopher Alexander (1936-2022), whose pattern language approach to building architecture directly inspired the cookbook format and the emphasis on composable, interconnected solutions.

---

## Part I: Understanding RESTful Hypermedia

### Chapter 1: Introducing RESTful Web APIs

The book opens by establishing the intellectual foundations for the recipes that follow. The guiding principle is: "Leverage global reach to solve problems you haven't thought of for people you have never met."

**Three Intellectual Pillars:**

1. **Fielding's REST.** Roy Fielding's 2000 dissertation ("Architectural Styles and the Design of Network-based Software Architectures") defined Representational State Transfer as an architectural style emphasizing scalability of component interactions, generality of interfaces, independent deployment of components, and intermediary components to reduce interaction latency, enforce security, and encapsulate legacy systems. Fielding's method was to identify desirable system-level properties and then select constraints to induce those properties. His work identified key architectural properties -- performance (network efficiency and user-perceived responsiveness), scalability (supporting large numbers of components), simplicity (through separation of concerns), modifiability (via evolvability, extensibility, customizability, configurability, and reusability), visibility (monitoring via caches and proxies), portability (running across environments), and reliability (resilience to single-component failures) -- that emerge when the REST constraints are applied as a whole. The book deliberately selects recipes that lead to services exhibiting these properties.

2. **Tim Berners-Lee's World Wide Web.** The web was designed as a "universal linked information system" where generality and portability matter most. Berners-Lee's 1989 proposal at CERN described a system for connecting related documents via links and forms that could be accessed from anywhere, using free software on common computers. Two principles stand out: the Rule of Least Power (use the simplest technology suitable for the task, later codified as a W3C document) and the ethos that anyone can link to anything without special arrangements. These principles lowered the barrier to entry and fueled the web's explosive growth. The book draws heavily on both: using simple, well-established standards, and designing services that allow unanticipated connections.

3. **Alan Kay's Extreme Late Binding.** Kay defined OOP as messaging, local state protection, and extreme late binding. As Curtis Poe explained in 2019, extreme late binding "permits you to not commit too early to the one true way of solving an issue ... and can also allow you to build systems that you can change while they are still running." Since the internet is always running, services must be designed to evolve in production. This concept of late binding directly underpins the book's emphasis on hypermedia controls being resolved at runtime rather than hardcoded at design time.

**Why Hypermedia?**

Hypermedia -- the ability to connect separate resources via links and forms -- is the central technique the book advocates. Hypermedia systems consist of nodes (resources) connected by links, expressed through URIs. Forms extend links by allowing data to be passed. Hypermedia controls (links and forms) embedded in responses allow clients to navigate and interact with services without prior knowledge of the interface details. This "follow your nose" approach is what makes the web work for humans; applying it to machine-to-machine (M2M) communication is the book's core thesis.

The history of hypermedia stretches back nearly a century: Paul Otlet's "World Wide Network" (1940), Vannevar Bush's "As We May Think" (1945), Douglas Engelbart's "Mother of All Demos" (1968), and Ted Nelson's coining of "hypertext" and "hypermedia" in the 1950s-60s all led to Berners-Lee's World Wide Web.

**The Value of Messages.** Drawing on J.C.R. Licklider's 1966 paper on interplanetary communication ("On-Line Man-Computer Communication"), the book argues that M2M communication requires a "metamessage" approach -- a shared understanding of how to communicate, separate from the meaning of the data being exchanged. Licklider's challenge was "how do you get communications started among totally uncorrelated 'sapient' beings?" This is essentially the same challenge faced by API designers today: how do you get services built by different teams, using different technologies, to communicate reliably? HTTP provides this shared protocol, media types provide shared message formats, and vocabularies provide shared data terms. The key insight from Licklider's work is that the *metamessage* (the rules of communication) must be separate from the *message* (the content being communicated). This separation of protocol from content is what makes the web's layered architecture work at scale.

**Richardson's Magic Strings.** Leonard Richardson observed that web APIs depend on a set of shared "magic strings" -- well-known identifiers, link relations, and property names that both client and server must agree on. These include IANA-registered link relation values like "self," "next," "prev," "collection," and "item," as well as domain-specific property names like "givenName" or "postalCode." Managing these strings through published vocabularies and semantic profiles is essential for interoperability. The book treats vocabulary management as a governance responsibility that should not be taken lightly -- teams that maintain shared vocabularies are doing "important and valuable work" that underpins the entire interoperability of the system.

**Shared Principles for Scalable Services.** The book identifies five supporting principles: Discovery (share solutions and find others' solutions), Extension (design for uses not yet imagined), Composition (enable strangers to interact safely), Evolution (promote longevity over decades), and Longevity (accept that everything changes).

---

### Chapter 2: Thinking and Designing in Hypermedia

This chapter provides the philosophical and technical background for each of the recipe categories in Part II.

**Hypermedia Designs.** The foundation of hypermedia-driven systems rests on three elements: messages (the format, e.g., HTML, Collection+JSON, SIREN), vocabularies (the domain-specific terms, e.g., Schema.org, FHIR, ACORD), and actions (operations like save, approve, share). Morville's information architecture framework provides the theoretical backbone: ontology (what things exist -- the individual data properties and their definitions), taxonomy (how things relate -- how individual properties are grouped into aggregate objects like "Person" or "Order"), and choreography (what you can do with things -- the actions or state transitions available, such as "goHome," "doCreate," "doUpdate," and "doRemove"). The book stresses that these three pillars must be addressed in any complete API design, and that semantic profile documents like ALPS encode all three in a machine-readable format. The book traces the concept of information architecture through Richard Saul Wurman, who coined the term "information architect" in 1997, through Louis Rosenfeld and Peter Morville's foundational work on organizing information for findability, and into the specific needs of M2M communication on the web.

**Hypermedia Clients.** HTML browsers demonstrate the ideal hypermedia client -- a single installed application that can interact with thousands of services without code changes, relying entirely on runtime hypermedia controls. The browser was never designed for any specific website; instead it was designed to interpret a general message format (HTML) that carries its own navigation instructions (links and forms). For M2M clients, the challenge is to build similarly resilient consumers that are driven by hypermedia metadata rather than hardcoded assumptions about specific services. The book introduces the concept of "message-centric" client implementations, where the client's first job is to validate the structure of the incoming message (its well-formedness) before attempting to extract and process the data content (its validity). This two-phase processing model is critical for resilience: it means the client never crashes when encountering unexpected data -- it simply ignores what it does not understand. The book also draws on James J. Gibson's ecological psychology concept of "affordances" -- the actionable possibilities that an environment offers. In the web context, links afford navigation and forms afford data submission. Clients should be coded to recognize and act upon these affordances generically.

**Hypermedia Services.** Services should be designed as "good citizens" of the web: they should publish at least one stable URL (the entry point), avoid leaking internal models through their external interfaces, support content negotiation so consumers can request preferred formats, publish vocabularies and metadata for runtime discovery, and provide health monitoring and standardized error reporting. The book emphasizes that services should be designed not just for a single known consumer but for any possible consumer -- including those not yet built. This is the practical application of the guiding principle. Services that expose internal database schemas, implementation-specific error messages, or technology-dependent URLs are fragile and resistant to change. Services that publish clean, vocabulary-aligned, hypermedia-rich interfaces are resilient and evolvable. The book also covers the pattern of using semantic proxies to wrap noncompliant services, allowing legacy or third-party services to participate in a hypermedia ecosystem without modification.

**Distributed Data.** Managing data in a distributed, hypermedia-driven system requires hiding storage internals, making all changes idempotent, supporting caching, handling unknown fields gracefully, and enabling safe modification of data models in production. The book takes the position that each service should own its own data storage and that services should interact through message passing (state transfer) rather than shared databases. This is a fundamental architectural decision that enables independent deployment and evolution. The data chapter covers practical patterns for query design (using URL structures and media types rather than exposing query languages), response pagination (using hypermedia links for next/previous navigation), caching strategies (leveraging HTTP's ETag and Cache-Control headers), and safe data model evolution (the "Don't Change It, Add It" rule applied at the storage layer). The chapter also addresses the challenge of data transformation between services that use different internal models but must interoperate through shared vocabulary terms.

**Hypermedia Workflow.** The most advanced topic in the book, workflow involves enlisting multiple independent services into a coordinated process. Each service must support a composable interface with four actions: Execute (perform the primary work), Repeat (retry the work in case of transient failure), Revert (undo the work in case of errors elsewhere in the workflow), and Cancel (stop processing and undo any previous work). Jobs (collections of tasks) add Continue, Restart, and Cancel actions. Key workflow challenges include sharing state without sharing data models (using structured documents as the transfer mechanism), constraining workflows through standardized affordances (similar to how HTML constrains interaction through its set of tags), observing workflows through progress resources and dashboards, managing time through maxTTL limits, and handling errors through automatic retries, local undo, and human escalation ("calling for help"). The book advocates for a declarative approach to workflow definition -- expressing workflows as hypermedia documents rather than imperative code -- because declarative descriptions can be modified at runtime without redeploying code. The RESTful Job Control Language (RJCL) defined in Recipe 7.6 provides a concrete specification for this approach, mapping each workflow operation to a hypermedia affordance with a well-defined URL, HTTP method, and request/response format.

---

## Part II: Hypermedia Recipe Catalog

### Chapter 3: Hypermedia Design (Recipes 3.1 -- 3.11)

This chapter addresses foundational design decisions that must be made before coding begins. It focuses on the relationship between media types, hypermedia controls, data properties, and semantic profiles.

**Recipe 3.1: Creating Interoperability with Registered Media Types.** To ensure long-term interoperability, services should support one or more open, registered media types (e.g., HTML, Collection+JSON, HAL, SIREN). Registered media types provide stable formats that clients can bind to without understanding the content. The IANA is the authoritative source. HTML is recommended as a default because of its 30+ year track record, universal browser support, and extensive tooling. Services should document which media types they support and allow consumers to discover and express preferences. Creating custom media types is only justified for very large consumer bases or domain-leading verticals.

**Recipe 3.2: Ensuring Future Compatibility with Structured Media Types.** Structured media types (SMTs) maintain a stable message structure even when content changes. For example, HTML `<ul>` and `<li>` elements form a structure that remains valid regardless of which properties appear. Unstructured formats like plain JSON change their structure when properties are added or removed. The key insight: separate well-formedness (compliance with message structure rules) from validity (compliance with content rules). Messages should remain well-formed even when validity rules evolve.

**Recipe 3.3: Sharing Domain Specifics via Published Vocabularies.** Services should use well-documented, widely known data property names from published vocabularies (Schema.org, Microformats.org, Dublin Core) rather than internal terminology. This decouples the external interface from internal data models. When internal terms differ from public vocabulary terms, services implement an "anti-corruption layer" to translate between them. Vocabularies should be documented using the ALPS (Application-Level Profile Semantics) format and published alongside the API. A governance document should establish a priority order for vocabulary sources.

**Recipe 3.4: Describing Problem Spaces with Semantic Profiles.** Semantic Profile Documents (SPDs) describe all data properties, objects, and actions a service supports, covering all three pillars of information architecture: ontology (properties), taxonomy (object groupings), and choreography (actions and state transitions). The ALPS format is the primary example. SPDs differ from API definition formats like OpenAPI -- they describe the problem space (what) rather than the implementation (how). Each action in an ALPS profile is typed as safe (read-only), unsafe (non-idempotent write), or idempotent (repeatable write), and includes a `rt` (return type) attribute indicating the expected resulting state.

**Recipe 3.5: Expressing Actions at Runtime with Embedded Hypermedia.** Actions should be expressed through hypermedia controls (links and forms) embedded in response messages at runtime, not hardcoded into client applications. This allows services to change their URLs, methods, and input parameters without breaking clients. Forms contain all the metadata needed to construct a valid request: the URL, HTTP method, content type, and input fields with their types and constraints. Links provide navigation affordances. This is how HTML has worked for decades, and M2M APIs should follow the same pattern.

**Recipe 3.6: Designing Consistent Data Writes with Idempotent Actions.** The "failed POST" problem -- when a client sends a POST and never receives a response -- creates dangerous ambiguity. Did the write succeed? Is it safe to retry? The solution is to use HTTP PUT instead of POST for all writes. PUT is idempotent by design, meaning it produces the same result regardless of how many times it is executed. For creating new resources, use PUT with the `If-None-Match: *` header. For updating existing resources, use PUT with the `If-Match:` header containing the ETag of the current version. This pattern, called "PUT-Create," requires clients to supply their own resource identifiers, which also improves reliability and throughput.

**Recipe 3.7: Enabling Interoperability with Inter-Service State Transfers.** Services should be designed to work as part of a larger solution, not just as standalone systems. Three approaches to state transfer between services: (1) Pass by value using inline forms -- the simplest approach, where hypermedia forms carry all needed state data. (2) Pass by value using dedicated import/export operations -- useful for larger, more complex state collections. (3) Pass by reference via shared URLs -- both services access the same resource by its URL, requiring prior agreement on format and vocabulary. The simpler the state transfer, the more composable the service.

**Recipe 3.8: Designing for Repeatable Actions.** Network unreliability demands that actions be safely repeatable. Two levels of repeatability: Network idempotence (using PUT instead of POST so the HTTP method itself is idempotent) and Operation idempotence (designing message bodies to use replacement values rather than increments). For example, instead of "increase price by 5%," send "if current price is 100, set to 105." This allows safe retries even when individual operations fail partway through.

**Recipe 3.9: Designing for Reversible Actions.** When updates need to be rolled back, two approaches apply: (1) Issue a second PUT with the previous values (assuming you stored them and no one else has modified the resource). (2) Implement special undo operations (e.g., `undoDelete`) that restore previously removed resources. Services designed for workflow participation must support reversibility as a first-class feature.

**Recipe 3.10: Designing for Extensible Messages.** To extend message formats without breaking existing consumers, follow the "Don't Change It, Add It" rule. Three techniques: (1) Add a name-value pair (NVP) collection to the initial design to accommodate future properties. (2) Add parallel properties alongside existing ones (e.g., add `givenName` and `familyName` while keeping `name`). (3) Use a root wrapper element that can host multiple output format versions in a single response. Structured media types like HAL, SIREN, and Collection+JSON already follow these patterns.

**Recipe 3.11: Designing for Modifiable Interfaces.** Three rules for modifying service interfaces without breaking consumers: (1) Take nothing away -- existing URLs, properties, and methods are promises. (2) Don't redefine things -- changing what an existing element means is equivalent to removing it. (3) Make additions optional -- new features must have sensible defaults and must not be required. The chapter cites Hyrum's Law: "With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody." When a breaking change is unavoidable, "fork" the interface by running both old and new APIs in parallel during migration.

---

### Chapter 4: Hypermedia Clients (Recipes 4.1 -- 4.16)

This chapter focuses on building resilient client applications that consume web APIs. The key insight is that clients should be driven by runtime hypermedia metadata rather than hardcoded assumptions about specific services, just as HTML browsers are.

**Recipe 4.1: Limiting the Use of Hardcoded URLs.** Client applications should know only one URL -- the "home" or "starting" URL of a service. All other URLs should be discovered at runtime through hypermedia links in responses. Hardcoding multiple URLs couples the client to the service's URL structure, which may change. The starting URL acts as the single point of entry; from there, all navigation is driven by links and forms in the response messages.

**Recipe 4.2: Coding Clients to Be HTTP Aware.** Clients must understand and properly use HTTP semantics, including status codes, headers, and methods. This means treating 2xx as success, 3xx as redirection, 4xx as client errors, and 5xx as server errors. Clients should honor cache headers (ETag, Cache-Control), support content negotiation (Accept headers), and use conditional requests (If-Match, If-None-Match) for optimistic concurrency control.

**Recipe 4.3: Coding Resilient Clients with Message-Centric Implementations.** Clients should parse messages based on the media type structure, not the specific data content. A message-centric client first validates the message structure (well-formedness) and then extracts data properties. This means the client can handle messages that include new, unknown properties without breaking -- the core advantage of structured media types.

**Recipe 4.4: Coding Effective Clients to Understand Vocabulary Profiles.** Clients should retrieve and understand semantic profile documents (ALPS) at runtime. This allows them to understand the meaning of data properties, the relationships between objects, and the available actions. By consulting the profile, clients can determine what actions are possible in each state and how to construct valid requests.

**Recipe 4.5: Negotiating for Profile Support at Runtime.** Clients should use the `Accept-Profile` and `Content-Profile` HTTP headers to negotiate which semantic profile both parties understand. This runtime negotiation allows clients and servers that share vocabulary understanding to communicate more effectively, even when they were not designed together.

**Recipe 4.6: Managing Representation Formats at Runtime.** Clients should use HTTP content negotiation (the `Accept` header) to indicate their preferred media types. Servers that support multiple formats can respond accordingly. Clients should be prepared to handle whatever format the server actually returns, falling back gracefully when their preferred format is not available.

**Recipe 4.7: Using Schema Documents as a Source of Message Metadata.** Clients can retrieve schema documents (JSON Schema, ALPS, etc.) at runtime to understand message structure and validation rules. These schemas provide metadata about expected properties, their types, and constraints, enabling clients to validate data and construct requests without hardcoded knowledge.

**Recipe 4.8: Every Important Element Within a Response Needs an Identifier.** Every significant element in a response -- forms, links, data blocks -- must have a unique identifier so clients can locate them programmatically. Four identifier types are recommended: ID (document-wide unique), NAME (application-wide unique), REL (system-wide unique, multivalue), and TAG (solution-specific, nonunique, multivalue). Clients should be able to find the desired form, link, or data block using at least one of these identifier types.

**Recipe 4.9: Relying on Hypermedia Controls in the Response.** Clients should rely entirely on hypermedia controls (links and forms) in the response to determine what actions are available and how to execute them. This means clients never need to guess URLs, HTTP methods, or input parameters -- they read them from the response at runtime.

**Recipe 4.10: Supporting Links and Forms for Nonhypermedia Services.** When consuming services that do not natively support hypermedia (e.g., plain JSON APIs without links or forms), clients can maintain a local mapping that "simulates" hypermedia controls. This adapter pattern allows clients to use hypermedia-driven logic even with non-compliant services.

**Recipe 4.11: Validating Data Properties at Runtime.** Clients should validate incoming data properties at runtime using vocabulary definitions and schema documents, not hardcoded validation rules. This allows clients to adapt when services add new properties or change validation constraints.

**Recipe 4.12: Using Document Schemas to Validate Outgoing Messages.** Before sending requests, clients should validate their outgoing messages against the schema or profile associated with the target action. This catches errors early and ensures the request will be accepted by the server.

**Recipe 4.13: Using Document Queries to Validate Incoming Messages.** Clients should use query-based validation (e.g., JSONPath, XPath, CSS selectors) to verify that incoming responses contain the expected elements. This is more resilient than strict schema validation because it does not fail when new elements are added.

**Recipe 4.14: Validating Incoming Data.** Beyond structural validation, clients should validate the semantic content of incoming data -- checking that values fall within expected ranges, that required properties are present, and that data types are correct. This validation should be driven by the semantic profile, not hardcoded rules.

**Recipe 4.15: Maintaining Your Own State.** Clients should maintain their own state locally rather than relying on the server to maintain session state. This aligns with REST's statelessness constraint and allows clients to recover from failures by replaying their state without server-side session dependency. State can be stored as a local document or data structure that captures where the client is in its interaction with the service.

**Recipe 4.16: Having a Goal in Mind.** Hypermedia clients should be designed with a specific goal -- a desired end state -- and navigate through hypermedia controls to achieve that goal. This is analogous to how humans browse the web with a purpose. The client starts at the home URL, examines available links and forms, selects the ones that move it closer to its goal, and repeats until the goal is achieved. This goal-driven approach, combined with semantic profiles, allows clients to solve problems without prior knowledge of the service's specific implementation.

---

### Chapter 5: Hypermedia Services (Recipes 5.1 -- 5.17)

This chapter covers server-side recipes for building resilient, discoverable, and evolvable services.

**Recipe 5.1: Publishing at Least One Stable URL.** Every service must publish at least one stable, well-known URL (the "home" or "entry point" URL). All other URLs can change over time as long as clients discover them through hypermedia links starting from the stable entry point. This is analogous to a website's homepage URL.

**Recipe 5.2: Preventing Internal Model Leaks.** Services must never expose internal implementation details (database column names, internal IDs, technology choices) through their external interface. An anti-corruption layer should translate between internal models and the published external vocabulary. This prevents internal changes from breaking the API contract.

**Recipe 5.3: Converting Internal Models to External Messages.** Services need a clear mapping between internal data representations and external message formats. The conversion should use the published vocabulary and structured media type, ensuring that internal model changes do not affect the external message structure. Each internal property maps to a well-known vocabulary term in the external interface.

**Recipe 5.4: Expressing Internal Functions as External Actions.** Internal operations should be exposed as hypermedia forms with clear semantics. Each form includes the URL, HTTP method, content type, and input fields. Actions should be typed as safe, unsafe, or idempotent in the semantic profile. This allows clients to discover available actions at runtime rather than depending on out-of-band documentation.

**Recipe 5.5: Advertising Support for Client Response Preferences.** Services should support the `Prefer` HTTP header to allow clients to express preferences about response content. For example, clients can request minimal representations, include/exclude specific properties, or ask for asynchronous processing. The `Preference-Applied` response header confirms which preferences were honored.

**Recipe 5.6: Supporting HTTP Content Negotiation.** Services should support both proactive (server-driven) content negotiation using the `Accept` header and reactive (agent-driven) negotiation using 300 Multiple Choices responses. Proactive negotiation is the most common approach; the client sends preferences and the server selects the best representation. The service should support multiple media types and clearly document which ones are available.

**Recipe 5.7: Publishing Complete Vocabularies for Machine Clients.** Services should publish machine-readable vocabulary documents (using ALPS or similar formats) that list all data properties, object types, and actions the service supports. This enables automated clients to discover and understand the service at runtime. The vocabulary document should include term definitions, descriptions, and references to authoritative sources.

**Recipe 5.8: Supporting Shared Vocabularies in Standard Formats.** Services should publish vocabularies in standard, widely supported formats and make them accessible via well-known URLs. The ALPS format is recommended because it is simple, supports both JSON and XML representations, and maps cleanly to the three pillars of information architecture.

**Recipe 5.9: Publishing Service Definition Documents.** In addition to semantic profiles, services should publish definition documents (e.g., OpenAPI, AsyncAPI) that describe the protocol-level interface -- URLs, methods, request/response formats, and status codes. These documents complement semantic profiles by providing implementation-level details.

**Recipe 5.10: Publishing API Metadata.** Services should publish metadata about themselves, including version information, deprecation notices, rate limits, authentication requirements, and supported features. This metadata helps clients adapt their behavior at runtime and plan for changes.

**Recipe 5.11: Supporting Service Health Monitoring.** Services should expose health check endpoints that report their operational status and the status of their dependencies. The health response should include the service version, uptime, and dependency health (database, external services, etc.). Standardized health check formats enable automated monitoring and alerting.

**Recipe 5.12: Standardizing Error Reporting.** Services should use RFC 7807 (Problem Details for HTTP APIs) for error responses. Problem detail documents include a type URI (identifying the error category), title (human-readable summary), status (HTTP status code), detail (specific explanation), and instance (the specific occurrence). This standardized format allows clients to parse and respond to errors programmatically.

**Recipe 5.13: Improving Service Discoverability with a Runtime Service Registry.** Services should register themselves in a runtime registry that allows clients to discover available services dynamically. The registry supports "find and bind" operations where clients locate services by capability at runtime rather than depending on hardcoded endpoints. This is especially valuable in microservice architectures where services are frequently added, removed, or relocated.

**Recipe 5.14: Increasing Throughput with Client-Supplied Identifiers.** When using PUT-Create (Recipe 3.6), clients supply their own resource identifiers. This eliminates the need for the server to generate IDs and reduces the risk of duplicate creation. UUIDs are a common choice. Client-supplied IDs also enable offline operation and reliable retries.

**Recipe 5.15: Improving Reliability with Idempotent Create.** This recipe expands on the PUT-Create pattern. By combining PUT with client-supplied identifiers and the `If-None-Match: *` header, services can guarantee that create operations are idempotent. If the resource already exists, the server returns 200 OK or 204 No Content instead of creating a duplicate. This eliminates the "did my POST succeed?" ambiguity entirely.

**Recipe 5.16: Providing Runtime Fallbacks for Dependent Services.** Services that depend on other services should implement fallback strategies for when dependencies are unavailable. Strategies include returning cached/stale data, providing degraded functionality, returning a meaningful error with retry guidance, or queuing the request for later processing. Circuit breaker patterns can prevent cascading failures.

**Recipe 5.17: Using Semantic Proxies to Access Noncompliant Services.** When you need to consume a service that does not follow hypermedia patterns, you can implement a semantic proxy that wraps the noncompliant service in a hypermedia-compliant interface. The proxy translates between the external hypermedia API and the internal noncompliant service, adding links, forms, and metadata. This allows you to bring consistency to your API ecosystem without rewriting legacy services. However, proxies add latency and complexity, so they should be used sparingly.

---

### Chapter 6: Distributed Data (Recipes 6.1 -- 6.13)

This chapter addresses the challenges of managing persisted data in a distributed, hypermedia-driven environment, focusing on responsiveness, scalability, reliability, and data integrity.

**Recipe 6.1: Hiding Your Data Storage Internals.** Never expose data storage technology details (SQL table names, MongoDB collections, Elasticsearch indices) through the API interface. Queries should be expressed using domain vocabulary, not storage-specific syntax. For example, instead of exposing a SQL-like query parameter like `?filter=status='active'`, expose a semantic query form like `?active=true`. This allows you to change storage technology without breaking the API.

**Recipe 6.2: Making All Changes Idempotent.** All data modifications should be idempotent at both the network and operation levels. Use PUT instead of POST for writes, and design update messages to use absolute values rather than relative increments. For example, instead of "add 5 to quantity," use "set quantity to 15." This ensures that repeated requests (due to network failures) produce the same result.

**Recipe 6.3: Hiding Data Relationships for External Actions.** Do not expose internal data relationships (foreign keys, join tables) through the API. Instead, express relationships through hypermedia links. For example, instead of embedding a `customerId` foreign key in an order resource, include a link with `rel="customer"` pointing to the customer resource. This decouples the API from the internal data model.

**Recipe 6.4: Leveraging HTTP URLs to Support "Contains" and "AND" Queries.** Design query interfaces that use URL paths and query parameters to express common query patterns. For example, `/customers?region=east&status=active` expresses an AND query. Containment queries can use path segments like `/customers/east/active`. These URL-based query patterns are intuitive, cacheable, and independent of the underlying query technology.

**Recipe 6.5: Returning Metadata for Query Responses.** Query responses should include metadata beyond the data itself: total result count, page information (offset, limit), links to next/previous pages, and query execution time. This metadata enables clients to navigate large result sets efficiently and understand the scope of the response. Standardized metadata structures allow generic client-side pagination and filtering logic.

**Recipe 6.6: Returning HTTP 200 Versus HTTP 400 for Data-Centric Queries.** When a query executes successfully but returns no results, return HTTP 200 with an empty collection, not HTTP 400 or 404. The query itself was valid; the absence of results is not an error. Reserve 4xx responses for malformed queries or queries against nonexistent resources.

**Recipe 6.7: Using Media Types for Data Queries.** Use media types to express query format and response format preferences. For example, a client can send `Accept: application/vnd.collection+json` to indicate the desired response format. This allows the same query endpoint to support multiple representation formats, improving interoperability.

**Recipe 6.8: Ignoring Unknown Data Fields.** Services should silently ignore unknown or unexpected fields in incoming requests rather than rejecting them. This is the "Robustness Principle" (Postel's Law): be conservative in what you send, liberal in what you accept. Ignoring unknown fields allows clients to evolve independently without coordination. Clients should also ignore unknown fields in responses.

**Recipe 6.9: Improving Performance with Caching Directives.** Services should use HTTP caching mechanisms (ETag, Last-Modified, Cache-Control, Expires) to enable efficient caching at multiple levels: client-side, proxy, and CDN. ETags enable conditional requests (`If-None-Match`) that return 304 Not Modified when data hasn't changed, saving bandwidth. Cache-Control headers specify how long responses can be cached and under what conditions.

**Recipe 6.10: Modifying Data Models in Production.** When internal data models must change, use a multi-step migration strategy: (1) Add new fields alongside existing ones without removing the old. (2) Support both old and new fields in the external API. (3) Migrate data gradually. (4) Remove old fields only after all consumers have updated. This follows the "Don't Change It, Add It" rule from Recipe 3.10.

**Recipe 6.11: Extending Remote Data Stores.** When extending data storage for a service, do so without disrupting the existing API contract. New storage fields should map to new optional properties in the external interface. If the extension requires new query capabilities, add them as new query forms rather than modifying existing ones.

**Recipe 6.12: Limiting Large-Scale Responses.** Services should implement pagination, field selection, and result limiting to prevent oversized responses. Standard pagination parameters (offset, limit) and hypermedia links (next, previous, first, last) enable clients to navigate large collections efficiently. Field selection allows clients to request only the properties they need, reducing bandwidth and processing time.

**Recipe 6.13: Using Pass-Through Proxies for Data Exchange.** When services cannot directly share data due to incompatible interfaces, a pass-through proxy can translate between them. The proxy sits between the services and handles format conversion, vocabulary mapping, and protocol adaptation. This is useful for integrating legacy services or third-party APIs that don't follow hypermedia patterns. As with all proxy patterns, use sparingly due to added latency and complexity.

---

### Chapter 7: Hypermedia Workflow (Recipes 7.1 -- 7.20)

The most advanced chapter, covering the coordination of multiple independent services into resilient workflows. This chapter brings together many recipes from earlier chapters.

**Recipe 7.1: Designing Workflow-Compliant Services.** Each service in a workflow must support a composable interface with four actions: Execute (do the work), Repeat (retry the work), Revert (undo the work), and Cancel (stop processing and undo). Workflows consist of tasks (individual service operations) collected into jobs. Jobs support Continue, Restart, and Cancel actions. This composable interface allows a workflow coordinator to manage multiple services without understanding their internal implementation.

**Recipe 7.2: Supporting Shared State for Workflows.** Services in a workflow should share state through structured documents (not shared data models or databases). Data values are passed as strongly typed documents using the agreed-upon media type and vocabulary. State can be shared by value (inline in forms) or by reference (via a shared URL). Sharing documents rather than data models keeps services loosely coupled.

**Recipe 7.3: Describing Workflow as Code.** Workflows can be expressed as imperative code that orchestrates service calls. While straightforward, this approach tightly couples the workflow to the specific service implementations and makes it difficult to modify the workflow at runtime.

**Recipe 7.4: Describing Workflow as DSL.** A domain-specific language (DSL) provides a more declarative way to express workflows. DSLs describe what needs to be done rather than how, making workflows easier to modify and understand. The DSL is interpreted at runtime by a workflow engine.

**Recipe 7.5: Describing Workflow as Documents.** The most flexible approach: workflows are expressed as hypermedia documents that describe the tasks, their dependencies, and the state transitions. These documents can be created, modified, and stored like any other resource, enabling runtime workflow definition and modification. This is the approach most aligned with the book's hypermedia philosophy.

**Recipe 7.6: Supporting RESTful Job Control Language.** This recipe defines a RESTful Job Control Language (RJCL) -- a standardized set of hypermedia affordances for managing workflow jobs. RJCL defines affordances for creating jobs, adding tasks, starting execution, checking progress, retrying failed tasks, reverting completed tasks, and cancelling jobs. Each job and task is represented as a resource with its own URL, and all operations are expressed as hypermedia forms. This provides a universal, protocol-level interface for workflow management.

**Recipe 7.7: Exposing a Progress Resource for Your Workflows.** Workflows should expose a progress resource that reports the current state of each task in the job. This includes task status (pending, running, completed, failed), execution timestamps, and error details. The progress resource enables observability -- operators and automated systems can monitor workflow execution and intervene when necessary.

**Recipe 7.8: Returning All Related Actions.** Service responses should include all actions currently available for a resource, not just the most likely ones. This allows workflow coordinators to choose the appropriate action based on the current state of the job, without needing out-of-band knowledge of the service's state machine.

**Recipe 7.9: Returning Most Recently Used Resources.** For workflows that involve revisiting previous steps, services should include links to recently used or modified resources. This simplifies the workflow coordinator's task of tracking which resources were affected by previous operations.

**Recipe 7.10: Supporting Stateful Work in Progress.** Long-running operations should be modeled as stateful resources with a clear lifecycle (created, in progress, completed, failed). The service should support partial updates and checkpointing so that work can be resumed after a failure. The 202 Accepted status code indicates that a request has been accepted but not yet completed, with a Location header pointing to a status resource.

**Recipe 7.11: Enabling Standard List Navigation.** Workflows often involve navigating through collections of items (e.g., processing all orders in a queue). Services should provide standard list navigation affordances: first, previous, next, last, and item links. This allows workflow coordinators to iterate through collections using a consistent pattern regardless of the specific service.

**Recipe 7.12: Supporting Partial Form Submit.** For long-running operations that require input in stages, services should support partial form submission. Clients can submit incomplete forms and the service stores the partial state, returning a form that includes the already-submitted fields and prompts for the remaining ones. This enables multi-step interactions without requiring the client to hold all state locally.

**Recipe 7.13: Using State-Watch to Enable Client-Driven Workflow.** The state-watch pattern allows clients to monitor changes to resources by registering "watch" subscriptions. The service maintains a list of watched resources for each client and includes change notifications in responses. This enables client-driven workflows where the client reacts to state changes rather than polling for updates. Each client has its own `watchSelected` resource that tracks which resources it is monitoring.

**Recipe 7.14: Optimizing Queries with Stored Replays.** For workflows that repeatedly execute the same queries, services can support stored replays -- saved query configurations that can be re-executed with a single request. The stored replay resource contains the query parameters and execution metadata, allowing the workflow to efficiently re-run the query without resubmitting all parameters.

**Recipe 7.15: Synchronous Reply for Incomplete Work with 202 Accepted.** When a workflow task takes too long to complete synchronously, the service should return 202 Accepted with a Location header pointing to a status resource. The client can poll this resource to check progress. The service should also support a maximum time-to-live (maxTTL) for tasks, automatically cancelling work that exceeds the time limit.

**Recipe 7.16: Short-Term Fixes with Automatic Retries.** Transient failures (network timeouts, temporary service unavailability) should be handled with automatic retries. The retry strategy should include exponential backoff, a maximum retry count, and jitter to prevent thundering herd effects. Idempotent operations (those using PUT) can be safely retried; non-idempotent operations (POST) require more careful handling, ideally using idempotency keys.

**Recipe 7.17: Supporting Local Undo or Rollback.** Each service should support local undo operations that reverse the effects of a previous action. This is distinct from reverting an entire workflow -- a local undo only affects the service's own resources. The service must maintain sufficient history (snapshots, event logs) to support undo operations.

**Recipe 7.18: Calling for Help.** When automated error handling fails, workflows should have a mechanism to "call for help" -- escalating to human intervention. This typically involves creating a support ticket, sending an alert, or pausing the workflow and waiting for manual resolution. The workflow should capture sufficient context (job state, error details, task history) to enable a human to make an informed decision about whether to continue, retry, or cancel.

**Recipe 7.19: Scaling Workflow with Queues and Clusters.** For high-throughput workflows, services should support message queue-based processing and horizontal scaling. Tasks are submitted to queues and processed by worker instances. This decouples task submission from execution, enables load balancing, and provides natural backpressure handling. The workflow coordinator submits tasks to queues and monitors progress through status resources.

**Recipe 7.20: Using Workflow Proxies to Enlist Noncompliant Services.** When a workflow needs to include a service that doesn't support the composable workflow interface (Execute, Repeat, Revert, Cancel), a workflow proxy can wrap the noncompliant service. The proxy implements the workflow interface and translates between the standard workflow actions and the noncompliant service's actual API. This introduces additional complexity and potential failure points, so it should only be used when replacing the noncompliant service is not feasible.

---

### Chapter 8: Closing Remarks

The final chapter provides guidance on applying the recipes in practice.

**Applying These Recipes.** The recipes should be applied incrementally, starting with the design recipes (Chapter 3) for new services. Even small improvements -- standardizing media types, using PUT for creates, publishing vocabulary documents -- can yield significant benefits. The recipes also provide a shared vocabulary for teams to discuss API design decisions.

**Transforming Existing Services.** The recommended approach is to make small, independent changes over time, each resulting in measurable improvement. Pass-through proxy recipes (5.17, 6.13, 7.20) can be used to wrap existing services in hypermedia-compliant interfaces without rewriting them. Adrian Cockcroft's advice applies: "Whenever you do a transition, do the smallest thing that teaches you the most and do that over and over again."

**Cultural Impact.** As teams apply these recipes, the benefits compound: better performance, more stable runtimes, less resource-intensive updates. This creates momentum for further improvement. The shared principles can also transform team dynamics, freeing teams from waterfall constraints and unlocking creativity.

---

## Key Takeaways

1. **Hypermedia is the glue.** Hypermedia controls (links and forms) embedded in response messages are the key to building evolvable, resilient APIs. They allow clients to discover actions and navigate services at runtime without hardcoded assumptions.

2. **Separate concerns at every level.** Keep protocol (HTTP), message format (media types), vocabulary (property names), and actions (hypermedia controls) as separate, independent layers. This separation enables each layer to evolve without breaking the others.

3. **Use structured media types.** Formats like HTML, Collection+JSON, HAL, and SIREN maintain stable message structures even when content changes. This is essential for future compatibility and nonbreaking evolution.

4. **Publish vocabularies and semantic profiles.** Use well-known terms from Schema.org, Microformats.org, and industry standards. Document your vocabulary and actions using semantic profile documents (ALPS) so that both humans and machines can understand your API.

5. **PUT, not POST, for writes.** Use HTTP PUT for all data modifications to leverage HTTP's built-in idempotency. The PUT-Create pattern (with `If-None-Match: *`) eliminates the "failed POST" ambiguity and makes retries safe.

6. **Design for repeatability, reversibility, and extensibility.** Actions should be safely repeatable (idempotent), reversible (support undo), and the interface should be extensible without breaking existing consumers. Follow the "Don't Change It, Add It" rule.

7. **Clients should be driven by runtime metadata.** Know only one URL (the entry point). Discover everything else through hypermedia controls. Maintain your own state. Have a goal in mind. This makes clients resilient to service changes.

8. **Services should be good web citizens.** Publish stable entry points. Hide internal models. Support content negotiation. Publish metadata, vocabularies, and health checks. Use standardized error reporting (RFC 7807). Implement fallbacks for dependent services.

9. **Data should be hidden behind the interface.** Never expose storage technology, internal relationships, or schema details. Make all changes idempotent. Support caching. Ignore unknown fields. These patterns enable you to change internal data models without breaking the API.

10. **Workflow requires composable interfaces.** Each service must support Execute, Repeat, Revert, and Cancel. State is shared through documents, not shared databases. The RESTful Job Control Language provides a universal interface for managing multi-service workflows.

11. **Start small and iterate.** Apply recipes incrementally. Each small improvement builds momentum. Use proxy patterns when you cannot modify existing services. The goal is continuous improvement, not big-bang rewrites.

12. **The guiding principle matters.** "Leverage global reach to solve problems you haven't thought of for people you have never met." This principle -- rooted in the web's architecture of universal linking, low barriers to entry, and extreme late binding -- is the foundation upon which all 70+ recipes are built.
