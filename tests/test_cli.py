import json

from listing_auditor.cli import SAMPLE, to_json, to_markdown
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
