from django.db import models
from datetime import date
from django.utils import timezone
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



