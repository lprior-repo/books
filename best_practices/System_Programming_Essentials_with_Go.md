# System Programming Essentials with Go
**Author:** Alex Rios
**Topic tags:** `#systems` `#cli` `#go` `#concurrency` `#performance` `#observability` `#networking` `#ipc`
**Language focus:** Go-first
**Sources:** `markdown_output/System_Programming_Essentials_with_Go_-_Alex_Rios/System_Programming_Essentials_with_Go_-_Alex_Rios.md` · `summaries/System_Programming_Essentials_with_Go_-_Alex_Rios.md`

## TL;DR
A modern (2024) systems-programming-with-Go guide that goes deeper than the basics: system calls, file/directory operations, signals, inotify, anonymous/named pipes, Unix domain sockets, GC tuning (`GOGC`/`GOMEMLIMIT`/ballast/arenas), escape analysis, benchmarking, profiling, TCP/UDP/QUIC, OpenTelemetry telemetry, distribution (`golangci-lint`, GoReleaser), resource pooling (`sync.Pool`, `sync.Once`, `singleflight`, `mmap`), and a capstone distributed cache with replication and consistent hashing. Distinctive: Functional Options for testable CLIs, plus heavy emphasis on measurement before optimization.

---

## Best Practices by Topic

### Testable CLIs with Functional Options  `#cli` `#testing`

**Principle:** Decouple your CLI's I/O streams from `os.Stdout`/`os.Stderr` via a config struct built with variadic option functions — tests then inject `bytes.Buffer` writers.

**Do:**
- Define `type Option func(*CliConfig) error` and helpers `WithOutStream(io.Writer)`, `WithErrStream(io.Writer)`.
- Default streams to `os.Stdout`/`os.Stderr` in the constructor.
- Accept `opts ...Option` so call sites read like prose: `NewCliConfig(WithOutStream(&buf))`.
- Keep business logic in a free function `app(args, cfg)` that main and tests both call.

**Don't:**
- Hardcode `fmt.Println` in business logic — you can't capture it in tests.
- Stuff every option into a positional constructor (explodes signatures over time).

**Code** — Functional Options pattern:
```go
type Option func(*CliConfig) error

func WithErrStream(errStream io.Writer) Option {
    return func(c *CliConfig) error { c.ErrStream = errStream; return nil }
}
func WithOutStream(outStream io.Writer) Option {
    return func(c *CliConfig) error { c.OutStream = outStream; return nil }
}

func NewCliConfig(opts ...Option) (CliConfig, error) {
    c := CliConfig{
        ErrStream: os.Stderr,
        OutStream: os.Stdout,
    }
    for _, opt := range opts {
        if err := opt(&c); err != nil {
            return CliConfig{}, err
        }
    }
    return c, nil
}
```
*Ref: System_Programming_Essentials_with_Go.md — "Functional Options"*

**Code** — capturing output in a test:
```go
func TestMainProgram(t *testing.T) {
    var stdoutBuf, stderrBuf bytes.Buffer
    config, err := NewCliConfig(WithOutStream(&stdoutBuf), WithErrStream(&stderrBuf))
    if err != nil { t.Fatal("Error creating config:", err) }
    app([]string{"main", "alex", "golang", "error"}, config)
    // assert on stdoutBuf.String() / stderrBuf.String()
}
```
*Ref: System_Programming_Essentials_with_Go.md — "Testing"*

**Code** — MultiWriter for tee-ing output to file + stdout:
```go
var outputWriter io.Writer
if cfg.OutputFile != "" {
    outputFile, err := os.Create(cfg.OutputFile)
    if err != nil { /* ... */ }
    defer outputFile.Close()
    outputWriter = io.MultiWriter(cfg.OutStream, outputFile)
} else {
    outputWriter = cfg.OutStream
}
```
*Ref: System_Programming_Essentials_with_Go.md — "File and Directory Operations"*

---

### System Calls & Standard Streams  `#systems`

**Principle:** Know your three syscall layers in Go: `os` (portable, high-level), `syscall` (version-locked, low-level), and `golang.org/x/sys/unix` (maintained, low-level). Standard streams are fds 0/1/2.

