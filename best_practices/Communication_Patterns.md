# Communication Patterns

**Author:** Jacqui Read (2023, O'Reilly; copyright 2024 Read the Architecture, Ltd.; ISBN 978-1-098-14054-0)
**Topic tags:** `#communication` `#general` `#leadership`
**Language focus:** Language-agnostic — patterns for developers, engineers, architects, BAs, and tech leads
**Sources:** `markdown_output/Communication Patterns/Communication Patterns.md` · `summaries/Communication_Patterns.md`

## TL;DR

Read's book applies the pattern/antipattern vocabulary of software to soft-skills — visual diagrams, written, verbal/nonverbal communication, knowledge management, and remote/hybrid work. Its working definition: *"Successful communication is the art and science of sharing or exchanging ideas and information, using a common set of symbols, signs, or behaviors, resulting in shared understanding"* (Michel Thomas: "get the ball over the net"). Apply these patterns when diagrams feel cluttered, decisions get re-litigated, meetings consume all focus time, distributed teammates can't find context, or stakeholders reject "good" designs.

---

## Best Practices by Topic

### Pattern vs Antipattern Vocabulary

**Principle:** Treat communication as engineering — a pattern is a reusable solution proven effective; an antipattern looks correct but its consequences outweigh the benefits.

**Do:**
- Build a personal vocabulary of named patterns (e.g., *Acceptance Prophecy*, *DRY Perspectives*, *Minto Pyramid*).
- Recognize antipatterns in existing artifacts before they calcify (*Boxes in Boxes in Boxes*, *Acronym Hell*, *Acronym Hell*).
- Pair every "do this" with the "don't" so the cost of getting it wrong is concrete.

**Don't:**
- Treat "soft skills" as innate talent — they're learned patterns you can rehearse.
- Reach for a brand-new pattern in a high-stakes moment; deploy one or two at a time.

*Ref: Communication Patterns.md — "Communication Essentials"*

---

### Know Your Audience

**Principle:** Every artifact and message is designed for *someone*; design for them first.

**Do:**
- List the roles that view each diagram type (developers, architects, BAs, product owners, PMs, customers, support).
- Ask four questions: *What do they want from me? What do I want from them? What is their technical understanding? What level of detail do they need?*
- Consider neurodivergent and non-native-speaker readers.

**Don't:**
- Default to UML or deep technical diagrams when a C4 context or domain story serves the audience.
- Assume developers don't need architecture detail or that executives need every interface signature.

*Ref: Communication Patterns.md — "Know Your Audience"*

---

### Mixing Levels of Abstraction (antipattern)

**Principle:** A diagram should sit at exactly one level of abstraction; mixing them produces diagrams that "don't make sense" (the C4 "software system" sitting alongside its own containers).

**Do:**
- Adopt an explicit abstraction hierarchy (C4: Context → Container → Component → Code).
- Use data flow diagram levels (0–3) with numbered processes (2 → 2.1, 2.2, 2.3) and labelled data stores (A, B, C).
- Split any mixed diagram into separate, single-purpose diagrams.

**Don't:**
- Conflate structure with behaviour in one figure.
- Include implementation details on a context diagram (the LEGO metaphor: show the pirate bay, not the bricks).

*Ref: Communication Patterns.md — "Mixing Levels of Abstraction"*

---

### Representational Consistency

**Principle:** Show the audience how diagrams relate across levels so they don't have to remember.

**Do:**
- Use the dashed-box convention (C4) to mark the system-in-focus across levels.
- Number processes/data stores hierarchically across DFD levels.
- Reference figures by label in body text and hyperlink in docs.

**Don't:**
- Renumber or relabel entities between diagrams without explicit cross-reference.
- Use brittle links to artifacts that may be moved or renamed.

*Ref: Communication Patterns.md — "Representational Consistency"*

---

### Color Overload (antipattern) / Color Purposefully

**Principle:** Color is communication, not decoration — every color must earn its place.

**Do:**
- Limit the palette to the minimum colors needed to convey meaning.
- Group by *type* (UI vs data store vs API vs service) with one color per category.
- Add a legend; never rely on the application default palette (draw.io pastels are not accessible).

**Don't:**
- Use a unique color per component ("explosion of unicorns").
- Trust default corporate palettes to be color-blind safe.

*Ref: Communication Patterns.md — "Color Overload"*

---

### Boxes in Boxes in Boxes (antipattern)

**Principle:** Boxes are a single visual primitive; overloading them with multiple meanings creates cognitive overload.

**Do:**
- Replace boxes with labels, notes, or color/pattern differentiation.
- Merge adjacent boxes that don't need to be separate.
- Use whitespace aggressively; it gives the eye somewhere to rest.

**Don't:**
- Use solid AND dashed boxes to mean different things in the same diagram.
- Let structural diagrams become unlabeled containers of containers.

*Ref: Communication Patterns.md — "Boxes in Boxes in Boxes"*

---

### Relationship Spiderweb (antipattern)

**Principle:** Crossed unlabeled arrows force the audience to decode geometry.

**Do:**
- Use orthogonal (right-angled) arrows for relationships.
- Use *line jumps* (arcs) to clarify non-intersecting crossings.
- Standardize label position (start, middle, or end of relationship) across a diagram.
- Split logging/sidebar services into their own diagram.

**Don't:**
- Allow tools to default to straight diagonals that cross everything.
- Put labels so close together the audience can't tell which arrow they describe.

*Ref: Communication Patterns.md — "Relationship Spiderweb"*

---

### Balance Text

**Principle:** Diagrams are visual; excess text blurs the message.

**Do:**
- Use flowchart annotations and numbered notes with superscript references rather than paragraphs in boxes.
- Convert relational data to tables; convert prose to labels.
- Drop repeated context (e.g., "customer" repeated in every box when the title says it).

**Don't:**
- Treat diagrams as documents with sentences.
- Move clutter to footnotes — *move it out of the diagram*, not into a side-channel.

*Ref: Communication Patterns.md — "Balance Text"*

---

### Relying on Color to Communicate (antipattern)

**Principle:** 4.5% of the population has color-vision deficiency; 1 in 12 men. Add shape, pattern, or position to every color cue.

**Do:**
- Add symbols (plus/minus) and patterns alongside red/green/yellow.
- Use contrast-ratio checkers (WhoCanUse, WebAIM) and simulators (Color Oracle, Coblis, Sim Daltonism, Viz Palette).
- Provide alt text for diagrams in public content.
- Use Atkinson Hyperlegible font, ≥12 pt.

**Don't:**
- Refer to "the red boxes" in narration — describe shape/pattern too.
- Assume projectors/printers will render your color palette as designed.

*Ref: Communication Patterns.md — "Relying on Color to Communicate", "Contrast"*

---

### Include a Legend

**Principle:** A legend is a ramp — those who need it use it; those who don't can ignore it.

**Do:**
- Provide a legend (full, partial, or linked/hideable) on any diagram with notation, symbols, or non-obvious acronyms.
- Use labels instead of a legend when the diagram is simple enough.

**Don't:**
- Assume the audience knows UML, ArchiMate, or your in-house notation.
- Make the legend so dominant it competes with the diagram.

*Ref: Communication Patterns.md — "Include a Legend"*

---

### Appropriate Labels

**Principle:** Diagrams communicate via composition, choice of components, and labels — labels are not optional.

**Do:**
- Label every component and every relationship descriptively.
- Place labels close to their referent with balanced whitespace.
- Use sentence-level text inside diagrams only when nothing else conveys it.

**Don't:**
- Leave relationships unlabeled ("the connector does something").
- Stuff boxes with paragraphs of explanation that should be in a perspective or ADR.

*Ref: Communication Patterns.md — "Appropriate Labels"*

---

### The Big Picture Comes First

**Principle:** Even an audience hungry for detail needs context first; you cannot "see the forest for the trees."

**Do:**
- Order diagrams context-first (Context → Container → Component → Code).
- Pair diagrams with business context, requirements summary, and benefit statements before zooming in.
- Use multi-level DFDs (Level 0/1/2/3) to stage the story.

**Don't:**
- Start a presentation with a level-2 DFD or a component diagram.
- Assume the audience knows your "why" — say it explicitly.

*Ref: Communication Patterns.md — "The Big Picture Comes First", "Narrative"*

---

### Match Diagram Flow to Expectations

**Principle:** Diagrams have a reading direction; align it with the audience's mental model.

**Do:**
- Place the *start* near the top-left or middle-left for L-to-R readers.
- Make request arrows flow left-to-right and responses right-to-left.
- Add a "Start here" label, arrow, or numbered sequence when editing is impossible.

**Don't:**
- Place the start in the bottom-right (the data-flow antipattern Read calls out).
- Make crossing arrows ambiguous between "intersection" and "jump."

*Ref: Communication Patterns.md — "Match Diagram Flow to Expectations"*

---

### Clear Relationships

**Principle:** Relationship style (solid, dashed, dotted; arrowhead type; color) communicates meaning.

**Do:**
- Use dashed lines for logical groupings (e.g., C4 system-in-focus) and solid for hard boundaries.
- Reserve color/pattern for relationship *type* (sync vs async, request vs response, deploy vs runtime).

**Don't:**
- Mix dashed and solid boxes with no semantic distinction.
- Use a single arrow style for everything; relationships are typed.

*Ref: Communication Patterns.md — "Clear Relationships"*

---

### Using Icons to Convey Meaning

**Principle:** Icons can replace text *if* the audience already shares the mental model.

**Do:**
- Use universally recognized play/pause/stop/skip symbols (▶︎ ⏸ ⏹ ⏭).
- Use event-storming shape conventions (orange sticky = domain event, blue = command, etc.).

**Don't:**
- Invent custom icons and assume the audience knows them.
- Use icons that have religious or strong cultural meaning (e.g., specific star shapes).

*Ref: Communication Patterns.md — "Using Icons to Convey Meaning"*

---

### Using UML for UML's Sake (antipattern)

**Principle:** UML is a precise language; use it where precision helps, not where simplicity would serve better.

**Do:**
- Use UML when precision is required (class diagrams for code review).
- Consider lighter alternatives (C4, simple sequence) when the audience is broader.

**Don't:**
- Default to UML because "it's the standard" — every notation choice has a cost.
- Mix UML with non-UML notation in the same diagram without explanation.

*Ref: Communication Patterns.md — "Using UML for UML's Sake"*

---

### Mixing Behavior and Structure (antipattern)

**Principle:** Structural diagrams show what exists; behavioural diagrams show what happens. Mixing them is a single-message violation.

**Do:**
- Keep structural and behavioural diagrams in separate artifacts.
- Use sequence/activity/flow diagrams for behaviour; class/component/deployment for structure.

**Don't:**
- Combine data flow + component layout in one figure.
- Let ER diagrams include process arrows.

*Ref: Communication Patterns.md — "Mixing Behavior and Structure"*

---

### Going Against Expectations (antipattern)

**Principle:** Break conventions only with justification and explicit announcement.

**Do:**
- Honour mental models: red = danger/stop, green = go (or use a +/– symbol alongside).
- If you must innovate (a new notation, a new color), introduce it explicitly and explain.

**Don't:**
- Assume red/green alone is accessible or culturally neutral (red = luck in Asia; green = shade of blue in Japan).
- Use religious or culturally loaded symbols without considering the audience.

*Ref: Communication Patterns.md — "Going Against Expectations"*

---

### Illegible Diagrams (antipattern)

**Principle:** A diagram that the audience can't read is worse than no diagram.

**Do:**
- Pick landscape (16:9 or 16:10) by default for screen/presentation; portrait only when required.
- Use crop-and-zoom in slides when forced to use an oversized portrait diagram.
- Greyscale-print check: do labels and patterns still differentiate?

**Don't:**
- Accept A4 portrait from draw.io/Visio defaults.
- Place small diagrams inside large slide white-space; the audience will tune out.

*Ref: Communication Patterns.md — "Illegible Diagrams"*

---

### Style Communicates (metastyle)

**Principle:** Diagram *style* — sketchy vs solid, hand-drawn vs polished — communicates the stage of thought.

**Do:**
- Match style to intent: sketch for early ideation, polished for sign-off.
- Recognize that the same content in different styles can receive different reactions (the "Nikki/Kaspar" example).

**Don't:**
- Submit a sketch when the audience expects production-ready artifacts.
- Submit polished boxes when you actually want feedback on early ideas.

*Ref: Communication Patterns.md — "Style Communicates"*

---

### Misleading Composition (antipattern)

**Principle:** Honest baseline, scale, and grouping make your visualizations credible.

**Do:**
- Keep chart baselines at 0 unless the chart type demands otherwise (and annotate the deviation).
- Use the same scale on side-by-side charts or explicitly mark the difference.
- Keep logical elements at consistent size unless size encodes meaning.

**Don't:**
- Set baselines at 450 to exaggerate a Cool Party lead (Read's election example).
- Show an ESB physically larger than other services — readers will infer capacity.

*Ref: Communication Patterns.md — "Misleading Composition"*

---

### Create a Visual Balance

**Principle:** Balance (symmetry or asymmetry) is an innate expectation; deliver it.

**Do:**
- Aim for bilateral or approximate symmetry across the canvas.
- Use symmetry at expansion/contraction points (fan-out/in).
- If asymmetric, balance by position, weight/size, and direction (treat the canvas as a seesaw).

**Don't:**
- Cram all elements into one corner.
- Treat "balance" as optional decoration; it affects credibility.

*Ref: Communication Patterns.md — "Create a Visual Balance"*

---

### Simple Language

**Principle:** Complexity in vocabulary is complexity in comprehension.

**Do:**
- Use the 4,000-word-family vocabulary that covers ~95% of English news.
- Define domain terms in a glossary; reuse definitions across the codebase.
- Replace: *acquire → buy*, *toward → to*, *dispatch → send*, *a majority of → most*.

**Don't:**
- Use idioms or sarcasm with neurodivergent or non-native speakers.
- Hide behind jargon; readers will infer you don't know the topic.

*Ref: Communication Patterns.md — "Simple Language", "Neurodiversity"*

---

### Acronym Hell (antipattern)

**Principle:** DFD, SPA, BLT each have many IT meanings — never assume.

**Do:**
- Spell out the acronym in parentheses on first use, then the short form.
- Maintain a glossary in the codebase/wiki and link to it.
- Define acronyms in legends and footnotes of diagrams.

**Don't:**
- Use SCUBA, LASER, RADAR, JCB, BMW without remembering they were once acronyms you had to learn.
- Confuse the curse of knowledge ("everyone knows what DFD means") with audience reality.

*Ref: Communication Patterns.md — "Acronym Hell", "The Curse of Knowledge", "Many Possible Meanings"*

---

### Structured Writing — The Minto Pyramid

**Principle:** Lead with the conclusion; group supporting ideas; descend the pyramid one idea at a time.

**Do:**
- State the key message up front; support it with logical arguments; descend to data.
- One paragraph = one idea ("what + why + how"); ~3–5 sentences.
- Use bullets, tables, and lists where structure beats prose.

**Don't:**
- Order emails the way thoughts arrive (Example 7-1 vs 7-2 in the book).
- Bury the request in background — readers will skim to the end and miss it.

*Ref: Communication Patterns.md — "Structured Writing", "Examples 7-1 to 7-4"*

---

### Syntax of Technical Writing — Strong Verbs, Short Sentences, Precise Paragraphs

**Principle:** Code quality != prose quality, but the same engineering virtues apply.

**Do:**
- Replace *was/happen/be* with specific verbs: *generates, convinces, transforms, raises, inspects*.
- Keep sentences short; paragraphs ~3–5 sentences; the opening sentence carries the message.
- Use parallel grammar in lists; numbers only when order matters.

**Don't:**
- Use *there is / there are* as filler.
- Mix vocabulary for the same concept (application/program/software) without explanation.

*Ref: Communication Patterns.md — "Syntax of Technical Writing", "Strong Verbs", "Short Sentences", "Precise Paragraphs", "Consistent Vocabulary"*

---

### Audience Empathy

**Principle:** Write for the reader's current knowledge, not yours.

**Do:**
- Complete the sentence: *"After reading, the audience will be able to…"*
- Compare new info to what they already know.
- Sequence steps when order is required; use numbered lists.

**Don't:**
- Assume "everyone knows" anything; check.
- Pad with basics the audience already has.

*Ref: Communication Patterns.md — "Audience Empathy", "Tips for Technical Documents"*

---

### Encoding — Acceptance Prophecy

**Principle:** If you believe your audience will accept you, you behave more warmly and they accept you more.

**Do:**
- Be a *social optimist*: assume the room is your friend and will approve of your design.
- Plan for questions, but enter with warmth.

**Don't:**
- Behave coldly because you expect rejection — you'll fulfill the prophecy.

*Ref: Communication Patterns.md — "Using the Acceptance Prophecy"*

---

### Encoding — Giving Your Full Attention

**Principle:** Full attention invites full attention back and improves decoding.

**Do:**
- Eye contact, devices away, pen-and-paper notes (tell the other person if device notes are needed).
- Pause; don't interrupt; clarify; paraphrase.
- Turn off notifications during 1:1s, stakeholder meetings, and presentations.

**Don't:**
- Multi-task visibly while someone is talking.
- Half-listen and then paraphrase incorrectly — worse than not paraphrasing.

*Ref: Communication Patterns.md — "Giving Your Full Attention"*

---

### Encoding — Body Language and Gestures

**Principle:** Body language is a controllable channel — keep gestures inside the chest-to-hips, half-body-width box.

**Do:**
- Use explanatory gestures (hands wide for "large"; pinching for "small").
- Use counting gestures for ordered lists; sweeping hands for "wipe the slate clean."
- Mirror the listener's body language subtly.

**Don't:**
- Stab fingers (power gesture reads as aggression).
- Use gestures outside the box on camera (they exaggerate).
- Skip gestures on audio calls — they change the sound of your voice.

*Ref: Communication Patterns.md — "Using Body Language and Gestures"*

---

### Decoding — Battling Bias

**Principle:** System 1 (fast) biases your decoding; awareness and process slow System 2 down.

**Do:**
- Learn the bias catalog (confirmation, hindsight, groupthink, sunk-cost, halo, anchoring).
- Use ADRs, prompts, and feedback from diverse people to slow decisions.
- Recognize that LLM training data carries the same biases.

**Don't:**
- Trust your first reaction to complex messages.
- Ask only people who share your biases (you'll both be wrong together).

*Ref: Communication Patterns.md — "Battling Bias", "Confirmation bias", "Hindsight bias", "Groupthink"*

---

### Decoding — Being Present (Active Listening)

**Principle:** Active listening is the most efficient decoder — listening noises, body language, paraphrase.

**Do:**
- Listen in full; ask clarifying questions; summarize; check body language for mismatches.
- Watch for verbal/nonverbal mismatch (e.g., "yes" + frown = warning).
- Make decisions on next steps only after summarizing.

**Don't:**
- Fill silences; assume you know what they'll say; insert your rebuttal mid-sentence.

*Ref: Communication Patterns.md — "Being Present"*

---

### Awareness of Cultural Differences

**Principle:** Diversity of *context* (institutions, politics, economics) helps teams; diversity of *personal* traits (culture, language) requires care.

**Do:**
- Research or ask about culturally-specific norms (eye contact, hierarchy, disagreement style).
- Foster relationships with offshore teams; sponsor shared understanding.

**Don't:**
- Treat culture as a non-issue because your team is "international."
- Equate disagreement with rudeness; recognize it as a cultural style.

*Ref: Communication Patterns.md — "Awareness of Cultural Differences"*

---

### Influence and Persuasion

**Principle:** Persuasion is a process, not an event — align goals first, then deploy techniques.

**Do:**
- Do discovery first; align your proposal to the audience's goals.
- Use a headline statement, a credibility statement (10s networking / 60s conference), and concrete benefits.
- Pre-empt objections with trade-off analysis; pause, repeat, clarify when questioned.

**Don't:**
- Try to persuade before demonstrating you've understood the problem.
- Use *try, maybe, hopefully* — they undercut conviction.

**Techniques catalog (from Read):**
- *Reciprocity:* give first.
- *Thoughtful pauses:* silence fills with agreement.
- *Give options:* not yes/no; people are happier with chosen options than with many options.
- *Repetition:* repeated claims feel true.
- *Cognitive reframing:* change the perspective on a problem.
- *Redefining:* move audience from their concern to your priority.

*Ref: Communication Patterns.md — "Influence and Persuasion"*

---

### Ethos (Credibility) — Establish Credentials

**Principle:** Build credibility by *showing* it, not announcing it.

**Do:**
- Mention relevant prior outcomes in meetings, not job titles.
- Cite trustworthy sources (academic, government, professional) and link online sources via Wayback Machine.
- Be transparent about motivations, biases, and conflicts of interest.

**Don't:**
- Name-drop companies/brands — describe outcomes.
- Hide a conflict of interest; declare it up front or just before the relevant section.

*Ref: Communication Patterns.md — "Establish Your Credentials", "Use Trustworthy Sources", "Be Transparent", "Bias and Conflict of Interest"*

---

### Pathos (Emotion) — Tell a Story

**Principle:** Stories are how humans accept and remember; use them liberally.

**Do:**
- Use success stories (others' wins), failure stories (lessons learned), use-case scenarios, and clarity stories (past → turning point → now → future).
- Speak from the heart; use concrete examples, even personal vulnerability.

**Don't:**
- Make up stories or pass off anecdotes as true.
- Bury the audience in data when a single well-told story would land harder.

*Ref: Communication Patterns.md — "Tell a Story", "Speak from the Heart"*

---

### Pathos — Vivid Language and Imagery

**Principle:** Sensory, concrete, comparative language is more memorable.

**Do:**
- Use metaphors (X *is* Y), similes (X *is like* Y), analogies (X is like Y, because…).
- Use personification (*the server was begging for a break*), hyperbole (*older than the internet*), strong action and emotional words.
- Show visuals (photos, videos, GIFs, physical props — Jules May's quantum-computing balls and sticks).

**Don't:**
- Choose precision-less abstractions when a vivid image will land.
- Use imagery that offends or excludes.

*Ref: Communication Patterns.md — "Use Vivid Language and Strong Imagery", "Metaphors, Similes, and Analogies"*

---

### Logos (Logic) — Data, Connections, Reasoning

**Principle:** A persuasive argument needs facts, structure, and explicit reasoning.

**Do:**
- Cite data sources (footnotes, parentheticals, or Wayback-Machine-preserved links).
- Use transition words (*therefore, consequently, in conclusion*).
- Use trade-off analysis and ADRs to expose counter-arguments before they happen.
- Maintain a FAQ in your artifact to preempt recurring objections.

**Don't:**
- Present data without a source or reasoning.
- Assume connections are obvious; draw the dot-to-dot for the audience.

*Ref: Communication Patterns.md — "Use Data and Facts", "Make Logical Connections", "Use Reasoning and Argumentation", "Example 9-2 ADR structure"*

---

### Products over Projects

**Principle:** Knowledge lives longer than projects; organize by product to outlive the people.

**Do:**
- Centralize a documentation portal indexed by product; tag with project and artifact type.
- Use metadata (YAML front matter) to make artifacts searchable by product, project, author, type.
- Apply tags + flat structure rather than deep folder hierarchies.

**Don't:**
- Bury knowledge in project folders that get archived when the project ends.
- Use only folder hierarchies; one artifact often belongs in multiple contexts.

*Ref: Communication Patterns.md — "Products over Projects", "Project Mindset", "Product Mindset", "Example 10-1 YAML metadata"*

```yaml
---
product: "My Cool Product"
author: "Kate"
project: "Project Trilby"
type: "requirements"
tags:
 - tag1
 - tag2
---
```

---

### Abstractions over Text

**Principle:** Pictures > words for cognitive load; lists, tables, visuals, and abstractions beat paragraphs.

**Do:**
- Use bullet lists (parallel grammar; ~same length per item; order with numbers only when order matters).
- Use tables for relational or repeatable data; introduce them with a colon-ended sentence.
- Use stars (out of 5) or Harvey balls (clockwise fill) for ratings; place positionally (red top, green bottom) and add symbols.
- Use word clouds, infographics, and image/illustration/video where they add value.

**Don't:**
- Use tables for one-off content; use paragraphs.
- Use more than 5 stars — the meaning blurs.

*Ref: Communication Patterns.md — "Abstractions over Text", "Lists", "Tables", "Visual Abstractions", "Word Clouds", "Other Abstractions"*

---

### Perspective-Driven Documentation

**Principle:** A *perspective* is a curated set of artifacts addressing one stakeholder's concern.

**Do:**
- Define perspectives collaboratively between stakeholder and author.
- Use templates/checklists per concern (security, scalability, operability).
- Make perspectives *fractal* (one perspective embeds another) and *DRY* (no copy-paste).

**Don't:**
- Treat long-form documents as the only documentation format.
- Duplicate artifacts across perspectives — embed/reference instead.

*Ref: Communication Patterns.md — "Perspective-Driven Documentation", "DRY Perspectives", "Fractal Perspectives", "Layering Diagrams"*

---

### Get Feedback Early and Often (anti-Sunk-Cost)

**Principle:** The longer feedback waits, the higher the cost of change; get it on small chunks.

**Do:**
- Use the smallest meaningful feedback loop (PRs, ADR drafts, daily stand-ups).
- Assign IDs to assumptions; explicitly document what you couldn't get sign-off on.
- Ask for feedback from people *outside* your project to escape echo chambers.
- Use the *Consultation* section of an ADR to capture input.

**Don't:**
- Spend three days on diagrams only to find an assumption was wrong.
- Treat sunk-cost bias as a reason to keep going on a bad design.

*Ref: Communication Patterns.md — "Get Feedback Early and Often", "The Sunk Cost Fallacy", "Example 'Feedback Is Part of the Process' at Polyglot Media"*

---

### Share the Load (Roles, Collaboration, Non-proprietary)

**Principle:** One person can't own communication; share by artifact type and reviewer role.

**Do:**
- Use non-proprietary formats (Markdown, AsciiDoc, Git, ODF, draw.io, PNG, PDF, YAML, HTML).
- Use collaboration tools (Google Docs, Teams, Slack, online whiteboards).
- Assign roles by artifact type and ensure an understudy for each.

**Don't:**
- Store institutional knowledge in email — it leaves with the employee.
- Treat proprietary formats (Word .docx, Visio) as durable.

*Ref: Communication Patterns.md — "Share the Load", "Nonproprietary Formats", "Accessibility", "Collaboration", "Roles and Responsibilities"*

---

### Just-in-Time Architecture (YAGNI for docs)

**Principle:** Defer decisions and documentation until the latest responsible moment; defer as long as possible.

**Do:**
- Document only what is needed *now*; update when feedback arrives.
- Combine with *just-long-enough*: retire docs that have served their purpose.
- Record future-relevant ideas in a wiki page so they don't get lost.

**Don't:**
- Predict the future; predictions get revised and chain-update prior artifacts.
- Mistake YAGNI for an excuse to skip best practices.

*Ref: Communication Patterns.md — "Just-in-Time Architecture", "Why Defer Decisions?"*

---

### ADRs — Why, When, Structure

**Principle:** ADRs (Nygard 2011) capture a decision *and* its reasoning, making the "why" durable.

**Do:**
- Write an ADR when the decision affects how developers write code, is hard to reverse, gets revisited, blocks onboarding, or has cross-team impact.
- Use the *Decided* (not *Accepted/Rejected*) status and supersede by ADR-NNN.
- Store ADRs against the *product*, not the project; link from RAID logs.

**Don't:**
- Edit an existing ADR except for status — immutability preserves history.
- Skip the *Evaluation Criteria*, *Options* scoring, *Implications*, or *Consultation* sections.

**ADR Structure (template):**
```markdown
# NNN Title — a statement of the decision made

## Status
Draft / Decided, YYYY-MM-DD / Superseded by ADR-NNN

## Context
Why this decision needs to be made; assumptions, constraints, drivers.

## Evaluation Criteria
What matters; which architecture characteristics apply.

## Options
Each option: per-criterion score + rationale + other trade-offs.

## Decision
What was decided and why.

## Implications
Positive and negative consequences.

## Consultation
Stakeholders invited; advice received (documented last to avoid obscuring the decision).
```

*Ref: Communication Patterns.md — "ADRs", "ADR Structure", "ADR Content", "ADR Storage"*

---

### ADR Storage

**Principle:** ADRs must be discoverable, durable, and link-stable.

**Do:**
- Store ADRs in a central location separate from RAID logs (RAID-D for Decisions; some teams use RAIDD/RAAIDD to capture dependencies separately).
- Fit storage to the team's existing workflow (developers: Git repo; business: wiki/Confluence; cross-team: central portal).
- Track ADR links with dynamic-link tooling (not brittle links) so renames don't break references.
- Run "broken-link checks" in CI; treat a broken ADR link as a defect.

**Don't:**
- Tuck ADRs inside a project folder that gets archived when the project ends.
- Mix ADRs into a generic "decisions" list in a project RAID log.

*Ref: Communication Patterns.md — "ADR Storage"*

---

### ADR Culture — Adoption Tactics

**Principle:** ADRs fail without culture; culture changes through repeated demonstration, not mandate.

**Do:**
- When asked a question, point at the ADR that answers it.
- Create ADRs for past decisions to seed the corpus.
- Use the systems people already use (VS Code for engineers; Notion/Confluence for BAs).
- Add ADR review to onboarding and to the weekly review meeting.
- Treat behaviour change as a multi-month project; don't quit at first resistance.

**Don't:**
- Send a memo announcing ADRs and expecting adoption.
- Make ADRs gate every small decision — that adds red tape and people will bypass.

*Ref: Communication Patterns.md — "ADR Culture"*

### ADR Options Table (with Harvey balls or stars)

**Principle:** A visual scoring table crystallises trade-offs and forces total-score comparison.

**Do:**
- Use one table per option; one row per evaluation criterion.
- Score 0–5 (stars or Harvey balls clockwise).
- Sum the total; list "other trade-offs" outside the criteria.

**Don't:**
- Use prose alone for the options section — readers can't compare at a glance.
- Include only the winning option; show what was rejected and why.

**Example ADR excerpt — ADR-044 Use an Event-Driven Distributed Architecture:**

| Criteria        | Score        | Rationale                                                                                                                                                     |
|-----------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Responsiveness  | ★★★☆☆ 3/5    | [Not inherently performant] but optimizations can be put in place at bottlenecks, e.g. scaling                                                                |
| Maintainability | ★★★☆☆ 3/5    | Dependencies can be an issue, many data stores to maintain                                                                                                    |
| Deployability   | ★★★★★ 5/5    | Deploy only what has changed                                                                                                                                  |
| Scalability     | ★★★★★ 5/5    | Scale on per-service basis                                                                                                                                    |
|                 | Total: 16/20 | Other Trade-offs<br>- Must split data into [one data store per service]<br>- Costs are usually high for building<br>- Complex and is hard to create workflows |

*Ref: Communication Patterns.md — "ADR Content", "Example 12-1 ADR structure", "Figures 12-3 to 12-5 ADR-044"*

---

### ADR Culture and Decision-Making Myths

**Principle:** ADRs only work if the team reads and writes them; bake them into rituals.

**Do:**
- Educate by example; make ADRs the answer to recurring questions.
- Use a simple status flow: *Draft → Decided → Superseded by NNN*.
- Review ADRs during onboarding and weekly review meetings.

**Don't:**
- Force complex status fields (Figure 12-2's "Rejected under Review" tree is explicitly *not* recommended).
- Add too much red tape — people will bypass the process.

**Seven decision-making myths Read debunks:**
1. Decision making is linear — *it's iterative*.
2. More choices = better — *paradox of choice* (≤3 options is the sweet spot).
3. The most senior person decides — *the person with the most expertise/impact is the decision owner*.
4. All stakeholders must be involved — *only those whose success depends on it*.
5. Ask for all kinds of feedback — *ask specific, tailored questions*.
6. All stakeholders must agree — *they must commit*, not agree.
7. The decision owner is rational — *biases apply; consult widely to mitigate*.

*Ref: Communication Patterns.md — "ADR Culture", "Decision-Making Myths"*

---

### Architecture Characteristics (formerly Quality Attributes)

**Principle:** Choose ≤7 architecture characteristics (Richards/Ford guidance) to drive every ADR evaluation criterion.

**Do:**
- Treat Feasibility, Maintainability, Security, Simplicity (and Cost) as *implicit* — they don't count toward the seven.
- Track each characteristic with an ID, applicability, source (requirement or analysis), date, and review date.
- Revisit characteristics as the product moves from initial → growth → optimization.

**Don't:**
- Try to optimize everything; "yes" to all characteristics means you prioritize none.
- Forget to evolve characteristics over the product lifecycle.

**Sample characteristic table:**

| ID   | Characteristic  | Applicable to                                                                | Source                                                                          |
|------|-----------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| AC01 | Auditability    | Media Service                                                                | REQ 014 The system will record access and use of all media for analysis         |
| AC02 | Fault-tolerance | Payment Interface, External Media Interface, Customer API, Customer UI       | REQ 025 and REQ 026                                                             |
| AC03 | Extensibility   | External Media Interface                                                     | REQ 029 It should be simple to add a new external media source to the system    |

*Ref: Communication Patterns.md — "Architecture Characteristics", "Table 12-1"*

---

### All Documentation as Code

**Principle:** Subject docs to the same quality gates as code (review, test, build, deploy).

**Do:**
- Store Markdown/AsciiDoc in Git alongside code; review via PR; verify in pipeline.
- Use static-site generators (Docusaurus, MkDocs, Docsify, Backstage, docToolchain) for publishing.
- Use text-to-diagram tools (Mermaid, PlantUML, GraphViz, Kroki) so diagrams diff cleanly.
- Add broken-link and readability tests in the doc CI.

**Don't:**
- Treat AI-generated docs as authoritative — they confidently produce wrong content.
- Mix doc tooling with code tooling in a way that adds a separate workflow.

**Tools Read lists:** static-site generators — Docusaurus, MkDocs, Docsify, Backstage, docToolchain. Doc generators — Doxygen, Swagger, docfx, phpDocumentor, Slate, Magidoc (GraphQL). Diagram tools — Mermaid, PlantUML, GraphViz, Kroki.

*Ref: Communication Patterns.md — "All Documentation as Code", "Technical Documentation", "Automatically Generated Documentation", "Other Documentation"*

---

### Synchronous vs Asynchronous Communication

**Principle:** Remote sync costs more energy than in-person sync (Stanford/Bailenson); default to async.

**Do:**
- Use sync for rapport-building and idea generation.
- Use async for progress reports, feedback on ADRs/docs, and announcements.
- Mix: brief async → sync decision → async follow-up (the *asynchronous sandwich*).
- Hold meetings only when attendees and time zone math justify the cost (10 people × 1 hour = 10 hours of work).

**Don't:**
- Run sync stand-ups when async status updates suffice.
- Hold all-hands meetings to deliver an announcement (use a recorded video).

*Ref: Communication Patterns.md — "Synchronous Versus Asynchronous", "Direction Matters", "Enhance Meetings"*

---

### Async to Think — Advantages and Obstacles

**Principle:** Async gives *built-in silence*; the cost is decoding friction and emoji ambiguity.

**Do:**
- Set the 4 Ws (+ Why) for every async message: *Who, What, When, Wah-wah (what happens if no response), Why*.
- Use the "four-replies rule" — if an email/chat has gone back-and-forth four times, switch to a call.
- Customize emoji or build a team emoji dictionary.

**Don't:**
- Treat Slack/Teams as inherently sync — they are async *if expectations are set*.
- Default to longer video calls; record once and share.

*Ref: Communication Patterns.md — "Async to Think", "Async Advantages", "Async Obstacles", "Setting and Handling Expectations for Async Communication"*

---

### Why Do You Get Zoom Fatigue? (Bailenson, Stanford VHIL)

**Principle:** Four causes — close-up eye contact, constant self-view, restricted mobility, higher cognitive load.

**Do:**
- Reduce face size (exit full-screen), use external keyboard/mouse, turn off self-view after checking framing.
- Use external camera farther away; turn away from the screen for breaks.
- Schedule breaks every 45–60 minutes; higher-energy activities early in the day.

**Don't:**
- Stare at full-screen faces for hours.
- Eat lunch at the desk during back-to-back calls.

*Ref: Communication Patterns.md — "Why Do You Get Zoom Fatigue?"*

---

### Time Zones, Dates, Clocks

**Principle:** Specify *recipient's* time zone (or a shared reference like UTC); specify dates unambiguously.

**Do:**
- Use ISO 8601 (2023-11-10) or month-name (10-Nov-2023) — never bare `10-11-2023`.
- Specify a.m./p.m. for hours 1–12 when communicating across cultures that don't use 24-hour clocks.
- Add a "I don't expect a reply outside your working hours" line to email signatures.
- Add multiple time zones to your calendar; use World Time Buddy or World Clock Meeting Planner for cross-time-zone scheduling.

**Don't:**
- Default to your own time zone ("send at 9 a.m.") without context.
- Forget DST — the US/EU offset changes twice a year, on different weeks.
- Use shared mailboxes that mask who's on-call.

*Ref: Communication Patterns.md — "Synchronize Time", "Time Zone", "Daylight Saving Time/Summer Time"*

---

### Empathy and Compromise Across Time Zones

**Principle:** When sync is required and time zones collide, take turns bearing the inconvenience.

**Do:**
- Take turns: if one team works late for one meeting, the other works early for the next.
- Compensate: overtime pay, comp time, expensed meals.
- Record the meeting; ensure absentees have input into decisions.
- Block non-working hours in your calendar on split-shift days.

**Don't:**
- Make the same team member always take the worst slot.
- Schedule a stand-up for someone at 6:30 a.m. just because 9:30 a.m. works for you.

*Ref: Communication Patterns.md — "Empathy and Compromise", "Split Shifts"*

---

### Respect Working Patterns and Part-Time Hours

**Principle:** Different people have different working patterns and part-time hours; defend them.

**Do:**
- Block non-availability in calendars as "Not Available" (no need for detail).
- Schedule meetings within part-timers' working hours.
- Auto-reply during leave; record meetings for catch-up.

**Don't:**
- Assume people are available at the same time as you.
- Penalize part-time workers for not attending optional meetings.

*Ref: Communication Patterns.md — "Respect Working Patterns", "Communicate Availability", "Defend Part-Time Hours", "Example 13-1 Email signature indicating working hours"*

```text
---
I understand that your working hours may differ from mine and I
do not expect a reply outside of your working hours.
My working hours (GMT/BST):
Mon-Thu 9 a.m. to 3 p.m. and 4.30 p.m. to 6.30 p.m.
Fri 10 a.m. to 2 p.m.
```

---

### Plan for Holidays, Geography, and Culture

**Principle:** Public holidays differ by country, region, and even state.

**Do:**
- Maintain a shared holiday calendar.
- Block leave as soon as planned (Pending/TBC is acceptable).
- Make TDD, DRY, factory-method, GDPR/HIPAA/NIST/OWASP expectations explicit for cross-cultural teams.

**Don't:**
- Assume a colleague in another country works on their national holiday — they may shift to match yours.
- Assume designs will be followed to the letter; some cultures improvise.

*Ref: Communication Patterns.md — "Plan for Holidays", "Public Holidays and Observances", "Account for Geography and Culture", "Working with Other Cultures"*

---

### Improve Energy and Productivity

**Principle:** Notifications and meetings are interruptions; schedule for energy, not for time.

**Do:**
- Turn off notifications; batch email processing into low-energy windows.
- Schedule high-cognitive meetings for high-energy hours (late morning, post-lunch).
- Schedule breaks every 45–60 minutes; rotate high-energy activities early in the agenda.
- Use focus-time blocks; mark them *busy* and set chat status.
- Automate repetitive communication (auto-replies, IFTTT/Zapier/Power Automate, bots).

**Don't:**
- Read email while listening to a podcast (your System 1 is already biased).
- Put the hardest decision at the end of a long meeting.

*Ref: Communication Patterns.md — "Improve Energy and Productivity", "Control Notifications", "Automate Tasks", "Work with Others' Rhythms", "Schedule for Energy", "Communicating Focus Time"*

---

### Remote-First vs Remote-Friendly

**Principle:** Remote-first optimises for remote; remote-friendly is office-centric with remote as a perk.

**Do (remote-first):**
- Treat all employees as remote (office workers are just colocated).
- Default to async; record meetings; expect mixed attendance virtually.
- Value output over hours; praise contribution, not proximity.
- Hire for fit, not geography (digital nomads welcome).
- Appoint a Head of Remote.

**Don't (remote-first):**
- Run side conversations that exclude remote attendees.
- Promote visibility (late nights in office) over contribution.

**Remote-friendly traits to avoid:** office-centric decision making; office workers taking meeting rooms while remote workers take Zoom; promotions biased toward office staff.

*Ref: Communication Patterns.md — "Remote-First Working", "Remote-First Versus Remote-Friendly", "Remote-First Benefits"*

---

### Evolving to Remote-First (EA-led change)

**Principle:** Use enterprise architecture techniques (impact analysis, BPM, gap analysis, capability mapping, EventStorming, domain storytelling) to evolve to remote-first.

**Do:**
- Apply remote-first bias to every change.
- Replace hours-based KPIs/OKRs with output-based ones.
- Fund virtual team-building and in-person retreats.
- Reimburse remote-relevant benefits (coworking stipend, home internet) instead of office-only perks.

**Don't:**
- Assume remote-first means remote-only — it's about *equal footing*.

*Ref: Communication Patterns.md — "Evolving to Remote-First"*

---

### Symmetrical Email

**Principle:** Solve email's three problems (variable response habits, unclear channel choice, missing expectations) with a shared communication agreement.

**Do:**
- Use subject-line prefixes: `[URGENT, response required by 1 p.m. CET today]`, `[FYI]`, `[Response required - Gino]`.
- State expected response time in the body too.
- Address each recipient explicitly (To/Cc ≠ implicit permission).
- Specify time-cost: "30 minutes," "5–7 mins to complete," "no more than 30 mins."
- Default to *Reply*, not *Reply All*; turn on *Undo Send*.
- One topic per email; link, don't attach.
- Be polite, concise, proofread; assume good intent.

**Don't:**
- Overuse "urgent" — you'll be the boy who cried wolf.
- Send robotic template prose; make it personal (*you*, *I*); read aloud before sending.

**Example email with explicit per-recipient expectations:**

```
from: kim@polyglotmedia.com
to: gino@polyglotmedia.com
cc: sander@polyglotmedia.com, elissa@glidani.com
subject: [Response required by Friday - Gino] Change of plan for kick-off meeting

Hi Gino, Elissa, and Sander,

The kick-off meeting arranged for next Thursday needs to be moved. Elissa has suggested
Friday at 10 a.m.-12 p.m. CET or 2 p.m.-4 p.m. CET.

@Gino, can you please let me know by 4 p.m. (CET) this Friday which one of Elissa's
suggestions is preferred by you and your team, or any days and times your team can make
it the following Monday or Tuesday if Friday is not possible.

@Sander, this is FYI but please let me know if you have any concerns.

@Elissa please let me know if the availability you gave me for the following Monday
and Tuesday changes.

Kind regards, Kim
```

*Ref: Communication Patterns.md — "Symmetrical Email", "Email Reasons", "Email Expectations", "Email Clarity", "Email Tips", "Avoiding Robotic Language", "Example 15-1"*

---

### Online Presentations and Screen Shares

**Principle:** Online presenting is harder than in-person; double the slides, halve the text.

**Do:**
- Use more slides than in person; advance faster; add visual breaks every 20 minutes.
- Enable presenter mode (picture-in-picture) so facial expressions are visible.
- Use exaggerated gestures and expressions on camera.
- Run polls/Mentimeter/Claper; use emoji reactions and chat for engagement.
- Open with bold statement, statistic, image, or story — *not* an agenda slide.
- End with next steps and a CTA link or feedback request.
- Share finished work full-screen/presentation mode; share work-in-progress in editing mode to invite input.
- Make your cursor visible: large, bright, slow; point for ≥5 seconds.

**Don't:**
- Use *slideuments* (slides that contain everything you'll say).
- Confuse *infodecks* (standalone, presentable as PDFs) with slide decks (audio/visual pairs).

*Ref: Communication Patterns.md — "Online Presentations", "Audience Engagement", "Presentation Content", "Infodecks Versus Slide Decks Versus Slideuments", "Screen Shares"*

---

### Remote Tools and Governance

**Principle:** Audit, evaluate, consolidate. Without governance, entropy plus shadow IT breaks the company.

**Do:**
- Use an application portfolio (table per tool: owner, users, licenses, renewal, cost, rationale, compliance).
- Apply ADRs and architecture characteristics to *tool selection* itself.
- Use a technology radar or technical reference model to categorize tools.
- Use the *strangler fig* pattern to phase out tools.
- Assign tool ownership to *roles*, not people, so reassignment survives turnover.
- Detect shadow IT (Netskope: orgs with 500–2,000 staff use ~800 cloud apps/month, 97% shadow IT).
- Set BYOD policy (Microsoft Intune).

**Don't:**
- Let departments silo-buy overlapping tools.
- Create overly restrictive approval processes — they push people to shadow IT.

**Sample application portfolio extract (from Polyglot Media):**

| App name   | Owner                       | Users                     | Licenses         | Renewal date | Initial outlay | Annual cost | Rationale | Compliance |
|------------|-----------------------------|---------------------------|------------------|--------------|----------------|-------------|-----------|------------|
| Obsidian   | Gino (tech lead)            | Tech dept                 | 50               | 2024-07-01   | $150           | $2,500      | [ADR link]| COMPLIANT  |
| draw.io    | Libby (lead architect)      | Architects, developers    | Free/open source | N/A          | 0              | 0           | [ADR link]| Desktop: COMPLIANT, Browser: NONCOMPLIANT |
| Mattermost | TBD (by end Q4 2023)        | Polyglot Media            | Enterprise       | 2024-02-07   | $200           | $1,750      | [ADR link]| COMPLIANT  |

*Ref: Communication Patterns.md — "Remote Tools and Governance", "Selection Techniques", "Data Proliferation", "Security", "Tool Efficiency", "Tool Governance", "Table 15-1"*

---

### Conflicting and Quiet Signals (nonverbal mismatch)

**Principle:** When words and body disagree, the body is usually telling the truth.

**Do:**
- Watch for "yes" + frown, or silence + crossed arms.
- Probe with clarifying questions when you see a mismatch.

**Don't:**
- Assume everyone signals the same way; cultural norms differ.

*Ref: Communication Patterns.md — "Being Present", "Using Body Language and Gestures"*

---

## Anti-Patterns & Common Mistakes

- **Acronym Hell:** Undefined acronyms (DFD, SPA, BLT) leave audience guessing. *Fix:* glossary + first-use expansion.
- **Boxes in Boxes in Boxes:** Boxes overloaded with multiple meanings. *Fix:* differentiate with color/pattern; merge redundant boxes; replace with labels.
- **Color Overload / Explosion of Unicorns:** A different color for every component. *Fix:* limit palette; group by type; legend.
- **Color Reliance:** Communicating only via red/green. *Fix:* add shapes, patterns, +/– symbols; simulator-test.
- **Confirmation bias / Groupthink:** Reading new info as supporting existing beliefs; harmony over truth. *Fix:* diverse Consultation, commitment-not-agreement, pre-mortems.
- **Curse of Knowledge:** Assuming the audience knows what you know. *Fix:* Glossary; first-use definitions; DDD ubiquitous language.
- **Firehose (informal):** Dumping all information into one artifact. *Fix:* Minto pyramid; one idea per paragraph; multiple diagrams.
- **Going Against Expectations:** Breaking mental models without justification. *Fix:* introduce deviations explicitly; honor cultural norms.
- **Illegible Diagrams:** Portrait orientation; unreadable fonts; small print. *Fix:* 16:9/16:10 landscape; ≥12 pt Atkinson Hyperlegible.
- **Mixing Levels of Abstraction:** Context + containers in one diagram. *Fix:* C4 or DFD level hierarchy; one diagram per level.
- **Mixing Behavior and Structure:** Sequence + component in one figure. *Fix:* separate diagrams.
- **Misleading Composition:** Baseline ≠ 0; mismatched scales. *Fix:* honest baseline; consistent scale.
- **Relationship Spiderweb:** Crossing unlabeled arrows. *Fix:* orthogonal lines; line jumps; standardized label position; split diagrams.
- **Slideuments:** Slides containing all presenter narration. *Fix:* presenter audio + visual slides; separate infodeck.
- **Sunk Cost Fallacy:** Continuing on a bad decision because of past investment. *Fix:* ADR-driven decisions; explicit feedback checkpoints.
- **UML for UML's Sake:** Defaulting to UML when C4 or simpler would serve. *Fix:* choose notation by audience need.
- **Long Email / Attached Document:** Big attachments duplicated for every recipient. *Fix:* link, don't attach; one source of truth.
- **All-Hands Announcement via Meeting:** Using sync time for one-way content. *Fix:* recorded video + written summary.
- **Status via Stand-up:** Eight humans updating each other live. *Fix:* async status updates; reserve stand-up for unblocking.
- **Email as Knowledge Repository:** Knowledge locked in a sender/recipient thread. *Fix:* move to wiki; archive after read.
- **Decision by HiPPO:** Highest-paid-person's opinion wins. *Fix:* ADR with Evaluation Criteria; decision owner != senior-most.
- **Predictive Architecture Over-Documentation:** Designing for imagined future needs. *Fix:* just-in-time architecture + YAGNI.
- **Project-Folder Documentation:** Knowledge dies with the project. *Fix:* organize by product; tag with project as metadata.
- **Status Set:** A tiny paragraph of every possible ADR status (Accepted/Rejected/Deferred/Reviewed/…). *Fix:* three statuses (Draft / Decided / Superseded by NNN).
- **Premature Choice of Standards (UML/ArchiMate for all):** Locks the audience pool to trained specialists. *Fix:* prefer C4, simple sequences, flowcharts; expand the maintainer pool.
- **No-Meeting-Block Violation:** Booking over protected focus time. *Fix:* respect tentative focus blocks; offer alternatives.
- **Color-Vision Blindness Untested Palette:** Using a default palette that collapses in deuteranopia simulation. *Fix:* run Color Oracle / Sim Daltonism / Coblis checks.
- **Idiom-Heavy Writing:** Idioms break for non-native English speakers and some neurodivergent readers. *Fix:* plain language, define terms.
- **Side-Conversation Dominance in Hybrid Meetings:** In-room attendees drown out remote voices. *Fix:* monitor chat; prompt quiet voices; require all-attendees-virtual rule.

---

## Decision Heuristics / Checklists

### Choosing Communication Channel
- Need a decision now, complex? → Sync meeting.
- Need feedback on a draft? → Async (ADR, PR, doc comments).
- One-way announcement? → Async (recorded video, wiki page).
- Time-zone math infeasible? → Async + record meeting for later.
- 4 back-and-forth replies already? → Switch to sync call.

### Choosing Diagram Notation
- C4 for system context, containers, components.
- DFD (level 0–3) for process/data flow narratives.
- UML class for code-level precision only.
- Sequence for behavioural flow with timing.
- Flowchart for decision logic; simple custom for one-off sketches.

### Deciding Whether to Write an ADR
- The decision is hard/expensive to change.
- It changes how developers write code.
- It keeps being revisited.
- It's a candidate for adoption from another team.
- It affects multiple components or teams.
- It's complex or hard to understand.
- It came from an RFC.

### Async Message 4 Ws (+ Why)
- *Who:* who's needed; who must respond.
- *What:* explicit expected response shape.
- *When:* ISO date/time/time zone, accounting for recipient hours.
- *Wah-wah:* what happens if no response by the deadline.
- *Why:* goals — drives the other 4.

### Decision-Making Roles
- *Decision owner:* expertise/impact, not seniority.
- *Consulted:* whose advice matters (recorded in ADR Consultation).
- *Informed:* notified of outcome, no input needed.
- *Committed:* required to commit (not agree) to the outcome.

---

### Pre-Meeting Checklist (Sync)
- Goal stated and tied to activities.
- Agenda + timings sent; documents linked and access verified.
- Right attendees only — and a fallback contact for each missed role.
- Car park / parking lot technique for tangent topics.
- Decision owner and note-taker identified.
- Recording permission set; out-of-office attendees looped in async before/after.
- Breaks every 45–60 minutes for sessions over an hour.

---

### Async Channels — When to Use Each
- **Email:** formal, external, long-form, or when no other channel exists.
- **Instant messaging (Slack/Teams/Mattermost):** quick coordination; set expectations to keep it async.
- **Prerecorded video / audio:** announcements where tone and expression matter.
- **Q&A platforms (Stack Overflow for Teams, Codidact):** knowledge preservation; avoid losing answers in chat.
- **Project management (Jira/Asana/Redmine/Taiga/WeKan):** task assignments, status, dependency tracking.
- **Wikis / KMS (Confluence/Notion/AppFlowy/MediaWiki/XWiki/BookStack/Obsidian):** durable, searchable, linkable knowledge.
- **Surveys and polls:** structured, anonymous feedback when live discussion fails.
- **Whiteboards / collaborative drawing (Excalidraw, draw.io, Mural, Miro):** diagram co-creation, async or sync.
- **Files + comments:** durable feedback on documents; avoid attaching to email.

---

### Hybrid-Meeting Hygiene
- All attendees join virtually (including in-office workers) so the playing field is level.
- Chat and Q&A monitored by a designated moderator.
- Open-ended questions to invite quiet voices.
- Use breakout rooms for parallel work.
- Polls and emoji reactions for low-bandwidth feedback.
- Cursor visible (large, bright) for at least 5 seconds per focus point.

*Ref: Communication Patterns.md — "Enhance Meetings", "Async Methods"*

---

### Reducing Sync Meetings — Practical Tactics
- Replace stand-up with async status updates in the project / KM tool; keep stand-up only for unblocking.
- Trial no-meeting blocks/days; only required meetings survive.
- Cut meeting length by 10–15 minutes; ask attendees to leave when the goal is hit.
- Run retros asynchronously; share shortlist at a brief sync.
- Move prework (reading, voting, brainstorming) to async; use meeting for decisions.
- Make a "right to be left alone" rule: if your topic doesn't need the team, send a message instead.

*Ref: Communication Patterns.md — "Reducing Synchronous Meetings"*

---

### Notification and Focus Discipline
- Turn off notifications during deep work; batch email at low-energy times.
- Use focus-time blocks: book as busy/working elsewhere; mark chat status.
- Configure filtered notifications (Teams/Slack) for must-respond senders.
- Archive rather than folder: keep one inbox; move only true exceptions to folders.
- Unsubscribe ruthlessly; route low-value email straight to junk via filter.
- Use IFTTT/Zapier/Power Automate to glue notifications across tools.

*Ref: Communication Patterns.md — "Control Notifications", "Communicating Focus Time", "Automate Tasks"*

---

### Tool Selection ADR (Apply Architecture Process to Tools)
1. Document context: why the tool is needed, decision drivers, assumptions, constraints.
2. Define evaluation criteria from your architecture characteristics + business fit + security + cultural fit (Gino's addition at Polyglot Media).
3. Score 2–4 options with stars or Harvey balls.
4. Document trade-offs beyond the criteria.
5. Decide; record implications; consult stakeholders; supersede when changed.

Apply MoSCoW prioritization (must / should / could / won't) on requirements.

*Ref: Communication Patterns.md — "Selection Techniques", "Example 'Selecting for Cultural Fit'"*

---

### Five-Question Async Message Template (5 Ws)
```
Who:       @person (responsibility); @person (FYI only)
What:      Action requested; format expected
When:      ISO 8601 date, time, time zone
Wah-wah:   What happens if no reply by deadline
Why:       Why this matters (the goal)
```

*Ref: Communication Patterns.md — "Setting and Handling Expectations for Async Communication"*

---

### Recognize Real Working Capacity
- An 8-hour day is rarely 8 productive hours; subtract meetings, email, time sheets.
- Estimate per-sprint capacity from real productive hours, not nominal hours.
- For multi-time-zone colleagues, factor their energy windows (low: ~3 p.m.; high: late morning + ~6 p.m.).
- Use meeting-booking tools (Cal.com, Easy!Appointments, Microsoft Bookings) to avoid scheduling ping-pong.

*Ref: Communication Patterns.md — "Recognize Real Working Capacity", "Book Meetings Efficiently", "Work with Others' Rhythms"*

---

### ADR Adoption Maturity Model
- **Level 0 — Ad hoc:** No ADRs; decisions live in chat/email/people's heads.
- **Level 1 — Mandated:** ADRs required by process; often incomplete or boilerplate.
- **Level 2 — Consulted:** Stakeholders actually contribute via Consultation section.
- **Level 3 — Read:** New team members onboard by reading ADRs; decisions rarely revisited.
- **Level 4 — Living:** Architecture characteristics evolve; ADRs get superseded; trade-offs reusable across products.

*Ref: Communication Patterns.md — "ADR Culture"*

---

### Polyglot Media Lessons Learned (Running Case Study)
The book's recurring case study illustrates several pitfalls and recoveries:

- **Distributed ball of mud:** Migrating from monolith → serverless functions created a *serverless pinball* (functions calling many other functions). Lesson: serverless is not a silver bullet; coupling must be reduced.
- **Strangler fig migration:** Used to migrate without halting new functionality development.
- **Inverse Conway maneuver:** Restructured teams so the communication structure produces the desired architecture (functions composed into larger services, one cross-functional team per service).
- **Event-driven follow-on:** ADR-044 records the move from serverless to event-driven with a Harvey-ball-scored options table (microservices 16/20, service-based 14/20, event-driven 17/20). Drivers: responsiveness, maintainability, deployability, scalability.
- **Team Topologies adoption:** Stream-aligned teams own services end-to-end; integrators/disintegrators shape service boundaries.

*Ref: Communication Patterns.md — "Lessons Learned at Polyglot Media", ADR-044*

---

### Email Subject-Line Prefix Catalog
Standardize subject prefixes so receivers triage in one glance:
- `[URGENT, response required by …]` — only for real urgency (don't cry wolf).
- `[FYI]` — informational only; no action.
- `[Response required - Name]` — single recipient expected to reply.
- `[Action required by Date]` — multiple recipients, deadline-bound.
- `[DECISION REQUIRED]` — final call needed.
- `[DRAFT - DO NOT FORWARD]` — mark pre-decisional artifacts.

*Ref: Communication Patterns.md — "Email Expectations"*

---

### Knowledge Graph and Tags
- A knowledge graph (Obsidian, Logseq, Notion backlinks) improves discoverability over folders.
- Use tags for cross-cutting classification; use folders only for top-level organization.
- Add YAML front matter for searchable metadata (product, project, type, author, dates).
- One artifact, many perspectives: embed rather than copy.

*Ref: Communication Patterns.md — "Implementing Perspectives", "Knowledge graphs"*

---

### Technology Radar for Tool Communication
- Use a Thoughtworks-style radar to categorize tools across quadrants (techniques, tools, platforms, languages & frameworks) and rings (Adopt, Trial, Assess, Hold).
- Provide a text/searchable version in addition to the visual.
- Update the radar on a fixed cadence (quarterly is common) so it remains a trusted reference.
- Reference ADR links from each radar entry; rationale for Hold/Adopt decisions should be one click away.

*Ref: Communication Patterns.md — "Technology radar"*

---

### Question Quality Heuristics
- Open-ended questions invite stories and detail ("What were you working on when…?").
- Closed questions get quick answers; useful for status ("Did the build pass?").
- Rhetorical questions can frame a section but shouldn't be answered in the same breath.
- Clarifying questions in persuasion: a quiet "What recovery time objective were you looking to achieve?" buys time and signals expertise.

*Ref: Communication Patterns.md — "Influence and Persuasion"*

## Key Takeaways

1. **Communication is a learned pattern set, not innate talent.** Practice one pattern at a time until it becomes natural.
2. **Know your audience before you draw a line.** Match notation, abstraction level, and depth to the roles viewing the artifact.
3. **Lead with the picture, then the details.** Big-picture-first prevents "can't see the forest for the trees."
4. **Aristotle's triangle still works.** Ethos (credibility) + Pathos (story) + Logos (data, structure) wins arguments.
5. **Write ADRs by default.** They outlive the people who made the decision and end "whack-a-mole" revisits.
6. **Defer architectural decisions and documentation until the latest responsible moment.** YAGNI + just-in-time reduces rework.
7. **Async by default; sync only when justified.** "Ten people in a one-hour meeting = ten hours of work."
8. **Make all employees feel equal, regardless of location.** Remote-first treats office workers as just-colocated.
9. **Specify time zones, dates, and deadlines unambiguously.** ISO-8601 and recipient-time-zone prevent silent confusion.
10. **Boring is fragile; entropy is real.** Audit your toolset and your diagrams regularly; the default state is chaos.

---

## Cross-References
- Related: [[../Microservices_Up_And_Running.md]] — service boundaries benefit from ADR-driven decisions.
- Related: [[../Software_Architecture_Hardparts.md]] — trade-off analysis depth.
- Related: [[../Team_Topologies.md]] — stream-aligned teams + product over projects.
- Topic index: [[../INDEX.md]]