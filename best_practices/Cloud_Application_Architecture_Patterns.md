# Cloud Application Architecture Patterns

**Author:** Kyle Brown, Bobby Woolf, Joseph Yoder
**Topic tags:** `#architecture` `#cloud` `#api` `#microservices`
**Language focus:** language-agnostic (Java / Node.js / Go / Python examples)
**Sources:** `markdown_output/Cloud_Application_Architecture_Patterns_ER/Cloud_Application_Architecture_Patterns_ER.md` (no summary file)

## TL;DR
A pattern-language catalog of cloud-application design decisions grounded in three root chapters: *Cloud Application* (what makes an application cloud-native vs. traditional IT), *Application Architecture* (Big Ball of Mud → Modular Monolith → Distributed Architecture), and *Cloud-Native Application* (Application Package, Service API, Stateless, Replicable, External Configuration, Backend Service). Apply when designing a new cloud app, modernizing a monolith, or judging whether an architecture is fit for the cloud. (Chapters 4–10 on Microservices, Event-Driven, Storage, Clients, Migration, Strangler are listed in the TOC but not yet released — only Ch 1–3 content exists in this early release.)

---

## Best Practices by Topic

### Why "Cloud-Native" Is Not "Running on a VM" — Cloud Application vs. Traditional IT

**Principle:** The cloud's defining characteristics (unreliable commodity hardware, eventual consistency, generic evolving hardware, application mobility, multi-tenancy, horizontal scaling, statelessness, immutability, componentization, service catalog, self-provisioning, cloud-native storage) require an application to be designed differently from a traditional-IT app. Lifting-and-shifting a monolith onto a cloud VM does not produce a cloud application.

**Do:**
- Design for *unreliable infrastructure* — assume any single instance, disk, rack, or zone can fail; make the application more reliable than the infrastructure beneath it.
- Design for *eventual consistency* — give up on cross-resource ACID transactions; build idempotent operations.
- Design for *horizontal scaling* — multiple replicas of the same code must run as one logical app.
- Design for *mobility* — the cloud may move your workload to a different computer; no fixed IP, no local disk, no host-specific config.
- Design for *statelessness* — load data per-request; persist immediately; do not keep domain state in process memory.
- Design for *immutability* — deploy new releases rather than patch running workloads; replace, never mutate.
- Design for *shared resources* — your workload runs alongside other tenants; isolate via process / container / namespace.

**Don't:**
- Don't rely on the hardware for reliability. (Cloud vendors explicitly buy *less-reliable* RAM when cheaper — they engineer reliability in software.)
- Don't use ACID transactions across services. The cloud provides no transaction manager.
- Don't pin a workload to a specific OS or hardware model. Hardware evolves under your feet.
- Don't store state in process memory expecting it to survive a restart.
- Don't depend on a central ops team to provision your environment — provision it yourself via the platform API.

