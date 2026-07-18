# Microservices: Up and Running
**Authors:** Ronnie Mitra & Irakli Nadareishvili
**Topic tags:** `#architecture` `#api` `#testing`
**Language focus:** Polyglot (Node.js, Python/Flask, Go, Java, etc.) on AWS EKS
**Sources:** `markdown_output/Microservices Up And Running/Microservices Up and Running.md` · `summaries/Microservices Up And Running.md`

## TL;DR
*Microservices: Up and Running* is a prescriptive implementation guide that
shows how to build a working microservices system end-to-end. The unifying
thesis is **minimize coordination costs** — the gain in delivery speed comes
from autonomous teams working on independent services with independent data
stores, not from any specific technology. The book operationalizes that
thesis via a five-team operating model (System Design, Platform,
Stream-Aligned Microservices, Complicated-Subsystem Release, Stream-Aligned
API/BFF), a seven-step design methodology (SEED(S)), data independence
with embedded DBs + event sourcing / CQRS, Terraform + GitHub Actions IaC,
Docker + Helm + Argo CD GitOps deployment, and three deployment patterns
(blue-green, canary, multiple-versions). The running example is two services
(`ms-flights` on Node/Express + MySQL, `ms-reservations` on Python/Flask +
Redis) orchestrated by a thin BFF API.

---

## Best Practices by Topic

### Why Microservices (and Why Coordination Is the Bottleneck)

**Principle:** Build microservices to **minimize coordination costs** between
teams. Coordination is the *fundamental* force — the entire architecture
serves that purpose.

**Do:**
- Reduce coordination to a *design-time* goal: every team boundary, data
  boundary, and API boundary should reduce cross-team conversations.
  *Ref: Microservices Up And Running.md — "Reducing Coordination Costs" (`page-19-0`).*
- Reserve microservices for *complex* systems; for simple systems a monolith
  is more appropriate.
  *Ref: Microservices Up And Running.md — "Toward a Microservices Architecture" (`page-16-0`).*
- Treat microservices as a *style* of architecture (componentization +
  service size + holistic optimization) rather than a checkbox.
  *Ref: Microservices Up And Running.md — "What Are Microservices?" (`page-18-0`).*
- *Always* run an "inverse Conway maneuver": design team + communication
  structure *first*, the system shape follows.
  *Ref: Microservices Up And Running.md — "Key Decision: When to Design Teams and Coordination Models" (`page-36-0`).*

**Don't:**
- Don't use microservices just because they are popular — without a real
  coordination problem you'll just create moving parts.
  *Ref: Microservices Up And Running.md — "The Hard Parts" (`page-21-0`).*
- Don't fall into *analysis paralysis* — most impactful decisions have long
  feedback loops. *Build, learn, iterate*.
  *Ref: Microservices Up And Running.md — "Analysis Paralysis" (`page-22-0`).*

---

### Recording Decisions: Lightweight ADRs (LADR)

**Principle:** Capture the *why* behind every key decision. Decisions are
immutable; you can supersede them with a new ADR.

**Do:**
- Use the Michael Nygard LADR format. Four sections: **Context / Decision /
  Consequences / Status**:
  ```markdown
  # OPM1: Use ADRs for decision tracking
  ## Status
  Accepted
  ## Context
  ## Decision
  ## Consequences
  ```
  *Ref: Microservices Up And Running.md — "Writing a Lightweight Architectural Decision Record" (`page-25-0`).*
- Store ADRs as text files in version control; treat them as code.
  *Ref: Microservices Up And Running.md — "Key Decision: Use ADRs for Decision Tracking" (`page-25-0`).*
- Mark *Key Decision* inline in the running prose so readers can see at a
  glance what was decided; link to the full ADR.
  *Ref: Microservices Up And Running.md — "Key Decision: Use ADRs for Decision Tracking" (`page-25-0`).*

---

### Operating Model: Five Teams, Three Interaction Modes

**Principle:** Define an explicit operating model before writing code.
Microservices fail for *organizational* reasons, not technical ones.

**Do — Team Topologies:**
- Build the operating model with **Team Topologies** (Skelton & Pais):
  four team archetypes (stream-aligned, platform, enabling,
  complicated-subsystem) × three interaction modes (collaboration,
  facilitating, x-as-a-service).
  *Ref: Microservices Up And Running.md — "Team Topologies" (`page-35-0`).*
- Cap team size at **5–8 people** (two-pizza / Dunbar-friendly). The book
  chose this from the start.
  *Ref: Microservices Up And Running.md — "Team Size" (`page-32-0`).*
