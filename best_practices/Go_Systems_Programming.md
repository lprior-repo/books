# Go Systems Programming
**Author:** Mihalis Tsoukalos
**Topic tags:** `#systems` `#cli` `#go` `#concurrency` `#io` `#networking` `#processes`
**Language focus:** Go-first
**Sources:** `markdown_output/Go_Systems_Programming_-_Mihalis_Tsoukalos/Go_Systems_Programming_-_Mihalis_Tsoukalos.md` · `summaries/Go_Systems_Programming_-_Mihalis_Tsoukalos.md`

## TL;DR
A practical, by-example tour of Unix systems programming in Go. Builds core utilities — `pwd`, `which`, `find`, `wc`, `cp`, `dd`, `cat` — from scratch to teach file/directory I/O, file permissions, signals, goroutines/channels, TCP/UDP/RPC networking, and web clients/servers. The recurring lessons: never ignore errors, prefer `flag` over raw `os.Args`, prefer `io.Copy` and `bufio.Scanner` over byte-at-a-time loops, and reach for `sync.WaitGroup` + channels over `time.Sleep`.

---

## Best Practices by Topic

### Command-Line Arguments & the `flag` Package  `#cli`

**Principle:** Use the `flag` package for parsing, not raw `os.Args` iteration. Flags are typed, validated, and self-documenting.

**Do:**
- Define typed flags with `flag.Bool`, `flag.Int`, `flag.String`; call `flag.Parse()` once at startup.
- Use `flag.NewFlagSet(name, ErrorHandling)` when you need subcommands or non-default error handling (`ContinueOnError`, `ExitOnError`, `PanicOnError`).
- In systems utilities, default to `ExitOnError` so the program exits on a bad flag.
- Remember `os.Args[0]` is the program name; real args start at `os.Args[1]`.

**Don't:**
- Ignore parse errors in production systems tools.
- Manually string-split `os.Args` when `flag` covers your needs.

**Code** — typed flags parsed once:
```go
var minusO = flag.Bool("o", false, "o flag")
var minusC = flag.Int("c", 0, "c flag")
flag.Parse()
```
*Ref: Go_Systems_Programming.md — "The flag Package"*

