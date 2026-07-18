# Learning eBPF: Programming the Linux Kernel for Enhanced Observability, Networking, and Security

**Author:** Liz Rice
**Published:** March 2023, O'Reilly Media

---

## Chapter 1: What Is eBPF, and Why Is It Important?

eBPF is a revolutionary kernel technology that allows developers to write custom code loaded dynamically into the Linux kernel, fundamentally changing how the kernel behaves at runtime. It enables a new generation of high-performance networking, observability, and security tools without requiring modifications to applications or the kernel itself.

### Roots in the Berkeley Packet Filter

eBPF descends from the BSD Packet Filter, first described in a 1993 paper by Steven McCanne and Van Jacobson at Lawrence Berkeley National Laboratory. The original BPF was a pseudomachine that ran filter programs -- small programs written in a 32-bit instruction set that closely resembled assembly language -- to determine whether to accept or reject network packets. BPF was introduced to Linux in kernel version 2.1.75 (1997), primarily used in the tcpdump utility.

In 2012, seccomp-bpf (kernel 3.5) extended BPF beyond packet filtering to making decisions about allowing or denying user space system calls, marking the first step in evolving BPF from a narrow packet filter into a general-purpose platform.

### From BPF to eBPF

The transformation to "extended BPF" began in kernel version 3.18 (2014) with several significant changes: the instruction set was overhauled for 64-bit machines, eBPF maps were introduced for data sharing between kernel and user space, the bpf() system call was added, BPF helper functions were introduced, and the eBPF verifier was created to ensure program safety.

By 2016, eBPF-based tools were running in production. Brendan Gregg's tracing work at Netflix demonstrated eBPF's "superpowers," while Cilium became the first networking project to use eBPF to replace the entire datapath in container environments. Facebook (Meta) open-sourced Katran, a layer 4 load balancer, and every packet to Facebook.com since 2017 has passed through eBPF/XDP.

In 2018, eBPF became a separate kernel subsystem with its own maintainers (Daniel Borkmann and Alexei Starovoitov), and BPF Type Format (BTF) was introduced for portability. The year 2020 saw LSM BPF, enabling eBPF programs on the Linux Security Module interface, establishing security as the third major use case alongside networking and observability.

### The Linux Kernel and eBPF's Advantages

The Linux kernel sits between applications and hardware. Applications in user space use the system call interface to request kernel operations -- file I/O, networking, memory access. The kernel coordinates concurrent processes. Because applications rely so heavily on the kernel, instrumenting the kernel with eBPF provides visibility into all application behavior.

Adding functionality to the kernel traditionally required modifying kernel source code (a slow process taking years to reach production) or writing kernel modules (risky because kernel code crashes take down the entire machine). eBPF offers a fundamentally different approach: programs can be loaded and removed dynamically, attach to events instantly, and are verified safe by the eBPF verifier before execution.

In cloud native environments, all containers on a Kubernetes node share the same kernel. eBPF programs loaded into that kernel gain visibility over all containerized workloads simultaneously, without modifying applications, restarting processes, or injecting sidecars. This eliminates the downsides of the sidecar model (pod restarts, YAML modification, startup race conditions, added latency from proxy containers).

eBPF programs run as native machine instructions after JIT compilation, avoiding expensive kernel-to-user-space transitions for each event. XDP (eXpress Data Path) provides 2.5x performance improvement for routing and 4.3x for load balancing compared to traditional kernel implementations.

---

## Chapter 2: eBPF's "Hello World"

The chapter introduces practical eBPF programming through the BCC (BPF Compiler Collection) Python framework, which provides the most accessible entry point for beginners.

### BCC's "Hello World"

A minimal BCC-based eBPF application consists of two parts: the eBPF program (written in C, running in the kernel) and user space code (Python) that loads and interacts with it. The example attaches to the execve syscall via a kprobe and prints "Hello World" each time a new program executes. BCC handles compilation, loading, and attachment behind the scenes.

