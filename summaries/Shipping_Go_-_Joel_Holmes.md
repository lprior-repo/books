# Shipping Go: Comprehensive Summary

**Author:** Joel Holmes
**Publisher:** Manning Publications, 2023

---

## Overview

*Shipping Go* is a practical guide that walks developers through building a complete software product from scratch, covering not just writing code but establishing the entire delivery pipeline. Written in a semi-narrative format, it places the reader in the shoes of a developer at a company that needs to replace a legacy translation service with a modern, scalable alternative. The book progresses from simple startup concerns through scaling challenges to production-grade infrastructure, always emphasizing that process, testing, and delivery are interconnected feedback loops rather than isolated activities.

The book uses Go as its primary language and GitHub Actions for CI/CD, deployed to Google Cloud Platform. However, its principles are explicitly language- and platform-agnostic, as demonstrated by appendices covering Kotlin, Python, JavaScript, and Terraform. The central thesis is that developers should think of product development as a continuous loop: develop, deliver, discuss, and design -- then repeat. Holmes draws extensively from industrial engineering, lean manufacturing, and the Toyota Production System to illustrate that software delivery follows the same patterns as physical product manufacturing, just with different materials.

The book is organized into three parts that mirror product maturity: Startup (chapters 1-4, covering initial setup, CI, testing, and deployment), Scaling (chapters 5-7, covering code quality, mocking and dependencies, and containers), and Going Public (chapters 8-11, covering configuration, integration testing, Kubernetes, and retrospective). Each part addresses three interwoven concerns -- process, testing, and delivery -- at increasing levels of sophistication.

---

## Part 1: Startup

### Chapter 1: Delivering Value

This opening chapter establishes the philosophical foundation of the book. Holmes draws extensively from industrial engineering and lean manufacturing -- particularly the Toyota Production System -- to explain how software teams should think about building products. The chapter does not contain any code; instead, it sets the mental framework that guides every subsequent chapter.

**Key concepts:**

- **Small pieces of work** reduce work-in-progress (WIP) and accelerate feedback. Drawing on Eliyahu Goldratt's *The Goal*, Holmes explains that WIP ties up revenue. When a developer spends three weeks on a feature nobody has tested, the investment in that developer's time (say $50/hour) generates zero return until the feature ships. Smaller chunks of work tie up less capital in the pipeline and reduce the risk of building the wrong thing.
- **The Four Ds** -- Develop, Deliver, Discuss, Design -- form a continuous feedback loop. Development writes code; delivery ships it; discussion gathers feedback from customers and stakeholders; design uses that feedback to plan the next iteration. This is the book's core rhythm, inspired by Toyota's practice of giving every assembly line worker the ability to stop production and suggest improvements.
- **Three pillars of continuous improvement**: Process (automation with a human touch -- automate the repetitive, let humans focus on creative work), Quality (approximating perfection through tests and checks -- quality is not the same as perfection, but a measurable approximation of it), and Delivery (shipping artifacts to get customer feedback -- without shipping, there is no feedback, and without feedback, there is no improvement).
- **The product development life cycle** mirrors the scientific method: hypothesis, experiment, results. You hypothesize that customers want a translation service, you build an MVP and deploy it (the experiment), and you observe how customers use it (the results).

The chapter outlines 10 progressive stages of product maturity that map to the rest of the book: initial setup, basic validation, zero-cost deployment, code confidence, integrations, portability, adaptability, user acceptance, scaled product, and end-to-end testing. Each stage adds capability without invalidating what came before, allowing teams to stop at any point that meets their needs.

### Chapter 2: Introducing Continuous Integration

The narrative begins with a product manager asking the reader to build a hello translation service in one day, with a live demo by tomorrow. The chapter demonstrates building a project from the ground up with process in mind from the very start.

**Key activities:**

- **README-driven development**: Before writing any Go code, Holmes creates a README.md with a thesis statement describing the product's purpose, a dependencies section (Go 1.18), a setup section (intentionally left blank as a reminder to fill it in), and release milestones (V0 in 1 day: onboarding documentation, simple API response, unit tests, running somewhere other than the dev machine; V1 in 7 days: translation endpoint, short-term storage, call existing service, long-term storage). The README becomes the living document and onboarding guide for the project -- a "lab notebook" for the experiment.

