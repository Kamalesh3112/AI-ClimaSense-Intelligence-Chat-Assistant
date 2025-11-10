"""
Formatter for concise vs detailed responses.
"""
def format_response(raw_text: str, mode: str = "concise", max_chars_concise: int = 300):
    if mode == "concise":
        if len(raw_text) <= max_chars_concise:
            return raw_text
        return raw_text[:max_chars_concise].rsplit(".", 1)[0] + "..."
    else:
        return raw_text