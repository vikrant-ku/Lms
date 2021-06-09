from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from admins.models.students import Students, Documents
from admins.models.fees import Student_fees, Academic_Year
from admins.models.professor import Teacher, Role
from admins.models.classes import Class, Class_subjects
from admins.models.attandance import Student_Attandance, Teacher_Attandance
from admins.models.notice import Notification
from teacher.models import Marks
from .index import is_class_teacher, validate_user
from student.views.index import get_notifications
import datetime
import decimal


class All_students(View):
    def get(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                user = get_object_or_404(Teacher, username=request.session.get('user'))
                ## for notification
                noti_info = get_notifications(user)
                notify = noti_info[0]
                notification = noti_info[1]
                # ------end  notification
                teacher_role = get_object_or_404(Role, user=user.id)

                students = Students.objects.filter(class_name=teacher_role.class_name, section=teacher_role.section)
                data = {'students':students, 'notify': notify, 'notifications': notification}
                is_ct = is_class_teacher(request)
                data['is_ct'] = is_ct
                return render(request, 'teachers/all-students.html', data )
            else:
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class Attandance(View):
    def get(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                user = get_object_or_404(Teacher, username=request.session.get('user'))
                ## for notification
                noti_info = get_notifications(user)
                notify = noti_info[0]
                notification = noti_info[1]
                # ------end  notification
                today = datetime.date.today()
                data = {'is_ct': True, 'date': today,'notify': notify, 'notifications': notification}
                attand = Student_Attandance.objects.filter(datetime__year=today.year, datetime__month=today.month, datetime__day=today.day)
                if len(attand)>0:
                 data['marked']=True # if today attandace already marked
                user_name = request.session.get('user')
                user = get_object_or_404(Teacher, username=user_name)
                teacher_role = get_object_or_404(Role, user=user.id)

                class_name = get_object_or_404(Class, class_name=teacher_role.class_name)
                students = Students.objects.filter(class_name=class_name.id , section=teacher_role.section)
                data['students'] = students
                is_ct = is_class_teacher(request)
                data['is_ct'] = is_ct
                return render(request, 'teachers/mark-attandance.html', data)
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                data = request.POST
                student = data.getlist('id')
                attand = data.getlist('attandance')
                academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
                for _ in range(len(student)):
                    user = get_object_or_404(Students, pk=int(student[_]))
                    cls = get_object_or_404(Class, class_name=user.class_name)
                    section = user.section
                    attandance = Student_Attandance(
                                            academic_year=academic,
                                            student=user,
                                            class_name = cls,
                                            section = section,
                                            attandance = attand[_],
                                            datetime = datetime.datetime.today()
                                                )
                    attandance.save()
                messages.success(request,f"Attandance for {datetime.date.today()} is marked successfully")
                return redirect('mark_attandnce')
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class View_attandance(View):
    def get(self, request):
        if validate_user(request):
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
            data = {'year':today.year, 'attandance':attandance, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/view-attandance.html', data)
        else:
            return redirect('teacher_login')

class Student_info(View):
    def get(self, request,username):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            if is_class_teacher(request):
                student = get_object_or_404(Students, username=username)

                data = {'student': student, 'is_ct': True, 'notify': notify, 'notifications': notification}

                try:
                    documents = Documents.objects.get(student=student)

                    data['documents']: documents
                except:
                    pass

                return render(request, 'teachers/student-info.html', data)
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        return redirect('teacher_login')

class Edit_student(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            if is_class_teacher(request):
                id = kwargs.get('username')
                user = Students.objects.get(username=id)
                classes = Class.objects.all()
                data = {'student':user , 'classes': classes,'is_ct': True, 'notify': notify, 'notifications': notification}
                return render(request, 'teachers/edit-student.html', data)
            return redirect("teacher_home")
        return redirect('login')

    def post(self, request, **kwargs):
        if validate_user(request):
            path = request.META['PATH_INFO']
            id = kwargs.get('username')
            try:
                image = request.FILES['image']
            except:
                image = None
            user = Students.objects.get(username=id)
            data = request.POST
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            fathername = data.get('fathername')
            mothername = data.get('mothername')
            admission_no = data.get('admno')
            address = data.get('address')
            country = data.get('country')
            state = data.get('state')
            city = data.get('city')
            postcode = data.get('postcode')
            image = data.get('image')
            phone = data.get('mobileno')
            dob = data.get('dob')
            class_name = data.get('class')
            section = data.get('section')
            gender = data.get('gender')
            is_rte = data.get('is_rte')

            if class_name is not None:
                try:
                    class_name = Class.objects.get(class_name=class_name)
                except:
                    messages.error(request, 'Class name is not valid or exist')
                    return HttpResponseRedirect(path)

            user.admission_no = admission_no
            user.first_name = firstname
            user.last_name = lastname
            user.father_name = fathername
            user.mother_name = mothername
            user.dob = dob
            user.address = address
            user.country = country
            user.state = state

            user.city = city
            user.zipcode = postcode
            user.phone = phone
            if gender is not None:
                user.gender = gender
            if class_name is not None:
                user.class_name = class_name
            if section is not None:
                user.section = section
            if image is not None:
                user.image = image
            if is_rte is not None:
                user.is_rte = True

            user.save()

            return HttpResponseRedirect(path)
        return redirect('login')

class View_students_attandance(View):
    def get(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                user = get_object_or_404(Teacher, username=request.session.get('user'))
                ## for notification
                noti_info = get_notifications(user)
                notify = noti_info[0]
                notification = noti_info[1]
                # ------end  notification
                today = datetime.date.today()
                data = {'is_ct': True,'year':today.year,'notify': notify, 'notifications': notification}
                months = [ str(i) for i in range(1,13)]
                month = request.GET.get('month')
                year = request.GET.get('year')
                if month in months:
                    #attandance = Student_Attandance.objects.filter(datetime__year=year, datetime__month=int(month))
                    date = Student_Attandance.objects.filter(datetime__year=year, datetime__month=int(month)).order_by('datetime__day').values_list('datetime__date', flat=True).distinct()
                    students = Student_Attandance.objects.filter(datetime__year=year, datetime__month=int(month)).values_list('student', flat=True).distinct()
                    allattandance = dict()
                    for i in students:
                        attand = []
                        for d in date:

                            attand_by_date = Student_Attandance.objects.filter(datetime__date=d,student=i).order_by('datetime__day').values_list('attandance', flat=True)
                            if len(attand_by_date) > 0:
                                attand.append(attand_by_date)
                            else:
                                attand.append("-")
                        #attand = Student_Attandance.objects.filter(datetime__year=year,datetime__month=int(month), student=i).order_by('datetime__day').values_list('attandance', flat=True)
                        student = get_object_or_404(Students,pk=i)
                        allattandance[student]= attand

                    # data['attandance']= attandance
                    data['dates']=date
                    data['allattandance']=allattandance

                    is_ct = is_class_teacher(request)
                    data['is_ct'] = is_ct
                    messages.success(request,"Information successfully Updated")
                return render(request, 'teachers/view-student-attandance.html', data)
            else:
                messages.error(request, 'You are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class Update_student_attandance(View):
    def get(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                user = get_object_or_404(Teacher, username=request.session.get('user'))
                ## for notification
                noti_info = get_notifications(user)
                notify = noti_info[0]
                notification = noti_info[1]
                # ------end  notification
                data = {'is_ct':True, 'notify': notify, 'notifications': notification}
                date = request.GET.get('date')
                if date is not None:
                    date = date.split('-')
                user_name = request.session.get('user')
                user = get_object_or_404(Teacher, username=user_name)
                teacher_role = get_object_or_404(Role, user=user.id)
                std_username = request.GET.get('username')
                if std_username is not None and date is not None:
                    student = get_object_or_404(Students,username=std_username)
                    if student.class_name == teacher_role.class_name and student.section == teacher_role.section:
                        attandance = Student_Attandance.objects.filter(student=student.id, datetime__year=date[0],datetime__month=date[1], datetime__day=date[2])
                        if len(attandance)==1:
                            data['attandance']=attandance[0]
                    else:
                        messages.error(request, "This Student is not in your class please Check Student ID .")

                return render(request, 'teachers/update-attandance.html', data)
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            if is_class_teacher(request):
                id = request.POST.get('id')
                attand= request.POST.get('attandance')
                attandance = get_object_or_404(Student_Attandance,pk=id)
                attandance.attandance = attand
                attandance.save()
                messages.success(request, 'Attandance Updated Successfully ')
                return redirect('update_student_attandnce')
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class Upload_marks(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
           # ------end  notification
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/upload-marks.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            today = datetime.date.today()
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()

            data = request.POST
            cls = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            clss = get_object_or_404(Class, class_name= cls)
            students = Students.objects.filter(class_name=clss.id, section=section)
            marks = Marks.objects.filter(class_name=clss.id, section=section, subject=subject,date_added__startswith=today )

            if len(marks) > 0:
                messages.error(request, f'You already Submitted {subject} marks for Class {cls} {section} . ')
                marked = True
            else:
                marked = False

            data = {'classes': classes, 'subjects': subjects,'class':cls,
                    'section':section, 'subject':subject, 'students':students, 'marked':marked,
                    'notify': notify, 'notifications': notification}
            return render(request, 'teachers/upload-marks.html', data)
        else:
            return redirect('teacher_login')

class Save_student_marks(View):
    def post(self, request):
        if validate_user(request):
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            data = request.POST
            std_id = data.getlist('id')
            obtain = data.getlist('obtain')
            remark = data.getlist('remarks')
            total = data.get('total')
            subject = data.get('subject')
            class_name = data.get('class')
            section = data.get('section')
            type = data.get('type')
            cls =  get_object_or_404(Class, class_name=class_name)
            for _ in range(len(std_id)):
                student = get_object_or_404(Students, pk=int(std_id[_]))
                marks = Marks(
                    academic_year=academic,
                    student=student,
                    class_name =cls,
                    section =section,
                    subject =subject,
                    obtain_marks = decimal.Decimal(obtain[_]),
                    total_marks =decimal.Decimal(total),
                    remarks=remark[_],
                    exam_type = type,
                    added_by = teacher
                )
                marks.save()
            return redirect('upload_marks')
        else:
            return redirect('teacher_login')

class View_marks(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects, 'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/view-marks.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification

            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0] # get academic year
            data = request.POST
            cls = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            type = data.get('type')
            clss = get_object_or_404(Class, class_name= cls)
            marks = Marks.objects.filter(academic_year=academic,class_name=clss.id, section=section, subject=subject, added_by=teacher.id, exam_type=type)

            data = {'classes': classes, 'subjects': subjects, 'marks':marks, 'notify': notify, 'notifications': notification }
            is_ct = is_class_teacher(request)
            data['is_ct'] = is_ct
            return render(request, 'teachers/view-marks.html', data)
        else:
            return redirect('teacher_login')

class update_student_mark(View):
    def get(self,request,**kwargs):
        if validate_user(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            pk = kwargs.get('pk')
            mark = get_object_or_404(Marks, pk=pk)
            data = {'mark':mark,'notify': notify, 'notifications': notification}
            is_ct = is_class_teacher(request)
            data['is_ct']=is_ct
            return render(request, 'teachers/update-mark.html', data)
        else:
            return redirect('teacher_login')

    def post(self,request,**kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            mark = get_object_or_404(Marks, pk=pk)
            obtaon = request.POST.get('obtain')
            total = request.POST.get('total')
            mark.obtain_marks = decimal.Decimal(obtaon)
            mark.total_marks = decimal.Decimal(total)
            mark.save()
            messages.success(request,f'{mark.student.first_name} marks Updated successfully.')
            return redirect('view_students_marks')
        else:
            return redirect('teacher_login')


class View_Fee(View):
    def get(self, request):
        if validate_user(request):
            is_ct = is_class_teacher(request)
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            data = {'notify': notify, 'notifications': notification}
            # ------end  notification
            if is_ct:
                data['is_ct'] = is_ct
                return render(request, 'teachers/Student-fee.html', data)
            else:
                messages.error(request, 'Yo are not a class teacher')
                return redirect('teacher_home')
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            teacher = get_object_or_404(Teacher, username= request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            role = get_object_or_404(Role, user=teacher.id)
            if role.role == "Class Teacher":
                month = request.POST.get('month')
                students = Students.objects.filter(class_name=role.class_name, section=role.section)
                students_fee = list()
                for std in students:
                    std_fee = [std]
                    try:
                        fee = Student_fees.objects.get(student=std.id,academic_year=academic, month=month, status=True)
                        std_fee.append(fee)
                    except:
                        pass
                    students_fee.append(std_fee)

                data = {'students_fee':students_fee, 'notify': notify, 'notifications': notification}
                is_ct = is_class_teacher(request)
                data['is_ct'] = is_ct
                return render(request, 'teachers/Student-fee.html', data)
            return redirect('teacher_home')
        else:
            return redirect('teacher_login')

class Send_Notification(View):
    def get(self, request):
        if validate_user(request):
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            classes = Class.objects.all()
            data = {'classes': classes, 'notify': notify, 'notifications': notification}
            return render(request, 'teachers/send-notification.html', data)
        return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            teacher = get_object_or_404(Teacher, username=request.session.get('user'))
            ## for notification
            noti_info = get_notifications(teacher)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            data = {'classes': classes, 'notify': notify, 'notifications': notification}
            notify_to = request.POST.get('notify_to')
            notification_msg = request.POST.get('notification')

            current_user = get_object_or_404(Teacher, username=request.session.get('user'))

            if notify_to == '1': # for perticular class and section
                cls = request.POST.get('class')
                section = request.POST.get('section')
                clss = get_object_or_404(Class, class_name= cls)
                students = Students.objects.filter(class_name=clss,section = section)
                for stdnt in students:
                    notification = Notification(student=stdnt, from_user=current_user, notification=notification_msg)
                    notification.save()
                messages.success(request, f'Notification Send to All {clss} {section} Students successfully')
            elif notify_to =='2': #for perticular user
                username = request.POST.get('username')
                if 'TE' in username:
                    messages.error(request, "You can not send notification to Teacher")
                elif "ST" in username:
                    user = get_object_or_404(Students, username=username)
                    notification = Notification(student=user, from_user=current_user, notification=notification_msg)
                    notification.save()
                    messages.success(request, f'Notification Send to {user.username} successfully')

            return render(request, 'lms_admin/send-notification.html', data )
        return redirect('teacher_login')


class View_notification(View):
    def get(self, request, **kwargs):
        if validate_user(request):
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
            return render(request, 'teachers/view-notifications.html', data)
        return redirect('login')










