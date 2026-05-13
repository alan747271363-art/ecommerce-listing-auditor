# Ecommerce Listing Auditor

Practical command-line auditor for ecommerce product listings. It scores listing
copy, flags conversion risks, and estimates margin pressure from price, landed
cost, ads, marketplace fees, shipping, and refunds.

This repo is a public monetizable sample project. The free CLI helps sellers run
quick checks; paid custom audits and template tuning can be requested through
Ko-fi:

https://ko-fi.com/alan363

## What It Checks

- Title clarity, length, and keyword coverage
- Description strength across benefits, specs, trust, and shipping cues
- Risk words that may trigger marketplace or ad review
- Gross margin, contribution margin, and break-even ad spend
- Batch executive summary for multi-listing audits
- Actionable next steps ranked by likely business impact

## Quick Start

Install the local package after cloning:

```bash
python -m pip install -e .
```

```bash
python -m listing_auditor \
  --title "Portable Blender USB Rechargeable 500ml Smoothie Maker" \
  --description "Rechargeable portable blender with six blades, BPA-free cup, USB-C charging, and easy cleaning for travel, gym, and office smoothies." \
  --price 29.99 \
  --cost 9.40 \
  --shipping 3.20 \
  --ad-spend 5.00 \
  --marketplace-fee-rate 0.15 \
  --refund-rate 0.04
```

For JSON output:

```bash
python -m listing_auditor --sample --format json
```

For a batch CSV audit:

```bash
python -m listing_auditor --input-csv samples/listings.csv
```

Batch Markdown reports start with an executive summary showing average score,
the lowest-scoring listing, how many listings are at or below break-even after
ads, and the top priority listings to fix first.

To save a client-ready report:

```bash
python -m listing_auditor --input-csv samples/listings.csv --output reports/audit.md
python -m listing_auditor --input-csv samples/listings.csv --format html --output reports/audit.html
python -m listing_auditor --input-csv samples/listings.csv --format json --output reports/audit.json
python -m listing_auditor --input-csv samples/listings.csv --format csv --output reports/audit-summary.csv
```

Use `--format html` when you want a client-facing report that opens directly in
a browser. It is a single self-contained file with the score, risks, unit
economics, and next actions for each listing.

The CSV needs these columns:

```text
title,description,price,cost,shipping,ad_spend,marketplace_fee_rate,refund_rate
```

An optional `sku` or `id` column is used as the report label.

## Example Output

```text
Listing Audit
Score: 82/100
Margin: $6.19 contribution profit per order
Break-even ad spend: $11.19

Top actions
1. Add 2-3 proof points such as warranty, review count, certification, or guarantee.
2. Add buyer-specific keywords that match search intent.
3. Keep refund assumptions visible because they materially affect contribution profit.
```

## Request a Custom Audit

Use the free CLI for quick checks, or request a paid manual audit through Ko-fi:

https://ko-fi.com/alan363

Useful starting points:

- [Custom audit offer](docs/custom-audit-offer.md)
- [Browser-ready HTML report service](docs/html-report-service.md)
- [Sample audit request](samples/sample-audit-request.md)
- [Sample audit report](samples/sample-audit-report.md)
- [Sample browser-ready HTML report](samples/sample-audit-report.html)
- [GitHub custom audit request template](.github/ISSUE_TEMPLATE/custom-audit-request.md)

Please do not share marketplace passwords, payment credentials, ad account
access, customer data, or private order exports. Public listing links, listing
text, and approximate unit economics are enough for a safe first review.

## Input Options

| Option | Description |
| --- | --- |
| `--title` | Product title to score |
| `--description` | Product description or bullet text |
| `--price` | Sale price |
| `--cost` | Product landed cost |
| `--shipping` | Seller-paid shipping or fulfillment cost |
| `--ad-spend` | Expected ad spend per order |
| `--marketplace-fee-rate` | Marketplace fee as decimal, e.g. `0.15` |
| `--refund-rate` | Expected refund rate as decimal, e.g. `0.04` |
| `--format` | `markdown`, `json`, `csv`, or `html` |
| `--sample` | Run a built-in demo audit |
| `--input-csv` | Audit multiple listings from a CSV file |
| `--output` | Save the report to a file instead of only printing it |

## Paid Use Cases

This tool can be used as a lead magnet for:

- Product listing audits
- Amazon/Shopify title and bullet rewrites
- Margin and break-even ad spend checks
- Product launch checklist reviews
- Bulk listing audit templates for ecommerce operators

Request paid customization or a manual audit through Ko-fi:

https://ko-fi.com/alan363

## Development

```bash
python -m compileall src tests
python -m pytest
python -m listing_auditor --sample
python -m listing_auditor --input-csv samples/listings.csv
python -m listing_auditor --input-csv samples/listings.csv --output reports/audit.md
python -m listing_auditor --input-csv samples/listings.csv --format html --output reports/audit.html
python -m listing_auditor --input-csv samples/listings.csv --format csv --output reports/audit-summary.csv
```

## Safety Notes

This tool does not connect to marketplaces, payment processors, ad accounts, or
stores. It only analyzes text and numbers provided by the user.
