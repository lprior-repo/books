# Building Micro-Frontends

**Author:** Luca Mezzalira
**Topic tags:** `#architecture` `#frontend` `#platform`
**Language focus:** language-agnostic (JavaScript / TypeScript)
**Sources:** `markdown_output/Building Micro-Frontends/Building Micro-Frontends.md` · `summaries/Building_Micro-Frontends.md`

## TL;DR
Apply microservices principles to the frontend: decompose a monolithic UI into independently deliverable vertical slices (micro-frontends) owned by different teams, with shared design system, application shell, and clear communication contract. Choose between vertical split (one team owns a full route/feature) and horizontal split (multiple teams compose a single page); choose between client-side, server-side, and edge-side composition; choose between Module Federation, iframes, and Web Components as the integration technology. Adopt when team coordination cost exceeds micro-frontend complexity — never before.

---

## Best Practices by Topic

### The Micro-Frontend Principles — Microservices for the Frontend

**Principle:** Micro-frontends are the application of microservices principles to the UI. Seven principles:

1. **Modeled Around Business Domains** — each micro-frontend owns a complete vertical slice of UI functionality (e.g., "product catalog," "checkout"), not a horizontal layer (e.g., "header," "footer").
2. **Culture of Automation** — CI/CD for every micro-frontend. Fast feedback loops.
3. **Hide Implementation Details** — each micro-frontend is a black box. Others interact through well-defined contracts.
4. **Decentralize Governance** — teams choose their own tools, frameworks, libraries within agreed guardrails.
5. **Deploy Independently** — no big-bang frontend releases.
6. **Isolate Failure** — error boundaries prevent cascade; one failing micro-frontend doesn't break the app.
7. **Highly Observable** — per-micro-frontend health metrics, logs, error reporting.

**Do:**
- Apply each principle deliberately; they're a system, not a checklist.
- Map micro-frontends to bounded contexts from backend DDD.
- Use a shared design system for visual consistency without coupling code.

**Don't:**
- Don't adopt micro-frontends for small teams or simple applications. They're a tool for organizational scaling, not technical problems.
- Don't confuse "components" with "micro-frontends" — components are open to extension; micro-frontends should be closed to extension but open to communication.

*Ref: Building Micro-Frontends.md — "Chapter 2. Micro-Frontend Principles"*

---

### The Micro-Frontend Decisions Framework

**Principle:** Four decisions must be made before any implementation:

1. **Define micro-frontends** — what are the bounded contexts in your UI?
2. **Composition** — how are micro-frontends composed into a single page? (Client-side, server-side, edge-side)
3. **Routing** — who handles URL routing? (Application shell, server, CDN edge)
4. **Communication** — how do micro-frontends share data? (Custom events, URL params, shared state, pub/sub)

**Do:**
- Resolve each decision explicitly. They cascade: composition choice narrows the implementation technology; routing follows composition; communication depends on composition.

**Don't:**
- Don't start with the technology. "Some implementations are done with iframes, while others are done with components library or web components. Too often we spend our time identifying a technical solution without taking the business side into consideration."

*Ref: Building Micro-Frontends.md — "Chapter 3" / "The Micro-Frontend Decisions Framework"*

---

### Vertical Split vs. Horizontal Split — Domain vs. Composition

**Principle:** Two ways to slice a frontend:

- **Vertical Split (by business domain):** each micro-frontend is a complete vertical slice — route → UI → data → logic. Best for independent teams with full-stack ownership. Examples: `/products` (catalog team), `/checkout` (payments team), `/account` (user team). The shell loads one micro-frontend at a time.
- **Horizontal Split (by technical layer):** multiple micro-frontends compose a single page. Common UI shell + micro-frontends that render individual regions. Easier to implement, harder to scale teams independently.

**Vertical Split trade-offs:**

| Characteristic | Vertical Split | Horizontal Split |
|---|---|---|
| Team autonomy | High | Medium |
| Independent deployment | Easier | Harder |
| Shared UI consistency | Harder (needs design system) | Easier |
| Technical complexity | Higher | Lower |
| Scalability | Better | Limited |

**Do:**
- Default to **vertical split** for new projects and for multi-team ownership of distinct features.
- Default to **horizontal split** only when reusability across views is the primary driver.
- Let business context drive the decision.

