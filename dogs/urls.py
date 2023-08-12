from django.urls import path
from .apps import DogsConfig
from . import views

app_name = DogsConfig.name

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path('<int:pk>/dogs', views.DogListView.as_view(), name='category_dogs'),
    path('dogs/create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dogs/upadte/<int:pk>/', views.DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>/', views.DogDeleteView.as_view(), name='dog_delete'),
]
