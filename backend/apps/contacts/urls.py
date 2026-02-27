from django.urls import path
from .views import ResolveContactView

urlpatterns = [
    path('resolve/', ResolveContactView.as_view(), name='contacts-resolve'),
]
