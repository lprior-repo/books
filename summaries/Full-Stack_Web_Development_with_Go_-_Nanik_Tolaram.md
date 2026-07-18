# Full-Stack Web Development with Go - Comprehensive Summary

**Authors:** Nanik Tolaram, Nick Glynn
**Published:** February 2023, Packt Publishing
**ISBN:** 978-1-80323-419-9

## Overview

This book guides developers through building a complete modern web application using Go for the backend and Vue.js for the frontend. The project built throughout the book is a fitness tracking application with features for creating exercises, building workout plans, and user authentication. The book progresses from foundational backend infrastructure (database, logging, observability) through web content serving, API design, frontend frameworks, session management, and finally into CI/CD and cloud deployment.

---

## Part 1: Building a Golang Backend

### Chapter 1: Building the Database and Model

This chapter establishes the database foundation for the fitness tracking application using PostgreSQL, Docker, and the sqlc code generation tool.

**Docker for Local Development:** The authors introduce Docker as the preferred method for running PostgreSQL locally, avoiding the complexity of bare-metal installations. The key command to spin up Postgres is:

```
docker run --name test-postgres \
  -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

**Database Design:** The application uses five tables organized under a `gowebapp` schema: `users` (login credentials with hashed passwords), `images` (exercise images stored as binary data), `exercises` (exercise definitions), `sets` (weight and rep configurations), and `workouts` (combinations of exercises). The entity relationship diagram ties these together through foreign key relationships, with the `users` table as the central entity linking to workouts, and exercises connected through sets.

**sqlc for Code Generation:** A major design decision in this book is the complete separation of SQL from Go code using sqlc (github.com/kyleconroy/sqlc). Rather than writing Go database code by hand, developers write pure SQL in `.sql` files and sqlc generates type-safe Go code. The workflow is:

1. Write a `sqlc.yaml` configuration file specifying paths for schemas, queries, and output
2. Create schema files (e.g., `schema.sql`) defining table structures
3. Write query files (e.g., `query.sql`) with annotated SQL statements using the `-- name: FunctionName :returnType` convention
4. Run `sqlc generate` to produce three Go files: `db.go` (database interface), `models.go` (struct definitions with JSON and db tags), and `query.sql_gen.go` (CRUD functions)

The generated code includes proper context support, transaction wrapping via `WithTx()`, and clean struct representations. Configuration options like `emit_json_tags`, `emit_db_tags`, and `json_tags_case_style` control the output format.

**Makefile Automation:** The chapter concludes by creating a makefile to automate repetitive tasks like bringing Postgres up/down, creating the database, and regenerating sqlc code. This becomes a recurring pattern throughout the book.

### Chapter 2: Application Logging

This chapter covers logging as a critical operational concern, progressing from Go's standard library to a custom logging server architecture.

**Go Standard Library Logging:** The built-in `log` package provides basic functionality (`Print`, `Fatal`, `Panic`, `Printf`) with configurable flags for date/time formats (`Ldate`, `Ltime`, `Lmicroseconds`, `Llongfile`, `Lshortfile`). While functional, it lacks leveled logging, file output features, and JSON formatting.

**golog Library:** The book introduces the golog library (github.com/kataras/golog) which adds severity levels (INFO, WARN, ERROR, DEBUG, FATAL) with color-coded output. Level-based filtering allows configuring different verbosity for development versus production. The `SetLevelOutput()` function enables routing different log levels to different destinations (e.g., errors to a file, info to stdout).

**Centralized Logging Server:** For distributed cloud environments, the authors build a custom REST-based logging server using Gorilla Mux that listens on port 8010 and accepts POST requests at the `/log` endpoint. Applications send JSON-formatted log messages containing timestamp, level, and message fields. The logging server serves as a single point of log collection across multiple application instances.

**Multi-Output Configuration:** A wrapper layer around golog provides configurable output via a `SetLoggingOutput()` function. When the `-local=true` flag is passed, logs go to stdout and local files; otherwise they are sent as HTTP POST requests to the remote logging server. This pattern allows the same binary to operate in both development and production environments without code changes.

### Chapter 3: Application Metrics and Tracing

This chapter introduces observability through the OpenTelemetry specification, covering both distributed tracing and metrics collection.

**OpenTelemetry Fundamentals:** OpenTelemetry (a merger of OpenTracing and OpenCensus) provides vendor-agnostic APIs and SDKs for instrumenting applications. The specification defines two main components: Tracing (tracking service requests across systems) and Metrics (collecting performance measurements). The architecture consists of a TracerProvider (entry point), Tracer (creates Spans), and Span (represents an individual operation). Spans are composed into Directed Acyclic Graphs (DAGs) to form complete traces.

**Jaeger for Distributed Tracing:** Jaeger runs as a Docker container exposing a web UI at port 16686. Integration with OpenTelemetry involves initializing a Jaeger exporter, creating a TracerProvider with the exporter and service name, and registering it globally. Applications then create Spans using `otel.Tracer(serviceName).Start(ctx, "operation-name")`, set attributes on them, and end them when the operation completes. The book demonstrates creating nested spans in goroutines to simulate concurrent operations.

**Prometheus for Metrics:** Prometheus operates on a pull model, scraping metrics from application endpoints at configured intervals. The integration creates an HTTP server on port 2112 that exposes metrics, which Prometheus discovers via its configuration file. The book demonstrates two metrics: `metric.totalrequest` (counting HTTP requests) and `metric.random` (reporting random values). The OpenTelemetry MeterProvider, Meter, and Instrument APIs handle metric recording.

**docker-compose:** Both Jaeger and Prometheus are orchestrated together using docker-compose, which allows configuring multiple containers as a single unit with shared networking. The `docker-compose.yml` file defines services, ports, volumes, and network modes for all observability infrastructure.

---

## Part 2: Serving Web Content

### Chapter 4: Serving and Embedding HTML Content

This chapter covers HTTP routing, serving static and dynamic content, and Go's embed directive for single-binary deployment.

**HTTP Handling with Go Standard Library:** The basics involve creating a `http.NewServeMux()` router, defining handler functions with the signature `func(http.ResponseWriter, *http.Request)`, registering them with `router.HandleFunc()`, and starting the server with `srv.ListenAndServe()`. The book recommends creating a custom ServeMux rather than using `http.DefaultServeMux` to avoid exposing unwanted debugging endpoints. Each request runs in its own goroutine automatically.

**Gorilla Mux:** The Gorilla Mux library extends the standard router with powerful features: method-based routing (`.Methods(http.MethodGet)`), path variable capture using `{slug}` syntax, and `StrictSlash` handling. The book demonstrates separating GET and POST handlers for the same endpoint, reading request bodies with `ioutil.ReadAll()`, and extracting path variables with `mux.Vars(req)["slug"]`.

**Static Content Serving:** The `http.FileServer(http.Dir("./static"))` function serves files from a directory. This is combined with Gorilla Mux using a custom `staticHandler` struct that implements the `http.Handler` interface via `ServeHTTP()`.

**Dynamic Content with Templates:** The `html/template` package enables server-side rendering. HTML files contain Go template directives like `{{.}}` for variable interpolation. The `template.ParseFiles()` and `template.Execute()` functions parse and render templates with data. The book demonstrates form handling where `r.ParseForm()` extracts submitted values, validation logic processes them, and a result template is rendered.

**Go Embed Directive:** Available since Go 1.16, the `//go:embed` directive bundles files into the binary at compile time. Three patterns are demonstrated: embedding a single file (`//go:embed version/version.txt`), embedding a directory (`//go:embed static/*`), and embedding by pattern (`//go:embed tmpl/*.html`). The embedded content is accessed via `embed.FS` and served using `http.FS()` for static files or `template.ParseFS()` for templates. This produces a single self-contained binary that includes all HTML, CSS, and other assets.

