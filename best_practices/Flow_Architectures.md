# Per-Book Best Practices — Deep Dive
> Exhaustive source-bound extraction of principles, do/don't guidance,
> anti-patterns, named technologies, case studies, and verbatim snippets.
---
# Flow Architectures
**Author:** James Urquhart
**Topic tags:** `#architecture` `#concurrency` `#api`
**Language focus:** Language-agnostic distributed systems and integration
**Sources:** `markdown_output/Flow Architectures/Flow Architectures.md` · `summaries/Flow_Architectures.md`
## TL;DR
*Flow Architectures* defines flow as networked software integration that is event-driven, loosely coupled, highly adaptable, and enabled by standard interfaces and protocols.
Its World Wide Flow thesis predicts that cheap, self-service exchange of timely events across organizational boundaries will link the world's activity as the World Wide Web linked information.
Use Wardley Mapping to locate each flow component on the Genesis → Custom built → Product → Commodity/Utility path, and use Mark Burgess's Promise Theory to validate what autonomous components can actually promise one another.
Build event-first systems now, but do not claim that a complete flow standard exists: the book treats common interfaces, payload standards, discovery, provenance, and end-to-end security as unfinished work.
### Source-fidelity boundary
- Treat this document as an extraction from the named book, not as a current market survey.
- Preserve the book's 2021 market snapshot and speculative framing.
- The book discusses JSON as CloudEvents' structured representation, opaque binary payloads, schemas, and schema registries.
- The book does **not** name Protocol Buffers, Avro, or JSON Schema as flow payload-contract choices.
- The book does **not** discuss AsyncAPI or Materialize.
- The book mentions gRPC only as an increasingly popular RPC framework that might influence a future flow interface.
- The book does **not** provide a gRPC-streaming design.
- The book discusses cellular protocols, telecom points of presence, and edge computing, but does **not** provide a 5G-specific architecture.
- Do not attribute modern products, guarantees, or standards absent from the source to Urquhart.
- Use the source's concepts—metadata, payload formats, discovery, delivery promises, latency, retention, and flow control—when evaluating those later technologies independently.
---
## Best Practices by Topic
### 1. Define Flow by Its Operating Contract
**Principle:** Define flow as networked integration that is event-driven, loosely coupled, adaptable, extensible, and standardized at the interface and protocol boundaries.
**Do:**
- Let consumers or their agents request streams through self-service interfaces.
- Let producers or their agents accept or reject stream requests.
- Push information after connection establishment instead of requiring repeated requests.
- Let producers control what information is transmitted, when it is transmitted, and to whom.
- Carry information over standard network protocols.
- Separate the connection interface from the data-exchange protocol.
- Treat producer and consumer agents as legitimate architectural participants.
- Allow agents to perform policy management, network optimization, routing, or telemetry.
- Keep producers unaware of consumers before subscription whenever the use case permits.
- Let consumers locate and request independently operated streams.
- Minimize coordinated setup between organizations.
- Make connection creation and closure predictable.
- Ensure one consumer's connection activity does not impair producer operation.
- Optimize for asynchronous interaction across organizational boundaries.
- Preserve producer control over formats, protocols, and sharing policies.
**Don't:**
- Don't call every network data exchange flow.
- Don't call batch file transfer flow merely because files cross a network.
- Don't call ordinary synchronous request-response flow.
- Don't require consumers to poll continuously for state changes when push is viable.
- Don't require producers to know every consumer in advance.
- Don't equate moving data with creating value.
- Don't omit the software that prepares, processes, consumes, or acts on streams.
- Don't claim a universally accepted flow standard exists in the book's market snapshot.
**Five defining properties:**
1. Consumers or their agents request streams through self-service interfaces.
2. Producers or their agents choose which requests to accept or reject.
3. Consumers need not actively request information after connection; producers push it as available.
4. Producers or their agents maintain transmission control.
5. Standard network protocols carry the information.
**Architectural test:**
- Ask whether the consumer can discover, connect, receive, and disconnect without bespoke bilateral engineering.
- Ask whether the producer remains autonomous after a consumer joins or leaves.
- Ask whether an agreed interface starts the relationship and an agreed protocol carries the stream.
- Reject the flow label if these properties do not substantially hold.
*Ref: Flow Architectures.md — "What Is Flow?"; "Flow and Integration"*
---
### 2. Turn State Changes into Contextual Events
**Principle:** Package a state change with enough context to make it an event; transmit a sequence of such events as an event stream.
**Do:**
- Identify the state change first.
- Add contextual data such as occurrence time and the identity of what changed.
- Publish the packaged state change for eventual consumption.
- Preserve event context as the event crosses processors and organizational boundaries.
- Give consumers enough metadata to determine how to interpret the payload.
- Prefer event streams for cross-organizational integration.
- Distinguish the event source from the eventual producer-facing interface.
- Treat an event stream as a series of contextual state-change records.
- Include context with each event when routing may send it through multiple processors.
- Let common metadata describe payload type, source, encoding, and other interpretation needs.
**Don't:**
- Don't force consumers to infer all context from a connection endpoint.
- Don't make consumers inspect camera images or sensor bytes merely to identify origin.
- Don't substitute the consumer's clock for the actual occurrence time when the producer can supply it.
- Don't assume raw bytes are self-describing.
- Don't confuse an event with the payload alone.
- Don't confuse an event stream with an unframed raw data stream.
- Don't require knowledge of producer internals to understand an event.
**Raw-stream contrast:**
- A raw stream sends each piece of data without contextual packaging.
- A raw-stream consumer must add context from source knowledge, payload clues, or its own clock.
- An event stream packages state-change data and context together.
- Context reduces the consumer's interpretation work.
- The book allows that flow could carry raw streams, but predicts events will dominate cross-organizational flow.
**Decision test:**
- Use a raw stream only when both sides deliberately share stable out-of-band context.
- Use an event stream when independent consumers, routing, replay, or cross-organization use matters.
- Make context durable enough to survive handoffs.
*Ref: Flow Architectures.md — "What Is Flow?"; Figure 1-1 "An event stream versus a raw data stream"*
---
### 3. Use the World Wide Flow Thesis as a Direction, Not a Deployed Standard
**Principle:** Treat the World Wide Flow as a forecast of a global activity graph created when low-cost standards make authorized event streams easy to publish, discover, combine, and consume.
**Do:**
- Compare the WWF to the Web carefully: the Web links knowledge; the WWF links activity.
- Expect the Web and WWF to be intertwined rather than mutually exclusive.
- Design for a growing graph of sources, processors, streams, and consumers.
- Expect low integration cost to increase experimentation.
- Expect new combinations of streams to expose previously uneconomic services.
- Treat real-time institutional cooperation as the central thesis.
- Design authorization and producer control into the activity graph.
- Expect standards to reduce plumbing work, not eliminate domain processing.
- Prepare for automation from individual scale through global institutions.
- Preserve flexibility because the book's future scenarios are intentionally speculative.
**Don't:**
- Don't present the fictional Internet Event Flow Suite as an existing standard.
- Don't present the fictional Event Metadata Protocol or Event Subscription Interface as deployed technology.
- Don't confuse the WWF forecast with a guarantee about a particular protocol winner.
- Don't assume all consequences will be beneficial.
- Don't centralize the entire WWF under one operator.
- Don't ignore regulation, privacy, abuse, employment disruption, or surveillance.
**Fictional finance cases:**
- Real-Time Economy reports key economic data in near real time.
- Banks consume those signals to adjust risk analysis.
- Standardized market feeds reduce access and processing costs.
- Lower trading costs attract hobbyist and algorithmic trading.
- The fictional Komputrade Crash warns that automated feedback can destabilize markets.
- The fictional Neuroquity acquisition illustrates exceptional winners created by stream-based models.
**Fictional retail cases:**
- Standard inventory events synchronize retailers and suppliers.
- Consolidated inventory services become products.
- AnyRent/RentAll creates a rental marketplace without owning inventory.
- Personal shopping assistants combine location, inventory, and customer context.
- Smart appliances and packaging contribute to grocery planning.
- Delivery routes react to traffic events.
- Past streams provide memory for current recommendations.
**Fictional transportation cases:**
- Tesla SelfCharging combines vehicle state, charger availability, robotics, and cloud coordination.
- LoadLeader matches spare cargo capacity with partial loads.
- Matching efficiency turns load scheduling toward utility status.
- Standard interfaces let specialized shipping services emerge.
- Real-time event exchange enables new participants to join the logistics ecosystem.
**Fictional health-care cases:**
- Fitness-device events feed patient and physician views.
- Independent personal health records collect data from institutions and personal sources.
- First-responder and 911 streams improve emergency-room planning.
- Smart cabinets trigger supply ordering.
- Prescription streams improve local pharmacy planning.
- Drug-efficacy streams support earlier adverse-reaction detection.
- Personal control, consent, and authorization remain essential.
**Fictional data-service case:**
- WeatherFlow combines more than a million weather stations and sensors.
- Regional analysis centers process and distribute weather observations.
- Transportation and logistics consume timely weather streams.
- Consumer applications add value to the same stream.
- The case illustrates Distributor scale, regionalization, and ecosystem effects.
**Negative cases and constraints:**
- Automation can displace clerical work.
- Security flaws create new interception and alteration opportunities.
- Strong stream security can also make illicit streams harder to detect.
- Governments can use flow for surveillance and policy enforcement.
- Advertising and subscription models can constrain access.
- Network neutrality and tiered traffic pricing can shape the ecosystem.
- Institutional and social adaptation will lag technical feasibility.
*Ref: Flow Architectures.md — "The 10-Year Impact of the World Wide Flow"; "The Future of the WWF"; "Flow and Integration"*
---
### 4. Start with Business Urgency, Not Architecture Fashion
**Principle:** Adopt flow only where timely event exchange improves customer experience, organizational efficiency, or innovation enough to justify change.
**Do:**
- Identify a real pain point before selecting event-driven integration.
- Quantify the value of more timely state changes.
- Look for inconsistent customer experiences caused by stale cross-system data.
- Look for process queues waiting on external signals.
- Look for decisions that lose value as data ages.
- Look for integrations whose bespoke plumbing blocks experimentation.
- Tie architecture to cost, revenue, mission, regulation, or competitive pressure.
- Ask whether lower integration cost changes the economics of the use case.
- Include businesses, governments, nonprofits, academic institutions, and individuals in the analysis.
- Make urgency visible to decision makers.
- Separate required adaptation from true innovation.
- Prefer projects that enable new value, not merely technology replacement.
**Don't:**
- Don't build a new flow architecture without a business need.
- Don't tell the technology story before identifying why users care.
- Don't treat digital transformation as innovation by default.
- Don't assume faster data always creates enough value.
- Don't ignore privacy costs while improving personalization.
- Don't assume an external real-time integration is affordable merely because an internal prototype is.
- Don't use speculative WWF benefits as the sole business case.
**Customer-experience test:**
- Require state changes in one business unit to become visible to relevant units quickly.
- Use timely updates to preserve trust in financial or account views.
- Use current context to personalize subsequent interactions.
- Evaluate the cost of inconsistency as lost business, trust, or mission impact.
**Business-case questions:**
- What decision becomes better?
- What waiting time disappears?
- What manual coordination disappears?
- What new experiment becomes cheap enough to run?
- What external data source becomes usable?
- What new ecosystem participant can add value?
*Ref: Flow Architectures.md — "The Business Case for Flow"; "Drivers for Flow Adoption"; "Improving Customer Experience"*
---
### 5. Use Value Stream Mapping to Find Event Opportunities
**Principle:** Find the dominant process constraint, then use timely signals and automation to reduce lead time or process time at that constraint.
**Do:**
- Follow a work element from process start to finish.
- Measure lead time at every queue.
- Measure process time at every work step.
- Record both measures in a value stream map.
- Identify the largest current constraint.
- Improve the constraint before optimizing less limiting steps.
- Ask what signal tells software that work is ready.
- Ask what data software needs to process the work.
- Use event-driven integration to remove notification delay.
- Use automation to prioritize work consistently.
- Use open interfaces and protocols as pre-negotiated integration options.
- Recalculate the constraint after each improvement.
**Don't:**
- Don't optimize nonconstraints while the main bottleneck dominates throughput.
- Don't count waiting as valuable work.
- Don't automate a step without assuring required data is available.
- Don't preserve overnight handoffs when an event can trigger immediate action.
- Don't assume rules engines or machine learning can act without timely inputs.
- Don't hide cross-organizational negotiation time from the lead-time measure.
- Don't confuse faster processing with faster end-to-end flow.
**Lead-time guidance:**
- Signal work as soon as it becomes actionable.
- Route urgent work before standard work when rules are stable.
- Keep software available beyond human working hours where the service commitment requires it.
- Use interoperability to remove bespoke connection negotiation.
- Treat lower connection cost as an enabler of more automation.
**Process-time guidance:**
- Make all required data available to the processing function.
- Expect data sources and business rules to change.
- Standardize connection, flow control, metadata interpretation, and source context.
- Limit custom work to domain payload interpretation where possible.
- Preserve the ability to experiment with new sources.
*Ref: Flow Architectures.md — "Improved Organizational Efficiency"; "Value stream mapping"; "Eliminating lead time"; "Eliminating process time"*
---
### 6. Design for Network Effects and the Jevons Paradox
**Principle:** Expect cheaper integration to increase total stream-processing demand, participants, traffic, and experiments rather than merely reduce the current bill.
**Do:**
- Standardize tools and methods to reduce per-integration work.
- Grow the pool of people able to build stream integrations.
- Exploit economies of scale in creation, transmission, and consumption.
- Track demand growth after lowering connection friction.
- Plan capacity for new use cases, not only existing streams.
- Enable producers and consumers to attract one another.
- Make valuable streams easy to find and combine.
- Focus developer work on domain logic instead of protocol plumbing.
- Expect programming libraries and platforms to internalize flow mechanisms over time.
- Use pay-for-use services where event volume is uncertain and operations toil is material.
- Evaluate cost across the whole value stream.
- Include network, development, testing, operations, intermediaries, and storage.
**Don't:**
- Don't forecast total integration spend to fall in proportion to unit cost.
- Don't size the platform only for today's traffic.
- Don't treat a lower-cost event as a reason to retain every event forever.
- Don't assume an ecosystem appears without useful streams.
- Don't assume useful streams attract consumers without discoverability.
- Don't optimize only compute cost while ignoring labor and connection negotiation.
- Don't confuse cloud billing convenience with an open flow ecosystem.
**Three cost reducers named by the book:**
1. Standard tools and methods.
2. A larger labor pool capable of integrating streams.
3. Economies of scale created by network effects.
**Jevons-paradox application:**
- More efficient steam engines increased total coal consumption.
- More efficient flow integration can increase total integration volume.
- Standard interfaces and protocols are the proposed efficiency mechanism.
- New uses consume the saved capacity and budget.
- Increased demand attracts new vendors and further optimization.
**Cost questions:**
- What is the cost to connect?
- What is the cost to interpret the payload?
- What is the cost to operate the stream?
- What is the cost to retain and replay it?
- What is the cost to secure and govern it?
- What new volume appears when those costs fall?
*Ref: Flow Architectures.md — "Lowering the Cost of Stream Processing"; "Innovation and Experimentation"; "Creating the Great Flow Ecosystem"*
---
### 7. Prefer Composable, Interoperable Building Blocks
**Principle:** Favor small components connected through common interfaces and protocols over contextual platforms that only allow extension in vendor-selected places.
**Do:**
- Hide component internals behind loosely coupled interfaces.
- Let components evolve on their own schedules.
- Connect fine-grained parts through stable exchange mechanisms.
- Use common metadata so arbitrary compliant consumers can inspect an event.
- Let producers select payload formats while advertising them clearly.
- Standardize common payload types at industry level when adoption justifies it.
- Preserve the ability to reorder, replace, or extend processing steps.
- Use interoperability to connect tools not explicitly designed together.
- Test whether a tool permits unanticipated compositions.
- Keep contextual platforms where their predefined workflows fit the whole need.
- Mix low-code productivity with extensible code where necessary.
**Don't:**
- Don't mistake a large connector catalog for universal composability.
- Don't let a tool's built-in abstractions block the final required behavior.
- Don't hardwire every producer to every consumer.
- Don't require coordinated redeployment for internal changes hidden behind an interface.
- Don't assume one payload format will fit every industry.
- Don't assume metadata compatibility guarantees payload compatibility.
- Don't ignore the security and management risks of extreme interconnection.
**Deitzler's Law warning:**
- Contextual tools may make the first 80% easy.
- The next 10% may be difficult.
- The final 10% may be impossible beneath locked abstractions.
- Use that pattern to challenge platform selection.
**Verbatim composability example:**
```
cat [my file] |
tr -cs A-Za-z '\n' |
tr A-Z a-z |
sort |
uniq -c |
sort -rn |
sed [n]q6
```
**Flow analogy:**
- Treat common interfaces like the shell pipe.
- Let each processor consume a known form and emit a known form.
- Compose streams in orders the component designer did not anticipate.
- Preserve domain-specific payload meaning while standardizing exchange context.
*Ref: Flow Architectures.md — "Increasing the Flexibility of Data Flow Design"; "Flow and Event-Driven Architectures"*
---
### 8. Engineer the Five Production Properties Together
**Principle:** Require security, agility, timeliness, manageability, and memory as independent but interacting production properties.
**Do:**
- Make producer and consumer trust explicit.
- Protect data shared with authorized consumers.
- Preserve producer control over access.
- Enable independent adaptation by producers and consumers.
- Deliver data within the value window of the use case.
- Expose enough behavior for both sides to understand the system.
- Give each side actions it can take within its own control boundary.
- Support replay when state reconstruction, audit, troubleshooting, or simulation requires it.
- Allow fire-and-done events when memory adds no value.
- Document trade-offs among latency, retention, security, and cost.
- Treat these properties as promises, not marketing adjectives.
**Don't:**
- Don't reduce production readiness to delivery latency.
- Don't claim agility while every schema change requires synchronized deployment.
- Don't claim manageability with dashboards but no corrective controls.
- Don't retain history without a use case and policy.
- Don't claim security from transport encryption alone.
- Don't promise replay from a transient queue.
- Don't apply the same timeliness target to HFT and traffic alerts.
**Property questions:**
- **Security:** Who may receive the stream, and how is data protected and validated?
- **Agility:** Can each party change without forcing the other to change?
- **Timeliness:** What is the latest arrival time that preserves value?
- **Manageability:** What can each party observe and control?
- **Memory:** What history must remain replayable, and for how long?
**Trade-off rule:**
- Strengthening one property can weaken another.
- Encryption and provenance add processing cost.
- Long retention adds storage cost and privacy exposure.
- Stronger delivery coordination adds state and latency.
- Greater observability can leak sensitive information.
- More consumer choice can complicate producer control.
*Ref: Flow Architectures.md — "What Businesses Will Require from Flow"; "Recap: The High-Level Properties for Flow"*
---
### 9. Build Wardley Maps from User Need to Evolution
**Principle:** Map the components required for a scoped user need, then place each component by visibility and evolution so spatial position carries strategic meaning.
**Do:**
- State a scope before listing components.
- Make the scope specific enough for a focused discussion.
- Keep it broad enough to expose evolutionary influences.
- Identify users and their need.
- Use producer and consumer as the primary flow roles.
- Anchor the map on the user need.
- Place visible, user-facing needs higher.
- Place supporting components lower.
- Place every component on the evolution axis.
- Challenge every position with market evidence.
- Show likely movement from left to right.
- Revisit the map as adoption and standards change.
- Use the map to frame debate, not to claim perfect prediction.
**Don't:**
- Don't draw an ordinary system diagram and call it a map.
- Don't use spatial position without meaning.
- Don't omit an anchor.
- Don't place technologies solely by age.
- Don't assume the first solution to a need becomes the final standard.
- Don't treat the map as a static project plan.
- Don't hide disagreement; use it to test assumptions.
- Don't map batch or request-response integration inside a scope explicitly limited to near-real-time event-driven integration.
**Four evolutionary stages:**
- **Genesis:** unique, rare, uncertain, changing, newly discovered.
- **Custom built:** uncommon, bespoke, environment-specific, frequently changing.
- **Product including rental:** increasingly common, repeatable, defined, understood, differentiated but stabilizing.
- **Commodity including utility:** highly standardized, ubiquitous, volume-oriented, operationally optimized, undifferentiated.
**Map semantics:**
- The user need is the anchor.
- Relative position on the evolution axis is meaningful.
- Expected left-to-right evolution provides consistency of movement.
- Movement changes strategy: explore at the left; optimize at the right.
**Flow scope used by the book:**
- Enable near-real-time integration between disparate organizations through event-driven architectures.
- Exclude batch integration.
- Exclude request-response API integration.
- Exclude event-driven control cases that generally do not cross organizational boundaries from this specific map scope.
*Ref: Flow Architectures.md — "Wardley Mapping"; "Establishing a Scope for the Map"; "Determining a Measure of Technology Evolution"; "What Is a Map?"*
---
### 10. Place Flow Components According to Current Maturity
**Principle:** Use the book's market snapshot to distinguish mature infrastructure and processing from immature discovery, metadata, payload, and general flow interfaces.
**Do:**
- Place flow integration near the Custom/Product boundary in the book's snapshot.
- Place physical connection mechanisms such as HTTP, WebSocket, and MQTT toward Commodity/Utility.
- Place logical flow connection interfaces in Product because no universal interface exists.
- Place discovery in Genesis because broadly adopted discovery APIs are absent.
- Place metadata formats in Custom moving toward Product.
- Place payload formats in Custom.
- Place processors and queues in Commodity/Utility at the abstraction level used by the map.
- Place sinks in Commodity/Utility for common storage and visualization needs.
- Place sources broadly in Product while recognizing their wide maturity range.
- Place cloud infrastructure in Commodity/Utility.
- Distinguish a component category's position from any one product's position.
- Use the appendix's promises and examples to challenge placement.
**Don't:**
- Don't call flow a commodity while every interface and payload contract is bespoke.
- Don't infer protocol maturity from network-protocol maturity.
- Don't call discovery mature because web search exists.
- Don't equate a product-specific API with a general flow interface.
- Don't place every source at the same evolutionary point.
- Don't ignore product ecosystems that accelerate movement toward utility.
- Don't assume commodity status eliminates differentiated quality of service.
**Strategic consequences:**
- Buy or consume commodity infrastructure where possible.
- Invest custom effort where the user need differentiates the organization.
- Watch discovery, metadata, provenance, and common connection interfaces for rapid movement.
- Expect standardization to shift competition toward data quality, algorithms, service quality, and price.
- Re-map after standards, cloud services, or open source projects gain adoption.
**Evolution dependency:**
- Flow integration cannot become commodity while its core interfaces remain incompatible.
- Metadata format must evolve for common event interpretation.
- Discovery likely coevolves because consumers need protocol, volume, language, and connection facts before subscribing.
- Payload formats may remain industry-specific longer than metadata.
*Ref: Flow Architectures.md — "Turning Our Value Chain into a Map"; "The users and user need"; "Flow integration components"; "Interaction components"; "Infrastructure"*
---
### 11. Validate Value Chains with Promise Theory
**Principle:** Model each component as an autonomous agent that can promise only its own behavior, then trace promises upward until they fulfill the user need.
**Do:**
- Define each agent boundary deliberately.
- Record the promiser.
- Record the promisee.
- State a body containing the quality and bound of the promise.
- Model the reciprocal promise to accept or use the offered behavior.
- Validate connections from less visible components toward more visible needs.
- Remove connections where no direct promise exists.
- Treat internal implementation as unknown when evaluating the promise.
- Let any observer independently assess whether a promise was kept.
- Let agents independently interpret promise intent.
- Use promises to identify missing value-chain components.
- Revisit promises when delivery, security, or retention commitments change.
**Don't:**
- Don't make one component promise another autonomous component's behavior.
- Don't treat a requirement imposed from above as an assured promise from below.
- Don't rely on imposition as if compliance were guaranteed.
- Don't connect producer directly to consumer if an intermediary actually makes the delivery promise.
- Don't draw queue-to-source or queue-to-sink promises without processing that makes the relationship real.
- Don't hide quantified limits behind vague labels such as reliable or real-time.
**Terms:**
- **Agent:** an autonomous active entity.
- **Promise:** a stated intention to perform a type of behavior.
- **Promiser:** the agent making the promise.
- **Promisee:** the agent receiving the promise.
- **Body:** the promised quality and its bounded extent.
- **Imposition:** an attempt to coerce behavior without a guarantee of compliance.
**Reciprocity:**
- The promiser states: “I promise to body.”
- The promisee states: “I promise to accept or utilize body.”
- Use `+Body` for the offered promise.
- Use `-Body` for the reciprocal acceptance promise.
**Flow application:**
- Flow integration promises usable integration to producers and consumers.
- Interfaces promise discovery and logical connection.
- Protocols promise consistent delivery of data and context.
- Infrastructure promises capacity and commodity services to computing components.
- Queues promise storage and forwarding to processors, not behavior on behalf of sources or sinks.
*Ref: Flow Architectures.md — "Promise Theory"; "What is Promise Theory?"; "Promise Theory notation"; "Building a Flow Integration Value Chain"*
---
### 12. Decompose the Flow Value Chain Explicitly
**Principle:** Separate users, integration, interaction, and infrastructure so every flow capability has an owner and a testable promise.
**Do:**
- Model producers and consumers as roles.
- Model flow integration as their shared user need.
- Separate logical connection from physical connection.
- Provide a discovery interface.
- Separate metadata format from payload format.
- Model source, processor, queue, and sink independently.
- Include infrastructure capacity and commodity services.
- Identify processors that act as producer, consumer, or both.
- Identify sidecar processors that act on stream conditions rather than payloads.
- Define the point at which each stream stops.
- Preserve asynchronous decoupling through queues where useful.
- Map all components to the same scoped need.
**Don't:**
- Don't let “platform” hide source, processor, queue, and sink responsibilities.
- Don't make consumers manage physical connections directly if infrastructure can abstract them.
- Don't confuse stream discovery with schema registration.
- Don't treat metadata and domain payload as one immutable specification.
- Don't assume every processor terminates the stream.
- Don't assume every sink is a database.
- Don't add a queue when direct routing meets the promises with less complexity.
**Integration components:**
- **Logical connection:** negotiate, establish, authenticate, manage, and close stream access.
- **Discovery:** find streams and learn volume, protocols, schemas, fees, and other qualities.
- **Metadata format:** describe context needed to route, decrypt, parse, and attribute events.
- **Payload format:** define the event-specific domain data.
**Interaction components:**
- **Source:** collect data from devices or software.
- **Processor:** transform, filter, route, aggregate, calculate, or trigger action.
- **Queue:** buffer, store, and forward events between independently operating parties.
- **Sink:** display, store, or finally use the stream without forwarding that event further.
**Infrastructure:**
- Include compute, storage, networking, operating systems, physical connections, power, facilities, and telecommunications behind the abstraction.
- Promise capacity and common services to computing components.
- Keep the high-level map simple when further decomposition does not change the flow strategy.
*Ref: Flow Architectures.md — "Flow Integration Components"; "Interfaces"; "Protocols"; "Interaction Components"; "The Final Piece"*
---
### 13. Use Queues for Decoupling and Logs for Ordered Memory
**Principle:** Select a transient queue, durable ordered log, or workflow according to the promises the use case needs.
**Do:**
- Use queues to decouple message senders and receivers.
- Use topics to route published messages to interested consumers.
- Use acknowledgment protocols only where the delivery promise requires them.
- Use logs when consumers must retrieve ordered history.
- Use workflows when a multistep process must hold and forward state over time.
- Document ordering scope.
- Document retention duration.
- Document whether reads remove messages.
- Document whether multiple consumers can read the same history independently.
- Document whether consumers can select offsets or time ranges.
- Keep delivery promises bounded to the queue or broker domain.
- Test queue saturation and consumer lag.
**Don't:**
- Don't call a transient queue a historical system of record.
- Don't promise global exactly-once behavior merely because a queue advertises a delivery mode.
- Don't assume reads leave queue contents available.
- Don't assume logs offer every queue delivery feature.
- Don't use a workflow engine as a high-volume log without matching its promises and limits.
- Don't treat “at least once,” “at most once,” and “exactly once” as interchangeable.
- Don't omit idempotence planning when duplicates are possible.
**Book-level delivery guarantees:**
- Early message-oriented middleware offered “deliver exactly once.”
- It also offered “deliver at least once.”
- It also offered “deliver at most once.”
- Queues implemented guarantees through acknowledgment exchanges.
- The source does not provide a complete end-to-end formalization of these semantics.
- Treat each as a scoped component promise, not a universal application outcome.
**Named queue examples:**
- IBM MQ.
- TIBCO Enterprise Message Service.
- RabbitMQ.
- Apache ActiveMQ.
- KubeMQ.
- Amazon SQS.
- Azure Service Bus.
- Azure Queue Storage.
- Azure Event Grid.
- Google Cloud Pub/Sub.
- Amazon MQ.
**SQS example in the source:**
- The high-throughput queue promises at-least-once delivery.
- The FIFO queue promises at-least-once delivery in received order.
- Use such wording precisely; do not silently strengthen it.
*Ref: Flow Architectures.md — "Message Queues"; Appendix "Queue/Log"; "Message queues"; "Process Automation"*
---
### 14. Avoid Recreating a Centralized Enterprise Service Bus
**Principle:** Use the ESB lesson to preserve decoupling without concentrating all transformation, routing, process control, and organizational change in one central bottleneck.
**Do:**
- Use a shared bus where the connection count and change rate remain manageable.
- Isolate ESB scope to bounded clusters when legacy integration requires it.
- Move domain processing toward responsible services.
- Standardize protocols to reduce adapter proliferation.
- Prefer composable functions and services for new event-driven integrations.
- Keep routing distributed where organizational ownership is distributed.
- Let local teams manage local event domains.
- Integrate event platforms with broader observability tools.
- Use connectors when they materially reduce work for stable product interfaces.
- Preserve an escape path from connector constraints.
**Don't:**
- Don't centralize all enterprise communication control.
- Don't put every domain transformation in a shared bus.
- Don't assume one pane of glass can control a large adaptive system.
- Don't let adapters conceal incompatible contracts indefinitely.
- Don't force all changes through one integration team.
- Don't recreate a distributed monolith from tightly chained functions.
- Don't confuse consistent deployment with loose coupling.
**ESB lesson:**
- SOA exposed shared functions as services.
- Diverse interfaces and protocols made direct many-to-many integration expensive.
- ESBs introduced adapters, routing, transformation, monitoring, security, and orchestration.
- Central control was attractive at manageable scale.
- Complexity, performance, and change limits constrained enterprise-wide centralization.
- Producer-consumer decoupling remained valuable and informed later streaming systems.
**Connector lesson:**
- Dell Boomi, MuleSoft, and IFTTT illustrate contextual connector ecosystems.
- Connectors can trigger ingress, intermediate, and egress actions.
- Vendors gain consistency and ecosystem control.
- Users lose flexibility for unanticipated integration shapes.
- Serverless composition can reduce connector management while increasing freedom.
*Ref: Flow Architectures.md — "Service Buses"; "Mapping Service Buses and Message Queues"; "Streaming Architectures and Integration Today"*
---
### 15. Match MQTT to Lightweight Publish-and-Subscribe Needs
**Principle:** Use MQTT where lightweight machine-to-machine pub/sub, constrained devices, brokered topics, and explicit connection management fit the problem.
**Do:**
- Let clients act as publishers, subscribers, or both.
- Connect clients to a broker.
- Route messages by topic name.
- Let subscribers request one or more topics.
- Let publishers mark each message with its topic.
- Acknowledge MQTT commands as required by the protocol.
- Close connections and subscriptions explicitly.
- Add queue capability when asynchronous delivery is required.
- Use MQTT over appropriate network and security layers.
- Evaluate message size before selecting it.
- Use CloudEvents bindings when common event metadata is needed.
- Consider Eclipse Sparkplug for its intended SCADA context.
**Don't:**
- Don't assume an MQTT broker must persist every message.
- Don't treat MQTT as a universal payload schema.
- Don't ignore payload-size constraints.
- Don't assume MQTT directly binds every other event protocol.
- Don't assume an IoT origin prevents business-message use, but validate fitness.
- Don't expose constrained devices to heavyweight integration assumptions.
- Don't omit broker authorization and identity controls.
**Basic exchange:**
1. A client requests a broker connection.
2. The broker assigns and monitors a connection ID.
3. The broker maintains topics.
4. Subscribers request topics.
5. Publishers send topic-marked messages.
6. The broker routes messages to subscribers.
**Named MQTT ecosystem examples:**
- HiveMQ.
- Solace PubSub+.
- Inductive Automation Ignition.
- Eclipse Mosquitto.
- EMQ/EMQX.
- VerneMQ.
- AWS IoT Core.
- Microsoft Azure IoT.
- Google Cloud IoT Core.
- RabbitMQ and IBM MQ plug-ins.
- Apache Kafka MQTT connectors.
*Ref: Flow Architectures.md — "Internet of Things"; "MQTT"; Appendix "MQTT"*
---
### 16. Layer Transport and Messaging Protocols Deliberately
**Principle:** Distinguish connection, transport, application, subscription, metadata, and payload responsibilities instead of demanding one protocol solve every layer.
**Do:**
- Use IP for routing across network boundaries.
- Use TCP where its connection and flow-control model fits.
- Evaluate QUIC for concurrent connections and HTTP/3 transport.
- Use HTTP for ubiquitous point-to-point request-response and connection establishment.
- Use HTTP/2 streaming where its model fits.
- Use WebSocket for long-lived bidirectional communication over web-compatible infrastructure.
- Use AMQP for open business-message exchange across platforms and organizations.
- Use NATS subjects where its simple messaging model fits.
- Place a common event metadata protocol over suitable transports.
- Encrypt network connections with TLS where supported.
- Treat protocol selection as a stack, not a winner-takes-all choice.
- Validate firewall, proxy, browser, device, latency, and payload constraints.
**Don't:**
- Don't call HTTP native pub/sub; it has no inherent topic or subscription model.
- Don't call WebSocket a payload schema.
- Don't call CloudEvents a transport.
- Don't treat AMQP's opaque payload as self-describing.
- Don't assume TCP, QUIC, HTTP, MQTT, and CloudEvents occupy the same layer.
- Don't infer application-level end-to-end security from TLS on one hop.
- Don't call gRPC streaming a book recommendation; the source does not make that claim.
**HTTP methods named by the source:**
- `GET` requests the state of a resource.
- `POST` sends data to a resource.
- `PUT` replaces a resource with supplied state.
- `DELETE` removes a resource and its state.
- HTTP is well suited to initial request-response connection activity.
- Flow control, stream errors, and routing may require additional mechanisms.
**WebSocket:**
- Begin with an HTTP upgrade request.
- Exchange security and subprotocol information.
- Maintain two-way communication.
- Carry protocols such as CloudEvents when appropriate.
- Reuse standard web ports and proxies.
**AMQP:**
- Negotiate connection over an underlying transport.
- Use channels to share a connection across streams.
- Represent streams beyond individual connection lifetimes.
- Use common metadata.
- Treat the base payload as an immutable opaque binary block.
**gRPC boundary:**
- The appendix lists gRPC as a CNCF RPC framework.
- The author says it could play a role in a future flow interface.
- The source gives no gRPC streaming pattern, guarantee, or recommendation.
*Ref: Flow Architectures.md — "HTTP and WebSocket"; Appendix "Connection"; Appendix "Protocol"; "Standards bodies"; "Open source projects"*
---
### 17. Keep the NATS Protocol Example Simple and Exact
**Principle:** Use NATS as evidence that publish/subscribe mechanics can be extremely small, while recognizing that its protocol remains product-specific in the book's map.
**Do:**
- Use a subject string to identify the stream of interest.
- Keep client-server commands explicit.
- Assign a client subscription ID.
- Include payload length in publish and delivery commands.
- Evaluate whether simplicity covers the required use cases.
- Separate NATS protocol simplicity from universal flow-standard status.
- Consider Synadia NGS's subject-based global connection model as a product-stage experiment.
**Don't:**
- Don't add complexity without a demonstrated promise.
- Don't claim the NATS Client Protocol is a vendor-neutral flow standard.
- Don't omit delivery, security, retention, or operational needs merely because the wire commands are small.
- Don't confuse a subject with discovery metadata.
**Verbatim subscription example:**
```
SUB foo.bar 90
```
**Verbatim publish example:**
```
PUB foo.bar 5 Hello
```
**Verbatim delivery example:**
```
MSG foo.bar 90 5 Hello
```
**Interpretation:**
- `SUB` requests the `foo.bar` subject.
- `90` is the client-generated subscription ID.
- `PUB` supplies subject, byte count, and payload.
- `MSG` supplies subject, subscription ID, byte count, and payload.
- Ask “Why can't it be this simple?” before accepting a heavier interface.
*Ref: Flow Architectures.md — Appendix "NATS Client Protocol"; Appendix "Synadia NGS"*
---
### 18. Use CloudEvents as Common Event Metadata, Not a Domain Schema
**Principle:** Use CloudEvents to normalize event context across protocol bindings while leaving domain payload semantics to separate contracts.
**Do:**
- Treat CloudEvents as a metadata specification.
- Bind CloudEvents to HTTP, MQTT, Kafka, NATS, or another supported mechanism.
- Use structured representation when the receiving system can interpret it.
- Use binary payloads where arbitrary digital content must be carried.
- Supply event type.
- Supply source.
- Supply a unique event ID.
- Supply occurrence time when available.
- Supply subject when identifying the changed object is useful.
- Supply data content type.
- Preserve extension attributes.
- Keep the event envelope lightweight.
- Use the same semantic fields across transport bindings.
- Evaluate the Subscription API and discovery work separately from the metadata format.
**Don't:**
- Don't treat CloudEvents as a network transport.
- Don't assume CloudEvents standardizes the domain payload.
- Don't assume binary data describes its own structure.
- Don't claim CloudEvents defines end-to-end encryption.
- Don't assume one binding behaves identically at every transport layer.
- Don't remove provenance, authorization, or retention work from the design.
- Don't overstate adoption in the book's 2021 snapshot.
**Verbatim CloudEvents example:**
```
{
 "specversion" : "1.x-wip",
 "type" : "com.github.pull_request.opened",
 "source" : "https://github.com/cloudevents/spec/pull",
 "subject" : "123",
 "id" : "A234-1234-1234",
 "time" : "2018-04-05T17:31:00Z",
 "comexampleextension1" : "value",
 "comexampleothervalue" : 5,
 "datacontenttype" : "text/xml",
 "data" : "<much wow=\"xml\"/>"
}
```
**Field meanings in the source:**
- `specversion` identifies the CloudEvents version.
- `type` identifies the event class.
- `source` identifies the original event source.
- `subject` identifies the object whose state changed.
- `id` uniquely labels the event.
- `time` records event creation time.
- Extension fields carry producer-defined metadata.
- `datacontenttype` identifies payload form.
- `data` carries the payload.
*Ref: Flow Architectures.md — Appendix "CNCF CloudEvents"; "A known and predictable protocol"; "Standards bodies"*
---
### 19. Separate Metadata, Payload Contracts, and Discovery
**Principle:** Treat event context, domain data, schema validation, and stream discovery as different contracts that evolve at different rates.
**Do:**
- Use metadata to explain what the event is and how to interpret it.
- Use a payload contract to define domain-specific data.
- Advertise the payload format through metadata or connection information.
- Register schemas when software must validate events before transmission or processing.
- Register streams when consumers must discover topics, URIs, rates, protocols, and policies.
- Let industries standardize common payloads where repeated use justifies it.
- Keep producer-specific payloads explicit during early evolution.
- Publish version and compatibility expectations outside the transport ambiguity.
- Test whether old consumers can reject or ignore unknown data safely.
- Make schema ownership visible.
- Distinguish a schema registry from a stream registry.
**Don't:**
- Don't assume a common event envelope creates a common domain model.
- Don't advertise a schema without the topics that use it.
- Don't advertise a stream without its payload contract.
- Don't infer compatibility from both payloads being JSON.
- Don't claim the book prescribes Protobuf, Avro, or JSON Schema.
- Don't claim the book gives a concrete schema-evolution algorithm.
- Don't evolve a contract silently.
**Source-grounded evolution guidance:**
- Keep interfaces loosely coupled so components can change independently.
- Preserve predictable protocols while implementations evolve.
- Use metadata to identify payload type and parsing needs.
- Expect early streams to define their own payload formats.
- Expect industries and governments to standardize common payloads over time.
- Expect common standards to depend on cost and flexibility.
- Treat payload standardization as less mature than transport and network standards.
**Requested technology boundary:**
- **Protocol Buffers:** not named in the book.
- **Avro:** not named in the book.
- **JSON Schema:** not named in the book.
- **CloudEvents:** covered as common event metadata with structured JSON and binary modes.
- Use the book's selection questions for the absent formats, but do not fabricate a book-endorsed ranking.
**Schema-evolution questions derived from the book's promises:**
- Can metadata identify the format in use?
- Can the consumer determine whether it can parse the payload?
- Can producer and consumer change independently?
- Can discovery reveal the current contract before connection?
- Does the change preserve trust, timeliness, and manageability?
- Is the payload standard shared widely enough to reduce integration cost?
*Ref: Flow Architectures.md — "Protocols"; "A known and predictable protocol"; Appendix "Discovery"; Appendix "CNCF CloudEvents"*
---
### 20. Design Discovery Before Stream Counts Explode
**Principle:** Make streams findable with enough information to determine fitness before connection; use web search now and registries where programmatic discovery creates value.
**Do:**
- Publish a human-readable page for each offered stream.
- Include a URI or connection mechanism.
- Include protocol requirements.
- Include event volume or rate.
- Include payload schema information.
- Include fees and access conditions where applicable.
- Include language or localization constraints where relevant.
- Use a stream registry when systems must discover and select streams programmatically.
- Use schema registries for event validation.
- Keep stream metadata accurate.
- Evaluate hybrid discovery across public search and vendor registries.
- Watch the CloudEvents Subscription API and discovery efforts as immature candidates.
**Don't:**
- Don't confuse stream discovery with schema discovery.
- Don't expect a schema registry to identify every topic that uses a schema.
- Don't build an internet-wide registry before demand exists.
- Don't assume a central public registry will succeed because the need sounds obvious.
- Don't hide rates, formats, or connection constraints until after subscription.
- Don't make discovery depend on private human contacts when self-service is the goal.
- Don't claim AsyncAPI is discussed by the book; it is absent from the source.
**Discovery options in the source:**
- Search engines and web pages.
- VANTIQ's product-scoped registry.
- Solace's schema, topic, traffic, and error information.
- AWS EventBridge schema registry and external integrations.
- Azure Event Hub schema registry.
- CloudEvents Subscription API work.
- Product- or platform-scoped registries.
- A possible future marketplace or broad search service.
**Discovery promises:**
- Help consumers find relevant stream options.
- Record the stream URI.
- Record volume.
- Record protocols.
- Record other qualities needed before connection.
- Support a point-and-click or automated selection experience where valuable.
**Market warning:**
- Public object and XML schema registries struggled historically.
- API discovery mostly uses vendor pages and search engines.
- Flow discovery may follow the same pattern.
- A “Google for event streams” has little value before enough streams exist.
- Reassess registry investment as network effects grow.
*Ref: Flow Architectures.md — "Discovery"; Appendix "Interface"; "CNCF Cloud Events Subscription API"*
---
### 21. Use Serverless and Low-Code to Reduce Toil, Not to Hide Architecture
**Principle:** Use event-triggered functions, workflows, and visual processors to reduce packaging and operations work while preserving explicit event contracts and flow boundaries.
**Do:**
- Trigger functions from events.
- Keep a function focused on a bounded action.
- Use a workflow engine for multistep coordination.
- Pay for execution rather than idle capacity where the economics fit.
- Use managed triggers to connect cloud-service state changes.
- Use serverless as a scripting mechanism for operations events.
- Use visual flow models where they cover the process cleanly.
- Mix low-code and code when custom behavior exceeds the platform abstraction.
- Keep producer, queue, processor, and sink responsibilities visible.
- Test scale-to-zero and burst behavior against timeliness needs.
- Document vendor-specific event formats.
- Preserve a path to common metadata and interfaces.
**Don't:**
- Don't chain functions into an opaque distributed monolith.
- Don't use one function for a process requiring durable multistep state.
- Don't assume “serverless” means infrastructure has disappeared.
- Don't assume low-code means no operational complexity.
- Don't accept the 85% rule when the remaining behavior is critical.
- Don't confuse a proprietary cloud event ecosystem with the open WWF.
- Don't ignore vendor inertia and portability cost.
**Named examples:**
- AWS Lambda.
- AWS Step Functions.
- Amazon CloudWatch events.
- Microsoft Azure Functions.
- Azure Logic Apps.
- Google Cloud Functions.
- Knative Eventing.
- VANTIQ.
- Mendix.
- OutSystems.
- Apache Flink.
- Apache Storm.
**Serverless value:**
- Remove server provisioning from the developer's immediate task.
- Trigger code from service events.
- Scale execution with event demand.
- Charge for actual execution time.
- Increase composability across managed services.
**Serverless constraint:**
- Cloud providers define proprietary event interfaces and formats.
- Cross-cloud or third-party integration can require custom mapping.
- Use this as evidence of proto-flow, not proof of universal flow.
*Ref: Flow Architectures.md — "Code and Flow"; "Functions, Low-Code, and No-Code Processors"; "Serverless"; Appendix "Serverless event processing"*
---
### 22. Build Durable, Replayable, Partitioned Event Logs Deliberately
**Principle:** Use log-based platforms when ordered history, independent consumer positions, replay, partitioned scale, or event sourcing are required.
**Do:**
- Publish events to named topics.
- Give each record a key, value, and timestamp as required by the platform model.
- Partition topics using criteria aligned with consumer access and scale.
- Let consumers select their starting offset or time.
- Let consumers read independently from different positions.
- Retain events for a declared period.
- Use ordered history to reconstruct state.
- Use replay to recover, audit, test, or analyze patterns.
- Monitor consumer progress against retention.
- Choose partition criteria before volume makes repartitioning expensive.
- Preserve the sequence needed by the domain.
- Use log memory only where its storage and governance costs are justified.
**Don't:**
- Don't remove an event merely because one consumer read it.
- Don't choose a partition key that scatters one entity's required sequence without accepting the consequence.
- Don't call time order global when it is only guaranteed within a partition.
- Don't assume every query belongs on the active log.
- Don't use a relational database query as the only trigger for time-critical new events.
- Don't retain an unbounded log by accident.
- Don't confuse a log with a general-purpose database.
**Named platforms:**
- Apache Kafka.
- Apache Pulsar.
- AWS Kinesis.
- AWS Managed Streaming for Kafka.
- Microsoft Azure Event Hubs.
- Confluent Cloud on GCP.
**Kafka/Pulsar comparison in the source:**
- Kafka leads in ecosystem depth.
- Kafka has extensive connectors, management tools, and managed providers.
- Pulsar can offer lower latency for many use cases.
- Pulsar includes multitenancy and tiered storage in the comparison.
- Pulsar has a smaller ecosystem in the book's snapshot.
- Select by promises and environment, not name recognition alone.
**Key-routing guidance:**
- The source gives producer ID prefix and geography as partition examples.
- Use a key that groups events consumers must process together.
- Keep partition placement discoverable through platform interfaces.
- Balance ordering locality against parallelism.
- Validate hot partitions and uneven geography.
**Scale and event-sourcing guidance:**
- The book cites LinkedIn processing more than seven trillion Kafka messages per day; treat this as evidence, not an arbitrary deployment promise.
- Use event sourcing only when the log is intentionally the state authority: record every relevant change, preserve order, replay deterministically, and fold to current state.
- Rebuild state after failure or restart, explain how state arose, and let consumers replay independently.
- Don't call any append-only audit table event sourcing, mix nondeterministic effects into reconstruction, or delete required history.
- Separate active replay retention from long-term sink retention; govern sensitive history and the cost of long replays.
*Ref: Flow Architectures.md — "Log-Based Stream Processing Platforms"; "Memory"; "Retention"; "Series events"; Appendix "Log-based Streaming Platforms"*
---
### 23. Choose Stateful Stream Processing for Live World Models
**Principle:** Use stateful stream processors when decisions depend on the current state and relationships of many agents, not merely on independent records flowing through a pipeline.
**Do:**
- Model real-world entities as digital twins.
- Model relationships among those twins.
- Update the model continuously from events.
- Let each agent interpret its local state.
- Let agents exchange state through explicit relationships.
- Run broader calculations across the graph where needed.
- Use the model for reactive action or prediction.
- Emit derived insights to downstream streams.
- Keep the bounded problem domain explicit.
- Evaluate consistency, redundancy, and recovery of the live model.
- Compare stateful processing with a keyed log and external state store.
- Use a workflow instead when the problem is a bounded sequence of interdependent steps.
**Don't:**
- Don't introduce digital twins for simple stateless transformation.
- Don't hide the event history needed to rebuild the live model.
- Don't model an unbounded real world without ownership boundaries.
- Don't assume a stateful graph eliminates delivery and provenance concerns.
- Don't use a stateful engine merely because the word “real-time” appears in requirements.
- Don't treat experimental platform maturity as commodity certainty.
**Named examples:**
- Swim.ai / SwimOS.
- Apache Flink.
- EnterpriseWeb.
- Traffic-light coordination.
- Metropolitan bus ETA calculation.
- City-scale device state.
**Stateful-versus-log distinction:**
- A log records ordered events and leaves active entity state to consumers.
- A stateful processor keeps a live domain representation.
- A digital-twin graph makes relationships first-class.
- A log remains valuable for replay and reconstruction.
- The two approaches can be combined.
**Selection test:**
- Choose stateless horizontal processors when each event can be handled independently.
- Choose a stateful processor when the action requires a shared current world model.
- Choose a workflow when one event must pass through known dependent steps.
- Choose a log when ordered history is the dominant requirement.
*Ref: Flow Architectures.md — "Stateful Stream Processing"; "Command and control"; Appendix "Stateful Stream Processing"*
---
### 24. Use Reactive Programming for Nonblocking Stream Consumers
**Principle:** Use reactive programming when services consume asynchronous streams continuously and must avoid blocking scarce execution resources.
**Do:**
- Treat data exchange as asynchronous flow.
- Use nonblocking processing where the framework supports it.
- Buffer deliberately and bound the buffer.
- Connect libraries to queues or logs where appropriate.
- Apply actor or observer patterns only when their semantics fit.
- Propagate flow-control signals through supporting libraries and protocols.
- Measure resource use under sustained load.
- Separate framework-level flow control from business-level overload policy.
- Use RSocket where its built-in flow-control promise fits the connection.
- Keep failure and cancellation behavior explicit.
**Don't:**
- Don't equate reactive syntax with an end-to-end flow architecture.
- Don't use unbounded in-memory buffering.
- Don't assume nonblocking code eliminates backpressure.
- Don't hide blocking database or network calls inside reactive handlers.
- Don't let one slow sink exhaust processor memory.
- Don't claim the book defines a complete backpressure protocol.
- Don't assume every event consumer needs a reactive framework.
**Named frameworks and platforms:**
- Spring WebFlux.
- Project Reactor.
- Spring Data.
- Spring Cloud Gateway.
- Akka.
- Eclipse Vert.x.
- ReactiveX.
- Lightbend.
- Netifi.
- RSocket.
- Spring Cloud Stream.
- Faust.
- JavaScript Streams API.
**Backpressure and flow-control extraction:**
- Flow must manage rates so consumers are not overwhelmed.
- A producer may promise to modulate event flow for an overwhelmed consumer.
- MQTT includes control functions such as message expiration and message-length limits.
- TCP performs packet-level flow control.
- RSocket is identified as having built-in flow control.
- Buffering shifts pressure; it does not remove it.
- Rate policy must be part of producer-consumer promises.
*Ref: Flow Architectures.md — Appendix "Reactive programming platforms and frameworks"; "Discrete events"; Appendix "Protocol"*
---
### 25. Design Timeliness as Latency Plus Retention
**Principle:** Deliver events early enough to retain value and keep them available long enough for intended consumers; optimize both latency and retention.
**Do:**
- Define the event's value window.
- Measure network latency.
- Measure processing latency at every step.
- Count routing, duplication, inspection, transformation, and queueing time.
- Establish performance budgets for processors.
- Process independent branches in parallel where safe.
- Place computation closer to sources or sinks when distance dominates.
- Minimize network hops for latency-sensitive paths.
- Advertise event retention.
- Set retention by use case, volume, regulation, and financial cost.
- Distinguish seconds, weeks, and years explicitly.
- Coordinate forgetting where consumers require every event.
**Don't:**
- Don't use “real-time” without a bounded value window.
- Don't assume consumers always process events immediately.
- Don't optimize network latency while ignoring processor time.
- Don't ignore speed-of-light limits.
- Don't keep events forever because storage appears cheap.
- Don't delete events before promised consumers can receive them.
- Don't apply sink data-retention rules blindly to active streams.
**Latency facts used by the book:**
- Mumbai to Chicago is roughly 12,939 kilometers.
- The theoretical light-speed floor is a little over 43 milliseconds.
- Real routes add network devices, indirect paths, bandwidth contention, and processing.
- HFT often colocates systems in exchange data centers.
- Cross-organizational systems must usually accept more distance and hops.
**Retention questions:**
- How long does the event remain valuable?
- Must a disconnected consumer catch up?
- Must state be reconstructed from the stream?
- Must every event be acknowledged before deletion?
- What privacy obligation applies while the event remains active?
- What happens when a consumer falls behind retention?
**Timeliness rule:**
- Optimize for “available when valuable,” not universally “as fast as possible.”
- A consumer may intentionally wait for related data or capacity.
- The stream must still make the event available before the intended action loses value.
*Ref: Flow Architectures.md — "Timeliness"; "Latency"; "Retention"*
---
### 26. Scale Through Edge Locality and Hierarchical Flow
**Principle:** Use localized flows, regional aggregation, and core coordination to reduce latency and scale traffic in the trunk-limb-branch-leaf pattern seen in natural networks.
**Do:**
- Place processing near sources and sinks.
- Keep local command-and-control traffic local.
- Aggregate or filter before forwarding to the core.
- Use regional endpoints for region-specific events.
- Coordinate only cross-region behavior centrally.
- Use data centers, branches, colocation facilities, and telecom points of presence as edge locations.
- Preserve local operation during central disruption where the domain requires it.
- Forward events to the core later when central storage is needed but immediate central action is not.
- Make regional latency trade-offs visible to consumers.
- Partition distributor streams by region where semantics allow.
- Use CDNs and application delivery networks as familiar locality analogies.
**Don't:**
- Don't route local producer-consumer traffic across a distant central cloud without a reason.
- Don't claim edge removes the distance between the original source and global endpoints.
- Don't replicate every event everywhere by default.
- Don't make every edge wait on global consensus for local action.
- Don't lose the ability to perform aggregate analysis.
- Don't centralize all event-routing decisions in one global service.
- Don't claim a 5G-specific pattern from this book.
**Allometric-scaling guidance:**
- Complex systems optimize resource-delivery networks nonlinearly.
- The WWF is expected to develop central flows for important data sets.
- Granular streams may be aggregated into higher-level streams.
- Local flows connect to larger regional flows.
- Regional flows connect to core flows.
- Reverse distribution moves decisions or data back toward local consumers.
**5G source boundary:**
- The source lists 2G/3G, LTE, Wi-Fi, Bluetooth, Zigbee, ZWave, and other IoT protocols.
- It discusses network-provider demand, telecom POPs, private networks, and edge computing.
- It does not specify 5G slicing, radio behavior, or 5G guarantees.
- Apply the edge principles to 5G only as an independent extension, not as a book claim.
*Ref: Flow Architectures.md — "Flow and Scale"; "Latency"; "The Distributor Pattern"; "Distributed control"; "Messaging"*
---
### 27. Make Security a Stack of Explicit Promises
**Principle:** Combine access control, connection security, payload protection, identity, and provenance; no single layer establishes trust for a cross-organizational event path.
**Do:**
- Authenticate producers, consumers, and brokers as required.
- Authorize stream access.
- Encrypt network connections with TLS where applicable.
- Encrypt sensitive payloads independently when intermediaries or storage require it.
- Communicate how authorized consumers decrypt payloads.
- Verify peer identity through trusted certificates.
- Protect every connection-establishment step from spoofing.
- Preserve payload integrity across intermediaries.
- Track provenance when processors transform or extend data.
- Audit access and event movement where required.
- Minimize metadata leakage.
- Treat security as a prerequisite to producer and consumer participation.
**Don't:**
- Don't equate transport encryption with end-to-end encryption.
- Don't assume a broker is trusted merely because the client connected to it.
- Don't expose decryption keys in event metadata without a secure scheme.
- Don't assume CloudEvents defines encryption.
- Don't assume authorized processors cannot alter data improperly.
- Don't ignore devices that cannot support TLS directly.
- Don't call a stream secure without defining the trust boundary.
**Encryption guidance:**
- TLS protects data between connected parties.
- Payload encryption can protect data through intermediaries and at rest.
- MQTT can carry encrypted binary payloads.
- AMQP's immutable base message can preserve encrypted payload bits.
- CloudEvents can bind to MQTT and AMQP but leaves encryption outside its specification in the source snapshot.
- Flexibility may favor carrying independently encrypted payloads over embedding algorithms into the flow standard.
**Connection-security guidance:**
- Protect against man-in-the-middle interception and alteration.
- Use certificate authorities to validate identities where TLS is used.
- Authenticate brokers for clients that cannot establish direct TLS paths.
- Remember that one-hop TLS is insufficient for multi-intermediary end-to-end protection.
- Expect new mechanisms where many producers and consumers exceed 1:1 assumptions.
*Ref: Flow Architectures.md — "Security"; "Encryption"; "Connection security"*
---
### 28. Preserve Data Provenance Across Transformations
**Principle:** Record the inputs, entities, systems, and processes that influence event data so consumers can assess origin and detect unexpected alteration.
**Do:**
- Identify the original source.
- Record each meaningful transformation.
- Preserve event lineage through processors.
- Validate payload integrity.
- Append transformation evidence rather than overwriting origin.
- Separate provenance evidence from mutable event data where needed.
- Evaluate checksums or verification values for tamper detection.
- Evaluate append-only external logs for change history.
- Balance provenance strength against latency and throughput.
- Make provenance available to downstream authorized consumers.
- Treat provenance as part of brand and trust.
**Don't:**
- Don't assume a secure connection proves data accuracy.
- Don't let intermediaries erase origin.
- Don't claim a checksum alone provides complete provenance.
- Don't assume an event-contained record cannot itself be altered.
- Don't adopt blockchain solely because it is immutable in theory.
- Don't ignore distributed-ledger processing cost.
- Don't claim the book identifies a mature universal provenance solution.
**Approaches explored by the source:**
- Calculate a verification value from payload data.
- Use secrets known to producers.
- Append verification values after transformations.
- Store change records outside the event.
- Use an immutable ledger attested by independent parties.
- Explore blockchain-based systems cautiously.
**Unresolved promises:**
- Verify that consumed data matches produced data.
- Show how authorized transformations changed the data.
- Keep evidence trustworthy at WWF volume.
- Avoid destroying timeliness through verification overhead.
- Let consumers validate provenance without learning unauthorized information.
*Ref: Flow Architectures.md — "Data provenance"; "Control of Intellectual Property"*
---
### 29. Protect Intellectual Property and Define Monetization
**Principle:** Give data owners control, licensing, and compensation mechanisms sufficient to make valuable streams safe and economically attractive to publish.
**Do:**
- Define who owns event data.
- Restrict access to authorized consumers.
- Use encryption keys or certificates to enforce access periods where suitable.
- Attach licensing terms to stream access.
- Track downstream use where feasible.
- Preserve provenance so the owner's data is not misrepresented.
- Offer subscriptions or other payment arrangements through predictable interfaces.
- Price retention, volume, latency, and service quality explicitly.
- Make legal and technical controls complement one another.
- Reduce the incentive to copy by making legitimate streaming convenient.
**Don't:**
- Don't assume technical controls can prevent every copy after data reaches another computer.
- Don't rely on licensing without access enforcement.
- Don't rely on encryption without key governance.
- Don't publish valuable streams without commercial terms when compensation is required.
- Don't expose more event detail than consumers need.
- Don't ignore competitive intelligence revealed by fine-grained streams.
- Don't assume open standards require free data.
**Streaming analogy:**
- Downloadable digital music weakened distribution control.
- Convenient music and video streaming restored a measure of control and revenue.
- Business-data streaming can similarly offer access without making file distribution the primary model.
- Convenience can reduce incentives for unauthorized copying.
- The analogy does not imply perfect enforcement.
**Commercial opportunity:**
- Let consumers subscribe under producer-defined terms.
- Support news, weather, market, health, and other data subscriptions.
- Keep payment and authorization separable from the event payload.
- Expect monetization support to attract more producers.
- Treat the exact future mechanism as unresolved.
*Ref: Flow Architectures.md — "Control of Intellectual Property"; "Driving Technology Development"*
---
### 30. Pair Observability with Controllability
**Principle:** Make flow manageable by exposing meaningful signals and giving each autonomous party predictable actions it can take when behavior deviates.
**Do:**
- Monitor whether producers are sending expected events.
- Detect duplicates where they violate promises.
- Monitor event rates, latency, errors, and connection state.
- Exchange only the operational signals needed for healthy cooperation.
- Use connection-time error codes where request-response exists.
- Add liveness messages where silent push failure would be ambiguous.
- Let consumers retry, choose another route, or select another producer.
- Publish operational event streams where useful.
- Define configuration controls for subscriptions and delivery.
- Build circuit breakers for dangerous feedback.
- Trace event identity across processors.
- Keep control within the actor's real authority.
**Don't:**
- Don't collect every signal without cost and security analysis.
- Don't expose sensitive internals to external consumers unnecessarily.
- Don't build a dashboard without corrective actions.
- Don't assume a missing event produces an error response.
- Don't give consumers fictional control over producer operations.
- Don't rely on manual intervention for high-speed cascading failure.
- Don't expect one agent to observe the whole adaptive system from local connections.
**Observability tension:**
- Too little data makes event chains impossible to diagnose.
- Too much data can cost more than event processing.
- Too much data can expose security-sensitive insights.
- Share the minimum sufficient operational contract.
- Use API and Web error-handling precedent cautiously because flow is primarily push.
**Controllability and feedback-loop actions:**
- Change subscription configuration, retry, choose another route or producer, pause harmful processing, trigger a circuit breaker, or modify an agent.
- Trace event identity, detect cycles, test retry amplification and queue buildup, and keep emergency controls independent of the failing path.
- In the source's A→B→C→A example, each local action is valid while the global cycle reinforces itself.
- During the May 6, 2010 Flash Crash, interacting trading algorithms amplified selling and the Dow Jones dropped 9% in under 30 minutes.
- Use trading circuit breakers as the model: stop unsafe feedback automatically instead of waiting for human diagnosis.
*Ref: Flow Architectures.md — "Manageability"; "Observability"; "Controllability"; Figures 5-6 through 5-8*
---
### 31. Apply the Collector Pattern to Massive Fan-In
**Principle:** Use the Collector pattern when one consumer receives streams from many producers and must normalize, identify, buffer, or aggregate them.
**Do:**
- Design for hundreds, thousands, or millions of inputs as required.
- Define whether the consumer or producer initiates each connection.
- Consider a consumer-owned topic or URI where many producers submit the same event type.
- Assign stable producer or entity identities.
- Detect duplicates.
- Buffer bursts before downstream processing.
- Normalize only what downstream value requires.
- Partition collection by geography, producer class, or another useful dimension.
- Preserve source provenance.
- Apply backpressure or rate policy at collection boundaries.
- Separate ingestion scale from processing scale.
**Don't:**
- Don't assume every collector subscription must be manually configured.
- Don't use one unpartitioned ingress endpoint for unbounded producers.
- Don't lose producer identity during normalization.
- Don't count duplicate discoveries as new agents.
- Don't let one producer monopolize shared capacity.
- Don't infer that consumer-initiated subscription is mandatory for every collector case.
- Don't conflate collection with final consumption.
**Named cases:**
- AnyRent collecting rental inventory.
- IoT sensors feeding one application.
- Retail inventory aggregation.
- Securities trading inputs.
- Government sales-tax collection scenario.
- Registration and discovery services.
- Telemetry and analytics fan-in.
**Critical promises:**
- Accept producer input at required volume.
- Identify each source.
- Maintain security across many producers.
- Keep quality and format differences manageable.
- Avoid duplicate or conflicting state.
- Deliver normalized or aggregated output to the next processor or sink.
*Ref: Flow Architectures.md — "The Collector Pattern"; "Addressing and discovery"; "Telemetry and analytics"*
---
### 32. Apply the Distributor Pattern to Massive Fan-Out
**Principle:** Use the Distributor pattern when one producer or small producer set broadcasts events to many consumers across regions.
**Do:**
- Replicate publishing endpoints near consumers.
- Partition streams regionally when the event semantics allow it.
- Advertise regional availability and latency trade-offs.
- Decide whether all regions must publish simultaneously.
- Delay publication until all endpoints have the event only when simultaneous receipt is essential.
- Keep consumers close to regional endpoints.
- Scale output connections independently from source processing.
- Protect the producer from slow consumers.
- Preserve consistent metadata across replicas.
- Monitor replication delay.
- Use content-distribution lessons without assuming static-cache semantics.
**Don't:**
- Don't connect every global consumer to one server or data center.
- Don't claim edge replication eliminates source-to-edge travel time.
- Don't promise simultaneous global arrival casually.
- Don't hide region-specific origin or freshness.
- Don't let one consumer's flow-control state block all others.
- Don't replicate sensitive payloads into every region without policy.
- Don't treat fan-out as merely the reverse of fan-in; geography makes it harder.
**Named cases:**
- WeatherFlow.
- Stock ticker streams.
- Market feeds.
- Cloud-provider regional operational events.
- Query and observability distribution.
- Telemetry dashboards fed by a shared stream.
**Critical promises:**
- Reach all authorized subscribers.
- Preserve event identity across replicas.
- Bound regional delivery delay where possible.
- Handle subscription churn.
- Keep bandwidth and connection growth manageable.
- Expose regional limitations through discovery.
*Ref: Flow Architectures.md — "The Distributor Pattern"; "Latency"; "Telemetry and analytics"*
---
### 33. Apply the Signal Pattern to Derived Decisions and Events
**Principle:** Use the Signal pattern when processors interpret one or more incoming streams and emit higher-value events, commands, or insights.
**Do:**
- Give each signal processor one bounded responsibility.
- Define the input streams.
- Define the decision or transformation.
- Define the output event or action.
- Preserve input lineage.
- Compose many small signal processors rather than one universal processor where ownership is distributed.
- Integrate with system-wide observability.
- Make each processor resilient to missing, duplicate, and delayed inputs.
- Use stateful processing when the signal depends on a live shared model.
- Use stateless horizontal processing when each event is independent.
- Keep command output distinct from factual event output.
- Monitor processing latency against the event's value window.
**Don't:**
- Don't rebuild a monolithic ESB under a new name.
- Don't make every signal pass through one central cluster.
- Don't obscure derivation lineage.
- Don't infer global system behavior from one processor's local view.
- Don't add a feedback edge without a circuit breaker analysis.
- Don't mix unrelated domains in one signal processor.
- Don't emit a “fact” that is actually an untracked command intent.
**Named cases:**
- Real-Time Economy economic analysis.
- SCADA control services.
- Fraud or anomaly detection in event streams.
- Traffic coordination.
- Event routing and transformation.
- Telemetry analysis that emits actionable signals.
**Centralization warning:**
- Central platforms appear simpler.
- Complex adaptive systems require distributed decision making.
- Local platform ownership often wins over enterprise-wide control.
- Use a common event contract to connect local signal domains.
*Ref: Flow Architectures.md — "The Signal Pattern"; "Command and control"; "Stateful Stream Processing"*
---
### 34. Apply the Facilitator Pattern to Real-Time Matching
**Principle:** Use the Facilitator pattern when a broker matches sellers and buyers, producers and consumers, or supply and demand, then signals the parties or completes a transaction.
**Do:**
- Define the offered resource.
- Define the requested resource.
- Normalize identities sufficiently for matching.
- Prevent the same unique resource from being committed twice.
- Scale matching independently from participants.
- Signal both parties when a match occurs.
- Preserve an auditable decision trail.
- Keep market rules explicit.
- Separate protocol-level event exchange from application-level transaction correctness.
- Design for the cold-start problem on both sides of the market.
- Evaluate whether settlement belongs inside or after the facilitator.
**Don't:**
- Don't call every signal processor a facilitator.
- Don't assume a matching event completes the underlying transaction.
- Don't put double-sale prevention into the transport without a clear reason.
- Don't hide conflicts or race conditions.
- Don't build only for seller scale or only for buyer scale.
- Don't assume compensation is required; “seller” and “buyer” are role labels in the book's explanation.
- Don't underestimate marketplace governance.
**Named cases:**
- LoadLeader matching spare shipping capacity to partial loads.
- Securities markets matching asks and bids.
- Uber matching riders and drivers.
- Google AdWords matching ads and opportunities.
- Any future flow marketplace matching event supply and demand.
**Scale evidence cited by the source:**
- Dow Jones averaged roughly 406 million transactions per day in the cited period.
- Uber provided roughly 18 million trips per day in 2019.
- Google AdWords served more than 29 billion ads per day on average.
- Use these as evidence that matching can scale, not as architecture blueprints.
*Ref: Flow Architectures.md — "The Facilitator Pattern"; "The WWF in Transportation"*
---
### 35. Classify Use Cases with Collison's Four Categories
**Principle:** Classify the activity as addressing/discovery, command/control, query/observability, or telemetry/analytics before choosing a flow pattern and processing architecture.
**Do:**
- Ask whether agents are dynamic and must be found.
- Ask whether an event demands immediate action.
- Ask whether the consumer wants the state of particular agents.
- Ask whether the consumer wants system-wide behavior and trends.
- Combine categories when the use case genuinely spans them.
- Map categories to Collector, Distributor, Signal, or Facilitator shapes.
- Select stateless, stateful, log-based, workflow, or API processing after classification.
- Revisit classification as scope changes.
**Don't:**
- Don't treat every stream as telemetry.
- Don't confuse service discovery with public stream discovery.
- Don't use system-wide analytics when one agent query is enough.
- Don't force asynchronous flow onto a simple synchronous object query.
- Don't centralize command and control without considering edge deployment.
- Don't ignore identity and duplicate handling in discovery.
**Addressing and discovery:**
- Track which agents exist.
- Assign or recognize identities.
- Publish join, change, and leave events.
- Use registration services when agents can call a known API.
- Use discovery services when they cannot.
- Handle high rates of agent creation and deletion.
**Command and control:**
- Connect sources to decision and action services.
- Use centralized stateless processors for simple independent decisions.
- Use stateful processors when current system state matters.
- Use distributed edge controllers for localized decisions and scale.
- Distinguish message conversations from one-way events.
**Query and observability:**
- Query specific agents synchronously through APIs when they have stable endpoints.
- Use asynchronous events when agent sets are dynamic or connectivity is intermittent.
- Choose many targeted topics or broader streams with consumer filtering.
- Balance producer-side sorting against consumer-side processing.
**Telemetry and analytics:**
- Collect large volumes from many agents.
- Analyze system behavior rather than one object.
- Use near-real-time analysis where delayed insight loses value.
- Consider Collector, Distributor, or Signal shapes according to fan-in and fan-out.
*Ref: Flow Architectures.md — "Flow Use Cases"; "Addressing and discovery"; "Command and control"; "Query and observability"; "Telemetry and analytics"*
---
### 36. Run EventStorming as a Cross-Functional Event Timeline
**Principle:** Use Alberto Brandolini's EventStorming to expose how people, systems, commands, policies, and events cooperate across a business activity.
**Do:**
- Select a business activity or complex process.
- Provide a long physical workspace or a large virtual board.
- Invite business leaders and subject-matter experts.
- Invite user-experience designers, developers, and architects.
- Ask participants to identify meaningful events.
- Write events on orange sticky notes.
- Place events on a timeline from earliest to latest.
- Debate and revise the event set and order.
- Add human users on yellow notes.
- Add external systems on pink notes.
- Add commands that initiate events.
- Add policies on purple notes.
- Add outputs to users and external systems.
- Mark constraints and unresolved issues with hot-pink notes.
- Use the final model to expose external integration opportunities.
**Don't:**
- Don't run the workshop with engineers alone.
- Don't begin with service names or database tables.
- Don't suppress disagreement about the real timeline.
- Don't omit manual activities.
- Don't omit external systems.
- Don't confuse commands with events.
- Don't hide constraints discovered during the discussion.
- Don't assume every outgoing external signal should be asynchronous.
**Seven source steps:**
1. Identify the business activity to model.
2. Provide sufficient meeting and wall space.
3. Invite key stakeholders and translators of domain expertise.
4. Identify interesting or required events.
5. Arrange events along a timeline.
6. Add users, external systems, commands, policies, and outputs.
7. Highlight constraints and outstanding issues.
**Flow extraction:**
- An incoming external event is a clear flow candidate.
- An outgoing signal needing an immediate response is often better served by an API.
- An asynchronous outgoing signal is a candidate for event- or message-driven integration.
- Use the model to find hidden waiting, conversion, and coordination work.
*Ref: Flow Architectures.md — "Modeling Flow"; "The 10,000-Foot View of EventStorming"*
---
### 37. Make Architecture Event-First
**Principle:** Decide first whether communication expresses intent or fact, whether facts are discrete or serial, and whether handling requires one action or a workflow.
**Do:**
- Start from the event and its business meaning.
- Define functional requirements.
- Define event volume and processing scale.
- Define resilience and performance commitments.
- Decide between messaging and eventing.
- For eventing, decide between discrete events and event series.
- For discrete events, decide between single action and workflow.
- Use the decision tree as guidance rather than a rigid law.
- Minimize producer-consumer promises for highly scalable discrete eventing.
- Preserve order and history for event series.
- Use stateful processing when accurate live entity state dominates.
- Document how consumers connect and receive events.
**Don't:**
- Don't choose Kafka, functions, or workflows before classifying the communication.
- Don't call commands facts.
- Don't force a conversation where a broadcast fact suffices.
- Don't discard sequence when history creates meaning.
- Don't create a workflow for one bounded action.
- Don't split one workflow into untracked function chains.
- Don't claim the decision tree forbids hybrids.
**Messaging:**
- Use when producer and consumer coordinate a task.
- Maintain enough state to understand the conversation.
- Expect acknowledgment or completion messages.
- Accept added coordination, latency, and scale cost.
- Localize conversations at the edge where possible.
**Eventing:**
- Use when the producer communicates facts.
- Let consumers join and leave without disrupting the producer.
- Avoid producer dependence on consumer outcomes.
- Prefer this looser coupling for broad WWF-style experimentation.
**Discrete event:**
- Let the event stand alone.
- Push it to interested consumers.
- Include payload or a payload URI.
- Minimize delivery and history promises unless required.
**Event series:**
- Preserve relationships among events.
- Use pull and replay where consumers need ranges.
- Retain ordered history.
- Use logs for scalable series access.
*Ref: Flow Architectures.md — "Event-First Use Cases for Flow"; "Messaging Versus Eventing"; "Discrete Events Versus Event Series"*
---
### 38. Separate Single Actions from Workflows
**Principle:** Route one-event/one-action handling to a bounded processor; use a workflow engine when multiple dependent steps must retain process state over time.
**Do:**
- Route a single discrete event to one responsible function or service.
- Use an event router or queue to decouple delivery.
- Use cloud event routers where their ecosystem fits.
- Use Knative Eventing for Kubernetes-based routing where appropriate.
- Keep single-action functions independently deployable.
- Use a workflow definition for multi-step processing.
- Version workflow definitions.
- Let workflows wait for related events or human action when needed.
- Keep process state in the workflow mechanism.
- Decouple the process definition from step implementations.
- Permit third-party actions at explicit workflow boundaries.
**Don't:**
- Don't use a workflow engine for trivial routing.
- Don't represent a durable process as an undocumented chain of queues and functions.
- Don't assume a single function can safely own long-running coordination.
- Don't hide process state in transient memory.
- Don't let one step's implementation define the whole workflow.
- Don't confuse a digital-twin graph with a workflow.
- Don't claim an event is fully handled before required workflow steps complete.
**Single-action examples:**
- Azure Event Hubs routing.
- Google Pub/Sub routing.
- AWS EventBridge routing.
- Knative Brokers and Triggers.
- AWS Lambda or another function handling one event.
- A stateful processor updating a live entity model.
**Workflow examples:**
- Insurance claim processing.
- Medical triage.
- AWS Step Functions.
- Azure Logic Apps.
- Robotic process automation.
- A process waiting for a human or related event.
**Decision rule:**
- Choose a function for one bounded action.
- Choose a stateful stream processor for a network of agents reacting from live state.
- Choose a workflow engine for a defined sequence of interdependent actions.
- Keep all three connected through explicit event contracts.
*Ref: Flow Architectures.md — "Single Actions Versus Workflows"; "Single actions"; "Workflows"*
---
### 39. Choose Flow or Request-Response by Interaction Semantics
**Principle:** Use request-response for a synchronous answer from a known endpoint; use flow for asynchronous, timely facts from dynamic or independently operated producers.
**Do:**
- Use an API when a consumer needs an immediate response.
- Use an API to query a specific object with a stable endpoint.
- Use an API when the producer action is known and explicitly requested.
- Use flow when data should arrive without repeated polling.
- Use flow when consumers are not known in advance.
- Use flow when consumers should join and leave independently.
- Use asynchronous events when network availability or scale makes synchronous exchange unsuitable.
- Use messaging when two-way coordination is required but asynchronous handling is valuable.
- Use Webhook-style callbacks for flow-friendly discrete-event push where appropriate.
- Combine HTTP connection setup with a streaming protocol when that layering fits.
**Don't:**
- Don't poll an API continuously to simulate event push unless no streaming option exists.
- Don't publish an event when the caller needs a synchronous result before proceeding.
- Don't force every object query through a stream.
- Don't force every event notification through request-response.
- Don't make the producer call every consumer-specific API if a consumer-provided callback or topic decouples them.
- Don't claim flow replaces APIs.
- Don't claim event-driven architecture replaces other distributed application styles.
**Flow wins when:**
- State changes must be communicated as they happen.
- Many independent consumers may care.
- Producers should not depend on consumer availability.
- Consumer membership is dynamic.
- Replay or stream memory matters.
- Cross-organizational experimentation benefits from standard connection and metadata.
**Request-response wins when:**
- The consumer asks a specific question now.
- A known resource owns the answer.
- The caller needs synchronous success or failure.
- The interaction is naturally point-to-point.
- A direct response is simpler than correlating asynchronous messages.
- Event history and fan-out add no value.
**Hybrid rule:**
- Use HTTP or another request-response interface to discover, authenticate, and establish a subscription.
- Push events after connection.
- Use an API to retrieve a large or protected payload referenced by event metadata.
- Keep the semantic boundary explicit.
*Ref: Flow Architectures.md — "Flow and Event-Driven Architectures"; "Query and observability"; "Modeling Flow"; "Discrete events"*
---
### 40. Use Streaming SQL and Analytics at the Right Sink
**Principle:** Use stream-native query and analytics tools for near-real-time event insight; move data to traditional stores for historical analysis and other at-rest workloads.
**Do:**
- Use SQL-like stream tools when they reduce custom series-processing code.
- Query event series directly when order and recent history matter.
- Use streaming analytics for live statistics, correlation, and dashboards.
- Emit derived events when analysis should trigger further action.
- Use traditional warehouses for historical analysis at rest.
- Select sinks by volume, event type, existing environment, and access pattern.
- Update current state in a database when that is the actual consumer need.
- Preserve raw event history separately when audit or replay requires it.
- Distinguish a processor that retransmits from a sink that terminates the event path.
- Treat Kafka-like logs as specialized event stores, not universal databases.
**Don't:**
- Don't dump every stream into a relational database before time-sensitive processing.
- Don't use an active log as a general-purpose analytical store without evaluating access patterns.
- Don't call a dashboard the only possible sink.
- Don't call a processor a sink if it forwards the event.
- Don't claim Materialize is covered by the source.
- Don't claim the source compares modern streaming SQL engines beyond its named examples.
- Don't delay all insight to an overnight batch when near-real-time action has value.
**Named streaming-query and analytics examples:**
- ksqlDB/KSQL.
- Amazon Kinesis Data Analytics.
- Microsoft Azure Stream Analytics.
- Google Dataflow.
- Rockset.
- Apache Flink.
- Apache Druid.
- Tableau Online.
- AWS Redshift.
- Azure Synapse Analytics.
- Google BigQuery.
- IBM Data Warehouse.
- SAP HANA.
**Source boundary:**
- The book names ksqlDB as an event database connected to Kafka topics with SQL syntax.
- It says this can save development time for large event-series workloads.
- It names Flink in stream processing and streaming analytics contexts.
- It does not discuss Materialize.
- It does not offer a detailed comparative benchmark among streaming SQL systems.
**Sink categories:**
- Relational databases.
- NoSQL document and key-value stores.
- Event logs.
- Historical analytics platforms.
- Near-real-time streaming analytics.
- Event-aware applications and services.
- Human-facing interfaces.
*Ref: Flow Architectures.md — "Series events"; Appendix "Sinks"; "Streaming Analytics"; "Event data stores and databases"*
---
### 41. Optimize Cost Across Compute, Network, Storage, and Labor
**Principle:** Optimize the cost of useful event outcomes, not only broker throughput or compute time.
**Do:**
- Count development, testing, connectors, network, low-latency links, brokers, processors, serverless execution, retention, replay, schemas, discovery, security, and operations.
- Buy managed commodity capacity when its promises fit; build differentiating domain logic.
- Filter or aggregate at the edge to reduce core traffic and global distribution.
- Send payload URLs when most consumers ignore the payload and retrieval latency is acceptable; embed payloads for immediate action.
- Set the shortest retention that satisfies replay, audit, and consumer promises.
- Recalculate capacity after lower integration cost increases demand.
**Don't:**
- Don't optimize unit cost while ignoring Jevons-paradox volume growth, open-source operations, portability, or regional placement.
- Don't retain everything, distribute globally, or add payload fetches by default.
**Trade-offs and sequence:**
- Stronger coordination consumes compute and network; provenance adds latency; retention adds storage; edge adds distributed operations.
- Confirm value → remove bespoke connection work → avoid unnecessary messaging state → localize processing → bound memory → select by total cost → resize for adoption.
*Ref: Flow Architectures.md — "Lowering the Cost of Stream Processing"; "Messaging"; "Discrete events"; "Retention"; "Memory"*
---
### 42. Drive Standards Through Markets, Communities, and Running Code
**Principle:** Participate in standards, open source, trade groups, and ecosystems because no single vendor or document can create the WWF alone.
**Do:**
- Participate in IETF work relevant to TLS, WebSocket, and HTTP.
- Participate in OASIS work relevant to MQTT and AMQP.
- Follow CNCF CloudEvents metadata, subscription, and discovery work.
- Implement standards in running code.
- Report implementation failures back to standards communities.
- Join trade groups with shared integration needs.
- Form an alliance when no suitable group exists.
- Define industry payload contracts collaboratively.
- Build ecosystem partnerships around valuable streams.
- Use open source alliances to prove interoperable operations events.
- Encourage both producers and consumers.
- Prepare for standards to emerge organically from adoption.
**Don't:**
- Don't expect a standards body to impose adoption.
- Don't create a competing specification before understanding existing efforts.
- Don't wait passively for a final winner.
- Don't rely on one vendor's proprietary format as a universal standard.
- Don't assume specifications without user adoption create a market.
- Don't ignore government influence on public and private standards.
- Don't assume consensus eliminates vendor or enterprise inertia.
**Named communities and projects:**
- IETF.
- OASIS.
- CNCF.
- W3C.
- Apache Kafka.
- Apache Pulsar.
- Apache Beam.
- Apache Flink.
- Apache Heron.
- Apache NiFi.
- Apache Samza.
- Apache Storm.
- Apache Druid.
- gRPC.
- NATS.io.
- Argo.
- Kubernetes.
- Postgres.
- ActiveMQ.
**Trade and ecosystem examples:**
- IFX Foundation and Nacha.
- FDX.
- Health-information coordination through government agencies.
- AWS's AMI, Docker-container, and S3-event conventions.
- Open source operational events using CloudEvents.
- Industry-specific financial transaction streams.
*Ref: Flow Architectures.md — "Driving Technology Development"; "Standards bodies"; "Open source projects"; "Trade groups"; "Ecosystem partnerships"; "Open source alliances"*
---
### 43. Plan for Inertia and Unpredictable Innovation
**Principle:** Use standards games, network effects, cocreation, and phased adoption to move flow forward while expecting vendor resistance, enterprise delay, and unforeseen applications.
**Do:**
- Use Wardley gameplay to test strategic options.
- Support open approaches that accelerate network effects.
- Cocreate with partners that share a valuable use case.
- Differentiate on data, algorithms, quality, and price after interfaces commoditize.
- Start enterprise exploration before the market is fully settled.
- Use greenfield or bounded projects to demonstrate value.
- Budget roughly three stages for major enterprise adoption: exploration, first rollout, then scale.
- Keep proprietary systems connected through bridges during transition.
- Treat current maps as incomplete.
- Preserve architecture adaptability for “here be dragons” innovation.
- Reassess after security breaches, regulation, or market shifts.
**Don't:**
- Don't assume first-mover status guarantees a durable advantage.
- Don't assume cloud providers will immediately abandon ecosystem lock-in.
- Don't force a full replacement before value is proven.
- Don't underestimate complex IT portfolios.
- Don't predict exact future consumers of commoditized flow.
- Don't mistake a speculative map for certainty.
- Don't ignore ethical and regulatory consequences of strategic plays.
**Gameplay highlighted by the book:**
- Standards game.
- Exploiting network effects.
- Cocreation.
- Alliances.
- Open approaches.
- Market enablement.
- Differentiation.
- Managing inertia.
- Education.
- Cooperation.
**Enterprise adoption observation:**
- Year one often focuses on fit and exploration.
- Year two often focuses on prototypes, planning, and first uses.
- Year three often focuses on scaling.
- Legislation or immediate ROI can accelerate the pattern.
- Treat the timeline as the author's field observation, not a universal law.
**Here-be-dragons rule:**
- Commodity integration creates applications that cannot be predicted from today's market.
- Preserve cheap composition and experimentation.
- Avoid freezing the architecture around only known use cases.
- Expect the most valuable network effects to come from unexpected consumers.
*Ref: Flow Architectures.md — "Gameplay"; "Market: Standards Game"; "Accelerators: Exploiting Network Effects"; "Ecosystem: Cocreation"; "Inertia"; "Here Be Dragons"*
---
#### Source-Bounded 2021 Market Inventory
**Principle:** Catalog examples by the promise they make and their Wardley position; treat the appendix as illustrative, not exhaustive.
- **Infrastructure:** AWS, Azure, GCP; HPE, Dell, Lenovo, Cisco, NetApp; VMware ESX, Hyper-V, Xen; Docker, OCI, Kubernetes, Knative, Helm.
- **Connections:** IP, TCP, QUIC, HTTP, MQTT, WebSocket, Synadia NGS.
- **Interfaces:** Kafka Consumer API, Kafka Connect/Sink API, EdgeX API, CloudEvents Subscription API, REST, subjects/topics.
- **Sources:** environmental, inertial, fusion, and trigger sensors; converters; agents; web/mobile/desktop apps; public/private feeds; Twitter; stock tickers; PubNub; Socket.io; Stream.
- **Processors:** Kafka, Pulsar, Storm, Flink, Spring Cloud Stream, Faust, JavaScript Streams API, SwimOS, Lambda, Step Functions, Microsoft/Google Functions, VANTIQ, OutSystems, Mendix, Spring WebFlux, Akka, Vert.x, ReactiveX, Lightbend, Netifi, RSocket.
- **Sinks:** Oracle and Microsoft RDBMSs; MongoDB, Cassandra, DynamoDB, Cosmos DB, Azure Table Storage, Google Cloud Datastore; Elasticsearch, Splunk; IBM, SAP, TIBCO, Tableau; Redshift, Synapse, BigQuery; Kinesis Data Analytics, KSQL, Rockset, Azure Stream Analytics, Google Dataflow.
- Preserve the source's 2021 maturity judgments; define scope, primary promise, dependent promises, differentiated promise, and evolutionary position before comparing products.
*Ref: Flow Architectures.md — Appendix "Evaluating the Current Flow Market"*
---
## Anti-Patterns & Common Mistakes
- **Solution looking for a problem:** Adopt event infrastructure without a valuable timely-data need → *fix:* identify the integration pain and value window first.
- **Flow by label:** Rename batch transfer or synchronous APIs as flow → *fix:* test the five defining flow properties.
- **Polling as real time:** Repeatedly query a producer for changes → *fix:* use push when independent event notification is the actual need.
- **Context-free bytes:** Send raw payloads and expect consumers to infer origin and meaning → *fix:* package contextual metadata with state changes.
- **Envelope-as-domain-model:** Treat CloudEvents fields as the business payload schema → *fix:* maintain a separate payload contract.
- **Transport-as-security:** Assume TLS on one hop protects a multi-hop event path end to end → *fix:* define payload, identity, and provenance controls.
- **Schema-registry confusion:** Treat registered schemas as discoverable streams → *fix:* publish topic, URI, rate, policy, and schema information together.
- **Universal-registry optimism:** Build a global catalog before streams and users exist → *fix:* start with accurate web pages or scoped registries.
- **Connector captivity:** Depend on a contextual platform for behavior it cannot extend → *fix:* preserve composable interfaces and a code escape path.
- **ESB rebirth:** Centralize all routing, transformation, policy, and process control → *fix:* distribute domain decisions while standardizing exchange.
- **Function pinball:** Chain event-triggered functions without an explicit process model → *fix:* use bounded actions or a workflow engine.
- **Conversation for a fact:** Use messaging state for one-way notification → *fix:* choose eventing and reduce promises.
- **Fact for a command:** Publish an intent as if it were an immutable occurrence → *fix:* distinguish command semantics from event semantics.
- **Series flattened to discrete:** Drop ordering and history from related observations → *fix:* use an ordered retained log.
- **Queue as memory:** Expect acknowledged transient messages to remain replayable → *fix:* use a log with explicit retention.
- **Log as universal database:** Force every query and workload onto an event log → *fix:* route suitable data to purpose-built sinks.
- **Exactly-once inflation:** Extend a broker delivery label into an end-to-end application guarantee → *fix:* scope the promise and plan duplicate handling.
- **Unbounded retention:** Keep every event indefinitely → *fix:* set retention from replay, audit, privacy, and cost needs.
- **Unbounded buffering:** Absorb slow consumers in memory → *fix:* bound buffers and define flow-control behavior.
- **Global ordering assumption:** Treat partition order as whole-topic order → *fix:* define the actual ordering scope.
- **Bad partition key:** Scatter one entity's dependent events or create hot partitions → *fix:* key by processing and ordering needs.
- **Stateful overkill:** Build digital twins for stateless conversion → *fix:* use the simplest processor that satisfies the decision.
- **Workflow underkill:** Hide durable process state in chained handlers → *fix:* model and version the workflow.
- **Central-cloud reflex:** Send local event traffic across distant infrastructure → *fix:* process and aggregate at the edge when valuable.
- **Edge magic:** Claim edge removes source-to-global-replica distance → *fix:* measure every leg and expose regional delay.
- **Dashboard-only operations:** Observe a failure without a safe corrective lever → *fix:* pair observability with controllability.
- **Silent push failure:** Assume no events means nothing happened → *fix:* define liveness and expected-rate signals.
- **Circular dependency:** Let A→B→C actions trigger A indefinitely → *fix:* trace event identity and insert circuit breakers.
- **Local-correctness fallacy:** Declare a system safe because each component is well designed → *fix:* test emergent system behavior.
- **Provenance laundering:** Replace origin when transforming an event → *fix:* append lineage and integrity evidence.
- **Open-equals-free:** Assume an open protocol forbids paid streams → *fix:* separate interoperable connection from licensing and pricing.
- **Cloud-ecosystem myopia:** Treat proprietary event formats as WWF standards → *fix:* identify adapters and common metadata boundaries.
- **Maturity inflation:** Present product-stage discovery or metadata as commodity → *fix:* use Wardley evidence and adoption.
- **Map as prophecy:** Treat speculative evolution as guaranteed → *fix:* use maps to challenge options and update them.
- **Promise overreach:** Make one autonomous agent responsible for another's behavior → *fix:* promise only controllable outcomes.
- **Immediate-standard fantasy:** Expect large enterprises to switch stacks instantly → *fix:* phase exploration, rollout, and scale.
- **Current-market anachronism:** Attribute later technologies to a 2021 book → *fix:* mark source boundaries explicitly.
---
## Decision Heuristics / Checklists
### Flow qualification checklist
- Confirm a meaningful state change, a decaying value window, and a benefit from push over polling or batch.
- Confirm consumers may be unknown or independently joining/leaving, while the producer retains access and transmission control.
- Confirm metadata, payload, security, operations, and retention costs are justified; otherwise use request-response or batch.
### Messaging versus eventing checklist
- Intent, conversation state, completion, or acknowledgment → messaging.
- Independent fact, optional consumers, and safe disconnect → eventing.
- Minimize promises in either model.
### Discrete versus series checklist
- Standalone fact with payload or URI → discrete push.
- Meaning depends on order, ranges, history, or replay → ordered retained series.
- State the actual ordering and retention scope.
### Single action versus workflow checklist
- One processor and no durable inter-step state → bounded function or service.
- Dependent steps, waits, people, or later events → workflow engine.
- Network of agents reacting from live shared state → stateful graph.
### Collector checklist
- Count producers; define connection initiation, source identity, duplicate detection, normalization, buffering, noisy-source isolation, and lineage.
- Partition ingestion before fan-in scale overwhelms one endpoint.
### Distributor checklist
- Count and locate consumers; define regional partitions, replication delay, simultaneous-delivery needs, slow-consumer isolation, churn, and jurisdiction policy.
- Never imply that edge replication removes source-to-region delay.
### Signal checklist
- Define input facts, decision, output fact or command, state needs, lineage, processing budget, feedback paths, and circuit breaker.
- Keep each signal processor bounded.
### Facilitator checklist
- Define offers, requests, identities, matching scale, race and double-commit prevention, completion, audit, and two-sided adoption.
- Keep transaction correctness in the application unless the protocol truly owns it.
### Protocol checklist
- Decide point-to-point versus pub/sub, directionality, device constraints, payload size, browser/proxy needs, transport flow control, metadata binding, and security per hop and end to end.
- Keep connection, transport, event metadata, and domain payload responsibilities separate.
### Schema and metadata checklist
- Identify type, source, event ID, occurrence time, subject, content type, contract location, unsupported-version behavior, and independent-change rules.
- Keep stream and schema registries distinct but linked.
### Log, partition, and guarantee checklist
- Define replay, ordering scope, key, hot-partition risk, retention, recovery horizon, deterministic reconstruction, and long-term sink.
- Scope at-most-once, at-least-once, or exactly-once to the component making the promise; test redelivery and weaker end-to-end outcomes.
### Backpressure checklist
- Define sustainable consumer rate, bounded buffers, producer modulation, expiration or rejection, catch-up, consumer isolation, overload signals, and corrective controls.
- Treat buffering as deferred pressure, not pressure removal.
### Timeliness checklist
- Define value half-life, maximum latency, network path, processing steps and budgets, parallelism, edge placement, availability duration, and forgetting policy.
- Optimize for available-while-valuable, not vague “real-time.”
### Security and manageability checklist
- Define authentication, subscription authorization, TLS hops, payload encryption, keys, broker identity, integrity, provenance, metadata disclosure, and audit.
- Define liveness, expected rate, connection errors, retries, alternate routes, configuration, tracing, observability cost, and circuit breakers.
### Cost checklist
- Count bespoke code, connectors, network, brokers, processors, serverless execution, active retention, sink storage, security, provenance, and edge operations.
- Model higher total volume after unit costs fall.
### Wardley and Promise Theory checklist
- State scope, users, need, components, visibility, Genesis → Commodity/Utility position, and expected movement.
- Trace each lower component's autonomous promise upward; remove false links and classify gaps as build, buy, standardize, or watch.
---
## Key Takeaways
1. Define flow by self-service subscription, producer control, push delivery, and standard network protocols.
2. Add context to state changes so consumers receive events, not unexplained bytes.
3. Treat flow interaction as the source of value; transport alone only moves data.
4. Use the WWF as a strategic thesis, not as an already deployed standard.
5. Start from business urgency and measurable timeliness value.
6. Use value stream mapping to remove the dominant lead-time or process-time constraint.
7. Expect cheaper integration to increase total demand through the Jevons paradox.
8. Prefer composable interfaces over contextual platforms that block unanticipated behavior.
9. Engineer security, agility, timeliness, manageability, and memory together.
10. Map user needs and components on the Wardley evolution axis.
11. Validate every dependency with promises made by autonomous agents.
12. Separate logical connection, discovery, metadata, payload, source, processor, queue, sink, and infrastructure.
13. Use queues for asynchronous decoupling and logs for ordered memory.
14. Scope delivery guarantees to the component that can actually keep them.
15. Avoid rebuilding centralized ESB control in event-platform form.
16. Use MQTT for lightweight brokered pub/sub where its constraints fit.
17. Layer IP, TCP/QUIC, HTTP/WebSocket, messaging, metadata, and payload protocols deliberately.
18. Use CloudEvents for common context, not as a universal domain schema.
19. Keep schemas, stream discovery, and payload contracts separate but linked.
20. Publish discoverable stream metadata before the ecosystem becomes unmanageable.
21. Use serverless functions for bounded actions and workflows for durable processes.
22. Partition event logs according to ordering and consumer-access needs.
23. Use event sourcing only when ordered history is intentionally authoritative.
24. Use stateful processors when decisions require a live graph of related entities.
25. Bound reactive buffers and define flow control; nonblocking code does not eliminate overload.
26. Define timeliness as both latency and retention.
27. Scale with local, regional, and core flows rather than one universal center.
28. Combine connection security, payload protection, authorization, and provenance.
29. Treat intellectual-property control and monetization as producer-adoption requirements.
30. Pair observability with controllability.
31. Detect circular dependencies and stop them with circuit breakers.
32. Name the flow pattern: Collector, Distributor, Signal, or Facilitator.
33. Classify the use case: addressing/discovery, command/control, query/observability, or telemetry/analytics.
34. Use EventStorming to discover the real event timeline and external boundaries.
35. Decide messaging versus eventing before selecting infrastructure.
36. Decide discrete versus series before selecting retention and routing.
37. Decide single action versus workflow before composing processors.
38. Prefer request-response for synchronous questions to known resources.
39. Prefer flow for asynchronous facts, dynamic consumers, fan-out, and replay.
40. Optimize total outcome cost across labor, network, compute, storage, security, and operations.
41. Drive standards through running code, communities, trade groups, and adoption.
42. Plan for vendor and enterprise inertia.
43. Preserve adaptability because commoditization creates unpredictable applications.
44. Keep every market claim bounded to the book's 2021 source.
---
## Cross-References
- Related: [[../Building_Event-Driven_Data_Mesh.md]]
- Related: [[../Building_Event-driven_Microservices.md]]
- Related: [[../Communication_Patterns.md]]
- Related: [[../Designing_Distributed_Systems.md]]
- Related: [[../Fundamentals_of_Software_Architecture.md]]
- Related: [[../Learning_API_Styles.md]]
- Related: [[../Mastering_Api_Architecture.md]]
- Related: [[../Microservices_Up_And_Running.md]]
- Topic index: [[../INDEX.md]]
