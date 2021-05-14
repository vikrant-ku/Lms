from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from admins.models.professor import Teacher, Role
from admins.models.attandance import Teacher_Attandance
from .login import validate_user

import datetime

class Attandance(View):
    def get(self, request):
        if validate_user(request):
            today = datetime.date.today()
            data = {'date': today}
            attand = Teacher_Attandance.objects.filter(datetime__year=today.year, datetime__month=today.month, datetime__day=today.day)
            if len(attand) > 0:
                data['marked'] = True  # if today attandace already marked

            teachers = Teacher.objects.all()
            data['teachers'] = teachers
            return render(request, 'lms_admin/mark-attandance.html', data)
        else:
            return redirect('teacher_login')


    def post(self, request):
        if validate_user(request):
            data = request.POST
            teacher = data.getlist('id')
            attand = data.getlist('attandance')

            for _ in range(len(teacher)):
                user = get_object_or_404(Teacher, pk=int(teacher[_]))
                attandance = Teacher_Attandance(
                                            teacher=user,
                                            attandance = attand[_]
                                            )
                attandance.save()
            messages.success(request,f"Attandance for {datetime.date.today()} is marked successfully")
            return redirect('admin_mark_attandance')
        else:
            return redirect('teacher_login')


class Update_attandance(View):
    def get(self, request):
        if validate_user(request):
            data = {}
            user = request.GET.get('username', None)
            date = request.GET.get('date', None)

            if user is not None and date is not None:

                date = date.split('-')
                teacher = get_object_or_404(Teacher, username=user)

                attandance = Teacher_Attandance.objects.filter(teacher=teacher.id, datetime__year=date[0],datetime__month=date[1], datetime__day=date[2])
                if len(attandance)==1:
                    data['attandance']= attandance[0]

            return render(request, 'lms_admin/update-attandance.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            attand= request.POST.get('attandance')
            id= request.POST.get('id')
            attandance= get_object_or_404(Teacher_Attandance, pk=int(id))
            attandance.attandance = attand
            attandance.save()
            messages.success(request, "Attandance Successfully Updated")
            return redirect('admin_update_attandance')
        else:
            return redirect('teacher_login')

class View_teacher_attand(View):
    def get(self, request):
        if validate_user(request):
            today = datetime.date.today()
            data = {'year': today.year}
            months = [str(i) for i in range(1, 13)]
            month = request.GET.get('month')
            year = request.GET.get('year')
            if month in months:
                # get all dates when attandance marked
                date = Teacher_Attandance.objects.filter(datetime__year=year, datetime__month=int(month)).order_by('datetime__day').values_list('datetime', flat=True).distinct()

                teachers = Teacher_Attandance.objects.filter(datetime__year=year, datetime__month=int(month)).values_list('teacher', flat=True).distinct()
                allattandance = dict()
                for i in teachers:
                    attand = []
                    for d in date:
                        dates =d.date()
                        attand_by_date = Teacher_Attandance.objects.filter(datetime__date=dates,teacher=i).order_by('datetime__day').values_list('attandance', flat=True)
                        # if teacher attandance available in date then add date else set - .
                        if len(attand_by_date)>0:
                            attand.append(attand_by_date)
                        else:
                            attand.append("-")
                    teacher = get_object_or_404(Teacher, pk=i)
                    # add teacher object as a key and add attandane list as a value
                    allattandance[teacher] = attand

                data['dates'] = date
                data['allattandance'] = allattandance

            return render(request, 'lms_admin/view-teacher-attandance.html', data)
        else:
            return redirect('teacher_login')



