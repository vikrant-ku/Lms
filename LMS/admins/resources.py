from import_export import resources
from admins.models.professor import Teacher
from admins.models.students import Students

class TeacherResources(resources.ModelResource):
    class meta:
        model = Teacher

class StudentsResources(resources.ModelResource):
    class meta:
        model = Students