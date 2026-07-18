# Writing An Interpreter In Go - Thorsten Ball

## Comprehensive Summary

This book walks readers through building a complete tree-walking interpreter for a programming language called Monkey, implemented entirely in Go. The project is built bottom-up: first a lexer to tokenize source code, then a parser to build an abstract syntax tree (AST), then an evaluator that walks the AST and produces results. No third-party tools or libraries are used.

---

## Introduction

Thorsten Ball wrote this book to fill the gap between academic compiler textbooks and trivial blog-post interpreters. The goal is a hands-on, line-by-line guide to building a real interpreter that handles a C-like language with curly braces, semicolons, functions, closures, and data structures.

### The Monkey Programming Language

Monkey is a language designed specifically for this book. Its features include:

- C-like syntax
- Variable bindings (`let x = 5;`)
- Integers and booleans
- Arithmetic expressions
- Built-in functions
- First-class and higher-order functions
- Closures
- Strings, arrays, and hashes

Example Monkey code:

```
let add = fn(a, b) { return a + b; };
add(5, 5); // => 10

let fibonacci = fn(x) {
  if (x == 0) {
    0
  } else {
    if (x == 1) {
      1
    } else {
      fibonacci(x - 1) + fibonacci(x - 2);
    }
  }
};
```

Functions are first-class citizens, meaning they can be passed as arguments, returned from other functions, and bound to names. Monkey also supports "if expressions" that produce values rather than just controlling flow.

### Why Go?

Go is chosen for its readability, excellent standard library (including a built-in testing framework), and the way Go code maps closely to lower-level languages like C, C++, and Rust. No meta-programming or complex object-oriented patterns are needed.

---

## Chapter 1: Lexing

### 1.1 - Lexical Analysis

The first transformation in an interpreter is from source code to tokens. This process is called lexical analysis (lexing) and is performed by a lexer (also called a tokenizer or scanner). Tokens are small, easily categorizable data structures fed to the parser.

Example: `"let x = 5 + 5;"` becomes:

```
[LET, IDENTIFIER("x"), EQUAL_SIGN, INTEGER(5), PLUS_SIGN, INTEGER(5), SEMICOLON]
```

Whitespace is not significant in Monkey (unlike Python), so the lexer skips it. Production lexers may attach line numbers and filenames to tokens for better error messages, but this book keeps things simple.

### 1.2 - Defining Our Tokens

The token system is defined in a `token` package:

```go
type TokenType string
type Token struct {
    Type    TokenType
    Literal string
}
```

