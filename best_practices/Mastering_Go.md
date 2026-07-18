# Mastering Go
**Author:** Mihalis Tsoukalos
**Topic tags:** `#concurrency` `#testing` `#cli` `#systems` `#api` `#general`
**Language focus:** Go-first
**Sources:** `markdown_output/Mastering_Go_-_Mihalis_Tsoukalos/Mastering_Go_-_Mihalis_Tsoukalos.md` · `summaries/Mastering_Go_-_Mihalis_Tsoukalos.md`

## TL;DR
Tsoukalos's *Mastering Go* is a deep, idiomatic tour of the Go runtime and standard library: goroutines/channels/context, the `sync` and `testing` packages, signal/file/network plumbing, and TCP/UDP/RPC servers. It is the right book when you need to understand *how* Go works under the hood and want vetted, runnable idioms rather than framework recipes. Apply its rules when building systems services, CLI tools, network daemons, or any Go program that has to be correct under concurrency and on Unix.

---

## Best Practices by Topic

### Goroutine Lifecycle and `sync.WaitGroup`

**Principle:** Spawn goroutines deliberately and synchronize their completion with `sync.WaitGroup`, never with `time.Sleep`.

**Do:**
- Call `wg.Add(n)` *before* the `go` statement that creates the worker — this prevents a race where the goroutine finishes before `Add` is called.
- Pair every `wg.Add(1)` with exactly one `wg.Done()` inside the goroutine (use `defer`).
- Spawn enough workers to match actual concurrency (e.g. `runtime.NumCPU()`), not arbitrary numbers.

**Don't:**
- Don't use `time.Sleep` to wait for goroutines — "this kind of code can cause nasty and unpredictable bugs down the road."
- Don't call `Done` more times than `Add` (causes `panic: sync: negative WaitGroup counter`).
- Don't rely on goroutine execution order — it is non-deterministic.

