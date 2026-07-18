# Building Multi-Tenant SaaS Architectures

**Author:** Tod Golding
**Topic tags:** `#architecture` `#api` `#cloud` `#platform`
**Language focus:** language-agnostic (AWS-leaning examples)
**Sources:** `markdown_output/Building Multi-Tenant SAAS Architectures/Building Multi-Tenant SAAS Architectures.md` · `summaries/Building_Multi-Tenant_SAAS_Architectures.md`

## TL;DR
SaaS is a business model first and a multi-tenant architecture second. The architecture splits into a control plane (the "single pane of glass" — onboarding, identity, tenant management, admin console — *not* itself multi-tenant) and an application plane (the product, where tenant context flows as a JWT through every service). Tenant context (typically embedded as custom claims in a JWT) is the connective tissue that powers logging, metrics, data access, routing, and isolation. Apply when designing a new SaaS product, migrating from installed/managed-service software to SaaS, or scaling an existing SaaS architecture across tiers and deployment models.

---

## Best Practices by Topic

### The SaaS Mindset — Business Strategy and Technical Strategy Together, Day One

**Principle:** SaaS is not a technology pattern bolted onto a product; it is a fundamental business model transformation. The book is explicit: "You do not design a multi-tenant architecture first and then figure out the business layer." The architect and the business strategist must co-evolve.

**Core SaaS business objectives:**
- **Agility** — speed of releasing features, reacting to market dynamics, changing pricing models.
- **Operational efficiency** — centralized management, automated deployment, streamlined operations.
- **Cost efficiency** — economies of scale through shared infrastructure, correlated consumption with tenant activity, maximized margins.
- **Building a service, not a product** — prioritize the overall service experience over chasing one-off feature requests. "The needs of the many outweigh the needs of the few."

**Distinguish SaaS from MSP (Managed Service Provider):** MSPs centrally manage separate customer environments running different versions. They inherit the complexity of per-customer variations and cannot achieve SaaS agility. SaaS providers enforce one version for all tenants and operate through a single pane of glass.

**Do:**
- Build a business model and strategy *first* — target markets, tenant personas, growth expectations, margins — before making architectural decisions.
- Treat every one-off customer exception as a warning signal. Every compromise that moves toward an MSP model erodes the agility, efficiency, and scalability that motivated the move to SaaS.
- Adopt a service-centric mindset: the product is the entire service experience.

**Don't:**
- Don't start by designing a multi-tenant architecture and figure out the business layer later.
- Don't accept one-off customizations even for premium customers. Use tiers and feature flags.
- Don't call your MSP a SaaS. The distinction matters operationally.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 1. The SaaS Mindset"; "Chapter 17. Guiding Principles"*

---

### Redefining Multi-Tenancy — Unified Management, Not Shared Infrastructure

**Principle:** The traditional view equates multi-tenancy with shared infrastructure. Golding argues this is too narrow. Resources exist on a spectrum from fully pooled (shared by all tenants) to fully siloed (dedicated per tenant), with many hybrid configurations in between. **What makes a system multi-tenant is not whether infrastructure is shared, but whether all tenants are onboarded, deployed, managed, and operated through a single, unified experience.** The term "single-tenant" is explicitly discarded; every architecture in the book is multi-tenant by this definition.

**Do:**
- Default to "unified experience" as the multi-tenant test, not "shared hardware."
- Build deployment models that allow fine-grained silo/pool decisions per service, per tier, per resource type.

**Don't:**
- Don't conflate "multi-tenant" with "shared-everywhere." The two are independent axes.
- Don't let "fully siloed premium tier" become an excuse for per-tenant customization.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 1" / "Redefining Multi-Tenancy"*

---

### Control Plane + Application Plane — The Two Halves of Every SaaS

**Principle:** Every SaaS architecture splits into two halves:

1. **Control Plane** — the "single pane of glass" providing all cross-cutting, horizontal services: onboarding, identity, metrics, billing, tenant management, admin console. Crucially, control plane services are *not* multi-tenant themselves — they serve the SaaS provider, not individual tenants. They are the foundation upon which tenancy is built. **Build the control plane first.**
2. **Application Plane** — where the actual SaaS product features live. A "blank canvas" that varies by domain and business, implementing multi-tenant principles: tenant context, isolation, data partitioning, routing. This is where tenants interact with the system.

