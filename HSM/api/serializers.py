from rest_framework import serializers
from .models import Patient_Records, Department, Custom_User
from django.contrib.auth.models import User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Records
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = ('id', 'username', 'is_doctor')