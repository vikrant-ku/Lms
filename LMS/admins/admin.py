from django.contrib import admin
from .models.students import Students, Documents
from .models.professor import Teacher, Role
from .models.classes import Class, Class_subjects, Syllabus
from .models.notice import Notices, Event,Notification, Feedback
from .models.leave import Leave
from .models.staff import Staff
from .models.attandance import Student_Attandance, Teacher_Attandance
from .models.fees import Fees, Student_fees, Academic_Year, Fee_discount
from import_export.admin import ImportExportModelAdmin


class StudentDocumentInline(admin.TabularInline):
    model = Documents

class StudentFeeDiscountInline(admin.TabularInline):
    model = Fee_discount

@admin.register(Students)
class Student_Admin(ImportExportModelAdmin):
    list_display = ('username', 'admission_no', 'first_name', 'class_name','section', )
    list_filter = ('class_name', 'section')
    search_fields = ['username', 'admission_no','first_name', 'last_name',]
    inlines = [
        StudentDocumentInline,
        StudentFeeDiscountInline
    ]

@admin.register(Teacher)
class Teacher_Admin(ImportExportModelAdmin):
    list_display = ('username', 'first_name', 'last_name','work_shift', )
    list_filter = ('work_shift',)
    search_fields = ['username','first_name', 'last_name',]

class Staff_Admin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role',)
    list_filter = ('role',)
    search_fields = ['first_name', 'last_name', 'email', 'role', 'aadhar_number' ]


class Notice_Admin(admin.ModelAdmin):
    list_display = ('recipient', 'type', 'date')
    list_filter = ('recipient', 'type', 'date')
    search_fields = ['recipient', 'type', ]

class Subject_Admin(admin.ModelAdmin):
    list_display = ('class_name', 'section')
    list_filter = ('class_name', 'section')

class Leave_admin(admin.ModelAdmin):
    list_display = ('type','teacher', 'student', 'start_date', 'end_date', 'halfday', 'status', 'is_teacher', 'is_student')
    list_filter = ('halfday', 'status', 'is_teacher', 'is_student')


class Role_admin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role', 'class_name')

class Event_admin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date')

class Teachet_Attandance_Admin(admin.ModelAdmin):
    list_display = ('teacher', 'attandance', 'datetime')
    search_fields = ['teacher__username' ]

class Student_fee_Admin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'month', 'status')
    list_filter = ('month', 'status')
    search_fields = ['student__username']

class Feedback_Admin(admin.ModelAdmin):
    list_display = ('student', 'title', 'datetime')
    list_filter = ('seen',)





admin.site.register(Staff, Staff_Admin)
admin.site.register(Class)
admin.site.register(Class_subjects, Subject_Admin)
admin.site.register(Role, Role_admin)
admin.site.register(Leave, Leave_admin)
admin.site.register(Event, Event_admin)
admin.site.register(Notices, Notice_Admin)
admin.site.register(Student_Attandance)
admin.site.register(Teacher_Attandance, Teachet_Attandance_Admin)
admin.site.register(Fees)
admin.site.register(Fee_discount)
admin.site.register(Academic_Year)
admin.site.register(Student_fees,Student_fee_Admin )
admin.site.register(Syllabus)
admin.site.register(Documents)
admin.site.register(Notification)
admin.site.register(Feedback, Feedback_Admin)