**Do:**
- Default to `os` for portable code; reach for `golang.org/x/sys/unix` when you need specific syscalls maintained across Go versions.
- Use `strace -e trace=open,read,write ./prog` to see what your program really asks the kernel.
- Treat `os.Stdin`/`os.Stdout`/`os.Stderr` as the CLI's primary I/O surface.

*Ref: System_Programming_Essentials_with_Go.md — "Understanding System Calls"*

---

### Filesystem: Permissions, WalkDir, Symlinks  `#systems` `#io`

**Principle:** Use `filepath.WalkDir` (not `Walk`) for efficiency — it gives you `fs.DirEntry` so you avoid an `os.Stat` per entry. Default to restrictive permissions.

**Do:**
- `filepath.Join` for portable path construction (correct separator per OS).
- `filepath.WalkDir(root, fn)` with `fn(path, d fs.DirEntry, err error) error`; return `filepath.SkipDir` to prune subtrees (e.g. `.git`).
- Use `d.IsDir()` and `d.Info()` to avoid extra syscalls.
- Detect insecure permissions: flag `0777` and world-writable files (`mode&0002 != 0`).
- Use `os.Symlink`/`os.Readlink`; watch for cycles and dangling links.
- `os.Remove` deletes a file; `os.RemoveAll` deletes a tree — validate paths first (irreversible).

**Don't:**
- Use `filepath.Walk` in new code — `WalkDir` is more efficient.
- Skip error handling in the walk callback — busy filesystems change between calls.

**Code** — `WalkDir` with `.git` pruning and multi-writer output:
```go
for _, directory := range directories {
    err := filepath.WalkDir(directory, func(path string, d os.DirEntry, err error) error {
        if path == ".git" {
            return filepath.SkipDir
        }
        if d.IsDir() {
            fmt.Fprintf(outputWriter, "%s\n", path)
        }
        return nil
    })
    if err != nil {
        fmt.Fprintf(cfg.ErrStream, "Error walking the path %q: %v\n", directory, err)
        continue
    }
}
```
*Ref: System_Programming_Essentials_with_Go.md — "File and Directory Operations"*

---

### Signals, Timers, fsnotify  `#systems` `#processes`

**Principle:** Capture signals through a buffered channel + `signal.Notify` + a consumer goroutine; pair with `time.Timer`/`time.Ticker` for scheduling and `fsnotify` for portable file-event watching.

**Do:**
- Always buffer the signal channel: `make(chan os.Signal, 1)`.
- Use a separate `done` channel (`chan struct{}`) so the main goroutine can block until shutdown completes.
- Handle SIGINT/SIGTERM for graceful shutdown: close listeners, flush buffers, remove socket files.
- Use `time.Timer` for one-shot delays, `time.Ticker` for repeating intervals, `time.AfterFunc` when you don't need a channel.
- Use `github.com/fsnotify/fsnotify` for cross-platform file-event watching (abstracts inotify/kqueue/ReadDirectoryChangesW).

**Don't:**
- Block the signal-handling goroutine on slow work — forward to a worker.
- Forget to clean up the Unix socket file before `net.Listen("unix", path)`.

**Code** — graceful shutdown via signal + done channel:
```go
signals := make(chan os.Signal, 1)
done := make(chan struct{}, 1)
signal.Notify(signals, os.Interrupt)

go func() {
    for {
        s := <-signals
        switch s {
        case os.Interrupt:
            fmt.Println("INTERRUPT")
            done <- struct{}{}
        default:
            fmt.Println("OTHER")
        }
    }
}()

fmt.Println("awaiting signal")
<-done
fmt.Println("exiting")
```
*Ref: System_Programming_Essentials_with_Go.md — "Signals"*

**Code** — fsnotify watcher:
```go
watcher, err := fsnotify.NewWatcher()
// ...
go func() {
    for {
        select {
        case event, ok := <-watcher.Events:
            if !ok { return }
            if event.Op&fsnotify.Write == fsnotify.Write {
                // handle write (e.g., log rotation trigger)
            }
        case err, ok := <-watcher.Errors:
            if !ok { return }
            // handle watcher error
        }
    }
}()
watcher.Add(logFilePath)
```
*Ref: System_Programming_Essentials_with_Go.md — "fsnotify"*

---

### Inter-Process Communication: Pipes  `#systems` `#ipc`

