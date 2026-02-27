from django.urls import path
from .views import ResolveCallView, LogCallView

urlpatterns = [
    path('resolve/', ResolveCallView.as_view(), name='calls-resolve'),
    path('log/', LogCallView.as_view(), name='calls-log'),
]