`TokenType` is a string for easy debugging. Constants are defined for each token type: `ILLEGAL`, `EOF`, `IDENT`, `INT`, `ASSIGN`, `PLUS`, `COMMA`, `SEMICOLON`, `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `FUNCTION`, `LET`, etc.

A `keywords` map and `LookupIdent` function distinguish user-defined identifiers from language keywords like `fn` and `let`.

### 1.3 - The Lexer

The `Lexer` struct tracks position in the input:

```go
type Lexer struct {
    input        string
    position     int  // current position (points to current char)
    readPosition int  // next reading position (after current char)
    ch           byte // current char under examination
}
```

Two position pointers allow peeking ahead. The `readChar()` method advances through the input. The `NextToken()` method uses a switch statement on `l.ch` to produce the appropriate token for each character.

Key methods:
- `readIdentifier()` reads consecutive letters to form identifiers/keywords
- `readNumber()` reads consecutive digits to form integer literals
- `skipWhitespace()` skips spaces, tabs, newlines, and carriage returns
- `peekChar()` looks ahead without advancing (needed for two-character tokens)

### 1.4 - Extending the Token Set and Lexer

The lexer is extended to support:
- **One-character tokens**: `-`, `/`, `*`, `<`, `>`
- **Two-character tokens**: `==` and `!=` (using `peekChar()`)
- **New keywords**: `true`, `false`, `if`, `else`, `return`

Two-character tokens require looking ahead: when the lexer sees `=`, it peeks at the next character. If it is also `=`, it produces `token.EQ`; otherwise it produces `token.ASSIGN`. The same pattern applies for `!` vs `!=`.

### 1.5 - Start of a REPL

A basic REPL (Read-Eval-Print-Loop) is created. At this point it only tokenizes input and prints tokens. The `Start` function in `repl/repl.go` reads lines from input, feeds them to the lexer, and prints each token until EOF. The `main.go` file welcomes the user and starts the REPL.

---

## Chapter 2: Parsing

### 2.1 - Parsers

A parser takes input data (frequently text or tokens) and builds a data structure -- often an abstract syntax tree (AST) -- giving a structural representation of the input while checking for correct syntax.

The key insight is that programming language parsers are conceptually similar to simpler parsers like JSON parsers. They turn text into a structured representation. The difference is that the AST for a programming language is not immediately visible from the source code.

### 2.2 - Why Not a Parser Generator?

Parser generators (yacc, bison, ANTLR) take formal grammar descriptions and produce parsers automatically. While useful in production, the book argues that writing a parser by hand is essential for learning. Only after writing your own parser do you truly understand the benefits and drawbacks of parser generators.

### 2.3 - Writing a Parser for the Monkey Programming Language

The parser uses a **recursive descent** strategy, specifically **top-down operator precedence** parsing (Pratt parsing, after Vaughan Pratt).

The `Parser` struct holds:

```go
type Parser struct {
    l      *lexer.Lexer
    errors []string
    curToken token.Token
    peekToken token.Token
    prefixParseFns map[token.TokenType]prefixParseFn
    infixParseFns  map[token.TokenType]infixParseFn
}
```

`curToken` and `peekToken` act like the lexer's two pointers, but for tokens. The parser always looks at `curToken` to decide what to do, and uses `peekToken` when `curToken` alone is insufficient.

The `ParseProgram()` method iterates through tokens, calling `parseStatement()` for each statement until EOF. Error handling is built in: the parser collects errors in a slice and reports all of them rather than stopping at the first one.

### 2.4 - Parsing Let Statements

The AST begins with core interfaces:

```go
type Node interface {
    TokenLiteral() string
    String() string
}
type Statement interface { Node; statementNode() }
type Expression interface { Node; expressionNode() }
```

`Program` is the root node containing a slice of `Statement` nodes. `LetStatement` holds a `Name` (identifier) and `Value` (expression). `Identifier` implements `Expression` so it can be reused both as a binding name and as an expression.

The `String()` method is added to all AST nodes, enabling readable debugging and testing by comparing AST output to expected strings.

### 2.5 - Parsing Return Statements

`ReturnStatement` has a `ReturnValue` field holding an expression. Parsing is straightforward: detect `return` keyword, skip past the expression (initially), and stop at the semicolon.

### 2.6 - Parsing Expressions

This is the heart of the parser. Expression parsing is challenging because of:
- **Operator precedence**: `5 * 5 + 10` must parse as `((5 * 5) + 10)`
- **Same tokens in different positions**: `-` can be prefix (`-5`) or infix (`5 - 3`)
- **Grouped expressions**: `(5 + 5) * 2` must boost precedence of the addition

#### Pratt Parsing

Pratt's approach associates parsing functions with token types rather than grammar rules. Each token type can have two parsing functions:
- **prefixParseFn**: called when the token appears in prefix position (e.g., `-5`, `!true`)
- **infixParseFn**: called when the token appears in infix position (e.g., `5 + 5`)

```go
type (
    prefixParseFn func() ast.Expression
    infixParseFn  func(ast.Expression) ast.Expression
)
```

Precedence levels are defined using `iota`:

```go
const (
    _           int = iota
    LOWEST
    EQUALS      // ==
    LESSGREATER // > or <
    SUM         // +
    PRODUCT     // *
    PREFIX      // -X or !X
    CALL        // myFunction(X)
    INDEX       // array[index]
)
```

The central `parseExpression` method:

```go
func (p *Parser) parseExpression(precedence int) ast.Expression {
    prefix := p.prefixParseFns[p.curToken.Type]
    if prefix == nil {
        p.noPrefixParseFnError(p.curToken.Type)
        return nil
    }
    leftExp := prefix()
    for !p.peekTokenIs(token.SEMICOLON) && precedence < p.peekPrecedence() {
        infix := p.infixParseFns[p.peekToken.Type]
        if infix == nil {
            return leftExp
        }
        p.nextToken()
        leftExp = infix(leftExp)
    }
    return leftExp
}
```

#### How Pratt Parsing Works (Detailed Walkthrough)

Parsing `1 + 2 + 3`:

1. `parseExpression(LOWEST)` is called. `curToken` is `1`, `peekToken` is `+`.
2. The prefix parser for `INT` (`parseIntegerLiteral`) returns an `*ast.IntegerLiteral(1)`.
3. The loop checks: `peekToken` is not `SEMICOLON` and `LOWEST < SUM` (precedence of `+`). True, so it enters the loop.
4. The infix parser for `+` (`parseInfixExpression`) is called with `left = IntegerLiteral(1)`. It saves `SUM` as precedence, advances tokens, and calls `parseExpression(SUM)`.
5. In this inner call, `parseIntegerLiteral` returns `IntegerLiteral(2)`. The loop condition `SUM < SUM` is false (equal, not less than), so the loop does not execute. `IntegerLiteral(2)` is returned.
6. Back in `parseInfixExpression`, `Right = IntegerLiteral(2)`, creating `InfixExpression(1, +, 2)`.
7. Back in the outer loop, `leftExp` is now `InfixExpression(1, +, 2)`. The condition checks again: `peekToken` is the second `+` and `LOWEST < SUM` is still true.
8. The process repeats, wrapping the first `InfixExpression` as the `Left` of a new one with `Right = IntegerLiteral(3)`.

Result: `InfixExpression(InfixExpression(1, +, 2), +, 3)` -- correct left-associativity.

The key mechanism is the interaction between **right-binding power** (the `precedence` argument) and **left-binding power** (`peekPrecedence`). The loop condition `precedence < p.peekPrecedence()` determines whether the next operator "sucks in" what has been parsed so far.

For right-associativity, you would decrement the precedence when calling `parseExpression` for the right side.

#### Expression Types Parsed

**Identifiers**: The simplest expression. `parseIdentifier` returns an `*ast.Identifier` with the current token's literal value.

**Integer Literals**: `parseIntegerLiteral` converts the string literal to `int64` using `strconv.ParseInt` and wraps it in `*ast.IntegerLiteral`.

**Prefix Operators** (`!` and `-`): `parsePrefixExpression` constructs a node, advances tokens, and recursively calls `parseExpression(PREFIX)` for the right operand.

**Infix Operators** (`+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`): `parseInfixExpression` takes the left expression, saves the current precedence, advances, and calls `parseExpression` with the operator's precedence for the right side.

**Boolean Literals**: `parseBoolean` checks `curTokenIs(token.TRUE)` and returns `*ast.Boolean`.

**Grouped Expressions**: `parseGroupedExpression` advances past `(`, calls `parseExpression(LOWEST)`, and expects `)`. This is the "greatest trick" of Pratt parsing -- parentheses boost precedence naturally without a separate AST node.

**If Expressions**: `parseIfExpression` parses `if (<condition>) { <consequence> } else { <alternative> }`. The else clause is optional. `BlockStatement` is defined as a series of statements enclosed in braces.

**Function Literals**: `parseFunctionLiteral` parses `fn(<params>) { <body> }`. Parameters are parsed as a comma-separated list of identifiers.

**Call Expressions**: `parseCallExpression` parses `<expression>(<arguments>)`. Registered as an infix parser for `(`. Arguments are parsed as comma-separated expressions using `parseExpressionList`.

### 2.8 - Extending the Parser

Helper functions `testLiteralExpression`, `testInfixExpression`, and `testBooleanLiteral` are introduced to reduce test boilerplate. The existing `parseCallArguments` method is generalized into `parseExpressionList(end token.TokenType)` which is reused for both call arguments and array elements.

### 2.9 - Read-Parse-Print-Loop

The REPL is updated to use the parser instead of the lexer. It now parses input, checks for errors, and prints the AST's `String()` representation. A friendly monkey ASCII art error message is added for parser errors.

The updated REPL demonstrates correct operator precedence:
```
>> let x = 1 * 2 * 3 * 4 * 5
let x = ((((1 * 2) * 3) * 4) * 5);
>> x * y / 2 + 3 * 8 - 123
((((x * y) / 2) + (3 * 8)) - 123)
```

---

## Chapter 3: Evaluation

### 3.1 - Giving Meaning to Symbols

Evaluation is where code becomes meaningful. `1 + 2` becomes `3`. The evaluation process defines how the programming language works -- whether integers are truthy, what order arguments are evaluated in, etc.

### 3.2 - Strategies of Evaluation

Different interpreter architectures:
- **Tree-walking interpreters**: Traverse the AST directly and evaluate on the fly (simplest, what this book builds)
- **Bytecode interpreters**: Convert AST to bytecode, then interpret bytecode in a virtual machine (faster; used by Ruby >= 1.9, Lua)
- **JIT compilers**: Compile bytecode to native machine code just before execution (fastest; used by LuaJIT, JavaScript engines)

### 3.3 - A Tree-Walking Interpreter

The evaluator is a recursive `Eval` function:

```go
func Eval(node ast.Node, env *object.Environment) object.Object
```

It pattern-matches on AST node types and recursively evaluates. For an `*ast.InfixExpression`, it evaluates left and right operands, then applies the operator. For an `*ast.IfExpression`, it evaluates the condition and then the appropriate branch.

### 3.4 - Representing Objects

Every value in the interpreter is represented as an `object.Object`:

```go
type Object interface {
    Type() ObjectType
    Inspect() string
}
type ObjectType string
```

Three foundational types are defined:
- **Integer**: `struct { Value int64 }`
- **Boolean**: `struct { Value bool }`
- **Null**: `struct{}` (represents absence of value)

Singletons are used for `TRUE`, `FALSE`, and `NULL` to avoid unnecessary allocations and enable pointer comparison for equality checks.

### 3.5 - Evaluating Expressions

**Integer Literals**: `Eval` returns `*object.Integer{Value: node.Value}` when encountering `*ast.IntegerLiteral`.

**Boolean Literals**: Uses `nativeBoolToBooleanObject` to return the singleton `TRUE` or `FALSE`.

**Null**: A single `NULL` instance is used throughout.

**Prefix Expressions**: The `!` operator negates truthiness (truthy values become `FALSE`, falsy values become `TRUE`). Everything except `NULL` and `FALSE` is truthy. The `-` operator negates integers and returns `NULL` for non-integers.

**Infix Expressions**: Arithmetic operators (`+`, `-`, `*`, `/`) work on integers. Comparison operators (`>`, `<`, `==`, `!=`) produce booleans. Boolean equality uses pointer comparison (works because of singletons). Integer comparison unwraps and compares values.

The REPL now works as a calculator:
```
>> 5 * 5 + 10
35
>> 3 + 4 * 5 == 3 * 1 + 4 * 5
true
```

### 3.6 - Conditionals

If-else expressions evaluate the condition and then the appropriate branch. The `isTruthy` function defines Monkey's truthiness rules: everything is truthy except `NULL` and `FALSE`.

```go
func evalIfExpression(ie *ast.IfExpression) object.Object {
    condition := Eval(ie.Condition, env)
    if isTruthy(condition) {
        return Eval(ie.Consequence, env)
    } else if ie.Alternative != nil {
        return Eval(ie.Alternative, env)
    } else {
        return NULL
    }
}
```

### 3.7 - Return Statements

Return statements are implemented using `object.ReturnValue`, a wrapper that signals "stop evaluation and return this value." The key challenge is handling nested block statements: a `return` inside a nested `if` must bubble up through all enclosing blocks.

The solution distinguishes between `evalProgram` (for top-level program statements) and `evalBlockStatement` (for block statements inside expressions). `evalBlockStatement` does NOT unwrap `ReturnValue`, allowing it to propagate upward. `evalProgram` unwraps the final `ReturnValue`.

```go
type ReturnValue struct {
    Value Object
}
```

The `unwrapReturnValue` function is used when returning from function calls to prevent returns from bubbling through multiple function boundaries.

### 3.8 - Error Handling

Errors are represented as `object.Error`:

```go
type Error struct {
    Message string
}
```

The `newError` function creates errors. The `isError` helper checks if an object is an error, allowing the evaluator to short-circuit when errors are encountered. Errors propagate upward through the evaluation chain -- if evaluating any sub-expression produces an error, the entire expression evaluation stops and returns the error.

Test cases ensure errors are produced for: unknown identifiers, type mismatches in operators, wrong number of arguments, using non-functions as functions, and unsupported operations.

### 3.9 - Bindings and the Environment

The `object.Environment` stores variable bindings:

```go
type Environment struct {
    store map[string]Object
    outer *Environment
}
```

The `outer` field enables scoped environments. `Get` checks the current store first, then delegates to the enclosing environment. `Set` always writes to the current (innermost) environment.

When evaluating `*ast.LetStatement`, the expression's value is computed and stored with `env.Set(node.Name.Value, val)`. When evaluating `*ast.Identifier`, the value is looked up with `env.Get(node.Value)`.

The environment persists between REPL lines (so `let x = 5` on one line is accessible on the next) but is fresh for each test case.

### 3.10 - Functions and Function Calls

Functions are represented as `object.Function`:

```go
type Function struct {
    Parameters []*ast.Identifier
    Body       *ast.BlockStatement
    Env        *Environment
}
```

The `Env` field is crucial: it captures the environment in which the function was defined, enabling closures.

When evaluating a function literal, the current environment is captured:

```go
case *ast.FunctionLiteral:
    return &object.Function{Parameters: node.Parameters, Env: env, Body: node.Body}
```

When calling a function:
1. Evaluate the function expression
2. Evaluate each argument left-to-right
3. Create a new enclosed environment (`NewEnclosedEnvironment(fn.Env)`) -- extending the function's captured environment, not the calling environment
4. Bind parameters to arguments in the new environment
5. Evaluate the function body in this new environment
6. Unwrap any `ReturnValue` so it does not propagate through the caller

```go
func extendFunctionEnv(fn *object.Function, args []object.Object) *object.Environment {
    env := object.NewEnclosedEnvironment(fn.Env)
    for paramIdx, param := range fn.Parameters {
        env.Set(param.Value, args[paramIdx])
    }
    return env
}
```

**Closures** work because the function's `Env` captures the defining environment. A function returned from another function retains access to the enclosing scope's variables:

```
>> let newAdder = fn(x) { fn(y) { x + y } };
>> let addTwo = newAdder(2);
>> addTwo(3);
5
```

### 3.11 - Who Is Taking the Trash Out?

The interpreter relies on Go's garbage collector. Each `Environment` holds references to objects, and Go's GC reclaims objects when they are no longer reachable. While not the most efficient approach, it is correct and keeps the implementation simple.

---

## Chapter 4: Extending the Interpreter

### 4.1 - Data Types and Functions (Overview)

The interpreter is extended with strings, built-in functions, arrays, and hashes. Each extension follows the same pattern: extend the lexer (new tokens), extend the parser (new AST nodes and parsing functions), extend the object system (new object types), and extend the evaluator.

### 4.2 - Strings

**Lexer**: String literals are delimited by double quotes. A `readString()` method reads characters until a closing `"` or EOF. `token.STRING` is the new token type.

**Parser**: `ast.StringLiteral` holds a string value. Registered as a prefix parser for `token.STRING`.

**Object System**: `object.String` wraps a Go string. String concatenation with `+` is supported via `evalStringInfixExpression`.

```
>> let greeting = "Hello" + " " + "World!";
>> greeting
Hello World!
```

### 4.3 - Built-in Functions

Built-in functions bridge Monkey and Go. They are defined in Go and callable from Monkey code.

The `object.Builtin` type wraps `BuiltinFunction func(args ...Object) Object`.

**len**: Returns string length (number of characters). Extended later to also work on arrays.

```go
"len": &object.Builtin{
    Fn: func(args ...object.Object) object.Object {
        if len(args) != 1 {
            return newError("wrong number of arguments. got=%d, want=1", len(args))
        }
        switch arg := args[0].(type) {
        case *object.String:
            return &object.Integer{Value: int64(len(arg.Value))}
        default:
            return newError("argument to `len` not supported, got %s", args[0].Type())
        }
    },
},
```

Built-ins are looked up in `evalIdentifier` as a fallback when an identifier is not found in the environment. The `applyFunction` method is extended to handle `*object.Builtin` by calling `fn.Fn(args...)`.

**puts** (added in section 4.6): Prints arguments to STDOUT, returns `NULL`.

### 4.4 - Arrays

**Lexer**: New tokens `token.LBRACKET` (`[`) and `token.RBRACKET` (`]`).

**Parser**: `ast.ArrayLiteral` contains `Elements []Expression`. `ast.IndexExpression` contains `Left Expression` and `Index Expression`. The index operator is registered as an infix parser with `INDEX` precedence.

**Object System**: `object.Array` wraps `Elements []object.Object`.

**Evaluator**: Array literals are evaluated by evaluating each element expression. Index expressions evaluate the left side and the index, then perform bounds checking. Out-of-bounds access returns `NULL`.

**Built-in functions for arrays**:
- `first(array)`: Returns the first element or `NULL` if empty
- `last(array)`: Returns the last element or `NULL` if empty
- `rest(array)`: Returns a new array with all elements except the first, or `NULL` if empty
- `push(array, element)`: Returns a new array with the element appended (arrays are immutable)
- `len(array)`: Extended to return array length

With these primitives, higher-order functions like `map` and `reduce` can be defined in Monkey itself:

```
let map = fn(arr, f) {
    let iter = fn(arr, accumulated) {
        if (len(arr) == 0) {
            accumulated
        } else {
            iter(rest(arr), push(accumulated, f(first(arr))));
        }
    };
    iter(arr, []);
};

let reduce = fn(arr, initial, f) {
    let iter = fn(arr, result) {
        if (len(arr) == 0) { result } else {
            iter(rest(arr), f(result, first(arr)));
        }
    };
    iter(arr, initial);
};
```

### 4.5 - Hashes

**Lexer**: New token `token.COLON` (`:`).

**Parser**: `ast.HashLiteral` contains `Pairs map[Expression]Expression`. Parsing uses `parseExpressionList` patterns to handle comma-separated key-value pairs.

**Object System -- The Hashing Problem**: A naive `map[Object]Object` does not work because Go compares pointers, not values. Two separate `*object.String{Value: "name"}` instances have different pointers.

The solution is `HashKey`:

```go
type HashKey struct {
    Type  ObjectType
    Value uint64
}
```

Each hashable type implements `HashKey() HashKey`:
- `Boolean`: Uses 1 for true, 0 for false
- `Integer`: Uses the integer value cast to `uint64`
- `String`: Uses FNV-1a hash of the string bytes

The `Hashable` interface defines which types can be hash keys. The `object.Hash` struct uses `map[HashKey]HashPair` where `HashPair` stores both the original key and value objects (for `Inspect()` output).

**Evaluator**: `evalHashLiteral` evaluates each key and value, checks that keys implement `Hashable`, generates `HashKey`s, and builds the pairs map. `evalHashIndexExpression` looks up values by generating a `HashKey` from the index expression.

```
>> let people = [{"name": "Alice", "age": 24}, {"name": "Anna", "age": 28}];
>> people[0]["name"];
Alice
>> let getName = fn(person) { person["name"]; };
>> getName(people[1]);
Anna
```

### 4.6 - The Grand Finale

The last built-in function is `puts`, which prints each argument on a new line and returns `NULL`:

```go
"puts": &object.Builtin{
    Fn: func(args ...object.Object) object.Object {
        for _, arg := range args {
            fmt.Println(arg.Inspect())
        }
        return NULL
    },
},
```

With `puts`, the interpreter can finally communicate with the outside world:

```
>> puts("Hello World!")
Hello World!
null
```

---

## Going Further

### The Lost Chapter

A free supplementary chapter covers implementing a macro system for Monkey, available at `interpreterbook.com/lost`.

### Writing A Compiler In Go

The sequel book replaces the tree-walking evaluator with a bytecode compiler and virtual machine, making Monkey approximately three times faster. Available at `compilerbook.com`.

---

## Key Takeaways

1. **Interpreters have three main stages**: lexing (source code to tokens), parsing (tokens to AST), and evaluation (AST to values). Each stage has a clear input/output contract.

2. **Pratt parsing is elegant for expressions**: By associating parsing functions with token types (prefix and infix) and using precedence levels, complex expression parsing becomes a simple, extensible loop. The `precedence < peekPrecedence()` condition is the key mechanism that handles operator associativity and precedence.

3. **The object system is the bridge**: Every value in the interpreted language must be represented as an object in the host language. The choice of representation affects correctness, performance, and implementation complexity.

4. **Environments enable closures**: By having each function carry its defining environment and creating enclosed environments for function calls, lexical scoping and closures work naturally. The environment chain (inner to outer) mirrors the scope chain.

5. **Return values and errors need special propagation**: `object.ReturnValue` wraps values to signal early exit from blocks. `object.Error` propagates through the evaluation chain. Both must be checked at every level to work correctly across nested blocks and function calls.

6. **Test-driven development shines for interpreters**: Each component (lexer, parser, evaluator) is built test-first. The extensive test suite catches off-by-one errors in token advancement, incorrect AST nesting, and wrong evaluation semantics. The `String()` methods on AST nodes enable powerful round-trip testing.

7. **Immutable data structures simplify reasoning**: Arrays in Monkey are immutable (`push` returns a new array). This prevents aliasing bugs and makes the interpreter easier to reason about, even if less efficient.

8. **Hash keys require careful design**: Using object pointers as hash keys fails because equivalent values at different memory locations are not equal. The solution is a `HashKey` type that combines the object type with a computed hash, enabling correct lookups regardless of object identity.

9. **The REPL is a powerful development tool**: Building the REPL incrementally (first lexing, then parsing, then evaluating) provides immediate feedback at each stage and makes the interpreter feel alive as it grows.

10. **Architecture matters more than performance**: The tree-walking approach is the slowest interpreter design, but it is the simplest to understand, build, and extend. Starting simple and optimizing later (as done in the sequel with bytecode compilation) is a proven strategy used by real-world languages like Ruby.

---

*Book by Thorsten Ball. Summary generated from the complete text.*
