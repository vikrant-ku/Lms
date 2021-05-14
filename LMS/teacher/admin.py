from django.contrib import admin
from .models import Assignment, OnlineClass, Marks

# Register your models here.
class Assignment_Admin(admin.ModelAdmin):
    list_display = ('teacher', 'class_name', 'section', 'subject')

class OnliceClass_Admin(admin.ModelAdmin):
    list_display = ('teacher', 'class_name', 'section', 'subject', 'date','start_time', 'end_time')

class Marks_Admin(admin.ModelAdmin):
    list_display = ('student', 'class_name', 'section', 'subject', 'exam_type')


admin.site.register(Assignment, Assignment_Admin)
admin.site.register(OnlineClass, OnliceClass_Admin)
admin.site.register(Marks, Marks_Admin)