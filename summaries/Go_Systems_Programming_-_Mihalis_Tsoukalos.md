# Go Systems Programming by Mihalis Tsoukalos - Comprehensive Summary

**Originally published:** September 2017 by Packt Publishing
**ISBN:** 978-1-78712-564-3
**Go version tested:** 1.8.x (macOS Sierra) and 1.3.3 (Debian Linux)

## Overview

*Go Systems Programming* is a practical guide to developing Unix system-level software using the Go programming language. The book covers the full spectrum of systems programming, from basic Go language features through file I/O, process management, signal handling, concurrency with goroutines, web applications, and network programming. Each chapter builds on the previous ones, progressively implementing real Unix utilities (pwd, which, find, wc, cp, dd, cat) in Go to demonstrate how systems tools work under the hood.

The book is structured in three parts: Go language fundamentals, file/directory/process programming, and advanced topics (goroutines, web, networking).

---

## Chapter 1: Getting Started with Go and Unix Systems Programming

### What Is Systems Programming?

Systems programming is a specialized area of programming concerned with developing software that interacts directly with the operating system and hardware. On Unix machines, this includes system administration tools, disk formatting utilities, network interface configuration, module loading, and kernel performance tracking. The `/etc` directory, found on all Unix systems, contains plain text configuration files that are manipulated by systems software.

The book organizes systems programming into these areas:
- **File and directory operations:** Reading, writing, creating, deleting, renaming files and directories
- **System file processing:** Working with log files and configuration files
- **Process management and signaling:** Creating, monitoring, and controlling Unix processes and handling signals
- **Network and web programming:** Building TCP/UDP servers, clients, and web applications
- **Concurrency:** Using goroutines and channels for parallel execution

### About Go

Go (or Golang) started as an internal Google project before becoming a popular open-source language. Its key strengths for systems programming include:
- A fast compiler that catches many errors at build time
- Garbage collection, removing the burden of manual memory management
- Static typing with type inference for cleaner code
- Built-in concurrency primitives (goroutines and channels)
- Cross-compilation support
- A comprehensive standard library

Go 1.8 features highlighted in the book include: `sort.Slice()` for easier sorting, a default GOPATH (`$HOME/go`), HTTP graceful shutdown support, and improved sorting performance through an optimized `sort` package.

### Two Useful Go Tools

- **gofmt:** Automatically formats Go source code according to a canonical style. The book strongly recommends using it on all code.
- **godoc:** Generates documentation from Go source code, displaying documentation for packages and their functions.

### Unix Process States

A Unix process can exist in several states:
- **Created:** The process has been created but not yet ready to execute
- **Running/Executing:** Currently using the CPU
- **Ready/Runnable:** Waiting for CPU time
- **Blocked/Waiting:** Waiting for an event (I/O, signal, etc.)
- **Stopped/Suspended:** Execution has been paused
- **Zombie:** Process has finished but its entry remains in the process table until the parent reads its exit status

Understanding process states is fundamental to writing systems software that interacts with the operating system process lifecycle.

---

## Chapter 2: Writing Programs in Go

### Compiling Go Code

Go code is compiled using `go build`, `go run` (compile and execute), or `go install` (compile and install). The resulting executable is a statically linked binary with no external dependencies (by default), making deployment straightforward.

### Command-Line Arguments

Go programs access command-line arguments via `os.Args`, where `os.Args[0]` is the program name and subsequent elements are the provided arguments. The book demonstrates this with `addCLA.go`, which sums integer command-line arguments:

```go
package main
import (
    "fmt"
    "os"
    "strconv"
)
func main() {
    arguments := os.Args
    sum := 0
    for i := 1; i < len(arguments); i++ {
        temp, _ := strconv.Atoi(arguments[i])
        sum = sum + temp
    }
    fmt.Println("Sum:", sum)
}
```

### User Input and Output

- **Getting input:** `fmt.Scanln()`, `fmt.Scanf()`, and `bufio.NewReader()` for reading user input
- **Printing output:** `fmt.Println()`, `fmt.Printf()`, and `fmt.Sprintf()` for formatted output

