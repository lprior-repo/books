# Building Modern CLI Applications in Go
**Author:** Marian Montagnino (Senior Software Engineer, Netflix)
**Topic tags:** `#cli` `#systems` `#testing` `#api` `#performance` `#go` `#cross-platform` `#distribution` `#ux` `#observability`
**Language focus:** Go-first
**Sources:** `markdown_output/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino.md` · `summaries/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino.md`

## TL;DR
Build Go CLIs as small, composable, human-first programs that remain predictable when called by scripts. The book covers UNIX conventions, project structure, Cobra/Viper, stdin and signals, file processing, `os/exec`, HTTP APIs, rate limits, TTY-aware presentation, empathetic errors and documentation, cross-platform builds, tests, containers, GoReleaser, and Homebrew.

---

## Best Practices by Topic

### 01 — Start with UNIX composability `#cli` `#systems`
**Principle:** Make small programs powerful through composition rather than making one program responsible for everything.
**Do:** Use standard input, output, errors, signals, exit codes, plain text, and JSON so other commands and automation can consume the result.
**Don't:** Hide the program behind an opaque interface that cannot be piped or scripted.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The philosophy of CLI development" / "Building a modular program"*

---

### 02 — Design for humans first `#cli` `#ux`
**Principle:** Treat the human as the primary consumer while preserving explicit machine-readable modes.
**Do:** Use prompts, state messages, suggestions, confirmations, `--plain`, `--json`, and quiet flags.
**Don't:** Assume every caller is another program or send conversational decoration into a pipe.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Building for humans first" / "Designing for a machine"*

---

### 03 — Keep complexity in data and keep programs small `#cli` `#performance`
**Principle:** Add complexity only when required and prefer data structures over branching policy.
**Do:** Reuse established patterns, prototype first, and optimize after observing the actual constraint.
**Don't:** Build a large abstraction or optimize an unmeasured bottleneck.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Keeping it simple" / "Staying small" / "Building a prototype first, then optimizing"*

---

### 04 — Fail noisily, early, and transparently `#cli` `#systems`
**Principle:** Stop invalid work before it corrupts downstream output and explain what happened.
**Do:** Validate early, return non-zero on failure, print a concise success response, and suggest the next step.
**Don't:** Continue after known misuse or leave the terminal silent while work is pending.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Being robust" / "Failing noisily" / "Output"*

---

### 05 — Name the CLI for humans `#cli`
**Principle:** Choose a lowercase name that is short, memorable, easy to pronounce, and easy to type.
**Do:** Use a name that plainly communicates purpose and use dashes only when necessary.
**Don't:** Choose an arbitrary name that makes users think before they can even try the tool.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Name"*

---

### 06 — Preserve recognizable CLI anatomy `#cli`
**Principle:** Keep prompt, command, argument, option, whitespace, syntax, semantics, and help understandable.
**Do:** Explain internal versus external commands, `PATH`, quoting, and the command grammar.
**Don't:** Hide the accepted shape of a command.
**Code:**
```text
~ cat -b transcript
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Anatomy"*

---

### 07 — Make whitespace unambiguous `#cli` `#systems`
**Principle:** Treat spaces inside parameters as data that must be quoted, escaped, or replaced.
**Code:**
```text
cat Screen_Shot_2021-06-05_at_10.23.16_PM.png
cat "Screen Shot 2021-06-05 at 10.23.16 PM.png"
cat Screen\ Shot\ 2021-06-05\ at\ 10.23.16\ PM.png
```
**Do:** Preserve the intended filename as one parameter.
**Don't:** Assume whitespace is part of the argument without shell syntax that says so.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Whitespace"*

---

### 08 — Make help self-sufficient `#cli`
**Principle:** Help is essential because a CLI lacks the visual cues of a GUI.
**Do:** Show help for the bare command and `-h`/`--help`; put common options first; include examples.
**Don't:** Make users search externally for the basic invocation grammar.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Help pages" / "Help and documentation"*

---

### 09 — Use standard help notation `#cli`
**Principle:** Familiar notation lowers the learning cost.
**Do:** Use `<required>`, `[optional]`, `...` for repetition, and `|` for choices.
**Don't:** Make required and optional values visually indistinguishable.
**Code:**
```text
ping <hostname>
mkdir [option] <dirname>
cp [option]... <source>... <directory>
netstat {-t | -u}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Help pages"*

---

### 10 — Choose a layout from project context `#cli` `#systems`
**Principle:** There is no universal Go layout; choose the simplest structure that remains understandable and testable.
**Do:** Justify the choice, begin simply, and let the structure evolve with requirements.
**Don't:** Choose flat, functional, modular, or hexagonal structure arbitrarily or too early.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Commonly used program layouts for robust applications"*

---

### 11 — Start flat for small applications `#cli`
**Principle:** A flat root is appropriate while the project is small and requirements are still forming.
**Do:** Use the lack of circular dependencies and easy refactoring as advantages.
**Don't:** Allow a growing flat project to become disorganized and globally mutable.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Flat structure"*

---

### 12 — Group by function when it clarifies navigation `#cli`
**Principle:** Put similar functionality together when the application is easier to understand that way.
**Do:** Group handlers, models, extractors, and storage; use root `main.go` to make initialization clear.
**Don't:** Leave shared behavior or initialization without a clear owner.
**Code:**
```text
✓ group-by-function
∨ cmd
√ api
  -co main.go
∨ cli
   main.go
√ dashboard
   -co main.go
∨ extractors
  tags.go
  transcript.go
∨ handlers
  handler_get.go
  handler_upload.go
∨ models
  tags.go
  transcript.go
∨ services / metadata
  metadata.go
✓ storage
  flatfile.go
go.mod
main.go
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Grouping code by function"*

---

### 13 — Group by module when cohesion justifies it `#cli` `#architecture`
**Principle:** Keep everything needed for a self-contained function in its module when low coupling outweighs complexity.
**Do:** Enforce strict organization and watch for package-name stutter and circular dependencies.
**Don't:** Assume more packages automatically create a better design.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Grouping by module"*

---

### 14 — Use hexagonal boundaries for domain-heavy CLIs `#cli` `#api`
**Principle:** Ports and adapters fit domains with changing business requirements and integrations.
**Do:** Put interfaces at boundaries, let outer layers call inner layers, and keep concrete storage in adapters.
**Don't:** Make the domain know whether storage is MongoDB, Elasticsearch, or a flat file.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Grouping by context" / "Repository"*

---

### 15 — Use recognizable Go folders `#cli` `#systems`
**Principle:** Folder names should reveal responsibility to current and future maintainers.
**Do:** Use `cmd`, `pkg`, `internal`, `api`, `configs`, `scripts`, `build`, `deployments`, `test`, and `vendor` for their stated purposes.
**Don't:** Use vague package names such as `util`, `common`, or `script`, or use snake_case/camelCase package names.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Common folders"*

---

### 16 — Define use cases before flags and endpoints `#cli` `#api`
**Principle:** Document functional behavior without implementation-specific language before coding.
**Do:** Record actors, preconditions, triggers, basic flows, and alternative flows.
**Don't:** Let an early parser or endpoint decide the business behavior by accident.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Use cases" / "Use cases, diagrams, and requirements for a CLI"*

---

### 17 — Record non-functional requirements `#systems` `#performance`
**Principle:** Specify security, capacity, compatibility, reliability, maintainability, scalability, usability, performance, and environment constraints.
**Do:** State supported platforms, data limits, response expectations, and third-party dependencies.
**Don't:** Assume functional correctness automatically satisfies user expectations.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Requirements" / "Requirements for a metadata CLI"*

---

