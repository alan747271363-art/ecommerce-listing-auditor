# Roadmap

This roadmap keeps the project honest about what is planned and what is out of
scope. It is not a promise of delivery dates.

## Near Term

- Add more sample listings across Amazon, Shopify, Etsy, and TikTok Shop style
  use cases.
- Improve title rewrite suggestions so they stay marketplace-neutral and avoid
  unverifiable claims.
- Add tests for unusual CSV values, missing costs, and zero ad spend.
- Keep HTML reports easy to open in a browser without external assets.
- Document how sellers can safely share non-sensitive data for audits.

## Maintainer Workflow

- Use issues for feature requests, bugs, and scoring-rule discussions.
- Use pull requests for reviewed changes.
- Keep CI passing before merging.
- Update CHANGELOG entries when user-visible output changes.
- Prefer small releases over large rewrites.

## Possible API Credit Uses

- Generate draft report explanations from structured audit output.
- Summarize public issue reports for maintainer triage.
- Draft tests for scoring-rule changes.
- Build optional local prompts for sellers who want plain-language rewrite
  suggestions.

## Out Of Scope

- Connecting to private stores or marketplaces.
- Handling customer data or order exports.
- Guaranteeing revenue, ranking, ad approval, or marketplace compliance.
- Requiring paid APIs for the core free CLI.
