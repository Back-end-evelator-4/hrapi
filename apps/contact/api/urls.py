from django.urls import path, include

app_name = 'contact'


urlpatterns = [
    path('v1/', include('apps.contact.api.v1.urls'))
    
]