Key concepts demonstrated:
- **Helper functions** like `bpf_trace_printk()` allow eBPF programs to interact with the system
- **Event attachment** -- eBPF programs must be attached to an event (kprobes, tracepoints, XDP events, etc.)
- **Dynamic loading** -- as soon as an eBPF program is attached, it triggers for preexisting processes
- **Privileges** -- eBPF requires root or specific capabilities (CAP_BPF, CAP_PERFMON, CAP_NET_ADMIN)

### BPF Maps

Maps are data structures accessible from both eBPF programs and user space -- a defining feature of extended BPF. They serve several purposes: user space writing configuration for eBPF programs, eBPF programs storing state, and eBPF programs sending results to user space.

Map types include hash tables, arrays, perf/ring buffers, queues, stacks, LRU caches, longest-prefix matching tables, Bloom filters, sockmaps, devmaps, and program arrays. Per-CPU variants exist for concurrent access without locking.

The chapter demonstrates a hash table map example that counts execve calls per user ID, showing how the eBPF program uses `bpf_get_current_uid_gid()` and `bpf_map_lookup_elem()` helpers, while the Python code periodically polls the map.

### Perf and Ring Buffer Maps

Perf buffers (and their successor, BPF ring buffers from kernel 5.8) provide efficient event-driven data passing from kernel to user space. Ring buffers are logically circular memory with separate read and write pointers. Data written at the write pointer includes length headers; if write overtakes read, a drop counter increments.

The chapter shows a more sophisticated example using `BPF_PERF_OUTPUT` that sends structured data (PID, UID, command, message) through a dedicated ring buffer rather than the shared trace pipe. Ring buffers are preferred over perf buffers for their single-buffer-per-core-set design, preserved ordering guarantees, and use of epoll instead of ppoll.

### Function Calls and Tail Calls

Early eBPF required all functions to be inlined. Since kernel 4.16 / LLVM 6.0, BPF-to-BPF function calls ("BPF subprograms") are supported. Tail calls use `bpf_tail_call()` to replace the current program with another eBPF program (stored in a program array map), similar to how `execve()` replaces a process. Tail calls avoid stack growth and are critical given eBPF's 512-byte stack limit. Up to 33 tail calls can be chained, and combined with the 1-million-instruction limit per program, this provides substantial programming headroom.

---

## Chapter 3: Anatomy of an eBPF Program

This chapter traces an eBPF program's journey from C source code through eBPF bytecode to native machine code, using a pure C/libbpf approach (without BCC's abstractions).

### The eBPF Virtual Machine

The eBPF VM is a software implementation that takes eBPF bytecode instructions and converts them to native machine code. Early implementations interpreted bytecode at runtime; modern kernels use JIT (just-in-time) compilation for performance and to mitigate Spectre-related vulnerabilities in the interpreter.

### eBPF Registers and Instructions

The eBPF VM uses 10 general-purpose registers (R0-R9) plus R10 as a read-only stack frame pointer. The context argument is loaded into R1 before execution; the return value is stored in R0. Function arguments are placed in R1-R5.

Each instruction is represented by an 8-byte `bpf_insn` structure containing opcode, destination/source register fields, offset, and immediate value. Wide (16-byte) instruction encoding handles cases where a 64-bit immediate value is needed. Instructions fall into categories: loading values into registers, storing values to memory, arithmetic operations, and conditional jumps.

### Compilation, Loading, and Inspection

eBPF C source code is compiled with Clang using `-target bpf` to produce ELF object files. The `llvm-objdump` tool shows the resulting eBPF bytecode. The `bpftool` utility loads programs into the kernel, pins them to the BPF filesystem (`/sys/fs/bpf/`), and inspects loaded programs showing IDs, types, names, tags (SHA hashes of instructions), license info, and byte counts for translated and JIT-compiled code.

The translated bytecode (post-verifier) and JIT-compiled machine code can both be dumped using bpftool. The example walks through an XDP "Hello World" program, showing how global variables are implemented using maps (`.bss` for uninitialized data, `.rodata` for read-only constants).

