# Maintainers

## Current Maintainer

- Alan (`@alan747271363-art`) - primary maintainer, repository owner, release
  manager, issue triage owner, and reviewer for pull requests.

## Maintainer Responsibilities

The maintainer is responsible for:

- Reviewing incoming issues and pull requests.
- Keeping the CLI safe for offline use with no store, payment, ad account, or
  customer-data access.
- Maintaining test coverage for scoring, report generation, and CSV behavior.
- Preparing releases and updating examples when output changes.
- Responding to security reports without asking users to share private data.

## Review Expectations

Pull requests should be small, tested, and explain the seller problem they solve.
Changes that touch scoring rules, output formats, or safety language need extra
care because sellers may use the output for business decisions.

## Maintainer Automation Use Cases

Codex or API credits can help with routine maintenance work:

- Drafting issue triage summaries from public issue text.
- Generating tests for new scoring and report behavior.
- Reviewing pull requests for regression risks.
- Updating examples after output changes.
- Preparing release notes from commit history.
