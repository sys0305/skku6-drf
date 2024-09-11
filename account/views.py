from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.tokens import AccessToken


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("인증 완료")


from .serializers import UserSerializer


class UserRegisterView(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer


# /account/board에 대해서 C.R.U.D 작성
# Create는 로그인 된 유저만 작성 가능하도록.
# Retrieve는 누구나 조회 가능하도록
# Update와 Delete는 글 작성한 유저만 접근 가능하도록 구성

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

# /account/board에 대해서 C.R.U.D 작성
# Create는 로그인 된 유저만 작성 가능하도록.
# Retrieve는 누구나 조회 가능하도록
# Update와 Delete는 글 작성한 유저만 접근 가능하도록 구성
from .serializers import BoardSerializer
from .models import Board
from rest_framework import status

from rest_framework import permissions


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if request.user.id != obj.user_id:
            return False
        return True


# BaseLine 코드
class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # obj = self.get_object()
        # if obj.user.id != request.user.id:
        #   return Response(status=status.HTTP_403_FORBIDDEN)
        request.data["user"] = request.user.id
        return super().update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]
        elif self.action in ["create"]:
            return [IsAuthenticated()]
        else:
            # ...
            return [IsAuthor()]