**Don't:**
- Don't adopt horizontal split just because a vertical split feels hard.
- Don't adopt micro-frontends at all if you don't have multiple teams. The team-coordination pain must exceed the micro-frontend complexity.

*Ref: Building Micro-Frontends.md — "Chapter 4. Discovering Micro-Frontend Architectures"*

---

### The Application Shell — Orchestrator and Authenticator

**Principle:** The application shell is a thin, persistent host that:
- Loads first; shepherds the user session from start to finish.
- Handles global routing (which micro-frontend loads for which URL).
- Manages authentication state and unauthenticated redirects.
- Provides shared layout, navigation, event bus.
- Loads/unloads micro-frontends dynamically.
- Exposes lifecycle APIs (mounted, unmounted) for micro-frontends to react to.

**Implementation guidance:**
- The shell is a simple HTML page + JavaScript wrapper. Use vanilla JS — keep it technology-agnostic and domain-unaware.
- Don't share any business domain logic with micro-frontends.
- Load route configurations at runtime (not at build time) to avoid redeploying the shell for routing changes.
- Initialize shared libraries (logging, telemetry) once at the shell level.

**Do:**
- Use the shell only for edge cases or initialization. "Never use the application shell as a layer to interact constantly with micro-frontends during a user session."
- Make the shell technology-agnostic so future framework changes don't break it.
- Use the shell for global authentication, layout, navigation, event bus.

**Don't:**
- Don't put domain logic in the shell. Doing so creates a logical coupling between the shell and every micro-frontend, forcing testing/redeployment of all of them. This is a "distributed monolith" — the worst-case micro-frontend failure mode.
- Don't bundle the shell with a specific UI framework.

*Ref: Building Micro-Frontends.md — "Chapter 4" / "Vertical-Split Architecture: Application Shell"*

---

### Composition — Client, Server, Edge

**Principle:** Three composition points:

| Layer | Where | Pros | Cons |
|---|---|---|---|
| **Client-side** | Application shell loads micro-frontends via JS in the browser | Easy to start, fully dynamic | SEO needs work, hydration complexity |
| **Server-side** | Server assembles HTML from multiple micro-frontends | Better SEO, faster initial paint | More infrastructure |
| **Edge-side** | CDN/edge composes fragments (ESI) | Fast, cacheable | Limited technology (ESI today) |

**Do:**
- Choose composition before choosing integration technology. "When you use client-side composition and routing, your best implementation choice is an application shell loading multiple micro-frontends in the same view with the webpack plug-in called Module Federation, with iframes, or with web components."
- Use edge-side composition (ESI) only for content where SEO and TTFB are critical.
- Use server-side composition when you need SSR for SEO and faster initial paint.

**Don't:**
- Don't reach for ESI as a default; it's the least flexible option.
- Don't mix composition strategies without a deliberate reason.

*Ref: Building Micro-Frontends.md — "Chapter 3" / "Composition"; "Chapter 4" / "Composition Choice"*

---

### Module Federation — The Leading Integration Technology

**Principle:** Module Federation (Webpack 5) is a plug-in that lets you load external modules, libraries, or entire applications inside another at runtime. It handles the undifferentiated heavy lifting: scope wrapping, dependency sharing, version conflict resolution.

**Two parts:**
- **Host (the application shell):** declares remotes it can load.
- **Remote (a micro-frontend or design system):** exposes modules for hosts to import.

**Capabilities:**
- Async and sync module loading.
- Dependency sharing: e.g., share Vue 3.0.0 across all micro-frontends; Module Federation loads it once.
- Different versions: Module Federation can wrap conflicting versions in different scopes.
- Works with server-side rendering too.
- Static and dynamic remote containers (load from a registry at runtime → zero-downtime updates).

**Trade-off:** "The great simplicity of code sharing across projects is also the weakest point of this plug-in. When you work in a team that's not disciplined enough, sharing libraries, code snippets, and micro-frontends across multiple views can result in a very complicated architecture to maintain."

**Do:**
- Use Module Federation for webpack-based projects to minimize learning curve.
- Specify shared libraries in the configuration; let Module Federation load them once.
- Use unidirectional sharing (host → remote). Discourage bidirectional (host ↔ remote) sharing to maintain hierarchical clarity.
- Use dynamic remote containers for zero-downtime updates.