### Go Functions

Functions in Go can return multiple values and support named return values:

```go
func namedReturn(min, max int) (result int) {
    result = min + max
    return
}
```

**Anonymous functions** (closures) can be defined inline:

```go
func(x, y int) int {
    return x + y
}(1, 2)
```

### The defer Keyword

The `defer` statement schedules a function call to be executed when the surrounding function returns. It is commonly used for cleanup operations like closing files or unlocking mutexes. Deferred calls are executed in Last-In-First-Out (LIFO) order.

### Pointer Variables in Functions

Go supports pointers, allowing functions to modify variables passed to them:

```go
func getPointer(n *int) {
    *n = *n * *n
}
```

### Go Data Structures

**Arrays** have a fixed size defined at creation time. Accessing an out-of-bounds element is a compile-time error in Go.

**Slices** are dynamic, resizeable views into arrays. They have both a length and a capacity:

```go
aSlice := []int{-1, 4, 5, 0, 7, 9}
aSlice = append(aSlice, -100)
```

When a slice grows beyond its capacity, Go doubles the capacity automatically for performance.

**Maps** are Go's implementation of hash tables, supporting nearly any comparable type as a key:

```go
aMap := make(map[string]int)
aMap["Mon"] = 0
_, ok := aMap["Tuesday"]  // Check if key exists
```

**Structures** group multiple fields of different types:

```go
type message struct {
    X     int
    Y     int
    Label string
}
```

### Interfaces

Interfaces define a set of method signatures. Any type that implements those methods satisfies the interface:

```go
type coordinates interface {
    xaxis() int
    yaxis() int
}
```

This allows writing functions that accept any type satisfying the interface, enabling polymorphism without traditional inheritance.

### Creating Random Numbers

The `math/rand` package generates pseudorandom numbers. Always seed with a unique value (e.g., current time) to avoid identical sequences:

```go
rand.Seed(time.Now().Unix())
myrand := rand.Intn(max-min) + min
```

For cryptographically secure random numbers, use `crypto/rand` instead.

---

## Chapter 3: Advanced Go Features

### Error Handling in Go

Go uses the `error` type for error handling. A nil error means no error occurred. Functions can return error variables:

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

**Key principle:** Always check error values, especially in systems software. Using `_` to ignore errors is bad practice.

### Error Logging

The `log` package provides various logging functions:
- `log.Printf()` / `log.Println()` -- gentle logging with timestamp
- `log.Fatalf()` -- logs and terminates the program
- `log.Panicf()` -- logs, prints stack trace, and terminates

### Pattern Matching and Regular Expressions

The `regexp` package provides Go's regular expression capabilities:

```go
parse, err := regexp.Compile("[Mm]ihalis")
if err == nil {
    fmt.Println(parse.MatchString("Mihalis Tsoukalos"))  // true
    fmt.Println(parse.ReplaceAllString("mihalis Mihalis", "MIHALIS"))
}
```

The book demonstrates practical examples including:
- **Printing column values** from structured text using `strings.Fields()`
- **Creating summaries** by summing values from a specific column
- **Counting occurrences** of words or tokens using a map
- **Find and replace** using `regexp.Compile()` and `ReplaceAllString()`

### Reflection

The `reflect` package allows runtime type inspection:

```go
typeOfX1 := reflect.TypeOf(x1)
st1 := reflect.ValueOf(&x1).Elem()
for i := 0; i < st1.NumField(); i++ {
    f := st1.Field(i)
    fmt.Printf("%s = %v\n", f.Type(), f.Interface())
}
```

Reflection is useful for writing generic code that operates on unknown types.

### Calling C Code from Go

Go can call C code using the `cgo` tool and the `unsafe` package, though this is generally discouraged for portability reasons.

### Analyzing Software with strace(1) and DTrace

- **strace(1):** Intercepts and records system calls made by a process, invaluable for debugging systems software
- **DTrace:** Available on macOS and Solaris/SunOS for dynamic tracing of system behavior