**Do:**
- Build the control plane first (onboarding, identity, tenant management). It forces tenancy into the architecture from day one.
- Keep the control plane in a separate account from the application plane (when on AWS).
- Update the control plane on its own schedule (operational/internal) and the application plane on its own schedule (feature/tier).

**Don't:**
- Don't start with the application and bolt on tenancy later. The book is explicit: "Starting with the application and bolting on tenancy later does not work."
- Don't make control plane services multi-tenant. They serve the SaaS provider, not the tenants.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 2" / "The Two Halves: Control Plane and Application Plane"; "Chapter 17" / "Build the multi-tenant foundation on day one"*

---

### Tenant Context — The JWT as Connective Tissue

**Principle:** Tenant context — typically represented as a JSON Web Token (JWT) — is the most fundamental concept in the application plane. It packages user identity with tenant attributes (tenant ID, tier, role) and flows through every service and resource interaction. This token enables tenant-aware logging, metrics, data access, routing, and isolation.

**Do:**
- Embed tenant attributes as *custom claims* in JWTs at authentication time. This eliminates centralized lookups in services.
- Propagate the JWT as a bearer token through every downstream service call. (The Order service passes it to the Product service, which passes it further, etc.)
- Use the identity provider (Amazon Cognito, Okta, etc.) to inject custom claims during token issuance.
- Aim for "a service never needs to invoke some external mechanism to resolve tenant context."

**Don't:**
- Don't store tenant context only in the JWT — but never look it up again. The JWT should be the universal currency.
- Don't authenticate-then-look-up. Every lookup adds latency and creates a single point of failure.
- Don't confuse authentication with isolation (see below).

**Code (JWT custom claims example, conceptual — OIDC claims merged with tenant context):**
```json
{
  "sub": "user-12345",
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "custom:tenant_id": "tnt_8f3a2c91",
  "custom:tenant_tier": "premium",
  "custom:role": "admin"
}
```
*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 4" / "SaaS Identity"; "Chapter 2" / "Tenant Context"*

---

### SaaS Identity — Every User Bound to a Tenant

**Principle:** Identity in SaaS is fundamentally different from classic authentication. Every user must be bound to a tenant — this user/tenant binding is what Golding calls a **SaaS identity**. Identity providers (Amazon Cognito, Okta, Auth0) can be configured with custom claims in JWTs to embed tenant ID, tier, and role directly into authentication tokens.

**Key identity patterns:**
- **Federated identity** — support SSO via external identity providers (SAML, OIDC) while still binding users to tenants. Some IdPs (Amazon Cognito) can seamlessly stitch custom claims into JWTs even when authentication is federated.
- **Tenant grouping constructs** — map external identity groups to internal tenant identifiers.
- **Separation of authentication from isolation** — authenticating a tenant is *not* the same as isolating their resources.

**Do:**
- Configure custom claims for tenant ID, tier, role at identity-provider level.
- Map federated identity groups to internal tenant constructs.
- Per-tier identity settings (MFA, password policies) can be a differentiating feature.

**Don't:**
- Don't authenticate against an identity provider that has no awareness of tenant context without planning for token enrichment.
- Don't equate authentication to tenant isolation.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 4" / "SaaS Identity"; "Chapter 6" / "Authentication Flow"*

---

### Deployment Models — Silo, Pool, Hybrid, Mixed-Mode, Pod

**Principle:** Deployment model choices are fine-grained — they can vary per service, per tier, per resource type within a single SaaS environment.

| Model | Description | When to use |
|---|---|---|
| **Full Stack Silo** | Each tenant gets a completely dedicated stack (compute, storage, networking) | Strict compliance, early SaaS migration, premium tier |
| **Full Stack Pool** | All tenants share one infrastructure footprint | Maximum cost efficiency, noisy-neighbor tolerable |
| **Hybrid Full Stack** | Some tenants siloed (premium), others pooled (basic) | Tier-based mix |
| **Mixed Mode** | Individual services within a tenant's stack are siloed/pooled independently | Service-by-service trade-off (compute shared, DB siloed per tenant) |
| **Pod Model** | Groups of tenants placed into separate pods (clusters of shared resources) | Balance efficiency with isolation; limit blast radius |

**Do:**
- Default to pooled for non-differentiating capabilities; silo where compliance, isolation, security, tiering, or performance require it.
- Even within "Full Stack Silo," treat all siloed environments as part of one managed fleet: same version, same config, same policies. "In all respects, a full stack silo environment is treated the same as a pooled environment."
- Treat the deployment model as evolving over time. "Expect and be looking for ways to refine your deployment model based on the changing/emerging needs of customers."

