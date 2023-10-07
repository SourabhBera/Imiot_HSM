from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



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
    patient_id = models.ForeignKey(User, related_name='patient_records', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id_misc = models.CharField(max_length=255)

    def __str__(self):
        return self.patient_id.username