**Code** — summing integer args via `os.Args` (when flag parsing isn't appropriate):
```go
arguments := os.Args
sum := 0
for i := 1; i < len(arguments); i++ {
    temp, _ := strconv.Atoi(arguments[i])
    sum = sum + temp
}
fmt.Println("Sum:", sum)
```
*Ref: Go_Systems_Programming.md — "Command-Line Arguments"*

---

### Error Handling & Logging  `#systems` `#error-handling`

**Principle:** Always check error values. Use `log` for severity-tiered output; reserve `log.Fatal` for unrecoverable situations.

**Do:**
- Treat a nil error as the only success signal; check every error.
- Use `log.Printf`/`log.Println` (gentle, timestamped), `log.Fatalf` (log + exit), `log.Panicf` (log + stack trace + terminate).
- For multi-mode operations, return multiple errors (e.g. `(result, hardErr, softErr)`).
- Use `strace(1)` (Linux) / `DTrace` (macOS) to debug system-call failures.

**Don't:**
- Discard errors with `_` in systems code.
- Use `log.Fatal` for recoverable conditions.

**Code** — multiple return values for distinct error kinds:
```go
func division(x, y int) (int, error, error) {
    if y == 0 {
        return 0, nil, errors.New("Cannot divide by zero!")
    }
    if x%y != 0 {
        remainder := errors.New("There is a remainder!")
        return x / y, remainder, nil
    }
    return x / y, nil, nil
}
```
*Ref: Go_Systems_Programming.md — "Error Handling in Go"*

---

### Files & Directories (`os`, `path/filepath`)  `#systems` `#io`

**Principle:** Use `os.Stat`/`os.Lstat` to check existence and follow (or not) symlinks. Use `filepath.Walk` for traversal and `filepath.Join` for portable path construction.

**Do:**
- Use `os.Stat` to confirm a path exists; `os.Lstat` when you need symlink info without following.
- Detect symlinks via `s.Mode()&os.ModeSymlink != 0` then `os.Readlink`.
- Inspect permissions via `info.Mode().Perm()`; flag world-writable with `mode.Perm()&0002 != 0`.
- Delete/rename with `os.Remove` / `os.Rename`.
- Implement `pwd(1)` via `os.Getwd()` + `os.Getenv("PWD")`.
- Implement `which(1)` by splitting `os.Getenv("PATH")` on `:` and probing each dir.

**Don't:**
- Trust that a path is stable between `Stat` and use — re-stat inside the walk function on busy filesystems.
- Concatenate paths with string `+`; always use `filepath.Join`.

**Code** — `which(1)` implementation:
```go
path := os.Getenv("PATH")
pathSplit := strings.Split(path, ":")
for _, directory := range pathSplit {
    fullPath := filepath.Join(directory, filename)
    fileInfo, err := os.Stat(fullPath)
    if err == nil && fileInfo.Mode().IsRegular() {
        // Found the executable
    }
}
```
*Ref: Go_Systems_Programming.md — "Developing which(1) in Go"*

**Code** — `filepath.Walk` callback that re-stats defensively:
```go
func walkFunction(path string, info os.FileInfo, err error) error {
    _, err = os.Stat(path)
    if err != nil { return err }
    fmt.Println(path)
    return nil
}

err := filepath.Walk(Path, walkFunction)
```
*Ref: Go_Systems_Programming.md — "Developing find(1) in Go"*

**Code** — directories-only traversal:
```go
func walkFunction(path string, info os.FileInfo, err error) error {
    fileInfo, err := os.Stat(path)
    if err != nil { return err }
    if fileInfo.Mode().IsDir() {
        fmt.Println(path)
    }
    return nil
}
```
*Ref: Go_Systems_Programming.md — "Visiting directories only!"*

**Code** — symlink detection and readlink:
```go
s, err := os.Lstat(path)
if s.Mode()&os.ModeSymlink != 0 {
    link, _ := os.Readlink(path)
}
```
*Ref: Go_Systems_Programming.md — "Symbolic Links"*

**Code** — permission checks and `chmod`:
```go
info, _ := os.Stat(filename)
mode := info.Mode()
if mode.Perm()&0002 != 0 {
    fmt.Println("World-writable!")
}
os.Chmod(filename, 0644)
```
*Ref: Go_Systems_Programming.md — "File Permissions Revisited"*

---

### File I/O: Reading & Writing  `#systems` `#io`

**Principle:** Pick the right strategy for the file size and shape: `io.Copy` for whole-file copies, `bufio.Scanner` for line-oriented reads, `ioutil.ReadFile` for small files, buffer-based loops with configurable size when you need control.

**Do:**
- Use `io.Copy(dst, src)` — simplest and most efficient whole-file copy.
- Use `bufio.Scanner` to iterate lines; `bufio.NewReader(f).ReadString('\n')` when you need a custom delimiter.
- Use `os.OpenFile` with `O_APPEND|O_WRONLY|O_CREATE` for appends.
- Stat before copy to verify the source is a regular file (`sourceFileStat.Mode().IsRegular()`).
- Benchmark buffer sizes: a 16-byte buffer copying 5 GB takes 10+ minutes; a 1 MB buffer completes in ~7 s.

**Don't:**
- Copy byte-by-byte (catastrophic performance).
- Use `ioutil.ReadFile` on huge files (loads entire file into memory).

**Code** — `io.Copy` with regular-file check:
```go
func Copy(src, dst string) (int64, error) {
    sourceFileStat, err := os.Stat(src)
    if err != nil { return 0, err }
    if !sourceFileStat.Mode().IsRegular() {
        return 0, fmt.Errorf("%s is not a regular file", src)
    }
    source, err := os.Open(src)
    if err != nil { return 0, err }
    defer source.Close()
    destination, err := os.Create(dst)
    if err != nil { return 0, err }
    defer destination.Close()
    nBytes, err := io.Copy(destination, source)
    return nBytes, err
}
```
*Ref: Go_Systems_Programming.md — "Using io.Copy"*

**Code** — read entire file (small files only):
```go
input, err := ioutil.ReadFile(sourceFile)
if err != nil { fmt.Println(err); os.Exit(1) }
err = ioutil.WriteFile(destinationFile, input, 0644)
```
*Ref: Go_Systems_Programming.md — "Reading a file all at once!"*

**Code** — append mode:
```go
f, err := os.OpenFile(filename, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
fmt.Fprintf(f, "New data\n")
f.Close()
```
*Ref: Go_Systems_Programming.md — "Putting Data at the End of a File (Appending)"*

**Code** — line-by-line with `bufio.Scanner` (the `wc(1)` / `cat(1)` loop):
```go
scanner := bufio.NewScanner(f)
for scanner.Scan() {
    line := scanner.Text()
    fmt.Println(line)
}
```
*Ref: Go_Systems_Programming.md — "Implementing cat(1) in Go"*

---

### Binary Data & `encoding/binary`  `#systems` `#io`

**Principle:** Use `binary.Write`/`binary.Read` with an explicit byte order (`LittleEndian`/`BigEndian`) for binary file formats and network protocols.

**Code** — endianness conversion:
```go
err := binary.Write(buf, binary.LittleEndian, aNumber)
// ...
buf.Reset()
err = binary.Write(buf, binary.BigEndian, aNumber)
```
*Ref: Go_Systems_Programming.md — "About Binary Files"*

---

### Concurrency with File Locking (`sync.Mutex`)  `#concurrency` `#io`

**Principle:** Guard shared file writes with `sync.Mutex`; pair it with `sync.WaitGroup` so main waits for all writers. Forgetting `Unlock` deadlocks every waiter.

**Do:**
- Use `defer mu.Unlock()` immediately after `mu.Lock()` to guarantee release.
- `wg.Add(n)` before spawning; `defer wg.Done()` inside each goroutine; `wg.Wait()` in main.
- For read-heavy shared data, prefer `sync.RWMutex` (`RLock`/`RUnlock` for readers, `Lock`/`Unlock` for the single writer).

**Don't:**
- Forget `Unlock` — Go's detector will print `fatal error: all goroutines are asleep - deadlock!`.

**Code** — locked file writes with WaitGroup:
```go
var mu sync.Mutex

func writeDataToFile(i int, file *os.File, w *sync.WaitGroup) {
    mu.Lock()
    time.Sleep(time.Duration(random(10, 1000)) * time.Millisecond)
    fmt.Fprintf(file, "From %d, writing %d\n", i, 2*i)
    fmt.Printf("Wrote from %d\n", i)
    w.Done()
    mu.Unlock()
}

var w *sync.WaitGroup = new(sync.WaitGroup)
w.Add(number)
for r := 0; r < number; r++ {
    go writeDataToFile(r, file, w)
}
w.Wait()
```
*Ref: Go_Systems_Programming.md — "File Locking in Go"*

---

### Signals (`os/signal`)  `#systems` `#processes`

**Principle:** Catch signals via a buffered channel + `signal.Notify` + a goroutine consumer. Either enumerate the signals you handle or catch-all and switch on the ones you care about.

**Do:**
- Buffer the signal channel: `make(chan os.Signal, 1)`.
- Catch-all with `signal.Notify(sigs)` (no signal list) then switch inside the goroutine; this is the author's preferred idiom.
- Make one of your handlers actually terminate the program (otherwise you'll need `kill -9`).
- Use SIGUSR1 / SIGINFO (macOS) for non-destructive control: log rotation, progress reports.

**Don't:**
- Forget that `SIGKILL` and `SIGSTOP` cannot be caught.
- Use signal handling on Windows (`os/signal` is not supported there).

**Code** — handling three named signals:
```go
sigs := make(chan os.Signal, 1)
signal.Notify(sigs, os.Interrupt, syscall.SIGTERM, syscall.SIGHUP)
go func() {
    for {
        sig := <-sigs
        switch sig {
        case os.Interrupt:
            handleSignal(sig)
        case syscall.SIGTERM:
            handleSignal(sig)
        case syscall.SIGHUP:
            fmt.Println("Got:", sig)
            os.Exit(-1)
        }
    }
}()
```
*Ref: Go_Systems_Programming.md — "Handling three different signals!"*

**Code** — catch-all with default-ignore:
```go
sigs := make(chan os.Signal, 1)
signal.Notify(sigs)
go func() {
    for {
        sig := <-sigs
        switch sig {
        case os.Interrupt:
            handleSignal(sig)
        case syscall.SIGTERM:
            handleSignal(sig)
            os.Exit(-1)
        case syscall.SIGUSR1:
            handleSignal(sig)
        default:
            fmt.Println("Ignoring:", sig)
        }
    }
}()
```
*Ref: Go_Systems_Programming.md — "Catching every signal that can be handled"*

| Signal         | Default meaning                          | Catchable? |
|----------------|------------------------------------------|------------|
| SIGINT (Ctrl-C)| Interrupt                                | Yes        |
| SIGTERM        | Software termination (`kill` default)    | Yes        |
| SIGHUP         | Hangup on controlling terminal           | Yes        |
| SIGUSR1/2      | User-defined                             | Yes        |
| SIGKILL        | Kill immediately, no cleanup             | No         |
| SIGSTOP        | Stop process                             | No         |

*Ref: Go_Systems_Programming.md — "Unix Processes and Signals"*

---

### Goroutines, Channels & Pipelines  `#concurrency`

**Principle:** "Don't communicate by sharing memory; share memory by communicating." Use goroutines for units of work, channels for coordination, `sync.WaitGroup` to know when they're all done.

**Do:**
- Spawn with `go func(){ ... }()` — goroutines start at ~2 KB stack.
- Use `sync.WaitGroup`: `Add(1)` before spawn, `defer Done()` inside, `Wait()` in main.
- Use unbuffered channels for synchronization (send blocks until receive); buffered channels to absorb producer bursts.
- Compose pipelines: `[g1] --ch1--> [g2] --ch2--> [g3]`.
- Close channels in order from the first stage to terminate a pipeline cleanly.
- Use `select` to multiplex channel operations and `time.After` for timeouts.
- Use `chan struct{}` as a signal-only (zero-byte) channel; `close(sig)` broadcasts.
- Use a nil channel in a `select` to disable that case dynamically.
- Use `runtime.GOMAXPROCS(runtime.NumCPU())` for CPU-bound work (default since Go 1.5 is already `NumCPU`).

**Don't:**
- Capture loop variables by reference in goroutines — pass as parameters.
- Forget `WaitGroup.Done()` (use `defer`) — `Wait()` will block forever.
- Leave a pipeline stage's input channel open — downstream reads will deadlock.

**Code** — WaitGroup pattern:
```go
var wg sync.WaitGroup
for i := 0; i < n; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        // Do work
    }()
}
wg.Wait()
```
*Ref: Go_Systems_Programming.md — "The sync Package"*

**Code** — race-safe loop-variable capture (pass as parameter):
```go
// Buggy: closures capture `i` by reference
for i := 0; i < n; i++ {
    go func() { fmt.Println(i) }()  // RACE
}
// Fix: pass `i` as a parameter
for i := 0; i < n; i++ {
    go func(n int) { fmt.Println(n) }(i)
}
```
*Ref: Go_Systems_Programming.md — "Detecting Race Conditions"*

**Code** — `select` with timeout:
```go
select {
case msg := <-ch1:
    fmt.Println("Received from ch1:", msg)
case msg := <-ch2:
    fmt.Println("Received from ch2:", msg)
case <-time.After(5 * time.Second):
    fmt.Println("Timed out")
}
```
*Ref: Go_Systems_Programming.md — "The select Keyword"*

**Code** — buffered + signal channels:
```go
ch := make(chan int, 10)           // buffer of 10
signal := make(chan struct{})
close(signal)                      // broadcast to all listeners
```
*Ref: Go_Systems_Programming.md — "Buffered Channels" / "Signal Channels"*

---

### Shared Memory: `sync.Mutex` vs `sync.RWMutex`  `#concurrency`

**Principle:** Choose by access pattern: exclusive (Mutex) for write-heavy, reader-writer (RWMutex) for read-heavy.

**Do:**
- `sync.Mutex`: `Lock()`/`Unlock()` — one writer, no concurrent readers.
- `sync.RWMutex`: `RLock()`/`RUnlock()` for many readers, `Lock()`/`Unlock()` for the single writer.
- Embed `sync.RWMutex` in a struct so its methods are promoted.

**Don't:**
- Hold a lock across slow I/O if avoidable — it serializes everyone.

**Code** — `RWMutex` reader/writer pair:
```go
type secret struct {
    sync.RWMutex
    // ... fields ...
}

// Multiple readers:
func (s *secret) read() int {
    s.RLock()
    defer s.RUnlock()
    return s.value
}
// Single writer:
func (s *secret) write(v int) {
    s.Lock()
    defer s.Unlock()
    s.value = v
}
```
*Ref: Go_Systems_Programming.md — "Using sync.RWMutex"*

---

### Race Detection & GOMAXPROCS  `#concurrency` `#testing`

**Principle:** Always run with `-race` during development; tune `GOMAXPROCS` only when measured.

**Do:**
- `go run -race prog.go` (or `go test -race ./...`) — records shared-variable accesses and sync events.
- Default `GOMAXPROCS` = `runtime.NumCPU()` since Go 1.5; leave it alone unless you have data showing otherwise.

*Ref: Go_Systems_Programming.md — "Detecting Race Conditions" / "About GOMAXPROCS"*

---

### Date/Time & Logging  `#systems` `#observability`

**Principle:** Go's reference time is `Mon Jan 2 15:04:05 MST 2006` (not strftime). Use `log` for severity, `log/syslog` for the system log.

**Code** — Go's reference-time formatting:
```go
now := time.Now()
formatted := now.Format("Mon Jan 2 15:04:05 MST 2006")
parsed, _ := time.Parse("2006-01-02", "2017-01-01")
```
*Ref: Go_Systems_Programming.md — "Date and Time Operations"*

**Code** — syslog integration:
```go
sysLog, err := syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, "myProgram")
sysLog.Info("Information message")
sysLog.Notice("Notice message")
sysLog.Warning("Warning message")
```
*Ref: Go_Systems_Programming.md — "Logging in Go"*

---

### Web Clients & Servers (`net/http`)  `#systems` `#networking`

**Principle:** Always set client timeouts; route server requests via `http.ServeMux`.

**Do:**
- Set `http.Client{Timeout: ...}` to avoid hung requests.
- For finer control, use `net.DialTimeout` for connect timeout + `conn.SetDeadline` for read/write.
- Use `json.Marshal`/`Unmarshal` for byte-slice conversion; `json.Encode`/`Decode` for streaming (`io.Writer`/`io.Reader`).
- Use `html/template` (not `text/template`) for HTML output to get contextual auto-escaping.

**Don't:**
- Call `http.Get(url)` with no client timeout in production.

**Code** — HTTP client with timeout:
```go
timeout := time.Duration(5 * time.Second)
client := http.Client{Timeout: timeout}
response, err := client.Get(url)
```
*Ref: Go_Systems_Programming.md — "Web Clients"*

**Code** — small HTTP server with custom mux:
```go
mux := http.NewServeMux()
mux.HandleFunc("/static", staticHandler)
mux.HandleFunc("/dynamic", dynamicHandler)
http.ListenAndServe(":8001", mux)
```
*Ref: Go_Systems_Programming.md — "A Small Web Server"*

---

### TCP / UDP / RPC Networking  `#systems` `#networking`

**Principle:** TCP needs `Listen`+`Accept` (and a goroutine per connection for concurrency). UDP is connectionless: `ListenUDP` + `ReadFromUDP`/`WriteToUDP`. RPC abstracts function calls over TCP.

**Do:**
- Concurrent TCP server: `for { c, _ := l.Accept(); go handleConnection(c) }`.
- Prefer `net.ResolveTCPAddr`+`net.ListenTCP`/`net.DialTCP` when you need socket options on the resulting `TCPConn`.
- For RPC: define a shared interface package; `rpc.Register(impl)` on the server, `rpc.Dial("tcp", addr)` + `client.Call("Iface.Method", args, &reply)` on the client.
- Use `defer l.Close()` on listeners.
- Echo clients/servers via `bufio.NewReader(c).ReadString('\n')` for line-oriented protocols.

**Don't:**
- Write a single-client TCP server (no goroutine per connection) for production.

**Code** — concurrent TCP server:
```go
l, err := net.Listen("tcp", PORT)
if err != nil { fmt.Println(err); os.Exit(100) }
defer l.Close()
for {
    c, err := l.Accept()
    if err != nil { fmt.Println(err); os.Exit(100) }
    go handleConnection(c)
}
```
*Ref: Go_Systems_Programming.md — "Concurrent TCP Server"*

**Code** — TCP client:
```go
c, err := net.Dial("tcp", "localhost:1234")
fmt.Fprintf(c, "Hello\n")
message, _ := bufio.NewReader(c).ReadString('\n')
```
*Ref: Go_Systems_Programming.md — "TCP Client"*

**Code** — UDP server + client:
```go
// Server
s, _ := net.ResolveUDPAddr("udp", ":1234")
conn, _ := net.ListenUDP("udp", s)
n, addr, _ := conn.ReadFromUDP(buffer)
conn.WriteToUDP(data, addr)

// Client
s, _ := net.ResolveUDPAddr("udp", "localhost:1234")
c, _ := net.DialUDP("udp", nil, s)
c.Write(data)
n, _, _ := c.ReadFromUDP(buffer)
```
*Ref: Go_Systems_Programming.md — "UDP Server and Client"*

**Code** — RPC shared interface, server, client:
```go
// sharedRPC.go
type MyInts struct { A1, A2 uint; S1, S2 bool }
type MyInterface interface {
    Add(arguments *MyInts, reply *int) error
    Subtract(arguments *MyInts, reply *int) error
}

// RPCserver.go
rpc.Register(myInterface)
l, _ := net.ListenTCP("tcp", t)
for { c, _ := l.Accept(); rpc.ServeConn(c) }

// RPCclient.go
c, _ := rpc.Dial("tcp", CONNECT)
err = c.Call("MyInterface.Add", args, &reply)
```
*Ref: Go_Systems_Programming.md — "Remote Procedure Call (RPC)"*

---

### Unix Domain Sockets  `#systems` `#networking`

**Principle:** Same-machine IPC via `net.Listen("unix", path)` / `net.Dial("unix", path)`; reuse the `io.Reader`/`io.Writer` interface on the resulting `net.Conn`.

**Code:**
```go
// Server
l, _ := net.Listen("unix", socketFile)
// Client
c, _ := net.Dial("unix", socketFile)
```
*Ref: Go_Systems_Programming.md — "Unix Sockets in Go"*

---

### Unix Pipes  `#systems` `#processes`

**Principle:** `os.Pipe()` returns a reader/writer pair for in-process IPC; combine with goroutines for streaming pipelines.

**Code:**
```go
r, w, _ := os.Pipe()
w.WriteString("data through pipe\n")
w.Close()
// Read from r
```
*Ref: Go_Systems_Programming.md — "Unix Pipes in Go"*

---

### Regular Expressions  `#systems`

**Principle:** `regexp.Compile` (returns error) for dynamic patterns, `regexp.MustCompile` (panics) for compile-time-constant patterns. Combine with `strings.Fields` for column extraction.

**Code:**
```go
parse, err := regexp.Compile("[Mm]ihalis")
if err == nil {
    parse.MatchString("Mihalis Tsoukalos")           // true
    parse.ReplaceAllString("mihalis Mihalis", "MIHALIS")
}
```
*Ref: Go_Systems_Programming.md — "Pattern Matching and Regular Expressions"*

---

## Anti-Patterns & Common Mistakes

- **Ignoring error returns** with `_` — silent failures in systems code. → *fix:* always check, even if you only log.
- **Forgetting slices are reference types** — modifying a slice in a function mutates the caller's backing array.
- **Skipping `defer` for cleanup** — files/mutexes leak on early return. → *fix:* `defer f.Close()` / `defer mu.Unlock()` immediately after acquisition.
- **Capturing loop variables in goroutines by reference** — classic data race. → *fix:* pass as parameter.
- **Forgetting `Unlock`** — every goroutine deadlocks (`fatal error: all goroutines are asleep - deadlock!`).
- **Leaving pipeline input channels open** — downstream `range`/reads block forever. → *fix:* close in first stage.
- **Byte-at-a-time file copy** — orders of magnitude slower than buffered or `io.Copy`.
- **`ioutil.ReadFile` on multi-GB files** — OOM risk.
- **No timeout on `http.Get`** — request can hang indefinitely.
- **Single-client TCP server** (no goroutine per connection) — fails under concurrent load.
- **Not using `filepath.Join`** — breaks portability across OS separators.
- **Not handling `SIGINT`/`SIGTERM`** — ungraceful shutdown, lost state.

---

## Decision Heuristics / Checklists

### File-copy strategy
- Small file, simple need → `ioutil.ReadFile`/`WriteFile`.
- Whole-file copy, any size → `io.Copy` (let the runtime handle buffering).
- Need block/count semantics (`dd`-like) → buffer-based loop with configurable size.
- Need streaming transform → `bufio.Reader`/`bufio.Writer` chain.

### Sync primitive choice
- "Wait for N goroutines" → `sync.WaitGroup`.
- "Coordinate / pass data" → channels.
- "Mutate shared state" → `sync.Mutex` (write-heavy) or `sync.RWMutex` (read-heavy).
- "Multiplex channel ops / timeout" → `select`.

### Network protocol choice
- Reliable ordered bytes on a connection → TCP.
- Fire-and-forget datagrams → UDP.
- Same-machine IPC, lower overhead → Unix domain socket.
- Remote function-call abstraction over TCP → `net/rpc`.

### Signal handler design
- Known small set → `signal.Notify(sigs, sig1, sig2, ...)`.
- Many signals, mostly ignored → `signal.Notify(sigs)` + `switch` with `default: ignore`.
- Always make one handler terminate (or you'll need `kill -9`).

### Buffer-size checklist for streaming I/O
- [ ] Default 16 B / 4 KB is too small for bulk transfer.
- [ ] Try 64 KB → 1 MB and benchmark; `time ./prog` is sufficient.
- [ ] Larger isn't always better — measure with realistic input.

---

## Key Takeaways

1. **Go is well-suited for systems programming** — static binaries, GC, built-in concurrency.
2. **Error handling is non-negotiable** — check every error; never `_` it away in systems code.
3. **The stdlib is remarkably complete** — `os`, `io`, `bufio`, `path/filepath`, `net`, `net/http`, `encoding/json`, `encoding/binary`, `regexp`, `os/signal`, `sync` cover almost everything.
4. **`io.Reader` / `io.Writer` are the foundation** — understanding them unlocks the entire I/O ecosystem.
5. **Prefer `flag` over raw `os.Args`** for typed, validated, self-documenting CLI parsing.
6. **Prefer `io.Copy` and `bufio.Scanner`** over byte-at-a-time loops; benchmark buffer sizes.
7. **Concurrency model: goroutines + channels** — "share memory by communicating"; `WaitGroup` to know when done.
8. **Pick the right sync primitive** — WaitGroup (wait), channels (communicate), Mutex/RWMutex (shared state), `select` (multiplex).
9. **Race conditions are easy to make, hard to debug** — always run `go run -race`.
10. **Signal handling enables robust daemons** — log rotation, progress, graceful shutdown via `os/signal`.
11. **Network programming follows consistent patterns** — TCP: `Listen`+`Accept`+goroutine; UDP: `ListenUDP`+`ReadFromUDP`; RPC: shared interface + `rpc.Register`/`rpc.Dial`.
12. **Always set HTTP client timeouts** — both connect (`net.DialTimeout`) and read/write (`conn.SetDeadline` or `http.Client{Timeout}`).
13. **Pipelines need orderly shutdown** — close channels from the first stage.
14. **Build real Unix tools to learn** — `pwd`, `which`, `find`, `wc`, `cp`, `dd`, `cat` teach both Go and Unix internals.
15. **Go compiles to self-contained static binaries** — trivial deployment vs. interpreted languages.

---

## Cross-References
- Related: [[../Building_Modern_CLI_Applications_in_Go.md]]
- Related: [[../System_Programming_Essentials_with_Go.md]]
- Topic index: [[../INDEX.md]]
