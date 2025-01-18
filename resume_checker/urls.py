
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/', include('resume_hr_side.urls')),  # Include your app URLs
]
