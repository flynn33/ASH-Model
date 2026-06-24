# Governance and Discussions

## Governance surfaces

| Surface | File |
|---|---|
| Contribution process | `CONTRIBUTING.md` |
| Pull request template | `.github/pull_request_template.md` |
| Code of conduct | `CODE_OF_CONDUCT.md` |
| Discussion response policy | `docs/governance/github_automation_agents.md` |
| Moderation policy | `docs/governance/discussion_moderation_policy.md` |
| Workflow definitions | `.github/workflows/` |

## Pull request lifecycle

```mermaid
flowchart TD
    A["Scope change"] --> B["Update code, data, docs, or wiki"]
    B --> C["Run repository validation"]
    C --> D["Open pull request"]
    D --> E["CI checks"]
    E --> F["Review"]
    F --> G["Merge or revise"]
```

## Documentation rule

If a change affects commands, outputs, generated evidence, finite-theory status, science blockers, or public claims, update README, docs, changelog, and wiki source together.
