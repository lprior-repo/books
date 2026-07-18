# Terraform at Scale - Comprehensive Summary

**Author:** Robert Glenn
**Publisher:** O'Reilly Media (Early Release, 2026)
**Subtitle:** Patterns, Practices, and Pitfalls of Enterprise Terraform and OpenTofu Development

---

## Note on Early Release

This is an Early Release edition containing 3 of the planned 15 chapters. The available chapters cover effective use of logic in Terraform (Chapter 3) and balancing state size with cardinality (Chapter 7). The remaining 12 chapters covering anti-patterns, built-in fields, tightly coupled projects, remote modules, enterprise operations, self-service, validation, and more were unavailable at the time of writing.

---

## Part 1: Foundations

### Chapter 3: Effective Use of Logic

This chapter provides a thorough examination of how to use HashiCorp Configuration Language (HCL) logic expressions effectively in Terraform, while understanding their limitations and knowing when to move logic outside of Terraform entirely.

#### Logic and Terraform

HCL is primarily a configuration language, not a general-purpose programming language. While it supports a wide variety of expressions and operators, its functional programming style can be confusing for engineers accustomed to object-oriented (Java, JavaScript), procedural (C), or scripted (Bash/PowerShell) paradigms. HCL functions operate in a functional programming style where statement results can be chained (the output of one becomes input to the next), but intermediate results are not preserved by default. HCL introduces the `locals{}` block to preserve arbitrary values for later reference.

The general recommendation is to externalize complex logic and minimize HCL functions. If working in a codebase that heavily leverages functions, the author recommends studying functional programming fundamentals.

#### Automated Logic Outside of TF

Terraform is typically embedded in automation tool DSLs (YAML, bash scripts). Containerized execution contexts allow custom container images with additional tools. Rather than using inline `sed`/`awk` commands, the author recommends using friendlier scripting languages like Python or JavaScript for complex logic -- code that can be tested and debugged in ways Terraform cannot. This logic can execute before Terraform (generating input variables) or after (interpreting outputs), and can even drive Terraform execution through CDK tooling for self-service solutions.

#### Manual Processes

Before robust automation is developed, manual procedures are necessary for managing TF project dependencies (copying output values between modules), calculating inputs, and remediating incidents. Manual processes have their place, especially in early exploratory work and when using provider configuration wizards to learn component structures. However, they scale poorly, are error-prone, and should be progressively encoded into programmatic procedures as systems mature.

The author recommends prioritizing which manual procedures to automate based on three dimensions: computational simplicity (easy to encode), frequency (how often they arise), and time sensitivity (urgency of execution). Procedures falling into all three categories should be automated first.

#### The "Messy Middle"

As TF adoption expands from one team to many, variation in structure and convention increases. While centralizing IaC expertise seems logical, pioneering techniques often emerge from teams developing the most complex solutions. The challenge is balancing "optimized" code with "shipped" code -- excessive variety is confusing and can lead to misuse, especially with similar but distinct TF expressions like `count` and `for_each`.

Refactoring working code is rarely a priority since benefits are hard to measure, but no one wants to navigate spaghetti code during a P1 incident. Clean-up sprints, "improve what you touch" policies, and refactor bounties can help pay down technical debt.

#### Things to Avoid

**Inline Logic:** Placing logic directly in field assignments (especially `for`/`in` expressions outside of `for_each`) creates unreadable, undebuggable code. Instead, place logic in `locals{}` blocks for clear decomposition and reference.

**Implicit Type Conversion:** Relying on TF to convert strings to numbers is sloppy and potentially issue-prone. Use explicit built-in type conversion functions instead.

#### Expressions

HCL supports several key expression types:

**Arithmetic and Logical Operators:** Standard operators (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `&&`, `||`, `!`) work as expected. These should be used judiciously in locals rather than inline.

**The for Expression:** Transforms one collection into another by iterating over elements and applying a projection. Can produce lists, maps, or objects. The author recommends storing results in locals for readability.

**The if Clause:** Used within `for` expressions to filter elements based on a condition. Can be combined with grouping syntax to create maps from filtered results.

**Ternary Conditional Expressions:** The `condition ? true_val : false_val` syntax is the primary conditional mechanism in HCL. Both branches must be type-compatible.

**String Interpolation and Directives:** `${}` for variable interpolation and `%{}` for conditional/iterative directives within strings. Useful for constructing resource names and descriptions, but excessive use creates hard-to-read code.

