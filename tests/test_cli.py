import json
from pathlib import Path

import pytest

from listing_auditor.cli import SAMPLE, audit_csv, csv_to_json, csv_to_markdown, to_json, to_markdown
from listing_auditor.audit import audit_listing


def test_markdown_output_contains_actions_and_score() -> None:
    output = to_markdown(audit_listing(SAMPLE))

    assert "Listing Audit" in output
    assert "Score:" in output
    assert "Top actions" in output


def test_json_output_is_valid_json() -> None:
    parsed = json.loads(to_json(audit_listing(SAMPLE)))

    assert parsed["score"] > 0
    assert "economics" in parsed


def test_csv_audit_reads_multiple_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "listings.csv"
    csv_path.write_text(
        "\n".join(
            [
                "sku,title,description,price,cost,shipping,ad_spend,marketplace_fee_rate,refund_rate",
                (
                    "BLENDER-1,Portable Blender USB Rechargeable 500ml,"
                    "Portable BPA-free blender with warranty and easy cleaning for travel,"
                    "29.99,9.40,3.20,5.00,0.15,0.04"
                ),
                (
                    "MUG-1,Leakproof Travel Mug Stainless Steel,"
                    "Durable travel mug with warranty safe materials and fast delivery,"
                    "24.00,6.00,3.00,4.00,0.12,0.03"
                ),
            ]
        ),
        encoding="utf-8",
    )

    audits = audit_csv(csv_path)

    assert len(audits) == 2
    assert audits[0][0] == "BLENDER-1"
    assert audits[0][2].score > 0

    markdown = csv_to_markdown(audits)
    assert "Bulk Listing Audit" in markdown
    assert "BLENDER-1" in markdown

    parsed = json.loads(csv_to_json(audits))
    assert parsed[1]["label"] == "MUG-1"
    assert parsed[1]["audit"]["score"] > 0


def test_csv_audit_rejects_missing_required_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "bad-listings.csv"
    csv_path.write_text("title,price\nTravel Mug,24.00\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="missing required columns"):
        audit_csv(csv_path)
