import PyPDF2 as pdf
import os
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import User
from django.http import JsonResponse
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]


    def post(self ,request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "User registered successfully"} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        # Step 1: Retrieve the user based on email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Check if the provided password matches the stored password
        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Check if the role matches
        if user.role != role:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        # If the credentials are valid, generate the token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful!",
            "access_token": access_token , 
            "user_name" : user.name
        }, status=status.HTTP_200_OK)
    


def extract_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text


def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

class ResumeUploadAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self , request):
        if request.user.is_authenticated:
            # User is authenticated, proceed with the logic
            return Response({"message": "You are authenticated"}, status=200)
        else:
            return Response({"error": "User is not authenticated"}, status=401)
    
    def post(self, request):
        print("Authenticated user:", request.user)
        print("User authenticated:", request.user.is_authenticated)
        print("User role:", request.user.role)
        
        if request.user.role != "HR":
            return Response({"error": "Only HRs can upload resumes"}, status=403)

        user_id = request.data.get("id")
        if not user_id:
            return Response({"error": "Please provide a valid student ID"}, status=400)

        user = get_object_or_404(User, id=user_id, role="Student")

        uploaded_file = request.FILES.get("resume")
        job_description = request.data.get("job_description", "")

        if not uploaded_file:
            return Response({"error": "Please upload a resume"}, status=400)

        resume_text = extract_pdf_text(uploaded_file)

        prompt1 = f"""
        You are an HR Manager with Tech Experience in Big Data Science, Feature Engineering, Full Stack Development, DevOps, MLOps, Machine Learning, Data Science, and related technical domains. Analyze the provided resume and offer insights to enhance its content and impact. Evaluate the resume on key factors such as technical skills, relevant experience, achievements, and project descriptions. Identify gaps, suggest improvements for job-specific tailoring, and recommend keywords to optimize visibility for applicant tracking systems (ATS). Provide actionable suggestions to strengthen the professional summary, highlight quantifiable results, and ensure alignment with industry best practices.

        Consider that the job market is very competitive and you should provide the best assistance for improving the resume. Assign a percentage match based on the job description and list the missing keywords with high accuracy.

        Resume: {resume_text}
        Job Description: {job_description}

        I want the response in a structured JSON-like format:
        {{
            "JD match": "%",
            "MissingKeyWords": [],
            "Profile summary": ""
        }}
        """

        response_text = get_gemini_response(prompt1)
        return Response(response_text, status=200)