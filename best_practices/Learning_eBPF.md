# Learning eBPF
**Author:** Liz Rice (O'Reilly, March 2023)
**Topic tags:** `#systems` `#observability` `#cloud` `#security`
**Language focus:** C-first (kernel), Python/Go/Rust (user space)
**Sources:** `markdown_output/Learning_eBPF_-_Liz_Rice/Learning_eBPF_-_Liz_Rice.md` · `summaries/Learning_eBPF_-_Liz_Rice.md`

## TL;DR
eBPF lets you load custom, verified, JIT-compiled programs into the Linux kernel at runtime — no kernel module, no reboot, no application change. The three pillars are observability (kprobes/tracepoints), networking (XDP/TC/sockets), and security (LSM/seccomp/Tetragon). CO-RE + BTF + libbpf solve cross-kernel portability, the verifier enforces safety by exhaustive path analysis, and modern toolchains (libbpf/C, cilium/ebpf/Go, Aya/Rust, bpftrace) cover every entry point. In cloud-native environments eBPF replaces the sidecar model: one program in the kernel sees every container on a node.

---

## Best Practices by Topic

### 1. Treat eBPF as a Platform, Not a Feature

**Principle:** eBPF is a runtime-instrumentable kernel platform. Most users consume it indirectly through tools (Cilium, Falco, Parca, Tetragon, Pixie) — few write raw bytecode.

**Do:**
- Use eBPF when you need visibility or control over events no application would willingly expose (syscalls, packet ingress, LSM decisions, scheduling).
- Load programs dynamically — no reboot, no kernel patch — and let them start observing preexisting processes.
- Prefer the kernel vantage point for cross-container observability in Kubernetes (one kernel sees every pod on a node).
- Treat the verifier as your safety net: it eliminates entire classes of kernel-module failure modes.

**Don't:**
- Don't reach for a kernel module first; the verifier-checked eBPF program is safer and reversible.
- Don't assume you need to write eBPF code yourself; most value comes from using eBPF-based tools.
- Don't underestimate kernel upgrade lag — enterprise distros run kernels years behind upstream, gating which eBPF features are usable.

*Ref: Learning_eBPF.md — "What Is eBPF, and Why Is It Important?", "eBPF in Cloud Native Environments", "eBPF Is a Platform, Not a Feature"*

---

### 2. Know the History: BPF → seccomp-bPF → eBPF → Today

**Principle:** The acronym is historical baggage — "packet filter" hasn't fit for over a decade. Inside the kernel source the type is still `BPF_*`, outside the community says eBPF. They're synonyms.

**Do:**
- Cite the roots: BSD Packet Filter (McCanne & Jacobson, 1993), Linux adoption in 2.1.75 (1997), seccomp-bPF in kernel 3.5 (2012), eBPF in 3.18 (2014).
- Remember kprobe attachment arrived in 2015 — that's the moment tracing became practical.
- Use `bpf()` (lowercase) for the syscall; `BPF_*` for type/macro/struct names; `eBPF` when talking to humans.
- Track that BTF arrived in 2018 and LSM BPF in 2020 — those define the modern era.

**Don't:**
- Don't argue about whether to call it BPF or eBPF — they're the same.
- Don't expect to understand modern eBPF without grasping the BSD-PF roots (registers, instructions, packet verdicts).
- Don't ignore that production eBPF has been battle-tested at Meta since 2017 (every Facebook.com packet through XDP) and Netflix since 2016.

*Ref: Learning_eBPF.md — "eBPF's Roots: The Berkeley Packet Filter", "From BPF to eBPF", "The Evolution of eBPF to Production Systems", "Naming Is Hard"*

---

### 3. Understand the Linux-Kernel Vantage Point

**Principle:** eBPF lives in the layer that mediates all hardware access — file I/O, networking, memory, scheduling — so instrumenting it reveals everything applications do.

**Do:**
- Use `strace` to feel how much kernel traffic a "simple" command generates (a single `cat` invokes >100 syscalls).
- Exploit the shared-kernel property in containers: one eBPF program sees every container on a node without sidecars.
- Trust the kernel's vantage point over application instrumentation — bad actors won't helpfully instrument themselves.
- Treat syscalls as the natural event source for both tracing and security observability.

**Don't:**
- Don't underestimate ~30M lines of kernel code as a barrier — you don't need to know most of it.
- Don't try to add features by patching upstream kernel source: only ~33% of patches are accepted and ship-times are years.
- Don't reintroduce sidecars for cross-container observability — that's the very problem eBPF solves.

*Ref: Learning_eBPF.md — "The Linux Kernel", "Adding New Functionality to the Kernel", "eBPF in Cloud Native Environments"*

---

### 4. Start with the BCC Python "Hello World"

**Principle:** BCC is the lowest-friction entry point. The Python loader compiles a C string at runtime, attaches it, and prints the trace.

**Do:**
- Try the canonical example in *chapter2/hello.py* — attach to `execve` and watch all process launches.
- Run as root (or with `CAP_BPF` + `CAP_PERFMON`/`CAP_NET_ADMIN`); expect "Operation not permitted" otherwise.
- Recognize that dynamic-loading triggers already-running processes immediately.
- Use `bpf_trace_printk()` early for debugging — it writes to `/sys/kernel/debug/tracing/trace_pipe`.

**Don't:**
- Don't build production tools on BCC — see cluster 30 on BCC's portability cost.
- Don't confuse BCC's `bpf_trace_printk()` with libbpf's `bpf_printk()` — both wrap the same kernel helper.
- Don't rely on the trace pipe for production data — every program on the machine shares it.

**Code:**
```python
from bcc import BPF
program = r"""
int hello(void *ctx) {
    bpf_trace_printk("Hello World!");
    return 0;
}
"""
b = BPF(text=program)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")
b.trace_print()
```

```bash
$ hello.py
b' bash-5412 [001] .... 90432.904952: 0: bpf_trace_printk: Hello World'
```

*Ref: Learning_eBPF.md — "BCC's 'Hello World'", "Running 'Hello World'"*

---

### 5. Use the Right Linux Capabilities

**Principle:** `CAP_BPF` (kernel 5.8+) is necessary but not sufficient — different program types need different capability combinations.

**Do:**
- Run as root for development; design production deploys that grant only the minimum capability set.
- For tracing programs: `CAP_PERFMON` AND `CAP_BPF`.
- For networking programs: `CAP_NET_ADMIN` AND `CAP_BPF`.
- Read Milan Landaverde's "Introduction to CAP_BPF" for the complete table.

**Don't:**
- Don't assume `CAP_BPF` alone is enough — the additional perfmon/net_admin capability is still required for most workloads.
- Don't grant `CAP_SYS_ADMIN` as a shortcut — it unlocks everything but bypasses the principle of least privilege.
- Don't ignore "Operation not permitted" errors — they're almost always a capability problem, not a code bug.

*Ref: Learning_eBPF.md — "Running 'Hello World'" NOTE*

---

### 6. Choose the Right Map Type for the Job

**Principle:** All BPF maps are key-value stores, but each type has specialized performance or semantics. Pick the type that matches the access pattern.

**Do:**
- Hash tables for arbitrary key types and flexible schemas (`BPF_HASH`).
- Arrays when the key is a 4-byte index (`BPF_MAP_TYPE_ARRAY`).
- Per-CPU variants (`BPF_MAP_TYPE_PERF_EVENT_ARRAY`, per-CPU hash) to avoid lock contention.
- LRU caches when entries age out under memory pressure.
- Longest-prefix-match (`LPM_TRIE`) for routing-table-style lookups.
- Bloom filters when "definitely no" is acceptable and you need extreme speed.
- Sockmaps / devmaps for redirecting traffic at the socket/NIC layer.
- Program arrays for tail-call dispatch.
- Map-of-maps for storing references to other maps.

**Don't:**
- Don't use arrays when you need a non-`u32` key — the kernel requires array keys to be exactly 4 bytes.
- Don't reach for shared (non-per-CPU) maps under hot contention without considering spinlocks (kernel 5.1+, only for hash/array types, never for tracing/socket-filter programs).
- Don't forget that some maps have ordering or stack semantics (FIFO queues, LIFO stacks) — they're not interchangeable with arrays.

*Ref: Learning_eBPF.md — "BPF Maps"*

---

### 7. Pass Structured Data with Perf and Ring Buffers

**Principle:** For anything more than debug strings, send a typed struct via a buffer rather than the global trace pipe.

**Do:**
- Define a struct that mirrors what user space needs (`pid`, `uid`, `command`, plus a payload).
- Use `BPF_PERF_OUTPUT(output)` and `output.perf_submit(ctx, &data, sizeof(data))` in BCC.
- Use `BPF_RINGBUF_OUTPUT(output, 1)` on kernel 5.8+ — preferred over perf.
- Read from user space with a callback: `b["output"].event(data)` then format the fields.
- Use the 8-byte `bpf_get_current_pid_tgid() >> 32` idiom to extract the PID, masking `& 0xFFFFFFFF` for the UID.

**Don't:**
- Don't ship perf buffers on new code if your minimum kernel is 5.8+ — ring buffers preserve ordering across cores and use epoll.
- Don't forget `bpf_probe_read_kernel()` when copying strings from a local buffer into the payload (verifier won't let you assign C strings directly).
- Don't leave debug `bpf_trace_printk()` calls in production code — they share one global pipe.

**Code:**
```c
BPF_PERF_OUTPUT(output);
struct data_t {
   int pid;
   int uid;
   char command[16];
   char message[12];
};
int hello(void *ctx) {
   struct data_t data = {};
   char message[12] = "Hello World";
   data.pid = bpf_get_current_pid_tgid() >> 32;
   data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
   bpf_get_current_comm(&data.command, sizeof(data.command));
   bpf_probe_read_kernel(&data.message, sizeof(data.message), message);
   output.perf_submit(ctx, &data, sizeof(data));
   return 0;
}
```

```python
def print_event(cpu, data, size):
   data = b["output"].event(data)
   print(f"{data.pid} {data.uid} {data.command.decode()} " + \
         f"{data.message.decode()}")
b["output"].open_perf_buffer(print_event)
while True:
   b.perf_buffer_poll()
```

*Ref: Learning_eBPF.md — "Perf and Ring Buffer Maps", "Hash Table Map"*

---

### 8. Use Hash Tables for State and Aggregations

**Principle:** BCC's `BPF_HASH(...)` macro turns a one-liner into a typed hash table — perfect for counters keyed by UID, PID, or any scalar.

**Do:**
- Initialize the counter at zero before each lookup so the lookup-then-increment is unconditional.
- Read the map from user space with a polling loop (`b["counter_table"].items()`) when event latency is acceptable.
- Mask `bpf_get_current_uid_gid() & 0xFFFFFFFF` to extract just the UID (the top 32 bits are the GID).
- Treat the map as a snapshot — refresh from the kernel side on each event.

**Don't:**
- Don't treat the helper as a free-standing C method — BCC rewrites `counter_table.lookup(&uid)` into `bpf_map_lookup_elem()` before compilation.
- Don't poll faster than you need; the example polls every 2 seconds.
- Don't forget that the lookup may return NULL — always check before dereferencing (the verifier will reject unconditional deref).

