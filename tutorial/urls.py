"""
    Views for Tutorial Page application.
"""
from django.urls import path
from . import views

urlpatterns = [

    # Views
    path('', views.tutorial, name='tutorial')

]