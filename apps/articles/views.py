from django.shortcuts import render
from rest_framework import generics , viewsets
from .models import Article , Review,Tag, Like
from .serializers import MyModelSerializer, ReviewSerializer, LikeSerializer, RatingSerializer, TagSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
class MyModelList(ModelViewSet, Article):

    queryset = Article.objects.all() 
    serializer_class = MyModelSerializer

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
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        article = self.get_object()
        like = Like.objects.filter(user=request.user, article=article)
        if like.exists():
            like.delete()
            return Response({'liked': False})
        else:
            Like.objects.create(user=request.user, article=article).save()
            return Response({'liked': True})
        

    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_article(self, request, pk=None) -> Response:
        article = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
        return Response(serializer.data)
        

    
    

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = MyModelSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer