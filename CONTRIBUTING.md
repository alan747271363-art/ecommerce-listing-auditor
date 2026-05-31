# Contributing

Thanks for considering a contribution. This project is intentionally small and
practical: it helps ecommerce sellers audit listing copy and simple unit
economics without connecting to private store systems.

## Good First Contributions

- Improve sample CSV rows or sample reports.
- Add tests for edge cases in scoring or CSV parsing.
- Clarify README instructions.
- Add marketplace-neutral risk words that are easy to justify.
- Improve HTML or Markdown report readability without adding heavy dependencies.

## Local Development

```bash
python -m pip install -e .
python -m pip install pytest ruff
python -m compileall src tests
python -m pytest
python -m ruff check src tests
python -m listing_auditor --sample
```

## Pull Request Checklist

- Explain the seller problem or maintainer problem the change solves.
- Keep the change focused and easy to review.
- Add or update tests when behavior changes.
- Update sample reports when output changes.
- Do not add dependencies unless the benefit is clear and documented.
- Do not include private marketplace data, customer data, API keys, or account
  screenshots.

## Safety Boundaries

This project should remain safe to run offline. It must not require passwords,
payment credentials, ad account access, marketplace tokens, or customer data.

If you are unsure whether a change affects seller safety or business decisions,
open an issue first and describe the risk in plain language.
