# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Domain-Driven Design with Golang
**Author:** Matthew Boyle (Packt, 2022)
**Topic tags:** `#architecture` `#general` `#ddd` `#golang`
**Language focus:** Go-first (Go 1.19+) — preserves all book code verbatim
**Sources:** `markdown_output/Domain-Driven_Design_with_Golang_-_Matthew_Boyle/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md` · `summaries/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md`

## TL;DR
A hands-on translation of Eric Evans's DDD into idiomatic Go. The book's two halves: (1) the DDD tactical building blocks as Go idioms — entities, value objects, aggregates, factories, repositories, services, with caveats specific to Go (no classical inheritance, struct/pointer semantics, interfaces over implementations); (2) a working CoffeeCo+microservice codebase that demonstrates Ports & Adapters, Anti-Corruption Layer, Open Host Service, MongoDB persistence, Stripe infrastructure service, saga, distributed systems patterns, and TDD/BDD. Apply this when you build Go services that need to model a real business domain faithfully.

---

## Best Practices by Topic

### DDD in Go: Foundational Mindset

**Principle:** DDD puts business logic first. Go is not OO (no classical inheritance), so DDD building blocks are realised via *composition*, value-receiver methods, interface-based polymorphism, and the `internal/` directory for encapsulation.

**Do:**
- Put domain code inside Go's special `internal/` directory so external projects can't import it — strong package boundary for DDD.
- Lean on Go's standard `time` and `context` packages — they underpin almost every domain method.
- Treat the book as "DDD applied" rather than "DDD theory" — verify every example compiles in your head against Go's type system.
- Recognise Go's three strengths for DDD: simple value semantics (struct values vs. pointers), implicit interfaces, composition over inheritance.

**Don't:**
- Don't try to map Go directly to OO DDD examples — value/pointer semantics change everything.
- Don't reach for an ORM to "save" your model — let the model dictate the schema, not vice versa.

*Ref: Domain-Driven Design with Golang.md — "Getting started with our CoffeeCo system", "A Brief History of Domain-Driven Design"*

---

### Entities

