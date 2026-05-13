from __future__ import annotations

import argparse
import csv
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


def csv_to_markdown(audits: list[tuple[str, AuditInput, AuditResult]]) -> str:
    sections = ["Bulk Listing Audit", f"Listings audited: {len(audits)}"]
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit ecommerce listing copy and economics.")
    parser.add_argument("--sample", action="store_true", help="Run the built-in sample audit.")
    parser.add_argument("--input-csv", type=Path, help="Audit multiple listings from a CSV file.")
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
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
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
        print(csv_to_json(audits) if args.format == "json" else csv_to_markdown(audits))
        return 0

    result = audit_listing(input_from_args(args))
    print(to_json(result) if args.format == "json" else to_markdown(result))
    return 0
