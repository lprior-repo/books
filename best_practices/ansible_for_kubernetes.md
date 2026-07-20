# Ansible for Kubernetes

**Author:** Jeff Geerling
**Topic tags:** `#devops` `#cli` `#architecture`
**Language focus:** Ansible YAML / Kubernetes YAML / Helm / Go (operators)
**Sources:** `markdown_output/ansible-for-kubernetes/ansible-for-kubernetes.md` · `summaries/ansible-for-kubernetes.md`

## TL;DR

Ansible is the configuration glue between infrastructure (provisioning, secrets, DNS, ELBs) and Kubernetes workloads (manifests, Helm releases, RBAC, operators). This book walks from "Hello World in a Docker container" through cluster bootstrapping (Vagrant, Kubespray), cloud-managed clusters (EKS, GKE), in-cluster testing (Molecule + Kind), and Ansible-based operators. Use it when you need one tool to manage the cluster AND the things inside it.

---

## Best Practices by Topic

### Containers First, Kubernetes Second

**Principle:** Containerize first; Kubernetes is the runtime that makes containers resilient and declarative.

**Do:**
- Use multi-stage Docker builds to keep runtime images small.
- Log to stdout/stderr — Kubernetes routes them centrally.
- Distinguish between build-time tooling and runtime artifacts.

**Don't:**
- Ship a 300 MB Go toolchain in your deployment image.

**Code:**
```dockerfile
# Multi-stage build keeps the runtime image tiny.
FROM golang:1-alpine AS build
WORKDIR /app
COPY cmd cmd
RUN go build cmd/hello/hello.go

FROM alpine:latest
WORKDIR /app
COPY --from=build /app/hello /app/hello
EXPOSE 8180
ENTRYPOINT ["./hello"]
```
*Ref: ansible-for-kubernetes.md — "Deploying Hello Go in a container"*

---

### Hello Go App — The Smallest Useful K8s Workload

**Principle:** Start with a stateless, stdout-logging app so the Kubernetes deployment surface area is small.

**Code:**
```go
// cmd/hello/hello.go
package main

import (
  "fmt"
  "log"
  "net/http"
)

func HelloServer(w http.ResponseWriter, r *http.Request) {
  fmt.Fprintf(w, "Hello, you requested: %s", r.URL.Path)
  log.Printf("Received request for path: %s", r.URL.Path)
}

func main() {
  addr := ":8180"
  handler := http.HandlerFunc(HelloServer)
  if err := http.ListenAndServe(addr, handler); err != nil {
    log.Fatalf("Could not listen on port %s %v", addr, err)
  }
}
```

```bash
go build cmd/hello/hello.go
./hello
# Then later
kubectl create deployment hello-go --image=hello-go
kubectl expose deployment hello-go --type=LoadBalancer --port=8180
```
*Ref: ansible-for-kubernetes.md — Chapter 1*

---

### Why Ansible for Kubernetes?

**Principle:** Ansible is the integration layer that runs above and around Kubernetes — provisioning VMs/cloud resources, configuring OS-level concerns, deploying manifest sets, and orchestrating operators.

**Use Ansible for:**
- Provisioning clusters (EKS, GKE, Kubespray).
- Composing multi-document manifest sets with templating.
- Bootstrapping secrets (Vault) before a manifest depends on them.
- DNS, ELB/NLB provisioning alongside a `LoadBalancer` Service.
- Operator lifecycle hooks in YAML rather than Go.

**Don't:**
- Use Ansible to manage individual Pod replicas — that's what the Deployment controller is for.
- Hand-edit resources via `kubectl edit` in production — automate everything.

*Ref: ansible-for-kubernetes.md — Introduction*

---

### Building Docker Images via Ansible

**Principle:** Use the `community.docker.docker_image` module with `source: build` for declarative image builds; `present` is idempotent.

**Code:**
```yaml
- name: Build Docker image
  community.docker.docker_image:
    build:
      path: /path/to/app
    name: myapp
    tag: latest
    source: build
```
*Ref: ansible-for-kubernetes.md — Chapter 3*

---

### Minikube for Local K8s Learning

**Principle:** Minikube runs a single-node K8s in a VM — perfect for iterating before provisioning cloud infrastructure.

**Code:**
```bash
brew install minikube         # macOS
choco install minikube        # Windows
minikube start --cpus 4 --memory 4g
eval $(minikube docker-env)   # point docker CLI at minikube
docker build -t hello-go .
kubectl create deployment hello-go --image=hello-go
kubectl expose deployment hello-go --type=LoadBalancer --port=8180
minikube service hello-go
```
*Ref: ansible-for-kubernetes.md — "Installing Minikube"*

---

### Deploying with `kubectl edit` is Snowflake Management

**Principle:** Hand-editing clusters is fine in development; equivalent to manual configuration in production.

**Do:**
- Set `imagePullPolicy: IfNotPresent` in dev (use Always in prod where images are tagged immutably).
- Move all manual changes into Ansible-managed manifests as soon as you know what you want.

**Code:**
```yaml
# After kubectl edit deployment hello-go → spec.template.spec.containers.0.imagePullPolicy
spec:
  containers:
    - image: hello-go
      imagePullPolicy: IfNotPresent
      name: hello-go
```
*Ref: ansible-for-kubernetes.md — "Running Hello Go in Minikube"*

---

### Building a K8s Cluster with Ansible + Vagrant

**Principle:** Locally, use Vagrant to provision a multi-VM "cluster", then drive kubeadm, kubelet, kubectl, and a CNI via Ansible roles.

**Code:**
```ruby
# Vagrantfile — multi-VM cluster
Vagrant.configure("2") do |config|
  config.vm.box = "geerlingguy/rockylinux8"

  config.vm.define "master" do |m|
    m.vm.hostname = "master.test"
    m.vm.network "private_network", ip: "192.168.56.10"
  end

  config.vm.define "worker1" do |w|
    w.vm.hostname = "worker1.test"
    w.vm.network "private_network", ip: "192.168.56.11"
  end

  config.vm.define "worker2" do |w|
    w.vm.hostname = "worker2.test"
    w.vm.network "private_network", ip: "192.168.56.12"
  end
end
```
*Ref: ansible-for-kubernetes.md — Chapter 4*

---

### Kubespray for Production Cluster Bootstrapping

**Principle:** Don't hand-roll kubeadm + CNI + Ingress + Kubernetes add-ons; use Kubespray's battle-tested Ansible playbooks.

**Do:**
- Use Kubespray for AWS/GCP/Azure/bare metal/Raspberry Pi.
- Pin Kubernetes version.
- Run from a dedicated control node with SSH access to the cluster members.

*Ref: ansible-for-kubernetes.md — "Building a cluster using Kubespray"*

---

### EKS: CloudFormation for Infra, Ansible for Glue

**Principle:** Use CloudFormation for VPC + EKS + Node Group resources, then Ansible to wire up kubeconfig, kube-context, and application deploys.

**Code (CloudFormation: EKS Cluster role + cluster):**
```yaml
---
AWSTemplateFormatVersion: "2010-09-09"
Description: "EKS Cluster definition."

Parameters:
  VpcId:
    Type: String
  Subnets:
    Type: CommaDelimitedList
  ClusterName:
    Type: String
  KubernetesVersion:
    Type: String

Resources:
  ClusterRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: { Service: [eks.amazonaws.com] }
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
        - arn:aws:iam::aws:policy/AmazonEKSServicePolicy

  ClusterControlPlaneSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Cluster communication with worker nodes.
      VpcId: !Ref VpcId

  Cluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: !Ref ClusterName
      Version: !Ref KubernetesVersion
      RoleArn: !GetAtt ClusterRole.Arn
      ResourcesVpcConfig:
        SecurityGroupIds: [!Ref ClusterControlPlaneSecurityGroup]
        SubnetIds: !Ref Subnets

Outputs:
  ClusterName:    { Value: !Ref ClusterName,   Export: { Name: { "Fn::Sub": "${AWS::StackName}-ClusterName"    } } }
  ClusterEndpoint:{ Value: !GetAtt Cluster.Endpoint, Export: { Name: { "Fn::Sub": "${AWS::StackName}-ClusterEndpoint" } } }
```
*Ref: ansible-for-kubernetes.md — Chapter 5*

---

### Applying CloudFormation Stacks via Ansible

**Principle:** Drive CloudFormation through the `amazon.aws.cloudformation` module; chain stacks via stack outputs.

**Code:**
```yaml
- name: Ensure VPC exists via CloudFormation.
  amazon.aws.cloudformation:
    stack_name: eks-example-vpc
    state: present
    region: "{{ aws_region }}"
    profile: "{{ aws_profile }}"
    disable_rollback: false
    template: cloudformation/vpc.yml
    template_parameters:
      Region: "{{ aws_region }}"
    tags:
      stack: eks-example-vpc
      application: eks-example
  register: vpc_info

- name: Add to stack_outputs.
  set_fact:
    stack_outputs: "{{ stack_outputs | combine(vpc_info['stack_outputs']) }}"

- name: Ensure EKS Cluster exists via CloudFormation.
  amazon.aws.cloudformation:
    stack_name: eks-example-cluster
    state: present
    region: "{{ aws_region }}"
    template: cloudformation/eks-cluster.yml
    template_parameters:
      ClusterName:       "{{ eks_cluster_name }}"
      KubernetesVersion: "{{ eks_kubernetes_version }}"
      Subnets:           "{{ stack_outputs.Subnets }}"
      VpcId:             "{{ stack_outputs.VpcId }}"
  register: eks_cluster_info
```
*Ref: ansible-for-kubernetes.md — "Applying CloudFormation Templates with Ansible"*

---

### Authenticating to EKS via kubeconfig

**Principle:** Use `aws eks update-kubeconfig` to generate a kubeconfig, then point Ansible and kubectl at it via `KUBECONFIG`.

**Code:**
```bash
aws eks --region us-east-1 update-kubeconfig --name eks-example \
       --kubeconfig ~/.kube/eks-example
export KUBECONFIG=~/.kube/eks-example
kubectl get svc
```
*Ref: ansible-for-kubernetes.md — "Authenticating to the EKS Cluster via kubeconfig"*

---

### WordPress on EKS — Multi-Document Manifest Sets

**Principle:** Compose a multi-document manifest file; deploy with `k8s` + `lookup('template', file) | from_yaml_all | list`.

**Code (headless MySQL service + WordPress deployment):**
```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: mysql-pass
  namespace: default
  labels: { app: wordpress }
data:
  password: "{{ wordpress_mysql_password | b64encode }}"
---
apiVersion: v1
kind: Service
metadata:
  name: wordpress-mysql
  namespace: default
  labels: { app: wordpress }
spec:
  ports: [{ port: 3306 }]
  selector: { app: wordpress, tier: mysql }
  clusterIP: None                # headless service: DNS to the pod directly
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  accessModes: [ReadWriteOnce]
  resources: { requests: { storage: 20Gi } }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress-mysql
  namespace: default
  labels: { app: wordpress, tier: mysql }
spec:
  selector: { matchLabels: { app: wordpress, tier: mysql } }
  strategy: { type: Recreate }
  template:
    metadata: { labels: { app: wordpress, tier: mysql } }
    spec:
      containers:
        - name: mysql
          image: mysql:5.6
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom: { secretKeyRef: { name: mysql-pass, key: password } }
          ports: [{ containerPort: 3306, name: mysql }]
          volumeMounts:
            - name: mysql-persistent-storage
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-persistent-storage
          persistentVolumeClaim: { claimName: mysql-pv-claim }
```
*Ref: ansible-for-kubernetes.md — "Build the WordPress Kubernetes manifests"*

---

### Deploying Manifests via `k8s` Module

**Principle:** Use `kubernetes.core.k8s` (or `k8s` collection) with `state: present` for declarative, idempotent manifest application.

**Code:**
```yaml
- name: Deploy WordPress secrets.
  kubernetes.core.k8s:
    definition: "{{ item }}"
    kubeconfig: "{{ k8s_kubeconfig }}"
    state: present
  loop: "{{ lookup('template', 'wordpress/mysql-pass.yml') | from_yaml_all | list }}"
  no_log: true

- name: Deploy MySQL and WordPress.
  kubernetes.core.k8s:
    definition: "{{ item }}"
    kubeconfig: "{{ k8s_kubeconfig }}"
    state: present
  loop:
    - "{{ lookup('template', 'wordpress/mysql.yml')      | from_yaml_all | list }}"
    - "{{ lookup('template', 'wordpress/wordpress.yml') | from_yaml_all | list }}"
```
*Ref: ansible-for-kubernetes.md — "Build an Ansible Playbook to deploy the manifests to EKS"*

---

### Wiring Up DNS + Waiting for ELB

**Principle:** Combine `k8s_info` (read-only) with `uri` (poll), then `ec2_elb_info` and `route53` (write).

**Code:**
```yaml
- name: Get load balancer DNS name.
  kubernetes.core.k8s_info:
    kubeconfig: "{{ k8s_kubeconfig }}"
    kind: Service
    name: wordpress
    namespace: default
  register: wordpress_svc

- name: Set the load balancer URL as a fact.
  set_fact:
    wordpress_lb_host: "{{ wordpress_svc['resources'][0]['status']['loadBalancer']['ingress'][0]['hostname'] }}"
  when: aws_environment | bool

- name: Wait for Load Balancer to respond.
  ansible.builtin.uri:
    url: "http://{{ wordpress_lb_host }}"
  register: lb_result
  until: lb_result.status == 200
  retries: 60
  delay: 5
  when: aws_environment | bool

- name: Get ELB info.
  amazon.aws.ec2_elb_info:
    region: "{{ aws_region }}"
    profile: "{{ aws_profile }}"
    names: "{{ wordpress_lb_host.split('-')[0] }}"
  register: elb_info
  when: aws_environment | bool

- name: Add an A record in Route53.
  amazon.aws.route53:
    profile: "{{ aws_profile }}"
    zone: "{{ wordpress_route53_zone }}"
    record: "{{ wordpress_route53_domain }}"
    state: present
    type: A
    ttl: 300
    value: "{{ wordpress_lb_host }}."
    alias: true
    alias_hosted_zone_id: "{{ elb_info['elbs'][0]['canonical_hosted_zone_name_id'] }}"
    wait: true
  when:
    - aws_environment | bool
    - wordpress_route53_zone != ''
    - wordpress_route53_domain != ''
```
*Ref: ansible-for-kubernetes.md — "Point a custom domain at the WordPress ELB"*

---

### GKE with Terraform and Ansible

**Principle:** Terraform for Google-side GKE provisioning; Ansible for application lifecycle.

**Tool boundary:**
- Terraform `google_container_cluster` resource creates the cluster.
- Ansible `k8s` module deploys manifests once kubeconfig is written.
- The book leaves GKE for a future chapter — combine the book's EKS + GKE guidance.

*Ref: ansible-for-kubernetes.md — Chapter 6*

---

### CI Testing with Molecule + Kind

**Principle:** Reproduce a Kubernetes test environment in CI with Molecule's `delegated` driver, spinning up a Kind cluster via a `create.yml` and tearing it down with `destroy.yml`.

**Code (Molecule scenario):**
```yaml
---
driver:
  name: delegated
lint: |
  set -e
  yamllint .
  ansible-lint
platforms:
  - name: molecule-test
provisioner:
  name: ansible
  inventory:
    host_vars:
      localhost:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        kubeconfig: "{{ lookup('env', 'KUBECONFIG') }}"
  env:
    KUBECONFIG:         ~/.kube/config-molecule-test
    K8S_AUTH_KUBECONFIG: ~/.kube/config-molecule-test
```

```yaml
# molecule/default/create.yml
---
- name: Create
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Build a kind cluster (wait for control plane).
      ansible.builtin.command: >-
        kind create cluster
        --wait 300s
        --name molecule-test
        --kubeconfig {{ kubeconfig }}
      changed_when: true
```

```yaml
# molecule/default/destroy.yml
---
- name: Destroy
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Delete the kind cluster.
      ansible.builtin.command: >-
        kind delete cluster
        --name molecule-test
        --kubeconfig {{ kubeconfig }}
      changed_when: false
```

```yaml
# molecule/default/converge.yml
---
- name: Converge
  hosts: localhost
  connection: local
  gather_facts: false
  - import_playbook: ../../main.yml
```

```yaml
# molecule/default/verify.yml
---
- name: Verify
  hosts: localhost
  connection: local
  gather_facts: true
  tasks:
    - name: Get 'hello' Job info.
      kubernetes.core.k8s_info:
        kind: Job
        name: hello
        namespace: default
      register: jobs
    - name: Assert that 'hello' Job ran successfully.
      ansible.builtin.assert:
        that: jobs['resources'][0]['status']['succeeded'] == 1
```
*Ref: ansible-for-kubernetes.md — Chapter 7*

---

### Core Ansible Kubernetes Modules

**Principle:** The `kubernetes.core` collection ships modules for every Kubernetes verb — use them; don't write `command: kubectl` shims.

**Modules:**
- `k8s` — create/update/delete any resource (drives manifests)
- `k8s_info` — query existing resources (used for facts)
- `k8s_scale` — scale deployments/replicas
- `k8s_exec` — run commands in a Pod
- `k8s_log` — fetch container logs
- `k8s_service` — manage Services
- `k8s_inventory` — build inventory from K8s resources
- `helm` / `helm_info` / `helm_repository` — manage Helm releases
- `geerlingguy.k8s` collection — common opinionated roles

*Ref: ansible-for-kubernetes.md — Chapter 8*

---

### Operators in YAML, Not Go

**Principle:** The Operator Pattern codifies human operational knowledge into software; Ansible lets you write Operators in YAML instead of compiling Go against the Operator SDK.

**Trade-offs:**
- Go Operators: faster, smaller, type-safe, deeply integrated with `controller-runtime`.
- Ansible Operators: easier authoring, larger footprint, slower reconciliation, fewer CRDs to learn.

**Do:**
- Choose Ansible-based Operators for simple lifecycle (install/configure/upgrade) and human-familiar logic.
- Choose Go Operators when you need tight control loops, mutating webhooks, or complex state reconciliation.

*Ref: ansible-for-kubernetes.md — Chapter 9 "Hello Operator"*

---

### End-to-End Operator Testing with Molecule + Kind

**Principle:** Treat an Operator like any other Ansible role — `molecule test` with a Kind cluster is the unit of truth.

**Do:**
- Provide a CR sample in `molecule/default/`.
- Verify reconciliation produces expected Kubernetes resources via `k8s_info`.
- Run `molecule test` in CI on every PR.

*Ref: ansible-for-kubernetes.md — "End-to-end testing for an Ansible-based Operator with Molecule"*

---

### Vault and Secret Management

**Principle:** Store Kubernetes secrets in YAML-backed by Ansible Vault or HashiCorp Vault — never in plaintext `vars.yml` files.

**Do:**
- Use `no_log: true` on any task that handles a Secret.
- Pipe secrets via `Secret.fromSecretNameV2()` or your secret manager, then reference them in Kubernetes manifests.

**Don't:**
- Hardcode database passwords in `vars/main.yml` (the book does this only for the example; production must use Vault).

*Ref: ansible-for-kubernetes.md — "wordpress_mysql_password" sidebar*

---

### Debugging Cluster Networking Issues

**Principle:** When a Pod fails to network, debug in a deterministic order: `kubectl describe` → `kubectl logs` → `kubectl exec` → check CNI.

**Common fixes (the book documents these specifically):**
- Flannel + nftables → switch to `iptables-legacy`
- Wrong network interface → patch Flannel with the right `--iface` or `--ip-masq`

**Code:**
```yaml
# Patch Flannel to use the right network interface
- name: Patch Flannel to use ens5
  ansible.builtin.command: >-
    kubectl -n kube-flannel patch daemonset/kube-flannel-ds
    --type=json
    -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--iface=ens5"}]'
```
*Ref: ansible-for-kubernetes.md — "Debugging cluster networking issues"*

---

### Helm Integration via Ansible

**Principle:** Install/upgrade Helm charts declaratively via the `kubernetes.core.helm` module — same `state: present` discipline as the `k8s` module.

**Code:**
```yaml
- name: Install nginx-ingress via Helm
  kubernetes.core.helm:
    name: nginx-ingress
    chart_ref: ingress-nginx/ingress-nginx
    chart_version: "4.10.1"
    release_namespace: ingress
    create_namespace: true
    values:
      controller:
        replicaCount: 2
        service:
          type: LoadBalancer
```
*Ref: ansible-for-kubernetes.md — "Helm integration"*

---

### NetworkPolicy for Tenant Isolation

**Principle:** Default-deny is the safe policy; explicitly allow only what is required.

**Code:**
```yaml
- name: Apply default-deny + explicit allow list
  kubernetes.core.k8s:
    definition:
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
        name: default-deny
        namespace: app
      spec:
        podSelector: {}
        policyTypes: [Ingress, Egress]
        ingress:
          - from:
              - namespaceSelector: { matchLabels: { name: ingress } }
            ports:
              - port: 80
        egress:
          - to:
              - namespaceSelector: { matchLabels: { name: db } }
            ports:
              - port: 5432
```
*Ref: ansible-for-kubernetes.md — Summary / multi-stack guidance*

---

### RBAC Scoped to Each Component

**Principle:** Use Kubernetes RBAC (ServiceAccount + RoleBinding) so each Pod's identity has the minimum cluster scope it needs.

**Code:**
```yaml
- name: Create a ServiceAccount for the app
  kubernetes.core.k8s:
    definition:
      apiVersion: v1
      kind: ServiceAccount
      metadata: { name: app-sa, namespace: app }

- name: Bind app-sa to a role that lets it read its own ConfigMap
  kubernetes.core.k8s:
    definition:
      apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata: { name: app-read-config, namespace: app }
      subjects:
        - kind: ServiceAccount
          name: app-sa
          namespace: app
      roleRef:
        kind: Role
        name: app-read-config
        apiGroup: rbac.authorization.k8s.io
```
*Ref: ansible-for-kubernetes.md — RBAC patterns*

---

### IPv4/IPv6 and Pod Networking

**Principle:** Use CNI plugins that match your network requirements (Calico for policy, Cilium for eBPF, Flannel for simplicity).

**Do:**
- Pair Calico/Cilium with NetworkPolicy for enforcement.
- Document the CNI choice and version in `group_vars/`.

**Don't:**
- Mix two CNIs on the same cluster — they will fight over pod CIDRs.

*Ref: ansible-for-kubernetes.md — Chapter 4 / CNI discussion*

---

### Production Deployments: Multi-Cluster GitOps

**Principle:** Treat clusters as cattle; treat each manifest set as the source of truth driven by Ansible.

**Reference pattern:**
1. `ansible` provisions cluster infra (cloud or Kubespray).
2. `ansible` deploys CoreDNS + CNI + addons (e.g. metrics-server, ingress-nginx).
3. `ansible` applies application manifests via `k8s`/`helm`.
4. Molecule + Kind test the manifests in CI before they reach production.

*Ref: ansible-for-kubernetes.md — Synthesis*

---

### Ansible from a Kubernetes Container

**Principle:** Run Ansible inside a Kubernetes Job/CronJob to reconcile cluster state — this is the Ansible Operator pattern.

**Do:**
- Use `kubernetes.core.k8s_exec` to drive one-off jobs from a controller.
- Pin the Ansible version in the container image.

**Don't:**
- Run a long-lived Ansible control plane inside a Pod without explicit restart/crash policies.

*Ref: ansible-for-kubernetes.md — Operator section*

---

## Anti-Patterns & Common Mistakes

