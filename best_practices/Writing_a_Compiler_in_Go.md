# Writing a Compiler in Go
**Author:** Thorsten Ball
**Topic tags:** `#general` `#go` `#compiler`
**Language focus:** Go-first
**Sources:** `markdown_output/Writing_a_Compiler_in_Go_-_Thorsten_Ball/Writing_a_Compiler_in_Go_-_Thorsten_Ball.md` · `summaries/Writing_a_Compiler_in_Go_-_Thorsten_Ball_-_Thorsten_Ball.md`

## TL;DR
A practical, code-first sequel to *Writing an Interpreter in Go* that replaces the tree-walking interpreter with a bytecode compiler and stack-based virtual machine, achieving roughly 3x speedup. It teaches the complete pipeline — AST → compiler → bytecode → VM → result — by building each layer test-first for the Monkey language: a `code` package defines opcodes and encoding; a `compiler` package walks the AST emitting instructions and managing a constant pool, symbol table, scopes, and back-patching; a `vm` package runs a fetch-decode-execute loop over a preallocated stack and a frame-based call stack. The book ends with first-class functions, closures (via free variables and `OpCurrentClosure` for self-reference), and built-ins.

---

## Best Practices by Topic

### 1. Treat Compilation as Translation, Not Magic

**Principle:** A compiler is fundamentally a translator from one language (source) to another (target); producing an executable is only one specialization of that idea.

**Do:**
- Choose the target language deliberately based on the host machine, performance targets, and downstream tooling.
- Keep the frontend (lexer + parser → AST) shared between interpreters and compilers; divergence happens after the AST.
- Decide early whether your target is machine code, assembly, another high-level language, or bytecode for a virtual machine.

**Don't:**
- Don't assume "compiler" means "GCC-sized project" — small, focused translators are still compilers.
- Don't entangle frontend concerns (lexing/parsing) with backend concerns (code generation).

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 1 / Compilers"*

---

### 2. Choose a Stack Machine for Simplicity, a Register Machine for Density

**Principle:** The VM architecture is the single biggest influence on the bytecode format; pick the architecture before specifying opcodes.

**Do:**
- Pick a stack machine for pedagogical clarity: fewer concepts, fewer moving parts, simpler instruction encoding.
- Accept that stack machines emit more (but simpler) instructions because everything flows through the stack.
- Use register machines when instruction density and direct operand addressing matter more than implementation simplicity.

**Don't:**
- Don't speculate about performance before measuring — the book's stack VM is ~3.3x faster than the previous tree-walking interpreter without low-level tweaking.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / First Instructions"*

---

### 3. Model Bytecode as `[]byte` with One-Byte Opcodes

**Principle:** Keep the bytecode representation a flat byte slice; reserve the first byte of every instruction for the opcode and let the rest encode operands.

**Code:**
```go
// code/code.go
package code

type Instructions []byte
type Opcode byte
```

`Instructions` is just bytes — handy to pass around and avoids cumbersome type assertions from a hypothetical `Instruction` (singular) type. `Bytecode` itself is defined in the compiler package (not here) to avoid an import cycle with the `object` package.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Starting With Bytes"*

---

### 4. Use a Constant Pool Instead of Embedding Literals in Bytecode

**Principle:** Integer, string, and compiled-function literals are *constant expressions* — evaluate them at compile time, store them once in a constant pool, and reference them by index.

**Do:**
- Use a 2-byte (uint16) operand for the constant index — enough for 65,536 constants and keeps instructions compact.
- Add constants eagerly as you encounter them and reuse indices when the same value appears again.

**Don't:**
- Don't bloat bytecode by inlining strings or large literals inline.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Starting With Bytes"*

---

### 5. Define Opcodes with `iota` and a `Definition` Map

**Principle:** Define each opcode as a distinct byte value via `iota`, and pair it with a `Definition` recording its human-readable name and operand widths.

**Code:**
```go
// code/code.go
const (
    OpConstant Opcode = iota
)

var definitions = map[Opcode]*Definition{
    OpConstant: {"OpConstant", []int{2}},
}

type Definition struct {
    Name          string
    OperandWidths []int
}

func Lookup(op byte) (*Definition, error) {
    def, ok := definitions[Opcode(op)]
    if !ok {
        return nil, fmt.Errorf("opcode %d undefined", op)
    }
    return def, nil
}
```

The `iota` value itself is irrelevant — opcodes just need to be distinct and fit in one byte. `OperandWidths` lets tooling (and the disassembler) decode instructions generically.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Starting With Bytes"*

---

### 6. Encode Instructions in Big-Endian via a Single `Make` Function

**Principle:** Expose one `Make` function that turns an opcode plus variadic operands into a fully encoded `[]byte`; keep endianness explicit.

**Code:**
```go
// code/code.go
import (
    "encoding/binary"
    "fmt"
)

func Make(op Opcode, operands ...int) []byte {
    def, ok := definitions[op]
    if !ok {
        return []byte{}
    }
    instructionLen := 1
    for _, w := range def.OperandWidths {
        instructionLen += w
    }
    instruction := make([]byte, instructionLen)
    instruction[0] = byte(op)

    offset := 1
    for i, o := range operands {
        width := def.OperandWidths[i]
        switch width {
        case 2:
            binary.BigEndian.PutUint16(instruction[offset:], uint16(o))
        case 1:
            instruction[offset] = byte(o)
        }
        offset += width
    }
    return instruction
}
```

**Do:**
- Bypass `Lookup` (and its error return) inside `Make` so callers can build bytecode ergonomically without per-call error checking.
- Use `encoding/binary` so the byte order is named in code.

**Don't:**
- Don't return errors from `Make` for unknown opcodes — empty bytes on the producing side is acceptable; correctness comes from the compiler only emitting known opcodes.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Starting With Bytes"*

---

### 7. Provide a Matching `ReadOperands` for Decoding

**Principle:** Pair `Make` with a `ReadOperands` that decodes operands given a `*Definition`, plus public per-width helpers (`ReadUint16`, `ReadUint8`) the VM can call directly in its hot loop.

**Code:**
```go
// code/code.go
func ReadOperands(def *Definition, ins Instructions) ([]int, int) {
    operands := make([]int, len(def.OperandWidths))
    offset := 0
    for i, width := range def.OperandWidths {
        switch width {
        case 2:
            operands[i] = int(ReadUint16(ins[offset:]))
        case 1:
            operands[i] = int(ReadUint8(ins[offset:]))
        }
        offset += width
    }
    return operands, offset
}

func ReadUint16(ins Instructions) uint16 {
    return binary.BigEndian.Uint16(ins)
}

func ReadUint8(ins Instructions) uint8 {
    return uint8(ins[0])
}
```

The public `ReadUint16`/`ReadUint8` helpers exist so the VM can skip the `Definition` lookup in its dispatch loop.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Bytecode, Disassemble!"*

---

### 8. Give `Instructions` a `String()` Method — A Mini-Disassembler

**Principle:** Bytecode debuggability hinges on readable output; teach `Instructions` to print `"%04d %s %d\n"` lines so test failures look like `0000 OpConstant 0\n0003 OpAdd\n` instead of `\x00\x00\x00\x00\x00\x01`.

**Code:**
```go
// code/code.go
import (
    "bytes"
    // [...]
)

func (ins Instructions) String() string {
    var out bytes.Buffer
    i := 0
    for i < len(ins) {
        def, err := Lookup(ins[i])
        if err != nil {
            fmt.Fprintf(&out, "ERROR: %s\n", err)
            continue
        }
        operands, read := ReadOperands(def, ins[i+1:])
        fmt.Fprintf(&out, "%04d %s\n", i, ins.fmtInstruction(def, operands))
        i += 1 + read
    }
    return out.String()
}

func (ins Instructions) fmtInstruction(def *Definition, operands []int) string {
    operandCount := len(def.OperandWidths)
    if len(operands) != operandCount {
        return fmt.Sprintf("ERROR: operand len %d does not match defined %d\n",
            len(operands), operandCount)
    }
    switch operandCount {
    case 0:
        return def.Name
    case 1:
        return fmt.Sprintf("%s %d", def.Name, operands[0])
    case 2:
        return fmt.Sprintf("%s %d %d", def.Name, operands[0], operands[1])
    }
    return fmt.Sprintf("ERROR: unhandled operandCount for %s\n", def.Name)
}
```

**Do:**
- Add the `String()` method *before* fleshing out the compiler — early investment in debuggability pays back across every subsequent chapter.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Bytecode, Disassemble!"*

---

### 9. Start with the Smallest End-to-End Compiler

**Principle:** Build the thinnest possible slice — compile `1 + 2` to two `OpConstant` instructions — before adding features; this forces the compiler/VM contract to exist early.

**Code:**
```go
// compiler/compiler.go
package compiler

import (
    "monkey/ast"
    "monkey/code"
    "monkey/object"
)

type Compiler struct {
    instructions code.Instructions
    constants    []object.Object
}

func New() *Compiler {
    return &Compiler{
        instructions: code.Instructions{},
        constants:    []object.Object{},
    }
}

func (c *Compiler) Compile(node ast.Node) error {
    return nil
}

func (c *Compiler) Bytecode() *Bytecode {
    return &Bytecode{
        Instructions: c.instructions,
        Constants:    c.constants,
    }
}

type Bytecode struct {
    Instructions code.Instructions
    Constants    []object.Object
}
```

`Bytecode` lives in the compiler package (not `code`) specifically to avoid an import cycle with `object`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / The Smallest Compiler"*

---

### 10. Drive the Compiler with Table-Driven Tests + `t.Helper()`

**Principle:** Use Go 1.9's `t.Helper()` to factor out parse-compile-assert boilerplate so each test reads as `{input, expectedConstants, expectedInstructions}`.

**Code:**
```go
// compiler/compiler_test.go
type compilerTestCase struct {
    input                string
    expectedConstants    []interface{}
    expectedInstructions []code.Instructions
}

func runCompilerTests(t *testing.T, tests []compilerTestCase) {
    t.Helper()
    for _, tt := range tests {
        program := parse(tt.input)
        compiler := New()
        err := compiler.Compile(program)
        if err != nil {
            t.Fatalf("compiler error: %s", err)
        }
        bytecode := compiler.Bytecode()
        err = testInstructions(tt.expectedInstructions, bytecode.Instructions)
        if err != nil {
            t.Fatalf("testInstructions failed: %s", err)
        }
        err = testConstants(t, tt.expectedConstants, bytecode.Constants)
        if err != nil {
            t.Fatalf("testConstants failed: %s", err)
        }
    }
}

func parse(input string) *ast.Program {
    l := lexer.New(input)
    p := parser.New(l)
    return p.ParseProgram()
}

func concatInstructions(s []code.Instructions) code.Instructions {
    out := code.Instructions{}
    for _, ins := range s {
        out = append(out, ins...)
    }
    return out
}

func testInstructions(expected []code.Instructions, actual code.Instructions) error {
    concatted := concatInstructions(expected)
    if len(actual) != len(concatted) {
        return fmt.Errorf("wrong instructions length.\nwant=%q\ngot =%q",
            concatted, actual)
    }
    for i, ins := range concatted {
        if actual[i] != ins {
            return fmt.Errorf("wrong instruction at %d.\nwant=%q\ngot=%q",
                i, concatted, actual)
        }
    }
    return nil
}
```

`expectedInstructions` is `[]code.Instructions` (a slice of slices) so each entry can be built with `code.Make`; `concatInstructions` flattens them for comparison.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / The Smallest Compiler"*

---

### 11. Make `testConstants` a Type Switch Over Expected Constants

**Principle:** Assert the constant pool with a type-switched helper so adding new constant kinds (strings, compiled functions) is a one-line `case` extension.

