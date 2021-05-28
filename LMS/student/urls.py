from django.urls import path
from .views.login import Login, Logout, Change_password, Logout_all_devices
from .views.index import Index, Issue_books, View_assignment, View_attandance, Scheduled_class, View_marks, View_syllabus, View_documents
from .views.events import All_notice, Events, Apply_leave, All_leaves, View_notification, Send_feedback, view_feedback, Delete_feedback
from .views.fee import PayFee, View_Fee, handlerequest, Get_invoice
from admins.middleware.auth import auth_middleware


urlpatterns = [

    path('login/', Login.as_view() , name= "login"),
    path('change_password/', auth_middleware(Change_password.as_view()) , name= "change_password"),
    path('logout/', Logout.as_view() , name= "logout"),
    path('logout-from-all-devices/', Logout_all_devices.as_view() , name= "logout_all_devices"),

    #Index
    path('', auth_middleware(Index.as_view()) , name= "student_home"),
    path('view_documents/', auth_middleware(View_documents.as_view()) , name= "student_view_documents"),
    path('view_issue_books/',auth_middleware(Issue_books.as_view()), name='issue_books' ),
    path('assignment/',auth_middleware(View_assignment.as_view()), name='view_assignment' ),
    path('view_marks/',auth_middleware(View_marks.as_view()), name='view_marks' ),
    path('view_attandance/',auth_middleware(View_attandance.as_view()), name='view_attandance' ),
    path('classess/',auth_middleware(Scheduled_class.as_view()), name='classess' ),
    path('view_syllabus/',auth_middleware(View_syllabus.as_view()), name='view_syllabus' ),



    #Events
    path('events/', auth_middleware(Events.as_view()), name='student_events'),
    path('notice/', auth_middleware(All_notice.as_view()) , name= "student_notice"),
    path('apply_leave/', auth_middleware(Apply_leave.as_view()), name="apply_leave" ),
    path('view_leave/', auth_middleware(All_leaves.as_view()), name="view_leave" ),
    path('view-notification/', auth_middleware(View_notification.as_view()), name="student_view_notification" ),
    path('send-feedback/', auth_middleware(Send_feedback.as_view()), name="send-feedback" ),
    path('view_feedback/', auth_middleware(view_feedback.as_view()), name="view_feedback" ),
    path('delete_feedback/', auth_middleware(Delete_feedback.as_view()), name="delete_feedback" ),

    #Fee
    path('view-fee-info/', auth_middleware(View_Fee.as_view()), name="view_fee" ),
    path('get_invoice/', auth_middleware(Get_invoice.as_view()), name="get_invoice" ),
    path('pay_fee/', auth_middleware(PayFee.as_view()), name="pay_fee" ),
    path('pay_fee/handle_request/', handlerequest, name="handle_request" ),



]