**Principle:** Domain objects defined by stable identity, not attributes. Attributes can mutate; identity cannot. Use `uuid.UUID` (Google's `github.com/google/uuid`) for safe, future-proof IDs.

**Do:**
- Use Google UUIDs (`github.com/google/uuid`) for entity IDs — they are 128-bit, effectively unique, and avoid the `math.MaxInt+1` overflow trap.
- Treat attributes as private (`lowercase`) — encapsulation prevents unintended mutation.
- Expose business-logic methods (commands) that validate inputs and maintain invariants.
- Use a dedicated money library (e.g., `github.com/Rhymond/go-money`) — floats are not appropriate for money.
- Treat immutable fields as `readonly` is unusual in Go; expose them through read-only methods.
- Distinguish entity attributes from derived/computed values; expose the *behavior*, not the raw attribute.
- Export entity attributes only when you need them for JSON marshalling; otherwise keep them private.

**Don't:**
- Don't use `int` IDs at scale — they overflow and force costly migrations.
- Don't use mutable identifiers (e.g., email) for entity IDs.
- Don't build anemic entities: full of public getters/setters with no behavior — they are "anemic models." Push behavior into the entity.
- Don't let the database ORM dictate your entity shape — keep entity layer free of persistence tags where possible.

**Code: Auction entity — Go-first, behavior + data:**
```go
package chapter3

import (
    "time"
    "github.com/Rhymond/go-money"
)

// Auction is an entity to represent our auction construct.
type Auction struct {
    ID            int
    // We use a specific money library as floats are not good ways to represent money.
    startingPrice money.Money
    sellerID      int
    createdAt     time.Time
    auctionStart  time.Time
    auctionEnd    time.Time
}
```
**Code: Refactored entity (behavior, not setters):**
```go
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

func (a *AuctionRefactored) SetAuctionStartTimeInUTC(auctionStart time.Time) error {
    if err := a.validateTimeZone(auctionStart); err != nil {
        return err
    }
    a.auctionStart = auctionStart
    return nil
}

func (a *AuctionRefactored) validateTimeZone(t time.Time) error {
    tz, _ := t.Zone()
    if tz != time.UTC.String() {
        return errors.New("time zone must be UTC")
    }
    return nil
}
```
**Code: UUID adoption:**
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
*Ref: Domain-Driven Design with Golang.md — "Working with entities", "Generating good identifiers", "A warning when defining entities", "Anemic models"*

---

### Value Objects

**Principle:** Domain concepts identified by their values, not identity. Two value objects with the same values are equal. **Immutability + replaceability** are the cornerstone — returning a new instance is the answer to "mutation."

**Do:**
- Return value types (not pointers) from constructors so equality checks (`if a != b`) work as expected.
- Lowercase all fields to prevent external mutation; expose read-only methods.
- Let `move`-style operations return *new* value objects from existing ones (replaceability).
- Keep behavior side-effect-free; this enables pure-function unit tests.
- Build small constructors (`NewPoint`, `Height.Metric`, `PhoneNumber.Parse`) that validate and decode at the boundary.
- Always answer "yes" to all three: immutability, measures a domain concept, value-based equality — if so, it's a value object.
- Use value objects for entity properties (PersonId, Name, PhoneNumber, EmailAddress, Height, CountryCode).

**Don't:**
- Don't return pointers from value-object constructors unless you have a specific need — pointer comparison breaks equality.
- Don't mutate fields inside value-object methods — return new instances.
- Don't introduce a `ColorId` "for uniqueness" — it's redundant; two colors with the same RGB are the same color.
- Don't reuse primitive types for domain concepts (`string` for phone, `int` for height). Always wrap.

**Code: Value object — return value type, lowercase fields, replaceable:**
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
*Ref: Domain-Driven Design with Golang.md — "Working with value objects", "How should I decide whether to use an entity or value object?"*

---

### Aggregates

**Principle:** A cluster of entities and value objects treated as a single transactional consistency boundary. The aggregate root is the only legal entry point; all changes go through it.

**Do:**
- Discover aggregates by finding *invariants* — business rules that must always hold. The aggregate is the *transactional consistency boundary*.
- Keep aggregates **small** — include only data that must be strongly consistent for the aggregate's business logic.
- Change only one aggregate per transaction. Need to commit multiple aggregates = wrong boundary.
- Reference other aggregates by *ID* (typically UUID), not by pointer — enforces independent boundaries.
- Have one entity serve as the **aggregate root** exposing the public interface.
- Treat aggregates beyond a single bounded context as *eventually* consistent across the boundary; strongly consistent *within*.
- Validate assumptions with domain experts (e.g., "allow partial redemption of a purchase against a loyalty card?") — interface changes ripple through code.

**Don't:**
- Don't include data whose consistency tolerance is "eventual" inside the aggregate — it bloats the transactional boundary and hurts scalability.
- Don't be misled by data structures (arrays, slices, maps) — these are not aggregates.
- Don't expect strong consistency *across* aggregates — accept eventual consistency, design for it.

**Code: Wallet aggregate with `WalletItem` interface**
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
**Code: Order aggregate — keep small, exclude unrelated data:**
```go
type Order struct {
    items         []item
    taxAmount     money.Money
    discount      money.Money
    paymentCardID uuid.UUID
    customerID    uuid.UUID
}
// NOTE: marketingOptIn was removed because it is unrelated to the order's
// transactional invariant and changes between order-start and order-complete
// would not corrupt the order's state.
```
*Ref: Domain-Driven Design with Golang.md — "The aggregate pattern", "Discovering aggregates", "Designing aggregates", "Aggregates beyond a single bounded context"*

---

### Factory Pattern

**Principle:** Encapsulate complex object creation. Ensures aggregates are always created in a valid state and hides construction details from callers.

**Do:**
- Use factory functions for entities and aggregates — they enforce creation invariants at the boundary.
- Let the factory generate the ID (`uuid.New()`) unless you have a specific reason not to.
- Add business validation at the boundary: e.g., "no bookings after closing time" lives in `CreateBooking`.
- Return errors rather than panicking on invalid inputs.
- Use Go's package structure: define factory in the same package as the entity.

**Don't:**
- Don't expose constructors that produce invalid entities — push validation into the factory.
- Don't sprinkle construction logic across the codebase — centralize in factories.

**Code: Go factory with validation:**
```go
package chapter4

import (
    "errors"
    "time"
    "github.com/google/uuid"
)

type Booking struct {
    id            uuid.UUID
    from          time.Time
    to            time.Time
    hairDresserID uuid.UUID
}

func CreateBooking(from, to time.Time, hairDresserID uuid.UUID) (*Booking, error) {
    closingTime, _ := time.Parse(time.Kitchen, "17:00pm")
    if from.After(closingTime) {
        return nil, errors.New("no appointments after closing time")
    }
    return &Booking{
        hairDresserID: uuid.New(),
        id:            uuid.New(),
        from:          from,
        to:            to,
    }, nil
}
```
*Ref: Domain-Driven Design with Golang.md — "Introducing the factory pattern", "Entity factories"*

---

### Repository Pattern (Per Aggregate, Not Per Table)

**Principle:** The repository layer centralizes data access. Define the *interface* in the domain layer; implement it in the infrastructure layer. **One repository per aggregate, not per database table.**

**Do:**
- Define the repository *interface* in the same package as your aggregate / domain service.
- Pass `context.Context` to every method — standard Go practice for cancellation/timeouts.
- Let a single repository aggregate write to multiple tables if that's how the aggregate is structured.
- Keep the repository thin — no business logic; just persistence.
- Use modern Go drivers (`pgx` for Postgres, official Mongo driver) and wrap errors with `%w`.
- Use interface segregation: the domain declares only the operations it needs; infrastructure provides them.
- Decouple the domain from the persistence representation with a translation struct (e.g., `mongoPurchase` for Mongo).

**Don't:**
- Don't make *one repository per database table* — that's an antipattern; aggregates span tables.
- Don't mix business logic into the repository — it belongs in the domain layer.
- Don't bypass the repository — direct DB access from controllers breaks encapsulation.
- Don't lean on ORMs (e.g., GORM) — they "lead to a layer of unnecessary abstraction and poor database query design" — keep the domain free of ORM tags.

**Code: Repository interface in the domain layer:**
```go
package purchase

import "context"

type Repository interface {
    Store(ctx context.Context, purchase Purchase) error
}
```
**Code: Postgres implementation with pgx:**
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
**Code: Mongo implementation — repository decoupled from domain via `mongoPurchase`:**
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
    mongoP := New(purchase) // translate domain Purchase to mongoPurchase
    _, err := mr.purchases.InsertOne(ctx, mongoP)
    if err != nil {
        return fmt.Errorf("failed to persist purchase: %w", err)
    }
    return nil
}

