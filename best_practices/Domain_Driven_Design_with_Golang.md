# Per-Book Best Practices — Domain-Driven Design with Golang (Deep Dive)

> Maximum-depth extract from *Domain-Driven Design with Golang* (Matthew Boyle, Packt 2022). All Go code from the book is preserved verbatim. Use this document as both a tactical reference and a strategic playbook when introducing DDD into a Go service.

---

# Domain-Driven Design with Golang
**Author:** Matthew Boyle
**Published:** December 2022 (Packt Publishing, 1st Edition)
**Topic tags:** `#architecture` `#general` `#ddd` `#bounded-contexts` `#aggregates` `#go` `#microservices` `#cqrs` `#eda` `#testing`
**Language focus:** Go-first (also DDD language-agnostic — patterns transfer)
**Sources:** `markdown_output/Domain-Driven_Design_with_Golang_-_Matthew_Boyle/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md` · `summaries/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md`

---

## TL;DR

DDD is a collaborative discipline (engineers + domain experts + leadership), not just an architectural pattern. The book teaches DDD end-to-end through the lens of Go: strategic foundations (ubiquitous language, bounded contexts, subdomains), tactical building blocks (entities, value objects, aggregates, factories, repositories, domain/application/infrastructure services), two full reference implementations (CoffeeCo monolith + Recommendation microservice using ports/adapters and anti-corruption layers), distributed-system extensions (CQRS, EDA, 2PC, saga, message buses), and a TDD/BDD bonus chapter with a worked Go example. Apply it when complexity is real, transactional consistency boundaries matter, and the team has the appetite for ubiquitous-language workshops. Skip it for pure CRUD with fewer than ~30 user stories.

---

## How to Read This Document

This document mirrors the book's two-part structure:

- **Part 1 (Foundations):** Strategic + tactical DDD concepts and the Go that implements each.
- **Part 2 (Real-World):** A monolith and a microservice built end-to-end, then distributed-system extensions, then TDD/BDD.
- **Reference sections:** Cross-cutting Go best practices, anti-patterns, and decision heuristics.

Every Go snippet is taken straight from the source. References use the form `book.md:` followed by a chapter heading. The full source book is at `markdown_output/Domain-Driven_Design_with_Golang_-_Matthew_Boyle/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md`.

---

# PART 1 — FOUNDATIONS

# Chapter 1 — A Brief History of Domain-Driven Design

DDD was introduced by Eric Evans in his 2003 book *Domain-Driven Design: Tackling Complexity in the Heart of Software* (the "Big Blue Book"). Evans wrote it because he kept watching complex software projects fail in the same way: the system's internal model drifted away from the real-world domain, engineers and business folks talked past each other, and refactors became excavations.

> "The book Domain-Driven Design was an attempt to capture for people the successful practices that I had seen or used, some of which have been around for a long time and some of which are relatively new, and put together into a coherent set of practices with clear names so that maybe we can have broader success than we have in the past… a great deal of domain-driven design comes straight out of good old-fashioned object-oriented design patterns." (Evans, *Software Engineering Radio*, 2019)

## 1.1 The World Before DDD

The closer a system's representation matches the domain it serves, the easier the system is to maintain and the easier it is to discuss with non-technical stakeholders. Before DDD, engineers still tried to organize code around domain concepts, but no formal vocabulary existed. Some teams invented their own; many did not.

### 1.1.1 Object-Oriented Design Patterns

Evans drew heavily on the 23 patterns in the 1995 *Gang of Four (GoF)* book: *Design Patterns, Elements of Reusable Object-Oriented Software* (Gamma, Helm, Johnson, Vlissides). The GoF split them into three categories — all still relevant in DDD:

| Category          | Concern                                        | Example              |
|-------------------|------------------------------------------------|----------------------|
| Creational        | How objects are created                        | Factory, Builder     |
| Structural        | How objects are composed                       | Adapter, Decorator   |
| Behavioral        | How objects communicate                        | Strategy, Observer   |

DDD did not "invent" factories, repositories, or services — those come straight from OOD. What DDD contributes is **a discipline for deciding when and how to apply them** so that the code structure mirrors the business.

If Go is your first programming language, you will not have traditional OO instincts, and that is fine — Go's interface system and type-driven design give you the same modelling tools without inheritance tax.

### 1.1.2 A Concrete OO Example (Java, Book Excerpt)

To show what OOD modelling looks like in practice, the book includes a Java employee class:

```java
public class Employee {
    private String firstName;
    private String lastName;

    public Employee(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    public String getFirstName() {
        return this.firstName;
    }

    public String getLastName() {
        return this.lastName;
    }

    public String toString() {
        return "Employee(" + this.firstName + "," + this.lastName + ")";
    }
}
```

The class is readable, models an employee cleanly, and is a sane starting point for any HR feature ("list all employees", "add location to profile", etc.). The DDD lesson: keep your objects this close to the business.

## 1.2 Eric Evans and the Three Pillars of DDD

Evans calls his three pillars:

### 1. Ubiquitous Language
The shared, rigorous vocabulary used by developers *and* business people within a single bounded context. Used in conversation, requirements docs, design docs, **and in source code**. Never imposed by domain experts — built collaboratively. Evolves as understanding deepens.

### 2. Strategic Design
The phase where you map the business domain and decide the **bounded contexts**. Goal: architecture follows business outcomes. Output: a domain model diagram (an abstract representation of the problem space). For a shipping system the model puts "shipping" at the centre and surrounds it with subordinate concerns. Bounded contexts are sketched but not finalised until later.

### 3. Tactical Design
The patterns that define software boundaries: **entities, aggregates, value objects**. These map to Chapter 3 of the book.

## 1.3 Adoption of DDD — When to Use It

DDD has remained popular continuously since 2004 (Google Trends shows steady interest). Three forces have kept it alive: Greg Young's work on **CQRS**, the free 2006 mini-book *Domain-Driven Design Quickly*, and Vaughn Vernon's *Implementing Domain-Driven Design* (2013, the "Big Red Book", which Evans called *"the most ambitious book since my own"*).

Microsoft, Amazon, and IBM all publish DDD guidance for their platforms. Just because they use it does not mean your side project should.

### 1.3.1 The DDD Scorecard (Simplified Vernon Scorecard)

Score yourself 0–5 against each row:

| Question                                                                                          | Points |
|---------------------------------------------------------------------------------------------------|--------|
| Mostly simple CRUD against a database?                                                            | 0      |
| <30 user stories / business flows?                                                                | 1      |
| 40+ user stories / business flows?                                                               | 2      |
| Likely to grow in complexity over time?                                                          | 3      |
| Long-lived; future changes non-trivial?                                                           | 4      |
| Novel domain; no one has built this before?                                                       | 5      |

**Score > 7 → DDD is a strong fit.** Below 7 may still benefit from individual principles, but the full commitment is rarely worth it. DDD is an organisational commitment, not an engineering side project: it requires time with domain experts, a willingness to iterate on the language, and engineers who can think at the level of behaviour rather than syntax.

## 1.4 Strengths of the Go Fit

Go is not OO; its interface system, structural typing, and package model are an excellent substrate for DDD:

- **Interfaces as ubiquitous-language contracts.** Define `Customer` or `Booking` behaviour as interfaces in the same package as the entity. Consumer defines the interface; the implementer fulfils it.
- **Unexported fields enforce value-object immutability.** Go's visibility rules literally prevent external mutation if you keep fields lowercase — no language annotations needed.
- **`internal/` packages enforce aggregate boundaries.** Anything under `internal/` cannot be imported by other modules. DDD wants exactly this.
- **Function-based factories.** No static factory class needed; `func NewX(...) (*X, error)` plays the role idiomatically.
- **Context-aware services.** `context.Context` flows through every layer — authorisation, tracing, cancellation sit naturally at the application-service boundary.

---

# Chapter 2 — Understanding Domains, Ubiquitous Language, and Bounded Contexts

Strategic foundation. One running scenario (payments-and-subscriptions team) is rewritten multiple times to show how DDD tightens naming, boundaries, and external communication.

## 2.1 Setting the Scene — The Payments/Subscriptions Team

You have just been promoted to team lead. Domain experts tell you:

> When a lead uses our app for the first time, they must pick one of three subscription plans: **basic**, **premium**, or **exclusive**. Which plan determines which features they get. After a plan is created, the lead converts to a **customer** until they **churn**, at which point they become a **lead** again. After 6 months they are a **lost lead** and we might target them with a **re-engagement campaign** that could include a **discount code**. Once a plan is created, we set up a **recurring payment** to **capture funds** from the customer via **direct debit**.

Excitedly, you write a first pass:

```go
package chapter2

import (
    "context"
)

type UserType = int
type SubscriptionType = int

const (
    unknownUserType UserType = iota
    lead
    customer
    churned
    lostLead
)

const (
    unknownSubscriptionType SubscriptionType = iota
    basic
    premium
    exclusive
)

type UserAddRequest struct {
    UserType      UserType
    Email         string
    SubType       SubscriptionType
    PaymentDetails PaymentDetails
}

type UserModifyRequest struct {
    ID            string
    UserType      UserType
    Email         string
    SubType       SubscriptionType
    PaymentDetails PaymentDetails
}

type User struct {
    ID            string
    PaymentDetails PaymentDetails
}

type PaymentDetails struct {
    stripeTokenID string
}

type UserManager interface {
    AddUser(ctx context.Context, request UserAddRequest) (User, error)
    ModifyUser(ctx context.Context, request UserModifyRequest) (User, error)
}
```

*Note:* at this stage the author has not added an `import "errors"` because nothing returns errors yet, but as we will see most of these APIs will need it. Take the imports as illustrative.

The author holds this code up and says: "We'll revisit this as we learn more about DDD."

## 2.2 Domains and Sub-Domains

Evans: "a sphere of knowledge, influence, or activity." Practically, the **business** the software serves. Sub-domain is used interchangeably with domain except that *sub-domain* signals a domain is a child of a higher-level one.

The running example has two sub-domains: **payments** and **subscriptions**. Mature organisations debate and structure teams around domains; new sub-domains emerge, teams split. The discipline is "DDD is not a science" — multiple splits are defensible as long as each split is grounded in how the business actually works.

## 2.3 Ubiquitous Language

**Ubiquitous language is the overlap between domain-expert language and technical-expert language.** Common terms in the running example: *lead, customer, churn, lost lead, subscription, plan, feature, recurring payment, capture funds, direct debit, discount code, re-engagement campaign*.

Benefits when you invest:

1. **No lost-in-translation bugs.** The book opens with a horror story: business asked for "support multiple accounts per customer"; the system had no `Customer` entity (it had `User`), assumed one user per account, so a trivial change became a quarter-long re-architecture.
2. **Code as documentation.** `CreateLead(...)` reads like the domain expert's sentence; `AddUser(...)` does not.
3. **Sharper conversations.** Subject-matter experts can review your PRs.

### 2.3.1 The Code Smell That Fixes Itself

Look again at the original `UserType`/`AddUser`:

```go
type UserType = int
type subscriptionType = int

const (
    unknownUserType UserType = iota
    lead
    customer
    churned
    lostLead
)
```

Two issues:

1. The constants are great — `lead`, `customer`, `churned`, `lostLead` *are* the language.
2. But the word **user** is nowhere in the domain experts' brief. We invented it. That is exactly the kind of term that should not be in the code unless we get the experts to define it explicitly.

The author proposes defining *user* as: "a way to represent any person using our app (or who has used our app) regardless of status," with possible states `lead`, `lostLead`, `customer`, `churned`. With that definition, `AddUser` is the wrong verb — the domain has no concept of adding users. **Refactored:**

```go
type LeadRequest struct {
    email string
}

type Lead struct {
    id string
}

type LeadCreator interface {
    CreateLead(ctx context.Context, request LeadRequest) (Lead, error)
}

type Customer struct {
    leadID string
    userID string
}

func (c *Customer) UserID() string {
    return c.userID
}

func (c *Customer) SetUserID(userID string) {
    c.userID = userID
}

type LeadConvertor interface {
    Convert(ctx context.Context, subSelection SubscriptionType) (Customer, error)
}

func (l Lead) Convert(ctx context.Context, subSelection SubscriptionType) (Customer, error) {
    // TODO implement me
    panic("implement me")
}
```

