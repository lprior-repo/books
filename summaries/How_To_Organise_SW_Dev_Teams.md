# Comprehensive Summary: How To Organise Software Development Teams

*Based on "How To Organise Software Development Teams" (21-08-22) by Dave Farley, part of the "Better Software Faster" series*

---

## Introduction: Why Team Organisation Matters

One of the most consequential decisions any software organisation will make is not about technology, architecture, or tooling -- it is about people. How do we divide up the work? What skills do we need on each team? How do we create a team structure capable of working on a complex system? And, critically, what happens when that system grows more complex and the organisation scales?

These questions sit at the heart of software delivery performance. Get them wrong and teams become gridlocked in dependencies, communication overhead explodes, and even talented engineers produce subpar results. Get them right and small, focused teams can move fast, innovate, and deliver high-quality software reliably. This book, grounded in the "Better Software Faster" philosophy and drawing on research from the State of DevOps reports, Team Topologies by Matthew Skelton and Manuel Pais, and decades of industry experience, provides a practical framework for answering these questions.

The central thesis is that team organisation is inseparable from system design. The way you structure your teams will, for better or worse, be reflected in the structure of the software they produce. This insight, formalised as Conway's Law, is not merely an observation -- it is an engineering constraint that must be actively managed.

---

## Chapter 1: Team Size and Structure

### The Case for Small Teams

A foundational claim running throughout the book is that small teams outperform large teams. This is not an opinion; it is supported by numerous studies and by the real-world experience of high-performing organisations. The reasons are rooted in the mathematics of human interaction.

As team size grows, two things increase exponentially: cognitive load and communication complexity. Cognitive load refers to the mental effort required to understand the system, keep track of who is working on what, and maintain awareness of changes that might affect your work. Communication complexity is a combinatorial problem -- the number of communication channels between n people is n(n-1)/2. A team of 5 has 10 communication channels. A team of 10 has 45. A team of 20 has 190. The overhead becomes crushing.

The book cites various sources recommending an optimal team size of between 5 and 9 people. This range balances having enough diversity of skills with keeping communication overhead manageable. Below 5, teams may lack the breadth of skills needed to be autonomous. Above 9, the communication tax becomes significant enough to degrade performance.

### The Scaling Problem

The recommendation for small teams raises an obvious question: what about large projects at large organisations? You cannot build a complex system with a single team of 7 people. You need many teams. And this is where things get difficult.

As organisational size and the number of teams grow, a natural and harmful pattern emerges: teams become increasingly interconnected and dependent on one another. Progress slows to a crawl because no team can move forward without coordinating with, waiting for, or negotiating with several other teams. The organisation ends up in a state where the sum of its parts is far less than it could be.

This pattern is not inevitable. It is a consequence of how the work is divided and how teams are structured. The key insight is that team focus and responsibility are the levers. How we organise our work and structure our teams is deeply related to how we structure the code and systems we build.

### The Functional Silo Trap

A particularly common and damaging pattern is organising teams around functional specialities. As systems grow more complex and the volume of work increases, organisations naturally divide work into "functions": coding, testing, architecture, UI, backend, DevOps, and so on. Teams are then created to handle each function.

The problem with this approach is that no single team can deliver anything of value on its own. The coding team needs the architecture team to approve designs, the UI team to build the interface, the backend team to build the services, and the testing team to verify quality. Every piece of work requires coordination across multiple teams. Hand-offs proliferate. Bottlenecks form at the boundaries. Information is lost in translation between teams. The overall system throughput collapses.

This is the functional silo anti-pattern, and it is one of the most significant barriers to high-performance software delivery. The solution is not to eliminate specialisation -- it is to change the axis around which teams are organised.

---

## Chapter 2: Conway's Law and Its Implications

### The Law

> "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." -- Melvin E. Conway

This is one of the most important ideas in software engineering, and the book treats it as such. Conway's Law is not a suggestion or a tendency; it is a reliable predictor of system design. If your organisation is divided into a frontend team, a backend team, a database team, and a QA team, your software will be designed along exactly those lines -- with all the coupling and coordination problems that implies.

