from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views import View
from admins.models.professor import Teacher, Role
from admins.models.leave import Leave
from admins.models.classes import Class
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from .student import proper_pagination
from .login import validate_user
from admins.resources import TeacherResources
from tablib import Dataset

class Add_professors(View):
    def get(self, request):
        if validate_user(request):
            return render(request,'lms_admin/add-professor.html')
        return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
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
            pass1 = data.get('pass1')
            pass2 = data.get('pass2')

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

            if pass1==pass2 and gender is not None:

                user = Teacher(
                    first_name = firstname,
                    last_name = lastname,
                    gender = gender,
                    dob = dob,
                    address = address,
                    country = country,
                    state = state,
                    city = city,
                    zipcode = postcode,
                    phone = mobileno,
                    email = email,
                    designation = designation,
                    qualification = qualification,
                    basic_salary = salary,
                    contract_type = contract,
                    work_shift = shift,
                    # account info
                    bank_name = bank,
                    branch_name = branch,
                    account_number = account,
                    ifsc_code = ifsc,
                    aadhar_number =aadhar,
                    pancard_number = pan,
                    descripation =description,

                    )
                user.password = make_password(pass1)
                user.save()
                user.username = "TE00"+str(user.id)

                if image is not None:
                    user.image= image
                user.save()
                messages.success(request, f'{user.first_name} addedd Successfully')
            elif gender is None:
                messages.error(request, "Please select Gender")
            else:
                messages.error(request,"password do not match")
            return redirect('add_teacher')
        return redirect('teacher_login')


class Add_teacher_by_excel(View):
    def post(self, request):
        if validate_user(request):
            Teacher_resources = TeacherResources()
            data_set = Dataset()
            file = request.FILES['data']
            if not file.name.endswith('xlsx'):
                messages.error(request, "Please Upload .xlsx File")
            try:
                imported_data = data_set.load(file.read(),format='xlsx')
            except:
                messages.error(request, 'Something went wrong Please check your Excel file and try again..')

            for data in imported_data:

                data = tuple('' if x == None else x for x in data)

                teacher = Teacher(
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
                    data[16],
                    data[17],
                    data[18],
                    data[19],
                    data[20],
                    data[21],
                    data[22],
                    data[23],
                    data[24],
                    data[25],
                    data[26],
                )
                teacher.password = make_password(str(data[2]))
                teacher.save()
                teacher.username = "TE00"+str(teacher.id)
                teacher.save()
            return redirect('add_teacher')
        return redirect('teacher_login')

class All_professor(View):

    def get(self, request):
        if validate_user(request):
            q = request.GET.get('q')
            if q is not None:
                all_tchr = Teacher.objects.filter(
                                                    Q(username__icontains=q)|
                                                    Q(first_name__icontains = q)|
                                                    Q(last_name__icontains = q)|
                                                    Q(email__icontains = q)
                                                )
            else:
                all_tchr = Teacher.objects.all()
            # paginator
            paginator = Paginator(all_tchr, 10)
            last_page = paginator.page_range[-1]

            page = request.GET.get('page')

            try:
                allteacher = paginator.page(page)
            except PageNotAnInteger:
                allteacher = paginator.page(1)
            except EmptyPage:
                allteacher = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(allteacher, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = allteacher.start_index()

            data = {'all_teacher': allteacher, 'page_range': page_range, 'count': count, 'last_page':last_page}
            if q is not None:
                data['q']= q
                data['all_teacher']= all_tchr
            return render(request, 'lms_admin/all-professors.html', data)
        return redirect('teacher_login')


class View_professor(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            user = get_object_or_404(Teacher, pk=id)
            data = {'teacher':user}
            return render(request, 'lms_admin/view-teacher.html',data)
        return redirect('login')



class Edit_professor(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            user = Teacher.objects.get(pk=id)
            data = {'teacher':user}
            return render(request, 'lms_admin/edit-professor.html', data )
        return redirect('login')

    def post(self, request, **kwargs):
        path = request.META['PATH_INFO']
        data = request.POST
        try:
            image = request.FILES['image']
        except:
            image = None

        id = kwargs.get('pk')
        try:
            user = Teacher.objects.get(pk=id)
        except:
            user = None

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

        if user is not None:
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
            messages.success(request, 'Teacher Detail Successfully Updated')
        return HttpResponseRedirect(path)


class Delete_professor(View):
    def get(self, request,*arge, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            user = get_object_or_404(Teacher, pk=id)
            try:
                role = Role.objects.get(user=user.id)
                if role.role == "Admin":
                    messages.error(request, 'Being an Admin You can not delete Your self.')
            except:
                messages.success(request, f"{user.first_name} Successfully deleted")
                user.delete()
            return redirect("all_teachers")
        return redirect('login')

class Assign_role(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            user = Teacher.objects.get(pk=id)
            cls = Class.objects.all()
            data = {"classes":cls, 'teacher':user}
            return render(request, 'lms_admin/assign-role.html', data)
        return redirect('teacher_login')

    def post(self,request, **kwargs):
        if validate_user(request):
            # returnUrl = request.META['PATH_INFO']
            data = request.POST
            user = data.get('username')
            role = data.get('role')
            class_name = data.get('class')
            section = data.get('section')
            username = get_object_or_404(Teacher, username= user)
            try:
                teacher_role = Role.objects.get(user = username.id)
            except:
                teacher_role= None
            if teacher_role is None:
                role = Role(user=username, role=role)
                if class_name is not None:
                    cls = get_object_or_404(Class, class_name=class_name)
                    role.class_name=cls
                    role.section=section
                role.save()
                messages.success(request, f"{role} role Assign to the {username.first_name} . ")
            else:
                messages.error(request, f"User has already assigned a role. ")
            return redirect('view_role')
        return redirect('teacher_login')

class View_role(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            if id is not None:
                role = get_object_or_404(Role,pk=id)
                role.delete()
                if role.role.lower() =="admin":
                    return redirect('teacher_login')

                messages.success(request, f"{role.user.first_name}'s role deleted successfully")
                return redirect('view_role')
            all_role = Role.objects.all()
            data = {"all_role": all_role}
            return render(request, 'lms_admin/view-role.html', data)
        return redirect('teacher_login')

class teacher_leave(View):
    def get(self, request):
        if validate_user(request):
            leaves = Leave.objects.filter(is_teacher = True).order_by('-start_date')
            data = {'all_leaves':leaves}
            return render(request, 'lms_admin/view-leave.html', data)
        return redirect('teacher_login')

class teacher_leave_status(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            status = kwargs.get('status')
            leave = get_object_or_404(Leave, pk=pk)
            leave.status=status
            leave.save()
            return redirect('teachers_leave')
        return redirect('teacher_login')
