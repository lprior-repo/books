# Terraform at Scale

**Author:** Robert Glenn
**Topic tags:** `#architecture` `#devops` `#cloud`
**Language focus:** HashiCorp Configuration Language (HCL) / Terraform / OpenTofu (language-agnostic)
**Sources:** `markdown_output/Terraform_at_Scale_Early_Release/Terraform_at_Scale_Early_Release.md` · `summaries/Terraform_at_Scale_Early_Release.md`

> Note on source: this file is an Early Release covering Chapter 3 (Effective Use of Logic) and Chapter 7 (Balancing State Size with Cardinality). The remaining 12 planned chapters are unavailable in the public source. Cluster scope is therefore concentrated on these two deep chapters, with a forward look from the planned TOC.

## TL;DR

This book argues that Terraform is a configuration framework, not a programming language, and that scale pains come from a small set of predictable choices: how you express logic in HCL, the structure of your state objects, and the boundaries you draw between repositories and teams. Apply it when you need to grow past the "one team, one repo" stage and need durable guidance on state organization, role boundaries, refactor procedures, and anti-patterns that do not show up until an incident.

---

## Best Practices by Topic

### HCL is a Configuration Language, Not a Programming Language

**Principle:** Treat HCL as a constrained configuration DSL; reach for a full language (Python/JavaScript/CDK) when logic exceeds what a `locals{}` block can hold.

**Do:**
- Keep logic flat: one concern per `locals{}` block, with descriptive names.
- Externalize complex logic into a tested scripting language (Python, JavaScript) that runs before or after `tf apply`.
- Preserve intermediate results in `locals{}` rather than chaining function calls inline.
- Study functional programming basics if your codebase uses `for` expressions heavily.

**Don't:**
- Use inline `for`/`in` expressions outside of `for_each` meta-arguments.
- Rely on implicit type conversion of strings to numbers/booleans.
- Treat HCL as a substitute for a real language once you start wrestling with cases it was not designed for.

**Code:**
```hcl
# Externalized logic: a Python step computes variable values, then writes tfvars.json
# (the source repo lists this as the recommended pattern over inline sed/awk in pipelines).
# reasoning: "Unlike HCL, Python can be tested and stepped through with a debugger."
```
*Ref: Terraform_at_Scale_Early_Release.md — "Logic and TF" / "Automated Logic Outside of TF"*

---

### The Functional Programming Style of HCL Functions

**Principle:** HCL functions chain results input-to-output without preserving intermediates; compensate by storing named values in `locals{}`.

**Do:**
- Map function calls to a method-chaining mental model — output of inner becomes input of outer.
- Adopt standard naming (e.g. `k`, `v` or descriptive names) for `for` expression iterators and publish the convention.
- Reach for the documentation when reading unfamiliar combinators; assume nothing.

**Don't:**
- Inline deeply nested function chains in resource argument fields.
- Assume function results are preserved for later statements.

**Code:**
```hcl
locals {
  result = trimspace(substr(module.upstream.output_value, 0, 8))
}
```
*Ref: Terraform_at_Scale_Early_Release.md — "Terraform Functions and Expressions"*

---

### Manual Processes Have a Place Early, but Must Be Encoded

**Principle:** Automate procedures that are computationally simple, frequent, and time-sensitive — anything in all three boxes goes first.

**Do:**
- Walk provider configuration wizards early to learn what resources get created in the background.
- Use system access logs to discover implicit resources created alongside an explicit one.
- Triangulate on three dimensions (simple, frequent, time-sensitive) when sequencing automation work.

**Don't:**
- Add a permission to 100 IAM groups one at a time through a UI.
- Store reusable manual procedures in someone's head; they always become a P1 incident.

*Ref: Terraform_at_Scale_Early_Release.md — "Manual Processes"*

---

### The "Messy Middle" and Multi-Team Adoption Drift

**Principle:** Variation across teams is unavoidable; tame it with standards and refactoring ceremonies, not central command.

**Do:**
- Run clean-up sprints, "improve what you touch" policies, and refactor bounties.
- Document and publish standards for `for_each` vs `count`, locals vs variable defaults, etc.
- Allow pioneering techniques to emerge from teams with the hardest problems.

**Don't:**
- Centralize IaC expertise as a "mastermind unit" that never touches production complexity.
- Treat refactoring of working code as optional — no one navigates spaghetti in an incident willingly.

*Ref: Terraform_at_Scale_Early_Release.md — "The 'Messy Middle'"*

---

### Inline Logic Anti-Pattern

