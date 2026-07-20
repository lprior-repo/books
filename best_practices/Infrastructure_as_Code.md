# Infrastructure as Code, Third Edition — Best Practices Deep Dive

> Deep-dive extracted from the O'Reilly book *Infrastructure as Code, Third Edition* by Kief Morris (O'Reilly, 2025, ISBN 978-1-098-10467-0). Every pattern below is grounded in the book's hand-on "FoodSpin" running example and quoted source. All code/snippets are verbatim from the book. References cite the section heading as it appears in `Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md`.

**Author:** Kief Morris
**Topic tags:** `#architecture` `#devops` `#cloud`
**Language focus:** language-agnostic (HCL/Terraform, CloudFormation YAML, CDK/Pulumi TypeScript & Python, Ansible YAML, Bash)
**Sources:** `markdown_output/Infrastructure_as_Code_3rd_Ed_-_Kief_Morris/Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md` · `summaries/Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md`

---

## TL;DR

Morris's third edition is a complete playbook for treating infrastructure the way we treat application code: define everything as code, test and deliver it continually, and build it from small, simple pieces that can change independently. The book anchors every recommendation in the DORA "Four Key Metrics" (Lead Time, Deploy Frequency, Change Fail %, MTTR) and a pattern language that covers IaC tools, stack sizing & integration, configuration management, secrets, code libraries, server-as-code, environments, application runtime, CD pipelines, progressive testing, deployment strategies, safe change patterns (Expand and Contract, moved blocks, immutable servers, blue-green, canary), and shift-left governance/compliance-as-code. The case study is the fictional **FoodSpin** online restaurant menu service — used throughout to show how an infra team evolves from manually managed servers to reusable stacks, compositions, modular monolith-free designs, and full continuous delivery. Apply when you are provisioning cloud infrastructure, designing IaC codebases, building CD pipelines, splitting monoliths into stacks, choosing between Terraform/CloudFormation/CDK/Pulumi, setting up secrets/config, integrating multiple stacks, or implementing governance/compliance as code.

---

## Best Practices by Topic

### Cluster 1 — Infrastructure as Code Definition & Three Core Practices

**Principle:** IaC is the practice of provisioning and managing infrastructure using code rather than command-line tools or GUI-based "ClickOps" — applying the principles, practices, and tools of software engineering to infrastructure (TDD, CI, CD, sound design).

**Do:**
- Define everything as code — reusability, consistency, visibility.
- Continually test and deliver all work in progress — build quality in rather than testing it in afterward.
- Build small, simple pieces that can change independently — large, tightly coupled systems become difficult to change and easy to break.

**Don't:**
- Treat IaC as "scripts that provision things" — humans must put their knowledge and decision making into the code ahead of time, so they can stay hands-off and let machines do the work.
- Confuse IaC with the older "task-based scripting" approach (run a script to do one thing).
- Skip the software-design discipline — infrastructure codebases that aren't given the full SWE discipline inevitably evolve into unmanageable messes.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Core Practices for Infrastructure as Code"*

---

### Cluster 2 — DORA Four Key Metrics & Optimizing for Change

**Principle:** The central thesis of the book: **optimize for change**. DORA/Accelerate research proves there is no trade-off between speed and quality — high performers excel at both. The four key metrics predict organizational performance:

```text
Delivery Lead Time      Deployment Frequency
Change Fail Percentage  Mean Time to Restore (MTTR)
```

**Do:**
- Measure all four metrics for both software and infrastructure delivery — they directly drive business outcomes.
- Use the four metrics as a fitness function: "If stability and throughput numbers are good, your technical delivery is good."
- Apply the metrics to evaluate any process, org, or technology change ("did this move the dial?").

**Don't:**
- Reach for vanity metrics (lines of code, story points, coverage without assertion count) — not correlated with success.
- Treat "speed vs quality" as a binary trade-off — the data shows this is false.
- Add change-approval boards (CABs) hoping to improve stability — Accelerate research shows CABs *hurt* lead time, deploy frequency, and restore time and have **no** correlation with change fail rate.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "The Four Key Metrics", "Use Infrastructure as Code to Optimize for Change"*

---

### Cluster 3 — The Three Cloud-Age Eras (Iron → Shadow → Sprawl → Sustainable Growth)

**Principle:** Organizations evolve through distinct eras. The book frames them to help you see where you are and what comes next:

```text
Iron Age          → physical hardware, manual processes
Shadow Age        → cloud + DevOps used quietly by startups
Age of Sprawl     → rapid cloud adoption, uncontrolled tool/platform proliferation
Age of Sustainable Growth → rationalize systems, manage cost, keep innovating
```

**Do:**
- Acknowledge the era you're in — Sprawl-era organizations need rationalization, not more speed.
- Use the era framing to argue for investment in IaC discipline as the foundation for Sustainable Growth.

**Don't:**
- Stay in Shadow Age — quietly using cloud without the engineering discipline to match will eventually produce unmanaged sprawl.
- Treat Iron Age reflexes (manual handover, hand-edited config) as scalable.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "From the Iron Age to the Cloud Age", "The Path to the Cloud Age"*

---

### Cluster 4 — The Seven Principles of Cloud Infrastructure

**Principle:** Every IaC design should be evaluated against these seven principles:

```text
1. Assume systems are unreliable          (cloud hardware fails routinely)
2. Make everything reproducible           (rebuildable from code, including rollback)
3. Avoid snowflake systems                (no hard-to-rebuild, drifted instances)
4. Create disposable things               ("cattle not pets")
5. Minimize variation                     (necessary vs. unnecessary; no config drift)
6. Ensure any procedure can be repeated   (script everything; strong scripting culture)
7. Apply software design principles to infrastructure code
```

**Do:**
- Design for uninterrupted service when underlying resources change (Principle 1).
- Make rollback to a previous state effortless (Principle 2).
- Distinguish necessary variation (different DB products for genuinely different requirements) from unnecessary variation (different DBs for identical workloads) (Principle 5).

**Don't:**
- Confuse "disposable" with "unmanaged" — disposable implies replaceable *via code*, not untracked.
- Add variation as a shortcut — every difference is a future drift candidate.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Chapter 2. Principles of Cloud Infrastructure"*

---

### Cluster 5 — The Automation Fear Spiral & Antifragility

**Principle:** Teams are afraid to run automation because their servers are inconsistent, and their servers are inconsistent because they don't run automation frequently. The way to break the spiral is to face fears: start applying code continually to one set of servers, build confidence through testing, and expand from there.

**Do:**
- Recognize the spiral early — symptoms include "we'll fix it manually first then automate later."
- Connect the spiral to **antifragility** (Taleb): systems that grow *stronger* when stressed. In infrastructure this means designing systems that not only survive failures but become more resilient as a result (chaos engineering).

**Don't:**
- Wait for the system to be "clean" before automating — automation is what makes it clean.
- Treat chaos engineering as reckless — controlled failure injection is how you build antifragility.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Minimize Variation", "Myth: Speed and Quality Are Trade-Offs"*

---

### Cluster 6 — The Three-Layer Platform Model

**Principle:** Define three system layers clearly so ownership, design forces, and change cadence can be aligned to each:

```text
Applications              (top)    — your workloads, services
Engineering Platform      (middle) — application runtime, operational services
Infrastructure Platform   (bottom) — compute, storage, networking (the IaaS)
```

**Do:**
- Use the layering to drive team boundaries and ownership.
- Make the boundary between Engineering and Infrastructure Platform explicit (different SLAs, different cadence).

**Don't:**
- Conflate the engineering platform with the infrastructure platform — confusing them produces ownership gaps and handoff friction.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Infrastructure Platforms", "Engineering Platforms"*

---

### Cluster 7 — Primitive vs Composite Resources & Multicloud

**Principle:** Infrastructure resources come in two forms:
- **Primitive resources** — subnets, virtual disk volumes, VMs (the smallest addressable units)
- **Composite resources** — database-as-a-service, container clusters (assembled from primitives)

The hyperscalers are AWS, Azure, GCP (with Alibaba Cloud as an edge case). Multicloud has three models: **hybrid cloud** (private + public), **polycloud** (different workloads on different clouds), **cloud-agnostic** (workloads shift dynamically).

**Do:**
- Prefer well-designed engineering platforms over cloud-agnostic abstraction layers — abstracting away cloud-specific details creates more problems than it solves (lowest-common-denominator APIs).
- Be deliberate about which multicloud model you're pursuing; each has different cost/complexity profiles.

**Don't:**
- Build cloud-agnostic abstraction layers "just in case" — the cost of true cloud-agnostic infrastructure is an order of magnitude higher than using a single cloud.
- Treat primitive and composite resources as equivalent in design conversations — composability rules differ.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Infrastructure Resources", "Multicloud"*

---

### Cluster 8 — Platform Service Provisioning Models

**Principle:** Platform service functionality can be provided three ways — and infrastructure code must manage integrations across all three:

```text
1. Packaged software      — deployed onto infrastructure
2. Cloud platform-provided services — configured via IaaS APIs
3. Externally hosted SaaS solutions
```

**Do:**
- Recognize that **platform delivery services** (meta-capabilities for building/deploying) include application delivery (CI/CD), platform management (developer portals, PaaS), and infrastructure delivery (Terraform, CDK, Pulumi).

**Don't:**
- Treat SaaS integrations as "outside IaC scope" — they still need DNS, IAM, secrets, and networking managed as code.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Providing Platform Service Functionality", "Platform Delivery Services"*

---

### Cluster 9 — Infrastructure Code Processing Model (Assemble / Compile / Execute)

**Principle:** Unlike application code (which executes *after* deployment), infrastructure code executes *during* deployment. This has significant implications for testing, debugging, and refactoring. Three substeps during deployment:

```text
1. Assemble  — collate code files and dependencies into a build
2. Compile   — generate the desired-state model (what infrastructure should look like)
3. Execute   — compare desired state with current infra via IaaS API and apply changes
```

**Do:**
- Treat "refactoring infrastructure code" and "refactoring infrastructure resources" as different — code refactors are safe in an IDE; resource refactors can destroy live data.
- Use **preview** (terraform plan, pulumi preview) before applying — but recognize it is **not deep**: it usually doesn't check that referenced images/APIs exist.

**Don't:**
- Trust previews to be exhaustive — they usually miss dependency-level drift.
- Try to unit-test the *generated intermediate code* (e.g., CDK synthesizing CloudFormation) as if it proved the resulting infrastructure works.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Infrastructure Code Processing", "Processing and Deploying Infrastructure Code"*

---

### Cluster 10 — State Management & State Files

**Principle:** State management is a key IaC concern. IaaS-native tools (CloudFormation, CDK) handle state internally; third-party tools (Terraform, OpenTofu, Pulumi) maintain external state files mapping code definitions to provisioned resources.

**Do:**
- Choose your state backend deliberately — remote state, encrypted at rest, with locking.
- Treat the state file as production data — back it up, audit access, restrict who can write to it.

