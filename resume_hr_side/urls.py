from django.urls import path
from resume_hr_side.views import ResumeAnalysisAPIView, LoginApiView , UserRegistrationView , ResumeUploadAPIViewStudents , GetAllCandidates




urlpatterns = [
    #basic utilities
    path('login/', LoginApiView.as_view(), name='login'),
    path("register/", UserRegistrationView.as_view(), name="user-register"),

    #Hr side
    path('analysis/', ResumeAnalysisAPIView.as_view(), name='upload-resume'),
    path('all-users/', GetAllCandidates.as_view(), name='upload-resume'),
    # path('upload_resume_by_hr/', ResumeUploadAPIViewProfessional.as_view(), name='upload-resume'),
    # path('hr_missing-skills/', MissingSkills.as_view(), name='missing-skills'),


    #Student or other side
    path('upload_resume_by_Students/', ResumeUploadAPIViewStudents.as_view(), name='upload-resume'),
]