Conversely, if your organisation is structured around cross-functional teams aligned to business domains, your software will tend toward modularity, loose coupling, and independent deployability. The organisation's communication structure becomes the system's architecture.

### Designing Around Conway's Law

Rather than treating Conway's Law as an unfortunate inevitability, the book advocates for the "Inverse Conway Maneuver" -- deliberately designing your organisation's structure to produce the system architecture you want. If you want microservices that are independently deployable, you need teams that can independently deploy them. If you want loosely coupled modules, you need loosely coupled teams.

This means that organisational design is not an HR concern; it is an architectural concern. Technical leaders must be involved in, and often drive, decisions about team structure. The architecture of the software and the architecture of the organisation are two sides of the same coin.

### Practical Implications

The practical implications of Conway's Law are far-reaching:

1. **Team boundaries should mirror module or service boundaries.** If two pieces of functionality are handled by the same team, they will tend to become tightly coupled. If they are handled by different teams, they will tend to become loosely coupled through well-defined interfaces.

2. **Communication paths should be designed, not accidental.** The people who need to coordinate frequently should be on the same team. People who should not need to coordinate should be on different teams with clear interfaces between their work.

3. **Organisational change is architectural change.** Restructuring teams will, over time, restructure the software. This can be used deliberately to improve system design, but it also means that a poorly structured organisation will continuously produce poorly structured software regardless of the best intentions of individual engineers.

---

## Chapter 3: Team Skills and Responsibilities

### The Team as the Primary Unit of Work

A core principle of the "Better Software Faster" approach is that the team, not the individual, is the primary unit of work. This means that everyone in the team shares the work and the responsibility to achieve shared goals. There are no solo heroes carrying the load while others watch. Success and failure belong to the team collectively.

This principle has profound implications for how teams are composed and how work is assigned.

### Minimising Hand-offs

To produce, as near as possible, a complete piece of work, teams must minimise hand-offs between teams. The book identifies several common and harmful hand-off patterns:

- **Building the backend service and then handing over to another team to build the frontend UI.** This creates a sequential dependency where neither team can test the full feature end-to-end until both are done. Misunderstandings at the interface between frontend and backend are discovered late and are expensive to fix.

- **Assuming responsibility for overall architecture of the system lies elsewhere.** When architects sit in a separate team from the people writing the code, architectural decisions are made without full understanding of implementation constraints, and implementation decisions are made without full understanding of architectural intent.

- **Passing responsibility for the quality of the code to another team to do the testing.** This is perhaps the most damaging pattern of all. When developers know that someone else will catch their bugs, they have less incentive to write correct code. When testers receive code they did not help design, they can only test for what they imagine might be wrong, not for what the developers know is fragile.

Each of these hand-offs introduces delay, information loss, and misalignment. The solution is to give each team the skills and responsibility to handle all of these aspects for their part of the system.

### The Full Spectrum of Skills

It is common to think first of the "Dev Team" as responsible for development and coding, design and architecture, and sometimes infrastructure and operability. But the book challenges this narrow view by asking: what about Metrics and Monitoring? Testing and QA? Application Security? Commercial and Operational Viability? User Experience?

A high-performing team needs competence across all of these areas. This does not mean every team member needs to be an expert in everything -- that is neither realistic nor desirable. It means the team collectively should have sufficient skill in each area to handle the common cases independently, and to know when to call in specialist help for the difficult cases.

To reduce the coupling between teams -- the interdependencies that prevent independent progress -- teams cannot be built around functional fragments of the work. Teams need to be multi-functional, with the range of skills they need to complete a piece of work, instead of handing it off to another team.

### The 80/20 Principle

The book introduces a pragmatic guideline: teams should have the skills to handle approximately 80% of their work without any outside help. The remaining 20% -- the genuinely difficult, specialised, or unusual problems -- can be handled by bringing in expertise from enabling teams or specialists. This balance allows teams to maintain their autonomy for the vast majority of their work while still having access to deep expertise when they need it.

Over time, as team members learn from the experts who temporarily join them, the team's own skill base grows. What was once part of the "difficult 20%" becomes part of the routine 80%. This creates a virtuous cycle of learning and increasing autonomy.

---

## Chapter 4: Team Organisation -- The Team Topologies Framework

### Stream-Aligned Teams

