# Go Systems Programming

**Author:** Mihalis Tsoukalos
**Topic tags:** `#systems` `#cli` `#concurrency` `#unix`
**Language focus:** Go-first / Unix-focused
**Sources:** `markdown_output/Go_Systems_Programming_-_Mihalis_Tsoukalos/Go_Systems_Programming_-_Mihalis_Tsoukalos.md` · `summaries/Go_Systems_Programming_-_Mihalis_Tsoukalos.md`

## TL;DR
A hands-on tour of writing system utilities in Go — reimplementing Unix classics (`pwd`, `which`, `find`, `wc`, `cp`, `dd`, `cat`), using `flag` for CLI parsing, signal handling with `os/signal`, goroutines/channels/pipelines for I/O concurrency, `sync.Mutex`/`RWMutex` for shared state, race detection with `-race`, and TCP/UDP/RPC networking. Apply when porting shell tooling to Go or building native Unix daemons.

---

## Best Practices by Topic

### Why Go for Unix Systems Programming

**Principle:** Go produces small, statically-linked binaries that compile fast and run anywhere — yet the language is expressive enough for systems work without the footguns of C.

**Do:**
- Use Go for new CLI tools, network daemons, and log processors.
- Reach for `os`, `io`, `bufio`, `net`, `syscall` (and `golang.org/x/sys/unix`) — they cover 95 % of Unix sysprog needs.
- Build with `go build` for a single, dependency-free binary you can `scp` to a server.

**Don't:**
- Don't write a Go program that shells out to `sed`/`awk` to do core work — call the libraries directly.
- Don't reinvent `grep`/`find` from scratch — start from the patterns this book demonstrates and extend.

*Ref: Go_Systems_Programming.md — "What is systems programming?", "About Go", "Advantages and disadvantages of Go"*

---

### Two Useful Tools: `gofmt` and `godoc`

**Principle:** Standard tooling enforces a single canonical style and surfaces docs locally.