**Code:**
```go
// compiler/compiler_test.go
func testConstants(
    t *testing.T,
    expected []interface{},
    actual []object.Object,
) error {
    if len(expected) != len(actual) {
        return fmt.Errorf("wrong number of constants. got=%d, want=%d",
            len(actual), len(expected))
    }
    for i, constant := range expected {
        switch constant := constant.(type) {
        case int:
            err := testIntegerObject(int64(constant), actual[i])
            if err != nil {
                return fmt.Errorf("constant %d - testIntegerObject failed: %s",
                    i, err)
            }
        case string:
            err := testStringObject(constant, actual[i])
            if err != nil {
                return fmt.Errorf("constant %d - testStringObject failed: %s",
                    i, err)
            }
        case []code.Instructions:
            fn, ok := actual[i].(*object.CompiledFunction)
            if !ok {
                return fmt.Errorf("constant %d - not a function: %T",
                    i, actual[i])
            }
            err := testInstructions(constant, fn.Instructions)
            if err != nil {
                return fmt.Errorf("constant %d - testInstructions failed: %s",
                    i, err)
            }
        }
    }
    return nil
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / The Smallest Compiler" & "Chapter 6 / String" & "Chapter 7 / Compiling Function Literals"*

---

### 12. Walk the AST Recursively in `Compile`

**Principle:** Mirror the interpreter's `Eval` recursion: a single `Compile(node ast.Node) error` switches on the concrete AST node type and recurses into children.

**Code:**
```go
// compiler/compiler.go
func (c *Compiler) Compile(node ast.Node) error {
    switch node := node.(type) {
    case *ast.Program:
        for _, s := range node.Statements {
            err := c.Compile(s)
            if err != nil {
                return err
            }
        }
    case *ast.ExpressionStatement:
        err := c.Compile(node.Expression)
        if err != nil {
            return err
        }
        c.emit(code.OpPop)
    case *ast.InfixExpression:
        err := c.Compile(node.Left)
        if err != nil {
            return err
        }
        err = c.Compile(node.Right)
        if err != nil {
            return err
        }
        switch node.Operator {
        case "+":
            c.emit(code.OpAdd)
        case "-":
            c.emit(code.OpSub)
        case "*":
            c.emit(code.OpMul)
        case "/":
            c.emit(code.OpDiv)
        case ">":
            c.emit(code.OpGreaterThan)
        case "==":
            c.emit(code.OpEqual)
        case "!=":
            c.emit(code.OpNotEqual)
        default:
            return fmt.Errorf("unknown operator %s", node.Operator)
        }
    case *ast.IntegerLiteral:
        integer := &object.Integer{Value: node.Value}
        c.emit(code.OpConstant, c.addConstant(integer))
    }
    return nil
}
```

This is the canonical single-pass compiler pattern: each node emits instructions that leave their result on the stack.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Back to the Task at Hand"*

---

### 13. `emit` Returns Its Position for Later Back-Patching

**Principle:** Keep `emit` tiny — `Make`, append, record position — and have it return the starting offset of the just-emitted instruction. That return value is the handle you'll use later to fix up forward references.

**Code:**
```go
// compiler/compiler.go
func (c *Compiler) emit(op code.Opcode, operands ...int) int {
    ins := code.Make(op, operands...)
    pos := c.addInstruction(ins)
    c.setLastInstruction(op, pos)
    return pos
}

func (c *Compiler) addInstruction(ins []byte) int {
    posNewInstruction := len(c.instructions)
    c.instructions = append(c.instructions, ins...)
    return posNewInstruction
}

