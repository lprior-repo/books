# Best Practices — Cross-Topic Index

> **Extracted from 54 technical books** in the personal library at `/home/lewis/books`.
> **~77,000 lines across 55 deep-dive files** of distilled principles, do/don't
> rules, anti-patterns, and verbatim code snippets, drawn from `markdown_output/`
> + `summaries/`. Each book targets **30-50 pages** of extracted content
> (1,500-2,500 lines), with the deepest files exceeding 3,000 lines.
> Generated from a parallel sweep of the full book library.

---

## How to use this index

Each book has one deep-dive file under `best_practices/`. Files are tagged by topic
in their headers — use the topic sections below to jump straight to the books that
go deepest on what you need. Every deep-dive follows the structure in
`_TEMPLATE.md`: TL;DR → Best Practices by Topic (Principle / Do / Don't / Code) →
Anti-Patterns → Decision Heuristics → Key Takeaways → Cross-References.

**Tag legend:** `#testing` `#concurrency` `#architecture` `#api` `#cli` `#systems`
`#general` `#performance` `#cloud` `#platform` `#strategy` `#organization` `#leadership`

---

## #testing — 14 books

| Book | Coverage |
|------|----------|
| [The Art of Unit Testing (3E)](./The_Art_of_Unit_Testing.md) | Stubs/mocks/fakes/doubles, AAA, test design, isolation/seams, async patterns, parameterized tests, factory methods, legacy code, maintainability |
| [Fundamentals of Software Testing](./Fundamentals_of_Software_Testing.md) | Test process & levels, static review/analysis, EP/BVA/decision tables, coverage hierarchy, experience-based testing, risk-based testing, defect management |
| [TDD Top Tips](./TDD_Top_Tips.md) | Red/Green/Refactor discipline, behaviour-not-implementation, legacy-code strategy |
| [ATDD Guide](./ATDD_Guide.md) | Acceptance TDD, Gherkin DSL, protocol drivers, four-layer architecture |
| [What to Test and When](./What_to_Test_and_When.md) | Commit/Acceptance/Release/Production four-phase framework, decision tables |
| [The Feedback-Driven Developer](./The_Feedback-Driven_Developer.md) | Fast feedback loops, internal/external feedback, Pomodoro discipline |
| [100 Go Mistakes](./100_Go_Mistakes.md) | Full testing chapter: table-driven, mocking, flakiness, benchmark discipline |
| [Learning Go](./Learning_Go.md) | Rich: `go test`, table tests, fuzzing, benchmarks, httptest, race detector, goleak |
| [Mastering Go](./Mastering_Go.md) | Benchmarking, profiling, testable CLI design |
| [Shipping Go](./Shipping_Go.md) | Test in CI/release pipeline, golden tests |
| [Efficient Go](./Efficient_Go.md) | Efficient testing, `goleak.VerifyNone`, sink pattern |
| [Functional Programming in Go](./Functional_Programming_in_Go.md) | Property-based testing, pure-function testability |
| [Building Modern CLI Applications in Go](./Building_Modern_CLI_Applications_in_Go.md) | Testing CLIs, golden-file tests |
| [Concurrency in Go](./Concurrency_in_Go.md) | Testing concurrent code, `-race`, strategies for flaky async tests |

## #concurrency — 10 books

| Book | Coverage |
|------|----------|
| [Concurrency in Go](./Concurrency_in_Go.md) | **PRIMARY** — CSP, goroutines, channels, `select`, `sync` package, patterns (or/or-done/tee/bridge/fan-in), pipelines, context, heartbeats, rate limiting, replicated requests, testing |
| [Grokking Concurrency](./Grokking_Concurrency.md) | Hardware/cache/Flynn taxonomy, IPC menu, thread pools, Amdahl/Gustafson, pipeline/map/fork-join/map-reduce, mutex/semaphore/atomic, Coffman deadlocks, C10k, reactor/event-loop, async/await |
| [100 Go Mistakes](./100_Go_Mistakes.md) | Rich: 8+ channel/goroutine/mutex mistakes, sync package misuse, race conditions |
| [Learning Go](./Learning_Go.md) | Rich: goroutines, channels, select, sync.Once, WaitGroup, context (Cancel/Timeout/Deadline/Cause), channels-vs-mutex decision tree |
| [Mastering Go](./Mastering_Go.md) | Concurrency patterns, race detection |
| [Efficient Go](./Efficient_Go.md) | Coordination-free sharding, channel drainage, GC tuning |
| [Building Modern CLI Applications in Go](./Building_Modern_CLI_Applications_in_Go.md) | Goroutines in CLI tools |
| [Go Systems Programming](./Go_Systems_Programming.md) | Goroutines/channels/pipelines for Unix tooling, `sync.Mutex/RWMutex` |
| [System Programming Essentials with Go](./System_Programming_Essentials_with_Go.md) | GOGC/GOMEMLIMIT, sync.Pool, singleflight, mmap, modern runtime tuning |
| [Foundations of Scalable Systems](./Foundations_of_Scalable_Systems.md) | Distributed concurrency patterns, race conditions |

## #architecture — 10 books

| Book | Coverage |
|------|----------|
| [Fundamentals of Software Architecture](./Fundamentals_of_Software_Architecture.md) | **PRIMARY** — 4 C's, characteristics, ADRs, trade-off analysis, 8 styles (layered/pipeline/microkernel/SOA/event-driven/space-based/microservices), quantum, connascence, fitness functions, C4/UML, team topology, evolutionary architecture |
| [Building Microservices (2E)](./Building_Microservices.md) | **PRIMARY** — Boundaries, coupling, decomposition, migration/strangler fig, sync vs async, sagas, gateways/BFF, observability, resilience, Conway's law, when-NOT-to-use |
| [Software Architecture — The Hard Parts](./Software_Architecture_Hardparts.md) | Trade-off analysis, architecture quanta, granularity disintegrators/integrators, data decomposition, 8 saga patterns (Epic/Phone-Tag/Fairy-Tale/...), contract strictness, data mesh |
| [Software Architecture Patterns (2E)](./Software_Architecture_Patterns.md) | Layered/Microkernel/Event-Driven/Microservices/Space-Based styles with star ratings, monolithic-vs-distributed, technical-vs-domain partitioning |
| [Designing Distributed Systems](./Designing_Distributed_Systems.md) | Sidecar/Ambassador/Adapter single-node patterns; Replicated/Sharded/Scatter-Gather/FaaS serving; Work Queue/Copier/Filter/Splitter batch patterns |
| [Foundations of Scalable Systems](./Foundations_of_Scalable_Systems.md) | Scalability dimensions, coupling/cohesion, load balancing, caching, sharding/partitioning, replication, async/messaging, scale cube, capacity |
| [Learning Domain-Driven Design](./Learning_Domain_Driven_Design.md) | Ubiquitous language, subdomains, bounded contexts, context mapping, aggregates, value objects, domain events, layered/hexagonal/CQRS/event-sourcing |
| [Domain-Driven Design with Golang](./Domain_Driven_Design_with_Golang.md) | DDD applied to Go: aggregates, value objects, factories, repositories, hexagonal/clean architecture, anti-corruption layers |
| [Continuous API Management](./Continuous_API_Management.md) | API as product, lifecycle, governance, design-first OpenAPI, developer portals |
| [Learning API Styles](./Learning_API_Styles.md) | REST/GraphQL/gRPC/SOAP/async/webhooks style selection |

## #api — 10 books

| Book | Coverage |
|------|----------|
| [Mastering API Architecture](./Mastering_Api_Architecture.md) | REST/Richardson maturity, MS standards, pagination/filtering, PII hygiene, errors, OpenAPI tooling, gRPC `.proto`, REST/gRPC/GraphQL exchange modeling, test pyramid, Pact CDCs, OAuth2/JWT, STRIDE/DREAD, Kubernetes NetworkPolicy |
| [RESTful Web API Patterns & Practices](./Restful_Web_API_Patterns_and_Practices.md) | Four-layer separation, registered media types, ALPS profiles, embedded hypermedia, PUT-Create (`If-None-Match`/`If-Match`), repeatability, content negotiation, RFC 7807 Problem Details, health checks, fallback chains, semantic proxies, pagination rels, async 202 patterns |
| [Learning API Styles](./Learning_API_Styles.md) | REST/GraphQL/gRPC/SOAP/event-driven/webhooks comparison, schema/IDL, versioning, contracts, when-to-choose-which |
| [Continuous API Management](./Continuous_API_Management.md) | API product thinking, lifecycle, versioning/evolution, deprecation, governance, design-first, OpenAPI, developer portals, monetization |
| [Building Microservices](./Building_Microservices.md) | API design for services, contracts, backward compatibility, versioning, gateways, BFF, service discovery |
| [Building Modern CLI Applications in Go](./Building_Modern_CLI_Applications_in_Go.md) | `net/http` + rate limiting, timeouts/errors, REST clients |
| [Learning Go](./Learning_Go.md) | Error idioms (`errors.Is/As`, `%w`), HTTP client/server, middleware patterns |
| [100 Go Mistakes](./100_Go_Mistakes.md) | Error handling, function design, interfaces, generics |
| [Mastering Go](./Mastering_Go.md) | HTTP servers in Go |
| [Shipping Go](./Shipping_Go.md) | API packaging/release |

## #cli / #systems — 7 books

| Book | Coverage |
|------|----------|
| [Building Modern CLI Applications in Go](./Building_Modern_CLI_Applications_in_Go.md) | **PRIMARY** — Unix philosophy, flag/Cobra/Viper, stdin/signals/prompts, file reading, `os/exec`, `net/http`, timeouts/errors/panics, TTY-aware output, color/emoji/spinners, Zap logging, man pages, empathy-driven docs, cross-platform build tags, cross-compilation, CLI testing, Docker multi-stage + Compose, GoReleaser + Homebrew |
| [Go Systems Programming](./Go_Systems_Programming.md) | Unix-tool reimplementation (`pwd`/`which`/`find`/`wc`/`cp`/`dd`/`cat`), signal handling, goroutines/channels/pipelines for sysprog, `sync.Mutex/RWMutex`, race detection, TCP/UDP/RPC networking |
| [System Programming Essentials with Go](./System_Programming_Essentials_with_Go.md) | **Most modern (2024)** — Functional Options for testable CLIs, `filepath.WalkDir`, `fsnotify`, anonymous/named pipes, Unix sockets, GOGC/GOMEMLIMIT/ballast/arenas, `pprof`/`benchstat`, `sync.Pool`/`sync.Once`/`singleflight`/`mmap`, OpenTelemetry, QUIC, consistent-hashing distributed-cache capstone |
| [Mastering Go](./Mastering_Go.md) | CLI/systems techniques, networking, profiling |
| [Shipping Go](./Shipping_Go.md) | Distribution, cross-compilation, CI/CD for CLIs |
| [100 Go Mistakes](./100_Go_Mistakes.md) | Stdlib/CLI pitfalls |
| [Learning Go](./Learning_Go.md) | Modules, project layout for CLI tooling |

## #performance / #general — cross-cutting

| Book | Coverage |
|------|----------|
| [Efficient Go](./Efficient_Go.md) | Profiling (pprof/flame/trace), benchmark discipline, memory/GC/allocations, caching, resource leak detection |
| [Functional Programming in Go](./Functional_Programming_in_Go.md) | Pure functions, immutability, higher-order, currying, monads, `Option`/`Result`, FP design patterns |

---

## Source coverage map

```
Books in library:        ~94
Already-converted:       80 markdown / 89 summaries
Processed in this sweep: 54 books
Skipped:                 Test-Driven Development in Go (PDF-to-markdown
                         conversion produced images only — no .md)
NOTE:                   Communication Patterns folder contains Jacqui Read's
                         O'Reilly 2023 communication-skills book, NOT
                         Hohpe & Woolf's EAI messaging book — flagged in
                         that file.
```

## Coverage by source pair

Every deep-dive file is built from BOTH:
- The full book conversion: `markdown_output/<book>/<book>.md`
- The condensed summary: `summaries/<book>.md` (where present)

Cross-references between deep-dives are in each file's "Cross-References" section.

---

## #reliability & #observability — 4 books

| Book | Coverage |
|------|----------|
| [Modern Software Engineering — David Farley](./Modern_Software_Engineering.md) | **PRIMARY** — Optimizing for learning/feedback, managing complexity (modularity/cohesion/SoC/abstraction), iterative/incremental development, testability as design tool, engineering professionalism, empirical process control, technical debt management |
| [Engineering Resilient Systems on AWS](./Engineering_Resilient_Systems_on_AWS.md) | RAF/SEEMS model, RTO/RPO/BRT, AWS WAF/ALB/RDS Proxy/Aurora Global/SecretsCache/FIS, idempotency decorators, retry-with-jitter, circuit breaker lifecycle, graceful degradation, soft/hard TTL, zonal shift, multi-region failover |
| [Observability Engineering (2E ER)](./Observability_Engineering.md) | Kálmán observability definition, unified telemetry (logs/metrics/traces), golden signals, USE/RED methods, SLO/SLI/error budgets, profile-guided tracing, LLM observability |
| [Continuous Deployment](./Continuous_Deployment.md) | CD lineage (XP→DevOps→CI→CD), DORA metrics, lean one-piece flow, trunk-based dev, feature toggles, N/(N−1) backward compat, three DB-migration patterns, blue/green/rolling/canary trade-offs |

## #architecture — extended — 18 books

| Book | Coverage |
|------|----------|
| [Software Architecture Metrics](./Software_Architecture_Metrics.md) | Structural metrics (coupling/cohesion/complexity/connascence), process metrics (cycle time/MTTR), people metrics, fitness functions, leading-vs-lagging indicators, measuring tech debt |
| [Building Evolutionary Architectures (2E)](./Building_Evolutionary_Architectures.md) | Incremental change, fitness functions (atomic/holistic/triggered/continuous/temporal/dynamic), guided change, migration patterns, evolvability practices |
| [Software Architect Elevator](./Software_Architect_Elevator.md) | Architect as bridge business↔IT↔DevOps, full-stack architect role, modularization, scalability/elasticity/resilience, communicating architecture up/down the org |
| [Head First Software Architecture](./Head_First_Software_Architecture.md) | Qualities/non-functional reqs, architecture styles (layered/microservices/event-driven/space-based), designing for change, trade-off analysis |
| [Crafting Engineering Strategy — Will Larson](./Crafting_Engineering_Strategy.md) | Engineering strategy as design problem, diagnosis & prescription, team topologies, quality/velocity/reliability as strategy dimensions, developer productivity |
| [Building An Event-Driven Data Mesh](./Building_An_Event-Driven_Data_Mesh.md) | Data mesh principles (domain ownership, data-as-product, self-serve platform, federated governance), event-stream backbone, schema contracts |
| [Building Event-driven Microservices](./Building_Event-driven_Microservices.md) | Event-driven architecture, event storming, event sourcing, CQRS, sagas, reliable messaging, idempotency, dead-letter queues, schema evolution |
| [Flow Architectures](./Flow_Architectures.md) | Flow-based paradigm, streams, reactive streams, backpressure, composition, streaming SQL, stateful processors |
| [Microservices Up And Running](./Microservices_Up_And_Running.md) | Pragmatic microservices in production, granularity, inter-service comms, data management, transactions/saga, observability, deployment at scale |
| [Monolith To Microservices](./Monolith_To_Microservices.md) | Migration patterns: strangler fig, parallel run, change data capture, decompose by capability/transaction/verb, data decomposition, team structure |
| [Enabling Microservice Success](./Enabling_Microservice_Success.md) | Adopting microservices in orgs, team readiness, operational maturity, business case, reverse Conway, investment |
| [Cloud Application Architecture Patterns](./Cloud_Application_Architecture_Patterns.md) | Cloud-native: scaling, elasticity, caching, partitioning, replication, multi-region, circuit breaker, bulkhead, retry-with-backoff, observability, cloud-reliability patterns |
| [Learning Systems Thinking](./Learning_Systems_Thinking.md) | Stocks & flows, feedback loops, leverage points, delays, mental models, iceberg model, archetypes (fixes-that-fail, tragedy-of-the-commons, success-to-the-successful) |
| [Team Topologies (2E)](./Team_Topologies.md) | Four team types (stream-aligned/platform/enabling/complicated-subsystem), cognitive load, team interaction modes, team APIs, platform thinking |
| [Technology Strategy Patterns](./Technology_Strategy_Patterns.md) | Strategy formulation, technology radar, build-vs-buy, technical debt as portfolio, platform thinking, ecosystem strategy, option theory |
| [Building Multi-Tenant SAAS Architectures](./Building_Multi-Tenant_SAAS.md) | Multi-tenancy models (silo/pool), tenant isolation, data partitioning, identity, deployment, pricing tiers, onboarding |
| [Building Micro-Frontends](./Building_Micro-Frontends.md) | Micro-frontend principles, composition, integration approaches (build-time/server-side/runtime/edge), routing, state sharing, ownership |
| [Mastering Enterprise Platform Engineering](./Mastering_Enterprise_Platform_Engineering.md) | Internal developer platform, golden paths, paved road, self-serve infra, platform capabilities, adoption |
| [Platform Engineering — Camille F](./Platform_Engineering_Camille_F.md) | Platform-as-product, IDPs, measuring platform success, team topologies for platforms, DX |
| [Communication Patterns (O'Reilly 2023)](./Communication_Patterns.md) | **NOTE:** This is Jacqui Read's communication-skills book (visual/written/verbal/nonverbal, ADRs, async-first remote work, Nudge theory) — not Hohpe & Woolf's EAI book |

## Suggested learning order

1. **Foundations first:** Concurrency in Go → Grokking Concurrency → Learning Go → 100 Go Mistakes
2. **API/CLI discipline:** Mastering API Architecture → RESTful Web API Patterns → Building Modern CLI Applications in Go
3. **Architecture thinking:** Fundamentals of Software Architecture → Building Microservices → Designing Distributed Systems → Software Architecture Hardparts → Head First Software Architecture
4. **Reliability & engineering discipline:** Modern Software Engineering → Observability Engineering → Engineering Resilient Systems on AWS → Continuous Deployment
5. **Architectural evolution:** Building Evolutionary Architectures → Software Architecture Metrics → Crafting Engineering Strategy → Software Architect Elevator
6. **Distributed systems & microservices:** Building Event-driven Microservices → Building Microservices → Microservices Up And Running → Monolith To Microservices → Communication Patterns → Flow Architectures → Building An Event-Driven Data Mesh → Enabling Microservice Success
7. **Platforms, teams, org design:** Team Topologies → Mastering Enterprise Platform Engineering → Platform Engineering Camille → Technology Strategy Patterns → Cloud Application Architecture Patterns
8. **Frontier patterns:** Learning Systems Thinking → Building Micro-Frontends → Building Multi-Tenant SAAS
9. **Domain modeling:** Learning Domain-Driven Design → Domain-Driven Design with Golang
10. **Testing craft:** Art of Unit Testing → Fundamentals of Software Testing → TDD Top Tips → ATDD Guide
11. **Process & feedback:** Feedback-Driven Developer → Shipping Go → Continuous API Management
12. **Performance & rigor:** Efficient Go → Functional Programming in Go → System Programming Essentials with Go

---

## File map (sorted by topic coverage)

### Cross-cutting (most bang for buck — read these first)
- `Concurrency_in_Go.md` — 2,128 lines, ~140 code snippets, 22 clusters
- `Building_Microservices.md` — 1,079 lines, 19 clusters, 16 chapters
- `Shipping_Go.md` — 1,441 lines (full release engineering chapter)
- `Learning_Go.md` — 978 lines, ~58 KB
- `Building_Modern_CLI_Applications_in_Go.md` — 1,344 lines, ~61 snippets, 24 clusters
- `100_Go_Mistakes.md` — 1,033 lines, 100 anti-patterns captured
- `Fundamentals_of_Software_Architecture.md` — 923 lines, 27 clusters
- `Restful_Web_API_Patterns_and_Practices.md` — 993 lines, 32 clusters
- `Mastering_Api_Architecture.md` — 969 lines, 23 clusters
- `Domain_Driven_Design_with_Golang.md` — 964 lines, 13 Go-rich clusters
- `Learning_Go.md` — 978 lines

### Testing-focused
- `The_Art_of_Unit_Testing.md` — 1,104 lines, 22 clusters
- `Fundamentals_of_Software_Testing.md` — 628 lines, 16 clusters
- `The_Feedback-Driven_Developer.md` — 346 lines
- `TDD_Top_Tips.md` — 264 lines
- `ATDD_Guide.md` — 220 lines
- `What_to_Test_and_When.md` — 314 lines

### Architecture-focused
- `Designing_Distributed_Systems.md` — 848 lines
- `Software_Architecture_Hardparts.md` — 773 lines
- `Foundations_of_Scalable_Systems.md` — 530 lines
- `Learning_Domain_Driven_Design.md` — 559 lines
- `Software_Architecture_Patterns.md` — 463 lines

### API & CLI-focused
- `Continuous_API_Management.md` — 767 lines
- `Learning_API_Styles.md` — 763 lines
- `Go_Systems_Programming.md` — 708 lines
- `Grokking_Concurrency.md` — 747 lines
- `System_Programming_Essentials_with_Go.md` — 603 lines

### Cross-cutting Go
- `Mastering_Go.md` — 1,072 lines
- `Efficient_Go.md` — 490 lines
- `Functional_Programming_in_Go.md` — 608 lines

---

## Total extracted content

**54 best-practices files · INDEX + TEMPLATE = 56 files · ~77,000 lines · ~50+ Go code snippets per rich file · ~2,500+ principles distilled**

**Page distribution (30-50 page target):**
- 48 of 55 substantive files are at 30+ pages (1,500+ lines)
- 6 files under 30 pages are short source books (methodology guides 5-15pp, Early Release sources, etc.)
- Deepest: 100_Go_Mistakes (3,175L), DDD-with-Golang (3,062L), Mastering_Api_Architecture (3,037L), Functional_Programming_in_Go (2,918L), Mastering_Go (2,888L), Engineering_Resilient_Systems_on_AWS (2,862L)

Wave coverage:
- Wave 1 — concurrency, testing, CLI, API fundamentals (9 books)
- Wave 2 — cross-cutting Go + architecture foundations (17 books)
- Wave 3 — reliability, observability, metrics, evolutionary architecture, event-driven systems, microservices migration, platforms & org design (22 books)
- Wave 4 — depth expansion: every file re-extracted to 30-50 page target (50 files re-written)