**Code:**
```c
BPF_HASH(counter_table);
int hello(void *ctx) {
  u64 uid;
  u64 counter = 0;
  u64 *p;
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
  p = counter_table.lookup(&uid);
  if (p != 0) {
     counter = *p;
  }
  counter++;
  counter_table.update(&uid, &counter);
  return 0;
}
```

```python
while True:
  sleep(2)
  s = ""
  for k,v in b["counter_table"].items():
    s += f"ID {k.value}: {v.value}\t"
  print(s)
```

*Ref: Learning_eBPF.md — "Hash Table Map"*

---

### 9. Prefer Ring Buffers Over Perf Buffers on Kernel 5.8+

**Principle:** Ring buffers give one shared buffer with ordering preserved across cores, single epoll wakeup, and no per-CPU allocation.

**Do:**
- Switch the BCC macro `BPF_PERF_OUTPUT(output)` to `BPF_RINGBUF_OUTPUT(output, 1)`.
- Switch the kernel submit from `output.perf_submit(ctx, &data, sizeof(data))` to `output.ringbuf_output(&data, sizeof(data), 0)`.
- Switch user space from `open_perf_buffer`/`perf_buffer_poll` to `open_ring_buffer`/`ring_buffer_poll`.
- Update your syscall trace to expect a single `BPF_MAP_TYPE_RINGBUF` creation, not 4× `perf_event_open` calls.

**Don't:**
- Don't expect zero code churn — the strace pattern changes substantially (no per-CPU ppoll, just `epoll_pwait`).
- Don't use ring buffers if you must support pre-5.8 kernels — fall back to perf buffers there.

**Code:**
```python
# hello-ring-buffer-config.py (user-space diff vs hello-buffer-config.py)
# BPF_PERF_OUTPUT(output);            -> BPF_RINGBUF_OUTPUT(output, 1);
# output.perf_submit(ctx, &data, ...); -> output.ringbuf_output(&data, sizeof(data), 0);
# b["output"].open_perf_buffer(print_event) -> b["output"].open_ring_buffer(print_event)
# b.perf_buffer_poll()                -> b.ring_buffer_poll()
```

```c
bpf(BPF_MAP_CREATE, {map_type=BPF_MAP_TYPE_RINGBUF, key_size=0, value_size=0,
max_entries=4096, ... map_name="output", ...}, 128) = 4
```

*Ref: Learning_eBPF.md — "Perf and Ring Buffer Maps", "Ring Buffers"*

---

### 10. Use Tail Calls for Program Decomposition Without Stack Growth

**Principle:** `bpf_tail_call(ctx, prog_array_map, index)` replaces the running program rather than calling it — critical because the eBPF stack is only 512 bytes.

**Do:**
- Build a `BPF_PROG_ARRAY(syscall, 300)` and populate indices in user space with `prog_array[ct.c_int(59)] = ct.c_int(exec_fn.fd)`.
- Treat the parent program as a dispatcher that does a `bpf_tail_call()` and continues with a default trace on failure.
- Use one program to handle multiple opcodes — the same `hello_timer` can be referenced by indices 222, 223, 224, 225, 226.
- Use an `ignore_opcode()` no-op program for syscalls that would flood the output.
- Combine with the 1-million-instruction limit — up to 33 chained tail calls give huge headroom.

**Don't:**
- Don't expect tail calls to compose with BPF subprograms on x86 before kernel 5.10 (the JIT support was incomplete).
- Don't assume a missing program-array entry is an error — the helper fails silently and execution continues.
- Don't use tail calls when you actually need the caller's state — tail calls replace execution and never return.

**Code:**
```c
BPF_PROG_ARRAY(syscall, 300);
int hello(struct bpf_raw_tracepoint_args *ctx) {
   int opcode = ctx->args[1];
   syscall.call(ctx, opcode);
   bpf_trace_printk("Another syscall: %d", opcode);
   return 0;
}
int hello_execve(void *ctx) {
   bpf_trace_printk("Executing a program");
   return 0;
}
int hello_timer(struct bpf_raw_tracepoint_args *ctx) {
   if (ctx->args[1] == 222) {
       bpf_trace_printk("Creating a timer");
   } else if (ctx->args[1] == 226) {
       bpf_trace_printk("Deleting a timer");
   } else {
       bpf_trace_printk("Some other timer operation");
   }
   return 0;
}
int ignore_opcode(void *ctx) {
   return 0;
}
```

```python
b.attach_raw_tracepoint(tp="sys_enter", fn_name="hello")
ignore_fn = b.load_func("ignore_opcode", BPF.RAW_TRACEPOINT)
exec_fn   = b.load_func("hello_exec",    BPF.RAW_TRACEPOINT)
timer_fn  = b.load_func("hello_timer",  BPF.RAW_TRACEPOINT)
prog_array = b.get_table("syscall")
prog_array[ct.c_int(59)]  = ct.c_int(exec_fn.fd)
prog_array[ct.c_int(222)] = ct.c_int(timer_fn.fd)
prog_array[ct.c_int(223)] = ct.c_int(timer_fn.fd)
prog_array[ct.c_int(224)] = ct.c_int(timer_fn.fd)
prog_array[ct.c_int(225)] = ct.c_int(timer_fn.fd)
prog_array[ct.c_int(226)] = ct.c_int(timer_fn.fd)
prog_array[ct.c_int(21)]  = ct.c_int(ignore_fn.fd)
prog_array[ct.c_int(22)]  = ct.c_int(ignore_fn.fd)
prog_array[ct.c_int(25)]  = ct.c_int(ignore_fn.fd)
b.trace_print()
```

*Ref: Learning_eBPF.md — "Function Calls", "Tail Calls"*

---

### 11. Use BPF Subprograms for Function Calls (Kernel 4.16+, LLVM 6+)

**Principle:** Real function calls (with call/return) became possible once the verifier learned to follow them. Stack usage still constrains depth.

**Do:**
- Add `static __attribute((noinline))` to functions you want to keep as subprograms (not inlined).
- Use the `call 0x85` opcode pattern; bpftool's `prog dump xlated` will show `call pc+7#bpf_prog_<tag>_<fn>`.
- Keep nesting shallow — every active call consumes the 512-byte stack.

**Don't:**
- Don't expect BCC to support BPF-to-BPF calls — keep functions inlined there.
- Don't try deep recursion — eBPF has no proper stack frame for it; the verifier will reject.

**Code:**
```c
static __attribute((noinline)) int get_opcode(struct bpf_raw_tracepoint_args *ctx)
{
   return ctx->args[1];
}

SEC("raw_tp")
int hello(struct bpf_raw_tracepoint_args *ctx) {
   int opcode = get_opcode(ctx);
   bpf_printk("Syscall: %d", opcode);
   return 0;
}
```

```text
$ bpftool prog dump xlated name hello
int hello(struct bpf_raw_tracepoint_args * ctx):
; int opcode = get_opcode(ctx);
   0: (85) call pc+7#bpf_prog_cbacc90865b1b9a5_get_opcode
; bpf_printk("Syscall: %d", opcode);
   1: (18) r1 = map[id:193][0]+0
   ...
int get_opcode(struct bpf_raw_tracepoint_args * ctx):
   8: (79) r0 = *(u64 *)(r1 +8)
   9: (95) exit
```

*Ref: Learning_eBPF.md — "BPF to BPF Calls"*

---

### 12. Trace Into the eBPF Virtual Machine

**Principle:** eBPF bytecode runs in a software VM with 10 general-purpose registers (R0–R9) plus a read-only frame pointer (R10). Knowing this is essential for reading verifier output.

**Do:**
- Treat R1 as the incoming context pointer; copy it to R6 before calling helpers (helpers clobber R1–R5, preserve R6–R9).
- Expect R0 to hold the return value and to be checked by the verifier (`R0 !read_ok`).
- Recognize `struct bpf_insn` — 8 bytes (16 for wide encoding) with opcode, dst/src register nibbles, offset, and immediate.
- Read `bpftool prog dump xlated` to see the post-verifier bytecode and `dump jited` for the native code.

**Don't:**
- Don't try to write R10 — it's a read-only frame pointer.
- Don't use `callx <register>` — Clang emits `callx` by default but eBPF can't dispatch through registers, so use `-O2` to rewrite them.
- Don't think of "wide" instructions (16 bytes) as exceptional — they're how 64-bit immediates are loaded.

**Code:**
```text
hello.bpf.o: file format elf64-bpf
Disassembly of section xdp:
0000000000000000 <hello>:
; bpf_printk("Hello World %d", counter");
   0: 18 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 r6 = 0 ll
   2: 61 63 00 00 00 00 00 00 r3 = *(u32 *)(r6 +0)
   3: 18 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 r1 = 0 ll
   5: b7 02 00 00 0f 00 00 00 r2 = 15
   6: 85 00 00 00 06 00 00 00 call 6
; counter++;
   7: 61 61 00 00 00 00 00 00 r1 = *(u32 *)(r6 +0)
   8: 07 01 00 00 01 00 00 00 r1 += 1
   9: 63 16 00 00 00 00 00 00 *(u32 *)(r6 +0) = r1
; return XDP_PASS;
  10: b7 00 00 00 02 00 00 00 r0 = 2
  11: 95 00 00 00 00 00 00 00 exit
```

*Ref: Learning_eBPF.md — "The eBPF Virtual Machine", "eBPF Registers", "eBPF Instructions", "The Translated Bytecode", "The JIT-Compiled Machine Code"*

---

### 13. Write XDP "Hello World" with libbpf in Pure C

**Principle:** libbpf + Clang exposes what BCC hides: section names, license strings, SEC() macros, and the actual bytecode lifecycle.

**Do:**
- Always `#include <linux/bpf.h>` and `<bpf/bpf_helpers.h>`.
- Mark the section: `SEC("xdp")` for XDP programs.
- Always declare the license: `char LICENSE[] SEC("license") = "Dual BSD/GPL";` — some helpers are GPL-only.
- Compile with `-target bpf -g -O2` to get BTF, debug info, and verifier-friendly output.
- Strip DWARF after compile: `llvm-strip -g hello.bpf.o`.

**Don't:**
- Don't forget the `SEC("license")` — verifier rejects GPL-only helper calls otherwise.
- Don't confuse `bpf_printk()` (libbpf) with `bpf_trace_printk()` (BCC) — they wrap the same kernel helper but in different headers.
- Don't omit `-O2` — by default Clang emits `callx <register>` which the verifier rejects.

**Code:**
```c
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
int counter = 0;

SEC("xdp")
int hello(void *ctx) {
    bpf_printk("Hello World %d", counter);
    counter++;
    return XDP_PASS;
}
char LICENSE[] SEC("license") = "Dual BSD/GPL";
```

```makefile
hello.bpf.o: %.o: %.c
   clang \
       -target bpf \
       -I/usr/include/$(shell uname -m)-linux-gnu \
       -g \
       -O2 -c $< -o $@
```

