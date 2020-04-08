

def clean_html(text: str) -> str:
    import re
    import html
    text = re.sub(r'<.*?>', '', text)
    text = html.unescape(text)
    return text


def strip_weird_t(text: str) -> str:
    """
    =T("21212") -> 21212
    """
    text = text[4:]
    text = text[:-2]
    return text