**Don't:**
- Don't use Full Stack Silo as cover for per-tenant customization. The book is explicit: "The full stack silo only exists to accommodate domain, compliance, tiering, and any other business realities that might warrant the use of a full stack silo model."
- Don't ship the same deployment model for every service and every tier.
- Don't let per-tenant deployment differences become per-tenant code paths.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 3. Multi-Tenant Deployment Models"; "Chapter 13" / "Silo Lift-and-Shift"*

---

### Onboarding — Fully Automated and Repeatable

**Principle:** Onboarding weaves together the creation of tenants, users, identity constructs, and application resources. It must be fully automated and repeatable. Onboarding is also where deployment, identity, routing, and tiering strategies are put into action — every multi-tenant design choice is ultimately expressed through the onboarding process.

**Onboarding flow:**
1. Receive create-tenant request (company name, identity config, tier, ...).
2. Generate a tenant identifier (GUID — globally unique, immutable, opaque; never derived from tenant name).
3. Provision tenant resources via Provisioning service (tier-aware: basic gets pooled, premium gets siloed).
4. Add tenant to billing system (correlate tenant profile to preconfigured billing plan).
5. Set up admin user with tenant custom claims.
6. Update onboarding state throughout (track each step; handle failures gracefully).

**Do:**
- Track onboarding state explicitly. Each step must be observable and recoverable.
- Use tier-based onboarding: basic tier → pooled resources, premium tier → siloed resources.
- Treat onboarding as the *executable expression* of your deployment model.
- Add automated tests for onboarding: load tests, recovery tests, performance tests at the per-tenant and per-tier level.

**Don't:**
- Don't manually onboard. The book is explicit: onboarding must be fully automated.
- Don't conflate onboarding with the Provisioning service — onboarding orchestrates Provisioning (and Tenant Management, Identity, Billing, etc.).

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 4. Onboarding and Identity"; "Chapter 5. Tenant Management"*

---

### Tenant Management — Central Registry for Tenant State

**Principle:** The Tenant Management service is the central registry for all tenant state and configuration.

**Core responsibilities:**
- Store tenant attributes (identifier, name, status, tier, onboarding state, last active date).
- Manage identity configuration (MFA policies, password policies, IdP mappings).
- Store infrastructure configuration (routing patterns, per-tenant URLs, siloed resource references).
- Manage per-tenant keys and secrets.
- Track all users associated with a tenant.

**Tenant identifiers:** GUIDs — globally unique, immutable, opaque (not derivable from tenant names). Friendly names (subdomains, vanity domains) map to internal IDs but remain separate to allow renaming without cascading changes.

**Tenant lifecycle:**
- **Activation / Deactivation** — temporarily enable/disable access. Deactivation can be triggered by billing events (delinquent payments) and must propagate to identity and authentication.
- **Decommissioning** — removing resources entirely. Requires locating and selectively removing data from pooled storage, deleting siloed resources, archiving state. A dedicated Decommissioning service is recommended.
- **Tier Changes** — can range from simple (update feature flags, throttling policies in pooled model) to complex (migrate data from pooled to siloed storage when upgrading from basic to premium).

**Do:**
- Build a dedicated Tenant Management service as part of the control plane.
- Use GUIDs for internal tenant identifiers; keep friendly names separate.
- Beware of Tenant Management becoming a bottleneck. Embed critical tenant attributes in the JWT to avoid frequent lookups.

**Don't:**
- Don't let Tenant Management be the source of truth for tenant data that's also queried from every service. Hot data goes in the JWT.
- Don't use tenant name as the internal identifier. Renames would cascade.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 5. Tenant Management"*

---

### Routing Authenticated Tenants

**Principle:** Once authenticated, requests must be routed to the correct shared or dedicated resources.

**Routing strategies:**
- **Domain-based:** `tenantA.saasprovider.com` → tenant mapping → tenant ID → route to tenant's resources.
- **Single-domain + JWT:** one shared domain; tenant context extracted from the JWT custom claims.
- **Serverless routing:** API Gateway with custom authorizers that extract tenant context and route to Lambda functions.
- **Container routing:** Kubernetes ingress controllers, namespace-based routing, or service mesh constructs (Istio).
- **API Gateway-per-tenant:** separate gateways for premium tier (siloed) and basic tier (pooled).

**Do:**
- Scale-aware gateway design. Having a gateway-per-tenant may not scale for thousands of tenants; reserve it for premium-tier tenants.

