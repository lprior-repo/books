# Platform Engineering: A Guide for Technical, Product, and People Leaders

**Authors:** Camille Fournier, Ian Nowland, with Michelle Garcia, Heidi Waterhouse, Kassandra Perlongo
**Topic tags:** `#general` `#platform` `#leadership` `#product`
**Language focus:** language-agnostic
**Sources:** `markdown_output/Platform_Engineering_Camille_F/Platform_Engineering_Camille_F.md` · `summaries/Platform_Engineering_Camille_F.md`

## TL;DR
Platform engineering is the discipline of building internal tools, services, and infrastructure that enable product teams to ship software more efficiently. The book's central thesis: **platforms should be treated as products with internal customers**, and success requires balancing three pillars — technology, product management, and people leadership. Apply when designing or scaling an Internal Developer Platform, when adoption of existing tooling is low, or when building a new platform team.

---

## Best Practices by Topic

### What Platform Engineering Is — Leverage, Not Just Tooling

**Principle:** Platform engineering is the discipline of building internal tools, services, and infrastructure that enable product development teams to ship software more efficiently. The key differentiator from infrastructure engineering, DevOps, or SRE: **treating the platform as a product with internal customers.** The goal is *leverage* — a small platform team amplifying the productivity of a much larger number of product developers.

**Four types of platforms (commonly):**
- **Compute / deployment platforms** — how code gets built, deployed, run.
- **Data platforms** — data infrastructure and tooling.
- **Networking platforms** — connectivity, DNS, load balancing, security.
- **Developer experience platforms** — unify the development workflow.

**Do:**
- Build for leverage. The platform must multiply the productivity of product engineers, not just exist.
- Apply the discipline where cognitive load is the binding constraint.

**Don't:**
- Don't conflate "platform engineering" with "infrastructure team renamed." Infrastructure teams take tickets; platform teams build leverage.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 1. Understanding Platform Engineering"*

---

### Why Now — Drivers

**Principle:** Key drivers:
- Increasing complexity of cloud-native infrastructure (Kubernetes, containers, cloud services).
- Unsustainable expectation that every developer be an infrastructure expert.
- Cognitive-load problem (Team Topologies framing).
- Success of large tech companies that invested heavily in internal platforms.

Platform engineering represents the maturation of DevOps: from "you build it, you run it" to "we build the platform, you use it to build and run."

**Do:**
- Use these drivers to justify platform investment to leadership.
- Tie platform work to the cognitive-load problem.

**Don't:**
- Don't position platform engineering as a replacement for DevOps; it's an evolution.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 2. Why Platform Engineering, Why Now?"*

---

### Technical Building Blocks — Self-Service, Paved Road, IDP

**Principle:** Core technical components:
- **Infrastructure abstraction layers** that hide complexity from developers.
- **Self-service provisioning** — developers get what they need without filing tickets.
- **Golden paths / paved roads** — opinionated, well-supported default approaches. "The goal is not to prevent developers from doing things differently, but to make the standard path so smooth that most teams naturally choose it."
- **Internal developer portals (IDPs)** like Spotify's Backstage — unify access to tools and services.

**Three characteristics of a sound platform offering (paraphrased from the book):**
1. **Self-service:** access, provisioning, configuration via UI or CLI.
2. **Defaults with escape hatches:** easy for novices; power users can reach the building blocks.
3. **User observability:** telemetry that lets developers debug their own problems.

**Do:**
- Provide both UI and CLI; developers want automation-friendly interfaces.
- Make the paved road optional, but so good that most teams choose it.
- Build user observability into the platform — debuggability for self-service.

**Don't:**
- Don't force adoption. "The paved road should be optional — forcing adoption breeds resentment, while building something genuinely useful drives organic adoption."
- Don't add an IDP because Backstage is shiny. "Integrating the majority of platform use cases that would make it worthwhile is going to be a lot of work, and arguing 'look at what the shiny UI could do someday' is not going to reduce that work."

*Ref: Platform_Engineering_Camille_F.md — "Chapter 3. Technical Building Blocks"*

---

