from django.urls import path
from .views import UserProfileView, SessionView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('session/', SessionView.as_view(), name='session-create'),
    path('session/<str:session_id>/', SessionView.as_view(), name='session-delete'),
]
