from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("register", views.UserRegisterView, "register")
router.register("board", views.BoardViewSet, "board")

urlpatterns = router.urls + [path("protected/", views.ProtectedView.as_view())]