### Architecture and Design Principles

**Principle:** Key technical principles:
- **Build composable, modular systems** rather than monolithic platforms.
- **Provide APIs and CLIs**, not just UIs — developers want automation-friendly interfaces.
- **Design for multi-tenancy** from the start.
- **Invest in observability** as a first-class concern, not an afterthought.
- **Embrace gradual migration** — you cannot flip a switch and move everyone to a new platform.

**Do:**
- Default to composable systems. Monolithic platforms become bottlenecks.
- Design multi-tenancy up front — retrofitting is expensive.

**Don't:**
- Don't build a "platform" that is really just a set of point tools with no coherent product vision. "A true platform provides integrated, well-documented workflows, not just point solutions."
- Don't promise big-bang migrations.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 4. Architecture and Design Principles"*

---

### Technology Choices — Established Beats Cutting-Edge

**Principle:** Practical guidance on technology selection:
- Prefer established, widely-used tools over cutting-edge for core infrastructure.
- Evaluate the ecosystem and community, not just the technology itself.
- Consider team's existing expertise and the hiring market.
- Be cautious about technologies requiring deep expertise (e.g., Kubernetes).
- Consider managed Kubernetes offerings (EKS, GKE, AKS) before self-hosted.

**Kubernetes specifically:** It's the de facto standard for container orchestration, but its complexity makes it a poor fit for many organizations. The book is explicit: Kubernetes can be a wrong choice.

**Do:**
- Default to managed services for core infrastructure.
- Evaluate the ecosystem and hiring market around a technology.

**Don't:**
- Don't run Kubernetes for the resume. "Be especially cautious about technologies that require deep expertise to operate."

*Ref: Platform_Engineering_Camille_F.md — "Chapter 5. Technology Choices"*

---

### Product Management for Platforms

**Principle:** Platform teams need product management disciplines:
- **User research** — understand actual workflows and pain points.
- **Roadmap planning** — balance new features, tech debt, and maintenance.
- **Prioritization frameworks** — make tradeoffs when you can't do everything.
- **Communication** — keep stakeholders informed about what's coming and why.

**Internal platforms compete for attention with external-facing work.** Platform teams must articulate value in business outcomes, not just technical elegance.

**Do:**
- Treat platform PM seriously. Hire or assign a product manager.
- Frame platform value in business terms.
- Apply user research to internal customers (just like external product teams).

**Don't:**
- Don't add a product manager and call it a day. The team needs to spend more time with customers, more time strategically planning — fewer tickets, slower visible pace, better outcomes.
- Don't build based on the engineers' whims. "Project leaders assume that 'if you build it, they will come.' But even for internal projects, you can seldom guarantee eager adoption if you don't spend time with the target users and understand their needs."

*Ref: Platform_Engineering_Camille_F.md — "Chapter 6. Product Management for Platforms"*

---

### Developer Experience (DX)

**Principle:** DX is the user experience of the platform. Key principles:
- **Fast feedback loops** — developers know quickly whether changes worked.
- **Clear error messages** — when things go wrong, the platform helps fix the problem.
- **Consistency** — similar workflows work similarly across the platform.
- **Documentation** — discoverable, accurate, includes examples.
- **Measuring DX** — surveys (CSAT, NPS), time-to-first-deploy, DORA metrics.

DX is the entire developer journey from writing code to seeing it running in production — not just UI polish.

**Do:**
- Invest in error messages. "The easier the system is to use, and the better your documentation/self-service/error messages, the more likely it is that the support questions will fall on the 'unusual' side."
- Track time-to-first-deploy as a leading DX indicator.

**Don't:**
- Don't reduce DX to UI polish. The journey includes CI, deploys, observability, incident response.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 7. Developer Experience (DX)"*

---

### Stakeholder Management — Trust, Communication, Saying No

**Principle:** Practical advice for managing relationships:
- **Identify key stakeholders** — who depends on, funds, influences your platform.
- **Build trust through reliability** — fastest way to lose credibility is to break things.
- **Communicate proactively** — roadmaps, changelogs, incident reports.
- **Learn to say "no" gracefully** — with specific techniques for declining requests without damaging relationships.
- **Saying "yes" strategically** — accept requests that align with real business needs.