- **Standardized tooling via Makefile**: A Makefile provides repeatable commands for installing Go (pinned to version 1.18 to prevent "works on my machine" issues), building the project, and running tasks. The Makefile includes a `setup` target that installs Go from a specific download URL, extracts it to `/usr/local`, and configures the PATH. This ensures that every developer and every CI system uses the exact same toolchain. Holmes notes that TODO comments in the Makefile (like `#TODO add MacOS support`) are intentional signals for future contributors.

- **GitHub Actions pipeline**: The first pipeline is created before any application code exists. It lives at `.github/workflows/pipeline.yml` and defines a workflow triggered on pushes to the main branch. The workflow contains a single `build` job running on `ubuntu-latest` with steps to set up Go, check out code, build using `make build`, copy the binary to an artifacts directory, and upload it as a GitHub artifact using `actions/upload-artifact@v2`. This gives the team a downloadable binary from every commit.

- **The assembly line metaphor**: Just as Henry Ford's principles were to place tools and people in order of operation, optimize the flow for each station, and automate the line to move the product, a CI pipeline automates the flow from code commit to build artifact. The developer commits code (raw material), the pipeline assembles and validates it (the factory), and a build artifact is produced (the product). Importantly, Ford did not invent the assembly line -- he applied core principles to it. Similarly, CI/CD tools existed before GitHub Actions; what matters is the principle of automated flow.

- **Repositories as warehouses**: Code, tests, infrastructure definitions, and documentation all live in the same repository (single source of truth). Holmes draws a parallel to Pittsburgh's steel industry: proximity to raw materials and distribution networks drove success. Similarly, code should be close to the pipeline that processes it. A `.gitignore` file prevents binaries, test output, coverage files, and IDE artifacts from entering version control. Having test code in the same repository as product code means the pipeline can easily run integration tests after a build, without complex cross-repository triggers.

- **A minimal Go HTTP server**: The first application is a simple HTTP server in `cmd/main.go` listening on port 8080 that returns a hardcoded JSON response at the `/hello` endpoint:
```go
func main() {
    addr := ":8080"
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        enc := json.NewEncoder(w)
        w.Header().Set("Content-Type", "application/json; charset=utf-8")
        resp := Resp{Language: "English", Translation: "Hello"}
        enc.Encode(resp)
    })
    log.Fatal(http.ListenAndServe(addr, mux))
}
```
This is intentionally "dumb" code -- hardcoded, inflexible, and lacking error handling. But it proves the pipeline works end to end: commit code, pipeline builds it, artifact is produced. Other teams can download the binary and start integrating immediately, even before the business logic is complete.

The chapter emphasizes a counterintuitive but crucial lesson: build the pipeline before writing application code. This ensures process is foundational, not retrofitted. The pipeline is agnostic to the code -- if the product pivots from a hello-service to a good-bye-service, all the CI infrastructure remains unchanged.

### Chapter 3: Introducing Continuous Testing

The QA lead visits the developer, frustrated by buggy code and strained developer-QA relationships. The chapter opens with an important reframe: QA stands for quality assurance, but a single person or group will never be able to assure quality. Quality should be the focus of everyone in the company. This chapter establishes testing as a shared responsibility and introduces test-driven development as both a testing and a design practice.

**Testing approach:**

- **Systems Under Test (SUT)**: Break the monolithic main function into testable units -- service (translation logic), handler (HTTP request/response handling), and server (running the application) -- treating each as a black box. The goal is to test inputs and outputs, not implementation details.

- **Test-driven development (TDD)**: Following Kent Beck's red-green-refactor pattern, tests are written before implementation. A `translation` package is extracted from the main function with a minimal `Translate(word, language string) string` function that returns an empty string. The first test expects "hello" in English to return "hello" -- it fails (red), then the simplest fix is applied (just return the word), and it passes (green). Then the test list drives additional features: German, Finnish, unsupported languages, edge cases.

- **Given-When-Then format**: Tests follow a behavior-driven structure that maps directly from business requirements. The chapter builds a test list collaboratively with QA: translating "hello" to English returns "hello", to German returns "hallo", to Finnish returns "hei", unsupported languages return empty strings, unsupported words return empty strings, and edge cases like capitalization and whitespace are handled properly.

