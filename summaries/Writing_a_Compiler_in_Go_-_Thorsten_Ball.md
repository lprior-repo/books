# Writing a Compiler in Go - Thorsten Ball

## Comprehensive Summary

This book is the sequel to *Writing an Interpreter in Go*. It takes the tree-walking interpreter built in the first book and replaces it with a bytecode compiler and a virtual machine (VM), achieving roughly 3x performance improvement. The book walks through building both components from scratch for the Monkey programming language, covering opcodes, bytecode encoding, stack-based computation, jump instructions, closures, and more.

---

## Introduction and Motivation

The Monkey language supports integers, booleans, strings, arrays, hashes, prefix/infix/index operators, conditionals, global and local bindings, first-class functions, return statements, and closures. In the first book, these were implemented via a tree-walking interpreter: lexer tokenizes source into tokens, a Pratt parser builds an AST, and a recursive `Eval` function walks the AST to produce values.

This book transforms that architecture into a bytecode compiler and VM -- one of the most common interpreter architectures, used by Ruby, Lua, Python, Perl, JavaScript implementations, and the JVM. The key benefit: bytecode interpreters are significantly faster. The compiled Monkey runs roughly 3x faster than the tree-walking interpreter.

---

## Chapter 1: Compilers and Virtual Machines

### What Is a Compiler?

A compiler is fundamentally a translator. It takes source code in one language and produces code in another language (the target language). Compilers share a frontend (lexer + parser producing an AST) with interpreters. The divergence happens after the AST: an interpreter evaluates it, while a compiler generates code in a target language.

The archetype of a compiler includes: frontend (lexer/parser), optionally an optimizer that translates the AST into another intermediate representation (IR), optimization passes, and a backend (code generator) that produces target language output. Variations are endless -- some compilers have multiple backends for multiple architectures, some omit optimization entirely, some output machine code, others output assembly or another high-level language.

### Virtual Machines

A VM is a software entity that mimics how a computer works. It has a run loop implementing the fetch-decode-execute cycle, a program counter, a stack, and sometimes registers. The two major architectural choices are:

- **Stack machines**: Easier to build; instructions are simpler but more numerous since everything goes through the stack.
- **Register machines**: More complex to build; instructions are denser since they refer to registers directly; generally fewer instructions needed.

### Real Machines and the Von Neumann Architecture

The Von Neumann architecture describes a computer with a CPU (containing an ALU, processor registers, and a control unit with an instruction register and program counter), memory (RAM), mass storage, and I/O devices. The CPU executes the fetch-decode-execute cycle: fetch an instruction from memory (using the program counter to find it), decode it, execute it, and repeat.

Memory is addressed by numbers. Data and programs share the same memory, but conventions separate them into different regions. The most important memory region for the book is **the stack** -- used to implement the call stack. The call stack tracks which function is currently executing, the return address (where to resume after the current function), function arguments, and local variables. Function calls are often nested, so a LIFO structure is ideal.

Processor registers are much faster than main memory but limited in number (e.g., 16 general-purpose 64-bit registers on x86-64). The **stack pointer** is so important that most CPUs dedicate a specific register to it.

### Bytecode

Bytecode is a sequence of opcodes (one byte each) and operands laid out in memory. Opcodes are the operator part of an instruction; their human-readable names (like PUSH, ADD) are mnemonics. Bytecode is a domain-specific language for a domain-specific machine -- specialized for the source language. The JVM has `invokeinterface`, `getstatic`, `new`; Ruby has `putself`, `send`; Lua has dedicated table/tuple instructions.

### The Plan: Build Compiler and VM Simultaneously

Building both at the same time provides fast feedback cycles. Start with a tiny VM supporting few instructions and a tiny compiler producing them, then gradually expand.

---

## Chapter 2: Hello Bytecode!

The goal is to compile and execute `1 + 2`. The data flow is: Monkey source -> tokens -> AST -> compiler -> bytecode -> VM -> result (3).

