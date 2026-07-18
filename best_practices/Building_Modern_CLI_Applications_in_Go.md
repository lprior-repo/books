# Building Modern CLI Applications in Go
**Author:** Marian Montagnino (Senior Software Engineer, Netflix)
**Topic tags:** `#cli` `#systems` `#go` `#cross-platform` `#testing` `#distribution` `#ux`
**Language focus:** Go-first
**Sources:** `markdown_output/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino.md` · `summaries/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino.md`

## TL;DR
The definitive modern-Go CLI playbook. Grounded in UNIX philosophy and empathy-driven design, it walks through project structure, the Cobra+Viper stack, input/process/output handling, external processes and HTTP, cross-platform build tags, TTY-aware output, error decoration, testing strategies, container distribution, and GoReleaser+Homebrew release automation. Treat this as the canonical checklist when starting or hardening any Go CLI.

---

## Best Practices by Topic

### Unix Philosophy & Modern CLI Guidelines  `#cli`

**Principle:** Build small, composable, modular programs designed for humans first; provide composable text/JSON output and fail noisily.

**Do:**
- Build modular programs that compose via pipes, standard I/O, standardized exit codes, and signals.
- Design for humans first (conversation, prompts, suggestions); fall back to machine-readable output via flags.
- Keep it simple — fold complexity into data, not logic; reuse existing patterns.
- Be transparent: comprehensive help text and examples in-product so users never need Stack Overflow.
- Be robust: work as expected; on error, explain clearly with a suggested next step.
- Be succinct: no unnecessary output, but never silent.
- Fail noisily and early — prevent incorrect output corrupting downstream programs.
- Prototype first, then optimize. Save developer time over machine time.
- Be a good CLI citizen — reuse `ls`, `cp`, `rm`, `cat`; consistent casing; lowercase names; dashes only when needed.

**Don't:**
- Hardcode intelligence and assume user ignorance (the "Windows" model).
- Use ambiguous subcommand names (e.g. `update` vs `upgrade`).
- Change human-readable output without warning; never break machine-readable output silently.
- Print full stack traces to a human without context.

*Ref: Building_Modern_CLI_Applications_in_Go.md — "The philosophy of CLI development" / "Checklist for a successful CLI" / "The guidelines"*

---

### Command Structure, Subcommands & Project Layout  `#cli` `#architecture`

**Principle:** Follow `APPNAME NOUN VERB --ADJECTIVE` (noun-verb preferred). Pick a folder structure intentionally — start flat, evolve to modular/hexagonal only when justified.

**Do:**
- Use consistent ordering (noun-verb or verb-noun); keep subcommands unambiguous.
- Use standard folder names: `cmd/` (entry), `internal/` (private), `pkg/` (public), `api/`, `configs/`, `scripts/`, `build/`, `deployments/`, `test/`, `vendor/`.
- Avoid generic package names (`util`, `common`, `script`); lowercase, no snake_case/camelCase in package names.
- Document use cases (functional) and requirements (non-functional: security, capacity, compatibility, reliability, maintainability, scalability, usability, performance, environment) before coding.
- For domain-heavy CLIs, adopt hexagonal architecture (ports = interfaces, adapters = implementations; outer layers may call inner layers only).

**Don't:**
- Choose a structure arbitrarily or too early; don't write a big monolithic program unless unavoidable.
- Allow circular dependencies in "group by module" layouts.

