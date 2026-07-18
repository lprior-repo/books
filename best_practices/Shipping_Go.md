# Shipping Go
**Author:** Joel Holmes
**Topic tags:** `#concurrency` `#testing` `#cli` `#systems` `#api` `#general`
**Language focus:** Go-first
**Sources:** `markdown_output/Shipping_Go_-_Joel_Holmes/Shipping_Go_-_Joel_Holmes.md` · `summaries/Shipping_Go_-_Joel_Holmes.md`

## TL;DR
*Shipping Go* is a delivery-engineering book wrapped in a Go tutorial: every chapter grows a real HTTP service while progressively adding CI/CD, testing discipline, mocking, containerization, semantic versioning, configuration, BDD integration tests, and Kubernetes. The book is Go-first but explicitly language-agnostic — the appendices repeat the pipeline in Kotlin, Python, and JavaScript, and a Terraform appendix covers the IaaS alternative. Apply its practices whenever you ship a service: small slices, pipeline before code, format/lint/test gates, interfaces early, feature flags, tag-driven releases, smoke + regression tiers, and "FaaS → PaaS → CaaS → K8s" only when metrics justify it.

---

## Best Practices by Topic

### Build the Pipeline Before the Code

**Principle:** Establish CI/CD as a foundational artifact, not a retrofit. "Build the pipeline before writing application code" — process should be agnostic to the product.

**Do:**
- Create README.md with thesis, dependencies (pinned), setup steps (intentionally left blank as a reminder), and release milestones (V0 / V1 / V2).
- Use a Makefile as the single source of build commands shared by developers and CI.
- Put product code, test code, and infrastructure definitions in the same repository.

**Don't:**
- Don't hand-author CI commands that diverge from local commands.

**Code:**
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
	go build -ldflags "$(LDFLAGS)" -o api main.go
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 2.2 Makefile / Listing 2.5 .gitignore"*

---

### GitHub Actions: First Pipeline Before First Code

**Principle:** A CI pipeline is a moving assembly line: tools grouped by order of operation, flow optimised, automation moves the product. The pipeline runs the same `make` commands developers run locally.

**Code:**
```yaml
name: CI Checks
on:
  push:
    branches:
    - main
jobs:
  build:
    name: Build App
    runs-on: ubuntu-latest            # Linux-based CI image
    steps:
    - name: Set up Go 1.x
      uses: actions/setup-go@v2
      with:
        go-version: ^1.18
    - name: Check out code into the Go module directory
      uses: actions/checkout@v2
    - name: Build
      run: make build                  # Same command dev uses
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 2.4 pipeline.yml"*

---

### Branch Protection and Quality Gates

**Principle:** Protect `main` from direct commits. Require reviews + passing checks. Checks should run in dependency order from cheapest to most expensive.

**Do:**
- Enable branch protection: one review + required checks.
- Order gates: format check → lint → test → build → deploy.
- Run CI on `pull_request` to main, run deploys only on `push` to main.

**Code:**
```yaml
name: CI Checks
on:
  pull_request:                       # Also runs on PRs
    branches:
    - main
  push:
    branches:
    - main
jobs:
  deploy-function:
    needs: test
    if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
    # ↑ deploys only on push, never on PRs
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 5.2 pipeline.yml / Setting up branch protection in GitHub Repo"*

---

### Layered Configuration (Defaults → JSON → Env → Flags)

**Principle:** Load configuration in priority order so a developer can override anything locally while production uses environment variables injected by the platform.

**Code:**
```go
type Configuration struct {
    Port            string `json:"port"`
    DefaultLanguage string `json:"default_language"`
    LegacyEndpoint  string `json:"legacy_endpoint"`
    DatabaseType    string `json:"database_type"`
    DatabaseURL     string `json:"database_url"`
}

var defaultConfiguration = Configuration{
    Port:            ":8080",
    DefaultLanguage: "english",
}

func (c *Configuration) LoadFromEnv() {
    if lang := os.Getenv("DEFAULT_LANGUAGE"); lang != "" {
        c.DefaultLanguage = lang
    }
    if port := os.Getenv("PORT"); port != "" {
        c.Port = port
    }
}

func LoadConfiguration() Configuration {
    cfgfileFlag := flag.String("config_file", "", "load configurations from a file")
    portFlag    := flag.String("port", "", "set port")
    flag.Parse()
    cfg := defaultConfiguration                   // 1. defaults
    if cfgfileFlag != nil && *cfgfileFlag != "" {
        if err := cfg.LoadFromJSON(*cfgfileFlag); err != nil { /* log */ } // 2. file
    }
    cfg.LoadFromEnv()                            // 3. env vars
    if portFlag != nil && *portFlag != "" {
        cfg.Port = *portFlag                     // 4. flags
    }
    cfg.ParsePort()                              // validate
    return cfg
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 8.3 / 8.4 / 8.5 / 8.7 / 8.8"*

Precedence demo:
```
$ go run cmd/main.go --config_file config.json
listening on :8079                                       # file
$ PORT=8081 go run cmd/main.go --config_file config.json
listening on :8081                                       # env wins over file
$ PORT=8081 go run cmd/main.go --config_file config.json --port 8082
listening on :8082                                       # flag wins over env
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Updating the port"*

---

### Feature Flags via Configuration + Dependency Injection

**Principle:** A single binary builds all variants. Configuration flips which service is wired into the handler — like car dashboards that ship with blanks for absent options. "Same steering wheel or console can be made for all types of cars, but only specific cars will have buttons."

