# Ansible for DevOps

**Author:** Jeff Geerling
**Topic tags:** `#devops` `#cli` `#architecture`
**Language focus:** YAML / Jinja2 / Ansible (language-agnostic — runs over SSH)
**Sources:** `markdown_output/ansible-for-devops/ansible-for-devops.md` · `summaries/ansible-for-devops.md`

## TL;DR

Ansible is an agentless, SSH-based automation engine for configuration management, provisioning, and application deployment. The book teaches you to start with ad-hoc commands, graduate to playbooks, organize them with roles, parameterize everything via variables + Jinja, secure secrets with Vault, test with Molecule, and ship real apps (LAMP, Solr, Docker, ELK, GlusterFS, Mac, AWS, Kubernetes) with idempotent declared state.

---

## Best Practices by Topic

### Ansible's Value Proposition

**Principle:** Use the same declarative language for one-off commands and long-running configuration. No agents. SSH-only.

**Do:**
- Leverage Ansible for one-off commands, configuration management, and orchestration in one tool.
- Push changes from a control node; never install daemons on managed hosts.
- Use modules over raw shell — module idempotence beats shell scripts.

**Don't:**
- Run Ansible agents on managed nodes; the design is agentless.
- Equate Ansible with Puppet/Chef — they're different paradigms.

*Ref: ansible-for-devops.md — "In the beginning, there were sysadmins"*

---

### Idempotence as a Core Discipline

**Principle:** Ansible modules are idempotent — running them once or ten times yields the same end state.

**Do:**
- Use `state=present` / `state=started` and similar declarative states.
- Override `changed_when: false` only when a task genuinely doesn't change state.

**Don't:**
- Wrap a non-idempotent shell script in `command:` and pretend it's idempotent.

**Code:**
```bash
$ ansible all -m ping -u [username]
# CHANGED if the host was first discovered via setup; SUCCESS if facts already cached
```
*Ref: ansible-for-devops.md — "On snowflakes and shell scripts" / "Configuration management"*

---

### Installation and Ad-Hoc Commands

**Principle:** Install via `pip`, `dnf`, or `apt`; use ad-hoc commands for one-offs, playbooks for repeatable work.

**Code:**
```bash
$ pip install ansible           # macOS
$ dnf -y install ansible        # RHEL/Fedora
$ sudo apt-get install -y ansible  # Debian/Ubuntu

$ ansible -i hosts.ini example -m ping -u [username]
$ ansible multi -a "free -h" -u [username]
```
*Ref: ansible-for-devops.md — "Installing Ansible" / "Running your first Ad-Hoc Ansible command"*

---

### Inventory with Groups and Children

**Principle:** Group hosts by role/function; use group children and `group_vars` to share variables at the right level.

**Code:**
```ini
# Application servers
[app]
192.168.56.4
192.168.56.5

# Database server
[db]
192.168.56.6

# Group 'multi' with all servers
[multi:children]
app
db

# Variables that will be applied to all servers
[multi:vars]
ansible_user=vagrant
ansible_ssh_private_key_file=~/.vagrant.d/insecure_private_key
```
*Ref: ansible-for-devops.md — "Inventory file for multiple servers"*

---

### Ansible's Parallel Execution Model

**Principle:** Ansible forks by default; use `-f N` to increase or `-f 1` for serial runs.

**Code:**
```bash
$ ansible multi -a "hostname"
# Parallel: results may arrive out of order

$ ansible multi -a "hostname" -f 1
# Serial: deterministic order

$ ansible app -b -a "service chronyd restart" --limit "*.4"
# Limit to a single host by wildcard
```
*Ref: ansible-for-devops.md — "Discover Ansible's parallel nature" / "Make changes to just one server"*

---

### Package Management Across Distros

**Principle:** Use the per-OS module (`apt`, `dnf`, `yum`, `package`) for clarity; use `package` when you need cross-platform abstraction.

**Code:**
```bash
$ ansible app -b -m package -a "name=git state=present"
$ ansible db -b -m dnf -a "name=mariadb-server state=present"
$ ansible db -b -m service -a "name=mariadb state=started enabled=yes"
```
*Ref: ansible-for-devops.md — "Manage packages"*

---

### First Playbook: chrony Install + Service

**Principle:** Playbooks are ordered lists of plays (one per host group), each play contains tasks (modules with state).

**Code:**
```yaml
---
- hosts: all
  become: yes

  tasks:
    - name: Ensure chrony (for time synchronization) is installed.
      dnf:
        name: chrony
        state: present

    - name: Ensure chrony is running.
      service:
        name: chronyd
        state: started
        enabled: yes
```

**Shorthand equivalent:**
```yaml
---
- hosts: all
  become: yes
  tasks:
    - dnf: name=chrony state=present
    - service: name=chronyd state=started enabled=yes
```
*Ref: ansible-for-devops.md — "Your first Ansible playbook"*

---

### First Real Playbook (Node.js App)

**Principle:** A real playbook orchestrates package install + app copy + dependency resolution + supervised start, with idempotence at every step.

**Code:**
```yaml
---
- name: Install Node.js and npm.
  dnf: name=npm state=present enablerepo=epel

- name: Install Forever (to run our Node.js app).
  npm: name=forever global=yes state=present

- name: Ensure Node.js app folder exists.
  file: "path={{ node_apps_location }} state=directory"

- name: Copy example Node.js app to server.
  copy: "src=app dest={{ node_apps_location }}"

- name: Install app dependencies defined in package.json.
  npm: path={{ node_apps_location }}/app

- name: Check list of running Node.js apps.
  command: npx forever list
  register: forever_list
  changed_when: false

- name: Start example Node.js app.
  command: "npx forever start {{ node_apps_location }}/app/app.js"
  when: "forever_list.stdout.find(node_apps_location + '/app/app.js') == -1"
```
*Ref: ansible-for-devops.md — "Real-world playbook: Node.js app server"*

---

### Real-World Playbook: LAMP + Drupal (Ubuntu)

**Principle:** Larger stacks split into `vars_files`, `pre_tasks`, `handlers`, `tasks` for readability.

**Code:**
```yaml
---
- hosts: all
  become: yes

  vars_files:
    - vars.yml

  pre_tasks:
    - name: Update apt cache if needed.
      apt: update_cache=yes cache_valid_time=3600

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted

  tasks:
    - name: "Install Apache, MySQL, PHP, and other dependencies."
      apt:
        state: present
        name:
          - apache2
          - mysql-server
          - php8.2-common
          - php8.2-mysql

    - name: Enable Apache rewrite module (required for Drupal).
      apache2_module: name=rewrite state=present
      notify: restart apache

    - name: Add Apache virtualhost for Drupal.
      template:
        src: "templates/drupal.test.conf.j2"
        dest: "/etc/apache2/sites-available/{{ domain }}.test.conf"
        mode: 0644
      notify: restart apache

    - name: Adjust OpCache memory setting.
      lineinfile:
        dest: "/etc/php/8.2/apache2/conf.d/10-opcache.ini"
        regexp: "^opcache.memory_consumption"
        line: "opcache.memory_consumption = 96"
        state: present
      notify: restart apache

    - name: Create a MySQL database for Drupal.
      mysql_db: "db={{ domain }} state=present"

    - name: Create a MySQL user for Drupal.
      mysql_user:
        name: "{{ domain }}"
        password: "1234"
        priv: "{{ domain }}.*:ALL"
        host: localhost
        state: present

    - name: Install Drupal.
      command: >
        vendor/bin/drush si -y --site-name="{{ drupal_site_name }}"
        --account-name=admin --account-pass=admin
        --db-url=mysql://{{ domain }}:1234@localhost/{{ domain }}
        --root={{ drupal_core_path }}/web
        chdir={{ drupal_core_path }}
        creates={{ drupal_core_path }}/web/sites/default/settings.php
      become_user: www-data
      notify: restart apache
```
*Ref: ansible-for-devops.md — "Real-world playbook: Ubuntu LAMP server with Drupal"*

---

### Variables Precedence and Sourcing

**Principle:** Variables come from many places; more specific wins. Inventory `vars` beat group defaults, which beat role defaults.

**Precedence (high → low, simplified):** command-line `--extra-vars` → role defaults → play vars → inventory vars → play vars_files → defaults.

**Code:**
```yaml
---
- hosts: webservers
  vars:
    http_port: 80           # play-scoped
  vars_files:
    - vars.yml              # external
  roles:
    - role: nginx           # role defaults
      vars:
        http_port: 8080     # role-scoped override
```
*Ref: ansible-for-devops.md — "Variable Precedence"*

---

### Registered Variables and `when`

**Principle:** Capture task output via `register:`, then gate subsequent tasks with `when:` based on stdout/stderr.

**Code:**
```yaml
- name: Check for existing log files in dynamic log_file_paths variable.
  find:
    paths: "{{ item }}"
    patterns: '*.log'
  register: found_log_file_paths
  with_items: "{{ log_file_paths }}"

- command: forever list
  register: forever_list

- command: forever start /path/to/app/app.js
  when: "forever_list.stdout.find('/path/to/app/app.js') == -1"

- shell: php --version
  register: php_version

- shell: dnf -y downgrade php*
  when: "'7.0' in php_version.stdout"
```
*Ref: ansible-for-devops.md — "register" / "when"*

---

### `changed_when`, `failed_when`, `ignore_errors`

**Principle:** Tell Ansible when raw `command`/`shell` results count as changes, failures, or should be ignored — without losing control of playbook flow.

**Code:**
```yaml
- name: Install dependencies via Composer.
  command: "/usr/local/bin/composer global require phpunit/phpunit --prefer-dist"
  register: composer
  changed_when: "'Nothing to install' not in composer.stdout"

- name: Import a Jenkins job via CLI.
  shell: >
    java -jar /opt/jenkins-cli.jar -s http://localhost:8080/
    create-job "My Job" < /usr/local/my-job.xml
  register: import
  failed_when: "import.stderr and 'exists' not in import.stderr"
```
*Ref: ansible-for-devops.md — "changed_when and failed_when" / "ignore_errors"*

---

### Delegation, Local Actions, and `wait_for`

**Principle:** Use `delegate_to:` to run a task on one host for all hosts (LB pool add/remove); use `wait_for` to pause for boot/port availability.

**Code:**
```yaml
- name: Add server to Munin monitoring configuration.
  command: monitor-server webservers {{ inventory_hostname }}
  delegate_to: "{{ monitoring_master }}"

- name: Remove server from load balancer.
  command: remove-from-lb {{ inventory_hostname }}
  delegate_to: 127.0.0.1

- name: Wait for web server to start.
  local_action:
    module: wait_for
    host: "{{ inventory_hostname }}"
    port: "{{ webserver_port }}"
    delay: 10
    timeout: 300
    state: started
```
*Ref: ansible-for-devops.md — "Delegation, Local Actions, and Pauses" / "Pausing playbook execution with wait_for"*

---

### Jinja2 Templating in Playbooks

**Principle:** Use Jinja2 expressions inline; quote them whenever leading `{{ }}` or `:` could confuse YAML.

**Do:**
- Use `{{ var }}` syntax for substitution.
- Quote strings that begin with `{` or contain `:`.
- Apply Jinja `| default('fallback')` for safe defaults.

**Code:**
```jinja
# templates/drupal.test.conf.j2
<VirtualHost *:80>
  ServerName {{ domain }}.test
  DocumentRoot {{ drupal_core_path }}/web
  <Directory "{{ drupal_core_path }}/web">
    AllowOverride All
  </Directory>
</VirtualHost>
```
*Ref: ansible-for-devops.md — "Real-world playbook: Configure Apache"*

---

### Tags for Selective Playbook Runs

**Principle:** Tag a play or task; run only what you need with `--tags` or skip with `--skip-tags`.

**Code:**
```yaml
---
- hosts: webservers
  tags: deploy
  roles:
    - role: tomcat
      tags: ['tomcat', 'app']

  tasks:
    - name: Notify on completion.
      local_action:
        module: osx_say
        msg: "{{ inventory_hostname }} is finished!"
        voice: Zarvox
      tags:
        - notifications
        - say
```

```bash
ansible-playbook tags.yml --tags "tomcat,say"
ansible-playbook tags.yml --skip-tags "notifications"
```
*Ref: ansible-for-devops.md — "Tags"*

---

### Blocks for Conditional Grouping and Failure Handling

**Principle:** Group tasks under shared `when:`/`become:`; add `rescue:`/`always:` for exception-style flow.

