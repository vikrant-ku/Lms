from django.db import models
from admins.models.professor import Teacher
from admins.models.classes import Class
from admins.models.students import Students
from admins.models.fees import Academic_Year
from datetime import date

# Create your models here.
class Assignment(models.Model):
    teacher  = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    section = models.CharField(max_length=5, default="")
    subject = models.CharField(max_length=50, default="")
    due_date = models.DateField()
    date = models.DateField(auto_now_add=True)
    assignment = models.FileField(upload_to='assignments', null=True, blank=True)

    def __str__(self):
        return self.teacher.first_name


class OnlineClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=2, default="A")
    subject = models.CharField(max_length=50, default="")
    date = models.DateField(default=date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    link = models.CharField(max_length=500, default="")
    message = models.TextField(default= "")

class Marks(models.Model):
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=2, default="A")
    subject = models.CharField(max_length=50, default="")
    obtain_marks = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(default="", blank=True)
    exam_type = models.CharField(max_length=20, default="Half Yearly")
    added_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name='date_added', auto_now_add=True)

