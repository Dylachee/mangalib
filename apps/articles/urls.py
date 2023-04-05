from django.urls import path
from .views import MyModelList, MyModelDetail

urlpatterns = [
    path('article/', MyModelList.as_view()),
    path('articles/<int:pk>/', MyModelDetail.as_view()),
]