**Code:**
```yaml
- hosts: web
  tasks:
    - block:
        - dnf: name=httpd state=present
        - template: src=httpd.conf.j2 dest=/etc/httpd/conf/httpd.conf
        - service: name=httpd state=started enabled=yes
      when: ansible_os_family == 'RedHat'
      become: yes

    - block:
        - apt: name=apache2 state=present
        - template: src=httpd.conf.j2 dest=/etc/apache2/apache2.conf
        - service: name=apache2 state=started enabled=yes
      when: ansible_os_family == 'Debian'
      become: yes

    - block:
        - name: Connect the app to monitoring.
          script: monitoring-connect.sh
      rescue:
        - debug: msg="There was an error in the block."
      always:
        - debug: msg="This always executes."
```
*Ref: ansible-for-devops.md — "Blocks"*

---

### Imports vs Includes (Static vs Dynamic)

**Principle:** `import_*` is static (resolved before play starts); `include_*` is dynamic (resolved at runtime).

**Code:**
```yaml
# import_tasks = static (cannot use runtime variables in file names)
- import_tasks: tasks/drush.yml

# include_tasks = dynamic
- name: Check if extra_tasks.yml is present.
  stat:
    path: tasks/extra-tasks.yml
  register: extra_tasks_file
  connection: local

- include_tasks: tasks/extra-tasks.yml
  when: extra_tasks_file.stat.exists
```
*Ref: ansible-for-devops.md — "Imports" / "Includes" / "Dynamic includes"*

---

### Roles: Directory Conventions and Defaults

**Principle:** A role is a directory with `meta/`, `tasks/`, `handlers/`, `defaults/`, `vars/`, `files/`, `templates/`. Use defaults for overridable values, vars for fixed ones.

**Code:**
```text
role_name/
  defaults/     # default variables (lowest precedence, easy to override)
  files/        # static files to copy
  handlers/     # handler tasks
  meta/         # role metadata and dependencies
  tasks/        # main task list
  templates/    # Jinja2 templates
  vars/         # role variables (higher precedence)
```

```yaml
# tasks/main.yml
- name: Install Node.js (npm plus all its dependencies).
  dnf: name=npm state=present enablerepo=epel

- name: Install npm modules required by our app.
  npm: name={{ item }} global=yes state=present
  with_items: "{{ node_npm_modules }}"
```

```yaml
# defaults/main.yml — overridable defaults
node_npm_modules:
  - forever
```
*Ref: ansible-for-devops.md — "Roles" / "Role scaffolding"*

---

### Cross-Platform Roles via `include_vars` by OS

**Principle:** Use `include_vars: "{{ ansible_os_family }}.yml"` and `include_tasks: setup-{{ ansible_os_family }}.yml` to ship one role that works across distros.

**Code:**
```yaml
---
- name: Include OS-specific variables.
  include_vars: "{{ ansible_os_family }}.yml"

- name: Include OS-specific setup tasks.
  include_tasks: setup-{{ ansible_os_family }}.yml
```
*Ref: ansible-for-devops.md — "Organizing more complex and cross-platform roles"*

---

### Ansible Galaxy: Roles in Nine Lines

**Principle:** A LAMP or Solr server is `geerlingguy.nginx` + a variables file. Use Galaxy to skip the boilerplate; pin versions.

**Code:**
```yaml
---
- hosts: all
  become: yes

  roles:
    - geerlingguy.mysql
    - geerlingguy.apache
    - geerlingguy.php
    - geerlingguy.php-mysql
```

```yaml
# requirements.yml
---
roles:
  - name: geerlingguy.firewall
  - name: geerlingguy.php
    version: 4.3.1
  - src: https://github.com/geerlingguy/ansible-role-passenger
    name: passenger
    version: 2.0.0
```

```bash
ansible-galaxy install -r requirements.yml
ansible-galaxy role init my_role
ansible-galaxy role list
```
*Ref: ansible-for-devops.md — "Ansible Galaxy" / "A LAMP server in nine lines of YAML"*

---

### Dynamic Inventories for Ephemeral Cloud

**Principle:** Discover instances with `aws_ec2.yml`, `gcp.yml`, etc., so the inventory is always the source of truth.