**Code (Java — env-var external config, no in-code literals):**
```java
// Read configuration from env vars at startup
String dbHost = System.getenv("DB_HOST");
String dbUser = System.getenv("DB_USER");
String dbPwd  = System.getenv("DB_PASSWORD");
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Chapter 1. Cloud Applications" / "Cloud computing practices"*

---

### Big Ball of Mud — When "No Architecture" Is the Right Architecture

**Principle:** For prototypes, MVPs, and exploratory programming, the simplest architecture is no architecture. A Big Ball of Mud (BBoM) — circular dependencies, global variables, copy-paste duplication — is sometimes the correct choice *for a limited window* of a system's life.

**Do:**
- Use BBoM for MVPs and exploratory prototypes where learning the requirements matters more than the design.
- Apply Kent Beck's discipline: "Make it work. Make it right. Make it fast." Don't try to design the perfect architecture before the code runs.
- Apply sustainment patterns (Foote & Yoder / Wirfs-Brock & Yoder) to keep BBoM from collapsing: *Shearing Layers* (group code that changes at similar rates), *Sweep It Under The Rug* (cordon off the mess), *Paving Over The Wagon Trail* (shore up architectural boundaries), *Wiping Your Feet At The Door* (don't add new mud).
- Track technical debt explicitly; the team that builds the BBoM must also own the moment to refactor.

**Don't:**
- Don't ship a BBoM to long-lived production without a plan to evolve it. Once an MVP proves viable, technical debt begins to compound.
- Don't confuse "agile = no design" — without attention to architecture, even a Modular Monolith devolves into a distributed Big Ball of Mud, which is harder to escape than the original.
- Don't reach for the cleanest possible architecture when the requirements are still unknown.

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Chapter 2. Application Architecture" / "Big Ball of Mud"*

---

### Modular Monolith — Cohesive Modules Without Distributed Costs

**Principle:** When requirements are stable and the application will live for years, organize it into cohesive, well-encapsulated modules with limited dependencies between them. One process; many modules. Same process means easy debugging, shared memory, single deployable, easy crosscutting concerns (security, logging).

**Do:**
- Design modules around the domain, one cohesive unit of functionality per module.
- Make modules loosely coupled via explicit interfaces; enforce no-circular-dependencies.
- Assign each module to a separate team (6–12 people, "two-pizza team") that can work in parallel.
- Use OSGi-style bundles (or Java JAR with explicit package exports) to enforce module isolation at the classloader level — the Eclipse/OSGi model solved classpath isolation that JAR files alone could not.
- Treat the Modular Monolith as the *stepping stone* to a Distributed Architecture when modules need independent scale or failure domains.

**Don't:**
- Don't let modules depend on each other's internals — Eclipse's original XPCOM failure showed what happens when extensions can reach into too many internals (the 2016 WebExtensions API narrowed this and deprecation of XPCOM in 2017 was the result).
- Don't ship modules that are tightly coupled at the class level just because they're in different JARs — standard Java packaging has no enforced isolation.
- Don't keep adding "one more module" inside a single process once independent scaling or independent deployability is needed; that's the signal to distribute.

**Code (OSGi-style bundle, the Eclipse plugin manifest):**
```
# Manifest fragment — explicit package exports and versioned imports
Bundle-SymbolicName: com.example.orders
Export-Package: com.example.orders.api; version="1.0.0"
Import-Package: com.example.common; version="[1.0,2.0)"
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Chapter 2. Application Architecture" / "Modular Monolith" / "Eclipse / OSGi"*

---

### Distributed Architecture — Independent Processes, Independent Scale, Independent Failure

**Principle:** When parts of the application need to be developed, deployed, scaled, and failed independently, model the application as a set of services in separate processes communicating over a network. Each service scales and fails independently; an outage of one service does not bring down the rest.

**Do:**
- Design the service boundaries by analyzing interactions with the application (model around the domain) so each service has one well-encapsulated responsibility.
- Use coarse-grained task APIs (Session Facade / Remote Facade) to reduce chatty round-trips — pass-by-value across the network is expensive.
- Choose a remote technology deliberately: gRPC for typed RPC; REST/HTTP+JSON for universal web interop; RabbitMQ / Kafka for asynchronous messaging.
- Apply the Airline Reservation lesson: different parts of the same app have *vastly* different scaling needs (browse ≫ purchase ≫ frequent-flier). Distribute so each scales alone.
- Adopt the language-server lesson: VS Code runs each language support as a separate process communicating over Language Server Protocol — same separation yields UX, scale, and testability wins.
- For data, follow *Database per Service* — replication of monolith DB to a service store is acceptable as a *temporary* bridge; long term, each service owns its data.

**Don't:**
- Don't fall for the *Fallacies of Distributed Computing* — the network is unreliable, has latency, has zero bandwidth at moments, is not secure, topology changes, transport cost is non-zero, and the network is heterogeneous.
- Don't distribute prematurely when a Modular Monolith still serves. Distribution adds concurrency, failure handling, logging, security, and testing complexity that you pay for even when nothing fails.
- Don't share a single relational database across multiple services — it becomes both a bottleneck and a single point of failure, plus it couples the services' schemas.
- Don't expose fine-grained methods as remote APIs. Use Remote Facade to make the network boundary coarse-grained.
- Don't rely on sticky sessions across distributed services — cloud routing is stateless.

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Chapter 2. Application Architecture" / "Distributed Architecture"*

