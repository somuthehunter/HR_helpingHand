from rest_framework import serializers
from .models import CustomUser , Student
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'role', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    resume_content = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "role", "resume_content"]

    def get_resume_content(self, obj):
        
        student = getattr(obj, 'student', None)
        return student.resume_content if student else None