**Don't:**
- Don't allow unidirectional discipline to erode into bidirectional sharing. "A unidirectional implementation brings several advantages."
- Don't enable frictionless sharing without architectural guardrails. This is a recipe for organizational friction.

**Code (conceptual webpack configuration — Host):**
```js
// webpack.config.js (host / application shell)
new ModuleFederationPlugin({
  name: 'shell',
  remotes: {
    catalog: 'catalog@https://mfe.example.com/catalog/remoteEntry.js',
    checkout: 'checkout@https://mfe.example.com/checkout/remoteEntry.js',
  },
  shared: {
    react: { singleton: true, requiredVersion: '^18.0.0' },
    'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
    '@acme/design-system': { singleton: true },
  },
})
```
**Code (conceptual webpack configuration — Remote):**
```js
// webpack.config.js (remote micro-frontend)
new ModuleFederationPlugin({
  name: 'catalog',
  filename: 'remoteEntry.js',
  exposes: {
    './CatalogApp': './src/CatalogApp',
  },
  shared: {
    react: { singleton: true, requiredVersion: '^18.0.0' },
    'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
    '@acme/design-system': { singleton: true },
  },
})
```
*Ref: Building Micro-Frontends.md — "Chapter 4" / "Module Federation"*

---

### iframes — Maximum Isolation, Maximum Trade-off

**Principle:** An iframe loads another HTML document inside the host page. Provides granular control over what runs inside via the `sandbox` attribute. Complete isolation between micro-frontends.

**Sandbox attributes:**
- Default: prevents JavaScript execution and form submission.
- `allow-scripts`: enable JS.
- `allow-forms`: enable form submission.
- `allow-same-origin`: treat as same-origin.

**Communication:** `postMessage` API between iframe and host.

**Trade-offs:**
- Maximum isolation, no CSS conflicts, no JS clashes.
- Drawbacks: performance overhead, accessibility issues, communication complexity.

**When to use:**
- Embedding third-party content.
- Legacy migration (when complete isolation is required).
- B2B enterprise apps where SEO and bandwidth aren't problems (SAP Luigi).

**Do:**
- Use iframes when complete isolation is a hard requirement.
- Use `postMessage` for iframe ↔ host communication.
- Combine with the `sandbox` attribute to restrict capabilities.

**Don't:**
- Don't use iframes when micro-frontends need frequent, complex communication. The cost is too high.
- Don't use iframes for high-performance user-facing apps. Spotify abandoned iframes on web for performance reasons.

**Code (iframe sandbox example):**
```html
<!-- Maximum restriction: no JS, no forms -->
<iframe sandbox src="https://mfe.mywebsite.com/catalog/"></iframe>

<!-- Loosened: allow JS and form submission -->
<iframe sandbox="allow-scripts allow-forms" 
        src="https://mfe.mywebsite.com/catalog/"></iframe>
```
*Ref: Building Micro-Frontends.md — "Chapter 4" / "iframes"*

---

### Web Components — Framework-Agnostic Encapsulation

**Principle:** Web Components are a set of web platform APIs for creating reusable, encapsulated HTML tags. Two key pieces:
- **Custom elements:** wrappers for micro-frontends.
- **Shadow DOM:** encapsulates styles so they don't leak into the application shell.

**Web Components + micro-frontends:**
- Framework-agnostic: works with React, Angular, Vue, Svelte.
- Encapsulation without iframe overhead.
- Great for multi-tenant environments (micro-frontends used in multiple apps).
- Great for shared design system components (so they outlive framework changes).

**Trade-offs:**
- Customized built-in elements have bugs in WebKit (older Safari).
- Older browsers need polyfills (large package size).
- SEO with shadow DOM is harder — expose content in light DOM for crawlers.

**Do:**
- Use Web Components for the design system. "The best investment you can make for creating a design system is in web components. Since you can use web components with any UI framework, should you decide to change the UI framework later, the design system will remain the same."
- Use Web Components for multi-tenant or cross-app reuse.
- Expose content in light DOM when SEO matters.

**Don't:**
- Don't target old browsers without a polyfill strategy.
- Don't blur components and micro-frontends. Components are open to extension; micro-frontends should be closed to extension.
- Don't use Web Components when an iframe is simpler and isolation is sufficient.

