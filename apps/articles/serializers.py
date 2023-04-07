from rest_framework import serializers
from .models import RelatedModel , Article , Review, Tag, Like, Rating
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Avg

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
    class Meta:
        model = Review
        fields = ['id', 'article', 'text', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ('user',)

class ArticleListSerializer(serializers.ListSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'tag', 'user')



class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name='get_likes_count')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['user', 'id']
        list_serializer_class = ArticleListSerializer

    def get_likes_count(self, instance) -> int:
        return Like.objects.filter(article=instance).count()

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['reviews'] = ReviewSerializer(instance.review.all(), many=True).data
        representation['tag'] = [tag.title for tag in instance.tag.all()]
        representation['rating'] = instance.ratings.aggregate(Avg('rate'))['rate__avg']
        representation['liked_users'] = LikeSerializer(instance.likes.all(), many=True).data
        # aggregate() -> {'rate__avg': 3.8}
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'article', 'rate')
        read_only_fields = ['user', 'article']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=('user', 'article'),
        #         message='Вы уже ставили рейтинг!'
        #     )
        # ]

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