- **`kubectl edit` in production:** snowflake management → *fix:* put the change in a manifest and apply via Ansible.
- **Plaintext secrets in `vars/main.yml`:** leaked in logs → *fix:* Ansible Vault, HashiCorp Vault, or sealed-secrets; always `no_log: true`.
- **Mixing two CNIs:** pod CIDR conflicts → *fix:* choose one CNI for the cluster's lifetime.
- **Manual image build with `docker build`:** ephemeral CI artifacts → *fix:* build in-cluster or use a CI registry; reference by tag.
- **Running `kubectl` from `command:` modules:** missed idempotence, missed `no_log`, missed retries → *fix:* use `kubernetes.core.k8s`/`k8s_info`/`helm`.
- **Direct Helm CLI in production:** drift between Helm-managed and free resources → *fix:* drive Helm through `kubernetes.core.helm` module.
- **`--kubeconfig` arg passing via shell:** prone to expansion errors → *fix:* use the `k8s_kubeconfig` parameter and `lookup('env', 'KUBECONFIG')`.
- **Molecule `delegated` driver without explicit create/destroy:** orphaned clusters → *fix:* always write `create.yml` and `destroy.yml` explicitly.
- **WordPress-style `clusterIP: None` everywhere:** remove the safety net of Kubernetes Service discovery → *fix:* only use headless services for StatefulSets.
- **Operators that mutate cluster-wide:** excessive blast radius → *fix:* use `--namespace` flags and `kustomize` overlays.
- **`--wait 300s` blindly:** hangs forever on slow CI → *fix:* explicitly `retries` + `delay` + `until` on the readiness probe.
- **No `imagePullPolicy: IfNotPresent` in dev:** Minikube can't see your local image → *fix:* `imagePullPolicy: IfNotPresent` for dev, `Always` for production with immutable tags.

## Decision Heuristics / Checklists

- *Local development?* Minikube or Kind.
- *Production cluster?* EKS / GKE / AKS or Kubespray on bare metal.
- *Cluster install?* Use CloudFormation/Terraform for control plane + Ansible for glue.
- *Single-cluster deploy?* `k8s` module + manifest lookup.
- *Helm chart?* `kubernetes.core.helm` with `state: present`.
- *Operator?* Ansible-based for simple lifecycle, Go-based for tight control loops.
- *CI?* Molecule `delegated` driver + Kind + `verify.yml` asserting via `k8s_info`.
- *Multi-cluster?* Per-cluster `KUBECONFIG`, environment-scoped vars, Molecule matrix.
- *Secret?* `no_log: true`, Vault or external secrets operator.
- *Network policy?* Default-deny, explicit allows, CNI-supported.
- *Apply order?* Namespace → ConfigMap → Secret → PVC → Deployment → Service → Ingress.

## Key Takeaways

1. **Ansible is the glue, not the cluster.** Use Terraform/CloudFormation for control plane, Ansible for everything around and inside it.
2. **Drive Kubernetes via the `k8s` and `helm` modules.** Don't shell out to `kubectl`; you lose idempotence and auditability.
3. **Templating + multi-document YAML is the simplest deployment pattern.** Compose sets with `lookup('template') | from_yaml_all | list`.
4. **Test in `molecule` with `delegated` driver + Kind cluster.** No tests means no guarantees.
5. **Use Vault or external-secrets for passwords.** Mark secret tasks with `no_log: true`.
6. **Operators: prefer Ansible for lifecycle, Go for control.** Use Ansible Operators when humans can read the YAML.
7. **Manage DNS at the same time as the application.** Combine `k8s_info` (read), `uri` (wait), `route53` (write).
8. **Pick a CNI and stick with it.** Don't mix Flannel with Calico.
9. **Default-deny NetworkPolicy.** Open only what's required by ad-hoc allow rules.
10. **End every workflow with `molecule test` in CI.** Kubernetes drift is silent; only automation catches it.

## Cross-References

- Related: [[../ansible_for_devops.md]] — Same tool, same modules; this file focuses on the Kubernetes surface area.
- Related: [[../Terraform_at_Scale.md]] — Use Terraform for cluster infra (VPC + EKS), Ansible for everything else.
- Related: [[../Ultimate_AWS_CDK.md]] — CDK can manage EKS clusters; pair with Ansible for application-side ops.
- Topic index: [[../INDEX.md]]
