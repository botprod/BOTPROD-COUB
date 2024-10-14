from urllib.parse import parse_qs, unquote, urlparse

def parse_query(query: str):
    if '#' in query:
        url_part, fragment_part = query.split('#', 1)
    else:
        url_part = query
        fragment_part = ''

    parsed_url = urlparse(url_part)
    parsed_url_query = parse_qs(parsed_url.query)
    start_param_main = parsed_url_query.get('tgWebAppStartParam', [''])[0]

    fragment_part_unquoted = unquote(fragment_part)
    parsed_fragment = parse_qs(fragment_part_unquoted)

    start_param_fragment = parsed_fragment.get('start_param', [''])[0]
    start_param = start_param_fragment or start_param_main

    tg_web_app_data = parsed_fragment.get('tgWebAppData', [''])[0]

    result_data = {
        'user': '',
        'chat_instance': '',
        'chat_type': '',
        'start_param': start_param,
        'auth_date': '',
        'hash': ''
    }

    if tg_web_app_data:
        tg_web_app_data_unquoted = unquote(tg_web_app_data)
        tg_web_app_data_parsed = parse_qs(tg_web_app_data_unquoted)

        user_data = tg_web_app_data_parsed.get('user', [''])[0]
        result_data['user'] = user_data

        result_data['chat_instance'] = parsed_fragment.get('chat_instance', [''])[0]
        result_data['chat_type'] = parsed_fragment.get('chat_type', [''])[0]
        result_data['auth_date'] = parsed_fragment.get('auth_date', [''])[0]
        result_data['hash'] = parsed_fragment.get('hash', [''])[0]
    else:
        print("Warning: 'tgWebAppData' key not found in the fragment")

    ordered_result = {
        'user': result_data['user'],
        'chat_instance': result_data['chat_instance'],
        'chat_type': result_data['chat_type'],
        'start_param': result_data['start_param'],
        'auth_date': result_data['auth_date'],
        'hash': result_data['hash'],
    }
    return ordered_result, query.split("#tgWebAppData=")[1].split("&tgWebAppVersion=6.7")[0], query