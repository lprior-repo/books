# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# Writing An Interpreter In Go
**Author:** Thorsten Ball
**Topic tags:** `#general` `#go` `#compiler` `#parser`
**Language focus:** Go-first
**Sources:** `markdown_output/Writing_an_Interpreter_In_Go_-_Thorsten_Ball/Writing_an_Interpreter_In_Go_-_Thorsten_Ball.md` · `summaries/Writing_an_Interpreter_In_Go_-_Thorsten_Ball.md`

## TL;DR
A line-by-line, test-driven walkthrough for building a complete tree-walking interpreter ("Monkey") in Go from scratch — no third-party libraries. It covers every stage: hand-written lexer, recursive-descent / Pratt parser, AST design, object system, environment-based scoping, error propagation, and built-in data types (strings, arrays, hashes). Apply it whenever you need to build a parser, DSL, expression evaluator, or understand how language runtimes work; it is the canonical "from zero to interpreter" reference for Go.

---

## Best Practices by Topic

### 1. The Three-Stage Interpreter Pipeline `#general` `#compiler`

**Principle:** Source code is transformed twice before evaluation: source → tokens (lexer), tokens → AST (parser), AST → values (evaluator). Each stage has a clear contract, an input type, and an output type.

**Do:**
- Keep each stage independent and testable.
- Use distinct types (`token.Token`, `ast.Node`, `object.Object`) so the compiler catches cross-stage mistakes.
- Grow the interpreter by extending every stage in lockstep: token → lexer → AST node → parser registration → object type → evaluator branch.

**Don't:**
- Combine stages — e.g., evaluating during parsing destroys error recovery and test isolation.
- Skip a layer: building the AST during lexing makes future extensions painful.

---

## Chapter 1 — Lexing `#compiler` `#go`

### 2. Token Type & Struct Design

**Principle:** Define tokens as a `TokenType` string alias plus a `Token` struct that carries a type and the literal source text. Strings make debugging trivial.

**Do:**
- Use a `string`-backed `TokenType` so tokens print usefully without helpers.
- Define an `ILLEGAL` token (unknown character) and an `EOF` token (end of input).
- Distinguish keywords from identifiers with a `keywords` map plus a `LookupIdent` function.

**Don't:**
- Use `int`/`byte` for `TokenType` for "performance" before you need it — debuggability wins.

