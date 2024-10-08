from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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


# /students
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


# 학생 삭제
# 학생에 대한 id가 필요.
# students/<int:student_id>
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


# Class Based View

from rest_framework.views import APIView


class StudentView(APIView):
    # /students

    def get(self, request):
        qs = Student.objects.prefetch_related("score_set").all()
        # ListSerializer if many=True
        serializer = StudentSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    # /students/<int:pk>

    def get_object(self, pk):
        qs = get_object_or_404(Student, pk=pk)
        return qs

    def get(self, request, pk):
        qs = self.get_object(pk)
        serializer = StudentSerializer(qs)
        return Response(serializer.data)

    def put(self, request, pk):
        qs = self.get_object(pk)
        serializer = StudentSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScoreView(APIView):

    def get_object(self):
        qs = Score.objects.all()
        return qs

    def get(self, request):
        qs = self.get_object()
        serializer = ScoreSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreDetailView(APIView):

    def get_object(self, pk):
        qs = get_object_or_404(Score, pk=pk)
        return qs

    def get(self, request, pk):
        qs = self.get_object(pk)
        serializer = ScoreSerializer(qs)
        return Response(serializer.data)

    def put(self, request, pk):
        qs = self.get_object(pk)
        serializer = ScoreSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# [심화]
# GET /students/1/score : 1번학생의 모든 점수 데이터 조회
# POST /students/1/score : 1번학생의 모든 점수 데이터 추가
class StudentScoreView(APIView):

    def get(self, request, pk):
        qs = get_list_or_404(Score.objects.filter(student_id=pk))
        # qs = Score.objects.filter(student_id=pk).all()
        # if not qs:
        #     raise Http404("찾으시는 리소스가 없습니다.")
        serializer = ScoreSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ScoreSerializer(data={**request.data, "student": pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet

from rest_framework.viewsets import ViewSet


class StudentViewSet(ViewSet):

    def get_object(self, pk):
        qs = get_object_or_404(Student, pk=pk)
        return qs

    def list(self, request):
        # 목록조회
        # /students GET
        qs = Student.objects.prefetch_related("score_set").all()
        # ListSerializer if many=True
        serializer = StudentSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        # 생성
        # /students POST
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # students/<int:pk>
        # 상세 조회 (StudentDetailView's get)
        qs = self.get_object(pk)
        serializer = StudentSerializer(qs)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # 수정 (StudentDetailView's put)
        qs = self.get_object(pk)
        serializer = StudentSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # 삭제 (StudentDetailView's delete)
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScoreViewSet(ViewSet):
    """
    /score/ GET             : list
    /score/ POST            : create
    /score/<int:pk> GET     : retrieve
    /score/<int:pk> PUT     : update
    /score/<int:pk> DELETE  : destroy
    """

    def list(self, request):
        qs = Score.objects.all()
        serializer = ScoreSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        qs = get_object_or_404(Score, pk=pk)
        return qs

    def retrieve(self, request, pk):
        qs = self.get_object(pk)
        serializer = ScoreSerializer(qs)
        return Response(serializer.data)

    def update(self, request, pk):
        qs = self.get_object(pk)
        serializer = ScoreSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


# smtp://...
# ftp://... (통신규약 - 프로토콜)
# www.naver.com(host - domain)
# /search.naver (url path 영역)
# ?where=news&query=무역전쟁(query parameter, query strint, queryset)
# https://www.naver.com/search.naver?where=news&query=무역전쟁
# ModelViewSet
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # https://www.naver.com/search.naver?where=news
        print(self.request.query_params)
        name = self.request.query_params.get("name")
        if name:
            qs = qs.filter(name=name)
        return qs

    # /students/
    # /studetns/<int:pk>/

    # /students/seoul
    @action(["GET"], detail=False)
    def seoul(self, request):
        qs = self.get_queryset()
        qs = qs.filter(address__contains="서울")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # /students/4/reset => {name: '-', address: '-', email: '-'}
    @action(["PUT"], detail=True)
    def reset(self, request, pk):
        instance = self.get_object()
        instance.name = "-"
        instance.address = "-"
        instance.email = "-"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from django.db.models import F


class ScoreViewSet(ModelViewSet):
    # score에서 params로 각 과목의 점수가 입력되면, 해당 점수 이상인 score들만 반영되도록
    # url example: /study/score/?math=80&english=60
    #       -> math가 80이상이고 english가 60이상인 score들 반환
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    # 3. order 파라메터가 있을경우 해당 파라메터값으로 정렬해주세요
    # url example: /study/score/?order=math&math=80&english=60&
    #       => math별로 내림차순 정렬
    def get_queryset(self):
        qs = super().get_queryset()
        # https://www.naver.com/search.naver?where=news
        filter_kwargs = {}
        for subject in [
                "math",
                "english",
                "science",
        ]:
            _subject = self.request.query_params.get(subject)
            if _subject:
                filter_kwargs[f"{subject}__gte"] = _subject
        qs = qs.filter(**filter_kwargs)

        order = self.request.query_params.get("order")
        if order:
            qs = qs.order_by(f"-{order}")

        return qs

    # 4. score 서비스에 /top 을 넣으면 모든점수의 합이 270점이 넘는사람만 조회해주세요.
    #       => django model F객체 GreaterThan
    @action(["GET"], detail=False)
    def top(self, request):
        qs = self.get_queryset()
        qs = qs.annotate(total2=F("math") + F("english") + F("science"))
        qs = qs.filter(total2__gte=270)
        # from django.db.models.lookups import GreaterThan

        # qs = qs.filter(
        #     GreaterThan(F("math") + F("english") + F("science"), 270))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin


class ReadOnlyStudentViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# GET, POST
class ReadWriteStudentViewSet(ListModelMixin, RetrieveModelMixin,
                              CreateModelMixin, GenericViewSet):
    # / :GET, POST
    # /<int:pk> :GET
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
