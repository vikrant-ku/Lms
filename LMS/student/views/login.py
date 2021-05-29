from django.shortcuts import render , redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.views import View
from admins.models.students import Students
from .index import validate_user , get_notifications
from datetime import date
from admins.models.leave import Leave
import random
import string
today = date.today()

class Login(View):
    update = False
    def get(self, request):
        # for change all leave previous leave status
        if self.update is False:
            reject_leave()
            self.update = True
        is_student = True
        data = {'is_student':is_student}
        return render(request, 'lms_admin/login.html', data)


    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = None
        if "ST" in username:
            try:
                user = Students.objects.get(username=username)
            except:
                messages.error(request, "User dose'nt Exist")

        if user is not None:
            if user.is_login:
                return render(request, 'lms_admin/Login-error.html',{"user":user})
            else:
                flag = check_password(password, user.password)
                if flag:
                    # is_login is for user can't login more than one device
                    user.is_login = True
                    user.token = otp_gen(10)
                    user.save()
                    request.session['user'] = user.username
                    request.session['name'] = user.first_name
                    request.session['token'] = user.token
                    if password==123 or password=='123':
                        messages.warning(request, "For Security Reason Please Change Your Password.")
                        return redirect('change_password')
                    messages.success(request, 'You Are Successfully Login')
                    return redirect('student_home')
                else:
                    messages.error(request, "Password Do not match")
        else:
            messages.error(request, 'Please check username')
        return redirect("login")

class Logout(View):
    def get(self, request):
        username = request.session.get('user')
        if "ST" in username:
            student = get_object_or_404(Students, username=username)
            student.is_login = False
            student.save()
        request.session.pop('user')
        request.session.pop('name')
        messages.success(request, f"{username} successfully logout ")
        return redirect('login')

class Logout_all_devices(View):
    def post(self, request):
        username = request.POST.get('username')
        student = get_object_or_404(Students, username=username)
        student.is_login=False
        student.save()
        messages.success(request, "You are Successfully logout form all devices")
        return redirect('login')

class Change_password(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            data = {'notify':notify,'notification':notification }
            return render(request, "students/change_password.html", data)
        else:
            return redirect('login')
    def post(self, request):
        if validate_user(request):
            old_pass = request.POST.get('old_pass')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if pass1 == pass2:
                username = request.session.get('user')
                user = get_object_or_404(Students, username=username)
                flag = check_password(old_pass, user.password)
                if flag:
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request, "Password Changed Successfully.")
                else:
                    messages.error(request, 'Please Check Your Password')
            else:
                messages.error(request, "New Password and Confirm Password Do not Match !")
            return redirect('change_password')
        else:
            return redirect('login')



# if leave is not responced before end date then change status to reject
def reject_leave():
    leaves = Leave.objects.all()
    for leave in leaves:
        if leave.end_date is not None:
            if leave.end_date < today:
                leave.status = 'Reject'
                leave.save()
        else:
            if leave.start_date < today:
                leave.status = 'Reject'
                leave.save()

def otp_gen(size):
    generate_pass = ''.join([random.choice(string.ascii_uppercase +
                                           string.ascii_lowercase +
                                           string.digits)
                             for n in range(size)])

    return generate_pass
