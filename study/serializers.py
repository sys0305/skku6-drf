from rest_framework import serializers
from .models import Student, Score


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["name", "address", "email"]


# Serializer도 추가해주세요.
# score_view 도 GET으로 만들기
class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ["student", "english", "math", "science", "exam_date"]