### 18 — Use domain language consistently `#api` `#architecture`
**Principle:** A bounded context and ubiquitous language give entities and values stable meaning.
**Do:** Define terms such as metadata, extraction, user, and audio with the domain experts.
**Don't:** Let different teams silently use the same word for different behavior.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Bounded context" / "Language"*

---

### 19 — Separate entities, values, services, events, and repositories `#api`
**Principle:** Name domain building blocks by their responsibility.
**Do:** Use entities for domain objects, value objects for fields, services for domain functions, events for occurrences, and repositories for domain collections.
**Don't:** Put concrete database knowledge into the domain interface.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Entities and value objects" / "Service" / "Events" / "Repository"*

---

### 20 — Keep the audio metadata boundary explicit `#api`
**Principle:** Separate entry points, extractors, interfaces, models, services, and storage.
**Code:**
```text
/Users/username/go/src/github.com/audiocompany/audiofile
   |--cmd
   |----api
   |----cli
   |--extractors
   |----tags
   |----transcript
   |--internal
   |----interfaces
   |--models
   |--services
   |----metadata
   |--storage
   |--vendor
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating the structure"*

---

### 21 — Keep entry points thin `#cli` `#api`
**Principle:** Parse configuration and delegate behavior to a service or command package.
**Code:**
```go
package main
import (
    metadataService "audiofile/services/metadata"
    "flag"
    "fmt"
)
func main() {
    var port int
    flag.IntVar(&port, "p", 8000, "Port for metadata
      service")
    flag.Parse()
    fmt.Printf("Starting API at http://localhost:%d\n",
      port)
    metadataService.Run(port)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/api/"*

---

### 22 — Inject the client and define a command contract `#cli` `#testing`
**Principle:** Commands should depend on small interfaces that can be replaced in tests.
**Code:**
```go
type Command interface {
   ParseFlags([]string) error
   Run() error
   Name() string
}
```
```go
package main
import (
    "audiofile/internal/command"
    "audiofile/internal/interfaces"
    "fmt"
    "net/http"
    "os"
)
func main() {
    client := &http.Client{}
    cmds := []interfaces.Command{
        command.NewGetCommand(client),
        command.NewUploadCommand(client),
        command.NewListCommand(client),
    }
    parser := command.NewParser(cmds)
    if err := parser.Parse(os.Args[1:]); err != nil {
        os.Stderr.WriteString(fmt.Sprintf("error: %v",
          err.Error()))
        os.Exit(1)
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/cli/" / "internal/interfaces"*

---

### 23 — Dispatch commands explicitly `#cli`
**Principle:** The parser should choose by the first argument, parse the remainder, and return unknown-command errors.
**Code:**
```go
type Parser struct {
    commands []interfaces.Command
}
func NewParser(commands []interfaces.Command) *Parser {
    return &Parser{commands: commands}
}
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

### 24 — Give empty invocation a usable help path `#cli`
**Principle:** A command with no arguments should teach the user what can be run.
**Code:**
```go
func help() {
    help := `usage: ./audiofile-cli <command> [<flags>]
These are a few Audiofile commands:
   get Get metadata for a particular audio file by id
   list List all metadata
   upload Upload audio file
   `
    fmt.Println(help)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/cli/command"*

---

### 25 — Use the standard `flag` package for small surfaces `#cli`
**Principle:** Use typed standard flags until nested commands justify Cobra.
**Do:** Define all flags before `flag.Parse`; choose `ContinueOnError`, `ExitOnError`, or `PanicOnError` intentionally.
**Don't:** Introduce framework machinery for a one-command entry point without a need.
**Code:**
```go
var port int
flag.IntVar(&port, "p", 8000, "Port for metadata service")
flag.Parse()
fmt.Printf("Starting API at http://localhost:%d\n", port)
metadataService.Run(port)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "cmd/api/" / "Implementing use cases"*

---

### 26 — Prefer long flag forms `#cli`
**Principle:** Full-length flags are discoverable; shorthand is for common options.
**Do:** Provide `--help`, `--json`, `--no-input`, `--output`, `--port`, `--quiet`, `--version`, and similar long forms.
**Don't:** Assign a single letter to every option or create shorthand collisions.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Flags" / "Input"*

---

### 27 — Use Cobra when the tree grows `#cli`
**Principle:** Cobra supplies nested commands, completion, suggestions, help, and scaffolding.
**Code:**
```text
cd audiofile-cli
go mod init <module path>
cobra-cli init
cobra-cli add upload
```
**Don't:** Hand-roll complicated nested parsing after adopting a framework that provides it.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Cobra – a library for building modern CLI applications"*

---

### 28 — Populate Cobra command metadata `#cli` `#ux`
**Principle:** `Use`, `Short`, `Long`, and `Example` are executable documentation.
**Code:**
```go
var uploadCmd = &cobra.Command{
    Use: "upload [audio|video] [-f|--filename]
      <filename>",
    Short: "upload an audio or video file",
    Long: `This command allows you to upload either an
      audio or video file for metadata extraction.
    To pass in a filename, use the -f or --filename flag
     followed by the path of the file.
    Examples:
    ./audiofile-cli upload audio -f audio/beatdoctor.mp3`,
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating subcommands"*

---

### 29 — Model nested resources clearly `#cli`
**Principle:** Use familiar noun/action relationships and avoid ambiguous command pairs.
**Do:** Prefer consistent patterns such as `docker image ls` and `docker container ls`.
**Don't:** Give users both `update` and `upgrade` without a clear distinction.
**Code:**
```go
func init() {
    audioCmd.Flags().StringP("filename", "f", "", "audio
      file")
    uploadCmd.AddCommand(audioCmd)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating subcommands" / "Commands and subcommands"*

---

### 30 — Return errors through `RunE` `#cli` `#error-handling`
**Principle:** Use `RunE` when a command can fail and return errors from validation.
**Code:**
```go
RunE: func(cmd *cobra.Command, args []string) error {
    filename, err := cmd.Flags().GetString("filename")
    if err != nil {
        fmt.Printf("error retrieving filename: %s\n",
        err.Error())
        return err
    }
    if filename == "" {
        return errors.New("missing filename")
    }
    fmt.Println("uploading audio file, ", filename)
    return nil
},
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating subcommands"*

---

### 31 — Scope flags deliberately `#cli`
**Principle:** Local flags belong to one command; persistent flags belong to a command and descendants.
**Code:**
```go
var (
    Filename = ""
)
func init() {
    uploadCmd.PersistentFlags().StringVarP(&Filename,
      "filename", "f", "", "file to upload")
    uploadCmd.MarkPersistentFlagRequired("filename")
    rootCmd.AddCommand(uploadCmd)
}
```
**Don't:** Reimplement required-flag validation in every subcommand when Cobra can enforce it.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Global, local, and required flags"*

---

### 32 — Keep suggestions and generated help enabled `#cli` `#ux`
**Principle:** Mistyped commands should suggest recovery and help should come from the command tree.
**Do:** Tune `SuggestionsMinimumDistance` or use `SuggestFor` for logical substitutes.
**Don't:** Return only an unknown-command message with no next step.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Intelligent suggestions" / "Automatically generated help and man pages"*

---

### 33 — Layer configuration with Viper `#cli` `#systems`
**Principle:** Support files, environment variables, flags, buffers, and remote configuration through one layer.
**Do:** Use defaults, typed getters, and explicit search paths; support JSON, TOML, YAML, HCL, INI, envfile, and Java properties as required.
**Don't:** Hardcode hostnames, ports, storage paths, or environment-specific settings in commands.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Viper – easy configuration for CLIs" / "Configuration types"*

---

