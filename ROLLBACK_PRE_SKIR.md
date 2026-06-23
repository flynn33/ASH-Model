# Rollback Request: Return main to pre-Skir baseline

This branch marks the requested rollback target for ASH-Model.

Target pre-Skir commit:

```text
6619b9ca877add5d16b64cb722c320d7ee1d9147
```

Intent:

- Revert `main` to the repository state immediately before the Skir merge.
- Remove Skir implementation, documentation, validation gates, tests, simulation controls, and wiki-source additions introduced after that point.
- Preserve this rollback as a normal pull request rather than force-pushing `main`.

Implementation note:

This marker file exists only to make the rollback branch openable as a pull request from a historical baseline. The actual merge strategy should restore the tree of commit `6619b9ca877add5d16b64cb722c320d7ee1d9147` onto `main`.
