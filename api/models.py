from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Custom_User(AbstractUser):
    is_doctor = models.BooleanField(null=True, default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.id + " " + self.username

class Department(models.Model):
    attributes_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    diagnostics = models.TextField()
    location = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient_Records(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Custom_User, related_name='patient_records', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id_misc = models.CharField(max_length=255)

    def __str__(self):
        return self.patient_id.username

