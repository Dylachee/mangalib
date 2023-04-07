from rest_framework import serializers
from .models import RelatedModel , Article , Review
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedModel
        fields = ('id', 'name')

class MyModelSerializer(serializers.ModelSerializer):
    related_models = RelatedModelSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'name', 'description', 'created_at', 'related_models')


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, min_value=0.0, max_value=5.0)
    class Meta:
        model = Review
        fields = ['id', 'article', 'text', 'created_at', 'rating']




























