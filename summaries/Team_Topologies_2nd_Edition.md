# Team Topologies, Second Edition (2025) - Comprehensive Summary

**Authors:** Matthew Skelton and Manuel Pais
**Publisher:** IT Revolution Press

---

## Overview

Team Topologies provides a practical, adaptive model for organizational design based on four fundamental team types and three interaction modes. The core thesis is that organizations must design their team structures intentionally to achieve a fast flow of value to customers, leveraging Conway's law rather than being victimized by it. The second edition (2025) adds significant new material including an expanded foreword reflecting on five years of industry adoption, nine detailed case studies in a new appendix, refined concepts around platform groupings, and a more nuanced treatment of cognitive load as a dynamic, evolving concern rather than a static limit.

The book is organized in three parts: Part I establishes the foundational concepts of teams as delivery units and Conway's law; Part II defines the four team types, three interaction modes, and software boundary patterns; Part III focuses on the evolutionary aspect -- how organizations must continuously sense and adapt their team structures over time.

The book is intended for anyone who cares about the effectiveness of software delivery and operations: C-level leaders, managers, heads of department, software and systems architects, and anyone involved in building or running software systems. The authors emphasize that Team Topologies is not a universal formula but rather a set of clear patterns that are straightforward for many organizations to follow and interpret. The analogy they use is instructive: Team Topologies is like printed music parts for an orchestra or big band -- it helps the group succeed but does not dictate every aspect of performance; lots of detail is left for the ensemble to interpret to suit the occasion, venue, or mix of players.

The origin of the book traces back to 2013 when Matthew Skelton devised the original DevOps Topologies patterns in a blog post titled "What Team Structure Is Right for DevOps to Flourish?" Manuel Pais later interviewed Skelton at QCon London in 2015, and together they expanded the DevOps Topology patterns based on community contributions. Over time, they realized that the static view of team interrelationships was useful for initial discussions but limited in scope. Through combined experience with training and consulting across the world, they evolved the ideas into the dynamic, adaptive Team Topologies model presented in this book.

---

## Note on the Second Edition

The second edition introduces a critical clarification: a "platform team" is better understood as a "platform grouping" -- a collection of multiple teams providing a coherent capability. In organizations larger than forty to fifty people, a platform will typically need more than one eight-person team. The concept of a "fractal organization" is central: self-similar patterns repeat at multiple zoom levels, where teams inside a platform grouping are the same types (stream-aligned, enabling, complicated-subsystem, or inner platform teams) as those outside it. The updated Figure 5.1 now shows the platform grouping with dotted lines to indicate it is not a team type in the sense of a single team of around eight people, but instead a kind of "container" for one or more teams.

The authors also introduce "value stream groupings" as a generalization, where a platform grouping is merely a special kind of value stream grouping that provides services to other teams or groupings. For any platform grouping, we can "zoom in" and see the same types of teams and groupings. Conversely, we can "zoom out" and visualize the platform as a single entity. This zooming back and forth between different levels is vital for understanding how Team Topologies platforms work. The Telenet case study in the appendix illustrates a similar approach with their internal and external customer-centric tribes.

---

## Foreword to the Second Edition

The authors reflect on the five years since the first edition. Key real-world results include: EBSCO reported 26% faster feature delivery and over $9 million in cost savings; KFC's digital sales increased threefold; Yassir saw a 230% increase in employee satisfaction. The Norwegian company Capra Consulting applied Team Topologies to their entire organization (including sales, operations, recruitment, and leadership), not just technology teams.

The authors emphasize that team types and interaction modes are building blocks, not an end state. Organizations that adopted a static view of the four types and three modes tended to overlook the importance of continuous evolution. The foreword also stresses that "fast flow" means fast flow of value to customers, not simply fast delivery from idea inception -- organizations must validate that customers actually accrue value.

Several important examples illustrate the breadth of Team Topologies adoption beyond traditional tech companies. The State Treasury of Rio de Janeiro (SEFAZ-RJ) provides over 250 citizen services for 17 million inhabitants. In 2020, they were organized around technical component teams aligned to internal processes. Key citizen user journeys (like tax refunds) spanned multiple business areas, creating a maze of dependencies. By applying an inverse Conway maneuver at both the team and organizational level -- creating a new business area focused on taxpayer citizen services -- they achieved tax refunds in twenty-four hours versus multiple months previously, and drastically reduced citizen complaints. Kodea, an NGO promoting technological inclusion for underrepresented groups in Latin America, selectively adopted patterns from the book despite lacking budget for dedicated platform teams, demonstrating that the principles apply even in resource-constrained environments.

The foreword also discusses how bol.com (a leading Dutch online retailer) scaled their data science capabilities. Rather than centralizing all data science work, they created a structural enabling team of data science leads who sensed organizational needs, plus temporary enabling teams to upskill product teams. Eventually, platform teams around data science were also created, but enabling teams continued to surface new challenges and facilitate emerging practices.

The authors acknowledge how Team Topologies is just one of multiple approaches needed for more humane and effective organizations. They highlight complementary approaches including Jon Smart's Sooner Safer Happier, Heidi Helfand's Dynamic Reteaming, Zhamak Dehghani's "data mesh" concept, and Susanne Kaiser's "Architecture for Flow" which brings together Team Topologies, Wardley Maps, and domain-driven design.

New insights on cognitive load are introduced: the authors collaborated with Dr. Laura Weis to develop a scientific model identifying more than twenty drivers of team cognitive load across four clusters (team characteristics, work practices and processes, task characteristics, and work environments and tools). A river analogy replaces the bucket analogy: cognitive load is dynamic, not a fixed capacity that fills up.

---

## Part I: Teams as the Means of Delivery

### Chapter 1: The Problem with Org Charts

Traditional organizational charts fail modern software delivery in several fundamental ways. They reflect historical power structures rather than communication pathways needed for effective software delivery. Real communication in organizations looks nothing like the hierarchical org chart; actual lines of communication cut across reporting structures in complex webs. Mark Schwartz, author of The Art of Business Possibility, observes that org charts represent "how the organization looked at some time in the past," not how it actually functions today.

The chapter identifies key obstacles to fast flow: bottlenecks where single teams become constraints, excessive cognitive load on teams trying to manage too many domains, and communication structures that encourage monolithic architectures. The authors argue that org-chart thinking leads to handoffs between teams, which introduce delays and miscommunication. When a feature requires work from a front-end team, a back-end team, and a database team, the coordination overhead dwarfs the actual development effort. Moreover, traditional org charts assume a predictability in work allocation that does not exist in collaborative knowledge work filled with uncertainty and novelty.

The authors contrast this with the need for an organization that can reshape itself frequently for collaborative knowledge work. They introduce the concept of a "value stream grouping" -- a collection of teams brought together around a common mission -- and argue that traditional org charts are out of sync with this new reality.

