from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=30)


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    english = models.IntegerField()
    math = models.IntegerField()
    science = models.IntegerField()

    exam_date = models.DateTimeField(null=True)


# ManyToMany
class Department(models.Model):
    """
    Student와 다대다 연결.
    eg. 미화부, 도서부, 방송부, 신문부...

    django ManyToMany
    공식문서 ManyToMany
    """

    pass
