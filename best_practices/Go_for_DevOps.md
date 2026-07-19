# Go for DevOps
**Author:** John Doak & David Justice (Packt, 2022)
**Topic tags:** `#general` `#go` `#cli` `#systems` `#devops` `#cloud` `#architecture`
**Language focus:** Go-first (DevOps tooling, infra automation, K8s, cloud SDKs)
**Sources:** `markdown_output/Go_for_DevOps_-_John_Doak_David_Justice/Go_for_DevOps_-_John_Doak_David_Justice.md` · `summaries/Go_for_DevOps_-_John_Doak_David_Justice.md`

## TL;DR
A practitioner's roadmap from Go language essentials to production DevOps tooling: filesystem/IPC, REST + gRPC, SSH/exec automation, OpenTelemetry observability, GitHub Actions, ChatOps, Packer/Terraform IaC, `client-go` Kubernetes programming, Azure SDK, and chaos-resistant workflow design. The recurring thesis: **standardize on Go + gRPC, abstract storage behind interfaces, design every workflow to be idempotent, rate-limited, and emergency-stoppable** — because the spectacular cloud outages (AWS, Google satellite disk erase) were caused by infrastructure tooling, not user code.

---

## Best Practices by Topic

### Go Foundations — Idiomatic Building Blocks

**Principle:** Go's static typing, multiple-return error handling, goroutines, and `context.Context` are the foundation that makes cloud tooling reliable.

**Do:**
- Treat errors as values: return them as the last return value, wrap with `%w`, inspect with `errors.Is` / `errors.As`.
- Always thread `ctx context.Context` as the first argument through I/O call chains.
- Use `:=` inside functions, `var` at package level; remember declared variables must be used.
- Prefer pointer receivers consistently for a type — never mix pointer and value receivers.
- Use `defer` for cleanup (file close, mutex unlock, `wg.Done()`).

**Don't:**
- Use `panic` outside `main`; reserve it for unrecoverable startup failures.
- Reach for `recover` except at RPC framework boundaries (gRPC uses it to keep servers alive).
- Reuse `iota` enumerations across persisted versions — values shift if entries are inserted.
- Shadow loop variables in goroutines: copy with `x := x` before `go func(){ ... x ... }()`.

**Code:**
```go
// Idiomatic error wrapping — preserves the chain for errors.Is/As.
func restCall(data string) error {
    if err := someFunc(data); err != nil {
        return fmt.Errorf("restCall(%s) had an error: %w", data, err)
    }
    return nil
}

// Caller unwraps the chain to detect a specific sentinel.
var netErr ErrNetwork
if errors.As(err, &netErr) {
    if netErr.Code == AuthFailureCode {
        log.Println("unrecoverable auth failure: ", err)
        break
    }
}
```
*Ref: Go_for_DevOps.md — "Wrapping errors" / "Using an error"*

---

```go
// Named errors + retry-on-network-error loop.
var (
    ErrNetwork = errors.New("network error")
    ErrInput   = errors.New("input error")
)

for {
    err := someFunc("data")
    if err == nil {
        break
    }
    if errors.Is(err, ErrNetwork) {
        log.Println("recoverable network error")
        time.Sleep(1 * time.Second)
        continue
    }
    log.Println("unrecoverable error")
    break
}
```
*Ref: Go_for_DevOps.md — "Creating named errors"*

---

```go
// Context that propagates cancellation and per-call deadlines.
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
data, err := GatherData(ctx, args)
if err != nil {
    return err
}

// Honoring context inside a function.
func GatherData(ctx context.Context, args Args) ([]file, error) {
    if ctx.Err() != nil {
        return nil, ctx.Err()
    }
    localCtx, localCancel := context.WithTimeout(ctx, 2*time.Second)
    local, err := getFilesLocal(localCtx, args.local)
    localCancel()
    if err != nil {
        return nil, err
    }
    return local, nil
}
```
*Ref: Go_for_DevOps.md — "Using a Context to signal a timeout" / "Honoring a context when receiving"*

---

```go
// WaitGroup + goroutine lifecycle — never call Add() inside the goroutine.
func main() {
    wg := sync.WaitGroup{}
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            fmt.Println(n)
        }(i)
    }
    wg.Wait()
}
```
*Ref: Go_for_DevOps.md — "WaitGroups"*

---

```go
// Channels as exit signals: close(exit) causes <-exit to return immediately.
func printWords(in1, in2 chan string, exit chan struct{}, wg *sync.WaitGroup) {
    defer wg.Done()
    for {
        select {
        case <-exit:
            fmt.Println("exiting")
            return
        case str := <-in1:
            fmt.Println("in1: ", str)
        case str := <-in2:
            fmt.Println("in2: ", str)
        }
    }
}
```
*Ref: Go_for_DevOps.md — "Channels as an event signal"*

---

```go
// Table-driven tests are the idiomatic Go testing pattern.
func TestGreet(t *testing.T) {
    tests := []struct {
        desc      string
        name      string
        want      string
        expectErr bool
    }{
        {desc: "Error: name is an empty string", expectErr: true},
        {desc: "Success", name: "John", want: "Hello John"},
    }
    for _, test := range tests {
        got, err := Greet(test.name)
        switch {
        case err == nil && test.expectErr:
            t.Errorf("TestGreet(%s): got err == nil, want err != nil", test.desc)
            continue
        case err != nil && !test.expectErr:
            t.Errorf("TestGreet(%s): got err == %s, want err == nil", test.desc, err)
            continue
        case err != nil:
            continue
        }
        if got != test.want {
            t.Errorf("TestGreet(%s): got result %q, want %q", test.desc, got, test.want)
        }
    }
}
```
*Ref: Go_for_DevOps.md — "Table Driven Tests (TDT)"*

---

```go
// Hermetic tests via interfaces + fakes: define the interface your code needs,
// then inject a fake in tests instead of hitting real services.
type recorder interface {
    Record(name string) (Record, error)
}

func Greeter(name string, fetch recorder) (string, error) {
    rec, err := fetch.Record(name)
    if err != nil {
        return "", err
    }
    return fmt.Sprintf("Greetings %s", name), nil
}

type fakeRecorder struct {
    data Record
    err  bool
}

func (f fakeRecorder) Record(name string) (Record, error) {
    if f.err {
        return Record{}, errors.New("error")
    }
    return f.data, nil
}
```
*Ref: Go_for_DevOps.md — "Creating fakes with interfaces"*

---

```go
// Generics — use only when the only thing varying is the type (Ian Taylor's rule).
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
        ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
        ~float32 | ~float64 |
        ~string
}

func sortSlice[O Ordered](slice []O) { /* ... */ }

func ExtractMapKeys[K comparable, V any](m map[K]V) []K {
    keys := make([]K, 0, len(m))
    for k := range m {
        keys = append(keys, k)
    }
    return keys
}
```
*Ref: Go_for_DevOps.md — "Generics" / "Current built-in constraints"*

---

### Filesystem Interactions (Chapter 4)

**Principle:** Everything in Go I/O is a `Reader`/`Writer` — disk files, HTTP bodies, network sockets, STDIN/STDOUT all share one abstraction.

**Do:**
- Stream large files with `bufio.Scanner` / `io.Copy` to avoid loading them into memory.
- Use `filepath.Join` for OS-agnostic paths; use `os.TempDir()` for scratch space.
- Embed static assets via `//go:embed` so binaries are self-contained.
- Open files with `os.OpenFile(..., flags, perm)` and always `defer f.Close()`.

**Don't:**
- Read entire remote files into memory when streaming suffices.
- Hard-code path separators — `path/filepath` abstracts them.

**Code:**
```go
// Core io interfaces that everything implements.
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Seeker interface { Seek(offset int64, whence int) (int64, error) }
type Closer interface { Close() error }
```
*Ref: Go_for_DevOps.md — "All I/O in Go are files"*

---

```go
// Reading/writing local files.
data, err := os.ReadFile("path/to/file")
if err != nil {
    return err
}
s := string(data) // []byte -> string

if err := os.WriteFile("path/to/file", data, 0644); err != nil {
    return err
}
```
*Ref: Go_for_DevOps.md — "Reading local files" / "Writing local files"*

---

```go
// Stream an HTTP body directly to disk without buffering the whole response.
client := &http.Client{}
req, err := http.NewRequest("GET", "http://myserver.mydomain/myfile", nil)
if err != nil {
    return err
}
req = req.WithContext(ctx)
resp, err := client.Do(req)
if err != nil {
    return err
}

flags := os.O_CREATE | os.O_WRONLY | os.O_TRUNC
f, err := os.OpenFile("path/to/file", flags, 0644)
if err != nil {
    return err
}
defer f.Close()
if err := io.Copy(f, resp.Body); err != nil {
    return err
}
```
*Ref: Go_for_DevOps.md — "Reading remote files"*

---

```go
// Streaming a file line-by-line on a channel, with context cancellation.
func decodeUsers(ctx context.Context, r io.Reader) chan User {
    ch := make(chan User, 1)
    go func() {
        defer close(ch)
        scanner := bufio.NewScanner(r)
        for scanner.Scan() {
            if ctx.Err() != nil {
                ch <- User{err: ctx.Err()}
                return
            }
            u, err := getUser(scanner.Text())
            if err != nil {
                u.err = err
                ch <- u
                return
            }
            ch <- u
        }
    }()
    return ch
}
```
*Ref: Go_for_DevOps.md — "Reading data out of a stream"*

---

```go
// OS-agnostic pathing — works on Linux, macOS, and Windows.
wd, err := os.Getwd()
if err != nil {
    return err
}
content, err := os.ReadFile(filepath.Join(wd, "config", "config.json"))

// Copy a file to the OS TMPDIR while preserving its base name.
fileName := filepath.Base(fp)
newPath := filepath.Join(os.TempDir(), fileName)
r, err := os.Open(fp)
if err != nil {
    return err
}
defer r.Close()
w, err := os.OpenFile(newPath, os.O_WRONLY|os.O_CREATE, 0644)
if err != nil {
    return err
}
defer w.Close()
_, err = io.Copy(w, r)
```
*Ref: Go_for_DevOps.md — "OS-agnostic pathing"*

---

```go
// embed: ship static assets inside the binary.
import _ "embed"

//go:embed hello.txt
var s string

//go:embed world.txt
var b []byte

//go:embed image/*
//go:embed index.html
var content embed.FS
```
*Ref: Go_for_DevOps.md — "embed"*

---

```go
// io/fs: walk any FS (including embed.FS) the same way.
err := fs.WalkDir(
    content,
    ".",
    func(path string, d fs.DirEntry, err error) error {
        if err != nil {
            return err
        }
        if !d.IsDir() && filepath.Ext(path) == ".jpg" {
            fmt.Println("jpeg file: ", path)
        }
        return nil
    },
)
```
*Ref: Go_for_DevOps.md — "Walking our filesystem"*

---

### Common Data Formats (Chapter 5)

**Principle:** Struct field tags (`json:`, `yaml:`) drive marshaling. Stream large data sets with `json.Decoder`/`csv.Reader` rather than loading everything into memory.

