from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, role, password=None):
        user = self.create_user(email, name, role, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ("HR", "HR"),
        ("Student", "Student"),
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128)  # Store hashed passwords (default behavior of set_password)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Perform any additional logic here, if needed.
        super().save(*args, **kwargs)

class Professional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add fields specific to Professional role here
    resume_content = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"Professional Profile of {self.user.name}"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add fields specific to Student role here
    resume_content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Student Profile of {self.user.name}"