### 34 — Read file and environment configuration predictably `#cli`
**Principle:** Name the config, add search paths, read it, then bind environment overrides.
**Code:**
```yaml
environments:
  test:
    url: 89.45.23.123
    port: 1234
  prod:
    url: 123.23.45.89
    port: 5678
loglevel: 1
keys:
  assemblyai: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
```go
viper.SetConfigName("config") // config filename, omit
  extension
viper.AddConfigPath(".") // optional locations for
  searching for config files
err = viper.ReadInConfig() // using the previous
  settings above, attempt to find and read in the
    configuration
if err != nil { // Handle errors
    panic(fmt.Errorf("err: %w \n", err))
}
fmt.Println("prod environment url:",
  viper.Get("environments.prod.url"))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Config file"*

---

### 35 — Use environment prefixes and typed defaults `#cli` `#systems`
**Principle:** Give environment variables an application namespace and retrieve values in their intended types.
**Code:**
```go
viper.SetEnvPrefix("AUDIOFILE")
viper.BindEnv("TEST_URL")
os.Setenv("AUDIOFILE_TEST_URL", "89.45.23.123") //sets the
  environment variable
fmt.Println(viper.Get("TEST_URL"))
viper.SetDefault("host", "localhost")
viper.SetDefault("port", 1234)
viper.BindEnv("host", "AUDIOFILE_HOST")
viper.BindEnv("port", "AUDIOFILE_PORT")
port := viper.GetInt("port")
host := viper.GetString("host")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Environment variable" / "Flags"*

---

### 36 — Bind pflags, custom flags, buffers, and live sources `#cli`
**Principle:** Keep configuration access uniform even when its source varies.
**Code:**
```go
pflag.CommandLine.AddGoFlagSet(flag.CommandLine)
pflag.Int("port", 1234, "port")
pflag.String("url", "12.34.567.123", "url")
plag.Parse()
viper.BindPFlags(pflag.CommandLine)
```
```go
type FlagValue interface {
    HasChanged() bool
    Name() string
    ValueString() string
    ValueType() string
}
type FlagValueSet interface {
    VisitAll(fn func(FlagValue))
}
```
```go
viper.OnConfigChange(func(event fsnotify.Event) {
    fmt.Println("Config modified:", event)
})
viper.WatchConfig()
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Pflags" / "Flag interfaces" / "Watching for live config changes"*

---

### 37 — Keep secrets out of arguments and environment variables `#cli` `#systems`
**Principle:** Use `--password-file` or standard input for discreet secret delivery.
**Do:** Follow the XDG Spec for configuration locations and exclude sensitive session data from logs.
**Don't:** Put passwords in arguments, flags, or ordinary environment variables.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Security" / "XDG Spec"*

---

### 38 — Use a stable command grammar `#cli`
**Principle:** Keep application, resource, action, and modifier positions predictable.
**Code:**
```text
APPNAME NOUN VERB --ADJECTIVE
APPNAME ARGUMENT <COMMAND | SUBCOMMANDS> --FLAG
```
**Do:** Keep arguments, flags, and subcommands order-independent where possible.
**Don't:** Mix noun-verb and verb-noun conventions without a rule.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Defining subcommands, arguments, and flags"*

---

### 39 — Use arguments for nouns and flags for modifiers `#cli`
**Principle:** Positional values name the objects acted upon; flags describe how the action behaves.
**Do:** Allow multiple arguments for simple multi-file actions and globbing where it makes sense.
**Don't:** Use several positional values with unrelated meanings when named flags would clarify them.
**Code:**
```go
Run: func(cmd *cobra.Command, args []string) {
    if len(args) == 0 {
        fmt.Println("subcommand called")
    } else {
        fmt.Println("subcommand called with arguments: ",
          args)
    }
},
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Arguments" / "Flags"*

---

### 40 — Support stdin and pipelines `#cli` `#systems`
**Principle:** Let one command do one thing well and compose with another command through standard streams.
**Code:**
```go
reader := bufio.NewReader(os.Stdin)
s, _ := reader.ReadString('\n')
fmt.Printf("piped in: %s\n", s)
```
**Don't:** Prompt when stdin is already a pipe.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Piping"*

---

### 41 — Treat signals as input `#systems`
**Principle:** User control characters and kernel signals are part of the command's input model.
**Do:** Handle `SIGINT`, `SIGTSTP`, `SIGQUIT`, `SIGHUP`, and `SIGPIPE` where the workflow requires them; remember `SIGKILL` and `SIGSTOP` cannot be caught.
**Don't:** Assume flags and arguments are the only ways a command can stop.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Signals and control characters"*

---

### 42 — Install interrupt handlers before execution `#systems`
**Principle:** Register graceful handlers before the root command starts.
**Code:**
```go
func SetupInterruptHandler() {
    c := make(chan os.Signal)
    signal.Notify(c, os.Interrupt, syscall.SIGINT)
    go func() {
        <-c
        fmt.Println("\r- Wake up! Sleep has been
          interrupted.")
        os.Exit(0)
    }()
}
func SetupStopHandler() {
    c := make(chan os.Signal)
    signal.Notify(c, os.Interrupt, syscall.SIGTSTP)
    go func() {
        <-c
        fmt.Println("\r- Wake up! Stopped sleeping.")
        os.Exit(0)
    }()
}
func Execute() {
    SetupInterruptHandler()
    SetupStopHandler()
    err := rootCmd.Execute()
    if err != nil {
        os.Exit(1)
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Signals and control characters"*

---

### 43 — Prompt only when a human is present `#cli` `#ux`
**Principle:** Prompts create conversational flow but must not be the only input path.
**Do:** Use `survey.Input`, `Select`, `MultiSelect`, `Multiline`, `Password`, and `Confirm`; validate results and mask secrets.
**Don't:** Start an interactive prompt in a pipe, CI job, or script.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "User interaction" / "Guiding users with prompts"*

---

### 44 — Prompt for missing values with suggestions `#cli`
**Principle:** Turn missing human input into guided discovery.
**Code:**
```go
func AskForID() (string, error) {
  id := ""
  prompt := &survey.Input{
    Message: "What is the id of the audiofile?",
  }
  survey.AskOne(prompt, &id)
  if id == "" {
    return "", fmt.Errorf("missing required argument: id")
  }
  return id, nil
}
func AskForFilename() (string, error) {
  file := ""
  prompt := &survey.Input{
    Message: "What is the filename of the audio to upload
      for metadata extraction?",
    Suggest: func(toComplete string) []string {
      files, _ := filepath.Glob(toComplete + "*")
      return files
    },
  }
  survey.AskOne(prompt, &file)
  if file == "" {
    return "", fmt.Errorf("missing required argument:
      file")
  }
  return file, nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Example 1: Prompt for information when a flag is missing"*

---

### 45 — Scale destructive confirmations to danger `#cli` `#systems`
**Principle:** Mild, moderate, and severe operations need progressively stronger confirmation.
**Do:** Offer a dry run for moderate changes and typed resource confirmation or `--confirm="name-of-resource"` for severe changes.
**Code:**
```go
func Confirm(confirmationText string) bool {
  confirmed := false
  prompt := &survey.Confirm{
    Message: confirmationText,
  }
  survey.AskOne(prompt, &confirmed)
  return confirmed
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Conversation as the norm" / "Example 2: Confirm deletion"*

---

### 46 — Validate typed input at the boundary `#cli`
**Principle:** Convert argument strings before side effects and use typed flags where possible.
**Code:**
```go
val, err := strconv.Atoi("123")
var intValue int
flag.IntVar(&intValue, "flagName", 123, "help message")
```
```go
type Value interface {
    String() string
    Set(string) error
    Type() string
}
```
**Don't:** Delay conversion until after a request or file mutation.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Processing data"*

---

