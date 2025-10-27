from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

class TestView(APIView):
    def get(self, request):
        return Response({"message": "LiverGuard API is running!"})
# Create your views here.
