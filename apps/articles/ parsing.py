import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from apps.articles.models import Article , Review

def parse_articles():
    url = 'http://127.0.0.1:8000/articles'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', {'class': 'article'})
        for article in articles:
            name = article.find('h2').text.strip()
            description = article.find('div', {'class': 'description'}).text.strip()
            article_slug = slugify(name)
            # проверяем, существует ли статья с таким же slug, если нет, то создаем новую статью
            if not Article.objects.filter(slug=article_slug).exists():
                Article.objects.create(name=name, description=description, slug=article_slug)
            # получаем отзывы для данной статьи
            parse_reviews(name, article_slug)

def parse_reviews(article_name, article_slug):
    url = 'http://127.0.0.1:8000/articles/reviews'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 'review'})
        for review in reviews:
            text = review.find('p').text.strip()
            rating = review.find('div', {'class': 'rating'}).text.strip()
            # проверяем, существует ли отзыв с таким же текстом, если нет, то создаем новый отзыв
            if not Review.objects.filter(text=text).exists():
                article = Article.objects.get(name=article_name)
                Review.objects.create(article=article, text=text, rating=rating)