### The Code Package and First Instructions

A new `code` package defines the bytecode format:

- `Instructions` is `[]byte` (a flat byte slice)
- `Opcode` is `byte` (each opcode is one byte)
- `OpConstant` is the first opcode, with a single 2-byte operand (uint16) that serves as an index into the constant pool

Instead of embedding values directly in bytecode (which would cause bloat for strings and other types), the compiler uses a **constant pool**: it stores evaluated constant expressions (like integer literals) in a separate data structure and references them by index.

The `Definition` struct tracks each opcode's `Name` and `OperandWidths`. The `Make` function encodes an opcode and operands into a byte slice using big-endian encoding. The `ReadOperands` function decodes them. A `String()` method on `Instructions` acts as a mini-disassembler, producing human-readable output like `0000 OpConstant 0`.

### The Smallest Compiler

The `Compiler` struct contains `instructions` (generated bytecode) and `constants` (the constant pool). Its `Compile` method walks the AST recursively. For `*ast.IntegerLiteral` nodes, it creates an `*object.Integer`, adds it to the constant pool, and emits an `OpConstant` instruction referencing the constant's index. The `Bytecode` struct bundles instructions and constants together.

The `emit` helper generates an instruction and appends it, returning the position. The `addConstant` helper appends an object to the constants slice and returns its index.

### Powering On the Machine

The `VM` struct holds constants, instructions, a preallocated stack (size 2048), and a stack pointer `sp` that always points to the next free slot. The `Run` method contains the fetch-decode-execute loop:

```go
func (vm *VM) Run() error {
    for ip := 0; ip < len(vm.instructions); ip++ {
        op := code.Opcode(vm.instructions[ip])
        switch op {
        case code.OpConstant:
            constIndex := code.ReadUint16(vm.instructions[ip+1:])
            ip += 2
            err := vm.push(vm.constants[constIndex])
            // ...
        }
    }
    return nil
}
```

For `OpConstant`, it decodes the 2-byte operand, fetches the constant, and pushes it onto the stack.

### Adding OpAdd

`OpAdd` has no operands. It pops the two topmost elements, adds them, and pushes the result. The compiler emits `OpAdd` for `+` infix expressions after compiling the left and right operands.

### Hooking Up the REPL

The REPL is updated to replace the evaluator with the compiler+VM pipeline: lex, parse, compile, execute, and print the top of the stack.

---

## Chapter 3: Compiling Expressions

### Cleaning Up the Stack: OpPop

Expression statements leave values on the stack. `OpPop` is introduced to pop the topmost element after every expression statement, preventing stack overflow from multiple expression statements.

### Infix Expressions

Four arithmetic opcodes are added: `OpAdd`, `OpSub`, `OpMul`, `OpDiv`. The compiler maps `+`, `-`, `*`, `/` to their respective opcodes. The VM's `executeBinaryOperation` method type-checks operands and delegates to `executeBinaryIntegerOperation`, which unwraps integers, performs the operation, and pushes the result.

Stack arithmetic handles operator precedence correctly because the Pratt parser has already built the correct AST structure. Complex expressions like `5 + 2 * 10` naturally decompose into the right sequence of stack operations.

### Booleans: OpTrue and OpFalse

Rather than treating `true` and `false` as constants (wasteful), two dedicated opcodes push global `True` and `False` singleton objects. This enables efficient pointer comparison for `true == true`.

### Comparison Operators

Three opcodes: `OpEqual`, `OpNotEqual`, `OpGreaterThan`. Notably, `<` is not given its own opcode. Instead, the compiler reorders `3 < 5` into `5 > 3` and emits `OpGreaterThan`. This is a simple example of code transformation during compilation. The VM's `executeComparison` handles both integer and boolean (pointer) comparisons.

### Prefix Expressions

`OpMinus` negates integers; `OpBang` negates booleans (with truthiness: everything except `False` and `Null` is truthy).

