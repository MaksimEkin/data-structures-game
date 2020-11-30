"""
    Views for Register Page application.
"""

#from django.shortcuts import render
# Create your views here.
from django.shortcuts import render

def register(request):
    """Redirect to the register view."""

    # Change this to the actual React frontend for game board when ready.
    return render(request, 'index.html')
