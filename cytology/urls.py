from django.urls import path
from .models import Sample
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sample/', views.sample, name='sample'),
    path('<int:sample_id>/results/', views.results, name='results'),
]