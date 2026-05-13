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
- Actionable next steps ranked by likely business impact

## Quick Start

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
| `--format` | `markdown` or `json` |
| `--sample` | Run a built-in demo audit |

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
```

## Safety Notes

This tool does not connect to marketplaces, payment processors, ad accounts, or
stores. It only analyzes text and numbers provided by the user.
