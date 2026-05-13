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

STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "or",
    "the",
    "to",
    "with",
}

USE_CASE_WORDS = {
    "daily",
    "gym",
    "home",
    "kitchen",
    "office",
    "outdoor",
    "travel",
    "work",
}

SPEC_WORDS = {
    "blade",
    "blades",
    "cup",
    "cups",
    "pack",
    "set",
    "six",
    "usb",
}

ACRONYM_WORDS = {
    "bpa",
    "led",
    "usb",
    "uv",
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
class RewriteSuggestions:
    title: str
    bullets: list[str]


@dataclass(frozen=True)
class AuditResult:
    score: int
    title_score: int
    description_score: int
    economics_score: int
    risks: list[str]
    actions: list[str]
    economics: Economics
    rewrite: RewriteSuggestions


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower())


def _contains_phrase(text: str, phrase: str) -> bool:
    return phrase in text.lower()


def _dedupe_tokens(text: str, limit: int) -> list[str]:
    seen = set()
    words = []
    risky_tokens = {token for phrase in RISK_WORDS for token in _tokens(phrase)}
    for word in _tokens(text):
        if word in STOP_WORDS or word in risky_tokens or word in seen:
            continue
        seen.add(word)
        words.append(word)
        if len(words) == limit:
            break
    return words


def _title_case(words: list[str]) -> str:
    return " ".join(
        word.upper() if word in ACRONYM_WORDS or any(character.isdigit() for character in word) else word.title()
        for word in words
    )


def suggest_rewrite(data: AuditInput, economics: Economics, risks: list[str]) -> RewriteSuggestions:
    keywords = _dedupe_tokens(f"{data.title} {data.description}", 20)
    title_words = _dedupe_tokens(data.title, 8)
    product_words = [
        word
        for word in title_words
        if word not in BENEFIT_WORDS
        and word not in USE_CASE_WORDS
        and word not in SPEC_WORDS
        and not any(character.isdigit() for character in word)
    ][:4]
    benefit_words = [word for word in keywords if word in BENEFIT_WORDS][:2]
    use_case_words = [word for word in keywords if word in USE_CASE_WORDS and word not in benefit_words][:2]

    product_phrase = _title_case(product_words) or _title_case(keywords[:4]) or "Featured Product"
    benefit_phrase = f"{_title_case(benefit_words)} " if benefit_words else ""
    use_case = _title_case(use_case_words[:3]) or "Everyday Use"
    title = f"{benefit_phrase}{product_phrase} for {use_case}"
    if len(title) < 45:
        title = f"{title} with Easy Setup"
    if len(title) > 120:
        title = title[:117].rstrip() + "..."

    trust_note = "Add warranty, review, testing, or return details before scaling traffic."
    if any(word in _tokens(data.description) for word in TRUST_WORDS):
        trust_note = "Lead with the strongest proof point, then support it with specs and use cases."

    margin_note = (
        "Keep ad spend below the break-even ad spend until conversion is proven."
        if economics.contribution_profit > 0
        else "Fix price, landed cost, or ad spend before increasing paid traffic."
    )
    risk_note = (
        "Replace risky absolute claims with specific, provable benefits."
        if risks
        else "Keep claims specific and easy for a marketplace reviewer to verify."
    )

    bullets = [
        f"Position the offer around {product_phrase.lower()} and one clear buyer use case.",
        trust_note,
        f"{margin_note} Current break-even ad spend is ${economics.break_even_ad_spend:.2f}.",
        risk_note,
    ]
    return RewriteSuggestions(title=title, bullets=bullets)


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
    rewrite = suggest_rewrite(data, economics, risks)

    return AuditResult(
        score=score,
        title_score=title_score,
        description_score=description_score,
        economics_score=economics_score,
        risks=risks,
        actions=actions[:5],
        economics=economics,
        rewrite=rewrite,
    )