**Do:**
- Use `json.Decoder`/`json.Encoder` for streaming many objects from one `io.Reader`.
- Use `json.NewDecoder().DisallowUnknownFields()` for strict API contracts.
- Use `csv.NewReader` (RFC 4180 compliant) instead of `strings.Split` when fields can contain commas.
- Use `excelize` to produce Excel reports with summaries and charts.
- Use `yaml.UnmarshalStrict` when unknown fields should fail loudly.

**Don't:**
- Decode JSON into `map[string]interface{}` when you can decode into a typed struct.
- Mix data plane (storing data) with control plane (config files) — JSON is poor for human-edited config.

**Code:**
```go
// JSON struct tags control field renaming and omission.
type Record struct {
    Name string `json:"user_name"`
    User string `json:"user"`
    ID   int    `json:"id"`
    Age  int    `json:"-"` // never serialized
}

b, err := json.Marshal(rec)
if err != nil {
    return err
}

// Decoding into a struct is preferred over map[string]interface{}.
rec := Record{}
if err := json.Unmarshal(b, &rec); err != nil {
    return err
}
```
*Ref: Go_for_DevOps.md — "Marshaling and unmarshaling to structs"*

---

```go
// Streaming JSON: read objects separated by newlines without loading all into memory.
dec := json.NewDecoder(reader)
msgs := make(chan Message, 1)
errs := make(chan error, 1)

go func() {
    defer close(msgs)
    defer close(errs)
    for {
        var m Message
        if err := dec.Decode(&m); err == io.EOF {
            break
        } else if err != nil {
            errs <- err
            return
        }
        msgs <- m
    }
}()

for m := range msgs {
    fmt.Printf("%+v\n", m)
}

// Streaming an array with leading/trailing brackets via dec.Token / dec.More.
dec := json.NewDecoder(reader)
_, err := dec.Token() // reads [
if err != nil {
    return fmt.Errorf("outer [ is missing")
}
for dec.More() {
    var m Message
    if err := dec.Decode(&m); err != nil {
        return err
    }
    fmt.Printf("%+v\n", m)
}
_, err = dec.Token() // reads ]
```
*Ref: Go_for_DevOps.md — "Marshaling and unmarshaling large messages"*

---

```go
// RFC 4180 CSV reading and writing.
func readRecs() ([]record, error) {
    file, err := os.Open("data.csv")
    if err != nil {
        return nil, err
    }
    defer file.Close()

    reader := csv.NewReader(file)
    reader.FieldsPerRecord = 2
    reader.TrimLeadingSpace = true

    var recs []record
    for {
        data, err := reader.Read()
        if err != nil {
            if err == io.EOF {
                break
            }
            return nil, err
        }
        rec := record(data)
        recs = append(recs, rec)
    }
    return recs, nil
}

w := csv.NewWriter(file)
defer w.Flush()
for _, rec := range recs {
    if err := w.Write(rec); err != nil {
        return err
    }
}
```
*Ref: Go_for_DevOps.md — "Using the encoding/csv package"*

---

```go
// Excel reporting with excelize: typed cells, summaries, and charts.
func main() {
    const sheet = "Sheet1"
    xlsx := excelize.NewFile()
    xlsx.SetCellValue(sheet, "A1", "Server Name")
    xlsx.SetCellValue(sheet, "B1", "Generation")
    xlsx.SetCellValue(sheet, "C1", "Acquisition Date")
    xlsx.SetCellValue(sheet, "D1", "CPU Vendor")
    xlsx.SetCellValue(sheet, "A2", "svlaa01")
    xlsx.SetCellValue(sheet, "B2", 12)
    xlsx.SetCellValue(sheet, "C2", mustParse("10/27/2021"))
    xlsx.SetCellValue(sheet, "D2", "Intel")
    if err := xlsx.SaveAs("./Book1.xlsx"); err != nil {
        panic(err)
    }
}
```
*Ref: Go_for_DevOps.md — "Using excelize when dealing with Excel"*

---

```go
// YAML config structs — same struct-tag pattern as JSON.
type Config struct {
    Jobs []Job
}
type Job struct {
    Name     string
    Interval time.Duration
    Cmd      string
}

data := []byte(`
jobs:
  - name: Clear tmp
    interval: 24h0m0s
    cmd: rm -rf /tmp
`)
c := Config{}
if err := yaml.Unmarshal(data, &c); err != nil {
    panic(err)
}

// yaml.UnmarshalStrict fails on unknown fields — safer for configs.
```
*Ref: Go_for_DevOps.md — "Marshaling and unmarshaling to structs" (YAML)*

---

### SQL Data Access (Chapter 6)

**Principle:** Use `database/sql` for portability; use a database-specific driver (e.g. `pgx`) when you need native types like `jsonb`. Always hide storage behind an interface so backends can be swapped and tests stay hermetic.

**Do:**
- Wrap connections in a `*sql.DB` pool — `sql.Open` does not test connectivity, follow with `PingContext`.
- Use prepared statements (`*sql.Stmt`) for hot queries.
- Use `sql.NullString` / `sql.NullInt64` to distinguish NULL from a zero value.
- Wrap multi-step mutations in a transaction with `BeginTx` + `defer Commit/Rollback`.
- Define a storage interface and inject it — enables caching, migration, and unit tests.

**Don't:**
- Pass a `*sql.DB` directly through your business code — it locks you to one backend.

**Code:**
```go
// Connecting with database/sql + a driver registered via anonymous import.
import _ "github.com/jackc/pgx/v4/stdlib"

conn, err := sql.Open("pgx", dbURL)
if err != nil {
    return fmt.Errorf("connect to db error: %s\n", err)
}
defer conn.Close()

ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
if err := conn.PingContext(ctx); err != nil {
    return err
}
cancel()
```
*Ref: Go_for_DevOps.md — "Connecting to a Postgres database"*

---

```go
// Storage struct that caches prepared statements.
type Storage struct {
    conn          *sql.DB
    getUserStmt   *sql.Stmt
}

func NewStorage(ctx context.Context, conn *sql.DB) *Storage {
    return &Storage{
        getUserStmt: conn.PrepareContext(
            ctx,
            `SELECT "User","DisplayName" FROM users WHERE "ID" = $1`,
        ),
    }
}

func (s *Storage) GetUser(ctx context.Context, id int) (UserRec, error) {
    u := UserRec{ID: id}
    err := s.getUserStmt.QueryRow(id).Scan(&u)
    return u, err
}
```
*Ref: Go_for_DevOps.md — "Querying a Postgres database"*

---

```go
// Transactions: BeginTx + defer Rollback-or-Commit, with serializable isolation.
func (s *Storage) AddOrUpdateUser(ctx context.Context, u UserRec) (err error) {
    const (
        getStmt    = `SELECT "ID" FROM users WHERE "User" = $1`
        insertStmt = `INSERT INTO users (User,DisplayName,ID) VALUES ($1, $2, $3)`
        updateStmt = `UPDATE "users" SET "User" = $1, "DisplayName" = $2 WHERE "ID" = $3`
    )
    tx, err := s.conn.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
    if err != nil {
        return err
    }
    defer func() {
        if err != nil {
            tx.Rollback()
            return
        }
        err = tx.Commit()
    }()
    _, err = tx.QueryRowContext(ctx, getStmt, u.User)
    if err != nil {
        if err == sql.ErrNoRows {
            _, err = tx.ExecContext(ctx, insertStmt, u.User, u.DisplayName, u.ID)
        }
        return err
    }
    _, err = tx.ExecContext(ctx, updateStmt, u.User, u.DisplayName, u.ID)
    return err
}
```
*Ref: Go_for_DevOps.md — "Transactions"*

---

```go
// Hide storage behind an interface so the backend can be replaced
// (Postgres -> Spanner, with cache wrappers, with in-memory test doubles, etc.).
type UserStorage interface {
    User(ctx context.Context, id string) (UserRec, error)
    AddUser(ctx context.Context, u UserRec) error
    UpdateDisplayName(ctx context.Context, id string, name string) error
}
```
*Ref: Go_for_DevOps.md — "Storage abstractions"*

---

### REST Clients and Servers (Chapter 6)

**Principle:** REST is unstructured; for an internal org standard, **mandate POST-only + JSON-only + no query variables** to cut framework complexity.

**Do:**
- Default-request timeouts via `context.WithDeadline`.
- Use `http.NewRequestWithContext` so the request honors cancellation.
- Read the body with `io.ReadAll(resp.Body)` and unmarshal into a typed response struct.
- Separate transport (`http.Client`) from request construction.

**Code:**
```go
// Generic REST POST helper: any struct request/response via interface{}.
func (q *QOTD) restCall(ctx context.Context, endpoint string, req, resp interface{}) error {
    if _, ok := ctx.Deadline(); !ok {
        var cancel context.CancelFunc
        ctx, cancel = context.WithDeadline(ctx, 2*time.Second)
        defer cancel()
    }
    b, err := json.Marshal(req)
    if err != nil {
        return err
    }
    hReq, err := http.NewRequestWithContext(
        ctx,
        http.MethodPost,
        endpoint,
        bytes.NewBuffer(b),
    )
    if err != nil {
        return err
    }
    resp_, err := q.client.Do(hReq)
    if err != nil {
        return err
    }
    b, err = io.ReadAll(resp_.Body)
    if err != nil {
        return err
    }
    return json.Unmarshal(b, resp)
}
```
*Ref: Go_for_DevOps.md — "Writing a REST client"*

---

```go
// Standard library HTTP server with ServeMux routing.
func newServer(port int) (*server, error) {
    s := &server{
        serv: &http.Server{
            Addr: ":" + strconv.Itoa(port),
        },
        quotes: map[string][]string{
            // Add quotes here
        },
    }
    mux := http.NewServeMux()
    mux.HandleFunc(`/qotd/v1/get`, s.qotdGet)
    s.serv.Handler = mux
    return s, nil
}

func (s *server) start() error {
    return s.serv.ListenAndServe()
}
```
*Ref: Go_for_DevOps.md — "Writing a REST service"*

---

### gRPC Services and Clients (Chapter 6)

**Principle:** Standardize your organization on gRPC + protocol buffers — strong typing, 10x JSON perf, generated stubs in every language, streaming built in.

**Do:**
- Use `buf` (`buf build`, `buf generate`) instead of raw `protoc` to manage `.proto` → Go generation.
- Use `status.Error(codes.X, msg)` for gRPC errors that map cleanly to HTTP semantics.
- Embed `pb.Unimplemented<X>Server` so the compiler catches missing RPC methods.
- Hold one connection per service (`grpc.Dial` once, reuse the `ClientConn`).

**Code:**
```proto
syntax = "proto3";
package qotd;
option go_package = "github.com/[repo]/proto/qotd";

message GetReq  { string author = 1; }
message GetResp { string author = 1; string quote = 2; }

service QOTD {
  rpc GetQOTD(GetReq) returns (GetResp) {};
}
```
*Ref: Go_for_DevOps.md — "Protocol buffers"*

---

