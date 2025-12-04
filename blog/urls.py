from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('category/<str:category_name>/', views.blog_category, name='blog_category'),
]
