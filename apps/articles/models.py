from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField



User = get_user_model()

class Article(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.name

class RelatedModel(models.Model):
    mymodel = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


from django.db import models
from .models import Article

class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.created_at} на статью "{self.article.name}"'


class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайк'
        unique_together = ('user', 'article')

    def __str__(self):
        return f'Liked by {self.user.username}'



class Rating(models.Model):
    RATES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    rate = models.PositiveSmallIntegerField(choices=RATES)
    # rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ['user', 'article']
 
 