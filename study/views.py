from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import Response

# Create your views here.
from .models import Student, Score
from .serializers import StudentSerializer, ScoreSerializer


@api_view(["GET"])
def StudentView(request):
    qs = Student.objects.all()
    # ListSerializer if many=True
    serializer = StudentSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def ScoreView(request):
    qs = Score.objects.all()
    serializer = ScoreSerializer(qs, many=True)
    response = Response(serializer.data)
    return response