### Avoiding Common Go Mistakes

- Not checking error return values
- Using `=` instead of `==` in comparisons (Go prevents this for most cases)
- Forgetting that slices are reference types
- Not using `defer` for cleanup operations
- Ignoring the `GOMAXPROCS` setting for CPU-bound programs

---

## Chapter 4: Go Packages, Algorithms, and Data Structures

### Algorithms and Big O Notation

The chapter introduces algorithmic complexity using Big O notation to describe how algorithm performance scales with input size. Common complexities discussed include O(1), O(n), O(n log n), O(n^2), and O(2^n).

### Sorting Algorithms

Go's `sort` package provides built-in sorting. The `sort.Slice()` function (Go 1.8+) simplifies sorting custom structures:

```go
sort.Slice(mySlice, func(i, j int) bool {
    return mySlice[i].weight < mySlice[j].weight
})
```

### Linked Lists in Go

The book implements a singly linked list with `Value`, `Next`, and `Prev` pointers, demonstrating insertion at the beginning and traversal:

```go
type Node struct {
    Value int
    Next  *Node
    Prev  *Node
}
```

### Trees in Go

A binary tree implementation is provided with a `TreeNode` struct and an `insert()` method that uses recursion to place values in the correct position:

```go
type TreeNode struct {
    Value       int
    Left, Right *TreeNode
}
```

### Developing a Hash Table in Go

The book implements a custom hash table with a fixed number of buckets and a hash function that distributes keys across buckets. Each bucket stores key-value pairs.

### Go Packages

- **Standard packages:** Go's extensive standard library covers I/O, networking, encoding, and more
- **Creating custom packages:** Place code in a directory under `$GOPATH/src/` and use `go install`
- **Private variables/functions:** Names starting with a lowercase letter are unexported (private to the package)
- **The init() function:** A special function called automatically when a package is imported, before `main()` runs
- **External packages:** Use `go get` to download and install third-party packages

### Garbage Collection

Go uses a concurrent, low-latency garbage collector. Developers generally do not need to manage memory manually, though understanding GC behavior helps with performance tuning. The `runtime.GC()` function can force garbage collection when needed.

---

## Chapter 5: Files and Directories

This is the first chapter focused entirely on systems programming.

### The flag Package

The `flag` package provides robust command-line argument parsing:

```go
var minusO = flag.Bool("o", false, "o flag")
var minusC = flag.Int("c", 0, "c flag")
flag.Parse()
```

This is far more robust than manually parsing `os.Args`.

### Dealing with Directories

The `os` package provides functions for directory operations:
- `os.Open()` to open a directory
- `os.Stat()` / `os.Lstat()` to get file information (the latter does not follow symlinks)
- `filepath.Walk()` to recursively traverse a directory tree

### Symbolic Links

Symlinks are handled using `os.Readlink()` and `os.Symlink()`:

```go
s, err := os.Lstat(path)
if s.Mode()&os.ModeSymlink != 0 {
    link, _ := os.Readlink(path)
}
```

### Implementing pwd(1) in Go

The book develops a Go version of the `pwd` command using `os.Getwd()` and `os.Getenv("PWD")`.

### Developing which(1) in Go

The `which` utility searches the PATH environment variable for executables:

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

### Developing find(1) in Go

The book progressively builds a Go implementation of `find(1)`:
1. **Basic traversal** using `filepath.Walk()`
2. **Directory-only mode** filtering for directories
3. **Adding command-line options** like `-mindepth`, `-maxdepth`, `-name` patterns
4. **Excluding filenames** and file extensions
5. **Regular expression matching** for filename filtering

### File Permission Bits

File permissions are accessed via `os.FileMode`:

```go
info, _ := os.Stat(filename)
mode := info.Mode()
fmt.Println("Permission bits:", mode.Perm())
```

### Deleting, Renaming, and Moving Files

```go
os.Remove(filename)          // Delete
os.Rename(oldName, newName)  // Rename or move
```

