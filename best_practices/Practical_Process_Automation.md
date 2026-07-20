# Per-Book Best Practices — Deep Dive: Practical Process Automation

# Practical Process Automation: Orchestration and Integration in Microservices and Cloud Native Architectures
**Author:** Bernd Ruecker (O'Reilly, 2021)
**Topic tags:** `#architecture` `#workflow` `#api` `#systems`
**Language focus:** Language-agnostic (Java/Spring Boot + BPMN examples)
**Sources:** `markdown_output/Practical Process Automation/Practical Process Automation.md` (no matching summary found)

## TL;DR
Bernd Ruecker argues that any non-trivial coordination of software, humans, decisions, or bots — especially when it is long-running and crosses boundaries — should be automated with a dedicated workflow engine executing a graphical process model (BPMN), not hand-rolled in code. A workflow engine gives you three things you would otherwise rebuild poorly: durable state, scheduling/retries, and versioning — plus operational visibility and an artifact business and IT can discuss together. Apply it whenever you face "Wild West integrations", distributed transactions/Sagas, event chains that secretly implement a business process, or human-task workflows; respect service boundaries by decentralizing engines and never building your own platform.

---

## Best Practices by Topic

### 1. Distinguish "Process" From "Workflow" Deliberately #workflow #architecture

**Principle:** Use the two terms consistently within your org; the book's rule of thumb is *process = what the business cares about*, *workflow = the tooling (engine) used to automate it*.

**Do:**
- Use "process" (or "business process") when talking about goals and business outcomes.
- Use "workflow" when talking about tooling ("workflow engine", "workflow model").
- Adjust terminology to whatever works for your audience — call it "orchestration engine" or "Saga" with technical folks if it lands better.

**Don't:**
- Don't waste energy arguing which term is "correct"; there is no globally agreed distinction.

*Ref: Practical Process Automation.md — "Business Processes, Integration Processes, and Workflows"*

---

### 2. Separate "Automation of Control Flow" From "Automation of Tasks" #workflow

**Principle:** Two orthogonal axes exist — automating the control flow between tasks vs. automating the tasks themselves. Full automation of both is *straight-through processing (STP)*.

**Do:**
- Treat the control flow as the part the workflow engine owns.
- Allow humans to remain in the loop on the 10% of non-standard cases; that is still process automation.
- Use human tasks as a deliberate first step toward automation, then replace humans with service tasks incrementally.

**Don't:**
- Don't assume "process automation" means "no humans involved".

*Ref: Practical Process Automation.md — "Process Automation"*

---

### 3. Recognize the Five Drivers That Justify Automation #workflow

**Principle:** Automation pays off when at least one of these is true: high volume of repetitions, standardization, compliance/auditability, need for consistent quality, or information richness.

**Do:**
- Build the business case by mapping your candidate process to one or more of these drivers.
- Use compliance requirements (audit trail, repeatable procedure) as a forcing function to get workflow tooling approved.

**Don't:**
- Don't automate a one-off, highly variant process — the engineering cost will exceed savings.

*Ref: Practical Process Automation.md — "Process Automation"*

---

### 4. Avoid "Wild West Integration" — The Default Anti-Pattern #architecture #api

**Principle:** Ad hoc integration without governance (direct DB access, naive point-to-point REST, DB triggers, brittle CSV-over-FTP) always rots into the same mess: hand-built state tables, homegrown schedulers, custom monitoring scripts, and a single developer who understands it.

**Do:**
- Recognize the early symptoms (a `payment` table with a `status` column, a hand-rolled poller, alerting shell scripts).
- Replace those features with the workflow engine's built-in equivalents (state persistence, scheduler, ops tooling).

**Don't:**
- Don't build a homegrown workflow engine — it will lag existing tools forever.
- Don't access another service's database to integrate with it.
- Don't pile on bespoke alerting scripts when the engine can surface incidents natively.

**Code:** Pseudocode of the "Wild West" homegrown approach Ruecker describes (state + scheduler, hand-built):
```
// every payment request gets inserted with status = open
// a hand-rolled scheduler polls every few seconds and processes open rows
// an exceptional row poisons the whole loop and crashes the scheduler
// a side script watches for unusual states and emails alerts
```

*Ref: Practical Process Automation.md — "Wild West Integrations"*

---

### 5. Lean on the Three Core Capabilities of a Workflow Engine #workflow #systems

**Principle:** A workflow engine is a state machine that is good at waiting and scheduling. Its three core capabilities are *durable state*, *scheduling*, and *versioning* — everything else is optional platforming.

**Do:**
- Push state, retry, and timer logic into the engine; remove it from your application code.
- Expect the engine to handle transactions and concurrent access to the same process instance.

**Don't:**
- Don't reinvent durable state, retry, or versioning in your own DB.

*Ref: Practical Process Automation.md — "Core Capabilities"*

---

### 6. Treat "Waiting" as Persistent State, Not a Blocked Thread #workflow #systems

**Principle:** When the book says a process "waits", it does *not* mean a thread is blocked. The engine persists state, returns the thread, and revives the instance when an external event or timer wakes it.

**Do:**
- Model long waits (hours, days, weeks) as BPMN tasks/timers without worrying about holding resources.
- Understand the persistence model your engine uses (relational DB vs. event-sourced) because it affects operations and scalability.

**Don't:**
- Don't assume "long-running" implies resource consumption — it implies persisted state.

*Ref: Practical Process Automation.md — "Architecture"*

---

### 7. Run the Workflow Engine as a Service by Default #architecture

**Principle:** Two deployment modes exist: as a self-contained service (your app talks to it remotely) or embedded as a library. Service mode is the modern default.

**Do:**
- Prefer service mode for isolation, language-agnostic glue code, and easy provisioning via Docker or a managed cloud service.
- Use embedded mode only when you really need it (e.g., a modular monolith).

**Don't:**
- Don't embed unless you can explain why — support cases around embedded engines are notoriously hard to debug.

*Ref: Practical Process Automation.md — "Architecture"*

---

### 7a. Persistence & Threading: Engine Internals You Must Understand #systems #workflow

**Principle:** Engines typically persist state (process definitions + instances + audit data) in either a relational DB or an event-sourced store. Understand which one — it determines scalability and ops.

**Do:**
- Know that "waiting" means *state in a database*, not a blocked thread — engines return threads between steps.
- For relational engines, verify supported DB products; you operate them.
- For event-sourced engines, expect horizontal scaling and high throughput, but check their ops requirements.
- Treat the engine DB schema as an implementation detail — never write to it directly if an API exists.

*Ref: Practical Process Automation.md — "Architecture"*

---

### 7b. Additional Engine Features: Visibility, Audit, Tooling — All Optional #workflow #systems

**Principle:** Beyond the three core capabilities (state, scheduling, versioning), engines offer *visibility*, *audit data*, and surrounding *tooling*. Good tools make these pluggable/optional so you can adopt incrementally.

**Do:**
- Adopt additional features as you see the need; don't try to use everything on day one.
- Mine audit data for KPIs, bottleneck analysis, and bottleneck discovery.

**Don't:**
- Don't confuse a heavyweight BPM suite (everything bundled, mandatory) with a modern lightweight engine (unbundled, optional).

*Ref: Practical Process Automation.md — "Additional Features of Workflow Platforms"*

---

### 7c. The Workflow Tool Stack Across the Project Life Cycle #workflow

**Principle:** A typical stack flanks the engine with five tool types, used at different life-cycle phases by different stakeholders:

| Tool | Used by | Phase |
|---|---|---|
| Graphical process modeler | Developers (this book's focus) | Design/Implementation |
| Collaboration tool | Analysts + developers + SMEs | Design |
| Operations tooling | Operators | Operation |
| Tasklist application | End users | Operation |
| Business monitoring & reporting | Business stakeholders | Operation |

**Do:**
- Pick tools that let you unbundle the platform — select only what helps.
- Use collaboration tools for *to-be* design, but keep the *executable* model in your Git repo.

*Ref: Practical Process Automation.md — "Typical Workflow Tools in a Project's Life Cycle"*

---

### 7d. Operations Tooling: Detect, Diagnose, Fix at Scale #systems #workflow

**Principle:** Once in production you need tooling to discover, analyze, and solve process problems — including the ability to operate on thousands of stuck instances at once.

**Do:**
- Wire incident alerts into your APM; require root-cause analysis views in the ops tool.
- Make sure the tool supports bulk actions: trigger retries for thousands of instances after an outage, fix corrupt data via GUI, increment version migrations.

**Don't:**
- Don't rely on log scraping + DB inspection + wiki pages of common fixes — that's the legacy way and burns out operators.

*Ref: Practical Process Automation.md — "Operations Tooling"*

---

### 8. A Process Solution = Model + Glue Code + Tests + Forms #workflow #api

**Principle:** The process model is one artifact among several. A "process solution" also includes connectivity code, data transformations, decision logic, user forms, and tests.

**Do:**
- Treat the process solution as a normal development project (Maven, .NET, Node, serverless bundle) that contains the BPMN XML alongside code.
- Keep business entities in your application; the engine should mostly hold references (IDs), not the data itself.

**Don't:**
- Don't expect the engine to store your business entities.
- Don't treat the model as the whole solution.

*Ref: Practical Process Automation.md — "A Process Solution"*

---

### 9. Deploy BPMN With the Application, Not Through a Separate Pipeline #workflow #api

**Principle:** Hook the process model deploy into the normal application start-up or CI/CD pipeline so model and code ship together.

**Code (Spring Boot + Camunda Cloud auto-deploy on startup):**
```
@SpringBootApplication
@EnableZeebeClient
@ZeebeDeployment(classPathResources="customer-onboarding.bpmn")
public class CustomerOnboardingSpringbootApplication {
```

*Ref: Practical Process Automation.md — "An Executable Example"*

---

### 10. Start Process Instances From Your REST/Event Entry Points #api #workflow

**Principle:** When an incoming REST call or message arrives, the controller's job is to start a process instance and return an async-friendly response (HTTP 202 Accepted).

**Code:**
```
@RestController
public class CustomerOnboardingRestController {
 @Autowired
 private ZeebeClient workflowEngineClient;
 @PutMapping("/customer")
 public ResponseEntity onboardCustomer() {
  startCustomerOnboardingProcess();
  return ResponseEntity.status(HttpStatus.ACCEPTED).build();
 }
 public void startCustomerOnboardingProcess() {
  HashMap<String, Object> variables = new HashMap<String, Object>();
  variables.put("automaticProcessing", true);
  variables.put("someInput", "yeah");
  client.newCreateInstanceCommand()
  .bpmnProcessId("customer-onboarding")
  .latestVersion()
  .variables(variables)
  .send().join();
 }
```

*Ref: Practical Process Automation.md — "An Executable Example"*

---

### 11. Connect Glue Code to Service Tasks by Logical Task Type #workflow #api

**Principle:** Use the engine's pub/sub mechanism: a service task declares a logical `taskType` and any worker subscribing to that type executes it. This decouples model from code and lets you scale workers independently.

**Code (Camunda Cloud `@ZeebeWorker`):**
```
@Component
public class CustomerOnboardingGlueCode {
 @Autowired
 private RestTemplate restTemplate;
 @ZeebeWorker(type = "addCustomerToCrm")
 public void addCustomerToCrmViaREST(JobClient client, ActivatedJob job) {
  log.info("Add customer to CRM via REST [" + job + "]");
  // TODO some real logic to create the request
  restTemplate.put(ENDPOINT, request);
  // TODO some real logic to process the response
  // let the workflow engine know the task is complete
  client.newCompleteCommand(job.getKey()).send().join();
 }
```

*Ref: Practical Process Automation.md — "An Executable Example"*

---

### 11a. Applications, Engines, Definitions, Instances: Get the Cardinality Right #architecture #workflow

**Principle:** Think of the engine like a database installation: many process definitions can be deployed, each definition can run zero-to-many instances, and many applications can connect to the same engine.

**Do:**
- Allow a service to deploy multiple related process definitions (e.g., order fulfillment + order cancellation) to one engine.
- Consider separate engines per service for isolation, especially in microservices.

**Don't:**
- Don't assume one engine = one application = one process definition — that needlessly constrains design.

*Ref: Practical Process Automation.md — "Applications, Processes, and Workflow Engines"*

---

### 11b. Reusable DMS Adapter Story: Pragmatic Library Packaging #workflow #api

**Principle:** When a remote API is awkward (e.g., SOAP callback requiring firewall rules), it's legitimate to extract a small *adapter process* into a library that each client deploys into its own engine, instead of forcing cross-engine call activities.

**Do:**
- Package the adapter (process model + glue code) as a versioned library.
- Accept the deployment coupling (clients must update the library) only when the alternative is worse.
- Prefer a clean API call across boundaries whenever you can.

*Ref: Practical Process Automation.md — "Crossing Boundaries Is an API Call"*

---

### 12. Treat BPMN Models as Source Code, Not Documentation #workflow

**Principle:** The BPMN XML file lives in version control alongside code; it is the authoritative blueprint and is executed directly by the engine.

**Code (BPMN XML excerpt for an order fulfillment process):**
```
<?xml version="1.0" encoding="UTF-8"?>
<definitions>
 <!-- Execution semantics understood by a workflow engine: -->
 <process id="OrderFulfillment" isExecutable="true">
  <startEvent id="Event_OrderPlaced" name="Order Placed" />
  <sequenceFlow id="1"
  sourceRef="Event_OrderPlaced" targetRef="Task_RetrievePayment" />
  <serviceTask id="Task_RetrievePayment" name="Retrieve payment" />
  <sequenceFlow id="2"
  sourceRef="Task_RetrievePayment" targetRef="Task_FetchGoods" />
  <serviceTask id="Task_FetchGoods" name="Fetch goods" />
  <sequenceFlow id="3"
  sourceRef="Task_FetchGoods" targetRef="Task_ShipGoods" />
  <serviceTask id="Task_ShipGoods" name="Ship goods" />
  <sequenceFlow id="4"
  sourceRef="Task_ShipGoods" targetRef="Event_OrderDelivered" />
  <endEvent id="Event_OrderDelivered" name="Order delivered" />
 </process>
 <!-- Graphical layout information: -->
 <BPMNDiagram id="BPMNDiagram_1">
  <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="OrderFulfillment">
  <bpmndi:BPMNShape id="_BPMNShape_Event_OrderPlaced"
  bpmnElement="Event_OrderPlaced">
  <dc:Bounds x="179" y="99" width="36" height="36" />
```

**Do:**
- Store `.bpmn` files in Git with the rest of the source.
- Treat the model as living documentation — it cannot drift from execution.

**Don't:**
- Don't hide the model in a vendor-specific repository that drifts from your code repo.

*Ref: Practical Process Automation.md — "Business Process Model and Notation (BPMN)"*

---

### 13. Use BPMN — It Is the Only Mature, Adopted, ISO-Standardized Process Language #workflow

**Principle:** BPMN (ISO/IEC 19510:2013) is the standard; no competing language matches its maturity and tooling ecosystem.

**Do:**
- Learn BPMN — it carries even if you later pick a non-BPMN tool.
- Use BPMN 2.0 XML as the interchange format.

**Don't:**
- Don't reject BPMN because "XML is legacy" — that critique does not survive scrutiny.
- Don't pick a proprietary "lightweight" language; over time it reinvents BPMN badly.

*Ref: Practical Process Automation.md — "Business Process Model and Notation (BPMN)"*

---

### 14. Use Tokens to Reason About Control Flow #workflow

**Principle:** Per the BPMN spec, a *token* is the theoretical concept that travels through a process model. One process instance ≈ one (or more) tokens moving through the model. Engines persist token positions as the instance's state.

**Do:**
- Trace tokens mentally when designing or debugging flows.
- Remember tokens can split (parallel gateway) and merge (synchronization).

**Don't:**
- Don't expect to "clone a car" — tokens clone naturally; physical metaphors break at parallelism.

*Ref: Practical Process Automation.md — "The Token Concept: Implementing Control Flow"*

---

### 15. Pick the Right BPMN Task Type for Each Unit of Work #workflow

**Principle:** BPMN defines task types that refine what "work" means: *service task* (code runs), *user task* (human works via a tasklist), *business rule task* (decision engine), *script task* (engine runs a script).

**Do:**
- Use service tasks for any code-driven step (REST call, DB update, function invocation).
- Use user tasks to delegate to humans.
- Use business rule tasks to invoke a DMN decision.

**Don't:**
- Don't mix user and service semantics in a single task type.

*Ref: Practical Process Automation.md — "Tasks: Units of Work"*

---

### 16. Gateways Steer Flow — Pick Exclusive or Parallel Deliberately #workflow

**Principle:** The *exclusive gateway* picks exactly one outgoing path by data; the *parallel gateway* activates multiple paths concurrently.

**Do:**
- Use exclusive gateways (the BPMN diamond with `X`) for either/or decisions.
- Use parallel gateways when work can proceed independently.
- Note: parallel here means "you can do something else while waiting", not necessarily multithreading.

**Don't:**
- Don't use a parallel gateway when one branch is conditional — that is an exclusive gateway.

*Ref: Practical Process Automation.md — "Gateways: Steering Flow"*

---

### 17. Use Boundary and Intermediate Events for Timeouts and External Triggers #workflow

**Principle:** *Timer events* wait for time to pass; *boundary events* attach to a task and fire if a condition (e.g., a 5-day timeout) is met while the task is active, cancelling the task and diverting flow.

**Do:**
- Attach boundary timers to tasks that have SLAs (e.g., "wait 5 days for payment, else cancel").
- Use intermediate timer events in the sequence flow to wait (e.g., 1 day for right-of-withdrawal).

**Don't:**
- Don't implement SLAs by polling in glue code.

*Ref: Practical Process Automation.md — "Events: Waiting for Something to Happen"*

---

### 18. BPMN "Messages" Are Triggers, Not Broker Messages #workflow #api

**Principle:** A BPMN *message event* represents any external trigger — it could be a method call, a REST callback, or a broker message. The connection to your real transport is glue code.

**Do:**
- Write glue code that subscribes to your message broker and forwards to the engine, or use a vendor connector.
- Use the *event subprocess* to allow a message (e.g., cancellation) to interrupt the process from any state.

**Don't:**
- Don't assume BPMN message events auto-bind to Kafka/Rabbit topics.

*Ref: Practical Process Automation.md — "Message Events: Waiting for a Trigger from the Outside"*

---

### 19. Three Valid Ways to Attach Code to a Process Model #workflow #api

**Principle:** Use (1) **pub/sub** — workers subscribe to task types, (2) **referenced code** — the engine invokes a class/method directly, or (3) **prebuilt connectors** — vendor-provided building blocks.

**Do:**
- Default to pub/sub: it gives polyglot code, independent scaling, control over timeouts, and back-pressure (close the subscription to throttle).

**Don't:**
- Don't use referenced code unless you accept its limitations: single language, engine-thread execution, no temporal decoupling, tight transactional coupling, hard failure investigation.

*Ref: Practical Process Automation.md — "Combining Process Models and Programming Code"*

---

### 20. Pub/Sub Service Tasks — Subscription Pseudocode #workflow #api

**Code (subscribe a handler to a task type):**
```
paymentHandler = new WorkflowLogicHandler() {
public void handle(WorkflowContext context) {
  // Do input mapping of data here
  restRequest = RetrievePaymentRequest
  .paymentReason( context.getVariable('orderId') ) // ...
  // The real logic that is executed, e.g. calling a REST endpoint
  restResponse =
  restEndpoint.PUT(paymentEndpoint, restRequest);
  // Do output mapping of data here
  context.setVariable( 'paymentId', restResponse.getPaymentId()));
  // Let the workflow engine know once we are done
  context.completeServiceTask();
}
```

**Opening the subscription:**
```
subscription = workflowEngineClient
 .subscribeToTaskType("retrieve-payment")
 .handler( paymentHandler )
 .open();
```

**Do:**
- Use long polling–based subscriptions to keep the protocol one-directional (client → engine).
- Close the subscription to back-pressure or pause work when downstream is unavailable.

*Ref: Practical Process Automation.md — "Publish/Subscribe to a Process"*

---

### 21. Prebuilt Connectors: Useful, but Don't Get Locked In #api #workflow

**Principle:** Connectors (HTTP, S3, Slack, etc.) are convenient but proprietary, limited to what the vendor foresaw, and harder to test.

**Code (pseudocode HTTP connector configured in BPMN):**
```
<bpmn:serviceTask name="Retrieve Payment">
 <bpmn:extensionElements>
 <vendorExtension:connector type="HTTP" />
 <vendorExtension:connectorConfig key="method" value="PUT" />
 <vendorExtension:connectorConfig key="url"
 value="http://myPayment/retrieval" />
 </bpmn:extensionElements>
```

**Do:**
- Use connectors when stitching together serverless functions or RPA bots.
- Write glue code in your language of choice whenever you can.

**Don't:**
- Don't rely on connectors alone — you will hit limitations (e.g., multipart forms) with no escape hatch.

*Ref: Practical Process Automation.md — "Using Prebuilt Connectors"*

---

### 22. The Model-vs-Code Decision: Ask Three Questions #workflow #architecture

**Principle:** Default to code for business logic; promote something to the model when one of these is true:
1. You need to wait (state must be persisted).
2. You discuss it regularly with other stakeholders.
3. It crosses a boundary (technical transaction, service, organizational).

**Do:**
- Split a "check customer" step into "verify data" + "score customer" tasks if scoring cost money and the sequence is discussed.
- Add elements for compliance, analytics, or intelligence — even if they only emit a milestone event.

**Don't:**
- Don't draw "graphical programming" with every line of logic in the model.
- Don't dump all logic in one task labelled "the magic happens here".

*Ref: Practical Process Automation.md — "Model or Code?"*

---

### 23. Test Process Models Like You Test Code #workflow

**Principle:** The model is source code — write unit tests (e.g., JUnit) that assert the happy path, gateway decisions, and glue-code wiring. Mock external systems.

**Code (Camunda Cloud + JUnit happy-path test):**
```
@Test
void testHappyPath() throws Exception {
 // simulate an incoming REST call that will kick off a new process instance
 customerOnboardingRest.onboardCustomer();
 // assert that a process was started
 ProcessInstanceEvent pi = assertProcessInstanceStarted();
 // Assert that a job (pub/sub mechanism of the workflow engine) for scoring
 // was created
 RecordedJob job = assertJob(pi, "scoreCustomer");
 assertEquals("TaskScoreCustomer", job.getBpmnElementId());
 assertEquals("customer-scoring", job.getBpmnProcessId());
```

```
// and complete the task, executing some fake logic instead of the real adapter
execute(job, new JobHandler() {
 public handle(JobClient client, ActivatedJob job) {
  // do some fake behavior instead of the real Java code
 }
});
// Verify that human task was created
RecordedHumanTask task = assertHumanTask(pi);
assertEquals("TaskApproveCustomerOrder", task.getBpmnElementId());
// ... maybe do more assertions ...
// and simulate it being completed with approval
Map variables = new HashMap();
variables.put("automaticProcessing", true);
complete(task, variables);
// Assert the next job for the call to the CRM system was created
job = assertJob(pi, "create");
assertEquals("TaskCreateCustomerInCrm", job.getBpmnElementId());
// and trigger its execution with the normal behavior
execute(job);
// A mock rest server was injected into the glue code by Spring,
// so we can verify the right request was sent
mockRestServer
 .expect(requestTo("http://localhost:8080/crm/customer")) //
 .andExpect(method(HttpMethod.PUT))
 .andRespond(withSuccess("{\"transactionId\": \"12345\"}",
 MediaType.APPLICATION_JSON));
assertEnded(pi);
}
```

**Don't:**
- Don't pick a tool that doesn't support automated testing of models.
- Don't make every test a full integration test — mock external services.

*Ref: Practical Process Automation.md — "Testing Processes" / "An Executable Example"*

---

### 24. Version Process Models — Run Parallel or Migrate #workflow #systems

**Principle:** Engines version process definitions. New instances run the new version; existing instances keep their original version unless you migrate them.

**Do:**
- Run versions in parallel for legal/audit reasons or when migration is too costly.
- Migrate when deploying patches/bug fixes or to avoid operational complexity.
- Version glue code and data definitions alongside the model (e.g., reference `customer-scoring-v2`).

**Don't:**
- Don't forget that deserializing old process data requires backward-compatible schemas (make new fields optional).
- Don't accumulate dead code in old versions — periodically clean up.

*Ref: Practical Process Automation.md — "Versioning of Process Solutions" / "Running Versions in Parallel"*

---

### 25. Orchestrate Anything That Has an API — Software, Humans, Decisions, Bots, Things #architecture #api #workflow

**Principle:** In process automation, *orchestration* = coordination. A workflow engine can orchestrate anything reachable by an API call, decision, human tasklist, RPA bot, or IoT connector.

**Do:**
- Mix orchestration targets in one process (a service task calling payment, a user task for an approval, a business-rule task for risk scoring, an RPA bot for the legacy billing UI).

**Don't:**
- Don't confuse this with Kubernetes-style container orchestration — same word, different domain.

*Ref: Practical Process Automation.md — "Orchestrate Anything"*

---

### 26. Microservices: The Process Lives Inside One Service, Not as a Central Platform #architecture #workflow

**Principle:** Per Sam Newman, microservices are "small, autonomous services that work together". The onboarding *process* belongs inside the onboarding *microservice*; using a workflow engine is an internal implementation detail.

**Do:**
- Treat the workflow engine choice as local to the microservice.
- Communicate between services via standard APIs (REST, messaging), not via the BPM platform.

**Don't:**
- Don't reintroduce a central BPM platform that microservices must talk through.

*Ref: Practical Process Automation.md — "Microservices"*

---

### 27. Serverless Functions: Orchestrate Them With a Workflow Engine, Don't Chain Them Ad Hoc #architecture #workflow

**Principle:** Chaining functions via direct calls accumulates latency and partial-failure risk. Chaining them via a broker loses visibility. A workflow engine (also managed/serverless) orchestrates them cleanly.

**Code (anti-pattern — combined function accumulating 7 s of latency):**
```
function onboardCustomer(customer) {
 crmPromise = createCustomerInCrm(customer); // 2 seconds
 billingPromise = createCustomerInBilling(customer); // 100 ms
 // TODO: Wait for 2 promises
 simCard = provisionSimCard(customer); // 1 second
 registerSim(simCard); // 4 seconds
} // --> 7 seconds runtime for onboardCustomer
```

**Code (broker-chain anti-pattern — invisible end-to-end flow):**
```
// callback function registered for message "customerOnboardingRequest"
function onboardCustomer(customer) {
 ... do business logic ...
 send('createCustomerInCrmRequest');
}
// callback function registered for message "createCustomerInCrmRequest"
function createCustomerInCrmRequest(customer) {
 ... do business logic ...
 send('createCustomerInBillingRequest');
}
// callback function registered for message "createCustomerInBillingRequest"
function createCustomerInBilling(customer) {
 ... do business logic ...
}
```

**Do:**
- Use a managed, BPMN-based workflow engine to orchestrate functions (AWS Step Functions / Azure Durable / GCP Cloud Workflows lack BPMN and visualization — prefer BPMN-based alternatives where possible).

*Ref: Practical Process Automation.md — "Serverless Functions"*

---

### 28. Modular Monoliths Can Use Workflow Engines Too #architecture #workflow

**Principle:** Even if you're not breaking up the monolith, embedding an engine as a library gives you state handling and visibility, and lets you change processes without redeploying everything.

**Do:**
- Embed the engine library; orchestrate internal components via local method calls.
- Use process automation to slowly deconstruct the monolith: extract a process into a microservice, add facades in the monolith, remove hardwired connections.

**Don't:**
- Don't force microservices on a 10-person team that masters a monolith — but a 1,000-developer single monolith won't work either.

*Ref: Practical Process Automation.md — "Modular Monoliths" / "Deconstructing the Monolith"*

---

### 29. Orchestrate Decisions With DMN and FEEL #workflow #api

**Principle:** Decision logic changes faster than process flow and is core business logic — extract it into a Decision Model and Notation (DMN) table and invoke it from a BPMN *business rule task*.

**Do:**
- Use FEEL (Friendly Enough Expression Language) for expressions inside DMN and BPMN.
- Pick a hit policy deliberately: "first" (first matching rule wins), unique, collective (sum, etc.).

**Sample DMN decision table (Automatic Processing Applicability, hit policy: First):**

| # | When: Payment Type | And: Customer Region Score | And: Monthly Payment | Then: Manual Check Necessary? |
|---|---|---|---|---|
| 1 | "prepaid" | – | – | false |
| 2 | "invoice" | <50 | – | true |
| 3 | "invoice" | >= 50 | < 25 | false |
| 4 | "invoice" | >= 50 | >= 25 | true |
| + | – | – | – | |

**Code (FEEL expressions allowed in cells):**
```
Party.Date < date("2021-01-01")
Party.NumberOfGuests in [25..100]
not( Party.Cancelled )
```

**Code (invoke a parsed DMN decision):**
```
input = Map
 .putValue("paymentType", "invoice")
 .putValue("customerRegionScore", 34)
 .putValue("monthlyPayment", 30);
decisionDefinition = dmnEngine.parseDecision('automaticProcessing.dmn')
output = dmnEngine.evaluateDecision(decisionDefinition, input)
output.get('manualCheckNecessary')
```

*Ref: Practical Process Automation.md — "Decision Model and Notation (DMN)" / "Decisions in a Process Model"*

---

### 30. Human Task Management: Use the Built-in Lifecycle, Don't Rebuild It #workflow

**Principle:** Most platforms ship a task lifecycle (candidate → claimed → assigned → completed, with delegate/reassign). Configure it via task attributes; do not re-model it in the BPMN flow.

**Do:**
- Route human tasks to *groups* (e.g., "sales"), not specific individuals — accommodates vacation, attrition, new hires.
- Use built-in notification, timeout, escalation, and vacation rules instead of modeling email reminders in BPMN.
- Allow non-employees (customers, suppliers) to be assigned tasks too.

**Don't:**
- Don't model email reminders as explicit BPMN tasks if a configuration can do it.

**Code (BPMN user task with potential owner):**
```
<bpmn:userTask id="Check payment"/>
 <potentialOwner>
 <resourceAssignmentExpression>
 <formalExpression>sales</formalExpression>
 </resourceAssignmentExpression>
```

*Ref: Practical Process Automation.md — "Task Assignment" / "Additional Tool Support"*

---

### 31. Choose the Right User-Task UI Strategy #workflow #api

**Principle:** Three options exist: (1) the vendor's tasklist app (fast start, prototyping), (2) integrate with an existing external tasklist (SAP, Trello, mainframe screens), (3) build a custom app (high customization, grouped tasks).

**Do:**
- Build a custom tasklist when you need to bundle multiple related user tasks into one screen for efficiency.
- Plan for bi-directional state sync and problem detection when integrating external tasklists.

**Don't:**
- Don't forget cancellation flows and data round-tripping when integrating third-party task UIs.

*Ref: Practical Process Automation.md — "The User Interface of User Tasks"*

---

### 32. Orchestrate RPA Bots as Single Service Tasks — Not Whole Processes #workflow #architecture

**Principle:** RPA bots are brittle wrappers around GUIs without APIs. Use them only as one service task inside a BPMN-driven process; never use RPA tooling as a low-code process automation platform.

**Do:**
- Use RPA for the 80% happy path; route exceptions to a human-task fallback.
- Plan to replace each bot with a real API as soon as feasible; treat every new bot as technical debt to be reported.

**Don't:**
- Don't let RPA bots own business process flow — that becomes an unmaintainable low-code monolith.

*Ref: Practical Process Automation.md — "Orchestrate RPA Bots"*

---

### 33. Orchestrate IoT by Bridging Streams to Process Instances #workflow #systems

**Principle:** Stream processors derive insights (e.g., "low oil pressure"); start a process instance per insight. Use a stateful connector to dedupe so the same insight doesn't start multiple instances, and route follow-up events into the existing instance.

**Do:**
- Cancel the process instance when the underlying condition returns to normal.

*Ref: Practical Process Automation.md — "Orchestrate Physical Devices and Things"*

---

### 34. Champion BPMN/Engines by Knowing the Limitations of Alternatives #workflow #architecture

**Principle:** Each alternative to a workflow engine (hardcoded processes, batches, data pipelines, actor model, stateful functions) has documented shortcomings — know them so you can justify the engine.

**Do:**
- Cite "batches add latency, lack visibility, are hard to recover" — for batch processing.
- Cite "pinball-machine architecture, no visibility, acyclic-only, hard to operate" — for streaming/data pipelines.
- Cite "no modeling language for long-running patterns, source code buried logic, limited industry adoption" — for the actor model.
- Cite "no graphical representation, limited scheduling/versioning, basic operations tooling" — for stateful functions.

**Don't:**
- Don't reject workflow engines based on a gut feeling about BPMN/XML — investigate the actual trade-offs.

*Ref: Practical Process Automation.md — "Limitations of Other Implementation Options"*

---

### 34a. Data Streaming: Pinball Machine Architecture #architecture #workflow

**Principle:** Streaming is great for low-latency data motion (double-swipe detection, ETL) but weak for process automation: state is distributed across stream processors, behavior is emergent ("pinball machine", Neal Ford's term), changes require coordinated multi-processor deploys, and acyclic-only tools can't loop.

**Do:**
- Use streaming where it fits — ETL, derived insights, real-time anomaly detection.
- Reach for a workflow engine once your "stream pipeline" is secretly implementing a business process with order, loops, or compensation.

**Don't:**
- Don't expect visibility into "where is order #42 right now?" from a stream topology — there is no single component that knows.

*Ref: Practical Process Automation.md — "Data Pipelines and Streaming"*

---

### 34b. Stateful Functions: Watch the Limitations #workflow #architecture

**Principle:** Stateful functions (Azure Durable Functions and similar) can persist state between executions but currently lack: a modeling language for long-running patterns, graphical representation, robust scheduling/versioning, and mature operations tooling.

**Do:**
- Re-check this category if you're considering it — innovation is happening quickly, especially in serverless.
- Pick a dedicated workflow engine for non-trivial long-running processes today.

*Ref: Practical Process Automation.md — "Stateful Functions"*

---

### 35. Judge Modeling Languages by the Workflow Patterns They Support #workflow

**Principle:** The Workflow Patterns initiative (workflowpatterns.com) defines control-flow, data, resource, and exception-handling patterns. BPMN implements most; Amazon States Language (AWS Step Functions) implements only some.

**Selected patterns mapped to BPMN:**

| # | Pattern | Description |
|---|---|---|
| 1 | Sequence | A task is enabled after the completion of a preceding task. |
| 2 | Parallel Split | A branch diverges into concurrent branches. |
| 3 | Synchronization | Convergence where control passes only when all input branches are enabled. |
| 4 | Exclusive Choice | One outgoing branch selected based on data. |
| 5 | Simple Merge | Convergence where each incoming enablement passes control onward. |
| 14 | Multiple Instances with a Priori Run-Time Knowledge | Multiple task instances created at runtime, count known before creation, run concurrently, synchronized at completion. |

**Do:**
- Use the Workflow Patterns list to evaluate any candidate modeling language.
- Expect that "simpler" custom languages eventually re-grow BPMN's complexity.

*Ref: Practical Process Automation.md — "Workflow Patterns"*

---

### 36. Graphical vs Textual Modeling — Pick Graphical (BPMN) #workflow

**Principle:** Visual models use the brain's "GPU" for pattern recognition; text uses the CPU. For process logic, visual wins for communication across roles.

**Code (Netflix Conductor JSON workflow — textual, hard to read):**
```
 "name": "sample-workflow",
 "version": 1,
 "tasks": [
 {
 "name": "task_1",
 "type": "SIMPLE"
 },
 {
 "name": "someDecision",
 "type": "DECISION",
 "decisionCases": {
 "0": [
 {
 "name": "task_2",
 "type": "SIMPLE"
 }
 ],
 "1": [
 {
 "name": "fork_join",
 "type": "FORK_JOIN",
 "forkTasks": [
 [
 {
 "name": "task_3",
 "type": "SIMPLE"
 }
 ],
 [
 {
 "name": "task_4",
 "type": "SIMPLE"
 }
 ]
 ]
 }
```

**Code (Spring State Machine textual model — also hard for parallel/loops):**
```
public void configure() {
 states.withStates()
 .initial(States.START)
 .state(States.RETRIEVE_PAYMENT, new RetrievePaymentAction())
 .state(States.WAIT_FOR_PAYMENT_RETRY)
 .end(States.DONE);
 transitions.withExternal()
 .source(States.START)
 .target(States.RETRIEVE_PAYMENT)
 .event(Events.STARTED)
 .and()
 .withExternal()
 .source(States.RETRIEVE_PAYMENT)
 .target(States.DONE)
 .event(Events.PAYMENT_RECEIVED)
 .and()
 .withExternal()
 .source(States.RETRIEVE_PAYMENT)
 .target(States.WAIT_FOR_PAYMENT_RETRY)
 .event(Events.PAYMENT_UNAVAILABLE)
 .and()
 .withExternal()
 .source(States.WAIT_FOR_PAYMENT_RETRY)
 .target(States.RETRIEVE_PAYMENT)
 .timer(5000l);
```

**Do:**
- Acknowledge the real developer concerns: hidden magic in property panels, IDE feature loss, perceived threat to self-image.
- Counter by toggling between the graphical view and the XML; both are source code.

**Don't:**
- Don't let business stakeholders override developers' technical modeling decisions — executable models are owned by the dev team.

*Ref: Practical Process Automation.md — "Textual Process Modeling Approaches" / "Typical Concerns About Graphical Modeling"*

---

### 37. Blockchain Smart Contracts Are a Public Workflow Engine — Edge Case #architecture #workflow

**Principle:** Smart contracts automate only the *public*, multi-party part of a process. Private per-party processes still use regular workflow engines.

**Do:**
- Consider blockchain when mutually distrustful parties need an intermediary.
- Expect that workflow engines remain essential for each party's internal automation.

*Ref: Practical Process Automation.md — "Process Automation with Blockchain?"*

---

### 38. Decide "When to Use a Workflow Engine" by ROI, Not by Gospel #architecture #workflow

**Principle:** Use an engine when long-running capabilities + visibility exceed the investment. Lightweight/managed engines lower the investment bar, so the range of valid use cases keeps growing.

**Do:**
- Apply engines to end-to-end business processes (high value), distributed transactions, and even purely technical long-running scenarios (visibility less critical but still worth it).
- Reject use cases that are just "graphical programming" with no state/collaboration value.

*Ref: Practical Process Automation.md — "When to Use a Workflow Engine"*

---

### 39. Decentralized vs Shared Engines: Default to Decentralized in Microservices #architecture #systems

**Principle:** In microservices, default to one engine per service for autonomy and isolation. Sharing an engine is OK if ownership of process models stays with the teams.

**Do:**
- Decentralize to allow each team to pick its tool, version, and patch cycle.
- Accept shared engines when operations simplicity matters more than isolation (think: shared RDBMS with per-team schemas).

**Don't:**
- Don't conflate *physical deployment* with *ownership* — even a shared engine must let teams own their models.

*Ref: Practical Process Automation.md — "Decentralized Engines" / "Sharing Engines" / "Ownership of Process Models"*

---

### 40. Never Build Your Own Workflow Platform #architecture #workflow

**Principle:** Building a bespoke platform on top of a vendor engine consistently fails — it lags the underlying product, hides features, blocks upgrades, and can't be Googled.

**Do:**
- Provide reusable *libraries* (auth connectors, logging hooks, ESB adapters) treated like internal open source.
- Wait until you have several projects live before even considering a facade.

**Don't:**
- Don't assemble a SOA/integration stack "to avoid vendor lock-in" — the cost is far higher than the risk.

*Ref: Practical Process Automation.md — "In-House Workflow Platforms" / "Don't Build Your Own Platform"*

---

### 41. Performance & Scalability: Test With Realistic Load Early #systems #workflow

**Principle:** Measure *actions per second* (process starts, service tasks, events) rather than waiting instances. Peaks matter more than averages.

**Do:**
- Spin up a near-production load test early in cloud environments; don't wait for prod.
- Verify latency budget for fully automated processes (e.g., 10 tasks within N ms).
- Investigate whether the engine supports horizontal scaling if you need high throughput.

**Don't:**
- Don't assume engines are only for low-throughput human-task scenarios — modern engines handle payments, trades, telecom, retail peaks.

*Ref: Practical Process Automation.md — "Performance and Scalability"*

---

### 42. Developer Experience & CI/CD: Vet This Before Committing #workflow #systems

**Principle:** The engine must fit your dev workflow or it will sabotage productivity.

**Do:**
- Confirm: preferred UI technology allowed? Deploy via your CI/CD? Unit tests with JUnit-equivalent? Models stored in Git?
- Verify client libraries exist for your languages and frameworks.

**Don't:**
- Don't accept tools that force manual model deploys or separate model repositories.

*Ref: Practical Process Automation.md — "Developer Experience and Continuous Delivery"*

---

### 43. Workflow Engine Categories — Know What You're Evaluating #workflow #architecture

**Principle:** The "workflow engine" category is blurry. Map candidates to: developer-friendly workflow engines, managed orchestrators, homegrown open source, BPM suites, RPA tools, low-code platforms — plus non-engines (data pipeline tools, integration tools, distributed tracing, process mining).

**Do:**
- Evaluate vision/roadmap and extensibility over feature checklists.
- Run multi-vendor POCs in parallel.

**Don't:**
- Don't trust RFP spreadsheets — vendors optimize for box-ticking and the resulting features are often unusable.

*Ref: Practical Process Automation.md — "Evaluating Workflow Engines" / "Be Cautious with RFPs"*

---

### 44. RFP Evaluation Criteria Checklist #workflow #architecture

**Principle:** Use these dimensions when shortlisting tools.

**Checklist:**
- **Integration possibilities:** language choice, connectors vs code, extensible?
- **Deployment options:** managed cloud / Docker / Kubernetes / library / application server / DB dependency?
- **Tooling:** modeler, ops, tasklist, monitoring — all optional/unbundled?
- **Process modeling language:** BPMN? Which elements supported?
- **Scalability & resilience:** fault tolerance setup complexity?
- **License & support:** source access, SLAs, open source guarantees?

*Ref: Practical Process Automation.md — "Be Cautious with RFPs"*

---

### 45. Aim for Strong Cohesion and Low Coupling (Constantine's Law) #architecture

**Principle:** "A structure is stable if cohesion is high and coupling is low." Sam Newman: "the code that changes together, stays together."

**Do:**
- Minimize all forms of coupling: *implementation* (peeking at internals/DBs), *temporal* (sync availability dependency), *deployment* (release trains, monolithic deploys), *domain* (unavoidable but design boundaries to minimize it).

**Don't:**
- Don't try to eliminate domain coupling — it can only be reduced by changing business requirements.

*Ref: Practical Process Automation.md — "Strong Cohesion and Low Coupling"*

---

### 46. Use DDD Bounded Contexts to Set Process Boundaries #architecture #workflow

**Principle:** Each context (e.g., checkout, payment, inventory, shipment, order fulfillment) owns its own ubiquitous language; one or more services implement a context; no service spans contexts.

**Do:**
- Recognize that "order" or "customer" means different things in different contexts — that's expected.
- Use BPMN collaboration diagrams to validate boundaries during design (then throw them away).

*Ref: Practical Process Automation.md — "Domain-Driven Design, Bounded Contexts, and Services"*

---

### 47. Avoid Process Monoliths — One Model, One Owner #architecture #workflow

**Principle:** An end-to-end model that mixes contexts (order fulfillment + payment internals + procurement) has no single owner, violates ubiquitous language, and forces cross-team coordination on every change.

**Do:**
- Cut end-to-end processes into per-service models owned by exactly one team.
- Ask "who is blamed if this fails?" to find the right owner.

**Don't:**
- Don't put call activities crossing service boundaries.
- Don't share a model just because teams aren't ready to run separate engines — design boundaries independently of physical deployment.

*Ref: Practical Process Automation.md — "Respect Boundaries and Avoid Process Monoliths"*

---

### 48. Long-Running Behavior Defends Boundaries — Defeat the "Hot Potato" Anti-Pattern #architecture #api

**Principle:** Without long-running capabilities, a service cannot absorb problems and rethrows them to the client (the *hot potato* anti-pattern), leaking internal concepts upstream. A workflow engine lets your service keep the problem local and expose a clean API.

**Do:**
- Make your payment service long-running so it can wait days for the customer to fix an expired card, then return a single paid/failed result to the client.
- Use the workflow engine within the service to own that waiting state.

**Don't:**
- Don't let payment error concepts (e.g., "credit card service unavailable") leak into the order fulfillment service's API.

*Ref: Practical Process Automation.md — "Long-Running Behavior Helps You Defend Boundaries"*

---

### 49. Call Activities vs API Calls Across Boundaries #workflow #api #architecture

**Principle:** BPMN *call activities* invoke another process on the same engine — handy within a boundary. Across service boundaries, use a normal API (REST, messaging); the caller should not know a workflow engine is at play.

**Do:**
- Use call activities to extract reusable subprocesses within one service.
- Cross boundaries with API calls; consider adapter subprocesses (e.g., polling wrappers) packaged as libraries if the remote API is awkward.

**Don't:**
- Don't share a call activity across engines or services — that's coupling via the engine.

*Ref: Practical Process Automation.md — "Call Activities: Handy Shortcuts Only Within the Boundary" / "Crossing Boundaries Is an API Call"*

---

### 50. Microservices: "Smart Endpoints and Dumb Pipes" (Fowler) #architecture

**Principle:** Microservices favor smart endpoints and dumb pipes over ESBs with routing/choreography/transformations baked into the middleware.

**Do:**
- Disconnect "process automation" from "centralized tooling" in your brain — orchestration can live locally in each microservice.

*Ref: Practical Process Automation.md — "Decentralized Workflow Tooling"*

---

### 51. Event-Driven Systems: Events for Autonomy, but Watch for Event Chains #architecture #workflow

**Principle:** Events enable autonomy (notification service, inventory caching) but turn toxic when chained into an implicit business process.

**Do:**
- Use events when the emitter genuinely does not care who reacts (notification emails, stock-level replication).
- Accept eventual consistency and storage overhead as the cost of decoupling.

**Don't:**
- Don't fool yourself that events are "free" — they create emergent behavior that may tip into chaos.

*Ref: Practical Process Automation.md — "Event-Driven Systems"*

---

### 52. Event Chains Are Implicit Processes — A Trap #architecture #workflow

**Principle:** When a sequence of event subscriptions implements a logical flow (order placed → payment received → goods fetched → shipped), the flow is invisible, has no owner, and is hard to change.

**Do:**
- Recognize the symptoms: changes to the sequence require editing multiple services, deployment coordination, and distributed versioning headaches.
- Replace event chains with commands issued by an owning orchestration process.

**Don't:**
- Don't accept "we'll just chain events" as a long-term design for an SLA-bearing business process.

*Ref: Practical Process Automation.md — "Event Chains"*

---

### 53. Beware Distributed Monoliths From Event-Driven Dogma #architecture

**Principle:** Forcing everything through events can *increase* coupling — e.g., a central authorization service that has to understand every other context's events becomes a rebuild target whenever any context changes.

**Do:**
- Refactor to a stable command-based API for cases like authorization; let the owning service decide what to push.

*Ref: Practical Process Automation.md — "The Risk of Distributed Monoliths"*

---

### 54. Define Orchestration vs Choreography by Communication Direction #architecture #workflow

**Principle:** Ruecker's definitions:
- **Command-driven communication = orchestration**
- **Event-driven communication = choreography**

These apply per communication link, not per system. A great architecture mixes both.

*Ref: Practical Process Automation.md — "Contrasting Orchestration and Choreography" / "Terminology and Definitions"*

---

### 55. Events vs Commands: Semantics, Not Protocol #api #architecture

**Principle:** Events = facts ("I'm hungry"); commands = intent ("prepare my order"). Both can be sent sync or async, via REST or messaging.

**Do:**
- Use a tweet metaphor to explain events to non-tech stakeholders.
- Acknowledge that commands typically require a feedback loop (ack/response).

**Don't:**
- Don't confuse the *transport* (message) with the *payload* (event vs command). Kafka stores "records"; whether they carry events or commands is up to you.

*Ref: Practical Process Automation.md — "Introducing Commands" / "Messages, Events, and Commands"*

---

### 56. Avoid "Commands in Disguise" Anti-Pattern #api #architecture

**Principle:** If you find yourself naming an event "Customer Needs To Be Sent Notification About Their Order", that's a command pretending to be an event — rename it ("Send Notification") and treat it as a command.

*Ref: Practical Process Automation.md — "Messages, Events, and Commands"*

---

### 57. Choose Event vs Command by Direction of Dependency #architecture #api

**Principle:** With events, the *receiver* is domain-coupled to the sender. With commands, the *sender* is domain-coupled to the receiver. Pick which side you want coupled based on responsibilities.

**Do:**
- Use events when the receiver owns the responsibility (notification team owns sending emails).
- Use commands when the sender owns the responsibility and needs the action to happen (legally mandated welcome letter).

*Ref: Practical Process Automation.md — "The Direction of Dependency"*

---

### 58. Litmus Test: "Is It OK If This Is Ignored?" #api #architecture

**Principle:** If the emitter is OK with the message being ignored → event. If not → command.

**Example:** Order notifications can be ignored by order fulfillment team (annoying but not catastrophic) → event. Legally required welcome letters cannot → command, owned by onboarding team.

*Ref: Practical Process Automation.md — "Deciding Whether to Use Commands or Events"*

---

### 59. Mix Commands and Events in the Same Process #workflow #architecture

**Principle:** Real processes mix both. A customer-onboarding process may command credit/address/criminal checks (orchestration) and then emit a `customer-created` event that the loyalty program listens to (choreography).

**Do:**
- Walk every communication link in your collaboration diagram and consciously label it command or event.

*Ref: Practical Process Automation.md — "Mixing Commands and Events"*

---

### 60. Design Responsibilities First — Events/Commands Follow #architecture #api

**Principle:** Don't decide events vs commands in a vacuum. First decide which team is accountable for what; the communication style falls out of that.

**Do:**
- Ask "who does the CEO blame when X fails?" to find the owner; the owner commands, others subscribe.

**Don't:**
- Don't skip responsibility design — it leads to finger-pointing and frustration.

*Ref: Practical Process Automation.md — "Designing Responsibilities"*

---

### 61. Validate Decisions by Walking Through Change Scenarios #architecture #workflow

**Principle:** Compare orchestration vs choreography by tracing a realistic change (e.g., adding a criminal check to onboarding) and counting how many services must be touched and redeployed.

**Do:**
- Use this technique to debunk the myth "event-driven is always more decoupled". Often the same number of services change, but orchestration also gives you a single place to see the flow.

*Ref: Practical Process Automation.md — "Evaluating Change Scenarios to Validate Decisions"*

---

### 62. Myth: Commands Require Synchronous Communication #api #architecture

**Principle:** Commands can be sent asynchronously (e.g., a queue). Temporal coupling comes from *synchronous* communication, not from commands.

**Do:**
- Send commands via messages to remove temporal coupling.
- Combine async command with a feedback channel (subscription, callback, or polling).

**Don't:**
- Don't build orchestration as a chain of synchronous blocking calls — that erodes latency and availability.

*Ref: Practical Process Automation.md — "Commands Do Not Require Synchronous Communication"*

---

### 63. Myth: Orchestration Must Be Central #architecture

**Principle:** Orchestration simply means commanding another component. Every microservice can orchestrate locally; "local orchestration" or "distributed orchestration" are valid terms.

*Ref: Practical Process Automation.md — "Orchestration Does Not Need to Be Central"*

---

### 64. Myth: Choreography Is Always More Decoupled #architecture

**Principle:** Generalizing "events reduce coupling" is wrong. Events shift coupling to the receiver; in some scenarios that is worse.

*Ref: Practical Process Automation.md — "Choreography Does Not Automatically Lead to More Decoupling"*

---

### 65. Workflow Engines Belong in Event-Driven Systems Too #workflow #architecture

**Principle:** An engine can subscribe to events, start instances, wait for events within an instance, and issue commands — all in one model. This is the natural home for time-window logic and SLA enforcement.

**Do:**
- Use BPMN receive tasks / message boundary events to model event-driven behavior with explicit timeouts.

*Ref: Practical Process Automation.md — "The Role of Workflow Engines"*

---

### 66. Synchronous Request/Response: Don't Push Failures to the Client #api #workflow

**Principle:** When a downstream service fails, the question is *who* holds the retry state. Pushing it to the end user (e.g., "please try again in five minutes" on a boarding pass flow) is usually wrong.

**Do:**
- Have the responsible service own retry state via a workflow engine; return HTTP 202 (Accepted) when async is needed.
- Keep failures local — encapsulation yields a cleaner API.

*Ref: Practical Process Automation.md — "Synchronous Request/Response"*

---

### 67. Asynchronous Request/Response: Model It Explicitly in BPMN #workflow #api

**Principle:** Use a send task + receive task (or a combined service task) to model async communication with timeouts. The engine handles correlation.

**Do:**
- Model timeouts explicitly — engines can wait milliseconds or days.

*Ref: Practical Process Automation.md — "Asynchronous Request/Response"*

---

### 68. Correlation: Use Artificial IDs, Not Engine or Business IDs #api #workflow

**Principle:** For matching responses to waiting instances, the book recommends three rules:

**Do:**
- Generate a fresh UUID per communication; store it in process variables.
- Be cautious with engine process instance IDs — they may change on restart or vendor changes.
- Be cautious with business IDs (e.g., order ID) — they can collide (split payments).

*Ref: Practical Process Automation.md — "Asynchronous Request/Response"*

---

### 69. BPMN "Ready to Receive" Gotcha — Use Message Buffering #workflow #api

**Principle:** Per the BPMN standard, an incoming message can only correlate when a token is *already waiting* in the matching receive task. Race conditions cause messages to be dumped.

**Do:**
- Pick a vendor that supports proprietary *message buffering* with TTL — it removes this whole class of bugs.
- If unavailable, work around with retries or `Thread.sleep` while correlating (unsatisfying but functional).

*Ref: Practical Process Automation.md — "BPMN and Being Ready to Receive"*

---

### 70. Aggregator Pattern — Stateful Collection of Related Messages #workflow #api

**Principle:** The Enterprise Integration Patterns *aggregator* collects related messages until a complete set arrives, then publishes one distilled message. BPMN implements this naturally as a process with multiple receive events and a timeout.

**Do:**
- Leverage the engine's persistent state and timeout handling to implement aggregators.

*Ref: Practical Process Automation.md — "Aggregating Messages"*

---

### 71. Poisoned Messages & DLQs — Workflow Engines Provide Context #workflow #systems

**Principle:** Poisoned messages that exhaust retries land in a dead-letter queue with no context. A failed process instance, by contrast, exposes its history, path, and attached data.

**Do:**
- Prefer process instances over raw message flows for any non-trivial handling.
- Build "message hospitals" if you must use DLQs.

*Ref: Practical Process Automation.md — "Poisoned and Dead Messages"*

---

### 72. Synchronous Facade Over Asynchronous Engine #api #workflow

**Principle:** Sometimes frontends demand synchronous APIs. Build a facade that sends the request, waits for the async response with a timeout, and falls back to async on timeout.

**Code (facade pseudocode):**
```
try {
 sendRequestToServiceB(correlationId, ...)
 response = waitForResponseFromServiceB(correlationId, timeout)
 // ...
}
catch (timeoutError) {
 // ?
}
```

**Do:**
- Return synchronously when all is well (HTTP 200); fall back to async (HTTP 202) on glitches and follow up via email/push.

**Don't:**
- Don't block forever — pick a timeout and design the fallback UX.

*Ref: Practical Process Automation.md — "Synchronous Facades Hiding Asynchronous Communication"*

---

### 73. ACID Only Within One Boundary — Plan for Eventual Consistency #architecture #systems

**Principle:** Monoliths get ACID for free across tables. Distributed systems cannot — two-phase commit (XA) is expensive and brittle. You must design for *eventual consistency* on the business level.

**Do:**
- Make intermediary states non-harmful (or understand the consequences if they leak).
- Plan a strategy: ignore, apologize, or resolve.

**Don't:**
- Don't pretend a remote call participates in your DB transaction.

*Ref: Practical Process Automation.md — "Transactions and Consistency" / "Eventual Consistency"*

---

### 74. Three Business Strategies for Inconsistency #architecture #workflow

**Principle:** Picking a strategy is a *business decision*, not a technical one.

- **Ignore:** Accept dead CRM entries; cheap, but causes reporting noise.
- **Apologize:** Wait for customers to complain; compensate with vouchers (think airline overbooking).
- **Resolve:** Tackle head-on via reconciliation jobs, Sagas, or the outbox pattern.

**Do:**
- Bring business stakeholders into this decision; use BPMN visualizations to show failure scenarios.

*Ref: Practical Process Automation.md — "Business Strategies to Handle Inconsistency"*

---

### 75. Saga Pattern: When You Can't Roll Back, Compensate #workflow #architecture #systems

**Principle:** Sagas undo tasks instead of rolling them back. BPMN supports this natively via *compensation events* linking each task to its undo task.

**Do:**
- Define compensation per task (e.g., a shipped SIM card can only be deactivated, not un-shipped).
- Expect compensation to make the model more complex — that mirrors real business complexity.
- Leverage the engine to guarantee all required compensations execute on failure.

*Ref: Practical Process Automation.md — "The Saga Pattern and Compensation"*

---

### 76. Outbox Pattern: At-Least-Once Event Publishing #architecture #api #systems

**Principle:** To atomically commit DB writes *and* publish an event, write the event to an *outbox* table in the same transaction, then a scheduler publishes and deletes it. This gives at-least-once semantics.

**Do:**
- Replace the outbox table+scheduler with a workflow engine: express "do logic" and "publish event" as two consecutive tasks; the engine retries the second on failure.
- Use this to elevate consistency from "best effort" to "at least once".

*Ref: Practical Process Automation.md — "Chaining Resources by Using the Outbox Pattern"*

---

### 77. Eventual Consistency Starts at the First Remote Call #api #systems

**Principle:** Even a single REST call can leave you in an unknown state — a network exception might mean the request never arrived *or* the response was lost. The server may have already charged the card.

**Do:**
- Decide on a strategy: query first, use a cleanup API, or cancel-and-ignore errors. Don't ignore the ambiguity.

*Ref: Practical Process Automation.md — "Eventual Consistency Applies to Every Form of Remote Communication"*

---

### 78. Idempotency Is Mandatory for Every Remote Operation #api #systems

**Principle:** Retries are unavoidable in distributed systems; therefore every remote operation must be safe to repeat.

**Do:**
- Lean on naturally idempotent operations (queries, deletions).
- For non-idempotent operations (charging a card), generate a unique client-side ID per logical operation and have the server dedupe.
- Require idempotency at the API design stage — clients cannot retrofit it.

**Don't:**
- Don't dedupe based on business payload (amount + card) — two real customers can charge identical amounts in the same millisecond.

*Ref: Practical Process Automation.md — "The Importance of Idempotency"*

---

### 78a. Workflow Engine APIs Are Idempotent by Design — Lean on That #workflow #api

**Principle:** Good engines offer idempotent operations on top of inherent idempotency in the model. Use them.

**Do:**
- Use the engine's "create process instance by key" so the same business key starts only one instance.
- Rely on task completion being naturally idempotent — once a task is completed, repeating the call is a no-op.
- Even loops arriving at the same task again get a new task instance ID, so completion is unambiguous.

*Ref: Practical Process Automation.md — "The Importance of Idempotency"*

---

### 79. BizDevOps: One Joined Model for All Three Roles #workflow #architecture

**Principle:** A single executable BPMN model serves business (requirements, living docs), development (test visualization, navigation), and operations (incidents in context, fix capability).

**Do:**
- Treat the model as a communication hub across the PDCA life cycle (analyze → design → implement → operate).
- Expect an early spike in analysis effort — it surfaces problems cheaply.

*Ref: Practical Process Automation.md — "Including All the People: BizDevOps" / "The Process Automation Life Cycle"*

---

### 80. One Joined Operational Model — Not Two (Business + Technical) #workflow #architecture

**Principle:** Avoid a "business model" thrown over the fence to IT for a separate "technical model". Have *one* comprehensive operational model (the "house" not the "pyramid"), containing both human and technical flows.

**Do:**
- Use BPMN *collaboration diagrams* (multiple pools) to show human flow + executable flow + system flow together during design.
- Discard collaboration diagrams after they've served their purpose — they don't need long-term accuracy.

**Don't:**
- Don't maintain a separate "business" model and "executable" model with translation steps between them.

*Ref: Practical Process Automation.md — "The Power of One Joined Model" / "From a Process Pyramid to a House"*

---

### 81. Who Models? Analysts Draft, Developers Execute, Both Own #workflow

**Principle:** Analysts create the first drafts (the "what/why"); developers make them executable and must be empowered to adjust; the executable artifact is owned by developers.

**Do:**
- Hold joint workshops with analysts + developers (+ SMEs, ops) for first drafts.
- Sync physical model copies regularly; "discipline is more important than tool features".

**Don't:**
- Don't let business analysts overwrite technical attributes they can't see — that's why dev owns the executable file.

*Ref: Practical Process Automation.md — "Who Does the Modeling?"*

---

### 82. Extract (Integration) Logic Into Subprocesses Within a Boundary #workflow

**Principle:** If a step in your main process hides a lot of integration complexity (clumsy API, async wait, retries), extract it into a separate BPMN process invoked via a call activity — *within* the same service boundary.

**Do:**
- Use subprocesses to keep the main model at one level of granularity.
- Avoid subprocesses by default; introduce them when granularity clearly differs.

**Don't:**
- Don't share subprocesses across service boundaries — extract a proper service with API instead.

*Ref: Practical Process Automation.md — "Extracting (Integration) Logic into Subprocesses"*

---

### 83. Results vs Exceptions vs Errors — Pick the Right Construct #workflow

**Principle:** Model expected results (e.g., "customer not scorable") as gateways; model exceptions that hinder reaching the expected result (e.g., service threw) as error events; treat technical problems (temporarily unavailable) as configuration-driven retries/incidents, not visible flow.

**Do:**
- Talk about *business reactions* (modeled) vs *technical reactions* (configured) rather than "business error" vs "technical error".
- Escalate from technical to business reactions when SLAs are at risk.

*Ref: Practical Process Automation.md — "Distinguishing Between Results, Exceptions, and Errors"*

---

### 84. Readability: Label Elements and Emphasize the Happy Path #workflow

**Principle:** Naming conventions + layout make models readable.

**Do:**
- Label start events in passive voice ("Order placed"), tasks as verb + object ("Retrieve payment"), gateways as a question with answers on outgoing flows, end events as the business outcome ("Order delivered").
- Model left-to-right (cultural direction), place elements by typical time, and put the happy path on a straight line in the center.

**Don't:**
- Don't model top-to-bottom — humans read wide screens better.

*Ref: Practical Process Automation.md — "Increasing Readability"*

---

### 84a. Don't Over-Engineer Models: "Perfection Is the Enemy of Progress" #workflow

**Principle:** Models are long-lived artifacts read by many roles — invest in quality, but accept that "an imperfect model in production beats a perfect model that never ships" (Churchill).

**Do:**
- Aim for the model "with the fewest unhappy people" (colleague quote).
- Iterate: improve models in the next sprint based on real feedback.

**Don't:**
- Don't block delivery to perfect the diagram.

*Ref: Practical Process Automation.md — "Creating Better Process Models"*

---

### 84b. Discover Boundaries With Event Storming / Storystorming / Domain Storytelling #architecture #workflow

**Principle:** If BPMN collaboration diagrams are rejected as too heavy, use lighter discovery techniques (Event Storming, Storystorming, Domain Storytelling) — but still convert what you learn into a BPMN collaboration model for analytical verification.

**Do:**
- Use collaboration diagrams to validate boundary and exception-handling designs before implementation.
- Throw them away after — they're typically incomplete and not worth keeping perfectly up to date.

*Ref: Practical Process Automation.md — "Foster Your Understanding of Responsibilities"*

---

### 85. Process Visibility Has Two Dimensions: Improvement + Operation #workflow #systems

**Principle:** Visibility serves *process improvement* (cheaper, faster, scalable) and *process operation* (SLA monitoring, incident detection). Both need situation awareness.

**Do:**
- Plan reporting and dashboards for both audiences from day one.

*Ref: Practical Process Automation.md — "The Value of Process Visibility"*

---

### 86. Leverage Audit Data From the Engine — Don't Build Your Own #workflow #systems

**Principle:** Engines emit audit data for free. Access it via vendor monitoring tools, the engine API, an event stream of history events, or (last resort) direct DB reads.

**Do:**
- Prefer the API or vendor tool.
- If reading the engine DB directly, treat the schema as an implementation detail — no backward-compatibility guarantees.

*Ref: Practical Process Automation.md — "Leverage Audit Data from Your Workflow Engine"*

---

### 87. Model Milestones and Phases to Measure KPIs #workflow

**Principle:** Add intermediate events as *milestones* (status: passed / not passed) or use embedded subprocesses as *phases* (status: active / passed / not passed) to give reporting natural measuring points.

**Do:**
- Use milestones to build customer-facing status checklists ("Where is my order?").
- Build simplified status-only BPMN diagrams for customers; don't expose the full executable model.

*Ref: Practical Process Automation.md — "Model Events to Measure Key Performance Indicators" / "Status Inquiries"*

---

### 88. End-to-End Visibility Across Systems — Pick Your Approach #workflow #systems

**Principle:** End-to-end processes span multiple engines and legacy systems. Five approaches exist, with trade-offs:

| Approach | Strength | Weakness |
|---|---|---|
| Distributed tracing (Jaeger, Zipkin) | Mature, easy start | Too low-level for non-engineers; sampling hides 90%+ |
| Custom centralized monitoring | Right granularity, business events | Effort to build; ownership questions |
| DWH / data lakes / BI | Reuses existing tools | Loses process context; ETL-heavy |
| Process mining (Celonis, Prom) | Discovers legacy flows | Offline analysis; weak at live monitoring |
| Process event monitoring | Live, prebuilt | Emerging category |

**Do:**
- Build custom monitoring on business/domain events with a unique trace ID per end-to-end instance; link back to per-engine ops tools for deep dives.

*Ref: Practical Process Automation.md — "Understanding Processes That Span Multiple Systems"*

---

### 89. Typical Process Metrics: Duration + Count #workflow #systems

**Principle:** Track a small set of high-value metrics and slice them by process context.

**Metrics:**
- *Duration:* cycle time, phase duration, single-task duration (vs SLA).
- *Count:* started/ended instances, path frequency, end-state distribution.

**Do:**
- Provide (near-) real-time dashboards with process context, alerting on threshold breaches.
- Allow deep drill-down: distinguish automated vs manual paths, analyze outliers by attached data.

*Ref: Practical Process Automation.md — "Typical Metrics and Reports" / "Allowing for a Deeper Understanding"*

---

### 89a. Eventual Consistency in Customer-Facing Dashboards #workflow #systems

**Principle:** Real-time process dashboards are powerful but must acknowledge that data may be slightly delayed, sampled, or partial. Communicate this in the UI.

**Do:**
- Distinguish "running / completed / canceled" states in reports — averaging only completed instances hides stuck ones.
- Slice by attached business data (e.g., driver age + car type) to find otherwise-invisible outliers.
- Provide self-service report builders for business stakeholders to do their own exploration.

*Ref: Practical Process Automation.md — "Allowing for a Deeper Understanding"*

---

### 90. Adoption Journey Pattern: POC → Pilot → Lighthouse → Scale #workflow #architecture

**Principle:** Successful adoption follows a pattern: throwaway POC (days) → pilot (real but small, goes live) → lighthouse (broader, showcased) → scale (only after 5–6 successes).

**Do:**
- Plan to throw the POC away — its purpose is learning, not production code.
- Go live with the pilot — only production teaches the full life cycle.
- Make the lighthouse visible: "show and tell", shared source, live demos over slideware.

**Don't:**
- Don't scale before you have a handful of projects; you'll repeat mistakes in parallel.

*Ref: Practical Process Automation.md — "The Pattern of Successful Adoption Journeys"*

---

### 91. Avoid the "DontDoItAtHome" Adoption Failures #architecture #workflow

**Principle:** Big-bang strategic programs with bespoke platforms and upfront process landscapes consistently fail to deliver value.

**Don't:**
- Don't start with a program — start with a project.
- Don't mandate top-down — let bottom-up lighthouse projects emerge.
- Don't build a custom platform; don't start too many projects at once.
- Don't begin with process landscape architecture — derive it after you have working projects.
- Don't pick "the most crucial core process" as the pilot — too risky.

*Ref: Practical Process Automation.md — "Failures You Want to Avoid"*

---

### 92. A Successful Adoption Story Looks Like This #workflow #architecture

**Principle:** The real insurance-company success story followed this arc:
1. Form a team around one painful process (car insurance claims).
2. Evaluate, model, implement, deploy, operate — narrow scope.
3. Be pragmatic (cut off too-detailed DWH discussions).
4. Reorganize the team into a department that helps other teams.
5. Evolve into an internal consulting COE.
6. Provide reusable libraries (AD integration, ESB connectors) — never forced.
7. Move from central engine to managed per-team engines.
8. After five years: ~100 process solutions in production, management happy.

*Ref: Practical Process Automation.md — "A Success Story"*

---

### 93. Adjust the Journey to Your Starting Point #workflow #architecture

**Principle:** Replacing an existing tool, introducing into SOA, introducing into event-driven architecture, or riding a strategic program — each requires a different emphasis.

**Do:**
- In event-driven overgrowth: start with a *tracking* process that only records events; add orchestration incrementally.
- In SOA: avoid re-centralizing; be cautious about preconceptions from old BPM suites.
- In strategic programs: keep pilots small and "fly under the radar" if needed.

*Ref: Practical Process Automation.md — "Different Journeys for Different Scenarios"*

---

### 94. POC Practices: 3–5 Days, Throwaway, Co-Developed #workflow

**Principle:** A POC is a few days of focused prototyping whose code is discarded. Define concrete goals, include a moderator, co-develop with a consultant.

**Do:**
- Decide up front: prove technology or showcase UI? You usually can't do both in a week.
- Define a spokesperson; rehearse the demo; prepare a focused storyline.
- Run an MVP only after a POC.

**Don't:**
- Don't expect a spontaneous demo to "speak for itself".

*Ref: Practical Process Automation.md — "Proofs of Concepts"*

---

### 94a. Bottom-Up Adoption Beats Top-Down (Usually) #architecture

**Principle:** Grass-roots adoption — developers try a tool, push it into production, get noticed, become a lighthouse — is the most reliable motion. Top-down mandates (typical of SOA) tend to fail because developers either don't use the tool or fail to use it successfully.

**Do:**
- Define company-wide *recommendations* but leave projects room to decide.
- Accept that procurement may happen *after* the tool is already settled — that's OK.

**Don't:**
- Don't impose a single company-wide stack — even if it works short-term, it breeds resentment.

*Ref: Practical Process Automation.md — "Bottom-up Versus Top-down Adoption"*

---

### 94b. Tracking Process as the First Step Out of Event-Driven Chaos #workflow #architecture

**Principle:** If you're already in an over-grown event-driven architecture, introduce a BPMN model that *only* tracks events (no commands). It records flow, enables monitoring/SLA detection, and gives you a foothold to incrementally add orchestration.

**Example:** an order-tracking process that waits for milestones, escalates after 14 days (inform customer), and gives up after 21 days (cancel order):

```
[Order placed] --> (wait for "Order shipped")
                      |        |
                  +14d |        | +21d
                      v        v
            "Inform customer   "Cancel
             of delay"          order"
```

**Do:**
- Use the tracking process to gain visibility without disturbing existing services.
- Migrate event-chain links to commands one at a time, removing choreography piecemeal.

*Ref: Practical Process Automation.md — "Introducing process automation in event-driven architectures"*

---

### 95. Present the Business Case With Numbers #workflow

**Principle:** Quantitative wins (e.g., $100k invest → $1M/year savings; €3M/year licensing saved) or qualitative wins ("we'd have been in chaos without it") both move decision makers.

**Value propositions table (excerpted):**

| Value Proposition | Type | Example |
|---|---|---|
| Reducing dev effort around state handling | Quantitative, hard to measure | ~10 person-years bespoke state handling replaced by ~$100k engine + training |
| Automating manual tasks | Quantitative, easy to measure | Onboarding saves 4 h/day + 1 FTE ≈ $100k/yr |
| Building the right thing | Qualitative | Early visual review catches a flaw costing days of rework |
| Avoiding stuck instances | Qualitative | Operations auto-notified; customers never notice delays |
| Saving effort via prebuilt components | Quantitative, easy | Vendor tasklist UI ≈ saves a full dev team ($500k/yr) |
| Scaling processes | Qualitative | Survive viral load without manual collapse |

*Ref: Practical Process Automation.md — "Presenting the Business Case"*

---

### 96. Reuse: Internal Open Source Libraries, Not a Mandatory Platform #architecture #workflow

**Principle:** Treat reusable components (messaging adapters, auth hooks, ESB glue) as internal open source — offered, not mandated. Teams can fork or extend via pull requests.

**Do:**
- Allow libraries to evolve inside real projects first.
- Provide help and resources; let adoption be organic.

**Don't:**
- Don't extract "reusable process fragments" across teams — extract a proper service instead.

*Ref: Practical Process Automation.md — "Dos and Don'ts Around Reuse"*

---

### 97. Center of Excellence: Internal Consulting, Not Governance Tyranny #architecture #workflow

**Principle:** As you scale, a COE provides best practices, getting-started guides, project templates, training, and community — but does not dictate tool choice.

**Do:**
- Build a self-service portal (one big bank did this over two years).
- Run internal forums / Slack / community events.
- Couple freedom of choice with "you build it, you run it" accountability.

*Ref: Practical Process Automation.md — "Establishing a Center of Excellence" / "Managing Architecture Decisions"*

---

### 98. Choose Boring Technology — With Guardrails, Not Dictates #architecture

**Principle:** Combine freedom of choice with operational accountability ("you build it, you run it"). Dan McKinley's "choose boring technology" rule tends to win when teams own production.

**Do:**
- Maintain an architecture board with a list of *approved* tools; teams wanting something new pitch it (fast decision or proceed-with-awareness).
- Use stricter gatekeeping for bridge technologies (e.g., RPA): require teams to present a payback plan.

*Ref: Practical Process Automation.md — "Managing Architecture Decisions"*

---

### 99. Decentralized Tooling at Scale: Harvest Data via APIs #systems #workflow

**Principle:** With per-team engines, questions arise: what's running? Are patches applied? Are we within license limits? Answer by harvesting data via tool APIs — or use managed services with built-in control planes.

*Ref: Practical Process Automation.md — "Decentralized Workflow Tooling"*

---

### 100. Skill Development per Persona #workflow

**Principle:** Match training to persona; the more developer-friendly the tool, the less proprietary training is needed.

- **Rockstar developers:** give them the engine and get out of the way; risk: overengineering, distraction.
- **Professional developers:** vendor training + ongoing consulting; make good COE coaches.
- **Low-code developers:** constrained environment, customized training.
- **Citizen developers:** out of scope for this book.
- **Business analysts:** learn BPMN; can use discovery techniques (Event Storming, Storystorming, Domain Storytelling).
- **Operations:** dedicated vendor training on deploy/troubleshoot.
- **Enterprise architects:** understand role + specifics of chosen tool.
- **Process methodology experts:** COE members who simplify models.

**Do:**
- Schedule training immediately before project start; follow with on-the-job coaching.

*Ref: Practical Process Automation.md — "Roles and Skill Development"*

---

### 101. Rethink Synchronous UX — Async UX Is Usually Better #api #workflow

**Principle:** Business folks often demand synchronous UX ("customers need their PDF ticket now!"). Challenge it: a async experience with status updates, deep links, and notifications is more resilient and usually preferred by customers (Amazon does this).

**Do:**
- Ask "what would Amazon do?" to push back on forced synchronous UX.
- Embrace eventual consistency in the UX — receive a boarding pass by email later rather than failing the whole flow now.

*Ref: Practical Process Automation.md — "Rethinking Business Processes and the User Experience"*

---

### 101a. Current Architecture Trends Increase the Need for Workflow Engines #architecture #workflow

**Principle:** Fine-grained distributed components, reactive event-driven systems, remote communication consistency challenges, continuous delivery, cloud shift, polyglot stacks, and more automation overall — every modern architecture trend *increases* the applicability of workflow engines.

**Do:**
- Expect engine adoption to keep growing; pick tools that are lightweight and flexible enough for modern stacks.

*Ref: Practical Process Automation.md — "Current Architecture Trends Influence Process Automation"*

---

### 101b. Combine Actors With Workflow Engines for the Best of Both #architecture #workflow

**Principle:** The actor model has nice properties (single-owner messaging, persistent actors) but lacks a long-running modeling language. A powerful combination: build an actor that implements a process but delegates the long-running details to a workflow engine.

**Do:**
- Use the workflow engine for state, scheduling, and visibility; use the actor system for concurrency and messaging.
- Acknowledge the actor model's limited industry adoption before committing to it.

*Ref: Practical Process Automation.md — "The Actor Model"*

---

## Anti-Patterns & Common Mistakes

- **Wild West integration:** ad hoc DB triggers, point-to-point REST, brittle CSV-over-FTP → *fix:* introduce a workflow engine for state + scheduling.
- **Homegrown workflow engine:** bespoke `status` columns + hand-rolled schedulers → *fix:* use an existing engine.
- **Hot potato:** services rethrow internal errors to clients → *fix:* make services long-running; expose clean paid/failed APIs.
- **Process monolith:** one BPMN model mixing contexts → *fix:* cut into per-service models with single owners.
- **Event chains:** implicit business processes via chained event subscriptions → *fix:* introduce an orchestrating service that issues commands.
- **Distributed monolith:** central service forced to understand every other context's events → *fix:* command-based stable API.
- **Commands in disguise:** events named "Customer Needs To Be Notified" → *fix:* rename as commands.
- **Building your own platform:** custom facade on a vendor engine → *fix:* ship libraries as internal open source.
- **RPA as process platform:** using RPA tooling for end-to-end business flows → *fix:* keep RPA bots as single service tasks inside BPMN.
- **Top-down big-bang adoption:** strategic program with bespoke platform before any project → *fix:* start with a throwaway POC + pilot.
- **Ignoring eventual consistency:** assuming one remote call is atomic → *fix:* design compensation or apologize strategy.
- **Non-idempotent APIs:** relying on payload comparison for dedupe → *fix:* generate unique client IDs for each logical operation.
- **Two-model split:** business model + technical model with translation → *fix:* one joined operational model.

---

## Decision Heuristics / Checklists

**When to use a workflow engine (yes if any):**
- Process is long-running (minutes → months).
- You need visibility for business / ops / dev collaboration.
- You cross service, transaction, or organizational boundaries.
- You need durable retries, timers, or compensation.
- You need audit data for compliance or KPIs.

**When NOT to use one:**
- Pure graphical programming without state or collaboration value.
- One-off, high-variance process.
- Synchronous CRUD with no orchestration.

**Model vs code (promote to model if any):**
- You need to wait (state must persist).
- The logic is regularly discussed with other stakeholders.
- The logic crosses a boundary (transactional, service, org).

**Command vs event (per communication link):**
- Emitter owns the outcome / must guarantee action → **command**.
- Emitter doesn't care who reacts → **event**.
- Litmus test: "Is it OK if this is ignored?" Yes → event; No → command.

**Inconsistency strategy (business decision):**
- Low impact, rare → **ignore** (maybe with periodic reconciliation).
- High impact, rare, compensable → **apologize** (voucher, manual fix).
- High impact, frequent, or regulated → **resolve** (Saga, outbox, reconciliation).

**Idempotency design:**
- Natural (queries, deletes) → no work needed.
- Mutations → require client-generated unique operation ID; server keeps a dedupe store.

**Engine deployment:**
- Microservices, polyglot, autonomy-first → **decentralized** (one engine per service).
- Operations simplicity priority → **shared** engine with per-team ownership of models.
- Modular monolith → **embedded** library.

**Adoption step you're ready for:**
- No engine yet, want to validate → **POC** (throwaway).
- POC convinced you → **pilot** (goes live).
- Pilot succeeded, want to showcase → **lighthouse**.
- 5–6 projects live → **scale** with COE + libraries.

---

## Key Takeaways

1. **Don't hardcode state machines.** A workflow engine gives you durable state, scheduling, and versioning for free — and visibility on top.
2. **BPMN is the lingua franca.** Use it; it's the only mature, standardized, executable process language with broad tooling.
3. **Models are source code.** Store them in Git, deploy them with the app, test them with JUnit-equivalent frameworks.
4. **Respect boundaries.** One process model = one owner. Cut end-to-end flows at service boundaries; cross boundaries with APIs, not call activities.
5. **Orchestration is not central.** Each microservice can — and should — orchestrate locally. Disconnect "orchestration" from "central BPM platform" in your brain.
6. **Balance orchestration and choreography per link.** Commands when the sender owns the outcome; events when the receiver does. The litmus test is "OK to ignore?".
7. **Plan for eventual consistency from the first remote call.** Pick a business strategy (ignore / apologize / resolve); use Sagas and the outbox pattern to resolve.
8. **Idempotency is not optional.** Design every remote API to be safe to retry.
9. **Never build your own platform.** Provide libraries as internal open source instead.
10. **Adopt iteratively: POC → pilot → lighthouse → scale.** Throw the POC away; go live with the pilot; scale only after 5–6 successes.

---

## Cross-References
- Related: [[../Build_an_Orchestrator_in_Go.md]] — control-plane/data-plane architecture, state machines
- Related: [[../Building_Event-driven_Microservices.md]] — choreography, events, brokers
- Related: [[../Flow_Architectures.md]] — event-driven and streaming architectures
- Related: [[../Building_Microservices.md]] — service boundaries, autonomy, coupling
- Related: [[../Software_Architect_Elevator.md]] — BizDevOps, architecture boards
- Topic index: [[../INDEX.md]]