**Principle:** Anonymous pipes (`os.Pipe`) connect related processes; named pipes/FIFOs (`unix.Mkfifo`) connect unrelated processes via a filesystem entry.

**Do:**
- Always `defer close` on pipe file descriptors.
- Chunk large writes to avoid buffer overflow; compress with `compress/gzip` to reduce pipe volume.
- Use context-based timeouts on reads to prevent deadlocks.
- Secure named pipes with restrictive permissions (`0600`) and randomized names to prevent name-squatting.
- Use a sentinel value (e.g. `"EOD"`) on a named pipe to signal end-of-stream cleanly.
- Pair producer/consumer goroutines with a `sync.WaitGroup`.

**Don't:**
- Hold a pipe open indefinitely without a close path.

*Ref: System_Programming_Essentials_with_Go.md — "Understanding Pipes in Inter-Process Communication"*

---

### Unix Domain Sockets  `#systems` `#networking` `#ipc`

**Principle:** Same-machine IPC via filesystem-node sockets — lower latency than TCP, with file-permission-based access control.

**Do:**
- Server: `net.Listen("unix", socketPath)`; `os.Remove(socketPath)` before bind to avoid "address in use".
- Accept in a loop; handle each connection in its own goroutine.
- Intercept SIGINT/SIGTERM to close the listener and remove the socket file.
- Serve HTTP over a Unix socket: `http.Serve(listener, nil)` after `net.Listen("unix", ...)`.
- For multi-client systems (e.g., chat), protect the client list with a mutex and broadcast to all connected clients.

**Don't:**
- Forget to clean up the socket file on graceful shutdown.

*Ref: System_Programming_Essentials_with_Go.md — "Unix Sockets"*

---

### Concurrency: Goroutines, Sync Primitives, Channels  `#concurrency`

**Principle:** Match the primitive to the job — atomics for counters/flags, mutexes for multi-variable critical sections, channels for cross-goroutine communication, `select` for multiplexing.

**Do:**
- `sync.WaitGroup`: `Add(n)` before spawn, `defer Done()` inside, `Wait()` in main — eliminates the unreliability of `time.Sleep`.
- `sync.Mutex` for write-heavy shared state; `sync.RWMutex` for read-heavy (multiple `RLock`/`RUnlock` readers, one `Lock`/`Unlock` writer).
- `sync/atomic` for single-variable counters (`atomic.AddInt32`, etc.).
- Unbuffered channels (`make(chan T)`) for synchronous handoff; buffered (`make(chan T, n)`) for burst absorption.
- `select` to wait on multiple channels; pair with `time.After` for timeouts.
- Pass loop variables as parameters to goroutines to avoid the classic data race.

**Don't:**
- Capture loop variables by reference in goroutines.
- Mix "share state" and "communicate" models ad hoc — pick per data structure.

*Ref: System_Programming_Essentials_with_Go.md — "Refreshing Concurrency and Parallelism"*

**Code** — WaitGroup with two goroutines:
```go
var wg sync.WaitGroup
wg.Add(2)
go say("hello", &wg)
go say("world", &wg)
wg.Wait()
fmt.Println("Both goroutines have finished.")
```
*Ref: System_Programming_Essentials_with_Go.md — "Goroutines and WaitGroups"*

---

### Memory Management: GC, GOGC, GOMEMLIMIT, Ballast, Arenas  `#systems` `#performance`

**Principle:** Go's concurrent tri-color mark-and-sweep targets low STW latency. Tune via `GOGC` (trigger threshold), `GOMEMLIMIT` (soft ceiling, Go 1.19+), or experimental arenas (Go 1.20+, `GOEXPERIMENT=arenas`). Don't reach for memory ballast or arenas until you've measured.

**Do:**
- Use `GODEBUG=gctrace=1` to see per-cycle STW times, heap sizes, CPU costs.
- Prefer `GOMEMLIMIT` (env var or `runtime/debug.SetMemoryLimit`) over manual memory ballast for Go ≥ 1.19 — they're redundant together.
- Lower `GOGC` (e.g. 50) for smaller heap + more CPU; raise it (e.g. 200) for less frequent GC.
- Use `go run -asan` to detect arena use-after-free.
- Understand escape analysis (`-gcflags "-m -m"`) — references that outlive their stack frame escape to the heap.