- **Table tests**: Go's idiomatic pattern for parameterized tests replaces repetitive individual test functions with an array of anonymous structs containing `Word`, `Language`, and `Translation` fields, iterated in a loop:
```go
tt := []struct {
    Word        string
    Language    string
    Translation string
}{
    {Word: "hello", Language: "english", Translation: "hello"},
    {Word: "hello", Language: "german", Translation: "hallo"},
    {Word: "hello", Language: "dutch", Translation: ""},
}
for _, test := range tt {
    res := translation.Translate(test.Word, test.Language)
    if res != test.Translation {
        t.Errorf(`expected "%s" to be "%s" from "%s" but received "%s"`,
            test.Word, test.Language, test.Translation, res)
    }
}
```

- **Input sanitization**: Testing edge cases reveals that the service needs to handle capitalization and whitespace. A `sanitizeInput` function converts to lowercase and trims spaces, demonstrating that testing drives better code -- not the other way around.

- **The testing pyramid**: Unit tests form the broad base (fast, isolated, numerous), integration tests form the middle, and end-to-end tests form the narrow top (expensive, fewer). An inverted "snow cone" pyramid is an anti-pattern: if you have many end-to-end tests but few unit tests, failures are hard to diagnose because you must untangle the entire system to find the root cause. A solid unit test foundation makes integration and end-to-end tests more reliable and easier to debug.

- **System tests**: HTTP handler tests use `httptest.NewRecorder()` and `http.NewRequest()` to test request/response cycles without starting a real server. Tests assert both the JSON body content and HTTP status codes (200 OK for found translations, 404 Not Found for missing ones). Common HTTP status codes are discussed: 2xx for success, 4xx for client errors, 5xx for server errors.

- **Pipeline integration and code coverage**: Tests are added as a quality gate before the build step -- a "quality sieve" that catches problems early. The Makefile gains `test`, `coverage`, and `report` targets. Coverage is enforced at 80% minimum using `go tool cover -func coverage.out | grep "total:" | awk '{print ((int($$3) > 80) != 1) }'`. HTML coverage reports are generated and uploaded as pipeline artifacts. Holmes notes that 100% coverage is not the goal -- arbitrary coverage targets lead to poorly written tests that are hard to maintain. The goal is meaningful tests that protect against business logic regressions.

Key Go testing patterns introduced: separate test packages (`translation_test` instead of `translation`) for true black-box testing where tests cannot access unexported functions, the Arrange-Act-Assert pattern, and using `go test ./... -cover` to see which code paths are exercised.

### Chapter 4: Introducing Continuous Deployment

The developer talks with operations staff early in the morning at the coffee machine. Ops is overwhelmed -- they have a backlog of deployments, system upgrades, and emergencies, and adding another project seems impossible. The solution: developers own their own deployments. The chapter references NASA's early space program, where Gene Kranz realized that engineers needed to become operators to close the knowledge gap between building systems and running them. This is the origin of DevOps -- blending development and operations so both teams understand each other's challenges.

**Key distinctions:**

- **Delivery vs. Deployment**: Delivery means producing an artifact (binary, container) for someone to use. Deployment means running that artifact as a live service. Not all products are deployed (e.g., libraries are delivered but not deployed), but all products should be delivered. A GitHub Release with an attached binary is the simplest form of delivery.

- **Minimal viable product (MVP)**: Ship early, get feedback, iterate. The book ships the first version in chapter 2, reinforcing that perfection is the enemy of progress. Many companies wait too long to get feedback because they want the product to be "stable" first. Holmes argues the opposite: ship the minimum, observe how it is used, and adjust.

- **"As a Service" spectrum** (from most to least abstraction):
  - **FaaS (Function as a Service)**: AWS Lambda, Google Cloud Functions. Highest abstraction, lowest control, pay per invocation. Best for startups because there are no idle costs.
  - **PaaS (Platform as a Service)**: Heroku, Google App Engine. Hand over source code, and the platform builds and runs it.
  - **CaaS (Container as a Service)**: AWS ECS, Google Cloud Run. Provide a container image, and the platform runs it.
  - **IaaS (Infrastructure as a Service)**: AWS EC2, Google Compute. Virtual machines you fully manage.

- **Health checks**: A `/health` endpoint returns `{"status":"up"}` -- essential for platforms to know whether to restart or route traffic to an instance. This becomes critical in later chapters when Kubernetes uses these endpoints for liveness and readiness probes.

