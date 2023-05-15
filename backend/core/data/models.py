from django.db import models
from django.core.validators import RegexValidator


class StaffDetail(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('teaching', 'Teaching'),
        ('non-teaching', 'Non-Teaching'),
    ]

    email = models.EmailField(primary_key=True, max_length=254, unique=True, verbose_name='Email', help_text='e.g. firstname.lastname@ljku.edu.in')
    first_name = models.CharField(max_length=20, verbose_name='First Name')
    middle_name = models.CharField(max_length=20, null=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=20, verbose_name='Last Name')
    short_name = models.CharField(max_length=5, verbose_name='Short Name', help_text='e.g. DKT')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, verbose_name='Gender')
    birth_date = models.DateField(verbose_name='Birth Date', help_text='dd-mm-yyyy')
    mobile_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?\d{6,15}$',
            message='Mobile number must be in international format with no spaces or special characters.',
        ),
    ], verbose_name='Mobile Number', help_text='e.g. +1234567890')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Category')
    active = models.BooleanField(default=True, verbose_name='Active', help_text='Is the staff actively doing his/her job?')

    class Meta:
        verbose_name_plural = 'Staff Details'
        verbose_name = 'Staff Detail'

    def __str__(self):
        return self.email
    


class Weightage(models.Model):

    TEACHING_TYPE_CHOICES = [
        ('T','Theory'),
        ('P','Practical'),
        ('TU','Tutorial'),
    ]

    CATEGOTY_CHOICES = [
        ('MCQ', 'MCQ'),
        ('THEORY_DESC', 'Theory Descriptive'),
        ('FORMULA_DERIVATION', 'Formulas and Derivation'),
        ('NUMERICAL', 'Numerical'),
        ('INDIVIDUAL_PROJ', 'Individual Project'),
        ('IPE', 'Internal Practical Evaluation (IPE)'),
        ('GROUP_PROJ', 'Group Project'),
        ('VIVA', 'Viva'),
        ('SEMINAR', 'Seminar'),
    ]

    teaching_type = models.CharField(choices=TEACHING_TYPE_CHOICES, max_length=15)
    category = models.CharField(choices=CATEGOTY_CHOICES, max_length=50)
    percentage_weightage = models.PositiveSmallIntegerField(help_text='Percemtage weightage distribution.')
    marks_weightage = models.PositiveSmallIntegerField(help_text='Marks weightage distribution.')

    class Meta:
        verbose_name_plural = 'Weightages'
        verbose_name = 'Weightage'

    def __str__(self):
        return self.subject_set().subject_short_name + ' ' + self.teaching_type + ' ' + self.category


class Subject(models.Model):
    subject_code = models.CharField(primary_key=True, max_length=15, verbose_name='Subject Code')
    subject_short_name = models.CharField(max_length=10, verbose_name='Subject Short Name', help_text='e.g. FCSP-I')
    subject_full_name = models.CharField(max_length=50, verbose_name='Subject Full Name', help_text='Fundamentals of Computer Science using Python-I')
    total_credit = models.PositiveSmallIntegerField(verbose_name='Total Credit', help_text='Total credit of the subject.')
    theory_credit = models.PositiveSmallIntegerField(verbose_name='Theory Credit', help_text='Theory credit of the subject.')
    tutorial_credit = models.PositiveSmallIntegerField(null=True, verbose_name='Tutorial Credit', help_text='Tutorial credit of the subject.')
    practical_credit = models.PositiveSmallIntegerField(null=True, verbose_name='Practical Credit', help_text='Practical credit of the subject.')
    Weightage = models.ManyToManyField("Weightage", verbose_name='Weightage', help_text='Weightage distribution of the subject')

    class Meta:
        verbose_name_plural = 'Subjects'
        verbose_name = 'Subject'

    def __str__(self):
        return self.subject_code + ' '  + self.subject_short_name 
    
class Branch(models.Model):
    branch_code = models.CharField(primary_key=True, max_length=15, verbose_name='Branch Code')
    branch_short_name = models.CharField(max_length=10, verbose_name='Branch Name', help_text='e.g. CSE')
    branch_full_name = models.CharField(max_length=50, verbose_name='Branch Full Name', help_text='e.g. Computer Science and Engineering')
    available = models.BooleanField(default=True, help_text='If branch is currently available to enrollment.')

    class Meta:
        verbose_name_plural = 'Branches'
        verbose_name = 'Branch'

    def __str__(self):
        return self.branch_code + ' '  + self.branch_short_name

class StudentDetail(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    enrolment_no = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(unique=True, max_length=30, verbose_name='Email', help_text='e.g. enrolment_number@ljku.edu.in')
    first_name = models.CharField(max_length=20, verbose_name='First Name')
    middle_name = models.CharField(max_length=20, null=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=20, verbose_name='Last Name')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, verbose_name='Gender')
    birth_date = models.DateField(verbose_name='Birth Date', help_text='dd-mm-yyyy')
    mobile_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?\d{6,15}$',
            message='Mobile number must be in international format with no spaces or special characters.',
        ),
    ], verbose_name='Mobile Number', help_text='e.g. +1234567890')
    branch = models.ForeignKey("Branch", verbose_name='Branch', help_text='Branch details where student is enrolled.', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Student Details'
        verbose_name = 'Student Detail'

    def __str__(self):
        return self.enrolment_no
    

class FacultyAllocation(models.Model):
    faculty = models.ForeignKey("StaffDetail", verbose_name='Faculty', help_text='Faculty details', on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", verbose_name='Subject',help_text='Subject details', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Faculty Allocation'
        verbose_name = 'Faculty Allocation'

    def __str__(self):
        return self.faculty.email
    