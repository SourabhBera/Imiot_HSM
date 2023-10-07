from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Department, Patient_Records
from .serializers import PatientRecordSerializer, DepartmentSerializer, UserSerializer
from .permissions import IsDoctor, IsPatient
class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response( {
                'error': 'Username and password are required.'
                })

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message' : 'User created successfully.',
            'refresh': str(refresh), 
            'access': str(refresh.access_token)
            })


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            # print('\n \n', refresh)
            return Response({
                'message' : 'Login successful.',
                'refresh': str(refresh), 
                'access': str(refresh.access_token)
                })
        else:
            return Response({
                'error': 'Invalid credentials.'
                })

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
            logout(request)
            return Response({'message': 'Logout successful.'})
    


class DoctorsList(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    serializer_class = UserSerializer

class DoctorDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    serializer_class = UserSerializer

class PatientsList(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Patients')
    serializer_class = UserSerializer

class PatientDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(groups__name='Patients')
    serializer_class = UserSerializer

class DepartmentsList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentPatients(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return User.objects.filter(groups__name='Patients', patientrecords__department_id=department_id)

class DepartmentDoctors(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return User.objects.filter(groups__name='Doctors', doctorprofile__department_id=department_id)

class PatientRecordsList(generics.ListCreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return Patient_Records.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class PatientRecordsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient_Records.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsPatient]