**Do:**
- Run `gofmt -w file.go` before every commit (or wire it into your editor's save).
- Use `godoc -http=:6060` to browse docs offline.
- `go doc fmt Println` from the terminal to look up a signature.

**Don't:**
- Don't argue about brace placement or import ordering — `gofmt` already decided.

**Code:**
```bash
# Format in place
gofmt -w main.go

# Or fix on stdout (no -w)
gofmt unglyHW.go

# Run local docs server
godoc -http=:8080

# Quick lookup
go doc fmt Println
```

*Ref: Go_Systems_Programming.md — "Two useful Go tools"*

---

### The States of a Unix Process

**Principle:** A process is an execution environment with instructions, user-data, and system-data parts. The kernel scheduler — not your program — decides when it runs.

**Do:**
- Treat process state as opaque to your application code.
- Use `syscall.Exec` for low-level fork/exec-style behaviour.
- Use `os/exec` for the common case.

**Don't:**
- Don't assume your goroutine will run in any particular order — the kernel + Go scheduler decide.

*Ref: Go_Systems_Programming.md — "The various states of a Unix process"*

---

### Command-Line Argument Parsing with `flag`

**Principle:** The stdlib `flag` package is sufficient for 80 % of CLIs. Avoid `if`-ladder parsing.

**Do:**
- Use `flag.Bool`, `flag.Int`, `flag.String` for typed flags.
- Call `flag.Parse()` exactly once, before reading `flag.Args()`.
- Provide a usage string for every flag.
- Use `NewFlagSet` for subcommands with isolated flag sets.

**Don't:**
- Don't keep growing `if arg == "-x"` chains — switch to `flag` early.

**Code:**
```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    minusA := flag.Bool("a", false, "show all instances")
    minusS := flag.Bool("s", false, "silent return code only")
    flag.Parse()

    args := flag.Args()
    if len(args) == 0 {
        fmt.Println("Please provide an argument!")
        return
    }

    file := args[0]
    _ = file
    _ = *minusA
    _ = *minusS
}
```

*Ref: Go_Systems_Programming.md — "The flag package", "Command-line arguments revisited!"*

---

### Type-Safe CLI Args: `int`, `String`, `Bool`

**Principle:** `flag.Int` parses and validates — you don't need `strconv.Atoi` after.

**Do:**
- Use `flag.Int("port", 8080, "listen port")` to get `*int`.
- Use `flag.Duration` for time args (`-timeout=5s`).
- Use `flag.Var` to plug in custom `flag.Value` types.

**Don't:**
- Don't write your own parser — `flag` already handles `-flag value` and `-flag=value`.

*Ref: Go_Systems_Programming.md — "The flag package"*

---

### Strings, Bytes, and Conversions

**Principle:** All CLI args arrive as `string`. Use `strconv` to convert, never panic on error.

**Do:**
- Always check the `error` from `strconv.Atoi`, `ParseFloat`, `ParseInt`.
- Use `fmt.Sscanf` or `strconv.ParseUint` for fixed-width binary formats.

**Don't:**
- Don't ignore `err` from `strconv.Atoi` — bad input silently becomes 0.

**Code:**
```go
temp, err := strconv.Atoi(arguments[i])
if err != nil {
    fmt.Println("Ignoring", arguments[i])
    continue
}
sum += temp
```

*Ref: Go_Systems_Programming.md — "Finding the sum of the commandline arguments", "The addCLA.go program revisited"*

---

### Error Handling in Systems Programs

**Principle:** Systems software is correctness-critical. Every error must be checked, every message precise ("File not found" vs "Not enough permissions to read file").

**Do:**
- Return `(value, error)` and check at every callsite.
- Use `errors.New("cannot divide by zero")` for sentinel messages.
- Prefer `fmt.Errorf("%s is not a regular file", src)` for context-rich errors.

**Don't:**
- Don't use `panic` for normal errors — that's for unrecoverable invariants.

**Code:**
```go
func division(x, y int) (int, error, error) {
    if y == 0 {
        return 0, nil, errors.New("Cannot divide by zero!")
    }
    if x%y != 0 {
        return x / y, errors.New("There is a remainder!"), nil
    }
    return x / y, nil, nil
}
```

*Ref: Go_Systems_Programming.md — "Error handling in Go", "Functions can return error variables"*

---

### Error Logging with `log`

**Principle:** `log.Print*` adds timestamps automatically. `log.Fatal` exits after printing — reserve for truly fatal conditions.

**Do:**
- Use `log.Printf("op=%s err=%v", op, err)` for diagnostic context.
- Use `log.Fatal` only when the program cannot continue (no recover possible).
- Pipe stderr to log files (`./tool 2>> app.log`).

**Don't:**
- Don't use `log.Fatal` for routine errors — it kills your program.
- Don't mix `log` and `fmt` for diagnostic output — pick one.

**Code:**
```go
log.Printf("log.Print() function: %d", x)
log.Panicf("log.Panicf() function: %d", x) // prints stack, panics
```

*Ref: Go_Systems_Programming.md — "About error logging"*

---

### `defer` for Resource Cleanup

**Principle:** `defer` runs a function when the surrounding function returns — perfect for `Close()` on every open handle.

**Do:**
- Place `defer f.Close()` immediately after a successful `os.Open`.
- Remember that deferred calls run in LIFO order.
- For huge loop counts, lift `defer` into a helper to avoid the per-call overhead.

**Don't:**
- Don't `defer` in a 10 000-iteration loop — it accumulates until the function returns.

**Code:**
```go
func a1() {
    for i := 0; i < 3; i++ {
        defer fmt.Print(i, " ")
    }
}
// Output on return: "2 1 0" (LIFO order)
```

*Ref: Go_Systems_Programming.md — "The defer keyword"*

---

### Anonymous Functions and Closures

**Principle:** Anonymous functions are inline `func`s with local usage. They become closures over variables they reference.

**Do:**
- Use anonymous functions for one-off goroutines, callbacks, sort comparators.
- Pass loop variables as arguments to avoid the classic closure-over-loop bug.

**Don't:**
- Don't reassign the same variable to different anonymous functions — readers can't tell which one runs.
- Don't capture loop variables in goroutines without arguments — `for i := 0; i < n; i++ { go func() { fmt.Println(i) }() }` prints `n` `n` times.

**Code:**
```go
// Buggy: every goroutine sees the final i
for i := 0; i < 3; i++ {
    go func() { fmt.Print(i, " ") }()
}
// Output: "3 3 3"

// Correct: pass i as argument
for i := 0; i < 3; i++ {
    go func(n int) { fmt.Print(n, " ") }(i)
}
// Output: "2 1 0" (order non-deterministic)
```

*Ref: Go_Systems_Programming.md — "Anonymous functions", "The defer keyword"*

---

### Naming Return Values for Clarity and `defer` Use

**Principle:** Named returns act as declared locals and let `defer` modify them.

**Do:**
```go
func minMax(x, y int) (min, max int) {
    if x > y { min = y; max = x } else { min = x; max = y }
    return // naked return — uses named values
}
```

**Don't:**
- Don't name every return — only when the name aids documentation or enables `defer` to update.

*Ref: Go_Systems_Programming.md — "Naming the return values of a Go function"*

---

### Slices vs Arrays

**Principle:** Arrays are fixed-size, value-copied; slices are dynamic, header-by-reference.

**Do:**
- Use slices for almost everything (`make([]T, 0, hint)`).
- Use arrays for fixed-size data you want stack-allocated (a `[3]int` doesn't escape).
- `append` grows slices automatically; pre-size with `make` when you know the final length.

**Don't:**
- Don't pass large arrays by value — slices share underlying storage and are cheap.

**Code:**
```go
aSlice := []int{-1, 4, 5, 0, 7, 9}
aSlice = append(aSlice, -100)
// cap doubles: 6 -> 12

anotherSlice := make([]int, 4) // zero-initialised
```

*Ref: Go_Systems_Programming.md — "Arrays", "Slices"*

---

### Maps: Existence Check and Iteration

**Principle:** `value, ok := m[key]` is the safe way to test existence; iteration order is intentionally randomised.

**Do:**
- Use the comma-ok idiom: `_, ok := counts[word]; if ok { ... }`.
- Pre-size with `make(map[K]V, hint)` when you know the count.
- Don't rely on iteration order — it's randomised by design.

**Don't:**
- Don't use `m[key] == zero` to test existence — the value might genuinely be zero.

**Code:**
```go
counts := make(map[string]int)
for _, word := range data {
    counts[word]++
}

_, ok := counts["Tuesday"]
if ok {
    fmt.Println("Tuesday exists")
}
```

*Ref: Go_Systems_Programming.md — "Maps"*

---

### Sorting with `sort.Slice` (Go 1.8+)

**Principle:** `sort.Slice(s, less func(i, j int) bool)` sorts any slice with a comparator callback.

**Do:**
- Provide a comparator that returns `s[i] < s[j]` for ascending.
- Use `sort.SliceStable` if relative order matters for equal elements.

**Don't:**
- Don't implement `sort.Interface` by hand unless you need a custom data structure.

**Code:**
```go
people := []aStructure{
    {"Mihalis", 180, 90},
    {"Marietta", 155, 45},
}
sort.Slice(people, func(i, j int) bool {
    return people[i].weight < people[j].weight
})
```

*Ref: Go_Systems_Programming.md — "The sort.Slice() function"*

---

### Big-O Awareness for System Software

**Principle:** The right data structure makes a 1000× difference. Built-in `map` lookups are O(1) (hash); slices are O(n) for search.

**Do:**
- Prefer `map[K]V` for lookups; slice for ordered iteration.
- Remember: array operations are faster than map operations when linear scans suffice.
- Quicksort is O(n log n) on average, O(n²) worst case — bubble sort is always O(n²).

*Ref: Go_Systems_Programming.md — "The Big O notation", "Sorting algorithms"*

---

### Linked Lists, Trees, and Hash Tables (When You Need Them)

**Principle:** Built-in types (slice, map) outperform custom data structures in nearly all system-level code. Build custom ones only when requirements demand.

**Do:**
- Implement linked lists / trees / hash tables only as exercises or when a profile demands it.
- Always store the `head` pointer safely (Go's zero-value pointer is `nil`, so use sentinel nodes if you need a non-nil empty state).

*Ref: Go_Systems_Programming.md — "Linked lists in Go", "Trees in Go", "Developing a hash table in Go"*

---

### `path/filepath` for OS-Aware Paths

**Principle:** `path/filepath` is the OS-correct path library. Use `filepath.Walk` / `WalkDir` for tree traversal.

**Do:**
- Use `filepath.Walk(root, walkFunc)` to visit every file/dir.
- Pass a `walkFunction` that re-checks the entry with `os.Lstat` (filesystem races between walk and walkFunction).
- Use `filepath.EvalSymlinks` to canonicalise.

**Don't:**
- Don't use `path.Join` for filesystem paths — it always uses `/`.

**Code:**
```go
func walkFunction(path string, info os.FileInfo, err error) error {
    if err != nil {
        return err
    }
    fmt.Println(path)
    return nil
}

err := filepath.Walk(root, walkFunction)
```

*Ref: Go_Systems_Programming.md — "Traversing a directory tree", "About symbolic links"*

---

### Symbolic Links: `Lstat` vs `Stat`

**Principle:** `os.Lstat` reads link metadata; `os.Stat` follows. Use the right one.

**Do:**
- Use `os.Lstat` to detect symlinks: `fileinfo.Mode()&os.ModeSymlink != 0`.
- Use `filepath.EvalSymlinks` to resolve chains.
- Skip symbolic links during destructive operations (e.g., `cpStructure`).

**Code:**
```go
if fileInfo.Mode()&os.ModeSymlink != 0 {
    fmt.Println("Skipping", currentPath)
    return nil
}
```

*Ref: Go_Systems_Programming.md — "About symbolic links", "Creating a copy of a directory structure"*

---

### Permission Bit Reading

**Principle:** `os.FileMode` carries the full permission string (`drwxr-xr-x`). Read it with `mode.String()` or `mode.Perm()`.

**Do:**
- Print `mode.String()` for human-readable form.
- Use `mode.IsRegular()`, `mode.IsDir()`, `mode&os.ModeNamedPipe != 0` to classify.
- Convert to numeric with `mode.Perm()` for `os.Chmod`.

**Code:**
```go
info, _ := os.Stat(filename)
mode := info.Mode()
fmt.Println(mode)               // -rw-------
fmt.Println(mode.Perm())       // 0600
fmt.Println(mode.IsRegular())  // true
```

*Ref: Go_Systems_Programming.md — "Printing the permission bits of a file or directory"*

---

### Implementing `pwd`

**Principle:** `os.Getwd` returns the current directory; `filepath.EvalSymlinks` resolves the physical path.

**Do:**
- Use `os.Getwd` for the logical path.
- Use `EvalSymlinks(pwd)` only when `-P` is requested.

**Don't:**
- Don't implement your own `getcwd(3)` — `os.Getwd` already calls it.

**Code:**
```go
pwd, err := os.Getwd()
if err == nil {
    fmt.Println(pwd)
}
```

*Ref: Go_Systems_Programming.md — "Implementing the pwd(1) command"*

---

### Implementing `which`

**Principle:** Walk `$PATH`, stat each candidate, return the first executable.

**Do:**
- Split `PATH` with `strings.Split(path, ":")`.
- Verify `mode.IsRegular() && mode&0o111 != 0` — must be a regular file with any execute bit.
- Support `-a` (all matches) and `-s` (silent / exit code only).

**Don't:**
- Don't forget to check the executable bit — a directory in `$PATH` should be skipped.

**Code:**
```go
path := os.Getenv("PATH")
for _, dir := range strings.Split(path, ":") {
    full := dir + "/" + file
    info, err := os.Stat(full)
    if err != nil { continue }
    if info.Mode().IsRegular() && info.Mode()&0o111 != 0 {
        fmt.Println(full)
        return
    }
}
```

*Ref: Go_Systems_Programming.md — "Developing the which(1) utility in Go"*

---

### Implementing `find`

**Principle:** A `find`-like tool is `filepath.Walk` plus a `walkFunction` that classifies entries.

**Do:**
- Use `os.Lstat` inside the walker to detect symlinks.
- Classify via `Mode()`: regular, dir, symlink, named pipe, socket.
- Support `-x` (exclude name) and `-ext` (exclude extension) and `-re` (regex).

**Don't:**
- Don't allocate a fresh regex per file — compile once outside the walker.

*Ref: Go_Systems_Programming.md — "Developing find(1) in Go", "Excluding filenames from the find output", "Using regular expressions"*

---

### Implementing `cp`

**Principle:** Copying a file = open source, open destination, loop `Read`/`Write`, close both.

**Do:**
- Refuse to overwrite unless explicitly asked.
- Choose buffer size based on file size: 1 MiB is a sweet spot for most workloads.
- Use `io.Copy` for a one-liner; use a manual buffer loop when you need progress reporting.

**Don't:**
- Don't read the entire file into memory (`ioutil.ReadFile`) for huge inputs.

**Code:**
```go
func Copy(src, dst string, bufferSize int64) error {
    source, err := os.Open(src)
    if err != nil { return err }
    defer source.Close()

    dest, err := os.Create(dst)
    if err != nil { return err }
    defer dest.Close()

    buf := make([]byte, bufferSize)
    for {
        n, err := source.Read(buf)
        if n > 0 {
            if _, werr := dest.Write(buf[:n]); werr != nil { return werr }
        }
        if err == io.EOF { break }
        if err != nil { return err }
    }
    return nil
}
```

*Ref: Go_Systems_Programming.md — "Copying files in Go", "An even better file copy program", "Benchmarking file copying operations"*

---

### Buffer Size Tuning for File Copy

**Principle:** A 16-byte buffer makes `cp` 100× slower than a 1 MiB buffer. Sweet spot: 1 MiB for typical files.

**Benchmark pattern (5 GB file):**
| Buffer | Time    |
|--------|---------|
| 16 B   | 10:41   |
| 1024 B | 16.5 s  |
| 1 MiB  | 7.2 s   |
| 1 GiB  | 8.6 s   |

**Don't:**
- Don't pick buffer = file size — no benefit, wastes memory.

*Ref: Go_Systems_Programming.md — "Benchmarking file copying operations"*

---

### Implementing `wc`

**Principle:** Read line-by-line with `bufio.NewReader` and a regex for word counting.

**Do:**
- Use `regexp.MustCompile("[^\\s]+")` to split words on whitespace.
- Track lines, words, characters in one pass.
- Print `total` when more than one file is given.

**Don't:**
- Don't iterate runes for character counting — `len(line)` is the byte count, but that's what Unix `wc` reports.

**Code:**
```go
r := regexp.MustCompile("[^\\s]+")
for range r.FindAllString(line, -1) {
    numberOfWords++
}
```

*Ref: Go_Systems_Programming.md — "Developing wc(1) in Go", "Counting words"*

---

### Implementing `dd` (Simplified)

**Principle:** `dd if=src of=dst bs=N count=M` = read `M` blocks of `N` bytes from `src`, write to `dst`.

**Do:**
- Allocate a `[]byte` of `bs` per iteration.
- Always close the destination file in a `defer`.
- Reset (`buf = nil`) the buffer between iterations so `append` doesn't grow it unboundedly.

**Code:**
```go
buf := make([]byte, *bs)
buf = nil
for i := 0; i < *count; i++ {
    createBytes(&buf, *bs)
    if _, err := dst.Write(buf); err != nil {
        log.Fatal(err)
    }
    buf = nil
}
```

*Ref: Go_Systems_Programming.md — "A simplified Go version of the dd utility"*

---

### Sparse Files

**Principle:** A sparse file has holes that don't occupy disk blocks — created by `Seek` past EOF then writing one byte.

**Do:**
- Use `os.Seek(size-1, 0)` then `Write([]byte{0})` to create a sparse file.
- Verify with `ls -ls` — block count < size.
- Useful for stubbing huge test data without disk cost.

**Don't:**
- Don't assume `mmap`-backed filesystems support holes — macOS HFS does not.

**Code:**
```go
fd, _ := os.Create(filename)
fd.Seek(SIZE-1, 0)
fd.Write([]byte{0})
fd.Close()
```

*Ref: Go_Systems_Programming.md — "Sparse files in Go"*

---

### Reading from `os.Stdin` vs Files

**Principle:** When a CLI receives a filename, read it; otherwise read `os.Stdin`. The same `*os.File` works for both.

**Do:**
```go
var f *os.File
if len(os.Args) == 1 {
    f = os.Stdin
} else {
    f, _ = os.Open(os.Args[1])
    defer f.Close()
}
```

**Don't:**
- Don't open `/dev/stdin` explicitly — `os.Stdin` already is it.

*Ref: Go_Systems_Programming.md — "Reading from standard input"*

---

### Reading File by Rune

**Principle:** `bufio.ScanRunes` is the easy way to walk a text file rune-by-rune.

**Do:**
- Use `s.Split(bufio.ScanRunes)` then `for s.Scan() { fmt.Print(s.Text()) }`.
- Validate byte ↔ rune conversion when character counting.

**Code:**
```go
s := bufio.NewScanner(strings.NewReader(in))
s.Split(bufio.ScanRunes)
for s.Scan() { fmt.Print(s.Text()) }
```

*Ref: Go_Systems_Programming.md — "Reading a text file character by character"*

---

### Reading Columns from Structured Text

**Principle:** `strings.Fields` splits on whitespace, giving you a `[]string`. Combine with `flag.Int` to pick a column.

**Do:**
- Always verify `len(data) >= column` before indexing.
- Use `flag.Int("COL", 1, "Column number")` for the column argument.

**Don't:**
- Don't use `strings.Split` with a literal space — it breaks on runs of spaces and tabs.

**Code:**
```go
data := strings.Fields(line)
if len(data) >= column {
    fmt.Println(data[column-1])
}
```

*Ref: Go_Systems_Programming.md — "Printing all the values from a given column of a line", "Finding out the third column of a line"*

---

### Tab/Space Conversion

**Principle:** Use `strings.Replace` to swap tabs and spaces. Print to stdout — let the user redirect.

**Code:**
```go
if convertTabs {
    newLine = strings.Replace(line, "\t", "    ", -1)
}
fmt.Print(newLine)
```

*Ref: Go_Systems_Programming.md — "Doing some file editing!"*

---

### File Locking with `sync.Mutex` (Process-Internal)

**Principle:** A `sync.Mutex` is a process-internal file lock. It does **not** use `flock(2)`.

**Do:**
- Wrap all reads/writes of a `*os.File` with a global `sync.Mutex` when multiple goroutines touch it.
- Always `mu.Unlock()` — forgotten unlocks cause deadlocks.

**Don't:**
- Don't expect `sync.Mutex` to lock across processes — it doesn't.

**Code:**
```go
var mu sync.Mutex

func writeDataToFile(i int, file *os.File, w *sync.WaitGroup) {
    mu.Lock()
    fmt.Fprintf(file, "From %d, writing %d\n", i, 2*i)
    w.Done()
    mu.Unlock()
}
```

*Ref: Go_Systems_Programming.md — "File locking in Go"*

---

### Spawning External Commands Safely

**Principle:** Use `exec.LookPath` to find binaries, `exec.Command` to build, and capture stdout/stderr explicitly.

**Do:**
- Set `cmd.Stdout` / `cmd.Stderr` to avoid losing output.
- Use `cmd.Run()` and check `err`.
- Use `syscall.Exec` only when you want to replace the current process image.

**Don't:**
- Don't ignore `err` from `exec.Command(...).Run()` — non-zero exit is an error.

**Code:**
```go
PS, err := exec.LookPath("ps")
if err != nil { log.Fatal(err) }
cmd := exec.Command(PS, "-a", "-x")
cmd.Stdout = os.Stdout
cmd.Stderr = os.Stderr
log.Fatal(cmd.Run())
```

*Ref: Go_Systems_Programming.md — "About Unix processes and signals", "Process management"*

---

### Signal Handling with `os/signal`

**Principle:** Go exposes OS signals via channels. `signal.Notify` registers the signals you care about.

**Do:**
- Use a buffered channel: `sigs := make(chan os.Signal, 1)`.
- Pass explicit signals: `signal.Notify(sigs, os.Interrupt, syscall.SIGTERM, syscall.SIGHUP)`.
- Run a goroutine that ranges over `sigs`.
- Make one branch call `os.Exit` so the program can be terminated cleanly.

**Don't:**
- Don't rely on `SIGHUP` killing your process — explicit `signal.Notify` lets you handle it.
- Don't `kill -9` your own process — graceful shutdown is the whole point.

**Code:**
```go
sigs := make(chan os.Signal, 1)
signal.Notify(sigs, os.Interrupt, syscall.SIGTERM, syscall.SIGHUP)

go func() {
    for {
        sig := <-sigs
        switch sig {
        case syscall.SIGTERM:
            log.Println("Got:", sig)
            os.Exit(-1)
        case os.Interrupt:
            rotateLog(filename)
        default:
            log.Println("Got:", sig)
        }
    }
}()
```

*Ref: Go_Systems_Programming.md — "Unix signals in Go", "A simple signal handler in Go"*

---

### Handling SIGHUP for Log Rotation

**Principle:** SIGHUP is the Unix convention for "reload config / rotate logs". Daemons should catch it.

**Do:**
- Use `signal.Notify(sigs, syscall.SIGHUP)` and rotate the log inside the handler.
- Combine with `time.NewTicker` for time-based rotation.

*Ref: Go_Systems_Programming.md — "Rotating log files revisited!"*

---

### `kill -l` — Listing All Signals

**Principle:** Unix signals are numbered 1..N. `kill -l` lists them all. Know which ones you can catch.

**Do:**
- Memorise: SIGTERM (15) is the polite kill; SIGKILL (9) and SIGSTOP cannot be caught.
- Reference `syscall.SIGUSR1` / `SIGUSR2` for app-defined triggers (e.g., "reload config").

**Don't:**
- Don't try to catch SIGKILL or SIGSTOP — the kernel forbids it.

*Ref: Go_Systems_Programming.md — "The kill(1) command"*

---

### Progress Reporting via SIGINFO

**Principle:** BSD/macOS define SIGINFO (Ctrl-T) for status reports. On Linux, fall back to SIGUSR1.

**Do:**
- Track `BYTESWRITTEN` and `FILESIZE` as globals.
- On SIGINFO, print `BYTESWRITTEN / FILESIZE * 100`.

**Code:**
```go
case syscall.SIGINFO:
    progress := float64(BYTESWRITTEN) / float64(FILESIZE) * 100
    fmt.Printf("Progress: %.2f%%\n", progress)
```

*Ref: Go_Systems_Programming.md — "Improving file copying"*

---

### Building a Lock Manager (Distributed)

**Principle:** A distributed lock manager needs:
1. TTL so a crashed holder can't lock forever.
2. Unique fencing token so a release only deletes its own lock.
3. Renewal heartbeat for long operations.

**Don't:**
- Don't use `SETNX` without TTL — orphans forever.
- Don't release by key only — another holder may own it.

*Ref: Go_Systems_Programming.md — "Building a distributed lock manager in Go"*

---

### Goroutines: Lightweight "Threads"

**Principle:** Goroutines are not autonomous processes — they live in OS threads, which live in processes. They are cheaper than threads, which are cheaper than processes.

**Do:**
- Create thousands of goroutines freely — Go was designed for this.
- Use `WaitGroup` to wait for them.
- Communicate via channels, not shared memory.

**Don't:**
- Don't confuse goroutines with OS threads — `GOMAXPROCS` controls the latter.

*Ref: Go_Systems_Programming.md — "About goroutines"*

---

### Concurrency vs Parallelism

**Principle:** Concurrency is a structuring technique; parallelism is simultaneous execution. Concurrent designs may or may not run in parallel.

**Do:**
- Design components to be independent and composable.
- Let the runtime/OS decide whether to parallelise.

**Don't:**
- Don't conflate "more goroutines" with "more parallelism" — often the OS scheduler sees no benefit.

*Ref: Go_Systems_Programming.md — "Concurrency and parallelism"*

---

### Creating Goroutines with `go`

**Do:**
```go
go func() {
    fmt.Println("running in goroutine")
}()
```

**Don't:**
- Don't assume goroutine completion — `main` will exit and orphan them.

*Ref: Go_Systems_Programming.md — "A simple example"*

---

### `sync.WaitGroup` Discipline

**Do:**
- `wg.Add(n)` **before** the goroutines start.
- `defer wg.Done()` inside each goroutine.
- `wg.Wait()` to block until all are done.
- Pass `*WaitGroup` as a function parameter; zero value is ready.

**Don't:**
- Don't call `Add` after `Wait` — race.
- Don't call `Add` with a count greater than the number of goroutines you actually launch — deadlock.

**Code:**
```go
var wg sync.WaitGroup
wg.Add(10)
for i := 0; i < 10; i++ {
    go func(x int) {
        defer wg.Done()
        fmt.Printf("%d ", x)
    }(i)
}
wg.Wait()
```

*Ref: Go_Systems_Programming.md — "Waiting for goroutines to finish their jobs", "Creating a dynamic number of goroutines"*

---

### Channels: Synchronisation Primitive

**Principle:** A channel is a typed conduit. Direction matters: `chan<-` is send-only, `<-chan` is receive-only.

**Do:**
- Declare direction in function signatures for compile-time safety.
- Close channels when producers are done — consumers ranging over them will exit.
- Use `chan struct{}` as a zero-cost signal channel.

**Don't:**
- Don't send on a closed channel — panic.
- Don't close a channel twice — panic.
- Don't forget to close — consumers block forever.

**Code:**
```go
func writeChannel(c chan<- int, x int) {
    c <- x
    close(c)
}

func main() {
    c := make(chan int)
    go writeChannel(c, 10)
    fmt.Println("Read:", <-c)
}
```

*Ref: Go_Systems_Programming.md — "About channels", "Writing to a channel", "Reading from a channel"*

---

### `select` — Multi-Channel Wait

**Principle:** `select` waits on multiple channel operations; `default` makes it non-blocking.

**Do:**
- Combine `select` with `time.After(d)` for timeouts.
- Use `select { case c <- x: ... default: ... }` to fail-fast on full channels.
- Always include `ctx.Done()` in production selects.

**Code:**
```go
select {
case x := <-c1:
    fmt.Println(x)
case <-time.After(1 * time.Second):
    fmt.Println("timeout")
}
```

*Ref: Go_Systems_Programming.md — "About timeouts"*

---

### Buffered Channels

**Principle:** A buffered channel (`make(chan T, N)`) holds up to `N` values without a receiver ready. Use for rate mismatch.

**Do:**
- Use when producer rate > consumer rate and you can tolerate queue depth N.
- Combine with `select { case c <- v: default: drop }` to never block.

**Don't:**
- Don't size buffers arbitrarily — measure.

*Ref: Go_Systems_Programming.md — "Buffered channels"*

---

### Pipelines: Compose Stages with Channels

**Principle:** A pipeline chains goroutines where the output of one is the input of the next.

**Do:**
- Each stage takes an input channel and returns an output channel.
- Close channels in producer order; receivers exit when range finishes.

**Code:**
```go
func genNumbers(min, max int64, out chan<- int64) {
    for i := min; i <= max; i++ { out <- i }
    close(out)
}

func findSquares(out chan<- int64, in <-chan int64) {
    for x := range in { out <- x * x }
    close(out)
}

func calcSum(in <-chan int64) {
    var sum int64
    for x := range in { sum += x }
    fmt.Println("Sum:", sum)
}

func main() {
    naturals := make(chan int64)
    squares := make(chan int64)
    go genNumbers(1, 20, naturals)
    go findSquares(squares, naturals)
    calcSum(squares)
}
```

*Ref: Go_Systems_Programming.md — "Pipelines"*

---

### Signal Channels (Empty Struct Channels)

**Principle:** `chan struct{}` carries no data — `close(c)` is the signal. Useful for "ready"/"done" broadcast.

**Code:**
```go
x := make(chan struct{})
y := make(chan struct{})
z := make(chan struct{})

go A(x, y)
go C(z)
go B(y, z)
go C(z)
close(x)
```

*Ref: Go_Systems_Programming.md — "Signal channels"*

---

### Channels of Channels

**Principle:** A `chan chan T` is a channel that itself carries channels. Useful for acknowledging or fan-out.

**Do:**
- Use for worker pools where each worker has its own reply channel.

**Don't:**
- Don't reach for this until simpler designs fail — it adds complexity fast.

*Ref: Go_Systems_Programming.md — "Channels of channels"*

---

### Nil Channels Block Forever

**Principle:** A `nil` channel always blocks. Use this to dynamically disable a `select` case.

**Code:**
```go
case <-t.C:
    c = nil // disable this case
    fmt.Println(sum)
```

*Ref: Go_Systems_Programming.md — "Nil channels"*

---

### `sync.Mutex` Discipline

**Do:**
- `Lock` / `Unlock` with `defer` inside the function that owns the lock.
- Keep critical sections tiny.

**Don't:**
- Don't forget `Unlock` — deadlock.
- Don't nest two locks on the same mutex.

**Code:**
```go
var aMutex sync.Mutex
var sharedVariable string

func addDot() {
    aMutex.Lock()
    sharedVariable += "."
    aMutex.Unlock()
}
```

*Ref: Go_Systems_Programming.md — "Using sync.Mutex"*

---

### `sync.RWMutex` — Read-Heavy State

**Principle:** Multiple readers can hold the lock simultaneously; a writer gets exclusive access.

**Do:**
- Use when reads dominate writes by 10:1 or more.
- Embed `sync.RWMutex` in the struct so methods can call `.Lock()` / `.RLock()` directly.

**Don't:**
- Don't use `RLock` for writes — readers will see partial state.

**Code:**
```go
type secret struct {
    sync.RWMutex
    counter  int
    password string
}

func Change(c *secret, pass string) {
    c.Lock()
    c.password = pass
    c.Unlock()
}

func Show(c *secret) string {
    c.RLock()
    defer c.RUnlock()
    return c.password
}
```

*Ref: Go_Systems_Programming.md — "Using sync.RWMutex"*

---

### Race Detection with `-race`

**Principle:** `go run -race` (or `go test -race`) instruments the binary to detect concurrent access to shared variables.

**Do:**
- Run `-race` in CI on every PR.
- Read the output: `WARNING: DATA RACE` lines name the read/write goroutines.

**Don't:**
- Don't ship `-race` binaries to production — they use more memory and run slower.

*Ref: Go_Systems_Programming.md — "Detecting race conditions"*

---

### `GOMAXPROCS` — Bound Parallelism

**Principle:** `GOMAXPROCS` is the number of OS threads that can run user-level Go code simultaneously.

**Do:**
- Leave it at the default (`NumCPU()` since Go 1.5).
- Set lower to reduce contention on a contended system.

**Don't:**
- Don't set higher than `NumCPU()` — won't make CPU-bound code faster.

**Code:**
```go
import "runtime"
runtime.GOMAXPROCS(runtime.NumCPU())
```

*Ref: Go_Systems_Programming.md — "About GOMAXPROCS"*

---

### Shared Memory via Monitor Goroutine

**Principle:** A monitor goroutine owns the shared state; all other goroutines send messages. This is "share by communicating".

**Do:**
```go
var (
    readValue  = make(chan int)
    writeValue = make(chan int)
)

func SetValue(newValue int) { writeValue <- newValue }
func ReadValue() int        { return <-readValue }

func monitor() {
    var value int
    for {
        select {
        case newValue := <-writeValue:
            value = newValue
        case readValue <- value:
        }
    }
}
```

**Don't:**
- Don't expose raw shared variables — always go through the monitor.

*Ref: Go_Systems_Programming.md — "Shared memory"*

---

### TCP Servers: Concurrent Per-Connection Handlers

**Principle:** Accept a connection, spawn a goroutine to handle it, write back.

**Do:**
- Set deadlines on every accepted `net.Conn`.
- Pool buffers with `sync.Pool` per handler.
- Use a `sync.WaitGroup` or `errgroup` to drain on shutdown.

**Don't:**
- Don't block `Accept` indefinitely without a shutdown path.

*Ref: Go_Systems_Programming.md — "A concurrent TCP server"*

---

### TCP Client with Timeouts

**Do:**
- `net.DialTimeout` for connection.
- `conn.SetDeadline(time.Now().Add(d))` for I/O.

**Don't:**
- Don't use `net.Dial` for anything user-facing — it can block indefinitely.

**Code:**
```go
conn, err := net.DialTimeout("tcp", "example.com:80", 5*time.Second)
if err != nil { return err }
defer conn.Close()
conn.SetDeadline(time.Now().Add(30 * time.Second))
```

*Ref: Go_Systems_Programming.md — "Developing a simple TCP client"*

---

### UDP Servers and Clients

**Principle:** UDP is connectionless; `net.ListenPacket("udp", addr)` returns a `net.PacketConn`. `ReadFrom`/`WriteTo` carry addresses per datagram.

**Do:**
- Set read/write buffer sizes with `SetReadBuffer`/`SetWriteBuffer` for high-throughput UDP.
- Validate packet sizes — UDP datagrams can be truncated.

**Don't:**
- Don't assume UDP is "free" — sending faster than the network delivers causes drops.

*Ref: Go_Systems_Programming.md — "Developing a simple UDP server"*

---

### DNS Lookups

**Do:**
- Use `net.LookupHost`, `net.LookupCNAME`, `net.LookupMX`, `net.LookupTXT`.
- `net.LookupNS` for name servers.
- Always handle the error — DNS failures are normal.

**Code:**
```go
addrs, err := net.LookupHost("example.com")
if err != nil { return err }
```

*Ref: Go_Systems_Programming.md — "Performing DNS lookups"*

---

### Unix Sockets — TCP/IP Equivalent

**Principle:** `net.Listen("unix", "/path")` is identical to TCP except the address is a filesystem path.

**Do:**
- `os.Remove` the socket file before `Listen`.
- Use `SO_PEERCRED` (`unix.SO_PEERCRED`) to verify peer credentials.

**Don't:**
- Don't put Unix sockets in `/tmp` if the host is multi-tenant.

*Ref: Go_Systems_Programming.md — "Unix sockets in Go"*

---

### RPC with `net/rpc`

**Principle:** `net/rpc` lets you call exported methods on a remote object over TCP/HTTP/Unix.

**Do:**
- Methods must be exported, take `args, reply` where `reply` is a pointer.
- Register with `rpc.Register(obj)` then `rpc.HandleHTTP()` for HTTP transport.

**Don't:**
- Don't use `gob` for cross-language RPC — use gRPC instead.

*Ref: Go_Systems_Programming.md — "RPC in Go", "An RPC server", "An RPC client"*

---

### Wireshark for Network Debugging

**Principle:** When the bytes stop flowing, capture them with `tcpdump`/`tshark` and inspect.

**Do:**
- Filter to your PID: `tcpdump -i any -w /tmp/cap.pcap -s 0 host 1.2.3.4`.
- Open in Wireshark GUI for protocol dissection.
- Use `-Y "tcp.port==8080"` to filter.

*Ref: Go_Systems_Programming.md — "About Wireshark and tshark"*

---

### `strace` / `dtruss` for Syscall Tracing

**Principle:** When a Go program misbehaves at the OS level, `strace` (Linux) and `dtruss` (macOS) show every syscall.

**Do:**
- Use `strace -e write ./myapp` to focus on a syscall family.
- Pipe through `grep` to extract the lines you care about: `strace ./app 2>&1 | grep write`.
- Build the binary first (`go build`), don't `strace go run` — the runtime noise drowns your trace.

**Don't:**
- Don't `dtruss` without disabling System Integrity Protection on macOS.

**Code:**
```bash
strace -e execve ls 2>&1 | head
```

*Ref: Go_Systems_Programming.md — "Using the strace(1) command-line utility", "The DTrace utility"*

---

### `go tool vet` for Unreachable Code

**Do:**
- Run `go tool vet ./...` — it catches unreachable code, suspicious constructs, printf format mismatches.

**Code:**
```bash
$ go tool vet cannotReach.go
cannotReach.go:9: unreachable code
```

*Ref: Go_Systems_Programming.md — "Unreachable code"*

---

### Avoiding Common Go Mistakes

- Errors: log OR return — not both, unless you have a reason.
- Interfaces define behaviour, not data.
- Use `io.Reader`/`io.Writer` for extensibility.
- Pass pointers only when needed — values by default.
- Errors are values, not strings.
- Don't test production on production.

*Ref: Go_Systems_Programming.md — "Avoiding common Go mistakes"*

---

### Unix Pipes: Reader/Writer Pair

**Principle:** A pipe is a unidirectional, OS-buffered byte stream between two processes sharing an ancestor.

**Do:**
- Use `io.Pipe` for in-process goroutine pairs.
- Use `os.Pipe` for parent/child FD passing.
- Close the write end when done — the reader gets EOF.

**Don't:**
- Don't share a pipe across unrelated processes (use FIFO or Unix socket instead).

*Ref: Go_Systems_Programming.md — "Interprocess communication"*

---

### Logging to the System Log

**Principle:** Daemons have no TTY — they must log to `syslog` or a file.

**Do:**
- Use `log/syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, "myprog")`.
- Choose a facility (LOCAL0–LOCAL7 are app-defined).
- Choose a priority (LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERR, LOG_CRIT).

**Don't:**
- Don't `log.Fatal` from a daemon — syslogd will lose the message if you exit too fast.

**Code:**
```go
sysLog, err := syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, "myprog")
if err != nil { log.Fatal(err) }
sysLog.Info("started")
```

*Ref: Go_Systems_Programming.md — "The syslog Go package"*

---

### Rotating Log Files via Signals

**Do:**
- Open with `os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)`.
- Use `log.SetOutput(file)` to redirect the standard logger.
- On SIGHUP: close, rename, reopen.

**Code:**
```go
func rotateLogFile(filename string) error {
    openLogFile.Close()
    os.Rename(filename, filename+"."+strconv.Itoa(TOTALWRITES))
    return setUpLogFile(filename)
}
```

*Ref: Go_Systems_Programming.md — "Rotating log files revisited!"*

---

### Good Random Passwords from `/dev/random`

**Principle:** `/dev/random` is the kernel CSPRNG. Read 8 bytes as an `int64` to seed `math/rand`.

**Do:**
- Use `/dev/urandom` for non-blocking reads (still cryptographically strong for most uses).
- Use `/dev/random` only when you need guaranteed entropy.

**Don't:**
- Don't seed `math/rand` with `time.Now().UnixNano()` for security — predictable.

**Code:**
```go
f, _ := os.Open("/dev/urandom")
var seed int64
binary.Read(f, binary.LittleEndian, &seed)
f.Close()
rand.Seed(seed)
```

*Ref: Go_Systems_Programming.md — "Creating good random passwords"*

---

### GC Stats via `runtime.MemStats`

**Do:**
- `runtime.ReadMemStats(&mem)` to snapshot.
- Watch `mem.NumGC` rising — more frequent = more allocation pressure.

**Code:**
```go
var mem runtime.MemStats
runtime.ReadMemStats(&mem)
fmt.Printf("alloc=%d heap=%d gc=%d\n", mem.Alloc, mem.HeapAlloc, mem.NumGC)

// GC trace
// GODEBUG=gctrace=1 ./myapp
```

*Ref: Go_Systems_Programming.md — "Garbage collection"*

---

### Detect Runtime Environment

**Code:**
```go
fmt.Println("Compiler:", runtime.Compiler)
fmt.Println("GOARCH:", runtime.GOARCH)
fmt.Println("Go version:", runtime.Version())
fmt.Println("Goroutines:", runtime.NumGoroutine())
```

*Ref: Go_Systems_Programming.md — "Your environment"*

---

### Building Packages (Pre-Go-Modules Era)

**Principle:** Pre-modules, packages live under `$GOPATH/src/` and compile with `go install`.

**Do:**
- `mkdir -p ~/go/src/myPackage && export GOPATH=~/go`.
- Capital letter = public; lowercase = package-private.
- `init()` runs automatically at package import.

**Don't:**
- Don't shadow import paths with `_` unless you need `init()` to fire.

*Ref: Go_Systems_Programming.md — "About Go packages", "Using external Go packages"*

---

### Reflection: `reflect.TypeOf` / `reflect.ValueOf`

**Do:**
- Use `reflect.ValueOf(&x).Elem()` to get a settable `Value`.
- Iterate fields with `Type.NumField()` / `Field(i)`.

**Don't:**
- Don't reflect in hot paths — it's slow.

*Code:**
```go
st := reflect.ValueOf(&x).Elem()
typeOfX := st.Type()
for i := 0; i < st.NumField(); i++ {
    fmt.Println(typeOfX.Field(i).Name, st.Field(i).Interface())
}
```

*Ref: Go_Systems_Programming.md — "Reflection"*

---

### `unsafe` — Bypass Type Safety

**Principle:** `unsafe.Pointer` lets you cast pointers between types. Use only when forced (e.g., syscall interop).

**Do:**
- Use `unsafe.Pointer(p)` to convert between unrelated pointer types.
- Document the alignment and lifetime invariants.

**Don't:**
- Don't use `unsafe` for "performance" — the compiler already optimises typed code.
- Don't dereference `unsafe.Pointer` without type assertion.

*Ref: Go_Systems_Programming.md — "Unsafe code"*

---

### Anti-Patterns & Common Mistakes

- **Race conditions buried under "it works on my box":** always run `-race`.
- **Ignoring errors from `strconv.Atoi`, `os.Open`, etc.:** silent zero values hide bugs.
- **Using `defer` in million-iteration loops:** accumulates until function returns.
- **Closing over loop variables in goroutines:** pass as parameter.
- **Using `time.After` in `select` for tickers:** use `time.NewTicker`.
- **Reading the whole file into memory:** stream.
- **Spawning unlimited goroutines:** cap with a semaphore or worker pool.
- **Using `log.Fatal` for normal errors:** kills the process.
- **Forgetting `defer ticker.Stop()`:** leaks the timer.
- **Synchronising via `os.File.Close` across processes:** use `flock(2)` or `syscall.Flock`.
- **Forgetting `O_RDWR` when writing to FIFO:** blocks forever.
- **Sending on a closed channel:** panic.
- **Forgetting to close channels:** consumers block forever.

---

## Decision Heuristics / Checklists

### Picking a CLI Argument Parser
- Few flags, no subcommands → `flag`
- Subcommands + defaults → `cobra`
- Pure config → `viper` / `envconfig`

### Picking a Synchronisation Mechanism
- One-shot init → `sync.Once`
- Counter under contention → `sync/atomic`
- Cache → `sync.Map` or sharded map
- Pipeline → channels + `select`
- Long-running worker → goroutine + `context.Context`
- Coordinating goroutines by event → `chan struct{}` + `close()`

### Picking a Network Transport
- Same host, low latency → Unix socket
- In-cluster, typed → gRPC
- Public API, simple → HTTP/JSON
- Fire-and-forget, low latency → UDP
- State, ordering, reliability → TCP

### Building a Unix Daemon
- Catch SIGTERM, SIGHUP, SIGUSR1
- Log to syslog (or a file via `log.SetOutput`)
- `os.Signal` channel for graceful shutdown
- `context.WithCancel` to cancel background goroutines
- Drain in-flight work before exit
- Profile endpoint behind auth
- Metrics endpoint (Prometheus exposition format)

---

### Unix Domain Sockets vs TCP — Pick the Right Transport

**Principle:** Unix sockets skip the network stack entirely — no TCP handshake, no kernel network buffers, just memory copies between processes. Use them when both ends are on the same host.

**Do:**
- Use for IPC between sidecar processes (e.g., log shipper + main service).
- Set `0o660` perms on the socket file.
- Always `os.Remove` before `Listen` to clean up stale sockets.

**Don't:**
- Don't use TCP for same-host sidecars — Unix sockets are 2-3× faster.

*Ref: Go_Systems_Programming.md — "About network programming", "Unix sockets revisited"*

---

### Worker Pools — Bounded Concurrency

**Principle:** Unbounded goroutine creation can OOM the host. Cap concurrent workers with a semaphore channel.

**Do:**
- Create `N := runtime.NumCPU()` workers via a buffered channel used as a semaphore.
- Feed jobs through another channel.
- Wait via `WaitGroup` and close.

**Code:**
```go
sem := make(chan struct{}, runtime.NumCPU())
jobs := make(chan Job, 100)
var wg sync.WaitGroup

for j := range jobs {
    sem <- struct{}{}        // acquire
    wg.Add(1)
    go func(j Job) {
        defer wg.Done()
        defer func() { <-sem }() // release
        process(j)
    }(j)
}
wg.Wait()
```

*Ref: Go_Systems_Programming.md — "A concurrent TCP server"*

---

### Context Cancellation Across Goroutine Boundaries

**Principle:** Every long-running goroutine should accept a `context.Context`. When the ctx is cancelled, the goroutine must exit.

**Do:**
- Pass `ctx` as the first parameter.
- `select` on `ctx.Done()` in every wait.
- Return early on `ctx.Err()`.

**Don't:**
- Don't `os.Exit` from inside a library — that's the caller's job.

**Code:**
```go
func worker(ctx context.Context, jobs <-chan Job) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case j, ok := <-jobs:
            if !ok { return nil }
            if err := process(ctx, j); err != nil { return err }
        }
    }
}
```

*Ref: Go_Systems_Programming.md — "About goroutines"*

---

### Error Wrapping with `fmt.Errorf` and `errors.Is`

**Do:**
- Wrap with context: `fmt.Errorf("open %s: %w", path, err)`.
- Check with `errors.Is(err, os.ErrNotExist)`.

**Don't:**
- Don't string-match error messages — fragile.

**Code:**
```go
f, err := os.Open(path)
if err != nil {
    return fmt.Errorf("open %s: %w", path, err)
}
```

*Ref: Go_Systems_Programming.md — "Error handling in Go"*

---

### Sentinel Errors vs Custom Error Types

**Principle:** Use sentinel errors (`io.EOF`, `os.ErrNotExist`) for "this happened", and custom types for structured data ("this happened with fields X, Y").

**Code:**
```go
// Sentinel
var ErrLockHeld = errors.New("lock held")

// Structured
type LockError struct {
    Key string
    TTL time.Duration
}
func (e *LockError) Error() string {
    return fmt.Sprintf("lock %q held for %s", e.Key, e.TTL)
}
```

*Ref: Go_Systems_Programming.md — "Functions can return error variables"*

---

### `defer` Evaluation Argument vs Body

**Principle:** `defer` evaluates arguments at the `defer` line but executes the body at the surrounding function's return.

**Do:**
- Use parameter capture for stable values: `defer func(n int) { fmt.Print(n) }(i)`.
- Use closure capture when you want the final loop value (often a bug).

**Code:**
```go
// Args evaluated at defer-line, body at return — LIFO order
func a1() {
    for i := 0; i < 3; i++ {
        defer fmt.Print(i, " ")
    }
}
// Output: "2 1 0"

// Closure captures loop variable — sees final value
func a2() {
    for i := 0; i < 3; i++ {
        defer func() { fmt.Print(i, " ") }()
    }
}
// Output: "3 3 3"
```

*Ref: Go_Systems_Programming.md — "The defer keyword"*

---

### Pointer Discipline

**Principle:** `&x` gives `*T`; `*p` reads/writes. Use pointers for mutation, large structs, and shared state.

**Do:**
- Pass `*T` to functions that modify the value.
- Return `*T` from constructors.
- Pass value types for small structs (≤ 3 words) — avoids allocation.

**Don't:**
- Don't dereference a nil pointer — `panic`.
- Don't return pointers to loop variables.

*Ref: Go_Systems_Programming.md — "Using pointer variables in functions"*

---

### `strings.Builder` for Concatenation

**Do:**
- Use `strings.Builder` (or `bytes.Buffer`) for repeated concatenation.
- Pre-grow with `Grow(n)` when you know the final size.

**Don't:**
- Don't `s := ""; for ... { s += chunk }` — O(n²).

**Code:**
```go
var b strings.Builder
b.Grow(1024)
for _, line := range lines {
    b.WriteString(line)
    b.WriteByte('\n')
}
result := b.String()
```

*Ref: Go_Systems_Programming.md — "Go data structures"*

---

### CSV Reading and Writing

**Do:**
- `csv.NewWriter` + `writer.Write(record)` + `writer.Flush()`.
- `csv.NewReader` + `reader.FieldsPerRecord = -1` to allow variable columns.
- Set `reader.FieldsPerRecord` to enforce schema.

*Ref: Go_Systems_Programming.md — "Reading and writing data records"*

---

### Logging Levels (syslog Priorities)

| Priority | Use |
|----------|-----|
| LOG_DEBUG | Verbose diagnostic |
| LOG_INFO | Normal events |
| LOG_NOTICE | Unusual but not error |
| LOG_WARNING | Recoverable anomalies |
| LOG_ERR | Errors |
| LOG_CRIT | Critical conditions |
| LOG_ALERT | Action must be taken |
| LOG_EMERG | System unusable |

**Do:**
- Use LOG_INFO for lifecycle events.
- Use LOG_WARNING for retried failures.
- Use LOG_ERR for failed operations that the caller should know about.

*Ref: Go_Systems_Programming.md — "Logging levels"*

---

### String Splitting with `strings.Fields`

**Do:**
- `strings.Fields(s)` splits on any whitespace (Unicode-aware).
- `strings.Split(s, sep)` splits on a literal separator.

**Don't:**
- Don't `strings.Split(s, " ")` for whitespace-separated fields — it breaks on runs of spaces.

*Ref: Go_Systems_Programming.md — "Printing all the values from a given column of a line"*

---

### Reading Network Connections with `bufio.Scanner`

**Do:**
- `bufio.NewScanner(conn)` with default `ScanLines` for line-based protocols.
- Increase buffer size for long lines: `scanner.Buffer(make([]byte, 1<<20), 1<<24)`.

*Ref: Go_Systems_Programming.md — "About Unix pipes in Go"*

---

### Channel Direction in Function Signatures

**Do:**
- Use `chan<-` for producers: prevents accidental reads.
- Use `<-chan` for consumers: prevents accidental sends.
- Compiler enforces.

**Don't:**
- Don't use bidirectional channels in function signatures — you lose the safety.

**Code:**
```go
func genNumbers(out chan<- int64) {
    for i := 0; i < 10; i++ {
        out <- int64(i)
    }
    close(out)
}
```

*Ref: Go_Systems_Programming.md — "About channels"*

---

### Comparing Performance: `time` and `benchstat`

**Do:**
- Run `./myapp` vs `cp(1)` with `time(1)`.
- Repeat at least 3 times — single runs lie.
- For benchmarks, use `go test -bench` and `benchstat`.

*Ref: Go_Systems_Programming.md — "Comparing the performance of wc.go and wc(1)"*

---

### `time.Time` Formatting

**Principle:** Go uses reference time `Mon Jan 2 15:04:05 MST 2006` (numeric 01/02/03/04/05/06/07) for format strings. Memorise it.

**Code:**
```go
t := time.Now()
fmt.Println(t.Format("2006-01-02 15:04:05"))    // ISO-like
fmt.Println(t.Format(time.RFC3339))             // RFC 3339
fmt.Println(t.Format(time.RFC3339Nano))         // with nanos
```

*Ref: Go_Systems_Programming.md — "Playing with dates and times"*

---

### Timezone Handling

**Do:**
- `time.LoadLocation("Europe/London")` to load by name.
- `t.In(loc)` to convert a `time.Time` to a location.
- Store everything in UTC; convert at the edge.

**Don't:**
- Don't use `time.Local` in stored data — ambiguous across machines.

*Ref: Go_Systems_Programming.md — "Playing with dates and times"*

---

### Parsing Log Lines with Regex

**Do:**
- Compile regexes once, outside hot loops.
- Use named captures for clarity: `(?P<host>\S+)`.
- Test with the actual log format — they're never as regular as you hope.

**Don't:**
- Don't try to validate IP ranges in regex alone — pair with `net.ParseIP`.

*Ref: Go_Systems_Programming.md — "An advanced example of pattern matching"*

---

### `crypto/rand` for Security-Sensitive Values

**Do:**
- Use `crypto/rand.Read(buf)` for cryptographic randomness.
- Use `math/rand` only for simulations and tests.

**Don't:**
- Don't seed `math/rand` with `time.Now()` for anything security-related.

**Code:**
```go
buf := make([]byte, 32)
if _, err := rand.Read(buf); err != nil {
    log.Fatal(err)
}
```

*Ref: Go_Systems_Programming.md — "Creating good random passwords"*

---

### Finding User/Group Info with `os/user`

**Do:**
- `user.Current()` for the running user.
- `user.Lookup("username")` to look up by name.
- `user.LookupGroupId(gid)` for group details.

*Ref: Go_Systems_Programming.md — "Finding the user ID of a user", "Finding all the groups a user belongs to"*

---

### Cross-Platform Note: `syscall.Stat_t`

**Principle:** `fileInfo.Sys().(*syscall.Stat_t)` returns platform-specific metadata. The `Uid`/`Gid` fields exist on both macOS and Linux but with different layouts.

**Don't:**
- Don't rely on `Sys()` in portable code — it's `any` for a reason.

*Ref: Go_Systems_Programming.md — "Finding other kinds of information about files"*

---

### `os/exec` for Replacing Self (syscall.Exec)

**Do:**
- Use `syscall.Exec(path, args, env)` to replace the current process image.
- `os.Environ()` gives you the current env.

**Don't:**
- Don't use `os.Exec` — it doesn't exist. It's `syscall.Exec`.

*Ref: Go_Systems_Programming.md — "Process management"*

---

### `log/syslog` Writer as `io.Writer`

**Principle:** `syslog.New(...)` returns a `*Writer` that satisfies `io.Writer`. Pass it anywhere you'd pass `os.Stdout`.

**Code:**
```go
sysLog, _ := syslog.New(syslog.LOG_INFO|syslog.LOG_LOCAL7, "myprog")
fmt.Fprintf(sysLog, "log.Print: Logging in Go!")
```

*Ref: Go_Systems_Programming.md — "The syslog Go package"*

---

### Worker Drainage Pattern

**Do:**
```go
func worker(jobs <-chan int, results chan<- int, done chan<- struct{}) {
    for j := range jobs {
        results <- process(j)
    }
    done <- struct{}{}
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    done := make(chan struct{}, 10)

    for w := 0; w < 10; w++ {
        go worker(jobs, results, done)
    }
    // ... feed jobs ...
    close(jobs)

    for w := 0; w < 10; w++ {
        <-done
    }
    close(results)
}
```

*Ref: Go_Systems_Programming.md — "About goroutines", "Pipelines"*

---

### Concurrent TCP Server with Worker Pool

**Do:**
- Accept in main loop, hand off to a worker goroutine.
- Use a semaphore (buffered channel) to bound workers.
- Close connections with `defer conn.Close()`.

*Ref: Go_Systems_Programming.md — "A concurrent TCP server"*

---

### TCP/UDP Choice in Practice

| Need | Use |
|------|-----|
| Reliable byte stream | TCP |
| Request-response, low overhead | TCP (or Unix socket) |
| Voice/video, custom retransmit | UDP |
| Service discovery, telemetry | UDP |
| File transfer | TCP |

*Ref: Go_Systems_Programming.md — "About TCP/IP", "About UDP and IP"*

---

### `wireshark` Filters for Common Issues

- `tcp.port==8080`: only traffic on port 8080
- `http.request.method==POST`: only POST requests
- `ip.addr==10.0.0.5`: traffic involving a specific IP
- `tcp.analysis.retransmission`: dropped/retransmitted packets

*Ref: Go_Systems_Programming.md — "About Wireshark and tshark"*

---

### Anti-Patterns & Common Mistakes (additions)

- **Spawning a goroutine without a termination path:** leaks on shutdown.
- **Mixing `log.Printf` and `fmt.Println`:** inconsistent log format breaks parsers.
- **Reading the entire stdin into memory:** blocks on interactive input.
- **Calling `os.Exit` from a library:** violates caller expectations.
- **Forgetting to `Close()` HTTP response bodies:** connection pool exhaustion.
- **Building your own UUID generator:** use `github.com/google/uuid`.
- **Using `path` instead of `path/filepath`:** breaks on Windows.
- **Storing the connection in a global:** makes testing and lifecycle impossible.

---

---

## Cross-References
- Related: [[../System_Programming_Essentials_with_Go.md]]
- Related: [[../Efficient_Go.md]]
- Topic index: [[../INDEX.md]]