A "team-first" approach begins by dividing the work in ways that minimise dependencies between teams: defining boundaries and responsibilities so that each team has more autonomy and the overall team structure is loosely coupled.

The starting point is to align teams with a bounded context in the problem domain, such that each team is aligned with a single valuable piece of work. This concept, drawn from Domain-Driven Design and popularised in the excellent book "Team Topologies" by Matthew Skelton and Manuel Pais, is called a "Stream-Aligned Team."

A stream-aligned team is responsible for delivering value to users or customers in a specific business domain. It is cross-functional, possessing all the skills needed to take a feature from conception through to production. It is aligned with a flow of work -- a "stream" -- rather than with a functional speciality.

Across the whole software development organisation, the majority of teams should be stream-aligned. These are the teams that are focused on business goals, producing valuable software for users quickly and reliably. They are the engine of value creation.

The State of DevOps research, cited in the book, identifies a key predictor of success: "the ability of a team to make decisions and make progress without coordinating with or asking permission of people outside the team." Stream-aligned teams are designed to maximise this property.

### Enabling Teams

Not every team can have deep expertise in all areas. But they should know enough to know when to ask for help. Enabling teams exist to provide that help.

An enabling team is a group of specialists who lend their expertise to stream-aligned teams when required. Their role is not to do the work for the stream-aligned team, nor to dictate how it should be done. Their role is twofold:

1. **Work with the stream-aligned team to implement the new feature or solve the difficult problem.** They roll up their sleeves and collaborate as temporary team members.

2. **Teach the stream-aligned team a bit more about their speciality in the context of the real work being done.** They are educators and mentors, not consultants who drop in with advice and leave.

The aim is that over time, the stream-aligned team's knowledge grows, and they become less dependent on the enabling team for that particular area of expertise. The enabling team then moves on to help other teams with other challenges.

This model avoids the common trap of creating permanent specialist silos while still ensuring that deep expertise is available when needed. It also ensures that knowledge transfer happens in the most effective way possible -- through collaboration on real, pressing problems rather than through abstract training sessions.

### Complex Subsystem Teams

Some parts of a system are inherently specialised and complex. Examples might include interfacing with complex hardware, implementing advanced cryptographic algorithms, or building high-performance data processing pipelines. These components require deep expertise in a narrow field.

Complex subsystem teams are formed to handle these technically specialised, complex components. The people on these teams have deep expertise in their narrow field and use their skills to write the code that allows stream-aligned teams to make progress without worrying about the technicalities of systems that are not their natural focus.

The key distinction between a complex subsystem team and a functional silo is the nature of the boundary. A complex subsystem team owns a well-defined, technically coherent component with a stable interface. Stream-aligned teams interact with it through that interface and do not need to understand its internals. A functional silo, by contrast, owns a cross-cutting concern (like "all testing" or "all architecture") that touches every part of the system and creates dependencies everywhere.

### Platform Teams

Platform teams deserve special attention, both because of their importance and because of how frequently they are done badly. The role of the platform team is to provide common functions and services that stream-aligned teams can rely on to make their jobs easier.

A platform team's goal should be to enable stream-aligned teams to deliver work with substantial autonomy, allowing them to make progress independently of others -- including the platform team itself.

The book identifies several common mistakes in platform team implementation:

**The "leftovers" anti-pattern.** When defining a team structure, organisations typically adopt some organising principle for breaking up systems -- bounded contexts, for example. But often, there is a load of stuff left over that did not fit neatly into this division. A very common mistake is to group these leftovers together into the "platform," even though they are not obviously related to one another. This creates a dumping ground of unrelated concerns that becomes difficult to maintain, difficult to use, and a source of coupling between otherwise independent teams.

**The "grand design" anti-pattern.** Another common failing is the grand vision for the platform that must be complete in its entirety before anyone can sensibly make use of it. Progress is stalled, requiring all teams to wait to start work on a new feature until the perfect platform is built. This is the waterfall approach applied to internal tooling, and it has all the same problems: long feedback loops, speculative design, and a high risk of building something that does not match actual needs.

**The "pet project" problem.** Platform teams can become disconnected from the needs of stream-aligned teams, building what they find technically interesting rather than what their consumers actually need. This transforms the platform from an enabler into a barrier.

