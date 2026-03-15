# GitHub Automation Agents

Date: 2026-03-15
Project: ASH Model
Status: discussion automation baseline

## Purpose

This document describes the GitHub automation added to this repository for discussion responses, topic seeding, and moderation.

## Discussion Response Agents

The discussion-response workflow routes new GitHub Discussions topics and new discussion comments to one of three repo-grounded agents:
- Technical Discussion Agent
- Support Discussion Agent
- Research/Theory Discussion Agent

It works by:
- classifying each new discussion post or comment into technical, support, or research/theory scope
- searching only repository-tracked source material for matching information
- replying with file-grounded references from the repo when relevant sources exist
- falling back to `There is not information available at this time. Check back soon.` when the repository does not currently answer the question

Boundary rules:
- the agents respond only from repository truth and do not invent unsupported answers
- support responses prefer README, contribution guidance, wiki setup, and operating instructions
- technical responses prefer simulation scripts, tools, workflows, audits, and repository-structure docs
- research/theory responses prefer the paper narrative, axioms, manuscript surfaces, and theory-review docs

## Discussion Topic Seeder Agent

The discussion-topic-seeder workflow scans repository truth on a schedule and opens category-level GitHub Discussions topics when equivalent seeded topics do not already exist.

It works by:
- reading repository-driven topic sources such as `wiki/Home.md`, `.github/wiki-sync.json`, and `docs/ASH-research-paper.md`
- deriving candidate topics from wiki sections, mapped wiki pages, and research-paper headings
- classifying each candidate into the technical, support, or research/theory family using the same repo-grounded routing logic as the response agents
- selecting at most one new topic per family and at most three total topics per run
- creating discussions only when the seeded topic marker or exact topic title is not already present on the discussion board

Boundary rules:
- generated topics must be derived from repository truth, not invented freeform prompts
- topic bodies must point back to the repository source path and include a repository-grounded summary
- when no new seeded topics are needed, the workflow exits without creating anything

## Discussion Moderation Agent

The discussion-moderation workflow enforces the repository code of conduct on GitHub Discussions content.

It works by:
- moderating newly created or edited discussions and discussion comments
- rescanning recent discussion content on a six-hour schedule
- deleting discussion threads or comments that match the repository moderation policy
- logging moderation incidents to a repository-owned issue for maintainer review
- attempting user blocking for severe violations only when an owner-supplied admin token is available

Boundary rules:
- the moderation rules come from `CODE_OF_CONDUCT.md` and `docs/governance/discussion_moderation_policy.md`
- the bot removes content rather than rewriting it in place
- owner reporting stays inside the repository issue tracker
- automated blocking is best-effort only and requires `DISCUSSION_MODERATION_ADMIN_TOKEN`
