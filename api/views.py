from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Department, Patient_Records, Custom_User
from .serializers import PatientRecordSerializer, DepartmentSerializer, UserSerializer
from .permissions import IsDoctor, IsPatient
from rest_framework.decorators import api_view
from .sendemail import send_IOE_email


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
    


class DoctorsList(generics.ListCreateAPIView):
    queryset = Custom_User.objects.filter(groups__name='Doctors')
    serializer_class = UserSerializer

    def get_queryset(self):
        return Custom_User.objects.filter(is_doctor=True)


@api_view(['PUT', 'GET', 'DELETE'])
def DoctorDetail(request, pk):
    if request.method == 'GET':
        query_data = Custom_User.objects.get(is_doctor=True, id=pk)
        serailize = UserSerializer(query_data)
        return Response(serailize.data)
    
    
    if request.method == 'PUT':
        query_data = Custom_User.objects.get(is_doctor=True, id=pk)
        serializer = UserSerializer(query_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User Updated Successfully",
                             "data": serializer.data })
    
    if request.method == 'DELETE':
        query_data = Custom_User.objects.get(is_doctor=True, id=pk)
        query_data.delete()
        return Response({"message": "User Deleted Successfully"})

    return Response({"message": "User is not a Doctor."})
class PatientsList(generics.ListCreateAPIView):
    queryset = Custom_User.objects.filter(groups__name='Patients')
    serializer_class = UserSerializer

    def get_queryset(self):
        return Custom_User.objects.filter(is_doctor= False)

class PatientDetail(generics.RetrieveAPIView):
    queryset = Custom_User.objects.filter(groups__name='Patients')
    serializer_class = UserSerializer

class DepartmentsList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentPatients(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return Custom_User.objects.filter(groups__name='Patients', patientrecords__department_id=department_id)

class DepartmentDoctors(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return Custom_User.objects.filter(groups__name='Doctors', doctorprofile__department_id=department_id)

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



class SendIoeEmailView(APIView):
    def post(self,request):
        send_IOE_email()
        return Response({'message':'email sent successfully'})
