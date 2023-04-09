from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import status


User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100 ,null=True)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
    
    def __str__(self) -> str:
        return self.title
    
class Article(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    tag = models.ManyToManyField("Tag", related_name='articles')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
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



 

 


 
 

 
 
 
 
 
 
 
 

 
 
 
 
 
 
 

 
 
 

 
 

 
 
 
 