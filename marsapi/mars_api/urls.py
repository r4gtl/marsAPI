from django.urls import path
from .views import home, get_images

app_name="mars_api"

urlpatterns = [
    path('', home, name='home'),  # Questa riga gestisce la radice del sito web
    path('<str:rover_name>/', home, name='home'),
    path('get_images/<str:rover_name>/<int:max_sol>/', get_images, name='get_images')
    
]