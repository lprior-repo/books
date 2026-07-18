# Building Multi-Tenant SaaS Architectures
**Author:** Tod Golding (O'Reilly, 2024)
**Topic tags:** `#architecture` `#api` `#multi-tenancy` `#saas` `#cloud` `#platform`
**Language focus:** language-agnostic (AWS-leaning: Python/Boto3 examples, IAM policies, EKS/Kubernetes YAML, Lambda/SAM)
**Sources:** `markdown_output/Building Multi-Tenant SAAS Architectures/Building Multi-Tenant SAAS Architectures.md` · `summaries/Building_Multi-Tenant_SAAS_Architectures.md`

## TL;DR
SaaS is a **business model**, not a technology pattern: business and technology strategies must co-evolve from day one. Multi-tenancy is defined by **unified operations** (onboarding, deployment, management, operation through one pane of glass), not by infrastructure sharing — "single-tenant" is an obsolete label. The control plane (onboarding, identity, tenant management, metrics, billing) is **non-negotiable first-day work**. Tenant context (the JWT) is the connective tissue that flows through every service, driving logging, metrics, data access, routing, and isolation. Deployment models, isolation strategies, and data partitioning are **fine-grained and composable per service, per tier, per resource type** — there is no one-size-fits-all answer. Across every technology stack, the same principles reappear: noisy-neighbor defence, runtime vs deployment-time isolation, mixed-mode partitioning, tenant-aware observability, tier-based throttling, and the discipline of resisting one-off customization.

---

## Best Practices by Topic

### 1. SaaS Mindset — Business and Technology Co-evolve

**Principle:** Never design the multi-tenant architecture first and then bolt on business strategy; the two must evolve in lockstep from day one.

**Do:**
- Define the target market, tenant personas, growth expectations, and margins before any architectural decision.
- Treat SaaS as a business transformation that unlocks agility, operational efficiency, and cost efficiency — not just a hosting model.
- Pursue economies of scale, correlated consumption, and unified operations rather than per-customer customisation.
- Be all-in with SaaS; avoid per-customer exceptions that erode SaaS principles and slide back toward an MSP model.
- Adopt a service-centric mindset (restaurant analogy): food is the product; speed, greeting, freshness are the service.
- Ask the "1,000 new tenants tomorrow" question to validate the operational model end-to-end.

**Don't:**
- Treat SaaS as "we moved our app to the cloud" — that is IaaS, not SaaS.
- Allow "one-off customer exceptions" to creep into the model; every exception chips away at the operational and agility gains.
- Conflate SaaS with Managed Service Provider (MSP). MSPs inherit per-customer variations, run multiple versions, and cannot match SaaS agility.
- Neglect the B2B vs B2C distinction: dedicated infrastructure is viable in B2B but rarely in B2C.
- Build for a single tenant and "bolt on" multi-tenancy later — this rarely works.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 1: The SaaS Mindset" / "Where We Started" / "At Its Core, SaaS Is a Business Model" / "Defining SaaS"*

---

### 2. Redefine Multi-Tenancy Around Unified Operations

**Principle:** A system is multi-tenant when **all tenants are onboarded, deployed, managed, and operated through a single, unified experience** — regardless of whether infrastructure is shared.

**Do:**
- Use "multi-tenant" as a positive umbrella that accommodates pooled, siloed, and mixed-mode deployments.
- Decouple the term "multi-tenant" from "shared infrastructure"; sharing infrastructure is one optimisation, not the defining trait.
- Recognise that B2B SaaS providers typically serve hundreds-to-thousands of tenants (viable to offer dedicated infrastructure); B2C patterns differ.
- Drop the term "single-tenant" from the design vocabulary to avoid ambiguity.
- Hold the line on the wall: tenants see the surface, not the infrastructure — preserves agility.

**Don't:**
- Map "multi-tenant" strictly to "infrastructure shared by all tenants" — this misses legitimate siloed-by-design SaaS models.
- Treat MSP as SaaS: MSP supports multiple versions, custom environments, and per-customer operations; SaaS runs one version for all tenants.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Redefining Multi-Tenancy" / "Avoiding the 'Single-Tenant' Term" / "The Managed Service Provider Model"*

---

### 3. The SaaS Value Proposition — Agility, Operational Efficiency, Innovation, Growth

**Principle:** SaaS exists to deliver four business outcomes in concert: **agility, operational efficiency, innovation, and frictionless growth**. Compromising any one of them collapses the value.

**Do:**
- Pursue agility as "releasing new versions, reacting to market dynamics, targeting new segments, changing pricing models".
- Build operational efficiency as a forcing function: if 1,000 new tenants sign up tomorrow, your tooling, onboarding, and support must absorb them.
- Treat onboarding friction as a leak in your growth funnel — measure time-to-value and optimize for it.
- Use SaaS agility as fuel for innovation — frequent releases + customer feedback loops = differentiated market position.
- Anchor subscription / pay-as-you-go pricing to the elasticity of cloud.

**Don't:**
- Reduce SaaS to "software that bills monthly".
- Build an org where operations, engineering, and product live in silos; the SaaS mindset demands shared operational goals.

*Ref: Building Multi-Tenant SaaS Architectures.md — "At Its Core, SaaS Is a Business Model" / "Building a Service—Not a Product"*

---

### 4. The Control Plane Comes First — Always

**Principle:** Build onboarding, identity, tenant management, metrics, and billing **before** any application code. The control plane is the foundation; tenancy must be forced into the architecture from day one.

**Do:**
- Build the baseline environment first: VPCs, databases, identity providers, admin console.
- Create system admin identities that operate the SaaS environment through the admin console.
- Implement self-service onboarding AND internal onboarding paths.
- Track every onboarding step with state machines; surface state in the admin console.
- Make onboarding a first-class part of the service, not a side-quest.
- Carry the control plane from day one, even in a migration — it is non-negotiable.
- Separate the control plane from the application plane in deployment and operational terms even if they live in the same network.
- Automate the control plane's provisioning; it is the single pane of glass.

**Don't:**
- Build the application first and plan to "add the control plane later" — this never works.
- Allow the application plane to manage tenant state directly — go through the Tenant Management service.
- Skip the admin console — most teams under-invest in this and it cripples operations.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 2: Multi-Tenant Architecture Fundamentals" / "Inside the Control Plane" / "Onboarding" / "Identity" / "Tenant Management"*

---

### 5. The Two Halves: Control Plane vs Application Plane

**Principle:** Every SaaS architecture splits cleanly into **control plane** (cross-cutting services that span all tenants — non-multitenant themselves) and **application plane** (the actual product features — fully tenancy-aware). Confusing the two is a leading architectural mistake.

**Do:**
- Treat the control plane as the single pane of glass for operators; it is the home of tenant state, identity configuration, billing, metrics, and the admin console.
- Keep control plane services from being multi-tenant — they serve the SaaS provider, not individual tenants.
- Force tenants into the application plane via tenant context; never mix application and tenant-state code in a control plane service.
- Provision pooled resources during baseline creation; provision siloed/per-tenant resources during onboarding.
- Choose technologies for each plane independently — serverless control plane + container application plane is legitimate.
- Pick loose-coupling vs native integration between planes based on the nature of your interactions.

**Don't:**
- Bake per-tenant state into control plane services; control plane services are the platform, not the product.
- Couple the planes' lifecycle; the control plane evolves on its own cadence.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Two Halves of Every SaaS Architecture" / "Inside the Control Plane" / "Inside the Application Plane"*

---

### 6. Tenant Context is the Connective Tissue

**Principle:** **Tenant context** (usually a JWT carrying tenant ID, tier, role, and user identity) is the universal currency that flows through every service. It must originate at the IdP and never require a downstream lookup.

**Do:**
- Embed tenant attributes as **custom claims** in JWTs at the IdP — not as something each service has to resolve.
- Issue tokens at the front door; pass them as bearer tokens downstream.
- Cascade tenant context across service-to-service invocations in HTTP, gRPC, or wherever APIs go.
- Touch every important concern with tenant context: logging, metrics, data access, billing, tiering, isolation, routing.
- Treat every code path that "doesn't yet have tenant context" as a bug to fix.

**Don't:**
- Build a centralized Tenant Mapping service every request must call — this becomes a hotspot, a single point of failure, and an anti-pattern.
- Bloat the JWT with application-level RBAC attributes; keep tokens about tenant identity, not feature flags.
- Re-derive tenant context from session state when the JWT already has it.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Inside the Application Plane" — "Tenant Context" / "Chapter 4: Attaching a Tenant Identity" / "No Centralized Services for Resolving Tenant Context"*

---

### 7. Onboarding — The Front-Door of the SaaS Experience

**Principle:** Onboarding is the first impression, it gates time-to-value, and it should be **fully automated, repeatable, and observable** from day one.

**Do:**
- Treat onboarding as part of the service, not a script.
- Surface every onboarding step (`TENANT_CREATED`, `TENANT_PROVISIONED`, `BILLING_INITIALIALIZED`, `USER_CREATED`, `TENANT_ACTIVATED`) in the admin console.
- Wrap onboarding orchestration in a single Onboarding service that owns the full lifecycle and tolerates async/third-party failures with retries.
- Trigger onboarding either via self-service sign-up OR via the admin console (or both).
- Decouple per-tenant provisioning into its own Provisioning service so it can run during onboarding.
- Pre-provision pooled resources during baseline creation; do not lazy-load them.
- Test the onboarding experience aggressively: load tests for burst onboarding, failure recovery tests, tier-path tests, performance tests.
- Push provisioning failures to a synchronous retry queue with exponential backoff; isolate flaky third-party integrations (e.g., billing) so onboarding does not block on them.

**Don't:**
- Treat onboarding as a "set up later" task.
- Couple the tenant's active status flip with every downstream step — keep state tracking clean.
- Run onboarding synchronously through one flaw-prone third party (e.g., billing).

*Ref: Building Multi-Tenant SaaS Architectures.md — "Onboarding" / "The Onboarding Experience" / "Handling Onboarding Failures" / "Testing Your Onboarding Experience"*

---

### 8. Tier-Based Onboarding — Mixed-Mode Provisioning

**Principle:** A single onboarding service must support different provisioning footprints per tier — pooled for basic, siloed for premium, hybrid for advanced. The Onboarding service reads tenant tier and calls a tier-aware Provisioning service.

**Do:**
- Encode tier information into the provisioning payload.
- Pre-provision pooled microservices at baseline; only provision dedicated resources per premium tenant at onboarding time.
- Wire tier-based policies (storage IOPS, throughput, retention) into the same onboarding flow.
- For mixed-mode, silo *what earns its way out*: default to pooled, force siloed to earn its keep.
- Track onboarded resources in a structured table so CI/CD pipelines and the deployment system can find them.
- Treat every tier as still-same-version — siloed tiers still run the same code path.

**Don't:**
- Couple tier provisioning to one-off customization rules.
- Interpret tier-based onboarding as permission to add per-tenant customization.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tier-Based Onboarding" / "Tracking Onboarded Resources"*

---

### 9. SaaS Identity — Bind User to Tenant via Custom Claims

**Principle:** A SaaS identity is the logical union of **user** + **tenant**. Embed this binding in JWT custom claims at issuance so every downstream service inherits the binding without any lookup.

**Do:**
- Configure your identity provider with custom attributes (`tenantId`, `tenantTier`, `role`, etc.) per tenant.
- Populate those claims during tenant creation AND during subsequent user additions.
- Use Cognito User Pools or equivalent constructs to organize tenants at the IdP layer.
- Apply per-tenant identity configurations (MFA, password policy) where supported.
- Use OAuth/OIDC standards — let the IdP handle token issuance, refresh, and revocation.
- For federated/external IdPs, use Cognito (or equivalent) to **enrich** incoming tokens with your custom claims — your SaaS identity remains stable across IdP boundaries.

**Don't:**
- Keep the IdP ignorant of tenancy and expect services to reconstruct tenant context.
- Bloat custom claims with feature flags or app-level access control; tokens should evolve slowly.
- Use email-as-tenant without a robust mapping table that leaks which tenants a user belongs to.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 4: Onboarding and Identity" / "Creating a SaaS Identity" / "Attaching a Tenant Identity" / "Using Custom Claims Judiciously" / "Federated SaaS Identity" / "Tenant Grouping/Mapping Constructs"*

---

### 10. JWT Bearer-Token Auth Flow in Code

**Principle:** Authenticate, extract tenant context at the front door, and **thread the JWT as a bearer token** through every downstream call. Code that ignores tenant context is a defect.

**Code (Python / Boto3 verbatim from book):**

```python
def query_orders(self, status):
    # get tenant context
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")
    if (token[0] != "Bearer"):
        raise Exception('No bearer token in request')
    bearer_token = token[1]
    decoded_jwt = jwt.decode(bearer_token, "secret",
    algorithms=["HS256"])
    tenant_id = decoded_jwt['tenantId']
    tenant_tier = decoded_jwt['tenantTier']
    # query for orders with a specific status
    logger.info("Tenant: %s, Tier: %s, Find orders with status %s",
    tenant_id, tenant_tier, status);
    ...
```

```http
GET /api/orders HTTP/1.1
Authorization: Bearer <JWT>
```

**Do:**
- Standardize JWT decoding into a shared helper (e.g., `get_tenant_context(request)`).
- Inject tenant context into every log line; never emit tenant activity without it.
- Cascade the JWT to downstream service calls via HTTP headers or equivalents.
- Push JWT decoding to an API Gateway if you want to keep the decode cost out of every service.

**Don't:**
- Re-decode the JWT multiple times in the same request path.
- Couple `query_orders` directly to a specific tenant's database without first verifying isolation scope.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Inside Multi-Tenant Services" — "Extracting Tenant Context" / "Logging and Metrics with Tenant Context"*

---

### 11. Tenant-Aware Logging and Metrics (do/don't)

**Principle:** Every log line and every metric event from a multi-tenant service must carry `tenantId` and `tenantTier` as first-class fields. Without these, you cannot reason about tenant activity.

**Code (publishing per-tenant metrics via Kinesis Data Firehose):**

```python
def query_orders(self, status):
    # get tenant context
    ...
    tenant_id = decoded_jwt['tenantId']
    tenant_tier = decoded_jwt['tenantTier']
    # query for orders with a specific status
    logger.info("Tenant: %s, Role: %s, Finding orders with status: %s",
    tenant_id, tenant_role, status);
    try:
        start_time = time.time()
        response = ddb.query(
            TableName = "order_table",
            KeyConditionExpression = Key(status).eq(status))
        duration = (time.time() - start_time)
        message = {
            "tenantId": tenant_id,
            "tier": tenant_tier,
            "service": "order",
            "operation": "query_orders",
            "duration": duration
        }
        firehose = boto3.client('firehose')
        firehose.put_record(
            DeliveryStreamName = "saas_metrics",
            Record = message
        )
    except ClientError as err:
        logger.error(
            "Tenant: %s, Find order error, status: %s. Info: %s: %s",
            tenant_id, status,
            err.response['Error']['Code'],
            err.response['Error']['Message'])
        raise
    else:
        return response['Items']
```

**Do:**
- Pick metric schemas deliberately — `{tenantId, tier, service, operation, duration}` is a strong baseline.
- Push metrics through a streaming pipeline (Firehose/Kinesis) so they reach the analytics layer reliably.
- Add timing instrumentation around every storage/network operation worth measuring.
- Capture failures with tenant context so on-call can route issues to the right tenant dialogue.

**Don't:**
- Allow bare, tenant-less log lines in any multi-tenant service.
- Emit metrics for the sake of metrics — choose dimensions that map to actionable questions.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Logging and Metrics with Tenant Context"*

---

### 12. Per-Tenant Data Access Patterns

**Principle:** In pooled storage, every query must include `tenantId` as a key; in siloed storage, every query must resolve to the tenant's table/index/bucket. Either way, isolate by code AND by infrastructure, not code alone.

**Code (pooled query with TenantId partition key):**

```python
response = ddb.query(
    TableName = "order_table",
    KeyConditionExpression = Key('TenantId').eq(tenant_id),
    FilterExpression=Attr('status').eq(status))
```

**Code (tier-based table resolution — basic pooled, premium siloed):**

```python
response = ddb.query(
    TableName = getTenantOrderTable(tenant_id, tenant_tier),
    KeyConditionExpression = Key('TenantId').eq(tenant_id),
    FilterExpression=Attr('status').eq(status))
# helper function to get generate tier-based table name
def getTenantOrderTableName(tenant_id, tenant_tier):
    if tenant_tier == BASIC_TIER:
        table_name = "pooled_order_table"
    elif tenant_tier == PREMIUM_TIER:
        table_name = "order_table_" + tenantId
    return table_name
```

**Do:**
- Hide tier-aware table resolution behind a DAL.
- Use `TenantId` as the partition key (primary) for pooled DynamoDB tables; let `status` become a filter.
- Treat runtime isolation as a separate layer from data partitioning — both are needed.

**Don't:**
- Let tenant-aware access logic leak into business logic.
- Treat filtering by `tenantId` as sufficient isolation — code may have bugs; enforcement must be policy-based at the storage layer too.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Accessing Data with Tenant Context" / "Supporting Tenant Isolation"*

---

### 13. Tenant Isolation via STS AssumeRole (Runtime, In-Service)

**Principle:** Acquire **tenant-scoped credentials** per request by assuming a parameterized IAM role populated with the current `tenantId`. The scoped session encrypts the contract — even buggy code cannot cross the tenant boundary.

**Code (STS-driven scoped session):**

```python
def query_orders(self, status):
    # get database client (DynamoDB) with tenant scoped credentials
    sts = boto3.client('sts')
    # get credentials based on tenant scope policy
    tenant_credentials = sts.assume_role(
        RoleArn = os.environ.get('IDENTITY_ROLE'),
        RoleSessionName = tenant_id,
        Policy = scoped_policy,
        DurationSeconds = 1000
    )

    # get a scoped session using assumed role credentials
    tenant_scoped_session = boto3.Session(
        aws_access_key_id =
        tenant_credentials['Credentials']['AccessKeyId'],
        aws_secret_access_key =
        tenant_credentials['Credentials']['SecretAccessKey'],
        aws_session_token =
        tenant_credentials['Credentials']['SessionToken']
    )
    # get database client with tenant scoped credentials
    ddb = tenant_scoped_session.client('dynamodb')
    ...
```

**Do:**
- Use policy templates (one parameterized policy) rather than one policy per tenant — avoids IAM service limits.
- Cache scoped credentials with TTL to reduce `assume_role` overhead.
- Wire scope acquisition into a shared library / interception mechanism so developers do not own isolation by hand.

**Don't:**
- Default to scope-everything-static — runtime scoping is required when compute is shared.
- Trust code review alone; enforce isolation at the infrastructure layer.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Supporting Tenant Isolation"*

---

### 14. Hide Multi-Tenant Complexity From Builders

**Principle:** Multi-tenant plumbing (token decode, scoped credentials, tenant-aware logging) belongs in **shared libraries / helpers / aspects / sidecars / middlewares / Lambda Layers**, not in business logic.

**Code (centralized tenant context extraction):**

```python
def get_tenant_context(request):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")
    if (token[0] != "Bearer"):
        raise Exception('No bearer token in request')
    bearer_token = token[1]
    decoded_jwt = jwt.decode(bearer_token, "secret",
    algorithms=["HS256"])
    tenant_context = {
        "TenantId": decoded_jwt['tenantId'],
        "Tier": decoded_jwt['tenantTier']
    }
    return tenant_context
```

**Code (streamlined business-facing service):**

```python
def query_orders(request, status):
    # get tenant context from request
    tenant_context = get_tenant_context(request)
    # get scoped database client
    ddb = get_scoped_client(tenant_context, policy)
    # query for orders with a specific status
    log_helper.info(request, "Find order with the status of %s", status)
    try:
        response = get_orders(ddb, tenant_context, status)
    except ClientError as err:
        log_helper.error(
            request,
            "Find order error, status: %s. Info: %s: %s",
            status,
            err.response['Error']['Code'],
            err.response['Error']['Message'])
        raise
    else:
        return response['Items']
```

**Do:**
- Move tenant extraction, logging wrappers, scoped client factories, and DALs into shared modules.
- Prefer interception mechanisms (aspects, middleware, Lambda Layers, sidecars) over inline code.
- Use a Lambda Layer to share multi-tenant helpers across functions and version them independently.

**Don't:**
- Force every service to copy-paste JWT decoding logic.
- Treat tenant context as a per-service concern.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Hiding Away and Centralizing Multi-Tenant Details" / "Interception Tools and Strategies" — "Aspects" / "Sidecars" / "Middleware" / "AWS Lambda Layers/Extensions"*

---

### 15. Tenant Management Service — The Single Source of Truth

**Principle:** Every tenant has exactly one authoritative state record. The Tenant Management service owns tenant attributes, identity configuration, routing policy, infrastructure configuration, secrets, and user associations.

**Do:**
- Store: tenantId (GUID), status, tier, name, onboarding state, lastActive, billing plan, identity settings, MFA policy, identity provider mapping, routing data, infrastructure pointers (e.g., siloed table names), secrets.
- Use **GUID tenant identifiers** that are immutable, opaque, and never derived from names.
- Keep tenant identifiers separate from friendly names / subdomains / vanity domains — renaming is a property of the latter.
- Expose CRUD for tenant configuration and lifecycle-management operations (activate, deactivate, decommission, tier-change).
- Surface all of this through the admin console with deep-links to the underlying tenant resources.
- Maintain a `LastUpdated` audit field so admins have visibility into tenant activity.

**Don't:**
- Allow tenant state to be cached in multiple places — make Tenant Management the only source.
- Embed business logic in the Tenant Management service; it should be a CRUD + lifecycle orchestrator.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 5: Tenant Management" / "Generating a Tenant Identifier" / "Storing Infrastructure Configuration"*

---

### 16. Tenant Lifecycle — Activation, Deactivation, Decommissioning, Tier-Change

**Principle:** Every tenant walks through a lifecycle. Each transition must be visible, automated, and reversible (where possible).

**Do:**
- **Activation/Deactivation:** Toggle a `status` flag, propagate to identity provider so users cannot authenticate. Triggered by Tenant Management or externally by Billing (delinquency).
- **Decommissioning:** Carve out a **Decommissioning service** as a first-class orchestrator. Iterate over all tenant resources (silos, queues, configs, users, data) and remove them. Run as a low-impact batch, after-hours when possible, asynchronously to avoid impacting live tenants.
- For pooled data, **selectively remove** by `TenantId` partition key across all pooled tables and indexes.
- Archive the tenant record (or at least the user and config data) for cheap rehydration; weight this against cost/complexity.
- **Tier changes:** Simple tier flips (basic → premium in pooled mode) are just feature-flag + throttle updates. Cross-deployment-model migrations (pooled → silo) require provisioning new resources, migrating data, and waving traffic over — reuse onboarding code where possible.
- Treat tier-change events as full lifecycle operations that may disrupt live workloads.

**Don't:**
- Couple deactivation with hard delete (deactivation is reversible; decommissioning is not).
- Run decommissioning inline during peak traffic.
- Skip archiving — rehydrating a tenant should not require rebuilding from scratch.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Activating and Deactivating a Tenant" / "Decommissioning a Tenant" / "Changing Tenant Tiers"*

---

### 17. Front-Door Access — Domain vs Token Resolution

**Principle:** Choose between **tenant-specific domains** (subdomain/vanity) and **single shared domain** based on identity and tiering model. Whatever you pick drives routing, identity, and tenant-mapping complexity.

**Do:**
- Use **subdomain-per-tenant** (`tenant1.saasprovider.com`) when you want frictionless tenant branding without managing full DNS per tenant — configure CDN (CloudFront) and DNS (Route 53) during onboarding.
- Use **vanity domain-per-tenant** when tenants want to white-label their own branded experience.
- Use **single shared domain** when tenants are resolved from JWTs and the IdP can host all of them (B2C).
- Wire a `tenant_mapping` step (CDN, DNS, API Gateway lookup) when the domain must be resolved to a tenant.
- Use subdomains to extract tenant context via HTTP request `Host` — clean, no centralized lookup.

**Don't:**
- Mix subdomain routing with a single-identity-provider without an additional tenant-to-group mapping (the "Man in the Middle" challenge).
- Allow the client to be expected to know the tenant mapping — push it server-side.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 6" — "Entering the Front Door" / "Access via a Tenant Domain" / "Subdomain-per-Tenant" / "Vanity Domain-per-Tenant" / "Access via a Single Domain" / "Onboarding with Tenant Domains"*

---

### 18. Tenant Authentication Flow

**Principle:** Standard OIDC flow: web → IdP redirect → credentials → JWT → downstream. SaaS-specific: extract tenant context from the JWT and pass it everywhere.

**Do:**
- Have the IdP return the JWT enriched with tenant custom claims.
- Inject JWT as `Authorization: Bearer <JWT>` for all downstream calls.
- Use Tenant Management as the single place that maps a tenant to its specific IdP construct (User Pool, group, etc.).
- Set up your authentication manager/orchestrator when tenants use external IdPs so it can enrich the returned tokens with the missing tenant context.
- Plan for the "man in the middle" — adding a mapping layer to authentication introduces a single point of failure; harden it.

**Don't:**
- Redirect directly to a tenant-specific IdP construct without a way to discover which construct to use, unless the subdomain already encodes it.
- Embed tenant resolution into web app business logic when it can be done at the gateway or auth proxy.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Multi-Tenant Authentication Flow" / "A Sample Authentication Flow" / "Federated Authentication" / "The Man in the Middle Challenge"*

---

### 19. Tenant Routing — Stack the Layers You Need

**Principle:** Routing in a multi-tenant environment has **two levels**: top-level (tenant → siloed stack vs shared) and intra-stack (tenant → siloed microservice within a shared service pool). Design for both.

**Do:**
- Plan for a top-level router that extracts tenant context from the request and routes to the correct stack.
- Plan for intra-stack routers in shared namespaces that route to tenant-specific microservice instances.
- Use subdomains to drive both layers naturally via HTTP `Host`.
- For serverless, an **API Gateway-per-tenant** model for premium tiers keeps policy/isolation scope clean.
- For Kubernetes, use Ingress controllers + namespaces + service mesh (Istio) to express tenant-aware routing.
- Cache the tenant → gateway URL mapping at the gateway to absorb per-request latency.

**Don't:**
- Build a per-request DB lookup chain just to resolve a tenant's resources.
- Couple the gateway to specific microservice tiers — make it a generic dispatcher.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Serverless Tenant Routing" / "Container Tenant Routing" / "Routing with Different Technology Stacks"*

---

### 20. Deployment Models — Silo, Pool, Hybrid, Mixed Mode, Pod

**Principle:** Deployment models are **fine-grained and composable** — pick per service, per tier, per resource type. There is no one-size-fits-all.

**Do:**
- **Full stack silo** — when compliance, customer demand, or migration simplicity demand full tenant isolation. Higher cost; account-per-tenant or VPC-per-tenant.
- **Full stack pool** — when scale and efficiency dominate. Aligns resource consumption with tenant activity; demands stronger isolation, metering, and noisy-neighbor controls.
- **Hybrid full stack** — basic tier pool + premium tier silo. Same-control-plane, two-footprint system.
- **Mixed mode** — service-by-service / resource-by-resource siloed vs pooled. Use when one service's noise issues can be solved by isolating just that service.
- **Pod** — group tenants into self-contained units for blast-radius control, scaling across cloud accounts, or geography. Do NOT conflate with Kubernetes `pod` constructs.
- Treat these as parameters in your codebase, not as decision points you make forever.

**Don't:**
- Conflate "multi-tenant" with "full stack pool" — other models are legitimate.
- Default to siloed for everything; it kills economies of scale.
- Build a pod model that drifts into one-off customization per pod.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 3: Multi-Tenant Deployment Models" / "Full Stack Silo" / "Full Stack Pool" / "Hybrid Full Stack" / "Mixed Mode Deployment Model" / "The Pod Deployment Model"*

---

### 21. Account-Per-Tenant vs VPC-Per-Tenant Full Stack Silo

**Principle:** Two primary silo constructs on AWS. Each has scale ceilings and operational cost.

**Do:**
- **Account-per-tenant** — strongest boundary, simplest isolation, easiest cost attribution, but account limits and operational sprawl make it awkward above tens of tenants.
- **VPC-per-tenant** — within one account; gives strong network segmentation with multiple AZs + subnets + Auto Scaling groups. Limited by VPC count.
- Pre-allocate the maximum account/VPC count you'll need and raise limits during onboarding automation.
- Use SAML subdomain routing to attach tenants to their silo.

**Don't:**
- Pick account-per-tenant without quantifying the operational cost at your target scale.
- Treat either silo as "free" — both carry a baseline cost per tenant.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The account-per-tenant model" / "The VPC-per-tenant model"*

---

### 22. Noisy Neighbor Defense — Decompose the Service

**Principle:** In a pool, **one bad tenant can starve all the others**. Decompose services so that bottlenecks become independently scalable, instead of dragging the whole service down.

**Do:**
- Look for high-latency, resource-heavy operations in your services (e.g., `uploadThumbnail`) and consider extracting them into a dedicated service.
- Apply granular decomposition: split a Catalog service into Product + Thumbnail; split Order into Order + Tax; allocate metrics per operation.
- Overprovisioning is acceptable as a buffer, but prefer decomposition to avoid waste.
- Continuously monitor per-tenant load; refine the decomposition as patterns emerge.

**Don't:**
- Scale the entire service to handle one operation's spike — it overprovisions the whole blast radius.
- Ignore noisy-neighbor candidates until production tells you it was a problem.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Addressing Noisy Neighbor" / "One Theme, Many Lenses"*

---

### 23. Compute Stack Influences Service Decomposition

**Principle:** The compute model (serverless, container) materially affects service boundaries. Serverless makes operation-level granularity free; containers bias toward service-level granularity.

**Do:**
- With serverless (Lambda), treat each operation as an independent function — `createOrder()` scales on its own without you having to reason about container-level scaling.
- With containers, use classic decomposition (services). Plan for container-level scaling.
- Let real-world noisy-neighbor data drive deeper decomposition over time.

**Don't:**
- Assume your day-one decomposition is final — evolve it as metrics emerge.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Influence of Compute Technologies"*

---

### 24. Storage Considerations in Service Design

**Principle:** Data volume, tenant concurrency on a shared store, and storage-tier SLAs all shape service granularity. A noisy database produces noisy-neighbor symptoms you can't fix in compute alone.

**Do:**
- Storage compute is typically fixed — rightsizing is hard. Use serverless storage (Aurora Serverless, DynamoDB on-demand) to align consumption with tenant activity in pools.
- Decompose services along noisy storage boundaries.
- Pick coarse-grained services when the data profile is uniform; pick fine-grained when storage profiles diverge per service.

**Don't:**
- Underestimate the noisy-neighbor impact of pooled relational stores with a single compute profile.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Influence of Storage Considerations"*

---

### 25. Data Partitioning Fundamentals — Pick Per Service, Per Resource

**Principle:** Pick **silo** vs **pool** per resource based on workload, compliance, isolation needs, blast-radius goals, and operational footprint. The book makes clear: these are fine-grained decisions.

**Do:**
- For pooled: introduce `TenantId` as the partition key (primary), demote the natural key to a sort key / filter.
- For siloed: name each resource with a tenant-scoped naming convention (`Order-TENANT_NAME`, `saasco-tenant1-...`).
- Default to pooled; force siloed to earn its way out.
- Respect schema-isolation tradeoffs (relational migrations are expensive; NoSQL migrations are cheap).
- Think through backup/restore implications — pooled data needs selective extraction.

**Don't:**
- Pick "one model fits all storage" without inspection.
- Right-size pooled storage compute naively (you'll overprovision).
- Forget about compliance — some data must be siloed.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 8: Data Partitioning" — "Data Partitioning Fundamentals" / "The Right Tool for the Job" / "Defaulting to a Pooled Model" / "Supporting Multiple Environments"*

---

### 26. Throughput / Throttling / Rightsizing for Pooled Storage

**Principle:** Pooled storage compute is fixed and rarely matches tenant-spike demand exactly. Accept some overprovisioning, but tune throttling/throughput policies to align with tier expectations.

**Do:**
- Configure tier-appropriate IOPS, throughput, and capacity.
- Use throughput configuration knobs your storage exposes (e.g., DynamoDB capacity mode).
- Lean on serverless storage (Aurora Serverless, DynamoDB on-demand) where alignment matters most.
- Continuously profile storage consumption to size policies.

**Don't:**
- Assume rightsizing is precise. Some overprovisioning is inevitable.
- Leave storage at default capacity mode for pooled multi-tenant traffic.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Rightsizing Challenge" / "Throughput and Throttling" / "Serverless Storage"*

---

### 27. Relational Data Partitioning

**Principle:** Relational stores give you three silo granularities: **database instance per tenant**, **database per tenant within an instance**, or **table per tenant within a database**. Each implies a scale ceiling and operational cost.

**Do:**
- Use **pooled relational** (single table with `TenantId` column) for low-noise/balanced workloads; the migration cost is low and access is uniform.
- Use **database-per-tenant** when isolation and lifecycle independence matter.
- Map tenant requests to the appropriate granularity via your DAL — never via inline code in business logic.
- Validate your choice against engine limits (max tables per schema, max connections, etc.) at your target tenant count.

**Don't:**
- Assume "all-or-nothing" between instance vs schema vs table — pick per workload.
- Pick the siloed approach without checking whether your engine's isolation primitives are sufficient.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Relational Database Partitioning" / "Pooled Relational Data Partitioning" / "Siloed Relational Data Partitioning"*

---

### 28. NoSQL Data Partitioning (DynamoDB-centric)

**Principle:** NoSQL stores (`DynamoDB`) favor pooled partitioning because of their schemaless, partition-key design. Siloed = table-per-tenant. Schema-evolution cost is low in either case.

**Do:**
- Use `TenantId` as partition key for pooled DynamoDB.
- Promote natural-key attributes (e.g., `EmployeeId`) to sort keys when adding tenancy.
- Use **on-demand capacity** for pooled tables; reserved capacity for predictable workloads.
- For siloed, name tables uniquely (`product_catalog_<tenantId>`), pay attention to per-account table limits.

**Don't:**
- Use schemaless stores without considering how your access patterns shift after introducing `TenantId`.
- Assume DynamoDB table-per-tenant scales for free — every account has limits.

*Ref: Building Multi-Tenant SaaS Architectures.md — "NoSQL Data Partitioning" / "Pooled NoSQL Data Partitioning" / "Siloed NoSQL Data Partitioning" / "NoSQL Tuning Options"*

---

### 29. Object Storage (S3) Data Partitioning

**Principle:** S3 partitioning uses bucket prefix-key boundaries. Pooled = shared bucket with tenant-prefixed keys; siloed = bucket-per-tenant or dedicated prefix-keys per tenant.

**Do:**
- Use **pooled buckets with prefix keys** (`<service>/<tenantId>/<object-name>`) for most deployments — easy management, IAM policy at prefix level.
- Use **bucket-per-tenant** for compliance-sensitive tenancies (cap at 1,000 buckets/account).
- Use **prefix-key silo** (`<service>/<tenantId>/...`) when you want isolation without bucket proliferation.
- Add a metadata-database layer for richer queries (e.g., S3-as-blob with relational metadata).

**Don't:**
- Bucket-per-tenant without first confirming scale (1,000-bucket limit).
- Mix object naming conventions across services — pick one strategy per service.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Object Data Partitioning" / "Pooled Object Data Partitioning" / "Siloed Object Data Partitioning" / "Database Managed Access"*

---

### 30. OpenSearch / Search Data Partitioning

**Principle:** Search and analytics stores have distinct partitioning constructs: **domain** (cluster), **index**, and shard distribution. Pick pooled indexes with `TenantId` field, separate indexes per tenant, or mixed-mode.

**Do:**
- **Pooled index with TenantId** in every document — works well at small scale, simple operations.
- **Index-per-tenant in shared domain** — isolation without cluster proliferation; watch shard imbalance if some tenants are huge.
- **Domain-per-tenant** — strictest isolation; expensive and operationally heavy.
- Use **OpenSearch Serverless** for simpler sizing.

**Don't:**
- Skip shard-distribution analysis. Tenant data imbalances can wreck performance.
- Pick domain-per-tenant without sizing the operational cost.

*Ref: Building Multi-Tenant SaaS Architectures.md — "OpenSearch Data Partitioning" / "Pooled OpenSearch Data Partitioning" / "Siloed OpenSearch Data Partitioning" / "A Mixed Mode Partitioning Model"*

---

### 31. Sharding Tenant Data When Pool Is Too Big

**Principle:** When a single pooled store can't carry all tenants, **shard tenants into multiple pool clusters**. This is a heavy-handed last resort, but legitimate when scale exceeds a single DB's throughput.

**Do:**
- Distribute groups of tenants across separate pool shards (e.g., `pool-A`, `pool-B`).
- Use a custom partition lookup (DAL) to map a tenant to its shard.
- Use this as a remediation tool when pods/pools can't grow further.

**Don't:**
- Treat sharding as a default — it's a stop-gap for scale.
- Forget that sharding adds operational and migration complexity.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Sharding Tenant Data"*

---

### 32. Multi-Tenant Data Lifecycle

**Principle:** Tier changes, decommissioning, and backup/restore are **tenant-data lifecycle operations** that require an architecture that knows where each tenant's data lives.

**Do:**
- Build tooling that handles tier migration including pooled ↔ siloed data movement.
- Choose decommissioning policy: delete everything, or archive + minimal record.
- For backup/restore, design selective extraction (pooled) or instance-scoped backup (siloed) — both have cost.
- Run decommissioning as conservative, off-peak batch jobs.

**Don't:**
- Defer lifecycle decisions; you will face them in the first twelve months of operation.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Data Lifecycle Considerations"*

---

### 33. Multi-Tenant Data Security

**Principle:** Encryption is non-negotiable. Per-tenant keys add isolation but also require key-lifecycle management.

**Do:**
- Encrypt at rest and in transit using managed-service features (S3 SSE, DynamoDB encryption, RDS encryption).
- For tenants who demand key ownership, offer Bring-Your-Own-Key (BYOK) per tenant — implies siloed storage.
- Lifecycle the per-tenant keys along with tenant lifecycle.

**Don't:**
- Assume managed encryption is sufficient when compliance demands per-tenant keys.
- Forget the operational complexity of per-tenant key management.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Multi-Tenant Data Security"*

---

### 34. Tenant Isolation — Deployment-Time vs Runtime

**Principle:** Isolation should be **explicitly enforced** at runtime, regardless of deployment model. Two complementary strategies: bake isolation into the deployed infrastructure (deployment-time) or acquire scoped credentials per request (runtime).

**Do:**
- For siloed compute: **bake the policy into the compute** (IAM role attached to the instance/pod). Compliance does not depend on developer code.
- For pooled compute: **acquire scoped credentials per request** (STS `assume_role` with parameterized policy). The developer's code can't accidentally cross a tenant boundary.
- Cache scoped credentials with TTL to reduce assume-role overhead.
- Use **policy templates** (one parameterized policy) to dodge IAM service limits.
- Combine both: siloed compute gets deployment-time policies; pooled compute gets runtime + deployment-time for outer surfaces (like API Gateway).

**Don't:**
- Rely on developer code discipline alone — it WILL break.
- Generate a unique IAM policy per tenant when a parameterized template works.
- Run STS assume-role on the synchronous hot path without caching.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 9: Tenant Isolation" — "Deployment-Time Versus Runtime Isolation" / "Scaling Considerations"*

---

### 35. Isolation Categories — Full Stack / Resource-Level / Item-Level

**Principle:** Pick the isolation depth that matches your deployment model and risk profile.

**Do:**
- **Full stack isolation** (account-per-tenant, VPC-per-tenant) — easiest, most expensive.
- **Resource-level isolation** (database/queue per tenant, shared compute) — common B2B pattern; runtime isolation strategy needed.
- **Item-level isolation** (pooled table, items keyed by tenant) — cheapest, hardest; requires runtime + IAM `dynamodb:LeadingKeys`-style mechanisms or ABAC/OPA.

**Don't:**
- Equate "siloed deployment" with "isolated" — they're different concerns.
- Use siloed storage as your only isolation strategy in pooled compute — it leaves the application code free to cross boundaries.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Categorizing Isolation Models" / "Real-World Examples"*

---

### 36. Application-Enforced Isolation When Tools Don't Suffice

**Principle:** When the storage platform's IAM/RBAC can't enforce item-level isolation, **build the enforcement layer in code** using ABAC, OPA, or framework-level authorization.

**Do:**
- Use Open Policy Agent (OPA), Casbin, or framework RBAC where built-in IAM lacks granularity.
- Compose decisions based on tenant context, role, resource attributes.
- Test the enforcement layer with explicit cross-tenant attempts (replace `tenantId` mid-flight and expect denial).

**Don't:**
- Skip building an enforcement layer when the platform can't reach item-level granularity.
- Trust code review to catch isolation bugs.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Application-Enforced Isolation" / "RBAC, Authorization, and Isolation"*

---

### 37. Isolation Through Interception

**Principle:** Move isolation out of business logic by **interception**: aspects, middleware, sidecars, proxy services. Developers stop owning isolation by hand.

**Do:**
- Pick the interception mechanism that matches your stack: aspects (AOP), middleware (Express), sidecars (Istio in K8s), API Gateway preprocessing (Lambda authorizer).
- Where possible, run interception outside the service process (gateways, sidecars) to remove any temptation for developers to bypass.
- Cache scoped credentials at the interception layer.

**Don't:**
- Couple interception too tightly to one service's implementation.
- Let interception break the natural shape of tracing, logging, and metrics.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Isolation Through Interception" / "Real-World Examples" / "Aspects" / "Sidecars" / "Middleware" / "AWS Lambda Layers/Extensions"*

---

### 38. Caching Isolated Credentials

**Principle:** Per-request `assume_role()` adds latency. Cache the scoped credentials per tenant with a TTL to balance security and performance.

**Do:**
- Cache in-process (no extra service hop) with TTL.
- Tie TTL to your security profile (short for sensitive ops, longer for safe ops).
- Re-cache automatically when expired.

**Don't:**
- Build a separate credential-caching microservice — adds network hop and defeats the purpose.
- Cache forever — leaks across tenant lifecycle.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Scaling Considerations"*

---

### 39. Isolation Policy Lifecycle — Ownership and Versioning

**Principle:** Decide whether isolation policies live with each microservice (preferred — boundary-aligned) or in a centralized policy store.

**Do:**
- Per-service ownership: policies are reviewed with the service code, versioned with the service.
- Centralized policies work but break the mental model.
- Validate isolation at deployment with tests that simulate cross-tenant access.

**Don't:**
- Stale policies — isolate with chaos engineering and explicit cross-tenant simulation tests.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Managing Isolation Policies"*

---

### 40. EKS / Kubernetes SaaS Patterns

**Principle:** Kubernetes provides natural multi-tenant primitives — **namespaces** for logical isolation, **resource quotas** for tiering, **ingress controllers** for routing, **RBAC** for access. Use them, but plan for noisy neighbors.

**Do:**
- **Pooled deployment** — single namespace, shared pods; horizontal scaling handles load.
- **Namespace-per-tenant (siloed)** — each tenant gets its own namespace; pods/processes scoped to that namespace.
- **Node-per-tenant** — siloed namespace bound to specific compute nodes for physical isolation (compliance use cases).
- **Mixed mode** — some namespaces pooled, others siloed.
- Track deployed resources so the CI/CD pipeline can update all of them.

**Don't:**
- Treat "pod" in Kubernetes as the same as "pod" in this book — different concepts.
- Run siloed namespaces per tenant if you have thousands of tenants — use a pod/grouped deployment instead.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 10: EKS" — "Deployment Patterns" / "Pooled Deployment" / "Siloed Deployments" / "Mixing Pooled and Siloed Deployments" / "Tenant-Aware Service Deployments"*

---

### 41. EKS Tenant Isolation Network Policies

**Principle:** Default-deny cross-namespace traffic in a multi-tenant EKS cluster.

**Code (per-tenant namespace deny policy):**

```yaml
# tenant-service-policy.yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  namespace: TENANT_NAME
  name: TENANT_NAME-policy-deny-other-namespace
spec:
  podSelector:
    matchLabels:
  ingress:
  - from:
  - podSelector: {}
```

**Do:**
- Apply `NetworkPolicy` per tenant namespace on provisioning — deny ingress from other namespaces by default.
- Use `podSelector` to scope the policy to the right set of pods.
- Combine with RBAC, resource quotas, and pod security policies for layered isolation.

**Don't:**
- Skip NetworkPolicy — by default Kubernetes namespaces are NOT isolated.
- Forget egress — sometimes you need both ingress and egress policies.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant Isolation" — EKS section*

---

### 42. EKS Isolation — IRSA + IAM Policies

**Principle:** Use **IAM Roles for Service Accounts (IRSA)** to attach a tenant-scoped IAM policy to each tenant namespace's service account. The compute inherits the policy automatically.

**Code (per-tenant DynamoDB policy template):**

```json
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "TENANT_NAME",
 "Effect": "Allow",
 "Action": "dynamodb:*",
 "Resource":
 "arn:aws:dynamodb:us-east-1:ACCOUNT_ID:table/Order-TENANT_NAME"
 }
 ]
}
```

**Do:**
- Bake `TENANT_NAME` placeholders during onboarding.
- Apply policies to service accounts in each tenant namespace.
- Combine deployment-time IRSA (for siloed resources) with runtime scoping (for pooled resources).

**Don't:**
- Forget to apply IRSA during the namespace creation step of onboarding.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant Isolation" — Order table isolation with IRSA*

---

### 43. EKS Onboarding Automation — Helm + Argo Workflows + Flux

**Principle:** Combine the right tools so onboarding is **declarative, idempotent, GitOps-friendly**, and **auditable**. Use Helm for templating, Argo Workflows for orchestration, Flux for reconciliation.

**Do:**
- Define a **baseline Helm template** capturing common resources.
- Generate **tier-specific Helm charts** by merging tier parameters over the baseline.
- Use **Argo Workflows** to coordinate tenant provisioning across Tier Aware steps.
- Use **Flux** (or ArgoCD) for GitOps-based reconciliation.
- Track deployed tenant resources in a structured table so CI/CD pipelines can find them all.

**Don't:**
- Couple onboarding to one-off CloudFormation or CDK scripts — bypasses Helm's templating power.
- Forget to version Helm releases — use chart version to enable updates to be detected and rolled out.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Configuring Onboarding with Helm" / "Automating with Argo Workflows and Flux"*

---

### 44. EKS Routing with Ingress + Service Mesh

**Principle:** Use **Ingress controllers** (NGINX, Contour, Kong) and **service mesh** (Istio, Linkerd, AWS App Mesh) to express tenant-aware routing.

**Do:**
- Extract subdomain from request to drive routing decisions.
- Use Ingress to map paths/hosts to services per tenant namespace.
- Use a service mesh when you need more sophisticated routing, telemetry, and policy enforcement.
- Map CDN entries like `*.saasprovider.com` to a single ingress that fans out based on subdomain.

**Don't:**
- Pick service mesh unless you need its L7 features — operational cost is non-trivial.
- Forget to add tenant-aware traffic policies in the mesh.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Routing Considerations" / "Applying EKS routing tools" / "Routing tenants to namespaces"*

---

### 45. Node Type Selection and Karpenter

**Principle:** Match node types to workload profiles. Use **Karpenter** for dynamic, workload-aware node provisioning that aligns compute cost with tenant activity.

**Do:**
- Define managed node groups for known workload patterns (memory-optimized R5, compute-optimized C5, GPU G5).
- Configure Karpenter with candidate instance types and let it pick based on real workload profile.
- Iterate on node selection as your multi-tenant workload patterns emerge.
- Avoid overprovisioning by letting Karpenter scale down aggressively.

**Don't:**
- Hand-pick too many node types — operational complexity multiplies.
- Tie pods to specific nodes unless you truly need pod-to-node co-location (compliance scenarios).

*Ref: Building Multi-Tenant SaaS Architectures.md — "Node Type Selection" / "Optimizing node types with Karpenter"*

---

### 46. Mixing Serverless with EKS (Fargate)

**Principle:** Use **Fargate** for serverless EKS compute to remove the node-management burden. Combine with managed node groups for workloads that need specific instance types.

**Do:**
- Use Fargate for stateless, spiky workloads — eliminates node overhead.
- Use managed node groups for workloads that need GPUs, large memory, or specific image types.
- Make the choice per workload, not per cluster.

**Don't:**
- Treat Fargate as a universal replacement — it has constraints (e.g., no privileged containers).

*Ref: Building Multi-Tenant SaaS Architectures.md — "Mixing Serverless Compute with EKS"*

---

### 47. Serverless Tenant Routing

**Principle:** Each Lambda function executes one tenant at a time — which makes serverless compute inherently *siloed at execution*. But you still need routing.

**Do:**
- Use **API Gateway** to map requests to functions. Combine with custom Lambda authorizers that extract tenant context from JWT.
- For siloed compute per tier, use a **gateway-per-tenant** model — easier per-tenant throttling and isolation.
- For pooled compute, share a gateway and route based on JWT-extracted tenant context.
- Cache the tenant → gateway URL mapping for low latency.

**Don't:**
- Have the client know the mapping — keep it server-side.
- Spin up thousands of gateways (cost / scale limits).

*Ref: Building Multi-Tenant SaaS Architectures.md — "Routing Strategies" / "Serverless Tenant Routing"*

---

### 48. Serverless State Residue and Cold Starts

**Principle:** Lambda execution environments are reused; tenant state can leak between invocations. Cold starts affect siloed functions disproportionately.

**Do:**
- Treat each Lambda invocation as **stateless** — clear all local state at the end.
- Use **provisioned concurrency** for premium-tier siloed functions to reduce cold starts.
- Pool functions naturally stay warm because they get hit often.

**Don't:**
- Hold per-tenant data in module-level globals.
- Forget to consider cold-start latency in your SLA for siloed premium-tier functions.

*Ref: Building Multi-Tenant SaaS Architectures.md — "More Deployment Considerations" / "Control Plane Deployment" / "Operations Implications"*

---

### 49. Serverless Isolation — Runtime Credential Injection at API Gateway

**Principle:** For pooled serverless functions, the API Gateway should **inject tenant-scoped credentials** before the request reaches the function. This eliminates per-function isolation code.

**Do:**
- Configure a Lambda authorizer on the API Gateway that extracts tenant context from JWT, populates an IAM policy, runs `assume_role`, and injects the credentials into the request header.
- Cache credentials at the gateway to amortize the cost.
- For siloed functions, attach Lambda **execution roles** at deployment for baked-in isolation.

**Don't:**
- Have each Lambda function call `assume_role` independently — both expensive and noisy.
- Mix the two patterns within one function without a clear branch (see code sample below).

*Ref: Building Multi-Tenant SaaS Architectures.md — "Pooled Isolation with Dynamic Injection" / "Deployment-Time Isolation"*

---

### 50. Serverless Tier-Aware Isolation Code

**Principle:** A single function may serve both pooled and siloed tenants; the function body must branch based on deployment mode.

**Code (silently routes to the right credential model):**

```python
def __get_dynamodb_table(event, dynamodb):
    if (is_pooled_deploy=='true'):
        accesskey = event['requestContext']['authorizer']['accesskey']
        secretkey = event['requestContext']['authorizer']['secretkey']
        sessiontoken =
        event['requestContext']['authorizer']['sessiontoken']
        dynamodb = boto3.resource('dynamodb',
        aws_access_key_id=accesskey,
        aws_secret_access_key=secretkey,
        aws_session_token=sessiontoken
        )
    else:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        return dynamodb.Table(table_name)
```

**Do:**
- Branch on a deployment-time flag (`is_pooled_deploy`) rather than runtime detection.
- Initialize the right client (injected credentials vs default).
- Keep the branch out of business logic — wrap it in a helper.

**Don't:**
- Mix both credential models at runtime — leads to subtle privilege errors.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Simultaneously Supporting Silo and Pool Isolation"*

---

### 51. Serverless Concurrency vs Noisy Neighbor

**Principle:** Lambda functions can be throttled by account-level concurrency limits and per-function reserved concurrency. Use **reserved concurrency per tier** to prevent noisy neighbor at the function level.

**Do:**
- Set reserved concurrency per function tier deployment (basic: 100, advanced: 300, premium: remainder).
- Reuse the pool reserved concurrency limit to **protect premium-tier functions**.
- Treat reserved concurrency as a tiering knob, not just a scaling knob.

**Don't:**
- Allow one basic-tier function to starve premium-tier functions.
- Forget that provisioned concurrency also costs money — apply it where it matters.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Concurrency and Noisy Neighbor"*

---

### 52. Serverless Onboarding via SAM Templates

**Principle:** Use **SAM templates** (or equivalent IaC) to declaratively provision tenant environments with tier-aware parameters.

**Do:**
- Build a universal SAM template that describes the full tenant stack (API Gateway + Lambda + RDS).
- Use tier-specific config files to inject parameters (`ProvisionedConcurrency`, `ReservedConcurrency`).
- Track tenant stacks in a `tenant_stack_mapping` table — basic-tier tenants share an entry; premium-tier tenants get their own.
- Use CodePipeline → CodeBuild → Step Function to package, deploy, and update the SAM stack per tenant.

**Don't:**
- Hardcode tier logic into the template; parameterize.
- Skip the tenant-stack-mapping table — you'll lose visibility into which tenants are on which stack.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Onboarding and Deployment Automation" / "Onboarding orchestration" / "Applying tier-aware updates"*

---

### 53. Tier-Aware Operations Mindset

**Principle:** Operations in SaaS spans product, customer success, engineering, and ops. Share operational goals across roles.

**Do:**
- Track **tenant activity metrics** (onboarding, app analytics, lifecycle events).
- Correlate onboarding state with feature adoption to identify struggling tenants.
- Adopt **DORA-style agility metrics** (availability, deployment frequency, failed deploys, cycle time, MTTD, MTTR, defect escape rate).
- Build **consumption metrics** at API, microservice, and infrastructure layers.
- Compute **cost-per-tenant** by joining consumption with billing — share with product/pricing teams.
- Track **business health metrics** (MRR, Churn, CAC, CLTV, CLTV/CAC).

**Don't:**
- Treat ops as purely a health-monitoring role — SaaS ops observe the *entire* service experience.
- Build metrics that don't drive decisions.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 12" — "The SaaS Operations Mindset" / "Multi-Tenant Operational Metrics" / "Business Health Metrics"*

---

### 54. Cost-per-Tenant Metrics

**Principle:** Map consumption data to infrastructure billing to **approximate** per-tenant cost. It's an operational view (not accounting-grade billing) that informs tier/pricing decisions.

**Do:**
- Capture per-tenant consumption from APIs, microservices, and infrastructure.
- Ingest cloud billing data (Cost & Usage Reports or third-party tools).
- Join consumption → billing to allocate cost to tenant.
- Use the data for tiering and pricing decisions, not finance billing.

**Don't:**
- Try to make cost-per-tenant perfectly accurate — approximation is fine.
- Skip building it entirely — pricing strategy without cost data is a guess.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Cost-per-Tenant Metrics" / "Correlating consumption with costs"*

---

### 55. Tenant-Aware Operations Console

**Principle:** Off-the-shelf monitoring tools don't have tenant context. Build or configure a **tenant-aware operations console** with per-tenant and per-tier views.

**Do:**
- Filter all dashboards by tenant / tier.
- Surface most-active tenants, noisy-neighbor candidates, and tenants approaching limits.
- Link directly to tenant's infrastructure resources for fast triage.
- Provide persona-specific dashboards (ops, product, customer success, leadership).
- Use tenant-aware logs (every log line has tenant ID).

**Don't:**
- Rely solely on generic health dashboards — they cannot answer tenant-specific questions.
- Mix tenant data into a global view without a filter.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Building a Tenant-Aware Operations Console" / "Persona-Specific Dashboards" / "Tenant-Aware Logs"*

---

### 56. Targeted Releases / Canary by Tier

**Principle:** In a SaaS environment, canary releases by tier protect premium experiences during risky rollouts.

**Do:**
- Group tenants for staged releases (e.g., friendly tenants first, basic-tier pool last, premium tier first).
- Use feature flags to gate new features per tenant tier.
- Tie canary decisions to observable metrics (error rate, latency).
- Use deployment scripts that understand tenant-stack mapping (especially for siloed/serverless).

**Don't:**
- Do "big bang" releases for all tenants — high blast radius.
- Couple feature flags to per-tenant customization — they are tier-level mechanisms.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Multi-Tenant Deployment Automation" / "Targeted Releases" / "Scoping Deployments"*

---

### 57. Tenant Isolation Test Strategy

**Principle:** Multi-tenant bugs are catastrophic. Build **explicit cross-tenant test cases**.

**Do:**
- Inject an invalid tenant context mid-test and expect denial.
- Use chaos engineering to confirm isolation holds under load.
- Add operational alerts when isolation violations are detected.
- Treat cross-tenant violations as P0 incidents.

**Don't:**
- Assume isolation works without testing — it must be exercised explicitly.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Managing Isolation Policies"*

---

### 58. SaaS Migration — Build the Control Plane First

**Principle:** Every migration pattern (silo lift-and-shift, layered, service-by-service) **begins with the control plane**. There is no shortcut around onboarding, identity, and tenant management.

**Do:**
- Build the control plane, tenant management, identity, onboarding, and basic metrics before migrating application code.
- Choose a migration pattern based on business and technology realities:
  - **Silo lift-and-shift** — fastest path, lowest risk, but limited efficiency.
  - **Layered migration** — incrementally move layers to shared infrastructure.
  - **Service-by-service** — modernize one service at a time; strangler pattern.
- Build new microservices as **first-class, multi-tenant-ready** from day one.

**Don't:**
- Defer control plane work — it will collapse into a bolting-on exercise.
- Build new microservices with per-tenant shortcuts.
- Couple legacy app-tier code with the new control plane without a clear plan.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 13: SaaS Migration Strategies" — "The Foundation" / "Silo Lift-and-Shift" / "Layered Migration" / "Service-by-Service Migration" / "Where You Start Matters"*

---

### 59. Migration Timing — SaaS Now vs Modernize First

**Principle:** Favor **"SaaS now"** with minimal application refactoring, then modernize using real customer feedback. Tech debt + delays = missed markets.

**Do:**
- Get to a multi-tenant SaaS offering fast; use customer feedback to drive modernization.
- Track economics via the **fish model** (Baker/Lah): expect cost to rise during transformation and revenue to dip during pricing-model transition.
- Treat the migration as a business transformation (sales, support, ops), not just code.

**Don't:**
- Modernize for years before going to market.
- Frame migration as a tech problem — it's business + technology.

*Ref: Building Multi-Tenant SaaS Architectures.md — "The Migration Balancing Act" / "What Kind of Fish Are You?"*

---

### 60. Migration Pattern Pros/Cons

**Principle:** Pick a migration pattern honestly.

**Silo lift-and-shift:**
- + Time to market; minimal invasiveness; simpler isolation.
- − Agility/innovation; cost; manageability.

**Layered migration:**
- + Incremental; moderate invasion; quick successes.
- − Time to market; manageability; cost.

**Service-by-service:**
- + Incremental; full modernization; scale/availability/agility.
- − Time to market; data-model migration; complexity.

**Do:**
- Combine patterns in phases.
- Reassess at each phase — your decisions should evolve with real-world data.

**Don't:**
- Commit to a single pattern without an exit criteria.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Comparing Patterns" / "A Phased Approach"*

---

### 61. Tiering Patterns — Consumption / Value / Deployment / Composite

**Principle:** Combine **consumption** (capacity limits), **value** (features, SLAs), and **deployment** (silod vs pool) tiers into a coherent offering. Add a **free tier** for product-led growth.

**Do:**
- Align cost-per-tenant insight with tier boundaries so consumption tiering is grounded in real data.
- Tie consumption constraints to actual pricing (a $50 tier should not consume at the rate of a $5,000 one).
- Use value tiering to differentiate features, throughput SLAs.
- Use deployment tiering to address compliance and isolation needs.
- Mix and combine patterns — composite strategies are the norm.

**Don't:**
- Rely on consumption-based pricing without tier constraints — free-reign can saturate the system.
- Forget free-tier cost analysis — free tiers can eat margin quickly.
- Hide free-tier limits from tenants — be explicit.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 14: Tiering Strategies" — "Consumption-Focused Tiering" / "Value-Focused Tiering" / "Deployment-Focused Tiering" / "Free Tiers" / "Composite Tiering Strategies"*

---

### 62. API Tiering — Throttling & API Keys

**Principle:** Apply tier-based throttling at the API edge using usage plans and API keys. Mask the mapping from the client.

**Do:**
- Configure each tier (usage plan) with its own rate, burst, and quota.
- Use a Lambda custom authorizer to map incoming tenant context to the correct API key (so the client doesn't need to know).
- Set tier-appropriate throttling in API Gateway.

**Don't:**
- Require clients to know their tier's API key — abstract it server-side.
- Forget to surface throttling activity in operational dashboards.

*Ref: Building Multi-Tenant SaaS Architectures.md — "API Tiering"*

---

### 63. Compute Tiering — Reserved Concurrency & Resource Quotas

**Principle:** Tier compute resources by reserving concurrency (serverless) or applying resource quotas (Kubernetes).

**Do:**
- In serverless: deploy tier-specific function copies with different `ReservedConcurrency` settings.
- In Kubernetes: apply ResourceQuota per namespace; tie quotas to tier.
- Use tier-differentiated autoscaling policies to reinforce tier SLAs.

**Don't:**
- Share a single concurrency limit across tiers without protecting higher tiers.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Compute Tiering" / "Serverless tiering with concurrency" / "Tiering Kubernetes compute resources"*

---

### 64. Storage Tiering — IOPS / Throughput / Capacity / Retention

**Principle:** Tier storage by IOPS, throughput, capacity, and retention. Combine with silo-vs-pool decisions at the service level.

**Do:**
- Configure per-tier performance (IOPS, throughput) on shared storage.
- Differentiate siloed storage by tier when premium experience warrants it.
- Apply capacity limits and retention policies per tier where appropriate.

**Don't:**
- Pick per-tenant storage configurations — keep tier-differentiated.
- Forget that per-tenant configurations erode operational efficiency.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Storage Tiering"*

---

### 65. Tiering and Microservice Deployment

**Principle:** Composition of deployment models can itself be a tiering strategy (e.g., basic tier pool; premium tier partial silo).

**Do:**
- Decide per microservice whether it's pooled, siloed, or tier-dependent.
- Mix-and-match — basic-tier pool + premium-tier siloed subset is common.
- Lean into deployment-based tiering when compliance or isolation is involved.

**Don't:**
- Couple tiering to one mechanism (price-only, capacity-only, etc.).
- Forget to surface tier-based deployment differences in operations.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Deployment Models and Tiering" / "Applying tiering to microservice deployments"*

---

### 66. SaaS Anywhere (Remote Resources) — Resist Drift Toward MSP

**Principle:** Place only what is absolutely necessary in tenant environments. Every remote concession chips away at SaaS agility.

**Do:**
- Prefer **same-cloud remote** (tenant's account in your cloud) — keeps you in familiar territory.
- Use a centralized **control plane orchestrator** that owns the lifecycle of remote resources.
- Be explicit about which resources are remote and why.
- Preserve single-version discipline even across remote footprints.

**Don't:**
- Treat remote application plane as a fallback — it's an MSP pattern.
- Concede per-tenant remote for marketing convenience alone.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 15: SaaS Anywhere" — "Ownership" / "Limiting Drift" / "Multiple Flavors of Remote Environments" / "Architecture Patterns" / "Remote Data" / "Remote Application Services" / "Remote Application Plane"*

---

### 67. SaaS Anywhere Architecture Patterns

**Principle:** Three remote patterns sit on a spectrum from least to most concession.

- **Remote data** — application plane in your environment; data lives in tenant. Most concession-compatible.
- **Remote application services** — full microservices in tenant; lowest latency for local data.
- **Remote application plane** — entire application plane in tenant; only control plane in SaaS provider. Maximum concession — virtually full-stack silo.

**Do:**
- Default to remote data for compliance/security/volume.
- Treat remote application services as legitimate when latency demands.
- Avoid full remote application plane unless absolutely necessary.

**Don't:**
- Slip from "remote data" to "remote application plane" without a clear trigger.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Architecture Patterns" — "Remote Data" / "Remote Application Services" / "Remote Application Plane"*

---

### 68. SaaS Anywhere — Operational Discipline

**Principle:** Remote resources complicate deployment, observability, scale, and availability. Treat them with the same rigor as primary-plane resources.

**Do:**
- Require remote services to publish logs/metrics/billing events to your control plane.
- Plan for graceful degradation when a remote resource is unavailable.
- Keep deployment automation tenant-aware for remote updates.
- Treat remote integration as a security boundary.

**Don't:**
- Run remote resources without observability into the control plane.
- Skip authorization flows for cross-environment access.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Operations Impacts and Considerations" / "Provisioning and Onboarding" / "Access to Remote Resources" / "Scale and Availability" / "Operational Insights" / "Deploying Updates"*

---

### 69. GenAI in SaaS — Tenant Refinements (RAG, Fine-Tuning)

**Principle:** Bring tenant context to LLMs through **RAG** (pre-prompt augmentation from per-tenant data) or **fine-tuning** (per-tenant logical model). Combine both when each technique targets a different concern.

**Do:**
- RAG: pre-process prompts with tenant-specific data (knowledge stores per tenant).
- Per-tenant fine-tuning: pair a base LLM with each tenant's tuning data into logical models; reference by tenant at invocation.
- Combine: RAG augments the prompt, fine-tuning changes behavior. Both can coexist.
- Leverage managed GenAI services (Amazon Bedrock, OpenAI) for base model access.

**Don't:**
- Confuse RAG (pre-prompt augmentation) with fine-tuning (LLM behavior change).
- Forget isolation, onboarding, and noisy-neighbor considerations for RAG stores and fine-tuning data.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 16: GenAI and Multi-Tenancy" — "Core Concepts" / "The Influence of Multi-Tenancy" / "Supporting Tenant-Level Refinement with RAG" / "Supporting Tenant Refinement with Fine-Tuning" / "Combining RAG and Fine-Tuning"*

---

### 70. GenAI Tenant Data — Partition, Isolate, Onboard

**Principle:** Every per-tenant GenAI asset (RAG indexes, fine-tuning data, vector stores) must follow the same partitioning, isolation, and onboarding discipline as the rest of multi-tenant data.

**Do:**
- Use siloed OpenSearch indexes (per-tenant) for vector data when isolation matters; pool indexes with `TenantId` partitioning for cheap scale.
- Extract, transform, and load (ETL) tenant data into per-tenant RAG stores during onboarding.
- Add isolation policies around vector store access.
- Validate noisy-neighbor risk on shared embeddings indexes.

**Don't:**
- Share a single embedding index across all tenants in regulated contexts.
- Defer isolation review for GenAI assets to "later".

*Ref: Building Multi-Tenant SaaS Architectures.md — "Applying General Multi-Tenant Principles" — "Onboarding" / "Tenant Isolation"*

---

### 71. GenAI Noisy Neighbor — Token Complexity

**Principle:** Token volume alone doesn't measure GenAI load. **Prompt/output complexity** (number of tokens, model used) drives both cost AND noisy-neighbor potential.

**Do:**
- Track token counts (prompt + output) per request alongside tenant context.
- Throttle by complexity, not just request count.
- Expose model selection by tier (cheaper models for basic, expensive models for premium).

**Don't:**
- Throttle purely on request frequency — a single huge prompt can saturate the system.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Noisy Neighbor" / "Creating Tiered Tenant Experiences"*

---

### 72. GenAI Pricing — Capture Token Complexity

**Principle:** Build metering events for prompt AND output tokens. Use them for both billing and noisy-neighbor analytics.

**Do:**
- Add a consumption billing library that intercepts prompts and outputs, meters tokens, and publishes events to the billing service.
- Model pricing as fixed (predictable) for embedded GenAI usage; usage-based for user-facing GenAI usage.
- Tie tiering to GenAI tier characteristics: reserved throughput, allowed model tier, allowed token counts.

**Don't:**
- Quote prices without visibility into token consumption cost.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Developing a Pricing Model" / "Capturing and calculating token complexity"*

---

### 73. AI/ML in SaaS — Per-Tenant Models via SageMaker

**Principle:** Traditional AI/ML (per-tenant models via SageMaker) often beats GenAI for granular multi-tenant control. Pool a model for basic; dedicate or fine-tune per tenant for premium.

**Do:**
- Offer pooled inference for basic tier.
- Use SageMaker dedicated/elastic inference for premium tier SLAs.
- Build model-as-a-service offerings where customers access your ML models via API.

**Don't:**
- Funnel every AI workload through GenAI when AI/ML fits better.

*Ref: Building Multi-Tenant SaaS Architectures.md — "SaaS and AI/ML"*

---

### 74. Guiding Principles — Build the Business Model and Strategy First

**Principle:** SaaS architects cannot design in a vacuum. Without a business model (target market, personas, growth, margins) you can't pick an architecture.

**Do:**
- Press the business for clarity on personas, segments, growth, margins.
- Build that data into every architecture decision.
- Treat vision and strategy as living documents updated with real-world feedback.

**Don't:**
- Defer business alignment — it compounds into rework.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 17" — "Vision, Strategy, and Structure" / "Build a Business Model and Strategy"*

---

### 75. Avoid Tech-First Trap

**Principle:** Many SaaS projects fail because technology chose architecture before business strategy landed.

**Do:**
- Pair every architecture decision with a business rationale.
- Ask: "what does this enable the business to do?"
- Co-evolve business and technical roadmaps.

**Don't:**
- Build the SaaS app first, then try to retro-fit a business case.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Avoiding the Tech-First Trap"*

---

### 76. Adopt a Service-Centric Mindset (Restaurant Analogy)

**Principle:** SaaS is **service** (restaurant experience: greeting, water, food speed) not product (food alone). The same applies to onboarding, support, and operations.

**Do:**
- Measure the **service experience** end-to-end.
- Expand product-owner backlog with service metrics.
- Adopt shared service-focused goals across teams.

**Don't:**
- Treat SaaS as just monthly billing.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Adopt a Service-Centric Mindset" / "Building a Service—Not a Product"*

---

### 77. Be All-In With SaaS — Resist One-Off Customization

**Principle:** Compromise on SaaS once and you trigger MSP drift. Resist — every one-off customer erodes agility.

**Do:**
- Use tier-based and configuration-based customization rather than per-tenant custom code paths.
- Encode feature flags at the tier level.

**Don't:**
- Land "strategic" deals that demand per-tenant exceptions.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Be All-In with SaaS" / "Avoid One-Off Customization"*

---

### 78. Measure Your Multi-Tenant Architecture

**Principle:** Without tenant-aware metrics, you cannot validate that your multi-tenant architecture is performing as designed. Continuously measure noisy neighbors, tier SLAs, isolation, and efficiency.

**Do:**
- Instrument every multi-tenant concern (noisy neighbor, tier SLAs, isolation, cost-per-tenant).
- Instrument proactively — before complaints come in.
- Build dashboards per persona (ops, product, customer success, leadership).

**Don't:**
- Rely on out-of-the-box monitoring without tenant context.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Measure Your Multi-Tenant Architecture"*

---

### 79. Streamline the Developer Experience

**Principle:** Builders should focus on **business logic**, not on multi-tenant plumbing. Push tenant handling into shared libraries, helpers, aspects, sidecars, Lambda Layers.

**Do:**
- Provide `get_tenant_context()`, scoped-client factories, tenant-aware logging wrappers.
- Use Lambda Layers to version multi-tenant helpers across serverless functions.
- Set service templates that include multi-tenant plumbing by default.

**Don't:**
- Leave multi-tenant code copy-pasted in every service.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Streamline the Developer Experience"*

---

### 80. Operations Mindset — Beyond System Health

**Principle:** Operations in SaaS observes the **whole service experience** — not just uptime.

**Do:**
- Track onboarding time-to-value.
- Watch tier-throttling policies for signs of being too aggressive or too lenient.
- Surface cost-per-tenant trends to product/pricing.
- Tie operations to business outcomes.

**Don't:**
- Treat "the system is up" as the operations job.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Operations Mindset" / "Thinking Beyond System Health"*

---

## Anti-Patterns & Common Mistakes

- **"Single-tenant" thinking:** Treating dedicated-infrastructure tenants as not-SaaS; missing that SaaS is defined by unified operations, not shared compute. → *Fix:* Operate all dedicated tenants through the same control plane, deploy same version, surface in same admin console.
- **Bolt-on multi-tenancy:** Building the application first, planning to "add tenancy later". Almost always ends in refactor. → *Fix:* Start with control plane (onboarding, identity, tenant management).
- **Centralized tenant-mapping service on every request:** Forces every service to resolve tenant context via a service hop — hotspot and SPOF. → *Fix:* Embed tenant context in JWT custom claims; avoid centralized lookup.
- **Conflating deployment and isolation:** Putting data in separate DBs and calling it "isolated". Code can still cross. → *Fix:* Decouple deployment model from isolation enforcement (use policies).
- **One-off tenant customization:** Per-tenant code paths, per-tenant features, per-tenant deployment. Erodes SaaS agility and shifts toward MSP. → *Fix:* Tier-based feature flags, configuration, deployment models.
- **Per-request STS assume_role without caching:** Latency and throttling pressure. → *Fix:* Cache scoped credentials in-process with TTL.
- **Object store with bucket-per-tenant at scale:** Hits 1,000-bucket/account limits. → *Fix:* Use bucket + prefix-key or prefix-key-as-silo.
- **Treating SaaS as cost optimization:** Misses the real value (agility, innovation, growth). → *Fix:* Frame goals broadly: economies of scale, reach, innovation.
- **Per-tenant IAM policies:** Hits service limits; maintenance burden. → *Fix:* Use parameterized policy templates.
- **Full-stack silo as default:** High baseline cost per tenant; kills scaling economics. → *Fix:* Default to pooled; silo only when compliance/noisy-neighbor demands.
- **Cold-start blind spot for serverless siloed functions:** Premium-tier tenants get unexpected latency. → *Fix:* Apply provisioned concurrency where warranted.
- **GenAI pricing without token metering:** Lose money on heavy users; no noisy-neighbor control. → *Fix:* Build prompt/output metering and gate by complexity.
- **Tenant isolation test coverage missing:** Cross-tenant bugs slip into production. → *Fix:* Inject invalid tenant context mid-test; add alerts on cross-tenant access attempts.
- **SaaS Anywhere as escape hatch:** Remote application planes or services drift toward MSP. → *Fix:* Limit remote concessions to specific data/services; preserve control-plane-driven operations.
- **Cost-per-tenant "all-or-nothing":** Per-resource cost accounting is hard to maintain. → *Fix:* Approximate cost-per-tenant; focus on major cost drivers.
- **Per-tenant OpenSearch domain:** Operational sprawl and high cost. → *Fix:* Index-per-tenant in shared domain.
- **Ignoring sharding when one pool maxes out:** Service degrades silently. → *Fix:* Shard tenant pools before failure; use DAL for tenant→pool mapping.
- **Tier changes that look simple but include cross-deployment migration:** Disrupts live tenants. → *Fix:* Plan migration as a complete lifecycle event; reuse onboarding code.

## Decision Heuristics / Checklists

- **Pool or silo?** Ask: "Where does compliance require isolation? Where does noisy-neighbor pressure demand isolation? Where does scale make pooled preferable?" Default to pool; silo to earn its way out.
- **Deployment-time or runtime isolation?** Siloed compute → deployment-time. Pooled compute → runtime + DAL.
- **Per-tenant or per-tier configuration?** Always tier-level. One-offs erode agility.
- **Self-service or internal onboarding?** Same automation bar.
- **Build the control plane first?** Yes. Always.
- **What part of the system goes remote?** A strong default: as little as possible. Prefer same-cloud remote over cross-cloud.
- **When to use GenAI vs AI/ML?** GenAI for natural-language / RAG workloads; AI/ML for predictable per-tenant ML models.
- **When to use RDS schemas, databases, instances?** Per-tenant DB instances for strict isolation; per-tenant DBs for shared infrastructure with isolation; per-tenant tables for shared DB isolation.
- **When to use EKS Fargate vs managed node groups?** Fargate when node selection is non-issue; managed node groups for specific instance-type optimization (Karpenter).
- **When to use cross-tenant JWT central lookup?** Only as a last resort (e.g., single-domain auth flow with grouped IdP constructs). Inject claims at IdP when possible.

## Key Takeaways

1. **SaaS is a business model.** Business strategy + technical architecture co-evolve.
2. **Multi-tenancy = unified operations**, not shared infrastructure. Avoid the "single-tenant" word.
3. **Control plane first.** Onboarding, identity, tenant management, metrics, billing are day-one.
4. **Tenant context is the connective tissue.** Issue JWTs with custom claims at the IdP; never require a downstream lookup.
5. **Deployment and isolation are distinct concerns.** Silos don't auto-isolate; pools require explicit policy enforcement.
6. **Compose silo/pool per service, per tier, per resource.** There is no one-size-fits-all model.
7. **Hide multi-tenant plumbing from developers.** Helpers, aspects, sidecars, Lambda Layers, middleware.
8. **Tenant context everywhere.** Every log line, every metric, every query must include `tenantId` and `tenantTier`.
9. **Tenant-aware ops console.** Off-the-shelf monitoring tools don't have tenant context — build it.
10. **Tiering aligns consumption with revenue.** Combine consumption, value, and deployment tiering. Use free tiers responsibly.
11. **Silo lift-and-shift is the fastest migration.** Layered and service-by-service are incremental modernization paths.
12. **SaaS Anywhere is a balancing act.** Limit remote concessions; prefer same-cloud; preserve control-plane control.
13. **GenAI is multi-tenant data too.** Treat RAG indexes, fine-tuning data, and embeddings with the same partitioning/isolation discipline.
14. **Measure the architecture.** Tenant-aware metrics drive architectural evolution.
15. **Guard the SaaS principles.** Every one-off customer erodes agility and pushes toward MSP.

---

### 81. B2B vs B2C Multi-Tenancy — Implications for Architecture

**Principle:** B2B and B2C SaaS have fundamentally different **tenant counts, workload profiles, deployment tolerance, and customization pressure**. Conflating them produces architectures that are bad at both.

**Do:**
- **B2B** — Hundreds to thousands of tenants, larger per-tenant footprint, willingness to pay for premium tiers, frequent domain/compliance constraints. Mix siloed and pooled deployments freely; dedicate infrastructure for premium tiers; support vanity domains; longer sales cycles, manual onboarding common.
- **B2C** — Hundreds of thousands to millions of "tenants" that are really users. Aggressive scaling, freemium/product-led growth, fully pooled, shared identity, single domain for routing. Customization is rare — feature flags cover the bulk of variation.
- For B2B: build identity constructs that map to **tenant grouping** (User Pools, groups) so a tenant admin can manage their own users.
- For B2C: keep one global identity construct; the tenant is the user.

**Don't:**
- Apply the same tiering, onboarding, or isolation strategy across B2B and B2C.
- Assume B2C's hyper-scale demands are valid in B2B (and vice versa).

*Ref: Building Multi-Tenant SaaS Architectures.md — "The B2B and B2C SaaS Story"*

---

### 82. Federated Identity — Enriching Tokens with Tenant Context

**Principle:** When tenants bring their own IdP (SAML, OIDC), the JWT you receive **lacks your custom tenant claims**. Enrich the tokens with a SaaS identity layer that injects tenant context.

**Do:**
- Use an identity proxy / token enrichment service (e.g., Cognito with federated providers) to add your custom claims on top of the federated JWT.
- Encode the mapping between external identity groups/users and your internal tenant identifier.
- Treat this as part of the multi-tenant identity story — document the enrichment path.

**Don't:**
- Bypass the IdP and parse arbitrary JWTs in code — fragile.
- Assume external IdPs will respect your custom-claim requirements.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Federated SaaS Identity"*

---

### 83. Multi-Factor Authentication (MFA) and Per-Tenant Auth Policies

**Principle:** Use your IdP's per-tenant configuration constructs to apply MFA, password complexity, lockout, and rotation policies.

**Do:**
- Configure MFA, password policy, rotation as per-tenant settings where supported by your IdP.
- Tier MFA (e.g., only enable MFA on premium tier tenants).
- Surface the configuration through the Tenant Management service.

**Don't:**
- Hard-code identity policies in microservices — keep them in Tenant Management.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant Grouping/Mapping Constructs"*

---

### 84. Sharing User IDs Across Tenants

**Principle:** If a single user can belong to multiple tenants, your IdP construct needs careful design — the same email is unique within a User Pool.

**Do:**
- Use multiple identity constructs (User Pools, group hierarchies) to allow the same email to belong to different tenants.
- Resolve tenant membership **before** redirecting to the IdP.
- Use subdomains as the cleanest tie-breaker (`tenant1.saasprovider.com`).

**Don't:**
- Implement a login-time tenant picker that leaks which tenants a user belongs to.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Sharing User IDs Across Tenants"*

---

### 85. Tenant-Aware Caching Strategies

**Principle:** Cache aggressively, but **always include tenant context** in cache keys. Otherwise you risk serving one tenant's data to another.

**Do:**
- Build cache keys that include `tenantId` (and tier if relevant).
- Use TTLs appropriate to the data freshness SLA.
- Invalidate caches during tenant lifecycle events (tier change, decommission).

**Don't:**
- Use `tenantId:None` caches in pooled multi-tenant systems — high cross-tenant risk.

*Ref: Building Multi-Tenant SaaS Architectures.md — Implicit in "Tenant Context" / "Tenant Isolation" / "Accessing Data with Tenant Context"*

---

### 86. Connection Pool Sizing and Tenant Awareness

**Principle:** Database connection pools become a **natural noisy-neighbor vector** in pooled SaaS. Tenant awareness plus tier-aware pool sizes prevents collisions.

**Do:**
- Tier pool sizes when possible (premium-tier functions get larger pool slices).
- Cap pool sizes with a per-instance limit so one pool can't starve another.
- Treat connection exhaustion as a per-tenant metric.
- Consider PgBouncer, ProxySQL, or RDS Proxy for relational stores.

**Don't:**
- Share an unbounded connection pool across tenants.
- Let a noisy tenant use all available connections.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Serverless Storage" / "Throughput and Throttling" / implied by performance-isolation discussion*

---

### 87. Tenant-Aware Database Schema Migrations

**Principle:** Tenant data partitioning interacts with schema evolution. Different partitioning strategies absorb migrations differently.

**Do:**
- **Pooled (TenantId column)**: feature-friendly — schemaless NoSQL tolerates new fields; relational requires migration but only updates the shared table.
- **Siloed tables/schemas**: feature-friendly (each migration is small per tenant but applied across all tenants).
- **Siloed databases/instances**: feature-expensive — migration must fan out to N tenant instances, doubling deployment cost.
- Plan migration rollouts to match partitioning model.

**Don't:**
- Pick partitioning without considering migration cost.
- Apply schema changes to a fleet of siloed instances by hand.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Serverless Storage" + general theme of data partitioning*

---

### 88. Per-Tenant Encryption Keys (BYOK)

**Principle:** Compliance often requires tenant-owned keys. This implies **siloed storage** at the data layer.

**Do:**
- Provide a per-tenant KMS key for sensitive workloads.
- Lifecycle the per-tenant key with the tenant — delete with decommissioning.
- Use managed encryption features (S3 SSE with KMS, RDS encryption with KMS, DynamoDB encryption with KMS).
- Document the BYOK flow in the admin console.

**Don't:**
- Share a single encryption key across tenants when regulations demand BYOK.
- Forget operational complexity — every key has a lifecycle.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Multi-Tenant Data Security"*

---

### 89. Regional/Global Tenancy — Data Residency

**Principle:** Regional deployments satisfy data-residency / GDPR / data-sovereignty requirements but introduce multi-region complexity.

**Do:**
- Select region per tenant where the workload allows.
- Pin data plane to a region; pin control plane to its own region (or replicated).
- Use regional constructs for compliance reporting.

**Don't:**
- Replicate tenant data across regions without explicit consent.
- Treat all regions as fungible for compliance-sensitive data.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Regional Deployments Versus Remote Resources"*

---

### 90. Microservices Must Be Designed for Multi-Tenant Scale

**Principle:** The shape of a microservice in pooled multi-tenant mode is fundamentally different from the same service in a single-tenant world. Decompose for fine-grained scale.

**Do:**
- Decompose services to address noisy-neighbor pressure points.
- Make every service tenant-aware through shared libraries.
- Reason about scaling at the **operation level** (serverless) or **service level** (container).
- Design data access for pooled (TenantId partitioned) and siloed (per-tenant table/db) alike.

**Don't:**
- Reuse single-tenant microservice designs unchanged in pooled multi-tenant mode.
- Forget that one slow tenant can exhaust a shared service pool.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Designing Multi-Tenant Services" / "Services in Classic Software Environments" / "Services in Pooled Multi-Tenant Environments"*

---

### 91. Serverless Function Cold Start Mitigation Strategies

**Principle:** Cold starts disproportionately affect siloed functions (single tenant = less steady traffic = more cold). Mitigate deliberately.

**Do:**
- Apply **Provisioned Concurrency** for tier-deployed, siloed functions where SLA demands it.
- Use **keep-warm** pings judiciously (cheap, predictable, but uses capacity).
- Choose function memory to balance compute cost vs cold-start latency.

**Don't:**
- Rely on cold-start tolerance for premium-tier SLAs.
- Apply Provisioned Concurrency to all functions — it's expensive and unnecessary for pool-deployed ones.

*Ref: Building Multi-Tenant SaaS Architectures.md — "More Deployment Considerations" / "Deployment Time" Control Plane /serverless cold-start context*

---

### 92. SAM Tier Configuration Pattern

**Principle:** Use parameter files to express tier variability cleanly — keep the SAM template generic.

**Do:**
- Build a **universal SAM template** with parameter placeholders.
- Maintain tier-specific config files (`basic-tier.json`, `premium-tier.json`) that supply the values.
- Tier config decides `ProvisionedConcurrency`, `ReservedConcurrency`, throughput settings, etc.
- Pass tier config into the template via Step Functions / CI.

**Don't:**
- Branch the SAM template per tier — sprawl.
- Skip parameterization — you lose auditability.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Defining serverless tiered environments" / "Onboarding orchestration"*

---

### 93. Tenant Stack Mapping Table (Serverless-Specific)

**Principle:** Without a registry of which tenants are on which stacks, you cannot deploy reliably or audit usage. Maintain this table as a first-class control-plane resource.

**Do:**
- Keep a table linking: `tenantId` (or "pooled"), `deployment_type`, `stack_id`, `api_gateway_url`, `version`.
- Update the table in your onboarding and deployment steps.
- Read the table in your CI/CD to identify deployment targets.
- Use flags (e.g., `canary_phase`) to gate staged rollouts.

**Don't:**
- Skip this table — you'll lose visibility into which deployments exist for whom.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Onboarding orchestration" / "Applying tier-aware updates"*

---

### 94. Helm Tier Charts in Detail

**Principle:** Tier-specific Helm charts inherit from a baseline template. This is your **versioned source of truth** for what each tenant gets.

**Do:**
- Maintain one **baseline** Helm chart (services, defaults).
- Maintain tier-parameter config files.
- Generate tenant-specific Helm releases by merging baseline + tier params.
- Commit tenant-specific Helm configs to git; let Flux reconcile.

**Don't:**
- Hand-edit cluster state for tenants — drift city.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Configuring Onboarding with Helm"*

---

### 95. Karpenter + Tier-Aware Node Selection

**Principle:** Karpenter's dynamic selection complements tier-aware deployments. Combine for the best efficiency.

**Do:**
- Define candidate instance types Karpenter can pick from.
- Bias toward smaller nodes for basic-tier pooled pods; bigger nodes for premium-tier siloed pods (using pod-to-node affinities where needed).
- Periodically review node-type usage and adjust candidates.

**Don't:**
- Forget that Karpenter still applies a baseline cost — set budgets.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Node Type Selection" / "Optimizing node types with Karpenter"*

---

### 96. Istio Mesh Tenant Routing

**Principle:** Use Istio as your **tenant-aware L7 routing/proxy**. Offload tenant identification, JWT validation, and policy enforcement to the mesh.

**Do:**
- Centralize JWT validation and tenant-context injection at the Istio ingress gateway.
- Use Envoy filters for per-tenant routing decisions.
- Apply peer authentication and AuthorizationPolicy per namespace.

**Don't:**
- Couple Istio configuration to per-tenant manifests — that's thousands of YAMLs.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Container Tenant Routing" / "Routing tenant requests with a service mesh"*

---

### 97. Rate Limiting and Throttling at the Edge

**Principle:** Apply per-tenant rate limiting at the edge — API Gateway, CDN, WAF — to absorb spike traffic before it touches downstream services.

**Do:**
- Use API Gateway usage plans per tier.
- Configure AWS WAF rate-based rules for hostname/header-based limits.
- Combine token-bucket and quota models where appropriate.
- Throttle by tier — protect premium from basic-tier flooding.

**Don't:**
- Build per-tenant throttling in microservices — push it to the edge.

*Ref: Building Multi-Tenant SaaS Architectures.md — "API Tiering" / "Routing"*

---

### 98. Tier-Based Consumption Analytics

**Principle:** Layer consumption analytics with **tier and tenant context**. This unlocks usage patterns per tier that drive feature and pricing decisions.

**Do:**
- Build dashboards that filter by tier (basic, premium) and by individual tenant.
- Track feature usage per tenant and feed cohort analyses to product.
- Combine tenant activity + cost-per-tenant + billing for end-to-end visibility.

**Don't:**
- Build global dashboards without tenant filter — they obscure tier-specific signals.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Cost-per-Tenant Metrics" / "Tenant Activity Metrics"*

---

### 99. Composite Tiering Strategy

**Principle:** Tiering benefits from combining **consumption, value, and deployment** characteristics. Pick the mix that fits your business.

**Do:**
- Treat consumption tiering as the basic axis (rate limits, capacity).
- Add value tiering (features, throughput SLA, support level) as the second axis.
- Layer deployment tiering (silod vs pool) for compliance/SLA reasons.
- Mix freely — pricing is a UX problem as much as a cost problem.

**Don't:**
- Let any one tiering mechanism dominate without testing combinations.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Composite Tiering Strategies"*

---

### 100. Edge Cases for Tenant Onboarding — Failure Recovery

**Principle:** Onboarding is a **multi-step distributed transaction** that hits your own services, third-party IdPs, third-party billing, and remote infrastructure. Plan for partial failures.

**Do:**
- Make every step idempotent — retrying must converge.
- Use a state machine per onboarding run; surface transitions in the admin console.
- Track retry counts and timeouts.
- Decide policy for partial failure (mark tenant inactive, retry, rollback, manual intervention).

**Don't:**
- Trust any step to succeed the first time — design for failure.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Handling Onboarding Failures" / "Tracking and Surfacing Onboarding States"*

---

### 101. Tier-Changing Best Practices

**Principle:** Tier changes are **end-to-end lifecycle events** — treat them with the same rigor as onboarding.

**Do:**
- For tier flip in pooled mode: feature-flag updates + throttle changes.
- For tier migration across deployment models: full provisioning + data migration + traffic cutover.
- Notify the tenant before, during, and after migration.
- Roll back capability if needed (don't lose customer data).

**Don't:**
- Treat tier changes as trivial DB updates.
- Migrate live tenants without scheduled downtime or zero-downtime infrastructure.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Changing Tenant Tiers" / mixed mode tier migration*

---

### 102. SOC2 / GDPR Compliance Patterns in SaaS

**Principle:** Compliance regimes feed directly into your deployment, isolation, and operational choices.

**Do:**
- Map SOC2 / GDPR / PCI controls to specific technical implementations (audit logs, encryption, isolation, regional pinning).
- Embed compliance in your tenant management — emit audit events on tenant lifecycle changes.
- Use **regional** deployments for data residency.
- Per-tenant keys for regulated workloads.
- Document the controls and their implementations.

**Don't:**
- Treat compliance as a checklist — embed it in architecture.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Multi-Tenant Data Security" / "Regional Deployments Versus Remote Resources" / "Tenant Management"*

---

### 103. Per-Tenant Network Policies (EKS)

**Principle:** Combine Kubernetes `NetworkPolicy`, RBAC, and pod security policies for **layered tenant isolation**. No single primitive is sufficient.

**Do:**
- Default-deny ingress across namespaces.
- Default-deny egress from tenant namespaces to control-plane-only services.
- Use pod security standards for tenant pods.
- Apply NetworkPolicies via the onboarding automation.

**Don't:**
- Rely on RBAC alone — it does not restrict network traffic.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant Isolation" EKS / "Tenant Isolation in Kubernetes"*

---

### 104. Per-Tenant Service Quotas (EKS)

**Principle:** Apply per-namespace `ResourceQuota` to enforce tier-based compute ceilings.

**Do:**
- Map tier to quota profile (basic: low quota; premium: high quota).
- Apply quota via onboarding automation.
- Monitor quota usage; surface warnings to ops.
- Use LimitRange for default-tenant pod sizing.

**Don't:**
- Allow tenants to consume unbounded namespace resources.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant Isolation in Kubernetes" / resource quota context*

---

### 105. Tenant-Aware Build and Deployment Pipelines

**Principle:** CI/CD must understand your multi-tenant deployment model and the **tenant-stack-mapping table**.

**Do:**
- Treat tenant-stack-mapping as a deployable artifact.
- For each new microservice version: enumerate all target stacks from the table; deploy in waves.
- Validate the deployment by reading health per stack.

**Don't:**
- Deploy to all stacks at once in production — staged rollout exists for a reason.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Tenant-Aware Service Deployments" / "Applying tier-aware updates"*

---

### 106. Mixed Tenant-Tier Operations Dashboard

**Principle:** The operations console must show **tenant and tier views side-by-side**.

**Do:**
- Heatmaps of service health filtered by tier or tenant.
- Top-N most-active tenants with their health state.
- Tier-throughput vs SLA dashboards.
- Tenant drill-downs.

**Don't:**
- Treat tenant views as separate from operational views — they must share the same data plane.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Building a Tenant-Aware Operations Console" / "Surfacing tenant-aware operational insights"*

---

### 107. Tenant Lifecycle Audit Logging

**Principle:** Every tenant lifecycle event must be **audited** for compliance and forensic purposes.

**Do:**
- Capture: tenant created, configuration changed, tier changed, deactivated, decommissioned, data archived.
- Store audit events separately from operational metrics.
- Make audit logs immutable.
- Surface audit logs in the admin console with tenant filter.

**Don't:**
- Mutate or delete audit logs.
- Lose the chain of custody for tenant state changes.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Managing Tenant Lifecycle"*

---

### 108. Regional Failover with Tenants

**Principle:** Regional failover in a multi-tenant world must be tenant-aware to avoid cross-region data exposure.

**Do:**
- Use **regional deployment models** (full env per region).
- Pin tenant data and compute to one region; avoid cross-region read/write.
- Stage tenants across regions deliberately if you need multi-region tenancy.
- For service mesh: prefer per-region mesh deployments.

**Don't:**
- Replicate tenant data across regions without explicit consent.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Regional Deployments Versus Remote Resources"*

---

### 109. AWS Lambda Concurrency Pool Across Tiers

**Principle:** Account-wide concurrency is a **shared resource**. Tier-aware reserved concurrency is the lever to enforce tier SLAs.

**Do:**
- Reserve base concurrency for premium tier first.
- Reserve smaller slices for lower tiers.
- Use unreserved concurrency for absorbed traffic.
- Monitor account-level concurrency use and per-function utilization.

**Don't:**
- Share unlimited concurrency across tiers — basic tier will starve premium tier.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Concurrency and Noisy Neighbor"*

---

### 110. Multi-Tenant Observability Backbone (Three-Layer Model)

**Principle:** Capture telemetry at **three layers** — API, microservice, infrastructure — and join everything by `tenantId`.

**Do:**
- **API layer:** per-request metrics (latency, error rate, token use).
- **Microservice layer:** per-operation metrics keyed by tenant.
- **Infrastructure layer:** per-resource consumption tagged with tenant context (where possible).
- Use a streaming pipeline (Firehose/Kinesis) for resilience.
- Sink to a warehouse (Redshift), search (Elasticsearch), or analytics (QuickSight).

**Don't:**
- Skip per-layer instrumentation thinking microservices have it covered.
- Lose the `tenantId` correlation at any layer.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Consumption Metrics" / "A layered approach to gathering consumption metrics"*

---

### 111. RAG Onboarding Pipeline Deep-Dive

**Principle:** RAG data onboarding is a **multi-stage ETL pipeline** that creates per-tenant vector indexes.

**Do:**
- Extract: tenant data (catalogs, documents, configs).
- Transform: tokenize via the GenAI service to compute embeddings.
- Load: insert embeddings into a tenant-scoped OpenSearch index (or chosen vector store).
- Onboard as part of the standard onboarding orchestration.
- Track ETL state per tenant; surface failures.

**Don't:**
- Share embeddings indexes across tenants in regulated contexts.
- Skip tenant-side validation of embedding quality.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Create per-tenant OpenSearch indexes"*

---

### 112. Fine-Tuning Deployment Lifecycle

**Principle:** Fine-tuning creates a **logical model** per tenant. Its lifecycle must be managed like any tenant asset.

**Do:**
- During onboarding: trigger fine-tuning with tenant data.
- Store the logical model reference in Tenant Management (so invocations can resolve).
- Track fine-tuning job status (in-progress, ready, failed).
- Re-train when tenant data drifts; deprecate at decommission.

**Don't:**
- Forget fine-tuning data lifecycle when decommissioning a tenant.
- Tie fine-tuning to a specific LLM version without a re-train plan.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Supporting Tenant Refinement with Fine-Tuning"*

---

### 113. Combining RAG + Fine-Tuning — When and Why

**Principle:** Use them together when each technique targets a different dimension.

**Do:**
- RAG for fast-changing contextual data (product catalogs).
- Fine-tuning for stable behavior shaping (tone, format, domain vocabulary).
- Combine in the same invocation: augment prompt with RAG; invoke logical model with fine-tuning.
- Track both as tenant assets.

**Don't:**
- Use fine-tuning where RAG fits — fine-tuning has higher lifecycle cost.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Combining RAG and Fine-Tuning"*

---

### 114. Multi-Tenant SageMaker Inference Patterns

**Principle:** Use SageMaker's per-tenant endpoint constructs for predictable inference isolation.

**Do:**
- Provide **pooled inference endpoints** for basic tier.
- Provide **dedicated inference endpoints** for premium tier with SLAs.
- Track token/request consumption per tenant for billing.

**Don't:**
- Force all tenants onto pooled inference if SLAs require per-tenant SLAs.

*Ref: Building Multi-Tenant SaaS Architectures.md — "SaaS and AI/ML"*

---

### 115. Streaming Architecture for Multi-Tenant SaaS

**Principle:** Use streaming (Kinesis) for telemetry, billing events, and onboarding events so the system is resilient and back-pressure friendly.

**Do:**
- Stream per-tenant events into Kinesis; sinks consume at their own pace.
- Decouple metrics, billing, and operational data flows.
- Use dead-letter queues for failed events.

**Don't:**
- Block the application path on telemetry or billing writes.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Logging and Metrics with Tenant Context" / "Onboarding orchestration" (asynchronous billing integration)*

---

### 116. Quota, Rate Limiting, Burst — A Layered Approach

**Principle:** Throttling is a **defense in depth** problem. Apply limits at multiple layers.

**Do:**
- Edge: API Gateway / WAF rate limits per tenant.
- Service tier: reserved concurrency (Lambda) or ResourceQuota (K8s).
- Storage: throughput caps (DynamoDB capacity mode) per tier.
- Application: in-DAL queue limits for shared resources.

**Don't:**
- Rely on any single layer — overload conditions cascade.

*Ref: Building Multi-Tenant SaaS Architectures.md — "API Tiering" / "Concurrency" / "Storage Tiering"*

---

### 117. Tenant Onboarding Anti-Pattern: Synchronous Multi-Step Chains

**Principle:** Onboarding that waits synchronously on every external service is **slow and fragile**. Push as many steps as possible to async.

**Do:**
- Decouple billing, telemetry, and analytics from tenant activation.
- Keep only critical-path steps synchronous (tenant created, identity setup, user created).
- Use Step Functions / queues / event buses for the rest.

**Don't:**
- Wait for billing to activate a tenant — billing failures should not block activation.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Handling Onboarding Failures"*

---

### 118. Decommissioning Anti-Pattern: Synchronous Cascading Deletes

**Principle:** Decommissioning must not block other tenants' workloads.

**Do:**
- Run decommissioning as a batch at low-priority hours when possible.
- Decouple per-resource cleanup steps with retry policies.
- Surface decommission progress in the admin console.
- Allow partial decommissioning (config archive only, or storage archive only).

**Don't:**
- Run decommissioning inline at peak usage.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Decommissioning a Tenant"*

---

### 119. Validate Your Migration Plan Continually

**Principle:** Migration is iterative. Build **observable** migration runs.

**Do:**
- Tag all migrated tenants with their migration phase.
- Publish migration metrics into the operational console.
- Validate service parity after migration.
- Treat migration as a release — gated, observable, reversible.

**Don't:**
- Run silent bulk migrations.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Service-by-service migration" / "Where You Start Matters"*

---

### 120. SaaS as a Service Mindset — Wrap-up

**Principle:** The greatest insight of this book is that **SaaS is a service**. The technology (namespaces, JWTs, tiering, isolation, observability) is downstream of that mindset.

**Do:**
- Teach SaaS principles before teaching SaaS technology.
- Onboard business, product, and engineering to the SaaS mindset in parallel.
- Use the guiding principles from Chapter 17 as your north star.
- Audit your multi-tenant practices against them annually.

**Don't:**
- Skip the mindset and jump straight to architecture.

*Ref: Building Multi-Tenant SaaS Architectures.md — "Chapter 17: Guiding Principles"*

---

## Cross-References

- Related: `../Building_Microservices.md` — Service decomposition, isolation, and observability patterns
- Related: `../Designing_Distributed_Systems.md` — Deployment models, multi-region, and operational patterns
- Related: `../Cloud_Application_Architecture_Patterns.md` — Pool/silo patterns at the cloud construct level
- Related: `../Software_Architecture_Patterns.md` — Event-driven, microkernel, and other patterns relevant to multi-tenant composition
- Related: `../Observability_Engineering.md` — Tenant-aware metrics, logs, and operations
- Related: `../Engineering_Resilient_Systems_on_AWS.md` — Regional deployments, scale, and resilience patterns
- Related: `../Building_Micro-Frontends.md` — Multi-tenancy at the presentation layer (per-tenant micro-frontends)
- Related: `../Mastering_Enterprise_Platform_Engineering.md` — Multi-tenancy as a canonical platform abstraction
- Related: `../Platform_Engineering_Camille_F.md` — Tenant-aware platform engineering
- Related: `../INDEX.md` — Cross-topic best-practices index