**Code:**
```yaml
# Use AWS dynamic inventory via amazon.aws.aws_ec2 plugin
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
keyed_groups:
  - key: tags.Environment
    prefix: env
  - key: tags.Role
groups:
  webservers: "'web' in tags.Role"
```
*Ref: ansible-for-devops.md — "Dynamic inventory" / "Ephemeral infrastructure"*

---

### Provisioning EC2 with Ansible

**Principle:** Use the `amazon.aws.ec2` module; then immediately hand off to a playbook over SSH once provisioned.

**Code:**
```yaml
- name: Launch EC2 instance
  amazon.aws.ec2:
    key_name: my-key
    instance_type: t3.micro
    image: ami-12345678
    region: us-east-1
    group: webserver
    count: 3
```

*Ref: ansible-for-devops.md — "AWS EC2 Provisioning"*

---

### Vault for Encrypted Secrets

**Principle:** Encrypt secrets at rest in version control; decrypt at run time.

**Code:**
```bash
ansible-vault create secrets.yml
ansible-vault edit secrets.yml
ansible-playbook site.yml --ask-vault-pass

# Or use a vault password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

```yaml
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  306236613261...encrypted ciphertext...
```
*Ref: ansible-for-devops.md — "Ansible Vault - Keeping secrets secret"*

---

### Idempotency Tests in Molecule

**Principle:** A playbook should produce zero changes on its second run. Use Molecule + Docker to assert that.

**Code:**
```yaml
# molecule/default/converge.yml
---
- name: Converge
  hosts: all
  roles:
    - role: my_role

# molecule/default/verify.yml
---
- name: Verify
  hosts: all
  tasks:
    - name: Check that the service is running
      service:
        name: myapp
        state: started
      register: result
    - assert:
        that:
          - result.state is defined
          - result.state.running == true
```
*Ref: ansible-for-devops.md — "Chapter 13: Automated testing with Molecule"*

---

### Linting and Syntax Checking

**Principle:** Lint before you commit; verify the rendered YAML is valid YAML; confirm idempotency in check mode before production runs.

**Code:**
```bash
yamllint playbook.yml
ansible-lint playbook.yml
ansible-playbook --syntax-check playbook.yml
ansible-playbook --check playbook.yml        # dry-run
ansible-playbook --diff playbook.yml         # show changes
```
*Ref: ansible-for-devops.md — "Linting YAML with yamllint" / "Performing a --syntax-check"*

---

### Debug, Fail, Assert

**Principle:** Use `debug` to investigate, `assert` to gate, `fail` to halt on a custom check.

**Code:**
```yaml
- name: Print the current system date.
  debug:
    var: date.stdout

- name: Assert that the service is running
  assert:
    that:
      - "'running' in result.state"

- name: Fail explicitly when something is wrong
  fail:
    msg: "Database is not reachable"
  when: not db_reachable
```
*Ref: ansible-for-devops.md — "Debugging and Asserting"*

---

### Local Provisioning with `--connection=local`

**Principle:** Use `connection: local` for self-provisioning and `ansible-pull` for agent-like behavior; use `--connection=local` to skip SSH overhead.

**Code:**
```yaml
---
- hosts: 127.0.0.1
  gather_facts: no

  tasks:
    - name: Check the current system date.
      command: date
      register: date

    - name: Print the current system date.
      debug:
        var: date.stdout
```

```bash
ansible-playbook test.yml --connection=local
```
*Ref: ansible-for-devops.md — "Running an entire playbook locally"*

---

### Solr + Java — `get_url` + `unarchive` + `creates`

**Principle:** Verify downloaded artifacts with `checksum`; use the `creates:` parameter on shell commands for idempotence.

**Code:**
```yaml
vars:
  download_dir: /tmp
  solr_version: 8.6.0
  solr_checksum: "sha512:6b0d61..."

