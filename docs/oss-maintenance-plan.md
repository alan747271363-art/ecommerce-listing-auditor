# OSS Maintenance Plan

This document explains why this public project is a legitimate open-source
maintenance target and how maintainer automation would be used.

## Project Role

`ecommerce-listing-auditor` is a small Python CLI for ecommerce operators. It
turns public listing text and approximate unit economics into practical audit
output: score, risks, margins, break-even ad spend, and rewrite direction.

The project is useful because many small sellers need a safe first-pass review
without connecting private stores, payment processors, ad accounts, or customer
databases.

## Maintainer Role

Alan (`@alan747271363-art`) is the repository owner and primary maintainer. The
maintainer work includes:

- Reviewing issues and pull requests.
- Keeping CI and tests healthy.
- Managing releases and sample reports.
- Updating safety guidance so users do not share private data.
- Evaluating scoring-rule changes against business and marketplace risk.

## Why Codex Or API Credits Help

API credits would be used for open-source maintainer workflows, not private
store automation:

- Summarize public issues and propose triage labels.
- Draft tests for scoring and report-output changes.
- Review pull requests for regression risks and missing documentation.
- Generate release-note drafts from commits and changelog entries.
- Convert structured audit results into clearer, plain-language explanations.

## Boundaries

The core CLI should remain free, offline, and dependency-light. Any future AI
feature should be optional and must not require users to provide credentials,
customer data, payment data, ad account access, or private order exports.

## Current Evidence

- Public repository owned by `alan747271363-art`.
- CI workflow for compile, tests, lint, and sample audit.
- Maintainer documentation, roadmap, security policy, PR template, and issue
  templates.
- Existing sample reports and multiple releases.
