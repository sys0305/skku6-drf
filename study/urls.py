from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.StudentView.as_view()),
    path("students/<int:pk>", views.StudentDetailView.as_view()),
    path("score/", views.ScoreView.as_view()),
    path("score/<int:pk>", views.ScoreDetailView.as_view()),
    path("students/<int:pk>/score", views.StudentScoreView.as_view()),
]
