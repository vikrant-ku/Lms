from django.shortcuts import render , redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib import messages
from admins.models.notice import Notices, Event
from admins.models.fees import Academic_Year
from .login import validate_user
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from .student import proper_pagination
import datetime


class Add_events(View):
    def get(self, request):
        if validate_user(request):
            return render(request, 'lms_admin/add-event.html')
        return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            data = request.POST
            title = data.get('title')
            description = data.get('description')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()


            if end_date != "":
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

                if end_date<start_date:
                    messages.error(request, 'Start date is not smaller than end date')
                    return render(request, 'lms_admin/add-event.html')
            else:
                end_date= None

            event = Event(title=title, description=description, start_date=start_date, end_date=end_date)
            event.save()
            messages.success(request, 'Event Save Successfully')
            return render(request, 'lms_admin/add-event.html')
        else:
            return redirect('teacher_login')


class All_events(View):
    def get(self, request):
        if validate_user(request):
            q = request.GET.get('q')
            if q is not None:
                all_events = Event.objects.filter(Q(title__icontains=q)|
                                                   Q(description__icontains = q)|
                                                   Q(start_date__icontains = q)|
                                                   Q(start_date__icontains = q)

                                                   )

            else:
                all_events = Event.objects.all().order_by('start_date')
            # paginator
            paginator = Paginator(all_events, 10)
            page = request.GET.get('page')

            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(events, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = events.start_index()

            data = {'events':events, 'page_range': page_range, 'count': count}
            if q is not None:
                data['q'] = q
                data['events'] = all_events
            return render(request, 'lms_admin/view-events.html', data)
        return redirect('teacher_login')

class Delete_event(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            pk = kwargs.get('pk')
            event = get_object_or_404(Event, pk=pk)
            event.delete()
            return redirect('admin_events')
        return redirect('teacher_login')

class Add_notice(View):
    def get(self,request):
        if validate_user(request):
            return render(request, 'lms_admin/add-notice.html')
        return redirect('teacher_login')


    def post(self, request):
        if validate_user(request):

            data = request.POST
            recipient = data.get('recipient')
            type = data.get('type')
            date = data.get('date')
            notice = data.get('notice')

            notic = Notices(
                recipient = recipient,
                type = type,
                date = date,
                notice = notice
                )
            notic.save()
            return redirect('add_notice')
        return redirect('teacher_login')

class All_notice(View):
    def get(self, request):
        if validate_user(request):
            q = request.GET.get('q')
            if q is not None:
                notices = Notices.objects.filter(
                                        Q(recipient__icontains=q)
                                        | Q(type__icontains=q)
                                        | Q(date__icontains=q)
                                        | Q(notice__icontains=q)
                                         ).order_by('-date')

                if len(notices)>0:
                    all_notice = notices
                else:
                    all_notice = Notices.objects.all().order_by('-date')
            else:
                all_notice = Notices.objects.all().order_by('-date')

            data = {'all_notice':all_notice, "is_admin":True}
            return render(request,'lms_admin/notice.html', data)
        return redirect('teacher_login')

class Delete_notice(View):
    def get(self, request, **kwargs):
        if validate_user(request):
            id = kwargs.get('pk')
            notic = get_object_or_404(Notices, pk=id)
            notic.delete()
            return redirect('admin_notice')
        return redirect('teacher_login')


class Add_academic_year(View):
    def get(self, request):
        if validate_user(request):
            today = datetime.date.today()
            return render(request, 'lms_admin/add_academic_year.html', {'year':int(today.year)})
        return redirect('teacher_login')

    def post(self, request):
        if validate_user(request):
            today = datetime.date.today()
            academic=request.POST.get('academic')
            years = academic.split('-')
            if int(today.year)>int(years[0]):
                messages.error(request,f"Year must be grater or equal than {int(today.year)} year. {academic}" )
                return redirect('add_academic_year')
            elif(int(years[1])-int(years[0]))!= 1:
                messages.error(request, f"Invalid Academic Year. {academic}")
                return redirect('add_academic_year')
            else:
                acdmic = Academic_Year(academic_year=academic)
                acdmic.save()
                messages.success(request, f'Academic Year {academic} added successfully')
                return redirect("view_academic_year")

        return redirect('teacher_login')

class All_academic_year(View):
    def get(self, request):
        if validate_user(request):
            all_academics = Academic_Year.objects.all().order_by('academic_year')
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]

            return render(request, 'lms_admin/view_academic_year.html',{'all_academics':all_academics})
        return redirect('teacher_login')




