from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 
    is_teacher = models.BooleanField(default=False)

    otp_token = models.CharField(max_length=6, null=True, blank=True)
    otp_token_expiry = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_groups')
    students = models.ManyToManyField(User, related_name='student_groups')

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    file = models.FileField(upload_to='uploaded_files/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    