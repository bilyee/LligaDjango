from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='futbol_index'),
    path('clasificacio/', views.standings, name='clasificacio'),
    path('clasificacio/<int:lliga_id>/', views.standings, name='clasificacio_lliga'),
]