**Code:**
```go
var waitGroup sync.WaitGroup
for i := 0; i < count; i++ {
    waitGroup.Add(1)            // Must be BEFORE the go statement
    go func(x int) {
        defer waitGroup.Done()  // Decrements counter when goroutine finishes
        fmt.Printf("%d ", x)
    }(i)
}
waitGroup.Wait()               // Blocks until counter is zero
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Goroutines / Creating a goroutine / Waiting for your goroutines to finish"*

---

### Channels: Direction, Closing, and Signal Channels

**Principle:** Channels connect goroutines. Use directional channel types at function boundaries, close only from the sender, and use unbuffered/signal channels for orchestration.

**Do:**
- Declare directional parameters `chan<- int` (send-only) or `<-chan int` (receive-only) to make misuse a compile error.
- Use a `struct{}` signal channel when you want zero-data signaling — "no data can be sent to it, which can save you from bugs and misconceptions."
- Read with `_, ok := <-c` to test whether the channel is still open.

**Don't:**
- Don't write to a closed channel — it panics.
- Don't close a `nil` channel — it panics (`close of nil channel`).
- Don't write to a channel with no reader — the goroutine blocks forever.

**Code:**
```go
// Unidirectional channels as function parameters — compile-time safety
func f1(out chan<- int64, in <-chan int64) {  // out: send-only, in: receive-only
    fmt.Println(x)
    c <- x
}
// Read with open/closed detection
_, ok := <-c
if ok {
    fmt.Println("Channel is open!")
} else {
    fmt.Println("Channel is closed!")
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Channels / Writing to a channel / Reading from a channel / Channels as function parameters"*

---

### Pipelines with `close()` to Signal Termination

**Principle:** Each pipeline stage must `close()` its outbound channel when finished; downstream stages terminate their `for range` loop on EOF.

**Do:**
- Close the output channel when the stage decides no more values will be produced.
- Iterate downstream with `for x := range in { ... }` — the loop ends naturally when `in` is closed.

**Code:**
```go
func second(out chan<- int, in <-chan int) {
    for x := range in {
        fmt.Print(x, " ")
        _, ok := DATA[x]
        if ok {
            CLOSEA = true             // Tell first() to stop
        } else {
            DATA[x] = true
            out <- x
        }
    }
    fmt.Println()
    close(out)                     // Signal downstream: no more values
}

func third(in <-chan int) {
    var sum int
    sum = 0
    for x2 := range in {           // Terminates when second() closes its out
        sum = sum + x2
    }
    fmt.Printf("The sum of the random numbers is %d\n", sum)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Pipelines"*

---

### `select`, Timeouts, and `time.After`

**Principle:** Use `select` to wait on multiple channel operations; combine with `time.After` to bound waiting, and `time.After(4 * time.Second)` inside a select is a "clever default branch."

**Do:**
- Treat `time.After(d)` in a `select` as a timeout branch — it unblocks the select if every other channel is blocked.
- Pick a timeout value "appropriate" to the operation; too short produces spurious timeouts.

**Don't:**
- Don't omit the timeout when calling external systems — "you will not be able to follow this section without first downloading the context package" applies broadly to any blocking operation.

**Code:**
```go
select {
case createNumber <- rand.Intn(max-min) + min:
case <-end:
    close(end)
    return
case <-time.After(4 * time.Second):
    fmt.Println("n\time.After()!")
}
// Random selection across ready channels; if multiple ready, Go picks uniformly.
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The select keyword"*

---

### Goroutine Ordering with Signal Channels

**Principle:** Use closed-channel signalling (not shared counters) to force deterministic execution order across goroutines.

**Code:**
```go
func A(a, b chan struct{}) {
    <-a                          // Block until a is closed
    fmt.Println("A()!")
    time.Sleep(time.Second)
    close(b)                     // Unblock the next stage
}
func main() {
    x := make(chan struct{})
    y := make(chan struct{})
    z := make(chan struct{})
    go C(z)
    go A(x, y)                    // x triggers A
    go C(z)
    go B(y, z)                    // A's close(y) triggers B
    go C(z)
    close(x)                      // Kick off A
    time.Sleep(3 * time.Second)
}
// Output: A()! / B()! / C()! / C()! / C()!
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Specifying the order of execution for your goroutines"*

---

### Buffered Channels as Semaphores

**Principle:** A buffered channel of capacity N gates a pool to N concurrent workers — use it to bound throughput, not for queuing.

**Code:**
```go
numbers := make(chan int, 5)     // Buffer of 5
for i := 0; i < counter; i++ {
    select {
    case numbers <- i:
    default:
        fmt.Println("Not enough space for", i)  // Buffer full → back-pressure
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Buffered channels"*

---

### Nil Channels as `select` Disablers

**Principle:** Assign `nil` to a channel variable to permanently disable that `case` in a `select` — used to "turn off" a branch after it has done its job.

**Code:**
```go
func add(c chan int) {
    sum := 0
    t := time.NewTimer(time.Second)
    for {
        select {
        case input := <-c:
            sum = sum + input
        case <-t.c:
            c = nil              // Disables the receive branch permanently
            fmt.Println(sum)
        }
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Nil channels"*

---

### Worker Pools with Buffered Channels

**Principle:** A fixed-size pool of worker goroutines reading from a buffered jobs channel bounds concurrency and resource usage.

**Do:**
- Buffer the jobs and results channels (prevents unnecessary blocking).
- Close the jobs channel from the producer to drain workers naturally with `for c := range clients`.

**Code:**
```go
var (
    size    = 10
    clients = make(chan Client, size)   // jobs
    data    = make(chan Data, size)     // results
)
func worker(w *sync.WaitGroup) {
    for c := range clients {            // Exits when clients is closed
        square := c.integer * c.integer
        output := Data{c, square}
        data <- output
        time.Sleep(time.Second)
    }
    w.Done()
}
func makeWP(n int) {
    var w sync.WaitGroup
    for i := 0; i < n; i++ {
        w.Add(1)
        go worker(&w)
    }
    w.Wait()
    close(data)
}
func create(n int) {
    for i := 0; i < n; i++ {
        c := Client{i, i}
        clients <- c
    }
    close(clients)                       // Workers exit after consuming all
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Worker pools"*

---

### Monitor Goroutine: Share by Communicating

**Principle:** Prefer one goroutine owning the shared state and serving read/write via channels, instead of `sync.Mutex` everywhere. "Personally, I prefer to use a monitor goroutine instead of the traditional shared memory techniques because the implementation that uses the monitor goroutine is safer and closer to the Go philosophy."

**Code:**
```go
var readValue = make(chan int)
var writeValue = make(chan int)

func set(newValue int)    { writeValue <- newValue }
func read() int           { return <-readValue }

func monitor() {
    var value int
    for {
        select {
        case newValue := <-writeValue:
            value = newValue
            fmt.Printf("%d ", value)
        case readValue <- value:
        }
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Sharing memory using goroutines"*

---

### `sync.Mutex` and `sync.RWMutex`

**Principle:** When you must share memory, use `sync.Mutex` for exclusive access and `sync.RWMutex` when many readers and few writers exist. Always `defer Unlock()`.

**Don't:**
- Don't forget `Unlock` — even a single missing unlock causes `fatal error: all goroutines are asleep - deadlock!`.
- Don't nest critical sections guarded by the *same* mutex ("avoid, at almost any cost, spreading mutexes across functions").

**Code:**
```go
var Password = secret{password: "myPassword"}
type secret struct {
    RWM     sync.RWMutex
    M       sync.Mutex
    password string
}

func Change(c *secret, pass string) {
    c.RWM.Lock()                       // Exclusive for write
    fmt.Println("LChange")
    time.Sleep(10 * time.Second)
    c.password = pass
    c.RWM.Unlock()
}

func show(c *secret) string {
    c.RWM.RLock()                      // Many concurrent readers OK
    fmt.Print("show")
    time.Sleep(3 * time.Second)
    defer c.RWM.RUnlock()
    return c.password
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The sync.Mutex type / The sync.RWMutex type"*

Benchmark: `sync.RWMutex` reader path was ~22s vs `sync.Mutex` ~51s for the same 15-goroutine test.

---

### Race Conditions and `go run -race`

**Principle:** Race conditions "occur when two or more running elements ... access the same variable concurrently and at least one access is a write." Detect them with the race detector before they ship.

**Don't:**
- Don't loop over a shared variable from goroutines without synchronizing — even reading it inside a closure that "captures" the loop variable by closure (not by parameter) reads the final value.

**Code:**
```go
// WRONG: closure captures the loop variable, sees final value
for i := 0; i < numGR; i++ {
    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        k[i] = i                  // data race: i is shared + write
    }()
}

// RIGHT: pass i as parameter
for i = 0; i < numGR; i++ {
    waitGroup.Add(1)
    go func(j int) {
        defer waitGroup.Done()
        aMutex.Lock()
        k[j] = j
        aMutex.Unlock()
    }(i)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Catching race conditions"*

---

### The `context` Package

**Principle:** Use `context.Context` to carry cancellation, deadlines, and request-scoped values across API and goroutine boundaries. Every long-running operation should accept a `context.Context` as its first parameter.

**Do:**
- Always `defer cancel()` after `context.WithTimeout`/`context.WithCancel`.
- Pass `ctx` as the first parameter to functions; treat it as a request-scoped handle.

**Don't:**
- Don't implement `context.Context` yourself — modify via `WithCancel`/`WithTimeout`/`WithDeadline`/`WithValue`.

**Code:**
```go
func f2(t int) {
    c2 := context.Background()
    c2, cancel := context.WithTimeout(c2, time.Duration(t)*time.Second)
    defer cancel()                              // Always release the resources
    go func() {
        time.Sleep(4 * time.Second)
        cancel()                                // Manual early cancel
    }()
    select {
    case <-c2.Done():
        fmt.Println("f2():", c2.Err())          // context.DeadlineExceeded
        return
    case r := <-time.After(time.Duration(t) * time.Second):
        fmt.Println("f2():", r)
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The context package / An advanced example of the context package"*

---

### `flag` Package for CLIs

**Principle:** Use the `flag` package (standard library, well-tested) for all non-trivial CLIs; it produces automatic usage messages and handles ordering.

**Do:**
- Always call `flag.Parse()` after defining flags.
- Use `flag.Var()` to support custom types via the `flag.Value` interface (`String()` + `Set(string) error`).
- Use `flag.Args()` to read remaining positional arguments after flags are consumed.

**Code:**
```go
func main() {
    minusK := flag.Bool("k", true, "k")         // default true
    minusO := flag.Int("O", 1, "O")            // default 1
    flag.Parse()
    valueK := *minusK
    valueO := *minusO
    valueO++
    fmt.Println("-k:", valueK)
    fmt.Println("-O:", valueO)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The flag package"*

---

### Custom Flag Types via `flag.Value`

**Principle:** Implement `String() string` + `Set(string) error` to register any type with `flag.Var()`.

**Code:**
```go
type Value interface {
    String() string
    Set(string) error
}

type NamesFlag struct{ Names []string }
func (s *NamesFlag) String() string     { return fmt.Sprint(s.Names) }
func (s *NamesFlag) Set(v string) error {
    if len(s.Names) > 0 {
        return fmt.Errorf("Cannot use names flag more than once!")
    }
    for _, item := range strings.Split(v, ",") {
        s.Names = append(s.Names, item)
    }
    return nil
}
// Usage:
flag.Var(&manyNames, "names", "Comma-separated list")
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The flag package" (custom types)*

---

### Unix Signal Handling with `os/signal`

**Principle:** Signals arrive asynchronously; catch them with `signal.Notify` driving a channel, then dispatch with a `switch`. Always handle `SIGTERM` (and `os.Interrupt`) for graceful shutdown.

**Do:**
- Use `signal.Notify(c, os.Interrupt, syscall.SIGTERM, ...)` — only the listed signals are delivered.
- Use `signal.Notify(c)` (no args) to receive *all* signals — much safer default.
- Map one signal to "do cleanup and exit" (e.g. `os.Exit(0)` on `SIGTERM`).

**Code:**
```go
func main() {
    sigs := make(chan os.Signal, 1)
    signal.Notify(sigs)                        // Catch EVERY signal
    go func() {
        for {
            sig := <-sigs
            switch sig {
            case os.Interrupt:
                handle(sig)
            case syscall.SIGTERM:
                handle(sig)
                os.Exit(0)                     // Graceful shutdown
            case syscall.SIGUSR2:
                fmt.Println("Handling syscall.SIGUSR2!")
            default:
                fmt.Println("Ignoring:", sig)
            }
        }
    }()
    for {
        fmt.Printf(".")
        time.Sleep(30 * time.Second)
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Handling Unix signals / Handling all signals"*

---

### File I/O with `bufio` + `defer Close`

**Principle:** Always `defer f.Close()` after a successful `os.Open` and use `bufio.NewReader` for line-by-line reading via `r.ReadString('\n')`.

**Code:**
```go
func lineByLine(file string) error {
    var err error
    f, err := os.Open(file)
    if err != nil {
        return err
    }
    defer f.Close()                            // Closes even on early return
    r := bufio.NewReader(f)
    for {
        line, err := r.ReadString('\n')        // Read until '\n' = line by line
        if err == io.EOF {
            break
        } else if err != nil {
            fmt.Printf("error reading file %s", err)
            break
        }
        fmt.Print(line)                        // fmt.Print — newline is in line
    }
    return nil
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Reading text files / Reading a text file line by line"*

---

### Serialization with `encoding/gob`

**Principle:** Use `encoding/gob` for Go-to-Go persistence — it is built in, efficient, and handles all the dirty work.

**Code:**
```go
func save() error {
    fmt.Println("Saving", DATAFILE)
    err := os.Remove(DATAFILE)                 // Remove old; gob overwrites cleanly
    if err != nil { fmt.Println(err) }
    saveTo, err := os.Create(DATAFILE)
    if err != nil {
        return err
    }
    defer saveTo.Close()
    encoder := gob.NewEncoder(saveTo)
    return encoder.Encode(DATA)
}

func load() error {
    loadFrom, err := os.Open(DATAFILE)
    defer loadFrom.Close()
    if err != nil { return err }
    decoder := gob.NewDecoder(loadFrom)
    return decoder.Decode(&DATA)
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Loading and saving data on disk"*

---

### File Permissions via `os.FileMode`

**Principle:** `os.Stat(path).Mode()` exposes Unix permission bits; print `mode.String()[1:10]` for the `rwxrwxrwx` portion.

**Code:**
```go
filename := arguments[1]
info, _ := os.Stat(filename)
mode := info.Mode()
fmt.Println(filename, "mode is", mode.String()[1:10])
// /tmp/adobegc.log mode is rw-rw-rw-
// /dev/random mode is crw-rw-rw
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "File permissions"*

---

### Directory Traversal with `filepath.Walk`

**Principle:** Use `filepath.Walk(path, walkFn)` to recursively traverse a tree — `os.FileInfo` exposes `IsRegular()` and `IsDir()` for filtering.

**Code:**
```go
func walk(path string, info os.FileInfo, err error) error {
    fileInfo, err := os.Stat(path)
    if err != nil { return err }
    mode := fileInfo.Mode()
    if mode.IsRegular() && minusF { fmt.Println("+", path); return nil }
    if mode.IsDir() && minusD      { fmt.Println("*", path); return nil }
    fmt.Println(path)
    return nil
}
err := filepath.Walk(Path, walk)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Traversing directory trees"*

---

### Unix Pipes: A `cat(1)` Clone

**Principle:** Read from stdin when no file argument is supplied so the program composes with Unix pipes.

**Code:**
```go
func main() {
    arguments := os.Args
    if len(arguments) == 1 {
        io.Copy(os.Stdout, os.Stdin)          // No args → read from stdin (pipes)
        return
    }
    for i := 1; i < len(arguments); i++ {
        filename := arguments[i]
        if err := printFile(filename); err != nil {
            fmt.Println(err)
        }
    }
}
// Composes: cat.go /tmp/a.log /tmp/b.log | wc
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Programming Unix pipes in Go / Implementing the cat(1) utility in Go"*

---

### HTTP Server with `http.HandleFunc` and `http.ListenAndServe`

**Principle:** A handler is `func(http.ResponseWriter, *http.Request)`. Register with `http.HandleFunc` and serve with `http.ListenAndServe`. The default `ServeMux` dispatches by longest-prefix match.

**Code:**
```go
func myHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Serving: %s\n", r.URL.Path)
    fmt.Printf("Served: %s\n", r.Host)
}
func timeHandler(w http.ResponseWriter, r *http.Request) {
    t := time.Now().Format(time.RFC1123)
    fmt.Fprintf(w, "<h1 align=\"center\">The current time is:</h1>")
    fmt.Fprintf(w, "<h2 align=\"center\">%s</h2>\n", t)
    fmt.Fprintf(w, "Serving: %s\n", r.URL.Path)
}
func main() {
    PORT := ":8001"
    arguments := os.Args
    if len(arguments) == 1 {
        fmt.Println("Using default port number: ", PORT)
    } else { PORT = ":" + arguments[1] }
    http.HandleFunc("/time", timeHandler)        // Specific prefix
    http.HandleFunc("/", myHandler)              // Catches everything else
    err := http.ListenAndServe(PORT, nil)
    if err != nil { fmt.Println(err); return }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating a web server in Go"*

---

### HTTP Profiling via `net/http/pprof`

**Principle:** Importing `net/http/pprof` registers profiling handlers under `/debug/pprof/`. Pair with `go tool pprof http://host/debug/pprof/profile`.

**Code:**
```go
import (
    "net/http"
    "net/http/pprof"
)
func main() {
    PORT := ":8001"
    r := http.NewServeMux()
    r.HandleFunc("/time", timeHandler)
    r.HandleFunc("/", myHandler)
    // Register pprof handlers when using your own mux
    r.HandleFunc("/debug/pprof/", pprof.Index)
    r.HandleFunc("/debug/pprof/cmdline", pprof.Cmdline)
    r.HandleFunc("/debug/pprof/profile", pprof.Profile)
    r.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
    r.HandleFunc("/debug/pprof/trace", pprof.Trace)
    http.ListenAndServe(PORT, r)
}
// Capture: go tool pprof http://localhost:1234/debug/pprof/profile
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Profiling an HTTP server"*

---

### HTTP Server Timeouts

**Principle:** Always set `ReadTimeout` and `WriteTimeout` on `http.Server` — bugs in clients and DOS attacks both lead to slow connections that will silently leak resources otherwise.

**Code:**
```go
srv := &http.Server{
    Addr:         PORT,
    Handler:      m,
    ReadTimeout:  3 * time.Second,            // Max to read entire request incl. body
    WriteTimeout: 3 * time.Second,            // From end-of-headers to end-of-response
}
m.HandleFunc("/time", timeHandler)
m.HandleFunc("/", myHandler)
err := srv.ListenAndServe()
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Setting the timeout period on the server side"*

---

### HTTP Client with `context.WithTimeout`

**Principle:** For client-side timeout, the simplest form is `http.Client{Timeout: duration}`. For per-call control, wrap the request in a goroutine with a `select` on `ctx.Done()`.

**Code:**
```go
client := http.Client{ Timeout: timeout }
data, err := client.Get(URL)
if err != nil {
    fmt.Println(err)
    return
} else {
    defer data.Body.Close()
    _, err := io.Copy(os.Stdout, data.Body)
    if err != nil { fmt.Println(err); return }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Yet another way to time out!"*

---

### Fine-grained HTTP Timeout via `http.Transport`

**Principle:** Override `http.Transport.Dial` with a function that sets a per-connection deadline when you need lower-level control than `Client.Timeout`.

**Code:**
```go
func Timeout(network, host string) (net.Conn, error) {
    conn, err := net.DialTimeout(network, host, timeout)
    if err != nil { return nil, err }
    conn.SetDeadline(time.Now().Add(timeout))    // Apply deadline to the conn
    return conn, nil
}
// Then:
t := http.Transport{ Dial: Timeout }
client := http.Client{ Transport: &t }
data, err := client.Get(URL)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Timing out HTTP connections"*

---

### HTTP Handler Testing with `httptest.NewRecorder`

**Principle:** Test handlers with `httptest.NewRecorder` + `http.NewRequest` + `handler.ServeHTTP(rr, req)`. No real socket required.

**Code:**
```go
func TestCheckStatusOK(t *testing.T) {
    req, err := http.NewRequest("GET", "/CheckStatusOK", nil)
    if err != nil { fmt.Println(err); return }
    rr := httptest.NewRecorder()                // Captures the response
    handler := http.HandlerFunc(CheckStatusOK)
    handler.ServeHTTP(rr, req)                  // Run synchronously
    status := rr.Code
    if status != http.StatusOK {
        t.Errorf("handler returned %v", status)
    }
    expect := `Fine!`
    if rr.Body.String() != expect {
        t.Errorf("handler returned %v", rr.Body.String())
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Testing HTTP handlers"*

---

### TCP Server Concurrency

**Principle:** For each accepted connection, spawn a goroutine. Each goroutine owns its connection until `Close`.

**Code:**
```go
func handleConnection(c net.Conn) {
    for {
        netData, err := bufio.NewReader(c).ReadString('\n')
        if err != nil { fmt.Println(err); os.Exit(100) }
        temp := strings.TrimSpace(string(netData))
        if temp == "STOP" { break }
        fibo := "-1\n"
        n, err := strconv.Atoi(temp)
        if err == nil {
            fibo = strconv.Itoa(f(n)) + "\n"
        }
        c.Write([]byte(string(fibo)))
    }
    time.Sleep(5 * time.Second)   // Allow output to drain
    c.Close()
}

func main() {
    PORT := ":" + arguments[1]
    l, err := net.Listen("tcp4", PORT)
    if err != nil { fmt.Println(err); return }
    defer l.Close()
    for {
        c, err := l.Accept()
        if err != nil { fmt.Println(err); return }
        go handleConnection(c)              // Concurrent per-client goroutine
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "A concurrent TCP server"*

---

### RPC Server and Client

**Principle:** Implement the server-side interface; register it; expose over HTTP. Client uses `rpc.Dial` and `client.Call("Type.Method", args, &reply)`.

**Code:**
```go
// Shared types (sharedRPC.go)
type MyFloats struct { A1, A2 float64 }
type MyInterface interface {
    Multiply(arguments *MyFloats, reply *float64) error
    Power(arguments *MyFloats, reply *float64) error
}

// Server (RPCServer.go)
type MyInterface struct{}
func (t *MyInterface) Multiply(args *sharedRPC.MyFloats, reply *float64) error {
    *reply = args.A1 * args.A2
    return nil
}
func (t *MyInterface) Power(args *sharedRPC.MyFloats, reply *float64) error {
    *reply = math.Pow(args.A1, args.A2)
    return nil
}

func main() {
    PORT := ":1234"
    myInterface := new(MyInterface)
    rpc.Register(myInterface)                  // Registers exported methods
    t, _ := net.ResolveTCPAddr("tcp4", PORT)
    l, _ := net.ListenTCP("tcp4", t)
    for {
        c, err := l.Accept()
        if err != nil { continue }
        fmt.Printf("%s\n", c.RemoteAddr())
        rpc.ServeConn(c)
    }
}

// Client (RPCclient.go)
c, _ := rpc.Dial("tcp", CONNECT)
args := sharedRPC.MyFloats{16, -0.5}
var reply float64
c.Call("MyInterface.Multiply", args, &reply)
c.Call("MyInterface.Power", args, &reply)
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Remote Procedure Call (RPC) / The RPC client / The RPC server"*

---

### CPU Profiling with `runtime/pprof`

**Principle:** To profile Go code, import `runtime/pprof` directly or indirectly, and write a CPU profile to a file. Analyze with `go tool pprof`.

**Code:**
```go
import "runtime/pprof"

func main() {
    cpuFile, err := os.Create("/tmp/cpuProfile.out")
    if err != nil { fmt.Println(err); return }
    pprof.StartCPUProfile(cpuFile)
    defer pprof.StopCPUProfile()               // Stops on function return
    total := 0
    for i := 2; i < 100000; i++ {
        n := N1(i)
        if n { total = total + 1 }
    }
    fmt.Println("Total primes:", total)
    // ... more work ...
    runtime.GC()
    // Memory profiling
    memory, _ := os.Create("/tmp/memoryProfile.out")
    defer memory.Close()
    pprof.WriteHeapProfile(memory)
}
// Inspect interactively:
//   go tool pprof /tmp/cpuProfile.out
//   (pprof) top            -- top 10 by self time
//   (pprof) list main.N1   -- annotated source
//   (pprof) top --cum      -- cumulative
// Web UI:
//   go tool pprof -http=:8080 /tmp/cpuProfile.out
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Profiling Go code / A simple profiling example"*

---

### Execution Tracing with `runtime/trace`

**Principle:** `runtime/trace` records goroutine creation/blocking/unblocking, syscalls, GC events, and processor state. View in browser with `go tool trace`.

**Code:**
```go
import "runtime/trace"

func main() {
    f, err := os.Create("/tmp/traceFile.out")
    if err != nil { panic(err) }
    defer f.Close()
    err = trace.Start(f)
    if err != nil { fmt.Println(err); return }
    defer trace.Stop()                         // Always stop before exit
    // ... do work ...
}
// View: go tool trace /tmp/traceFile.out
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "The go tool trace utility"*

---

### Unit Testing Conventions

**Principle:** Test files end with `_test.go`, package may be `<pkg>_test` (black-box), functions start with `Test` and take `*testing.T`.

**Do:**
- Use `package <name>_test` for black-box tests (cannot access unexported).
- Use `t.Errorf` for non-fatal and `t.Fatalf` for fatal failures.
- Use `go test -run=Name` to filter.

**Don't:**
- Don't ignore errors in production code just to save space — `strconv.Atoi` errors "should never be done in real applications."

**Code:**
```go
package testMe
import "testing"
func TestS1(t *testing.T) {
    if s1("123456789") != 9 {
        t.Error(`s1("123456789") != 9`)
    }
    if s1("") != 0 {
        t.Error(`s1("") != 0`)
    }
}
func TestF1(t *testing.T) {
    if f1(10) != 55 {
        t.Error(`f1(10) != 55`)
    }
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Testing Go code / Writing tests for existing Go code"*

---

### Benchmarking

**Principle:** Functions named `Benchmark*` taking `*testing.B` run with `go test -bench=.`. Capture results in a package-level variable to defeat dead-code elimination.

**Don't:**
- Don't make the input size depend on `b.N` — the framework scales `b.N` and you'll never converge.
- Don't compute the result without using it (compiler will optimize it away).

**Code:**
```go
var result int                                    // Package-level to defeat DCE
func benchmarkfibo1(b *testing.B, n int) {
    var r int
    for i := 0; i < b.N; i++ {
        r = fibo1(n)
    }
    result = r                                   // Force use of r
}
func Benchmark30fibo1(b *testing.B) {
    benchmarkfibo1(b, 30)
}
// Run: go test -bench=. benchmarkMe.go benchmarkMe_test.go
// With allocations: go test -benchmem -bench=.
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Benchmarking Go code / A simple benchmarking example"*

---

### Cross-Compilation

**Principle:** Cross-compile with `GOOS` and `GOARCH` env vars. Go is statically linked by default, so the resulting binary runs anywhere with the matching kernel/arch.

**Code:**
```bash
$ env GOOS=linux GOARCH=arm go build xCompile.go
$ file xCompile
xCompile: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Cross-compilation"*

---

### Example Functions as Executable Documentation

**Principle:** Functions named `Example*` in `_test.go` files are both documentation and tests. The `// Output:` comment makes them assertion-backed.

**Code:**
```go
func ExampleF1() {
    fmt.Println(F1(10))
    fmt.Println(F1(2))
    // Output:
    // 55
    // 1
}
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Creating example functions"*

---

### Interface Design Rule

**Principle:** "If you define an interface and its implementation in the same package, you may be using interfaces incorrectly."

**Do:**
- Define interfaces where they are *consumed* (the handler package), not where the type is implemented.
- Keep interfaces small and composable.

**Code:**
```go
// In the handler package (consumer side):
type Translator interface {
    Translate(word string, language string) string
}
// Concrete impl in the translation package satisfies this implicitly (Go duck typing)
type StaticService struct{}
func (s *StaticService) Translate(word string, language string) string { ... }
```
*Ref: Mastering_Go_-_Mihalis_Tsoukalos.md — "Go Interfaces / Defining an interface"*

---

## Anti-Patterns & Common Mistakes

- **Forgetting `mutex.Unlock()`:** causes `fatal error: all goroutines are asleep - deadlock!` immediately. *Fix:* always `defer m.Unlock()` as the first statement after `Lock`.
- **Race conditions on maps:** Concurrent map writes without synchronization panic with `fatal error: concurrent map writes`. *Fix:* wrap with a mutex or use a monitor goroutine.
- **Missing WaitGroup pair:** `Add` without matching `Done` ⇒ deadlock; `Done` without matching `Add` ⇒ `panic: sync: negative WaitGroup counter`. *Fix:* audit counter in tests; use `defer` for `Done`.
- **Goroutine loop capture bug:** `go func() { fmt.Println(i) }()` over loop var reads the final value. *Fix:* pass `i` as a parameter: `go func(j int) { ... }(i)`.
- **Closing the wrong side:** Sending on a closed channel panics. *Fix:* only the sender closes; use `for v := range ch` on the receiver.
- **Time-based goroutine sync:** `time.Sleep(N)` to wait for goroutines is unreliable. *Fix:* `sync.WaitGroup` or a done channel.
- **Reading `len(buf)` for read sizes:** Always use `n, _ := f.Read(buf)` and `buf[:n]`, never `len(buf)`.
- **Calling `signal.Notify` with no args vs `os.Interrupt`:** Picking too narrow a list causes "if it gets a signal which is not programmed to handle, it will ignore it." *Fix:* prefer `signal.Notify(sigs)` to catch all signals.
- **Bare `_ = ` on errors to silence linters:** `_ = json.Unmarshal(...)` is a code smell — "situations like missing error checks can hide underlying problems." *Fix:* check the error or return it.
- **Wrong path capture in shell:** `go run cat.go cat.go` fails with case-insensitive file name collision. *Fix:* `go build cat.go` first, then run with the binary name as an arg.
- **Optimizing buggy code:** "There is no point in optimizing a bug." *Fix:* debug first.
- **Closing a `nil` channel:** `panic: close of nil channel`. *Fix:* initialise channels with `make` or check before close.
- **Comparing optimization speeds across languages without bench:** "Premature optimization is the root of all evil (or at least most of it) in programming." *Fix:* profile before optimizing.
- **Using `http.Get` when you need control:** "The main problem with webClient.go is that it gives you almost no control over the process." *Fix:* use `http.Client` + `http.NewRequest`.

## Decision Heuristics / Checklists

- **Channels vs mutex:** prefer channels to coordinate; prefer mutex to protect a single in-memory value when many goroutines need low-level access; use a monitor goroutine when state is complex and only one goroutine owns it.
- **`sync.RWMutex` vs `sync.Mutex`:** use `RWMutex` when reads dominate and write latency is acceptable; use plain `Mutex` when writes are common or contention is high.
- **`select` + `time.After` vs `context.WithTimeout`:** use `context` for any operation that crosses an API or service boundary (cancellation propagates); use `select` + `time.After` for short, in-process deadlines.
- **`go test -race`:** run in CI on every PR; cost is acceptable; catch is invaluable.
- **`httptest.NewRecorder`:** use for any `http.Handler` test; never start a real listener in a unit test.
- **Profiling:** start with `go test -benchmem -bench=.`; move to `runtime/pprof` for production-shaped workloads; use `runtime/trace` when you suspect scheduler contention.
- **Channel direction in signatures:** always type channel parameters as `chan<- T` or `<-chan T` — compiler enforces correctness.
- **Goroutine spawn budget:** size pools by `runtime.NumCPU()` for CPU-bound work; size by external dependency limit for IO-bound.
- **TCP server concurrency:** one goroutine per accepted connection; close on disconnect; never share the `net.Conn` across goroutines without external sync.
- **RPC method signature:** `func (t *T) Method(args *ArgType, reply *ReplyType) error` — exported type, exported method, exactly two args, second is a pointer.

## Key Takeaways

1. **Share by communicating, not by communicating by sharing.** Monitor goroutines and channels beat bare mutexes for complex state.
2. **`sync.WaitGroup` is the only acceptable way to wait for goroutines** — `time.Sleep` is a code smell.
3. **Directional channels (`chan<-` / `<-chan`) make misuse a compile error.** Use them at every function boundary.
4. **`context.Context` is mandatory** for any function that may block on IO or run as a goroutine — `defer cancel()` always.
5. **Test handlers with `httptest.NewRecorder`**, never with real sockets.
6. **Profile before optimizing.** `runtime/pprof` for CPU/memory, `runtime/trace` for scheduling, `go test -race` for correctness, `go tool pprof -http=:8080` for visual exploration.
7. **`go test -benchmem -bench=.` exposes both speed and allocations.** Always store the result in a package-level variable to defeat dead-code elimination.
8. **Use `signal.Notify(sigs)` (no args) by default** — handle all signals you can; ignore the rest with a `default` case.
9. **Interfaces belong with the consumer, not the provider.** Small, composable interfaces drive testable design.
10. **Cross-compile with `GOOS`/`GOARCH`** — Go is statically linked by default; one toolchain builds for every target.

## Cross-References
- Related: [[../Shipping_Go.md]]
- Topic index: [[../INDEX.md]]