```go
// gRPC client wrapper — sets default deadline, forwards cancellation to server.
func New(addr string) (*Client, error) {
    conn, err := grpc.Dial(addr, grpc.WithInsecure())
    if err != nil {
        return nil, err
    }
    return &Client{
        client: pb.NewQOTDClient(conn),
        conn:   conn,
    }, nil
}

func (c *Client) QOTD(ctx context.Context, wantAuthor string) (author, quote string, err error) {
    if _, ok := ctx.Deadline(); !ok {
        var cancel context.CancelFunc
        ctx, cancel = context.WithTimeout(ctx, 2*time.Second)
        defer cancel()
    }
    resp, err := c.client.GetQOTD(ctx, &pb.GetReq{Author: wantAuthor})
    if err != nil {
        return "", "", err
    }
    return resp.Author, resp.Quote, nil
}
```
*Ref: Go_for_DevOps.md — "Writing a gRPC client"*

---

```go
// gRPC server skeleton: embed UnimplementedX, register service, serve on TCP.
type API struct {
    pb.UnimplementedQOTDServer
    addr       string
    quotes     map[string][]string
    mu         sync.Mutex
    grpcServer *grpc.Server
}

func New(addr string) (*API, error) {
    var opts []grpc.ServerOption
    a := &API{
        addr:       addr,
        grpcServer: grpc.NewServer(opts...),
    }
    a.grpcServer.RegisterService(&pb.QOTD_ServiceDesc, a)
    return a, nil
}

func (a *API) Start() error {
    lis, err := net.Listen("tcp", a.addr)
    if err != nil {
        return err
    }
    return a.grpcServer.Serve(lis)
}

func (a *API) GetQOTD(ctx context.Context, req *pb.GetReq) (*pb.GetResp, error) {
    quotes, ok := a.quotes[req.Author]
    if !ok {
        return nil, status.Error(codes.NotFound,
            fmt.Sprintf("author %q not found", req.Author))
    }
    return &pb.GetResp{
        Author: req.Author,
        Quote:  quotes[rand.Intn(len(quotes))],
    }, nil
}
```
*Ref: Go_for_DevOps.md — "Writing a gRPC server"*

---

### Command-Line Tooling — flag and Cobra (Chapter 7)

**Principle:** Use stdlib `flag` for trivial CLIs; switch to `cobra` (used by `kubectl`, `gh`, `docker`) once you need subcommands, persistent flags, shell completion, or generated help.

**Do:**
- Never define flags outside `main` — pass values as function/constructor args.
- Capture `SIGINT`/`SIGTERM`/`SIGQUIT` and propagate cancellation via `context.WithCancel`.
- For Cobra: thread `context.Context` through `cmd.ExecuteContext(ctx)` so signal cancellation reaches Run handlers.

**Don't:**
- Mix `for loop` braces onto their own line — compiler rejects it.

**Code:**
```go
// stdlib flag package — defaults, descriptions, override via --name.
var endpoint = flag.String(
    "endpoint",
    "myserver.aws.com",
    "The server this app will contact",
)

func main() {
    flag.Parse()
    fmt.Println("server endpoint is: ", *endpoint)
}
```
*Ref: Go_for_DevOps.md — "The flag package"*

---

```go
// Custom flag.Value implementation for typed args (e.g. *url.URL).
type URLValue struct{ URL *url.URL }

func (v URLValue) String() string {
    if v.URL != nil {
        return v.URL.String()
    }
    return ""
}
func (v URLValue) Set(s string) error {
    u, err := url.Parse(s)
    if err != nil {
        return err
    }
    *v.URL = *u
    return nil
}

var u = &url.URL{}
func init() {
    flag.Var(&URLValue{u}, "url", "URL to parse")
}
```
*Ref: Go_for_DevOps.md — "Custom flags"*

---

```go
// Read from STDIN when no file arg is supplied (Unix-pipeline style).
var errRE = regexp.MustCompile(`(?i)error`)

func main() {
    var s *bufio.Scanner
    switch len(os.Args) {
    case 1:
        log.Println("No file specified, using STDIN")
        s = bufio.NewScanner(os.Stdin)
    case 2:
        f, err := os.Open(os.Args[1])
        if err != nil {
            log.Println(err)
            os.Exit(1)
        }
        s = bufio.NewScanner(f)
    default:
        log.Println("too many arguments provided")
        os.Exit(1)
    }
    for s.Scan() {
        line := s.Bytes()
        if errRE.Match(line) {
            fmt.Printf("%s\n", line)
        }
    }
    if err := s.Err(); err != nil {
        log.Println("Error: ", err)
        os.Exit(1)
    }
}
```
*Ref: Go_for_DevOps.md — "Retrieving input from STDIN"*

---

```go
// Cobra: subcommand with flags wired through to a Run handler.
var getCmd = &cobra.Command{
    Use:   "get",
    Short: "Get a quote from the QOTD server",
    Run: func(cmd *cobra.Command, args []string) {
        fs := cmd.Flags()
        addr := mustString(fs, "addr")
        if mustBool(fs, "dev") {
            addr = "127.0.0.1:3450"
        }
        c, err := client.New(addr)
        if err != nil {
            fmt.Println("error: ", err)
            os.Exit(1)
        }
        a, q, err := c.QOTD(cmd.Context(), mustString(fs, "author"))
        if err != nil {
            fmt.Println("error: ", err)
            os.Exit(1)
        }
        fmt.Println("Author: ", a)
        fmt.Println("Quote: ", q)
    },
}

func init() {
    rootCmd.AddCommand(getCmd)
    getCmd.Flags().BoolP("dev", "d", false, "Uses the dev server instead of prod")
    getCmd.Flags().String("addr", "127.0.0.1:80", "Set the QOTD server to use")
    getCmd.Flags().StringP("author", "a", "", "Specify the author to get a quote for")
    getCmd.Flags().Bool("json", false, "Output is in JSON format")
}
```
*Ref: Go_for_DevOps.md — "The command package"*

---

```go
// OS signal handling -> context cancellation -> cleanup.
func handleSignal(cancel context.CancelFunc) chan os.Signal {
    out := make(chan os.Signal, 1)
    notify := make(chan os.Signal, 10)
    signal.Notify(notify, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT)
    go func() {
        defer close(out)
        for {
            sig := <-notify
            switch sig {
            case syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT:
                cancel()
                out <- sig
                return
            default:
                log.Println("unhandled signal: ", sig)
            }
        }
    }()
    return out
}
```
*Ref: Go_for_DevOps.md — "Using Context to cancel"*

---

### os/exec and SSH Automation (Chapter 8)

**Principle:** Use `exec.LookPath` to verify prerequisites, `exec.CommandContext` to honor cancellation, and `golang.org/x/crypto/ssh` for in-process SSH instead of shelling out to the `ssh` binary.

**Do:**
- Check tool availability up front — fail fast before partial mutations.
- Pass `context.Context` to `exec.CommandContext` so timeouts cancel child processes.
- Use `gobreaker`/exponential backoff around RPCs to prevent retry storms.
- For rollouts: separate canary (serial, sleep between) from general (concurrent, max-failure bounded).

**Don't:**
- Use `ssh.InsecureIgnoreHostKey()` in production — it allows MITM.

**Code:**
```go
// Verify essential binaries are on PATH before starting work.
const (
    kubectl = "kubectl"
    git     = "git"
)
if _, err := exec.LookPath(kubectl); err != nil {
    return fmt.Errorf("cannot find kubectl in our PATH")
}
if _, err := exec.LookPath(git); err != nil {
    return fmt.Errorf("cannot find git in our PATH")
}
```
*Ref: Go_for_DevOps.md — "Determining the availability of essential tools"*

---

```go
// Run a binary with a context-enforced timeout.
cmd := exec.CommandContext(ctx, kubectl, "apply", "-f", config)
output, err := cmd.CombinedOutput()
if err != nil {
    return fmt.Errorf("kubectl apply failed: %w: %s", err, output)
}
```
*Ref: Go_for_DevOps.md — "Executing binaries with the exec package"*

---

```go
// Concurrent scanner: ping up to 100 hosts at once via a buffered-channel limiter.
func scanPrefixes(ipCh chan net.IP) chan record {
    ch := make(chan record, 1)
    go func() {
        defer close(ch)
        limit := make(chan struct{}, 100)
        wg := sync.WaitGroup{}
        for ip := range ipCh {
            limit <- struct{}{}
            wg.Add(1)
            go func(ip net.IP) {
                defer func() { <-limit }()
                defer wg.Done()
                ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
                defer cancel()
                rec := record{Host: ip}
                if hostAlive(ctx, ip) {
                    rec.Reachable = true
                }
                ch <- rec
            }(ip)
        }
        wg.Wait()
    }()
    return ch
}
```
*Ref: Go_for_DevOps.md — "Using os/exec to automate local changes"*

---

```go
// SSH via the golang.org/x/crypto/ssh package — no shelling out.
// Public-key auth from a private key file.
func publicKey(privateKeyFile string) (ssh.AuthMethod, error) {
    k, err := os.ReadFile(privateKeyFile)
    if err != nil {
        return nil, err
    }
    signer, err := ssh.ParsePrivateKey(k)
    if err != nil {
        return nil, err
    }
    return ssh.PublicKeys(signer), nil
}

config := &ssh.ClientConfig{
    User:            user,
    Auth:            []ssh.AuthMethod{auth},
    HostKeyCallback: ssh.InsecureIgnoreHostKey(), // NEVER in production
    Timeout:         5 * time.Second,
}

conn, err := ssh.Dial("tcp", host, config)
if err != nil {
    return err
}
defer conn.Close()

// Run a single command on a new session.
func combinedOutput(conn *ssh.Client, cmd string) (string, error) {
    sess, err := conn.NewSession()
    if err != nil {
        return "", err
    }
    defer sess.Close()
    b, err := sess.Output(cmd)
    return string(b), err
}
```
*Ref: Go_for_DevOps.md — "Using SSH in Go to automate remote changes"*

---

```go
// State-machine style action runner for ordered rollout steps.
type stateFn func(ctx context.Context) (stateFn, error)

type actions struct { /* ... */ }

func (s *actions) run(ctx context.Context) error {
    fn := s.rmBackend
    for {
        if ctx.Err() != nil {
            return ctx.Err()
        }
        next, err := fn(ctx)
        if err != nil {
            return err
        }
        if next == nil {
            return nil
        }
        fn = next
    }
}

func (a *actions) rmBackend(ctx context.Context) (stateFn, error) {
    if err := a.lb.RemoveBackend(ctx, a.config.Pattern, a.backend); err != nil {
        return nil, fmt.Errorf("problem removing backend from pool: %w", err)
    }
    return a.jobKill, nil
}
```
*Ref: Go_for_DevOps.md — "Writing a concurrent job"*

---