The chapter previews the Team Topologies model: four team types (stream-aligned, enabling, complicated-subsystem, and platform) and three interaction modes (collaboration, X-as-a-Service, and facilitating). The goal is to give organizations the approach and mental tools to dynamically find when collaboration is needed versus when execution focus with reduced communication overhead is optimal. The authors share a fascinating analogy from nature: grouper fish and moray eels, seemingly unrelated species, explicitly collaborate via signals to hunt down smaller fish -- the eel scares fish from crevices, and the grouper catches them as they emerge. Organizations need similar intentional cross-team collaboration patterns.

### Chapter 2: Conway's Law and Why It Matters

Conway's law, formulated by Mel Conway in 1968, states: "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." The modern interpretation is even broader: organizational design prevails over software architecture design. If your organization is structured in silos, your software will be siloed. Conway himself posed the imperative question: "Is there a better design that is not available to us because of our organization?"

The chapter explains the "homomorphic force" -- the pressure exerted by organizational structure on software architecture. A traditional ops team managing shared databases will naturally produce a monolithic shared database architecture, regardless of architectural intent. A database administrator team that controls all database access will produce software where all data access funnels through a single shared database layer. The authors present the "reverse Conway maneuver" as a deliberate strategy: design the team structure you want and let the software architecture follow. This is different from the "inverse Conway maneuver" -- the distinction is that the reverse approach is proactive and strategic, while the inverse is reactive.

Key insights from Conway's law:

- **Communication paths** are the mechanism. The design of the system mirrors the communication paths available to the people designing it. Harvard Business School research by Alan MacCormack and colleagues confirmed that the communication structure of the organization significantly affects the modularity of the software produced.
- **Team-scoped flow** is essential. When a single team owns the full lifecycle of a service (build, test, deploy, operate), the architecture tends toward modularity and loose coupling. Version compatibility between services becomes a team concern, not a cross-team coordination problem.
- **Focused communication** is more valuable than unrestricted communication. Not everyone needs to talk to everyone. Team assignments should be designed to restrict the solution search space productively. Unnecessary communication is wasteful: it consumes time and attention that could be spent on productive work.
- **Naive uses of Conway's law** can be harmful. Simply reorganizing teams without understanding the underlying communication patterns will not improve the architecture. Using log-aggregation tools to force cross-team communication, or treating Conway's law as a simple one-to-one mapping between teams and microservices, misses the deeper point about communication structures.
- **Reorganizations** are a blunt instrument. Simply reorganizing without a clear understanding of the desired communication patterns will not produce the desired architecture. The authors recommend using the reverse Conway maneuver as a more targeted approach.

Practical advice includes: avoid cross-team testing dependencies (testing should be owned by the team that builds the software), design for high cohesion and loose coupling at the team level, treat software architecture as flows of change rather than static structures, and be intentional about which teams need to communicate and which should be isolated from each other. Ruth Malan, quoted extensively, emphasizes that "architecture is about the significant decisions that shape the structure and behavior of a system." By shaping team communication patterns, we shape these decisions.

### Chapter 3: Team-First Thinking

This chapter establishes teams as the primary unit of delivery, not individuals. The authors draw on research from multiple fields to define what makes effective teams. The quote from General Stanley McChrystal's "Team of Teams" sets the tone: the goal is to create organizations with the adaptability and agility of small teams, at enterprise scale.

**Team size and trust:** Dunbar's number suggests humans can maintain meaningful relationships with approximately 150 people, with nested layers of 5, 15, 50, and 150. Effective software teams should be small (5-9 people) to maintain high trust and fast communication. The "onion concept" shows how teams relate to each other in concentric circles of decreasing trust and increasing communication distance. High-trust organizations are more effective because trust reduces the overhead of communication and coordination. Nokia's decline is cited as a cautionary example: research by Jiao Luo and others found that Nokia's organizational structure in the 2000s inhibited the flow of information about smartphone threats, preventing the company from adapting.

**Team lifespans:** Teams should be long-lived, not formed and dissolved around projects. The Tuckman model of forming-storming-norming-performing applies, and dissolving teams wastes the investment in norming and performing. Heidi Helfand, author of "Dynamic Reteaming," provides guidance on how to change team composition without losing effectiveness, but the default should be team stability. Teams need stability to build trust and shared mental models.

**Software ownership:** Teams should own their software systems end-to-end, including production operation. This "you build it, you run it" principle ensures fast feedback loops and alignment of incentives. The authors cite the DORA (DevOps Research and Assessment) research showing that teams with end-to-end ownership deliver software faster, more reliably, and with higher quality.

**Team-first mindset:** This means thinking of the team as the smallest unit of delivery, not the individual. Naomi Stanford's "Guide to Organisation Design" is cited: modern organizational design is about designing for collaborative technologies and the voice of the customer. Organizations should optimize for team autonomy, limit cognitive load per team, and design boundaries around team capabilities. Diversity within teams is important: diverse teams produce better solutions but need psychological safety to function effectively. W. Edwards Deming and Tom DeMarco's work (Peopleware) are cited as foundational influences.

**Cognitive load:** The chapter introduces three types of cognitive load, drawing on John Sweller's Cognitive Load Theory:
- **Intrinsic load:** The inherent complexity of the business domain and technical problem.
- **Extraneous load:** Unnecessary complexity from the environment, tooling, processes, and interactions with other teams. This is the load that organizations should work hardest to reduce.
- **Germane load:** The effort of learning, improving, and developing new capabilities. This is desirable load that teams need time for.

The goal is to minimize extraneous load, manage intrinsic load through appropriate team boundaries, and allocate sufficient capacity for germane load (learning). A team should own no more than one complicated or complex domain. The chapter provides concrete heuristics for domain assignment: relative domain complexity should be assessed (a team working on a "complicated" domain like real-time pricing should not also own a "complex" domain like machine learning), and the number of domains a team handles should be limited based on the complexity of each. Software boundary size should be assessed: if the boundary of what a team owns is too large, it should be split.

**Responsibility restriction:** Teams should have a clear, limited scope of responsibility. The chapter provides heuristics for domain assignment, including the "Eyes On, Hands Off" approach where a team monitors a domain but does not actively develop it unless necessary. Brooks's Law ("adding people to a late software project makes it later") is cited as a reason to restrict team responsibilities rather than adding more people.

**Team APIs:** The authors introduce the concept of a "team API" -- the explicit interface a team presents to other teams. This includes the code repos the team owns, documentation, versioning practices, communication channels (Slack channels, issue trackers), and working hours. The team API should be well-defined, versioned, and stable. The concept is inspired by Spotify's use of "squads" and the idea that teams should have clear interfaces. Examples from Auto Trader and CDL (Cambridge Decision Labs) illustrate how explicit team APIs reduce friction between teams. At CDL, the team API included explicit documentation of what the team owned, how to request work from them, and how they communicated. At Auto Trader, the team API concept helped teams define clear boundaries and reduce cross-team dependencies.

