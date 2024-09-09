from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import Response

# Create your views here.
from .models import Student, Score
from .serializers import StudentSerializer, ScoreSerializer

# @api_view(["GET"])
# def StudentView(request):
#     # qs = Student.objects.all()
#     qs = Student.objects.prefetch_related("score_set").all()

#     # ListSerializer if many=True
#     serializer = StudentSerializer(qs, many=True)
#     return Response(serializer.data)

from rest_framework import status


@api_view(["GET", "POST"])
def StudentView(request):
    if request.method == "GET":
        qs = Student.objects.prefetch_related("score_set").all()
        # ListSerializer if many=True
        serializer = StudentSerializer(qs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def ScoreView(request):
    qs = Score.objects.all()
    serializer = ScoreSerializer(qs, many=True)
    response = Response(serializer.data)
    return response