tasks:
  - name: Download Solr.
    get_url:
      url: "https://archive.apache.org/dist/lucene/solr/{{ solr_version }}/solr-{{ solr_version }}.tgz"
      dest: "{{ download_dir }}/solr-{{ solr_version }}.tgz"
      checksum: "{{ solr_checksum }}"

  - name: Expand Solr.
    unarchive:
      src: "{{ download_dir }}/solr-{{ solr_version }}.tgz"
      dest: "{{ download_dir }}"
      remote_src: true
      creates: "{{ download_dir }}/solr-{{ solr_version }}/README.txt"

  - name: Run Solr installation script.
    command: >
      {{ download_dir }}/solr-{{ solr_version }}/bin/install_solr_service.sh
      {{ download_dir }}/solr-{{ solr_version }}.tgz
      -i /opt -d /var/solr -u solr -s solr -p 8983
      creates={{ solr_dir }}/bin/solr
```
*Ref: ansible-for-devops.md — "Real-world playbook: Solr"*

---

### Docker Containers with Ansible

**Principle:** Use `community.docker.docker_image` and `community.docker.docker_container` for declarative container management.

**Code:**
```yaml
- name: Build Docker image
  community.docker.docker_image:
    build:
      path: /path/to/app
    name: myapp
    tag: latest
    source: build

- name: Run a container
  community.docker.docker_container:
    name: myapp
    image: myapp:latest
    state: started
    published_ports: "80:80"
```
*Ref: ansible-for-devops.md — "Using Ansible to build and manage containers"*

---

### Firewalld with `firewalld` Module

**Principle:** Use the `firewalld` module for zone-based firewall management; pair with MySQL ACLs for layered access.

**Code:**
```bash
ansible db -b -m firewalld -a "zone=database state=present permanent=yes"
ansible db -b -m firewalld -a "source=192.168.56.0/24 zone=database state=enabled permanent=yes"
ansible db -b -m firewalld -a "port=3306/tcp zone=database state=enabled permanent=yes"
```
*Ref: ansible-for-devops.md — "Configure the Database servers"*

---

### Multi-Tier Deployment with `serial`

**Principle:** Roll out changes tier by tier; cap failures with `max_fail_percentage`.

**Code:**
```yaml
- hosts: dbservers
  tasks: [database migration tasks]
- hosts: appservers
  serial: 1   # one at a time
  tasks: [app deployment tasks]
- hosts: webservers
  serial: 5   # five at a time
  tasks: [web server tasks]
```
*Ref: ansible-for-devops.md — Summary / Deployment chapter*

---

### SSH Hardening with the `lineinfile` Module

**Principle:** Use `lineinfile` for surgical edits to `/etc/ssh/sshd_config`; restart the service via `notify`.

**Code:**
```yaml
- name: Disable SSH password authentication.
  lineinfile:
    dest: /etc/ssh/sshd_config
    regexp: "^#?PasswordAuthentication"
    line: "PasswordAuthentication no"
    state: present
  notify: restart sshd

- name: Disable root login.
  lineinfile:
    dest: /etc/ssh/sshd_config
    regexp: "^#?PermitRootLogin"
    line: "PermitRootLogin no"
    state: present
  notify: restart sshd
```
*Ref: ansible-for-devops.md — "Chapter 11 - Server Security and Ansible"*

---

### Docker Compose and Ansible

**Principle:** Use the `community.docker.docker_compose` module to declaratively apply a Compose stack.

**Code:**
```yaml
- name: Apply Docker Compose stack
  community.docker.docker_compose:
    project_src: /opt/myapp
    state: present
```
*Ref: ansible-for-devops.md — "Container orchestration"*

---

### ELK Logging with Filebeat

**Principle:** Use Ansible to deploy Filebeat (or Logstash) configs that forward local logs to a central ELK stack.

**Code:**
```yaml
- name: Install Filebeat.
  apt: name=filebeat state=present

- name: Configure Filebeat to forward logs.
  template:
    src: filebeat.yml.j2
    dest: /etc/filebeat/filebeat.yml
  notify: restart filebeat
