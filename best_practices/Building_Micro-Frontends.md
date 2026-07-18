# Building Micro-Frontends — Deep Dive
**Author:** Luca Mezzalira (foreword by Neal Ford)
**Topic tags:** `#architecture` `#frontend`
**Language focus:** Framework-agnostic (JavaScript/TypeScript, React, Angular, Vue)
**Sources:** `markdown_output/Building Micro-Frontends/Building Micro-Frontends.md` · `summaries/Building_Micro-Frontends.md`

> "Micro-frontends are an emerging architecture inspired by microservices architecture. The main idea behind it is to break down a monolithic codebase into smaller parts, allowing an organization to spread out the work among autonomous teams, whether collocated or distributed, without the need to slow down their delivery throughput." — Ref: *Building Micro-Frontends.md — "Micro-Frontend Applications"*

---

## TL;DR

Building Micro-Frontends (O'Reilly, 2021) is the canonical practitioner's guide to applying
microservices thinking to the browser. Mezzalira introduces a four-pillar decisions framework
(**define / compose / route / communicate**), maps it to seven concrete architectures
(vertical-split application shell, horizontal-split via Module Federation, iframes, web
components, server-side, edge-side, and build-time), and grounds every choice in real
case studies from Spotify, IKEA, DAZN, Zalando, OpenTable, SAP and New Relic. Apply the
book when a frontend codebase has outgrown one team — typically when coordination
overhead, long release trains, or platform-team bottlenecks appear. The book is the
opposite of silver-bullet: it is a continuous exercise in trade-offs (autonomy vs.
consistency, performance vs. DX, governance vs. team speed), best consumed alongside
DDD, Conway's law, and the *Fundamentals of Software Architecture* notion of the
"least worst architecture."

---

## Best Practices by Topic

### 1. What a Micro-Frontend Actually Is

**Principle:** A micro-frontend is an autonomous, independently deliverable artifact
that represents one business domain and is owned by a single team.

**Do:**
- Map each micro-frontend to one bounded context from your DDD analysis.
- Insist that a micro-frontend be deployable without coordinating releases with
  any other team.
- Treat it as the frontend equivalent of a microservice: hidden implementation
  details, public contract, observable, independently testable.

**Don't:**
- Treat micro-frontends as components — components extend via props, micro-frontends
  encapsulate via events.
- Split on technical layers (header team / footer team) — that is the horizontal
  trap that produces a distributed frontend monolith.
- Couple their release cadence through a shared library or compile-time build.

**Code (definition sketch):**
```
A micro-frontend represents a business domain that is autonomous,
independently deliverable, and owned by a single team.
  - Business domain representation
  - Autonomous codebase
  - Independent deployment
  - Single-team ownership
```
*Ref: Building Micro-Frontends.md — "Micro-Frontend Architects and Challenges"*

---

### 2. The Micro-Frontend Decisions Framework (Four Pillars)

**Principle:** Always make four orthogonal decisions before writing code —
*define, compose, route, communicate*.

**Do:**
- Use the framework as a checklist for every new project and case study.
- Pin every architectural choice (e.g. "horizontal split, client-side, root
  composition, event emitter") to one option in each pillar.
- Revisit decisions when the business evolves; the framework is iterative.

**Don't:**
- Choose a framework or tool before you have answered all four pillars.
- Mix "vertical split" with "edge-side composition" — a vertical-split loads one
  MFE per view, which edge-side does not naturally support.
- Treat the framework as a one-time ceremony; record decisions as ADRs.

**Pillar summary:**
| Decision      | Options                                                                 |
|---------------|-------------------------------------------------------------------------|
| Define        | Horizontal split / Vertical split                                       |
| Compose       | Client side / Server side / Edge side / Build time                      |
| Route         | Client side / Server side / Edge side                                   |
| Communicate   | Event emitter / Custom events / Web storage / Query strings / Pub-sub  |

*Ref: Building Micro-Frontends.md — "Micro-Frontends Decisions Framework"*

---

### 3. Domain-Driven Design and Bounded Contexts

**Principle:** Frontends map onto bounded contexts. The team that owns the
context owns the screen — vertical ownership end to end.

**Do:**
- Identify core, supporting, and generic subdomains first (Netflix example:
  catalog = core, voting = supporting, sign-in = generic).
- Use DDD context mapping to draw the seam between frontend and backend; the
  same bounded context should drive both.
- Wait for "last responsible moment" before splitting — premature decomposition
  is more expensive than late refactoring.

**Don't:**
- Define subdomains purely from technical layers (auth, models, views).
- Allow two teams to share ownership of one bounded context.
- Skip the ubiquitous-language step — a shared glossary prevents integration
  errors at the event-bus contract.

**Subdomain cheat-sheet:**
- *Core:* The reason the product exists; treat as a premium citizen.
- *Supporting:* Not differentiating but necessary; can be off-the-shelf.
- *Generic:* Infrastructure-like; usually a vendor or platform concern.

*Ref: Building Micro-Frontends.md — "Domain-Driven Design with Micro-Frontends"*

---

### 4. Conway's Law and the Inverse Conway Maneuver

**Principle:** Architecture mirrors communication structure. If you want a
micro-frontend topology, you must engineer the team topology that produces it.

**Do:**
- Map your user journeys (new-user onboarding, returning-user authentication,
  authenticated browsing) before assigning teams to subdomains.
- Use the inverse Conway maneuver when possible — restructure teams around the
  architecture you want.
- Cluster subdomains that share similarity inside one colocated team so that
  fine-grained communication stays in one room.

**Don't:**
- Allow distributed teams to own the same subdomain — coarse-grained remote
  communication breaks tight coupling.
- Believe architecture can be designed in isolation from org design.
- Reorganize once and never revisit — communication flows drift with headcount.

> "Organizations which design systems are constrained to produce designs which
> are copies of the communication structures of these organizations." — Melvin Conway
*Ref: Building Micro-Frontends.md — "How Do Committees Invent?"*

---

### 5. Vertical Split — One Domain Per Micro-Frontend

**Principle:** Each micro-frontend represents one subdomain end to end. The
application shell loads exactly one at a time.

**Do:**
- Use vertical split when teams have SPA experience and a consistent UX is
  required.
- Keep the application shell technology-agnostic (vanilla JS is acceptable) so
  micro-frontends can pick their own stack.
- Make the shell own only initialization, error fallback, routing and lifecycle
  APIs — never business logic.

**Don't:**
- Put business logic in the shell — that turns the shell into a distributed
  monolith.
- Use a UI framework inside the shell; it bleeds opinions into every remote.
- Share more than web-storage tokens across vertical micro-frontends — query
  strings for volatile data, web storage for persistent.

**Code (shell-level lazy import via React Suspense + Module Federation):**
```jsx
const Catalog    = React.lazy(() => import("Catalog/Catalog"));
const SignIn     = React.lazy(() => import("SignIn/SignIn"));
const MyAccount  = React.lazy(() => import("MyAccount/MyAccount"));

const renderMFE = (MFE) => (
  <React.Suspense fallback="Loading...">
    <MFE />
  </React.Suspense>
);

<Switch>
  <Route path="/myaccount"  render={() => renderMFE(MyAccount)}/>
  <Route path="/shop"       render={() => renderMFE(Catalog)}/>
  <Route path=""            render={() => renderMFE(SignIn)}/>
</Switch>
```
*Ref: Building Micro-Frontends.md — "Vertical-Split Architectures", "Application Shell"*

---

### 6. Horizontal Split — Multiple Micro-Frontends Per View

**Principle:** Multiple micro-frontends compose a single view; each team owns
its piece and communicates via asynchronous events.

**Do:**
- Use horizontal split when a subdomain is reused across many views or when you
  need granular code reuse (payment micro-frontend across checkout, subscription,
  product detail).
- Make one team the *view composer* and responsible for the final rendered page.
- Communicate via pub/sub (event emitter / custom events) — never shared state.

**Don't:**
- Put shared state in a global object — that is the distributed monolith trap.
- Have every team contributing to the same Redux store; every team must own
  its own state.
- Let more than two teams ship into the same view without a designated
  integrator; coordination overhead grows super-linearly with team count.

*Ref: Building Micro-Frontends.md — "Horizontal-Split Architectures"*

---

### 7. Composition: Client-Side (Application Shell)

**Principle:** The application shell is a thin HTML+JS orchestrator that
mounts exactly one micro-frontend (vertical) or several (horizontal) inside
the browser.

**Do:**
- Load micro-frontends lazily through a runtime registry fetched from a JSON
  or an API, not hard-coded in the shell.
- Centralize observability and error fallbacks in the shell.
- Apply CSS prefixes per micro-frontend to defeat style clashes (BEM-style
  `myaccount_avatar__image--active`).

**Don't:**
- Use the shell as a synchronous shared layer during the user's session.
- Couple the shell to any specific UI framework's component model.
- Deploy the shell whenever a micro-frontend changes — load configuration at
  runtime.

**Code (Material-UI seed for CSS isolation):**
```js
const generateClassName = createGenerateClassName({
  seed: 'appshell'
});
// All CSS classes now become e.g. appshell-MuiTypography-h6
```
*Ref: Building Micro-Frontends.md — "Application Shell", "Implementing a Design System"*

---

### 8. Composition: Server-Side (SSR / Tailor / Mosaic)

**Principle:** The origin server assembles HTML from multiple micro-frontend
fragments before responding.

**Do:**
- Use when SEO is non-negotiable (news sites, ecommerce, B2C landing pages).
- Cache the fully composed page at the CDN when content is cacheable.
- Co-locate frontend and backend developers on the composition-layer team.

**Don't:**
- Use for highly personalised content unless you accept a non-cacheable hit
  on every request.
- Skip observability on the composition layer — it becomes the new monolith.
- Treat it as the easier option; server-side composition is the *most powerful*
  and the *most challenging* architecture.

**Code (Holocron / Amex OneApp architecture):**
```
Browser -> Amazon CloudFront -> OneApp server
  -> fetch modules-map JSON (cached in memory)
  -> retrieve Holocron root for the URL
  -> compose micro-frontend modules -> server-side render -> serve HTML
```
*Ref: Building Micro-Frontends.md — "Server Side", "Available frameworks"*

---

### 9. Composition: Edge-Side (ESI)

**Principle:** The CDN itself stitches fragments via Edge Side Includes.

**Do:**
- Use for static, cacheable, geographically distributed content (IKEA catalog
  reference).
- Combine with client-side includes (CSI via h-include) for the dynamic parts.
- Plan for a vendor-specific test harness (Akamai ESI test server in Docker,
  Varnish, NGINX).

**Don't:**
- Use ESI if you need a multi-CDN strategy — implementations diverge across
  vendors.
- Try to inject personalised data at the edge — segments become too large to
  cache meaningfully.
- Assume community tooling will save you — ESI DX is the worst of the four
  composition styles.

**Code (ESI template):**
```html
<html>
 <body>
  Welcome to MFE with ESI
  <esi:include src="https://www.myorigin.com/MFE_A.html"/>
  <esi:include src="https://www.myorigin.com/MFE_B.html"/>
 </body>
</html>
```
*Ref: Building Micro-Frontends.md — "Edge Side"*

---

### 10. Composition: Build-Time (Monorepo Package Imports)

**Principle:** Micro-frontends are npm packages consumed by a host at compile
time. Simplest but most coupling.

**Do:**
- Use when the application is small, owned by one team, and rebuilt often.
- Combine with monorepo tooling (Lerna, Nx, Turborepo) to hoist dependencies.
- Reserve for tactical prototyping before migrating to runtime composition.

**Don't:**
- Use as a long-term architecture when independent deployment is required —
  every consumer rebuilds on every producer change.
- Mix build-time imports with runtime composition in the same view without a
  clear boundary; the cognitive model diverges.
- Skip semver discipline — a single breaking change in a shared package cascades.

*Ref: Building Micro-Frontends.md — "Discovering Micro-Frontend Architectures" (intro)*

---

### 11. Routing: Per-Team vs. Root Composition

**Principle:** Routing decisions follow composition. A client-side composition
implies client-side routing; server-side implies origin routing; edge-side
implies URL-driven fragment assembly.

**Do:**
- Split routing into *global* (shell) and *local* (micro-frontend) levels.
- Make the shell responsible for only the first URL depth (e.g.
  `acme.com/shop`); deeper paths belong to the micro-frontend.
- Validate authentication on every deep-link entry; redirect unauthenticated
  users from authenticated routes via the shell.

**Don't:**
- Allow multiple teams to own the same first-level route.
- Hard-code route tables in the shell; load them via JSON/API so adding a
  micro-frontend does not require a shell redeploy.
- Forget query strings as a fallback for cross-view ephemeral data (product id,
  return URL).

**Code (catalog micro-frontend local routing):**
```jsx
const Catalog = () => {
  let { path } = useRouteMatch();
  return (
    <div>
      <h1>Shop</h1>
      <Switch>
        <Route exact path={`${path}`}                    component={Home}/>
        <Route exact path={`${path}/product/:productId`} component={Details}/>
      </Switch>
    </div>
  );
};
```
*Ref: Building Micro-Frontends.md — "Routing Micro-Frontends", "Catalog Micro-Frontend"*

---

### 12. Communication: Event Emitter / Pub-Sub

**Principle:** When micro-frontends must talk, they publish and subscribe —
never share state directly.

**Do:**
- Inject the event emitter from the host (shell or container) so that no
  micro-frontend has to discover another.
- Document every event name and payload contract in a typed object; freeze
  the constants so typos fail at boot.
- Buffer events that arrive while a late-loading micro-frontend is mounting
  and replay them once mounted.

**Don't:**
- Use a shared Redux store across micro-frontends — that recreates the
  distributed monolith.
- Emit events with raw string literals; freeze the contract object.
- Assume events arrive in order; design payloads to be self-describing.

**Code (NanoEvents emitter across micro-frontends):**
```js
// Inside the host container
if (token) {
  const emitter = createNanoEvents();
  view = <AuthenticatedView emitter={emitter}/>;
}

// Inside the payment micro-frontend
const onPaymentChanged = () => {
  props.emitter.emit("paymentChanged", "May 2021");
};

// Inside the account-details micro-frontend
const [lastPaymentDate, setPaymentChanged] = useState("Jan 2021");
props.emitter.on("paymentChanged", date => setPaymentChanged(date));
```
*Ref: Building Micro-Frontends.md — "Account Management Micro-Frontend"*

---

### 13. Communication: Web Storage, Query Strings, Custom Events

**Principle:** Pick the most ephemeral channel that fits the data lifetime.

**Do:**
- Use **session/local storage** for tokens, user preferences, settings that
  must outlive a single view.
- Use **query strings** for volatile data (product ID, return URL) and
  redirect-after-login flows.
- Use **CustomEvent** on the window object when only same-tab decoupled
  notification is needed.

**Don't:**
- Store sensitive data (passwords, long-lived tokens) in query strings — they
  end up in server logs.
- Share storage across subdomains unless you control the cookie domain.
- Assume every browser handles `localStorage` quota identically — guard with
  try/catch and fall back to cookies.

**Code (CustomEvent):**
```js
new CustomEvent('myCustomEvent', { detail: { someObj: 'customData' } });
window.dispatchEvent(event);
```
*Ref: Building Micro-Frontends.md — "Micro-Frontends Communication"*

---

### 14. Authentication Across Micro-Frontends

**Principle:** Authenticate at the edge, share the token via web storage, and
let every micro-frontend validate before rendering.

**Do:**
- Use web storage (or cookies for cross-subdomain) as the contract medium.
- Store the JWT immediately after sign-in and read it from every authenticated
  micro-frontend.
- Run a short-TTL refresh loop so a stale token never blocks the user.

**Don't:**
- Hardcode tokens into URLs or query strings.
- Re-implement auth in every micro-frontend; share a thin SDK instead.
- Forget that localStorage is origin-scoped — every micro-frontend must live on
  the same subdomain (or use cookies for cross-subdomain).

**Code (sign-in → token in sessionStorage):**
```jsx
const SignIn = () => {
  let history = useHistory();
  const onSignIn = () => {
    window.sessionStorage.setItem("token", token);
    history.push("/shop");
  };
  // ...
};
```
*Ref: Building Micro-Frontends.md — "Authentication Micro-Frontend"*

---

### 15. State Sharing: Local First, Event Bus Second

**Principle:** Every micro-frontend owns its state. Cross-MFE state is an
exception, not the rule.

**Do:**
- Encapsulate state inside a MobX-State-Tree, Redux slice, or equivalent owned
  by the team.
- Use composition-friendly state libraries so future splits are easier.
- Use a publish/subscribe boundary for the rare cross-MFE event.

**Don't:**
- Build a global Redux store shared by all micro-frontends.
- Allow one micro-frontend to call into another's state object directly.
- Treat shared state as the easy option — it is the most expensive option
  socially and technically.

> "Shared state between multiple micro-frontends represents an antipattern."
*Ref: Building Micro-Frontends.md — "Micro-frontend communication" (Figure 4-14)*

---

### 16. Ownership: One Team Per Business Capability

**Principle:** A micro-frontend must have exactly one team owner; ownership
extends end to end (frontend, backend, infrastructure).

**Do:**
- Use a single two-pizza team per subdomain (8–9 people max).
- Let the team pick its own libraries, framework, CI tooling within guardrails.
- Require an owner team before merging a micro-frontend into production.
- Add an *adapter micro-frontend* for legacy code so a new team can own it
  incrementally.

**Don't:**
- Split ownership across backend team + frontend team + DevOps team — that
  recreates Conway's law in miniature.
- Adopt a micro-frontend that nobody on the team has full-stack confidence in.
- Leave a micro-frontend unowned during the strangler migration.

*Ref: Building Micro-Frontends.md — "Embedding a Legacy Application", "Decentralization Implications"*

---

### 17. When to Use Micro-Frontends

**Principle:** Adopt micro-frontends when organisational complexity (multiple
teams, distributed timezones, conflicting release cadences) dominates the
cost of integration.

**Use when:**
- 3+ teams own the frontend.
- Time to market suffers because of code freezes and merge conflicts.
- You need to migrate a legacy SPA iteratively (strangler pattern).
- You must support multiframework or polyglot UI stacks.
- You must enable hundreds of developers to ship independently.

**Do:**
- Start simple (vertical split + application shell).
- Make a clear business case tied to delivery velocity, not technical curiosity.
- Run a PoC before committing.

**Don't:**
- Adopt for one-team, one-repo projects.
- Adopt because microservices are popular — micro-frontends have their own
  cost profile.
- Adopt before you have a solid automation and observability culture.

*Ref: Building Micro-Frontends.md — "Why Should We Use Micro-Frontends?", "Micro-Frontends Are Not a Silver Bullet"*

---

### 18. When NOT to Use Micro-Frontends

**Principle:** The complexity tax is real. Refuse the architecture when the
problem does not require it.

**Do not use when:**
- A single team owns the entire frontend.
- The application is a small marketing site.
- Release cadence is not the bottleneck.
- The team lacks CI/CD, observability, and design-system investment.
- The micro-frontends would have heavy, chatty inter-communication — that is a
  smell that the seam is wrong.

**Mitigation:** Start as a monolith or modular monolith; migrate when team
boundaries force it.

*Ref: Building Micro-Frontends.md — "When would you suggest using micro-frontends" (interviews with Joel Denning, Erik Grijzen)*

---

### 19. Trade-offs: Consistency vs. Autonomy

**Principle:** Every decision is a trade-off. Optimise for the *least worst*
outcome, not the "best".

**Do:**
- Use the architecture scoring tables (Deployability, Modularity, Simplicity,
  Testability, Performance, DX, Scalability, Coordination) when comparing
  architectures.
- Revisit trade-offs at every architectural inflection point.
- Document the trade-off you accepted in an ADR.

**Don't:**
- Believe any architecture is "best" — context drives the answer.
- Optimise every axis — trade-offs are zero-sum.
- Conflate *technical* trade-offs with *organisational* ones.

> "Never shoot for the best architecture, but rather the least worst
> architecture." — Neal Ford & Mark Richards
*Ref: Building Micro-Frontends.md — "Architecture and Trade-offs"*

---

### 20. Trade-offs: Performance vs. Developer Experience

**Principle:** Performance budgets protect users; DX tools protect developers.
Cap both explicitly.

**Do:**
- Set a **performance budget** (bundle size, JS parse time) per micro-frontend
  and enforce it in CI.
- Set a **DX budget** (max minutes for CI feedback, max commands to run a
  local micro-frontend) and report against it.
- Use Lighthouse CLI in CI for every artifact.

**Don't:**
- Allow a micro-frontend to grow without bound.
- Make developers fight tooling they did not choose.
- Let performance regressions ship because DX made them easy.

*Ref: Building Micro-Frontends.md — "Performance and Micro-Frontends"*

---

### 21. Anti-Pattern: Distributed Frontend Monolith

**Principle:** Independent deployment is the test of independence. If you must
coordinate releases, you have a monolith with extra steps.

**Do:**
- Detect the smell: shared global state, mandatory joint releases, frequent
  coupled tickets.
- Refactor by introducing explicit contracts (events, query strings, web
  storage) instead of shared modules.
- Validate via "blast radius" analysis: how many teams are blocked by a single
  change?

**Don't:**
- Share a global Redux store.
- Synchronise deployments via a release train.
- Use a "shared library of business logic" — that is a monolith disguised.

*Ref: Building Micro-Frontends.md — "Micro-frontend communication", Chapter 10 interviews*

---

### 22. Anti-Pattern: Premature Decomposition

**Principle:** Wait for the *last responsible moment* before splitting. You will
have more data about traffic and value later.

**Do:**
- Use analytics (GA, Mixpanel) to see which flows are actually used.
- Split based on data (e.g. only 4% of users hit "My Account" → small
  micro-frontend is fine).
- Combine analytics with DDD subdomain mapping before drawing the seam.

**Don't:**
- Split on day 1 — initial data is poor.
- Use technical layering (one MFE per framework folder) as the decomposition
  driver.
- Treat premature decomposition as cheap — untangling later is hard.

*Ref: Building Micro-Frontends.md — "How to Define a Bounded Context"*

---

### 23. Anti-Pattern: Over-Engineering into Nano-Frontends

**Principle:** A micro-frontend is a *business* artifact, not a *component*.
Once you blur the line, you lose independence.

**Rule of thumb (the book's component vs. micro-frontend test):**
- Component: extended via props for many use cases.
- Micro-frontend: encapsulates logic, communicates via events.

**Do:**
- Keep the granularity at subdomain, not widget.
- Prefer one micro-frontend per page-section-team combination.

**Don't:**
- Create one MFE per Material-UI component.
- Allow component-style extension via attribute injection on a micro-frontend
  shell (that couples container to contract).

*Ref: Building Micro-Frontends.md — "Components Versus Micro-Frontends"*

---

### 24. Design System and Shared Component Library

**Principle:** A design system is the single source of truth for visual and
behavioural consistency in a distributed UI.

**Do:**
- Layer the system: **design tokens → basic components → UI components → MFE**.
- Implement design-system components as **web components** so they survive a
  framework migration.
- Enforce the latest version via a CI check on every micro-frontend's
  `package.json`.
- Run a fitness function that fails the build if the version is more than one
  major behind.

**Don't:**
- Treat the design system as a one-time delivery — it needs ongoing governance.
- Duplicate the same complex component (video player) in every micro-frontend;
  share it.
- Couple micro-frontends to the design system at runtime unless you really need
  evergreen updates; usually compile-time integration is enough.

**Code (per-team seed prefix with Material-UI):**
```js
const generateClassName = createGenerateClassName({ seed: 'myaccount' });
// Output: myaccount-MuiTypography-h6
```
*Ref: Building Micro-Frontends.md — "Implementing a Design System"*

---

### 25. Cross-Team Communication & Contracts

**Principle:** Codify inter-team contracts the same way you codify APIs —
through documentation, automation, and review.

**Do:**
- Use **RFCs** for changes that touch multiple teams; include motivation,
  alternatives, drawbacks.
- Use **ADRs** for architectural decisions; capture context, status, outcome.
- Document every published event (name + payload) in a single, searchable
  source.
- Use **PR/FAQs** (Amazon "working backwards") for new cross-team features.

**Don't:**
- Rely on verbal sync meetings as the primary contract medium.
- Merge an event-payload change without notifying consumers.
- Allow undocumented shared APIs to exist for more than one sprint.

*Ref: Building Micro-Frontends.md — "Requests for Comments", "Architectural Decision Records", "Working Backward"*

---

### 26. Testing: Unit, Integration, E2E, Contract

**Principle:** Test at the level the failure would manifest.

**Do:**
- Run unit + integration tests **inside each micro-frontend's pipeline** —
  fast, isolated, owned by the team.
- Use **contract tests** to verify shell ↔ micro-frontend interfaces.
- Run **end-to-end tests** in staging or production (with feature flags).
- Use **visual regression** to catch CSS-prefix regressions.
- Add **fitness functions**: bundle size, Lighthouse score, code coverage,
  cyclomatic complexity, security.

**Don't:**
- Test the whole shell in every micro-frontend's pipeline (slow, redundant).
- Skip e2e on horizontal-split views — that is where regressions hide.
- Run e2e only in production without a rollback plan.

**Code (CI bundle-size fitness):**
```yaml
# pseudo
- name: bundle budget
  run: |
    SIZE=$(stat -c%s dist/mfe.js)
    if [ "$SIZE" -gt 250000 ]; then exit 1; fi
```
*Ref: Building Micro-Frontends.md — "Testing Micro-Frontends", "Fitness Functions"*

---

### 27. Build and Deployment: Monorepo vs. Polyrepo

**Principle:** Pick the repository model that matches your team and CI budget.

**Monorepo (Lerna, Nx, Turborepo):**
- Do when you want code-sharing, easy refactors, atomic commits, fast
  on-boarding.
- Don't when build times explode or trunk discipline is weak.
- Requires trunk-based development and disciplined developers.

**Polyrepo (one repo per micro-frontend):**
- Do when teams are large and siloed, when access control matters, when
  release cadence varies per project.
- Don't when discoverability and code duplication become bottlenecks.
- Requires a clear naming convention and a shared internal library pattern.

**Hybrid:** One polyrepo *per bounded context* — captures monorepo's strengths
inside the context while keeping isolation across contexts.

*Ref: Building Micro-Frontends.md — "Version Control", "Polyrepo", "Monorepo"*

---

### 28. Continuous Integration Pipeline Anatomy

**Principle:** Six areas — version control, pipeline init, code-quality review,
build, post-build review, deployment.

**Do:**
- Clone with `--depth 1` to keep monorepo CI fast.
- Run lint, unit tests, contract tests, design-system-version checks in
  parallel.
- Publish the artifact to a central repository (Nexus, Artifactory, S3) so
  every environment promotes the same bytes.
- Run Lighthouse and visual regression in post-build before deployment.

**Don't:**
- Use full-history clones for CI — every commit is the only commit that
  matters.
- Re-test shared libraries in every micro-frontend's pipeline.
- Deploy to production directly from a developer's machine.

*Ref: Building Micro-Frontends.md — "Automation Pipeline Case Study", "Pipeline Initialization"*

---

### 29. Deployment Strategies: Blue-Green and Canary

**Principle:** Reduce release risk by controlling how traffic reaches a new
version.

**Blue-Green:** Two environments; switch the router after smoke tests in prod.
Use when you want a clean rollback lever.

**Canary:** Gradually shift traffic (5% → 20% → 50% → 100%) while watching
metrics. Use when you want signal-driven promotion.

**Do:**
- Use **Lambda@Edge** or **Cloudflare Workers** to make routing decisions
  close to the user.
- Stamp the assigned version in a cookie so the user sticks to it for the
  session.
- Tie promotion to error-rate and engagement metrics, not just minutes since
  deploy.

**Don't:**
- Run canary without observability on the new version.
- Skip the rollback plan because canary "should" be safe.

**Code (version-router config):**
```json
{
  "homepage":{
    "v.1.1.0": { "traffic": 20, "url": "acme.com/mfes/homepage-1_1_0.html" },
    "v.1.2.2": { "traffic": 80, "url": "acme.com/mfes/homepage-1_2_2.html" }
  },
  "signin":{
    "v.4.0.0": { "traffic": 90, "url": "acme.com/mfes/signin-4_0_0.html" },
    "v.4.1.5": { "traffic": 10, "url": "acme.com/mfes/signin-4_1_5.html" }
  }
}
```
*Ref: Building Micro-Frontends.md — "Blue-Green Deployment Versus Canary Releases"*

---

### 30. Strangler Pattern for Incremental Migration

**Principle:** Replace a monolith frontend piece by piece, running both
side-by-side, with a router redirecting legacy URLs to the new platform.

**Do:**
- Keep three versions alive (legacy, hybrid, micro-frontends) until the
  legacy is gone.
- Use Lambda@Edge or an API gateway to route between them based on URL.
- Redirect from legacy to absolute URLs so the router logic stays consistent.
- Start with the highest-value subdomain (catalog) — measure, learn, then
  scale the pattern.

**Don't:**
- Big-bang rewrite the entire frontend.
- Forget to keep a working "everything-is-legacy" fallback during the
  transition.

*Ref: Building Micro-Frontends.md — "Strangler Pattern", "From Monolith to Micro-Frontends"*

---

### 31. Performance: Bundle Size and Lazy Loading

**Principle:** Optimise per-user-flow, not per-page. A user who never visits
"My Account" should never download its code.

**Do:**
- Set a **performance budget** per micro-frontend and enforce it in CI
  (Lighthouse CLI).
- Lazy-load micro-frontends inside `React.Suspense` or equivalent.
- Use **dynamic remote containers** so a new micro-frontend does not require
  a shell redeploy.
- Consider bundling shared libraries separately so the CDN can cache them
  longer.

**Don't:**
- Force every micro-frontend to bundle the entire design system — share at
  the right layer.
- Load micro-frontends on initial paint unless they are above the fold.
- Mix large vendor libraries with hot business logic in the same chunk.

*Ref: Building Micro-Frontends.md — "Performance and Micro-Frontends", "Dynamic Remote Containers"*

---

### 32. SEO: Dynamic Rendering and Server-Side Composition

**Principle:** Crawlers need HTML in the first response. Two main strategies.

**Do:**
- Use **dynamic rendering**: redirect user-agents matching Googlebot/Bingbot to
  a pre-rendered version (Puppeteer / Rendertron) — does not penalise SEO.
- Prefer **server-side composition** when SEO is non-negotiable from day one.
- Use Lambda@Edge user-agent sniffing (`crawler-user-agents` npm) for cheap
  detection.

**Don't:**
- Rely on client-side hydration alone for crawler indexing — many crawlers do
  not execute JS, or do so slowly.
- Forget to serve a fallback when the pre-render service is down.

*Ref: Building Micro-Frontends.md — "Search Engine Optimization"*

---

### 33. Observability: Errors, Logs, Tracing

**Principle:** A distributed UI demands distributed observability. Without it,
you cannot answer "which micro-frontend broke?"

**Do:**
- Standardise a frontend observability SDK (Sentry, New Relic, LogRocket) and
  enforce it in every micro-frontend.
- Capture stack traces, user journey (last N events), browser, OS, country,
  MFE version.
- Wire alerts into PagerDuty / Opsgenie for production exceptions.
- Track web vitals (LCP, FID, CLS) per micro-frontend.

**Don't:**
- Silo logs per micro-frontend with no cross-MFE correlation id.
- Ship a micro-frontend that does not report errors — observability is part
  of "done".

*Ref: Building Micro-Frontends.md — "Observability", "Highly Observable"*

---

### 34. Security: CSP, Isolation, Auth

**Principle:** Distributed UIs widen the attack surface. Defence in depth is
non-negotiable.

**Do:**
- Use **Content Security Policy** headers to restrict script sources to your
  CDN.
- Pin iframe `sandbox` attribute (e.g. `allow-scripts allow-forms`) for
  isolation.
- Use **HTTP-only, Secure, SameSite** cookies for token storage to defeat XSS
  exfiltration.
- Validate JWTs at the API gateway, not just at the micro-frontend.
- Use Shadow DOM (web components) to encapsulate style and behaviour.

**Don't:**
- Trust `localStorage` for long-lived tokens (XSS exfiltration risk).
- Embed third-party iframes without `sandbox`.
- Allow micro-frontends to load arbitrary JS from arbitrary origins.

*Ref: Building Micro-Frontends.md — "Cross-Site Scripting" sidebar, "Authentication"*

---

### 35. Module Federation (Webpack 5) — Host and Remote

**Principle:** A **host** loads shared libraries and micro-frontends
(**remotes**) at runtime. Single-direction sharing is the recommended pattern.

**Do:**
- Specify `singleton: true` for shared libraries you want loaded once
  (React, design system).
- Use `eager: true` only for libraries that must be available synchronously.
- Prefer `requiredVersion` to pin compatible ranges.
- Use `shareKey`/`shareScope` to keep different versions of the same library in
  different scopes.
- Configure a **dynamic remote container** so the shell can load new MFEs
  without redeploying.

**Don't:**
- Make Module Federation bidirectional (host ↔ remote ↔ host) — flatten the
  hierarchy and lose debuggability.
- Rely on the default "greatest version wins" without `requiredVersion` —
  silent upgrade bugs await.
- Forget to test what happens when a remote is unreachable.

**Code (host config with remotes + shared):**
```js
new ModuleFederationPlugin({
  name: "AppShell",
  remotes: {
    MyAccount: "MyAccount@http://localhost:3004/remoteEntry.js",
    Catalog:   "Catalog@http://localhost:3002/remoteEntry.js",
    SignIn:    "SignIn@http://localhost:3003/remoteEntry.js"
  },
  shared: {
    react:           { singleton: true },
    "react-dom":     { singleton: true },
    "react-router-dom": { singleton: true },
    "@material-ui/core":  { singleton: true },
    "@material-ui/icons": { singleton: true }
  }
})
```

**Code (remote config):**
```js
new ModuleFederationPlugin({
  name: "SignIn",
  filename: "remoteEntry.js",
  exposes: { "./SignIn": "./src/SignIn" },
  shared:   { /* same shared map */ }
})
```
*Ref: Building Micro-Frontends.md — "Module Federation", "Module Federation 101", "Application Shell"*

---

### 36. Web Components as Encapsulated Wrappers

**Principle:** Custom elements + Shadow DOM = framework-agnostic encapsulation
ideal for design systems and shared widgets.

**Do:**
- Use web components for design-system primitives that may outlive any single
  framework.
- Expose attributes for configuration but not for behaviour injection.
- Provide callbacks/events for inter-component communication.
- Fall back to lightweight polyfills (only the ones the browser needs) for
  legacy targets.

**Don't:**
- Put SEO-critical content inside the Shadow DOM — crawlers may not see it.
- Use customised built-in elements on WebKit without testing — bugs exist.
- Treat web components as the magic answer for every micro-frontend boundary —
  they are best for design-system wrappers, not for whole-app composition.

*Ref: Building Micro-Frontends.md — "Web Components"*

---

### 37. iframes — Maximum Isolation, Maximum Cost

**Principle:** iframes are the strongest sandbox available in the browser;
use when isolation matters more than performance.

**Do:**
- Use the `sandbox` attribute (`allow-scripts allow-forms`) for granular
  privilege control.
- Communicate via `postMessage` or via an injected event emitter on
  `contentWindow`.
- Use iframes for desktop apps, intranet tools, B2B apps where SEO and
  performance are not critical.
- Use them as **adapter micro-frontends** for legacy code during strangler
  migrations.

**Don't:**
- Use iframes for consumer websites — performance and accessibility suffer.
- Try to coordinate fluid responsive layouts across many iframes.
- Skip e2e testing — DOM nesting across iframes makes selectors verbose.

**Code (sandbox + postMessage):**
```html
<iframe sandbox="allow-scripts allow-forms"
        src="https://mfe.mywebsite.com/catalog"/>
```
*Ref: Building Micro-Frontends.md — "Iframes"*

---

### 38. Single SPA, Piral, OpenComponents, Qiankun

**Principle:** Frameworks are choices; pick by team skill and target environment.

| Framework         | Best for                                                                 |
|-------------------|--------------------------------------------------------------------------|
| single-spa        | Mature orchestrator with life-cycle hooks; horizontal + vertical splits. |
| qiankun           | single-spa superset; HTML-entry-point MFEs (qiankun micro-app).          |
| Piral            | App-shell + plugin model for portal-style micro-frontends.               |
| OpenComponents   | Server-side SSR composition with registry (OpenTable, Skyscanner).       |
| Mosaic / Tailor  | SSI/ESI-style composition (Zalando legacy stack).                        |
| Podium / Puzzle.js | Server-side composition with fragment contracts.                       |
| Module Federation| Webpack 5 native plugin for runtime composition.                        |
| Luigi (SAP)      | iframe-based enterprise micro-frontends with SAP integration.            |

**Do:**
- Evaluate the framework's developer experience against your team skills.
- Prefer a thin orchestration layer over a heavyweight framework.
- Plan an exit strategy — every framework choice is a future migration.

**Don't:**
- Pick a framework before applying the decisions framework.
- Confuse a framework with an architecture; the framework is one tool inside
  the architecture.

*Ref: Building Micro-Frontends.md — "Available frameworks", "Iframes Available framework", "Micro-Frontend Technical Implementation"*

---

### 39. Case Study: Spotify — iframe-based Desktop, SPA Web

**Principle:** Spotify's desktop app embeds each micro-frontend as a `.spa`
artifact (HTML + CSS + manifest + JS bundle) inside an iframe, communicating
via a C++ bridge. The web player started with the same approach but moved
back to an SPA due to performance.

**Do:**
- Reuse desktop patterns for sandboxed, performance-tolerant environments.
- Treat failed experiments as data — Spotify's web abandonment of iframes is a
  case study, not a defeat.

**Don't:**
- Force a desktop pattern onto consumer web without measuring performance.
- Assume iframes scale linearly — Spotify web proved they do not.

*Ref: Building Micro-Frontends.md — "Spotify" (Micro-Frontends in Practice)*

---

### 40. Case Study: DAZN — Bootstrap Orchestrator for Smart TVs

**Principle:** DAZN's fully client-side architecture uses a Bootstrap
orchestrator that loads SPAs at runtime whenever a user moves between
business domains. Targets web, smart TVs, set-top boxes, consoles.

**Do:**
- Use a custom client-side agent when CDN or server composition is
  unavailable (low-end TVs, consoles).
- Keep the orchestrator small; it is always loaded.

**Don't:**
- Assume every target supports modern JS runtimes — DAZN explicitly
  constrained the architecture to survive low-power devices.

*Ref: Building Micro-Frontends.md — "DAZN", "From Monolith to Micro-Frontends"*

---

### 41. Case Study: IKEA (ESI + CSI)

**Principle:** IKEA's catalog in some countries combines ESI at the CDN with
CSI (`h-include`) on the client for dynamic regions. Static everywhere
possible, dynamic only where needed.

**Do:**
- Mix ESI and CSI to balance CDN scalability with client interactivity.
- Use CSI for the dynamic parts of an otherwise static page.

**Don't:**
- Try to cache personalised ESI content — segments explode.

*Ref: Building Micro-Frontends.md — "Use cases" (Edge Side)*

---

### 42. Case Study: New Relic — Horizontal at Scale

**Principle:** New Relic serves cloud-monitoring dashboards with horizontal-
split micro-frontends; small teams own individual dashboards that are
lazy-loaded inside an application shell. Strong design-system ownership and
SDK injection keep the UX consistent.

**Do:**
- Centralise React (or chosen framework) version + design system via the
  shell to defeat version sprawl.
- Provide a CLI for scaffolding MFEs so every team starts from the same
  baseline.
- Use a *SDK on the platform* — all micro-frontends receive the same UI
  primitives and platform APIs.

**Don't:**
- Let every team pick its own React version — performance and bundle size
  collapse fast.
- Skip the design-system ownership question — "everyone contributes" usually
  means "nobody maintains".

*Ref: Building Micro-Frontends.md — Appendix interview with Erik Grijzen (New Relic)*

---

### 43. Case Study: edX — Capabilities Model for Replatforming

**Principle:** edX used a *capabilities model* to escape a 1.5M-line Django
monolith. Capabilities are coarse-grained platform APIs (auth, analytics,
i18n) that every micro-frontend consumes, replacing the previous server-
rendered views.

**Do:**
- Define a small set of platform capabilities before launching MFEs.
- Use a frontend-platform library to bundle logging, analytics, auth, i18n.
- Use frontend-build for lint, test, build, dev-server standardisation.

**Don't:**
- Try to maintain feature parity while replatforming — that multiplies risk.
  Use the strangler pattern instead.

*Ref: Building Micro-Frontends.md — Appendix interview with Nimisha Asthagiri (edX)*

---

### 44. Migration Playbook: From SPA to Micro-Frontends (ACME Inc.)

**Principle:** Use data + DDD + the decisions framework in that order, then
build outward.

**Steps:**
1. Inventory user journeys with analytics.
2. Identify subdomains (core/supporting/generic).
3. Apply the decisions framework (define, compose, route, communicate).
4. Build the application shell first; release it to production.
5. Build the highest-value micro-frontend first (catalog in ACME's case).
6. Run the strangler pattern: keep legacy alive, route traffic incrementally.
7. Move authentication last — it touches everything.
8. Add fitness functions for design-system version, bundle size, Lighthouse.

**Do:**
- Use Lambda@Edge to flip traffic between legacy SPA and new shell.
- Use `git clone --depth 1` in CI for monorepo performance.
- Maintain a semver-friendly naming for artifacts.

**Don't:**
- Migrate authentication first — it is the highest-risk, lowest-value first
  step.
- Forget to define a "rollback to legacy" lever for every release.

*Ref: Building Micro-Frontends.md — "From Monolith to Micro-Frontends" (entire chapter)*

---

### 45. The Strangler + Canary Combo at ACME

**Principle:** Combine canary releases with the strangler pattern for a
bulletproof migration.

**Mechanics:**
- Application shell loads configuration from API.
- Lambda@Edge assigns each user a random 1–100 bucket.
- Configuration maps bucket range → version for each MFE.
- Cookie stores the assigned version to keep the user pinned.
- Move users off the new version by changing the config — no redeploy.

**Do:**
- Map micro-frontend versions using semver; cache by hash.
- Use the major version in the config so backward-compatible upgrades flow
  automatically.

**Don't:**
- Skip the cookie — without it, users bounce between versions per request.

*Ref: Building Micro-Frontends.md — "Implementing Canary Releases"*

---

### 46. Service Dictionary — API Endpoint Discovery

**Principle:** Don't bake endpoints into the frontend. Load them from a
service dictionary at startup.

**Do:**
- Return JSON in the shape `service -> version -> url`.
- Group endpoints by bounded context.
- Cache the dictionary at the CDN.
- Use a header (`X-Experiment-Id`) to test new endpoints in production
  without affecting real users.

**Don't:**
- Hardcode endpoint URLs in the JS bundle.
- Ship a shared client library of "endpoint constants" — version drift
  follows.

**Code (dictionary shape):**
```json
{
  "my_amazing_api": {
    "v1": "https://api.acme.com/v1/my_amazing_api",
    "v2": "https://api.acme.com/v2/my_amazing_api"
  },
  "my_super_awesome_api": {
    "v1": "https://api.acme.com/v1/my_super_awesome_api"
  }
}
```
*Ref: Building Micro-Frontends.md — "Working with a Service Dictionary"*

---

### 47. API Gateway vs. BFF vs. Service Dictionary

**Principle:** Different entry-point patterns for different aggregation needs.

| Pattern            | Aggregation | Best for                                                  |
|--------------------|-------------|-----------------------------------------------------------|
| Service Dictionary | None        | Endpoint discovery without coupling to backend topology. |
| API Gateway        | None        | Single entry point, central auth, rate-limiting, routing. |
| BFF                | Heavy       | Cross-platform apps, dashboard aggregation per device.    |
| GraphQL            | Medium      | Schema federation across subdomains.                     |

**Do:**
- Match the pattern to the subdomain's data shape.
- One BFF per subdomain (or per platform) is healthier than one mega-BFF.

**Don't:**
- Use a BFF for a vertical split where each micro-frontend already knows its
  endpoints — adds latency without value.
- Couple multiple BFFs to the same microservices without SLAs.

*Ref: Building Micro-Frontends.md — "API Integration and Micro-Frontends"*

---

### 48. GraphQL Schema Federation

**Principle:** Each team owns its GraphQL schema; the gateway composes them
into one data graph.

**Do:**
- Use Apollo Federation (or similar) to combine per-team schemas.
- Design the schema UI-first, not database-first.
- Plan schema reviews with multiple teams — silos inside the GraphQL layer
  defeat the purpose.

**Don't:**
- Federate before you need it — federation has operational cost.
- Skip the design-review step; GraphQL schemas calcify quickly.

*Ref: Building Micro-Frontends.md — "Using GraphQL with Micro-Frontends"*

---

### 49. WebSockets with Micro-Frontends

**Principle:** One socket per application, not one per micro-frontend.

**Do:**
- Open the WebSocket in the application shell.
- Forward messages to micro-frontends via the event emitter.
- Buffer messages that arrive while a slow-loading micro-frontend is
  mounting.

**Don't:**
- Open one socket per micro-frontend — connection cost compounds.
- Couple the WebSocket lifecycle to any single micro-frontend.

*Ref: Building Micro-Frontends.md — "WebSocket and micro-frontends"*

---

### 50. Localization in Micro-Frontends

**Principle:** Each micro-frontend owns the labels it needs. The dictionary
API returns only those.

**Do:**
- Pass `subdomain + language + country` in the labels API request.
- Cache labels at the CDN by `(subdomain, country, language)`.
- Keep a legacy endpoint as a fallback during migration.

**Don't:**
- Send every label for every micro-frontend to every user.
- Hardcode labels in JS bundles — kills i18n agility.

*Ref: Building Micro-Frontends.md — "Localization"*

---

### 51. Developer Experience (DX) for Micro-Frontends

**Principle:** Without a frictionless DX, teams will route around the
architecture.

**Do:**
- Provide a CLI scaffold (`create-mfe`) with the company's standards baked
  in (logging, observability, design-system imports).
- Use import-map overrides (single-spa) so a developer runs *only* their MFE
  locally.
- Provide dashboards that show MFE versions deployed per environment.
- Offer on-demand environments (Kubernetes namespaces, spot instances) for
  cross-MFE testing.

**Don't:**
- Force every developer to spin up the entire app on every change.
- Hide the build pipeline behind a "platform team only" wall — empower devs
  to own their CI.

*Ref: Building Micro-Frontends.md — "Developer Experience"*

---

### 52. CI/CD: Reverse Proxy for Local E2E

**Principle:** Use a webpack DevServer proxy (or equivalent) to assemble a
local MFE against staging/prod siblings.

**Code:**
```js
// webpack.config.js
{
  devServer: {
    proxy: {
      '/catalog-mfe': {
        target: 'https://other-server.example.com',
        secure: false
      }
    }
  }
}
// Multiple entries
proxy: [
  {
    context: ['/catalog-mfe/**', '/myaccount-mfe/**'],
    target: 'https://other-server.example.com',
    secure: false
  }
]
```
*Ref: Building Micro-Frontends.md — "Webpack Dev Server Proxy Configuration"*

---

### 53. Adapter Pattern for Legacy Embedding

**Principle:** Wrap a legacy app in an iframe inside an adapter
micro-frontend that translates its events into your event bus.

**Do:**
- Use the adapter micro-frontend as the anti-corruption layer.
- Pass configuration via query strings.
- Translate iframe `postMessage` into the host's event emitter.

**Don't:**
- Pollute the application shell with legacy-code knowledge.
- Couple the legacy's data model to the new platform's vocabulary.

*Ref: Building Micro-Frontends.md — "Embedding a Legacy Application"*

---

### 54. Cart Component Without Domain Leak

**Principle:** Let the team that owns checkout own the cart component
even when it lives inside the application shell.

**Mechanics:**
- Shell mounts the cart component (compiled as a separate MFE or library).
- Cart subscribes to product-added events via the event emitter.
- Cart controls its own visibility (no shell-side logic).

*Ref: Building Micro-Frontends.md — "Developing the Checkout Experience"*

---

### 55. Dynamic Remote Containers

**Principle:** Load Module Federation remotes at runtime from a registry,
not from a hard-coded config.

**Do:**
- Fetch the list of remotes from an API.
- Decide which version to load based on user country, role, canary policy.
- Add a new micro-frontend without redeploying the shell.

**Don't:**
- Hardcode remote URLs in `webpack.config.js` past version 1.

*Ref: Building Micro-Frontends.md — "Implementing Dynamic Remotes Containers"*

---

### 56. Webpack Lock-In — Risk Management

**Principle:** Module Federation is webpack-5 native; that is both power and
risk.

**Do:**
- Treat the choice as a 3-to-5-year decision, not a 10-year one.
- Maintain an exit plan: keep MFEs small enough to rewrite in another tool.
- Use Fronts (a wrapper) when you want Module Federation's ergonomics without
  the plugin.

**Don't:**
- Build 100+ MFEs in webpack without considering escape cost.
- Confuse ergonomics with safety; the simplicity is the lock-in.

*Ref: Building Micro-Frontends.md — "Webpack Lock-in"*

---

### 57. Two-Pizza Team Math

**Principle:** Communication links in a team grow as `n(n-1)/2`. Double the
team to quadruple the links.

**Do:**
- Keep teams at 6–9 people.
- Choose cross-functional (features) teams when a micro-frontend is owned
  end-to-end.
- Choose component teams when cross-platform (web + mobile + TV) consumes
  shared APIs.

**Don't:**
- Build a 15-person "frontend platform" team — coordination cost kills
  delivery.

*Ref: Building Micro-Frontends.md — "A Two-Pizza Team", "Features Versus Components Teams"*

---

### 58. Community of Practice & Town Halls

**Principle:** Distributed architectures need distributed communication.

**Do:**
- Run biweekly community-of-practice meetings for frontend developers.
- Use town halls for cross-discipline updates.
- Use mob programming sessions during the community-of-practice for hard
  problems.

**Don't:**
- Substitute documentation for synchronous conversation entirely — context
  is best transmitted in person.
- Skip onboarding rituals; new hires need curated context.

*Ref: Building Micro-Frontends.md — "Community of Practice and Town Halls"*

---

### 59. ADR Template

**Principle:** Capture *context* and *trade-offs* at decision time, not
after.

**Sections:**
- Status (draft / agreed)
- Stakeholders
- Outcome
- Due date
- Owners
- Introduction (company context + problem)
- Forces (parallel streams pushing toward change)
- Options (with pros/cons)
- Final decision and rationale
- Appendix

*Ref: Building Micro-Frontends.md — "Architectural Decision Records"*

---

### 60. Performance Budget Enforcement

**Principle:** A budget is a number + an enforcement point.

**Do:**
- Allocate a per-micro-frontend budget (e.g. 100 KB business + 250 KB shared).
- Fail the build if exceeded.
- Re-evaluate budgets after every major refactor.

**Don't:**
- Set budgets in a wiki and forget them.
- Treat Lighthouse as the only metric — bundle size, parse time, TTI matter
  too.

*Ref: Building Micro-Frontends.md — "Performance and Micro-Frontends"*

---

### 61. Inverse Conway Maneuver — When to Use

**Principle:** Restructure teams around the architecture you want, not the
architecture your teams have.

**Do:**
- Apply when you have authority to move people.
- Apply when the new team boundary is stable enough to last 12+ months.
- Pair with strong communication rituals (CoP, town halls).

**Don't:**
- Reorganise more than once a year.
- Use the inverse Conway maneuver as a substitute for technical discipline.

*Ref: Building Micro-Frontends.md — "How Do Committees Invent?"*

---

### 62. Loose vs. Tight Coupling Trade-offs

**Principle:** Loose coupling enables autonomy; tight coupling enables
consistency. Pick consciously.

**Do:**
- Default to loose coupling (events, query strings, web storage).
- Allow tight coupling only inside a single micro-frontend.
- Document every place where tight coupling exists.

**Don't:**
- Introduce shared state to "simplify" two MFEs — you have just coupled their
  release cycles.

*Ref: Building Micro-Frontends.md — "Sharing state"*

---

### 63. Choosing the Right Architecture — Decision Tree

**Principle:** Start at the top; each branch eliminates options.

```
Q1. Multiple micro-frontends per view?
    Yes → Horizontal split.  No  → Vertical split.

Q2. SEO required?
    Yes → Server-side or edge-side.  No → Client-side.

Q3. Personalised content per user?
    Yes → Server-side.  No → Edge-side (CDN cache friendly).

Q4. Independent framework choice per team?
    Yes → Web components or iframes.
    No  → Module Federation or single-spa.

Q5. Legacy code to embed?
    Yes → iframe adapter micro-frontend.
    No  → Skip adapter.
```

*Ref: Building Micro-Frontends.md — synthesised from Chapters 3 + 4*

---

### 64. Migration Anti-Patterns

**Principle:** Most migration failures come from skipping steps.

**Anti-patterns:**
- Migrating auth first (highest risk, lowest learning).
- Big-bang rewrite instead of strangler.
- Letting the monolith and micro-frontend share state.
- Skipping the design system — every MFE drifts visually.
- Letting teams pick frameworks independently during migration.

*Ref: Building Micro-Frontends.md — "From Monolith to Micro-Frontends"*

---

### 65. Architecture Scoring (Synthesis)

**Principle:** Use the book's 8-axis scoring to compare options
quantitatively.

| Axis            | Vertical (AppShell) | Horizontal MF | iframes | Web Components | Server-side | Edge-side |
|-----------------|---------------------|---------------|---------|----------------|-------------|-----------|
| Deployability   | 5/5                 | 4/5           | 5/5     | 4/5            | 4/5         | 3/5       |
| Modularity      | 2/5                 | 4/5           | 3/5     | 3/5            | 5/5         | 4/5       |
| Simplicity      | 4/5                 | 5/5           | 3/5     | 4/5            | 3/5         | 2/5       |
| Testability     | 4/5                 | 4/5           | 3/5     | 4/5            | 4/5         | 3/5       |
| Performance     | 4/5                 | 4/5           | 2/5     | 4/5            | 5/5         | 3/5       |
| DX              | 4/5                 | 5/5           | 3/5     | 4/5            | 3/5         | 2/5       |
| Scalability     | 5/5                 | 5/5           | 5/5     | 5/5            | 3/5         | 4/5       |
| Coordination    | 4/5                 | 3/5           | 3/5     | 3/5            | 3/5         | 3/5       |

Use this table to argue for a choice; never to declare a winner.

*Ref: Building Micro-Frontends.md — Tables 4-1 through 4-6*

---

### 66. Automation First, Micro-Frontends Second

**Principle:** Do not adopt micro-frontends without first having a solid
automation culture.

**Do:**
- Invest in CI/CD, observability, and design system before launching MFEs.
- Treat automation as iterative — review pipelines every 1–2 months.

**Don't:**
- Treat micro-frontends as a substitute for automation — they amplify the
  cost of bad automation.

*Ref: Building Micro-Frontends.md — "Automation Principles"*

---

### 67. The "Less Worse" Architecture Mindset

**Principle:** No architecture is universally best. Pick the one whose
trade-offs you can live with.

**Do:**
- Document the trade-offs you accepted.
- Review trade-offs at every ADR.
- Use the 8-axis score as a discussion tool, not a decision tool.

**Don't:**
- Use the score to declare a winner.
- Let a single axis (e.g. performance) drive the decision in isolation.

*Ref: Building Micro-Frontends.md — "Architecture and Trade-offs"*

---

### 68. Conway's Law Applied to APIs

**Principle:** API contracts between MFEs and between MFEs and backends are
the new team boundaries.

**Do:**
- Treat each API contract as a public surface.
- Version APIs explicitly (URL or header).
- Document breaking changes via RFC.

**Don't:**
- Embed API versions in micro-frontend names.
- Couple frontend and backend teams around the same API definition process.

*Ref: Building Micro-Frontends.md — "API Consistency"*

---

### 69. Automation Pipeline Stages (Recap)

**Six stages:**
1. Version control (commit + monorepo/polyrepo rules).
2. Pipeline initialization (clone with `--depth 1`, install).
3. Code-quality review (lint, unit, integration, contract, design-system
   version check).
4. Build (bundle, optimise, chunk per micro-frontend).
5. Post-build review (e2e in on-demand env, Lighthouse, visual regression,
   store artifact).
6. Deployment (CDN push, promotion dashboard, canary or blue-green).

*Ref: Building Micro-Frontends.md — "Automation Pipeline for Micro-Frontends: A Case Study"*

---

### 70. The 25× Defect Cost Rule

**Principle:** NIST estimates fixing a defect in production costs 25× more
than catching it during development.

**Do:**
- Maximise the number of checks before code reaches production.
- Run every check locally before pushing (lint, unit, contract).
- Fail the build loudly on regression.

**Don't:**
- Defer checks to "later sprints" — later is exponentially more expensive.

*Ref: Building Micro-Frontends.md — "Defect Costs Rise over Time"*

---

### 71. Multiframework — Use Sparingly

**Principle:** Multiple UI frameworks in the same view hurt performance and
stability.

**Acceptable scenarios:**
- Migration period (legacy alongside new).
- Hard polyglot requirements (e.g. embedding a third-party widget).

**Do:**
- Document the migration window during which multiframework is tolerated.
- Bundle each framework's chunk separately and lazy-load it.

**Don't:**
- Treat multiframework as a long-term architectural choice.

*Ref: Building Micro-Frontends.md — "Multiframework approach"*

---

### 72. Pricing the Architecture — Total Cost of Ownership

**Principle:** Micro-frontends cost automation, governance, observability,
and communication. Budget for all four.

**Hidden costs:**
- Per-team CI/CD pipelines.
- Per-team observability dashboards.
- Cross-team coordination rituals (CoP, town halls).
- DX tooling (CLI scaffolds, dashboards).

**Do:**
- Estimate TCO before adoption.
- Charge the micro-frontend investment back to product velocity wins.

*Ref: Building Micro-Frontends.md — synthesised from Chapters 6, 7, 10*

---

### 73. The Right Boundary Test

**Principle:** If two micro-frontends share the same API frequently, they
are probably one micro-frontend.

**Do:**
- Review API consumption patterns quarterly.
- Merge micro-frontends when the data shows shared-API smell.

**Don't:**
- Treat the initial decomposition as permanent — boundaries evolve.

*Ref: Building Micro-Frontends.md — "Best Practices" (Chapter 8)*

---

### 74. PR/FAQ for Cross-Team Features

**Principle:** One-page press release + up to 5 pages of FAQs before code.

**Do:**
- Write the press release first — what would customers see in 12 months?
- Use the FAQ to align techies and product people before any code.
- Use it as the seed for the architecture diagram.

**Don't:**
- Skip the customer framing — internal-only PR/FAQs lose half the value.

*Ref: Building Micro-Frontends.md — "Working Backward"*

---

### 75. Tools Mentioned (Quick Reference)

| Tool / Project            | Role                                              |
|---------------------------|---------------------------------------------------|
| webpack 5 + Module Federation | Runtime composition                            |
| single-spa                | Lifecycle orchestration                           |
| qiankun                   | single-spa + HTML entry points                    |
| Piral                     | App shell + plugin model                          |
| OpenComponents            | SSR registry-based composition                    |
| Mosaic / Tailor / Podium  | SSI / ESI / SSR frameworks                        |
| Puzzle.js                 | SSR fragment composition                          |
| Ara Framework             | Server-side + bridge for cross-stack MFEs         |
| Luigi (SAP)               | iframe-based enterprise MFEs                      |
| MobX-State-Tree           | Composable state trees                            |
| Material-UI               | Design system + per-team seed CSS prefixes       |
| Puppeteer / Rendertron    | Dynamic rendering for SEO crawlers                |
| crawler-user-agents       | User-agent detection (npm)                        |
| Lerna / Nx / Turborepo    | Monorepo tooling                                  |
| Lambda@Edge / Cloudflare Workers | Edge compute for canary + routing         |
| Sentry / New Relic Browser / LogRocket | Frontend observability                  |
| Spotify iframe bridge (C++) | Desktop micro-frontend communication             |
| MobX / Redux-observable   | Reactive state primitives                         |

*Ref: Building Micro-Frontends.md — Chapters 4, 5, 8, 9*

---

### 76. The "Three Versions" Strangler Strategy

**Principle:** Keep legacy, hybrid, and micro-frontend versions alive during
migration.

**Why:** Gives you an always-on fallback to the legacy monolith if a
micro-frontend release goes wrong.

**Do:**
- Maintain a small "hybrid" layer that routes between the three.
- Use Lambda@Edge or an API gateway as the router.
- Retire each legacy surface only after the micro-frontend has run in
  production for ≥ 1 sprint with zero rollback.

**Don't:**
- Delete legacy code immediately after the micro-frontend ships.
- Skip the hybrid layer — you lose the safety net.

*Ref: Building Micro-Frontends.md — "Strangler Pattern" (Chapter 6)*

---

### 77. Authorization in Horizontal Split

**Principle:** The container (host) validates auth; the micro-frontends
trust the host.

**Do:**
- Have the host reject unauthorised loads before mounting any MFE.
- Pass a normalised `user` object via the event emitter so MFEs do not
  re-fetch identity.

**Don't:**
- Trust the JWT inside a micro-frontend without re-validating scope.
- Store user roles in localStorage where they can drift from the backend.

*Ref: Building Micro-Frontends.md — "Authentication"*

---

### 78. The Five-Question Migration Sanity Check

Before declaring a micro-frontend migration successful, answer "yes" to:

1. Can each micro-frontend deploy independently? (no shared release train)
2. Does each team own its subdomain end-to-end?
3. Is the design system enforced in CI?
4. Is observability wired into every MFE?
5. Is rollback to the legacy or previous version one click away?

If any answer is "no", the migration is incomplete.

*Ref: Building Micro-Frontends.md — synthesised from Chapters 6, 9, 10*

---

### 79. The Cyclomatic Complexity Ceiling

**Principle:** A function with CYC > 10 is a refactoring candidate; enforce
the ceiling as a CI gate.

**Code:**
```js
const myFunc = (someValue) =>{
  // variable definitions
  if(someValue === "1234-5678"){        // CYC: 1 - first branch
    // do something
  } else if(someValue === "9876-5432"){ // CYC: 2 - second branch
    // do something else
  } else {                              // CYC: 3 - third branch
    // default case
  }
  // return something
}
// CYC = 3 → need ≥ 3 unit tests
```
*Ref: Building Micro-Frontends.md — "Code-Quality Review"*

---

### 80. The "Don'ts" Final List

- Don't put business logic in the application shell.
- Don't share a Redux store across micro-frontends.
- Don't adopt micro-frontends for one-team projects.
- Don't write your own MFE orchestration before evaluating single-spa and
  Module Federation.
- Don't use ESI without an Akamai / Varnish / NGINX test rig.
- Don't forget the `--depth 1` clone in CI.
- Don't blame the architecture for missing automation — the architecture is not
  the cure.
- Don't ship a micro-frontend without observability.
- Don't store long-lived tokens in `localStorage`.
- Don't use iframes for consumer web without measuring performance.
- Don't mix build-time and runtime composition in the same view without a
  clear boundary.

*Ref: Building Micro-Frontends.md — synthesised*

---

## Anti-Patterns & Common Mistakes

- **Distributed frontend monolith:** Global shared state, coordinated releases, frequent cross-team tickets — fix by introducing explicit contracts (events, query strings) and re-splitting. *Ref: Ch.4*
- **Premature decomposition:** Splitting on day 1 with no analytics — fix by waiting for flow data. *Ref: Ch.3*
- **Nano-frontends:** One MFE per component — merge into a subdomain-level MFE. *Ref: Ch.4*
- **Shell-as-monolith:** Shell accumulating business logic — extract to MFE; shell = lifecycle only. *Ref: Ch.4*
- **Coupled CI/CD:** Every MFE rebuilds on every shared-library change — publish libs as versioned artifacts. *Ref: Ch.6*
- **Mega-BFF:** Single BFF for every subdomain and platform — one BFF per subdomain/platform. *Ref: Ch.8*
- **Hidden shared CSS:** Class collisions — per-team BEM prefixes or `seed` (Material-UI). *Ref: Ch.4*
- **Designer-developer split:** Centralised design team bottlenecks — distributed contribution with guardrails. *Ref: Ch.4*
- **Migration big-bang:** SPA rewrite in one go — use strangler pattern with three versions. *Ref: Ch.9*
- **Auth-first migration:** Auth is the riskiest first step — migrate user-facing flows first. *Ref: Ch.9*
- **Single-feature monolith disguised as MFE:** One MFE with every feature — subdomain-decompose. *Ref: Ch.4*
- **Untyped event payloads:** Magic strings across MFE boundaries — freeze `const EventNames = { ... }` and type. *Ref: Ch.5*

---

## Decision Heuristics / Checklists

**Use micro-frontends when:** 3+ teams touch the same frontend; release coordination is the bottleneck; a strangler migration of a legacy SPA is needed; team topology can be reshaped along business subdomains.

**Don't use when:** One team owns the entire frontend; the app is a small marketing site; the team lacks CI/CD + observability investment; MFEs would chat constantly (signals a wrong seam).

**Choose composition by:** SEO critical → server-side or edge-side; highly personalised → server-side; static catalog → edge-side; SPA-like UX → client-side; small latency budget → client-side + CDN.

**Choose routing by:** server-side composition → server-side routing; edge-side → URL-driven edge routing; client-side → client-side routing in the application shell.

**Choose communication by:** same view, multiple MFEs → pub/sub; different views, persistent data → web storage; different views, ephemeral data → query strings; iframe escape → `postMessage` + injected emitter.

**Lock-in / dependency:** single framework → Module Federation; multiple frameworks tolerated → web components or iframes; strict isolation → iframes.

**Repository:** few teams + cross-cutting refactors → monorepo; many independent teams → polyrepo; mixed → polyrepo per bounded context (hybrid).

*Ref: Building Micro-Frontends.md — Chapters 3, 4, 6, 9*

---

## Key Takeaways

1. **Micro-frontends are an organisational decision first.** They exist to scale teams; the technology is secondary. Adopt only when 3+ teams share a frontend.
2. **Apply the four-pillar decisions framework every time.** Define → Compose → Route → Communicate. Skipping one pillar creates the next anti-pattern.
3. **Vertical split is the recommended default.** Application shell + one MFE per subdomain + client-side composition + web-storage auth.
4. **Horizontal split is for true reuse.** When a subdomain appears in many views (payment, video player), horizontal split earns its complexity.
5. **Conway's law is a feature, not a bug.** Design the team topology first; the architecture follows. The inverse Conway maneuver is your friend.
6. **Communicate via events, not state.** Shared state is the #1 path to the distributed frontend monolith.
7. **Module Federation (Webpack 5) is the leading runtime composition.** Use `singleton: true` for shared libraries and `requiredVersion` to pin compatible ranges.
8. **Design system + CI-enforced version check is non-negotiable.** Visual consistency across MFEs comes from automation, not from goodwill.
9. **Strangler pattern + canary = safe migration.** Three versions alive (legacy / hybrid / MFE); Lambda@Edge routes between them.
10. **Performance budgets per MFE.** Bundle size, Lighthouse score, TTI; enforce in CI; review every 1–2 months.
11. **Automation is the prerequisite, not the bonus.** Micro-frontends amplify the cost of bad CI/CD.
12. **Observability is part of "done".** Every MFE ships with Sentry / New Relic Browser / LogRocket wired in.
13. **Edge composition (ESI) is the underdog.** Best for static, cacheable, geographically distributed catalogs (IKEA); requires Akamai/Varnish test rig.
14. **Piral, single-spa, qiankun, OpenComponents, Module Federation each have a niche.** Pick by team skill and target environment, not by hype.
15. **DAZN, Spotify, IKEA, New Relic, edX, SAP, OpenTable, Zalando prove the model.** Each chose differently; all succeeded because the choice fit context.

*Ref: Building Micro-Frontends.md — synthesised*

---

## Cross-References

- Related: `../Building_Microservices.md` (microservices principles that ground
  the micro-frontend principles chapter).
- Related: `../Software_Architecture_Patterns.md` (architectural decision
  heuristics, trade-off frameworks).
- Related: `../Building_Evolutionary_Architectures.md` (fitness functions for
  measuring architectural characteristics).
- Related: `../Team_Topologies.md` (inverse Conway maneuver and stream-aligned
  teams).
- Related: `../Crafting_Engineering_Strategy.md` (when and how to invest in
  DX, automation, governance).
- Related: `../Continuous_Deployment.md` (canary, blue-green, strangler
  pattern details).
- Related: `../Observability_Engineering.md` (frontend observability tooling).
- Topic index: `../INDEX.md`