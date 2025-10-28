from django.urls import path
from .views import PatientListView, PatientDetailView
from .views import DoctorLoginView, DoctorLogoutView
from .views import check_session

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<uuid:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor-login'),
    path("doctor/logout/", DoctorLogoutView.as_view(), name="doctor-logout"),
    path("doctor/session/", check_session, name="check-session"),
]