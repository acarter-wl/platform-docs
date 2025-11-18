# Welcome to Platform Documentation

!!! tip "Quick Links"
    - [Architecture](architecture/overview.md) - Design decisions and system architecture
    - [Runbooks](runbooks/) - Operational procedures and incident response
    - [How-To Guides](how-to/) - Step-by-step tutorials

## About

This is a centralized documentation hub that aggregates documentation from multiple repositories into a single searchable site.

**Key Features:**

- **Multi-repo aggregation** - Pull docs from multiple GitHub repos automatically
- **Unified search** - Search across all documentation in one place
- **Docs as code** - Documentation lives next to the code it documents
- **AI-ready** - Structure supports future AI-generated documentation
- **Auto-deploy** - GitHub Actions automatically updates and deploys

---

## Documentation Structure & Navigation

### Search
Use the search bar in the top right (or press `s`) to find specific topics across all documentation.

### Architecture
System architecture, design patterns, and architectural decision records (ADRs).

**What you'll find:**
- High-level architecture overviews
- ADRs explaining "why we built it this way"
- Technical design documents
- Network diagrams and infrastructure maps

**When to read:**
- Understanding system design
- Proposing architectural changes
- Learning about technical decisions

### Runbooks
Operational procedures for incidents, maintenance, and risky operations.

**What you'll find:**
- Step-by-step incident response procedures
- Troubleshooting guides
- Disaster recovery procedures
- Maintenance playbooks

**When to use:**
- Responding to alerts and incidents
- On-call shifts
- Performing operational tasks

### How-To Guides
Practical, task-oriented guides for common development and operational tasks.

**What you'll find:**
- Step-by-step tutorials
- Code examples and templates
- Best practices and standards
- Testing and verification procedures

**When to use:**
- Learning a new task
- Following team standards
- Reference for correct procedures

---

## Contributing

We welcome contributions to improve our documentation!

### How to Contribute

1. **Found an error?** - Click the edit button (top right of any page)
2. **Missing documentation?** - Create an issue or PR in the [platform-docs repo](https://github.com/acarter-wl/platform-docs)
3. **Have feedback?** - Use the feedback widget at the bottom of each page

### Documentation Standards

| Type | Purpose | Location |
|------|---------|----------|
| **Architecture** | Significant architectural decision | architecture/adr/ |
| **Runbook** | Operational procedures | runbooks/ |
| **How-To** | Step-by-step guides | how-to/ |

---

## Getting Help

**GitHub:** [Create an issue](https://github.com/acarter-wl/platform-docs/issues)

**MkDocs:** [MkDocs Material Documentation](https://squidfunk.github.io/mkdocs-material/)

---

*Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)*
