def convert_price_text_to_num(raw_price_text: str, replace_str_list: list = None, convert_to_int: bool = True):
    fixed_price_text = raw_price_text.replace(" ", "").replace("вЂ‰", "")

    if replace_str_list is None:
        replace_str_list = ["в‚Ѕ"]

    for s in replace_str_list:
        fixed_price_text = fixed_price_text.replace(s, "")

    if convert_to_int:
        return int(float(fixed_price_text))

    return float(fixed_price_text)


def trim_text_after_symbol(text, symbol) -> str:
    trimmed_text = text.split(symbol)[0]
    return trimmed_text


def get_url_without_protocol(url):
    try:
        from urllib.parse import urlparse
    except Exception:
        return url
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path