---

### Cloud-Native Architecture — Application Program + Backend Services

**Principle:** A cloud-native application is two parts: (1) the *Application* — the custom domain logic implemented by your team, packaged and deployed as a unit; (2) *Services* — reusable SaaS / platform-managed functionality the application delegates to remotely. The split enables mobility, polyglot development, independent scaling, and reuse.

**Do:**
- Separate the application from its middleware. Cloud provides no in-process middleware server; delegate to remote backend services.
- Pick languages and frameworks that have a runtime environment + package manager (Java/JVM + Maven/Gradle, Node.js + NPM, Go, Python, PHP, Ruby) so the application can run unchanged on any cloud platform.
- Use polyglot development — each module can be written in a different language because each runs in its own runtime environment.
- Map the CNCF Cloud Native Maturity Model across People, Process, Policy, Technology, and Business Outcomes — cloud-native is not just architecture, it's how the whole IT department works.

**Don't:**
- Don't try to install custom middleware servers on cloud VMs — that's a 2000s-era application-server pattern; cloud provides middleware as a service.
- Don't tie the application package to a specific OS version or hardware model.
- Don't treat cloud-native as "where the app runs" — IBM is explicit: "cloud native refers less to where an application resides and more to how it is built and deployed."

**Code (Node.js — language-runtime + package manager):**
```json
// package.json — declares dependencies, run via "npm start"
{
  "dependencies": {
    "upper-case": "^2.0.0"
  },
  "scripts": { "start": "node server.js" }
}
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Chapter 3. Cloud-Native Application" / "Cloud-Native Architecture"*

---

### Application Package — Package the Program With All Its Dependencies

**Principle:** An application package contains the program, all required libraries, and the configuration needed to run — built by a package manager from a registry, executed inside a runtime environment. The same package runs on any OS that has the runtime.

**Do:**
- Choose a language whose ecosystem provides both a runtime and a package manager: Java/JVM (Maven/Gradle → JAR/WAR/EAR), Node.js (NPM), Go (compiles to native), Python (pip).
- Build the package *immutably* — once built, it deploys unchanged to every environment. Do not edit the package after build.
- Declare every dependency in the manifest (Maven `pom.xml`, NPM `package.json`, Gradle `build.gradle`). No implicit system-wide packages.
- Use Open Liberty / server.xml with `featureManager` so the runtime ships *only* the features the app needs (smaller, faster, safer).
- Build the package into a container image or VM image so the cloud platform's deployer can stamp out identical replicas.

**Don't:**
- Don't depend on system-wide packages or shared OS libraries; the Twelve-Factor App forbids this explicitly.
- Don't choose a language without a runtime-and-package-manager combo for a cloud application. C / C++ / assembler / shell scripts "don't have separate runtimes; those programs are highly dependent on the underlying operating system" — avoid them for cloud-native.
- Don't customize the OS or runtime to fit one application — multiple applications share the same runtime.

**Code (Open Liberty server.xml — minimal runtime feature set):**
```xml
<server description="Sample Liberty server">
  <featureManager>
    <feature>restfulWS-3.0</feature>
    <!-- only the features the app actually uses -->
  </featureManager>
</server>
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Application Package" / "Java", "Node.js", "Open Liberty"*

---

### Service API — Expose Coarse-Grained Tasks as Web Services over HTTP

**Principle:** A service API exposes the application's functionality as a set of coarse-grained tasks (use cases) implemented as a web service over HTTP. The API is a contract: provider implements, consumer invokes, neither knows the other's internals.

**Do:**
- Model the API as tasks the application can perform, not as CRUD on internal objects (REST URIs map to resources; gRPC maps to typed procedures).
- Use HTTP as the universal transport — firewalls, browsers, routers, and intranets all pass it. SOAP → REST → OpenAPI/gRPC is the modern standard; publish the API as an OpenAPI/Swagger document as the contract.
- Keep request/response payloads primitives and simple objects — large objects are expensive to marshal across the network. Use a *claim check* (a small identifier) to look up a large object in shared storage rather than passing it.
- Design once per API evolution — once published, the API is hard to change; adopt an API versioning strategy from the start.
- Treat the API as the contract between independent teams: server team designs and implements, client team consumes. Coordinate on the contract, not on internals.

