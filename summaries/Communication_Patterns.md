# Communication Patterns - Jacqui Read

## Comprehensive Summary

---

## Part I: Foundations

### Chapter 1: Why Communication Patterns

**The problem:** Having a great architecture or design isn't enough. If you can't communicate it effectively to stakeholders, teams, and decision-makers, the best design in the world won't succeed. Poor communication leads to:
- Increasing costs from misunderstandings
- Unmet requirements from unclear specifications
- Architectures that don't match intent
- Team friction and disengagement

**The solution:** Communication is a learnable skill with repeatable patterns, just like software design patterns. This book provides a vocabulary and framework for thinking about communication systematically.

### Chapter 2: Communication Fundamentals

**The communication model:**
- **Sender** encodes a message → **Medium** carries it → **Receiver** decodes it
- Noise (distractions, biases, jargon) disrupts at every stage
- Feedback loops verify understanding

**Three modes of communication:**
1. **Written**: Documents, emails, chat, code comments, documentation
2. **Verbal**: Meetings, presentations, conversations, phone calls
3. **Visual**: Diagrams, charts, sketches, whiteboards, presentations

**Audience analysis:**
Before communicating, ask:
- Who is the audience? (technical, business, executive, mixed)
- What do they already know?
- What do they need to know?
- What is their preferred communication style?
- What decision are they trying to make?

**Communication anti-patterns:**
- **Curse of knowledge**: You can't imagine not knowing what you know
- **Jargon overload**: Using technical terms with non-technical audiences
- **Assumed consensus**: Thinking silence means agreement
- **Firehose**: Overwhelming the audience with too much information

---

## Part II: Visual Communication

### Chapter 3: Diagrams and Visual Design

**Why diagrams matter:**
- Visual processing is the fastest cognitive channel
- Complex relationships are easier to see than to read
- Diagrams create shared mental models

**Diagram types:**
- **System context diagrams**: Show system boundaries and external actors
- **Container diagrams**: Show deployable units and their interactions
- **Component diagrams**: Show internal components within a container
- **Sequence diagrams**: Show message flow over time
- **Flowcharts**: Show decision logic and process flow
- **Entity-relationship diagrams**: Show data relationships
- **Network diagrams**: Show infrastructure and connectivity

**C4 Model** (Simon Brown):
- **Context**: System in its environment
- **Container**: Applications, data stores, message buses
- **Component**: Modules within containers
- **Code**: Classes, interfaces, objects (usually auto-generated)

**Diagram design principles:**
- **One diagram, one message**: Don't try to show everything
- **Consistent notation**: Use the same shapes/colors for the same concepts
- **Clear labels**: Every element should be labeled
- **Layout matters**: Left-to-right for flow, top-to-bottom for hierarchy
- **Color for purpose**: Use color to highlight, not decorate
- **Legend**: Always include a legend

**Accessibility in diagrams:**
- Don't rely solely on color to convey meaning (use shapes/patterns too)
- Use high contrast
- Provide text alternatives for screen readers
- Consider color blindness (affects ~8% of men)

### Chapter 4: Documentation

**Patterns for effective documentation:**

**Just-Enough Documentation:**
- Document decisions, not implementations
- Capture the "why," not just the "what"
- Keep documentation close to code (README, ADRs)

**Living Documentation:**
- Documentation that evolves with the codebase
- Auto-generated from code where possible (API docs, schemas)
- Version-controlled alongside code

**Architecture Decision Records (ADRs):**
- Numbered sequence of architectural decisions
- Format: Context → Decision → Status → Consequences
- Lightweight: one page per decision
- Stored in version control

**Audience-specific documentation:**
- **For developers**: API docs, runbooks, READMEs, code comments
- **For architects**: ADRs, trade-off analyses, system diagrams
- **For management**: Executive summaries, risk assessments, cost analyses
- **For operations**: Deployment guides, monitoring runbooks, incident playbooks

---

## Part III: Written Communication

### Chapter 5-7: Written Patterns

**Precise Paragraphs pattern:**
- One idea per paragraph
- Lead with the conclusion, then supporting evidence
- Use active voice: "The service processes orders" not "Orders are processed by the service"

**Consistent Vocabulary pattern:**
- Use the same term for the same concept everywhere
- Create a glossary for domain-specific terms
- Avoid synonyms that create confusion

**Audience Empathy pattern:**
- Write for your reader, not for yourself
- Adjust technical depth to audience capability
- Provide context that the reader needs but you might take for granted

**Written communication for different contexts:**
- **Proposals**: Problem → Options → Recommendation → Next Steps
- **Status updates**: What's done → What's in progress → What's blocked → What's next
- **Incident reports**: Timeline → Impact → Root cause → Remediation → Follow-ups
- **Code reviews**: Specific, actionable feedback; explain why, not just what

---

## Part IV: Verbal and Nonverbal Communication

### Chapter 8: Verbal and Nonverbal Patterns

**Encoding Messages (Sending):**
- **Acceptance Prophecy**: Assume people will be receptive; they usually are
- **Full Attention**: Put away devices, make eye contact, show engagement
- **Body Language and Gestures**: Open posture, nodding, mirroring build rapport

**Decoding Messages (Receiving):**
- **Battling Bias**: Recognize your own biases (confirmation bias, anchoring, halo effect)
- **Being Present**: Active listening—paraphrase what you heard to confirm understanding
- **Cultural Awareness**: Different cultures have different communication norms