**Do:**
- Treat stakeholder relationships as a core competency.
- Use specific scripts and frameworks for difficult conversations.

**Don't:**
- Don't say "yes" to every request. That leads to bespoke implementations and over-customization.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 8. Stakeholder Management"*

---

### Organizing Platform Teams — Four Models

**Principle:** Four organizational models:

| Model | Description |
|---|---|
| **Centralized platform team** | One team owns the entire platform |
| **Platform "team of teams"** | Multiple specialized teams under shared leadership |
| **Embedded platform engineers** | Platform specialists embedded in product teams |
| **Federated model** | Small central team sets standards; platform engineers distributed across the org |

**Recommended evolution:** Start with a small centralized team; evolve toward more distributed models as the organization grows. The right structure depends on organization size, platform maturity, and culture.

**Do:**
- Default to Centralized for early-stage platform teams.
- Evolve to Hybrid / Federated as the org grows.

**Don't:**
- Don't Decentralize from day one. You'll create inconsistency.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 9. Organizing Platform Teams"*

---

### Hiring and Growing Platform Engineers

**Principle:** Platform engineering requires a unique combination:
- Strong software engineering fundamentals.
- Infrastructure and systems thinking.
- Product mindset and empathy for developers.
- Communication and collaboration skills.

**Career concerns:** Platform engineering must not be seen as a "lesser" path compared to product engineering. Provide growth opportunities where work can sometimes feel less visible than product-facing work.

**Do:**
- Hire for the combination of engineering + product + empathy skills.
- Build clear career ladders for platform engineers.
- Recognize and reward platform work publicly.

**Don't:**
- Don't treat platform as a junior rotation. It's a senior skill set.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 10. Hiring and Growing Platform Engineers"*

---

### Culture and Values

**Principle:** Key cultural attributes:
- **Service mindset** — the platform team exists to serve other engineers, not to control them.
- **Humility** — be willing to deprecate or replace your own work when better solutions emerge.
- **Transparency** — open decision-making, public roadmaps, honest communication about tradeoffs.
- **Blameless culture** — especially important for platform teams; failures affect many people.
- **Iterative approach** — ship small, learn fast, not big-bang launches.

**Do:**
- Reward service and humility, not control and gatekeeping.
- Run blameless postmortems on platform incidents.
- Make roadmaps public.

**Don't:**
- Don't fall into the "platform team superiority complex." "Where platform engineers view themselves as more sophisticated than product engineers. This attitude destroys trust and adoption."

*Ref: Platform_Engineering_Camille_F.md — "Chapter 11. Culture and Values"*

---

### Strategy — Vision, Strategy, Tactics

**Principle:** Three layers:
- **Vision** (long-term) — desired future state. Aspirational but specific. Example: "developers can provision any environment they need in under two hours."
- **Strategy** (medium-term) — key obstacles and approaches to overcome them.
- **Tactics** (short-term) — concrete plans and projects.

Align with company-level strategy and objectives.

**Do:**
- Write the vision down. Make it measurable.
- Trace tactics back to strategy; trace strategy back to vision.

**Don't:**
- Don't ship tactics without a strategy. Don't ship strategy without a vision.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 12. Strategy"*

---

### Measuring Success — Adoption as Secondary Metric

**Principle:** Metrics to consider:
- **Adoption rates** — are teams actually using the platform?
- **Time to productivity** — how quickly a new team starts using the platform?
- **Developer satisfaction** — CSAT, NPS.
- **Reliability** — uptime, incident frequency, MTTR.
- **DORA metrics** — deployment frequency, lead time, change failure rate.
- **Cost efficiency** — per-developer cost of infrastructure.

**Critical caveat on adoption:** "Be careful about using adoption as anything other than a secondary metric. Instead, think about how you are delivering leverage by understanding who will benefit most from your platform."

The book warns against:
- Adoption as the sole metric (encourages forcing).
- 100% adoption targets (encourages mandated migrations).
- Adoption as a stick to use on customers.