**Splat Expressions:** `[*]` and `.*)` operators for accessing attributes across all elements in a list. Useful shorthand but can be confusing when nested.

#### Functional Terraform

The chapter provides detailed guidance on using HCL's built-in function categories:

**String Functions:** `substr()` is commonly used with string interpolations to enforce maximum length constraints. `length()` determines string length. Use these when constructing input strings based on output values from other resources.

**Collection Functions:** Functions like `merge()`, `concat()`, `distinct()`, `flatten()`, `keys()`, `values()`, `lookup()`, and `contains()` operate on lists, maps, and sets. The `for` expression is the most powerful collection transformation tool. Use locals to store intermediate results for readability.

**The length() Function:** Returns the number of elements in a collection or characters in a string. Useful for conditional logic (e.g., `count = length(var.items) > 0 ? 1 : 0`).

**Encoding and Hash/Crypto Functions:** `base64encode()`, `base64decode()`, `md5()`, `sha256()`, `uuid()`, and similar functions for encoding, hashing, and cryptographic operations. Use these for generating unique identifiers and secure configurations.

**Filesystem Functions:** `file()`, `templatefile()`, `fileexists()`, `fileset()` for reading and templating files. `templatefile()` is particularly useful for generating configuration files from templates.

**Type Conversion and Safety Functions:** `tostring()`, `tonumber()`, `tobool()`, `tolist()`, `tomap()`, `toset()`, and `can()` / `try()` for safe type conversions. Always prefer explicit conversion over implicit.

**Sensitive Value Functions:** `sensitive()` marks values as sensitive, preventing them from appearing in logs and console output. `nonsensitive()` does the reverse.

**Other Functions:** Numeric functions (`abs()`, `ceil()`, `floor()`, `max()`, `min()`), IP network functions (`cidrsubnet()`, `cidrhost()`), and date/time functions (`formatdate()`, `timeadd()`).

---

## Part 2: Terraform Project Organization

### Chapter 7: Balancing State Size with Cardinality

This is the book's most extensive chapter, covering TF state management comprehensively -- from fundamental concepts through common problems to practical approaches for maintaining balance at enterprise scale.

#### State Concepts and Definitions

**State Backend:** The location where state is stored -- a local file, cloud storage bucket, or managed storage service. This is the source of truth for TF state, preserved at the time of the last `tf apply` operation. Without additional logic, a repository has a 1:1 relationship with a state backend.

**State Object (State Tree):** A tree-like JSON structure representing the state of instantiated services at the time of a `tf apply`. This is TF's "memory," recording what resources were observed and configured. The state object only records what was configured through `tf apply` -- it has no awareness of other resources, even those managed by separate TF states. It only constitutes a reliable source of truth immediately upon a successful apply.

**State Triplet:** The three-way relationship between the codebase, the state object, and the running resource instances. All three must be kept in alignment. Changing the backend (and successfully running an apply) effectively moves the TF state.

**State Address:** The location of a particular node in the state tree, addressed as a progressive path from the root node using dot notation (e.g., `module.network.google_compute_subnetwork.subnets["snet-01"]`).

**State Replication:** Using the same codebase with different backend fields and inputs to create additional states for domain separation. Effective for reselling standardized infrastructure or developing department-specific infrastructure.

**Importing State:** The `tf import` command brings existing resources under TF management without modifying them. This is useful when resources were configured manually but should be incorporated into IaC. After importing, a `tf plan` should show no changes if the code matches the resource configuration.

**State Trimming and Propagation:** `tf state rm` removes portions of a state object without destroying running resources. This is primarily useful when refactoring a codebase to split into multiple states. Because `tf state rm` does not remove running resources, a subsequent `tf apply` on an unaltered codebase will attempt to recreate the resource, potentially failing due to duplicates. Therefore, all state triplet operations (removing state, moving code, handling running resources) should be completed in one sitting.

#### Drift

TF is generally idempotent but runs only when triggered. It will not automatically detect changes made through platform CLIs, UIs, APIs, or other TF states. This creates configuration drift. When detected, TF will attempt to correct it, which sometimes forces resource recreation (destroying and recreating the resource).

#### Atomic States

Each TF state is completely ignorant of every other state. Each `tf apply` results in exactly one state object. Connections between states must be implemented outside the state triplet (through data sources, variable passing, etc.). Each state tree is atomic -- self-contained and independent.

#### Root Module

The root module is the module in the code repository against which `tf apply` is run. It serves as the root node of the state tree.

#### State Don'ts

**One-off Operations:** TF does not lend itself to operations that must be run exactly once. The `-target` option can focus operations on individual resources, but should be reserved for emergencies. Incorporating one-off operations into normal TF operation violates its idempotent nature and introduces ever-increasing overhead. Instead, use a "wildcard job" for specialized operations.

**Abusing the -target Option:** While `-target` allows focusing on specific resources, its regular use indicates systemic issues that should be addressed through refactoring. It should not be included in normal deployment pipelines. Overuse suggests the need to isolate problematic resources into separate states.

**Tightly-Coupled States:** States become tightly coupled when there is high dependency between them -- e.g., one state managing VPCs and firewalls while another manages subnets. Every VPC change requires coordinated changes to both states in a specific order. This creates cascading changes that require heightened coordination. Mutual interdependence (dependencies in both directions) is especially problematic and can even create change cycles.

**Lopsided State:** Avoid mixing module and resource blocks in the same root module, mixing different module types (complementary vs. disparate resources), and mixing collection nodes (`for_each`) with non-collection nodes. These automatically create imbalance.

**"Too Many Cooks":** Multiple teams working on a single repository causes friction with locked or broken states, especially when resources have divergent exposure levels, severity, or update frequency. Recommendations include formalized knowledge transfers before team transitions, strict deprecation periods, and refactoring resources into projects served by single teams.

**ClickOps:** Creating resources manually and then attempting to incorporate them into IaC is the antithesis of Infrastructure as Code. It doesn't scale, creates security risks, places excessive responsibility on specialists, and compounds with IaC to create effort greater than either approach alone. Reserve ClickOps for rapid prototyping, then design proper IaC.

#### State Do's

**Balanced States:** Develop code to keep the state tree reasonably balanced -- approximately equal volume of child nodes under each branch, with depth bounded by `2*log_x(n)` where x is the average branching factor.

**Environment-aligned State Objects:** Separate state by environment (production, staging, development). Implement environment graduation so changes are tested outside production first. Drive environmental differences through versioned remote modules and input variables. For ephemeral environments, choose between persistent backends (one at a time) and ephemeral backends (multiple concurrent).

**Clean Up Unused States:** Remove state objects when their resources are relocated or removed. Empty state files with non-empty objects confuse auditors. Clean state files demonstrate proper tracking.

**Domain-aligned Code Modules:** Group resources within the same technical domain together. Keep dependencies between projects to a minimum, with upstream projects changing slower than downstream. Eliminate mutual dependency loops.

**Lifecycle-aligned Code Modules:** Group resources that are updated in the same or related lifecycle. This allows bundled maintenance and separation of concerns.

#### Common State Problems

**Locked States:** State locks prevent concurrent writes but can block intentional operations. Aborted operations may leave locks in place, requiring manual intervention. Resolution involves deleting the lock file and reconciling the state triplet.

**"Broken" States:** Occur when the state object does not reflect reality, causing unexpected plans or outright failures. Common causes include: misusing `for_each` and `count`, ClickOps undoing IaC changes, data resources referencing managed resources with non-deterministic values, and version constraint mismatches. Resolution requires analyzing all three state triplet components.

**Gridlocked States:** The most severe problem -- any subsequent `tf apply` fails regardless of codebase state. Occurs when an unsuccessful apply cannot fully undo its operations (e.g., a protected resource is created but the overall apply fails, and the protected resource cannot be cleaned up by rollback). Options include removing the resource through other means or removing the offending code.

**Bloated States:** Overly large state trees cause severe slowdowns to `tf plan` and `tf apply`. The blast radius of a broken or locked state is the entire state tree, so self-contained states are recommended. Breadth is preferred to depth (high leaf-to-module ratio). The balance between data references and state size is a key indicator of maintainability.

**Too Many States:** The opposite extreme, typically caused by separating by service type or product offering. If you need a spreadsheet to track your states, you have too many. Address by combining states that share lifecycles and domains.

**Unbalanced States:** Excessive depth or uneven distribution of activity makes troubleshooting difficult. Changes at leaf nodes cascade up the hierarchy to the root. Uneven activity distribution (a few frequently-changed resources mixed with many rarely-changed ones) suggests unnatural coupling.

**Never-Clean States:** Occur when non-deterministic data sources break TF's idempotence. Every `tf plan` reports changes, even when no intentional modifications were made. Fix by constructing field values in the preferred format that matches the state object.

#### Common Approaches

**Approach 1: Backend Key Variation:** Use the same codebase with multiple state backends by partially configuring the backend and passing the key/prefix at execution time via `-backend-config`. This creates distinct state objects for different environments or workloads from a single codebase. Store backend configurations securely (e.g., in HashiCorp Vault).

**Approach 2: Distinct Variable Files:** Provide distinct `.tfvars` files for each state. Structure variable precedence carefully: environment variables (first, use sparingly) > `terraform.tfvars` (common configs) > `*.auto.tfvars` (overrides, use at most one) > `-var` and `-var-file` (most control). Don't mix `.auto.tfvars` with `-var-file`. For truly immutable values, encode them as locals in a protected file.

**Approach 3: Graduated Environment Configuration:** Apply infrastructure for each environment at different release stages (Development in Integration stage, Test in Staging, Production in Deploy). The main risk is experimental features in lower environments blocking urgent patches to all environments. Best suited for piloting new services in sandbox environments outside the application lifecycle.

**Approach 4: Versioned Environment Modules:** Configure entire environments as remote modules, applied through root modules with version references. This simplifies patch application to a single line of code (the module version), though it doesn't fully resolve the leapfrog risk.

**Approach 5: "Wildcard Jobs":** Develop automation jobs that support flexible TF operations with a variety of flags and free text. Protect them with RBAC/ABAC access controls, require temporary elevated permissions, identify the human operator (not the automation identity) in all actions, and always freshly clone the source repository. Record all operations consistently for audit purposes.

#### Common Scenarios

**Scenario 1: Organizational Scaling:** When teams grow and split, TF projects must follow. Example procedure: create new repository, copy relevant code, run `tf plan` to discover import addresses, import resources one by one, confirm imports, run `tf state rm` to remove resources from old state, confirm removals.

**Scenario 2: Reducing Duplication:** Refactor massive flat TF files with repeated resource blocks into modular configurations. Create local modules with `for_each` for repeated resource types, construct per-workload `.tfvars` files, refactor root modules, vary backend keys, then import resources into new states and remove from old states. Track "from" and "to" state addresses in a shared spreadsheet.

**Scenario 3: Merger/Acquisition:** Integrate two companies' TF ecosystems. Two options: consolidate resources into one account (recreating some) or construct a second provider configuration block to manage the other account's resources. Both require careful import/removal procedures and tracking of state address mappings.

**Scenario 4: Organizational Change Management:** Reorganizing TF projects during corporate reorgs -- a many-to-many transformation. Create new repositories, copy and refactor code, construct new modules, import resources across all new repositories, confirm imports, remove from old states, and confirm removals. This is typically a "big bang" operation performed by a single individual or very small team with temporary elevated permissions.

---

## Key Takeaways

1. **HCL is a configuration language, not a programming language.** Keep logic simple, use locals for intermediate values, and externalize complex logic to Python, JavaScript, or other full-featured languages.

2. **The state triplet (code, state object, running resources) must be kept in alignment.** Any operation that modifies one element must account for the other two. Complete all triplet operations in one sitting.

3. **State is TF's memory and is inherently point-in-time.** It does not automatically detect external changes and only reflects reality immediately after a successful `tf apply`.

4. **Avoid tightly-coupled states.** Dependencies between states create cascading changes that require coordination. Minimize cross-state dependencies and eliminate mutual dependency loops entirely.

5. **Keep state trees balanced and reasonably sized.** A bloated state has excessive blast radius when problems occur. Too many states create management overhead. Find the right granularity through domain and lifecycle alignment.

6. **Reserve dangerous operations for emergencies.** The `-target` option, `tf state rm`, and manual state manipulation should be exceptional, governed by policy, and executed through controlled "wildcard jobs."

7. **ClickOps is the enemy of IaC.** Manual resource creation does not scale, creates security risks, and compounds problems when mixed with Terraform. Reserve it for rapid prototyping only.

8. **Plan for organizational change.** Teams grow, split, merge, and reorganize. Structure TF projects so they can be split and recombined without recreating resources. Track state address mappings during transitions.

9. **Variable precedence matters.** Structure `.tfvars` files thoughtfully, use locals for immutable values, and don't mix `*.auto.tfvars` with `-var-file` options.

10. **Everything is production.** All infrastructure -- even development environments -- should be treated with production-quality practices. The only difference between environments should be the stage at which changes are applied.