*Ref: Learning_eBPF.md — "eBPF 'Hello World' for a Network Interface", "Compiling an eBPF Object File"*

---

### 14. Use bpftool to Inspect, Load, Attach, Detach, Unload

**Principle:** bpftool is the canonical CLI for everything eBPF. It's the cheapest way to ground-truth what your program is doing.

**Do:**
- `bpftool prog list` to see every loaded program, including its tag, type, map IDs, BTF ID.
- `bpftool prog show id 540 --pretty` to see xlated bytes, jited bytes, memlock.
- `bpftool prog dump xlated name hello` for post-verifier bytecode; `dump jited` for native code.
- `bpftool prog load hello.bpf.o /sys/fs/bpf/hello` to load and pin in one step.
- `bpftool net attach xdp id 540 dev eth0` to attach; `bpftool net detach xdp dev eth0` to remove.
- `bpftool map list` / `bpftool map dump name config` to inspect maps.
- Use `rm /sys/fs/bpf/hello` to unload — there's no `bpftool prog unload`.

**Don't:**
- Don't rely on program IDs as stable identifiers — only the tag (SHA) and pinned path are stable.
- Don't expect bpftool's JIT dump on every distro — some packages lack libbfd; build from source if you need it.
- Don't leave stale pinned objects around — they hold reference counts and keep programs alive.

*Ref: Learning_eBPF.md — "Loading the Program into the Kernel", "Inspecting the Loaded Program", "Detaching the Program", "Unloading the Program"*

---

### 15. Recognize the Program Tag as Stable Identity

**Principle:** The program tag is a SHA of the instructions — same code = same tag. Use it for reproducible identification.

**Do:**
- Reference programs by ID, name, tag, or pinned path — all work in bpftool.
- Treat the tag as your content-addressable handle across reboots and recompiles.
- Combine with the loaded_at timestamp for forensics.

**Don't:**
- Don't expect IDs to persist — they re-allocated each load.
- Don't confuse `bpftool prog show name hello` with multiple programs having the same name — IDs and pinned paths are unique.

*Ref: Learning_eBPF.md — "The BPF Program Tag"*

---

### 16. Use Global Variables by Naming Them (Maps Are Created Automatically)

**Principle:** Before 2019 you had to declare a map explicitly; now `int counter = 0;` becomes a `.bss` map, `const char fmt[] = "...";` becomes `.rodata` — both implicitly.

**Do:**
- Trust the libbpf loader to create `.bss` (mutable) and `.rodata` (read-only/frozen) maps for global variables.
- Use `bpftool map dump name hello.bss` to see live counter values, including pretty field names if `-g` was used.
- Use `bpftool map dump name hello.rodata` to see constant strings.

**Don't:**
- Don't hand-roll maps for simple global state — let the loader handle it.
- Don't try to write to a `.rodata` map (the verifier will reject it).

**Code:**
```bash
$ bpftool map list
165: array  name hello.bss   flags 0x400
       key 4B value 4B max_entries 1 memlock 4096B
       btf_id 254
166: array  name hello.rodata flags 0x80
       key 4B value 15B max_entries 1 memlock 4096B
       btf_id 254 frozen

$ bpftool map dump name hello.bss
[{
        "value": {
            ".bss": [{
                "counter": 11127
            }]
        }
}]
```

*Ref: Learning_eBPF.md — "Global Variables"*

---

### 17. Master the bpf() System Call Interface

**Principle:** Every user-space eBPF library ultimately calls `bpf(int cmd, union bpf_attr *attr, unsigned int size)`. Knowing the cmds lets you debug any library.

**Do:**
- Recognize the major commands: `BPF_PROG_LOAD`, `BPF_MAP_CREATE`, `BPF_MAP_UPDATE_ELEM`, `BPF_MAP_LOOKUP_ELEM`, `BPF_MAP_DELETE_ELEM`, `BPF_MAP_GET_NEXT_KEY`, `BPF_BTF_LOAD`, `BPF_OBJ_GET_INFO_BY_FD`, `BPF_RAW_TRACEPOINT_OPEN`, `BPF_LINK_CREATE`, `BPF_PROG_BIND_MAP`.
- Trace `strace -e bpf ./your_tool` to see exactly what your tool does.
- Treat returned FDs as process-local — different processes may have different FD numbers for the same map.

**Don't:**
- Don't try to read events from a map with `bpf()` syscalls — use `ppoll`/`epoll` on the perf/ring buffer FDs.
- Don't forget to size `attr` correctly; the kernel validates `size` and rejects mismatches.

*Ref: Learning_eBPF.md — "The bpf() Syscall", "Key Operations Traced via strace"*

---

### 18. Understand Reference Counting, Pinning, and BPF Links

**Principle:** Programs and maps live until their reference count hits zero. Pinning and BPF links are how you keep them alive past the loader process.

**Do:**
- Remember that loading returns an FD; the FD is one reference. When the loader exits, the FD closes.
- Pin programs/maps to `/sys/fs/bpf/<name>` to keep them alive (`bpftool prog load ... /sys/fs/bpf/hello`).
- Use BPF links (kernel 5.8+) when you want a stable attachment that survives loader exit.
- Recognize that some program types (XDP, TC, cgroup) stay attached even after the loader process exits — their attachment counts as a reference.
- For tracing programs, the loader process owns the reference; if it dies, the program is unloaded.

**Don't:**
- Don't assume that `ip link set dev eth0 xdp obj hello.bpf.o sec xdp` automatically pins — it doesn't; the XDP attachment holds the reference.
- Don't forget that `/sys/fs/bpf/` is a pseudo-filesystem (in-memory, gone on reboot).
- Don't manually bind a map to a program with `BPF_PROG_BIND_MAP` unless you have a specific reason — libbpf handles it.

*Ref: Learning_eBPF.md — "BPF Program and Map References", "Pinning", "BPF Links"*

---

### 19. Trace Through a Perf-Buffer Setup with strace

**Principle:** Watching the syscalls demystifies why perf buffers need four `perf_event_open` calls on a four-core machine.

**Do:**
- Run `strace -e bpf,perf_event_open,ioctl,ppoll ./hello-buffer-config.py` to see the full sequence.
- Expect `BPF_BTF_LOAD` → `BPF_MAP_CREATE` (PERF_EVENT_ARRAY) → `BPF_MAP_CREATE` (HASH) → `BPF_PROG_LOAD` → `BPF_MAP_UPDATE_ELEM` × 4 (one per CPU).
- Expect one `perf_event_open(PERF_TYPE_SOFTWARE, PERF_COUNT_SW_BPF_OUTPUT, ...)` per CPU with `cpu` ∈ {0,1,2,3}.
- Expect one `ioctl(fd, PERF_EVENT_IOC_SET_BPF, prog_fd)` and `ioctl(fd, PERF_EVENT_IOC_ENABLE, 0)` per event FD.
- Expect `ppoll` over all event FDs to read events.

**Don't:**
- Don't confuse the four `BPF_MAP_UPDATE_ELEM` calls for the config map — they're setting the array entry for each CPU's buffer.

*Ref: Learning_eBPF.md — "Initializing the Perf Buffer", "Setting Up and Reading Perf Events"*

---

### 20. Use ppoll vs epoll Appropriately

**Principle:** ppoll is rebuilt every call (perf buffer model); epoll registers the FD set once and waits (ring buffer / modern model).

**Do:**
- Use ppoll for perf buffers — the FD set changes as CPUs come and go.
- Use epoll for ring buffers and any single-FD event source — it's more efficient.
- Recognize that BCC currently uses ppoll for perf and epoll for ring buffers even though libbpf offers ring_buffer__poll.

**Don't:**
- Don't build the FD set on every call when epoll would do — wasteful.
- Don't use epoll on FD sets that change dynamically without re-registering.

*Ref: Learning_eBPF.md — "Ring Buffers"*

---

### 21. Compile Once, Run Everywhere with CO-RE + BTF + libbpf

**Principle:** CO-RE solves the kernel-data-structure portability problem by emitting relocations that libbpf applies at load time. Without it you must recompile on every target.

**Do:**
- Use the four ingredients: BTF (kernel 5.4+), `vmlinux.h` (generated from `/sys/kernel/btf/vmlinux`), compiler with relocation support (Clang `-g`, GCC 12+), and a CO-RE-aware loader (libbpf, cilium/ebpf, Aya).
- Generate `vmlinux.h` with `bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h`.
- Use BTFHub for older kernels that don't ship `vmlinux` BTF.
- Include `<vmlinux.h>`, `<bpf/bpf_helpers.h>`, `<bpf/bpf_tracing.h>`, `<bpf/bpf_core_read.h>`.

**Don't:**
- Don't keep BCC's runtime-compilation model for production — it requires toolchains on every target, has startup latency, and wastes compute on fleet machines.
- Don't hand-define kernel structs — let `vmlinux.h` provide them, then trust the relocations.

*Ref: Learning_eBPF.md — "BCC's Approach to Portability", "CO-RE Overview"*

---

### 22. Trust BTF to Pretty-Print and Validate

**Principle:** BTF is metadata about types and functions. Use it for pretty-printing, debugging, source-line mapping, and CO-RE relocations.

**Do:**
- Inspect with `bpftool btf list`, `bpftool btf dump id <id>`, `bpftool btf dump map name <name>`, `bpftool btf dump prog <id>`.
- Notice that BTF types are IDs that reference each other (e.g., `[1] TYPEDEF 'u32' type_id=2`).
- Use BTF for BPF spin locks — the lock field requires a BTF-described value struct.
- Compile with `-g` so the kernel can interleave source lines in verifier logs.

**Don't:**
- Don't strip `-g` and expect debug-friendly output — verifier logs without source-line info are painful.
- Don't try to maintain your own kernel data-type definitions — BTFHub has them.
- Don't ignore the difference between data BTF (`.BTF`) and function/line BTF (`.BTF.ext`) — both are needed.

**Code:**
```text
[1] TYPEDEF 'u32' type_id=2
[2] TYPEDEF '__u32' type_id=3
[3] INT 'unsigned int' size=4 bits_offset=0 nr_bits=32 encoding=(none)
[4] STRUCT 'user_msg_t' size=12 vlen=1
        'message' type_id=6 bits_offset=0
[5] INT 'char' size=1 bits_offset=0 nr_bits=8 encoding=(none)
[6] ARRAY '(anon)' type_id=5 index_type_id=7 nr_elems=12
[7] INT '__ARRAY_SIZE_TYPE__' size=4 bits_offset=0 nr_bits=32 encoding=(none)
[8] STRUCT '____btf_map_config' size=16 vlen=2
        'key' type_id=1 bits_offset=0
        'value' type_id=4 bits_offset=32
```

*Ref: Learning_eBPF.md — "BPF Type Format", "BTF Types", "Maps with BTF Information"*

---

### 23. Write libbpf CO-RE Programs with the Right Headers and Macros

**Principle:** The standard header stack and map-definition macros make CO-RE programs portable and readable.

