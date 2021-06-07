from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from teacher.models import Assignment, OnlineClass
from admins.models.professor import Teacher, Role
from admins.models.classes import Class, Class_subjects, Syllabus
from library.models import Issue_book
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from admins.views.student import proper_pagination
from django.db.models import Q
from datetime import datetime
from student.views.index import get_notifications


class Index(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify':notify, 'notifications':notification}
            # ------end  notification
            data['user'] = user
            is_ct = is_class_teacher(request)
            data['is_ct']=is_ct
            return render(request, 'teachers/index.html', data)
        else:
            return redirect('teacher_login')

class Update_profile(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification}
            # ------end  notification

            data['user'] = user
            is_ct = is_class_teacher(request)
            data['is_ct']=is_ct
            return render(request, 'teachers/edit-profile.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
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




class Issue_books(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification

            issue_books = Issue_book.objects.filter(teacher= user.id)
            data = {'is_ct': True, 'all_issue_book': issue_books, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/all-issue-book.html', data)
        else:
            return redirect('teacher_login')

class Upload_assignment(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects,'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/upload-assignment.html',data)
        else:
            return redirect('teacher_login')

    def post(self,request):
        if validate_user(request):
            data = request.POST
            try:
                image = request.FILES['assignment']
            except:
                image = None
            class_name = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            due_date = data.get('due_date')

            username = request.session.get('user')
            user = get_object_or_404(Teacher, username = username)
            cls = get_object_or_404(Class, class_name=class_name)


            if image is not None:
                assign = Assignment(
                        teacher = user,
                        class_name = cls,
                        section = section,
                        subject = subject,
                        due_date = due_date,
                        assignment = image
                    )
                assign.save()
            else:
                messages.error(request, 'Please Upload Assignment !!')
            return redirect('upload_assignment')
        return redirect('teacger_login')

class View_assignment(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]

            # ------end  notification

            q = request.GET.get('q')
            if q is not None:
                assig = Assignment.objects.filter(
                    Q(class_name__class_name__icontains=q)
                    | Q(section__icontains=q)
                    | Q(subject__icontains=q)
                                       )
                if len(assig) > 0:
                    all_assig = assig
                else:
                    all_assig = Assignment.objects.filter(teacher=user.id)
            else:
                all_assig = Assignment.objects.filter(teacher=user.id)

            # paginator
            paginator = Paginator(all_assig, 10)
            page = request.GET.get('page')

            try:
                all_assign = paginator.page(page)
            except PageNotAnInteger:
                all_assign = paginator.page(1)
            except EmptyPage:
                all_assign = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(all_assign, index=3)
            page_range = list(paginator.page_range)[start_index:end_index]
            if page is None or page == 1:
                count = 1
            else:
                count = all_assign.start_index()
            data = {'is_ct': True, 'all_assign': all_assign, 'page_range': page_range, 'count': count, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            data['q']= q
            return render(request,'teachers/assignment.html', data)
        else:
            return redirect('teacher_login')


class Delete_assign(View):
    def get(self, request, pk):
        pk = pk
        assign = get_object_or_404(Assignment, pk=pk)
        assign.delete()
        return redirect('assignment')


class Schedule_class(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/schedule_class.html',data)
        else:
            return redirect('teacher_login')

    def post(self,request):
        if validate_user(request):
            data = request.POST
            class_name = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            date = data.get('date')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            link = data.get('link')
            msg = data.get('msg')

            starttime = datetime.strptime(start_time, '%H:%M')
            endtime = datetime.strptime(end_time, '%H:%M')
            if starttime>endtime or starttime==endtime:
                messages.error(request, "End time must be smaller than Start Time")
                return redirect('schedule_class')

            user = get_object_or_404(Teacher, username = request.session.get('user'))
            schdl_cls = OnlineClass.objects.filter(teacher=user.id, date=date)
            if len(schdl_cls)>0:
                for _ in schdl_cls:

                    if _.end_time <= starttime.time():
                        messages.error(request, f"You Already Schedule Class on {starttime.time()} Time.")
                        return redirect('schedule_class')
            cls = get_object_or_404(Class, class_name=class_name)
            online_class = OnlineClass(
                        teacher = user,
                        class_name = cls,
                        section = section,
                        subject = subject,
                        date = date,
                        start_time =start_time,
                        end_time = end_time,
                        link = link,
                        message= msg
                            )
            online_class.save()
            return redirect('schedule_class')
        return redirect('teacher_login')

class View_schedule_class(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            q = request.GET.get('q')
            if q is not None:
                allonlineclass = OnlineClass.objects.filter(
                    Q(class_name__class_name__icontains=q) |
                    Q(section__icontains=q) |
                    Q(subject__icontains=q) |
                    Q(date__icontains=q)
                )
            else:
                allonlineclass = OnlineClass.objects.filter(teacher=user.id)

            # paginator
            paginator = Paginator(allonlineclass, 1)
            last_page = paginator.page_range[-1]


            page = request.GET.get('page')

            try:
                onlineclass = paginator.page(page)
            except PageNotAnInteger:
                onlineclass = paginator.page(1)
            except EmptyPage:
                onlineclass = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(onlineclass, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = onlineclass.start_index()

            data = {'onlineclasses': onlineclass, 'page_range': page_range, 'count': count,
                    'last_page': last_page, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            if q is not None:
                data['q']= q
            return render(request, 'teachers/view-schedule-classes.html', data)
        else:
            return redirect('teacher_login')

class Delete_schedule_class(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            cls = get_object_or_404(OnlineClass, pk=pk)
            cls.delete()
            messages.success(request, "Scheduled Class deleted Successfully .")
            return redirect('view_schedule_class')
        else:
            return redirect('teacher_login')

class Upload_syllabus(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects,'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/upload_syllabus.html',data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            try:
                file = request.FILES['syllabus']
            except:
                file = None
            class_name = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            cls = get_object_or_404(Class, class_name=class_name)
            if file is not None:
                try:
                    syllabus = Syllabus.objects.get(class_name=cls, section=section, subject=subject)
                    syllabus.class_name = cls
                    syllabus.section = section
                    syllabus.subject = subject
                    syllabus.syllabus = file
                    syllabus.save()
                    messages.success(request, f'Syllabus Updated successfully')
                except:
                    syllabus = Syllabus(class_name=cls, section=section, subject=subject, syllabus=file)
                    syllabus.save()
                    messages.success(request, f'Syllabus added successfully')
            else:
                messages.error(request, 'Please Upload syllabus.')
            return redirect('teacher_upload_syllabus')
        else:
            return redirect('teacher_login')

class View_syllabus(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            data = {'classes': classes, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/view-syllabus.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            data = request.POST
            #send cls in dropdown
            classes = Class.objects.all()

            cls = data.get('class')
            section = data.get('section')
            clss = get_object_or_404(Class, class_name=cls)
            all_syllabus = Syllabus.objects.filter(class_name=clss.id,section=section,)
            data = {'classes': classes, 'all_syllabus':all_syllabus, 'notify': notify, 'notifications': notification}

            return render(request, 'teachers/view-syllabus.html', data)
        else:
            return redirect('teacher_login')




def validate_user(request):
    username = request.session.get('user')
    if 'TE' not in username:
        return False
    else:
        try:
            user = Teacher.objects.get(username=username)
        except:
            user= None
        if user is None:
            return False
        try:
            teacher_role = Role.objects.get(user=user)
        except:
            return True
        role = ['Librarian', 'Admin',]
        if teacher_role.role in role:
            return False
        else:
            return True

def is_class_teacher(request):
    user_name = request.session.get('user')
    user = get_object_or_404(Teacher, username=user_name)
    try:
        teacher_role = Role.objects.get(user=user.id)
        if teacher_role.role == "Class Teacher":
            return True
        else:
            return False
    except:
        return False