**Principle:** Logic inline in field assignments is hard to read and impossible to debug step-by-step.

**Do:**
- Use `locals{}` for any non-trivial computation.
- Restrict inline string interpolation to narrow idioms (`name`, `description`) inside `for_each` blocks.
- Decompose complex values into named locals for traceability.

**Don't:**
- Place `for`/`in` expressions inline in arbitrary resource argument fields.
- Mix too many variables into the same inline interpolation.

*Ref: Terraform_at_Scale_Early_Release.md — "Things to Avoid / Inline Logic"*

---

### Implicit Type Conversion Anti-Pattern

**Principle:** Always use explicit HCL type-conversion functions rather than relying on TF to coerce types.

**Do:**
- Use `tonumber()`, `tobool()`, `tostring()` etc. when converting values from external sources.
- Validate inputs against pattern via `variable "x" { validation { condition = can(tonumber(var.x)) } }`.

**Don't:**
- Slice a string like `'myinstance_m32_d120'` and rely on TF to interpret the substrings as integers.
- Assume converted values will fail safely; they may quietly apply the wrong type.

*Ref: Terraform_at_Scale_Early_Release.md — "Things to Avoid / Implicit Type Conversion"*

---

### Arithmetic and Logical Operators

**Principle:** TF operators follow standard precedence; `!` and negation are best reserved for values flowing between modules.

**Do:**
- Use `>`, `>=`, `<`, `<=`, `==`, `!=` where the logic requires them.
- Use modulo (`%`) for uniform spreading across sets (regions, subnets, AZs).
- Document a style standard for `count = condition ? 1 : 0` so `1`/`0` ordering is consistent.

**Don't:**
- Inline `+`/`-` outside well-defined offsets.

**Code:**
```hcl
resource "google_compute_firewall" "https-fw" {
  count = !(var.http_only) ? 1 : 0
  name  = var.https_firewall_name
  network = var.vpc_network
  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
}
```
*Ref: Terraform_at_Scale_Early_Release.md — "Arithmetic and Logical Operators" / Example 1-1*

---

### Modulo for Uniform Spreading Across Regions

**Principle:** Use `%` on a stable index to distribute workloads evenly across a fixed set of zones/regions.

**Do:**
- Pair modulo with a `slice()` on the discovered regions list.
- Document the cardinality assumption (e.g. "expect 3 regions").