---

## Chapter 4: Conditionals

### The Challenge: Branching in Flat Bytecode

Bytecode is a flat sequence -- there is no AST to selectively traverse. The solution is **jump instructions**: `OpJumpNotTruthy` (conditional jump) and `OpJump` (unconditional jump). Each has a 2-byte operand specifying the offset to jump to.

### Compiling Conditionals

The key challenge is that jump targets are unknown when the jump instruction is emitted (the alternative branch hasn't been compiled yet). The solution is **back-patching**: emit the jump with a placeholder operand (9999), compile the remaining code, then go back and replace the placeholder with the correct offset.

The compiler tracks emitted instructions using `EmittedInstruction` structs (opcode + position) to enable back-patching. Helper methods `replaceInstruction` and `changeOperand` allow modifying already-emitted bytecode.

For `if (cond) { consequence } else { alternative }`:

1. Compile the condition
2. Emit `OpJumpNotTruthy` with placeholder
3. Compile the consequence (remove trailing `OpPop` since conditionals are expressions that produce values)
4. If there's an alternative: emit `OpJump` with placeholder, patch `OpJumpNotTruthy` target to after the consequence, compile the alternative (remove trailing `OpPop`)
5. Patch `OpJump` target to after the alternative
6. If no alternative: emit `OpNull` and patch `OpJumpNotTruthy` to jump to it

### Executing Jumps in the VM

`OpJump` sets `ip` to the target minus one (the for loop increments ip). `OpJumpNotTruthy` pops the condition, checks truthiness, and jumps if not truthy. The `isTruthy` helper returns `true` for everything except `False` and `Null`.

### Null Handling

`OpNull` pushes the global `Null` singleton. Conditionals without alternatives produce `Null`. The VM must handle `Null` in `executeBangOperator` and `isTruthy`.

---

## Chapter 5: Keeping Track of Names (Bindings)

### The Plan: OpSetGlobal and OpGetGlobal

Bindings are implemented with two new opcodes, each with a 2-byte operand. Identifiers are mapped to unique numbers via a **symbol table**. The VM stores globals in a preallocated slice (size 65536).

### The Symbol Table

The `SymbolTable` associates identifiers with `Symbol` structs containing `Name`, `Scope` (e.g., `GlobalScope`), and `Index`. It supports `Define` (associate name with a new unique index) and `Resolve` (look up a previously defined symbol).

### Compilation

For `*ast.LetStatement`: compile the value expression, define the identifier in the symbol table, emit `OpSetGlobal` with the symbol's index. For `*ast.Identifier`: resolve the name, emit `OpGetGlobal` with the symbol's index.

A notable side effect: undefined variables are now detected at **compile time** rather than run time.

### VM Implementation

`OpSetGlobal` pops the stack and stores the value at the given index in the globals slice. `OpGetGlobal` fetches the value from the globals slice and pushes it onto the stack.

### REPL Persistence

The REPL must preserve the symbol table and globals store across lines. New constructors `NewWithState` (compiler) and `NewWithGlobalsStore` (VM) allow reusing existing state.

---

## Chapter 6: String, Array and Hash

### Strings

String literals are treated as constants (their value doesn't change). The compiler creates `*object.String` objects and adds them to the constant pool. String concatenation reuses `OpAdd` -- the VM's `executeBinaryOperation` is extended with a type check for strings, delegating to `executeBinaryStringOperation`.

### Arrays

Arrays are composite types -- their value can't be determined at compile time. `OpArray` has one 2-byte operand: the number of elements. The compiler emits instructions to evaluate all element expressions (leaving N values on the stack), then emits `OpArray` with N. The VM's `buildArray` method takes N elements from the stack and constructs an `*object.Array`.

### Hashes

Similar to arrays. `OpHash` has one operand: the number of keys AND values. The compiler sorts hash keys by string representation to ensure deterministic output (Go maps iterate in random order). The VM's `buildHash` method iterates through stack elements in pairs, generating `HashKey`/`HashPair` entries.

### Index Operator: OpIndex

A single opcode `OpIndex` handles both array and hash indexing. The compiler compiles the left expression (the collection) and the index expression, then emits `OpIndex`. The VM dispatches to `executeArrayIndex` (with bounds checking, returning `Null` for out-of-bounds) or `executeHashIndex` (using `HashKey` lookup).

---

## Chapter 7: Functions

### Representing Functions

`object.CompiledFunction` holds `code.Instructions` (and later `NumLocals` and `NumParameters`). Functions are treated as constants -- their code doesn't change, so they're added to the constant pool and loaded via `OpConstant` (later `OpClosure`).

### New Opcodes

- `OpCall` (later gains a 1-byte operand for argument count): tells the VM to execute the function on top of the stack
- `OpReturnValue`: return from function with the value on top of the stack
- `OpReturn`: return from function with implicit `Null`

### Compilation Scopes

To prevent function body instructions from mingling with the main program, the compiler gains a **scope stack**. `CompilationScope` bundles `instructions`, `lastInstruction`, and `previousInstruction`. `enterScope()` pushes a new scope; `leaveScope()` pops it and returns the accumulated instructions.

### Compiling Function Literals

When compiling `*ast.FunctionLiteral`: enter a new scope, compile the body, leave the scope, wrap the instructions in a `*object.CompiledFunction`, add to constant pool, and emit an instruction to load it.

### Compiling Return Statements

`*ast.ReturnStatement` compiles the return value expression, then emits `OpReturnValue`. Implicit returns (the last expression in a function body) work because the compiler removes the trailing `OpPop` from the function body, leaving the value on the stack, and appends `OpReturnValue`. Functions with empty bodies or only let statements get an `OpReturn` appended.

### Functions in the VM: Frames

The VM uses a **frame stack** to track function calls. Each `Frame` holds a reference to the compiled function, an instruction pointer, and a `basePointer` (the stack position when the frame was created). The frame stack is preallocated to size 1024.

When `OpCall` is executed: the function is taken from the stack, a new frame is created and pushed. The VM switches to executing the function's instructions. When `OpReturnValue` or `OpReturn` is executed: the frame is popped, the stack pointer is reset using `basePointer`, and execution resumes in the calling frame.

### Local Bindings: OpSetLocal and OpGetLocal

Two new opcodes with 1-byte operands. Local bindings are stored on the stack relative to the frame's `basePointer`. The compiler's symbol table gains a `LocalScope`. When entering a function scope, parameters are defined as locals.

The `NumLocals` field on `CompiledFunction` tells the VM how many stack slots to reserve. The VM sets `vm.sp = frame.basePointer + fn.NumLocals` when entering a function, creating "the hole" -- preallocated stack slots for local bindings.

`OpSetLocal` stores the top-of-stack value at `basePointer + operand`. `OpGetLocal` pushes the value at `basePointer + operand` onto the stack. Nested scopes use `NewEnclosedSymbolTable` to create child symbol tables that can resolve names in parent scopes.

Stack cleanup on return: `vm.sp = frame.basePointer - 1` (the `-1` removes the function itself from the stack).

### Arguments

Arguments are treated as local bindings. The calling convention becomes: push the function, push all arguments, emit `OpCall` with argument count. In the compiler, function parameters are defined in the symbol table as locals (with indices 0, 1, 2, ...). References to parameters become `OpGetLocal` instructions.

The `basePointer` is adjusted: `basePointer = vm.sp - numArgs` (pointing to where the first argument sits on the stack). This ensures `basePointer + index` correctly addresses both arguments and local bindings. Wrong argument counts are caught by comparing `numArgs` with `fn.NumParameters`.

---

## Chapter 8: Built-in Functions

### Refactoring: Moving Built-ins to the Object Package

The built-in functions (`len`, `puts`, `first`, `last`, `rest`, `push`) are moved from the evaluator package to a new `object/builtins.go` file. They're stored as a slice of structs (for stable iteration order) with `GetBuiltinByName` for lookup. Functions that previously returned `evaluator.NULL` now return `nil` (bring-your-own-null strategy).

### BuiltinScope and OpGetBuiltin

A new `BuiltinScope` is added to the symbol table. Built-in functions are defined with `DefineBuiltin` during compiler initialization. A new opcode `OpGetBuiltin` (1-byte operand: index into `object.Builtins`) loads the built-in function onto the stack.

The compiler's `loadSymbol` method now dispatches based on scope: `GlobalScope` -> `OpGetGlobal`, `LocalScope` -> `OpGetLocal`, `BuiltinScope` -> `OpGetBuiltin`.

### Executing Built-in Functions

The VM's `executeCall` dispatches between `*object.Closure` (user functions) and `*object.Builtin`. The `callBuiltin` method extracts arguments from the stack, calls the built-in function, cleans up the stack (removing arguments and the function), and pushes the result (or `Null` if nil).

---

## Chapter 9: Closures

### The Problem

In the tree-walking interpreter, closures "close over" their environment at the time of definition -- the function carries a pointer to the environment. In a compiler/VM, functions are compiled to bytecode at compile time, but the values they reference (free variables) only exist at run time. The challenge: get run-time values into an already-compiled function.

### Free Variables

A **free variable** is one that is used locally but defined in an enclosing scope -- neither a local binding nor a global. The implementation revolves around detecting, tracking, and resolving free variables.

### Everything's a Closure

The `object.Closure` struct wraps a `*CompiledFunction` and a `Free []Object` slice for carrying free variables. Every function is treated as a closure (even those with zero free variables), simplifying the architecture.

`OpClosure` has two operands: a 2-byte constant index (to find the `CompiledFunction`) and a 1-byte count of free variables. The VM's `pushClosure` method wraps the function in a `Closure` and pushes it.

Frames are updated to reference `*object.Closure` instead of `*object.CompiledFunction`.

### Compiling and Resolving Free Variables

A new `FreeScope` is added to the symbol table. When `Resolve` walks up enclosing scopes and finds a symbol that is neither global nor built-in, it calls `defineFree`, which adds the original symbol to a `FreeSymbols` list and creates a new `FreeScope` symbol.

New opcode: `OpGetFree` (1-byte operand: index into the closure's `Free` slice).

The compiler's `loadSymbol` gains a `FreeScope` case emitting `OpGetFree`.

After compiling a function's body and leaving its scope, the compiler iterates through `FreeSymbols` and calls `loadSymbol` for each -- this emits instructions in the enclosing scope that push the free variable values onto the stack. Then `OpClosure` is emitted with the correct free variable count.

For deeply nested closures, a free variable in one scope might itself be a free variable from an outer scope. The symbol table handles this naturally: `defineFree` in an inner scope resolves the variable from the enclosing scope's perspective (which may also have it as a free variable).

### Creating Closures at Run Time

The VM's `pushClosure` method now also pops the free variables from the stack and stores them in the `Closure.Free` slice:

```go
func (vm *VM) pushClosure(constIndex int, numFree int) error {
    constant := vm.constants[constIndex]
    function, ok := constant.(*object.CompiledFunction)
    // ...
    free := make([]object.Object, numFree)
    copy(free, vm.stack[vm.sp-numFree:vm.sp])
    vm.sp -= numFree
    closure := &object.Closure{Fn: function, Free: free}
    return vm.push(closure)
}
```

### Recursive Closures

Recursive functions (a function that references itself) require special handling. The compiler detects when a function's name is used as a free variable within its own body (a self-reference) and emits instructions to bind the closure to its own name before the recursive call.

---

## Key Patterns and Best Practices

### Bytecode Design Principles
- Opcodes are one byte; operands use the minimum necessary width (1 byte for locals/free vars/args, 2 bytes for constants/globals/jump targets)
- Big-endian encoding for multi-byte operands
- Domain-specific opcodes keep the instruction set small and efficient
- Back-patching handles forward references in jump instructions

### Compiler Architecture
- Single-pass compiler: traverses the AST once, emitting bytecode
- Compilation scopes isolate function bodies from the main program
- Symbol table tracks identifiers across scopes (Global, Local, Builtin, Free)
- The `emit` method returns positions for later back-patching
- Tracking `lastInstruction` and `previousInstruction` enables removing/patching emitted instructions

### VM Architecture
- Stack machine with preallocated stack (2048 elements)
- Frame stack (1024 frames) implements the call stack
- Each frame holds: closure reference, instruction pointer, base pointer
- `basePointer` serves dual purpose: stack cleanup on return and reference point for local bindings
- Global singleton objects (`True`, `False`, `Null`) enable efficient pointer comparison
- The fetch-decode-execute loop is the hot path -- avoid unnecessary lookups

### Testing Strategy
- Compiler tests: parse Monkey code, compile, assert expected instructions and constants
- VM tests: parse, compile, execute, assert the value left on the stack
- Test helpers (`runCompilerTests`, `runVmTests`) abstract away boilerplate
- The disassembler (`Instructions.String()`) provides human-readable bytecode for debugging

### Performance Considerations
- The VM directly decodes opcodes in the switch statement (no `Lookup` call in the hot path)
- Preallocated stack and globals store avoid allocation overhead
- Global singleton objects for `True`, `False`, `Null` reduce allocations
- The final implementation achieves ~3x speedup over the tree-walking interpreter without low-level optimizations

---

## Complete Opcode Reference

| Opcode | Operands | Description |
|--------|----------|-------------|
| OpConstant | 2 (uint16) | Load constant from pool onto stack |
| OpPop | 0 | Pop top of stack |
| OpAdd | 0 | Add two topmost stack elements |
| OpSub | 0 | Subtract |
| OpMul | 0 | Multiply |
| OpDiv | 0 | Divide |
| OpTrue | 0 | Push True |
| OpFalse | 0 | Push False |
| OpEqual | 0 | Compare equality |
| OpNotEqual | 0 | Compare inequality |
| OpGreaterThan | 0 | Compare greater than |
| OpMinus | 0 | Negate integer |
| OpBang | 0 | Negate boolean (truthiness) |
| OpJump | 2 (uint16) | Unconditional jump |
| OpJumpNotTruthy | 2 (uint16) | Jump if top of stack is not truthy |
| OpNull | 0 | Push Null |
| OpSetGlobal | 2 (uint16) | Store value in globals |
| OpGetGlobal | 2 (uint16) | Load value from globals |
| OpArray | 2 (uint16) | Build array from N stack elements |
| OpHash | 2 (uint16) | Build hash from N stack elements |
| OpIndex | 0 | Index into array or hash |
| OpCall | 1 (uint8) | Call function with N arguments |
| OpReturnValue | 0 | Return with value from top of stack |
| OpReturn | 0 | Return with Null |
| OpSetLocal | 1 (uint8) | Store value as local binding |
| OpGetLocal | 1 (uint8) | Load local binding |
| OpGetBuiltin | 1 (uint8) | Load built-in function |
| OpClosure | 2 (uint16) + 1 (uint8) | Create closure with N free variables |
| OpGetFree | 1 (uint8) | Load free variable from closure |

---

## Architecture Summary

The complete pipeline: **Source Code -> Lexer -> Tokens -> Parser -> AST -> Compiler -> Bytecode -> VM -> Result**

The compiler translates the AST into bytecode instructions and a constant pool. The VM executes the bytecode using a stack, a globals store, a frame stack for function calls, and closures that carry free variables. The symbol table in the compiler resolves identifiers to the correct scope (global, local, builtin, or free) and emits the appropriate load/store instruction for each.