- **FaaS deployment**: A `faas.go` proxy file wraps the existing `TranslateHandler` for Google Cloud Functions. The pipeline uses `google-github-actions/deploy-cloud-functions` to deploy automatically on pushes to main, with a curl test against the deployed URL to verify it works. Permissions must be set to allow public access via the `allUsers` member with the Cloud Function Invoker role.

- **PaaS deployment**: An `app.yaml` file configures Google App Engine with liveness and readiness checks (pointing to `/health`), runtime version (`go116`), and check intervals. The pipeline uses `google-github-actions/deploy-appengine` to deploy.

- **Service accounts**: A dedicated GCP service account with scoped permissions (App Engine admin, deployer, Cloud Build editor, Storage admin, Cloud Functions admin/developer) is created for pipeline deployments. Credentials are stored as a GitHub secret (`GCP_CREDENTIALS`) -- never in the repository. This follows the principle of least privilege.

The chapter demonstrates deploying to both FaaS and PaaS in parallel, showing how the same code can target multiple abstraction levels. After deployment, making a code change (adding French translation), pushing it, and watching the pipeline deploy it in minutes demonstrates the power of automated deployment for rapid iteration.

---

## Part 2: Scaling

### Chapter 5: Code Quality Enforcement

After a successful demo, the CTO asks how the process will scale across the organization. This chapter focuses on standardization and quality automation as the foundation for team growth.

**Code reviews:**

- **Pull requests**: Branch protection rules require one approval and passing CI checks before merging to main. PRs create accountability -- bugs become team failures, not individual ones. Holmes notes that even when working alone, he creates PRs for himself to review his own changes, catching mistakes he missed during initial development.
- **Review best practices**: Keep reviews under 300 lines (human attention span is limited; a review is like reading a recipe, not a novel). Keep an open mind (reviews are philosophical discussions, not political debates). Keep reviews moving (WIP is tied-up money -- at $50/hour, a review sitting for days wastes significant capital). Keep reviews interesting (team-building activities). Keep reviews standardized (PR templates with checklists).
- **PR template**: Includes description, associated task, and a checklist: code compiles correctly, tests added, all tests passing, documentation extended.

**Theory of Constraints:**

- Goldratt's theory states that optimizing non-bottleneck stations is pointless. In software, developers are the bottleneck. Everything should be done to protect and elevate developer productivity. Adding more people does not help (Brooks's Law: "nine women cannot make a baby in one month"). Instead, reduce rework (bugs) and streamline the pipeline.
- The "I Love Lucy" chocolate factory scene illustrates constraints: Lucy and Ethel cannot keep up with the assembly line, causing chocolates to pile up. The solution is not to speed up the conveyor belt (more features) but to help the constraint (reduce rework, provide better tools).

**Code standardization:**

- **Formatting**: `go fmt ./...` enforces Go's standard style. A `check-format` Makefile target (`test -z $$(go fmt ./...)`) verifies formatting in the pipeline by checking whether any files changed after formatting.
- **go vet**: Built-in static analysis catches bugs like format string mismatches, unreachable code, and suspicious function calls.
- **golangci-lint**: Extended linting with multiple linters configured in `.golangci.yml`. The book uses `gosec` (security checks), `godot` (comment punctuation), `misspell` (spelling), and `stylecheck` (enforcing comment standards). Holmes shares a personal anecdote where the linter caught a missing error check that would have hidden an underlying problem in production.
- **Pipeline ordering**: Format check and lint run in parallel before tests, because they are faster. This follows the "sieve" metaphor: progressively finer quality checks catch different-sized problems. Format check catches style issues in seconds; lint catches anti-patterns in a minute; tests verify behavior in a few minutes.

**Git hooks:** A pre-commit hook (`scripts/hooks/pre-commit`) runs `go fmt` on staged Go files and runs the linter locally, catching problems before they reach the CI pipeline. The `copy-hooks` Makefile target installs hooks into `.git/hooks/`.

**Developer flow:** Referencing Mihaly Csikszentmihalyi's research on "flow" states, Holmes argues that process should enhance, not interrupt, developer concentration. Overly strict checks can be as harmful as no checks. The key is finding the right balance for your team.

### Chapter 6: Testing Frameworks, Mocking, and Dependencies