**Don't:**
- Don't centralize routing in the application code. Use the gateway / ingress / mesh to keep services tenant-agnostic at the routing level.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 6. Tenant Authentication and Routing"*

---

### Building Multi-Tenant Services — Hide the Complexity from Developers

**Principle:** Services in pooled multi-tenant environments face unique challenges around noisy neighbor, tenant-aware logging and metrics, tiered storage, and tenant isolation. The book emphasizes extracting all multi-tenant code into reusable libraries and helper functions so service code stays focused on business logic.

**Pattern: A Code-Level Walkthrough (Order service in Python):**

1. **Baseline:** vanilla service, no tenant awareness.
2. **Extract tenant context:** decode the JWT from the Authorization header to get tenant ID and tier.
3. **Logging and metrics with tenant context:** inject tenant context into log messages; publish tenant-aware metrics (e.g., query duration by tenant) to a data pipeline (Amazon Kinesis Data Firehose).
4. **Data access with tenant context:** tenant ID as partition key in pooled DynamoDB queries; resolve table names dynamically based on tenant tier (pooled table for basic, siloed table per tenant for premium).
5. **Tenant isolation:** AWS STS `assume_role` with tenant-scoped IAM policies to acquire credentials that restrict database access to *only* the current tenant's items — regardless of what a developer puts in a query.

**Interception tools and strategies:**
- **Aspects (AOP):** weave pre/post-processing logic into services.
- **Sidecars (Kubernetes):** containers between services and resources that apply tenant policies.
- **Middleware (e.g., Express.js):** framework-level request interception.
- **AWS Lambda Layers / Extensions:** shared libraries deployed independently.
- **Helper libraries** that wrap every multi-tenant operation.

**Do:**
- Provide `get_tenant_context(request)` as the standard first call.
- Wrap logging so tenant context is auto-injected.
- Wrap data access (DALs) so tier-based table resolution is invisible.
- Use scoped client factories for tenant isolation.

**Don't:**
- Don't scatter tenant-aware logic through service code. Centralize.
- Don't make every developer re-implement tenant context extraction.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 7. Building Multi-Tenant Services"; "Chapter 9" / "Isolation Through Interception"*

---

### Data Partitioning — Pooled, Siloed, Hybrid

**Principle:** Three partitioning strategies:

- **Pooled (shared):** all tenant data commingled in one table/index/bucket, partitioned by tenant ID. Maximizes efficiency but complicates isolation and noisy-neighbor management.
- **Siloed (dedicated):** each tenant gets separate storage (separate table, database, bucket, or index). Simplifies isolation and compliance but reduces economies of scale.
- **Hybrid:** some data pooled, some siloed, varying by service and tier.

**Technology-specific patterns:**
- **Relational:** separate schemas per tenant, separate databases per tenant, or shared tables with a tenant ID column.
- **NoSQL (DynamoDB):** tenant ID as partition key in pooled tables, or separate tables per tenant. Capacity modes influence choices.
- **Object storage (S3):** key prefixes (pooled) or separate buckets per tenant (siloed). IAM policies enforce access at either level.
- **OpenSearch:** separate indexes per tenant or shared indexes with tenant-aware routing.

**Do:**
- Partition choice is per-service, per-tier, per-resource type. There is no single right answer.
- Plan for tier changes (pooled → siloed migration) and decommissioning (selective data removal) from day one.
- Encrypt data at rest and in transit; consider per-tenant encryption keys.

**Don't:**
- Don't assume pooling always saves money. Tier migrations and decommissioning complicate pooled storage.
- Don't use the same partitioning strategy for every service.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 8. Data Partitioning"*

---

### Tenant Isolation — Separate from Deployment, Enforced Explicitly

**Principle:** "Tenant isolation is treated as a distinct concern from data partitioning and deployment models. Just because resources are in separate databases does not mean they are isolated — isolation must be explicitly enforced." Golding's three isolation categories:

1. **Full stack isolation** — each tenant has a dedicated stack. Isolation via infrastructure boundaries.
2. **Resource-level isolation** — shared compute with dedicated resources (separate DBs, queues, buckets per tenant). Isolation boundary is an entire resource.
3. **Item-level isolation** — shared resources with commingled data. Most challenging; requires granular row-/message-level access control.

