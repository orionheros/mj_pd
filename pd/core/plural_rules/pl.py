#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/plural_rules/pl.py

def plural_form(n: int) -> str:
    if n == 1:
        return "one"
    else:
        return "few"