(Yes, the book's version uses `panic("implement me")` as a placeholder — readers are expected to replace these stubs.)

Now `CreateLead` and `LeadConvertor.Convert` read like the domain experts' sentences. Engineers and product people can talk about the same code together.

### 2.3.2 Practical Tips for Building a Ubiquitous Language

- Sit in the domain experts' meetings; offer to take minutes. Capture every term you don't recognise and follow up offline to add definitions to your team's glossary.
- Treat the glossary as living; review during sprint planning.
- **Never apply a single language company-wide.** A *customer* in marketing is not the same as a *customer* in subscriptions. Rigour is local.

## 2.4 Bounded Contexts

A bounded context is a boundary inside which a particular model and a particular ubiquitous language apply. The same word can mean different things in different contexts. Strategic design draws the boundary; tactical design implements the boundary.

Running example has at least two contexts sharing the term *customer*:

- **Subscription context** — `Customer = lead with an active plan`.
- **Marketing context** — `Customer = anyone in the marketing DB including former leads`.

The takeaway: draw the contexts first, *then* specify how they communicate.

### 2.4.1 Patterns for Inter-Context Communication

**Open Host Service**, **Published Language**, **Anti-Corruption Layer** — these are the spines of Chapters 2 and 6.

## 2.5 Open Host Service

Anything that gives other systems access to yours. Implementation deliberately vague — REST, gRPC, XML, queue, file. Most common modern interpretation: RPC.

A minimal HTTP example using `gorilla/mux`:

```go
package chapter2

import (
    "context"
    "encoding/json"
    "net/http"

    "github.com/gorilla/mux"
)

type UserHandler interface {
    IsUserSubscriptionActive(ctx context.Context, userID string) bool
}

type UserActiveResponse struct {
    IsActive bool
}

func router(u UserHandler) {
    m := mux.NewRouter()
    m.HandleFunc("/user/{userID}/subscription/active", func(writer http.ResponseWriter, request *http.Request) {
        // check auth, etc
        uID := mux.Vars(request)["userID"]
        if uID == "" {
            writer.WriteHeader(http.StatusBadRequest)
            return
        }
        isActive := u.IsUserSubscriptionActive(request.Context(), uID)
        b, err := json.Marshal(UserActiveResponse{IsActive: isActive})
        if err != nil {
            writer.WriteHeader(http.StatusInternalServerError)
            return
        }
        _, _ = writer.Write(b)
    }).Methods(http.MethodGet)
}
```

The contract is small and crisp: `GET /user/{userID}/subscription/active → {"IsActive": true|false}`. Other contexts can call it without knowing anything about Go, Mongo, Stripe, or the team's internal model.

## 2.6 Published Language

A **published language** is the externally-documented contract for a published interface. Two tooling choices dominate in 2024–2026:

### 2.6.1 OpenAPI / Swagger

Schema first; generate docs, server stubs, client SDKs. Swagger Editor at <https://editor.swagger.io>.

Schema for the running example:

```yaml
swagger: "2.0"
info:
  description: "Public documentation for payment & subscription System"
  version: "1.0.0"
  title: "Payment & Subscription API"
host: "api.payments.com"
schemes: ["https"]
paths:
  /users:
    get:
      summary: "Return details about users"
      operationId: "getUsers"
      produces: ["application/json"]
      responses:
        "200":
          description: "successful operation"
          schema: { $ref: "#/definitions/User" }
        "400": { description: "bad request" }
        "404": { description: "users not found" }
definitions:
  User:
    type: "object"
    properties:
      id: { type: "integer", format: "int64" }
      username: { type: "string" }
      subscriptionStatus: { type: "boolean" }
      subscriptionType: { type: "string" }
      email: { type: "string" }
```

Generate Go:

```yaml
# config.yml
package: oapi
output: ./openapi.gen.go
generate:
  models: true
```

```bash
go install github.com/deepmap/oapi-codegen/cmd/oapi-codegen@latest
oapi-codegen --config=config.yml ./oapi.yaml
go mod tidy && go mod vendor   # if errors about missing modules
```

Adding `client: true` produces a typed client:

```go
type ClientInterface interface {
    GetUsers(ctx context.Context, reqEditors ...RequestEditorFn) (*http.Response, error)
}
```

Hook `oapi-codegen` into CI so the published language regenerates every spec change.

**OpenAPI trade-offs:** ✅ documentation-first, code generation, retrofit-friendly / ❌ no breaking-change protection, larger payloads than binary.

### 2.6.2 gRPC and Protobuf

Google's high-throughput schema-first RPC. Built-in load balancing, tracing, health checks, bi-directional streaming, auth; binary protobuf on the wire. Native langs: C#, C++, Dart, Go, Java, Kotlin, Node, Objective-C, PHP, Python, Ruby.

Author's recommendation: use **buf** (`<https://buf.build>`) for Go protobuf tooling.

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"
brew install bufbuild/buf/buf
```

`buf.gen.yml`:

```yaml
version: v1
plugins:
  - name: go
    out: gen/proto/go
    opt: paths=source_relative
  - name: go-grpc
    out: gen/proto/go
    opt:
      - paths=source_relative
      - require_unimplemented_servers=false
```

A naive user.proto will lint-fail until it gets a `package` and `go_package`:

```protobuf
syntax = "proto3";
package user.v1;
option go_package = "example.com/testing/protos/user";

message User {
    int64 id = 1;
    string username = 2;
    string email = 3;
}

service UserService {
    rpc CreateUser (CreateUserRequest) returns (CreateUserResponse) {}
}

message CreateUserRequest {
    User user = 1;
}

message CreateUserResponse {
    bool success = 1;
}
```

`buf generate` writes importable Go code to `gen/proto/go`. Register a `grpc.Server`, implement the service, and you're done.

**gRPC trade-offs:** ✅ compact, fast, rich distributed-systems features / ❌ steeper setup, opinionated tooling.

**Bottom line:** pick whichever the team can operate competently. Either produces excellent published languages.

## 2.7 Anti-Corruption Layer

An **anti-corruption layer** (a.k.a. **adapter layer**) translates data and concepts from one bounded context to another. It prevents one context's model from contaminating another's. The marketing team's published language may look like:

```json
{
  "id": "4cdd4ba9-7c04-4a3d-ac52-71f37ba75d7f",
  "metadata": {
    "name": "some campaign",
    "category": "growth",
    "endDate": "2023-04-12"
  }
}
```

The internal (subscription) campaign model may look completely different — different field names, ISO date format, `Category` repurposed as `Goal`. Either adopt the external model wholesale (couples you to their evolution), or build a translation layer. Translation layer:

```go
package chapter2

import (
    "errors"
    "time"
)

type Campaign struct {
    ID      string
    Title   string
    Goal    string
    EndDate time.Time
}

type MarketingCampaignModel struct {
    Id       string `json:"id"`
    Metadata struct {
        Name     string `json:"name"`
        Category string `json:"category"`
        EndDate  string `json:"endDate"`
    } `json:"metadata"`
}

func (m *MarketingCampaignModel) ToCampaign() (*Campaign, error) {
    if m.Id == "" {
        return nil, errors.New("campaign ID cannot be empty")
    }
    formattedDate, err := time.Parse("2006-01-02", m.Metadata.EndDate)
    if err != nil {
        return nil, errors.New("endDate was not in a parsable format")
    }
    return &Campaign{
        ID:      m.Id,
        Title:   m.Metadata.Name,
        Goal:    m.Metadata.Category,
        EndDate: formattedDate,
    }, nil
}
```

Three properties of a healthy anti-corruption layer: **validates** incoming data so junk cannot poison your domain; **translates** to the destination context's ubiquitous language; **is replaceable** — when the source changes its API, only this layer changes. In large migrations the layer may be an entire service (extra hop for latency/failure modes; staged migration + safe rollback in return).

> "Of all the DDD patterns, the anti-corruption pattern is the one I use most when working on systems that do not use DDD." — Matthew Boyle

## 2.8 Chapter 2 Summary — Strategic Checklist

- [ ] Document every domain; name the sub-domains.
- [ ] Co-create the ubiquitous language with domain experts; track it in a wiki.
- [ ] Use the language in code (structs, methods, errors, packages).
- [ ] Treat the language as living; review during sprint planning.
- [ ] Draw bounded-context boundaries explicitly on a whiteboard before coding.
- [ ] Pick one Open Host Service tech (REST or gRPC) and standardise.
- [ ] Write a published language for every externally-visible contract.
- [ ] Translate via anti-corruption layers; never bind your domain to an external model.

---

# Chapter 3 — Entities, Value Objects, and Aggregates

Where the business logic lives. Entities and value objects are the two basic domain constructs; aggregates combine them into a transactional unit.

## 3.1 Entities

In DDD, **entities are defined by their identity, not their attributes**. Identities survive changes that would render attributes unrecognisable. Example: an eBay user who becomes a seller, a bidder, both, and changes address and email repeatedly — same ID, same person, different state.

A naive auction-site model (user/seller/bidder as separate entities) breaks easily; one rich `Auction` entity with behavioural methods does not:

```go
package chapter3

import (
    "time"

    "github.com/Rhymond/go-money"
)

// Auction is an entity to represent our auction construct.
type Auction struct {
    ID           int
    // We use a specific money library as floats are not good ways to represent money.
    startingPrice money.Money
    sellerID      int
    createdAt     time.Time
    auctionStart  time.Time
    auctionEnd    time.Time
}
```

(The comment is the author's own — go-money's `Money` type stores currency as cents with explicit currency code, eliminating precision loss.)

### 3.1.1 Generating Good Identifiers

Integers break at scale:

```go
fmt.Println(math.MaxInt)
// → 9223372036854775807

fmt.Println(math.MaxInt + 1)
// cannot use math.MaxInt + 1 (...) as int value in argument to fmt.Println (overflows)
```

If your ID scheme is integer-based, you *will* hit the ceiling. Use UUIDs as a safer default:

```go
package chapter3

import "github.com/google/uuid"

type SomeEntity struct {
    id uuid.UUID
}

func NewSomeEntity() *SomeEntity {
    id := uuid.New()
    return &SomeEntity{id: id}
}
```

If you use PostgreSQL, you can lean on the database to generate the UUID (`uuid-ossp` or `gen_random_uuid()` from `pgcrypto`).

**Other ID heuristics:**

| Source                  | Pros                              | Cons                                                                |
|-------------------------|-----------------------------------|---------------------------------------------------------------------|
| `int` auto-increment    | Simplest                          | Overflow, leaks business volume, painful to shard                  |
| UUID v4 (`uuid.New()`)  | Effectively infinite              | 128 bits vs 64 — bigger index, not sortable by time                |
| UUID v7 (`uuid.NewV7()`)| Time-ordered UUID                | Newer; some libs still pre-v7                                     |
| Snowflake (Twitter-style)| Time-ordered, integer storage    | Requires a coordinator; mid-scale complexity                       |
| Domain attribute (SSN, government ID) | Human-meaningful         | Changes! PII! Avoid.                                                |

### 3.1.2 Anemic Domain Models — The Most Common DDD Mistake

An **anemic model** is a struct with mostly public getters/setters and no behaviour; the business logic lives in services or controllers. Symptoms: mostly public getters/setters; no business logic in the entity; other constructs implement the rules in different ways.

Anemic auction (negative example — do **not** copy):

```go
package chapter3

import (
    "time"

    "github.com/Rhymond/go-money"
)

type AnemicAuction struct {
    id            int
    startingPrice money.Money
    sellerID      int
    createdAt     time.Time
    auctionStart  time.Time
    auctionEnd    time.Time
}

func (a *AnemicAuction) GetID() int { return a.id }
func (a *AnemicAuction) StartingPrice() money.Money { return a.startingPrice }
func (a *AnemicAuction) SetStartingPrice(sp money.Money) { a.startingPrice = sp }
func (a *AnemicAuction) GetSellerID() int { return a.sellerID }
func (a *AnemicAuction) SetSellerID(sellerID int) { a.sellerID = sellerID }
func (a *AnemicAuction) GetCreatedAt() time.Time { return a.createdAt }
func (a *AnemicAuction) SetCreatedAt(createdAt time.Time) { a.createdAt = createdAt }
func (a *AnemicAuction) GetAuctionStart() time.Time { return a.auctionStart }
func (a *AnemicAuction) SetAuctionStart(t time.Time) { a.auctionStart = t }
func (a *AnemicAuction) GetAuctionEnd() time.Time { return a.auctionEnd }
func (a *AnemicAuction) SetAuctionEnd(t time.Time) { a.auctionEnd = t }
```

A richer, refactored version — behaviour-rich, invariants enforced:

```go
package chapter3

import (
    "errors"
    "time"

    "github.com/Rhymond/go-money"
)

type AuctionRefactored struct {
    id            int
    startingPrice money.Money
    sellerID      int
    createdAt     time.Time
    auctionStart  time.Time
    auctionEnd    time.Time
}

func (a *AuctionRefactored) GetAuctionElapsedDuration() time.Duration {
    return a.auctionStart.Sub(a.auctionEnd)
}

func (a *AuctionRefactored) GetAuctionEndTimeInUTC() time.Time {
    return a.auctionEnd
}

func (a *AuctionRefactored) SetAuctionEnd(auctionEnd time.Time) error {
    if err := a.validateTimeZone(auctionEnd); err != nil {
        return err
    }
    a.auctionEnd = auctionEnd
    return nil
}

func (a *AuctionRefactored) GetAuctionStartTimeInUTC() time.Time {
    return a.auctionStart
}

func (a *AuctionRefactored) SetAuctionStartTimeInUTC(auctionStart time.Time) error {
    if err := a.validateTimeZone(auctionStart); err != nil {
        return err
    }
    // in reality, we would likely persist this to a database
    a.auctionStart = auctionStart
    return nil
}

func (a *AuctionRefactored) GetId() int { return a.id }

func (a *AuctionRefactored) validateTimeZone(t time.Time) error {
    tz, _ := t.Zone()
    if tz != time.UTC.String() {
        return errors.New("time zone must be UTC")
    }
    return nil
}
```

Even in this small example, the value of behaviour-rich entities is clear: invariant enforcement (UTC), clear caller expectations, and consistent derived views (elapsed duration).

### 3.1.3 ORM Caveat

ORMs (GORM etc.) are not DDD tools. They push you toward anemic structs, hide the query plan (a major source of slow apps), and couple the domain to the persistence library. If you must use one, put it behind an **adapter layer** — keep domain clean and out of the ORM package.

## 3.2 Value Objects

Value objects are the **opposite** of entities: defined by **values** (not identity); two VOs with the same fields are equal; they **measure, quantify, or describe** a domain concept.

### 3.2.1 The Point Lesson (Verbatim From the Book)

```go
package chapter3

type Point struct {
    x int
    y int
}

func NewPoint(x, y int) *Point {
    return &Point{
        x: x,
        y: y,
    }
}
```

A test that compares two pointer-returned Points:

```go
package chapter3_test

import (
    "testing"

    "ddd-golang/chapter3"
)

func Test_Point(t *testing.T) {
    a := chapter3.NewPoint(1, 1)
    b := chapter3.NewPoint(1, 1)
    if a != b {
        t.Fatal("a and b were not equal")
    }
}
```

Fails because `&Point` returns pointers; pointer comparison compares addresses, not contents.

```
=== RUN Test_Point
    value_objects_test.go:13: a and b were not equal
--- FAIL: Test_Point (0.00s)
```

Switch the constructor to return a value:

```go
type Point struct {
    x int
    y int
}

func NewPoint(x, y int) Point {
    return Point{
        x: x,
        y: y,
    }
}
```

Now the test passes — Go compares the two `Point` values by their contents.

Three rules the book extracts from this:

1. **Lowercase fields** — keeps them unexported so callers cannot mutate them.
2. **Replace, don't mutate** — value objects should be immutable; new state ⇒ new instance.
3. **Side-effect-free functions** — methods on value objects should not mutate state or perform I/O.

The "moving player" example demonstrates replaceability:

```go
package chapter3

type Point struct {
    x int
    y int
}

func NewPoint(x, y int) Point {
    return Point{x: x, y: y}
}

const (
    directionUnknown = iota
    directionNorth
    directionSouth
    directionEast
    directionWest
)

func TrackPlayer() {
    currLocation := NewPoint(3, 4)
    currLocation = move(currLocation, directionNorth)
}

func move(currLocation Point, direction int) Point {
    switch direction {
    case directionNorth:
        return NewPoint(currLocation.x, currLocation.y+1)
    case directionSouth:
        return NewPoint(currLocation.x, currLocation.y-1)
    case directionEast:
        return NewPoint(currLocation.x+1, currLocation.y)
    case directionWest:
        return NewPoint(currLocation.x-1, currLocation.x)
    default:
        // do a barrel roll
    }
    return currLocation
}
```

(Note: the book's `directionWest` contains a bug in the original — `currLocation.x` instead of `currLocation.y`. Reproduced verbatim here; do not copy-paste it.)

### 3.2.2 Choosing Value Objects vs. Entities

Default to value objects — they are safer. Three questions: immutable? measures/quantifies/describes a domain concept? comparable by field values? Yes to all three ⇒ value object; otherwise entity. Pragmatic rule: **start as a value object; promote to entity only when you discover you need identity**.

## 3.3 Aggregates — The Transactional Consistency Boundary

An **aggregate** is a cluster of domain objects treated as a single unit for transactional consistency. Examples:

- **Order** with line items.
- **Team** with employees.
- **Wallet** with cards and currencies.

Aggregates are NOT collections of data. They have methods, enforce invariants, and act as a transaction boundary. The book:

> "Loading, saving, editing, and deleting should happen to all objects within the aggregate or not at all."

Aggregate-sized invariants:

- Cancelling an order returns all items to stock and fires a refund.
- Adding an employee to a team updates the line-manager graph.
- Adding a card to a wallet updates the wallet's total balance.

### 3.3.1 Wallet Aggregate (Verbatim)

```go
type WalletItem interface {
    GetBalance() (money.Money, error)
}

type Wallet struct {
    id          uuid.UUID
    ownerID     uuid.UUID
    walletItems []WalletItem
}

func (w Wallet) GetWalletBalance() (*money.Money, error) {
    var bal *money.Money
    for _, v := range w.walletItems {
        itemBal, err := v.GetBalance()
        if err != nil {
            return nil, errors.New("failed to get balance")
        }
        bal, err = bal.Add(&itemBal)
        if err != nil {
            return nil, errors.New("failed to increment balance")
        }
    }
    return bal, nil
}
```

Three field-by-field notes:

- `id` is the **aggregate root** identity — the wallet's.
- `ownerID` references the owner; load on demand.
- `walletItems` is a slice of `WalletItem`. `WalletItem` is an interface so items can be `DebitCard`, `CreditCard`, `CryptoHolding`, etc., without exposing them externally.

### 3.3.2 Discovering Aggregates

Evans' heuristic: find your **invariants** — rules that must *always* hold. Examples:

- "An order can be created only if the items are in stock."
- "A wallet's available balance cannot exceed the sum of its positive balances minus its credit limits."

For aggregates the *kind* of consistency you want is **transactional** (immediate, atomic), not eventual. **One aggregate per transaction.** If you need more, the model is probably wrong — refactor before adding code.

### 3.3.3 Designing Aggregates

Aim for **small** aggregates: small aggregates ⇒ small transactions ⇒ high transaction success rate under contention; small aggregates ⇒ small locks ⇒ high throughput.

An order aggregate that includes `marketingOptIn` is wrong:

```go
type Order struct {
    items          []item
    taxAmount      money.Money
    discount       money.Money
    paymentCardID  uuid.UUID
    customerID     uuid.UUID
    marketingOptIn bool
}
```

Two reasons: (1) **wrong bounded context** — marketing consent belongs to the marketing context; (2) **wrong transaction boundary** — if a user opts out between starting and completing an order, the order should still complete. Including it in the aggregate makes that impossible.

```go
type Order struct {
    items         []item
    taxAmount     money.Money
    discount      money.Money
    paymentCardID uuid.UUID
    customerID    uuid.UUID
}
```

> "We can still surface a marketing opt-in checkbox in the UI; it just shouldn't belong to the aggregate."

### 3.3.4 Aggregates Across Bounded Contexts

Once you cross a context boundary you cannot keep *transactional* consistency — the receiving system processes the change **eventually**. Verify with domain experts that eventual consistency is acceptable; you unlock better resilience and scalability. Domain events are the primary mechanism (Chapter 7).

## 3.4 Chapter 3 Summary — Tactical Pillar

- [ ] Use UUIDs for entity IDs (`github.com/google/uuid`).
- [ ] Avoid anemic models: methods on the entity, getters not the only API.
- [ ] Default to value objects; promote to entities only when identity is needed.
- [ ] Keep value objects immutable (lowercase fields, replace-not-mutate).
- [ ] Discover aggregates by hunting for invariants.
- [ ] Keep aggregates **small**: one aggregate per transaction.
- [ ] Outside a single bounded context, expect **eventual** consistency.

---

# Chapter 4 — Exploring Factories, Repositories, and Services

The three remaining tactical DDD building blocks. None of them are unique to DDD — they're applied DDD-discipline to OOD patterns.

## 4.1 The Factory Pattern

A factory's job is to **create other objects**. The classic OO shape:

```php
class Factory
{
    public static function build($carType)
    {
        if ($carType == "tesla") {
            return new Tesla();
        }
        if ($carType == "bmw") {
            return new BMW();
        }
    }
}
$myCar = Factory::build("tesla");
```

Go equivalent — idiomatic, no class needed, error for unknown input:

```go
package chapter4

import (
    "errors"
    "log"
)

type Car interface {
    BeepBeep()
}

type BMW struct {
    heatedSeatSubscriptionEnabled bool
}

func (B BMW) BeepBeep() {
    // TODO implement me
    panic("implement me")
}

type Tesla struct {
    autoPilotEnabled bool
}

func (t Tesla) BeepBeep() {
    // TODO implement me
    panic("implement me")
}

func BuildCar(carType string) (Car, error) {
    switch carType {
    case "bmw":
        return BMW{heatedSeatSubscriptionEnabled: true}, nil
    case "tesla":
        return Tesla{autoPilotEnabled: true}, nil
    default:
        return nil, errors.New("unknown car type")
    }
}

func main() {
    myCar, err := BuildCar("tesla")
    if err != nil {
        log.Fatal(err)
    }
    // do something with myCar
}
```

Note: `BMW{}` and `Tesla{}` returned **by value**, not by pointer. The factory hands you a populated, ready-to-use value; you don't reach in and tweak fields.

Three reasons factories are useful:

1. **Standardise creation** of complex structs.
2. **Encapsulate internal details** — the caller never sees unexported fields.
3. **Enforce invariants at creation time** — the most important reason.

### 4.1.1 Entity Factories

A hair-salon booking factory that enforces business hours at creation time:

```go
package chapter4

import (
    "errors"
    "time"

    "github.com/google/uuid"
)

type Booking struct {
    id             uuid.UUID
    from           time.Time
    to             time.Time
    hairDresserID  uuid.UUID
}

func CreateBooking(from, to time.Time, hairDresserID uuid.UUID) (*Booking, error) {
    closingTime, _ := time.Parse(time.Kitchen, "17:00pm")
    if from.After(closingTime) {
        return nil, errors.New("no appointments after closing time")
    }
    return &Booking{
        hairDresserID: hairDresserID,
        id:            uuid.New(),
        from:          from,
        to:            to,
    }, nil
}
```

### 4.1.2 Should the Factory Generate the ID?

Two camps. Both are valid. **Default:** let the factory generate it unless the business requires otherwise (e.g., ID is supplied by an external system for idempotency).

## 4.2 Repository Pattern

A **repository** contains the logic to talk to a data source (database, S3 bucket, file system, third-party API). Putting it behind an interface centralises access and decouples the domain from the storage technology. This is what enables "we're switching from MySQL to Postgres" to be a small project instead of a re-architecture.

> "Some developers query the database using other channels (such as CQRS). This can work, since queries should not change state of the database, but if you are just starting, ensuring that all interactions with the database happen in the repository layer is recommended." — Matthew Boyle

### 4.2.1 One Repository Per Aggregate — NOT Per Table

The most common repository mistake. The book is explicit: **one repository per aggregate**, not per database table. A single repository call can write to multiple tables because the aggregate is the transactional unit.

### 4.2.2 Booking Repository Interface (Domain Side)

```go
type BookingRepository interface {
    SaveBooking(ctx context.Context, booking Booking) error
    DeleteBooking(ctx context.Context, booking Booking) error
}
```

### 4.2.3 Postgres Implementation (Infrastructure Side)

```go
type PostgresRepository struct {
    connPool *pgx.Conn
}

func NewPostgresRepository(ctx context.Context, dbConnString string) (*PostgresRepository, error) {
    conn, err := pgx.Connect(ctx, dbConnString)
    if err != nil {
        return nil, fmt.Errorf("failed to connect to db: %w", err)
    }
    defer conn.Close(ctx)
    return &PostgresRepository{connPool: conn}, nil
}

func (p PostgresRepository) SaveBooking(ctx context.Context, booking Booking) error {
    _, err := p.connPool.Exec(
        ctx,
        "INSERT into bookings (id, from, to, hair_dresser_id) VALUES ($1,$2,$3,$4)",
        booking.id.String(),
        booking.from.String(),
        booking.to.String(),
        booking.hairDresserID.String(),
    )
    if err != nil {
        return fmt.Errorf("failed to SaveBooking: %w", err)
    }
    return nil
}

func (p PostgresRepository) DeleteBooking(ctx context.Context, booking Booking) error {
    _, err := p.connPool.Exec(
        ctx,
        "DELETE from bookings WHERE id = $1",
        booking.id,
    )
    if err != nil {
        return fmt.Errorf("failed to DeleteBooking: %w", err)
    }
    return nil
}
```

Every interaction with the database happens here. Domain logic stays in the domain layer.

## 4.3 Services

| Service kind                  | Owns                                                  | Depends on                                  | Domain logic?            |
|-------------------------------|-------------------------------------------------------|---------------------------------------------|--------------------------|
| **Domain service**            | Significant business logic, multi-object              | Entities, value objects, repositories       | Yes                      |
| **Application service**       | Composition, transactions, authorisation              | Domain services, repositories, infrastructure | No — thin coordinator   |
| **Infrastructure service**    | External system concerns (email, payment, analytics)  | SDK of the external system                  | No — keep external logic contained |

### 4.3.1 Domain Services

Use when business logic spans multiple entities, when you transform one domain object into another, or when you compute a value from properties of multiple objects.

The book's example — a `Product` with a `CanBeBought()` method that depends on cart state, implemented naively:

```go
package chapter4

type Product struct {
    ID              int
    InStock         bool
    InSomeonesCart  bool
}

func (p *Product) CanBeBought() bool {
    return p.InStock && !p.InSomeonesCart
}

type ShoppingCart struct {
    ID          int
    Products    []Product
    IsFull      bool
    MaxCartSize int
}

func (s *ShoppingCart) AddToCart(p Product) bool {
    if s.IsFull {
        return false
    }
    if p.CanBeBought() {
        s.Products = append(s.Products, p)
        return true
    }
    if s.MaxCartSize == len(s.Products) {
        s.IsFull = true
    }
    return true
}
```

The smell: `ShoppingCart` references `Product` and adds business logic that isn't really the cart's concern. Move the cross-aggregate logic into a `CheckoutService`:

```go
package chapter4

import "errors"

type CheckoutService struct {
    shoppingCart *ShoppingCart
}

func NewCheckoutService(shoppingCart *ShoppingCart) *CheckoutService {
    return &CheckoutService{shoppingCart: shoppingCart}
}

func (c CheckoutService) AddProductToBasket(p *Product) error {
    if c.shoppingCart.IsFull {
        return errors.New("cannot add to cart, its full")
    }
    if p.CanBeBought() {
        c.shoppingCart.Products = append(c.shoppingCart.Products, *p)
        return nil
    }
    if c.shoppingCart.MaxCartSize == len(c.shoppingCart.Products) {
        c.shoppingCart.IsFull = true
    }
    return nil
}
```

A domain service is the right home for orchestration that does not fit any single entity. It is **stateless** (no per-call instance state) and expressed in ubiquitous language.

### 4.3.2 Application Services

Thin coordinators. They compose domain services and repositories, manage transactions, and handle cross-cutting concerns (security, observability, request validation that does not belong in the domain).

```go
package chapter4

import (
    "context"
    "errors"
    "fmt"

    "github.com/PacktPublishing/Domain-Driven-Design-with-GoLang/chapter2"
)

type accountKey = int
const accountCtxKey = accountKey(1)

type BookingDomainService interface {
    CreateBooking(ctx context.Context, booking Booking) error
}

type BookingAppService struct {
    bookingRepo         BookingRepository
    bookingDomainService BookingDomainService
}

func NewBookingAppService(bookingRepo BookingRepository, bookingDomainService BookingDomainService) *BookingAppService {
    return &BookingAppService{
        bookingRepo:         bookingRepo,
        bookingDomainService: bookingDomainService,
    }
}

func (b *BookingAppService) CreateBooking(ctx context.Context, booking Booking) error {
    u, ok := ctx.Value(accountCtxKey).(*chapter2.Customer)
    if !ok {
        return errors.New("invalid customer")
    }
    if u.UserID() != booking.userID.String() {
        return errors.New("cannot create booking for other users")
    }
    if err := b.bookingDomainService.CreateBooking(ctx, booking); err != nil {
        return fmt.Errorf("could not create booking: %w", err)
    }
    if err := b.bookingRepo.SaveBooking(ctx, booking); err != nil {
        return fmt.Errorf("could not save booking: %w", err)
    }
    return nil
}
```

Anatomy:

1. **Authorisation** at the top — application layer's job.
2. **Delegate** to the domain service for the business rules.
3. **Persist** via the repository.
4. **Return** an aggregate error if any step failed.

Application services are also where you compose multiple domain services for a UI screen or an RPC handler. Think of them as the "use case orchestrators."

### 4.3.3 Infrastructure Services

Wrap anything external — email, payment, analytics. Always behind an interface so the domain doesn't know.

```go
package chapter4

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"
)

