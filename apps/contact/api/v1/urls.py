from django.urls import path
from .views import ContactListAPIView, ContactCreateAPIView, ContactRUDAPIView


urlpatterns = [
    path('create/', ContactCreateAPIView.as_view()),
    path('list/', ContactListAPIView.as_view()),
    path('rud/<int:pk>/', ContactRUDAPIView.as_view()),
]
