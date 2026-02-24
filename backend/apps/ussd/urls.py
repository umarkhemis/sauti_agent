from django.urls import path
from .views import BuildUSSDCodeView, ParseUSSDResponseView

urlpatterns = [
    path('build-code/', BuildUSSDCodeView.as_view(), name='ussd-build-code'),
    path('parse/', ParseUSSDResponseView.as_view(), name='ussd-parse'),
]
