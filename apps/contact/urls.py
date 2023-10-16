from django.urls import path, include

app_name = 'contact'


urlpatterns = [
    path('api/', include('apps.contact.api.urls')),
]
