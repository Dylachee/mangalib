from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class RelatedModel(models.Model):
    mymodel = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


