from django.shortcuts import render
from django.http import HttpResponse

def board(request):
    return HttpResponse("<h1>Test</h1>")