# yourapp/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from .models import DoctorProfiles
from django.contrib.auth.hashers import check_password

class DoctorBackend(BaseBackend):
    def authenticate(self, request, doctor_id=None, password=None, **kwargs):
        try:
            doctor = DoctorProfiles.objects.get(doctor_id=doctor_id)
        except DoctorProfiles.DoesNotExist:
            return None

        if doctor.check_password(password):
            return doctor
        return None

    def get_user(self, doctor_id):
        try:
            return DoctorProfiles.objects.get(pk=doctor_id)
        except DoctorProfiles.DoesNotExist:
            return None