```go
// Canary + concurrent rollout with max-failure circuit breaker.
limit := make(chan struct{}, w.config.Concurrency)
wg := sync.WaitGroup{}
for i := w.config.CanaryNum; int(i) < len(w.actions); i++ {
    i := i
    limit <- struct{}{}
    if atomic.LoadInt32(&w.failures) > w.config.MaxFailures {
        break
    }
    wg.Add(1)
    go func() {
        defer func() { <-limit }()
        defer wg.Done()
        ctx, cancel := context.WithTimeout(ctx, 10*time.Minute)
        err := w.actions[i].run(ctx)
        cancel()
        if err != nil {
            atomic.AddInt32(&w.failures, 1)
        }
    }()
}
wg.Wait()
```
*Ref: Go_for_DevOps.md — "Designing safe, concurrent change automations"*

---

### System Agents (Chapter 8)

**Principle:** Run an agent on every machine exposing RPCs (gRPC over Unix socket) and read-only metrics over HTTP — uniform control across OSes.

**Code:**
```go
// Collect perf stats in a loop, store via atomic.Value, expose via expvar.
func (a *Agent) collectCPU(resolution int) error {
    stat, err := linuxproc.ReadStat("/proc/stat")
    if err != nil {
        return err
    }
    v := &pb.CPUPerfs{
        ResolutionSecs: resolution,
        UnixTimeNano:   time.Now().UnixNano(),
    }
    for _, p := range stat.CPUStats {
        v.Cpu = append(v.Cpu, &pb.CPUPerf{
            Id: p.Id, User: int32(p.User), System: int32(p.System),
            Idle: int32(p.Idle), IoWait: int32(p.IOWait), Irq: int32(p.IRQ),
        })
    }
    a.cpuData.Store(v) // atomic.Value — replace, never mutate
    return nil
}

func (a *Agent) perfLoop() error {
    const resolutionSecs = 10
    if err := a.collectCPU(resolutionSecs); err != nil {
        return err
    }
    expvar.Publish("system-cpu", expvar.Func(func() interface{} {
        return a.cpuData.Load().(*pb.CPUPerfs)
    }))
    go func() {
        for {
            time.Sleep(resolutionSecs * time.Second)
            if err := a.collectCPU(resolutionSecs); err != nil {
                log.Println(err)
            }
        }
    }()
    return nil
}
```
*Ref: Go_for_DevOps.md — "Implementing SystemPerf"*

---

### Observability with OpenTelemetry (Chapter 9)

**Principle:** Without logs + traces + metrics you are blind during an outage. Use OpenTelemetry (vendor-neutral) → OTel Collector → Jaeger / Prometheus / Alertmanager.

**Do:**
- Use Zap for structured, leveled logs with typed fields (`zap.String`, `zap.Int`, `zap.Duration`).
- Inject `trace_id` and `span_id` into every log line so logs correlate with traces.
- Set `service.name` via `resource.WithAttributes(semconv.ServiceNameKey.String(...))`.
- Wrap HTTP transports and handlers with `otelhttp.NewTransport` / `otelhttp.NewHandler` for automatic propagation.
- Define Prometheus alert rules declaratively in `rules/*.yml`, route via Alertmanager to PagerDuty/Slack.

**Don't:**
- Run `log.Println` in production services — no structure, no levels, no correlation.

**Code:**
```go
// Structured logging with Zap — strongly typed fields, named sub-loggers.
logger, _ := zap.NewProduction()
defer logger.Sync()
logger = logger.Named("my-app")
logger.Info("failed to fetch URL",
    zap.String("url", "https://github.com"),
    zap.Int("attempt", 3),
    zap.Duration("backoff", time.Second),
)
```
*Ref: Go_for_DevOps.md — "Structured and leveled logs with Zap"*

---

```go
// Initialize the global tracer provider: OTLP/gRPC exporter + AlwaysSample.
func initTracer(ctx context.Context, otelAgentAddr string) func(context.Context) {
    traceClient := otlptracegrpc.NewClient(
        otlptracegrpc.WithInsecure(),
        otlptracegrpc.WithEndpoint(otelAgentAddr),
        otlptracegrpc.WithDialOption(grpc.WithBlock()),
    )
    traceExp, err := otlptrace.New(ctx, traceClient)
    if err != nil {
        log.Fatal("Failed to create the collector trace exporter", err)
    }
    res, _ := resource.New(ctx,
        resource.WithFromEnv(),
        resource.WithProcess(),
        resource.WithTelemetrySDK(),
        resource.WithHost(),
        resource.WithAttributes(semconv.ServiceNameKey.String("demo-client")),
    )
    bsp := sdktrace.NewBatchSpanProcessor(traceExp)
    tracerProvider := sdktrace.NewTracerProvider(
        sdktrace.WithSampler(sdktrace.AlwaysSample()),
        sdktrace.WithResource(res),
        sdktrace.WithSpanProcessor(bsp),
    )
    otel.SetTextMapPropagator(propagation.TraceContext{})
    otel.SetTracerProvider(tracerProvider)
    return func(doneCtx context.Context) {
        if err := traceExp.Shutdown(doneCtx); err != nil {
            otel.Handle(err)
        }
    }
}
```
*Ref: Go_for_DevOps.md — "Client/server-distributed tracing with OpenTelemetry"*

---

```go
// Client-side: wrap http.Client transport to inject span context on outgoing requests.
func makeRequest(ctx context.Context) {
    client := http.Client{
        Transport: otelhttp.NewTransport(http.DefaultTransport),
    }
    req, _ := http.NewRequestWithContext(ctx, "GET", demoServerAddr, nil)
    res, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    res.Body.Close()
}

// Server-side: wrap the handler so incoming span context is extracted and
// continued.
func main() {
    shutdown := initTraceProvider()
    defer shutdown()
    handler := handleRequestWithRandomSleep()
    wrappedHandler := otelhttp.NewHandler(handler, "/hello")
    http.Handle("/hello", wrappedHandler)
    http.ListenAndServe(":7080", nil)
}

// Add attributes to the propagated span.
func handleRequestWithRandomSleep() http.HandlerFunc {
    commonLabels := []attribute.KeyValue{attribute.String("server-attribute", "foo")}
    return func(w http.ResponseWriter, req *http.Request) {
        ctx := req.Context()
        span := trace.SpanFromContext(ctx)
        span.SetAttributes(commonLabels...)
        w.Write([]byte("Hello World"))
    }
}
```
*Ref: Go_for_DevOps.md — "Client/server-distributed tracing with OpenTelemetry"*

---

```go
// Correlate logs with traces by attaching span_id / trace_id to the logger.
func WithCorrelation(span trace.Span, log *zap.Logger) *zap.Logger {
    return log.With(
        zap.String("span_id", span.SpanContext().SpanID().String()),
        zap.String("trace_id", span.SpanContext().TraceID().String()),
    )
}

// Embed log events directly into spans (visible in Jaeger).
func SuccessfullyFinishedRequestEvent(span trace.Span, opts ...trace.EventOption) {
    opts = append(opts, trace.WithAttributes(attribute.String("someKey", "someValue")))
    span.AddEvent("successfully finished request operation", opts...)
}
```
*Ref: Go_for_DevOps.md — "Correlating traces and logs" / "Adding log entries to spans"*

---

```go
// Define metric instruments with descriptive names — used for Prometheus queries.
func NewClientInstruments(meter metric.Meter) ClientInstruments {
    return ClientInstruments{
        RequestLatency: metric.Must(meter).NewFloat64Histogram(
            "demo_client/request_latency",
            metric.WithDescription("The latency of requests processed"),
        ),
        RequestCount: metric.Must(meter).NewInt64Counter(
            "demo_client/request_counts",
            metric.WithDescription("The number of requests processed"),
        ),
    }
}

// Record a batch of correlated measurements.
meter.RecordBatch(
    ctx,
    commonLabels,
    instruments.RequestLatency.Measurement(latencyMs),
    instruments.RequestCount.Measurement(1),
)
```
*Ref: Go_for_DevOps.md — "Instrumenting for metrics"*

---

```yaml
# Prometheus alert rule — declarative, version-controlled.
groups:
  - name: demo-server
    rules:
      - alert: HighRequestLatency
        expr: |
          histogram_quantile(0.5, rate(http_server_duration_bucket{exported_job="demo-server"}[5m])) > 200000
        labels:
          severity: page
        annotations:
          summary: High request latency
```
*Ref: Go_for_DevOps.md — "Alerting on metrics abnormalities"*

---

### GitHub Actions and CI/CD (Chapter 10)

**Principle:** Eliminate toil by turning manual release steps into event-driven YAML workflows; ship Go-based custom actions via container images for fast cold-start.

**Do:**
- Use matrix builds to test on (ubuntu/macos/windows) × (Go versions) concurrently.
- Trigger releases on semantic-version tags (`v[0-9]+.[0-9]+.*`); gate the release job behind `needs: test`.
- Build cross-platform binaries with `gox` and `CGO_ENABLED=0` for static linking.
- Use `gh release create` with auto-generated release notes from PRs (`.github/release.yml` categorizes by label).
- For custom container actions, publish to `ghcr.io` and reference `docker://…` in `action.yaml` to skip rebuild on every run.

**Code:**
```yaml
# Continuous integration: matrix on OS × Go version, lint, test.
name: tweeter-automation
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.*'
    branches:
      - main
  pull_request:
    branches:
      - main
jobs:
  test:
    strategy:
      matrix:
        go-version: [ 1.16.x, 1.17.x ]
        os: [ ubuntu-latest, macos-latest, windows-latest ]
    runs-on: ${{ matrix.os }}
    steps:
      - name: install go
        uses: actions/setup-go@v2
        with:
          go-version: ${{ matrix.go-version }}
      - uses: actions/checkout@v2
      - name: lint with golangci-lint
        uses: golangci/golangci-lint-action@v2
      - name: run go test
        run: go test ./...
```
*Ref: Go_for_DevOps.md — "Continuous integration workflow for tweeter"*

---

```yaml
# Release job — gated by tests, restricted to tag pushes, cross-compiles with gox.
  release:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set RELEASE_VERSION ENV var
        run: echo "RELEASE_VERSION=${GITHUB_REF:10}" >> $GITHUB_ENV
      - name: install go
        uses: actions/setup-go@v2
        with:
          go-version: 1.17.x
      - name: install gox
        run: go install github.com/mitchellh/gox@v1.0.1
      - name: build cross-platform binaries
        env:
          PLATFORMS: darwin/amd64 darwin/arm64 windows/amd64 linux/amd64 linux/arm64
          VERSION_INJECT: github.com/devopsforgo/github-actions/pkg/tweeter.Version
          OUTPUT_PATH_FORMAT: ./bin/${{ env.RELEASE_VERSION }}/{{.OS}}/{{.Arch}}/tweeter
        run: |
          gox -osarch="${PLATFORMS}" \
            -ldflags "-X ${VERSION_INJECT}=${RELEASE_VERSION}" \
            -output "${OUTPUT_PATH_FORMAT}"
```
*Ref: Go_for_DevOps.md — "Building cross-platform binaries and version injection"*

---