**Don't:**
- Use memory ballast (`make([]byte, 10<<30)`) on Go ≥ 1.20 without measuring — `GOMEMLIMIT` is the standardized replacement.
- Reach for memory arenas as a premature optimization — first try GC/GOMEMLIMIT combinations.

**Code** — Twitch-style memory ballast (legacy technique):
```go
ballast := make([]byte, 10<<30) // 10 GiB virtual; influences GC pacing
// Reported: ~99% reduction in GC cycles, ~30% CPU reduction, ~45% p99 latency
```
*Ref: System_Programming_Essentials_with_Go.md — "Memory ballast"*

| Knob          | Effect                                                   | Default            |
|---------------|----------------------------------------------------------|--------------------|
| `GOGC=100`    | GC when heap reaches 2× live heap after last cycle       | 100                |
| `GOGC=50`     | Smaller heap, more CPU                                                                   |
| `GOGC=200`    | Larger heap, less frequent GC                                                            |
| `GOGC=off`    | Disable GC (use only for very short-lived programs)                                      |
| `GOMEMLIMIT`  | Soft memory ceiling (B/KiB/MiB/GiB/TiB); Go 1.19+        | `math.MaxInt64`    |

*Ref: System_Programming_Essentials_with_Go.md — "GOGC" / "GOMEMLIMIT"*

---

### Performance: Benchmarking & Profiling  `#performance` `#testing`

**Principle:** Measure, don't guess. Use `go test -bench`, `pprof`, and `benchstat` to drive optimization; understand the six common benchmark pitfalls.

**Do:**
- Benchmark signature: `func BenchmarkXxx(b *testing.B) { for n := 0; n < b.N; n++ { ... } }`.
- Use `b.ResetTimer()` after expensive setup; `b.Run(name, ...)` for parameterized sub-benchmarks.
- Add `-benchmem` for bytes/allocs per op; compare runs with `benchstat` for delta, p-value, CI.
- CPU profile: `pprof.StartCPUProfile(f)` / `pprof.StopCPUProfile()`; analyze via `go tool pprof -web cpuprofile.out`.
- Memory profile: `runtime/pprof.WriteHeapProfile(f)`.
- Consume benchmark results so the compiler doesn't optimize them away.

