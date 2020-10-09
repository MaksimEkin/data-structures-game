from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def game_board(request):
    # Change this to the actual React frontend for game board when ready.
    return render(request, 'index.html')
