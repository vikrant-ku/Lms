from django.shortcuts import render, redirect
from django.views import View
from admins.models.professor import Teacher
from admins.models.staff import Staff
from admins.models.students import Students
from admins.models.fees import Fees, Student_fees
from admins.models.attandance import Teacher_Attandance
from admins.models.classes import Class
from admins.models.leave import Leave


from .login import validate_user
from datetime import date

class Index(View):
    update = False
    def get(self, request):
        if validate_user(request):
            tchr_count = Teacher.objects.all().count()
            staff_count = Staff.objects.all().count()
            std_count = Students.objects.all().count()
            current_month = date.today().strftime('%B')
            fees = Student_fees.objects.filter(month=current_month[:3:].upper())
            collection = 0
            for fee in fees:
                collection+= fee.amount

            tchr_attand = Teacher_Attandance.objects.filter(attandance='P', datetime__year=date.today().year, datetime__month=date.today().month, datetime__day=date.today().day).count()
            all_cls = Class.objects.all().count()
            all_leaves = Leave.objects.filter(is_teacher=True, status="Pending").count()
            data = {'tchr_count':tchr_count, 'staff_count':staff_count,'std_count':std_count,'month':current_month,
                    'collection':collection, 'tchr_attand':tchr_attand, 'all_cls':all_cls, "all_leaves":all_leaves }
            return render(request, 'lms_admin/index.html', data)
        else:
            return redirect('teacher_login')

