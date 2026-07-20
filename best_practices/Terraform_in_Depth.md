# Terraform in Depth — Infrastructure as Code with Terraform and OpenTofu
**Author:** Robert Hafner (Manning Publications, 2025; forewords by Christian Mesh & Anton Babenko)
**Topic tags:** `#architecture` `#devops` `#cloud`
**Language focus:** HCL, Go (Terratest / provider development), Python (CDKTF / external programs), Bash
**Sources:** `markdown_output/Terraform_in_Depth_Infrastructure_as_Code_-_Robert_Hafner/Terraform_in_Depth_Infrastructure_as_Code_-_Robert_Hafner.md` · `summaries/Terraform_in_Depth_Infrastructure_as_Code_-_Robert_Hafner.md`

## TL;DR
Terraform is a declarative, stateful, DAG-driven infrastructure-as-code engine whose language (HCL) maps nouns (blocks) to a graph of providers, modules, and backends. Production-grade Terraform means disciplined module composition (prefer `for_each` over `count`), protected state (remote backend + locking + lineage/serial), disciplined CI (format → validate → lint → security → plan), real tests (Terratest for integration, the native `.tftest.hcl` framework + mocks for unit-style), GitOps delivery through TACOS or Terragrunt, OIDC instead of stored credentials, and a healthy respect for state drift, cascading changes, and circular dependencies. OpenTofu is the fully open-source community fork after HashiCorp's BSL relicense in 2023; it is a near drop-in replacement that has become the de-facto choice for new projects that need cross-vendor CD platforms (Spacelift, Env0, Scalr, Terrakube) instead of HCP Terraform.

---

## Best Practices by Topic

### 1. Distinguish Declarative from Imperative Languages

**Principle:** Terraform is declarative — describe the desired end state, not the steps; the engine builds a DAG and figures out the order.

**Do:**
- Use nouns (resource, data, variable, output, locals) and let Terraform sequence work.
- Trust Terraform's dependency resolution; reference attributes across blocks to declare edges implicitly.
- Pair declarative specs with explicit `depends_on` only when there is a *real* hidden edge (e.g., Internet Gateway → NAT Gateway).

**Don't:**
- Don't write procedural wrappers that try to "do" things — that's imperative. Use providers, data sources, and provisioners as the escape hatches.
- Don't try to enforce cyclic dependencies — they are illegal by definition (the "acyclic" in DAG) and Terraform will error with `Error: Cycle:`.

*Ref: Terraform_in_Depth.md — "1.3 Declarative languages"*

---

### 2. Internalize the Init → Plan → Apply → Destroy Lifecycle

**Principle:** `init` downloads providers/modules + initializes backend; `plan` does refresh → compare → propose; `apply` executes the DAG; `destroy` tears down. Save plans to a file before applying for any production change.

**Do:**
- Always run `terraform plan -out=plan.tfplan` for production changes, then `terraform apply plan.tfplan` (skips the second prompt).
- Use `terraform plan -refresh-only` (not the deprecated `terraform refresh`) to update state from real-world drift without changing infra.
- Use `-input=false` in CI so missing variables fail loudly instead of prompting.

**Don't:**
- Don't use the deprecated `terraform refresh` command — it mutates state without showing a plan and can wipe resources when auth fails.
- Don't rely on plain `terraform apply` in CI for production — always use a saved plan file so the apply exactly matches what was reviewed.

*Ref: Terraform_in_Depth.md — "5.4 The Terraform plan", "5.5 Apply"*

---

### 3. Author Resources Using the Block Grammar (type, labels, args, subblocks)

**Principle:** HCL is built around blocks; understand the 12 block types (terraform, provider, resource, data, variable, output, locals, module, import, moved, removed, check) and their label rules.

**Do:**
- Keep two labels on `resource`/`data` (`subtype` + `local name`); keep one label on `variable`/`output`/`module`/`provider`; keep zero labels on `terraform` and `locals`.
- Use arguments (key = value) for things that appear once; use subblocks for things you may repeat (filters, ingress rules, lifecycle rules).
- Separate label by whitespace inside `{}`, separate args with newlines or whitespace, and align `=` signs within a block for readability (`terraform fmt` enforces this).

```hcl
data "aws_ami" "ubuntu" {
  owners      = ["099720109477"]
  most_recent = true
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

**Don't:**
- Don't make subblocks carry duplicate semantics of arguments — subblocks repeat, arguments appear once.
- Don't reorder arguments to mean anything; Terraform ignores order and uses the DAG.

*Ref: Terraform_in_Depth.md — "2.2 Block syntax"*

---

### 4. Style Resources with the Terraform Conventions (`terraform fmt`)

**Principle:** `terraform fmt` enforces a stable style: meta-args first, then resource-specific args (with aligned `=` signs), then resource-specific subblocks, then meta subblocks (e.g., `lifecycle`) at the end.

```hcl
resource "resource_type" "unique_resource_name" {
  provider           = aws.dns
  string_parameter   = "value"
  integer_parameter  = 134
  boolean_parameter  = true
  object_arguments = {
    key1 = "value"
    key2 = "value"
    key3 = "value"
  }
  subblock {
    subargument  = "value"
    subargument2 = "another_value"
  }
  lifecycle {
    ignore_changes = [object_arguments]
  }
}
```

**Do:**
- Run `terraform fmt -recursive .` as a local chore and `terraform fmt -check -recursive .` in CI.

**Don't:**
- Don't try to enforce argument order yourself beyond what `fmt` does — the tool is the source of truth.

*Ref: Terraform_in_Depth.md — "2.2.6 Style"*

---

### 5. Pin Providers in `required_providers` — Always

**Principle:** Even though HashiCorp namespace providers auto-resolve, you must declare every provider explicitly so version constraints are enforced.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

**Don't:**
- Don't rely on implicit `hashicorp/<localname>` lookup — it makes upgrades silently breaking and removes your ability to test against a version range.

*Ref: Terraform_in_Depth.md — "2.4.2 Required providers"*

---

### 6. Use Provider Aliases to Manage Multi-Region / Multi-Account Resources

**Principle:** Declare one provider block per configuration; use the `alias` meta-argument on data/resource blocks to select a non-default provider.

```hcl
provider "aws" {
  region = "us-east-1"
}
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

data "aws_vpc" "backup" {
  provider = aws.west
  default  = true
}

