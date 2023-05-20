from django.db import models
from django.core.validators import RegexValidator


class StaffDetail(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('T', 'Teaching'),
        ('NT', 'Non-Teaching'),
    ]

    email = models.EmailField(primary_key=True, max_length=100, verbose_name='Email',
                              help_text='e.g. firstname.lastname@ljku.edu.in')
    first_name = models.CharField(max_length=20, verbose_name='First Name')
    middle_name = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=20, verbose_name='Last Name')
    short_name = models.CharField(
        max_length=5, verbose_name='Short Name', help_text='e.g. DKT')
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=1, verbose_name='Gender')
    birth_date = models.DateField(
        verbose_name='Birth Date', help_text='dd/mm/yyyy')
    mobile_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?\d{6,15}$',
            message='Mobile number must be in international format with no spaces or special characters.',
        ),
    ], verbose_name='Mobile Number', help_text='e.g. +1234567890')
    category = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, verbose_name='Category')
    active = models.BooleanField(
        default=True, verbose_name='Active', help_text='Is the staff actively doing his/her job?')

    class Meta:
        verbose_name_plural = 'Staff Details'
        verbose_name = 'Staff Detail'

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class Weightage(models.Model):

    TEACHING_TYPE_CHOICES = [
        ('T', 'Theory'),
        ('P', 'Practical'),
        ('TU', 'Tutorial'),
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

    teaching_type = models.CharField(
        choices=TEACHING_TYPE_CHOICES, verbose_name='Teaching Type', max_length=2)
    category = models.CharField(
        choices=CATEGOTY_CHOICES, verbose_name='Category', max_length=25)
    percentage_weightage = models.PositiveSmallIntegerField(
        verbose_name='Percentage Weightage', help_text='Percentage weightage distribution.')
    marks_weightage = models.PositiveSmallIntegerField(
        verbose_name='Marks Weightage', help_text='Marks weightage distribution.')

    class Meta:
        verbose_name_plural = 'Subject Weightages'
        verbose_name = 'Subject Weightage'

    def __str__(self):
        subject = self.subject_set().first()
        if subject:
            return f'{subject.subject_short_name} {self.teaching_type} {self.category}'
        else:
            return f'{self.teaching_type} {self.category}'


class Subject(models.Model):
    subject_code = models.CharField(
        primary_key=True, max_length=15, verbose_name='Subject Code')
    subject_short_name = models.CharField(
        max_length=10, verbose_name='Subject Short Name', help_text='e.g. FCSP-I')
    subject_full_name = models.CharField(
        max_length=50, verbose_name='Subject Full Name', help_text='Fundamentals of Computer Science using Python-I')
    total_credit = models.PositiveSmallIntegerField(
        verbose_name='Total Credit', help_text='Total credit of the subject.')
    theory_credit = models.PositiveSmallIntegerField(
        verbose_name='Theory Credit', help_text='Theory credit of the subject.')
    tutorial_credit = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='Tutorial Credit', help_text='Tutorial credit of the subject.')
    practical_credit = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='Practical Credit', help_text='Practical credit of the subject.')
    Weightage = models.ManyToManyField(
        'Weightage', verbose_name='Weightage', help_text='Weightage distribution of the subject')

    class Meta:
        verbose_name_plural = 'Subjects'
        verbose_name = 'Subject'

    def __str__(self):
        return f'{self.subject_code} {self.subject_short_name}'


class Branch(models.Model):
    branch_code = models.CharField(
        primary_key=True, max_length=15, verbose_name='Branch Code')
    branch_short_name = models.CharField(
        max_length=10, verbose_name='Branch Name', help_text='e.g. CSE')
    branch_full_name = models.CharField(
        max_length=50, verbose_name='Branch Full Name', help_text='e.g. Computer Science and Engineering')
    available = models.BooleanField(default=True, verbose_name='Available',
                                    help_text='If branch is currently available to enrollment.')

    class Meta:
        verbose_name_plural = 'Branches'
        verbose_name = 'Branch'

    def __str__(self):
        return f'{self.branch_code} {self.branch_short_name}'


