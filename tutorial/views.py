"""
    Views for Tutorial Page application.
"""

# Create your views here.
from django.shortcuts import render

def tutorial(request):
    """Redirect to the tutorial view."""

    # Change this to the actual React frontend for game board when ready.
    return render(request, 'index.html')