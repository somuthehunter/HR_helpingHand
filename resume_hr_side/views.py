import PyPDF2 as pdf
import os
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import CustomUser , Student , Professional
from django.http import JsonResponse
from .serializers import UserRegistrationSerializer,UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


genai.configure(api_key="AIzaSyCRZNNnmtoDxHeKsJPHQQMgqTkaWwZA4eQ")


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Initialize the serializer with the request data
        serializer = UserRegistrationSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the user instance
            user = serializer.save()
            
            # Handle additional profile creation based on the user's role
            if user.role == "HR":
                Professional.objects.get_or_create(user=user)
            elif user.role == "Student":
                Student.objects.get_or_create(user=user)

            # Return a success message
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        # Return errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        # Step 1: Retrieve the user based on email and role
        try:
            # Query CustomUser for email, then get the associated profile based on role
            user = CustomUser.objects.get(email=email)
            
            # Check if the role matches
            if user.role != role:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
            
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Check if the provided password matches the stored password
        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Generate the token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful!",
            "access_token": access_token, 
            "user_name": user.name,
            "user_id" : user.id
        }, status=status.HTTP_200_OK)
    


def extract_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text


def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# class ResumeUploadAPIViewProfessional(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         if request.user.is_authenticated:
#             # User is authenticated, proceed with the logic
#             return Response({"message": "You are authenticated"}, status=200)
#         else:
#             return Response({"error": "User is not authenticated"}, status=401)
    
#     def post(self, request):
#         print("Authenticated user:", request.user)
#         print("User authenticated:", request.user.is_authenticated)
#         print("user role:", request.user.role)

#         # Ensure that we are working with the correct CustomUser model
#         if request.user.role == "HR":
#             uploaded_file = request.FILES.get("resume")
#             job_description = request.data.get("job_description", "")

#             if not uploaded_file:
#                 return Response({"error": "Please upload a resume"}, status=400)

#             resume_text = extract_pdf_text(uploaded_file)

#         # AI Processing
#             prompt = f"""
#             You are an HR Manager with expertise in Data Science, Full Stack Development, DevOps, and related fields.
#             Analyze the resume and evaluate technical skills, achievements, and missing keywords.

#             Resume: {resume_text}
#             Job Description: {job_description}

#             Output format:
#             {{
#                 "JD match": "%",
#                 "MissingKeyWords": [],
#                 "Profile summary": ""
#             }}
#             """

#             response_text = get_gemini_response(prompt)
#             return Response(response_text, status=200)
            
class ResumeAnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        This API handles:
        1. Resume Upload & Analysis for HR
        2. Missing Skills Analysis

        It differentiates between functionalities based on `analysis_type` in the request.
        """
        if request.user.role != "HR":
            return Response({"error": "Only HRs are allowed to access this feature"}, status=403)

        # Determine the analysis type from the request data
        analysis_type = request.data.get("analysis_type", "").lower()
        uploaded_file = request.FILES.get("resume")
        job_description = request.data.get("job_description", "")

        if not uploaded_file:
            return Response({"error": "Please upload a resume"}, status=400)

        # Extract resume text
        resume_text = extract_pdf_text(uploaded_file)

        if analysis_type == "resume_analysis":
            # AI Processing for resume analysis
            prompt = f"""
            You are an HR Manager with expertise in Data Science, Full Stack Development, DevOps, and related fields.
            Analyze the resume and evaluate technical skills, achievements, and missing keywords.

            Resume: {resume_text}
            Job Description: {job_description}

            Output format:
            {{
                "JD match": "%",
                "MissingKeyWords": [],
                "Profile summary": ""
            }}
            """
        
        elif analysis_type == "missing_skills":
            # AI Processing for missing skills analysis
            prompt = f"""
            You are an experienced HR professional and a Tech Lead with expertise in Data Science, Full Stack Development, DevOps, MLOps, and related technical domains. 
            Your role is to analyze a candidate’s resume against a given job description and identify missing skills, gaps in experience, and areas of improvement.
            Identify missing keywords, certifications, or tools that are crucial for the job role.

            Resume: {resume_text}
            Job Description: {job_description}

            Output format:
            {{
                "MissingKeyWords": [],
                "Skills": ""
            }}
            """
        
        else:
            return Response({"error": "Invalid analysis type. Use 'resume_analysis' or 'missing_skills'."}, status=400)

        # Get AI response
        response_text = get_gemini_response(prompt)

        return Response(response_text, status=200)
    

class ResumeUploadAPIViewStudents(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("Authenticated user:", request.user)
        print("User authenticated:", request.user.is_authenticated)
        print("user role:", request.user.role)

        # Ensure that we are working with the correct CustomUser model
        if request.user.role == "Student":
            uploaded_file = request.FILES.get("resume")
            job_description = request.data.get("job_description", "")

            if not uploaded_file:
                return Response({"error": "Please upload a resume"}, status=400)

            resume_text = extract_pdf_text(uploaded_file)

        # AI Processing
            prompt = f"""
            You are an HR Manager with expertise in Data Science, Full Stack Development, DevOps, and related fields.
            Analyze the resume and evaluate technical skills, achievements, and missing keywords.

            Resume: {resume_text}
            Job Description: {job_description}

            Output format:
            {{
                "JD match": "%",
                "MissingKeyWords": [],
                "Profile summary": ""
            }}
            """

            response_text = get_gemini_response(prompt)
            return Response(response_text, status=200)
        
# class MissingSkills(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         if request.user.role == "HR":
#             uploaded_file = request.FILES.get("resume")
#             job_description = request.data.get("job_description", "")

#             if not uploaded_file:
#                 return Response({"error": "Please upload a resume"}, status=400)

#             resume_text = extract_pdf_text(uploaded_file)
#             prompt = f""" You are an experienced HR professional and a Tech Lead with expertise in Data Science, Full Stack Development, DevOps, MLOps, and related technical domains. Your role is to analyze a candidate’s resume against a given job description and identify missing skills, gaps in experience, and areas of improvement .
#             Identify missing keywords, certifications, or tools that are crucial for the job role.
#             Resume : {resume_text} 
#             Job Description: {job_description}
#  Output format:
#             {{
#                 "MissingKeyWords": [],
#                 "Skills" : "",
#             }}
            
#             """
#             response_text = get_gemini_response(prompt)
#             return Response(response_text, status=200)
        
class GetAllCandidates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        if request.user.role == "Student":
            return Response({"error": "Only HRs are allowed to access this feature"}, status=403)
        users = CustomUser.objects.filter(role = "Student")

        serialized_users = UserSerializer(users, many=True)

        return Response({"users":serialized_users.data} ,status=200)

