from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('add/', views.collect_trades, name='add'),
    path('',views.dashboard, name='dashboard' ),
    path('journal/', views.journal, name='journal'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)