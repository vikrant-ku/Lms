from django.db import models

class Staff(models.Model):

    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=6, default="")
    dob = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    zipcode = models.CharField(max_length=10, default="")
    phone = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length = 254, default="")
    role = models.CharField(max_length=20, default="")
    basic_salary = models.CharField(max_length=30, default="")
    aadhar_number = models.CharField(max_length=20, default="")
    image = models.ImageField(upload_to="teacher", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)

    def __str__(self):
        return self.first_name