```yaml
# Auto-generate release notes from PRs and create a GitHub release with artifacts.
      - name: generate release notes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh api -X POST 'repos/{owner}/{repo}/releases/generate-notes' \
            -F commitish=${{ env.RELEASE_VERSION }} \
            -F tag_name=${{ env.RELEASE_VERSION }} \
            > tmp-release-notes.json
      - name: create release
        env:
          OUT_BASE: ./bin/${{ env.RELEASE_VERSION }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          jq -r .body tmp-release-notes.json > tmp-release-notes.md
          gh release create ${{ env.RELEASE_VERSION }} \
            -t "$(jq -r .name tmp-release-notes.json)" \
            -F tmp-release-notes.md \
            "${OUT_BASE}/linux/amd64/tweeter_linux_amd64.tar.gz#tweeter_linux_amd64"
```
*Ref: Go_for_DevOps.md — "Generating release notes" / "Creating the GitHub release"*

---

```yaml
# .github/release.yml — categorize release notes by PR label.
changelog:
  exclude:
    labels:
      - ignore-for-release
  categories:
    - title: Breaking Changes
      labels: [ breaking-change ]
    - title: New Features
      labels: [ enhancement ]
    - title: Bug Fixes
      labels: [ bug-fix ]
    - title: Other Changes
      labels: [ "*" ]
```
*Ref: Go_for_DevOps.md — "Generating release notes"*

---

```dockerfile
# Multi-stage Dockerfile for a Go action — distroless final image.
FROM golang:1.17 as builder
WORKDIR /workspace
COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download
COPY ./ ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -ldflags '-extldflags "-static"' -o tweeter .

FROM gcr.io/distroless/static:latest
WORKDIR /
COPY --from=builder /workspace/tweeter .
ENTRYPOINT ["/tweeter"]
```
*Ref: Go_for_DevOps.md — "Defining a Dockerfile"*

---

```go
// Output variables from a Go action via the ::set-output:: protocol.
func printOutput(key, message string) {
    fmt.Printf("::set-output name=%s::%s\n", key, message)
}
```
*Ref: Go_for_DevOps.md — "Creating action metadata"*

---

### ChatOps with Slack (Chapter 11)

**Principle:** Separate the **Ops service** (does real work — Jaeger/Prometheus/etc.) from the **ChatOps service** (translates Slack messages into Ops RPCs). This lets you swap chat platforms without touching operations code.

**Do:**
- Use `slack-go/socketmode` to operate behind firewalls (WebSocket, no inbound).
- Route messages to handlers with regex — first match wins; provide a `lastResort` default.
- Always provide a `help` handler so users can discover commands.

**Code:**
```go
// Bot skeleton: register regex → handler, listen on socketmode events.
type HandleFunc func(ctx context.Context, m Message)

type Bot struct {
    api            *slack.Client
    client         *socketmode.Client
    ctx            context.Context
    cancel         context.CancelFunc
    defaultHandler HandleFunc
    reg            []register
}

func (b *Bot) Register(r *regexp.Regexp, h HandleFunc) {
    if r == nil {
        b.defaultHandler = h
        return
    }
    b.reg = append(b.reg, register{r, h})
}

func (b *Bot) Start() {
    b.ctx, b.cancel = context.WithCancel(context.Background())
    go b.loop()
    b.client.RunContext(b.ctx)
}

func (b *Bot) loop() {
    for {
        select {
        case <-b.ctx.Done():
            return
        case evt := <-b.client.Events:
            if evt.Type == socketmode.EventTypeEventsAPI {
                data, _ := evt.Data.(slackevents.EventsAPIEvent)
                b.client.Ack(*evt.Request)
                go b.appMentioned(data)
            }
        }
    }
}
```
*Ref: Go_for_DevOps.md — "Building a basic chatbot"*

---

```go
// Message handler: parse options via regex, call Ops gRPC, render an ASCII table.
var listTracesRE = regexp.MustCompile(`(\S+)=(?:(\S+))`)

func (o Ops) ListTraces(ctx context.Context, m bot.Message) {
    sp := strings.Split(m.Text, "list traces")
    if len(sp) != 2 {
        o.write(m, "The 'list traces' command is malformed")
        return
    }
    matches := listTracesRE.FindAllStringSubmatch(strings.TrimSpace(sp[1]), -1)

    options := []client.CallOption{}
    for _, match := range matches {
        key, val := strings.TrimSpace(match[1]), strings.TrimSpace(match[2])
        switch key {
        case "operation":
            options = append(options, client.WithOperation(val))
        case "limit":
            i, err := strconv.Atoi(val)
            if err != nil || i > 100 {
                o.write(m, "limit must be an integer <= 100")
                return
            }
            options = append(options, client.WithLimit(int32(i)))
        /* ... */
        }
    }

    traces, err := o.OpsClient.ListTraces(ctx, options...)
    if err != nil {
        o.write(m, "Ops server had an error: %s", err)
        return
    }
    b := strings.Builder{}
    table := tablewriter.NewWriter(&b)
    table.SetHeader([]string{"Start Time(UTC)", "Trace ID"})
    for _, item := range traces {
        table.Append([]string{
            item.Start.Format("01/02/2006 04:05"),
            "http://127.0.0.1:16686/trace/" + item.ID,
        })
    }
    table.Render()
    o.write(m, b.String())
}
```
*Ref: Go_for_DevOps.md — "Creating event handlers"*

---

### Packer — Immutable Infrastructure (Chapter 12)

**Principle:** Standardize OS images across VMs and containers; validate every image with Goss before publishing.

**Do:**
- Use HCL2 (`*.pkr.hcl`), not the deprecated JSON template.
- Declare `required_plugins` with version + source so `packer init` is reproducible.
- Compose provisioners (shell + file + Goss) — each provisioner block is one logical change.
- Write custom provisioners as multi-plugins (`plugin.NewSet`) so users install via `packer init`.

**Code:**
```hcl
# required_plugins block — packer init downloads these automatically.
packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/amazon"
    }
    installGo = {
      version = ">= 0.0.1"
      source  = "github.com/johnsiilver/goenv"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  access_key      = "your key"
  secret_key      = "your secret"
  ami_name        = "ubuntu-amd64"
  instance_type   = "t2.micro"
  region          = "us-east-2"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-xenial-16.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }
  ssh_username = "ubuntu"
}

build {
  name = "goBook"
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get install -y dbus dbus-x11",
    ]
  }

  provisioner "file" {
    source      = "./files/agent"
    destination = "/tmp/agent"
  }

  provisioner "shell" {
    inline = [
      "sudo mv /tmp/agent.service /etc/systemd/system/agent.service",
      "sudo systemctl enable agent.service",
      "sudo systemctl daemon-reload",
      "sudo systemctl start agent.service",
      "sleep 10",
      "sudo systemctl is-active agent.service",
    ]
  }

  # Goss validation — fails the build if the image doesn't meet spec.
  provisioner "goss" {
    retry_timeout = "30s"
    tests = [
      "files/goss/goss.yaml",
      "files/goss/files.yaml",
      "files/goss/dbus.yaml",
      "files/goss/process.yaml",
    ]
  }
}
```
*Ref: Go_for_DevOps.md — "Building an Amazon Machine Image" / "Validating images with Goss"*

---

```go
// Custom Packer provisioner plugin (multi-plugin style).
type Provisioner struct {
    packer.Provisioner
    conf     *config.Provisioner
    content  []byte
    fileName string
}

func (p *Provisioner) ConfigSpec() hcldec.ObjectSpec {
    return new(config.FlatProvisioner).HCL2Spec()
}

func (p *Provisioner) Prepare(raws ...interface{}) error {
    c := config.Provisioner{}
    if err := packerConfig.Decode(&c, nil, raws...); err != nil {
        return err
    }
    c.Defaults()
    p.conf = &c
    return nil
}

func (p *Provisioner) Provision(
    ctx context.Context,
    u packer.Ui,
    c packer.Communicator,
    m map[string]interface{},
) error {
    u.Message("Begin Go environment install")
    if err := p.fetch(ctx, u, c); err != nil { return err }
    if err := p.push(ctx, u, c); err != nil { return err }
    if err := p.unpack(ctx, u, c); err != nil { return err }
    if err := p.test(ctx, u, c); err != nil { return err }
    return nil
}

func main() {
    set := plugin.NewSet()
    set.SetVersion(pv)
    set.RegisterProvisioner("goenv", &Provisioner{})
    if err := set.Run(); err != nil {
        fmt.Fprintln(os.Stderr, err.Error())
        os.Exit(1)
    }
}
```
*Ref: Go_for_DevOps.md — "Writing your own plugin"*

---

### Terraform — Infrastructure as Code (Chapter 13)

**Principle:** Terraform reconciles desired state with real infrastructure via providers (plugins). Build custom providers for any external API your team manages.

**Do:**
- Always `terraform init` after changing `required_providers`, then `plan` before `apply`.
- Store `terraform.tfstate` remotely for team sharing (S3 + DynamoDB lock, Azure blob, etc.).
- Use `terraform destroy` to clean up — don't delete resources by hand.
- For custom providers, register CRUD handlers via `schema.Resource` and validate inputs with `ValidateDiagFunc`.

**Code:**
```hcl
# Define an Azure resource group + App Service plan + Linux web app (running nginx).
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "mygroup" {
  name     = "mygroup"
  location = "southcentralus"
}

resource "azurerm_service_plan" "myplan" {
  name                = "myplan"
  resource_group_name = azurerm_resource_group.mygroup.name
  location            = azurerm_resource_group.mygroup.location
  os_type             = "Linux"
  sku_name            = "S1"
}

resource "azurerm_linux_web_app" "myapp" {
  name                = "myapp-${random_integer.ri.result}"
  resource_group_name = azurerm_resource_group.mygroup.name
  location            = azurerm_service_plan.myplan.location
  service_plan_id     = azurerm_service_plan.myplan.id
  site_config {
    application_stack {
      docker_image     = "nginxdemos/hello"
      docker_image_tag = "latest"
    }
  }
}

output "host_name" {
  value = azurerm_linux_web_app.myapp.default_hostname
}
```
*Ref: Go_for_DevOps.md — "Defining and provisioning cloud resources"*

---

```go
// Custom Terraform provider entry point.
func Provider() *schema.Provider {
    return &schema.Provider{
        Schema: map[string]*schema.Schema{
            "host": {
                Type:         schema.TypeString,
                Optional:     true,
                DefaultFunc:  schema.EnvDefaultFunc("PETSTORE_HOST", nil),
            },
        },
        ResourcesMap: map[string]*schema.Resource{
            "petstore_pet": resourcePet(),
        },
        DataSourcesMap: map[string]*schema.Resource{
            "petstore_pet": dataSourcePet(),
        },
        ConfigureContextFunc: configure,
    }
}

func configure(_ context.Context, data *schema.ResourceData) (interface{}, diag.Diagnostics) {
    var diags diag.Diagnostics
    host, ok := data.Get("host").(string)
    if !ok {
        return nil, diag.Errorf("the host must be provided explicitly or via PETSTORE_HOST")
    }
    c, err := client.New(host)
    if err != nil {
        return nil, append(diags, diag.Diagnostic{
            Severity: diag.Error,
            Summary:  "Unable to create Pet Store client",
            Detail:   "Unable to connect to the Pet Store service",
        })
    }
    return c, diags
}
```
*Ref: Go_for_DevOps.md — "The pet store provider"*

