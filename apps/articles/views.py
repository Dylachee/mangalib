from django.shortcuts import render
from rest_framework import generics , viewsets , filters , status , serializers
from .models import Article , Review , Author , Tag
from .serializers import MyModelSerializer, ReviewSerializer, AuthorSerializer , TagSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class MyModelList(ModelViewSet, Article):

    queryset = Article.objects.all() 
    serializer_class = MyModelSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @cache_page(60 * 15) # кэшируем детальную информацию на 15 минут
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_context(self):
        """  
        Метод для добавления дополнительных данных в сериалайзеры
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_permissions(self):
        """  
        Метод отвечающий за выдачу прав различным пользователям
        https://www.django-rest-framework.org/api-guide/permissions/
        """
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
        

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = MyModelSerializer

    @cache_page(60 * 15) # кэшируем детальную информацию на 15 минут
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ArticleTagSerializer(serializers.Serializer):
    tag_ids = serializers.ListField(child=serializers.IntegerField())

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids')
        instance.tag.set(tag_ids)
        instance.save()
        return instance

class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleTagAPIView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleTagSerializer
