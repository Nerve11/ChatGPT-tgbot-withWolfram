import json

def load_translations(language: str) -> dict:
    with open(f"i18n/{language}.json", "r", encoding="utf-8") as file:
        return json.load(file)

def translate(message_key: str, language: str) -> str:
    translations = load_translations(language)
    return translations.get(message_key, message_key)
