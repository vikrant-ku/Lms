from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from admins.models.classes import Class, Class_subjects
from django.contrib import messages
from .login import validate_user

class Add_subjects(View):
    def get(self, request):
        if validate_user(request):
            all_cls = Class.objects.all().order_by('class_name')
            data = {'all_cls': all_cls}
            return render(request, 'lms_admin/add-subjects.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            subjects = data.getlist('subject')

            cls_name = data.get('class')
            section = data.get('section')
            clss = get_object_or_404(Class, class_name = cls_name)
            length = len(subjects)
            try:
                subject = Class_subjects.objects.get(class_name=clss.id,section=section)

            except:
                subject = None
            if subject is None:

                if length<15:
                    for _ in range(15-length):
                        subjects.append(None)

                    cls = Class_subjects(
                        class_name = clss,
                        section= section,
                        subject_1=subjects[0],
                        subject_2=subjects[1],
                        subject_3=subjects[2],
                        subject_4=subjects[3],
                        subject_5=subjects[4],
                        subject_6=subjects[5],
                        subject_7=subjects[6],
                        subject_8=subjects[7],
                        subject_9=subjects[8],
                        subject_10=subjects[9],
                        subject_11=subjects[10],
                        subject_12=subjects[11],
                        subject_13=subjects[12],
                        subject_14=subjects[13],
                        subject_15=subjects[14],
                    )
                    cls.save()
                else:
                    messages.error(request,"You can not add subject more than 15 !")
            else:
                messages.error(request, f"Subjects is already added in class {cls_name} {section} .")
            return redirect('add_subjects')
        return redirect('login')

class All_subjects(View):
    def get(self, request):
        if validate_user(request):
            requesturl = request.META['PATH_INFO']
            all_cls = Class.objects.all().order_by('class_name')
            subjects = Class_subjects.objects.all()
            data = {'all_cls': all_cls, 'subjects': subjects, 'requesturl':requesturl}
            return render(request, 'lms_admin/view-subjects.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            subjects = data.getlist('subject')

            cls_name = data.get('class')
            section = data.get('section')
            clss = get_object_or_404(Class, class_name=cls_name)
            length = len(subjects)
            try:
                subject = Class_subjects.objects.get(class_name=clss.id, section=section)

            except:
                subject = None


            if length <= 15:
                for _ in range(15 - length):
                    subjects.append(None)

                print(f"subjects {subjects}")
                if subject is None:
                    cls = Class_subjects(
                        class_name=clss,
                        section=section,
                        subject_1=subjects[0],
                        subject_2=subjects[1],
                        subject_3=subjects[2],
                        subject_4=subjects[3],
                        subject_5=subjects[4],
                        subject_6=subjects[5],
                        subject_7=subjects[6],
                        subject_8=subjects[7],
                        subject_9=subjects[8],
                        subject_10=subjects[9],
                        subject_11=subjects[10],
                        subject_12=subjects[11],
                        subject_13=subjects[12],
                        subject_14=subjects[13],
                        subject_15=subjects[14],
                    )
                    cls.save()
                    messages.success(request, f"Subject successfully added in {cls_name}{section}")
                else:

                    subject.subject_1 = subjects[0]
                    subject.subject_2 = subjects[1]
                    subject.subject_3 = subjects[2]
                    subject.subject_4 = subjects[3]
                    subject.subject_5 = subjects[4]
                    subject.subject_6 = subjects[5]
                    subject.subject_7 = subjects[6]
                    subject.subject_8 = subjects[7]
                    subject.subject_9 = subjects[8]
                    subject.subject_10 = subjects[9]
                    subject.subject_11 = subjects[10]
                    subject.subject_12 = subjects[11]
                    subject.subject_13 = subjects[12]
                    subject.subject_14 = subjects[13]
                    subject.subject_15 = subjects[14]
                    subject.save()
                    messages.success(request, f"subject successfully updated on {cls_name}{section}")
            else:
                    messages.error(request, "You can not add subject more than 15 !")

            returnurl = data.get('return_url')
            return HttpResponseRedirect(returnurl)
        return redirect('login')







