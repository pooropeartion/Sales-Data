
from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.Extract_data, name='orders'),
    path('jokes/', views.fetch_and_store_jokes, name='jokes'),
    
]