**Focus instead:** Whether product teams are more productive because of the platform.

**Do:**
- Track adoption, satisfaction, reliability, DORA, cost.
- Treat adoption as a *secondary* metric; productivity impact is primary.

**Don't:**
- Don't use adoption as a stick. "The risk of using adoption metrics when you are targeting a captive or nearly captive audience is forgetting to build what people want, and instead building what you think they should want and then forcing them to use it."
- Don't rely on vanity metrics (number of features shipped, lines of code).

*Ref: Platform_Engineering_Camille_F.md — "Chapter 13. Measuring Success"*

---

### Operating the Platform — On-Call, Deprecation, Capacity

**Principle:** Day-to-day operational concerns:
- **On-call and incident management** — platform teams must be reliable; invest in on-call rotation and incident response.
- **Deprecation** — retire old tools and migrate users without disruption.
- **Capacity planning** — understand growth patterns and plan ahead.
- **Security** — vulnerabilities in the platform affect everyone.
- **Compliance** — make compliance easy by building it into the platform.

**Sustainable on-call target:** ~5 pages per week (per Camille). More than that = you've reached critical adoption levels; raise the white flag, restore stability.

**Do:**
- Define critical issue criteria explicitly. Both the type of business impact and the conditions where paging helps.
- Invest in deprecation tooling and processes.

**Don't:**
- Don't accept >5 pages/week as normal. It's a signal to pause feature work.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 14. Operating the Platform"*

---

### Scaling — Technical, Organizational, Communication, Decision

**Principle:** Four dimensions of platform scaling:
- **Technical scaling** — more users, services, traffic.
- **Organizational scaling** — team structure evolves to support more stakeholders.
- **Communication scaling** — information flow as users grow.
- **Decision-making scaling** — governance models for who makes platform decisions.

**Do:**
- Plan for all four dimensions, not just technical scaling.
- Establish governance models before growth forces them.

**Don't:**
- Don't scale technical capacity without scaling communication and decision-making.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 15. Scaling"*

---

### Common Failure Modes

**Principle:** Most common ways platform efforts fail:
- **Building a platform nobody uses** — typically because the team didn't treat it as a product.
- **Over-engineering** — building a grand unified platform before validating real problems.
- **Under-investing in DX** — technically excellent but painful to use.
- **Ignoring organizational politics** — failing to build needed relationships.
- **Forcing adoption** — mandating use before the platform is ready.
- **Neglecting maintenance** — building new features while existing ones decay.
- **One-off bespoke feature requests** — customers get used to providing requirements and waiting, entrenching current architecture and preventing self-service.

**Do:**
- Validate before building. Market research → alpha → beta → GA.
- Invest in DX and maintenance.

**Don't:**
- Don't build grand unified platforms on speculative demand. "If you are struggling to find compelling customer benefits for this offering to encourage adoption, your company may not have real demand for the product."
- Don't accept one-off feature requests without checking the common thread. "If you can't find the common thread in your new feature requests, is the common thread that you haven't made it possible for your customers to solve a class of problems for themselves?"

*Ref: Platform_Engineering_Camille_F.md — "Chapter 16. Common Failure Modes"*

---

### Getting Started

**Principle:** Practical advice for starting:
- Start with a small, focused team addressing a specific, high-value problem.
- Pick a problem universally acknowledged as painful (e.g., deployment).
- Build trust through quick wins before tackling larger initiatives.
- Invest in relationships with early adopters who can become advocates.
- Be patient — building a great platform takes years, not months.

**Do:**
- Pick a universally painful problem first.
- Get early adopters who can advocate.
- Set realistic timelines (years, not months).

**Don't:**
- Don't try to boil the ocean. Start small.
- Don't promise quarterly platform transformations.

*Ref: Platform_Engineering_Camille_F.md — "Chapter 17. Getting Started"*

---

### Identifying Potential Platform Products

**Principle:** Several guidance patterns for evaluating which products to build:

- **Assimilate and expand:** Bring products in-house from external OSS/vendor offerings; once they're stable, expand.
- **Partner to prototype:** Work with a customer team to prototype a real solution; expand based on learnings.
- **Look for products with realistic paths to adoption:** If you can't find compelling customer benefits, demand may not exist.
- **You aren't Google:** Don't build what you don't have to. Many platform efforts succeed by being small and not pretending to be Google-scale.

**Do:**
- Validate demand before building.
- Choose products with natural adoption paths.

**Don't:**
- Don't copy Google's monorepo, Google's Bazel, or Google's Borg. "The bigger the company, the more likely it is that their solutions rely on undocumented internal context."
- Don't build because vendors are selling something. Don't build because other companies are talking about it.

*Ref: Platform_Engineering_Camille_F.md — "Identifying Potential Platform Products"*

---

### Change Budget — Adoption Is Not Free

**Principle:** "Most users have a long list of things on their plate, and adopting a new tool, workflow, or system has to fit into the wider picture of all this work." This is the **change budget** — every adoption competes for the customer's time and attention.

**Do:**
- Plan adoption as a first-class product concern.
- Recognize that adoption cost is part of the product.

**Don't:**
- Don't assume "build it and they will come." "Even for internal projects, you can seldom guarantee eager adoption if you don't spend time with the target users and understand their needs."

*Ref: Platform_Engineering_Camille_F.md — "What's the appetite for immediate adoption?"*

---

### Day-Zero Adoption Strategy

**Principle:** "The highest leverage a successful platform can provide to an organization is by driving velocity for its users, bringing delight to its users, and making its users awesome at what they do. This not only requires bringing a product mindset to building a platform, but also shifting away from the 'build it and they'll come' mindset to a more intentional, focused objective around day zero adoption."

**Do:**
- Plan adoption before launch.
- Identify the carrots that will draw users (efficiencies, SLOs, security, speed).

**Don't:**
- Don't ship first, plan adoption later.

*Ref: Platform_Engineering_Camille_F.md — "Day Zero Adoption"*

---

### Reliability Wins Adoption — Camille's S3 Story

**Principle:** "One of the most-loved platforms Camille's organization developed and launched was an internal version of S3... If this product had been unstable when it was launched, it might not have gotten the immediate wide adoption it did. People love things that just work, especially when they're using them for critical production workloads. Since this platform was built on top of production-hardened components, it was much easier to get to a stable offering."

**Do:**
- Build on production-hardened components when possible.
- Test for performance SLOs before pushing adoption.

**Don't:**
- Don't push adoption before you've done enough performance testing. "When an application would try to migrate, the system would struggle to meet its performance needs, causing latency problems and occasional brownouts."

*Ref: Platform_Engineering_Camille_F.md — "Camille's S3 story"*

---

## Anti-Patterns & Common Mistakes

- **Platform team renamed:** Infrastructure team with new branding. *Fix:* Provide self-service; measure developer NPS; build leverage.
- **Forcing adoption:** Mandating platform use before it's ready. *Fix:* Build something genuinely useful; let adoption be organic.
- **Over-engineering:** Building a grand unified platform before validating demand. *Fix:* Start small with universally painful problems.
- **Under-investing in DX:** Technically excellent but painful to use. *Fix:* Invest in error messages, documentation, fast feedback.
- **Adoption as the only metric:** Drives forcing and competition between platform teams. *Fix:* Adoption is secondary; productivity impact is primary.
- **One-off bespoke requests:** Customers get used to providing requirements, entrenching current architecture. *Fix:* Find the common thread; build self-service.
- **Build it and they will come:** No day-zero adoption strategy. *Fix:* Plan adoption before launch.
- **Platform team superiority complex:** "We know more than product engineers." *Fix:* Service mindset; humility.
- **Captive-audience blind spot:** Adoption metrics with a captive audience → forcing. *Fix:* Build what people want.
- **Burning change budget:** Too many migrations at once. *Fix:* Stage migrations; respect the change budget.
- **Tool sprawl without integration:** Each platform component is a separate tool with separate onboarding. *Fix:* Integrate or accept the integration tax explicitly.
- **Treating dev portal as a strategy:** "Look at what the shiny UI could do someday" is not a strategy. *Fix:* Integrate enough use cases to make the portal worth it, or skip the portal.
- **Copying Google:** Borg, Bazel, monorepo. *Fix:* You aren't Google; your context isn't Google's. Validate demand locally.
- **Ignoring reliability:** Pushing adoption before SLOs are proven. *Fix:* Test first; production-hardened components only.