### Principles for Effective Platform Teams

The book offers several principles for building effective platform teams:

1. **Solve real problems for stream-aligned teams in a way that makes their work simpler, not more difficult.** The platform exists to serve its consumers, not the other way around.

2. **Meet long-term needs, not just respond to feature requests.** A purely reactive platform team becomes a ticket-processing factory. A purely proactive one builds things nobody uses. The balance is to understand the real needs of stream-aligned teams and design solutions that address those needs thoughtfully.

3. **Focus on ease-of-use from the perspective of consumers, even if that means doing more work in the platform code itself.** This is a version of the "smart endpoints, dumb pipes" principle from microservices architecture. The platform should absorb complexity so its consumers do not have to.

4. **Work incrementally in small steps and discover what really works over several iterations in real use.** Allow both the implementation and the vision to evolve in the face of reality. This is continuous delivery applied to platform development.

5. **Never force change on stream-aligned teams.** The goal of an effective platform should never be to dictate how consuming teams work. Instead, make the platform so useful and easy to adopt that teams choose to use it.

---

## Chapter 5: Cooperation and Collaboration

### The Autonomy Imperative

It is a big problem if every change to a system demands that several teams coordinate their work. It is much more effective when teams can make progress independently. But the book is careful to distinguish between independence and isolation. Teams should be autonomous, not disconnected.

If the aim is for teams to make progress with greater autonomy, that does not rule out the need for cooperation and collaboration. The key is that cooperation and collaboration must happen in ways that do not block independent progress.

### Recommendations for Effective Collaboration

The book provides a concrete set of recommendations for achieving this balance:

1. **Each team takes full responsibility for all aspects of its part of the system.** This means development, testing, operations, monitoring, security, and user experience for the bounded context they own. No passing the buck.

2. **Each team has the skills it needs to cope with most common aspects of their work.** The target is that 80% of the time, the team can make progress without any help.

3. **When they hit the difficult 20%, they can draft in expertise from an enabling team.** This is not a sign of weakness; it is a sign of a healthy, learning-oriented team.

4. **The expert's aim is twofold: work with the stream-aligned team to implement the new feature, and teach the stream-aligned team more about the speciality in context.** The expert leaves the team more capable than they found it.

5. **The aim of all non-stream-aligned teams is to reduce cognitive load in stream-aligned teams.** Enabling teams, complex subsystem teams, and platform teams all exist to make stream-aligned teams more effective. If they are not doing this, something is wrong.

### Two Approaches for Platform Team Collaboration

The book highlights two particularly effective approaches for platform teams that prevent them from forcing change on stream-aligned teams:

**Approach 1: Loosely coupled API design.** Work in ways that allow APIs to change without forcing stream-aligned teams to change their code. This means designing APIs for backward compatibility, using versioning strategies, and adopting patterns that decouple API consumers from implementation details. Techniques include semantic versioning, backward-compatible defaults, and feature flags.

**Approach 2: Consumer-driven change.** Work in ways that keep things working when the platform API changes. If a platform team needs to make a breaking change, they take the responsibility to update all of the consumers' code that uses the affected API. This shifts the burden of change from the many (stream-aligned teams) to the few (the platform team), which is the correct direction. It also creates a natural incentive for the platform team to maintain backward compatibility, because they are the ones who bear the cost of breaking it.

Both of these approaches embody a broader principle: the platform team should absorb complexity so that stream-aligned teams do not have to. This is the fundamental value proposition of a platform, and it is the yardstick by which a platform team's effectiveness should be measured.

---

## Chapter 6: Transforming Team Structure

### The Reality of Existing Organisations

Most organisations do not have the luxury of building their team structure from scratch. They have existing org charts, established teams, entrenched cultures, and legacy systems. The question is not "how would we design this if we were starting from zero?" but "what can we do to introduce better team roles and structure into an existing organisation?"

The book offers practical, incremental guidance for this transformation.

### Step 1: Create an Enabling Team

One of the most effective first steps is to create an enabling team whose mission is to promote and motivate the adoption of continuous delivery practices. This team lends expertise where required and builds infrastructure -- such as deployment pipelines -- to share with other teams.

