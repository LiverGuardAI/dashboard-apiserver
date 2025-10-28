from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Patients
from .serializers import PatientSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import DoctorProfiles
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password

# login view
class DoctorLoginView(APIView):
    def post(self, request):
        doctor_id = request.data.get("doctor_id")
        password = request.data.get("password")

        try:
            doctor = DoctorProfiles.objects.get(doctor_id=doctor_id)
        except DoctorProfiles.DoesNotExist:
            return Response({"error": "존재하지 않는 아이디입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 비밀번호 확인
        if not check_password(password, doctor.password):
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 세션에 로그인 정보 직접 저장
        request.session["doctor_id"] = doctor.doctor_id
        request.session["doctor_name"] = doctor.name
        request.session.set_expiry(60 * 60 * 2)  # 2시간 후 만료 (선택)

        return Response({
            "message": "로그인 성공",
            "doctor_id": doctor.doctor_id,
            "name": doctor.name,
            "position": doctor.position,
        }, status=status.HTTP_200_OK)

# logout view
class DoctorLogoutView(APIView):
    def post(self, request):
        # 세션 전체 삭제 (현재 로그인 정보 포함)
        request.session.flush()
        return Response(
            {"message": "로그아웃 완료"},
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
def check_session(request):
    doctor_id = request.session.get("doctor_id")
    doctor_name = request.session.get("doctor_name")

    if doctor_id and doctor_name:
        return Response({
            "is_authenticated": True,
            "doctor_id": doctor_id,
            "name": doctor_name
        })
    return Response({"is_authenticated": False})


# 환자 목록 조회 (GET /api/patients/)
class PatientListView(generics.ListAPIView):
    queryset = Patients.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer

# 단일 환자 조회 (GET /api/patients/<patient_id>/)
class PatientDetailView(generics.RetrieveAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'
    
