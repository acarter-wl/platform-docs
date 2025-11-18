# How-To Guides

## What are How-To Guides?

**How-To Guides** are practical, step-by-step tutorials for common development and operational tasks.

How-To guides help us:
- 🎓 Learn new tasks quickly
- 📋 Follow team standards consistently
- 🔄 Reduce repeated questions in Slack
- 📊 Onboard new team members faster

## When to Use How-To Guides

Use how-to guides when:
- **Learning a new task** - First time doing something
- **Following standards** - Ensuring you do it "the right way"
- **Need reference** - Quick lookup for commands/procedures
- **Onboarding** - Learning team workflows

## Available How-To Guides

### Terraform & Infrastructure
| Guide | Difficulty | Time | Updated |
|-------|------------|------|---------|
| [Create a Terraform Module](create-terraform-module.md) | Intermediate | 45-60 min | 2025-11-17 |

### Kubernetes
*No guides yet - help us add some!*

### CI/CD
*No guides yet*

### Networking
*No guides yet*

---

## How-To Format

Each guide includes:
- **Time Required** - How long will this take?
- **Difficulty** - Beginner, Intermediate, Advanced
- **Prerequisites** - What do you need before starting?
- **Step-by-step instructions** - Clear, numbered steps
- **Examples** - Working code you can copy
- **Troubleshooting** - Common errors and solutions
- **Verification** - How to confirm it worked

---

## Creating a How-To Guide

### When to Write One
Write a how-to guide when:
- Same question asked 3+ times in Slack
- New team members struggle with a task
- No documented procedure exists
- Task requires following specific standards

### Writing Process
1. **Identify the task** - Be specific about scope
2. **Test the procedure** - Actually follow your own steps
3. **Use the template** from plt-modules repo
4. **Include examples** - Working code/commands
5. **Add troubleshooting** - Common errors you encountered
6. **Get review** from someone who hasn't done it before
7. **Update as needed** - Mark when last tested

**Template:** [How-To Template](https://github.com/intelerad-org/plt-modules/blob/main/docs/how-to/template.md)

---

## How-To Best Practices

### Do ✅
- **Make it actionable** - Clear steps anyone can follow
- **Include working examples** - Copy-paste ready code
- **Test the procedure** - Follow your own steps
- **Show expected output** - What should I see?
- **Add time estimates** - Set expectations
- **Keep it updated** - Note when last tested

### Don't ❌
- Don't assume prior knowledge - explain concepts
- Don't skip verification steps
- Don't forget prerequisites - list tools/access needed
- Don't make it too abstract - be specific
- Don't let guides go stale - mark outdated ones

---

## How-To vs Runbook vs ADR

| Type | Purpose | When to Use | Example |
|------|---------|-------------|---------|
| **How-To** | Learn a task | "How do I...?" | Creating a terraform module |
| **Runbook** | Handle incidents | "Service is down!" | Atlantis outage response |
| **ADR** | Understand decisions | "Why did we...?" | Why use Atlantis vs GitHub Actions |

---

## How-To Guides We Need

Help us build our guide library! High-priority guides needed:

### Terraform
- [ ] Deploy infrastructure to production
- [ ] Release a new module version
- [ ] Import existing resources into terraform
- [ ] Troubleshoot terraform state issues

### Kubernetes
- [ ] Deploy a new application to K8s
- [ ] Create a new K8s cluster
- [ ] Update a helm chart
- [ ] Troubleshoot pod failures

### CI/CD
- [ ] Use Atlantis for terraform deployments
- [ ] Configure ArgoCD for new app
- [ ] Set up Renovate for dependency updates
- [ ] Create GitHub Actions workflow

### Networking
- [ ] Provision TrustGrid gateway
- [ ] Configure BGP routing
- [ ] Set up Direct Connect
- [ ] Troubleshoot network connectivity

### Operations
- [ ] Provision a new AWS account
- [ ] Set up monitoring/alerting
- [ ] Configure SSM access to EC2
- [ ] Respond to security audit findings

Pick one and create a PR!

---

## Quick Reference by Task

### "How do I deploy...?"
- **Terraform changes?** → *[Guide needed: Using Atlantis]*
- **K8s application?** → *[Guide needed: Deploy to K8s]*
- **To production?** → *[Guide needed: Production deployment]*

### "How do I create...?"
- **Terraform module?** → [Create a Terraform Module](create-terraform-module.md)
- **K8s cluster?** → *[Guide needed]*
- **New AWS account?** → *[Guide needed]*

### "How do I troubleshoot...?"
- **Terraform issues?** → *[Guide needed]*
- **K8s pod problems?** → *[Guide needed]*
- **Network connectivity?** → *[Guide needed]*

---

## Related Resources
- [Runbooks](../runbooks/) - Incident response procedures
- [ADRs](../architecture/adr/) - Architecture decisions
- [Architecture Overview](../architecture/overview.md) - System design

---

**Questions?**
- Slack: #platform-team
- Email: platform-engineering@intelerad.com
