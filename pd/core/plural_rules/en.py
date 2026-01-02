#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/plural_rules/en.py

def plural_form(n: int) -> str:
    return "one" if n == 1 else "other"
