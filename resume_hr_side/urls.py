from django.urls import path
from .views import LoginApiView, ResumeUploadAPIView , UserRegistrationView




urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('upload_resume/', ResumeUploadAPIView.as_view(), name='upload-resume'),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
]