### Creating a Copy of a Directory Structure

The chapter concludes with a utility that replicates a source directory structure (directories only, no files) to a destination path.

---

## Chapter 6: File Input and Output

### Byte Slices

Byte slices (`[]byte`) are the fundamental type for file I/O in Go. They represent a mutable sequence of bytes and can be converted to/from strings.

### About Binary Files

Binary files contain data in a format that is not plain text. Go handles binary data using the `encoding/binary` package with `binary.Read()` and `binary.Write()`.

### Useful I/O Packages

- **io package:** Defines `io.Reader` and `io.Writer` interfaces, the foundation of Go's I/O model. Anything that reads data implements `io.Reader`; anything that writes data implements `io.Writer`.
- **bufio package:** Provides buffered I/O for better performance when reading/writing many small operations. Key types include `bufio.Scanner`, `bufio.Reader`, and `bufio.Writer`.

### Writing to Files

```go
f, err := os.Create(filename)
fmt.Fprintf(f, "Writing to file: %s\n", filename)
f.Close()
```

### Copying Files in Go

The book presents multiple approaches to file copying:
1. **Character-by-character** reading and writing (very slow)
2. **Using `io.Copy()`** -- the simplest and most efficient approach
3. **Reading entire file at once** with `ioutil.ReadFile()` (quick but memory-intensive for large files)
4. **Buffer-based copying** with configurable buffer size

Benchmarking shows buffer size dramatically affects performance. A 16-byte buffer copying 5GB takes over 10 minutes, while a 1MB buffer completes in about 7 seconds.

### Developing wc(1) in Go

The book implements the `wc` (word count) utility, counting lines, words, and characters:

```go
scanner := bufio.NewScanner(f)
for scanner.Scan() {
    line := scanner.Text()
    // Count lines, words, characters
}
```

Word counting uses regular expressions: `regexp.MustCompile("[^\\s]+")` to find non-whitespace sequences.

### Interprocess Communication

Go supports standard Unix IPC mechanisms including pipes, where the output of one process feeds as input to another.

### Sparse Files

Sparse files have "holes" (regions of null bytes) that occupy no disk space. The book shows how to create sparse files by seeking past unwritten regions.

### Reading and Writing Data Records

The `encoding/binary` package reads and writes structured binary records:

```go
binary.Write(file, binary.LittleEndian, &record)
binary.Read(file, binary.LittleEndian, &record)
```

### File Locking in Go

File locking prevents concurrent access conflicts using `sync.Mutex`:

```go
var mu sync.Mutex
mu.Lock()
// Write to file
mu.Unlock()
```

Forgetting to unlock causes a deadlock where all waiting goroutines freeze permanently.

### A Simplified dd Utility

The chapter implements a simplified version of the Unix `dd` command that copies data with specified block sizes and counts.

---

## Chapter 7: Working with System Files

### System Files

System files include log files (`/var/log/*`), configuration files (`/etc/*`), and other files used by the operating system and its services.

### Logging in Go

The `log` package provides basic logging with timestamps. The `log/syslog` package interfaces with the system log service:

```go
sysLog, err := syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, "myProgram")
sysLog.Info("Information message")
sysLog.Notice("Notice message")
sysLog.Warning("Warning message")
```

### Putting Data at the End of a File (Appending)

```go
f, err := os.OpenFile(filename, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
fmt.Fprintf(f, "New data\n")
f.Close()
```

### Altering Existing Data

Modifying existing file content requires reading the file, modifying in memory, and rewriting. The book shows how to find and replace specific lines in a text file.

### Processing Log Files

Practical examples include:
- Parsing Apache log files to extract IP addresses
- Reformatting timestamps in log entries
- Summarizing data from multiple log files

### File Permissions Revisited

```go
info, _ := os.Stat(filename)
mode := info.Mode()
// Check if world-writable
if mode.Perm()&0002 != 0 {
    fmt.Println("World-writable!")
}
```

Changing permissions with `os.Chmod()`:

```go
os.Chmod(filename, 0644)
```

### Finding User IDs and Groups

```go
user, _ := user.Lookup("username")
fmt.Println("UID:", user.Uid)
fmt.Println("GID:", user.Gid)
```

Finding all groups a user belongs to requires parsing `/etc/group` or using `os/user` package functions.

### Date and Time Operations

The `time` package handles all date/time operations:

```go
now := time.Now()
formatted := now.Format("Mon Jan 2 15:04:05 MST 2006")
parsed, _ := time.Parse("2006-01-02", "2017-01-01")
```

Go uses a unique reference time (Mon Jan 2 15:04:05 MST 2006) for formatting patterns instead of strftime-style codes.

### Rotating Log Files

The book develops a utility that rotates log files when they reach a specified size, renaming the current log file and creating a new one.

### Creating Good Random Passwords

Combining the `crypto/rand` package with configurable character sets to generate secure random passwords.

---

## Chapter 8: Processes and Signals

### Unix Processes and Signals

Signals are software interrupts sent to a process to notify it of events. Common signals include:
- **SIGINT** (Ctrl+C): Interrupt signal
- **SIGTERM**: Termination signal
- **SIGHUP**: Hangup detected (used for reloading config)
- **SIGKILL**: Kill signal (cannot be caught or ignored)
- **SIGUSR1/SIGUSR2**: User-defined signals

### Signal Handling in Go

The `os/signal` package handles Unix signals:

```go
sigs := make(chan os.Signal, 1)
signal.Notify(sigs, os.Interrupt, syscall.SIGTERM)
go func() {
    sig := <-sigs
    fmt.Println("Received:", sig)
}()
```

The book presents progressively more complex signal handlers:
1. **Single signal handler** (SIGINT only)
2. **Multi-signal handler** (SIGTERM, SIGINT, SIGHUP)
3. **Catch-all handler** that handles every catchable signal

### Rotating Log Files with Signals

A practical example that uses SIGUSR1 to trigger log file rotation, allowing administrators to rotate logs without restarting the process.

### Improving File Copying with Signals

A file copy program that displays progress when it receives SIGINFO (macOS) or SIGUSR1 (Linux), and handles SIGINT for graceful termination.

### Plotting Data

The book demonstrates generating data suitable for plotting with external tools like Gnuplot, showing how to export metrics from Go programs for visualization.

### Unix Pipes in Go

Implementing Unix pipes where data flows between processes:

```go
r, w, _ := os.Pipe()
w.WriteString("data through pipe\n")
w.Close()
// Read from r
```

### Implementing cat(1) in Go

A Go version of the `cat` command that reads from files or stdin and writes to stdout:

```go
scanner := bufio.NewScanner(f)
for scanner.Scan() {
    fmt.Println(scanner.Text())
}
```

### Unix Sockets in Go

Unix domain sockets provide interprocess communication on the same machine:

```go
// Server
l, _ := net.Listen("unix", "/tmp/socket")
conn, _ := l.Accept()

// Client
conn, _ := net.Dial("unix", "/tmp/socket")
```

### Programming a Unix Shell in Go

The chapter briefly discusses how one might begin implementing a shell in Go, including reading user input, parsing commands, and executing external programs using `os/exec`.

---

## Chapter 9: Goroutines - Basic Features

### About Goroutines

Goroutines are lightweight concurrent execution units managed by the Go runtime (not OS threads). They are created with the `go` keyword:

```go
go func() {
    fmt.Println("Running in a goroutine")
}()
```

**Concurrency vs. Parallelism:** Concurrency is about dealing with many things at once (structure), while parallelism is about doing many things at once (execution). Goroutines enable concurrency; parallel execution requires multiple CPU cores and proper GOMAXPROCS settings.

### The sync Package

**sync.WaitGroup** waits for a collection of goroutines to finish:

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

This is the recommended way to ensure all goroutines complete before the program exits. Without `WaitGroup`, you would need `time.Sleep()` which is unreliable.

### Channels