**Workspace design:** Physical and virtual environments should be designed to support team interactions. The "benched bay" approach gives teams dedicated physical spaces. Scott Doorley and Scott Witthoft's "Make Space" is referenced for designing physical environments. Virtual environments should use group chat prefixes (e.g., "#team-checkout-" prefixed channels) to signal team boundaries and reduce noise. Jason Fried and David Heinemeier Hansson's "Remote: Office Not Required" is cited for guidance on remote team communication. The authors argue that both physical and virtual workspace design directly affects team communication and therefore (via Conway's law) software architecture. Communities of practice, guilds, and internal tech conferences provide spaces for cross-team learning and trust building that support effective team interactions.

---

## Part II: Team Topologies That Work

### Chapter 4: Choosing Team Topologies for Fast Flow

This chapter examines static team patterns observed across the industry and provides guidance on which patterns work in which contexts. It serves as a bridge between the conceptual foundations of Part I and the four fundamental topologies of Chapter 5.

**Designing for flow of change:** The authors contrast organizations optimized for siloed control (where each functional area has its own team) with organizations optimized for flow (where cross-functional teams own entire value streams). The key insight is that the flow of change through the organization determines software architecture: teams that own the full lifecycle of a service produce better architectures. The DORA research (documented in "Accelerate" by Nicole Forsgren, Jez Humble, and Gene Kim) shows that high-performing teams have deploy-to-production times measured in minutes or hours, not weeks or months. This requires organizational structures that support fast flow.

**Organizational sensing:** Organizations need mechanisms to detect when team structures are not working. This includes tracking dependencies between teams, monitoring wait times, and observing communication patterns. Spotify relies on a simple spreadsheet to detect and track interdependencies between squads and tribes, highlighting whether a dependency is on a squad within the same tribe (acceptable) or in a different tribe (potentially indicating misaligned team design). Dominica DeGrandis, in "Making Work Visible," recommends using a Physical Dependency Matrix or "dependency tags" on kanban cards to identify and track dependencies. Diane Strode and Sid Huff's 2012 taxonomy of dependencies in agile software development identifies three categories: knowledge, task, and resource dependencies.

**DevOps topologies:** The chapter reviews the DevOps Topologies catalog (originally created by Matthew Skelton) and its evolution. Key successful patterns include:

- **Feature teams / product teams:** Cross-functional teams that own features end-to-end, reducing handoffs and dependencies.
- **Cloud teams:** Teams that provide infrastructure as self-service capabilities, reducing the need for dedicated ops teams.
- **Site Reliability Engineering (SRE):** Google's SRE model where reliability engineers collaborate closely with development teams, with a dynamic relationship that evolves over time based on application scale and maturity.
- **Non-blocking dependencies:** Patterns where teams can proceed without waiting on other teams, typically through self-service capabilities and well-defined APIs.

**Topology choice considerations:** The chapter identifies factors that influence which topology works:
- **Technical and cultural maturity:** Organizations at different stages need different structures. Both Amazon and Netflix had well-established cross-functional teams by 2013, while traditional organizations adopting Agile often lacked mature engineering practices and benefited from temporary DevOps teams with battle-tested engineers.
- **Organization size and software scale:** Larger organizations and software systems benefit from platform teams providing infrastructure as a service.
- **Engineering discipline:** The SRE model requires a high degree of engineering discipline and management commitment.
- **Dependencies between teams and their wait times:** Track dependencies per area and establish thresholds and alerts.
- **Splitting responsibilities to break down silos:** Breaking down responsibilities and empowering other teams to take some on can reduce dependencies. The pattern of separating database development (DB Dev) from database administration (DBA) is cited, where the DBA role becomes part of a platform.

The TransUnion case study (Part 1) shows how an organization evolved its team structures over four years, from a hybrid model with temporary DevOps teams through to fully integrated development and operations teams. Ian Watson, Head of DevOps at TransUnion from 2015 to 2018, recalls how they adopted a hybrid model with two temporary DevOps teams (a "system-build" team and a "platform-build" team) collaborating to bring Dev and Ops together. This evolution took three years longer than initially expected, but the business benefits were clear: safer, more regular production changes, fewer deployment mistakes, and better traceability. By late 2018, the temporary teams had been merged back into Dev and Ops teams, bringing higher levels of operational awareness and accountability.

The Accenture healthcare client case study illustrates a three-stage evolution: starting with a DevOps team that became an anti-pattern (tooling expertise siloed in one team), evolving to closer collaboration between development, operations, and the tooling team, and finally transitioning the DevOps team to an evangelizing role that made itself obsolete.

### Chapter 5: The Four Fundamental Team Topologies

This is the core chapter of the book, defining the four team types that the authors argue are the only topologies needed to build and run modern software systems.

#### Stream-Aligned Teams

The primary team type. A stream-aligned team is aligned to a single, valuable stream of work -- a product, service, set of features, user journey, or user persona. The team is empowered to build and deliver customer value as quickly, safely, and independently as possible, without handoffs to other teams.

Key characteristics:
- **End-to-end ownership:** The team owns the full lifecycle from requirements through production operation.
- **Cross-functional capabilities:** The team includes (or has access to) application security, commercial analysis, design, development, infrastructure, metrics, product management, testing, and UX skills. Not every capability maps to a dedicated individual; the team as a whole must provide them.
- **Close to the customer:** The team receives direct customer feedback and can react in near real-time.
- **Long-lived and funded sustainably:** Not formed around temporary projects.
- **Most teams should be stream-aligned.** The purpose of the other three team types is to support stream-aligned teams.

Different types of streams include customer streams, business-area streams, geography streams, product streams, user-persona streams, and compliance streams. The Amazon "two-pizza team" model is presented as an early example of stream-aligned teams, dating back to Bezos's 2002 mandate that each team be fully responsible for developing and operating its own service through APIs.

The term "stream-aligned" is preferred over "product team" or "feature team" because modern customer experiences span multiple products and devices (mobile, embedded, voice, web). A stream-oriented view better captures the continuous flow of value.

Expected behaviors for a stream-aligned team include: maintaining a stable cadence of delivery, answering to customers, producing telemetry for the software in production, attending to security and compliance, and collaborating with enabling and platform teams as needed.

#### Enabling Teams

An enabling team helps stream-aligned teams acquire missing capabilities. Their mission is to research, try out new tools and practices, and help stream-aligned teams grow. Enabling teams do not do the work themselves; they multiply the capabilities of others.

Key characteristics:
- **Detecting capability gaps:** Enabling teams actively scan for areas where stream-aligned teams lack skills or knowledge.
- **Temporary and transitional:** An enabling team for a specific capability should eventually make itself unnecessary as the capability spreads across stream-aligned teams.
- **Communities of practice vs. enabling teams:** Communities of practice are voluntary and self-organizing; enabling teams are purposeful and funded. Both are valuable, but they serve different purposes.

Expected behaviors include: asking questions to understand gaps, keeping up with industry developments, acting as coaches rather than doers, and proactively engaging with stream-aligned teams.

The BCG Digital Ventures case study illustrates how enabling teams helped new ventures adopt modern engineering practices quickly.

#### Complicated-Subsystem Teams

A complicated-subsystem team handles a component of the system that requires deep specialist expertise. The goal is to reduce the cognitive load of stream-aligned teams by isolating complicated domains.

Key characteristics:
- **Specialist expertise required:** The subsystem is genuinely complicated (not just complex) and requires deep specialist knowledge (e.g., machine learning algorithms, real-time pricing engines, complex image processing).
- **Low interaction with consumers:** The team provides its capability "as a service" to stream-aligned teams, minimizing the need for collaboration.
- **Only when necessary:** The authors stress that complicated-subsystem teams should be created only when the domain is genuinely beyond the capability of a stream-aligned team. Most domains are not as complicated as they first appear.

The Auto Trader case study shows how a complicated-subsystem team managed a complex search engine component, allowing stream-aligned teams to consume search as a service without needing to understand the internals.

Expected behaviors include: minimizing the cognitive load on consumers, providing clear APIs and documentation, and proactively improving the usability of the component.

#### Platform Teams

A platform team provides internal services that reduce cognitive load for stream-aligned teams. The platform is a grouping of teams (not a single team) providing a coherent set of services to other teams.

Key characteristics of effective platforms:
- **Thinnest viable platform (TVP):** Start with the minimum set of services that actually help stream-aligned teams. Resist the temptation to build a comprehensive platform before anyone needs it.
- **Managed as a live product:** The platform should be treated as a product with internal customers, using product-management practices (versioning, roadmaps, customer feedback).
- **Reduces cognitive load:** The primary purpose of a platform is to reduce the cognitive load of stream-aligned teams by abstracting away infrastructure complexity.
- **Fractal nature:** Inside a platform grouping, the same team types appear: stream-aligned teams aligned to platform services, enabling teams, complicated-subsystem teams, and inner platform teams.

Platform composition is discussed in detail: a platform may contain stream-aligned teams (focused on specific platform services), enabling teams (helping onboard new teams), complicated-subsystem teams (handling specialized platform components), and other (inner) platform teams.

Support teams in the traditional sense should be converted: infrastructure teams become platform teams, tooling teams become enabling teams, component teams become platform teams, and traditional support teams become part of stream-aligned teams with swarming patterns rather than tiered support.

The concept of team silos is addressed: anti-patterns where teams become isolated from the needs of stream-aligned teams, building what they find interesting rather than what the organization needs.

#### Converting Common Team Types

The chapter provides guidance on converting common team types to fundamental topologies:
- **Component teams to platform teams:** Teams owning shared technical components should become platform teams providing those components as services.
- **Infrastructure teams to platform teams:** Infrastructure teams should adopt platform-thinking, treating infrastructure as a product with internal customers.
- **Tooling teams to enabling teams:** Teams that build and maintain tooling should transition to enabling other teams to use and extend tools themselves.
- **Support teams:** Traditional tiered support should be replaced with swarming models where stream-aligned teams handle their own production issues, supported by enabling teams for specialized knowledge.
- **Architects:** Architecture should be embedded in teams rather than centralized, with architects acting as enablers rather than gatekeepers.

---

### Chapter 6: Software Boundaries and Fracture Planes

This chapter addresses how to draw boundaries in software systems that align with team structures, using Conway's law to guide architectural decisions.

**The problem with monoliths:** The chapter identifies many types of monoliths, not just the obvious application monolith:
- **Joined-at-the-database monolith:** Services appear independent but share a database.
- **Hidden monolith:** A system that looks modular but has deep coupling.
- **Monolithic thinking:** The belief that everything must be standardized across the organization.
- **Monolithic workplace:** Open-plan offices that force all teams into the same communication patterns.
- **Monolithic rebuilds:** Attempts to rewrite everything at once.
- **Coupled releases:** Different parts of the system that must be released together.
- **Single view of the world:** The assumption that all teams need the same data model.

**Fracture planes** are natural seams along which a software system can be split. The authors identify nine types:

1. **Business domain bounded context:** Drawing boundaries along domain-driven design bounded contexts. Each bounded context represents a coherent area of business activity with its own ubiquitous language. This is the primary fracture plane.

2. **Regulatory compliance:** Systems subject to different regulatory requirements should be split along compliance boundaries. The Payment Card Industry Data Security Standard (PCI DSS) is an example: compliance requirements should apply only to the subsystem handling card data, not to the entire monolith.

3. **Change cadence:** Parts of the system that change at different speeds should be separated. In a monolith, every part moves at the speed of the slowest component. Splitting allows each part to change at its own cadence.

4. **Team location:** Geographically distributed teams may need separate subsystems. Different time zones and communication patterns make tight coupling between remote teams difficult.

5. **Risk:** Different risk profiles suggest different subsystems. High-risk components (payment processing, authentication) may need different deployment, testing, and security practices than low-risk components.

6. **Performance isolation:** Components with different performance characteristics should be isolated. A reporting subsystem that generates heavy database load should not degrade the performance of a real-time user-facing service.

7. **Technology:** Different technology stacks form natural fracture planes. A Java back-end, a React front-end, and a Python data pipeline should be separate subsystems.

8. **User personas:** Systems serving different user types (internal vs. external, admin vs. end-user) should be split along persona boundaries.

9. **Natural fracture planes:** Sometimes the domain itself suggests natural boundaries. Manufacturing IoT scenarios often split along the physical topology of the factory floor.

The Poppulo case study illustrates how a team used fracture planes to split a monolithic system: separating the core platform (technology fracture plane), the messaging engine (change cadence fracture plane), and the analytics subsystem (performance isolation fracture plane).

Additional guidance includes treating software boundary size as a cognitive load concern: boundaries should be small enough that a single team can own them, and using ecosystem tuning to adjust boundaries over time.

---

### Chapter 7: Team Interaction Modes

This chapter defines the three interaction modes that govern how teams work together.

#### Collaboration Mode

Teams work closely together for a period of time to discover new things. Collaboration is characterized by:
- **High communication bandwidth:** Frequent, rich communication between teams, including shared planning sessions, joint retrospectives, and pair programming across team boundaries.
- **Divergent thinking:** Exploring multiple possible solutions rather than converging on one. Kyung Hee Kim and Robert A. Pierce's research on convergent versus divergent thinking is cited: collaboration is associated with divergent thinking (generating many ideas), while X-as-a-Service is associated with convergent thinking (selecting and refining the best idea).
- **Temporary by nature:** Collaboration should not be permanent. Once the discovery phase is complete, teams should transition to a more efficient interaction mode. Research by Bernstein and others on "intermittent collaboration" shows that groups who alternate between collaboration and independent work outperform groups in either pure collaboration or pure isolation.
- **Suitable for exploration:** When the problem space is not well understood, collaboration helps both teams learn. Mike Rother's "Toyota Kata" is cited as an example of how structured collaborative improvement works in practice.

Advantages include rapid knowledge sharing and joint discovery. Disadvantages include high communication overhead, potential confusion about ownership, and the risk of collaboration becoming permanent when it should be transitional. The authors stress that collaboration is expensive and should be used sparingly -- only when the value of discovery justifies the cost of coordination.

#### X-as-a-Service Mode

One team provides something to another team as a service with minimal day-to-day interaction. Characteristics:
- **Low communication overhead:** The consuming team can use the service without needing to understand its internals. This is the explicit benefit of the X-as-a-Service model: if the aspect being provided needs little interaction from the consuming team, then it is highly fit for purpose.
- **Well-defined service boundaries:** The service API must be clear, well-documented, and stable.
- **Product-management discipline:** The providing team treats the service as a product, considering the needs of all consumers when making changes. The team must have a strong sense of responsibility toward both consumers and the viability of the service.
- **Convergent thinking:** The solution space is well understood, and the focus is on efficient delivery.
- **Compelling developer experience (DevEx):** The service should be straightforward to use, test, deploy, and debug; documentation should be clear, well-written, and current. Feature requests from consuming teams are considered but not built just because a team asked; instead, the purpose is evolved with the best interest of all consumers in mind.

This mode works well only if the service boundary is well chosen and well implemented. Pivotal (now part of VMware) is cited as an example: their Cloud Foundry platform was designed to be consumed as a service with minimal interaction between platform and application teams. Evan Wiley, who worked at Pivotal, describes how the platform team focused on making the developer experience so good that consuming teams had no reason to ask for help.

Advantages include low overhead, fast consumption, and scalability to many consuming teams. Disadvantages include the risk of the service not meeting consumer needs if the boundary is wrong, and the significant effort required to maintain good service management and documentation.

#### Facilitating Mode

One team helps (or is helped by) another team to remove blockers or fill capability gaps. Characteristics:
- **Coaching and mentoring:** The facilitating team acts as a guide rather than a doer. The enabling team should never do the work that the stream-aligned team should be doing; instead, they help the team learn to do it themselves.
- **Promise theory:** Based on the work of Mark Burgess, the idea that teams make explicit promises to each other about what they will provide, creating a network of voluntary commitments rather than imposed requirements. This creates a more resilient and adaptive organizational structure.
- **Principle of overlapping measurement:** Don Reinertsen's concept from "The Principles of Product Development Flow" -- both teams share some metrics to ensure alignment, without fully overlapping responsibilities. This prevents the facilitating team from losing touch with the reality of the teams they support.

The facilitating mode is particularly relevant for enabling teams working with stream-aligned teams. The facilitating team helps the other team grow capabilities while respecting their autonomy. The Capra Consulting case study in Norway shows how an entire organization adopted the facilitating mode, with senior practitioners acting as enablers across teams.

Advantages include capability growth, trust building, and reduced dependency on specialists over time. Disadvantages include the risk of the facilitating team becoming a crutch (teams stop trying to learn because the enablers will do it for them) and the difficulty of knowing when to step back.

#### Choosing and Combining Interaction Modes

The chapter provides a framework for choosing interaction modes based on the situation:
- **Discovery phase:** Use collaboration to explore the problem space.
- **Execution phase:** Use X-as-a-Service for well-understood, stable capabilities.
- **Learning phase:** Use facilitating to help teams acquire new capabilities.

Interaction modes can change over time: a platform team might collaborate closely with a stream-aligned team to discover requirements, then transition to X-as-a-Service once the platform capability is stable. This evolution is natural and expected.

The chapter includes tables summarizing advantages and disadvantages of each mode and a reference table showing which interaction modes apply between which team types. Key pairings include:
- Stream-aligned to stream-aligned: Collaboration (for shared features) or X-as-a-Service (for shared services)
- Stream-aligned to platform: X-as-a-Service (primary) or Collaboration (for new platform capabilities)
- Stream-aligned to enabling: Facilitating (primary)
- Stream-aligned to complicated-subsystem: X-as-a-Service
- Enabling to platform: Facilitating or Collaboration

The IBM case study illustrates how an organization moved from ad-hoc team interactions to explicitly defined interaction modes, improving clarity and reducing friction.

#### Enhancing Flow Through Interaction Modes

The authors explain how well-chosen interaction modes enhance the flow of change through several mechanisms:

- **Effective APIs:** Clear team interfaces reduce the need for ad-hoc communication. The concept of a team API (from Chapter 3) is extended here: when teams have well-defined interfaces, they can interact more efficiently. A platform team with a well-documented, versioned API allows stream-aligned teams to consume platform services without needing to schedule meetings or send messages.
- **Reducing uncertainty:** Collaboration during discovery reduces uncertainty about what to build; X-as-a-Service during execution reduces communication overhead once the solution is well-understood. The key insight is that different phases of product development require different interaction modes, and organizations should expect these modes to shift over time.
- **Detecting problems through interaction patterns:** Awkward team interactions signal misaligned boundaries or missing capabilities. Two concrete examples are provided: (1) A stream-aligned team spending hours trying to use a calculation component "as a service" from a complicated-subsystem team signals that the component boundary, API, or documentation needs improvement. (2) A platform team expecting collaboration with a stream-aligned team but receiving little interaction signals that the stream-aligned team may not understand the value of the collaboration, or the boundary being bridged is too ambitious.

The chapter also discusses temporary changes to interaction modes. Sometimes a team needs to shift from X-as-a-Service to collaboration temporarily -- for example, when a platform team needs to discover new requirements for a major platform upgrade. The Pivotal case study (Evan Wiley) illustrates how a platform team at Pivotal Cloud Foundry shifted from X-as-a-Service to collaboration and back again as the platform evolved.

The reverse Conway maneuver plays a role here: by deliberately choosing interaction modes between specific teams, organizations can guide the architecture of the software. If two teams are told to collaborate, their software components will tend toward tight coupling. If they are told to interact via X-as-a-Service, their components will tend toward loose coupling with well-defined APIs. This is Conway's law in action at the interaction level.

---

## Part III: Evolving Team Topologies

### Chapter 8: Sensing the Organization

This chapter focuses on how organizations can sense when their team structures need to evolve. The key message is that team topologies must change over time, and organizations need mechanisms to detect when change is needed. The chapter opens with a quote from Drucker: "The greatest danger in times of turbulence is not the turbulence itself, but to act with yesterday's logic."

**Organizational sensing** is the practice of actively monitoring the health and effectiveness of team structures. The authors argue that organizations need both formal and informal sensing mechanisms:

- **Formal sensing:** Regular reviews of team topologies, dependency tracking, cognitive load assessments, and delivery metrics. The DORA metrics (deployment frequency, lead time for changes, mean time to restore, and change failure rate) provide objective measures of delivery performance that can signal when team structures are degrading.
- **Informal sensing:** Guilds, communities of practice, internal tech conferences, and hallway conversations that surface problems early. The authors emphasize that because these interactions are outside the everyday building and running of systems, Conway's law plays a much less obvious role, and a freer cross-association between teams can take place.

**Rapid learning** is enabled by providing time, space, and money for people from different teams with similar skills to come together. The authors cite Robert Axelrod's research showing that teams that rehearse their interactions in learning contexts find it easier to interact effectively when building and running software systems. Two critical mechanisms are identified: (1) consciously designed physical and virtual environments, and (2) time away from desks at guilds, communities of practice, and internal tech conferences. The CDL office layout case study shows how physical space was designed to support both focused team work and cross-team learning.

**Adoption of new practices** follows a pattern: early adopters experiment, enabling teams help spread successful practices, and eventually the practice becomes part of the standard way of working. The GovTech Singapore case study shows how a forward-deployment team (FDT) acted as an enabling team, helping product teams adopt new practices around CI/CD, testing, and observability. The FDT was staffed with senior engineers who paired with product team members, gradually transferring knowledge and capability. The DORA and SPACE frameworks were used to measure the impact of these enabling efforts.

**Team topology evolution** happens in response to specific triggers:
1. **Delivery cadence slowing down:** When teams can no longer deliver at the expected pace, it signals that the team structure may need to change. This could mean the team owns too much (cognitive overload), the boundaries are wrong, or there are too many dependencies on other teams.
2. **Software too large for one team:** When a single team can no longer effectively own a subsystem, it should be split along fracture planes.
3. **Multiple business services relying on one large set of underlying services:** This creates bottlenecks and suggests the need for platform teams or additional stream-aligned teams. The "Phoenix Project" scenario (referencing Gene Kim's novel) is a well-known illustration of this pattern.

The Sky Betting and Gaming case study, described by Michael Maibaum, illustrates how a complicated-subsystem team evolved over time: initially collaborating closely with stream-aligned teams to understand requirements for a complex real-time pricing component, then transitioning to X-as-a-Service once the component stabilized. The team also sensed when the interaction mode needed to change based on the maturity of the consuming teams and the stability of the API.

**Combining team topologies** is discussed: organizations may need multiple instances of each team type, and the mix will change over time. The ING Netherlands case study shows how a large bank used a combination of stream-aligned, enabling, and platform teams to support rapid digital transformation. Andy Higgins and Andy Heyden, leading the transformation at ING, describe how they started with a "benched bay" approach for cross-functional teams and gradually introduced platform teams as the need for shared capabilities became clear.

**Evolution triggers** are specific signals that a team topology needs to change:
- Increasing wait times between teams (measured through dependency tracking)
- Growing dependency count per team (measured through tools like the Physical Dependency Matrix)
- Rising cognitive load (measured through the Teamperature survey or similar assessments)
- Repeated failures in delivery or production
- Team member frustration or low morale

The chapter introduces the concept of **self-steering design and development**: empowering teams to sense and respond to their own needs, within guardrails set by the organization. Naomi Stanford's work on organizational design is cited: modern organizations should support self-steering teams with clear boundaries and access to information. This requires trust, clear boundaries, and access to information. Jeff Sussna's "Designing Delivery" concept of "continuous design" -- treating service, feedback, failure, and learning as first-class concepts -- is presented as a philosophical foundation for self-steering teams.

**Business as usual (BAU) teams** are discussed as an anti-pattern to be avoided. Instead of separating "new feature" teams from "maintenance" teams, stream-aligned teams should handle their own operational concerns with support from enabling and platform teams. Separating "new development" from "maintenance" creates artificial handoffs and slows the flow of value. The authors recommend a "side-by-side" approach where a new team takes on a new service while the existing team continues with the legacy system, with a planned transition period.

**Environmental scanning** is the practice of monitoring external trends (new technologies, market shifts, regulatory changes) that may require organizational adaptation. This is a strategic responsibility, not just a technical one. The authors cite the Internet of Things (IoT) as an example of a technology shift that forced many organizations to rethink their team structures, creating new stream-aligned teams for connected devices and new platform teams for device management. Sriram Narayan's "Agile IT Organization Design" is referenced for guidance on aligning IT organization structure with business strategy.

---

### Chapter 9: Conclusion -- The Road Ahead

The conclusion summarizes the core ideas of Team Topologies and provides practical guidance for getting started. Ruth Malan's observation that "the architecture of the system gets cemented in the forms of the teams that develop it" frames the entire argument: getting team design right is not an organizational nice-to-have but an architectural imperative.

**Core ideas:**
1. **Team-first thinking:** The team is the smallest unit of delivery. Optimize for team autonomy, cognitive load management, and clear boundaries.
2. **Conway's law:** Use it deliberately through the reverse Conway maneuver to guide both team structure and software architecture.
3. **Four fundamental team types:** Stream-aligned, enabling, complicated-subsystem, and platform. Every team should gravitate toward one of these types.
4. **Three interaction modes:** Collaboration, X-as-a-Service, and facilitating. Choose the right mode for the right situation and evolve over time.
5. **Fracture planes:** Use natural seams in the business domain, technology, regulation, and team structure to guide software boundaries.

**Getting started -- five concrete steps:**

1. **Identify suitable streams of change:** Look for valuable, independent flows of work that can be owned by a single team. A good heuristic is to ask: "Does this stream of work have a clear set of external or internal customers? Can it move at its own cadence without being blocked by other teams?"

2. **Build the thinnest viable platform:** Start with the minimum platform capabilities that actually help stream-aligned teams. Resist the urge to build a comprehensive platform before teams need it. Ask stream-aligned teams what slows them down the most, and build only that.

3. **Assess capability gaps:** Identify what stream-aligned teams are missing and determine whether enabling teams or other support is needed. Look for patterns: if multiple stream-aligned teams are struggling with the same capability (e.g., CI/CD, security, observability), an enabling team may be warranted.

4. **Share and practice interaction modes:** Explicitly define and communicate how teams should interact. Many people have never experienced a team-first way of working. Take the time to explain and demonstrate the interaction modes. Explain why some teams are closer together and some are further apart. Explain the basics of Conway's law, and how the conscious design of teams and intercommunications can help improve the software architecture.

5. **Evolve continuously:** Team topologies are not static. Regularly assess and adjust based on delivery performance, cognitive load, and organizational sensing. Heidi Helfand's "Dynamic Reteaming" is referenced for guidance on how to adapt team composition over time.

The authors emphasize that this is an ever-evolving approach, not a short-term change program. It might require an initial period of intensive change to "start up the engine," but the car never stops. There is no autopilot for organizational change. As Ismail Chaib says: "Org design is like a martial art; you have to keep practicing to stay sharp."

The authors deliberately omit details of how to undertake large-scale transformations, instead pointing readers to Mary Lynn Manns and Linda Rising's "Fearless Change" for excellent patterns of organizational change. They emphasize the humanistic aspects of Team Topologies: the focus on the team, the explicit limits on cognitive load, the reduction in noise and interruptions through team-first workspace design, and a limit on free-for-all communications. Above all, they encourage sharing how the Team Topologies approach makes for better outcomes for humans, software systems, and the organization itself.

---

## Appendix: Case Studies (Second Edition)

The second edition includes nine detailed case studies from organizations that have applied Team Topologies principles, representing a range of industries, organization sizes, and geographies. These case studies provide concrete evidence that the principles work across diverse contexts.

### EBSCO
EBSCO, a large information services company providing research databases and discovery services to libraries worldwide, reorganized teams around business domains using Team Topologies. Starting from a traditional functional structure with separate front-end, back-end, and database teams, they assessed cognitive load across teams using surveys and interviews, identified misaligned boundaries where team responsibilities did not match domain boundaries, and reorganized to create cross-functional stream-aligned teams. The transformation included moving from component teams to full-stack teams that owned the entire vertical slice of functionality.

Results included 26% faster feature delivery, over $9 million in cost savings, and a comprehensive application inventory -- the first in the company's history -- that established clear connections between business capabilities, applications, IT components, and responsible teams. This inventory created a foundation for application rationalization with substantial future cost-saving potential. Even initially skeptical senior leaders were converted. Mike Gunning, SVP of Development, admitted: "At first I was skeptical that reorganizing the teams would have any significant benefit. However, once the Team Topologies work had been completed, my development managers reported that they felt they had much less cognitive load and there was an increase in their job satisfaction." Craig Spara, Senior Software Engineer, highlighted that becoming a full-stack development team "removed the predecessor dependency a UI feature has on the API, allowing us to work on API and UI features in tandem which can reduce completion of both features to a single PI."

### GovTech Singapore
GovTech Singapore, the government agency responsible for digital transformation of public services, used enabling teams (called "forward deployment teams" or FDTs) to help product teams adopt modern engineering practices. They focused on CI/CD, automated testing, and observability. The FDT model embedded experienced engineers within product teams for limited periods, coaching them on modern practices while respecting the team's autonomy over their product decisions. This approach is a textbook example of the facilitating interaction mode, where the enabling team acts as a coach and mentor rather than taking over the work. The SPACE framework (Satisfaction, Performance, Activity, Communication, Efficiency) was used to measure developer productivity and well-being, and DORA metrics tracked software delivery performance.

### ING Netherlands
ING Netherlands, one of the largest banks in Europe, applied Team Topologies as part of a broader digital transformation called "ING Agile." They combined stream-aligned teams with enabling and platform teams to accelerate delivery while managing stringent regulatory requirements in the banking sector. The transformation was notable for its scale -- affecting thousands of employees -- and its emphasis on team autonomy within guardrails set by compliance and risk management. ING's approach illustrates how Team Topologies can coexist with heavy regulatory oversight by aligning compliance requirements to specific stream-aligned teams rather than imposing them on the entire organization.

### KFC UK&I
KFC UK&I reorganized their technology teams from a traditional functional structure (separate teams for web, mobile, back-end, and infrastructure) to stream-aligned teams focused on customer-facing digital products. The original team organization showed teams grouped by technical function with multiple cross-team dependencies for every feature. The reconfigured organization created cross-functional stream-aligned teams aligned to customer journeys: ordering, delivery, restaurant experience, and loyalty. Results included a threefold increase in digital sales. The transformation involved rethinking team boundaries, cognitive load (assessed through a three-month cognitive load assessment), and interaction modes, with a particular focus on reducing dependencies between teams. A later expansion of collaboration scope showed how the team topologies continued to evolve as the organization matured.

### Creditas
Creditas, a Brazilian fintech founded in 2012, provides secured loans with low interest rates through a digital platform. By 2022, the company had grown to over 3,000 employees. They used Team Topologies to manage cognitive load as they scaled product development, particularly for a multi-product initiative to offer a single credit card connecting multiple existing and new products. They encountered significant challenges: a single Payments Team responsible for multiple strategic bets, accumulating product and technical debt, an overly complicated microservices architecture that was effectively a "distributed monolith," and external service dependencies forcing custom-built components.

By applying the Teamperature model (a systematic approach to assessing cognitive load across teams developed with Dr. Laura Weis), they identified cognitive load drivers across four clusters: team characteristics, work practices and processes, task characteristics, and work environments and tools. This data-driven approach helped them make sense of recurring cognitive load challenges across teams, make better-informed decisions about how to address them, and evaluate whether changes actually improved overall cognitive health and performance. Teams were reorganized around value streams with clearer responsibilities, and platform teams were established to reduce the cognitive load on product teams.

### Yassir
Yassir, a super-app operating across North Africa offering ride-hailing, delivery, and financial services, applied Team Topologies to scale their engineering organization from a startup to a significant technology operation. They tracked a 230% increase in employee satisfaction over two years. The case study shows how enabling teams helped spread capabilities across stream-aligned teams, with a particular emphasis on growing mobile development and data engineering capabilities. The approach demonstrates that Team Topologies principles apply beyond Western technology companies and that the humanistic benefits (employee satisfaction, engagement) can be measured and are significant.

### Telenet
Telenet, a Belgian telecommunications company, used internal and external customer-centric tribes as value stream groupings. Their approach illustrates the fractal nature of Team Topologies, with the same patterns repeating at different organizational levels. Within each tribe, there were stream-aligned teams focused on specific customer journeys, platform teams providing shared capabilities, and enabling teams helping to upskill other teams. The use of Wardley Maps to understand the evolution of their capabilities and inform team topology decisions is highlighted as a complementary practice that works well with Team Topologies.

### Trade Me
Trade Me, New Zealand's largest online marketplace (similar to eBay), used Team Topologies to develop a thinnest viable platform (TVP) approach. They focused on providing the minimum platform services needed to support stream-aligned teams, evolving the platform over time based on actual team needs rather than anticipated requirements. The TVP initially included basic deployment pipelines, shared logging, and a few self-service infrastructure components. As stream-aligned teams consumed these services and identified gaps, the platform team expanded its offerings. This evolutionary, demand-driven approach to platform building is presented as a model for organizations that want to avoid the common trap of building elaborate platforms that nobody uses.

### Adidas
Adidas's digital platform engineering journey, led by Fernando Cornago, exemplifies the combination of platform and enabling team behaviors within a large enterprise. The digital platform team acted as both a platform team providing self-service infrastructure and an enabling team helping product teams adopt best practices. The platform eventually provided essential capabilities for cloud-native engineering: compute resources on Kubernetes, data streaming and APIs, CI/CD pipelines, testing frameworks, and observability tools. These foundational services allowed product teams to rapidly build and deploy new features for the Adidas website and mobile apps.

Adidas also illustrates the multi-platform reality of large enterprises: alongside the digital platform, there are enterprise platforms (for SAP, Salesforce, Microsoft) and a data and analytics platform (supporting advanced analytics, big data, and enterprise reporting). The platform group actively engaged with other teams through enabling and collaborating interaction modes, helping teams learn good practices and effectively utilize the platform through consulting, training, onboarding, and co-creation. Existing stable services were consumed by onboarded teams with an "as-a-Service" interaction mode. Adidas demonstrates the value of combining different interaction modes at different times, using collaboration for discovery, enabling for onboarding, and X-as-a-Service for stable platform services.

---

## Key Takeaways

1. **Teams are the primary unit of delivery, not individuals.** Optimize everything around team effectiveness: team size (5-9 people), team lifespan (long-lived), team ownership (end-to-end including production operations), and team boundaries (clear and limited). The DORA research confirms that teams with end-to-end ownership deliver faster and more reliably. The Tuckman model reminds us that teams need time to form, storm, and norm before they can perform -- dissolving teams wastes this investment.

2. **Conway's law is real and powerful.** Your software architecture will mirror your organizational communication structure, whether you intend it to or not. The homomorphic force ensures that siloed organizations produce siloed software, and cross-functional teams produce modular architectures. Use the reverse Conway maneuver deliberately: design the team structure you want and let the architecture follow. Be aware of naive uses of Conway's law that treat it as a simple one-to-one mapping between teams and microservices.

3. **There are only four fundamental team types.** Stream-aligned teams (the primary type, aligned to valuable flows of work), enabling teams (capability multipliers that help other teams grow), complicated-subsystem teams (handling genuinely specialist domains to reduce cognitive load on stream-aligned teams), and platform teams/groupings (providing internal services that abstract away infrastructure complexity). Every team in the organization should gravitate toward one of these four types. There is deliberately no "ops team" or "support team" in this taxonomy -- operations and support are integrated into stream-aligned teams.

4. **There are only three interaction modes.** Collaboration (high-bandwidth, temporary, for discovery and exploration), X-as-a-Service (low-overhead, stable, for well-understood capabilities that can be consumed with minimal communication), and facilitating (coaching, mentoring, for capability growth where one team helps another without doing the work for them). Choose the right mode for the situation and expect modes to change over time as understanding grows.

5. **Cognitive load is a team-level concern, and it is dynamic.** A team should own no more than one complicated or complex domain. Minimize extraneous load (unnecessary complexity from environment, tooling, and inter-team interactions), manage intrinsic load through good boundaries, and leave room for germane load (learning). The river analogy is more accurate than the bucket analogy: load fluctuates naturally over time, and a temporary increase is acceptable when there is a clear objective (taking on new ownership, integrating new tools, modernizing systems). What must be avoided is continuously increasing load without adequate support, or standing still while the number of tools, services, and processes proliferates.

6. **Use fracture planes to draw software boundaries.** The nine fracture planes identified -- business domain bounded context (primary), regulatory compliance, change cadence, team location, risk, performance isolation, technology, user personas, and natural domain boundaries -- provide concrete guidance for splitting software systems. The business domain bounded context from Domain-Driven Design is the most important and should be the first fracture plane considered. The monolith is not just a technical concern: monolithic thinking, monolithic workplace design, and monolithic rebuild attempts are all anti-patterns.

7. **Platforms should be thinnest viable (TVP).** Start with the minimum services that actually help stream-aligned teams. Treat the platform as a product with internal customers, using product-management practices (versioning, roadmaps, customer feedback). The platform grouping is fractal: the same team types appear inside and outside the platform. In large organizations, resist the "single platform that does it all" anti-pattern -- NAV's approach of "a small number of coherent internal platforms" is presented as a better model.

8. **Team topologies must evolve continuously.** There is no final state. Organizations must sense (monitor delivery cadence, cognitive load, dependencies, wait times), respond (adjust team types, interaction modes, boundaries), and repeat. The three primary evolution triggers are delivery slowdowns, growing software size beyond one team's capacity, and accumulating dependencies where multiple business services rely on one large set of underlying services. The TransUnion case study demonstrates that evolution takes longer than expected (three years longer than initially planned).

9. **Fast flow means fast flow of value to customers, not just fast delivery.** Validate that customers are actually benefiting from the changes you deliver. Teams close to customers produce better outcomes than teams separated by multiple handoffs and layers of indirection. Piotr Kacala's formulation captures this: "Flow is how quickly work moves from idea to customer value without getting stuck in organizational bottlenecks. Structure only matters if it helps ideas become reality faster."

10. **This is a humanistic approach.** Team Topologies aims to make work more humane while increasing organizational effectiveness. Successful adoptions report not just faster delivery but significant improvements in employee engagement and satisfaction. Capra Consulting applied Team Topologies to their entire organization (including sales, operations, recruitment, and leadership). Yassir tracked a 230% increase in employee satisfaction. EBSCO's skeptics were converted when they saw reduced cognitive load and increased job satisfaction. The book is ultimately about making organizations work better for the humans within them.

11. **The approach is fractal and adaptable to organization size.** In a small startup of thirty people, "enabling" might mean senior practitioners pairing with juniors. A well-maintained wiki with clear owners can serve as a "platform." These patterns ease the transition to dedicated teams during later growth phases. The question "Are our product teams spending enough time focused on end customers' needs?" is a good heuristic for determining when to form dedicated platform teams. Large organizations need dedicated enabling and platform teams, and the fractal nature means the same patterns repeat at every level.

12. **Avoid the anti-pattern of static adoption.** Organizations that merely map their existing teams to the four types without understanding the underlying principles of flow, cognitive load, and evolution will see limited benefits. The most successful transformations have been driven by clear business needs and competitive pressure. Large re-orgs with loosely defined goals around improved efficiency tend to fall short. The patterns are building blocks for continuous adaptation, not a destination. As George Box said (via W. Edwards Deming): "All models are wrong, but some are useful." Contextual awareness, together with useful modelling, is the key to driving meaningful organizational change.