**Don't:**
- Benchmark the wrong thing (e.g. sorting already-sorted data).
- Misuse `b.N` (the framework sets it — don't feed it as input).
- Ignore GC impact on allocation-heavy benchmarks.
- Compare benchmarks across non-representative environments.

*Ref: System_Programming_Essentials_with_Go.md — "Analyzing Performance"*

---

### Resource Pooling: sync.Pool, sync.Once, singleflight, mmap  `#concurrency` `#performance`

**Principle:** Reuse short-lived objects to cut GC pressure, deduplicate concurrent expensive calls, and bypass `read`/`write` syscalls for large files via `mmap`.

**Do:**
- `sync.Pool`: wrap `bytes.Buffer` (or other reusable objects) with a `BufferPool` struct; `Reset()` before `Put`; copy data out before returning to pool.
- `sync.Once` for one-time init; prefer `sync.OnceFunc`/`sync.OnceValue`/`sync.OnceValues` (Go 1.21+) for less boilerplate.
- `golang.org/x/sync/singleflight.Group` for deduplicating concurrent calls by key (DB queries, API calls, throttling, background tasks).
- `golang.org/x/exp/mmap` for read-heavy large-file workloads (`mmap.Open` → `ReaderAt`).

**Don't:**
- Trust pooled objects to persist — the GC may reclaim them at any cycle.
- Hold large pools in memory-constrained containers.
- Return a buffer to the pool and then keep reading/writing it — data corruption.

**Code** — `BufferPool` over `sync.Pool`:
```go
type BufferPool struct { pool sync.Pool }

func NewBufferPool() *BufferPool {
    return &BufferPool{
        pool: sync.Pool{
            New: func() interface{} { return new(bytes.Buffer) },
        },
    }
}

func (bp *BufferPool) Get() *bytes.Buffer { return bp.pool.Get().(*bytes.Buffer) }

func (bp *BufferPool) Put(buf *bytes.Buffer) {
    buf.Reset()            // critical: avoid leftover data corruption
    bp.pool.Put(buf)
}

func ProcessData(data []byte, bp *BufferPool) {
    buf := bp.Get()
    defer bp.Put(buf)      // ensure return even on panic
    buf.Write(data)
    fmt.Println(buf.String())
}
```
*Ref: System_Programming_Essentials_with_Go.md — "sync.Pool"*

**Code** — pooled buffers in a TCP server:
```go
var bufferPool = sync.Pool{
    New: func() interface{} { return make([]byte, 1024) },
}

func handleConnection(conn net.Conn) {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf)
    for {
        n, err := conn.Read(buf)
        if err != nil { if err != io.EOF { println("Error reading:", err.Error()) }; break }
        conn.Write(buf[:n])
    }
    conn.Close()
}
```
*Ref: System_Programming_Essentials_with_Go.md — "Using sync.Pool in a network server"*

**Code** — `singleflight.Group` deduplicating concurrent calls:
```go
var g singleflight.Group
var wg sync.WaitGroup

fetchData := func(key string) (interface{}, error) {
    time.Sleep(2 * time.Second)
    return fmt.Sprintf("Data for key %s", key), nil
}

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(i int) {
        defer wg.Done()
        result, err, shared := g.Do("my_key", func() (interface{}, error) {
            return fetchData("my_key")
        })
        if err != nil { fmt.Printf("Error: %v\n", err); return }
        fmt.Printf("Goroutine %d got result: %v (shared: %v)\n", i, result, shared)
    }(i)
}
wg.Wait()
// fetchData executes exactly once; all 5 goroutines share the result.
```
*Ref: System_Programming_Essentials_with_Go.md — "singleflight"*

---

### Telemetry: Logs, Traces, Metrics, OpenTelemetry  `#observability`

**Principle:** Three pillars of observability — structured logs (slog/zap/log), distributed traces (spans), metrics (counters/gauges/histograms/summaries). Use OpenTelemetry for vendor-neutral instrumentation.

**Do:**
- Prefer `slog` (stdlib since Go 1.21) or `zap` (high-performance) for structured key-value logs.
- Log who/what/when/where/why; never log passwords, tokens, or PII.
- Use log levels: DEBUG, INFO, WARN, ERROR.
- Pick metrics by methodology: **RED** (Rate, Errors, Duration) for services; **USE** (Utilization, Saturation, Errors) for resources.
- Capture p50/p95/p99 latency, error rates, throughput, CPU/mem/connections.
- OTel: install packages, configure OTLP exporter, init tracer provider, wrap operations in spans with attributes.

*Ref: System_Programming_Essentials_with_Go.md — "Telemetry"*

---

### Networking: TCP, UDP, QUIC, TLS, HTTP  `#networking`

**Principle:** Unified `net.Listen`/`net.Dial` API spans TCP/UDP/Unix sockets. Add TLS for security; consider QUIC for connection-migration, 0-RTT, and multiplexed streams without head-of-line blocking.

**Do:**
- Concurrent TCP server: `for { c, _ := l.Accept(); go handleConnection(c) }`.
- UDP: `ListenUDP` + `ReadFromUDP`/`WriteToUDP` — no `Accept`.
- Production HTTP: set `http.Client{Timeout: ...}` and `http.Transport{MaxIdleConns: ...}` for pooling.
- TLS: serve with `http.ListenAndServeTLS(cert, key)`; load system CAs for prod; restrict TLS versions and cipher suites.
- Use context for cancellation and per-request deadlines.

**Don't:**
- Use plain `http.Get` without a timeout in production.
- Forget connection pooling for high-throughput HTTP clients.

*Ref: System_Programming_Essentials_with_Go.md — "Networking"*

---

### Distribution: Modules, CI, Static Analysis, GoReleaser  `#distribution` `#cli`

**Principle:** `go mod` for deps, GitHub Actions for CI (lint + test + build + publish), `golangci-lint` for static analysis, GoReleaser for cross-platform releases + Docker images + changelog.

**Do:**
- `go mod init`/`go get`/`go mod tidy`; commit `go.sum` for reproducible builds; `go mod vendor` for offline builds.
- CI: matrix builds across Go versions; cache `~/.cache/go-build` and module downloads; enforce coverage thresholds.
- Lint with `golangci-lint` (aggregates `go vet`, `staticcheck`, etc.); wire into pre-commit hooks.
- GoReleaser: multi-GOOS/GOARCH binaries, GitHub Release, container image, auto changelog.

*Ref: System_Programming_Essentials_with_Go.md — "Distributing Your Apps"*

---

### Capstone: Distributed Cache Design Trade-offs  `#systems` `#concurrency` `#architecture`

**Principle:** The capstone forces you to make every systems decision explicitly and own the trade-offs.

**Do:**
- **Interface**: HTTP (simple, debuggable) vs. TCP (lower latency) — chosen: HTTP.
- **Thread safety**: `sync.RWMutex` (read-heavy cache) — `RLock`/`RUnlock` for `Get`, `Lock`/`Unlock` for `Set`.
- **Eviction**: LRU via `container/list` (doubly-linked) + map; TTL via background goroutine + `time.Ticker` (proactive beats on-demand for read latency).
- **Replication**: P2P over primary-replica/pub-sub/consensus — chosen: P2P for no SPOF. Use a custom header (`X-Replication-Request`) to prevent infinite replication loops.
- **Sharding**: consistent hashing (SHA-1 ring + binary search) over range/hash-based — minimizes redistribution on join/leave. Use `X-Forwarded-For` to prevent forwarding loops.

**Code** — thread-safe cache with `RWMutex`:
```go
type Cache struct {
    mu    sync.RWMutex
    items map[string]Item
}
// Get: RLock / RUnlock
// Set: Lock / Unlock
```
*Ref: System_Programming_Essentials_with_Go.md — "Thread Safety"*

**Code** — consistent hashing `HashRing`:
```go
type Node struct { ID, Addr string }

type HashRing struct {
    nodes  []Node
    hashes []uint32       // sorted, for binary search
    lock   sync.RWMutex
}

// AddNode: hash ID, insert, keep sorted
// GetNode(key): binary search for first hash >= hash(key)
// hash(): SHA-1 of node ID or key
```
*Ref: System_Programming_Essentials_with_Go.md — "Implementing consistent hashing"*

**Code** — replication-aware `SetHandler`:
```go
const replicationHeader = "X-Replication-Request"

func (cs *CacheServer) SetHandler(w http.ResponseWriter, r *http.Request) {
    var req struct{ Key, Value string }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest); return
    }
    targetNode := cs.hashRing.GetNode(req.Key)
    if targetNode.Addr == "self" {
        cs.cache.Set(req.Key, req.Value, 1*time.Hour)
        if r.Header.Get(replicationHeader) == "" {
            // replicate to peers (only on client-originated requests)
        }
    } else {
        // forward to targetNode with X-Forwarded-For to prevent loops
    }
}
```
*Ref: System_Programming_Essentials_with_Go.md — "Sharding with Consistent Hashing"*

---

## Anti-Patterns & Common Mistakes

- **Untestable CLI with hardcoded `fmt.Println`** in business logic. → *fix:* Functional Options with injectable `io.Writer`.
- **`filepath.Walk` in new code** — extra `os.Stat` per entry. → *fix:* `filepath.WalkDir` + `DirEntry.Info()`.
- **Unbuffered signal channel** — can drop signals under load. → *fix:* `make(chan os.Signal, 1)` (or larger).
- **No `os.Remove(socketPath)` before `net.Listen("unix", ...)`** — "address already in use".
- **Leaving pipe fds open** — deadlock or resource leak. → *fix:* `defer close`.
- **Named pipe without `0600` perms / random name** — name-squatting / snooping attacks.
- **Memory ballast on Go ≥ 1.20** — superseded by `GOMEMLIMIT`. → *fix:* `runtime/debug.SetMemoryLimit`.
- **`sync.Pool` without `Reset()`** — stale bytes corrupt next user.
- **Returning a buffer to the pool then continuing to use it** — silent data corruption.
- **`http.Get` with no client timeout** — hung requests in production.
- **Single-client TCP server (no goroutine per connection)** — fails under concurrent load.
- **Capturing loop variables in goroutines by reference** — classic data race.
- **Benchmarking the wrong thing / not consuming results** — compiler eliminates dead code, numbers lie.
- **Reaching for memory arenas prematurely** — try GC/GOMEMLIMIT first.
- **Mixing ballast + GOMEMLIMIT** — redundant; "wearing two watches".

---

## Decision Heuristics / Checklists

### Sync primitive chooser
| Need                                  | Primitive                       |
|---------------------------------------|---------------------------------|
| Wait for N goroutines                 | `sync.WaitGroup`                |
| Counter / flag                        | `sync/atomic`                   |
| Multi-variable critical section        | `sync.Mutex`                    |
| Read-heavy shared state               | `sync.RWMutex`                  |
| Cross-goroutine data handoff           | channel (unbuffered = sync)     |
| Burst absorption                      | channel (buffered)              |
| Multiplex channel ops / timeout        | `select` + `time.After`         |
| One-time init                         | `sync.Once` / `OnceValue`       |
| Deduplicate concurrent calls by key   | `singleflight.Group`            |
| Reuse short-lived objects             | `sync.Pool`                     |

### GC tuning checklist
- [ ] `GODEBUG=gctrace=1` captured under realistic load.
- [ ] Tried `GOGC` 50 / 100 / 200 first.
- [ ] Set `GOMEMLIMIT` (Go ≥ 1.19) before reaching for ballast.
- [ ] Only then consider arenas (Go 1.20+ experimental) with `-asan`.
- [ ] Verified with `benchstat` that the change actually improves things.

### IPC chooser
- Parent ↔ child only → anonymous pipe (`os.Pipe`).
- Unrelated processes, same host → named pipe (FIFO) or **Unix domain socket** (preferred for request/response).
- Cross-host → TCP/UDP/QUIC.

### Distributed-cache decision matrix
| Decision               | Options                                       | Default choice            |
|------------------------|-----------------------------------------------|---------------------------|
| Interface              | HTTP vs TCP                                   | HTTP (debuggability)      |
| Thread safety          | Mutex vs channel vs RWMutex                   | RWMutex (read-heavy)      |
| Eviction               | LRU vs TTL vs FIFO                            | LRU + TTL (proactive)     |
| Replication            | Primary-replica vs P2P vs pub/sub vs Raft     | P2P (no SPOF)             |
| Sharding               | Range vs hash vs consistent hashing           | Consistent hashing        |

---

## Key Takeaways

1. **Go is uniquely positioned for systems programming** — C-level performance with GC, built-in concurrency, and a minimal cross-platform toolchain.
2. **Functional Options make CLIs testable** — inject `io.Writer` for stdout/stderr; main and tests share one `app(args, cfg)`.
3. **Three syscall layers** — `os` (portable), `syscall` (locked), `golang.org/x/sys` (maintained low-level).
4. **`filepath.WalkDir` over `Walk`** — fewer syscalls, same API shape.
5. **Graceful shutdown via signals** — buffered channel + `signal.Notify` + `done` channel; clean up listeners/sockets.
6. **IPC ladder** — pipes (parent/child) → named pipes (unrelated) → Unix sockets (efficient local) → TCP/UDP/QUIC (distributed).
7. **GC knobs in order** — `GODEBUG=gctrace=1` → `GOGC` → `GOMEMLIMIT` → ballast/arenas (last resort).
8. **Performance is measured** — `go test -bench` + `-benchmem` + `benchstat`; CPU/memory via `pprof`; watch the six benchmark pitfalls.
9. **Resource reuse cuts GC pressure** — `sync.Pool`, `sync.Once`/`OnceValue`, `singleflight`, `mmap`.
10. **Observability is non-negotiable** — structured logs + traces + metrics; OpenTelemetry for vendor-neutral instrumentation.
11. **Production HTTP needs timeouts and pooling** — `http.Client{Timeout}`, `Transport.MaxIdleConns`, context-based cancellation.
12. **Every distributed-system choice is a trade-off** — the capstone cache forces explicit decisions on interface, locking, eviction, replication, and sharding, each with named alternatives.
13. **Distribution is automated end-to-end** — modules → CI (lint/test/build) → `golangci-lint` → GoReleaser for cross-platform binaries + Docker images + changelog.
14. **Real-world validation** — Docker, Kubernetes, HashiCorp (Terraform/Consul/Vault), Grafana Labs all picked Go for infrastructure at scale.

---

## Cross-References
- Related: [[../Building_Modern_CLI_Applications_in_Go.md]]
- Related: [[../Go_Systems_Programming.md]]
- Topic index: [[../INDEX.md]]