type EmailSender interface {
    SendEmail(ctx context.Context, to string, title string, body string) error
}

const emailURL = "https://mandrillapp.com/api/1.0/messages/send"

type MailChimp struct {
    apiKey     string
    from       string
    httpClient http.Client
}

type MailChimpReqBody struct {
    Key     string `json:"key"`
    Message struct {
        FromEmail string `json:"from_email"`
        Subject   string `json:"subject"`
        Text      string `json:"text"`
        To        []struct {
            Email string `json:"email"`
            Type  string `json:"type"`
        } `json:"to"`
    } `json:"message"`
}

func NewMailChimp(apiKey string, from string, httpClient http.Client) *MailChimp {
    return &MailChimp{apiKey: apiKey, from: from, httpClient: httpClient}
}

func (m MailChimp) SendEmail(ctx context.Context, to string, title string, body string) error {
    bod := MailChimpReqBody{
        Key: m.apiKey,
        Message: struct {
            FromEmail string `json:"from_email"`
            Subject   string `json:"subject"`
            Text      string `json:"text"`
            To []struct {
                Email string `json:"email"`
                Type  string `json:"type"`
            } `json:"to"`
        }{
            FromEmail: m.from,
            Subject:   title,
            Text:      body,
            To: []struct {
                Email string `json:"email"`
                Type  string `json:"type"`
            }{{Email: to, Type: "to"}},
        },
    }
    b, err := json.Marshal(bod)
    if err != nil {
        return fmt.Errorf("failed to marshall body: %w", err)
    }
    req, err := http.NewRequest(http.MethodPost, emailURL, bytes.NewReader(b))
    if err != nil {
        return fmt.Errorf("failed to create request: %w", err)
    }
    if _, err := m.httpClient.Do(req); err != nil {
        return fmt.Errorf("failed to send email: %w", err)
    }
    return nil
}
```

Wire the sender into the application service:

```go
type BookingAppService struct {
    bookingRepo          BookingRepository
    bookingDomainService BookingDomainService
    emailService         EmailSender
}
```

And call it from `CreateBooking` — wrapping the email send with `if err := ...; err != nil` (handle as fits your use case).

End-state: created → saved → email fired. Single use case, three collaborators, all behind interfaces.

## 4.4 Chapter 4 Summary — Service Decision Tree

```
Does this behaviour belong to ONE entity?
   ├─ Yes → put it on the entity
   └─ No
       ├─ Core business logic spanning multiple aggregates? → Domain service
       ├─ Composing domain services / repositories / handling auth? → Application service
       └─ Calling an external system (email, payment, analytics)? → Infrastructure service
