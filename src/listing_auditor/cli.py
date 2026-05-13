from __future__ import annotations

import argparse
import csv
from html import escape
from io import StringIO
import json
from pathlib import Path

from listing_auditor.audit import AuditInput, AuditResult, audit_listing


SAMPLE = AuditInput(
    title="Portable Blender USB Rechargeable 500ml Smoothie Maker",
    description=(
        "Rechargeable portable blender with six blades, BPA-free cup, USB-C charging, "
        "and easy cleaning for travel, gym, and office smoothies."
    ),
    price=29.99,
    cost=9.40,
    shipping=3.20,
    ad_spend=5.00,
    marketplace_fee_rate=0.15,
    refund_rate=0.04,
)

CSV_REQUIRED_FIELDS = (
    "title",
    "description",
    "price",
    "cost",
    "shipping",
    "ad_spend",
    "marketplace_fee_rate",
    "refund_rate",
)


def _money(value: float) -> str:
    return f"${value:.2f}"


def to_markdown(result: AuditResult) -> str:
    risk_lines = result.risks or ["No obvious high-risk claim phrases found."]
    action_lines = [f"{index}. {action}" for index, action in enumerate(result.actions, start=1)]
    return "\n".join(
        [
            "Listing Audit",
            f"Score: {result.score}/100",
            "",
            "Score breakdown",
            f"- Title: {result.title_score}/35",
            f"- Description: {result.description_score}/35",
            f"- Economics: {result.economics_score}/30",
            "",
            "Unit economics",
            f"- Marketplace fee: {_money(result.economics.marketplace_fee)}",
            f"- Expected refund cost: {_money(result.economics.expected_refund_cost)}",
            f"- Gross profit before ads: {_money(result.economics.gross_profit)}",
            f"- Contribution profit after ads: {_money(result.economics.contribution_profit)}",
            f"- Gross margin rate: {result.economics.gross_margin_rate:.1%}",
            f"- Break-even ad spend: {_money(result.economics.break_even_ad_spend)}",
            "",
            "Risks",
            *[f"- {risk}" for risk in risk_lines],
            "",
            "Top actions",
            *action_lines,
        ]
    )


def to_json(result: AuditResult) -> str:
    return json.dumps(result_to_dict(result), indent=2)


def _score_class(score: int) -> str:
    if score >= 80:
        return "good"
    if score >= 60:
        return "watch"
    return "urgent"