This is a high-leverage starting point because it does not require restructuring the entire organisation. It adds a small, focused team that can begin making an immediate impact. The deployment pipeline infrastructure they build benefits everyone, and the practices they promote -- continuous integration, automated testing, small batch sizes -- naturally push teams toward greater autonomy and faster delivery.

### Step 2: Increase Dev Team Independence

Look at how the existing development teams can operate more independently. The goal is to reduce coupling and dependence between teams and recapture some of the energy, focus, and speed that the organisation had when it was young and small.

This often involves identifying the most painful cross-team dependencies and finding ways to eliminate them. Can a shared database be split so that each team owns its own data? Can a shared library be forked or replaced so that teams are not blocked waiting for changes? Can release cycles be decoupled so that teams can deploy on their own schedule?

### Step 3: Build Multi-Skilled Teams

Bring more software development functions together to create more multi-skilled teams, each aligned with a bounded context in the problem domain. This does not mean making teams bigger. The 5-to-9 person limit still applies. Instead, it means being thoughtful about which skills are combined and using temporary lending of expertise to fill gaps.

For example, rather than having a separate QA team, bring testing skills into each stream-aligned team. Rather than having a separate UX team, embed UX thinking into each team (or have an enabling team that temporarily embeds a UX specialist when needed). Rather than having a separate DevOps team, give each team the skills and tools to deploy and operate their own services.

### Step 4: Review Platform Team Effectiveness

Review the role of any existing platform teams. Are they genuinely making life simpler for stream-aligned teams? Or are they someone's pet project, a tactical hack that has grown beyond its usefulness, or a bottleneck that teams must wait for?

A good starting point for a platform team, or for improving an existing one, can be something incredibly simple. Maybe even just documentation that describes how to add a new service, or how to organise a directory structure to make it easy to find tests. The point is to start small, deliver something useful, and iterate from there based on real feedback.

### Step 5: Maintain Laser Focus on Stream-Aligned Teams

Maintain a laser focus on what stream-aligned teams need, and work to prioritise and service those needs. Check that these teams are able to make decisions about their work without control and interference from others. If a stream-aligned team cannot make a technical decision about their own service without getting approval from an architecture board, a platform team, or a manager who is not on their team, then the organisation has a structural problem that needs to be addressed.

### Step 6: Iterate Incrementally

Work incrementally in small steps and discover what really works over several iterations. Aim for teams of 5-9 people and agree on how larger teams can be reshaped into several smaller teams. Avoid big-hit restructuring and the disruption that ensues. Organisational change, like software change, is best done in small, reversible steps with frequent feedback.

### Step 7: Accept Extra Costs for Independence

Be willing to accept some extra costs in your design, as long as those costs allow teams to work more independently and therefore be more productive overall. This might mean some duplication of effort between teams, or a slightly more complex system architecture in exchange for loose coupling. The investment in independence pays dividends in speed, quality, and team satisfaction over the long term.

---

## Chapter 7: The Interplay Between Team Structure and System Architecture

### Co-Evolution of Organisation and Code

Throughout the book, a recurring theme is the deep connection between team structure and system architecture. This is not merely Conway's Law as an observation; it is Conway's Law as a design tool. The organisation and the system should co-evolve.

When teams are structured around bounded contexts in the problem domain, the natural tendency is for the software to evolve toward a modular architecture with clear boundaries between components. When teams are structured around functional specialities, the natural tendency is for the software to become a monolith with tangled dependencies.

This means that changing team structure is not just an organisational change; it is also an architectural change. And changing the system architecture -- introducing new service boundaries, for example -- may require corresponding changes in team structure. The two must be considered together.

### Maintaining the Ability to Change

The book emphasises that maintaining the ability to change code easily is a key attribute of good design, and one that liberates the value that platforms can deliver. If the platform or the system architecture makes it hard to change things, teams become reluctant to make improvements, technical debt accumulates, and the system gradually becomes rigid.

This is why loose coupling is so important at every level: between services, between teams, and between the platform and its consumers. Loose coupling is what allows independent progress, and independent progress is what allows teams to move fast.

### Cognitive Load as a Design Constraint

