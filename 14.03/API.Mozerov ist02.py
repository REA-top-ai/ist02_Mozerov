import requests
import json
api_key = "a8f1e1524e8d41ecb1e47e2cc063df50"
params = {'apiKey': api_key, 'pageSize': 100, 'q': 'Python'}
r = requests.get('https://newsapi.org/v2/everything', params=params)


if r.status_code == 200:
    data = r.json()

    articles = data.get('articles', [])
    if not articles:
        print('Статьи не найдены')
    else:
        filtered_articles = []
        for article in articles:
            title = article.get('title')
            description = article.get('description')
            url = article.get('url')

            if title and description and url:
                if len(description) >= 50:
                    published = article.get('publishedAt', 'Дата неизвестна')
                    author = article.get('author', 'Автор неизвестен')

                    filtered_articles.append({'title': title, 'description': description, 'published': published, 'author': author})
        top_articles = filtered_articles[:50]
        if not top_articles:
                        print('Не найдено подходящих под условия статей')
        else:
            print(json.dumps(top_articles, ensure_ascii=False, indent=2))

else:
        print(f'Ошибка {r.status_code}: {r.text}')