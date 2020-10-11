from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def home(request):
    return render(request, 'index.html')