**Deployment-time vs. runtime isolation:**
- **Deployment-time:** isolation policies are attached to resources at provisioning (e.g., IAM policies on siloed microservice compute). No runtime dependency on code compliance.
- **Runtime:** isolation policies are dynamically applied per request using tenant context from the JWT. Requires code/libraries to acquire tenant-scoped credentials (STS `assume_role`). More flexible but introduces latency and relies on developer compliance.

**Scaling considerations:**
- Runtime isolation adds latency; use TTL-based credential caching.
- Policy templates (one parameterized policy for all tenants) avoid IAM service limits.

**Do:**
- Combine deployment-time isolation (for siloed resources) with runtime isolation (for pooled resources).
- Use STS `assume_role` with tenant-scoped IAM policies to make isolation independent of developer code.
- Centralize isolation in libraries / sidecars / aspects — remove developers from the isolation equation.

**Don't:**
- Don't trust the database to enforce isolation by itself. Use STS-style policies.
- Don't let runtime isolation introduce per-request latency without caching.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 9. Tenant Isolation"*

---

### EKS (Kubernetes) SaaS Patterns

**Principle:** Kubernetes provides natural multi-tenant constructs:
- **Namespaces** for logical isolation.
- **Resource quotas** for tiering.
- **Ingress controllers** for routing.
- **RBAC** for access control.

**EKS deployment patterns:**
- **Pooled namespace:** all tenants share one namespace with shared pods/services. Simplest but least isolated.
- **Siloed namespace per tenant:** each tenant gets a dedicated namespace with its own pods.
- **Node-per-tenant:** siloed namespaces bound to specific compute nodes for physical isolation.
- **Pod model:** groups of tenants distributed across multiple clusters (one for basic, one for premium).

**Tenant isolation in Kubernetes:**
- Network policies for traffic isolation.
- RBAC for API access.
- Pod security policies for workload constraints.
- Resource quotas for tier-based limits.

**Do:**
- Use namespaces as the primary isolation unit.
- Bind tier to resource quota (basic tier → lower quota, premium tier → higher).
- Mix EKS workloads with serverless functions (Lambda) for services where each fits better.

**Don't:**
- Don't deploy one cluster per tenant unless compliance demands physical isolation. Most cases work with namespace isolation.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 10. EKS (Kubernetes) SaaS Architecture Patterns"*

---

### Serverless SaaS Patterns

**Principle:** Serverless (Lambda, API Gateway, DynamoDB, S3) aligns naturally with SaaS: pay-per-use, automatic scaling, reduced operational overhead, fine-grained cost attribution.

**Serverless deployment patterns:**
- **Pooled Lambda functions:** all tenants share the same functions.
- **Siloed functions per tenant (or tier):** separate function deployments per tenant/tier.
- **Hybrid:** some functions pooled, some siloed.

**Concurrency and noisy neighbor:**
- Allocate different concurrency limits per tier (e.g., basic 100, advanced 300, premium: remaining capacity).
- **State Residue:** Lambda reuses execution environments. State from one tenant's request can leak to a subsequent request from a different tenant. Functions must explicitly clear state between invocations.

**Beyond compute:**
- Serverless storage: DynamoDB, S3.
- Serverless messaging: SQS, SNS.
- Serverless orchestration: Step Functions.
- A fully serverless SaaS stack is achievable.

**Do:**
- Use Lambda concurrency limits to protect higher-tier tenants from lower-tier consumption.
- Treat state residue as a first-class concern in pooled Lambda designs.
- Use Lambda Layers / Extensions to share multi-tenant utilities.

**Don't:**
- Don't store anything in a Lambda execution environment across invocations in pooled mode. State residue leaks across tenants.
- Don't forget to explicitly clear state between invocations.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 11. Serverless SaaS Architecture Patterns"*

---

### Tenant-Aware Operations — Beyond System Health

**Principle:** Operations in SaaS extends far beyond keeping the system running. It encompasses the entire tenant experience: onboarding quality, time to value, feature adoption, proactive issue detection.

**Five categories of multi-tenant operational metrics:**

1. **Tenant activity metrics** — onboarding progress, per-tenant application analytics, lifecycle events (declining usage, approaching renewal). Enable teams to identify tenants needing outreach.
2. **Agility metrics** — availability, deployment frequency, failed deployments, cycle time, MTTD/MTTR, defect escape rate (DORA-style).
3. **Consumption metrics** — how much of each shared resource individual tenants consume. Critical for pooled environments where native tools can't attribute usage per tenant.
4. **Cost-per-tenant metrics** — correlate tenant consumption with cloud billing data to approximate per-tenant infrastructure cost. Not an accounting function; an operational view that informs pricing, tiering, and margin analysis.
5. **Business health metrics** — MRR, churn, CAC, CLTV, CLTV/CAC ratio.

