# Security Policy

## Supported Versions

The latest version on the `main` branch is supported for security fixes.

## Reporting a Vulnerability

Please open a GitHub issue if the report does not contain sensitive information.
For sensitive reports, contact the maintainer through the public profile or Ko-fi
contact flow without posting secrets in public.

Do not include:

- Marketplace passwords or session cookies.
- Payment credentials.
- Ad account access.
- Customer names, addresses, emails, or order exports.
- Supplier contracts or private cost sheets.

## Project Security Model

The CLI is designed to run offline. It does not connect to stores, payment
processors, ad platforms, marketplaces, or customer databases. Inputs should be
public listing text and approximate business numbers only.

Security-sensitive changes include:

- Any network access.
- Any file upload or export feature.
- Any dependency that processes untrusted files.
- Any feature that encourages users to paste credentials or private customer
  data.