**Don't:**
- Don't expose fine-grained methods as remote APIs (chatty network). Coarse-grained task APIs (Session Facade / Remote Facade) only.
- Don't return pass-by-reference or large object graphs. Pass-by-value only.
- Don't use object-oriented RPC like DCOM, CORBA, .NET Remoting, Java RMI as the primary interface — they don't traverse IP networks well; HTTP is universal.
- Don't return domain state directly from the API when the application should be stateless — the API exposes tasks that encapsulate the state changes, not the state itself.

**Code (JAX-RS web resource exposing a coarse-grained task):**
```java
@Path("/currency")
public class CurrencyResource {
  @POST @Path("/convert/")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_PLAIN)
  public String convert(@FormParam("amount") String amount,
                        @FormParam("from")   String from,
                        @FormParam("to")     String to) {
    BigDecimal unconverted = new BigDecimal(amount);
    Currency fromC = Currency.getInstance(from);
    Currency toC   = Currency.getInstance(to);
    MoneyConverter mc = new MyConverter();
    return mc.convert(unconverted, fromC, toC).toString();
  }
}
```
**Code (OpenAPI 3.0 contract — single coarse-grained endpoint):**
```yaml
openapi: 3.0.0
paths:
  /convert:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [amount, from, to]
              properties:
                amount: { type: number }
                from:   { type: string }
                to:     { type: string }
      responses:
        '200':
          description: Successfully converted
          content:
            application/json:
              schema: { type: number }
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Service API" / "OpenAPI interface", "JAX-RS interface", "Go interface"*

---

### Stateless Application — Domain State in Databases, Session State in the Client

**Principle:** A stateless application stores no domain state in process memory between requests and stores no session state on the server. Each request carries the context (e.g. a record ID) the application needs to load its working state from a shared database.

**Do:**
- Pass session context as request parameters (HTTP cookies, query/body params) so any replica can serve any request.
- Load domain data from a shared backend database per request; write changes back before returning; flush in-process caches between transactions.
- Use temporary / local variables in methods, *not* instance or class fields, so each thread has its own data and the class is thread-safe by construction.
- Keep business transactions brief — when a stateless app crashes, only in-flight uncompleted transactions are lost; minimize that window by persisting quickly.
- If in-memory caching is needed, delegate to a backend service like Redis or Memcached (not a process-local cache) so the application remains stateless.

**Don't:**
- Don't cache domain data in instance variables / class fields / singletons — that re-introduces state, and once you have state you have scale, consistency, shutdown, and recovery problems.
- Don't use sticky sessions / HTTP session objects / stateful session beans to remember per-user state on the server. The Twelve-Factor App: "Sticky sessions are a violation of twelve-factor and should never be used or relied upon. Session state data is a good candidate for a datastore that offers time-expiration, such as Memcached or Redis."
- Don't delay persisting changes hoping to batch them later. The longer the delay, the larger the RPO when the app crashes.
- Don't return database records that the application mutated in-place; the application is stateless — read, modify, write, return.

**Code (Java — stateless ProductManager):**
```java
// Stateless — no instance variable for products
public class ProductManager {
  private Database getDatabase() { /* get connection */ return db; }

  public Product getProductNamed(String name) {
    // Load from DB every time — never cache in memory
    return this.getDatabase().get(name);
  }
}
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Stateless Application" / "Make domain state external", "Make session state external"*

---

### Replicable Application — Multiple Equivalent Replicas, No Singletons

**Principle:** Design the application so it can run as many equivalent replicas as needed, with no replica being special. The cloud platform deploys replicas from the same application package; replicas don't know about each other; all replicas share state via backend services.