**Code (light DOM for SEO with Web Components):**
```js
// Avoid: content in shadow DOM is invisible to most crawlers
this.attachShadow({ mode: 'open' }).innerHTML = `<h1>Product ${this.productId}</h1>`;

// Prefer: light DOM for SEO-critical content
this.innerHTML = `<h1>Product ${this.productId}</h1>`;
```
*Ref: Building Micro-Frontends.md — "Chapter 4" / "Web Components"; "Chapter 4" / "SEO and web components"*

---

### Communication Between Micro-Frontends

**Principle:** Communication patterns, in order of preference:

- **URL/parameters:** route-based, most decoupled. The default.
- **Custom events on `window`:** browser-native, loosely coupled. Standard pub/sub.
- **Pub/sub event bus:** event emitter pattern, especially useful for iframes (each iframe has its own window).
- **Web storage (localStorage / sessionStorage):** for sensitive data like authentication tokens; cache with TTL stamp.
- **Shared state (Redux, etc.):** use sparingly — creates coupling. "An anti-corruption layer should exist between the inner and the outer systems."

**Do:**
- Default to URL/parameters for navigation state.
- Use custom events for cross-micro-frontend messaging.
- Cache sensitive shared data in web storage with a timestamp.
- Treat the shell as the only event-bus owner when possible; let micro-frontends talk to the shell, not to each other.

**Don't:**
- Don't put business logic in the event bus. The bus should carry notifications, not data.
- Don't share state across micro-frontends unless absolutely necessary. Shared state is shared coupling.

*Ref: Building Micro-Frontends.md — "Chapter 3" / "Communication"; "Chapter 5" / "Application Shell"*

---

### State Sharing Across Micro-Frontends

**Principle:** Two patterns for shared state:

- **In-memory via the shell:** the shell owns a state object; micro-frontends register/unregister with the shell's lifecycle. Use for ephemeral session data.
- **Web storage with TTL:** the first micro-frontend loads sensitive data from a public API and writes it to web storage with a retrieval timestamp; subsequent micro-frontends read from web storage and refresh if the timestamp is too old.

**Do:**
- Choose state sharing strategy per data type, not globally.
- Cache with timestamps; refresh when stale.
- Decouple micro-frontends by routing shared state through the shell or a well-known contract.

**Don't:**
- Don't make every micro-frontend call the same API to retrieve the same shared data.
- Don't use shared in-memory state without a clear ownership model.

*Ref: Building Micro-Frontends.md — "Chapter 4" / "Sharing State"*

---

### Design System — The Visual Backbone

**Principle:** A design system in a micro-frontend architecture has four layers:

1. **Design tokens** (JSON/YAML) — low-level values: fonts, colors, sizes. Generally not distributed per micro-frontend.
2. **Basic components** — buttons, inputs, primitives.
3. **UI library** — composed components.
4. **Micro-frontends** — host the design system pieces together.

**Implementation guidance:**
- Build the design system in **web components** so it survives framework changes.
- Automate design-system version validation in CI: check `package.json` of every micro-frontend; fail the build if the design system is outdated.
- Distribute design-system ownership thoughtfully: a core team provides core components and direction; other teams contribute components under guardrails.