---

```go
// Custom resource CRUD: schema with validation + Create/Read/Update/Delete handlers.
func resourcePet() *schema.Resource {
    return &schema.Resource{
        CreateContext: resourcePetCreate,
        ReadContext:   resourcePetRead,
        UpdateContext: resourcePetUpdate,
        DeleteContext: resourcePetDelete,
        Schema:        getPetResourceSchema(),
        Importer: &schema.ResourceImporter{
            StateContext: schema.ImportStatePassthroughContext,
        },
    }
}

func getPetResourceSchema() map[string]*schema.Schema {
    return map[string]*schema.Schema{
        "id":       {Type: schema.TypeString, Optional: true, Computed: true},
        "name":     {Type: schema.TypeString, Required: true, ValidateDiagFunc: validateName()},
        "type":     {Type: schema.TypeString, Required: true, ValidateDiagFunc: validateType()},
        "birthday": {Type: schema.TypeString, Required: true, ValidateDiagFunc: validateBirthday()},
    }
}

func validateType() schema.SchemaValidateDiagFunc {
    return validateDiagFunc(validation.StringInSlice([]string{
        string(DogPetType), string(CatPetType),
        string(ReptilePetType), string(BirdPetType),
    }, true))
}

func resourcePetCreate(ctx context.Context, data *schema.ResourceData, meta interface{}) diag.Diagnostics {
    psClient, _ := clientFromMeta(meta)
    pet := &client.Pet{Pet: &pb.Pet{}}
    diags := fillPetFromData(pet, data)
    ids, err := psClient.AddPets(ctx, []*pb.Pet{pet.Pet})
    if err != nil {
        return append(diags, diag.FromErr(err)...)
    }
    data.SetId(ids[0])
    return diags
}
```
*Ref: Go_for_DevOps.md — "Implementing the Pet resource"*

---

### Kubernetes with client-go (Chapter 14)

**Principle:** Kubernetes is a set of REST APIs exposed by the API server; `client-go` lets you CRUD any resource (built-in or custom) programmatically. Operators/CRDs let you reconcile **any** external state, not just containers.

**Do:**
- Build a `*kubernetes.Clientset` from kubeconfig with `clientcmd.BuildConfigFromFlags`.
- Use `metav1.CreateOptions{}` / `metav1.GetOptions{}` on every call.
- Wait for `Status.ReadyReplicas == Spec.Replicas` before declaring a Deployment ready.
- For operators: use `operator-sdk` scaffolding, set finalizers, and use a `patch.NewHelper` to track status changes.
- Reconcile loops must be **idempotent** — they re-run from scratch on every trigger.

**Code:**
```go
// Build a Clientset from ~/.kube/config (or --kubeconfig flag).
func getClientSet() *kubernetes.Clientset {
    var kubeconfig *string
    if home := homedir.HomeDir(); home != "" {
        kubeconfig = flag.String("kubeconfig",
            filepath.Join(home, ".kube", "config"),
            "(optional) absolute path to the kubeconfig file")
    } else {
        kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
    }
    flag.Parse()
    config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
    panicIfError(err)
    cs, err := kubernetes.NewForConfig(config)
    panicIfError(err)
    return cs
}

// Create a namespace.
func createNamespace(ctx context.Context, clientSet *kubernetes.Clientset, name string) *corev1.Namespace {
    ns := &corev1.Namespace{
        ObjectMeta: metav1.ObjectMeta{Name: name},
    }
    ns, err := clientSet.CoreV1().Namespaces().Create(ctx, ns, metav1.CreateOptions{})
    panicIfError(err)
    return ns
}
```
*Ref: Go_for_DevOps.md — "Creating a ClientSet" / "Creating a namespace"*

---

```go
// Deploy 2 NGINX replicas with a label selector matching the Service.
func createNginxDeployment(
    ctx context.Context,
    clientSet *kubernetes.Clientset,
    ns *corev1.Namespace,
    name string,
) *appv1.Deployment {
    matchLabel := map[string]string{"app": "nginx"}
    deployment := &appv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name: name, Namespace: ns.Name, Labels: matchLabel,
        },
        Spec: appv1.DeploymentSpec{
            Replicas: to.Int32Ptr(2),
            Selector: &metav1.LabelSelector{MatchLabels: matchLabel},
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{Labels: matchLabel},
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Name:  "nginx",
                        Image: "nginxdemos/hello:latest",
                        Ports: []corev1.ContainerPort{{ContainerPort: 80}},
                    }},
                },
            },
        },
    }
    deployment, err := clientSet.AppsV1().
        Deployments(ns.Name).
        Create(ctx, deployment, metav1.CreateOptions{})
    panicIfError(err)
    return deployment
}

// Wait for ReadyReplicas to match Spec.Replicas.
func waitForReadyReplicas(ctx context.Context, clientSet *kubernetes.Clientset, deployment *appv1.Deployment) {
    for {
        expected := *deployment.Spec.Replicas
        dep, _ := clientSet.AppsV1().
            Deployments(deployment.Namespace).
            Get(ctx, deployment.Name, metav1.GetOptions{})
        if dep.Status.ReadyReplicas == expected {
            return
        }
        time.Sleep(1 * time.Second)
    }
}
```
*Ref: Go_for_DevOps.md — "Creating the NGINX deployment" / "Waiting for ready replicas"*

---

```go
// Service to load-balance across pods, selected by label matchLabel.
service := &corev1.Service{
    ObjectMeta: metav1.ObjectMeta{Name: name, Namespace: ns.Name},
    Spec: corev1.ServiceSpec{
        Selector: matchLabel,
        Ports: []corev1.ServicePort{{
            Port: 80, Protocol: corev1.ProtocolTCP, Name: "http",
        }},
    },
}
service, err := clientSet.CoreV1().
    Services(ns.Name).
    Create(ctx, service, metav1.CreateOptions{})
```
*Ref: Go_for_DevOps.md — "Creating a Service to load-balance"*

---

```go
// Stream pod logs to STDOUT — one goroutine per pod.
func listenToPodLogs(ctx context.Context, clientSet *kubernetes.Clientset, ns *corev1.Namespace, containerName string) {
    podList, _ := clientSet.CoreV1().Pods(ns.Name).List(ctx, metav1.ListOptions{})
    for _, pod := range podList.Items {
        podName := pod.Name
        go func() {
            opts := &corev1.PodLogOptions{Container: containerName, Follow: true}
            podLogs, err := clientSet.CoreV1().
                Pods(ns.Name).
                GetLogs(podName, opts).
                Stream(ctx)
            panicIfError(err)
            _, _ = os.Stdout.ReadFrom(podLogs)
        }()
    }
}
```
*Ref: Go_for_DevOps.md — "Streaming pod logs for the NGINX application"*

---

```go
// Custom Resource Definition: strongly typed Pet type with kubebuilder markers.
// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
type Pet struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec              PetSpec   `json:"spec,omitempty"`
    Status            PetStatus `json:"status,omitempty"`
}

// +kubebuilder:validation:Enum=dog;cat;bird;reptile
type PetType string

const (
    DogPetType      PetType = "dog"
    CatPetType      PetType = "cat"
    BirdPetType     PetType = "bird"
    ReptilePetType  PetType = "reptile"
)

type PetSpec struct {
    Name    string      `json:"name"`
    Type    PetType     `json:"type"`
    Birthday metav1.Time `json:"birthday"`
}

type PetStatus struct {
    ID string `json:"id,omitempty"`
}
```
*Ref: Go_for_DevOps.md — "Initializing the new operator"*

---

```go
// Reconcile loop: fetch Pet, defer patch, branch on DeletionTimestamp.
func (r *PetReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    logger := log.FromContext(ctx)
    pet := &petstorev1.Pet{}
    if err := r.Get(ctx, req.NamespacedName, pet); err != nil {
        if apierrors.IsNotFound(err) {
            logger.Info("object was not found")
            return reconcile.Result{}, nil
        }
        return ctrl.Result{}, err
    }

    helper, err := patch.NewHelper(pet, r.Client)
    if err != nil {
        return ctrl.Result{}, errors.Wrap(err, "failed to create patch helper")
    }
    defer func() {
        if err := helper.Patch(ctx, pet); err != nil {
            /* surface via named return */
        }
    }()

    if pet.DeletionTimestamp.IsZero() {
        return r.ReconcileNormal(ctx, pet)
    }
    return r.ReconcileDelete(ctx, pet)
}

// Create-or-update against an external pet store service, then set finalizer.
func (r *PetReconciler) ReconcileNormal(ctx context.Context, pet *petstorev1.Pet) (ctrl.Result, error) {
    controllerutil.AddFinalizer(pet, PetFinalizer)
    psc, err := getPetstoreClient()
    if err != nil {
        return ctrl.Result{}, err
    }
    psPet, err := findPetInStore(ctx, psc, pet)
    if err != nil {
        return ctrl.Result{}, err
    }
    if psPet == nil {
        return ctrl.Result{}, createPetInStore(ctx, pet, psc)
    }
    return ctrl.Result{}, updatePetInStore(ctx, psc, pet, psPet.Pet)
}

// ReconcileDelete: delete from external store, then remove finalizer so K8s GCs.
func (r *PetReconciler) ReconcileDelete(ctx context.Context, pet *petstorev1.Pet) (ctrl.Result, error) {
    psc, _ := getPetstoreClient()
    if pet.Status.ID != "" {
        if err := psc.DeletePets(ctx, []string{pet.Status.ID}); err != nil {
            return ctrl.Result{}, err
        }
    }
    controllerutil.RemoveFinalizer(pet, PetFinalizer)
    return ctrl.Result{}, nil
}
```
*Ref: Go_for_DevOps.md — "Building a pet store operator"*

---

### Cloud SDKs — Microsoft Azure (Chapter 15)

**Principle:** Cloud APIs split into a **management plane** (provision resources via ARM) and a **data plane** (use the provisioned service). SDKs are auto-generated from OpenAPI specs; identity comes from AAD service principals or managed identities, not user accounts.

**Do:**
- Use `azidentity.NewDefaultAzureCredential` for local dev (env vars → managed identity → Azure CLI fallback).
- For production code on Azure, use managed identities — no secrets to rotate.
- Use long-running operations (`BeginCreateOrUpdate` → poller) for resource creation; `CreateOrUpdate` only for fast ones like resource groups.
- Generate constrained-access URIs with SAS tokens instead of sharing account keys.

**Don't:**
- Use Azure CLI auth for deployed applications — it isn't designed for non-interactive use.

