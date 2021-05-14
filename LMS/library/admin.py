from django.contrib import admin
from .models import Books, Issue_book


class Books_admin(admin.ModelAdmin):
    list_display = ('book_name','auther_name', 'publication', 'subject')


class Issue_book_admin(admin.ModelAdmin):
    list_display = ( 'book','teacher', 'student',)


admin.site.register(Books, Books_admin)
admin.site.register(Issue_book, Issue_book_admin)