### BPF-to-BPF Calls

The chapter demonstrates a function call within eBPF bytecode: the `call` instruction (opcode 0x85) jumps to a subprogram, and the subprogram's `exit` instruction returns control. The calling program's state is saved on the eBPF stack, limiting call nesting depth due to the 512-byte stack.

---

## Chapter 4: The bpf() System Call

This chapter examines the system call interface that user space programs use to interact with eBPF programs and maps in the kernel.

### The bpf() Syscall

```c
int bpf(int cmd, union bpf_attr *attr, unsigned int size);
```

The `cmd` argument specifies the operation (BPF_PROG_LOAD, BPF_MAP_CREATE, BPF_MAP_UPDATE_ELEM, etc.). The `attr` structure holds command-specific parameters, and `size` indicates its byte count.

### Key Operations Traced via strace

Using `strace -e bpf` on a BCC example, the chapter reveals the syscall sequence:

1. **BTF loading** (`BPF_BTF_LOAD`): Loads BPF Type Format data for portability and pretty-printing
2. **Map creation** (`BPF_MAP_CREATE`): Creates perf event array and hash table maps, returning file descriptors
3. **Program loading** (`BPF_PROG_LOAD`): Loads bytecode into the kernel with program type, instruction count, license, and BTF reference. Returns a file descriptor on success or negative on verification failure
4. **Map updates** (`BPF_MAP_UPDATE_ELEM`): User space writes key-value pairs into maps

### Reference Counting and Pinning

The kernel tracks references to BPF programs and maps via file descriptors. When a user space process exits, its file descriptors are released and reference counts decremented. Objects are removed when reference counts reach zero.

**Pinning** creates additional references by storing objects in the `/sys/fs/bpf/` pseudo-filesystem, allowing programs to persist after the loading process exits. **BPF links** provide an abstraction layer between programs and events, also pinnable for persistent references.

### Attaching to Events

Attachment mechanisms vary by program type. For kprobes, the process involves `perf_event_open()` to create an event file descriptor, then `ioctl(PERF_EVENT_IOC_SET_BPF)` to attach the eBPF program, and `ioctl(PERF_EVENT_IOC_ENABLE)` to activate it. For raw tracepoints, a simpler `bpf(BPF_RAW_TRACEPOINT_OPEN)` suffices.

### Perf and Ring Buffer Setup

Perf buffers require one buffer per CPU core (four `perf_event_open` calls on a four-core machine). Ring buffers use a single shared buffer across all cores with epoll-based notification, making them simpler and more efficient.

---

## Chapter 5: CO-RE, BTF, and Libbpf

This chapter addresses the critical portability challenge: eBPF programs accessing kernel data structures that may differ between kernel versions.

### BCC's Approach to Portability

BCC compiles eBPF code at runtime on the destination machine, ensuring compatibility with local kernel headers. This has significant drawbacks: requiring compiler toolchains and kernel headers on every target, start-up compilation delays, wasted compute across identical fleet machines, and unsuitability for embedded devices.

### CO-RE (Compile Once, Run Everywhere)

CO-RE solves portability through several components:

1. **BTF (BPF Type Format)**: Describes data structure layouts and function signatures. Used to determine differences between compile-time and runtime structures. Available in kernels 5.4+.
2. **Kernel headers**: `bpftool btf dump file /sys/kernel/btf/vmlinux format c` generates a `vmlinux.h` file containing all kernel data type definitions.
3. **Compiler support**: Clang (with `-g` flag) emits CO-RE relocation entries alongside bytecode. GCC added support in version 12.
4. **Library relocation**: libbpf (C), cilium/ebpf (Go), and Aya (Rust) adjust bytecode during loading to account for structure layout differences.
5. **BPF skeletons**: Auto-generated code from bpftool providing convenient lifecycle management functions.

### BTF in Practice

