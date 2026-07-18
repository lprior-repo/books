# Infrastructure as Code, Third Edition - Comprehensive Summary

**Author:** Kief Morris
**Published:** March 2025 (O'Reilly Media)
**Subtitle:** Designing and Delivering Dynamic Systems for the Cloud Age

---

## Part I: Foundations

### Chapter 1: What Is Infrastructure as Code?

Infrastructure as Code (Iac) is the practice of provisioning and managing infrastructure using code rather than command-line tools or GUI-based "ClickOps." More broadly, it means applying the principles, practices, and tools of software engineering to infrastructure -- test-driven development (TDD), continuous integration (CI), continuous delivery (CD), and sound software design principles.

The book frames the evolution of IT through eras: the **Iron Age** of physical hardware and manual processes; the **Shadow Age** where cloud and DevOps were used quietly by startups; the **Age of Sprawl** where organizations adopted cloud rapidly and created uncontrolled proliferation of platforms and tools; and the emerging **Age of Sustainable Growth** where organizations must rationalize systems and manage costs while continuing to innovate.

A central thesis is that organizations must **optimize for change**. The DORA/Accelerate research proves there is no trade-off between speed and quality -- high performers excel at both. The **Four Key Metrics** for measuring delivery effectiveness are: Delivery Lead Time, Deployment Frequency, Change Fail Percentage, and Mean Time to Restore (MTTR). Organizations that perform well against these metrics also perform well against their business goals.

Three **core practices** underpin effective Infrastructure as Code:
1. **Define everything as code** -- for reusability, consistency, and visibility.
2. **Continually test and deliver all work in progress** -- build quality in rather than testing it in after the fact.
3. **Build small, simple pieces that can change independently** -- large, tightly coupled systems become difficult to change and easy to break.

The book uses a fictional company called **FoodSpin** (an online restaurant menu service) throughout to illustrate concepts, patterns, and anti-patterns.

### Chapter 2: Principles of Cloud Infrastructure

This chapter establishes seven principles for designing cloud infrastructure managed as code:

1. **Assume systems are unreliable.** Cloud hardware fails routinely. Design for uninterrupted service when underlying resources change.
2. **Make everything reproducible.** Every part of the system should be effortlessly rebuildable from code, including rollback to previous states. This enables test environment consistency, geographic replication, and on-demand scaling.
3. **Avoid snowflake systems.** A snowflake is any instance that is difficult to rebuild or that has drifted from what it should be. Snowflakes create risk and waste team time. Replace them with reproducible, code-defined systems.
4. **Create disposable things.** Infrastructure elements should be gracefully added, removed, started, stopped, and moved. "Treat your servers like cattle, not pets."
5. **Minimize variation.** Fewer types of pieces make a system more manageable. Distinguish between necessary variation (different database products for genuinely different requirements) and unnecessary variation (using different databases for services with identical requirements). **Configuration drift** -- unintended differences between environments over time -- is a specific and common type of harmful variation.
6. **Ensure that any procedure can be repeated.** Automate tasks with scripts and tools rather than relying on manual steps. A strong scripting culture is essential.
7. **Apply software design principles to infrastructure code.** Many software engineering concepts translate to infrastructure, though with important differences covered in later chapters.

The chapter introduces the **automation fear spiral**: teams are afraid to run automation because their servers are inconsistent, and their servers are inconsistent because they don't run automation frequently. The way to break the spiral is to face fears -- start applying code continually to one set of servers, build confidence through testing, and expand from there.

The concept of **antifragility** (from Nassim Nicholas Taleb) is relevant -- systems that actually grow stronger when stressed. In infrastructure, this means designing systems that not only survive failures but become more resilient as a result of experiencing them. This connects directly to practices like chaos engineering, which injects failures in controlled circumstances to test and improve reliability.

### Chapter 3: Infrastructure Platforms

The book defines three system layers: **Applications** (top), **Engineering Platform** (middle), and **Infrastructure Platform** (bottom). The infrastructure platform provides compute, storage, and networking resources. The engineering platform provides technology capabilities including application runtime services (hosting) and operational services (monitoring, security, disaster recovery).

Infrastructure resources come in two forms: **primitive resources** (subnets, virtual disk volumes) and **composite resources** (database as a service, container clusters) assembled from primitives. The major IaaS hyperscalers are AWS, Azure, and Google Cloud, with Alibaba Cloud as an edge case.

The chapter discusses multicloud models: **hybrid cloud** (mixing private and public), **polycloud** (different workloads on different clouds), and **cloud agnostic** (workloads that shift dynamically among clouds). The author argues that the cost of true cloud-agnostic infrastructure is an order of magnitude higher than using a single cloud, and that building abstraction layers to hide cloud implementations creates more problems than it solves. A better approach than cloud-agnostic abstractions is to build a well-designed engineering platform that defines how the organization uses and interacts with cloud platforms, without attempting to hide cloud-specific details behind a lowest-common-denominator abstraction layer.

Platform service functionality can be provided three ways: **packaged software** deployed onto infrastructure, **cloud platform-provided services** configured via IaaS APIs, and **externally hosted SaaS solutions**. Infrastructure code can manage integrations across all three models.

**Platform delivery services** are meta-capabilities for building, deploying, and managing system elements. These include application delivery services (CI/CD pipelines), platform management services (developer portals, PaaS solutions), and infrastructure delivery services (Terraform, CDK, Pulumi, and related tooling).

### Chapter 4: Infrastructure as Code Tools and Languages

This chapter covers the mechanics of how infrastructure code works and the landscape of tools and languages.

**Infrastructure code processing** involves three substeps during deployment:
1. **Assemble** -- collate code files and dependencies into a build.
2. **Compile** -- generate the desired state model (a data structure reflecting what infrastructure should look like).
3. **Execute** -- compare desired state with current infrastructure via the IaaS API and apply changes.

Unlike application code (which executes after deployment), infrastructure code executes during deployment. This has significant implications for testing, debugging, and refactoring. Unit tests for infrastructure code can validate the desired-state model but are less useful for asserting how resources will actually behave. Refactoring infrastructure code can unexpectedly destroy resources with critical data.

**State management** is a key concern. IaaS-native tools (CloudFormation, CDK) handle state internally, while third-party tools (Terraform, OpenTofu, Pulumi) maintain external state files mapping code definitions to provisioned resources.

The tool landscape includes:
- **Server configuration tools** (CFEngine, Puppet, Chef, Ansible, Salt) focused on configuring OS and applications
- **Stack-oriented tools with declarative DSLs** (Terraform, OpenTofu, CloudFormation, Bicep)
- **Stack-oriented tools with general-purpose languages** (CDK, Pulumi) supporting TypeScript, Python, Java, etc.
- **Infrastructure as Data (IaD) tools** (Crossplane, ACK) using Kubernetes controller patterns for continual synchronization
- **Infrastructure from Code (IfC) tools** (Ampt, Winglang, Nitric) embedding infrastructure definitions into application code

Language considerations include four dimensions:
- **Procedural vs. idempotent**: Modern tools work idempotently, ensuring the same result regardless of how many times code is applied.
- **Imperative vs. declarative**: Declarative code specifies what you want; imperative code specifies how to make it happen. Most modern tools use a declarative model even when written in imperative languages.
- **Domain-specific vs. general-purpose**: DSLs closely map infrastructure concepts; GPLs offer richer ecosystems and tooling.
- **Low-level vs. high-level**: Most infrastructure languages are thin wrappers over IaaS APIs; teams can build their own abstraction layers.

The author recommends not trying to use a single language across a large, complex infrastructure estate -- different languages suit different parts of the system.

---

## Part II: Design

### Chapter 5: Design Principles for Infrastructure as Code

The book advocates for evolutionary design -- building systems that can continually adapt rather than attempting to create a perfect initial design. Traditional approaches assume infrastructure won't change much after initial build, but in reality, nontrivial systems change continually until decommissioned.

Key design concepts include:
- **Cohesion** -- grouping elements that are used together and changed together. A component has high cohesion when all its elements relate to a single purpose. Low-cohesion components contain unrelated elements, meaning changes to one part risk affecting unrelated parts.
- **Coupling** -- the degree to which changes to one element affect others. Two components are tightly coupled when a change to one frequently requires a change to the other; they are loosely coupled when one depends on the other but changes can usually be made independently.
- **Loose coupling** -- enabling independent change through clearly defined interfaces and dependency injection
- **Design forces** -- balancing factors like team ownership, speed of change, risk, and reuse

The author introduces the **CUPID properties** (from Daniel Terhorst-North) for evaluating design quality: **Composable** (plays well with others, small surface area, minimal dependencies), **Unix philosophy** (does one thing well), **Predictable** (deterministic and observable), **Idiomatic** (feels natural to users familiar with the platform), and **Domain-based** (the solution domain models the problem domain in language and structure).

A crucial concept is the **provider-consumer relationship**: a provider component creates resources that consumer components depend on. Dependencies should be managed through explicit **interface contracts**, not implicit resource references. The provider commits to maintaining the interface, while consumers depend only on the interface, not implementation details. This is the **principle of least knowledge** (Law of Demeter). Circular dependencies -- where a provider depends on one of its own consumers -- must always be avoided.

The chapter introduces the **DRY principle** (Don't Repeat Yourself) but warns against over-applying it. Premature abstraction -- creating shared modules before understanding the true patterns -- is a common trap. The author cites Sandi Metz's "The Wrong Abstraction" and Kent C. Dodds's "AHA Programming" (Avoid Hasty Abstractions).

Design decisions play out differently across the infrastructure code lifecycle stages: **source code** (concerns: understanding, sharing, collaboration), **package** (concerns: fast and reliable feedback on production readiness), **deployment** (concerns: speed and reliability), and **live resources** (concerns: operability and troubleshooting). What looks like good organization at one stage may not be ideal at another.

**Conway's Law** -- the observation that system architecture tends to mirror organizational communication structures -- is highly relevant. Team boundaries should align with component boundaries, and infrastructure design should consider who owns, uses, and changes what.

Design forces specific to infrastructure packaging and deployment include: scope of change, blast radius, speed of provisioning and testing, dependency management, and configuration variation across instances.

### Chapter 6: Infrastructure Components

The book defines four types of infrastructure components at different scope levels:

1. **IaaS resources** (primitive) -- the smallest independently provisionable unit (a VM, subnet, or disk volume).
2. **Code libraries** (low-level) -- groups of infrastructure code shared and reused across stack projects (Terraform modules, CDK Level 3 constructs, Pulumi component resources).
3. **Infrastructure deployment stacks** (mid-level) -- complete collections of resources deployed as a unit. A stack is an "architectural quantum" -- independently deployable with high functional cohesion.
4. **Infrastructure compositions** (high-level) -- collections of stacks organized around a workload-relevant concern, defining integrations and dependencies.

The chapter emphasizes **application-driven infrastructure design** -- starting from workloads and working backward. This contrasts with the traditional horizontal design (networking together, databases together, compute together) in favor of vertical design (infrastructure grouped around each workload/service). The recommended approach is a mix: dedicated infrastructure stacks per workload, plus shared stacks for genuinely shared resources like networking and compute clusters.

A **design workflow** follows the infrastructure code deployment process backward: start with the workload, design compositions, design stacks, organize code projects, create libraries, and write the actual IaaS resource code.

The chapter introduces the concept of **shared-nothing infrastructure architectures**, where each workload has dedicated infrastructure instances, avoiding resource contention. This was expensive in the Iron Age but is simple, fast, and cheap with IaaS and Infrastructure as Code.

Key principles for layered design:
- Implement infrastructure at the most specific relevant level
- Lower levels of infrastructure should not know about higher levels

The four component types map to tool-specific terminology: Terraform calls code libraries "modules"; CDK calls them "Level 3 constructs"; Pulumi calls them "component resources." CloudFormation uses "stacks," Pulumi and CDK also use "stacks," while Terraform's newer "stack" feature actually refers to compositions. Despite this confusing terminology, the concepts are universal.

### Chapter 7: Designing Deployable Infrastructure Stacks

This chapter defines patterns and anti-patterns for sizing and structuring infrastructure stacks:

**Full System Stack** -- All infrastructure for a system in a single deployment stack. Appropriate for simple estates where everything is fast to deploy and resources are often changed together.

**Monolithic Stack** (anti-pattern) -- A stack that has grown too large with low cohesion, including resources for different workloads. Leads to slow deployments, difficult testing, high coupling, and poor performance on the four key metrics.

**Application Group Stack** -- Infrastructure for a group of related applications and services. Balances manageability with cohesion.

**Single Service Stack** -- Infrastructure for a single application or service in one stack. Provides fast, independent changes but pushes integration complexity to the boundaries.

**Micro Stack** -- Breaking even a single service's infrastructure across multiple stacks (e.g., separating networking from compute). Maximizes independence but increases integration overhead.

**Shared Stack** -- A stack providing infrastructure used by multiple workloads (e.g., shared networking). Necessary when workloads genuinely share resources.

For multi-instance patterns (deploying the same stack to multiple environments):

**Reusable Stack** (pattern) -- A single stack project deployed to create multiple instances. The book uses this pattern extensively. This is the core mechanism for keeping environments consistent: one code definition, many instances.

**Snowflakes as Code** (anti-pattern) -- Copying or forking a stack project to create a customized version for a specific instance. Over time, the copies diverge, creating unmaintainable sprawl that defeats the purpose of Infrastructure as Code. This is the most common reason teams fall into this trap: it seems easier to copy code than to properly parameterize configuration.

**Multi-Environment Stack** (anti-pattern) -- A single stack project that defines different infrastructure for different environments (e.g., separate resource blocks for dev, test, and production). This creates configuration drift, makes testing unreliable, and makes it hard to keep environments consistent.

**Snowflakes as Code** (anti-pattern) -- Infrastructure managed with code but where instances diverge because changes are not applied comprehensively and promptly across all instances.

### Chapter 8: Configuring Infrastructure Stack Instances

When using the Reusable Stack pattern, configuration is how instances differ (environment names, resource sizes, secrets, etc.). A key insight is that configuration parameters should be kept simple -- prefer strings, numbers, and lists over complex nested structures; minimize the the number of parameters (YAGNI); and avoid using parameters as conditionals that create significantly different infrastructure between instances (a Boolean parameter that conditionally provisions an entire resource is a code smell suggesting the stack should be split).

The chapter defines a progression of patterns for injecting configuration, from simplest to most robust:

**Configuration in Code** (anti-pattern) -- Hardcoding per-instance values directly in the stack project code. Creates coupling between the stack code and specific instances.

**Separate Configuration Code** -- Using a separate codebase or branch for each instance's configuration. Still problematic because it makes it hard to see what differs across instances and encourages drift.

**Separate Configuration Files** -- Storing instance-specific values in separate files (e.g., a terraform.tfvars file per environment). Better, but files can drift and become inconsistent.

**Configuration Registry** (recommended pattern) -- A centralized store that manages and serves configuration values for all stack instances. Can be implemented using various backends (parameter stores, key-value stores, databases). Ensures consistency and makes the full configuration of every instance visible.

**Dependency Injection** -- The most decoupled approach, where an external agent (pipeline, orchestration script, or composition) assembles configuration and passes it to the stack at deployment time. The stack code has no knowledge of how or where its configuration is stored.

The chapter also covers **secrets management**, emphasizing that unencrypted secrets should never be stored in source control. Approaches include platform-native secret stores (AWS Secrets Manager, Azure Key Vault), external secrets management tools (HashiCorp Vault), and pipeline-injected secrets. A particularly useful pattern is for the pipeline to inject secrets as parameters when the stack is applied, keeping secret values out of source code and state files while making them available to the stack code at deployment time.

A useful rule of thumb is that configuration parameters should be kept simple: prefer strings, numbers, and simple lists over complex nested structures. Avoid using parameters as conditionals that create significantly different infrastructure between instances. When following this advice becomes difficult, it is usually a sign that the stack code should be refactored, perhaps by splitting into multiple stack projects.

### Chapter 9: Integrating Infrastructure Stacks

When infrastructure is split across multiple stacks, stacks need to discover and reference resources created by other stacks. The chapter defines three patterns:

**Resource Matching** -- The consumer stack searches the IaaS platform for resources matching a naming or tagging scheme. Tool-agnostic and straightforward, but creates an implicit contract that the provider team must maintain.

**Stack State Lookup** -- The consumer reads output values from the provider's state data (e.g., Terraform remote state, Pulumi StackReference). Explicit and well-managed, but locks you into a single stack deployment tool and can complicate tool upgrades.

**Integration Registry Lookup** -- The provider publishes resource identifiers to a registry (e.g., a DNS record, service discovery catalog, or configuration registry), and the consumer looks them up. Most decoupled approach, but requires additional infrastructure.

Implementation approaches include implementing discovery in the consumer stack code, in an orchestration script, or in a composition definition. Dependency injection (passing discovered values as configuration parameters) is the most loosely coupled approach.

### Chapter 10: Designing Infrastructure Code Libraries

Code libraries (modules, constructs) enable sharing and reuse across stack projects. Patterns include:

**Facade Module** -- A module that exposes a simplified interface over a complex set of resources. For example, a "java_application_server" module that encapsulates VM provisioning, JDK installation, application server configuration, and monitoring setup. This is the most useful type of module.

**Unshared Module** (anti-pattern) -- A module used by only one stack project. Adds complexity without providing reuse value.

**Bundle Module** -- A module that combines multiple independent capabilities. Can be useful for common combinations but risks becoming a "kitchen sink" that tries to do too much.

**Spaghetti Module** (anti-pattern) -- A module with too many configuration parameters and conditional logic, trying to handle every possible variation. Complexity makes it harder to use and maintain than the raw resources it wraps.

**Infrastructure Domain Entity** -- A module representing a cohesive infrastructure concept (like a "database" that includes the DB instance, backup configuration, networking rules, and monitoring). Provides a meaningful abstraction rather than just wrapping IaaS primitives.

**Stack Module** -- Using a library as a complete, deployable stack. Common with tools like Terraform where modules have strong versioning and distribution support but native stack concepts are less mature. Deployed via a thin wrapper project.

**Modular Monolith** (anti-pattern) -- A single large codebase organized into modules but deployed as a single unit. Modules appear to be separate but share state and deployment lifecycle.

### Chapter 11: Building Servers as Code

While cloud native (containers, serverless) has reduced focus on servers, most organizations still have server-based workloads. The server lifecycle has four stages: build an image (optional), create a new instance, change an existing instance, and destroy an instance.

Server contents are divided into: **software** (static packages, managed identically across instances), **configuration** (files that vary by role, environment, or instance), and **data** (generated by the system, treated as opaque by infrastructure code).

**Server roles** specify which configuration modules to apply to a server. Roles can be fine-grained (composed together) or coarse-grained (all-inclusive), or use inheritance (a base role plus specialized extensions).

Creating a server involves selecting/provisioning hardware or VMs, installing a base image, and configuring the instance. Approaches include network provisioning (PXE boot for bare metal), IaaS API creation, stack-integrated provisioning, and event-driven creation (auto-scaling, auto-recovery).

**Baking vs. frying**: Baking (preconfiguring server images) optimizes for speed of instance creation and consistency. Frying (configuring at creation time) optimizes for variability and speed of delivering changes. Most practical approaches combine both.

**Updating servers** uses three strategies:
- **Push on change** (applying code only when you know a change is needed) -- leads to configuration drift and snowflakes
- **Continuous configuration synchronization** -- repeatedly applying code whether or not it changed, catching and correcting drift
- **Immutable servers** -- never changing running instances; instead replacing them entirely with new instances built from updated images

Server images can be built using **pipeline-driven image building** where a pipeline automatically builds, tests, and publishes images whenever their definition changes.

### Chapter 12: Designing Environments

An environment is a logical grouping of deployed infrastructure. Multi-environment architectures serve three purposes: **delivery environments** (dev/test/prod for change management), **alignment** (splitting for manageability, ownership, or governance), and **replicas** (multiple production instances for different regions, customers, or availability).

Key concerns for delivery environments: **segregation** (environments should not affect each other), **consistency** (differences undermine testing validity), and **variation** (some differences are necessary, like capacity or access controls). These concerns are always in tension.

Environment implementation layers, from most to least isolated:
- **Physical environments** -- dedicated hardware
- **Virtual environments** -- dedicated IaaS resources per environment
- **Configuration environments** -- shared runtime with logical separation (e.g., Kubernetes namespaces)

The choice of layer depends on governance requirements, workload optimization needs, team ownership, and continuity considerations.

**IaaS resource groups** (AWS accounts, Azure resource groups, Google Cloud projects) should align with environment boundaries. A best practice is one or more resource groups per environment, with fine-grained separation (e.g., separate accounts for application hosting, management services, and monitoring).

### Chapter 13: Providing Application Runtime Infrastructure

This chapter discusses infrastructure for hosting workloads, using **application-driven infrastructure design** -- starting from workload requirements to identify needed capabilities, then determining how each capability is provided.

**Application runtime platforms** include:
- **Servers** (physical and virtual) -- the traditional platform
- **Server clusters** -- identically configured servers running the same workload, with IaaS-managed scaling and recovery
- **Application/container clusters** -- dynamically orchestrated workloads across a shared pool, dominated by Kubernetes
- **Serverless** (Function as a Service) -- on-demand code execution with platform-managed infrastructure

Container cluster functionality can be provided as **cluster as a service** (IaaS-provisioned, like EKS, AKS, GKE), **packaged distributions** (self-managed Kubernetes with tools like kOps, OpenShift, Rancher), or custom implementations.

**Cluster topologies** for environments include: multiple environments in one cluster (simplest, but challenging at scale), one cluster per environment (simplifies governance and upgrades), multiple clusters per environment (for team isolation or optimization), and cross-environment clusters (split by governance concern rather than environment).

---

## Part III: Delivery

### Chapter 14: Core Infrastructure Delivery Workflows

This chapter applies **continuous delivery (CD)** principles to infrastructure. CD delivers incremental changes frequently and quickly, testing each change thoroughly enough to release. Benefits include: earlier issue detection, faster user feedback, consistent processes for pre- and post-release changes, and built-in governance.

Key CD principles for infrastructure:
- **Automate the full process** -- no manual steps in the delivery pipeline
- **Make changes using only the automated process** -- no out-of-band fixes
- **Ensure environments are consistent** -- using the Reusable Stack pattern
- **Deliver changes comprehensively** -- apply to all environments quickly
- **Keep delivery cycles short** -- slow processes encourage workarounds
- **Keep all code production-ready** -- always be able to deploy
- **Ensure code and deployed resources are consistent** -- using drift detection and continual synchronization

The core workflow has five stages:
1. **Development** -- edit code, run local tests, push changes
2. **Build** -- prepare code for distribution (resolve dependencies, create versioned artifacts)
3. **Test** -- validate in progressively more integrated environments
4. **Release** -- deploy to production environments
5. **Run** -- use, monitor, and maintain

Team topologies for infrastructure delivery include:
- **Infrastructure instance management teams** (separate infra and software teams) -- creates handoffs and delays. This topology is a simple translation of separate software and infrastructure workflows into team structure. Value stream mapping reveals multiple handoffs between teams, each creating opportunities for delay, waiting, and failure-based rework.
- **Full stack teams** (owning both software and infrastructure) -- minimizes handoffs, ideal for simpler systems. All members don't need the same skills, but the team prioritizes work across both software and infrastructure as a whole. Each change involving both can be worked as a single item.
- **Infrastructure enablement teams** -- help software teams manage their own infrastructure, an interim stage. Enablement teams work closely with supported teams, often pairing on infrastructure work. They are usually transitional, evolving toward infrastructure service teams or component teams as the organization matures.

The chapter also introduces **value stream mapping** as a technique for analyzing workflows. By measuring the time spent on various activities, including waiting for other teams, you can focus improvement efforts on areas that make the most difference. A key insight: the time to provision a server might drop from 8 hours to 10 minutes with automation (a 98% improvement), but if the full request process takes 7 to 10 days due to queuing, the actual improvement is only about 12%.

### Chapter 15: Building and Distributing Infrastructure as Code

The build stage takes a code commit and produces a **release candidate** -- a versioned package that can be deployed to any environment. The distinction between **build-time dependencies** (resolved once during assembly) and **deployment dependencies** (resolved per environment during compilation) is crucial.

Two workflows exist:
- **Build on deploy** -- resolving dependencies every time code is deployed to each environment. Risk: dependencies can change between deployments, causing inconsistent behavior.
- **Build once, deploy many** -- resolving dependencies once during build, producing an immutable artifact deployed to all environments. Ensures consistency.

The chapter describes **integration workflows** for coordinating changes across multiple components:
- **Individual component integration** -- each team handles its own dependencies
- **Coordinated integration** -- synchronized releases across components
- **Stack integration composition** -- a composition orchestrates the deployment and integration of multiple stacks

**Infrastructure service teams** provide shared infrastructure components to multiple consumer teams. Effective service teams define clear interfaces (provider contracts), support consumer self-service, and use semantic versioning for their releases.

### Chapter 16: Implementing Infrastructure Delivery with Pipelines

Codebase organization patterns include:
- **Separate project per stack** -- each stack has its own repository or project directory
- **Monorepo** -- all infrastructure code in one repository
- **Project per layer** -- code organized by infrastructure layer (networking, compute, etc.)

The chapter recommends trunk-based development (merging to main at least daily) over feature branches, citing the Accelerate research showing better outcomes with continuous integration.

**Pipeline design** follows the progressive testing model: faster, narrower-scope tests first; slower, broader-scope tests later. Pipeline stages typically include: source (trigger on commit), build (assemble and run static analysis), automated test (deploy to test environment and validate), manual test (exploratory testing), and production (deploy to live environments).

**Delivery orchestration scripts** coordinate the deployment of multiple stacks. The author recommends treating these scripts as first-class software -- applying good design principles, keeping them simple, and avoiding tight coupling with specific pipeline tools.

### Chapter 17: Infrastructure Code Testing Strategy

Testing infrastructure code is essential but challenging. The chapter advocates for **continual testing** -- testing as you work rather than after you finish -- with tight feedback loops.

What to test spans far beyond functional correctness:
- **Code quality** -- readability, formatting, complexity
- **Functionality** -- does the infrastructure work as intended?
- **Security** -- vulnerability scanning, secrets detection, access control
- **Compliance** -- regulatory and policy requirements
- **Provenance** -- supply chain analysis, known vulnerabilities in dependencies
- **Performance** -- speed of operations
- **Scalability** -- does auto-scaling work correctly?
- **Availability** -- recovery from failures
- **Operability** -- monitoring, logging, maintenance procedures

**Challenges with testing infrastructure code**:
- Tests for declarative code often have low value (simply restating the declarations)
- Unit testing code generation (e.g., CDK synthesizing CloudFormation) only validates intermediate code, not actual infrastructure behavior
- Testing is slow because it requires provisioning real infrastructure
- Dependencies complicate testing -- test doubles (mocks, fakes, stubs) help isolate components

**Progressive testing** runs test suites in sequence, from fastest/narrowest to slowest/broadest. The classic **test pyramid** (many unit tests, fewer integration tests, fewest end-to-end tests) may look more like a **diamond** for infrastructure, since declarative code has fewer useful low-level tests but significant integration testing needs.

The **Swiss cheese model** applies multiple layers of validation, each with gaps, arranged so the gaps don't align. This provides defense in depth: code quality checks, static analysis, unit tests, integration tests, journey tests, and production monitoring.

**Testing in production** includes: smoke tests after deployment, synthetic transactions, chaos engineering (injecting failures to test resilience), and monitoring/alerting.

### Chapter 18: Infrastructure Code Testing Implementation

**Offline testing stages** run without provisioning real infrastructure:
- Syntax checking and linting
- Static analysis (security scanning, policy validation)
- Unit testing (especially useful for imperative code with complex logic)
- Code generation validation (for tools like CDK that compile to intermediate formats)

**Online testing stages** require real infrastructure:
- **Stack testing** -- deploying a stack and verifying its resources
- **Integration testing** -- testing multiple stacks together
- **Journey testing** -- end-to-end validation of system behavior

**Test fixtures** handle dependencies by providing substitutes for infrastructure components that a stack under test needs but that are not themselves being tested. Patterns include:
- **Dependency fixture** -- a minimal version of a dependency deployed specifically for testing
- **Shared fixture** -- a long-running instance of shared infrastructure used by multiple test runs
- **Proxy fixture** -- a mock or stub that simulates a dependency

**Test instance lifecycles** manage how test infrastructure is created and torn down:
- **Ephemeral instances** -- created fresh for each test run (cleaner, slower)
- **Persistent instances** -- kept running between test runs (faster, but may accumulate state)
- **Dual persistent and ephemeral stages** (anti-pattern) -- running the same tests against both, adding complexity without proportional value

**Test orchestration** should be decoupled from pipeline tools so tests can run consistently locally and in CI. The same scripts should work everywhere.

### Chapter 19: Deploying Infrastructure

Software deployment strategies provide context for infrastructure deployment:
- **Push deployment** -- a pipeline or tool pushes code to environments
- **Pull deployment** -- infrastructure code specifies software to install, deployed when infrastructure is provisioned
- **GitOps** -- a continuous reconciliation loop that watches a source of truth and automatically syncs deployed state to match

Infrastructure deployment strategies include:
- **Siloed infrastructure deployment** -- infrastructure and software deployed separately, often by different teams (common but often inefficient)
- **Application infrastructure descriptor** -- application deployments include a file specifying required infrastructure, automatically provisioned by the deployment service
- **Infrastructure from Code** -- infrastructure definitions embedded in application code, provisioned when the application is deployed or first runs

**Running deployments**:
- Local deployment (from a developer's machine) is useful for personal testing but causes conflicts in shared environments
- Central deployment services provide controlled, auditable processes with full history
- Pipeline-based deployment keeps everything visible in one place
- Specialized infrastructure deployment services (Spacelift, env0, HCP Terraform, TACOS products) provide infrastructure-specific capabilities
- **Infrastructure as Data** uses the Kubernetes Controller pattern for continuous reconciliation, combining drift detection with deployment

**Triggering deployments** can be event-driven (on code commit), scheduled, manual, or continuous (drift detection).

### Chapter 20: Changing Existing Infrastructure

The core challenge: applying changes to infrastructure risks disrupting services, but failing to change leads to vulnerabilities and technical debt. The solution is making changes less disruptive through four techniques:

1. **Deliver changes in smaller increments.** Break large changes into a series of small ones. Use **walking skeletons** (minimal end-to-end implementations) and **tracer bullet pipelines** to establish working infrastructure and delivery processes early. Handle incomplete changes through feature toggles, feature hiding, and dark launching.

2. **Change live infrastructure progressively.** Techniques for non-destructive changes:
   - **Manually remap infrastructure** -- editing state files to reassign resources between stacks (risky "infrastructure surgery," to be avoided except in extreme cases)
   - **Remap in pipelines** -- using code features like Terraform moved blocks or Pulumi aliases to rename/move resources idempotently
   - **Script changes** -- using tools like tfmigrate to script state file edits
   - **Expand and Contract** (recommended) -- a three-step pattern: (1) add the new resource, (2) switch usage to it, (3) remove the old resource. Each step is a separate change pushed through the pipeline and tested. Works with any tool.

3. **Minimize disruption when deploying changes.** Blue-green deployment, canary releases, rolling updates, and feature toggles all apply to infrastructure. The key is having automated rollback capability.

4. **Manage data when changing infrastructure.** Data persistence strategies include: continuous replication (data is always synchronized to a backup), database-managed migration (using database-native replication and failover), application-managed migration (applications handle their own data migration), and backup and restore (the simplest but slowest approach).

The chapter provides a detailed taxonomy of **refactoring** for infrastructure. Unlike software refactoring, infrastructure refactoring can involve destroying running resources and recreating them, potentially interrupting service or losing data. The distinction between refactoring infrastructure code (which can be done safely in an IDE) and refactoring infrastructure resources (which may require service disruption) is crucial. The author introduces the concept of "infrastructure surgery" -- manually editing state files to remap resources between stacks -- as a risky last resort that should be avoided except in extreme situations.

### Chapter 21: Governance

Governance, compliance, and security must be built into system foundations, not added afterward. Automation makes governance an inherent part of workflows rather than an opposing force that slows delivery.

**Shift left** means addressing compliance, security, and quality as early as possible. Developers and infrastructure engineers are empowered and responsible for validating that their changes are compliant, with immediate feedback from automated checks in the pipeline. Governance specialists act as enablers (training, documentation), tool providers (scanning services), and researchers (investigating new risks).

**Compliance as code** defines governance controls as code, automatically applied in delivery pipelines. Three types of controls:
- **Detection controls** -- report violations for human action
- **Prevention controls** -- block noncompliant actions (e.g., stop deployment if security issues are found)
- **Correction controls** -- automatically fix violations (e.g., remove unauthorized user accounts)

Controls are implemented across two dimensions:
- **Component design layers** -- from global infrastructure to workload-specific infrastructure. Lower layers impose broad restrictions; higher layers define specific exceptions.
- **Workflow stages** -- platform controls (IaaS policies), delivery controls (pipeline tests), deployment controls (runtime checks), and monitoring controls (continuous validation of running systems).

The governance pipeline should be fast enough for emergency fixes. If the normal process is too slow, people will bypass it, which introduces more risk. The author advocates designing the minimal process that meets governance requirements and using it for all changes, routine or emergency.

---

## Key Themes and Takeaways

1. **Optimize for change.** The central thesis of the book is that infrastructure must be designed for continuous evolution. Stability comes from the ability to make changes frequently and reliably, not from resisting change. The DORA/Accelerate research conclusively demonstrates that high-performing organizations excel at both speed and stability, with no trade-off between them.

2. **Build small, independent pieces.** Decompose infrastructure into small stacks with high cohesion and loose coupling. This enables faster testing, deployment, and recovery. Smaller stacks mean smaller blast radius, faster feedback loops, and more independent teams.

3. **Treat infrastructure code as real code.** Apply the full discipline of software engineering: code reviews, automated testing, CI/CD, design principles, and technical debt management. Infrastructure codebases that are not given this discipline inevitably evolve into unmanageable messes.

4. **Use progressive testing.** Layer validation from fast offline checks through integration tests to production monitoring. Each layer catches different issues. The Swiss cheese model applies multiple layers of validation, each with gaps, arranged so the gaps don't align. For declarative infrastructure code, the classic test pyramid may look more like a diamond -- fewer useful low-level tests, but significant integration testing needs.

5. **Make governance automatic.** Define compliance as code, shift checks left into development, and run them continuously. Governance should enable delivery, not impede it. The normal delivery pipeline should be fast enough for emergency fixes; if it isn't, people will bypass it, introducing more risk.

6. **Align infrastructure with workloads.** Design infrastructure starting from the applications that run on it, using vertical decomposition rather than horizontal layers. Horizontal layering (networking team, database team, compute team) creates ownership friction and coupling across workloads. Vertical decomposition aligns infrastructure with the services that use it, enabling independent change.

7. **Keep environments consistent.** Use the Reusable Stack pattern with proper configuration injection to ensure dev, test, and production environments are genuinely comparable. The build-once-deploy-many workflow ensures the exact same artifact tested in earlier environments is what gets deployed to later ones.

8. **Automate everything.** Every procedure should be scripted, every change should flow through a pipeline, and no manual intervention should be needed except writing code and occasionally approving changes. The automation fear spiral -- afraid to automate because systems are inconsistent, inconsistent because you don't automate -- must be broken by facing fears and building confidence through testing.

9. **Evolve incrementally.** Start simple, deliver working infrastructure early, and grow organically. Avoid speculative complexity and over-engineering. Use walking skeletons and tracer bullet pipelines to establish working patterns early, then flesh them out as needs become clear.

10. **The field is still evolving.** Tools like Infrastructure from Code (IfC), Infrastructure as Data (IaD), and application-driven infrastructure deployment represent emerging paradigms that may reshape how we think about infrastructure management. The book's patterns and principles are designed to be relevant regardless of which specific tools and paradigms dominate in the future.

## Important Anti-Patterns to Avoid

The book catalogs numerous anti-patterns that teams commonly fall into:

- **Monolithic Stack** -- a single stack that has grown too large, containing resources for unrelated workloads with low cohesion. Deployments are slow, testing is difficult, and changes to one area risk breaking others.
- **Snowflakes as Code** -- infrastructure nominally managed with code but where instances diverge because changes aren't applied comprehensively. Worse than unmanaged snowflakes because they create a false sense of control.
- **Multi-Environment Stack** -- using conditional code within a single stack to create different infrastructure per environment. Makes testing unreliable and keeps environments from being truly consistent.
- **Configuration in Code** -- hardcoding instance-specific values (environment names, resource sizes) directly in reusable stack code, creating tight coupling between the code and specific instances.
- **Obfuscation Module** -- a wrapper module that doesn't simplify or add value over the underlying resource definition. Adds complexity and cognitive overhead without benefit.
- **Spaghetti Module** -- a module with so many configuration parameters and conditional branches that it becomes harder to use than the raw resources it wraps. Often the result of trying to make a declarative module handle too many different use cases.
- **Modular Monolith** -- organizing code into logical modules but deploying as a single unit. Modules appear to be independent but share state and deployment lifecycle, negating the benefits of modular design.

## The Pattern Language Summary

The book defines a rich pattern language for infrastructure design and delivery, organized by concern:

**Stack sizing patterns:** Full System Stack, Application Group Stack, Single Service Stack, Micro Stack, Shared Stack.

**Multi-instance patterns:** Reusable Stack (the cornerstone pattern used throughout the book).

**Configuration patterns:** Manual Parameters, Environment Variables, Scripted Parameters, Configuration Files, Deployment Wrapper Stack, Pipeline Parameters, Parameter Registry (the most robust option).

**Integration patterns:** Resource Matching (search by naming/tagging), Stack State Lookup (read provider's state), Integration Registry Lookup (provider publishes to a registry).

**Code library patterns:** Facade Module, Bundle Module, Infrastructure Domain Entity.

**Deployment strategies:** Push Deployment, Pull Deployment, GitOps, Application Infrastructure Descriptor, Infrastructure from Code, Infrastructure as Data.

**Change strategies:** Expand and Contract (three-step add-switch-remove), state file remapping, moved blocks/aliases.

**Testing patterns:** Progressive Testing, Test Pyramid (or Diamond for infrastructure), Swiss Cheese Model, Test Fixtures (dependency, shared, proxy), Ephemeral vs. Persistent test instances.

Together, these patterns provide a comprehensive vocabulary for discussing, evaluating, and improving infrastructure design and delivery practices.
