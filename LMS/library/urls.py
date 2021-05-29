from django.urls import path
from .views.books import Add_books, All_books, Edit_book, Delete_book, Issue_books, search_user, All_issue_book, Delete_issue_books
from .views.index import Index, Apply_leave,View_leave, All_notice, Change_password, Events, View_attandance, View_notification, Send_Notification,Profile, Update_profile
from admins.middleware.auth import auth_middleware


urlpatterns = [
    path('', auth_middleware(Index.as_view()) , name= "library_index"),
    path('profile/', auth_middleware(Profile.as_view()) , name= "library_profile"),
    path('profile/update-profile/', auth_middleware(Update_profile.as_view()) , name= "library_update_profile"),
    path('apply_leave/', auth_middleware(Apply_leave.as_view()) , name= "library_apply_leave"),
    path('view_leave/', auth_middleware(View_leave.as_view()) , name= "library_view_leave"),
    path('notice/', auth_middleware(All_notice.as_view()) , name= "library_notice"),
    path('change_password/', auth_middleware(Change_password.as_view()) , name= "library_change_password"),
    path('events/', auth_middleware(Events.as_view()), name='library_event'),
    path('send-notification/', auth_middleware(Send_Notification.as_view()), name='library_send_notification'),
    path('view-notification/', auth_middleware(View_notification.as_view()), name='library_view-notification'),

    #books
    path('add_books/', auth_middleware(Add_books.as_view()) , name= "add_books"),
    path('all_books/', auth_middleware(All_books.as_view()) , name= "all_books"),
    path('edit_book/<int:pk>/', auth_middleware(Edit_book.as_view()) , name= "edit_book"),
    path('delete_book/<int:pk>/', auth_middleware(Delete_book.as_view()) , name= "delete_book"),
    path('issue_book/', auth_middleware(Issue_books.as_view()) , name= "issue_book"),
    path('all_issue_books/', auth_middleware(All_issue_book.as_view()) , name= "all_issue_book"),
    path('delete_issue_book/<int:pk>/', auth_middleware(Delete_issue_books.as_view()) , name= "delete_issue_book"),
    path('view_attandance', auth_middleware(View_attandance.as_view()) , name= "library_view_attandance"),
    path('user/', auth_middleware(search_user), name='search_user'),

]