The book introduces cognitive load as an explicit design constraint for team organisation. Cognitive load theory, originally from educational psychology, refers to the amount of mental effort required to perform a task. In the context of software development, it encompasses the complexity of the domain, the codebase, the tooling, the deployment process, and the operational environment.

If a team's cognitive load is too high -- because they are responsible for too many services, or because the system they work on is poorly structured and hard to understand -- they will make more mistakes, move more slowly, and struggle to innovate. One of the key roles of enabling teams, complex subsystem teams, and platform teams is to reduce the cognitive load on stream-aligned teams, allowing them to focus on delivering business value.

---

## Chapter 8: Practical Patterns and Anti-Patterns

### Patterns to Embrace

**Small, cross-functional teams aligned to business domains.** This is the foundational pattern from which all others derive. Teams of 5-9 people with all the skills needed to deliver value in their domain.

**Temporary embedding of specialists.** Rather than creating permanent specialist teams that become bottlenecks, embed specialists into stream-aligned teams on a temporary basis to solve specific problems and transfer knowledge.

**Consumer-focused platform development.** Platform teams that measure their success by how much easier they make life for stream-aligned teams, not by the technical sophistication of their platform.

**Incremental, iterative improvement.** Making small changes, measuring the results, and adjusting course. This applies to team structure, platform development, and organisational transformation equally.

**Loose coupling at every level.** Between services, between teams, between the platform and its consumers. Loose coupling is the enabler of independent progress.

### Anti-Patterns to Avoid

**Functional silo teams.** Teams organised around technical specialities (frontend, backend, QA, DevOps) rather than business domains. These create cross-cutting dependencies that prevent any team from delivering value independently.

**The platform as a dumping ground.** Grouping unrelated "leftover" concerns into a platform team because they did not fit neatly elsewhere. This creates an incoherent platform that is hard to maintain and hard to use.

**The grand design platform.** Spending months or years building the perfect platform before anyone can use it. This blocks all teams and carries a high risk of building something that does not match real needs.

**Big-bang restructuring.** Attempting to reorganise the entire engineering department in one move. This causes massive disruption, destroys existing team dynamics, and often fails to achieve its goals.

**Forcing change on consuming teams.** Platform teams that dictate how stream-aligned teams must work, or that make breaking changes and expect all consumers to adapt immediately. This inverts the proper relationship between platform teams and their consumers.

**Ignoring cognitive load.** Assigning too many services, too many domains, or too much operational responsibility to a single team. This overloads the team and degrades their performance across all areas.

---

## Chapter 9: The Role of Continuous Delivery in Team Organisation

### Enabling Team Autonomy Through Technical Practices

While the book is primarily about team organisation, it is grounded in the "Better Software Faster" philosophy and the continuous delivery approach. The connection between team organisation and technical practices is bidirectional: good team structure enables good technical practices, and good technical practices enable good team structure.

Continuous delivery requires teams to be able to take a feature from conception through to production independently. This means each team needs the skills and tools to build, test, deploy, and operate their part of the system. It also means the system architecture must support independent deployment -- which brings us back to the importance of loose coupling and well-defined boundaries.

The enabling team's role in promoting continuous delivery practices is therefore not just a technical role; it is an organisational transformation role. By helping teams adopt practices like continuous integration, automated testing, and deployment pipelines, the enabling team is simultaneously helping them become more autonomous and more aligned with the stream-aligned team model.

### Deployment Pipelines as Infrastructure

The book specifically calls out deployment pipelines as an example of infrastructure that an enabling team can build and share. A deployment pipeline is an automated system that builds, tests, and deploys code changes. It is a foundational piece of infrastructure that every team needs, and providing a shared, well-maintained pipeline is a high-leverage way for an enabling team to make an impact.

The key is that the pipeline must be a shared service, not a shared bottleneck. Stream-aligned teams should be able to use the pipeline without needing to coordinate with the team that maintains it. This requires self-service tooling, clear documentation, and a focus on ease-of-use.

---

## Key Takeaways

### 1. Small teams win
Keep teams between 5 and 9 people. The exponential increase in communication complexity and cognitive load as teams grow makes large teams fundamentally less effective. This is not negotiable; it is backed by extensive research.

