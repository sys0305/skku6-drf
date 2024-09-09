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


# /student
# GET
# POST
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


from django.shortcuts import get_object_or_404


# 학생 삭제
# 학생에 대한 id가 필요.
# student/<int:student_id>
# GET : 학생 개별조회
# PUT : 학생 수정
# DELETE : 학생 삭제
@api_view(["GET", "PUT", "DELETE"])
def StudentDetailView(request, pk):
    qs = get_object_or_404(Student, pk=pk)
    if request.method == "GET":
        # 학생 상세조회 many=False이기 때문에 타입은 객체(dictionary 형태로 반환)
        serializer = StudentSerializer(qs)
        return Response(serializer.data)

    if request.method == "PUT":
        # 학생 수정 /student/<int:pk>
        # pk에 해당하는 학생을 어떻게(request body내용으로) 수정
        serializer = StudentSerializer(qs, data=request.data)
        # Validation Check <request.body에 대해>
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        # 학생 삭제 /student/<int:pk>
        # pk에 해당하는 학생 삭제. (물리적 삭제 vs 논리적 삭제) ==> 개발자의 마음대로
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# score 모델에
# student 모델과 똑같이 CRUD API 를 만드세요
# /score          GET:    데이터 리스트 조회
# /score          POST:   데이터 추가.
# /score/<int:pk> GET:    데이터 하나 조회
# /score/<int:pk> PUT:    데이터 수정
# /score/<int:pk> DELETE: 데이터 삭제


# /score          GET:    데이터 리스트 조회
# /score          POST:   데이터 추가.
@api_view(["GET", "POST"])
def ScoreView(request):
    if request.method == "GET":
        qs = Score.objects.all()
        serializer = ScoreSerializer(qs, many=True)
        response = Response(serializer.data)
        return response
    elif request.method == "POST":
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /score/<int:pk> GET:    데이터 하나 조회
# /score/<int:pk> PUT:    데이터 수정
# /score/<int:pk> DELETE: 데이터 삭제
@api_view(["GET", "PUT", "DELETE"])
def ScoreDetailView(request, pk):
    qs = get_object_or_404(Score, pk=pk)
    if request.method == "GET":
        serializer = ScoreSerializer(qs)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ScoreSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.http import Http404
from django.shortcuts import get_list_or_404


# [심화]
# GET /students/1/score : 1번학생의 모든 점수 데이터 조회
# POST /students/1/score : 1번학생의 모든 점수 데이터 추가
@api_view(["GET", "POST"])
def StudentScoreView(request, pk):
    if request.method == "GET":
        qs = get_list_or_404(Score.objects.filter(student_id=pk))
        # qs = Score.objects.filter(student_id=pk).all()
        # if not qs:
        #     raise Http404("찾으시는 리소스가 없습니다.")
        serializer = ScoreSerializer(qs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ScoreSerializer(data={**request.data, "student": pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