Channels are the communication mechanism between goroutines. They provide safe data exchange without shared memory:

```go
ch := make(chan int)
// Writing to a channel
ch <- value
// Reading from a channel
value := <-ch
```

Channels are blocking: a write blocks until someone reads, and a read blocks until someone writes. This synchronization behavior prevents race conditions.

### Pipelines

A pipeline connects goroutines through channels, where the output of one stage feeds into the input of the next:

```
[Goroutine 1] --channel1--> [Goroutine 2] --channel2--> [Goroutine 3]
```

Proper pipeline termination requires closing channels in order, starting from the first stage. Forgetting to close channels causes deadlocks.

### A Better Version of wc.go

The chapter develops a concurrent version of the `wc` utility where each file is processed in its own goroutine, with results aggregated through channels. The pipeline architecture:
1. **Stage 1:** Read filenames from command-line arguments
2. **Stage 2:** Process each file in a goroutine (count lines/words/chars)
3. **Stage 3:** Aggregate results and print totals

Benchmarking shows the goroutine version is faster than the sequential version when processing multiple files.

---

## Chapter 10: Goroutines - Advanced Features

### The Go Scheduler

Go uses an M:N scheduler that maps M goroutines onto N OS threads. The scheduler uses work-stealing to distribute goroutines across available threads efficiently.

### The select Keyword

The `select` statement lets a goroutine wait on multiple channel operations simultaneously:

```go
select {
case msg := <-ch1:
    fmt.Println("Received from ch1:", msg)
case msg := <-ch2:
    fmt.Println("Received from ch2:", msg)
case <-time.After(timeout):
    fmt.Println("Timed out")
}
```

`select` blocks until one of its cases can proceed. If multiple are ready, one is chosen randomly.

### Signal Channels

Signal channels carry no data -- they are used purely for signaling events:

```go
signal := make(chan struct{})
close(signal)  // Broadcast to all listeners
```

### Buffered Channels

Buffered channels allow a specified number of values to be written without a corresponding read:

```go
ch := make(chan int, 10)  // Buffer for 10 values
```

Buffered channels are useful when producers temporarily outpace consumers.

### Timeouts

The `time.After()` function creates a channel that sends the current time after a specified duration:

```go
select {
case result := <-ch:
    fmt.Println("Got result:", result)
case <-time.After(5 * time.Second):
    fmt.Println("Timed out!")
}
```

### Channels of Channels

Channels can carry other channels, enabling dynamic channel creation and routing:

```go
chOfCh := make(chan chan int)
```

### Nil Channels

A nil channel blocks forever. This is useful in `select` statements to effectively disable a case by setting a channel to nil.

### Shared Memory

When goroutines must share mutable state, Go provides synchronization primitives:

**sync.Mutex** provides exclusive locking:

```go
var mu sync.Mutex
mu.Lock()
// Critical section - modify shared data
mu.Unlock()
```

**sync.RWMutex** allows multiple concurrent readers or one exclusive writer:

```go
var rwmu sync.RWMutex
rwmu.RLock()   // Shared read lock
rwmu.RUnlock()
rwmu.Lock()    // Exclusive write lock
rwmu.Unlock()
```

### The dWC.go Utility Revisited

The chapter re-implements the word count utility three ways:
1. Using buffered channels for result collection
2. Using shared memory with mutex protection
3. Using `sync.RWMutex` for the read-heavy workload

Benchmarking compares all approaches, showing trade-offs between channel-based and mutex-based designs.

### Detecting Race Conditions

Go's race detector (`go run -race`) detects data races at runtime:

```go
// This has a race condition:
go func() {
    fmt.Println(i)  // i is shared unsafely
}()
```

The fix is to pass `i` as a parameter to the goroutine function, creating a copy:

```go
go func(n int) {
    fmt.Println(n)
}(i)
```

Race conditions commonly occur in anonymous goroutines that capture loop variables by reference.

### About GOMAXPROCS

