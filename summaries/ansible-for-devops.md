# Ansible for DevOps - Jeff Geerling

## Comprehensive Summary

---

## Introduction: Infrastructure Management

**From sysadmins to infrastructure as code:** Traditional system administration relied on manual configuration, "snowflake" servers (unique, undocumented configurations), and shell scripts that grew into unmaintainable messes. Ansible represents the shift to declarative, reproducible infrastructure management.

**Why Ansible:**
- Agentless: Uses SSH (no agents to install on target hosts)
- Human-readable YAML playbooks
- Idempotent: Running the same playbook multiple times produces the same result
- Large ecosystem of modules and community roles
- Backed by Red Hat

---

## Chapter 1: Getting Started

**Installing Ansible:** Available via pip, system package managers (apt, yum, brew). Requires Python on control machine and target hosts.

**Inventory:** Define the hosts Ansible manages in INI or YAML format:
```
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com

[all:children]
webservers
dbservers
```

**First commands:** Ad-hoc commands for quick tasks:
```bash
ansible all -m ping           # Test connectivity
ansible webservers -m setup   # Gather system facts
ansible all -m apt -a "name=nginx state=present"  # Install nginx
```

---

## Chapter 2-3: Playbooks and Ad-Hoc Commands

**Playbooks** are Ansible's configuration, deployment, and orchestration language. Written in YAML:

```yaml
---
- hosts: webservers
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

**Key playbook concepts:**
- **Tasks**: Individual actions (install package, copy file, start service)
- **Handlers**: Tasks triggered by notifications (e.g., restart service when config changes)
- **Modules**: The tools Ansible uses to perform tasks (apt, yum, copy, template, file, service, etc.)
- **Become**: Privilege escalation (sudo)

**Ad-hoc commands** are one-liner commands for quick operations without writing a playbook. Useful for:
- Ping testing all hosts
- Rebooting servers
- Managing packages
- Gathering facts

---

## Chapter 4-5: Variables, Facts, and Advanced Playbooks

**Variable types:**
- **Playbook variables**: Defined in the playbook itself
- **Inventory variables**: Host-specific or group-specific in inventory
- **Registered variables**: Captured output from tasks
- **Facts**: System information auto-collected (OS, IP, memory, disks)
- **Magic variables**: Special Ansible variables (hostvars, group_names, inventory_hostname)

**Variable precedence** (simplified, 22 levels): Command-line > role defaults > inventory > playbook. The general rule: more specific wins over more general.

**Ansible Vault:** Encrypt sensitive data (passwords, API keys) within playbooks:
```bash
ansible-vault create secrets.yml     # Create encrypted file
ansible-vault edit secrets.yml       # Edit encrypted file
ansible-playbook site.yml --ask-vault-pass  # Run with vault
```

**Conditionals and loops:**
- `when`: Conditional task execution
- `loop` / `with_items`: Iterate over lists
- `register`: Capture task output for later use
- `changed_when` / `failed_when`: Custom change detection and failure handling

**Tags:** Selectively run parts of playbooks:
```bash
ansible-playbook site.yml --tags "nginx,config"
ansible-playbook site.yml --skip-tags "database"
```

---

## Chapter 6-7: Roles and Galaxy

**Roles** organize playbooks into reusable, shareable components with a standard directory structure:
```
role_name/
  defaults/     # Default variables (lowest precedence)
  files/        # Static files to copy
  handlers/     # Handler tasks
  meta/         # Role metadata and dependencies
  tasks/        # Main task list
  templates/    # Jinja2 templates
  vars/         # Role variables (higher precedence)
```

**Ansible Galaxy** is the community hub for sharing roles:
```bash
ansible-galaxy install geerlingguy.nginx
ansible-galaxy init my_role   # Scaffold a new role
```

**Best practices for roles:**
- Keep roles focused on a single responsibility
- Use defaults for all configurable values
- Document variables and their purposes
- Test roles independently with Molecule

---

## Chapter 8-9: Ansible for AWS and Cloud

**Dynamic inventory:** Auto-discover AWS EC2 instances, tag them, and use them as Ansible targets. AWS provides a dynamic inventory script.

**EC2 provisioning:** Create, configure, and manage EC2 instances:
```yaml
- name: Launch EC2 instance
  ec2:
    key_name: my-key
    instance_type: t3.micro
    image: ami-12345678
    region: us-east-1
    group: webserver
    count: 3