### Chapter 5: Securing the Backend and Middleware

This chapter addresses authentication, middleware patterns, and session management with Redis.

**Authentication with bcrypt:** User passwords are hashed using the `golang.org/x/crypto/bcrypt` library. The `bcrypt.GenerateFromPassword()` function creates hashes, and `bcrypt.CompareHashAndPassword()` verifies them. The book creates a dummy user at application startup for testing. Authentication involves looking up the user by username via sqlc-generated `GetUserByName()` and then comparing the password hash.

**Middleware Pattern:** Middleware in Gorilla Mux follows the `func(http.Handler) http.Handler` signature. The `router.Use()` method registers middleware that executes for every request. The pattern wraps the next handler by calling `h.ServeHTTP(wr, req)` after performing pre-processing. The book shows a basic logging middleware that prints the URL path for each request.

**Session Management with Cookies:** Sessions solve the web's stateless nature by associating requests with users. The Gorilla sessions library (`github.com/gorilla/sessions`) provides cookie-based session stores. Sessions are retrieved with `store.Get(r, "session_token")`, values are stored in `session.Values["key"] = value`, and saved with `session.Save(r, w)`. Authentication status is tracked using an `authenticated` boolean in the session.

**Redis for Persistent Sessions:** In-memory sessions are lost on application restart, so the book integrates Redis for persistence. The `github.com/redis/go-redis` driver and `github.com/rbcervilla/redisstore` session store connect Redis to Gorilla sessions. Redis runs as a Docker container with a mounted volume for disk persistence. Logout is implemented by setting `session.Options.MaxAge = -1` to invalidate the session.

