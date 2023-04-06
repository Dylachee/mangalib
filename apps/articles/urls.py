from django.urls import path, include
from .views import MyModelList, MyModelDetail , ReviewSerializer , ReviewViewSet
from rest_framework.routers import DefaultRouter
from ckeditor_uploader import views as ckeditor_views

router = DefaultRouter() 
router.register('article', MyModelList, 'articles')
router.register('reviews', ReviewViewSet)


urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),
] + router.urls







