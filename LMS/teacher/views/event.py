from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from admins.models.notice import Notices, Event, Notification
from admins.models.professor import Teacher, Role
from admins.models.leave import Leave
from datetime import date
from django.contrib import messages
from .index import validate_user,is_class_teacher
from student.views.index import get_notifications
from django.db.models import Q


class Events(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            events = Event.objects.all().order_by('start_date')
            data = {'events': events, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/events.html', data)
        else:
            return redirect('teacher_login')


class All_notice(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            q = request.GET.get('q')
            if q is not None:
             all_notice = Notices.objects.filter(Q(recipient__icontains=q) | Q(type__icontains=q)).order_by('-date')
            else:
                all_notice = Notices.objects.filter(Q(recipient="All") | Q(recipient="Teacher")).order_by('-date')
            data = {'all_notice' : all_notice, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/notice.html', data)
        else:
            return redirect('teacher_login')

class Apply_leave(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            is_ct = is_class_teacher(request)
            data={'is_ct':is_ct, 'notify': notify, 'notifications': notification}
            return render(request, 'teachers/apply-leave.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            data= request.POST
            validate_user(request)
            leave_type = data.get('leave-type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            reason = data.get('reason')
            halfday = data.get('halfday', False)
            today = date.today()

            username = request.session.get('user')
            user = get_object_or_404(Teacher, username=username)
            leave = Leave(
            teacher = user,
            type = leave_type,
            start_date = start_date,
            reason = reason,
            is_teacher = True,
                )
            if halfday == True:
                leave.halfday = True
            if end_date != "":
                leave.end_date = end_date
            leave.save()

            return redirect('teacher_apply_leave')
        else:
            return redirect('teacher_login')

class Students_leave(View):
    def get(self, request):
        if validate_user(request):

            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            try:
                user_role = Role.objects.get(user = user.id)
            except:
                user_role = None
            if user_role is not None and user_role.role == "Class Teacher":
                leaves = Leave.objects.filter(is_student = True).order_by('-start_date')
                data = {'all_leaves':leaves, 'is_student':True, 'notify': notify, 'notifications': notification}
                is_ct = is_class_teacher(request)
                data['is_ct'] = is_ct
                return render(request, 'teachers/view-leave.html', data)
            else:
                messages.error(request, 'You are not class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class student_leave_status(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            status = kwargs.get('status')
            leave = get_object_or_404(Leave, pk=pk)
            leave.status=status
            leave.save()
            return redirect('teacher_students_leave')
        else:
            return redirect('teacher_login')


class View_leave(View):
    def get(self, request):
        if validate_user(request):

            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            leaves = Leave.objects.filter(teacher=user.pk).order_by('start_date')
            data = {'all_leaves': leaves, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/view-leave.html', data)
        else:
            return redirect('teacher_login')



