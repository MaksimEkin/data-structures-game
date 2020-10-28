"""
    Game Board app views.
"""
from django.shortcuts import render

def game_board(request):
    """Redirect to the game board view."""

    # Change this to the actual React frontend for game board when ready.
    return render(request, 'index.html')