```

---

# PART 2 — REAL-WORLD DDD WITH GOLANG

# Chapter 5 — Applying DDD to a Monolithic Application (CoffeeCo)

Complete DDD coffee-shop chain, built from a narrative: identify language, sketch domains, build entities/value objects, layer services and infrastructure services.

## 5.1 What Is a Monolith?

A monolithic application packs the UI, all domains, and infrastructure services into a single deployable unit.

**Pros:** simple to develop, deploy, scale (one binary); single deployment mental model.
**Cons:** slow startup at scale; all-or-nothing scaling; deployments slow over time; partial-failure cascades; long-term tech-stack lock-in; modularity blurs — exactly where DDD helps.

## 5.2 Setting the Scene — CoffeeCo

CoffeeCo is a national coffee chain with 50 new stores in the last year. Two pertinent systems:

- **CoffeeBux loyalty** — 1 free drink per 10 purchased across any store.
- **Online store / monthly subscription** — being scoped.

Domain modelling session outputs (verbatim from the book):

**Ubiquitous language:**

- *Coffee lovers* — what CoffeeCo calls its customers.
- *CoffeeBux* — the loyalty program. 1 CoffeeBux per drink or accessory purchased.
- *Tiny, medium, massive* — drink sizes in ascending order. Some drinks are one size, others are all three.

**Identified sub-domains:** Store, Products, Loyalty, Subscription.

**MVP feature list:**

- Purchase drink/accessory using CoffeeBux.
- Purchase drink/accessory with debit/credit card.
- Purchase drink/accessory with cash.
- Earn CoffeeBux on purchases.
- Store-specific (but not national) discounts.
- All purchases in USD for now; multi-currency later.
- Drinks in one size for now.

## 5.3 Getting Started — Project Skeleton

The author uses Go's `internal/` convention — anything under `internal/` cannot be imported by other modules. This is exactly the boundary DDD wants.

`internal/coffeelover.go`:

```go
package coffeeco

import "github.com/google/uuid"

type CoffeeLover struct {
    ID           uuid.UUID
    FirstName    string
    LastName     string
    EmailAddress string
}
```

The fields (FirstName, LastName, EmailAddress) were added only after talking to the domain experts. **Talk to your stakeholders first.**

`internal/store/store.go`:

```go
package store

import "github.com/google/uuid"

type Store struct {
    ID       uuid.UUID
    Location string
}
```

(Note: the book exports `ID` and `Location` even though lowercase fields would follow the value-object rule. We follow the book verbatim.)

`internal/coffeeco/product.go`:

```go
package coffeeco

import "github.com/Rhymond/go-money"

type Product struct {
    ItemName  string
    BasePrice money.Money
}
```

Back in `internal/store/store.go`:
    Location        string
    ProductsForSale []coffeeco.Product
}
```

`internal/purchase/purchase.go` (initial draft):

```go
package purchase

import (
    "github.com/Rhymond/go-money"
    "github.com/google/uuid"

    coffeeco "coffeeco/internal"
    "coffeeco/internal/store"
)

type Purchase struct {
    id                 uuid.UUID
    Store              store.Store
    ProductsToPurchase []coffeeco.Product
    total              money.Money
    PaymentMeans       payment.Means
    timeOfPurchase     time.Time
}
```

`internal/payment/means.go`:

```go
package payment

type Means string

const (
    MEANS_CARD      = "card"
    MEANS_CASH      = "cash"
    MEANS_COFFEEBUX = "coffeebux"
)

type CardDetails struct {
    cardToken string
}
```

Purchase gets a card token pointer:

```go
type Purchase struct {
    id                 uuid.UUID
    Store              store.Store
    ProductsToPurchase []coffeeco.Product
    total              money.Money
    PaymentMeans       payment.Means
    timeOfPurchase     time.Time
    CardToken          *string
}
```

`internal/loyalty/coffeebux.go`:

```go
package loyalty

import (
    "github.com/google/uuid"

    coffeeco "coffeeco/internal"
    "coffeeco/internal/store"
)

type CoffeeBux struct {
    ID                                     uuid.UUID
    store                                  store.Store
    coffeeLover                            coffeeco.CoffeeLover
    FreeDrinksAvailable                    int
    RemainingDrinkPurchasesUntilFreeDrink  int
}
```

### 5.3.1 Validation-as-Behaviour on the Purchase Aggregate

```go
func (p *Purchase) validateAndEnrich() error {
    if len(p.ProductsToPurchase) == 0 {
        return errors.New("purchase must consist of at least one product")
    }
    p.total = *money.New(0, "USD")
    for _, v := range p.ProductsToPurchase {
        newTotal, _ := p.total.Add(&v.BasePrice)
        p.total = *newTotal
    }
    if p.total.IsZero() {
        return errors.New("likely mistake; purchase should never be 0. Please validate")
    }
    p.id = uuid.New()
    p.timeOfPurchase = time.Now()
    return nil
}
```

Three DDD lessons: pointer receiver (mutates missing values); initialise to zero USD (currency-extensible); mutate-fill (caller supplies inputs, aggregate fills defaults).

### 5.3.2 The First Service