data "aws_subnets" "backup" {
  provider = aws.west
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.backup.id]
  }
}
```

**Don't:**
- Don't put provider blocks in non-root modules — only the root module configures providers.

*Ref: Terraform_in_Depth.md — "2.4.4 Provider aliases"*

---

### 7. Master the Lifecycle Meta-Arguments (create_before_destroy, prevent_destroy, ignore_changes, replace_triggered_by)

**Principle:** `lifecycle` is the escape hatch for "Terraform is being too clever". Each sub-argument is a different problem.

```hcl
resource "aws_instance" "hello_world" {
  ami           = data.aws_ami.ubuntu.id
  subnet_id     = data.aws_subnets.default.ids[0]
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true   # zero-downtime replacements
    ignore_changes        = [ami]  # don't replace when upstream AMI rotates
  }
}
```

- `create_before_destroy = true` — for HA replacements; the new resource is created before the old one is destroyed. Required when names are unique (IAM role names, EIPs).
- `prevent_destroy = true` — makes destroy plans fail. Use **rarely**; can't be conditional per-environment; deleting the block also removes the protection.
- `ignore_changes = [...]` — Terraform stops updating the listed attributes; use for AMI rotations, autoscaler count drift, tags added by external orchestrators (EKS/ECS).
- `ignore_changes = all` — read-only-after-creation resource (Terraform still refreshes attributes but never writes).
- `replace_triggered_by = [...]` — force replacement when another resource or attribute changes; replace local-only triggers by routing through `terraform_data.triggers_replace`.

```hcl
resource "null_resource" "replace_instance" {
  triggers = { instance_type = var.instance_type }
}
resource "aws_instance" "hello_world" {
  instance_type = var.instance_type
  lifecycle {
    replace_triggered_by = [null_resource.replace_instance]
  }
}
```

**Don't:**
- Don't use `prevent_destroy` to "protect" a resource you actually intend to leave alone — `ignore_changes` is almost always the right tool.

*Ref: Terraform_in_Depth.md — "2.7.2 Lifecycle"*

---

### 8. Use `depends_on` Only When the Edge Is Real and Hidden

**Principle:** Terraform auto-infers edges from attribute references. Use `depends_on` only when two resources depend on each other without an attribute edge (e.g., NAT Gateway needs an Internet Gateway that returns no attribute).

```hcl
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}
resource "aws_nat_gateway" "example" {
  subnet_id = aws_subnet.example.id
  depends_on = [aws_internet_gateway.main]
}
```

**Don't:**
- Don't sprinkle `depends_on` everywhere "just to be safe" — it overrides the DAG and can mask real refactors.
- Don't use string reference forms (`depends_on = [aws_internet_gateway.main.id]`) — the block reference itself is the argument.

*Ref: Terraform_in_Depth.md — "2.7.3 Explicit dependencies"*

---

### 9. Compose with Modules: Files, Variants, and Sources

**Principle:** Modules are the unit of reuse. Every Terraform project has a *root module* (where `terraform init` runs); submodules live in `modules/`; shared modules come from a registry, Git, or filesystem.

| File            | Purpose                                                                |
|-----------------|------------------------------------------------------------------------|
| `variables.tf`  | All input variable declarations                                         |
| `outputs.tf`    | All output value declarations                                          |
| `main.tf`       | Primary entry; can be the only file for simple modules                 |
| `*.tf`          | Any other HCL file                                                     |
| `README.md`     | Used by registries                                                     |
| `modules/`      | Submodules for compound modules                                         |
| `templates/`    | `templatefile()` source files                                          |
| `examples/`     | Working examples — and your Terratest test entry points                |

```hcl
module "vpn" {
  source     = "tedivm/cloudinit/general"
  version    = "~> 1.0"
  services   = ["consul", "nomad"]
}
```

**Don't:**
- Don't keep provider blocks in a non-root module — they belong only at the root.
- Don't forget to name the GitHub repository `terraform-<provider>-<name>` for the community registry to discover it.

*Ref: Terraform_in_Depth.md — "3.1 Modules", "3.8.5 Publishing"*

---

### 10. Always Type and Validate Input Variables

**Principle:** Variables can be `string | number | bool | list(...) | set(...) | map(...) | tuple(...) | object(...) | any | null`. Type constraints catch entire classes of bugs at plan time.

```hcl
variable "subnet_id" {
  type        = string
  description = "The ID of the Subnet to launch the instance into."
  validation {
    condition     = length(regexall("^subnet-[\\d|\\w]+$", var.subnet_id)) == 1
    error_message = "The subnet_id must match the pattern ^subnet-[\\d|\\w]+$"
  }
}
```

`validation` blocks can be repeated. As of Terraform 1.9.0 the `condition` may reference *other* variables and resources (previously the block could only see itself).

**Don't:**
- Don't use `type = list` without a subtype — Terraform quietly accepts that as `list(any)` and you lose all type safety.
- Don't use `null` as a type constraint — `null` is a value, not a type.

*Ref: Terraform_in_Depth.md — "3.6 Value types", "3.7 Validating inputs"*

---

### 11. Use Objects for Structure and Optionals for Backward-Compatible Defaults

**Principle:** Objects give you fixed-shape typed records with named fields; tuples give fixed-length heterogeneous lists. Use `optional()` for fields that may be absent.

```hcl
variable "nested_object" {
  type = object({
    key = object({
      subkey = object({
        nested_string = string
        nested_tuple  = tuple([string, string, string])
      })
    })
  })
  default = {
    key = {
      subkey = {
        nested_string = "hello world"
        nested_tuple  = ["one", "two", "three"]
      }
    }
  }
}
```

*Ref: Terraform_in_Depth.md — "3.6.7 Objects", "3.6.6 Tuples"*

---

### 12. Mark Sensitive Values; Treat Sensitivity as Contagious

**Principle:** `sensitive = true` on a `variable` or `output` masks the value in CLI/logs; the *flag* is propagated through derived values, so a string built from a sensitive variable is also sensitive.

```hcl
variable "logging_api_key" {
  description = "The API Key for our logging service."
  type        = string
  sensitive   = true
}
```

**Do:**
- Always mark generated credentials sensitive (`random_password.result` is marked sensitive for you).
- Mark outputs sensitive when they propagate sensitive data; Terraform will throw an error if you forget.

**Don't:**
- Don't rely on `sensitive = true` for *storage* security — the value still lives in state. Use state encryption + access control + secret managers instead.
- Don't try to "un-sensitive" with `nonsensitive(...)` unless you have a documented reason; the lint of any reviewer will flag it.

*Ref: Terraform_in_Depth.md — "3.3.2 Marking variables as sensitive", "4.6.3 Sensitive and nonsensitive"*

---

### 13. Prefer `for_each` Over `count` for Map/Set-Driven Resources

**Principle:** `count` multiplies by integer (brittle when the map reorders); `for_each` over a map/set gives you stable addresses keyed by the source key — adding or removing one item does not reshuffle all the others.

```hcl
resource "aws_instance" "server" {
  for_each      = var.instances      # map(string) of name → config
  ami           = data.aws_ami.ubuntu.id
  subnet_id     = each.value.subnet_id
  instance_type = each.value.instance_type
  tags = { Name = each.key }
}
```

**Don't:**
- Don't try to pass a `list` to `for_each` — error. Convert with `toset(...)` if you have a list (knowing that duplicates collapse and order is lost).
- Don't compute `for_each` keys from a resource attribute that is only known after apply — Terraform will refuse.

*Ref: Terraform_in_Depth.md — "4.8 count and for_each", "4.8.4 Limitations and workarounds"*

---

### 14. Use `count` as a Boolean Toggle for Optional Resources

**Principle:** `count = var.enable_x ? 1 : 0` is the idiomatic on/off switch for an optional feature inside a module.

```hcl
variable "enable_systems_manager" {
  type    = bool
  default = false
}
resource "aws_iam_role_policy_attachment" "ssm_attach" {
  count = var.enable_systems_manager ? 1 : 0
  role       = aws_iam_role.main.name
  policy_arn = data.aws_iam_policy.ssm_arn.arn
}
```

*Ref: Terraform_in_Depth.md — "4.8.1 count", "Listing 4.7"*

---

### 15. Use the Ternary Carefully — It Evaluates Both Sides

**Principle:** Terraform's ternary `cond ? a : b` is unique in that **both** `a` and `b` are evaluated, even if only one is returned. This breaks if either side references something that doesn't exist (e.g., a resource that is toggled off with `count`).

```hcl
output "nat_ip_address" {
  value = var.use_nat_instance ? module.nat_instance.ip : module.nat_gateway.ip
}
```

**Don't:**
- Don't use `cond ? resource_a[0].x : resource_b[0].x` if either branch's resource can be empty — wrap in `try(..., null)` or filter with `[0]`.

*Ref: Terraform_in_Depth.md — "4.2.4 Conditional"*

---

### 16. Splat with `[*]` for List Projection; `[for ... in ...]` for Transformation

**Principle:** `aws_instance.server[*].arn` is shorthand for `[for s in aws_instance.server : s.arn]`. Use the explicit `for` when filtering or transforming.

```hcl
locals {
  config_id_splat = var.object_config[*].id
  config_id_for   = [for x in var.object_config : x.id]
}
```

For grouping-by-key:
```hcl
servers_by_subnet = {
  for server in aws_instances.main[*]
  : server.subnet_id => server.id...
}
```

*Ref: Terraform_in_Depth.md — "4.9 For", "4.9.5 Splat"*

---

### 17. Use Dynamic Blocks for Variable Subblock Counts

**Principle:** `dynamic` lets a list input drive a repeated subblock. Inside `content`, references use the block label (here `ingress`).

```hcl
variable "security_group_rules" {
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
}
resource "aws_security_group" "main" {
  name = "${var.name}-sg"
  vpc_id = var.vpc_id
  dynamic "ingress" {
    for_each = var.security_group_rules
    content {
      description = ingress.value.description
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

To toggle a single dynamic block: `for_each = var.enable_https ? ["placeholder"] : []`.

*Ref: Terraform_in_Depth.md — "4.10 Dynamic blocks"*

---

### 18. Use the Right Function for the Job — and Avoid Impure Functions in Config

**Principle:** Terraform divides functions into Numeric, String, Collection, Encoding, Filesystem, Date, Hash/Crypto, IP network, and Type conversion. Since Terraform 1.8, providers can ship their own functions.

**Do:**
- Use `cidrsubnet("192.168.0.0/16", 2, 0)` for CIDR math.
- Use `jsonencode(obj)` / `yamlencode(obj)` instead of templating JSON/YAML.
- Use `templatefile(path, vars)` for any large config file with logic.

**Don't:**
- Don't use `uuid()`, `timestamp()`, or other impure functions in resource arguments — every plan will report drift. Use the `random` and `time` providers instead, which persist values in state.

```hcl
# BAD — uuid() generates a new value every plan
resource "aws_instance" "example" {
  tags = { id = uuid() }
}
```

*Ref: Terraform_in_Depth.md — "4.3 Functions", "4.3.3 Pure vs. impure functions"*

---

### 19. Use `try()` and `can()` to Defensively Read Optional Resources

**Principle:** `try(expr, default)` returns the default if `expr` errors; `can(expr)` returns true/false based on whether the expression errors. Use `try` for safe access to dynamic resources; use `can` only inside `validation` blocks.

```hcl
output "instance_id" {
  value = try(aws_instance.main[0].id, null)
}
```

```hcl
variable "number_string" {
  type = string
  validation {
    condition     = can(tonumber(var.number_string))
    error_message = "Although this variable is a string, it is expected to be numeric."
  }
}
```

**Don't:**
- Don't use `try` to mask real errors — fix the upstream cause.

*Ref: Terraform_in_Depth.md — "4.7 Try and can"*

---

### 20. Write Templates for Big Strings; Use Built-in Encoders for JSON/YAML

**Principle:** Templates (`.tftpl`) support `${...}` interpolation and `%{ if/for }` directives. Don't hand-roll JSON or YAML — use `jsonencode`/`yamlencode`.

```hcl
locals {
  json_string = <<EOT
    "{ \"name\": \"${var.name}\" }"
  EOT
  config_object = { name = var.name }
  yaml_config = yamlencode(local.config_object)
  json_config = jsonencode(local.config_object)
}
```

The deprecated `data "template_file"` resource should be replaced with `templatefile()` everywhere.

*Ref: Terraform_in_Depth.md — "4.4 Strings and templates"*

---

### 21. Use Regular Expressions Carefully (Go Syntax, Named/Anonymous)

**Principle:** Terraform uses Go's `regexp` package. Use `regex(...)` when failure should error; `regexall(...)` returns a list (empty on no match). Named capture groups give you a map; unnamed give you a list of substrings.

```hcl
variable "aws_region" {
  type = string
  validation {
    condition     = length(regexall("^[a-z]{2}-[a-z]*-\\d$", var.aws_region)) == 1
    error_message = "This value must match the aws region format."
  }
}
```

Use the `replace()` function (with `/(regex)/` delimiters) for substitution, capturing groups are available as `$1`, `$2`, … or named `$name`.

*Ref: Terraform_in_Depth.md — "4.5 Regular expressions"*

---

### 22. Order of Operators Matters; Use Parentheses for Clarity

```
1 !, - (when used to multiply by -1)
2 *, /, %
3 +, - (when used as subtraction)
4 >, >=, <, <=
5 ==, !=
6 &&
7 ||
```

For multi-operator expressions, parenthesize even when not required for correctness — Terraform and humans both read it easier.

*Ref: Terraform_in_Depth.md — "4.2.5 Order"*

---

### 23. Treat Plans as a DAG and Use `terraform graph` to Debug It

**Principle:** Terraform's resource graph has three node types: Resources (including data sources), Provider Configuration Nodes, and Resource Meta Nodes (the umbrella for `count > 1` resources). Modules are **not** first-class nodes — their contents are flattened.

**Do:**
- Run `terraform graph | dot -Tpng > graph.png` and view it with Graphviz.
- Use `terraform graph -type=plan-destroy` and `terraform graph -type=apply -plan=plan.tfplan` to visualize apply plans.

**Don't:**
- Don't trust module boundaries for ordering. A resource in module B can be created before module A if no edge exists between them — modules are a code-organization convenience, not a runtime boundary.

*Ref: Terraform_in_Depth.md — "5.2 The Terraform resource graph"*

---

### 24. Plan in Three Modes — Default, Destroy, Refresh-Only

```bash
terraform plan -out=plan.tfplan             # default: change vs. real world
terraform plan -destroy -out=destroy.tfplan # tear down everything
terraform plan -refresh-only               # update state from real world
```

**Use `-replace 'addr'` instead of the deprecated `terraform taint`** — `-replace` lets you preview the impact before applying.

**Avoid `-refresh=false`** unless you fully understand the consequences (Terraform will not see real-world drift and may attempt to re-create existing resources).

**Don't use `-target` routinely** — it should be reserved for emergency debugging. Modules that require `-target` to work are an antipattern.

*Ref: Terraform_in_Depth.md — "5.3 Plan", "5.3.2 Replace", "5.3.4 Disabling refresh"*

---

### 25. Solve the Three Classic Pitfalls: Circular Dependencies, Cascading Changes, Hidden Dependencies

**Circular dependencies:**
- The error: `Error: Cycle: null_resource.alpha, null_resource.bravo, null_resource.charlie`.
- Fix: introduce an upstream variable that all three depend on, instead of depending on each other in a loop.

```hcl
variable "build_id" {
  default = null
  type    = string
}
resource "null_resource" "alpha" {
  triggers = { rebuild = var.build_id }
}
# alpha/bravo/charlie all share the same var.build_id instead of chaining
```

**Cascading changes:**
- A change to one resource forces replacement of downstream resources (e.g., changing the CA key algorithm in a TLS module cascades to every signed certificate).
- Inspect every plan for `# forces replacement` notes; route the offending attribute through `ignore_changes` or `replace_triggered_by`.

**Hidden dependencies:**
- Resources that depend on each other without an attribute edge (e.g., NAT Gateway needs Internet Gateway to exist).
- Use `depends_on` to make the edge explicit.

**Always-detected changes ("eternal drift"):**
- Provider/normalizer bugs that cause every plan to show diffs.
- Match your input format to the API's response (lowercase, sorted, integer-vs-float).

**Calculated values + iterations:**
- `count`/`for_each` keys must be known at plan time; do not derive them from a resource attribute.

**Failed state updates:**
- If only updates/destroys: re-run with `apply -refresh-only`.
- If creates: `terraform import` the orphans or delete them and retry.

*Ref: Terraform_in_Depth.md — "5.7 Common pitfalls and errors"*

---

### 26. Treat State as Critical Infrastructure (Resilient, Secure, Available)

**Resiliency:**
- A 99.999999999% durability backend (S3) is your floor; nothing is bulletproof.
- Take *external* backups of state and **test restore** on a schedule.

**Security:**
- State contains every attribute (including sensitive ones). A leaked state = leaked architecture and creds.
- Use MFA, restrict access, lock down network paths, enable encryption, log access.

**Availability:**
- Aim for 99.99%+ (four nines = < 4m 30s/month of downtime).
- Never run Terraform without a remote backend in production.

*Ref: Terraform_in_Depth.md — "6.2 Important considerations"*

---

### 27. Read State JSON Safely — Understand `version`, `serial`, `lineage`

State is JSON; on the top level it contains:
- `version` — the state format version (currently `4`).
- `terraform_version` — engine version that wrote it.
- `serial` — incremented on every change (used by `state push -force`).
- `lineage` — UUID assigned at first `init`; backends compare it to refuse cross-project writes.
- `resources` — every managed resource + data source, with full attributes.
- `outputs` — root-level module outputs only (sub-module outputs are not stored).
- `check_results` — outcomes of `check` blocks.

```json
{
  "version": 4,
  "terraform_version": "1.5.4",
  "serial": 6,
  "lineage": "7490ef49-8634-ac56-596b-6f2f4259bece",
  "outputs": { "password": { "value": "[-Cz>m@XQnZc", "type": "string", "sensitive": true } },
  "resources": [
    {
      "module": "module.my_password",
      "mode": "managed",
      "type": "random_password",
      "name": "new_password",
      "provider": "provider[\"registry.terraform.io/hashicorp/random\"]",
      "instances": [{ "schema_version": 3, "attributes": { "result": "[-Cz>m@XQnZc", ... } }]
    }
  ],
  "check_results": null
}
```

*Ref: Terraform_in_Depth.md — "6.3 Dissecting state"*

---

### 28. Pick a Backend and Configure It Correctly

**Production-ready backends:** `s3` (with DynamoDB lock), `azurerm`, `gcs`, `cos`, `oss`, `pg`, `consul`, `kubernetes` (post-1.6), `remote`/`cloud` (TACOS). `local` is dev-only.

**Backend block (root module only):**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Partial configurations:**
- Leave the block empty, then supply values with `-backend-config=backend.hcl` or `-backend-config="key=value"` on `terraform init`.

```hcl
# backend.hcl
address      = "localhost:8500"
path         = "path/to/save/state"
access_token = "01a56e2d-a96a-4ca5-9d39-d5152015f533"
```

**Migrating backends:** `terraform init` will detect the change and tell you to add `-migrate-state` or `-reconfigure`.

*Ref: Terraform_in_Depth.md — "6.4 Storing state", "6.4.3 Backend block"*

---

### 29. Use the `cloud` Block for TACOS; Otherwise Use a Remote Backend

```hcl
terraform {
  cloud {
    organization = "acme-org"
    hostname     = "app.terraform.io"
    workspaces {
      tags = ["acme_application", "development"]
    }
  }
}
```

After configuring, run `terraform login <hostname>` once to mint a token.

> Note: when you use the `cloud` block, `terraform workspace select` switches *cloud* workspaces, not the classic CLI workspaces. This is a constant source of confusion.

*Ref: Terraform_in_Depth.md — "6.4.5 Cloud block"*

---

### 30. Manipulate State with Code, Not JSON Editing

**Code-driven (preferred):**
```hcl
resource "random_password" "main" { length = 12 }

moved {
  from = random_password.my_password
  to   = random_password.main
}

removed {
  from = aws_s3_bucket.bucket
  lifecycle { destroy = false }
}
```

**CLI-driven:**
- `terraform state list`
- `terraform state mv <from> <to>`
- `terraform state rm <addr>` (removes from state without destroying infra)
- `terraform state replace-provider hashicorp/random registry.example.com/hashicorp/random`

**Manual editing (last resort):**
1. `terraform state pull > backup.tfstate`
2. Edit carefully (validate JSON, keep `serial` strictly increasing).
3. `terraform state push -force backup.tfstate`.

**Don't:**
- Don't use `terraform state rm` without removing the matching block from your code — Terraform will try to re-create the resource on the next apply.

*Ref: Terraform_in_Depth.md — "6.5 Manipulating state"*

---

### 31. Classify State Drift and Plan Responses

| Drift category           | Cause                                                    | Response                                                                                                |
|--------------------------|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| Accidental manual change | Wrong account / fat-finger                                | Run `terraform plan` to fix; tighten production access + branch protection                            |
| Intentional manual change| Emergency hotfix                                          | Add the change to code immediately; running Terraform reverts otherwise                                 |
| Conflicting automation   | AMI release, orchestrator tag injection, autoscaler drift| Apply it (`ignore_changes` if you want to keep current values)                                          |
| Terraform error          | Crash, lost state write, auth lapse                      | Refresh-only apply; if creates were lost, `import` orphans or delete them and re-apply                |

Always identify *why* before responding — drift is a symptom of another problem.

*Ref: Terraform_in_Depth.md — "6.6 State drift"*

---

### 32. Cross-Project State via `terraform_remote_state` (and Prefer Data Sources)

```hcl
data "terraform_remote_state" "rds" {
  backend = "s3"
  config = {
    bucket = var.state_bucket_name
    key    = var.rds_state_path
    region = var.state_region
  }
  defaults = {
    rds_uri = null   # soft dependency: this project can run before RDS exists
  }
}
```

**Keep `terraform_remote_state` calls in the root module**, not in reusable modules — you don't want your VPC module to be coupled to a specific backend.

**Prefer data sources over `terraform_remote_state` whenever possible** — they don't expose sensitive state and don't require backend credentials.

*Ref: Terraform_in_Depth.md — "6.7 Accessing state across projects"*

---

### 33. Use Workspaces with `terraform.workspace` for Environment Mapping

```hcl
locals {
  networks = {
    "production" = { vpc = "vpc-e32ffed2c1e50a63", subnets = [...] }
    "staging"    = { vpc = "vpc-82504ae9e1ecc804", subnets = [...] }
    "default"    = { vpc = "vpc-a19de3767f7478f4", subnets = [...] }
  }
  current_network = local.networks[terraform.workspace]
}
```

Remember: classic CLI workspaces share the same code; *cloud-block* workspaces are completely independent environments.

*Ref: Terraform_in_Depth.md — "6.4.7 Workspaces"*

---

### 34. State-Only Resources: Random, Time, Null, terraform_data

**Random provider** — persist random values in state so plans don't drift:
```hcl
resource "random_password" "password" {
  length  = 16
  lower   = true
  numeric = true
  special = true
  upper   = true
}
```
`random_password.result` is marked sensitive; it is the only resource guaranteed to use a cryptographic RNG.

**Time provider** — replace `timestamp()` with persistent times. `time_rotating("every_two_days")` lets you trigger replacements on a schedule.

```hcl
resource "time_sleep" "delay" {
  create_duration = "2m"
  depends_on      = [aws_instance.main]
}
```

**Null provider** / **`terraform_data`** — no-op resources used to attach provisioners, triggers, or `replace_triggered_by` to expressions (locals are forbidden there):

```hcl
resource "terraform_data" "local_replacement" {
  triggers_replace = { is_even = local.is_even }
}
resource "aws_instance" "myinstance" {
  lifecycle {
    replace_triggered_by = [terraform_data.local_replacement]
  }
}
```

Use `terraform_data` for new code; `null_resource` is the legacy form (still installed millions of times per week in early 2025).

*Ref: Terraform_in_Depth.md — "6.8 State-only resources"*

---

### 35. CI Pipeline: Format → Validate → Lint → Security → Plan → Apply

**Makefile core (always project-local):**
```makefile
.PHONY: chores
chores: format document

.PHONY: format
format:
	$(TF_BINARY) fmt -recursive .

.PHONY: test_format
test_format:
	$(TF_BINARY) fmt -check -recursive .

.PHONY: documentation
documentation:
	terraform-docs -c .terraform-docs.yml .

.PHONY: test_documentation
test_documentation:
	terraform-docs -c .terraform-docs.yml --output-check .

.PHONY: test_validation
test_validation:
	$(TF_BINARY) init -backend=false
	$(TF_BINARY) validate

.PHONY: test_tflint
test_tflint:
	tflint --init
	tflint

.PHONY: security
security: test_checkov test_trivy
```

`TF_BINARY` defaults to `terraform`; override per-invocation with `make format TF_ENGINE=opentofu` (use `tenv` for version management).

**GitHub Actions matrix for both engines:**
```yaml
name: Validation
on: [push, pull_request]
jobs:
  validate:
    strategy:
      matrix:
        engine: ["opentofu", "terraform"]
        version: ["1.6", "1.7"]
      experimental: [false]
      include:
        - version: "1.9"
          engine: "opentofu"
          experimental: true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Terraform
        if: ${{ matrix.engine == 'terraform' }}
        uses: hashicorp/setup-terraform@v3
        with: { terraform_version: ${{ matrix.version }} }
      - name: Install OpenTofu
        if: ${{ matrix.engine == 'opentofu' }}
        uses: opentofu/setup-opentofu@v1
        with: { tofu_version: ${{ matrix.version }} }
      - run: make test_validation TF_ENGINE=${{ matrix.engine }}
```

*Ref: Terraform_in_Depth.md — "7.2 Local development", "7.7 Enforcing quality with CI systems"*

---

### 36. Use TFLint with Provider Plugins

```hcl
# .tflint.hcl
plugin "terraform" {
  enabled = true
  preset  = "all"     # "all" enables terraform_comment_syntax, require_description, etc.
}
rule "terraform_comment_syntax" { enabled = false }

plugin "aws" {
  enabled = true
  version = "0.30.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
```

**Inline disable:**
```hcl
resource "aws_instance" "this" {
  ami           = "ami-867166b8518f055af"
  # tflint-ignore: aws_instance_invalid_type
  instance_type = "p8.48xlarge"  # beta-only
}
```

*Ref: Terraform_in_Depth.md — "7.3.3 TFlint"*

---

### 37. Run Checkov AND Trivy — Both Are Free

**Checkov** — runs locally with `checkov --directory .`. Exceptions:
```hcl
resource "aws_instance" "this" {
  #checkov:skip=CKV_AWS_88:This instance is meant to be publicly accessible.
  associate_public_ip_address = true
}
```

**Trivy** — `trivy config .`. Inline disable:
```hcl
#trivy:ignore:AVD-AWS-0009
associate_public_ip_address = true
```

**Don't:**
- Don't blanket-ignore rules in `.trivyignore` without documenting why.

*Ref: Terraform_in_Depth.md — "7.4 Validating security"*

---

### 38. Custom Policy with Checkov YAML (Easier than OPA/Rego)

```yaml
# custom-checkov-policies/expensive-instance-types.yaml
metadata:
  id: CKV_CUSTOM_001
  name: "Disallow expensive instance families"
  category: "COST"
definition:
  cond_type: "attribute"
  resource_types: ["aws_instance"]
  attribute: "instance_type"
  operator: "not_regex"
  value: "^(p|g)[0-9]+.*"
```

Then in CI: `checkov --directory . --external-checks-git "https://github.com/your-org/policies.git"`.

OPA/Rego with the `tflint-ruleset-opa` plugin is more powerful but has a much steeper learning curve — start with Checkov YAML unless your team already uses OPA.

*Ref: Terraform_in_Depth.md — "7.5 Custom policy enforcement"*

---

### 39. Automate Chores: `terraform fmt`, `terraform-docs`, `tflint --fix`

```makefile
.PHONY: format test_format
format:
	$(TF_BINARY) fmt -recursive .
test_format:
	$(TF_BINARY) fmt -check -recursive .

.PHONY: documentation test_documentation
documentation:
	terraform-docs -c .terraform-docs.yml .
test_documentation:
	terraform-docs -c .terraform-docs.yml --output-check .
```

```yaml
# .terraform-docs.yml
formatter: "markdown table"
output:
  file: README.md
  mode: inject
  template: |-
    <!-- BEGIN_TF_DOCS -->
    <!-- END_TF_DOCS -->
settings:
  anchor: true
  color: true
  default: true
  description: true
  indent: 2
  readme: true
  sensitive: true
  type: true
```

`terraform-docs` rewrites only the section between `BEGIN_TF_DOCS` and `END_TF_DOCS`, so your hand-written README content is preserved.

*Ref: Terraform_in_Depth.md — "7.6 Automating chores"*

---

### 40. Use Pre-commit Hooks Locally (`.pre-commit-config.yaml`)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.88.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
      - id: terraform_tflint
      - id: terraform_checkov
```

`pre-commit install` registers hooks; `pre-commit run` invokes them on demand.

*Ref: Terraform_in_Depth.md — "7.2.6 Pre-commit hooks"*

---

### 41. Deliver Modules with Semantic Versioning

| Change                                | Field to increment | Result  |
|---------------------------------------|--------------------|---------|
| First stable release                  | (none)             | v1.0.0  |
| Fix bug in validation                 | Patch              | v1.0.1  |
| Add new optional variable             | Minor              | v1.1.0  |
| Rename an input                       | Major              | v2.0.0  |

**Use pessimistic constraints in callers** so Patch upgrades flow freely but Major upgrades are blocked:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"   # 5.x but not 6.0
}
```

```hcl
module "specific_example"                  { source = "...", version = "1.1.1" }
module "update_except_major"              { source = "...", version = ">= 1.1.0, < 2.0.0" }
module "update_except_major_excluding"    { source = "...", version = ">= 1.1.0, < 2.0.0, != 1.3.2" }
module "pessimistic_constraint_bugfix"    { source = "...", version = "~> 1.1.0" }  # = >=1.1.0, <1.2.0
module "pessimistic_constraint_minor"     { source = "...", version = "~> 1.1" }    # = >=1.1.0, <2.0.0
```

Don't pull modules straight from Git without a `ref` — you'll lose version constraints and force yourself to manually upgrade every commit.

*Ref: Terraform_in_Depth.md — "8.1.1 Semantic versioning and constraints"*

---

### 42. Publish to a Registry — Public or Private

- **Public**: `registry.terraform.io` (HashiCorp) or the OpenTofu registry. Submit once; both watch the GitHub repo for new semver tags.
- **Private**: HCP Terraform, Spacelift, Scalr, Artifactory, or Terrareg.

Artifactory push (`make publish_artifactory`):
```makefile
publish_artifactory:
	jf tf p --namespace=$(ARTIFACTORY_NAMESPACE) \
	         --provider=$(ARTIFACTORY_TF_PROVIDER) \
	         --tag=$(TAG)
```

```yaml
# .github/workflows/publish.yml
name: Publish to Artifactory
on:
  push:
    tags: ["v[0-9]+.[0-9]+.[0-9]+"]
jobs:
  artifactory:
    runs-on: ubuntu-latest
    permissions: { id-token: write }
    steps:
      - uses: actions/checkout@v4
      - uses: jfrog/setup-jfrog-cli@v4
        env: { JF_URL: https://registry.example.com }
        with: { oidc-provider-name: github-action-workflow }
      - run: make publish_artifactory TAG=${{ github.ref_name }}
```

*Ref: Terraform_in_Depth.md — "8.1.3 Public software registries", "8.1.5 Artifactory"*

---

### 43. Choose a Project Structure: Application-as-Root vs. Environment-as-Root vs. Terragrunt

- **Application as root module**: every env gets the same code with different `*.tfvars`. Easy to start; you cannot pin different module versions per env.
- **Environment as root module**: each env (staging, prod, future) is its own folder calling a shared application module at a pinned version. Each env can be promoted independently.
- **Terragrunt**: keeps the env-as-root structure but DRYs up backend, provider, and input boilerplate via a small `terragrunt.hcl` per env.

```hcl
# staging/terragrunt.hcl
terraform {
  source = "git::https://github.com/your-org/three_tier_example?ref=v1.0.2"
}
inputs = {
  num_tasks = 2
  db_size   = "db.t3.medium"
  network   = "vpc-staging"
}
```

`terragrunt run-all plan` plans across many envs at once.

*Ref: Terraform_in_Depth.md — "8.4 Project structures"*

---

### 44. Authenticate CI/CD with OIDC — No Stored Secrets

```hcl
data "tls_certificate" "gh_actions" {
  url = "https://token.actions.githubusercontent.com"
}
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  thumbprint_list = data.tls_certificate.gh_actions.certificates[*].sha1_fingerprint
  client_id_list  = ["sts.amazonaws.com"]
}
```

```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: actions/checkout@v4
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::9999999999:role/github-actions-${{ github.repository }}
      region: us-west-2
```

For Spacelift and similar TACOS, point the provider at `web_identity_token_file = "/mnt/workspace/spacelift.oidc"`.

**Do:** Always restrict the trust policy with conditions (specific repo, branch, workflow path).

*Ref: Terraform_in_Depth.md — "8.5.1 OpenID Connect"*

---

### 45. Use Secret Managers — Never Commit Secrets

```hcl
data "aws_secretsmanager_secret" "example" { arn = var.secret_arn }
data "aws_secretsmanager_secret_version" "secret-version" {
  secret_id = data.aws_secretsmanager_secret.example.id
}
output "aws_secret_value" {
  value     = data.aws_secretsmanager_secret_version.secret-version.value
  sensitive = true
}

data "vault_generic_secret" "example" { path = var.vault_path }
output "vault_secret" {
  value     = data.vault_generic_secret.example.data[var.vault_key]
  sensitive = true
}
```

**Don't:**
- Don't keep secrets in `*.tfvars` checked into Git.
- Don't put secrets in `TF_VAR_*` env vars in plain-text CI logs.
- Don't expose secret values through state unless absolutely necessary — prefer attaching ARNs to resources that fetch secrets at runtime (ECS task definition, K8s `envFrom`).

*Ref: Terraform_in_Depth.md — "8.5.2 Secret managers"*

---

### 46. Adopt GitOps with Drift Detection and Reconciliation

CNCF GitOps principles:
- *Declarative* — describe the desired state (Terraform does this natively).
- *Versioned and immutable* — keep state in Git.
- *Pulled automatically* — let the orchestrator fetch the config and call Terraform.
- *Continuously reconciled* — scheduled plans detect drift; humans or auto-correction respond.

A 2021 Travis-CI-style incident reminded us that *orchestrator-side* secrets need extra defense — OIDC + short-lived credentials > long-lived tokens.

*Ref: Terraform_in_Depth.md — "8.3 GitOps"*

---

### 47. Pick the Right CD Platform (TACOS)

| System            | Open source | State backend | Registry | Terraform only | Policy enforcement | Cost estimates |
|-------------------|:-----------:|:-------------:|:--------:|:--------------:|:------------------:|:--------------:|
| HCP Terraform      | No          | Yes           | Yes      | Yes            | Sentinel + OPA     | Yes (built-in) |
| Spacelift         | No          | Yes           | Yes      | No (Tofu, etc.) | OPA                | Infracost      |
| Env0              | No          | Yes           | Yes      | No             | OPA                | Infracost      |
| Scalr             | No          | Yes           | Yes      | Yes            | OPA                | Infracost      |
| Digger            | Yes         | No            | No       | Yes            | OPA                | No             |
| Terrateam         | No          | No            | No       | Yes            | Checkov + OPA      | Infracost      |
| Atlantis          | Yes         | No            | No       | Yes            | None               | No             |
| Terrakube         | Yes         | Yes           | Yes      | Yes            | OPA                | Infracost      |
| Harness           | No          | No            | No       | No             | OPA                | Infracost      |
| Octopus Deploy    | No          | No            | No       | No             | None               | Infracost      |

- **HCP Terraform** is the most polished for Terraform-only; rejects newer HashiCorp Terraform versions for competitors.
- **Spacelift / Env0 / Scalr** are the dominant OpenTofu-friendly TACOS; Env0 + Spacelift each sponsor 5 OpenTofu core devs.
- **Atlantis** is the easiest on-ramp (GitOps from PR comments).
- **Digger / Terrateam** are the new GitOps-from-PR-comment generation.
- **Terrakube** is the only self-hosted all-in-one.
- **Harness / Octopus** are general CD with Terraform support — pick if you have non-IaC workloads too.

*Ref: Terraform_in_Depth.md — "8.7 CD platform overview"*

---

### 48. Test What Matters — Transformations, Not Provider Glue

**Do test:**
- Data transforms (your logic, not the provider's).
- String construction from variables + data sources.
- Regular expressions with multiple patterns.
- Dynamic blocks with zero/one/many entries.
- System functionality (HTTP endpoints, generated credentials).

**Don't test:**
- Whether setting `instance_type = "t3.micro"` returns `t3.micro` — the AWS provider already tests that.
- Every permutation of every input — focus on edges that exercised your code.

*Ref: Terraform_in_Depth.md — "9.1.1 What to test"*

---

### 49. Make Tests Realistic — Examples Double as Test Fixtures

```hcl
resource "random_string" "random" {
  length  = 8
  special = false
  upper   = false
}
module "alb_example" {
  source = "../"
  name   = "testing_${random_string.random.result}"
}
```

Add randomness to resource names so concurrent test runs don't collide. AWS Secrets Manager takes a *week* to allow reusing a deleted name — build randomness into module defaults when possible.

Always provide for *automatic cleanup* on test failure: AWS Nuke (`rebuy-de/aws-nuke`), Azure Nuke (`ekristen/azure-nuke`), GCP project delete. Configure them in CI with OIDC and a tight role.

*Ref: Terraform_in_Depth.md — "9.2 Testing IaC in practice"*

---

### 50. Use Terratest for Integration Tests (Go)

```go
package tests

import (
    "os"
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestExample(t *testing.T) {
    t.Parallel()

    testInput := "test"
    terraformBinary := os.Getenv("TERRATEST_BINARY")
    if len(terraformBinary) <= 0 {
        terraformBinary = "terraform"
    }

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir:    "../examples/basic",
        TerraformBinary: terraformBinary,
        Vars: map[string]interface{}{
            "test_input": testInput,
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    testOutput := terraform.Output(t, terraformOptions, "test_output")
    assert.Equal(t, testInput, testOutput)
}
```

```makefile
.PHONY: terratest
terratest:
	cd test && go mod init github.com/your-org/your-module
	cd test && go mod tidy
	cd test && go test -v -timeout 60m $(GO_TEST_OPTS)
```

**Always set `-timeout 60m`** (or longer) — Go's default is 10m, and a hard kill leaves orphaned infra that costs money.

**Use `terraform.WithDefaultRetryableErrors`** — it auto-retries the common transient API errors so you don't have to.

*Ref: Terraform_in_Depth.md — "9.3 Terratest"*

---

### 51. Use the Native Terraform Testing Framework for Unit-Style Tests

```hcl
# tests/example.tftest.hcl
variables {
  test_input = "test"
}

run "input_and_output_match" {
  command = apply
  assert {
    condition     = output.test_output == "test"
    error_message = "The output does not match the input."
  }
}
```

```hcl
run "input_passed_to_resource" {
  assert {
    condition     = terraform_data.this.input == "test"
    error_message = "The resource parameter does not match the input."
  }
}
```

**Mock providers** (Terraform 1.7+, beta) for cheap, fast unit tests:

```hcl
mock_provider "aws" {
  mock_data "aws_region" {
    defaults = { name = "us-east-1" }
  }
}

run "dns_record_name" {
  command = plan
  variables {
    zone_id = "Z1234567890"
    records = ["127.0.0.1"]
    domain  = "example.com"
    name    = "my_test"
  }
  assert {
    condition     = aws_route53_record.main.name == "my_test.us-east-1.example.com"
    error_message = "Domain name not properly generated from region."
  }
}
```

**Reusable mocks:** put `mock_data`/`mock_resource` blocks in a `tests/mocks/` directory and import via `mock_provider "aws" { source = "./tests/mocks" }`.

*Ref: Terraform_in_Depth.md — "9.4 Terraform testing framework"*

---

### 52. Matrix-Stratify Your Tests Across Engines + Versions

```yaml
name: Terratest
on: [push, pull_request]
jobs:
  terratest:
    strategy:
      matrix:
        engine: ["opentofu", "terraform"]
        version: ["1.6", "1.7", "1.8"]
        experimental: [false]
        test: [BasicTest, LambdaTest, ECSTest, Ec2Test]
      include:
        - version: "1.9"
          engine: "opentofu"
          experimental: true
          test: [BasicTest, LambdaTest, ECSTest, Ec2Test]
      continue-on-error: ${{ matrix.experimental }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        if: ${{ matrix.engine == 'terraform' }}
        with: { terraform_version: ${{ matrix.version }} }
      - uses: opentofu/setup-opentofu@v1
        if: ${{ matrix.engine == 'opentofu' }}
        with: { tofu_version: ${{ matrix.version }} }
      - run: make terratest TF_ENGINE=${{ matrix.engine }} GO_TEST_OPTIONS="-run ${{ matrix.test }}"
```

For the native framework, run each example folder as a separate matrix entry — the test framework runs one `.tftest.hcl` file per invocation.

*Ref: Terraform_in_Depth.md — "9.3.6 Testing with CI", "9.4.6 Testing with CI"*

---

### 53. Refactor Safely: `moved` Blocks, Dual-Naming Variables, Major Version Discipline

**Renaming resources:**
```hcl
moved {
  from = random_password.my_password
  to   = random_password.main
}
```
`moved` is safe to leave in place indefinitely — once the from state is empty, it does nothing.

**Renaming variables (parallel change / expand-and-contract):**
```hcl
variable "my_old_variable" {
  type    = string
  default = null
}
variable "my_new_variable" {
  type    = string
  default = "my_fancy_default"
}
locals {
  use_this_variable = var.my_old_variable != null ? var.my_old_variable : var.my_new_variable
}
output "my_output" { value = local.use_this_variable }
```
Delete the deprecated variable only in the next major release.

**Project reorganization:**
- Terraform doesn't care about file layout. Move resources between files freely; reordering inside a block is a no-op.
- Use headers (`# --- Networking ---`) or split `main.tf` by concern — pick one and stay consistent.

*Ref: Terraform_in_Depth.md — "9.5 Refactoring"*

---

### 54. Plan a Major Version Release Carefully

- Collect breaking-change wishes in a `CHANGELOG.md` or ticket queue; release them together when an upstream provider has its own major bump (cascade justification).
- Branch off, develop features in parallel via PRs, merge to a release branch, tag, merge to main.
- Maintain the previous major with security patches for at least one release cycle.

*Ref: Terraform_in_Depth.md — "9.6 External refactoring"*

---

### 55. Adopt Hierarchical Naming Conventions

**Goals:** unique, human-readable, identifiable, sortable.

```
acme-dev-api
acme-dev-api-lb
acme-dev-api-cluster
acme-dev-api-service
acme-dev-api-logs
acme-prod-api
…
```

```hcl
locals {
  application = "acme"
  base_name  = "${local.application}-${var.environment}"
}
module "api"      { source = "./service"; name = "${local.base_name}-api" }
module "database" { source = "./db";      name = "${local.base_name}-db" }
```

Use `random_string` for resource-specific naming constraints (e.g., `aws_secretsmanager_secret`):
```hcl
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}
resource "aws_secretsmanager_secret" "main" {
  name = "${var.name}-${random_string.suffix.result}"
}
```

*Ref: Terraform_in_Depth.md — "10.1 Names and domains"*

---

### 56. Build Networks with `cidrsubnet` and Modular Topology Switches

```hcl
locals {
  subnet_bits   = var.availability_zones == 1 ? 0 : (var.availability_zones > 2 ? 2 : 1)
  subnet_count  = pow(2, local.subnet_bits)
  spare_subnet_cidr_blocks = [
    for i in range(var.availability_zones, local.subnet_count)
    : cidrsubnet(var.cidr_block, local.subnet_bits, i)
  ]
}

data "aws_availability_zones" "available" { state = "available" }

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
}

module "two_tier_subnets" {
  source   = "./modules/az_2"
  count    = var.enable_isolated_subnet ? local.subnet_count : 0
  for_each = { for az in data.aws_availability_zones.available.names : az => az }
  availability_zone = each.value
  vpc_id   = aws_vpc.main.id
  cidr_block = cidrsubnet(var.cidr_block, local.subnet_bits, each.key)
}
```

Use `count` for the topology binary toggle (`two_tier` vs `three_tier`) and `cidrsubnet` to carve subnets dynamically. Return `spare_subnet_cidr_blocks` as an output so users can decide what to do with leftover space.

*Ref: Terraform_in_Depth.md — "10.2 Network management"*

---

### 57. Avoid Provisioners — Use Cloud-Init, Packer, and Image Baking

Provisioners break Terraform's declarative model: they are imperative side-effects with unpredictable failure modes, they break the plan graph, and they run outside of state.

**Instead:**
- Pre-install software into machine images (Packer, Docker, cloud image baking).
- Pass configuration via `user_data` / Cloud-Init / launch templates.
- Use `terraform_data` + a custom command only when there is genuinely no provider-side equivalent.

When you must use a provisioner, attach it to `terraform_data` (not a real resource) so it isn't tied to the lifecycle of unrelated infra:

```hcl
resource "terraform_data" "provisioners" {
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = aws_instance.main.public_ip
  }
  provisioner "remote-exec" {
    script = "${path.module}/scripts/initialize.sh"
  }
  depends_on = [aws_instance.main, aws_db_instance.main]
}
```

*Ref: Terraform_in_Depth.md — "10.3 Provisioners"*

---

### 58. Use the External Provider for Last-Resort Custom Data Sources

```hcl
data "external" "main" {
  program = ["bash", "${path.module}/script.sh"]
  query   = { foo = "bar" }
}
output "result" { value = data.external.main.result }
```

```bash
#!/usr/bin/env bash
# Square-root script
a=$(bc <<<"scale=0; sqrt($1)")
echo "{\"value\":\"$a\"}"
```

Use Bash for portability when redistributing modules; consider Go + a real provider when you control the delivery environment and need richer logic.

*Ref: Terraform_in_Depth.md — "10.4 External provider"*

---

### 59. Use the Local Provider to Read/Save Local Files

```hcl
data "local_file" "foo" { filename = "${path.module}/config.txt" }
data "local_sensitive_file" "foo" { filename = "${path.module}/private.key" }

resource "local_file" "main" {
  content  = "Hello World!"
  filename = "${path.module}/hello.txt"
}
```

Provider-defined functions (Terraform 1.8+):
```hcl
locals {
  file_exists = fileexists("${path.module}/example.txt")
  dir_exists  = provider::local::direxists("${path.module}/scripts/")
}
```

*Ref: Terraform_in_Depth.md — "10.5 Local provider"*

---

### 60. Add `precondition` and `postcondition` Blocks for Resource-Level Validation

```hcl
resource "aws_lb" "example" {
  name               = "example"
  load_balancer_type = var.type
  ip_address_type    = var.ip_address_type
  subnets            = var.subnet_ids

  lifecycle {
    precondition {
      condition     = var.type == "application" ? true : var.ip_address_type != "dualstack-without-public-ipv4"
      error_message = "The ip address type can only be set to dualstack-without-public-ipv4 when the Load Balancer Type is application."
    }
  }
}
```

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  filter { name = "name"; values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"] }
  filter { name = "virtualization-type"; values = ["hvm"] }
  owners = ["099720109477"]
  lifecycle {
    postcondition {
      condition     = timecmp(timestamp(), self.deprecation_time) == -1
      error_message = "Unable to find an AMI that is not deprecated."
    }
  }
}
```

Use `self.<attr>` to refer to the resource itself; `condition` may reference any expression.

*Ref: Terraform_in_Depth.md — "10.6 Checks and conditions"*

---

### 61. Use `check` Blocks for Non-Blocking Health Assertions (Saved to State)

```hcl
check "password_strength" {
  data "random_password" "new_password" { length = 12 }
  assert {
    condition     = length(random_password.new_password.result) >= 12
    error_message = "random_password.new_password.id should return a password at least 12 characters long."
  }
}
```

`check_results` are persisted to state so dashboards and orchestrators can surface them.

*Ref: Terraform_in_Depth.md — "10.6.2 Checks"*

---

### 62. Know When NOT to Use Terraform

| Use case                  | Better tool                                                |
|---------------------------|-----------------------------------------------------------|
| Kubernetes manifests      | Helm, Kustomize, ArgoCD                                   |
| Container image build     | Dockerfile + Docker / Buildah / Kaniko                    |
| Machine image build       | Packer                                                     |
| Artifact storage/versioning | Artifactory, Nexus, Cloudsmith                         |

*Ref: Terraform_in_Depth.md — "10.8 When Terraform isn't appropriate"*

---

### 63. Drive Terraform from JSON or CDKTF When Generating Config Programmatically

**JSON as alternative syntax:**
```json
{
  "resource": {
    "terraform_data": {
      "main": {
        "input": "${var.test_input}"
      }
    }
  },
  "output": {
    "site_data": { "value": "${resource.terraform_data.main.output}" }
  }
}
```
Use `//` keys for comments: `"//": "Auto-generated"`.

**CDKTF** (Terraform only — no OpenTofu support) — generate configs from TypeScript, Python, Java, C#, or Go:
```python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.instance import Instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        instance = Instance(self, "main", ami="ami-12345678", instance_type="t3.micro")
        TerraformOutput(self, "public_ip", value=instance.public_ip)

app = App()
MyStack(app, "my-stack")
app.synth()
```

`cdktf synth` produces JSON; `cdktf deploy` runs `terraform plan && apply`. Use CDKTF when you need typed configs in your general-purpose language or when you build tooling that generates infra — but for day-to-day module work, HCL is still the right tool.

*Ref: Terraform_in_Depth.md — "11.2 Using JSON instead of HCL", "11.3 Cloud Development Kit for Terraform"*

---

### 64. Wrap the CLI in Python for Custom Scanners / CI Tools

Terraform emits JSON for most commands; wrap it in Python (or any language) to build custom tooling — security scanners, drift detectors, plan reviewers.

```python
import json, subprocess

def plan(project_dir):
    out = subprocess.check_output(
        ["terraform", "plan", "-json"],
        cwd=project_dir,
    )
    # each line is a JSON-encoded UI event
    for line in out.splitlines():
        event = json.loads(line)
        if event["type"] == "resource_drift":
            handle_drift(event)
```

*Ref: Terraform_in_Depth.md — "11.1 Wrapping Terraform"*

---

### 65. Build Custom Providers with the Terraform Plugin Framework (Go)

**Bootstrap with the HashiCorp scaffolding template**, then implement the `provider.Provider` interface:

```go
func (p *MastodonProvider) Metadata(ctx context.Context, req provider.MetadataRequest, resp *provider.MetadataResponse) {
    resp.TypeName = "mastodon"
    resp.Version  = p.version
}

func (p *MastodonProvider) Schema(ctx context.Context, req provider.SchemaRequest, resp *provider.SchemaResponse) {
    resp.Schema = schema.Schema{
        Attributes: map[string]schema.Attribute{
            "host": schema.StringAttribute{
                MarkdownDescription: "Mastodon host to connect to.",
                Optional:            true,
                Default:             stringdefault.StaticString("mastodon.social"),
            },
            "access_token": schema.StringAttribute{
                Optional:  true,
                Sensitive: true,
            },
        },
    }
}

func (p *MastodonProvider) Configure(ctx context.Context, req provider.ConfigureRequest, resp *provider.ConfigureResponse) {
    var data MastodonProviderModel
    tflog.Debug(ctx, "mastodon provider configure")
    resp.Diagnostics.Append(req.Config.Get(ctx, &data)...)
    if resp.Diagnostics.HasError() { return }

    accessToken := os.Getenv("MASTODON_ACCESS_TOKEN")
    if !data.AccessToken.IsNull() {
        accessToken = data.AccessToken.ValueString()
        ctx = tflog.SetField(ctx, "mastodon_access_token", accessToken)
        ctx = tflog.MaskFieldValuesWithFieldKeys(ctx, "mastodon_access_token")
    } else {
        resp.Diagnostics.AddAttributeError(
            path.Root("access_token"),
            "Missing Mastodon Credentials",
            "The provider cannot create the Mastodon API client as no Access Token is set.",
        )
        return
    }
    // ... build API client, store on resp.ResourceData / resp.DataSourceData
}
```

**Local development override:**
```hcl
# ~/.terraformrc
provider_installation {
  dev_overrides {
    "terraformindepth/mastodon" = "/Users/you/go/bin/"
  }
  direct {}
}
```

**Resource CRUD:**
```go
func (r *PostResource) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
    var data PostResourceModel
    resp.Diagnostics.Append(req.Plan.Get(ctx, &data)...)
    post, err := r.client.CreatePost(data.Content.ValueString())
    if err != nil {
        resp.Diagnostics.AddError("Create failed", err.Error())
        return
    }
    data.Id = types.StringValue(post.ID)
    resp.Diagnostics.Append(resp.State.Set(ctx, &data)...)
}
```

**Tests:** unit tests start with `Test`; acceptance tests start with `TestAcc` and only run when `TF_ACC=1`. Always set the version, register the resource, and write both unit + acceptance tests before publishing.

**Publishing:** generate docs with `tfplugindocs`, create a GPG key, register the provider on the registry, tag a release — the registry builds and signs automatically.

*Ref: Terraform_in_Depth.md — "12 Terraform providers"*

---

### 66. Choose OpenTofu vs. HashiCorp Terraform Deliberately

| Concern                              | HashiCorp Terraform                                  | OpenTofu                                                            |
|--------------------------------------|------------------------------------------------------|---------------------------------------------------------------------|
| License                              | BSL 1.1 (proprietary from v1.6+)                     | MPL 2.0 (fully open source)                                          |
| Forked from                          | HashiCorp                                            | Terraform v1.5.7 (last MPL release)                                 |
| Compatibility with Terraform         | Reference                                            | Drop-in for v1.6; now superset with extra features                  |
| CD platform support                  | HCP Terraform, Env0, Spacelift, Scalr, Atlantis, Digger | Same vendors + Atlantis + Terrakube, but most now require OpenTofu for new features |
| Governance                           | HashiCorp                                            | Linux Foundation (CNCF)                                            |
| Public module registry               | registry.terraform.io                                | OpenTofu registry + still indexed by HashiCorp                      |
| OIDC in CD                           | HCP Terraform, GitHub Actions, etc.                  | Same                                                               |
| `tofu login` / `terraform login`     | Available                                            | Available                                                          |

OpenTofu is now the safer long-term choice for any new project — it is the version used by Spacelift, Env0, Scalr, Harness, Terrakube, and most of the ecosystem. HashiCorp Terraform remains relevant only if you need HCP Terraform's tightly integrated Sentinel + cost estimation.

*Ref: Terraform_in_Depth.md — "1.6 Terraform and OpenTofu"*

---

## Anti-Patterns & Common Mistakes

- **Hardcoding instead of variables** — every region, AMI, instance type, subnet ID, or tag should be a variable or data source lookup, not a string literal. → *fix:* variable + data source + sensible default.
- **Implicit provider source** — relying on `hashicorp/<localname>` lookup. → *fix:* declare every provider in `required_providers` with an explicit version constraint.
- **`count = var.bool ? 1 : 0` accidentally dropping resources** — when the count drops to 0, Terraform plans to destroy them. → *fix:* document the behavior, or use `for_each = {for x in var.bool ? ["a"] : [] : x => x}` if you need stable addresses.
- **`terraform taint`** — deprecated; immediately mutates state without showing impact. → *fix:* `terraform plan -replace='addr'` then review.
- **Manual JSON state editing** — high blast radius, easy to corrupt. → *fix:* `moved`, `removed`, `import` blocks; or `terraform state mv/rm/replace-provider`.
- **`terraform refresh`** — deprecated, mutates state without confirmation. → *fix:* `terraform apply -refresh-only`.
- **Local backend in production** — no resilience, no team sharing. → *fix:* S3 + DynamoDB lock (or HCP/Spacelift/Env0).
- **`-target` as routine** — modules that require it are broken. → *fix:* refactor so the DAG orders correctly without targeting.
- **Secrets in `*.tfvars` / `-var` CLI / Git** — leaks via shell history, logs, repo history. → *fix:* OIDC + secret manager + `sensitive = true`.
- **`prevent_destroy = true` on everything** — makes dev environments impossible. → *fix:* `ignore_changes` is almost always the right tool.
- **`-refresh=false` to "speed things up"** — masks drift → failed applies. → *fix:* leave refresh on; tune parallelism or pre-stage.
- **Circular dependencies** — Terraform errors with `Cycle: …`. → *fix:* introduce an upstream variable or refactor the architecture.
- **Cascading replacements** — change one attribute, replace five resources. → *fix:* inspect every plan, route replace-triggering attributes through `ignore_changes` or `replace_triggered_by`.
- **Always-detected changes ("eternal drift")** — provider normalizer bugs. → *fix:* match your input to the API's response format, file upstream.
- **Drift in production** — manual hotfixes. → *fix:* get the change into code immediately, otherwise the next `apply` reverts it.
- **Module-level `terraform_remote_state`** — couples your module to a specific backend. → *fix:* keep `terraform_remote_state` in the root module only; prefer data sources.
- **Pulling modules from GitHub default branch** — no version constraint → random breakage. → *fix:* SCM-based delivery with `ref = v1.0.1` or, better, a registry.
- **`count` instead of `for_each` for map inputs** — adding/removing one entry reshuffles indices and destroys the wrong resources. → *fix:* `for_each` over a map or set.
- **Ternary accessing a toggled-off resource** — evaluates both sides and errors. → *fix:* `try(..., null)` or restructure.
- **`uuid()` / `timestamp()` in resource arguments** — impure → eternal drift. → *fix:* `random_*` or `time_*` providers.
- **Provisioning with `remote-exec`/`local-exec` instead of Cloud-Init or Packer** — imperative side-effects break the plan graph. → *fix:* immutable images + user_data / Cloud-Init.
- **Importing a random ID without `moved`** — Terraform will try to recreate the resource. → *fix:* `moved { from = old_addr to = new_addr }`.
- **Hardcoded CIDRs in network modules** — no reuse across environments. → *fix:* `cidrsubnet(input, bits, index)` to derive subnets dynamically.
- **Single test that builds 5-hour DB instances serially** — CI grinds to a halt. → *fix:* GitHub Actions matrix strategy, `t.Parallel()`, per-test parallelism.
- **CI workflows without `-input=false`** — interactive prompts hang CI. → *fix:* always set `-input=false` in pipelines.
- **`terraform plan` followed by `terraform apply` without `-out`** — apply may differ from the plan. → *fix:* always save the plan with `-out`.
- **Auto-approve in production** — one typo wipes a fleet. → *fix:* always require manual approval, even for "fast fixes".
- **Not enabling `-parallelism=1` + `TF_LOG=DEBUG` when debugging** — logs interleave across 10 parallel operations. → *fix:* lower parallelism for debugging.
- **Using HCP Terraform because "it's Terraform Cloud"** — pricing model charges per-resource in state (a VPC = ~$7.25/mo). → *fix:* evaluate Spacelift, Env0, Scalr, or Terrakube first.
- **Copying the `template_file` resource** — deprecated. → *fix:* `templatefile()` (and `templatestring()` since Terraform 1.9 / OpenTofu 1.6).
- **Bumping the Major version for cosmetic changes** — degrades trust. → *fix:* batch breaking changes; reserve Major for incompatible changes.
- **Trusting `ignore_changes` without review** — masks real drift. → *fix:* tag the attribute and write a comment explaining why it's safe to ignore.
- **Locking CI to a single Terraform version** — your module stops being useful for users on older engines. → *fix:* matrix across the version range you support.
- **Bypassing `terraform fmt` because "we have prettier"** — style is enforced by `fmt`; mixing styles breaks tooling. → *fix:* always run `fmt` before commit.
- **Forgetting `depends_on` on time-sensitive resources** — Terraform can launch a follow-up resource before the script finishes. → *fix:* explicit `depends_on` on `time_sleep` or other prerequisites.

---

## Decision Heuristics / Checklists

- **State backend choice** — Already on AWS? → `s3` + DynamoDB. Multi-cloud? → `cloud` (Spacelift, Env0, Scalr). Self-hosted? → Terrakube. Don't use `local` outside dev.
- **Module change kind** — New optional input? → Minor (`v1.1.0`). Bug fix? → Patch (`v1.0.1`). Rename input? → `moved` block now, Major release later. Resource attribute rename? → `moved` block only.
- **`count` vs `for_each`** — `for_each` over a map/set whenever the key is meaningful (stable addresses, no cascading recreation on reorder). `count` for boolean toggles and integer-driven loops. Never `for_each` over a list — `toset()` it first if you must.
- **Lifecycle override** — Want to survive upstream rotations? → `ignore_changes`. Need zero-downtime replacement? → `create_before_destroy`. Need to force a recreate on input change? → `replace_triggered_by` (or `terraform_data.triggers_replace` for non-resource inputs). Use `prevent_destroy` only for hard compliance boundaries.
- **Secrets handling** — OIDC + cloud IAM role → preferred. Cloud secret manager → for credentials that OIDC can't cover. CI/orchestrator secrets → only as last resort; never in `*.tfvars` or Git.
- **CD platform** — Single IaC framework, small team → HCP Terraform if pricing acceptable; otherwise OpenTofu + Spacelift/Env0/Scalr. Multi-framework → Env0 or Spacelift. Self-host → Terrakube. PR-comment UX → Atlantis (simple) or Digger/Terrateam (rich).
- **Test framework** — New team → native `.tftest.hcl` + mocks (Terraform 1.7+). Wide version support → Terratest. Production-going module → use both.
- **Drift response** — Identify the cause first (accidental, intentional, automated, Terraform error). Fix the cause, then the symptom.
- **Network segmentation** — Two tiers (public + private) is enough for most. Three tiers (add isolated) when compliance demands no internet egress. Use the count-based binary toggle between topology modules to keep callers simple.
- **Project structure** — One app, one env → application-as-root. Multiple envs at different module versions → environment-as-root. Many envs with shared config → Terragrunt.
- **Provider development** — Use the HashiCorp `terraform-provider-scaffolding` template. Always implement both unit (`Test…`) and acceptance (`TestAcc…`) tests. Use `resp.Diagnostics.Append` (not log.Fatal) for errors. Generate docs with `tfplugindocs`.

---

## Key Takeaways

1. **Terraform is declarative; trust the DAG.** Understand that resources form a directed acyclic graph, modules don't influence ordering, and `depends_on` is only for hidden edges.
2. **State is critical infrastructure.** Pick a remote backend with locking from day one, take external backups, and test restore regularly.
3. **Plan before applying.** Always `terraform plan -out=plan.tfplan` in production; never `terraform refresh`; prefer `-replace` over `terraform taint`.
4. **Pin everything.** Providers in `required_providers`, modules with pessimistic version constraints, providers with `version`/`source`.
5. **Modules are the unit of reuse.** Good module design — clear inputs, explicit types, validated variables, sensible outputs, type-constrained objects — is the foundation of scalable Terraform.
6. **`for_each` > `count` for maps/sets.** Stable addresses, no cascading recreation on reorder. Use `count = var.bool ? 1 : 0` only for true boolean toggles.
7. **Lifecycle is your escape hatch.** `create_before_destroy`, `ignore_changes`, `replace_triggered_by`, `moved` blocks — each solves a different problem.
8. **Lint, format, validate, scan, plan in CI.** `terraform fmt -check` → `terraform validate` → `tflint` → `checkov` + `trivy` → `terraform plan` in that order. Use a Cookiecutter template + Makefile so every repo gets it for free.
9. **Test what matters — transformations, not provider glue.** Terratest for integration, native `.tftest.hcl` + mocks for unit-style, `t.Parallel()` + GitHub Actions matrix for parallelism.
10. **GitOps from main, with drift detection.** SCM as source of truth, scheduled reconciliation, OIDC for CI → cloud auth, no stored credentials.
11. **OIDC instead of secrets.** Trust policies scoped to repo + branch + workflow path. `MASTODON_ACCESS_TOKEN`-style env vars are for the trash bin.
12. **Know when not to use Terraform.** K8s → Helm/ArgoCD. Images → Packer/Docker. Artifacts → Artifactory.
13. **OpenTofu is the de facto choice.** HashiCorp's 2023 BSL relicense made OpenTofu (Linux Foundation) the path forward for new projects that need cross-vendor TACOS.
14. **Refactor with `moved` blocks.** Never destroy-and-recreate to rename a resource. Batch breaking changes for major versions; keep the old major on security-patch support.
15. **Custom providers belong in the Plugin Framework.** Use the scaffolding template, implement CRUD on a typed model, log via `tflog`, return errors via `resp.Diagnostics`, and always write both unit + acceptance tests.

---

## Cross-References
- Related: [[../Building_Evolutionary_Architectures.md]] · [[../Engineering_Resilient_Systems_on_AWS.md]] · [[../Building_Microservices.md]] · [[../Cloud_Application_Architecture_Patterns.md]] · [[../Continuous_Deployment.md]]
- Topic index: [[../INDEX.md]]