**Code:**
```go
// token/token.go
package token

type TokenType string

type Token struct {
	Type    TokenType
	Literal string
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.2 - Defining Our Tokens"*

```go
// token/token.go
const (
	ILLEGAL = "ILLEGAL"
	EOF     = "EOF"

	// Identifiers + literals
	IDENT = "IDENT" // add, foobar, x, y, ...
	INT   = "INT"   // 1343456

	// Operators
	ASSIGN = "="
	PLUS   = "+"

	// Delimiters
	COMMA     = ","
	SEMICOLON = ";"
	LPAREN    = "("
	RPAREN    = ")"
	LBRACE    = "{"
	RBRACE    = "}"

	// Keywords
	FUNCTION = "FUNCTION"
	LET      = "LET"
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.2 - Defining Our Tokens"*

```go
// token/token.go
var keywords = map[string]TokenType{
	"fn":  FUNCTION,
	"let": LET,
}

func LookupIdent(ident string) TokenType {
	if tok, ok := keywords[ident]; ok {
		return tok
	}
	return IDENT
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

### 3. Two-Pointer Lexer State

**Principle:** Track position with two pointers — `position` (current char) and `readPosition` (next char) — so you can always peek one character ahead without advancing.

**Do:**
- Initialize the lexer by calling `readChar()` once in `New` so `ch`, `position`, and `readPosition` are valid before the first `NextToken()`.
- Use `ch == 0` (NUL) to signal "nothing read yet" or "end of input".

**Don't:**
- Use a single pointer — you'll be unable to lookahead for two-character tokens like `==`.

**Code:**
```go
// lexer/lexer.go
package lexer

type Lexer struct {
	input        string
	position     int  // current position in input (points to current char)
	readPosition int  // current reading position in input (after current char)
	ch           byte // current char under examination
}

func New(input string) *Lexer {
	l := &Lexer{input: input}
	l.readChar()
	return l
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) readChar() {
	if l.readPosition >= len(l.input) {
		l.ch = 0
	} else {
		l.ch = l.input[l.readPosition]
	}
	l.position = l.readPosition
	l.readPosition += 1
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

### 4. Lexer Test-First with a Token Stream

**Principle:** Drive lexer development with a single table-driven test that walks an entire snippet and asserts every emitted token type and literal. The input can be gibberish — the lexer's job is tokenization, not validity.

**Do:**
- Cover all token categories plus edge cases (EOF, multi-digit numbers, whitespace, newlines).
- Keep one big `tests` slice; extend it as tokens are added.

**Code:**
```go
// lexer/lexer_test.go
package lexer

import (
	"testing"
	"monkey/token"
)

func TestNextToken(t *testing.T) {
	input := `=+(){},;`
	tests := []struct {
		expectedType    token.TokenType
		expectedLiteral string
	}{
		{token.ASSIGN, "="},
		{token.PLUS, "+"},
		{token.LPAREN, "("},
		{token.RPAREN, ")"},
		{token.LBRACE, "{"},
		{token.RBRACE, "}"},
		{token.COMMA, ","},
		{token.SEMICOLON, ";"},
		{token.EOF, ""},
	}
	l := New(input)
	for i, tt := range tests {
		tok := l.NextToken()
		if tok.Type != tt.expectedType {
			t.Fatalf("tests[%d] - tokentype wrong. expected=%q, got=%q",
				i, tt.expectedType, tok.Type)
		}
		if tok.Literal != tt.expectedLiteral {
			t.Fatalf("tests[%d] - literal wrong. expected=%q, got=%q",
				i, tt.expectedLiteral, tok.Literal)
		}
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

### 5. Switch-Driven NextToken with Default Branch

**Principle:** `NextToken()` is a big `switch l.ch` that maps each known character to a token. Unknown characters fall through to a `default` that distinguishes letters (identifiers/keywords) and digits (integers) from genuinely illegal input.

**Do:**
- Return early from `readIdentifier` / `readNumber` — they already advance `position` past the literal, so the trailing `readChar()` would skip a character.
- Always `skipWhitespace()` at the top of `NextToken()` so whitespace acts purely as a separator.

**Don't:**
- Forget to call `readChar()` after producing a one-character token — the lexer's pointers won't advance.

**Code:**
```go
// lexer/lexer.go
package lexer

import "monkey/token"

func (l *Lexer) NextToken() token.Token {
	var tok token.Token
	switch l.ch {
	case '=':
		tok = newToken(token.ASSIGN, l.ch)
	case ';':
		tok = newToken(token.SEMICOLON, l.ch)
	case '(':
		tok = newToken(token.LPAREN, l.ch)
	case ')':
		tok = newToken(token.RPAREN, l.ch)
	case ',':
		tok = newToken(token.COMMA, l.ch)
	case '+':
		tok = newToken(token.PLUS, l.ch)
	case '{':
		tok = newToken(token.LBRACE, l.ch)
	case '}':
		tok = newToken(token.RBRACE, l.ch)
	case 0:
		tok.Literal = ""
		tok.Type = token.EOF
	}
	l.readChar()
	return tok
}

func newToken(tokenType token.TokenType, ch byte) token.Token {
	return token.Token{Type: tokenType, Literal: string(ch)}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

### 6. Reading Identifiers, Numbers, and Skipping Whitespace

**Principle:** Treat `_` as a letter so identifiers like `foo_bar` work. `readNumber` mirrors `readIdentifier`. `isLetter` / `isDigit` are tiny predicate functions that effectively define the language's lexical grammar.

**Do:**
- Localize all "what counts as an identifier character" decisions in `isLetter` so language extensions (e.g., allowing `?` or `!` in identifiers) live in one place.

**Code:**
```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	var tok token.Token
	l.skipWhitespace()
	switch l.ch {
	// [...]
	default:
		if isLetter(l.ch) {
			tok.Literal = l.readIdentifier()
			tok.Type = token.LookupIdent(tok.Literal)
			return tok
		} else if isDigit(l.ch) {
			tok.Type = token.INT
			tok.Literal = l.readNumber()
			return tok
		} else {
			tok = newToken(token.ILLEGAL, l.ch)
		}
	}
	// [...]
}

func (l *Lexer) readIdentifier() string {
	position := l.position
	for isLetter(l.ch) {
		l.readChar()
	}
	return l.input[position:l.position]
}

func isLetter(ch byte) bool {
	return 'a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || ch == '_'
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) skipWhitespace() {
	for l.ch == ' ' || l.ch == '\t' || l.ch == '\n' || l.ch == '\r' {
		l.readChar()
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) readNumber() string {
	position := l.position
	for isDigit(l.ch) {
		l.readChar()
	}
	return l.input[position:l.position]
}

func isDigit(ch byte) bool {
	return '0' <= ch && ch <= '9'
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.3 - The Lexer"*

### 7. Extending the Token Set — New Operators & Keywords

**Principle:** Adding one-character tokens (`-`, `!`, `*`, `/`, `<`, `>`) and keywords (`true`, `false`, `if`, `else`, `return`) is mechanical: define the constant, add a switch case or extend the `keywords` map. The pattern is the lexer's greatest strength — it scales linearly with the language.

**Code:**
```go
// token/token.go
const (
	// [...]
	// Operators
	ASSIGN   = "="
	PLUS     = "+"
	MINUS    = "-"
	BANG     = "!"
	ASTERISK = "*"
	SLASH    = "/"

	LT = "<"
	GT = ">"
	// [...]
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

```go
// token/token.go
const (
	// [...]
	// Keywords
	FUNCTION = "FUNCTION"
	LET      = "LET"
	TRUE     = "TRUE"
	FALSE    = "FALSE"
	IF       = "IF"
	ELSE     = "ELSE"
	RETURN   = "RETURN"
)

var keywords = map[string]TokenType{
	"fn":     FUNCTION,
	"let":    LET,
	"true":   TRUE,
	"false":  FALSE,
	"if":     IF,
	"else":   ELSE,
	"return": RETURN,
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	// [...]
	switch l.ch {
	case '=':
		tok = newToken(token.ASSIGN, l.ch)
	case '+':
		tok = newToken(token.PLUS, l.ch)
	case '-':
		tok = newToken(token.MINUS, l.ch)
	case '!':
		tok = newToken(token.BANG, l.ch)
	case '/':
		tok = newToken(token.SLASH, l.ch)
	case '*':
		tok = newToken(token.ASTERISK, l.ch)
	case '<':
		tok = newToken(token.LT, l.ch)
	case '>':
		tok = newToken(token.GT, l.ch)
	case ';':
		tok = newToken(token.SEMICOLON, l.ch)
	case ',':
		tok = newToken(token.COMMA, l.ch)
	// [...]
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

### 8. Two-Character Tokens via peekChar

**Principle:** Two-character tokens (`==`, `!=`) require looking ahead without consuming. `peekChar()` returns the next char without advancing; the `=` / `!` branches check it before deciding which token to emit. Always save `l.ch` in a local before calling `readChar()` so the literal is reconstructable.

**Do:**
- Generalize with a `makeTwoCharToken` helper if more two-character operators appear.

**Code:**
```go
// lexer/lexer.go
func (l *Lexer) peekChar() byte {
	if l.readPosition >= len(l.input) {
		return 0
	} else {
		return l.input[l.readPosition]
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

```go
// token/token.go
const (
	// [...]
	EQ     = "=="
	NOT_EQ = "!="
	// [...]
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	// [...]
	switch l.ch {
	case '=':
		if l.peekChar() == '=' {
			ch := l.ch
			l.readChar()
			literal := string(ch) + string(l.ch)
			tok = token.Token{Type: token.EQ, Literal: literal}
		} else {
			tok = newToken(token.ASSIGN, l.ch)
		}
	case '!':
		if l.peekChar() == '=' {
			ch := l.ch
			l.readChar()
			literal := string(ch) + string(l.ch)
			tok = token.Token{Type: token.NOT_EQ, Literal: literal}
		} else {
			tok = newToken(token.BANG, l.ch)
		}
	// [...]
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.4 - Extending our Token Set and Lexer"*

### 9. The REPL Bootstrap `#general`

**Principle:** Build the REPL early, even if it only prints tokens. It grows incrementally with each stage (lex → parse → eval) and provides immediate feedback that the interpreter is alive.

**Do:**
- Pass `io.Reader`/`io.Writer` so the REPL is testable and embeddable.
- Persist a single `*object.Environment` across lines so bindings survive between inputs.

**Don't:**
- Forget to greet the user with a friendly prompt — it sets the tone.

**Code:**
```go
// repl/repl.go
package repl

import (
	"bufio"
	"fmt"
	"io"
	"monkey/lexer"
	"monkey/token"
)

const PROMPT = ">> "

func Start(in io.Reader, out io.Writer) {
	scanner := bufio.NewScanner(in)
	for {
		fmt.Fprintf(out, PROMPT)
		scanned := scanner.Scan()
		if !scanned {
			return
		}
		line := scanner.Text()
		l := lexer.New(line)
		for tok := l.NextToken(); tok.Type != token.EOF; tok = l.NextToken() {
			fmt.Fprintf(out, "%+v\n", tok)
		}
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.5 - Start of a REPL"*

```go
// main.go
package main

import (
	"fmt"
	"os"
	"os/user"
	"monkey/repl"
)

func main() {
	user, err := user.Current()
	if err != nil {
		panic(err)
	}
	fmt.Printf("Hello %s! This is the Monkey programming language!\n",
		user.Username)
	fmt.Printf("Feel free to type in commands\n")
	repl.Start(os.Stdin, os.Stdout)
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "1.5 - Start of a REPL"*

---

## Chapter 2 — Parsing `#parser` `#go`

### 10. AST Interfaces: Node / Statement / Expression

**Principle:** Define a small interface hierarchy — `Node` (with `TokenLiteral()` and `String()`), `Statement`, and `Expression` (each adds a dummy marker method). The marker methods (`statementNode()`, `expressionNode()`) let the Go compiler reject a Statement where an Expression is required.

**Do:**
- Implement `String()` on every node so you can round-trip the AST back to source — invaluable for parser tests.
- Make `Program` itself a `Node` that holds `[]Statement`.

**Don't:**
- Use a single concrete struct type for all nodes — you'll lose type safety and pattern matching.

**Code:**
```go
// ast/ast.go
package ast

type Node interface {
	TokenLiteral() string
	String() string
}

type Statement interface {
	Node
	statementNode()
}

type Expression interface {
	Node
	expressionNode()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 - Parser's first steps: parsing let statements"*

```go
// ast/ast.go
type Program struct {
	Statements []Statement
}

func (p *Program) TokenLiteral() string {
	if len(p.Statements) > 0 {
		return p.Statements[0].TokenLiteral()
	} else {
		return ""
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 - Parser's first steps: parsing let statements"*

```go
// ast/ast.go
import (
	"bytes"
)

func (p *Program) String() string {
	var out bytes.Buffer
	for _, s := range p.Statements {
		out.WriteString(s.String())
	}
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Parsing Expressions / Preparing the AST"*

### 11. LetStatement and Identifier Nodes

**Principle:** A `LetStatement` holds `Name *Identifier` and `Value Expression`. `Identifier` is an `Expression` (so it can be reused in expression position later) even though as a binding name it doesn't produce a value — this keeps the node set small.

**Code:**
```go
// ast/ast.go
import "monkey/token"

type LetStatement struct {
	Token token.Token // the token.LET token
	Name  *Identifier
	Value Expression
}

func (ls *LetStatement) statementNode()       {}
func (ls *LetStatement) TokenLiteral() string { return ls.Token.Literal }

type Identifier struct {
	Token token.Token // the token.IDENT token
	Value string
}

func (i *Identifier) expressionNode()      {}
func (i *Identifier) TokenLiteral() string { return i.Token.Literal }
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 - Parser's first steps: parsing let statements"*

```go
// ast/ast.go
func (ls *LetStatement) String() string {
	var out bytes.Buffer
	out.WriteString(ls.TokenLiteral() + " ")
	out.WriteString(ls.Name.String())
	out.WriteString(" = ")
	if ls.Value != nil {
		out.WriteString(ls.Value.String())
	}
	out.WriteString(";")
	return out.String()
}

func (i *Identifier) String() string { return i.Value }
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Parsing Expressions / Preparing the AST"*

### 12. Parser State: curToken / peekToken

**Principle:** Mirror the lexer's two-pointer design at the token level — `curToken` is what we're deciding on, `peekToken` lets us look one token ahead. Bootstrap by calling `nextToken()` twice in `New` so both fields are populated.

**Do:**
- Keep `errors []string` so the parser can report every parse error in one pass, not just the first.

**Don't:**
- Stop on the first parse error — users hate rerunning to find the next mistake.

**Code:**
```go
// parser/parser.go
package parser

import (
	"monkey/ast"
	"monkey/lexer"
	"monkey/token"
)

type Parser struct {
	l      *lexer.Lexer
	errors []string
	curToken  token.Token
	peekToken token.Token
	prefixParseFns map[token.TokenType]prefixParseFn
	infixParseFns  map[token.TokenType]infixParseFn
}

func New(l *lexer.Lexer) *Parser {
	p := &Parser{
		l:      l,
		errors: []string{},
	}
	// Read two tokens, so curToken and peekToken are both set
	p.nextToken()
	p.nextToken()
	return p
}

func (p *Parser) nextToken() {
	p.curToken = p.peekToken
	p.peekToken = p.l.NextToken()
}

func (p *Parser) ParseProgram() *ast.Program {
	program := &ast.Program{}
	program.Statements = []ast.Statement{}
	for !p.curTokenIs(token.EOF) {
		stmt := p.parseStatement()
		if stmt != nil {
			program.Statements = append(program.Statements, stmt)
		}
		p.nextToken()
	}
	return program
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.3 / 2.4 - Writing a Parser"*

### 13. Statement Dispatch & Assertion Helpers

**Principle:** `parseStatement()` switches on `curToken.Type`. `expectPeek(t)` is the workhorse assertion: if the next token matches, advance and return true; otherwise record an error. Always provide `curTokenIs`, `peekTokenIs`, and an `Errors()` accessor.

**Code:**
```go
// parser/parser.go
func (p *Parser) parseStatement() ast.Statement {
	switch p.curToken.Type {
	case token.LET:
		return p.parseLetStatement()
	case token.RETURN:
		return p.parseReturnStatement()
	default:
		return p.parseExpressionStatement()
	}
}

func (p *Parser) parseLetStatement() *ast.LetStatement {
	stmt := &ast.LetStatement{Token: p.curToken}
	if !p.expectPeek(token.IDENT) {
		return nil
	}
	stmt.Name = &ast.Identifier{Token: p.curToken, Value: p.curToken.Literal}
	if !p.expectPeek(token.ASSIGN) {
		return nil
	}
	p.nextToken()
	stmt.Value = p.parseExpression(LOWEST)
	if p.peekTokenIs(token.SEMICOLON) {
		p.nextToken()
	}
	return stmt
}

func (p *Parser) curTokenIs(t token.TokenType) bool {
	return p.curToken.Type == t
}

func (p *Parser) peekTokenIs(t token.TokenType) bool {
	return p.peekToken.Type == t
}

func (p *Parser) expectPeek(t token.TokenType) bool {
	if p.peekTokenIs(t) {
		p.nextToken()
		return true
	} else {
		p.peekError(t)
		return false
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 / 2.5 / Removing TODOs"*

```go
// parser/parser.go
import (
	// [...]
	"fmt"
)

func (p *Parser) Errors() []string { return p.errors }

func (p *Parser) peekError(t token.TokenType) {
	msg := fmt.Sprintf("expected next token to be %s, got %s instead",
		t, p.peekToken.Type)
	p.errors = append(p.errors, msg)
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 - Parser's first steps"*

### 14. ReturnStatement & ExpressionStatement

**Principle:** `ReturnStatement` mirrors `LetStatement` minus the name. `ExpressionStatement` is a thin wrapper letting any expression stand alone as a statement (so `5 + 5;` is legal).

**Code:**
```go
// ast/ast.go
type ReturnStatement struct {
	Token       token.Token // the 'return' token
	ReturnValue Expression
}

func (rs *ReturnStatement) statementNode()       {}
func (rs *ReturnStatement) TokenLiteral() string { return rs.Token.Literal }

func (rs *ReturnStatement) String() string {
	var out bytes.Buffer
	out.WriteString(rs.TokenLiteral() + " ")
	if rs.ReturnValue != nil {
		out.WriteString(rs.ReturnValue.String())
	}
	out.WriteString(";")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.5 - Parsing Return Statements"*

```go
// ast/ast.go
type ExpressionStatement struct {
	Token      token.Token // the first token of the expression
	Expression Expression
}

func (es *ExpressionStatement) statementNode()       {}
func (es *ExpressionStatement) TokenLiteral() string { return es.Token.Literal }

func (es *ExpressionStatement) String() string {
	if es.Expression != nil {
		return es.Expression.String()
	}
	return ""
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Preparing the AST"*

```go
// parser/parser.go
func (p *Parser) parseReturnStatement() *ast.ReturnStatement {
	stmt := &ast.ReturnStatement{Token: p.curToken}
	p.nextToken()
	stmt.ReturnValue = p.parseExpression(LOWEST)
	if p.peekTokenIs(token.SEMICOLON) {
		p.nextToken()
	}
	return stmt
}

func (p *Parser) parseExpressionStatement() *ast.ExpressionStatement {
	stmt := &ast.ExpressionStatement{Token: p.curToken}
	stmt.Expression = p.parseExpression(LOWEST)
	if p.peekTokenIs(token.SEMICOLON) {
		p.nextToken()
	}
	return stmt
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.5 / 2.6 - Return Statements / Parsing Expressions"*

### 15. Pratt Parser — Prefix & Infix Function Maps

**Principle:** Vaughan Pratt's top-down operator precedence parsing attaches parse functions to token types, not grammar rules. Each token can have a `prefixParseFn` (called when the token is in prefix position, e.g. `-5`) and an `infixParseFn` (called when in infix position, e.g. `5 + 5`). Two maps enable the central `parseExpression` loop.

**Do:**
- Register all prefix/infix handlers in `New()` so the table is always complete.
- Add a `noPrefixParseFnError` so a missing handler is an explicit, debuggable error instead of silent `nil`.

**Code:**
```go
// parser/parser.go
type (
	prefixParseFn func() ast.Expression
	infixParseFn  func(ast.Expression) ast.Expression
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Implementing the Pratt Parser"*

```go
// parser/parser.go
func (p *Parser) registerPrefix(tokenType token.TokenType, fn prefixParseFn) {
	p.prefixParseFns[tokenType] = fn
}

func (p *Parser) registerInfix(tokenType token.TokenType, fn infixParseFn) {
	p.infixParseFns[tokenType] = fn
}

func (p *Parser) noPrefixParseFnError(t token.TokenType) {
	msg := fmt.Sprintf("no prefix parse function for %s found", t)
	p.errors = append(p.errors, msg)
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Implementing the Pratt Parser"*

### 16. Precedence Constants and Lookup Table

**Principle:** Use `iota` to define ordered precedence levels — the order matters, the absolute numbers do not. A `precedences` map ties token types to their left-binding power. `peekPrecedence` and `curPrecedence` look these up with `LOWEST` as the default.

**Do:**
- Make `INDEX` (the array/hash subscript operator) the highest precedence.
- Default unknown tokens to `LOWEST` so they naturally terminate expression parsing.

**Code:**
```go
// parser/parser.go
const (
	_ int = iota
	LOWEST
	EQUALS      // ==
	LESSGREATER // > or <
	SUM         // +
	PRODUCT     // *
	PREFIX      // -X or !X
	CALL        // myFunction(X)
	INDEX       // array[index]
)

var precedences = map[token.TokenType]int{
	token.EQ:       EQUALS,
	token.NOT_EQ:   EQUALS,
	token.LT:       LESSGREATER,
	token.GT:       LESSGREATER,
	token.PLUS:     SUM,
	token.MINUS:    SUM,
	token.SLASH:    PRODUCT,
	token.ASTERISK: PRODUCT,
	token.LPAREN:   CALL,
	token.LBRACKET: INDEX,
}

func (p *Parser) peekPrecedence() int {
	if p, ok := precedences[p.peekToken.Type]; ok {
		return p
	}
	return LOWEST
}

func (p *Parser) curPrecedence() int {
	if p, ok := precedences[p.curToken.Type]; ok {
		return p
	}
	return LOWEST
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Infix Operators" and "2.8 - Call Expressions"*

### 17. The Heart of Pratt Parsing — parseExpression

**Principle:** The complete `parseExpression(precedence)` is short but does it all: invoke the prefix parser for the current token, then loop while the next token has higher precedence than the caller's `precedence`, calling infix parsers to fold in operators. The condition `precedence < peekPrecedence()` is what handles associativity and parenthesization.

**Do:**
- Stop the loop early on `SEMICOLON` to make expression terminators explicit.
- Pass the saved operator precedence (not `LOWEST`) to the recursive call when parsing the right side of an infix operator — that is what gives left-associativity.

**Code:**
```go
// parser/parser.go
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
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Infix Operators"*

### 18. Parsing Identifiers, Integers, Booleans

**Principle:** Literal parsers share a protocol: start with `curToken` of the right type, do not advance past the last token of the expression. For integers, convert the literal with `strconv.ParseInt` and record a parser error on failure.

**Code:**
```go
// parser/parser.go
import (
	// [...]
	"strconv"
)

func (p *Parser) parseIdentifier() ast.Expression {
	return &ast.Identifier{Token: p.curToken, Value: p.curToken.Literal}
}

func (p *Parser) parseIntegerLiteral() ast.Expression {
	lit := &ast.IntegerLiteral{Token: p.curToken}
	value, err := strconv.ParseInt(p.curToken.Literal, 0, 64)
	if err != nil {
		msg := fmt.Sprintf("could not parse %q as integer", p.curToken.Literal)
		p.errors = append(p.errors, msg)
		return nil
	}
	lit.Value = value
	return lit
}

func (p *Parser) parseBoolean() ast.Expression {
	return &ast.Boolean{Token: p.curToken, Value: p.curTokenIs(token.TRUE)}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 / 2.8 - Identifiers / Integer Literals / Boolean Literals"*

```go
// ast/ast.go
type IntegerLiteral struct {
	Token token.Token
	Value int64
}

func (il *IntegerLiteral) expressionNode()      {}
func (il *IntegerLiteral) TokenLiteral() string { return il.Token.Literal }
func (il *IntegerLiteral) String() string       { return il.Token.Literal }

type Boolean struct {
	Token token.Token
	Value bool
}

func (b *Boolean) expressionNode()      {}
func (b *Boolean) TokenLiteral() string { return b.Token.Literal }
func (b *Boolean) String() string       { return b.Token.Literal }
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 / 2.8 - Integer Literals / Boolean Literals"*

### 19. Prefix & Infix Expression Nodes

**Principle:** `PrefixExpression` has `Operator` and `Right`. `InfixExpression` adds `Left`. Both `String()` methods emit parentheses so the resulting AST string exposes precedence and associativity — perfect for table-driven tests.

**Code:**
```go
// ast/ast.go
type PrefixExpression struct {
	Token    token.Token // The prefix token, e.g. !
	Operator string
	Right    Expression
}

func (pe *PrefixExpression) expressionNode()      {}
func (pe *PrefixExpression) TokenLiteral() string { return pe.Token.Literal }

func (pe *PrefixExpression) String() string {
	var out bytes.Buffer
	out.WriteString("(")
	out.WriteString(pe.Operator)
	out.WriteString(pe.Right.String())
	out.WriteString(")")
	return out.String()
}

type InfixExpression struct {
	Token    token.Token // The operator token, e.g. +
	Left     Expression
	Operator string
	Right    Expression
}

func (ie *InfixExpression) expressionNode()      {}
func (ie *InfixExpression) TokenLiteral() string { return ie.Token.Literal }

func (ie *InfixExpression) String() string {
	var out bytes.Buffer
	out.WriteString("(")
	out.WriteString(ie.Left.String())
	out.WriteString(" " + ie.Operator + " ")
	out.WriteString(ie.Right.String())
	out.WriteString(")")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Prefix Operators / Infix Operators"*

```go
// parser/parser.go
func (p *Parser) parsePrefixExpression() ast.Expression {
	expression := &ast.PrefixExpression{
		Token:    p.curToken,
		Operator: p.curToken.Literal,
	}
	p.nextToken()
	expression.Right = p.parseExpression(PREFIX)
	return expression
}

func (p *Parser) parseInfixExpression(left ast.Expression) ast.Expression {
	expression := &ast.InfixExpression{
		Token:    p.curToken,
		Operator: p.curToken.Literal,
		Left:     left,
	}
	precedence := p.curPrecedence()
	p.nextToken()
	expression.Right = p.parseExpression(precedence)
	return expression
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 - Prefix Operators / Infix Operators"*

### 20. Registering All Parse Functions in New()

**Principle:** Wire up the entire prefix/infix table once in `New()`. This is the parser's most-edited function — every new expression type adds one or two lines.

**Code:**
```go
// parser/parser.go
func New(l *lexer.Lexer) *Parser {
	p := &Parser{
		l:      l,
		errors: []string{},
	}
	p.prefixParseFns = make(map[token.TokenType]prefixParseFn)
	p.infixParseFns = make(map[token.TokenType]infixParseFn)

	p.registerPrefix(token.IDENT, p.parseIdentifier)
	p.registerPrefix(token.INT, p.parseIntegerLiteral)
	p.registerPrefix(token.BANG, p.parsePrefixExpression)
	p.registerPrefix(token.MINUS, p.parsePrefixExpression)
	p.registerPrefix(token.TRUE, p.parseBoolean)
	p.registerPrefix(token.FALSE, p.parseBoolean)
	p.registerPrefix(token.LPAREN, p.parseGroupedExpression)
	p.registerPrefix(token.IF, p.parseIfExpression)
	p.registerPrefix(token.FUNCTION, p.parseFunctionLiteral)
	p.registerPrefix(token.STRING, p.parseStringLiteral)
	p.registerPrefix(token.LBRACKET, p.parseArrayLiteral)
	p.registerPrefix(token.LBRACE, p.parseHashLiteral)

	p.registerInfix(token.PLUS, p.parseInfixExpression)
	p.registerInfix(token.MINUS, p.parseInfixExpression)
	p.registerInfix(token.SLASH, p.parseInfixExpression)
	p.registerInfix(token.ASTERISK, p.parseInfixExpression)
	p.registerInfix(token.EQ, p.parseInfixExpression)
	p.registerInfix(token.NOT_EQ, p.parseInfixExpression)
	p.registerInfix(token.LT, p.parseInfixExpression)
	p.registerInfix(token.GT, p.parseInfixExpression)
	p.registerInfix(token.LPAREN, p.parseCallExpression)
	p.registerInfix(token.LBRACKET, p.parseIndexExpression)

	p.nextToken()
	p.nextToken()
	return p
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "Synthesis of all parser registrations across chapter 2 and 4"*

### 21. Test Helpers for AST Assertion

**Principle:** Reduce boilerplate with `testIntegerLiteral`, `testIdentifier`, `testBooleanLiteral`, and a polymorphic `testLiteralExpression` / `testInfixExpression` that switch on the Go type of the expected value. These turn multi-line assertions into one-liners.

**Code:**
```go
// parser/parser_test.go
import (
	// [...]
	"fmt"
)

func testIntegerLiteral(t *testing.T, il ast.Expression, value int64) bool {
	integ, ok := il.(*ast.IntegerLiteral)
	if !ok {
		t.Errorf("il not *ast.IntegerLiteral. got=%T", il)
		return false
	}
	if integ.Value != value {
		t.Errorf("integ.Value not %d. got=%d", value, integ.Value)
		return false
	}
	if integ.TokenLiteral() != fmt.Sprintf("%d", value) {
		t.Errorf("integ.TokenLiteral not %d. got=%s", value,
			integ.TokenLiteral())
		return false
	}
	return true
}

func testIdentifier(t *testing.T, exp ast.Expression, value string) bool {
	ident, ok := exp.(*ast.Identifier)
	if !ok {
		t.Errorf("exp not *ast.Identifier. got=%T", exp)
		return false
	}
	if ident.Value != value {
		t.Errorf("ident.Value not %s. got=%s", value, ident.Value)
		return false
	}
	if ident.TokenLiteral() != value {
		t.Errorf("ident.TokenLiteral not %s. got=%s", value,
			ident.TokenLiteral())
		return false
	}
	return true
}

func testBooleanLiteral(t *testing.T, exp ast.Expression, value bool) bool {
	bo, ok := exp.(*ast.Boolean)
	if !ok {
		t.Errorf("exp not *ast.Boolean. got=%T", exp)
		return false
	}
	if bo.Value != value {
		t.Errorf("bo.Value not %t. got=%t", value, bo.Value)
		return false
	}
	if bo.TokenLiteral() != fmt.Sprintf("%t", value) {
		t.Errorf("bo.TokenLiteral not %t. got=%s",
			value, bo.TokenLiteral())
		return false
	}
	return true
}

func testLiteralExpression(
	t *testing.T,
	exp ast.Expression,
	expected interface{},
) bool {
	switch v := expected.(type) {
	case int:
		return testIntegerLiteral(t, exp, int64(v))
	case int64:
		return testIntegerLiteral(t, exp, v)
	case string:
		return testIdentifier(t, exp, v)
	case bool:
		return testBooleanLiteral(t, exp, v)
	}
	t.Errorf("type of exp not handled. got=%T", exp)
	return false
}

func testInfixExpression(t *testing.T, exp ast.Expression, left interface{},
	operator string, right interface{}) bool {
	opExp, ok := exp.(*ast.InfixExpression)
	if !ok {
		t.Errorf("exp is not ast.InfixExpression. got=%T(%s)", exp, exp)
		return false
	}
	if !testLiteralExpression(t, opExp.Left, left) {
		return false
	}
	if opExp.Operator != operator {
		t.Errorf("exp.Operator is not '%s'. got=%q", operator, opExp.Operator)
		return false
	}
	if !testLiteralExpression(t, opExp.Right, right) {
		return false
	}
	return true
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Extending the Parser"*

```go
// parser/parser_test.go
func checkParserErrors(t *testing.T, p *Parser) {
	errors := p.Errors()
	if len(errors) == 0 {
		return
	}
	t.Errorf("parser has %d errors", len(errors))
	for _, msg := range errors {
		t.Errorf("parser error: %q", msg)
	}
	t.FailNow()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.4 - Parser's first steps"*

### 22. Operator-Precedence Test Table

**Principle:** Drive precedence correctness by comparing `program.String()` against expected parenthesized strings. This single test catches the vast majority of associativity bugs.

**Code:**
```go
// parser/parser_test.go
func TestOperatorPrecedenceParsing(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"-a * b", "((-a) * b)"},
		{"!-a", "(!(-a))"},
		{"a + b + c", "((a + b) + c)"},
		{"a + b - c", "((a + b) - c)"},
		{"a * b * c", "((a * b) * c)"},
		{"a * b / c", "((a * b) / c)"},
		{"a + b / c", "(a + (b / c))"},
		{"a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"},
		{"3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"},
		{"5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"},
		{"5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"},
		{"3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"},
		{"true", "true"},
		{"false", "false"},
		{"3 > 5 == false", "((3 > 5) == false)"},
		{"3 < 5 == true", "((3 < 5) == true)"},
		{"1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"},
		{"(5 + 5) * 2", "((5 + 5) * 2)"},
		{"2 / (5 + 5)", "(2 / (5 + 5))"},
		{"-(5 + 5)", "(-(5 + 5))"},
		{"!(true == true)", "(!(true == true))"},
		{"a + add(b * c) + d", "((a + add((b * c))) + d)"},
		{"add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
			"add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"},
		{"a * [1, 2, 3, 4][b * c] * d",
			"((a * ([1, 2, 3, 4][(b * c)])) * d)"},
		{"add(a * b[2], b[1], 2 * [1, 2][1])",
			"add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))"},
	}
	for _, tt := range tests {
		l := lexer.New(tt.input)
		p := New(l)
		program := p.ParseProgram()
		checkParserErrors(t, p)
		actual := program.String()
		if actual != tt.expected {
			t.Errorf("expected=%q, got=%q", tt.expected, actual)
		}
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.6 / 2.8 - TestOperatorPrecedenceParsing"*

### 23. Grouped Expressions — The Greatest Trick

**Principle:** Parentheses need no AST node. A `parseGroupedExpression` prefix parser advances past `(`, calls `parseExpression(LOWEST)`, expects `)`, and returns the inner expression. Parenthesization "just works" because the surrounding context's precedence is reset to `LOWEST`.

**Code:**
```go
// parser/parser.go
func (p *Parser) parseGroupedExpression() ast.Expression {
	p.nextToken()
	exp := p.parseExpression(LOWEST)
	if !p.expectPeek(token.RPAREN) {
		return nil
	}
	return exp
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Grouped Expressions"*

### 24. Block Statements & If Expressions

**Principle:** `BlockStatement` holds a series of statements delimited by `{ }`. `IfExpression` has `Condition`, `Consequence`, and an optional `Alternative`. Parse `if`, expect `( <expr> )`, expect `{`, parse a block, optionally consume `else { <block> }`.

**Code:**
```go
// ast/ast.go
type BlockStatement struct {
	Token      token.Token // the { token
	Statements []Statement
}

func (bs *BlockStatement) statementNode()       {}
func (bs *BlockStatement) TokenLiteral() string { return bs.Token.Literal }

func (bs *BlockStatement) String() string {
	var out bytes.Buffer
	for _, s := range bs.Statements {
		out.WriteString(s.String())
	}
	return out.String()
}

type IfExpression struct {
	Token       token.Token // The 'if' token
	Condition   Expression
	Consequence *BlockStatement
	Alternative *BlockStatement
}

func (ie *IfExpression) expressionNode()      {}
func (ie *IfExpression) TokenLiteral() string { return ie.Token.Literal }

func (ie *IfExpression) String() string {
	var out bytes.Buffer
	out.WriteString("if")
	out.WriteString(ie.Condition.String())
	out.WriteString(" ")
	out.WriteString(ie.Consequence.String())
	if ie.Alternative != nil {
		out.WriteString("else ")
		out.WriteString(ie.Alternative.String())
	}
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - If Expressions"*

```go
// parser/parser.go
func (p *Parser) parseIfExpression() ast.Expression {
	expression := &ast.IfExpression{Token: p.curToken}
	if !p.expectPeek(token.LPAREN) {
		return nil
	}
	p.nextToken()
	expression.Condition = p.parseExpression(LOWEST)
	if !p.expectPeek(token.RPAREN) {
		return nil
	}
	if !p.expectPeek(token.LBRACE) {
		return nil
	}
	expression.Consequence = p.parseBlockStatement()
	if p.peekTokenIs(token.ELSE) {
		p.nextToken()
		if !p.expectPeek(token.LBRACE) {
			return nil
		}
		expression.Alternative = p.parseBlockStatement()
	}
	return expression
}

func (p *Parser) parseBlockStatement() *ast.BlockStatement {
	block := &ast.BlockStatement{Token: p.curToken}
	block.Statements = []ast.Statement{}
	p.nextToken()
	for !p.curTokenIs(token.RBRACE) && !p.curTokenIs(token.EOF) {
		stmt := p.parseStatement()
		if stmt != nil {
			block.Statements = append(block.Statements, stmt)
		}
		p.nextToken()
	}
	return block
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - If Expressions"*

### 25. Function Literals & Parameters

**Principle:** `FunctionLiteral` holds `Parameters []*Identifier` and `Body *BlockStatement`. Parse `fn`, expect `(`, parse comma-separated parameters, expect `)`, expect `{`, parse a block. Empty parameter lists and single-parameter lists are both edge cases worth their own tests.

**Code:**
```go
// ast/ast.go
import (
	// [...]
	"strings"
)

type FunctionLiteral struct {
	Token      token.Token // The 'fn' token
	Parameters []*Identifier
	Body       *BlockStatement
}

func (fl *FunctionLiteral) expressionNode()      {}
func (fl *FunctionLiteral) TokenLiteral() string { return fl.Token.Literal }

func (fl *FunctionLiteral) String() string {
	var out bytes.Buffer
	params := []string{}
	for _, p := range fl.Parameters {
		params = append(params, p.String())
	}
	out.WriteString(fl.TokenLiteral())
	out.WriteString("(")
	out.WriteString(strings.Join(params, ", "))
	out.WriteString(") ")
	out.WriteString(fl.Body.String())
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Function Literals"*

```go
// parser/parser.go
func (p *Parser) parseFunctionLiteral() ast.Expression {
	lit := &ast.FunctionLiteral{Token: p.curToken}
	if !p.expectPeek(token.LPAREN) {
		return nil
	}
	lit.Parameters = p.parseFunctionParameters()
	if !p.expectPeek(token.LBRACE) {
		return nil
	}
	lit.Body = p.parseBlockStatement()
	return lit
}

func (p *Parser) parseFunctionParameters() []*ast.Identifier {
	identifiers := []*ast.Identifier{}
	if p.peekTokenIs(token.RPAREN) {
		p.nextToken()
		return identifiers
	}
	p.nextToken()
	ident := &ast.Identifier{Token: p.curToken, Value: p.curToken.Literal}
	identifiers = append(identifiers, ident)
	for p.peekTokenIs(token.COMMA) {
		p.nextToken()
		p.nextToken()
		ident := &ast.Identifier{Token: p.curToken, Value: p.curToken.Literal}
		identifiers = append(identifiers, ident)
	}
	if !p.expectPeek(token.RPAREN) {
		return nil
	}
	return identifiers
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Function Literals"*

### 26. Call Expressions & parseExpressionList

**Principle:** Treat `(` in `add(2, 3)` as an infix operator with the highest non-index precedence (`CALL`). The infix parser receives the already-parsed function expression and then parses the argument list. Generalize argument parsing into `parseExpressionList(end)` so the same code handles array elements.

**Code:**
```go
// ast/ast.go
type CallExpression struct {
	Token     token.Token // The '(' token
	Function  Expression  // Identifier or FunctionLiteral
	Arguments []Expression
}

func (ce *CallExpression) expressionNode()      {}
func (ce *CallExpression) TokenLiteral() string { return ce.Token.Literal }

func (ce *CallExpression) String() string {
	var out bytes.Buffer
	args := []string{}
	for _, a := range ce.Arguments {
		args = append(args, a.String())
	}
	out.WriteString(ce.Function.String())
	out.WriteString("(")
	out.WriteString(strings.Join(args, ", "))
	out.WriteString(")")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Call Expressions"*

```go
// parser/parser.go
func (p *Parser) parseCallExpression(function ast.Expression) ast.Expression {
	exp := &ast.CallExpression{Token: p.curToken, Function: function}
	exp.Arguments = p.parseExpressionList(token.RPAREN)
	return exp
}

func (p *Parser) parseExpressionList(end token.TokenType) []ast.Expression {
	list := []ast.Expression{}
	if p.peekTokenIs(end) {
		p.nextToken()
		return list
	}
	p.nextToken()
	list = append(list, p.parseExpression(LOWEST))
	for p.peekTokenIs(token.COMMA) {
		p.nextToken()
		p.nextToken()
		list = append(list, p.parseExpression(LOWEST))
	}
	if !p.expectPeek(end) {
		return nil
	}
	return list
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.8 - Call Expressions / 4.4 - Parsing Array Literals"*

### 27. Read-Parse-Print-Loop with Friendly Errors

**Principle:** Wire the parser into the REPL. On parse errors, print an ASCII monkey face plus every parser error — friendly UX matters even in toy languages.

**Code:**
```go
// repl/repl.go
import (
	"bufio"
	"fmt"
	"io"
	"monkey/lexer"
	"monkey/parser"
)

func Start(in io.Reader, out io.Writer) {
	scanner := bufio.NewScanner(in)
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
		io.WriteString(out, program.String())
		io.WriteString(out, "\n")
	}
}

const MONKEY_FACE = `            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
`

func printParserErrors(out io.Writer, errors []string) {
	io.WriteString(out, MONKEY_FACE)
	io.WriteString(out, "Woops! We ran into some monkey business here!\n")
	io.WriteString(out, " parser errors:\n")
	for _, msg := range errors {
		io.WriteString(out, "\t"+msg+"\n")
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "2.9 - Read-Parse-Print-Loop"*

---

## Chapter 3 — Evaluation `#general` `#go`

### 28. The object.Object Interface `#general`

**Principle:** Every runtime value is a Go struct that satisfies `Object`. Two methods: `Type() ObjectType` (a string tag) and `Inspect() string` (a printable form). An interface (not a struct) lets each value type use the most efficient representation.

**Code:**
```go
// object/object.go
package object

type ObjectType string

type Object interface {
	Type() ObjectType
	Inspect() string
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.4 - Foundation of our Object System"*

### 29. Integer, Boolean, Null Objects & Singletons

**Principle:** Wrap each primitive in a tiny struct. Use package-level singletons `TRUE`, `FALSE`, `NULL` instead of allocating fresh objects each evaluation — this enables pointer-comparison equality for booleans and saves GC pressure.

**Code:**
```go
// object/object.go
import "fmt"

type Integer struct {
	Value int64
}

func (i *Integer) Inspect() string                              { return fmt.Sprintf("%d", i.Value) }
func (i *Integer) Type() ObjectType                             { return INTEGER_OBJ }

type Boolean struct {
	Value bool
}

func (b *Boolean) Type() ObjectType                             { return BOOLEAN_OBJ }
func (b *Boolean) Inspect() string                              { return fmt.Sprintf("%t", b.Value) }

type Null struct{}

func (n *Null) Type() ObjectType                                { return NULL_OBJ }
func (n *Null) Inspect() string                                 { return "null" }
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.4 - Integers / Booleans / Null"*

```go
// evaluator/evaluator.go
var (
	NULL  = &object.Null{}
	TRUE  = &object.Boolean{Value: true}
	FALSE = &object.Boolean{Value: false}
)

func nativeBoolToBooleanObject(input bool) *object.Boolean {
	if input {
		return TRUE
	}
	return FALSE
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.5 - Boolean Literals / Null"*

### 30. The eval Helper for Tests

**Principle:** Tests share a `testEval` helper that pipes a Monkey source string through lexer → parser → Eval. Each test also gets fresh `*object.Environment` so test order doesn't matter.

**Code:**
```go
// evaluator/evaluator_test.go
package evaluator

import (
	"monkey/lexer"
	"monkey/object"
	"monkey/parser"
	"testing"
)

func testEval(input string) object.Object {
	l := lexer.New(input)
	p := parser.New(l)
	program := p.ParseProgram()
	env := object.NewEnvironment()
	return Eval(program, env)
}

func testIntegerObject(t *testing.T, obj object.Object, expected int64) bool {
	result, ok := obj.(*object.Integer)
	if !ok {
		t.Errorf("object is not Integer. got=%T (%+v)", obj, obj)
		return false
	}
	if result.Value != expected {
		t.Errorf("object has wrong value. got=%d, want=%d",
			result.Value, expected)
		return false
	}
	return true
}

func testBooleanObject(t *testing.T, obj object.Object, expected bool) bool {
	result, ok := obj.(*object.Boolean)
	if !ok {
		t.Errorf("object is not Boolean. got=%T (%+v)", obj, obj)
		return false
	}
	if result.Value != expected {
		t.Errorf("object has wrong value. got=%t, want=%t",
			result.Value, expected)
		return false
	}
	return true
}

func testNullObject(t *testing.T, obj object.Object) bool {
	if obj != NULL {
		t.Errorf("object is not NULL. got=%T (%+v)", obj, obj)
		return false
	}
	return true
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.5 - Evaluating Expressions"*

### 31. The Tree-Walking Eval Function — Skeleton

**Principle:** `Eval` is a recursive type switch over `ast.Node`. Each `case` either recurses (statements, blocks, prefix/infix) or returns a value directly (literals). Keep it a switch — never a giant if/else chain.

**Code:**
```go
// evaluator/evaluator.go
package evaluator

import (
	"monkey/ast"
	"monkey/object"
)

func Eval(node ast.Node, env *object.Environment) object.Object {
	switch node := node.(type) {
	// Statements
	case *ast.Program:
		return evalProgram(node)
	case *ast.ExpressionStatement:
		return Eval(node.Expression, env)
	case *ast.LetStatement:
		val := Eval(node.Value, env)
		if isError(val) {
			return val
		}
		env.Set(node.Name.Value, val)
	case *ast.ReturnStatement:
		val := Eval(node.ReturnValue, env)
		if isError(val) {
			return val
		}
		return &object.ReturnValue{Value: val}
	case *ast.BlockStatement:
		return evalBlockStatement(node)
	// Expressions
	case *ast.IntegerLiteral:
		return &object.Integer{Value: node.Value}
	case *ast.Boolean:
		return nativeBoolToBooleanObject(node.Value)
	case *ast.PrefixExpression:
		right := Eval(node.Right, env)
		if isError(right) {
			return right
		}
		return evalPrefixExpression(node.Operator, right)
	case *ast.InfixExpression:
		left := Eval(node.Left, env)
		if isError(left) {
			return left
		}
		right := Eval(node.Right, env)
		if isError(right) {
			return right
		}
		return evalInfixExpression(node.Operator, left, right)
	case *ast.IfExpression:
		return evalIfExpression(node, env)
	}
	return nil
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.5 / 3.7 / 3.8 / 3.9 - Eval consolidated"*

### 32. evalProgram vs evalBlockStatement — Return Bubbling

**Principle:** Top-level programs and inner block statements need different return semantics. `evalProgram` unwraps `*object.ReturnValue` to its inner value. `evalBlockStatement` does NOT unwrap — it returns the `*object.ReturnValue` so it bubbles up through nested blocks until the outermost program catches it. Without this distinction, a `return` inside a nested `if` would stop too early.

**Code:**
```go
// evaluator/evaluator.go
func evalProgram(program *ast.Program) object.Object {
	var result object.Object
	for _, statement := range program.Statements {
		result = Eval(statement, program.Env)
		switch result := result.(type) {
		case *object.ReturnValue:
			return result.Value
		case *object.Error:
			return result
		}
	}
	return result
}

func evalBlockStatement(block *ast.BlockStatement) object.Object {
	var result object.Object
	for _, statement := range block.Statements {
		result = Eval(statement)
		if result != nil {
			rt := result.Type()
			if rt == object.RETURN_VALUE_OBJ || rt == object.ERROR_OBJ {
				return result
			}
		}
	}
	return result
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.7 - Return Statements"*

### 33. Prefix Operator Evaluation — Truthiness & Negation

**Principle:** `!` flips Monkey's truthiness: `!NULL` and `!false` are true; everything else is false. `-` only works on integers; anything else produces an error.

**Code:**
```go
// evaluator/evaluator.go
func evalPrefixExpression(operator string, right object.Object) object.Object {
	switch operator {
	case "!":
		return evalBangOperatorExpression(right)
	case "-":
		return evalMinusPrefixOperatorExpression(right)
	default:
		return newError("unknown operator: %s%s", operator, right.Type())
	}
}

func evalBangOperatorExpression(right object.Object) object.Object {
	switch right {
	case TRUE:
		return FALSE
	case FALSE:
		return TRUE
	case NULL:
		return TRUE
	default:
		return FALSE
	}
}

func evalMinusPrefixOperatorExpression(right object.Object) object.Object {
	if right.Type() != object.INTEGER_OBJ {
		return newError("unknown operator: -%s", right.Type())
	}
	value := right.(*object.Integer).Value
	return &object.Integer{Value: -value}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.5 - Prefix Expressions"*

### 34. Infix Operator Evaluation — Type Dispatch

**Principle:** Infix evaluation is a type dispatch. Integer+Integer goes to `evalIntegerInfixExpression`; String+String to `evalStringInfixExpression`; equality (`==`, `!=`) between same-typed singletons uses fast pointer comparison. Mismatches produce `type mismatch` errors.

**Code:**
```go
// evaluator/evaluator.go
func evalInfixExpression(
	operator string,
	left, right object.Object,
) object.Object {
	switch {
	case left.Type() == object.INTEGER_OBJ && right.Type() == object.INTEGER_OBJ:
		return evalIntegerInfixExpression(operator, left, right)
	case left.Type() == object.STRING_OBJ && right.Type() == object.STRING_OBJ:
		return evalStringInfixExpression(operator, left, right)
	case operator == "==":
		return nativeBoolToBooleanObject(left == right)
	case operator == "!=":
		return nativeBoolToBooleanObject(left != right)
	case left.Type() != right.Type():
		return newError("type mismatch: %s %s %s",
			left.Type(), operator, right.Type())
	default:
		return newError("unknown operator: %s %s %s",
			left.Type(), operator, right.Type())
	}
}

func evalIntegerInfixExpression(
	operator string,
	left, right object.Object,
) object.Object {
	leftVal := left.(*object.Integer).Value
	rightVal := right.(*object.Integer).Value
	switch operator {
	case "+":
		return &object.Integer{Value: leftVal + rightVal}
	case "-":
		return &object.Integer{Value: leftVal - rightVal}
	case "*":
		return &object.Integer{Value: leftVal * rightVal}
	case "/":
		return &object.Integer{Value: leftVal / rightVal}
	case "<":
		return nativeBoolToBooleanObject(leftVal < rightVal)
	case ">":
		return nativeBoolToBooleanObject(leftVal > rightVal)
	case "==":
		return nativeBoolToBooleanObject(leftVal == rightVal)
	case "!=":
		return nativeBoolToBooleanObject(leftVal != rightVal)
	default:
		return newError("unknown operator: %s %s %s",
			left.Type(), operator, right.Type())
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.5 - Infix Expressions"*

### 35. Conditionals & Truthiness

**Principle:** `evalIfExpression` evaluates the condition, then evaluates the consequence or alternative based on `isTruthy`. Truthiness: everything except `NULL` and `FALSE` is truthy. A missing alternative returns `NULL`.

**Code:**
```go
// evaluator/evaluator.go
func evalIfExpression(ie *ast.IfExpression, env *object.Environment) object.Object {
	condition := Eval(ie.Condition, env)
	if isError(condition) {
		return condition
	}
	if isTruthy(condition) {
		return Eval(ie.Consequence, env)
	} else if ie.Alternative != nil {
		return Eval(ie.Alternative, env)
	} else {
		return NULL
	}
}

func isTruthy(obj object.Object) bool {
	switch obj {
	case NULL:
		return false
	case TRUE:
		return true
	case FALSE:
		return false
	default:
		return true
	}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.6 - Conditionals"*

### 36. Return Value Wrapper

**Principle:** `object.ReturnValue` is a sentinel wrapper that signals "stop evaluating a block and propagate this value." It is unwrapped only at the program level (or by `unwrapReturnValue` when leaving a function call).

**Code:**
```go
// object/object.go
const (
	// [...]
	RETURN_VALUE_OBJ = "RETURN_VALUE"
)

type ReturnValue struct {
	Value Object
}

func (rv *ReturnValue) Type() ObjectType     { return RETURN_VALUE_OBJ }
func (rv *ReturnValue) Inspect() string       { return rv.Value.Inspect() }
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.7 - Return Statements"*

### 37. Error Object & Short-Circuit Propagation

**Principle:** Errors are `*object.Error{Message string}`. The `isError` helper lets every recursive `Eval` call short-circuit on error, so errors bubble up exactly like return values. Always check `isError` between sub-evaluations so you don't operate on stale data.

**Code:**
```go
// object/object.go
const (
	// [...]
	ERROR_OBJ = "ERROR"
)

type Error struct {
	Message string
}

func (e *Error) Type() ObjectType { return ERROR_OBJ }
func (e *Error) Inspect() string   { return "ERROR: " + e.Message }
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.8 - Error Handling"*

```go
// evaluator/evaluator.go
import (
	// [...]
	"fmt"
)

func newError(format string, a ...interface{}) *object.Error {
	return &object.Error{Message: fmt.Sprintf(format, a...)}
}

func isError(obj object.Object) bool {
	if obj != nil {
		return obj.Type() == object.ERROR_OBJ
	}
	return false
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.8 - Error Handling"*

### 38. Environment — Bindings & Scope Chain

**Principle:** `object.Environment` is a hash map plus an optional `outer` pointer. `Get` walks the chain (inner → outer) until found; `Set` writes to the current (innermost) environment only. `NewEnclosedEnvironment(outer)` creates a child environment that extends an existing one — this is what makes lexical scoping work.

**Do:**
- Always persist the top-level environment across REPL lines so bindings survive.
- In tests, build a fresh environment per case so global state can't leak.

**Code:**
```go
// object/environment.go
package object

func NewEnvironment() *Environment {
	s := make(map[string]Object)
	return &Environment{store: s, outer: nil}
}

func NewEnclosedEnvironment(outer *Environment) *Environment {
	env := NewEnvironment()
	env.outer = outer
	return env
}

type Environment struct {
	store map[string]Object
	outer *Environment
}

func (e *Environment) Get(name string) (Object, bool) {
	obj, ok := e.store[name]
	if !ok && e.outer != nil {
		obj, ok = e.outer.Get(name)
	}
	return obj, ok
}

func (e *Environment) Set(name string, val Object) Object {
	e.store[name] = val
	return val
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.9 - Bindings & The Environment / 3.10 - Functions"*

```go
// evaluator/evaluator.go
func evalIdentifier(
	node *ast.Identifier,
	env *object.Environment,
) object.Object {
	if val, ok := env.Get(node.Value); ok {
		return val
	}
	if builtin, ok := builtins[node.Value]; ok {
		return builtin
	}
	return newError("identifier not found: " + node.Value)
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.9 / 4.3 - evalIdentifier"*

### 39. Function Objects, Closures, Application

**Principle:** `object.Function` stores `Parameters`, `Body`, and crucially `Env` — the environment captured at definition time. Applying a function: build a new enclosed environment around `fn.Env` (not the caller's environment!), bind parameters to arguments, evaluate the body, then unwrap any `ReturnValue` so it doesn't bleed through the caller. Closures work for free because the function carries its defining environment.

**Do:**
- Extend `fn.Env`, never the caller's env — that is the single line that gives you closures.
- Always `unwrapReturnValue` after evaluating the body so a `return` in `addTwo` doesn't terminate `callTwoTimes`.

**Don't:**
- Bind parameters in the caller's scope — that overwrites existing bindings and breaks shadowing.

**Code:**
```go
// object/object.go
import (
	"bytes"
	"fmt"
	"monkey/ast"
	"strings"
)

const (
	// [...]
	FUNCTION_OBJ = "FUNCTION"
)

type Function struct {
	Parameters []*ast.Identifier
	Body       *ast.BlockStatement
	Env        *Environment
}

func (f *Function) Type() ObjectType { return FUNCTION_OBJ }

func (f *Function) Inspect() string {
	var out bytes.Buffer
	params := []string{}
	for _, p := range f.Parameters {
		params = append(params, p.String())
	}
	out.WriteString("fn")
	out.WriteString("(")
	out.WriteString(strings.Join(params, ", "))
	out.WriteString(") {\n")
	out.WriteString(f.Body.String())
	out.WriteString("\n}")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.10 - Functions & Function Calls"*

```go
// evaluator/evaluator.go
func Eval(node ast.Node, env *object.Environment) object.Object {
	switch node := node.(type) {
	// [...]
	case *ast.FunctionLiteral:
		params := node.Parameters
		body := node.Body
		return &object.Function{Parameters: params, Env: env, Body: body}
	case *ast.CallExpression:
		function := Eval(node.Function, env)
		if isError(function) {
			return function
		}
		args := evalExpressions(node.Arguments, env)
		if len(args) == 1 && isError(args[0]) {
			return args[0]
		}
		return applyFunction(function, args)
	}
	return nil
}

func evalExpressions(
	exps []ast.Expression,
	env *object.Environment,
) []object.Object {
	var result []object.Object
	for _, e := range exps {
		evaluated := Eval(e, env)
		if isError(evaluated) {
			return []object.Object{evaluated}
		}
		result = append(result, evaluated)
	}
	return result
}

func applyFunction(fn object.Object, args []object.Object) object.Object {
	switch fn := fn.(type) {
	case *object.Function:
		extendedEnv := extendFunctionEnv(fn, args)
		evaluated := Eval(fn.Body, extendedEnv)
		return unwrapReturnValue(evaluated)
	case *object.Builtin:
		return fn.Fn(args...)
	default:
		return newError("not a function: %s", fn.Type())
	}
}

func extendFunctionEnv(
	fn *object.Function,
	args []object.Object,
) *object.Environment {
	env := object.NewEnclosedEnvironment(fn.Env)
	for paramIdx, param := range fn.Parameters {
		env.Set(param.Value, args[paramIdx])
	}
	return env
}

func unwrapReturnValue(obj object.Object) object.Object {
	if returnValue, ok := obj.(*object.ReturnValue); ok {
		return returnValue.Value
	}
	return obj
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.10 - Functions & Function Calls"*

### 40. Closure Test — The Proof `#general`

**Principle:** The simplest proof that environments work: a function returned from another function must still access the outer function's parameters even after the outer call has returned.

**Code:**
```go
// evaluator/evaluator_test.go
func TestClosures(t *testing.T) {
	input := `
let newAdder = fn(x) {
	fn(y) { x + y };
};
let addTwo = newAdder(2);
addTwo(2);`
	testIntegerObject(t, testEval(input), 4)
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "3.10 - Functions & Function Calls"*

---

## Chapter 4 — Extending the Interpreter `#general` `#go`

### 41. Adding a New Data Type — The Four-Layer Pattern

**Principle:** Every new data type follows the same recipe. (1) Add a `token.*` constant. (2) Add a lexer case. (3) Add an AST node + parser registration. (4) Add an `object.*` type + evaluator branch. The pattern keeps the codebase navigiable as features multiply.

**Do:**
- Mirror an existing data type's implementation as your starting template.
- Add tests at every layer in the same order.

### 42. String Literals

**Principle:** Strings are delimited by `"`. The lexer's `readString()` loops until the closing quote or EOF. The parser turns `token.STRING` into `*ast.StringLiteral`. The evaluator returns `*object.String{Value: node.Value}`. Concatenation is the only supported infix operator.

**Code:**
```go
// token/token.go
const (
	// [...]
	STRING = "STRING"
	// [...]
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - Supporting Strings in our Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	// [...]
	switch l.ch {
	// [...]
	case '"':
		tok.Type = token.STRING
		tok.Literal = l.readString()
	// [...]
	}
	// [...]
}

func (l *Lexer) readString() string {
	position := l.position + 1
	for {
		l.readChar()
		if l.ch == '"' || l.ch == 0 {
			break
		}
	}
	return l.input[position:l.position]
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - Supporting Strings in our Lexer"*

```go
// ast/ast.go
type StringLiteral struct {
	Token token.Token
	Value string
}

func (sl *StringLiteral) expressionNode()      {}
func (sl *StringLiteral) TokenLiteral() string { return sl.Token.Literal }
func (sl *StringLiteral) String() string       { return sl.Token.Literal }
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - Parsing Strings"*

```go
// parser/parser.go
func (p *Parser) parseStringLiteral() ast.Expression {
	return &ast.StringLiteral{Token: p.curToken, Value: p.curToken.Literal}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - Parsing Strings"*

```go
// object/object.go
const (
	// [...]
	STRING_OBJ = "STRING"
)

type String struct {
	Value string
}

func (s *String) Type() ObjectType { return STRING_OBJ }
func (s *String) Inspect() string   { return s.Value }
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - Evaluating Strings"*

```go
// evaluator/evaluator.go
func evalStringInfixExpression(
	operator string,
	left, right object.Object,
) object.Object {
	if operator != "+" {
		return newError("unknown operator: %s %s %s",
			left.Type(), operator, right.Type())
	}
	leftVal := left.(*object.String).Value
	rightVal := right.(*object.String).Value
	return &object.String{Value: leftVal + rightVal}
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.2 - String Concatenation"*

### 43. Built-in Functions — Bridge to Go

**Principle:** Built-ins are Go functions exposed to Monkey. Define a `BuiltinFunction func(args ...Object) Object` type, wrap instances in `*object.Builtin`, register them in a `builtins` map, and look them up as a fallback in `evalIdentifier`. `applyFunction` switches on `*object.Builtin` separately from `*object.Function` so built-ins skip environment setup.

**Do:**
- Always validate argument count and types inside the built-in — return `newError` for misuse.
- Have built-ins return `NULL` when they have no meaningful value (e.g. `puts`).

**Code:**
```go
// object/object.go
type BuiltinFunction func(args ...Object) Object

const (
	// [...]
	BUILTIN_OBJ = "BUILTIN"
)

type Builtin struct {
	Fn BuiltinFunction
}

func (b *Builtin) Type() ObjectType { return BUILTIN_OBJ }
func (b *Builtin) Inspect() string   { return "builtin function" }
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.3 - Built-in Functions"*

```go
// evaluator/builtins.go
package evaluator

import "monkey/object"

var builtins = map[string]*object.Builtin{
	"len": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			if len(args) != 1 {
				return newError("wrong number of arguments. got=%d, want=1",
					len(args))
			}
			switch arg := args[0].(type) {
			case *object.Array:
				return &object.Integer{Value: int64(len(arg.Elements))}
			case *object.String:
				return &object.Integer{Value: int64(len(arg.Value))}
			default:
				return newError("argument to `len` not supported, got %s",
					args[0].Type())
			}
		},
	},
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.3 - len / 4.4 - Adding Built-in Functions for Arrays"*

### 44. Arrays — Lexer, Parser, Evaluator

**Principle:** Arrays reuse `parseExpressionList` for elements. The index operator is registered as an infix parser for `token.LBRACKET` with `INDEX` precedence. Out-of-bounds access returns `NULL` (a design choice — errors are an alternative). Arrays are immutable: `push` returns a new array.

**Code:**
```go
// token/token.go
const (
	// [...]
	LBRACKET = "["
	RBRACKET = "]"
	// [...]
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Supporting Arrays in our Lexer"*

```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	// [...]
	case '[':
		tok = newToken(token.LBRACKET, l.ch)
	case ']':
		tok = newToken(token.RBRACKET, l.ch)
	// [...]
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Supporting Arrays in our Lexer"*

```go
// ast/ast.go
type ArrayLiteral struct {
	Token    token.Token // the '[' token
	Elements []Expression
}

func (al *ArrayLiteral) expressionNode()      {}
func (al *ArrayLiteral) TokenLiteral() string { return al.Token.Literal }

func (al *ArrayLiteral) String() string {
	var out bytes.Buffer
	elements := []string{}
	for _, el := range al.Elements {
		elements = append(elements, el.String())
	}
	out.WriteString("[")
	out.WriteString(strings.Join(elements, ", "))
	out.WriteString("]")
	return out.String()
}

type IndexExpression struct {
	Token token.Token // The [ token
	Left  Expression
	Index Expression
}

func (ie *IndexExpression) expressionNode()      {}
func (ie *IndexExpression) TokenLiteral() string { return ie.Token.Literal }

func (ie *IndexExpression) String() string {
	var out bytes.Buffer
	out.WriteString("(")
	out.WriteString(ie.Left.String())
	out.WriteString("[")
	out.WriteString(ie.Index.String())
	out.WriteString("])")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Parsing Array Literals / Index Operator"*

```go
// parser/parser.go
func (p *Parser) parseArrayLiteral() ast.Expression {
	array := &ast.ArrayLiteral{Token: p.curToken}
	array.Elements = p.parseExpressionList(token.RBRACKET)
	return array
}

func (p *Parser) parseIndexExpression(left ast.Expression) ast.Expression {
	exp := &ast.IndexExpression{Token: p.curToken, Left: left}
	p.nextToken()
	exp.Index = p.parseExpression(LOWEST)
	if !p.expectPeek(token.RBRACKET) {
		return nil
	}
	return exp
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Parsing Array Literals / Index Operator"*

```go
// object/object.go
const (
	// [...]
	ARRAY_OBJ = "ARRAY"
)

type Array struct {
	Elements []Object
}

func (ao *Array) Type() ObjectType { return ARRAY_OBJ }

func (ao *Array) Inspect() string {
	var out bytes.Buffer
	elements := []string{}
	for _, e := range ao.Elements {
		elements = append(elements, e.Inspect())
	}
	out.WriteString("[")
	out.WriteString(strings.Join(elements, ", "))
	out.WriteString("]")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Evaluating Array Literals"*

```go
// evaluator/evaluator.go
func Eval(node ast.Node, env *object.Environment) object.Object {
	switch node := node.(type) {
	// [...]
	case *ast.ArrayLiteral:
		elements := evalExpressions(node.Elements, env)
		if len(elements) == 1 && isError(elements[0]) {
			return elements[0]
		}
		return &object.Array{Elements: elements}
	case *ast.IndexExpression:
		left := Eval(node.Left, env)
		if isError(left) {
			return left
		}
		index := Eval(node.Index, env)
		if isError(index) {
			return index
		}
		return evalIndexExpression(left, index)
	// [...]
	}
}

func evalIndexExpression(left, index object.Object) object.Object {
	switch {
	case left.Type() == object.ARRAY_OBJ && index.Type() == object.INTEGER_OBJ:
		return evalArrayIndexExpression(left, index)
	case left.Type() == object.HASH_OBJ:
		return evalHashIndexExpression(left, index)
	default:
		return newError("index operator not supported: %s", left.Type())
	}
}

func evalArrayIndexExpression(array, index object.Object) object.Object {
	arrayObject := array.(*object.Array)
	idx := index.(*object.Integer).Value
	max := int64(len(arrayObject.Elements) - 1)
	if idx < 0 || idx > max {
		return NULL
	}
	return arrayObject.Elements[idx]
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Evaluating Array Literals / Index Expressions / 4.5 - Hash Index"*

### 45. Array Built-ins — first / last / rest / push

**Principle:** Build the standard Lisp-like array toolkit on top of immutable arrays. `rest` and `push` allocate new arrays so the originals are never mutated — this prevents aliasing bugs and makes programs easier to reason about. These four primitives are sufficient to implement `map` and `reduce` in Monkey itself.

**Code:**
```go
// evaluator/builtins.go
var builtins = map[string]*object.Builtin{
	// [...]
	"first": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			if len(args) != 1 {
				return newError("wrong number of arguments. got=%d, want=1",
					len(args))
			}
			if args[0].Type() != object.ARRAY_OBJ {
				return newError("argument to `first` must be ARRAY, got %s",
					args[0].Type())
			}
			arr := args[0].(*object.Array)
			if len(arr.Elements) > 0 {
				return arr.Elements[0]
			}
			return NULL
		},
	},
	"last": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			if len(args) != 1 {
				return newError("wrong number of arguments. got=%d, want=1",
					len(args))
			}
			if args[0].Type() != object.ARRAY_OBJ {
				return newError("argument to `last` must be ARRAY, got %s",
					args[0].Type())
			}
			arr := args[0].(*object.Array)
			length := len(arr.Elements)
			if length > 0 {
				return arr.Elements[length-1]
			}
			return NULL
		},
	},
	"rest": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			if len(args) != 1 {
				return newError("wrong number of arguments. got=%d, want=1",
					len(args))
			}
			if args[0].Type() != object.ARRAY_OBJ {
				return newError("argument to `rest` must be ARRAY, got %s",
					args[0].Type())
			}
			arr := args[0].(*object.Array)
			length := len(arr.Elements)
			if length > 0 {
				newElements := make([]object.Object, length-1, length-1)
				copy(newElements, arr.Elements[1:length])
				return &object.Array{Elements: newElements}
			}
			return NULL
		},
	},
	"push": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			if len(args) != 2 {
				return newError("wrong number of arguments. got=%d, want=2",
					len(args))
			}
			if args[0].Type() != object.ARRAY_OBJ {
				return newError("argument to `push` must be ARRAY, got %s",
					args[0].Type())
			}
			arr := args[0].(*object.Array)
			length := len(arr.Elements)
			newElements := make([]object.Object, length+1, length+1)
			copy(newElements, arr.Elements)
			newElements[length] = args[1]
			return &object.Array{Elements: newElements}
		},
	},
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Adding Built-in Functions for Arrays"*

### 46. Hash Literals — Lexing & Parsing

**Principle:** A hash literal `{ expr: expr, expr: expr, ... }` is a comma-separated list of colon-separated pairs. Allow any expression as key or value at parse time — enforce "hashable" restriction in the evaluator, so identifiers and computed expressions can be keys.

**Code:**
```go
// token/token.go
const (
	// [...]
	COLON = ":"
	// [...]
)
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Lexing Hash Literals"*

```go
// lexer/lexer.go
func (l *Lexer) NextToken() token.Token {
	// [...]
	case ':':
		tok = newToken(token.COLON, l.ch)
	// [...]
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Lexing Hash Literals"*

```go
// ast/ast.go
type HashLiteral struct {
	Token token.Token // the '{' token
	Pairs map[Expression]Expression
}

func (hl *HashLiteral) expressionNode()      {}
func (hl *HashLiteral) TokenLiteral() string { return hl.Token.Literal }

func (hl *HashLiteral) String() string {
	var out bytes.Buffer
	pairs := []string{}
	for key, value := range hl.Pairs {
		pairs = append(pairs, key.String()+":"+value.String())
	}
	out.WriteString("{")
	out.WriteString(strings.Join(pairs, ", "))
	out.WriteString("}")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Parsing Hash Literals"*

```go
// parser/parser.go
func (p *Parser) parseHashLiteral() ast.Expression {
	hash := &ast.HashLiteral{Token: p.curToken}
	hash.Pairs = make(map[ast.Expression]ast.Expression)
	for !p.peekTokenIs(token.RBRACE) {
		p.nextToken()
		key := p.parseExpression(LOWEST)
		if !p.expectPeek(token.COLON) {
			return nil
		}
		p.nextToken()
		value := p.parseExpression(LOWEST)
		hash.Pairs[key] = value
		if !p.peekTokenIs(token.RBRACE) && !p.expectPeek(token.COMMA) {
			return nil
		}
	}
	if !p.expectPeek(token.RBRACE) {
		return nil
	}
	return hash
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Parsing Hash Literals"*

### 47. The Hashing Problem — HashKey & Hashable

**Principle:** A naive `map[Object]Object` fails because Go compares pointers, not values — two `*object.String{Value:"name"}` instances point to different memory. The solution is `HashKey{Type ObjectType, Value uint64}` that combines the type tag (so different types never collide) with a value-derived hash (FNV-1a for strings, raw integer for integers, 0/1 for booleans). `Hashable` is the interface gates which types may serve as keys.

**Do:**
- Always include `Type` in `HashKey` — without it, the integer `1` and boolean `true` would collide.
- Keep the original key object around (in `HashPair`) so `Inspect()` can render the user-facing value.

**Don't:**
- Try to compare `*object.String` pointers directly — equivalent values at different addresses will not be equal.

**Code:**
```go
// object/object.go
import (
	// [...]
	"hash/fnv"
)

type HashKey struct {
	Type  ObjectType
	Value uint64
}

func (b *Boolean) HashKey() HashKey {
	var value uint64
	if b.Value {
		value = 1
	} else {
		value = 0
	}
	return HashKey{Type: b.Type(), Value: value}
}

func (i *Integer) HashKey() HashKey {
	return HashKey{Type: i.Type(), Value: uint64(i.Value)}
}

func (s *String) HashKey() HashKey {
	h := fnv.New64a()
	h.Write([]byte(s.Value))
	return HashKey{Type: s.Type(), Value: h.Sum64()}
}

type Hashable interface {
	HashKey() HashKey
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Hashing Objects"*

```go
// object/object.go
const (
	// [...]
	HASH_OBJ = "HASH"
)

type HashPair struct {
	Key   Object
	Value Object
}

type Hash struct {
	Pairs map[HashKey]HashPair
}

func (h *Hash) Type() ObjectType { return HASH_OBJ }

func (h *Hash) Inspect() string {
	var out bytes.Buffer
	pairs := []string{}
	for _, pair := range h.Pairs {
		pairs = append(pairs, fmt.Sprintf("%s: %s",
			pair.Key.Inspect(), pair.Value.Inspect()))
	}
	out.WriteString("{")
	out.WriteString(strings.Join(pairs, ", "))
	out.WriteString("}")
	return out.String()
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Hashing Objects"*

### 48. Evaluating Hash Literals & Index Lookups

**Principle:** When evaluating `*ast.HashLiteral`, evaluate each key, assert it implements `Hashable`, generate its `HashKey`, evaluate the value, store both in `HashPair`. For index lookups on a hash, type-assert the index to `Hashable` and look up `key.HashKey()` in `Pairs`; missing keys return `NULL`.

**Code:**
```go
// evaluator/evaluator.go
func evalHashLiteral(
	node *ast.HashLiteral,
	env *object.Environment,
) object.Object {
	pairs := make(map[object.HashKey]object.HashPair)
	for keyNode, valueNode := range node.Pairs {
		key := Eval(keyNode, env)
		if isError(key) {
			return key
		}
		hashKey, ok := key.(object.Hashable)
		if !ok {
			return newError("unusable as hash key: %s", key.Type())
		}
		value := Eval(valueNode, env)
		if isError(value) {
			return value
		}
		hashed := hashKey.HashKey()
		pairs[hashed] = object.HashPair{Key: key, Value: value}
	}
	return &object.Hash{Pairs: pairs}
}

func evalHashIndexExpression(hash, index object.Object) object.Object {
	hashObject := hash.(*object.Hash)
	key, ok := index.(object.Hashable)
	if !ok {
		return newError("unusable as hash key: %s", index.Type())
	}
	pair, ok := hashObject.Pairs[key.HashKey()]
	if !ok {
		return NULL
	}
	return pair.Value
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.5 - Evaluating Hash Literals / Index Expressions With Hashes"*

### 49. The puts Built-in — Talking to the Outside World

**Principle:** `puts` prints each argument's `Inspect()` output on a separate line and returns `NULL`. It is the final piece that makes Monkey a real language — output, not just computation. Built-ins skip `unwrapReturnValue` because they never return `*object.ReturnValue`.

**Code:**
```go
// evaluator/builtins.go
import (
	"fmt"
	"monkey/object"
)

var builtins = map[string]*object.Builtin{
	// [...]
	"puts": &object.Builtin{
		Fn: func(args ...object.Object) object.Object {
			for _, arg := range args {
				fmt.Println(arg.Inspect())
			}
			return NULL
		},
	},
}
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.6 - The Grand Finale"*

### 50. Defining map & reduce in Monkey Itself `#general`

**Principle:** With `first`, `rest`, and `push` available, higher-order combinators can be written in Monkey rather than Go. This proves the interpreter is sufficiently expressive — the standard library lives in the language it implements.

**Code (Monkey source, not Go):**
```monkey
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

let sum = fn(arr) {
    reduce(arr, 0, fn(initial, el) { initial + el });
};
```
*Ref: Writing_an_Interpreter_in_Go.md — "4.4 - Test-Driving Arrays"*

---

## Anti-Patterns & Common Mistakes

- **Single-pointer lexer:** Can't lookahead for `==` / `!=` → *fix:* track `position` AND `readPosition`, expose `peekChar()`.
- **Stop on first parse error:** Forces users to fix-and-rerun for every error → *fix:* accumulate `errors []string` and report them all.
- **Forgetting to call `readChar` / `nextToken` after emitting a token:** Off-by-one infinite loops → *fix:* adopt a strict "where does my parser start and end on `curToken`?" protocol.
- **Using `*object.String` pointers as Go map keys:** Equivalent values at different addresses fail to match → *fix:* define `HashKey` with a type tag + value hash; use it as the map key.
- **Binding arguments in the caller's environment:** Breaks shadowing and overwrites outer bindings → *fix:* always `NewEnclosedEnvironment(fn.Env)` and bind there.
- **Unwrapping `ReturnValue` inside `evalBlockStatement`:** A nested `return` stops too early → *fix:* only `evalProgram` (and `unwrapReturnValue` after function calls) unwrap.
- **Returning `NULL` for unsupported operations silently:** Hides bugs → *fix:* once errors exist, replace every `return NULL` in operator paths with `newError(...)`.
- **Allocating fresh `*object.Boolean`/`*object.Null` per literal:** Wastes GC and breaks pointer-equality for `==` → *fix:* use package-level singletons `TRUE`/`FALSE`/`NULL`.
- **Skipping `isError` checks between sub-evaluations:** Errors propagate partially, hide root cause → *fix:* check after every `Eval` call inside `Eval`.
- **Letting `IndexExpression` precedence be too low:** `arr[i] + 1` mis-parses → *fix:* `INDEX` must be the highest precedence constant.

## Decision Heuristics / Checklists

**When to extend which layer for a new language feature:**
1. New literal or operator? Add `token.*` constant, lexer case, AST node, parser registration, object type, evaluator branch.
2. Behavior only (no new syntax)? Add a built-in in `evaluator/builtins.go`.
3. New keyword? Add to `keywords` map and write a new prefix parse function.

**Parser protocol checklist for every parse function:**
- [ ] Enter with `curToken` of the associated token type.
- [ ] Exit with `curToken` on the last token of the expression.
- [ ] Use `expectPeek` (not raw `nextToken`) whenever a specific next token is required.
- [ ] Register both prefix and infix handlers if the token can appear in either position.

**Evaluator checklist for every new node type:**
- [ ] Add a `case *ast.YourNode:` branch to `Eval`.
- [ ] Check `isError` after every recursive `Eval` call.
- [ ] Use singletons (`TRUE`/`FALSE`/`NULL`) instead of allocating where possible.
- [ ] Add tests for the happy path, error path, and at least one nested context.

**Test-design heuristics:**
- Use table-driven tests for operators, precedences, and built-ins.
- Use `String()` round-trip comparison for parser output — single-line assertions catch precedence bugs.
- Build a fresh `*object.Environment` per test case so order doesn't matter.

## Key Takeaways

1. **Three layers, three contracts.** Lexer emits tokens, parser emits AST, evaluator emits objects — each with its own types and tests. Keep them independent.
2. **Pratt parsing is the elegant answer to expressions.** Token-typed prefix/infix functions + a `precedence < peekPrecedence()` loop handle associativity, precedence, and parentheses uniformly.
3. **The object system is the bridge.** Every runtime value wraps a Go primitive in a struct implementing `Object`. Singletons for `TRUE`/`FALSE`/`NULL` enable fast pointer equality and reduce allocation pressure.
4. **Environments give you closures for free.** A `*Function` captures its defining environment; applying it extends that environment rather than the caller's. Closures fall out naturally.
5. **Return values and errors are both propagation problems.** Model them as wrapped objects (`ReturnValue`, `Error`) and short-circuit at every level. Distinguish `evalProgram` (unwraps return) from `evalBlockStatement` (does not).
6. **Hash keys need value-equality, not pointer-equality.** Use a typed `HashKey` (type tag + value hash) so equivalent values at different addresses compare equal and different types never collide.
7. **Immutability simplifies reasoning.** Array built-ins like `push`/`rest` allocate new arrays — no aliasing bugs, easier mental model, tiny performance cost in a teaching interpreter.
8. **TDD shines for language implementations.** Each layer is built test-first; the test suite is the language specification. The `String()` methods on AST nodes enable round-trip checks that catch precedence bugs in one assertion.
9. **Start simple, optimize later.** A tree-walking interpreter is the slowest design but the easiest to understand, build, and extend. The sequel ("Writing A Compiler In Go") shows the natural next step: bytecode + VM, ~3× faster.
10. **Reuse Go's GC.** Don't write your own garbage collector unless you're forced to (e.g., a C host). Reusing Go's GC is correct, simple, and outside the scope of a first interpreter.

## Cross-References
- Related: [[../Writing_A_Compiler_In_Go.md]] — the sequel that replaces the tree-walking evaluator with a bytecode VM
- Topic index: [[../INDEX.md]]
