"""
    Views for Profile Page application.
"""

#from django.shortcuts import render
# Create your views here.
from django.shortcuts import render

def profile_page(request):
    """Redirect to the profile page view."""

    # Change this to the actual React frontend for game board when ready.
    return render(request, 'index.html')
