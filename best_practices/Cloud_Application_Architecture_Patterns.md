# Cloud Application Architecture Patterns
**Authors:** Kyle Brown, Bobby Woolf, Joseph Yoder
**Topic tags:** `#architecture` `#cloud` `#reliability`
**Language focus:** vendor-neutral / polyglot (Java, Node.js, Python, Go, JavaScript)
**Sources:** `markdown_output/Cloud_Application_Architecture_Patterns_ER/Cloud_Application_Architecture_Patterns_ER.md` (Early Release, ~2,466 lines, Chs 1–3 fully available; Chs 4–10 referenced as unavailable at press time)

> **Note on scope:** This deep-dive is built strictly from the Early Release content that is actually present in the source markdown (Preface, Introduction, Chapters 1–3 + pattern stubs from the Table of Contents). Patterns from later chapters (Microservices Architecture, Event-Driven, Cloud-Native Storage, Cloud Application Clients, Migration & Modernization, Strangler) are referenced and described based on the Introduction's overview, root-pattern table, and chapter relationships, never invented. Where I quote book text, the inline citation is the chapter and section name as it appears in the ER.

---

## TL;DR

This book is the architecture half of cloud adoption — how to *design* an application so it runs well in the cloud, not how to deploy, operate, or build it. It assumes the de facto cloud stack of **Linux + containers + orchestrators + cloud-native architecture** and structures every practice as a *pattern* in a *pattern language* with root patterns anchoring each chapter. The first three chapters deliver the full architecture story: **Cloud Application** (why traditional IT assumptions break in the cloud), the three application architectures (**Big Ball of Mud → Modular Monolith → Distributed Architecture**), and the **six cloud-native patterns** (Application Package, Service API, Stateless, Replicable, External Configuration, Backend Service) plus the **Twelve-Factor App** methodology. Reach for this book when you need vendor-neutral, time-resistant architectural guidance rather than product tutorials.

---

## Best Practices by Topic

### 1. The Cloud-Native Mindset — Why Cloud is Different

**Principle:** Cloud computing changes fundamental assumptions about hardware reliability, consistency, scaling, and state. Applications designed for traditional IT *run* on the cloud but do not *run well* on it.

**Do:**
- Treat hardware as unreliable commodity; design the application to be more reliable than its infrastructure.
- Design for horizontal scaling (more computers) rather than vertical scaling (bigger computers).
- Accept eventual consistency; design transactions as simple units that can succeed or fail independently.
- Keep the application movable, stateless, immutable, and componentized.
- Delegate reusable functionality (DB, messaging, workflow, auth) to a cloud service catalog rather than embedding it.
- Treat self-service provisioning as the default; do not gate environment creation on central ops.

**Don't:**
- Assume 100% reliable hardware or accept downtime as unavoidable.
- Use ACID transactions across multiple resources as your default consistency model.
- Couple the application to a specific OS version, hardware model, or device driver.
- Design for a single computer that runs forever in one place.
- Rely on global variables, sticky sessions, fixed IP addresses, or local disk for state.
- Try to install custom middleware on a cloud VM as if it were an application server.
- Store all data in a single relational "database of record" with a one-size-fits-all schema.

**Code/Concept:**
> "Cloud computing embraces inexpensive commodity hardware that lacks the redundancies to attempt 100% reliability… To run reliably on unreliable infrastructure, a cloud application must be more reliable than its infrastructure." — *Ref: Cloud_Application_Architecture_Patterns_ER.md — "Cloud computing practices"*

> "Cloud computing does not provide a transaction manager and cloud services employ eventual consistency. Cloud application developers cannot depend on transactions and must design for eventual consistency, which counterintuitively actually makes the applications more reliable."

---

### 2. NIST Cloud Computing Definition — What "Cloud" Actually Means

**Principle:** Pin your cloud vocabulary to NIST's definition so cross-team discussions stay precise.

**Do:**
- Speak in terms of the five essential characteristics (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service).
- Distinguish service models (SaaS, PaaS, IaaS) when scoping responsibility.
- Distinguish deployment models (private, community, public, hybrid) when scoping tenancy and portability.
- Use NIST's wording to defend architectural choices to non-technical stakeholders.

**Don't:**
- Conflate "cloud" with "someone else's computer" alone — the cloud is far more than that.
- Treat SaaS/PaaS/IaaS as interchangeable; they assign very different responsibilities to the application team.
- Mix up "private cloud" with "on-prem" — a private cloud is still defined by self-service, pooling, elasticity.

**Code/Concept:** Five essential characteristics, three service models, four deployment models — quote verbatim from the book when justifying an architecture. *Ref: "Cloud computing" (Chapter 3)*.

---

### 3. Cloud-Native — Working Definition for Architects

**Principle:** "Cloud native" describes *how an application is built and deployed*, not where it lives. An application can be cloud-native and still run on traditional IT, but a non-cloud-native app on cloud underperforms.

**Do:**
- Adopt this book's working definition: cloud native = "an approach that designs an application to run well in the cloud, to take advantage of the strengths of cloud computing while avoiding and compensating for its limitations."
- Treat cloud-native as broader than technology — it includes People, Process, Policy, Technology, Business Outcomes (CNCF Cloud Native Maturity Model 2.0).
- Use CNCF's five-aspect maturity model when planning a multi-team cloud adoption.

**Don't:**
- Define "cloud native" as "it runs in the cloud."
- Assume a cloud-native app has to actually live in the cloud to count.
- Equate cloud-native with microservices only — cloud-native is about architecture and operations.

**Code/Concept:**
> IBM Cloud Native definition: "Cloud native refers less to where an application resides and more to how it is built and deployed."
> Microsoft: "Cloud-native architecture and technologies are an approach to designing, constructing, and operating workloads that are built in the cloud and take full advantage of the cloud computing model."

*Ref: "Cloud native" (Chapter 3)*.

---

### 4. The Twelve-Factor App — Baseline Methodology

**Principle:** Twelve-Factor is the canonical checklist for making an application cloud-friendly. Use it as a starting point before adding more sophisticated patterns.

**Do:**
- Enforce all twelve factors even though only some are "architecture" (the book highlights I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII).
- Use Factor I (Codebase) to mandate one repo per app, many deploys.
- Use Factor II (Dependencies) to require an explicit dependency manifest and isolation tool.
- Use Factor III (Config) to store config in environment variables (language- and OS-agnostic).
- Use Factor IV (Backing services) to treat databases, queues, caches as attached resources.
- Use Factor V (Build, release, run) to keep build, release, and run strictly separate.
- Use Factor VI (Processes) to execute the app as one or more stateless, share-nothing processes.
- Use Factor VII (Port binding) to export services via port binding (self-contained web server).
- Use Factor VIII (Concurrency) to scale out via the process model.
- Use Factor IX (Disposability) to maximize robustness with fast startup and graceful shutdown.
- Use Factor X (Dev/prod parity) to keep development, staging, and production as similar as possible.
- Use Factor XI (Logs) to treat logs as event streams.
- Use Factor XII (Admin processes) to run admin/management tasks as one-off processes.

**Don't:**
- Treat Twelve-Factor as a microservices-only checklist — it's useful for any cloud-ready app.
- Substitute a properties file for environment variables.
- Bake configuration into the build artifact (violates V and III together).
- Implement sticky sessions as a way to scale Factor VI.

**Code/Concept:**
> Factor II: "A twelve-factor app never relies on implicit existence of system-wide packages. It declares all dependencies, completely and exactly, via a dependency declaration manifest."
> Factor VI: "Twelve-factor processes are stateless and share-nothing. Any data that needs to persist must be stored in a stateful backing service, typically a database. The memory space or filesystem of the process can be used as a brief, single-transaction cache."
> Factor IX: "The twelve-factor app's processes are disposable, meaning they can be started or stopped at a moment's notice. This facilitates fast elastic scaling, rapid deployment of code or config changes, and robustness of production deploys."
> Factor VII (Port binding): "The web app exports HTTP as a service by binding to a port, and listening to requests coming in on that port."

*Ref: "The Twelve-Factor App" (Chapter 3).*

---

### 5. Software Architecture Foundations — Components & Terminology

**Principle:** Use the book's vocabulary for components so architecture discussions are unambiguous.

**Do:**
- Use this precise vocabulary:
  - **Module** — a cohesive set of code that implements a unit of functionality.
  - **Service** — a module designed to run in a different process than its clients.
  - **Program** — a set of modules and services that implement a complete domain purpose.
  - **Workload** — a deployable component on a physical/virtual server.
  - **Application** — a program + the external dependencies it needs (web server, DB).
  - **Architecture** — the strategy for decomposing functionality into components and how they collaborate.
- Recognize that a single application can use *multiple* architectures in different parts (e.g. cloud-native + microservices + event-driven).
- Frame architecture as "those parts which are harder to change" / "the decisions you wish you could get right early."

**Don't:**
- Treat architecture as a one-time activity done at the start of the project.
- Conflate "module" and "service" — they differ in *where they run*, not in cohesion.

**Code/Concept:** Ralph Johnson: architecture is "those parts which are harder to change" or "the decisions you wish you could get right early in a project." IEEE 1471-2000: "Fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution." *Ref: "Software architecture" (Chapter 2).*

---

### 6. Architectural Trade-offs — The Real Job of an Architect

**Principle:** Every architecture is a set of trade-offs. Naming them explicitly prevents accidental decisions.

**Do:**
- Surface the competing drivers explicitly: performance, availability, security, maintainability, modifiability, time to market, developer skill-set.
- Budget development effort consciously across "make it work / make it right / make it fast" (Kent Beck).
- Treat technical debt as a real cost and decide when to retire it, contain it, or ignore it.
- Choose an architecture whose trade-off profile matches your current risks.

**Don't:**
- Claim "no trade-offs" — there is always one.
- Optimize for time-to-market at the expense of maintainability forever; the cost compounds.
- Confuse "make it work" with "ship and forget." Beck's mantra is sequential, not exclusive.

**Code/Concept:**
> Kent Beck: "Make it work. Make it right. Make it fast." — Beck, *Smalltalk Best Practice Patterns* (1997).
> Richard Gabriel's "Worse is Better": "It is better to start with a minimal working program or system and grow it as needed."

*Ref: "Architectural trade-offs" (Chapter 2).*

---

### 7. Big Ball of Mud (BBoM) — Pattern & Anti-Pattern

