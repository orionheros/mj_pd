#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/i18n.py

import json

from dataclasses import dataclass

from pd.core.plural import get_plural_form
from pd.platform.resources import resource_path

class I18n:
    def __init__(self, language: str):
        self.language = language
        self.translations = self._load_translations(language)

    def _load_translations(self, language: str) -> dict:
        path = resource_path(f"pd/assets/i18n/{language}.json")
        if not path.exists():
            raise RuntimeError(f"Missing language file: {language}.json")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def t(self, key: str) -> str:
        """
        Translate a given key to the current language.
        """
        node = self.translations
        for part in key.split('.'):
            if not isinstance(node, dict) or part not in node:
                return f"[{key}]"
            node = node[part]
        if not isinstance(node, str):
            return f"[{key}]"
        
        return node
    
    def current_language(self) -> str:
        code = self.language
        return code
    
    def plural(self, key: str, n: int, **kwargs) -> str:
        form = get_plural_form(self.language, n)
        template = self.t(f"{key}.{form}")
        return template.format(n=n, **kwargs)
    
@dataclass(frozen=True)
class Language:
    code: str           # "pl", "en"
    name: str           # "Polish", "English"
    native_name: str    # "Polski", "English"

AVAILABLE_LANGUAGES = [
    Language("pl", "Polish", "Polski"),
    Language("en", "English", "English"),
]