An intern joins the team, and pair programming becomes the vehicle for exploring dependency management and advanced testing techniques. This is one of the most technically dense chapters, covering core software design patterns that enable testable, maintainable code.

**Dependency inversion principle:**

- "Depend on abstractions, not concretions." The electrical plug/outlet analogy: devices do not wire directly into the wall -- they use a standardized interface (the plug). Any device with the right plug works in any outlet.
- **Interfaces in Go**: The `Translator` interface is defined in the handler package (the consumer, not the provider -- following Go convention):
```go
type Translator interface {
    Translate(word string, language string) string
}
```
Go uses duck typing -- any struct with a `Translate(word, language string) string` method automatically satisfies this interface. No explicit `implements` declaration is needed.
- **Interface segregation**: Keep interfaces small and composable, like Go's standard library: `io.Reader` has one method, `io.Writer` has one method, and `io.ReadWriter` composes both.

**Dependency injection:**

- A `TranslateHandler` struct holds a `Translator` interface. A constructor function `NewTranslateHandler(service Translator)` injects the concrete implementation. Main wires everything together:
```go
func main() {
    translationService := translation.NewStaticService()
    translateHandler := rest.NewTranslateHandler(translationService)
    mux.HandleFunc("/translate/hello", translateHandler.TranslateHandler)
}
```
This refactoring causes pain -- tests break, the FaaS function needs updating -- demonstrating why interfaces should be established early rather than retrofitted later.

**Testing stubs:**

- A `stubbedService` struct satisfies the `Translator` interface with simple logic (returns "bar" for "foo", empty string otherwise). This decouples handler tests from the real service. The test uses obviously fake values ("foo", "bar", "baz") to signal that the test is about handler behavior, not service logic.

**Mocking with testify:**

- The `testify` library provides suites, mocks, and assertion helpers. A `RemoteServiceTestSuite` uses `mock.Mock` to create a `MockHelloClient`:
```go
type MockHelloClient struct {
    mock.Mock
}
func (m *MockHelloClient) Translate(word, language string) (string, error) {
    args := m.Called(word, language)
    return args.String(0), args.Error(1)
}
```
- Mocks verify both inputs and outputs: `suite.client.On("Translate", "foo", "bar").Return("baz", nil)` sets expectations. `suite.client.AssertExpectations(suite.T())` verifies all expected calls were made.
- Tests verify case-insensitive input handling (the service should lowercase "Foo" to "foo" before calling the client), error handling (returning empty string on client errors), and caching behavior (the remote service should only be called once for the same word/language pair, verified with `.Times(1)`).

**Fakes:**

- A fake HTTP server (`httptest.Server`) simulates an external API. The test suite uses a mock-backed handler to control responses (success, 404, 500, invalid JSON). The `APIClient` struct calls the external endpoint via HTTP POST, handles various status codes, and parses JSON responses. Tests cover the happy path, API errors, and malformed JSON responses.

**Comparison of test doubles:**

| Type | Pros | Cons |
|------|------|------|
| Stub | Easy to create and manipulate | Verification of interactions becomes complicated |
| Mock | Records interactions for later verification | More complex setup and teardown |
| Fake | Higher-fidelity simulated system interactions | Complicated to write and maintain |

Holmes warns that complicated test doubles are a "canary in the coal mine" -- if your mocks are getting overly complex, your code may need to be broken into smaller, more focused pieces.

### Chapter 7: Containerized Deployment

Carol from the mobile app team needs to run the API locally, but binaries compiled for Linux will not work on macOS or Windows. The solution is containers. The chapter uses the shipping container analogy: standardized ISO containers (8 feet wide, 20-40 feet long) revolutionized global shipping by allowing the same container to travel on trucks, trains, and ships without repacking.

**Container fundamentals:**

- Containers are virtualized operating systems that share the host kernel. Unlike full virtual machines, they are lightweight because they do not need separate kernel resources. A container image is a snapshot of what the system should look like; a running container is an instance of that image.
- Layered architecture: Base OS image -> Language runtime -> Application. Each layer adds size and potential security vulnerabilities. Images are stored in registries (Docker Hub, GitHub Container Registry, Google Container Registry).

**Buildpacks:**