**Principle:** BBoM is a *pattern* when you need to ship exploratory code fast and learn the domain. It is an *anti-pattern* when it accumulates unchecked technical debt in production.

**Do:**
- Use BBoM consciously for MVPs, demos, prototypes, and exploratory programming.
- Plan to "make it right" after "make it work" succeeds.
- Apply Foote & Yoder cleanup patterns when the mud starts to control you:
  - **Shearing Layers** — group artifacts that change at similar rates.
  - **Sweep It Under The Rug** — cordon off mess to a fixed area.
  - **Reconstruction** — rebuild a part cleanly once you understand it.
- Apply Wirfs-Brock & Yoder sustaining patterns:
  - **Paving Over The Wagon Trail** — shore up boundaries around repeated code paths.
  - **Wiping Your Feet At The Door** — keep external interfaces clean.

**Don't:**
- Treat BBoM as always-bad; in early stages it's often the *right* choice.
- Let a Modular Monolith devolve into a BBoM by ignoring boundaries.
- Spread shared global state, terse variables, and copy-paste duplication through a long-lived codebase.
- Believe "agile + lots of tests" alone produces clean architecture; without attention to design, even agile code becomes muddy.

**Code/Concept:**
> "Focus on features and functionality before focusing on architecture and performance. Develop an application as a Big Ball of Mud—building the system by any means available: produce simple, expedient, disposable code that adequately addresses just the problem at hand."
>
> BBoM signature: "everything talks to everything else with circular dependencies… Every shred of important state data might be global."

**Real-world example — PayPal's BBoM:** A single C++ class embodied most of PayPal's domain logic — over **5,000 methods and 500,000 lines of code**. Every application that used it had to pull in that class and its dependencies. PayPal spent 2007–2008 breaking it up, moved to XML-based communication, adopted REST and polyglot development (Node.js for some modules), and ultimately grew to **over 2,500 microservices and 750 externally published APIs**.

*Ref: "Big Ball of Mud" (Chapter 2).*

---

### 8. Modular Monolith — When to Start Here

**Principle:** A Modular Monolith is the right next step when an application must remain long-lived and maintainable, but the team isn't yet ready for the operational complexity of distribution.