**Influence and Persuasion:**
- **Reciprocity**: Give before you ask
- **Social proof**: Show that others have adopted the approach
- **Authority**: Cite credible sources and data
- **Scarcity**: Highlight urgency (but don't manufacture it)
- **Commitment and consistency**: Start small, build up

### Chapter 9: The Rhetoric Triangle

**Ethos (Credibility):**
- Establish your credentials
- Use trustworthy sources
- Be transparent about limitations
- Demonstrate deep knowledge

**Pathos (Emotion):**
- Tell stories (the most powerful communication tool)
- Speak from the heart—show genuine conviction
- Use vivid language and imagery
- Connect to the audience's values and concerns

**Logos (Logic):**
- Use data and facts
- Make logical connections explicit
- Use structured reasoning (deductive, inductive, abductive)
- Present trade-offs honestly

### Chapter 10: Presentations and Storytelling

**Presentation patterns:**
- **Storyboard first**: Outline the narrative before making slides
- **The 10/20/30 rule** (Kawasaki): 10 slides, 20 minutes, 30-point font
- **Rule of three**: Group ideas in threes for memorability
- **Start with why**: Open with the problem/motivation, not the solution

**Storytelling for architects:**
- **Hero's journey**: Current state → Challenge → Journey → Resolution → New normal
- **User stories**: Frame technical decisions in terms of user impact
- **War stories**: Share real incidents to make abstract concepts concrete
- **Future vision**: Paint a picture of the desired end state

---

## Part V: Collaboration and Team Communication

### Chapter 11: Working with Stakeholders

**Stakeholder mapping:**
- Identify all stakeholders and their interests
- Map influence vs. interest grid
- Tailor communication strategy per stakeholder group

**Patterns for stakeholder engagement:**
- **Regular cadence**: Weekly/biweekly updates build trust
- **Executive summaries**: One-page summaries for time-poor stakeholders
- **Decision logs**: Record who decided what and why
- **Feedback loops**: Create explicit channels for feedback

### Chapter 12: Distributed Teams

**Challenges of distributed communication:**
- Time zone differences reduce overlap hours
- Lack of informal communication (hallway conversations)
- Cultural and language differences
- Technology barriers

**Patterns for distributed teams:**
- **Async-first**: Default to written, async communication; reserve sync for complex discussions
- **Documentation as communication**: If it's not written down, it didn't happen
- **Video over audio**: Visual cues matter
- **Overlap hours**: Identify and protect shared working hours
- **Inclusive scheduling**: Rotate meeting times to share the burden fairly
- **Digital whiteboarding**: Use collaborative tools (Miro, FigJam) for visual discussions

### Chapter 13: Negotiation and Conflict

**Patterns for healthy conflict:**
- **Separate people from problems**: Attack the issue, not the person
- **Focus on interests, not positions**: Understand *why* someone wants something
- **Generate options before deciding**: Brainstorm multiple solutions
- **Use objective criteria**: Data-driven decisions reduce emotional conflict

**ADR (Architecture Decision Records) as negotiation tool:**
- Forces structured thinking before advocacy
- Makes trade-offs visible
- Creates a shared reference point

---

## Part VI: Practical Application

### Chapter 14: Architecture Decision Records in Depth

**ADR structure:**
1. **Title**: Short noun phrase describing the decision
2. **Status**: Proposed → Accepted → Deprecated → Superseded
3. **Context**: What is the issue that motivates this decision?
4. **Decision**: What is the change that we're proposing/making?
5. **Consequences**: What becomes easier or harder because of this change?

**ADR best practices:**
- Keep them short (1-2 pages)
- Store in version control
- Number sequentially
- Never delete—supersede with new ADRs
- Link to related ADRs

### Chapter 15: Putting It All Together

**Communication strategy for a new architecture initiative:**
1. **Storyboard** the narrative: Why change? What's the vision? How do we get there?
2. **Map stakeholders**: Who needs to know? What do they care about?
3. **Create artifacts**: Diagrams, ADRs, executive summaries—each tailored to its audience
4. **Build a cadence**: Regular updates, feedback sessions, decision reviews
5. **Iterate**: Communication improves with practice and feedback

---

## Key Takeaways

1. **Communication is a learnable skill with patterns**: Just like software design, effective communication follows repeatable patterns that can be studied and practiced.

2. **Know your audience**: Every piece of communication should be tailored to its specific audience—technical depth, vocabulary, medium, and level of detail.

3. **Visual communication is the fastest channel**: Invest in clear diagrams. One good diagram can replace pages of text.

4. **The Rhetoric Triangle—Ethos, Pathos, Logos**: Combine credibility, emotional connection, and logical argument for persuasive communication.

5. **Document decisions, not implementations**: ADRs capture the "why" at a fraction of the effort of comprehensive documentation.

6. **Storytelling is the architect's superpower**: Frame technical decisions as narratives with characters, conflict, and resolution.

7. **Async-first for distributed teams**: Write things down. If it's not documented, it didn't happen.

8. **Healthy conflict requires structure**: Separate people from problems, focus on interests, use objective criteria.

9. **Accessibility is not optional**: Design diagrams, documents, and presentations that work for everyone, including those with disabilities.

10. **Practice and iterate**: Communication skills improve with deliberate practice. Seek feedback and refine.