**Do:**
- Run at least two replicas by default to survive single-instance failure.
- Coordinate through shared backend services (databases, message brokers), not through in-memory data or fixed IP addresses.
- Distribute a shared connection pool (e.g. to a legacy SoR with a connection limit) via an integration service (IBM App Connect, MuleSoft) — let *one* pool be shared by all replicas rather than each replica creating its own.
- Use ReplicaSets, Auto Scaling groups, or platform equivalent so the cloud platform can scale out and in automatically.
- For Stateful workloads that cannot be made stateless, use a platform-managed database service (RDS, Cloudant, Cosmos DB) that handles replication and failover rather than rolling your own.

**Don't:**
- Don't use the Singleton pattern anywhere that prevents running multiple replicas. The book is explicit: "The number one enemy of replication is the Singleton pattern and variations thereof such as block storage and fixed IP addresses."
- Don't use block or file storage for shared data across replicas. Each replica gets its own volume and won't see the others' writes. Use a database service instead.
- Don't create per-replica connection pools to a constrained backend (e.g. a 10-connection SoR) — 10 replicas × 10 connections = 100 connections will crash the SoR.
- Don't pick a fixed IP address or hostname — cloud moves workloads.
- Don't implement leader election for stateful coordination when the state can be moved into a backend service.

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Replicable Application" / "Avoid singletons", "Store data in a shared database service", "Manage a connection pool using an integration service"*

---

### External Configuration — Environment Variables, Not Properties Files

**Principle:** Configuration values (database endpoints, credentials, environment-specific URLs) live outside the application package as environment variables. The same immutable package deploys to every environment; each environment provides its own values.

**Do:**
- Store all environment-specific values in OS environment variables (or Kubernetes ConfigMap / Secret / Vault equivalents).
- Read environment variables in the application's startup path using the language's standard API.
- Use platform-specific mechanisms to inject values: Kubernetes ConfigMap (non-sensitive) and Secret (sensitive), AWS SSM Parameter Store, HashiCorp Vault, IBM Cloud Secrets Manager.
- Keep secrets in a secrets vault — *never* commit credentials to source control. Encrypt with git-crypt if absolutely forced to commit.
- Provide a single external configuration that all replicas share (the platform sets the environment once for all replicas).

**Don't:**
- Don't hardcode endpoints, credentials, or environment-specific URLs in source code. Every new environment forces a rebuild.
- Don't use properties files packaged inside the application — they're state, and they can't be changed without rebuilding.
- Don't store credentials in source control (even in a "private" repo — they leak).
- Don't have the application try to read a database *to get its configuration* — chicken-and-egg.
- Don't store all settings in a single file inside the repo — sensitive and non-sensitive need separate treatment.

**Code (Java — read env vars):**
```java
Map<String, String> env = System.getenv();
String port = System.getenv("PORT");
if (port == null) { /* handle missing config */ }
```
**Code (Node.js — read env vars):**
```javascript
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`listening on ${PORT}`));
```
**Code (Kubernetes ConfigMap):**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"
```
**Code (Kubernetes Secret):**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  USER_NAME: YWRtaW4=       # base64("admin")
  PASSWORD: MWYyZDFlMmU2N2Rm # base64
```
*Ref: Cloud_Application_Architecture_Patterns_ER.md — "External Configuration" / "Read environment variables in Java", "Node.js", "Kubernetes Configuration Map and Secret", "Secrets storage and encryption"*

---

### Backend Service — Reusable Functionality as a Remote Service

**Principle:** Reusable, common functionality (databases, messaging, key management, identity, workflow engines) lives in backend services that the application invokes remotely. Reusing a service (vs. embedding a library) gives language-independence, independent distribution, scaling, failure, composition, and no code duplication.