### 47 — Match file reading to the data shape `#systems` `#performance`
**Principle:** Use all-at-once, chunked, line, or word reads according to memory and record requirements.
**Do:** Use `os.ReadFile` for small complete files, `file.Read` for bounded chunks, default scanners for lines, and `ScanWords` for words.
**Don't:** Read a huge line-oriented file into memory without need.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Processing data"*

---

### 48 — Read complete small files simply `#systems`
**Principle:** `os.ReadFile` is appropriate when the entire file is the useful unit.
**Code:**
```go
func all(filename string) {
    content, err := os.ReadFile(filename)
    if err != nil {
        fmt.Printf("Error reading file: %s\n", err)
        return
    }
    fmt.Printf("content: %s\n", content)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "In its entirety, all at once"*

---

### 49 — Stream bounded chunks and scanner tokens `#systems` `#performance`
**Principle:** Bound memory and select the correct token boundary.
**Code:**
```go
func chunk(file *os.File) {
    const size = 8 // chunk size
    buff := make([]byte, size)
    fmt.Println("content: ")
    for {
        read8Bytes, err := file.Read(buff)
        if err != nil {
            if err != io.EOF {
                fmt.Println(err)
            }
            break
        }
        fmt.Println(string(buff[:read8Bytes]))
    }
}
func line(file *os.File) {
    scanner := bufio.NewScanner(file)
    lineCount := 0
    for scanner.Scan() {
        fmt.Printf("%d: %s\n", lineCount, scanner.Text())
        lineCount++
    }
    if err := scanner.Err(); err != nil {
        fmt.Printf("error scanning line by line: %s\n", err)
    }
}
func word(file *os.File) {
    scanner := bufio.NewScanner(file)
    scanner.Split(bufio.ScanWords)
    wordCount := 0
    for scanner.Scan() {
        fmt.Printf("%d: %s\n", wordCount, scanner.Text())
        wordCount++
    }
    if err := scanner.Err(); err != nil {
        fmt.Printf("error scanning by words: %s\n", err)
    }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "In predefined chunks" / "Line by line" / "Word by word"*

---

### 50 — Classify processing as batch, online, or real time `#systems` `#api`
**Principle:** The use case determines whether tasks are grouped, Internet-bound, or time-critical.
**Do:** Use batch for collected work, online for API-backed work, and real time where timeliness is the requirement.
**Don't:** Force every workload into one processing model.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Processing data"*

---

### 51 — Separate stdout, stderr, and exit status `#cli` `#systems`
**Principle:** Streams and exit codes are part of the public CLI contract.
**Do:** Put results on stdout, errors on stderr, debug and warnings in verbose output, and return zero only on success.
**Don't:** Mix logs into machine-readable output or use stderr as a general log file.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Returning the resulting output" / "stdout" / "stderr"*

---

### 52 — Detect TTY status before formatting `#cli` `#systems`
**Principle:** A character device suggests a human; a pipe suggests another program.
**Code:**
```go
fileInfo, _ := os.Stdout.Stat()
if (fileInfo.Mode() & os.ModeCharDevice) != 0 {
    fmt.Println("terminal")
} else {
    fmt.Println("not a terminal")
}
```
```go
package utils
import (
  "fmt"
  "os"
  isatty "github.com/mattn/go-isatty"
)
func IsaTTY() {
  if isatty.IsTerminal(os.Stdout.Fd()) || isatty.
     IsCygwinTerminal(os.Stdout.Fd()) {
    fmt.Println("Is a TTY")
  } else {
    fmt.Println("Is not a TTY")
  }
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Is it a TTY?"*

---

### 53 — Make machine output stable and plain `#cli` `#api`
**Principle:** Pipes need predictable records rather than human decoration.
**Do:** Disable color, ASCII art, animation, and prompts; support `--plain`, `--json`, `--quiet`, and `--silent`.
**Don't:** Force scripts to strip emojis, progress bars, or ANSI escape codes.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Designing for a machine"*

---

### 54 — Keep human output conversational and fast `#cli` `#performance`
**Principle:** Response time is perceived quality; print before a slow network or file boundary.
**Do:** Communicate current state, success, and suggested next commands in concise language.
**Don't:** Show developer-only details unless verbose mode is requested.
**Code:**
```go
fmt.Printf("Sending request: %s %s %s...\n",
           http.MethodGet, path, payload)
resp, err := client.Do(req)
if err != nil {
  return nil, err
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Conversation as the norm" / "Example 3: Notify users when making a network request"*

---

### 55 — Use tables, color, and emoji intentionally `#cli` `#ux`
**Principle:** Increase information density without making every item visually loud.
**Do:** Use green for success, red for errors, and a plain fallback when decoration is unavailable.
**Don't:** Use so many colors that nothing stands out.
**Code:**
```go
const (
  checkMark = "\U00002705"
  crossMark = "\U0000274C"
)
fmt.Println(checkMark, " Successfully uploaded!")
var IdColor = color.New(color.FgGreen).SprintFunc()
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Displaying information with tables" / "Clarifying with emojis" / "Using color with intention"*

---

### 56 — Render tables without breaking scripts `#cli` `#api`
**Principle:** Tables are for scanning; plain records are for machine integration.
**Code:**
```go
var header = []string{"ID", "Path", "Status", "Title", "Album"}
func row(audio Audio) []string {
  return []string{
    audio.Id, audio.Path, audio.Status,
    audio.Metadata.Tags.Title, audio.Metadata.Tags.Album,
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

---

### 57 — Page only human-scale output `#cli` `#systems`
**Principle:** Use `less` on Unix and `more` on Windows only when a human is reading a large result.
**Code:**
```go
func Pager(data string) error {
  lessCmd := exec.Command("less", "-r")
  lessCmd.Stdin = strings.NewReader(data)
  lessCmd.Stdout = os.Stdout
  lessCmd.Stderr = os.Stderr
  return lessCmd.Run()
}
```
```go
func Pager(data string) error {
    moreCmd := exec.Command("cmd", "/C", "more")
    moreCmd.Stdin = strings.NewReader(data)
    moreCmd.Stdout = os.Stdout
    moreCmd.Stderr = os.Stderr
    return moreCmd.Run()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Pagination for Unix or Linux" / "Pagination for Windows"*

---

### 58 — Gate spinners and progress bars on TTY `#cli` `#performance`
**Principle:** Motion communicates activity only when the destination can display it usefully.
**Code:**
```go
spinnerInfo := &pterm.SpinnerPrinter{}
if utils.IsaTTY() {
    spinnerInfo, _ = pterm.DefaultSpinner.Start("Enjoy the music...")
}
err := cmd.Wait()
if utils.IsaTTY() { spinnerInfo.Stop() }
```
```go
p, _ := pterm.DefaultProgressbar.WithTotal(4).WithTitle("Initiating upload...").Start()
pterm.Success.Println("Created multipart writer")
p.Increment()
p.UpdateTitle("Sending request...")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Spinners and progress bars"*

---

### 59 — Treat `os/exec` as a process API, not a shell `#systems` `#security`
**Principle:** `os/exec` does not expand globs, pipes, or redirections.
**Do:** Use `filepath.Glob`, `os.ExpandEnv`, or explicit safe shell invocation when shell behavior is required.
**Don't:** Pass unescaped user values to a shell or expect a `Cmd` to be reusable.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The os/exec package"*

---

### 60 — Configure `Cmd` fields intentionally `#systems`
**Principle:** Path, args, environment, directory, streams, extra files, process, and state define the child boundary.
**Do:** Set `Path`, `Args`, `Env`, `Dir`, `Stdin`, `Stdout`, and `Stderr` explicitly when the default is not correct; remember `ExtraFiles` starts at descriptor 3 and is unsupported on Windows.
**Don't:** Let output disappear into `os.DevNull` by accident.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Types" / "Cmd struct"*

