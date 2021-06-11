from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views import View
from admins.models.fees import Fees, Student_fees, Academic_Year, Fee_discount
from admins.models.students import Students, Documents
from admins.models.classes import Class
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from .login import validate_user
from admins.resources import StudentsResources
from tablib import Dataset

class Add_students(View):
    def get(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            data = {'classes': classes}
            return render(request, 'lms_admin/add-student.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            try:
                image = request.FILES['image']
            except:
                image = None
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            fathername = data.get('fathername')
            mothername = data.get('mothername')
            admission_no = str(data.get('admno'))
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
            pass1= data.get('pass1')
            pass2= data.get('pass2')
            is_rte = data.get('is_rte')
            if pass1==pass2:
                try:
                    class_name = Class.objects.get(class_name=class_name)
                except:
                    messages.error(request, 'Class name is not valid or exist')
                    return redirect('add_students')
                try:
                    user = Students.objects.get(admission_no = admission_no)
                    messages.error(request, 'This Admission number is Available Please Confirm admission number !!')
                    return redirect('add_students')
                except:
                    pass

                user = Students(
                    password = pass1,
                    admission_no = admission_no,
                    first_name = firstname,
                    last_name = lastname,
                    father_name = fathername,
                    mother_name = mothername,
                    dob = dob,
                    address = address,
                    country = country,
                    state = state,
                    city = city,
                    zipcode = postcode,
                    phone = phone,
                    gender = gender,
                    class_name = class_name,
                    section = section
                        )
                user.password = make_password(user.password)
                user.save()
                user.username = "ST00"+str(user.id)

                if is_rte is not None:
                    user.is_rte = True

                if image is not None:
                    user.image = image
                user.save()
                messages.success(request, f'{user.username} is registered')
            else:
                messages.error(request, 'password do not registered')
            return redirect('add_students')
        return redirect('login')

class Add_Student_by_Excel(View):
    def post(self, request):
        if validate_user(request):
            Student_resources = StudentsResources()
            data_set = Dataset()
            file = request.FILES['data']

            if not file.name.endswith('xlsx'):
                messages.error(request, "Please Upload .xlsx File")

            imported_data = data_set.load(file.read(),format='xlsx')

            admission_no = [_[15] for _ in imported_data]

            if len(set(admission_no))==len(admission_no) and None not in admission_no:
                for data in imported_data:
                    data = tuple('' if x == None else x for x in data)
                    student = Students(
                        None,
                        None,
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                        data[8],
                        data[9],
                        data[10],
                        data[11],
                        data[12],
                        data[13],
                        data[14],
                        data[15],
                        None,
                        data[17],
                        data[18],
                        False,
                        data[20],
                        data[21],
                        False

                    )
                    student.password = make_password(str(data[2]))
                    student.save()
                    student.username = "ST00"+str(student.id)
                    if data[16] !="":
                        try:
                            cls = Class.objects.get(class_name=str(data[16]))
                            student.class_name = cls
                        except:
                            pass
                    if data[22]!="":
                        student.is_rte=True
                    student.save()
            else:
                messages.error(request, "Admission No Must be Unique. Please Check your Excel File and Try Again..")
            return redirect('add_students')
        return redirect('teacher_login')

class All_students(View):

    def get(self, request):
        if validate_user(request):
            q = request.GET.get('q')
            cls = request.GET.get('class')
            section = request.GET.get('section')
            is_rte = request.GET.get('is_rte')

            if q is not None:
                all_q = q.split(" ")
                all_stdnt = Students.objects.filter(Q(username__icontains=all_q[0])|
                                                   Q(first_name__icontains = all_q[0])|
                                                   Q(last_name__icontains = all_q[0])|
                                                   Q(phone__icontains = all_q[0])|
                                                   Q(class_name__class_name__icontains = all_q[0])
                                                   )
                if len(all_q)>1:
                    for i in range(1,len(all_q)):
                        all_studnt = Students.objects.filter(Q(username__icontains=all_q[0]) |
                                                            Q(first_name__icontains=all_q[0]) |
                                                            Q(last_name__icontains=all_q[0]) |
                                                            Q(phone__icontains=all_q[0]) |
                                                            Q(class_name__class_name__icontains=all_q[0])
                                                            )
                        all_stdnt = all_stdnt.union(all_studnt)
            else:
                if cls is not None and is_rte is not None:
                    try:
                        clss = Class.objects.get(class_name = cls)
                        if section is None:
                            all_stdnt = Students.objects.filter(class_name=clss,is_rte=True)
                        else:
                            all_stdnt = Students.objects.filter(class_name=clss, section=section,is_rte=True)
                    except:
                        all_stdnt = Students.objects.filter(is_rte=True)
                elif cls is not None:
                    try:
                        clss = Class.objects.get(class_name = cls)
                        if section is None:
                            all_stdnt = Students.objects.filter(class_name=clss)
                        else:
                            all_stdnt = Students.objects.filter(class_name=clss, section=section)
                    except:
                        all_stdnt = Students.objects.all()

                else:
                    if is_rte is not None:
                        all_stdnt = Students.objects.filter(is_rte=True)
                    else:
                        all_stdnt = Students.objects.all()

            #paginator
            paginator = Paginator(all_stdnt, 30)
            last_page = paginator.page_range[-1]

            page = request.GET.get('page')

            try:
                allstud = paginator.page(page)
            except PageNotAnInteger:
                allstud = paginator.page(1)
            except EmptyPage:
                allstud = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index= 5
            else:
                (start_index, end_index)=proper_pagination(allstud, index=3)
            page_range = list(paginator.page_range)[start_index:end_index]
            # Page count for serial number in template
            if page is None or page==1:
                count = 1
            else:
                count = allstud.start_index()

            classes = Class.objects.all()
            data = {'classes': classes,'all_stud': allstud, 'page_range': page_range,
                    'count': count, "last_page":last_page, 'cls': cls, 'section': section, 'is_rte':is_rte
                    }
            if q is not None:
                data['q'] = q
                data['all_stud'] = all_stdnt
            return render(request, 'lms_admin/all-students.html', data)
        return redirect('login')

class View_Student(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            user = get_object_or_404(Students, pk=id)
            class_name = str(user.class_name)
            data = {'student': user, 'class_name':class_name }
            try:
                documents = Documents.objects.get(student=user)

                data['documents']:documents
            except:
                pass
            return render(request,'lms_admin/view-student.html',data)
        return redirect('login')

class View_documents(View):
    def get(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            data = {'classes': classes}
            class_name = request.GET.get('class')
            section = request.GET.get('section')
            if class_name is not None:
                data['class_name']=str(class_name)
                data['section']=section
                cls = get_object_or_404(Class, class_name=class_name)
                students = Students.objects.filter(class_name=cls, section=section)
                documents = dict()
                for std in students:
                    try:
                        document = Documents.objects.get(student=std)
                    except:
                        document = None
                    documents[std] = document
                data['documents'] = documents
            return render(request,'lms_admin/view-document.html',data)
        return redirect('login')

class Edit_student(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')

            user = Students.objects.get(pk=id)
            classes = Class.objects.all()
            data = {'student':user , 'classes': classes}
            return render(request, 'lms_admin/edit-student.html', data)
        return redirect('login')

    def post(self, request, **kwargs):
        if validate_user(request):
            path = request.META['PATH_INFO']
            id = kwargs.get('pk')
            try:
                image = request.FILES['image']
            except:
                image = None
            user = Students.objects.get(pk=id)

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

class Delete_student(View):
    def get(self, request,*arge, **kwargs):
        if validate_user(request):

            pk = kwargs.get('pk')
            stud = get_object_or_404(Students, pk=pk)
            stud.delete()
            return redirect("admin_all_students")
        return redirect('login')

class Add_fees(View):
    def get(self,request):
        if validate_user(request):
            classes = Class.objects.all()
            data = {'classes': classes}
            return render(request, 'lms_admin/add-fees.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            cls = data.get('class')
            fee = data.get('fee')
            clss = get_object_or_404(Class, pk=int(cls))
            try:
                fees = Fees.objects.get(class_name = int(cls))
                fees.class_name = clss
                fees.fees = fee
                fees.save()
                messages.success(request,f"{clss} fee has been changed. ")
            except:
                fees = Fees(class_name = clss, fees=fee)
                fees.save()
                messages.success(request, f"{clss} fee added successfully. ")
            return redirect('add_fees')
        return redirect('login')

class View_fees(View):
    def get(self, request):
        if validate_user(request):
            fees = Fees.objects.all()
            data = {'fees': fees}
            return render(request, 'lms_admin/view-fees.html', data)
        return redirect('login')


class Students_fee(View):
    def get(self, request):
        if validate_user(request):
            classes = Class.objects.all()
            month = request.GET.get('month')
            cls = request.GET.get('class')
            section = request.GET.get('section')
            if month is None:
                data = {'classes': classes}
                return render(request, 'lms_admin/view-fee-info.html', data)
            else:
                clss = get_object_or_404(Class, class_name=cls)
                academic_year = Academic_Year.objects.all().last()
                students = Students.objects.filter(class_name=clss, section=section)
                stud_fee = list()
                for stud in students:
                    std_fee = [stud]
                    try:
                        fee = Student_fees.objects.get(student=stud.id, academic_year=academic_year, month=month,
                                                       status=True)
                        std_fee.append(fee)
                    except:
                        pass
                    stud_fee.append(std_fee)
                data = {'students_fee': stud_fee, 'month': month, 'classes': classes}
                return render(request, 'lms_admin/view-fee-info.html', data)
        return redirect('login')

class Fee_discounts(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'lms_admin/fee-discount.html')
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            username = data.get('username')
            discount = data.get('discount')
            student = get_object_or_404(Students, username = username)
            try:
                user_discount = Fee_discount.objects.get(student=student.id)
                user_discount.discount= discount
                messages.success(request,'Discount Updated Successfully')
            except:
                user_discount = Fee_discount(student=student, discount=discount)
            user_discount.save()
            return redirect('admin-view-fee-discount')
        return redirect('login')

class View_fee_discounts(View):
    def get(self, request):
        if validate_user(request):
            cls = request.GET.get('class')
            section = request.GET.get('section')
            is_rte = request.GET.get('is_rte')

            q = request.GET.get('q')
            if q is not None:
                all_q = q.split(" ")
                all_discounts = Fee_discount.objects.filter(Q(student__username__icontains=all_q[0]) |
                                                    Q(student__first_name__icontains=all_q[0]) |
                                                    Q(student__last_name__icontains=all_q[0]) |
                                                    Q(student__father_name__icontains=all_q[0])
                                                    )
                if len(all_q) > 1:
                    for i in range(1, len(all_q)):
                        discounts = Fee_discount.objects.filter(Q(student__username__icontains=all_q[0]) |
                                                    Q(student__first_name__icontains=all_q[0]) |
                                                    Q(student__last_name__icontains=all_q[0]) |
                                                    Q(student__father_name__icontains=all_q[0])
                                                    )
                        all_discounts = all_discounts.union(discounts)
            else:
                if cls is not None and is_rte is not None:
                    try:
                        clss = Class.objects.get(class_name = cls)
                        if section is None:
                            all_discounts = Fee_discount.objects.filter(student__class_name=clss,student__is_rte=True)
                        else:
                            all_discounts = Fee_discount.objects.filter(student__class_name=clss, student__section=section,student__is_rte=True)
                    except:
                        all_discounts = Fee_discount.objects.filter(student__is_rte=True)
                elif cls is not None:

                    try:
                        clss = Class.objects.get(class_name = cls)

                        if section is None:
                            all_discounts = Fee_discount.objects.filter(student__class_name=clss)
                        else:
                            all_discounts = Fee_discount.objects.filter(student__class_name=clss, student__section=section)
                    except:
                        all_discounts = Fee_discount.objects.all()

                else:
                    if is_rte is not None:
                        all_discounts = Fee_discount.objects.filter(student__is_rte=True)
                    else:
                        all_discounts = Fee_discount.objects.all()

            classes = Class.objects.all()

            data = {'classes': classes,'all_discounts': all_discounts}
            return render(request, 'lms_admin/view-fee-discount.html', data)
        return redirect('login')

class Edit_fee_discount(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            username = kwargs.get('username')
            student = get_object_or_404(Students, username=username)
            try:
                discount = Fee_discount.objects.get(student=student.id)
                data = {'discount':discount}
            except:
                data = {'student': student}
            return render(request, 'lms_admin/fee-discount.html', data)
        return redirect('login')


class Delete_discount(View):
    def get(self, request, **kwargs):
        print("cllled")
        if validate_user(request):
            discount= get_object_or_404(Fee_discount, pk=kwargs.get('pk'))
            discount.delete()
            return redirect("admin-view-fee-discount")
        return redirect('login')







def proper_pagination(prods, index):
    start_index = 0
    end_index = 5
    if prods.number > index:
        start_index = prods.number - index
        end_index = start_index + end_index
    return (start_index,end_index)