- Originally developed by Heroku (2011), Buildpacks automatically detect your language and build an optimized container image. Cloud Native Buildpacks extend this with `pack`, a CLI tool. Running `pack build hello-api --builder gcr.io/buildpacks/builder:v1` produces a container from source code without writing a Dockerfile. Buildpacks go through two stages: detection (does this look like a Go project?) and building (determine runtime, install dependencies, compile).

**Custom Dockerfile with multi-stage builds:**

```dockerfile
FROM golang:1.18 AS deps
WORKDIR /hello-api
ADD *.mod *.sum ./
RUN go mod download

FROM deps as dev
ADD . .
EXPOSE 8080
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags "-w -X main.docker=true" -o api cmd/main.go
CMD ["/hello-api/api"]

FROM scratch as prod
WORKDIR /
EXPOSE 8080
COPY --from=dev /hello-api/api /
CMD ["/api"]
```
The `scratch` base is completely empty -- Go binaries are self-contained, so the resulting image is only 4.74MB, compared to 962MB for the dev image and 129MB for the Buildpack image. This is a 96% size reduction with zero OS-level attack surface.

**Docker Compose:**

- A `docker-compose.yml` file organizes multiple containers with profiles (`dev` and `prod`), port mappings, and build contexts. Profiles allow targeted deployments: `docker-compose --profile prod up` runs the production image. Compose files serve as both local development configuration and CI build definitions.

---

## Part 3: Going Public

### Chapter 8: Configuration Management and Stable Releases

QA is nervous about rolling out the new system. The solution: configuration management that allows features to be toggled without code changes, combined with semantic versioning for clear communication about what changed.

**Configuration system:**

- A `Configuration` struct with fields for port, default language, legacy endpoint, database type, and database URL. Configuration sources are applied in priority order: defaults -> JSON file -> environment variables -> command-line flags. This layering means a developer can override any setting locally while production uses environment variables set by the infrastructure.
- Port validation ensures the format includes a colon prefix and is a valid number, reverting to the default (8080) if invalid.

**Feature hiding (the "blanks" analogy):**

- Car dashboards have plastic blanks where buttons would go in luxury models. The same manufacturing process produces both -- just with different features visible. Similarly, configuration combined with dependency injection allows the same binary to behave differently:
```go
var translationService rest.Translator
translationService = translation.NewStaticService()
if cfg.LegacyEndpoint != "" {
    client := translation.NewHelloClient(cfg.LegacyEndpoint)
    translationService = translation.NewRemoteService(client)
}
translateHandler := rest.NewTranslateHandler(translationService)
```
This enables the "strangler application" pattern: the new system depends on the old system for translations it does not yet have, gradually replacing functionality without a risky big-bang migration.

**Semantic versioning:**

- Version format: MAJOR.MINOR.PATCH (e.g., v1.2.3). Major = breaking changes, Minor = new features, Patch = bug fixes.
- An `/info` endpoint returns tag, commit hash, and build date -- values injected at compile time via `-ldflags` in the Makefile:
```makefile
TAG := $(shell git describe --abbrev=0 --tags --always)
HASH := $(shell git rev-parse HEAD)
DATE := $(shell date +%Y-%m-%d.%H:%M:%S)
LDFLAGS := -w -X github.com/holmes89/hello-api/handlers.hash=$(HASH) \
    -X github.com/holmes89/hello-api/handlers.tag=$(TAG) \
    -X github.com/holmes89/hello-api/handlers.date=$(DATE)
```
- Git tags trigger release builds. The pipeline uses `scottbrenner/generate-changelog-action` to auto-generate release notes from commit messages.

**Culture of accountability:**

- Westrum's generative vs. bureaucratic culture model. Generative cultures investigate failure rather than assigning blame, share responsibilities across team boundaries, and embrace new ideas. Toyota's "andon cord" -- where any worker can stop the entire production line -- is the model. Build and deployment failures should be visible to the whole team, and no additional work should proceed until the problem is resolved.

### Chapter 9: Integration Testing

The team decides to fully replace the legacy system using the "strangler application" pattern. This requires adding a database (Redis) and validating the entire system against user requirements using behavior-driven development.

**Behavior-driven development (BDD):**