def _html_list(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def _single_audit_html(label: str, data: AuditInput, result: AuditResult) -> str:
    risks = result.risks or ["No obvious high-risk claim phrases found."]
    return f"""
    <section class="audit-card">
      <div class="audit-head">
        <div>
          <p class="eyebrow">{escape(label)}</p>
          <h2>{escape(data.title)}</h2>
        </div>
        <strong class="score {_score_class(result.score)}">{result.score}/100</strong>
      </div>
      <div class="grid">
        <div>
          <h3>Score breakdown</h3>
          <ul>
            <li>Title: {result.title_score}/35</li>
            <li>Description: {result.description_score}/35</li>
            <li>Economics: {result.economics_score}/30</li>
          </ul>
        </div>
        <div>
          <h3>Unit economics</h3>
          <ul>
            <li>Contribution profit after ads: {_money(result.economics.contribution_profit)}</li>
            <li>Gross margin rate: {result.economics.gross_margin_rate:.1%}</li>
            <li>Break-even ad spend: {_money(result.economics.break_even_ad_spend)}</li>
          </ul>
        </div>
      </div>
      <h3>Risks</h3>
      <ul>{_html_list(risks)}</ul>
      <h3>Top actions</h3>
      <ol>{_html_list(result.actions)}</ol>
    </section>
    """.strip()


def html_document(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color: #17202a;
      background: #f7f5ef;
      font-family: Arial, Helvetica, sans-serif;
    }}
    body {{
      margin: 0;
      background: #f7f5ef;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1, h2, h3, p {{
      margin-top: 0;
    }}
    h1 {{
      font-size: 34px;
      margin-bottom: 8px;
    }}
    h2 {{
      font-size: 22px;
      margin-bottom: 8px;
    }}
    h3 {{
      font-size: 15px;
      margin-bottom: 8px;
    }}
    ul, ol {{
      margin-top: 0;
      padding-left: 22px;
    }}
    li {{
      margin: 6px 0;
    }}
    .subtle {{
      color: #586575;
      margin-bottom: 24px;
    }}
    .summary, .audit-card {{
      background: #ffffff;
      border: 1px solid #e0ddd4;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 18px;
      box-shadow: 0 8px 24px rgba(23, 32, 42, 0.06);
    }}
    .audit-head {{
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: flex-start;
      margin-bottom: 16px;
    }}
    .eyebrow {{
      color: #69717c;
      font-size: 12px;
      letter-spacing: 0;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .score {{
      border-radius: 6px;
      min-width: 90px;
      padding: 10px 12px;
      text-align: center;
    }}
    .good {{
      background: #dff4e6;
      color: #116238;
    }}
    .watch {{
      background: #fff0c2;
      color: #7a4b00;
    }}
    .urgent {{
      background: #ffe0df;
      color: #9b2320;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}
    @media (max-width: 680px) {{
      .audit-head, .grid {{
        display: block;
      }}
      .score {{
        display: inline-block;
        margin-top: 8px;
      }}
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>"""


def to_html(label: str, data: AuditInput, result: AuditResult) -> str:
    body = "\n".join(
        [
            "<h1>Listing Audit Report</h1>",
            '<p class="subtle">Client-ready ecommerce listing review.</p>',
            _single_audit_html(label, data, result),
        ]
    )
    return html_document("Listing Audit Report", body)


def result_to_dict(result: AuditResult) -> dict[str, object]:
    return {
        "score": result.score,
        "title_score": result.title_score,
        "description_score": result.description_score,
        "economics_score": result.economics_score,
        "risks": result.risks,
        "actions": result.actions,
        "economics": {
            "marketplace_fee": result.economics.marketplace_fee,
            "expected_refund_cost": result.economics.expected_refund_cost,
            "gross_profit": result.economics.gross_profit,
            "contribution_profit": result.economics.contribution_profit,
            "gross_margin_rate": result.economics.gross_margin_rate,
            "break_even_ad_spend": result.economics.break_even_ad_spend,
        },
    }


def _parse_float(row: dict[str, str], field: str, row_number: int) -> float:
    raw_value = (row.get(field) or "").strip()
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise SystemExit(f"CSV row {row_number}: {field} must be a number.") from exc
    if value < 0:
        raise SystemExit(f"CSV row {row_number}: {field} cannot be negative.")
    return value


def input_from_csv_row(row: dict[str, str], row_number: int) -> AuditInput:
    missing = [field for field in CSV_REQUIRED_FIELDS if not (row.get(field) or "").strip()]
    if missing:
        raise SystemExit(f"CSV row {row_number}: missing required fields: {', '.join(missing)}.")

    price = _parse_float(row, "price", row_number)
    if price <= 0:
        raise SystemExit(f"CSV row {row_number}: price must be greater than zero.")

    return AuditInput(
        title=row["title"].strip(),
        description=row["description"].strip(),
        price=price,
        cost=_parse_float(row, "cost", row_number),
        shipping=_parse_float(row, "shipping", row_number),
        ad_spend=_parse_float(row, "ad_spend", row_number),
        marketplace_fee_rate=_parse_float(row, "marketplace_fee_rate", row_number),
        refund_rate=_parse_float(row, "refund_rate", row_number),
    )


def audit_csv(path: Path) -> list[tuple[str, AuditInput, AuditResult]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("CSV file is empty.")

        missing_columns = [field for field in CSV_REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing_columns:
            raise SystemExit(f"CSV is missing required columns: {', '.join(missing_columns)}.")

        audits = []
        for row_number, row in enumerate(reader, start=2):
            data = input_from_csv_row(row, row_number)
            label = (row.get("sku") or row.get("id") or data.title).strip()
            audits.append((label, data, audit_listing(data)))

    if not audits:
        raise SystemExit("CSV file has no listing rows.")
    return audits


def batch_summary_lines(audits: list[tuple[str, AuditInput, AuditResult]]) -> list[str]:
    average_score = sum(result.score for _, _, result in audits) / len(audits)
    lowest_label, _, lowest_result = min(audits, key=lambda audit: audit[2].score)
    negative_profit = [
        label for label, _, result in audits if result.economics.contribution_profit <= 0
    ]
    priority_items = sorted(
        audits,
        key=lambda audit: (audit[2].score, audit[2].economics.contribution_profit),
    )[:3]

    lines = [
        "Executive summary",
        f"- Average score: {average_score:.1f}/100",
        f"- Lowest scoring listing: {lowest_label} ({lowest_result.score}/100)",
        f"- Listings at or below break-even after ads: {len(negative_profit)}",
        "",
        "Priority list",
    ]
    for index, (label, _, result) in enumerate(priority_items, start=1):
        top_action = result.actions[0] if result.actions else "Review images, offer, and traffic quality."
        lines.append(
            f"{index}. {label}: {result.score}/100, "
            f"{_money(result.economics.contribution_profit)} contribution profit. {top_action}"
        )
    return lines


def csv_to_markdown(audits: list[tuple[str, AuditInput, AuditResult]]) -> str:
    sections = ["Bulk Listing Audit", f"Listings audited: {len(audits)}", "", *batch_summary_lines(audits)]
    for label, data, result in audits:
        sections.extend(
            [
                "",
                f"## {label}",
                f"Title: {data.title}",
                "",
                to_markdown(result),
            ]
        )
    return "\n".join(sections)


def csv_to_json(audits: list[tuple[str, AuditInput, AuditResult]]) -> str:
    return json.dumps(
        [
            {
                "label": label,
                "title": data.title,
                "audit": result_to_dict(result),
            }
            for label, data, result in audits
        ],
        indent=2,
    )


def csv_to_html(audits: list[tuple[str, AuditInput, AuditResult]]) -> str:
    summary = "\n".join(f"<li>{escape(line.lstrip('- '))}</li>" for line in batch_summary_lines(audits))
    cards = "\n".join(
        _single_audit_html(label, data, result) for label, data, result in audits
    )
    body = "\n".join(
        [
            "<h1>Bulk Listing Audit Report</h1>",
            f'<p class="subtle">Listings audited: {len(audits)}</p>',
            '<section class="summary">',
            "<h2>Executive summary</h2>",
            f"<ul>{summary}</ul>",
            "</section>",
            cards,
        ]
    )
    return html_document("Bulk Listing Audit Report", body)


def audit_row(label: str, data: AuditInput, result: AuditResult) -> dict[str, str | int | float]:
    return {
        "label": label,
        "title": data.title,
        "score": result.score,
        "title_score": result.title_score,
        "description_score": result.description_score,
        "economics_score": result.economics_score,
        "contribution_profit": result.economics.contribution_profit,
        "break_even_ad_spend": result.economics.break_even_ad_spend,
        "gross_margin_rate": result.economics.gross_margin_rate,
        "top_action": result.actions[0] if result.actions else "",
        "risks": "; ".join(result.risks),
    }


def audits_to_csv(audits: list[tuple[str, AuditInput, AuditResult]]) -> str:
    output = StringIO()
    fieldnames = [
        "label",
        "title",
        "score",
        "title_score",
        "description_score",
        "economics_score",
        "contribution_profit",
        "break_even_ad_spend",
        "gross_margin_rate",
        "top_action",
        "risks",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for label, data, result in audits:
        writer.writerow(audit_row(label, data, result))
    return output.getvalue().rstrip("\n")


def write_or_print(content: str, output_path: Path | None) -> None:
    if output_path is None:
        print(content)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{content}\n", encoding="utf-8")
    print(f"Wrote audit report to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit ecommerce listing copy and economics.")
    parser.add_argument("--sample", action="store_true", help="Run the built-in sample audit.")
    parser.add_argument("--input-csv", type=Path, help="Audit multiple listings from a CSV file.")
    parser.add_argument("--output", type=Path, help="Write the audit report to a file.")
    parser.add_argument("--title", default="", help="Product title.")
    parser.add_argument("--description", default="", help="Product description or bullet text.")
    parser.add_argument("--price", type=float, default=0.0, help="Sale price.")
    parser.add_argument("--cost", type=float, default=0.0, help="Product landed cost.")
    parser.add_argument("--shipping", type=float, default=0.0, help="Seller-paid shipping cost.")
    parser.add_argument("--ad-spend", type=float, default=0.0, help="Ad spend per order.")
    parser.add_argument(
        "--marketplace-fee-rate",
        type=float,
        default=0.15,
        help="Marketplace fee rate as a decimal.",
    )
    parser.add_argument("--refund-rate", type=float, default=0.03, help="Refund rate as a decimal.")
    parser.add_argument("--format", choices=("markdown", "json", "csv", "html"), default="markdown")
    return parser.parse_args()


def input_from_args(args: argparse.Namespace) -> AuditInput:
    if args.sample:
        return SAMPLE
    if not args.title.strip() or not args.description.strip():
        raise SystemExit("Provide --title and --description, or use --sample.")
    if args.price <= 0:
        raise SystemExit("Provide a positive --price.")
    if min(args.cost, args.shipping, args.ad_spend, args.marketplace_fee_rate, args.refund_rate) < 0:
        raise SystemExit("Costs, rates, and ad spend cannot be negative.")
    return AuditInput(
        title=args.title,
        description=args.description,
        price=args.price,
        cost=args.cost,
        shipping=args.shipping,
        ad_spend=args.ad_spend,
        marketplace_fee_rate=args.marketplace_fee_rate,
        refund_rate=args.refund_rate,
    )


def main() -> int:
    args = parse_args()
    if args.input_csv:
        audits = audit_csv(args.input_csv)
        if args.format == "json":
            content = csv_to_json(audits)
        elif args.format == "csv":
            content = audits_to_csv(audits)
        elif args.format == "html":
            content = csv_to_html(audits)
        else:
            content = csv_to_markdown(audits)
        write_or_print(content, args.output)
        return 0

    data = input_from_args(args)
    result = audit_listing(data)
    if args.format == "json":
        content = to_json(result)
    elif args.format == "csv":
        content = audits_to_csv([("single-listing", data, result)])
    elif args.format == "html":
        content = to_html("single-listing", data, result)
    else:
        content = to_markdown(result)
    write_or_print(content, args.output)
    return 0