BTF encodes type information including structures (with field offsets and sizes), typedefs, integers, arrays, function prototypes, and function definitions. Each type has an ID and references other types by ID. The chapter walks through BTF output showing how `u32`, `user_msg_t`, and map key-value types are described.

BTF enables pretty-printing of map contents, interleaving source code with bytecode dumps, and BPF spin locks. Maps include BTF type IDs for keys and values in their creation parameters.

### Writing CO-RE Programs with libbpf

CO-RE eBPF programs include `vmlinux.h` for kernel types, `bpf/bpf_helpers.h` for helper functions, `bpf/bpf_core_read.h` for portable memory access, and application-specific headers for shared structures.

Maps are defined using `SEC(".maps")` with `__uint` and `__type` macros. Program sections like `SEC("ksyscall/execve")` tell libbpf both the program type and attachment point.

Memory access uses `bpf_core_read()` (wrapping `bpf_probe_read_kernel()` with `__builtin_preserve_access_index()` for CO-RE relocations) and the `BPF_CORE_READ()` macro for chained pointer dereferences.

Compilation requires `-target bpf`, `-g` for debug/BTF info, `-O2` for verifier-compatible bytecode, and `-D __TARGET_ARCH_*` for architecture-specific macros. DWARF debug info can be stripped with `llvm-strip -g` to reduce object size.

### BPF Relocations

During loading, libbpf compares the program's BTF data against the target kernel's BTF (`vmlinux`). For each instruction accessing a structure field, the `bpf_core_relo` structure records the instruction offset, BTF type ID, access path, and relocation kind. If field offsets differ between compile-time and runtime kernels, libbpf patches the bytecode instructions accordingly.

### User Space with BPF Skeletons

`bpftool gen skeleton` auto-generates C header files containing structures for all maps and programs, lifecycle functions (`open`, `load`, `attach`, `destroy`), and the embedded ELF bytecode bytes. The user space program calls skeleton functions to open/load/attach, sets up perf or ring buffer polling with callback functions, and handles cleanup on exit.

---

## Chapter 6: The eBPF Verifier

The verifier is perhaps the most important characteristic distinguishing eBPF from kernel modules. It ensures programs are safe to run before they are loaded into the kernel.

### Verification Process

The verifier analyzes all possible execution paths through the program, tracking register states in `bpf_reg_state` structures. Each register has a type (`NOT_INIT`, `SCALAR_VALUE`, `PTR_TO_CTX`, `PTR_TO_PACKET`, `PTR_TO_MAP_VALUE`, etc.) and a tracked range of possible values.

At branches, the verifier pushes state onto a stack and explores each path. It processes up to one million instructions per program. State pruning optimizations avoid reevaluating equivalent paths by recording register states at intervals and matching against them.

### Verifier Log

When verification fails, the log shows the instruction sequence, source code lines (if compiled with `-g`), and register state information including types and value ranges. The log ends with a summary showing instructions processed, states stored, and peak states.

### Key Verification Checks

**Validating helper functions**: Only helper functions appropriate for the program type are permitted. For example, `bpf_get_current_pid_tgid()` is not allowed in XDP programs because no user space process is involved when a network packet arrives.

**Helper function arguments**: The verifier checks that arguments match expected types (map pointer vs. frame pointer vs. context pointer) using `bpf_func_proto` structures that define each helper's argument constraints.

**License checking**: GPL-only helper functions require GPL-compatible program licenses.

**Memory access**: Programs cannot access memory beyond defined bounds. XDP programs must check packet boundaries (`data` to `data_end`). Array accesses require explicit bounds checking (the verifier catches off-by-one errors). Pointer arithmetic on `pkt_end` is prohibited.

**Null pointer checking**: All pointers must be checked for null before dereferencing. The return from `bpf_map_lookup_elem()` may be null, and the verifier rejects code that dereferences it without an explicit null check.

**Running to completion**: The verifier enforces the one-million-instruction limit to prevent infinite loops. Loops were prohibited entirely before kernel 5.3; now bounded loops are accepted if the verifier can confirm they complete within limits. The `bpf_loop()` helper (kernel 5.17) provides efficient verified looping by validating the loop body function only once.

**Return code checking**: Register 0 must be initialized (it holds the return value). Unreachable instructions are rejected.

---

## Chapter 7: eBPF Program and Attachment Types

There are approximately 30 program types and over 40 attachment types, each defining what events programs attach to, what context they receive, what helper functions they can call, and what their return codes mean.

### Program Context and Constraints

Each program type receives a different context structure. The verifier ensures context is handled appropriately for the type. Helper functions and return code meanings are type-specific. Kfuncs allow internal kernel functions to be registered for eBPF use, but without compatibility guarantees.

### Tracing Program Types

**Kprobes/Kretprobes**: Attach to almost any kernel function entry/exit point. Kprobes at syscall entry points use `BPF_KPROBE_SYSCALL` for typed parameter access. Kprobes at internal kernel functions use `BPF_KPROBE`. Kretprobes capture return values but not input parameters. Functions may be inlined by the compiler, making them unavailable for kprobe attachment.

**Fentry/Fexit**: More efficient than kprobes (introduced kernel 5.5 with BPF trampoline). Fexit programs have access to both input parameters and return values, unlike kretprobes. Uses `BPF_PROG` macro for typed parameters.

**Tracepoints**: Stable kernel hooks defined in `/sys/kernel/tracing/available_events` (1,400+ on kernel 5.15). Context structure must match the tracepoint format. BTF-enabled tracepoints (`tp_btf`) use auto-generated structures from `vmlinux.h`.

**Raw tracepoints**: More performant variant that receives raw `__u64` arguments instead of pre-mapped structures.

**User space attachments**: Uprobes/uretprobes attach to user space function entry/exit. USDTs (User Statically Defined Tracepoints) attach to tracepoints in application code. These use the same BPF_PROG_TYPE_KPROBE type.

**LSM**: BPF_PROG_TYPE_LSM programs attach to the Linux Security Module interface. Unlike other tracing types, LSM programs can influence kernel behavior -- nonzero return codes block the security-checked operation.

### Networking Program Types

Networking programs process packets at various points in the network stack. They can observe, modify, drop, or redirect packets, and set socket parameters. Key types include:

- **Socket filter** (BPF_PROG_TYPE_SOCKET_FILTER): Filters copies of socket data for observability
- **Socket operations** (BPF_PROG_TYPE_SOCK_OPS): Intercepts socket operations, sets TCP parameters
- **Sockmap** (BPF_PROG_TYPE_SK_SKB): Redirects traffic at the socket layer
- **Traffic Control (TC)**: Custom classifiers and filters for ingress/egress traffic, supporting multiple chained programs
- **XDP**: Processes packets at the earliest point upon arrival at a network interface. Supports multiple program types for different NICs
- **Flow dissector**: Custom packet header parsing
- **Lightweight tunnels**: Network encapsulation
- **Cgroup programs**: Per-cgroup networking and sysctl policies

### BPF Attachment Types

Attachment types provide finer-grained control over where programs attach. Some program types have a one-to-one mapping to attachment points; others require explicit attachment type specification. The attachment type affects valid helper functions and accessible context fields.

---

## Chapter 8: eBPF for Networking

Networking is one of eBPF's most impactful application areas, enabling firewalling, DDoS protection, load balancing, traffic encryption, and Kubernetes networking at massive scale.

### Packet Drops with XDP

XDP programs receive packets immediately upon arrival at a network interface. Return codes determine packet fate: `XDP_PASS` (normal processing), `XDP_DROP` (discard), `XDP_TX` (send back out same interface), `XDP_REDIRECT` (send to different interface), `XDP_ABORTED` (error-case drop).

### XDP Packet Parsing

