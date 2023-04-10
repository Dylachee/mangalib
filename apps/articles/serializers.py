from rest_framework import serializers
from .models import RelatedModel , Article , Review , Author , Tag
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.validators import MinValueValidator, MaxValueValidator

class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedModel
        fields = ('id', 'name')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
class MyModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    related_models = RelatedModelSerializer(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    tags = TagSerializer(many=True, read_only=True)


    class Meta:
        model = Article
        fields = ('id', 'name', 'description', 'author', 'tags' ,'created_at', 'related_models', 'image')

    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'article', 'text', 'created_at']



















