from django.db import  models
from .classes import Class


class Teacher(models.Model):
    username = models.CharField(max_length=20, default="TE", null=True, blank=True)
    password = models.CharField(max_length=500, default="")

    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=6, default="")
    dob = models.CharField(max_length=20)
    address = models.TextField(default="")
    country = models.CharField(max_length=20, default="INDIA")
    state = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    zipcode = models.CharField(max_length=10, default="")
    phone = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length = 254, default="")

    designation = models.CharField(max_length=20, default="")
    qualification = models.CharField(max_length=50, default="")
    basic_salary = models.CharField(max_length=30, default="")
    contract_type = models.CharField(max_length=30, default="")
    work_shift = models.CharField(max_length=30, default="")


    #account info
    bank_name = models.CharField(max_length=30, default="")
    branch_name = models.CharField(max_length=30, default="")
    account_number = models.CharField(max_length=30, default="")
    ifsc_code = models.CharField(max_length=30, default="")
    aadhar_number = models.CharField(max_length=20, default="")
    pancard_number = models.CharField(max_length=20, default="")
    descripation = models.TextField()
    image = models.ImageField(upload_to="teacher", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)

    def __str__(self):
        return self.username


class Role(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default="")
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.user.username
