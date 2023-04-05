from django.shortcuts import render
from rest_framework import generics
from .models import Article , Comment
from .serializers import MyModelSerializer , CommentSerializer , RatingSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
    
    def get_serializer_class(self):
        """  
        Выдача разных сериализаторов в зависимости от вызываемой функции
        """
        if self.action == 'comment':
            return CommentSerializer
        elif self.action == 'rate_article':
            return RatingSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        """  
        декоратор action позволяет добавить новую функцию в качестве действия для ViewSetов
        https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
        """
        article = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        return Response({'TODO': 'ДОБАВИТЬ УДАЛЕНИЕ КОММЕНТА'})
    

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = MyModelSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated,]
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
# 