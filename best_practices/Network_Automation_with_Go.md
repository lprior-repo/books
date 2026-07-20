# Network Automation with Go
**Author:** Nicolas Leiva & Michael Kashin (Packt, 2022)
**Topic tags:** `#cli` `#systems` `#go` `#network` `#devops`
**Language focus:** Go-first (1.17/1.18+)
**Sources:** `markdown_output/_pdf_extracts/Network_Automation_with_Go.md` (no summary exists)

## TL;DR
A practitioner's guide that marries Go's standard library (`net`, `net/http`, `crypto/ssh`, `encoding/*`, `sync`, `io`) with the modern network automation stack (Scrapligo, gNMI/gNOI, OpenConfig/ygot, gRPC, Prometheus, Containerlab). The book argues Go beats Python for production network automation because of static typing, compiled binaries, first-class concurrency, and a standard library strong enough that most network tasks need no third-party framework. Use it when building anything from CLI scrapers and config templating to closed-loop telemetry pipelines and Kubernetes-style operators for network state.

---

## Best Practices by Topic

### 1. Project & File Structure

**Principle:** Every Go file is `package` + `import` + top-level declarations; the language is intentionally tiny (25 keywords) so prefer the standard layout over creativity.

**Do:**
- Name files lowercase, single-word, `.go` suffix
- Use `package main` with a single `func main()` for executables
- Co-locate related declarations in one package; split into files only for readability

**Don't:**
- Invent filename conventions (no snake_case, no PascalCase)
- Mix multiple `main` packages in one folder

**Code:**
```go
// Package clause
package main
// import declaration
import "fmt"
// top level declaration
const s = "Hello, 世界"
func main() {
    fmt.Println(s)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 2 / Go source code files"*

---

### 2. Go Modules & Dependency Hygiene

**Principle:** Use `go mod init <import-path>` from day one; pin versions; prefer the standard library over external deps ("a little copying is better than a little dependency").

**Do:**
- `go mod init github.com/<user>/<project>` to establish the import path
- Use `replace` for local dev (`replace github.com/foo/bar => ../bar`)
- Run `go mod tidy` to prune, `go mod why <pkg>` to investigate why a dep is present
- Tag `v2+` modules with `/v2` suffix in the import path

**Don't:**
- Commit `go.sum` churn without review
- Use legacy `go get` to install binaries (deprecated since Go 1.17; use `go install pkg@version`)

**Code:**
```
module github.com/PacktPublishing/Network-Automation-with-Go/ch02/pong

go 1.17

require github.com/PacktPublishing/Network-Automation-with-Go/ch02/ping v0.0.0-20220223180011-2e4e63479343

replace github.com/PacktPublishing/Network-Automation-with-Go/ch02/ping v1.0.0 => ../ping
```
*Ref: Network_Automation_with_Go.md — "Chapter 2 / Go modules"*

---

### 3. Go Tooling — Build, Run, Cross-Compile

**Principle:** One tool (`go`) handles build, run, test, format, vet, mod, env, install. Set `GOOS`/`GOARCH` for cross-compiles; inject build metadata with `-ldflags`.

**Do:**
- `go build -ldflags='-X main.Version=1.0 -X main.GitCommit=600a82c442'` to tag binaries
- `GOOS=windows GOARCH=amd64 go build` to cross-compile
- `go test -race` always for concurrent code

**Code:**
```sh
ch02/hello$ go build -ldflags='-X main.Version=1.0 -X main.GitCommit=600a82c442' *.go
ch02/hello$ ./main
Version: "1.0"
Git Commit: "600a82c442"
Hello World
```
*Ref: Network_Automation_with_Go.md — "Chapter 2 / Build"*

---

### 4. Comments Become Documentation

**Principle:** The line(s) immediately preceding an exported declaration become its godoc. Comment only *what* / *how* / *why*; never the obvious.

**Do:**
- Start each comment with the declaration name (`// IsPrivate reports...`)
- Use `/* */` blocks only for license headers and package docs

**Don't:**
- Comment trivial types (`// x is an int`)
- Forget to update comments when refactoring

**Code:**
```go
// IsPrivate reports whether ip is a private address, according to
// RFC 1918 (IPv4 addresses) and RFC 4193 (IPv6 addresses).
func (ip IP) IsPrivate() bool {
    if ip4 := ip.To4(); ip4 != nil {
        return ip4[0] == 10 ||
           (ip4[0] == 172 && ip4[1]&0xf0 == 16) ||
           (ip4[0] == 192 && ip4[1] == 168)
    }
    return len(ip) == IPv6len && ip[0]&0xfe == 0xfc
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 2 / Comments"*

---

### 5. Naming & Export Control

**Principle:** Capitalization is the only access modifier. `Ping` is exported; `ping` is not. Acronyms keep their case (`ServeHTTP`, not `ServeHttp`).

**Code:**
```go
// IsMulticast reports whether ip is a multicast address.
func (ip IP) IsMulticast() bool {
    if ip4 := ip.To4(); ip4 != nil {
        return ip4[0]&0xf0 == 0xe0
    }
    return len(ip) == IPv6len && ip[0] == 0xff
}