---

### 61 — Pass additional descriptors only where supported `#systems`
**Principle:** Use `ExtraFiles` and pipes for Unix-style child communication, and isolate Windows alternatives.
**Code:**
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

---

### 62 — Pair `Start` and `Wait` and choose output methods `#systems`
**Principle:** Start asynchronously only when you will wait; choose output capture by stream requirement.
**Code:**
```go
if err := cmd.Start(); err != nil {
    panic(err)
}
err = cmd.Wait()
if err != nil {
    panic(err)
}
out, err := cmd.Output()
CombinedOutput, err := cmd.CombinedOutput()
```
**Don't:** Call `Wait` after `Run`, or call `Run` while relying on an unfinished stdout/stderr pipe.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Running the command" / "Methods"*

---

### 63 — Adapt external commands for Windows `#systems` `#cross-platform`
**Principle:** Use `cmd /C`, Windows executable conventions, and `more` where required.
**Code:**
```go
func CreateCommandUsingCommandFunction() {
    cmd := exec.Command("cmd", "/C", "ping", "google.com")
    output, err := cmd.CombinedOutput()
    if err != nil {
        panic(err)
    }
    fmt.Println(string(output))
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Executing commands on Windows"*

---

### 64 — Build HTTP requests with full control `#api` `#cli`
**Principle:** Use `http.NewRequest` and `client.Do` when method, URL, body, headers, client, and response handling matter.
**Code:**
```go
params := "id=" + url.QueryEscape(cmd.id)
path := fmt.Sprintf("http://localhost/request?%s", params)
payload := &bytes.Buffer{}
req, err := http.NewRequest("GET", path, payload)
if err != nil { return err }
resp, err := client.Do(req)
if err != nil { return err }
defer resp.Body.Close()
b, err := io.ReadAll(resp.Body)
if err != nil { return err }
fmt.Println(string(b))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Get request"*

---

### 65 — Upload multipart data explicitly `#api` `#systems`
**Principle:** Validate the file, preserve its base name, stream its bytes, close the multipart writer, and set its content type.
**Code:**
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

---

### 66 — Implement upload and get as testable commands `#api` `#testing`
**Principle:** Command methods should validate flags and use injected clients rather than global transport behavior.
**Code:**
```go
func (cmd *GetCommand) Run() error {
    if cmd.id == "" {
        return fmt.Errorf("missing id")
    }
    params := "id=" + url.QueryEscape(cmd.id)
    path := fmt.Sprintf("http://localhost/request?%s", params)
    payload := &bytes.Buffer{}
    method := "GET"
    client := cmd.client
    req, err := http.NewRequest(method, path, payload)
    if err != nil { return err }
    resp, err := client.Do(req)
    if err != nil { return err }
    defer resp.Body.Close()
    b, err := io.ReadAll(resp.Body)
    if err != nil { return err }
    fmt.Println(string(b))
    return nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Requesting metadata"*

---

### 67 — Handle HTTP responses in four steps `#api`
**Principle:** Check status, log safe data, store when required, and transform the body into a typed model.
**Do:** Use `http.DetectContentType` when the response format is not known and unmarshal JSON into a local struct.
**Don't:** Treat a body read as complete response handling.
**Code:**
```go
var audio Audio
If err := json.Unmarshal(b, &audio); err != nil {
fmt.Println("error unmarshalling JSON response"
}
contentType := http.DetectContentType(b)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Get request"*

---

### 68 — Paginate API results and rate-limit calls `#api` `#performance`
**Principle:** Bound result size and request frequency.
**Code:**
```go
path := fmt.Sprintf("http://localhost/request?limit=%d&page=%d", limit, page)
```
```go
type runner struct {
    Run func() bool
    limiter *rate.Limiter
}
thing := runner{}
start := time.Now()
thing.Run = func() bool {
    if thing.limiter.Allow() {
        fmt.Println(time.Now())
        return false
    }
    if time.Since(start) > 30*time.Second { return true }
    return false
}
thing.limiter = rate.NewLimiter(rate.Every(5*time.Second), 1)
for { if thing.Run() { break } }
```
**Don't:** Hit public APIs repeatedly or load an unbounded result into one response.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Pagination" / "Rate limiting"*

---

### 69 — Time out external commands `#systems` `#performance`
**Principle:** Race process completion against a timeout.
**Code:**
```go
func Timeout() {
    errChan := make(chan error, 1)
    cmd := exec.Command(filepath.Join(os.Getenv("GOPATH"),
           "bin", "timeout"))
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

---

### 70 — Separate transport errors, status errors, and panics `#api` `#error-handling`
**Principle:** A Go error, an HTTP status, and a panic are different failure classes.
**Do:** Use `errors.Is` for wrapped exec errors, inspect `*url.Error`, switch on `StatusCode`, and recover unexpected panics at a boundary.
**Don't:** Compare wrapped errors with `==` or expose raw traces without an empathetic overlay.
**Code:**
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

---

### 71 — Set HTTP timeouts and inspect `url.Error` `#api` `#performance`
**Principle:** Bound remote waiting time and classify timeout or temporary network behavior.
**Code:**
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
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Timeouts and other errors with HTTP requests"*

---

### 72 — Inspect non-OK response status and body `#api`
**Principle:** 4xx and 5xx responses are response data, not necessarily Go errors.
**Code:**
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
data, err := ioutil.ReadAll(resp.Body)
if err != nil { fmt.Println("err:", err) }
fmt.Println("response body:", string(data))
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Timeouts and other errors with HTTP requests"*

---

### 73 — Use portable OS, time, path, and runtime APIs `#systems` `#cross-platform`
**Principle:** Prefer standard abstractions before platform-specific code.
**Do:** Use `os.UserHomeDir`, `filepath.Join`, `filepath.WalkDir`, `time.Now`, `time.Until`, `runtime.GOOS`, `runtime.GOARCH`, `runtime.NumCPU`, and `runtime.Version`.
**Don't:** Hardcode `/`, `\`, Unix permissions, or platform-specific signal assumptions.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Packages for platform-independent functionality"*

---

### 74 — Manage environment and files through `os` `#systems`
**Principle:** Use `os` for working directories, environment variables, files, links, and user directories.
**Code:**
```go
func environment() {
    dir, err := os.Getwd()
    if err != nil { fmt.Println("error getting working directory:", err) }
    fmt.Println("retrieved working directory: ", dir)
    err = os.Setenv("WORKING_DIR", dir)
    if err != nil { fmt.Println("error setting working directory:", err) }
    fmt.Println(os.ExpandEnv("WORKING_DIR=${WORKING_DIR}"))
    err = os.Unsetenv("WORKING_DIR")
    if err != nil { fmt.Println("error unsetting working directory:", err) }
    fmt.Println(os.ExpandEnv("WORKING_DIR=${WORKING_DIR}"))
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Environmental operations"*

---

### 75 — Measure duration with the monotonic clock and inspect runtime `#systems` `#performance`
**Principle:** Go's `Time` stores wall and monotonic values; runtime facts support diagnostics and decisions.
**Code:**
```go
func timer() {
    start := time.Now()
    fmt.Println("start time: ", start)
    time.Sleep(1 * time.Second)
    elapsed := time.Until(start)
    fmt.Println("elapsed time: ", elapsed)
}
func checkRuntime() {
    fmt.Println("Operating System:", runtime.GOOS)
    fmt.Println("Architecture:", runtime.GOARCH)
    fmt.Println("Go Root:", runtime.GOROOT())
    fmt.Println("Compiler:", runtime.Compiler)
    fmt.Println("No. of CPU:", runtime.NumCPU())
    fmt.Println("No. of Goroutines:", runtime.NumGoroutine())
    fmt.Println("Version:", runtime.Version())
    debug.PrintStack()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The time package" / "The runtime package"*

---

### 76 — Isolate platform-specific commands with runtime or tags `#systems` `#cross-platform`
**Principle:** Keep OS-specific process names and arguments out of shared command flow.
**Code:**
```go
switch runtime.GOOS {
case "darwin":  darwinPlay(audio.Path)
case "windows": windowsPlay(audio.Path)
case "linux":   linuxPlay(audio.Path)
default:
    fmt.Println(`Your operating system isn't supported for playing music yet.`)
}
```
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
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Platform-specific code" / "Build tags"*

---

### 77 — Put one build constraint at the top `#testing` `#cross-platform`
**Principle:** Build tags select files at compile time and use Boolean logic.
**Do:** Put `//go:build [tag]` before the package clause, combine with `||`, `&&`, `!`, and parentheses, and use `_windows.go` when the suffix is sufficient.
**Don't:** Define the build constraint more than once in a file.
**Code:**
```go
//go:build (linux || openbsd) && amd64 && !cgo
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "What are build tags and how can you use them?"*

---

### 78 — Use tags for tiers, integration tests, and profiling `#testing` `#performance`
**Principle:** Tags can separate free, pro, dev, profile, and integration variants.
**Code:**
```go
//go:build !free && pro
```
```go
//go:build int && pro
```
```go
//go:build profile && (free || pro)
package metadata
func init() {
    profile = true
}
```
```go
if profile {
    mux.HandleFunc("/debug/pprof/", pprof.Index)
    mux.HandleFunc("/debug/pprof/{action}", pprof.Index)
    mux.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating a pro, free, and dev version" / "Adding build tags to enable pprof"*

---

### 79 — Cross-compile with explicit `GOOS` and `GOARCH` `#cross-platform` `#distribution`
**Principle:** The Go toolchain can target different operating systems and architectures from one development machine.
**Code:**
```text
go tool dist list
go env GOOS GOARCH
GOOS=linux GOARCH=amd64 go build -o bin/audiofile-linux main.go
GOOS=darwin GOARCH=arm64 go build -o bin/audiofile-darwin main.go
GOOS=windows GOARCH=amd64 go build -o bin/audiofile-windows.exe main.go
GOOS=linux GOARCH=amd64 go build -tags pro -o bin/audiofile-linux-pro main.go
```
**Don't:** Assume cgo support or an identical filesystem/command model on every port.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Using GOOS and GOARCH" / "Manual compilation"*

---

### 80 — Automate build matrices with scripts `#cross-platform`
**Principle:** Use scripts when a Makefile becomes a long list of OS, architecture, and feature combinations.
**Code:**
```bash
# Generate darwin builds
darwin_archs=(amd64 arm64)
for darwin_arch in ${darwin_archs[@]}
do
    echo "building for darwin/${darwin_arch} free version..."
    env GOOS=darwin GOARCH=${darwin_arch} go build -tags free -o
    builds/free/darwin/${darwin_arch}/audiofile main.go
    echo "building for darwin/${darwin_arch} pro version..."
    env GOOS=darwin GOARCH=${darwin_arch} go build -tags pro -o
    builds/pro/darwin/${darwin_arch}/audiofile main.go
done
```
```powershell
# Generate windows builds
$windows_archs="386","amd64","arm","arm64"
foreach ($windows_arch in $windows_archs)
{
    Write-Output "building for windows/$($windows_arch) free version..."
    $env:GOOS="windows";$env:GOARCH=$windows_arch; go build -tags free -o
    .\builds\free\windows\$windows_arch\audiofile.exe main.go
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating a bash script to compile in Darwin or Linux" / "Creating a PowerShell script in Windows"*

---

### 81 — Mock the HTTP client behind one method `#testing` `#api`
**Principle:** Unit tests should not depend on live API availability.
**Code:**
```go
type AudiofileClient interface {
    Do(req *http.Request) (*http.Response, error)
}
var (
    getClient = GetHTTPClient()
)
func GetHTTPClient() AudiofileClient {
    return &http.Client{Timeout: 15 * time.Second}
}
type ClientMock struct {}
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
    }
    return &http.Response{}, nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Mocking the HTTP client"*

---

### 82 — Initialize test state explicitly `#testing`
**Principle:** Each test needs predictable client, Viper, and logger state.
**Code:**
```go
var Logger *zap.Logger
var Verbose *zap.Logger
func ConfigureTest() {
    getClient = &ClientMock{}
    viper.SetDefault("cli.hostname", "testHostname")
    viper.SetDefault("cli.port", 8000)
    utils.InitCLILogger()
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Handling test configuration"*

---

### 83 — Drive Cobra through real argument vectors `#testing` `#cli`
**Principle:** Test command parsing, flags, output, and errors through `SetArgs` and `Execute`.
**Code:**
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

---

### 84 — Cover success and failure paths `#testing`
**Principle:** A command is not covered until expected failures are asserted.
**Do:** Test missing files, successful uploads, unknown IDs, missing flags, malformed values, and successful retrieval.
**Don't:** Treat a passing happy-path test as proof of the command contract.
**Code:**
```go
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        p := &Parser{commands: tt.fields.commands}
        if err := p.Parse(tt.args.args); (err != nil)
          != tt.wantErr {
            t.Errorf("Parser.Parse() error = %v,
              wantErr %v", err, tt.wantErr)
        }
    })
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Testing and mocking"*

---

### 85 — Separate integration tests with tags and containers `#testing` `#systems`
**Principle:** Keep external workflows explicit and exercise command-to-API-to-storage behavior.
**Code:**
```go
//go:build int && pro
```
```go
ConfigureTest()
rootCmd.SetArgs([]string{"upload", "--filename",
  "../audio/algorithms.mp3"})
err := rootCmd.Execute()
if err != nil { fmt.Println("err: ", err) }
uploadResponse, err := ioutil.ReadAll(b)
id := string(uploadResponse)
if id == "" { t.Fatalf("expected id returned") }
rootCmd.SetArgs([]string{"get", "--id", id, "--json"})
err = rootCmd.Execute()
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Creating the integration test file" / "Writing the integration tests"*

---

### 86 — Use containers when consistency outweighs complexity `#systems` `#distribution`
**Principle:** Containers bundle code and dependencies, isolate environments, and make CI and distribution repeatable.
**Do:** Use them for integration tests, reproducible builds, versioning, and registry distribution.
**Don't:** Ignore Docker's external dependency, shared-kernel security model, or operational overhead.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Why use containers?" / "Deciding not to use containers"*

---

### 87 — Build and run explicit Docker images `#distribution`
**Principle:** Define the base image, source copy, build command, and executable command in a Dockerfile.
**Code:**
```dockerfile
FROM golang:1.19
WORKDIR /app
COPY . .
RUN go build -o audiofile cmd/cli/main.go
CMD ["./audiofile"]
```
```text
docker build --tag hello-world:latest
docker run --rm hello-world:latest
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Building a simple Docker image" / "Running a simple Docker container"*

---

### 88 — Compose API and CLI integration services `#testing` `#distribution`
**Principle:** Put the API and CLI test roles in one Compose file.
**Code:**
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
**Don't:** Assume mocks prove the whole API/filesystem workflow.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Writing the Docker Compose file"*

---

### 89 — Map volumes when state must persist `#systems` `#distribution`
**Principle:** A disposable container filesystem is not host persistence.
**Code:**
```text
docker run -p 8000:8000 --rm -v $HOME/audiofile:/root/audiofile audiofile:api
```
```yaml
volumes:
  - "${HOME}/audiofile:/root/audiofile"
```
**Do:** Explain host-path to container-path mapping and its persistence effect.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Mapping host machine to container file paths"*

---

### 90 — Use multi-stage builds for small runtime images `#distribution` `#performance`
**Principle:** Build with Go, then copy only the binary into the final runtime image.
**Code:**
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
**Don't:** Ship the full Go toolchain as the runtime image when the binary is sufficient.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Reducing image size by using multi-stage builds"*

---

### 91 — Distribute container images with instructions `#distribution`
**Principle:** Tag, push, version, and document the exact run command.
**Code:**
```text
docker tag audiofile:dist marianmontagnino/audiofile:latest
docker push marianmontagnino/audiofile:latest
docker run --rm --network host -ti marianmontagnino/audiofile:latest help
```
**Do:** Publish to a registry and explain volumes, network mode, and TTY requirements.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Distributing your Docker image"*

---

### 92 — Automate releases with GoReleaser `#distribution` `#cross-platform`
**Principle:** A tag should drive build, packaging, checksum, changelog, release, and Homebrew publication.
**Do:** Initialize with `goreleaser init` and validate with `goreleaser release --snapshot --clean`.
**Don't:** Make every platform release a manual process.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "GoReleaser workflow" / "Configuring your project to use GoReleaser"*

---

### 93 — Configure hooks, builds, and release flags `#distribution`
**Principle:** Put deterministic preparation and feature selection in the release configuration.
**Code:**
```yaml
before:
  hooks:
    - go mod tidy
    - go generate ./...
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
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Global hooks" / "Builds and environment variables"*

---

### 94 — Package archives, checksums, snapshots, and changelogs `#distribution`
**Principle:** Release artifacts must be identifiable, verifiable, and understandable.
**Code:**
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

---

### 95 — Publish Homebrew formulas through a tap `#distribution` `#cli`
**Principle:** A separate tap repository gives users a simple package-manager install path.
**Code:**
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
```text
brew tap marianina8/audiofile
brew install marianina8/audiofile/audiofile
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Brews" / "Installing with Homebrew and Testing"*

---

### 96 — Trigger GitHub Actions from tags with least privilege `#distribution`
**Principle:** Fetch full history, grant needed contents write access, and run GoReleaser on pushed tags.
**Code:**
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
**Don't:** Use a shallow checkout or grant package/issues permissions without a requirement.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "On" / "Permissions" / "Jobs"*

---

### 97 — Rewrite errors as a user-facing contract `#cli` `#ux`
**Principle:** Say what failed, why, and what to do next without blaming the user.
**Do:** Be specific, human, light-hearted only when appropriate, concise, consistently punctuated, and visible at the end of output.
**Don't:** Print raw low-level errors or repeated stack traces as the normal experience.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Guidelines for writing error messages"*

---

### 98 — Wrap and customize errors `#cli` `#error-handling`
**Principle:** Preserve causal context while adding task and severity information when it is useful.
**Code:**
```go
err1 := errors.Wrap(err, "operation1")
err2 := errors.Wrap(err1, "operation2")
err3 := errors.Wrap(err2, "operation3")
type customError struct {
    Task string
    Err error
}
func (e *customError) Error() string {
    var errorColor = color.New(color.BgRed, color.FgWhite).SprintFunc()
    return fmt.Sprintf("%s: %s %s", errorColor(e.Task), crossMark, e.Err)
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Decorating errors" / "Customizing errors"*

---

### 99 — Rewrite HTTP statuses with actionable language `#api` `#cli`
**Principle:** Translate transport details into the next useful action.
**Code:**
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

---

### 100 — Use Zap for structured verbose diagnostics `#observability`
**Principle:** Keep normal UX concise and make debug, request, response, and stack data available through configured logging.
**Code:**
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
func Error(errString string, err error, verbose bool) error {
    errString = cleanup(errString, err)
    if err != nil {
        if verbose { Verbose.Error(errString) } else { Logger.Error(errString) }
        return fmt.Errorf(errString)
    }
    return nil
}
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Initiating a logger" / "Implementing a logger"*

---

### 101 — Make bug reporting and documentation reachable `#cli` `#ux`
**Principle:** A bug command and generated man pages shorten the path from failure to support.
**Code:**
```go
var buf bytes.Buffer
buf.WriteString(fmt.Sprintf("**Audiofile version**\n%s\n\n", utils.Version()))
buf.WriteString(description)
buf.WriteString(toReproduce)
buf.WriteString(expectedBehavior)
buf.WriteString(additionalDetails)
body := buf.String()
url := "https://github.com/marianina8/audiofile/issues/new?title=Bug Report&body=" + url.QueryEscape(body)
if !openBrowser(url) { fmt.Print(body) }
```
```go
header := &doc.GenManHeader{Title: "Audiofile", Source: "Auto generated by marianina8"}
doc.GenManTree(cmd.RootCMD(), header, "./pages")
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Effortless bug submission" / "Generating man pages"*

---

### 102 — Write empathetic documentation `#cli` `#ux`
**Principle:** Documentation must account for readers who are tired, frustrated, confused, or short on cognitive capacity.
**Do:** Use visual storytelling, synopses, time frames, short videos, fewer screenshots, single-scoped documents, and deliberate priorities.
**Don't:** Use dense text and sprawling FAQs as the only recovery path.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Embedding empathy into your documentation"*

---

### 103 — Use survey controls that match answers `#cli` `#ux`
**Principle:** Text, select, multiselect, multiline, password, and confirmation each communicate a different answer shape.
**Code:**
```go
questions := []*survey.Question{
    {
        Name: "email",
        Prompt: &survey.Input{Message: "What is your email address?"},
        Validate: survey.Required,
        Transform: survey.Title,
    },
    {
        Name: "rating",
        Prompt: &survey.Select{
            Message: "How would you rate your experience with the CLI?",
            Options: []string{"Hated it", "Disliked", "Decent", "Great", "Loved it"},
        },
    },
    {
        Name: "issues",
        Prompt: &survey.MultiSelect{
            Message: "Have you encountered any of these issues?",
            Options: []string{"audio player issues", "upload issues", "search issues", "other technical issues"},
        },
    },
    {
        Name: "suggestions",
        Prompt: &survey.Multiline{Message: "Please provide any other feedback or suggestions you may have."},
    },
}
results := struct { Email string; Rating string; Issues []string; Suggestions string }{}
err := survey.Ask(questions, &results)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Guiding users with prompts"*

---

### 104 — Organize terminal dashboards by layers `#cli` `#systems`
**Principle:** Termdash separates terminal cells, infrastructure, containers, and widgets.
**Do:** Use `tcell` for the terminal, infrastructure for redraws and events, containers for layout, and widgets for information and action.
**Don't:** Put every terminal concern into one untestable function.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Learning about Termdash"*

---

### 105 — Initialize, redraw, and close a dashboard deliberately `#cli` `#performance`
**Principle:** A dashboard needs bounded lifetime and explicit refresh behavior.
**Code:**
```go
t, err := tcell.New(tcell.ColorMode(terminalapi.ColorMode256))
if err != nil { return err }
defer t.Close()
c, err := container.New(t)
if err != nil { return err }
ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
defer cancel()
if err := termdash.Run(ctx, t, c, termdash.RedrawInterval(100*time.Millisecond)); err != nil {
    panic(err)
}
```
**Don't:** Let runtime errors panic without an error handler.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The infrastructure layer" / "Implementing a terminal dashboard"*

---

