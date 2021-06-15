from django.db import models

class Class(models.Model):
    class_name = models.CharField(max_length=15)
    section_a = models.CharField(max_length=2, default='A')
    section_b = models.CharField(max_length=2, null=True, blank=True)
    section_c = models.CharField(max_length=2, null=True, blank=True)
    section_d = models.CharField(max_length=2, null=True, blank=True)
    section_e = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.class_name

class Class_subjects(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=2, default="A")
    subject_1 = models.CharField(max_length=50, null=True, blank=True)
    subject_2 = models.CharField(max_length=50, null=True, blank=True)
    subject_3 = models.CharField(max_length=50, null=True, blank=True)
    subject_4 = models.CharField(max_length=50, null=True, blank=True)
    subject_5 = models.CharField(max_length=50, null=True, blank=True)
    subject_6 = models.CharField(max_length=50, null=True, blank=True)
    subject_7 = models.CharField(max_length=50, null=True, blank=True)
    subject_8 = models.CharField(max_length=50, null=True, blank=True)
    subject_9 = models.CharField(max_length=50, null=True, blank=True)
    subject_10 = models.CharField(max_length=50, null=True, blank=True)
    subject_11 = models.CharField(max_length=50, null=True, blank=True)
    subject_12 = models.CharField(max_length=50, null=True, blank=True)
    subject_13 = models.CharField(max_length=50, null=True, blank=True)
    subject_14 = models.CharField(max_length=50, null=True, blank=True)
    subject_15 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.class_name.class_name

class Syllabus(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=2, default="A")
    subject = models.CharField(max_length=30, null=True, blank=True)
    syllabus = models.FileField(upload_to="syllabus", blank=True, null=True)

    def __str__(self):
        return self.class_name.class_name













