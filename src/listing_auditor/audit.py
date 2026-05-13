from __future__ import annotations

from dataclasses import dataclass
import re


BENEFIT_WORDS = {
    "easy",
    "portable",
    "fast",
    "durable",
    "rechargeable",
    "waterproof",
    "lightweight",
    "comfortable",
    "travel",
    "safe",
}

TRUST_WORDS = {
    "warranty",
    "guarantee",
    "certified",
    "bpa-free",
    "reviews",
    "rating",
    "tested",
    "authentic",
}

RISK_WORDS = {
    "cure",
    "guaranteed results",
    "miracle",
    "best ever",
    "free money",
    "100% safe",
    "permanent",
}


@dataclass(frozen=True)
class AuditInput:
    title: str
    description: str
    price: float
    cost: float
    shipping: float
    ad_spend: float
    marketplace_fee_rate: float
    refund_rate: float


@dataclass(frozen=True)
class Economics:
    marketplace_fee: float
    expected_refund_cost: float
    gross_profit: float
    contribution_profit: float
    gross_margin_rate: float
    break_even_ad_spend: float


@dataclass(frozen=True)
class AuditResult:
    score: int
    title_score: int
    description_score: int
    economics_score: int
    risks: list[str]
    actions: list[str]
    economics: Economics


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower())


def _contains_phrase(text: str, phrase: str) -> bool:
    return phrase in text.lower()


def score_title(title: str) -> tuple[int, list[str]]:
    words = _tokens(title)
    actions: list[str] = []
    score = 35

    if len(title) < 35:
        score -= 12
        actions.append("Make the title more specific; include product type, key feature, and use case.")
    elif len(title) > 120:
        score -= 10
        actions.append("Shorten the title so the main value is visible on mobile search results.")

    if len(set(words)) < max(4, len(words) * 0.65):
        score -= 8
        actions.append("Reduce repeated words in the title and use the space for buyer intent keywords.")

    if not any(word in BENEFIT_WORDS for word in words):
        score -= 7
        actions.append("Add buyer-specific keywords that match search intent.")

    return max(0, min(35, score)), actions


def score_description(description: str) -> tuple[int, list[str]]:
    words = _tokens(description)
    actions: list[str] = []
    score = 35

    if len(words) < 35:
        score -= 12
        actions.append("Expand the description with benefits, specs, use cases, and what is included.")

    if not any(word in BENEFIT_WORDS for word in words):
        score -= 8
        actions.append("Add clear benefit language, not only feature names.")

    if not any(word in TRUST_WORDS for word in words):
        score -= 7
        actions.append("Add 2-3 proof points such as warranty, review count, certification, or guarantee.")

    if not any(word in words for word in ("shipping", "returns", "refund", "delivery")):
        score -= 4
        actions.append("Mention shipping, delivery, returns, or after-sale expectations.")

    return max(0, min(35, score)), actions


def calculate_economics(data: AuditInput) -> Economics:
    marketplace_fee = data.price * data.marketplace_fee_rate
    expected_refund_cost = data.price * data.refund_rate
    gross_profit = data.price - data.cost - data.shipping - marketplace_fee - expected_refund_cost
    contribution_profit = gross_profit - data.ad_spend
    gross_margin_rate = gross_profit / data.price if data.price else 0
    return Economics(
        marketplace_fee=round(marketplace_fee, 2),
        expected_refund_cost=round(expected_refund_cost, 2),
        gross_profit=round(gross_profit, 2),
        contribution_profit=round(contribution_profit, 2),
        gross_margin_rate=round(gross_margin_rate, 4),
        break_even_ad_spend=round(max(0, gross_profit), 2),
    )


def score_economics(economics: Economics) -> tuple[int, list[str]]:
    actions: list[str] = []
    score = 30

    if economics.gross_margin_rate < 0.25:
        score -= 14
        actions.append("Raise price, reduce landed cost, or lower fees before scaling ads.")
    elif economics.gross_margin_rate < 0.4:
        score -= 7
        actions.append("Margin is workable but thin; keep ad tests small until conversion is proven.")

    if economics.contribution_profit <= 0:
        score -= 10
        actions.append("Reduce ad spend or improve conversion before scaling this listing.")

    if economics.expected_refund_cost > economics.gross_profit * 0.25:
        score -= 4
        actions.append("Keep refund assumptions visible because they materially affect contribution profit.")

    return max(0, min(30, score)), actions


def find_risks(text: str) -> list[str]:
    risks = []
    for phrase in sorted(RISK_WORDS):
        if _contains_phrase(text, phrase):
            risks.append(f"Potential policy or trust risk phrase: {phrase}")
    return risks


def audit_listing(data: AuditInput) -> AuditResult:
    title_score, title_actions = score_title(data.title)
    description_score, description_actions = score_description(data.description)
    economics = calculate_economics(data)
    economics_score, economics_actions = score_economics(economics)
    risks = find_risks(f"{data.title}\n{data.description}")
    risk_penalty = min(10, len(risks) * 4)

    score = max(0, min(100, title_score + description_score + economics_score - risk_penalty))
    actions = title_actions + description_actions + economics_actions
    if risks:
        actions.append("Remove or soften risky claims before marketplace or ad review.")
    if not actions:
        actions.append("Listing is in good shape; test images, price points, and first-review strategy next.")

    return AuditResult(
        score=score,
        title_score=title_score,
        description_score=description_score,
        economics_score=economics_score,
        risks=risks,
        actions=actions[:5],
        economics=economics,
    )
