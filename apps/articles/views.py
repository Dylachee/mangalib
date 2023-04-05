from django.shortcuts import render
from rest_framework import generics
from .models import Article
from .serializers import MyModelSerializer

class MyModelList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = MyModelSerializer

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = MyModelSerializer