The `xdp_md` context provides `data` and `data_end` pointers defining the packet in memory. Parsing involves casting to Ethernet header (`struct ethhdr`), then IP header (`struct iphdr`), then Layer 4 headers, with mandatory bounds checks at each level. The `bpf_ntohs()` function handles byte order conversion.

The example demonstrates detecting ICMP ping packets and optionally dropping them -- a simple illustration of firewalling, DDoS protection, and packet-of-death vulnerability mitigation.

### Load Balancing and Forwarding

XDP programs can modify packet contents. The example implements a simple load balancer that randomly distributes TCP traffic between two backend containers. It updates destination IP and MAC addresses in the packet, recalculates the IP header checksum, and returns `XDP_TX` to send the modified packet back out the same interface.

### XDP Offloading

Some network cards support running XDP programs directly on the NIC's processor, meaning dropped or redirected packets never reach the host CPU. Even without full offload, many NIC drivers support XDP hooks that minimize memory copying.

### Traffic Control (TC)

TC programs process packets later in the network stack (after `sk_buff` structure creation), supporting both ingress and egress directions. Multiple eBPF programs can be chained. Return codes include `TC_ACT_OK` (pass), `TC_ACT_SHOT` (drop), `TC_ACT_REDIRECT`, and `TC_ACT_UNSPEC`.

TC is used where egress processing is needed (XDP handles only ingress), where `sk_buff` access is required, or where chained programs are beneficial. The example shows a TC program that intercepts ping requests and generates ping responses by swapping addresses and redirecting cloned packets.

### eBPF and Kubernetes Networking

Cilium uses eBPF to replace iptables-based kube-proxy for Kubernetes service load balancing, achieving significant performance improvements by handling packet routing and load balancing decisions within the kernel at XDP and TC levels. eBPF programs attached at various network stack points implement coordinated networking behavior.

### Packet Encryption and Decryption

eBPF can inspect encrypted traffic by hooking into SSL/TLS libraries (OpenSSL, GnuTLS, NSS) at the user space level. Uprobes attached to functions like `SSL_write()` and `SSL_read()` capture decrypted data before encryption or after decryption. This approach has limitations: it only works for instrumented libraries, and there are TOCTOU (Time Of Check to Time Of Use) considerations.

Transparent encryption between Kubernetes nodes can be implemented using XDP or TC programs to encrypt/decrypt traffic at the kernel level, using protocols like WireGuard or IPsec.

### Network Policy Enforcement

eBPF enables fine-grained network policy enforcement (allowing/denying connections based on identity, labels, DNS names) with lower overhead than iptables. Cilium implements network policies by attaching eBPF programs at TC and XDP hooks that evaluate policy rules for each packet.

---

## Chapter 9: eBPF for Security

Security is the third major use case for eBPF, complementing observability and networking. Security observability tools can see everything happening on a machine, but effective security requires both observability and policy enforcement.

### Security Observability Requires Policy and Context

Simply observing events is insufficient for security. Tools need defined policies specifying what behavior is expected, and contextual information (process identity, binary paths, network connections) to evaluate events against policies.

### Using System Calls for Security Events

System calls are a natural security event source because they represent the boundary between untrusted user space and privileged kernel space. Tools like Falco and Tetragon track syscall events to detect suspicious behavior.

However, syscall-based security has a TOCTOU vulnerability: by the time a kprobe or tracepoint fires at syscall entry, the user space arguments could have been modified by another thread. Raw tracepoints and BTF-enabled tracepoints partially address this.

### Generating Seccomp Profiles

Seccomp (secure computing) restricts the system calls available to a process. eBPF programs can be used to observe actual syscall usage and generate seccomp profiles, providing least-privilege configurations. The example shows recording syscalls used by individual processes to build allowlists.

### BPF LSM (Linux Security Module)

BPF LSM programs attach to the kernel's LSM hooks (introduced kernel 5.7), enabling dynamic security policy enforcement. Unlike other tracing program types, LSM BPF programs can block operations by returning nonzero values. This allows implementing mandatory access controls, file permission checks, and other security policies as eBPF programs that can be loaded and modified dynamically.