- Build **cross-functional** teams — every member must directly influence
  the output. No observers.
  *Ref: Microservices Up And Running.md — "Team Skills" (`page-33-0`).*

**Do — The five teams this book prescribes:**
- **System Design Team** (enabling, 3–5 ppl) — sets standards & guardrails,
  continually improves the system.
  *Ref: Microservices Up And Running.md — "Establish a System Design Team" (`page-40-0`).*
- **Microservices Teams** (stream-aligned, 5–8 ppl each) — one team per
  microservice, owns design through retirement.
  *Ref: Microservices Up And Running.md — "Key Decision: Microservice Ownership" (`page-41-0`).*
- **Cloud Platform Team** (platform, 5–8 ppl) — self-service infra-as-service
  (network + compute + deployment), treats internal teams as customers.
  *Ref: Microservices Up And Running.md — "Platform Teams" (`page-44-0`).*
- **Release Team** (complicated-subsystem, 5–8 ppl) — deploys to
  production-like environments, owns the deployment pipeline.
  *Ref: Microservices Up And Running.md — "Enabling and Complicated-Subsystem Teams" (`page-46-0`).*
- **API / BFF Team** (stream-aligned, 5–8 ppl) — exposes a thin
  Backend-For-Frontend API that orchestrates microservices. No business
  logic in BFF.
  *Ref: Microservices Up And Running.md — "Consumer Teams" (`page-47-0`).*

**Don't:**
- Don't let microservices call each other directly. Always go through the
  BFF API for orchestration.
  *Ref: Microservices Up And Running.md — "Key Decision: Avoid Microservices Calling Each Other Directly" (`page-213-0`).*

---

### Designing Microservices: SEED(S) Methodology

**Principle:** Use a repeatable seven-step design process so service
boundaries stay aligned with business needs, not technology layers.

**Do — the seven steps:**
- 1. **Identify Actors** — who interacts with the system: customers, apps,
  APIs, microservices.
  *Ref: Microservices Up And Running.md — "Identifying Actors" (`page-37-0`).*
- 2. **Collect Jobs-To-Be-Done (JTBDs)** — *"When [situation], the [actor] needs
  [need], so that [outcome]."*
  *Ref: Microservices Up And Running.md — "Identifying Jobs That Actors Have to Do" (`page-39-0`).*
- 3. **Describe Interactions** — UML sequence diagrams in PlantUML:
  ```text
  @startuml
  actor Customer as cust
  participant "Web App" as app
  participant "BFF API" as api
  participant "ms-flights" as msf
  participant "ms-reservations" as msr
  cust -> app : "Flight Seats Page"
  app -> api : flight.getSeatingSituation()
  api -> api : auth
  api -> msf : getFlightId()
  msf --> api : flight_id
  api -> msf : getFlightSeating()
  api -> msr : getReservedSeats()
  @enduml
  ```
  *Ref: Microservices Up And Running.md — "Discovering Interaction Patterns" (`page-43-0`).*
- 4. **Compile Actions and Queries** — actions modify state, queries read.
- 5. **Design an OpenAPI Specification (OAS)** — formal REST contract:
  ```yaml
  openapi: 3.0.0
  info:
    title: Flights Management Microservice API
    version: 1.0.1
  paths:
    /flights:
      get:
        summary: Look Up Flight Details
        parameters:
          - name: flight_no
            in: query
            required: true
            schema: { type: string }
        responses:
          '200':
            description: Successful
  ```
  *Ref: Microservices Up And Running.md — "Designing an OpenAPI Specification" (`page-217-0`).*
- 6. **Select Technologies** — heterogeneous stacks encouraged; one
  stack fits one problem best.
- 7. **Write Code** — implement against the OAS.

---

### Finding Service Boundaries (Event Storming + DDD + Universal Sizing)

**Principle:** Start coarse-grained, aligned to bounded contexts. Don't
create too many microservices too early.

**Do:**
- Use **Event Storming** — collaborative workshop with sticky notes —
  to discover natural domain boundaries.
  *Ref: Microservices Up And Running.md — "Event Storming" (`page-66-0`).*
- Apply **bounded context** (DDD) — each context has its own ubiquitous
  language and data model.
  *Ref: Microservices Up And Running.md — "Domain-Driven Design and Microservice Boundaries" (`page-59-0`).*
- Honor **Sam Newman's rules**: loose coupling, high cohesion, small
  enough for one team to own.
  *Ref: Microservices Up And Running.md — "Why Boundaries Matter" (`page-57-0`).*