- Unlike TDD (which tests units of code), BDD tests features from the user's perspective. Requirements are written in Gherkin syntax:
```gherkin
Feature: Translation Service
  @smoke-test
  Scenario: Translation
    Given the word "hello"
    When I translate it to "german"
    Then the response should be "Hallo"
```
- **Godog** (Go's Cucumber implementation) parses Gherkin feature files and maps steps to Go test functions. The main function is refactored: logic moves into an `API(cfg config.Configuration) *http.ServeMux` function, while `main()` just starts the server. This allows tests to create a configured application without starting a real HTTP listener.
- The test suite uses `resty` as an HTTP client and `httptest.Server` for the application server, with before/after hooks managing server lifecycle.

**Adding a database:**

- Redis is added as a key-value store for translations, matching the caching pattern already implemented. A `Database` struct satisfies the `Translator` interface using `go-redis/v9` to query translations stored in `word:language` key format. Docker Compose adds a `database` service using `redis:latest` with mounted data volumes containing a production data backup.
- The `dockertest` library spins up a Redis container for integration tests, mounting the data backup for realistic testing.

**Test tags and pipeline integration:**

- Feature scenarios are tagged with `@smoke-test` or `@regression-test`. Smoke tests run on every build (fast, basic functionality: "does it turn on?"). Regression tests run separately (comprehensive: "did previously working things break?"). The pipeline runs smoke tests after unit tests but before the build step.

### Chapter 10: Advanced Deployment

Traffic has grown, making on-demand services expensive. The team evaluates Kubernetes as a cost-effective scaling solution. Kubernetes sits between CaaS and IaaS -- it abstracts infrastructure through code-defined resources while handling load balancing, scaling, and restarts automatically.

**Kubernetes fundamentals:**

- **Deployments** define pods (groups of containers), replica sets (scaling), and health checks. A `deployment.yml` specifies the container image, ports, and replica count.
- **Services** route external traffic to deployments. A `service.yml` with type `LoadBalancer` creates a cloud load balancer.
- **Rolling deployments**: Liveness probes (is it running?) and readiness probes (can it receive traffic?) enable zero-downtime updates. Both use the `/health` endpoint created in chapter 4. The liveness probe checks every 3 seconds; if it fails, Kubernetes kills the pod and starts a new one. The readiness probe prevents traffic from being routed to a pod until it is ready -- enabling rolling updates where old pods stay alive until new ones are confirmed healthy.

**Deploying Redis with Helm:**

- Helm is a package manager for Kubernetes clusters. `helm install redis-cluster bitnami/redis --set password=$(random_string)` deploys a production-ready Redis instance.
- **ConfigMaps** define environment variables, decoupling configuration from the container image. **Secrets** store sensitive values (like the Redis password), though Holmes notes that Kubernetes secrets are merely obfuscated, not encrypted -- production systems should use a secret manager like Vault.
- The deployment configuration maps `DATABASE_URL` from the ConfigMap and `DATABASE_PASSWORD` from the Helm secret into the container's environment, making the same binary work in any Kubernetes namespace or cluster.

### Chapter 11: The Loop

The final chapter reflects on the entire journey and frames product development as a continuous cycle rather than a linear progression.

**Three phases of product development:**

- **Startup**: Build fast, establish minimal process, deploy cheaply (FaaS/PaaS). Like setting up a tent -- temporary, mobile. Automate anything you do more than once a week. The trick is recognizing the turning point when a project is here to stay and investing more heavily in quality.
- **Acceleration**: Standardize (linting, vetting, documentation), modularize (interfaces, dependency injection), and make portable (containers). Like building permanent structures. Continue accelerating because momentum is a compounding force. Holmes warns against over-engineering with a personal story of building an unnecessarily complex event-driven system that became a maintenance burden when the underlying library was deprecated within weeks.
- **Cruising**: Make flexible (configuration, feature flags), validate behavior (BDD testing), and scale infrastructure (Kubernetes). Focus on exploring and improving. When the cloud bill gets too high, that is the signal to consider reducing abstraction levels.

**The OODA Loop (Colonel John Boyd):**

- **Observe** -- Collect data (metrics, user feedback, cloud bills).
- **Orient** -- Analyze the data (what patterns emerge, what needs change).
- **Decide** -- Determine action (build features, change infrastructure, improve process).
- **Act** -- Execute (deploy, release, iterate).
- The book itself followed this pattern multiple times: observe the legacy system's cost -> orient around modern practices -> decide to build a replacement -> act by building it -> observe results -> repeat at each scaling inflection point.

**Elements of development revisited:**

- **Process**: Pipelines save time. Having a process for your process (periodic evaluation, metrics on build time and delivery time) enables continuous improvement. Toyota's model: when automation freed up employee time, they used it to improve their processes rather than being idle.
- **Testing**: Start with simple unit tests on deterministic code. If tests are constantly breaking or team members resist writing them, that is a process bug, not a testing bug. The eventual goal is freeing the team to do exploratory testing (performance, usability, edge cases) while automation handles regression.
- **Delivering**: Cloud technologies will change, but the principles remain: start cheap, observe usage, scale when needed. Follow the five Ws of investigation: Who uses it? What do they do? Where are they? When do they use it? Why do they use it?

---

## Appendices

**Appendix A: Using Kotlin** -- Demonstrates building the same translation API using Kotlin with the Quarkus framework. Covers Maven for building, `@QuarkusTest` with `testcontainers` for integration testing against a Redis container, `ktlint` for formatting, and containerizing with native compilation for minimal images.

**Appendix B: Using Python** -- Rebuilds the API using FastAPI with uvicorn, Poetry for dependency management, pytest for testing, and similar CI/CD patterns.

**Appendix C: Using JavaScript** -- Implements the same service in Node.js with Express, demonstrating the language-agnostic nature of the book's pipeline principles.

**Appendix D: Using Terraform** -- Provides an alternative to Kubernetes by using HashiCorp Terraform for infrastructure-as-code deployments, showing how to provision virtual machines, networking, and load balancers through declarative configuration files.

---

## Key Takeaways

1. **Build the pipeline first.** Establishing CI/CD before writing application code ensures process is foundational, not retrofitted. The pipeline should run the same commands developers use locally (via Makefile), keeping environments in sync. Process is agnostic to the code -- if the product pivots, the pipeline remains.

2. **Small, iterative work beats large batches.** Smaller changes mean faster feedback, less risk, easier debugging, and more frequent delivery. WIP is tied-up capital -- minimize it. A 2,000-line change can be broken into ten 200-line reviews that are each easier to verify.

3. **Testing is a spectrum, not a destination.** Start with unit tests on core logic. Add mocking and stubbing for dependency isolation. Progress to integration tests with real databases in containers. Use BDD for user-facing validation. The testing pyramid should be broad at the base (unit), narrow at the top (end-to-end). Code coverage targets should be meaningful (80%) rather than absolute (100%).

4. **Depend on abstractions.** Interfaces decouple your code from specific implementations, enabling dependency injection, easier testing, and the flexibility to swap services (static, remote, database) via configuration rather than code changes. Define interfaces where they are consumed, not where they are implemented.

5. **Configuration enables hidden features.** Feature flags, configurable endpoints, and switchable service implementations allow development, testing, and production to run the same binary with different behavior. This is critical for strangler application patterns and safe rollouts where features can be toggled without redeployment.

6. **Quality gates should be fast and early.** Format checks and linting run before tests; tests run before builds; smoke tests run before container builds. Each gate catches progressively different problems, and failures provide immediate, specific feedback. Move checks as close to the developer as possible (git hooks, local Makefile targets).

7. **Containers provide universal portability.** Buildpacks for optimized production images, custom Dockerfiles for minimal scratch-based images (Go binaries can be as small as 4.74MB with a scratch base), and Docker Compose for local development organization. The same artifact runs identically on every developer's machine and in every cloud environment.

8. **Start cheap, scale when needed.** FaaS -> PaaS -> CaaS -> Kubernetes. Each step reduces abstraction, increases control, and potentially reduces cost -- but adds operational complexity. Only move to the next level when metrics justify it. The cloud bill is usually the first signal.

9. **Culture matters as much as code.** Generative cultures that investigate failures, share responsibility, and encourage experimentation produce better software than bureaucratic cultures that assign blame and silo teams. Blameless postmortems, visible build failures, and collaborative code reviews build this culture. Everyone should have a voice about technical problems and team improvements.

10. **It is a loop, not a line.** The OODA loop (Observe, Orient, Decide, Act) applies to every level: individual features, team processes, product direction, and infrastructure decisions. Products do not "finish" -- they evolve through continuous feedback. The measure of success is how quickly you can observe, learn, and adapt.
