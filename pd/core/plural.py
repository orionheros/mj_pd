#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/plural.py

from .plural_rules import pl, en

PLURAL_RULES = {
    "pl": pl.plural_form,
    "en": en.plural_form,
}

def get_plural_form(lang: str, n: int) -> str:
    try:
        return PLURAL_RULES[lang](n)
    except KeyError:
        return PLURAL_RULES["en"](n) # Fallback to English
    