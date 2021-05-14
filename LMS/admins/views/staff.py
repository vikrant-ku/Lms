from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from admins.models.staff import Staff
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from .student import proper_pagination
from django.db.models import Q
from .login import validate_user

class Add_staff(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'lms_admin/add-staff.html')
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
            gender = data.get('gender')
            dob = data.get('dob')
            address = data.get('address')
            country = data.get('country')
            state = data.get('state')
            city = data.get('city')
            postcode = data.get('postcode')
            mobileno = data.get('mobileno')
            email = data.get('email')
            role = data.get('role')
            salary = data.get('salary')
            aadhar = data.get('aadhar')

            if gender is not None:
                staff = Staff(
                    first_name= firstname,
                    last_name = lastname,
                    gender=gender,
                    dob = dob,
                    address = address,
                    country = country,
                    state = state,
                    city = city,
                    zipcode = postcode,
                    phone = mobileno,
                    email = email,
                    role = role,
                    basic_salary = salary,
                    aadhar_number = aadhar
                   )
                if image is not None:
                    staff.image = image

                staff.save()
            else:
                messages.error(request, 'Please select the gender : ')

            return redirect('add_staff')
        return redirect('login')

class Edit_staff(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            staff = get_object_or_404(Staff, pk=pk)
            data = {'staff':staff, 'is_edit':True}
            return render(request, 'lms_admin/add-staff.html', data)
        return redirect('login')

    def post(self, request, **kwargs):
        if validate_user(request):
            path = request.META['PATH_INFO']

            data = request.POST

            try:
                image = request.FILES['image']
            except:
                image = None

            pk = kwargs.get('pk')
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
            role = data.get('role')
            salary = data.get('salary')
            aadhar = data.get('aadhar')

            staff = get_object_or_404(Staff, pk=pk)

            staff.first_name = firstname
            staff.last_name = lastname
            staff.gender = gender
            staff.dob = dob
            staff.address = address
            staff.country = country
            staff.state = state
            staff.city = city
            staff.zipcode = postcode
            staff.phone = mobileno
            staff.email = email
            staff.role = role
            staff.basic_salary = salary
            staff.aadhar_number = aadhar

            if image is not None:
                staff.image = image
            staff.save()
            messages.success(request, f"{staff.first_name}'s detail successfully updated")
            return HttpResponseRedirect(path)
        return redirect('login')

class All_staff(View):

    def get(self, request):
        if validate_user(request):
            q = request.GET.get('q')
            if q is not None:
                 all_staff = Staff.objects.filter(
                    Q(first_name__icontains=q)
                    | Q(last_name__icontains=q)
                    | Q(email__icontains=q)
                    | Q(role__icontains=q)
                    | Q(aadhar_number__icontains=q)
                    )
            else:
                all_staff = Staff.objects.all()

            # paginator
            paginator = Paginator(all_staff, 10)
            page = request.GET.get('page')

            try:
                allstaff = paginator.page(page)
            except PageNotAnInteger:
                allstaff = paginator.page(1)
            except EmptyPage:
                allstaff = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(allstaff, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = allstaff.start_index()

            data = {'all_staff': allstaff, 'page_range': page_range, 'count': count}
            return render(request, 'lms_admin/all-staff.html', data)
        return redirect('login')

class delete_staff(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            staff = get_object_or_404(Staff, pk=pk)
            staff.delete()
            return redirect('all_staff')
        return redirect('login')



