from django.shortcuts import render , redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from admins.models.professor import Teacher
from admins.models.leave import Leave
from admins.models.students import Students
from admins.models.notice import Notices, Event, Notification
from admins.models.attandance import Teacher_Attandance
from library.models import Books
from library.models import Issue_book
from student.views.index import get_notifications
import datetime
from .books import user_validate


class Index(View):
    def get(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            all_books_count = Books.objects.all().count()
            issue_book_count= Issue_book.objects.all().count()
            data = {'notify': notify, 'notifications': notification,'book_count':all_books_count, 'issue_book_count':issue_book_count}
            return render(request, 'library/index.html', data)
        else:
            return redirect('teacher_login')

class Update_profile(View):
    def get(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification,'user':user}
            # ------end  notification

            return render(request, 'teachers/edit-profile.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if user_validate(request):
            data = request.POST
            try:
                image = request.FILES['image']
            except:
                image = None

            user = get_object_or_404(Teacher, username=request.session.get('user'))
            gender = data.get('gender')

            user.first_name = data.get('firstname')
            user.last_name = data.get('lastname')
            user.dob = data.get('dob')
            user.address = data.get('address')
            user.country = data.get('country')
            user.state = data.get('state')
            user.city = data.get('city')
            user.zipcode = data.get('postcode')
            user.phone = data.get('mobileno')
            user.email = data.get('email')
            user.designation = data.get('designation')
            user.qualification = data.get('qualification')
            user.basic_salary = data.get('salary')
            user.contract_type = data.get('contract')
            user.work_shift = data.get('shift')
            # account info
            user.bank_name = data.get('bank')
            user.branch_name = data.get('branch')
            user.account_number = data.get('account')
            user.ifsc_code = data.get('ifsc')
            user.aadhar_number = data.get('aadhar')
            user.pancard_number = data.get('pan')
            user.descripation = data.get('description')

            if gender is not None:
                user.gender = gender
            if image is not None:
                user.image = image
            user.save()
            messages.success(request, 'Your Profile Updated successfully. ')
            return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class Events(View):
    def get(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            events = Event.objects.all().order_by('start_date')
            data = {'notify': notify, 'notifications': notification, 'events': events}
            return render(request, 'library/events.html', data)
        else:
            return redirect('teacher_login')

class Apply_leave(View):
    def get(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification,}
            # ------end  notification
            return render(request, 'library/apply-leave.html', data)
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
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            leaves = Leave.objects.filter(teacher=user.pk).order_by('start_date')
            data = {'notify': notify, 'notifications': notification,'all_leaves': leaves}
            return render(request, 'library/view-leave.html', data)
        else:
            return redirect('teacher_login')

class All_notice(View):
    def get(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification

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
            data = {'notify': notify, 'notifications': notification,'all_notice': all_notice}
            return render(request, 'library/notice.html', data)
        else:
            return redirect('teacher_login')


class View_attandance(View):
    def get(self, request):
        if user_validate(request):
            today = datetime.datetime.today()
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            year = request.GET.get('year')
            month = request.GET.get('month')

            mnth = [str(i) for i in range(1, 13)]
            if month in mnth:
                attandance = Teacher_Attandance.objects.filter(teacher=user.id, datetime__year=year,
                                                               datetime__month=int(month))
            else:
                attandance = None
            data = {'notify': notify, 'notifications': notification,'year': today.year, 'attandance': attandance}
            return render(request, 'library/view-attandance.html', data)
        else:
            return redirect('teacher_login')



class Change_password(View):
    def get(self, request):
        user = get_object_or_404(Teacher, username=request.session.get('user'))
        ## for notification
        noti_info = get_notifications(user)
        notify = noti_info[0]
        notification = noti_info[1]
        data = {'notify': notify, 'notifications': notification}
        return render(request, "library/change_password.html",data)
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


class Send_Notification(View):
    def get(self, request):
        if user_validate(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            data = {'notify': notify, 'notifications': notification}
            return render(request, 'library/send-notification.html', data)
        return redirect('teacher_login')

    def post(self, request):
        if user_validate(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            data = {'notify': notify, 'notifications': notification}

            notification_msg = request.POST.get('notification')
            username = request.POST.get('username')
            if 'TE' in username:
                messages.error(request, "You can not send notification to Teacher")
            elif "ST" in username:
                user = get_object_or_404(Students, username=username)
                notification = Notification(student=user, from_user=teacher, notification=notification_msg)
                notification.save()
                messages.success(request, f'Notification Send to {user.username} successfully')

            return redirect('library_send_notification')
        return redirect('teacher_login')


class View_notification(View):
    def get(self, request, **kwargs):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
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
                all_notific = Notification.objects.filter(teacher= user).order_by('-datetime')
                unseen_notific = Notification.objects.filter(teacher= user, seen=False)
                for _ in unseen_notific:
                    _.seen=True
                    _.save()

            # for send notifications
            all_send_nofific = Notification.objects.filter(from_user= user).order_by('-datetime')

            #----------------------
            data['all_notific'] = all_notific
            data['all_send_nofific'] = all_send_nofific
            return render(request, 'library/view-notification.html', data)
        return redirect('login')

class Profile(View):
    def get(self, request):
        if user_validate(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification

            data = {'notify': notify, 'notifications': notification, 'teacher':teacher}
            return render(request, 'library/profile.html', data)
        return redirect('teacher_login')

class Update_profile(View):
    def get(self, request):
        if user_validate(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            data = {'notify': notify, 'notifications': notification, 'teacher': teacher}
            return render(request, 'library/edit-profile.html', data)
        return redirect('teacher_login')

    def post(self, request):
        if user_validate(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            data = request.POST
            try:
                image = request.FILES['image']
            except:
                image = None

            firstname = data.get('firstname')
            lastname = data.get('lastname')
            gender = data.get('gender')
            dob = data.get('dob')
            address = data.get('address')
            country = data.get('country')
            state = data.get('state')
            city = data.get('city')
            postcode = data.get('postcode')
            mobileno = data.get('mobileno')
            email = data.get('email')
            designation = data.get('designation')
            qualification = data.get('qualification')
            salary = data.get('salary')
            contract = data.get('contract')
            shift = data.get('shift')
            bank = data.get('bank')
            branch = data.get('branch')
            account = data.get('account')
            ifsc = data.get('ifsc')
            pan = data.get('pan')
            aadhar = data.get('aadhar')
            description = data.get('description')

            user.first_name = firstname
            user.last_name = lastname
            user.dob = dob
            user.address = address
            user.country = country
            user.state = state
            user.city = city
            user.zipcode = postcode
            user.phone = mobileno
            user.email = email
            user.designation = designation
            user.qualification = qualification
            user.basic_salary = salary
            user.contract_type = contract
            user.work_shift = shift
                # account info
            user.bank_name = bank
            user.branch_name = branch
            user.account_number = account
            user.ifsc_code = ifsc
            user.aadhar_number = aadhar
            user.pancard_number = pan
            user.descripation = description

            if gender is not None:
                user.gender = gender
            if image is not None:
                user.image = image
            user.save()
            return redirect('library_profile')
        return redirect('teacher_login')





