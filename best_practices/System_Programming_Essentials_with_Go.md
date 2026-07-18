# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# System Programming Essentials with Go
**Author:** Alex Rios
**Topic tags:** `#systems` `#cli` `#performance` `#concurrency`
**Language focus:** Go-first
**Sources:** `markdown_output/System_Programming_Essentials_with_Go_-_Alex_Rios/System_Programming_Essentials_with_Go_-_Alex_Rios.md` · `summaries/System_Programming_Essentials_with_Go_-_Alex_Rios.md`

## TL;DR
A practitioner's guide to building efficient system software in Go: from functional-options-based testable CLIs, through filesystem traversal, fsnotify, and IPC (pipes + Unix sockets), to memory management (GOGC, GOMEMLIMIT, ballast, arenas), profiling (pprof/benchstat), and resource reuse primitives (`sync.Pool`, `sync.Once`, `singleflight`, mmap). The capstone is a consistent-hashing distributed cache. Apply when shipping daemons, CLIs, network services, or any process that has to behave well under load.

---

## Best Practices by Topic

### Why Go for System Programming

**Principle:** Go trades raw CPU efficiency for programmer productivity and concurrency safety — its GC is fast (worst-case STW < 100 µs) and the runtime gives you goroutines, channels, and m:n scheduling for free.

**Do:**
- Use goroutines for I/O-bound work and CPU-bound work that benefits from concurrency.
- Prefer CSP-style "share by communicating" over explicit locks when ownership transfers naturally.
- Reach for `os`/`io`/`net` first; reserve `syscall`/`x/sys` for cases where you need fine-grained control.

**Don't:**
- Don't pick Go for hot-path nanosecond-critical code where GC pauses matter.
- Don't assume goroutine execution order — the Go scheduler decides.
- Don't translate lock-heavy designs from other languages unchanged; channels are usually cleaner.

*Ref: System_Programming_Essentials_with_Go.md — "Concurrency and goroutines", "Interacting with the OS"*

---

### Tooling for Build / Test / Run / Lint

**Principle:** Standard Go tooling covers every step from edit to ship; learn it before reaching for third-party tooling.

**Do:**
- Use `go build` to produce a single statically-linked binary.
- Use `go test -race` on every change that touches shared state.
- Use `go vet` to catch format-string mismatches and shadowed errors.
- Use `go fmt` (or `gofmt -w`) on save.
- Cross-compile with `GOOS`/`GOARCH` env vars.
- Use build tags for OS-specific files (`//go:build linux`, `//go:build windows`).

**Don't:**
- Don't mix `gofmt` violations into commits — auto-format is the standard.
- Don't ignore `-race` failures; a single "spurious" failure is a real race.

**Code:**
```bash
# Compile
go build main.go

# Tests with race detector
go test -race ./...

# Vet catches wrong format verb
go vet error.go
# -> Printf format %s has arg 1999 of wrong type int.

# Format on save
go fmt unformatted.go

# Cross-platform builds
GOOS=linux  GOARCH=amd64 go build -o app
GOOS=darwin GOARCH=amd64 go run

# Build tags split per OS
// main_windows.go: //go:build windows
// main_linux.go:   //go:build linux
```

*Ref: System_Programming_Essentials_with_Go.md — "Tooling", "Cross-platform development with Go"*

---

### Goroutine Lifecycle and WaitGroup Discipline

**Principle:** Goroutines launched with `go` outlive the calling function unless synchronised — `sync.WaitGroup` is the canonical way to wait for a known number of goroutines.

**Do:**
- Call `wg.Add(n)` **before** the `go` statement (or inside the same loop iteration).
- `defer wg.Done()` inside the goroutine so it runs even on panic.
- Keep the zero value usable: `wg := sync.WaitGroup{}`.

**Don't:**
- Don't call `wg.Add` after goroutines have started — it can race.
- Don't forget `wg.Done()`; missing it causes `fatal error: all goroutines are asleep - deadlock!` in `Wait`.

**Code:**
```go
func main() {
    wg := sync.WaitGroup{}
    wg.Add(2)
    go say("world", &wg)
    go say("hello", &wg)
    wg.Wait()
}

func say(s string, wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 0; i < 5; i++ {
        fmt.Println(s)
    }
}
```

*Ref: System_Programming_Essentials_with_Go.md — "WaitGroup"*

---

### Data Race Detection with `go test -race`

**Principle:** Race conditions can pass thousands of iterations before failing once. The runtime race detector finds them deterministically.

**Do:**
- Run `go test -race` in CI on every change.
- Use `runtime.Gosched()` inside tight loops to *force* scheduler interference and surface races earlier.
- Read the WARNING output: `Read at 0x...` and `Previous write at 0x...` give the exact goroutines.

**Don't:**
- Don't ship concurrency tests without `-race`.
- Don't assume "ran 16,000 times without failing" means safe.

**Code:**
```go
// buggy version: 2 workers updating totalItems without sync
func PackItems(totalItems int) int {
    const workers, itemsPerWorker = 2, 1000
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for j := 0; j < itemsPerWorker; j++ {
                itemsPacked := totalItems
                runtime.Gosched() // emulating noise!
                itemsPacked++
                totalItems = itemsPacked
            }
        }(i)
    }
    wg.Wait()
    return totalItems
}

// test
func TestPackItems(t *testing.T) {
    if got := PackItems(2000); got != 2000 {
        t.Errorf("want 2000, got %d", got)
    }
}

// go test -race -> WARNING: DATA RACE
```

*Ref: System_Programming_Essentials_with_Go.md — "Managing data races"*

---

### Atomic Operations for Single-Word State

**Principle:** `sync/atomic` gives lock-free, single-instruction safety for counters, flags, and `int32`/`int64`/`uint32`/`uint64`/`uintptr`/`float32`/`float64`.

**Do:**
- Use `atomic.AddInt32(&x, 1)` instead of `x++` when `x` is shared across goroutines.
- Combine with `atomic.LoadInt32`/`StoreInt32` for reads.
- Consider `atomic.CompareAndSwap` for lock-free algorithms.

**Don't:**
- Don't use atomic on slices, maps, or structs — it works only on the supported word-sized primitives.
- Don't forget the `&` — atomic functions take pointers.

**Code:**
```go
import "sync/atomic"

var totalItems int32

for j := 0; j < itemsPerWorker; j++ {
    atomic.AddInt32(&totalItems, 1)
}
// go test -race -> clean
```

*Ref: System_Programming_Essentials_with_Go.md — "Atomic operations"*

---

### Mutex Critical Sections: Smaller is Faster

**Principle:** `sync.Mutex` serialises access to a critical section. Locking and unlocking are not free — `~64%` slowdown observed when a single section was split into three separate locks.

**Do:**
- Hold the lock for the minimum amount of work.
- Defer `Unlock` when the entire function body is critical.
- Embed mutexes by value when the struct is its own self-contained unit.

**Don't:**
- Don't lock around non-shared work (no I/O, no allocation that escapes).
- Don't nest two critical sections on the same `Mutex` — deadlock.
- Don't lock in a loop body if you can hoist the work outside.

**Code:**
```go
// Fast — one lock per iteration
for j := 0; j < itemsPerWorker; j++ {
    m.Lock()
    itemsPacked := totalItems
    itemsPacked++
    totalItems = itemsPacked
    m.Unlock()
}

// Slow — three locks per iteration (~64% slower in benchmark)
for j := 0; j < itemsPerWorker; j++ {
    m.Lock(); itemsPacked = totalItems; m.Unlock()
    m.Lock(); itemsPacked++; m.Unlock()
    m.Lock(); totalItems = itemsPacked; m.Unlock()
}
// Benchmark-8:              36546    32629 ns/op
// BenchmarkMultipleLocks-8: 13243    91246 ns/op
```

*Ref: System_Programming_Essentials_with_Go.md — "Mutexes"*

---

### Channels: Unbuffered vs Buffered

**Principle:** Unbuffered channels guarantee delivery at the cost of latency; buffered channels trade that guarantee for throughput.