**Operations console:** views filtered by tenant, tier, time period; onboarding state, consumption dashboards, cost-per-tenant analysis, proactive alerts.

**Multi-tenant deployment automation:**
- Blue-green deployments.
- Canary releases targeting specific tenant populations (e.g., a canary tier).
- Automated rollback mechanisms.

**Do:**
- Layer metrics: API-level, microservice-level, infrastructure-level.
- Set up proactive alerts at multi-tenant stress points: throttling limits, database load, noisy neighbor indicators.
- Validate multi-tenant strategies with operational data continuously.

**Don't:**
- Don't treat operations as only "is it up?" Operations is the entire tenant experience.
- Don't stop at DORA metrics. Add tenant-specific metrics on top.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 12. Tenant-Aware Operations"*

---

### Tiering — Business Strategy and Technical Strategy

**Principle:** Tiering is "a strategy most architects have encountered as part of consuming various third-party offerings… but tiering can have a significant impact on many of the dimensions of your multi-tenant architecture." Tier is carried in the JWT and influences routing, security, throttling, storage, and deployment.

**Tiering patterns:**
- **Consumption-focused:** constrain tenant resource consumption by tier. Basic tier tenants should not consume infrastructure at the same rate as platinum tier tenants.
- **Value-focused:** different features, performance SLAs, capabilities per tier. Feature flags and RBAC.
- **Deployment-focused:** different deployment models per tier (basic: fully pooled; advanced: some siloed services; premium: full stack silo).
- **Free tiers:** powerful customer acquisition but must be carefully managed to limit cost exposure while providing enough value to convert.

**Implementation layers:**
- **API tiering:** API Gateway throttling policies (requests/sec, burst rate, daily quota); custom authorizers map tenant tiers to API keys.
- **Compute tiering:** Lambda concurrency limits; Kubernetes resource quotas per namespace.
- **Storage tiering:** different IOPS, throughput, capacity per tier; siloed vs. pooled by tier.

**Do:**
- Implement tiering at every layer that has a cost or SLA dimension.
- Apply tier policies automatically based on JWT custom claims — keep the client unaware.
- Track which tier a tenant belongs to in the JWT, not in per-service config.

**Don't:**
- Don't make tier a pricing-only concept. Tier influences infrastructure.
- Don't ship tier migrations that disrupt active tenants.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 14. Tiering Strategies"; "Chapter 5" / "Tier Changes"*

---

### Migration — Silo Lift-and-Shift First, Modernize Later

**Principle:** Migration is as much a business decision as a technical one. Two extremes: "modernize first" (delay release for clean architecture) vs. "SaaS now" (compromise on modernization to start operating as SaaS immediately). **Golding favors "SaaS now":** faster customer feedback, forces organizational transformation sooner.

**The Fish Model:** Borrowed from the Technology-as-a-Service Playbook. Costs rise during transformation; revenue may dip during pricing model transition. Goal: keep the "fish" as thin as possible before reaching the inflection point where SaaS efficiencies drive costs down and revenue up.

**Migration patterns:**
1. **Silo Lift-and-Shift** — fastest path. Each tenant gets a full stack silo with the existing application code, managed by a new control plane. All tenants run the same version. Recommended starting point for most migrations.
2. **Layered Migration** — progressively pool layers. Start with the web tier (least tenant-aware), then optionally the application tier. Each layer moved to shared infrastructure increases efficiency but requires more refactoring.
3. **Service-by-Service Migration** — incrementally extract functionality from monolith into multi-tenant microservices. Most modernized but most complex. Data must also be extracted.

**Foundation for every migration pattern:** Build the control plane (onboarding, identity, tenant management, admin console) first.

**Do:**
- Start with Silo Lift-and-Shift to get to SaaS fastest.
- Build the control plane first, regardless of migration pattern.
- Use real customer feedback and operational data to drive subsequent modernization.

**Don't:**
- Don't try to design a perfect architecture before going to market.
- Don't skip the control plane. Every pattern needs it.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 13. SaaS Migration Strategies"*

---

### SaaS Anywhere — When Tenants Need Remote Footprints

**Principle:** SaaS Anywhere addresses scenarios where parts of the SaaS architecture must run in tenant-controlled environments (on-prem, tenant cloud account, tenant data center).

