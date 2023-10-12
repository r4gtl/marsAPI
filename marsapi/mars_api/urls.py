from django.urls import path
from .views import home

app_name="mars_api"

urlpatterns = [
    path('', home, name='home'),  # Questa riga gestisce la radice del sito web
    path('<str:rover_name>/', home, name='home'),
]