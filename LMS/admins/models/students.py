from django.db import  models
from .classes import Class


class Students(models.Model):
    username = models.CharField(max_length=20, default="ST", null=True, blank=True)
    password = models.CharField(max_length=500, default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    father_name = models.CharField(max_length=30, default="")
    mother_name = models.CharField(max_length=30, default="")
    address = models.TextField()
    country = models.CharField(max_length=30, default="")
    state = models.CharField(max_length=30, default="")
    city = models.CharField(max_length=30, default="")
    zipcode = models.CharField(max_length=10, default="")
    phone = models.CharField(max_length=30, default="")
    gender = models.CharField(max_length=6, default="")
    dob = models.CharField(max_length=20)
    admission_no = models.CharField(max_length=30, default="", unique=True,null=True, blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    section = models.CharField(max_length=2, default="", null=True, blank=True)
    image = models.ImageField(upload_to="student", blank=True , null=True)
    is_login = models.BooleanField(default=False)
    token = models.CharField(max_length=12, default="")
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    is_rte = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Documents(models.Model):
    student = models.OneToOneField(Students, on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to="documents", blank=True , null=True)
    aadhar = models.FileField(upload_to="documents", blank=True, null=True)
    parent_aadhar = models.FileField(upload_to="documents", blank=True , null=True)
    tc = models.FileField(upload_to="documents", blank=True , null=True)
    progress_report = models.FileField(upload_to="documents", blank=True , null=True)
    affidavit = models.FileField(upload_to="documents", blank=True , null=True)
    under_taking = models.FileField(upload_to="documents", blank=True , null=True)

    def __str__(self):
        return self.student.username