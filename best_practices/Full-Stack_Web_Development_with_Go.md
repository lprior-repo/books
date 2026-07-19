# Full-Stack Web Development with Go
**Author:** Nanik Tolaram, Nick Glynn
**Topic tags:** `#api` `#general` `#go` `#architecture` `#web`
**Language focus:** Go-first (Vue.js frontend, Docker/Terraform ops)
**Sources:** `markdown_output/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram.md` · `summaries/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram.md`

## TL;DR
A fitness-tracking reference app is built end-to-end: PostgreSQL schema designed in SQL, `sqlc` generates all DB Go code, `gorilla/mux` provides routing/middleware, `html/template` + `//go:embed` produce a single self-contained binary, sessions graduate from cookies to Redis to JWT, `OpenTelemetry` + Jaeger + Prometheus give full observability, and GitHub Actions + multi-stage Docker + Terraform on AWS ECS complete the delivery pipeline. Apply when you need a complete, opinionated Go web stack blueprint with maximum SQL/Go separation and single-binary deployment.

---

## Best Practices by Topic

### Project Layout & Package Conventions  `#architecture` `#go`

**Principle:** Use the `internal/` directory for private application packages — the Go toolchain itself prevents external imports — and split generated DB code, migrations, queries, and HTTP handlers into distinct folders.

**Do:**
- Put private packages (api, auth, env) under `internal/` so they cannot be imported outside the module.
- Keep `store/` for sqlc-generated code, `migrations/` for schema files, `queries/` for SQL queries.
- Drive code generation through a `generate.go` file with `//go:generate` directives.
- Name files after the functionality they hold (`handlers.go`, `auth.go`, `env.go`).

**Don't:**
- Don't replicate the legacy `pkg/` directory idiom; the Go team removed it.
- Don't mix generated code with hand-written code in the same directory.

**Code:**
```go
package main
//go:generate echo Generating SQL Schemas
//go:generate sqlc generate
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining packages — generate.go"*

`sqlc.yaml` separates source from generated output:
```
path: store/
schema: migrations/
queries: queries/
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / migrations, queries, and store"*

---

### Database Setup with Docker & Postgres  `#general` `#web`

**Principle:** Run Postgres in Docker so the same command works on every developer's machine; mount the local directory so schema files are reachable inside the container.

**Do:**
- Use `-v $(pwd):/usr/share/chapterX` to mount the working directory into the container.
- Run psql from inside the running container: `docker exec -it test-postgres psql …`.
- Pin ports explicitly via `-p 5432:5432`; choose non-conflicting ports for parallel projects.

**Don't:**
- Don't install Postgres on bare metal — the install/maintenance cost is unjustified for development.

**Commands (verbatim from the book):**
```bash
docker run --name test-postgres \
-e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Setting up Postgres"*

```bash
docker exec -it test-postgres psql -h localhost -p 5432 -U 
postgres -d postgres
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Setting up Postgres"*

Mount-and-run pattern (chapter 1 sample):
```bash
docker run --name test-postgres -e POSTGRES_
PASSWORD=mysecretpassword -v $(pwd):/usr/share/chapter1 -p 
5432:5432 postgres
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Setting up the database"*

---

### Schema Design & Data Types (PostgreSQL)  `#architecture` `#general`

**Principle:** Choose the narrowest correct type per column — `BIGSERIAL` for synthetic primary keys, `JSONB` for flexible config blobs, `TIMESTAMP WITH TIME ZONE` for created_at, `BOOLEAN` for flags.

**Code:**
```sql
CREATE TABLE gowebapp.users (
User_ID BIGSERIAL PRIMARY KEY,
User_Name text NOT NULL,
Password_Hash text NOT NULL,
Name text NOT NULL,
Config JSONB DEFAULT '{}'::JSONB NOT NULL,
Created_At TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
Is_Enabled BOOLEAN DEFAULT TRUE NOT NULL
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Adding authentication"*

| Type | Use |
|------|-----|
| `BIGSERIAL` | Auto-incrementing primary key |
| `TEXT` | Variable-length strings |
| `JSONB` | Indexable, parseable JSON |
| `TIMESTAMP` | Date/time with timezone |
| `BOOLEAN` | true/false flag |

---

### sqlc — Generate Type-Safe Go From SQL  `#go` `#architecture`

**Principle:** Write SQL in `.sql` files and let `sqlc generate` emit fully typed Go — never write database boilerplate by hand. The developer writes pure SQL; the tool produces the Go.

**Do:**
- Configure `emit_db_tags`, `emit_json_tags`, and `json_tags_case_style` so the generated structs are usable both as DB rows and as JSON API models.
- Use `-- name: FunctionName :returnType` annotations (`:one`, `:many`, `:exec`) to control generated signatures.
- Re-run `sqlc generate` via `make generate` after every schema/query change.

**Don't:**
- Don't hand-edit generated files (they live under `gen/` or `store/`).
- Don't reach for an ORM unless you genuinely need cross-DB portability — sqlc's SQL-first approach is more maintainable for SQL-centric apps.

**`sqlc.yaml` config (full):**
```
---
version: '1'
packages:
 - name: chapter1
 path: gen
 schema: db/
 queries: queries/
 engine: postgresql
 emit_db_tags: true
 emit_interface: false
 emit_exact_table_names: false
 emit_empty_slices: false
 emit_exported_queries: false
 emit_json_tags: true
 json_tags_case_style: camel
 output_files_suffix: _gen
 emit_prepared_queries: false
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc"*

**Schema snippet (`schema.sql`):**
```sql
CREATE SCHEMA IF NOT EXISTS gowebapp;
CREATE TABLE gowebapp.users (
User_ID BIGSERIAL PRIMARY KEY,
User_Name text NOT NULL,
....
);
....
CREATE TABLE gowebapp.sets (
Set_ID BIGSERIAL PRIMARY KEY,
Exercise_ID BIGINT NOT NULL,
Weight INT NOT NULL DEFAULT 0
);
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc"*

**Query snippet (`query.sql`) — annotations drive the Go signature:**
```sql
-- name: ListUsers :many
-- get all users ordered by the username
SELECT *
```
```sql
FROM gowebapp.users
ORDER BY user_name;
...
-- name: DeleteUserImage :exec
-- delete a particular user's image
DELETE
FROM gowebapp.images i
WHERE i.user_id = $1;
...
-- name: UpsertExercise :one
-- insert or update exercise of a particular id
INSERT INTO gowebapp.exercises (Exercise_Name)
VALUES ($1) ON CONFLICT (Exercise_ID) DO
UPDATE
 SET Exercise_Name = EXCLUDED.Exercise_Name
 RETURNING Exercise_ID;
-- name: CreateUserImage :one
-- insert a new image
INSERT INTO gowebapp.images (User_ID, Content_Type,
 Image_Data)
values ($1,
 $2,
 $3) RETURNING *;
...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc"*

---

### sqlc Generated Output — `db.go`  `#go`

**Principle:** The generated `db.go` exposes a `DBTX` interface accepting either `*sql.DB` or `*sql.Conn`, plus a `WithTx` helper to bind the Queries object to a transaction.

**Code:**
```go
func New(db DBTX) *Queries {
 return &Queries{db: db}
}
func (q *Queries) WithTx(tx *sql.Tx) *Queries {
 return &Queries{
 db: tx,
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc — db.go"*

---

### sqlc Generated Output — `models.go`  `#go`

**Principle:** Generated structs carry both `db:` and `json:` tags (controlled by `emit_db_tags` and `emit_json_tags`) so they serve as both row types and API response bodies.

**Code:**
```go
type GowebappExercise struct {
 ExerciseID int64 `db:"exercise_id"
json:"exerciseID"`
 ExerciseName string `db:"exercise_name"
json:"exerciseName"`
}
...
type GowebappWorkout struct {
 WorkoutID int64 `db:"workout_id"
json:"workoutID"`
 UserID int64 `db:"user_id" json:"userID"`
 SetID int64 `db:"set_id" json:"setID"`
 StartDate time.Time `db:"start_date"
json:"startDate"`
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc — models.go"*

---

### sqlc Generated Output — `query.sql_gen.go`  `#go`

**Principle:** Each annotated query becomes a typed method on `*Queries` that takes a `context.Context` and the named params and returns the row struct (or error). Constants hold the literal SQL for traceability.

**Code:**
```go
const deleteUsers = `-- name: DeleteUsers :exec
DELETE FROM gowebapp.users
WHERE user_id = $1
`
func (q *Queries) DeleteUsers(ctx context.Context,
userID int64) error {
 _, err := q.db.ExecContext(ctx, deleteUsers, userID)
 return err
}
...
const getUsers = `-- name: GetUsers :one
SELECT user_id, user_name, pass_word_hash, name, config, 
created_at, is_enabled FROM gowebapp.users
WHERE user_id = $1 LIMIT 1
`
func (q *Queries) GetUsers(ctx context.Context, userID 
int64) (GowebappUser, error) {
 row := q.db.QueryRowContext(ctx, getUsers, userID)
 var i GowebappUser
 err := row.Scan(
 &i.UserID,
 &i.UserName,
 &i.PassWordHash,
 &i.Name,
 &i.Config,
 &i.CreatedAt,
 &i.IsEnabled,
 )
 return i, err
```
```go
}
...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc — query.sql_gen.go"*

---

### Using sqlc from `main.go`  `#go`

**Principle:** Open the pool with `sql.Open`, validate connectivity with `db.Ping()`, then build the `Queries` object via the generated `New(db)` constructor. Insert by passing a generated `CreateUsersParams` struct.

**Code:**
```go
package main
import (
 ...
)
func main() {
 ...
 // Open the database
 db, err := sql.Open("postgres", dbURI)
 if err != nil {
 panic(err)
 }
 // Connectivity check
 if err := db.Ping(); err != nil {
 log.Fatalln("Error from database ping:", err)
 }
 // Create the store
 st := chapter1.New(db)
 st.CreateUsers(context.Background(),
 chapter1.CreateUsersParams{
 UserName: "testuser",
 PassWordHash: "hash",
 Name: "test",
 })
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Generating CRUD with sqlc"*

---

### Makefile Automation  `#general`

**Principle:** Wrap every multi-step dev task (DB up/down, sqlc regenerate, schema load) in a Makefile so the whole team runs identical commands.

**Code:**
```makefile
..
.PHONY : postgresup postgresdown psql createdb teardown_
recreate generate
```
```makefile
postgresup:
 docker run --name test-postgres -v $(PWD):/usr/share/
chapter1 -e POSTGRES_PASSWORD=$(DB_PWD) -p 5432:5432 -d $(DB_
NAME)
...
# task to create database without typing it manually
createdb:
 docker exec -it test-postgres psql $(PSQLURL) -c "\i /usr/
share/chapter1/db/schema.sql"
...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 1 / Building the makefile"*

---

### Standard Library `log` Package  `#go`

