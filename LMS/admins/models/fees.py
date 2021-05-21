from django.db import models
from .students import Students
from .classes import Class
from decimal import Decimal
from django.utils import timezone


class Academic_Year(models.Model):
    academic_year = models.CharField(max_length=9, default="2020-2021")

    def __str__(self):
        return self.academic_year


MONTH_CHOICES = (
        ('JAN', 'JANUARY' ),
        ('FEB', 'FEBRARY'),
        ('MAR', 'MARCH'),
        ('APR', 'APRIL'),
        ('MAY', 'MAY'),
        ('JUN', 'JUNE'),
        ('JUL', 'JULY'),
        ('AUG', 'AUGUST'),
        ('SEP', 'SEPTEMBER'),
        ('OCT', 'OCTOBE'),
        ('NOV', 'NOVEMBER'),
        ('DEC', 'DECEMBER'),
)
STATUS_CHOICES = (
        ('PAID', 'PAID' ),
        ('UNPAID', 'UNPAID'),
        )


class Fees(models.Model):
    class_name = models.OneToOneField(Class, on_delete=models.CASCADE)
    fees = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('00.00'))

    def __str__(self):
        return str(self.fees)


class Student_fees(models.Model):
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True, blank=True)
    total_fee = models.ForeignKey(Fees, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year =models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('00.00'))
    month = models.CharField(max_length=10, choices=MONTH_CHOICES, default="", null=True, blank=True)
    payment_mode = models.CharField(max_length=30, default="" , null=True, blank=True)
    order_id = models.CharField(max_length=50, default="", null=True, blank=True)
    payment_id = models.CharField(max_length=50, default="", null=True, blank=True)
    status = models.BooleanField(default=False)
    submit_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.student.first_name