**Do:**
- Include `vmlinux.h`, `<bpf/bpf_helpers.h>`, `<bpf/bpf_tracing.h>`, `<bpf/bpf_core_read.h>`, plus your app-specific header.
- Use `SEC("ksyscall/execve")` to auto-attach to the syscall entry on any architecture.
- Use `BPF_KPROBE_SYSCALL(name, arg1, ...)` for typed syscall parameters.
- Use `BPF_CORE_READ(struct_ptr, field1, field2, ...)` for chained pointer dereferences.
- Define maps with `__uint(type, ...)` and `__type(key, ...)`/`__type(value, ...)` placed in a `SEC(".maps")` struct.

**Don't:**
- Don't forget to set `-D __TARGET_ARCH_<arch>` — required by BPF_KPROBE macros.
- Don't rely on BCC's `my_map.lookup(&key)` syntax — write `bpf_map_lookup_elem(&my_map, &key)` directly.
- Don't include `<linux/types.h>` only and expect full kernel struct coverage — use `vmlinux.h`.

**Code:**
```c
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <bpf/bpf_core_read.h>
#include "hello-buffer-config.h"

struct {
   __uint(type, BPF_MAP_TYPE_PERF_EVENT_ARRAY);
   __uint(key_size, sizeof(u32));
   __uint(value_size, sizeof(u32));
} output SEC(".maps");

struct user_msg_t {
   char message[12];
};
struct {
   __uint(type, BPF_MAP_TYPE_HASH);
   __uint(max_entries, 10240);
   __type(key, u32);
   __type(value, struct user_msg_t);
} my_config SEC(".maps");

char message[12] = "Hello World";
char LICENSE[] SEC("license") = "Dual BSD/GPL";

SEC("ksyscall/execve")
int BPF_KPROBE_SYSCALL(hello, const char *pathname)
{
   struct data_t data = {};
   struct user_msg_t *p;
   data.pid = bpf_get_current_pid_tgid() >> 32;
   data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
   bpf_get_current_comm(&data.command, sizeof(data.command));
   bpf_probe_read_user_str(&data.path, sizeof(data.path), pathname);
   p = bpf_map_lookup_elem(&my_config, &data.uid);
   if (p != 0) {
      bpf_probe_read_kernel(&data.message, sizeof(data.message), p->message);
   } else {
      bpf_probe_read_kernel(&data.message, sizeof(data.message), message);
   }
   bpf_perf_event_output(ctx, &output, BPF_F_CURRENT_CPU,
                         &data, sizeof(data));
   return 0;
}
```

```makefile
hello-buffer-config.bpf.o: %.o: %.c
   clang \
       -target bpf \
       -D __TARGET_ARCH_$(ARCH) \
       -I/usr/include/$(shell uname -m)-linux-gnu \
       -Wall \
       -O2 -g \
       -c $< -o $@
   llvm-strip -g $@
```

*Ref: Learning_eBPF.md — "CO-RE eBPF Programs", "Header Files", "Defining Maps", "eBPF Program Sections", "Memory Access with CO-RE", "License Definition", "Compiling eBPF Programs for CO-RE"*

---

### 24. Use bpf_map_lookup_elem Directly (No BCC Sugar)

**Principle:** In libbpf you write the helper call directly — there's no `.lookup()` shorthand.

**Do:**
- Always check the return for NULL — the verifier will reject unconditional deref.
- Use `bpf_map_lookup_elem(&map, &key)` returning `void *` (NULL on miss).
- Pass `BPF_F_CURRENT_CPU` to perf output helpers so the right per-CPU buffer is selected.

**Don't:**
- Don't write `my_map.lookup(&key)` — that's BCC sugar; libbpf requires the helper.
- Don't use `bpf_probe_write_user()` except for experiments — it's restricted and rarely appropriate.

*Ref: Learning_eBPF.md — "Memory Access with CO-RE", "eBPF Program Sections"*

---

### 25. Generate and Use BPF Skeletons for Lifecycle Management

**Principle:** Skeletons give you one-liner open/load/attach/destroy functions plus typed access to maps and programs.

**Do:**
- Generate with `bpftool gen skeleton hello-buffer-config.bpf.o > hello-buffer-config.skel.h`.
- Use `hello_buffer_config_bpf__open_and_load()` to bring it all into the kernel.
- Use `hello_buffer_config_bpf__attach(skel)` to auto-attach per the SEC() names.
- Use `bpf_map__fd(skel->maps.output)` to get the FD for `perf_buffer__new`.
- Modify `skel->data->c` between open and load to initialize globals.
- Free with `perf_buffer__free(pb); hello_buffer_config_bpf__destroy(skel);`.

**Don't:**
- Don't change `skel->data->c` *after* loading — it's only the user-space mirror.
- Don't skip the destroy call — leaks the kernel objects.
- Don't try to load the `.o` file separately — the skeleton embeds the bytecode bytes.

**Code:**
```c
#include "hello-buffer-config.h"
#include "hello-buffer-config.skel.h"
int main()
{
   struct hello_buffer_config_bpf *skel;
   struct perf_buffer *pb = NULL;
   int err;
   libbpf_set_print(libbpf_print_fn);
   skel = hello_buffer_config_bpf__open_and_load();
   err = hello_buffer_config_bpf__attach(skel);
   pb = perf_buffer__new(bpf_map__fd(skel->maps.output), 8, handle_event,
                                                          lost_event, NULL, NULL);
   while (true) {
       err = perf_buffer__poll(pb, 100);
   }
   perf_buffer__free(pb);
   hello_buffer_config_bpf__destroy(skel);
   return -err;
}
```

*Ref: Learning_eBPF.md — "BPF Skeletons", "Loading programs and maps into the kernel", "Attaching to events", "Managing an event buffer"*

---

### 26. Reuse Pinned Maps When You Need Cross-Program State

**Principle:** Maps pinned under `/sys/fs/bpf/<name>` are visible to any process with the right capabilities — perfect for sharing state between independently loaded programs.

**Do:**
- Pin a map once with `bpftool map create /sys/fs/bpf/findme type array key 4 value 32 entries 4 name findme`.
- Open it from another program with `bpf_obj_get("/sys/fs/bpf/findme")`.
- Use `bpf_map__set_autocreate()` if you want libbpf to skip auto-creation when reusing.
- Use it when only one program should create the map.

**Don't:**
- Don't create a second map with the same name and expect shared state — they're independent.
- Don't forget the cleanup path; pinning doesn't auto-delete.

**Code:**
```c
struct bpf_map_info info = {};
unsigned int len = sizeof(info);
int findme = bpf_obj_get("/sys/fs/bpf/findme");
if (findme <= 0) {
    printf("No FD\n");
} else {
    bpf_obj_get_info_by_fd(findme, &info, &len);
    printf("Name: %s\n", info.name);
}
```

*Ref: Learning_eBPF.md — "Accessing existing maps"*

---

### 27. Understand How BPF Relocations Patch Instructions

**Principle:** Each CO-RE relocation records instruction offset, BTF type ID, access path, and relocation kind. libbpf patches the bytecode at load time.

**Do:**
- Run `bpftool -d prog load hello.bpf.o /sys/fs/bpf/hello` to see relocation messages.
- Recognize "matching candidate" lines and "patched insn" lines.
- Use `bpftool btf dump file` to see what BTF information the object carries.
- Add `#pragma clang attribute push (__attribute__((preserve_access_index)), apply_to = record)` semantics via `vmlinux.h` so Clang emits relocations automatically.

**Don't:**
- Don't strip BTF info from the object — relocations depend on it.
- Don't expect the same offsets after CO-RE — the kernel may differ from your build machine.

**Code:**
```text
libbpf: CO-RE relocating [24] struct user_pt_regs: found target candidate [205]
struct user_pt_regs in [vmlinux]
libbpf: prog 'hello': relo #0: <byte_off> [24] struct user_pt_regs.regs[0]
(0:0:0 @ offset 0)
libbpf: prog 'hello': relo #0: matching candidate #0 <byte_off> [205] struct
user_pt_regs.regs[0] (0:0:0 @ offset 0)
libbpf: prog 'hello': relo #0: patched insn #1 (LDX/ST/STX) off 0 -> 0
```

*Ref: Learning_eBPF.md — "BPF Relocations"*

---

### 28. Embrace the Verifier — and Read Its Log

**Principle:** The verifier exhaustively explores all paths, tracking register types and ranges. Rejection is a feature; the log is your debugging partner.

**Do:**
- Compile with `-g` so the verifier log interleaves source lines.
- Build a mental model: register states are tracked in `bpf_reg_state` with a `bpf_reg_type` (`NOT_INIT`, `SCALAR_VALUE`, `PTR_TO_CTX`, `PTR_TO_PACKET`, `PTR_TO_MAP_VALUE`, …) plus a value range.
- Use `libbpf_set_print()` to capture the log from your loader.
- Capture the log on success too if you're learning — it's illuminating.

**Don't:**
- Don't ignore `processed 61 insns (limit 1000000) max_states_per_insn 0 total_states 4 peak_states 4` — those numbers tell you how hard the verifier worked.
- Don't panic at arbitrary errors — the verifier has improved dramatically and gives real hints now.

**Code:**
```text
0: (bf) r6 = r1
; data.counter = c;
1: (18) r1 = 0xffff800008178000
3: (61) r2 = *(u32 *)(r1 +0)
 R1_w=map_value(id=0,off=0,ks=4,vs=16,imm=0) R6_w=ctx(id=0,off=0,imm=0)
 R10=fp0
; c++;
4: (bf) r3 = r2
5: (07) r3 += 1
6: (63) *(u32 *)(r1 +0) = r3
 R1_w=map_value(id=0,off=0,ks=4,vs=16,imm=0)
 R2_w=inv(id=1,umax_value=4294967295,
  var_off=(0x0; 0xffffffff))
 R3_w=inv(id=0,umin_value=1,umax_value=4294967296,
  var_off=(0x0; 0x1ffffffff)) R6_w=ctx(id=0,off=0,imm=0) R10=fp0
```

*Ref: Learning_eBPF.md — "The Verification Process", "The Verifier Log"*

---

### 29. Visualize Control Flow with bpftool + dot

**Principle:** When the verifier rejects something complex, a graph reveals what paths exist and which one is the culprit.

**Do:**
- Run `bpftool prog dump xlated name kprobe_exec visual > out.dot`.
- Convert with `dot -Tpng out.dot > out.png`.
- Use the visualizer to spot unreachable blocks and surprise loops.

**Don't:**
- Don't expect every distro's bpftool to support the `visual` subcommand — some are old.

*Ref: Learning_eBPF.md — "Visualizing Control Flow"*

---

### 30. Match Helper Functions to the Program Type

**Principle:** The verifier rejects helpers that don't make sense for the program type. A `bpf_get_current_pid_tgid()` in an XDP program is meaningless.

**Do:**
- Use `bpftool feature` to see which helpers are available for each program type.
- Treat the verifier's "unknown func" error as "not available for this program type".
- Pass the right register type for each argument — frame pointer (`fp`), map pointer (`map_ptr`), etc.

**Don't:**
- Don't call `bpf_get_current_pid_tgid()` from XDP — there's no current process when a packet arrives.
- Don't pass a frame pointer where a map pointer is expected (`R1 type=fp expected=map_ptr`).

