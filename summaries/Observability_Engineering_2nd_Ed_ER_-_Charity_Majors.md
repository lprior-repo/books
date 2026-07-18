# Observability Engineering, 2nd Edition: Comprehensive Summary

**Authors:** Charity Majors, Liz Fong-Jones, and George Miranda
**Subtitle:** Achieving Production Excellence
**Publisher:** O'Reilly Media, 2025

---

## Overview

This second edition of *Observability Engineering* significantly expands on the foundational concepts of the first edition. It deepens the theoretical framework by defining observability as a property of software dependability, introduces performance engineering as a discipline tightly coupled with observability, and adds an entirely new chapter on AI observability for LLM-powered applications. The book argues that the transition from fragmented "three pillars" (logs, metrics, traces) to unified telemetry represents a paradigm shift enabling a higher degree of observability in modern distributed systems.

---

## Chapter 1: What Is Observability?

### Mathematical Origins

The term "observability" was coined by Rudolf E. Kalman in 1960 in the context of control systems theory. In that context, observability measures how well internal states of a system can be inferred from external outputs. The authors adapt this concept to software systems, noting that while the mathematical definition provides grounding, software observability requires additional considerations.

### Observability as a Property of Software Dependability

The first edition classified observability primarily as a new breed of tooling. The second edition takes a broader view: observability is a **property of your software systems**, similar to performance or availability. It is a dimension of software dependability.

The authors build on J.C. Laprie's 1994 framework for software dependability, which defined properties as: availability, reliability, safety, security, integrity, and maintainability. The authors argue that **observability must be added** to this list:

> Observability: ability to understand or debug any given system state.

Laprie also defined techniques for building dependable systems: fault prevention, fault tolerance, fault removal, and fault forecasting. Observability encompasses techniques from all four categories.

### Why Traditional Monitoring Falls Short

In the era of monolithic systems, monitoring was relatively straightforward: services were either up or down. Monitoring tools measured aggregate system state and alerted on known failure modes. In the modern distributed-by-default era, failures are far more complex:

- Partial degradation rather than binary up/down states
- Failures caused by configuration defaults (e.g., data retrieval from wrong regions)
- Partially degraded load balancers affecting a small fraction of requests
- Multiple application versions running simultaneously during progressive delivery
- Dependencies on external infrastructure controlled by other companies

Traditional monitoring tells you *that* something is wrong and maybe *where*, but cannot tell you *why*. Observability enables understanding any system state, including novel ones never before encountered.

### How Observable Is Your Software?

The authors provide a comprehensive litmus test. A system with high observability allows you to:

- Understand any system state, even novel ones you have never seen before
- Answer open-ended questions about inner workings without hitting investigative dead ends
- Understand what any particular user is experiencing at any given time
- See any cross-section of system performance from aggregate views down to individual requests
- Compare arbitrary groups of requests to identify common attributes of unexpected behavior
- Find the Nth most load-generating user, not just the top one
- Isolate a specific user's requests to understand their individual experience
- Find hidden timeouts even when percentile metrics look healthy
- Answer all these questions without having predicted them in advance
- Get answers within seconds to maintain your train of thought during investigation

### Monitoring vs. Observability

The authors push back against marketing-driven conflation. Some vendors claim "observability" is just another word for monitoring; others claim it means using logs, metrics, and traces together. The authors argue for judging tools by outcomes: can the tool help you achieve a high degree of observability?

### Technological Step Changes

The "three pillars" model (logs, metrics, and traces in separate data stores) was historically necessary but creates fundamental problems. Correlation between different data types living in different stores is error-prone and inefficient. Engineers must maintain shared context in their brains while jumping between tools.

The key innovation: **unified telemetry** -- capturing all debugging-relevant data as the same data type in a single data store. This eliminates artificial correlation problems and enables a fundamentally higher degree of observability. The authors term this the shift from "multiple pillars" to "unified" observability, and argue it is the only genuine paradigm shift the industry has seen in this space.

---

## Chapter 2: Performance Engineering with Observability

### The Case for Performance Engineering

The chapter opens with a real Honeycomb story: in December 2021, the team discovered that their HTTP router was being discarded and recreated after every request rather than reused as a singleton. The `regexp.Compile` path was consuming 17% of CPU because regular expressions were being recompiled on every request. The fix was just five lines of code, but the problem was invisible to distributed tracing because tracing hooks were called after the router had already been instantiated.

This experience prompted Honeycomb to build a systematic performance engineering practice integrated with their observability tooling.

### Building a Performance Engineering Practice

Performance engineering addresses two business needs: lowering costs and speeding up customer experiences. The core loop is: measure to find potential improvement, do the improvement, measure the effects, repeat.

Key principles:
- Like observability-driven development, performance engineering requires identifying the most impactful changes first
- Avoid premature optimization -- but have the visibility to know what actually needs optimizing
- Don't build a separate performance engineering team; spread the knowledge across all developers

### Optimizing Cost Without Modifying Code

**Infrastructure purchasing models** -- six models for compute capacity:
1. Capital expenditure (own datacenter)
2. Reserved capacity (AWS Savings Plans)
3. Persistent defined capacity (EC2, VMs)
4. Interruptible defined capacity (Spot, Preemptible)
5. Persistent elastic capacity (Fargate, Cloud Run)
6. Interruptible flexible (Lambda, Functions)

Each model has tradeoffs in cost, developer experience, and performance. The right answer is typically a mix. Observability data drives decisions about when to migrate between models.

**Fleet-wide optimization:**
- Squeeze: reduce task counts, CPU/memory allocations; test to find actual saturation limits
- Optimize: check CPU-to-memory-to-storage ratios; consider NVMe drives for I/O-bound workloads
- Migrate: switch to ARM architectures (AWS Graviton, Azure Cobalt, Google Axion) for significant cost savings

**Cost-optimizing Kubernetes:**
- Pack workloads efficiently; size machines to fit common pod configurations
- Use interruptible/spot instances for stateless workloads with the Karpenter plugin
- Monitor pod CPU utilization and memory usage via OpenTelemetry Collector daemonsets
- Use heatmaps instead of percentiles for saturation analysis (percentiles are misleading for wide-variance data)
- Identify biggest consumers first -- saving 1% of 10% is better than saving 5% of 1%

### CPU Profiling

**How profiling works:** The operating system interrupts a program at regular intervals, recording the program counter and stack frames. Over time, this builds a statistical picture of where time is spent -- at the function, line-of-code, and even assembly-instruction level.

**Flame graphs** are the recommended visualization: width represents total time in a function and its children, stacking represents call hierarchy, and individual flames represent collections of stack traces sharing the same function order.

**Scaling profile collection:** Continuous profiling tools (Grafana Pyroscope, Polar Signals, Blackfire) collect profiles continuously so you can interrogate them when needed, rather than having to "catch them in the act." OpenTelemetry is developing a standard profiling agent and encoding.

### Blending Performance Engineering and Observability

The real magic happens when profiles are indexed at the level of individual trace spans. This lets you understand *what* was slow, *for whom*, and *why/how* all at the same time.

**Honeycomb example:** Profiling revealed that a specific user's query was triggering hundreds of thousands of Lambda invocations, each serializing a complex protobuf-to-JSON conversion. Caching the serialization fixed the immediate problem. Further analysis showed the user's query used deeply nested if-else chains that could be simplified with a switch statement, dramatically improving execution time.

This behavior would never have appeared in traces (too expensive to trace each function in inner loops), but high-cardinality profiling on a per-customer basis revealed both the problem and the fix.

---

## Chapter 3: AI Observability

This entirely new chapter addresses the unique challenges of observing and improving applications powered by large language models (LLMs).

### Why Observability Matters for LLMs

LLMs introduce challenges that make traditional debugging approaches inadequate:

- **Open-ended inputs:** Natural language inputs are infinitely broader than programming languages or UIs. Users will do things you cannot predict.
- **Nondeterministic outputs:** The same input may produce different outputs on different runs. Temperature and top_p parameters affect randomness but don't guarantee repeatability.
- **Opaque systems:** You cannot step through LLM execution with a debugger. You generally cannot explain why a particular output was produced for a given input.
- **Failed early access programs:** Limited user testing introduces bias and fails to capture the full range of real-world usage patterns.

Key realities:
- Failure will happen -- it is a question of *when*, not *if*
- You cannot write unit tests for LLMs or practice TDD
- You will ship a "bug fix" that breaks something else
- These properties are not unique to LLMs, but LLMs make them dramatically more apparent

### Prompt Engineering Primer

Prompt engineering is a set of methods for steering LLM outputs toward desired results without changing the model. Prompts may contain instructions, data, user inputs, and example outputs. Even slight modifications to prompts can yield dramatically different outputs, requiring rigorous experimentation.

### Evaluations (Evals)

Evals are the foundation for making LLMs more reliable. They are similar to traditional software tests but have key differences:

**Two categories:**
- **Deterministic outputs:** Standard tests (e.g., checking that responses don't contain foul language)
- **Fuzzy outputs:** Tests that evaluate whether a response is "good" where many possible responses could be acceptable

**Three components of an eval:**
1. **Data:** Golden data (hand-created representative inputs/outputs) and larger datasets (synthetic or curated from production)
2. **Task function:** The actual LLM operation being tested
3. **Scoring function:** Determines if an output passes or fails

**Key principles:**
- The goal is NOT 100% pass rate; regularly passing all evals means you don't have enough representative inputs
- Evals are often run as the basis for experiments (testing new models, prompts, or RAG configurations)
- Build "good enough for production" evals first, then iterate with real-world data

### Designing Your Telemetry

The chapter provides detailed guidance on instrumenting LLM applications with OpenTelemetry:

**Simple LLM Call with Static Prompt:** Three spans -- overall tracking span, LLM call span, output parsing/validation span.

**Retrieval Augmented Generation (RAG):** Additional spans for embedding vector calculation, vector store retrieval (including which documents were selected), LLM call, and output parsing.

**Agents or Chained LLM Calls:** Parent span tracking all steps, with child spans for each LLM call correctly named and logging specific inputs/outputs.

**What to track:**
- User inputs
- LLM output (raw)
- Parsed/validated output
- All errors (network, timeout, LLM errors, parsing errors)
- User feedback (thumbs up/down) if available
- Token counts for cost tracking
- Prompt construction details for dynamic prompts

### Analyzing Telemetry for AI Applications

Multidimensional analysis is crucial. Rather than just asking "which errors are most common?", you can answer:
- Are users repeatedly entering the same inputs when they get errors?
- What commonalities exist in user inputs for the same error?
- Are there similarities between LLM outputs that lead to the same parsing error?
- Do identical user inputs result in different errors?

### Service-Level Objectives for LLMs

**Latency SLOs:** Track end-to-end latency including all steps (embedding calculation, LLM call, parsing). Start with development-time baselines; set thresholds at around 95% success over 7 days.

**Error Rate SLOs:** Any error in the pipeline counts as a failure. If internal testing shows 75% success, set the initial SLI at 75% and iterate upward.

**Alerting:** SLO alerts for LLMs should be non-urgent -- inform via Slack/Teams, never page. They signal the need for planned corrective action, not emergency response.

### Feeding Observability Data Back into Development

The authors describe a virtuous cycle:
1. Ship feature with "good enough" evals
2. Collect production telemetry
3. Analyze errors, inputs, and outputs
4. Feed production data back into evals (update golden data, expand test datasets)
5. Experiment with prompts, models, RAG configurations
6. Evaluate experiments against updated evals
7. Promote improvements to production
8. Repeat

**Intervening on correctable errors:** Many LLM output errors are "mostly correct" and can be programmatically fixed. Honeycomb's Query Assistant went from 75% success to 96% largely by programmatically correcting structural errors in LLM outputs (e.g., removing an invalid column from a COUNT operation). This is a source of quick wins but does not replace prompt engineering for long-term reliability.

### Evals and Observability Together

The core message: use both evals and observability, not one or the other. Evals provide a controlled environment for systematic iteration. Observability provides real-world production data. Together they form a virtuous cycle:

- Evals validate changes before production
- Observability reveals what users actually do
- Production data feeds back into evals
- Improved evals catch regressions

**Public benchmarks and generic metrics are not very helpful.** Provider benchmarks test general capabilities but say nothing about your specific business use case. Out-of-the-box metrics like "helpfulness" or "tone" can report high scores while saying nothing about actual usefulness. The one semi-useful generic metric is "grounding in facts" for RAG applications.

### Observability Is a Team Sport

LLM observability requires collaboration across roles:
- Software engineers must understand data quality and probabilistic systems
- ML engineers must understand user interactions and product behavior
- Product managers may need to learn Python and Jupyter for prompt experiments
- AI engineers, data scientists, and customer success teams all have stakes

LLMs force people at all levels to understand how users interact with their products. New modalities of interaction require new organizational responsibilities.

---

## Key Takeaways

1. **Observability is a property of software dependability**, not just a category of tools. It measures your ability to understand or debug any given system state.

2. **Unified telemetry is a paradigm shift.** Moving from fragmented "three pillars" (logs, metrics, traces in separate stores) to unified data in a single store eliminates correlation problems and enables fundamentally better debugging.

3. **Traditional monitoring is insufficient for distributed systems.** Binary up/down health checks cannot diagnose partial failures, degraded performance, or novel issues that have never been encountered before.

4. **Performance engineering and observability are complementary disciplines.** Profiling reveals inner-function-level detail; tracing provides cross-service visibility. When combined (profiles indexed to trace spans), they enable understanding of *what* is slow, *for whom*, and *why*.

5. **Cost optimization is a key performance engineering outcome.** Infrastructure purchasing models, fleet-wide optimization, Kubernetes bin-packing, and ARM migration all benefit from observability data.

6. **LLMs demand a fundamentally different approach to reliability.** Nondeterministic, opaque, and open-ended systems cannot be debugged with traditional methods. Observability is essential.

7. **Evals are the foundation for LLM reliability.** Build "good enough" evals with golden data and scoring functions, then iterate using real production data. The goal is not 100% pass rate.

8. **Production data feeds development.** The virtuous cycle of collecting telemetry, analyzing errors, feeding data back into evals, and iterating on prompts/models is the core methodology for reliable LLM applications.

9. **Programmatic correction of LLM outputs provides quick wins.** Honeycomb improved Query Assistant reliability from 75% to 96% largely by programmatically fixing structural errors in LLM outputs before resorting to prompt engineering.

10. **Public benchmarks and generic metrics are largely irrelevant.** Teams must invest in their own evals specific to their business domain and customer workflows.

11. **SLOs for LLM features should be non-urgently alerted.** Latency and error rate SLOs inform planned corrective action rather than triggering pages.

12. **LLM observability requires cross-functional collaboration.** New responsibilities must be adopted by existing roles; the technology forces organizations to deeply understand user interactions.
