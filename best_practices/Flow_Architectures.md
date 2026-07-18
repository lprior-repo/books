# Flow Architectures
**Author:** James Urquhart (Global Field CTO, VMware)
**Topic tags:** `#architecture` `#concurrency` `#api`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/Flow Architectures/Flow Architectures.md` · `summaries/Flow_Architectures.md`

## TL;DR
*Flow Architectures* argues that the next generation of integration — a
World Wide Flow (WWF) analogous to the WWW — emerges when
event-driven integration, currently stuck inside single organizations, escapes
those walls via **standardized interfaces and protocols** so any producer can
publish and any authorized consumer can subscribe without per-partner
friction. Three analytical tools drive the thesis: **Wardley Mapping** to see
where each component sits on the Genesis→Custom→Product→Commodity curve,
**Promise Theory** to validate value-chain relationships between autonomous
agents, and **EventStorming + Event-First thinking + four flow patterns** to
turn the blueprint into something you can actually build.

The engineering ground floor: durable, replayable, partitioned, key-routed
event streams (Kafka, Pulsar, Kinesis) act as the queue/log; Protobuf / Avro /
JSON Schema / CloudEvents provide schema contracts; MQTT / AMQP / HTTP / WS
are today's near-Commodity transports; CNCF CloudEvents + AsyncAPI sit
between layers as the strongest candidate format; discovery (CloudEvents
Subscription API / Solace / Vantiq) is in Genesis today. Required production
properties: *security* (auth + encryption + data provenance), *agility* (loose
coupling + composability), *timeliness* (latency budget + retention window),
*memory* (replay), *manageability* (observability + circuit-breakers).

---

## Best Practices by Topic

### The Definition of Flow (and Why It's Inevitable)

**Principle:** Flow = real-time, event-driven, loosely coupled, network-scaled
integration enabled by standardized interfaces and protocols. Service /
protocol definitions: producer controls the format + transmission; consumer
controls connection lifecycle.

**Do:**
- Treat event streams as data + behavior — events are "facts", not signals
  to log into a database.
  *Ref: Flow Architectures.md — "What Is Flow?" (`page-29-0`).*
- Compose solutions from primitives with stable interfaces (Unix pipe
  analogy).
  *Ref: Flow Architectures.md — "Increasing the Flexibility of Data Flow Design" (`page-54-0`).*
- Match the integration to the user need first, then choose the technology —
  start by *finding an integration problem* before picking tools.
  *Ref: Flow Architectures.md — "Identifying Flow in Your Business" (`page-160-0`).*
- Build around the four pattern roles — **Collector**, **Distributor**,
  **Signal Processor**, **Facilitator** — with **Source**, **Processor**,
  **Queue**, **Sink** as interaction components.
  *Ref: Flow Architectures.md — "Flow Integration Components" (`page-82-0`), Tables 3-1/3-2/3-3 (`page-79-0`/`page-80-0`/`page-84-0`).*

**Don't:**
- Don't build "an entirely new architecture without a business need for it"
  — *"creating a solution looking for a problem."*
  *Ref: Flow Architectures.md — "Identifying Flow in Your Business" (`page-160-0`).*
- Don't couple producers and consumers on a synchronous request-response
  contract; flow inverts this — passive push, not active request.
  *Ref: Flow Architectures.md — "Event-Driven Communication Structures" (`page-31-0`).*

---

### The Value Chain (Wardley Mapping + Promise Theory)

**Principle:** Understand a tech landscape by:
1. *Anchor* (user need) → 2. *Position* (evolutionary stage) → 3. *Consistent
   movement* (left to right as things commodify).

**Do:**
- Place components on the four-stage scale (*Genesis → Custom → Product →
  Commodity (+utility)*) and design strategy for each.
  *Ref: Flow Architectures.md — "Determining a Measure of Technology Evolution" (`page-86-0`).*
- Use **Promise Theory** to validate the value chain: each agent only
  promises its *own* behavior (no impositions possible). Validate connections
  by asking "does the lower-level component make a useful promise to the
  higher-level one?"
  *Ref: Flow Architectures.md — "Promise Theory" (`page-72-0`).*
- Build a Wardley Map *before* committing major investment; map co-evolution
  groups (e.g., discovery may co-evolve with metadata format).
  *Ref: Flow Architectures.md — "Mapping the Evolution to Flow" (`page-120-0`).*
- Apply Geoffrey West's *Scale*: highly localized edge flows feed
  increasingly aggregated central flows; structure is "leaf, branch, limb,
  trunk." Don't centralize everything.
  *Ref: Flow Architectures.md — "Flow and Scale" (`page-69-0`), "Distributed control" (`page-168-0`).*

---

### Streaming / Queue Components

**Principle:** Use append-only **durable, replayable, partitioned, ordered
logs** (not queues) for flow's queue/log role. Multiple consumers can
read different offsets of the same topic simultaneously.

**Do:**
- Choose Kafka, Pulsar, or a managed equivalent (AWS Kinesis, Azure Event
  Hubs, Confluent Cloud) as the substrate.
  *Ref: Flow Architectures.md — "Log-based Streaming Platforms (Apache Kafka, Apache Pulsar, AWS Kinesis...)" (`page-231-0`).*
- Partition topics by entity key for ordering + horizontal parallelism;
  consumer groups spread work across instances; each consumer manages its
  own offset.
  *Ref: Flow Architectures.md — "Consuming from the Immutable Log" / "Log-Based Stream Processing" (`page-108-0`).*
- Combine topics with **changelogs** for stateful processor recovery.
  *Ref: Flow Architectures.md — "Log-Based Stream Processing Platforms" (`page-111-0`).*
- Use log-based platforms for "event series" use cases where sequence and
  replay matter; LinkedIn runs > 7 trillion messages/day through Kafka.
  *Ref: Flow Architectures.md — "Processing series of events" (`page-183-0`).*
- Deploy producers as **serverless / FaaS** (Lambda, Azure Functions)
  triggered by event sources — no servers to operate, pay per execution.
  *Ref: Flow Architectures.md — "Functions, Low-Code, and No-Code Processors" (`page-109-0`).*

**Don't:**
- Don't repurpose a *queue* (RabbitMQ, ActiveMQ) as the substrate for
  large-scale flow; queues delete events after ack and don't allow multiple
  independent consumers to read the same offset range.
  *Ref: Flow Architectures.md — "Queue/Log" (`page-228-0`).*

---

### Connection / Transport

**Principle:** Use commodity internet transports today (HTTP/2, WebSocket,
MQTT, AMQP, gRPC, QUIC). Flow will be "carried by" these; flow-specific
protocols are CloudEvents bindings on top.

**Do:**
- Use HTTPS or WSS for connection-level security; encrypt payloads
  independently if data is sensitive.
  *Ref: Flow Architectures.md — "Connection security" (`page-135-0`).*
- For IoT / constrained devices, use **MQTT** — three QoS levels,
  lightweight, OASIS standard.
  *Ref: Flow Architectures.md — "MQTT" (`page-79-0`).*
- For inter-org business messaging with channel/transaction semantics, use
  **AMQP**.
  *Ref: Flow Architectures.md — "AMQP" (`page-214-0`).*
- For 1:1 long-lived bi-directional connections over HTTP infra, use
  **WebSocket**.
  *Ref: Flow Architectures.md — "WebSockets" (`page-215-0`).*
- QUIC under HTTP/3 enables parallel streams over multiple connections —
  adopted for streaming and HTTP/3.
  *Ref: Flow Architectures.md — "TCP, QUIC" (`page-205-0`).*

---

### Interface & Protocol (Discovery + Subscription)

**Principle:** A flow interface is *location + initiation*; a flow protocol is
*packaging + transmission*. CloudEvents' spec achieves both — metadata via
the spec, payload via binding-defined mode (structured-JSON or binary).

**Do:**
- Use **CNCF CloudEvents** for event metadata. Example (v1.0 JSON):
  ```json
  {
    "specversion": "1.x-wip",
    "type": "com.github.pull_request.opened",
    "source": "https://github.com/cloudevents/spec/pull",
    "subject": "123",
    "id": "A234-1234-1234",
    "time": "2018-04-05T17:31:00Z",
    "datacontenttype": "text/xml",
    "data": "<much wow=\"xml\"/>"
  }
  ```
  *Ref: Flow Architectures.md — "CloudEvents" (`page-209-0`).*
- Look at the **CloudEvents Subscription API** as the emerging flow interface.
  *Ref: Flow Architectures.md — "CNCF Cloud Events Subscription API" (`page-206-0`).*
- For "URL = topic" simplicity, study **NATS NGS** / **NATS subject strings**
  — "Why can't it be this simple?"
  ```text
  SUB foo.bar 90
  PUB foo.bar 5 Hello
  MSG foo.bar 90 5 Hello
  ```
  *Ref: Flow Architectures.md — "NATS Client Protocol" (`page-211-0`).*
- Treat metadata format (CloudEvents) and payload format as separate
  concerns. Payload stays opaque-binary for now — common formats will emerge
  per industry.
  *Ref: Flow Architectures.md — "A known and predictable protocol" (`page-140-0`).*

**Don't:**
- Don't try to standardize every flow payload type upfront — *"in the long
  term, ... most industries and governments will define or reuse common
  payload standards for most common streaming use cases. What exactly those
  standard formats will be, however, is impossible to predict."*
  *Ref: Flow Architectures.md — "A known and predictable protocol" (`page-140-0`).*

### Discovery

**Principle:** Discovery is in **Genesis** today. Most producers solve this
with a documentation page (or no solution at all).

**Do:**
- For now, expose a discovery web page (GitHub README works); search
  engines will index it. "Incredibly consistent with the way the API economy
  has evolved to date. There is no central repository or website with a list
  of available APIs across the internet."
  *Ref: Flow Architectures.md — "Discovery > Search Engines and Web Pages" (`page-217-0`).*
- Watch the CloudEvents Subscription/Discovery working group as the
  consensus emerges.

**Don't:**
- Don't build a "Google for event streams" today — there are too few
  streams to justify the *company*.

---

### Producer / Consumer / Processor Patterns

**Principle:** Producer controls format + transmission; consumer controls
connection + lifecycle. Pick **eventing** (one-way, fire-and-forget) over
*messaging* (request-response / interactive) where possible — lower-coupling
= more network effects.

**Do:**
- Use **streaming SQL** for cross-stream joins + stateful aggregations
  (ksqlDB / Flink SQL).
  *Ref: Flow Architectures.md — "Observations on log-based" (`page-227-0`).*
- Distinguish *Eventing* (one-way facts) from *Messaging* (interactive
  coordination) — *eventing is the preferential way to build for flow*.
  *Ref: Flow Architectures.md — "Messaging Versus Eventing" (`page-176-0`).*
- For high-volume data stream processing with state (digital twins, traffic
  optimization), consider **stateful stream processors** (Swim.ai style)
  over pipeline-style (Flink/Spark).
  *Ref: Flow Architectures.md — "Stateful Stream Processing" (`page-87-0`).*
- For "single-action" reactions to discrete events, use FaaS with event
  triggers (Lambda, Azure Event Grid → Logic Apps, AWS EventBridge
  → Step Functions).
  *Ref: Flow Architectures.md — "Single Actions Versus Workflows" (`page-184-0`).*
- For "workflow" reactions, use a workflow engine (Step Functions, Logic
  Apps, Argo) so the process is decoupled from apps and services.
  *Ref: Flow Architectures.md — "Single Actions Versus Workflows" (`page-184-0`).*
- For *event series* (stock ticker, climate, health-monitoring) where
  history matters as much as the latest event, use log-based processors.
  *Ref: Flow Architectures.md — "Series events" (`page-182-0`).*

---

### Use-Case Categorization

**Principle:** All streaming systems fall into Derek Collison's four
categories — *Addressing & Discovery*, *Command & Control*, *Query &
Observability*, *Telemetry & Analytics*.

**Do:**
- *Addressing & discovery* — registration services + bounded topic
  cardinality; watch for duplicate discovery (must be idempotent).
  *Ref: Flow Architectures.md — "Addressing and discovery" (`page-163-0`).*
- *Command & control* — centralize or distribute at the edge depending on
  scale; collect local aggregates before flowing to core.
  *Ref: Flow Architectures.md — "Command and control" (`page-165-0`).*
- *Query & observability* — sort upstream by subject / geography for targeted
  topics vs. let consumer filter downstream; pick the balance.
  *Ref: Flow Architectures.md — "Query and observability" (`page-169-0`).*
- *Telemetry & analytics* — RUM-style data product within seconds (vs
  24-hr batch overnight) is the differentiator.
  *Ref: Flow Architectures.md — "Telemetry and analytics" (`page-171-0`).*

---

### Composability Over Context

**Principle:** Build like Unix pipes — small, composable primitives with
common interfaces — not like the contextual plug-in model (Maven, Access)
that locks users into rigid extension points.

**Do:**
- "Compose some or all of a solution from known building blocks, using
  known interfaces to connect the parts together."
  *Ref: Flow Architectures.md — "Agility / Loosely coupled interfaces" (`page-138-0`).*
- Use **Deitzler's Law** as a heuristic — every tool "hits the wall" when
  10–20% of what users want is impossible within the tool's constraints.

**Don't:**
- Don't pick integration platforms that "only allow modification and
  extension in certain contexts."
  *Ref: Flow Architectures.md — "Composability vs Contextual" (`page-114-0`).*

---

### Composability-of-Flow Patterns (4)

**Principle:** The four named flow patterns are *Collector*, *Distributor*,
*Signal Processor*, *Facilitator*. Map your integration to one of these
before designing.

**Do:**
- **Collector** — one consumer subscribes to many producers; consistent
  URI everywhere (e.g., a tax-collection endpoint). Watch scaling.
  *Ref: Flow Architectures.md — "The Collector Pattern" (`page-153-0`).*
- **Distributor** — one producer → many consumers (WeatherFlow,
  market-ticker). Use **edge computing** to bring endpoints close to
  consumers; partition by region to keep RTT honest.
  *Ref: Flow Architectures.md — "The Distributor Pattern" (`page-154-0`).*
- **Signal Processor** — traffic-cop pattern; large, complex central
  systems were the downfall of ESBs; favor *distributed* (edge + local
  aggregate) over centralized.
  *Ref: Flow Architectures.md — "The Signal Pattern" (`page-156-0`).*
- **Facilitator** — broker matching (Uber, AdWords). At scale, expect
  middlepersons to be some of the biggest wealth generators.
  *Ref: Flow Architectures.md — "The Facilitator Pattern" (`page-157-0`).*

---

### Modeling Flow (EventStorming)

**Principle:** EventStorming maps a complex business process to events on a
timeline, exposing hidden cross-team integration points.

**Do — the 7-step process:**
- 1. Identify the business activity to model.
- 2. Reserve a long wall / Miro canvas.
- 3. Invite business leaders + SMEs + BAs + architects + UX.
- 4. Brainstorm events (orange stickies) — "what activity signals a step?"
- 5. Lay out on a timeline.
- 6. Capture actors (yellow), external systems (pink), commands, policies
  (purple), outputs.
- 7. Highlight constraints / hot-pink stickies for current issues.
  *Ref: Flow Architectures.md — "Modeling Flow" (`page-173-0`).*

**Don't:**
- Don't conflate **messaging** (interactive coordination) with **eventing**
  (one-way facts) — different architectures.
  *Ref: Flow Architectures.md — "Messaging Versus Eventing" (`page-152-0`).*

---

### Required Properties for Flow (Security, Agility, Timeliness, Memory, Manageability)

**Principle:** Five properties must be met before flow can support real
business value. Bake them in from day one.

**Do — Security:**
- Plan for **end-to-end encryption** (TLS for transport + payload
  encryption for sensitive fields). CNCF CloudEvents "strongly suggests
  payloads be encrypted, though today the method of encryption and exchange
  of required keys or certificates is not a part of the specification."
  *Ref: Flow Architectures.md — "Encryption" (`page-133-0`).*
- Address **data provenance** (immutable verification values + ledger-based
  audit trails / blockchain-class). 'One of the next billion-dollar startups...
  will be the company that solves maintaining data provenance in a high-volume,
  rapidly changing environment like the WWF.'
  *Ref: Flow Architectures.md — "Data provenance" (`page-137-0`).*
- Plan ahead for **state-driven connection security** (X.509 certs between
  brokers and clients even when TLS is unavailable).

**Do — Agility:**
- Loosely coupled interfaces + known-and-predictable protocols.
  *Ref: Flow Architectures.md — "Agility" (`page-116-0`).*

**Do — Timeliness:**
- Set a **performance budget** per processing step (web-pattern).
- Place processing close to consumers via **edge computing**; let edge
  aggregate into central flows (the allometric-scaling pattern).
  *Ref: Flow Architectures.md — "Latency" (`page-142-0`).*
- For high-throughput localized coordination, put a localized message bus at
  the edge.
  *Ref: Flow Architectures.md — "Distributed control" (`page-165-0`).*
- Document event **retention** per producer; specify in the schema/metadata so
  consumers know the replay window.

**Do — Memory:**
- Allow producers to advertise retention; consumers can request ranges;
  immutable log + changelogs covers most cases.
  *Ref: Flow Architectures.md — "Memory" (`page-125-0`).*

**Do — Manageability:**
- Add **circuit breakers** between actors to break feedback loops
  (post-2010 Flash Crash lesson: "A great example of circular dependencies
  comes from the US stock market").
  *Ref: Flow Architectures.md — "Controllability" (`page-147-0`).*
- Make consumers resilient to "known categories of problems" — unknown
  failure shapes will surface; build observability around available signals.
  *Ref: Flow Architectures.md — "The Signal Pattern" (`page-156-0`).*

**Don't:**
- Don't promise *more* than you deliver between parties —
  each agent should promise only what it controls (Promise Theory).
  *Ref: Flow Architectures.md — "Promise Theory" (`page-72-0`).*

---

### Standards & Open-Source Strategy

**Principle:** No single body can *impose* a flow standard. Standards
emerge from running code + market acceptance. Multiple specs will matter.

**Do:**
- Track / participate in IETF (TLS, WebSocket, HTTP/3), OASIS (MQTT,
  AMQP), CNCF (CloudEvents, NATS, Knative), Apache Foundation (Kafka,
  Pulsar, Beam, Flink, Storm, Druid).
  *Ref: Flow Architectures.md — "Standards bodies" (`page-187-0`), "Open source projects" (`page-188-0`).*
- Stand up trade-group-level coordination in your industry — *"There may be
  opportunities for those that do not belong to trade groups to create a new
  organization with flow standards in mind."*
  *Ref: Flow Architectures.md — "Trade groups" (`page-191-0`).*
- Pick ecosystem-friendly tech (e.g., AWS AMIs, Docker/OCI images,
  EventBridge event format) so vendors can build on your conventions
  cheaply.
  *Ref: Flow Architectures.md — "Ecosystem partnerships" (`page-192-0`).*

**Don't:**
- Don't burn the only-organic-growth lesson: standards imposed rather
  than adopted get the no-adoption penalty.

---

### Vendor Inertia & Enterprise Inertia (Patterns to Break)

**Principle:** Recognize inertia phases. Two-to-three year enterprise
adoption timeline is the standard pattern (year 1 explore, year 2
prototype/first rollout, year 3 scale).

**Do:**
- Start with **greenfield projects** to demonstrate flow value before
  migrating existing integrations.
  *Ref: Flow Architectures.md — "Starting with greenfield projects" (`page-104-0`).*
- Build **bridges and adapters** to legacy systems.
  *Ref: Flow Architectures.md — "Enterprise Inertia" (`page-104-0`).*
- Pursue the *Standards Game* aggressively — open standards commoditize
  vendor lock-in.
  *Ref: Flow Architectures.md — "Market: Standards Game" (`page-123-0`).*
- Exploit network effects — "Make sure you are positioned as an early
  player in relevant standards as flow emerges."
  *Ref: Flow Architectures.md — "Accelerators: Exploiting Network Effects" (`page-124-0`).*

---

### Streaming SQL / Stateful Stream Processing

**Principle:** Streaming SQL (ksqlDB, Flink SQL) + stateful stream
processors (Swim.ai) are rising abstractions over raw log consumers.

**Do:**
- Adopt streaming SQL for cross-stream joins and aggregations — "ksqlDB
  ... connects directly to Kafka topics and enables you to formulate your
  queries about event series in familiar SQL syntax."
  *Ref: Flow Architectures.md — "ksqlDB" (`page-182-0`).*
- Use a stateful processor when real-time decisions depend on the current
  state of a graph of related entities (digital twins).
  *Ref: Flow Architectures.md — "Stateful Stream Processing" (`page-87-0`).*

---

### Composability Patterns and Pitfalls

**Principle:** Many of today's "integration platforms" (Service Bus,
MuleSoft, Dell Boomi) are *contextual* and constrain what developers can
build. Flow is composable.

**Do:**
- Use Kafka Connect source/sink connectors to integrate with commercial
  apps (Salesforce, Splunk, JIRA, Zendesk, Reddit) — proves demand.
  *Ref: Flow Architectures.md — "Confluent Kafka Connectors" (`page-231-0`).*
- For serverless glue: AWS Lambda + EventBridge + Step Functions / Knative
  Eventing + Argo.
  *Ref: Flow Architectures.md — "Knative Eventing" / "AWS Step Functions" (`page-185-0`/`page-184-0`).*

**Don't:**
- Don't build a closed, "single pane of glass" control plane for distributed
  processors — failures will be local; decision-making must be local.
  *Ref: Flow Architectures.md — "The Signal Pattern" (`page-156-0`).*

---

## Anti-Patterns & Common Mistakes
- **Closed event APIs with per-partner SDKs.** *fix:* push metadata format
  toward CloudEvents and require an HTTP/WebSocket/MQTT/AMQP binding; any
  compliant consumer should be able to read metadata. *Ref: Flow Architectures.md — "Composability vs Contextual" (`page-114-0`).*
- **Producer-knows-consumer coupling** (Twitter-style negotiated
  connections) for the open WWF. *fix:* a connection paradigm where
  consumer initiates and producer accepts/rejects; producer does not know
  consumer ahead of time. *Ref: Flow Architectures.md — "What is Flow?" (`page-29-0`).*
- **Synchronous messaging pretending to be events.** *fix:* if both sides
  need conversation, use messaging (RPC/Kafka request-reply); otherwise
  prefer loosely-coupled eventing. *Ref: Flow Architectures.md — "Messaging Versus Eventing" (`page-176-0`).*
- **Centralized event-router for very-large-scale use.** *fix:* distributed
  controllers at the edge, aggregate to central.
- **Treating events as temporary pointers** — *"events are not messages …
  events carry data, not just 'something happened.'"*
- **Single pane-of-glass management of distributed stateful
  processors.** *fix:* let each agent manage its own state; expose
  via signal events.
- **Batch-only analytics on a stream you could compute in seconds.**
  *fix:* RUM-style streaming analytics closes the campaign-feedback loop
  faster.
- **Promising cross-boundary guarantees between parties that don't control
  each other.** *fix:* Promise Theory — each agent promises only itself.

---

## Decision Heuristics / Checklists
- **Single tech team can't decide alone on a stream substrate?** Choose
  managed (Confluent Cloud, MSK, Azure Event Hubs Premium) so the
  commodity/utility tier is owned by the platform vendor.
- **Customer-facing real-time?** Use FaaS + push event triggers; stream
  analytics within ~10 s. *Ref: Flow Architectures.md — "Telemetry and analytics" (`page-171-0`).*
- **Command & control of physical or low-latency devices?** MQTT +
  stateful stream processor at the edge.
- **Cross-org business partner?** Async eventing via CloudEvents +
  HTTP/WebSocket, with a discovery page.
- **Workflow with human steps or long-running compensations?** Workflow
  engine (Step Functions, Logic Apps, Argo) on top of events, not instead
  of events.
- **Need data audit / chain-of-evidence?** Ledger or hash-chain
  provenance from day one.
- **Many small domains with overlapping events?** Use one of the four flow
  patterns (Collector / Distributor / Signal Processor / Facilitator)
  explicitly — name it, then build.

---

## Key Takeaways
1. **Adopt event-first thinking today**, even if cross-org flow is 5–10
   years out — each bit of state change you treat as an event becomes
   fodder for future flow.
2. **Build like Unix pipes** — small composable primitives behind stable
   interfaces. Avoid contextual / plug-in architectures.
3. **Today the substrate is real** — Kafka / Pulsar / Kinesis / Event Hubs
   / Pub/Sub; MQTT / AMQP / HTTP / WebSocket; CloudEvents metadata;
   FaaS for processing.
4. **Tomorrow's gap is five properties**: security (encryption +
   provenance), agility (loose coupling + composability), timeliness
   (latency budget + retention), memory (replay), manageability
   (observability + circuit breakers). Build them into your platform from
   the start.
5. **Standards are emergent** — contribute to existing efforts
   (CNCF/IETF/OASIS/Apache) before inventing new ones.
6. **Pattern your integration by role** — Collector, Distributor, Signal
   Processor, Facilitator — and by Collison's four use-case categories.
7. **Use EventStorming + Event-First + structured Eventing** to drive
   decomposition; use Messaging only when conversations are required.
8. **Edge + center scaling** beats pure-central for very large scale:
   local compute + bus, aggregate into bigger flows, repeat.
9. **Compose, don't centralize management** — distributed agents must
   own their own state; failures are local.
10. **Drive network effects** — be an early player in standards, publish
    your own streams, lower the cost of integration to build momentum.

---

## Cross-References
- Related: `../Building_Event-driven_Microservices.md` (the in-organization
  layer flow enables).
- Related: `../Building_An_Event-Driven_Data_Mesh.md` (data product design
  patterns that flow will externalize).
- Related: `../Monolith_To_Microservices.md` (organizations extract data
  products as they migrate, seeding the supply side of flow).
- Related: `../Microservices_Up_And_Running.md` (operationally running the
  edge services and event recipients that flow depends on).
- Topic index: `../INDEX.md`
