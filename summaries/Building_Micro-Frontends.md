# Building Micro-Frontends - Luca Mezzalira

## Comprehensive Summary

---

## Chapter 1: The Frontend Landscape

**Types of frontend architectures:**

1. **Micro-Frontend Applications**: Decompose a monolithic frontend into smaller, independently deliverable pieces owned by different teams. Each team can choose its own framework and release on its own schedule.

2. **Single-Page Applications (SPAs)**: One large JavaScript application loaded in the browser. All routing and rendering happens client-side. Simple to start, becomes unwieldy at scale.

3. **Isomorphic Applications**: Code runs on both server and client. Server-side rendering (SSR) for initial load performance, client-side hydration for interactivity. Examples: Next.js, Nuxt.js.

4. **Static-Page Websites**: Pre-built HTML served directly. Fast, simple, but limited interactivity. Good for content sites.

5. **Jamstack**: JavaScript + APIs + Markup. Static frontends that call APIs for dynamic content. Combines static performance with dynamic capability.

**Why micro-frontends emerged:** As frontend applications grew, single teams couldn't manage the entire UI. SPAs became monoliths with the same problems as backend monoliths—slow builds, merge conflicts, release coordination.

---

## Chapter 2: Micro-Frontend Principles

**Applying microservices principles to frontend:**

1. **Modeled Around Business Domains**: Each micro-frontend owns a complete vertical slice of UI functionality (e.g., "product catalog" or "checkout"), not a horizontal layer (e.g., "header" or "footer").

2. **Culture of Automation**: CI/CD for every micro-frontend. Automated testing, building, and deployment. Fast feedback loops.

3. **Hide Implementation Details**: Each micro-frontend is a black box. Other micro-frontends interact through well-defined contracts, not shared internals.

4. **Decentralize Governance**: Teams choose their own tools, frameworks, and libraries within agreed guardrails. No central "frontend standards committee."

5. **Deploy Independently**: Each micro-frontend can be deployed without coordinating with other teams. No "big bang" frontend releases.

6. **Isolate Failure**: If one micro-frontend fails, the rest of the application continues working. Error boundaries prevent cascade.

7. **Highly Observable**: Each micro-frontend exposes its own health metrics, logs, and error reporting.

**Micro-frontends are not a silver bullet:** They add complexity. Don't adopt them for small teams or simple applications. Use when you have multiple teams working on the same frontend product.

---

## Chapter 3: Micro-Frontend Architectures and Challenges

**The Micro-Frontend Decisions Framework:**

1. **Define micro-frontends**: What are the bounded contexts in your UI?
2. **Composition**: How are micro-frontends composed into a single page?
3. **Routing**: Who handles URL routing?
4. **Communication**: How do micro-frontends share data?

**Domain-Driven Design for micro-frontends:**
- Use bounded contexts from backend DDD as a starting point
- A micro-frontend should map to one bounded context
- Shared UI language: design system provides consistent look and feel

**Composition approaches:**
- **Client-side composition**: Micro-frontends loaded in the browser, composed by an application shell
- **Server-side composition**: Server assembles HTML from multiple micro-frontends
- **Edge-side composition**: CDN/edge layer composes fragments (ESI)

**Communication between micro-frontends:**
- **Custom events**: Browser-native, loosely coupled
- **Shared state**: A global store (Redux, custom) — use sparingly, creates coupling
- **URL/parameters**: Route-based communication, most decoupled
- **Pub/sub**: Event bus pattern, custom events are the web standard

**Real-world adopters:** Zalando, HelloFresh, Spotify, SAP, OpenTable, DAZN—each with different architectures tailored to their needs.

---

## Chapter 4: Discovering Micro-Frontend Architectures

**Vertical Split (by business domain):**
- Each micro-frontend is a complete vertical slice: route → UI → data → logic
- Best for independent teams with full-stack ownership
- Examples: /products (catalog team), /checkout (payments team), /account (user team)

**Horizontal Split (by technical layer):**
- Common UI shell + micro-frontends that render individual components
- Easier to implement, but harder to scale teams independently
- Example: Header team, sidebar team, content area team

**Architecture analysis and trade-offs:**

| Characteristic | Vertical Split | Horizontal Split |
|---------------|---------------|-----------------|
| Team autonomy | High | Medium |
| Independent deployment | Easier | Harder |
| Shared UI consistency | Harder (needs design system) | Easier |
| Technical complexity | Higher | Lower |
| Scalability | Better | Limited |

**Vertical-Split Architecture: Application Shell**
- A thin shell that handles routing, authentication, and layout
- Loads micro-frontends dynamically based on the current route
- Shell provides shared services: auth, navigation, event bus
- Each micro-frontend registers itself with the shell

**Challenges and solutions:**
- **Design consistency**: Implement a shared design system (component library) as an npm package
- **Performance**: Lazy loading, code splitting, shared dependencies
- **SEO**: Server-side rendering or prerendering for search engines
- **Developer experience**: Local development should run a single micro-frontend without the entire system

