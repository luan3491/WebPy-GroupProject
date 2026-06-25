from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('list/', TemplateView.as_view(template_name='computer_games_list.html'), name='list')
]