**Do:**
- Use **unbuffered** when you need a hard synchronisation point (signalling, handoffs).
- Use **buffered** when you have producer/consumer rate mismatch or want back-pressure up to N.
- Declare channel direction in function signatures: `func write(c chan<- int)` and `func read(c <-chan int)` for compile-time safety.
- Always have a sender and receiver `ready` at the same time — otherwise deadlock.

**Don't:**
- Don't write to a nil channel (blocks forever); don't close twice (panic); don't send on closed (panic).
- Don't add a buffered channel "just in case" — that hides synchronisation requirements.
- Don't `range` over a channel without ensuring `close()` is called eventually.

**Code:**
```go
// Unbuffered — guaranteed delivery (synchronous handoff)
c := make(chan string)
go throwBalls("red", c)
fmt.Println(<-c, "received!")

// Buffered — async up to capacity (clown car)
clownChannel := make(chan int, 3)
select {
case clownChannel <- clownID:
    fmt.Printf("Clown %d hopped in\n", clownID)
default:
    fmt.Printf("Car full, can't fit %d\n", clownID)
}

// Direction-typed channel parameters
func writeChannel(c chan<- int, x int) { c <- x; close(c) }
func readChannel(c <-chan int) int       { return <-c }

// Closing after all senders done — via WaitGroup
func main() {
    balls := make(chan string)
    wg := sync.WaitGroup{}
    wg.Add(2)
    go func() { defer wg.Done(); throwBalls("red", balls) }()
    go func() { defer wg.Done(); throwBalls("green", balls) }()
    go func() { wg.Wait(); close(balls) }()
    for color := range balls {
        fmt.Println(color, "received!")
    }
}
```

*Ref: System_Programming_Essentials_with_Go.md — "An unbuffered channel", "Buffered channels", "State and signaling"*

---

### Channels vs Mutexes — When to Pick Each

**Principle:** Channels for ownership transfer / work distribution / async signalling; mutexes for caches and shared state.

**Do:**
- Use channels when you **pass ownership of data**, **distribute units of work**, or **communicate results asynchronously**.
- Use mutexes when guarding a **cache** or **shared state** that needs atomic snapshots.

**Don't:**
- Don't force one paradigm everywhere — pragmatic readability wins.

*Ref: System_Programming_Essentials_with_Go.md — "Choosing your synchronization mechanism"*

---

### Functional Options Pattern for Testable CLIs

**Principle:** Functional options give callers a clean, evolvable way to configure a struct without combinatorial constructors, while making every option independently overridable in tests.

**Do:**
- Define `type Option func(*config)` and accept variadic `...Option`.
- Make options idempotent so test code can layer them safely.
- Provide sensible defaults inside the constructor.
- Use options for `stdin`/`stdout`/`stderr`, time sources, loggers, and dependencies.

**Don't:**
- Don't grow positional constructors past 3 arguments.
- Don't bake I/O into the function you want to test — inject it as an option.

**Code:**
```go
type Option func(*myApp)

func WithStdin(r io.Reader) Option  { return func(a *myApp) { a.stdin = r } }
func WithStdout(w io.Writer) Option { return func(a *myApp) { a.stdout = w } }
func WithLogger(l *log.Logger) Option {
    return func(a *myApp) { a.logger = l }
}

type myApp struct {
    stdin  io.Reader
    stdout io.Writer
    logger *log.Logger
}

func New(opts ...Option) *myApp {
    a := &myApp{
        stdin:  os.Stdin,
        stdout: os.Stdout,
        logger: log.Default(),
    }
    for _, opt := range opts {
        opt(a)
    }
    return a
}

// In production
app := New(WithStdout(buf), WithLogger(myLog))

// In tests — overrides without touching internals
app := New(WithStdin(strings.NewReader("input\n")))
```

*Ref: System_Programming_Essentials_with_Go.md — "Developing and testing a CLI program", "Making it testable"*

---

### CLI Standard Streams (stdin / stdout / stderr) Discipline

**Principle:** A correct Unix-style CLI reads from `stdin`, writes results to `stdout`, and reports errors to `stderr`. This lets it compose via pipes.

**Do:**
- Send logs/diagnostics to `stderr` (file descriptor 2).
- Send user-facing results to `stdout` (file descriptor 1).
- Read input from `stdin` (file descriptor 0) when no file is given.
- Combine `2>&1` to merge streams for `grep`/`less`.

**Don't:**
- Don't write error messages to `stdout` — they break pipes.
- Don't read everything into memory just to "process" it.

*Ref: System_Programming_Essentials_with_Go.md — "Standard streams", "Redirections and standard streams"*

---

### File Descriptor and `os` Package Basics

**Principle:** File descriptors are integer handles to OS resources. The `os` package wraps them portably; reach for `x/sys` only when you need raw control.

**Do:**
- Use `os.Open`, `os.Create`, `os.Stat`, `os.IsNotExist`, `os.IsPermission` for filesystem work.
- Use `os.Getwd` / `os.Chdir` for working directory.
- Use `os.Getpid` / `os.Getppid` / `os.Getuid` / `os.Getgid` for process/identity info.
- Always `defer f.Close()` after a successful `os.Open`.

**Don't:**
- Don't call `os.Exit` inside `main()` while leaving `os.File` handles open — they leak.

**Code:**
```go
f, err := os.Open("data.bin")
if err != nil {
    return err
}
defer f.Close()

info, err := os.Stat("data.bin")
if os.IsNotExist(err) {
    // ...
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Operating system functionality", "File descriptors"*

---

### Detecting Unsafe File Permissions

**Principle:** World-writable or setuid files are security risks. Detect them by reading the mode bits before opening.

**Do:**
- Inspect `info.Mode().Perm()` and compare against `0o777`.
- Use `info.Mode()&os.ModeSetuid != 0` to detect setuid.
- Refuse to load files matching dangerous patterns.

**Don't:**
- Don't blindly trust `/etc/passwd`-style files because their name is conventional.

*Ref: System_Programming_Essentials_with_Go.md — "Identifying unsafe file and directory permissions", "Files and permissions"*

---

### `path/filepath` vs `path`

**Principle:** `path/filepath` is OS-aware (`/` on Unix, `\` on Windows); `path` is URL-style and Unix-only. Use `filepath` for filesystem code.

**Do:**
- Use `filepath.Join`, `filepath.Base`, `filepath.Dir`, `filepath.Ext` for filesystem paths.
- Use `filepath.WalkDir` (Go 1.16+) for tree traversal — it returns `fs.DirEntry` to avoid stat-per-entry.
- Use `filepath.EvalSymlinks` to resolve symlink chains.

**Don't:**
- Don't use `path.Join` on filesystem paths — it will produce broken paths on Windows.

*Ref: System_Programming_Essentials_with_Go.md — "Using the path/filepath package", "Traversing directories"*

---

### Directory Traversal with `filepath.WalkDir`

**Principle:** `WalkDir(root, fn)` calls `fn(path, d DirEntry, err)` for every file/dir. It does not follow symlinks and uses `readdir` under the hood — much faster than `Walk`.

**Do:**
- Always call `filepath.WalkDir` (not the deprecated `Walk`).
- Inside the walker, call `os.Lstat(path)` again before reading — filesystems change under you.
- Skip symbolic links explicitly if you don't want to follow them.
- Use `fs.SkipDir` to short-circuit into a subtree.

**Don't:**
- Don't perform expensive operations inside the walker without first classifying the entry.

**Code:**
```go
func walkFunction(path string, d fs.DirEntry, err error) error {
    if err != nil {
        return err
    }
    fmt.Println(path)
    return nil
}

func main() {
    root := os.Args[1]
    if err := filepath.WalkDir(root, walkFunction); err != nil {
        log.Fatal(err)
    }
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Traversing directories"*

---

### Symbolic Links: Detect, Resolve, Don't Follow

**Principle:** `os.Lstat` reads link metadata; `os.Stat` follows. Use `Lstat` to detect links, `EvalSymlinks` to resolve.

**Do:**
- Use `os.Lstat` to test `info.Mode()&os.ModeSymlink != 0`.
- Use `filepath.EvalSymlinks` to canonicalise a path.
- Treat broken symlinks as errors, not silent success.

**Don't:**
- Don't use `os.Stat` when you specifically want link metadata.
- Don't chain `EvalSymlinks` repeatedly without a termination guard.

**Code:**
```go
fileinfo, err := os.Lstat(filename)
if err != nil { return err }
if fileinfo.Mode()&os.ModeSymlink != 0 {
    realpath, err := filepath.EvalSymlinks(filename)
    if err == nil {
        fmt.Println("real:", realpath)
    }
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Symbolic links and unlinking files"*

---

### Calculating Directory Size

**Principle:** Walk the tree, sum file sizes, follow symlinks only if you intend to count them.

**Do:**
- Use `filepath.WalkDir` + `info.Size()` from `d.Info()`.
- Handle errors per entry — don't abort the whole walk on one bad file.
- Consider goroutine parallelism for huge trees, but watch syscall amplification.

*Ref: System_Programming_Essentials_with_Go.md — "Calculating directory size"*

---

### Finding Duplicate Files (Hash-Based)

**Principle:** Hashing (MD5/SHA-1/SHA-256) is the standard way to dedupe. Compare on size first, then on hash, to avoid hashing everything.

**Do:**
- Group files by size first — only files matching a duplicate size need hashing.
- Stream-hash via `io.Copy(hash, file)` so huge files don't OOM.
- Use `crypto/sha256` over `md5` for new code; MD5 is fine for non-security dedup.

**Don't:**
- Don't read whole files into memory before hashing.

*Ref: System_Programming_Essentials_with_Go.md — "Finding duplicate files"*

---

### `os/signal` — Trap and Forward Signals

**Principle:** Use `signal.Notify` to convert OS signals into Go channel values, then range over the channel in a goroutine.

**Do:**
- Create a buffered channel: `sigs := make(chan os.Signal, 1)`.
- Pass every signal you care about: `signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)`.
- Always make one handler path exit (`os.Exit`) — otherwise `kill -9` is the only way out.
- Use `signal.NotifyContext` (Go 1.16+) to compose with `context.Context`.

**Don't:**
- Don't ignore `SIGHUP` if your program is a daemon — you'll need it for log rotation.

**Code:**
```go
sigs := make(chan os.Signal, 1)
signal.Notify(sigs, os.Interrupt, syscall.SIGTERM, syscall.SIGHUP)

go func() {
    for sig := range sigs {
        switch sig {
        case syscall.SIGTERM:
            rotateLog()
            os.Exit(0)
        case os.Interrupt:
            rotateLog() // Ctrl-C rotates, doesn't kill
        }
    }
}()
```

*Ref: System_Programming_Essentials_with_Go.md — "The os/signal package", "File rotation"*

---

### Task Scheduling with `time.Ticker` and Goroutines

**Principle:** Schedulers for housekeeping (log rotation, snapshotting, metrics flush) belong in goroutines driven by `time.Ticker` or `time.AfterFunc`.

**Do:**
- Use `time.NewTicker(d)` and `defer ticker.Stop()`.
- Pass durations as `time.Duration`; never `int` milliseconds.
- Handle timer signals with a dedicated case in `select`.

**Don't:**
- Don't `time.Sleep` in a loop when you actually want a periodic tick — use `Ticker` (drift-free).

**Code:**
```go
ticker := time.NewTicker(1 * time.Minute)
defer ticker.Stop()
for {
    select {
    case <-ticker.C:
        evictExpired()
    case <-stop:
        return
    }
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Task scheduling in Go"*

---

### File Monitoring with `fsnotify`

**Principle:** `fsnotify` wraps OS file-system events (`inotify` on Linux, `FSEvents` on macOS, `ReadDirectoryChangesW` on Windows) into a `Watcher` channel.

**Do:**
- Watch the **directory**, not individual files — file events on Linux often coalesce or drop.
- Re-add watches after a rename or move.
- Handle `Event.Op & (Create|Write|Remove|Rename|Chmod)` explicitly.

**Don't:**
- Don't rely on `fsnotify` to give you every byte — events are coalesced.

**Code:**
```go
w, err := fsnotify.NewWatcher()
if err != nil { log.Fatal(err) }
defer w.Close()

go func() {
    for {
        select {
        case ev, ok := <-w.Events:
            if !ok { return }
            if ev.Op&fsnotify.Write == fsnotify.Write {
                rotateIfOversize(ev.Name)
            }
        case err, ok := <-w.Errors:
            if !ok { return }
            log.Println("watch error:", err)
        }
    }
}()

if err := w.Add("/var/log/app"); err != nil { log.Fatal(err) }
<-stop
```

*Ref: System_Programming_Essentials_with_Go.md — "fsnotify", "Inotify"*

---

### Log Rotation

**Principle:** Long-lived services must rotate logs to avoid filling the disk. Rotate on size, time, or external signal.

**Do:**
- Use `os.OpenFile` with `O_APPEND|O_CREATE` and `O_WRONLY` for the current file.
- Rename the current file, reopen with `O_CREATE`, continue writing.
- Trigger rotation via SIGUSR1/SIGHUP or a Ticker.
- Compress rotated files out-of-band.

**Don't:**
- Don't reopen the file in the writing goroutine without a lock — race on FD.
- Don't rotate by truncating in place — external log readers lose continuity.

**Code:**
```go
func rotateLogFile(path string) error {
    current.Close()
    if err := os.Rename(path, path+"."+time.Now().Format("20060102T150405")); err != nil {
        return err
    }
    return openCurrent(path)
}
```

*Ref: System_Programming_Essentials_with_Go.md — "File rotation"*

---

### Distributed Locking (Redis/etcd-style)

**Principle:** Use a quorum write to `/lock/<resource>` with a TTL; renew the TTL while you hold it; release by deleting only if you still own it.

**Do:**
- Set the lock value to a unique token (UUID) and use a compare-and-delete script on release.
- Use a TTL slightly longer than your critical section — never permanent.
- Renew the TTL in a separate goroutine for long operations.
- Use `redislock`/`etcd`/`consul` libraries that implement Redlock/Mutex correctly.

**Don't:**
- Don't `SETNX` without TTL — a crashed holder locks forever.
- Don't delete by key only — another holder may have taken over.

*Ref: System_Programming_Essentials_with_Go.md — "Building a distributed lock manager in Go"*

---

### Process Management: Timeouts and Execution Bounds

**Principle:** Always bound how long a child process can run; never trust an unknown binary to exit.

**Do:**
- Use `exec.CommandContext(ctx, ...)` and cancel the ctx on timeout.
- Capture both stdout and stderr separately for diagnostics.
- Inspect `cmd.ProcessState.ExitCode()` after `Run()`.
- Stream output rather than buffering it all.

**Don't:**
- Don't ignore the `error` from `cmd.Run()` — non-zero exit is an error.

**Code:**
```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

cmd := exec.CommandContext(ctx, "/usr/bin/myservice", "--check")
out, err := cmd.Output() // captures stdout; stderr is lost unless redirected
if err != nil {
    if ctx.Err() == context.DeadlineExceeded {
        log.Println("service timed out")
    }
    return err
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Execution and timeouts", "Execute and control process execution time"*

---

### Anonymous Pipes (`os.Pipe`)

**Principle:** `os.Pipe` returns an in-memory `*os.File` pair connected like a Unix pipe — use it to stream data between in-process goroutines or to capture child stdout.

**Do:**
- Use `io.Copy(dst, src)` between the two ends.
- `defer` close both ends.
- Pipe buffer is OS-dependent (~64 KiB on Linux) — readers must drain or writers block.

**Don't:**
- Don't share one end across goroutines without a wrapper that synchronises access.

**Code:**
```go
r, w, err := os.Pipe()
if err != nil { return err }
defer r.Close()
defer w.Close()

go func() {
    io.Copy(w, strings.NewReader("payload"))
    w.Close()
}()
data, err := io.ReadAll(r)
```

*Ref: System_Programming_Essentials_with_Go.md — "The mechanics of anonymous pipes"*

---

### Named Pipes (`mkfifo` / `os.Create` to FIFO path)

**Principle:** Named pipes live in the filesystem and connect unrelated processes. Use them for producer/consumer daemons on the same host.

**Do:**
- Check `info.Mode()&os.ModeNamedPipe != 0` to confirm a path is a FIFO.
- Use `os.OpenFile(path, os.O_RDWR, 0)` for FIFO writes — opening **write-only** deadlocks when no reader is attached; `O_RDWR` guarantees at least one FD reference.
- Handle `ENOENT` for missing FIFOs and create on demand.

**Don't:**
- Don't `os.Open` (read-only) a FIFO with no writer — blocks until one appears.

*Ref: System_Programming_Essentials_with_Go.md — "Navigating named pipes (Mkfifo())"*

---

### Pipe Performance: Sizing Buffers and Drain Discipline

**Principle:** Pipe throughput is bounded by buffer size + drain speed. A reader slower than the writer stalls the whole pipeline.

**Do:**
- Drain readers in goroutines.
- Pool the buffers you write to (see `sync.Pool` topic).
- Use `bufio.NewReaderSize`/`NewWriterSize` for high-volume flows.

**Don't:**
- Don't allocate a fresh `bytes.Buffer` per message in a hot loop.

*Ref: System_Programming_Essentials_with_Go.md — "Efficient data handling"*

---

### Pipe Security Considerations

**Principle:** Pipes on disk are visible to anyone with directory access.

**Do:**
- Place FIFOs in a directory with `0o700` permissions.
- Verify the writer's UID matches expectations before reading.
- Rotate FIFO paths and document them in `--help`.

**Don't:**
- Don't trust the file's location as authentication — always verify content.

*Ref: System_Programming_Essentials_with_Go.md — "Security considerations"*

---

### Unix Domain Sockets (`net.Listen("unix", ...)`)

**Principle:** Unix sockets give you TCP-like stream semantics over a filesystem path with no network stack overhead and natural filesystem permissions.

**Do:**
- Use `net.Listen("unix", "/tmp/app.sock")` for servers, `net.Dial("unix", path)` for clients.
- Set `0o660` on the socket file; use a parent directory with restrictive perms.
- Use `os.Remove` to clean up stale socket files before `Listen`.
- Use `SOCK_STREAM` for byte streams, `SOCK_DGRAM` for datagrams.

**Don't:**
- Don't leave stale socket files — bind will fail with "address in use".

**Code:**
```go
// Server
ln, err := net.Listen("unix", "/tmp/chat.sock")
if err != nil { log.Fatal(err) }
defer os.Remove("/tmp/chat.sock") // cleanup

for {
    conn, err := ln.Accept()
    if err != nil { continue }
    go handle(conn)
}

// Client
c, err := net.Dial("unix", "/tmp/chat.sock")
if err != nil { return err }
defer c.Close()
fmt.Fprintln(c, "hello")
```

*Ref: System_Programming_Essentials_with_Go.md — "Introduction to Unix sockets", "Creating a Unix socket"*

---

### HTTP-over-Unix-Socket Servers

**Principle:** `http.Server` can serve over any `net.Listener`, including Unix sockets — useful for sidecar communication without ports.

**Do:**
- Wrap `net.Listen("unix", ...)` in a standard `http.Server`.
- Set timeouts (`ReadHeaderTimeout`, `WriteTimeout`) even for local sockets.

**Don't:**
- Don't serve Unix-socket HTTP from a globally-writable directory.

**Code:**
```go
ln, _ := net.Listen("unix", "/tmp/api.sock")
srv := &http.Server{
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
}
go srv.Serve(ln)
defer srv.Shutdown(context.Background())
defer os.Remove("/tmp/api.sock")
```

*Ref: System_Programming_Essentials_with_Go.md — "Serving HTTP under UNIX domain sockets"*

---

### Garbage Collection Tuning: GOGC and GOMEMLIMIT

**Principle:** Go's GC is concurrent and tuned for low latency. Two knobs cover most cases.

**Do:**
- Set `GOMEMLIMIT` (Go 1.19+) to a soft memory cap so the GC becomes more aggressive under pressure: `GOMEMLIMIT=512MiB`.
- Set `GOGC` only if you know your allocation pattern — default 100 is fine for most.
- Use `runtime.ReadMemStats(&mem)` to inspect `mem.HeapAlloc`, `mem.NumGC`.
- Use `GODEBUG=gctrace=1` to print GC events.

**Don't:**
- Don't set `GOGC=off` in production unless you have measured the GC pause budget and accepted the risk.

**Code:**
```go
var mem runtime.MemStats
runtime.ReadMemStats(&mem)
fmt.Println("alloc:", mem.Alloc, "numgc:", mem.NumGC)

// GC trace
// GODEBUG=gctrace=1 ./myservice
// gc 11 @0.101s 0%: 0.003+0.083+0.020 ms clock, ...
```

*Ref: System_Programming_Essentials_with_Go.md — "Garbage collection", "GOGC", "GOMEMLIMIT", "GODEBUG"*

---

### Memory Ballast for High-Throughput Servers

**Principle:** Allocating a large never-touched slice at startup gives the GC a "fudge factor" — it triggers fewer cycles at the same heap size, lowering CPU usage.

**Do:**
- Add `ballast := make([]byte, 1<<30)` (1 GiB) at startup if memory allows.
- Document why and how to tune it.

**Don't:**
- Don't use a ballast on memory-constrained hosts (< 2 GiB RAM).

*Ref: System_Programming_Essentials_with_Go.md — "Memory ballast"*

---

### Memory Arenas (Go 1.20+)

**Principle:** `arena` lets you allocate from a manually-managed region that you `Free()` in one shot. Great for batch processing where you'd otherwise thrash the GC.

**Do:**
- Use arenas for request-scoped batches: parse, process, free together.
- Be careful: pointers cannot outlive `arena.Free()`.

**Don't:**
- Don't put long-lived shared data in arenas.

**Code:**
```go
import "arena"

func processBatch(items []Item) {
    a := arena.New()
    defer a.Free()
    // use arena.New[T]() instead of new(T)
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Memory arenas", "Using memory arenas"*

---

### Stack vs Heap and Escape Analysis

**Principle:** Values that don't escape a function live on the stack (free). Escape analysis (`go build -gcflags="-m"`) tells you which variables the compiler proved escape.

**Do:**
- Run `go build -gcflags="-m=1"` on hot paths to spot unintended escapes.
- Reuse pointers when the caller outlives the callee.
- Watch large `[]byte`/`string` copies that don't need to be copied.

**Don't:**
- Don't dereference huge structs into interfaces unless necessary — they often escape.

**Code:**
```bash
go build -gcflags="-m=2" ./...
# main.go:12:6: can inline (*T).Sum
# main.go:18:6: buf escapes to heap
```

*Ref: System_Programming_Essentials_with_Go.md — "Escape analysis", "Stack and pointers"*

---

### Allocations: Reduce, Pool, Pre-size

**Principle:** Allocations are the GC's fuel. Reduce them.

**Do:**
- Pre-size slices: `make([]T, 0, n)` if `n` is known.
- Use `bytes.Buffer` or `strings.Builder` instead of `+` concatenation.
- `sync.Pool` reusable buffers.
- Stack-allocate small structs; pass by value where it fits.

**Don't:**
- Don't `append` to a `nil` slice in a hot loop without `make(... 0, expected)`.

*Ref: System_Programming_Essentials_with_Go.md — "Memory allocations", "Common pitfalls"*

---

### Benchmarking: `testing.B` Discipline

**Principle:** Benchmarks are experiments. `b.N` is the loop count; the framework tunes it for statistical significance.

**Do:**
- Run `go test -bench=. -benchmem -count=10` and use `benchstat` to compare.
- Call `b.ResetTimer()` after expensive setup.
- Use `b.RunParallel` for concurrent code.
- Sub-benchmark with `b.Run("name", func(b *testing.B) { ... })`.

**Don't:**
- Don't benchmark without `-benchmem` — allocs/op and bytes/op matter.
- Don't compare across machines.

**Code:**
```go
func BenchmarkSum(b *testing.B) {
    data := make([]int, 1024)
    for i := range data { data[i] = i }

    b.ResetTimer()
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        _ = Sum(data)
    }
}

// benchstat old.txt new.txt
// name    old time/op    new time/op    delta
// Sum-8    1.23µs ± 2%   0.45µs ± 1%   -63.4%
```

*Ref: System_Programming_Essentials_with_Go.md — "Benchmarking your code", "Writing your first benchmark"*

---

### Profiling: CPU, Memory, Block, Mutex, Goroutine

**Principle:** `runtime/pprof` exposes hooks for everything. Use `pprof.StartCPUProfile`/`StopCPUProfile` for CPU, `runtime/heap` writes for memory.

**Do:**
- Profile with a realistic load: empty benchmarks lie.
- Use `-cpuprofile`, `-memprofile`, `-blockprofile`, `-mutexprofile` flags.
- View with `go tool pprof -http=:8080 cpu.prof`.
- Look at `flat` (time spent in this function) and `cum` (time spent in this function + callees).

**Don't:**
- Don't profile a release build with debugging stripped — symbols vanish.

*Ref: System_Programming_Essentials_with_Go.md — "CPU profiling", "Memory profiling", "Profiling memory over time"*

---

### Flame Graphs and Trace Visualisation

**Principle:** A flame graph collapses stacks into coloured bars; wide bars = hot paths. Go's `pprof` can render them via `-http`.

**Do:**
- Combine `pprof` with Brendan Gregg's `flamegraph.pl` if you want static SVGs.
- Use `go tool trace` for scheduler-level analysis (goroutine states, GC events).

**Don't:**
- Don't micro-optimise functions whose bar is below 1 %.

*Ref: System_Programming_Essentials_with_Go.md — "Profiling memory over time"*

---

### TCP Networking: Servers and Clients

**Principle:** `net` is the lowest portable layer. `net/http` is built on top.

**Do:**
- Always set deadlines: `conn.SetReadDeadline(time.Now().Add(30 * time.Second))`.
- Reuse listeners; pool outbound connections.
- Use `SO_REUSEADDR` (via `net.ListenConfig`) for restart-safe servers.
- For binary protocols, frame your messages — TCP gives you bytes, not records.

**Don't:**
- Don't read from `net.Conn` without a deadline — a stalled peer hangs forever.

*Ref: System_Programming_Essentials_with_Go.md — "TCP sockets"*

---

### HTTP Servers with Sensible Defaults

**Principle:** `http.Server` ships with zero timeouts — that's a footgun.

**Do:**
- Always set `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`.
- Set `MaxHeaderBytes` to bound header memory.
- Use `http.Server.RegisterOnShutdown` to release resources cleanly.

**Don't:**
- Don't use `http.ListenAndServe` in production — it returns no error to the caller and has no timeouts.

**Code:**
```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       30 * time.Second,
    WriteTimeout:      30 * time.Second,
    IdleTimeout:       120 * time.Second,
    MaxHeaderBytes:    1 << 20,
}
log.Fatal(srv.ListenAndServe())
```

*Ref: System_Programming_Essentials_with_Go.md — "HTTP servers and clients", "HTTP verbs", "HTTP status codes"*

---

### Securing the Connection: TLS Configuration

**Principle:** Modern TLS defaults are good; the unsafe overrides are still the defaults in some examples.

**Do:**
- Use `tls.Config{MinVersion: tls.VersionTLS12}` (or higher).
- Prefer `tls.VersionTLS13` when both sides support it.
- Provide `GetCertificate` for SNI.

**Don't:**
- Don't ship TLS without verifying peer certificates (`InsecureSkipVerify: true`).

*Ref: System_Programming_Essentials_with_Go.md — "Securing the connection", "Certificates"*

---

### UDP vs TCP: Pick by Shape

**Principle:** TCP = reliable stream; UDP = unreliable datagram. Use TCP for stateful protocols, UDP for low-latency fire-and-forget.

**Do:**
- Use UDP for telemetry, voice/video, game state.
- Use TCP for request/response, file transfer, anything that needs ordering.

**Don't:**
- Don't build reliability on top of UDP (retransmit, dedup) unless you really need UDP's latency properties — TCP usually wins.

*Ref: System_Programming_Essentials_with_Go.md — "UDP versus TCP"*

---

### QUIC: HTTP/3's Transport

**Principle:** QUIC gives you multiplexed, encrypted streams over UDP without TCP's head-of-line blocking.

**Do:**
- Use `github.com/quic-go/quic-go` for native Go servers/clients.
- Take advantage of 0-RTT handshakes for repeat connections.

**Don't:**
- Don't fall back to TCP silently — explicit fallback keeps observability clean.

*Ref: System_Programming_Essentials_with_Go.md — "Advanced networking"*

---

### Logging: `log/slog` (Go 1.21+)

**Principle:** Structured, leveled logging is the baseline for modern services. `slog` is in the standard library.

**Do:**
- Use `slog.NewJSONHandler` for machine-readable, `slog.NewTextHandler` for humans.
- Set a `*slog.Logger` on `context.Context` for request-scoped fields.
- Log at appropriate levels: Debug/Info/Warn/Error.

**Don't:**
- Don't mix `fmt.Println` and `log.Printf` — pick one structured form.

**Code:**
```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
slog.SetDefault(logger)

logger.Info("request handled",
    "method", r.Method,
    "path", r.URL.Path,
    "duration_ms", time.Since(start).Milliseconds(),
)
```

*Ref: System_Programming_Essentials_with_Go.md — "Zap versus slog"*

---

### Logging: What to Log (and What Not To)

**Principle:** Log for diagnosis, not narration.

**Do:**
- Log request start/end with duration and request ID.
- Log errors with stack/cause, not just message.
- Log lifecycle events (start, stop, config loaded).

**Don't:**
- Don't log secrets, passwords, tokens, full request bodies, or PII.
- Don't log inside hot loops — sample.

*Ref: System_Programming_Essentials_with_Go.md — "What to log?", "What not to log?"*

---

### Distributed Tracing with OpenTelemetry

**Principle:** A trace stitches a request across services via context-propagated span IDs.

**Do:**
- Propagate `context.Context` through every layer.
- Use `otel.Tracer("my-service").Start(ctx, "name")`.
- Use `propagation.TraceContext` (W3C) over the wire.

**Don't:**
- Don't create spans manually for every function — only at I/O or meaningful units of work.

**Code:**
```go
ctx, span := tracer.Start(r.Context(), "handleOrder")
defer span.End()

if err := db.QueryContext(ctx, ...); err != nil {
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
    return err
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Distributed tracing", "Effective tracing"*

---

### Metrics: RED Method

**Principle:** For every service, instrument **R**ate, **E**rrors, **D**uration.

**Do:**
- Counters for events (`requests_total{status="500"}`).
- Histograms for latencies (`request_duration_seconds`).
- Gauges for current state (`inflight_requests`).
- Use the Prometheus naming convention.

**Don't:**
- Don't put unbounded labels (raw URLs, user IDs) — cardinality explosion.

*Ref: System_Programming_Essentials_with_Go.md — "Metrics", "What metric should we use?"*

---

### OpenTelemetry Project Layout

**Principle:** Standardise on OTel APIs (`go.opentelemetry.io/otel`) and exporters (`otlp`). Vendor-specific SDKs should be swappable.

**Do:**
- Initialise `trace.TracerProvider`, `metric.MeterProvider`, `propagation.TraceContext` once at boot.
- Use the OTLP exporter to ship to a collector, not directly to a backend.

**Don't:**
- Don't initialise exporters in libraries — let the application configure them.

*Ref: System_Programming_Essentials_with_Go.md — "The OTel project", "OTel"*

---

### Module Hygiene and CI

**Principle:** A clean module graph and a green CI pipeline catch problems before they ship.

**Do:**
- Use `go mod tidy` regularly; commit `go.sum`.
- Pin to patch versions for stability, minor versions for new features.
- Run `go vet`, `staticcheck`, `golangci-lint`, `go test -race`, `govulncheck` on every PR.
- Cache module downloads in CI (`GOMODCACHE`).

**Don't:**
- Don't vendor unless you have to — `go mod` resolution is normally fast enough.

*Ref: System_Programming_Essentials_with_Go.md — "Go Modules", "The routine using modules", "CI"*

---

### Static Analysis Tools

**Principle:** Linters find bugs humans miss.

**Do:**
- `go vet ./...` (always).
- `staticcheck ./...` (recommended).
- `golangci-lint run` as a one-shot aggregator.
- `govulncheck ./...` for known CVEs.

**Don't:**
- Don't disable lint rules globally — fix the warnings.

*Ref: System_Programming_Essentials_with_Go.md — "Static analysis"*

---

### Releasing Your Application

**Principle:** Reproducible, auditable releases.

**Do:**
- Tag with `git tag -s vX.Y.Z` (signed).
- Generate checksums (`sha256sum`) and sign them.
- Publish SBOMs (CycloneDX/SPDX).
- Use `goreleaser` for cross-platform binaries.

**Don't:**
- Don't release binaries built from `main` — only tagged commits.

*Ref: System_Programming_Essentials_with_Go.md — "Releasing your application"*

---

### Distributed Cache: Sharding with Consistent Hashing

**Principle:** Consistent hashing minimises remapping when nodes join/leave. A virtual-node ring smooths the distribution.

**Do:**
- Pick a hash function (e.g. `crc32` or `xxhash`) — MD5 is overkill.
- Use ≥ 100 virtual nodes per physical node.
- Replicate keys to the next N nodes on the ring.
- Handle gossip-based membership changes.

**Don't:**
- Don't use naive `key % N` — adding one node remaps almost everything.

*Ref: System_Programming_Essentials_with_Go.md — "Sharding", "Capstone Project – Distributed Cache"*

---

### Cache Eviction Policies

**Principle:** Pick the policy that matches your workload; cache is always a trade-off.

**Do:**
- **LRU** for general-purpose caches (`container/list` + map).
- **LFU** when "hot" items are stable (compilation artefacts).
- **TTL** for time-sensitive data (sessions, prices).
- **ARC** when you can't decide between recency and frequency.

**Don't:**
- Don't mix eviction policies per-key without a documented reason.

*Ref: System_Programming_Essentials_with_Go.md — "Eviction policies"*

---

### Distributed Cache Interface Design

**Principle:** A tiny, well-typed interface lets you swap backends (in-memory, Redis, custom).

**Do:**
```go
type Cache interface {
    Get(ctx context.Context, key string) ([]byte, bool)
    Set(ctx context.Context, key string, val []byte, ttl time.Duration) error
    Delete(ctx context.Context, key string) error
}
```

**Don't:**
- Don't expose internal data structures in the interface.

*Ref: System_Programming_Essentials_with_Go.md — "The interface"*

---

### Transport Choice for the Cache: TCP, HTTP, gRPC

**Principle:** Pick the transport that matches the operational reality.

**Do:**
- TCP for in-cluster peers with custom framing.
- HTTP/JSON for browser/edge clients.
- gRPC for typed microservices with protobuf schemas.
- Unix sockets for same-host sidecars.

**Don't:**
- Don't use HTTP for high-frequency internal RPC — gRPC or raw TCP wins.

*Ref: System_Programming_Essentials_with_Go.md — "TCP", "HTTP", "Others"*

---

### Thread Safety for Cache State

**Principle:** A concurrent cache must synchronise map access. The simplest correct option is `sync.Map` or a sharded map.

**Do:**
- Use `sync.Map` for "write once, read many" caches.
- For high-write caches, shard the map and lock per shard.
- Document the locking strategy on the struct.

**Don't:**
- Don't use a plain `map` with no lock — runtime panic on concurrent access.

*Ref: System_Programming_Essentials_with_Go.md — "Adding thread safety", "Thread safety"*

---

### `sync.Pool` for Object Reuse

**Principle:** `sync.Pool` caches values that are expensive to allocate but safe to discard. The runtime empties pools at GC.

**Do:**
- Use `Pool` for `*bytes.Buffer`, `[]byte` slices, JSON encoders.
- Wrap `Get()` to always `Put()` back, even on errors:
  ```go
  buf := pool.Get().(*bytes.Buffer)
  buf.Reset()
  defer pool.Put(buf)
  ```
- Tune `New` to return zero-value, never `nil`.

**Don't:**
- Don't use `sync.Pool` for items that must survive across GC cycles — it gets cleared.

**Code:**
```go
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func handle(w http.ResponseWriter, r *http.Request) {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    defer bufPool.Put(buf)
    // ... use buf
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Using sync.Pool in a network server", "Using sync.Pool for JSON marshaling"*

---

### `sync.Once` for One-Shot Initialisation

**Principle:** `sync.Once` guarantees a function runs exactly once across all goroutines, even under contention.

**Do:**
- Use for singleton init (DB pools, feature flags, expensive clients).
- Stack-allocate (`var once sync.Once`) — no need for `new`.

**Don't:**
- Don't use it inside hot paths — even a no-op `Once.Do` has atomic cost.

**Code:**
```go
var (
    client *http.Client
    once   sync.Once
)

func getClient() *http.Client {
    once.Do(func() {
        client = &http.Client{Timeout: 5 * time.Second}
    })
    return client
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Executing tasks once"*

---

### `singleflight` — Collapse Duplicate Concurrent Calls

**Principle:** `golang.org/x/sync/singleflight` deduplicates concurrent calls to the same key — the second caller waits for the first's result instead of duplicating work.

**Do:**
- Use in front of caches, remote services, expensive computations.
- Return `shared bool` so callers know if they got a cached in-flight result.

**Don't:**
- Don't use it for writes — duplicate writes can corrupt state.

**Code:**
```go
var group singleflight.Group

func GetUser(ctx context.Context, id string) (*User, error) {
    v, err, _ := group.Do(id, func() (any, error) {
        return fetchUserFromDB(ctx, id)
    })
    if err != nil { return nil, err }
    return v.(*User), nil
}
```

*Ref: System_Programming_Essentials_with_Go.md — "singleflight"*

---

### Memory Mapping (`syscall.Mmap` / `golang.org/x/sys/unix.Mmap`)

**Principle:** `mmap` lets you treat a file as a `[]byte` in virtual memory — the kernel pages data in on demand.

**Do:**
- Use for large read-only datasets (genomes, lookup tables).
- Always `munmap` when done (use `defer`).
- Choose `PROT_READ` if you don't need writes.
- `MADV_SEQUENTIAL`/`MADV_RANDOM` to advise the kernel.

**Don't:**
- Don't `mmap` a file you're also writing through `os.File.Write` — undefined behaviour.
- Don't forget that pages are 4 KiB-aligned — `offset` must be page-aligned.

*Ref: System_Programming_Essentials_with_Go.md — "Effective memory mapping"*

---

### Avoiding Common Performance Pitfalls

**Principle:** Most "fast Go" comes from avoiding the obvious mistakes.

**Do:**
- Reuse buffers with `sync.Pool`.
- Set `GOMEMLIMIT`.
- Use `strings.Builder` for concatenation.
- Stream large responses.

**Don't:**
- Don't call `time.After` inside tight loops — it allocates.
- Don't close over loop variables in goroutines without passing them as args.

*Ref: System_Programming_Essentials_with_Go.md — "Avoiding common performance pitfalls"*

---

### Avoiding `time.After` Leaks in Loops

**Principle:** `time.After` allocates a new `*time.Timer` each iteration — in a hot loop, this thrashes the GC and can leak timers.

**Do:**
- Hoist a `*time.Timer` outside the loop and call `t.Reset(d)` each iteration.
- Use `time.NewTicker` for periodic ticks.

**Don't:**
- Don't call `time.After` inside `for { ... }`.

**Code:**
```go
t := time.NewTimer(timeout)
defer t.Stop()
for {
    select {
    case <-ch:
        // work
    case <-t.C:
        return errTimeout
    }
    if !t.Stop() { <-t.C } // drain
    t.Reset(timeout)
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Leaking with time.After"*

---

### Avoid `defer` Inside Hot For-Loops

**Principle:** `defer` adds overhead (≈ 35 ns/call). In hot loops the deferred functions pile up until the function returns.

**Do:**
- Lift `defer` out of the loop into a helper.
- Or use plain close calls when you can prove it's safe.

**Don't:**
- Don't `defer f.Close()` for a hundred files in a loop — close explicitly.

**Code:**
```go
// Bad: defer accumulates
for _, p := range paths {
    f, _ := os.Open(p)
    defer f.Close() // ALL of them close when main returns
    process(f)
}

// Good: helper function
func processAll(paths []string) error {
    for _, p := range paths {
        if err := processOne(p); err != nil {
            return err
        }
    }
    return nil
}

func processOne(p string) error {
    f, err := os.Open(p)
    if err != nil { return err }
    defer f.Close()
    // ...
}
```

*Ref: System_Programming_Essentials_with_Go.md — "Defer in for loops"*

---

### Map Management: Pre-size and Replace, Don't Delete

**Principle:** `delete(m, k)` doesn't shrink a map — it leaves tombstones. For long-lived maps, replace.

**Do:**
- Pre-size with `make(map[K]V, hint)`.
- For periodic eviction, build a fresh map in one pass.

**Don't:**
- Don't expect `delete` to release memory.

*Ref: System_Programming_Essentials_with_Go.md — "Maps management"*

---

### Resource Management: Always Close

**Principle:** Every `Open` deserves a `Close`; every `Acquire` deserves a `Release`.

**Do:**
- `defer` immediately after the success check.
- Track goroutines with `WaitGroup`; cancel them via context.
- Use `runtime.SetFinalizer` only as a safety net, never as primary cleanup.

**Don't:**
- Don't `os.Exit` inside a function holding open resources — `defer` won't run.

*Ref: System_Programming_Essentials_with_Go.md — "Resource management"*

---

### Reading HTTP Bodies Fully Before Discarding

**Principle:** HTTP/1.1 keep-alive requires the server to drain the request body before reusing the connection. Failure to do so leaks connections.

**Do:**
- Use `io.Copy(io.Discard, r.Body)` to drain, then `r.Body.Close()`.
- Set a deadline on the drain — `r.Body.Read` could block forever.

**Don't:**
- Don't `r.Body.Close()` without draining — the connection can't be reused.

*Ref: System_Programming_Essentials_with_Go.md — "Handling HTTP bodies"*

---

### Channel Drainage on Cancellation

**Principle:** A goroutine blocked on `<-ch` won't exit on context cancellation. Always select on `ctx.Done()` too.

**Do:**
```go
for {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case v, ok := <-ch:
        if !ok { return nil }
        process(v)
    }
}
```

**Don't:**
- Don't `for v := range ch { ... }` without a context path — leaks on shutdown.

*Ref: System_Programming_Essentials_with_Go.md — "Channel mismanagement"*

---

### Coordination-Free Sharding

**Principle:** Sharding by `hash(key) % N` removes the need for a central lock — each shard has its own mutex, reducing contention.

**Do:**
- Pick `N` ≈ 2× your CPU count or until benchmark stops improving.
- Use `xxhash` or `fnv` for cheap hashing.

**Don't:**
- Don't shard with a non-power-of-two unless you intentionally want modulo behaviour.

*Ref: System_Programming_Essentials_with_Go.md — "Adding thread safety"*

---

### Channel Selection: When Channels Outperform Mutexes

**Principle:** Channels win for hand-offs and pipelines; mutexes win for in-place mutation of small shared state.

*Ref: System_Programming_Essentials_with_Go.md — "Choosing your synchronization mechanism"*

---

### Anti-Patterns & Common Mistakes

- **Unhandled errors:** `if err != nil { ... }` everywhere; never `_ = something_that_returns_err`.
- **String concatenation in loops:** use `strings.Builder` or `bytes.Buffer`.
- **Reading whole files into memory:** stream with `io.Copy`.
- **Goroutines without termination:** every goroutine must have an exit path (context, channel close, return).
- **Sharing maps across goroutines without sync:** runtime panic.
- **`time.After` in loops:** leaks.
- **`defer` in loops:** accumulates.
- **Returning goroutines from functions:** goroutines need explicit ownership.
- **Race conditions brushed off:** always run `go test -race`.
- **Forgetting `O_RDWR` on named pipes:** deadlocks on write.
- **Profiling the wrong binary:** always profile what's deployed (release, no -trimpath stripping).
- **Long-running goroutines leaking timers:** use `time.NewTimer` + `Reset`/`Stop`.
- **Building debug binaries for production benchmarks:** `-ldflags="-s -w"` matters less than compiler optimisations.
- **Closing over loop variables:** pass `i` as a parameter to the goroutine.

---

## Decision Heuristics / Checklists

### When to pick what synchronisation primitive
- One-shot init? → `sync.Once`
- Hot-path shared counter? → `sync/atomic`
- Cache (read-heavy)? → `sync.Map` or sharded map + `sync.RWMutex`
- Pipeline of stages? → channels + `select`
- Hand-off / cancellation? → `context.Context`
- Long-running worker? → goroutine + `WaitGroup` + `context.Done()`

### Building a Go CLI — checklist
- Functional options for config
- `stdin`/`stdout`/`stderr` discipline
- `flag` (stdlib) for args; or `cobra` for subcommands
- Timeouts on every I/O
- Structured logging (`slog`)
- Context propagation
- Graceful shutdown (SIGTERM → drain → exit)
- Version flag and build-time info (`-ldflags "-X main.Version=..."`)
- Reproducible builds (`-trimpath`)
- `go test -race` + coverage gate in CI

### Building a Go service — checklist
- `http.Server` with full timeout set
- Metrics: RED method
- Tracing: OpenTelemetry + W3C propagation
- Logging: `slog` JSON to stderr
- Profiling endpoint: `net/http/pprof` guarded by auth
- `GOMEMLIMIT` set
- `sync.Pool` for hot-path buffers
- Health/readiness/liveness endpoints
- Graceful shutdown
- `govulncheck` in CI

---

### Goroutine Scheduler and m:n Scheduling

**Principle:** Go's runtime uses m:n scheduling — many goroutines multiplexed onto few OS threads. The Go scheduler (not the kernel) decides which goroutine runs next, which is much cheaper than kernel context switching.

**Do:**
- Set `GOMAXPROCS` to the number of cores (default since 1.5).
- Design goroutines to be cooperative — yield on I/O, channel sends, mutex contention.

**Don't:**
- Don't pin goroutines to OS threads with `runtime.LockOSThread` unless you're calling C code that requires it.
- Don't expect `GOMAXPROCS > cores` to make your code faster — it won't.

*Ref: System_Programming_Essentials_with_Go.md — "Concurrency and goroutines"*

---

### `runtime.Gosched()` for Cooperative Yielding

**Principle:** `runtime.Gosched()` yields the processor, allowing other goroutines to run. Use it to surface races in tests.

**Do:**
- Sprinkle it inside tight CPU loops to simulate "noise" during race-condition testing.
- Use sparingly in production code — usually the scheduler knows better than you do.

**Don't:**
- Don't call `runtime.Gosched()` as a substitute for proper synchronisation.

*Ref: System_Programming_Essentials_with_Go.md — "Changing shared state"*

---

### Signal Channels for Goroutine Orchestration

**Principle:** A signal channel carries no data — its closure signals an event. `chan struct{}` is the canonical empty channel.

**Do:**
- Use `close(c)` as a broadcast signal — every receiver wakes up.
- Define as `chan struct{}` — zero memory overhead.

**Don't:**
- Don't send values on a signal channel — senders would block since no one is reading (or you'd need a buffered channel, which defeats the purpose).

*Ref: System_Programming_Essentials_with_Go.md — "Buffered channels"*

---

### `select` for Multi-Channel Coordination

**Principle:** `select` waits on multiple channel operations simultaneously, picking the first that's ready.

**Do:**
- Use `select` with a `default` for non-blocking sends/receives.
- Use `select` with `time.After` for timeouts.
- Always include `ctx.Done()` in production `select` statements.

**Don't:**
- Don't put side-effecting code in `case` clauses without thinking about which branch fires.

*Ref: System_Programming_Essentials_with_Go.md — "An unbuffered channel", "select"*

---

### Time-Bounded Operations with `context.WithTimeout`

**Principle:** Any I/O call that doesn't honour a context can hang forever. Wrap them.

**Do:**
- Use `context.WithTimeout` for all outbound calls.
- Carry the ctx through every layer.
- Honour `ctx.Err()` in error returns.

**Don't:**
- Don't use `context.Background()` deep inside business logic — pass the ctx from the top.

*Ref: System_Programming_Essentials_with_Go.md — "Advanced networking"*

---

### Unix Socket File Cleanup Before `Listen`

**Principle:** `net.Listen("unix", path)` fails with "address in use" if a stale socket file exists.

**Do:**
- Always `os.Remove(path)` before `Listen` (or in an `init` that runs once).
- Use `SO_REUSEADDR` semantics via `net.ListenConfig`.
- Document the socket path in `--help`.

**Don't:**
- Don't blindly overwrite — the old daemon might still be running.

**Code:**
```go
path := "/tmp/app.sock"
_ = os.Remove(path) // best effort
ln, err := net.Listen("unix", path)
if err != nil { return err }
defer os.Remove(path)
```

*Ref: System_Programming_Essentials_with_Go.md — "Creating a Unix socket"*

---

### HTTP-over-Unix-Socket Address Normalisation

**Principle:** When using `http.Server` over a Unix socket, the `Addr` field is ignored — only the listener's address matters.

**Do:**
- Leave `Addr` empty when serving over Unix socket.
- Set sensible timeouts regardless of transport.

*Ref: System_Programming_Essentials_with_Go.md — "Serving HTTP under UNIX domain sockets"*

---

### Optimising Pipes for Streaming Workloads

**Principle:** Pipe throughput depends on reader speed and buffer size. Don't block the writer waiting for a slow consumer.

**Do:**
- Use `bufio.NewWriterSize` for the writer side.
- Decouple producer/consumer via channels when both run as goroutines.
- Batch writes when possible.

*Ref: System_Programming_Essentials_with_Go.md — "Efficient data handling"*

---

### Memory Leak Detection in Long-Running Services

**Principle:** A slow leak in a 24/7 process will eventually OOM the host. Detect it early.

**Do:**
- Use `runtime.MemStats` to sample `HeapAlloc`, `HeapObjects`, `NumGC` periodically.
- Export as a gauge metric and alert on monotonic growth.
- Run `runtime/heap` profile weekly.

**Don't:**
- Don't rely on `runtime.GC()` to "fix" leaks — they need code changes.

*Ref: System_Programming_Essentials_with_Go.md — "Memory profiling", "Profiling memory over time"*

---

### Benchmark Reproducibility

**Principle:** Benchmarks are noisy. Use `-count=N` and `benchstat` to compare reliably.

**Do:**
- Pin CPU frequency when running micro-benchmarks (`performance` governor on Linux).
- Run multiple iterations and let `benchstat` compute the confidence interval.
- Compare against a baseline you commit to the repo.

**Don't:**
- Don't change the kernel, hardware, or environment between benchmark runs.

*Ref: System_Programming_Essentials_with_Go.md — "Writing your first benchmark"*

---

### `runtime/trace` for Scheduler-Level Diagnosis

**Principle:** `go tool trace` shows goroutine state transitions, GC events, syscall blocking — useful when pprof says "where" but you want to know "why it's waiting".

**Do:**
- Generate a trace with `os.WriteFile("/tmp/trace.out", trace.Start(...).Stop())`.
- Open in `go tool trace trace.out` for a timeline view.
- Look for long Schedule-latency bars or "Syscall" rectangles.

*Ref: System_Programming_Essentials_with_Go.md — "Profiling memory over time"*

---

### `pprof` HTTP Endpoint in Production

**Principle:** `net/http/pprof` lets you grab profiles from a live process via HTTP.

**Do:**
- Mount on a separate port (`localhost:6060`) or behind auth.
- Restrict via firewall / sidecar.
- Document the endpoint for on-call.

**Don't:**
- Don't expose `/debug/pprof` to the public internet — it leaks goroutine stacks and memory contents.

**Code:**
```go
import _ "net/http/pprof"

go func() {
    log.Fatal(http.ListenAndServe("localhost:6060", nil))
}()
```

*Ref: System_Programming_Essentials_with_Go.md — "Memory profiling"*

---

### Mutex vs RWMutex vs Atomic — Pick the Right Tool

**Principle:** `sync.Mutex` blocks all access; `sync.RWMutex` allows concurrent readers; `sync/atomic` is lock-free.

**Do:**
- Use `atomic.AddInt64` for counters.
- Use `RWMutex` when reads dominate writes (>10:1).
- Use plain `Mutex` for write-heavy or short critical sections (less overhead).

*Ref: System_Programming_Essentials_with_Go.md — "Mutexes"*

---

### Trace Propagation Across Services

**Principle:** A trace needs to flow across process boundaries — W3C `traceparent` header does that.

**Do:**
- Use OpenTelemetry's `otelhttp` middleware.
- Propagate context over gRPC and HTTP automatically.
- Add a `request_id` for cross-system correlation when full tracing isn't available.

**Don't:**
- Don't invent your own trace-id format — pick W3C.

*Ref: System_Programming_Essentials_with_Go.md — "Effective tracing", "Distributed tracing"*

---

### Cardinality Discipline for Metrics

**Principle:** Every unique label combination creates a new time series. Unbounded cardinality = OOM in your TSDB.

**Do:**
- Use enums for status (`status="ok|error"`), not raw error messages.
- Limit URL labels to path templates, not actual paths.
- Bound label values that come from user input.

**Don't:**
- Don't label with user IDs, raw URLs, full error messages, or timestamps.

*Ref: System_Programming_Essentials_with_Go.md — "Metrics"*

---

### Secure Defaults for Sockets and Pipes

**Principle:** A socket or FIFO on disk is a door to your process.

**Do:**
- Create parent directory with `0o700`.
- `chmod 0o660` on the socket file.
- Authenticate peers via SO_PEERCRED (`unix.SO_PEERCRED`) when available.

**Don't:**
- Don't put sockets in `/tmp` if your threat model includes hostile local users.

*Ref: System_Programming_Essentials_with_Go.md — "Security considerations"*

---

### Iterative Capstone: From In-Memory to Distributed Cache

**Principle:** Build features step-by-step — start single-node, add TCP, then HTTP, then sharding. Each step is a committable, runnable, testable increment.

**Do:**
- Define the interface first; pick the implementation later.
- Implement one transport at a time.
- Add eviction policies in their own commit.
- Add sharding on top of a working single-node cache.

**Don't:**
- Don't design the entire system before writing the first line of code.

*Ref: System_Programming_Essentials_with_Go.md — "Capstone Project – Distributed Cache"*

---

---

## Cross-References
- Related: [[../Go_Systems_Programming.md]]
- Related: [[../Efficient_Go.md]]
- Topic index: [[../INDEX.md]]
