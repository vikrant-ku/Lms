from django.db import models
from admins.models.professor import Teacher
from admins.models.students import Students

class Books(models.Model):
    book_name = models.CharField(max_length=50, default="")
    auther_name = models.CharField(max_length=30, default="")
    publishing_year = models.CharField(max_length=10, default="")
    isbn_number = models.CharField(max_length=20, default="", unique=True)
    publication = models.CharField(max_length=20, default="")
    edition = models.CharField(max_length=10, default="")
    subject = models.CharField(max_length=50, default="")
    number_of_copies = models.CharField(max_length=20, default="")
    price = models.CharField(max_length=10, default="20")
    cupbord_number = models.CharField(max_length=10, default="")
    rack_number = models.CharField(max_length=10, default="")
    date = models.DateTimeField(verbose_name='Add date', auto_now_add=True)

    def __str__(self):
        return self.book_name

class Issue_book(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateField( auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.book.book_name