### Chapter 6: Moving to API-First

This chapter restructures the application around a JSON API, introducing proper project layout, CORS, and standardized error reporting.

**Project Structure:** The book adopts a common Go project layout: `internal/` for private packages (enforced by the Go tool to prevent external imports), `store/` for generated database code, `migrations/` for schema files, `queries/` for SQL queries, and a `generate.go` file using `//go:generate` directives. The API server is abstracted into `internal/api` with methods for starting, stopping, and adding routes with middleware.

**API Server Pattern:** A new `api.NewServer()` abstraction accepts a port, and routes are added via `server.AddRoute(path, handler, method, middleware...)`. Default middleware includes JSON enforcement and CORS. Protected routes append session validation middleware to the default stack.

**CORS (Cross-Origin Resource Sharing):** When frontend and backend run on different origins, browsers enforce CORS by sending preflight OPTIONS requests. The backend must respond with appropriate `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers` headers. The Gorilla handlers library's `handlers.CORS()` middleware configures allowed origins, methods, credentials, and headers.

**JSON Middleware:** This middleware enforces JSON-only communication by checking the `Content-Type` header for `application/json` and rejecting non-JSON requests with `http.StatusUnsupportedMediaType`. It also sets the response Content-Type header.

**Session Middleware:** Cookie-based session validation is extracted into middleware that retrieves the session, asserts type-safe values for `userID` and `userAuthenticated`, checks authentication status, and injects a `UserSession` into the request context using `context.WithValue()`. Handlers can then retrieve user information from context.

**JSON Request/Response Handling:** The book uses `json.NewDecoder(req.Body).Decode(&payload)` for streaming request parsing and `json.NewEncoder(wr).Encode(&data)` for responses. Struct tags like `json:"field_name,omitempty"` control serialization. The sqlc-generated model structs serve double duty as both database models and API response types.

**Standardized Error Reporting:** Two helper functions provide consistent JSON error and message formatting: `JSONError()` returns status codes with error messages, and `JSONMessage()` wraps successful responses. Both include a status field combining the numeric code and HTTP status text.

---

## Part 3: Single-Page Apps with Vue and Go

### Chapter 7: Frontend Frameworks

This chapter surveys the frontend landscape and introduces Vue.js as the book's chosen framework.

**Server-Side Rendering vs. Client-Side Rendering:** SSR (used in earlier chapters) generates HTML on the backend and sends complete pages on each request. CSR delivers a JavaScript bundle that renders dynamically in the browser, enabling single-page applications with improved interactivity and no page reloads. Reactivity -- automatic DOM updates when application state changes -- is a key attribute of CSR frameworks.

