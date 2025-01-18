from django.db import models

class Professional(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    # company_name = models.TextField()  

    def __str__(self):
        return f"Professional: {self.user.name}"


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    # institution = models.CharField(max_length=100)  # Example: Student-related fields

    def __str__(self):
        return f"Student: {self.user.name}"


class User(models.Model):
    ROLE_CHOICES = [
        ("HR", "HR"),
        ("Student", "Student"),
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=50)  # Should be hashed in real case

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)  # First, save the User instance

        if self.role == "HR":
            Professional.objects.get_or_create(user=self)
        elif self.role == "Student":
            Student.objects.get_or_create(user=self)

    def __str__(self):
        return self.name