type mongoPurchase struct {
    id                  uuid.UUID
    store               store.Store
    productsToPurchase  []coffeeco.Product
    total               money.Money
    paymentMeans        payment.Means
    timeOfPurchase      time.Time
    cardToken           *string
}
```
*Ref: Domain-Driven Design with Golang.md — "Implementing the repository pattern in Golang", "Implementing our product repository"*

---

### Services: Domain, Application, Infrastructure

**Principle:** Three service types; clean layering. Each has a distinct scope:
- **Domain Service** — stateful orchestration of domain logic across multiple aggregates (read across, write to one).
- **Application Service** — thin coordinator across repositories/domain services; where authorization lives; no domain logic.
- **Infrastructure Service** — adapters to external systems (Stripe, MailChimp); never contains domain logic.

**Do:**
- Push business logic down into the domain (entities, value objects, factories). Keep application services *thin* — coordination only.
- Use application services for authorization, transaction boundaries, and orchestration across repositories/domain services.
- Treat external integrations as *infrastructure services* behind interfaces (so payment provider changes don't ripple).
- Use Go's *interfaces-as-contracts* pattern: define what *you need* in the consumer; let infrastructure satisfy it.

**Don't:**
- Don't put domain logic in application services — they violate YAGNI and bleed business rules across layers.
- Don't put infrastructure code in domain logic — violations of dependency direction.
- Don't grow application services into "god services" — they should compose, not own.

**Code: Domain Service for cross-aggregate logic:**
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
**Code: Application Service — thin, authorization, orchestration:**
```go
package chapter4

