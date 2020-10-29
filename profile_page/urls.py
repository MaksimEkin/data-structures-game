"""
 Profile Page app API URLs.
"""
from django.urls import path
from profile_page.api import api

urlpatterns = [
    # Profile Page API Calls for Authentication
    path('api', api.api_overview, name='profile-page-api_overview'),
    path('api/register', api.register, name='profile-page-register'),
    path('api/login', api.login, name='profile-page-login'),
    path('api/logout', api.logout, name='profile-page-logout'),

    # Game Board Import/Export API calls
    path('api/save_board', api.save_board, name='profile-save_board'),
    path('api/delete_board', api.delete_board, name='profile-delete_board'),
    path('api/share', api.share, name='profile-share'),
    path('api/saved_boards/<str:user_id>/<str:token>', api.saved_boards, name='profile-saved_boards'),
    path('api/load_board', api.load_board, name='profile-load_board'),
]