```go
type CardChargeService interface {
    ChargeCard(ctx context.Context, amount money.Money, cardToken string) error
}

type Service struct {
    cardService  CardChargeService
    purchaseRepo Repository
}

func (s Service) CompletePurchase(ctx context.Context, purchase *Purchase) error {
    if err := purchase.validateAndEnrich(); err != nil {
        return err
    }
    switch purchase.PaymentMeans {
    case payment.MEANS_CARD:
        if err := s.cardService.ChargeCard(ctx, purchase.total, *purchase.cardToken); err != nil {
            return errors.New("card charge failed, cancelling purchase")
        }
    case payment.MEANS_CASH:
        // TODO: For the reader to add :)
    default:
        return errors.New("unknown payment type")
    }
    if err := s.purchaseRepo.Store(ctx, *purchase); err != nil {
        return errors.New("failed to store purchase")
    }
    return nil
}
```

Architectural move: `CardChargeService` is an **interface defined in the purchase package**. The payments team writes the Stripe implementation independently; the purchase team does not wait. `Repository` likewise:

```go
package purchase

import "context"

type Repository interface {
    Store(ctx context.Context, purchase Purchase) error
}
```

Interface in the domain package; concrete impl elsewhere.

## 5.4 MongoDB Product Repository

CoffeeCo uses Mongo (the team has experience; the schema is flexible). (The book's "product repository" heading actually denotes the Purchase Mongo repo.)

```go
type MongoRepository struct {
    purchases *mongo.Collection
}

func NewMongoRepo(ctx context.Context, connectionString string) (*MongoRepository, error) {
    client, err := mongo.Connect(ctx, options.Client().ApplyURI(connectionString))
    if err != nil {
        return nil, fmt.Errorf("failed to create a mongo client: %w", err)
    }
    purchases := client.Database("coffeeco").Collection("purchases")
    return &MongoRepository{purchases: purchases}, nil
}

func (mr *MongoRepository) Store(ctx context.Context, purchase Purchase) error {
    mongoP := New(purchase)
    _, err := mr.purchases.InsertOne(ctx, mongoP)
    if err != nil {
        return fmt.Errorf("failed to persist purchase: %w", err)
    }
    return nil
}
```

The translation function decouples domain from storage:

```go
type mongoPurchase struct {
    id                 uuid.UUID
    store              store.Store
    productsToPurchase []coffeeco.Product
    total              money.Money
    paymentMeans       payment.Means
    timeOfPurchase     time.Time
    cardToken          *string
}

func toMongoPurchase(p Purchase) mongoPurchase {
    return mongoPurchase{
        id:                 p.id,
        store:              p.Store,
        productsToPurchase: p.ProductsToPurchase,
        total:              p.total,
        paymentMeans:       p.PaymentMeans,
        timeOfPurchase:     p.timeOfPurchase,
        cardToken:          p.cardToken,
    }
}
```

Apply the same pattern in reverse for query paths (left as an exercise).

## 5.5 Stripe Payment Infrastructure Service

```go
package payment

import (
    "context"
    "errors"
    "fmt"

    "github.com/Rhymond/go-money"
    "github.com/stripe/stripe-go/v73"
    "github.com/stripe/stripe-go/v73/charge"
    "github.com/stripe/stripe-go/v73/client"
)

type StripeService struct {
    stripeClient *client.API
}

func NewStripeService(apiKey string) (*StripeService, error) {
    if apiKey == "" {
        return nil, errors.New("API key cannot be nil ")
    }
    sc := &client.API{}
    sc.Init(apiKey, nil)
    return &StripeService{stripeClient: sc}, nil
}

func (s StripeService) ChargeCard(ctx context.Context, amount money.Money, cardToken string) error {
    params := &stripe.ChargeParams{
        Amount:   stripe.Int64(amount.Amount()),
        Currency: stripe.String(string(stripe.CurrencyUSD)),
        Source:   &stripe.PaymentSourceSourceParams{Token: stripe.String(cardToken)},
    }
    _, err := charge.New(params)
    if err != nil {
        return fmt.Errorf("failed to create a charge:%w", err)
    }
    return nil
}
```

Interface satisfaction:

```go
type CardChargeService interface {
    ChargeCard(ctx context.Context, amount money.Money, cardToken string) error
}
```

CoffeeCo could swap Stripe for Square with no domain changes.

## 5.6 Paying with CoffeeBux

Add `AddStamp()` to the loyalty card:

```go
func (c *CoffeeBux) AddStamp() {
    if c.RemainingDrinkPurchasesUntilFreeDrink == 1 {
        c.RemainingDrinkPurchasesUntilFreeDrink = 10
        c.FreeDrinksAvailable += 1
    } else {
        c.RemainingDrinkPurchasesUntilFreeDrink--
    }
}
```

Update the purchase service signature:

```go
func (s Service) CompletePurchase(ctx context.Context, purchase *Purchase, coffeeBuxCard *loyalty.CoffeeBux) error {
    if err := purchase.validateAndEnrich(); err != nil {
        return err
    }
    switch purchase.PaymentMeans {
    case payment.MEANS_CARD:
        if err := s.cardService.ChargeCard(ctx, purchase.total, *purchase.cardToken); err != nil {
            return errors.New("card charge failed, cancelling purchase")
        }
    case payment.MEANS_CASH:
        // For the reader to add :)
    default:
        return errors.New("unknown payment type")
    }
    if err := s.purchaseRepo.Store(ctx, *purchase); err != nil {
        return errors.New("failed to store purchase")
    }
    if coffeeBuxCard != nil {
        coffeeBuxCard.AddStamp()
    }
    return nil
}
```

CoffeeBux needs a `Pay` method (loyalty now participates in payments):

```go
func (c *CoffeeBux) Pay(ctx context.Context, purchases []purchase.Purchase) error {
    lp := len(purchases)
    if lp == 0 {
        return errors.New("nothing to buy")
    }
    if c.FreeDrinksAvailable < lp {
        return fmt.Errorf("not enough coffeeBux to cover entire purchase. Have %d, need %d", len(purchases), c.FreeDrinksAvailable)
    }
    c.FreeDrinksAvailable = c.FreeDrinksAvailable - lp
    return nil
}
```

Wired into the service (only the new case shown):

```go
case payment.MEANS_COFFEEBUX:
    if err := coffeeBuxCard.Pay(ctx, purchase.ProductsToPurchase); err != nil {
        return fmt.Errorf("failed to charge loyalty card: %w", err)
    }
```

A subtle bug: **paying with CoffeeBux still earns a stamp.** Domain-expert answer required.

## 5.7 Store-Specific Discounts
`internal/store/repository.go`:

```go
package store

import (
    "context"
    "errors"
    "fmt"

    "github.com/google/uuid"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

var ErrNoDiscount = errors.New("no discount for store")

type Repository interface {
    GetStoreDiscount(ctx context.Context, storeID uuid.UUID) (int, error)
}

type MongoRepository struct {
    storeDiscounts *mongo.Collection
}

func NewMongoRepo(ctx context.Context, connectionString string) (*MongoRepository, error) {
    client, err := mongo.Connect(ctx, options.Client().ApplyURI(connectionString))
    if err != nil {
        return nil, fmt.Errorf("failed to create a mongo client: %w", err)
    }
    discounts := client.Database("coffeeco").Collection("store_discounts")
    return &MongoRepository{storeDiscounts: discounts}, nil
}

func (m MongoRepository) GetStoreDiscount(ctx context.Context, storeID uuid.UUID) (float32, error) {
    var discount float32
    if err := m.storeDiscounts.FindOne(ctx, bson.D{{"store_id", storeID.String()}}).Decode(&discount); err != nil {
        if err == mongo.ErrNoDocuments {
            return 0, ErrNoDiscount
        }
        return 0, fmt.Errorf("failed to find discount for store: %w", err)
    }
    return discount, nil
}
```

Distinguishing the "this is not an error" case (no discount) from a real error is a common Go pattern — use a sentinel error like `ErrNoDiscount` so callers can `==` against it.

In the purchase service:

```go
type StoreService interface {
    GetStoreSpecificDiscount(ctx context.Context, storeID uuid.UUID) (float32, error)
}

type Service struct {
    cardService  CardChargeService
    purchaseRepo Repository
    storeService StoreService
}
```

Add a `storeID` to `CompletePurchase` and use the discount. Refactor the discount into its own method:

```go
func (s Service) CompletePurchase(ctx context.Context, storeID uuid.UUID, purchase *Purchase, coffeeBuxCard *loyalty.CoffeeBux) error {
    if err := purchase.validateAndEnrich(); err != nil {
        return err
    }
    if err := s.calculateStoreSpecificDiscount(ctx, storeID, purchase); err != nil {
        return err
    }
    switch purchase.PaymentMeans {
    case payment.MEANS_CARD:
        if err := s.cardService.ChargeCard(ctx, purchase.total, *purchase.cardToken); err != nil {
            return errors.New("card charge failed, cancelling purchase")
        }
    case payment.MEANS_CASH:
        // For the reader to add :)
    case payment.MEANS_COFFEEBUX:
        if err := coffeeBuxCard.Pay(ctx, purchase.ProductsToPurchase); err != nil {
            return fmt.Errorf("failed to charge loyatly card: %w", err)
        }
    default:
        return errors.New("unknown payment type")
    }
    if err := s.purchaseRepo.Store(ctx, *purchase); err != nil {
        return errors.New("failed to store purchase")
    }
    if coffeeBuxCard != nil {
        coffeeBuxCard.AddStamp()
    }
    return nil
}

func (s *Service) calculateStoreSpecificDiscount(ctx context.Context, storeID uuid.UUID, purchase *Purchase) error {
    discount, err := s.storeService.GetStoreSpecificDiscount(ctx, storeID)
    if err != nil && err != store.ErrNoDiscount {
        return fmt.Errorf("failed to get discount: %w", err)
    }
    purchasePrice := purchase.total
    if discount > 0 {
        purchase.total = *purchasePrice.Multiply(int64(100 - discount))
    }
    return nil
}
```

When discount logic grows (loyalty tiering, time-of-day rules, store-specific stamps), this function is the natural extension point.

Implement the `StoreService`:

```go
type Service struct {
    repo Repository
}

func (s Service) GetStoreSpecificDiscount(ctx context.Context, storeID uuid.UUID) (float32, error) {
    dis, err := s.repo.GetStoreDiscount(ctx, storeID)
    if err != nil {
        return 0, err
    }
    return float32(dis), nil
}
```

## 5.8 Applying DDD to an Existing Monolith

For a legacy codebase:

1. Start with **domain-expert relationships**. Co-author the ubiquitous language even if you don't change a line of code. Future conversations get dramatically better.
2. Even without repository/domain-object refactors, **decouple infrastructure from specific vendors**. Replacing Stripe later is a small change if your code talks to a `CardChargeService` interface today.
3. Pick the highest-pain area, refactor there, ship, repeat.

## 5.9 Chapter 5 Summary — Monolith Checklist

- [ ] Use `internal/` for the domain.
- [ ] Decide entities first, then value objects.
- [ ] Use `go-money` for currency (never `float`).
- [ ] Use UUIDs.
- [ ] Define repository as an interface in the domain package.
- [ ] One repository per aggregate.
- [ ] Use sentinel errors (`ErrNoDiscount`) for "not-found but not-an-error" cases.
- [ ] Stripe / MailChimp / etc. live behind interfaces as infrastructure services.
- [ ] Push business logic *down* into the entity, leaving the service thin.

---

# Chapter 6 — Building a Microservice Using DDD

A focused service (travel-recommendation) that depends on a temperamental "partnerships" service in another team. Three lessons: keep the domain clean, use anti-corruption layers at the boundary, expect failure.

## 6.1 Microservices in One Sentence

Small, independently deployable services with their own databases that talk via RPC. They are as much an organisational decision as a technical one.

### 6.1.1 Benefits

Velocity, flexible scaling, smaller deployments, technology freedom per service, adoptable resilience.

### 6.1.2 Downsides

Distributed systems expertise required; broader skillset (Kubernetes, networking, latency budgets); harder end-to-end testing, especially with events.

### 6.1.3 Adoption Questions

Distributed-systems expertise (or a hiring/training plan)? Observability tooling? Platform (Kubernetes or otherwise)? Who owns each service's CI/CD? Leadership time + budget?

## 6.2 The Scenario

The recommendation team (you) needs to expose an API; they depend on the partnership team for hotel availability. The partnership team has been clear:

- Auth via password in `Authorization` header.
- 400 for bad request, 401 for bad auth, 500 for sporadic failures.
- 30% of requests fail; partnership system will be rebuilt soon.

Published language sample response:

```json
{
  "availableHotels": [
    {"name": "hotel1_name", "priceInUSDPerNight": 500},
    {"name": "hotel2_name", "priceInUSDPerNight": 300}
  ]
}
```

ISO-3166 Alpha 3 country codes; ISO-8601 dates.

## 6.3 Recommendation Domain Model

`recommendation.go`:

```go
type Recommendation struct {
    TripStart  time.Time
    TripEnd    time.Time
    HotelName  string
    Location   string
    TripPrice  money.Money
}

type Option struct {
    HotelName     string
    Location      string
    PricePerNight money.Money
}

type AvailabilityGetter interface {
    GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error)
}
```

`AvailabilityGetter` is described in **our** language. The partnership system's model never enters the domain.

`Service`:

```go
type Service struct {
    availability AvailabilityGetter
}

func NewService(availability AvailabilityGetter) (*Service, error) {
    if availability == nil {
        return nil, errors.New("availability must not be nil")
    }
    return &Service{availability: availability}, nil
}

func (svc *Service) Get(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string, budget money.Money) (*Recommendation, error) {
    switch {
    case tripStart.IsZero():
        return nil, errors.New("trip start cannot be empty")
    case tripEnd.IsZero():
        return nil, errors.New("trip end cannot be empty")
    case location == "":
        return nil, errors.New("location cannot be empty")
    }
    return nil, nil
}
```

Calculate cheapest viable trip:

```go
opts, err := svc.availability.GetAvailability(ctx, tripStart, tripEnd, location)
if err != nil {
    return nil, fmt.Errorf("error getting availability: %w", err)
}

tripDuration := math.Round(tripEnd.Sub(tripStart).Hours() / 24)
lowestPrice := money.NewFromFloat(999999999, "USD")
var cheapestTrip *Option
for _, option := range opts {
    price := option.PricePerNight.Multiply(int64(tripDuration))
    if ok, _ := price.GreaterThan(budget); ok {
        continue
    }
    if ok, _ := price.LessThan(lowestPrice); ok {
        lowestPrice = price
        cheapestTrip = &option
    }
}
if cheapestTrip == nil {
    return nil, errors.New("no trips within budget")
}
return &Recommendation{
    TripStart:  tripStart,
    TripEnd:    tripEnd,
    HotelName:  cheapestTrip.HotelName,
    Location:   cheapestTrip.Location,
    TripPrice:  *lowestPrice,
}, nil
```

Domain language all the way through.

## 6.4 Anti-Corruption Layer — PartnershipAdaptor

`adapter.go`:

```go
type PartnershipAdaptor struct {
    client *http.Client
    url    string
}

func NewPartnerShipAdaptor(client *http.Client, url string) (*Client, error) {
    if client == nil {
        return nil, errors.New("client cannot be nil")
    }
    if url == "" {
        return nil, errors.New("url cannot be empty")
    }
    return &Client{client: client, url: url}, nil
}

func (p PartnershipAdaptor) GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error) {
    return nil, nil
}
```

Stub first; iterate:

```go
func (p PartnershipAdaptor) GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error) {
    from := fmt.Sprintf("%d-%d-%d", tripStart.Year(), tripStart.Month(), tripStart.Day())
    to := fmt.Sprintf("%d-%d-%d", tripEnd.Year(), tripEnd.Month(), tripEnd.Day())
    url := fmt.Sprintf("%s/partnerships?location=%s&from=%s&to=%s", p.url, location, from, to)
    res, err := p.client.Get(url)
    if err != nil {
        return nil, fmt.Errorf("failed to call partnerships: %w", err)
    }
    defer res.Body.Close()
    if res.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("bad request to partnerships: %d", res.StatusCode)
    }
}
```

Decode into a private struct so the partnership schema never leaks:

```go
type partnerShipsResponse struct {
    AvailableHotels []struct {
        Name              string `json:"name"`
        PriceInUSDPerNight int   `json:"priceInUSDPerNight"`
    } `json:"availableHotels"`
}

var pr partnerShipsResponse
if err := json.NewDecoder(res.Body).Decode(&pr); err != nil {
    return nil, fmt.Errorf("could not decode the response body of partnerships: %w", err)
}
```

Translate to the domain's `[]Option`:

```go
opts := make([]Option, len(pr.AvailableHotels))
for i, p := range pr.AvailableHotels {
    opts[i] = Option{
        HotelName:    p.Name,
        Location:     location,
        PricePerNight: *money.New(int64(p.PriceInUSDPerNight), "USD"),
    }
}
return opts, nil
```

Whole function (verbatim; note the URL typo `?from=%s?to=%s` in the source — both `?` separators are wrong):

```go
func (p PartnershipAdaptor) GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error) {
    res, err := p.client.Get(fmt.Sprintf("%s/partnerships?location=%s?from=%s?to=%s ", p.url, location, tripStart, tripEnd))
    if err != nil {
        return nil, fmt.Errorf("failed to call partnerships: %w", err)
    }
    defer res.Body.Close()
    var pr partnerShipsResponse
    if err := json.NewDecoder(res.Body).Decode(&pr); err != nil {
        return nil, fmt.Errorf("could not decode the response body of partnerships: %w", err)
    }
    opts := make([]Option, len(pr.AvailableHotels))
    for i, p := range pr.AvailableHotels {
        opts[i] = Option{
            HotelName:    p.Name,
            Location:     location,
            PricePerNight: *money.New(int64(p.PriceInUSDPerNight), "USD"),
        }
    }
    return opts, nil
}
```

When the partnership team ships their new API, **only this file changes**.

## 6.5 Exposing the Service — Open Host Service

The recommendation service must also expose its API:

```
GET /recommendation?location={country}&from={YYYY-MM-DD}&to={YYYY-MM-DD}&budget={cents}
→ {"hotelName": "...", "totalCost": {"cost": 300, "currency": "USD"}}
```

```go
type Handler struct {
    svc Service
}

func NewHandler(svc Service) (*Handler, error) {
    if svc == (Service{}) {
        return nil, errors.New("service cannot be empty")
    }
    return &Handler{svc: svc}, nil
}

type GetRecommendationResponse struct {
    HotelName string `json:"hotelName"`
    TotalCost struct {
        Cost     int64  `json:"cost"`
        Currency string `json:"currency"`
    } `json:"totalCost"`
}
```

The handler validates inputs and converts types before calling the domain:

```go
func (h Handler) GetRecommendation(w http.ResponseWriter, req *http.Request) {
    q := mux.Vars(req)
    location, ok := q["location"]
    if !ok {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    from, ok := q["from"]
    if !ok {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    to, ok := q["to"]
    if !ok {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    budget, ok := q["budget"]
    if !ok {
        w.WriteHeader(http.StatusBadRequest)
        return
    }

    const expectedFormat = "2006-01-02"
    formattedStart, err := time.Parse(expectedFormat, from)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    formattedEnd, err := time.Parse(expectedFormat, to)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        return
    }

    b, err := strconv.ParseInt(budget, 10, 64)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    budgetMon := money.New(b, "USD")

    rec, err := h.svc.Get(req.Context(), formattedStart, formattedEnd, location, budgetMon)
    if err != nil {
        w.WriteHeader(http.StatusInternalServerError)
        return
    }
    res, err := json.Marshal(GetRecommendationResponse{
        HotelName: rec.HotelName,
        TotalCost: struct {
            Cost     int64  `json:"cost"`
            Currency string `json:"currency"`
        }{
            Cost:     rec.TripPrice.Amount(),
            Currency: "USD",
        },
    })
    if err != nil {
        w.WriteHeader(http.StatusInternalServerError)
        return
    }
    w.WriteHeader(http.StatusOK)
    _, _ = w.Write(res)
    return
}
```

A separate `transport` package keeps HTTP details out of the domain:

```go
package transport

import (
    "net/http"

    "github.com/gorilla/mux"
    "github.com/PacktPublishing/Domain-Driven-Design-with-GoLang/chapter6/recommendation/internal/recommendation"
)

func NewMux(recHandler recommendation.Handler) *mux.Router {
    m := mux.NewRouter()
    m.HandleFunc("/recommendation", recHandler.GetRecommendation).Methods(http.MethodGet)
    return m
}
```

## 6.6 Resilient HTTP With go-retryablehttp

Partnerships will fail 30% of the time. HashiCorp's `retryablehttp` handles that transparently:

```go
package main

import (
    "log"
    "net/http"

    "github.com/hashicorp/go-retryablehttp"
    "github.com/PacktPublishing/Domain-Driven-Design-with-GoLang/chapter6/recommendation/internal/recommendation"
    "github.com/PacktPublishing/Domain-Driven-Design-with-GoLang/chapter6/recommendation/internal/transport"
)

func main() {
    c := retryablehttp.NewClient()
    c.RetryMax = 10

    partnerAdaptor, err := recommendation.NewPartnerShipAdaptor(
        c.StandardClient(),
        "http://localhost:3031",
    )
    if err != nil {
        log.Fatal("failed to create a partnerAdaptor: ", err)
    }

    svc, err := recommendation.NewService(partnerAdaptor)
    if err != nil {
        log.Fatal("failed to create a service: ", err)
    }
    handler, err := recommendation.NewHandler(*svc)
    if err != nil {
        log.Fatal("failed to create a handler: ", err)
    }

    m := transport.NewMux(*handler)
    if err := http.ListenAndServe(":4040", m); err != nil {
        log.Fatal("server errored: ", err)
    }
}
```

The retryable client retries 5xx by default. Tune `RetryMax`, backoff strategy, and which status codes trigger a retry. The domain code stays oblivious.

Call from the host:

```bash
curl --location --request GET 'http://localhost:4040/recommendation?location=UK&from=2022-09-01&to=2022-09-08&budget=5000'
```

Response:
```json
{
  "hotelName": "some fourth hotel",
  "totalCost": {"cost": 210, "currency": "USD"}
}
```

## 6.7 Chapter 6 Summary — Microservice Checklist

- [ ] Define domain interfaces in **your** language; do not import the partner's vocabulary.
- [ ] Put anti-corruption logic in its own file/package; make it the *only* place that knows the partner's schema.
- [ ] Fail fast at the transport boundary; do not push parse failures into the domain.
- [ ] Use a separate `transport/` package (or equivalent) for HTTP handlers.
- [ ] Plan for partner failure from day one: retries with exponential backoff.
- [ ] Use `go-retryablehttp` or equivalent for transient-failure tolerance.
- [ ] Co-locate each service's contract, domain, infrastructure adaptors, and `main.go` (`cmd/`).

---

# Chapter 7 — DDD for Distributed Systems

Once you have multiple DDD services you have a distributed system. This chapter covers the practical bits: CAP, CQRS, EDA, 2PC, sagas, and message buses.

## 7.1 What Is a Distributed System?

Multiple computing components on a network coordinating for jobs no single machine could do. Common characteristics:

| Trait          | Description                                                          |
|----------------|----------------------------------------------------------------------|
| Scalable       | Grows up and down with workload                                      |
| Fault-tolerant | One component failing doesn't take the system down                   |
| Transparent    | Appears as a single unit to the user                                 |
| Concurrent     | Multiple activities simultaneously                                   |
| Heterogeneous  | Mixed OSes, languages, paradigms                                     |
| Replicated     | Data copied for redundancy                                           |

## 7.2 CAP Theorem and Databases

In a distributed store you can choose only two of three properties:

- **Consistency** — reads see the most recent write or an error.
- **Availability** — every request gets a non-error response.
- **Partition tolerance** — the system keeps operating despite network failures.

In practice, network partitions happen, so you choose between **CP** and **AP**:

### 7.2.1 MongoDB — CP

- Single primary; writes go to primary, replicated to secondaries.
- If primary dies, a secondary is promoted; during promotion the system is unavailable.
- Reads can hit secondaries (configurable) at the risk of seeing stale data.

### 7.2.2 Cassandra — AP

- No primary; write to any node.
- "Claimed to survive entire data-centre loss."
- Consistent hashing distributes data across a logical ring; nodes can come and go without rehashing the world.
- Trade-off: eventual consistency.

## 7.3 CQRS — Command Query Responsibility Segregation

Different read and write models. Commands mutate, queries read.

### 7.3.1 Rules for Go

- A method that mutates the receiver or the database **must** return only `error` (or `nil`).
- A method that returns a value **must not** mutate state or the database.

A bad interface attempt:

```go
type Commander interface {
    Command(ctx context.Context, args ...interface{}) error
}
type Querier interface {
    Question(ctx context.Context, args ...interface{}) (interface{}, error)
}
```

The author rejects this — Go's type system is bypassed and method names obscure intent. Let idiomatic Go signatures enforce CQRS.

### 7.3.2 When CQRS Helps

Event-sourced systems where commands emit events; heavy read workloads (separate denormalised read store); async pipelines where reads/writes have different SLAs. In monoliths the author rarely recommends CQRS unless implemented perfectly; in distributed DDD it is a natural fit.

## 7.4 Event-Driven Architecture

EDA: produce, detect, and respond to events. An event = a significant change in state.

```json
{"event_type": "user.logged_in", "user_id": "135649039"}
```

Events have a **header** (timestamp, source, message ID, sometimes correlation IDs) and a **body** (the change data, in JSON / Protobuf / Avro / Cap'n Proto). In DDD the interesting events are **domain events** (`user.loggedIn`, `purchase.failed`); other contexts can subscribe if they care.

Domain events can be pipelined:

```
addressesRequested → addressesValidated → addressesMatched → emailComposed → emailSent
```

Long-running tasks become observable stages. New requirements ("if `addressesMatched < 500`, take a lighter path") slot in by subscribing to existing events.

## 7.5 Dealing With Failure

### 7.5.1 Two-Phase Commit (2PC)

Coordinator asks each participant to **prepare** (locking resources). If all reply yes, the coordinator says **commit**. If any reply no, the coordinator says **abort**.

```
C  → A,B: prepare?
A  → C: yes
B  → C: yes
C  → A,B: commit
```

Properties: ✅ strong consistency if all cooperate; ❌ blocking (locks held until commit, surviving coordinator death), ❌ coordinator = SPOF, ❌ cannot scale to many participants.

### 7.5.2 The Saga Pattern

For each forward action, define a **compensating** action. Roll back completed steps if a later one fails.

A naive Go implementation:

```go
package chapter7

import "context"

type Saga interface {
    Execute(ctx context.Context) error
    Rollback(ctx context.Context) error
}

type OrderCreator struct{}

func (o OrderCreator) Execute(ctx context.Context) error {
    return o.createOrder(ctx)
}

func (o OrderCreator) Rollback(ctx context.Context) error {
    // Rollback Saga here
    return nil
}

func (o OrderCreator) createOrder(ctx context.Context) error {
    // Create Order here
    return nil
}

type PaymentCreator struct{}

func (p PaymentCreator) Execute(ctx context.Context) error {
    return p.createPayment(ctx)
}

func (p PaymentCreator) Rollback(ctx context.Context) error {
    // Rollback Saga here
    return nil
}

func (p PaymentCreator) createPayment(ctx context.Context) error {
    // Create payment here
    return nil
}

type SagaManager struct {
    actions []Saga
}

func (s SagaManager) Handle(ctx context.Context) {
    for i, action := range s.actions {
        if err := action.Execute(ctx); err != nil {
            for j := 0; j <= i; j++ {
                if err := s.actions[j].Rollback(ctx); err != nil {
                    // One of our compensation actions failed; we need to handle it (perhaps by emitting a message to a messagebus.)
                }
            }
        }
    }
}
```

Practical guidance: if a rollback fails, **emit an event** to a message bus — let downstream consumers retry at their pace. Don't try to be perfect synchronously; distributed systems are not synchronous.

## 7.6 Message Buses

| Tool      | Pros                                                              | Cons                                                          | When to reach for it                                 |
|-----------|-------------------------------------------------------------------|---------------------------------------------------------------|------------------------------------------------------|
| Kafka     | Millions of msgs/sec; rich features                               | Steep learning curve; easy to break ordering; hard to monitor | Event-sourced systems; large-scale event pipelines   |
| RabbitMQ  | Easy to start; AMQP; nice UI                                      | Doesn't scale as well; fewer features                         | Simpler queues; classic task queues                   |
| NATS      | Written in Go (readable); wildcard subjects; lightweight          | At-most-once delivery                                         | IoT; lowest-latency pub/sub where loss is OK         |

**Kafka topology:** brokers → topics → partitions; producers send; consumers subscribe (groups scale horizontally). Wrong partition key = out-of-order delivery.
**RabbitMQ topology:** producer → exchange → queue (routed by key) → consumer. Once consumed and acked the message is gone.
**NATS topology:** subjects instead of topics; wildcard subscriptions (`foo.*`); at-most-once only.

## 7.7 Chapter 7 Summary — Distributed Checklist

- [ ] Classify against CAP; pick the trade-off knowingly.
- [ ] CQRS when read/write models diverge; let idiomatic Go signatures enforce it.
- [ ] Each domain event is a stable published contract: schema, header, body.
- [ ] Sagas over 2PC; emit rollback-failure events for human review.
- [ ] Message bus by feature need, not fashion.
- [ ] Partner failure in every adapter; never trust a single network call.

---

# Chapter 8 — TDD, BDD, and DDD

Bonus chapter. TDD and BDD are not part of the DDD canon but are excellent complements.

## 8.1 TDD — Test-Driven Development

The TDD cycle:

1. **Add a test** — write the test from business requirements (user story or Given/When/Then) *before* any code.
2. **Run the test — it should fail** — proves the behaviour is missing, the test framework is alive, and the test cannot trivially pass.
3. **Write as little code as possible to pass** — spaghetti is welcome at this stage.
4. **Rerun all tests** — new and old, to prove no regressions.
5. **Refactor** — clean up; keep rerunning.

> "TDD and DDD are complementary patterns." — Matthew Boyle

### 8.1.1 The Ticket

> **Title:** As a customer, when I purchase a cookie, I get an email receipt.
>
> Acceptance criteria (Given/When/Then):
>
> - **Given** cookies in stock, **when** card is tapped, **then** charge + email receipt.
> - **Given** out of stock, **then** error so the cashier can apologise.
> - **Given** stock but card declined, **then** error so we can ban the customer.
> - **Given** charge succeeds but email fails, **then** notify cashier; transaction still complete.
> - **Given** requested > stock, **then** charge only for what's in stock.

### 8.1.2 Step 1 — Add a Test

`cookies_test.go`, black-box package (`chapter8_test`) — test as a consumer, not the implementer.

```go
package chapter8_test
import "testing"

func Test_CookiePurchases(t *testing.T) {
    t.Run(`Given a user tries to purchase a cookie and we have them in stock,
        "when they tap their card, they get charged and then receive an email receipt a few moments later.`,
        func(t *testing.T) {
            t.FailNow()
        })
}
```

`t.FailNow()` is critical — empty tests otherwise pass silently.

### 8.1.3 Step 2 — Run and Watch It Fail

```
=== RUN Test_CookiePurchases
=== RUN Test_CookiePurchases/Given_a_user_tries_to_purchase_a_cookie_...
--- FAIL: Test_CookiePurchases (0.00s)
FAIL
```

### 8.1.4 Step 3 — Minimum Code to Pass

```go
package chapter8

