from django.shortcuts import render , redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views import View
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