**Horizontal-Split Architecture:**
- **Client-side**: Module Federation (Webpack 5), iframes, Web Components
- **Server-side**: Template composition on the server (fragments assembled into pages)
- **Edge-side**: ESI (Edge Side Includes) processed at CDN layer

**Module Federation (Webpack 5):**
- Load modules from different builds at runtime
- Share dependencies between micro-frontends (React, lodash)
- Most popular approach for horizontal splits
- Enables independent builds with shared runtime

**iframes:**
- Maximum isolation: each micro-frontend in its own iframe
- Complete independence: no shared state, no CSS conflicts
- Drawbacks: performance overhead, accessibility issues, communication complexity
- Use when: complete isolation is required (embedding third-party content)

**Web Components:**
- Browser-native custom elements
- Shadow DOM provides CSS isolation
- Framework-agnostic: works with any library
- Good for component-level micro-frontends

---

## Chapter 5: Technical Implementation

**Building a micro-frontend application with Module Federation:**

1. **Application Shell**: Host application that loads micro-frontends
   - Handles routing and navigation
   - Manages authentication state
   - Provides shared layout

2. **Micro-Frontend modules**: Each deployed as a separate build
   - Exposes specific components via Module Federation
   - Can be developed, tested, and deployed independently
   - Shares common dependencies (React, design system) with the shell

3. **Authentication**: Typically handled by the shell, token passed to micro-frontends

4. **Embedding legacy applications**: Use iframes or Module Federation to gradually wrap existing apps

5. **Dynamic remote containers**: Load micro-frontends from a registry at runtime, enabling zero-downtime updates

---

## Chapter 6: Build and Deploy Micro-Frontends

**Automation principles:**
1. **Keep feedback loops fast**: Developers must see results quickly
2. **Iterate often**: Small, frequent changes
3. **Empower teams**: Self-service CI/CD
4. **Define guardrails**: Shared quality standards (linting, testing, accessibility)
5. **Define test strategy**: Unit, integration, E2E tests per micro-frontend

**Version control strategies:**
- **Monorepo**: All micro-frontends in one repository
  - Pros: Atomic changes, shared tooling, easy refactoring
  - Cons: Build complexity, ownership boundaries blur
  - Tools: Nx, Turborepo, Lerna
- **Polyrepo**: Each micro-frontend in its own repository
  - Pros: Clear ownership, independent CI/CD
  - Cons: Cross-cutting changes require coordination, shared library versioning

**Testing micro-frontends:**
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test micro-frontend with mocked shell
- **Contract tests**: Verify shell ↔ micro-frontend interfaces
- **E2E tests**: Test complete user journeys across micro-frontends
- **Visual regression tests**: Screenshot comparison for UI consistency
- **Fitness functions**: Automated tests for performance budgets, accessibility, bundle size

**Deployment strategies:**
- **Blue-green**: Two versions, instant switch
- **Canary releases**: Gradual traffic shift to new version
- **Strangler pattern**: Incrementally replace monolith frontend with micro-frontends

**Observability:**
- Per micro-frontend error tracking (Sentry, DataDog)
- Performance monitoring (Core Web Vitals per micro-frontend)
- Health check endpoints for each micro-frontend

---

## Chapter 7: Automation Pipeline Case Study

**Complete CI/CD pipeline for micro-frontends:**
1. Code commit → Linting + formatting
2. Unit tests + contract tests
3. Build (per micro-frontend, not entire application)
4. Visual regression tests
5. Integration tests (micro-frontend + shell)
6. Deploy to staging
7. E2E tests against staging
8. Canary deployment to production
9. Monitoring and alerting

**Key insight**: Only build and test the micro-frontend that changed, not the entire application. This is the primary benefit of micro-frontend architecture.

---

## Key Takeaways

1. **Micro-frontends solve organizational scaling, not technical problems**: Adopt when multiple teams need to work on the same frontend independently.

2. **Apply microservices principles**: Domain-driven, independently deployable, hidden implementation details, decentralized governance.

3. **Vertical splits align with business domains**: Each micro-frontend owns a complete feature vertical, not a horizontal UI layer.

4. **The Application Shell is the orchestrator**: It handles routing, auth, and loading micro-frontends, but delegates all business logic.

5. **Module Federation is the leading technology**: Webpack 5's Module Federation enables runtime module sharing with independent builds.

6. **Design systems ensure visual consistency**: Shared component libraries prevent the "Frankenstein UI" problem.

7. **Monorepo vs polyrepo is a team decision**: Monorepo for simplicity, polyrepo for team independence. Tools like Nx bridge the gap.

8. **Fitness functions protect quality**: Automated tests for bundle size, performance, accessibility, and visual regression.

9. **Only build what changed**: The primary CI/CD benefit—independent builds mean faster pipelines.

10. **Start with a monolith frontend**: Don't prematurely decompose. Split when team coordination pain exceeds micro-frontend complexity.
