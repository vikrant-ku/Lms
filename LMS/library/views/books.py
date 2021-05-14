from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from library.models import Books
from django.contrib import messages
from admins.models.professor import Teacher, Role
from admins.models.students import Students
from library.models import Issue_book
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from admins.views.student import proper_pagination


class Index(View):
    def get(self, request):
        if user_validate(request):
            return render(request, 'library/index.html')
        else:
            return redirect('teacher_login')



class Add_books(View):
    def get(self, request):
        if user_validate(request):
            return render(request, 'library/add-books.html')
        else:
            return redirect('teacher_login')

    def post(self, request):
        data = request.POST
        book_name = data.get("book_name")
        author_name = data.get("author_name")
        publish_year = data.get("publish_year")
        isbn_num = data.get("isbn_num")
        publication = data.get("publication")
        edition = data.get("edition")
        subject = data.get('subject')
        no_of_copies = data.get("no_of_copies")
        price = data.get("price")
        cupbord = data.get("cupbord")
        rack = data.get("rack")

        try:
            book = Books.objects.get(isbn_number = str(isbn_num))
            messages.error(request, 'Please Check book ISBN number')
        except:
            book = Books(
                book_name = book_name,
                auther_name = author_name,
                publishing_year = publish_year,
                isbn_number = isbn_num,
                publication = publication,
                edition = edition,
                subject = subject,
                number_of_copies = no_of_copies,
                price = price,
                cupbord_number = cupbord,
                rack_number = rack
            )
            book.save()
            messages.success(request, f"Book {book.book_name} is added successfully .")
        return redirect('add_books')

