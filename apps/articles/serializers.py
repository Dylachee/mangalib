from rest_framework import serializers
from .models import RelatedModel , Article , Review , Author
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedModel
        fields = ('id', 'name')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class MyModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    related_models = RelatedModelSerializer(many=True, read_only=True)
    

    class Meta:
        model = Article
        fields = ('id', 'name', 'description', 'author' ,'created_at', 'related_models', 'image')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'article', 'text', 'created_at']


