**Framework Comparison:**
- **React** (by Meta): Uses JSX syntax, offers maximum flexibility with many competing choices (Redux, Flux, React Router), has a full lifecycle model with hooks. The flexibility can lead to team debates about the "right" approach.
- **Svelte**: Pushes more work into the compilation step, transpiling to vanilla JavaScript without virtual DOM diffing. Lightweight but newer with fewer resources.
- **Vue** (chosen framework): Uses Single-File Components (SFCs) with separate `<template>`, `<script>`, and `<style scoped>` sections. Offers opinionated tooling (Vite, Vue Router), familiar HTML-like syntax, and is lightweight. The book prefers its opinionated nature as it reduces team debates.

**Creating Vue Applications:** A Vue application starts with `createApp()` and is mounted to a DOM element using `.mount('#app')`. The Options API defines `data()` for reactive state and `methods` for functions. Template interpolation uses `{{ variableName }}` syntax, and event binding uses `@click="functionName"`.

**Vite Build Tool:** Created by the Vue team, Vite (French for "quick") provides extremely fast hot module replacement during development and optimized production builds. The `npm create vite@latest` command scaffolds a new project. The `main.js` file initializes Vue with `createApp(App).mount('#app')`, and components are imported using the Composition API's `<script setup>` tag.

**Vue Router:** Enables SPA navigation by mapping URL paths to components. Routes are defined in a router configuration file with `path`, `name`, and `component` properties. The `<router-link>` tag creates navigation elements, and `<router-view>` renders the matched component. Both dynamic routes (`/users/:id`) and static routes are supported. The book uses `createWebHashHistory()` for hash-based routing.

### Chapter 8: Frontend Libraries

This chapter explores UI component libraries, form validation, and input formatting tools.

**Vuetify:** A Material Design framework built on Vue, providing pre-built components (color pickers, buttons, badges, data tables) with `<v-row>`, `<v-col>`, `<v-container>` layout primitives. Initialized as a Vue plugin via `Vue.use(Vuetify)`. Configuration is done through a plugins directory structure.

**Buefy:** Built on the Bulma CSS framework, Buefy offers lighter-weight components (carousels, breadcrumbs, sliders). Bulma itself is a pure CSS framework using semantic class names (`hero`, `section`, `columns`, `column`). Buefy is also initialized as a Vue plugin.

**Vuelidate for Form Validation:** Unlike vee-validate (which embeds validation rules in templates), Vuelidate decouples validation from templates by defining rules against the data model. The `$v` validation object exposes `$error`, `$dirty`, and individual validator states. Built-in validators include `required`, `minLength`, `email`, `alpha`, and many more. Validation rules can be organized across multiple forms using grouped validation collections.

**Cleave.js for Input Formatting:** Provides real-time input formatting for structured data like credit card numbers, phone numbers, and dates. While Vue support is not first-class, it can be integrated via custom directives. The `v-cleave` directive applies formatting rules such as `{ creditCard: true, onCreditCardTypeChanged: callback }`.

### Chapter 9: Tailwind, Middleware, and CORS

This chapter brings the frontend and backend together, introducing Tailwind CSS and Axios for API communication.

**Tailwind CSS:** Unlike opinionated frameworks (Vuetify, Buefy), Tailwind takes a utility-first approach, providing low-level CSS classes that directly manipulate individual properties (padding, margins, colors, responsive breakpoints). The Just-In-Time (JIT) compiler (default since v3) generates only the CSS actually used, eliminating bloat. Setup involves installing `tailwindcss`, creating a `tailwind.config.js` specifying content paths, and adding `@tailwind base/components/utilities` directives to a CSS file.