**Code:**
```go
func main() {
    cfg := config.LoadConfiguration()
    var translationService rest.Translator       // Interface variable
    translationService = translation.NewStaticService()   // default
    if cfg.LegacyEndpoint != "" {                // feature flag
        log.Printf("creating external translation client: %s", cfg.LegacyEndpoint)
        client := translation.NewHelloClient(cfg.LegacyEndpoint)
        translationService = translation.NewRemoteService(client)  // swap
    }
    translateHandler := rest.NewTranslateHandler(translationService)  // inject
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 8.10 main.go"*

---

### Semantic Versioning + Tag-Driven Releases

**Principle:** Use MAJOR.MINOR.PATCH (breaking.feature.fix). Tag-driven releases let you separate "always integrate" from "promote to users." Inject tag/hash/build-date into the binary via `-ldflags` so the artifact carries its provenance.

**Code:**
```makefile
TAG := $(shell git describe --abbrev=0 --tags --always)
HASH := $(shell git rev-parse HEAD)
DATE := $(shell date +%Y-%m-%d.%H:%M:%S)
LDFLAGS := -w \
  -X github.com/holmes89/hello-api/handlers.hash=$(HASH) \
  -X github.com/holmes89/hello-api/handlers.tag=$(TAG) \
  -X github.com/holmes89/hello-api/handlers.date=$(DATE)
build:
	go build -ldflags "$(LDFLAGS)" -o api main.go