class StudentDetail(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    enrolment_no = models.CharField(
        max_length=16, primary_key=True, verbose_name='Enrolmentment No')
    email = models.EmailField(unique=True, max_length=30, verbose_name='Email',
                              help_text='e.g. enrolment_number@ljku.edu.in')
    first_name = models.CharField(max_length=20, verbose_name='First Name')
    middle_name = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=20, verbose_name='Last Name')
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=1, verbose_name='Gender')
    birth_date = models.DateField(
        verbose_name='Birth Date', help_text='dd/mm/yyyy')
    mobile_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?\d{6,15}$',
            message='Mobile number must be in international format with no spaces or special characters.',
        ),
    ], verbose_name='Mobile Number', help_text='e.g. +1234567890')
    branch = models.ForeignKey('Branch', verbose_name='Branch',
                               help_text='Branch details where student is enrolled.', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Student Details'
        verbose_name = 'Student Detail'

    def __str__(self):
        return f'{self.enrolment_no}'


class FacultyAllocation(models.Model):
    faculty = models.ForeignKey('StaffDetail', verbose_name='Faculty',
                                help_text='Faculty details', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', verbose_name='Subject',
                                help_text='Subject details', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Faculty Allocation'
        verbose_name = 'Faculty Allocation'

    def __str__(self):
        return f'{self.faculty.email}'


class Batch(models.Model):
    name = models.CharField(max_length=10, verbose_name='Batch Name')
    faculty = models.ManyToManyField(
        'FacultyAllocation', verbose_name='Faculty', help_text='Faculty allocated to batch')
    student = models.ManyToManyField(
        'StudentDetail', verbose_name='Student', help_text='Student allocated to batch')

    class Meta:
        verbose_name_plural = 'Batches'
        verbose_name = 'Batch'

    def __str__(self):
        department = self.department_set().first()
        if department:
            return f'{department.year} {department.semester} {department.name} {self.name}'
        else:
            return f'{self.name}'


class StudyResource(models.Model):
    subject = models.ForeignKey(
        'Subject', verbose_name='Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name='Resource Name')
    resource_type = models.CharField(
        max_length=50, verbose_name='Resource Type')
    upload_date = models.DateField(
        verbose_name='Upload Date', auto_now=True, help_text='dd/mm/yyyy')
    file = models.FileField(
        verbose_name='Study Resource File', upload_to='study_resources/')

    class Meta:
        verbose_name_plural = 'Study Resources'
        verbose_name = 'Study Resource'

    def __str__(self):
        return f'{self.subject.subject_short_name} {self.resource_type}'


class Department(models.Model):
    year = models.CharField(
        max_length=7, verbose_name='Year', help_text='e.g. 2022-23')
    semester = models.PositiveSmallIntegerField(
        verbose_name='Semester', help_text='e.g. 1')
    branch = models.ManyToManyField('Branch', verbose_name='Branch')
    batch = models.ManyToManyField('Batch', verbose_name='Batch')
    name = models.CharField(
        max_length=20, verbose_name='Department Name', help_text='e.g. CE_IT_2')
    hod = models.ForeignKey(
        'StaffDetail', verbose_name='Head of Department', on_delete=models.CASCADE)
    study_resources = models.ManyToManyField(
        'StudyResource', verbose_name='Study Resources')

    class Meta:
        verbose_name_plural = 'Departments'
        verbose_name = 'Department'

    def __str__(self):
        return f'{self.year} {self.semester} {self.name}'


class Attendance(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('R', 'Regular'),
        ('PRX', 'proxy')
    )
    date = models.DateField(verbose_name='Date', help_text='dd/mm/yyyy')
    subject = models.ForeignKey(
        'Subject', verbose_name='Subject', on_delete=models.CASCADE)
    mode = models.CharField(
        max_length=5, choices=RESOURCE_TYPE_CHOICES, default='R', verbose_name='Mode')
    present = models.BooleanField(
        verbose_name='Present', help_text='If student is present or not.')

    class Meta:
        verbose_name_plural = 'Attendances'
        verbose_name = 'Attendance'
        # Sort by date field in descending order (most recent first)
        ordering = ['-date']

    def __str__(self):
        student_semester_record = self.studentsemesterrecord_set.first()
        if student_semester_record:
            department = student_semester_record.department
            return f'{department.semester} {department.name} {self.subject.subject_short_name} {self.date}'
        else:
            return f'{self.subject.subject_short_name} {self.date}'


class RemedialTestResult(models.Model):
    theory = models.FloatField(verbose_name='Theory', null=True, blank=True)
    individual_project = models.FloatField(
        verbose_name='Individual Project', null=True, blank=True)
    group_project = models.FloatField(
        verbose_name='Group project', null=True, blank=True)
    ipe = models.FloatField(verbose_name='IPE', null=True, blank=True)
    other = models.FloatField(verbose_name='other', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Remedial Test Results'
        verbose_name = 'Remedial Test Result'

    def __str__(self):
        return f'Remedial Test Result {self.id}'


class TestResult(models.Model):
    subject = models.ForeignKey(
        'Subject', verbose_name='Subject', on_delete=models.CASCADE)
    T1 = models.FloatField(verbose_name='T1', null=True, blank=True,
                           help_text='Test 1 Result')
    T2 = models.FloatField(verbose_name='T2', null=True, blank=True,
                           help_text='Test 2 Result')
    T3 = models.FloatField(verbose_name='T3', null=True, blank=True,
                           help_text='Test 3 Result')
    T4 = models.FloatField(verbose_name='T4', null=True, blank=True,
                           help_text='Test 4 Result')
    T1_file = models.FileField(
        verbose_name='T1 Files', upload_to='test_files/', null=True, blank=True, help_text='Test 1 Scanned Copy')
    T2_file = models.FileField(
        verbose_name='T2 Files', upload_to='test_files/', null=True, blank=True, help_text='Test 2 Scanned Copy')
    T3_file = models.FileField(
        verbose_name='T3 Files', upload_to='test_files/', null=True, blank=True, help_text='Test 3 Scanned Copy')
    T4_file = models.FileField(
        verbose_name='T4 Files', upload_to='test_files/', null=True, blank=True, help_text='Test 4 Scanned Copy')

    individual_project = models.FloatField(
        verbose_name='Individual Project', null=True, blank=True)
    group_project = models.FloatField(
        verbose_name='Group Project', null=True, blank=True)
    ipe = models.FloatField(
        verbose_name='IPE', null=True, blank=True, help_text='IPE Marks')
    other = models.FloatField(verbose_name='Other', null=True, blank=True)
    bonus = models.FloatField(
        verbose_name='Bonus', null=True, blank=True, help_text='HOD Bonus, Attendance Bonus etc.')
    remedial_result = models.ManyToManyField(
        'RemedialTestResult', verbose_name='Remedial Result')

    class Meta:
        verbose_name_plural = 'Test Results'
        verbose_name = 'Test Result'

    def _str_(self):
        student_semester_record = self.studentsemesterrecord_set().first()
        return_text = ''
        if student_semester_record:
            student = student_semester_record.student
            return_text += f'{student.enrolment_no}'
            department = student_semester_record.department.first()
            if department:
                return_text += f' {department.semester}'
        return_text += f' {self.subject.subject_short_name}'
        return return_text


class MOOCCourses(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='Course')
    platform = models.CharField(
        max_length=30, verbose_name='Platform', help_text='e.g. Coursera')
    university = models.CharField(
        max_length=60, verbose_name='University')

    class Meta:
        verbose_name_plural = 'MOOC Courses'
        verbose_name = 'MOOC Course'

    def _str_(self):
        return f'{self.course_name}'


class MOOCResult(models.Model):
    course = models.ForeignKey(
        'MOOCCourses', verbose_name='MOOC Course', on_delete=models.CASCADE)
    percentage = models.FloatField(
        verbose_name='Percentage', null=True, blank=True)
    certificate = models.URLField(
        verbose_name='Certificate', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'MOOC Results'
        verbose_name = 'MOOC Result'

    def _str_(self):
        return f'{self.course.course_name}'


class IndividualProject(models.Model):
    subject = models.ForeignKey(
        'Subject', verbose_name='Subject', on_delete=models.CASCADE)
    definition = models.TextField(verbose_name='Project Definition')
    create_timestamp = models.DateTimeField(
        verbose_name='Create Timestamp', auto_now_add=True)
    update_timestamp = models.DateTimeField(
        verbose_name='Update Timestamp', auto_now=True)

    class Meta:
        verbose_name_plural = 'Individual Projects'
        verbose_name = 'Individual Project'

    def _str_(self):
        student_semester_record = self.studentsemesterrecord_set().first()
        return_text = self.subject.subject_short_name
        if student_semester_record:
            department = student_semester_record.department.first()
            if department:
                return_text = f'{department.year} {department.semester} {department.name} {self.subject.subject_short_name}'
            return_text += f' {student_semester_record.roll_no}'
        return return_text


class GroupProject(models.Model):
    subject = models.ForeignKey(
        'Subject', verbose_name='Subject', on_delete=models.CASCADE)
    definition = models.TextField(verbose_name='Project Definition')
    create_timestamp = models.DateTimeField(
        verbose_name='Create Timestamp', auto_now_add=True)
    update_timestamp = models.DateTimeField(
        verbose_name='Update Timestamp', auto_now=True)

    class Meta:
        verbose_name_plural = 'Group Projects'
        verbose_name = 'Group Project'

    def _str_(self):
        student_semester_records = self.studentsemesterrecord_set()
        return_text = self.subject.subject_short_name
        if student_semester_records:
            department = student_semester_records.first().department
            if department:
                return_text = f'{department.year} {department.semester} {department.name} {self.subject.subject_short_name}'
            for student_semester_record in student_semester_records:
                return_text += f' {student_semester_record.roll_no}'
        return return_text


class StudentSemesterRecord(models.Model):
    student = models.ForeignKey(
        'StudentDetail', verbose_name='Student Details', on_delete=models.CASCADE)
    department = models.ForeignKey(
        'Department', verbose_name='Department', on_delete=models.CASCADE)
    roll_no = models.PositiveSmallIntegerField(verbose_name='Roll No')
    attendance = models.ManyToManyField(
        'Attendance', verbose_name='Attendance')
    test_result = models.ManyToManyField(
        'TestResult', verbose_name='Test Result'),
    MOOC_courses = models.ManyToManyField(
        'MOOCResult', verbose_name='MOOC Courses')
    individual_project = models.ManyToManyField(
        'IndividualProject', verbose_name='Individual Project')
    group_project = models.ManyToManyField(
        'GroupProject', verbose_name='Group Project')

    class Meta:
        verbose_name_plural = 'Student Semester Records'
        verbose_name = 'Student Semester Record'

    def _str_(self):
        return f'{self.student.enrolment_no}'