### Cilium Tetragon

Tetragon is an eBPF-based security observability and enforcement tool. It attaches eBPF programs to internal kernel functions (not just syscalls), providing deeper visibility into kernel-level operations. It can enforce preventative security policies by blocking operations at the kernel level, including restricting process execution, file access, and network connections based on process identity and security labels.

### Network Security

eBPF-based network security tools enforce policies at the packet level using XDP and TC programs. They can drop packets based on IP/port rules, rate-limit traffic for DDoS protection, implement identity-based access controls (using Kubernetes labels rather than IP addresses), and provide DNS-aware policy enforcement.

---

## Chapter 10: eBPF Programming

This chapter surveys the language and framework options for writing eBPF applications.

### bpftrace

bpftrace is a high-level tracing language for one-liners and short scripts. It abstracts away maps, programs, and compilation, making it ideal for quick performance analysis. Scripts can coordinate multiple eBPF programs across different events (e.g., tracking both entry and exit of syscalls). Built on BCC.

### Language Choices for the Kernel

eBPF bytecode is the compilation target. C (via Clang or GCC) and Rust are the primary languages, as both have compilers supporting eBPF targets. Languages with runtime components (garbage collection, virtual machines) are incompatible with the verifier. Lua has been explored via the XDPLua project.

### BCC Python/Lua/C++

BCC provides a convenient framework where eBPF C code is defined as strings within Python programs, compiled at runtime. BCC preprocesses the code with macros (`BPF_HASH`, `BPF_RINGBUF_OUTPUT`) and provides Python objects representing maps. It handles shared structure definitions between kernel and user space. The main drawback is the runtime compilation requirement.

### C and Libbpf

libbpf provides the modern approach to portable eBPF development. Both LLVM/Clang and GCC (from version 10) support compiling to eBPF. The BCC project has migrated many tools to libbpf-based implementations with significantly lower memory footprints (9 MB vs. 80 MB for opensnoop). The `libbpf-bootstrap` project and `libxdp` library provide starting points.

### Go Libraries

- **ebpf-go** (Cilium): The most popular Go library with ~4,000 GitHub stars. Pure Go implementation with CO-RE support. The `bpf2go` tool generates Go skeleton code from C eBPF source, embedding bytecode into Go binaries. Generates separate files for big-endian and little-endian architectures.
- **libbpfgo** (Aqua Security): Go wrapper around libbpf C code. Uses Go channels for async event handling. Used by Tracee and Parca. Concerns about CGo boundary performance.
- **gobpf** (Iovisor): Original Go implementation, now largely unmaintained.

### Rust Libraries

- **Aya**: Built directly to the syscall level without libbpf dependency. Supports CO-RE relocations and BTF. Uses the Rust compiler directly for both kernel and user space code. Strong emphasis on developer experience with good documentation.
- **libbpf-rs**: Rust wrapper around libbpf. Kernel-side code remains C.
- **Redbpf**: Uses multi-step compilation (Rust to LLVM bitcode to eBPF bytecode). Supports various program types.

### Testing BPF Programs

`BPF_PROG_RUN` allows running eBPF programs from user space for testing (limited to networking-related program types). Enabling `kernel.bpf_stats_enabled` provides runtime statistics (run count, total time) visible through bpftool.

### Multiple eBPF Programs

Real applications typically need multiple eBPF programs attached to different events. For example, opensnoop tracks four syscall tracepoints (entry/exit for open/openat) using maps to coordinate between programs. Libraries like libbpf and ebpf-go generate skeleton code that loads all programs and maps in a single call.

---

## Chapter 11: The Future Evolution of eBPF

### The eBPF Foundation

Established in 2021 by Google, Isovalent, Meta, Microsoft, and Netflix under the Linux Foundation, the eBPF Foundation acts as a neutral body for coordinating eBPF technology development. It focuses on eBPF as a platform and the tooling ecosystem, directed by a technical steering committee including kernel BPF maintainers.

