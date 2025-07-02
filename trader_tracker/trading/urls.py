from django.urls import path
from . import views

urlpatterns = [
    
    path('add/', views.collect_trades, name='add'),
    path('',views.dashboard, name='dashboard' )
]