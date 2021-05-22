from django.db import models
from .fees import Academic_Year
from .students import Students
from .professor import Teacher
from .classes import Class
from datetime import datetime



class Student_Attandance(models.Model):
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=10, default="")
    attandance = models.CharField(max_length=2, default='A')
    datetime = models.DateTimeField(blank=True)

    def __str__(self):
        return self.student.username


class Teacher_Attandance(models.Model):
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    attandance = models.CharField(max_length=2, default='A')
    datetime = models.DateTimeField(blank=True)

    def __str__(self):
        return self.teacher.username