**Code:**
```hcl
locals {
  three_supported_regions = slice(data.google_compute_regions.available.names, 0, 3)
}

resource "google_compute_instance" "vm-instances" {
  for_each = { for idx, vm in var.vm_instance : vm.name => merge(vm, { index = idx }) }
  name         = each.value.name
  machine_type = each.value.machine_type
  zone         = local.three_supported_regions[each.value.index % 3]
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-2*

---

### The `for` Expression — Map Outputs for `for_each`

**Principle:** When the result drives a `for_each`, produce a map; when it flows out of a module as an output, produce a list.

**Do:**
- Use `{ for k, v in collection : k => transformed_value }` for `for_each` inputs.
- Use `[ for x in collection : transformed ]` for module outputs.
- Do not nest `for` expressions; break each into its own local.

**Don't:**
- Chain `for` expressions in a single line.
- Mix temporary symbol conventions in the same codebase.

**Code:**
```hcl
resource "google_compute_firewall" "fws" {
  for_each = var.config_map
  name     = each.value.firewall_name
  network  = each.value.network_name
  allow {
    protocol = "tcp"
    ports = [
      for item in var.port_data : item.port if item.protocol == "tcp"
    ]
  }
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-3*

---

### The `if` Clause for Filtering Iterations

**Principle:** Use `if` clauses as the final predicate of a `for` expression to filter, not as a generic conditional.

**Do:**
- Build multiple filtered locals (each with a different `if` clause) for distinct views of the same collection.
- Give each local a name that advertises its uniqueness.

**Don't:**
- Use `if` outside a `for` expression — that is not how HCL conditional logic works.

**Code:**
```hcl
resource "google_compute_disk" "attached-disks" {
  for_each = {
    for key, vm in var.vm_inputs : key => vm
    if vm.has_attached_disk
  }
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-4*

---

### Multiple `if` Clauses Live Better in Locals

**Principle:** Distinct filtered views should live as named locals, never as inline mappings.

**Code:**
```hcl
locals {
  vms_with_attached_disks = {
    for key, vm in var.vm_inputs : key => vm
    if vm.has_attached_disk
  }
  vms_needing_second_nic = {
    for key, vm in var.vm_inputs : key => vm
    if vm.has_second_nic
  }
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-5*

---

### Ternary Conditional Expressions

**Principle:** `condition ? if_true : if_false` is the primary conditional form in HCL; both branches must be type-compatible.

**Do:**
- Use ternary to gate resource/module creation via `count`.
- Use ternary to provide a safe default when a value might be null.

**Don't:**
- Use ternary for trivial booleans in deeply nested expressions (use `try()`/`can()` instead).

**Code:**
```
BOOLEAN_STATEMENT ? IF_TRUE_RESULT : IF_FALSE_RESULT
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-6*

---

### Null-Safe Ternary When Outputs May Be Absent

**Principle:** Protect against null values flowing from upstream modules by short-circuiting with the identity element.

**Code:**
```hcl
numberField = module.remote-module.complex_output.possibly_null ? length(module.remote-module.complex_output.possibly_null) : 0
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-7*

---

### String Interpolation and Directives

**Principle:** `${}` for variable interpolation; `%{ if/endif/for %}` only when the rendered text is long and the variations are few.

**Do:**
- Use string interpolation for constructing longer strings from small building blocks.
- Use directives only when the resulting strings are long and similar.
- Construct complex strings in `locals{}` rather than inline.

**Don't:**
- Use directives for short, very different results (use ternary).
- Add newline characters via interpolation when a heredoc would be cleaner.

**Code:**
```hcl
variable "vms_map" {
  type = map(object({
    app_id      = string
    zone        = string
    machine_type = string
  }))
}

resource "google_compute_instance" "vms-collection" {
  for_each    = var.vms_map
  name        = "vm-${each.value.app_id}-${each.value.machine_type}"
  description = "${each.value.type} vm for app ${each.value.app_id}"
  zone        = each.value.zone
  machine_type = each.value.machine_type
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-8*

---

### Augmenting Locals for Cleaner Composition

**Principle:** Compute `name`, `description`, and other string-built fields inside `locals{}`, then reference in the resource block.

**Code:**
```hcl
locals {
  augmented_vms_map = {
    for vm in var.vms_map : vm => merge(
      vm,
      {
        name = "vm-${vm.app_id}-${slice(vm.machine_type, 0, 2)}-${slice(vm.zone, 0, 6)}"
        description = "Dedicated ${vm.machine_type} vm for app ${vm.app_id}"
      }
    )
  }
}

resource "google_compute_instance" "vms-collection" {
  for_each    = local.augmented_vms_map
  name        = each.value.name
  description = each.value.description
  zone        = each.value.zone
  machine_type = each.value.machine_type
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Figure 1-1*

---

### Directives vs Ternary — Pick the Readable One

**Principle:** Most `if/endif` directives can be replaced by a ternary and interpolation, and the ternary is usually clearer.

**Code:**
```hcl
locals {
  high_or_low  = var.random > 0.5 ? "better than 50/50" : "worse than 50/50"
  no_directive = "The answer is ${local.high_or_low}"
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-9*

---

### Splat Expressions

**Principle:** `[*]` and `.*)` are shorthand for projecting a field across all elements of a list of resources.

**Do:**
- Use splat in module outputs that feed downstream modules (compact list of IDs).
- Pair splat with `toset()` and `tostring()` when the upstream type is loose.

**Don't:**
- Expect splat to filter — it has no predicate form; use `for` with `if` for that.

**Code:**
```hcl
output "vm_boot_disk_sources_splat" {
  value = google_compute_instance.gce-vms[*].boot_disk.source
}

# Equivalent for expression
output "vm_boot_disk_sources_for" {
  value = [
    for vm in google_compute_instance.gce-vms : vm.boot_disk.source
  ]
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-10*

---

### `substr()` and `length()` for Length Compliance

**Principle:** Use `substr()` to cap interpolated strings, and `length()` to validate minimums and produce aggregate indicators.

**Code:**
```hcl
locals {
  first_item  = substr(data.google_compute_machine_types.example, 0, 8)
  second_item = substr(data.google_compute_zones.available.names[0], 0, 10)
  final_string = "vm-${local.first_item}-${local.second_item}"
}

output "vms_count" {
  description = "Count of vms created by this module"
  value       = length(google_compute_instance.vms-list)
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Examples 1-11, 1-17*

---

### Collection Functions: `concat()`, `merge()`, and Overrides

**Principle:** `concat()` for lists, `merge()` for maps; merge lets later values override earlier ones — useful for layering defaults.

**Code:**
```hcl
list_1 = [0, 1, 2, 3]
list_2 = ['a', 'b', 'c']
big_list = concat(list_1, list_2, ['inline', 'list'])

# merge() with override pattern
locals {
  vm_config_default = { vm_type = "n1-standard-1", disk_size_gb = 20 }
  vm_config_final   = merge(local.vm_config_default, var.vm_override_map)
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Examples 1-12, 1-13*

---

### `matchkeys()` vs For-Expression Filtering

**Principle:** When the collection needs reshaping, prefer a `for`/`if` for readability over `matchkeys()`.

**Code:**
```hcl
# Less accessible: matchkeys pattern
locals {
  filter_keys   = ["app_name", "region"]
  vals          = values(var.config_map)
  keys          = keys(var.config_map)
  using_matchkeys = matchkeys(local.vals, local.keys, local.filter_keys)
}

# More accessible: for + if
locals {
  filter_keys = ["app_name", "region"]
  using_for = [
    for ikey, ival in var.config_map : ival
    if contains(local.filter_keys, ikey)
  ]
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-14*

---

### Set Functions and Cartesian Products

**Principle:** `setproduct()` shines when you need resources for every combination of two independent sets (e.g. subnets for VPC × region).

**Do:**
- Use `setintersection()`, `setunion()`, `setsubtract()`, `setproduct()` sparingly and only when the combinatorial pattern is unavoidable.
- Document the cardinality assumptions explicitly.

**Code:**
```hcl
locals {
  vpc_names      = ['vpc-dev', 'vpc-test', 'vpc-prod']
  subnet_regions = ['us-west1', 'us-east1', 'us-central1']
  zones          = ['trust', 'non-trust']
  to_create      = setproduct(local.vpc_names, local.subnet_regions, local.zones)
  # produces 18 tuples, one per (vpc, region, zone)
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-15*

---

### `transpose()` to Flip Map Keys with Values

**Principle:** When the upstream module outputs `vpc_name -> [regions]`, `transpose()` yields `region -> [vpc_names]` for free.

**Code:**
```hcl
locals {
  regions_per_vpc = { for vpc in module.networks : vpc.name => vpc.regions }
  vpcs_by_region  = transpose(local.regions_per_vpc)
}
# regions_per_vpc: { "vpc-123": ["us-central1", "us-west1"], "vpc-456": ["us-central1", "us-east1"] ... }
# vpcs_by_region : { "us-central1": ["vpc-123", "vpc-456"], ... }
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-16*

---

### Encoding and Hash Functions

**Principle:** Reach for `base64encode()`, `sha256()`, `uuid()`, `uuidv5()` for IDs and signatures — never for confidentiality.

**Do:**
- Use `base64encode()` for safe text encoding only. Encoding is not encryption.
- Use `uuidv5()` when you need deterministic IDs derived from a namespace.

**Don't:**
- Mistake `base64encode()` for `encrypt()`. Use `rsadecrypt()` only for decryption; do encryption outside TF.

*Ref: Terraform_at_Scale_Early_Release.md — "Effective Use of Encoding and Hash/Crypto Functions"*

---

### Filesystem Functions

**Principle:** `file()`, `templatefile()`, `fileexists()` are useful but the files must exist on the executor's filesystem before `tf plan`.

**Do:**
- Use `templatefile()` to render startup scripts that get shipped to compute instances.
- Use `path.module`, `path.root`, `path.cwd`, `terraform.workspace` for stable references.

**Don't:**
- Use `file()` to load secrets — sensitive data should never be on the executor's disk.

*Ref: Terraform_at_Scale_Early_Release.md — "Effective Use of Filesystem Functions"*

---

### Type Conversion & Safety Functions

**Principle:** Prefer explicit `tostring()`, `tonumber()`, `tobool()`, `tolist()`, `tomap()`, `toset()` over implicit coercion.

**Do:**
- Use `try()` to provide defaults for nullable upstream values.
- Use `can()` exclusively inside variable validation rules.
- Keep `try()` scope tight — wrap only the specific attribute reference at risk.

**Don't:**
- Mix boolean→number or number→boolean conversions; use `boolVal ? 1 : 0` instead.

**Code:**
```hcl
# UNSAFE: try wraps too much
try(tostring(local.raw_value.name), null)

# SAFE: try wraps only the attribute reference
tostring(try(local.raw_value.name, null))
```
*Ref: Terraform_at_Scale_Early_Release.md — Example 1-19*

---

### Sensitive Value Functions

**Principle:** Mark variables and outputs `sensitive = true`; `sensitive()` / `nonsensitive()` are escape hatches, not defaults.

**Do:**
- Configure secrets systems (Vault, AWS Secrets Manager, GCP Secret Manager) to inject values; let TF reference them via data sources.
- Use `nonsensitive()` only when you have derived a new value that demonstrably strips the secret.

**Don't:**
- Mark a derived value sensitive and then rely on `sensitive()` again — once it's been printed, the moment is lost.

*Ref: Terraform_at_Scale_Early_Release.md — "Effective Use of Sensitive Value Functions"*

---

### Numeric, IP Network, and Date/Time Functions

**Principle:** Use `cidrhost()`, `cidrsubnet()`, `cidrsubnets()`, `cidrnetmask()` for VPC math; use `formatdate()` / `timeadd()` for time-bound resources; pair `timestamp()` with `ignore_changes` to avoid idempotence breaks.

**Do:**
- Compute complex CIDR hierarchies externally (Python) and feed them via variables when possible.
- Use `plantimestamp()` inside `check{}` blocks for evaluating expiry pre-apply.

**Don't:**
- Use `timestamp()` for security certificates or temporary credentials — handle those outside TF entirely.

*Ref: Terraform_at_Scale_Early_Release.md — "Effective Use of Other Functions (Numeric, IP Network, and Date/Time)"*

---

### State Backend

**Principle:** The state backend is the source of truth, populated at the time of the last successful `tf apply`.

**Do:**
- Choose a remote backend that supports locking (S3+DynamoDB, GCS, Terraform Cloud).
- Treat backend configuration as code — store sensitive parts in Vault, not in the repo.
- Configure `prevent_destroy` on critical resources when the state mutation risk is high.

**Don't:**
- Mix local backends between team members — concurrent edits will silently corrupt state.

*Ref: Terraform_at_Scale_Early_Release.md — "State Backend"*

---

### State Object (Tree)

**Principle:** The state object is a tree-like JSON structure (technically a DAG), populated by `tf apply`.

**Do:**
- Visualize the state tree during reviews to spot depth imbalances.
- Prefer breadth over depth: many leaves under each module beats deeply nested modules.

**Don't:**
- Assume the state object reflects reality more than one apply old — it is a point-in-time snapshot.

*Ref: Terraform_at_Scale_Early_Release.md — "State Object"*

---

### State Triplet — Code, State, Running Resources

**Principle:** There are three legs of the triplet; change must update all three in one sitting.

**Do:**
- Run any `tf import` / `tf state rm` / `tf apply` sequence atomically and validate with `tf plan` between steps.
- Record "from" and "to" addresses in a shared spreadsheet during migrations.

**Don't:**
- Run `tf state rm` on Friday afternoon and plan to clean up after lunch on Monday.

**Code:**
```
# Validate a successful import:
$ tf plan
# should report zero changes if the resource config matches
```
*Ref: Terraform_at_Scale_Early_Release.md — "State Triplet" / "Importing State"*

---

### State Address

**Principle:** State addresses are progressive dot-separated paths from the root module.

**Code:**
```
# module.network.google_compute_subnetwork.subnets["snet-01"]
# This is what tf import / tf state rm expect
```
*Ref: Terraform_at_Scale_Early_Release.md — "State Address"*

---

### State Replication and Variable Configuration

**Principle:** One codebase can service multiple state backends via partially-configured backends + variable files; perfect for resold standardized infrastructure.

**Do:**
- Partially configure backend `key`/`prefix`, supply the rest via `-backend-config` at `tf init`.
- Pair this with distinct `.tfvars` files per workload.

**Don't:**
- Hard-code the full backend config in the repo when you need multiple states from the same code.

*Ref: Terraform_at_Scale_Early_Release.md — "State Replication" / Approach 1*

---

### Importing Existing Resources into TF

**Principle:** `tf import` adds a resource to state without modifying the running instance; the code must already describe the resource accurately.

**Code:**
```
$ tf plan
Terraform will perform the following actions:
  # google_compute_subnetwork.tas-7-5-snets["snet-03-..."] will be created
  + resource "google_compute_subnetwork" "tas-7-5-snets" { ... }

$ tf import 'google_compute_subnetwork.tas-7-5-snets["snet-03-..."]' terraform-at-scale-book/us-east1/snet-03-...
google_compute_subnetwork.tas-7-5-snets["snet-03-..."]: Importing from ID "..."...
google_compute_subnetwork.tas-7-5-snets["snet-03-..."]: Import prepared!
google_compute_subnetwork.tas-7-5-snets["snet-03-..."]: Refreshing state...
Import successful!
```
*Ref: Terraform_at_Scale_Early_Release.md — Figure 2-5*

---

### State Trimming and Propagation

**Principle:** `tf state rm` removes from state, not from the cloud; the next `tf apply` against unmodified code will try to recreate it.

**Do:**
- Complete state trim, code move, and resource destroy in one window.
- Use `tf state rm -dry-run` first to preview.

**Don't:**
- Treat `tf state rm` as a delete-from-cloud operation.

*Ref: Terraform_at_Scale_Early_Release.md — "State Trimming & Propagation"*

---

### Drift

**Principle:** TF only sees drift when you ask — UIs, CLIs, and other stateful systems are invisible until next `tf plan`/`apply`.

**Do:**
- Detect drift on a cron or post-deploy hook.
- Force `refresh = true` or rely on plan's refresh phase to surface it.

**Don't:**
- Allow ClickOps without then immediately `tf apply`ing the same change to absorb it.

*Ref: Terraform_at_Scale_Early_Release.md — "Drift"*

---

### Atomic States

**Principle:** Each TF state is fully ignorant of all other states. Connections must be built via data sources, not co-owned resources.

**Do:**
- Cross-reference via `data` blocks and `terraform_remote_state` outputs.
- Document cross-state trust boundaries.

**Don't:**
- Encode the same resource in two states — even as a "temporary" measure.

*Ref: Terraform_at_Scale_Early_Release.md — "Atomic States"*

---

### One-Off Operations Are a TF Anti-Pattern

**Principle:** `-target` and one-off operations violate TF's idempotence and add overhead that compounds.

**Do:**
- Build a governed "wildcard job" for emergencies (gated by RBAC/ABAC, always fresh clone).
- Use `-target` only when the alternative is a P1 incident.

**Don't:**
- Bake `-target` into normal pipelines.

*Ref: Terraform_at_Scale_Early_Release.md — "One-Off Operations"*

---

### Avoid `-target` in Production Pipelines

**Principle:** `-target` indicates a systemic issue that should be fixed by refactoring, not normalized.

**Do:**
- Refactor problematic resources into their own state.
- Reserve `-target` for emergency hotfix workflows with strict access policies.

*Ref: Terraform_at_Scale_Early_Release.md — "Abusing the -target Option"*

---

### Tightly-Coupled States

**Principle:** Mutual dependencies between states cause cascading changes that may even cycle.

**Do:**
- Identify upstream/downstream roles explicitly; upstream should change slower.
- Eliminate any project that depends on another project that depends back on it.

**Don't:**
- Mix VPC/firewall ownership with subnet ownership across projects.

*Ref: Terraform_at_Scale_Early_Release.md — "Tightly-Coupled States"*

---

### Lopsided State

**Principle:** Three automatic imbalance patterns to avoid: modules mixed with resources, complementary vs disparate module types, and `for_each` nodes next to non-collection nodes.

**Do:**
- Place homogeneous module types together; isolate complementary within their own module.

**Don't:**
- Use `for_each` outside the root module without good reason.

*Ref: Terraform_at_Scale_Early_Release.md — "Lopsided State"*

---

### Too Many Cooks — Multi-Team Single-Repo Friction

**Principle:** Locked and broken states disproportionately affect teams that don't own the offending resource.

**Do:**
- Formalize KT before role transitions and enforce IAM access auto-expiration.
- Refactor resources into projects served by single teams.

*Ref: Terraform_at_Scale_Early_Release.md — "Too Many Cooks"*

---

### ClickOps Is the Antithesis of IaC

**Principle:** Manual provisioning is acceptable for prototypes; once it is "pilot," move it to code.

**Do:**
- Use the configuration wizard to learn what side-effects get created.

**Don't:**
- Mix ClickOps and IaC on a single resource — the result is work > IaC + ClickOps.

*Ref: Terraform_at_Scale_Early_Release.md — "ClickOps"*

---

### Environment-Aligned State Objects

**Principle:** Separate state by environment; drive differences via versioned remote modules and input variables.

**Do:**
- Implement environment graduation: try new features in sandbox before production.
- Drive env differences via remote modules + variables rather than parallel codebases.

*Ref: Terraform_at_Scale_Early_Release.md — "Environment-aligned State Objects"*

---

### Domain-aligned and Lifecycle-aligned Code Modules

**Principle:** Group resources by technical domain, then by update lifecycle, then minimize dependencies.

**Do:**
- Co-locate resources of the same domain (e.g. all network components for a workload) within a single module.
- Make the upstream project change slower than the downstream.

**Don't:**
- Lump unrelated resources in one state to "simplify."

**Code:**
```hcl
# Network domain
resource "google_compute_network" "tas-7-8-vpc" {
  project = "terraform-at-scale-book"
  name    = "vpc-terraform-at-scale-7-8"
}

resource "google_compute_subnetwork" "tas-7-8-snet" {
  project       = "terraform-at-scale-book"
  name          = "subnetwork-terraform-at-scale-7-8"
  ip_cidr_range = "10.0.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.tas-7-8-vpc.id
}

resource "google_compute_firewall" "tas-7-8-fw" {
  project = "terraform-at-scale-book"
  name    = "firewall-terraform-at-scale-7-8"
  network = google_compute_network.tas-7-8-vpc.self_link
  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Figure 2-7*

---

### Common State Problems — Locked, Broken, Gridlocked, Bloated, Never-Clean

**Principle:** Recognize the failure modes to address them proactively; a gridlocked state is the worst.

**Do:**
- For a broken state, triage the state triplet: state, code, reality — fix all three.
- For a gridlocked state, remove the offending resource by another route (or remove it from code and re-import later).
- For a bloated state, split it; blast radius is the entire tree.
- For a never-clean state, replace non-deterministic data values with deterministic constructions that match the provider's expected format.

**Don't:**
- Unlock a state by deleting the lock file without reconciling the triplet.

*Ref: Terraform_at_Scale_Early_Release.md — "Common State Problems"*

---

### Common Approach — Versioned Environment Modules

**Principle:** Wrap entire environments in a versioned remote module; the root module just pins the version.

**Do:**
- Use semantic versioning and changelogs for the remote module.
- Document expected adoption cadence.

**Don't:**
- Use this to mask actually-different environment configurations — drive differences via variables.

*Ref: Terraform_at_Scale_Early_Release.md — "Approach 4: Versioned Environment Modules"*

---

### Wildcard Jobs for One-Off TF Operations

**Principle:** Build a single, governed job that allows flexible flags + free text for emergencies; identify the human operator in cloud audit logs.

**Do:**
- Always freshly clone the source repository before running the operation.
- Use RBAC/ABAC; require temporary elevated permissions; record who triggered and what they ran.
- Use impersonation (when available) so the human operator's identity is logged.

**Don't:**
- Allow raw shell access to a workstation with TF credentials.

*Ref: Terraform_at_Scale_Early_Release.md — "Approach 5: Wildcard Jobs"*

---

### Scenario: Organizational Scaling

**Principle:** Splitting a single large repo into team-specific repos follows an import/removal dance; complete all three triplet operations in one window.

**Do:**
- 1. Create the new repository
- 2. Copy the relevant code
- 3. `tf plan` in the new repo to discover import addresses
- 4. `tf import` each resource one by one
- 5. `tf plan` to confirm zero changes
- 6. `tf plan` in the repurposed repo to find removals
- 7. `tf state rm` for each, or in bulk with `tf state rm $(terraform state list)`
- 8. `tf plan` to confirm

**Don't:**
- Spread the procedure across multiple days.

*Ref: Terraform_at_Scale_Early_Release.md — "Scenario 1: Organizational Scaling"*

---

### Scenario: Reducing Duplication

**Principle:** Convert flat `resource "..." "..."` blocks into a single block with `for_each`, expose variable inputs as a list, and create one `.tfvars` per workload.

**Code:**
```hcl
# After: bundle of subnets via for_each
variable "snet_configs" {
  description = "A list of subnet information."
  type = list(object({
    name   = string
    cidr   = string
    region = string
  }))
}

resource "google_compute_subnetwork" "tas-7-16-snet-01" {
  for_each = { for snet in var.snet_configs : snet.name => snet }
  name          = each.value.name
  ip_cidr_range = each.value.cidr
  region        = each.value.region
  network       = google_compute_network.tas-7-16-vpc.id
}
```
*Ref: Terraform_at_Scale_Early_Release.md — Figure 2-13*

---

### Scenario: Merger / Acquisition

**Principle:** Two options — consolidate into one account (recreating) or use a second provider block in the dominant project.

**Do:**
- Choose option 2 (second provider block) whenever preservation matters more than convergence.
- Track address mappings across both accounts.

**Don't:**
- Recreate resources when the existing configurations are valid; prefer import + provider alias.

*Ref: Terraform_at_Scale_Early_Release.md — "Scenario 3: Merger/Acquisition"*

---

### Scenario: Organizational Change (Many-to-Many)

**Principle:** A reorg requires a many-to-many state redistribution; perform as a "big bang" by a small team with temporary permissions.

**Do:**
- Create the new repositories, copy and refactor code, optionally construct new modules.
- Discover, import, confirm imports; discover, remove, confirm removals — across all repos.
- Track all "from" / "to" address mappings in a shared spreadsheet.

**Don't:**
- Rely on a single engineer with permanent high-privilege access; the audit trail must be clearly attributable.

*Ref: Terraform_at_Scale_Early_Release.md — "Scenario 4: Organizational Change Management"*

---

## Anti-Patterns & Common Mistakes

- **Inline `for`/`in` expressions:** unreadable, hard to debug → *fix:* decompose into named `locals{}` blocks.
- **Implicit type conversion:** silently wrong → *fix:* use `tonumber()` / `tobool()` / `tostring()` and add `variable { validation }` blocks.
- **`-target` in normal pipelines:** hides systemic issues → *fix:* refactor the offending state to isolate the problematic resource.
- **Tightly-coupled states with mutual dependencies:** cyclic change risk → *fix:* introduce explicit up/down stream and ensure upstream moves slower.
- **ClickOps on production resources:** compounds with IaC to produce extra work → *fix:* reserve for prototyping; immediately absorb into code once a "pilot" emerges.
- **`tf state rm` followed by leaving the running resource untouched:** next apply recreates it and may fail with a duplicate → *fix:* complete the triplet operation in one window.
- **Codifying `timestamp()` into certificate/policy lifecycles:** breaks idempotency → *fix:* handle time-bound secrets outside TF.
- **`matchkeys()` for filtering:** obscure → *fix:* replace with a `for`/`if` expression.
- **String directives for short, dissimilar outputs:** obfuscation → *fix:* ternary + interpolation.
- **One-off TF operations in normal automation:** violates idempotence → *fix:* build a gated wildcard job.
- **Lopsided states from mixing module and resource blocks, mixing module types, or mixing `for_each` with non-collection nodes:** automatic imbalance → *fix:* split into homogeneous modules, prefer wrapping over `for_each` outside the root.

## Decision Heuristics / Checklists

- *Logic lives in HCL?* Yes, if it can be one ternary and one interpolation. No, otherwise — push to Python/JavaScript.
- *Single state, multiple workloads?* Use Approach 1 (backend key variation) with per-workload `.tfvars` files.
- *New repo per environment?* Use Approach 4 (versioned remote modules) and pass environment variables.
- *Need to combine/separate states mid-stream?* Use the documented procedure (create repo → import → state rm) and complete triplet operations in one window.
- *Multiple teams touching one repo?* Refactor into one-team-per-state before they fight over a locked state in a P1.
- *Secret value, ever?* Use variable `sensitive = true`, never `file()`.
- *Cross-state data reference?* Use a `data` block / `terraform_remote_state`, never a duplicated `resource`.
- *Storing idempotence-breaking fields?* Pair `timestamp()` with `ignore_changes` or move outside TF.
- *Need "-target"?* Pause — refactor or use a wildcard job.

## Key Takeaways

1. **HCL is a configuration language, not a programming language.** Externalize complex logic to Python/JavaScript; use `locals{}` to name every meaningful intermediate value.
2. **The state triplet is the unit of truth.** Code, state, and running instances must be reconciled together — never split across days.
3. **Build for state balance at the start.** Avoid mixing module/resource blocks, mixing module types, or mixing `for_each` with non-`for_each` siblings.
4. **One-off operations belong in a governed "wildcard job."** They do not belong in pipelines.
5. **Keep states self-contained, leaf-rich, and shallow.** Blast radius equals the entire state tree.
6. **Drive environment differences through versioned remote modules + variables,** not parallel codebases.
7. **ClickOps is the antithesis of IaC.** Reserve it for rapid prototyping only.
8. **Use `tf import` to add to state, never to add to cloud**; the cloud resource must already exist.
9. **Refactor working code via clean-up sprints, "improve what you touch" policies, or refactor bounties.**
10. **Plan for organizational change.** Use Approach 1 + per-workload `.tfvars` so a future split is mechanical, not destructive.

## Cross-References

- Related: [[../Ultimate_AWS_CDK.md]] — CDK has no state file of its own; CloudFormation owns it. Different state-management discipline.
- Related: [[../ansible_for_devops.md]] — Ansible has no state; idempotency comes from module convergence instead of a state object.
- Topic index: [[../INDEX.md]]