---

## Decision Heuristics / Checklists

- **When to adopt platform engineering:**
  - Multiple teams doing similar infrastructure work repeatedly.
  - Cognitive load on product teams is high.
  - Every resource requires a ticket.
  - Developer satisfaction (NPS) is dropping.
- **Centralized vs. Federated:**
  - Small org, consistent needs → Centralized.
  - Large org, varied needs → Federated / Hybrid.
  - Default to Centralized; evolve.
- **Build vs. Buy for platform components:**
  - Differentiating capability with no good option? → Build.
  - Commodity capability with mature OSS/vendor? → Buy.
  - Default: don't build what already exists.
- **Is the demand real?**
  - Are there customers asking for this? → Yes, validate.
  - Can you find compelling customer benefits? → If no, don't build.
  - Can you explain the migration cost in user-time? → If you can't, adoption will fail.
- **Adoption strategy:**
  - Voluntary adoption of high-leverage tool → standard product marketing.
  - Captive audience → build what they want first; let adoption be organic.
- **On-call capacity:**
  - >5 pages/week per engineer → pause feature work; restore stability.
- **Day-zero adoption plan:**
  - What is the migration story?
  - What are the carrots (efficiency, SLO, security, speed)?
  - Who are the early adopters / advocates?
  - What is the timeline (weeks? months?)?
- **Product management investment:**
  - No PM → engineers doing PM work inefficiently.
  - Too many PMs for the engineering team → too much product strategy, not enough delivery.
  - Right-sized PM → clear roadmap; balanced feature/tech-debt/maintenance.

---

## Key Takeaways

1. **Treat the platform as a product** with internal customers. The central thesis of the book.
2. **Adoption over mandate.** Forcing teams to use a platform is a sign of failure. Build something so good they choose to use it.
3. **Three pillars:** technology, product management, people leadership. Weakness in any one undermines the others.
4. **Start small.** The path to a great platform begins with solving one real problem really well.
5. **Invest in relationships** — political and interpersonal dimensions are as important as technical.
6. **Measure what matters** — adoption is secondary; productivity impact is primary.
7. **Patience and iteration** — meaningful results take quarters or years, not sprints.
8. **Self-service is essential** for leverage — manual work at scale is not a platform.
9. **Paved road is optional, but should be so good teams choose it.** Forcing breeds resentment.
10. **Don't build what you don't have to.** You aren't Google. Validate demand locally.
11. **Reliability wins adoption.** Build on production-hardened components; test SLOs before pushing adoption.
12. **No shortcuts to operational maturity.** Empower leaders who put trust ahead of adoption.
13. **Change budget is real.** Adoption is not free; it's part of the product.
14. **Avoid the platform superiority complex.** Service mindset; humility; transparency; blameless culture.
15. **The SRE on-call ceiling (~5 pages/week)** signals critical adoption levels — pause feature work, restore stability.

---

## Cross-References
- Related: [[../Team_Topologies.md]] (cognitive load; platform team as Team Topologies type)
- Related: [[../Mastering_Enterprise_Platform_Engineering.md]] (complementary platform engineering perspective)
- Related: [[../Cloud_Application_Architecture_Patterns.md]] (cloud-native patterns the platform must support)
- Related: [[../Technology_Strategy_Patterns.md]] (vision / strategy / tactics for platform investment)
- Related: [[../Learning_Systems_Thinking.md]] (organizational culture; systems thinking for adoption)
- Related: [[../Observability_Engineering.md]] (observability as a first-class platform concern)
- Related: [[../Continuous_Deployment.md]] (CI/CD as paved road)
- Topic index: [[../INDEX.md]]