**Principle:** The stdlib `log` package covers basic needs (`Print`, `Fatal`, `Panic`, `Printf`) plus configurable flags for date/time/file prefixes, but it lacks leveled logging, JSON output, and multi-destination routing.

**Do:**
- Use `SetFlags(log.LstdFlags)` for default date+time prefix.
- Use `Lshortfile` during development to track call sites.

**Don't:**
- Don't rely on the stdlib logger for production services that need severity filtering or structured output.

**Available functions:**
```go
func (l *Logger) Fatal(v ...interface{})
func (l *Logger) Fatalf(format string, v ...interface{})
func (l *Logger) Fatalln(v ...interface{})
func (l *Logger) Panic(v ...interface{})
func (l *Logger) Prefix() string
func (l *Logger) Print(v ...interface{})
func (l *Logger) Printf(format string, v ...interface{})
func (l *Logger) Println(v ...interface{})
func (l *Logger) SetFlags(flag int)
func (l *Logger) SetOutput(w io.Writer)
func (l *Logger) SetPrefix(prefix string)
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Exploring Go standard logging"*

**SetFlags example:**
```go
func main() {
 ...
 // set log format to - dd/mm/yy hh:mm:ss
 ol.SetFlags(log.LstdFlags)
 ol.Println(«Just a log text»)
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Exploring Go standard logging"*

| Flag | Effect |
|------|--------|
| `Ldate` | Date in local timezone (YYYY/MM/DD) |
| `Ltime` | Time HH:MM:SS |
| `Lmicroseconds` | Microsecond precision |
| `Llongfile` | Full file path + line |
| `Lshortfile` | Final filename + line |
| `LUTC` | Use UTC instead of local timezone |
| `Lmsgprefix` | Prefix text before message |
| `LstdFlags` | `Ldate | Ltime` |

---

### Levelled Logging with `golog`  `#go` `#general`

**Principle:** For severity-based filtering (INFO/DEBUG/WARN/ERROR/FATAL) use `github.com/kataras/golog` — same ergonomic API as stdlib but with colors and level filtering.

**Code:**
```go
func main() {
 golog.SetLevel(«error»)
 golog.Println(«This is a raw message, no levels, no
 colors.»)
 golog.Info(«This is an info message, with colors (if the
 output is terminal)»)
 golog.Warn(«This is a warning message»)
 golog.Error(«This is an error message»)
 golog.Debug(«This is a debug message»)
 golog.Fatal(`Fatal will exit no matter what,
 but it will also print the log message if
 logger›s Level is >=FatalLevel`)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Using golog"*

| Severity | Purpose |
|----------|---------|
| INFO | Informational |
| WARN | Watch closely — may worsen |
| ERROR | Needs attention |
| DEBUG | Troubleshooting/tracing detail |
| FATAL | Immediate response required |

---

### Per-Level Output Routing  `#go` `#general`

**Principle:** Use `golog.SetLevelOutput(level, io.Writer)` to split log streams — errors to one file, info to another, everything else to stdout.

**Code:**
```go
func configureLogger() {
 // open infolog.txt append if exist (os.O_APPEND) or
 // create if not (os.O_CREATE) and read write
 // (os.O_WRONLY)
 infof, err := os.OpenFile(logFile,
 os.O_APPEND|os.O_CREATE|os.O_WRONLY,
 0666)
```
```go
 ...
 golog.SetLevelOutput(«info», infof)
 // open infoerr.txt append if exist (os.O_APPEND) or
 create if not (os.O_CREATE) and read write
 // (os.O_WRONLY)
 // errf, err := os.OpenFile(«infoerr.txt»,
 os.O_APPEND|os.O_CREATE|os.O_WRONLY,
 0666)
 ...
 golog.SetLevelOutput(«error», errf)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Local logging"*

---

### Centralized REST Logging Server  `#api` `#go` `#architecture`

**Principle:** In a distributed/cloud environment, build a small HTTP server (e.g. Gorilla Mux on port 8010, endpoint `/log`, method POST) to aggregate logs from many app instances in one place.

**Do:**
- Accept JSON payloads containing `timestamp`, `level`, `message`.
- Return HTTP 201 Created when the log entry has been received/printed.

**Server bootstrap:**
```go
import (
 ...
 «github.com/gorilla/mux»
 ...
)
func runServer(addr string) {
 router = mux.NewRouter()
 initializeRoutes()
 ...
```
```go
 log.Fatal(http.ListenAndServe(addr, router))
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Writing log messages to the logging server"*

**Route registration — only POST is allowed:**
```go
func initializeRoutes() {
 router.HandleFunc(«/log», loghandler).Methods(http.
 MethodPost)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Writing log messages to the logging server"*

**Handler — read body then acknowledge with 201:**
```go
func loghandler(w http.ResponseWriter, r *http.Request) {
 body, err := ioutil.ReadAll(r.Body)
 ...
 w.WriteHeader(http.StatusCreated)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Writing log messages to the logging server"*

---

### Multi-Output Logging Wrapper  `#go` `#general`

**Principle:** Wrap the logger so a `-local=true` flag toggles between stdout+file and HTTP-POST-to-remote-server modes — same binary works for development and production.

**Driver — `flag.Bool` selects the destination:**
```go
func main() {
 l := flag.Bool(«local», false, «true - send to stdout, false
 - send to logging server»)
 flag.Parse()
 logger.SetLoggingOutput(*l)
 logger.Logger.Debugf(«Application logging to stdout =
 %v», *l)
 ...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Configuring multiple outputs"*

**Local mode:**
```go
...
func configureLocal() {
 file, err := os.OpenFile(«logs.txt»,
 os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
 ...
 Logger.SetOutput(os.Stdout)
 Logger.SetLevel(«debug»)
 Logger.SetLevelOutput(«info», file)
}
...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Configuring multiple outputs"*

**Remote mode — implement `io.Writer` and POST asynchronously:**
```go
//configureRemote for remote logger configuration
func configureRemote() {
 r := remote{}
 Logger.SetLevelFormat(«info», «json»)
 Logger.SetLevelOutput(«info», r)
```
```go
func (r remote) Write(data []byte) (n int, err error) {
 go func() {
 req, err := http.NewRequest("POST",
 «http://localhost:8010/log»,
 bytes.NewBuffer(data),
 )
 ...
 resp, _ := client.Do(req)
 defer resp.Body.Close()
 }
 }()
 return len(data), nil
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 2 / Configuring multiple outputs"*

---

### OpenTelemetry — TracerProvider Initialization  `#go` `#architecture`

**Principle:** Build the Jaeger exporter once at startup, wrap it in a `TracerProvider` with a `resource` describing the service, and register it globally via `otel.SetTracerProvider`.

**Code (tracing.go):**
```go
 package trace
 import (
 «context»
 «go.opentelemetry.io/otel"
 «go.opentelemetry.io/otel/exporters/jaeger"
 «go.opentelemetry.io/otel/sdk/resource"
 «go.opentelemetry.io/otel/sdk/trace"
 sc "go.opentelemetry.io/otel/semconv/v1.4.0"
 )
 type ShutdownTracing func(ctx context.Context) error
 func InitTracing(service string) (ShutdownTracing, error)
 {
 // Create the Jaeger exporter.
 exp, err := jaeger.New(jaeger.WithCollectorEndpoint())
 if err != nil {
 return func(ctx context.Context) error { return nil },
 err
 }
 // Create the TracerProvider.
 tp := trace.NewTracerProvider(
 trace.WithBatcher(exp),
```
```go
 trace.WithResource(resource.NewWithAttributes(
 sc.SchemaURL,
 sc.ServiceNameKey.String(service),
 )),
 )
 otel.SetTracerProvider(tp)
 return tp.Shutdown, nil
 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Integrating the Jaeger SDK"*

---

### OpenTelemetry — Creating Spans  `#go`

**Principle:** Start spans with `otel.Tracer(name).Start(ctx, "operation")`, always `defer span.End()`, attach attributes for queryable detail, and nest spans across goroutines to build a DAG.

**Code (main.go):**
```go
 package main
 import (
 t "chapter.3/trace/trace"
 "context"
 "fmt"
 "go.opentelemetry.io/otel"
 "go.opentelemetry.io/otel/attribute"
 "go.opentelemetry.io/otel/trace"
 "log"
```
```go
 "sync"
 "time"
 )
 const serviceName = "tracing"
 func main() {
 sTracing, err := t.InitTracing(serviceName)
 if err != nil {
 log.Fatalf("Failed to setup tracing: %v\n", err)
 }
 defer func() {
 if err := sTracing(context.Background()); err != nil
 {
 log.Printf("Failed to shutdown tracing: %v\n", err)
 }
 }()
 ctx, span := otel.Tracer(serviceName)
 .Start(context.Background(), "outside")
 defer span.End()
 var wg sync.WaitGroup
 wg.Add(1)
 go func() {
 _, s := otel.Tracer(serviceName).Start(ctx, "inside")
 ...
 wg.Done()
 }()
 wg.Add(1)
 go func() {
 _, ss := otel.Tracer(serviceName).Start(ctx,
 "inside")
 ...
 wg.Done()
```
```go
 }()
 wg.Wait()
 fmt.Println("\nDone!")
 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Integration with Jaeger"*

---

### The `Span` Interface  `#go`

**Principle:** A Span represents one operation. Multiple spans compose into a trace forming a DAG. The interface exposes lifecycle (`End`, `IsRecording`), event (`AddEvent`, `RecordError`), and metadata (`SetAttributes`, `SetStatus`, `SetName`) operations.

**Code:**
```go
type Span interface {
 End(options ...SpanEndOption)
 AddEvent(name string, options ...EventOption)
 IsRecording() bool
 RecordError(err error, options ...EventOption)
 SpanContext() SpanContext
 SetStatus(code codes.Code, description string)
 SetName(name string)
 SetAttributes(kv ...attribute.KeyValue)
 TracerProvider() TracerProvider
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Integration with Jaeger"*

---

### Nested Goroutine Spans with Attributes  `#go`

**Principle:** Each goroutine should open its own child span off the parent context, set attributes that uniquely identify the work, then end the span via `defer`.

**Code:**
```go
go func() {
 _, s := otel.Tracer(serviceName).Start(ctx, "inside")
 defer s.End()
 time.Sleep(1 * time.Second)
 s.SetAttributes(attribute.String("sleep", "done"))
 s.SetAttributes(attribute.String("go func", "1"))
 wg.Done()
}()
...
...
go func() {
 _, ss := otel.Tracer(serviceName).Start(ctx, "inside")
 defer ss.End()
 time.Sleep(2 * time.Second)
 ss.SetAttributes(attribute.String("sleep", "done"))
 ss.SetAttributes(attribute.String("go func", "2"))
 wg.Done()
}()
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / DAGs"*

---

### Prometheus Metrics with OpenTelemetry  `#go` `#architecture`

**Principle:** Initialize the Prometheus exporter, register it as the global MeterProvider, and expose it via an HTTP server on a dedicated port (e.g. `:2112`) that Prometheus scrapes on an interval.

**Code (metrics.go):**
```go
package metric
...
type ShutdownMetrics func(ctx context.Context) error
// InitMetrics use Prometheus exporter
func InitMetrics(service string) (ShutdownMetrics, error) {
 config := prometheus.Config{}
```
```go
 c := controller.New(
 processor.NewFactory(
 selector.NewWithExactDistribution(),
 aggregation.CumulativeTemporalitySelector(),
 processor.WithMemory(true),
 ),
 controller.WithResource(resource.NewWithAttributes(
 semconv.SchemaURL,
 semconv.ServiceNameKey.String(service),
 )),
 )
 exporter, err := prometheus.New(config, c)
 if err != nil {
 return func(ctx context.Context) error { return nil},
 err
 }
 global.SetMeterProvider(exporter.MeterProvider())
 srv := &http.Server{Addr: ":2112", Handler: exporter}
 go func() {
 _ = srv.ListenAndServe()
 }()
 return srv.Shutdown, nil
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Adding metrics using Prometheus"*

**Recording a counter on every request (main.go):**
```go
package main
...
const serviceName = "samplemetrics"
func main() {
 ...
 //setup handler for rqeuest
```
```go
 r.HandleFunc("/", func(rw http.ResponseWriter, r
 *http.Request) {
 log.Println("Reporting metric metric.totalrequest")
 ctx := r.Context()
 //add request metric counter
 ctr.Add(ctx, 1)
 ...
 }).Methods("GET")
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Adding metrics using Prometheus"*

Prometheus `config.yml` (scrapes the host machine on `:2112` every 5 s):
```yaml
scrape_configs:
 - job_name: 'prometheus'
 scrape_interval: 5s
 static_configs:
 - targets:
 - host.docker.internal:2112
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Adding metrics using Prometheus"*

---

### HTTP Fundamentals — `net/http` Server  `#api` `#go` `#web`

**Principle:** Build a custom `*ServeMux` via `http.NewServeMux()` rather than reusing `http.DefaultServeMux` (which exposes debug endpoints). Configure the server with explicit `ReadTimeout`, `WriteTimeout`, and `MaxHeaderBytes`. Every request runs in its own goroutine.

**Do:**
- Always set timeouts to avoid slowloris-style resource exhaustion.
- Use `router.HandleFunc(pattern, handler)` to wire endpoints.

**Don't:**
- Don't use `http.DefaultServeMux` in production — it leaks debug endpoints.

**Code:**
```go
 1 package main
 2
 3 import (
 4 "fmt"
 5 "log"
 6 "net/http"
 7 "os"
 8 "time"
 9 )
 10
 11 func handlerGetHelloWorld(wr http.ResponseWriter,
 req *http.Request) {
 12 fmt.Fprintf(wr, "Hello, World\n")
 13 log.Println(req.Method) // request method
 14 log.Println(req.URL) // request URL
 15 log.Println(req.Header) // request headers
 16 log.Println(req.Body) // request body)
 17 }
 18
 ...
 29
 30 func main() {
 ...
 43 router := http.NewServeMux()
 44
 45 srv := http.Server{
 46 Addr: ":" + port,
 47 Handler: router,
```
```go
 48 ReadTimeout: 10 * time.Second,
 49 WriteTimeout: 120 * time.Second,
 50 MaxHeaderBytes: 1 << 20,
 51 }
 52
 ...
 57 router.HandleFunc("/", handlerGetHelloWorld)
 58 router.Handle("/1", dummyHandler)
 59 err := srv.ListenAndServe()
 60 if err != nil {
 61 log.Fatalln("Couldnt ListenAndServe()",
 err)
 62 }
 63 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Hello, World with defaults"*

---

### Method Switch Inside a Handler  `#api` `#go`

**Principle:** When you can't register per-method routes, dispatch inside the handler with a `switch req.Method` and always include a `default` returning `http.StatusMethodNotAllowed`.

**Code:**
```go
func methodFunc(wr http.ResponseWriter, req http.Request) {
 ...
 switch req.Method {
 case http.MethodGet:
 // Serve page - GET is the default when you visit a
 // site.
 case http.MethodPost:
 // Take user provided data and create a record.
 case http.MethodPut:
 // Update an existing record.
 case http.MethodDelete:
 // Remove the record.
 default:
 http.Error(wr, "Unsupported Method!",
 http.StatusMethodNotAllowed)
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Handling HTTP functions and Gorilla Mux"*

---

### Gorilla Mux — Method Routing & Path Slugs  `#api` `#go` `#web`

**Principle:** Use `mux.NewRouter().StrictSlash(true)` so trailing slashes are normalized, register handlers with `.Methods(http.MethodGet)` for per-verb dispatch, and capture path segments with `{slug}` retrieved via `mux.Vars(req)["slug"]`.

**Do:**
- Read the request body exactly once via `ioutil.ReadAll(req.Body)` — it's an `io.ReadCloser`.
- Echo request bodies back with `io.Copy(wr, bytes.NewReader(body))`.

**Code:**
```go
 1 package main
 2
 3 import (
 4 "bytes"
 5 "fmt"
 6 "io"
 7 "io/ioutil"
 8 "log"
 9 "net/http"
 10 "os"
 11
 12 "github.com/gorilla/mux"
 13 )
 14
 15 func handlerSlug(wr http.ResponseWriter, req
 *http.Request) {
 16 slug := mux.Vars(req)["slug"]
 17 if slug == "" {
 18 log.Println("Slug not provided")
 19 return
 20 }
 21 log.Println("Got slug", slug)
 22 }
 23
 24 func handlerGetHelloWorld(wr http.ResponseWriter,
 req *http.Request) {
 25 fmt.Fprintf(wr, "Hello, World\n")
 26 log.Println("Request via", req.Method)
 27 log.Println(req.URL)
 28 log.Println(req.Header)
 29 log.Println(req.Body)
```
```go
 30 }
 31
 32 func handlerPostEcho(wr http.ResponseWriter,
 req *http.Request) {
 33 log.Println("Request via", req.Method)
 34 log.Println(req.URL)
 35 log.Println(req.Header)
 36
 37 // We are going to read it into a buffer
 38 // as the request body is an io.ReadCloser
 39 // and so we should only read it once.
 40 body, err := ioutil.ReadAll(req.Body)
 41
 42 log.Println("read >", string(body), "<")
 43
 44 n, err := io.Copy(wr, bytes.NewReader(body))
 45 if err != nil {
 46 log.Println("Error echoing response",
 err)
 47 }
 48 log.Println("Wrote back", n, "bytes")
 49 }
 50
 51 func main() {
 52 log.SetFlags(log.Lshortfile | log.Ldate |
 log.Lmicroseconds)
 53
 54 port := "9002"
 55 if value, exists :=
 os.LookupEnv("SERVER_PORT"); exists {
 56 port = value
 57 }
 58
 59 // StrictSlash:true -> "/foo/" redirects to "/foo"
 // (and vice versa).
 60
 67 router := mux.NewRouter().StrictSlash(true)
 68
 69 srv := http.Server{
 70 Addr: ":" + port,
 71 Handler: router,
 72 }
 73
 74 router.HandleFunc("/", handlerGetHelloWorld)
 .Methods(http.MethodGet)
 75 router.HandleFunc("/", handlerPostEcho)
 .Methods(http.MethodPost)
 76 router.HandleFunc("/{slug}", handlerSlug)
 .Methods(http.MethodGet)
 77
 78 log.Println("Starting on", port)
 79 err := srv.ListenAndServe()
 80 if err != nil {
 81 log.Fatalln("Couldnt ListenAndServe()", err)
 82 }
 83 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Building on the basics with Gorilla Mux"*

---

### Serving Static Content  `#web` `#go`

**Principle:** `http.FileServer(http.Dir("./static"))` is the simplest way to serve a directory of static assets; pair it with `http.Handle("/", fs)` and `http.ListenAndServe(":port", nil)`.

**Code:**
```go
 1 package main
 2
 3 import (
 4 "log"
 5 "net/http"
 6 )
 7
 8 func main() {
 9 fs := http.FileServer(http.Dir("./static"))
 10 http.Handle("/", fs)
 11
 12 log.Println("Starting up server on port 3333
 ...")
 13 err := http.ListenAndServe(":3333", nil)
 14 if err != nil {
 15 log.Fatal("error occurred starting up
 server : ", err)
 16 }
 17 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Rendering static content"*

---

### Dynamic Templates with `html/template`  `#web` `#go`

**Principle:** Implement a custom `http.Handler` struct for the static SPA fallback, register POST handlers separately with Gorilla Mux, parse form data with `r.ParseForm()`, validate, then render an `html/template` parsed with `template.ParseFiles` / `template.Must`.

**Code:**
```go
 1 package main
 2
 3 import (
 4 "fmt"
 5 "github.com/gorilla/mux"
 6 "html/template"
 7 "log"
 8 "net/http"
 9 "os"
 10 "path/filepath"
 11 "time"
 12 )
 13
 14 type staticHandler struct {
 15 staticPath string
 16 indexPage string
 17 }
```
```go
 19 func (h staticHandler) ServeHTTP(w
 http.ResponseWriter, r *http.Request) {
 20 path, err := filepath.Abs(r.URL.Path)
 21 log.Println(r.URL.Path)
 22 if err != nil {
 23 http.Error(w, err.Error(),
 http.StatusBadRequest)
 24 return
 25 }
 26
 27 path = filepath.Join(h.staticPath, path)
 28
 29 _, err = os.Stat(path)
 30
 31 http.FileServer(
 32 http.Dir(h.staticPath)).ServeHTTP(w, r)
 33 }
 34
 35 func postHandler(w http.ResponseWriter,
 r *http.Request) {
 36 result := "Login "
 37 r.ParseForm()
 38
 39 if validateUser(r.FormValue("username"),
 r.FormValue("password")) {
 40 result = result + "successfull"
 41 } else {
 42 result = result + "unsuccessful"
 43 }
 44
 45 t, err :=
 template.ParseFiles("static/tmpl/msg.html")
 46
 47 if err != nil {
 48 fmt.Fprintf(w, "error processing")
 49 return
 50 }
 51
 52 tpl := template.Must(t, err)
 53
 54 tpl.Execute(w, result)
 55 }
 56
 57 func validateUser(username string,
 password string) bool {
 58 return (username == "admin") &&
 59 (password == "admin")
 60 }
 61
 62 func main() {
 63 router := mux.NewRouter()
 64
 65 router.HandleFunc("/login",
 postHandler).Methods("POST")
 66
 67 spa := staticHandler{staticPath: "static",
 indexPage: "index.html"}
 68 router.PathPrefix("/").Handler(spa)
 69
 70 srv := &http.Server{
 71 Handler: router,
 72 Addr: "127.0.0.1:3333",
 73 WriteTimeout: 15 * time.Second,
 74 ReadTimeout: 15 * time.Second,
 75 }
 76
 77 log.Fatal(srv.ListenAndServe())
 78 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Rendering dynamic content"*

**Template uses `{{.}}` for top-level interpolation:**
```html
 1 <!DOCTYPE html>
 2 <html>
 3 <head>
 ...
 18 <p class="text-xs text-gray-50">{{.}}
 </p>
 ...
 24 </html>
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Rendering dynamic content"*

---

### `//go:embed` — Bundle Assets Into the Binary  `#go` `#web` `#architecture`

**Principle:** Available since Go 1.16, `//go:embed` inlines files into the binary at compile time, producing a single self-contained executable. Embed single files (`//go:embed version/version.txt`), directories (`//go:embed static/*`), or patterns (`//go:embed tmpl/*.html`) into `embed.FS` variables.

**Do:**
- Use `fs.Sub(staticEmbed, "static")` to strip a prefix before passing to `http.FileServer(http.FS(fsys))`.
- Use `template.ParseFS(tmplEmbed, "tmpl/name.html")` to render embedded templates.

**Code:**
```go
 1 package main
 2
 3 import (
 4 "embed"
 5 "fmt"
 6 "github.com/gorilla/mux"
 7 "html/template"
 8 "io/fs"
 9 "log"
 10 "net/http"
 11 "os"
 12 "path/filepath"
 13 "strings"
 14 "time"
 15 )
 16
 17 var (
 18 Version string = strings.TrimSpace(version)
 19 //go:embed version/version.txt
 20 version string
 21
 22 //go:embed static/*
 23 staticEmbed embed.FS
 24
 25 //go:embed tmpl/*.html
 26 tmplEmbed embed.FS
 27 )
 28
 29 type staticHandler struct {
 30 staticPath string
 31 indexPage string
```
```go
 32 }
 33
 34 func (h staticHandler) ServeHTTP(w
 http.ResponseWriter, r *http.Request) {
 35 path, err := filepath.Abs(r.URL.Path)
 36 log.Println(r.URL.Path)
 37 if err != nil {
 38 http.Error(w, err.Error(),
 http.StatusBadRequest)
 39 return
 40 }
 41
 42 path = filepath.Join(h.staticPath, path)
 43
 44 _, err = os.Stat(path)
 45
 46 log.Print("using embed mode")
 47 fsys, err := fs.Sub(staticEmbed, "static")
 48 if err != nil {
 49 panic(err)
 50 }
 51
 52 http.FileServer(http.FS(fsys)).ServeHTTP(w,
 r)
 53 }
 54
 55 //renderFiles renders file and push data (d) into
 56 // the templates to be rendered
 57 func renderFiles(tmpl string, w
 http.ResponseWriter, d interface{}) {
 58 t, err := template.ParseFS(tmplEmbed,
 59 fmt.Sprintf("tmpl/%s.html", tmpl))
 60 if err != nil {
 61 log.Fatal(err)
 62 }
 63
 64 if err := t.Execute(w, d); err != nil {
 65 log.Fatal(err)
 66 }
 67 }
 68
 69 func postHandler(w http.ResponseWriter,
 r *http.Request) {
 70 result := "Login "
 71 r.ParseForm()
 72
 73 if validateUser(r.FormValue("username"),
 r.FormValue("password")) {
 74 result = result + "successfull"
 75 } else {
 76 result = result + "unsuccessful"
 77 }
 78
 79 renderFiles("msg", w, result)
 80 }
 81
 82 func validateUser(username string,
 password string) bool {
 83 return (username == "admin") &&
 84 (password == "admin")
 85 }
 86
 87 func main() {
 88 log.Println("Server Version :", Version)
 89
 90 router := mux.NewRouter()
 91
 92 router.HandleFunc("/login", postHandler)
 93 .Methods("POST")
 94
 95 spa := staticHandler{staticPath: "static",
 indexPage: "index.html"}
 96 router.PathPrefix("/").Handler(spa)
 97
 98 srv := &http.Server{
 99 Handler: router,
100 Addr: "127.0.0.1:3333",
101 WriteTimeout: 15 * time.Second,
102 ReadTimeout: 15 * time.Second,
103 }
104
105 log.Fatal(srv.ListenAndServe())
106 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 4 / Using Go embed to bundle your content"*

---

### Password Hashing with `bcrypt`  `#go` `#api`

**Principle:** Hash passwords with `bcrypt.GenerateFromPassword(pwd, cost)` — cost 14 in this book — and verify with `bcrypt.CompareHashAndPassword`, which returns `nil` on match.

**Do:**
- Always store hashes, never plaintext.
- Pick the highest bcrypt cost your latency budget allows.

**Don't:**
- Don't compare hashes with `==` or `subtle.ConstantTimeCompare` — let bcrypt do the comparison internally.

**Hash function:**
```go
func HashPassword(password string) (string, error) {
 bytes, err := 
 bcrypt.GenerateFromPassword([]byte(password), 14)
 return string(bytes), err
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Creating our dummy user"*

**Verify function:**
```go
func CheckPasswordHash(password, hash string) bool {
 err := bcrypt.CompareHashAndPassword([]byte(hash), 
 []byte(password))
return err == nil
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Authenticating a user"*

**Validate user against DB:**
```go
func validateUser(username string, password string) bool {
 ...
 u, _ := dbQuery.GetUserByName(ctx, username)
 ...
 return pkg.CheckPasswordHash(password, u.PassWordHash)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Authenticating a user"*

---

### Bootstrapping a Dummy User  `#go`

**Principle:** On startup, check whether a known test user already exists; if not, create one with a hashed password. This keeps demo/test environments self-seeding.

**Code:**
```go
func createUserDb(ctx context.Context) {
 //has the user been created
 u, _ := dbQuery.GetUserByName(ctx, "user@user")
 if u.UserName == "user@user" {
 log.Println("user@user exist...")
 return
 }
 log.Println("Creating user@user...")
 hashPwd, _ := pkg.HashPassword("password")
 _, err := dbQuery.CreateUsers(ctx,
 chapter5.CreateUsersParams{
 UserName: "user@user",
 PassWordHash: hashPwd,
 Name: "Dummy user",
 })
...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Creating our dummy user"*

---

### sqlc Query by Unique Field — `GetUserByName`  `#go`

**Principle:** Annotate the SQL with `-- name: GetUserByName :one` to generate a method that returns a single typed row; pass the named parameter via `QueryRowContext`.

**SQL constant:**
```go
const getUserByName = `-- name: GetUserByName :one
SELECT user_id, user_name, pass_word_hash, name, config, 
created_at, is_enabled
FROM gowebapp.users
WHERE user_name = $1
`
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / make generate"*

**Generated Go:**
```go
...
func (q *Queries) GetUserByName(ctx context.Context, userName 
string) (GowebappUser, error) {
 row := q.db.QueryRowContext(ctx, getUserByName, userName)
 var i GowebappUser
 err := row.Scan(
 &i.UserID,
 &i.UserName,
 &i.PasswordHash,
 &i.Name,
 &i.Config,
 &i.CreatedAt,
 &i.IsEnabled,
 )
 return i, err
}
...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / make generate"*

---

### Middleware — The `func(http.Handler) http.Handler` Pattern  `#go` `#api` `#architecture`

**Principle:** A middleware wraps the next handler: pre-process the request, call `h.ServeHTTP(wr, req)`, then optionally post-process. Gorilla Mux exposes `router.Use(...)` which stacks middleware in declaration order.

**Do:**
- Return `http.HandlerFunc(closure)` to satisfy the `http.Handler` interface.
- Use middleware for cross-cutting concerns: logging, auth, CORS, rate limiting, JSON enforcement.

**Don't:**
- Don't write per-handler boilerplate for cross-cutting concerns.

**Basic logging middleware:**
```go
func basicMiddleware(h http.Handler) http.Handler {
 return http.HandlerFunc(func(wr http.ResponseWriter,
 req *http.Request) {
 log.Println("Middleware called on", req.URL.Path)
 // do stuff
 h.ServeHTTP(wr, req)
 })
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Basic middleware"*

**`mux.MiddlewareFunc` signature:**
```go
func (*mux.Router).Use(mwf ...mux.MiddlewareFunc)
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Basic middleware"*

**Registration:**
```go
func main() {
 ...
 // Use our basicMiddleware
 router.Use(basicMiddleware)
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Basic middleware"*

---

### Cookie-Based Sessions with `gorilla/sessions`  `#go` `#web`

**Principle:** The web is stateless; `gorilla/sessions` overcomes this by associating requests with a server-side session keyed by a `session_token` cookie. `store.Get(r, name)` auto-creates a session if none exists.

**Do:**
- Track an `authenticated` boolean in `session.Values`.
- Call `session.Save(r, w)` after every mutation.

**Check session validity:**
```go
//sessionValid check whether the session is a valid session
func sessionValid(w http.ResponseWriter, r *http.Request) bool 
{
 session, _ := store.Get(r, "session_token")
 return !session.IsNew
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Cookies and session handling"*

**Check authentication flag:**
```go
func hasBeenAuthenticated(w http.ResponseWriter, r *http.
Request) bool {
 session, _ := store.Get(r, "session_token")
 a, _ := session.Values["authenticated"]
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Cookies and session handling"*

**Redirect when not authenticated:**
```go
//if it does have a valid session make sure it has been 
//authenticated
if hasBeenAuthenticated(w, r) {
 ...
}
//otherwise it will need to be redirected to /login
...
http.Redirect(w, r, "/login", 307)
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Cookies and session handling"*

**Persisting the flag:**
```go
func storeAuthenticated(w http.ResponseWriter, r *http.Request, 
v bool) {
 session, _ := store.Get(r, "session_token")
 session.Values["authenticated"] = v
 err := session.Save(r, w)
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Storing session information"*

---

### Redis-Backed Sessions  `#go` `#architecture`

**Principle:** In-memory sessions are lost on restart. Use `github.com/redis/go-redis` plus `github.com/rbcervilla/redisstore` to persist gorilla sessions in Redis with disk-backed durability.

**Initialization:**
```go
func initRedis() {
 var err error
 client = redis.NewClient(&redis.Options{
 Addr: "localhost:6379",
 })
 store, err = rstore.NewRedisStore(context.Background(), 
 client)
 if err != nil {
 log.Fatal("failed to create redis store: ", err)
 }
 store.KeyPrefix("session_token")
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Using Redis for a session"*

**Logout — set `MaxAge = -1` to invalidate:**
```go
func logoutHandler(w http.ResponseWriter, r *http.Request) {
 if hasBeenAuthenticated(w, r) {
 session, _ := store.Get(r, "session_token")
 session.Options.MaxAge = -1
 err := session.Save(r, w)
 if err != nil {
 log.Println("failed to delete session", err)
}
 }
 http.Redirect(w, r, "/login", 307)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 5 / Using Redis for a session"*

---

### API-First Server Abstraction  `#api` `#go` `#architecture`

**Principle:** Encapsulate the HTTP server in an `internal/api` package exposing `NewServer(port)`, `MustStart()`, `Stop()`, and `AddRoute(path, handler, method, middleware...)`. Compose middleware slices — default middleware plus protected-only middleware appended per route.

**Code:**
```go
 1 func main() {
 2 ...
 3 server := api.NewServer(internal.GetAsInt(
 4 "SERVER_PORT", 9002))
 5
 6 server.MustStart()
 7 defer server.Stop()
 8
 9 defaultMiddleware := []mux.MiddlewareFunc{
 10 api.JSONMiddleware,
 11 api.CORSMiddleware(internal.GetAsSlice(
 12 "CORS_WHITELIST",
 13 []string{
 14 "http://localhost:9000",
 15 "http://0.0.0.0:9000",
 16 }, ","),
 17 )
 18 }
 19
 20 // Handlers
 21 server.AddRoute("/login", handleLogin(db),
```
```go
 22 http.MethodPost, defaultMiddleware...)
 23 server.AddRoute("/logout", handleLogout(),
 24 http.MethodGet, defaultMiddleware...)
 25
 26 // Our session protected middleware
 27 protectedMiddleware :=
 28 append(defaultMiddleware,
 29 validCookieMiddleware(db))
 30 server.AddRoute("/checkSecret",
 31 checkSecret(db), http.MethodGet,
 32 protectedMiddleware...)
 33
 34 ...
 35 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Exposing our REST API"*

---

### JSON Enforcement Middleware  `#api` `#go`

**Principle:** Reject any request whose `Content-Type` is not `application/json` (HTTP 415), set the response `Content-Type` explicitly, and use `mime.ParseMediaType` to normalize header parsing.

**Code:**
```go
 1 func JSONMiddleware(next http.Handler)
 http.Handler {
 2 return http.HandlerFunc(func(wr
 http.ResponseWriter, req *http.Request) {
 3 contentType :=
 req.Header.Get("Content-Type")
 4
 5 if strings.TrimSpace(contentType) == "" {
 6 var parseError error
 7 contentType, _, parseError =
 8 mime.ParseMediaType(contentType)
 9 if parseError != nil {
 10 JSONError(wr,
 11 http.StatusBadRequest,
 12                 "Bad or no content-type header
 13 found")
 14 return
 15 }
 16 }
 17
 18 if contentType != "application/json" {
 19 JSONError(wr,
 20 http.StatusUnsupportedMediaType,
 21              "Content-Type not
 22 application/json")
 23 return
 24 }
 25 // Tell the client we're talking JSON as
 26 // well.
 27 wr.Header().Add("Content-Type",
```
```go
 28 "application/json")
 29 next.ServeHTTP(wr, req)
 30 })
 31 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / JSON middleware"*

---

### Session Validation Middleware  `#api` `#go`

**Principle:** Read the cookie store, type-assert `userID` and `userAuthenticated` from the session map, and on success inject a `UserSession` into the request context via `context.WithValue` so handlers can retrieve it through a typed key.

**Code:**
```go
 1 session, err := cookieStore.Get(req,
 2 "session-name")
 3 if err != nil {
 4 api.JSONError(wr,
 5 http.StatusInternalServerError,
 6              "Session Error")
 7 return
 8 }
 9
 10 userID, userIDOK :=
 11 session.Values["userID"].(int64)
 12 isAuthd, isAuthdOK :=
 13 session.Values["userAuthenticated"].(bool)
 14 if !userIDOK || !isAuthdOK {
 15 api.JSONError(wr,
 16 http.StatusInternalServerError,
 17 "Session Error")
 18 return
 19 }
 20
 21 if !isAuthd || userID < 1 {
 22 api.JSONError(wr, http.StatusForbidden,
 23 "Bad Credentials")
```
```go
 24 return
 25 }
 26 ...
 27 ctx := context.WithValue(req.Context(),
 28 SessionKey, UserSession{
 29 UserID: user.UserID,
 30 })
 31 h.ServeHTTP(wr, req.WithContext(ctx))
 32
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Session middleware"*

---

### JSON Request Models — Decode with Streaming  `#api` `#go`

**Principle:** Use `json.NewDecoder(req.Body).Decode(&payload)` instead of `json.Marshal`/`Unmarshal` — it streams through `io.Reader`/`io.Writer`, is chainable, and avoids preallocating byte buffers. Define request structs as local types inside the handler so the schema lives next to its use.

**Login handler:**
```go
func handleLogin(db *sql.DB) http.HandlerFunc {
 return http.HandlerFunc(func(wr http.ResponseWriter, req
 *http.Request) {
 type loginRequest struct {
 Username string `json:"username"`
 Password string `json:"password"`
 }
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining request model"*

**Decoding:**
```go
payload := loginRequest{}
if err := json.NewDecoder(req.Body).Decode(&payload); err != 
nil {
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining request model"*

**Larger request with omitempty tags:**
```go
 1 func handleAddSet(db *sql.DB) http.HandlerFunc {
 2 return http.HandlerFunc(func(wr
 3 http.ResponseWriter,
 4 req *http.Request) {
 5
 6 ...
 7
 8 type newSetRequest struct {
 9 ExerciseName string
10 `json:"exercise_name,omitempty"`
11 Weight int `json:"weight,omitempty"`
12 }
13
14 payload := newSetRequest{}
15 if err := json.NewDecoder(req.Body)
16 .Decode(&payload); err != nil {
17 ...
18 return
19 }
20
21 ...
22 })
23 }
24
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining request model"*

---

### JSON Response Models — Encode & Struct Tags  `#api` `#go`

**Principle:** sqlc-generated structs (with `json:` tags) double as API response bodies. Call `json.NewEncoder(wr).Encode(&set)` to stream the response.

**Code:**
```go
func handleAddSet(db *sql.DB) http.HandlerFunc {
 return http.HandlerFunc(func(wr http.ResponseWriter,
 req *http.Request) {
 ...
 set, err :=
 querier.CreateDefaultSetForExercise(req.Context(),
 store.CreateDefaultSetForExerciseParams{
 WorkoutID: int64(workoutID),
 ExerciseName: payload.ExerciseName,
 Weight: int32(payload.Weight),
 })
 ...
 json.NewEncoder(wr).Encode(&set)
 })
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining a response model"*

**The generated `GowebappSet` struct:**
```go
type GowebappSet struct {
 SetID int64 `json:"set_id"`
 WorkoutID int64 `json:"workout_id"`
 ExerciseName string `json:"exercise_name"`
 Weight int32 `json:"weight"`
 Set1 int64 `json:"set1"`
 Set2 int64 `json:"set2"`
 Set3 int64 `json:"set3"`
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining a response model"*

**Resulting JSON response:**
```json
{
 "set_id": 1,
 "workout_id": 1,
 "exercise_name": "Barbell",
 "weight": 700,
 "set1": 0,
 "set2": 0,
 "set3": 0
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Defining a response model"*

---

### Standardized JSON Error & Message Helpers  `#api` `#go`

**Principle:** Centralize error and success envelopes in `internal/api/wrappers.go`. `JSONError` writes the status code and a `{status, error}` or `{status, errors[]}` body depending on how many messages are passed. This guarantees every endpoint emits the same shape.

**Do:**
- Combine numeric code + HTTP status text: `fmt.Sprintf("%d / %s", code, http.StatusText(code))`.
- Avoid leaking internal details (DB connection errors, stack traces) to clients.

**Code:**
```go
 1 func JSONError(wr http.ResponseWriter,
 2 errorCode int, errorMessages ...string) {
 3 wr.WriteHeader(errorCode)
 4 if len(errorMessages) > 1 {
 5 json.NewEncoder(wr).Encode(struct {
 6 Status string `json:"status,omitempty"`
 7 Errors []string `json:"errors,omitempty"`
 8 }{
 9 Status: fmt.Sprintf("%d / %s", errorCode,
 10 http.StatusText(errorCode)),
 11 Errors: errorMessages,
 12 })
 13 return
 14 }
 15
 16 json.NewEncoder(wr).Encode(struct {
 17 Status string `json:"status,omitempty"`
 18 Error string `json:"error,omitempty"`
 19 }{
 20 Status: fmt.Sprintf("%d / %s", errorCode,
 21 http.StatusText(errorCode)),
 22 Error: errorMessages[0],
 23 })
 24 }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Using JSONError"*

**Typical error response (403):**
```json
{"status":"403 / Forbidden","error":"Bad Credentials"}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 6 / Using JSONError"*

---

### Backend Handlers for the Frontend Sample  `#api` `#go`

**Principle:** Keep demo handlers tiny — one for GET (fixed payload), one for POST (decodes a struct, encodes a transformed response).

**Code:**
```go
func appGET() http.HandlerFunc {
 type ResponseBody struct {
 Message string
 }
 return func(rw http.ResponseWriter, req *http.Request) {
 log.Println("GET", req)
 json.NewEncoder(rw).Encode(ResponseBody{
 Message: "Hello World",
 })
 }
}
func appPOST() http.HandlerFunc {
 type RequestBody struct {
 Inbound string
 }
 type ResponseBody struct {
 OutBound string
 }
 return func(rw http.ResponseWriter, req *http.Request) {
 log.Println("POST", req)
 var rb RequestBody
 if err := json.NewDecoder(req.Body).Decode(&rb);
 err != nil {
 log.Println("apiAdminPatchUser: Decode
 failed:", err)
 rw.WriteHeader(http.StatusBadRequest)
 return
 }
 log.Println("We received an inbound value of",
 rb.Inbound)
 json.NewEncoder(rw).Encode(ResponseBody{
 OutBound: stringutil.Reverse(rb.Inbound),
```
```go
 })
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Consuming your Golang APIs"*

---

### Axios Instance & `withCredentials`  `#web` `#general`

**Principle:** Build a shared Axios instance with a `baseURL` sourced from `import.meta.env.VITE_BASE_API_URL` and `withCredentials: true` so cookies flow on cross-origin requests.

**Code (`lib/api.js`):**
```javascript
import axios from 'axios';
// Create our "axios" object and export
// to the general namespace. This lets us call it as
// api.post(), api.get() etc
export default axios.create({
 baseURL: import.meta.env.VITE_BASE_API_URL,
 withCredentials: true,
});
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Consuming your Golang APIs"*

---

### CORS with `gorilla/handlers`  `#api` `#go` `#architecture`

**Principle:** Browsers send an OPTIONS preflight before cross-origin JSON POSTs; respond with `AllowedHeaders`, `AllowedOrigins`, `AllowedMethods`, and `AllowCredentials()`. Append `http.MethodOptions` to the POST route so the same handler answers the preflight.

**Do:**
- Drive origins/headers from environment variables in production (no hard-coded localhost).
- Include `Content-Type` in `AllowedHeaders` — without it, JSON requests are rejected.

**Code:**
```go
...
 port := ":8000"
 rtr := mux.NewRouter()
 rtr.Handle("/", appGET()).Methods(http.MethodGet)
 rtr.Handle("/", appPOST()).Methods(http.MethodPost,
 http.MethodOptions)
 // Apply the CORS middleware to our top-level router, with
 // the defaults.
 rtr.Use(
 handlers.CORS(
 handlers.AllowedHeaders(
 []string{"X-Requested-With", 
 "Origin", "Content-Type",}),
 handlers.AllowedOrigins([]string{
 "http://0.0.0.0:3000", 
 "http://localhost:3000"}),
 handlers.AllowCredentials(),
 handlers.AllowedMethods([]string{
 http.MethodGet,
 http.MethodPost,
 })),
 )
 log.Printf("Listening on http://0.0.0.0%s/", port)
 http.ListenAndServe(port, rtr)
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / CORS for secure applications"*

**Env-driven production variant:**
```go
rtr.Use(
 handlers.CORS(
 handlers.AllowedHeaders(
 env.GetAsSlice("ALLOWED_HEADERS")),
 handlers.AllowedOrigins(
 env.GetAsSlice("ORIGIN_WHITELIST")),
 handlers.AllowCredentials(),
 handlers.AllowedMethods([]string{
 http.MethodGet,
 http.MethodPost,
 })),
 )
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / CORS for secure applications"*

---

### Axios Transformers — snake_case ↔ camelCase  `#web` `#api`

**Principle:** When the backend speaks snake_case and the frontend speaks camelCase, transform payloads inside Axios via `transformRequest` (outbound → snake) and `transformResponse` (inbound → camel). Keeps both codebases idiomatic.

**Code (`lib/api.js` with transformers):**
```javascript
import axios from 'axios';
import camelCaseKeys from 'camelcase-keys';
import snakeCaseKeys from 'snakecase-keys';
function isObject(value) {
 return typeof value === 'object' && value instanceof
 Object;
}
export function transformSnakeCase(data) {
 if (isObject(data) || Array.isArray(data)) {
 return snakeCaseKeys(data, { deep: true });
 }
 if (typeof data === 'string') {
 try {
 const parsedString = JSON.parse(data);
 const snakeCase = snakeCaseKeys(parsedString, { deep:
 true });
 return JSON.stringify(snakeCase);
 } catch (error) {
 // Bailout with no modification
 return data;
 }
 }
 return data;
}
export function transformCamelCase(data) {
 if (isObject(data) || Array.isArray(data)) {
 return camelCaseKeys(data, { deep: true });
 }
 return data;
}
export default axios.create({
 baseURL: import.meta.env.VITE_BASE_API_URL,
 withCredentials: true,
 transformRequest: [...axios.defaults.transformRequest,
 transformSnakeCase],
 transformResponse: [...axios.defaults.transformResponse,
 transformCamelCase],
});
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Creating Vue middleware"*

---

### JWT — Custom Claims on Top of `StandardClaims`  `#api` `#go`

**Principle:** A JWT carries header + payload (claims) + signature. Embed `jwt.StandardClaims` in your own struct to add domain-specific claims while honoring the registered ones (`iss`, `sub`, `exp`, `iat`, `jti`, etc.).

**The library's `StandardClaims`:**
```go
// Structured version of Claims Section, as referenced at
// https://tools.ietf.org/html/rfc7519#section-4.1
type StandardClaims struct {
 Audience string `json:"aud,omitempty"`
 ExpiresAt int64 `json:"exp,omitempty"`
 Id string `json:"jti,omitempty"`
 IssuedAt int64 `json:"iat,omitempty"`
 Issuer string `json:"iss,omitempty"`
 NotBefore int64 `json:"nbf,omitempty"`
 Subject string `json:"sub,omitempty"`
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / What's a JWT?"*

**Custom claims + token creation:**
```go
 mySigningKey := []byte("PacktPub")
 // Your claims above and beyond the default
 type MyCustomClaims struct {
 Foo string `json:"foo"`
 jwt.StandardClaims
 }
 // Create the Claims
 claims := MyCustomClaims{
 "bar",
 // Note we embed the standard claims here
 jwt.StandardClaims{
 ExpiresAt: time.Now().Add(time.Minute *
 1).Unix(),
 Issuer: "FullStackGo",
 },
 }
 // Encode to token
 token := jwt.NewWithClaims(jwt.SigningMethodHS256,
 claims)
 tokenString, err := token.SignedString(mySigningKey)
 fmt.Printf("Your JWT as a string is %v\n", tokenString)
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / What's a JWT?"*

---

### JWT Gotchas — `none` Algorithm, Logout, Stale Data  `#api` `#go`

**Principle:** JWTs are self-contained, so attackers can decode one, swap `alg` to `"none"`, and strip the signature. Always verify the algorithm matches expectation. Logout doesn't truly invalidate a JWT until expiry, and stored claims go stale until the token is refreshed.

**The "none algorithm" attack in action:**
```bash
$ Pipe our encoded JWT through the base64 command to decode it
$ echo eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 | base64 -D
{"alg":"HS256","typ":"JWT"}
$ echo '{"alg":"none","typ":"JWT"}' | base64
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0K
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / The 'none algorithm' gotcha"*

---

### JWT Cookie Middleware  `#api` `#go`

**Principle:** Pull the `jwt-token` cookie, decode it to a user, return 401 with a JSON message on failure, and on success refresh the token (sliding expiration) and re-set the cookie before invoking `next.ServeHTTP`.

**Code:**
```go
// JWTProtectedMiddleware verifies a valid JWT exists in
// our cookie and if not, encourages the consumer to login
// again.
func JWTProtectedMiddleware(next http.Handler) http.Handler {
 return http.HandlerFunc(func(w http.ResponseWriter,
 r *http.Request) {
 // Grab jwt-token cookie
 jwtCookie, err := r.Cookie("jwt-token")
 if err != nil {
 log.Println("Error occurred reading cookie", err)
 w.WriteHeader(http.StatusUnauthorized)
 json.NewEncoder(w).Encode(struct {
 Message string `json:"message,omitempty"`
 }{
 Message: "Your session is not valid –
 please login",
 })
 return
 }
 // Decode and validate JWT if there is one
 userEmail, err := decodeJWTToUser(jwtCookie.Value)
 if userEmail == "" || err != nil {
 log.Println("Error decoding token", err)
 w.WriteHeader(http.StatusUnauthorized)
 json.NewEncoder(w).Encode(struct {
 Message string `json:"message,omitempty"`
 }{
```
```go
 Message: "Your session is not valid –
 please login",
 })
 return
 }
 // If it's good, update the expiry time
 freshToken := createJWTTokenForUser(userEmail)
 // Set the new cookie and continue into the handler
 w.Header().Add("Content-Type", "application/json")
 http.SetCookie(w, authCookie(freshToken))
 next.ServeHTTP(w, r)
 })
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / Setting cookies and validation middleware"*

---

### Secure Cookie Configuration  `#api` `#go` `#web`

**Principle:** Always set `HttpOnly: true` (blocks JS access — XSS mitigation), `Secure: true` (HTTPS only), and `SameSite: LaxMode` (CSRF mitigation). Drive domain and key from environment variables.

**Code:**
```go
var jwtSigningKey []byte
var defaultCookie http.Cookie
var jwtSessionLength time.Duration
var jwtSigningMethod = jwt.SigningMethodHS256
func init() {
 jwtSigningKey = []byte(env.GetAsString(
 "JWT_SIGNING_KEY", "PacktPub"))
 defaultSecureCookie = http.Cookie{
 HttpOnly: true,
 SameSite: http.SameSiteLaxMode,
 Domain: env.GetAsString("COOKIE_DOMAIN",
 "localhost"),
 Secure: env.GetAsBool("COOKIE_SECURE", true),
 }
 jwtSessionLength = time.Duration(env.GetAsInt(
 "JWT_SESSION_LENGTH", 5))
}
...
func authCookie(token string) *http.Cookie {
 d := defaultSecureCookie
 d.Name = "jwt-token"
 d.Value = token
 d.Path = "/"
 return &d
}
func expiredAuthCookie() *http.Cookie {
 d := defaultSecureCookie
 d.Name = "jwt-token"
 d.Value = ""
 d.Path = "/"
 d.MaxAge = -1
 // set our expiration to some date in the distant
 // past
 d.Expires = time.Date(1983, 7, 26, 20, 34, 58,
 651387237, time.UTC)
 return &d
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / Setting cookies and validation middleware"*

---

### Vue Router Navigation Guards  `#web`

**Principle:** `router.beforeEach(async (to, from) => …)` runs before every navigation. Return `false` to cancel, a route object to redirect, or `undefined`/`true` to allow. Use per-route `meta.requiresAuth` to mark protected pages and call a backend `/profile` (or any 20x endpoint) to verify the cookie still authenticates.

**Code (`checkAuth` factory):**
```javascript
export function getCheckLogin() {
 return api.get('/profile');
}
export default function checkAuth() {
 return async function checkAuthOrRedirect(to, from) {
 if (!to?.meta?.requiresAuth) {
 // non protected route, allow it
 return;
 }
 try {
 const { data } = await getCheckLogin();
 return;
 } catch (error) {
 return { name: 'Login'};
 }
 };
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / Navigation guards"*

**Installing the guard with meta flags:**
```javascript
...
const router = createRouter({
 history: createWebHistory(import.meta.env.BASE_URL),
 routes: [
{
 path: '/login',
 Name: 'Login',
 meta: {
 requiresAuth: false,
 },
 props: true,
 component: () => import('@/views/login.vue'),
 },{
 path: '/dashboard,
 Name: 'Dashboard',
 meta: {
 requiresAuth: true,
 },
 props: true,
 component: () => import('@/views/dashboard.vue'),
 }]
});
...
router.beforeEach(checkAuth());
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / Navigation guards"*

---

### Vue Router Catch-All 404  `#web`

**Principle:** Vue Router v4 uses a regexp pathMatch wildcard as the final route entry to render a NotFound component for unmatched paths.

**Code:**
```javascript
{ path: '/:pathMatch(.*)*', name: 'not-found', component: 
NotFound }
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 10 / Defaults and error pages"*

---

### Feature Flag Server — REST API  `#api` `#architecture`

**Principle:** Feature flags decouple deploy from release — toggles can target user segments, gate microservices, or control UI. Run a small REST server (`github.com/nanikjava/feature-flags`) exposing `POST /features`, `PATCH /features/{key}`, `GET /features/{key}`.

**Flag payload shape:**
```json
{
 "key": "disable_get",
 "enabled": false,
 "users": [],
 "groups": [
 "dev",
 "admin"
 ],
 "percentage": 0
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Installing the feature flag server"*

**Creating a flag:**
```bash
curl -v -X POST http://localhost:8080/features -H "Content-
Type:
application/json" -d '{"key":"disable_get","enabled":false,
"users":[],"groups":["dev","admin"],"percentage":0}'
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Installing the feature flag server"*

**Patching a flag:**
```bash
curl -v -X PATCH http://localhost:8080/features/disable_get 
-H "Content-Type: application/json" -d '{"key":"disable_
get","enabled":true}'
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Web application"*

---

### Feature Flag — Backend Microservice Integration  `#go` `#architecture`

**Principle:** On server startup, fire goroutines to fetch each downstream service's flag from the feature-flag server; cache the booleans; handlers then conditionally call downstream services and stitch the responses together.

**Startup fetches flags concurrently:**
```go
...
func main() {
 port := ":8000"
 ...
 wg := &sync.WaitGroup{}
 wg.Add(1)
 go func(w *sync.WaitGroup) {
 defer w.Done()
 serviceA = checkFlags("servicea")
 serviceB = checkFlags("serviceb")
 }(wg)
 wg.Wait()
 http.ListenAndServe(port, rtr)
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Microservice integration"*

**Handler merges responses from enabled services:**
```go
func handler() http.HandlerFunc {
 type ResponseBody struct {
 Message string
 }
 return func(rw http.ResponseWriter, req *http.Request) {
 var a, b string
 if serviceA {
 a = callService("8081")
 }
 if serviceB {
 b = callService("8082")
 }
```
```go
 json.NewEncoder(rw).Encode(ResponseBody{
 Message: a + "-" + b,
 })
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Microservice integration"*

**Flag lookup — HTTP GET + JSON unmarshal:**
```go
func checkFlags(key string) bool {
 ...
 requestURL := fmt.Sprintf("http://localhost:%d/features/%s",
 8080, key)
 res, err := http.Get(requestURL)
 ...
 resBody, err := ioutil.ReadAll(res.Body)
 if err != nil {
 log.Printf("client: could not read response body: %s\n",
 err)
 os.Exit(1)
 }
 ...
 return f.Enabled
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Microservice integration"*

**Typed response struct:**
```go
func checkFlags(key string) bool {
 type FeatureFlagServerResponse struct {
 Enabled bool `json:"enabled"`
 }
 ...
 var f FeatureFlagServerResponse
 err = json.Unmarshal(resBody, &f)
 ...
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Microservice integration"*

**Return just the boolean:**
```go
func checkFlags(key string) bool {
 ...
 return f.Enabled
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Microservice integration"*

---

### Feature Flag — Frontend UI Toggle  `#web`

**Principle:** In the `mounted()` lifecycle hook, fetch the flag and bind its `enabled` value to `v-if` on the UI element.

**Code:**
```javascript
...
<script>
import axios from 'axios';
export default {
 data() {
 return {
 enabled: true
 }
 },
 mounted() {
 axios({method: "GET", "url":
 "http://localhost:8080/features/disable_get"}).then(result
 => {
 this.enabled = result.data.enabled
 console.log(result);
 }, error => {
 console.error(error);
 });
 }
}
</script>
<template>
 <div v-if="enabled" class="flex space-2 justify-center">
 ...
 </button>
 </div>
 ...
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 11 / Web application"*

---

### GitHub Actions Workflow — Lint + Build  `#general` `#architecture`

**Principle:** Put YAML under `.github/workflows/`. Trigger on push to `main` and on PRs. Run lint and build jobs on `ubuntu-latest`; gate `build` on `lint` via `needs: [lint]`.

**Code (`.github/workflows/build.yml`):**
```yaml
name: Build and Package
on:
 push:
 branches:
 - main
 pull_request:
jobs:
 lint:
 name: Lint
 runs-on: ubuntu-latest
 steps:
 - name: Set up Go
 uses: actions/setup-go@v1
 with:
 go-version: 1.18
 - name: Check out code
 uses: actions/checkout@v1
 - name: Lint Go Code
 run: |
```
```yaml
 curl -sSfL 
 https://raw.githubusercontent.com/golangci/golangci-
lint/
 master/install.sh | sh -s -- -b $(go env GOPATH)/bin
 $(go env GOPATH)/bin/golangci-lint run
 build:
 name: Build
 runs-on: ubuntu-latest
 needs: [ lint ]
 steps:
 - name: Set up Go
 uses: actions/setup-go@v1
 with:
 go-version: 1.18
 - name: Check out code
 uses: actions/checkout@v1
 - name: Build
 run: make build
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 12 / GitHub Actions"*

---

### Multi-Stage Dockerfile  `#general` `#architecture`

**Principle:** Two `FROM` stages — `golang:1.18 as builder` for compilation, `alpine:latest` for runtime — produce ~17 MB images versus ~964 MB for the full Go image. `CGO_ENABLED=0 GOOS=linux` produces a static binary.

**Code:**
```dockerfile
# 1. Compile the app.
FROM golang:1.18 as builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -o bin/embed
# 2. Create final environment for the compiled binary.
FROM alpine:latest
RUN apk --update upgrade && apk --no-cache add curl 
ca-certificates && rm -rf /var/cache/apk/*
RUN mkdir -p /app
# 3. Copy the binary from step 1 and set it as the default 
# command.
COPY --from=builder /app/bin/embed /app
WORKDIR /app
CMD /app/embed
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 12 / Dockerfile"*

---

### Publishing Images to GitHub Packages (ghcr.io)  `#general` `#architecture`

**Principle:** Use `docker/login-action@v2` with `${{ secrets.GITHUB_TOKEN }}` to authenticate to `ghcr.io`, then `docker/build-push-action@v3` to build and push. Tag as `ghcr.io/{owner}/{repo}/{name}:latest`.

**Code (`.github/workflows/builddocker.yml`):**
```yaml
name: Build Docker Image
on:
 push:
 branches:
 - main
 pull_request:
env:
 REGISTRY: ghcr.io
 IMAGE_NAME: ${{ github.repository }}
jobs:
 push_to_github_registry:
 name: Push Docker image to Docker Hub
 runs-on: ubuntu-latest
 steps:
 ...
 - name: Log in to the Container registry
 uses: docker/login-action@v2
 with:
 registry: ${{ env.REGISTRY }}
```
```yaml
 username: ${{ github.actor }}
 password: ${{ secrets.GITHUB_TOKEN }}
 - name: Build and push Docker image
 uses: docker/build-push-action@v3
 with:
 context: .
 file: ./Dockerfile
 push: true
 tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME 
 }}/chapter12:latest
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 12 / Publishing to GitHub Packages"*

---

### Docker Compose — Multi-Service Local Stack  `#general` `#architecture`

**Principle:** Define multi-container stacks (app + Redis + DB) in one `compose.yaml`. Networking is automatic; volumes persist data.

**Code:**
```yaml
version: '3'
services:
 server:
 build: .
 ports:
 - "3333:3333"
 cache:z
 image: redis:7.0.4-alpine
 restart: always
 ports:
 - '6379:6379'
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 13 / Docker Compose"*

---

### docker-compose for Observability Stack  `#general` `#architecture`

**Principle:** Bundle Jaeger + Prometheus in one compose file so traces and metrics share networking.

**Code:**
```yaml
version: '3.3'
services:
 jaeger:
 image: jaegertracing/all-in-one:latest
 ports:
 - "6831:6831/udp"
```
```yaml
 - "16686:16686"
 - "14268:14268"
 prometheus:
 image: prom/prometheus:latest
 volumes:
 -./prom/opentelem/config.yml:/etc/prometheus/
 prometheus.yml
 command:
 - '--config.file=/etc/prometheus/prometheus.yml'
 - '--web.console.libraries=/usr/share/prometheus/
 console_libraries'
 - '--web.console.templates=/usr/share/prometheus/
 consoles›
 ports:
 - 9090:9090
 network_mode: "host"
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 3 / Running docker-compose"*

---

### Terraform — Local Docker Provider Example  `#general` `#architecture`

**Principle:** Infrastructure-as-Code lets you declare, plan, and apply infrastructure repeatably. The `kreuzwerker/docker` provider manages Docker images and containers via Terraform.

**Code (`main.tf`):**
```hcl
terraform {
 required_providers {
 docker = {
 source = "kreuzwerker/docker"
 version = "~> 2.16.0"
 }
 }
}
resource "docker_image" "nginx" {
 name = "nginx:latest"
 keep_locally = false
}
resource "docker_container" "nginx" {
 image = docker_image.nginx.name
 name = "hello-terraform"
```
```hcl
 ports {
 internal = 80
 external = 8000
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / Providers"*

---

### Terraform — AWS EC2 with VPC + Subnet  `#general` `#architecture`

**Principle:** Pass AWS credentials as Terraform variables; declare VPC, subnet, then EC2 instance referencing the subnet ID.

**Variables & provider:**
```hcl
terraform {
 ...
}
variable "aws_access_key" {
 type = string
}
variable "aws_secret_key" {
 type = string
}
provider "aws" {
 region = "us-east-1"
 access_key = var.aws_access_key
 secret_key = var.aws_secret_key
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / AWS EC2 setup"*

**VPC + subnet:**
```hcl
resource "aws_vpc" "default-vpc" {
 cidr_block = "10.0.0.0/16"
 enable_dns_hostnames = true
 tags = {
 env = "dev"
 }
}
resource "aws_subnet" "default-subnet" {
 cidr_block = "10.0.0.0/24"
 vpc_id = aws_vpc.default-vpc.id
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / AWS EC2 setup"*

**EC2 instance:**
```hcl
resource "aws_instance" "app_server" {
 ami = "ami-0ff8a91507f77f867"
 instance_type = "t2.nano"
 subnet_id = aws_subnet.default-subnet.id
 tags = {
 Name = "Chapter14"
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / AWS EC2 setup"*

---

### Terraform — ECS + Load Balancer  `#general` `#architecture`

**Principle:** Internet gateway enables VPC-to-internet; security groups gate traffic (TCP 80–3333); two subnets are required for the ALB; the ECS task definition references the `ghcr.io` image; Fargate launch type removes EC2 management.

**Internet gateway & routes:**
```hcl
resource "aws_internet_gateway" "lbecs-igw" {
 vpc_id = aws_vpc.lbecs-vpc.id
 tags = {
```
```hcl
 Name = "Internet Gateway"
 }
}
resource "aws_default_route_table" "lbecs-subnet-default-route-
table" {
 default_route_table_id =
 aws_vpc.lbecs-vpc.default_route_table_id
 route {
 cidr_block = "0.0.0.0/0"
 gateway_id = "${aws_internet_gateway.lbecs-igw.id}"
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / Deploying to ECS with a load balancer"*

**Security group:**
```hcl
resource "aws_security_group" "lbecs-security-group" {
 name = "allow_http"
 description = "Allow HTTP inbound traffic"
 vpc_id = aws_vpc.lbecs-vpc.id
 egress {
 from_port = 0
 to_port = 0
 protocol = "-1"
 cidr_blocks = ["0.0.0.0/0"]
 }
 ingress {
 description = "Allow HTTP for all"
 from_port = 80
 to_port = 3333
 protocol = "tcp"
```
```hcl
 cidr_blocks = ["0.0.0.0/0"]
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / Deploying to ECS with a load balancer"*

**Load balancer:**
```hcl
resource "aws_lb" "lbecs-load-balancer" {
 name = "load-balancer"
 internal = false
 load_balancer_type = "application"
 security_groups = [aws_security_group.lbecs-security-group.
 id]
 subnets = [aws_subnet.lbecs-subnet.id,
 aws_subnet.lbecs-subnet-1.id]
 tags = {
 env = "dev"
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / Deploying to ECS with a load balancer"*

**ECS cluster, task definition, and service:**
```hcl
resource "aws_ecs_cluster" "lbecs-ecs-cluster" {
 name = "lbecs-ecs-cluster"
}
resource "aws_ecs_task_definition" "lbecs-ecs-task-definition" 
{
 family = "service"
 requires_compatibilities = ["FARGATE"]
 network_mode = "awsvpc"
 cpu = 1024
 memory = 2048
 container_definitions = jsonencode([
 {
 name = "lbecs-ecs-cluster-chapter14"
 image =
```
```hcl
 "ghcr.io/nanikjava/golangci/chapter12:latest"
 ...
 portMappings = [
 {
 containerPort = 3333
 }
 ]
 }
 ])
}
resource "aws_ecs_service" "lbecs-ecs-service" {
 name = "lbecs-ecs-service"
 cluster = aws_ecs_cluster.lbecs-ecs-cluster.id
 task_definition =
 aws_ecs_task_definition.lbecs-ecs-task-definition.arn
 desired_count = 1
 launch_type = "FARGATE"
 network_configuration {
 ...
 }
 load_balancer {
 target_group_arn = aws_lb_target_group.lbecs-load-
 balancer-target-group.arn
 container_name = "lbecs-ecs-cluster-chapter14"
 container_port = 3333
 }
 tags = {
 env = "dev"
 }
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 14 / Deploying to ECS with a load balancer"*

---

### Vue SFC Anatomy (Options API)  `#web`

**Principle:** A Vue Single-File Component splits cleanly into `<template>`, `<script>`, and `<style scoped>`. The Options API exposes `data()`, `methods`, `mounted()`, `props`, and `components`.

**Code (`Greeter.vue`):**
```vue
<template>
 <div>
 <Thing @click="greetLog" />
 <p class="greeting">{{ greeting }}</p>
 </div>
</template>
<script>
import Thing from '@/components/thing.vue';
export default {
 name: 'Greeter',
 components: ['Thing'],
 props:{},
 mounted(){},
 methods: {
 greetLog() { console.log('Greeter') };
 },
 data() {
 return {
 greeting: 'Hello World!'
 }
 }
}
</script>
```
```vue
<style scoped>
.greeting {
 color: red;
 font-weight: bold;
}
</style>
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 7 / Vue — Example of a SFC Greeter.vue"*

---

### Vite + Vue 3 Bootstrap  `#web`

**Principle:** `main.js` creates the app from `App.vue` and mounts to `#app`. The `<script setup>` Composition API tag imports child components inline.

**Code (`main.js`):**
```javascript
import { createApp } from 'vue'
import App from './App.vue'
createApp(App).mount('#app')
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 7 / Using Vite"*

**`App.vue` (Composition API):**
```vue
<script setup>
import Login from './components/Login.vue'
</script>
<template>
 <Login />
</template>
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 7 / Using Vite"*

---

### Vue Router Static Routes  `#web`

**Principle:** `createRouter({ history, routes })` ties paths to components. Use `createWebHashHistory()` for hash-based routing on static hosts; `<router-link>` triggers navigation; `<router-view>` renders the matched component.

**Code (`router/index.js`):**
```javascript
import Vue from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue';
import Login from "../views/Login.vue";
Vue.use(VueRouter);
const routes = [
```
```javascript
 {
 path: '/',
 name: 'Home',
 component: Home
 },
 {
 path: '/login',
 name: 'Login',
 component: Login
 },
];
const router = createRouter({
 history: createWebHashHistory(),
 base: process.env.BASE_URL,
 routes
})
export default router
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 7 / Using Vue Router to move around"*

---

### Vite Path Alias `@`  `#web`

**Principle:** Configure `@` as an alias for `src/` in `vite.config.js` to eliminate `../../` import chains.

**Code (`vite.config.js`):**
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';
// https://vitejs.dev/config/
export default defineConfig({
 plugins: [vue()],
 // Add the '@' resolver
 resolve: {
 alias: {
 '@': path.resolve(__dirname, 'src'),
 },
 },
})
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Consuming your Golang APIs"*

---

### Tailwind CSS Bootstrap  `#web`

**Principle:** Install `tailwindcss postcss autoprefixer`; run `npx tailwindcss init -p` to scaffold config; declare content paths so the JIT compiler emits only the classes you use.

**Config:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
 content: [
 "./index.html",
 "./src/**/*.{vue,js}",
 ],
 theme: {
 extend: {},
 },
 plugins: [],
}
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Creating a new Tailwind and Vite project"*

**CSS entry (`src/tailwind.css`):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
*Ref: Full-Stack_Web_Development_with_Go.md — "Chapter 9 / Creating a new Tailwind and Vite project"*

---

## Anti-Patterns & Common Mistakes

- **Using `http.DefaultServeMux` in production:** exposes debug endpoints you didn't intend to ship → *fix:* always construct `http.NewServeMux()`.
- **Storing plaintext passwords:** catastrophic if the DB leaks → *fix:* `bcrypt.GenerateFromPassword` at cost ≥ 12.
- **Skipping `db.Ping()` after `sql.Open`:** open is lazy; connectivity errors surface later → *fix:* always ping before serving traffic.
- **Reading `req.Body` twice:** it's an `io.ReadCloser`; the second read is empty → *fix:* buffer with `ioutil.ReadAll` and reuse the bytes.
- **In-memory session store with no persistence:** restart logs everyone out → *fix:* back `gorilla/sessions` with Redis (`redisstore`) or use JWTs.
- **CORS `Access-Control-Allow-Origin: *` with credentials:** browsers reject it → *fix:* enumerate explicit origins via env vars.
- **Hand-editing sqlc-generated code:** regenerated on the next `make generate` and your edits vanish → *fix:* extend via wrappers in non-generated packages.
- **Mixing JSON tag conventions:** frontend camelCase vs backend snake_case breaks the contract silently → *fix:* centralize via Axios transformers or pick one style project-wide.
- **Accepting `"none"` JWT algorithm:** trivial attack that strips signatures → *fix:* verify `alg` matches what you signed with.
- **Logging internal error details to clients:** leaks DB topology and credentials → *fix:* use the `JSONError` envelope and log details server-side only.
- **No `ReadTimeout` / `WriteTimeout` on `http.Server`:** slowloris-style resource exhaustion → *fix:* set both, plus `MaxHeaderBytes`.
- **Setting JWT cookies without `HttpOnly` / `Secure` / `SameSite`:** XSS and CSRF exposure → *fix:* enable all three flags by default.
- **Frontend-only validation:** trivially bypassed by curl/Postman → *fix:* validate again on the backend.
- **Committing AWS access keys into Terraform source:** leaks credentials via git history → *fix:* pass as `-var` from env/secret store.
- **Forgetting `terraform destroy` on AWS examples:** surprise bills → *fix:* always destroy after experiments.

---

## Decision Heuristics / Checklists

### When to use sqlc vs GORM vs database/sql
- **sqlc** — SQL-first, type-safe, no runtime reflection. Best when SQL is the source of truth and you have a static schema.
- **GORM** — auto-migrations, associations, hooks. Best for fast-changing schemas where you'd rather think in structs.
- **database/sql + hand-written code** — only when you need maximum control or sqlc can't express a query.

### When to use JWT vs Cookie Sessions
- Use **cookie sessions (Redis-backed)** when you need real logout, ban lists, and per-request DB/state checks are cheap.
- Use **JWT** when you want stateless validation across services and can tolerate eventual consistency on permissions (refresh-token rotation mitigates stale-claim windows).

### CORS checklist
- [ ] Origin allowed list sourced from env, not hard-coded.
- [ ] `Content-Type` included in `AllowedHeaders`.
- [ ] `AllowCredentials()` enabled iff cookies are sent.
- [ ] `http.MethodOptions` handled on every non-GET route.
- [ ] Preflight cache lifetime tuned via `Access-Control-Max-Age`.

### Embed checklist
- [ ] Directives placed immediately above the variable (no blank line).
- [ ] Variable typed as `string`, `[]byte`, or `embed.FS`.
- [ ] `fs.Sub` strips directory prefix before passing to `http.FileServer(http.FS(...))`.
- [ ] Templates rendered via `template.ParseFS`, not `ParseFiles`.

### Middleware ordering (outermost → innermost)
1. Recovery / panic capture
2. Request logging / tracing (OpenTelemetry span start)
3. CORS
4. JSON enforcement
5. Auth / session / JWT
6. Rate limiting
7. Business handler

### Production readiness
- [ ] Lint + build pipeline on every push
- [ ] Multi-stage Dockerfile, `CGO_ENABLED=0`
- [ ] Image published to registry (ghcr.io)
- [ ] Health endpoint
- [ ] Metrics endpoint scraped by Prometheus
- [ ] Traces exported to Jaeger
- [ ] Structured leveled logs
- [ ] Graceful shutdown on SIGTERM
- [ ] Infrastructure codified in Terraform
- [ ] `terraform plan` review before apply

---

## Key Takeaways

1. **SQL/Go separation via sqlc:** write SQL, get typed Go — no ORM leakage, no boilerplate.
2. **Observability from day one:** golog (leveled), OpenTelemetry (traces), Prometheus (metrics) — all vendor-agnostic.
3. **`//go:embed` ships a single binary:** HTML, CSS, JS, and version strings inlined at compile time.
4. **Middleware is the cross-cutting lever:** JSON enforcement, CORS, auth, sessions — all `func(http.Handler) http.Handler`.
5. **bcrypt for passwords, JWT for stateless auth, Redis for sessions:** pick the right tool per layer.
6. **Cookie hardening:** always `HttpOnly` + `Secure` + `SameSite=Lax`.
7. **JSON envelopes matter:** `JSONError` and `JSONMessage` standardize client contracts.
8. **CORS is not optional for split origins:** configure headers, methods, and credentials explicitly via env vars.
9. **Feature flags decouple deploy from release:** toggle UI and route to microservices per flag state.
10. **CI/CD on GitHub Actions:** lint → build → multi-stage Docker → ghcr.io.
11. **Terraform for IaC:** plan, apply, destroy — versioned infrastructure alongside application code.
12. **Axios transformers bridge schema mismatches:** snake_case ↔ camelCase without rewriting either side.
13. **Vue Router navigation guards enforce client-side auth:** `meta.requiresAuth` + `router.beforeEach` redirect unauthenticated users.
14. **Always set `http.Server` timeouts:** slowloris protection is one struct field away.

---

## Cross-References
- Related: [[../summaries/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram.md]]
- Source book: `markdown_output/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram.md`
- Topic index: [[../INDEX.md]]