- **Don't** create too many microservices too early — "it is acceptable for
  early services to be larger than their target state."
  *Ref: Microservices Up And Running.md — "Boundaries" (`page-73-0`).*

**Don't:**
- Don't align services on technical layers (frontend/backend/datalayer)
  — Conway's Law will force a distributed monolith.
  *Ref: Microservices Up And Running.md — "DDD and Microservice Boundaries" (`page-59-0`).*

---

### Data Architecture: Independence + Event Sourcing + CQRS

**Principle:** Each microservice owns its data. No shared databases. Use
the right tool for each service.

**Do:**
- Apply the **Database-per-Service** pattern; avoid the **Shared
  Database** anti-pattern.
  *Ref: Microservices Up And Running.md — "Microservices Embed Their Data" (`page-77-0`).*
- **Match the data store to the use case**:
  - **Redis** for fast in-memory key/value with `HSETNX` (atomic
    set-if-not-exists) for seat reservations:
    ```text
    > HSETNX flight:40d1-898d-bf84a266f1b9 12C e0392920-...  -> 1
    > HSETNX flight:40d1-898d-bf84a266f1b9 12C 083a6fc2-...  -> 0 (already reserved)
    ```
    *Ref: Microservices Up And Running.md — "Redis for the Reservations Data Model" (`page-224-0`).*
  - **MySQL with native JSON columns** for complex seat-map objects that
    need relational queries by `(flight_no, flight_date)`:
    ```sql
    CREATE TABLE seat_maps (
      flight_no varchar(10) PRIMARY KEY,
      seat_map json NULL,
      origin_code varchar(10) NULL,
      destination_code varchar(10) NULL
    );
    CREATE TABLE flights (
      flight_id varchar(36) PRIMARY KEY,
      flight_no varchar(10),
      flight_date datetime(0),
      FOREIGN KEY(flight_no) REFERENCES seat_maps(flight_no)
    );
    SELECT seat_map->>"$.Cabin[0].firstRow" FROM seat_maps;
    ```
    *Ref: Microservices Up And Running.md — "MySQL Data Model" (`page-226-0`).*
- Use **Event Sourcing** when you need a full audit trail, time-travel
  queries, or natural read-model decoupling. The state is the *projection*
  of all events replayed in order.
  *Ref: Microservices Up And Running.md — "Event Sourcing" (`page-85-0`).*
- Use **CQRS** (Command Query Responsibility Segregation) to separate
  write models from optimized read models — pairs naturally with Event
  Sourcing.
  *Ref: Microservices Up And Running.md — "Command Query Responsibility Segregation" (`page-93-0`).*
- Apply **Rolling Snapshots** as a performance optimization to avoid
  replaying all events from time-zero.
  *Ref: Microservices Up And Running.md — "Improving Performance with Rolling Snapshots" (`page-91-0`).*

**Don't:**
- Don't use shared databases to "simplify" cross-service queries — it
  creates tight coupling. The data delegate pattern can help during
  migration but should not be the steady state.
  *Ref: Microservices Up And Running.md — "Data Delegate Pattern" (`page-79-0`).*

---

### Infrastructure Pipeline (Terraform + GitHub Actions)

**Principle:** All infrastructure defined in version-controlled code; no
manual changes; immutable.

**Do:**
- Use **Terraform** with the **S3 backend** for state — never local
  state, so the team can share.
  *Ref: Microservices Up And Running.md — "Creating an S3 Backend for Terraform" (`page-115-0`).*
- One **Git repository per environment** (sandbox / staging / prod).
  *Ref: Microservices Up And Running.md — "Creating the Sandbox Repository" (`page-117-0`).*
- **Trigger the pipeline on Git tag creation** (tags starting with `v`):
  install deps → `terraform fmt` → `terraform validate` → `terraform plan`
  → `terraform apply` → publish kubeconfig as a downloadable artifact.
  *Ref: Microservices Up And Running.md — "Building the IaC Pipeline" (`page-123-0`).*
- Store AWS credentials as **GitHub secrets**; never in code.
  *Ref: Microservices Up And Running.md — "Store AWS credentials as GitHub secrets" (`page-131-0`).*
- Follow the **Twelve-Factor App** principles for runtime configuration.
  *Ref: Microservices Up And Running.md — "Twelve-Factor App" (`page-237-0`).*

**Don't:**
- Don't make manual infrastructure changes — they create drift and are
  invisible to VCS.
  *Ref: Microservices Up And Running.md — "Immutable Infrastructure" (`page-99-0`).*