**Code:**
```c
const struct bpf_func_proto bpf_map_lookup_elem_proto = {
   .func = bpf_map_lookup_elem,
   .gpl_only = false,
   .pkt_access = true,
   .ret_type = RET_PTR_TO_MAP_VALUE_OR_NULL,
   .arg1_type = ARG_CONST_MAP_PTR,
   .arg2_type = ARG_PTR_TO_MAP_KEY,
};
```

*Ref: Learning_eBPF.md — "Validating Helper Functions", "Helper Function Arguments"*

---

### 31. Pick a License That Matches Your Helper Use

**Principle:** Some helpers are GPL-only. The verifier enforces the license compatibility at load time.

**Do:**
- Default to `char LICENSE[] SEC("license") = "Dual BSD/GPL";`.
- Check the BCC project's helper list when in doubt about GPL-ness.
- Add `gpl_only = true` in mind whenever you use `bpf_probe_read_kernel()` — it's GPL.

**Don't:**
- Don't ship a BSD-only license and then call a GPL helper — verifier rejects it.
- Don't omit the license section — verifier won't be able to load the program.

**Code:**
```text
cannot call GPL-restricted function from non-GPL compatible program
```

*Ref: Learning_eBPF.md — "Checking the License"*

---

### 32. Always Bounds-Check Before Memory Access

**Principle:** The verifier rejects any memory access that could be out of bounds. Off-by-one and unbounded pointer arithmetic are the top causes.

**Do:**
- In XDP/TC: explicitly check `data + sizeof(header) <= data_end` before reading each header.
- For arrays: use `if (c < sizeof(arr))` — never `<=`.
- Use `bpf_probe_read_*()` helpers for arbitrary kernel memory access.
- Trust the verifier to catch `data_end++;` — pointer arithmetic on `pkt_end` is explicitly prohibited.

**Don't:**
- Don't write `if (c <= sizeof(message))` — verifier catches it as `invalid access to map value, value_size=16 off=16 size=1`.
- Don't modify `data_end` and expect the verifier to let you — `R3 pointer arithmetic on pkt_end prohibited`.
- Don't dereference pointers returned from helpers without a NULL check.

**Code:**
```c
SEC("xdp")
int xdp_hello(struct xdp_md *ctx) {
  void *data = (void *)(long)ctx->data;
  void *data_end = (void *)(long)ctx->data_end;
  bpf_printk("%x", data_end);
  return XDP_PASS;
}
```

*Ref: Learning_eBPF.md — "Checking Memory Access"*

---

### 33. Always Check Helper-Returned Pointers for NULL

**Principle:** Every `bpf_map_lookup_elem()` may return NULL; the verifier will reject any code that doesn't check.

**Do:**
- Wrap every map-lookup result in `if (p != 0)` before reading.
- For helper functions like `bpf_probe_read_kernel()`, the third arg is named `unsafe_ptr` precisely so the helper does the NULL check for you.
- Check fentry return types — they default to `map_value_or_null` until narrowed.

**Don't:**
- Don't write `char a = p->message[0];` without a NULL check — verifier says `R7 invalid mem access 'map_value_or_null'`.
- Don't trust the compiler to warn you — only the verifier cares.

**Code:**
```c
p = bpf_map_lookup_elem(&my_config, &uid);
if (p != 0) {
   char a = p->message[0];
   bpf_printk("%d", cc);
}
```

*Ref: Learning_eBPF.md — "Checking Pointers Before Dereferencing Them"*

---

### 34. Respect the Instruction-Complexity Limit

**Principle:** The verifier processes up to 1,000,000 instructions per program. Loops are bounded (kernel 5.3+) and must fit.

**Do:**
- Use bounded `for (int i=0; i < 10; i++)` — verifier unrolls it 10 times.
- Use `bpf_loop(n, callback_fn, ...)` on kernel 5.17+ — verifier validates the callback once.
- Use `bpf_for_each_map_elem()` to iterate maps without writing a loop.
- Trust the verifier to refuse loops without a provable upper bound.

**Don't:**
- Don't write `for (int i=0; i < c; i++)` where `c` is a runtime global — verifier will hit the complexity limit.
- Don't pre-kernel-5.3 expect loops to work — `#pragma unroll` was the workaround.
- Don't assume the 4,096-instruction limit for unprivileged users is gone — it still applies there.

*Ref: Learning_eBPF.md — "Running to Completion", "Loops"*

---

### 35. Initialize R0 Before Returning

**Principle:** R0 holds the program return value; the verifier refuses to load if R0 is uninitialized.