```

**VPC, security groups, and ELB:** Ansible modules manage the full AWS stack:
- `ec2_vpc_net`, `ec2_vpc_subnet`, `ec2_vpc_route_table`
- `ec2_group` (security groups)
- `ec2_elb_lb` (load balancers)
- `route53` (DNS)

**Cloud-agnostic approach:** Use variables and inventory to abstract cloud-specific details, making playbooks portable across AWS, GCP, Azure, and bare metal.

---

## Chapter 10-11: Docker and Containers

**Ansible for Docker:**
- Build Docker images with Ansible (instead of Dockerfile) for idempotent, readable builds
- `docker_image`, `docker_container`, `docker_compose` modules
- Manage container lifecycles from Ansible playbooks

**Container orchestration:** Ansible can deploy to Docker Swarm, manage container networks, volumes, and compose stacks.

---

## Chapter 12: Orchestration and Complex Workflows

**Multi-tier application deployment:** Orchestrate deployments across web, app, and database tiers with controlled sequencing:
```yaml
- hosts: dbservers
  tasks: [database migration tasks]
- hosts: appservers
  serial: 1   # One at a time
  tasks: [app deployment tasks]
- hosts: webservers
  tasks: [web server tasks]
```

**Rolling updates:** Use `serial` to update hosts in batches, with `max_fail_percentage` to stop if too many fail.

**Delegation:** Run tasks on one host on behalf of another (`delegate_to`), useful for health checks from a monitoring server.

---

## Chapter 13: Security Best Practices

**SSH hardening:**
- Disable password authentication
- Disable root login
- Change default SSH port
- Use SSH key pairs
- Configure fail2ban

**Ansible security practices:**
- Use Ansible Vault for all secrets
- Rotate encryption passwords regularly
- Use `check_mode` (dry run) before applying changes
- Implement `diff` mode to see what changes
- Audit playbooks with `ansible-lint`

---

## Chapter 14-15: Testing and CI/CD

**Molecule:** Testing framework for Ansible roles:
- Test roles against different OS images (Docker, Vagrant)
- Verify idempotency (running twice produces no changes)
- Integration with CI pipelines

**CI/CD integration:**
- Run Ansible playbooks in CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI)
- Use `--check` mode for dry runs
- Use `--diff` for change visibility
- Integrate with infrastructure testing tools (TestInfra, InSpec, Goss)

---

## Chapter 16: Ansible Tower / AWX

**Ansible Tower** (commercial) / **AWX** (open source) provides:
- Web UI for managing playbooks and inventories
- Role-based access control (RBAC)
- Job scheduling and logging
- API for integration
- Credential management
- Workflow visualization

---

## Key Takeaways

1. **Agentless architecture**: Ansible's SSH-based approach means no agents to install, update, or troubleshoot on target hosts.

2. **Idempotency is key**: Write playbooks that produce the same result regardless of how many times they run. Check state before making changes.

3. **Start with ad-hoc, graduate to playbooks**: Use ad-hoc commands for quick tasks, playbooks for repeatable processes, roles for shared components.

4. **Use roles for organization**: Roles make playbooks modular, testable, and shareable. Follow the standard directory structure.

5. **Encrypt secrets**: Use Ansible Vault for any sensitive data. Never commit plaintext credentials.

6. **Test everything**: Molecule for role testing, check mode for dry runs, CI integration for automated validation.

7. **Leverage Galaxy**: Don't reinvent the wheel. Use community roles, but review them before trusting in production.

8. **Document as code**: Playbooks are documentation. Well-written YAML with clear task names tells the story of your infrastructure.

9. **Use dynamic inventory for cloud**: Let Ansible discover your infrastructure automatically rather than maintaining static inventories.

10. **Think in terms of desired state**: Declare what you want, not how to get there. Ansible handles the how.