type BookingDomainService interface {
    CreateBooking(ctx context.Context, booking Booking) error
}

type BookingAppService struct {
    bookingRepo         BookingRepository
    bookingDomainService BookingDomainService
}

func NewBookingAppService(bookingRepo BookingRepository, bookingDomainService BookingDomainService) *BookingAppService {
    return &BookingAppService{bookingRepo: bookingRepo, bookingDomainService: bookingDomainService}
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
*Ref: Domain-Driven Design with Golang.md — "Understanding services", "Domain services", "Application services", "Adding an infrastructure service for payment handling"*

---

### Infrastructure Services (Stripe, MailChimp, etc.)

**Principle:** External integrations belong behind a domain-defined interface. The infrastructure implementation is replaceable — that's the point.

**Do:**
- Define an interface for what the domain needs (e.g., `CardChargeService`, `EmailSender`) in the domain layer.
- Implement that interface in the infrastructure layer using vendor SDKs.
- Inject the infrastructure service into the application service — never call vendor SDKs from domain code.

**Don't:**
- Don't call vendor SDKs directly from the domain layer; it couples your domain to a vendor.
- Don't duplicate domain logic in infrastructure services — keep them dumb adapters.

**Code: Stripe adapter implementing `CardChargeService`:**
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
*Ref: Domain-Driven Design with Golang.md — "Adding an infrastructure service for payment handling"*

---

### Microservices & Hexagonal Architecture (Ports & Adapters)

**Principle:** Boundary is everything. The domain declares what it needs (a *port*); infrastructure supplies an implementation (an *adapter*). The dependency arrow points *inward* — infrastructure depends on domain, not vice versa.

**Do:**
- Define every external concern as an interface in the domain layer (`AvailabilityGetter`, `CardChargeService`, `EmailSender`).
- Have your domain service depend only on those interfaces (not on `*http.Client`, `*mongo.Client`, etc.).
- Develop the domain with stubs / mocks against the interface — work can proceed in parallel with infrastructure teams.
- Use the same `internal/` package convention to enforce boundaries.
- Generate a clear failure-friendly flow: validate parameters, parse inputs, return clearly typed JSON; never leak internal structures.
- When refactoring, the published-API of the API gateway becomes your contract — other services decouple from your internal model.

**Don't:**
- Don't import infra packages (`net/http`, `mongo`, `stripe`) from the domain package — that points the arrow the wrong way.
- Don't couple your domain to a specific external API's exact response shape — wrap it in your own type via an adapter.
- Don't share code via libraries across microservices — couples release cycles.

**Code: Domain declares port; infrastructure provides adapter:**
```go
package chapter6  // recommendation domain

type Option struct {
    HotelName    string
    Location     string
    PricePerNight money.Money
}

type AvailabilityGetter interface {
    GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error)
}

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
    // algorithm body...
}
```
**Code: Adapter implements the domain's port against an external API:**
```go
type partnerShipsResponse struct {
    AvailableHotels []struct {
        Name              string `json:"name"`
        PriceInUSDPerNight int   `json:"priceInUSDPerNight"`
    } `json:"availableHotels"`
}

func (p PartnershipAdaptor) GetAvailability(ctx context.Context, tripStart time.Time, tripEnd time.Time, location string) ([]Option, error) {
    url := fmt.Sprintf("%s/partnerships?location=%s&from=%s&to=%s", p.url, location, from, to)
    res, err := p.client.Get(url)
    if err != nil {
        return nil, fmt.Errorf("failed to call partnerships: %w", err)
    }
    defer res.Body.Close()
    if res.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("bad request to partnerships: %d", res.StatusCode)
    }
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
*Ref: Domain-Driven Design with Golang.md — "Building a microservice using DDD", "Setting the scene", "Building a recommendation system", "What do we mean by microservices?"*

---

### Anti-Corruption Layer (ACL) in Go

**Principle:** When integrating with an external system, decouple its model from yours. The ACL *owns* the translation. Your bounded context remains pure.

**Do:**
- Implement the ACL as a separate package (e.g., `adapter.go`) backed by a domain-defined interface.
- Validate inputs at the boundary — fail fast with `400 Bad Request` for malformed requests.
- Translate external response structures into your domain's types (`Option`, `Recommendation`) — never leak `partnerShipsResponse` upward.
- Wrap external errors with `%w` so callers can inspect the underlying cause; decide what to surface externally.

**Don't:**
- Don't expose the external API's exact response shape from your domain — it locks you in.
- Don't expose raw errors from external calls verbatim — give callers a meaningful domain-level error.
- Don't let the external system dictate your response types — your domain owns its own types.

*Ref: Domain-Driven Design with Golang.md — "Revisiting the anti-corruption layer"*

---

### Open Host Service (Published Language)

**Principle:** Expose an API whose request/response shapes are designed for *consumers* — separate from your internal model. Other teams build against it; you can refactor internally without breaking them.

**Do:**
- Define request and response structs that fit the use case *for your consumers* — not for your internals.
- Validate inputs at the HTTP boundary (`WriteHeader(BadRequest)` or rich error response).
- Document the published contract clearly; communicate with consumer teams about changes.

**Don't:**
- Don't expose your internal aggregate shape through your public API — internal refactors become breaking changes.
- Don't accept untyped requests — parse and validate before reaching domain logic.

**Code: HTTP handler with input validation and published-language response:**
```go
type GetRecommendationResponse struct {
    HotelName string `json:"hotelName"`
    TotalCost struct {
        Cost     int64  `json:"cost"`
        Currency string `json:"currency"`
    } `json:"totalCost"`
}

func (h Handler) GetRecommendation(w http.ResponseWriter, req *http.Request) {
    q := mux.Vars(req)
    location, ok := q["location"]
    if !ok {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    // ...extract and parse from, to, budget...
    const expectedFormat = "2006-01-02"
    formattedStart, err := time.Parse(expectedFormat, from)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    // ...convert budget string to money.Money...
    rec, err := h.svc.Get(req.Context(), formattedStart, formattedEnd, location, budgetMon)
    if err != nil {
        w.WriteHeader(http.StatusInternalServerError)
        return
    }
    res, err := json.Marshal(GetRecommendationResponse{ /* ... */ })
    // ...
}
```
*Ref: Domain-Driven Design with Golang.md — "Exposing our service via an open host service"*

---

### Distributed Systems with Go

**Principle:** Be explicit about trade-offs. Understand CAP. Use proven patterns (CQRS, EDA, saga, message bus) at the right scale — not by default. Plan for failure; the network is asynchronous.

**Do:**
- Treat the system as **scalable, fault-tolerant, transparent, concurrent, heterogeneous, replicated** — explicitly trade off among them.
- Match CQRS rules to Go: "If a method modifies the state of the receiver struct or database, it is a command and should return an error or nil. If a method returns a value, it should not modify the database or its receiver struct."
- Use **events** (event header + event body) for cross-service communication; output `domain events` (`user.loggedIn`, `purchase.failed`) as the meaningful interchange format.
- Use the **saga pattern** for multi-step consistency without 2PC: each step has a compensating action; combine with EDA for retries.
- Pick a message bus (Kafka for scale, RabbitMQ for simplicity, NATS for IoT/speed) based on workload.
- Place domain event emission behind a *Command* that returns *error* and never returns a value.

**Don't:**
- Don't enforce CQRS via single `Commander`/`Querier` interfaces with `interface{}` parameters — "we have lost all benefits of Go's type system" and command names give little insight.
- Don't assume 2PC is non-blocking — locks persist after coordinator failure.
- Don't rely on Kafka's at-most-once durability guarantees — NATS delivers at most once (your message *might never arrive*).
- Don't assume RabbitMQ scales to Kafka-level workloads — pick the right tool.
- Don't make services depend on synchronous chains of other services — every hop is a failure surface.

**Code: Saga interface + linear manager (rollback on failure):**
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
                    // One of our compensation actions failed; we need to handle it (perhaps by emitting a message to a messagebus).
                }
            }
        }
    }
}
```
*Ref: Domain-Driven Design with Golang.md — "What is a distributed system?", "Distributed system patterns", "CQRS", "EDA", "Dealing with failure", "Two-phase commit (2PC)", "The saga pattern", "What is a message bus?"*

---

### TDD and BDD in Go

**Principle:** TDD complements DDD: write tests in domain language (the ubiquitous language) before code. BDD is TDD extended to multi-stakeholder acceptance criteria written as Given/When/Then (Gherkin).

**Do:**
- Use Go's `_test.go` convention; declare test package as `chapter8_test` (black-box) — tests the *consumer's* view, not implementation.
- Use the Given/When/Then naming style (`Given ... when ... then ...`) — it doubles as documentation and aligns with the ubiquitous language.
- Use `t.Run(name, func(t *testing.T) { t.FailNow() })` to scaffold tests — Go treats empty test functions as passing, so explicitly fail until implemented.
- Always include `t.FailNow()` for unimplemented tests — otherwise an empty test silently passes.
- Use `gomock` to mock interfaces — keeps tests free of vendor dependencies and lets you exercise failure paths deterministically.
- Run tests from CLI: `go test ./...`.

**Don't:**
- Don't write tests against internal implementation details; prefer package tests (`_test`) for black-box testing.
- Don't write code before tests (in TDD) — discipline matters; write "just enough" code to pass.
- Don't conflate unit, integration, and acceptance tests — be explicit about which is which.
- Don't assume BDD without domain-expert buy-in — scaffolding cost is high and BDD pays only with active cross-functional collaboration.

**Code: TDD scaffold with Given-When-Then:**
```go
package chapter8_test

import "testing"

func Test_CookiePurchases(t *testing.T) {
    t.Run(`Given a user tries to purchase a cookie and we have them in stock,
        "when they tap their card, they get charged and then receive an email receipt a few moments later."`,
        func(t *testing.T) {
            t.FailNow() // scaffold; will be replaced as we implement
        })
}
```
**Code: Mocking dependencies with gomock:**
```go
func Test_CookiePurchases(t *testing.T) {
    t.Run(`Given a user tries to purchase a cookie and we have them in stock,
        "when they tap their card, they get charged and then receive an email receipt a few moments later."`,
        func(t *testing.T) {
            var (
                ctrl = gomock.NewController(t)
                e    = mocks.NewMockEmailSender(ctrl)
                c    = mocks.NewMockCardCharger(ctrl)
                s    = mocks.NewMockCookieStockChecker(ctrl)
                ctx  = context.Background()
            )
            cookiesToBuy := 5
            totalExpectedCost := 250
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
**Code: BDD with Gherkin + go-bdd:**
```gherkin
Feature: Adding numbers
  Scenario: add two numbers together
    When I add 3 and 6
    Then the result should equal 9
```
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
*Ref: Domain-Driven Design with Golang.md — "TDD", "BDD"*

---

## Anti-Patterns & Common Mistakes

- **Anemic entities** (full of public getters/setters with no business logic) — *fix:* push behavior into the entity; methods validate invariants.
- **ORM-driven entities** (e.g., GORM struct tags defining both schema and domain) — *fix:* keep ORM out of the domain; translate via an adapter layer.
- **Service entities with `int` IDs** — *fix:* use UUID (`github.com/google/uuid`).
- **Value objects returning pointers from constructors** — *fix:* return value types so `==` compares by value.
- **Mutable value object fields** — *fix:* lowercase all fields; return new instances from "modifications."
- **Domain depending on infrastructure packages** (`net/http`, `mongo`, `stripe`) — *fix:* define ports as interfaces in the domain; implement in adapter packages.
- **One repository per database table** — *fix:* one repository per aggregate.
- **Mixing domain logic into application services** — *fix:* thin application services that compose domain services + repositories.
- **Putting domain logic in infrastructure adapters** — *fix:* keep adapters dumb; delegate business rules back to the domain.
- **Internal events exposed externally** — *fix:* private (internal) vs public (integration) events; expose only integration-optimized events through the published language.
- **Multi-step transitions in synchronous chains** — *fix:* use saga or process manager; accept eventual consistency.
- **Trying to enforce CQRS via `interface{}` interfaces** — *fix:* let Go's type system express it; use domain types directly.
- **Slack off into "containerizing the monolith without extracting boundaries"** — *fix:* identify bounded contexts and decompose.
- **Skipping validation at the HTTP boundary** — *fix:* validate every request parameter; fail fast.
- **Coupling microservices via shared libraries** — *fix:* communicate via APIs or events.
- **Treating an eventual-consistency database as a strongly consistent one** — *fix:* design for the model the DB actually provides; surface inconsistencies explicitly.

## Decision Heuristics / Checklists

- **Entity or Value Object?** Default to value object; upgrade to entity only when identity matters across attribute changes.
- **Entity ID type?** UUID for new projects; entity-attribute IDs only when the business genuinely uses them (e.g., social-security number).
- **Money type?** Always `github.com/Rhymond/go-money` or similar — never `float`.
- **Repository per aggregate or per table?** Per aggregate. Aggregates can span tables.
- **Interfaces in domain or in infrastructure?** Interfaces in the *consumer's* package (domain declares port; infrastructure provides adapter).
- **Should this be a domain entity method, a domain service, or an application service?** Entity method → behavior on that entity. Domain service → orchestration across multiple aggregates (read more, write to one). Application service → thin coordinator for repository access, authorization, transaction boundaries.
- **Internal vs public events?** Internal events stay inside the bounded context (private). Public events exposed through the published language integrate with external systems.
- **Saga or 2PC?** Saga unless you genuinely need atomic distributed transactions (and accept the cost).
- **Idempotency on retries?** Required for state-mutating remote calls; use `enable.idempotence=true` or client idempotency keys.
- **Mock or real service in tests?** Mock external dependencies; use `gomock` to generate them.
- **TDD or BDD?** Start with TDD. Adopt BDD only when domain experts actively write Given/When/Then criteria.
- **Black-box or white-box test?** Default black-box (`_test` package). White-box only when probing internals.
- **Time-zone discipline?** Always UTC for time stored; convert at the edges.
- **Validate at the HTTP boundary?** Always — fail fast with `400 Bad Request`.

## Key Takeaways

1. **Go's `internal/` directory is a built-in enforcement mechanism for DDD boundaries** — put domain code inside; never expose aggregates externally.
2. **Default to value objects; prefer struct values over pointers for equality-based identity** — Go's value semantics are power tools for DDD when used well.
3. **Use UUIDs for entity IDs** (`github.com/google/uuid`); never let `int` IDs overflow your design.
4. **Money is a value object** — use `github.com/Rhymond/go-money`.
5. **Repositories: interface in domain, implementation in infrastructure; one per aggregate, not per table.**
6. **Anemic entities are a smell** — push behavior into the entity; methods enforce invariants.
7. **Domain → Infrastructure dependency arrow** — interfaces live with the consumer (domain), implementations live with the producer (infra).
8. **Application services are thin** — authorization, transactions, coordination; never domain logic.
9. **Infrastructure services are dumb adapters** — they translate, not decide.
10. **Anti-Corruption Layer protects your domain from an external system's model** — adapter translates the response, your domain never sees the upstream shape.
11. **Open Host Service publishes an integration-optimized contract** — separate from internal model — that lets consumers integrate and you refactor freely.
12. **Aggregates are transactional consistency boundaries** — keep small, reference others by ID, one aggregate per transaction.
13. **Saga with compensating actions replaces 2PC** for distributed workflows in event-driven systems.
14. **TDD and DDD are complementary** — Given/When/Then scenario names are documentation in the ubiquitous language.
15. **CAP forces trade-offs** — pick what your subdomain needs; don't apply defaults blindly.

## Cross-References
- Related: [[../Learning_Domain_Driven_Design.md]] — DDD theory and patterns that this book concretises in Go.
- Related: [[../Foundations_of_Scalable_Systems.md]] — distributed-systems context: load balancing, async messaging, Kafka, sharding, resilience.
- Topic index: [[../INDEX.md]]