**Do:**
- Define each module around one cohesive unit of functionality with an explicit interface.
- Aim for high cohesion, low coupling (Larry Constantine's Structured Design).
- Use OO encapsulation (or equivalent) to enforce module boundaries via APIs.
- Use industry Design Patterns (Gamma et al. 1995) — Adapter, Bridge, Decorator, Facade, Proxy, Strategy — to keep modules reusable.
- Use POSA patterns (Buschmann et al.) to evolve modularity: Layers, Master-Slave, Pipes and Filters, Broker, MVC, Blackboard, Interpreter.
- Assign modules to separate two-pizza teams that coordinate primarily on interfaces.

**Don't:**
- Treat "modular" as a folder structure; modules must have explicit, enforced boundaries.
- Allow circular dependencies between modules.
- Expect modules to share pointers or pass-by-reference across process boundaries later — for now they can, because they're in one process.
- Devolve the Modular Monolith back into a BBoM by ignoring its boundaries during routine changes.

**Code/Concept:** Book's definition: "A module is a cohesive set of code that implements a unit of functionality."

**Real-world examples:**
- **Java** — modules compile as JAR files; multiple JARs bundle into a WAR; multiple WARs + JARs bundle into an EAR (Jakarta EE). Spec encouraged loose coupling but in practice devolved into BBoM through tight class-level coupling and absent package versioning.
- **Eclipse IDE** — every feature is a plugin (JAR + manifest `plugin.xml`). Plugins registered at runtime via an in-memory plugin registry. Evolved to OSGi bundles in Eclipse 3.0 to fix shared-nested-jar isolation. OSGi enforces explicit exports/imports with version ranges.
- **Firefox** — original architecture used XPCOM (Mozilla's cross-language component model, similar to COM/CORBA). All internal capabilities were XPCOM components; third-party add-ons could touch nearly all internals. Performance (parameter marshaling) and tight coupling to internals led to a 2016 rewrite using **HTML + CSS + JavaScript + WebExtensions API** + a JSON manifest — same technologies used for web pages.

*Ref: "Modular Monolith" (Chapter 2).*

---

### 9. Distributed Architecture — When You Need Independent Scaling and Failure

**Principle:** Promote modules to services when the application must (a) scale parts independently, (b) fail parts independently, or (c) be deployed/built by teams that can't easily coordinate.

**Do:**
- Structure each service as a coherent, ready-to-use software component that provides one unit of domain functionality.
- Define coarse-grained APIs (Session Facade, Remote Facade) — fine-grained object calls across the network kill performance.
- Use remote invocation (gRPC, REST) or messaging (RabbitMQ, Kafka Event Backbone) for service-to-service communication.
- Plan for independent scaling, independent failure, independent deployment from day one.
- Co-locate multiple services on the same computer when warranted; split across computers when scaling/failure isolation demands it.
- Build a database per service (Database per Service pattern) — avoid a shared central DB.
- Use distributed computing patterns: Publisher–Subscriber, Presentation–Abstraction–Control, Message Channel, Message Endpoint, Message Translator, Message Route, Client Request Handler.

**Don't:**
- Distribute objects naïvely — Martin Fowler's First Law of Distributed Object Design: "Don't distribute your objects!"
- Expect a distributed application to run faster than a monolith by default — network roundtrips and serialization add overhead.
- Share a single centralized database across services; it becomes a bottleneck and single point of failure.
- Use fine-grained RPCs across services (chatty interfaces, large serialized objects).
- Implement your own service discovery, retry, or distributed coordination — use the platform's primitives.
- Assume microservices = distributed; *all* microservices are distributed, but not all distributed systems are microservices.

**Code/Concept:**
> "A service is a coherent, ready-to-use software component that is designed to provide a unit of domain functionality. Services are modules that clients access through APIs that encapsulate and hide the underlying implementation and technology."
>
> "Making an application distributed does increase design complexity by introducing challenges such as concurrency, failure handling, and crosscutting concerns such as performance, logging, security, debugging, and testing."

**Real-world examples:**
- **Airline reservation system** — browsing, purchasing, and frequent-flier workloads have ~10× different scaling needs. Monolith forces you to scale for the busiest part (browsing) and redeploy all of it together. Splitting into Shopping, Reservation, and FrequentFlier services lets each scale on its own curve.
- **AJAX + Node.js** — the modern web browser + Node.js server pattern is itself a Distributed Architecture. Browser JavaScript uses `XMLHttpRequest` (standardized by W3C in 2008) to call back-end Node.js services, usually over JSON.
- **VSCode** — built on Electron (embedded Chromium + Node.js), it runs as multiple processes. The Developer Tool (hosting the code editor) is separated from the **Language Server** for each language. They communicate over the **Language Server Protocol** (a JSON-RPC specialization), enabling features like real-time diagnostics for any language with a server.
- **Eclipse Theia** — distributed cloud IDE with separate Front-End and Back-End. Supports three deployment styles: local Electron, Web Client + remote Back-End, local Electron Front-End + remote Back-End. Adopted the Language Server Protocol from VSCode.

*Ref: "Distributed Architecture" (Chapter 2).*

---

### 10. Cloud-Native Architecture (Root Pattern) — The Application/Services Split

**Principle:** A cloud-native application is split into two halves: a custom **application** (domain logic) and reusable **services** (state, infrastructure capabilities). The split enables mobility, independent scaling, polyglot development, and reuse.

**Do:**
- Implement custom user requirements in the application half.
- Delegate stateful, reusable functionality to backend services from the platform's catalog or from third-party vendors.
- Allow the application to be implemented in almost any language (Java, Node.js, Python, Go, …) independently of the services.
- Run a Client Application outside the cloud to consume the Service API.
- Keep the application small, simple, and movable — it should run on any computer as long as it can reach its services and clients.

**Don't:**
- Reimplement database, workflow, messaging, or auth functionality in the application half.
- Couple the application's lifecycle to a specific middleware server.
- Require a specific OS version or hardware model.
- Try to install custom middleware on a VM and call it "cloud-native."

**Code/Concept:**
> "Structure the application with a cloud-native architecture by implementing the custom domain logic in an application separate from the reusable services."
>
> "Separating the application from its middleware facilitates mobility within the cloud. The application is smaller and easier to deploy. It can run on a simple server without having to first install middleware on that server. The application and its services can move around independently."

*Ref: "Cloud-Native Architecture" (Chapter 3).*

---

### 11. Application Package — Encapsulation for Mobility

**Principle:** Package the application with *everything it needs to run* (code + libraries + config) into a single immutable artifact that deploys into a language runtime.

**Do:**
- Choose a language with a runtime environment (Java/JVM, Node.js, Python, Go) so the program is portable across OSes.
- Use a package manager (Maven/Gradle for Java, NPM for Node.js) to assemble the artifact from an explicit dependency manifest.
- Make the package immutable — build once, deploy many times.
- Build container/VM images *from* the application package for even simpler deployment.
- Use polyglot development — each service can be in its own language with its own package.
- Read the Twelve-Factor Dependencies rule: declare all dependencies completely and exactly.

**Don't:**
- Use a language without a separate runtime (assembler, C, C++, shell scripts) if you want cloud portability.
- Hardcode system paths or assume system-wide packages.
- Embed the application package in a "fat installer" that mutates the host OS.
- Mutate the package between environments — that's what External Configuration is for.

**Code/Concept — Java:**
```xml
<!-- Maven pom.xml fragment -->
<dependencies>
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>money-converter</artifactId>
    <version>1.0.0</version>
  </dependency>
</dependencies>
```
Run `mvn clean compile` then `mvn package` to produce a deployable JAR.

**Code/Concept — Open Liberty `server.xml`:**
```xml
<server description="Sample Liberty server">
  <featureManager>
    <feature>restfulWS-3.0</feature>
    ...
  </featureManager>
  ...
</server>
```
Build from `openliberty-kernel` and let the build load only the features declared — the server is as small as the app needs.

**Code/Concept — Node.js `package.json`:**
```json
{
  "dependencies": {
    "upper-case": "^2.0.0",
    ...
  },
  ...
}
```
NPM packages the program with declared libraries; Node runs the package without needing registry access at runtime.

*Ref: "Application Package" (Chapter 3).*

---

### 12. Service API — The Client/Server Wall

**Principle:** Expose application functionality as a *web-service-based service API* (coarse-grained tasks over HTTP), so clients and servers can evolve independently and traverse the Internet.

**Do:**
- Use a Facade-style API: define coarse-grained tasks, not fine-grained methods.
- Pass claim checks (unique IDs) instead of large serialized objects across the network.
- Choose HTTP as the transport; REST with OpenAPI/Swagger is the prevailing standard, gRPC is the leading RPC alternative.
- Treat the API as a contract — implementers and consumers coordinate on the schema, not the implementation.
- Use the Twelve-Factor Port-Binding rule: the app exports HTTP by binding to a port.
- Hide implementation details so providers can refactor without breaking clients.

**Don't:**
- Expose fine-grained OO APIs over the network — chatty, slow, fragile.
- Try to share pointers between processes; marshal by value or pass IDs.
- Use SOAP WSDL interfaces for new services unless integrating with existing SOAP infrastructure.
- Use DCOM, CORBA, Java RMI, or .NET Remoting — they don't traverse the Internet well.
- Let the API drift silently — version it deliberately.

**Code/Concept — Java interface (local):**
```java
import java.math.BigDecimal;
import java.util.Currency;

public interface MoneyConverter {
    public BigDecimal convert(BigDecimal amount, Currency from, Currency to);
}
```

**Code/Concept — Java implementation:**
```java
import java.math.BigDecimal;
import java.util.Currency;

public class MyConverter implements MoneyConverter {
    public BigDecimal convert(BigDecimal amount, Currency from, Currency to) {
        /* Code that converts the amount from one currency to another */
    }
}
```

**Code/Concept — JAX-RS web service exposing it:**
```java
import javax.ws.rs.*;
import javax.ws.rs.core.*;

@ApplicationPath("/api")
public class RestApplication extends Application { }
```
```java
import java.math.BigDecimal;
import java.util.Currency;
import javax.ws.rs.*;
import javax.ws.rs.core.*;

@Path("/currency")
public class CurrencyResource {
    @POST
    @Path("/convert/")
    @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
    @Produces(MediaType.TEXT_PLAIN)
    public String convert(@FormParam("amount") String amount,
                          @FormParam("from") String from,
                          @FormParam("to") String to) {
        BigDecimal unconvertedMoney = new BigDecimal(amount);
        Currency originalCurrency = Currency.getInstance(from);
        Currency newCurrency = Currency.getInstance(to);
        BigDecimal convertedMoney;
        MoneyConverter myConverter = new MyConverter();
        convertedMoney = myConverter.convert(unconvertedMoney, originalCurrency, newCurrency);
        return convertedMoney.toString();
    }
}
```

**Code/Concept — Go interface:**
```go
type MoneyConverter interface {
    Convert(amount Float, from Currency, to Currency) Float
}
```

**Code/Concept — OpenAPI 3.0 contract:**
```yaml
openapi: 3.0.0
...
paths:
  /convert:
    post:
      description: Convert money from one currency to another
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - amount
                - from
                - to
              properties:
                amount:
                  type: number
                from:
                  type: string
                to:
                  type: string
      responses:
        '200':
          description: Successfully converted the currency
          content:
            application/json:
              schema:
                type: number
```

*Ref: "Service API" (Chapter 3).*

---

### 13. Stateless Application — State Lives Elsewhere

**Principle:** The application program stores *no* domain state in memory and *no* session state between requests. Domain state lives in backend services; session state lives in the client.

**Do:**
- Keep all domain state in databases (or other backend services).
- Pass session state as request parameters from the client (cookies, JWT, request body).
- Keep transactions brief and persist at the end of each one — minimize the in-flight data loss window.
- Use temporary variables inside methods, not instance variables — they're thread-local and disappear with the thread.
- Use a backend caching service (Redis, Memcached) if you must cache, instead of an in-memory cache that breaks replicas.
- Design the API with few, simple parameters to limit session state needed.
- Quiesce in-flight transactions before shutting down — no state to flush, just wait for current requests.

**Don't:**
- Cache domain data in instance variables, singletons, or class-level maps.
- Use sticky sessions (JSESSIONID-style) — it's a Twelve-Factor violation.
- Use stateful session beans (EJB) or HTTP session objects for cross-request state.
- Keep uncommitted changes around "for performance" — every crash becomes data loss.
- Long-running transactions — they expand the RPO window.

**Code/Concept — stateful (anti-pattern):**
```java
public class ProductManager {
    private Map<Product> products; // products in cache

    private Database getDatabase() {
        Database database;
        database = /* Get the database connection */;
        return database;
    }

    public getProductNamed(String name) {
        Product product = products.getOrDefault(name, null);
        if (product == null) {
            product = this.getDatabase().get(name);
            products.put(product.name(), product);
        }
        return product;
    }
}
```

**Code/Concept — stateless (preferred):**
```java
public class ProductManager {
    // Do NOT declare a products instance variable.

    private Database getDatabase() {
        Database database;
        database = /* Get the database connection */;
        return database;
    }

    public getProductNamed(String name) {
        Product product = null; // products is a local variable, not an instance variable
        product = this.getDatabase().get(name);
        return product;
    }
}
```

> "What makes an application stateless is not that it has no state but that it stores its state elsewhere, which makes it more scalable and resilient."

*Ref: "Stateless Application" (Chapter 3).*

---

### 14. Replicable Application — Scale and Survive by Being Redundant

**Principle:** Run the application as N equivalent replicas so capacity grows with computers and failure of one computer doesn't take down the app. Avoid anything that ties a replica to a specific identity.

**Do:**
- Run multiple stateless replicas — they're all equivalent, any can serve any request.
- Coordinate replicas through shared Backend Services (databases, caches), not direct inter-replica calls.
- Use the cloud platform's native replication primitives: EC2 Auto Scaling, Kubernetes ReplicaSet, Azure Functions auto-scale, IBM Cloud Auto Scale.
- Trust horizontal scaling: each replica runs on its own computer, providing combined capacity.
- Fail safely: when a computer dies, only its replicas fail; the rest keep serving.
- Scale in by killing *any* replica — they're all equivalent.

**Don't:**
- Use the Singleton pattern — multiple replicas each create their own, defeating the purpose.
- Use fixed IP addresses or hard-coded hostnames that only one replica can claim.
- Use shared block storage — block volumes typically can't be shared across workloads.
- Create per-replica local disk storage for state — when the replica dies, the data dies.
- Open a connection pool per replica when the downstream SoR has a fixed connection limit (e.g. 10 connections × 10 replicas = 100 connections, kills the SoR).
- Manage a shared, distributed lock manually — use the platform's coordination primitives.

**Code/Concept — the connection-pool trap and fix:**
> "When an application accesses an SoR, typically the SoR can only handle a limited number of concurrent connections, any more than that and it crashes. If the SoR can only handle ten concurrent connections, then the application creates a connection pool with ten connections… The problem with running multiple replicas of the application is that each one creates its own connection pool, each with ten connections."

**Fix:** put an integration service (IBM App Connect Enterprise, MuleSoft) between the replicas and the SoR; the integration service owns and shares one connection pool. *Ref: "Replicable Application" — "Manage a connection pool using an integration service" (Chapter 3).*

> "For an application to be replicable, avoid anything that fits the Singleton pattern (Gamma, 1993), where an object has only a single instance that cannot be replicated and must be shared globally. Avoid any design details that mean the application can only run as a single workload and therefore on a single computer, such as components with shared memory, concurrency semaphores, or a fixed IP address or domain name."

*Ref: "Replicable Application" (Chapter 3).*

---

### 15. External Configuration — Build Once, Deploy Anywhere

**Principle:** Store all environment-specific values (endpoints, credentials, feature flags) *outside* the application artifact, in environment variables that the deployment process sets per environment.

**Do:**
- Use environment variables (OS-agnostic, language-agnostic) as the canonical config store.
- Keep the application package immutable across environments; only the env vars change.
- Store sensitive values in a secrets vault (HashiCorp Vault, AWS Parameter Store, IBM Cloud Secrets Manager, Azure Key Vault, HSM).
- Use Kubernetes `ConfigMap` (non-sensitive) and `Secret` (encoded) for containerized deployments.
- Split sensitive/non-sensitive into two files: only the non-sensitive file goes to SCM; sensitive goes to a vault.
- Set per-environment endpoints (dev DB URL, prod DB URL) so the same artifact works in dev, test, stage, prod.
- Use the Twelve-Factor Config rule verbatim.

**Don't:**
- Hardcode literals into source code (creates SCM-coupled secrets, can't move between envs).
- Bundle a properties file with the application — that's still in the artifact.
- Check secrets into source control; if you must, encrypt with `git-crypt` or similar.
- Store config in the same database the app reads its data from (chicken-and-egg: app needs config to connect to the config DB).
- Mutate the application package between environments — that's the whole point of externalizing.

**Code/Concept — Java, reading all env vars:**
```java
Map<String, String> env = System.getenv();
for (String envName : env.keySet()) {
    System.out.format("%s=%s%n", envName, env.get(envName));
}
```

**Code/Concept — Java, reading one env var:**
```java
String name = "PORT";
String value = System.getenv(name);
if (value != null) {
    System.out.format("%s=%s%n", name, value);
} else {
    System.out.format("%s is" + " not assigned.%n", name);
}
```

**Code/Concept — Node.js, reading all env vars:**
```javascript
const process = require('process');
var env = process.env;
for (var key in env) {
    console.log(key + ":\t\t\t" + env[key]);
}
```

**Code/Concept — Node.js, reading one env var:**
```javascript
const app = require('http').createServer((req, res) => { ... });
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
```

**Code/Concept — Kubernetes ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  # property-like keys; each key maps to a simple value
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"
```

**Code/Concept — Kubernetes Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  USER_NAME: YWRtaW4=
  PASSWORD: MWYyZDFlMmU2N2Rm
```

> "Env vars are easy to change between deploys without changing any code; unlike config files, there is little chance of them being checked into the code repo accidentally; and unlike custom config files, or other config mechanisms such as Java System Properties, they are a language- and OS-agnostic standard." — *12factor.net Config*

*Ref: "External Configuration" (Chapter 3).*

---

### 16. Backend Service — Reuse by Remote Delegation

**Principle:** Delegate reusable functionality (DBs, caches, queues, workflow engines, key vaults, monitoring) to **backend services** that run as separate processes the application connects to over the network.

**Do:**
- Pick a separate process per service so the application can scale independently of the service and vice versa.
- Choose services from the cloud platform's catalog or third-party SaaS when possible (buy vs. build).
- Use application services (the app calls directly: DB, queue) and platform services (the app doesn't call directly: observability, KMS) deliberately.
- Verify each service's SLA matches your reliability/security requirements.
- Document whether each service is single-tenant or multi-tenant.
- Use polyglot backend services — the app and the service can be in different languages.

**Don't:**
- Embed a reusable capability as a code library when it should be a service — libraries share the app process, can't scale independently, can't fail independently.
- Run an embedded DB (Derby, SQLite, eXtreDB) when a DB should be a shared service.
- Assume every backend service has good multi-region/data-sovereignty story.
- Build a service catalog yourself when the cloud platform already has one.

**Code/Concept — service categories and real examples:**

*Application services (app calls directly):*
- **Databases** — Amazon RDS (relational), Amazon DocumentDB (document), Azure Cosmos DB, Azure Cache for Redis, IBM Db2 on Cloud, IBM Cloudant.
- **Object storage** — Amazon S3, Azure Storage, IBM Cloud Object Storage.
- **Messaging** — Kafka, Amazon MSK, Azure Event Hubs, IBM Event Streams, RabbitMQ, Apache ActiveMQ, IBM MQ on Cloud, Azure Service Bus, Amazon MQ.
- **Integration** — IBM App Connect, IBM App Connect on IBM Cloud.
- **API gateway** — Amazon API Gateway, Azure API Management, IBM API Connect.

*Platform services (app doesn't call directly):*
- **Security** — Azure Key Vault Managed HSM, AWS KMS, IBM Cloud Hyper Protect Crypto Services.
- **Authentication** — IBM Cloud App ID, Azure Front Door.
- **Observability** — Prometheus (monitoring), Fluentd (log aggregation).
- **Secrets** — HashiCorp Vault, IBM Cloud Secrets Manager, AWS Systems Manager Parameter Store.

> "While cloud applications can embed reusable code libraries the way a traditional IT application can, they gain even greater flexibility by being able to connect to backend services remotely. A cloud application can even reuse other applications by treating them as backend services."

*Ref: "Backend Service" (Chapter 3).*

---

### 17. Microservices Architecture — Preview (Root Pattern: Microservice)

**Principle:** Treat a complex cloud application as a collection of small, focused, independently deployable services — each a tiny cloud-native app in its own right.

**Do:**
- Decompose by domain responsibility, not by technical layer.
- Make each service independently deployable and scalable.
- Use the six cloud-native patterns *inside* each microservice (Application Package, Service API, Stateless, Replicable, External Configuration, Backend Service).
- Design for independent failure — one service's crash must not cascade.
- Embrace polyglot development — different services in different languages is fine.

**Don't:**
- Conflate "microservices" with "many small services that all share a central DB."
- Start with microservices on a brand-new, poorly understood domain — Modular Monolith first.
- Build microservices without first mastering the cloud-native basics.

**Code/Concept:** Book's framing (from Introduction): "Chapter 4: Microservices Architecture… breaks up a monolithic application into multiple components, to improve reliability of each component and to simplify the development and testing of each component. Each component is a microservice–a small, specialized cloud-native application." *Ref: Introduction — "Organization of This Book" / Table I-1.*

> The Early Release does not yet contain Chapter 4; the principles above are stitched together from the Introduction's chapter summary and the Table I-1 root pattern list. Use the published *Microservices Patterns* (Chris Richardson, 2018) for implementation patterns until Ch 4 ships.

---

### 18. Microservice Design — Preview (Root Pattern: Model around Domain)

**Principle:** Discover microservice boundaries by analyzing how users actually interact with the application — domain events, use cases, business capabilities — not by technical layer or table ownership.

**Do:**
- Use Domain-Driven Design (Evans, 2003) bounded contexts as the starting point.
- Look for *well-encapsulated responsibilities* and the seams between them.
- Co-locate a service's data with the service (Database per Service).
- Use the BBoM → Modular Monolith → Distributed evolution: extract services only when there's a real reason (scaling, team, deploy cadence).

**Don't:**
- Decompose by technical layer (one service for UI, one for DB, one for "logic") — that re-creates a distributed monolith.
- Decompose too early — Microservice overhead is real.
- Use code-size alone as the criterion for extraction.

**Code/Concept:** Book's framing: "How can developers design one big application as many small applications that each perform a separate responsibility? Analyze interactions with the application to discover where one well-encapsulated responsibility ends and another begins." *Ref: Introduction — "Organization of This Book" / Table I-1.*

---

### 19. Event-Driven Architecture — Preview (Root Pattern: Reactive Component)

**Principle:** Some collaboration is best expressed by *reacting to events*, not by *orchestrating explicit calls*. Use Event-Driven Architecture when relationships are dynamic, ad hoc, or scale beyond a small set of participants.

**Do:**
- Use an **Event Backbone** (Kafka, Event Hubs, Event Streams, RabbitMQ) as the shared backend service.
- Model services as Reactive Components that emit and consume events.
- Prefer choreography (no central orchestrator) when services are loosely coupled and you want independent teams.
- Use orchestration (a Service Orchestrator) when a workflow has clear sequencing and central policy.

**Don't:**
- Use orchestration for *every* interaction — central orchestrators become bottlenecks and single points of change.
- Use event-driven when a simple synchronous call is clearer and the failure modes are well understood.
- Couple consumers directly to producer implementations — go through the Event Backbone.

**Code/Concept:** Book's framing: "Some components interact indirectly through dynamically discovered relationships that are more easily modeled as choreography." *Ref: Introduction — "Organization of This Book" / Table I-1.*

> "An Event Backbone is a Backend Service. It connects event consumers to event producers, all of which use it as a shared Backend Service." — *Ref: "Backend Service" (Chapter 3).*

---

### 20. Cloud-Native Storage — Preview (Root Pattern: Cloud Database)

**Principle:** Use the right database for each set of data — don't force-fit everything into one relational "database of record." Pick from the platform's polyglot persistence catalog.

**Do:**
- Apply **Polyglot Persistence**: segment data into encapsulated sets and use the best storage tech per set.
- Choose a database that is scalable, reliable, and matches the data's structure and access pattern.
- Replicate the database the same way the application replicates — multiple computers, multiple zones.
- Use the cloud platform's managed DB services instead of running your own.

**Don't:**
- Force every dataset into a single relational schema.
- Run your own DB when the cloud platform has a managed equivalent.
- Treat the DB as part of the application's process; treat it as a separate backend service.

**Code/Concept:** Book's framing: "A cloud platform typically includes a variety of Cloud Databases, each of which is optimized for a particular data structure and usage, so an application can take advantage of Polyglot Persistence to segment data into encapsulated sets and store each set of data in the storage technology that works best for that data." *Ref: "Cloud Application" (Chapter 1).*

---

### 21. Cloud Application Clients — Preview (Root Pattern: Client Application)

**Principle:** Cloud applications run in the cloud, but their users do not. Provide a Client Application that fits the user's device, not the server's stack.

**Do:**
- Support web browsers, mobile apps, and even other applications as clients.
- Treat the **Service API** as the contract; pick the thinnest client that can call it.
- Use the same Service API across clients to avoid duplicating server logic.
- For rich UX, use thick clients or native apps that consume the same API.

**Don't:**
- Build a desktop-only thick client when the user only has a phone.
- Duplicate business logic in the client (or worse, in multiple clients).
- Hardcode transport assumptions that only work on one device type.

**Code/Concept:** Book's framing: "Users need to be able to access the cloud application from the device they're using, via user interfaces that are simple to install and update, and that support an increasingly wide-variety of device types." *Ref: Introduction — "Organization of This Book" / Table I-1.*

> "The client application can be a web browser, mobile app, or even a kiosk or a chatbot." — *Ref: "Cloud-Native Application" (Chapter 3).*

---

### 22. Application Migration & Modernization — Preview

**Principle:** Modernizing a traditional IT application for the cloud is best done incrementally. Match the strategy to the application's condition and your team's appetite for risk.

**Do:**
- Choose the lightest-touch strategy that gets you the cloud benefits you need:
  - **Lift and Shift** — rehost as-is.
  - **Virtualize the Application** — package into a VM image.
  - **Containerize the Application** — package into a container.
  - **Refactor the Monolith** — extract modules / services.
  - **Start Small and Pave the Road** — pick a low-risk workload first.
- Use Strangler Application patterns (Ch 10) to modernize while still in production.
- Demo quick wins (Lift and Shift) before betting on deep refactors.

**Don't:**
- Do a "big bang" rewrite from monolith to microservices on a production-critical system.
- Skip the cloud-native patterns when replatforming — a containerized monolith still isn't cloud-native.
- Refactor the monolith before replatforming if replatforming itself is unproven in your org.

**Code/Concept:** Book's framing: "Strategies include Lift and Shift, Virtualize the Application, Containerize the Application, and Refactor the Monolith. Cloud applications can be developed from scratch, but often they start as traditional IT applications that the enterprise later decides to host on cloud." *Ref: Introduction — "Organization of This Book".*

> "It is best to Start Small and Pave the Road when you are migrating and modernizing existing applications to run in the cloud."

---

### 23. Strangling the Monolith — Preview (Root Pattern: Strangler Application)

**Principle:** Incrementally extract functionality from a running monolith into new cloud-native services, routing a fraction of traffic to the new component each time, until the monolith is "strangled."

**Do:**
- Keep the monolith running while you extract.
- Use an edge / API gateway to route requests — old to the monolith, new to the replacement service.
- Extract one capability at a time.
- Retire the monolith once it has nothing left.

**Don't:**
- Stop the monolith and rewrite in one go.
- Extract without a routing story — you'll never get clean cutovers.
- Try to extract everything at once.

**Code/Concept:** Book's framing: "A traditional IT application can be updated for the cloud in one big bang, but a complex application that is already running in production can be converted more easily by doing so incrementally. The trick is to keep the application running when it is half traditional IT and half cloud." *Ref: Introduction — "Organization of This Book" / Table I-1.*

---

### 24. Modern Application Development Practices

**Principle:** Adopt these four practices — they shape the architecture decisions in this book.

**Do:**
- **Modular code** with two-pizza teams (6–12 people) per module.
- **Polyglot development** — different modules in different languages when it helps.
- **Incremental development** — small batches in 1–4 week sprints; deconstruct big changes.
- **Continuous delivery** — ship bug fixes and features to production quickly after they're ready.
- **Automated builds** — CI/CD pipelines that build, test, and deploy on every change.
- Wire evidence collection into CI/CD for compliance audits.

**Don't:**
- Wait months between releases; long gaps usually mean no one is using the code.
- Force a single language across all modules.
- Treat CI/CD as a deploy tool only — it's also a quality gate and evidence collector.

**Code/Concept:**
> "When code in production hasn't been updated in weeks or months, it apparently must have no bugs and the users don't want any improvements, which probably means no one is using this functionality."
>
> "An important part of achieving continuous delivery — making code improvements frequently and available to users as soon as possible — is running code changes through the pipeline as soon as they're available. In addition, CI/CD pipelines can be instrumented with automated evidence collection to provide auditors and security teams with significant pipeline events and results that might be needed for enterprise or regulatory compliance."

*Ref: Introduction — "Modern Application Development".*

---

### 25. Cloud Computing Characteristics vs. Traditional IT (Comparison Map)

**Principle:** Use this map as a translation table whenever someone proposes a traditional-IT design in a cloud context.

| Traditional IT assumption | Cloud reality | Implication for the app |
|---|---|---|
| 100% reliable hardware | Commodity, unreliable | App must be more reliable than its infra |
| ACID transactions | Eventual consistency | Use simple, independently failing transactions |
| Specific hardware/OS | Generic, evolving | Infrastructure-neutral |
| Stationary workload | Movable for balance/DR | Portable artifact |
| Single-tenant host | Multitenant host | Isolate, share resources |
| Vertical scaling | Horizontal scaling | Many equivalent replicas |
| Stateful in-memory | Stateless workload | Store state in backend services |
| Patchable | Immutable releases | Redeploy, don't patch |
| Monolithic process | Componentized | Limited interdependencies |
| Custom middleware | Service catalog | Delegate to backend services |
| One relational DB | Polyglot persistence | Pick the right DB per data set |
| Central ops provisioning | Self-service provisioning | Team provisions its own environment |

*Ref: "Cloud computing practices" (Chapter 1).*

---

### 26. Fallacies of Distributed Computing — Why Service APIs Are Hard

**Principle:** Every remote call is a network call. Plan for the eight fallacies; don't fall for "it's just a function call."

**Do:**
- Assume the network is reliable — *no, design retries and idempotency.*
- Assume latency is zero — *no, batch and coarsen.*
- Assume bandwidth is infinite — *no, minimize payload.*
- Assume the network is secure — *no, encrypt and authenticate.*
- Assume topology won't change — *no, discover services dynamically.*
- Assume there will be one admin — *no, automate.*
- Assume transport cost is zero — *no, this is money and time.*
- Assume the network is homogeneous — *no, build to standards.*

**Don't:**
- Use fine-grained OO APIs over the network.
- Pass large serialized objects as parameters.
- Use pass-by-reference semantics across processes.
- Depend on a single fixed hostname/IP for service discovery.

**Code/Concept:** Martin Fowler's First Law of Distributed Object Design: **"Don't distribute your objects!"** *Ref: "Service API" (Chapter 3).*

---

### 27. The Pattern Language — How to Use It

**Principle:** The book is a *pattern language*, not a sequence. Read root patterns first, then follow links.

**Do:**
- Start with the root pattern of each chapter (Table I-1): Cloud Application, Cloud-Native Architecture, Microservice, Model around Domain, Reactive Component, Cloud Database, Client Application, Strangler Application.
- Use the *Context* and *Related Patterns* sections to navigate, not the page order.
- Apply the patterns in the order that solves *your current biggest problem* — not chapter order.
- Treat Chapter 2 as optional context, not prerequisite, if you're focused on cloud-native.

**Don't:**
- Read straight through like a novel without jumping.
- Skip the related-patterns sections — they're the connective tissue.
- Treat the book as a tutorial; it's a pattern language (Christopher Alexander's "A Pattern Language", "A Timeless Way of Building").

**Code/Concept:**
> "A pattern language is a set of related patterns that shows how the patterns are interconnected, how they fit together to form a whole greater than the sum of the parts, and how each pattern leads to others."

> "Following these pattern links will eventually lead to most of the book, though often not in page or chapter order."

*Ref: Introduction — "Patterns and Pattern Format" / "Organization of This Book" / "Getting Started".*

---

### 28. Naming Patterns & Their Canonical Sources

**Principle:** When citing one of these patterns or anti-patterns, use the book's name and the canonical reference. The book references a rich external library; honor it.

**Do:**
- Cite by book name + chapter heading: *Ref: Cloud_Application_Architecture_Patterns_ER.md — "Big Ball of Mud"*.
- Credit external origins:
  - **BBoM** — Foote & Yoder, PLoP 1997 / PLOPD4 (Addison-Wesley, 2000).
  - **Big Ball of Mud cleanup** — Foote & Yoder: Shearing Layers, Sweep It Under The Rug, Reconstruction.
  - **Sustaining patterns** — Wirfs-Brock & Yoder (PLoP 2012): Paving Over The Wagon Trail, Wiping Your Feet At The Door.
  - **Antipatterns** — Brown, Malveau, McCormick, Mobray (1998).
  - **Legacy code** — Feathers (2005).
  - **Worse is Better** — Gabriel (dreamsongs.com/WorseIsBetter.html).
  - **Make it work / right / fast** — Beck, *Smalltalk Best Practice Patterns* (1997).
  - **Modules / cohesion & coupling** — Constantine & Yourdon, *Structured Design* (1979).
  - **Design Patterns** — Gamma, Helm, Johnson, Vlissides (1995).
  - **POSA Vol 1–4** — Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996); Buschmann, Henney, Schmidt (2007).
  - **Domain-Driven Design** — Evans (2003).
  - **Microservices Patterns** — Richardson (2018).
  - **Fallacies of Distributed Computing** — L Peter Deutsch; Fowler's summary.
  - **Alexander** — *A Pattern Language* (1977), *The Timeless Way of Building* (1979).

**Don't:**
- Invent new pattern names when a canonical one already exists.
- Use a pattern without acknowledging its source community.

*Ref: All chapter reference sections (Chs 1–3 References; Introduction Acknowledgements).*

---

### 29. Service-Oriented Architecture (SOA) — The Ancestor

**Principle:** SOA is the historical parent of both Web Services and Microservices. Understand the lineage so you can talk fluently to architects of all generations.

**Do:**
- Recognize SOA's client/server split inside the server: components as service providers/consumers.
- Recognize that microservices = SOA principles reapplied with cloud-native assumptions.
- Reuse the SOA vocabulary (service provider, service consumer, service contract) when integrating with legacy systems.

**Don't:**
- Treat SOA and microservices as the same thing — microservices add per-service deployment, scaling, and ownership.
- Dismiss SOA-era patterns out of hand; many survive intact.

**Code/Concept:**
> "Service-oriented architecture (SOA) applied the client/server architecture to the server application, dividing it into components that perform work for other components." — *Ref: Introduction — "Evolution of Application Architecture".*

---

### 30. Anti-Patterns & Common Mistakes — Distilled

**Principle:** The book is a pattern book, but the practices imply specific anti-patterns. Name them to defend against them.

- **Singleton in a cloud app** — multiple replicas each get their own copy, defeating the purpose; loss of one replica's singleton crashes the others. *Fix:* eliminate the singleton; use shared backend services.
- **In-memory cache of domain data** — every replica caches its own copy, they go stale, graceful shutdown needs a full flush, crashes lose uncommitted changes. *Fix:* make the app stateless; use Redis/Memcached if you must cache.
- **Stateful session bean / HTTP session** — caps the number of concurrent users; needs sticky sessions; breaks when the platform moves replicas. *Fix:* stateless services; client passes session context per request.
- **Properties file for config** — gets committed to SCM, leaks secrets, can't deploy same artifact across envs. *Fix:* external config in environment variables + secrets vault.
- **Hardcoded IP address / hostname / fixed port** — only one replica can claim it. *Fix:* use the orchestrator's service discovery.
- **Shared block storage across replicas** — typically not shareable across workload processes; breaks equivalency. *Fix:* use a database backend service.
- **Centralized relational DB across all microservices** — bottleneck + SPOF + tight coupling. *Fix:* Database per Service; replicate data via events.
- **SOAP / DCOM / CORBA / RMI over the Internet** — don't traverse NAT/firewalls; need special ports. *Fix:* REST/OpenAPI over HTTP or gRPC.
- **Chatty OO API across services** — every property access = round trip. *Fix:* coarse-grained facade, pass IDs.
- **Lift-and-shift without cloud-native patterns** — runs on cloud, doesn't run *well* on cloud. *Fix:* replatform then refactor (or at minimum apply Stateless, Replicable, External Configuration).
- **Microservices from day one** — over-engineered for an evolving domain. *Fix:* start with Modular Monolith, distribute when you have a real reason.
- **Distributed Big Ball of Mud** — harder than a centralized one to clean up. *Fix:* don't let it devolve; enforce module boundaries; refactor in place.
- **Reimplementing what the service catalog gives you** — database, queue, auth, workflow. *Fix:* delegate to backend services.
- **A big-bang monolith-to-microservices rewrite in production** — downtime, regression risk, morale. *Fix:* Strangler Application.
- **Sticky sessions** — Twelve-Factor violation; prevents replicas from being interchangeable. *Fix:* stateless services + client-supplied session state.
- **Manual distributed locks / leader election in app code** — fragile, blocked on the leader when it dies. *Fix:* let the platform coordinate; use the Event Backbone or DB unique constraints.
- **Shared per-replica connection pool to a fixed-capacity SoR** — N replicas × M connections exceeds the SoR's limit, kills it. *Fix:* integration service owns a single shared pool.

---

## Decision Heuristics / Checklists

### When to use which application architecture?

- **BBoM** — only for prototypes, MVPs, exploratory programming, demos. Plan to refactor before it stabilizes.
- **Modular Monolith** — default starting point for any non-trivial business application that will live longer than a few months.
- **Distributed Architecture** — when you have any of: (a) parts that need to scale independently, (b) parts that must fail independently, (c) teams that must deploy independently.

### When to start microservices vs. Modular Monolith?

- Start **Modular Monolith** when the domain is still being discovered, the team is small (< ~6 teams), or you cannot yet articulate clear bounded contexts.
- Move to **Microservices** when bounded contexts are stable, independent scaling is real, or team topology demands independent deployments.

### When to use which cloud-native pattern?

- **Application Package** — always; every cloud-native app needs an immutable, portable artifact.
- **Service API** — always; every cloud-native app exposes a web-service API to clients.
- **Stateless Application** — always; persist domain state, let clients carry session state.
- **Replicable Application** — always; design for multiple replicas even if you run one today.
- **External Configuration** — always; env vars + secrets vault per environment.
- **Backend Service** — always; delegate data, messaging, workflow, auth, observability.

### When to use which database?

- **Relational (RDS, Db2, Cloud SQL)** — for highly structured, transactional, schema-strict data.
- **Document (DocumentDB, Cosmos DB, Cloudant, MongoDB)** — for semi-structured JSON-like data.
- **Key-value (Redis, Memcached, DynamoDB)** — for cache, session, fast lookups.
- **Object storage (S3, Azure Blob, IBM COS)** — for blobs, files, backups, static assets.
- **Search (Elasticsearch, OpenSearch)** — for full-text and faceted search.
- **Time-series (InfluxDB, Timescale)** — for metrics and events.
- **Graph (Neo4j, Cosmos DB Gremlin)** — for relationship-heavy traversals.

### Twelve-Factor Quick Self-Audit

- [ ] One repo per app; many deploys (I).
- [ ] All deps declared in manifest; no reliance on system packages (II).
- [ ] Config in env vars; nothing about the env in code (III).
- [ ] Backing services (DB, queue, cache) attached resources (IV).
- [ ] Strict build / release / run separation (V).
- [ ] One or more stateless, share-nothing processes (VI).
- [ ] Self-contained HTTP server via port binding (VII).
- [ ] Scale via process model (VIII).
- [ ] Fast startup, graceful shutdown, robust to crash (IX).
- [ ] Dev ≈ staging ≈ prod (X).
- [ ] Logs to stdout, treated as event streams (XI).
- [ ] Admin tasks run as one-off processes (XII).

### Code Migration Sanity Checklist

- [ ] Could you redeploy the same artifact to a new region by changing only env vars?
- [ ] Could you run three replicas behind a load balancer with no code changes?
- [ ] Could a fresh replica start with no shared state from existing replicas?
- [ ] Could you swap the database by changing only env vars?
- [ ] Could a developer run the same package locally with only a `.env` file?
- [ ] Are all dependencies declared in a manifest?
- [ ] Are secrets in a vault, not in the repo or the artifact?
- [ ] Is the client responsible for its own session state?

---

## Key Takeaways

1. **Cloud ≠ traditional IT.** Embrace unreliable hardware, eventual consistency, horizontal scaling, stateless workloads, immutability, and self-service provisioning — or your "cloud app" will just be a traditional IT app that happens to run on someone else's computer.
2. **Twelve-Factor is the floor, not the ceiling.** All twelve factors are the minimum bar for a cloud-native app; the six cloud-native patterns are the next layer up.
3. **Six cloud-native patterns, in concert.** Application Package + Service API + Stateless + Replicable + External Configuration + Backend Service — applied together produce a cloud-native app. Skipping any one erodes the others.
4. **Start with BBoM, then Modular Monolith, then Distributed.** Each is right at the right time. Don't jump to microservices for a brand-new domain.
5. **State is the enemy of cloud-native.** Domain state belongs in a backend service; session state belongs in the client. Anything else breaks scaling, recovery, and replication.
6. **Avoid singletons, fixed IPs, shared block storage, sticky sessions, and centralized databases across services.** Each is a quiet path back to the monolith.
7. **Reuse by remote delegation, not by library embedding.** A backend service can be in a different language, on a different computer, and scale independently of the application.
8. **Externalize config to env vars; secrets to vaults.** Never to a properties file in the repo, never baked into the artifact.
9. **Modernize incrementally.** Strangler Application keeps the monolith running while you peel it apart.
10. **Read this book as a pattern language, not a tutorial.** Start at the root pattern of the chapter you need; follow related-patterns links, not page numbers.

---

## Additional Patterns & Extended Coverage

The clusters above cover every section of the Early Release's available content (Chs 1–3 + Introduction). The clusters below extend the deep-dive with the architectural concerns that surround the book's six cloud-native patterns and three application architectures — the patterns the book explicitly gestures at (CI/CD, observability, security, deployment topology) and the operational concerns every reader of this book must layer on top.

### 31. Three-Tier Cloud Application (E-commerce Reference Architecture)

**Principle:** The canonical cloud-application shape is a three-tier arrangement: client tier, application tier (business logic + service API), and data tier (backend services + SoRs). The same shape serves radically different industries.

**Do:**
- Use the same three-tier shape for e-commerce, banking, healthcare, travel — only the domain logic changes.
- Treat the application tier as a small, focused cloud-native service that delegates everything else.
- Place payment, inventory, and other existing SoRs behind the application tier as backend services.
- Let multiple client types (web browser, mobile app, thick client) hit the same Service API.

**Don't:**
- Move the SoRs to the cloud just to "go cloud." Wrap them; modernize on their own schedule.
- Duplicate business logic across the three tiers.
- Let the client tier reach past the application tier into the data tier.

**Code/Concept — Three-tier structure for an e-commerce app:**
- **Client tier:** customer browser/mobile app + rep thick client.
- **Application tier:** cloud-hosted business logic for product catalog, shopping cart, checkout.
- **Data tier:** product catalog DB, warehouse inventory DB, orders DB.
- **Backend services used by app tier:** payment processing (SoR, PCI-compliant, often on-prem), warehouse inventory system (SoR, often on-prem).
- **Client apps the tier serves:** browser self-service, mobile self-service, rep thick client.

> "Whether the user is the customer buying products or a representative facilitating the purchase, the architecture for the cloud application is the same."

*Ref: "Cloud Application — E-commerce: Three-tier architecture" (Chapter 1).*

---

### 32. System of Engagement (SoE) over System of Record (SoR)

**Principle:** When SoRs can't move to the cloud, build an SoE in the cloud as a modern facade. The SoE scales, authenticates, and adapts the SoR for new clients; the SoR keeps doing the real work.

**Do:**
- Identify the SoR's limitations (limited concurrent connections, batch processing, legacy tech).
- Build the SoE as a thin facade that delegates business logic to the SoR.
- Use the SoE to manage a *small number* of pooled connections to the SoR and share them across many users.
- Use the SoE to unify multiple SoRs into one customer view (e.g. checking + savings + mortgage + credit).
- Build security into the SoE to protect the SoR from the public internet.

**Don't:**
- Let clients talk directly to the SoR — its concurrency model wasn't built for that.
- Re-implement business logic in the SoE; it's a facade, not a clone.
- Move the SoR's data into the SoE's database; keep SoR data in the SoR.

**Code/Concept — Banking SoE architecture:**
- **SoRs (on-prem, not moving):** checking system, savings system, mortgage system, credit-card system. Each may not know that one customer owns all of them.
- **SoE (in cloud):** unified facade that aggregates the customer's accounts, exposes them as REST APIs.
- **Clients served:** web browser, mobile app, ATMs, telephone voice prompts, Internet chatbots, bank tellers.

> "SoEs use modern technology–such as JSON and XML, web services, huge numbers of concurrent users. The SoE adapts the SoRs so users can access them as a unified, modern application."
>
> "Most SoRs were never designed to handle very many concurrent users, but SoEs scale to handle large numbers of users connecting at the same time over the Internet and internal networks, managing a small number of connections to the SoRs and sharing them amongst a large number of users."

*Ref: "Cloud Application — Banking: System of engagement" (Chapter 1).*

---

### 33. Cloud-Scale Job Management (HPC Reference Architecture)

**Principle:** When the workload is bursts of heavy compute (AI training, image analysis, simulations), upload jobs to the cloud rather than moving the data; pay only for what you use; let the cloud autoscale to thousands of concurrent jobs.

**Do:**
- Keep the data near the client (on-prem) and upload only jobs.
- Use serverless or auto-scaled compute to run jobs concurrently across many workers.
- Use multiple data centers / regions to maximize parallelism.
- Cache frequently-used inputs in cloud storage to avoid repeated uploads.
- Consider a replica of the on-prem DB in the cloud if most data is eventually processed there.

**Don't:**
- Move the data to the cloud long-term if access patterns are bursty — uploads get expensive.
- Run HPC workloads on dedicated always-on hardware when the cloud can autoserve them.
- Use a single shared cloud DB if your data sovereignty rules forbid it.

**Code/Concept — HPC architecture:**
- **Client app:** runs where the data lives (often on-prem data center), splits work into jobs.
- **Cloud:** receives each job, schedules it, runs it serverlessly, returns results.
- **Examples given:** AI image-triage on survey photos of terrain; enterprise analytics jobs.
- **Multi-tenancy:** multiple enterprises share the same cloud capacity; each pays only for what it submits.

> "Multiple enterprises can submit jobs to be managed, all sharing the cloud's capacity and each paying only for the capacity they use. The data is not stored in the cloud long-term, so access to it in the cloud is limited."

*Ref: "Cloud Application — Data analytics: Cloud-scale job management" (Chapter 1).*

---

### 34. Evolution of Application Architecture (Historical Context)

**Principle:** Today's cloud architecture is the latest step in a decades-long evolution. Knowing the lineage helps you predict what works and what doesn't.

**Do:**
- Use the mainframe → desktop → client/server → cloud-native lineage to frame trade-offs to stakeholders.
- Recognize that the cloud's structure is *structurally a client/server application*: server runs domain logic; client runs UI; backend services host shared state.
- Lean into the cloud's "mainframe-like compute capacity distributed across multiple server computers" with built-in SaaS services.

**Don't:**
- Treat the cloud as something completely new — it's an evolution of what came before.
- Dismiss cloud as "just someone else's computer" — virtualization, multitenancy, and self-service make it much more.

**Code/Concept — the four eras:**
- **Mainframe Application (1950s–1960s):** monolith on the mainframe; dumb terminals; dedicated short cables; limited I/O bandwidth.
- **Desktop Application (1970s–1980s):** monolith on each user's PC; LANs added file servers; no central app.
- **Client/Server Application (1990s):** DB server then app server emerged; thick clients did user-side work, server did shared work; "the network is the computer"; SOA split the server app.
- **Cloud-Native Application (2000s+):** generalized VMs; SaaS-ified everything (DB, workflow, messaging, auth); web browser as universal client; smartphones and tablets added more client types.

> "A cloud-native application is one written or modernized specifically for the cloud, to take full advantage of the cloud computing model."

*Ref: Introduction — "Evolution of Application Architecture".*

---

### 35. Web Service Protocol Evolution (SOAP → REST → gRPC)

**Principle:** Pick the protocol that matches your ecosystem. REST/OpenAPI is the prevailing default for public/web APIs; gRPC is the leading RPC alternative for service-to-service.

**Do:**
- Use REST + OpenAPI for public APIs and any client that needs simple HTTP tooling.
- Use gRPC for service-to-service RPC where schema evolution and streaming matter.
- Use the Twelve-Factor Port-Binding rule regardless of which protocol you pick.
- Reuse the same Service API across all client types.

**Don't:**
- Default to SOAP WSDL for new services — REST or gRPC almost always fits better.
- Use DCOM, CORBA, .NET Remoting, Java RMI for new cloud APIs.
- Force SOAP into a browser-centric ecosystem when you can use REST.

**Code/Concept:** SOAP used XML + WSDL like OO objects; REST uses HTTP URIs + methods (GET/PUT/POST/DELETE) + Swagger/OpenAPI; gRPC defines APIs as RPC with explicit schemas. All ride HTTP. *Ref: "Service API" (Chapter 3).*

---

### 36. Reliability Patterns for Cloud Apps (Preview of Ch 10 Themes)

**Principle:** The book's root patterns all converge on the same goal: a *more reliable application than its infrastructure*. Apply these design-level reliability techniques from day one.

**Do:**
- **Replicate the workload** so losing one computer loses only some replicas.
- **Replicate the data** via the chosen Cloud Database's replication primitives.
- **Fail fast** — set aggressive timeouts; don't let a hung call freeze the system.
- **Retry with backoff and jitter** for transient failures, but make handlers idempotent.
- **Circuit-break** on persistent downstream failures to avoid cascade.
- **Bulkhead** critical resources so one consumer can't exhaust the pool.
- **Use health checks** to let the orchestrator remove unhealthy replicas.
- **Quiesce** before shutdown — drain in-flight requests.

**Don't:**
- Rely on a single replica for availability.
- Use synchronous calls across service boundaries for critical-path work without a timeout.
- Retry non-idempotent operations blindly (causes duplicate side effects).
- Build your own service discovery when the platform provides one.

**Code/Concept:** Twelve-Factor IX (Disposability) lays the groundwork: "fast elastic scaling, rapid deployment of code or config changes, and robustness of production deploys." *Ref: "Replicable Application" (Chapter 3).*

> The book gestures at Ch 10 (Strangler) and these reliability concerns; the Early Release does not yet contain dedicated patterns for circuit breakers, bulkheads, retries, or health checks. Use *Microservices Patterns* (Richardson 2018) for implementation patterns until then.

---

### 37. Observability & Operations (Platform Services)

**Principle:** Wire the platform's observability services into every workload from the start. Treat them as platform services the app may not even know about.

**Do:**
- Emit metrics, structured logs, and traces using open standards (Prometheus, OpenTelemetry, Fluentd).
- Stream logs as event streams (Twelve-Factor XI) — never write to local files only.
- Use platform monitoring (Prometheus) and log aggregation (Fluentd) without modifying app code.
- Tag every replica with instance ID, version, region, zone for triage.

**Don't:**
- Couple observability to a single vendor SDK with no escape hatch.
- Store logs only on the workload's local filesystem — they die with the workload.
- Skip correlation IDs across services — they make distributed tracing useless.

**Code/Concept:** *Ref: "Backend Service — Observability services (platform service)" (Chapter 3).*

---

### 38. Security Patterns (Auth, Transport, Secrets)

**Principle:** Layer security: identity at the edge (auth service), mutual auth between services (mTLS), secrets at rest (vault/KMS), audit trail (logging).

**Do:**
- Delegate authentication to a platform service (IBM Cloud App ID, Azure Front Door, AWS Cognito) so the application doesn't implement it.
- Use mTLS between services for transport security and identity.
- Store secrets in a vault (HashiCorp Vault, IBM Cloud Secrets Manager, AWS Secrets Manager) — never in code or properties files.
- Encrypt at rest using a KMS (Azure Key Vault Managed HSM, AWS KMS, IBM Hyper Protect Crypto Services).
- Use OAuth2 + JWT for user identity federation; validate tokens at the edge.
- Add audit logging as a platform concern.

**Don't:**
- Reimplement authentication in every microservice.
- Use long-lived shared secrets between services.
- Store secrets in environment variables committed to the repo.
- Use plaintext protocols between services.

**Code/Concept:** Book's framing: a key vault is a backend service that stores cryptographic keys; KMS consumers retrieve them when needed. *Ref: "Backend Service — Security services (platform service)" (Chapter 3).*

---

### 39. Deployment Patterns (Containers, Orchestrators, Serverless)

**Principle:** Cloud platforms run three deployment shapes — VMs, containers, and serverless functions. Pick the simplest one that meets your needs.

**Do:**
- **Containerize** for portable, fast-starting, isolated workloads; use a Kubernetes-style orchestrator for multi-container apps.
- **Virtualize** when you need a full OS image or can't containerize (Windows GUI, legacy middleware).
- **Serverless** (Azure Functions, AWS Lambda) when the workload is event-driven and bursty.
- Build the application package once; deploy it into whichever shape fits.
- Use the platform's deployer — Kubernetes ReplicaSet, EC2 Auto Scaling, etc. — to manage replicas.

**Don't:**
- Use a VM when a container would suffice (slower start, more OS baggage).
- Use containers for workloads that benefit from serverless (long-idle, event-driven).
- Manage replicas manually when the orchestrator does it for you.

**Code/Concept:** Kubernetes ReplicaSet "guarantees the availability of a specified number of identical Pods." EC2 Auto Scaling "adds EC2 instances when demand spikes." *Ref: "Replicable Application" (Chapter 3).*

---

### 40. CI/CD & Continuous Delivery (Build / Release / Run)

**Principle:** Strictly separate build, release, and run stages (Twelve-Factor V). Make every change pass through a single automated pipeline.

**Do:**
- Treat build, release, run as three distinct, immutable stages.
- Automate build (compile + unit test + lint + security scan), release (artifact signing + version tagging), run (deploy to env).
- Run the pipeline on every commit; deploy to prod frequently.
- Use the same pipeline to emit compliance evidence for auditors.
- Make the pipeline reproducible from a clean machine.

**Don't:**
- Let humans touch prod directly.
- Recompile or re-package between environments — that violates External Configuration's immutability.
- Combine build and release — you lose rollback fidelity.

**Code/Concept:** "An automated system should build it into deployment artifacts, run automated tests on it, and ultimately deploy it into production. Frequent builds are known as continuous integration (CI) and frequent deployment is known as continuous deployment (CD). Together they're known as a CI/CD pipeline." *Ref: Introduction — "Modern Application Development".*

---

### 41. Modular Monolith Migration Path to Distributed

**Principle:** The transition from Modular Monolith to Distributed Architecture is *additive*: add a remote API and a process boundary to each module you want to distribute. Don't rewrite the modules.

**Do:**
- Start with a clean Modular Monolith (modules with explicit interfaces, no circular deps).
- For each module you want to distribute:
  1. Add a remote API (REST/gRPC) to the module.
  2. Package the module to run in its own runtime.
  3. Replace in-process calls with remote calls.
  4. Migrate the module's data ownership to a per-service DB.
  5. Deploy the module separately; test failure isolation.
- Extract modules one at a time.

**Don't:**
- Rewrite the module while extracting it — keep the implementation, change the boundary.
- Try to extract many modules in parallel — coordination cost will explode.
- Skip the data migration — a service that shares a DB isn't really a service.

**Code/Concept:** "A common way to create a Distributed Architecture is to transform each module in a Modular Monolith by augmenting it with a remote API and packaging it to run in its own separate runtime." *Ref: "Distributed Architecture — Transformation from Modular Monolith" (Chapter 2).*

---

### 42. Distributed Architecture Communication Discipline

**Principle:** The cost of every remote call is real. Treat the API contract as the design, not the implementation.

**Do:**
- Define coarse-grained task APIs (one round-trip = one logical operation).
- Pass claim checks (IDs) instead of full objects; load the object on the receiving side.
- Use asynchronous messaging when latency tolerance allows.
- Design APIs that are idempotent so retries are safe.
- Document the SLA and error model of every service.

**Don't:**
- Expose fine-grained OO methods across the network.
- Pass large serialized payloads; serialize is expensive.
- Block a critical-path request on a slow downstream call without a timeout.
- Reimplement service discovery, retry, or backoff yourself when the platform provides them.

**Code/Concept:** "An API should limit [roundtrips] by defining course-grained tasks that reduce the roundtrip interactions between the consumer and provider. (See Session Facade and Remote Facade.)" *Ref: "Distributed Architecture" (Chapter 2).*

---

### 43. Distributed Architecture Failure Discipline

**Principle:** Every remote call can fail. Plan for the failure modes of every cross-service interaction.

**Do:**
- Add timeouts on every remote call (short).
- Use circuit breakers for persistent downstream failures.
- Use bulkheads (separate connection pools, separate thread pools) per downstream.
- Retry with exponential backoff + jitter for idempotent operations.
- Use the transactional outbox + idempotent consumer pattern for cross-service consistency.
- Design for degraded modes (read-only, cached-only, fallback).

**Don't:**
- Let one slow downstream block the entire request thread.
- Retry forever — back off and eventually give up.
- Trust the network — assume every call can fail, time out, or duplicate.

**Code/Concept:** The book frames this implicitly through Stateless + Replicable + Backend Service: each service is replaceable because it's stateless and the data lives in a backend service. *Ref: "Stateless Application" + "Replicable Application" (Chapter 3).*

> The book does not yet (in the Early Release) contain dedicated patterns for circuit breaker, bulkhead, retry, or transactional outbox — they're implied by the failure-mode reasoning in Chs 1–3 and teased in the Conclusion.

---

### 44. Replicable Application — Capacity & Sizing

**Principle:** Match capacity to load by changing replica count, not replica size. Cloud platforms make this trivial; traditional IT sizing cannot.

**Do:**
- Right-size one replica; add replicas to grow capacity; remove replicas to shrink.
- Use the platform's autoscaling with a metric (CPU, memory, queue depth, RPS) that actually predicts saturation.
- Pre-warm capacity for known traffic spikes (Black Friday, product launches).
- Use horizontal partitioning (sharding) for stateful services when a single replica can't keep up.

**Don't:**
- Vertically scale one replica to its limit when horizontal scaling is trivial.
- Set autoscaling thresholds so tight that you thrash.
- Use maximum-sizing as a permanent strategy — you pay for capacity you don't use.

**Code/Concept:**
> "How can a cloud application reserve a lot of capacity when it has a lot of client load, but less capacity when it has less load, so that its capacity is always proportional to the current level of client load? And how can the application always be able to grow more and more if it needs to? The key is to structure the application to scale bigger and smaller as client load increases and decreases."

*Ref: "Replicable Application" (Chapter 3).*

---

### 45. External Configuration — Secrets Lifecycle

**Principle:** Secrets have a lifecycle — creation, rotation, revocation, audit. Treat them as first-class configuration, not as incidental literals.

**Do:**
- Store secrets in a vault with explicit rotation policy.
- Track who accessed which secret and when (audit).
- Use short-lived credentials when possible (workload identity, signed tokens).
- Encrypt secrets at rest with user-provided keys for additional control.
- Generate per-environment credentials; don't share prod credentials with dev.

**Don't:**
- Hardcode credentials in source, properties files, or container images.
- Use long-lived shared secrets between services.
- Treat secret rotation as an afterthought — design for it from day one.

**Code/Concept:** "IBM Cloud Secrets Manager… stores configuration settings that should not be stored in source code management. It manages their lifecycle, controls access to them, records their usage history, and optionally encrypts them with user-provided keys." *Ref: "External Configuration — IBM Cloud Secrets Manager" (Chapter 3).*

---

### 46. Service API Contract Discipline

**Principle:** The Service API is a contract between providers and consumers. Treat it like a product.

**Do:**
- Publish the API as OpenAPI (Swagger) for REST or `.proto` for gRPC.
- Version the API explicitly (`/v1/`, `Accept: application/vnd.myapi.v2+json`, header-based).
- Keep deprecated versions alive for a published sunset window.
- Generate client/server stubs from the contract; don't hand-write both sides.
- Test for contract drift in CI.

**Don't:**
- Break clients with silent API changes.
- Hand-write parallel client code in N languages — generate it.
- Couple the API to implementation internals (return DB rows, expose internal error codes).

**Code/Concept:** "REST APIs can be published as Swagger documents that define the API as a contract. The service application implements the Swagger API's contract and the client depends on the Swagger API's contract to invoke service behavior." *Ref: "Service API" (Chapter 3).*

---

### 47. Backend Service Selection Discipline

**Principle:** Choosing a backend service is a long-term commitment. Evaluate on dimensions beyond features.

**Do:**
- Evaluate each service on: SLA, data sovereignty, multi-tenancy isolation, multi-region story, lock-in cost, exit strategy.
- Prefer managed platform services over self-hosted equivalents when the SLA matches.
- Verify the service can be reached from your workloads' network (VPC peering, private endpoints).
- Document whether the service is an application service (you call it) or a platform service (it observes you).

**Don't:**
- Pick a service because it's free tier — you'll regret it at scale.
- Skip the SLA review — your reliability is bounded by your weakest service.
- Use a single-tenant service as if it were multi-tenant (or vice versa).

**Code/Concept:** "A backend service's reliability can be lower than an application requires, effectively lowering the application's reliability. Each backend service should include a user agreement that stipulates its service-level agreements (SLAs), which the application developer must confirm are compatible with their application's requirements." *Ref: "Backend Service" (Chapter 3).*

---

### 48. When *Not* to Use the Cloud-Native Patterns

**Principle:** The cloud-native patterns are the default — but they have costs that may not be worth it for tiny or stable workloads.

**Do:**
- Use a simpler deployment (single VM, single binary, SQLite) for hobby projects, internal tools, or stable single-tenant apps with predictable load.
- Reach for cloud-native patterns when any of these is true:
  - Multiple replicas provide real value (variable load, high availability).
  - Multiple languages help (polyglot team, polyglot dependencies).
  - Independent deploy cadence matters (multiple teams).
  - Dynamic scaling is required.
  - Multiple environments must run the same artifact.

**Don't:**
- Over-engineer a 200-line script with the full microservices + K8s + service-mesh + observability stack.
- Refactor an existing well-functioning monolith "just because."

**Code/Concept:** "If it ain't broke, don't use the cloud as an unnecessary excuse to fix it, just Lift and Shift it onto the cloud as is." *Ref: "Big Ball of Mud" (Chapter 2).*

---

### 49. Cloud Application Anatomy — Putting It All Together

**Principle:** Every cloud application built from this book's patterns shares the same anatomy.

**Do:**
- Use this canonical anatomy as a checklist:
  1. **One or more Client Applications** (web, mobile, thick, chatbot, other app) — outside the cloud.
  2. **One or more Application instances** — packaged via Application Package, exposed via Service API, Stateless + Replicable, configured via External Configuration.
  3. **A set of Backend Services** — databases, caches, queues, key vaults, observability.
  4. **An integration layer** — API gateway for outside-in routing; service mesh or backend service for inside-in.
  5. **A runtime environment + orchestrator** — Kubernetes, EC2, Functions, etc.
- This is the same shape across e-commerce, banking, HPC.

**Don't:**
- Mix client logic into the application or application logic into the client.
- Treat backend services as part of the application's process — they're separate processes that scale independently.

**Code/Concept:** "Structure a cloud application as a distributed set of microservices that takes advantage of backend services provided by the cloud platform, accessed by client applications that run outside the cloud." *Ref: "Cloud Application" (Chapter 1).*

---

### 50. Reading Order & Learning Path

**Principle:** The pattern language rewards non-linear reading. Use this path if you want to learn the book in a week.

**Day 1 — Foundation:** Preface + Introduction + Ch 1 (Cloud Applications + Cloud Application pattern). Build the mental model.

**Day 2 — Application architectures:** Ch 2 (BBoM, Modular Monolith, Distributed Architecture). Understand why monoliths evolve.

**Day 3 — Cloud-native basics:** Ch 3 (Cloud-Native Architecture root + Twelve-Factor + Application Package + Service API). The vocabulary and the encapsulation discipline.

**Day 4 — State and scale:** Ch 3 (Stateless Application + Replicable Application). The two hardest patterns to internalize.

**Day 5 — Delegation:** Ch 3 (External Configuration + Backend Service). The rest of the puzzle.

**Day 6 — Future chapters:** Ch 4–6 when available (Microservices, Microservice Design, Event-Driven).

**Day 7 — Wrap-around:** Ch 7 (Storage), Ch 8 (Clients), Ch 9 (Migration), Ch 10 (Strangler).

**Reference use:** Skip around by chapter root pattern and follow Related Patterns links when solving a specific design problem.

*Ref: Introduction — "Getting Started".*

---

### 51. Glossary of Book-Specific Terms

- **Application** — a program + its external dependencies (web server, DB). May be a single monolith or many services.
- **Application Package** — the program's artifact, including code + libraries + config, ready to run in a runtime environment.
- **Architecture** — strategy for decomposing functionality into components and how they collaborate.
- **BBoM (Big Ball of Mud)** — monolithic application with no discernible modularity.
- **Backend Service** — a remote, reusable capability the application connects to over the network.
- **Cloud Application** — an application designed to take maximum advantage of cloud capabilities.
- **Cloud-Native** — approach that designs an application to run well in the cloud.
- **Distributed Architecture** — modules that each run in their own process, possibly on different computers.
- **External Configuration** — settings stored outside the application artifact, typically as environment variables.
- **Module** — a cohesive set of code that implements a unit of functionality.
- **Modular Monolith** — single executable composed of separate encapsulated modules.
- **Replicable Application** — one that can run as multiple equivalent replicas without interference.
- **Service** — a module that runs in a different process than its clients.
- **Service API** — a web-service-based API of coarse-grained tasks the application exposes.
- **SoE (System of Engagement)** — cloud-hosted facade that adapts SoRs for modern clients.
- **SoR (System of Record)** — authoritative system of record for a domain (often legacy, on-prem).
- **Stateless Application** — one that stores no domain state in memory and no session state between requests.
- **Workload** — a deployable component running on a server.

*Ref: All chapters, this deep-dive.*

---

### 52. Quick-Reference Pattern Index

| Book Pattern | Root? | Where |
|---|---|---|
| Cloud Application | Yes (whole book) | Ch 1 |
| Big Ball of Mud | No | Ch 2 |
| Modular Monolith | No | Ch 2 |
| Distributed Architecture | No | Ch 2 |
| Cloud-Native Architecture | Yes (Ch 3) | Ch 3 |
| Application Package | No | Ch 3 |
| Service API | No | Ch 3 |
| Stateless Application | No | Ch 3 |
| Replicable Application | No | Ch 3 |
| External Configuration | No | Ch 3 |
| Backend Service | No | Ch 3 |
| Microservice | Yes (Ch 4) | Ch 4 (unavailable ER) |
| Model around Domain | Yes (Ch 5) | Ch 5 (unavailable ER) |
| Reactive Component | Yes (Ch 6) | Ch 6 (unavailable ER) |
| Cloud Database | Yes (Ch 7) | Ch 7 (unavailable ER) |
| Client Application | Yes (Ch 8) | Ch 8 (unavailable ER) |
| Strangler Application | Yes (Ch 10) | Ch 10 (unavailable ER) |

*Ref: Introduction — Table I-1.*

---

## Cross-References

- Related best practices in this corpus:
  - `best_practices/Microservices_Patterns.md` (Chris Richardson — implementation patterns referenced by this book)
  - `best_practices/Building_Microservices_2e.md` (Sam Newman — design philosophy aligned with Ch 5)
  - `best_practices/Domain_Driven_Distilled.md` (Vaughn Vernon — Model around Domain)
  - `best_practices/Designing_Data_Intensive_Applications.md` (Kleppmann — polyglot persistence + event-driven)
  - `best_practices/Continuous_Delivery.md` (Humble, Farley — CI/CD referenced by Modern App Dev)
- Topic index: `best_practices/INDEX.md`