**Three architecture patterns:**
- **Remote data:** tenant data in tenant environments, accessed by SaaS microservices. Compliance/security/volume driven.
- **Remote application services:** full microservices deployed to tenant environments.
- **Remote application plane:** entire application plane in tenant environments, only control plane in SaaS provider's environment. Most significant compromise — essentially full stack silo in remote locations.

**Ownership and drift:**
- The ideal gives the SaaS provider full control. The realistic scenario involves shared ownership with tenant administrators.
- Each concession to tenant-specific configurations erodes SaaS efficiency and agility — risks pulling the architecture toward an MSP model.
- Same-cloud remote (tenant's account in the same cloud provider) is preferred because it preserves access to all cloud constructs.

**Do:**
- Default to same-cloud remote when footprint must extend to tenant environments.
- Apply tiers consistently across remote footprints.
- Keep the control plane in the SaaS provider's environment to maintain unified management.

**Don't:**
- Don't let SaaS Anywhere become an excuse for per-tenant customization. Maintain unified management via the control plane.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 15. SaaS Anywhere"*

---

### GenAI in a Multi-Tenant SaaS

**Principle:** GenAI requires the same multi-tenant rigor as any other resource.

**Tenant refinements for GenAI:**
- **RAG with tenant context** — augment prompts with tenant-specific data before sending to the GenAI service. Example: ecommerce SaaS uses per-tenant product catalog data to generate domain-specific responses for a golf store vs. a clothing store. RAG data can be siloed (separate OpenSearch index per tenant) or pooled (shared index partitioned by tenant ID).
- **Fine-tuning** — global fine-tuning applies to all tenants (e.g., healthcare domain). Tenant-level fine-tuning creates logical per-tenant models pairing the base LLM with tenant-specific tuning parameters.
- **Combining RAG and fine-tuning** — both can be used together.

**Multi-tenant principles applied to GenAI:**
- **Tenant isolation:** one tenant's GenAI data (RAG indexes, fine-tuning models, prompts) cannot be accessed by another.
- **Noisy neighbor:** prevent one tenant's GenAI requests from saturating the system.
- **Onboarding:** automate creation of per-tenant RAG indexes and fine-tuning models as part of tenant provisioning.
- **Pricing and tiering:** GenAI introduces new cost dimensions (token consumption, model training, vector storage). Tiering strategies must account for these.

**Do:**
- Apply the same partitioning, isolation, tiering, and metering discipline to GenAI resources as to any other.
- Consider traditional AI/ML models (per-tenant via SageMaker) for cases requiring more granular control over inference infrastructure.

**Don't:**
- Don't ship GenAI features without tenant-aware partitioning and metering.
- Don't assume a shared LLM service is multi-tenant safe — your prompts and context may be too.

*Ref: Building Multi-Tenant SAAS Architectures.md — "Chapter 16. GenAI and Multi-Tenancy"*

---

## Anti-Patterns & Common Mistakes

- **MSP disguised as SaaS:** Centrally managing per-customer versions. *Fix:* Enforce one version for all tenants; single pane of glass.
- **Bolting tenancy onto an existing app:** Starting with the application and bolting on tenancy later. *Fix:* Build the control plane first.
- **Authentication-as-isolation:** Assuming authenticating a tenant achieves isolation. *Fix:* Add explicit isolation layer (STS assume_role, policies, runtime checks).
- **Full stack silo as customization cover:** Using siloed deployment to sneak in per-tenant code paths. *Fix:* Treat siloed environments as part of one fleet: same version, same config.
- **State residue in pooled Lambda:** Trusting Lambda execution environment isolation. *Fix:* Explicitly clear state between invocations.
- **Shared database, shared responsibility:** Trusting database row-level filters to enforce isolation. *Fix:* Combine with STS-scoped credentials.
- **One-off customizations:** Accepting a per-tenant exception "just this once." *Fix:* Tier-based or feature-flag-based, never per-tenant.
- **Tenant name as identifier:** Using tenant name as the internal ID. *Fix:* GUID, opaque, immutable; friendly name maps to it.
- **Centralized tenant lookups on every request:** Calling Tenant Management from every service. *Fix:* Embed tenant context in JWT; lookup only on cold paths.
- **Noisy neighbor in pooled compute:** All tenants share the same Lambda or pod. *Fix:* Concurrency limits per tier; silo where performance isolation matters.
- **Deployment model as one-time decision:** Picking silo or pool on day one and never revisiting. *Fix:* Treat deployment model as evolving; use operational data to refine.
- **Tier migration breaking tenants:** Pulling a tenant out of pooled storage and into siloed without zero-downtime planning. *Fix:* Plan tier migrations as a first-class operational workflow; consider whether the migration can be non-disruptive.
- **GenAI as a multi-tenant afterthought:** Sharing prompts/context across tenants without isolation. *Fix:* Per-tenant RAG indexes, per-tenant fine-tuning models, explicit partitioning.
- **Tier as pricing-only:** Treating tier as a billing concept without infrastructure implications. *Fix:* Tier influences routing, throttling, deployment model, concurrency.

---

## Decision Heuristics / Checklists

- **Is this SaaS?** Test: are all tenants onboarded, deployed, managed, and operated through a single pane of glass? If no, it's an MSP.
- **Where does this concern belong — control plane or application plane?**
  - Cross-cutting horizontal (onboarding, identity, billing, tenant management) → control plane.
  - Tenant-facing business logic → application plane.
- **Silo or pool for this service?**
  - Strict compliance (PCI, HIPAA)? → Silo.
  - Premium tier with strict performance? → Silo.
  - Performance-sensitive and high-consumption variance? → Silo.
  - Cost-efficient shared capability? → Pool.
- **What goes in the JWT?**
  - tenant_id (GUID), tier, role, sub (user id), standard OIDC claims, optionally tenant-specific custom claims.
- **What intercepts tenant context in this service?**
  - Aspect / middleware / sidecar / Lambda Layer / wrapper library. Choose one; standardize.
- **What's the per-tenant cost?** Always know — it informs pricing, tiering, and margin.
- **How do we migrate a tenant between tiers?**
  - Pooled → Pooled: update tenant configuration (feature flags, throttling).
  - Pooled → Siloed: provision new siloed resources; migrate data; switch routing; decommission old resources.
  - Siloed → Pooled: extract data into pooled storage; decommission siloed resources.
  - Always leverage onboarding code for tier upgrades that create new resources.
- **What's the noisy-neighbor risk?** Per-tier concurrency limits (Lambda), per-namespace resource quotas (Kubernetes), per-tenant request quotas (API Gateway).
- **What's the blast radius?** Pod model limits it for pooled environments.
- **GenAI: RAG pooled or siloed?** RAG data can be pooled with tenant ID partition or siloed. Siloed gives stronger isolation; pooled is more efficient.

---

## Key Takeaways

1. **SaaS is a business model, not a technology pattern.** Business and technical strategy must co-evolve from day one.
2. **Multi-tenancy is unified management, not shared infrastructure.** Pool or silo at fine granularity.
3. **Build the control plane first.** Onboarding, identity, tenant management — non-negotiable foundation.
4. **Tenant context in the JWT is the connective tissue.** It flows through every service, enabling logging, metrics, data access, routing, isolation.
5. **Isolation is separate from deployment.** Same DB or different DB doesn't matter — isolation must be explicitly enforced.
6. **Deployment models are composable and fine-grained.** Mix silo and pool at every level (per service, per tier, per resource).
7. **Hide multi-tenant complexity from developers.** Libraries, aspects, sidecars, middleware, Lambda Layers.
8. **Invest deeply in tenant-aware operations.** Five categories of metrics (tenant activity, agility, consumption, cost-per-tenant, business health).
9. **Tiering is a tool for both business and technical strategy.** Implements across API, compute, storage, deployment.
10. **Migrate with Silo Lift-and-Shift first, modernize from real data.** Build the control plane first.
11. **GenAI requires the same multi-tenant rigor.** Partition, isolate, tier, and meter per tenant.
12. **Guard SaaS principles zealously.** Every one-off exception, every compromise that moves toward MSP, erodes agility, efficiency, and scalability.

---

## Cross-References
- Related: [[../Cloud_Application_Architecture_Patterns.md]] (cloud-native fundamentals — application package, service API, stateless, replicable)
- Related: [[../Designing_Distributed_Systems.md]] (containers, sidecars, scaling)
- Related: [[../Engineering_Resilient_Systems_on_AWS.md]] (multi-region, reliability patterns)
- Related: [[../Building_Microservices.md]] (microservices decomposition; data-per-service)
- Related: [[../Observability_Engineering.md]] (tenant-aware observability)
- Related: [[../Continuous_API_Management.md]] (API tiering, gateways, consumption models)
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] (platform-as-product for SaaS providers)
- Topic index: [[../INDEX.md]]