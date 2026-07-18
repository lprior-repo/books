# Per-Book Best Practices — Deep Dive Template

> Copy this structure for every book. Keep it exhaustive: principles, do/don't,
> anti-patterns, and ALL relevant code snippets. Tag every file with topic(s).

---

# {Book Title}
**Author:** {name}
**Topic tags:** `#concurrency` `#testing` `#architecture` `#api` `#cli` (use the relevant ones)
**Language focus:** Go-first / language-agnostic
**Sources:** `markdown_output/{book}/{book}.md` · `summaries/{book}.md`

## TL;DR
{2–4 sentences: what this book contributes and when to apply it.}

---

## Best Practices by Topic

### {Topic, e.g. Concurrency Primitives / Goroutine Lifecycle}

**Principle:** {the rule in one sentence}

**Do:**
- {actionable best practice}
- {actionable best practice}

**Don't:**
- {anti-pattern to avoid}
- {anti-pattern to avoid}

**Code:**
```go
// {what this demonstrates}
...real snippet from the book...
```
*Ref: {book}.md — "{section / chapter heading}"*

---

(repeat per topic / principle cluster)

## Anti-Patterns & Common Mistakes
- **{pattern name}:** {why it's bad} → *fix:* {correct approach}
- ...

## Decision Heuristics / Checklists
- {e.g. "When to use channels vs mutexes"}
- {e.g. "Table-driven test checklist"}

## Key Takeaways
1. {most important, reusable rule}
2. ...

## Cross-References
- Related: [[../{other-book}.md]]
- Topic index: [[../INDEX.md]]
