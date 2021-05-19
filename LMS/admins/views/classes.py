from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admins.models.classes import Class, Class_subjects, Syllabus
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
            all_cls = Class.objects.all().order_by('class_name')
            subjects = Class_subjects.objects.all()
            data = {'all_cls': all_cls, 'subjects':subjects, 'requesturl':requesturl}
            return render(request, 'lms_admin/view-class.html', data)
        return redirect('teacher_login')

class Upload_syllabus(View):
    def get(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects}
            data['is_admin']= True
            return render(request, 'lms_admin/upload_syllabus.html',data)
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
                    syllabus = Syllabus.objects.get(class_name=cls,section=section,subject=subject)
                    syllabus.class_name=cls
                    syllabus.section=section
                    syllabus.subject=subject
                    syllabus.syllabus=file
                    syllabus.save()
                    messages.success(request, f'Syllabus Updated successfully')
                except:
                    syllabus = Syllabus(class_name = cls, section=section, subject=subject, syllabus=file)
                    syllabus.save()
                    messages.success(request, f'Syllabus added successfully')
            else:
                messages.error(request, 'Please Upload syllabus.')
            return redirect('admin_upload_syllabus')
        else:
            return redirect('teacher_login')

class View_syllabus(View):
    def get(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            subjects = Class_subjects.objects.all()
            data = {'classes': classes, 'subjects': subjects}
            data['is_admin'] = True
            return render(request, 'lms_admin/view-syllabus.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            cls = data.get('class')
            section = data.get('section')
            subject = data.get('subject')
            clss = get_object_or_404(Class, class_name=cls)
            all_syllabus = Syllabus.objects.filter(class_name=clss.id,section=section, subject=subject)
            data = {'all_syllabus':all_syllabus}
            data['is_admin'] = True
            return render(request, 'lms_admin/view-syllabus.html', data)
        else:
            return redirect('teacher_login')

class Delete_syllabus(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            syllabus = get_object_or_404(Syllabus, pk=pk)
            syllabus.delete()
            messages.success(request, "syllabus successfully delete")
            return redirect('admin_view_syllabus')
        else:
            return redirect('teacher_login')