- Don't keep Terraform state locally — concurrent pipelines will collide.
  *Ref: Microservices Up And Running.md — "Creating an S3 Backend for Terraform" (`page-115-0`).*

---

### Microservices Infrastructure (VPC, EKS, Argo CD)

**Principle:** The platform team provides self-service infrastructure
"as a service" so microservices teams don't reinvent it.

**Do:**
- **Network module** (Terraform) — VPC with public + private subnets across
  two AZs, NAT gateways with elastic IPs, internet gateway, route tables.
  *Ref: Microservices Up And Running.md — "The Network Module" (`page-145-0`).*
- **Kubernetes module** — AWS EKS managed cluster with managed node
  group; tag resources for EKS integration.
  *Ref: Microservices Up And Running.md — "The Kubernetes Module" (`page-160-0`).*
- **Argo CD module** — install via Helm into a dedicated `argo` namespace
  for GitOps.
  *Ref: Microservices Up And Running.md — "Setting Up Argo CD" (`page-171-0`).*
- Use **`terraform destroy`** to tear down sandbox environments when
  done — the entire environment is reproducible from code.
  *Ref: Microservices Up And Running.md — "Cleaning Up the Infrastructure" (`page-177-0`).*

---

### Developer Workspace (10 Guidelines)

**Principle:** A new developer should be productive in under an hour.
Reproducible, language-agnostic, Docker-first.

**Do — the 10 guidelines:**
- 1. **Docker is the only dependency.** No assumptions about installed
  languages or tools.
  *Ref: Microservices Up And Running.md — "Guideline 1" (`page-181-0`).*
- 2. **Remote or local shouldn't matter** — same setup on laptop and CI.
- 3. **Heterogeneous-ready workspace** — use the **Rule of Twos**: at
  least two alternatives in production for any critical component.
  *Ref: Microservices Up And Running.md — "Guideline 3" (`page-182-0`).*
- 4. **Run a single microservice or a subsystem with equal ease.**
- 5. **Run databases locally** — Docker-ize them (e.g., `docker-compose`
  with MySQL, Cassandra, MinIO for S3).
  *Ref: Microservices Up And Running.md — "Testing Docker" (`page-207-0`).*
- 6. **Use Dockerfile + docker-compose for local containerization**;
  multistage builds; hot-reload; debug support.
- 7. **Database migrations are codified** — all schema changes as date-ordered
  scripts, run automatically on startup.
  *Ref: Microservices Up And Running.md — "Guideline 7" (`page-199-0`).*
- 8. **Pragmatic testing** — test-first, test-as-you-code, or test-after is
  fine; all must be merged with tests.
  *Ref: Microservices Up And Running.md — "Guideline 8" (`page-200-0`).*
- 9. **Branching hygiene** — feature branches, no merge without green tests,
  linters block pushes.
  *Ref: Microservices Up And Running.md — "Guideline 9" (`page-201-0`).*
- 10. **Common `make` targets** in every repo:
  ```makefile
  start:    # run the service
  stop:     # stop the service
  build:    # build container image
  test:     # run all tests + coverage
  tests-unit:  # unit only
  tests-at:    # acceptance only
  lint:     # style checks
  migrate:  # apply DB migrations
  add-migration: # create new migration
  logs:     # tail logs in container
  exec:     # run a command in the container
  ```
  *Ref: Microservices Up And Running.md — "Guideline 10" (`page-201-0`).*
- Use **Multipass** (Ubuntu VMs on macOS/Windows via HyperKit/Hyper-V)
  to install Docker + Compose in a reproducible way.
  *Ref: Microservices Up And Running.md — "Installing Multipass" (`page-203-0`).*
- **Avoid local Kubernetes** for day-to-day dev — Docker Compose covers
  90% of needs; use k3s/MicroK8s only for targeted Kubernetes tests.
  *Ref: Microservices Up And Running.md — "Avoid Using Kubernetes Locally Unless You Must" (`page-208-0`).*

---

### Developing Microservices: Heterogeneous Stacks

**Principle:** Pick the best tech stack per service. Demonstrate the
architecture is *not* coupled to one technology.

**Do:**
- Start new microservices from a **stack-specific template** (e.g.,
  NodeBootstrap for Node.js; Flask template for Python).
  *Ref: Microservices Up And Running.md — "Key Decision: Start Microservices with Reusable Templates" (`page-227-0`).*
- Implement `ms-flights` in **Node.js + Express + MySQL** for relational
  + complex JSON queries.
