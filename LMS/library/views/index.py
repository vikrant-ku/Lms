from django.shortcuts import render , redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from admins.models.professor import Teacher
from admins.models.leave import Leave
from admins.models.notice import Notices, Event
from admins.models.attandance import Teacher_Attandance
from library.models import Books
from library.models import Issue_book

import datetime


from .books import user_validate


class Index(View):
    def get(self, request):
        if user_validate(request):
            all_books_count = Books.objects.all().count()
            issue_book_count= Issue_book.objects.all().count()
            data = {'book_count':all_books_count, 'issue_book_count':issue_book_count}
            return render(request, 'library/index.html', data)
        else:
            return redirect('teacher_login')

class Events(View):
    def get(self, request):
        if user_validate(request):
            events = Event.objects.all().order_by('start_date')
            data = {'events': events}
            return render(request, 'library/events.html', data)
        else:
            return redirect('teacher_login')

class Apply_leave(View):
    def get(self, request):
        if user_validate(request):
            return render(request, 'library/apply-leave.html')
        else:
            return redirect('teacher_login')


    def post(self, request):
        if user_validate(request):
            data= request.POST

            leave_type = data.get('leave-type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            reason = data.get('reason')
            halfday = data.get('halfday', False)
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()  # convert srt date to datetime
            if end_date != "":
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()  # convert srt date to datetime

                if end_date < start_date:
                    messages.error(request, "Start Date is grater than End Date")
                    return redirect('library_apply_leave')

            username = request.session.get('user')
            user = get_object_or_404(Teacher, username=username)
            leave = Leave(
                teacher = user,
                type = leave_type,
                start_date = start_date,
                reason = reason,
                is_teacher = True,
            )
            if end_date != "" and halfday == True:
                leave.halfday = True
            if end_date != "":
                leave.end_date = end_date
            leave.save()

            return redirect('library_apply_leave')
        else:
            return redirect('teacher_login')

class View_leave(View):
    def get(self, request):
        if user_validate(request):
            username = request.session.get('user')
            user = get_object_or_404(Teacher,username=username)
            leaves = Leave.objects.filter(teacher=user.pk).order_by('start_date')
            data = {'all_leaves': leaves,}
            return render(request, 'library/view-leave.html', data)
        else:
            return redirect('teacher_login')

class All_notice(View):
    def get(self, request):
        if user_validate(request):

            q = request.GET.get('q')
            if q is not None:
                notices = Notices.objects.filter(Q(recipient__icontains=q)
                                                 | Q(type__icontains=q))
                if (len(notices) > 0):
                    all_notice = notices
                else:
                    all_notice = Notices.objects.filter(Q(recipient__icontains="All") |
                                                        Q(recipient__icontains="Teacher")).order_by('-date')

            else:
                all_notice = Notices.objects.filter(Q(recipient__icontains="All") |
                                                    Q(recipient__icontains="Teacher")).order_by('-date')
            data = {'all_notice': all_notice}
            return render(request, 'library/notice.html', data)
        else:
            return redirect('teacher_login')


class View_attandance(View):
    def get(self, request):
        if user_validate(request):
            today = datetime.datetime.today()
            username = request.session.get('user')
            user = get_object_or_404(Teacher, username=username)
            year = request.GET.get('year')
            month = request.GET.get('month')

            mnth = [str(i) for i in range(1, 13)]
            if month in mnth:
                attandance = Teacher_Attandance.objects.filter(teacher=user.id, datetime__year=year,
                                                               datetime__month=int(month))
            else:
                attandance = None
            data = {'year': today.year, 'attandance': attandance}
            return render(request, 'library/view-attandance.html', data)
        else:
            return redirect('teacher_login')



class Change_password(View):
    def get(self, request):

        return render(request, "library/change_password.html",)
    def post(self, request):
        old_pass = request.POST.get('old_pass')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:
            username = request.session.get('user')
            user = get_object_or_404(Teacher, username=username)
            flag = check_password(old_pass, user.password)
            if flag:
                user.password = make_password(pass1)
                user.save()
                messages.success(request, 'Your Password Successfully changed. ')
            else:
                messages.error(request, 'Please Check Your Password')
        else:
            messages.error(request, "New Password and Confirm Password Do not Match !")
        return redirect('library_change_password')