`GOMAXPROCS` controls the number of OS threads available for executing goroutines. As of Go 1.5, the default is the number of available CPU cores. It can be adjusted:

```go
runtime.GOMAXPROCS(runtime.NumCPU())
```

Or via the environment variable: `export GOMAXPROCS=4`

---

## Chapter 11: Writing Web Applications in Go

### Web Clients

The `net/http` package provides HTTP client functionality:

```go
response, err := http.Get(url)
body, _ := ioutil.ReadAll(response.Body)
fmt.Println(string(body))
response.Body.Close()
```

Setting timeouts is critical for production clients:

```go
timeout := time.Duration(5 * time.Second)
client := http.Client{Timeout: timeout}
response, err := client.Get(url)
```

The book develops a more robust web client that handles errors properly and sets custom headers.

### A Small Web Server

```go
http.HandleFunc("/", handler)
http.ListenAndServe(":8001", nil)
```

The `http.ServeMux` type provides custom request routing:

```go
mux := http.NewServeMux()
mux.HandleFunc("/static", staticHandler)
mux.HandleFunc("/dynamic", dynamicHandler)
http.ListenAndServe(":8001", mux)
```

### The html/template Package

Go's `html/template` package generates HTML output from templates:

```go
t, _ := template.ParseFiles(templateFile)
t.Execute(w, data)
```

Templates support conditionals, loops, and variable interpolation. The book demonstrates serving both static HTML files and dynamically generated pages.

### JSON Handling

The `encoding/json` package handles JSON encoding and decoding:

```go
// Marshal: Go struct to JSON
data, _ := json.Marshal(structure)

// Unmarshal: JSON to Go struct
err := json.Unmarshal(jsonData, &structure)
```

The `Encode()` and `Decode()` functions work with streams (io.Writer/io.Reader), while `Marshal()` and `Unmarshal()` work with byte slices.

### Using MongoDB

The book demonstrates connecting to MongoDB using the official Go driver:
- Basic CRUD operations
- Iterating through query results
- Displaying data in a web interface

Similarly, connecting to MySQL using the `database/sql` package with the MySQL driver is shown, including executing queries and scanning results.

### A Handy Command-Line Utility

The chapter concludes with a utility that reads multiple web pages and counts keyword occurrences, combining HTTP client code with text processing and regular expressions.

---

## Chapter 12: Network Programming

### TCP/IP Fundamentals

The chapter covers the TCP/IP protocol suite:
- **TCP:** Connection-oriented, reliable, ordered delivery with a three-way handshake (SYN, SYN-ACK, ACK)
- **UDP:** Connectionless, unreliable, unordered delivery -- simpler and faster than TCP
- **IP:** The network layer protocol that handles addressing and routing

### Wireshark and tshark

Wireshark is a network protocol analyzer for inspecting network traffic. `tshark` is its command-line version. Both are essential tools for debugging network applications.

### DNS Lookups

The `net` package provides DNS lookup functions:

```go
// Lookup host by name
ips, _ := net.LookupHost("example.com")

// Lookup NS records
ns, _ := net.LookupNS("example.com")

// Reverse lookup by IP
names, _ := net.LookupAddr("1.2.3.4")
```

### TCP Server

```go
l, _ := net.Listen("tcp", ":1234")
c, _ := l.Accept()
for {
    netData, _ := bufio.NewReader(c).ReadString('\n')
    c.Write([]byte(netData))  // Echo back
}
```

Alternative implementations use `net.ResolveTCPAddr()` and `net.ListenTCP()` for more control over socket options.

### TCP Client

```go
c, _ := net.Dial("tcp", "localhost:1234")
fmt.Fprintf(c, "Hello\n")
message, _ := bufio.NewReader(c).ReadString('\n')
```

### UDP Server and Client

UDP uses connectionless communication:

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

UDP does not require `Accept()` since it is connectionless.

### Concurrent TCP Server

The concurrent server spawns a goroutine per client connection:

```go
for {
    c, _ := l.Accept()
    go handleConnection(c)  // Each client gets its own goroutine
}
```