import "context"

type (
    EmailSender interface {
        SendEmailReceipt(ctx context.Context, emailAddress string) error
    }
    CardCharger interface {
        ChargeCard(ctx context.Context, cardToken string, amountInCents int) error
    }
    CookieStockChecker interface {
        AmountInStock(ctx context.Context) int
    }
    CookieService struct {
        emailSender  EmailSender
        cardCharger  CardCharger
        stockChecker CookieStockChecker
    }
)

func NewCookieService(e EmailSender, c CardCharger, a CookieStockChecker) (*CookieService, error) {
    return &CookieService{emailSender: e, cardCharger: c, stockChecker: a}, nil
}

func (c *CookieService) PurchaseCookies(ctx context.Context, amountOfCookiesToPurchase int) error {
    // TODO: ask how much cookies cost. This is a placeholder.
    priceOfCookie := 5

    cookiesInStock := c.stockChecker.AmountInStock(ctx)
    if amountOfCookiesToPurchase > cookiesInStock {
        // TODO: what do I do in this situation?
    }
    cost := priceOfCookie * amountOfCookiesToPurchase
    // TODO: where do I get cardtoken from?
    if err := c.cardCharger.ChargeCard(ctx, "some-token", cost); err != nil {
        // TODO: handle this later.
    }
    if err := c.emailSender.SendEmailReceipt(ctx, "some-email"); err != nil {
        // TODO: handle error later
    }
    return nil
}
```

Notice the **TODO comments** — placeholders for the conversation with the domain expert. TDD forces you to enumerate the unknowns.

### 8.1.5 Generate Mocks With gomock

```go
// gen.go
package gen

