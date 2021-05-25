from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from admins.models.classes import Syllabus
from admins.models.students import Students,Documents
from admins.models.attandance import Student_Attandance
from library.models import Issue_book
from teacher.models import Assignment, OnlineClass, Marks
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from admins.views.student import proper_pagination
from django.db.models import Q
import datetime

class Index(View):
    def get(self, request):
        if validate_user(request):
            username = request.session.get('user')
            user = get_object_or_404(Students, username = username)

            data = {'user':user}
            return render(request, 'students/index.html', data)
        else:
            return redirect('login')

class View_documents(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            cls_name = user.class_name
            try:
                documents = Documents.objects.get(student = user)
            except:
                documents = Documents(student=user)
                documents.save()

            data ={'user':user,'documents': documents,'cls_name':str(cls_name)}

            return render(request, 'students/view-documents.html', data)
        else:
            return redirect('login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            documents = Documents.objects.get(student=user)
            msg= list()
            try:
                image = request.FILES['image']
                if file_size(image):
                    user.image = image
                    user.save()
                else:
                    msg.append('Image')
            except:
                pass
            try:
                birth_certificate = request.FILES['birth_certificate']
                if file_size(birth_certificate):
                   documents.birth_certificate = birth_certificate
                else:
                    msg.append('Birth Certificate')
            except:
               pass

            try:
                aadhar = request.FILES['aadhar']
                if file_size(aadhar):
                   documents.aadhar = aadhar
                else:
                    msg.append('Aadhar')
            except:
               pass

            try:
                parent_aadhar = request.FILES['parent_aadhar']
                if file_size(parent_aadhar):
                   documents.parent_aadhar = parent_aadhar
                else:
                    msg.append('Parents Aadhar')
            except:
                pass

            try:
                tc = request.FILES['tc']
                if file_size(tc):
                   documents.tc = tc
                else:
                    msg.append('Transfer Certificate')
            except:
                pass

            try:
                progress_report = request.FILES['progress_report']
                if file_size(progress_report):
                   documents.progress_report = progress_report
                else:
                    msg.append('Progress Report')
            except:
                pass

            try:
                affidavit = request.FILES['affidavit']
                if file_size(affidavit):
                   documents.affidavit = affidavit
                else:
                    msg.append('Affidavit')
            except:
                pass

            try:
                under_taking = request.FILES['under_taking']
                if file_size(under_taking):
                   documents.under_taking = under_taking
                else:
                    msg.append('Under Taking Form')
            except:
                pass
            documents.save()
            if len(msg)>0:
                messg = (', ').join(msg)
                messages.error(request, f"{messg} size must be less than 2MB. ")

            return redirect('student_view_documents')
        else:
            return redirect('login')
class Issue_books(View):
    def get(self, request):
        if validate_user(request):
            username = request.session.get('user')
            user = get_object_or_404(Students, username=username)
            issue_books = Issue_book.objects.filter(student= user.id)
            data = {'all_issue_book': issue_books}
            return render(request, 'students/all-issue-book.html', data)
        else:
            return redirect('login')

class View_assignment(View):
    def get(self, request):
        if validate_user(request):
            username = request.session.get('user')
            user = get_object_or_404(Students, username=username)

            q = request.GET.get('q')
            print(q,'Q')
            if q is not None:
                print("q is None")
                assig = Assignment.objects.filter(
                    Q(class_name__class_name__icontains=q)
                    | Q(section__icontains=q)
                    | Q(subject__icontains=q)
                                           )
                if len(assig) > 0:
                    all_assig = assig
                else:
                    all_assig = Assignment.objects.filter(class_name= user.class_name,section=user.section )
            else:
                all_assig = Assignment.objects.filter(class_name=user.class_name, section=user.section)
                print(all_assig)

            # paginator
            paginator = Paginator(all_assig, 1)
            page = request.GET.get('page')

            try:
                all_assign = paginator.page(page)
            except PageNotAnInteger:
                all_assign = paginator.page(1)
            except EmptyPage:
                all_assign = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 7
            else:
                (start_index, end_index) = proper_pagination(all_assign, index=1)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = all_assign.start_index()

            data = {'all_assign': all_assign, 'page_range': page_range, 'count': count}

            return render(request,'students/assignment.html', data)
        return redirect('login')

class View_attandance(View):
    def get(self, request):
        if validate_user(request):
            today = datetime.datetime.today()
            username = request.session.get('user')
            user = get_object_or_404(Students, username=username)

            month = request.GET.get('month')
            year = request.GET.get('year')
            mnth = [str(i) for i in range(1,13)]
            if month in mnth:
                attandance = Student_Attandance.objects.filter(student =user.id, datetime__year=year, datetime__month=int(month))
            else:
                attandance = None

            data = {'attandance':attandance, 'year':today.year}

            return render(request, 'students/view-attandance.html', data)
        else:
            return redirect('login')

class Scheduled_class(View):
    def get(self, request):
        if validate_user(request):
            username = request.session.get('user')
            user = get_object_or_404(Students, username=username)

            sch_cls = OnlineClass.objects.filter(class_name = user.class_name , section=user.section ).order_by('date')

            q = request.GET.get('q')
            if q is not None:
                schcls = OnlineClass.objects.filter(
                     Q(subject__icontains=q)
                                           )
            #     if len(assig) > 0:
            #         all_assig = assig
            #     else:
            #         all_assig = Assigmnent.objects.filter(class_name= user.class_name , section=user.class_name)
            #
            # else:
            #     all_assig = Assigmnent.objects.filter(class_name= user.class_name , section=user.class_name)


            # paginator
            # paginator = Paginator(all_assig, 1)
            # page = request.GET.get('page')
            #
            # try:
            #     all_assign = paginator.page(page)
            # except PageNotAnInteger:
            #     all_assign = paginator.page(1)
            # except EmptyPage:
            #     all_assign = paginator.page(paginator.num_pages)
            #
            # if page is None:
            #     start_index = 0
            #     end_index = 7
            # else:
            #     (start_index, end_index) = proper_pagination(all_assig, index=1)
            #
            # page_range = list(paginator.page_range)[start_index:end_index]
            #
            # if page is None or page == 1:
            #     count = 1
            # else:
            #     count = all_assig.start_index()

            data = {'all_sch_cls': sch_cls}


            return render(request,'students/view-class.html', data)
        return redirect('login')

class View_marks(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'students/view-marks.html')
        else:
            return redirect('login')

    def post(self, request):
        if validate_user(request):
            type = request.POST.get('type')
            user = get_object_or_404(Students, username=request.session.get('user'))
            marks = Marks.objects.filter(student=user.id,class_name=user.class_name, section=user.section, exam_type=type)
            data = {'marks':marks}
            return render(request, 'students/view-marks.html', data)
        else:
            return redirect('login')

class View_syllabus(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            all_syllabus = Syllabus.objects.filter(class_name =user.class_name, section=user.section )
            data = {'all_syllabus':all_syllabus}
            return render(request, 'students/view-syllabus.html', data)
        else:
            return redirect('login')

def validate_user(request):
    username = request.session.get('user')
    if username is not None and 'ST' in username:
        student = get_object_or_404(Students, username=username)
        if student.token == request.session.get('token'):
            return True
    return False

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        return False
    return True




