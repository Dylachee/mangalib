from rest_framework import serializers
from .models import Comment , RelatedModel , Article , Rating

class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedModel
        fields = ('id', 'name')

class MyModelSerializer(serializers.ModelSerializer):
    related_models = RelatedModelSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'name', 'description', 'created_at', 'related_models')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'text', 'created_at', 'updated_at', 'sub_comment')
        read_only_fields = ['article']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'article', 'rate')
        read_only_fields = ['user', 'article']
        
    def validate(self, attrs):
        user = self.context.get('request').user
        article = self.context.get('article')
        rate = Rating.objects.filter(user=user, article=article).exists()
        if rate:
            raise serializers.ValidationError({'message': 'Rate already exists'})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    