**Consuming Go APIs with Axios:** Axios is configured with a `baseURL` (from Vite's `import.meta.env.VITE_BASE_API_URL` environment variable) and `withCredentials: true` for cookie handling. API functions are organized in separate files under `src/api/`, importing the shared Axios instance. The `@` path alias (configured in `vite.config.js` using `path.resolve(__dirname, 'src')`) simplifies imports.

**CORS Configuration:** The backend must respond to OPTIONS preflight requests with appropriate headers. The Gorilla handlers CORS middleware is configured with `AllowedHeaders` (including `Content-Type`), `AllowedOrigins` (matching the frontend dev server URLs), `AllowCredentials()`, and `AllowedMethods`. Environment variables should drive these values in production.

**Vue/Axios Transformers:** When backend APIs use snake_case JSON keys but frontend code expects camelCase, Axios transformers bridge the gap. The `snakecase-keys` and `camelcase-keys` npm packages convert request payloads to snake_case (outbound) and response data to camelCase (inbound). Transformers are added to the Axios instance via `transformRequest` and `transformResponse` arrays.

### Chapter 10: Session Management

This chapter covers JWT-based session management, Vue Router navigation guards, and error page handling.

**JWT (JSON Web Tokens):** A JWT consists of three base64-encoded parts: header, payload (with claims), and signature. Standard claims include `iss` (issuer), `sub` (subject), `exp` (expiration), `iat` (issued at), and `jti` (unique ID). The `golang-jwt/jwt` library provides Go structs for these claims. Custom claims are created by embedding `jwt.StandardClaims` in a custom struct.

**JWT vs Cookie Sessions:** JWTs eliminate database round trips on each request by encoding user information in the token itself. The backend middleware decodes the JWT, extracts claims, and can make authorization decisions without querying the database.

**JWT Gotchas:**
- **"none" algorithm attack:** Malicious actors can decode the JWT, change the algorithm to "none", and strip the signature. Libraries must verify the algorithm matches expectations.
- **Logout problem:** JWTs remain valid until expiration regardless of server-side logout. A stolen JWT grants access until it expires.
- **Stale data:** User permission changes do not take effect until the JWT is refreshed.

**JWT Cookie Integration:** The `JWTProtectedMiddleware` checks for a `jwt-token` cookie, decodes it using `decodeJWTToUser()`, and if valid, refreshes the token with a new expiration. Cookies are configured with `HttpOnly: true` (prevents JavaScript access, mitigating XSS), `SameSite: LaxMode`, and `Secure: true` (HTTPS only). The `withCredentials: true` Axios setting ensures cookies are sent with cross-origin requests.

**Vue Router Navigation Guards:** Guards intercept navigation before components load, enabling authentication checks. The `router.beforeEach()` function receives `to` and `from` route objects and can return `false` (cancel), a route object (redirect), or `true`/`undefined` (allow). The book implements a `checkAuth()` guard that checks the `meta.requiresAuth` flag on routes and makes an API call to verify the session before allowing navigation.

**Catch-All Error Pages:** Vue Router v4 uses `{ path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }` as a wildcard route to handle 404 errors. This should be the last route in the configuration.

---

## Part 4: Release and Deployment

### Chapter 11: Feature Flags

This chapter introduces feature flags as a technique for enabling/disabling application features without code deployment.

**Feature Flag Concepts:** Feature flags act as on/off switches for application features. Use cases include segment targeting (enabling features for specific user demographics), risk mitigation (quickly disabling problematic features), and pre-launch feedback gathering. Flags can control frontend UI elements, route requests to different microservices, or determine which backend response to return.

**Open Source Feature Flag Server:** The book uses a custom feature flag server (github.com/nanikjava/feature-flags) running on port 8080. Flags are managed via REST API: POST to `/features` creates flags, PATCH to `/features/{key}` updates them, and GET retrieves flag state. Each flag has a `key`, `enabled` boolean, `users` array, `groups` array, and `percentage` for gradual rollout.

**Frontend Integration:** Vue components fetch flag state in the `mounted()` lifecycle hook using Axios GET requests. The flag's `enabled` value controls UI rendering via `v-if` directives, enabling or disabling buttons and other elements dynamically.

**Backend Microservice Integration:** A main server checks flags for multiple downstream services (e.g., `servicea`, `serviceb`) on startup using goroutines. The `checkFlags()` function makes HTTP GET requests to the feature flag server and returns boolean values. Handler functions conditionally call downstream services based on flag state, combining results into a single JSON response.

### Chapter 12: Building Continuous Integration

This chapter covers automating build, test, and deployment using GitHub Actions and GitHub Packages.

**CI Importance:** Continuous integration ensures all committed code compiles correctly and passes tests. This is critical in team environments to catch integration issues early and detect machine-specific dependencies.

**GitHub Actions Workflows:** Workflows are YAML files in `.github/workflows/` triggered by events like `push` to specific branches. The book's workflow has two jobs: `lint` (installs golangci-lint and runs code quality checks) and `build` (compiles the application with `make build`). Jobs run on `ubuntu-latest` runners and use GitHub Actions like `actions/setup-go@v1` and `actions/checkout@v1`.

**Dockerfile:** The book uses a multi-stage Docker build:
1. **Build stage:** Uses `golang:1.18` image to compile the Go binary with `CGO_ENABLED=0 GOOS=linux`
2. **Runtime stage:** Uses `alpine:latest` (minimal Linux) with the compiled binary copied from the build stage
3. **CMD** executes the binary

**GitHub Packages:** Docker images are published to GitHub Container Registry (ghcr.io) using the `docker/build-push-action@v3` GitHub Action. Authentication uses the automatic `GITHUB_TOKEN` secret. The workflow logs in with `docker/login-action@v2`, builds the image from the Dockerfile, tags it as `ghcr.io/{owner}/{repo}/chapter12:latest`, and pushes it. Images can then be pulled locally with `docker pull` and run with `docker run`.

### Chapter 13: Dockerizing an Application

This chapter provides a deeper exploration of Docker concepts including image storage, container inspection, and Docker Compose.

**Docker Fundamentals:** A Docker image is a file containing the application and OS files; when executed by the Docker engine, it becomes a container. Images are stored locally in `/var/lib/docker/image/overlay2/` and can be inspected with `docker image inspect`. The image metadata (architecture, commands, root filesystem layers) is stored as JSON.

**Container Inspection:** The `docker inspect` command reveals running container state including network configuration (port mappings), volume mounts, environment variables, and process information. The Mounts parameter shows host-to-container directory mappings, and NetworkSettings shows exposed ports.

**Multi-Stage Dockerfile:** The build pattern separates compilation from runtime:
```dockerfile
FROM golang:1.18 as builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -o bin/embed

FROM alpine:latest
RUN apk --update upgrade && apk --no-cache add curl ca-certificates
RUN mkdir -p /app
COPY --from=builder /app/bin/embed /app
WORKDIR /app
CMD /app/embed
```
This produces small images (~17MB) compared to the full Go build image (~964MB).

**Docker Compose:** The `compose.yaml` file defines multi-container applications:
```yaml
version: '3'
services:
  server:
    build: .
    ports:
      - "3333:3333"
  cache:
    image: redis:7.0.4-alpine
    restart: always
    ports:
      - '6379:6379'
```
Running `docker compose -f compose.yaml up` builds and starts all services together, managing networking automatically.

### Chapter 14: Cloud Deployment

This final chapter covers AWS infrastructure and Terraform for infrastructure-as-code deployment.

**AWS Infrastructure Overview:**
- **EC2 (Elastic Compute Cloud):** Virtual machines ranging from 512MB to 384GB memory configurations
- **EBS (Elastic Block Store):** Scalable block storage (HDD/SSD) that can grow without hardware changes
- **VPC (Virtual Private Cloud):** Software-defined networking connecting resources across Regions
- **RDS (Relational Database Service):** Managed database service supporting MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server
- **ECS (Elastic Container Service):** Container orchestration with auto-scaling capabilities

**Terraform Fundamentals:** Terraform provides Infrastructure as Code (IaC) using HashiCorp Configuration Language (HCL). The core workflow is:
1. `terraform init` -- downloads providers and initializes the working directory
2. `terraform plan` -- shows what changes will be made (adds, changes, destroys)
3. `terraform apply` -- executes the planned changes
4. `terraform destroy` -- removes all managed infrastructure

**Providers:** Terraform uses providers (plugins) to interact with cloud services. The book demonstrates the `kreuzwerker/docker` provider for local Docker operations and the `aws` provider for AWS resources. Providers are declared in the `required_providers` block and automatically downloaded during init.

**Local Docker Example:** The simplest Terraform example creates an nginx container:
```hcl
resource "docker_image" "nginx" {
  name = "nginx:latest"
}
resource "docker_container" "nginx" {
  image = docker_image.nginx.name
  name  = "hello-terraform"
  ports {
    internal = 80
    external = 8000
  }
}
```

**AWS EC2 Deployment:** Creating an EC2 instance requires a VPC, subnet, and the instance itself. AWS credentials are passed as variables. The configuration specifies the AMI, instance type (e.g., `t2.nano`), and subnet association.

**ECS with Load Balancer:** The most complex example deploys the application to ECS with:
- Internet gateway for VPC-to-internet connectivity
- Security groups controlling inbound/outbound traffic (allowing ports 80-3333)
- Two subnets required by the load balancer
- Application load balancer distributing traffic across targets
- ECS cluster, task definition (referencing the ghcr.io Docker image), and service
- Fargate launch type for serverless container execution

The task definition specifies CPU (1024), memory (2048), and the container image from GitHub Packages. The complete setup creates 12 AWS resources and outputs the load balancer URL for public access.

---

## Key Takeaways

1. **sqlc for Type-Safe Database Access:** Using sqlc to generate Go code from SQL queries provides complete separation between SQL and Go code, eliminates boilerplate, and ensures type safety. This pattern is more maintainable than ORMs for SQL-centric applications.

2. **Observability from the Start:** Logging (golog), tracing (OpenTelemetry/Jaeger), and metrics (Prometheus) should be built into applications from the beginning, not bolted on later. OpenTelemetry's vendor-agnostic specification makes it possible to switch backends without code changes.

3. **Go Embed for Single-Binary Deployment:** The `//go:embed` directive (Go 1.16+) enables packaging all web assets into a single executable, simplifying deployment dramatically. Combined with Docker multi-stage builds, this produces minimal container images.

4. **Middleware as a Core Pattern:** HTTP middleware in Go (using Gorilla Mux) provides a clean mechanism for cross-cutting concerns: authentication, session validation, JSON enforcement, CORS, and logging. The `func(http.Handler) http.Handler` signature enables composable middleware chains.

5. **JWT Trade-offs:** JWTs eliminate database lookups on each request but introduce security considerations (the "none" algorithm attack, inability to truly logout, stale permissions). The HttpOnly, Secure, and SameSite cookie flags are essential for protecting session tokens.

6. **Vue.js for Opinionated Frontend Development:** Vue's Single-File Components, opinionated toolchain (Vite, Vue Router), and clear separation of template/script/style reduce team friction. Navigation guards provide robust client-side authentication enforcement.

7. **Utility-First CSS with Tailwind:** Tailwind's approach of composing UI from small utility classes, combined with JIT compilation, avoids the bloat and override difficulties of component libraries while providing consistent design tokens.

8. **Axios Transformers Bridge API Format Gaps:** When frontend and backend use different JSON key conventions (camelCase vs snake_case), Axios request/response transformers handle the conversion transparently without modifying either codebase.

9. **Feature Flags for Controlled Rollout:** Feature flags decouple deployment from feature release, enabling gradual rollouts, A/B testing, risk mitigation, and emergency feature disabling without code changes.

10. **Infrastructure as Code with Terraform:** Terraform codifies cloud infrastructure, making it versionable, reviewable, and reproducible. The plan-apply-destroy workflow provides visibility into changes before execution, and the state management ensures infrastructure converges to the desired configuration.

11. **Full CI/CD Pipeline:** GitHub Actions automate linting, building, Docker image creation, and publishing to GitHub Packages. This ensures every code push is validated and deployable, catching issues before they reach production.

12. **Docker Multi-Stage Builds:** Separating the build environment (full Go toolchain) from the runtime environment (minimal Alpine Linux) dramatically reduces image size from hundreds of megabytes to tens of megabytes, improving deployment speed and security.
