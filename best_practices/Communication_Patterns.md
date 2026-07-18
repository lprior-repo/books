# Communication Patterns
**Author:** Jacqui Read
**Topic tags:** `#api` `#general`
**Language focus:** Language-agnostic
**Sources:** `markdown_output/Communication Patterns/Communication Patterns.md` · `summaries/Communication_Patterns.md`

> ⚠️ Note on coverage. The task brief described *Enterprise Integration
> Patterns* topics (messaging styles, message channels, envelope construction,
> content-based / recipient-list / load-balancer routing, message endpoints,
> system-management channels). The book actually present at this path is
> Jacqui Read's *Communication Patterns: A Guide for Developers and Architects*
> (O'Reilly, 2023, ISBN 978-1-098-14054-0) — a book on technical *communication
> skills* (visual, written, verbal/nonverbal, knowledge management, remote teams,
> ADRs), *not* on EAI message routing. This file extracts exhaustively from the
> actual book. Hohpe/Woolf-style messaging patterns are covered in
> `../Monolith_To_Microservices.md` and `../Building_Event-driven_Microservices.md`
> where they actually appear in the corpus.

## TL;DR
*Communication Patterns* teaches developers and architects the **soft-skills
patterns** that determine whether their designs ever ship. Visual artifacts
(diagrams, docs, slides, ADRs) are the highest-leverage channel; messages
must be tailored to audience, use a single level of abstraction, be accessible,
and tell a story. Written communication favors simple, structured, action-
oriented prose. Verbal/nonverbal communication relies on ethos / pathos /
logos, active listening, and *async-first* cadence for distributed teams.
Knowledge is treated as a product (not a project artefact): capture the
*why* (ADRs), persist in version control, regenerate from code where
possible, and apply perspective-driven documentation (DRY, fractal, "just enough").

---

## Best Practices by Topic

### Communication Essentials (Foundational Patterns)

**Principle:** Know your audience before drafting any artifact; keep one
abstraction level per diagram; be representationally consistent across
the diagram set.

**Do:**
- Make a list of roles that will read each diagram, then ask: "What do they
  want from me? What do I want from them? What is their technical
  understanding? What level of detail?"
  *Ref: Communication Patterns.md — "Know Your Audience" (`page-25-0`).*
- Use the **C4 model** (Context → Container → Component → Code) to keep each
  diagram at exactly one level of abstraction.
  *Ref: Communication Patterns.md — "Mixing Levels of Abstraction" (`page-28-0`).*
- Maintain **representational consistency** across related diagrams — same
  central label, same identifiers, same color. Link diagrams by explicit
  labels ("Figure 3: Polyglot Media — container").
  *Ref: Communication Patterns.md — "Representational Consistency" (`page-32-0`).*

**Don't:**
- Don't put a low-level data-flow diagram (level 2) before a high-level
  level-1; without context details are confusing.
  *Ref: Communication Patterns.md — "The Big Picture Comes First" (`page-64-0`).*
- Don't use C4 *and* ArchiMate *and* Visio at random — pick a notation
  the audience can read.
  *Ref: Communication Patterns.md — "Going Against Expectations" (`page-64-0`).*

---

### Clarify the Clutter (Diagram Anti-Patterns)

**Principle:** A diagram earns its place by reducing the audience's cognitive
load. Anything that doesn't serve *the one message* is clutter.

**Do:**
- Use **4 colors max** — each color groups a *type* (UI / data store / API /
  service). Provide a legend.
  *Ref: Communication Patterns.md — "Color Overload" (`page-38-0`).*
- Use *orthogonal* (right-angle) connectors, not diagonal ones. Use line
  *jumps* (an arc) when two lines cross.
  *Ref: Communication Patterns.md — "Relationship Spiderweb" (`page-43-0`).*
- Replace *boxes in boxes in boxes* with labels, color patterns, or a
  separate diagram. Whitespace is your friend.
  *Ref: Communication Patterns.md — "Boxes in Boxes in Boxes" (`page-40-0`).*
- Promote repeated words to a title; use annotations / superscripted notes
  rather than paragraph text inside shapes.
  *Ref: Communication Patterns.md — "Balance Text" (`page-47-0`).*

**Don't:**
- Don't color every component differently — "rainbow sequence diagram"
  antipattern.
  *Ref: Communication Patterns.md — "Color Overload" (`page-38-0`).*
- Don't let connector lines cross components without line jumps.
  *Ref: Communication Patterns.md — "Relationship Spiderweb" (`page-44-0`).*

---

### Accessibility

**Principle:** Aim for diagrams that an audience member with *any* color-vision
deficiency, screen size, reading level, or language background can read.

**Do:**
- Always combine color with a second differentiator (pattern, shape,
  symbol, position, label) — *"The red boxes with dashed borders show…"*
  *Ref: Communication Patterns.md — "Relying on Color to Communicate" (`page-52-0`).*
- Use a contrast-ratio tool (e.g., WhoCanUse) and a color-blindness simulator
  (Color Oracle, Coblis, Sim Daltonism) on every corporate palette and
  every default palette from your drawing tool.
  *Ref: Communication Patterns.md — "Design Tools for Color Vision Deficiency" (`page-55-0`).*
- Include a legend and explicit alt text; reach for 12-pt legibility
  minimum, consider Atkinson Hyperlegible.
  *Ref: Communication Patterns.md — "Include a Legend" (`page-58-0`), "Appropriate Labels" (`page-60-0`).*
- Adjust palette for medium: print is grayscale; projector palettes differ
  from web.
  *Ref: Communication Patterns.md — "Contrast" (`page-54-0`).*

**Don't:**
- Don't exclusively use red / green to signal pass / fail — accessible
  GitHub diff adds + and - signs for this reason.
  *Ref: Communication Patterns.md — "Relying on Color to Communicate" (`page-52-0`).*
- Don't trust the default palette of your diagramming tool.
  *Ref: Communication Patterns.md — "Color Oracle..." (`page-57-0`).*

---

### Narrative (Story-Driven Diagrams)

**Principle:** Order diagrams as a story — *The Big Picture Comes First*;
match diagram flow to audience reading expectations.

**Do:**
- Place the *start* of the diagram at the top-left, in the natural
  reading-flow direction (English: left → right, top → bottom).
  *Ref: Communication Patterns.md — "Match Diagram Flow to Expectations" (`page-68-0`).*
- For data flow: requests flow left → right, responses right → left.
  For sequence: arrange participants in the order they're called. For
  infrastructure diagrams: actors on top, systems in middle, data stores
  on bottom.
  *Ref: Communication Patterns.md — "Match Diagram Flow to Expectations" (`page-68-0`).*
- Use *clear relationships* — unidirectional arrows labeled in the
  direction of the call. Bidirectional arrows lose information.
  *Ref: Communication Patterns.md — "Clear Relationships" (`page-72-0`).*
- Use a "Start here" marker or numbered labels when the natural layout
  has to deviate.
  *Ref: Communication Patterns.md — "Match Diagram Flow to Expectations" (`page-68-0`).*
- Quote Gregor's LEGOs mental model: "When you look at the cover of a box
  of LEGOs you don't see a picture of each individual brick."
  *Ref: Communication Patterns.md — "The Big Picture Comes First" (`page-64-0`).*

**Don't:**
- Don't lead with implementation details: "Figure 4-1 is a Level-2 data
  flow diagram. That is where you want to get to eventually, but it is not
  where the document or presentation should start."
  *Ref: Communication Patterns.md — "The Big Picture Comes First" (`page-65-0`).*

---

### Notation (Use Right Notation for Right Audience)

**Principle:** Pick the notation that matches the audience and message; never
"UML for UML's sake."

**Do:**
- Use icons to convey meaning clearly — but only when the convention is
  shared.
  *Ref: Communication Patterns.md — "Using Icons to Convey Meaning" (`page-55-0`).*
- Use UML when audience already knows it; use C4 when introducing
  context/container diagrams; use plain shapes + labels for mixed-technical
  audiences.
  *Ref: Communication Patterns.md — "Using UML for UML's Sake" (`page-57-0`).*
- Keep structural and behavioral concerns on different diagrams.
  *Ref: Communication Patterns.md — "Mixing Behavior and Structure" (`page-61-0`).*

**Don't:**
- Don't force ArchiMate on a non-architect audience.
  *Ref: Communication Patterns.md — "Notation" (`page-55-0`).*
- Don't use one diagram to show both structure *and* behavior.
  *Ref: Communication Patterns.md — "Mixing Behavior and Structure" (`page-61-0`).*

---

### Composition (Layout, Style, Legibility)

**Principle:** Make the diagram legible at every scale; let consistent style
carry implicit meaning.

**Do:**
- Pick the *right* diagram size — legibility beats density.
  *Ref: Communication Patterns.md — "Illegible Diagrams" (`page-67-0`).*
- Use *style* (border weight, fill, font weight) as a secondary channel
  beside color, so monochrome prints and color-blind viewers still get
  the meaning.
  *Ref: Communication Patterns.md — "Style Communicates" (`page-74-0`).*
- Create *visual balance* — avoid orphan components floating on one side.
  *Ref: Communication Patterns.md — "Create a Visual Balance" (`page-81-0`).*
- Beware *misleading composition*: arrows that look like they connect to A
  when they connect to B, accidental boxes stacked in ways that imply
  containment.
  *Ref: Communication Patterns.md — "Misleading Composition" (`page-75-0`).*

---

### Written Communication (Patterns)

**Principle:** Optimize written artifacts for the reader's understanding, not
the writer's preferred idiom.

**Do:**
- Use *Simple Language* — everyday words beat jargon. Define or replace
  domain acronyms on first use.
  *Ref: Communication Patterns.md — "Simple Language" (`page-87-0`), "Acronym Hell" (`page-90-0`).*
- Use *Structured Writing*: one idea per paragraph; lead with the conclusion;
  use active voice; strong verbs; short sentences.
  *Ref: Communication Patterns.md — "Structured Writing" (`page-92-0`), "Precise Paragraphs" (`page-96-0`), "Strong Verbs" (`page-95-0`), "Short Sentences" (`page-96-0`).*
- Keep *consistent vocabulary* — same term for the same concept; build a
  glossary.
  *Ref: Communication Patterns.md — "Consistent Vocabulary" (`page-97-0`).*
- Apply *Audience Empathy* — write for the reader, not for the writer; never
  assume context the reader doesn't have.
  *Ref: Communication Patterns.md — "Audience Empathy" (`page-97-0`).*
- Pick a document structure by purpose:
  - *Proposals*: Problem → Options → Recommendation → Next Steps
  - *Status updates*: Done → In progress → Blocked → Next
  - *Incident reports*: Timeline → Impact → Root cause → Remediation → Follow-ups
  - *Code reviews*: Specific + actionable; explain *why*
  *Ref: Communication Patterns.md — "Proposals / Status Updates / Incident Reports / Code Reviews" — synthesized from Part III guidance.*

**Don't:**
- Don't bury ledes — research shows most readers will only see the headline.
  *Ref: Communication Patterns.md — "Structured Writing" (`page-92-0`).*
- Don't let verb tense flip awkwardly; stay present-tense for current state.
  *Ref: Communication Patterns.md — "Syntax of Technical Writing" (`page-95-0`).*

---

### Verbal & Nonverbal Communication

**Principle:** Successful encoding (sending) + successful decoding (receiving)
= understanding. Reach for attention, openness, and bias awareness.

**Do — Encoding:**
- *Acceptance Prophecy:* "Assume people will be receptive; they usually are."
  *Ref: Communication Patterns.md — "Using the Acceptance Prophecy" (`page-101-0`).*
- Give *full attention* — put devices away, eye contact, engaged posture.
  *Ref: Communication Patterns.md — "Giving Your Full Attention" (`page-102-0`).*
- Use open *body language and gestures*; mirror to build rapport.
  *Ref: Communication Patterns.md — "Using Body Language and Gestures" (`page-103-0`).*

**Do — Decoding:**
- *Battling Bias:* name and counter confirmation bias, anchoring, halo.
  *Ref: Communication Patterns.md — "Battling Bias" (`page-106-0`).*
- *Be present* — paraphrase what you heard back to the speaker.
  *Ref: Communication Patterns.md — "Being Present" (`page-108-0`).*
- *Cultural awareness:* time, formality, eye-contact, directness all vary.
  *Ref: Communication Patterns.md — "Awareness of Cultural Differences" (`page-109-0`).*

**Apply the influence levers (ethically):**
- *Reciprocity:* give before you ask.
- *Social proof:* show others have adopted.
- *Authority:* cite sources.
- *Scarcity:* highlight real urgency.
- *Commitment & consistency:* start small, build up.
  *Ref: Communication Patterns.md — "Influence and Persuasion" (`page-110-0`).*

**Don't:**
- Don't assume silence = agreement — *"assumed consensus" antipattern*.
  *Ref: Communication Patterns.md — `summaries/Communication_Patterns.md` — "Communication anti-patterns".*

---

### The Rhetoric Triangle (Ethos, Pathos, Logos)

**Principle:** Combine credibility, emotional connection, and logical argument.

**Do — Ethos (credibility):**
- State credentials, cite trustworthy sources, be transparent about limits,
  demonstrate deep knowledge.
  *Ref: Communication Patterns.md — "Establish Your Credentials" (`page-116-0`).*

**Do — Pathos (emotion):**
- Tell a *story* — "stories can capture your audience's attention, keep that
  attention, communicate concepts…"
  *Ref: Communication Patterns.md — "Tell a Story" (`page-122-0`).*
- Speak from the heart, use vivid imagery.
  *Ref: Communication Patterns.md — "Use Vivid Language and Strong Imagery" (`page-126-0`).*

**Do — Logos (logic):**
- Use data and facts, make logical connections explicit, present
  trade-offs honestly (especially useful for ADRs).
  *Ref: Communication Patterns.md — "Use Data and Facts" (`page-128-0`), "Make Logical Connections" (`page-129-0`).*

---

### Presentations & Storytelling

**Principle:** Storyboard before slides. Use the Hero's-journey arc:
current state → challenge → journey → resolution → new normal.

**Do:**
- *10/20/30* (Kawasaki): 10 slides, 20 min, 30-point font.
  *Ref: Communication Patterns.md — "Part IV / Part III" summary guidance.*
- Group ideas in *rule of three* for memorability.
  *Ref: Communication Patterns.md — synthesized from "Storyboard first" pattern.*
- *Start with why* — open with the problem/motivation, not the solution.
  *Ref: Communication Patterns.md — "Storytelling for architects" guidance.*

---

### Knowledge Management & Documentation

**Principle:** Treat documentation as a *product*, not a *project artefact*. It
must outlive the project that produced it.

**Do:**
- Apply **Products over Projects** — keep the doc team stable, give the
  docs a backlog, a roadmap, and on-call rotation.
  *Ref: Communication Patterns.md — "Products over Projects" (`page-135-0`).*
- Use **abstractions over text**: lists, tables, charts, word clouds — pick
  the most compact form for each fact.
  *Ref: Communication Patterns.md — "Lists" (`page-140-0`), "Tables" (`page-141-0`), "Charts" (`page-145-0`).*
- Apply **DRY, fractal, and perspective-driven documentation** — same
  concept at multiple zooms; abstractions mirror the codebase.
  *Ref: Communication Patterns.md — "Perspective-Driven Documentation" (`page-146-0`).*
- Just-enough / living documentation — *"document decisions, not
  implementations; capture the 'why', not just the 'what'."*
  *Ref: Communication Patterns.md — synthesized from "Just-Enough Documentation".*
- All documentation as code — store alongside the code it documents.
  *Ref: Communication Patterns.md — "All Documentation as Code" (`page-187-0`).*
- Get feedback early, share the doc load, use non-proprietary formats
  (Markdown, AsciiDoc) — lock-in hurts longevity.
  *Ref: Communication Patterns.md — "Get Feedback Early" (`page-153-0`), "Share the Load" (`page-157-0`), "Nonproprietary Formats" (`page-157-0`).*

**Don't:**
- Don't write a comprehensive wiki no one reads — *"just enough
  documentation"* with the *why* survives; the *what* rots.
  *Ref: Communication Patterns.md — "Just-Enough Documentation" (synthesized).*

---

### Architecture Decision Records (ADRs)

**Principle:** Lightweight, numbered, version-controlled, immutable (supersede
rather than delete).

**Do:**
- Use the standard structure: **Title**, **Status** (Proposed → Accepted →
  Deprecated → Superseded), **Context**, **Decision**, **Consequences**.
  *Ref: Communication Patterns.md — "ADR Structure" (`page-171-0`).*
- Keep them short — 1–2 pages.
  *Ref: Communication Patterns.md — "ADR Best Practices" (`page-178-0`).*
- Number sequentially, store in VCS, link related ADRs, never delete —
  *supersede* with a new ADR pointing to the old.
  *Ref: Communication Patterns.md — "ADR Storage" (`page-179-0`), "ADR Culture" (`page-180-0`).*
- Treat ADRs as negotiation tools — "forces structured thinking before
  advocacy; makes trade-offs visible; creates a shared reference point."
  *Ref: Communication Patterns.md — "ADR (Architecture Decision Records) as negotiation tool" (`page-153-0`).*
- Capture the *consequences* (positive AND negative) — that's where the
  future-you finds out what was actually weighed.
  *Ref: Communication Patterns.md — "ADR Structure" (`page-171-0`).*

**Don't:**
- Don't write an ADR as a one-time obligation that nobody updates; pick a
  status workflow and stick to it.
  *Ref: Communication Patterns.md — "ADR Culture" (`page-180-0`).*

---

### Architecture Characteristics

**Principle:** Define the top-N *architecture characteristics* explicitly per
system — they're the priorities design choices must satisfy.

**Do:**
- Drive characteristics from business goals (not "how we always do it"),
  revisit at every step / per agile cadence.
  *Ref: Communication Patterns.md — "Consider defining architecture characteristics to be an agile process" (`page-185-0`).*
- Make implicit ones (security, operability, observability, …) explicit
  when they affect design choices.
  *Ref: Communication Patterns.md — "Security" (`page-179-0`).*

---

### Remote / Distributed Teams

**Principle:** Async-first by default; reserve synchronous meetings for things
that *require* synchronous discussion.

**Do:**
- Default to *async* written communication; sync only when truly needed.
  *Ref: Communication Patterns.md — "Async to Think" (`page-223-0`).*
- *Document or it didn't happen* — async requires written artefacts.
  *Ref: Communication Patterns.md — "If it is not written down, it didn't happen".*
- *Synchronize time* — protect overlap hours, rotate meeting slots to share
  burden fairly, defend part-time hours, plan for holidays.
  *Ref: Communication Patterns.md — "Synchronize Time" (`page-198-0`), "Split Shifts" (`page-202-0`), "Defend Part-Time Hours" (`page-205-0`), "Plan for Holidays" (`page-206-0`).*
- Video > audio; collaborative whiteboards (Miro, FigJam) for visual
  discussions.
  *Ref: Communication Patterns.md — "Distributed Teams" pattern guidance.*
- Use clear *channel selection* — email for formal/auditable, chat for fast,
  presentations for big-picture, screen-shares for live walk-throughs.
  *Ref: Communication Patterns.md — "Symmetrical Email" (`page-239-0`), "Online Presentations" (`page-244-0`), "Screen Shares" (`page-247-0`).*
- Apply *async enhancements*: clear subjects, decision requests with
  explicit asks & deadlines, appropriate tool choice per conversation.
  *Ref: Communication Patterns.md — "Async Methods" (`page-226-0`), "Enhance Async" (`page-229-0`).*

**Remote-first vs Remote-friendly:**
- *Remote-friendly*: office is the default; remote allowed but at a
  disadvantage.
- *Remote-first*: the office is forbidden or optional; remote is the
  default and the office is the accommodation. Prefer this for new hires
  and geographically-spread teams.
  *Ref: Communication Patterns.md — "Remote-First Versus Remote-Friendly" (`page-230-0`).*

---

### Stakeholder & Negotiation Patterns

**Principle:** Map stakeholders by influence × interest, then tailor.

**Do:**
- Use a regular cadence (weekly/biweekly update) for stakeholders;
  one-page executive summaries; decision logs; explicit feedback channels.
  *Ref: Communication Patterns.md — "Patterns for stakeholder engagement" — synthesized from p.153+.*
- Healthy conflict: *separate people from problem; focus on interests not
  positions; generate options before deciding; use objective criteria*.
  *Ref: Communication Patterns.md — "Patterns for healthy conflict" — synthesized.*
- Use ADRs as the negotiation artefact — *ADR culture* keeps conflict
  productive.
  *Ref: Communication Patterns.md — "ADR Culture" (`page-180-0`).*

---

### Accessibility (Non-Diagram)

**Principle:** Don't disable people by environment. Aim for inclusion.

**Do:**
- Caption / transcribe videos for hearing-impaired.
- Provide alt text on every diagram.
- Respect pronouns, time-zone aware scheduling, regular breaks.
- Auto-generated captions are a starting point, not a finish line.
  *Ref: Communication Patterns.md — "Accessibility" (`page-52-0`).*

---

## Anti-Patterns & Common Mistakes
- **Curse of knowledge / mixing levels of abstraction.** → *fix:* one diagram,
  one abstraction level, one C4 layer.
- **Color overload / rainbow diagram.** → *fix:* ≤ 4 colors, each tied to a
  type, paired with shape / pattern / label.
- **Boxes in boxes in boxes / relationship spiderweb.** → *fix:* ortho
  connectors, line jumps, whitespace, splittable diagrams.
- **Relying on color to communicate.** → *fix:* always pair with shape,
  pattern, or symbol (and include a legend).
- **No legend.** → *fix:* include legend or hyperlinked toggle, or use
  labels in place of legend when possible.
- **Jargon overload / acronym hell.** → *fix:* glossary, simple-language
  pass before publishing.
- **Assumed consensus** (silence = agreement). → *fix:* explicit check-ins,
  paraphrase-and-confirm.
- **Curse of knowledge when reading your own ADRs** — *fix:* have a
  neutral reviewer.
- **Open-ended migration window** — *fix:* tag deprecated; bounded timelines.
  *Ref: Communication Patterns.md — "Migration Time Windows" guidance.*

---

## Decision Heuristics / Checklists
- **C4 layer?** Use Context for mixed audiences; Container for engineers;
  Component for implementers; Code almost never.
- **Color palette?** Always use a color-blindness simulator + a
  contrast-ratio checker on the corporate palette before publishing.
- **Diagram type?** UML when audience knows it; C4 / DFD for broader tech /
  mixed; ArchiMate for EA governance.
- **Document type?** Per purpose — Proposal, Status, Incident, Code review.
- **Sync vs async?** Async by default, sync only when conversation requires
  real-time exchange (e.g., incident triage).
- **ADR?** Decision with trade-offs and consequences → yes, write one.
  (Even "small" decisions accumulate organizational context.)
- **Remote policy?** Prefer remote-first when hiring globally or you have
  flexible talent.

---

## Key Takeaways
1. Audience first — pick the *diagram type* and *level of detail* by who is
   reading it.
2. One diagram, one message, one level of abstraction.
3. Color is *never* the only channel — pair it with shape, pattern, position,
   or label, and test with a color-blindness simulator.
4. Flow goes where the reader expects: top-left start, left → right,
   top → bottom, requests ↔ responses in opposite directions.
5. Stories beat specs — frame technical decisions as narratives with
   characters, conflict, resolution.
6. Combine **ethos + pathos + logos** — credibility, story, and data.
7. Async-first for distributed teams; document or it didn't happen.
8. Knowledge is a product, not a project artefact — give it a backlog,
   owner, on-call rotation.
9. ADRs capture the *why* and the *consequences* — supersede, never delete.
10. Communication has *measurable* cost — invest early or pay later.

---

## Cross-References
- Related: `../Microservices_Up_And_Running.md` (operational diagrams +
  service ownership patterns that pair with the C4 + ADR practice).
- Related: `../Enabling_Microservice_Success.md` (organizational-readiness
  patterns — adopter teams need both this book *and* that one).
- Related: `../Monolith_To_Microservices.md` (migration proposals benefit
  from the Proposal / ADR structure covered here).
- Topic index: `../INDEX.md`
