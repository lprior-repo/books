# Microservices Up & Running -- Comprehensive Summary

**Authors:** Ronnie Mitra & Irakli Nadareishvili

## Overview

*Microservices Up & Running* is a step-by-step guide to building a microservices architecture from the ground up. The book walks through the entire lifecycle: establishing guiding principles, defining an operating model with team responsibilities, designing services using a repeatable methodology, building cloud infrastructure with infrastructure-as-code, implementing heterogeneous microservices with different tech stacks, and deploying them using GitOps. The authors anchor their guidance in a running example: a flight management system with two microservices (flights and reservations) built on AWS with Kubernetes.

---

## Chapter 1: Why Microservices?

Microservices architectures offer faster change speeds, better scalability, and cleaner, evolvable system designs. However, implementing your first microservices architecture is difficult because of the myriad technical and organizational choices involved. This book provides a structured, end-to-end implementation journey based on proven techniques.

The authors introduce the concept that microservices are most beneficial when applied to complex systems. For simpler systems, a monolith may be more appropriate. The key value proposition is that microservices reduce the cost of change by enabling independent deployability, bounded contexts, and team autonomy. The book is organized around a phased approach: principles and operating model, design methodology, data architecture, infrastructure, development, release, and change management.

---

## Chapter 2: Operating Model

Before writing any code, the authors insist on defining an explicit operating model -- the organizational structure, team responsibilities, and guidelines for how teams work together. This is a deliberate choice: microservices fail not because of technology, but because of organizational dysfunction.

**Team Structure:** The model defines five key teams:

1. **Product Team** -- Owns the product vision, prioritizes features using Jobs-to-be-Done (JTBD), and works with customers.
2. **Platform Team** -- Builds and maintains the shared infrastructure platform (networking, Kubernetes, databases, CI/CD pipelines). Offers infrastructure as a service to other teams.
3. **Microservices Teams** -- Each team owns one or more microservices end to end: design, development, testing, and delivery. They are the primary builders.
4. **Release Team** -- Responsible for deploying microservices into production and production-like environments. They own the deployment process and tools.
5. **API Team** -- Owns the "backend for frontend" (BFF) APIs that compose microservices into cohesive experiences for client applications. BFF APIs are thin orchestration layers with no business logic.

**Key Principles:**
- Teams should be autonomous and minimize coordination with other teams.
- Microservices should not call each other directly; orchestration happens at the BFF API layer.
- Each team has a clear domain of ownership and responsibility.
- The operating model should be explicit, documented, and agreed upon by all stakeholders.

The authors emphasize that coordination minimization is a primary success factor. The more teams need to coordinate, the slower and more fragile the system becomes.

---

## Chapter 3: Microservices Design with SEED(S)

This chapter introduces the **SEED(S) method** -- Seven Essential Evolutions of Design for Services. It is a top-down, multi-step methodology where each step evolves from the previous one.

**The Seven Steps:**

1. **Identify Actors** -- Determine who interacts with the system: customers, applications, APIs, and microservices.

2. **Collect Jobs-to-be-Done (JTBD)** -- Capture user needs in a structured format: "When [situation], the [actor] needs [need], so that [outcome]." These come from customer interviews and business analysis.

3. **Describe Interactions** -- Use UML sequence diagrams (in PlantUML format) to visualize how actors interact to fulfill each JTBD. This reveals which microservices need to communicate and in what order.

4. **Compile Actions and Queries** -- Translate interactions into concrete API operations. Actions modify state (commands); queries read state. This bridges the gap between business-oriented JTBD and technical specifications.

5. **Design an OpenAPI Specification (OAS)** -- Translate actions and queries into a formal RESTful API specification using the OpenAPI standard. This becomes the contract for the microservice.

6. **Select Technologies** -- Choose the appropriate programming language, framework, and data storage for each microservice. Heterogeneous stacks are encouraged.

7. **Write Code** -- Implement the microservice based on the OAS and technology choices.

The authors stress that BFF APIs should orchestrate microservices, not the other way around. Direct microservice-to-microservice calls should be avoided to minimize coupling. The OAS serves as both documentation and contract, and can be rendered with tools like Swagger Editor for easy visualization.

---

## Chapter 4: Finding Service Boundaries

This chapter addresses the critical question: how do you slice a big application into a collection of microservices? The authors introduce **Event Storming** as the primary discovery technique.