**Do:**
- Use atomic design methodology (atoms → molecules → organisms → templates → pages).
- Use CSS prefixes per micro-frontend to avoid style clashes (e.g., Material-UI's `seed` property).
- Centralize the design system but allow contribution under governance.
- Validate the design system version in CI as a fitness function.

**Don't:**
- Don't distribute design tokens to each micro-frontend. That invites bugs.
- Don't let the design system become a bottleneck by being 100% central without contribution paths.

*Ref: Building Micro-Frontends.md — "Chapter 4" / "Design System"; "Chapter 7" / "Pipeline"; ACME case study*

---

### Monorepo vs. Polyrepo

**Principle:** Two repository strategies:

**Monorepo** — all micro-frontends in one repository.
- Pros: atomic changes, shared tooling, easy refactoring, encourage continuous refactoring.
- Cons: build complexity, ownership boundaries blur, requires constant tooling investment (Nx, Turborepo, Lerna).
- Use trunk-based development.

**Polyrepo** — each micro-frontend in its own repository.
- Pros: clear ownership, independent CI/CD, flexible branching strategies, smaller build artifacts.
- Cons: cross-cutting changes require coordination, shared library versioning is harder, code duplication risk, naming conventions critical, harder discovery.
- Use the right branching strategy per project.

**Do:**
- Default to **monorepo** for vertical-split architectures; default to **polyrepo** when teams are highly independent.
- Invest in monorepo tooling (Nx, Turborepo) when the repo grows.
- Establish naming conventions for polyrepo to enable discoverability.
- Use polyrepo's flexibility to support legacy projects on different branching/release cadences alongside modern projects.

**Don't:**
- Don't distribute repositories without naming conventions.
- Don't let polyrepo lead to silent code duplication (logging, observability, etc.) — coordinate shared libraries explicitly.

*Ref: Building Micro-Frontends.md — "Chapter 6. Build and Deploy" / "Version control strategies"*

---

### Automation Pipelines — Only Build What Changed

**Principle:** The primary benefit of micro-frontends is **independent builds**. The CI/CD pipeline must reflect this. Build and test only the micro-frontend that changed, not the entire application.

**Pipeline stages:**
1. Code commit → linting + formatting.
2. Unit tests + contract tests.
3. Build (per micro-frontend).
4. Visual regression tests.
5. Integration tests (micro-frontend + shell).
6. Deploy to staging.
7. E2E tests against staging.
8. Canary deployment to production.
9. Monitoring and alerting.

**Do:**
- Keep feedback loops fast — developers must see results quickly.
- Empower teams with self-service CI/CD.
- Define guardrails (linting, testing, accessibility, bundle size, design system version).
- Use fitness functions to enforce architecture characteristics automatically.

**Don't:**
- Don't build the entire application on every micro-frontend commit. That defeats the purpose.
- Don't skip integration or contract tests even when build is fast.

*Ref: Building Micro-Frontends.md — "Chapter 6" / "Automation principles"; "Chapter 7" / "Automation Pipeline Case Study"*

---

### Testing Micro-Frontends

**Principle:** Multi-layered test strategy:

- **Unit tests** — individual components in isolation.
- **Integration tests** — micro-frontend with mocked shell.
- **Contract tests** — verify shell ↔ micro-frontend interfaces.
- **End-to-end tests** — complete user journeys across micro-frontends.
- **Visual regression tests** — screenshot comparison for UI consistency.
- **Fitness functions** — automated checks for performance budgets, accessibility, bundle size, design-system version.

**Do:**
- Test contracts explicitly between shell and micro-frontends.
- Use visual regression for UI consistency.
- Include design-system version checks as fitness functions.

**Don't:**
- Don't rely on code coverage alone as a quality measure. "This metric doesn't provide us with the quality of the test, just a snapshot of tests written for public functions."

*Ref: Building Micro-Frontends.md — "Chapter 6" / "Testing micro-frontends"*

---

### Deployment Strategies

**Principle:** Three primary deployment strategies:

- **Blue-green deployment:** two versions, instant switch.
- **Canary releases:** gradual traffic shift to a new version.
- **Strangler pattern:** incrementally replace the legacy application with micro-frontends — release parts of the application instead of waiting for the entire rewrite.

**Edge logic for advanced routing:** Use Lambda@Edge (AWS) or Cloudflare Workers to handle canary routing or dynamic rendering for SEO at the CDN edge.

**Strangler pattern mechanics:**
- Build a micro-frontend for one area of the legacy application.
- Deploy it in production alongside the legacy app.
- The legacy application redirects that area to the new micro-frontend URL.
- Repeat until the legacy app is fully replaced.

**Do:**
- Use canary releases for high-risk changes.
- Use the strangler pattern when migrating from a legacy frontend — it provides immediate business value while reducing risk.
- Use edge compute (Lambda@Edge, Workers) for canary routing and dynamic rendering for SEO.

**Don't:**
- Don't wait until the entire micro-frontend architecture is complete before deploying anything.
- Don't rewrite the entire app at once. Use the strangler pattern incrementally.

*Ref: Building Micro-Frontends.md — "Chapter 6" / "Deployment strategies"; "Chapter 6" / "Strangler Pattern"*

---

### Fitness Functions for Architecture Characteristics

**Principle:** Fitness functions provide "an objective integrity assessment of some architectural characteristic(s)" (Neal Ford et al., *Building Evolutionary Architecture*). Apply them to micro-frontends:

- Bundle size budget.
- Cyclomatic complexity.
- Design-system version.
- Required libraries present in `package.json`.
- Test coverage.
- Performance metrics (Core Web Vitals per micro-frontend).

**Do:**
- Make fitness functions a CI gate, not an advisory check. Block the build on failure.
- Customize fitness functions to your architecture's specific characteristics.

**Don't:**
- Don't rely on code coverage as a quality signal.

*Ref: Building Micro-Frontends.md — "Chapter 7" / "Fitness Functions"*

---

### Observability

**Principle:** Each micro-frontend must expose its own:
- Error tracking (Sentry, DataDog).
- Performance monitoring (Core Web Vitals per micro-frontend).
- Health check endpoints.
- Logging tied to a shared observability service.

**Do:**
- Implement per-micro-frontend error tracking.
- Track Core Web Vitals per micro-frontend.
- Expose health check endpoints.

**Don't:**
- Don't rely on global frontend monitoring only. Each micro-frontend must be observable in isolation.

*Ref: Building Micro-Frontends.md — "Chapter 6" / "Observability"*

---

### Migration from Monolith — Strangler Pattern

**Principle:** Migrate incrementally using the strangler pattern:
1. Pick a low-risk area of the legacy application.
2. Build a micro-frontend for it.
3. Deploy alongside the legacy app; legacy redirects that area to the new URL.
4. Repeat until the legacy app is fully replaced.

**Pitfall observed in practice:** "The high cost of replatforming eight-year-old features that didn't have defined APIs in place (since the UI was server-rendered) and our goal to achieve feature parity. We chose to retain parity with the old implementation in order to avoid making multiple changes at once (technology plus features) that could result in inadvertent business performance issues."

**Do:**
- Set realistic scope — don't require feature parity with every legacy page at once.
- Allow feature teams to rewrite pages in stride with UX work, not all upfront.
- Use the strangler pattern to deliver value continuously.

**Don't:**
- Don't couple technology changes (micro-frontend rewrite) with feature changes. Do them separately to isolate risk.

*Ref: Building Micro-Frontends.md — "Chapter 9" / "ACME case study"*

---

### Multiframework Approach — Avoid by Default

**Principle:** "Using a multiframework implementation for this architecture style isn't recommended." Each additional framework = more kilobytes to download and slower customer experience.

**When multiframework is acceptable:** migrating a legacy application to a new one, where micro-frontends are iteratively released.

**Do:**
- Stick to one framework when at all possible.
- Accept multiframework only during a documented migration window.

**Don't:**
- Don't ship multiframework because each team likes a different framework. The performance cost is real.

*Ref: Building Micro-Frontends.md — "Chapter 4" / "Multiframework approach"; OpenTable case study*

---

### Conway's Law Applied to Frontend Architecture

**Principle:** "I've often seen companies design systems in accordance with Conway's law… Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." Apply the **inverse Conway maneuver** for micro-frontends: design the team structure first, then let the micro-frontend topology follow.

**Do:**
- Map team boundaries to micro-frontend boundaries.
- Use Conway's law to justify the architecture to leadership: the structure will mirror the org chart anyway.

**Don't:**
- Don't try to fight Conway's law by imposing micro-frontend boundaries that don't match team structure.

*Ref: Building Micro-Frontends.md — "Chapter 3" / "Real-world adopters"*

---

## Anti-Patterns & Common Mistakes

- **Distributed monolith:** application shell holds domain logic; every micro-frontend depends on shell changes; testing and redeployment become coupled. *Fix:* Keep the shell business-unaware.
- **Premature decomposition:** adopting micro-frontends for a small team. *Fix:* Wait for the team-coordination pain to exceed micro-frontend complexity.
- **Horizontal split when vertical would do:** forcing a team to aggregate multiple micro-frontends in the same view, leading to "spending more time aggregating different micro-frontends in the same view and debugging to make sure everything works properly." *Fix:* Use vertical split unless business demands horizontal reuse.
- **Multiframework by default:** every team picks its own framework. *Fix:* Standardize on one framework; allow multiframework only during legacy migration.
- **Micro-frontend = component confusion:** blurring the line between micro-frontends (closed to extension, open to communication) and components (open to extension). *Fix:* Stick to the business-domain definition.
- **No design system:** "without it, you will definitely be in a world of trouble." *Fix:* Invest in a design system early; ideally in web components.
- **Full-app build on every commit:** rebuilding the entire application defeats the purpose. *Fix:* Build only the changed micro-frontend.
- **State leakage:** using in-memory state across micro-frontends without a clear ownership model. *Fix:* Use URL params, custom events, or web storage with TTL.
- **Mega-iframe:** using iframes for high-performance user-facing apps. Spotify abandoned iframes on web for performance. *Fix:* Use Module Federation or Web Components for performance-critical surfaces.
- **Bidirectional Module Federation sharing:** host ↔ remote sharing. *Fix:* Unidirectional sharing only.
- **No fitness functions:** advisory checks instead of build gates. *Fix:* Block the build on fitness function failure.
- **Strangler without scoping:** trying to rewrite the entire app at once. *Fix:* Pick low-risk areas first; allow feature teams to rewrite in stride with UX work.
- **Silent code duplication in polyrepo:** every team reinvents logging/observability. *Fix:* Coordinate shared libraries; enforce presence in CI.

---

## Decision Heuristics / Checklists

- **Should we adopt micro-frontends?** Checklist:
  - Multiple teams working on the same frontend product? → Yes, adopt.
  - Team coordination pain exceeding micro-frontend complexity? → Yes, adopt.
  - Single team or simple application? → No, stay monolithic.
- **Vertical or horizontal split?**
  - Independent teams owning distinct features? → Vertical.
  - Multiple teams composing a single page (high reusability)? → Horizontal.
  - Default new projects? → Vertical.
- **Composition layer?**
  - SEO critical + fast initial paint? → Server-side or edge-side.
  - Internal app, SEO not critical? → Client-side.
  - Content site, cacheable? → Edge-side (ESI).
- **Integration technology?**
  - Default for webpack projects? → Module Federation.
  - Maximum isolation needed (third-party embed, legacy migration)? → iframes.
  - Framework-agnostic shared design system or multi-tenant? → Web Components.
- **Routing?**
  - Client-side composition → client-side routing in the application shell.
  - Server-side composition → server-side routing.
  - Edge-side → ESI-based routing.
- **Communication?**
  - Default → URL parameters.
  - Cross-micro-frontend event → custom events on window.
  - iframe → postMessage.
  - Sensitive shared data → web storage with TTL.
- **Repository?**
  - Vertical split, single org → monorepo.
  - Highly independent teams, varied release cadences → polyrepo.
- **Deployment?**
  - High-risk change → canary.
  - Migrating from legacy → strangler pattern.
  - Default → blue-green.
- **Fitness functions to enforce:**
  - Bundle size budget.
  - Design-system version.
  - Required libraries present.
  - Test coverage (with quality caveat).
  - Cyclomatic complexity.

---

## Key Takeaways

1. **Micro-frontends solve organizational scaling, not technical problems.** Adopt when multiple teams need to work on the same frontend independently.
2. **Apply microservices principles:** domain-driven, independently deployable, hidden implementation details, decentralized governance.
3. **Default to vertical splits** unless business demands horizontal reuse.
4. **The application shell is the orchestrator:** handles routing, auth, layout, lifecycle — but stays business-unaware.
5. **Module Federation is the leading technology** for webpack projects; iframes for maximum isolation; Web Components for design system and multi-tenant reuse.
6. **A shared design system is non-negotiable** for visual consistency across distributed teams.
7. **Independent builds are the primary CI/CD benefit.** Build only what changed.
8. **Fitness functions protect architecture characteristics** in CI: bundle size, design-system version, required libraries.
9. **Start with a monolith frontend.** Split when team coordination pain exceeds micro-frontend complexity.
10. **Use the strangler pattern** for migration: incremental, value-delivering, low-risk.
11. **Conway's law applies:** team boundaries drive micro-frontend boundaries.
12. **Communication is via URL params and custom events** by default; shared state sparingly; web storage for sensitive shared data.

---

## Cross-References
- Related: [[../Building_Microservices.md]] (microservices principles applied here)
- Related: [[../Team_Topologies.md]] (stream-aligned teams map to micro-frontends; Conway's law)
- Related: [[../Cloud_Application_Architecture_Patterns.md]] (client/server boundaries, replicable applications)
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] (design system as a platform capability)
- Related: [[../Observability_Engineering.md]] (per-micro-frontend observability)
- Topic index: [[../INDEX.md]]