class All_books(View):
    def get(self, request):
        if user_validate(request):
            q = request.GET.get('q')
            if q is not None:
                allbooks = Books.objects.filter(
                    Q(book_name__icontains=q)|
                    Q(auther_name__icontains=q)|
                    Q(isbn_number__icontains=q)|
                    Q(subject__icontains=q)
                )
                if len(allbooks)<0:
                    books = Books.objects.all()
                else:
                    books=allbooks
            else:
                books = Books.objects.all()

                # paginator
            paginator = Paginator(books, 1)
            page = request.GET.get('page')

            try:
                all_books = paginator.page(page)
            except PageNotAnInteger:
                all_books = paginator.page(1)
            except EmptyPage:
                all_books = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(all_books, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = all_books.start_index()

            data = {'books': all_books, 'page_range': page_range, 'count': count}
            if q is None:
                data['q']=q
            else:
                data['q']=None
            return render(request, 'library/all-books.html', data)
        else:
            return redirect('teacher_login')


class Delete_book(View):
    def get(self, request, **kwargs):
        if user_validate(request):
            id = kwargs.get('pk')
            book = get_object_or_404(Books, pk=id)
            book.delete()
            messages.success(request, f"{book.book_name} successfully deleted")
            return redirect('all_books')
        else:
            return redirect('teacher_login')


class Edit_book(View):
    def get(self, request, **kwargs):
        if user_validate(request):
            id = kwargs.get('pk')
            book = get_object_or_404(Books, pk=id)
            data = {'book':book}
            return render(request, 'library/edit-book.html', data)
        else:
            return redirect('teacher_login')

    def post(self, request, **kwargs):
        return_url= request.META['PATH_INFO']
        id = kwargs.get('pk')
        data = request.POST

        book_name = data.get("book_name")
        author_name = data.get("author_name")
        publish_year = data.get("publish_year")
        isbn_num = data.get("isbn_num")
        publication = data.get("publication")
        edition = data.get("edition")
        no_of_copies = data.get("no_of_copies")
        price = data.get("price")
        cupbord = data.get("cupbord")
        rack = data.get("rack")


        book = Books.objects.get(isbn_number = str(isbn_num))
        if book.id == id:

            book.book_name = book_name
            book.auther_name = author_name
            book.publishing_year = publish_year
            book.isbn_number = isbn_num
            book.publication = publication
            book.edition = edition
            book.number_of_copies = no_of_copies
            book.price = price
            book.cupbord_number = cupbord
            book.rack_number = rack

            book.save()
            messages.success(request, F"Book {book.book_name} Updated successfully.")
        else:
            messages.error(request, f"{isbn_num} is Available please Confirm ISBN Number.")
        return HttpResponseRedirect(return_url)

class Issue_books(View):
    def get(self, request):
        if user_validate(request):
            return render(request, 'library/issue-book.html')
        else:
            return redirect('teacher_login')

    def post(self, request):
        data = request.POST
        return_date = data.get('return_date')
        username = data.get('username')

        book_name = data.get('book_name')
        book_dict = book_name.split(",")
        book = Books.objects.get(book_name=book_dict[0], edition=book_dict[1].strip())
        issue_book = Issue_book(
            book = book,
            return_date = return_date,
        )
        if "ST" in username:
            user = get_object_or_404(Students, username=username)
            issue_book.student = user
        else:
            user = get_object_or_404(Teacher, username=username)
            issue_book.teacher = user

        issue_book.save()
        messages.success(request, f"{book_dict[0]} is issued to {username}")
        return redirect("issue_book")

class All_issue_book(View):
    def get(self, request):
        if user_validate(request):
            msg= False
            q = request.GET.get('q')
            if q is not None:
                if "ST" in q:
                    try:
                        user = get_object_or_404(Students, username=q.upper())
                        all_issues = Issue_book.objects.filter(student = user.id)
                    except:
                        msg = f"No Data found related to {q} User."
                elif "TE" in q:
                    try:
                        user = get_object_or_404(Teacher, username= q.upper())
                        all_issues = Issue_book.objects.filter(student=user.id)
                    except:
                        msg = f"No data found related to {q} User."
                else:
                    all_issues = Issue_book.objects.all()
            else:

                all_issues = Issue_book.objects.all()

                if (len(all_issues) < 1):
                    msg = "There is No Record"
            paginator = Paginator(all_issues, 1)
            page = request.GET.get('page')

            try:
                all_issue_books = paginator.page(page)
            except PageNotAnInteger:
                all_issue_books = paginator.page(1)
            except EmptyPage:
                all_issue_books = paginator.page(paginator.num_pages)

            if page is None:
                start_index = 0
                end_index = 5
            else:
                (start_index, end_index) = proper_pagination(all_issue_books, index=3)

            page_range = list(paginator.page_range)[start_index:end_index]

            if page is None or page == 1:
                count = 1
            else:
                count = all_issue_books.start_index()

            data = {'all_issue_book':all_issue_books, 'page_range': page_range, 'count': count, 'msg': msg }
            return render(request, 'library/all-issue-book.html', data)
        else:
            return redirect('teacher_login')

class Delete_issue_books(View):
    def get(self,request, **kwargs):
        pk = kwargs.get('pk')
        issue_book = get_object_or_404(Issue_book, pk=pk)
        issue_book.delete()
        return redirect('all_issue_book')



def search_user(request):
    if user_validate(request):
        data = {}
        username = False
        user = request.GET.get('user')
        if 'ST' in user:
            try:
                username = Students.objects.get(username = user)
            except:
                messages.error(request,'Please check userID')
        elif 'TE' in user:
            try:
                username = Teacher.objects.get(username = user)
            except:
                messages.error(request, 'Please check userID')
        else:
            messages.error(request, 'Please check userID')

        if username:
            books = Books.objects.all()
            data = {'user' : username, 'books':books}

        return render(request, 'library/issue-book.html', data)
    else:
        return redirect('teacher_login')


def user_validate(request):
    username = request.session.get('user')
    if 'TE' not in username:
        return False
    user = get_object_or_404(Teacher, username= username)
    role = get_object_or_404(Role, user = user)
    if role.role == "Librarian":
        return True
    else:
        return False