### eBPF for Windows

Microsoft is actively developing eBPF for Windows, with functional demos showing Cilium L4 load balancing and connection tracking. The architecture reuses open source components (libbpf, Clang eBPF support) but implements its own verifier (PREVAIL) and JIT compiler (uBPF) due to licensing constraints. Verification and JIT compilation happen in user space for security. Cross-OS compatibility parallels the challenges of cross-kernel-version portability already addressed by CO-RE.

### Linux eBPF Evolution

eBPF capabilities expand with practically every kernel release. Future developments discussed include:

- **Signed eBPF programs**: Cryptographic verification of program provenance is challenging because CO-RE relocations modify bytecode after compilation, making it difficult to distinguish legitimate adjustments from tampering.
- **Long-lived kernel pointers**: Allowing eBPF programs to store kernel object pointers in maps for use across program invocations.
- **Memory allocation**: eBPF-specific memory allocation mechanisms that work safely within verifier constraints.
- **Big TCP**: Support for 100+ GBit/s networking through packet batching (kernel 5.19).
- **Hardware device support**: Using eBPF for human interface devices, building on existing infrared controller support.

eBPF C language capabilities continue to expand, potentially evolving to allow the flexibility of kernel modules with the safety of verified eBPF programs.

### eBPF Is a Platform, Not a Feature

Most users will not write eBPF code directly but will use tools built on it. eBPF is becoming the de facto technology platform for infrastructure tooling, much as containers (using kernel features like namespaces and cgroups) became part of daily development life. eBPF-based projects and products highlight their use of eBPF because it implies significant advantages in performance, observability, and security.

---

## Key Takeaways

**Architecture and Safety**: eBPF allows safe, dynamic kernel programming through a verifier that checks all possible execution paths before code runs. Programs are JIT-compiled to native machine code for high performance, avoiding kernel-to-user-space transitions for event processing.

**Three Pillars**: eBPF excels in observability (tracing any kernel event with contextual data), networking (high-performance packet processing at XDP, TC, and socket levels), and security (LSM hooks, syscall tracking, network policy enforcement). These use cases leverage eBPF's kernel-level vantage point to see all processes, including containerized workloads, without application modification.

**Portability via CO-RE**: The compile-once-run-everywhere approach, enabled by BTF type information and compiler-emitted relocations, allows eBPF programs compiled on one machine to run on different kernel versions. This is critical for distributing production tools without shipping compiler toolchains.

**Program Lifecycle**: eBPF programs are written in C or Rust, compiled to eBPF bytecode, loaded into the kernel via the bpf() syscall, verified for safety, JIT-compiled to native code, and attached to events. Maps provide shared data structures between kernel programs and user space. Reference counting and pinning manage object lifetimes.

**Verification is Central**: The verifier distinguishes eBPF from dangerous kernel modules by ensuring programs cannot crash the kernel, access invalid memory, dereference null pointers, execute infinite loops, or perform unauthorized operations. Understanding verifier constraints is essential for eBPF programmers.

**Cloud Native Superpower**: In Kubernetes environments, all containers on a node share one kernel. eBPF programs loaded into that kernel instantly gain visibility over all workloads without sidecars, application changes, or pod restarts. This makes eBPF-based tooling more reliable, performant, and comprehensive than alternatives.

**Ecosystem Maturity**: Multiple language libraries (libbpf for C, cilium/ebpf for Go, Aya for Rust) support production eBPF development. bpftool provides essential debugging and inspection capabilities. The eBPF Foundation coordinates standardization and cross-platform development including Windows support.

**Performance Advantages**: eBPF delivers measurable performance improvements -- 2.5x for routing, 4.3x for load balancing -- by processing events within the kernel without user-space transitions. XDP offloading to NICs provides even greater efficiency. Meta has processed every packet to/from Facebook.com through eBPF since 2017.