- Implement `ms-reservations` in **Python + Flask + Redis** for
  in-memory seat-booking concurrency control (HSETNX).
  *Ref: Microservices Up And Running.md — "Implementing the Data for a Microservice" (`page-223-0`).*
- Provide standard **health endpoints**:
  - `/ping` — liveness, lightweight
  - `/health` — readiness, includes DB query
  *Ref: Microservices Up And Running.md — "Health Checks" (`page-218-0`).*
- Serve the **OAS at `/docs`** (via Redocly) so consumers always have the
  contract.
  *Ref: Microservices Up And Running.md — "Health Checks / docs" (`page-218-0`).*
- Use **Traefik** as edge router with path-prefix routing in the
  umbrella workspace; run multiple services together with one
  `docker-compose.yml`.
  *Ref: Microservices Up And Running.md — "Hooking Services Up with an Umbrella Project" (`page-226-0`).*

---

### Releasing Microservices (CI → Container → GitOps)

**Principle:** Three independent repos = three independent pipelines,
each owned by the right team.

**Do:**
- **Repository 1** (Platform Team) — Terraform infrastructure.
  *Ref: Microservices Up And Running.md — "Three separate GitHub repositories" (`page-263-0`).*
- **Repository 2** (Microservices Team) — code → unit tests → `docker
  build` → push to Docker Hub on a GitHub release tag. Container must be
  **environment-agnostic**.
  *Ref: Microservices Up And Running.md — "Shipping the Flight Information Container" (`page-241-0`).*
- **Repository 3** (Release Team) — Helm chart + Argo CD application.
  ```text
  ms-deploy/
    Chart.yaml
    values.yaml
    templates/
      deployment.yaml
      service.yaml
      ingress.yaml
  ```
  Deployment template specifies container image, env vars (MySQL host),
  ports, and liveness/readiness probes.
  *Ref: Microservices Up And Running.md — "Creating a Helm Chart" (`page-248-0`).*
- Use **Argo CD** to deploy by syncing the Helm chart to the cluster —
  the deployment repo is the source of truth.
  *Ref: Microservices Up And Running.md — "Argo CD for GitOps Deployment" (`page-255-0`).*

**Don't:**
- Don't bake environment-specific values into the container image —
  pass them via Helm `values.yaml`.
  *Ref: Microservices Up And Running.md — "Container is environment-agnostic" (`page-242-0`).*

---

### Managing Change: Three Deployment Patterns

**Principle:** Match deployment pattern to risk; measure outcomes.

**Do:**
- **Blue-Green** — two parallel environments; deploy to idle; switch
  traffic when ready. Zero-downtime but needs persistent data
  synchronization.
  *Ref: Microservices Up And Running.md — "Three Deployment Patterns" (`page-266-0`).*
- **Canary** — release new version alongside, route small % traffic,
  grow if healthy. **Finer-grained** than blue-green; works well with
  independently deployable services.
  *Ref: Microservices Up And Running.md — "Three Deployment Patterns" (`page-267-0`).*
- **Multiple Versions** — explicitly version APIs and run side-by-side.
  Reduces coordination but increases maintenance; eventually contract.
  *Ref: Microservices Up And Running.md — "Three Deployment Patterns" (`page-267-0`).*
- Be **data-oriented**: collect *change time per microservice*,
  *frequency of changes*, *runtime latency*, *inter-service dependencies*.
  *Ref: Microservices Up And Running.md — "Be Data-Oriented" (`page-264-0`).*
- Track the **four change-impact factors**: implementation time,
  coordination time, downtime, consumer impact.
  *Ref: Microservices Up And Running.md — "The Impact of Changes" (`page-265-0`).*

---

### Microservices Quadrant (Self-Assessment)

**Principle:** Use the *Microservices Quadrant* to track your transformation
maturity along independent axes (people/process maturity ×
tool/technology maturity).

**Do:**
- Re-assess at every major milestone; don't declare victory on the
  technology side without proportional investment in the people side.
  *Ref: Microservices Up And Running.md — "Microservices Quadrant" (`page-283-0`).*
- *Clean up* sandbox environments with `terraform destroy` — they're
  reproducible from code, so destroying them is low-risk and avoids AWS
  charges.
  *Ref: Microservices Up And Running.md — "Clean Up" (`page-260-0`).*

---

## Anti-Patterns & Common Mistakes
- **Shared database between microservices.** *fix:* one DB per service, even
  if it means duplication. *Ref: Microservices Up And Running.md — "Shared Database" (`page-78-0`).*
