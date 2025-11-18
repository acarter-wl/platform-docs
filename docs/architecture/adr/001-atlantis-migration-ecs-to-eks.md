# ADR-001: Migrate Atlantis from ECS to EKS

## Status
Accepted

**Date:** 2025-09-08

## Context
Atlantis, our Terraform CI/CD automation tool, was initially deployed on AWS ECS. However, our infrastructure landscape has evolved significantly:

- We now operate 15 production Kubernetes clusters running customer-facing workloads (Ambra/IntelePACS)
- The Platform Engineering team has deep Kubernetes operational expertise
- ECS represents operational divergence from our primary container orchestration platform
- Managing two different container platforms increases cognitive load and operational complexity

**Current Situation:**
- Atlantis runs as an ECS task in platform-prod account
- Uses ECS-specific monitoring and deployment patterns
- Team must maintain expertise in both ECS and Kubernetes operations

**Problem:**
We're not "dogfooding" our own Kubernetes platform, and maintaining operational knowledge for two container platforms is inefficient.

## Decision
Migrate Atlantis from ECS to EKS, deploying it to our existing platform-prod Kubernetes cluster.

**Implementation Approach:**
- Deploy Atlantis as a Kubernetes Deployment with 1 replica
- Use Helm chart for deployment configuration
- Maintain existing GitHub webhook integration
- Preserve S3-backed state storage
- Implement Kubernetes-native monitoring and logging

## Consequences

### Positive Consequences
✅ **Unified Operations:** Single operational model for all containerized workloads
✅ **Team Expertise:** Leverages existing Kubernetes knowledge
✅ **Better Observability:** Can use existing Prometheus/Grafana stack
✅ **Dogfooding:** Platform team uses the platform we provide to others
✅ **Flexibility:** Easier to add sidecars (monitoring, security scanning, etc.)
✅ **GitOps:** Can manage Atlantis configuration via ArgoCD like other apps

### Negative Consequences
❌ **Migration Risk:** Downtime during cutover could block terraform deployments
❌ **Complexity:** Kubernetes adds operational complexity vs simple ECS task
❌ **Different Backup Model:** Need to implement K8s-native backup/DR strategies
❌ **Learning Curve:** Small learning curve for team members only familiar with ECS

### Risks
⚠️ **Risk 1: Migration downtime**
- Mitigation: Perform migration during low-activity window, have rollback plan

⚠️ **Risk 2: Persistent volume issues**
- Mitigation: Test PVC creation and mounting in staging first

⚠️ **Risk 3: Webhook delivery failures**
- Mitigation: Monitor webhook queue, ensure ingress is properly configured

## Alternatives Considered

### Alternative 1: Stay on ECS
**Description:** Continue running Atlantis on ECS

**Rejected because:**
- Perpetuates operational divergence
- Team is shifting focus to Kubernetes
- Misses opportunity to dogfood our platform

### Alternative 2: Managed GitHub Actions
**Description:** Replace Atlantis with GitHub Actions workflows

**Rejected because:**
- Lacks built-in terraform state locking
- Would require custom implementation of plan/apply workflow
- Less visibility into plan status directly in GitHub
- Atlantis provides better multi-workspace management

### Alternative 3: Terraform Cloud
**Description:** Use HashiCorp's managed Terraform Cloud

**Rejected because:**
- Cost prohibitive at our scale (100+ accounts)
- Reduces control over CI/CD process
- Vendor lock-in concerns
- Would still need to migrate existing workflows

## References
- Jira ticket: PLT-4647
- Migration PR: [Link when created]
- Atlantis documentation: https://www.runatlantis.io/
- Related: Future ADR on Atlantis monitoring/observability

## Notes
**Post-Migration TODO:**
- Implement health checks and monitoring (PLT-4648)
- Document runbook for Atlantis operations on K8s
- Train team on K8s-specific troubleshooting for Atlantis

**Future Considerations:**
- May want to explore running multiple Atlantis replicas for HA
- Consider implementing blue/green deployment strategy

---

**Author(s):** Platform Engineering Team
**Reviewers:** Tech Lead, SRE Team
**Last Updated:** 2025-09-08
