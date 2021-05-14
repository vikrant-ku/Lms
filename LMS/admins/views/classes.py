from django.shortcuts import render, redirect
from django.views import View
from admins.models.classes import Class, Class_subjects
from django.contrib import messages
from .login import validate_user


class Add_class(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'lms_admin/add-class.html')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            class_name = data.get('class_name')
            section_a = data.get('section_a')
            section_b = data.get('section_b')
            section_c = data.get('section_c')
            section_d = data.get('section_d')
            section_e = data.get('section_e')
            section_f = data.get('section_f')

            try:
                Class.objects.get(class_name=class_name)
                messages.error(request,'This class is alreadty exist')
            except:

                cls = Class(
                    class_name = class_name,
                    section_a = section_a,
                )
                if section_b is not None:
                    cls.section_b = section_b
                if section_c is not None:
                    cls.section_c = section_c
                if section_d is not None:
                    cls.section_d = section_d
                if section_e is not None:
                    cls.section_e = section_e
                if section_f is not None:
                    cls.section_f = section_f

                cls.save()
            return redirect('add_class')
        else:
            return redirect('teacher_login')

class All_class(View):
    def get(self, request):
        if validate_user(request):
            requesturl= request.META['PATH_INFO']
            all_cls = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'all_cls': all_cls, 'subjects':subjects, 'requesturl':requesturl}
            return render(request, 'lms_admin/view-class.html', data)
        return redirect('teacher_login')
