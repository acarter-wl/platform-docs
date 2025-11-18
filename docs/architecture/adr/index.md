# Architecture Decision Records (ADRs)

## What is an ADR?

An **Architecture Decision Record** (ADR) is a document that captures an important architectural decision made along with its context and consequences.

ADRs help us:
- 📝 Remember why we made specific decisions
- 🎓 Onboard new team members
- 🔄 Avoid re-litigating past decisions
- 📊 Track architectural evolution over time

## When to Write an ADR

Create an ADR when:
- Choosing between different technologies or approaches
- Making decisions that will affect the team for months/years
- Establishing architectural patterns or standards
- Migrating from one technology to another

**Examples:**
- "Should we use Atlantis or GitHub Actions for terraform CI/CD?"
- "How should we structure our AWS account organization?"
- "Which Kubernetes distribution should we use?"

## ADR Format

Each ADR includes:
- **Status:** Proposed, Accepted, Deprecated, or Superseded
- **Context:** What problem are we solving?
- **Decision:** What did we decide to do?
- **Consequences:** What are the trade-offs?
- **Alternatives:** What else did we consider?

## All ADRs

### Active ADRs

| Number | Title | Date | Status |
|--------|-------|------|--------|
| [ADR-001](001-atlantis-migration-ecs-to-eks.md) | Atlantis Migration from ECS to EKS | 2025-09-08 | Accepted |

### Deprecated ADRs
*None yet*

### Superseded ADRs
*None yet*

---

## Creating an ADR

1. **Copy the template** from plt-modules repo
2. **Number it** sequentially (next available number)
3. **Fill it out** completely
4. **Get review** from team/tech lead
5. **Commit and merge** to document the decision

**Template:** [ADR Template](https://github.com/intelerad-org/plt-modules/blob/main/docs/adr/template.md)

---

## ADR Best Practices

### Do ✅
- Write ADRs **before** or **during** implementation
- Include the **context** that led to the decision
- Document **alternatives considered** and why they were rejected
- Be **honest** about consequences (both positive and negative)
- Keep ADRs **concise** (2-3 pages max)

### Don't ❌
- Don't write ADRs after-the-fact to justify decisions
- Don't skip alternatives considered section
- Don't hide negative consequences
- Don't make ADRs too detailed (save that for technical specs)

---

## Related Resources
- [Architecture Overview](../overview.md)
- [Runbooks](../../runbooks/)
- [How-To Guides](../../how-to/)

---

**Need help?** Ask in #platform-team on Slack