func (c *Compiler) addConstant(obj object.Object) int {
    c.constants = append(c.constants, obj)
    return len(c.constants) - 1
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Back to the Task at Hand"*

---

### 14. Model the VM as Four Fields + a Stack Pointer

**Principle:** A stack VM needs very little state: the bytecode's constants, its instructions, a preallocated stack, and a stack pointer that *always* points to the next free slot.

**Code:**
```go
// vm/vm.go
package vm

import (
    "monkey/code"
    "monkey/compiler"
    "monkey/object"
)

const StackSize = 2048

type VM struct {
    constants    []object.Object
    instructions code.Instructions
    stack        []object.Object
    sp           int // Always points to the next value. Top of stack is stack[sp-1]
}

func New(bytecode *compiler.Bytecode) *VM {
    return &VM{
        instructions: bytecode.Instructions,
        constants:    bytecode.Constants,
        stack:        make([]object.Object, StackSize),
        sp:           0,
    }
}
```

**Do:**
- Preallocate the stack to a fixed `StackSize`; the sp moves, the slice never grows.
- Treat `sp` as "next free slot" so top-of-stack is always `stack[sp-1]`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Powering On the Machine"*

---

### 15. Keep Push/Pop Trivial and Bounds-Checked

**Code:**
```go
// vm/vm.go
func (vm *VM) push(o object.Object) error {
    if vm.sp >= StackSize {
        return fmt.Errorf("stack overflow")
    }
    vm.stack[vm.sp] = o
    vm.sp++
    return nil
}

func (vm *VM) pop() object.Object {
    o := vm.stack[vm.sp-1]
    vm.sp--
    return o
}

func (vm *VM) StackTop() object.Object {
    if vm.sp == 0 {
        return nil
    }
    return vm.stack[vm.sp-1]
}

func (vm *VM) LastPoppedStackElem() object.Object {
    return vm.stack[vm.sp]
}
```

`LastPoppedStackElem` works because `pop` only decrements `sp` — it doesn't nil out the slot — letting tests read "what was popped" without contortions.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Powering On the Machine" & "Chapter 3 / Cleaning Up the Stack"*

---

### 16. The Fetch-Decode-Execute Loop Is the Hot Path — Inline Everything

**Principle:** Don't call `code.Lookup` or `code.ReadOperands` inside the VM's main loop; switch directly on `Opcode` and read operands via the typed `ReadUint16`/`ReadUint8` helpers.

**Code:**
```go
// vm/vm.go
func (vm *VM) Run() error {
    for ip := 0; ip < len(vm.instructions); ip++ {
        op := code.Opcode(vm.instructions[ip])
        switch op {
        case code.OpConstant:
            constIndex := code.ReadUint16(vm.instructions[ip+1:])
            ip += 2
            err := vm.push(vm.constants[constIndex])
            if err != nil {
                return err
            }
        case code.OpAdd:
            right := vm.pop()
            left := vm.pop()
            leftValue := left.(*object.Integer).Value
            rightValue := right.(*object.Integer).Value
            result := leftValue + rightValue
            vm.push(&object.Integer{Value: result})
        }
    }
    return nil
}
```

**Don't:**
- Don't dispatch via a generic `Lookup`-then-`ReadOperands` path in `Run` — that's fine for the disassembler, not the interpreter.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Powering On the Machine"*

---

### 17. Clean the Stack After Every Expression Statement with `OpPop`

**Principle:** Expression statements wrap an expression whose value is otherwise unused; emit an `OpPop` after each one or your stack will silently grow until overflow.

**Code:**
```go
// code/code.go
const (
    // [...]
    OpPop
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpPop: {"OpPop", []int{}},
}
```

```go
// compiler/compiler.go
case *ast.ExpressionStatement:
    err := c.Compile(node.Expression)
    if err != nil {
        return err
    }
    c.emit(code.OpPop)
```

```go
// vm/vm.go
case code.OpPop:
    vm.pop()
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Cleaning Up the Stack"*

---

### 18. Use Global Singletons for `True`, `False`, `Null`

**Principle:** Booleans and Null are immutable, unique values; define them once as package-level pointers so `true == true` becomes a pointer comparison instead of an allocation.

**Code:**
```go
// vm/vm.go
var True = &object.Boolean{Value: true}
var False = &object.Boolean{Value: false}
var Null = &object.Null{}

func nativeBoolToBooleanObject(input bool) *object.Boolean {
    if input {
        return True
    }
    return False
}
```

`OpTrue`/`OpFalse`/`OpNull` are dedicated zero-operand opcodes that push these globals — cheaper than routing booleans through the constant pool.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Booleans" & "Chapter 4 / Welcome Back, Null!"*

---

### 19. Dispatch Binary Operations by Type, Then by Opcode

**Principle:** Pop operands, branch on their types, and delegate to a type-specific method that switches on the opcode; this keeps the main loop small and makes adding types (e.g., strings) a one-case change.

**Code:**
```go
// vm/vm.go
case code.OpAdd, code.OpSub, code.OpMul, code.OpDiv:
    err := vm.executeBinaryOperation(op)
    if err != nil {
        return err
    }

func (vm *VM) executeBinaryOperation(op code.Opcode) error {
    right := vm.pop()
    left := vm.pop()
    leftType := left.Type()
    rightType := right.Type()
    switch {
    case leftType == object.INTEGER_OBJ && rightType == object.INTEGER_OBJ:
        return vm.executeBinaryIntegerOperation(op, left, right)
    case leftType == object.STRING_OBJ && rightType == object.STRING_OBJ:
        return vm.executeBinaryStringOperation(op, left, right)
    default:
        return fmt.Errorf("unsupported types for binary operation: %s %s",
            leftType, rightType)
    }
}

func (vm *VM) executeBinaryIntegerOperation(
    op code.Opcode,
    left, right object.Object,
) error {
    leftValue := left.(*object.Integer).Value
    rightValue := right.(*object.Integer).Value
    var result int64
    switch op {
    case code.OpAdd:
        result = leftValue + rightValue
    case code.OpSub:
        result = leftValue - rightValue
    case code.OpMul:
        result = leftValue * rightValue
    case code.OpDiv:
        result = leftValue / rightValue
    default:
        return fmt.Errorf("unknown integer operator: %d", op)
    }
    return vm.push(&object.Integer{Value: result})
}

func (vm *VM) executeBinaryStringOperation(
    op code.Opcode,
    left, right object.Object,
) error {
    if op != code.OpAdd {
        return fmt.Errorf("unknown string operator: %d", op)
    }
    leftValue := left.(*object.String).Value
    rightValue := right.(*object.String).Value
    return vm.push(&object.String{Value: leftValue + rightValue})
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Infix Expressions" & "Chapter 6 / String"*

---

### 20. Reorder `<` Into `>` at Compile Time — Keep the Opcode Set Small

**Principle:** Compilation lets you transform source-level constructs into equivalent bytecode. `3 < 5` is observationally identical to `5 > 3`, so emit only `OpGreaterThan` and swap operand order in the compiler.

**Code:**
```go
// compiler/compiler.go
case *ast.InfixExpression:
    if node.Operator == "<" {
        err := c.Compile(node.Right)
        if err != nil {
            return err
        }
        err = c.Compile(node.Left)
        if err != nil {
            return err
        }
        c.emit(code.OpGreaterThan)
        return nil
    }
    // normal Left, Right, opcode emission...
```

This is the book's simplest demonstration of code transformation during compilation — impossible in a pure tree-walking interpreter without special cases.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Comparison Operators"*

---

### 21. Implement Truthiness Once and Reuse It

**Principle:** Define truthiness in a single helper so `OpBang`, `OpJumpNotTruthy`, and conditionals all agree.

**Code:**
```go
// vm/vm.go
func isTruthy(obj object.Object) bool {
    switch obj := obj.(type) {
    case *object.Boolean:
        return obj.Value
    case *object.Null:
        return false
    default:
        return true
    }
}

func (vm *VM) executeBangOperator() error {
    operand := vm.pop()
    switch operand {
    case True:
        return vm.push(False)
    case False:
        return vm.push(True)
    case Null:
        return vm.push(True)
    default:
        return vm.push(False)
    }
}

func (vm *VM) executeMinusOperator() error {
    operand := vm.pop()
    if operand.Type() != object.INTEGER_OBJ {
        return fmt.Errorf("unsupported type for negation: %s", operand.Type())
    }
    value := operand.(*object.Integer).Value
    return vm.push(&object.Integer{Value: -value})
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Prefix Expressions" & "Chapter 4 / Welcome Back, Null!"*

---

### 22. Model Conditionals as Conditional + Unconditional Jumps

**Principle:** Bytecode is flat — implement branching with two jump opcodes: `OpJumpNotTruthy` (pop condition, jump if falsy) and `OpJump` (unconditional). Both take a 2-byte absolute target.

**Code:**
```go
// code/code.go
const (
    // [...]
    OpJumpNotTruthy
    OpJump
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpJumpNotTruthy: {"OpJumpNotTruthy", []int{2}},
    OpJump:          {"OpJump", []int{2}},
}
```

```go
// vm/vm.go
case code.OpJump:
    pos := int(code.ReadUint16(ins[ip+1:]))
    ip = pos - 1

case code.OpJumpNotTruthy:
    pos := int(code.ReadUint16(ins[ip+1:]))
    ip += 2
    condition := vm.pop()
    if !isTruthy(condition) {
        ip = pos - 1
    }
```

Set `ip = pos - 1` because the for-loop increments `ip` before the next fetch.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 4 / Jumps" & "Chapter 4 / Executing Jumps"*

---

### 23. Back-Patch Forward Jumps with a Placeholder Operand

**Principle:** When emitting a forward jump you don't yet know the target — emit a bogus operand (the book uses `9999`), remember the instruction's position, then `changeOperand` once the real target is known.

**Code:**
```go
// compiler/compiler.go
type EmittedInstruction struct {
    Opcode   code.Opcode
    Position int
}

type Compiler struct {
    // [...]
    lastInstruction    EmittedInstruction
    previousInstruction EmittedInstruction
}

func (c *Compiler) setLastInstruction(op code.Opcode, pos int) {
    previous := c.lastInstruction
    last := EmittedInstruction{Opcode: op, Position: pos}
    c.previousInstruction = previous
    c.lastInstruction = last
}

func (c *Compiler) lastInstructionIsPop() bool {
    return c.lastInstruction.Opcode == code.OpPop
}

func (c *Compiler) removeLastPop() {
    c.instructions = c.instructions[:c.lastInstruction.Position]
    c.lastInstruction = c.previousInstruction
}

func (c *Compiler) replaceInstruction(pos int, newInstruction []byte) {
    for i := 0; i < len(newInstruction); i++ {
        c.instructions[pos+i] = newInstruction[i]
    }
}

func (c *Compiler) changeOperand(opPos int, operand int) {
    op := code.Opcode(c.instructions[opPos])
    newInstruction := code.Make(op, operand)
    c.replaceInstruction(opPos, newInstruction)
}
```

Tracking both `lastInstruction` and `previousInstruction` is essential: after `removeLastPop`, the previous becomes the new last.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 4 / Compiling Conditionals"*

---

### 24. Compile `if`/`else` with a Single Unified Back-Patching Flow

**Code:**
```go
// compiler/compiler.go
case *ast.IfExpression:
    err := c.Compile(node.Condition)
    if err != nil {
        return err
    }
    // Emit an `OpJumpNotTruthy` with a bogus value
    jumpNotTruthyPos := c.emit(code.OpJumpNotTruthy, 9999)
    err = c.Compile(node.Consequence)
    if err != nil {
        return err
    }
    if c.lastInstructionIsPop() {
        c.removeLastPop()
    }
    // Emit an `OpJump` with a bogus value
    jumpPos := c.emit(code.OpJump, 9999)
    afterConsequencePos := len(c.instructions)
    c.changeOperand(jumpNotTruthyPos, afterConsequencePos)
    if node.Alternative == nil {
        c.emit(code.OpNull)
    } else {
        err := c.Compile(node.Alternative)
        if err != nil {
            return err
        }
        if c.lastInstructionIsPop() {
            c.removeLastPop()
        }
    }
    afterAlternativePos := len(c.instructions)
    c.changeOperand(jumpPos, afterAlternativePos)
```

The unconditional `OpJump` is *always* emitted (even when there's no alternative) so the conditional's value reaches the stack in both branches — the missing alternative just emits `OpNull`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 4 / Welcome Back, Null!"*

---

### 25. Build a Symbol Table — Names Become Numbers

**Principle:** Bytecode operands are integers, not identifiers; introduce a symbol table that maps identifiers to `{Scope, Index}` tuples so the compiler can emit numeric operands.

**Code:**
```go
// compiler/symbol_table.go
package compiler

type SymbolScope string

const (
    GlobalScope SymbolScope = "GLOBAL"
)

type Symbol struct {
    Name  string
    Scope SymbolScope
    Index int
}

type SymbolTable struct {
    store          map[string]Symbol
    numDefinitions int
}

func NewSymbolTable() *SymbolTable {
    s := make(map[string]Symbol)
    return &SymbolTable{store: s}
}

func (s *SymbolTable) Define(name string) Symbol {
    symbol := Symbol{Name: name, Index: s.numDefinitions, Scope: GlobalScope}
    s.store[name] = symbol
    s.numDefinitions++
    return symbol
}

func (s *SymbolTable) Resolve(name string) (Symbol, bool) {
    obj, ok := s.store[name]
    return obj, ok
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 5 / Introducing: the Symbol Table"*

---

### 26. Emit `OpSetGlobal`/`OpGetGlobal` from the Symbol Table

**Code:**
```go
// code/code.go
const (
    // [...]
    OpGetGlobal
    OpSetGlobal
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpGetGlobal: {"OpGetGlobal", []int{2}},
    OpSetGlobal: {"OpSetGlobal", []int{2}},
}
```

```go
// compiler/compiler.go
case *ast.LetStatement:
    err := c.Compile(node.Value)
    if err != nil {
        return err
    }
    symbol := c.symbolTable.Define(node.Name.Value)
    c.emit(code.OpSetGlobal, symbol.Index)

case *ast.Identifier:
    symbol, ok := c.symbolTable.Resolve(node.Value)
    if !ok {
        return fmt.Errorf("undefined variable %s", node.Value)
    }
    c.emit(code.OpGetGlobal, symbol.Index)
```

A pivotal side effect: undefined variables are now **compile-time errors**, not runtime errors. The compiler emits the message before the VM ever runs.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 5 / Using Symbols in the Compiler"*

---

### 27. Use a Preallocated Globals Store in the VM

**Code:**
```go
// vm/vm.go
const GlobalsSize = 65536

type VM struct {
    // [...]
    globals []object.Object
}

func New(bytecode *compiler.Bytecode) *VM {
    return &VM{
        // [...]
        globals: make([]object.Object, GlobalsSize),
    }
}

// In Run():
case code.OpSetGlobal:
    globalIndex := code.ReadUint16(ins[ip+1:])
    ip += 2
    vm.globals[globalIndex] = vm.pop()

case code.OpGetGlobal:
    globalIndex := code.ReadUint16(ins[ip+1:])
    ip += 2
    err := vm.push(vm.globals[globalIndex])
    if err != nil {
        return err
    }
```

The 2-byte operand caps globals at 65,536, which lets us preallocate the store up front.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 5 / Adding Globals to the VM"*

---

### 28. Preserve REPL State Across Lines with `NewWithState` Constructors

**Principle:** Each REPL iteration must reuse the symbol table, constants, and globals from prior iterations; expose constructors that accept external state instead of always allocating fresh.

**Code:**
```go
// compiler/compiler.go
func NewWithState(s *SymbolTable, constants []object.Object) *Compiler {
    compiler := New()
    compiler.symbolTable = s
    compiler.constants = constants
    return compiler
}
```

```go
// vm/vm.go
func NewWithGlobalsStore(bytecode *compiler.Bytecode, s []object.Object) *VM {
    vm := New(bytecode)
    vm.globals = s
    return vm
}
```

```go
// repl/repl.go
func Start(in io.Reader, out io.Writer) {
    scanner := bufio.NewScanner(in)
    constants := []object.Object{}
    globals := make([]object.Object, vm.GlobalsSize)
    symbolTable := compiler.NewSymbolTable()
    for {
        // [...]
        comp := compiler.NewWithState(symbolTable, constants)
        err := comp.Compile(program)
        if err != nil {
            fmt.Fprintf(out, "Woops! Compilation failed:\n %s\n", err)
            continue
        }
        code := comp.Bytecode()
        constants = code.Constants
        machine := vm.NewWithGlobalsStore(code, globals)
        // [...]
    }
}
```

Note that `constants = code.Constants` is required because the compiler uses `append` internally; the slice you passed in may be replaced.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 5 / REPL Persistence"*

---

### 29. Treat Strings as Constants; Reuse `OpAdd` for Concatenation

**Principle:** String literals are constant expressions — route them through the constant pool like integers. Concatenation reuses `OpAdd` because the operand-handling code is identical; only the VM's binary-op dispatch changes.

**Code:**
```go
// compiler/compiler.go
case *ast.StringLiteral:
    str := &object.String{Value: node.Value}
    c.emit(code.OpConstant, c.addConstant(str))
```

This is the same shape as `*ast.IntegerLiteral`. The compiler doesn't care that the VM will end up calling `executeBinaryStringOperation` for the `+`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 6 / String"*

---

### 30. Build Composite Values at Run Time — Teach the VM, Don't Inline

**Principle:** Arrays and hashes contain expressions whose values can't be known at compile time; emit instructions that push N elements, then a final opcode (`OpArray`/`OpHash`) whose operand is N and which constructs the composite on the stack.

**Code:**
```go
// code/code.go
const (
    // [...]
    OpArray
    OpHash
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpArray: {"OpArray", []int{2}},
    OpHash:  {"OpHash", []int{2}},
}
```

```go
// compiler/compiler.go
case *ast.ArrayLiteral:
    for _, el := range node.Elements {
        err := c.Compile(el)
        if err != nil {
            return err
        }
    }
    c.emit(code.OpArray, len(node.Elements))

case *ast.HashLiteral:
    keys := []ast.Expression{}
    for k := range node.Pairs {
        keys = append(keys, k)
    }
    sort.Slice(keys, func(i, j int) bool {
        return keys[i].String() < keys[j].String()
    })
    for _, k := range keys {
        err := c.Compile(k)
        if err != nil {
            return err
        }
        err = c.Compile(node.Pairs[k])
        if err != nil {
            return err
        }
    }
    c.emit(code.OpHash, len(node.Pairs)*2)
```

**Do:**
- Sort hash keys by their `String()` representation before compiling — Go map iteration is randomised and your tests will become flaky without deterministic output.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 6 / Array" & "Chapter 6 / Hash"*

---

### 31. Implement the Index Operator Generically Across Arrays and Hashes

**Principle:** Don't bake array-vs-hash distinctions into the compiler. Emit a single `OpIndex` and let the VM dispatch on the runtime type of the target.

**Code:**
```go
// vm/vm.go
case code.OpIndex:
    index := vm.pop()
    left := vm.pop()
    err := vm.executeIndexExpression(left, index)
    if err != nil {
        return err
    }

func (vm *VM) executeIndexExpression(left, index object.Object) error {
    switch {
    case left.Type() == object.ARRAY_OBJ && index.Type() == object.INTEGER_OBJ:
        return vm.executeArrayIndex(left, index)
    case left.Type() == object.HASH_OBJ:
        return vm.executeHashIndex(left, index)
    default:
        return fmt.Errorf("index operator not supported: %s", left.Type())
    }
}

func (vm *VM) executeArrayIndex(array, index object.Object) error {
    arrayObject := array.(*object.Array)
    i := index.(*object.Integer).Value
    max := int64(len(arrayObject.Elements) - 1)
    if i < 0 || i > max {
        return vm.push(Null)
    }
    return vm.push(arrayObject.Elements[i])
}

func (vm *VM) executeHashIndex(hash, index object.Object) error {
    hashObject := hash.(*object.Hash)
    key, ok := index.(object.Hashable)
    if !ok {
        return fmt.Errorf("unusable as hash key: %s", index.Type())
    }
    pair, ok := hashObject.Pairs[key.HashKey()]
    if !ok {
        return vm.push(Null)
    }
    return vm.push(pair.Value)
}
```

Out-of-bounds array index and missing hash key both push `Null` — predictable, null-safe behavior.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 6 / Adding the index operator"*

---

### 32. Represent Compiled Functions as Constants

**Principle:** A function literal's value (its compiled body) never changes — compile it to `code.Instructions`, wrap in `*object.CompiledFunction`, and store in the constant pool. Load it onto the stack with `OpConstant` (later `OpClosure`).

**Code:**
```go
// object/object.go
import (
    // [...]
    "monkey/code"
    // [...]
)

const (
    // [...]
    COMPILED_FUNCTION_OBJ = "COMPILED_FUNCTION_OBJ"
)

type CompiledFunction struct {
    Instructions  code.Instructions
    NumLocals     int
    NumParameters int
}

func (cf *CompiledFunction) Type() ObjectType { return COMPILED_FUNCTION_OBJ }
func (cf *CompiledFunction) Inspect() string {
    return fmt.Sprintf("CompiledFunction[%p]", cf)
}
```

`NumLocals` and `NumParameters` are added incrementally as the book adds locals and arguments; the initial version has only `Instructions`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Representing Functions"*

---

### 33. Define Function-Oriented Opcodes for Call and Return

**Code:**
```go
// code/code.go
const (
    // [...]
    OpCall
    OpReturnValue
    OpReturn
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpCall:       {"OpCall", []int{1}}, // later gains a 1-byte numArgs operand
    OpReturnValue: {"OpReturnValue", []int{}},
    OpReturn:      {"OpReturn", []int{}},
}
```

- `OpCall` — function sits on the stack (below any arguments); operand is argument count.
- `OpReturnValue` — return the value currently on top of the stack.
- `OpReturn` — return implicit `Null` (empty function body or body of only `let` statements).

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Opcodes to Execute Functions"*

---

### 34. Use a Compilation-Scope Stack to Isolate Function Bodies

**Principle:** Function body instructions must not mingle with the surrounding program; bundle `instructions` + `lastInstruction` + `previousInstruction` into a `CompilationScope` and push/pop a stack of scopes around function literals.

**Code:**
```go
// compiler/compiler.go
type CompilationScope struct {
    instructions        code.Instructions
    lastInstruction     EmittedInstruction
    previousInstruction EmittedInstruction
}

type Compiler struct {
    constants   []object.Object
    symbolTable *SymbolTable
    scopes      []CompilationScope
    scopeIndex  int
}

func New() *Compiler {
    mainScope := CompilationScope{
        instructions:        code.Instructions{},
        lastInstruction:     EmittedInstruction{},
        previousInstruction: EmittedInstruction{},
    }
    return &Compiler{
        constants:   []object.Object{},
        symbolTable: NewSymbolTable(),
        scopes:      []CompilationScope{mainScope},
        scopeIndex:  0,
    }
}

func (c *Compiler) currentInstructions() code.Instructions {
    return c.scopes[c.scopeIndex].instructions
}

func (c *Compiler) enterScope() {
    scope := CompilationScope{
        instructions:        code.Instructions{},
        lastInstruction:     EmittedInstruction{},
        previousInstruction: EmittedInstruction{},
    }
    c.scopes = append(c.scopes, scope)
    c.scopeIndex++
}

func (c *Compiler) leaveScope() code.Instructions {
    instructions := c.currentInstructions()
    c.scopes = c.scopes[:len(c.scopes)-1]
    c.scopeIndex--
    return instructions
}
```

Every helper that previously touched `c.instructions` now goes through `c.currentInstructions()` and writes back via `c.scopes[c.scopeIndex].instructions = ...`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Adding Scopes"*

---

### 35. Refactor `lastInstructionIsPop` to a Generic `lastInstructionIs`

**Code:**
```go
// compiler/compiler.go
func (c *Compiler) lastInstructionIs(op code.Opcode) bool {
    if len(c.currentInstructions()) == 0 {
        return false
    }
    return c.scopes[c.scopeIndex].lastInstruction.Opcode == op
}
```

The defensive `len(...) == 0` check matters once you start calling this for empty function bodies.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Compiling With Scopes"*

---

### 36. Compile Function Literals by Entering a Scope, Compiling the Body, Leaving

**Code:**
```go
// compiler/compiler.go
case *ast.FunctionLiteral:
    c.enterScope()
    for _, p := range node.Parameters {
        c.symbolTable.Define(p.Value)
    }
    err := c.Compile(node.Body)
    if err != nil {
        return err
    }
    if c.lastInstructionIs(code.OpPop) {
        c.replaceLastPopWithReturn()
    }
    if !c.lastInstructionIs(code.OpReturnValue) {
        c.emit(code.OpReturn)
    }
    freeSymbols := c.symbolTable.FreeSymbols
    numLocals := c.symbolTable.numDefinitions
    instructions := c.leaveScope()
    for _, s := range freeSymbols {
        c.loadSymbol(s)
    }
    compiledFn := &object.CompiledFunction{
        Instructions:  instructions,
        NumLocals:     numLocals,
        NumParameters: len(node.Parameters),
    }
    fnIndex := c.addConstant(compiledFn)
    c.emit(code.OpClosure, fnIndex, len(freeSymbols))

func (c *Compiler) replaceLastPopWithReturn() {
    lastPos := c.scopes[c.scopeIndex].lastInstruction.Position
    c.replaceInstruction(lastPos, code.Make(code.OpReturnValue))
    c.scopes[c.scopeIndex].lastInstruction.Opcode = code.OpReturnValue
}
```

The three-tier end-of-body handling is key:
1. If the last statement was an expression, turn its `OpPop` into `OpReturnValue` (implicit return).
2. If there's still no `OpReturnValue`, append `OpReturn` (empty body or only lets).
3. Capture `FreeSymbols` and `numLocals` *before* `leaveScope` resets the symbol table.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Compiling With Scopes" & "Chapter 9 / Compiling and resolving free variables"*

---

### 37. Compile Call Expressions by Pushing the Function, Then Args, Then `OpCall`

**Code:**
```go
// compiler/compiler.go
case *ast.CallExpression:
    err := c.Compile(node.Function)
    if err != nil {
        return err
    }
    for _, a := range node.Arguments {
        err := c.Compile(a)
        if err != nil {
            return err
        }
    }
    c.emit(code.OpCall, len(node.Arguments))
```

The compiler doesn't care whether the callee is a closure, a global binding, or a built-in — `node.Function` is an expression like any other.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Compiling Calls With Arguments"*

---

### 38. Introduce `Frame` to Bundle a Function + Instruction Pointer

**Principle:** Each call needs its own instruction pointer and (later) a base pointer; tie them together in a `Frame` and keep a stack of frames.

**Code:**
```go
// vm/frame.go
package vm

import (
    "monkey/code"
    "monkey/object"
)

type Frame struct {
    cl         *object.Closure
    ip         int
    basePointer int
}

func NewFrame(cl *object.Closure, basePointer int) *Frame {
    f := &Frame{
        cl:          cl,
        ip:          -1,
        basePointer: basePointer,
    }
    return f
}

func (f *Frame) Instructions() code.Instructions {
    return f.cl.Fn.Instructions
}
```

`ip` starts at -1 because the run loop increments before fetching.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Adding Frames"*

---

### 39. Treat the Main Program as the Outermost Frame

**Principle:** Don't special-case the top-level program — wrap its instructions in a fake `CompiledFunction`/`Closure` and make it the first frame; this lets the run loop be uniform.

**Code:**
```go
// vm/vm.go
const MaxFrames = 1024

type VM struct {
    constants   []object.Object
    stack       []object.Object
    sp          int
    globals     []object.Object
    frames      []*Frame
    framesIndex int
}

func New(bytecode *compiler.Bytecode) *VM {
    mainFn := &object.CompiledFunction{Instructions: bytecode.Instructions}
    mainClosure := &object.Closure{Fn: mainFn}
    mainFrame := NewFrame(mainClosure, 0)
    frames := make([]*Frame, MaxFrames)
    frames[0] = mainFrame
    return &VM{
        constants:   bytecode.Constants,
        stack:       make([]object.Object, StackSize),
        sp:          0,
        globals:     make([]object.Object, GlobalsSize),
        frames:      frames,
        framesIndex: 1,
    }
}

func (vm *VM) currentFrame() *Frame {
    return vm.frames[vm.framesIndex-1]
}

func (vm *VM) pushFrame(f *Frame) {
    vm.frames[vm.framesIndex] = f
    vm.framesIndex++
}

func (vm *VM) popFrame() *Frame {
    vm.framesIndex--
    return vm.frames[vm.framesIndex]
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Adding Frames"*

---

### 40. Run Loop Fetches from `currentFrame()` — Not `vm.instructions`

**Code:**
```go
// vm/vm.go
func (vm *VM) Run() error {
    var ip int
    var ins code.Instructions
    var op code.Opcode
    for vm.currentFrame().ip < len(vm.currentFrame().Instructions())-1 {
        vm.currentFrame().ip++
        ip = vm.currentFrame().ip
        ins = vm.currentFrame().Instructions()
        op = code.Opcode(ins[ip])
        switch op {
        case code.OpConstant:
            constIndex := code.ReadUint16(ins[ip+1:])
            vm.currentFrame().ip += 2
            // ...
        case code.OpJump:
            pos := int(code.ReadUint16(ins[ip+1:]))
            vm.currentFrame().ip = pos - 1
        // ...
        }
    }
    return nil
}
```

The three local helpers (`ip`, `ins`, `op`) keep the loop body readable; every operand skip now mutates `vm.currentFrame().ip` instead of a loop-local `ip`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Adding Frames"*

---

### 41. Implement `OpCall`/`OpReturnValue`/`OpReturn` via Frames

**Code:**
```go
// vm/vm.go
case code.OpCall:
    numArgs := code.ReadUint8(ins[ip+1:])
    vm.currentFrame().ip += 1
    err := vm.executeCall(int(numArgs))
    if err != nil {
        return err
    }

case code.OpReturnValue:
    returnValue := vm.pop()
    frame := vm.popFrame()
    vm.sp = frame.basePointer - 1
    err := vm.push(returnValue)
    if err != nil {
        return err
    }

case code.OpReturn:
    frame := vm.popFrame()
    vm.sp = frame.basePointer - 1
    err := vm.push(Null)
    if err != nil {
        return err
    }
```

`vm.sp = frame.basePointer - 1` does double duty: it clears locals *and* removes the now-executed function from the stack — the `-1` avoids needing an extra `vm.pop()` call.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Executing Function Calls"*

---

### 42. Locals Live in a "Hole" Above `basePointer` on the Stack

**Principle:** Don't allocate a separate data structure for locals — reserve `NumLocals` stack slots above `basePointer` so the same stack serves both locals and temporary values.

**Code:**
```go
// code/code.go
const (
    // [...]
    OpGetLocal
    OpSetLocal
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpGetLocal: {"OpGetLocal", []int{1}},
    OpSetLocal: {"OpSetLocal", []int{1}},
}
```

```go
// vm/vm.go
case code.OpSetLocal:
    localIndex := code.ReadUint8(ins[ip+1:])
    vm.currentFrame().ip += 1
    frame := vm.currentFrame()
    vm.stack[frame.basePointer+int(localIndex)] = vm.pop()

case code.OpGetLocal:
    localIndex := code.ReadUint8(ins[ip+1:])
    vm.currentFrame().ip += 1
    frame := vm.currentFrame()
    err := vm.push(vm.stack[frame.basePointer+int(localIndex)])
    if err != nil {
        return err
    }
```

Use 1-byte operands for locals (256 max per function) — they're more numerous than globals but smaller per-function.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Opcodes for Local Bindings" & "Chapter 7 / Implementing Local Bindings in the VM"*

---

### 43. Make the Symbol Table Recursive via an `Outer` Pointer

**Principle:** To handle nested scopes, give each `SymbolTable` an `Outer *SymbolTable`; `Resolve` walks the chain recursively.

**Code:**
```go
// compiler/symbol_table.go
const (
    LocalScope  SymbolScope = "LOCAL"
    GlobalScope SymbolScope = "GLOBAL"
)

type SymbolTable struct {
    Outer          *SymbolTable
    store          map[string]Symbol
    numDefinitions int
    FreeSymbols    []Symbol
}

func NewSymbolTable() *SymbolTable {
    s := make(map[string]Symbol)
    free := []Symbol{}
    return &SymbolTable{store: s, FreeSymbols: free}
}

func NewEnclosedSymbolTable(outer *SymbolTable) *SymbolTable {
    s := NewSymbolTable()
    s.Outer = outer
    return s
}

func (s *SymbolTable) Define(name string) Symbol {
    symbol := Symbol{Name: name, Index: s.numDefinitions}
    if s.Outer == nil {
        symbol.Scope = GlobalScope
    } else {
        symbol.Scope = LocalScope
    }
    s.store[name] = symbol
    s.numDefinitions++
    return symbol
}

func (s *SymbolTable) Resolve(name string) (Symbol, bool) {
    obj, ok := s.store[name]
    if !ok && s.Outer != nil {
        obj, ok = s.Outer.Resolve(name)
        if !ok {
            return obj, ok
        }
        if obj.Scope == GlobalScope || obj.Scope == BuiltinScope {
            return obj, ok
        }
        free := s.defineFree(obj)
        return free, true
    }
    return obj, ok
}

func (s *SymbolTable) defineFree(original Symbol) Symbol {
    s.FreeSymbols = append(s.FreeSymbols, original)
    symbol := Symbol{Name: original.Name, Index: len(s.FreeSymbols) - 1}
    symbol.Scope = FreeScope
    s.store[original.Name] = symbol
    return symbol
}
```

`Define` picks the scope based on whether `Outer` is set; `Resolve` recurses and (when not at the global/builtin level) marks resolved symbols as free via `defineFree`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Extending the Symbol Table" & "Chapter 9 / Compiling and resolving free variables"*

---

### 44. The Compiler Encloses/Restores the Symbol Table with Scope Entry/Exit

**Code:**
```go
// compiler/compiler.go
func (c *Compiler) enterScope() {
    scope := CompilationScope{
        instructions:        code.Instructions{},
        lastInstruction:     EmittedInstruction{},
        previousInstruction: EmittedInstruction{},
    }
    c.scopes = append(c.scopes, scope)
    c.scopeIndex++
    c.symbolTable = NewEnclosedSymbolTable(c.symbolTable)
}

func (c *Compiler) leaveScope() code.Instructions {
    instructions := c.currentInstructions()
    c.scopes = c.scopes[:len(c.scopes)-1]
    c.scopeIndex--
    c.symbolTable = c.symbolTable.Outer
    return instructions
}
```

Every `enterScope` (function body) gets a fresh enclosed symbol table; every `leaveScope` restores the outer one — symmetric with the compilation-scope stack.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Compiling With Scopes"*

---

### 45. Emit `OpSetLocal`/`OpGetLocal` Based on the Resolved Symbol's Scope

**Code:**
```go
// compiler/compiler.go
case *ast.LetStatement:
    symbol := c.symbolTable.Define(node.Name.Value)
    err := c.Compile(node.Value)
    if err != nil {
        return err
    }
    if symbol.Scope == GlobalScope {
        c.emit(code.OpSetGlobal, symbol.Index)
    } else {
        c.emit(code.OpSetLocal, symbol.Index)
    }

case *ast.Identifier:
    symbol, ok := c.symbolTable.Resolve(node.Value)
    if !ok {
        return fmt.Errorf("undefined variable %s", node.Value)
    }
    c.loadSymbol(symbol)
```

The `Define` call was deliberately hoisted above the `Compile(node.Value)` so that recursive functions can resolve their own name — see Recursive Closures below.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Compiling With Scopes" & "Chapter 9 / Recursive Closures"*

---

### 46. Treat Function Arguments as Local Bindings

**Principle:** Arguments already sit on the stack where locals live — define each parameter via `symbolTable.Define` so references compile to `OpGetLocal`. This avoids a separate argument scope and opcode.

**Code:**
```go
// compiler/compiler.go
case *ast.FunctionLiteral:
    c.enterScope()
    if node.Name != "" {
        c.symbolTable.DefineFunctionName(node.Name)
    }
    for _, p := range node.Parameters {
        c.symbolTable.Define(p.Value)
    }
    // compile body...
```

In the VM, `basePointer = vm.sp - numArgs` (not `vm.sp`) so argument slots align with `OpGetLocal index`:

```go
// vm/vm.go
func (vm *VM) callClosure(cl *object.Closure, numArgs int) error {
    if numArgs != cl.Fn.NumParameters {
        return fmt.Errorf("wrong number of arguments: want=%d, got=%d",
            cl.Fn.NumParameters, numArgs)
    }
    frame := NewFrame(cl, vm.sp-numArgs)
    vm.pushFrame(frame)
    vm.sp = frame.basePointer + cl.Fn.NumLocals
    return nil
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Arguments in the VM"*

---

### 47. Validate Argument Counts in the VM

**Code:**
```go
// vm/vm.go
func TestCallingFunctionsWithWrongArguments(t *testing.T) {
    tests := []vmTestCase{
        {input: `fn() { 1; }(1);`,
         expected: `wrong number of arguments: want=0, got=1`},
        {input: `fn(a) { a; }();`,
         expected: `wrong number of arguments: want=1, got=0`},
        {input: `fn(a, b) { a + b; }(1);`,
         expected: `wrong number of arguments: want=2, got=1`},
    }
    for _, tt := range tests {
        program := parse(tt.input)
        comp := compiler.New()
        err := comp.Compile(program)
        if err != nil {
            t.Fatalf("compiler error: %s", err)
        }
        vm := New(comp.Bytecode())
        err = vm.Run()
        if err == nil {
            t.Fatalf("expected VM error but resulted in none.")
        }
        if err.Error() != tt.expected {
            t.Fatalf("wrong VM error: want=%q, got=%q", tt.expected, err)
        }
    }
}
```

Storing `NumParameters` on `CompiledFunction` lets the VM catch mismatched arity before stack layout is corrupted.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Arguments in the VM"*

---

### 48. Move Built-ins to the `object` Package — Bring Your Own Null

**Principle:** Don't let compiler/VM depend on evaluator — move built-in function definitions to `object/builtins.go`, store them in a slice of `{Name, *Builtin}` structs for stable iteration, and have them return `nil` (rather than `evaluator.NULL`) so callers translate to their preferred null.

**Code:**
```go
// object/builtins.go
package object

import "fmt"

var Builtins = []struct {
    Name    string
    Builtin *Builtin
}{
    {
        "len",
        &Builtin{Fn: func(args ...Object) Object {
            if len(args) != 1 {
                return newError("wrong number of arguments. got=%d, want=1",
                    len(args))
            }
            switch arg := args[0].(type) {
            case *Array:
                return &Integer{Value: int64(len(arg.Elements))}
            case *String:
                return &Integer{Value: int64(len(arg.Value))}
            default:
                return newError("argument to `len` not supported, got %s",
                    args[0].Type())
            }
        }},
    },
    {
        "puts",
        &Builtin{Fn: func(args ...Object) Object {
            for _, arg := range args {
                fmt.Println(arg.Inspect())
            }
            return nil
        }},
    },
    {
        "first",
        &Builtin{Fn: func(args ...Object) Object {
            if len(args) != 1 {
                return newError("wrong number of arguments. got=%d, want=1",
                    len(args))
            }
            if args[0].Type() != ARRAY_OBJ {
                return newError("argument to `first` must be ARRAY, got %s",
                    args[0].Type())
            }
            arr := args[0].(*Array)
            if len(arr.Elements) > 0 {
                return arr.Elements[0]
            }
            return nil
        }},
    },
    {
        "last",
        &Builtin{Fn: func(args ...Object) Object {
            if len(args) != 1 {
                return newError("wrong number of arguments. got=%d, want=1",
                    len(args))
            }
            if args[0].Type() != ARRAY_OBJ {
                return newError("argument to `last` must be ARRAY, got %s",
                    args[0].Type())
            }
            arr := args[0].(*Array)
            length := len(arr.Elements)
            if length > 0 {
                return arr.Elements[length-1]
            }
            return nil
        }},
    },
    {
        "rest",
        &Builtin{Fn: func(args ...Object) Object {
            if len(args) != 1 {
                return newError("wrong number of arguments. got=%d, want=1",
                    len(args))
            }
            if args[0].Type() != ARRAY_OBJ {
                return newError("argument to `rest` must be ARRAY, got %s",
                    args[0].Type())
            }
            arr := args[0].(*Array)
            length := len(arr.Elements)
            if length > 0 {
                newElements := make([]Object, length-1, length-1)
                copy(newElements, arr.Elements[1:length])
                return &Array{Elements: newElements}
            }
            return nil
        }},
    },
    {
        "push",
        &Builtin{Fn: func(args ...Object) Object {
            if len(args) != 2 {
                return newError("wrong number of arguments. got=%d, want=2",
                    len(args))
            }
            if args[0].Type() != ARRAY_OBJ {
                return newError("argument to `push` must be ARRAY, got %s",
                    args[0].Type())
            }
            arr := args[0].(*Array)
            length := len(arr.Elements)
            newElements := make([]Object, length+1, length+1)
            copy(newElements, arr.Elements)
            newElements[length] = args[1]
            return &Array{Elements: newElements}
        }},
    },
}

func GetBuiltinByName(name string) *Builtin {
    for _, def := range Builtins {
        if def.Name == name {
            return def.Builtin
        }
    }
    return nil
}

func newError(format string, a ...interface{}) *Error {
    return &Error{Message: fmt.Sprintf(format, a...)}
}
```

The evaluator now becomes a thin shim:

```go
// evaluator/builtins.go
var builtins = map[string]*object.Builtin{
    "len":   object.GetBuiltinByName("len"),
    "puts":  object.GetBuiltinByName("puts"),
    "first": object.GetBuiltinByName("first"),
    "last":  object.GetBuiltinByName("last"),
    "rest":  object.GetBuiltinByName("rest"),
    "push":  object.GetBuiltinByName("push"),
}
```

```go
// evaluator/evaluator.go
case *object.Builtin:
    if result := fn.Fn(args...); result != nil {
        return result
    }
    return NULL
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 8 / Making the Change Easy"*

---

### 49. Add a `BuiltinScope` and Define Built-ins at Compiler Construction

**Code:**
```go
// compiler/symbol_table.go
const (
    BuiltinScope SymbolScope = "BUILTIN"
    // [...]
)

func (s *SymbolTable) DefineBuiltin(index int, name string) Symbol {
    symbol := Symbol{Name: name, Index: index, Scope: BuiltinScope}
    s.store[name] = symbol
    return symbol
}
```

```go
// compiler/compiler.go
func New() *Compiler {
    symbolTable := NewSymbolTable()
    for i, v := range object.Builtins {
        symbolTable.DefineBuiltin(i, v.Name)
    }
    return &Compiler{
        constants:   []object.Object{},
        symbolTable: symbolTable,
        scopes:      []CompilationScope{mainScope},
        scopeIndex:  0,
    }
}
```

```go
// code/code.go
const (
    // [...]
    OpGetBuiltin
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpGetBuiltin: {"OpGetBuiltin", []int{1}},
}
```

The 1-byte operand is the index into `object.Builtins`; the VM uses the same slice to look up the function.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 8 / A New Scope for Built-in Functions"*

---

### 50. Dispatch Calls by Type: Closures vs. Built-ins

**Principle:** Keep the calling convention uniform (function on stack, args on top, `OpCall`); the VM sniffs the callee's type and dispatches.

**Code:**
```go
// vm/vm.go
func (vm *VM) executeCall(numArgs int) error {
    callee := vm.stack[vm.sp-1-numArgs]
    switch callee := callee.(type) {
    case *object.Closure:
        return vm.callClosure(callee, numArgs)
    case *object.Builtin:
        return vm.callBuiltin(callee, numArgs)
    default:
        return fmt.Errorf("calling non-closure and non-builtin")
    }
}

func (vm *VM) callClosure(cl *object.Closure, numArgs int) error {
    if numArgs != cl.Fn.NumParameters {
        return fmt.Errorf("wrong number of arguments: want=%d, got=%d",
            cl.Fn.NumParameters, numArgs)
    }
    frame := NewFrame(cl, vm.sp-numArgs)
    vm.pushFrame(frame)
    vm.sp = frame.basePointer + cl.Fn.NumLocals
    return nil
}

func (vm *VM) callBuiltin(builtin *object.Builtin, numArgs int) error {
    args := vm.stack[vm.sp-numArgs : vm.sp]
    result := builtin.Fn(args...)
    vm.sp = vm.sp - numArgs - 1
    if result != nil {
        vm.push(result)
    } else {
        vm.push(Null)
    }
    return nil
}

case code.OpGetBuiltin:
    builtinIndex := code.ReadUint8(ins[ip+1:])
    vm.currentFrame().ip += 1
    definition := object.Builtins[builtinIndex]
    err := vm.push(definition.Builtin)
    if err != nil {
        return err
    }
```

`callBuiltin` slices the args directly off the stack (no copying), calls the Go function, then collapses the stack (`vm.sp - numArgs - 1` removes args *and* the function). `nil` return → push `Null` — that's the bring-your-own-null strategy.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 8 / Executing built-in functions"*

---

### 51. Centralize Symbol → Opcode Mapping in `loadSymbol`

**Principle:** As scopes multiply (Global, Local, Builtin, Free, Function), resist scattering `if scope == ...` checks; funnel everything through a single dispatcher.

**Code:**
```go
// compiler/compiler.go
func (c *Compiler) loadSymbol(s Symbol) {
    switch s.Scope {
    case GlobalScope:
        c.emit(code.OpGetGlobal, s.Index)
    case LocalScope:
        c.emit(code.OpGetLocal, s.Index)
    case BuiltinScope:
        c.emit(code.OpGetBuiltin, s.Index)
    case FreeScope:
        c.emit(code.OpGetFree, s.Index)
    case FunctionScope:
        c.emit(code.OpCurrentClosure)
    }
}
```

Every new scope is one `case` here; the rest of the compiler stays agnostic.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 8 / A New Scope for Built-in Functions" & "Chapter 9 / Recursive Closures"*

---

### 52. Define `object.Closure` — Function + Free Variables

**Principle:** Close over free variables by wrapping each `*CompiledFunction` in a `*Closure` that carries a `Free []Object` slice. Treat every function as a closure (zero or more free vars) to keep the architecture uniform.

**Code:**
```go
// object/object.go
const (
    // [...]
    CLOSURE_OBJ = "CLOSURE"
)

type Closure struct {
    Fn   *CompiledFunction
    Free []Object
}

func (c *Closure) Type() ObjectType { return CLOSURE_OBJ }
func (c *Closure) Inspect() string {
    return fmt.Sprintf("Closure[%p]", c)
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Everything's a closure"*

---

### 53. `OpClosure` Has Two Operands — Constant Index + Free-Variable Count

**Code:**
```go
// code/code.go
const (
    // [...]
    OpClosure
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpClosure: {"OpClosure", []int{2, 1}},
}
```

The first operand matches `OpConstant`'s width (2 bytes) so any function indexable by `OpConstant` is also reachable by `OpClosure`. The second operand (1 byte, max 256 free vars) tells the VM how many stack values to roll into the closure's `Free` slice.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Everything's a closure"*

---

### 54. Support Multi-Operand Opcodes in `Make`, `ReadOperands`, and `fmtInstruction`

**Code:**
```go
// code/code.go
func Make(op Opcode, operands ...int) []byte {
    // ...
    switch width {
    case 2:
        binary.BigEndian.PutUint16(instruction[offset:], uint16(o))
    case 1:
        instruction[offset] = byte(o)
    }
    // ...
}

func (ins Instructions) fmtInstruction(def *Definition, operands []int) string {
    // ...
    switch operandCount {
    case 0:
        return def.Name
    case 1:
        return fmt.Sprintf("%s %d", def.Name, operands[0])
    case 2:
        return fmt.Sprintf("%s %d %d", def.Name, operands[0], operands[1])
    }
    // ...
}
```

Test the encoding exhaustively:

```go
// code/code_test.go
func TestMake(t *testing.T) {
    tests := []struct {
        op       Opcode
        operands []int
        expected []byte
    }{
        {OpConstant, []int{65534}, []byte{byte(OpConstant), 255, 254}},
        {OpAdd, []int{}, []byte{byte(OpAdd)}},
        {OpGetLocal, []int{255}, []byte{byte(OpGetLocal), 255}},
        {OpClosure, []int{65534, 255}, []byte{byte(OpClosure), 255, 254, 255}},
    }
    // ...
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Opcodes for Local Bindings" & "Chapter 9 / Everything's a closure"*

---

### 55. Emit `OpClosure` Instead of `OpConstant` for Function Literals

**Code:**
```go
// compiler/compiler.go
case *ast.FunctionLiteral:
    c.enterScope()
    if node.Name != "" {
        c.symbolTable.DefineFunctionName(node.Name)
    }
    for _, p := range node.Parameters {
        c.symbolTable.Define(p.Value)
    }
    err := c.Compile(node.Body)
    if err != nil {
        return err
    }
    if c.lastInstructionIs(code.OpPop) {
        c.replaceLastPopWithReturn()
    }
    if !c.lastInstructionIs(code.OpReturnValue) {
        c.emit(code.OpReturn)
    }
    freeSymbols := c.symbolTable.FreeSymbols
    numLocals := c.symbolTable.numDefinitions
    instructions := c.leaveScope()
    for _, s := range freeSymbols {
        c.loadSymbol(s)
    }
    compiledFn := &object.CompiledFunction{
        Instructions:  instructions,
        NumLocals:     numLocals,
        NumParameters: len(node.Parameters),
    }
    fnIndex := c.addConstant(compiledFn)
    c.emit(code.OpClosure, fnIndex, len(freeSymbols))
```

The loop `for _, s := range freeSymbols { c.loadSymbol(s) }` runs *after* `leaveScope`, so the load instructions live in the enclosing scope and push values onto the enclosing stack — exactly where `OpClosure` will pop them.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Compiling and resolving free variables"*

---

### 56. Implement `OpGetFree` to Load from the Current Closure's `Free` Slice

**Code:**
```go
// code/code.go
const (
    // [...]
    OpGetFree
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpGetFree: {"OpGetFree", []int{1}},
}
```

```go
// vm/vm.go
case code.OpGetFree:
    freeIndex := code.ReadUint8(ins[ip+1:])
    vm.currentFrame().ip += 1
    currentClosure := vm.currentFrame().cl
    err := vm.push(currentClosure.Free[freeIndex])
    if err != nil {
        return err
    }
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Compiling and resolving free variables" & "Chapter 9 / Creating real closures at run time"*

---

### 57. `pushClosure` Pops Free Vars from the Stack in Order

**Code:**
```go
// vm/vm.go
case code.OpClosure:
    constIndex := code.ReadUint16(ins[ip+1:])
    numFree := code.ReadUint8(ins[ip+3:])
    vm.currentFrame().ip += 3
    err := vm.pushClosure(int(constIndex), int(numFree))
    if err != nil {
        return err
    }

func (vm *VM) pushClosure(constIndex, numFree int) error {
    constant := vm.constants[constIndex]
    function, ok := constant.(*object.CompiledFunction)
    if !ok {
        return fmt.Errorf("not a function: %+v", constant)
    }
    free := make([]object.Object, numFree)
    for i := 0; i < numFree; i++ {
        free[i] = vm.stack[vm.sp-numFree+i]
    }
    vm.sp = vm.sp - numFree
    closure := &object.Closure{Fn: function, Free: free}
    return vm.push(closure)
}
```

Copy from the *lowest* free var first (`vm.sp-numFree+i`) so `free[i]` matches the order in which the compiler emitted `loadSymbol` calls.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Creating real closures at run time"*

---

### 58. Detect Recursive Self-Reference via `FunctionScope` and `OpCurrentClosure`

**Principle:** A closure that references itself can't be loaded via `OpGetLocal` (its slot isn't populated yet) or `OpGetFree` (its free var points to nothing). Solution: mark the function's own name with `FunctionScope`, and have `loadSymbol` emit `OpCurrentClosure` for that scope — the VM pushes the closure currently executing.

**Code:**
```go
// compiler/symbol_table.go
const (
    FreeScope     SymbolScope = "FREE"
    FunctionScope SymbolScope = "FUNCTION"
)

func (s *SymbolTable) DefineFunctionName(name string) Symbol {
    symbol := Symbol{Name: name, Index: 0, Scope: FunctionScope}
    s.store[name] = symbol
    return symbol
}
```

```go
// ast/ast.go
type FunctionLiteral struct {
    Token      token.Token
    Parameters []*Identifier
    Body       *BlockStatement
    Name       string
}
```

```go
// parser/parser.go
func (p *Parser) parseLetStatement() *ast.LetStatement {
    // ...
    stmt.Value = p.parseExpression(LOWEST)
    if fl, ok := stmt.Value.(*ast.FunctionLiteral); ok {
        fl.Name = stmt.Name.Value
    }
    // ...
}
```

```go
// code/code.go
const (
    // [...]
    OpCurrentClosure
)

var definitions = map[Opcode]*Definition{
    // [...]
    OpCurrentClosure: {"OpCurrentClosure", []int{}},
}
```

```go
// vm/vm.go
case code.OpCurrentClosure:
    currentClosure := vm.currentFrame().cl
    err := vm.push(currentClosure)
    if err != nil {
        return err
    }
```

The parser stamps the let-bound name onto the `FunctionLiteral` so the compiler knows what name to define in `FunctionScope`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Recursive Closures"*

---

### 59. Promote Local-Binding `Define` Before Compiling the Value

**Principle:** For `let name = fn(...){...}` to allow self-reference, `Define(name)` must happen *before* `Compile(value)`.

**Code:**
```go
// compiler/compiler.go
case *ast.LetStatement:
    symbol := c.symbolTable.Define(node.Name.Value)
    err := c.Compile(node.Value)
    if err != nil {
        return err
    }
    if symbol.Scope == GlobalScope {
        c.emit(code.OpSetGlobal, symbol.Index)
    } else {
        c.emit(code.OpSetLocal, symbol.Index)
    }
```

Note that this intentionally allows the binding to be referenced inside its own initializer — a deliberate, scoped exception to the usual "define after evaluation" rule.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Recursive Closures"*

---

### 60. VM Tests Should Be Table-Driven Like Compiler Tests

**Principle:** Mirror the compiler's test ergonomics in the VM: `vmTestCase{input, expected}`, parse, compile, run, then assert against `LastPoppedStackElem()`.

**Code:**
```go
// vm/vm_test.go
type vmTestCase struct {
    input    string
    expected interface{}
}

func runVmTests(t *testing.T, tests []vmTestCase) {
    t.Helper()
    for _, tt := range tests {
        program := parse(tt.input)
        comp := compiler.New()
        err := comp.Compile(program)
        if err != nil {
            t.Fatalf("compiler error: %s", err)
        }
        vm := New(comp.Bytecode())
        err = vm.Run()
        if err != nil {
            t.Fatalf("vm error: %s", err)
        }
        stackElem := vm.LastPoppedStackElem()
        testExpectedObject(t, tt.expected, stackElem)
    }
}

func testExpectedObject(
    t *testing.T,
    expected interface{},
    actual object.Object,
) {
    t.Helper()
    switch expected := expected.(type) {
    case int:
        err := testIntegerObject(int64(expected), actual)
        if err != nil {
            t.Errorf("testIntegerObject failed: %s", err)
        }
    case bool:
        err := testBooleanObject(bool(expected), actual)
        if err != nil {
            t.Errorf("testBooleanObject failed: %s", err)
        }
    case string:
        err := testStringObject(expected, actual)
        if err != nil {
            t.Errorf("testStringObject failed: %s", err)
        }
    case *object.Null:
        if actual != Null {
            t.Errorf("object is not Null: %T (%+v)", actual, actual)
        }
    case []int:
        array, ok := actual.(*object.Array)
        if !ok {
            t.Errorf("object not Array: %T (%+v)", actual, actual)
            return
        }
        if len(array.Elements) != len(expected) {
            t.Errorf("wrong num of elements. want=%d, got=%d",
                len(expected), len(array.Elements))
            return
        }
        for i, expectedElem := range expected {
            err := testIntegerObject(int64(expectedElem), array.Elements[i])
            if err != nil {
                t.Errorf("testIntegerObject failed: %s", err)
            }
        }
    case map[object.HashKey]int64:
        hash, ok := actual.(*object.Hash)
        if !ok {
            t.Errorf("object is not Hash. got=%T (%+v)", actual, actual)
            return
        }
        if len(hash.Pairs) != len(expected) {
            t.Errorf("hash has wrong number of Pairs. want=%d, got=%d",
                len(expected), len(hash.Pairs))
            return
        }
        for expectedKey, expectedValue := range expected {
            pair, ok := hash.Pairs[expectedKey]
            if !ok {
                t.Errorf("no pair for given key in Pairs")
            }
            err := testIntegerObject(expectedValue, pair.Value)
            if err != nil {
                t.Errorf("testIntegerObject failed: %s", err)
            }
        }
    case *object.Error:
        errObj, ok := actual.(*object.Error)
        if !ok {
            t.Errorf("object is not Error: %T (%+v)", actual, actual)
            return
        }
        if errObj.Message != expected.Message {
            t.Errorf("wrong error message. expected=%q, got=%q",
                expected.Message, errObj.Message)
        }
    }
}
```

The type switch makes adding new test kinds a one-case change — the same flexibility principle as `testConstants`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Powering On the Machine" & throughout*

---

### 61. Benchmark with a Real Workload — Fibonacci(35)

**Principle:** The cheapest credible performance signal for a recursive interpreter is a deep Fibonacci computation; it stresses function calls, arithmetic, and conditionals uniformly.

**Code:**
```go
// benchmark/main.go
package main

import (
    "flag"
    "fmt"
    "time"

    "monkey/compiler"
    "monkey/evaluator"
    "monkey/lexer"
    "monkey/object"
    "monkey/parser"
    "monkey/vm"
)

var engine = flag.String("engine", "vm", "use 'vm' or 'eval'")

var input = `
let fibonacci = fn(x) {
  if (x == 0) {
    0
  } else {
    if (x == 1) {
      return 1;
    } else {
      fibonacci(x - 1) + fibonacci(x - 2);
    }
  }
};
fibonacci(35);
`

func main() {
    flag.Parse()
    var duration time.Duration
    var result object.Object
    l := lexer.New(input)
    p := parser.New(l)
    program := p.ParseProgram()
    if *engine == "vm" {
        comp := compiler.New()
        err := comp.Compile(program)
        if err != nil {
            fmt.Printf("compiler error: %s", err)
            return
        }
        machine := vm.New(comp.Bytecode())
        start := time.Now()
        err = machine.Run()
        if err != nil {
            fmt.Printf("vm error: %s", err)
            return
        }
        duration = time.Since(start)
        result = machine.LastPoppedStackElem()
    } else {
        env := object.NewEnvironment()
        start := time.Now()
        result = evaluator.Eval(program, env)
        duration = time.Since(start)
    }
    fmt.Printf(
        "engine=%s, result=%s, duration=%s\n",
        *engine,
        result.Inspect(),
        duration)
}
```

The book's results: `engine=eval, result=9227465, duration=27.204277379s` vs `engine=vm, result=9227465, duration=8.876222455s` — a 3.3x speedup with zero low-level tuning.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 10 / Taking Time"*

---

### 62. Hook the REPL to Compiler + VM

**Code:**
```go
// repl/repl.go
import (
    "bufio"
    "fmt"
    "io"

    "monkey/compiler"
    "monkey/lexer"
    "monkey/object"
    "monkey/parser"
    "monkey/vm"
)

func Start(in io.Reader, out io.Writer) {
    scanner := bufio.NewScanner(in)
    constants := []object.Object{}
    globals := make([]object.Object, vm.GlobalsSize)
    symbolTable := compiler.NewSymbolTable()
    for i, v := range object.Builtins {
        symbolTable.DefineBuiltin(i, v.Name)
    }
    for {
        fmt.Fprintf(out, PROMPT)
        scanned := scanner.Scan()
        if !scanned {
            return
        }
        line := scanner.Text()
        l := lexer.New(line)
        p := parser.New(l)
        program := p.ParseProgram()
        if len(p.Errors()) != 0 {
            printParserErrors(out, p.Errors())
            continue
        }
        comp := compiler.NewWithState(symbolTable, constants)
        err := comp.Compile(program)
        if err != nil {
            fmt.Fprintf(out, "Woops! Compilation failed:\n %s\n", err)
            continue
        }
        code := comp.Bytecode()
        constants = code.Constants
        machine := vm.NewWithGlobalsStore(code, globals)
        err = machine.Run()
        if err != nil {
            fmt.Fprintf(out, "Woops! Executing bytecode failed:\n %s\n", err)
            continue
        }
        lastPopped := machine.LastPoppedStackElem()
        io.WriteString(out, lastPopped.Inspect())
        io.WriteString(out, "\n")
    }
}
```

Note that built-ins must be re-registered on the REPL's symbol table because `NewWithState` overwrites the one that `New` populates.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Hooking up the REPL" & "Chapter 8 / Executing built-in functions"*

---

### 63. Hash Construction Pairs Keys to `HashKey` for Stable Lookup

**Principle:** `object.Hash` uses `map[HashKey]HashPair`; only types implementing `object.Hashable` (Integer, Boolean, String) can serve as keys.

**Code:**
```go
// vm/vm.go
func (vm *VM) buildHash(startIndex, endIndex int) (object.Object, error) {
    hashedPairs := make(map[object.HashKey]object.HashPair)
    for i := startIndex; i < endIndex; i += 2 {
        key := vm.stack[i]
        value := vm.stack[i+1]
        pair := object.HashPair{Key: key, Value: value}
        hashKey, ok := key.(object.Hashable)
        if !ok {
            return nil, fmt.Errorf("unusable as hash key: %s", key.Type())
        }
        hashedPairs[hashKey.HashKey()] = pair
    }
    return &object.Hash{Pairs: hashedPairs}, nil
}

func (vm *VM) buildArray(startIndex, endIndex int) object.Object {
    elements := make([]object.Object, endIndex-startIndex)
    for i := startIndex; i < endIndex; i++ {
        elements[i-startIndex] = vm.stack[i]
    }
    return &object.Array{Elements: elements}
}
```

```go
// vm/vm.go
case code.OpArray:
    numElements := int(code.ReadUint16(ins[ip+1:]))
    ip += 2
    array := vm.buildArray(vm.sp-numElements, vm.sp)
    vm.sp = vm.sp - numElements
    err := vm.push(array)
    if err != nil {
        return err
    }

case code.OpHash:
    numElements := int(code.ReadUint16(ins[ip+1:]))
    ip += 2
    hash, err := vm.buildHash(vm.sp-numElements, vm.sp)
    if err != nil {
        return err
    }
    vm.sp = vm.sp - numElements
    err = vm.push(hash)
    if err != nil {
        return err
    }
```

The pattern is uniform: build the composite *before* decrementing `sp`, then decrement and push.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 6 / Array" & "Chapter 6 / Hash"*

---

### 64. Use Defect-Driven Development: Test, Watch Fail, Implement

**Principle:** The book's rhythm is mechanical: write the smallest test that captures the next behavior, run it, read the failure, write the minimum code to flip it green.

**Do:**
- Express the desired bytecode as `expectedInstructions` *before* touching the compiler — the diff in the disassembler output tells you exactly what to emit.
- Express the desired stack top as `expected interface{}` *before* touching the VM — the panic or wrong value tells you which opcode case is missing.
- Refactor `lastInstructionIsPop` → `lastInstructionIs` only when a second use case (e.g., `OpReturnValue`) demands it.

**Don't:**
- Don't write the implementation first and retrofit tests — the book's failing-test output is the primary design tool.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Bytecode, Disassemble!" & throughout*

---

### 65. Refactor by Extracting Methods When the Switch Grows

**Principle:** Each new opcode category (binary op, comparison, prefix, index, call) is an opportunity to extract a private method (`executeBinaryOperation`, `executeComparison`, `executeIndexExpression`, `executeCall`). Keep `Run` as a dispatch table.

**Code:**
```go
// vm/vm.go
case code.OpEqual, code.OpNotEqual, code.OpGreaterThan:
    err := vm.executeComparison(op)
    if err != nil {
        return err
    }

func (vm *VM) executeComparison(op code.Opcode) error {
    right := vm.pop()
    left := vm.pop()
    if left.Type() == object.INTEGER_OBJ && right.Type() == object.INTEGER_OBJ {
        return vm.executeIntegerComparison(op, left, right)
    }
    switch op {
    case code.OpEqual:
        return vm.push(nativeBoolToBooleanObject(right == left))
    case code.OpNotEqual:
        return vm.push(nativeBoolToBooleanObject(right != left))
    default:
        return fmt.Errorf("unknown operator: %d (%s %s)",
            op, left.Type(), right.Type())
    }
}

func (vm *VM) executeIntegerComparison(
    op code.Opcode,
    left, right object.Object,
) error {
    leftValue := left.(*object.Integer).Value
    rightValue := right.(*object.Integer).Value
    switch op {
    case code.OpEqual:
        return vm.push(nativeBoolToBooleanObject(rightValue == leftValue))
    case code.OpNotEqual:
        return vm.push(nativeBoolToBooleanObject(rightValue != leftValue))
    case code.OpGreaterThan:
        return vm.push(nativeBoolToBooleanObject(leftValue > rightValue))
    default:
        return fmt.Errorf("unknown operator: %d", op)
    }
}
```

The global `True`/`False` singletons make `right == left` a pointer comparison when both came from earlier `OpTrue`/`OpFalse`/comparison pushes.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Comparison Operators"*

---

### 66. Define the Complete Opcode Set Together — Don't Dribble

**Principle:** Even though opcodes are introduced chapter by chapter, keep the `const` block and `definitions` map cohesive so the encoding rules are visible at a glance.

**Complete opcode reference (final form):**

| Opcode          | Operands       | Purpose                                   |
|-----------------|----------------|-------------------------------------------|
| OpConstant      | 2 (uint16)     | Load constant from pool onto stack        |
| OpPop           | 0              | Pop top of stack                          |
| OpAdd           | 0              | Add two topmost stack elements            |
| OpSub           | 0              | Subtract                                  |
| OpMul           | 0              | Multiply                                  |
| OpDiv           | 0              | Divide                                    |
| OpTrue          | 0              | Push True                                 |
| OpFalse         | 0              | Push False                                |
| OpEqual         | 0              | Compare equality                          |
| OpNotEqual      | 0              | Compare inequality                        |
| OpGreaterThan   | 0              | Compare greater than                      |
| OpMinus         | 0              | Negate integer                            |
| OpBang          | 0              | Negate boolean (truthiness)               |
| OpJump          | 2 (uint16)     | Unconditional jump                        |
| OpJumpNotTruthy | 2 (uint16)     | Jump if top of stack is not truthy        |
| OpNull          | 0              | Push Null                                 |
| OpSetGlobal     | 2 (uint16)     | Store value in globals                    |
| OpGetGlobal     | 2 (uint16)     | Load value from globals                   |
| OpArray         | 2 (uint16)     | Build array from N stack elements         |
| OpHash          | 2 (uint16)     | Build hash from N stack elements          |
| OpIndex         | 0              | Index into array or hash                  |
| OpCall          | 1 (uint8)      | Call function with N arguments            |
| OpReturnValue   | 0              | Return with value from top of stack       |
| OpReturn        | 0              | Return with Null                          |
| OpSetLocal      | 1 (uint8)      | Store value as local binding              |
| OpGetLocal      | 1 (uint8)      | Load local binding                        |
| OpGetBuiltin    | 1 (uint8)      | Load built-in function                    |
| OpClosure       | 2 (uint16)+1 (uint8) | Create closure with N free variables |
| OpGetFree       | 1 (uint8)      | Load free variable from closure           |
| OpCurrentClosure | 0             | Push the currently executing closure      |

*Ref: Writing_a_Compiler_in_Go.md — "Complete Opcode Reference" (summary) & chapter-by-chapter const blocks*

---

### 67. Choose Operand Widths Deliberately

**Principle:** Operand width trades instruction size against maximum range; pick the smallest width that comfortably covers expected use.

**Do:**
- 2 bytes (uint16) for constant indices, globals, and jump targets — 65,536 is plenty.
- 1 byte (uint8) for locals, free vars, built-in indices, argument counts — 256 per function is plenty.

**Don't:**
- Don't reach for `uint32` "just in case" — the bytecode bloat compounds across every emitted instruction.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 2 / Starting With Bytes" & "Chapter 7 / Opcodes for Local Bindings"*

---

### 68. Treat the AST as the Source of Truth for Precedence

**Principle:** Don't re-implement precedence in the compiler. The Pratt parser already produced an AST whose structure encodes precedence; emit postfix-style instructions and the stack naturally evaluates in the right order.

**Code:**
```go
// vm/vm_test.go
func TestIntegerArithmetic(t *testing.T) {
    tests := []vmTestCase{
        {"1", 1},
        {"2", 2},
        {"1 + 2", 3},
        {"1 - 2", -1},
        {"1 * 2", 2},
        {"4 / 2", 2},
        {"50 / 2 * 2 + 10 - 5", 55},
        {"5 + 5 + 5 + 5 - 10", 10},
        {"2 * 2 * 2 * 2 * 2", 32},
        {"5 * 2 + 10", 20},
        {"5 + 2 * 10", 25},
        {"5 * (2 + 10)", 60},
        {"-5", -5},
        {"-10", -10},
        {"-50 + 100 + -50", 0},
        {"(5 + 10 * 2 + 15 / 3) * 2 + -10", 50},
    }
    runVmTests(t, tests)
}
```

`5 + 2 * 10` and `5 * (2 + 10)` need *no* special handling in the VM — they emit `OpConstant; OpConstant; OpMul; OpConstant; OpAdd` and `OpConstant; OpConstant; OpConstant; OpAdd; OpMul` respectively.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 3 / Infix Expressions"*

---

### 69. Use `EmittedInstruction` to Track the Last Two Emissions

**Principle:** Single-pass back-patching needs at least the last *two* instructions in flight (because `removeLastPop` rewrites "last" from "previous").

**Code:**
```go
// compiler/compiler.go
type EmittedInstruction struct {
    Opcode   code.Opcode
    Position int
}

// Inside emit:
func (c *Compiler) emit(op code.Opcode, operands ...int) int {
    ins := code.Make(op, operands...)
    pos := c.addInstruction(ins)
    c.setLastInstruction(op, pos)
    return pos
}

// After entering scopes:
func (c *Compiler) removeLastPop() {
    last := c.scopes[c.scopeIndex].lastInstruction
    previous := c.scopes[c.scopeIndex].previousInstruction
    old := c.currentInstructions()
    new := old[:last.Position]
    c.scopes[c.scopeIndex].instructions = new
    c.scopes[c.scopeIndex].lastInstruction = previous
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 4 / Compiling Conditionals"*

---

### 70. Handle the Empty-Function Body Edge Case Explicitly

**Principle:** Functions with empty bodies or only `let` statements can't synthesize an implicit return value; detect this and append `OpReturn`.

**Code:**
```go
// compiler/compiler_test.go
func TestFunctionsWithoutReturnValue(t *testing.T) {
    tests := []compilerTestCase{
        {
            input: `fn() { }`,
            expectedConstants: []interface{}{
                []code.Instructions{
                    code.Make(code.OpReturn),
                },
            },
            expectedInstructions: []code.Instructions{
                code.Make(code.OpClosure, 0, 0),
                code.Make(code.OpPop),
            },
        },
    }
    runCompilerTests(t, tests)
}
```

The compiler's two-step end-of-body logic (`replaceLastPopWithReturn` then `if !lastInstructionIs(OpReturnValue) emit OpReturn`) handles both "ends with expression" and "ends with let-or-nothing" uniformly.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / It's Not Nothing, It's Null"*

---

### 71. Preallocate Frame Stack to Avoid Hot-Path Allocation

**Principle:** The compiler's `scopes` stack uses append-and-slice; the VM's `frames` stack preallocates `MaxFrames = 1024` slots because the call/return cycle is hotter than scope entry/exit.

**Code:**
```go
// vm/vm.go
const MaxFrames = 1024

func New(bytecode *compiler.Bytecode) *VM {
    // ...
    frames := make([]*Frame, MaxFrames)
    frames[0] = mainFrame
    return &VM{
        // ...
        frames:      frames,
        framesIndex: 1,
    }
}

func (vm *VM) pushFrame(f *Frame) {
    vm.frames[vm.framesIndex] = f
    vm.framesIndex++
}

func (vm *VM) popFrame() *Frame {
    vm.framesIndex--
    return vm.frames[vm.framesIndex]
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 7 / Adding Frames"*

---

### 72. Closures in Deeply Nested Scopes Chain Through `defineFree`

**Principle:** A free variable in an inner scope may itself be free from the perspective of its immediate enclosing scope; `Resolve`'s recursion naturally handles this — every enclosed scope that fails its own `store` lookup calls `defineFree` on the *current* table before returning.

**Test coverage:**
```go
// compiler/compiler_test.go
{
    input: `
    fn(a) {
         fn(b) {
             fn(c) {
                 a + b + c
             }
         }
    };
    `,
    expectedConstants: []interface{}{
        []code.Instructions{
            code.Make(code.OpGetFree, 0),  // a (free in innermost)
            code.Make(code.OpGetFree, 1),  // b (free in innermost)
            code.Make(code.OpAdd),
            code.Make(code.OpGetLocal, 0), // c (local)
            code.Make(code.OpAdd),
            code.Make(code.OpReturnValue),
        },
        []code.Instructions{
            code.Make(code.OpGetFree, 0),  // a (free in middle too!)
            code.Make(code.OpGetLocal, 0), // b (local in middle)
            code.Make(code.OpClosure, 0, 2),
            code.Make(code.OpReturnValue),
        },
        []code.Instructions{
            code.Make(code.OpGetLocal, 0), // a (local in outermost)
            code.Make(code.OpClosure, 1, 1),
            code.Make(code.OpReturnValue),
        },
    },
    expectedInstructions: []code.Instructions{
        code.Make(code.OpClosure, 2, 0),
        code.Make(code.OpPop),
    },
},
```

The middle function emits `OpGetFree 0` for `a` because from its perspective `a` is also free — and the enclosing scope's load instruction is what populates *its* `Free[0]`.

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Compiling and resolving free variables"*

---

### 73. Globals Are Never Free — They're Globally Reachable

**Principle:** Don't classify global bindings as free variables; `Resolve` short-circuits them so deeply-nested closures still emit `OpGetGlobal`.

**Test coverage:**
```go
// compiler/compiler_test.go
{
    input: `
    let global = 55;
    fn() {
        let a = 66;
        fn() {
            let b = 77;
            fn() {
                 let c = 88;
                 global + a + b + c;
            }
        }
    }
    `,
    // innermost function's instructions:
    // code.Make(code.OpGetGlobal, 0),     // global
    // code.Make(code.OpGetFree, 0),       // a
    // code.Make(code.OpAdd),
    // code.Make(code.OpGetFree, 1),       // b
    // code.Make(code.OpAdd),
    // code.Make(code.OpGetLocal, 0),      // c
    // code.Make(code.OpAdd),
    // code.Make(code.OpReturnValue),
}
```

The short-circuit lives in `Resolve`:

```go
if obj.Scope == GlobalScope || obj.Scope == BuiltinScope {
    return obj, ok
}
free := s.defineFree(obj)
return free, true
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Compiling and resolving free variables"*

---

### 74. Build a Crude Bytecode Dumper for VM Debugging

**Principle:** When a VM test fails inexplicably, dump the constant pool to see exactly which instructions make up each compiled function.

**Code:**
```go
// vm/vm_test.go
func runVmTests(t *testing.T, tests []vmTestCase) {
    // [...]
    for _, tt := range tests {
        // [...]
        for i, constant := range comp.Bytecode().Constants {
            fmt.Printf("CONSTANT %d %p (%T):\n", i, constant, constant)
            switch constant := constant.(type) {
            case *object.CompiledFunction:
                fmt.Printf(" Instructions:\n%s", constant.Instructions)
            case *object.Integer:
                fmt.Printf(" Value: %d\n", constant.Value)
            }
            fmt.Printf("\n")
        }
        vm := New(comp.Bytecode())
        // [...]
    }
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Recursive Closures"*

---

### 75. Parser Support: Stash the Let-Bound Name on the Function Literal

**Principle:** The compiler needs to know the function's name *while* compiling its body (to set up `FunctionScope`); have the parser attach the let-bound name to the `FunctionLiteral` node.

**Code:**
```go
// ast/ast.go
type FunctionLiteral struct {
    Token      token.Token
    Parameters []*Identifier
    Body       *BlockStatement
    Name       string
}

func (fl *FunctionLiteral) String() string {
    var out bytes.Buffer
    out.WriteString(fl.TokenLiteral())
    if fl.Name != "" {
        out.WriteString(fmt.Sprintf("<%s>", fl.Name))
    }
    out.WriteString("(")
    // ...
}
```

```go
// parser/parser.go
func (p *Parser) parseLetStatement() *ast.LetStatement {
    // ...
    stmt.Value = p.parseExpression(LOWEST)
    if fl, ok := stmt.Value.(*ast.FunctionLiteral); ok {
        fl.Name = stmt.Name.Value
    }
    // ...
}
```

```go
// parser/parser_test.go
func TestFunctionLiteralWithName(t *testing.T) {
    input := `let myFunction = fn() { };`
    l := lexer.New(input)
    p := New(l)
    program := p.ParseProgram()
    checkParserErrors(t, p)
    // ...
    function, ok := stmt.Value.(*ast.FunctionLiteral)
    if !ok {
        t.Fatalf("stmt.Value is not ast.FunctionLiteral. got=%T",
            stmt.Value)
    }
    if function.Name != "myFunction" {
        t.Fatalf("function literal name wrong. want 'myFunction', got=%q\n",
            function.Name)
    }
}
```

*Ref: Writing_a_Compiler_in_Go.md — "Chapter 9 / Recursive Closures"*

---

## Anti-Patterns & Common Mistakes

- **Calling `code.Lookup` in the VM's hot loop:** ~10x slowdown vs. direct `switch op`. → *fix:* Switch directly on `Opcode`; reserve `Lookup` for the disassembler.
- **Forgetting to skip operand bytes after decoding:** Causes the next iteration to misinterpret operands as opcodes (book's recurring panic: `runtime error: index out of range`). → *fix:* Always pair `ReadUint16`/`ReadUint8` with `vm.currentFrame().ip += width`.
- **Letting expression statements leave values on the stack:** Causes slow stack growth and eventual overflow. → *fix:* Emit `OpPop` after every `*ast.ExpressionStatement`.
- **Treating booleans as constants:** Wastes constant-pool slots and loses pointer-identity comparison. → *fix:* Add `OpTrue`/`OpFalse` pushing global singletons.
- **Inverting operand order for non-commutative operators:** `left - right` becomes `right - left`. → *fix:* Always pop `right` first, then `left`; document the convention in `pop()`.
- **Back-patching with the wrong offset:** Off-by-one in `changeOperand`. → *fix:* Use `len(c.currentInstructions())` *after* compiling the target branch, not before.
- **Using `OpJump` to skip a consequence without an alternative:** Leaves the alternative's value in the wrong place. → *fix:* Always emit `OpJump` after the consequence; emit `OpNull` when there's no real alternative.
- **Iterating Go maps for hash literals without sorting:** Random key order → flaky tests, non-deterministic constant indices. → *fix:* `sort.Slice(keys, func(i, j int) bool { return keys[i].String() < keys[j].String() })`.
- **Defining `let name = value` after compiling `value`:** Breaks recursive self-reference. → *fix:* Hoist `symbolTable.Define(name)` above `Compile(value)`.
- **Trying to load a self-referential closure via `OpGetFree`:** The local slot for the closure hasn't been populated yet when the free-var load runs. → *fix:* Use `OpCurrentClosure` (push the executing closure) for `FunctionScope` symbols.
- **Wrapping built-ins in `evaluator.NULL`:** Couples the object package to the evaluator. → *fix:* Return `nil` from built-ins; let each caller substitute its own Null (`vm.Null` or `evaluator.NULL`).
- **Allocating fresh arrays in `rest`/`push` without preserving immutability:** Silent mutation bugs. → *fix:* Always allocate a new `*object.Array` with `make + copy`.
- **Letting the REPL create a new symbol table per line:** Breaks multi-line bindings (`let a = 1; let b = a + 1;` across two prompts). → *fix:* Use `NewWithState`/`NewWithGlobalsStore` and persist `symbolTable`, `constants`, `globals`.
- **Special-casing built-ins vs. user functions in the calling convention:** Doubles the dispatch surface. → *fix:* Push the callee (closure or built-in) onto the stack, then `OpCall`; let `executeCall` type-switch.
- **Forgetting `OpReturnValue` is required even for implicit returns:** Empty-body functions return garbage. → *fix:* `replaceLastPopWithReturn` then fall through to `emit(OpReturn)` if still no `OpReturnValue`.
- **Setting `vm.sp = frame.basePointer` on return (instead of `basePointer - 1`):** Leaves the just-called function pointer on the stack. → *fix:* `vm.sp = frame.basePointer - 1` collapses locals *and* function in one operation.

## Decision Heuristics / Checklists

### When Adding a New Opcode
1. Add it to the `const (...)` block via `iota`.
2. Register a `Definition` with the correct `OperandWidths`.
3. Extend `Make`'s switch if a new operand width is introduced.
4. Extend `ReadOperands` and `ReadUint*` helpers to decode it.
5. Extend `fmtInstruction`'s operand-count switch (0/1/2).
6. Add a `TestMake` and `TestReadOperands` row.
7. Add a `TestInstructionsString` row.
8. Write a compiler test (`expectedInstructions`).
9. Emit the opcode from the compiler's `Compile` switch.
10. Write a VM test (`expected` value).
11. Add a `case` in `Run`'s switch.

### When Choosing an Operand Width
- Constant index, global index, jump target → **2 bytes** (uint16). 65,536 ceiling.
- Local index, free-var index, built-in index, argument count → **1 byte** (uint8). 256 per function.
- Anything else → question whether you really need a new operand shape.

### When Deciding Where to Store State in the VM
- Top of stack → temporary values from the currently executing expression.
- `globals[0..65535]` → top-level `let` bindings.
- `stack[basePointer..basePointer+NumLocals-1]` → local bindings (including arguments).
- `closure.Free[0..255]` → captured free variables.
- `frame.cl` → the currently executing closure (for `OpCurrentClosure`).

### When Adding a New Symbol Scope
1. Define a new `SymbolScope` constant alongside `GlobalScope`/`LocalScope`/etc.
2. Decide whether `Define` (or a new method like `DefineBuiltin`/`DefineFunctionName`) sets it.
3. Update `Resolve` if the new scope should short-circuit (`GlobalScope`/`BuiltinScope`) or trigger `defineFree` (anything else from an outer scope).
4. Add a `case` to `loadSymbol` mapping the scope to its `OpGet*` opcode.

### Testing Checklist for Each New Feature
- [ ] Compiler test: `expectedInstructions` and `expectedConstants`.
- [ ] VM test: `expected` value (or error) on top of stack after `LastPoppedStackElem`.
- [ ] Edge cases: empty input, wrong types, wrong arity, out-of-bounds, nested usage.
- [ ] REPL spot-check if the feature changes global state.

## Key Takeaways

1. **The bytecode format follows the VM architecture, not the other way around.** Decide stack vs. register first; the opcodes fall out.
2. **A flat `[]byte` plus a `Definition` map is enough bytecode infrastructure** — don't over-engineer instruction types until the cost of bytes-as-instructions bites.
3. **The disassembler (`Instructions.String()`) is the highest-leverage debugging tool you'll write.** Build it before you need it.
4. **Single-pass compilation with back-patching** handles forward jumps (conditionals) without a second AST walk.
5. **Tracking the last two emitted instructions** is the minimum state for back-patching and `removeLastPop`.
6. **Compile-time symbol resolution** turns undefined-variable errors from runtime panics into compiler messages.
7. **A symbol table with an `Outer` pointer** elegantly supports arbitrary scope nesting and free-variable detection.
8. **Treat arguments as locals** — they already sit in the right place on the stack; the calling convention folds them into the local-binding machinery for free.
9. **A frame is just `{closure, ip, basePointer}`** — base pointer doubles as a reset point on return and a reference for local-slot addressing.
10. **Closures = functions + a slice of captured free variables.** Detect free variables in the compiler's symbol table, push them onto the enclosing stack, then `OpClosure` rolls them into a `*object.Closure`.
11. **Recursive closures need `OpCurrentClosure`** because the binding's local slot isn't populated when the load runs — push the executing closure directly.
12. **Built-ins belong in the `object` package**, not the evaluator. Use a slice (not a map) for stable iteration and a `BuiltinScope` so the compiler treats them uniformly with other scopes.
13. **Test-first compiler development is fast** because the disassembler output tells you precisely what's missing — no printf debugging required.
14. **Stack arithmetic is faster than tree-walking** — 3.3x speedup with no low-level optimization, just by changing the evaluation strategy.
15. **Invest in test helpers early**: `runCompilerTests`, `runVmTests`, `testInstructions`, `testConstants`, and `testExpectedObject` make every subsequent feature a one-test-case addition.

## Cross-References
- Related: [[../summaries/Writing_a_Compiler_in_Go_-_Thorsten_Ball.md]]
- Predecessor: [[../Writing_An_Interpreter_in_Go.md]] (tree-walking evaluator; this book reuses its lexer, parser, AST, and object system)
- Topic index: [[../INDEX.md]]
