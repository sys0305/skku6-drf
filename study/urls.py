from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

# Router객체: 자원에 대한 viewset을 하나의 url처럼 관리하자.
router = DefaultRouter()
router.register("students", views.StudentViewSet, basename="student")
router.register("score", views.ScoreViewSet, basename="score")

urlpatterns = router.urls + [
    # path("students/", views.StudentView.as_view()),
    # path("students/<int:pk>", views.StudentDetailView.as_view()),
    # path("students/",
    #      views.StudentViewSet.as_view({
    #          "get": "list",
    #          "post": "create"
    #      })),
    # path(
    #     "students/<int:pk>",
    #     views.StudentViewSet.as_view({
    #         "get": "retrieve",
    #         "put": "update",
    #         "delete": "destroy"
    #     }),
    # ),
    # path("score/", views.ScoreView.as_view()),
    # path("score/<int:pk>", views.ScoreDetailView.as_view()),
    path("students/<int:pk>/score", views.StudentScoreView.as_view()),
]