```
```go
// /info handler exposes the provenance embedded in the binary
package handlers
var (
    tag  string
    hash string
    date string
)
func Info(w http.ResponseWriter, r *http.Request) {
    enc := json.NewEncoder(w)
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    enc.Encode(map[string]string{"tag": tag, "hash": hash, "date": date})
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 8.11 / 8.13 Makefile / 8.14 pipeline.yml"*

---

### PR Template as Quality Checklist

**Principle:** Standardise the PR form. The checklist is a contract, not a suggestion.

**Code:**
```markdown
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 5.1 PULL_REQUEST_TEMPLATE.md"*

---

### Review Hygiene

**Principle:** A review is "more like reading a recipe than a book." Cap reviews at 300 lines, treat them as philosophical discussions, and unblock WIP fast.

**Code:**
- 5 review rules: small (<300 LOC), open mind, keep moving (review is WIP — $50/hour sitting), keep interesting, keep standardised (templates).
- "Even while working alone ... I find myself creating pull requests for myself."

*Ref: Shipping_Go_-_Joel_Holmes.md — "5.1.1 Keep it small / 5.1.2 Keep an open mind / 5.1.3 Keep it moving"*

---

### Table-Driven Black-Box Tests

**Principle:** Arrange-Act-Assert maps 1:1 to Given-When-Then. Use anonymous-struct slices for parameterised tests so adding a case is one line. Use `<pkg>_test` packages so tests cannot see inside the package — assert behaviour, not implementation.

**Code:**
```go
package translation_test                                // Black-box: cannot see unexported
import (
    "testing"
    "github.com/holmes89/hello-api/translation"
)
func TestTranslate(t *testing.T) {
    // Arrange
    tt := []struct {
        Word        string
        Language    string
        Translation string
    }{
        {Word: "hello", Language: "english", Translation: "hello"},
        {Word: "hello", Language: "german",  Translation: "hallo"},
        {Word: "hello", Language: "finnish", Translation: "hei"},
        {Word: "hello", Language: "dutch",   Translation: ""},
    }
    for _, test := range tt {
        // Act
        res := translation.Translate(test.Word, test.Language)
        // Assert
        if res != test.Translation {
            t.Errorf(`expected "%s" to be "%s" from "%s" but received "%s"`,
                test.Word, test.Language, test.Translation, res)
        }
    }
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.7 translator_test.go"*

---

### Test-Driven Development: Red → Green → Refactor

**Principle:** Write the failing test first; implement the minimum to pass; refactor with confidence. Tests are experiments that prove a behaviour.

**Code:**
```go
package translation_test
func TestTranslate(t *testing.T) {
    // Arrange
    word := "hello"
    language := "english"
    // Act
    res := translation.Translate(word, language)
    // Assert
    if res != "hello" {
        t.Errorf(`expected "hello" but received "%s"`, res)
    }
}
// Implementation passes by returning the word, then is refactored to support more languages.
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.3 / 3.4"*

---

### Edge-Case and Input Sanitation Tests

**Principle:** Negative cases ("dutch" returns ""), edge cases (capitalisation, whitespace), and input sanitation belong in the unit test base.

**Code:**
```go
// Edge cases table:
{Word: "hello", Language: "German",  Translation: "hallo"},     // Capitalised lang
{Word: "Hello", Language: "german",  Translation: "hallo"},     // Capitalised word
{Word: "hello ", Language: "german", Translation: "hallo"},     // Trailing space

// Service-side sanitation:
func Translate(word string, language string) string {
    word     = sanitizeInput(word)
    language = sanitizeInput(language)
    if word != "hello" { return "" }
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.11 / 3.12 translator_test.go, translator.go"*

---

### The Testing Pyramid (Unit → Integration → E2E)

**Principle:** A broad unit-test base, narrower integration tests, and a thin end-to-end top. "If you have many end-to-end tests but few unit tests, failures are hard to diagnose because you must untangle the entire system."

**Code (Makefile coverage gate):**
```makefile
test:
	go test ./... -coverprofile=coverage.out
coverage:
	go tool cover -func coverage.out | grep "total:" | \
	awk '{print ((int($$3) > 80) != 1) }'
report:
	go tool cover -html=coverage.out -o cover.xhtml
# Coverage gate fails pipeline if <80%.
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.22 / 3.23 Makefile, pipeline.yml"*

**Do:**
- Enforce ~80% coverage, not 100% — "arbitrary goals lead to poorly written tests that are hard to maintain."

---

### Format Check as Fastest Gate

**Principle:** Run `go fmt`/`go vet`/`golangci-lint` *before* tests because they're faster and catch different-sized problems. Move checks as close to the developer as possible (pre-commit, local Makefile).

**Code:**
```makefile
check-format:
	test -z $$(go fmt ./...)            # Fails if any file would change
```
```yaml
format-check:
  name: Check formatting
  runs-on: ubuntu-latest
  steps:
  - uses: actions/setup-go@v2
    with: { go-version: ^1.18 }
  - uses: actions/checkout@v2
  - name: Run Format Check
    run: make check-format
test:
  needs:
  - format-check                        # Format first (cheapest)
  - lint                                # Then lint
  name: Test Application
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 5.3 Makefile / 5.4 pipeline.yml"*

---

### Pre-Commit Hook for Local Checks

**Principle:** Catching failures in the developer's editor saves reviewers and CI minutes. Install hooks from the repo so they propagate to every contributor.

**Code:**
```sh
#!/bin/sh                                    # scripts/hooks/pre-commit
STAGED_GO_FILES=$(git diff --cached --name-only -- '*.go')
if [[ $STAGED_GO_FILES == "" ]]; then
    echo "no go files updated"
else
    for file in $STAGED_GO_FILES; do
        go fmt $file
        git add $file
    done
fi
golang-ci run                               # Lint locally before push
```
```makefile
setup: install-go init-go copy-hooks
copy-hooks:
	chmod +x scripts/hooks/*
	cp -r scripts/hooks .git/.
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 5.12 / 5.13"*

---

### golangci-lint Config (gosec, godot, misspell, stylecheck)

**Principle:** Lint catches missing error checks (which can hide production bugs), undocumented exports, misspellings, and stylistic drift.

**Code:**
```yaml
# .golangci.yml
linters:
  enable:
  - gosec        # Security checks
  - godot        # Comments end with a period
  - misspell     # Spelling
  - stylecheck   # Enforce comment style
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 5.7 / 5.11 golangci.yml"*

---

### `gofmt` as Non-Negotiable Style

**Principle:** "Nobody likes Go format, everyone loves Go format." `gofmt` removes style debates; run it locally and in CI.

**Code:**
```
$ go fmt ./...
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "5.3 Standardizing our code through format and lint checks"*

---

### System Under Test (SUT) Boundaries

**Principle:** Break monoliths into testable units — service (business logic), handler (request/response), server (wiring). Test inputs and outputs, never internals.

**Code (handler test via `httptest.NewRecorder`):**
```go
package rest_test
import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/holmes89/hello-api/handlers/rest"
)
func TestTranslateAPI(t *testing.T) {
    // Arrange
    rr := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/hello", nil)
    handler := http.HandlerFunc(rest.TranslateHandler)
    // Act
    handler.ServeHTTP(rr, req)
    // Assert
    if rr.Code != http.StatusOK {
        t.Errorf(`expected status 200 but received %d`, rr.Code)
    }
    var resp rest.Resp
    json.Unmarshal(rr.Body.Bytes(), &resp)
    if resp.Translation != "hello" {
        t.Errorf(`expected Translation "hello" but received %s`, resp.Translation)
    }
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.14 translator_test.go"*

---

### Black-Box Test Package Naming

**Principle:** Use `<pkg>_test` package naming so tests cannot reach into unexported internals. Forces you to test the public surface — i.e. the interface that other code will actually depend on.

**Code:**
```go
package translation_test                          // Underscore = black-box
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 3.3 translator_test.go (❶)"*

---

### Define Interfaces Where They're Consumed

**Principle:** "Depend on abstractions, not concretions" — but in Go, define the interface in the *consumer* package (handler), not the implementer (service). Go uses duck typing: any struct with matching methods satisfies the interface implicitly.

**Code:**
```go
// handlers/rest/translate.go — interface lives here (consumer)
type Translator interface {
    Translate(word string, language string) string
}

// translation/translator.go — implements, doesn't know about the interface
type StaticService struct{}
func (s *StaticService) Translate(word, language string) string { ... }
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.3 translate.go / 6.6 translate.go"*

---

### Interface Segregation — Small Interfaces Compose

**Principle:** Tiny, composable interfaces beat fat ones. Like `io.Reader` (one method) composing into `io.ReadWriter`.

**Code:**
```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface { Reader; Writer }    // Composed
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.4 io.go"*

---

### Constructor Injection (Hand-Wired DI)

**Principle:** Inject dependencies via constructor. Wire everything in `main`. Keep wiring trivial — manual injection is fine until complexity demands Wire/Fx/Kit.

**Code:**
```go
type TranslateHandler struct {
    service Translator
}
func NewTranslateHandler(service Translator) *TranslateHandler {
    return &TranslateHandler{service: service}
}
// In main():
translationService := translation.NewStaticService()
translateHandler   := rest.NewTranslateHandler(translationService)
mux.HandleFunc("/translate/hello", translateHandler.TranslateHandler)
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.5 / 6.7 translate.go, main.go"*

---

### Interface Compile-Time Check

**Principle:** A blank-identifier assignment forces the compiler to verify the concrete type satisfies the interface. Fail at compile time, not at runtime.

**Code:**
```go
package translation
import "github.com/holmes89/hello-api/handlers/rest"
var _ rest.Translator = &RemoteService{}    // Compile-time guarantee
type RemoteService struct { client HelloClient }
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.12 remote_translator.go (❶)"*

---

### Test Doubles: Stubs, Mocks, Fakes — Pick the Right One

**Principle:** Stubs are simple placeholders for handlers. Mocks record calls for verification. Fakes stand in for *external* services (e.g. a fake HTTP server for testing a real HTTP client). "Complicated test doubles are a canary in the coal mine — your code may need to be broken up."

**Code (stub for handler tests):**
```go
type stubbedService struct{}
func (s *stubbedService) Translate(word, language string) string {
    if word == "foo" { return "bar" }            // obviously fake values
    return ""
}
// Use: rest.NewTranslateHandler(&stubbedService{})
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.10 translate_test.go"*

**Code (testify mock that asserts input + return + call count):**
```go
type MockHelloClient struct { mock.Mock }
func (m *MockHelloClient) Translate(word, language string) (string, error) {
    args := m.Called(word, language)
    return args.String(0), args.Error(1)
}
// Usage:
suite.client.On("Translate", "foo", "bar").Return("baz", nil)
res := suite.underTest.Translate("foo", "bar")
suite.client.AssertExpectations(suite.T())
// Cache test — call once, expected once:
suite.client.On("Translate", "foo", "bar").Return("baz", nil).Times(1)
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.13 / 6.14 / 6.19 remote_translator_test.go"*

**Code (testify suite setup/teardown):**
```go
type RemoteServiceTestSuite struct {
    suite.Suite
    client    *MockHelloClient
    underTest *translation.RemoteService
}
func (suite *RemoteServiceTestSuite) SetupTest() {  // runs before every test
    suite.client = new(MockHelloClient)
    suite.underTest = translation.NewRemoteService(suite.client)
}
func TestRemoteServiceTestSuite(t *testing.T) {
    suite.Run(t, new(RemoteServiceTestSuite))
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.13"*

**Code (fake HTTP server for testing an HTTP client):**
```go
func (suite *HelloClientSuite) SetupSuite() {
    suite.mockServerService = new(MockService)
    handler := func(w http.ResponseWriter, r *http.Request) {
        b, _ := ioutil.ReadAll(r.Body); defer r.Body.Close()
        var m map[string]interface{}
        _ = json.Unmarshal(b, &m)
        word := m["word"].(string); language := m["language"].(string)
        resp, err := suite.mockServerService.Translate(word, language)
        if err != nil { http.Error(w, "error", 500) }
        if resp == "" { http.Error(w, "missing", 404) }
        w.Header().Set("Content-Type", "application/json")
        _, _ = io.WriteString(w, resp)
    }
    mux := http.NewServeMux(); mux.HandleFunc("/", handler)
    suite.server = httptest.NewServer(mux)
}
func (suite *HelloClientSuite) TearDownSuite() { suite.server.Close() }
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.22 client_test.go"*

---

### In-Memory Cache via `map[string]string`

**Principle:** Short-lived caches for slow external calls belong in the service, not the handler. Cache key = `word:language`.

**Code:**
```go
type RemoteService struct {
    client HelloClient
    cache  map[string]string
}
func (s *RemoteService) Translate(word, language string) string {
    word     = strings.ToLower(word)
    language = strings.ToLower(language)
    key := fmt.Sprintf("%s:%s", word, language)
    if tr, ok := s.cache[key]; ok { return tr }   // cache hit
    resp, err := s.client.Translate(word, language)
    if err != nil { log.Println(err); return "" }
    s.cache[key] = resp                           // cache miss → store
    return resp
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 6.20 remote_translator.go"*

---

### Behaviour-Driven Development (Gherkin + Godog)

**Principle:** BDD tests are user-facing requirements written in plain English. Project managers or QA can write the feature file; engineers wire the steps. One feature file can drive backend, frontend, and integration suites.

**Code:**
```gherkin
Feature: Translation Service
  Users should be able to submit a word to translate words within the application
  @smoke-test
  Scenario: Translation
    Given the word "hello"
    When I translate it to "german"
    Then the response should be "Hallo"
  @regression-test
  Scenario: Translation Czech
    Given the word "hello"
    When I translate it to "Czech"
    Then the response should be "Ahoj"
```
```go
// Wire steps in main_test.go
type apiFeature struct {
    client  *resty.Client
    server  *httptest.Server
    word    string
    language string
}
func (api *apiFeature) theWord(arg1 string) error  { api.word = arg1; return nil }
func (api *apiFeature) iTranslateItTo(arg1 string) error { api.language = arg1; return nil }
func (api *apiFeature) theResponseShouldBe(arg1 string) error {
    url := fmt.Sprintf("%s/translate/%s", api.server.URL, api.word)
    resp, err := api.client.R().
        SetHeader("Content-Type", "application/json").
        SetQueryParams(map[string]string{"language": api.language}).
        SetResult(&rest.Resp{}).Get(url)
    if err != nil { return err }
    res := resp.Result().(*rest.Resp)
    if res.Translation != arg1 {
        return fmt.Errorf("translation should be set to %s", arg1)
    }
    return nil
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 9.2 / 9.11"*

---

### Tag Test Suites (Smoke vs Regression)

**Principle:** Smoke tests are "does it turn on?" — fast, run on every build. Regression tests cover previously-reported bugs — slower, run less often. Tags let the same feature file serve both audiences.

**Code:**
```yaml
smoke-test:
  needs: test
  steps:
  - run: godog run --tags=smoke-test
regression-test:
  needs: test
  steps:
  - run: godog run --tags=regression-test
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 9.19 / 9.21 ci.yaml"*

---

### Containerised Integration Tests (dockertest)

**Principle:** Mount a production backup into a Docker-managed Redis for integration tests. Same code path as production; no mocking the database.

**Code:**
```go
func InitializeTestSuite(sc *godog.TestSuiteContext) {
    pool, _ = dockertest.NewPool("")
    wd, _ := os.Getwd()
    mount := fmt.Sprintf("%s/data/:/data/", filepath.Dir(wd))
    redis, _ := pool.RunWithOptions(&dockertest.RunOptions{
        Repository: "redis",
        Mounts:     []string{mount},
    })
    redis.Expire(600)                            // Kill container if it hangs
    database = redis
}
// Each scenario:
ctx.Before(func(...) {
    cfg := config.Configuration{}
    cfg.LoadFromEnv()
    cfg.DatabaseURL  = "localhost"
    cfg.DatabasePort = database.Port("6379")     // Docker-assigned random port
    mux := API(cfg)
    server := httptest.NewServer(mux)
    api.server = server
})
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 9.15 / 9.16 main_test.go"*

---

### FaaS Proxy Wrapper for Cloud Functions

**Principle:** Google Cloud Functions only sees the package root. Provide a thin proxy file that re-exports your `http.Handler`.

**Code:**
```go
package faas
import (
    "net/http"
    "github.com/holmes89/hello-api/handlers/rest"
)
func Translate(w http.ResponseWriter, r *http.Request) {
    rest.TranslateHandler(w, r)                  // delegates to the real handler
}
// You can always use http.Mux here to reroute multiple calls in the future
// through a single function.
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 4.2 faas.go"*

---

### FaaS Deploy in Pipeline + Smoke Test

**Code:**
```yaml
deploy-function:
  name: Deploy FaaS
  runs-on: ubuntu-latest
  needs: test
  if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
  steps:
  - uses: actions/checkout@v2
    with: { fetch-depth: 0 }
  - name: Deploy function
    id: deploy
    uses: google-github-actions/deploy-cloud-functions@main
    with:
      name: translate
      entry_point: Translate
      runtime: go116
      credentials: ${{ secrets.gcp_credentials }}
  - id: test
    run: curl "${{ steps.deploy.outputs.url }}/hello"     # Smoke test the live URL
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 4.3 pipeline.yml"*

---

### PaaS Health Check (and App Engine `app.yaml`)

**Principle:** Long-running services need a `/health` endpoint that returns 200 + `{"status":"up"}` so the platform can decide to restart or route traffic. FaaS typically doesn't need it (functions spin up per invocation).

**Code:**
```go
// handlers/health.go
func HealthCheck(w http.ResponseWriter, r *http.Request) {
    enc := json.NewEncoder(w)
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    resp := map[string]string{"status": "up"}
    if err := enc.Encode(resp); err != nil { panic("unable to encode response") }
}
// main.go
mux.HandleFunc("/health", handlers.HealthCheck)
```
```yaml
# app.yaml — Google App Engine PaaS
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 4.6 / 4.7 / 4.8"*

---

### Buildpacks for Zero-Config Containers

**Principle:** Buildpacks detect your language, build, and produce a cloud-optimised image. No Dockerfile required.

**Code:**
```bash
$ pack builder suggest
Google: gcr.io/buildpacks/builder:v1 Ubuntu 18 base image
  with buildpacks for .NET, Go, Java, Node.js, and Python
Heroku: heroku/buildpacks:20 ...
Paketo: paketobuildpacks/builder:base ...

$ pack build hello-api --builder gcr.io/buildpacks/builder:v1
$ docker run hello-api                          # runs immediately
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "7.2 / 7.3"*

---

### Multi-Stage Dockerfile: Min Image ~5MB on `scratch`

**Principle:** Go binaries are statically linked. A `scratch`-based final image gives you the smallest possible footprint and zero OS attack surface.

**Code:**
```dockerfile
FROM golang:1.18 AS deps                        # Build deps cached separately
WORKDIR /hello-api
ADD *.mod *.sum ./
RUN go mod download

FROM deps as dev                                # Full toolchain for dev
ADD . .
EXPOSE 8080
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags "-w -X main.docker=true" \
    -o api cmd/main.go
CMD ["/hello-api/api"]

FROM scratch as prod                            # Empty base; binary is self-contained
WORKDIR /
EXPOSE 8080
COPY --from=dev /hello-api/api /
CMD ["/api"]
```
Image sizes reported in the book:
```
| hello-api | dev    | 962MB   | (full toolchain)
| hello-api | min    | 4.74MB  | (scratch — 3% of Buildpack image)
| hello-api | latest | 129MB   | (Buildpack)
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 7.3 Dockerfile"*

---

### Docker Compose Profiles for Local Dev vs Prod

**Principle:** Profiles let the same compose file drive dev iteration *and* a prod-like stack.

**Code:**
```yaml
version: "3.8"
services:
  api-min:
    profiles: ['prod']
    image: ghcr.io/holmes89/hello-api:min
    ports: ['8080:8080']
    build: .
  api-dev:
    profiles: ['dev']
    image: ghcr.io/holmes89/hello-api:dev
    ports: ['8080:8080']
    build:
      context: .
      target: dev
  database:
    image: redis:latest
    ports: ['6379:6379']
    volumes:
      - "./data/:/data/"
```
```bash
docker-compose --profile prod up                # prod-like stack
docker-compose --profile dev up                 # dev mode
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 7.5 docker-compose.yml / 9.13"*

---

### Kubernetes Deployment with Health Probes

**Principle:** Always set liveness and readiness probes on the same `/health` endpoint. Liveness = "is it running?" (restart if not). Readiness = "is it serving traffic?" (route only if yes).

**Code:**
```yaml
# k8s/hello-api/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata: { name: hello-api }
spec:
  replicas: 1                                    # Bump for HA
  selector: { matchLabels: { app: hello-api } }
  template:
    metadata: { labels: { app: hello-api } }
    spec:
      containers:
      - name: hello-api
        imagePullPolicy: Always
        image: gcr.io/PROJECT_NAME/hello-api:latest
        ports:
        - containerPort: 8080
          name: hello-api-svc
        livenessProbe:
          httpGet: { path: /health, port: 8080 }
          initialDelaySeconds: 3
          periodSeconds: 3                      # Check every 3 seconds
        readinessProbe:
          httpGet: { path: /health, port: 8080 }
          initialDelaySeconds: 3
          periodSeconds: 3
```
```yaml
# k8s/hello-api/service.yml
apiVersion: v1
kind: Service
metadata: { name: hello-api }
spec:
  type: LoadBalancer                             # Cloud-provided LB
  selector: { app: hello-api }
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 10.2 / 10.3 / 10.4"*

---

### ConfigMap + Secret for K8s Application Configuration

**Principle:** Use ConfigMap for non-sensitive config and Secret for passwords. Wire them into the deployment as env vars. Secrets are "obfuscated, not encrypted" — production should use Vault or a real secret manager.

**Code:**
```yaml
# k8s/hello-api/config.yml
apiVersion: v1
kind: ConfigMap
metadata: { name: hello-api }
data:
  database_url: "redis-cluster"                 # DNS name from Helm chart
```
```yaml
# deployment.yml — env section
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
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 10.8 / 10.9"*

---

### Deploy Production Redis with Helm

**Principle:** Helm is Kubernetes' package manager. Use it for out-of-the-box production-grade dependencies.

**Code:**
```makefile
install-redis:
	helm install redis-cluster bitnami/redis --set password=$$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '')
deploy:
	kubectl apply -f k8s
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 10.7 Makefile"*

---

### GitHub Release + Changelog on Tag Push

**Principle:** Only tag-driven releases go to customers. Auto-generate release notes from commit messages so the bar for clear commits stays high.

**Code:**
```yaml
name: CI Checks
on:
  push:
    branches: [main]
    tags: ['v*']                              # Tag-driven release path
jobs:
  deliver:
    name: Release
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && contains(github.ref, 'refs/tags/')
    steps:
    - uses: actions/checkout@v2
    - uses: actions/download-artifact@v2
      with: { name: api }
    - name: Changelog                            # auto-generate from commits
      uses: scottbrenner/generate-changelog-action@master
      id: Changelog
    - name: Create Release
      id: create_release
      uses: actions/create-release@v1
      env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: ${{ steps.Changelog.outputs.changelog }}
        draft: false                            # promotion, not preview
        prerelease: false
    - name: Upload Release Binary
      uses: actions/upload-release-asset@v1
      env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: api
        asset_name: api
        asset_content_type: application/octet-stream
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 4.1 / 8.15 pipeline.yml"*

---

### Service Account + GitHub Secret for Cloud Deploys

**Principle:** Never store cloud credentials in the repository. Create a dedicated service account with least-privilege roles; upload its JSON key as a GitHub Actions secret.

**Code (GCP service-account role set):**
- App Engine admin
- App Engine deployer
- Cloud Build editor
- Cloud Functions admin
- Cloud Functions developer
- Storage admin

```bash
# Create JSON key, then in GitHub repo: Settings → Secrets → GCP_CREDENTIALS
$ cat keyfile.json    # paste into the secret value
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "4.3 Setting up a deployment account"*

---

### Service Decomposition: `service` + `handler` + `server`

**Principle:** Treat business logic, request handling, and server wiring as three distinct units. Each has its own tests.

**Code:**
```
// service — pure business logic
package translation
func Translate(word, language string) string { ... }

// handler — request/response translation only
package rest
func TranslateHandler(w http.ResponseWriter, r *http.Request) { ... }

// server — wires service → handler → mux
func main() {
    svc := translation.NewStaticService()
    h   := rest.NewTranslateHandler(svc)
    http.HandleFunc("/translate/hello", h.TranslateHandler)
    http.ListenAndServe(":8080", nil)
}
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "3.1 What to test / 6.3 / 6.7"*

---

### Testable `main()`: Extract the Wiring

**Principle:** Move the mux-building logic out of `main()` into an `API(cfg)` function so tests can call it with a configuration and wrap the result in `httptest.NewServer`.

**Code:**
```go
// main.go
func main() {
    cfg := config.LoadConfiguration()
    addr := cfg.Port
    mux := API(cfg)
    log.Printf("listening on %s\n", addr)
    log.Fatal(http.ListenAndServe(addr, mux))
}
func API(cfg config.Configuration) *http.ServeMux {
    mux := http.NewServeMux()
    var translationService rest.Translator
    translationService = translation.NewStaticService()
    if cfg.LegacyEndpoint != "" {
        client := translation.NewHelloClient(cfg.LegacyEndpoint)
        translationService = translation.NewRemoteService(client)
    }
    translateHandler := rest.NewTranslateHandler(translationService)
    mux.HandleFunc("/translate/hello", translateHandler.TranslateHandler)
    mux.HandleFunc("/health", handlers.HealthCheck)
    return mux
}
// Test (from main_test.go):
mux := API(cfg)
server := httptest.NewServer(mux)
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 9.6 / 9.10"*

---

### Resty for Readable HTTP Test Clients

**Principle:** `resty` produces fluent, chainable HTTP client code that reads like a sentence.

**Code:**
```go
resp, err := resty.New().R().
    SetHeader("Content-Type", "application/json").
    SetQueryParams(map[string]string{"language": "german"}).
    Get("http://localhost:8080/translate/hello")
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 9.7 / 9.11"*

---

### From FaaS → PaaS → CaaS → K8s — Only When Metrics Justify It

**Principle:** Move left-to-right (more control, less abstraction) only when usage data and cost demand it. The cloud bill is usually the first signal.

| Abbreviation | Service                | Products                          |
|--------------|------------------------|-----------------------------------|
| IaaS         | Infrastructure as a Service | AWS EC2, Google Compute       |
| CaaS         | Container as a Service | AWS ECS, Google Cloud Run         |
| PaaS         | Platform as a Service  | Heroku, Google App Engine, Elastic Beanstalk |
| FaaS         | Function as a Service  | AWS Lambda, Google Cloud Functions |

**Rule of thumb:** FaaS for low-traffic startups (pay per invocation, no idle cost). PaaS when you outgrow serverless but still want managed infrastructure. CaaS when you need OS-level access. K8s when cloud bills warrant the operational investment.

*Ref: Shipping_Go_-_Joel_Holmes.md — "Table 4.1 / 11.3 Cruising"*

---

### Pipeline Publishes to Both GCP and GitHub Container Registries

**Code:**
```yaml
containerize-buildpack:
  name: Build Container buildpack
  runs-on: ubuntu-latest
  needs: test
  steps:
  - uses: actions/checkout@v2
  - run: (curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.21.1/pack-v0.21.1-linux.tgz" | sudo tar -C /usr/local/bin/ --no-same-owner -xzv pack)
  - run: pack build gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest --builder gcr.io/buildpacks/builder:v1
  - uses: google-github-actions/setup-gcloud@master
    with: { project_id: ${{ secrets.GCP_PROJECT_ID }}, service_account_key: ${{ secrets.gcp_credentials }} }
  - run: gcloud auth configure-docker --quiet
  - run: docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest    # GCP
  - uses: docker/login-action@master                                                # GitHub
    with: { registry: ${{ env.REGISTRY }}, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
  - run: docker image tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
  - run: docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 7.1 pipeline.yml"*

---

### Deploy CaaS (Google Cloud Run) From Same Image

**Code:**
```yaml
deploy-container:
  name: Deploy Container buildpack
  runs-on: ubuntu-latest
  needs: containerize-buildpack
  if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
  steps:
  - uses: google-github-actions/deploy-cloudrun@main
    id: deploy
    with:
      service: translate
      image: gcr.io/${{ secrets.GCP_PROJECT_ID }}/hello-api:latest
      credentials: ${{ secrets.gcp_credentials }}
  - id: test                                              # Smoke test the deployed URL
    run: curl "${{ steps.deploy.outputs.url }}/hello"
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 7.2 pipeline.yml"*

---

### `.gitignore` for Go Projects

**Code:**
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
api                                                # Don't commit your binary
coverage.out
cover.xhtml
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "Listing 2.5 .gitignore"*

---

### Generative Culture Over Bureaucratic

**Principle:** "Generative cultures investigate failure, share responsibilities, and embrace new ideas." Build failures should be visible to the whole team, and no new work starts until the pipeline is green (Toyota's andon cord).

**Code (failure-mode response):**
| Bureaucratic                              | Generative                              |
|-------------------------------------------|-----------------------------------------|
| Information may be ignored.               | Information is actively sought.         |
| Messengers are tolerated.                 | Messengers are trained.                 |
| Responsibilities are compartmentalized.  | Responsibilities are shared.            |
| Bridging between teams is discouraged.    | Bridging between teams is rewarded.     |
| Failure causes blame.                     | Failure causes inquiry.                 |
| New ideas create problems.                | New ideas are encouraged.               |

*Ref: Shipping_Go_-_Joel_Holmes.md — "8.6 Accountability and handling failure / Table 8.1"*

---

### Three Phases of Product Maturity

**Principle:** Match your process to your product's stage. Process too heavy for a startup wastes time; process too light for a mature product invites bugs.

| Phase        | Focus                                                                                  | Metaphor    |
|--------------|----------------------------------------------------------------------------------------|-------------|
| Startup      | Standardise (Makefile, CI), quick feedback, FaaS/PaaS, cheap unit tests               | Tent        |
| Acceleration | Standardise (lint, vet), modularise (interfaces + DI), containerise (portability)        | Building walls and roof |
| Cruising     | Flexibility (config + feature flags), BDD, Kubernetes, observability                   | Cruising in space |

*Ref: Shipping_Go_-_Joel_Holmes.md — "11.1 Startup / 11.2 Acceleration / 11.3 Cruising"*

---

### OODA Loop for Product Development

**Principle:** Treat product development as Observe → Orient → Decide → Act — repeat forever. Products don't end; they evolve.

```
Observe → Orient → Decide → Act
   ↑________________________|
```

*Ref: Shipping_Go_-_Joel_Holmes.md — "11.5 The OODA loop / Figure 11.4"*

---

### Constraint Theory: Protect the Developer

**Principle:** In software pipelines, the developer is the bottleneck. "Adding more people to a project doesn't speed up delivery time, just as 'nine women cannot make a baby in one month.'" Optimise and protect developer time.

*Ref: Shipping_Go_-_Joel_Holmes.md — "5.2 Constraints on development"*

---

### Developer Flow (Csikszentmihalyi) vs Quality Guards

**Principle:** Quality enforcement interrupts flow. Move checks as close to the developer as possible (pre-commit, local Makefile) so they fail in seconds, not minutes.

**Code:**
```yaml
# Pipelines order checks from cheapest to most expensive
format-check (seconds) → lint (minute) → test (minutes) → build → deploy
```
*Ref: Shipping_Go_-_Joel_Holmes.md — "5.7 Flow / 5.6 Git hooks"*

---

### Five Ws for Deployment Decisions

**Principle:** Before scaling infrastructure, gather metrics on the five Ws — Who, What, Where, When, Why — so the next abstraction level matches real usage.

*Ref: Shipping_Go_-_Joel_Holmes.md — "11.4.3 Delivering"*

---

### Cross-Language Pipeline Portability

**Principle:** The pipeline is language-agnostic. "Your process should be agnostic of the code we have written." Appendices repeat the same patterns in Kotlin (Quarkus + Maven + Testcontainers), Python (FastAPI + Poetry + pytest), JavaScript (Express), and Terraform (IaaS alternative).

*Ref: Shipping_Go_-_Joel_Holmes.md — "Appendix A. Using Kotlin / Appendix B. Using Python / Appendix C. Using JavaScript / Appendix D. Using Terraform"*

---

### Small Pieces → Fast Feedback → Less Risk

**Principle:** A 2,000-line change becomes ten 200-line reviews, each easier to verify. Smaller work-in-progress ties up less capital (WIP is money on the table). Ship the smallest valuable thing, observe, iterate.

*Ref: Shipping_Go_-_Joel_Holmes.md — "1.2 Small pieces"*

---

### Empty Main Package for FaaS, Tagged Binary for CLI

**Principle:** GCP Cloud Functions ignores sub-packages — keep a thin `faas.go` in the repo root that delegates to your real handler. "You can always use an http.Mux here to reroute multiple calls in the future through a single function."

*Ref: Shipping_Go_-_Joel_Holmes.md — "4.5 Function as a Service (FaaS)"*

---

## Anti-Patterns & Common Mistakes

- **Tightly coupled handler tests:** A handler test that fails when the underlying service changes is testing the wrong thing. *Fix:* inject a stub so the test asserts only handler behaviour.
- **Retrofitting interfaces after the fact:** "The first reason is to underline the importance of creating interfaces early in development instead of doing it later. You can see the difficulty and pain of making these changes after the fact." *Fix:* design interfaces during the first commit.
- **Over-mocking:** "Complicated structs are hard to write tests for and therefore are more prone to errors." If your mock is more complex than the unit, the unit is too big. *Fix:* split it.
- **Mocks that need constant updating:** If you change the mock interface, your abstraction is wrong. *Fix:* rethink the interface.
- **100% coverage target:** "Attempting to reach total code coverage can lead to poorly written tests that are difficult to maintain over time." *Fix:* ~80%, focusing on business logic.
- **Sloppy interfaces:** Interfaces with too many methods or too many parameters. *Fix:* interface segregation, one or two methods per interface.
- **Secrets in repo or `.env`:** "Your account houses things like credit cards and other personal identifying information." *Fix:* service account + GitHub secret + least-privilege roles.
- **Insecure "allUsers" exposure:** Required for public FaaS access — but ensure the function is idempotent and bounded.
- **Reaching for new tools before basic ones work:** "People want to grab for a new tool all of the time but don't know how to use it. The old beat-up tools are old and beat up for a reason — it's because they work." *Fix:* design docs and RFCs before adopting new tech.
- **Storing tag/hash at runtime instead of build:** "We want these values to be linked to the binary instead of read through an environment variable because it should be associated with the binary itself." *Fix:* `-ldflags -X package.var=value`.
- **Linting only in CI:** Pre-commit hooks run `golang-ci` locally so mistakes die in the editor.
- **Coverage report ignored:** "HTML coverage reports are generated and uploaded as pipeline artifacts." *Fix:* treat them as part of the team's review backlog.
- **Big-bang migrations:** "Strangler application" pattern lets you swap the new system in gradually without a risky cutover.
- **Assuming config in a fixed location:** K8s has ConfigMap *and* Secret — never store a database password in a ConfigMap.
- **Helm secrets considered encrypted:** "Kubernetes has a special field called a secret, it does not mean this is encrypted or secure, only that it is obfuscated." *Fix:* use Vault, AWS Secrets Manager, or GCP Secret Manager.

## Decision Heuristics / Checklists

- **Build phase choice (FaaS / PaaS / CaaS / K8s):** FaaS while idle cost dominates; PaaS when you outgrow serverless but want managed infra; CaaS when you need OS-level access; K8s when cloud bills justify operational overhead.
- **Test tier selection:**
  - Unit: deterministic algorithms (calculate, transform). Always table-driven. ≥80% coverage.
  - System (httptest): handlers — black-box inputs/outputs, no real socket.
  - Integration (Godog + dockertest): user-facing features, BDD scenarios tagged `@smoke-test` / `@regression-test`.
  - End-to-end (UI/Selenium/Cypress): critical user journeys only.
- **Stub vs mock vs fake:**
  - Stub → simple placeholder, no call verification.
  - Mock → verify inputs and call counts (use `Times(1)` for cache behaviour).
  - Fake → entire subsystem simulation (httptest.Server for HTTP clients).
- **Configuration precedence:** defaults → JSON file → env vars → flags. Production uses env vars injected by the platform; developers override with flags.
- **Review size:** ≤300 lines. If larger, break it up.
- **Pipeline order:** format-check → lint → vet → test → build → smoke-test → deploy.
- **Branch protection:** `main` requires 1 review + passing checks. Deploys only on `push`, never on `pull_request`.
- **Container base choice:** Buildpacks for cloud-tuned images with no config; multi-stage Dockerfile with `scratch` for smallest possible Go image; full toolchain only in `dev` stage.
- **Kubernetes probe placement:** both liveness and readiness on `/health`. Liveness restarts the pod; readiness gates traffic routing.
- **Release tagging:** tags `v*` only — git tag `v1.2.3` and `git push origin v1.2.3` triggers GitHub Release + changelog + binary upload.
- **When to add K8s:** when monthly cloud bill on FaaS/PaaS exceeds the cost of an engineer running the cluster.
- **Smoke vs regression tests:** smoke on every PR (fast); regression on tag pushes or nightly (slow).

## Key Takeaways

1. **Build the pipeline first.** CI/CD is foundational, not a retrofit. The pipeline runs the same `make` commands developers run locally.
2. **Quality gates run cheap → expensive in order.** Format, lint, vet, test, build, smoke, deploy. Local hooks catch the cheap ones in seconds.
3. **Define interfaces where they're consumed.** Go's duck typing means concrete types satisfy interfaces implicitly — keep interfaces tiny and composable.
4. **Inject dependencies via constructors.** Manual DI is fine until complexity demands Wire/Fx/Kit. The wiring belongs in `main()`; the logic belongs in services.
5. **Layered configuration: defaults → JSON → env → flags.** Production uses env vars; developers override locally with flags.
6. **Tag-driven releases with provenance injection.** Use `-ldflags -X` to embed tag, hash, build-date in the binary and expose them via `/info`.
7. **Strangler-application pattern for migrations.** Same binary builds all variants; configuration flips which service is wired in.
8. **Smoke tests run on every PR; regression tests run on tags.** Godog + dockertest enables real-world integration coverage.
9. **Container images: Buildpacks for cloud-tuned, multi-stage `scratch` Dockerfile for minimal Go images (~5MB).** Compose profiles separate dev from prod.
10. **The pipeline is language-agnostic.** The same CI/CD, testing, and release patterns work for Kotlin, Python, JavaScript — and Terraform replaces K8s for IaaS-style infrastructure.

## Cross-References
- Related: [[../Mastering_Go.md]]
- Topic index: [[../INDEX.md]]