**Event Storming** is a collaborative workshop where participants write domain events on sticky notes and arrange them chronologically. Events represent things that happen in the business domain (e.g., "Flight Scheduled," "Seat Reserved," "Payment Received"). Participants then group related events into clusters, which naturally reveal **bounded contexts** -- cohesive areas of the business with clear boundaries.

**Bounded Contexts** come from Domain-Driven Design (DDD). Each bounded context represents a distinct area of the business with its own ubiquitous language, data models, and business rules. Microservices should initially be aligned with bounded contexts.

**Key Guidelines:**
- Start with coarse-grained services aligned to bounded contexts. Do not create too many microservices too early.
- Services should be **loosely coupled** (changes in one don't ripple to others) and **highly cohesive** (related functionality stays together).
- Increase the number of microservices slowly over time. It is acceptable for early services to be larger than their target state.
- Avoid the trap of designing an overly granular system at the outset.

The authors reference Sam Newman's foundational rules: loose coupling, high cohesion, and the principle that services should be small enough for a single team to own but not so small that they create excessive operational overhead.

---

## Chapter 5: Data Architecture

Data is one of the most difficult aspects of microservices design. The chapter introduces the principle of **data independence**: each microservice owns and manages its own data store. No microservice should share a database with another.

**Why Data Independence Matters:**
- Shared databases create tight coupling between services.
- Schema changes in a shared database can break multiple services simultaneously.
- Independent data stores allow each team to choose the right database technology for their use case.

**Database Patterns:**

- **Database per Service** -- Each microservice has its own dedicated database instance.
- **Shared Database (anti-pattern)** -- Multiple services reading/writing the same database. Avoid this.

**Event Sourcing** is introduced as an advanced pattern where instead of storing current state, you store the sequence of events that led to the current state. The current state is derived by replaying events (a "projection"). This enables:
- Complete audit trail
- Time-travel queries (state at any point in time)
- Natural decoupling between events and read models

**CQRS (Command Query Responsibility Segregation)** separates the write model (commands) from the read model (queries). Commands modify state; queries read from optimized read stores. This pattern pairs naturally with Event Sourcing.

**Rolling Snapshots** are introduced as a performance optimization for Event Sourcing. Instead of replaying all events from the beginning of time, periodic snapshots capture intermediary state, reducing the computational cost of projections.

The chapter emphasizes that these patterns are tools, not mandates. Use them when the complexity they address actually exists in your system.

---

## Chapter 6: Infrastructure as Code (IaC) Pipeline

This chapter focuses on establishing the infrastructure foundation using immutable infrastructure and infrastructure-as-code principles. The tool of choice is **Terraform**.

**Key Decisions:**
- Use Terraform for declarative infrastructure definition.
- Store Terraform state in an AWS S3 backend (not locally) to enable sharing and avoid conflicts.
- Use GitHub Actions for CI/CD pipeline automation.
- One Git repository per environment (sandbox, staging, production).

**Setting Up AWS:**
1. Create an AWS account and configure an IAM operator user with appropriate permissions.
2. Create an S3 bucket for Terraform state storage.
3. Install Terraform, AWS CLI, and Git locally.

**Terraform Concepts:**
- **Backends** -- Where Terraform stores state (S3 in this case).
- **Providers** -- Libraries for interacting with cloud APIs (AWS provider).
- **Resources** -- Declarations of infrastructure objects (VPCs, subnets, etc.).
- **Modules** -- Reusable, encapsulated infrastructure code (like functions in programming).

**Building the Pipeline:**
1. Create a GitHub repository for the sandbox environment.
2. Write a starter `main.tf` Terraform file with S3 backend configuration.
3. Create a GitHub Actions workflow that:
   - Triggers on Git tag creation (tags starting with "v").
   - Installs dependencies (AWS IAM Authenticator, Istio CLI, Terraform).
   - Formats, validates, plans, and applies Terraform code.
   - Publishes a kubeconfig file as a downloadable artifact.
4. Store AWS credentials as GitHub secrets.
5. Test the pipeline by pushing a version tag.

The workflow follows an immutable infrastructure model: changes are made through code, tested in a pipeline, and applied automatically. Manual infrastructure changes are eliminated.

---

## Chapter 7: Building a Microservices Infrastructure

This chapter implements three infrastructure components using Terraform modules:

**1. Network Module (module-aws-network):**
- Creates a Virtual Private Cloud (VPC) with CIDR block configuration.
- Defines four subnets across two availability zones: two public, two private.
- Sets up an internet gateway for public subnet routing.
- Configures NAT gateways with elastic IPs for private subnet outbound access.
- Creates route tables and associations for all subnets.
- Adds Kubernetes-specific tags for EKS integration.

**2. Kubernetes Module (module-aws-kubernetes):**
- Uses AWS EKS (Elastic Kubernetes Service) as a managed Kubernetes offering.
- Configures IAM roles and policies for the cluster control plane and node groups.
- Defines a security group for cluster networking.
- Creates an EKS cluster referencing the VPC and subnets from the network module.
- Sets up a managed node group with configurable instance types, disk sizes, and scaling parameters.
- Generates a kubeconfig file for remote cluster access.

**3. Argo CD Module (module-argo-cd):**
- Installs Argo CD into the Kubernetes cluster using Helm.
- Uses Terraform's Kubernetes and Helm providers.
- Creates a dedicated namespace ("argo") for the installation.
- Receives cluster connection details from the Kubernetes module outputs.

**Sandbox Environment:**
All three modules are composed in a sandbox environment definition that passes outputs from one module as inputs to the next. The environment is provisioned through the CI/CD pipeline by pushing version tags. After provisioning, the infrastructure is tested using kubectl commands to verify cluster connectivity and Argo CD pod status.

The chapter concludes with instructions for cleaning up (destroying) the infrastructure using `terraform destroy` to avoid incurring AWS charges.

---

## Chapter 8: Developer Workspace

This chapter focuses on creating an exceptional developer experience through standardized, containerized development environments. The authors argue that investing early in developer tooling is one of the most underappreciated prerequisites for successful microservices adoption.

**Three High-Level Goals:**
1. Code can be set up in a short time frame (under an hour for a new developer).
2. New microservices can be created quickly, easily, and predictably using templates.
3. Quality control must be automated.

**10 Workspace Guidelines:**

1. **Make Docker the only dependency.** No assumptions about installed languages or tools. Everything runs in containers.
2. **Remote or local should not matter.** Setup works identically on laptops and cloud servers.
3. **Ensure a heterogeneous-ready workspace.** Support multiple languages and databases. Practice the "Rule of Twos" -- use at least two alternatives in production for any critical component.
4. **Running a single microservice and/or a subsystem should be equally easy.** Developers should be able to work on individual services or groups of services with equal convenience.
5. **Run databases locally if possible.** Provide Docker-ized alternatives for all databases (e.g., MinIO for S3).
6. **Implement containerization guidelines.** Use Dockerfiles for building images, Docker Compose for running locally. Use multistage builds. Enable hot-reloading and debugger support.
7. **Establish rules for painless database migrations.** All schema changes must be codified in migration scripts, ordered by date, and automated as part of builds.
8. **Determine a pragmatic automated testing practice.** Support test-first, test-as-you-code, or test-after approaches. Use idiomatic frameworks for each stack.
9. **Branching and merging.** All development on feature branches. No merge without passing tests. Linting errors should block pushes.
10. **Common targets in a makefile.** Every repository should have a makefile with standard targets: `start`, `stop`, `build`, `test`, `lint`, `migrate`, `logs`, etc.

**Container Setup:**
- Use Multipass (from Canonical) for lightweight Ubuntu VMs on macOS/Windows.
- Install Docker and Docker Compose inside the VM.
- Test with MySQL using a simple docker-compose file.
- Advanced example: install Cassandra in Docker for more complex data needs.
- Local Kubernetes options include k3s, MicroK8s, and Minikube, though the authors recommend avoiding local Kubernetes for everyday development unless specifically needed.

---

## Chapter 9: Developing Microservices

This chapter implements two microservices for a flight management system using the SEED(S) methodology from Chapter 3.

**Design Phase:**
1. **Actors identified:** Customer, Web App, BFF API, ms-flights, ms-reservations.
2. **JTBDs collected:** "When a customer interacts with the UI, the app needs to render a seating chart" and "When a customer is finalizing a booking, the web app needs to reserve a seat."
3. **Sequence diagrams** show the BFF API orchestrating calls to both microservices.
4. **Actions and queries** are compiled for each service:
   - ms-flights: Get flight details (query), Get flight seating map (query).
   - ms-reservations: Get reserved seats for a flight (query), Reserve a seat (action).
5. **OpenAPI Specifications** are designed for both services.

**Key Design Decision:** Avoid microservices calling each other directly. The BFF API orchestrates all inter-service communication.

**Implementation -- ms-flights (Node.js + MySQL):**
- Bootstrapped from the NodeBootstrap template.
- Uses Express.js for routing with input validation via the Spieler library.
- MySQL for data storage with native JSON column support for complex seat map objects.
- Two tables: `seat_maps` (with JSON seat_map column) and `flights` (with foreign key to seat_maps).
- Database migrations managed via db-migrate tool, applied automatically on project start.
- Health checks implemented: `/ping` for liveness, `/health` for readiness (includes database query).
- OAS rendered at `/docs` endpoint using Redocly.

**Implementation -- ms-reservations (Python + Redis):**
- Bootstrapped from a GitHub template repository for Flask.
- Uses Redis hashes for data storage -- the HSETNX command naturally prevents double-booking.
- Redis hash keys: `flight:{flight_id}` with seat numbers as field keys and customer IDs as values.
- Two endpoints: PUT `/reservations` to reserve a seat, GET `/reservations` to list reserved seats.
- Follows Twelve-Factor App principles for configuration management.

**Umbrella Project:**
To run both microservices together, the authors introduce an umbrella workspace using Faux Git Submodules. This allows developers to clone multiple service repositories under one workspace and start/stop them together. Traefik is used as an edge router to route requests to the appropriate service based on URL path prefixes.

---

## Chapter 10: Releasing Microservices

This chapter brings everything together: staging infrastructure, container delivery, and GitOps deployment.

**Setting Up the Staging Environment:**
- Fork a pre-built staging infrastructure repository.
- Add three new infrastructure components: Traefik ingress controller, AWS RDS MySQL database, and AWS ElastiCache Redis.
- Configure GitHub secrets for AWS credentials and MySQL password.
- Update Terraform code with environment-specific values (S3 bucket, AWS region).
- Add IAM permissions for database resources (RDS and ElastiCache).
- Provision through the CI/CD pipeline using version tags.
- Verify cluster access with kubectl and create a Kubernetes secret for the MySQL password.

**Shipping the Container:**
- Use Docker Hub as the container registry.
- Create a GitHub Actions workflow in the ms-flights repository that:
  1. Runs unit tests.
  2. Builds a containerized version of the microservice.
  3. Pushes the container to Docker Hub.
- The container is environment-agnostic -- no environment-specific logic is baked in.
- Trigger the workflow by creating a GitHub release with a version tag.

**Deploying with Argo CD:**
- Create a deployment repository (ms-deploy) containing Helm charts.
- Helm chart structure: Chart.yaml (metadata), values.yaml (configuration), templates/ (Kubernetes YAML).
- Key Kubernetes objects: Deployment (Pod specification with replicas), Service (network endpoint), Ingress (routing rules).
- The deployment template specifies container image, environment variables (MySQL connection), ports, and liveness/readiness probes.
- Values file parameterizes environment-specific configuration (image tag, database host, ingress rules).
- Test with `helm install --debug --dry-run`.
- Use Argo CD to create an application pointing to the Helm chart in the deployment repository.
- Synchronize to deploy. Argo CD applies the Helm chart to the Kubernetes cluster.
- Test the deployed service by curling the Traefik load balancer with the appropriate Host header.

**Architecture of the Release:**
Three separate GitHub repositories each with their own pipeline:
1. Infrastructure repository -- Terraform-based environment provisioning.
2. Microservice code repository -- Build and push container images.
3. Deployment repository -- Helm charts for Argo CD.

This separation aligns with the operating model: platform team owns infrastructure, microservices teams own code, release team owns deployment.

---

## Chapter 11: Managing Change

The final chapter evaluates the architecture from the perspective of change -- the whole point of microservices.

**Types of Change:**
- **Extrinsic drivers:** New product launches, bug fixes, partner integrations (driven by business needs).
- **Intrinsic drivers:** Splitting services, redeploying infrastructure, optimizing pipelines (driven by system observation).

The authors advocate being **data-oriented** -- collect metrics like change time per microservice, frequency of changes, runtime latency, and inter-service dependencies to guide improvement decisions.

**Four Change Impact Factors:**
1. **Implementation time** -- How long the change takes to make.
2. **Coordination time** -- How much cross-team communication is required.
3. **Downtime** -- How long the system is unavailable during change.
4. **Consumer impact** -- How the change affects users and dependent systems.

**Three Deployment Patterns:**

1. **Blue-Green Deployment:** Two parallel environments (live and idle). Changes applied to idle; traffic switched when ready. Enables zero-downtime but requires handling persistent data synchronization.

2. **Canary Deployment:** Release new version alongside existing version. Route a small percentage of traffic to the canary. Gradually increase traffic if healthy. Finer-grained than blue-green. Works well with independently deployable microservices.

3. **Multiple Versions:** Explicitly version APIs and run multiple versions in parallel. Useful when changes require clients to also change. Reduces coordination but increases maintenance burden. Eventually requires version contraction.

**Infrastructure Change Assessment:**
- Immutable infrastructure and IaC make infrastructure changes traceable, repeatable, and testable.
- Adding new resources (extending) has low impact; altering existing resources requires more care.
- The CI/CD pipeline automates testing and validation.
- Infrastructure drift is detectable and correctable through Terraform.

**Microservices Change Assessment:**
- Independent deployability is the key strength. Each service can be changed and deployed without affecting others.
- Container-based deployment ensures consistent runtime across environments.
- Health checks enable Kubernetes to manage the service lifecycle automatically.
- Helm charts make deployment configurations reusable and parameterizable.
- Argo CD provides declarative, auditable deployment management.

**Data Change Assessment:**
- Data independence means schema changes in one service don't affect others.
- Database migrations are codified and automated.
- Event Sourcing and CQRS provide patterns for evolving data models without breaking consumers.
- Data synchronization across services is handled through events or API contracts, not shared databases.

**Organizational Change:**
- The explicit operating model makes team boundaries clear.
- Autonomy reduces coordination costs.
- The platform team's self-service model empowers microservices teams.
- As the system evolves, teams may need to be restructured (Conway's Law in reverse).

---

## Key Takeaways

1. **Start with principles and an operating model, not technology.** Define team responsibilities, communication patterns, and decision-making frameworks before writing any code. The operating model is the foundation upon which everything else is built.

2. **Minimize coordination.** The single most important success factor is reducing the need for teams to coordinate. Independent teams working on independent services with independent data stores move faster and break less.

3. **Use a repeatable design methodology (SEED(S)).** Go from actors to JTBDs to sequence diagrams to actions/queries to OpenAPI specs to code. This structured approach produces consistently high-quality, customer-centric service designs.

4. **Align services with bounded contexts, not technical layers.** Use Event Storming to discover natural domain boundaries. Start coarse-grained and split services over time as understanding deepens. Never create too many microservices too early.

5. **Enforce data independence.** Each microservice owns its data. No shared databases. Choose the right database technology for each service's needs (Redis for reservations, MySQL for flights). This eliminates schema-coupling and enables heterogeneous data architectures.

6. **Invest in infrastructure as code and immutable infrastructure.** Use Terraform modules for all infrastructure. Automate provisioning through CI/CD pipelines. Never make manual changes to environments. This makes infrastructure changes safe, repeatable, and auditable.

7. **Create an exceptional developer experience.** Standardize on Docker as the only dependency. Use makefiles with common targets. Provide templates for each tech stack. Ensure new developers can be productive in under an hour. Developer experience is an underappreciated competitive advantage.

8. **Practice heterogeneity deliberately.** Use the "Rule of Twos" -- maintain at least two different tech stacks in production. This proves the architecture works as intended and prevents accidental coupling to a single technology.

9. **Use BFF APIs for orchestration, not inter-service calls.** Microservices should not call each other directly. A thin API layer composes and orchestrates services, keeping them decoupled and independently deployable.

10. **Automate the entire delivery pipeline.** From code commit to container build to deployment, everything should be automated. Use GitHub Actions for CI/CD, Docker Hub for container registry, Helm for packaging, and Argo CD for GitOps-based deployment. The deployment repository becomes the source of truth.

11. **Design for change.** Use blue-green and canary deployment patterns. Version APIs explicitly when breaking changes are needed. Collect metrics to guide improvement decisions. Be data-oriented about both extrinsic and intrinsic change.

12. **Clean up resources.** AWS EKS and related resources incur charges even when idle. Use `terraform destroy` to tear down environments when not in use. The entire environment is reproducible from code, so destroying it is low-risk.
