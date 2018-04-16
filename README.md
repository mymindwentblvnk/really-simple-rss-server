# really-simple-rss-server
A super slim (100 lines of code) RSS (Atom) server based on Flask framework and SQLAlchemy.

## Run Server

```bash
python app.py
```

## Payload

```python
# Here you can also add:
# 'content'
# 'updated' (if not set it's datetime.now())
# 'category'

payload = {
  'title': 'Schalke beats Dortmund 2-0 for 1st Ruhr derby win since 2014',
  'link': 'https://mainichi.jp/english/articles/20180416/p2g/00m/0sp/044000c',
  'summary': 'Schalke beat rival Borussia Dortmund 2-0 in the Ruhr derby on Sunday to consolidate second place in the Bundesliga and take a giant step toward guaranteeing a Champions League spot.'
}
```

## POST

```python
domain = 'news'  # The domain which this article belongs to
filter = 'sport'  # A possibility to filter for articles
url = 'http://localhost:5000/feed/{}/{}'.format(domain, filter)
requests.post(url, json=payload)
```

## GET

![Example Feed](https://i.imgur.com/zuJjbly.png)
