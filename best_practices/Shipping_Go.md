# Per-Book Best Practices — Deep Dive: Shipping Go

> **Source:** `markdown_output/Shipping_Go_-_Joel_Holmes/Shipping_Go_-_Joel_Holmes.md` (484K, 8,118 lines)
> **Companion summary:** `summaries/Shipping_Go_-_Joel_Holmes.md`
> **Author:** Joel Holmes (Manning, 2023)
> **Reading:** This book is the definitive "build the conveyor belt first" manual for shipping software in Go. It is half narrative (a junior dev shipping a translation API in two weeks) and half reference (every chapter produces runnable Go, YAML, Dockerfile, Kubernetes, Helm, Gherkin, Terraform manifests). Almost every modern Go deployment convention is grounded here, anchored to its industrial-engineering origin (Ford, Toyota Production System, Goldratt's *Theory of Constraints*, Westrum's organizational typology, Boyd's OODA loop).

---

# Shipping Go — Joel Holmes
**Author:** Joel Holmes
**Publisher:** Manning Publications, 2023
**Topic tags:** `#general` `#cli` `#systems` `#devops` `#api` `#testing`
**Language focus:** Go-first, language-agnostic (full Kotlin, Python, JavaScript, Terraform appendices)
**Sources:** `markdown_output/Shipping_Go_-_Joel_Holmes/Shipping_Go_-_Joel_Holmes.md` · `summaries/Shipping_Go_-_Joel_Holmes.md`

## TL;DR
Treat shipping as a three-tier product maturity loop — **Startup → Acceleration → Cruising** — each tier adding one new capability to an existing pipeline instead of bolting on a new one. The book is the rare Go text that explicitly orders: build the assembly line (CI) before the product (HTTP server), standardize the line (format + lint + vet + Git hooks) before scaling the team, containerize for portability before deploying, and graduate to Kubernetes only when the cloud bill forces it. Every artifact in the book has a stable URL, a version, a health check, and a roll-back path; tests run before builds, smoke tests run before container builds, integration tests run against real databases in containers, and deployments are gated by Git tags.

---

## Best Practices by Topic

### 1. The Industrial Engineering Frame (Mindset)
**Principle:** Software delivery is industrial engineering applied to a digital assembly line — model it on Ford's flow optimization and the Toyota Production System (TPS), not on individual artisan craft.

**Do:**
- Treat source commits as *raw material*, pipelines as the *factory*, and binaries/containers as *finished products* on a dock.
- Adopt TPS's *automation with a human touch*: automate every task you perform more than once a week, but keep humans in the design loop.
- Quote the Three Pillars of continuous improvement: **Process**, **Quality**, **Delivery** — every chapter in the book maps to exactly one of these.
- Keep feedback loops tight: develop → deliver → discuss → design (the "Four Ds"), then loop.
- Embrace *incremental shipping*: a one-day MVP beats a perfect-spec unreleased project.
**Don't:**
- Skip the assembly line because "we're a small team." Productivity collapse follows process debt at every headcount.
- Confuse *automation* with *abandoning judgment*: machine-checks never replace code review or design discussion.
- Let *quality* mean "perfection" — it is an approximation verified by tests, not by wishful thinking.

*Ref: Shipping_Go.md — "1 Delivering value" / "1.1 Simple concepts" / "1.2 Small pieces"*

---

### 2. The Four Ds Loop (Feedback Cycle)
**Principle:** Product development is a continuous loop, not a waterfall: Develop → Deliver → Discuss → Design, then back to Develop.

**Do:**
- Make *delivery* the boundary of every iteration — no work counts as "done" until a customer can use it.
- Pair *Discuss* and *Design* before the next *Develop* cycle, treating feedback as the design input.
- Treat production feedback (metrics, error rates, support tickets) as equal-weight to internal review feedback.
- Use the loop to drive the next sprint's test cases — what customers complain about becomes your regression test list.
**Don't:**
- Conflate the loop with Agile/Scrum ceremonies; the Four Ds are about artifact flow, not standups.
- Skip the *Discuss* phase for "obvious bugs" — the root cause is often social, not technical.
- Replace discussion with feature flagging and skip customer input entirely.

*Ref: Shipping_Go.md — "1 Delivering value" — "Develop, deliver, discuss, design loop" (Figure 1.2)*

---

### 3. WIP Reduction / Small Iterative Steps (Theory of Constraints)
**Principle:** Optimizing non-bottleneck stations is pointless — in software the developer is the bottleneck, so protect their time by shrinking WIP.

**Do:**
- Limit pull-request size to **≤ 300 lines** of code + tests; smaller is faster to review, easier to merge, and cheaper to revert.
- Break a 2,000-line feature into ten 200-line PRs; the reviewers can focus, you merge faster, and roll-back granularity improves.
- Track WIP cost in dollars: at $50/hr, a three-week unreleased feature is **$6,000 of dead capital** (Goldratt's *The Goal*).
- Use the *I Love Lucy* chocolate factory heuristic: speeding up the conveyor belt when the wrapper is the constraint just creates a pile of unwrapped chocolates.
**Don't:**
- Add headcount to speed up a software project (Brooks: "nine women cannot make a baby in one month").
- Treat PR backlog as a status symbol; it is *typoed capital*, not leverage.
- Couple "small PR" with "no tests" — small PRs demand *more* coverage because they ship more often.

*Ref: Shipping_Go.md — "1.2 Small pieces" / "5.2 Constraints on development"*

---

### 4. Build the Pipeline BEFORE the Code (Anti-Retrofit)
**Principle:** Establishing CI/CD before application code exists ensures process is foundational, not retrofitted.

**Do:**
- On day one, commit the README, Makefile, and `.github/workflows/pipeline.yml` *before* the first Go file.
- Configure the pipeline with placeholder steps (format-check, test, build, deliver) even when `cmd/main.go` is empty.
- Let the pipeline be *language- and product-agnostic*: replacing "hello-api" with "goodbye-api" requires zero pipeline edits.
**Don't:**
- Treat CI setup as a "we'll get to it" task — retrofitting PRs and hooks into a sprawling codebase is exponentially harder.
- Pipeline-first only works if the pipeline itself is real (runnable); a documented pipeline that nobody uses is decorative.
- Tie the pipeline to one branch name early; design it for both `main` and PRs from the start.

*Ref: Shipping_Go.md — "2 Introducing continuous integration" — "2.5 Material"*

---

### 5. README-Driven Development (Living Lab Notebook)
**Principle:** The README is the project's thesis statement, onboarding doc, and change-log-by-construction. Write it before any code.

**Do:**
- Open a project by writing a README with: thesis, dependencies, setup (intentionally blank as a *TODO* trigger), and release milestones (`V0` in 1 day, `V1` in 7).
- Use the README to make your *first* design decision explicit: which language, which runtime, which targets.
- Treat Setup and Dependencies sections as living — every process change produces a README edit in the same PR.
**Don't:**
- Skip the README "until things stabilize" — onboarding cost compounds as the team grows.
- Hardcode setup steps in a CONTRIBUTING.md that nobody reads; the README is read first.

```md
# Hello API

This is an improved version of the current hello-api we use in production. It will use less
memory and be cheaper to run in production, and it will scale, expand to additional
words, and be more stable.

## Dependencies
- Go version 1.18

## Setup

## Release Milestones
### V0 (1 day)
- [ ] Onboarding Documentation
- [ ] Simple API response (hello world!)
- [ ] Unit tests
- [ ] Running somewhere other than the dev machine
### V1 (7 days)
- [ ] Create translation endpoint
- [ ] Store translations in short-term storage
- [ ] Call existing service for translation
- [ ] Move towards long-term storage
```
*Ref: Shipping_Go.md — "Listing 2.1 README.md" / "2.1 Where to start?"*

---

### 6. Makefile as Standardized Toolchain Entry Point
**Principle:** A Makefile gives every developer and the pipeline the same commands; this is what makes CI/CD *repeatable*.

**Do:**
- Pin tool versions in the Makefile (Go `1.18`, linter `v1.41.1`) so developers and CI build with identical binaries.
- Provide one Makefile target per pipeline step: `setup`, `install-go`, `init-go`, `build`, `test`, `coverage`, `report`, `check-format`, `static-check`.
- Add a `#TODO` comment for every known gap (e.g. MacOS support) — it is a *signal*, not a smell.
- Surface the *exact* install steps (download URL, extract path, `PATH` export) so onboarding is one `sudo make setup` away.

```makefile
GO_VERSION := 1.18

.PHONY: install-go init-go

setup: install-go init-go
#TODO add MacOS support
install-go:
	wget "https://golang.org/dl/go$(GO_VERSION).linux-amd64.tar.gz"
	sudo tar -C /usr/local -xzf go$(GO_VERSION).linux-amd64.tar.gz
	rm go$(GO_VERSION).linux-amd64.tar.gz
init-go:
	echo 'export PATH=$$PATH:/usr/local/go/bin' >> $${HOME}/.bashrc
	echo 'export PATH=$$PATH:$${HOME}/go/bin' >> $${HOME}/.bashrc

build:
	go build -o api cmd/main.go
```
**Don't:**
- Spread build commands across shell scripts, README steps, and CI YAML; the Makefile is the single source of truth.
- Use environment defaults that aren't visible in `make setup` — every environmental dependency the project has must be in a target.

*Ref: Shipping_Go.md — "Listing 2.2 Makefile" / "Listing 2.5 pipeline.yml (Makefile build target)"*

---

### 7. GitHub Actions as the Assembly Line (First Pipeline)
**Principle:** A CI system is just an application that moves code along predefined steps — start with one job (build) and one artifact (binary), then add gates.

**Do:**
- Trigger on push to `main` *and* on pull requests, so reviews run the same checks.
- Pin Go via `actions/setup-go@v2` with `go-version: ^1.18` (any compatible minor — never `latest`).
- Always checkout + cache before running build; keep `runs-on: ubuntu-latest` unless you need a specific OS.
- Run the same `make build` the developer runs locally — uniformity between local and CI is the whole point.
- Use `actions/upload-artifact@v2` to make the binary downloadable from the Actions run page — this is *delivery* before *deployment*.

```yaml
name: CI Checks
on:
  push:
    branches:
      - main
jobs:
  build:
    name: Build App
    runs-on: ubuntu-latest
    steps:
      - name: Set up Go 1.x
        uses: actions/setup-go@v2
        with:
          go-version: ^1.18
      - name: Check out code into the Go module directory
        uses: actions/checkout@v2
      - name: Build
        run: make build
      - name: Copy Files
        run: |
          mkdir artifacts
          cp api artifacts/.
      - name: Archive
        uses: actions/upload-artifact@v2
        with:
          name: api
          path: artifacts
```
**Don't:**
- Use `latest` for Go, linter versions, or any tool — pipelines that drift break the "same environment" promise.
- Skip artifact upload; the binary on the Actions page is what makes "delivery" tangible to non-developers.

*Ref: Shipping_Go.md — "Listing 2.4 pipeline.yml" / "Listing 2.3 README.md"*

---

### 8. .gitignore Hygiene (Repos as Warehouses)
**Principle:** Binaries, test data, coverage files, and IDE artifacts don't belong in version control; the repo must contain only source that the pipeline can re-process.

**Do:**
- Start every Go project with a Go-template `.gitignore` (binaries, `.exe`, `.dll`, `.so`, `.dylib`, `.test`, `.out`).
- Add `coverage.out` and `cover.xhtml` once coverage gating begins.
- House product code, test code, infrastructure definitions, and tests *all in one repo* — proximity drives productivity (Pittsburgh steel analogy).
- Keep tests next to product code so the same pipeline can build and integration-test without cross-repo triggers.
**Don't:**
- Add `.gitignore` rules *after* you've committed the things you don't want — repositories don't forget.
- Split tests into a sibling repo to "decouple" them; you lose single-source-of-truth and gain hard dependencies.

```gitignore
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib
# Test binary, built with `go test -c`
*.test
# Output of the go coverage tool, specifically when used with LiteIDE
*.out
# Dependency directories (remove the comment below to include it)
# vendor/
api
coverage.out
cover.xhtml
```
*Ref: Shipping_Go.md — "Listing 2.5 .gitignore" / "2.4 Warehouses"*

---

### 9. The "Dumb First Server" (Prove the Pipeline, Then Code)
**Principle:** Ship a hard-coded, inflexible first version to prove the pipeline end-to-end before adding business logic.

**Do:**
- Write the minimum HTTP handler that returns a single hard-coded JSON response — the goal is to verify commit → pipeline → artifact flow.
- Realize the test for "intentionally dumb code" comes *first*; logic layers come in chapter 3.
- Treat every commit as two artifacts: source + binary; both must be reproducible from the repo alone.

```go
package main
import (
    "encoding/json"
    "log"
    "net/http"
)
func main() {
    addr := ":8080"
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        enc := json.NewEncoder(w)
        w.Header().Set("Content-Type", "application/json; charset=utf-8")
        resp := Resp{Language: "English", Translation: "Hello"}
        if err := enc.Encode(resp); err != nil {
            panic("unable to encode response")
        }
    })
    log.Printf("listening on %s\n", addr)
    log.Fatal(http.ListenAndServe(addr, mux))
}
type Resp struct {
    Language    string `json:"language"`
    Translation string `json:"translation"`
}
```
**Don't:**
- Block the pipeline build on "real" business logic — the pipeline must be green *before* the product is interesting.
- Add error handling, logs, config, or frameworks in v1 — defer until v2 so reviewers can read the diff in 30 seconds.

*Ref: Shipping_Go.md — "Listing 2.6 main.go" / "2.5 Material"*

---

### 10. Single-Repository, Multi-Purpose Workspace (Pittsburgh Steel)
**Principle:** Code, tests, infra-as-code, and documentation belong in one repo so the pipeline can do build → integration-test → deploy without cross-repo triggers.

**Do:**
- Keep `cmd/`, `pkg/`, `handlers/`, `translation/`, `config/`, `k8s/`, `Dockerfile`, `docker-compose.yml`, `Makefile`, `.github/` in one repo.
- Treat the repo as a *warehouse*: raw materials go in (commits), finished goods come out (binaries, containers, releases).
- Document that not every project needs this; if a project is split, document the cross-repo trigger in both places.
**Don't:**
- Separate "ops repo" from "app repo" — pipeline orchestration becomes a network of brittle webhooks.

*Ref: Shipping_Go.md — "2.4 Warehouses" — Pittsburgh steel-city example*

---

### 11. TDD / Red-Green-Refactor (Kent Beck Discipline)
**Principle:** Write the test first, see it red, write the minimum code to make it green, then refactor — this is also a design practice, not just a verification one.

**Do:**
- Establish a *test list* before any code: Given/When/Then sentences that translate directly into Go tests.
- Write the smallest test that fails for the right reason, then make it pass with the dumbest possible code.
- Cross off list items as you cover them; the surviving list is the *next* sprint.
- Treat TDD as an experiment: hypothesis (translation works) → experiment (call the function) → results (assertion passes/fails).
**Don't:**
- Skip the failing step — a green test that never went red hasn't proven anything about its own ability to fail.
- Use TDD to over-design; "duct tape programmer" (Ian Cooper) — get the test green with the dumbest code, then refactor.
- Change the test instead of the implementation unless the business rule actually changed.

*Ref: Shipping_Go.md — "3.2 Writing unit tests" — Red/green/refactor (after "Listing 3.4 translator.go")*

---

### 12. Given-When-Then / Arrange-Act-Assert
**Principle:** Test bodies should mirror the business sentence that produced them — this makes tests self-documenting and audit-able.

**Do:**
- Write the test list in *Given a word when translated to language X should return Y* form.
- In Go, structure as **Arrange** (variables) → **Act** (call) → **Assert** (`t.Errorf` with inputs and outputs in the message).
- Make assertion messages informative: include *input*, *expected*, and *actual* so a single failure tells the full story.

```go
// Arrange
word := "hello"
language := "english"
// Act
res := translation.Translate(word, language)
// Assert
if res != "hello" {
    t.Errorf(`expected "hello" but received "%s"`, res)
}
```
**Don't:**
- Use a generic `t.Errorf("wrong")` — every assertion message must answer "what input produced what wrong output".
- Skip the Arrange block; the test should be readable top-to-bottom without scanning the Act line for setup.

*Ref: Shipping_Go.md — "Listing 3.3 translator_test.go" / "3.2 Writing unit tests"*

---

### 13. Table Tests (Idiomatic Parameterization in Go)
**Principle:** Replace copy-pasted test functions with anonymous-struct slices and a single for-loop — adds cases in 3 lines instead of 30.

**Do:**
- Use a `tt := []struct{ Word, Language, Translation string }{...}` literal; cases live as data, not as code.
- Loop `for _, test := range tt { ... }`; the assertion block stays small, focused, and uniform.
- Use obviously-fake values (`foo`, `bar`, `baz`) when stubbing, real words when integration-testing.
- Add a case to the slice to add a test — never duplicate a function.

```go
tt := []struct {
    Word        string
    Language    string
    Translation string
}{
    {Word: "hello", Language: "english", Translation: "hello"},
    {Word: "hello", Language: "german",  Translation: "hallo"},
    {Word: "hello", Language: "finnish", Translation: "hei"},
    {Word: "hello", Language: "dutch",   Translation: ""},
    {Word: "hello", Language: "French",  Translation: "bonjour"},
    {Word: "Hello", Language: "german",  Translation: "hallo"},
    {Word: "hello ", Language: "german", Translation: "hallo"},
}
for _, test := range tt {
    res := translation.Translate(test.Word, test.Language)
    if res != test.Translation {
        t.Errorf(
            `expected "%s" to be "%s" from "%s" but received "%s"`,
            test.Word, test.Language, test.Translation, res)
    }
}
```
**Don't:**
- Keep a separate `TestFoo`, `TestBar`, `TestBaz` — that's anemic table-test avoidance with extra steps.
- Forget negative cases (empty strings, unsupported values) and edge cases (capitalization, whitespace) — they belong in the same table.

*Ref: Shipping_Go.md — "Listing 3.7 translator_test.go" / "3.3 Refactor, refactor, refactor"*

---

### 14. Systems Under Test (SUT) — Black Box Boundaries
**Principle:** Break monolithic functions into testable units — service, handler, server — and test each as a black box from the start.

**Do:**
- Extract a `translation` package with `Translate(word, language string) string` — small surface, maximum testability.
- Test across three layers: **service** (pure logic), **handler** (HTTP I/O), **server** (lifecycle).
- Define interfaces based on what the *handler* needs (consumer), not what the service offers — this enables dependency injection later.
**Don't:**
- Keep business logic inside `func main()`; it is not testable, period.
- Test implementation details (private variables, internal state); only the public surface matters.

*Ref: Shipping_Go.md — "3.1 What to test" — "service, handler, and server"*

---

### 15. Black-Box Testing via `package x_test`
**Principle:** Use `package translation_test` (with the `_test` suffix) instead of `package translation` to remove access to unexported identifiers — tests assert *behavior*, not internals.

**Do:**
- Drop tests into a `_test` package so the test binary can only see the public surface.
- This forces tests to drive the *interface* rather than the *guts*; later refactors stay free to reshape internals.
- Combine with `go test ./... -cover` for free coverage reporting per package.
**Don't:**
- Reach into private fields with `package_internal_test` helpers — that couples tests to implementation.
- Skip the `_test` package until refactoring becomes painful; the pain compounds.

*Ref: Shipping_Go.md — "Listing 3.3 translator_test.go" / "3.2 Writing unit tests" (footnote ❶)*

---

### 16. Input Sanitization Discipline
**Principle:** Services must normalize inputs (case, whitespace) at the boundary; testing reveals this need before production does.

**Do:**
- Add a `sanitizeInput(w string) string` helper that lowercases and trims — call it at the top of every public entry point.
- Cover capitalization (`Hello` vs `hello`), whitespace (`" hello "`), and case-of-language (`German` vs `german`) in your table tests.

```go
func Translate(word string, language string) string {
    word = sanitizeInput(word)
    language = sanitizeInput(language)
    if word != "hello" {
        return ""
    }
    switch language {
    case "english": return "hello"
    case "finnish": return "hei"
    case "german":  return "hallo"
    default:        return ""
    }
}
func sanitizeInput(w string) string {
    w = strings.ToLower(w)
    return strings.TrimSpace(w)
}
```
**Don't:**
- Sanitize inside the data store — the boundary is where it belongs, exactly once.
- Skip edge cases "because QA will find them" — Alan Perlis: "software system can best be designed if the testing is interlaced with the designing".

*Ref: Shipping_Go.md — "Listing 3.12 translator.go" / "3.3 Refactor, refactor, refactor"*

---

### 17. The Testing Pyramid (Pyramid, Not Snow Cone)
**Principle:** Unit tests are the broad base, integration tests the middle, end-to-end tests the narrow top — each layer runs separately because cheaper layers fail faster.

**Do:**
- Run unit tests on every commit (seconds).
- Run integration tests after unit tests pass but before build (seconds to minutes).
- Run E2E tests only after a release candidate exists — they're expensive and flaky.
- Invert the pyramid ("snow cone" with too many E2E tests) and you're untangling the whole system for every regression.
**Don't:**
- Build a test suite that's 80% end-to-end — failures become unfalsifiable.
- Skip unit tests because "we have integration tests" — they catch different bugs at different speeds.

*Ref: Shipping_Go.md — "3.4 Testing pyramid" — Figure 3.2*

---

### 18. System / Handler Tests with `httptest`
**Principle:** Test HTTP request/response cycles without binding a port — use `httptest.NewRecorder()` and `http.NewRequest()`.

**Do:**
- Capture the response body via `json.Unmarshal(rr.Body.Bytes(), &resp)`; assert both the body *and* the status code.
- Use table tests of `{Endpoint, StatusCode, ExpectedLanguage, ExpectedTranslation}` to drive the test.

```go
rr := httptest.NewRecorder()
req, _ := http.NewRequest("GET", "/hello", nil)
handler := http.HandlerFunc(rest.TranslateHandler)
handler.ServeHTTP(rr, req)
if rr.Code != http.StatusOK {
    t.Errorf(`expected status 200 but received %d`, rr.Code)
}
var resp rest.Resp
json.Unmarshal(rr.Body.Bytes(), &resp)
if resp.Translation != "hello" {
    t.Errorf(`expected Translation "hello" but received %s`, resp.Translation)
}
```
**Don't:**
- Bind a real port via `net.Listen` for tests — `httptest` is faster, parallel-safe, and hermetic.
- Forget the status code; an HTTP handler is only correct if status *and* body match the contract.

*Ref: Shipping_Go.md — "Listing 3.14 translator_test.go" / "3.5 System testing"*

---

### 19. Coverage Gating (~80%, Not 100%)
**Principle:** Use a coverage threshold as a *guide for where to add tests*, not as a north-star KPI — 100% coverage produces brittle, low-value tests.

**Do:**
- Use `go test ./... -coverprofile=coverage.out` to produce a profile.
- Gate merges on `awk '{print ((int($$3) > 80) != 1) }'` — i.e., fail when total < 80%.
- Generate `cover.xhtml` and upload as a pipeline artifact; let engineers visually see what's red.
- Mention a "testing day" quarterly — the team spends a session adding tests in red areas.

```makefile
test:
	go test ./... -coverprofile=coverage.out
coverage:
	go tool cover -func coverage.out | grep "total:" | \
	awk '{print ((int($$3) > 80) != 1) }'
report:
	go tool cover -html=coverage.out -o cover.xhtml
```
**Don't:**
- Use 100% as a target — Alan Perlis's warning about "well-intentioned" targets producing unmaintanable tests applies here.
- Skip uploading the HTML report; a coverage threshold without a visible artifact produces finger-pointing, not improvements.

*Ref: Shipping_Go.md — "Listing 3.22 Makefile" / "3.7 Code coverage"*

---

### 20. Coverage Reports as Pipeline Artifacts
**Principle:** Coverage reports must travel with the build; humans read them after every green check to find the next testing focus.

**Do:**
- Emit `cover.xhtml` to `reports/cover.xhtml` and `actions/upload-artifact`.
- Add `.gitignore` entries for `coverage.out` and `cover.xhtml` — generated artifacts do not belong in version control.
- Optionally publish results to a dashboard or Slack via post-processing.

*Ref: Shipping_Go.md — "Listing 3.23 pipeline.yml" (Generate Report step) / "3.7 Code coverage"*

---

### 21. Delivery vs Deployment (Definitions Matter)
**Principle:** Delivery is producing an artifact (binary, container) for *someone to use*; deployment is *running* that artifact as a service. Not all products deploy (libraries do not), but all should deliver.

**Do:**
- Default to "deliver to GitHub Releases" first — even before any cloud deployment exists, customers can download and run your binary.
- Use `prerelease: true` and `draft: true` on early releases so customers see them only when you're ready.
- Distinguish the two in PR conversations and design docs so engineers don't conflate them.

```yaml
- name: Create Release
  id: create_release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: ${{ github.ref }}
    release_name: Release ${{ github.ref }}
    body: |
      Still in experimentation phase
    draft: true
    prerelease: true
```
**Don't:**
- Skip delivery because "we deploy directly to FaaS" — releases are the audit trail of what reached customers.
- Tag a release as both *draft* and *prerelease* in production; choose one based on actual stability.

*Ref: Shipping_Go.md — "Listing 4.1 pipeline.yml" / "4.1 Delivery"*

---

### 22. Developers as Operators (DevOps Origin Story)
**Principle:** Closing the development/operations gap requires engineers to ship and run, and operators to read code — that's the NASA / Gene Kranz insight that birthed DevOps.

**Do:**
- Have developers own deploys end-to-end; operations consults on tooling and on-call coverage.
- Treat ops handoff as a "wait a week for the deployment window" failure mode — automate it away.
- Use a *service account* for pipeline deployments; never store personal cloud credentials.
**Don't:**
- Treat QA-bugs-dev-bugs-ops-handoff as a normal flow — the victim is the *customer*, not the team.
- Confuse DevOps with "ops has Jenkins" — DevOps is the *blend*, not the abbreviation.

*Ref: Shipping_Go.md — "4.2 Developers as operators" — Gene Kranz / Apollo 13 anecdote*

---

### 23. MVP Mindset (Ship the Minimum, Iterate in Public)
**Principle:** Ship the smallest thing that demonstrates the hypothesis; use customer feedback to design the next iteration.

**Do:**
- Measure success by days-from-idea-to-feedback, not by lines of code.
- Treat early releases as experiments (drafts, pre-releases) that *earn* the right to be called stable.
- Get a UI team integrated against the running binary *before* the API is feature-complete — they discover contract bugs early.
**Don't:**
- Wait for "stable" before exposing customers — "stable" is the enemy of "real".
- Let MVP scope creep into "we'll add it now while we're here" — feature scope is the next PR, not this one.

*Ref: Shipping_Go.md — "4.2 Developers as operators" — "MVP" / Figure 4.6*

---

### 24. Service Accounts & Least Privilege (Cloud Deployment Identity)
**Principle:** Deployments use a dedicated service account with scoped IAM roles — never your personal credentials, and never full project admin.

**Do:**
- Create a service account per product (not per project); name it `hello-api-deployer` or similar.
- Grant only the roles the deployer needs: App Engine admin + deployer, Cloud Build editor, Cloud Functions admin + developer, Storage admin.
- Persist the JSON key as a *GitHub Secret* (`GCP_CREDENTIALS`); let CI consume it, never developers.
**Don't:**
- Use your own user account for CI; revoking your access kills the pipeline.
- Grant `roles/owner` to the service account — least privilege is the principle of least surprise.

*Ref: Shipping_Go.md — "4.3 Setting up a deployment account" / Figure 4.4 (per-product roles)*

---

### 25. The "*aaS" Spectrum (FaaS → PaaS → CaaS → IaaS)
**Principle:** Choose the lowest abstraction you can afford — abstraction costs money and hides capability; each step down the ladder trades cost for control.

**Do:**
- Default to FaaS for any "version 1" of a service — cheap and zero idle cost.
- Move to PaaS when you want a long-running process with a `/health` endpoint.
- Move to CaaS / Kubernetes when the cloud bill exceeds the cost of running the orchestration yourself.
- Compare apples-to-apples: FaaS costs more per request; CaaS costs less per request but adds maintenance.
**Don't:**
- Pick by fashion; pick by stage. Each tier supports a different *organizational maturity*, not a different workload.
- Skip stages entirely — graduating from PaaS straight to bare IaaS is the textbook "over-engineered startup" anti-pattern.

*Ref: Shipping_Go.md — "4.4 As you like it" — Table 4.1*

| Tier | Service | Products |
|---|---|---|
| IaaS | Infrastructure as a Service | AWS EC2, Google Compute |
| CaaS | Container as a Service | AWS ECS, Google Cloud Run |
| PaaS | Platform as a Service | Heroku, Google App Engine, AWS Elastic Beanstalk |
| FaaS | Function as a Service | AWS Lambda, Google Cloud Functions |

---

### 26. FaaS Deployment (Google Cloud Functions as Go Binary)
**Principle:** FaaS needs a proxy function in the *root* package — subpackages are not entry points on Google Cloud Functions for Go.

**Do:**
- Create `faas.go` at the package root that re-exports your handler:

```go
package faas
import (
    "net/http"
    "github.com/holmes89/hello-api/handlers/rest"
)
func Translate(w http.ResponseWriter, r *http.Request) {
    rest.TranslateHandler(w, r)
}
```
- Use `google-github-actions/deploy-cloud-functions@main` with `runtime: go116`, `entry_point: Translate`, `name: translate`.
- Validate with `curl "${{ steps.deploy.outputs.url }}/hello"` immediately after deploy.
- Grant `allUsers` the `Cloud Function Invoker` role only after you've confirmed the response shape.

**Don't:**
- Try to deploy an `http.Handler` from a subpackage — Cloud Functions won't find the entry point.
- Skip the smoke `curl` — every FaaS deploy must self-verify before merge.

*Ref: Shipping_Go.md — "Listing 4.2 / Listing 4.3 pipeline.yml" / "4.5 Function as a Service (FaaS)"*

---

### 27. PaaS Deployment (Google App Engine with `app.yaml`)
**Principle:** PaaS apps are configured declaratively via a small YAML — runtime version, main entry, and the liveness/readiness checks map directly from `/health`.

**Do:**
- Specify `runtime: go116`, `main: ./cmd`, and explicit liveness + readiness probes pointing at `/health`.
- Set liveness `check_interval_sec` higher than readiness — readiness gets queried more often because it's on the request path.

```yaml
runtime: go116
main: ./cmd
liveness_check:
  path: "/health"
  check_interval_sec: 30
  timeout_sec: 4
  failure_threshold: 2
  success_threshold: 2
readiness_check:
  path: "/health"
  check_interval_sec: 5
  timeout_sec: 4
  failure_threshold: 2
  success_threshold: 2
app_start_timeout_sec: 300
```
**Don't:**
- Skip `app_start_timeout_sec` — cold-start Go binaries may take a few minutes the first time.
- Forget the `/health` route — without it PaaS can't decide whether to restart or route traffic.

*Ref: Shipping_Go.md — "Listing 4.8 app.yaml" / "4.6 Platform as a Service"*

---

### 28. Health Check Endpoints (Sentinel Routes)
**Principle:** Every long-running service must expose `/health` returning `{"status":"up"}` — platforms and orchestrators will use it to decide restarts, drains, and traffic.

**Do:**
- Return JSON with content-type `application/json; charset=utf-8`.
- Initialize the handler with a minimal `map[string]string{"status":"up"}` for v1; expand later with dependency checks (DB, cache).

```go
func HealthCheck(w http.ResponseWriter, r *http.Request) {
    enc := json.NewEncoder(w)
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    resp := map[string]string{"status": "up"}
    if err := enc.Encode(resp); err != nil {
        panic("unable to encode response")
    }
}
```
**Don't:**
- Return 200 unless all dependencies are healthy — readiness ≠ liveness.
- Skip on FaaS (functions are short-lived by nature); add it on every long-running binary.

*Ref: Shipping_Go.md — "Listing 4.6 health.go" / "4.6 Platform as a Service"*

---

### 29. PaaS Deployment (`app.yaml` Schema Notes)
**Principle:** `app.yaml` is the contract with the platform — get the structure right and your service is "magic-deployed"; get it wrong and you're debugging platform behavior.

**Do:**
- Keep `runtime` pinned (e.g. `go116`) — runtime drift across deploys is a class of bugs you don't want.
- Use the *lowest* `failure_threshold` your service can tolerate; aggressive restarts catch real issues quickly.
- Wire `readiness_check` to `/health` so traffic only routes to a started app — partial readiness still drains old replicas.
**Don't:**
- Combine liveness and readiness into one — they're different signals (running vs. ready) and deserve different thresholds.

*Ref: Shipping_Go.md — "Listing 4.8 app.yaml"*

---

### 30. GitHub Releases as the First Delivery Mechanism
**Principle:** A binary attached to a GitHub Release is the *simplest* delivery target — no cloud account, no cluster, just a downloadable file.

**Do:**
- Use `actions/create-release@v1` + `actions/upload-release-asset@v1` to attach binaries to a tag.
- Set `asset_content_type: application/octet-stream` so browsers don't try to render the binary.
- Use `${{ github.ref }}` for `tag_name` so the release tag matches the Git ref that triggered the build.

```yaml
- name: Upload Release Binary
  uses: actions/upload-release-asset@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    upload_url: ${{ steps.create_release.outputs.upload_url }}
    asset_path: api
    asset_name: api
    asset_content_type: application/octet-stream
```
**Don't:**
- Skip the `GITHUB_TOKEN` env — without it the action can't authenticate.
- Forget `draft: true` while you're still iterating — undraft the release only when ready for customers.

*Ref: Shipping_Go.md — "Listing 4.1 pipeline.yml" / "4.1 Delivery"*

---

### 31. Pull Requests & Branch Protection (Code as Inbound Shipment)
**Principle:** A pull request is the *warehouse receiving desk* — someone signs for the shipment, and if boxes are broken, there's a trail.

**Do:**
- Enable branch protection on `main`: require 1 approval + passing CI checks before merge.
- Require status checks to pass before merging — branch protection without check gating is purely cosmetic.
- Make yourself a PR even when working solo — self-review catches bugs the original draft missed.
**Don't:**
- Allow direct commits to `main` for any developer, including yourself.
- Treat PRs as bureaucratic overhead — they're accountability and education in one.

*Ref: Shipping_Go.md — "5.1 Reviewing code" / Figure 5.1 (GitHub branch-protection UI)*

---

### 32. The Five Ks of Code Review (Quality Bar)
**Principle:** PRs should be **Small**, **Open-minded**, **Moving**, **Interesting**, and **Standardized** — the Five Ks turn reviews into a force multiplier instead of a tax.

**Do:**
- **Small:** ≤ 300 lines including tests; limit reviewer attention.
- **Open-minded:** treat reviews as philosophical discussions, not political debates — give the benefit of the doubt, take it offline when heated.
- **Moving:** review with your morning coffee; a 4-day-old review costs ~$1,600 in tied-up developer time.
- **Interesting:** try a "GIF of the PR" or "best refactor of the week" — team-building encourages participation.
- **Standardized:** use a PR template with a checklist (compiles, tests added, tests pass, docs updated).

**Don't:**
- Use reviews as a means of personal one-upmanship — Code reviews are not political.
- Treat "I'll review after I finish this feature" as acceptable — every hour of delay ties up $50 of WIP.

*Ref: Shipping_Go.md — "5.1.1 Keep it small" through "5.1.5 Keep it the same"*

---

### 33. PR Templates & Checklists
**Principle:** Standardize the *shape* of every PR so reviewers know what to look for and authors remember what to do.

**Do:**
- Store `PULL_REQUEST_TEMPLATE.md` in `.github/`.
- Require an Associated Task (issue/ticket link), a clear description, and a checklist of expected checks.

```md
### Description
Please explain the changes you made here.
### Associated Task
Please list closed, fixed, or resolved issues here with a # and the number.
### Checklist
- [ ] Code compiles correctly
- [ ] Added tests that fail without the change (if possible)
- [ ] All tests passing
- [ ] Extended the documentation
```
**Don't:**
- Allow free-form PR descriptions only — checklists catch the "I forgot to update docs" omissions.
- Add *too many* checkboxes; 4–6 items is the sweet spot before review fatigue sets in.

*Ref: Shipping_Go.md — "Listing 5.1 PULL_REQUEST_TEMPLATE.md" / "5.1.5 Keep it the same"*

---

### 34. Theory of Constraints Applied to Developers
**Principle:** In software, the developer is the bottleneck — protect their time by reducing rework (bugs), not by adding more bodies.

**Do:**
- Measure throughput as *features shipped*, not as *PRs opened* — rework (bug fixes) counts as wasted developer time, not progress.
- When constraints tighten, help the constraint — better tools, faster feedback, cleaner code standards.
- Apply Brooks's Law explicitly: adding people to a late project makes it later.
**Don't:**
- Treat "developer shortages" as a hiring problem; treat them as a *removing-waste* problem.
- Believe that a faster IDE makes code better — fast edits of bad code are still bad.

*Ref: Shipping_Go.md — "5.2 Constraints on development" — Goldratt, *I Love Lucy* chocolate factory, two-pizza rule*

---

### 35. Two-Pizza Team Rule (Communication Overhead Ceiling)
**Principle:** A team should have no more people than can be fed by two pizzas — beyond that, communication overhead dominates throughput.

**Do:**
- Split work into sub-teams that fit this size; let them own a product or layer end-to-end.
- When growth pressure hits, *carve off* a new two-pizza team with full ownership; don't keep adding to the original.
**Don't:**
- Treat "scaling the team" as the answer to delivery delays — it usually isn't.
- Allow cross-team dependencies that force larger meetings — interface ownership cuts the lines of communication.

*Ref: Shipping_Go.md — "5.2 Constraints on development" — two-pizza rule footnote*

---

### 36. `go fmt` as the First Pipeline Gate
**Principle:** Formatting is the cheapest gate — run it *first*, because a format failure is cheaper to debug than any other.

**Do:**
- Use the trick `test -z $$(go fmt ./...)` — exits non-zero if any file would change.
- Gate pipeline: format-check → lint → test → build, in order of cost.

```makefile
check-format:
	test -z $$(go fmt ./...)
```
**Don't:**
- Make format a developer-discretion step; turn it into a CI gate and add a pre-commit hook.
- Ignore whitespace-only diffs in reviews — they cascade into false-positive diffs that hide real changes.

*Ref: Shipping_Go.md — "Listing 5.3 Makefile" / "Listing 5.4 pipeline.yml" / "5.3 Standardizing our code"*

---

### 37. `go vet` in Pipeline (Static Sanity)
**Principle:** Run `go vet ./...` as a static-analysis pre-test — it catches bugs (e.g. wrong `Printf` arity) that the compiler will not.

**Do:**
- Place `vet` in its own job that fan-in to `test` so it always runs.
- Vet adds < 10 seconds to your pipeline for typical Go projects — the cost is negligible.

```yaml
vet:
  name: Check formatting
  runs-on: ubuntu-latest
  steps:
    - name: Set up Go 1.x
      uses: actions/setup-go@v2
      with:
        go-version: ^1.18
    - name: Check out code into the Go module directory
      uses: actions/checkout@v2
    - name: Vet
      run: go vet ./...
```
**Don't:**
- Skip vet because "I write clean code" — vet catches compiler-passing, runtime-broken patterns.
- Run vet after tests; vet must precede tests because cheaper-faster-finer-grained belongs upstream.

*Ref: Shipping_Go.md — "Listing 5.6 pipeline.yml" / "5.4 Static code analysis"*

---

### 38. `golangci-lint` as the Aggregate Gate
**Principle:** Use `golangci-lint` as the single entry point for many linters — one tool, one config, many checks.

**Do:**
- Pin a specific version in the Makefile (`v1.41.1` in the book's example) to avoid surprise upgrades.
- Wire it as a separate job *before* tests so a lint failure is fast feedback.

```makefile
install-lint:
	sudo curl -sSfL \
	https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh \
	| sh -s -- -b $$(go env GOPATH)/bin v1.41.1
static-check:
	golangci-lint run
```
**Don't:**
- Enable every linter — start with `gosec`, `godot`, `misspell`, `stylecheck` and grow.
- Let linter rules drift between local and CI; run `make static-check` locally too.

*Ref: Shipping_Go.md — "Listing 5.9 pipeline.yml (Makefile install-lint) / 5.4 Static code analysis"*

---

### 39. Linter Roster: gosec, godot, misspell, stylecheck
**Principle:** Choose a small, opinionated linter set that catches *categorically different* bugs — security, punctuation, spelling, comment style.

**Do:**
- `gosec` — security (hardening, weak crypto, SQL injection risks).
- `godot` — comments end in periods; package + exported functions must be commented.
- `misspell` — spelling errors in source, comments, and docs.
- `stylecheck` — `ST1*` family: comment + naming style (e.g. `ST1000` for package comment).

```yaml
linters:
  enable:
    - gosec
    - godot
    - misspell
    - stylecheck
linters-settings:
  stylecheck:
    go: "1.18"
    checks: ["all","ST1*"]
issues:
  exclude-use-default: false
output:
  format: colored-line-number
  print-issued-lines: false
  print-linter-name: true
```
**Don't:**
- Skip `godot` because it's pedantic; missing periods in package docs are real friction for new contributors.
- Leave `exclude-use-default: true` — that hides genuine bugs (`errcheck`, `deadcode`, etc.).

*Ref: Shipping_Go.md — "Listing 5.11 .golangci-lint.yml" / "5.5 Code documentation"*

---

### 40. Pre-Commit Hooks (Move Gates Closer to the Source)
**Principle:** Every check that runs in CI should also run locally via a `pre-commit` hook — moving checks toward the developer eliminates the 4-hour "CI failed" round-trip.

**Do:**
- Run `go fmt` on staged Go files and `golangci-lint run` as the pre-commit hook:

```sh
#!/bin/sh
STAGED_GO_FILES=$(git diff --cached --name-only -- '*.go')
if [[ $STAGED_GO_FILES == "" ]]; then
  echo "no go files updated"
else
  for file in $STAGED_GO_FILES; do
    go fmt $file
    git add $file
  done
fi
golang-ci run
```
- `Makefile` target `copy-hooks` installs the hook into `.git/hooks/`.
- Keep pre-commit *fast* — full tests belong in pre-push or CI, not pre-commit (don't break flow).

**Don't:**
- Run full test suites in `pre-commit`; flow is destroyed when every commit takes minutes.
- Make hooks mandatory without providing an escape hatch for emergencies; document the bypass.

*Ref: Shipping_Go.md — "Listing 5.12 pre-commit / Listing 5.13 Makefile (copy-hooks) / 5.6 Git hooks"*

---

### 41. Dependency Inversion Principle (DIP)
**Principle:** "Depend on abstractions, not concretions." — high-level modules own the interface contract; low-level modules implement it.

**Do:**
- Define the interface where it's *consumed* (the handler) not where it's implemented (the service).
- Treat concretions as swappable bricks behind the wall; the handler doesn't care which brick fills the gap.
**Don't:**
- Define interfaces in the provider package because "that's where the implementation lives" — it produces tightly-coupled designs.

*Ref: Shipping_Go.md — "6.1 Dependency inversion principle" — electrical-plug analogy*

---

### 42. Interfaces Defined at the Consumer Site
**Principle:** The package that *uses* an interface should define it — this is Go's idiomatic "consumer-defined interface" pattern.

**Do:**
- Declare `Translator` inside the handler package; the translation package implements it implicitly via duck typing.
- Allow a single implementation to satisfy *many* interfaces — interfaces are descriptive, not prescriptive.

```go
// In the handler package (consumer)
type Translator interface {
    Translate(word string, language string) string
}
```
**Don't:**
- Define a god-interface "Interface" that everything implements — interfaces should be small and atomic.

*Ref: Shipping_Go.md — "Listing 6.3 translate.go / 6.2 Defining an interface"*

---

### 43. Duck Typing in Go (Implicit Interface Satisfaction)
**Principle:** "If it walks like a duck and quacks like a duck, it must be a duck." — Go uses structural typing for interfaces; no `implements` keyword.

**Do:**
- Add methods to a struct as you normally would; the interface is satisfied automatically.
- Add a compile-time check `var _ rest.Translator = &RemoteService{}` so missing methods fail the build, not runtime.
**Don't:**
- Try to express the relationship in the type system — Go's design says you don't need to.

*Ref: Shipping_Go.md — "Listing 6.12 remote_translator.go / 6.2 Defining an interface"*

---

### 44. Interface Segregation (Small Interfaces Compose Large Ones)
**Principle:** Interfaces should be small (one method) and composable — Go's `io.Reader`, `io.Writer`, `io.ReadWriter` is the canonical example.

**Do:**
- One method per interface; build larger interfaces by composition.
- A consumer should be able to depend on the *smallest* interface it needs — like a Lego block.

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface {
    Reader
    Writer
}
```
**Don't:**
- Define a five-method interface in a domain package — consumers will mock-out methods they don't use, producing fragile tests.

*Ref: Shipping_Go.md — "Listing 6.4 io.go / 6.2 Defining an interface"*

---

### 45. Dependency Injection via Constructor Functions
**Principle:** Dependencies come in through constructor functions; the `main()` wires concretions while consumers receive abstractions.

**Do:**
- Use `NewTranslateHandler(service Translator) *TranslateHandler` constructors that fail loudly if missing.
- Wire in `main()`: `translationService := translation.NewStaticService(); translateHandler := rest.NewTranslateHandler(translationService)`.

```go
func main() {
    mux := http.NewServeMux()
    translationService := translation.NewStaticService()
    translateHandler := rest.NewTranslateHandler(translationService)
    mux.HandleFunc("/translate/hello", translateHandler.TranslateHandler)
}
```
**Don't:**
- Reach for a DI framework (Wire, Fx, Kit) until you feel the pain — hand wiring is fine for most apps.

*Ref: Shipping_Go.md — "Listing 6.5 / Listing 6.7 main.go / 6.3 Dependency injection"*

---

### 46. Test Stubs (Cheap Placeholders for Dependencies)
**Principle:** A stub is the *minimum* struct that satisfies the dependency interface — used in tests and during feature development.

**Do:**
- Use obviously fake values (`foo`, `bar`, `baz`) so engineers reading the test know it's stubbed data.
- Allow multiple developers to stub one another's dependencies — UI hand-off starts while the real backend is being built.

```go
type stubbedService struct{}
func (s *stubbedService) Translate(word string, language string) string {
    if word == "foo" { return "bar" }
    return ""
}
```
**Don't:**
- Add logic to a stub that mirrors production behavior — that's a fake, not a stub.

*Ref: Shipping_Go.md — "Listing 6.10 translate_test.go / 6.4 Testing stubs"*

---

### 47. Testify Suites & Mocks (`suite.Suite`, `mock.Mock`)
**Principle:** Use `testify/suite` for setup/teardown; use `testify/mock` for verifying inputs and outputs on dependency calls.

**Do:**
- Embed `suite.Suite` in your suite struct; override `SetupTest` to wire deps.
- Use `client.On("Translate", "foo", "bar").Return("baz", nil)` to set expectations and `client.AssertExpectations(suite.T())` to verify.

```go
type RemoteServiceTestSuite struct {
    suite.Suite
    client   *MockHelloClient
    underTest *translation.RemoteService
}
type MockHelloClient struct { mock.Mock }
func (m *MockHelloClient) Translate(word, language string) (string, error) {
    args := m.Called(word, language)
    return args.String(0), args.Error(1)
}
```
- Use `.Times(1)` to assert a method was called exactly once (e.g. cache hit).

**Don't:**
- Skip `AssertExpectations` — a test that forgets to verify expectations passes silently.
- Mix suites with `t.Errorf` assertions — suites provide `suite.Equal`, `suite.NoError`, etc.

*Ref: Shipping_Go.md — "Listing 6.13 / Listing 6.14 / Listing 6.15 / 6.5 Mocking"*

---

### 48. Fakes (httptest.Server for External HTTP)
**Principle:** When you don't control the dependency (external API), use `httptest.NewServer` to spin up a fake that simulates responses.

**Do:**
- Combine `httptest.Server` with a `mock.Mock`-backed handler to test all HTTP outcomes (200, 404, 500, invalid JSON).
- Use `SetupSuite` (not `SetupTest`) when the server should be reused across the suite.

```go
suite.server = httptest.NewServer(mux)
suite.mockServerService = new(MockService)
...
suite.underTest = translation.NewHelloClient(suite.server.URL)
```
- Test the full HTTP contract (status codes, content-type, body shape) — that's the value fakes provide over stubs.

**Don't:**
- Hit a real external API in tests; flakiness from the network pollutes your pipeline and your data.

*Ref: Shipping_Go.md — "Listing 6.21 / Listing 6.22 / Listing 6.23 / 6.6 Fake"*

---

### 49. Stubs vs Mocks vs Fakes (Trade-off Table)

| Type | Pros | Cons |
|---|---|---|
| **Stub** | Easy to create and manipulate | Verification of interactions becomes complicated |
| **Mock** | Records interactions for later verification | More complex setup and teardown |
| **Fake** | Higher-fidelity simulated system interactions | Complicated to write and maintain |

**Do:**
- Start with stubs for trivial dependencies (in-memory key-value).
- Use mocks when you care about *what was called with what arguments*.
- Use fakes for external HTTP / IPC / databases.
**Don't:**
- Over-mock. If a test has more lines of mock setup than assertion, refactor the code.

*Ref: Shipping_Go.md — "Table 6.2 Comparing stubs, mocks, and fakes / 6.7 Just the base of the pyramid"*

---

### 50. Mocks as a Refactoring Canary
**Principle:** When mocks grow painful, your code probably needs to be broken up — mocks are a *mirror* for your design.

**Do:**
- If a test's mock setup is bigger than the test itself, extract a smaller interface or split the struct.
- If a mock needs constant updates because the interface is changing, freeze the interface; consumers shouldn't track every internal evolution.
**Don't:**
- Add mock complexity to hide the fact that a struct is doing too many things.
- Treat mock-induced friction as a Go-problem — it's a design problem.

*Ref: Shipping_Go.md — "6.7 Just the base of the pyramid" — "Mocks can become complicated ... tests can become hard to follow"*

---

### 51. Container Fundamentals (Virtualization)
**Principle:** Containers are virtualized operating systems sharing the host kernel — lightweight because they don't carry a separate kernel.

**Do:**
- Think *ISO shipping containers*: standardized dimensions mean a single image travels across laptop → CI → registry → cluster unmodified.
- Treat each layer as a security surface — fewer layers, fewer CVEs.
- Use `scratch` as base when the binary is self-contained (Go compiles statically by default).
**Don't:**
- Compare containers to VMs casually — VMs carry a kernel, containers do not; resource and isolation differ.

*Ref: Shipping_Go.md — "7.1 What is a container?"*

---

### 52. Layer-Based Images (Composition Tree)
**Principle:** Images are layers stacked: base OS → language runtime → app. Each `FROM`, `COPY`, `RUN` is a layer; fewer layers = smaller image.

**Do:**
- Order layers by *least-frequently-changed* — base OS at bottom, app code at top.
- Place `go mod download` in a separate layer from `COPY . .` so dependency cache survives across commits.
- Use multi-stage builds (`FROM golang:1.18 AS deps`) to keep the runtime image tiny.

**Don't:**
- `RUN apk add curl && curl https://... | sh && rm curl` in one RUN — that's three layers, not one.
- Use `:latest` for base images — pin to a digest or version for reproducibility.

*Ref: Shipping_Go.md — "Figure 7.3 Layers of containers / 7.3 Let's build a container"*

---

### 53. Cloud Native Buildpacks (`pack build`)
**Principle:** Buildpacks detect your language from source and produce a production-grade OCI image — no Dockerfile required.

**Do:**
- Use `pack build hello-api --builder gcr.io/buildpacks/builder:v1` for zero-config Go images.
- Detect stages: Buildpacks go through **detection** (is this a Go project?) then **building** (runtime + install + compile).

```bash
pack build gcr.io/$PROJECT/hello-api:latest \
  --builder gcr.io/buildpacks/builder:v1
```
- Try multiple builders (Heroku, Paketo, Google) — each may optimize for different runtimes.

**Don't:**
- Use Buildpacks when you need a stripped image under ~50 MB; the convenience comes with a larger footprint.

*Ref: Shipping_Go.md — "7.2 What is a Buildpack? / 7.3 Let's build a container"*

---

### 54. Dockerfile Multi-Stage Build (deps → dev → scratch)
**Principle:** Three stages: `deps` (module cache), `dev` (compile binary), `prod` (scratch + binary) — `prod` is what you ship.

**Do:**
- Copy `go.mod` and `go.sum` first, `RUN go mod download` to seed the dep cache.
- Build a *separate* dev image with `golang:1.18` for debugging; produce a *separate* prod image with `FROM scratch`.
- Use `CGO_ENABLED=0` and `GOOS=linux` for static binaries — they don't need libc.

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
**Don't:**
- Skip `CGO_ENABLED=0`; without it the scratch image will fail with "no such file or directory" on dynamic linker.
- Bundle shell or `/bin/sh` into your prod image — you will not be able to debug interactively anyway.

*Ref: Shipping_Go.md — "Listing 7.3 Dockerfile / 7.6 Writing your own image"*

---

### 55. Minimal `scratch` Images (~4.74 MB for Go)
**Principle:** Go binaries statically linked against `scratch` produce images ~25× smaller than a dev image and ~30× smaller than a Buildpack image.

**Do:**
- Compare image sizes after every Docker refactor — `docker images` is your friend.
- Trade-off: no shell, no debugger, no env vars passed via `docker run -e KEY=VAL` works the same; you must embed env defaults at build time.
- Use the `dev` target locally and the `prod` target in registry — `docker build -t hello:dev --target dev .`

*Ref: Shipping_Go.md — "7.6 Writing your own image" (size table: dev 962MB, min 4.74MB, latest 129MB)*

---

### 56. Cross-Compile Friendly Pipeline (`CGO_ENABLED=0`)
**Principle:** Compile Go to any OS/arch from any host — use `CGO_ENABLED=0` + `GOOS=linux` for scratch images.

**Do:**
- Build with a single command on Linux or macOS:
  `CGO_ENABLED=0 GOOS=linux go build -o api cmd/main.go`
- Pin the Go version in your base image to match the developer toolchain.
- Consider `GOARCH=arm64` build targets for ARM clusters (Graviton, Apple Silicon CI).

**Don't:**
- Build with `CGO_ENABLED=1` and expect to land a scratch image; the C runtime needs glibc/musl.

*Ref: Shipping_Go.md — "Listing 7.3 Dockerfile (RUN CGO_ENABLED=0 GOOS=linux go build ...)"*

---

### 57. Docker Compose & Profiles (Local Composition)
**Principle:** Compose is the local *and* CI definition for multi-container apps — one YAML drives development, integration tests, and (sometimes) production.

**Do:**
- Use `profiles` so you can run `docker-compose --profile prod up` or `--profile dev up`.
- Use `build.context: .` with `target: dev` so the dev service builds the dev image.

```yaml
version: "3.8"
services:
  api-min:
    profiles: ['prod']
    image: ghcr.io/holmes89/hello-api:min
    ports: 8080:8080
    build: .
  api-dev:
    profiles: ['dev']
    image: ghcr.io/holmes89/hello-api:dev
    ports: 8080:8080
    build:
      context: .
      target: dev
```
**Don't:**
- Mix dev and prod services in the same compose file without profiles — `docker-compose up` becomes ambiguous.
- Use compose for production orchestration — that's Kubernetes' job.

*Ref: Shipping_Go.md — "Listing 7.5 docker-compose.yml / 7.7 Local environment organization"*

---

### 58. Container Registries (GCR, GHCR, Docker Hub)
**Principle:** A registry is a *storage area* for images — push to multiple registries in your pipeline so dev teams and your cloud can both pull.

**Do:**
- Push to GCR (for GCP deployments) and GHCR (for shared distribution).
- Authenticate Docker once per pipeline: `gcloud auth configure-docker --quiet`.
- Re-tag the same image for each registry with `docker image tag`.

```yaml
- name: Push Docker image to GCP
  run: docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest
- name: Log in to the GHCR
  uses: docker/login-action@master
  with:
    registry: ${{ env.REGISTRY }}
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
- name: Tag for Github
  run: docker image tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest \
    ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```
**Don't:**
- Use `:latest` as the only tag; tag with the commit SHA and the version so rollbacks are deterministic.

*Ref: Shipping_Go.md — "Listing 7.1 pipeline.yml / 7.4 Adding a container build"*

---

### 59. Image Tagging (Latest vs Versioned)
**Principle:** `:latest` is "I don't care what version" — use it only for development. Production deployments should use version tags.

**Do:**
- Tag images on every release with the same semantic version you tag the Git commit.
- Use `git tag v0.0.1` then push `v0.0.1`; the pipeline uses `contains(github.ref, 'refs/tags/')` to switch behavior.
- Treat `:latest` as ephemeral; never roll back to `:latest`.

```yaml
containerize-buildpack:
  runs-on: ubuntu-latest
  needs: smoke-test
  if: github.event_name == 'push' && contains(github.ref, 'refs/tags/')
```
**Don't:**
- Promote `:latest` to production; use a version tag whose contents you can fingerprint.

*Ref: Shipping_Go.md — "Listing 10.6 pipeline / 10.5 Automatically deploying"*

---

### 60. Container Runtimes (Docker, Podman)
**Principle:** The container *spec* (OCI) is portable across runtimes; Docker is the most popular, Podman the rising alternative.

**Do:**
- Use Docker locally; verify your image runs on whichever runtime your cluster uses (containerd, cri-o).
- Treat `docker run hello-api` as a smoke test — if it works locally it usually works in production.
**Don't:**
- Hard-code Docker-only assumptions (`docker.sock` mounts, Compose-specific YAML) into your pipeline.

*Ref: Shipping_Go.md — "7.1 What is a container?" footnote "Docker is a common container runtime...Podman is gaining popularity"*

---

### 61. Configuration Struct & Layered Loading
**Principle:** Load configuration in priority order: defaults → JSON file → env vars → flags — the *last* writer wins.

**Do:**
- Keep `defaultConfiguration` as a package-level `var`; Load functions mutate the running instance.
- Validate every value after loading (e.g. port must be `:NNNN` and parseable as integer).

```go
var defaultConfiguration = Configuration{
    Port: ":8080",
    DefaultLanguage: "english",
}
func LoadConfiguration() Configuration {
    cfgfileFlag := flag.String("config_file", "", "load configurations from a file")
    portFlag := flag.String("port", "", "set port")
    flag.Parse()
    cfg := defaultConfiguration
    if cfgfileFlag != nil && *cfgfileFlag != "" {
        if err := cfg.LoadFromJSON(*cfgfileFlag); err != nil {
            log.Printf("unable to load configuration from json: %s, using default values", *cfgfileFlag)
        }
    }
    cfg.LoadFromEnv()
    if portFlag != nil && *portFlag != "" {
        cfg.Port = *portFlag
    }
    cfg.ParsePort()
    return cfg
}
```
**Don't:**
- Read from env vars at the point of use; centralize configuration in a struct passed explicitly — improves testability.

*Ref: Shipping_Go.md — "Listing 8.8 core.go / 8.2 Advanced configuration"*

---

### 62. Config Sources: Defaults / JSON / Env / Flags
**Principle:** Four sources, one priority — defaults are last because *something* must always load.

**Do:**
- JSON tags on the struct so `json.Unmarshal` works directly: `Port string \`json:"port"\``.
- Env var names UPPER_SNAKE_CASE; flag names lower-dash-case.

```go
func (c *Configuration) LoadFromEnv() {
    if lang := os.Getenv("DEFAULT_LANGUAGE"); lang != "" {
        c.DefaultLanguage = lang
    }
    if port := os.Getenv("PORT"); port != "" {
        c.Port = port
    }
}
```
**Don't:**
- Treat absence as an error — fall back to defaults and log a one-line warning.
- Mix config sources within the same function; each source should have its own loader.

*Ref: Shipping_Go.md — "Listing 8.5 / Listing 8.7 core.go"*

---

### 63. Port Validation & Fallback
**Principle:** Configuration values must be *validated* at load time, not at use time — fail fast with a clear log message and fall back to a known-good default.

**Do:**
- Ensure `Port` starts with `:`; fall back to `:8080` if not parseable as integer.

```go
func (c *Configuration) ParsePort() {
    if c.Port[0] != ':' {
        c.Port = ":" + c.Port
    }
    if _, err := strconv.Atoi(string(c.Port[1:])); err != nil {
        fmt.Printf("invalid port %s", c.Port)
        c.Port = defaultConfiguration.Port
    }
}
```
**Don't:**
- Panic on bad config; log + default is friendlier than a stack trace on startup.

*Ref: Shipping_Go.md — "Listing 8.6 core.go / 8.2.1 Environmental variables"*

---

### 64. Feature Flags via Dependency Injection (Car Dashboard Blanks)
**Principle:** Configuration selects which implementation of an interface the handler uses — the binary stays identical, behavior shifts.

**Do:**
- Wire `LegacyEndpoint == ""` to skip remote calls; set it to enable them. Same binary, two deployments.

```go
var translationService rest.Translator
translationService = translation.NewStaticService()
if cfg.LegacyEndpoint != "" {
    log.Printf("creating external translation client: %s", cfg.LegacyEndpoint)
    client := translation.NewHelloClient(cfg.LegacyEndpoint)
    translationService = translation.NewRemoteService(client)
}
translateHandler := rest.NewTranslateHandler(translationService)
```
**Don't:**
- Build *two* binaries; one binary with a flag covers dev, staging, prod, and the strangler migration.

*Ref: Shipping_Go.md — "Listing 8.10 main.go / 8.3 Hiding features" — car-dashboard blanks analogy*

---

### 65. Strangler Application Pattern (Gradual Replacement)
**Principle:** Build the new system *around* the old system, gradually shifting load until the old system can be decommissioned.

**Do:**
- Default to local service; override with remote service via config; add a database service that overrides both.
- Phases: V0 (in-memory), V1 (remote-call fallback), V2 (database), V3 (decommission old).
- Use feature flags per request *and* per environment to roll out safely.
**Don't:**
- Big-bang cutovers — they always blow up; use configuration to throttle risk.

*Ref: Shipping_Go.md — "9.1 Phasing out the old / Figure: strangler fig tree"*

---

### 66. `/info` Endpoint (Tag, Commit SHA, Build Date)
**Principle:** An `/info` endpoint exposes what version is running — invaluable when triaging production issues.

**Do:**
- Inject tag/hash/date at build time via `ldflags`; bake them into the binary (not env vars).

```go
var (
    tag string
    hash string
    date string
)
func Info(w http.ResponseWriter, r *http.Request) {
    enc := json.NewEncoder(w)
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    resp := map[string]string{
        "tag":  tag,
        "hash": hash,
        "date": date,
    }
    if err := enc.Encode(resp); err != nil {
        panic("unable to encode response")
    }
}
```
**Don't:**
- Read version from env vars; it should be associated *with the binary* so logs/traces align with the artifact.

*Ref: Shipping_Go.md — "Listing 8.11 info.go / 8.4 Semantic versioning"*

---

### 67. `ldflags` Build-Time Variable Injection
**Principle:** Use `-ldflags "-X package.variable=value"` to bake runtime values into the binary at compile time.

**Do:**
- Combine tag, hash, and date into a single `LDFLAGS` Makefile variable.

```makefile
TAG  := $(shell git describe --abbrev=0 --tags --always)
HASH := $(shell git rev-parse HEAD)
DATE := $(shell date +%Y-%m-%d.%H:%M:%S)
LDFLAGS := -w \
  -X github.com/holmes89/hello-api/handlers.hash=$(HASH) \
  -X github.com/holmes89/hello-api/handlers.tag=$(TAG) \
  -X github.com/holmes89/hello-api/handlers.date=$(DATE)
build:
	go build -ldflags "$(LDFLAGS)" -o api main.go
```
**Don't:**
- Use `os.Getenv` for version — env can be lost across processes, log forwarders, etc.

*Ref: Shipping_Go.md — "Listing 8.13 Makefile / 8.4 Semantic versioning"*

---

### 68. Semantic Versioning (MAJOR.MINOR.PATCH)
**Principle:** v*MAJOR*.*MINOR*.*PATCH* — major changes break, minor add features, patch fix bugs; pre-release suffixes (`-alpha`, `-e5ad2`) signal instability.

**Do:**
- Bump major when removing endpoints, changing function signatures, or reworking contracts.
- Use `-alpha`, `-beta`, `-rc1` for pre-release; partial-hash suffixes (e.g. `1.2.3-e5ad2`) for *developer builds*.
- Decide your *team's* policy explicitly; document it where contributors can find it.
**Don't:**
- Use semver as a substitute for *talking* about breaking changes; major bumps require an announcement channel too.

*Ref: Shipping_Go.md — "8.4 Semantic versioning / Figure 8.3 (iPhone software version example)"*

---

### 69. Git Tag-Driven Releases (`if contains github.ref 'refs/tags/'`)
**Principle:** Use the presence of a Git tag to switch the pipeline from "build latest" to "ship a release" — one trigger, two behaviors.

**Do:**
- Add `tags: - v*` to the workflow's `on` section.
- Gate the `deliver` job with `if: github.event_name == 'push' && contains(github.ref, 'refs/tags/')`.

```yaml
on:
  push:
    branches:
      - main
    tags:
      - v*
```
**Don't:**
- Tag and merge in the same operation; tags are *after* the merge commit you want to ship.

*Ref: Shipping_Go.md — "Listing 8.14 pipeline.yml / 8.5 Change log"*

---

### 70. Auto-Generated Changelogs (Commit Discipline Forces Good Messages)
**Principle:** Generate release notes from commit messages via a GitHub Action — this forces the team to write useful commits.

**Do:**
- Use `scottbrenner/generate-changelog-action@master` to populate the release body.
- Write commit messages a customer would read: "Fix spelling error on About Page" beats "updated text".
- Reference tickets: "Created new stub API endpoint for Issue #43".

```yaml
- name: Changelog
  uses: scottbrenner/generate-changelog-action@master
  id: Changelog
- name: Create Release
  id: create_release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: ${{ github.ref }}
    release_name: Release ${{ github.ref }}
    body: |
      ${{ steps.Changelog.outputs.changelog }}
    draft: false
    prerelease: false
```
**Don't:**
- Rely on auto-changelog to fix sloppy commits; garbage commits make garbage release notes.

*Ref: Shipping_Go.md — "Listing 8.15 pipeline.yml / 8.5 Change log"*

---

### 71. BDD vs TDD (Test Behaviors, Not Units)
**Principle:** BDD describes features from the *user's perspective*; TDD describes units from the code's perspective. They're complementary.

**Do:**
- Use BDD when "did this feature work end-to-end?" matters; TDD when "does this function work?" matters.
- Write Gherkin scenarios *before* implementation; the BDD runner is your spec-by-construction.
**Don't:**
- Use BDD for everything; Gherkin is overhead you don't need for `Add(int, int) int`.

*Ref: Shipping_Go.md — "9.2 Behavior-driven design"*

---

### 72. Gherkin Feature Files (Feature / Scenario / Given-When-Then)
**Principle:** Gherkin is a domain-specific language that lets PMs and QA write requirements that *become* tests when implemented.

**Do:**
- Write features as `Feature: <capability>` followed by multiple `Scenario: <usage>` blocks.
- Each scenario uses `Given`, `When`, `Then` — these become the test function names in Go.

```gherkin
Feature: Translation Service
  @smoke-test
  Scenario: Translation
    Given the word "hello"
    When I translate it to "german"
    Then the response should be "Hallo"

  Scenario: Translation Bulgarian
    Given the word "hello"
    When I translate it to "bulgarian"
    Then the response should be "Здравейте"
```
- Tag scenarios with `@smoke-test` or `@regression-test` for selective execution.

**Don't:**
- Mix one *huge* scenario across multiple features; keep scenarios small and atomic.
- Forget to bind a Gherkin step to a Go function (`godog run` generates a stub for missing steps).

*Ref: Shipping_Go.md — "Listing 9.2 / Listing 9.12 app.feature / 9.2 Behavior-driven design"*

---

### 73. Godog (Cucumber for Go)
**Principle:** Use `github.com/cucumber/godog` to execute Gherkin against Go test functions — the BDD runner for Go projects.

**Do:**
- Install via `go install github.com/cucumber/godog/cmd/godog@latest`.
- Wire steps via `ctx.Step(...)` and run via `godog run --tags=smoke-test`.
- Implement pending steps with `godog.ErrPending` until the actual logic exists.

```go
func InitializeScenario(ctx *godog.ScenarioContext) {
    api := &apiFeature{}
    ctx.Step(`^I translate it to "([^"]*)"$`, api.iTranslateItTo)
    ctx.Step(`^the response should be "([^"]*)"$`, api.theResponseShouldBe)
    ctx.Step(`^the word "([^"]*)"$`, api.theWord)
}
```
**Don't:**
- Couple Godog scenarios to implementation details (specific structs, JSON field names); keep them at HTTP boundaries.

*Ref: Shipping_Go.md — "Listing 9.5 / Listing 9.10 main_test.go / 9.3 Writing BDD tests"*

---

### 74. Testcontainers / `dockertest` for Integration
**Principle:** Spin up real database containers (Redis, Postgres) inside integration tests so you exercise the *actual* network protocol — not a mock.

**Do:**
- Use `dockertest.NewPool("")` to start Redis per suite; mount a production-data backup for realistic testing.
- Set `database.Expire(600)` so leaked containers don't sit forever.

```go
func InitializeTestSuite(sc *godog.TestSuiteContext) {
    sc.BeforeSuite(func() {
        pool, _ = dockertest.NewPool("")
        wd, _ := os.Getwd()
        mount := fmt.Sprintf("%s/data/:/data/", filepath.Dir(wd))
        redis, _ := pool.RunWithOptions(&dockertest.RunOptions{
            Repository: "redis",
            Mounts:     []string{mount},
        })
        redis.Expire(600)
        database = redis
    })
    sc.AfterSuite(func() { database.Close() })
}
```
**Don't:**
- Connect to a long-running shared test database — concurrent test isolation breaks immediately.
- Forget to destroy the container — CI boxes accumulate zombies.

*Ref: Shipping_Go.md — "Listing 9.15 main_test.go / 9.4 Adding a database"*

---

### 75. Smoke Tests (Fast, Before Build)
**Principle:** Smoke tests verify "does it turn on?" — they run after unit tests but before container build; they catch wiring and runtime bugs early.

**Do:**
- Tag fast, broad-coverage scenarios `@smoke-test` and run them in their own CI job.
- Gate container build on smoke test success: `needs: smoke-test`.

```yaml
smoke-test:
  name: Smoke Test Application
  needs: test
  runs-on: ubuntu-latest
  steps:
    - name: Install Godog
      run: go install github.com/cucumber/godog/cmd/godog@latest
    - name: Run Smoke Tests
      run: |
        go get ./...
        godog run --tags=smoke-test
```
**Don't:**
- Put full E2E browser suites in smoke — keep them at the API edge so they finish in < 5 min.

*Ref: Shipping_Go.md — "Listing 9.19 / 9.5 Releasing"*

---

### 76. Regression Tests (Slower, After Smoke)
**Principle:** Regression tests verify "did previously-working things break?" — they run on a different schedule and tolerate some flakiness.

**Do:**
- Tag deeper, slower scenarios `@regression-test`; run them separately.
- Treat regression failures as "investigate, don't necessarily block"; they often catch pre-existing bug exposure.

```yaml
regression-test:
  name: Regression Test Application
  needs: test
  runs-on: ubuntu-latest
  steps:
    - name: Run Smoke Tests
      run: |
        go get ./...
        godog run --tags=regression-test
```
**Don't:**
- Couple smoke and regression in one job — separating them lets failure isolation be fast.

*Ref: Shipping_Go.md — "Listing 9.21 ci.yaml / 9.5 Releasing"*

---

### 77. Feature Scenarios as Documentation
**Principle:** Gherkin feature files are *living documentation* — when the PM changes the spec, the file changes, the test changes, the binary follows.

**Do:**
- Store feature files in `cmd/features/` so they ship with the binary's tests.
- Cite the ticket number in the scenario name so the spec → code chain is auditable.
**Don't:**
- Write features the dev team never reads; treat feature files as the formal product specification.

*Ref: Shipping_Go.md — "9.3 Writing BDD tests / 9.4 Adding a database"*

---

### 78. Test Suite Setup/Teardown (BeforeSuite / AfterSuite)
**Principle:** Use `SetupSuite`/`BeforeSuite` for expensive one-time setup (containers, databases) and `SetupTest`/`Before` for per-scenario setup (HTTP servers).

**Do:**
- Spin containers in `BeforeSuite`; close them in `AfterSuite`.
- Recreate in-memory state per scenario in `ctx.Before`.

```go
ctx.Before(func(ctx context.Context, sc *godog.Scenario) (context.Context, error) {
    cfg := config.Configuration{}
    cfg.LoadFromEnv()
    cfg.DatabaseURL = "localhost"
    cfg.DatabasePort = database.Port("6379")
    mux := API(cfg)
    server := httptest.NewServer(mux)
    api.server = server
    return ctx, nil
})
```
**Don't:**
- Run container-per-test; the cost is unbearable; suite-level is the right granularity.

*Ref: Shipping_Go.md — "Listing 9.10 / Listing 9.16 main_test.go"*

---

### 79. Functional Test Types (Smoke vs Sanity vs Regression vs Usability)

| Type | Description | Question |
|---|---|---|
| **Smoke test** | Preliminary test to check for basic functionality | Does it turn on? |
| **Sanity test** | Validates high-level calculations (aggregations, math) | Is the count of items correct? |
| **Regression test** | Verifies previously reported bugs have been addressed | Did this used to work? |
| **Usability test** | Evaluates customer interactions with the product | How do people use this feature? |

**Do:**
- Run smoke before build (block release), regression after build (signal only), usability manually or quarterly.
**Don't:**
- Conflate smoke and regression — the former must always pass; the latter is a safety net.

*Ref: Shipping_Go.md — "Table 9.1 Types of functional tests / 9.5 Releasing"*

---

### 80. "Feature Complete" Definitions
**Principle:** A feature is "complete" when its Gherkin scenarios all pass — make this an explicit reporting metric.

**Do:**
- Generate a feature-completion report from Gherkin tags and Godog output.
- Track "completed scenarios / total scenarios" in dashboards.
**Don't:**
- Use "merged to main" as your definition of done — merge is the *start* of validation, not the end.

*Ref: Shipping_Go.md — "9.4 Adding a database" — "dubbed *feature complete*"*

---

### 81. Container Orchestration Concepts (Pods, Replica Sets, Deployments)
**Principle:** A *Pod* is one or more containers; a *ReplicaSet* runs N copies of a Pod; a *Deployment* manages ReplicaSets + rolling updates.

**Do:**
- Treat these as your unit of deployment; forget about "individual containers" once you're in Kubernetes.
- Let the cluster restart, scale, and load-balance for you.
**Don't:**
- Try to manage individual pods manually — Kubernetes will reconcile faster than you can.

*Ref: Shipping_Go.md — "10.3 Building blocks" — "Pods are groups of containers (a play on the Docker Whale)"*

---

### 82. Kubernetes Cluster Creation (GKE Quick-Start)
**Principle:** Use the cloud provider's managed Kubernetes (GKE, EKS, AKS) — don't manage the control plane yourself.

**Do:**
- Run `gcloud container clusters create hello-cluster --zone=us-central1-a`.
- Enable the registry, install `gke-gcloud-auth-plugin`, fetch credentials.
- Locally, use Minikube or KinD for offline development.

```bash
gcloud container clusters create \
  --zone=us-central1-a
gcloud services enable \
  containerregistry.googleapis.com container.googleapis.com
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters get-credentials hello-cluster --zone=us-central1-a
```
**Don't:**
- Run `kubernetes-the-hard-way` against production infrastructure unless you have a platform team for it.

*Ref: Shipping_Go.md — "Listing 10.1 Creating a cluster / 10.2 Your first cluster"*

---

### 83. Kubernetes Deployment Manifest
**Principle:** A Deployment is the smallest unit of release; define the container image, the replicas, and the ports.

**Do:**
- Set `imagePullPolicy: Always` for `latest`; switch to `IfNotPresent` once you pin tags.
- Pin the image to a specific version in production (`holmes89/hello-api:v0.3`).
- Use `matchLabels` consistently across Deployment, Service, and (later) Ingress.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-api
  template:
    metadata:
      labels:
        app: hello-api
    spec:
      containers:
        - name: hello-api
          imagePullPolicy: Always
          image: gcr.io/PROJECT_NAME/hello-api:latest
          ports:
            - containerPort: 8080
              name: hello-api-svc
```
**Don't:**
- Use `latest` in production manifests; pin a tag or digest.
- Forget `app: hello-api` labels — Services select on them.

*Ref: Shipping_Go.md — "Listing 10.2 deployment.yml / 10.3 Building blocks"*

---

### 84. Kubernetes Service (LoadBalancer)
**Principle:** A Service is a stable network endpoint that points at a Deployment's pods via label selectors.

**Do:**
- Use `type: LoadBalancer` to provision a cloud LB automatically.
- Keep `port` and `targetPort` separated so the LB can shift without app changes.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-api
spec:
  selector:
    app: hello-api
  type: LoadBalancer
  ports:
    - port: 80
      protocol: TCP
      targetPort: 8080
```
**Don't:**
- Use `ClusterIP` for external traffic; that's for internal services only.

*Ref: Shipping_Go.md — "Listing 10.3 service.yml / 10.3 Building blocks"*

---

### 85. Liveness & Readiness Probes (`/health`)
**Principle:** Liveness = "is the process alive?" Readiness = "can it receive traffic?" — they answer different questions and deserve different thresholds.

**Do:**
- Liveness probe: kill + restart the pod if it fails (process is wedged).
- Readiness probe: stop sending traffic if it fails (process is warming up).
- Use `/health` for both initially; differentiate when you have multi-process pods (API + cache).

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3
```
**Don't:**
- Make liveness overly aggressive (restarts on transient blips) — your service will thrash.
- Make readiness lazy — traffic queues against broken pods.

*Ref: Shipping_Go.md — "Listing 10.4 deployment.yml / 10.4 Scaling and health status"*

---

### 86. Rolling Deployments (Zero Downtime)
**Principle:** Kubernetes rolls new pods in, kills old pods after readiness succeeds — zero downtime, but only if your probes are correct.

**Do:**
- Ensure `readinessProbe` is strict enough to reject traffic until the new pod is ready.
- Bump `replicas` for capacity during the rollout (old + new overlap briefly).
**Don't:**
- Deploy without probes — Kubernetes has no signal to keep old pods running.

*Ref: Shipping_Go.md — "10.4 Scaling and health status"*

---

### 87. Helm Charts for Packaged Apps (Redis as Example)
**Principle:** Helm is the *package manager* for Kubernetes — `helm install <release> <chart>` deploys a known-good third-party manifest with your overrides.

**Do:**
- Use Bitnami/Paketo charts for production-grade stateful services like Redis.
- Pass secrets via `--set password=$(openssl rand ...)` to keep secrets out of git.

```makefile
install-redis:
	helm install redis-cluster bitnami/redis \
	  --set password=$$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '')
deploy:
	kubectl apply -f k8s
```
**Don't:**
- Hand-write a Redis StatefulSet — the chart exists, is hardened, and battle-tested.

*Ref: Shipping_Go.md — "Listing 10.7 Makefile / 10.6 Deploying Redis using Helm"*

---

### 88. Helm-Generated Secrets (`redis-password`)
**Principle:** When Helm deploys Redis, it creates a Secret named after the release — reference it from your deployment's env vars.

**Do:**
- Reference the secret by Helm release name (`name: redis-cluster`) and Helm-known key (`redis-password`).
- Mark the dependency `optional: false` so the pod refuses to start without it.

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      configMapKeyRef:
        name: hello-api
        key: database_url
  - name: DATABASE_PASSWORD
    valueFrom:
      secretKeyRef:
        name: redis-cluster
        key: redis-password
        optional: false
```
**Don't:**
- Bake passwords into ConfigMaps — that's the wrong primitive for sensitive values.

*Ref: Shipping_Go.md — "Listing 10.9 deployment.yml / 10.7 Updating deployment configuration"*

---

### 89. ConfigMaps for Non-Sensitive Config, Secrets for Sensitive
**Principle:** ConfigMaps for shape (`DATABASE_URL`), Secrets for substance (`DATABASE_PASSWORD`); both flow into container `env:`.

**Do:**
- Treat ConfigMaps as version-controlled (in `git`) but Secrets as not (use external secret managers like Vault).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-api
data:
  database_url: "redis-cluster"
```
- Quoting the author: K8s Secrets are "obfuscated, not encrypted" — production should use Vault, AWS Secrets Manager, or GCP Secret Manager.

**Don't:**
- Embed passwords in Helm values files stored in git; rotate them via the secret manager.

*Ref: Shipping_Go.md — "Listing 10.8 config.yml / 10.7 Updating deployment configuration" — Secrets warning*

---

### 90. Probe-Driven Self-Healing (Health, Restarts, Draining)
**Principle:** The right probe configuration lets Kubernetes *self-heal* your service: replace dead pods, drain traffic from degraded ones.

**Do:**
- Wire every long-running service with `/health` returning 200 when ready.
- Set `failure_threshold` × `periodSeconds` such that total probe failure time matches your SLA.
**Don't:**
- Treat probes as optional; without them, Kubernetes can't decide what to do.

*Ref: Shipping_Go.md — "10.4 Scaling and health status"*

---

### 91. Generative vs Bureaucratic Culture (Westrum)
**Principle:** Ron Westrum's organizational typology distinguishes three cultures; only the *generative* one produces safe, fast software delivery.

| Bureaucratic | Generative |
|---|---|
| Information may be ignored. | Information is actively sought. |
| Messengers are tolerated. | Messengers are trained. |
| Responsibilities are compartmentalized. | Responsibilities are shared. |
| Bridging between teams is allowed but discouraged. | Bridging between teams is rewarded. |
| Organization is just and merciful. | Failure causes inquiry. |
| New ideas create problems. | New ideas are encouraged. |

**Do:**
- Hold *blameless postmortems* — investigate the system, not the person.
- Reward bridging between teams (e.g., shared on-call, shared tools).
**Don't:**
- Tolerate "messengers are shot" behavior even informally — culture is what people *do*, not what's posted on the wall.

*Ref: Shipping_Go.md — "Table 8.1 Types of company cultures / 8.6 Accountability and handling failure"*

---

### 92. Toyota Production System / Andon Cord
**Principle:** Toyota gives any assembly-line worker the power to *stop the line* via the *andon cord* — failure is investigated, not assigned.

**Do:**
- Wire your pipeline so a failing build stops the team; alerts go to everyone, not just the committer.
- Stop additional work until the failing build/deploy is resolved (the *line* is paused).
- "Throw a rubber chicken" — make alerts visible, audible, or amusing so they're noticed.
**Don't:**
- Continue stacking PRs on top of a red main branch; the WIP compounds and the fix grows.

*Ref: Shipping_Go.md — "8.6 Accountability and handling failure" — Toyota andon cord anecdote*

---

### 93. OODA Loop (Observe → Orient → Decide → Act)
**Principle:** Colonel John Boyd's OODA loop is the *meta-pattern* behind the entire book: observe metrics/orient by analysis/decide on a change/act on it.

**Do:**
- Apply OODA at every level: a feature, a pipeline, a deployment, a company process.
- Treat the OODA loop itself as the artifact being improved — shorten each iteration.
**Don't:**
- Substitute a long annual planning meeting for OODA — the loop's value is in iteration speed.

*Ref: Shipping_Go.md — "11.5 The OODA loop / Figure 11.4"*

---

### 94. Startup / Acceleration / Cruising Phases
**Principle:** Software products mature through three phases — start cheap, scale deliberately, optimize for adaptability.

| Phase | Mindset | Tools |
|---|---|---|
| **Startup** | Trailblazing, mobile, temporary ("a tent") | FaaS, README, basic Makefile, simple unit tests |
| **Acceleration** | Expanding fast in the right direction | Lint + vet, interfaces + DI, containers, BDD |
| **Cruising** | Flexible, exploratory, self-healing | ConfigMaps, secrets, Kubernetes, observability |

**Do:**
- Recognize which phase you're in — the wrong tools in the wrong phase waste capital.
- Move to the next phase when *customers* feel the lag (cloud bill, deployment friction), not when *engineers* feel the lag.
**Don't:**
- Skip ahead — moving to Kubernetes from FaaS without traffic justifying it is over-engineering.

*Ref: Shipping_Go.md — "11.1 Startup / 11.2 Acceleration / 11.3 Cruising"*

---

### 95. Continuous Improvement (the *Second* CI)
**Principle:** When automation frees up time, Toyota re-invests that time in *improving the process* — not in idleness.

**Do:**
- Track delivery time, build time, response time, test run time.
- Run retrospective meetings on the *process itself* quarterly.
- Reserve slack time ("improvement days") for actual improvements.
**Don't:**
- Treat free time as "we can take more work" — it's an investment in the next bottleneck.

*Ref: Shipping_Go.md — "11.4.1 Process"*

---

### 96. Blameless Postmortems (Kent Beck "Brave")
**Principle:** Mistakes are inevitable — a "brave" team confronts them with automated tests, code standards, pair programming, and blameless retrospectives.

**Do:**
- Run a postmortem on every production incident; the artifact (a doc) is the unit of accountability.
- Treat each postmortem as an input to a *new* automated test (incident → regression test → same bug never repeats).
**Don't:**
- Attribute fault to individuals; the question is always "what in the system allowed this?".

*Ref: Shipping_Go.md — "8.6 Accountability and handling failure"*

---

### 97. Lead Time / Cycle Time / Build Time (Metrics Trio)
**Principle:** Optimize cycle time to reduce lead time; both shrink when build time, test time, and review time are measured.

**Do:**
- Measure: customer-request → delivery (lead); per-stage duration (cycle); CI build wall-clock.
- Break "speed" into the components above before optimizing — guessing is wasted investment.
**Don't:**
- Optimize the wrong node. If your slowest stage is review, faster builds don't help.

*Ref: Shipping_Go.md — "5.4 Static code analysis" — Lead time / Figure 5.3*

---

### 98. RFCs (Design Documents in `docs/`)
**Principle:** A "Request for Comments" document in the repo captures design decisions *before* implementation — preventing over-engineering and giving reviewers a target.

**Do:**
- Write a short RFC in `docs/` when introducing a new abstraction, library, or framework.
- Reference the RFC from the PR; reviewers read both side-by-side.
**Don't:**
- Treat RFCs as bureaucracy; one page is enough for most changes.

*Ref: Shipping_Go.md — "11.3 Cruising" — "RFCs allow teams to think about and discuss designs before they develop"*

---

### 99. Industrial vs Personal Projects
**Principle:** *Industrial programming* — multiple developers, multiple consumers, sustained over years — needs the chapter 2-11 machinery. *Personal projects* don't.

**Do:**
- Use the *absence* of a pipeline to justify keeping a project personal.
- Re-industrialize when the project graduates from personal to product (e.g., it gets a real user).
**Don't:**
- Apply every practice to every project — over-tooled personal projects die of friction.

*Ref: Shipping_Go.md — "5.3 Standardizing our code through format and lint checks" — footnote*

---

### 100. The Five Ws (Investigate Before Optimizing)
**Principle:** Who uses your product? What do they do? Where are they? When do they use it? Why? — These five questions decide your delivery strategy.

**Do:**
- Use the Ws to choose cloud regions (Where), deployment windows (When), feature priority (What).
- Track Ws answers over time; usage patterns evolve.
**Don't:**
- Decide deployment topology without data; cost and latency trade-offs depend on Where and When.

*Ref: Shipping_Go.md — "11.4.3 Delivering" — five Ws of investigation*

---

### 101. Kotlin / Quarkus / Maven Pipeline (Appendix A)
**Principle:** JVM languages have mature tooling (`mvnw`, `ktlint`, Quarkus native-image); pipe them through the same quality-gate stages.

**Do:**
- Use `@QuarkusTestResource(RedisTestContainer::class)` + `@QuarkusTest` for integration tests.
- Use `testcontainers` (`GenericContainer(DockerImageName.parse("redis:latest"))`) for stateful integration.
- Add `ktlint` first (format), `./mvnw clean test` next, then container build.
- Use GraalVM native compilation (`-Pnative`) for tiny container images.

```xml
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers</artifactId>
  <version>1.17.3</version>
  <scope>test</scope>
</dependency>
```
```yaml
- name: Lint
  run: ./ktlint
- name: Run Test
  run: ./mvnw clean test
```
**Don't:**
- Skip Quarkus native compilation if size matters; native images skip JVM patches.

*Ref: Shipping_Go.md — "A.4 Testing / A.5 Linting and the initial pipeline / A.6 Containerizing"*

---

### 102. Python / FastAPI / Poetry Pipeline (Appendix B)
**Principle:** Python's `pip freeze` is brittle — use `Poetry` to manage reproducible dependencies and `redislite` for in-memory Redis tests.

**Do:**
- `poetry new hello-api`; declare deps in `pyproject.toml`.
- Use FastAPI's `app.dependency_overrides[repo]` to swap the *real* repo for an in-memory fake in tests.
- Use `redislite` (in-process Redis) for unit/integration tests; no Docker needed.

```python
from fastapi import FastAPI, Depends
app = FastAPI()
repo = deps.redis_client
@app.get("/translate/{word}")
def translation(
    word: str,
    language: str = "english",
    repo: RepositoryInterface = Depends(repo),
):
    resp = repo.translate(language, word)
    return {"language": language.lower(), "translation": resp}
```
- Run lint + tests via `nox` (`nox -rs lint`, `nox -rs tests`).
- Bake `PYTHONUNBUFFERED=1` into the prod container so logs aren't trapped.

```dockerfile
FROM python:3.10.7-slim-bullseye as base
ENV PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONUNBUFFERED=1
WORKDIR /app
CMD ["uvicorn","hello_api.app:app","--port","8080","--host","0.0.0.0"]
```
**Don't:**
- Pin Python with `FROM python:latest`; pin to a minor (e.g. 3.10.7) for reproducibility.

*Ref: Shipping_Go.md — "B.1 Poetry / B.2 Coding / B.3 Testing / B.5 Defining the container"*

---

### 103. JavaScript / Express / NPM Pipeline (Appendix C)
**Principle:** Use `package.json` for both deps *and* scripts; integrate `Jest` + `testcontainers` for real Redis integration tests.

**Do:**
- Add scripts: `test`, `format`, `check-format`, `lint` to `package.json`.
- Use `jest` + `supertest` for HTTP integration tests.
- Use `testcontainers.GenericContainer('redis').withExposedPorts(6379)` and `testcontainers.withCopyFileToContainer('./data/dump.rdb', '/data/dump.rdb')` for realistic data.
- `npm ci --only=production` (not `npm install`) in the Dockerfile — uses lockfile, deterministic.

```json
"scripts": {
  "test": "jest --config jest.config.js",
  "start": "node ./bin/www",
  "format": "prettier --single-quote --write --use-tabs .",
  "check-format": "prettier --single-quote --use-tabs --check .",
  "lint": "eslint \"**/*.js\" --max-warnings 0 --ignore-pattern node_modules/"
}
```
**Don't:**
- `npm install` in a Dockerfile; use `npm ci` for reproducible installs.

*Ref: Shipping_Go.md — "C.1 NPM / C.3 Testing / C.5 Defining the container"*

---

### 104. Terraform / Packer / IaC Pipeline (Appendix D)
**Principle:** For teams that prefer bare VMs over Kubernetes, Packer (image builds) + Terraform (state management) is the mature path.

**Do:**
- Use Packer to bake your binary into a VM image tagged with the Git SHA: `image_name = "hello-api-${var.git_sha}"`.
- Store Terraform state in a GCS bucket with versioning — never on a laptop.
- Grant the service account `compute.instanceAdmin.v1`, `iam.serviceAccountUser`, `iap.tunnelResourceAccessor` — not `owner`.

```hcl
variable "project_id" { type = string }
variable "git_sha" { type = string; default = "UNKNOWN" }
source "googlecompute" "hello-api" {
  project_id          = var.project_id
  source_image_family = "ubuntu-2204-lts"
  image_name          = "hello-api-${var.git_sha}"
  ssh_username        = "packer"
  zone                = "us-central1-a"
}
```
```hcl
terraform {
  backend "gcs" {
    bucket = "hello-api-bucket-tfstate"
    prefix = "terraform/state"
  }
}
resource "google_compute_instance" "hello_api" {
  name         = "hello-api"
  machine_type = "f1-micro"
  zone         = "us-east1-a"
  boot_disk {
    initialize_params { image = var.image_name }
  }
  lifecycle { create_before_destroy = true }
  metadata_startup_script = "sudo chmod +x /home/ubuntu/hello-api && sudo /home/ubuntu/hello-api"
}
```
**Don't:**
- Hand-edit state files; use `terraform apply -auto-approve` in CI only.

*Ref: Shipping_Go.md — "D.1 Building the image / D.2 Deploying the image / D.3 Creating the pipeline"*

---

### 105. Lockfile Hygiene & Reproducible Builds
**Principle:** Lock dependency versions; commit `package-lock.json`, `poetry.lock`, `go.sum`; treat CI as a *function of source + lockfile*.

**Do:**
- `go.sum` automatically pins Go modules; commit it always.
- `package-lock.json` for npm — runs `npm ci` not `npm install` in CI.
- `poetry.lock` for Python; commit it; use `poetry install --no-dev` in production.
**Don't:**
- `--no-dev` install in dev environments; in production, yes.
- `^` ranges in lockfiles drift across environments; pin in production manifests.

*Ref: Shipping_Go.md — "B.1 Poetry / C.1 NPM"*

---

### 106. Cross-Language Pipeline Pattern (Stages Always Stay the Same)
**Principle:** Every pipeline in this book has the same shape — *lint → test → build → container → deploy* — regardless of language.

**Do:**
- Reproduce the chapter-by-chapter pipeline when adopting a new language: lint tool, test runner, build command, container build, deploy.
- Don't add steps that aren't from this list (security scans, signing, SBOM) until the basics are stable.
**Don't:**
- Skip lint on JVM or Node projects because "the compiler enforces it" — lints catch *style*, compiler catches *correctness*; both are necessary.

*Ref: Shipping_Go.md — "Appendices A-D" cross-reference*

---

### 107. Containerization for Scripts vs Compiled Binaries
**Principle:** Compiled binaries (Go, Quarkus native) need only a small base; scripts (Python, Node) need their full runtime in the image.

**Do:**
- Go: `FROM scratch` (4.74 MB); CGO_ENABLED=0; embed env defaults via ldflags.
- Kotlin/Quarkus: use Maven Quarkus `Dockerfile.jvm` or native-image for minimal images.
- Python: `python:3.10.7-slim-bullseye` + `PYTHONUNBUFFERED=1` + `poetry install`.
- Node: `FROM node:17` + `npm ci --only=production` + `NODE_ENV production`.

**Don't:**
- Use full OS bases (Ubuntu) for any of these — slim variants exist for every runtime.

*Ref: Shipping_Go.md — "A.6 Containerizing / B.5 Defining the container / C.5 Defining the container"*

---

### 108. Pipeline Lockfile Pinning Across Languages
**Principle:** Each language's tooling uses a "lockfile" — pin its versions in the same way across the stack.

**Do:**
- `package.json` versions (`^` for libs, exact for tooling), `package-lock.json` committed.
- `pyproject.toml` with `poetry.lock` committed; pin `poetry` version in Dockerfile.
- `pom.xml` versions with the Maven Wrapper (`./mvnw`) — no global Maven.
- `go.mod` with `go.sum` checked in.

**Don't:**
- Touch a lockfile manually; let the tool regenerate it.

*Ref: Shipping_Go.md — entire Appendix approach*

---

## Anti-Patterns & Common Mistakes

- **`main()` with business logic:** unwrappable, untestable. *Fix:* factor service/handler/server from `cmd/main.go`.
- **100% coverage gate:** produces mock-driven, brittle tests. *Fix:* ~80% gate + visible HTML report.
- **Interface defined in the provider package:** forces consumers to depend on details. *Fix:* define interfaces where they're consumed.
- **`docker run -it bash` to debug a `scratch` image:** there's no shell. *Fix:* ship a `dev` target with `golang:1.18` for debugging.
- **`:latest` in production manifests:** makes roll-back impossible. *Fix:* pin tags in `deployment.yml`.
- **Personal cloud credentials in CI:** you become a single point of failure. *Fix:* service account + GitHub Secret.
- **Big-bang cutover from old system:** every migration burns. *Fix:* strangler application with feature-flagged wiring.
- **Migrating to Kubernetes because "it's modern":** cost & ops aren't free. *Fix:* wait for the cloud-bill spike.
- **Treating PR review backlog as status:** every delayed review ties up WIP dollars. *Fix:* review with morning coffee; merge before EOD.
- **Pre-commit hooks that run the world:** flow dies; developers `git commit --no-verify` their way around them. *Fix:* pre-commit = format + lint; full tests in CI.
- **Quarkus/Kotlin's `@QuarkusTest` without `QuarkusTestResource`:** tests run against the production app, not the test container. *Fix:* always declare a test resource.
- **Mocking the entire database:** test maintenance cost exceeds the value. *Fix:* use `dockertest` / `testcontainers` for real databases in integration tests.
- **Forgetting `gcloud auth configure-docker`:** `docker push` to GCR silently fails. *Fix:* make it a pipeline step.

---

## Decision Heuristics / Checklists

### "Should I add a new pipeline stage?"
- Is it cheaper than the tests below it? → Place it upstream.
- Does it catch a *different* class of bug than existing stages? → Add it.
- Does it run in < 60 seconds locally? → Make it a pre-commit hook.
- Else → leave it as a CI job.

### "Should I move from FaaS to PaaS?"
- Are you running a *long-lived* process (e.g., websockets, scheduled jobs)? → PaaS.
- Are you paying more in FaaS than the equivalent VM? → PaaS or CaaS.
- Else → stay on FaaS.

### "Should I move to Kubernetes?"
- Are you hitting cloud-bill thresholds your finance team calls out? → Yes.
- Do you have headcount to manage nodes, upgrades, RBAC? → Yes.
- Else → containerize without orchestrating (Cloud Run, ECS, Fargate).

### "Should I use a mock, stub, or fake?"
- Does it need to verify *call arguments*? → **Mock**.
- Is the dependency *in-process, trivial*? → **Stub**.
- Does it need real network/protocol behavior? → **Fake** (httptest / testcontainers).

### "Should I add a pre-commit hook?"
- Is the check < 1 second? Yes → hook.
- Is it deterministically fast for every commit? Yes → hook.
- Otherwise → CI job.

### "Should I add tests for a function?"
- Is it pure (no I/O)? Yes → unit test, table-driven.
- Does it call an external service? Yes → integration test (testcontainers).
- Does it depend on time, randomness, or the file system? Yes → inject a clock/seed/path.

### "TDD or BDD?"
- TDD for units (function-level).
- BDD for features that cross code layers or have user-visible behavior.

### "How often should I bump semver?"
- Patch: bug fixes with no contract change.
- Minor: new features, no breaking changes.
- Major: any breaking change to an exposed API.

---

## Key Takeaways

1. **Build the conveyor belt first.** Pipeline precedes product. README + Makefile + `.github/workflows/pipeline.yml` + `.gitignore` on day one; the first HTTP handler is the *proof*, not the *purpose*.
2. **Small, iterative work beats large batches.** ≤300-line PRs, ≤10-min stage budget, ≤5-min integration feedback. WIP is tied-up money; shrink it.
3. **Tests are a spectrum.** Unit (broad base) → integration (testcontainers, dockertest) → BDD (Godog/Gherkin) → E2E (Selenium/Cypress). Start with the base; grow upward.
4. **Depend on abstractions.** Consumer-defined interfaces, duck typing, dependency injection. Mocks are a *mirror* of design — if they hurt, refactor.
5. **Configuration enables hidden features.** Flags + DI = strangler applications, zero-downtime migrations, and one binary across dev/staging/prod.
6. **Quality gates are fast-and-early.** `go fmt` → `go vet` → `golangci-lint` → unit tests → smoke tests → build → deploy. Each catches a different bug class.
7. **Containers provide universal portability.** Buildpacks for turnkey; multi-stage Dockerfile for minimal (`scratch` = 4.74 MB for Go). Docker Compose for local multi-container apps.
8. **Start cheap, scale when needed.** FaaS → PaaS → CaaS → IaaS. Each step reduces abstraction, adds control, and (eventually) reduces cost.
9. **Culture matters as much as code.** Generative organizations (Westrum) investigate failure; bureaucratic ones assign blame. Andon-cord alerts, blameless retros, visible build status.
10. **It is a loop, not a line.** OODA at every level — features, pipelines, deployment topology, company strategy. Products don't "finish"; they evolve through continuous feedback.

---

## Cross-References
- Related: `Continuous_Deployment.md`, `How_To_Continuous_Integration.md`, `Building_Modern_CLI_Applications_in_Go.md`, `Terraform_at_Scale_Early_Release.md`, `Infrastructure_as_Code_3rd_Ed_-_Kief_Morris.md`, `Crafting_Engineering_Strategy_-_Will_Larson.md`.
- Topic index: `INDEX.md`