### 2. The team is the primary unit of work, not the individual
Everyone in the team shares the work and the responsibility to achieve shared goals. There are no solo performers carrying the team. Success and failure belong to the collective.

### 3. Minimise hand-offs between teams
Every hand-off introduces delay, information loss, and misalignment. Give teams the skills and responsibility to handle all aspects of their part of the system: development, testing, operations, security, and user experience.

### 4. Conway's Law is a design tool, not just an observation
Your organisation's communication structure will determine your system's architecture. Use this deliberately: structure your teams to produce the architecture you want, through the Inverse Conway Maneuver.

### 5. Align teams with business domains, not technical functions
Stream-aligned teams, aligned with bounded contexts in the problem domain, are the primary value-creating units. They should make up the majority of teams in the organisation. Functional silos (frontend, backend, QA, etc.) are an anti-pattern.

### 6. Support stream-aligned teams with three specialist team types
Enabling teams lend expertise and transfer knowledge. Complex subsystem teams handle technically specialised, narrow-domain components. Platform teams provide common infrastructure and services. All three exist to reduce cognitive load on stream-aligned teams.

### 7. Platform teams exist to serve their consumers
The measure of a platform team's success is how much easier they make life for stream-aligned teams. Avoid the "leftovers" anti-pattern, the "grand design" anti-pattern, and the "pet project" problem. Start simple, iterate, and focus on real consumer needs.

### 8. Design for loose coupling at every level
Between services, between teams, and between the platform and its consumers. Loose coupling is what enables independent progress. Use loosely coupled API design and consumer-driven change approaches to prevent platform teams from blocking stream-aligned teams.

### 9. Aim for the 80/20 skill balance
Teams should have the skills to handle 80% of their work without outside help. For the remaining 20%, bring in expertise from enabling teams. Over time, the team's skill base grows through this collaboration, reducing future dependence.

### 10. Transform incrementally, not in big bangs
Most organisations cannot redesign their team structure from scratch. Start by creating an enabling team, then gradually increase team independence, build multi-skilled teams aligned to business domains, and improve platform team effectiveness. Work in small steps and iterate.

### 11. Accept extra costs for independence
Be willing to accept some duplication of effort or architectural complexity in exchange for team independence. The long-term gains in speed, quality, and team satisfaction far outweigh the short-term costs.

### 12. Cognitive load is a design constraint
Do not overload teams with too many services, too many domains, or too much operational responsibility. One of the primary purposes of specialist team types is to reduce the cognitive load on stream-aligned teams, allowing them to focus on delivering business value.

### 13. Maintaining the ability to change is paramount
Good design -- of systems, of platforms, and of organisations -- preserves the ability to change easily. When change becomes difficult, progress slows, technical debt accumulates, and morale declines. Optimise for ease of change at every level.

### 14. Team structure and system architecture must co-evolve
Changes to team structure will affect system architecture, and vice versa. These two dimensions must be considered together, not in isolation. Technical leaders must be involved in organisational design decisions.

---

## Recommended Resources

The book concludes with a curated set of resources for further study:

- **Team Topologies** by Matthew Skelton and Manuel Pais -- the foundational text on the four team types and their interactions.
- **Importance of Small Teams** (QSM research) -- quantitative evidence for the superiority of small teams.
- **State of DevOps research** (DORA) -- the research behind the predictors of software delivery performance, including team autonomy.
- **Dave Farley and Randy Shoup (eBay VP of Engineering) discussion** -- a video conversation about the role of platforms and infrastructure teams, technical choices, and autonomy at large organisations.
- **How to Scale Software Teams** -- a video on practical approaches to scaling.
- **Tips for Building Successful Platform Teams** -- specific guidance for the most commonly mishandled team type.

---

*This summary covers the complete content of "How To Organise Software Development Teams" from the "Better Software Faster" series. The book's core message is that team organisation is not a secondary concern to be delegated to HR; it is a primary engineering decision that directly determines the quality, speed, and sustainability of software delivery. By structuring teams as small, cross-functional, stream-aligned units supported by enabling teams, complex subsystem teams, and well-run platform teams, organisations can achieve both speed and quality at scale.*
