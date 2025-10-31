# liverguard/serializers.py
from rest_framework import serializers
from .models import DbrPatients, DbrBloodResults, DbrAppointments, DbrBloodTestReferences, Announcements


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrPatients
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 응답에 포함하지 않음
        }


class BloodResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = DbrBloodResults
        fields = '__all__'
        read_only_fields = ['created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DbrAppointments
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BloodTestReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrBloodTestReferences
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']