import _ "github.com/golang/mock/mockgen/model"

//go:generate mockgen -package mocks -destination chapter8/mocks/cookies.go github.com/PacktPublishing/Domain-Driven-Design-with-GoLang/chapter8 CookieStockChecker,CardCharger,EmailSender
```

```bash
go generate ./...
```

### 8.1.6 Step 4 — Rerun Tests With Mocks

```go
func Test_CookiePurchases(t *testing.T) {
    t.Run(`Given a user tries to purchase a cookie and we have them in stock,
        "when they tap their card, they get charged and then receive an email receipt a few moments later.`,
        func(t *testing.T) {
            var (
                ctrl = gomock.NewController(t)
                e    = mocks.NewMockEmailSender(ctrl)
                c    = mocks.NewMockCardCharger(ctrl)
                s    = mocks.NewMockCookieStockChecker(ctrl)
                ctx  = context.Background()
            )
            cookiesToBuy := 5
            totalExpectedCost := 25
            cs, err := chapter8.NewCookieService(e, c, s)
            if err != nil {
                t.Fatalf("expected no error but got %v", err)
            }
            gomock.InOrder(
                s.EXPECT().AmountInStock(ctx).Times(1).Return(cookiesToBuy),
                c.EXPECT().ChargeCard(ctx, "some-token", totalExpectedCost).Times(1).Return(nil),
                e.EXPECT().SendEmailReceipt(ctx, "some-email").Times(1).Return(nil),
            )
            err = cs.PurchaseCookies(ctx, cookiesToBuy)
            if err != nil {
                t.Fatalf("expected no error but got %v", err)
            }
        })
}
```

### 8.1.7 Q&A With the Domain Expert

- **Q: Cookie price?** A: 50 cents; might change.
- **Q: Out of stock?** A: Sell them what we have.
- **Q: Card token source?** A: Provided by the card machine.
- **Q: Email source?** A: Same, from the card machine.

Stub the remaining four tests with `t.FailNow()` so they fail fast (each `t.Run` takes a prose name from the acceptance criteria — see the book for full strings).

### 8.1.8 Step 5 — Refactor Each Test in Lockstep With Production

Bump `priceOfCookie` to 50; the first test fails with `Got: 250, Want: 25`; fix the expected total. Tests pass.

Now fill in the four remaining scenarios. Each follows the same shape — bump a `gomock` expectation or assert on a specific error message; then patch the production code. Four minimal production patches cover them:

```go
// 1. Out of stock
if cookiesInStock == 0 {
    return errors.New("no cookies in stock sorry :(")
}
// 2. Card declined
if err := c.cardCharger.ChargeCard(ctx, "some-token", cost); err != nil {
    return errors.New("your card was declined, you are banned!")
}
// 3. Email fails after successful charge
if err := c.emailSender.SendEmailReceipt(ctx, "some-email"); err != nil {
    return errors.New("we are sorry but the email receipt did not send")
}
// 4. Over-purchase — clamp to what's in stock
if amountOfCookiesToPurchase > cookiesInStock {
    amountOfCookiesToPurchase = cookiesInStock
}
```

The four tests assert the error messages verbatim; each production patch makes its test pass.

### 8.1.9 Final Refactor — Function Signature Becomes Honest

The domain expert told us the **card token and email are supplied at call time**. Move them onto the function:

```go
func (c *CookieService) PurchaseCookies(
    ctx context.Context,
    amountOfCookiesToPurchase int,
    cardToken string,
    email string,
) error {
    priceOfCookie := 50
    cookiesInStock := c.stockChecker.AmountInStock(ctx)
    if cookiesInStock == 0 {
        return errors.New("no cookies in stock sorry :(")
    }
    if amountOfCookiesToPurchase > cookiesInStock {
        amountOfCookiesToPurchase = cookiesInStock
    }
    cost := priceOfCookie * amountOfCookiesToPurchase
    if err := c.cardCharger.ChargeCard(ctx, cardToken, cost); err != nil {
        return errors.New("your card was declined, you are banned!")
    }
    if err := c.emailSender.SendEmailReceipt(ctx, email); err != nil {
        return errors.New("we are sorry but the email receipt did not send")
    }
    return nil
}
```

Update each test to pass and expect the real values:

```go
email := "some@email.com"
cardToken := "token"
...
c.EXPECT().ChargeCard(ctx, cardToken, totalExpectedCost).Times(1).Return(nil),
e.EXPECT().SendEmailReceipt(ctx, email).Times(1).Return(nil),
...
err = cs.PurchaseCookies(ctx, cookiesToBuy, cardToken, email)
```

100% coverage. Three follow-up exercises: 12-char card token validation, restricted email domains, free purchases on January 14th.

### 8.1.10 A Note on DRY in Tests

> "Tests are the best documentation we can have, and ensuring that every test has all the information you need to figure out what it is doing outlined clearly is the best way to ensure other engineers (and your future self) can get up to speed with the code base." — Matthew Boyle

Code is written once, read many times. Optimise for the reader. Avoid table-driven tests for the same reason.

## 8.2 BDD — Behaviour-Driven Development

BDD layers a domain-specific language on top of TDD so that acceptance criteria become executable. **Gherkin** (the language) + **Cucumber** (the runner). For Go: `go-bdd`.

### 8.2.1 Gherkin Example

```gherkin
Feature: checkout Integration
Scenario: Successfully Capture a payment
    Given I am a customer
    When I purchase a cookie for 50 cents.
    Then my card should be charged 50 cents and an e-mail receipt is sent.
