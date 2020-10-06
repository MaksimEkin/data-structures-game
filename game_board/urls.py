from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='game-board-test'),
]