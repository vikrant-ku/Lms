from .views.index import Index
from .views.student import Add_students, All_students , Delete_student, Edit_student, Add_fees, View_fees,Students_fee, Add_Student_by_Excel
from .views.professor import Add_professors , All_professor , Edit_professor, Delete_professor, Assign_role,View_role, teacher_leave, teacher_leave_status
from .views.professor import Add_teacher_by_excel
from .views.staff import Add_staff, All_staff, delete_staff, Edit_staff
from .views.login import Reset_password
from .views.events import Add_events, All_events,Delete_event, Add_notice, All_notice, Delete_notice, Add_academic_year,All_academic_year
from .views.classes import Add_class, All_class, View_syllabus, Upload_syllabus, Delete_syllabus
from .views.subject import Add_subjects, All_subjects
from .views.attandance import Attandance, Update_attandance, View_teacher_attand
from django.urls import path
from .middleware.auth import auth_middleware

urlpatterns = [

    path('', auth_middleware(Index.as_view()), name="admin_home"),
    path('reset_password/', auth_middleware(Reset_password.as_view()), name="reset_password"),

    #students
    path('add_student/', auth_middleware(Add_students.as_view()), name="add_students"),
    path('add_student_by_excel/', auth_middleware(Add_Student_by_Excel.as_view()), name="add_student_excel"),
    path('all_students/', auth_middleware(All_students.as_view()), name='admin_all_students'),
    path('delete_student/<int:pk>/', auth_middleware(Delete_student.as_view()), name='all_students'),
    path('edit_student/<int:pk>/', auth_middleware(Edit_student.as_view()), name="edit_student"),
    path('add_fees/', auth_middleware(Add_fees.as_view()), name="add_fees"),
    path('view_fees/', auth_middleware(View_fees.as_view()), name="admin_view_fees"),
    path('view_students_fees/', auth_middleware(Students_fee.as_view()), name="admin_students_fee"),

    #Teachers
    path('add_teachers/', auth_middleware(Add_professors.as_view()), name="add_teacher"),
    path('add_teacher_by_excel/', auth_middleware(Add_teacher_by_excel.as_view()), name="add_teacher_excel"),
    path('all_teachers/', auth_middleware(All_professor.as_view()), name='all_teachers'),
    path('delete_teacher/<int:pk>/', auth_middleware(Delete_professor.as_view()), name='delete_teachers'),
    path('edit_teacher/<int:pk>/', auth_middleware(Edit_professor.as_view()), name="edit_teacher"),
    path('assign_role/<int:pk>/', auth_middleware(Assign_role.as_view()), name='assign_role'),
    path('view_role/', auth_middleware(View_role.as_view()), name='view_role'),
    path('view_role/<int:pk>/', auth_middleware(View_role.as_view()), name='delete_role'),
    path('leaves/', auth_middleware(teacher_leave.as_view()), name='teachers_leave'),
    path('leave_status/<int:pk>/<str:status>/', auth_middleware(teacher_leave_status.as_view()), name='teacher_leave_status'),

    #staff
    path('add_staff/', auth_middleware(Add_staff.as_view()), name='add_staff'),
    path('all_staff/', auth_middleware(All_staff.as_view()), name='all_staff'),
    path('delete_staff/<int:pk>/', auth_middleware(delete_staff.as_view()), name='delete_staff'),
    path('edit_staff/<int:pk>/<str:first_name>/', auth_middleware(Edit_staff.as_view()), name='edit_staff'),

    #events
    path('add_academic_year/', auth_middleware(Add_academic_year.as_view()), name='add_academic_year'),
    path('view_academic_year/', auth_middleware(All_academic_year.as_view()), name='view_academic_year'),
    path('events/', auth_middleware(All_events.as_view()), name='admin_events'),
    path('add_event/', auth_middleware(Add_events.as_view()), name='add_event'),
    path('delete_event/<int:pk>/', auth_middleware(Delete_event.as_view()), name='delete_event'),
    path('add_notice/', auth_middleware(Add_notice.as_view()), name='add_notice'),
    path('notice/', auth_middleware(All_notice.as_view()), name='admin_notice'),
    path('delete_notice/<int:pk>/', auth_middleware(Delete_notice.as_view()), name='delete_notice'),

    #class
    path('add_class/', auth_middleware(Add_class.as_view()), name='add_class'),
    path('all_class/', auth_middleware(All_class.as_view()), name='all_class'),
    path('upload_syllabus/', auth_middleware(Upload_syllabus.as_view()), name='admin_upload_syllabus'),
    path('view_syllabus/', auth_middleware(View_syllabus.as_view()), name='admin_view_syllabus'),
    path('delete_syllabus/<int:pk>', auth_middleware(Delete_syllabus.as_view()), name='admin_delete_syllabus'),
    #subjects
    path('add_subjects/', auth_middleware(Add_subjects.as_view()), name='add_subjects'),
    path('all_subjects/', auth_middleware(All_subjects.as_view()), name='all_subjects'),

    #Attandance
    path('mark_attandance/', auth_middleware(Attandance.as_view()), name='admin_mark_attandance'),
    path('update_attandance/', auth_middleware(Update_attandance.as_view()), name='admin_update_attandance'),
    path('teacher_attandance/', auth_middleware(View_teacher_attand.as_view()), name='admin_teacher_attandance'),

]





