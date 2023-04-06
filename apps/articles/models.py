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

class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.created_at} на статью "{self.article.name}"'












 

 


 
 

 
 
 
 
 
 
 
 

 
 
 
 
 
 
 

 
 
 

 
 

 
 
 
 