**Do:**
- Treat each backend service as an attached resource — discoverable by URL, replaceable, swappable between environments.
- Prefer cloud-managed SaaS services over self-hosted equivalents when the SLA fits: Amazon RDS, Azure Cosmos DB, IBM Db2 on Cloud; Kafka / Event Hubs / IBM Event Streams; IBM App Connect; AWS KMS, Azure Key Vault.
- Distinguish *application services* (the app's code invokes them — DB, queue, workflow) from *platform services* (the platform invokes them — KMS, observability, auth gateway) and design accordingly.
- Verify the service's SLA matches the application's requirements. A backend service's reliability caps the application's reliability.
- Watch out for data-sovereignty restrictions: not knowing where the service is hosted is a real blocker for regulated workloads.

**Don't:**
- Don't embed databases in-process for shared state (Derby, SQLite, eXtremeDB embedded) — that defeats the backend-service model and breaks replicability.
- Don't connect an app directly to a legacy SoR with a tight connection limit and run multiple replicas; route through an integration service that owns the pool.
- Don't expose internal implementation endpoints as "backend services" — they're really platform plumbing (monitoring, log aggregation, API gateway).
- Don't ignore a service's multi-tenancy model. Understand how the service isolates tenants before adopting.

**Code (Twelve-Factor III / IV):**
- *Config*: "The twelve-factor app stores config in environment variables (often shortened to env vars or env). Env vars are easy to change between deploys without changing any code; unlike config files, there is little chance of them being checked into the code repo accidentally; and unlike custom config files, or other config mechanisms such as Java System Properties, they are a language- and OS-agnostic standard."
- *Backing services*: "A backing service is any service the app consumes over the network as part of its normal operation."

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Backend Service" / "Database services", "Integration services", "Security services", "Observability services"*

---

### Twelve-Factor App Methodology — Foundation of Cloud-Native

**Principle:** The Twelve-Factor App (Heroku) is a widely accepted set of 12 practices that, together, make an application fit for modern cloud platforms.

**Do (the 12 factors):**
1. **Codebase** — One codebase tracked in revision control, many deploys.
2. **Dependencies** — Explicitly declare and isolate dependencies (manifest + package manager).
3. **Config** — Store config in the environment (env vars).
4. **Backing services** — Treat backing services as attached resources.
5. **Build, release, run** — Strictly separate build and run stages.
6. **Processes** — Execute the app as one or more stateless processes.
7. **Port binding** — Export services via port binding (HTTP).
8. **Concurrency** — Scale out via the process model (multiple replicas).
9. **Disposability** — Maximize robustness with fast startup and graceful shutdown.
10. **Dev/prod parity** — Keep development, staging, and production as similar as possible.
11. **Logs** — Treat logs as event streams (write to stdout, let the platform aggregate).
12. **Admin processes** — Run admin/management tasks as one-off processes (same env, same code, one-off release).

**Don't:**
- Don't break any of the 12. They reinforce each other; pick-and-choose leads to inconstencies (e.g. stateless processes but stateful sessions).
- Don't treat twelve-factor as Heroku-only. The book is explicit: a twelve-factor app "does not have to be deployed on a cloud."

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "The Twelve-Factor App"*

---

### Architecture Evolution — The Right Time to Modernize

**Principle:** Applications evolve from BBoM → Modular Monolith → Distributed Architecture as requirements stabilize and load grows. Each step is appropriate at a different time. Forcing distributed architecture on an unknown domain is premature; staying in BBoM once a system is long-lived is negligent.

**Do:**
- Start with BBoM when requirements are provisional and learning matters most.
- Refactor to Modular Monolith once the application is in long-term production.
- Move to Distributed Architecture when modules need to scale or fail independently (the airline example: browse 10× purchase 10× frequent-flier).
- Continuously reinvest in architecture — the book warns: "Often a Modular Monolith devolves into a Big Ball of Mud... This even becomes worse and scarier when you have a distributed Big Ball of Mud."
- Design with *Model around the Domain* (Chapter 5 root pattern) — discover microservice boundaries from real interactions.

**Don't:**
- Don't treat "we have microservices" as the goal — it's a means to independent scale and independent deploy.
- Don't conflate "agile" with "no architecture." Agile without architectural care produces BBoM.
- Don't skip the Modular Monolith step when a Distributed Architecture would actually be premature for the team's skills or the load profile.

*Ref: Cloud_Application_Architecture_Patterns_ER.md — "Conclusion: Wrapping Up Application Architecture"*

---

## Anti-Patterns & Common Mistakes

- **Singleton dependency:** Object that can only have one instance per process → can't replicate. *Fix:* Remove the singleton; if shared state is required, move it to a backend service.
- **In-memory domain cache in an instance variable:** Re-introduces state, breaks statelessness, hides a disaster-recovery RPO time-bomb. *Fix:* Drop the cache or move it to Redis/Memcached.
- **Sticky sessions to a stateful server:** Defeats horizontal scaling. *Fix:* Pass session state as parameters from the client; store only in a time-expiring backend store.
- **Properties file baked into the package:** Cannot change config without rebuilding. *Fix:* External Configuration via env vars / Kubernetes ConfigMap + Secret / Vault.
- **Shared block storage between replicas:** Only one replica can attach; data loss on shutdown. *Fix:* Use a cloud-managed database service.
- **Per-replica connection pool to a constrained SoR:** 10 replicas × 10 connections = crash. *Fix:* Integration service (App Connect, MuleSoft) owns the shared pool.
- **Hardcoded endpoints / credentials in source code:** Forces rebuild per environment; leaks secrets. *Fix:* External Configuration + secrets vault.
- **Distributed Big Ball of Mud:** Distributed architecture with no internal modularity — the worst of both worlds. *Fix:* Stop and refactor before adding more services.
- **Chatty fine-grained API across the network:** Latency kills throughput. *Fix:* Session Facade / Remote Facade — coarse-grained task APIs.
- **Custom in-process middleware on a cloud VM:** A traditional-IT anti-pattern carried onto the cloud. *Fix:* Delegate to a cloud-managed backend service.

---

## Decision Heuristics / Checklists

- **Choosing architecture for a new application:**
  - Requirements unknown / MVP → BBoM (with discipline to refactor later).
  - Requirements known, long-lived, one team → Modular Monolith.
  - Modules need independent scale or independent failure → Distributed Architecture.
- **Is this app cloud-native?** Checklist: (1) Stateless? (2) Replicable? (3) Immutable package? (4) External configuration? (5) Service API over HTTP? (6) Backend services for shared functionality? (7) Horizontal scale only (no vertical scaling assumptions)?
- **API design checklist:** Coarse-grained tasks? HTTP transport? OpenAPI/contract published? Versioning strategy? No large objects in payloads (use claim check)?
- **Replicable app checklist:** No singletons? No local disk? No fixed IP? Shared backend for all state? Pool-managed connection to constrained SoRs? At least 2 replicas in prod?
- **Configuration checklist:** No literals in code? All settings env-var / ConfigMap / Secret / Vault? Secrets out of SCM? Each environment provides its own values?
- **When to introduce microservices:** Independent scale needed? Independent release cadence needed? Module owned by different team? Module needs different technology stack? If no to all → keep the Modular Monolith.

---

## Key Takeaways

1. The cloud is not "someone else's computer you can ignore" — its characteristics (unreliability, eventual consistency, horizontal scale, mobility, multi-tenancy) demand a different application design.
2. A cloud-native application = Application Package + Service API + Stateless + Replicable + External Configuration + Backend Services. The six patterns work as a set; break one and the rest weaken.
3. Statelessness is the multiplier — it makes scaling, replication, fast startup, clean shutdown, and crash recovery all work. Cache in backend services, not in process memory.
4. The biggest enemy of replication is the Singleton. The second biggest is local disk / block storage. Both push you back into single-instance territory.
5. Configuration lives in the environment, not in the package or the code. Build once, deploy everywhere, change values per environment.
6. Backend services beat code libraries for reuse — language-independent, scale-independent, failure-isolated, no duplication, composable.
7. Architecture evolves with the application. Match the architecture to the requirements and the team. Don't distribute what isn't ready; don't stay a BBoM longer than you have to.

---

## Cross-References
- Related: [[../Building_Microservices.md]]
- Related: [[../Designing_Distributed_Systems.md]]
- Related: [[../Foundations_of_Scalable_Systems.md]]
- Related: [[../Software_Architecture_Patterns.md]]
- Related: [[../Continuous_Deployment.md]]
- Related: [[../Observability_Engineering.md]]
- Topic index: [[../INDEX.md]]