**Code:**
```go
// VirtualMachineFactory pattern: hold all ARM clients in one struct.
type VirtualMachineFactory struct {
    subscriptionID string
    sshPubKeyPath  string
    cred           azcore.TokenCredential
    groupsClient   *armresources.ResourceGroupsClient
    vmClient       *armcompute.VirtualMachinesClient
    vnetClient     *armnetwork.VirtualNetworksClient
    subnetClient   *armnetwork.SubnetsClient
    nicClient      *armnetwork.InterfacesClient
    nsgClient      *armnetwork.SecurityGroupsClient
    pipClient      *armnetwork.PublicIPAddressesClient
}

func NewVirtualMachineFactory(subscriptionID, sshPubKeyPath string) *VirtualMachineFactory {
    cred := HandleErrWithResult(azidentity.NewDefaultAzureCredential(nil))
    return &VirtualMachineFactory{
        cred:           cred,
        subscriptionID: subscriptionID,
        sshPubKeyPath:  sshPubKeyPath,
        groupsClient:   BuildClient(subscriptionID, cred, armresources.NewResourceGroupsClient),
        vmClient:       BuildClient(subscriptionID, cred, armcompute.NewVirtualMachinesClient),
        // ...
    }
}
```
*Ref: Go_for_DevOps.md — "Provisioning Azure infrastructure using Go"*

---

```go
// Resource groups are created with CreateOrUpdate (synchronous, fast).
func (vmf *VirtualMachineFactory) createResourceGroup(
    ctx context.Context, name, location string,
) armresources.ResourceGroup {
    param := armresources.ResourceGroup{Location: to.Ptr(location)}
    res, err := vmf.groupsClient.CreateOrUpdate(ctx, name, param, nil)
    HandleErr(err)
    return res.ResourceGroup
}

// Network security group: long-running op, wait on the poller.
func (vmf *VirtualMachineFactory) createSecurityGroup(
    ctx context.Context, name, location string,
) armnetwork.SecurityGroup {
    param := armnetwork.SecurityGroup{
        Location: to.Ptr(location),
        Name:     to.Ptr(name + "-nsg"),
        Properties: &armnetwork.SecurityGroupPropertiesFormat{
            SecurityRules: []*armnetwork.SecurityRule{{
                Name: to.Ptr("ssh"),
                Properties: &armnetwork.SecurityRulePropertiesFormat{
                    Access:                   to.Ptr(armnetwork.SecurityRuleAccessAllow),
                    Direction:                to.Ptr(armnetwork.SecurityRuleDirectionInbound),
                    Protocol:                 to.Ptr(armnetwork.SecurityRuleProtocolAsterisk),
                    Description:              to.Ptr("allow ssh on 22"),
                    DestinationAddressPrefix: to.Ptr("*"),
                    DestinationPortRange:     to.Ptr("22"),
                    Priority:                 to.Ptr(int32(101)),
                    SourcePortRange:          to.Ptr("*"),
                    SourceAddressPrefix:      to.Ptr("*"),
                },
            }},
        },
    }
    poller, err := vmf.nsgClient.BeginCreateOrUpdate(ctx, name, *param.Name, param, nil)
    HandleErr(err)
    res := HandleErrPoller(ctx, poller)
    return res.SecurityGroup
}
```
*Ref: Go_for_DevOps.md — "Provisioning Azure infrastructure using Go"*

---

```go
// VM definition: hardware profile, image reference, network profile, OS profile
// with cloud-init bootstrap.
func linuxVM(vmStack *VirtualMachineStack) armcompute.VirtualMachine {
    return armcompute.VirtualMachine{
        Location: to.Ptr(vmStack.Location),
        Name:     to.Ptr(vmStack.name + "-vm"),
        Properties: &armcompute.VirtualMachineProperties{
            HardwareProfile: &armcompute.HardwareProfile{
                VMSize: to.Ptr(armcompute.VirtualMachineSizeTypesStandardD2SV3),
            },
            StorageProfile: &armcompute.StorageProfile{
                ImageReference: &armcompute.ImageReference{
                    Publisher: to.Ptr("Canonical"),
                    Offer:     to.Ptr("UbuntuServer"),
                    SKU:       to.Ptr("18.04-LTS"),
                    Version:   to.Ptr("latest"),
                },
            },
            NetworkProfile: networkProfile(vmStack),
            OSProfile:      linuxOSProfile(vmStack),
        },
    }
}

// cloud-init: install nginx + golang on first boot.
func linuxOSProfile(vmStack *VirtualMachineStack) *armcompute.OSProfile {
    sshKeyData := HandleErrWithResult(ioutil.ReadFile(vmStack.sshKeyPath))
    cloudInitContent := HandleErrWithResult(ioutil.ReadFile("./cloud-init/init.yml"))
    b64 := base64.StdEncoding.EncodeToString(cloudInitContent)
    return &armcompute.OSProfile{
        AdminUsername: to.Ptr("devops"),
        ComputerName:  to.Ptr(vmStack.name),
        CustomData:    to.Ptr(b64),
        LinuxConfiguration: &armcompute.LinuxConfiguration{
            DisablePasswordAuthentication: to.Ptr(true),
            SSH: &armcompute.SSHConfiguration{
                PublicKeys: []*armcompute.SSHPublicKey{{
                    Path:    to.Ptr("/home/devops/.ssh/authorized_keys"),
                    KeyData: to.Ptr(string(sshKeyData)),
                }},
            },
        },
    }
}
```
*Ref: Go_for_DevOps.md — "Building an Azure virtual machine"*

---

```go
// Data plane: upload blobs to Azure Storage and generate read-only SAS URIs.
func uploadBlobs(stack *mgmt.StorageStack) {
    serviceClient := stack.ServiceClient()
    containerClient, _ := serviceClient.NewContainerClient("jd-imgs")
    _, _ = containerClient.Create(context.Background(), nil)
    files, _ := ioutil.ReadDir("./blobs")
    for _, file := range files {
        blobClient, _ := containerClient.NewBlockBlobClient(file.Name())
        osFile, _ := os.Open(path.Join("./blobs", file.Name()))
        _ = blobClient.UploadFile(context.Background(), osFile, azblob.UploadOption{})
    }
}

func printSASUris(stack *mgmt.StorageStack) {
    serviceClient := stack.ServiceClient()
    containerClient, _ := serviceClient.NewContainerClient("jd-imgs")
    files, _ := ioutil.ReadDir("./blobs")
    now := time.Now().UTC()
    for _, file := range files {
        blobClient, _ := containerClient.NewBlockBlobClient(file.Name())
        sasQuery, _ := blobClient.GetSASToken(
            azblob.BlobSASPermissions{Read: true},
            now, now.Add(2*time.Hour),
        )
        fmt.Println(blobClient.URL() + "?" + sasQuery.Encode())
    }
}

// ServiceClient uses the storage account key (not AAD) for the data plane.
func (ss *StorageStack) ServiceClient() *azblob.ServiceClient {
    cred, _ := azblob.NewSharedKeyCredential(*ss.Account.Name, *ss.AccountKey.Value)
    blobURI := *ss.Account.Properties.PrimaryEndpoints.Blob
    client, _ := azblob.NewServiceClientWithSharedKey(blobURI, cred, nil)
    return client
}
```
*Ref: Go_for_DevOps.md — "Building an Azure Storage account" / "Using Azure Storage"*

---

```yaml
#cloud-config
package_upgrade: true
packages:
  - nginx
  - golang
runcmd:
  - echo "hello world"
```
*Ref: Go_for_DevOps.md — "Building an Azure virtual machine"*

---

### Designing for Chaos (Chapter 16)

**Principle:** Spectacular outages are caused by infrastructure tooling, not user code. Every workflow must have (a) overload prevention, (b) rate limiting, (c) idempotency, (d) a three-way submit handshake, (e) policy validation, and (f) an emergency stop.

**Do:**
- Wrap RPCs in circuit breakers (`gobreaker`) AND exponential backoff with jitter (`cenkalti/backoff`).
- Use buffered channels as concurrency limiters — never spawn unbounded goroutines.
- Make every workflow idempotent: check if the work is already done before doing it.
- Use a three-way handshake (Submit → record ID → Exec) so client crashes don't lose work.
- Build an emergency-stop system that defaults to **Stop** for unknown workflows.
- Keep policy engines simple — 80% coverage, no Turing-complete config languages.

**Don't:**
- Build retry loops without backoff — they amplify load during outages (AWS case study).
- Allow a single tool to affect all machines in all satellites at once (Google disk erase case study).
- Assume tools will integrate emergency stops voluntarily — centralize execution.

**Code:**
```go
// Circuit breaker wrapping an HTTP client (Sony gobreaker).
type HTTP struct {
    client *http.Client
    cb     *gobreaker.CircuitBreaker
}

func New(client *http.Client) *HTTP {
    return &HTTP{
        client: client,
        cb: gobreaker.NewCircuitBreaker(gobreaker.Settings{
            MaxRequests: 1,
            Interval:    30 * time.Second,
            Timeout:     10 * time.Second,
            ReadyToTrip: func(c gobreaker.Counts) bool {
                return c.ConsecutiveFailures > 5
            },
        }),
    }
}

func (h *HTTP) Get(req *http.Request) (*http.Response, error) {
    if _, ok := req.Context().Deadline(); !ok {
        return nil, fmt.Errorf("all requests must have a Context deadline set")
    }
    r, err := h.cb.Execute(func() (interface{}, error) {
        resp, err := h.client.Do(req)
        if err != nil {
            return nil, err
        }
        if resp.StatusCode != 200 {
            return nil, fmt.Errorf("non-200 response code")
        }
        return resp, nil
    })
    if err != nil {
        return nil, err
    }
    return r.(*http.Response), nil
}
```
*Ref: Go_for_DevOps.md — "Using circuit breakers"*

---

```go
// Exponential backoff with jitter honoring context cancellation.
func (h *HTTP) Get(req *http.Request) (*http.Response, error) {
    if _, ok := req.Context().Deadline(); !ok {
        return nil, fmt.Errorf("all requests must have a Context deadline set")
    }
    var resp *http.Response
    op := func() error {
        var err error
        resp, err = h.client.Do(req)
        if err != nil {
            return err
        }
        if resp.StatusCode != 200 {
            return fmt.Errorf("non-200 response code")
        }
        return nil
    }
    err := backoff.Retry(
        op,
        backoff.WithContext(backoff.NewExponentialBackOff(), req.Context()),
    )
    if err != nil {
        return nil, err
    }
    return resp, nil
}
```
*Ref: Go_for_DevOps.md — "Using backoff implementations"*

---

```go
// Channel-based concurrency limiter — at most req.Limit jobs in flight.
limit := make(chan struct{}, req.Limit)
wg := sync.WaitGroup{}
for _, block := range work.Blocks {
    for _, job := range block.Jobs {
        job := job // capture loop variable for goroutine
        limit <- struct{}{}
        wg.Add(1)
        go func() {
            defer wg.Done()
            defer func() { <-limit }()
            job()
        }()
    }
}
wg.Wait()
```
*Ref: Go_for_DevOps.md — "Channel-based rate limiter"*

---