This is the standard pattern for building scalable TCP servers in Go. The book demonstrates multiple clients connecting simultaneously.

### Remote Procedure Call (RPC)

RPC allows a client to call functions on a remote server as if they were local. Go's `net/rpc` package implements this:

**Shared interface (sharedRPC.go):**
```go
type MyInts struct {
    A1, A2 uint
    S1, S2 bool
}
type MyInterface interface {
    Add(arguments *MyInts, reply *int) error
    Subtract(arguments *MyInts, reply *int) error
}
```

**RPC Server:**
```go
rpc.Register(myInterface)
l, _ := net.ListenTCP("tcp", tcpAddr)
for {
    c, _ := l.Accept()
    rpc.ServeConn(c)
}
```

**RPC Client:**
```go
c, _ := rpc.Dial("tcp", "localhost:1234")
err = c.Call("MyInterface.Add", args, &reply)
```

The client calls remote methods by name using `Call()`, with arguments and a reply pointer. RPC uses TCP for transport and can work across machines.

---

## Key Takeaways

1. **Go is well-suited for systems programming.** Its compiled binaries, static linking, garbage collection, and built-in concurrency primitives make it a practical alternative to C for many systems programming tasks.

2. **Error handling is non-negotiable in systems software.** Always check error return values. Use `log` for non-fatal errors and `log.Fatal` only for truly unrecoverable situations. Never ignore errors with `_` in production systems code.

3. **The Go standard library is remarkably complete.** File I/O, network programming, regular expressions, HTTP servers/clients, JSON encoding, process management, and signal handling are all covered by the standard library without external dependencies.

4. **Goroutines and channels are Go's concurrency model.** Goroutines are cheap (starting at ~2KB stack) and managed by the Go runtime. Channels provide safe communication between goroutines, following the principle: "Don't communicate by sharing memory; share memory by communicating."

5. **Use the right synchronization primitive.** `sync.WaitGroup` for waiting on goroutines, channels for communication, `sync.Mutex`/`sync.RWMutex` for shared memory, and `select` for multiplexing channel operations.

6. **Race conditions are easy to create and hard to debug.** Always use `go run -race` during development. The most common source is anonymous goroutines capturing loop variables by reference instead of by value.

7. **The `io.Reader` and `io.Writer` interfaces are the foundation of Go I/O.** Nearly every I/O operation in Go is built on these two interfaces. Understanding them unlocks the entire I/O ecosystem.

8. **Signal handling enables robust daemon behavior.** Using signals for log rotation, progress reporting, and graceful shutdown is a standard Unix practice that Go supports well through the `os/signal` package.

9. **Network programming follows consistent patterns.** TCP servers listen and accept, UDP servers read from connections. Concurrent TCP servers spawn goroutines per connection. RPC abstracts remote function calls over TCP.

10. **File operations require careful permission and error handling.** Systems software must deal with file permissions, symlinks, directory traversal, and concurrent file access (locking). The `os`, `path/filepath`, and `bufio` packages provide all necessary tools.

11. **Pipelines are a powerful concurrency pattern.** Connecting goroutines through channels in stages allows for composable, testable concurrent processing. Always close channels properly to avoid deadlocks.

12. **Benchmark your code.** The book consistently benchmarks different approaches (file copy buffer sizes, sequential vs. concurrent processing), demonstrating that intuition about performance is often wrong. Use `time` command, Go benchmarks, and profiling tools to measure actual performance.

13. **Build real Unix tools to learn.** The book's approach of reimplementing standard Unix utilities (pwd, which, find, wc, cp, dd, cat) provides practical, grounded learning that teaches both Go and Unix internals simultaneously.

14. **GOMAXPROCS matters for CPU-bound programs.** While Go defaults to using all available cores since version 1.5, understanding and controlling this setting is important for performance-critical applications.

15. **Go compiles to self-contained static binaries.** This makes Go systems software easy to deploy -- a single binary with no runtime dependencies, unlike Python, Ruby, or Node.js applications.
