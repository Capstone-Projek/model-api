from django.urls import path
from .views import ModelAPIView

urlpatterns = [
    path('classify/', ModelAPIView.as_view(), name='classify'),
]