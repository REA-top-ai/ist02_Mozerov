import requests

base_url = 'https://newsapi.org/v2/'

def _make_requests(endpoint: str, api_key: str, params: dict[str, str] = None) -> dict:
    url = f"{base_url}/{endpoint}"
    default_params = {'apiKey': api_key}
    if params:
        default_params.update(params)
    try:
        response = requests.get(url, params=default_params, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при запросе к NewsAPI {endpoint}: {e}")
    except ValueError as e:
        raise Exception(f"Ошибка при парсинге json {endpoint}: {e}")

def get_top_headlines(api_key: str, q: str = None, country: str = None,
                      category: str = None, sources: str = None,
                      page_size: int = None, page: int = None) -> dict:
    params = {
        'q': q, 'country': country, 'category': category, 'sources': sources,
        'pageSize': page_size, 'page': page
    }
    final_params = {key: value for key, value in params.items() if value is not None}
    return _make_requests('top-headlines', api_key, final_params)

def get_everything(api_key: str, q: str = None, search_in: str = None,
                   sources: str = None, domains: str = None,
                   from_date: str = None, to_date: str = None,
                   language: str = None, sort_by: str = None,
                   page_size: int = None, page: int = None) -> dict:
    params = {
        'q': q, 'searchIn': search_in, 'sources': sources, 'domains': domains,
        'from': from_date, 'to': to_date, 'language': language, 'sortBy': sort_by,
        'pageSize': page_size, 'page': page
    }
    final_params = {key: value for key, value in params.items() if value is not None}
    return _make_requests('everything', api_key, final_params)

def get_sources(api_key: str, category: str = None, language: str = None,
                country: str = None) -> dict:
    params = {
        'category': category,
        'language': language,
        'country': country
    }
    final_params = {key: value for key, value in params.items() if value is not None}
    return _make_requests('sources', api_key, final_params)