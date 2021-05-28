from django.db import models
from .professor import Teacher
from django.utils import timezone
from .students import Students



class Notices(models.Model):
    recipient = models.CharField(max_length=10, default='All')
    type = models.CharField(max_length=10, default='Holiday')
    date = models.DateField()
    notice = models.TextField()

    def __str__(self):
        return self.recipient


class Event(models.Model):

    title = models.CharField(max_length=200, default='')
    description = models.TextField(default="")
    start_date = models.DateField()
    end_date = models.DateField( default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.title



class Notification(models.Model):

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    from_user = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="from_user")
    notification = models.CharField(max_length=1000, default="")
    seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.teacher:
            return self.teacher.username
        else:
            return self.student.username

class Feedback(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    title = models.TextField(max_length=500, default="")
    message = models.TextField(default="")
    seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.username






