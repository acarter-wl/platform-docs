# Team Information

Welcome to the Platform Engineering team!

## Who We Are

The Platform Engineering team builds and maintains the infrastructure platform that enables engineering teams at Intelerad to move fast with confidence.

**Our Mission:**
Enable developers to deploy secure, scalable infrastructure without needing to be infrastructure experts.

## Team Resources

### For New Team Members
- [Onboarding Guide](onboarding.md) - Start here!
- [Architecture Overview](../architecture/overview.md) - Understand our systems
- [How-To Guides](../how-to/) - Learn our workflows

### For Everyone
- [On-Call Guide](on-call.md) - On-call procedures and escalation
- [Runbooks](../runbooks/) - Incident response procedures
- [ADRs](../architecture/adr/) - Architecture decisions

---

## Communication

### Slack Channels
- **#platform-team** - General team discussion
- **#platform-incidents** - Incident response and postmortems
- **#platform-announcements** - Important updates

### Meetings
- **Weekly Standup** - Monday 10am ET
- **Sprint Planning** - Every 2 weeks
- **Retrospective** - End of each sprint
- **Architecture Review** - As needed

### Email
- **Team Email:** platform-engineering@intelerad.com
- **On-Call:** @platform-oncall (Slack)

---

## Team Conventions

### Code Reviews
- All PRs require 1 approval before merge
- Use PR templates for consistency
- Review within 24 hours when possible
- Be respectful and constructive

### Git Workflow
- Branch naming: `feature/description`, `fix/description`, `docs/description`
- Commit messages: Follow conventional commits
- PR titles: Clear and descriptive
- Merge strategy: Squash and merge for feature branches

### Documentation
- ADRs for architectural decisions
- Runbooks after incidents (within 48 hours)
- How-To guides for repeated tasks
- Update docs as you work, not after

---

## Tools We Use

### Infrastructure
- **AWS** - Primary cloud provider
- **Terraform** - Infrastructure as code
- **Atlantis** - Terraform CI/CD
- **Ansible** - Network automation

### Kubernetes
- **ArgoCD** - GitOps for K8s
- **Helm** - Package manager
- **Renovate** - Dependency updates
- **kubectl** - CLI tool

### Developer Tools
- **Port.io** - Developer portal
- **GitHub** - Code repository and CI/CD
- **VS Code** - Recommended IDE
- **Slack** - Team communication

### Monitoring
- **PagerDuty** - On-call and alerting
- **Grafana** - Metrics (planned)
- **Prometheus** - Monitoring (planned)

---

## On-Call

### On-Call Schedule
View current schedule: [PagerDuty](https://intelerad.pagerduty.com)

### On-Call Responsibilities
- Respond to alerts within 15 minutes
- Follow runbooks for known issues
- Escalate to secondary if unable to resolve in 30 min
- Document incidents and create runbooks

**Learn More:** [On-Call Guide](on-call.md)

---

## Career Development

### Growth Paths
- **Individual Contributor:** Junior → Mid → Senior → Staff → Principal
- **Leadership:** Team Lead → Engineering Manager

### Skills We Value
- Infrastructure as code (Terraform)
- Container orchestration (Kubernetes)
- Network engineering
- CI/CD automation
- System design and architecture
- Incident response
- Documentation and communication

### Learning Resources
- **Internal:** Browse our [How-To Guides](../how-to/)
- **External:** [Recommended reading list](https://example.com) *(to be added)*
- **Budget:** $X/year for conferences, training, books

---

## Team Values

### Automation Over Toil
If you do it twice manually, automate it the third time.

### Documentation is Code
Document as you build, not after. Docs are as important as code.

### Blameless Culture
Focus on systems that failed, not people who made mistakes.

### Security by Default
Security is not optional. Build it in from the start.

### Empathy for Users
Remember that developers are our customers. Make their lives easier.

---

## Contact Information

### Team
- **Slack:** #platform-team
- **Email:** platform-engineering@intelerad.com
- **On-Call:** @platform-oncall

### Leadership
- **Team Lead:** [Name]
- **Engineering Manager:** [Name]

### Escalation
See [On-Call Guide](on-call.md) for escalation procedures

---

## Quick Links

**For New Team Members:**
- [Onboarding Guide](onboarding.md)
- [Architecture Overview](../architecture/overview.md)
- [How-To Guides](../how-to/)

**For Daily Work:**
- [Runbooks](../runbooks/)
- [ADRs](../architecture/adr/)
- [GitHub Org](https://github.com/intelerad-org)

**For Incidents:**
- [Incident Response Runbooks](../runbooks/)
- [PagerDuty](https://intelerad.pagerduty.com)
- Slack: #platform-incidents

---

**Questions?** Ask in #platform-team on Slack!
