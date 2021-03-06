from django.shortcuts import render , redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views import View
from admins.models.classes import Class
from django.contrib.auth.models import User
from admins.models.students import Students
from admins.models.professor import Teacher, Role

class Reset_password(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'lms_admin/password-recovery.html')
        return redirect('teacher_login')


    def post(self, request):
        if validate_user(request):
            data = request.POST
            username = data.get('username')
            pass1 = data.get('pass1')
            pass2 = data.get('pass2')
            print(type(pass1))
            user = None
            if pass1 == pass2:
                if "ST" in username:
                    try:
                       user = Students.objects.get(username= username)
                    except:
                        messages.error(request, "User is Not Exist")

                elif "TE" in username:
                    try:
                       user = Teacher.objects.get(username= username)
                    except:
                        messages.error(request, "User is Not Exist")

                if user:
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request, f"{user.username} password successfully changed")

            else:
                messages.error(request,"Password Do not Match")

            return redirect("reset_password")
        return redirect('teacher_login')

import xlwt
class Reset_password_all(View):
    def get(self, request):
        if validate_user(request):

            class_name = request.GET.get('class_name')
            section = request.GET.get('section')
            cls = get_object_or_404(Class, class_name=class_name)

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Student-'+class_name+section+'.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')

            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Username', 'First Name', 'Last Name', 'Password']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

                # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            all_stud = Students.objects.filter(class_name=cls.id,section=section)
            if len(all_stud)>0:
                for i in all_stud:
                    pswrd = random_password()
                    i.password = make_password(pswrd)
                    i.save()
                    row_num += 1
                    ws.write(row_num,0, i.username,font_style)
                    ws.write(row_num,1, i.first_name,font_style)
                    ws.write(row_num,2, i.last_name,font_style)
                    ws.write(row_num,3, pswrd,font_style)

                wb.save(response)
                return response
            else:
                messages.error(request, 'Please Check Class or section')
            return redirect("admin_home")
        return redirect('teacher_login')


def validate_user(request):
    username = request.session.get('user')
    if "TE" not in username:
        try:
            superuser = User.objects.get(username=username)
            return True
        except:
            return False
    try:
        user = Teacher.objects.get(username= username)
    except:
        return False

    role = get_object_or_404(Role, user = user)
    if role.role == "admin" or role.role == 'Admin':
        return True


import string
import random


def random_password(n=6):
    LETTERS = string.ascii_letters
    NUMBERS = string.digits
    printable = f'{LETTERS}{NUMBERS}'
    printable = list(printable)
    random.shuffle(printable)
    random_password = random.choices(printable, k=n)
    random_password = ''.join(random_password)

    return str(random_password)