"""
    Home Page application view. Loads the home page from React.
"""
from django.shortcuts import render

def home(request):
    """Return React front-end."""
    return render(request, 'index.html')