```

### 8.2.2 go-bdd Walkthrough

```bash
go get github.com/go-bdd/gobdd
mkdir -p features
```

`features/add.feature`:

```gherkin
Feature: Adding numbers
    Scenario: add two numbers together
        When I add 3 and 6
        Then the result should equal 9
```

`add_test.go`:

```go
package chapter8

import (
    "testing"

    "github.com/go-bdd/gobdd"
)

func add(t gobdd.StepTest, ctx gobdd.Context, first, second int) {
    res := first + second
    ctx.Set("result", res)
}

func check(t gobdd.StepTest, ctx gobdd.Context, sum int) {
    received, err := ctx.GetInt("result")
    if err != nil {
        t.Fatal(err)
        return
    }
    if sum != received {
        t.Fatalf("expected %d but got %d", sum, received)
    }
}

func TestScenarios(t *testing.T) {
    suite := gobdd.NewSuite(t)
    suite.AddStep(`I add (\d+) and (\d+)`, add)
    suite.AddStep(`the result should equal (\d+)`, check)
    suite.Run()
}
```

Step names appear in the regexes so spec + code stay readable together; `ctx.Set`/`ctx.GetInt` is a tiny whiteboard for steps. Fine for trivial scenarios; heavy scaffolding for complex ones — BDD rarely pays off without engaged domain experts.

## 8.3 Chapter 8 Summary — Testing Playbook

- [ ] Write the test before the code; use Given/When/Then prose where it helps.
- [ ] Use `t.FailNow()` in stub tests so empty tests fail loud.
- [ ] Test as a consumer: package `xxx_test`, not `xxx`.
- [ ] Name tests after acceptance criteria — the test file becomes documentation.
- [ ] Mock interfaces with `gomock`; use `gomock.InOrder` to assert call order.
- [ ] Don't over-DRY tests — clarity beats brevity.
- [ ] Reach for BDD only when domain experts will actually participate.

---

# CROSS-CUTTING TOPICS

# Go-Specific Best Practices for DDD

Patterns the book uses over and over. Use them as a checklist when reviewing a Go+DDD PR.

## A. Project Layout

```
service/
├── cmd/
│   └── main.go                   # composition root only
└── internal/                     # cannot be imported by other modules
    ├── coffeeco/                 # cross-domain primitives (CoffeeLover, Product)
    ├── store/
    │   ├── store.go              # entity
    │   └── repository.go         # MongoRepository, etc.
    ├── purchase/
    │   ├── purchase.go           # aggregate
    │   ├── service.go            # domain service
    │   ├── repository.go         # interface
    │   └── mongo.go              # infrastructure repository
    ├── payment/
    │   ├── means.go
    │   └── stripe.go             # infrastructure service
    └── loyalty/
        └── coffeebux.go
```

- **`internal/`** is the DDD "this is not your public API" enforcement.
- **`cmd/`** keeps the wiring (`main.go`) separate from the domain.
- One package per aggregate, not one big bag-of-stuff.

## B. Money

Use `github.com/Rhymond/go-money`. Never `float64`. Always non-exported fields and a small wrapper type that enforces currency.

## C. Identifiers

Use `github.com/google/uuid`. Document the choice (UUIDv4 vs UUIDv7) in your README. If you must use ints, document the rollover contingency and split counters (e.g., Twitter Snowflake) before they bite you.

## D. Context Propagation

Every adapter, service, and repository method takes `ctx context.Context` as its first argument. Authorisation, cancellation, tracing, and deadlines are all in there. Don't smuggle them via package-level globals.## E. Errors

Use `errors.New` for sentinel errors; `fmt.Errorf("...: %w", err)` for wrapping. Define sentinel errors on the producing package (e.g., `store.ErrNoDiscount`) and let callers `errors.Is` against them.

```go
var ErrNoDiscount = errors.New("no discount for store")

if err != nil && err != store.ErrNoDiscount {
    return fmt.Errorf("failed to get discount: %w", err)
}
```

## F. Interfaces

Define the interface in the **consumer**'s package, not the implementer's. Keep interfaces small (often one method). Use `interface{}` (or `any`) only when you really mean it.

## G. Getters / Setters (Entity Method Shapes)

- Methods that mutate → return `error`.
- Methods that compute → return the value, never `error` unless something can actually go wrong.
- Avoid exposing raw setters; expose intent-named methods (`AddStamp()`, `SetAuctionEnd(ts time.Time) error`).

## H. Mocks

gomock for unit tests. For larger programs consider counterfeiter (literate, no codegen command). Always test the interface, never the concrete type.

## I. Configuration

12-factor: env vars for secrets. Composition root reads env, builds deps, calls `main`. Never import config in domain packages.

## J. Observability

(Not book content, but consistent with the author's "expect failure" attitude.) Wrap your application service with OpenTelemetry tracing and structured logs. Tests don't need telemetry; production does.

## K. Module Hygiene

```bash
go mod tidy
go mod vendor
```

Vendor only if you have to (private proxies, airgapped). Otherwise rely on Go's module cache + proxy.

# Anti-Patterns & Common Mistakes

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| **Anemic entity** | No behaviour in entity; logic scattered across services | Move invariants onto entity as methods; keep service thin |
| **`float64` for money** | Precision loss, rounding bugs | `github.com/Rhymond/go-money` |
| **Public getters/setters everywhere** | Invariants cannot be enforced | Intent-named methods (`AddStamp()`, `SetAuctionEnd(t) error`) |
| **Repository per database table** | Aggregate consistency lost across boundaries | One repository per aggregate |
| **Domain knows the DB library** | Future swaps painful | Adapter layer; DB structs in infrastructure package |
| **ORM-as-domain** | Anemic structs by default | Thin ORM or hand-rolled SQL; keep domain separate |
| **Calling external SDKs directly from the domain** | Hard to test; coupled | Wrap as infrastructure service behind an interface |
| **Internal package imported from outside** | Domain leaks to public API | Use `internal/` |
| **Ubiquitous language used inconsistently** | Domain experts and engineers talk past each other | Glossary + sprint review + code review enforce |
| **Marketing opt-in on the order aggregate** | Wrong context, wrong transaction boundary | Move to marketing context; eventually consistent |
| **Service interface in implementer's package** | Couples consumers to producer | Define interface in consumer's package |
| **Big switch in a service for every payment type** | Open-closed violation | Push each type into value object / domain service |
| **Two-phase commit assumed safe** | Blocking + SPOF; won't scale | Sagas + compensating actions + event on rollback failure |
| **CQRS via `interface{}` return types** | Type system bypassed | Let idiomatic Go signatures enforce CQRS |
| **CoffeeBux-paying customers still earning stamps** | Wrong invariant | Branch on payment means; consult experts |
| **Refusing to declare partial-redemption rules** | Consumers write their own logic | Push back; document with experts |
| **Saga rollback silently swallowed** | Invisible failures | Emit domain event for out-of-band process |
| **200 OK with `error: ...` body** | Forces string parsing | HTTP status codes; structured errors |
| **Empty passing tests** | Masks missing behaviour | `t.FailNow()` + fail-fast on incomplete tests |
| **TDD as afterthought** | Refactors break behaviour silently | Test first; tests document the domain |

# Decision Heuristics / Checklists

| Decision                                                    | Heuristic                                                                                   |
|-------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| Apply DDD at all?                                           | Simple CRUD with < ~30 stories → don't. 40+ stories, growth, longevity, novelty → strong fit. No leadership commitment to expert time → don't. |
| Value object vs. entity?                                    | Immutable + measures/describes + comparable by value → value object. Needs identity across attribute changes → entity. |
| Where does a method live?                                   | One entity → method on entity. Multi-entity business logic → domain service. Auth/coordination → application service. External SaaS/API → infrastructure service. |
| Where does state live?                                      | Aggregate root field. Cross-aggregate within one context → domain event (eventual). Cross-context → message bus (eventual). |
| Open host tech?                                             | REST fluency + multi-language consumers → OpenAPI + oapi-codegen. Streaming / latency-critical → gRPC + buf. Pure file/queue → Kafka + schema. |
| Message bus?                                                | Millions msg/sec + ordering + Kafka learning budget → Kafka. Classic queues + AMQP + UI → RabbitMQ. At-most-once OK + Go-readability → NATS. |
| Synchronous vs. async consistency?                          | One aggregate → transactional. Multi-aggregate same context → domain event (eventual). Cross-context → bus (eventual). |
| Mock vs. run real?                                          | Mock external SDKs always. Mock repos in unit tests; integration-test the concrete impl. Never mock the type under test. |
| Add an anti-corruption layer?                               | External model drifts from yours. Cross-context boundary. Mid-migration from legacy. |

# Quick Reference — DDD Patterns in One Glance

| Pattern                     | One-liner                                                                  | Go hint                                      |
|-----------------------------|----------------------------------------------------------------------------|----------------------------------------------|
| Ubiquitous language         | Shared terms used in conversation, docs, code                              | Build a `glossary.md`; enforce in code review |
| Bounded context             | Boundary in which a model and language apply                               | One Go module per context; `internal/` enforces |
| Subdomain                   | Domain that is a child of a parent business domain                         | One package per subdomain                    |
| Open Host Service           | Anything that exposes your context to others                               | HTTP handler + gorilla/mux; gRPC server      |
| Published language          | Documented external contract                                               | OpenAPI spec or gRPC `.proto`                |
| Anti-corruption layer       | Translates between context's model and an external model                   | One file in the consumer's package           |
| Entity                      | Identity-driven object; behaviour-rich methods                              | UUID ID; unexported fields; validate-time methods return `error` |
| Value object                | Value-driven; immutable; replace-not-mutate                                | `func New(x, y) X` (no pointer); unexported fields |
| Aggregate                   | Transactional consistency boundary; root + members                         | `root` with `[]Member`; methods on root only |
| Domain event                | "Something happened" message; carries state-change                         | Struct with type, payload, headers, ID        |
| Factory                     | Function whose only job is construction                                    | `func NewBooking(...) (*Booking, error)`     |
| Repository                  | All persistence for an aggregate, behind an interface                       | One per aggregate; no domain logic           |
| Domain service              | Behaviour that doesn't fit one entity                                       | Stateless; pure methods                       |
| Application service         | Thin coordinator; auth, transactions, composition                          | Constructed once; one method per use case    |
| Infrastructure service      | Wrapper around external system                                             | One per provider; behind consumer-defined interface |
| CQRS                        | Separate command and query concerns                                        | Mutating methods return only `error`; queries return only values |
| Saga                        | Forward action + compensating action; rollback completed steps on failure  | `Saga` interface; iterate and `Rollback`     |
| 2PC                         | Coordinator asks "can you commit?" then commits                            | Use only when no other way                   |
| TDD                         | Test first, code to pass, refactor                                          | `t.FailNow` on stub tests; gomock mocks      |
| BDD                         | Acceptance criteria in natural language become tests                       | Gherkin + Cucumber or `go-bdd`               |

# Closing Notes

A **strategic primer** for explaining DDD to a new team, a **tactical reference** for PR review (the anti-patterns table is your grep target), and a **starter kit** for new services (copy the layout, copy the patterns, write the test first). The book's central argument: DDD is not a tech-stack choice; it is a **commitment** between engineers, domain experts, and leadership. The Go patterns shown here are how that commitment shows up in code.

**Source pointers:**

- `markdown_output/Domain-Driven_Design_with_Golang_-_Matthew_Boyle/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md` — full book text.
- `summaries/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md` — chapter-level synthesis.
- `https://github.com/PacktPublishing/Domain-Driven-Design-with-GoLang` — companion code (chapters 2–8).
