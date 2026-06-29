from django.shortcuts import render

from .models import ComputerGame

# Create your views here.
def computer_games_list(request):
    all_computer_games = ComputerGame.objects.all()
    context = {'all_computer_games': all_computer_games}
    return render(request, 'computer_games_list.html', context)