// allFF is package-private (lowercase first letter).
func allFF(b []byte) bool {
    for _, c := range b {
        if c != 0xff {
            return false
        }
    }
    return true
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 2 / Names"*

---

### 6. Static Typing & Type Inference

**Principle:** Declare types explicitly for clarity, use `:=` only for brevity inside functions. Every type conversion is explicit — Go never coerces.

**Do:**
- Use the smallest type that fits the value range (`uint32` not `int` for an ASN)
- Convert explicitly: `T(v)` (`b := uint32(a)`)
- Let zero values be meaningful (`""`, `0`, `nil`)

**Don't:**
- Reassign a variable to a different type (`n = "Hello"` after `n := 42` won't compile)
- Alias types just to alias — wrap behavior with methods

**Code:**
```go
func main() {
    a := -1
    var b uint32
    b = 4294967295
    var c float32 = 42.1
}

func main() {
    a := 4294967295
    b := uint32(a)
    c := float32(b)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Go's type system & Arithmetic operators"*

---

### 7. Strings — Immutability and Memory

**Principle:** A Go string is a 16-byte struct: 8-byte pointer + 8-byte length. Strings are immutable byte slices (UTF-8). Slicing is cheap (shares storage).

**Code:**
```go
func main() {
    n := "Network Automation"
    fmt.Println(len(n))     // 18
    w := n[3:7]
    fmt.Println(w)          // work
}

func main() {
    s1 := "Net"
    s2 := `work`
    if s1 != s2 {
        fmt.Println(s1 + s2 + " Automation") // Network Automation
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Strings"*

---

### 8. Boolean & Error Types

**Principle:** `if` requires a real `bool`. Errors are values returned by functions; never exceptions. Use `errors.New` for static messages and `fmt.Errorf` with `%w` to wrap.

**Code:**
```go
func main() {
    err1 := errors.New("This is a new error")
    msg := "another error message"
    err2 := fmt.Errorf("This is %s", msg)
}

func main() {
    result, err := myFunction()
    if err != nil {
        fmt.Printf("Received an error: %s", err)
        return err
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Boolean & Error"*

---

### 9. Arrays vs Slices vs Maps

**Principle:** Use fixed arrays only for fixed-size data (IP/MAC bytes, headers). Use slices everywhere else. Use `make` for maps and bounded slices.

**Do:**
- Pre-size slices when you know the length (`make([]string, 0, n)`)
- Pass slices by pointer if you need to `append` and have caller see results
- Use two-value map lookup (`v, ok := m[k]`) to disambiguate zero values

**Don't:**
- Mutate a slice passed by value and expect the caller to see appends
- Assume maps are concurrent-safe — they are not

**Code:**
```go
// Fixed array for an IP header
func main() {
    var ipAddr [4]byte
    var localhost = [4]byte{127, 0, 0, 1}
    fmt.Println(len(localhost))
    fmt.Printf("%b\n", localhost)
    fmt.Println(ipAddr == localhost)
}

// Slice semantics
func main() {
    empty := []string{}
    words := []string{"zero", "one", "two", "three", "four", "five", "six"}
    three := make([]string, 3)
    fmt.Printf("empty: length: %d, capacity: %d, %v\n", len(empty), cap(empty), empty)
    fmt.Printf("words: length: %d, capacity: %d, %v\n", len(words), cap(words), words)
    fmt.Printf("three: length: %d, capacity: %d, %v\n", len(three), cap(three), three)
}

// Map with membership test
func main() {
    dc := make(map[string]string)
    dc["spine"] = "192.168.100.1"
    ip := dc["spine"]
    ip, exists := dc["spine"]
    if exists {
        fmt.Println(ip)
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Container types"*

---

### 10. Structs & Embedding

**Principle:** Group fixed fields with structs. Use embedding (not inheritance) for composition. Use field tags to drive encoders (`json:`, `xml:`, `yaml:`).

**Code:**
```go
type Router struct {
    Hostname  string `json:"hostname" xml:"hostname"`
    IP        string `json:"ip" xml:"ip"`
    ASN       uint16 `json:"asn" xml:"asn"`
}

type Inventory struct {
    Routers []Router `json:"router" xml:"router"`
}

func main() {
    var r1 Router
    r1.Hostname = "router1.example.com"
    r2 := new(Router)
    r2.Hostname = "router2.example.com"
    r3 := Router{
        Hostname: "router3.example.com",
        Platform: "cisco_iosxr",
        Username: "user",
        Password: "secret",
        StrictKey: false,
    }
    inv := Inventory{
        Routers: []Router{r1, *r2, r3},
    }
    fmt.Printf("Inventory: %+v\n", inv)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Structs & Encoding"*

---

### 11. Bit Manipulation for Protocol Headers

**Principle:** Build/parse network headers with shift (`<<`, `>>`) and bitwise operators (`&`, `|`, `^`). Use `uint8` for single-byte fields.

**Code:**
```go
func main() {
    // Header length (measured in 32-bit words) is 5
    var headerWords uint8 = 5
    headerLen := headerWords * 32 / 8
    b := make([]byte, headerLen)
    s := headerWords << 4
    b[13] = b[13] | s
    fmt.Printf("%08b\n", b[13])

    var tcpSyn uint8 = 1
    f := tcpSyn << 1
    b[14] = b[14] | f
    fmt.Printf("%08b\n", b[14])

    tcpSynFlag := (b[14] & 0x02) != 0
    parsedHeaderWords := b[13] >> 4
    fmt.Printf("TCP Flag is set: %t\n", tcpSynFlag)
    fmt.Printf("TCP header words: %d\n", parsedHeaderWords)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Arithmetic operators"*

---

### 12. Control Flow — `for` is the Only Loop

**Principle:** Go has one loop keyword. Use `for {}` (infinite), `for cond {}` (while), `for i:=0; i<n; i++ {}` (C-style), `for k, v := range x {}` (iteration).

**Code:**
```go
func main() {
    for i := 0; i < 5; i++ {
        fmt.Println(i)
    }

    slice := []string{"r1", "r2", "r3"}
    for i, v := range slice {
        fmt.Printf("index %d: value: %s\n", i, v)
    }

    hashMap := map[int]string{1: "r1", 2: "r2", 3: "r3"}
    for i, v := range hashMap {
        fmt.Printf("key %d: value: %s\n", i, v)
    }

    i := 0
    for i < 5 { // while-style
        fmt.Println(i)
        i++
    }

    for { // infinite
        time.Sleep(time.Second)
        break
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / for loops"*

---

### 13. Conditional Expressions & `switch`

**Principle:** Left-align the happy path; drop `else` after a `return`. Prefer `switch` over `if-else if` chains. `switch` cases don't fall through.

**Code:**
```go
func main() {
    resp, err := http.Get("https://www.tkng.io/")
    if err != nil {
        log.Fatalf("Could not connect: %v", err)
    }
    fmt.Printf("Received response: %v", resp.Status)
}

func main() {
    resp, _ := http.Get("http://httpstat.us/304")
    switch {
    case resp.StatusCode >= 500:
        fmt.Println("Server Error")
    case resp.StatusCode >= 400:
        fmt.Println("Client Error")
    case resp.StatusCode >= 300:
        fmt.Println("Redirect")
    case resp.StatusCode >= 200:
        fmt.Println("Success")
    default:
        fmt.Println("Informational")
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Conditional statements"*

---

### 14. Functions — Values, Closures, Variadics

**Principle:** Functions are first-class values. Closures capture their enclosing scope. Variadics (`...T`) collect extra args into a slice.

**Code:**
```go
// Function as argument
func processDevice(getName func(string, string) string, ip string) {
    base := "device"
    name := getName(base, ip)
    fmt.Println(name)
}

// Variadic
func printOctets(octets ...string) {
    fmt.Println(strings.Join(octets, "."))
}
func main() {
    printOctets("127", "1")
    ip := []string{"192", "0", "2", "1"}
    printOctets(ip...)
}

// Closure with state
func suffixGenerator() func() string {
    i := 0
    return func() string {
        i++
        return fmt.Sprintf("%02d", i)
    }
}
func main() {
    generator1 := suffixGenerator()
    fmt.Printf("%s-%s\n", "device", generator1()) // device-01
    fmt.Printf("%s-%s\n", "device", generator1()) // device-02
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Functions, Variadic, Closures"*

---

### 15. Pointers & Mutation Semantics

**Principle:** Go passes everything by value — including pointers (which are themselves values). Use pointers to mutate caller state or to avoid copying large structs. Slices, maps, channels, and functions are already reference-like.

**Code:**
```go
type Device struct{ name string }

// By value — caller unaffected
func mutate(input Device) {
    input.name += "-suffix"
}

// By pointer — caller sees change
func mutate(input *Device) {
    input.name += "-suffix"
}
func main() {
    d := Device{name: "myname"}
    mutate(&d)
    fmt.Println(d.name) // myname-suffix
}

// Map is already pointer-like
func fn(m map[int]int) {
    m[1] = 11
}
func main() {
    m := make(map[int]int)
    fn(m)
    fmt.Println(m[1]) // 11
}

// Slice gotcha — in-place change visible, append NOT visible
func mutateV(input []string) {
    input[0] = "r03"
    input = append(input, "r04")
}
func mutateP(input *[]string) {
    (*input)[0] = "r03"
    *input = append(*input, "r04")
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Function arguments"*

---

### 16. Methods & Pointer Receivers

**Principle:** Choose pointer receivers when the method mutates the receiver or the struct is large. Be consistent across a type's methods.

**Code:**
```go
type Device struct{ name string }

func (d *Device) GenerateName() { // mutates
    d.name = "device-" + d.name
}
func (d Device) GetFullName() string { // read-only
    return d.name
}
func main() {
    d2 := Device{name: "r2"}
    d2.GenerateName()
    fmt.Println(d2.GetFullName()) // device-r2
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Methods"*

---

### 17. Error Handling — Wrap, Don't Discard

**Principle:** Don't just check errors — handle them gracefully. Wrap with `%w` to preserve the chain. Return errors as the last positional value.

**Code:**
```go
func makeCall(url string) (*http.Response, error) {
    resp, err := http.Get("example.com")
    if err != nil {
        return nil, fmt.Errorf("error in makeCall: %w", err)
    }
    return resp, nil
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Error handling"*

---

### 18. `defer` for Resource Cleanup

**Principle:** Pair each `Open`/`Dial`/`Connect` with a `defer` `Close()` on the very next line. Defers run LIFO at function return.

**Code:**
```go
func main() {
    resp, err := http.Get("http://example.com")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    defer fmt.Println("Deferred cleanup")
    fmt.Println("Response status:", resp.Status)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Defer"*

---

### 19. Interfaces — Implicit Contracts

**Principle:** Interfaces are satisfied implicitly ("duck typing with compile-time checks"). Accept interfaces, return structs. Define small interfaces at the point of use.

**Do:**
- Define interfaces in the *consumer* package, not the producer
- Keep them single-method when possible (`io.Reader`, `io.Writer`)

**Code:**
```go
// Both CiscoIOS and CiscoNXOS satisfy NetworkDevice implicitly
type CiscoIOS struct {
    Hostname string
    Platform string
}
func (r CiscoIOS) getUptime() int { /* ... */ return 0 }

type CiscoNXOS struct {
    Hostname string
    Platform string
    ACI      bool
}
func (s CiscoNXOS) getUptime() int { /* ... */ return 0 }

type NetworkDevice interface {
    getUptime() int
}

func LastToReboot(r1, r2 NetworkDevice) bool {
    return r1.getUptime() < r2.getUptime()
}

func main() {
    ios := CiscoIOS{}
    nexus := CiscoNXOS{}
    if LastToReboot(ios, nexus) {
        fmt.Println("IOS-XE was last to reboot")
    }
}

// net.Conn — real-world interface from the standard library
type Conn interface {
    LocalAddr() Addr
    RemoteAddr() Addr
    SetDeadline(t time.Time) error
    SetReadDeadline(t time.Time) error
    SetWriteDeadline(t time.Time) error
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Interfaces & Standard library example"*

---

### 20. `io.Reader` / `io.Writer` — The Streaming ABCs

**Principle:** Almost every encoding/transport library in Go speaks `io.Reader`/`io.Writer`. They let you chain file/network/string/transform sources and sinks without buffering whole payloads.

**Code:**
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
type Writer interface {
    Write(p []byte) (n int, err error)
}

// Copy file → file
func main() {
    src := strings.NewReader("The text")
    dst, err := os.Create("./file.txt")
    if err != nil { panic(err) }
    defer dst.Close()
    io.Copy(dst, src)
}

// Copy URL → stdout
func main() {
    res, err := http.Get("https://www.tkng.io/")
    if err != nil { panic(err) }
    src := res.Body
    defer src.Close()
    dst := os.Stdout
    io.Copy(dst, src)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / io.Reader, io.Writer, io.Copy"*

---

### 21. Composition — Decorate a Reader

**Principle:** Embed one type in another to add behavior while satisfying the same interface. Override only the methods you need to customize.

**Code:**
```go
type myReader struct {
    src io.Reader
}
func (r *myReader) Read(buf []byte) (int, error) {
    tmp := make([]byte, len(buf))
    n, err := r.src.Read(tmp)
    copy(buf[:n], bytes.Title(tmp[:n]))
    return n, err
}
func NewMyReader(r io.Reader) io.Reader {
    return &myReader{src: r}
}

func main() {
    r1 := strings.NewReader("network automation with go")
    r2 := NewMyReader(r1)
    io.Copy(os.Stdout, r2) // Network Automation With Go
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Composition"*

---

### 22. Structured Decoding — JSON / XML / YAML

**Principle:** Use struct tags to map fields. All `encoding/*` packages accept `io.Reader` so the same code works for files, HTTP bodies, strings. Use `map[string]interface{}` only for one-off inspection.

**Code:**
```go
// JSON
type Router struct {
    Hostname string `json:"hostname"`
    IP       string `json:"ip"`
    ASN      uint16 `json:"asn"`
}
type Inventory struct {
    Routers []Router `json:"router"`
}

func main() {
    file, _ := os.Open("input.json")
    defer file.Close()
    d := json.NewDecoder(file)
    var inv Inventory
    d.Decode(&inv)
    fmt.Printf("%+v\n", inv)
}

// XML — only the imports and tags change
type Router struct {
    Hostname string `xml:"hostname"`
    IP       string `xml:"ip"`
    ASN      uint16 `xml:"asn"`
}
d := xml.NewDecoder(file)

// YAML (via gopkg.in/yaml.v2)
type Router struct {
    Hostname string `yaml:"hostname"`
    IP       string `yaml:"ip"`
    ASN      uint16 `yaml:"asn"`
}
d := yaml.NewDecoder(file)
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Decoding"*

---

### 23. Encoding (Marshal) Roundtrip

**Principle:** Same struct can carry tags for multiple formats. `strings.Builder` satisfies `io.Writer` for in-memory encoding.

**Code:**
```go
func main() {
    /* decode JSON into inv */
    var dest strings.Builder
    e := xml.NewEncoder(&dest)
    err = e.Encode(&inv)
    fmt.Printf("%+v\n", dest.String())
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Encoding"*

---

### 24. Goroutines — Cheap Concurrency

**Principle:** A `go` prefix spawns a goroutine. Use `sync.WaitGroup` to wait for fan-out. The race detector (`-race`) is mandatory for non-trivial concurrent code.

**Do:**
- Pass loop variables as parameters to the goroutine to avoid the classic closure capture bug
- Make hot functions "goroutine-aware" by accepting `*sync.WaitGroup` directly

**Don't:**
- Spawn unbounded goroutines for unbounded inputs (use a worker pool)
- Share memory across goroutines without synchronization

**Code:**
```go
// Sequential — slow
func main() {
    for _, r := range inv.Routers {
        getVersion(r)
    }
}

// Naive goroutine — main may exit early
func main() {
    for _, r := range inv.Routers {
        go getVersion(r)
    }
}

// Proper fan-out with WaitGroup
func main() {
    var wg sync.WaitGroup
    for _, v := range inv.Routers {
        wg.Add(1)
        go func(r Router) {
            defer wg.Done()
            getVersion(r)
        }(v)
    }
    wg.Wait()
}

// Goroutine-aware function
func getVersion(r Router, wg *sync.WaitGroup) {
    defer wg.Done()
    /* ... */
}
func main() {
    for _, v := range inv.Routers {
        wg.Add(1)
        go getVersion(v, &wg)
    }
    wg.Wait()
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Goroutines"*

---

### 25. Channels — Communicate by Sharing

**Principle:** "Don't communicate by sharing memory; share memory by communicating." Use buffered channels for fan-in/fan-out; close them only from the sender.

**Code:**
```go
// Single-goroutine ping
func main() {
    ch := make(chan int, 1)
    send := 1
    ch <- send
    receive := <-ch
    fmt.Println(receive)
}

// Fan-in: printer goroutine consumes from workers
func printer(in chan data) {
    for out := range in {
        fmt.Printf("Hostname: %s\nHW: %s\nSW Version: %s\nUptime: %s\n\n",
            out.host, out.hw, out.version, out.uptime)
    }
}

func main() {
    ch := make(chan data)
    go printer(ch)
    var wg sync.WaitGroup
    for _, v := range inv.Routers {
        wg.Add(1)
        go getVersion(v, ch, &wg)
    }
    wg.Wait()
    close(ch)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Channels"*

---

### 26. `select`, Timers & Tickers

**Principle:** `select` is the channel multiplexer. Use `time.After` for deadlines, `time.NewTicker` for periodic work, and a `done` channel for cancellation.

**Code:**
```go
// Timeout via select
for {
    select {
    case out := <-ch:
        fmt.Printf("Hostname: %s\n", out.host)
    case <-time.After(5 * time.Second):
        close(ch)
        fmt.Println("Timeout: 5 seconds")
        return
    }
}

// Ticker with done channel
func main() {
    ticker := time.NewTicker(500 * time.Millisecond)
    done := make(chan bool)
    go repeat(done, ticker.C)
    time.Sleep(2100 * time.Millisecond)
    ticker.Stop()
    done <- true
}

func repeat(d chan bool, c <-chan time.Time) {
    for {
        select {
        case <-d:
            return
        case t := <-c:
            fmt.Println("Run at", t.Local())
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Channels and Timers"*

---

### 27. `sync.Mutex` / `sync.RWMutex` — Shared State

**Principle:** Channels are the default, but mutexes are right for protecting shared counters and maps. Use `RWMutex` when reads dominate.

**Code:**
```go
var m sync.RWMutex = sync.RWMutex{}

func getVersion(r Router, out chan data, wg *sync.WaitGroup, isAlive map[string]bool) {
    defer wg.Done()
    rs, err := d.SendCommand("show version")
    if err != nil {
        m.Lock()
        isAlive[r.Hostname] = false
        m.Unlock()
        return
    }
    m.Lock()
    isAlive[r.Hostname] = true
    m.Unlock()
}

// Read path uses RLock
func main() {
    m.RLock()
    for name, v := range isAlive {
        fmt.Printf("Router %s is alive: %t\n", name, v)
    }
    m.RUnlock()
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Shared data access"*

---

### 28. Race Detector — Always On for Tests

**Principle:** Run `go test -race` (or `go run -race`) to catch data races in concurrent code. The detector instruments every memory access.

**Code:**
```sh
$ go run -race main.go
==================
WARNING: DATA RACE
Write at 0x00c00011c6f0 by goroutine 9:
  runtime.mapassign_faststr()
  main.getVersion()
      ~/Network-Automation-with-Go/ch03/race/main.go:35 +0xeb
Found 1 data race(s)
exit status 66
```
*Ref: Network_Automation_with_Go.md — "Chapter 3 / Shared data access (race example)"*

---

### 29. Link Layer — Netlink via `mdlayher/netlink`

**Principle:** On Linux, Netlink is the kernel↔user-space API for interfaces, routes, addresses, neighbors. Use `mdlayher/netlink` ecosystem (idiomatic `Dial`/`Close` pattern, like `net/http`). Operations that change state need `CAP_NET_ADMIN`.

**Code:**
```go
func main() {
    conn, err := rtnl.Dial(nil)
    if err != nil { /* ... */ }
    defer conn.Close()

    links, _ := conn.Links()
    var loopback *net.Interface
    for _, l := range links {
        if l.Name == "lo" {
            loopback = l
            log.Printf("Name: %s, Flags:%s\n", l.Name, l.Flags)
        }
    }

    conn.LinkDown(loopback)
    loopback, _ = conn.LinkByIndex(loopback.Index)
    log.Printf("Name: %s, Flags:%s\n", loopback.Name, loopback.Flags)

    conn.LinkUp(loopback)
    loopback, _ = conn.LinkByIndex(loopback.Index)
    log.Printf("Name: %s, Flags:%s\n", loopback.Name, loopback.Flags)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / Network interfaces"*

---

### 30. Ethernet & ARP — Building a VIP / GARP Sender

**Principle:** Layer frames by hand with `mdlayher/ethernet` + `mdlayher/arp` + `mdlayher/packet`. Marshal each layer to binary, wrap, and write to a raw socket.

**Code:**
```go
VIP1 = "198.51.100.1/32"

type vip struct {
    IP       string
    netlink  *rtnl.Conn
    intf     *net.Interface
    l2Sock   *raw.Conn
}

func (c *vip) addVIP() error {
    return c.netlink.AddrAdd(c.intf, rtnl.MustParseAddr(c.IP))
}

func (c *vip) sendGARP() error {
    arpPayload, err := arp.NewPacket(
        arp.OperationReply, c.intf.HardwareAddr, ip,
        c.intf.HardwareAddr, ip,
    )
    arpBinary, _ := arpPayload.MarshalBinary()

    ethFrame := &ethernet.Frame{
        Destination: ethernet.Broadcast,
        Source:      c.intf.HardwareAddr,
        EtherType:   ethernet.EtherTypeARP,
        Payload:     arpBinary,
    }
    return c.emitFrame(ethFrame)
}

func (c *vip) emitFrame(frame *ethernet.Frame) error {
    b, err := frame.MarshalBinary()
    addr := &packet.Addr{HardwareAddr: ethernet.Broadcast}
    if _, err := c.l2Sock.WriteTo(b, addr); err != nil {
        return fmt.Errorf("emitFrame failed: %s", err)
    }
    log.Println("GARP sent")
    return nil
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / Ethernet"*

---

### 31. The `net` Package — Parsing IPs and CIDRs

**Principle:** `net.IP` is a `[]byte`. `net.ParseIP` / `net.ParseCIDR` / `net.CIDRMask` are the workhorses. Note `net.IP` is mutable and not comparable — use `netip.Addr` for that.

**Code:**
```go
func main() {
    ipv4 := net.ParseIP("192.0.2.1")
    fmt.Println(ipv4.IsPrivate()) // false

    // CIDRMask
    fmt.Printf("%b\n", net.CIDRMask(31, 32)) // [11111111 11111111 11111111 11111110]
    fmt.Printf("%s\n", net.CIDRMask(64, 128))

    ipv4Addr, ipv4Net, _ := net.ParseCIDR("192.0.2.1/24")
    fmt.Println(ipv4Addr)    // 192.0.2.1
    fmt.Println(ipv4Net)     // 192.0.2.0/24
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / The net package"*

---

### 32. The New `net/netip` Package (Go 1.18+)

**Principle:** `netip.Addr` is a value type (no slice header) — immutable, comparable, and usable as a map key. Prefer it for new code.

**Code:**
```go
func main() {
    IPv4, _ := netip.ParseAddr("224.0.0.1")
    if IPv4.IsMulticast() {
        fmt.Println("IPv4 address is Multicast")
    }

    IPv6, _ := netip.ParseAddr("FE80:F00D::1")
    if IPv6.IsLinkLocalUnicast() {
        fmt.Println("IPv6 address is Link Local Unicast")
    }

    // Prefix / Contains
    pf := netip.MustParsePrefix("192.0.2.0/24")
    ip1 := netip.MustParseAddr("192.0.2.18")
    if pf.Contains(ip1) {
        fmt.Println("192.0.2.18 is in 192.0.2.0/24")
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / The New netip package"*

---

### 33. Prefix Tries & GeoIP

**Principle:** Use `cidranger` for longest-prefix-match lookups, `oschwald/geoip2` for GeoIP, `iplib` for arithmetic on addresses (increment, compare, enumerate).

**Code:**
```go
// Longest-prefix match
ranger := cidranger.NewPCTrieRanger()
for _, prefix := range IPs {
    ipv4Addr, ipv4Net, _ := net.ParseCIDR(prefix)
    ranger.Insert(cidranger.NewBasicRangerEntry(*ipv4Net))
}
ok, _ := ranger.Contains(net.ParseIP("127.0.0.1"))
nets, _ := ranger.ContainingNetworks(net.ParseIP("192.0.2.18"))

// GeoIP
db, _ := geoip2.Open("GeoIP2-City-Test.mmdb")
defer db.Close()
record, _ := db.City(net.ParseIP("81.2.69.143"))
fmt.Printf("City: %v, Country: %v\n",
    record.City.Names["en"], record.Country.Names["en"])

// iplib arithmetic
IP := net.ParseIP("192.0.2.1")
nextIP := iplib.NextIP(IP)
incrIP := iplib.IncrementIPBy(nextIP, 19)
fmt.Println(iplib.DeltaIP(IP, incrIP)) // 20
fmt.Println(iplib.CompareIPs(IP, incrIP)) // -1
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / Route lookups, GeoIP, Extra IP functions"*

---

### 34. UDP Server & Client (with binary encoding)

**Principle:** `net.ListenUDP` / `net.DialUDP` give you a `UDPConn` that implements `io.Reader`/`io.Writer`. Use `encoding/binary` for fixed-size wire formats.

**Do:**
- Always call `SetReadDeadline` so blocking `ReadFromUDP` can be interrupted
- Mirror packets back with `WriteToUDP` and the captured remote address

**Code:**
```go
// Server
func main() {
    listenSoc := &net.UDPAddr{IP: net.ParseIP("0.0.0.0"), Port: 32767}
    udpConn, err := net.ListenUDP("udp", listenSoc)
    defer udpConn.Close()

    for {
        bytes := make([]byte, 425984)
        udpConn.SetReadDeadline(time.Now().Add(5 * time.Second))
        n, raddr, err := udpConn.ReadFromUDP(bytes)
        if err != nil { continue }
        udpConn.WriteToUDP(bytes[:n], raddr)
    }
}

// Client — embed binary probe
type probe struct {
    SeqNum uint8
    SendTS int64
}

func main() {
    rAddr := &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 32767}
    udpConn, _ := net.DialUDP("udp", nil, rAddr)
    defer udpConn.Close()

    go receive(*udpConn)
    var seq uint8
    for {
        p := &probe{SeqNum: seq, SendTS: time.Now().UnixMilli()}
        binary.Write(udpConn, binary.BigEndian, p)
        seq++
    }
}

func receive(udpConn net.UDPConn) {
    var nextSeq uint8
    var lost int
    for {
        p := &probe{}
        binary.Read(&udpConn, binary.BigEndian, p)
        if p.SeqNum > nextSeq {
            lost += int(p.SeqNum - nextSeq)
            nextSeq = p.SeqNum
        }
        latency := time.Now().UnixMilli() - p.SendTS
        log.Printf("E2E latency: %d ms, lost: %d", latency, lost)
        nextSeq++
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / UDP ping application"*

---

### 35. HTTP Client — Build URLs with `net/url`

**Principle:** Use `url.Parse` + `url.Values` instead of string concatenation. `http.DefaultClient` is safe for concurrent use; only customize `Transport` when needed.

**Code:**
```go
func main() {
    server := "localhost:8080"
    lookup := "domain"
    argument := "tkng.io"
    addr, _ := url.Parse("http://" + server + "/lookup")
    params := url.Values{}
    params.Add(lookup, argument)
    addr.RawQuery = params.Encode()

    res, err := http.DefaultClient.Get(addr.String())
    if err != nil { log.Fatal(err) }
    defer res.Body.Close()
    io.Copy(os.Stdout, res.Body)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / HTTP client"*

---

### 36. HTTP Server — `DefaultServeMux` & Handler Functions

**Principle:** `http.HandleFunc(pattern, fn)` registers a handler on the default mux. `ListenAndServe` blocks; spawn per-request goroutines automatically. Each handler gets `http.ResponseWriter` (an `io.Writer`) and `*http.Request`.

**Code:**
```go
func lookup(w http.ResponseWriter, req *http.Request) {
    log.Printf("Incoming %+v", req.URL.Query())
    var response string
    for k, v := range req.URL.Query() {
        switch k {
        case "ip":
            response = getWhois(v)
        case "mac":
            response = getMAC(v)
        case "domain":
            response = getWhois(v)
        default:
            response = fmt.Sprintf("query %q not recognized", k)
        }
    }
    fmt.Fprintf(w, response)
}

func main() {
    http.HandleFunc("/lookup", lookup)
    http.HandleFunc("/check", check)
    log.Println("Starting web server at 0.0.0.0:8080")
    srv := http.Server{Addr: "0.0.0.0:8080"}
    log.Fatal(srv.ListenAndServe())
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 4 / HTTP server"*

---

### 37. Network Automation — Closed-Loop Architecture

**Principle:** A closed-loop system = *intent* + *network intelligence* + *actuation*. Compute a hash of the desired state, poll the derived state, and reapply only when they differ.

**Do:**
- Hash the intent struct (`hashstructure.Hash`) for cheap equality checks
- Backup current config before each remediation cycle
- Sleep between iterations to avoid hammering the device

**Don't:**
- Treat every operational delta as actionable — some values (MAC tables) are inherently noisy

**Code:**
```go
intent := Service{
    Name:     "grpc",
    Port:     "57777",
    AF:       "ipv4",
    Insecure: false,
    CLI:      "show grpc status",
}
intentHash, _ := hashstructure.Hash(intent, hashstructure.FormatV2, nil)

// periodic enforcement loop
for {
    oper, _ := iosxr.getOper(intent)
    operHash, _ := hashstructure.Hash(oper, hashstructure.FormatV2, nil)
    if operHash == intentHash {
        continue
    }
    iosxr.sendConfig(genConfig(intent))
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 5 / Closed-loop automation"*

---

### 38. SSH Configuration via `golang.org/x/crypto/ssh`

**Principle:** For interactive CLI devices, dial SSH, request a PTY, then write template-rendered commands to the session's `stdin` pipe. Read from `stdout` until the prompt returns.

**Do:**
- `defer session.Close()` immediately after `NewSession`
- Set `HostKeyCallback: ssh.InsecureIgnoreHostKey()` only for lab/dev
- Build configs with `text/template` (range over input model)

**Code:**
```go
srlTemplate = `
enter candidate
{{- range $uplink := .Uplinks }}
set / interface {{ $uplink.Name }} subinterface 0 ipv4 address {{ $uplink.Prefix }}
set / network-instance default interface {{ $uplink.Name }}.0
{{- end }}
...
`

func devConfig(in Model) (b bytes.Buffer, err error) {
    t, err := template.New("config").Parse(srlTemplate)
    err = t.Execute(&b, in)
    return b, nil
}

func main() {
    settings := &ssh.ClientConfig{
        User: *username,
        Auth: []ssh.AuthMethod{ssh.Password(*password)},
        HostKeyCallback: ssh.InsecureIgnoreHostKey(),
    }
    conn, err := ssh.Dial("tcp",
        fmt.Sprintf("%s:%d", *hostname, sshPort), settings)
    defer conn.Close()

    session, _ := conn.NewSession()
    defer session.Close()
    modes := ssh.TerminalModes{
        ssh.ECHO:          1,
        ssh.TTY_OP_ISPEED: 115200,
        ssh.TTY_OP_OSPEED: 115200,
    }
    session.RequestPty("xterm", 40, 80, modes)
    stdin, _ := session.StdinPipe()
    stdout, _ := session.StdoutPipe()
    session.Shell()
    cfg.WriteTo(stdin)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / Using Go's SSH package"*

---

### 39. Scrapligo — Higher-Level SSH for Network OSes

**Principle:** Scrapligo abstracts platform-specific prompt handling, privilege escalation, and config load/commit. Always use `cfg.NewCfgDriver` over raw SSH when the platform is supported.

**Code:**
```go
func main() {
    conn, _ := platform.NewPlatform(
        *nos, *hostname,
        options.WithAuthNoStrictKey(),
        options.WithAuthUsername(*username),
        options.WithAuthPassword(*password),
    )
    driver, _ := conn.GetNetworkDriver()
    driver.Open()
    defer driver.Close()

    conf, _ := cfg.NewCfg(driver, *nos)
    conf.Prepare()                                  // strip "!"/"end"
    response, _ = conf.LoadConfig(config.String(), false)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / Automating routine SSH tasks"*

---

### 40. REST API Calls to Network Devices

**Principle:** Use Go struct tags to round-trip between YAML input and JSON output. `PATCH` with a candidate revision ID is the standard pattern for declarative NOSes (NVUE/Cumulus).

**Code:**
```go
type cvx struct {
    url    string
    token  string
    httpC  http.Client
}

func main() {
    device := cvx{
        url:    fmt.Sprintf("https://%s:%d", *hostname, defaultNVUEPort),
        token:  base64.StdEncoding.EncodeToString([]byte(
            fmt.Sprintf("%s:%s", *username, *password))),
        httpC: http.Client{
            Transport: &http.Transport{
                TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
            },
        },
    }

    revisionID, _ := createRevision(device)
    addr, _ := url.Parse(device.url + "/nvue_v1/")
    params := url.Values{}
    params.Add("rev", revisionID)
    addr.RawQuery = params.Encode()

    req, _ := http.NewRequest("PATCH", addr.String(), &cfg)
    req.Header.Add("Content-Type", "application/json")
    req.Header.Add("Authorization", "Basic "+device.token)

    res, _ := device.httpC.Do(req)
    defer res.Body.Close()
    applyRevision(device, revisionID)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / HTTP"*

---

### 41. State Validation with Interfaces

**Principle:** Define a `Router` interface with `GetRoutes(*sync.WaitGroup)`. Each vendor type (`SRL`, `CVX`, `CEOS`) implements it differently (regex / TextFSM / REST). Main loops over `[]Router` and fans out concurrently.

**Code:**
```go
type Router interface {
    GetRoutes(wg *sync.WaitGroup)
}

func main() {
    cvx  := CVX{Hostname: "clab-netgo-cvx", /*...*/}
    srl  := SRL{Hostname: "clab-netgo-srl", /*...*/}
    ceos := CEOS{Hostname: "clab-netgo-ceos", /*...*/}

    devices := []Router{cvx, srl, ceos}
    var wg sync.WaitGroup
    for _, router := range devices {
        wg.Add(1)
        go router.GetRoutes(&wg)
    }
    wg.Wait()
}

func checkRoutes(device string, in []string, wg *sync.WaitGroup) {
    defer wg.Done()
    expectedRoutes := map[string]bool{
        "198.51.100.0/32": false,
        "198.51.100.1/32": false,
        "198.51.100.2/32": false,
    }
    for _, route := range in {
        if _, ok := expectedRoutes[route]; ok {
            log.Print("Route ", route, " found on ", device)
            expectedRoutes[route] = true
        }
    }
    for route, found := range expectedRoutes {
        if !found {
            log.Print("! Route ", route, " NOT found on ", device)
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / State validation"*

---

### 42. Parsing CLI Output — Regex vs TextFSM

**Principle:** Use `regexp` for one-off extraction; use TextFSM templates (via Scrapligo's `TextFsmParse`) for tabular output. Regex uses RE2 — no backreferences.

**Code:**
```go
// Regex approach
func (r SRL) GetRoutes(wg *sync.WaitGroup) {
    lookupCmd := "show network-instance default route-table ipv4-unicast summary"
    conn, _ := platform.NewPlatform("nokia_srl", r.Hostname, /*...*/)
    driver, _ := conn.GetNetworkDriver()
    driver.Open()
    defer driver.Close()
    resp, _ := driver.SendCommand(lookupCmd)

    ipv4Prefix := regexp.MustCompile(`(\d{1,3}\.){3}\d{1,3}\/\d{1,2}`)
    out := []string{}
    for _, match := range ipv4Prefix.FindAll(resp.RawResult, -1) {
        out = append(out, string(match))
    }
    go checkRoutes(r.Hostname, out, wg)
}

// TextFSM approach
func (r CEOS) GetRoutes(wg *sync.WaitGroup) {
    template := "https://raw.githubusercontent.com/networktocode/ntc-templates/master/ntc_templates/templates/arista_eos_show_ip_route.textfsm"
    conn, _ := core.NewEOSDriver(r.Hostname,
        base.WithAuthStrictKey(false),
        base.WithAuthUsername(r.Username),
        base.WithAuthPassword(r.Password),
    )
    conn.Open()
    defer conn.Close()
    resp, _ := conn.SendCommand("sh ip route")
    parsed, _ := resp.TextFsmParse(template)
    out := []string{}
    for _, match := range parsed {
        out = append(out, fmt.Sprintf("%s/%s", match["NETWORK"], match["MASK"]))
    }
    go checkRoutes(r.Hostname, out, wg)
}

// REST approach (go-resty)
func (r CVX) GetRoutes(wg *sync.WaitGroup) {
    client := resty.NewWithClient(&http.Client{
        Transport: &http.Transport{
            TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
        },
    })
    client.SetBaseURL("https://" + r.Hostname + ":8765")
    client.SetBasicAuth(r.Username, r.Password)
    var routes map[string]interface{}
    client.R().
        SetResult(&routes).
        SetQueryParams(map[string]string{"rev": "operational"}).
        Get("/nvue_v1/vrf/default/router/rib/ipv4/route")
    out := []string{}
    for route := range routes {
        out = append(out, route)
    }
    go checkRoutes(r.Hostname, out, wg)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / Checking routing information"*

---

### 43. Building an Ansible Module in Go

**Principle:** A binary Ansible module receives a JSON file path as `os.Args[1]` and must print a JSON response to stdout. Wrap with a bash shim to normalize args for `go run`.

**Code:**
```go
// ModuleArgs are the module inputs
type ModuleArgs struct {
    Host     string
    User     string
    Password string
    Input    string
}

// Response is the values returned from the module
type Response struct {
    Msg     string `json:"msg"`
    Busy    bool   `json:"busy"`
    Changed bool   `json:"changed"`
    Failed  bool   `json:"failed"`
}

func main() {
    if len(os.Args) != 2 {
        // generate error
    }
    argsFile := os.Args[1]
    text, err := os.ReadFile(argsFile)
    var moduleArgs ModuleArgs
    json.Unmarshal(text, &moduleArgs)

    // base64 → YAML → Model
    src, _ := base64.StdEncoding.DecodeString(moduleArgs.Input)
    reader := bytes.NewReader(src)
    d := yaml.NewDecoder(reader)
    var input Model
    d.Decode(&input)

    // ... configure device ...

    var r Response
    r.Msg = "Device Configured Successfully"
    r.Changed = true
    r.Failed = false
    response, _ := json.Marshal(r)
    fmt.Println(string(response))
    os.Exit(0)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 7 / Developing an Ansible module"*

---

### 44. Terraform Provider — Schema & CRUD

**Principle:** Start from `terraform-provider-scaffolding`. Define provider + resource schemas that mirror the upstream API. Implement `CreateContext`/`ReadContext`/`UpdateContext`/`DeleteContext`; always call `Read` at the end of `Create` to sync state.

**Code:**
```go
func Provider(version string) func() *schema.Provider {
    return func() *schema.Provider {
        p := &schema.Provider{
            Schema: map[string]*schema.Schema{
                "url": {
                    Type:         schema.TypeString,
                    Required:     true,
                    DefaultFunc:  schema.EnvDefaultFunc("NAUTOBOT_URL", nil),
                    ValidateFunc: validation.IsURLWithHTTPorHTTPS,
                    Description:  "Nautobot API URL",
                },
                "token": {
                    Type:        schema.TypeString,
                    Required:    true,
                    Sensitive:   true,
                    DefaultFunc: schema.EnvDefaultFunc("NAUTOBOT_TOKEN", nil),
                    Description: "Admin API token",
                },
            },
            DataSourcesMap: map[string]*schema.Resource{
                "nautobot_manufacturers": dataSourceManufacturers(),
            },
            ResourcesMap: map[string]*schema.Resource{
                "nautobot_manufacturer": resourceManufacturer(),
            },
        }
        p.ConfigureContextFunc = configure(version, p)
        return p
    }
}

func resourceManufacturer() *schema.Resource {
    return &schema.Resource{
        CreateContext: resourceManufacturerCreate,
        ReadContext:   resourceManufacturerRead,
        UpdateContext: resourceManufacturerUpdate,
        DeleteContext: resourceManufacturerDelete,
        Schema: map[string]*schema.Schema{
            "description": {
                Type:     schema.TypeString,
                Optional: true,
            },
            "name": {
                Type:     schema.TypeString,
                Required: true,
            },
            // ...
        },
    }
}

func resourceManufacturerCreate(ctx context.Context, d *schema.ResourceData,
    meta interface{}) diag.Diagnostics {
    c := meta.(*apiClient).Client
    var m nb.Manufacturer
    name, ok := d.GetOk("name")
    if ok {
        m.Name = name.(string)
    }
    rsp, err := c.DcimManufacturersCreateWithResponse(ctx,
        nb.DcimManufacturersCreateJSONRequestBody(m))
    // process error & response
    d.SetId(id.String())
    return resourceManufacturerRead(ctx, d, meta)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 7 / Developing a Terraform provider"*

---

### 45. OpenAPI / CUE — Validate Before You Send

**Principle:** Use CUE to declare a schema with constraints (`asn: <=65535 & >=64512`), compile inputs against it, and only send valid config to the device.

**Code:**
```go
package input

import (
    "net"
)

asn:      <=65535 & >=64512
loopback: ip: net.IPv4 & string
uplinks: [...{
    name:    string
    prefix:  net.IPv4 & string
}]
peers: [...{
    ip:  net.IPv4 & string
    asn: <=65535 & >=64512
}]
LoopbackIP: "\(loopback.ip)/32"
VRFs: [{name: "default"}]

// Compile + validate inside Go:
func main() {
    bis := load.Instances([]string{"."}, &load.Config{Package: "cvx"})
    ctx := cuecontext.New()
    i := ctx.BuildInstance(bis[0])
    if err := i.Validate(cue.Final(), cue.Concrete(true)); err != nil {
        log.Fatal(err)
    }
    data, _ := e.MarshalJSON()
    sendBytes(data)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / OpenAPI & CUE"*

---

### 46. YANG → Go Bindings with `openconfig/ygot`

**Principle:** Never hand-build YANG JSON. Use `ygot` to generate Go structs from `.yang` models, then `ConstructIETFJSON` / `EmitJSON` for RFC7951 output. `//go:generate` makes the build reproducible.

**Code:**
```go
//go:generate go run github.com/openconfig/ygot/generator -path=yang -generate_fakeroot -fakeroot_name=device -output_file=pkg/srl/srl.go -package_name=srl yang/...

import (
    api "json-rpc/pkg/srl"
)

func (m Model) buildNetworkInstance(dev *api.Device) error {
    ni, _ := dev.NewNetworkInstance(defaultNetInst)

    ni.Protocols = &api.SrlNokiaNetworkInstance_NetworkInstance_Protocols{
        Bgp: &api.SrlNokiaNetworkInstance_NetworkInstance_Protocols_Bgp{
            AutonomousSystem: ygot.Uint32(uint32(m.ASN)),
            RouterId:         ygot.String(m.Loopback.IP),
            Ipv4Unicast: &api.SrlNokiaNetworkInstance_NetworkInstance_Protocols_Bgp_Ipv4Unicast{
                AdminState: api.SrlNokiaBgp_AdminState_enable,
            },
        },
    }

    ni.Protocols.Bgp.NewGroup(defaultBGPGroup)
    for _, peer := range m.Peers {
        n, _ := ni.Protocols.Bgp.NewNeighbor(peer.IP)
        n.PeerAs = ygot.Uint32(uint32(peer.ASN))
        n.PeerGroup = ygot.String(defaultBGPGroup)
    }
    return ni.Validate()
}

// Serialize to RFC7951 JSON for transport
v, _ := ygot.ConstructIETFJSON(device, nil)
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / JSON-RPC, Code generation"*

---

### 47. JSON-RPC over HTTP

**Principle:** Wrap the ygot-produced YANG JSON in a JSON-RPC envelope and POST it. One `set` RPC with `Action: update, Path: /` replaces the entire tree atomically.

**Code:**
```go
type RpcRequest struct {
    Version string    `json:"jsonrpc"`
    ID      int       `json:"id"`
    Method  string    `json:"method"`
    Params  Params    `json:"params"`
}

value, _ := json.Marshal(RpcRequest{
    Version: "2.0",
    ID:      0,
    Method:  "set",
    Params: Params{
        Commands: []*Command{
            {Action: "update", Path: "/", Value: v},
        },
    },
})
req, _ := http.NewRequest("POST", hostname, bytes.NewBuffer(value))
resp, _ := client.Do(req)
defer resp.Body.Close()
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / JSON-RPC / Device configuration"*

---

### 48. RESTCONF — PATCH with Auth & TLS

**Principle:** Build a `restconfRequest` (path + payload) per YANG subtree. Each request targets a specific URI; multiple PATCHes form a transaction.

**Code:**
```go
type restconfRequest struct {
    path    string
    payload []byte
}

func restconfPost(cmd *restconfRequest) error {
    baseURL, _ := url.Parse(fmt.Sprintf("https://%s:%d%s",
        ceosHostname, defaultRestconfPort, restconfPath))
    baseURL.Path = path.Join(restconfPath, cmd.path)
    req, _ := http.NewRequest("POST", baseURL.String(),
        bytes.NewBuffer(cmd.payload))
    req.Header.Add("Content-Type", "application/json")
    req.Header.Add("Authorization", "Basic "+base64.StdEncoding.EncodeToString(
        []byte(fmt.Sprintf("%s:%s", ceosUsername, ceosPassword))))
    client := &http.Client{Transport: &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }}
    resp, err := client.Do(req)
    defer resp.Body.Close()
    return err
}

// Build YANG payload via ygot
func (m *Model) enableRedistribution() (*restconfRequest, error) {
    netInst := &api.NetworkInstance{Name: ygot.String(defaultNetInst)}
    netInst.NewTableConnection(
        api.OpenconfigPolicyTypes_INSTALL_PROTOCOL_TYPE_DIRECTLY_CONNECTED,
        api.OpenconfigPolicyTypes_INSTALL_PROTOCOL_TYPE_BGP,
        api.OpenconfigTypes_ADDRESS_FAMILY_IPV4,
    )
    value, _ := ygot.Marshal7951(netInst)
    return &restconfRequest{
        path:    fmt.Sprintf("/network-instances/network-instance=%s", defaultNetInst),
        payload: value,
    }, nil
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / RESTCONF"*

---

### 49. Protobuf — Schema, Codegen, Wire Format

**Principle:** Define messages in a `.proto` file; `protoc --go_out=.` generates structs. Wire format is field-number + wire-type tagged TLVs — denser and faster than JSON.

**Code:**
```proto
syntax = "proto3";
message Router {
   repeated Uplink uplinks = 1;
   repeated Peer peers = 2;
   int32 asn = 3;
   Addr loopback = 4;
}
message Uplink { string name = 1; string prefix = 2; }
message Peer   { string ip = 1; int32 asn = 2; }
message Addr   { string ip = 1; }
```
```sh
protobuf$ protoc --go_out=. model.proto
# Produces pb/model.pb.go with auto-generated Router struct
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / Protobuf"*

---

### 50. gRPC Service Definitions

**Principle:** gRPC services are typed collections of RPCs. Unary, server-streaming, client-streaming, and bidirectional all supported. gNMI unifies vendor implementations.

**Code:**
```proto
// Cisco IOS XR ems_grpc.proto (excerpt)
service gRPCConfigOper {
  rpc GetConfig(ConfigGetArgs) returns(stream ConfigGetReply) {};
  rpc MergeConfig(ConfigArgs) returns(ConfigReply) {};
  rpc DeleteConfig(ConfigArgs) returns(ConfigReply) {};
  rpc ReplaceConfig(ConfigArgs) returns(ConfigReply) {};
  rpc CreateSubs(CreateSubsArgs) returns(stream CreateSubsReply) {};
}

// gNMI (vendor-neutral)
service gNMI {
  rpc Capabilities(CapabilityRequest) returns (CapabilityResponse);
  rpc Get(GetRequest) returns (GetResponse);
  rpc Set(SetRequest) returns (SetResponse);
  rpc Subscribe(stream SubscribeRequest) returns (stream SubscribeResponse);
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / Defining gRPC services"*

---

### 51. gRPC Config Replace — Wrap Stub in Helper

**Principle:** The auto-generated client (`NewGRPCConfigOperClient`) is verbose. Wrap with a method receiver that hides connection plumbing.

**Code:**
```go
type IOSXR struct {
    Hostname string
    Authentication
}
type xrgrpc struct {
    IOSXR
    conn *grpc.ClientConn
    ctx  context.Context
}

func (x *xrgrpc) ReplaceConfig(json string) error {
    id := rand.Int63()
    g := xr.NewGRPCConfigOperClient(x.conn)
    a := xr.ConfigArgs{ReqId: id, Yangjson: json}
    r, err := g.ReplaceConfig(x.ctx, &a)
    return err
}

// ygot → JSON → gRPC
device := &oc.Device{}
input.buildNetworkInstance(device)
payload, _ := ygot.EmitJSON(device, &ygot.EmitJSONConfig{
    Format: ygot.RFC7951,
    Indent: " ",
    RFC7951Config: &ygot.RFC7951JSONConfig{AppendModuleName: true},
})
iosxr.Connect()
defer router.conn.Close()
iosxr.ReplaceConfig(payload)
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / Configuring network devices with gRPC"*

---

### 52. gRPC Streaming Telemetry — `Recv` in a Goroutine

**Principle:** Subscribe with `CreateSubs`, then loop on `st.Recv()` in a goroutine, forwarding decoded bytes over a channel to the main goroutine.

**Code:**
```go
func (x *xrgrpc) GetSubscription(sub, enc string) (chan []byte, chan error, error) {
    c := xr.NewGRPCConfigOperClient(x.conn)
    b := make(chan []byte)
    a := xr.CreateSubsArgs{ReqId: id, Encode: encoding, Subidstr: sub}
    st, err := c.CreateSubs(x.ctx, &a)

    go func() {
        for {
            r, err := st.Recv()
            if err != nil { /* ... */ }
            b <- r.GetData()
        }
    }()
    return b, e, err
}

// Consumer decodes telemetry with the proto-generated Telemetry type
for msg := range ch {
    message := new(telemetry.Telemetry)
    proto.Unmarshal(msg, message)
    t := time.UnixMilli(int64(message.GetMsgTimestamp()))
    fmt.Printf("Time: %v\nPath: %v\n\n", t.Format(time.ANSIC),
        message.GetEncodingPath())

    // Decode each row into a typed BgpNbrBag
    for _, row := range message.GetDataGpb().GetRow() {
        content := row.GetContent()
        nbr := new(bgp.BgpNbrBag)
        proto.Unmarshal(content, nbr)
        state := nbr.GetConnectionState()
        addr := nbr.GetConnectionRemoteAddress().Ipv4Address
        fmt.Println(" Neighbor: ", addr, " state: ", state)
    }
}

// Self-describing (gpbkv) path — fallback when proto is unknown
for msg := range ch {
    message := new(telemetry.Telemetry)
    proto.Unmarshal(msg, message)
    b, _ := json.Marshal(message.GetDataGpbkv())
    j := string(b)
    data := gjson.Get(j,
        "0.fields.0.fields.#(name==neighbor-address).ValueByType.StringValue")
    fmt.Println(" Neighbor: ", data)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 8 / Streaming telemetry with gRPC"*

---

### 53. gNMIc — High-Level gNMI Client

**Principle:** Use `karimra/gnmic/api` over the lower-level `openconfig/gnmi`. Encode paths as strings (`api.Path("/interfaces/interface[name=Ethernet2]/config/description")`) instead of building `PathElem` structs by hand.

**Code:**
```go
func (r router) createTarget() (*target.Target, error) {
    return api.NewTarget(
        api.Name("gnmi"),
        api.Address(r.Hostname+":"+r.Port),
        api.Username(r.Username),
        api.Password(r.Password),
        api.Insecure(r.Insecure),
    )
}

func main() {
    for _, router := range inv.Routers {
        tg, _ := router.createTarget()
        ctx, cancel := context.WithCancel(context.Background())
        defer cancel()
        tg.CreateGNMIClient(ctx)
        defer tg.Close()

        for _, data := range info {
            setReq, _ := api.NewSetRequest(
                api.Update(
                    api.Path(data.Prefix+data.Path),
                    api.Value(data.Value, data.Encoding)),
            )
            configResp, _ := tg.Set(ctx, setReq)
            fmt.Println(prototext.Format(configResp))
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 9 / Using gNMI to configure network interfaces"*

---

### 54. Event-Driven Telemetry Pipeline (gNMI → Prometheus → Webhook)

**Principle:** Chain specialized tools: gNMIc (collect) → Prometheus TSDB (store) → AlertManager (route) → Go webhook (actuate). Keep the Go program tiny — it only translates alerts into device calls.

**Code:**
```go
// Prometheus alert arrives as JSON webhook
func alertHandler(w http.ResponseWriter, req *http.Request) {
    log.Println("Incoming alert")
    var alerts Alerts
    json.NewDecoder(req.Body).Decode(&alerts)
    for _, alert := range alerts.Alerts {
        if alert.Status == "firing" {
            if err := toggleBackup(alert.Labels.InterfaceName, "permit"); err != nil {
                w.WriteHeader(http.StatusInternalServerError)
                return
            }
            continue
        }
        toggleBackup(alert.Labels.InterfaceName, "deny")
    }
    w.WriteHeader(http.StatusOK)
}

// Toggle a prefix-list rule via Cumulus NVUE 3-stage commit
var backupRules = map[string][]int{
    "swp1": {10, 20},
}

func toggleBackup(intf string, action string) error {
    ruleIDs, _ := backupRules[intf]
    var pl PrefixList
    pl.Rules = make(map[string]Rule)
    for _, ruleID := range ruleIDs {
        pl.Rules[strconv.Itoa(ruleID)] = Rule{Action: action}
    }
    var payload nvue
    payload.Router.Policy.PrefixLists = map[string]PrefixList{plName: pl}
    b, _ := json.Marshal(payload)
    return sendBytes(b)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 9 / Event-manager sample program"*

---

### 55. gNOI Traceroute — Verify Path Diversity

**Principle:** gNOI's `System.Traceroute` streams `TracerouteResponse` messages. Use `goto` + labels for retry logic when control-plane rate-limiting drops probes. Compare hop sets across destinations to detect ECMP path divergence.

**Code:**
```go
conn, _ := grpc.Dial(target, grpc.WithInsecure())
defer conn.Close()
sysSvc := system.NewSystemClient(conn)
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

var wg sync.WaitGroup
wg.Add(len(destinations))
traceCh := make(chan map[string][]mapset.Set, len(destinations))

for _, dest := range destinations {
    go func(d string) {
        defer wg.Done()
    START:
        response, _ := sysSvc.Traceroute(ctx, &system.TracerouteRequest{
            Destination: d,
            Source:      source,
        })
        var route []mapset.Set
        for {
            resp, err := response.Recv()
            if errors.Is(err, io.EOF) { break }
            if int(resp.Hop) > len(route)+1 {
                if retryCount > retryMax-1 { goto FINISH }
                retryCount++
                goto START
            }
            if len(route) < int(resp.Hop) {
                route = append(route, mapset.NewSet())
            }
            route[resp.Hop-1].Add(resp.Address)
        }
    FINISH:
        traceCh <- map[string][]mapset.Set{d: route}
    }(dest)
}
wg.Wait()
close(traceCh)

// Compare hop sets across destinations
for hop, route := range routes {
    for myDest, myPaths := range route {
        for otherDest, otherPaths := range route {
            if myDest == otherDest { continue }
            if diff := myPaths.Difference(otherPaths); diff.Cardinality() > 0 {
                log.Printf("Found different paths at hop %d", hop)
            }
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 9 / Path verifier application"*

---

### 56. Packet Capturing with `gopacket` + `pcapgo`

**Principle:** Tap into traffic transparently with `pcapgo.NewEthernetHandle`. Attach a BPF filter so only the protocol of interest reaches user space. Iterate `PacketSource.Packets()` (a channel).

**Code:**
```go
func main() {
    handle, err := pcapgo.NewEthernetHandle(*intf)

    rawInstructions, _ := bpf.Assemble([]bpf.Instruction{
        bpf.LoadAbsolute{Off: 12, Size: 2},
        bpf.JumpIf{Cond: bpf.JumpNotEqual, Val: 0x800, SkipTrue: 3},
        bpf.LoadAbsolute{Off: 23, Size: 1},
        bpf.JumpIf{Cond: bpf.JumpNotEqual, Val: 0x11, SkipTrue: 1},
        bpf.RetConstant{Val: 4096},
        bpf.RetConstant{Val: 0},
    })
    handle.SetBPF(rawInstructions)

    packetSource := gopacket.NewPacketSource(handle, layers.LayerTypeEthernet)
    for packet := range packetSource.Packets() {
        sflowLayer := packet.Layer(layers.LayerTypeSFlow)
        if sflowLayer == nil { continue }
        sflow, ok := sflowLayer.(*layers.SFlowDatagram)
        if !ok { continue }
        for _, sample := range sflow.FlowSamples {
            for _, record := range sample.GetRecords() {
                p, ok := record.(layers.SFlowRawPacketFlowRecord)
                if !ok { continue }
                srcIP, dstIP := p.Header.NetworkLayer().NetworkFlow().Endpoints()
                sPort, dPort := p.Header.TransportLayer().TransportFlow().Endpoints()
                log.Printf("flow record: %s:%s <-> %s:%s\n", srcIP, sPort, dstIP, dPort)
            }
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 10 / Packet capturing, filtering, processing"*

---

### 57. Custom Transport Implementation (`goflow2`)

**Principle:** Implement `transport.TransportInterface` (`Send(key, data []byte) error`) to plug custom processing into a third-party pipeline. Build a flow key that is symmetric for ingress/egress by sorting IPs.

**Code:**
```go
type MyFlow struct {
    Key     string
    SrcAddr string `json:"SrcAddr,omitempty"`
    DstAddr string `json:"DstAddr,omitempty"`
    SrcPort int    `json:"SrcPort,omitempty"`
    DstPort int    `json:"DstPort,omitempty"`
    Count   int
}

type Heap []*MyFlow
type topTalker struct {
    flowMap map[string]*MyFlow
    heap    Heap
}

func (h Heap) Less(i, j int) bool { return h[i].Count > h[j].Count }

const flowMapKey = `%s:%d<->%s:%d`

func (c *topTalker) Send(key, data []byte) error {
    var myFlow MyFlow
    json.Unmarshal(data, &myFlow)

    ips := []string{myFlow.SrcAddr, myFlow.DstAddr}
    sort.Strings(ips)
    var mapKey string
    if ips[0] != myFlow.SrcAddr {
        mapKey = fmt.Sprintf(flowMapKey,
            myFlow.SrcAddr, myFlow.SrcPort, myFlow.DstAddr, myFlow.DstPort)
    } else {
        mapKey = fmt.Sprintf(flowMapKey,
            myFlow.DstAddr, myFlow.DstPort, myFlow.SrcAddr, myFlow.SrcPort)
    }

    myFlow.Key = mapKey
    foundFlow, ok := c.flowMap[mapKey]
    if !ok {
        myFlow.Count = 1
        c.flowMap[mapKey] = &myFlow
        heap.Push(&c.heap, &myFlow)
        return nil
    }
    c.heap.update(foundFlow)
    return nil
}

// Wire it up
tt := topTalker{
    flowMap: make(map[string]*MyPacket),
    heap:    make(Heap, 0),
}
formatter, _ := format.FindFormat(ctx, "json")
sSFlow := &utils.StateSFlow{
    Format:    formatter,
    Logger:    log.StandardLogger(),
    Transport: &tt,
}
go sSFlow.FlowRoutine(1, hostname, 6343, false)
```
*Ref: Network_Automation_with_Go.md — "Chapter 10 / Data plane telemetry aggregation"*

---

### 58. Table-Driven Tests

**Principle:** Encode each test case as a struct in a slice; range over them in a single `TestX(t *testing.T)`. Use `t.Errorf` (not `t.Fatal`) so all cases run.

**Do:**
- `_test.go` filename suffix; `Test<Name>` function prefix
- Use `package_x_test` to test only the public API
- Always run with `-race`

**Code:**
```go
package main

import (
    "container/heap"
    "testing"
)

type testFlow struct {
    startCount    int
    timesSeen     int
    wantPosition  int
    wantCount     int
}

type testCase struct {
    name  string
    flows map[string]testFlow
}

var testCases = []testCase{
    {
        name: "single packet",
        flows: map[string]testFlow{
            "1-1": {startCount: 1, timesSeen: 0, wantPosition: 0, wantCount: 1},
        },
    },
    {
        name: "last packet wins",
        flows: map[string]testFlow{
            "2-1": {startCount: 1, timesSeen: 1, wantPosition: 1, wantCount: 2},
            "2-2": {startCount: 2, timesSeen: 1, wantPosition: 0, wantCount: 3},
        },
    },
}

func TestHeap(t *testing.T) {
    for _, test := range testCases {
        h := make(Heap, 0)
        for key, f := range test.flows {
            flow := &MyFlow{Count: f.startCount, Key: key}
            heap.Push(&h, flow)
            for j := 0; j < f.timesSeen; j++ {
                h.update(flow)
            }
        }
        for i := 0; h.Len() > 0; i++ {
            f := heap.Pop(&h).(*MyFlow)
            tf := test.flows[f.Key]
            if tf.wantPosition != i {
                t.Errorf("%s: unexpected position for key %s: got %d, want %d",
                    test.name, f.Key, i, tf.wantPosition)
            }
            if tf.wantCount != f.Count {
                t.Errorf("%s: unexpected count for key %s: got %d, want %d",
                    test.name, f.Key, f.Count, tf.wantCount)
            }
        }
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 10 / Testing Go programs"*

---

### 59. Event-Driven BGP with CoreBGP

**Principle:** CoreBGP gives you a BGP FSM with plugin hooks. Implement `OnEstablished` (returns `handleUpdate`) and `handleUpdate` to inject custom behavior. Use GoBGP only for message encode/decode.

**Code:**
```go
type Plugin interface {
    GetCapabilities(...) []Capability
    OnOpenMessage(...) *Notification
    OnEstablished(...) handleUpdate
    OnClose(...)
}

const bgpPingType = 42

func (p *plugin) handleUpdate(peer corebgp.PeerConfig, update []byte) *corebgp.Notification {
    msg, err := bgp.ParseBGPBody(
        &bgp.BGPHeader{Type: bgp.BGP_MSG_UPDATE}, update)

    for _, attr := range msg.Body.(*bgp.BGPUpdate).PathAttributes {
        if attr.GetType() != bgpPingType { continue }

        source, dest, ts, err := parseType42(attr)
        sourceHost := string(bytes.Trim(source, "\x00"))
        destHost := string(bytes.Trim(dest, "\x00"))

        if sourceHost == *id {
            rtt := time.Since(ts).Nanoseconds()
            metric := fmt.Sprintf("bgp_ping_rtt_ms{device=%s} %f\n",
                destHost, float64(rtt)/1e6)
            p.store = append(p.store, metric)
            return nil
        }
        p.pingCh <- ping{source: source, ts: ts.Unix()}
        return nil
    }
    return nil
}

func (p *plugin) OnEstablished(peer corebgp.PeerConfig,
    writer corebgp.UpdateMessageWriter) corebgp.UpdateMessageHandler {
    go func() {
        for {
            select {
            case pingReq := <-p.pingCh:
                bytes, _ := p.buildUpdate(type42PathAttr,
                    peer.LocalAddress, peer.LocalAS)
                writer.WriteUpdate(bytes)
            case <-p.probeCh:
                bytes, _ := p.buildUpdate(type42PathAttr,
                    peer.LocalAddress, peer.LocalAS)
                writer.WriteUpdate(bytes)
            case <-withdraw.C:
                bytes, _ := p.buildWithdraw()
                writer.WriteUpdate(bytes)
            }
        }
    }()
    return p.handleUpdate
}

// GoBGP for encoding
func (p *plugin) buildWithdraw() ([]byte, error) {
    myNLRI := bgp.NewIPAddrPrefix(32, p.probe.String())
    withdrawnRoutes := []*bgp.IPAddrPrefix{myNLRI}
    msg := bgp.NewBGPUpdateMessage(withdrawnRoutes, []bgp.PathAttributeInterface{}, nil)
    return msg.Body.Serialize()
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 10 / Event-driven BGP state machine"*

---

### 60. Exposing Metrics via Cloudprober

**Principle:** Cloudprober can drive your probe via stdin/stdout. Trigger with a channel; reply with a `ProbeReply` containing the metric string.

**Code:**
```go
func main() {
    probeCh := make(chan struct{})
    resultsCh := make(chan string)

    peerPlugin := &plugin{
        probeCh:   probeCh,
        resultsCh: resultsCh,
    }

    if *cloudprober {
        go func() {
            serverutils.Serve(func(
                request *epb.ProbeRequest,
                reply *epb.ProbeReply,
            ) {
                probeCh <- struct{}{}
                reply.Payload = proto.String(<-resultsCh)
                if err != nil {
                    reply.ErrorMessage = proto.String(err.Error())
                }
            })
        }()
    }
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 10 / Collecting and exposing metrics"*

---

### 61. Dual-Format Encoding (XML + JSON from one struct)

**Principle:** A single struct can carry both `json:` and `xml:` tags, letting the same data model emit either format. Useful when integrating YANG/NETCONF (XML) and REST APIs (JSON).

**Code:**
```go
type DataEncodingExample struct {
    Key   string `json:"_key",xml:"_key"`
    Value string `json:"_value",xml:"_value"`
    VType string `json:"_type",xml:"_type"`
}

func main() {
    dataInput := DataEncodingExample{
        Key:   "blah",
        Value: "42",
        VType: "string",
    }
    jsonEncoded, _ := json.Marshal(dataInput)
    xmlEncoded, _ := xml.Marshal(dataInput)
    fmt.Println("JSON Encoded: ", string(jsonEncoded))
    fmt.Println("XML Encoded:  ", string(xmlEncoded))
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 11 / David Gee — Go's type system"*

---

### 62. Project Skeleton with Structured Logging & UUID

**Principle:** Standardize logging (`logrus`), config (`go-envconfig`), and per-invocation UUIDs for traceability — even for ad-hoc tools.

**Code:**
```go
const _VERSION = "0.0.1"

type Config struct {
    APIUser string `env:"PROG1_API_USER_ID"`
    APIKey  string `env:"PROG1_API_USER_ID"`
}

func (c *Config) GetToken(URL, uuid string) (string, error) {
    log.Info(fmt.Sprintf("system: updater, uuid: %v, message: logging into device with key %v\n",
        uuid, c.APIUser))
    return "JWT 42.42.42", nil
}

func main() {
    log.SetLevel(log.DebugLevel)
    uuid := uuid2.New().String()
    log.Info(fmt.Sprintf("system: updater, uuid: %v, version: %v, maintainer: davedotdev\n",
        uuid, _VERSION))
    ctx := context.Background()
    var c Config
    if err := envconfig.Process(ctx, &c); err != nil { log.Fatal(err) }
    token, err := c.GetToken("https://example.com/api/v1/auth", uuid)
    if err != nil { log.Fatal(err) }
    log.Debug(fmt.Sprintf("TODO: Got token from external provider: %v\n", token))
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 11 / David Gee — Growing your code"*

---

### 63. Containerlab Topology as Code

**Principle:** Describe multi-vendor topologies (Nokia SR Linux, NVIDIA Cumulus, Arista cEOS) in a single YAML file. `make lab-base` / `make lab-full` wrap `containerlab deploy`.

**Code:**
```yaml
# topo-base/topo.yml
topology:
  nodes:
    srl:
      kind: srl
      image: ghcr.io/nokia/srlinux:21.6.4
    ceos:
      kind: ceos
      image: ceos:4.26.4M
    cvx:
      kind: cvx
      image: networkop/cx:5.0.0
      runtime: docker
  links:
    - endpoints: ["srl:e1-1", "ceos:eth1"]
    - endpoints: ["cvx:swp1", "ceos:eth2"]
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / Creating the topology"*

---

### 64. Generic Device Data Model (vendor-agnostic input)

**Principle:** Use one Go struct (`Model`) as the universal input across SSH/HTTP/gNMI/YANG code paths. Vendor-specific transformations happen at the edge.

**Code:**
```go
type Model struct {
    Uplinks  []Link `yaml:"uplinks"`
    Peers    []Peer `yaml:"peers"`
    ASN      int    `yaml:"asn"`
    Loopback Addr   `yaml:"loopback"`
}
type Link struct {
    Name   string `yaml:"name"`
    Prefix string `yaml:"prefix"`
}
type Peer struct {
    IP  string `yaml:"ip"`
    ASN int    `yaml:"asn"`
}
type Addr struct {
    IP string `yaml:"ip"`
}

// Decode once, use everywhere
func main() {
    src, _ := os.Open("input.yml")
    defer src.Close()
    d := yaml.NewDecoder(src)
    var input Model
    d.Decode(&input)
}
```
*Ref: Network_Automation_with_Go.md — "Chapter 6 / Describing the network device configurations"*

---

## Anti-Patterns & Common Mistakes

- **Magic numbers in headers:** Use named constants (`bgpPingType = 42`) instead of bare ints → *fix:* declare `const` blocks at package level.
- **Naive goroutine fan-out without WaitGroup:** Program exits before workers finish → *fix:* `var wg sync.WaitGroup; defer wg.Wait()`.
- **Slice append across goroutines:** Append is not visible to caller when passed by value → *fix:* pass `*[]T` or use a channel.
- **Unprotected map access:** `concurrent map writes` panic or silent corruption → *fix:* `sync.Mutex`/`sync.RWMutex` or `sync.Map`.
- **JSON over Protobuf for high-throughput telemetry:** 4x size, slower encode/decode → *fix:* generate proto bindings with `protoc` and decode with `proto.Unmarshal`.
- **Hand-building YANG JSON:** Brittle, drifts from schema → *fix:* auto-generate with `ygot` (`ConstructIETFJSON`, `Marshal7951`).
- **Parsing CLI with regex only:** Brittle when output format changes → *fix:* TextFSM templates from `ntc-templates`.
- **SSH without `defer Close()`:** Resource leak, file descriptor exhaustion → *fix:* `defer` immediately after `Open`/`Dial`.
- **`InsecureSkipVerify: true` in production:** Man-in-the-middle risk → *fix:* ship a CA pool and pin host keys.
- **Wrapping errors with `%s`:** Loses the cause chain (`errors.Is`/`errors.As` won't work) → *fix:* use `%w`.
- **Logging + `os.Exit` inside library code:** Makes testing impossible → *fix:* return errors, let the caller decide.
- **Importing the entire `openconfig/gnmi` package when `gnmic` is enough:** Verbose, error-prone → *fix:* use `karimra/gnmic/api` for path-as-string ergonomics.
- **Bare `go run` for Ansible modules:** Arg passing differs from binary modules → *fix:* wrap with a bash shim that normalizes args to JSON.
- **Calling `Read` on closed body:** `panic: read on closed body` → *fix:* only `Read`/`io.Copy` before `defer Close()` fires.
- **Trusting `time.After` inside long loops:** Allocates a timer per iteration → *fix:* `time.NewTimer` + `Reset` for hot loops.
- **Silently dropping `proto.Unmarshal` errors:** Telemetry looks empty → *fix:* check error, log path, and continue.

## Decision Heuristics / Checklists

**When to use channels vs mutexes**
- Use **channels** when: passing ownership of data, fan-in/fan-out, signaling, work distribution.
- Use **mutexes** when: protecting a shared counter, caching map, or hot read-mostly state.
- Rule of thumb: "Don't communicate by sharing memory; share memory by communicating."

**Choosing a network API transport**
| Need | Use |
|---|---|
| Legacy CLI-only device | `crypto/ssh` or Scrapligo |
| Modern REST API (Cumulus, Nautobot) | `net/http` or `go-resty` |
| YANG + JSON (Arista, Nokia) | RESTCONF or JSON-RPC + `ygot` |
| Streaming telemetry / cfg at scale | gNMI via `karimra/gnmic` |
| Vendor-neutral ops (traceroute, reboot) | gNOI |
| Sub-millisecond control plane | gRPC + Protobuf |

**Checklist: production network automation tool**
1. [ ] Compiles cleanly with `go vet ./...` and `go test -race ./...`
2. [ ] All `Open`/`Dial` paired with `defer Close()`
3. [ ] All errors wrapped with `%w` and meaningful context
4. [ ] Concurrency bounded (worker pool or semaphore)
5. [ ] No `InsecureSkipVerify` outside dev (or escalate via flag)
6. [ ] Config via env vars (`os.Getenv` or `envconfig`)
7. [ ] Structured logging (`logrus` or `slog`)
8. [ ] Single static binary cross-compiled with `GOOS`/`GOARCH`
9. [ ] Version-stamped with `-ldflags='-X main.Version=...'`
10. [ ] Topology reproducible via Containerlab YAML

**Checklist: gRPC/gNMI integration**
1. [ ] `.proto` files checked in, `//go:generate` directive pinned
2. [ ] YANG models vendored or fetched with deterministic hashes
3. [ ] `grpc.WithInsecure()` only in lab; mTLS in prod
4. [ ] Subscription goroutines have a `context.WithCancel`
5. [ ] `Recv()` errors distinguished: `io.EOF` (clean) vs other (retry)
6. [ ] Telemetry decoders tolerate missing fields (`Get*` accessors)

## Key Takeaways

1. **Standard library first.** `net`, `net/http`, `encoding/*`, `crypto/ssh`, `io`, `sync` cover 80% of network automation needs without any external dependency.
2. **Concurrency is a language feature, not a library.** Goroutines + channels + the race detector make fan-out to thousands of devices both safe and cheap.
3. **Model-driven beats template-driven.** Use `ygot`/`protoc`/CUE to generate bindings from schemas; never hand-build YANG JSON.
4. **gNMI + gNOI are the future.** They replace SNMP + NETCONF + vendor SSH CLIs with a unified, vendor-neutral gRPC surface.
5. **Closed-loop > push-and-pray.** Hash the intent, poll derived state, remediate only on drift. This pattern scales from one device to a fleet.
6. **A Go binary is the deliverable.** Single static artifact, cross-compiled, version-stamped — no Python venv, no runtime deps, no interpreter on the target box.
7. **Test with table-driven tests + `-race`.** They catch the bugs that matter in network automation: parsing edge cases, concurrency races, schema mismatches.
8. **Don't over-engineer.** Marcus Hines: "If you think you need a goroutine, the chances are you probably do not." Profile with `pprof` first.
9. **Use Containerlab for reproducible labs.** Multi-vendor topologies in one YAML file — every example in the book runs against it.
10. **The ecosystem is Go-native.** Containerlab, Scrapligo, gNMIc, ygot, CoreBGP, GoBGP, gopacket, goflow2, Cloudprober, Prometheus, Terraform — all first-class Go.

## Cross-References
- Topic index: [[../INDEX.md]]
- Related concurrency patterns: [[Concurrency_in_Practice.md]] (if present)
- Related Go CLI design: [[../_TEMPLATE.md]]
- Containerlab topology reference: book repo `topo-base/topo.yml` and `topo-full/topo.yml`
- Official code: https://github.com/PacktPublishing/Network-Automation-with-Go
