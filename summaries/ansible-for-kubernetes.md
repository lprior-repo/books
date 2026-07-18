# Ansible for Kubernetes - Jeff Geerling

## Comprehensive Summary

---

## Chapter 1: Hello World - From Go to Container

The book starts from the ground up, building a Go web application, containerizing it, and deploying it.

**Building a Go app:**
- Create a simple HTTP server in Go
- Build the binary with `go build`
- Cross-compile for Linux if developing on macOS/Windows

**Docker containerization:**
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o hello-go

FROM alpine:latest
COPY --from=builder /app/hello-go /hello-go
CMD ["/hello-go"]
```

**Key insight:** Containerizing applications is the first step toward Kubernetes deployment. Ansible can automate both the container build and deployment.

---

## Chapter 2: Automation Brings DevOps Bliss

**Why automate Kubernetes operations:**
- Manual kubectl commands are error-prone and not reproducible
- Teams need consistent deployment processes
- Infrastructure changes should be version-controlled

**Ansible as Kubernetes automation tool:**
- Declarative YAML playbooks define desired state
- Idempotent: safe to run repeatedly
- Integrates with existing Ansible infrastructure management
- Can manage both infrastructure (VMs, networking) and applications (deployments, services)

---

## Chapter 3: Ansible Manages Containers

**Building container images with Ansible:**
```yaml
- name: Build Docker image
  community.docker.docker_image:
    build:
      path: /path/to/app
    name: myapp
    tag: latest
    source: build
```

**Testing containers before deployment:**
- Run containers locally, validate with health checks
- Integration testing against containerized dependencies
- Automated container rebuild and testing pipeline with Ansible

**Case study - Apache Solr container:**
- Multi-stage build with Ansible
- Automated testing of container functionality
- Integration with CI pipeline

---

## Chapter 4: Building K8s Clusters with Ansible

**Local Kubernetes cluster with Vagrant and Ansible:**
- Use Vagrant to provision VMs
- Ansible playbook to install Kubernetes components (kubeadm, kubelet, kubectl)
- Configure networking (Flannel, Calico)
- Join worker nodes to the cluster

**Ansible roles for cluster building:**
- `kubernetes-master`: Initialize control plane
- `kubernetes-worker`: Join workers
- `kubernetes-networking`: Configure CNI
- `kubernetes-addons`: Install Dashboard, Ingress, etc.

**Building with Kubespray:**
- Ansible-based Kubernetes cluster provisioning tool
- Supports AWS, GCP, Azure, bare metal, Raspberry Pi
- Production-grade configuration with HA support

---

## Chapter 5: AWS EKS with CloudFormation and Ansible

**Infrastructure provisioning:**
- CloudFormation templates for VPC, subnets, security groups
- EKS cluster and node group templates
- Ansible applies and manages CloudFormation stacks

**Application deployment:**
```yaml
- name: Deploy to EKS
  kubernetes.core.k8s:
    state: present
    definition: "{{ lookup('template', 'deployment.yml.j2') }}"
```

**Full workflow:**
1. Provision VPC with CloudFormation via Ansible
2. Create EKS cluster
3. Configure kubectl/kubeconfig
4. Deploy application manifests
5. Configure DNS and load balancing

---

## Chapter 6: GKE with Terraform and Ansible

**Terraform for infrastructure, Ansible for configuration:**
- Terraform provisions GKE clusters
- Ansible configures applications and Kubernetes resources
- The two tools complement each other: Terraform for raw infrastructure, Ansible for application lifecycle

---

## Chapter 7: CI Testing with Molecule and Kind

**Testing Ansible playbooks for Kubernetes:**
- **Molecule**: Test Ansible roles in isolated environments
- **Kind (Kubernetes in Docker)**: Lightweight K8s clusters for testing
- Molecule + Kind = reproducible, automated K8s playbook testing

**Testing workflow:**
1. Molecule creates a Kind cluster
2. Ansible playbook runs against the cluster
3. Molecule verifies the expected state
4. CI runs this pipeline on every commit

**GitHub Actions integration:**
```yaml
- name: Test with Molecule
  run: molecule test
```

---

## Chapter 8: Ansible's Kubernetes Integration

**Core modules:**
- `k8s`: Create, update, delete any Kubernetes resource
- `k8s_info`: Query existing resources
- `k8s_scale`: Scale deployments/replica sets
- `k8s_exec`: Execute commands in pods
- `k8s_log`: Retrieve pod logs
- `k8s_service`: Manage services
- `k8s_inventory`: Dynamic inventory from K8s

**Helm integration:**
- `kubernetes.core.helm`: Install, upgrade, delete Helm charts
- `kubernetes.core.helm_info`: Query Helm releases
- `kubernetes.core.helm_repository`: Manage chart repositories

---

## Key Takeaways

1. **Ansible bridges infrastructure and applications**: Manage VMs, networking, and Kubernetes resources with the same tool and language.

2. **Combine with other tools**: Use Terraform/CloudFormation for raw infrastructure, Ansible for application and configuration management.

3. **Test playbooks with real clusters**: Molecule + Kind gives you reproducible Kubernetes testing without production risk.

4. **Automate everything from cluster creation to application deployment**: Full lifecycle management through Ansible playbooks.

5. **Kubespray for production clusters**: Don't build from scratch—use Kubespray's battle-tested Ansible playbooks for cluster provisioning.

6. **Use the k8s module for everything**: It handles any Kubernetes resource type, so you don't need separate modules for each resource.

7. **Helm + Ansible is powerful**: Use Helm for complex application charts, Ansible to orchestrate when and how they're deployed.
