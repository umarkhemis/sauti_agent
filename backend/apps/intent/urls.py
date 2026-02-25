from django.urls import path
from .views import ClassifyIntentView

urlpatterns = [
    path('classify/', ClassifyIntentView.as_view(), name='intent-classify'),
]