### 106 — Use events and containers as explicit dashboard contracts `#cli`
**Principle:** Keyboard events, layout splits, focus, margin, and padding should be named operations.
**Code:**
```go
quitter := func(k *terminalapi.Keyboard) {
    if k.Key == 'q' || k.Key == 'Q' { cancel() }
}
containerLayer, err := container.New(
    t,
    container.SplitVertical(
        container.Left(),
        container.Right(
            container.SplitHorizontal(
                container.Top(),
                container.Bottom(),
                container.SplitPercent(60),
            ),
        ),
    ),
)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The container layer" / "Subscribing to keyboard events"*

---

### 107 — Choose widgets by information need `#cli` `#ux`
**Principle:** Text, input, buttons, bar charts, donuts, and gauges each make a different state legible.
**Code:**
```go
barChart, err := barchart.New()
if err != nil { return err }
values := []int{20, 40, 60, 80, 100}
max := 100
if err := barChart.Values(values, max); err != nil { return err }
progressGauge, err := gauge.New(
    gauge.Height(1), gauge.Border(linestyle.Light), gauge.BorderTitle("Percentage progress"),
)
if err != nil { return err }
progressGauge.Percent(75)
```
*Ref: Building_Modern_CLI_Applications_in_Go.md — "The widget layer"*

---

### 108 — Disable interactivity outside a TTY `#cli` `#systems`
**Principle:** Prompts, dashboards, animations, and progress displays must not block scripts or CI.
**Do:** Check TTY status and retain non-interactive flags and output modes.
**Don't:** Start `survey`, Termdash, a spinner, or a pager when the destination is a pipe.
*Ref: Building_Modern_CLI_Applications_in_Go.md — "Interactivity with Prompts and Terminal Dashboards"*

---

## Anti-Patterns & Common Mistakes

- **Ambiguous commands:** `update` and `upgrade` leave users guessing → *fix:* choose one clear verb.
- **Opaque help:** users must search the web for basic usage → *fix:* generate concise help and examples.
- **Single-letter flags everywhere:** shorthand collisions grow → *fix:* provide long forms.
- **Prompt-only workflows:** scripts hang → *fix:* preserve flags and gate prompts on TTY.
- **Unbounded reads:** large files exhaust memory → *fix:* stream chunks or scanner tokens.
- **Shell assumptions:** `os/exec` does not expand pipes or globs → *fix:* use explicit expansion or safe shell invocation.
- **Skipped `Wait`:** child resources remain held → *fix:* pair `Start` and `Wait`.
- **HTTP status blindness:** 4xx/5xx is not a Go error → *fix:* inspect status and body.
- **No HTTP timeout:** requests hang → *fix:* configure `http.Client.Timeout`.
- **No rate limit:** public API limits are exceeded → *fix:* use `x/time/rate`.
- **Raw stack traces:** users cannot tell what to do → *fix:* rewrite and reserve traces for verbose mode.
- **Colors in pipes:** machine output is polluted → *fix:* honor TTY, `NO_COLOR`, `TERM=dumb`, and `--no-color`.
- **Silent success:** users cannot tell whether work happened → *fix:* print briefly or support quiet mode.
- **Live API tests:** tests depend on the network → *fix:* inject a mock client.
- **Only happy-path tests:** failure behavior is unknown → *fix:* test missing files, IDs, flags, and statuses.
- **Single-stage images:** runtime includes the toolchain → *fix:* multi-stage Docker builds.
- **Unmapped container state:** data disappears → *fix:* document and use volumes.
- **Shallow release checkout:** tags and changelog history are missing → *fix:* use `fetch-depth: 0`.
- **Unverifiable artifacts:** downloads cannot be checked → *fix:* publish checksums.

---

## Decision Heuristics / Checklists

### Foundation
- [ ] Is the name lowercase, short, memorable, and easy to type?
- [ ] Does bare invocation print help?
- [ ] Are `-h` and `--help` available?
- [ ] Are successes zero and failures non-zero?
- [ ] Is invalid input rejected before side effects?

### Structure
- [ ] Is a flat structure still sufficient?
- [ ] Are functional groups and initialization clear?
- [ ] Are modules cohesive without circular dependencies?
- [ ] Are ports interfaces and adapters concrete?
- [ ] Are use cases separated from implementation details?
- [ ] Are security, capacity, compatibility, reliability, maintainability, scalability, usability, performance, and environment requirements recorded?

### Input
- [ ] Are flags used where positional values would be brittle?
- [ ] Does every common shorthand have a long form?
- [ ] Are persistent and local flags scoped correctly?
- [ ] Is stdin supported where composition helps?
- [ ] Are relevant signals handled?
- [ ] Are prompts and confirmations TTY-gated and danger-scaled?

### Files, processes, and APIs
- [ ] Is the file-reading strategy matched to size and record shape?
- [ ] Is every `Cmd` newly constructed?
- [ ] Is `Start` paired with `Wait`?
- [ ] Are stdout, stderr, and extra descriptors intentional?
- [ ] Is the HTTP client timed out?
- [ ] Are query values escaped and response bodies closed?
- [ ] Are status codes checked independently of Go errors?
- [ ] Are pagination and rate limits explicit?

### Output and errors
- [ ] Is TTY status detected on supported platforms?
- [ ] Are `--plain`, `--json`, `--quiet`, and `--no-color` available where useful?
- [ ] Are colors and animations disabled for pipes and `TERM=dumb`?
- [ ] Is output concise but not silent?
- [ ] Are errors specific, actionable, and non-blaming?
- [ ] Does verbose mode expose safe structured diagnostics?
- [ ] Are man pages, examples, and bug submission reachable?

### Cross-platform
- [ ] Are paths built with `filepath`?
- [ ] Are OS-specific commands isolated?
- [ ] Are build constraints placed once at the top?
- [ ] Are feature, profile, and integration tags tested?
- [ ] Are `GOOS`, `GOARCH`, and cgo support known for every artifact?

### Testing
- [ ] Is the HTTP client behind a minimal interface?
- [ ] Are mock responses fixture-driven?
- [ ] Are Viper defaults and loggers initialized?
- [ ] Are Cobra commands tested via `SetArgs` and `Execute`?
- [ ] Are success and failure paths covered?
- [ ] Are integration tests tagged and containerized?

### Distribution
- [ ] Does the final Docker image contain only runtime necessities?
- [ ] Are transient containers run with `--rm`?
- [ ] Are volumes and network behavior documented?
- [ ] Does GoReleaser build all supported targets?
- [ ] Are archives, checksums, snapshots, changelogs, and pre-releases configured?
- [ ] Is the Homebrew tap configured?
- [ ] Does GitHub Actions fetch full history and use the required token?
- [ ] Has Homebrew installation and a real command been tested?

---

## Key Takeaways

1. Build small, modular, composable programs that respect streams, signals, and exit codes.
2. Design for humans first and make machine-readable output explicit and stable.
3. Start with the simplest structure and let domain complexity justify modules or ports and adapters.
4. Define use cases and non-functional requirements before binding behavior to flags or endpoints.
5. Use Cobra for growing command trees and Viper for layered configuration.
6. Treat stdin, signals, prompts, and TTY status as separate input and interaction modes.
7. Match file reads to data shape and use process and HTTP timeouts at every external boundary.
8. Check both Go errors and HTTP statuses; rate-limit external APIs.
9. Isolate platform code with standard packages, build tags, `GOOS`, and `GOARCH`.
10. Make errors, logs, help, man pages, and bug submission part of the user experience.
11. Test commands through their real argument boundary with mocked clients and explicit failure cases.
12. Use containers for reproducibility, multi-stage builds for small images, and GoReleaser plus Homebrew for repeatable releases.
13. Disable prompts, animation, dashboards, and decoration when no human TTY is present.
14. Write documentation for users who are uncertain, rushed, or frustrated.

## Cross-References

- Related: [[../INDEX.md]]
- Topic index: [[../INDEX.md]]