```go
// Token bucket for pacing — refill incr tokens every interval up to size.
type bucket struct{ tokens chan struct{} }

func newBucket(size, incr int, interval time.Duration) *bucket {
    b := &bucket{tokens: make(chan struct{}, size)}
    go func() {
        for range time.Tick(interval) {
            for i := 0; i < incr; i++ {
                select {
                case b.tokens <- struct{}{}:
                default:
                    break
                }
            }
        }
    }()
    return b
}

func (b *bucket) token(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case b.tokens <- struct{}{}:
        return nil
    }
}
```
*Ref: Go_for_DevOps.md — "Token-bucket rate limiter"*

---

```go
// Idempotent file copy: short-circuit if the file already has the content.
func CopyToFile(content []byte, p string) error {
    if f, err := os.Open(p); err == nil {
        h0 := sha256.New()
        io.Copy(h0, f)
        h1 := sha256.New()
        h1.Write(content)
        if bytes.Equal(h0.Sum(nil), h1.Sum(nil)) {
            return nil
        }
    }
    return os.WriteFile(p, content, 0644)
}
```
*Ref: Go_for_DevOps.md — "Building idempotent workflows"*

---

```proto
// Three-way handshake workflow service: Submit returns ID without executing.
service Workflow {
  rpc Submit(WorkReq)   returns (WorkResp) {};
  rpc Exec(ExecReq)     returns (ExecResp) {};
  rpc Status(StatusReq) returns (StatusResp) {};
}

message WorkReq  { string name = 1; string desc = 2; repeated Block blocks = 3; }
message WorkResp { string id = 1; }
message Block    { string desc = 1; int32 rate_limit = 2; repeated Job jobs = 3; }
message Job      { string name = 1; map<string,string> args = 2; }
message ExecReq  { string id = 1; }
```
*Ref: Go_for_DevOps.md — "Using three-way handshakes to prevent workflow loss"*

---

```go
// Policy engine: concurrent evaluation, cancel-on-first-failure, no mutation of req.
type Settings interface{ Validate() error }
type Policy interface {
    Run(ctx context.Context, name string, req *pb.WorkReq, settings Settings) error
}

func Run(ctx context.Context, req *pb.WorkReq, args ...PolicyArgs) error {
    if len(args) == 0 {
        return nil
    }
    ctx, cancel := context.WithCancel(ctx)
    defer cancel()

    creq := proto.Clone(req).(*pb.WorkReq) // policies can't mutate the request

    runners := make([]func() error, 0, len(args))
    for _, arg := range args {
        r, ok := policies[arg.Name]
        if !ok {
            return fmt.Errorf("policy(%s) does not exist", arg.Name)
        }
        runners = append(runners, func() error {
            return r.Policy.Run(ctx, arg.Name, creq, arg.Settings)
        })
    }

    wg := sync.WaitGroup{}
    ch := make(chan error, 1)
    wg.Add(len(runners))
    for _, r := range runners {
        r := r
        go func() {
            defer wg.Done()
            if err := r(); err != nil {
                select {
                case ch <- err:
                    cancel()
                default:
                }
            }
        }()
    }
    wg.Wait()

    select {
    case err := <-ch:
        return err
    default:
    }
    if !proto.Equal(req, creq) {
        return fmt.Errorf("a policy tried to modify a request: security violation")
    }
    return nil
}

// restrictJobTypes policy: only allow named jobs in a WorkReq.
type Settings struct{ AllowedJobs []string }

func (s Settings) Validate() error {
    for _, n := range s.AllowedJobs {
        if _, err := jobs.GetJob(n); err != nil {
            return fmt.Errorf("allowed job(%s) is not defined", n)
        }
    }
    return nil
}

type Policy struct{}

func (p Policy) Run(ctx context.Context, name string, req *pb.WorkReq, settings policy.Settings) error {
    s, ok := settings.(Settings)
    if !ok {
        return fmt.Errorf("settings were not valid")
    }
    for blockNum, block := range req.Blocks {
        for jobNum, job := range block.Jobs {
            if ctx.Err() != nil {
                return ctx.Err()
            }
            if !s.allowed(job.Name) {
                return fmt.Errorf("policy(%s): block(%d)/job(%d) type(%s) not allowed",
                    name, blockNum, jobNum, job.Name)
            }
        }
    }
    return nil
}
```
*Ref: Go_for_DevOps.md — "Creating a policy engine" / "Writing a policy"*

---

```go
// Emergency-stop: default-deny (anything not explicitly "go" is "stop").
type Status string

const (
    Unknown Status = ""
    Go      Status = "go"
    Stop    Status = "stop"
)

type Info struct {
    Name   string
    Status Status
}

type Reader struct {
    entries     atomic.Value // map[string]Info
    mu          sync.Mutex
    subscribers map[string][]chan Status
}

// Usage: subscribe before Exec; cancel the context on any non-Go signal.
func (w *work) Exec(ctx context.Context) error {
    esCh, cancelES := es.Data.Subscribe(w.name)
    defer cancelES()
    if <-esCh != es.Go {
        return fmt.Errorf("es in Stop state")
    }
    ctx, cancel := context.WithCancel(ctx)
    defer cancel()
    go func() {
        select {
        case <-ctx.Done():
            return
        case <-esCh:
            cancel()
        }
    }()
    for _, job := range w.jobs {
        if err := job(ctx); err != nil {
            return err
        }
    }
    return nil
}
```
*Ref: Go_for_DevOps.md — "Building an emergency-stop package" / "Using the emergency-stop package"*

---

## Anti-Patterns & Common Mistakes

- **Loop-variable capture in goroutines:** `for _, x := range xs { go func() { use(x) }() }` — every goroutine sees the last `x`. Fix: `x := x` before the `go` statement.
- **No backoff on retries:** An internal service slows down → clients retry immediately → service dies → clients retry harder (the AWS us-east-1 cascade). Fix: `cenkalti/backoff` with jitter.
- **No rate limiting on automation:** Google's satellite disk erase wiped every satellite because the tool filtered twice removed the safety filter. Fix: centralized executor with token-bucket pacing.
- **Tools that don't honor context cancellation:** Google's Chipmunk spent 24 minutes per canceled request burning CPU under Python's GIL, cascading to a death spiral. Fix: thread `context.Context` everywhere, check `ctx.Err()` at loop tops.
- **Mixing pointer and value receivers:** `func (r Record) Foo()` and `func (r *Record) Bar()` on the same type — pick one and be consistent.
- **Decoding JSON into `map[string]interface{}`:** loses type safety, requires type switches everywhere. Decode into a struct.
- **`ssh.InsecureIgnoreHostKey()` in production:** enables MITM. Maintain a known-hosts list.
- **Building Terraform state only locally:** team members drift; corrupts on concurrent `apply`. Use remote state with locking.
- **Default-Allow emergency stop:** if the rule list doesn't mention your tool, you proceed — a single missing rule disables the safety net. Default to **Stop**.
- **`panic` outside `main`:** one bad request kills the whole server. Return errors; reserve `panic` for unrecoverable startup.
- **Reading entire files into memory:** a 2 GiB log will OOM your pod. Stream with `bufio.Scanner` / `io.Copy`.

## Decision Heuristics / Checklists

- **`database/sql` vs native driver (pgx):** Use `database/sql` when you might swap databases; use `pgx` directly when you need Postgres-specific types (jsonb, arrays) or higher throughput.
- **REST vs gRPC for internal services:** gRPC wins on perf, schema, streaming, and code generation. Use REST only for browser-facing or third-party APIs.
- **When to write a Kubernetes Operator:** if you have a runbook that a human follows repeatedly, encode it as a controller — Kubernetes gives you reconciliation, leader election, and CRDs for free.
- **When to use Packer vs Docker:** Packer for VMs/AMI/cloud images; Docker for container images. Both produce immutable artifacts that should be validated by Goss / health checks before publishing.
- **Channel vs mutex:** channel to *pass ownership* of data between goroutines; mutex to *protect shared access* to a value. Don't mix.
- **Concurrency checklist before shipping:**
  - [ ] Bounded goroutines (channel limiter or worker pool)?
  - [ ] `context.Context` plumbed through every I/O call?
  - [ ] No loop-variable capture bug?
  - [ ] `WaitGroup.Add` called *outside* the goroutine?
  - [ ] Channel `close` always called by the sender?
  - [ ] Retry loop has exponential backoff + jitter + max attempts?
  - [ ] Operation is idempotent under re-execution?
- **GitHub Actions security checklist:**
  - [ ] `pull_request` trigger doesn't expose secrets to untrusted PRs (use `pull_request_target` or a `safe-to-test` label gate).
  - [ ] Action versions pinned to a SHA or floating major (`@v1`).
  - [ ] `GITHUB_TOKEN` scoped with `permissions:` block (least privilege).
- **Workflow safety checklist (Chapter 16):**
  - [ ] Three-way handshake (Submit → record ID → Exec)?
  - [ ] Pre-condition checks (global + local) before any mutation?
  - [ ] Canary stage before general rollout?
  - [ ] Max-failure circuit breaker + concurrency cap?
  - [ ] Policy engine restricts job types and scope?
  - [ ] Emergency-stop integration with default-Stop?
  - [ ] Idempotent actions (re-running produces the same result)?

## Key Takeaways

1. **Go is the lingua franca of cloud infrastructure.** Kubernetes, Docker, Terraform, Packer, Prometheus, Jaeger, OTel Collector — all written in Go. Knowing Go gives you the source code to every tool you operate.
2. **Errors are values, not exceptions.** Every function that can fail returns an error; wrap with `%w`, inspect with `errors.Is`/`errors.As`. This discipline catches failure modes that exceptions hide.
3. **`context.Context` is non-negotiable.** Thread it as the first argument through every I/O function; check `ctx.Err()` at logical points. The Chipmunk case study shows what happens when you don't.
4. **Standardize on gRPC + protocol buffers internally.** Strong typing, 10x JSON performance, generated clients in every language, native streaming, and built-in cancellation/deadlines.
5. **Abstract storage behind interfaces.** The Google Bigtable→Spanner migration succeeded with zero downtime because storage was hidden behind an interface; the new dual-write backend was swapped in transparently.
6. **Observability is a feature, not an afterthought.** Logs + traces + metrics, all correlated via `trace_id`/`span_id`. Without them, the 3 A.M. outage is a nightmare; with them, it's a 5-minute fix.
7. **Idempotency enables recovery.** Every workflow action must be safe to re-run. Three-way handshakes (Submit → record ID → Exec) prevent lost work when clients crash.
8. **Centralize execution of dangerous tooling.** Google's backbone emergency stop worked *because* every tool ran through one service. Distributed tools = distributed accidents.
9. **Default-deny emergency stops.** Any tool not explicitly "Go" is "Stop" — this closed the gap where new tools forgot to integrate the stop package.
10. **Keep policy engines dumb.** Cover the critical 80% with simple checks. The moment your policy config looks like a programming language, you've built a Turing-tarpit that nobody understands.

## Cross-References

- Related: [[../go_in_practice.md]] · [[../programming_go.md]] · [[../concurrency_in_go.md]] · [[../kubernetes_patterns.md]] · [[../site_reliability_engineering.md]]
- Topic index: [[../INDEX.md]]
