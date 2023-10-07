from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('doctors/', DoctorsList.as_view(), name='doctors-list'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),
    path('patients/', PatientsList.as_view(), name='patients-list'),
    path('patients/<int:pk>/', PatientDetail.as_view(), name='patient-detail'),
    path('departments/', DepartmentsList.as_view(), name='departments-list'),
    path('departments/<int:pk>/patients/', DepartmentPatients.as_view(), name='department-patients'),
    path('departments/<int:pk>/doctors/', DepartmentDoctors.as_view(), name='department-doctors'),
    path('patient_records/', PatientRecordsList.as_view(), name='patient-records-list'),
    path('patient_records/<int:pk>/', PatientRecordsDetail.as_view(), name='patient-records-detail'),
]