**Do:**
- Always `return XDP_PASS;` (or equivalent) at the end.
- Recognize that calling a helper initializes R0 (the helper's return value), so `bpf_printk(...)` followed by `return;` works.
- Check the verifier's `R0 !read_ok` message when you forget.

**Don't:**
- Don't write `// return XDP_PASS;` for debugging and expect the program to load.
- Don't depend on a default return value.

**Code:**
```c
SEC("xdp")
int xdp_hello(struct xdp_md *ctx) {
 void *data = (void *)(long)ctx->data;
 void *data_end = (void *)(long)ctx->data_end;
 // bpf_printk("%x", data_end);
 // return XDP_PASS;
}
```

*Ref: Learning_eBPF.md — "Checking the Return Code"*

---

### 36. Pick the Right Tracing Attachment

**Principle:** There are ~30 program types and ~40 attachment types. Pick the most specific stable interface.

**Do:**
- Prefer tracepoints for stable kernel hooks (1400+ on kernel 5.15).
- Use kprobes for non-inlined internal functions; remember inlining can make kprobes impossible.
- Use fentry/fexit (kernel 5.5+) when available — more efficient than kprobes and fexit gives both args and return value.
- Use BTF-enabled tracepoints (`tp_btf/...`) when you can — they auto-generate context structures.
- Use uprobes/uretprobes/USDTs for user-space instrumentation.
- Use raw tracepoints (`raw_tp/...`) for performance — no pre-mapped structure.

**Don't:**
- Don't use syscall kprobes for security tooling — TOCTOU window.
- Don't assume you can attach a kprobe to an inlined function.
- Don't try to access tracepoint `common_*` fields in eBPF — verifier says `invalid bpf_context access`.

**Code:**
```c
SEC("ksyscall/execve")
int BPF_KPROBE_SYSCALL(kprobe_sys_execve, char *pathname)
{ ... }

SEC("kprobe/do_execve")
int BPF_KPROBE(kprobe_do_execve, struct filename *filename)
{ ... }

SEC("fentry/do_execve")
int BPF_PROG(fentry_execve, struct filename *filename)
{ ... }

SEC("tp/syscalls/sys_enter_execve")
int tp_sys_enter_execve(struct my_syscalls_enter_execve *ctx) { ... }

SEC("tp_btf/sched_process_exec")
int handle_exec(struct trace_event_raw_sched_process_exec *ctx) { ... }

SEC("uprobe/usr/lib/aarch64-linux-gnu/libssl.so.3/SSL_write")
```

*Ref: Learning_eBPF.md — "Tracing", "Kprobes and Kretprobes", "Fentry/Fexit", "Tracepoints", "BTF-Enabled Tracepoints", "User Space Attachments"*

---

### 37. Use fentry/fexit When You Need Args *and* Return Value

**Principle:** kretprobe gives you only the return value. fexit (kernel 5.5+) gives you both.

**Do:**
- Use the `BPF_PROG(do_unlinkat_exit, int dfd, struct filename *name, long ret)` signature for fexit.
- Use the BPF trampoline for performance (much faster than kretprobe).
- Trust that BTF makes typed parameters accessible.

**Don't:**
- Don't use kretprobe when you need input params — fexit is preferred.

**Code:**
```c
SEC("kretprobe/do_unlinkat")
int BPF_KRETPROBE(do_unlinkat_exit, long ret)
{ ... }

SEC("fexit/do_unlinkat")
int BPF_PROG(do_unlinkat_exit, int dfd, struct filename *name, long ret)
{ ... }
```

*Ref: Learning_eBPF.md — "Fentry/Fexit"*

---

### 38. Use XDP for Early Packet Decisions

**Principle:** XDP runs at the earliest point after a packet arrives on the NIC — before any sk_buff allocation, before the kernel network stack.

**Do:**
- Use the `xdp_md` context with `data`/`data_end` pointers and bounds-check at every header step.
- Use `bpf_ntohs()` for byte-order conversion from network (big-endian) to host.
- Pick the right verdict: `XDP_PASS`, `XDP_DROP`, `XDP_TX`, `XDP_REDIRECT`, `XDP_ABORTED`.
- For offload-capable NICs, packets never touch the host CPU.
- Use `eth->h_proto == ETH_P_IP` (with `bpf_ntohs`) to filter non-IP packets early.

**Don't:**
- Don't modify `data_end` — `R3 pointer arithmetic on pkt_end prohibited`.
- Don't expect to return 0 for "OK" — `0 == XDP_ABORTED` and will drop your SSH connection if attached to eth0.
- Don't skip bounds checks — `if (data + sizeof(struct ethhdr) > data_end) return XDP_PASS;` is mandatory.

**Code:**
```c
SEC("xdp")
int ping(struct xdp_md *ctx) {
   long protocol = lookup_protocol(ctx);
   if (protocol == 1) // ICMP
   {
       bpf_printk("Hello ping");
   }
   return XDP_PASS;
}

unsigned char lookup_protocol(struct xdp_md *ctx)
{
   unsigned char protocol = 0;
   void *data = (void *)(long)ctx->data;
   void *data_end = (void *)(long)ctx->data_end;
   struct ethhdr *eth = data;
   if (data + sizeof(struct ethhdr) > data_end)
       return 0;
   // Check that it's an IP packet
   if (bpf_ntohs(eth->h_proto) == ETH_P_IP)
   {
       // Return the protocol of this packet
       // 1 = ICMP
       // 6 = TCP
       // 17 = UDP
       struct iphdr *iph = data + sizeof(struct ethhdr);
       if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) <= data_end)
           protocol = iph->protocol;
   }
   return protocol;
}
```

*Ref: Learning_eBPF.md — "Packet Drops", "XDP Program Return Codes", "XDP Packet Parsing"*

---

### 39. Build Load Balancers and Forwarders with XDP_TX

**Principle:** Modify IP/MAC addresses in place, recalc the IP checksum, and bounce back out the same interface with `XDP_TX`.

**Do:**
- Use `bpf_get_prandom_u32()` for backend selection.
- Update `iph->saddr`, `iph->daddr`, `eth->h_source[5]`, `eth->h_dest[5]` for routing.
- Recalculate `iph->check = iph_csum(iph)` after modifying addresses.
- Process only `iph->protocol == IPPROTO_TCP` to keep the example simple.
- Attach inside the container so `eth0` is the right virtual interface.

**Don't:**
- Don't forget the checksum recalculation — the receiver will drop the packet.
- Don't ship the example as-is — it has hard-coded addresses and assumes a Docker setup.

**Code:**
```c
SEC("xdp_lb")
int xdp_load_balancer(struct xdp_md *ctx)
{
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    struct ethhdr *eth = data;
    if (data + sizeof(struct ethhdr) > data_end)
        return XDP_ABORTED;
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;
    struct iphdr *iph = data + sizeof(struct ethhdr);
    if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) > data_end)
        return XDP_ABORTED;
    if (iph->protocol != IPPROTO_TCP)
        return XDP_PASS;
    if (iph->saddr == IP_ADDRESS(CLIENT))
    {
        char be = BACKEND_A;
        if (bpf_get_prandom_u32() % 2)
            be = BACKEND_B;
        iph->daddr = IP_ADDRESS(be);
        eth->h_dest[5] = be;
    }
    else
    {
        iph->daddr = IP_ADDRESS(CLIENT);
        eth->h_dest[5] = CLIENT;
    }
    iph->saddr = IP_ADDRESS(LB);
    eth->h_source[5] = LB;
    iph->check = iph_csum(iph);
    return XDP_TX;
}
```

```makefile
xdp: $(BPF_OBJ)
   bpftool net detach xdpgeneric dev eth0
   rm -f /sys/fs/bpf/$(TARGET)
   bpftool prog load $(BPF_OBJ) /sys/fs/bpf/$(TARGET)
   bpftool net attach xdpgeneric pinned /sys/fs/bpf/$(TARGET) dev eth0
```

*Ref: Learning_eBPF.md — "Load Balancing and Forwarding"*

---

### 40. Use TC for Egress, sk_buff Access, and Program Chaining

**Principle:** TC programs run later in the stack with `sk_buff` access, support both ingress and egress, and can be chained.

**Do:**
- Use TC when you need egress (XDP only does ingress).
- Use TC when you need `sk_buff` access — XDP runs before `sk_buff` is created.
- Chain programs (multiple TC classifiers in sequence).
- Use `TC_ACT_SHOT` to drop, `TC_ACT_OK` to pass, `TC_ACT_UNSPEC` to defer, `TC_ACT_REDIRECT` to send elsewhere.
- Use `bpf_clone_redirect()` to send a clone back out — original goes to `TC_ACT_SHOT`.

**Don't:**
- Don't use TC when XDP would suffice — XDP is faster.
- Don't forget that `TC_ACT_OK` doesn't mean "stop" — there may be more classifiers.

**Code:**
```c
int tc_drop(struct __sk_buff *skb) {
  bpf_trace_printk("[tc] dropping packet\n");
  return TC_ACT_SHOT;
}

int tc(struct __sk_buff *skb) {
  void *data = (void *)(long)skb->data;
  void *data_end = (void *)(long)skb->data_end;
  if (is_icmp_ping_request(data, data_end)) {
    struct iphdr *iph = data + sizeof(struct ethhdr);
    struct icmphdr *icmp = data + sizeof(struct ethhdr) + sizeof(struct iphdr);
    bpf_trace_printk("[tc] ICMP request for %x type %x\n", iph->daddr,
                     icmp->type);
    return TC_ACT_SHOT;
  }
  return TC_ACT_OK;
}

int tc_pingpong(struct __sk_buff *skb) {
  void *data = (void *)(long)skb->data;
  void *data_end = (void *)(long)skb->data_end;
  if (!is_icmp_ping_request(data, data_end)) {
    return TC_ACT_OK;
  }
  struct iphdr *iph = data + sizeof(struct ethhdr);
  struct icmphdr *icmp = data + sizeof(struct ethhdr) + sizeof(struct iphdr);
  swap_mac_addresses(skb);
  swap_ip_addresses(skb);
  // Change the type of the ICMP packet to 0 (ICMP Echo Reply)
  // (was 8 for ICMP Echo request)
  update_icmp_type(skb, 8, 0);
  // Redirecting a clone of the modified skb back to the interface
  // it arrived on
  bpf_clone_redirect(skb, skb->ifindex, 0);
  return TC_ACT_SHOT;
}
```

*Ref: Learning_eBPF.md — "Traffic Control (TC)"*

---

### 41. Trace Encrypted Traffic via SSL_*() Uprobes

**Principle:** Up to the moment of encryption (and just after decryption), the data is in the clear. Hooking SSL_write/SSL_read via uprobes gets you the plaintext without keys.

**Do:**
- Use uprobe on entry to `SSL_write()` and `SSL_read()` to capture the buffer pointer (second arg) into a map keyed by PID+TGID.
- Use uretprobe on exit to read the decrypted buffer.
- Support `OpenSSL`, `BoringSSL`, `GnuTLS`, `NSS` (the `sslsniff` tool covers all four).
- Pass the cleartext through a perf buffer to user space.

**Don't:**
- Don't rely on this for every app — statically linked binaries don't have the shared library to probe.
- Don't assume container paths match host paths for the SSL library.
- Don't use this as your only security tool — TOCTOU concerns apply at the user-space boundary too.

**Code:**
```c
static int process_SSL_data(struct pt_regs* ctx, uint64_t id, enum
ssl_data_event_type type, const char* buf) {
    ...
    bpf_probe_read(event->data, event->data_len, buf);
    tls_events.perf_submit(ctx, event, sizeof(struct ssl_data_event_t));
    return 0;
}

// Function signature being probed:
// int SSL_read(SSL *s, void *buf, int num)
int probe_entry_SSL_read(struct pt_regs* ctx) {
  uint64_t current_pid_tgid = bpf_get_current_pid_tgid();
  ...
  const char* buf = (const char*)PT_REGS_PARM2(ctx);
  active_ssl_read_args_map.update(&current_pid_tgid, &buf);
  return 0;
}

int probe_ret_SSL_read(struct pt_regs* ctx) {
  uint64_t current_pid_tgid = bpf_get_current_pid_tgid();
  ...
  const char** buf = active_ssl_read_args_map.lookup(&current_pid_tgid);
  if (buf != NULL) {
    process_SSL_data(ctx, current_pid_tgid, kSSLRead, *buf);
  }
  active_ssl_read_args_map.delete(&current_pid_tgid);
  return 0;
}
```

*Ref: Learning_eBPF.md — "Packet Encryption and Decryption", "User Space SSL Libraries"*

---

### 42. Replace kube-proxy/iptables with Cilium eBPF

**Principle:** iptables updates are O(n) and rewrite fully on every pod change; eBPF hash-map lookups are O(1) and incremental.

**Do:**
- Use Cilium's eBPF implementation of kube-proxy for any non-trivial Kubernetes cluster.
- Expect 5-hour iptables reloads for 20k services to become seconds.
- Use Cilium's TC, XDP, and socket-layer programs in concert.
- Use Cilium's NetworkPolicy CRD for label-based and DNS-based policy.

**Don't:**
- Don't depend on iptables-based CNIs at scale — they can't keep up.
- Don't rely on IP-address-based firewall rules in Kubernetes — addresses come and go.

*Ref: Learning_eBPF.md — "eBPF and Kubernetes Networking", "Avoiding iptables", "Coordinated Network Programs"*

---

### 43. Use Cilium NetworkPolicy for Cloud-Native Firewalling

**Principle:** NetworkPolicy uses labels (stable identity), not IPs (transient), and Cilium extends it with DNS names and Layer 7 rules.

**Do:**
- Define NetworkPolicy based on pod labels.
- Use Cilium's DNS-aware policy to allow traffic by hostname, not IP.
- Use Cilium's L7 rules to allow HTTP GET but deny HTTP POST to specific paths.
- Treat NetworkPolicy as a CNI feature — CNIs that don't support it silently ignore your rules.

**Don't:**
- Don't try to maintain IP-based firewall rules in Kubernetes.
- Don't assume every CNI supports the Kubernetes-native NetworkPolicy.

*Ref: Learning_eBPF.md — "Network Policy Enforcement"*

---

### 44. Use Transparent Encryption Between Nodes

**Principle:** eBPF + WireGuard/IPsec gives you cluster-wide encryption with no application awareness and no mTLS overhead.

**Do:**
- Use IPsec or WireGuard (both supported by Cilium and Calico) between nodes.
- Combine with NetworkPolicy for layered security.
- Extend with SPIFFE/SPIRE for per-application identity.
- Trust that this works for any IP-borne protocol (not just TCP/TLS).

**Don't:**
- Don't enforce mTLS in every app when the network layer can do it transparently.
- Don't ignore that mTLS only works for TCP — kernel-level encryption handles all IP.

*Ref: Learning_eBPF.md — "Encrypted Connections"*

---

### 45. Use seccomp-bPF for Application Allowlisting, Not Detection

**Principle:** Seccomp profiles are deny-by-default-style allowlists for syscalls. eBPF programs help *generate* profiles; the enforcement happens via the kernel's seccomp mechanism.

**Do:**
- Use BCC-based or Inspektor Gadget-based seccomp profilers to capture actual syscall usage.
- Generate a JSON seccomp profile for each container.
- Pin the profile at process start; you cannot modify it mid-flight.
- Remember seccomp-bPF cannot dereference user-space pointers (a feature for safety, not a limitation).

**Don't:**
- Don't rely on the Docker default profile — it allows most syscalls.
- Don't expect seccomp_unotify to implement security policy — TOCTOU applies; the manpage explicitly forbids it.
- Don't write seccomp-bPF in C from scratch when a profiler will do.

*Ref: Learning_eBPF.md — "Seccomp", "Generating Seccomp Profiles"*

---

### 46. Use BPF LSM for Kernel-State Enforcement

**Principle:** LSM hooks fire after parameters are copied into kernel memory, eliminating the TOCTOU window that plagues syscall-entry observation.

**Do:**
- Attach a BPF_PROG_TYPE_LSM program with `SEC("lsm/<hook_name>")` (kernel 5.7+).
- Return 0 to allow, nonzero to deny — kernel aborts the operation.
- Combine with contextual data (path, mode, etc.) for fine-grained policy.
- Trust that the LSM interface is stable — it was designed for kernel modules originally.

**Don't:**
- Don't try to use LSM BPF on pre-5.7 kernels.
- Don't assume you can access all kernel state from an LSM hook — the hook arguments are constrained.

**Code:**
```c
SEC("lsm/path_chmod")
int BPF_PROG(path_chmod, const struct path *path, umode_t mode)
{
   bpf_printk("Change mode of file name %s\n", path->dentry->d_iname);
   return 0;
}
```

*Ref: Learning_eBPF.md — "BPF LSM"*

---

### 47. Use Cilium Tetragon for Internal-Function Security

**Principle:** Tetragon hooks arbitrary kernel functions (not just syscalls/LSM) to inspect things after the kernel has set up its internal state.

**Do:**
- Define a `TracingPolicy` CRD matching the eBPF attachment and conditions.
- Use stable internal functions like `fd_install` (called after a file is opened) for safe inspection.
- Start in audit mode (emit events) before enabling SIGKILL prevention.
- Trust that the Tetragon team includes kernel developers who pick safe attach points.

**Don't:**
- Don't enable SIGKILL policies without extensive audit-mode testing — a wrong rule kills production pods.
- Don't expect internal kernel function signatures to be stable across versions.

**Code:**
```yaml
spec:
 kprobes:
 - call: "fd_install"
...
     matchArgs:
     - index: 1
       operator: "Prefix"
       values:
       - "/etc/"
...
```

*Ref: Learning_eBPF.md — "Cilium Tetragon", "Attaching to Internal Kernel Functions", "Preventative Security"*

---

### 48. Use Falco for Syscall-Tracking Detection

**Principle:** Falco provides ready-made syscall-based security rules with a vibrant ecosystem. Use it when you need quick wins.

**Do:**
- Use the eBPF driver (not the kernel module) for dynamic loading.
- Define rules in YAML/Falco-rules format.
- Combine with audit-mode (not block) until confidence is built.
- Be aware of TOCTOU — Falco is detection, not enforcement.

**Don't:**
- Don't rely on Falco as your sole security control — combine with LSM-based enforcement.
- Don't expect it to block — it observes.

*Ref: Learning_eBPF.md — "Syscall-Tracking Security Tools"*

---

### 49. Use bpftrace for One-Off Tracing

**Principle:** bpftrace is the awk-style high-level language for eBPF. Ideal for one-liners and quick investigation.

**Do:**
- Use `bpftrace -l "*execve*"` to discover attachments.
- Use `bpftrace -e 'kprobe:do_execve { @[comm] = count(); }'` for instant histograms.
- Use multi-probe scripts (e.g., opensnoop) that coordinate entry/exit.
- Inspect loaded programs with bpftool while bpftrace runs.

**Don't:**
- Don't write production tools in bpftrace — it's built on BCC (runtime compile, distribution overhead).
- Don't expect full eBPF capabilities — bpftrace is tracing/perf-related only.

**Code:**
```bash
$ bpftrace -l "*execve*"
tracepoint:syscalls:sys_enter_execve
tracepoint:syscalls:sys_exit_execve
...
kprobe:do_execve_file
kprobe:do_execve
kprobe:__ia32_sys_execve
kprobe:__x64_sys_execve

$ bpftrace -e 'kprobe:do_execve { @[comm] = count(); }'
Attaching 1 probe...
^C
@[node]: 6
@[sh]: 6
@[cpuUsage.sh]: 18
```

*Ref: Learning_eBPF.md — "Bpftrace"*

---

### 50. Use BCC for Quick Tooling, Not Production Distribution

**Principle:** BCC compiles eBPF at runtime on the destination. Convenient for learning and prototyping; expensive for distribution.

**Do:**
- Use BCC's Python framework when you want to ship a small tool fast.
- Use BCC's macros (`BPF_HASH`, `BPF_RINGBUF_OUTPUT`) to keep C-like code short.
- Use BCC's ctypes integration to pass typed values to maps.

**Don't:**
- Don't ship BCC-based tools to large fleets — every machine needs the LLVM toolchain and kernel headers.
- Don't expect low startup latency — runtime compilation adds seconds.
- Don't use BCC for embedded devices that lack the resources to compile.

**Code:**
```python
#!/usr/bin/python3
from bcc import BPF
program = """
BPF_RINGBUF_OUTPUT(output, 1);
...
int hello(void *ctx) {
  ...
   output.ringbuf_output(&data, sizeof(data), 0);
   return 0;
}
"""
b = BPF(text=program)
...
b["output"].open_ring_buffer(print_event)
...
```

*Ref: Learning_eBPF.md — "BCC Python/Lua/C++", "BCC's Approach to Portability"*

---

### 51. Use libbpf + C for Production Distribution

**Principle:** libbpf + Clang (or GCC 12+) is the gold standard for portable, distributable eBPF tooling.

**Do:**
- Use `libbpf-bootstrap` as your starting template.
- Compile with `clang -target bpf -g -O2 -D __TARGET_ARCH_<arch>`.
- Generate a BPF skeleton with `bpftool gen skeleton`.
- Use `libxdp` on top of libbpf for XDP-specific helpers.
- Note the dramatic memory savings: libbpf-based opensnoop is ~9 MB vs BCC's ~80 MB.

**Don't:**
- Don't forget `-D __TARGET_ARCH_<arch>`.
- Don't ship the `.o` file alongside — embed it via the skeleton.
- Don't skip `llvm-strip -g` if size matters.

*Ref: Learning_eBPF.md — "C and Libbpf", "Libbpf Code Examples"*

---

### 52. Use cilium/ebpf for Production Go Tooling

**Principle:** cilium/ebpf (~4k stars, ~10k references) is the dominant Go eBPF library. It implements CO-RE natively in pure Go.

**Do:**
- Use `bpf2go` to embed eBPF bytecode into Go binaries.
- Generate separate `bpf_bpfeb.go` (big-endian) and `bpf_bpfel.go` (little-endian) files; the right one is selected at compile time.
- Use the generated `bpfObjects` struct with `bpfPrograms` and `bpfMaps` to drive the program.
- Trust the typed `link.Kprobe(...)` and `objs.KprobeExecve` accessors.

**Don't:**
- Don't use the older `gobpf` library — it's largely unmaintained.
- Don't confuse libbpfgo (CGo wrapper around libbpf) with cilium/ebpf (pure Go).
- Don't expect libbpfgo's CGo boundary to be free — performance and operational concerns exist.

**Code:**
```go
//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -cc $BPF_CLANG
//                     -cflags $BPF_CFLAGS bpf <C filename> -- -I../headers
```

```go
objs := bpfObjects{}
loadBpfObjects(&objs, nil)
defer objs.Close()

kp, _ := link.Kprobe("sys_execve",
                     objs.KprobeExecve, nil)
defer kp.Close()
ticker := time.NewTicker(1 * time.Second)
defer ticker.Stop()
for range ticker.C {
    var value uint64
    objs.KprobeMap.Lookup(mapKey, &value)
    log.Printf("%s called %d times\n", fn, value)
}
```

*Ref: Learning_eBPF.md — "Go", "Gobpf", "Ebpf-go", "Libbpfgo"*

---

### 53. Use Aya for Production Rust Tooling

**Principle:** Aya is built directly on the syscall level — no libbpf, no LLVM dependency — and supports the same CO-RE relocations as libbpf.

**Do:**
- Write both kernel-side and user-side code in Rust.
- Use `#[xdp(name="myapp")]` annotations to define section names.
- Use `Bpf::load(include_bytes_aligned!(...))?` to load bytecode.
- Use `aya-tool` to auto-generate Rust definitions for kernel structs.
- Lean on Aya's excellent docs ("The Aya book") for getting started.

**Don't:**
- Don't use `libbpf-rs` if you want pure-Rust kernel code — it requires C kernel-side.
- Don't expect Redbpf to be the future — Aya has more momentum.

**Code:**
```rust
#[xdp(name="myapp")]
pub fn myapp(ctx: XdpContext) -> u32 {
    match unsafe { try_myapp(ctx) } {
        Ok(ret) => ret,
        Err(_) => xdp_action::XDP_ABORTED,
    }
}
unsafe fn try_myapp(ctx: XdpContext) -> Result<u32, u32> {
    info!(&ctx, "received a packet");
    Ok(xdp_action::XDP_PASS)
}
```

```rust
let mut bpf = Bpf::load(include_bytes_aligned!(
   "../../target/bpfel-unknown-none/release/myapp"
))?;
let program: &mut Xdp = bpf.program_mut("myapp").unwrap().try_into()?;
program.load()?;
program.attach(&opt.iface, XdpFlags::default())
```

*Ref: Learning_eBPF.md — "Rust", "Libbpf-rs", "Redbpf", "Aya"*

---

### 54. Pick a Language by Use Case, Not Preference

**Principle:** Kernel-side must be C or Rust. User-side is open. Choose based on distribution, performance, and team experience.

**Do:**
- Use bpftrace for ad-hoc investigation.
- Use BCC Python/Lua/C++ for quick prototypes.
- Use C + libbpf for widely-distributed tooling and lowest memory footprint.
- Use cilium/ebpf (Go) when your team is Go-first and you need a single binary.
- Use Aya (Rust) when memory safety matters and you can go pure-Rust kernel-side.
- Consider language runtimes — Go/Java garbage collectors and concurrency primitives are incompatible with the verifier.

**Don't:**
- Don't try to compile Go directly to eBPF — the runtime is incompatible.
- Don't assume "Rust kernel-side" is a given — Aya is the only mature option.
- Don't pick a language because it's fashionable; pick it because the tooling, distribution model, and team match.

*Ref: Learning_eBPF.md — "Language Choices for eBPF in the Kernel", "BCC Python/Lua/C++", "C and Libbpf", "Go", "Rust"*

---

### 55. Test with BPF_PROG_RUN and bpftool Statistics

**Principle:** Two test mechanisms exist: run the program from user space (`BPF_PROG_RUN`) for unit-style tests, and enable runtime stats (`kernel.bpf_stats_enabled`) for production telemetry.

**Do:**
- Use `BPF_PROG_RUN` for unit-style tests of networking programs.
- Enable `sysctl -w kernel.bpf_stats_enabled=1` to get `run_time_ns` and `run_cnt` in `bpftool prog list`.
- Use these stats to identify hot programs and to detect regressions.

**Don't:**
- Don't expect `BPF_PROG_RUN` to support all program types — it's currently networking-focused.
- Don't forget to enable stats per-host — they cost a tiny per-instruction overhead.

**Code:**
```bash
$ sysctl -w kernel.bpf_stats_enabled=1
$ bpftool prog list
...
2179: raw_tracepoint name raw_tp_exec tag 7f6d182e48b7ed38 gpl
       run_time_ns 316876 run_cnt 4
       loaded_at 2023-01-09T11:07:31+0000 uid 0
       xlated 216B jited 264B memlock 4096B map_ids 780,777
       btf_id 953
       pids hello(19173)
```

*Ref: Learning_eBPF.md — "Testing BPF Programs"*

---

### 56. Coordinate Multiple eBPF Programs with Maps

**Principle:** Real applications need multiple programs — entry and exit, multiple syscalls, multiple events — coordinated through shared maps.

**Do:**
- Use maps as the inter-program communication channel.
- Look at opensnoop: 4 tracepoint programs (open/openat enter/exit) sharing a map keyed by TID.
- Trust that libbpf/cilium-ebpf skeletons load all programs and maps in one call.
- Allow programs to come and go dynamically — Cilium adds/removes per-pod XDP programs as pods scale.

**Don't:**
- Don't assume a one-program-per-application model.
- Don't manually attach each program — use skeletons.
- Don't forget cleanup when dynamically adding/removing programs.

*Ref: Learning_eBPF.md — "Multiple eBPF Programs"*

---

### 57. Understand the eBPF Foundation's Role

**Principle:** The eBPF Foundation coordinates cross-platform standardization; it doesn't own Linux kernel eBPF development.

**Do:**
- Track the foundation for cross-OS standards (especially for Windows compatibility).
- Follow maintainers Alexei Starovoitov and Andrii Nakryiko (Meta) and Daniel Borkmann (Isovalent).
- Recognize that Cilium, Pixie, Falco live under CNCF (cloud-native), not the eBPF Foundation.

**Don't:**
- Don't expect the Foundation to develop kernel features — that's still upstream.
- Don't assume Windows eBPF is production-ready without checking.

*Ref: Learning_eBPF.md — "The eBPF Foundation"*

---

### 58. Watch the Linux eBPF Roadmap

**Principle:** eBPF evolves with practically every kernel release. New capabilities arrive continuously.

**Do:**
- Track the Iovisor/BCC kernel-feature matrix for availability.
- Consider Big TCP (kernel 5.19+) for 100+ GBit/s networks.
- Follow signed eBPF programs work for supply-chain security.
- Track typed-pointer support, eBPF memory allocation, and HIDs.

**Don't:**
- Don't assume yesterday's eBPF capabilities still define the platform — verify against your target kernel.
- Don't write code that depends on bleeding-edge features without checking distro support.

*Ref: Learning_eBPF.md — "Linux eBPF Evolution"*

---

### 59. Cross-OS eBPF Reuses Components but Not the Linux Verifier

**Principle:** eBPF for Windows reuses libbpf and Clang eBPF support, but uses PREVAIL verifier and uBPF JIT due to GPL.

**Do:**
- Treat cross-OS as similar to cross-kernel-version portability.
- Verify/JIT in a Windows Secure user-space environment, not in the kernel.
- Expect some Linux programs to need adjustment for Windows.

**Don't:**
- Don't assume every Linux eBPF program will run unchanged on Windows.
- Don't expect the Linux kernel verifier to be reused — license forbids it.

*Ref: Learning_eBPF.md — "eBPF for Windows"*

---

### 60. Treat eBPF as a Platform When Picking Vendors and Tools

**Principle:** "Built on eBPF" implies significant advantages in performance, observability, and security — choose tools with this property.

**Do:**
- Prefer eBPF-based networking (Cilium) over iptables-based (Calico legacy, kube-proxy default).
- Prefer eBPF-based security (Tetragon, Falco) over module-based or in-app instrumentation.
- Prefer eBPF-based profiling (Parca) for continuous low-overhead CPU profiling.
- Recognize that even if you don't write eBPF, you'll use tools that depend on it.

**Don't:**
- Don't dismiss eBPF as "just a kernel feature" — it's the platform.
- Don't expect users to know they're using eBPF — it should just work.

*Ref: Learning_eBPF.md — "eBPF Is a Platform, Not a Feature", "The Future Evolution of eBPF"*

---

## Anti-Patterns & Common Mistakes

- **Forgetting the `SEC("license")` declaration:** Verifier rejects GPL-only helper calls. → *fix:* `char LICENSE[] SEC("license") = "Dual BSD/GPL";`.
- **Skipping `-O2`:** Clang emits `callx <register>` which the verifier rejects. → *fix:* always `-O2`.
- **Forgetting `-D __TARGET_ARCH_<arch>`:** BPF_KPROBE macros depend on it. → *fix:* pass it in the Makefile.
- **Building production tools on BCC:** Runtime compilation requires toolchains on every host. → *fix:* migrate to libbpf.
- **Returning `XDP_DROP` by accident:** `0 == XDP_ABORTED`, not `XDP_PASS`. A wrong return can drop your SSH session. → *fix:* explicit `XDP_PASS` or `XDP_DROP`.
- **Modifying `data_end` in XDP:** Verifier says `R3 pointer arithmetic on pkt_end prohibited`. → *fix:* bounds-check before every header read; never modify `data_end`.
- **Off-by-one in array bounds:** `if (c <= sizeof(arr))` fails; use `<`. → *fix:* explicit `< sizeof(arr)`.
- **Dereferencing a NULL `bpf_map_lookup_elem` result:** Verifier catches it. → *fix:* always `if (p != 0)` check.
- **Relying on syscall-entry observation for security:** TOCTOU window. → *fix:* use BPF LSM or Tetragon attaching to internal kernel functions.
- **Using `seccomp_unotify` for security policy:** Manpage explicitly forbids it. → *fix:* use the deny-via-BPF model.
- **Calling `bpf_get_current_pid_tgid()` from XDP:** No current process. → *fix:* match helpers to program type via `bpftool feature`.
- **Unbounded loops:** `for (int i=0; i<c; i++)` where `c` is a global — verifier hits complexity limit. → *fix:* use `bpf_loop()` or a provable bound.
- **Forgetting the four per-CPU `perf_event_open` calls when reasoning about perf buffers:** It's not a bug, but if you trace through it without expecting 4 FDs you get confused. → *fix:* read chapter 4 of the book.
- **Leaving stale pinned objects in `/sys/fs/bpf/`:** Reference counts stay high; programs don't unload. → *fix:* clean up pins; use BPF links instead.
- **Expecting BCC to support BPF-to-BPF calls:** It doesn't. → *fix:* use libbpf or keep functions inlined.
- **Confusing `bpf_printk()` (libbpf) with `bpf_trace_printk()` (BCC):** They wrap the same kernel helper but are different functions in different headers. → *fix:* pick a framework and stay consistent.
- **Building a stateless BCC program with global variables:** BCC doesn't support globals; use libbpf or refactor. → *fix:* migrate or scope variables to the function.
- **Treating XDP as bidirectional:** XDP is ingress only. → *fix:* use TC for egress.
- **Assuming BPF links are always needed:** Some attachment types (XDP, TC) hold their own references. → *fix:* pin only when you need cross-process lifetime.
- **Skipping the verifier log when debugging:** The log tells you exactly which path failed. → *fix:* compile with `-g`, install a log handler, and read it.
- **Testing in production:** Always audit-mode before SIGKILL. → *fix:* shadow deploy, watch false positives, then enable prevent.

## Decision Heuristics / Checklists

- **Which framework?**
  - Ad-hoc investigation → `bpftrace`.
  - Quick prototype → `BCC` (Python).
  - Widely distributed production tool → `libbpf` (C).
  - Go-only team, single binary → `cilium/ebpf`.
  - Memory-safe kernel + user space → `Aya` (Rust).
- **Which map type?**
  - Generic KV → `BPF_MAP_TYPE_HASH`.
  - 4-byte int key → `BPF_MAP_TYPE_ARRAY`.
  - Config per CPU → per-CPU variant.
  - Event stream from kernel → perf event array (legacy) or ring buffer (kernel 5.8+).
  - Aging memory-bound → LRU hash.
  - Routing lookups → LPM trie.
  - Probabilistic "definitely not" → Bloom filter.
- **Perf buffer or ring buffer?**
  - Minimum kernel ≥ 5.8 → ring buffer.
  - Need per-CPU ordering semantics → perf buffer.
- **Which attachment?**
  - Stable kernel hook → tracepoint (`tp/...`) or BTF-enabled (`tp_btf/...`).
  - Non-inlined internal function → fentry/fexit (kernel 5.5+) preferred; kprobe fallback.
  - User-space function → uprobe (entry args), uretprobe (return value).
  - Packet ingress, need maximum speed → XDP.
  - Egress or sk_buff access → TC.
  - File/socket authorization → LSM (kernel 5.7+).
- **How to ship?**
  - Same kernel everywhere, simple → BCC.
  - Different kernels across fleet → libbpf + CO-RE + skeleton.
  - Single Go binary → cilium/ebpf with `bpf2go`.
  - Pure Rust → Aya.
- **Verifying a verifier error?**
  - Find `R<n> invalid mem access 'map_value_or_null'` → add NULL check.
  - Find `R<n> pointer arithmetic on pkt_end prohibited` → remove the arithmetic on `data_end`.
  - Find `R<n> type=fp expected=map_ptr` → pass the right type.
  - Find `R<n> max value is outside of the allowed memory range` → tighten bounds.
  - Find `R0 !read_ok` → initialize R0 / add a return.
  - Find `cannot call GPL-restricted function from non-GPL compatible program` → change license or stop using GPL helper.
- **Security policy location?**
  - Syscall allowlist → seccomp.
  - File/socket decision → LSM BPF.
  - Internal-state inspection → Tetragon.
  - Network policy → Cilium NetworkPolicy at TC/XDP.
  - Detection only (audit) → Falco.
- **Capabilities?**
  - Tracing programs → `CAP_PERFMON` + `CAP_BPF`.
  - Networking programs → `CAP_NET_ADMIN` + `CAP_BPF`.
  - Catch-all dev → `CAP_SYS_ADMIN`.
- **Compile flags (libbpf):** `-target bpf -g -O2 -D __TARGET_ARCH_<arch> -Wall`; strip with `llvm-strip -g`.
- **Stack budget:** 512 bytes; track every active BPF-to-BPF call.
- **Instruction limit:** 1,000,000 verified instructions per program (lower for unprivileged).
- **Tail calls:** Up to 33 chained.
- **Verifier state pruning interval:** every 10 instructions.
- **Map spin locks:** kernel 5.1+; hash and array maps only; not in tracing or socket-filter programs.

## Key Takeaways

1. **eBPF is a verified, JIT-compiled kernel runtime.** No module, no reboot, no application change — but the verifier enforces safety on every path.
2. **Three pillars:** observability (kprobes/tracepoints), networking (XDP/TC/sockets), security (LSM/seccomp/Tetragon).
3. **CO-RE + BTF + libbpf** is the production distribution model. BCC's runtime compile is for prototyping only.
4. **The verifier is your friend.** Compile with `-g`, read the log, embrace the bounds checks — they catch real bugs.
5. **Ring buffers over perf buffers on kernel 5.8+.** Single buffer, epoll, cross-core ordering.
6. **Choose attachments wisely.** Prefer stable (tracepoints, fentry, LSM); use kprobes for non-inlined internals; XDP for early packet decisions.
7. **TOCTOU is real.** Syscall-entry observation is not security — use LSM or post-allocation hooks for enforcement.
8. **Cloud-native superpower.** One kernel, all containers, no sidecars — eBPF sees everything.
9. **Pick your language stack carefully.** libbpf/C for distribution, cilium/ebpf for Go, Aya for pure-Rust, bpftrace for one-liners.
10. **Trust the bpf() syscall vocabulary.** Every library ultimately uses these commands; knowing them helps debug any tool.
11. **Pinning and BPF links** are the lifecycle primitives — programs outlive the loader through them.
12. **Performance is real.** XDP gives 2.5× routing and 4.3× load-balancing wins; JIT means no kernel/user-space transitions per event.
13. **The verifier and JIT evolve continuously.** 1M instruction limit, bounded loops, bpf_loop(), typed pointers — check your target kernel's matrix.
14. **The verifier rejects:** OOB access, NULL deref, unbounded loops, GPL misuse, type mismatch, invalid opcodes, unreachable code, uninitialized R0.
15. **eBPF is a platform, not a feature.** Most users consume it through tools, not directly — but knowing its internals makes you a better consumer and creator.

## Cross-References
- Related: [[./Building_Microservices.md]]
- Related: [[./Designing_Distributed_Systems.md]]
- Related: [[./Concurrency_in_Go.md]]
- Related: [[./Learning_Domain_Driven_Design.md]]
- Related: [[./Linux_BPF_Performance_Tools.md]]
- Related: [[../INDEX.md]]