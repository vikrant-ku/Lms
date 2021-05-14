from django.db import models
from .professor import Teacher
from .students import Students

class Leave(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField(default="")
    halfday = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default="Pending")
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.type


