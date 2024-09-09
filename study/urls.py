from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.StudentView),
    path("students/<int:pk>", views.StudentDetailView),
    path("score/", views.ScoreView),
    path("score/<int:pk>", views.ScoreDetailView),
]
