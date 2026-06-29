from django.urls import path
from django.views.generic import TemplateView

from ComputerGames import views

urlpatterns = [
    path('', views.computer_games_list, name='computer_games_list')
    # path('', views.computer_games_list, name='computer_games_list')
]