**Don't:**
- Store state files in source control or on developer laptops.
- Skip state locking — concurrent applies to the same state can corrupt it.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Managing Infrastructure State"*

---

### Cluster 11 — IaC Tool Taxonomy

**Principle:** The tool landscape divides into four families:

```text
Server configuration tools    — CFEngine, Puppet, Chef, Ansible, Salt (configure OS/apps)
Stack DSL tools               — Terraform, OpenTofu, CloudFormation, Bicep
Stack GPL tools               — CDK, Pulumi (TypeScript, Python, Java, etc.)
Infrastructure as Data (IaD)  — Crossplane, ACK (Kubernetes Controller pattern)
Infrastructure from Code      — Ampt, Winglang, Nitric (embedded in app code)
```

**Do:**
- Match the tool family to the problem: server config tools for OS/app config, stack tools for resource provisioning, IaD for continuous reconciliation, IfC for tightly coupled app+infra.
- Use multiple tools when justified — different parts of the system may suit different tools better than forcing one.

**Don't:**
- Force a single language across a large, complex infrastructure estate — different languages suit different parts.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Infrastructure as Code Tools"*

---

### Cluster 12 — Procedural vs Idempotent Code

**Principle:** Task-focused scripts run only once and aren't safe to run multiple times. **Idempotent code** produces the same result regardless of how many times it's applied. Modern IaC tools are idempotent even when written in imperative languages.

**Code (procedural → idempotent transformation):**
```
stack-tool create-virtual-server \
  --name=my-server \
  --os_image=ubuntu-22.10 \
  --memory=4GB \
  --disk=80GB
```

If run once → one server. Run three times → three servers (the antipattern).

```
stack-tool find-virtual-server --name=my-server
if [ "$?" = "1" ] ; then
  echo "Creating a new server"
  stack-tool create-virtual-server \
    --name=my-server \
    --os_image=ubuntu-22.10 \
    --memory=4GB \
    --disk=80GB
else
  echo "Server already exists, not creating a new one"
fi
```

Now idempotent — same result regardless of run count.

**Do:**
- Make every IaC script idempotent so it can be applied continually.
- Use the tool's existence check (or a state file) rather than reimplementing it in shell conditionals.

**Don't:**
- Add a new conditional branch every time you discover a new "edge case" — eventually the script becomes an unmaintainable mess.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Procedural and Idempotent Code"*

---

### Cluster 13 — Declarative vs Imperative Languages

**Principle:** *Imperative code* specifies **how** to make an action happen; *declarative code* specifies **what** you want without specifying how. Most popular IaC tools (Ansible, Bicep, CloudFormation, Puppet, OpenTofu, Terraform) use declarative languages; CDK, Pulumi, most IfC tools support imperative languages — though they use a declarative *model* internally.

**Code (declarative example):**
```yaml
virtual_server:
  name: my_server
  os_image: ubuntu-22.10
  memory: 8GB
```

**Code (declarative model built from imperative code):**
```text
appserverMemory = switch (serverSizeParameter) {
        "S": "1GB"
        "M": "4GB"
        "L": "8GB"
        "XL": "16GB"
}
VirtualServer appServer = VirtualServer.new (
        name: "my_server"
                          ,
        os_image: "ubuntu-22"
                              ,
        memory: appserverMemory
)
```

**Do:**
- Prefer declarative for static resource definitions — clarity and brevity win.
- Reach for imperative when you need conditional logic, loops, or composition (e.g., dynamic sizing).

**Don't:**
- Try to write complex configurable components in pure declarative — it gets messy fast; the tool's expressions/sets are usually enough, but eventually move complexity into a module/library.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Imperative and Declarative Languages and Tools"*

---

### Cluster 14 — Domain-Specific vs General-Purpose Languages

**Principle:** DSLs closely map infrastructure concepts (Ansible/Chef/Puppet have packages/files/services/users); general-purpose languages (TypeScript, Python, Java) offer richer ecosystems and tooling.

**Code (server config DSL pseudocode):**
```text
package: jdk

package: tomcat

service: tomcat

port: 8443

user: tomcat group: tomcat

file: /var/lib/tomcat/server.conf

owner: tomcat
```

**Do:**
- Use DSLs when the work is configuration-heavy and the team is operations-oriented.
- Use GPLs (via CDK/Pulumi) when software developers are writing infra and need testability/typing.

**Don't:**
- Choose a tool purely on ideology — pick by who will write the code and what ecosystem they live in.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Domain-Specific and General-Purpose Languages"*

---

### Cluster 15 — Low-Level vs High-Level Languages & Infrastructure from Code

**Principle:** Most IaC languages are thin wrappers over IaaS APIs; teams can build their own abstraction layers. **Infrastructure from Code (IfC)** embeds infrastructure definitions into application code (Ampt, Winglang, Nitric); the platform provisions them when the app deploys or first runs.

**Do:**
- Build higher-level abstractions as modules/libraries — keep the low-level details in one place.
- Track IfC as an emerging paradigm — it may reshape deployment but currently lacks standardization.

**Don't:**
- Build a custom DSL on top of Terraform "to improve it" — that creates an Obfuscation Module (anti-pattern) with more cognitive load than the raw resource.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Low-Level and High-Level Languages", "Infrastructure from Code"*

---

### Cluster 16 — Evolutionary Design & CUPID Properties

**Principle:** Build systems that can continually adapt rather than aiming for a perfect initial design. Apply **CUPID** (Daniel Terhorst-North) to evaluate IaC design quality:

```text
Composable     — plays well with others, small surface area, minimal dependencies
Unix philosophy — does one thing well
Predictable     — deterministic and observable
Idiomatic       — feels natural to users familiar with the platform
Domain-based    — solution domain models the problem domain in language/structure
```

**Do:**
- Treat design as evolutionary — every nontrivial system changes continually until decommissioned.
- Use CUPID to review modules before they grow into Spaghetti Modules.

**Don't:**
- Try to get it right up front — "if we think/work hard enough we can get things right at the beginning" is a waterfall fantasy.
- Confuse "no recipe" with "no discipline" — there is a real framework, you must apply it thoughtfully.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Design Principles for Infrastructure as Code", "CUPID Properties for Design"*

---

### Cluster 17 — Cohesion, Coupling & the Law of Demeter

**Principle:** **Cohesion** groups elements used and changed together. **Coupling** measures how changes to one element affect another. Loose coupling = clearly defined interfaces + dependency injection.

**Do:**
- Aim for high cohesion — every element relates to a single purpose.
- Use explicit **interface contracts** between provider and consumer components — provider commits to the interface, consumer depends only on the interface, not implementation.
- Apply the **principle of least knowledge** (Law of Demeter) — consumer components should not depend on implementation details of providers.

**Don't:**
- Hide dependencies behind "clever" resource-level references — this creates a distributed monolith (see Cluster 35).
- Allow circular dependencies between provider and consumer — always avoid them.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Cohesion and Coupling", "Providers, Consumers, and Interfaces"*

---

### Cluster 18 — Interface Contracts via Component-Level Dependency

**Principle:** Implement interfaces between components at the component level rather than integrating with specific IaaS resources.

**Code (provider exports identifiers into registry):**
```text
component:
        name: shared_network
...
resource: subnet_group
        name: main_subnet_group
        ...
stored_values:
        shared_network/exported_subnets: main_subnet_group
```

**Code (consumer discovers without implementation knowledge):**
```text
component:
        name: search_server_cluster
        ...
        resource: cluster_load_balancer
                subnet_group: stored_values/shared_network/exported_subnets
```

**Do:**
- Export interface identifiers via outputs/registries, not by name conventions.
- Standardize namespace conventions across teams so consumers can discover resources consistently.

**Don't:**
- Hardcode resource names across components — restructure one, break the other.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Management of Interfaces Between Components", "Use of Interfaces for Composability"*

---

### Cluster 19 — DRY, AHA, and the Wrong Abstraction

**Principle:** Don't Repeat Yourself is correct in principle but routinely *over*-applied. Sandi Metz's "The Wrong Abstraction" and Kent C. Dodds's "AHA Programming" (Avoid Hasty Abstractions) warn: premature abstraction creates shared modules before you understand the true patterns.

**Do:**
- Apply the **rule of three** — turn something into a reusable component when you find three places that need it.
- Refactor back to duplication when the abstraction proves wrong — repeated code is cheaper than the wrong abstraction.

**Don't:**
- Create shared modules "in case" they're useful later — that's YAGNI-violating speculative work.
- Trust the DRY principle as a moral absolute — sometimes two similar things will diverge and need to be different.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Providers, Consumers, and Interfaces", "Designing Infrastructure Code Libraries"*

---

### Cluster 20 — Conway's Law & Inverse Conway Maneuver

**Principle:** "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure."

**Do:**
- Align team boundaries with component boundaries — easier integration when the same team owns both ends.
- Use the **inverse Conway maneuver** when the design you want doesn't match current team structure — restructure teams to reflect desired architecture.

**Don't:**
- Design components that multiple teams need to change — the friction will dominate the work.
- Ignore ownership signals when designing modules.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Organizational structure"*

---

### Cluster 21 — Design Forces Across the Infrastructure Code Lifecycle

**Principle:** What looks like good organization at one lifecycle stage may not be ideal at another:

| Lifecycle stage | Activities | Design concerns | Manifestation |
|---|---|---|---|
| Source code | Edit, test, collaborate | Understanding, sharing, collaboration | Repos, folders, files |
| Package | Make available to deploy | Fast, reliable feedback on production-readiness | Packages, branches, tags, artifacts |
| Deployment | Execute to generate desired state + apply via IaaS | Speed and reliability | Desired-state model (in tool memory) |
| Live resources | Workloads use the infra | Operability, troubleshooting | Provisioned resources |

**Do:**
- Optimize each stage for its specific concerns — don't force a one-size-fits-all design.
- Trace the "lifecycle journey" of a component when designing.

**Don't:**
- Assume source organization = deployment organization = runtime organization.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Design Across Infrastructure Code Lifecycle Stages"*

---

### Cluster 22 — Cognitive Size, Change Scope, Cost of Ownership

**Principle:** Three cross-lifecycle design forces:

```text
Cognitive size   — a component becomes more unwieldy as it grows; non-linear
Change scope     — more components per change = more complex/risky change
Cost of ownership — variation increases time/effort; fewer types = easier to maintain
```

The time to coordinate and manage changes to an infrastructure component grows *nonlinearly* with the number of resources it includes.

**Do:**
- Keep components small enough to fit in your head — James Lewis: "the right size of a component at any given level of abstraction is no bigger than what you can fit into your head."
- Analyze historical commits to find which elements change together — this suggests refactoring for cohesion.

**Don't:**
- Optimize for "fewer repositories" without considering change scope — more repos can mean more independent change.
- Ignore cognitive load when adding parameters.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Design Forces Across Lifecycle Stages"*

---

### Cluster 23 — The Four Infrastructure Component Types

**Principle:** Four types of components at different scope levels — each tool uses different names:

```text
1. IaaS resources (primitive)
   - smallest independently provisionable unit (VM, subnet, disk)
2. Code libraries (low-level)
   - Terraform modules, CDK L3 constructs, Pulumi component resources
3. Infrastructure deployment stacks (mid-level) — "architectural quantum"
   - CloudFormation stack, CDK stack, Pulumi stack, Terraform project
4. Infrastructure compositions (high-level)
   - Pulumi/Terragrunt/Atmos stack, Crossplane composition
```

Terminology map (Table 6-1 condensed):

```text
Component           | Terraform         | CDK              | Pulumi           | CloudFormation
--------------------|-------------------|------------------|------------------|------------------
Composition         | stack / Atmos     | —                | project          | —
Deployment stack    | project / workspace | stack           | stack            | stack
Code library        | module            | L3 construct     | component resource | module
IaaS resource       | resource          | resource         | resource         | resource
```

**Do:**
- Use the four-type vocabulary in design conversations to avoid tool-specific confusion.
- Match the right type to the right scope — primitives for atomic units, libraries for reuse, stacks for deploy, compositions for integration.

**Don't:**
- Force every component into "module" because Terraform uses that word — the *concept* is what matters.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "The Infrastructure Components"*

---

### Cluster 24 — Application-Driven Infrastructure Design (Vertical over Horizontal)

**Principle:** Start from workloads and work backward. This is **vertical design** (infrastructure grouped around each workload/service), contrasted with traditional **horizontal design** (networking together, databases together, compute together).

**Do:**
- Mix dedicated infrastructure stacks per workload + shared stacks for genuinely shared resources (networking, compute clusters).
- Walk backward through the deployment process: workload → compositions → stacks → projects → libraries → IaaS resources.

**Don't:**
- Mirror the team structure (DBAs/networking/compute silos) in the IaC repository — it creates ownership friction and couples across workloads.
- Group resources by IaaS type rather than by workload.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Application-Driven Infrastructure Design", "Reference Application-Driven Infrastructure Design"*

---

### Cluster 25 — Shared-Nothing Infrastructure Architecture

**Principle:** Each workload gets dedicated infrastructure instances, avoiding resource contention. This was expensive in the Iron Age but is simple, fast, and cheap with IaaS + IaC.

**Do:**
- Default to per-workload infrastructure unless there's a genuine reason to share.
- Use shared stacks only for resources that are *truly* shared (e.g., a shared VPC).

**Don't:**
- Default to a single big shared environment "for efficiency" — contention, blast radius, and ownership conflicts follow.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Sharing Stack Instances Across Workloads"*

---

### Cluster 26 — Stack Sizing Patterns (Full System → Micro)

**Principle:** A spectrum of stack-scope patterns, each appropriate in different contexts:

```text
Full System Stack      — everything in one stack; simple estates only
Monolithic Stack       — too large, low cohesion; ANTI-PATTERN
Application Group Stack — group of related apps; balance manageability/cohesion
Single Service Stack   — one app per stack; fast, independent changes
Micro Stack            — break even a single service across stacks; max independence, integration overhead
Shared Stack           — used by multiple workloads (e.g., shared networking)
```

**Do:**
- Start with Single Service Stack as a default for production workloads.
- Use Shared Stack for genuinely shared resources (VPCs, cluster control planes).
- Use Micro Stack only when one part genuinely needs to change much more often than another.

**Don't:**
- Use Monolithic Stack — slow deployments, difficult testing, high coupling, poor DORA metrics.
- Use Full System Stack beyond a simple estate — it becomes a Monolith.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Patterns for Sizing and Structuring Stacks"*

---

### Cluster 27 — Reusable Stack vs Snowflakes as Code

**Principle:** The cornerstone pattern: **Reusable Stack** = one stack project deployed to create multiple instances (one code definition, many instances). The most common antipattern: **Snowflakes as Code** = copying or forking a stack project to create customized versions that diverge over time.

**Code (Reusable Stack example):**
```
> stack up env=development --source mystack/src
SUCCESS: stack 'development' created

> stack up env=test --source mystack/src

SUCCESS: stack 'test' created
```

**Do:**
- Use the Reusable Stack pattern as the default — keeps environments consistent.
- Push stack project code changes to *all* existing instances within a short period — avoids drift.

**Don't:**
- Fall into Snowflakes as Code "because it's easier to copy" — this is the most common path back to unmanaged sprawl.
- Edit instance-specific logic directly into the stack project (Configuration in Code anti-pattern).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Reusable Stack", "Snowflakes as Code"*

---

### Cluster 28 — Multi-Environment Stack Anti-Pattern

**Principle:** Using a *single stack project* with conditional code that defines different infrastructure per environment (e.g., `if environment == "prod"` blocks) is an anti-pattern. It creates configuration drift, makes testing unreliable, and undermines environment consistency.

**Do:**
- Use a single stack project with **configuration parameters** to differentiate instances.
- Keep parameters simple (strings, numbers, lists) and minimal (YAGNI).

**Don't:**
- Use a Boolean parameter to conditionally provision an entire resource — that signals the stack should be split.
- Hide environment-specific logic in conditional blocks within the stack.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Multi-Environment Stack"*

---

### Cluster 29 — Configuring Stacks: Patterns Progression

**Principle:** A progression of patterns for injecting configuration, from simplest to most robust:

```text
1. Configuration in Code         — antipattern (hardcoded per-instance values)
2. Manual Stack Parameters       — type values on CLI (mistakes easy)
3. Stack Environment Variables   — pick up from runtime env
4. Scripted Parameters           — hardcoded in script per env
5. Stack Configuration Files     — properties/yml per env, in VCS
6. Deployment Wrapper Stack      — separate stack project per instance, imports library
7. Pipeline Stack Parameters     — defined in pipeline stage config
8. Stack Parameter Registry      — centralized store, retrieved by stack (recommended)
```

**Code (Example stack parameters):**
```text
container_cluster:
  id: web_cluster-${environment}
  min_workers: ${min_workers}
  max_workers: ${max_workers}
```

**Do:**
- Prefer the **Stack Parameter Registry** pattern — centralizes truth, scales, supports CMDB use cases.
- Move toward **Dependency Injection** — discovery happens outside the stack code (see Cluster 35).

**Don't:**
- Use Configuration in Code (hardcoded per-environment values in the stack code).
- Use **Manual Stack Parameters** for anything people care about — typos break production (true story: a major bank's ATM network was down for two days because of copy-paste mistakes in a runbook).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Patterns for Configuring Stacks"*

---

### Cluster 30 — Stack Configuration Files Layout

**Principle:** For the Stack Configuration Files pattern, files are kept in VCS with the stack source:

```text
├── src/
│ ├── cluster.infra
│ ├── host_servers.infra
│ └── networking.infra
├── environments/
│ ├── dev.properties
│ ├── test.properties
│ └── prod.properties
└── test/
```

**Code (parameter file):**
```text
environment = test
min_workers = 1
max_workers = 3
```

**Do:**
- Keep config files in source control for audit/history.
- Combine with `--config` flags for non-secret overrides and `.secrets/` directory for secrets (outside VCS).
- Pass both via `--config` arguments:
```
stack up --source ./src \
  --config ./environments/test.properties \
  --config ../.secrets/test.properties
```

**Don't:**
- Include secrets in configuration files inside source control.
- Forget that adding a new instance requires adding a new config file (limits dynamic env provisioning).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Stack Configuration Files"*

---

### Cluster 31 — Scripted Parameters with Secret Integration

**Principle:** Hardcode parameter values into scripts that call the stack tool, but don't hardcode secrets. Fetch secrets via `secrets-tool get-secret`.

**Code (env-aware script):**
```sh
#!/bin/sh
case $1 in
dev)
  MIN_WORKERS=1
  MAX_WORKERS=1
  ;;
test)
  MIN_WORKERS=2
  MAX_WORKERS=3
  ;;
prod)
  MIN_WORKERS=2
  MAX_WORKERS=6
  ;;
*)
  echo "Unknown environment $1"
  exit 1
  ;;
esac
stack up \
    environment=$1 \
    min_workers=${MIN_WORKERS} \
    max_workers=${MAX_WORKERS}
```

**Do:**
- Commit the provisioning script to source control alongside the stack.
- Combine with secrets fetched at runtime:
```sh
SSL_CERT_PASSPHRASE=$(secrets-tool get-secret id="/ssl_cert_passphrase/${ENV}")
```

**Don't:**
- Hardcode secrets in the script — use a separate pattern for secrets.
- Allow the script to drift across environment files (one script per env = maintenance pain).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Scripted Parameters"*

---

### Cluster 32 — Stack Parameter Registry & Configuration Registry Implementations

**Principle:** The recommended pattern: a central registry serves parameter values. Implementable as integrated tool registries, standalone products, IaaS-provided services, or your own (S3 + versioning, etc.).

```text
Integrated     — Pulumi ESC, Chef Infra Server, PuppetDB, AAP, Salt Mine
Standalone     — Apache ZooKeeper, etcd, Consul
IaaS-provided  — AWS SSM Parameter Store, Azure App Config
Your own       — S3 buckets, VCS, files, internal APT/YUM
```

**Code (registry-based stack):**
```text
└── env/
   ├── dev/
   │ └── cluster/
   │ ├── min = 1
   │ └── max = 1
   ├── test/
   │ └── cluster/
   │ ├── min = 2
   │ └── max = 3
   └── prod/
       └── cluster/
           ├── min = 2
           └── max = 6
```

```text
cluster:
  id: container_cluster-${environment}
  minimum: ${get_value("/env/${environment}/cluster/min")}
  maximum: ${get_value("/env/${environment}/cluster/max")}
```

**Do:**
- Use one centralized registry for configuration management — it becomes your CMDB.
- Establish clear naming conventions (`/infrastructure/production/cluster_subnet` style).

**Don't:**
- Try to "rule them all" with one mega-registry — pragmatic boundaries (per-tool, per-team) beat forced unification.
- Store secrets in registries that don't protect them — makes the registry a juicy target.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Stack Parameter Registry", "Implementing a Configuration Registry"*

---

### Cluster 33 — Secrets Management

**Principle:** Unencrypted secrets should *never* be in source control. Three generation lifecycles:

```text
Pregenerated        — generated ahead of deployment (long-lived, vulnerable)
Deployment-generated — generated/stored as part of stack deploy (humans not involved)
Runtime-generated   — short-lived tokens (e.g., 15-min DB passwords)
```

Storage mechanisms: encrypted files (agebox, BlackBox, git-crypt, SOPS, transcrypt), secrets storage services (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, Conjur, Doppler, Pulumi ESC, Infisical), or runtime injection (env vars, metadata).

**Do:**
- Inject secrets at runtime — pipeline passes them as parameters so values never live in source/state files.
- Rotate secrets when people leave the team.
- Beware of logs: "One of the most common ways for secrets to leak out, even when using the most sophisticated services and tools, is in logs."

**Don't:**
- Treat "we use a secret manager" as sufficient — the manager must be actually wired into the pipeline.
- Reuse pregenerated passwords across environments/lifetimes.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Handling Secrets", "Storing Secrets in Encrypted Files", "Using a Secrets Storage Service", "Injecting Secrets at Runtime"*

---

### Cluster 34 — Resource Discovery Patterns

**Principle:** Three patterns for one stack to discover resources created by another:

```text
1. Resource Matching        — search IaaS API by name/tag (tool-agnostic, implicit contract)
2. Stack State Lookup       — read provider's state (Terraform remote state, Pulumi StackReference)
3. Integration Registry Lookup — provider publishes IDs to a registry; consumer looks up
```

**Code (Resource Matching by tag):**
```text
subnets:
  count: 3
  vpc: local.vpc_id
  name: cluster_subnet_${environment_name}_${count.index}
  tags:
      network_tier: compute_cluster
      environment: ${environment_name}
```

```text
lookup_resources:
  cluster_subnets:
    type: subnet
    match_tags:
      network_tier: compute_cluster
      environment: ${environment_name}
container_cluster:
  name: compute_cluster_${environment_name}
  networking_subnets: ${cluster_subnets}
```

**Code (Stack State Lookup — provider exports):**
```text
export:
  - cluster_subnet_list: cluster_subnet_*
```

**Code (Integration Registry Lookup):**
```text
registry:
  host: registry.foodspin.biz
  set_values:
    ${environment_name}/cluster_subnet_list: ${cluster_subnets}
```

```text
registry:
  host: registry.foodspin.biz
  get_values:
    cluster_subnets: ${environment_name}/cluster_subnet list
container_cluster:
  name: compute_cluster_${environment_name}
  networking_subnets: ${cluster_subnets}
```

**Do:**
- Choose Stack State Lookup when everyone uses the same tool and you need explicit publish/subscribe.
- Choose Integration Registry Lookup when teams may use different tools or you want loose coupling.
- Pick Resource Matching when teams agree on naming/tags and tooling diversity is a goal.

**Don't:**
- Use Resource Matching without an explicit contract — silent breakage when provider renames resources.
- Use Stack State Lookup across heterogeneous tools — adds complexity and lock-in.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Resource Discovery Patterns"*

---

### Cluster 35 — Dependency Injection & Compositions

**Principle:** Dependency injection (DI) decouples code from the implementation details of discovering dependencies. The stack code declares dependencies as parameters; deployment passes values.

**Code (DI consumer):**
```text
parameters:
  - cluster_name
  - cluster_subnets
container_cluster:
  name: ${cluster_name}
  networking_subnets: ${cluster_subnets}
```

**Code (DI via deployment script):**
```bash
#!/usr/bin/env bash
SUBNET_ID_LIST=$(
  stack value \
    --stack_instance cluster_network_stack_${ENVIRONMENT_NAME} \
    --export_name cluster_subnet_list
)
stack up \
    --stack_instance container_cluster_${ENVIRONMENT_NAME} \
    --parameter cluster_name=container_cluster_${ENVIRONMENT_NAME} \
    --parameter cluster_subnets=${SUBNET_ID_LIST}
```

**Code (Composition — declarative wiring):**
```yaml
composition: runtime_platform
parameters:
  - environment_name
stacks:
  - name: cluster_network_stack
    inputs:
      environment_name: ${environment_name}
    outputs:
      - subnet_list
  - name: cluster_compute_stack
    inputs:
      environment_name: ${composition.environment_name}
      cluster_subnet_list: ${stack.cluster_network_stack.subnet_list}
```

**Do:**
- Default to DI when wiring stacks — keeps the stack testable in isolation.
- Use compositions for declarative multi-stack wiring (a YAML replacement for an imperative deployment script).

**Don't:**
- Implement hardcoded discovery in the stack code — creates a distributed monolith where pieces can only be developed/tested/deployed together.
- Let "deployment scripts become complex spaghetti monsters" — split scripts by activity, keep them generic.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Implementing Resource Discovery", "Using Dependency Injection", "Wiring Stacks Together with a Composition"*

---

### Cluster 36 — Facade Module Pattern

**Principle:** The *Facade Module* pattern creates a simplified interface to a complex resource. The module exposes a few parameters and hardcodes the rest.

**Code (consumer using facade):**
```text
use module: foodspin-server
  name: checkout-appserver
  memory: 8GB
```

**Code (facade module implementation):**
```text
declare module: foodspin-server
  virtual_machine:
    name: ${name}
    source_image: hardened-linux-base
    memory: ${memory}
    provision:
      tool: servermaker
      maker_server: maker.foodspin.biz
      role: application_server
    network:
      vlan: application_zone_vlan
```

**Do:**
- Use Facade Modules for simple, common cases (one resource, narrow interface).
- Use them when the underlying API is complex with options that don't need to be exposed.

**Don't:**
- Create Facade Modules that expose everything — that's the Obfuscation Module anti-pattern.
- Limit the underlying resource's flexibility unnecessarily.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Facade Module"*

---

### Cluster 37 — Bundle Module & Infrastructure Domain Entity

**Principle:** A *Bundle Module* declares multiple related resources with a simplified interface (e.g., application server = server cluster + load balancer + DNS entry).

**Code (Bundle Module consumer):**
```text
use module: application_server
  service_name: checkout_service
  application_name: checkout_application
  application_version: 1.23
  min_cluster: 1
  max_cluster: 3
  ram_required: 4GB
```

**Code (Bundle Module implementation):**
```text
declare module: application_server
  server_cluster:
    id: "${service_name}-cluster"
    min_size: ${min_cluster}
    max_size: ${max_cluster}
    each_server_node:
      source_image: base_linux
      memory: ${ram_required}
      provision:
tool: servermaker
      role: appserver
      parameters:
        app_package: "${checkout_application}-${application_version}.war"
        app_repository: "repository.foodspin.biz"
load_balancer:
  protocol: https
  target:
    type: server_cluster
    target_id: "${service_name}-cluster"
dns_entry:
  id: "${service_name}-hostname"
  record_type: "A"
  hostname: "${service_name}.foodspin.biz"
  ip_address: {$load_balancer.ip_address}
```

*Infrastructure Domain Entity* is similar but uses imperative code to dynamically provision resources based on a parameter (e.g., traffic level → cluster sizing).

**Do:**
- Use Bundle Modules for static, cohesive collections of resources.
- Use Infrastructure Domain Entities when sizing/resources vary by input — but write them in an imperative language.

**Don't:**
- Make Bundle Modules provision more than callers need — they'll use a more granular module instead.
- Try to express dynamic sizing in a declarative Bundle Module — that's how Spaghetti Modules are born.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Bundle Module", "Infrastructure Domain Entity"*

---

### Cluster 38 — Spaghetti Module Anti-Pattern

**Principle:** The *Spaghetti Module* antipattern is configurable to the point where it creates significantly different results — implementation is messy because of too many parameters and conditional logic.

**Code (Spaghetti — illustrates the smell):**
```text
declare module: application-server-infrastructure
  variable: network_segment = {
    if ${parameter.network_access} = "public"
      id: public_subnet
    else if ${parameter.network_access} = "customer"
      id: customer_subnet
    else
      id: internal_subnet
    end
  }
  switch ${parameter.application_type}:
    "java":
      virtual_machine:
        origin_image: base_tomcat
        ...
    "NET":
      virtual_machine:
        origin_image: windows_server
        ...
    "php":
      container_group:
        ...
  switch ${parameter.database}:
    "mysql":
      database_instance: my_database
      ...
```

**Do:**
- When you realize you have a Spaghetti Module, **refactor** — split it into multiple smaller modules with focused remits.
- Treat struggling-to-test modules as a design signal: "if you're struggling to write automated tests and build pipelines to test the module in isolation, it's a sign that you have a spaghetti module."

**Don't:**
- Try to make a declarative module "do everything" — that's where Spaghetti Modules come from.
- Keep adding parameters to a Bundle Module that should have been split years ago.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Spaghetti Module"*

---

### Cluster 39 — Stack Module, Unshared Module, Modular Monolith

**Principle:** Three patterns/anti-patterns in the code library space:

```text
Stack Module       — library written as complete deployable stack (Terraform no-code provisioning)
Unshared Module    — used by only one stack; ANTI-PATTERN (YAGNI; rule of three)
Modular Monolith   — divided into modules but deployed as single unit; ANTI-PATTERN
```

**Do:**
- Use Stack Module + Deployment Wrapper Stack when you want reusable stacks but your tool (Terraform) lacks first-class stack packaging.
- Use the **rule of three** (Glass) — turn something into a reusable component when you find three places that need it.
- When stack code grows, split it into multiple stacks rather than wrapping it in modules.

**Don't:**
- Wrap a single-stack project in modules "to organize it" — that adds versioning/dependency overhead for zero reuse benefit.
- Confuse Modular Monolith with proper modularization — modules deployed as a unit don't get the benefits.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Stack Module", "Unshared Module", "Modular Monolith"*

---

### Cluster 40 — Servers as Code: Software/Configuration/Data

**Principle:** Servers are composed of three categories, with different IaC treatment:

| Type | Description | How IaC treats it |
|---|---|---|
| Software | Apps, libs, static files (RPM packages, time-zone data) | Ensure same on every relevant server |
| Configuration | Files controlling system/app behavior, vary by role/env/instance | Builds file content; ensures consistency |
| Data | Files generated and updated by the system and apps | Treated as opaque; backup/distribute/replicate |

The difference between configuration and data is whether automation tools manage what's inside the file. Even if a system log is essential for infra, the IaC tool treats it as externally managed data.

**Do:**
- Categorize each server element explicitly into software/config/data.
- Apply different lifecycle management to each category.

**Don't:**
- Mix config and data — the IaC tool will fight you when "data" turns out to need versioned management.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "What's on a Server"*

---

### Cluster 41 — Server Configuration Tools & Server Roles

**Principle:** First-gen IaC tools (Ansible, CFEngine, Chef, Puppet, Salt) focus on automated server configuration. **Server roles** specify which modules apply to a server.

**Code (role example):**
```text
role: application-server
  server_modules:
    - jboss
    - monitoring_agent
    - logging_agent
    - network_hardening
  parameters:
    - inbound_port: 8443
```

**Do:**
- Use role inheritance — a base role with common modules (network hardening, monitoring agent), specialized roles include the base + add specifics.
- Be deliberate about fine-grained vs coarse-grained roles; consistency matters more than which you pick.

**Don't:**
- Create overly specific roles like `ShoppingServiceApplicationServer` — fine-grained composition scales better.
- Skip the base role — duplicating hardening across specialized roles is exactly the kind of copy-paste sprawl IaC should eliminate.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Server Configuration Code", "Server Roles"*

---

### Cluster 42 — Creating Servers (PXE / IaaS API / Events)

**Principle:** Four ways to create a server instance:

```text
1. Network provisioning (PXE / Cobbler / Foreman / MAAS / Tinkerbell / FAI)
2. IaaS API by hand (UI/CLI) — useful for learning, not for production
3. As part of a stack
4. From an event (auto-scaling, auto-recovery)
```

**Code (stack defining a server):**
```text
virtual_machine:
  name: menu-service-appserver
  source_image: ubuntu-24.04
  memory: 4GB
  provision:
    method: cloud-init
    tool: servermaker
    parameters:
      role: appserver
      application: menu-service
```

**Code (auto-scaling example):**
```text
server_cluster:
  server_instance:
    source_image: stock-linux-1.23
    memory: 2GB
    vnet: ${APPSERVER_VNET}
  scaling_rules:
    min_instances: 2
    max_instances: 5
    scaling_metric: cpu_utilization
    scaling_value_target: 40%
  health_check:
    type: http
    port: 8443
    path: /health
    expected_code: 200
    wait: 90s
```

**Do:**
- Default to stack-driven provisioning for production servers.
- Use IaaS API by hand only for experiments and one-off debugging.
- Define auto-scaling rules as code so they're testable and reviewable.

**Don't:**
- Create production servers by clicking through the IaaS UI — exactly the "ClickOps" IaC is meant to replace.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Creating and Provisioning a New Server Instance", "Creating a Server as Part of a Stack", "Creating a Server from an Event"*

---

### Cluster 43 — Baking vs Frying Server Images

**Principle:**

```text
Baking — preconfigure images; optimizes for speed/consistency at instance creation
Frying — configure at creation; optimizes for variability and fast changes
```

The practical answer: combine both. Bake language runtimes, app servers, DBs into the image; fry per-instance config (env name, role, secrets).

**Code (image builder using small numbered shell scripts):**
```text
image:
  name: foodspin-linux-image
  origin: fci-12345678
  configure:
    commands:
      - 10-install-monitoring-agent.sh
      - 20-install-jdk.sh
      - 30-install-tomcat.sh
```

**Do:**
- Bake large items (JDK, Tomcat, container cluster system software) — saves minutes per instance.
- Fry environment-specific config (env name, secrets, role parameters).
- Write small, single-task scripts prefixed with numbers so order is obvious.

**Don't:**
- Fry everything — instance creation becomes slow.
- Bake everything — image build pipeline becomes slow, lead time for changes blows up.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Baking Images and Frying Instances", "Building Server Images"*

---

### Cluster 44 — Updating Servers: Push on Change / Continuous Sync / Immutable

**Principle:** Three strategies for changing existing servers:

```text
Push on Change                  — apply code only when a change is needed; leads to drift
Continuous Configuration Sync   — repeatedly apply code; catches drift; correct for malicious changes
Immutable Server                — never change running instances; replace with new instances from updated images
```

The **Immutable Server** strategy is preferred: "The entire server configuration is defined in the image used to create instances. A change is made by building a new version of the image and replacing all the server instances that use it."

**Do:**
- Default to Immutable Servers for production workloads.
- Use Continuous Sync when you can't replace (legacy systems, stateful workloads).
- Randomize sync timing across the estate to avoid swamping the code repo (Chef `--splay`).
- Rebuild servers weekly or at most every few weeks.

**Don't:**
- Rely on continuous sync to stop attackers — they may target parts of the system not managed by code, or subvert the agent.
- Use "push on change" for the long tail — it guarantees configuration drift.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Updating and Changing Servers", "Continuous Configuration Synchronization", "Immutable Server"*

---

### Cluster 45 — Multi-Environment Architectures

**Principle:** Environments serve three purposes:

```text
Delivery environments   — dev/test/prod for change management
Alignment               — split for manageability/ownership/governance
Replicas                — multiple prod instances for regions/customers/brands
```

Three design concerns, always in tension: **segregation** (environments shouldn't affect each other), **consistency** (differences undermine testing validity), **variation** (some differences are necessary like capacity or access controls).

**Do:**
- Choose the right implementation layer (physical / virtual / configuration) based on governance, workload optimization, ownership, continuity.
- Map environments to **IaaS resource groups** — one or more resource groups per environment, with fine-grained separation (apps vs management vs monitoring).

**Don't:**
- Take "best practice dev/test/prod environments" as gospel — your architecture may need more or fewer environments based on the three purposes.
- Skip the "you will get the design wrong" mindset — plan for evolving environments, not freezing them.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Multi-Environment Architectures", "Environment Implementation Layers"*

---

### Cluster 46 — Application Runtime Platforms

**Principle:** Four runtime platforms, each with IaC implications:

```text
Servers               — physical/virtual; traditional platform
Server clusters       — identically configured pool; IaaS-managed scaling/recovery
Application/container clusters — dynamic orchestration; dominated by Kubernetes
Serverless            — on-demand code execution; platform-managed infrastructure
```

Container cluster functionality:

```text
Cluster-as-a-Service    — EKS, AKS, GKE (IaaS-provisioned, Kubernetes)
Packaged distribution   — kOps, OpenShift, Rancher, D2iQ, Mirantis, Tanzu
Serverless              — AWS Lambda, Azure Functions, Cloud Run; Fission, KEDA, Knative, OpenFaaS, OpenWhisk
```

**Do:**
- Use Application-Driven Infrastructure Design — start from workload requirements, identify needed capabilities, then determine how each is provided.
- Treat serverless as another platform to be IaC-managed, not as "the end of IaC."

**Don't:**
- Think serverless means Infrastructure as Code is irrelevant — serverless code depends on infra (storage, networking) that still needs IaC.
- Confuse PaaS with IaaS — some "container" services are really PaaS (Platform9 PMK, Civo).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Application Runtime Platforms", "Cluster as a service (IaaS provisioned)", "Serverless Application Infrastructure"*

---

### Cluster 47 — Cluster Topologies

**Principle:** Four topologies, applied across environments:

```text
Multiple environments per cluster          — simplest; OK for smaller orgs
One cluster per environment                — simplifies governance/upgrades
Multiple clusters per environment          — for team isolation/optimization
Cross-environment clusters                 — split by governance/optimization concern, not env
```

Design forces: governance, optimization, ownership, continuity.

**Do:**
- Pick the simplest topology that meets your design forces.
- Default to one cluster per environment when you have multiple environments — simplifies upgrades.

**Don't:**
- Run a single cluster across environments and teams at scale — upgrade scheduling becomes exponentially harder.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Cluster Topologies"*

---

### Cluster 48 — Continuous Delivery Principles for IaC

**Principle:** The core CD principles for infrastructure code:

```text
1. Automate the full process
2. Make changes using only the automated process
3. Ensure environments are consistent (Reusable Stack)
4. Deliver changes comprehensively (all environments quickly)
5. Keep delivery cycles short
6. Keep all code production-ready
7. Ensure code and deployed resources are consistent (drift detection)
8. Minimize disruption when deploying changes
```

**Do:**
- Use **GitOps** (continuous reconciliation loops, Weaveworks/Argo) to keep code and deployed state consistent.
- Use Puppet/Chef agents (continual sync) OR GitOps-style controllers — both are valid IaC reconciliation strategies.
- Measure **lag between applying a change to the first production system and the last** — that's the real cross-environment consistency metric.

**Don't:**
- Accept "we'll fix it manually first then add it to code" — fix the discipline, not the symptom.
- Skip drift detection — "Server-oriented IaC tools are designed to be run as agents that continually synchronize infrastructure code to servers."

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Continuous Delivery Principles for Infrastructure as Code", "Ensure That Code and Deployed Resources Are Consistent"*

---

### Cluster 49 — Core Delivery Workflow Stages

**Principle:** Five stages, repeated many times for incremental changes:

```text
1. Development — edit code, run local tests, push changes
2. Build      — prepare for distribution (deps, versioned artifact)
3. Test       — validate in progressively more integrated environments
4. Release    — deploy to production environments
5. Run        — use, monitor, maintain
```

Each stage may have multiple steps (different test suites, integration/no-integration). Activities repeat across stages (developer runs tests locally; pipeline runs the same tests and records results).

**Do:**
- Make every change releasable — "each change is finished, because it is releasable."
- Make **incremental, frequent commits** so each pipeline run covers a small scope; debugging is easier.
- Push to pipeline at least daily.

**Don't:**
- Batch a week's work and push once — "a day or more" debugging a week's worth of failures plus blocked pipeline for everyone else.
- Treat "deployment" as production-only — deployment happens in every test stage too.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Core Infrastructure Delivery Workflow"*

---

### Cluster 50 — Team Topologies for IaC Delivery

**Principle:** Three topologies, in increasing order of system complexity:

```text
Infrastructure Instance Management Teams — separate infra & software teams; handoffs, delays
Full Stack Infrastructure Team          — owns both; minimizes handoffs, ideal for simple systems
Infrastructure Enablement Team          — transitional; helps software teams manage their infra
Infrastructure Service Team             — mature; provides infra as a service, consumer self-service
```

Value stream mapping lesson: a team automated server provisioning from 8 hours to 10 minutes (98% improvement) but the *full process* took 7-10 days, so the actual improvement was only ~12%. Optimize the right queue, not the most obvious one.

**Do:**
- Default to Full Stack for simple systems.
- Move to Service Team as system complexity grows.
- Use value stream mapping before optimizing — find the actual bottleneck (often a queue, not a step).

**Don't:**
- Default to Infrastructure Instance Management — "value stream mapping reveals multiple handoffs between teams, each creating opportunities for delay, waiting, and failure-based rework."
- Treat enablement teams as permanent — they're transitional.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Delivering Software and Infrastructure", "Infrastructure Instance Management Teams", "Full Stack Infrastructure Team", "Infrastructure Enablement Team"*

---

### Cluster 51 — Build Once, Deploy Many

**Principle:** Resolve build-time dependencies *once* during build, not every deploy. The Assemble step runs once per commit; the Compile step runs per environment.

```text
Build on Deploy     — resolve deps every deploy; risk: deps change between deploys
Build Once Deploy Many — resolve deps once, bundle into artifact; consistency
```

**Do:**
- Use **dependency lock files** (Terraform dependency lock-file) committed with the build.
- Bundle deps with the artifact OR commit them to a branch.
- Prefer build once for regulated environments (finance, gov, healthcare) — gives audit trail for free.

**Don't:**
- Re-resolve dependencies each deploy — "troubleshooting inconsistent behavior and failures caused by it can be fiendishly difficult."

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Build on Deploy Workflow", "Build Once, Deploy Many Workflow", "Bundling or Locking Dependencies"*

---

### Cluster 52 — Trunk-Based Development for IaC

**Principle:** Trunk-based development (TBD) > pull requests for IaC: PRs put manual code review inside the merge loop; TBD merges incrementally to main and relies on fast automated tests.

**Do:**
- Default to TBD with merge-to-main at least daily.
- Keep test suite fast (release candidate in <10 minutes ideally).
- Use pair programming or post-merge review to satisfy audit/regulatory needs.

**Don't:**
- Confuse "no PR review" with "no code review" — use pairing or post-merge audits.
- Apply PR workflows to a codebase where tests can't catch regressions quickly.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Pull Requests and Trunk-Based Development"*

---

### Cluster 53 — Integration Workflows (Fan-in / Federated / Monorepo)

**Principle:** Three workflow patterns for integrating multiple stacks/components:

```text
Fan-in       — build/test each separately, then integrate and deploy together; OK within one team
Federated    — deliver each component independently across environments; requires mature dep mgmt
Monorepo     — build all components together in one repository with directed-graph build
```

**Do:**
- Use **fan-in** for components owned by a single stream-aligned team.
- Use **federated** when delivery coordination across dozens of teams becomes unworkable.
- Consider hybrid: fan-in within teams, federated between teams.
- Use monorepo build tools (Bazel, Buck, Pants, Please) when integrating at build time.

**Don't:**
- Use federated delivery without API design discipline, contract testing, and progressive deployment practices.
- Confuse "monorepo" with "single deployable artifact" — multiple artifacts built together is the point.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Integration Workflows", "Fan-in: Integrating Components During Delivery", "Federation: Integrating Components at Runtime", "Monorepo: Integrating Components in the Build"*

---

### Cluster 54 — Infrastructure Service Teams

**Principle:** Service teams provide infrastructure that consumer teams can use *without* the service team being involved in routine work. Self-service has two flavors:

```text
Shared instance, multitenancy — one cluster, multiple consumers (onboard/configure/troubleshoot/deploy)
Dedicated instances, on-demand — each consumer gets their own (separate DB instances per app)
```

The difference between instance management and service team is the *journey*: onboarding, configuring infra, troubleshooting, deploying.

**Do:**
- Make self-service possible for high-frequency journeys (e.g., deploy new app version multiple times per week).
- Publish versioned infrastructure components or compositions — consumers select and configure, don't edit.

**Don't:**
- Keep instance management for journeys that happen multiple times a week — switch to self-service.
- Use a service team for journeys that happen twice a year — instance management is fine.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Infrastructure Service Teams", "Shared Infrastructure as a Service", "Provisioning an Infrastructure Instance on Demand", "Providing Deployable Infrastructure as a Component"*

---

### Cluster 55 — Pipeline Stage Design

**Principle:** Each stage has three elements: **content** (input + output materials), **actions** (trigger, run, promote), **context** (scope, dependencies, environment).

**Do:**
- Run automated stages first, manual stages last — "Human time is valuable and shouldn't be wasted on a build that a machine could indicate isn't ready."
- Avoid mixing automated and manual modes in one stage — separate them.
- Use **passive triggers** (consumer detects new build) over active (provider calls consumer) — easier self-service, less coupling.

**Don't:**
- Use a pipeline tool as your only test runner — implement test orchestration in a separate script that pipeline stages call.
- Couple test orchestration tightly to pipeline tools — should run the same locally and in CI.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Pipeline Stage Content", "Pipeline Stage Actions", "Pipeline Stage Context"*

---

### Cluster 56 — Delivery Orchestration Scripts

**Principle:** Treat orchestration scripts as first-class software. Tasks they handle:

```text
Build, deployment, delivery, testing, dependencies, tool/platform setup,
authentication, configuration, packaging, promotion, execution
```

**Do:**
- Split scripts to keep them small and focused on a single activity.
- Test scripts (e.g., Bats for shell).
- Apply SOLID, single responsibility, composition principles.

**Don't:**
- Let orchestration scripts become as complicated as the infrastructure code — "I've worked on projects with infrastructure deployment scripts that had more lines of code than the infrastructure codebase."
- Embed build/deploy logic in pipeline configuration rather than scripts.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Using Delivery Orchestration Scripts"*

---

### Cluster 57 — Continual Testing Strategy

**Principle:** *Immediate testing* happens as soon as you push code; *eventual testing* waits. Continual testing = test as you code, push frequently (multiple times a day), get fast feedback.

**Do:**
- Test across **code quality, functionality, security, compliance, provenance, performance, scalability, availability, operability** — not just functional correctness.
- Treat deployment and operational tests as part of the same suite.
- Pair programming is a form of immediate testing — much faster than post-hoc code review.

**Don't:**
- Treat "tested in production" as a substitute for prerelease testing — they're complementary.
- Focus only on functional tests — non-functional/cross-functional requirements need validation too (the term *CFR* was coined by Sarah Taraporewalla to emphasize this).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Why Continually Test Infrastructure Code?", "What Should We Test with Infrastructure?"*

---

### Cluster 58 — Progressive Testing & the Infrastructure Test Diamond

**Principle:** Run test suites in sequence — fast/narrow first, slow/broad later. The classic **test pyramid** may look more like a **diamond** for infrastructure:

```text
                  /\
                 /  \      <- journey tests (few)
                /    \
               /  /\  \    <- integration tests (many)
              /  /  \  \
             /  /    \  \  <- unit tests (fewer than pyramid)
            /__/______\__\
```

**Do:**
- For declarative code, expect the diamond shape — fewer low-level tests, more integration.
- For imperative-heavy codebases, the pyramid still applies — more variable outcomes worth testing.

**Don't:**
- Force a pyramid onto a declarative codebase — produces low-value bookkeeping tests.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Progressive Testing", "Test Pyramid"*

---

### Cluster 59 — Swiss Cheese Testing Model

**Principle:** Multiple layers of validation, each with gaps (holes), arranged so the gaps don't align. Defense in depth:

```text
Layer 1: Code quality checks
Layer 2: Static analysis
Layer 3: Unit tests
Layer 4: Integration tests
Layer 5: Journey tests
Layer 6: Production monitoring
```

**Do:**
- Design your test suite based on *managing risks*, not fitting a formula.
- Decide where each risk is best caught.

**Don't:**
- Duplicate tests across stages — if you tested directory permissions in the offline stage, don't re-test in the integration stage.
- Treat the Swiss cheese model as a permission to skip earlier layers.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Swiss Cheese Testing Model"*

---

### Cluster 60 — Testing in Production

**Principle:** Some characteristics can't be replicated outside production: **data** (real users create weird values), **users** (more creative than testers), **traffic** (scale + duration), **concurrency** (unusual combinations).

**Do:**
- Use **monitoring as passive testing in production** — observe natural activity for undesirable outcomes.
- Add **observability** to investigate problems when they occur.
- Use **chaos engineering** to inject known failures and prove mitigations work.
- Run zero-downtime deployments and progressive rollouts.
- Maintain test data records (users, credit cards) that won't trigger real-world actions.

**Don't:**
- Treat testing in production as a substitute for prerelease testing — they address different unknowns.
- Test in production without monitoring to detect the tests' own problems.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Testing in Production", "Managing the Risks of Testing in Production"*

---

### Cluster 61 — Offline Testing Stages (Syntax, Linting, Policy, Supply Chain)

**Principle:** An offline stage should:
- Run quickly (fast feedback)
- Validate components in isolation (simplify debugging)
- Have no dependencies outside the stack
- Prove the component is cleanly decoupled

Activities: syntax checking, offline static analysis (linting), connected static analysis, supply-chain checks, local infrastructure emulators.

**Code (syntax check failure):**
```
$ stack validate
Error: Invalid resource type
  on appserver_vm.infra line 1, in resource "virtual_mahcine":
stack does not support resource type "virtual_mahcine".
```

**Code (TFLint connected check failure):**
```
$ stacklint
1 issue(s) found:
Notice: base_image 'SERVER_IMAGE.shopspinner_java_server_image' doesn't
  exist (validate_server_images)
  on appserver_vm.infra line 5, in resource "virtual_machine":
```

**Do:**
- Use linters and policy-as-code tools (TFLint, CloudFormation Linter, cfn_nag, Trivy, Checkov, Conftest, OPA, Snyk).
- Generate SBOMs and check deps against vulnerability databases.
- Use local emulators (LocalStack, Moto, Azurite, Cosmos DB emulator, gcloud emulators, Firebase Local Emulator Suite, Winglang Simulator) for fast feedback.

**Don't:**
- Run emulators and assume they prove what real infrastructure does — "These emulators don't replicate the full functionality of the IaaS platform."
- Skip supply-chain checks — vulnerabilities appear after you've provisioned.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Offline Testing Stages for Stacks", "Syntax Checking", "Offline Static Code Analysis", "Connected Static Code Analysis", "Supply-Chain Checks", "Local Infrastructure Emulators"*

---

### Cluster 62 — Test Fixtures (Dependency, Shared, Proxy)

**Principle:** Three patterns for handling dependencies in tests:

```text
Dependency fixture  — minimal version of a dependency deployed for testing
Shared fixture      — long-running instance of shared infra used by multiple test runs
Proxy fixture       — mock/stub that simulates a dependency
```

**Code (test fixture using connection check):**
```text
given stack_instance(stack: "cluster_network",
                                              ,
                     instance: "online_test") {
  can_connect(from: get_fixture("client_fixture"),
              to: get_fixture("server_fixture").address
              port: 8443)
}
```

**Do:**
- Use lightweight test fixtures — a stack that needs only a subnet can use a tiny fixture instead of the full hardened VPC.
- Refactor components that are hard to isolate — "A component that is difficult to test in isolation is a symptom of design issues."

**Don't:**
- Test the full integration at every stage — keep stack tests focused on the component, integration tests focused on interaction.
- Treat hard-to-test components as "just hard" — fix the design.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Use Test Fixtures to Handle Dependencies", "Use Test Fixtures to Replace Providers", "Use Test Fixtures to Replace Consumers"*

---

### Cluster 63 — Test Instance Lifecycles

**Principle:** Four lifecycle patterns:

```text
Persistent Test Stack           — always running, apply changes incrementally; fast but can wedge
Ephemeral Test Stack            — create fresh each run; clean but slow
Dual Persistent + Ephemeral     — ANTI-PATTERN (combines drawbacks of both)
Periodic Stack Rebuild          — persistent with scheduled teardown; cost-saving, masks issues
Continuous Stack Reset          — rebuild out-of-band from main test stage
```

**Do:**
- Use Persistent when updates are reliable and speed matters.
- Use Ephemeral when rebuild time is acceptable and clean state is essential.
- Use Periodic for cost reduction (destroy end-of-day, rebuild morning) when you have an "out of hours."

**Don't:**
- Use Dual Persistent + Ephemeral — "using both types of stack lifecycles often combines the disadvantages of both."
- Rely on Periodic rebuilds to mask resource leaks — that's "at best a temporary hack, and at worst a way to allow problems to build up until they cause a production outage."

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Test Instance Lifecycles", "Persistent Test Stack", "Ephemeral Test Stack", "Dual Persistent and Ephemeral Stack Stages", "Periodic Stack Rebuild", "Continuous Stack Reset"*

---

### Cluster 64 — Online Testing Stages (Preview / Verify / Outcome)

**Principle:** Three kinds of online validations:

```text
Preview     — see what changes will be made (terraform plan)
Verify      — assert about infra resources (exists, is_running, has_attached)
Outcomes    — prove infra works (can_connect, http_request)
```

**Code (verification test):**
```text
given virtual_machine(name: "myappserver") {
  it { exists }
  it { is_running }
  it { passes_healthcheck }
  it { has_attached storage_volume(name: "appserver-storage")
}
```

**Code (outcome test):**
```text
given stack_instance(stack: "shopspinner_networking",
                     instance: "online_test") {
  can_connect(ip_address: stack_instance.appserver_ip_address
              port:443)
http_request(ip_address: stack_instance.appserver_ip_address
              port:443,
              url: '/').response.code is('200')
}
```

**Do:**
- Use testing frameworks (awspec, Chef InSpec, TaskCat, Terratest) for structured assertions.
- Combine basic assertions (`exists`) with combination assertions (`has_attached`) and outcome assertions (`can_connect`).
- Move complex conditional logic into modules so the stack test stays simple.

**Don't:**
- Rely on previews to be deep — they usually don't check that referenced resources exist.
- Use the same stack code for both preview and outcome validation — different purposes, different scopes.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Online Testing Stages for Stacks", "Preview: Seeing What Changes Will Be Made", "Verification: Making Assertions About Infrastructure Resources", "Outcomes: Proving Infrastructure Works Correctly"*

---

### Cluster 65 — Deployment Strategies (Push / Pull / GitOps / IfC / IaD)

**Principle:** Software deployment strategies, extended for infrastructure:

```text
Push deployment          — pipeline pushes code to deploy
Pull deployment          — infra code specifies software to install; deployed when infra provisioned
GitOps                   — continuous reconciliation loop (declarative, versioned, pulled, reconciled)
Application Infrastructure Descriptor — app deployment includes infra descriptor
Infrastructure from Code — infra embedded in app code, provisioned on deploy/run
Infrastructure as Data   — Controller pattern; continual sync (Crossplane, ACK, Config Connector)
```

**Do:**
- Use **drift detection** as part of GitOps/IaD — reapply code when target resources change.
- Combine with monitoring: "Teams that use drift detection should be especially sure to have monitoring in place to report when code has been reapplied" (to detect loops).

**Don't:**
- Apply preview-based testing alone for reusable stacks — "less useful for testing code that you intend to reuse across multiple instances."
- Implement IfC without recognizing it ties infrastructure to application lifecycle — fine for serverless, harder for shared infra.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Understanding Software Deployment Strategies", "Using Infrastructure Deployment Strategies", "Infrastructure as Data"*

---

### Cluster 66 — Drift Detection & Correction

**Principle:** Two definitions of drift:
- Older: drift between instances that should be consistent (e.g., dev vs prod).
- Newer: drift between code and the deployed instance.

Drift detection runs when the target resources have changed (e.g., manual UI changes, partial outages, crashes).

**Do:**
- Implement drift detection by running an idempotent tool in a loop (every minute or so).
- Use `terraform plan -detailed-exitcode` to detect drift without running apply.
- Have monitoring to report reapplications.

**Don't:**
- Treat drift detection as "fire and forget" — silent loops of apply/revert/apply can hammer your systems.
- Skip drift detection on the assumption that humans won't touch infra — they will, especially under pressure.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Drift Detection and Correction"*

---

### Cluster 67 — Changing Infrastructure Safely (Expand and Contract)

**Principle:** The recommended pattern for changing live infrastructure without destroying resources:

```text
Expand and Contract (Parallel Change):
  Step 1 (Expand)   — add the new resource
  Step 2 (Switch)   — change usage from old to new
  Step 3 (Contract) — remove the old resource
```

Each step is a separate change pushed through the pipeline and tested.

**Do:**
- Use Expand and Contract by default — works with any tool, even those without editable state files.
- Each step is independently rollback-able.

**Don't:**
- Apply all three steps in one change — that's the "destroy and rebuild" antipattern that interrupts service.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Use Expand and Contract to Incrementally Change Live Infrastructure"*

---

### Cluster 68 — State File Remapping & Infrastructure Surgery

**Principle:** With external state files (Terraform, OpenTofu, Pulumi), you can safely rename/move resources using:
- **Terraform/OpenTofu `moved` blocks** — idempotent within a stack
- **Pulumi aliases** — cleaner code form
- **`tfmigrate`** — scripted migration, supports between-state-file moves
- **Manual state editing** — "infrastructure surgery," risky last resort

**Do:**
- Use `moved` blocks / aliases for rename-within-stack.
- Clean up `moved` blocks after the change has been applied to all instances.
- Back up state before any surgery.

**Don't:**
- Do infrastructure surgery casually — "Teams should avoid infrastructure surgery except in extreme situations."
- Skip backing up state — the worst-case mess may be unrecoverable.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Manually Remap Live Infrastructure", "Remap Live Infrastructure in Pipelines", "Define Changes to Live Infrastructure in Code", "Script Live Infrastructure Changes"*

---

### Cluster 69 — Minimizing Disruption (Blue-Green, Rolling, Canary, Immutable)

**Principle:** Three deployment patterns for zero-downtime:

```text
Blue-green    — new instance, switch traffic, drain old, destroy old
Rolling       — incrementally add new nodes, remove old ones (canary = stagger to detect issues)
Immutable     — new instance tested offline, then swap; old can be restored easily
```

Teams that deploy to production more often have higher reliability — they *must* use these techniques to make frequent deployments possible.

**Do:**
- Use blue-green for stateful components that need clean switchover (DBs with replicas, app servers).
- Use rolling upgrades for container cluster nodes — modern orchestration handles it natively.
- Use canary for risky changes — monitor each node before moving on.
- Build phoenix servers — rebuild instances frequently.

**Don't:**
- Implement blue-green at the data center level for frequent releases — it becomes unwieldy; move to per-service blue-green.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Blue-Green Deployments", "Rolling Upgrades and Canary Releases", "Immutable Infrastructure"*

---

### Cluster 70 — Managing Data When Changing Infrastructure

**Principle:** Four data management strategies:

```text
Store and Load                     — back up before destroy, restore after create (simplest, slowest)
Continuous Data Transfer           — stream from old to new (active-passive, brief switchover)
Segregate Data Infrastructure       — data in separate stacks; other changes don't touch it
Separate Software and Data Changes  — change DB schema separately from app code; back-compat first
Use Continuous Disaster Recovery   — reuse normal deploy processes for DR
```

**Do:**
- Separate data-hosting infrastructure into its own stacks — avoids coupling and speeds non-data changes.
- Make new software versions backward-compatible with old data formats; deploy software first, then change data format.
- Use lifecycle hooks (e.g., FaaS triggered before destroy/after create) for store-and-load.

**Don't:**
- Try to do data + software + infra changes in one release when the data format changes incompatibly.
- Treat DR as a separate process — make it just another deploy.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Managing Data When Changing Live Infrastructure"*

---

### Cluster 71 — Shift-Left Governance & DevSecOps

**Principle:** Governance concerns (compliance, security, quality) addressed as early as possible — extending TDD and "build quality in" to all aspects of governance.

**Do:**
- Run all possible checks during development and the build pipeline — immediate feedback for violations.
- Replace gatekeeper governance teams with:
  - Security **enablement** teams (training, docs, collaboration)
  - Security **scanning service** teams (pipeline tools, scanners)
  - Security **research** teams (new risk areas like generative AI)
- Implement DevSecOps: jointly own responsibility for governance.
- Have automated policy checks throughout the delivery lifecycle — no code change deploys without controls and approvals.

**Don't:**
- Keep governance specialists as separate gatekeepers for every change.
- Skip automation because "we trust our developers" — automation is what makes trust scalable.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Shift Left", "Team Topologies for Shifting Left"*

---

### Cluster 72 — Compliance as Code (Three Control Types × Two Dimensions)

**Principle:** Three control types:

```text
Detection      — report violations for human action
Prevention     — block noncompliant actions (e.g., reject deployment)
Correction     — auto-fix violations (e.g., remove unauthorized user)
```

Two dimensions for implementation:

```text
Component design layers (broader at bottom, specific at top):
  - Global infrastructure restrictions (lower)
  - Workload-specific exceptions (higher)

Workflow stages:
  - Platform control    — IaaS policies
  - Delivery control    — pipeline tests
  - Deployment control  — runtime checks
  - Monitoring control  — continuous validation
```

**Do:**
- Implement broader restrictions at lower layers; specific exceptions at higher layers (deny inbound by default, allow 443 at the workload).
- Apply controls across *all* environments, not just production — catch issues early.
- Log everything for audit trail.

**Don't:**
- Use only prevention controls for ambiguous risks — detection + human response is often safer (e.g., logging rather than blocking suspicious activity, to avoid giving attackers a DoS vector).
- Skip correction controls — automated fix + report is often better than report-only.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Compliance as Code", "Controls by Component Design Layer", "Controls by Workflow"*

---

### Cluster 73 — Walking Skeletons & Tracer Bullet Pipelines

**Principle:** A **walking skeleton** is an end-to-end minimal implementation that lets you start testing and getting feedback. A **tracer bullet pipeline** is the same idea for delivery pipelines — a starting iteration evolved along with the system.

**Do:**
- Build walking skeletons early — they help you work out how to build, test, configure, and deploy multiple components.
- Start with a tracer bullet pipeline — evolves with the system.

**Don't:**
- Build components one at a time and wait for "the system" to be testable at the end — you'll discover integration problems too late.
- Confuse "increment" (small change as part of larger intent) with "build component-by-component" (paint-by-numbers).

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Break a Change into Increments"*

---

### Cluster 74 — Handling Incomplete Changes

**Principle:** Strategies for when an increment can't be put into active use:

```text
Feature branches     — merge only when complete (limits feedback; risk accumulates)
Feature toggles      — deploy code, activate only for some environments
Feature hiding       — deploy but not actively used; can be dark-launched for testing
```

**Do:**
- Default to **feature toggles** + trunk-based development — gets code into production and tested without exposing unfinished features.
- Use **dark launching** to test new elements with production data without putting them in the critical path.

**Don't:**
- Default to long-lived feature branches — they defer integration pain and accumulate risk.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Handle Incomplete Changes"*

---

### Cluster 75 — FoodSpin Case Study: Evolution Patterns

**Principle:** The fictional FoodSpin case study illustrates recurring patterns:

```text
Container cluster + worker pool       — varying min_workers/max_workers per env
Shared compute team                   — provides container cluster as service to multiple app teams
Database service team                 — provides DB infra as service with policy checks
Vertical decomposition               — infra stacks per workload (browse/search/admin stacks)
Cluster slow load-balancer rules      — split into separate stack to keep dev envs fast
Database in same stack as compute     — split when patching compute triggered DB restores
Multitenancy                          — multiple FoodSpin customers in separate infra instances
PCI data                              — separate infra instances from other workloads
```

The chapter's team deliberately evolved shared stacks into per-workload stacks as different lifecycles became apparent.

**Do:**
- Recognize when a "shared stack" is really a single concern with different cadences.
- Look at commit history to find which resources change together — that's the signal for cohesion.
- Use **shared-nothing architecture** when contention is a concern.

**Don't:**
- Default to "one big stack for performance/efficiency" — contention and ownership will surface later.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Sharing Stack Instances Across Workloads", "Component lifecycles"*

---

### Cluster 76 — Anti-Patterns Catalog

**Principle:** The book's anti-pattern taxonomy:

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| **Monolithic Stack** | Slow deploys, difficult testing, high coupling, poor DORA metrics | Split into smaller stacks |
| **Snowflakes as Code** | Instances diverge because changes aren't applied comprehensively | Use Reusable Stack + config injection |
| **Multi-Environment Stack** | Conditional code per env creates drift, undermines consistency | One stack + config parameters |
| **Configuration in Code** | Per-env values hardcoded in stack code (violates Demeter) | Externalize config (files, registry) |
| **Obfuscation Module** | Wrapper module that doesn't simplify or add value | Remove or replace with raw resource |
| **Spaghetti Module** | Too many params/conditionals; harder than raw resources | Split into focused modules |
| **Modular Monolith** | Modules deployed as single unit; no benefit | Split into separate stacks |
| **Unshared Module** | Module used by only one stack; YAGNI | Inline or wait for rule-of-three |
| **Dual Persistent + Ephemeral** | Combines disadvantages of both lifecycles | Pick one |
| **Infrastructure Surgery** | Manual state file edits; risky, error-prone | Use moved blocks, Expand and Contract, tfmigrate |
| **ClickOps** | Manual infra changes via UI; can't be reproduced | Use IaC for everything |
| **Automation Fear Spiral** | Don't automate because inconsistent; inconsistent because no automation | Start small, build confidence |

**Do:**
- Treat this catalog as a checklist when reviewing IaC designs.
- Recognize the smell before the full anti-pattern develops.

**Don't:**
- Rationalize "we're different" without checking the underlying mechanism.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Designing Deployable Infrastructure Stacks", "Configuring Infrastructure Stack Instances", "Designing Infrastructure Code Libraries", "Test Instance Lifecycles"*

---

### Cluster 77 — Decision Heuristics

**Principle:** When to use which pattern — a summary:

```text
Reusable Stack           — default; use unless you have a real reason to fork
Parameter Registry       — default for configuration; use over per-stack config files
Resource Matching        — when teams agree on naming/tags and tool diversity matters
Stack State Lookup       — when all teams use the same tool and want explicit contracts
Integration Registry     — when teams use different tools or want true decoupling
Dependency Injection     — default for stack-to-stack wiring; avoids distributed monolith
Facade Module            — simple, single-resource wrappers
Bundle Module            — static, cohesive collection of related resources
Infrastructure Domain Entity — dynamic sizing/composition (use imperative language)
Stack Module             — Terraform/OpenTofu workaround for lack of stack packaging
Persistent Test Stack    — fast feedback, reliable updates
Ephemeral Test Stack     — clean state per run, rebuild time acceptable
Immutable Server         — default for production workloads
Continuous Sync          — when you can't replace (legacy, stateful)
Baking + Frying          — combine: bake large items, fry per-instance config
Expand and Contract      — default for changing live infra safely
Build Once Deploy Many   — default for environments needing consistency
Trunk-Based Development  — default for IaC with fast test suites
Fan-in                  — within a single stream-aligned team
Federated               — across teams; requires mature dep management
GitOps / IaD             — default for Kubernetes-style continuous reconciliation
```

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — entire book*

---

### Cluster 78 — Key Takeaways (Morris's Ten Theses)

**Principle:** The ten recurring themes distilled:

1. **Optimize for change.** Stability comes from the ability to make changes frequently and reliably.
2. **Build small, independent pieces.** Smaller stacks = smaller blast radius, faster feedback, more independent teams.
3. **Treat infrastructure code as real code.** Code reviews, automated testing, CI/CD, design principles, technical-debt management.
4. **Use progressive testing.** Fast offline checks → integration tests → production monitoring. Swiss cheese model.
5. **Make governance automatic.** Define compliance as code, shift left, run continuously. The normal pipeline should be fast enough for emergency fixes.
6. **Align infrastructure with workloads.** Application-driven design, vertical decomposition, not horizontal layers.
7. **Keep environments consistent.** Reusable Stack + build-once-deploy-many.
8. **Automate everything.** Every procedure scripted, every change through a pipeline. Break the automation fear spiral.
9. **Evolve incrementally.** Walking skeletons, tracer bullet pipelines, no speculative complexity.
10. **The field is still evolving.** IfC, IaD, application-driven deployment — tools will change but patterns hold.

*Ref: Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md — "Key Themes and Takeaways"*

---

## Anti-Patterns & Common Mistakes

- **Monolithic Stack:** A single stack that has grown too large, containing resources for unrelated workloads with low cohesion → *fix:* split into smaller stacks by workload or lifecycle.
- **Snowflakes as Code:** Infrastructure managed with code but instances diverge because changes aren't applied comprehensively → *fix:* Reusable Stack + build-once-deploy-many + automated delivery pipelines.
- **Multi-Environment Stack:** Conditional code per environment in a single stack project → *fix:* one stack + config parameters + parameter registry.
- **Configuration in Code:** Per-instance values hardcoded in stack code (violates Demeter) → *fix:* Stack Parameter Registry or Dependency Injection.
- **Obfuscation Module:** Wrapper module that doesn't simplify or add value → *fix:* remove and use raw resource definition.
- **Spaghetti Module:** Module with too many parameters and conditional branches → *fix:* split into focused modules.
- **Modular Monolith:** Divided into modules but deployed as single unit → *fix:* split into separate, independently deployable stacks.
- **Unshared Module:** Module used by only one stack project → *fix:* wait for rule of three; inline if not needed.
- **Dual Persistent + Ephemeral Stack Stages:** Combines disadvantages of both lifecycles → *fix:* pick one.
- **Infrastructure Surgery:** Manual state file edits to remap resources → *fix:* moved blocks, Expand and Contract, tfmigrate scripts.
- **ClickOps:** Manual infra changes via IaaS UI → *fix:* define and apply via IaC pipeline.
- **Automation Fear Spiral:** Don't automate because inconsistent; inconsistent because no automation → *fix:* start small, face fears, build confidence through testing.
- **Cloud-Agnostic Abstraction Layers:** Hidden cloud-specific details behind a lowest-common-denominator abstraction → *fix:* build a well-designed engineering platform that exposes cloud specifics.

## Decision Heuristics / Checklists

- **Choosing IaC tool family:** Server config tools for OS/app config; stack DSL for resource provisioning; stack GPL when devs write infra and need testing/typing; IaD for continuous reconciliation; IfC for tightly coupled app+infra.
- **Idempotent vs Procedural:** Always idempotent. If you find yourself adding existence checks, move to a declarative tool.
- **Declarative vs Imperative:** Default declarative for static resource definitions; imperative when conditional logic, loops, or dynamic composition required.
- **Stack sizing:** Default Single Service Stack; Shared Stack for genuinely shared resources; Micro Stack only when one part genuinely needs different cadence.
- **Reusable Stack vs Snowflakes:** Default Reusable Stack. Resist the urge to copy/fork — it's the path back to sprawl.
- **Configuration injection:** Prefer Stack Parameter Registry; move toward Dependency Injection for stack-to-stack wiring.
- **Resource discovery:** Resource Matching for tool-agnostic + naming/tag contracts; Stack State Lookup when same tool + explicit publish; Integration Registry for cross-team / cross-tool.
- **Module patterns:** Facade for simple wrappers; Bundle for static cohesive sets; Domain Entity for dynamic sizing (imperative language); Stack Module as Terraform workaround.
- **Server updates:** Default Immutable Server; Continuous Sync for legacy/stateful; never "push on change."
- **Bake vs Fry:** Bake large items (JDK, Tomcat, container cluster); fry per-instance config.
- **Testing strategy:** Test pyramid for imperative-heavy; test diamond for declarative; Swiss cheese for risk-based coverage.
- **Test instance lifecycle:** Persistent for fast feedback; Ephemeral when rebuild time OK; Continuous Reset as a hybrid.
- **Delivery workflow:** Trunk-based for fast feedback; build-once-deploy-many for consistency; fan-in within teams, federated between teams.
- **Changing live infra:** Default Expand and Contract; moved blocks / aliases for rename; tfmigrate for between-state-file moves; avoid manual surgery.
- **Deployment strategies:** GitOps/IaD default for continuous reconciliation; Push for one-off; Pull for infra-defined installs; IfC for app-coupled.
- **Minimizing disruption:** Blue-green for stateful switchover; rolling for clusters; canary for risky changes; immutable for safety.
- **Data management:** Separate data infra into its own stacks; separate software and data schema changes; use continuous DR as normal deploy.
- **Governance:** Detection for ambiguous risk; prevention for clear-cut violations; correction when safe to auto-fix. Apply controls across all environments.

## Key Takeaways

1. **Optimize for change.** DORA proves no speed/quality trade-off — high performers do both. IaC exists to make changes fast and safe.
2. **Three core practices:** Define everything as code; continually test and deliver all work in progress; build small, simple pieces that can change independently.
3. **Code executes *during* deployment** — not after. This is the fundamental difference from application code and drives every IaC design decision.
4. **Apply CUPID + cohesion/coupling + DRY-with-judgment + Conway's Law** — the same SWE principles work, with IaC-specific nuances.
5. **Reusable Stack + Stack Parameter Registry + Dependency Injection** = the core patterns for managing many instances consistently.
6. **The five-stage CD workflow** (Development → Build → Test → Release → Run) repeats for every incremental change — keep all code production-ready.
7. **Progressive testing + Swiss cheese + test diamond** = the testing strategy for declarative IaC.
8. **Expand and Contract + moved blocks + immutable servers + blue-green/rolling/canary** = the safe-change toolkit.
9. **Shift left + compliance as code** — build governance into the pipeline, not onto the side of delivery.
10. **Trunk-based + build-once-deploy-many + fan-in/federated integration** = the delivery patterns that match CD principles.

## Cross-References

- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] — AWS resilience patterns that complement IaC
- Related: [[../Continuous_Deployment.md]] — deployment practices that pair with IaC pipelines
- Related: [[../The_DevOps_Handbook.md]] — Three Ways + cultural practices for IaC adoption
- Related: [[../Fundamentals_of_Software_Architecture.md]] — architectural principles (CUPID, cohesion/coupling) applied to IaC
- Related: [[../Modern_Software_Engineering.md]] — Farley's empirical engineering framework that grounds IaC discipline
- Related: [[../Team_Topologies.md]] — Stream-aligned/enabling/platform team patterns for IaC delivery
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] — Platform engineering context for IaC teams
- Related: [[../Learning_Systems_Thinking.md]] — Systems-thinking foundation for the design forces framework
- Topic index: [[../INDEX.md]]