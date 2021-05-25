from django.urls import path
from .views.index import Index, Update_profile, Issue_books, Upload_assignment, View_assignment, Delete_assign, Schedule_class, View_schedule_class, Delete_schedule_class, Upload_syllabus, View_syllabus
from .views.event import Events, All_notice, Apply_leave, View_leave, Students_leave, student_leave_status
from .views.login import Login, Change_password
from .views.students import All_students,Student_info, Update_student_attandance, View_students_attandance, Attandance, View_attandance,Upload_marks, Save_student_marks, View_marks
from .views.students import update_student_mark, View_Fee
from admins.middleware.auth import auth_middleware




urlpatterns = [
    path('', auth_middleware(Index.as_view()) , name= "teacher_home"),

    # login
    path('login/', Login.as_view() , name= "teacher_login"),
    path('change_password/', auth_middleware(Change_password.as_view()) , name= "teacher_change_password"),

    #index
    path('update_profile', auth_middleware(Update_profile.as_view()), name="teacher_update_profile"),
    path('view_issue_books', auth_middleware(Issue_books.as_view()), name="teacher_issue_books"),
    path('upload_assignment/', auth_middleware(Upload_assignment.as_view()), name="upload_assignment"),
    path('assignments/', auth_middleware(View_assignment.as_view()), name="assignment"),
    path('upload_syllabus/', auth_middleware(Upload_syllabus.as_view()), name="teacher_upload_syllabus"),
    path('view_syllabus/', auth_middleware(View_syllabus.as_view()), name="teacher_view_syllabus"),
    path('delete_assignment/<int:pk>/', auth_middleware(Delete_assign.as_view()), name="delete_assignment"),
    path('schedule_class/', auth_middleware(Schedule_class.as_view()), name="schedule_class"),
    path('view-schedule-class/', auth_middleware(View_schedule_class.as_view()), name="view_schedule_class"),
    path('view-schedule-class/<int:pk>/', auth_middleware(Delete_schedule_class.as_view()), name="delete_schedule_class"),

    # students
    path('all_students/', auth_middleware(All_students.as_view()), name="teacher_all_students"),
    path('student_info/<str:username>/', auth_middleware(Student_info.as_view()), name="teacher_student_info"),
    path('mark_attandance/', auth_middleware(Attandance.as_view()), name="mark_attandnce"),
    path('view_students_attandance/', auth_middleware(View_students_attandance.as_view()), name="view_student_attandnce"),
    path('update_attandance/', auth_middleware(Update_student_attandance.as_view()), name="update_student_attandnce"),
    path('view_attandance/', auth_middleware(View_attandance.as_view()), name="view_teacher_attandnce"),
    path('upload-marks/', auth_middleware(Upload_marks.as_view()), name="upload_marks"),
    path('view-marks/', auth_middleware(View_marks.as_view()), name="view_students_marks"),
    path('update_mark/<int:pk>/<str:username>', auth_middleware(update_student_mark.as_view()), name="update_mark"),
    path('save-upload-marks/', auth_middleware(Save_student_marks.as_view()), name="save_upload_marks"),
    path('view_fee/', auth_middleware(View_Fee.as_view()), name="teacher_view_fee"),






    #event
    path('events/', auth_middleware(Events.as_view()) , name= "teacher_event"),
    path('notice/', auth_middleware(All_notice.as_view()) , name= "teacher_notice"),

    path('apply_leave/', auth_middleware(Apply_leave.as_view()), name='teacher_apply_leave'),
    path('view_leave/', auth_middleware(View_leave.as_view()), name='teacher_view_leave'),
    path('students_leave/', auth_middleware(Students_leave.as_view()), name='teacher_students_leave'),
    path('students_leave/<int:pk>/<str:status>/', auth_middleware(student_leave_status.as_view()), name='teacher_students_leave_status'),


    # path("students_leave", auth_middleware())


]