- **Microservices calling microservices directly.** *fix:* always go through
  the BFF API for orchestration. *Ref: Microservices Up And Running.md — "Key Decision: Avoid Microservices Calling Each Other Directly" (`page-213-0`).*
- **Adopting only the technical half of microservices.** *fix:* apply the
  Team Topologies operating model; people are the harder half. *Ref: Microservices Up And Running.md — "Quadrant" (`page-283-0`).*
- **Designing on technical layers.** *fix:* align on bounded contexts
  (DDD). *Ref: Microservices Up And Running.md — "DDD and Microservice Boundaries" (`page-59-0`).*
- **Baking environment config into the container image.** *fix:* pass
  via Helm `values.yaml` + Kubernetes env vars. *Ref: Microservices Up And Running.md — "Container is environment-agnostic" (`page-242-0`).*
- **Bigger teams to "go faster".** *fix:* cap at 5–8; add teams, not
  people. *Ref: Microservices Up And Running.md — "Team Size" (`page-32-0`).*
- **Shared communication library across services.** *fix:* heterogeneous
  stacks; no shared client lib. *Ref: Microservices Up And Running.md — "Long feedback loops" (`page-21-0`).*
- **Manual schema changes.** *fix:* migration scripts ordered by date,
  automated on startup. *Ref: Microservices Up And Running.md — "Guideline 7" (`page-199-0`).*
- **No health checks.** *fix:* always expose `/ping` (liveness) and
  `/health` (readiness) so Kubernetes can manage the lifecycle.
  *Ref: Microservices Up And Running.md — "Health Checks" (`page-218-0`).*

---

## Decision Heuristics / Checklists
- **Service boundary size?** Start with bounded contexts (coarse), not
  technical layers. Split later.
- **Data store?** Match the data structure to the use case: Redis for
  HSETNX seat-locking; MySQL JSON for complex relational seat maps.
  Apply the **Rule of Twos** (at least two alternatives in production).
- **Inter-service call?** Always through the BFF API. Never direct.
- **Team size?** 5–8 people. Add a team before adding members.
- **Schema change?** Migration script + applied on container start.
  Backwards-compatible.
- **Container image trigger?** GitHub release tag → unit tests → build →
  push to Docker Hub. Never bake env config.
- **Deployment pattern?** Rolling update for safe changes; full-stop for
  topology change; event-based migration for breaking schema change;
  blue-green for stateless services that produce no events.
- **When to do Event Sourcing?** When you need a complete audit trail,
  time-travel queries, or natural read-model decoupling.
- **When to write an ADR?** For every key decision the team makes —
  and "not deciding" is also a decision worth recording.

---

## Key Takeaways
1. **Minimize coordination costs.** This is the *only* reason to choose
   microservices. If your problem is simpler, use a monolith.
2. **Design team & coordination first, system second.** Conway's Law will
   encode your org chart into your architecture. Use Team Topologies.
3. **Use SEED(S)** for repeatable service design: actors → JTBDs →
   sequence diagrams → actions/queries → OAS → stack → code.
4. **Enforce data independence.** One DB per service. Right tool per use
   case. Heterogeneity is a feature, not a bug.
5. **Invest in IaC and immutable infrastructure.** Terraform + S3 backend
   + GitHub Actions + per-environment repos. Never touch prod by hand.
6. **GitOps everything.** Argo CD watches the deployment repo; the
   deployment repo is the source of truth; environment is reproducible.
7. **Pick the right deployment pattern** for the change: rolling update
   for safe changes, full-stop for topology, event-based migration for
   breaking schema, blue-green for stateless services.
8. **Standardize the developer experience.** Docker + make + ten
   workspace guidelines. A new dev is productive in under an hour.
9. **Use heterogeneous stacks on purpose.** A working fleet with two
   different languages / databases proves the architecture isn't tied to
   one technology.
10. **Record decisions.** ADRs as text files in VCS. Light, immutable
    (use "Superseded" status to update). Future-you thanks present-you.

---

## Cross-References
- Related: `../Monolith_To_Microservices.md` (the migration path that gets
  you to a place where this playbook applies).
- Related: `../Enabling_Microservice_Success.md` (the organizational
  readiness companion).
- Related: `../Building_Event-driven_Microservices.md` (the in-service
  patterns for the microservices the BFF API will orchestrate).
- Related: `../Building_An_Event-Driven_Data_Mesh.md` (when the embedded
  data stores need to grow into data products).
- Topic index: `../INDEX.md`
