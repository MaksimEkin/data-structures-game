"""
 Profile Page app API URLs.
"""
from django.urls import path
from profile_page.api import api
from . import views

urlpatterns = [

    # Views
    path('', views.profile_page, name='profile-page'),

    # Profile Page API Calls for Authentication
    path('api', api.api_overview, name='profile-page-api_overview'),
    path('api/register', api.register, name='profile-page-register'),
    path('api/login', api.login, name='profile-page-login'),
    path('api/logout', api.logout, name='profile-page-logout'),
    path('api/delete', api.delete, name='profile-page-delete'),

    # Get all profile information
    path('api/profile', api.profile, name='profile-page-profile'),

    # Adding, removing, and accepting friend
    path('api/add_friend', api.add_friend, name='profile-page-add_friend'),
    path('api/accept_decline_friend', api.accept_decline_friend, name='profile-page-accept_friend'),
    path('api/remove_friend', api.remove_friend, name='profile-page-remove_friend'),

    # Game Board Import/Export API calls
    path('api/save_board', api.save_board, name='profile-save_board'),
    path('api/delete_board', api.delete_board, name='profile-delete_board'),
    path('api/share', api.share, name='profile-share'),
    path('api/saved_boards/<str:user_id>/<str:token>', api.saved_boards, name='profile-saved_boards'),
    path('api/load_board', api.load_board, name='profile-load_board'),

    # Heroku scheduler
    path('api/scheduled_tasks', api.scheduled_tasks, name='profile-scheduled_tasks'),
]
