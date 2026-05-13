from listing_auditor.audit import AuditInput, audit_listing


def test_audit_scores_stronger_listing_higher_than_weak_listing() -> None:
    strong = AuditInput(
        title="Portable Blender USB Rechargeable 500ml Smoothie Maker for Travel",
        description=(
            "Portable BPA-free blender with USB-C charging, six blades, easy cleaning, "
            "travel cup, warranty, and safe design for smoothies at the gym or office."
        ),
        price=34.99,
        cost=8.0,
        shipping=3.0,
        ad_spend=4.0,
        marketplace_fee_rate=0.15,
        refund_rate=0.02,
    )
    weak = AuditInput(
        title="Blender",
        description="Best ever miracle blender with guaranteed results.",
        price=19.99,
        cost=14.0,
        shipping=4.0,
        ad_spend=5.0,
        marketplace_fee_rate=0.15,
        refund_rate=0.1,
    )

    assert audit_listing(strong).score > audit_listing(weak).score


def test_audit_flags_risky_claims() -> None:
    data = AuditInput(
        title="Miracle Acne Device",
        description="This device will cure skin problems with guaranteed results.",
        price=49.0,
        cost=10.0,
        shipping=5.0,
        ad_spend=7.0,
        marketplace_fee_rate=0.15,
        refund_rate=0.05,
    )

    result = audit_listing(data)

    assert result.risks
    assert any("cure" in risk for risk in result.risks)


def test_audit_calculates_break_even_ad_spend() -> None:
    data = AuditInput(
        title="Portable Travel Mug Stainless Steel Leakproof Coffee Cup",
        description="Durable travel mug with warranty, leakproof lid, easy cleaning, and safe materials.",
        price=20.0,
        cost=5.0,
        shipping=2.0,
        ad_spend=3.0,
        marketplace_fee_rate=0.1,
        refund_rate=0.05,
    )

    result = audit_listing(data)

    assert result.economics.break_even_ad_spend == 10.0
    assert result.economics.contribution_profit == 7.0
