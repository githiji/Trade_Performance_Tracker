from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.collect_trades, name='add'),
    path('dash/',views.dashboard, name='dashboard' )
]