```
*Ref: ansible-for-devops.md — "ELK Logging with Ansible"*

---

### Inventory Tuning for Production Playbooks

**Principle:** Use `forks` to control parallelism; pin to ~5 forks on a typical connection.

**Code:**
```ini
# ansible.cfg
[defaults]
inventory = hosts.ini
forks = 10
roles_path = ./roles
host_key_checking = False
```

```bash
ansible-playbook -i hosts.ini --forks 25 site.yml
```
*Ref: ansible-for-devops.md — Appendix B / Best Practices*

---

## Anti-Patterns & Common Mistakes

- **Ansible shell scripts replacing state:** hand-rolled idempotence → *fix:* use the `ansible.builtin.command`/`shell` modules with `creates:`/`removes:` or reframe as a module call.
- **Hard-coding `gather_facts: true` everywhere:** wasted time on hosts with no usable facts → *fix:* set `gather_facts: no` per play when you don't need them.
- **Inline `--extra-vars` for everything:** chaos → *fix:* put values in `group_vars`, `host_vars`, or role defaults.
- **`ignore_errors: yes` everywhere:** silencing real problems → *fix:* use `failed_when` with a precise condition instead.
- **Mixing `import_tasks` and runtime-variable file names:** static import won't expand Jinja → *fix:* use `include_tasks` for dynamic include.
- **`hosts: all` with no limits:** blast radius = everything → *fix:* restrict with `--limit`, group tags, or per-play hosts.
- **Ansible-Vault password checked into the repo:** unencrypted secrets are worse than none → *fix:* use a vault password file in CI, never commit it.
- **Galaxy roles without a pinned version:** "the latest" breaks unpredictably → *fix:* pin to a specific `version:` in requirements.yml.
- **Non-idempotent `command:` without `creates:`/`changed_when`:** re-runs report "changed" every time → *fix:* wrap with `creates:` or write a custom check.
- **`become: yes` everywhere:** privilege creep → *fix:* scope `become` to specific tasks or roles only.
- **`delegate_to: 127.0.0.1` confusion with `connection: local`:** different semantics → *fix:* `delegate_to: 127.0.0.1` runs once per host with localhost as executor; `connection: local` runs the entire play locally.

## Decision Heuristics / Checklists

- *Module or shell?* Module if available; otherwise `command` then `shell`; rarely `script`; never `raw`.
- *dynamic vs static include?* Dynamic (`include_*`) if file name depends on runtime facts; static (`import_*`) otherwise.
- *When to introduce roles?* When tasks > ~50 lines or appear in 2+ playbooks.
- *Defaults vs vars?* Defaults for overridable knobs; vars for internals.
- *Vault strategy?* One vault per environment; decrypt at run time; never commit the vault password file.
- *Molecule or hand-roll?* Molecule for roles with ≥ 5 tasks and any platform variation.
- *--check before --diff?* Always; combine with `--diff` to surface behavioral changes.
- *Galaxy or fork?* Galaxy first; fork only if the upstream role doesn't fit.
- *Cross-platform roles?* `include_vars: "{{ ansible_os_family }}.yml"` + per-OS task files.
- *Limit to a single host?* `--limit "*.4"` or `--limit ~".*\.4"` (regex prefix `~`).
- *Tags vs roles?* Tags for selective execution within a play; roles for grouping concerns.

## Key Takeaways

1. **Ansible is agentless, declarative, and idempotent.** Push changes via SSH; declare end state, not procedure.
2. **Idempotence is the discipline.** Every task should produce zero changes on the second run.
3. **Roles are the unit of reuse.** Default values live in `defaults/`, internals in `vars/`.
4. **Variables are everywhere; precedence governs.** More specific wins; defaults beat role vars; CLI extras win all.
5. **Jinja2 + YAML = the Ansible expression engine.** Quote Jinja strings that begin with `{`.
6. **Use Galaxy roles for boilerplate; pin versions.** Trust the community; verify the supply chain.
7. **Vault for secrets, never plaintext.** Vault id, prompts, or password file — but not raw variables.
8. **Test with Molecule.** Idempotency is the most important test.
9. **Debug with `debug`, `assert`, `fail`, `--check`, `--diff`.** Make non-determinism visible.
10. **Reusable patterns: pre_tasks, roles, vars_files, handlers, tags, blocks.** Compose them to manage thousands of hosts.

## Cross-References

- Related: [[../Terraform_at_Scale.md]] — Terraform and Ansible compete for config-management duties. Pick one as the source of truth per environment.
- Related: [[../Ultimate_AWS_CDK.md]] — CDK manages the resource graph; Ansible configures the OS and software inside the resulting EC2 instances.
- Related: [[../ansible_for_kubernetes.md]] — The Kubernetes companion book covers `k8s`/`helm` modules for managing workloads declaratively.
- Topic index: [[../INDEX.md]]
