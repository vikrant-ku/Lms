from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admins.models.notice import Notices, Event, Notification, Feedback
from admins.models.leave import Leave
from admins.models.students import Students
from django.contrib import messages
import datetime
from .index import validate_user, get_notifications

class Events(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]

            # ------end  notification
            events = Event.objects.all().order_by('start_date')
            data = {'events': events,'notify': notify, 'notification': notification}
            return render(request, 'students/events.html', data)
        return redirect('login')


class All_notice(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            all_notice = Notices.objects.filter(recipient='Students')|Notices.objects.filter(recipient='All')

            data = {'all_notice' : all_notice, 'notify': notify, 'notification': notification}
            return render(request, 'students/notice.html', data)
        else:
            return redirect('login')

class Apply_leave(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data ={'notify':notify, 'notification':notification}
            # ------end  notification
            return render(request, 'students/apply-leave.html', data)
        else:
            return redirect('login')

    def post(self, request):
        if validate_user(request):
            data= request.POST
            validate_user(request)
            leave_type = data.get('leave-type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')


            reason = data.get('reason')
            halfday = data.get('halfday', False)
            today = datetime.date.today()
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()# convert srt date to datetime
            if end_date != "":
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()# convert srt date to datetime

                if end_date < start_date:
                    messages.error(request, "Start Date is grater than End Date")
                    return redirect('apply_leave')

            if today <= start_date:

                user = get_object_or_404(Students, username=request.session.get('user'))
                leave = Leave(
                    student= user,
                    type = leave_type,
                    start_date = start_date,
                    reason = reason,
                    is_student = True,
                )
                if halfday:
                    leave.halfday = True
                if end_date != "":
                    leave.end_date = end_date
                leave.save()
            else:
                messages.error(request, 'Please check you date ')

            return redirect('apply_leave')
        return redirect('login')

class All_leaves(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            #------end  notification

            leaves = Leave.objects.filter(student=user.id)
            data = {'all_leaves' :leaves,'notify':notify, 'notification':notification }
            return render(request, 'students/view-leave.html', data)
        return redirect('login')

class View_notification(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification}

            pk = request.GET.get('id')
            all_notific = list()
            if pk is not None:
                notific = get_object_or_404(Notification, pk=pk)
                notific.seen = True
                notific.save()
                all_notific.append(notific)
            else:
                all_notific = Notification.objects.filter(student= user).order_by('-datetime')
                unseen_notific = Notification.objects.filter(student= user, seen=False)
                for _ in unseen_notific:
                    _.seen=True
                    _.save()
            data['all_notific'] = all_notific
            return render(request, 'students/view-notification.html', data)
        return redirect('login')


class Send_feedback(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification}
            return render(request, 'students/send-feedback.html', data)
        else:
            return redirect('login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            title = request.POST.get('title')
            msg = request.POST.get('msg')
            feedback = Feedback(student= user, title=title, message=msg)
            feedback.save()
            messages.success(request, f'your feedback has been sent successfully.')
            return redirect("send-feedback")
        else:
            return redirect('login')

class view_feedback(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            all_feedback = Feedback.objects.filter(student=user).order_by('-datetime')
            data = {'notify': notify, 'notifications': notification,'all_feedback':all_feedback}
            return render(request, 'students/view-feedback.html', data)

        else:
            return redirect('login')

class Delete_feedback(View):
    def post(self, request):
        if validate_user(request):
            pk = int(request.POST.get('pk'))
            feed = get_object_or_404(Feedback, pk=pk)
            feed.delete()

            return redirect('view_feedback')
        else:
            return redirect('login')