**Code** — define a `Command` interface so every subcommand is uniform and testable:
```go
type Command interface {
    ParseFlags([]string) error
    Run() error
    Name() string
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Defining the components" / "Grouping by context"*

**Code** — a parser that dispatches on the first arg and falls back to help:
```go
func (p *Parser) Parse(args []string) error {
    if len(args) < 1 {
        help()
        return nil
    }
    subcommand := args[0]
    for _, cmd := range p.commands {
        if cmd.Name() == subcommand {
            cmd.ParseFlags(args[1:])
            return cmd.Run()
        }
    }
    return fmt.Errorf("Unknown subcommand: %s", subcommand)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/cli/command"*

---

### Flag Parsing (stdlib `flag`, `pflag`, Cobra)  `#cli`

**Principle:** Prefer flags over positional arguments — they're easier to add/remove without breaking behavior. Always provide a long form; reserve short forms for commonly used flags.

**Do:**
- Provide full-length (`--help`) for every flag; only short form (`-h`) for common ones.
- Use standard flag names: `-a/--all`, `-d/--debug`, `-f/--force`, `--json`, `-h/--help`, `--no-input`, `-o/--output`, `-p/--port`, `-q/--quiet`, `-u/--user`, `--version`, `-v` (version or verbose).
- Use `PersistentFlags()` for flags inherited by subcommands; `Flags()` for local-only.
- Mark required flags via `MarkPersistentFlagRequired("filename")` / `MarkFlagRequired(...)`.
- Validate input early and fail fast with clear feedback.

**Don't:**
- Use single-letter flags for everything (collisions, ambiguity).
- Mix `update`/`upgrade`-style ambiguities.

**Code** — `flag` package basics with default port:
```go
var port int
flag.IntVar(&port, "p", 8000, "Port for metadata service")
flag.Parse()
fmt.Printf("Starting API at http://localhost:%d\n", port)
metadataService.Run(port)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/api/"*

**Code** — a command's flagset with `ContinueOnError`:
```go
gc := &RandomCommand{
    fs:    flag.NewFlagSet("random", flag.ContinueOnError),
    client: client,
}
gc.fs.StringVar(&gc.flag, "flag", "", "string flag for random command")
```
> `flag.ErrorHandling` options: `ContinueOnError`, `ExitOnError`, `PanicOnError`.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Implementing use cases"*

**Code** — Cobra persistent (global) and required flag:
```go
uploadCmd.PersistentFlags().StringVarP(&Filename, "filename", "f", "", "file to upload")
uploadCmd.MarkPersistentFlagRequired("filename")
rootCmd.AddCommand(uploadCmd)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Global, local, and required flags"*

**Code** — typed pflag and custom `Value` interface:
```go
var intValue int
flag.IntVar(&intValue, "flagName", 123, "help message")

// Custom flag type must satisfy:
type Value interface {
    String() string
    Set(string) error
    Type() string
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Processing data"*

---

### Cobra & Viper — the Standard Stack  `#cli` `#configuration`

**Principle:** Use Cobra for command/flag/help/autocomplete scaffolding and Viper for layered config (file → env → flag → buffer → remote). They eliminate thousands of lines of boilerplate.

**Do:**
- Scaffold with `go mod init`, then `cobra-cli init`, then `cobra-cli add <cmd>`.
- Generate help from `Use`, `Short`, `Long`, `Example`.
- Generate man pages via `github.com/spf13/cobra/doc`.
- Use Viper to support JSON/TOML/YAML/HCL/INI/envfile/properties, env vars (`SetEnvPrefix`+`BindEnv`+`AutomaticEnv`), pflag binding (`BindPFlags`), buffers, and remote providers (Consul/etcd).
- Watch live config changes via `WatchConfig()` + `OnConfigChange(...)`.
- Use `RunE` (not `Run`) when the command can fail so Cobra handles error printing.

**Don't:**
- Hand-roll a parser when Cobra covers your needs.
- Store secrets in env vars or flags — use `--password-file`.

**Code** — a Cobra command with `RunE`, `Use`, `Short`, `Long`, `Example`:
```go
var uploadCmd = &cobra.Command{
    Use:   "upload [audio|video] [-f|--filename] <filename>",
    Short: "upload an audio or video file",
    Long: `This command allows you to upload either an audio or video file for metadata extraction.
To pass in a filename, use the -f or --filename flag followed by the path of the file.
Examples:
./audiofile-cli upload audio -f audio/beatdoctor.mp3`,
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating subcommands"*

**Code** — Viper file + env config:
```go
viper.SetConfigName("config")           // name without extension
viper.AddConfigPath(".")                // search paths
if err := viper.ReadInConfig(); err != nil {
    panic(fmt.Errorf("err: %w \n", err))
}
fmt.Println("prod environment url:", viper.Get("environments.prod.url"))

viper.SetEnvPrefix("AUDIOFILE")
viper.BindEnv("TEST_URL")
os.Setenv("AUDIOFILE_TEST_URL", "89.45.23.123")
fmt.Println(viper.Get("TEST_URL"))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Config file" / "Environment variable"*

**Code** — Viper defaults, env binding, and typed getters:
```go
viper.SetDefault("host", "localhost")
viper.SetDefault("port", 1234)
viper.BindEnv("host", "AUDIOFILE_HOST")
viper.BindEnv("port", "AUDIOFILE_PORT")
// then:
port := viper.GetInt("port")
host := viper.GetString("host")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Flags"*

**Code** — watching live config changes (local and remote):
```go
viper.OnConfigChange(func(event fsnotify.Event) {
    fmt.Println("Config modified:", event)
})
viper.WatchConfig()

// remote (Consul/etcd):
remoteConfig := viper.New()
remoteConfig.AddRemoteProvider("consul", "http://127.0.0.1:2380", "/config/audiofile-cli.json")
remoteConfig.SetConfigType("json")
remoteConfig.ReadRemoteConfig()
go func() {
    for {
        time.Sleep(time.Second * 1)
        _ = remoteConfig.WatchRemoteConfig()
        remoteConfig.Unmarshal(&remote_conf)
    }
}()
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Watching for live config changes"*

---

### Input: stdin, Piping, Signals, Prompts  `#cli` `#systems`

**Principle:** Beyond flags/args, CLIs receive input from stdin (pipes), signals/control chars, and interactive prompts. Handle all paths.

**Do:**
- Support piping via `bufio.NewReader(os.Stdin)`.
- Handle `SIGINT`/`SIGTSTP`/`SIGQUIT`/`SIGHUP` for graceful shutdown using `os/signal` and channels.
- Use `survey` (or similar) for prompts: `Input`, `Select`, `MultiSelect`, `Multiline`, `Password`, `Confirm`.
- Mask passwords (`survey.Password`).
- Confirm destructive ops with difficulty scaling to danger (mild/moderate/severe → typed confirm or `--confirm="name"`).
- Print something within 100 ms; notify before network calls so the app never looks hung.

**Don't:**
- Use `survey`/interactive prompts when stdin is not a TTY.
- Block forever — pair long ops with timeouts/cancellation.

**Code** — reading from a pipe:
```go
reader := bufio.NewReader(os.Stdin)
s, _ := reader.ReadString('\n')
fmt.Printf("piped in: %s\n", s)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Piping"*

**Code** — graceful SIGINT/SIGTSTP handlers:
```go
func SetupInterruptHandler() {
    c := make(chan os.Signal, 1)
    signal.Notify(c, os.Interrupt, syscall.SIGINT)
    go func() {
        <-c
        fmt.Println("\r- Wake up! Sleep has been interrupted.")
        os.Exit(0)
    }()
}
// same shape for SetupStopHandler with syscall.SIGTSTP
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Signals and control characters"*

**Code** — interactive prompt with suggestions and validation:
```go
prompt := &survey.Input{
    Message: "What is the filename of the audio to upload for metadata extraction?",
    Suggest: func(toComplete string) []string {
        files, _ := filepath.Glob(toComplete + "*")
        return files
    },
}
survey.AskOne(prompt, &file)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example 1: Prompt for information when a flag is missing"*

**Code** — confirmation for destructive actions:
```go
func Confirm(confirmationText string) bool {
    confirmed := false
    prompt := &survey.Confirm{Message: confirmationText}
    survey.AskOne(prompt, &confirmed)
    return confirmed
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example 2: Confirm deletion"*

| Signal (Key)         | Description                                            |
|----------------------|-------------------------------------------------------|
| SIGINT (Ctrl-C)      | Interrupt application                                 |
| SIGTSTP (Ctrl-Z)     | Suspend application                                   |
| SIGQUIT (Ctrl-\\)     | Quit application                                      |
| SIGHUP               | Hangup on controlling terminal                        |
| SIGFPE               | Illegal math operation                                |
| SIGKILL              | Quit immediately, no cleanup                          |
| SIGALRM              | Alarm clock signal (timers)                           |
| SIGTERM              | Software termination (kill default)                   |

*Ref: Building_Modern_CLI_Applications_in_Go.md — "Signals and control characters"*

---

### Data Processing & File Reading Strategies  `#cli` `#systems`

**Principle:** Pick a reading strategy matched to your data shape; prefer streaming/chunked reads to bound memory.

**Do:**
- `os.ReadFile` — entire file at once (fast, but high memory).
- `file.Read(buf)` — predefined chunks (low memory, watch for EOF).
- `bufio.Scanner` default — line-by-line.
- `bufio.Scanner` with `scanner.Split(bufio.ScanWords)` — word-by-word.
- Use typed flags (`pflag.Int`, `Bool`, custom `Value`) to avoid manual `strconv` round-trips.

**Don't:**
- Read whole multi-GB files into memory for line-oriented processing.

**Code** — all four strategies side-by-side:
```go
// all at once
content, err := os.ReadFile(filename)

// chunked
const size = 8
buff := make([]byte, size)
for {
    n, err := file.Read(buff)
    if err != nil { if err != io.EOF { fmt.Println(err) }; break }
    fmt.Println(string(buff[:n]))
}

// line by line
scanner := bufio.NewScanner(file)
for scanner.Scan() { fmt.Println(scanner.Text()) }

// word by word
scanner := bufio.NewScanner(file)
scanner.Split(bufio.ScanWords)
for scanner.Scan() { fmt.Println(scanner.Text()) }
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Processing data"*

---

### Calling External Processes (`os/exec`)  `#cli` `#systems`

**Principle:** `os/exec` is the cross-platform wrapper over `os.StartProcess`. Use `exec.Command`/`exec.CommandContext` (context-aware), and choose `Run`, `Start`+`Wait`, `Output`, or `CombinedOutput` based on what you need back.

**Do:**
- Use `exec.CommandContext(ctx, name, args...)` for cancellable commands.
- Always call `cmd.Wait()` after `cmd.Start()` to release resources.
- Capture stderr into a `bytes.Buffer` when you need error detail.
- Use `StdoutPipe`/`StderrPipe`/`StdinPipe` for streaming; never use these with `Run` (which already waits).
- On Windows, use `exec.Command("cmd", "/C", ...)`; remember `ExtraFiles` is unsupported on Windows.

**Don't:**
- Reuse a `Cmd` after `Run`/`Output`/`CombinedOutput` — it cannot be reused.
- Use `os/exec` to expand globs or pipes — it doesn't invoke the shell. Use `filepath.Glob` or shell out explicitly with proper escaping.

**Cmd struct key fields:** `Path` (required), `Args`, `Env` (`"key=value"`), `Dir`, `Stdin` (`io.Reader`), `Stdout`/`Stderr` (`io.Writer`), `ExtraFiles` (fd 3+x, not Windows), `SysProcAttr`, `Process`, `ProcessState`.

**Code** — `Cmd` struct with `ExtraFiles` pipe:
```go
cmd := exec.Cmd{}
cmd.Path = filepath.Join(os.Getenv("GOPATH"), "bin", "uppercase")
cmd.Args = []string{"uppercase", "hack the planet"}
cmd.Stdin = os.Stdin
cmd.Stdout = os.Stdout
cmd.Stderr = os.Stderr

reader, writer, err := os.Pipe()
if err != nil { panic(err) }
cmd.ExtraFiles = []*os.File{writer}
if err := cmd.Start(); err != nil { panic(err) }

var data string
if err := json.NewDecoder(reader).Decode(&data); err != nil { panic(err) }
fmt.Println(data)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Using the Cmd struct"*

**Code** — capturing stdout and stderr separately on error:
```go
cmd := exec.Command(filepath.Join(os.Getenv("GOPATH"), "bin", "error"))
var out bytes.Buffer
var stderr bytes.Buffer
cmd.Stdout = &out
cmd.Stderr = &stderr
if err := cmd.Run(); err != nil {
    fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
    return
}
fmt.Println(out.String())
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Handling other errors"*

**Code** — running external commands on Windows (no `ExtraFiles`):
```go
func CreateCommandUsingCommandFunction() {
    cmd := exec.Command("cmd", "/C", "ping", "google.com")
    output, err := cmd.CombinedOutput()
    if err != nil { panic(err) }
    fmt.Println(string(output))
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Executing commands on Windows"*

---

### REST API Interaction (`net/http`)  `#cli` `#api`

**Principle:** Use `http.NewRequest`+`client.Do` for full control, or convenience `http.Get`/`http.Post`/`http.PostForm` for simple cases. Always set a client `Timeout` and check both the Go error and `resp.StatusCode`.

**Do:**
- Always set `http.Client{Timeout: ...}`.
- Check `resp.StatusCode` explicitly — non-2xx is **not** a Go error.
- Unmarshal `application/json` bodies into typed structs; use `http.DetectContentType(b)` when the content type is unknown.
- URL-encode user-supplied query params (`url.QueryEscape`).
- Support pagination with `limit`/`page` (or cursor) params.
- Rate-limit outbound calls with `golang.org/x/time/rate` (handles burst + limit; preferred over `time.Sleep`).
- Close `resp.Body` (always, usually via `defer`).

**Don't:**
- Assume 4xx/5xx populates the Go error — it doesn't.
- Hit public APIs without rate limiting.

**Code** — full GET request with query escape:
```go
params := "id=" + url.QueryEscape(cmd.id)
path := fmt.Sprintf("http://localhost/request?%s", params)
req, err := http.NewRequest("GET", path, &bytes.Buffer{})
if err != nil { return err }
resp, err := client.Do(req)
if err != nil { return err }
defer resp.Body.Close()
b, err := io.ReadAll(resp.Body)
if err != nil { return err }
fmt.Println(string(b))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Requesting metadata"*

**Code** — multipart file upload via POST:
```go
payload := &bytes.Buffer{}
multipartWriter := multipart.NewWriter(payload)
file, err := os.Open(cmd.filename)
if err != nil { return err }
defer file.Close()
partWriter, err := multipartWriter.CreateFormFile("file", filepath.Base(cmd.filename))
if err != nil { return err }
io.Copy(partWriter, file)
multipartWriter.Close()

req, _ := http.NewRequest("POST", "http://localhost/upload", payload)
req.Header.Set("Content-Type", multipartWriter.FormDataContentType())
res, err := client.Do(req)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Uploading audio"*

**Code** — rate limiter with `x/time/rate`:
```go
type runner struct {
    Run     func() bool
    limiter *rate.Limiter
}

thing := runner{}
thing.limiter = rate.NewLimiter(rate.Every(5*time.Second), 1) // 1 event / 5s, burst 1
thing.Run = func() bool {
    if thing.limiter.Allow() {
        fmt.Println(time.Now()) // or do request
        return false
    }
    if time.Since(start) > 30*time.Second { return true }
    return false
}
for { if thing.Run() { break } }
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Rate limiting"*

---

### Timeouts, Errors & Panics  `#cli` `#systems` `#error-handling`

**Principle:** Expect the unexpected on every external call — wrap with `select`+`time.After` for processes, set HTTP client timeouts, and recover panics at command boundaries.

**Do:**
- For long external commands, run `cmd.Wait()` in a goroutine and race it against `time.After` via `select`.
- Type-assert HTTP errors to `*url.Error` and call `.Timeout()` / `.Temporary()`.
- Switch on `resp.StatusCode` for actionable handling (`StatusBadRequest`, `StatusInternalServerError`, `StatusNotFound`, …).
- Use `errors.Is(err, exec.ErrDot)` / `errors.Is(err, exec.ErrNotFound)` (not `==`) to walk the error chain.
- For panics in your own command code: `defer` + `recover()` → print to stderr, `debug.PrintStack()`, exit non-zero.

**Don't:**
- Compare errors with `==` (loses wrapping context).
- Print stack traces to users without an empathetic overlay.

**Code** — external command timeout with `select`:
```go
func Timeout() {
    errChan := make(chan error, 1)
    cmd := exec.Command(filepath.Join(os.Getenv("GOPATH"), "bin", "timeout"))
    if err := cmd.Start(); err != nil { panic(err) }
    go func() { errChan <- cmd.Wait() }()
    select {
    case <-time.After(time.Second * 10):
        fmt.Println("timeout command timed out")
        return
    case err := <-errChan:
        if err != nil { fmt.Println("timeout error:", err) }
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Timeouts with external command processes"*

**Code** — HTTP timeout and `*url.Error` type-assertion:
```go
client := http.Client{ Timeout: 1 * time.Second }
req, err := http.NewRequest(http.MethodGet, "http://localhost:8080/timeout", &bytes.Buffer{})
if err != nil { panic(err) }
resp, err := client.Do(req)
if err != nil {
    urlErr := err.(*url.Error)
    if urlErr.Timeout() {
        fmt.Println("timeout: ", err)
        return
    }
}
defer resp.Body.Close()
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "HTTPTimeout"*

**Code** — switching on `resp.StatusCode`:
```go
if resp.StatusCode != http.StatusOK {
    switch resp.StatusCode {
    case http.StatusBadRequest:
        fmt.Printf("bad request: %v\n", resp.Status)
    case http.StatusInternalServerError:
        fmt.Printf("internal service error: %v\n", resp.Status)
    default:
        fmt.Printf("unexpected status code: %v\n", resp.StatusCode)
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "HTTPErrors"*

**Code** — recover from panic:
```go
defer func() {
    if panicMessage := recover(); panicMessage != nil {
        fmt.Fprintf(os.Stderr, "(panic) : %v\n", panicMessage)
        debug.PrintStack()
        os.Exit(1)
    }
}()
panic("help!")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Errors or panics with external command processes"*

**Code** — `errors.Is` for exec errors:
```go
cmd := exec.Command("doesnotexist", "arg1")
if errors.Is(cmd.Err, exec.ErrDot) {
    fmt.Println("path lookup resolved to a local directory")
}
if err := cmd.Run(); err != nil {
    if errors.Is(err, exec.ErrNotFound) {
        fmt.Println("executable failed to resolve")
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Handling errors when a command's path cannot be found"*

---

### TTY Detection & Human-vs-Machine Output  `#cli` `#ux`

**Principle:** Check whether stdout is a TTY; render colors, tables, spinners, emojis only for humans; emit one-record-per-line text/JSON for machines.

**Do:**
- Detect TTY cross-platform via `github.com/mattn/go-isatty` (`isatty.IsTerminal(os.Stdout.Fd()) || isatty.IsCygwinTerminal(...)`), or via `os.Stdout.Stat()` + `os.ModeCharDevice` on Unix.
- Provide `--plain`, `--json`, `--quiet`/`--silent` flags for machine consumption.
- Use `less` on Unix / `more` on Windows for paging long output (build-tag split).
- Display on success; communicate state changes; suggest next commands.
- Use color intentionally (red errors, green success); disable when piped, `NO_COLOR` set, `TERM=dumb`, or `--no-color`.
- Use spinners/progress bars only when outputting to a TTY.

**Don't:**
- Send ANSI colors or animations through a pipe.
- Be silent on success.

**Code** — Unix TTY check via file mode:
```go
if fileInfo, _ := os.Stdout.Stat(); (fileInfo.Mode() & os.ModeCharDevice) != 0 {
    fmt.Println("terminal")
} else {
    fmt.Println("not a terminal")
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Programmatically check on a Unix or Linux operating system"*

**Code** — cross-platform TTY check:
```go
if isatty.IsTerminal(os.Stdout.Fd()) || isatty.IsCygwinTerminal(os.Stdout.Fd()) {
    fmt.Println("Is a TTY")
} else {
    fmt.Println("Is not a TTY")
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Programmatically check on any operating system"*

**Code** — `pterm` table rendering with header:
```go
var header = []string{"ID", "Path", "Status", "Title", "Album", /* ... */}

func row(audio Audio) []string {
    return []string{
        audio.Id, audio.Path, audio.Status,
        audio.Metadata.Tags.Title, audio.Metadata.Tags.Album,
        /* ... */
        strconv.Itoa(audio.Metadata.Tags.Year),
        strings.Replace(audio.Metadata.Tags.Comment, "\r\n", "", -1),
    }
}

func (list *AudioList) Table() (string, error) {
    data := pterm.TableData{header}
    for _, audio := range *list { data = append(data, row(audio)) }
    return pterm.DefaultTable.WithHasHeader().WithData(data).Srender()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Displaying information with tables"*

**Code** — pagination (`less -r` on Unix, build-tagged):
```go
//go:build !windows
func Pager(data string) error {
    lessCmd := exec.Command("less", "-r")
    lessCmd.Stdin = strings.NewReader(data)
    lessCmd.Stdout = os.Stdout
    lessCmd.Stderr = os.Stderr
    return lessCmd.Run()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Pagination for Unix or Linux"*

---

### Visual Language: Color, Emoji, Spinners, Progress Bars  `#cli` `#ux`

**Principle:** Increase information density without clutter. Use color sparingly and intentionally.

**Do:**
- Green for success, red for errors (e.g. `fatih/color` with `Fg`/`Bg` prefixes).
- Emojis via UTF-8 codes: green checkmark `"\U00002705"`, red X `"\U0000274C"`.
- Spinners (`pterm.DefaultSpinner`) and progress bars (`pterm.DefaultProgressbar`) for long ops — only when TTY.
- Use `pterm` progress bar with `WithTotal(n)`, `Increment()`, `UpdateTitle(...)`.

**Don't:**
- Use multiple colors everywhere — nothing will stand out.

**Code** — emoji constants:
```go
const (
    checkMark = "\U00002705"
    crossMark = "\U0000274C"
)
fmt.Println(checkMark, " Successfully uploaded!")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Clarifying with emojis"*

**Code** — color helpers:
```go
var IdColor = color.New(color.FgGreen).SprintFunc()
// in row(): IdColor(audio.Id)

var errorColor = color.New(color.BgRed, color.FgWhite).SprintFunc()
return fmt.Errorf(errorColor(fmt.Sprintf("missing required argument (%s)", missingArg)))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Using color with intention"*

**Code** — spinner gated on TTY:
```go
spinnerInfo := &pterm.SpinnerPrinter{}
if utils.IsaTTY() {
    spinnerInfo, _ = pterm.DefaultSpinner.Start("Enjoy the music...")
}
err := cmd.Wait()
// ...
if utils.IsaTTY() { spinnerInfo.Stop() }
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example 1 – Spinner while playing music"*

**Code** — progress bar:
```go
p, _ := pterm.DefaultProgressbar.WithTotal(4).WithTitle("Initiating upload...").Start()
pterm.Success.Println("Created multipart writer")
p.Increment()
p.UpdateTitle("Sending request...")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example 2 – Progress bar when uploading a file"*

---

### Error Decoration, Rewriting & Logging  `#cli` `#error-handling` `#observability`

**Principle:** Errors are a primary UX surface. Decorate with context, rewrite for humans, and add structured logging for debug/verbose mode.

**Do:**
- Be specific about what failed and how to fix it; don't blame the user.
- Wrap errors: `fmt.Errorf("...: %w", err)` or `pkg/errors` `Wrap`/`Wrapf` for stack traces.
- Custom errors implementing `Error() string` can carry `Task`, severity, kind, etc.
- Rewrite HTTP status codes into actionable messages (`StatusNotFound` → "the id cannot be found").
- Use **Zap** (or zerolog) over logrus (now in maintenance) for performance and active development.
- Define two loggers: one to file, one to stdout for `--verbose`/`-v`.
- Provide a `bug` command that opens the GitHub issue page with a pre-filled template including the CLI version.
- Generate help text from Cobra fields; generate man pages via `cobra/doc.GenManTree`.

**Don't:**
- Print full raw stack traces to a non-verbose user.
- Use `stderr` as a log file (debug/warning should go to stdout).
- Choose unmaintained loggers when an active alternative exists.

**Code** — wrapping with stack traces:
```go
err1 := errors.Wrap(err, "operation1")
err2 := errors.Wrap(err1, "operation2")
err3 := errors.Wrap(err2, "operation3")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Decorating errors"*

**Code** — custom error type with color and emoji:
```go
type customError struct {
    Task string
    Err  error
}

func (e *customError) Error() string {
    var errorColor = color.New(color.BgRed, color.FgWhite).SprintFunc()
    return fmt.Sprintf("%s: %s %s", errorColor(e.Task), crossMark, e.Err)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Customizing errors"*

**Code** — `CheckResponse` rewriting HTTP codes:
```go
func CheckResponse(resp *http.Response) error {
    if resp != nil {
        if resp.StatusCode != http.StatusOK {
            switch resp.StatusCode {
            case http.StatusInternalServerError:
                return fmt.Errorf(errorColor("retry the command later"))
            case http.StatusNotFound:
                return fmt.Errorf(errorColor("the id cannot be found"))
            default:
                return fmt.Errorf(errorColor(fmt.Sprintf("unexpected response: %v", resp.Status)))
            }
        }
        return nil
    }
    return fmt.Errorf(errorColor("response body is nil"))
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Writing better error messages"*

**Code** — Zap logger init driven by Viper config:
```go
func InitCLILogger() {
    var cfg zap.Config
    config := viper.GetStringMap("cli.logging")
    configBytes, _ := json.Marshal(config)
    json.Unmarshal(configBytes, &cfg)
    cfg.EncoderConfig = encoderConfig()
    createFilesIfNotExists(cfg.OutputPaths)
    cfg.Encoding = "json"
    cfg.Level = zap.NewAtomicLevel()
    Logger, _ = cfg.Build()
    cfg.OutputPaths = append(cfg.OutputPaths, "stdout")
    Verbose, _ = cfg.Build()
    defer Logger.Sync()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Initiating a logger"*

**Code** — reusable error helper that respects verbose:
```go
func Error(errString string, err error, verbose bool) error {
    errString = cleanup(errString, err)
    if err != nil {
        if verbose {
            Verbose.Error(errString) // also prints to stdout
        } else {
            Logger.Error(errString)
        }
        return fmt.Errorf(errString)
    }
    return nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Implementing a logger"*

**Code** — `bug` command opening a browser to a pre-filled issue:
```go
var buf bytes.Buffer
buf.WriteString(fmt.Sprintf("**Audiofile version**\n%s\n\n", utils.Version()))
buf.WriteString(description)
buf.WriteString(toReproduce)
buf.WriteString(expectedBehavior)
buf.WriteString(additionalDetails)
body := buf.String()
url := "https://github.com/marianina8/audiofile/issues/new?title=Bug Report&body=" + url.QueryEscape(body)
if !openBrowser(url) {
    fmt.Print("Please file a new issue at ... using this template:\n\n")
    fmt.Print(body)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Effortless bug submission"*

**Code** — generating man pages:
```go
header := &doc.GenManHeader{
    Title:  "Audiofile",
    Source: "Auto generated by marianina8",
}
doc.GenManTree(cmd.RootCMD(), header, "./pages")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Generating man pages"*

---

### Empathy-Driven Documentation  `#cli` `#ux`

**Principle:** Documentation is part of the UX. Apply Ryan Macklin's seven empathy-advocacy tenets.

**Do:**
- Employ visual storytelling (mind accessibility: visual, cognitive, motor).
- Use synopses / tl;dr banners — lower the cognitive cost.
- Give time frames (outage ETAs, upload estimates) — uncertainty creates "vicious voids".
- Include short, single-topic videos.
- Reduce screenshots to only where the UI is genuinely confusing.
- Rethink FAQs into single-scoped documents with specific titles.
- Pick your battles; not everything works for everyone.

*Ref: Building_Modern_CLI_Applications_in_Go.md — "Embedding empathy into your documentation"*

---

### Cross-Platform: `os`, `time`, `path/filepath`, `runtime`  `#systems` `#cross-platform`

**Principle:** Use Go's platform-independent stdlib packages; isolate OS-specific code with `runtime.GOOS` switches or, preferably, build tags + filename suffixes.

**Do:**
- Use `os.UserHomeDir()`, `os.UserConfigDir()`, `os.UserCacheDir()` for user paths (cross-platform).
- Use `filepath.Join` / `filepath.WalkDir` (not string concatenation with `/`).
- Use `time.Now()` / `time.Until()` / `time.Sleep()` — `time.Time` carries both wall and monotonic clocks automatically; monotonic is used for durations.
- Read `runtime.GOOS`, `runtime.GOARCH`, `runtime.NumCPU()`, `runtime.NumGoroutine()`, `runtime.Version()`.
- Split OS-specific code into `play_darwin.go`, `play_linux.go`, `play_windows.go` with matching build tags.

**Don't:**
- Hardcode `/` or `\`.
- Rely on Unix-only concepts on Windows (file modes → ACLs, env case-sensitivity, ANSI colors, `os/signal`).

**OS-level differences to remember:**

| Area             | Windows                                    | Unix/Linux                                  |
|------------------|--------------------------------------------|---------------------------------------------|
| Filesystem       | Backslashes, drive letters                 | Forward slashes                             |
| Permissions      | ACLs                                       | File modes                                  |
| Command exec     | Requires `.exe`/`.bat` extensions          | No extensions                               |
| Env vars         | Case-insensitive                           | Case-sensitive                              |
| Line endings     | `\r\n`                                     | `\n`                                        |
| Signal handling  | `os/signal` unsupported                    | Supported                                   |
| Console colors   | No native ANSI                             | ANSI works                                  |
| ExtraFiles       | Unsupported                                | Supported                                   |

*Ref: Building_Modern_CLI_Applications_in_Go.md — "OS-level differences"*

**Code** — walking a directory cross-platform:
```go
func walking() {
    workingDir, _ := os.Getwd()
    dir1 := filepath.Join(workingDir, "dir1")
    filepath.WalkDir(dir1, func(path string, d fs.DirEntry, err error) error {
        if !d.IsDir() {
            contents, err := os.ReadFile(path)
            if err != nil { return err }
            fmt.Printf("%s -> %s\n", d.Name(), string(contents))
        }
        return nil
    })
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The path package"*

**Code** — `runtime.GOOS` switch (runtime OS dispatch):
```go
switch runtime.GOOS {
case "darwin":  darwinPlay(audio.Path)
case "windows": windowsPlay(audio.Path)
case "linux":   linuxPlay(audio.Path)
default:
    fmt.Println(`Your operating system isn't supported for playing music yet.`)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Platform-specific code"*

**Code** — build-tag split (cleaner than runtime switch):
```go
//go:build darwin
package cmd
import ("fmt"; "os/exec")
func play(audiofilePath string) error {
    cmd := exec.Command("afplay", audiofilePath)
    if err := cmd.Start(); err != nil { return err }
    fmt.Println("enjoy the music!")
    return cmd.Wait()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example in the audio file"*

**Code** — environment and process introspection:
```go
dir, _ := os.Getwd()
os.Setenv("WORKING_DIR", dir)
fmt.Println(os.ExpandEnv("WORKING_DIR=${WORKING_DIR}"))
os.Unsetenv("WORKING_DIR")

// processes
fmt.Println("Process id of caller", os.Getpid())
ps, _ := os.FindProcess(pid)
state, _ := ps.Wait()
if state.Exited() && state.Success() { /* ... */ }
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Environmental operations" / "Process operations"*

---

### Build Tags for Feature Tiers, Tests, and Profiling  `#cli` `#cross-platform` `#testing`

**Principle:** `//go:build` tags use Boolean logic (`||`, `&&`, `!`, parens) to gate files for OS/arch/feature/test-kind/profile-flag.

**Do:**
- Use tags for free/pro tiers (`//go:build !free && pro`), integration tests (`//go:build int`), and feature flags like pprof (`//go:build profile && (free || pro)`).
- Combine tags at build time: `go build -tags "darwin pro profile"`.
- Run targeted tests: `go test ./... -tags pro` or `go test ./cmd -tags "int pro"`.
- Use an `init()` in a tagged file to flip a `profile = true` flag rather than scattering `if runtime` checks.

**Don't:**
- Define `//go:build` more than once per file (compiler error).

**Code** — feature-flag init via tagged file:
```go
//go:build profile && (free || pro)
package metadata
func init() { profile = true }
```
```go
// in metadata.go (always built):
if profile {
    mux.HandleFunc("/debug/pprof/", pprof.Index)
    mux.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Adding build tags to enable pprof"*

**Build matrix examples:**
```bash
go build -tags "darwin free"           -o bin/audiofile main.go
go build -tags "darwin pro"            -o bin/audiofile main.go
go build -tags "darwin pro profile"    -o bin/audiofile main.go
go test  ./... -tags pro
go test  ./cmd -tags "int pro"
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Building a free version" / "Running the tests"*

---

### Cross-Compilation  `#cli` `#cross-platform` `#distribution`

**Principle:** Go cross-compiles natively via `GOOS`/`GOARCH`. View targets with `go tool dist list`; check your local with `go env GOOS GOARCH`.

**Do:**
- Set `GOOS`/`GOARCH` inline: `GOOS=linux GOARCH=amd64 go build -o bin/audiofile-linux main.go`.
- Combine with build tags: `GOOS=linux GOARCH=amd64 go build -tags pro -o bin/audiofile-linux-pro main.go`.
- Automate via a bash/PowerShell script iterating GOOS/GOARCH pairs and zipping archives.
- Prefer GoReleaser for end-to-end release automation (see Distribution).

**Don't:**
- Assume cgo ports work everywhere — check `CgoSupported` via `go tool dist list -json`.

**Code** — manual cross-compilation:
```bash
GOOS=linux   GOARCH=amd64 go build -o bin/audiofile-linux   main.go
GOOS=darwin  GOARCH=arm64 go build -o bin/audiofile-darwin  main.go
GOOS=windows GOARCH=amd64 go build -o bin/audiofile-windows.exe main.go
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Manual compilation"*

---

### Testing CLIs (Unit + Integration)  `#cli` `#testing`

**Principle:** Mock the HTTP client behind an interface; use `bytes.Buffer` for output capture; tag integration tests separately and run them against `httptest.NewServer` or containerized services.

**Do:**
- Define a client interface (`AudiofileClient { Do(req *http.Request) (*http.Response, error) }`) satisfied by both the real and mock client.
- Use `rootCmd.SetOut(&b)` + `rootCmd.SetArgs(...)` + `rootCmd.Execute()` to drive Cobra in tests.
- Compare actual output bytes against expected fixture files (`./testfiles/*.json`).
- Use Viper `SetDefault` in test setup to avoid config drift.
- Initialize both loggers in test config (`utils.InitCLILogger()`) to avoid panics during error logging.
- Separate integration tests with `//go:build int && pro` and run with `go test ./cmd -tags "int pro"`.

**Don't:**
- Hit real external APIs in unit tests.
- Skip failure-path test cases — both success and failure must be covered.

**Code** — interface-based mockable client:
```go
type AudiofileClient interface {
    Do(req *http.Request) (*http.Response, error)
}

var getClient = GetHTTPClient()

func GetHTTPClient() AudiofileClient {
    return &http.Client{Timeout: 15 * time.Second}
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Mocking the HTTP client"*

**Code** — `ClientMock.Do` returning fixture-driven responses:
```go
func (c *ClientMock) Do(req *http.Request) (*http.Response, error) {
    switch req.URL.Path {
    case "/request":
        return &http.Response{
            Status: "OK", StatusCode: http.StatusOK,
            Body: ioutil.NopCloser(bytes.NewBufferString(string(getBytes))),
        }, nil
    case "/upload":
        return &http.Response{
            Status: "OK", StatusCode: http.StatusOK,
            Body: ioutil.NopCloser(bytes.NewBufferString("123")),
        }, nil
    // /list, /delete, /search ...
    }
    return &http.Response{}, nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Mocking the HTTP client"*

**Code** — driving Cobra in a test with output capture:
```go
func TestGet(t *testing.T) {
    ConfigureTest()
    b := bytes.NewBufferString("")
    rootCmd.SetOut(b)
    rootCmd.SetArgs([]string{"get", "--id", "123", "--json"})
    err := rootCmd.Execute()
    if err != nil { fmt.Println("err: ", err) }
    actualBytes, _ := ioutil.ReadAll(b)
    expectedBytes, _ := os.ReadFile("./testfiles/get.json")
    var audio1, audio2 models.Audio
    json.Unmarshal(actualBytes, &audio1)
    json.Unmarshal(expectedBytes, &audio2)
    if !(audio1.Id == audio2.Id && /* ... */) {
        t.Fatalf("expected %q got %q", string(expectedBytes), string(actualBytes))
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Testing the get command"*

**Code** — test configuration with mocked client + Viper defaults:
```go
func ConfigureTest() {
    getClient = &ClientMock{}
    viper.SetDefault("cli.hostname", "testHostname")
    viper.SetDefault("cli.port", 8000)
    utils.InitCLILogger()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Handling test configuration"*

---

### Distribution: Containers (Docker)  `#cli` `#distribution`

**Principle:** Containers give reproducible builds, isolated dependencies, and easy distribution — at the cost of complexity and a Docker dependency.

**Do:**
- Use **multi-stage builds** (`FROM ... AS build` → `COPY --from=build ...` onto `alpine`) — image sizes drop from GB to MB.
- `EXPOSE <port>` and use `ENTRYPOINT ["./binary"]` to make the image behave as an executable.
- Use `docker run --rm -ti` to auto-cleanup and get an interactive TTY.
- Map host paths with `-v hostpath:containerpath` (e.g. `-v $HOME/audiofile:/root/audiofile`).
- Use `docker-compose.yml` to orchestrate CLI + API together; set `depends_on:` for ordering.
- Publish to Docker Hub via `docker tag` + `docker push`; document run instructions in the README.

**Don't:**
- Ship `golang:1.19` (or similar) as the final image — too large.
- Forget `--rm` — stopped containers accumulate gigabytes.

**Code** — multi-stage `Dockerfile` (~24 MB final image):
```dockerfile
# Stage 1
FROM golang:1.19 AS build
WORKDIR /audiofile
COPY . .
RUN go mod download
RUN go build -tags "pro" -o audiofile main.go
# Stage 2
FROM alpine:latest
COPY --from=build /audiofile/audiofile .
EXPOSE 8000
ENTRYPOINT ["./audiofile"]
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Reducing image size by using multi-stage builds"*

**Code** — `docker-compose.yml` for integration tests:
```yaml
version: '3'
services:
  cli:
    build:
      context: .
      dockerfile: cli.Dockerfile
    image: audiofile:cli
    network_mode: host
    depends_on:
      - api
  api:
    build:
      context: .
      dockerfile: api.Dockerfile
    image: audiofile:api
    ports:
      - "8000:8000"
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Writing the Docker Compose file"*

**Code** — distribution image with `ENTRYPOINT`:
```dockerfile
FROM golang:1.19
WORKDIR /audiofile
COPY . .
RUN go mod download
EXPOSE 8000
RUN go build -tags "pro" -o audiofile main.go
ENTRYPOINT ["./audiofile"]
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Building a new image to run as an executable"*

---

### Distribution: GoReleaser + GitHub Actions + Homebrew  `#cli` `#distribution`

**Principle:** Automate the full release pipeline — build matrix → archives → checksums → changelog → GitHub Release → Homebrew tap — triggered by a single `git tag`.

**Do:**
- Initialize with `goreleaser init`; sanity-check via `goreleaser release --snapshot --clean`.
- Configure `.goreleaser.yaml`: `before.hooks` (`go mod tidy`), `builds` (`env: CGO_ENABLED=0`, `goos`, `goarch`, `flags`), `archives` (`tar.gz` for Unix, `zip` for Windows), `checksum.name_template`, `snapshot.name_template`, `changelog` (sort + filters), `release.prerelease: auto`, `universal_binaries` (macOS fat), `brews` (tap owner/name, commit_author).
- Wire GitHub Actions in `.github/workflows/release.yml`: `on.push.tags: ['*']`, `permissions: contents: write`, job steps for checkout (fetch-depth 0), `git fetch --force --tags`, `setup-go`, `goreleaser/goreleaser-action@v4` with `args: release --clean`.
- Create a separate Homebrew tap repo (`homebrew-<app>`); store a `PUBLISHER_TOKEN` secret in the CLI repo for cross-repo formula pushes.
- Trigger via `git tag -a v0.1 -m "..."` then `git push origin v0.1`.

**Don't:**
- Forget `fetch-depth: 0` in checkout — GoReleaser needs full history for changelog.
- Use `latest` for GoReleaser version in CI — pin to `${{ env.GITHUB_REF_NAME }}`.

**Code** — minimal `.goreleaser.yaml` build section:
```yaml
builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - windows
      - darwin
    flags:
      - -tags=pro dev
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Builds and environment variables"*

**Code** — archives, checksum, snapshot, changelog:
```yaml
archives:
  - format: tar.gz
    name_template: >-
      {{ .ProjectName }}_
      {{- title .Os }}_
      {{- if eq .Arch "amd64" }}x86_64
      {{- else if eq .Arch "386" }}i386
      {{- else }}{{ .Arch }}{{ end }}
    format_overrides:
      - goos: windows
        format: zip
checksum:
  name_template: 'checksums.txt'
snapshot:
  name_template: "{{ incpatch .Version }}-next"
changelog:
  sort: asc
  filters:
    exclude:
      - '^docs:'
      - '^test:'
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Archives" / "Checksum" / "Snapshot" / "Changelog"*

**Code** — Homebrew tap block + universal binaries + pre-release:
```yaml
release:
  prerelease: auto
universal_binaries:
  - replace: true
brews:
  - name: audiofile
    homepage: https://github.com/marianina8
    tap:
      owner: marianina8
      name: homebrew-audiofile
    commit_author:
      name: marianina8
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Release" / "Universal binaries" / "Brews"*

**Code** — `.github/workflows/release.yml`:
```yaml
on:
  push:
    tags:
      - '*'
permissions:
  contents: write
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - run: git fetch --force --tags
      - uses: actions/setup-go@v3
        with:
          go-version: '>=1.20.0'
          cache: true
      - uses: goreleaser/goreleaser-action@v4
        with:
          distribution: goreleaser
          version: latest
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.PUBLISHER_TOKEN }}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Jobs"*

**Code** — triggering a release:
```bash
git tag -a v0.1 -m "Initial deploy"
git push origin v0.1
# users then install via:
brew tap marianina8/audiofile
brew install marianina8/audiofile/audiofile
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Tag and push the code" / "Installing with Homebrew and Testing"*

---

## Anti-Patterns & Common Mistakes

- **Silent success:** returning no output on success leaves users wondering if anything happened. → *fix:* always print something brief on success.
- **Raw stack traces to users:** scares users, erodes trust. → *fix:* rewrite into human-readable errors; reserve traces for `--verbose`.
- **Colors through pipes:** breaks `grep`/`awk`/`jq`. → *fix:* gate on `isatty` or `NO_COLOR`/`--no-color`.
- **Interactivity without TTY check:** prompts hang in CI/scripts. → *fix:* `if isatty { prompt }`.
- **`==` for error comparison:** loses wrapped context. → *fix:* `errors.Is` / `errors.As`.
- **Assuming HTTP 4xx/5xx sets the Go error:** it does **not**. → *fix:* explicitly switch on `resp.StatusCode`.
- **`cmd.Wait()` skipped after `cmd.Start()`:** leaks resources. → *fix:* always pair them.
- **Single-stage Docker images:** gigabytes of needless weight. → *fix:* multi-stage builds with `alpine` final stage.
- **Ambiguous subcommand pairs** (`update` vs `upgrade`). → *fix:* pick one, document it.
- **Reusing a `Cmd` after `Run`/`Output`.** → *fix:* construct a new `Cmd` per execution.
- **Single-letter flags for everything.** → *fix:* long forms for all flags, short forms only for common ones.
- **Storing secrets in env vars or args.** → *fix:* `--password-file`.
- **Choosing `logrus` for new projects** (in maintenance mode). → *fix:* Zap or zerolog.
- **Adding `goreleaser` version `latest`** in CI. → *fix:* pin to `${{ env.GITHUB_REF_NAME }}`.

---

## Decision Heuristics / Checklists

### Choosing a project layout
- **Flat** — small apps/libraries; easiest to refactor later.
- **Group by function** (`handlers/`, `models/`, `storage/`) — discourages global state; clear init in `main.go`.
- **Group by module** (self-contained packages) — low coupling, high cohesion; watch for naming stutter (`tags.ExtractTags`).
- **Group by context (hexagonal)** — DDD, ports/adapters, ubiquitous language; needs domain expertise; not for short-term projects.

### When to use which Cobra flag type
- Same flag on command + all subcommands → `PersistentFlags()`.
- Command-only flag → `Flags()`.
- Must be supplied → `MarkPersistentFlagRequired` / `MarkFlagRequired`.

### File-reading strategy decision
- Small file, simple need → `os.ReadFile`.
- Fixed-size streaming → `file.Read(buf)`.
- Line-oriented → `bufio.Scanner` (default split).
- Token-oriented → `bufio.Scanner` + `Split(bufio.ScanWords)`.

### Dangerous-action confirmation ladder
- **Mild** (delete file): no confirm if command is explicitly `delete`; otherwise prompt.
- **Moderate** (delete directory / remote / bulk): prompt + offer `--dry-run`.
- **Severe** (delete complex remote resource): require typing the resource name or `--confirm="name"`.

### Release artifact checklist
- [ ] Multi-platform binaries (`GOOS`/`GOARCH`).
- [ ] Build tags applied (`pro`, `dev`, etc.).
- [ ] `tar.gz` (Unix) + `zip` (Windows) archives.
- [ ] `checksums.txt` (SHA256).
- [ ] Auto-generated changelog (filters for `docs:`/`test:`).
- [ ] Pre-release flag (`prerelease: auto`).
- [ ] Universal/fat binaries for macOS (optional).
- [ ] Homebrew formula pushed to tap repo.
- [ ] Docker image built multi-stage and pushed to registry.

---

## Key Takeaways

1. **UNIX philosophy is the foundation** — small, composable, modular, transparent, robust; Go was designed by UNIX creators around these tenets.
2. **Structure matters from the start** — flat → modular → hexagonal as the project grows; define use cases and requirements before code.
3. **Cobra + Viper is the standard stack** — commands, flags, help, autocomplete, suggestions, man pages, layered config.
4. **Build for humans first, machines second** — always check TTY; offer `--json`/`--plain`/`--quiet`; never animate through a pipe.
5. **Errors are primary UX** — rewrite, decorate, color, suggest next steps; `--verbose` exposes stack traces; one-command bug submission.
6. **Cross-platform is table stakes** — use `os`/`time`/`path/filepath`/`runtime`; split OS code with build tags; remember the Windows/Unix difference table.
7. **External calls require robustness** — `os/exec` for processes, `net/http` for APIs; always set timeouts, rate-limit, check status codes, recover panics.
8. **Distribution should be automated** — GoReleaser + GitHub Actions → GitHub Release + Homebrew; multi-stage Docker for container distribution.
9. **Interactivity increases usability** — prompts, dashboards, spinners, progress bars — but always gated on TTY.
10. **Empathy is a technical skill** — visual storytelling, synopses, time frames, single-scoped docs; make users feel supported.

---

## Cross-References
- Related: [[../Go_Systems_Programming.md]]
- Related: [[../System_Programming_Essentials_with_Go.md]]
- Topic index: [[../INDEX.md]]
